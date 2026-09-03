#!/usr/bin/env python3
"""Find registers first, then ask which city they serve.

Hidde, 2026-08-16: "is there another way to go at it - just look for available
registers and then see if the register belongs to an interesting city?"

He is right, and it inverts what scouting had been doing. City-first scouting
costs a research pass per city and can end in nothing at all: Los Angeles was
scouted properly and turned out to have no register of any kind, because its
"protected tree" status is a species rule rather than a list. That hour bought
a verdict and no trees.

Register-first is cheap because somebody else already built the catalogue.
Almost every register this project has found lives on ArcGIS: Portland, Sydney,
Brisbane, Melbourne, Hobart, Quebec City, Forests Canada. ArcGIS Online has one
global search API across every public item on it, so one sweep sees them all at
once, and each item carries an extent, which is enough to say which city it is
near without fetching a single row of data.

What this does NOT do, deliberately: decide what to work on. It produces a
supply list. `scripts/scout_next.py` still walks the queue in demand order, and
a big register under a city nobody searches for is still worth less than a small
one under a city they do.

Usage:
    python3 scripts/register_sweep.py                sweep and report
    python3 scripts/register_sweep.py --km 40        wider join radius
    python3 scripts/register_sweep.py --all          include unranked cities
"""
import argparse
import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
OUT = os.path.join(ROOT, "data", "research", "arcgis-register-sweep.json")
SEARCH = "https://www.arcgis.com/sharing/rest/search"
UA = "AncientTrees/1.0 (https://ancienttrees.app; info@ancienttrees.app)"

# The words a government actually uses on a tree register, in the languages
# where ArcGIS is common. Deliberately NOT "tree" alone: that returns street
# inventories by the thousand, which the semantic filter forbids anyway.
TERMS = [
    '"significant tree"', '"significant trees"',
    '"heritage tree"', '"heritage trees"',
    '"remarkable tree"', '"remarkable trees"',
    '"monumental tree"', '"monumental trees"',
    '"notable tree"', '"notable trees"',
    '"veteran tree"', '"champion tree"', '"champion trees"',
    '"exceptional tree"', '"exceptional trees"',
    '"landmark tree"', '"landmark trees"',
    '"protected tree register"', '"tree register"',
    '"arbres remarquables"', '"arbol singular"', '"arboles singulares"',
    '"alberi monumentali"', '"arvores monumentais"', '"bijzondere bomen"',
    '"Naturdenkmal"', '"pomniki przyrody"',
]


def search(term, num=100):
    q = f'{term} AND (type:"Feature Service" OR type:"Map Service")'
    url = SEARCH + "?" + urllib.parse.urlencode(
        {"q": q, "f": "json", "num": num, "sortField": "numviews",
         "sortOrder": "desc"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except Exception as e:
        print("  ! %s: %s" % (term, e), file=sys.stderr)
        return {"results": [], "total": 0}


def centre(item):
    """An ArcGIS extent is [[west, south], [east, north]]. Items with a
    world-sized extent are global layers or defaults and tell us nothing about
    a city, so they are dropped rather than joined to whatever is nearest."""
    e = item.get("extent")
    if not e or len(e) != 2:
        return None
    try:
        (w, s), (x, n) = e
        if None in (w, s, x, n):
            return None
        if abs(x - w) > 20 or abs(n - s) > 20:
            return None
        return ((s + n) / 2.0, (w + x) / 2.0)
    except (TypeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--km", type=float, default=30.0)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--limit", type=int, default=60)
    a = ap.parse_args()

    import city_queue as Q
    queue = json.load(open(os.path.join(ROOT, "data", "city-queue.json"),
                           encoding="utf-8"))["cities"]
    cities = [c for c in queue if a.all or c.get("rank")]

    items, seen = [], set()
    for term in TERMS:
        d = search(term)
        for r in d.get("results", []):
            if r["id"] in seen:
                continue
            seen.add(r["id"])
            r["_term"] = term
            items.append(r)
        time.sleep(0.3)
    print("%d distinct ArcGIS items across %d search terms\n"
          % (len(items), len(TERMS)), file=sys.stderr)

    # City positions once, from the cache the queue already maintains.
    pos = {}
    for c in cities:
        p = Q.city_coords(c["city"], c.get("article"))
        if p:
            pos[c["city"]] = (p, c)

    hits = []
    for it in items:
        ctr = centre(it)
        if not ctr:
            continue
        for city, (p, c) in pos.items():
            dlat = a.km / 111.0
            dlng = a.km / (111.0 * max(math.cos(math.radians(p[0])), 0.1))
            if abs(ctr[0] - p[0]) < dlat and abs(ctr[1] - p[1]) < dlng:
                hits.append({
                    "nearest_city": city, "city": city, "rank": c.get("rank"),
                    "trees_live": c.get("trees", 0),
                    "title": it.get("title"), "owner": it.get("owner"),
                    "id": it["id"], "type": it.get("type"),
                    "url": it.get("url"),
                    # Presence, not content: a licence string here means
                    # somebody wrote one, which is the thing that has blocked
                    # five registers in a row.
                    "has_licence": bool((it.get("licenseInfo") or "").strip()),
                    "licence_excerpt": (it.get("licenseInfo") or "")[:200],
                    "matched_term": it["_term"],
                    # The item's own words about itself, and they are not
                    # decoration: joining by extent puts a NEIGHBOURING
                    # municipality under a big city every time. On the first
                    # run "Arbres_remarquables_OP2016" read as 322 Montreal
                    # trees and its snippet says Otterburn Park, 35 km away,
                    # and "Landmark Trees" read as Los Angeles and belongs to
                    # the City of Pasadena. Both were caught by reading this
                    # field, so it ships with the hit rather than needing a
                    # second lookup.
                    "snippet": (it.get("snippet") or "")[:200],
                    "item_owner_hint": it.get("owner"),
                })
                break

    hits.sort(key=lambda h: (h["rank"] or 9999))
    json.dump({"note": "ArcGIS Online items matching register wording, joined "
                       "to queue cities by item extent. A hit is a LEAD: the "
                       "extent says where, never what is inside or whether we "
                       "may use it.",
               "swept": "2026-08-16", "items_seen": len(items),
               "hits": hits},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("%4s  %-16s %3s  %-36s %-4s %s"
          % ("#", "nearest city", "liv", "register", "lic", "what the item says it is"))
    for h in hits[:a.limit]:
        print("%4s  %-16s %3d  %-36s %-4s %s"
              % (h["rank"] or "-", h["city"][:16], h["trees_live"],
                 (h["title"] or "")[:36], "yes" if h["has_licence"] else "NONE",
                 (h["snippet"] or h["item_owner_hint"] or "")[:46]))
    print("\n%d hits on %d ranked cities -> %s"
          % (len(hits), len({h["city"] for h in hits}),
             os.path.relpath(OUT, ROOT)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
