#!/usr/bin/env python3
"""Did this deploy change the shape of a feed the app reads?

THE PROBLEM. The app reads five feeds off ancienttrees.app and this site
deploys several times a day. A field that disappears or changes type breaks
every phone at once, and it does it SILENTLY: the app fails safe, keeps the
data it already had, and nobody crashes, so nobody reports anything while every
installed copy quietly stops updating.

WHY THIS COMPARES THE FEED TO ITSELF rather than to a description of what the
app wants. A second copy of the shape, written in Python next to the real one
in Swift, would drift within a fortnight and then we would be checking the copy.
So this asks a question that needs no second copy: is anything in the feed we
are about to publish MISSING or DIFFERENT from the feed that is live right now?
Additions are fine and happen weekly. Removals and type changes are the event.

The authoritative check is AncientTreesTests/LiveFeedContract.swift, which runs
the app's own decoder against the live feeds. This one is the early warning: it
runs at the moment the change is made, on the machine making it.

Usage:  python3 scripts/feedshape.py [--dist site/dist]
Exit 0 when nothing shrank, 1 when something did, 0 with a note when the live
site cannot be reached (a first deploy, or an outage, is not this check's news).
"""

import argparse
import json
import pathlib
import sys
import urllib.error
import urllib.request

LIVE = "https://ancienttrees.app"

# feed path -> the key holding its array of items, when it has one
FEEDS = {
    "/api/trees.json": "trees",
    "/api/walks.json": "walks",
    "/api/species.json": "species",
    "/api/browse.json": None,        # several arrays, walked generically
    "/api/version.json": None,
}


def kind(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, int):
        return "int"
    if isinstance(v, float):
        return "float"
    if isinstance(v, str):
        return "str"
    if isinstance(v, list):
        return "list"
    return "dict"


def profile(value, prefix="", out=None, depth=0):
    """field path -> how often it is there, out of how many, and its types.

    COUNTING MATTERS, and the first version of this did not do it. It only asked
    whether a field appeared SOMEWHERE, so five broken trees among eighteen
    hundred good ones were invisible: the field was still present on the other
    1853 and the type set still contained the right type. Five is enough. A
    Swift decoder reading an array gives up on the whole array at the first row
    it cannot read, so a partial break costs the entire feed, and a partial
    break is the likely kind: one city written differently, one script touching
    a subset.
    """
    out = {} if out is None else out
    if depth > 4:
        return out

    if isinstance(value, dict):
        for k, v in value.items():
            path = f"{prefix}.{k}" if prefix else k
            e = out.setdefault(path, {"types": set(), "present": 0, "of": 0})
            e["types"].add(kind(v))
            e["present"] += 1
            e["of"] += 1
            if isinstance(v, (dict, list)):
                profile(v, path, out, depth + 1)

    elif isinstance(value, list):
        # EVERY row, not a sample. A sample of the live feed and a sample of the
        # new one are not the same rows, so a field that is genuinely optional
        # and happens to cluster would read as "missing on 5 rows" purely
        # because the two samples fell differently. Eighteen hundred trees take
        # milliseconds here; the cap is only a runaway guard.
        items = [i for i in value[:20000] if isinstance(i, dict)]
        if not items:
            return out
        keys = set()
        for d in items:
            keys |= set(d.keys())
        for k in sorted(keys):
            path = f"{prefix}[].{k}"
            e = out.setdefault(path, {"types": set(), "present": 0, "of": 0})
            e["of"] += len(items)
            for d in items:
                if k not in d:
                    continue
                e["present"] += 1
                e["types"].add(kind(d[k]))
                if isinstance(d[k], (dict, list)):
                    profile(d[k], path, out, depth + 1)
    return out


def fetch(path):
    try:
        with urllib.request.urlopen(LIVE + path, timeout=30) as r:
            return json.loads(r.read())
    except (urllib.error.URLError, TimeoutError, ValueError, OSError):
        return None


def compare(path, live, new):
    """What the new feed lost or changed. Additions are deliberately ignored."""
    a, b = profile(live), profile(new)
    numbers = {"int", "float"}
    families = lambda ts: {"number" if t in numbers else t for t in ts}
    problems = []

    for field, was in sorted(a.items()):
        if field not in b:
            problems.append(f"{path}  {field} is GONE "
                            f"(was {'/'.join(sorted(families(was['types'])))})")
            continue
        now = b[field]

        # It used to be on every single row and now it is not. A decoder reading
        # a non-optional field gives up on the whole array at the first row that
        # lacks it, so "nearly always" is the same as "never".
        if was["of"] and was["present"] == was["of"] and now["present"] < now["of"]:
            missing = now["of"] - now["present"]
            problems.append(f"{path}  {field} is missing on {missing} of {now['of']} rows, "
                            f"and used to be on all of them")

        # A type that was never seen before. Not "the sets differ": adding an
        # int alongside a float is nothing, and null is caught by this too,
        # because null is a type this never saw.
        added = families(now["types"]) - families(was["types"])
        if added:
            problems.append(f"{path}  {field} is now sometimes "
                            f"{'/'.join(sorted(added))}, and never was "
                            f"(was {'/'.join(sorted(families(was['types'])))})")

    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default="site/dist")
    args = ap.parse_args()
    dist = pathlib.Path(args.dist)

    problems, checked, skipped = [], 0, []
    for path in FEEDS:
        built = dist / path.lstrip("/")
        if not built.exists():
            skipped.append(f"{path} was not built")
            continue
        try:
            new = json.loads(built.read_text())
        except ValueError as e:
            problems.append(f"{path}  is not valid JSON: {e}")
            continue
        live = fetch(path)
        if live is None:
            skipped.append(f"{path} could not be read from the live site")
            continue
        checked += 1
        problems += compare(path, live, new)

    for note in skipped:
        print(f"note: {note}")

    if problems:
        print(f"\n{len(problems)} feed change(s) that would break installed apps:\n")
        for p in problems:
            print("  " + p)
        print("\nAdding a field is always safe. Removing one, renaming one, or letting")
        print("one go null breaks every phone at once and silently, because the app")
        print("keeps the data it already had rather than crashing.")
        print("If this change is deliberate, the app has to ship first and this check")
        print("waits for it.")
        return 1

    if checked:
        print(f"feed shape: {checked} feed(s) unchanged or only added to")
    else:
        print("feed shape: nothing could be compared, so nothing is claimed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
