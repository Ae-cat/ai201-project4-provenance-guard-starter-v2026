# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-07 21:47
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `7cc9f5fc-3405-4be3-bf2c-ddf5744bcda6` | human | 0.332 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `df6e8ca2-7909-42b3-90a6-b0fc59bf21c8` | human | 0.297 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `82a5cecb-8ab2-4cd8-aad4-5c021e5a737c` | unsure | 0.461 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `663801eb-6ea7-4bb9-8fd8-e0622fe5d257` | unsure | 0.556 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `ecd3162f-072b-42c9-bce8-04e8f17b8980` | human | 0.180 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `b89eff9c-7dfb-49bc-b979-620912a6d82a` | human | 0.287 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `994f523b-2961-415a-b353-d0e7fd18f90e` | unsure | 0.521 | HELD |
| EV08 | evasion | signal one: text below the token window | 400 | `—` | — | — | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `ffbb38a2-148d-4705-9dc1-d07c1b4d4990` | unsure | 0.468 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `d5b976f0-5e93-4794-8d29-a4813274da82` | ai | 0.793 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `0c90efa7-78b7-4e7c-b796-0e71d5dceacf` | unsure | 0.456 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `7ad77e39-31fc-4d6a-8d3d-6388f8ac45f6` | unsure | 0.647 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `9d667d6f-6489-42ca-a007-19bb5086d186` | unsure | 0.607 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `4686ff60-6f67-4b28-8290-3abbd3710bc4` | unsure | 0.601 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `9acdc2ea-3445-4052-82b4-02ca4b6aff75` | ai | 0.746 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `1d2c04f7-fe0b-4457-b39d-55a30d4c44c9` | unsure | 0.588 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `6358992d-eaa6-4149-bef3-c1a12fd0d200` | unsure | 0.591 | HELD |
| FP08 | false_positive | very short genuine human submission | 400 | `—` | — | — | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `484a9160-83f8-47de-8470-e7cb30c83888` | human | 0.250 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c42130bc-bb1a-45ad-b455-2afeb13a5f7a` | human | 0.126 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `2303cb25-835c-47d2-8b21-1acf4342c16f` | unsure | 0.479 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `7cdb84ab-e1fc-4d70-8898-2b5127a0f08a` | human | 0.420 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `581015b6-5934-45fd-a5d0-aaa3d7afea79` | unsure | 0.534 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `9a773c3c-3f58-42ac-9391-fe7cb6e89444` | human | 0.429 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 400 | `—` | — | — | HELD |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — | HELD |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — | HELD |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — | HELD |
| MF07 | malformed | text is right-to-left script | 400 | `—` | — | — | HELD |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "7cc9f5fc-3405-4be3-bf2c-ddf5744bcda6",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.3317,
  "model_score": 0.1635,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "df6e8ca2-7909-42b3-90a6-b0fc59bf21c8",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.2972,
  "model_score": 0.5943,
  "style_score": 0.0,
  "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "82a5cecb-8ab2-4cd8-aad4-5c021e5a737c",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.4614,
  "model_score": 0.6662,
  "style_score": 0.2566,
  "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "663801eb-6ea7-4bb9-8fd8-e0622fe5d257",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5557,
  "model_score": 0.6114,
  "style_score": 0.5,
  "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "ecd3162f-072b-42c9-bce8-04e8f17b8980",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.1803,
  "model_score": 0.3212,
  "style_score": 0.0394,
  "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "b89eff9c-7dfb-49bc-b979-620912a6d82a",
  "creator_id": "attacker_EV06",
  "guess": "human",
  "confidence": 0.287,
  "model_score": 0.5727,
  "style_score": 0.0014,
  "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "994f523b-2961-415a-b353-d0e7fd18f90e",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5209,
  "model_score": 0.5862,
  "style_score": 0.4555,
  "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_EV08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "ffbb38a2-148d-4705-9dc1-d07c1b4d4990",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.4684,
  "model_score": 0.7042,
  "style_score": 0.2325,
  "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "d5b976f0-5e93-4794-8d29-a4813274da82",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.7926,
  "model_score": 0.9792,
  "style_score": 0.6061,
  "label": "We think this was probably written by AI, because its sentence structure looks like AI writing. If that's wrong, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "0c90efa7-78b7-4e7c-b796-0e71d5dceacf",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.4562,
  "model_score": 0.6175,
  "style_score": 0.2949,
  "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "7ad77e39-31fc-4d6a-8d3d-6388f8ac45f6",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6474,
  "model_score": 0.7387,
  "style_score": 0.5561,
  "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "9d667d6f-6489-42ca-a007-19bb5086d186",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6068,
  "model_score": 0.8051,
  "style_score": 0.4085,
  "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "4686ff60-6f67-4b28-8290-3abbd3710bc4",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6005,
  "model_score": 0.8329,
  "style_score": 0.3681,
  "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "9acdc2ea-3445-4052-82b4-02ca4b6aff75",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7464,
  "model_score": 0.8005,
  "style_score": 0.6923,
  "label": "We think this was probably written by AI, because its sentence structure looks like AI writing. If that's wrong, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "1d2c04f7-fe0b-4457-b39d-55a30d4c44c9",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5875,
  "model_score": 0.8814,
  "style_score": 0.2936,
  "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "6358992d-eaa6-4149-bef3-c1a12fd0d200",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5908,
  "model_score": 0.8816,
  "style_score": 0.3,
  "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_FP08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "484a9160-83f8-47de-8470-e7cb30c83888",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.2499,
  "model_score": 0.4625,
  "style_score": 0.0373,
  "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "c42130bc-bb1a-45ad-b455-2afeb13a5f7a",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1263,
  "model_score": 0.2044,
  "style_score": 0.0482,
  "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "2303cb25-835c-47d2-8b21-1acf4342c16f",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4787,
  "model_score": 0.5943,
  "style_score": 0.363,
  "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "7cdb84ab-e1fc-4d70-8898-2b5127a0f08a",
  "creator_id": "attacker_PI04",
  "guess": "human",
  "confidence": 0.4205,
  "model_score": 0.4998,
  "style_score": 0.3412,
  "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "581015b6-5934-45fd-a5d0-aaa3d7afea79",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5343,
  "model_score": 0.6401,
  "style_score": 0.4286,
  "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "9a773c3c-3f58-42ac-9391-fe7cb6e89444",
  "creator_id": "attacker_PI06",
  "guess": "human",
  "confidence": 0.4289,
  "model_score": 0.5583,
  "style_score": 0.2996,
  "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
