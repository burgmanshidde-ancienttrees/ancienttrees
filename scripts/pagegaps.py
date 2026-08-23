#!/usr/bin/env python3
"""Which species, country and park pages the data has earned but nobody wrote.

Hidde, 2026-08-13, on being shown that 255 species and 24 countries had trees
but no page: "wat mij betreft mogen die intros gewoon geautomatiseerd geschreven
worden, ik snap niet waar we zo moeilijk over doen, bouw gewoon."

He is right, and the thing I had made difficult was imaginary. SEO_GEO_BLUEPRINT
Contracts F and G require that a species or country page HAS a written intro.
They do not say a human must type it. A pass writing one is the same arrangement
we already use for tree stories and city copy, so nothing in that document has
to change and hard rule 7 is not in play.

What was in play is real and stays: P3 forbids fill-in-the-city-name templating,
so these intros are written per subject from its own trees, never generated from
a pattern. This script only says WHAT is missing and how much traffic-shaped
evidence sits behind it. A writing pass does the writing.

    python3 scripts/pagegaps.py             # the ranked gaps
    python3 scripts/pagegaps.py --next 30   # the batch to brief next
    python3 scripts/pagegaps.py --check     # exit 1 if a big gap has opened

A species page is worth writing when several trees share it, because the page
then genuinely lists something; a country page as soon as the country has trees
at all, because it is the entry point from a whole class of search. Parks carry
their own threshold in site/src/lib/parks.ts and this mirrors it.
"""
import argparse
import collections
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARK_MIN_TREES = 5          # mirrors site/src/lib/parks.ts
SPECIES_MIN_TREES = 3       # below this a species page lists too little to be a page
# A country page needs three cities before it renders (COUNTRY_MIN_CITIES in
# site/src/lib/species.ts). Reporting a one-city country as a gap sends a pass
# to write prose that cannot appear: nine of the ten country intros written on
# 2026-08-13 are correct, complete and invisible, waiting on a third city. So a
# country counts as a gap only once it can actually render, and the ones below
# the line are reported separately as waiting on coverage rather than on words.
COUNTRY_MIN_CITIES = 3
# Mirrors PARK_WORDS in site/src/lib/parks.ts exactly, including the trailing
# space on "villa " (Real Alcazar de Sevilla contains "villa" as a substring of
# "Sevilla" but not "villa " with a space, and matching without the space
# reported a park page gap that could never build: no tree there actually
# groups under that name in the site's own parkKey()).
PARKISH = re.compile(
    r"park|garden|jardin|jardim|giardin|parc|parco|tuin|villa |orto|botanic|"
    r"bois|hortus|schlosspark|stadtpark|retiro|arboret",
    re.I,
)


def slugify(name):
    s = name.split("(")[0].strip().lower().replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def corpus():
    species = collections.Counter()
    countries = collections.Counter()
    parks = collections.Counter()
    for path in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        countries[d.get("country", "")] += len(d.get("trees") or [])
        for t in d.get("trees") or []:
            if t.get("species"):
                species[t["species"]] += 1
            # Mirrors parkKey() in site/src/lib/parks.ts: neighbourhood first,
            # address second, first clause before a comma, parentheticals
            # stripped. A mismatch here reports a gap the site has already
            # closed (Padua's Orto Botanico, 2026-08-15: neighbourhood said
            # "Orto Botanico", this loop's old address-only check wanted
            # "Orto Botanico di Padova", and the site had already built and
            # published the page under the neighbourhood-derived name).
            loc = t.get("location") or {}
            park_name = None
            for field in (loc.get("neighbourhood"), loc.get("address")):
                head = (field or "").split(",")[0]
                head = re.sub(r"\([^)]*\)?", "", head)
                head = re.sub(r"\s+", " ", head).strip(" -/")
                if len(head) >= 4 and PARKISH.search(head):
                    park_name = head
                    break
            if park_name:
                parks[(d.get("city"), park_name)] += 1
    return species, countries, parks


