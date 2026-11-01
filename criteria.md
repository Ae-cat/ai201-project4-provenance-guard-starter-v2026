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
