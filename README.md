# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

A writer submits text with a creator ID, and it passes through these steps:

1. **`POST /submit` (`app.py`)** receives JSON with `text` and `creator_id`. It checks the input (missing, empty or too-long text is rejected) and adds a **`content_id`** that identifies this submission from here on, including in the appeal.
2. **`detector.py` (signal one)** receives the text and adds the **model score**: a 0–1 number where higher means more likely AI. It runs gpt2 locally and measures perplexity, meaning how predictable the text is.
3. **`stylometry.py` (signal two)** receives the text and adds the **style score**: a 0–1 number where higher means more likely AI. It measures the shape of the text: sentence-length spread, vocabulary variety and punctuation.
4. **`scoring.py::combine_signals`** receives both scores and adds the **combined score** (0–1). The weights are defined in `config.py`.
5. **`scoring.py::score_to_label`** receives the combined score and adds the **guess** (`ai`, `human` or `unsure`) and the **label text**, a plain sentence a non-technical reader can understand. Thresholds are in `config.py`.
6. **`audit.py`** receives the full decision and appends it to `logs/audit.jsonl`: timestamp, `content_id`, `creator_id`, guess, both signal scores, combined score, label and status (`decided`).
7. **The response** returns `content_id`, `guess`, `confidence`, `label`, `model_score` and `style_score` to the writer. `confidence` is the combined score, where higher means more likely AI (not how sure the system is of its guess). If the writer disagrees, `POST /appeal` takes the `content_id` and their reasoning and moves the item to `under_review`.

The full endpoint contracts and the false-positive trace are in [design.md](design.md).

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to a language model (gpt2, running locally), as perplexity. Low perplexity means the model finds the text easy to predict. The result is squashed onto a 0–1 score where higher means more likely AI.

**Why that might differ between human and AI writing:** AI writes by repeatedly choosing a likely next word, so its text tends to be easy for a model to predict. Human writing wanders more: odd word choices, abrupt turns, specific details.

**What it can't see:** Predictability is not authorship. Human writing can be predictable too, especially with direct quotes and common expressions. The writers most at risk are the ones who write plainly with common words and short sentences, such as non-native English writers, younger writers, or anyone writing simply on purpose. They can score as machine-like even though they wrote every word. AI writing can also be unpredictable, so this signal alone can't determine who wrote a piece.

### Signal two — the style signal

**What it measures:** The shape of the text as text, without understanding it: how much sentence length varies, how varied the vocabulary is (unique words over total words), and how much punctuation is used.

**Why that might differ between human and AI writing:** AI prose tends toward even, mid-length sentences and a narrower band of vocabulary. Human writing is lumpier, for example a three-word sentence next to a forty-word one.

**What it can't see:** It can't read, so it has no idea what the text says. Many human writers have wide vocabularies and polished technique, which can look AI-like. AI can be prompted to imitate a person's style. Cheap changes such as adding typos, breaking up sentences or pasting in a quotation shift the score without changing who wrote the text.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Normally, the combined score is a weighted average of the model score and the style score. But if the two signals differ by more than 0.30, I don't average them. I use the lower (more human) of the two instead. I chose this because a wrongly accused writer pays more than a missed AI text does, so an AI-leaning combined score should need *both* signals to lean that way. The cost is that when the signals split on text that really is AI, it comes out lower and is more likely to land in "unsure" instead of "AI".

**The numbers:**

| Setting | Value | Where |
|---|---|---|
| Model signal weight | 0.5 | `config.py::WEIGHT_MODEL_SIGNAL` |
| Style signal weight | 0.5 | `config.py::WEIGHT_STYLE_SIGNAL` |
| Disagreement gap | 0.30 | `config.py::DISAGREEMENT_GAP` |
| Style measure weights (spread / vocabulary / punctuation) | 0.5 / 0.3 / 0.2 | `config.py::STYLE_WEIGHT_*` |

The style measures are scaled onto 0–1 with first-guess cut-offs set at the top of `stylometry.py`. They are not calibrated yet.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

