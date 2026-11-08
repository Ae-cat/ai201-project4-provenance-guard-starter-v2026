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

**The rule:** The combined score is a weighted average of the model score and the style score (50% each). I originally had a second part: if the two signals differed by more than 0.30, the rule used the *lower* (more human) of the two instead of averaging, so that an AI label would need both signals to agree. In Unit 8 I removed that part (see "The Improvement" below), because the attack run and my criteria showed it let one low signal overrule the other, and it caused both missed criteria and six of the nine broken attacks. The calibration findings further down describe the original rule.

**The numbers:**

| Setting | Value | Where |
|---|---|---|
| Model signal weight | 0.5 | `config.py::WEIGHT_MODEL_SIGNAL` |
| Style signal weight | 0.5 | `config.py::WEIGHT_STYLE_SIGNAL` |
| Style measure weights (spread / vocabulary / punctuation) | 0.5 / 0.3 / 0.2 | `config.py::STYLE_WEIGHT_*` |

The style measures are scaled onto 0–1 with first-guess cut-offs set at the top of `stylometry.py`. They are not calibrated yet.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

My `formal_human` test text (a polite message I wrote myself) scored 0.583 on the model signal, which leans AI, but 0.250 on the style signal, which leans human. With the current rule they average to 0.416, which is below my 0.45 line, so it is labelled "human". My original rule would have used the lower score, 0.250, and also labelled it "human". The case that showed the difference was my clearly-AI `ai` sample (0.834 model, 0.460 style): the original rule gave 0.460, and the average gives 0.647, which is just under the 0.65 AI line, so it is "unsure".

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

**Moment 3: finding which stage caused the misses**

- *What I asked for:* after the first attack run and the five-criteria run, I asked Claude to help me work out why criteria 2 and 3 were missed and which stage each broken attack pointed at.
- *What came back:* Claude read `scoring.py` and my recorded scores and said the lower-of-two combining rule let one low signal overrule the other, which explained both missed criteria and six of the nine broken attacks. It said `FP05` was a different problem: both signals lean AI on plain writing, so no combining rule could fix it.
- *What I changed:* I wrote the diagnoses in my own words from that and kept `FP05` as a separate blind spot rather than folding it into the rule.

**Moment 4: choosing the one fix**

- *What I asked for:* I asked which single change to make. Claude tested three options on the scores I had already recorded: a plain average, weighting toward the model signal, and lowering the AI line.
- *What came back:* the plain average cut AI-style attacks labelled "human" from 8 to 6 and left false positives unchanged, while the other two options flagged real writers as AI (1 of 9 rising to 6 of 9, or 4 of 9). Claude warned that the average would also push some texts into "unsure".
- *What I changed:* I chose the plain average, and my real re-run showed the trade Claude described: 9 broken attacks became 7, and five real-writer texts moved from "human" to "unsure".

**Where AI was wrong or I had to catch it:** my first "after" run happened with the service not running, so every request errored and the appeal check showed 0/5. I deleted those two result files, restarted the server, checked `/health`, and re-ran.

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
| 1. My own writing flagged as AI | at most 2 of 5 | 0/5 | 0/5 | 0/5 | MET |
| 2. Score spread, AI vs. human | about 0.7 apart in at least 4 of 5 pairs | 0/5 | 0/5 | 0/5 | MISSED |
| 3. Label coverage | all 3 labels appear, and at least 4 of 5 get the expected label | 3/5 (3 labels appear) | 3/5 (3 labels appear) | 3/5 (3 labels appear) | MISSED |
| 4. The appeal path | 5 of 5 valid appeals correct, and 5 of 5 unknown ids refused | 5/5 and 5/5 | 5/5 and 5/5 | 5/5 and 5/5 | MET |
| 5. Bad input | 5 of 5 bad inputs get a clean error, no crash | 5/5 | 5/5 | 5/5 | MET |

All three trials came out identical for every criterion, which is expected because neither signal is random. Criterion 4 can't be run by `run_eval.py` (an appeal needs a `content_id` from an earlier submission), so I wrote `run_appeal_eval.py` for it: it submits five texts, appeals each, checks the log, and appeals five unknown ids, three times. The scenarios and my expected labels for criterion 3 were written in `scenarios.py` and committed before the run.

