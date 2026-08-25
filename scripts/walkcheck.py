#!/usr/bin/env python3
"""Does the drawn route actually go past the trees it is a route between.

Hidde, 2026-08-25, looking at Baarn's Cantonspark walk on his phone: "how come
this walk actually misses the tree, and does this happen more often?"

It happens because a pedestrian router snaps to the network it knows. A tree
stands inside a park; if the park's paths are missing from OpenStreetMap, the
nearest thing the router can route on is the road around the outside, so the line
runs along the street and never comes within fifty metres of the trunk. The route
is a real route and it is the wrong promise: somebody following it walks past the
tree and never sees it.

route_walks.py already refuses a route more than 2.5x the crow flies, which
catches the router going the LONG way round. Nothing measured whether the line
goes NEAR THE TREES, which is the thing a walk is for.

    python3 scripts/walkcheck.py             # every cached route, worst first
    python3 scripts/walkcheck.py --max 40    # fail above this many metres

A stop more than 40 m from the line is a miss: 40 m is about the width of a
street plus its pavements, so anything under that reads as "the line goes past
it" on a phone, and anything over reads as "the line ignores it".
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import km as geo_km  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def metres_to_line(point, shape):
    """Shortest distance in metres from a point to a polyline.

    Point to SEGMENT, not point to vertex: a long straight leg has few vertices
    and measuring to the nearest one would report a tree beside the middle of it
    as hundreds of metres away.
    """
    best = float("inf")
    lat, lng = point
    # A local flat approximation is fine at these distances and keeps this
    # readable: one degree of latitude is 111.32 km, longitude shrinks with
    # the cosine.
    import math
    kx = 111.32 * math.cos(math.radians(lat))
    ky = 111.32
    px, py = lng * kx, lat * ky
    for (alng, alat), (blng, blat) in zip(shape, shape[1:]):
        ax, ay = alng * kx, alat * ky
        bx, by = blng * kx, blat * ky
        dx, dy = bx - ax, by - ay
        if dx == 0 and dy == 0:
            d = math.hypot(px - ax, py - ay)
        else:
            t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
            d = math.hypot(px - (ax + t * dx), py - (ay + t * dy))
        best = min(best, d)
    return best * 1000.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=float, default=40.0,
                    help="metres a stop may sit from the line")
    ap.add_argument("--quiet", action="store_true", help="only the summary")
    args = ap.parse_args()

    routes = json.load(open(os.path.join(ROOT, "data", "walk-routes.json")))["routes"]
    # Coordinates by tree id, from the city files: the cache keys carry the ids.
    coords = {}
    cities = os.path.join(ROOT, "data", "cities")
    for name in sorted(os.listdir(cities)):
        if not name.endswith(".json"):
            continue
        for t in json.load(open(os.path.join(cities, name))).get("trees", []):
            loc = t.get("location") or {}
            if loc.get("latitude") is not None:
                coords[t["id"]] = (loc["latitude"], loc["longitude"])

    rows, checked, missed = [], 0, 0
    for key, r in sorted(routes.items()):
        shape = r.get("shape")
        if not shape or len(shape) < 2:
            continue
        city, _, ids = key.partition(":")
        for tid in ids.split(","):
            if tid not in coords:
                continue
            checked += 1
            d = metres_to_line(coords[tid], shape)
            if d > args.max:
                missed += 1
                rows.append((d, city, tid))

    rows.sort(reverse=True)
    if not args.quiet:
        for d, city, tid in rows[:40]:
            print("%6.0f m  %-14s %s" % (d, city, tid))
        if len(rows) > 40:
            print("  ... and %d more" % (len(rows) - 40))
    print("\n%d of %d stops sit more than %.0f m from their own route (%.1f%%)"
          % (missed, checked, args.max, 100.0 * missed / max(checked, 1)))
    walks = len({(c, ) for _, c, _ in rows})
    print("%d cities have at least one" % walks)
    return 1 if missed else 0


if __name__ == "__main__":
    raise SystemExit(main())