My `formal_human` test text (a polite message I wrote myself) scored 0.583 on the model signal, which leans AI, but 0.250 on the style signal, which leans human. That is a gap of 0.333, more than 0.30, so my rule uses the lower score and the combined score is 0.250. A plain average would have given 0.417, so the rule moves a real person's writing further from an AI label. The same rule also pulls clearly-AI text down: my `ai` sample scored 0.834 on the model but only 0.460 on style, so its combined score is 0.460 and it lands in "unsure".

### What my calibration inputs showed

Scores are 0–1, higher means more likely AI. `compare.py` prints this table from the files in `calibration/`. Sources: `ai` and `ai_edited` are AI-written text I generated (`ai_edited` has light human-style edits); `human` and `formal_human` are short messages I wrote myself; `pet_article` and `doll_article` are excerpts from articles whose authors I don't know (the pet one reads AI-like, the doll one reads human-like), so they are not treated as ground truth.

| input | words | model | style | combined |
|---|---|---|---|---|
| ai | 94 | 0.834 | 0.460 | 0.460 |
| ai_edited | 87 | 0.604 | 0.461 | 0.532 |
| pet_article | 70 | 0.833 | 0.625 | 0.729 |
| human | 30 | 0.490 | 0.520 | 0.505 |
| formal_human | 24 | 0.583 | 0.250 | 0.250 |
| doll_article | 98 | 0.386 | 0.216 | 0.301 |

What I found:

- **The style signal separates the two longer articles well** (pet 0.625, doll 0.216). Sentence-length spread carries it. Vocabulary variety and punctuation contributed almost nothing on the AI samples.
- **The signals do not reliably separate AI from human on short or lightly edited text.** My short casual human text (0.505) scored above my clearly-AI sample (0.460), and lightly edited AI (0.532) is close to that human text.
- **My combining rule hurts on the clean AI sample.** The model gave `ai` 0.834 but style gave 0.460, a gap over 0.30, so the rule used the lower score and it landed in "unsure". A plain average would have given 0.647.
- **A short human text can look AI-like to the style signal.** `human` is two sentences of almost equal length, so the spread measure read it as machine-like. Short texts are unreliable.
- **The gap between clear AI and clear human is small.** The best pair (`pet_article` and `doll_article`) is about 0.43 apart on the combined score, well under the 0.7 my criterion 2 asks for.
- **All three labels look reachable** with the current placeholder thresholds (0.35 and 0.65): `pet_article` is above 0.65, `formal_human` and `doll_article` are below 0.35, and the rest are between.
- **Not changed:** I did not tune the style cut-offs, because six texts is too few to tune on without just fitting them.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.45 | We think this was probably written by a person. If you know it wasn't, please let us know. |
| unsure | 0.45 – 0.65 | We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know. |
| high-confidence AI | 0.65 – 1.00 | We think this was probably written by AI, because its sentence structure looks like AI writing. If that's wrong, you can appeal. |

**Why these thresholds:** The human line is 0.45 because some human writing, such as formal work and reports, can score highly, so a text has to score clearly low before it earns the "human" label. The AI line is 0.65 because that is a clear point above the middle where a text can fairly be labelled AI. The middle band (0.45 to 0.65) is for text that could be human, AI, or AI-assisted, and the system can't tell which. Wrongly labelling a real writer as AI costs them more than missing some AI text, so the AI line sits well above the middle.

**Why I worded the "unsure" one this way:**

