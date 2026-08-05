#!/usr/bin/env python3
"""What is online, and which register clusters are worth doing next.

Two things this fixes about the way the queue was being read by hand.

**It matches on position, not on names.** A register says Napoli and Firenze
where our city files say Naples and Florence, and matching those by string sent
two research passes out to "open" cities that had been live for weeks. Distance
cannot be fooled by a language: a cluster belongs to a city we already publish
if it sits within reach of the trees we publish there.

**It separates cheap from wanted.** The cheapest clusters in the register are
villages with a lot of designated trees and no search traffic. Priverno has 46.
Nobody is looking for Priverno. So every cluster carries a second mark saying
whether it is somewhere people actually travel, and the queue sorts on that
first. That list is hand-made and says so: we have no per-city search volume,
only Search Console for pages that already exist.

    python3 scripts/backlog.py            the whole picture
    python3 scripts/backlog.py --new      only places we do not publish yet
"""
import argparse
import glob
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cluster_register import load, cluster, km  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Within this many km of a city's own trees, a cluster is that city, whatever
# either of them is called. Generous on purpose: the day-trip boundary in
# CLAUDE.md already puts Blarney on Cork's page.
SAME_CITY_KM = 20.0

# Hand-made, and that is the honest label. These are the places in our register
# countries that people travel to, so a page there gets read. No search volume
# was measured; when Search Console has enough history this list should be
# replaced by it rather than extended.
TOURIST = {
    # Italy
    "roma", "firenze", "venezia", "milano", "napoli", "torino", "bologna",
    "verona", "siena", "pisa", "lucca", "palermo", "catania", "genova",
    "padova", "ravenna", "bergamo", "como", "assisi", "perugia", "trieste",
    "lecce", "matera", "rimini", "ferrara", "mantova", "parma", "modena",
    "cagliari", "siracusa", "taormina", "sorrento", "amalfi", "positano",
    "bolzano", "trento", "urbino", "orvieto", "viterbo", "caserta", "tivoli",
    # Portugal
    "lisboa", "porto", "sintra", "coimbra", "braga", "guimaraes", "guimarães",
    "evora", "évora", "faro", "lagos", "aveiro", "cascais", "obidos", "óbidos",
    "tomar", "batalha", "nazare", "nazaré", "viana do castelo", "funchal",
    # Spain (the Andalusian register files by province, so these double as both)
    "sevilla", "granada", "malaga", "málaga", "cordoba", "córdoba", "cadiz",
    "cádiz", "barcelona", "madrid", "valencia", "jaen", "jaén", "huelva",
    "ronda", "marbella", "almeria", "almería",
}


def published_cities():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        d = json.load(open(f))
        trees = d.get("trees") or []
        if not trees:
            continue
        out.append({
            "city": d["city"],
            "country": d.get("country", ""),
            "slug": os.path.basename(f)[:-5],
            "n": len(trees),
            "photos": sum(1 for t in trees if (t.get("photo") or {}).get("url")),
            "lat": sum(t["location"]["latitude"] for t in trees) / len(trees),
            "lng": sum(t["location"]["longitude"] for t in trees) / len(trees),
        })
    return out


def nearest_published(lat, lng, cities):
    best, best_d = None, 1e9
    for c in cities:
        d = km((lat, lng), (c["lat"], c["lng"]))
        if d < best_d:
            best, best_d = c, d
    return best, best_d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--new", action="store_true", help="only places we do not publish yet")
    ap.add_argument("--radius", type=float, default=2.0)
    ap.add_argument("--limit", type=int, default=30)
    args = ap.parse_args()

    cities = published_cities()
    by_country = {}
    for c in cities:
        by_country.setdefault(c["country"], []).append(c)
    print(f"ONLINE: {len(cities)} places, {sum(c['n'] for c in cities)} trees, "
          f"{sum(c['photos'] for c in cities)} with a photo")
    for country, rows in sorted(by_country.items(), key=lambda kv: -len(kv[1]))[:10]:
        print(f"   {len(rows):3} {country:<18} {sum(r['n'] for r in rows):4} trees, "
              f"{sum(r['photos'] for r in rows):3} photos")

    rows = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "registers", "*.json"))):
        pts, _ = load(path)
        if not pts:
            continue
        country = json.load(open(path)).get("country", "")
        for g in cluster(pts, args.radius):
            if len(g) < 4:
                continue
            lat = sum(pts[i]["lat"] for i in g) / len(g)
            lng = sum(pts[i]["lng"] for i in g) / len(g)
            spread = max(km((pts[i]["lat"], pts[i]["lng"]), (pts[j]["lat"], pts[j]["lng"]))
                         for i in g for j in g)
            places = sorted({pts[i]["place"] for i in g if pts[i]["place"]})
            near, dist = nearest_published(lat, lng, cities)
            live = near if dist <= SAME_CITY_KM else None
            rows.append({
                "n": len(g), "spread": spread, "country": country,
                "place": places[0] if places else f"{lat:.3f},{lng:.3f}",
                "tourist": any(p.lower() in TOURIST for p in places),
                "live": live, "dist": dist,
            })

    def key(r):
        # wanted first, then dense, then tight
        return (not r["tourist"], -r["n"], r["spread"])

    fresh = [r for r in rows if not r["live"]]
    deepen = [r for r in rows if r["live"]]
    print(f"\nREGISTER CLUSTERS of 4+: {len(rows)} total, {len(fresh)} in places we do not "
          f"publish, {len(deepen)} sitting on top of a page we already have")

    print("\nNEW PAGES, best first (t = a place people travel to)")
    print(f"  {'n':>3} {'across':>7}  t  {'country':<9} place")
    for r in sorted(fresh, key=key)[:args.limit]:
        print(f"  {r['n']:3} {r['spread']:6.1f}km  {'t' if r['tourist'] else ' '}  "
              f"{r['country']:<9} {r['place']}")

    if not args.new:
        print("\nDEEPEN WHAT IS LIVE, biggest gap first (register trees vs published)")
        seen = {}
        for r in deepen:
            s = r["live"]["slug"]
            seen[s] = seen.get(s, {"live": r["live"], "reg": 0})
            seen[s]["reg"] += r["n"]
        for s, v in sorted(seen.items(), key=lambda kv: -(kv[1]["reg"] - kv[1]["live"]["n"]))[:15]:
            c = v["live"]
            print(f"  {c['city']:<16} publishes {c['n']:3}, register holds {v['reg']:3} nearby "
                  f"({c['photos']} photos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
