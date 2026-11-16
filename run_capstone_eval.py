#!/usr/bin/env python3
"""
Capstone: run the five criteria in criteria.md, three trials each.

Start the service with fault injection on, from this repository:

    AI201_FAULT_INJECTION=1 python app.py

Then, in another terminal:

    python run_capstone_eval.py --label before

Criterion 5 makes the audit log unwritable on purpose (chmod 444) and puts the
permissions back afterwards, even if you press Ctrl+C.
"""

import argparse
import json
import re
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

import config

BASE = "http://127.0.0.1:5000"
LOG = Path(config.AUDIT_LOG)
GOOD = ("I went for a long walk by the river this morning and it was lovely and quiet, "
        "so I stopped at the little cafe near the bridge and had a coffee before heading home.")
FAULT = config.FAULT_MARKER + " " + GOOD
SIX = {"content_id", "guess", "confidence", "label", "model_score", "style_score"}
LEAK = re.compile(r'Traceback|File "|\.py\b|/Users/|/home/')

samples = {}


def post(path, body, timeout=30):
    return requests.post(BASE + path, json=body, timeout=timeout)


def log_lines():
    return LOG.read_text(encoding="utf-8").splitlines() if LOG.exists() else []


def entries_since(n):
    out = []
    for line in log_lines()[n:]:
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return out


def is_json_error(r):
    if not r.headers.get("content-type", "").startswith("application/json"):
        return False
    try:
        body = r.json()
    except ValueError:
        return False
    return isinstance(body, dict) and "error" in body and "message" in body


