"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics

import config


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    # Curly apostrophes (it's, we'll) count as part of the word, like straight ones.
    return re.findall(r"[a-z0-9']+", text.lower().replace("\u2019", "'"))


# ── How raw measures become "how AI-like" ────────────────────────────────────
# Each raw measure is mapped onto 0–1 (1 = AI-like) with a straight line between
# two cut-offs. These cut-offs are first guesses from how the measures behave in
# general, NOT calibrated values. Milestone 4's four test inputs are where they
# get checked, and the README records any that move.

SPREAD_HUMAN_AT = 0.70   # sentence-length spread at or above this = fully human-like
SPREAD_AI_AT = 0.20      # at or below this = fully AI-like

VOCAB_HUMAN_AT = 0.85    # vocabulary variety at or above this = fully human-like
VOCAB_AI_AT = 0.60       # at or below this = fully AI-like

PUNCT_HUMAN_AT = 0.05    # punctuation marks per word at or below this = human-like
PUNCT_AI_AT = 0.20       # at or above this = AI-like

VOCAB_WINDOW = 50        # words per window for the vocabulary measure


def _scale(value: float, zero_at: float, one_at: float) -> float:
    """Straight-line map: `zero_at` -> 0.0 and `one_at` -> 1.0, clamped to 0-1.
    Works in either direction, which is how a measure that points the "wrong"
    way (low spread = AI) gets flipped."""
    t = (value - zero_at) / (one_at - zero_at)
    return min(max(t, 0.0), 1.0)


# ── The three measures ───────────────────────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies: the standard deviation of sentence lengths
    (in words) divided by their mean, so long and short texts are comparable.

    Scale: 0 = every sentence the same length. Around 0.2 is very even; around
    0.7 or more is lumpy. HIGHER MEANS MORE HUMAN-LIKE.

    A one-sentence text has no spread to measure, so this returns 0.0 for it.
    `style_signal` does NOT read that 0.0 as "very even" - it treats it as
    unknown and scores that part a neutral 0.5.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    return statistics.stdev(lengths) / mean if mean else 0.0


def type_token_ratio(text: str) -> float:
    """
    Vocabulary variety: unique words over total words, between 0 and 1.
    HIGHER MEANS MORE VARIED.

    Plain type-token ratio falls as text gets longer, so a long text and a short
    one can't be compared. Instead this averages the ratio over a sliding window
    of VOCAB_WINDOW words (or the whole text if it is shorter), which keeps
    texts of different lengths on the same footing.
    """
    ws = words(text)
    if not ws:
        return 0.0
    window = min(VOCAB_WINDOW, len(ws))
    ratios = [
        len(set(ws[i:i + window])) / window
        for i in range(len(ws) - window + 1)
    ]
    return sum(ratios) / len(ratios)


def punctuation_density(text: str) -> float:
    """
    Punctuation marks per word, counting commas, semicolons, colons, dashes and
    parentheses. Full stops, question marks and exclamation marks are left out:
    they only mark sentence ends, and the sentence-length measure already covers
    that. HIGHER MEANS MORE PUNCTUATION.
    """
    marks = re.findall(r"[,;:()\u2014\u2013]|--", text)
    n = len(words(text))
    return len(marks) / n if n else 0.0


# ── Combining them ───────────────────────────────────────────────────────────

def style_parts(text: str) -> dict:
    """Each measure's raw value and its 0-1 AI-likeness, for debugging."""
    spread = sentence_length_spread(text)
    vocab = type_token_ratio(text)
    punct = punctuation_density(text)

    # With under two sentences there is no spread to read: stay neutral.
    if len(sentences(text)) < 2:
        spread_ai = 0.5
    else:
        spread_ai = _scale(spread, SPREAD_HUMAN_AT, SPREAD_AI_AT)

    return {
        "spread": spread, "spread_ai": spread_ai,
        "vocab": vocab, "vocab_ai": _scale(vocab, VOCAB_HUMAN_AT, VOCAB_AI_AT),
        "punct": punct, "punct_ai": _scale(punct, PUNCT_HUMAN_AT, PUNCT_AI_AT),
    }


def style_signal(text: str) -> float:
    """
    The style signal as a 0-1 score. **Higher means more likely AI**, the same
    direction as `detector.model_signal`.

    Directions: each measure is flipped or scaled onto 0-1 where 1 = AI-like.
      - spread:      LOW spread = AI-like (sentences march in step)  -> flipped
      - vocab:       LOW variety = AI-like (narrow vocabulary)       -> flipped
      - punctuation: HIGH density = AI-like                          -> not flipped
    The three are then averaged with the weights in config.py.
    """
    if not words(text):
        return 0.5

    p = style_parts(text)
    score = (
        config.STYLE_WEIGHT_SPREAD * p["spread_ai"]
        + config.STYLE_WEIGHT_VOCAB * p["vocab_ai"]
        + config.STYLE_WEIGHT_PUNCT * p["punct_ai"]
    )
    return round(score, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    parts = style_parts(text)
    print(f"sentence_length_spread   {parts['spread']:.3f}   -> AI-likeness {parts['spread_ai']:.2f}")
    print(f"type_token_ratio         {parts['vocab']:.3f}   -> AI-likeness {parts['vocab_ai']:.2f}")
    print(f"punctuation_density      {parts['punct']:.3f}   -> AI-likeness {parts['punct_ai']:.2f}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
