#!/usr/bin/env python3
"""The walks, read from the one place that decides what a walk is.

Hidde, 2026-08-25: "ik denk dat 1 wandelalgoritme wel de moeite is toch om de
boel simpeler en hetzelfde te houden."

THE ALGORITHM NOW LIVES ONCE, in site/src/lib/walks.ts, which is where the pages
and the app's feed are built. It used to live twice, here in Python as well, and
scripts/walk_planning.py said in its own header that the two were "necessary,
not duplicated for its own sake" and warned that changing one without the other
is how they drift. They drifted anyway, and not through the algorithm: the site
started planning from walkableTrees() (no trees behind a ticket, none without a
story or coordinates) and the Python side kept planning from every tree. Two
planners with different INPUT produce different ordered id lists, and the ordered
id list is the cache key, so 67 of 212 walks had no route and the script that
fetches them reported nothing left to do.

A second implementation cannot be kept in step by discipline. So there is one,
and Python reads its output.

    from walks_feed import walks, by_city
    for w in walks():
        w["city_slug"], w["name"], w["trees"]   # ordered tree ids

Source order: the published feed, then the app's bundled snapshot of it. Both are
the same document; the snapshot is what appdata.py last downloaded, so it can be
a deploy behind and it keeps this working on a train.
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = "https://ancienttrees.app/api/walks.json"
BUNDLED = os.path.join(ROOT, "ios", "AncientTrees", "AncientTrees", "Data", "walks.json")

_cache = None


def _fetch():
    """curl, not urllib: the house style here, and the Python on this machine
    links a LibreSSL old enough to fail handshakes that curl completes."""
    out = subprocess.run(["curl", "-s", "-m", "25", LIVE],
                         capture_output=True, text=True)
    if out.returncode == 0 and out.stdout.strip().startswith("{"):
        return json.loads(out.stdout)
    return None


def walks(prefer_live=True):
    """Every published walk, newest published order preserved."""
    global _cache
    if _cache is not None:
        return _cache
    doc = _fetch() if prefer_live else None
    if doc is None:
        if not os.path.exists(BUNDLED):
            raise SystemExit("no walks to read: the feed is unreachable and "
                             "there is no bundled copy at %s" % BUNDLED)
        print("walks_feed: the live feed is unreachable, using the bundled copy")
        doc = json.load(open(BUNDLED, encoding="utf-8"))
    _cache = doc.get("walks", [])
    return _cache


def by_city(prefer_live=True):
    out = {}
    for w in walks(prefer_live):
        out.setdefault(w.get("city_slug") or "", []).append(w)
    return out


def tree_coords():
    """Every published tree's position, by id, from the city files."""
    out = {}
    cities = os.path.join(ROOT, "data", "cities")
    for name in sorted(os.listdir(cities)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(cities, name), encoding="utf-8") as fh:
            for t in json.load(fh).get("trees", []):
                loc = t.get("location") or {}
                if loc.get("latitude") is not None and loc.get("longitude") is not None:
                    out[t["id"]] = (loc["latitude"], loc["longitude"])
    return out


if __name__ == "__main__":
    ws = walks()
    per = by_city()
    print("%d walks in %d cities" % (len(ws), len(per)))
    print("with a routed shape: %d" % sum(1 for w in ws if w.get("shape")))
