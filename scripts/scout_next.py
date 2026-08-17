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


def out_of_focus():
    """Countries Hidde has ruled out of scope. A SCOPE decision, not a
    judgement about the trees: the queue still ranks these cities and nothing
    published is removed, but no scouting window is spent on them and --target
    never points there. 2026-08-16: "israel africa india and russia ar out of
    focus". Reversing it means deleting a line in the ledger."""
    with open(LEDGER, encoding="utf-8") as fh:
        d = json.load(fh)
    o = d.get("out_of_focus") or {}
    return {c.lower() for c in
            (o.get("countries", []) + o.get("africa_countries", []))}


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


def judged_count(slug):
    """How many register candidates near this city an earlier pass already ruled on.

    `register` counts what sits within reach; it says nothing about whether the
    trees are usable. Bratislava is the case that forced this: 26 register trees
    in hand, so --target named it BUILD three times in one day, while the leads
    file already recorded that its remaining candidates are private gardens and
    courtyards in the register's own wording. A tool that keeps recommending a
    city whose supply is written off is worse than no recommendation, because it
    is confident.

    So supply here means UNJUDGED supply: register trees minus everything a pass
    has already put in leads or blocked. Deliberately crude, a count rather than
    a coordinate join, because it only has to rank cities and passcheck does the
    exact matching later.
    """
    path = os.path.join(ROOT, "data", "leads", "%s.json" % (slug or ""))
    try:
        with open(path) as fh:
            doc = json.load(fh)
    except (OSError, ValueError):
        return 0
    if not isinstance(doc, dict):
        return 0
    return len(doc.get("leads") or []) + len(doc.get("blocked") or [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=25)
    ap.add_argument("--all", action="store_true",
                    help="include cities already at or above target")
    ap.add_argument("--target", action="store_true",
                    help="print the single next action: scout X, or build Y")
    a = ap.parse_args()

    by_place, by_country = ledger()
    wd = wikidata_counts()
    with open(QUEUE, encoding="utf-8") as fh:
        cities = json.load(fh)["cities"]

    skip = out_of_focus()
    rows = []
    for c in sorted([c for c in cities if c.get("rank")], key=lambda c: c["rank"]):
        if not a.all and c.get("trees", 0) >= 10:
            continue
        if (c.get("country") or "").lower() in skip:
            continue
        hit = (by_place.get(c["city"].lower())
               or by_country.get((c.get("country") or "").lower()))
        rows.append((c, hit))
        if len(rows) >= a.limit:
            break

    if a.target:
        # Hidde, 2026-08-16: "i want to make use of all usefull registers if it
        # speeds up the data building process", after catching a scout wander
        # into Innsbruck (#194) and Hallstatt (#219) while Sintra (#32) and
        # Bari (#41) had never been looked at.
        #
        # The rule, and the refinement that keeps it from becoming waste: scout
        # the country behind the HIGHEST-RANKED city that has neither supply
        # nor a recorded verdict. Not a nightly sweep, because the ArcGIS and
        # EU sweeps return the same answers most nights and re-running an
        # exhausted hunt is this project's most repeated waste. When every city
        # at the top has either trees in hand or a written reason it has none,
        # there is nothing left to scout and the answer is build.
        #
        # Measured the day this was written: 24 of the top 60 cities below
        # target had no supply, and 14 of those had never been scouted at all.
        for c, hit in rows:
            judged = judged_count(c.get("slug"))
            unjudged = max(0, (c.get("register") or 0) - judged)
            supply = unjudged + (c.get("ready") or 0)
            status = hit["status"] if hit else "unscouted"
            if supply >= 8:
                extra = ("" if not judged else
                         ", %d already judged by an earlier pass" % judged)
                print("BUILD  %s (#%d): %d unjudged register trees and %d ready "
                      "leads already in hand%s. Nothing to scout."
                      % (c["city"], c["rank"], unjudged, c.get("ready") or 0,
                         extra))
                return 0
            if status == "unscouted":
                print("SCOUT  %s (#%d), %s: no supply and no verdict. Scout "
                      "the register behind it before researching from zero."
                      % (c["city"], c["rank"], c.get("country")))
                return 0
            # blocked / empty / stalled all mean somebody already looked and
            # wrote down why. Scouting again buys nothing; the note says what
            # the city actually needs.
        print("BUILD: every city in this window has supply or a written "
              "verdict. Nothing left to scout at the top of the queue.")
        return 0

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
