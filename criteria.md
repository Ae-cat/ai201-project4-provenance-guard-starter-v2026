# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False positives
Of 5 pieces of writing that a human wrote, at most 2 receive the high-confidence AI label.

**Why this target:** Many people don't write in a formal or varied style. Someone writing in a language they know less well tends to use simple, common words, which look like AI to the system. I expect some wrongly flagged writers because of that, and I accept up to 2 in 5. Furthermore, human writers tend to use less punctuation than AI-generated text.

---

## 2. Score spread

Clearly-AI text and clearly-human text score about 0.7 apart on the combined score (AI text higher), in at least 4 of 5 pairs of texts. I choose and label each pair as clearly-AI and clearly-human before running anything.

**Why this target:** 0.7 out of 1 is a large gap, so a few pairs may fall short and score only 0.5 or 0.6 apart. That is why I only require it in 4 of 5.

---

## 3. Label coverage

All three labels (high-confidence human, unsure, high-confidence AI) appear at least once across 5 test texts, and at least 4 of the 5 get the label I expected for them before running.

**Why this target:** Every label has to be reachable, or part of the system isn't working. I allow 1 miss in 5 because a text with unusual word choices can be classified differently from how I expected.

---

## 4. The appeal path

In 5 of 5 appeals sent with a valid `content_id`, the response confirms the appeal, `GET /log` shows a new appeal entry with status `under_review` next to the original decision, and the original entry is unchanged. An appeal with an unknown `content_id` returns an error (not a success) in 5 of 5 attempts.

**Why this target:** The appeal is the only recourse for a writer wrongly flagged as AI, and the log is what a human reviewer would read. Unlike the detection, the appeal isn't a guess, so I allow no failures.

---

## 5. Bad input

For 5 bad inputs (including at least one with missing text, one with empty text and one with enormous text), the service returns an error message that tells the writer what to fix, such as "please provide text input," and does not crash, in 5 of 5 attempts.

**Why this target:** A crash on bad input is a common real failure, and it should never happen. A clear message also tells writers they forgot to include any text.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->


---

# Capstone acceptance criteria — the catch-all error handler

Written before any capstone results exist. The extension is a catch-all error handler on `/submit` (plus a `duration_ms` field in the log). Each criterion is tested over three trials and has to hold in all three.

## 1. Crash response

Of 10 deliberately triggered crashes on `/submit`, at least 9 return HTTP 500 with a JSON body containing `error` and `message`, and none of the response bodies contains "Traceback" or a file path.

*Why:* a caller needs a consistent, structured answer when something unexpected fails, and a stack trace would show the service's internals to a stranger.

*How to run it (added after the runs; no target was changed).* Start the service with `AI201_FAULT_INJECTION=1 python app.py`. Send 10 `POST /submit` requests, each with its own `creator_id` and a `text` that begins with `[[inject-fault]]` (the test switch raises a deliberate error). For each response, check that the status is 500, that the body parses as JSON with both `error` and `message`, and that the body text contains none of "Traceback", ".py" or a file path.

## 2. Crash logging

Of those same 10 crashes, 10 produce an `error` entry in the audit log with `error_type`, `duration_ms` and `creator_id`.

*Why:* a failure that leaves no record is one nobody investigates.

*How to run it (added after the runs; no target was changed).* Read `logs/audit.jsonl` (or `GET /log`). For each of the 10 `creator_id`s used in criterion 1, find an entry whose `event` is `error`, and check that `error_type`, `duration_ms` and `creator_id` are all present and not empty.

## 3. Duration tracking

At least 95% of the decision, rejection and error entries written during the test run have a numeric `duration_ms` (present and not null).

*Why:* timing is only useful if it is recorded on every outcome, not just on successful submissions.

*How to run it (added after the runs; no target was changed).* After the test traffic, take every entry in `logs/audit.jsonl` written during the run whose `event` is missing (a decision), `rejected` or `error` (appeals are not counted). Divide the number that have a numeric `duration_ms` by the total.

## 4. Original endpoints preserved

All 23 of these checks pass: 10 normal `/submit` requests return 200 with all six fields (`content_id`, `guess`, `confidence`, `label`, `model_score`, `style_score`); 10 `/ping` requests return 200; one empty-text request returns 400; one over-length request returns 413; and the 7th request within a minute from one `creator_id` returns 429. None of them returns 500.

*Why:* the catch-all must not swallow errors the service already handled on purpose.

*How to run it (added after the runs; no target was changed).* With the service running, send: 10 `POST /submit` requests with a valid text of at least 20 words (each must return 200 with all six fields); 10 `POST /ping` requests with `{"message": "hello"}` (each must return 200); one `POST /submit` with empty text (must return 400); one `POST /submit` with about 12,500 characters (must return 413); and 7 `POST /submit` requests in under a minute from the same `creator_id` (the 7th must return 429). That is 23 checks, and none may return 500.

## 5. Crash handling when the log can't be written

With the audit log made unwritable (`chmod 444 logs/audit.jsonl`), 5 of 5 requests that would crash still return a JSON 500 with `error` and `message`, with no HTML error page and no hang.

*Why:* a logging failure is the one failure the service can't record, and the caller should still get an answer.

*How to run it (added after the runs; no target was changed).* Run `chmod 444 logs/audit.jsonl` so the log can't be written. Send 5 fault-injected requests as in criterion 1, with a client timeout of 10 seconds. Each must return a 500 with a JSON body containing `error` and `message` inside that timeout. Then restore the log with `chmod 644 logs/audit.jsonl`.

> **Note on the "how to run it" lines.** I added them after the first runs because the original wording said "deliberately triggered crash" and "the log made unwritable" without saying how a reader would do that. The targets and the original sentences above are unchanged. These lines are the steps my `run_capstone_eval.py` already performed.
