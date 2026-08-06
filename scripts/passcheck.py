#!/usr/bin/env python3
"""Everything you must know about a place BEFORE writing a research brief.

Three passes have now been sent out to "open" a city that was already live
(Napoli, Firenze, Munich), each time because a queue entry said new and nobody
checked. Munich alone cost 127,000 tokens to discover the page had existed for
eleven days. The rule to check first has been written down twice and failed
twice, so this is the mechanism instead: one command, run before any brief.

    python3 scripts/passcheck.py Munich
    python3 scripts/passcheck.py Torino        works in the local language too
    python3 scripts/passcheck.py 45.07 7.68    or by coordinate

It answers, in order: is this place already published, under what name, with
how many trees and photos and how tight a walk; which id prefix it uses and
what the next free id is; how many register trees sit within reach; what a
previous pass already put in leads and blocked, so nothing is re-researched;
and which prefixes are taken, so a new city picks a free one.
"""
import glob
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cluster_register import km  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAME_CITY_KM = 20.0

# Local name to our slug, for the cases a name lookup alone would miss. Distance
# is the real test; this only helps the first guess.
ALIAS = {
    "napoli": "naples", "firenze": "florence", "roma": "rome", "milano": "milan",
    "torino": "turin", "genova": "genoa", "venezia": "venice", "lisboa": "lisbon",
    "sevilla": "seville", "muenchen": "munich", "munchen": "munich",
    "wien": "vienna", "praha": "prague", "bruxelles": "brussels",
    "brussel": "brussels", "koebenhavn": "copenhagen", "lissabon": "lisbon",
}


def fold(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def cities():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        d = json.load(open(f))
        trees = d.get("trees") or []
        if not trees:
            continue
        pts = [(t["location"]["latitude"], t["location"]["longitude"]) for t in trees]
        out.append({
            "city": d["city"], "slug": os.path.basename(f)[:-5], "n": len(trees),
            "photos": sum(1 for t in trees if (t.get("photo") or {}).get("url")),
            "approx": sum(1 for t in trees if t.get("location_precision") == "approximate"),
            "spread": max((km(a, b) for a in pts for b in pts), default=0.0),
            "ids": sorted(t["id"] for t in trees),
            "lat": sum(p[0] for p in pts) / len(pts),
            "lng": sum(p[1] for p in pts) / len(pts),
        })
    return out


def register_trees_near(lat, lng, radius=SAME_CITY_KM):
    n = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "registers", "*.json"))):
        d = json.load(open(path))
        if not isinstance(d, dict):
            continue
        for t in (d.get("entries") or []) + (d.get("trees") or []):
            if t.get("group"):
                continue
            la, lo = t.get("latitude"), t.get("longitude")
            if la is None or lo is None:
                continue
            if km((lat, lng), (la, lo)) <= radius:
                n += 1
    return n


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    live = cities()
    arg = " ".join(sys.argv[1:])

    match, coord = None, None
    parts = arg.replace(",", " ").split()
    if len(parts) == 2:
        try:
            coord = (float(parts[0]), float(parts[1]))
        except ValueError:
            coord = None
    if coord:
        match = min(live, key=lambda c: km(coord, (c["lat"], c["lng"])))
        if km(coord, (match["lat"], match["lng"])) > SAME_CITY_KM:
            match = None
    else:
        key = fold(arg)
        key = fold(ALIAS.get(key, key))
        match = next((c for c in live if fold(c["city"]) == key or fold(c["slug"]) == key), None)

    print(f"\n=== passcheck: {arg} ===\n")
    if match:
        print(f"  ALREADY PUBLISHED as {match['city']} (/{match['slug']})")
        print(f"  {match['n']} trees, {match['photos']} with a photo, "
              f"{match['approx']} approximate pins, walk spans {match['spread']:.1f} km")
        print(f"  ids {match['ids'][0]} to {match['ids'][-1]}; "
              f"a deepening pass starts at {match['ids'][-1][:4]}{int(match['ids'][-1][4:]) + 1:03d}")
        print(f"  register trees within {SAME_CITY_KM:.0f} km: "
              f"{register_trees_near(match['lat'], match['lng'])}")
        print("\n  => brief this as DEEPEN. Deliver a JSON ARRAY of tree objects to")
        print(f"     data/research/{match['slug']}-extra.json, never a full city object,")
        print("     and never edit the city file. Count promises in the existing copy")
        print("     must be fixed at merge or the build fails.")
    else:
        print("  NOT published. This would be a new city.")
        if coord:
            print(f"  register trees within {SAME_CITY_KM:.0f} km: {register_trees_near(*coord)}")
        taken = sorted({i[:3] for c in live for i in c["ids"]})
        print(f"\n  id prefixes already in use ({len(taken)}): {' '.join(taken)}")
        print("  pick three letters that are NOT in that list.")

    slug = match["slug"] if match else fold(arg)
    for kind, pat in (("leads", "leads"), ("research", "research")):
        for f in sorted(glob.glob(os.path.join(ROOT, "data", pat, f"*{slug}*"))):
            try:
                d = json.load(open(f))
                counts = {k: len(v) for k, v in d.items() if isinstance(v, list)} if isinstance(d, dict) else {"items": len(d)}
            except Exception:
                counts = "not json"
            print(f"\n  {kind}: {os.path.relpath(f, ROOT)}  {counts}")
            print("     read it before researching: it says what was already rejected and why")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