**Criterion 2, the five pairs** (combined scores from the first trial; the gap is AI text minus human text, and the target was about 0.7):

| Pair (AI text vs. my own text) | AI text | My text | Gap |
|---|---|---|---|
| time management vs. dinner message | 0.6598 | 0.25 | +0.410 |
| exercise vs. firework message | 0.5256 | 0.5048 | +0.021 |
| climate vs. Timmy story | 0.3753 | 0.6148 | -0.239 |
| reading vs. dodgeball story | 0.668 | 0.2785 | +0.390 |
| technology vs. dogs post | 0.6194 | 0.5822 | +0.037 |

The biggest gap is 0.41, and in the climate/Timmy pair my own writing scored *higher* than the AI text.

**Criterion 3, expected vs. actual** (expected labels written before the run):

| Text | Expected | Got |
|---|---|---|
| AI: time management | ai | ai |
| AI: climate change | ai | human |
| mine: dodgeball story | human | human |
| mine: dogs post | human | unsure |
| lightly edited AI: exercise | unsure | unsure |

**Real output from one trial** (trial 1, pasted as text).

Criterion 1, my own writing. Produced by `run_eval.py::main`, calling `app.py::submit`:

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.25,
    "model_score": 0.5826,
    "style_score": 0.25,
    "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
    "sent": "I would like to attend my family's dinner this evening so I will not b"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5048,
    "model_score": 0.4896,
    "style_score": 0.52,
    "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
    "sent": "Later today there is going to be a firework show, with vendors and suc"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6148,
    "model_score": 0.6202,
    "style_score": 0.6094,
    "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
    "sent": "Timmy went out to the grocery at 3pm, he has yet to arrive back home. "
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2785,
    "model_score": 0.3906,
    "style_score": 0.1664,
    "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
    "sent": "The bell rang! It is P.E time and all the kids went running. Today was"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5822,
    "model_score": 0.5693,
    "style_score": 0.5951,
    "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
    "sent": "Scrolling through instagram, I have recently learned that dogs such as"
  }
]
```

Criterion 2, score spread (the same texts, AI then human in each pair). Same file and function:

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6598,
    "model_score": 0.7804,
    "style_score": 0.5392,
    "label": "We think this was probably written by AI, because its sentence structure looks like AI writing. If that's wrong, you can appeal.",
    "sent": "Effective time management is a crucial skill that can greatly enhance "
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.25,
    "model_score": 0.5826,
    "style_score": 0.25,
    "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
    "sent": "I would like to attend my family's dinner this evening so I will not b"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5256,
    "model_score": 0.8818,
    "style_score": 0.5256,
    "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
    "sent": "Regular physical exercise offers numerous benefits for overall health "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5048,
    "model_score": 0.4896,
    "style_score": 0.52,
    "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
    "sent": "Later today there is going to be a firework show, with vendors and suc"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3753,
    "model_score": 0.9163,
    "style_score": 0.3753,
    "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
    "sent": "Climate change is one of the most pressing challenges facing humanity "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6148,
    "model_score": 0.6202,
    "style_score": 0.6094,
    "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
    "sent": "Timmy went out to the grocery at 3pm, he has yet to arrive back home. "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.668,
    "model_score": 0.7907,
    "style_score": 0.5453,
    "label": "We think this was probably written by AI, because its sentence structure looks like AI writing. If that's wrong, you can appeal.",
    "sent": "Reading is a fundamental activity that enriches the mind and expands o"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2785,
    "model_score": 0.3906,
    "style_score": 0.1664,
    "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
    "sent": "The bell rang! It is P.E time and all the kids went running. Today was"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6194,
    "model_score": 0.7193,
    "style_score": 0.5194,
    "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
    "sent": "Technology has transformed the way people communicate, work, and learn"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5822,
    "model_score": 0.5693,
    "style_score": 0.5951,
    "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
    "sent": "Scrolling through instagram, I have recently learned that dogs such as"
  }
]
```

