# Capstone run — before

Run at 2026-11-15 23:58 against http://127.0.0.1:5000, three trials, nothing changed in between.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Crash response | at least 9 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 2. Crash logging | 10 of 10 | 0/10 | 0/10 | 0/10 | MISSED |
| 3. Duration tracking | at least 95% | 0% (0/0) | 0% (0/0) | 0% (0/0) | MISSED |
| 4. Original endpoints preserved | 23 of 23 | 23/23 | 23/23 | 23/23 | MET |
| 5. Crash handling, log unwritable | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

## Real output from trial 1

**Criterion 1** (`app.py::unexpected_error`), first crash response:
```
status 500
{
  "error": "internal_error",
  "message": "Something went wrong on our side. Nothing was decided. Please try again."
}
```

**Criterion 2** (`audit.py::log_error`), the log entry for that crash:
```json
none
```

**Criterion 3** (`app.py::_duration_ms`, passed into `audit.py`):
```
0 of 0 entries had a numeric duration_ms
entries without it: none
```

**Criterion 4**, one normal submission, then the three error-code checks:
```
status 200
{
  "confidence": 0.5643,
  "content_id": "080310ed-e3ee-4d99-8907-408963c76f6b",
  "guess": "unsure",
  "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
  "model_score": 0.8467,
  "style_score": 0.2818
}

400 check: status 400 {
  "error": "empty_text",
  "message": "Please provide text input."
}
413 check: status 413 {
  "error": "text_too_long",
  "message": "Text is over 10000 characters."
}
429 check: seven requests from one creator gave [200, 200, 200, 200, 200, 200, 429]
```

**Criterion 5** (`app.py::unexpected_error` with the log unwritable), first response:
```
status 500
{
  "error": "internal_error",
  "message": "Something went wrong on our side. Nothing was decided. Please try again."
}
```
