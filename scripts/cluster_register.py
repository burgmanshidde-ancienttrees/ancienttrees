#!/usr/bin/env python3
"""Turn an official tree register into a worklist of walkable clusters.

The point (Hidde, 2026-08-03): a city page is only a good afternoon when its
trees can be walked between. Measured across the 81 published cities, Cadiz
spans 600 metres and reads as a walk; Kyoto spans 35 kilometres and does not.
So the unit of work is the cluster, not the city, and the count per city is an
output rather than an input.

This does the cheap half of a country pass. It is arithmetic, not research:
no model, no network, no cost. Point it at a register in data/registers/ and
it groups the entries into everything reachable on foot, so a research pass
starts from "verify these six trees around this point" instead of "find the
ten best trees in this metropolis".

    python3 scripts/cluster_register.py data/registers/portugal-icnf.json
    python3 scripts/cluster_register.py data/registers/*.json --radius 1.5

What it cannot do, and a run must still do: decide whether a designated tree
is actually remarkable, verify it against a second source, and write it.
A register says a tree is protected, not that it is worth the walk.
"""
import argparse
import glob
import json
import math
import sys

FLOOR = 4          # fewer than this and a place earns no page (CLAUDE.md)
CEILING = 8        # more than this is a second walk, not a longer one


def km(a, b):
    r, p = 6371.0, math.pi / 180
    dlat, dlon = (b[0] - a[0]) * p, (b[1] - a[1]) * p
    x = (math.sin(dlat / 2) ** 2
         + math.cos(a[0] * p) * math.cos(b[0] * p) * math.sin(dlon / 2) ** 2)
    return 2 * r * math.asin(math.sqrt(x))


def load(path):
    """Registers differ in shape; take entries or trees, and whatever the
    coordinate fields happen to be called."""
    d = json.load(open(path))
    rows = d.get("entries") or d.get("trees") or (d if isinstance(d, list) else [])
    out = []
    for t in rows:
        loc = t.get("location") or {}
        lat = t.get("latitude") or loc.get("latitude")
        lng = t.get("longitude") or loc.get("longitude")
        if lat is None or lng is None:
            continue
        out.append({
            "lat": float(lat), "lng": float(lng),
            "name": t.get("name") or t.get("name_pt") or t.get("species") or "?",
            "species": t.get("species", ""),
            "place": t.get("concelho") or t.get("freguesia") or t.get("city") or "",
            "age": t.get("age_register") or t.get("age_estimate") or "",
            "girth": t.get("girth_cm") or "",
        })
    return out, d.get("source", path)


def cluster(points, radius):
    """Greedy: repeatedly take the point with the most unclaimed neighbours
    within the radius and claim them together. Simple on purpose, and stable,
    which matters more here than optimality."""
    left = set(range(len(points)))
    groups = []
    while left:
        seed = max(left, key=lambda i: sum(
            1 for j in left if km((points[i]["lat"], points[i]["lng"]),
                                  (points[j]["lat"], points[j]["lng"])) <= radius))
        grp = [j for j in left
               if km((points[seed]["lat"], points[seed]["lng"]),
                     (points[j]["lat"], points[j]["lng"])) <= radius]
        groups.append(grp)
        left -= set(grp)
    return sorted(groups, key=len, reverse=True)


def report(path, radius):
    pts, source = load(path)
    if not pts:
        print(f"{path}: no entries with coordinates")
        return
    groups = cluster(pts, radius)
    usable = [g for g in groups if len(g) >= FLOOR]
    covered = sum(len(g) for g in usable)
    print(f"\n{source}")
    print(f"  {len(pts)} registered trees with coordinates, "
          f"{len(usable)} walkable clusters of {FLOOR}+ within {radius} km, "
          f"covering {covered} of them ({covered * 100 // len(pts)}%)")
    for n, g in enumerate(usable, 1):
        lat = sum(pts[i]["lat"] for i in g) / len(g)
        lng = sum(pts[i]["lng"] for i in g) / len(g)
        spread = max(km((pts[i]["lat"], pts[i]["lng"]), (pts[j]["lat"], pts[j]["lng"]))
                     for i in g for j in g) if len(g) > 1 else 0.0
        places = sorted({p["place"] for p in (pts[i] for i in g) if p["place"]})
        note = "" if len(g) <= CEILING else f"  (split into {math.ceil(len(g) / CEILING)} walks)"
        print(f"\n  {n}. {len(g)} trees, {spread:.1f} km across, centre {lat:.4f}, {lng:.4f}"
              f"{note}")
        if places:
            print(f"     {', '.join(places[:4])}")
        for i in g[:CEILING]:
            p = pts[i]
            extra = " ".join(x for x in (str(p["age"]), f"{p['girth']}cm" if p["girth"] else "") if x)
            print(f"       - {p['name'][:44]:<44} {extra}")
        if len(g) > CEILING:
            print(f"       ... and {len(g) - CEILING} more, which is the second walk")
    stranded = len(pts) - covered
    if stranded:
        print(f"\n  {stranded} trees stand alone and cannot join a walk. "
              f"They are leads, not entries.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("registers", nargs="+")
    ap.add_argument("--radius", type=float, default=2.0,
                    help="walkable radius in km, default 2.0 (about 25 minutes)")
    args = ap.parse_args()
    paths = [p for pat in args.registers for p in glob.glob(pat)]
    if not paths:
        print("no register files matched")
        return 1
    for p in sorted(paths):
        report(p, args.radius)
    return 0


if __name__ == "__main__":
    sys.exit(main())
