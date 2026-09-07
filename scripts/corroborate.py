#!/usr/bin/env python3
"""Has anybody official already said this tree is remarkable?

Written 2026-09-07, for Hidde's question about reader-added trees: "in the end
we want trees people find worth the visit, not an all-trees database. So how do
we check that."

THE SPLIT THIS SCRIPT SITS ON. Deciding whether somebody would cross town for a
tree is judgement and stays judgement. What is NOT judgement, and was being
done by nobody, is asking whether a government already answered it. We hold
59,000-odd register rows with coordinates, and every one of them is a state
body saying this particular tree is monumental, protected or remarkable. A
reader's tree that lands within thirty metres of one of those arrives with an
official source attached: the two-independent-sources bar half met, for free,
before anyone spends a minute looking.

It cuts both ways and the second way matters more. A tree in a country whose
register we hold, standing nowhere near any entry in it, is a tree the state
looked at and did not designate. That is not a refusal, because registers miss
plenty and a reader standing in front of something is evidence too. It is a
reason to spend the judgement somewhere else first.

    python3 scripts/corroborate.py 52.0907 5.1214      # one coordinate
    python3 scripts/corroborate.py --leads             # every reader lead on file

WHAT IT IS NOT. Not a licence check: a register being open enough to IMPORT is
a separate question answered in OPEN_DATA_SURVEY.md, and this only reads what
is already on disk. Not a publish decision: a match makes a lead worth looking
at sooner, never worth skipping the bar.
"""
import argparse
import glob
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTERS = os.path.join(ROOT, "data", "registers")
LEADS = os.path.join(ROOT, "data", "leads", "_sightings.json")

# Metres per degree of latitude. Longitude is scaled by the cosine of the
# latitude at the point, which is accurate enough at the tens-of-metres range
# this script works in and needs no projection library.
M_PER_DEG = 111_320.0


def rows():
    """Every register row that carries a coordinate, flattened.

    Register files disagree about their own shape (some hold `entries`, some
    `trees`, some are a bare list) and about field names, which is what a
    register layer looks like when it comes from thirty different states. The
    two fields every one of them agrees on are latitude and longitude, so those
    are required and everything else is best effort.
    """
    out = []
    for path in sorted(glob.glob(os.path.join(REGISTERS, "*.json"))):
        try:
            with open(path) as fh:
                doc = json.load(fh)
        except Exception:
            continue
        items = doc.get("entries") or doc.get("trees") or (doc if isinstance(doc, list) else [])
        if not isinstance(items, list):
            continue
        source = os.path.basename(path)[:-5]
        designation = (doc.get("designation") if isinstance(doc, dict) else None) or ""
        for r in items:
            if not isinstance(r, dict):
                continue
            lat = r.get("latitude", r.get("lat"))
            lng = r.get("longitude", r.get("lng"))
            if lat is None or lng is None:
                continue
            try:
                lat, lng = float(lat), float(lng)
            except (TypeError, ValueError):
                continue
            out.append({
                "lat": lat, "lng": lng, "source": source, "designation": designation,
                "name": (r.get("name") or r.get("name_it") or r.get("name_cz")
                         or r.get("name_nl") or r.get("nome") or ""),
                "species": (r.get("species") or r.get("species_cz") or r.get("species_nl")
                            or r.get("especie") or ""),
                "girth_cm": r.get("girth_cm"),
                "height_m": r.get("height_m"),
            })
    return out


def metres(lat1, lng1, lat2, lng2):
    dy = (lat2 - lat1) * M_PER_DEG
    dx = (lng2 - lng1) * M_PER_DEG * math.cos(math.radians((lat1 + lat2) / 2))
    return math.hypot(dx, dy)


def nearest(lat, lng, table, within=100.0, limit=3):
    """The closest register entries, nearest first.

    A bounding box first, because 59,000 great-circle calculations per lead is
    a second of nothing when a degree of latitude settles it.
    """
    dlat = within / M_PER_DEG
    dlng = dlat / max(math.cos(math.radians(lat)), 0.01)
    near = [r for r in table
            if abs(r["lat"] - lat) <= dlat and abs(r["lng"] - lng) <= dlng]
    hits = []
    for r in near:
        d = metres(lat, lng, r["lat"], r["lng"])
        if d <= within:
            hits.append({**r, "distance_m": round(d, 1)})
    hits.sort(key=lambda h: h["distance_m"])
    return hits[:limit]


def verdict(hits):
    """One line a person can act on, and never a decision."""
    if not hits:
        return ("unlisted", "no register entry within 100 m: only this reader has "
                            "said it is remarkable, so it needs the normal bar")
    top = hits[0]
    if top["distance_m"] <= 30:
        return ("designated", "a register entry sits %.0f m away (%s%s): an official body "
                              "already calls this one remarkable"
                % (top["distance_m"], top["source"],
                   ", " + top["name"] if top["name"] else ""))
    return ("near", "the nearest register entry is %.0f m away (%s): possibly the same "
                    "tree, possibly its neighbour, so check before leaning on it"
            % (top["distance_m"], top["source"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("coords", nargs="*", type=float, help="latitude longitude")
    ap.add_argument("--leads", action="store_true",
                    help="check every reader lead in data/leads/_sightings.json")
    ap.add_argument("--within", type=float, default=100.0)
    a = ap.parse_args()

    table = rows()
    if not a.leads and len(a.coords) != 2:
        ap.error("give a latitude and a longitude, or --leads")

    if a.leads:
        try:
            with open(LEADS) as fh:
                leads = json.load(fh).get("leads", [])
        except Exception:
            print("no reader leads on file yet")
            return 0
        print(f"{len(leads)} reader lead(s) against {len(table)} register rows\n")
        for l in leads:
            lat, lng = l.get("latitude"), l.get("longitude")
            if lat is None or lng is None:
                print(f"  {(l.get('name') or 'unnamed')[:40]:42} no coordinate, cannot check")
                continue
            hits = nearest(lat, lng, table, a.within)
            tag, why = verdict(hits)
            print(f"  {(l.get('name') or 'unnamed')[:40]:42} {tag.upper():11} {why}")
        return 0

    lat, lng = a.coords
    hits = nearest(lat, lng, table, a.within)
    tag, why = verdict(hits)
    print(f"{tag.upper()}: {why}")
    for h in hits:
        bits = [b for b in (h["name"], h["species"],
                            f"{h['girth_cm']} cm round" if h.get("girth_cm") else None,
                            f"{h['height_m']} m tall" if h.get("height_m") else None) if b]
        print(f"  {h['distance_m']:6.1f} m  {h['source']}  {' | '.join(bits)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
