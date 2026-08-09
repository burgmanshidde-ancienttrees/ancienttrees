#!/usr/bin/env python3
"""Harvest individually-notable trees from Wikidata around every published city.

The reflection of 2026-08-09 (30 passes in two days) found the same bottleneck
in nearly every report: discovery is cheap, the second source is expensive.
Wikidata is the one source that is CC0 (importable without any licence
question), machine-queryable, and often carries exactly what a verify pass
spends its window hunting: coordinates, a species statement, a Commons image,
and sitelinks to the Wikipedia articles that ARE second sources.

This script is retrieval, so it is code, not an agent (the measured doctrine:
scouting compounds, agents judge). One SPARQL query per city, throttled,
against query.wikidata.org, radius 15 km, deduped against our own published
trees (within 80 m = probably already ours, same threshold passcheck uses).

Output: data/research/wikidata-candidates.json, grouped per city slug, each
candidate with QID, label, coords, distance, image (P18) if any, sitelink
count, and the heritage designation (P1435) if any. A verify pass reads its
city's block instead of searching the web from zero; the sitelinked articles
are where its second sources live.

Run: python3 scripts/wikidata_harvest.py [slug ...]   (no args = all cities)
"""
import glob
import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "research", "wikidata-candidates.json")
ENDPOINT = "https://query.wikidata.org/sparql"
UA = "AncientTreesHarvester/1.0 (ancienttrees.app; research; contact via site form)"
RADIUS_KM = 15
NEAR_OURS_M = 80

QUERY = """
SELECT ?tree ?treeLabel ?coord ?image ?designation ?designationLabel ?sitelinks WHERE {
  SERVICE wikibase:around {
    ?tree wdt:P625 ?coord .
    bd:serviceParam wikibase:center "Point(%(lng)f %(lat)f)"^^geo:wktLiteral .
    bd:serviceParam wikibase:radius "%(radius)d" .
  }
  ?tree wdt:P31 ?cls .
  VALUES ?cls { wd:Q10884 wd:Q811534 wd:Q193472 }
  OPTIONAL { ?tree wdt:P18 ?image . }
  OPTIONAL { ?tree wdt:P1435 ?designation . }
  ?tree wikibase:sitelinks ?sitelinks .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,nl,de,fr,es,it,da,pt". }
}
LIMIT 300
"""


def haversine_m(a, b):
    R = 6371000.0
    p = math.pi / 180
    x = (math.sin((b[0] - a[0]) * p / 2) ** 2
         + math.cos(a[0] * p) * math.cos(b[0] * p)
         * math.sin((b[1] - a[1]) * p / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(x))


def parse_point(wkt):
    # "Point(lng lat)"
    try:
        lng, lat = wkt.strip()[6:-1].split()
        return float(lat), float(lng)
    except Exception:
        return None


def query_city(lat, lng):
    q = QUERY % {"lat": lat, "lng": lng, "radius": RADIUS_KM}
    url = ENDPOINT + "?" + urllib.parse.urlencode({"query": q, "format": "json"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["results"]["bindings"]


def main():
    only = {s.lower() for s in sys.argv[1:]}
    try:
        out = json.load(open(OUT))
    except Exception:
        out = {"note": "Wikidata (CC0) individual-tree candidates per city, "
                       "harvested by scripts/wikidata_harvest.py. Discovery "
                       "and corroboration feed for verify passes; sitelinked "
                       "Wikipedia articles are where second sources live.",
               "cities": {}}
    total_new = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "data/cities/*.json"))):
        slug = os.path.basename(path)[:-5]
        if only and slug not in only:
            continue
        d = json.load(open(path))
        pts = [(t["location"]["latitude"], t["location"]["longitude"])
               for t in d.get("trees", []) if t.get("location", {}).get("latitude")]
        if not pts:
            continue
        clat = sum(p[0] for p in pts) / len(pts)
        clng = sum(p[1] for p in pts) / len(pts)
        rows = None
        for attempt in (1, 2):
            try:
                rows = query_city(clat, clng)
                break
            except Exception as e:
                if attempt == 1 and "429" in str(e):
                    time.sleep(30)
                    continue
                print(f"  {slug}: query failed ({e}); skipping")
        if rows is None:
            continue
        cands = []
        for r in rows:
            coord = parse_point(r["coord"]["value"])
            if not coord:
                continue
            dist_own = min((haversine_m(coord, p) for p in pts), default=1e9)
            cands.append({
                "qid": r["tree"]["value"].rsplit("/", 1)[-1],
                "label": r.get("treeLabel", {}).get("value", ""),
                "latitude": coord[0], "longitude": coord[1],
                "image": r.get("image", {}).get("value"),
                "designation": r.get("designationLabel", {}).get("value"),
                "sitelinks": int(r.get("sitelinks", {}).get("value", 0)),
                "near_published_m": round(dist_own) if dist_own < 1e9 else None,
                "probably_ours": dist_own <= NEAR_OURS_M,
            })
        cands.sort(key=lambda c: (-c["sitelinks"], c.get("near_published_m") or 0))
        fresh = [c for c in cands if not c["probably_ours"]]
        out["cities"][slug] = {"harvested": time.strftime("%Y-%m-%d"),
                               "candidates": cands}
        total_new += len(fresh)
        print(f"  {slug}: {len(cands)} tree items, {len(fresh)} not already ours"
              f" ({sum(1 for c in fresh if c['image'])} with an image)")
        time.sleep(5)  # WDQS etiquette
    json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
    print(f"\n{total_new} new candidates written to {OUT}")


if __name__ == "__main__":
    main()
