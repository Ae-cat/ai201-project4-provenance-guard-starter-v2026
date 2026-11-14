#!/usr/bin/env python3
"""
Capstone check: does the catch-all error handler work, and is the old service intact?

Start the service with fault injection on, in one terminal:

    AI201_FAULT_INJECTION=1 python app.py

Then, in another:

    python check_error_handler.py
"""

import sys
import requests

BASE = "http://127.0.0.1:5000"
GOOD = ("I went for a long walk by the river this morning and it was lovely and quiet, "
        "so I stopped at the little cafe near the bridge and had a coffee before heading home.")
creator = "capstone_check"
failures = []


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    if not ok:
        failures.append(name)


def post(path, body):
    return requests.post(BASE + path, json=body, timeout=60)


print("Regression: the original service still works")
r = post("/ping", {"message": "hello"})
check("/ping answers", r.status_code == 200, r.status_code)
r = post("/submit", {"text": GOOD, "creator_id": creator})
check("a normal /submit returns 200 with a guess and both scores",
      r.status_code == 200 and {"guess", "model_score", "style_score"} <= set(r.json()), r.status_code)
r = post("/submit", {"text": "", "creator_id": creator})
check("empty text still gets a clean 400", r.status_code == 400, r.status_code)

print("The new handler: a deliberate crash")
r = post("/submit", {"text": "[[inject-fault]] " + GOOD, "creator_id": creator})
if r.status_code == 200:
    print("  The crash didn't happen. Restart the service with AI201_FAULT_INJECTION=1.")
    sys.exit(1)
check("the crash returns 500", r.status_code == 500, r.status_code)
body = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
check("the body is JSON with error 'internal_error'", body.get("error") == "internal_error",
      r.headers.get("content-type"))

entries = requests.get(BASE + "/log?limit=5", timeout=10).json()["entries"]
errors = [e for e in entries if e.get("event") == "error" and e.get("creator_id") == creator]
check("the crash left an 'error' entry in the log", bool(errors))
check("that entry has error_type and duration_ms",
      bool(errors) and "error_type" in errors[-1] and "duration_ms" in errors[-1])
if errors:
    print("  logged:", errors[-1])

r = post("/ping", {"message": "hello"})
check("the service still answers after the crash", r.status_code == 200, r.status_code)

print()
print("ALL PASSED" if not failures else f"{len(failures)} FAILED: {failures}")
sys.exit(1 if failures else 0)
