"""
Print both signals side by side for every .txt file in calibration/.

    python compare.py

Milestone 4: use this to see where your two signals agree and where they split.
Empty files are skipped, so you can add your own writing and re-run.
"""

from pathlib import Path

import detector
import scoring
import stylometry

FOLDER = Path(__file__).parent / "calibration"


def main():
    rows = []
    for f in sorted(FOLDER.glob("*.txt")):
        text = f.read_text(encoding="utf-8").strip()
        if not text:
            print(f"(skipping {f.name}: empty - paste some writing into it)")
            continue
        rows.append((
            f.stem,
            len(text.split()),
            detector.model_signal(text),
            stylometry.style_signal(text),
        ))

    print(f"\n{'input':<16}{'words':>6}{'model':>9}{'style':>9}{'gap':>9}{'combined':>10}")
    print("-" * 59)
    for name, n, m, s in rows:
        print(f"{name:<16}{n:>6}{m:>9.3f}{s:>9.3f}{m - s:>+9.3f}{scoring.combine_signals(m, s):>10.3f}")
    print("\nhigher = more likely AI.  gap = model - style (big = the signals split)")


if __name__ == "__main__":
    main()
