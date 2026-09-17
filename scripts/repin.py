#!/usr/bin/env python3
"""Recover a lead's position from a coordinate it already carries.

The sibling of refill.py, and the same shape of problem. refill.py recovers a
missing species from the tree's own name; this recovers a missing POSITION from
a coordinate the lead is already holding under a key nothing reads.

Found 2026-09-11 while asking why the writable pile stood at 3 against a floor
of 60. leads.readiness() looks for `latitude`/`longitude` or `lat`/`lng`, which
is what almost every lead uses. A handful were written by passes that spelled it
`coordinates: [lat, lng]`, `coords: [lat, lng]`, or `coordinate: "lat, lng"`,
and those leads have been counted as position-less ever since, so a story could
not be written from them and nobody could see why.

This is recovery, never geocoding: it copies a number the file already holds
into the field the pipeline reads, and it touches nothing else. A lead with no
coordinate anywhere stays without one, because inventing a position is the one
error CLAUDE.md says a reader cannot forgive.

    python3 scripts/repin.py            # report, writes nothing
    python3 scripts/repin.py --write    # copy and save
"""
import argparse
import glob
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEADS = os.path.join(ROOT, "data", "leads")
# Every spelling found in the corpus. Order matters only for reporting.
ALIASES = ("coordinates", "coords", "coordinate", "latlng", "position")
PAIR = re.compile(r"^\s*(-?\d{1,3}(?:\.\d+)?)\s*,\s*(-?\d{1,3}(?:\.\d+)?)\s*$")


def as_pair(value):
    """(lat, lng) from whatever shape the value is in, or None.

    Refuses anything it cannot read rather than guessing: a bare string like
    "in the churchyard" is a hint, not a position, and a pair outside the
    possible range of a coordinate is a unit error of the kind CLAUDE.md
    records for ICNF's girth column.
    """
    lat = lng = None
    if isinstance(value, (list, tuple)) and len(value) == 2:
        try:
            lat, lng = float(value[0]), float(value[1])
        except (TypeError, ValueError):
            return None
    elif isinstance(value, dict):
        for a, b in (("lat", "lng"), ("latitude", "longitude")):
            if value.get(a) is not None and value.get(b) is not None:
                try:
                    lat, lng = float(value[a]), float(value[b])
                except (TypeError, ValueError):
                    return None
                break
    elif isinstance(value, str):
        m = PAIR.match(value)
        if not m:
            return None
        lat, lng = float(m.group(1)), float(m.group(2))
    if lat is None or lng is None:
        return None
    if not (-90 <= lat <= 90 and -180 <= lng <= 180):
        return None
    # 0,0 is the Atlantic, and in practice it is a null that got written as a
    # number rather than a tree anybody has stood in front of.
    if lat == 0 and lng == 0:
        return None
    return lat, lng


def reference_point(slug, rows):
    """Roughly where this lead file's trees are, to sanity-check a recovery.

    Published pins first, because they are verified; otherwise the mean of the
    leads in the same file that already carry a position. A file with neither
    gets no recovery at all, which is the safe answer rather than the
    convenient one.
    """
    path = os.path.join(ROOT, "data", "cities", slug + ".json")
    pts = []
    if os.path.exists(path):
        try:
            doc = json.load(open(path, encoding="utf-8"))
            pts = [(t["location"]["latitude"], t["location"]["longitude"])
                   for t in doc.get("trees", [])
                   if (t.get("location") or {}).get("latitude") is not None]
        except Exception:                             # noqa: BLE001
            pts = []
    if not pts:
        for lead in rows:
            if not isinstance(lead, dict):
                continue
            lat = lead.get("latitude", lead.get("lat"))
            lng = lead.get("longitude", lead.get("lng"))
            if lat is not None and lng is not None:
                pts.append((lat, lng))
    if not pts:
        return None
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def km(a, b):
    r = 6371.0
    la1, lo1, la2, lo2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    h = (math.sin((la2 - la1) / 2) ** 2
         + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2)
    return 2 * r * math.asin(math.sqrt(h))


# A lead belongs to the place whose file it sits in, so a recovered pin has to
# land near that place. 120 km is loose on purpose: the day-trip boundary plus
# room for a lead somebody filed in the nearest city's file.
NEAR_KM = 120


def check(pair, ref):
    """(lat, lng, basis) for a pair that lands where it should, else None.

    Luxembourg is why this exists. Five of its leads carry `coordinates` as
    [lng, lat], so copying them as written would have put five pins in the
    Indian Ocean, and a wrong pin is the one error CLAUDE.md says a reader
    cannot forgive. A swap is not guessed: it is accepted only when the pair as
    written lands nowhere near the place and the swapped pair lands on it,
    which is evidence rather than a hunch.
    """
    lat, lng = pair
    if km((lat, lng), ref) <= NEAR_KM:
        return lat, lng, "field"
    flipped = (lng, lat)
    if -90 <= flipped[0] <= 90 and km(flipped, ref) <= NEAR_KM:
        return flipped[0], flipped[1], "field, lat/lng swapped"
    return None


def missing_position(lead):
    return (lead.get("latitude", lead.get("lat")) is None
            or lead.get("longitude", lead.get("lng")) is None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="save the recovered pins")
    args = ap.parse_args()

    found, refused, files = [], [], 0
    for path in sorted(glob.glob(os.path.join(LEADS, "*.json"))):
        doc = json.load(open(path, encoding="utf-8"))
        rows = doc.get("leads") if isinstance(doc, dict) else doc
        if not isinstance(rows, list):
            continue
        slug = os.path.basename(path)[:-5]
        ref = reference_point(slug, rows)
        touched = False
        for lead in rows:
            if not isinstance(lead, dict) or not missing_position(lead):
                continue
            for key in ALIASES:
                if key not in lead:
                    continue
                pair = as_pair(lead[key])
                if not pair:
                    continue
                name = lead.get("name") or "(unnamed)"
                if ref is None:
                    refused.append((slug, name, key, pair, "nothing to check it against"))
                    break
                ok = check(pair, ref)
                if not ok:
                    refused.append((slug, name, key, pair,
                                    "%d km from %s" % (round(km(pair, ref)), slug)))
                    break
                lat, lng, basis = ok
                found.append((slug, name, key, (lat, lng), basis))
                if args.write:
                    lead["lat"], lead["lng"] = lat, lng
                    # Say where it came from, per goal 3: a bare number with no
                    # provenance is a fact nobody can check later.
                    lead["position_basis"] = (
                        "recovered from the lead's own `%s` field (%s)" % (key, basis))
                    touched = True
                break
        if touched:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(doc, fh, ensure_ascii=False, indent=1)
                fh.write("\n")
            files += 1

    print("%d lead(s) recovered a position from a key the pipeline does not read"
          % len(found))
    for city, name, key, (lat, lng), basis in found:
        print("  %-22s %-48s %-12s %9.5f, %9.5f  %s"
              % (city, name[:48], key, lat, lng, basis))
    if refused:
        print("\n%d refused, left without a position rather than pinned wrongly:"
              % len(refused))
        for city, name, key, pair, why in refused:
            print("  %-22s %-48s %-12s %s  (%s)"
                  % (city, name[:48], key, pair, why))
    if args.write:
        print("wrote %d file(s)" % files, file=sys.stderr)
    else:
        print("\n--write copies them into lat/lng")
    return 0


if __name__ == "__main__":
    sys.exit(main())
