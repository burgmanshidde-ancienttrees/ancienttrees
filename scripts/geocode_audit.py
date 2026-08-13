"""
One-off audit: geocode every tree's own stored address via Nominatim and flag
any stored coordinate that sits implausibly far from what the address itself
resolves to. Not a build step, not run automatically; a research aid for a
single pass. Stdlib only (urllib), respects Nominatim's 1 req/sec usage policy.
"""
import json
import glob
import os
import sys
import time
import urllib.request
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import km  # noqa: E402

UA = "AncientTreesResearch/1.0 (https://ancienttrees.app; research contact via repo)"


def geocode(query):
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
        {"q": query, "format": "json", "limit": 1}
    )
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=15).read())
    except Exception as e:
        return None, str(e)
    if not data:
        return None, "no result"
    return (float(data[0]["lat"]), float(data[0]["lon"])), data[0].get("display_name")


def haversine_m(lat1, lon1, lat2, lon2):
    return km((lat1, lon1), (lat2, lon2)) * 1000


results = []
files = sorted(glob.glob("data/cities/*.json"))
for fi, f in enumerate(files):
    d = json.load(open(f))
    city = d["city"]
    for t in d["trees"]:
        addr = t["location"]["address"]
        lat = t["location"]["latitude"]
        lon = t["location"]["longitude"]
        query = f"{addr}"
        geo, info = geocode(query)
        if geo:
            dist = haversine_m(lat, lon, geo[0], geo[1])
            results.append((dist, city, t["id"], t["name"], addr, (lat, lon), geo, info))
            flag = "  <<<< FAR" if dist > 800 else ""
            print(f"{dist:8.0f}m  {city:12s} {t['id']:8s} {t['name'][:40]:40s}{flag}")
        else:
            print(f"     ---  {city:12s} {t['id']:8s} {t['name'][:40]:40s}  ({info})")
        time.sleep(1.1)

OUT_JSON = "geocode_audit_output.json"
json.dump(
    [
        {
            "dist_m": r[0],
            "city": r[1],
            "id": r[2],
            "name": r[3],
            "address": r[4],
            "stored": r[5],
            "geocoded": r[6],
            "geocoded_display": r[7],
        }
        for r in results
    ],
    open(OUT_JSON, "w"),
    indent=2,
)
print(f"\nDone. Full results in {OUT_JSON}")
far = [r for r in results if r[0] > 800]
far.sort(key=lambda r: -r[0])
print(f"\n{len(far)} entries over 800m from their own address's geocode:")
for r in far:
    print(f"  {r[0]:8.0f}m  {r[1]:12s} {r[2]:8s} {r[3]}")
