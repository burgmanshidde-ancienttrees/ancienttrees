#!/usr/bin/env python3
"""Refresh the catalogue the app ships with.

Found 2026-08-24: the app's city screen said Amsterdam has 2 walks while the
website said 3, and the same walk carried 14 trees in one and 9 in the other.
Neither was computing anything wrong. The app was reading the copy bundled in
ios/AncientTrees/AncientTrees/Data/, which was FIVE DAYS old and 48 walks
behind, and nothing in this repo has ever regenerated it.

The bundled copy is deliberately a floor rather than a cache: a fresh install on
a plane still opens. So it does not have to be current to the hour. It does have
to be bounded, and "whenever somebody remembers" is not a bound, which is why
this is a command and not a note.

    python3 scripts/appdata.py            # refresh, print what moved
    python3 scripts/appdata.py --check    # say how stale it is, change nothing

Run it before a release build. A running app catches up by itself on launch;
only a fresh install reads this, which is exactly the moment somebody decides
whether the thing is any good.
"""
import argparse
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "ios" / "AncientTrees" / "AncientTrees" / "Data"
BASE = "https://ancienttrees.app/api"
FEEDS = ["trees", "walks", "species", "browse"]


def fetch(name):
    with urllib.request.urlopen(f"{BASE}/{name}.json", timeout=60) as r:
        return r.read()


def counted(raw):
    """A number worth printing, whatever shape the feed is."""
    try:
        d = json.loads(raw)
    except Exception:
        return None, None
    if isinstance(d, dict):
        for key in ("count", "trees", "walks", "species", "cities"):
            v = d.get(key)
            if isinstance(v, int):
                return v, d.get("version")
            if isinstance(v, list):
                return len(v), d.get("version")
        return None, d.get("version")
    if isinstance(d, list):
        return len(d), None
    return None, None


MODELS = ROOT / "ios" / "AncientTrees" / "AncientTrees" / "Kit" / "Models.swift"
# `public let name: String` yes, `public let name: String?` no, and the raw
# form `let nameRaw: String?` carries its json key on the CodingKeys line.
DEMANDS = re.compile(r"^\s*(?:public\s+)?let\s+(\w+)\s*:\s*(String|Int|Double|Bool)\s*$",
                     re.M)
KEYMAP = re.compile(r"case\s+(\w+)\s*=\s*\"([^\"]+)\"")


def verify():
    """Every field the app REFUSES to see as null, checked against the feed.

    Written 2026-08-24 after the whole catalogue stopped decoding on one null:
    45 trees carry no neighbourhood and 59 no transport, the model declared
    both as plain String, and Codable rejects the entire file over the first
    one. Live installs would have silently stopped updating and a fresh install
    showed an error screen instead of a map. Nobody had seen it because the
    bundled copy was five days old, so the staleness was hiding the breakage.

    A regex over Swift is a blunt instrument and it is the right size here: it
    only has to answer which names the model will not accept as null.
    """
    src = MODELS.read_text(encoding="utf-8")
    swift_to_json = dict(KEYMAP.findall(src))
    required = set()
    for name, _kind in DEMANDS.findall(src):
        required.add(swift_to_json.get(name, name))

    problems = []
    for name in FEEDS:
        try:
            raw = fetch(name)
        except Exception as e:
            print("%s: could not fetch (%s)" % (name, e))
            continue
        d = json.loads(raw)
        rows = None
        if isinstance(d, dict):
            for key in ("trees", "walks", "species", "cities"):
                if isinstance(d.get(key), list):
                    rows = d[key]
                    break
        elif isinstance(d, list):
            rows = d
        if not rows:
            continue
        hits = {}
        for row in rows:
            if not isinstance(row, dict):
                continue
            for k, v in row.items():
                if v is None and k in required:
                    hits[k] = hits.get(k, 0) + 1
        for k, n in sorted(hits.items()):
            problems.append("%s.%s is null on %d row(s), and the app declares "
                            "it non-optional" % (name, k, n))

    for p in problems:
        print("BREAKS THE APP: " + p)
    if not problems:
        print("every field the app demands is present on every row.")
    return 1 if problems else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="report drift without writing")
    ap.add_argument("--verify", action="store_true",
                    help="check the live feed against what the app's model demands")
    args = ap.parse_args()
    if args.verify:
        return verify()

    drift = 0
    for name in FEEDS:
        path = DATA / f"{name}.json"
        old = path.read_bytes() if path.exists() else b""
        try:
            new = fetch(name)
        except Exception as e:
            print(f"{name}: could not fetch ({e})")
            continue
        n_old, v_old = counted(old)
        n_new, v_new = counted(new)
        same = old == new
        if same:
            print(f"{name}: current ({n_new})")
            continue
        drift += 1
        moved = ""
        if n_old is not None and n_new is not None and n_old != n_new:
            moved = f", {n_old} to {n_new}"
        print(f"{name}: STALE{moved}" + ("" if args.check else " -> written"))
        if not args.check:
            path.write_bytes(new)

    if args.check and drift:
        print(f"\n{drift} of {len(FEEDS)} bundled feeds are behind the live site.")
        print("python3 scripts/appdata.py   # refresh them")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
