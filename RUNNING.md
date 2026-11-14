# Running Provenance Guard

**Path B: local, with logs.** The service runs on your own machine, started by one command. It isn't hosted, because signal one loads a gpt2 model locally (about 550 MB), and the free host's 512 MB of memory can't hold it.

## What it needs

- **Python 3.11, 3.12 or 3.13.** Not 3.14. This was developed and run on Python 3.13.1 on macOS.
- **The pinned packages** in `requirements.txt` (flask, flask-limiter, requests, transformers, torch, gunicorn, certifi), installed in a virtual environment.
  Versions this was run with: Flask 3.1.3, Flask-Limiter 3.12, requests 2.34.2, transformers 4.57.6, gunicorn 23.0.0, certifi 2026.10.23, and torch 2.14.1 (development machine) or 2.15.0 (clean checkout). Both torch versions worked, because `requirements.txt` allows a range.
- **The gpt2 model files, about 550 MB.** They download once, the first time the model is used, and are cached on your machine after that. This needs an internet connection the first time only. There is no API key and no account.
- **Disk and memory:** several GB free for torch and the model, and enough RAM to hold gpt2.

## Set up (once)

```bash
git clone <this repository's URL> provenance-guard
cd provenance-guard
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python detector.py                 # downloads the model (about 550 MB) and scores a sample
python test.py                     # checks the environment; it should pass
```

## Start it (the one command)

```bash
python app.py
```

It serves on `http://127.0.0.1:5000`. The first request is slow while the model loads; after that each one takes a second or so.

Check it is alive from a second terminal:

```bash
curl http://127.0.0.1:5000/health
curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I went for a long walk by the river this morning and it was lovely and quiet, so I stopped at the little cafe near the bridge and had a coffee before heading home.", "creator_id": "me"}'
```

`/submit` needs at least 20 words. It returns `content_id`, `guess`, `confidence`, `label`, `model_score` and `style_score`.

## The log

Every request writes one JSON line to `logs/audit.jsonl`: decisions, rejected inputs, appeals, and unexpected errors. Read it with:

```bash
curl "http://127.0.0.1:5000/log?limit=10"
```

Decision, rejection and error entries carry `timestamp`, `creator_id`, `duration_ms` and `input_excerpt` (the first 200 characters of the text) and `input_chars`; decisions also carry both signal scores, the combined score, the guess and the label.

## Checks and measurements

| Command | What it does |
|---|---|
| `AI201_FAULT_INJECTION=1 python app.py` then `python check_error_handler.py` | Triggers a deliberate crash and checks the catch-all error handler and the log. **Only use the fault switch for testing.** |
| `python measure_cost.py` | Sends 10 submissions and reports seconds of compute per run. |
| `python run_attacks.py --set attack_set --label X` | The Unit 8 attack set. |
| `python run_eval.py --label X` | The Unit 8 criteria runs. |
| `python run_attacks.py --flood 15` | Pushes past the rate limit (6 per minute) and prints the 429s. |

## Troubleshooting

- *"Address already in use" / "Port 5000 is in use":* another copy of the service is still running (check your other terminals and stop it with Ctrl+C), or on a Mac the AirPlay Receiver is using port 5000. Either stop that, or start on another port: `PORT=5001 python app.py` (then use port 5001 in every URL).
- *`ModuleNotFoundError`:* the virtual environment isn't active. Run `source .venv/bin/activate`.
- *First request hangs or is very slow:* the model is still loading or downloading. Wait, or run `python detector.py` first.
- *Everything fails with connection errors:* the service isn't running. Check the terminal where you ran `python app.py`.