def trial(t):
    start_lines = len(log_lines())
    crash_users = [f"cap_t{t}_crash_{i}" for i in range(1, 11)]

    # ── Criterion 1 and 2: ten crashes on /submit ──────────────────────────
    ok1 = 0
    for i, who in enumerate(crash_users, 1):
        r = post("/submit", {"text": FAULT, "creator_id": who})
        if r.status_code == 200:
            sys.exit("A crash didn't happen. Restart the service with AI201_FAULT_INJECTION=1.")
        good = r.status_code == 500 and is_json_error(r) and not LEAK.search(r.text)
        ok1 += good
        if t == 1 and i == 1:
            samples["crit1"] = f"status {r.status_code}\n{r.text.strip()}"
    entries = entries_since(start_lines)
    ok2 = 0
    for who in crash_users:
        e = [x for x in entries if x.get("event") == "error" and x.get("creator_id") == who]
        if e and all(k in e[-1] and e[-1][k] not in (None, "") for k in ("error_type", "duration_ms", "creator_id")):
            ok2 += 1
            if t == 1 and "crit2" not in samples:
                samples["crit2"] = json.dumps(e[-1], indent=2)

    # ── Criterion 4: the original endpoints ───────────────────────────────
    ok4 = 0
    for i in range(1, 11):
        r = post("/submit", {"text": GOOD, "creator_id": f"cap_t{t}_normal_{i}"})
        ok4 += r.status_code == 200 and SIX <= set(r.json())
        if t == 1 and i == 1:
            samples["crit4_submit"] = f"status {r.status_code}\n{json.dumps(r.json(), indent=2)}"
    for _ in range(10):
        ok4 += post("/ping", {"message": "hello"}).status_code == 200
    r = post("/submit", {"text": "", "creator_id": f"cap_t{t}_400"})
    ok4 += r.status_code == 400
    s400 = f"400 check: status {r.status_code} {r.text.strip()}"
    r = post("/submit", {"text": "word " * 2500, "creator_id": f"cap_t{t}_413"})
    ok4 += r.status_code == 413
    s413 = f"413 check: status {r.status_code} {r.text.strip()}"
    codes = [post("/submit", {"text": GOOD, "creator_id": f"cap_t{t}_rate"}).status_code for _ in range(7)]
    ok4 += codes[-1] == 429
    s429 = f"429 check: seven requests from one creator gave {codes}"
    if t == 1:
        samples["crit4_codes"] = "\n".join([s400, s413, s429])

    # ── Criterion 3: duration_ms across everything written this trial ──────
    entries = entries_since(start_lines)
    judged = [e for e in entries if e.get("event") in (None, "rejected", "error")]
    with_dur = [e for e in judged
                if isinstance(e.get("duration_ms"), (int, float)) and not isinstance(e.get("duration_ms"), bool)]
    share = len(with_dur) / len(judged) if judged else 0.0
    missing = [e for e in judged if e not in with_dur]
    if t == 1:
        kinds = sorted({(e.get("event") or "decision", e.get("reason", "")) for e in missing})
        samples["crit3"] = (f"{len(with_dur)} of {len(judged)} entries had a numeric duration_ms\n"
                            f"entries without it: {kinds if kinds else 'none'}")

    # ── Criterion 5: crashes while the log can't be written ────────────────
    ok5 = 0
    mode = LOG.stat().st_mode
    LOG.chmod(0o444)
    try:
        for i in range(1, 6):
            began = time.perf_counter()
            try:
                r = post("/submit", {"text": FAULT, "creator_id": f"cap_t{t}_nolog_{i}"}, timeout=10)
            except requests.RequestException as exc:
                if t == 1:
                    samples["crit5"] = samples.get("crit5", "") + f"request {i}: {exc!r}\n"
                continue
            good = r.status_code == 500 and is_json_error(r) and (time.perf_counter() - began) < 10
            ok5 += good
            if t == 1 and i == 1:
                samples["crit5"] = f"status {r.status_code}\n{r.text.strip()}"
    finally:
        LOG.chmod(mode)

    return {"c1": ok1, "c2": ok2, "c3": share, "c3n": (len(with_dur), len(judged)), "c4": ok4, "c5": ok5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    label = ap.parse_args().label

    try:
        requests.get(BASE + "/health", timeout=5)
    except requests.RequestException:
        sys.exit("The service isn't running. Start it with: AI201_FAULT_INJECTION=1 python app.py")
    if not LOG.exists():
        sys.exit(f"No audit log at {LOG}. Run this from the repository the service is running in.")

    print("Warm-up (loads the model; not counted)...")
    before = len(log_lines())
    post("/submit", {"text": GOOD, "creator_id": "cap_warmup"}, timeout=120)
    if len(log_lines()) == before:
        sys.exit(f"The service answered, but nothing new appeared in {LOG}.\n"
                 "It is probably running from a different folder (for example the clean-checkout copy). "
                 "Stop it, then start it from THIS repository with: AI201_FAULT_INJECTION=1 python app.py")

    results = []
    for t in (1, 2, 3):
        print(f"Trial {t}...")
        results.append(trial(t))
        print("  ", results[-1])

    rows = [
        ("1. Crash response", "at least 9 of 10", [f"{r['c1']}/10" for r in results], [r["c1"] >= 9 for r in results]),
        ("2. Crash logging", "10 of 10", [f"{r['c2']}/10" for r in results], [r["c2"] == 10 for r in results]),
        ("3. Duration tracking", "at least 95%",
         [f"{r['c3']*100:.0f}% ({r['c3n'][0]}/{r['c3n'][1]})" for r in results], [r["c3"] >= 0.95 for r in results]),
        ("4. Original endpoints preserved", "23 of 23", [f"{r['c4']}/23" for r in results], [r["c4"] == 23 for r in results]),
        ("5. Crash handling, log unwritable", "5 of 5", [f"{r['c5']}/5" for r in results], [r["c5"] == 5 for r in results]),
    ]
    out = ["# Capstone run — " + label, "",
           f"Run at {datetime.now().strftime('%Y-%m-%d %H:%M')} against {BASE}, three trials, nothing changed in between.", "",
           "| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |", "|---|---|---|---|---|---|"]
    for name, target, cells, holds in rows:
        out.append(f"| {name} | {target} | {cells[0]} | {cells[1]} | {cells[2]} | {'MET' if all(holds) else 'MISSED'} |")
    out += ["", "## Real output from trial 1", "",
            "**Criterion 1** (`app.py::unexpected_error`), first crash response:", "```", samples.get("crit1", ""), "```", "",
            "**Criterion 2** (`audit.py::log_error`), the log entry for that crash:", "```json", samples.get("crit2", "none"), "```", "",
            "**Criterion 3** (`app.py::_duration_ms`, passed into `audit.py`):", "```", samples.get("crit3", ""), "```", "",
            "**Criterion 4**, one normal submission, then the three error-code checks:", "```",
            samples.get("crit4_submit", ""), "", samples.get("crit4_codes", ""), "```", "",
            "**Criterion 5** (`app.py::unexpected_error` with the log unwritable), first response:", "```",
            samples.get("crit5", ""), "```", ""]
    Path("results").mkdir(exist_ok=True)
    path = Path("results") / f"capstone_run_{datetime.now().strftime('%Y-%m-%d_%H%M')}_{label}.md"
    path.write_text("\n".join(out), encoding="utf-8")
    print()
    print("\n".join(out[4:11]))
    print(f"\nWrote {path}")


if __name__ == "__main__":
    main()
