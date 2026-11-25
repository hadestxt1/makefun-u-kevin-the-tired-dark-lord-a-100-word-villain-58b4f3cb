#!/usr/bin/env python3
"""The Tired Dark Lord: A 100-Word Villain Monologue.

Writes one monologue of about 100 words, spoken by a fantasy villain
who is secretly just very tired. The tiredness lives in the voice, the
rhythm and the small deflections — a guttering candle, a lost thread,
a sentence that trails off — never in a plain statement that he is
weary. The speaker is still a villain with a scheme and a history:
three hundred years ago he took his brother's sword, weeping, and now
the seventh seal breaks at midnight, the gate opens, the tithe is
counted, and the machine he built no longer needs its maker. The last
line lands the sting: whatever the hero does, the Dark Lord finally
gets to sit down.

The program writes the monologue to /output/entry.txt and prints it to
stdout. The monologue is validated on every run and the program refuses
to write an invalid text.

Deterministic: no clock, no randomness, no network, stdlib only.
"""

import argparse
import os
import sys

MONOLOGUE = (
    "Come in. Mind the third step \u2014 it bites. I honed it the year "
    "your grandsire owed me grain and, ah... the candles gutter when "
    "I... where was I?\n"
    "\n"
    "The sword. Yes. My brother forged it weeping. I took it from him "
    "weeping, three hundred years ago, and the tears dried to salt on "
    "the scabbard. The seventh seal breaks at midnight. The gate opens. "
    "The tithe is counted. It all goes on \u2014 that is the joke, hero. "
    "I built a machine that no longer needs its maker.\n"
    "\n"
    "Strike, or kneel. Either way, I get to sit down."
)

OUTPUT_PATH = "/output/entry.txt"

MIN_WORDS = 90
MAX_WORDS = 110
MAX_CHARS = 600

# Words that would state the weariness plainly. The brief forbids
# announcing it: the tiredness must live in the voice, the rhythm and
# the small deflections, so the monologue must not contain any of them.
FORBIDDEN_WORDS = ("tired", "weary", "exhausted", "fatigue", "sleepy")


def word_count(text: str) -> int:
    """Count words the way a reader would: split on whitespace."""
    return len(text.split())


def validate_monologue(text: str) -> None:
    """Fail loudly unless the monologue is a valid entry text.

    Valid means: non-empty and not only whitespace, at most 600
    characters (the sealed scorer's gate), about 100 words, and never
    stating the weariness plainly.
    """
    if not text or not text.strip():
        raise ValueError("monologue must not be empty")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"monologue is {len(text)} characters, over the "
            f"{MAX_CHARS} limit"
        )
    words = word_count(text)
    if words < MIN_WORDS or words > MAX_WORDS:
        raise ValueError(
            f"monologue is {words} words, outside the "
            f"{MIN_WORDS}-{MAX_WORDS} range"
        )
    lowered = text.lower()
    for word in FORBIDDEN_WORDS:
        if word in lowered:
            raise ValueError(
                f"monologue must not state the weariness plainly: "
                f"contains {word!r}"
            )


def write_entry(path: str = OUTPUT_PATH) -> str:
    """Write the monologue to path (no trailing newline) and return it."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(MONOLOGUE)
    return MONOLOGUE


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Write a 100-word villain monologue to "
        "/output/entry.txt and print it. The monologue is validated "
        "first: non-empty, at most 600 characters, about 100 words.",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="only validate the monologue (non-empty, at most 600 "
        "characters, about 100 words, never stating the weariness "
        "plainly) and exit 0 if it passes, 1 if it fails",
    )
    parser.add_argument(
        "--output",
        default=OUTPUT_PATH,
        help="path of the entry file (default: /output/entry.txt)",
    )
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        validate_monologue(MONOLOGUE)
    except ValueError as exc:
        print(f"invalid monologue: {exc}", file=sys.stderr)
        return 1
    if args.verify:
        print(
            f"monologue valid: {word_count(MONOLOGUE)} words, "
            f"{len(MONOLOGUE)} characters"
        )
        return 0
    monologue = write_entry(args.output)
    print(monologue)
    return 0


if __name__ == "__main__":
    sys.exit(main())
