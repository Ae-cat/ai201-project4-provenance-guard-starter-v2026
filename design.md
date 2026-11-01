# Design notes — Milestone 1

Written before building anything. The path and signals are summarised in the README; this file holds the false-positive trace and the endpoint contracts.

> The numbers in the false-positive trace are **hypothetical**. They illustrate the path, and will be replaced with real scores after the Milestone 4 calibration inputs.

---

## The false-positive trace

**Who:** a student writing in their second language. They wrote a short, plain essay entirely themselves, using vocabulary they're sure of and short sentences.

**What happens in the service (hypothetical numbers):**

| Step | Result |
|---|---|
| Signal one (`detector.py`) | **0.88.** Common words in short sentences are very predictable to gpt2, so it reads as machine-like. |
| Signal two (`stylometry.py`) | **0.70.** Even sentence lengths and repeated vocabulary look uniform. |
| Combined (`combine_signals`, weights 0.5 / 0.5) | **0.79** |
| Label (`score_to_label`, AI threshold currently 0.65) | **high-confidence AI** |

**What the label says to them:** the high-confidence AI label, which tells the writer the work was probably AI-generated. It is wrong, and the writer has no way to know why it was reached. (The label wording is a Milestone 5 decision.)

**What they can do:** send `POST /appeal` with their `content_id` and their reasoning. The item moves to `under_review`, the appeal is written to the log next to the original decision, and they get a confirmation. There is no automatic re-checking, so a person has to review it.

**What this means for my thresholds:**

- Both signals lean the same wrong way on plain writing, so averaging them doesn't help here. Two signals that agree can both be wrong.
- A wrong accusation costs the writer much more than a missed AI text costs the site. So the high-confidence AI line should sit **high**, and the wide middle should be "unsure." In `config.py` that means raising `AI_THRESHOLD` above the placeholder 0.65, decided in Milestone 5.
- The AI label should avoid wording that sounds like an accusation, and the page should make the appeal path visible.

---

## Endpoint contracts

### `POST /submit`

**In (JSON):**

| Field | Type | Rules |
|---|---|---|
| `text` | string | required, not empty or whitespace only, at most 10,000 characters |
| `creator_id` | string | required, not empty |

**Out, 200 (JSON):**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | unique id for this submission (UUID), used by `/appeal` |
| `guess` | string | `"ai"`, `"human"` or `"unsure"` |
| `confidence` | number 0–1 | the combined score. **Higher means more likely AI**, so a low value supports `"human"`. |
| `label` | string | the full sentence shown to the writer |
| `model_score` | number 0–1 | signal one, higher = more likely AI |
| `style_score` | number 0–1 | signal two, higher = more likely AI |

**Errors (JSON `{"error": "...", "message": "..."}`):**

| Case | Status | `error` |
|---|---|---|
| body isn't JSON, or `text` / `creator_id` missing | 400 | `missing_field` |
| `text` empty or whitespace only | 400 | `empty_text` |
| `text` under 20 words (a 3-word input scored a meaningless 0.0005) | 400 | `text_too_short` |
| `text` over 10,000 characters | 413 | `text_too_long` |
| model not downloaded or can't load | 503 | `detector_unavailable` |

Every rejected request should still leave a log trace (`audit.log_rejection`).

Note: the detector only reads the first ~400 tokens (about 300 words), so text longer than that is accepted but only its start is scored.

### `POST /appeal`

**In (JSON):**

| Field | Type | Rules |
|---|---|---|
| `content_id` | string | required, must match an existing submission |
| `reasoning` | string | required, not empty, at most 2,000 characters |

The writer's `creator_id` isn't sent. The route looks it up from the original entry with `audit.entries_for(content_id)`.

**Out, 200 (JSON):**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | echoed back |
| `status` | string | `"under_review"` |
| `message` | string | plain confirmation that the appeal was recorded |

**Errors:**

| Case | Status | `error` |
|---|---|---|
| `content_id` or `reasoning` missing or empty | 400 | `missing_field` |
| `content_id` not in the log | 404 | `unknown_content_id` |
| item is already `under_review` | 409 | `already_under_review` |

The log is append-only: the original `decided` entry stays, and the appeal is added after it with `event: "appeal"` and `status: "under_review"`. An item's current status is the status on its latest entry.

---

## Could someone else build against this without asking me?

I read both contracts back as someone who has never seen this project. Three things could have caused a question, and here is how each is settled:

1. **What does `confidence` mean?** It is the combined score, where **higher means more likely AI**. It is *not* how sure the system is of its guess, so a `"human"` guess comes with a low value (for example 0.12). The field name is easy to misread, so the response contract keeps this definition and the README says it too.
2. **How big can `text` be?** At most 10,000 characters. The detector only reads the first ~400 tokens (about 300 words), so longer text is accepted but only its start is scored. The cap just stops absurdly large requests.
3. **What if someone appeals twice?** The second appeal gets `409 already_under_review`. The item is already waiting for review, and rejecting the repeat keeps one appeal per item in the log. If later testing shows writers need to add more reasoning, this can change.

With those settled, a developer has every field, type, limit and error code they need for both endpoints.
