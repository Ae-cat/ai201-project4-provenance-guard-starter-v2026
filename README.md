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
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



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
  -d '{"text": "I went to the shop on Tuesday and the guy at the counter was arguing with his phone, so I just stood there for ten minutes. Honestly? Best part of my week.", "creator_id": "me"}'
```

```json
{
  "confidence": 0.6245,
  "content_id": "32a7225e-cd50-41b1-8261-a60ab1e3550e",
  "guess": "unsure",
  "label": "PLACEHOLDER label",
  "model_score": 0.6245,
  "style_score": null
}
```

<!-- Milestone 3 output: signal two (style_score), the combined score and the
     real label come in Milestones 4 and 5. Re-run and re-paste this block
     once they exist. -->

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
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 1,
  "entries": [
    {
      "combined_score": null,
      "content_id": "32a7225e-cd50-41b1-8261-a60ab1e3550e",
      "creator_id": "me",
      "guess": "unsure",
      "label": "PLACEHOLDER label",
      "model_score": 0.6245,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-11-01T17:30:53+00:00"
    }
  ]
}
```

The three bad requests above are logged as rejections in `logs/audit.jsonl`:

```json
{"timestamp": "2026-11-01T17:31:13+00:00", "creator_id": "me", "event": "rejected", "status": "rejected", "reason": "missing_field"}
{"timestamp": "2026-11-01T17:31:13+00:00", "creator_id": "me", "event": "rejected", "status": "rejected", "reason": "empty_text"}
{"timestamp": "2026-11-01T17:31:13+00:00", "creator_id": "me", "event": "rejected", "status": "rejected", "reason": "text_too_short"}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



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
