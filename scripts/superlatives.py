#!/usr/bin/env python3
"""Two of our own pages claiming the same crown.

Hard rule 8 used to ask a writer to check every superlative against everything
else the site says, which meant holding a thousand stories in your head, so in
practice a pass either guessed or refused. Hidde loosened it on 2026-08-13:
"wat maakt t uit als je het net fout hebt over dikte of hoogte... 80/20 is goed,
liever wel online en af en toe een foutje dan zo spastisch over iets niets
belangrijks."

He is right about accuracy: a girth off by a metre is an edit and a reader can
tell us. But one half of the old rule was never about accuracy. If two pages
each call their tree the largest fig in Palermo, that is not imprecision, it is
the site contradicting itself in one breath, and a reader who notices stops
trusting both pages.

So the writing rule is gone and this is what replaces it. Write the superlative
you believe; this finds the collisions afterwards, which is the cheap direction.

    python3 scripts/superlatives.py            # collisions, grouped
    python3 scripts/superlatives.py --all      # every superlative, for a read

A collision is two DIFFERENT trees making the same kind of claim about the same
place: same superlative word, same noun, same scope. "The oldest tree in Lisbon"
on two trees collides. "The oldest olive in Lisbon" and "the oldest tree in
Lisbon" do not, and neither does the same claim repeated in one tree's own story
and its city page, because those describe the same tree.
"""
import argparse
import collections
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# "the oldest tree in Lisbon", "the largest plane in Europe", "the tallest
# tree on this site". Deliberately narrow: a superlative with a noun and a
# scope, which is the shape that can collide.
CLAIM = re.compile(
    r"\b(?:the\s+)?(oldest|largest|biggest|tallest|thickest|widest|broadest|"
    r"heaviest|rarest|first)\s+([a-z][a-z-]{2,20}(?:\s+[a-z][a-z-]{2,20})?)\s+"
    r"(?:in|of|on)\s+((?:the\s+)?[A-Z][\w'-]*(?:\s+[A-Z][\w'-]*)?)",
    re.I,
)
# Words that are not the thing being ranked, so "the oldest of the three" and
# "the first world war" never register as claims.
STOP = {"the", "them", "these", "those", "his", "her", "its", "world", "war",
        "time", "century", "part", "half", "one", "two", "three", "four"}
# A claim about a SPECIES is a fact about botany, not a crown our tree wears.
# Two coast redwoods both saying their species is the tallest on earth are both
# right, and flagging them would train a reader of this report to ignore it.
NOT_A_CROWN = re.compile("\\bspecies\\b|\\bgenus\\b|\\bfamily\\b|\\bspecimen of\\b|"
                          "\\bhybrid\\b|\\bhybrids\\b", re.I)


def claims():
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        city = d.get("city", os.path.basename(path)[:-5])
        for tree in d.get("trees") or []:
            for field in ("story", "name"):
                text = tree.get(field) or ""
                for m in CLAIM.finditer(text):
                    sup, noun, scope = (g.strip().lower() for g in m.groups())
                    # Check a window before the match too: "London planes are
                    # hybrids, first bred in..." puts the word that marks this
                    # as a species fact rather than a crown BEFORE "first",
                    # outside the matched span itself.
                    window = text[max(0, m.start() - 40):m.end()]
                    if noun.split()[0] in STOP or NOT_A_CROWN.search(window):
                        continue
                    out.append({"city": city, "id": tree.get("id"),
                                "name": tree.get("name"), "sup": sup,
                                "noun": noun, "scope": scope,
                                "text": m.group(0)})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="list every claim found")
    a = ap.parse_args()
    rows = claims()

    if a.all:
        for r in rows:
            print("  %-14s %-9s %s" % (r["city"][:14], r["id"], r["text"]))
        print("\n%d superlative claim(s) across the corpus" % len(rows))
        return 0

    # A generic scope ("in the city", "on this list", "of its species") is only
    # a collision INSIDE one city: "the oldest tree in the city" said in
    # Amsterdam and in Istanbul is two true sentences, not a contradiction. A
    # named scope ("in Lisbon", "in Europe") collides wherever it is said.
    GENERIC = ("the city", "the garden", "the entire garden", "this list",
               "its species", "earth", "the park", "the world", "the site",
               "this site", "the country", "the grounds", "the collection")
    by = collections.defaultdict(list)
    for r in rows:
        scope = r["scope"]
        key_scope = ("%s (%s)" % (scope, r["city"])) if scope in GENERIC else scope
        by[(r["sup"], r["noun"], key_scope)].append(r)
    clashes = {k: v for k, v in by.items()
               if len({x["id"] for x in v}) > 1}
    if not clashes:
        print("%d superlative claim(s), no two trees claiming the same crown" % len(rows))
        return 0
    print("%d collision(s): different trees making the same claim\n" % len(clashes))
    for (sup, noun, scope), v in sorted(clashes.items()):
        print("  %s %s in %s" % (sup, noun, scope))
        for x in v:
            print("      %-9s %-38s %s" % (x["id"], (x["name"] or "")[:38], x["text"]))
    print("\nOne of each pair is wrong, or they mean different things and should say so.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