The system can't tell human writing, AI writing and AI-assisted writing apart in this range, so the label says exactly that: "we can't tell". I first wrote "this text may be AI assisted," but that guesses a cause the system doesn't know and would read as an accusation to someone who wrote every word themselves. I kept the invitation to respond ("please let us know") so the writer has a next step.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Pets have been a part of human lives for centuries, offering companionship, love, and a sense of purpose. The benefits of owning a pet go beyond the joy of having a furry friend to cuddle with. From physical to psychological advantages, the perks of pet ownership are vast and varied. In this article, we\u2019ll delve deep into the myriad benefits of pets and how they can positively impact our lives.", "creator_id": "me"}'
```

```json
{
  "confidence": 0.7292,
  "content_id": "ebefaade-0ed2-4c55-8c9c-ae1dad87b320",
  "guess": "ai",
  "label": "We think this was probably written by AI, because its sentence structure looks like AI writing. If that's wrong, you can appeal.",
  "model_score": 0.8333,
  "style_score": 0.6251
}
```

**All three labels are reachable.** The same service, run on three other texts with `python submit_file.py <file>`, returns each label:

```json
{
  "confidence": 0.3009,
  "content_id": "7282eaf4-27c0-48a5-be6f-264eeb7508ca",
  "guess": "human",
  "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
  "model_score": 0.3856,
  "style_score": 0.2162
}
{
  "confidence": 0.5048,
  "content_id": "4ae25f5c-915f-4230-9330-3171a2e38c4e",
  "guess": "unsure",
  "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
  "model_score": 0.4896,
  "style_score": 0.52
}
```

**Bad input** (each is rejected with a clear message and logged)

```bash
$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"creator_id": "me"}'
$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"text": "   ", "creator_id": "me"}'
$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"text": "I love cookies", "creator_id": "me"}'
```

```json
{
  "error": "missing_field",
  "message": "Please provide text and creator_id."
}
{
  "error": "empty_text",
  "message": "Please provide text input."
}
{
  "error": "text_too_short",
  "message": "Please provide at least 20 words."
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "ebefaade-0ed2-4c55-8c9c-ae1dad87b320", "reasoning": "I wrote this myself."}'
```

```json
{
  "content_id": "ebefaade-0ed2-4c55-8c9c-ae1dad87b320",
  "message": "Thanks. Your appeal has been recorded and this item is now under review.",
  "status": "under_review"
}
```

Appealing the same item again, or using an id that doesn't exist, is refused and logged:

```json
{
  "error": "already_under_review",
  "message": "This item is already under review."
}
{
  "error": "unknown_content_id",
  "message": "We couldn't find a submission with that content_id."
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.3009,
      "content_id": "7282eaf4-27c0-48a5-be6f-264eeb7508ca",
      "creator_id": "me",
      "guess": "human",
      "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
      "model_score": 0.3856,
      "status": "decided",
      "style_score": 0.2162,
      "timestamp": "2026-11-02T05:19:40+00:00"
    },
    {
      "combined_score": 0.5048,
      "content_id": "4ae25f5c-915f-4230-9330-3171a2e38c4e",
      "creator_id": "me",
      "guess": "unsure",
      "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
      "model_score": 0.4896,
      "status": "decided",
      "style_score": 0.52,
      "timestamp": "2026-11-02T05:19:40+00:00"
    },
    {
      "content_id": "ebefaade-0ed2-4c55-8c9c-ae1dad87b320",
      "creator_id": "me",
      "event": "appeal",
      "reasoning": "I wrote this myself.",
      "status": "under_review",
      "timestamp": "2026-11-02T05:20:12+00:00"
    }
  ]
}
```

The appeal sits after the original decision for the same `content_id` (the log is append-only, so the decision is not overwritten). Both lines from `logs/audit.jsonl`:

```json
{"timestamp": "2026-11-02T05:19:39+00:00", "content_id": "ebefaade-0ed2-4c55-8c9c-ae1dad87b320", "creator_id": "me", "guess": "ai", "model_score": 0.8333, "style_score": 0.6251, "combined_score": 0.7292, "label": "We think this was probably written by AI, because its sentence structure looks like AI writing. If that's wrong, you can appeal.", "status": "decided"}
{"timestamp": "2026-11-02T05:20:12+00:00", "content_id": "ebefaade-0ed2-4c55-8c9c-ae1dad87b320", "creator_id": "me", "event": "appeal", "status": "under_review", "reasoning": "I wrote this myself."}
```

The three bad requests above are logged as rejections in `logs/audit.jsonl`:

```json
{"timestamp": "2026-11-01T17:31:13+00:00", "creator_id": "me", "event": "rejected", "status": "rejected", "reason": "missing_field"}
{"timestamp": "2026-11-01T17:31:13+00:00", "creator_id": "me", "event": "rejected", "status": "rejected", "reason": "empty_text"}
{"timestamp": "2026-11-01T17:31:13+00:00", "creator_id": "me", "event": "rejected", "status": "rejected", "reason": "text_too_short"}
```

---

## How I Used AI

**Moment 1: checking my labels from a writer's point of view**

- *What I asked for:* I wrote my first three labels ("AI", "Human", "AI assisted writing" and a few rough fragments) and asked Claude to read each one as the writer who receives it and tell me how it comes across.
- *What came back:* Claude said the labels read as accusations or were confusing: they weren't full sentences, never said "probably", gave the writer no next step, and "AI assisted writing" claimed something my system can't know, since my own threshold note said the middle range could be human, AI or AI-assisted.
- *What I changed:* I rewrote them as full sentences with "probably" and "can't tell", added the appeal to the AI label, and replaced "may be AI assisted" in the unsure label with "can't tell whether a person or AI wrote this, or whether AI helped". I asked Claude to tighten my wording and chose that version because it still said what I meant.

**Moment 2: checking whether my acceptance criteria could be verified**

- *What I asked for:* I wrote my five criteria and asked Claude whether someone who couldn't ask me could check each one.
- *What came back:* Claude said several were vague (what the "5" counted, what "about 0.7" meant, "4 of 5" for a yes/no label check), and that my appeal criterion allowed 2 failures in 5 even though the appeal is plain code, not a guess, and is the only recourse for a wrongly flagged writer.
- *What I changed:* I kept my numbers for criteria 1, 2, 3 and 5 and reworded them so each says what is counted. I revised criterion 4 to 5 of 5 valid appeals, plus an error for an unknown id. Claude drafted that revised wording at my request, and I kept it.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 6 per minute, 150 per day

**Why those numbers and not others:** A real writer revising a piece submits one version at a time and reads the result before editing again, so 6 per minute is more than they would send, and 150 per day is far more than a person submits. A script is different: at 6 per minute it would use up 150 submissions in about 25 minutes, so the daily cap stops it from mapping my thresholds by brute force. But 150 is still enough for a careful script to find a threshold by narrowing in on it with a few dozen well-chosen tries, and a script that changes its `creator_id` each time is not limited at all. So these numbers slow a simple flood and do not stop a determined attacker.

**What a caller counts as:** Each `creator_id` is counted separately (`app.py::rate_limit_key`); a request with no usable `creator_id` falls back to the caller's address. The weakness is that `creator_id` is chosen by the caller, so a script that changes it on every request is never limited, while one household sharing a single `creator_id` would be counted as one.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 200 429 429 429 429 429 429 429 429 429
```

