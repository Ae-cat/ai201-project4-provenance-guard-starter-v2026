#!/usr/bin/env python3
"""
Capstone: what does one run cost?

For this service the cost is seconds of compute. Nothing is paid for: the model
runs on this machine. This sends 10 real submissions, one warm-up first, and
reports how long the service itself spent on each (the duration_ms it logged)
and how long the caller waited.

Start the service in one terminal:   python app.py
Then, in another:                    python measure_cost.py
"""

import statistics
import sys
import time

import requests

import scenarios

BASE = "http://127.0.0.1:5000"
TEXTS = list(scenarios.OWN) + list(scenarios.AI)          # 10 different texts


def submit(text, who):
    start = time.perf_counter()
    r = requests.post(BASE + "/submit", json={"text": text, "creator_id": who}, timeout=120)
    return r, (time.perf_counter() - start) * 1000


def server_ms(content_id):
    entries = requests.get(BASE + "/log?limit=200", timeout=10).json()["entries"]
    for e in reversed(entries):
        if e.get("content_id") == content_id and e.get("event") is None:
            return e.get("duration_ms")
    return None


try:
    requests.get(BASE + "/health", timeout=5)
except requests.RequestException:
    sys.exit("The service isn't running. Start it with: python app.py")

print("Warm-up (the first request loads the model, so it is not counted)...")
r, warm = submit(TEXTS[0], "cost_warmup")
print(f"  warm-up: {warm:.0f} ms (status {r.status_code})")

rows = []
for i, text in enumerate(TEXTS, 1):
    r, client = submit(text, f"cost_run_{i}")
    if r.status_code != 200:
        print(f"  run {i}: status {r.status_code}, skipped")
        continue
    srv = server_ms(r.json()["content_id"])
    rows.append((client, srv))
    print(f"  run {i:2d}: server {srv} ms, caller waited {client:.0f} ms")

if rows:
    srv_all = [s for _, s in rows if s is not None]
    cli_all = [c for c, _ in rows]
    print()
    print(f"{len(rows)} runs")
    print(f"  server time per run:  mean {statistics.mean(srv_all)/1000:.2f} s   "
          f"min {min(srv_all)/1000:.2f} s   max {max(srv_all)/1000:.2f} s")
    print(f"  caller wait per run:  mean {statistics.mean(cli_all)/1000:.2f} s")
    print(f"  one-time model load (first request): {warm/1000:.2f} s")
