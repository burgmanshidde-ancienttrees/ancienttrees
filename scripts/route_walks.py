#!/usr/bin/env python3
"""Real pedestrian routes for every city walk, fetched once and cached.

Hidde, 2026-08-08: "the walking route is very unrealistic because it's straight
lines from tree to tree, not the shape of the streets you need to walk." He is
right, and on a long walk a straight line stops being a hint and starts being a
lie: it can cross the Vltava or run through a building while telling somebody to
walk that way.

The fix deliberately does NOT put a routing service in the visitor's browser.
This script fetches each walk once, decodes the geometry, and writes it to
data/walk-routes.json, which the build reads. So there is no key in any page, no
request from any visitor, nothing to rate-limit, and if the service disappears
tomorrow every route we already have keeps working. Same pattern as the
registers: retrieval by script, cached in the repo, never a live dependency.

Service: FOSSGIS's public Valhalla, the OpenStreetMap community instance. No
key, no account, pedestrian costing. Be polite: one request at a time with a
pause, and never re-fetch a walk whose trees have not changed.

    python3 scripts/route_walks.py            # only walks with no cached route
    python3 scripts/route_walks.py --refresh  # re-fetch everything

A route is REJECTED and the straight line kept when the routed distance is more
than 2.5x the straight-line distance. That is the sanity check for the known
weak spot: pedestrian routing through parks and botanical gardens, where a path
may simply be missing from OpenStreetMap, so the router sends you the long way
round the outside. A wrong route is worse than an honest schematic one.
"""
import json
import os
import sys
import subprocess
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import walks_feed as WF  # noqa: E402
from geo import km as geo_km  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "walk-routes.json")
URL = "https://valhalla1.openstreetmap.de/route"
UA = "AncientTreesBot/1.0 (https://ancienttrees.app; walk routing, cached)"
MAX_DETOUR = 2.5
# And a floor. A pedestrian route is always LONGER than the crow flies; one that
# comes back shorter has snapped its stops together rather than routed between
# them. 0.4 is loose on purpose: the straight-line figure is itself a rounded
# sum, so a genuine route can undercut it slightly on a short walk.
MIN_PLAUSIBLE = 0.4
# And it has to go PAST THE TREES. A pedestrian router snaps to the network it
# knows: a tree inside a park whose paths are missing from OpenStreetMap gets a
# line along the road outside, which is a real route to the wrong place.
#
# Hidde found it on his phone (2026-08-25, Baarn's Cantonspark walk): "how come
# this walk actually misses the tree?" The American Oak of the Pekingtuin sat 75
# metres from its own route. Measured across the whole cache with
# scripts/walkcheck.py: 47 of 2027 stops, 2.3 percent, in 21 cities, the worst
# 260 metres in Boston.
#
# 60 metres, not the 40 walkcheck.py reports on: 40 is where a line stops
# reading as "past the tree" on a phone, and this is the line where a route is
# worse than the honest schematic it would fall back to.
MAX_MISS_M = 60.0


def decode_polyline6(s):
    """Valhalla returns an encoded polyline at precision 6."""
    coords, i, lat, lng = [], 0, 0, 0
    while i < len(s):
        for who in range(2):
            shift, result = 0, 0
            while True:
                b = ord(s[i]) - 63
                i += 1
                result |= (b & 0x1F) << shift
                shift += 5
                if b < 0x20:
                    break
            d = ~(result >> 1) if result & 1 else (result >> 1)
            if who == 0:
                lat += d
            else:
                lng += d
        coords.append([round(lng / 1e6, 6), round(lat / 1e6, 6)])
    return coords


