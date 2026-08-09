#!/usr/bin/env python3
"""Which places people actually care about, measured instead of guessed.

Hidde, 2026-08-09, on being shown a queue that ranked Bucaco near the top:
"ik heb zelf nog nooit van bucaco gehoord". He is right, and it exposes the
flaw in every ranking this project has used so far. backlog.py ranks by how
many register trees sit close together, which is SUPPLY. The hand-made
tourist list in that script is DEMAND, guessed, by one person, and CLAUDE.md
already says it should be replaced rather than extended by hand forever.

This measures demand instead. The proxy is English Wikipedia pageviews for
the place's own article over the last 90 days, which is free, official, has
no key, no account and no cost, and answers almost exactly the right
question: how many English-speaking people are looking this place up. Our
own audience is 72% mobile and overwhelmingly US/UK/CA, so English pageviews
are a closer proxy for our traffic than any tourist-arrivals table.

What it is NOT. It is not search volume, and a place can be famous without
anyone searching for its trees. It is a relative ranking, not a forecast.
Read it as "which of these places is in more people's heads", which is the
question that a supply-only ranking cannot answer at all.

The output crosses demand with what we already have, because the interesting
cell is not the biggest number in either column. It is a place with high
demand where we publish little, or where a register is sitting unused.

Usage:
  python3 scripts/demand.py                 # published cities, ranked
  python3 scripts/demand.py Cascais Coimbra Braga Evora   # candidates too
"""
import datetime
import glob
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = "AncientTrees/1.0 (https://ancienttrees.app; tree mapping project)"
API = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
       "en.wikipedia/all-access/user/%s/monthly/%s/%s")
CACHE = "data/demand-cache.json"

# Where the article title is not the city name we publish under. Kept small
# and explicit: a wrong title returns 404 and would read as "no demand",
# which is the one failure mode that would quietly mislead the queue.
TITLES = {
    "Bucaco": "Bussaco",
    "Den Bosch": "'s-Hertogenbosch",
    "Washington DC": "Washington,_D.C.",
    "New York": "New_York_City",
    "Cordoba": "Córdoba,_Spain",
    "Malaga": "Málaga",
    "Setubal": "Setúbal",
    "Guimaraes": "Guimarães",
    "Krakow": "Kraków",
    "Gothenburg": "Gothenburg",
    "The Hague": "The_Hague",
    # These resolve to a disambiguation page, a common noun or the wrong
    # subject, and a wrong title returns few views, which the ranking would
    # read as "nobody cares about this place". Every one of these was found
    # by disbelieving a low number, which is the check to keep doing.
    "Bath": "Bath,_Somerset",
    "Split": "Split,_Croatia",
    "Cork": "Cork_(city)",
    "Nara": "Nara,_Nara",
    "Cadiz": "Cádiz",
    "Reykjavik": "Reykjavík",
    "Evora": "Évora",
    "Faro": "Faro,_Portugal",
    "Aveiro": "Aveiro,_Portugal",
    "Valencia": "Valencia",
    "Granada": "Granada",
    "Bologna": "Bologna",
    "Genoa": "Genoa",
    "Padua": "Padua",
    "Lucca": "Lucca",
    "Turin": "Turin",
}


def load_cache():
    try:
        return json.load(open(CACHE))
    except Exception:
        return {}


def views(place, cache, today):
    """90-day English Wikipedia pageviews, cached by month so a rerun is free."""
    title = TITLES.get(place, place.replace(" ", "_"))
    start = (today - datetime.timedelta(days=95)).strftime("%Y%m01")
    end = today.strftime("%Y%m01")
    key = "%s|%s|%s" % (title, start, end)
    if key in cache:
        return cache[key]
    url = API % (urllib.parse.quote(title, safe=""), start, end)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            items = json.load(r).get("items", [])
        total = sum(i.get("views", 0) for i in items)
    except urllib.error.HTTPError as e:
        total = None if e.code == 404 else 0
    except Exception:
        total = 0
    cache[key] = total
    return total


def published():
    out = {}
    for p in sorted(glob.glob("data/cities/*.json")):
        d = json.load(open(p))
        photos = sum(1 for t in d.get("trees", [])
                     if (t.get("photo") or {}).get("status") == "approved")
        out[d["city"]] = {"trees": len(d.get("trees", [])), "photos": photos,
                          "country": d.get("country", "")}
    return out


def main():
    today = datetime.datetime.now(datetime.timezone.utc).date()
    cache = load_cache()
    have = published()
    extra = [a for a in sys.argv[1:] if not a.startswith("-")]
    places = list(have) + [p for p in extra if p not in have]

    rows = []
    for place in places:
        v = views(place, cache, today)
        h = have.get(place)
        rows.append({"place": place, "views": v,
                     "trees": h["trees"] if h else 0,
                     "photos": h["photos"] if h else 0,
                     "country": h["country"] if h else "",
                     "live": h is not None})
    os.makedirs("data", exist_ok=True)
    json.dump(cache, open(CACHE, "w"), indent=0)

    missing = [r["place"] for r in rows if r["views"] is None]
    rows = [r for r in rows if r["views"]]
    rows.sort(key=lambda r: -r["views"])

    print("DEMAND: English Wikipedia pageviews, last 3 full months")
    print("A relative ranking of how many English speakers look a place up.")
    print("Not search volume, and never proof anyone wants its trees.\n")
    print("%-24s %10s %6s %7s %8s  %s" % ("place", "views", "trees", "photos", "views/tree", ""))
    for r in rows:
        per = (r["views"] / r["trees"]) if r["trees"] else 0
        flag = "" if r["live"] else "  <- not published"
        print("%-24s %10d %6d %7d %8s%s" % (
            r["place"], r["views"], r["trees"], r["photos"],
            ("%d" % per) if per else "-", flag))
    if missing:
        print("\nNo English Wikipedia article found (check the title, do not read as zero):")
        print("  " + ", ".join(missing))

    live = [r for r in rows if r["live"] and r["trees"]]
    if live:
        print("\nWHERE ATTENTION IS UNDERSERVED (most looked up per tree we publish):")
        for r in sorted(live, key=lambda r: -(r["views"] / r["trees"]))[:12]:
            print("  %-22s %8d views, %2d trees, %2d photos" % (
                r["place"], r["views"], r["trees"], r["photos"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
