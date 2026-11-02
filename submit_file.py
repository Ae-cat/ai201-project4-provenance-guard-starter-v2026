"""
Submit a text file to the running service and print the response.

    python submit_file.py calibration/pet_article.txt

Handy for testing, because curl struggles with quotes and line breaks in text.
Start the service first (python app.py).
"""

import json
import sys
import urllib.error
import urllib.request

URL = "http://127.0.0.1:5000/submit"


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: python submit_file.py <file.txt> [creator_id]")
    text = open(sys.argv[1], encoding="utf-8").read().strip()
    creator = sys.argv[2] if len(sys.argv) > 2 else "me"
    body = json.dumps({"text": text, "creator_id": creator}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            print(json.dumps(json.load(resp), indent=2))
    except urllib.error.HTTPError as err:
        print(err.code, json.dumps(json.load(err), indent=2))


if __name__ == "__main__":
    main()