def fetch_route(points):
    """Fetched with curl, not urllib, and that is not a style choice.

    The Python on this machine links LibreSSL 2.8.3, which is old enough that
    valhalla1.openstreetmap.de refuses the handshake outright: every one of 87
    requests died with SSLV3_ALERT_HANDSHAKE_FAILURE while the identical request
    through curl returned 200. Worth remembering before blaming a host that is
    actually answering fine."""
    body = json.dumps({
        "locations": [{"lat": p[0], "lon": p[1]} for p in points],
        "costing": "pedestrian",
        "directions_options": {"units": "kilometers"},
    })
    out = subprocess.run(
        ["curl", "-s", "-m", "40", "-A", UA, "-H", "Content-Type: application/json",
         "-d", body, URL],
        capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    trip = d["trip"]
    shape = []
    for leg in trip["legs"]:
        shape.extend(decode_polyline6(leg["shape"]))
    return shape, trip["summary"]["length"], trip["summary"]["time"] / 60.0


def metres_to_line(point, shape):
    """Shortest distance from a stop to the drawn line, in metres.

    Shared with scripts/walkcheck.py, which reports on the whole cache; this
    file needs it to refuse a route as it arrives."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import walkcheck
    return walkcheck.metres_to_line(point, shape)


def worst_miss(shape, points):
    """How far the furthest stop sits from the line."""
    if not shape or len(shape) < 2:
        return 0.0
    return max(metres_to_line(p, shape) for p in points)


def main():
    refresh = "--refresh" in sys.argv
    recheck = "--recheck" in sys.argv
    cache = {}
    if os.path.exists(OUT) and not refresh:
        cache = json.load(open(OUT)).get("routes", {})

    # THE WALKS THE SITE PUBLISHES, not a second planning of them.
    #
    # This script used to plan the walks itself, in Python, from a port of the
    # same algorithm that site/src/lib/walks.ts runs. Two implementations cannot
    # be kept in step by discipline and were not: the site plans from
    # walkableTrees() and this planned from every tree, so the ordered id lists
    # differed, and the ordered id list is the cache key. 67 of 212 walks had no
    # route and re-running this said there was nothing to do.
    #
    # Hidde, 2026-08-25: "ik denk dat 1 wandelalgoritme wel de moeite is toch om
    # de boel simpeler en hetzelfde te houden." So the algorithm lives once, in
    # TypeScript, where the pages and the app's feed are built, and this reads
    # its output. scripts/walk_planning.py's planning half is gone with it.
    #
    # The consequence, stated because it is a real one: a NEW walk gets its
    # street route on the next deploy rather than the same one. Build, publish,
    # route, publish again. That is what the two passes today did by hand.
    coords = WF.tree_coords()
    todo, done, rejected, skipped = [], 0, 0, 0
    for w in WF.walks():
        ids = [i for i in (w.get("trees") or []) if i in coords]
        if len(ids) < 2:
            continue
        key = (w.get("city_slug") or "") + ":" + ",".join(ids)
        if key in cache:
            skipped += 1
            continue
        pts = [coords[i] for i in ids]
        # The crow flies between the stops, in the walk's own order. The feed's
        # own `km` carries the site's 1.35 detour factor, which would make the
        # 2.5x check compare a routed distance against an already-inflated one.
        straight = sum(geo_km(a, b) for a, b in zip(pts, pts[1:]))
        todo.append((key, pts, round(straight, 2)))

    if recheck:
        # Re-judge what is already cached against the rules as they stand now,
        # which is how the 60 metre miss rule reaches the routes fetched before
        # it existed. Also prunes keys no walk uses any more: the ordering
        # changed once today, and the cache kept both orders, one of them good
        # and one of them 75 metres off the tree.
        demoted = 0
        for key in sorted(cache):
            r = cache[key]
            shape = r.get("shape")
            if not shape:
                continue
            pts = [coords[i] for i in key.split(":", 1)[1].split(",") if i in coords]
            if not pts:
                continue
            miss = worst_miss(shape, pts)
            if miss > MAX_MISS_M:
                cache[key] = {"rejected": True,
                              "routed_km": r.get("km"),
                              "worst_miss_m": round(miss)}
                demoted += 1
                print(f"  {key[:44]:44} demoted: misses a stop by {miss:.0f} m")
        print(f"{demoted} cached route(s) demoted for missing a stop")

    print(f"{len(todo)} walks to route, {skipped} already cached")
    for key, pts, straight_km in todo:
        try:
            shape, km, mins = fetch_route(pts)
        except Exception as e:
            print(f"  {key[:44]:44} FAILED {e}")
            time.sleep(1.5)
            continue
        distinct = len({(round(c[0], 6), round(c[1], 6)) for c in shape})
        if straight_km and km > straight_km * MAX_DETOUR:
            print(f"  {key[:44]:44} rejected: routed {km:.1f} km vs {straight_km} straight")
            cache[key] = {"rejected": True, "routed_km": round(km, 2)}
            rejected += 1
        elif (miss := worst_miss(shape, pts)) > MAX_MISS_M:
            print(f"  {key[:44]:44} rejected: misses a stop by {miss:.0f} m")
            cache[key] = {"rejected": True, "routed_km": round(km, 2),
                          "worst_miss_m": round(miss)}
            rejected += 1
        elif distinct < 2 or (straight_km and km < straight_km * MIN_PLAUSIBLE):
            # The OTHER failure, and it is the dangerous one because it looks
            # like a success. Oahu came back on 2026-08-25 as eight copies of
            # one coordinate, 0.0 km and 0 minutes, for a five tree walk: the
            # router found no pedestrian network and snapped every stop to the
            # same node. A route shorter than the straight line between its own
            # ends is not a route, and drawing it would put a walk on the map
            # with no line and a promise of no distance at all.
            print(f"  {key[:44]:44} rejected: routed {km:.1f} km vs {straight_km} "
                  f"straight, {distinct} distinct point(s)")
            cache[key] = {"rejected": True, "routed_km": round(km, 2)}
            rejected += 1
        else:
            cache[key] = {"shape": shape, "km": round(km, 2), "minutes": int(round(mins))}
            done += 1
            print(f"  {key[:44]:44} {km:.1f} km, {int(round(mins))} min, {len(shape)} points")
        time.sleep(1.2)

    json.dump({
        "note": ("Pedestrian routes for city walks, fetched once from FOSSGIS's public "
                 "Valhalla (OpenStreetMap community instance, no key) and cached here so "
                 "no visitor's browser ever calls a routing service. Keyed by city slug "
                 "plus the walk's ordered tree ids, so a changed walk re-routes by itself. "
                 "'rejected' marks a route more than 2.5x longer than the straight line, "
                 "which usually means a path is missing from OSM inside a park; the build "
                 "falls back to the honest straight line for those."),
        "attribution": "Routing by Valhalla via FOSSGIS, data (c) OpenStreetMap contributors, ODbL",
        "routes": cache,
    }, open(OUT, "w"), indent=1)
    print(f"\n{done} routed, {rejected} rejected as implausible -> data/walk-routes.json")


if __name__ == "__main__":
    main()
