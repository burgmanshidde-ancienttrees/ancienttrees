#!/usr/bin/env python3
"""Which trees a park page holds, derived exactly as the site derives it.

A park is not a field on a tree. site/src/lib/parks.ts reads the tree's
neighbourhood, then its address, takes the clause before the first comma, and
calls it a park when it contains one of PARK_WORDS or is named in
data/park-names.json. This file is that function in Python, so a check can
count a park page's trees BEFORE a push instead of the Astro build finding out
in CI (2026-10-10: 45 Dutch trees retired, two park pages still promising the
old counts, main's deploy red for two and a half hours).

The word list is read from parks.ts itself rather than copied, so there is one
list. When the two ever disagree, parks.ts is right and this file is wrong.

Usage: python3 scripts/park_groups.py <city-slug>   prints the city's parks
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARKS_TS = os.path.join(ROOT, "site", "src", "lib", "parks.ts")

PARK_MIN_TREES = 5   # parks.ts PARK_MIN_TREES
PARK_WAIVER_MIN = 3  # parks.ts PARK_WAIVER_MIN

_WORDS = None
_EXPLICIT = None


def park_words():
    global _WORDS
    if _WORDS is None:
        with open(PARKS_TS, encoding="utf-8") as fh:
            m = re.search(r"const PARK_WORDS = \[(.*?)\];", fh.read(), re.S)
        if not m:
            raise SystemExit("%s: cannot find PARK_WORDS" % PARKS_TS)
        _WORDS = re.findall(r'"([^"]+)"', m.group(1))
    return _WORDS


def explicit_parks():
    global _EXPLICIT
    if _EXPLICIT is None:
        _EXPLICIT = set()
        try:
            with open(os.path.join(ROOT, "data", "park-names.json"), encoding="utf-8") as fh:
                _EXPLICIT = {k.lower() for k in (json.load(fh).get("parks") or {})}
        except (OSError, ValueError):
            pass  # same as parks.ts: no file means no explicit parks
    return _EXPLICIT


def renderable(tree):
    """trees.ts treeIsRenderable(): a story and both coordinates."""
    loc = tree.get("location") or {}
    return bool(tree.get("story")) and loc.get("latitude") is not None \
        and loc.get("longitude") is not None


def park_key(tree):
    """parks.ts parkKey(): the named park a tree stands in, or None."""
    loc = tree.get("location") or {}
    heads = []
    for field in (loc.get("neighbourhood"), loc.get("address")):
        head = str(field if field is not None else "").split(",")[0]
        head = re.sub(r"\([^)]*\)?", "", head)
        head = re.sub(r"\s+", " ", head).strip()
        head = re.sub(r"^[-/\s]+|[-/\s]+$", "", head)
        if len(head) < 4:
            continue
        if any(w in head.lower() for w in park_words()):
            return head
        heads.append(head)
    explicit = explicit_parks()
    for head in heads:
        if head.lower() in explicit:
            return head
    return None


def city_parks(city_doc):
    """{park name: [trees]} for one city's renderable trees."""
    out = {}
    for t in city_doc.get("trees") or []:
        if not renderable(t):
            continue
        name = park_key(t)
        if name:
            out.setdefault(name, []).append(t)
    return out


def page_allowed(n, intro):
    """parks.ts parkPageIsAllowed(): Contract H's gate."""
    if not intro:
        return False
    if n >= PARK_MIN_TREES:
        return True
    return n >= PARK_WAIVER_MIN and bool(intro.get("below_gate"))


def park_intros(city_slug=None):
    """(path, intro) for every data/parks file, optionally for one city."""
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "parks", "*.json"))):
        with open(path, encoding="utf-8") as fh:
            intro = json.load(fh)
        if city_slug is None or intro.get("city_slug") == city_slug:
            yield path, intro


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[-1])
        return 2
    slug = sys.argv[1]
    with open(os.path.join(ROOT, "data", "cities", slug + ".json"), encoding="utf-8") as fh:
        groups = city_parks(json.load(fh))
    pages = {i.get("park"): os.path.basename(p) for p, i in park_intros(slug)}
    for name, trees in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        print("%3d  %s%s" % (len(trees), name, "  (page: %s)" % pages[name] if name in pages else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
