#!/usr/bin/env python3
"""The cheap contract checks, run before pushing instead of one per red build.

Written 2026-08-09. Five city files grew that morning and the deploy went red
four times in a row, each build surfacing exactly one violation because a
build throws on the first error it meets: a stale count promise, then an
intro over the word range, then a description over 155. Each round trip cost
a push and two minutes. Everything below is already enforced at build time in
site/src, and it is enforced there too; this only moves the finding-out to
before the push. It is a mirror, never the authority: when the two disagree
the Astro build wins and this file is the thing that is wrong.

Usage: python3 scripts/preflight.py
"""
import glob
import json
import os
import re
import sys

DESC_MAX = 155          # site/src/lib/site-config.ts
INTRO_MIN, INTRO_MAX = 60, 100   # Contract C, site/src/pages/[city].astro

WORDS = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
         "fifteen sixteen seventeen eighteen nineteen twenty twenty-one twenty-two twenty-three "
         "twenty-four twenty-five twenty-six twenty-seven twenty-eight twenty-nine thirty").split()
NUM = {w: i for i, w in enumerate(WORDS)}
N = "|".join([r"\d+"] + sorted(WORDS, key=len, reverse=True))
NMW = r"(?<![\w-])"      # not the tail of a compound number
SUMMARY = {"meta_description", "question_meta"}
ALL_COPY = {"intro", "meta_description", "question_meta", "question_answer", "question_context", "faq"}

PROMISE = [
    (re.compile(NMW + r"(%s)\s+(?:most|remarkable)\b" % N, re.I), lambda n: {n}, ALL_COPY),
    (re.compile(NMW + r"(%s)\s+more\b" % N, re.I), lambda n: {n + 1, n + 2}, SUMMARY),
    (re.compile(r"\bof the\s+" + NMW + r"(%s)\s+trees?\b" % N, re.I), lambda n: {n}, ALL_COPY),
    (re.compile(r"\b(?:these|the)\s+" + NMW +
                r"(%s)\s+(?:are|is|need|needs|were|was|stand|stands|remain|listed|below)\b" % N, re.I),
     lambda n: {n}, ALL_COPY),
    (re.compile(r"\ball\s+" + NMW + r"(%s)\s+(?:trees?|are|stand|need|needs|remain)\b" % N, re.I),
     lambda n: {n}, ALL_COPY),
]


def check_city(path):
    d = json.load(open(path))
    slug = os.path.basename(path)[:-5]
    n = len(d.get("trees", []))
    out = []

    intro = (d.get("intro") or "").strip()
    if not intro:
        out.append("%s: no intro, Contract C requires 60-100 words" % slug)
    else:
        wc = len(intro.split())
        if not INTRO_MIN <= wc <= INTRO_MAX:
            out.append("%s: intro is %d words, Contract C requires %d-%d" % (slug, wc, INTRO_MIN, INTRO_MAX))

    for key in ("meta_description", "question_meta"):
        v = d.get(key) or ""
        if len(v) > DESC_MAX:
            out.append("%s: %s is %d chars, the limit is %d" % (slug, key, len(v), DESC_MAX))

    fields = [(k, d.get(k) or "") for k in
              ("intro", "meta_description", "question_meta", "question_answer", "question_context")]
    for f in d.get("faq") or []:
        fields += [("faq", f.get("q") or ""), ("faq", f.get("a") or "")]
    for key, text in fields:
        if not text:
            continue
        for rx, allowed, scope in PROMISE:
            if key not in scope:
                continue
            for m in rx.finditer(text):
                w = m.group(1).lower()
                claims = allowed(int(w) if w.isdigit() else NUM[w])
                if min(claims) < 4 or n in claims:
                    continue
                out.append("%s: %s promises %s trees but the city has %d (%r)" % (
                    slug, key, "/".join(str(c) for c in sorted(claims)), n, m.group(0)))
    return out


# Contract B, mirrored from site/src/pages/[city]/oldest-tree.astro. Added
# 2026-08-13 after four new cities went out with a 46-word question_context and
# the deploy went red on the first one: preflight checked the intro's word range
# and the description's length and had never looked at this field, so the whole
# point of running it before pushing was lost. Same mirror rule as the rest of
# this file: the Astro build is the authority and this only moves the finding-out
# earlier.
CONTEXT_MIN, CONTEXT_MAX = 150, 200


def check_contract_b(slug, d):
    out = []
    if not (d.get("trees") or []):
        return out
    answer = (d.get("question_answer") or "").strip()
    context = (d.get("question_context") or "").strip()
    if not answer or not context:
        out.append("%s: question_answer and question_context must both be written (Contract B)" % slug)
        return out
    wc = len(context.split())
    if wc < CONTEXT_MIN or wc > CONTEXT_MAX:
        out.append("%s: question_context is %d words, Contract B requires %d-%d"
                   % (slug, wc, CONTEXT_MIN, CONTEXT_MAX))
    return out


