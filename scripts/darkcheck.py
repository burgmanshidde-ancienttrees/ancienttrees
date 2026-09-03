#!/usr/bin/env python3
"""darkcheck.py - the app's palette, measured, in both appearances.

Written 2026-09-03. The app had a dark palette from the day it had a palette at
all, and nobody had ever measured it, because measuring a colour pair is exactly
the kind of arithmetic a person does not do by eye. White on the dark palette's
moss came out at 2.85:1, well under half of what a line of text needs, and it
was the fill of the primary button on every screen that has one. It read as a
highlighter slab with pale text on it and it had shipped.

This is the ratchet CLAUDE.md describes: a class of error found twice becomes a
check rather than a third note. It parses Brand out of Kit/Style.swift, so there
is no second copy of the palette to drift, and it asks the only question a
script can answer here: can this be read. Whether it is any good is still a
matter of looking at the screens, which is what appsweep --dark is for.

    python3 scripts/darkcheck.py          # both appearances, exit 1 on a fail
    python3 scripts/darkcheck.py --list   # print every pair and its ratio
"""

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
STYLE = ROOT / "ios" / "AncientTrees" / "AncientTrees" / "Kit" / "Style.swift"

# WCAG AA. 4.5:1 for text a person reads, 3:1 for a large heading or the edge of
# a control. Nothing here is stricter than the standard: the point is to catch a
# pair that is nowhere near, not to police a decimal.
TEXT = 4.5
LARGE = 3.0

# foreground, background, what it is, the floor it has to clear.
PAIRS = [
    ("ink", "ground", "body text on a screen", TEXT),
    ("ink", "surface", "body text on a card", TEXT),
    ("inkSoft", "ground", "a subtitle on a screen", TEXT),
    ("inkSoft", "surface", "a subtitle on a card", TEXT),
    ("moss", "ground", "a link on a screen", TEXT),
    ("moss", "surface", "a link on a card", TEXT),
    ("onMoss", "moss", "the label on the primary button", TEXT),
    ("goldInk", "surface", "gold set as text", TEXT),
    ("gold", "surface", "the season badge fill", 1.2),
    ("hairline", "surface", "the edge of a card", 1.2),
]


def palette():
    """Brand's colours, as {name: (light, dark)}, read from the Swift itself."""
    text = STYLE.read_text()
    found = {}
    for name, light, dark in re.findall(
            r"static let (\w+)\s*=\s*Color\(light:\s*0x([0-9A-Fa-f]{6}),"
            r"\s*dark:\s*0x([0-9A-Fa-f]{6})\)", text):
        found[name] = (int(light, 16), int(dark, 16))
    if not found:
        sys.exit("darkcheck: found no Brand colours in Style.swift. Has the "
                 "palette moved? This check reads the Swift so there is no "
                 "second copy of it to go stale.")
    return found


def luminance(hexval):
    def channel(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (hexval >> 16) & 255, (hexval >> 8) & 255, hexval & 255
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="print every pair")
    args = ap.parse_args()

    colours = palette()
    fails = []
    for index, appearance in enumerate(("light", "dark")):
        if args.list:
            print(f"\n{appearance}")
        for front, back, what, floor in PAIRS:
            if front not in colours or back not in colours:
                fails.append(f"{appearance}: no colour called "
                             f"{front if front not in colours else back}")
                continue
            r = ratio(colours[front][index], colours[back][index])
            ok = r >= floor
            if args.list:
                print(f"  {front:>9} on {back:<13} {r:5.2f}:1  "
                      f"{'ok ' if ok else 'FAIL'}  {what}")
            if not ok:
                fails.append(f"{appearance}: {front} on {back} is {r:.2f}:1, "
                             f"under {floor}:1, and it is {what}")

    if fails:
        print("\n".join("  " + f for f in fails))
        sys.exit("the palette has a pair nobody can read")
    print(f"the palette reads in both appearances ({len(PAIRS)} pairs each)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
