#!/usr/bin/env python3
"""
Run criterion 4 (the appeal path) three times.  <- UNIT 8, MILESTONE 3

    python app.py                                  # in one terminal
    python run_appeal_eval.py --label before       # in another

run_eval.py only sends text to /submit, and an appeal needs a real content_id
from an earlier submission, so this script does the whole sequence itself.

Each trial does five valid appeals and five appeals with an unknown id:

  valid:    submit a text, appeal its content_id, then check that
              - the response is 200 and says status "under_review"
              - GET /log has a new appeal entry for that content_id with
                status "under_review"
              - the original decision entry is unchanged
  unknown:  appeal an id that was never issued and check the service returns
            an error (a 4xx), not a success.

Writes results/appeal_run_<date>_<label>.md with the real responses.
"""

import argparse
import datetime as dt
import json
import sys
import uuid

import requests

import config

DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"

TEXTS = [
    "I spent the whole afternoon repainting the hallway and I still found a patch near the door that I had missed completely.",
    "The meeting ran long because nobody could agree on the schedule, so we decided to talk again on Thursday morning.",
    "My sister called last night to say she is moving across the country, and I honestly did not know what to say to her.",
    "We tried the new bakery on the corner today and the bread was great, though the line took nearly twenty minutes to get through.",
    "After three weeks of practice I can finally play the first page of the song without stopping to look at the notes.",
]


def entries_for(session, url, content_id):
    log = session.get(f"{url}/log", timeout=30).json()
    return [e for e in log["entries"] if e.get("content_id") == content_id]


def valid_appeal(session, url, text, trial, n):
    record = {"case": f"valid appeal {n}", "checks": {}}
    creator = f"eval_appeal_{trial}_{n}"
    sub = session.post(f"{url}/submit", json={"text": text, "creator_id": creator}, timeout=90)
    record["submit_status"] = sub.status_code
    if sub.status_code != 200:
        record["error"] = f"submit failed: {sub.text[:200]}"
        record["passed"] = False
        return record
    content_id = sub.json()["content_id"]
    record["content_id"] = content_id

    before = [e for e in entries_for(session, url, content_id) if "event" not in e]

    resp = session.post(f"{url}/appeal", json={"content_id": content_id,
                                               "reasoning": "I wrote this myself."}, timeout=30)
    body = resp.json() if resp.content else {}
    record["appeal_status"] = resp.status_code
    record["appeal_response"] = body

    after = entries_for(session, url, content_id)
    decisions = [e for e in after if "event" not in e]
    appeals = [e for e in after if e.get("event") == "appeal"]

    record["checks"] = {
        "response is 200 with under_review": resp.status_code == 200 and body.get("status") == "under_review",
        "appeal entry in log with under_review": len(appeals) == 1 and appeals[0].get("status") == "under_review",
        "original decision unchanged": bool(before) and decisions == before,
    }
    record["log_entries"] = after
    record["passed"] = all(record["checks"].values())
    return record


def unknown_appeal(session, url, n):
    fake = str(uuid.uuid4())
    resp = session.post(f"{url}/appeal", json={"content_id": fake,
                                               "reasoning": "I wrote this myself."}, timeout=30)
    body = resp.json() if resp.content else {}
    return {
        "case": f"unknown id {n}",
        "content_id": fake,
        "appeal_status": resp.status_code,
        "appeal_response": body,
        "checks": {"returns an error, not a success": 400 <= resp.status_code < 500},
        "passed": 400 <= resp.status_code < 500,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()

    session = requests.Session()
    try:
        session.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        sys.exit(f"Nothing answering at {args.url}. Start it:  python app.py")

    trials = []
    for trial in range(1, args.trials + 1):
        results = [valid_appeal(session, args.url, text, trial, n)
                   for n, text in enumerate(TEXTS, 1)]
        results += [unknown_appeal(session, args.url, n) for n in range(1, 6)]
        valid_ok = sum(r["passed"] for r in results if r["case"].startswith("valid"))
        unknown_ok = sum(r["passed"] for r in results if r["case"].startswith("unknown"))
        print(f"trial {trial}: valid appeals {valid_ok}/5 · unknown ids refused {unknown_ok}/5")
        trials.append({"valid": valid_ok, "unknown": unknown_ok, "results": results})

    write_report(trials, args)


def write_report(trials, args):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"appeal_run_{stamp}{label}.md"

    lines = [f"# Appeal path (criterion 4){f' — {args.label}' if args.label else ''}", "",
             "- Produced by: `run_appeal_eval.py::main`",
             f"- {len(trials)} trials · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}", "",
             "| Trial | Valid appeals passing all checks | Unknown ids refused |",
             "|---|---|---|"]
    for i, t in enumerate(trials, 1):
        lines.append(f"| {i} | {t['valid']}/5 | {t['unknown']}/5 |")
    lines += ["", "---", "", "## What actually came back", ""]
    for i, t in enumerate(trials, 1):
        lines += [f"### Trial {i}", "", "```json", json.dumps(t["results"], indent=2), "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
