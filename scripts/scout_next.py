#!/usr/bin/env python3
"""What to scout next, in the queue's order rather than the data's.

Why this exists. On 2026-08-16 a scouting round imported Estonia and Lithuania,
which serve Tallinn (#65) and Vilnius (#22), while Toronto (#8), Montreal (#10)
and Sydney (#14) sat untouched. Nothing was wrong with either import; the order
was wrong, and it was wrong for a reason worth naming: the round picked its
targets from `wikidata_trees.py --designations`, which ranks countries by how
many trees they have. That is a supply ranking. The queue ranks by demand times
our own realised yield, which is the ranking that decides whether anybody ever
reads the page.

So this script joins the two: it walks the queue from rank 1, keeps the cities
that still need trees, and prints what is known about the register behind each
from `data/register-scouting.json`. A city with status `unscouted` at rank 8
outranks a country with a thousand trees at rank 200, every time.

The ledger is deliberately not automatic. A verdict like "blocked on licence" or
"the state publishes nothing but volunteers have" is a judgement someone made
after reading a licence, and it belongs in a file a human can correct.

Usage:
    python3 scripts/scout_next.py            top of the queue, needs-work only
    python3 scripts/scout_next.py --all      including places already served
    python3 scripts/scout_next.py --limit 40
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "data", "register-scouting.json")
QUEUE = os.path.join(ROOT, "data", "city-queue.json")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

# A country-level verdict answers for its cities; a city-level one wins over it.
ORDER = ["unscouted", "stalled", "empty", "blocked", "imported"]


def ledger():
    with open(LEDGER, encoding="utf-8") as fh:
        d = json.load(fh)
    by_place, by_country = {}, {}
    for r in d["places"]:
        by_place[r["place"].lower()] = r
        # A region entry answers for the cities it names in "covers", and for
        # nothing else. Saxony must not answer for Berlin, and the first version
        # of this script let Frankfurt read as unscouted while the Hessen verdict
        # sat one row away.
        for city in r.get("covers", []):
            by_place.setdefault(city.lower(), r)
        # Only a whole-country entry generalises to its country.
        if r["place"] == r["country"]:
            by_country[r["country"].lower()] = r
    return by_place, by_country


def wikidata_counts():
    """Trees within 15 km per city, from the free Wikidata layer. This is the
    alternative route when a state publishes nothing, so it belongs on the same
    line as the scouting verdict rather than in a separate report."""
    try:
        import city_queue as Q
        import wikidata_trees as W
        trees = W.load()["trees"]
    except Exception:
        return {}

    def count(city, article):
        pos = Q.city_coords(city, article)
        return len(W.near(trees, pos[0], pos[1], 15.0)) if pos else None
    return count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=25)
    ap.add_argument("--all", action="store_true",
                    help="include cities already at or above target")
    a = ap.parse_args()

    by_place, by_country = ledger()
    wd = wikidata_counts()
    with open(QUEUE, encoding="utf-8") as fh:
        cities = json.load(fh)["cities"]

    rows = []
    for c in sorted([c for c in cities if c.get("rank")], key=lambda c: c["rank"]):
        if not a.all and c.get("trees", 0) >= 10:
            continue
        hit = (by_place.get(c["city"].lower())
               or by_country.get((c.get("country") or "").lower()))
        rows.append((c, hit))
        if len(rows) >= a.limit:
            break

    print("Scouting worklist, queue order. 'unscouted' at the top is the whole "
          "point:\na city nobody has checked at rank 8 beats a thousand trees "
          "at rank 200.\n")
    print("%4s  %-20s %5s %5s %5s  %-10s %s"
          % ("#", "city", "trees", "reg", "wd", "scouting", "what is known"))
    for c, hit in rows:
        status = hit["status"] if hit else "unscouted"
        note = (hit["note"] if hit else "no entry in the ledger")
        n = wd(c["city"], c.get("article")) if wd else None
        print("%4d  %-20s %5d %5d %5s  %-10s %s"
              % (c["rank"], c["city"][:20], c.get("trees", 0),
                 c.get("register", 0), "-" if n is None else n,
                 status, note[:96]))

    todo = [r for r in rows if not r[1] or r[1]["status"] in ("unscouted", "stalled")]
    print("\n%d of the top %d still have a register question open."
          % (len(todo), len(rows)))
    if todo:
        c, hit = todo[0]
        print("Start here: %s (#%d), %s."
              % (c["city"], c["rank"], hit["status"] if hit else "unscouted"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