Criterion 3, label coverage. Same file and function:

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6598,
    "model_score": 0.7804,
    "style_score": 0.5392,
    "label": "We think this was probably written by AI, because its sentence structure looks like AI writing. If that's wrong, you can appeal.",
    "sent": "Effective time management is a crucial skill that can greatly enhance "
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3753,
    "model_score": 0.9163,
    "style_score": 0.3753,
    "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
    "sent": "Climate change is one of the most pressing challenges facing humanity "
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2785,
    "model_score": 0.3906,
    "style_score": 0.1664,
    "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
    "sent": "The bell rang! It is P.E time and all the kids went running. Today was"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5822,
    "model_score": 0.5693,
    "style_score": 0.5951,
    "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
    "sent": "Scrolling through instagram, I have recently learned that dogs such as"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5164,
    "model_score": 0.8502,
    "style_score": 0.5164,
    "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
    "sent": "Regular exercise does a lot for your health, honestly more than most p"
  }
]
```

Criterion 4, the appeal path (one valid appeal with its log entries, and one unknown id). Produced by `run_appeal_eval.py::main`, calling `app.py::appeal`:

```json
[
  {
    "case": "valid appeal 1",
    "checks": {
      "response is 200 with under_review": true,
      "appeal entry in log with under_review": true,
      "original decision unchanged": true
    },
    "submit_status": 200,
    "content_id": "9ef57146-8e4e-4be7-a5db-f2f7584515c3",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "9ef57146-8e4e-4be7-a5db-f2f7584515c3",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.3752,
        "content_id": "9ef57146-8e4e-4be7-a5db-f2f7584515c3",
        "creator_id": "eval_appeal_1_1",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.4623,
        "status": "decided",
        "style_score": 0.2882,
        "timestamp": "2026-11-05T01:36:50+00:00"
      },
      {
        "content_id": "9ef57146-8e4e-4be7-a5db-f2f7584515c3",
        "creator_id": "eval_appeal_1_1",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-05T01:36:50+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "unknown id 1",
    "content_id": "dbeef0ad-6c10-4e7a-a74f-93c4deab2893",
    "appeal_status": 404,
    "appeal_response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id."
    },
    "checks": {
      "returns an error, not a success": true
    },
    "passed": true
  }
]
```

Criterion 5, bad input. Produced by `run_eval.py::main`, calling `app.py::submit` (statuses; the error messages come from `app.py::_reject`, shown in the Sample Run above):

```json
[
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 413,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "word word word word word word word word word word word word word word "
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": \"I went for a long walk by the river this morning and it was lovely and quiet.\"}"
  }
]
```

**How I decided each verdict**

1. **MET.** None of my five pieces got the AI label in any of the three trials (0 of 5, against a limit of 2). That target was generous, though: I allowed 2 and got 0, and `FP05` in the attack set shows a real writer's text can still get the AI label. Criterion 1 is the one I'd tighten.
2. **MISSED.** No pair came anywhere near 0.7 apart. The best was 0.41, and in one pair my own writing scored higher than the AI text.
3. **MISSED.** All three labels appeared, but only 3 of 5 texts got the label I expected, and I needed 4.
4. **MET.** 5 of 5 valid appeals passed every check and 5 of 5 unknown ids were refused, in all three trials.
5. **MET.** All 5 bad inputs returned a 4xx error and none crashed, in all three trials.

**Diagnoses**

**The combining rule (criteria 2 and 3, and six broken attacks).** Both signals score from 0 to 1, and a lower number means more likely human. My rule in `scoring.py::combine_signals` averages the two, but when they differ by more than 0.30 it uses the *lower* one. So one signal saying "human" overrules the other, even when the other is very sure. The clearest case is the climate AI text: signal one scored it 0.916 (clearly AI) and signal two scored it 0.375, so the combined score was 0.375 and it was labelled human. The same thing happened to `EV01`, `EV02`, `EV03`, `EV06`, `EV09` and `PI01`, all AI-style text that came out as "human", and it pulled `EV10` (signal one 0.979) down to "unsure". It also explains criterion 2: signal two rarely scores clear AI text above about 0.6, so with the lower-score rule even strongly AI text lands near the middle and a 0.7 gap can't happen. The stage is the combining rule. The mechanism is that a gap over 0.30 hands the decision to whichever signal is lower.

**Signal two (`EV02`, `EV06`, `EV03`, `PI01`).** Breaking AI text into uneven sentences, mixing one very long and one very short sentence, or adding a few short sentences drove the style score to about 0 (`EV02` 0.000, `EV06` 0.001, `PI01` 0.037). Signal two measures only the shape of the text (`stylometry.py::sentence_length_spread` and `style_signal`: how much sentence lengths vary, how varied the vocabulary is, and how much punctuation there is). Changing the shape changes the score without changing who wrote it. The stage is signal two. The mechanism is that sentence-length variation counts as human. The length limits on input (at least 20 words, at most 10,000 characters, in `app.py::submit`) are a different stage and worked as designed: they refused `EV08`, `FP08` and the 60,000-character `MF08`. These attacks were about 90 words, so they never touched that check.

**`FP05`, a real person's technical documentation.** Both signals leaned AI (signal one 0.800, signal two 0.692), so the average of 0.746 crossed my 0.65 line and nothing in the combining rule could correct it. Formal instructions follow a fixed format: short imperative sentences of similar length ("Set the host value... Set the port value... Save the file...") with plain, common words. Signal two doesn't check grammar; it saw sentences of even length and scored them as machine-like. Signal one saw predictable common words in short sentences, which gpt2 finds easy to predict. The stage is both signals (`detector.py::model_signal` and `stylometry.py::style_signal`), and the mechanism is a shared blind spot: plain, formatted writing looks like AI to both. My own plain writing shows the same lean, with the Timmy story at 0.61 and the dogs post at 0.58 on the combined score.

**The rest.** `EV05` (heavy human editing) and `PI02` (an injected "system message") scored low on both signals, so the combining rule averaged them and this isn't the rule's fault. The odd injected sentence raised signal one's perplexity (0.204 for `PI02`), and my signals don't read the text, so they never obeyed its instructions; they only reacted to how it changed the text.

**The pattern.** One stage, the combining rule, accounts for both missed criteria and six of the nine broken attacks. A second, separate problem is that plain or formal human writing looks AI-like to both signals. The first is a design choice I can change; the second is the structural blind spot the project is about.

---

## The Improvement

**What I changed:** I replaced the lower-of-two combining rule in `scoring.py::combine_signals` with a plain 0.5/0.5 weighted average of the model signal and the style signal. Before, when the two signals disagreed by more than 0.30, the combined score took the lower one. Nothing else changed: same thresholds (human at or below 0.45, AI at or above 0.65), same signals, same labels.

**Which diagnosis pointed at it:** The diagnosis of criteria 2 and 3 and of six of the nine broken attacks. In each case one low signal overruled the other. `EV02`, for example, scored 0.0 combined before and 0.2972 after the change, and the criterion 2 and 3 misses had the same cause. I tested three options on the scores I had already recorded (a plain average, weighting toward the model signal, and lowering the AI line). Only the plain average avoided flagging more real writers as AI, so I chose it.

### Attack Run — After

Same 56 attacks, same attack set, run with `python run_attacks.py --set attack_set --label after`. Full results are in `results/attack_run_2026-11-07_2147_after.md`; the two criteria runs are `results/run_2026-11-07_2147_after.md` and `results/appeal_run_2026-11-07_2147_after.md`.

| Family | Before (held / broke) | After (held / broke) |
|---|---|---|
| Evasion | 4 / 6 | 6 / 4 |
| False positive | 7 / 1 | 7 / 1 |
| Prompt injection | 4 / 2 | 4 / 2 |
| Malformed | 20 / 0 | 20 / 0 |
| Flood, same creator | 12 / 0 | 12 / 0 |
| **Total** | **47 / 9** | **49 / 7** |

Labels that changed (eight of 56):

| Input | Before | After | Verdict |
|---|---|---|---|
| `EV03` | human | unsure | BROKE → HELD |
| `EV09` | human | unsure | BROKE → HELD |
| `EV10` | unsure | ai | HELD (now caught outright) |
| `FP01`, `FP03`, `FP04`, `FP06`, `FP07` | human | unsure | HELD both times |

Criteria, before and after (identical across all three trials both times):

| Criterion | Before | After | Verdict after |
|---|---|---|---|
| 1. My own writing flagged as AI | 0/5 | 0/5 | MET |
| 2. Score spread (about 0.7 in 4 of 5 pairs) | 0/5 pairs; best gap 0.41 | 0/5 pairs; best gap 0.39 | MISSED |
| 3. Label coverage (4 of 5 expected labels, all 3 appear) | 3/5 | 2/5 | MISSED |
| 4. The appeal path | 5/5 and 5/5 | 5/5 and 5/5 | MET |
| 5. Bad input | 5/5 | 5/5 | MET |

**Did it help, and how do I know:** A little, and with a cost. Broken attacks went from 9 to 7: `EV03` and `EV09` (AI text with evasion edits) moved from "human" to "unsure", so they no longer pass as human-written, and `EV10` is now labelled AI. No real writer was newly labelled AI: the false-positive scenarios in criterion 1 stayed at 0/5 and `FP05` is still the only false positive in the attack set.

The cost is that the average pulls extreme scores toward the middle. Five of my real-writer texts (`FP01`, `FP03`, `FP04`, `FP06`, `FP07`) moved from "human" to "unsure". They are not accused, but they are no longer cleared either. Criterion 3 also got worse, from 3/5 to 2/5, because texts I expected to be labelled "human" or "ai" now land in "unsure". Criterion 2 is still missed: averaging cannot create separation the signals don't have, and the best gap is still 0.39 against a target of 0.7. So the fix removed the damage caused by the old rule, and it did not make the signals better at telling AI from human writing.

---

## What's Still Broken

Seven attacks still get through (`EV01`, `EV02`, `EV05`, `EV06`, `PI01`, `PI02`, `FP05`) and two criteria are still missed (2 and 3).

**`EV01`, `EV02`, `EV06`, `PI01` (AI text reshaped to look human).** The style signal still scores these near 0 because uneven sentence lengths count as human. After the average they still land below 0.45. *What I'd do:* make signal two measure something an editor can't change by reshaping sentences, such as word choice or repeated phrasing across the whole text, and stop letting sentence-length spread carry half the style score. *Why I stopped:* that means designing and calibrating a new signal, which is a bigger change than the one fix this unit allowed, and I had no way to check a new signal beyond the same small set of texts I already used.

**`EV05` and `PI02` (heavily edited AI text, and a fake "system message").** Both signals score these low, so no combining rule can recover them; averaging two wrong answers gives a wrong answer. *What I'd do:* nothing in the scoring. Heavily human-edited text is partly human, and I'd rather label it "unsure" through the appeal and a human reviewer than add a rule that guesses. *Why I stopped:* I can't separate "AI text a person rewrote" from "a person's own writing" with these signals, and chasing it would flag more real writers.

**`FP05` (a real person's technical documentation labelled AI).** Both signals lean AI on plain, formatted writing, and my change did not touch this. *What I'd do:* the safest fix is to stop giving the AI label to text that only one kind of evidence supports, for example requiring the AI label to need a high score from signal one and signal two separately. *Why I stopped:* in my own recorded scores that rule would also have lost most of the AI text the system does catch, and I didn't want to trade away detection without testing it. Until then, the appeal is the only recourse, and `FP05` is the reason I kept it as a 5-of-5 criterion.

**Criterion 2 (score spread, still 0 of 5 pairs).** The two signals don't separate AI from human text by 0.7. Averaging can't create separation that isn't in the signals; the best gap is 0.39. *What I'd do:* either find a better second signal or lower the target to something the signals can deliver and say so. *Why I stopped:* lowering the target after seeing the result would be moving the goalposts, so I've left it MISSED.

**Criterion 3 (label coverage, 2 of 5).** My fix moved texts into "unsure", so fewer get the sharp label I expected. This is the direct cost of the plain average, and it is the price I chose to pay for fewer evasion attacks passing. *What I'd do:* re-check whether my expected labels for the middle texts were reasonable. *Why I stopped:* changing the expected labels now would also be moving the goalposts.

**The trade I'd make if this ran for real:**

I'd lean toward catching more AI text, even though it means more real writers get wrongly flagged. The people who pay are those writers, especially people with plain or formal styles like the author of `FP05`, who would have to appeal and prove they wrote their own work, so the appeal path and the "unsure" label would have to do the protecting.

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
