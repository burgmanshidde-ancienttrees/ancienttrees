#!/usr/bin/env python3
"""Turn the Texas Big Tree Registry sweep into per-city leads.

Hidde, 2026-09-01: "ik wil meer lege steden in de US" and then "openen". The
supply for that was already on disk and unread. scripts/texas_big_trees.py
swept the whole state once on 2026-08-20 and left 660 trees in
data/research/texas-big-tree-registry.json, every one with WGS84 coordinates,
a Latin name, a circumference, a condition and a measurement date. Three
cities got a partial hand conversion that day and three never got one at all,
so 41 trees inside six ranked cities sat where nothing reads them.

LEADS, never registers, and never data/cities. OPEN_DATA_SURVEY.md records the
licence verdict and it does not bend: Texas A&M Forest Service's terms
disqualify the registry for bulk import, and it is usable only to FIND
candidates that are then hand-verified from an independent source. So each row
becomes a lead carrying its measurements and the reason it is a lead, and a
verify pass still has to find the second source and the actual place before
anything ships.

Matching is by distance from the city centre, not by county, because a Texas
county is far larger than a day trip: Harris County alone is bigger than
Luxembourg. The radius is CLAUDE.md's own day-trip boundary read generously
for cities built around driving.

Usage:
  python3 scripts/texas_leads.py            # report
  python3 scripts/texas_leads.py --write
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SWEEP = os.path.join(ROOT, "data", "research", "texas-big-tree-registry.json")
LEADS = os.path.join(ROOT, "data", "leads")

# City centres, for the distance match only. Hardcoded because these six are
# the whole Texas set in the queue and a geocoder call per run would be a
# network dependency bought for six constants.
CITIES = {
    "dallas":      ("Dallas",      32.7767,  -96.7970),
    "houston":     ("Houston",     29.7604,  -95.3698),
    "austin":      ("Austin",      30.2672,  -97.7431),
    "san-antonio": ("San Antonio", 29.4241,  -98.4936),
    "fort-worth":  ("Fort Worth",  32.7555,  -97.3308),
    "el-paso":     ("El Paso",     31.7619, -106.4850),
}
RADIUS_KM = 30.0


def km(a_lat, a_lng, b_lat, b_lng):
    r = 6371.0
    p1, p2 = math.radians(a_lat), math.radians(b_lat)
    dp = math.radians(b_lat - a_lat)
    dl = math.radians(b_lng - a_lng)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def inches_to_cm(v):
    try:
        return round(float(v) * 2.54)
    except (TypeError, ValueError):
        return None


def main():
    write = "--write" in sys.argv
    rows = json.load(open(SWEEP, encoding="utf-8"))
    if isinstance(rows, dict):
        rows = rows.get("trees") or rows.get("rows") or []

    for slug, (name, lat, lng) in sorted(CITIES.items()):
        near = []
        for r in rows:
            try:
                tlat, tlng = float(r["LatDec"]), float(r["LongDec"])
            except (KeyError, TypeError, ValueError):
                continue
            d = km(lat, lng, tlat, tlng)
            if d <= RADIUS_KM:
                near.append((d, r))
        near.sort(key=lambda p: p[0])

        path = os.path.join(LEADS, "%s.json" % slug)
        doc = {"city": name, "leads": [], "blocked": []}
        if os.path.exists(path):
            doc = json.load(open(path, encoding="utf-8"))
            doc.setdefault("leads", [])
        have = {(l.get("name") or "") for l in doc["leads"]}

        added = 0
        for d, r in near:
            species = (r.get("LatinName") or "").strip()
            tid = r.get("TreeID") or r.get("Id") or ""
            tag = "Texas Big Tree Registry TreeID %s" % tid if tid else "Texas Big Tree Registry"
            if any(str(tid) and str(tid) in h for h in have):
                continue
            girth = inches_to_cm(r.get("Circumference"))
            lead = {
                "name": "%s (%s)" % (species or "unnamed tree", tag),
                "species": species,
                "lat": float(r["LatDec"]),
                "lng": float(r["LongDec"]),
                "status": "lead",
                "reason": ("From the Texas Big Tree Registry sweep of 2026-08-20, "
                           "%.1f km from the centre of %s. Condition per the registry: "
                           "%s. Measured %s. NOT verified: the registry's licence "
                           "allows it as a lead source only, so this needs an "
                           "independent second source, the actual place named, and a "
                           "check that it stands somewhere the public may go."
                           % (d, name, r.get("Condition") or "not stated",
                              r.get("MeasurementDateString") or "date not stated")),
                # The flag, not just the prose: leads.py judges "has a pass
                # looked at this" by whether any reason text exists, so a
                # reason saying NOT VERIFIED would otherwise mark these READY.
                "needs_verification": True,
                "source": "Texas Big Tree Registry (lead source only, licence "
                          "disqualifies import; see OPEN_DATA_SURVEY.md)",
            }
            if girth:
                lead["girth_cm"] = girth
            doc["leads"].append(lead)
            added += 1

        print("%-12s %2d within %.0f km, %2d new (file had %d)"
              % (name, len(near), RADIUS_KM, added, len(doc["leads"]) - added))
        if write and added:
            json.dump(doc, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    if write:
        print("\nwritten. These are LEADS: a verify pass still has to find the second "
              "source before any of them ships.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