def written(kind, key="slug"):
    out = set()
    for path in glob.glob(os.path.join(ROOT, "data", kind, "*.json")):
        try:
            with open(path, encoding="utf-8") as fh:
                d = json.load(fh)
        except (OSError, ValueError):
            continue
        out.add(d.get(key) or os.path.basename(path)[:-5])
    return out


def written_parks():
    """Parks are matched by (city_slug, park name), which is what
    site/src/pages/parks/[slug].astro actually keys on. The first version of
    this script guessed a slug instead and reported York Museum Gardens and the
    Giardini Montanelli as missing while both pages were live; a writing pass
    caught it and refused to create the duplicates. Match on the key the site
    uses, never on a name you reconstruct."""
    out = set()
    for path in glob.glob(os.path.join(ROOT, "data", "parks", "*.json")):
        try:
            with open(path, encoding="utf-8") as fh:
                d = json.load(fh)
        except (OSError, ValueError):
            continue
        if d.get("city_slug") and d.get("park"):
            out.add((d["city_slug"], d["park"].strip().lower()))
    return out


def gaps():
    species, countries, parks = corpus()
    have_sp = written("species")
    have_co = written("countries", "slug")
    have_pk = written_parks()
    sp = [(n, s) for s, n in species.items()
          if n >= SPECIES_MIN_TREES and slugify(s) not in have_sp]
    cities_per = collections.Counter()
    for path in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        if d.get("trees"):
            cities_per[d.get("country", "")] += 1
    co = [(n, c) for c, n in countries.items()
          if c and n > 0 and slugify(c) not in have_co
          and cities_per[c] >= COUNTRY_MIN_CITIES]
    pk = [(n, city, park) for (city, park), n in parks.items()
          if n >= PARK_MIN_TREES and (slugify(city), park.strip().lower()) not in have_pk]
    sp.sort(reverse=True)
    co.sort(reverse=True)
    pk.sort(reverse=True)
    return sp, co, pk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--next", type=int, metavar="N",
                    help="print the N biggest gaps as a batch to brief")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if any country with trees, or any species with 8+, has no page")
    a = ap.parse_args()
    sp, co, pk = gaps()

    if a.check:
        bad = [c for n, c in co] + [s for n, s in sp if n >= 8] + [f"{c}: {p}" for n, c, p in pk]
        if bad:
            print("%d page(s) the data has earned and nobody has written: %s"
                  % (len(bad), ", ".join(str(b) for b in bad[:8])))
            return 1
        print("no page gaps")
        return 0

    if a.next:
        rows = ([("species", n, s) for n, s in sp] + [("country", n, c) for n, c in co]
                + [("park", n, f"{c}: {p}") for n, c, p in pk])
        rows.sort(key=lambda r: -r[1])
        print("The %d biggest gaps, most trees first. Each needs one intro file.\n" % a.next)
        for kind, n, name in rows[:a.next]:
            print("  %-8s %3d trees  %s" % (kind, n, name))
        return 0

    print("\nPAGES THE DATA HAS EARNED AND NOBODY WROTE\n")
    print("  species  %3d missing (%d trees behind them), threshold %d trees"
          % (len(sp), sum(n for n, _ in sp), SPECIES_MIN_TREES))
    print("  country  %3d missing (%d trees behind them)" % (len(co), sum(n for n, _ in co)))
    print("  park     %3d missing (%d trees behind them), threshold %d trees"
          % (len(pk), sum(n for n, _, _ in pk), PARK_MIN_TREES))
    for label, rows in (("species", [(n, s) for n, s in sp[:10]]),
                        ("country", [(n, c) for n, c in co[:10]])):
        if rows:
            print("\n  biggest %s gaps:" % label)
            for n, name in rows:
                print("    %3d  %s" % (n, name))
    if pk:
        print("\n  parks over the threshold with no page:")
        for n, city, park in pk[:10]:
            print("    %3d  %s: %s" % (n, city, park))
    return 0


if __name__ == "__main__":
    sys.exit(main())
