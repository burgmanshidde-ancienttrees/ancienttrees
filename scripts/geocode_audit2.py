"""
Follow-up to geocode_audit.py: for trees whose full address didn't geocode
at all (a "no result" in the first pass), try a lighter landmark-style query
(tree name + city) instead. Flags anything that resolves confidently AND far
from the stored pin, for manual review, not automatic correction.
Stdlib only, one Nominatim request per second.
"""
import json
import glob
import time
import urllib.request
import urllib.parse
import math
import re

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
    return (float(data[0]["lat"]), float(data[0]["lon"])), data[0].get("display_name"), data[0].get("importance", 0)


def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def clean_name(name):
    name = re.sub(r"^The\s+", "", name)
    name = re.sub(r"\s*\(.*?\)", "", name)
    return name


results = []
files = sorted(glob.glob("data/cities/*.json"))
for f in files:
    d = json.load(open(f))
    city = d["city"]
    for t in d["trees"]:
        addr = t["location"]["address"]
        lat = t["location"]["latitude"]
        lon = t["location"]["longitude"]
        # First pass already resolved this one; skip (cheap re-check not needed).
        first = geocode(addr)
        time.sleep(1.1)
        if first[0] is not None:
            continue
        query = f"{clean_name(t['name'])}, {city}"
        geo = geocode(query)
        time.sleep(1.1)
        if geo[0]:
            dist = haversine_m(lat, lon, geo[0][0], geo[0][1])
            importance = geo[2] if len(geo) > 2 else 0
            flag = "  <<<< FAR" if dist > 800 else ""
            print(f"{dist:8.0f}m  imp={importance:.3f}  {city:12s} {t['id']:8s} {t['name'][:40]:40s}{flag}")
            results.append(
                {
                    "dist_m": dist,
                    "importance": importance,
                    "city": city,
                    "id": t["id"],
                    "name": t["name"],
                    "query": query,
                    "stored": [lat, lon],
                    "geocoded": geo[0],
                    "geocoded_display": geo[1],
                }
            )
        else:
            print(f"     ---  {city:12s} {t['id']:8s} {t['name'][:40]:40s}  (name query: {geo[1]})")

json.dump(results, open("geocode_audit2_output.json", "w"), indent=2)
print(f"\nDone. {len(results)} name-based matches found; full results in geocode_audit2_output.json")
far = sorted([r for r in results if r["dist_m"] > 800], key=lambda r: -r["dist_m"])
print(f"\n{len(far)} over 800m (needs manual verification before any fix):")
for r in far:
    print(f"  {r['dist_m']:8.0f}m  imp={r['importance']:.3f}  {r['city']:12s} {r['id']:8s} {r['name']}")