15 submissions from one `creator_id`: the first 6 were accepted and the other 9 were rate limited. All 9 rejections appear in `logs/audit.jsonl` as `"reason": "rate_limited"`, for example:

```json
{"timestamp": "2026-11-04T23:24:45+00:00", "creator_id": "flood_tester", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "6 per 1 minute"}
```

---

## Attack Run — Before

56 attacks run with `python run_attacks.py --set attack_set --label before` (full output in `results/attack_run_2026-11-04_1923_before.md`). No crashes and no 5xx responses. **47 held, 9 broke.**

How I marked them: an evasion attack (AI text altered to look human) held if it was not labelled "human", so "unsure" counts as held. A false-positive attack (real human writing) broke only if it got the AI label. A rejected short text counts as held, because the writer was refused rather than accused. Malformed and flood rows held if the service answered with a clean error and did not crash.

| Family | Attacks | Held | Broke |
|---|---|---|---|
| evasion | 10 | 4 | 6 |
| false_positive | 8 | 7 | 1 |
| prompt_injection | 6 | 4 | 2 |
| malformed | 20 | 20 | 0 |
| flood_same_creator | 12 | 12 | 0 |

| ID | Family | Status | Guess | Score | Verdict | Note |
|---|---|---|---|---|---|---|
| EV01 | evasion | 200 | human | 0.164 | BROKE |  |
| EV02 | evasion | 200 | human | 0.000 | BROKE |  |
| EV03 | evasion | 200 | human | 0.257 | BROKE |  |
| EV04 | evasion | 200 | unsure | 0.556 | HELD | unsure, counted as held |
| EV05 | evasion | 200 | human | 0.180 | BROKE |  |
| EV06 | evasion | 200 | human | 0.001 | BROKE |  |
| EV07 | evasion | 200 | unsure | 0.521 | HELD | unsure, counted as held |
| EV08 | evasion | 400 | — | — | HELD | rejected (under 20 words) |
| EV09 | evasion | 200 | human | 0.233 | BROKE |  |
| EV10 | evasion | 200 | unsure | 0.606 | HELD | unsure, counted as held |
| FP01 | false_positive | 200 | human | 0.295 | HELD |  |
| FP02 | false_positive | 200 | unsure | 0.647 | HELD | unsure at 0.647, just under the 0.65 AI line |
| FP03 | false_positive | 200 | human | 0.408 | HELD |  |
| FP04 | false_positive | 200 | human | 0.368 | HELD |  |
| FP05 | false_positive | 200 | ai | 0.746 | BROKE | real person's documentation labelled AI |
| FP06 | false_positive | 200 | human | 0.294 | HELD |  |
| FP07 | false_positive | 200 | human | 0.300 | HELD |  |
| FP08 | false_positive | 400 | — | — | HELD | rejected (under 20 words), not accused |
| PI01 | prompt_injection | 200 | human | 0.037 | BROKE | AI-style text labelled human |
| PI02 | prompt_injection | 200 | human | 0.126 | BROKE | AI-style text labelled human |
| PI03 | prompt_injection | 200 | unsure | 0.479 | HELD |  |
| PI04 | prompt_injection | 200 | human | 0.420 | HELD |  |
| PI05 | prompt_injection | 200 | unsure | 0.534 | HELD | log not injected; entry holds only my fields |
| PI06 | prompt_injection | 200 | human | 0.429 | HELD |  |
| MF01 | malformed | 400 | — | — | HELD |  |
| MF02 | malformed | 400 | — | — | HELD |  |
| MF03 | malformed | 400 | — | — | HELD |  |
| MF04 | malformed | 400 | — | — | HELD |  |
| MF05 | malformed | 400 | — | — | HELD |  |
| MF06 | malformed | 400 | — | — | HELD |  |
| MF07 | malformed | 400 | — | — | HELD |  |
| MF08 | malformed | 413 | — | — | HELD |  |
| RQ01 | malformed | 400 | — | — | HELD |  |
| RQ02 | malformed | 400 | — | — | HELD |  |
| RQ03 | malformed | 400 | — | — | HELD |  |
| RQ04 | malformed | 400 | — | — | HELD |  |
| RQ05 | malformed | 400 | — | — | HELD |  |
| RQ06 | malformed | 400 | — | — | HELD |  |
| RQ07 | malformed | 400 | — | — | HELD |  |
| RQ08 | malformed | 400 | — | — | HELD |  |
| RQ09 | malformed | 400 | — | — | HELD |  |
| RQ10 | malformed | 400 | — | — | HELD |  |
| RQ11 | malformed | 429 | — | — | HELD | 429: bad request counted against the address bucket |
| RQ12 | malformed | 400 | — | — | HELD |  |
| FL01_01 | flood_same_creator | 400 | — | — | HELD | 400: text under 20 words |
| FL01_02 | flood_same_creator | 400 | — | — | HELD | 400: text under 20 words |
| FL01_03 | flood_same_creator | 400 | — | — | HELD | 400: text under 20 words |
| FL01_04 | flood_same_creator | 400 | — | — | HELD | 400: text under 20 words |
| FL01_05 | flood_same_creator | 400 | — | — | HELD | 400: text under 20 words |
| FL01_06 | flood_same_creator | 400 | — | — | HELD | 400: text under 20 words |
| FL01_07 | flood_same_creator | 429 | — | — | HELD | 429: limiter engaged after 6 |
| FL01_08 | flood_same_creator | 429 | — | — | HELD | 429: limiter engaged after 6 |
| FL01_09 | flood_same_creator | 429 | — | — | HELD | 429: limiter engaged after 6 |
| FL01_10 | flood_same_creator | 429 | — | — | HELD | 429: limiter engaged after 6 |
| FL01_11 | flood_same_creator | 429 | — | — | HELD | 429: limiter engaged after 6 |
| FL01_12 | flood_same_creator | 429 | — | — | HELD | 429: limiter engaged after 6 |

