#!/usr/bin/env python3
"""Which famous-tree leads are worth a verify pass, and which we already map.

Written 2026-09-01 after the same waste happened twice in one afternoon. A
verify pass on 19 Japanese candidates came back with 9 new trees, because 5
were already published under a different id (the Tsurugaoka ginkgo, the
Kencho-ji juniper, the Nagoya Castle kaya, the Dogata chinquapins, the
Kenrokuen raised-root pine). The same hour, a US pass delivered 10 trees of
which every single one was already live, General Sherman included.

Neither pass did anything wrong. The BRIEF was wrong, both times, because
data/leads/_famous-*.json carries no marker for what we already map and
whoever writes the brief is left to remember. passcheck.py catches it, but it
catches it AFTER the tokens are spent.

So this asks the question before the brief exists: of the famous-tree leads,
which are NOT already published, and which city would they land on. It ranks
by that city's queue rank, because a tree added to a city at rank 6 is worth
more than one added at rank 367, and it prints the candidates in the shape a
brief needs.

Distance, never names: CLAUDE.md's own rule, learned when register place names
were matched against our city names and three passes were briefed on cities
that had been live for weeks.

Usage:
  python3 scripts/famous_map.py                  # every country, best cities first
  python3 scripts/famous_map.py --country japan
  python3 scripts/famous_map.py --city Tenerife  # the brief for one city
"""
import argparse
import collections
import glob
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEADS = os.path.join(ROOT, "data", "leads")
CITIES = os.path.join(ROOT, "data", "cities")
QUEUE = os.path.join(ROOT, "data", "city-queue.json")
COORDS = os.path.join(ROOT, "data", "city-coords.json")

NEAR_CITY_KM = 30.0   # the day-trip boundary this project already publishes on
SAME_TREE_M = 60.0    # generous: two names for one trunk sat 36 m apart


def km(a_lat, a_lng, b_lat, b_lng):
    r = 6371.0
    p1, p2 = math.radians(a_lat), math.radians(b_lat)
    dp = math.radians(b_lat - a_lat)
    dl = math.radians(b_lng - a_lng)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def published():
    """Every live tree as (lat, lng, city, id, name)."""
    out = []
    for f in glob.glob(os.path.join(CITIES, "*.json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except (ValueError, OSError):
            continue
        for t in d.get("trees", []):
            loc = t.get("location") or {}
            if loc.get("latitude") is None:
                continue
            out.append((loc["latitude"], loc["longitude"], d.get("city"),
                        t.get("id"), t.get("name")))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--country")
    ap.add_argument("--city")
    ap.add_argument("--max-rank", type=int, default=None,
                    help="only cities ranked at or above this number")
    args = ap.parse_args()

    live = published()
    coords = json.load(open(COORDS, encoding="utf-8"))
    q = json.load(open(QUEUE, encoding="utf-8"))
    info = {c["city"]: (c.get("rank"), c.get("trees") or 0, c.get("target") or 0)
            for c in q["cities"]}

    pat = "_famous-%s.json" % args.country if args.country else "_famous-*.json"
    per_city = collections.defaultdict(list)
    seen = mapped = nopin = 0
    for f in sorted(glob.glob(os.path.join(LEADS, pat))):
        country = os.path.basename(f)[8:-5]
        try:
            doc = json.load(open(f, encoding="utf-8"))
        except (ValueError, OSError):
            continue
        for e in (doc.get("leads") or []):
            if not isinstance(e, dict):
                continue
            seen += 1
            if e.get("lat") is None:
                nopin += 1
                continue
            # Already ours? Distance decides, and a name never does.
            twin = min((km(e["lat"], e["lng"], p[0], p[1]), p) for p in live)
            if twin[0] * 1000 <= SAME_TREE_M:
                mapped += 1
                continue
            best = min((km(e["lat"], e["lng"], c[0], c[1]), n)
                       for n, c in coords.items() if c and c[0] is not None)
            if best[0] <= NEAR_CITY_KM:
                per_city[best[1]].append((round(best[0], 1), e.get("name"),
                                          e.get("species"), e["lat"], e["lng"], country))

    def rank_of(city):
        r = info.get(city, (None,))[0]
        return r if r else 9999

    cities = sorted(per_city, key=rank_of)
    if args.city:
        cities = [c for c in cities if c.lower() == args.city.lower()]
    if args.max_rank:
        cities = [c for c in cities if rank_of(c) <= args.max_rank]

    print("%d famous-tree leads read: %d already published (skipped), %d carry no pin."
          % (seen, mapped, nopin))
    print("Below: leads near a city we rank, NOT already mapped, best-ranked city first.\n")
    total = 0
    for c in cities:
        r, tr, tg = info.get(c, (None, 0, 0))
        rows = sorted(per_city[c])
        total += len(rows)
        print("## %s   rank %s, %d of %d trees   (%d candidate%s)"
              % (c, r, tr, tg, len(rows), "" if len(rows) == 1 else "s"))
        for d, n, sp, la, lo, country in rows:
            print("   %5.1f km | %-44s | %-26s | %.5f,%.5f | %s"
                  % (d, (n or "?")[:44], (sp or "?")[:26], la, lo, country))
        print()
    print("%d candidate(s) across %d cit%s."
          % (total, len(cities), "y" if len(cities) == 1 else "ies"))
    print("A pass under six candidates costs more per tree than it returns; batch "
          "neighbouring cities or one language area.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