RECOGNISE_MAX = 240
# Hidde, 2026-08-12, seeing the field on all eleven Den Bosch trees: "kun je deze
# which one is it functie weghalen, hij is alleen in den bosch, dit zou logisch
# om dieper te doen bij specifiek bomen die moeilijk te vinden zijn. niet bij
# elke in den bosch." Two failures at once. It was on every tree in the city
# including ones standing alone with nothing to confuse them for, and the longest
# ran to 499 characters of method: a register id, a re-confirmation date, GPS
# coordinates and an aerial-imagery cross-check. That is our working shown to a
# reader who asked which trunk to walk to, which is the builder-speak rule
# arriving in a new field.
#
# So the field is for trees a visitor genuinely cannot pick out: near-identical
# neighbours of the same species, close enough that the pin cannot settle it.
# One plain sentence about what you SEE. Never the evidence behind it.
RECOGNISE_METHOD = [
    r"register id", r"registered GPS", r"aerial imagery", r"cross-check",
    r"re-confirmed", r"\bper both\b", r"\b20\d\d-\d\d-\d\d\b",
    r"municipal register", r"coordinates",
]


def check_recognise(slug, d):
    out = []
    for tree in d.get("trees") or []:
        v = (tree.get("how_to_recognise") or "").strip()
        if not v:
            continue
        if len(v) > RECOGNISE_MAX:
            out.append("%s: %s how_to_recognise is %d chars, the limit is %d. "
                       "One plain sentence about what you see."
                       % (slug, tree.get("id"), len(v), RECOGNISE_MAX))
        for pat in RECOGNISE_METHOD:
            if re.search(pat, v, re.I):
                out.append("%s: %s how_to_recognise shows our method (%s). "
                           "The reader wants the tree, not the evidence."
                           % (slug, tree.get("id"), pat))
    return out


# Two cities must never share an id prefix. Added 2026-08-13, after a Portland
# write pass came back with ten trees numbered por_001 to por_010, which is
# Porto's prefix and covers ten live, indexed Porto trees. Merging would have
# overwritten them, which is hard rule 3. The writing pass caught it and refused;
# the brief that told it to use por_ was mine, written without running
# passcheck.py --brief, which prints the free prefix precisely so this cannot
# happen. A mechanism nobody runs is not a mechanism, so this one runs itself.
def check_id_prefixes():
    import collections
    owner = collections.defaultdict(set)
    for path in sorted(glob.glob("data/cities/*.json")):
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        for tree in d.get("trees") or []:
            tid = tree.get("id") or ""
            if "_" in tid:
                owner[tid.split("_")[0]].add(d.get("city") or path)
    out = []
    for prefix, cities in sorted(owner.items()):
        if len(cities) > 1:
            out.append("id prefix %r is used by %s: two cities sharing a prefix "
                       "will overwrite each other's trees" % (prefix, ", ".join(sorted(cities))))
    return out


# A pin a pin pass could not confirm must not become "confirmed" later without
# NEW evidence. Added 2026-08-13, after Baarn's brn_005. The pin pass wrote in
# data/research/baarn-pins.json that the tree's marker "could not be located in
# the aerial imagery" and left it approximate. A later pass set it to confirmed
# citing that same aerial survey, and the pin turned out to sit 60 metres off,
# on a different tree. Nothing was fabricated at any step: an earlier finding of
# our own simply sat in a file nobody re-read. So the file reads itself now.
# New evidence is a real thing (a site visit, a register coordinate, Wikidata,
# OSM, a fresh aerial check), named in the tree's own sources.
PIN_NEW_EVIDENCE = re.compile(
    r"on-site|site visit|photograph|register|geoproxy|arcgis|wikidata|inaturalist"
    r"|overpass|openstreetmap|\bosm\b|pdok|luchtfoto|aerial|geoportal|gis\b", re.I)


def check_pin_upgrades():
    pins = {}
    for path in sorted(glob.glob("data/research/*-pins.json")):
        try:
            with open(path, encoding="utf-8") as fh:
                d = json.load(fh)
        except (ValueError, OSError):
            continue
        rows = d if isinstance(d, list) else (d.get("pins") or d.get("trees") or [])
        for r in rows:
            if isinstance(r, dict) and r.get("id"):
                pins[r["id"]] = (os.path.basename(path), r.get("new_precision"))
    out = []
    for path in sorted(glob.glob("data/cities/*.json")):
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        for tree in d.get("trees") or []:
            prev = pins.get(tree.get("id"))
            if not prev or prev[1] != "approximate":
                continue
            if tree.get("location_precision") != "confirmed":
                continue
            if not PIN_NEW_EVIDENCE.search(" ".join(tree.get("verified_sources") or [])):
                out.append(
                    "%s: %s is marked confirmed, but %s recorded this pin as approximate "
                    "and no source names new evidence (a site visit, a register or Wikidata "
                    "coordinate, OSM, a fresh aerial check). Say where the certainty came "
                    "from, or leave it approximate."
                    % (os.path.basename(path)[:-5], tree.get("id"), prev[0]))
    return out


def main():
    problems = check_id_prefixes() + check_pin_upgrades()
    files = sorted(glob.glob("data/cities/*.json"))
    for p in files:
        problems += check_city(p)
        with open(p, encoding='utf-8') as fh:
            problems += check_recognise(os.path.basename(p)[:-5], json.load(fh))
        with open(p, encoding='utf-8') as fh2:
            problems += check_contract_b(os.path.basename(p)[:-5], json.load(fh2))
    for line in problems:
        print("FAIL " + line)
    print("preflight: %d cities checked, %d problems" % (len(files), len(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
