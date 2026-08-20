#!/usr/bin/env python3
"""The Texas Big Tree Registry, swept once and kept, then read per city.

Why this is a script and not a research pass. On 2026-08-20 a scouting pass
found the registry's backend, looped all 352 species by hand to answer one
question about Houston, kept the 18 Harris County rows and threw the other
several thousand away. The next Texas city would have paid for the same loop
again. Retrieval is code and costs nothing; judgement is what an agent is for,
and "which of these trees is worth the walk" is the only judgement here.

LICENCE, and it decides where the output may live. Texas A&M Forest Service
offers its content "for personal, educational, and other non-commercial
purposes" with a citation requirement
(tfsweb.tamu.edu/accessibility-site-policies-and-public-notices/). A
non-commercial term disqualifies a source for the register layer outright, so
this writes to data/research/ and NEVER to data/registers/. It is a lead and
verification source for hand-verified entries, the same ruling as Nevada's.
Full record in OPEN_DATA_SURVEY.md.

    python3 scripts/texas_big_trees.py --fetch        sweep all 352 species
    python3 scripts/texas_big_trees.py --near Austin  what is within reach
    python3 scripts/texas_big_trees.py --cities       every ranked Texas city

COUNTY NAMES ARE NOT TO BE TRUSTED. The scouting pass caught it in the raw
data: 4 of 18 rows tagged CountyName "Harris" carry coordinates in the
Panhandle near Amarillo, 800 km from Houston. So --near filters on distance
and prints CountyName only as a label. That is the same class of fault as
ICNF's metres-in-a-centimetres-column and it is why every register import here
gets a physical sanity check.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import km  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "research", "texas-big-tree-registry.json")
BASE = "https://texasforestinfo.tamu.edu/BigTreeRegistry"
TIMEOUT = 20  # every fetch gets a hard timeout; a host that hangs costs a window

# Texas is wide and its cities are far apart, so a single radius would be
# wrong. This is the day-trip band CLAUDE.md sets, roughly 30 minutes out,
# read generously because these are driving cities.
CITIES = {
    "Houston": (29.7604, -95.3698),
    "Dallas": (32.7767, -96.7970),
    "Austin": (30.2672, -97.7431),
    "San Antonio": (29.4241, -98.4936),
    "Fort Worth": (32.7555, -97.3308),
    "El Paso": (31.7619, -106.4850),
}
DEFAULT_KM = 40.0

# Below this a tree is not what this site ships. 250 cm of girth is roughly
# where a specimen starts reading as old rather than merely mature, and the
# scouting pass found Harris County full of 70 to 150 cm ornamentals.
INTERESTING_CM = 250.0
CM_PER_INCH = 2.54


def post(path, payload):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as fh:
        return json.loads(fh.read().decode("utf-8", "replace"))


def fetch():
    species = post("/Home/GetSpeciesList", {})
    names = []
    for s in species:
        if isinstance(s, dict):
            name = s.get("LatinName") or s.get("latinName") or s.get("Name")
        else:
            name = s
        if name:
            names.append(name)
    print("%d species to sweep" % len(names))

    seen, rows, failed = set(), [], []
    for i, name in enumerate(names, 1):
        try:
            got = post("/Home/GetAllTrees", {"species": name})
        except (urllib.error.URLError, OSError, ValueError) as exc:
            failed.append({"species": name, "error": str(exc)[:120]})
            continue
        for t in got or []:
            key = t.get("TreeID") or (t.get("LatDec"), t.get("LongDec"), t.get("LatinName"))
            if key in seen:
                continue
            seen.add(key)
            rows.append(t)
        if i % 50 == 0:
            print("  %d/%d species, %d trees" % (i, len(names), len(rows)))
        time.sleep(0.25)

    doc = {
        "source": "Texas Big Tree Registry, Texas A&M Forest Service",
        "url": BASE,
        "licence": "NON-COMMERCIAL, therefore NOT importable to data/registers/. "
                   "Texas A&M Forest Service offers content 'for personal, "
                   "educational, and other non-commercial purposes' with a "
                   "citation requirement. Usable as a lead and verification "
                   "source for hand-verified entries only. See "
                   "OPEN_DATA_SURVEY.md.",
        "warning": "CountyName is unreliable: rows tagged Harris have been seen "
                   "with Panhandle coordinates 800 km away. Filter on distance.",
        "species_swept": len(names),
        "species_failed": failed,
        "count": len(rows),
        "trees": rows,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
    print("%d trees from %d species -> %s%s"
          % (len(rows), len(names), os.path.relpath(OUT, ROOT),
             (" (%d species failed)" % len(failed)) if failed else ""))
    return doc


def load():
    with open(OUT, encoding="utf-8") as fh:
        return json.load(fh)


def girth_cm(t):
    """Circumference in cm. The registry publishes inches, so a raw number here
    would read as a sapling. This is exactly the ICNF trap pointing the other
    way, and it is worth stating in code rather than remembering."""
    v = t.get("Circumference")
    try:
        return float(v) * CM_PER_INCH
    except (TypeError, ValueError):
        return None


def near(point, trees, radius):
    out = []
    for t in trees:
        try:
            lat, lon = float(t["LatDec"]), float(t["LongDec"])
        except (KeyError, TypeError, ValueError):
            continue
        d = km(point, (lat, lon))
        if d <= radius:
            out.append((d, t))
    out.sort(key=lambda r: r[0])
    return out


def show(city, trees, radius):
    if city not in CITIES:
        print("unknown city: %s (known: %s)" % (city, ", ".join(sorted(CITIES))))
        return 1
    rows = near(CITIES[city], trees, radius)
    big = [(d, t) for d, t in rows if (girth_cm(t) or 0) >= INTERESTING_CM]
    print("%s: %d registry trees within %.0f km, %d of them %.0f cm round or more\n"
          % (city, len(rows), radius, len(big), INTERESTING_CM))
    if not big:
        print("  Nothing above the girth bar. The registry is a champion-tree list,")
        print("  so a county can be full of record-holding ornamentals and hold")
        print("  nothing this site would send anyone across town for.")
        return 0
    for d, t in big:
        g = girth_cm(t)
        print("%5.1f km  %-30s %6.0f cm  h %-5s  %-12s  %s"
              % (d, str(t.get("LatinName"))[:30], g,
                 t.get("Height") or "?", str(t.get("CountyName"))[:12],
                 "CHAMPION" if t.get("NationalChampion") else ""))
        print("          %.5f,%.5f  TreeID %s  condition %s"
              % (float(t["LatDec"]), float(t["LongDec"]),
                 t.get("TreeID"), t.get("Condition") or "?"))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="sweep every species")
    ap.add_argument("--near", help="one city name")
    ap.add_argument("--cities", action="store_true", help="every known Texas city")
    ap.add_argument("--km", type=float, default=DEFAULT_KM)
    a = ap.parse_args()

    if a.fetch:
        fetch()
        return 0
    try:
        doc = load()
    except OSError:
        print("no local sweep yet, run: python3 scripts/texas_big_trees.py --fetch")
        return 1
    trees = doc["trees"]
    print("%d trees swept from %d species\n" % (doc["count"], doc.get("species_swept", 0)))
    if a.near:
        return show(a.near, trees, a.km)
    if a.cities:
        for city in CITIES:
            rows = near(CITIES[city], trees, a.km)
            big = sum(1 for d, t in rows if (girth_cm(t) or 0) >= INTERESTING_CM)
            print("  %-13s %3d within %.0f km, %2d above %.0f cm"
                  % (city, len(rows), a.km, big, INTERESTING_CM))
        return 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
