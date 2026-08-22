#!/usr/bin/env python3
"""Catch the mistakes that translation passes keep finding for us.

Written 2026-08-22, after fourteen translation passes found roughly thirty
errors in published English pages in one day. The uncomfortable part is not
that the errors existed; it is that our existing checks ran over every one of
them and reported clean. qa.py greps rendered text, superlatives.py matches
phrasing, and every fault below is SEMANTIC: a number that contradicts another
number, a date that contradicts an age, a count that contradicts the data
sitting next to it.

A translator caught them because a translator cannot skim. Every clause has to
be understood before it can be re-expressed, and a sentence that means nothing
stops the work. That is expensive comprehension, and it should not be the only
thing standing between an arithmetic slip and a reader.

Three classes, all mechanical, all drawn from real faults found today:

  COUNT   "All sixteen mapped" on a page with 21 trees (the-hague).
          "Eight of the ten stand in free parks" where nine are free (nice).
          "Three of the four are camphors" where all four are (osaka).
  AGE     Planted 1840, "a 30 year old tree" in the 1860s (paris par_009).
          Planted 1780, "already mature" in 1794 (zurich zur_001).
          750 years old, "predates the Kamakura shogunate" of 1185 (tokyo).
  CLASH   par_005 says seven metres, par_014 says eight, same tree.
          mad_005 and mad_006 both the tallest in one garden.

It reports, it does not fix. Several hits will be legitimate: "the three
trees" often means three of them, not all of them, so the count check only
fires on a total-shaped claim. Read the output, do not obey it.

Usage:
  python3 scripts/consistency.py            # every city
  python3 scripts/consistency.py rome nice  # named cities
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CITIES = os.path.join(ROOT, "data", "cities")

WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve "
    "thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
WORDS.update({"twenty-one": 21, "twenty-two": 22, "twenty-three": 23, "twenty-four": 24,
              "twenty-five": 25, "twenty-six": 26, "twenty-seven": 27, "twenty-eight": 28,
              "twenty-nine": 29, "thirty": 30, "thirty-one": 31, "thirty-two": 32,
              "thirty-three": 33, "forty": 40, "fifty": 50})
NUM = r"(?:\d{1,3}|%s)" % "|".join(sorted(WORDS, key=len, reverse=True))


def num(tok):
    tok = tok.lower()
    return int(tok) if tok.isdigit() else WORDS.get(tok)


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text or "") if s.strip()]


def count_claims(city, trees, out):
    """A claim about how many trees the PAGE has, checked against the page.

    Only total-shaped claims: "all N mapped", "N verified trees", "N of the M".
    A bare "the three trees" is usually a subset and is deliberately ignored,
    because chasing those produced three false alarms for every real hit."""
    n = len(trees)
    blob = " ".join(str(city.get(k) or "") for k in
                    ("intro", "meta_description", "question_meta", "question_answer", "question_context"))
    for m in re.finditer(r"\ball\s+(%s)\s+(?:mapped|of them|trees)\b" % NUM, blob, re.I):
        v = num(m.group(1))
        if v and v != n:
            out.append(("COUNT", "says all %s, page has %d" % (m.group(1), n), m.group(0)))
    for m in re.finditer(r"\b(%s)\s+(?:verified|remarkable|ancient)\s+trees\b" % NUM, blob, re.I):
        v = num(m.group(1))
        if v and v != n:
            out.append(("COUNT", "claims %s trees, page has %d" % (m.group(1), n), m.group(0)))
    # "N of the M" where M should be the page total
    for m in re.finditer(r"\b(%s)\s+of\s+the\s+(%s)\b" % (NUM, NUM), blob, re.I):
        tot = num(m.group(2))
        if tot and tot != n and abs(tot - n) <= 6:
            out.append(("COUNT", "'of the %s' but the page has %d" % (m.group(2), n), m.group(0)))


def age_claims(tree, out):
    """A planting year plus a claim about the tree's state at a later year.

    "Planted in 1840, it was a 30 year old tree when ... the 1860s" is the
    shape. So is "planted in 1780 ... already mature when Napoleon crossed the
    Rhine", which needs the reader to know the date; only the arithmetic form
    is checked here, because the other needs history rather than a regex."""
    story = tree.get("story") or ""
    planted = re.search(r"\bplanted (?:in|around) (\d{4})\b", story, re.I)
    if not planted:
        return
    py = int(planted.group(1))
    for s in sentences(story):
        m = re.search(r"\b(?:a|was)\s+(%s)[\s-]+year[\s-]old\b" % NUM, s, re.I)
        y = re.search(r"\b(?:in the )?(\d{4})s?\b", s)
        if m and y:
            claimed, when = num(m.group(1)), int(y.group(1))
            if claimed and when > py:
                actual = when - py
                if abs(actual - claimed) > 5:
                    out.append(("AGE", "planted %d, called %s years old around %d (that is %d)"
                                % (py, m.group(1), when, actual), s[:110]))


def crown_clashes(trees, out):
    """Two trees on one page claiming the same superlative over the same place.

    superlatives.py matches the phrasing of a claim; this looks for the SHAPE
    (a superlative plus a place) so a paraphrase cannot walk past. mad_005 said
    "the tallest tree in" a garden and mad_006 said it "wins on height" there
    and was "the garden's tallest resident"; only one of those three is a
    phrasing the other checker knows."""
    SUP = r"(tallest|thickest|widest|biggest|largest|oldest|heaviest)"
    seen = {}
    for t in trees:
        story = (t.get("story") or "")
        for m in re.finditer(r"%s\b" % SUP, story, re.I):
            word = m.group(1).lower()
            ctx = story[max(0, m.start() - 90):m.start() + 90]
            place = re.search(r"\b(?:in|of|at)\s+(?:the\s+)?([A-Z][\w'’-]*(?:\s+[A-Z][\w'’-]*){0,3})", ctx)
            if not place:
                continue
            key = (word, place.group(1).strip())
            if key in seen and seen[key] != t["id"]:
                out.append(("CLASH", "%s and %s both claim '%s' in %s"
                            % (seen[key], t["id"], word, place.group(1)), ctx.strip()[:110]))
            seen.setdefault(key, t["id"])


def measure_clashes(trees, out):
    """Two entries giving different measurements for one named tree.

    par_005 said the Monceau plane had a seven metre waist; par_014 said the
    same tree measured eight metres around. Neither matched the register."""
    metres = {}
    for t in trees:
        for m in re.finditer(r"\b(%s|\d+(?:\.\d+)?)\s*met(?:re|er)s?\s+(?:around|in girth|round)\b" % NUM,
                             t.get("story") or "", re.I):
            v = num(m.group(1)) if not re.match(r"^\d+\.", m.group(1)) else float(m.group(1))
            ctx = (t.get("story") or "")[max(0, m.start() - 70):m.start()]
            place = re.search(r"\b([A-Z][\w'’-]*(?:\s+[A-Z][\w'’-]*){0,2})\s*$", ctx.strip())
            if v and place:
                key = place.group(1).strip()
                if key in metres and abs(metres[key][0] - v) > 0.6:
                    out.append(("CLASH", "%s says %s m and %s says %s m for %s"
                                % (metres[key][1], metres[key][0], t["id"], v, key), ctx.strip()[-90:]))
                metres.setdefault(key, (v, t["id"]))


def main():
    names = sys.argv[1:]
    total = 0
    for f in sorted(os.listdir(CITIES)):
        if not f.endswith(".json"):
            continue
        slug = f[:-5]
        if names and slug not in names:
            continue
        with open(os.path.join(CITIES, f), encoding="utf-8") as fh:
            city = json.load(fh)
        trees = city.get("trees") or []
        if not trees:
            continue
        out = []
        count_claims(city, trees, out)
        for t in trees:
            age_claims(t, out)
        crown_clashes(trees, out)
        measure_clashes(trees, out)
        if out:
            total += len(out)
            print("\n%s (%d trees)" % (slug, len(trees)))
            for kind, why, frag in out:
                print("  %-6s %s" % (kind, why))
                print("         %s" % frag)
    print("\n%d possible inconsistencies. These are leads, not verdicts: read each one."
          % total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