**Ten audit log entries from the run**

One false positive (`FP05`), a borderline one (`FP02`), five evasions or injections that got through or came close (`EV01`, `EV02`, `EV06`, `PI01`, `PI02`), the log-injection attempt that failed (`PI05`), and two rejections: a `429` from the flood and a short-text `400`.

```json
{"timestamp": "2026-11-05T00:23:48+00:00", "content_id": "ea11bbf9-2af1-4630-85c8-97e1b4e390c9", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.6923, "combined_score": 0.7464, "label": "We think this was probably written by AI, because its sentence structure looks like AI writing. If that's wrong, you can appeal.", "status": "decided"}
{"timestamp": "2026-11-05T00:23:47+00:00", "content_id": "de9644a5-ac29-493a-a8ba-2bc2821b8b72", "creator_id": "attacker_FP02", "guess": "unsure", "model_score": 0.7387, "style_score": 0.5561, "combined_score": 0.6474, "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.", "status": "decided"}
{"timestamp": "2026-11-05T00:23:47+00:00", "content_id": "5077806a-af38-4034-a592-a00156aaca54", "creator_id": "attacker_EV01", "guess": "human", "model_score": 0.1635, "style_score": 0.5, "combined_score": 0.1635, "label": "We think this was probably written by a person. If you know it wasn't, please let us know.", "status": "decided"}
{"timestamp": "2026-11-05T00:23:47+00:00", "content_id": "25df19a3-f21a-47f6-9908-5f61ec0d94d5", "creator_id": "attacker_EV02", "guess": "human", "model_score": 0.5943, "style_score": 0.0, "combined_score": 0.0, "label": "We think this was probably written by a person. If you know it wasn't, please let us know.", "status": "decided"}
{"timestamp": "2026-11-05T00:23:47+00:00", "content_id": "b7f9fbd9-d574-4f18-bc3d-c91a9a660f25", "creator_id": "attacker_EV06", "guess": "human", "model_score": 0.5727, "style_score": 0.0014, "combined_score": 0.0014, "label": "We think this was probably written by a person. If you know it wasn't, please let us know.", "status": "decided"}
{"timestamp": "2026-11-05T00:23:48+00:00", "content_id": "1552178a-1104-42e1-913a-cce739130258", "creator_id": "attacker_PI01", "guess": "human", "model_score": 0.4625, "style_score": 0.0373, "combined_score": 0.0373, "label": "We think this was probably written by a person. If you know it wasn't, please let us know.", "status": "decided"}
{"timestamp": "2026-11-05T00:23:48+00:00", "content_id": "b56223ad-9e3e-4cd0-a57a-fd5c99afa558", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.0482, "combined_score": 0.1263, "label": "We think this was probably written by a person. If you know it wasn't, please let us know.", "status": "decided"}
{"timestamp": "2026-11-05T00:23:48+00:00", "content_id": "51e3b9b4-4f3c-4de1-bdd2-eef49553daef", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.4286, "combined_score": 0.5343, "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.", "status": "decided"}
{"timestamp": "2026-11-05T00:23:48+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "6 per 1 minute"}
{"timestamp": "2026-11-05T00:23:48+00:00", "creator_id": "attacker_FP08", "event": "rejected", "status": "rejected", "reason": "text_too_short"}
```

**The single worst outcome** — the one I'd least want to explain to a writer whose work got caught by it:

`FP05`, a real person's technical documentation:

> To configure the service, edit the settings file in the installation directory. Set the host value to the address the service should bind to. Set the port value to an unused port above 1024. Save the file and restart the service. The service will log its startup configuration. If the port is already in use, the service will exit with an error. Check the log file for details before retrying.

My service labelled it as AI (combined score 0.7464, model signal 0.8005, style signal 0.6923):

> We think this was probably written by AI, because its sentence structure looks like AI writing. If that's wrong, you can appeal.

Both signals leaned AI, so there was no disagreement for my combining rule to catch.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
