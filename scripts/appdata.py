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


def fetch(name, source=None):
    """The feed's bytes, from the live site or from a local build of it.

    `source` exists because the sandbox a session runs in cannot reach
    ancienttrees.app (the proxy answers 403), so the one machine that always
    knows what the site publishes could not write the bundle. A local
    `npx astro build` emits exactly the same endpoints under site/dist/api,
    which is the SAME artefact the deploy uploads rather than a second
    implementation of the contract.
    """
    if source:
        return (pathlib.Path(source) / f"{name}.json").read_bytes()
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


def verify(source=None):
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
            raw = fetch(name, source)
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


def local_drift():
    """How far behind the bundled catalogue is, WITHOUT touching the network.

    --check asks the live feed, which is the honest question and needs four
    fetches and seven megabytes, and it answers nothing at all from a sandbox
    whose proxy does not allow ancienttrees.app. Neither is a thing a session
    brief can do on every start.

    This asks the cheap version of the same question: how many trees does this
    checkout publish, and how many did the copy inside the app binary have. The
    two only differ because the bundle is written at RELEASE time (release.py
    step 3) while the machine adds trees all day, so the number is the drift
    since the last archive.

    Worth being clear about what it is not: it is not the app showing old data.
    A running app replaces this on launch, and the bundle is the floor for a
    fresh install and for a phone with no signal. It is what somebody meets in
    the first seconds, which is also the moment they decide whether the thing
    is any good, and it is what you get if you press Run in Xcode rather than
    going through release.py.
    """
    path = DATA / "trees.json"
    if not path.exists():
        return None, None
    try:
        bundled = json.loads(path.read_text())
    except Exception:
        return None, None
    have = bundled.get("count")
    if not isinstance(have, int):
        have = len(bundled.get("trees") or [])
    published = 0
    for city in sorted((ROOT / "data" / "cities").glob("*.json")):
        try:
            published += len(json.loads(city.read_text()).get("trees") or [])
        except Exception:
            continue
    return have, published


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="report drift without writing")
    ap.add_argument("--verify", action="store_true",
                    help="check the live feed against what the app's model demands")
    ap.add_argument("--local", action="store_true",
                    help="drift against this checkout's own data, no network")
    ap.add_argument("--from", dest="source", metavar="DIR",
                    help="read the feeds from a local build (site/dist/api) "
                         "instead of the live site")
    args = ap.parse_args()
    if args.verify:
        # --from works here too: the question is whether the app's decoder
        # survives these bytes, and a local build's bytes are the bytes that
        # ship. Verifying the bundle I just wrote is the point.
        return verify(args.source)
    if args.local:
        have, published = local_drift()
        if have is None or published is None:
            print("bundled catalogue: cannot be read")
            return 0
        print("bundled catalogue: %d trees, this checkout publishes %d, "
              "%d behind" % (have, published, published - have))
        return 0

    if args.source:
        missing = [n for n in FEEDS
                   if not (pathlib.Path(args.source) / f"{n}.json").exists()]
        if missing:
            print("that build has no %s: run `npx astro build` in site/ first"
                  % ", ".join(f"{n}.json" for n in missing))
            return 1
        print("reading the feeds from %s (a local build, not the live site)\n"
              % args.source)

    # The live site can be BEHIND this checkout: the machine commits trees and
    # the deploy takes minutes. Refreshing from it then writes an older bundle
    # over a newer one, which checkouts.py --fix did on 2026-09-25 (3374 trees
    # to 3348, while the deploy of the newer data was still running). So a
    # live trees feed smaller than what this checkout publishes is refused.
    if not args.source and not args.check:
        _, published = local_drift()
        try:
            n_live, _ = counted(fetch("trees", None))
        except Exception:
            n_live = None
        if published and n_live is not None and n_live < published:
            print("the live site publishes %d trees and this checkout %d, so it "
                  "has not deployed yet; nothing written." % (n_live, published))
            print("Wait for the deploy, or read a local build:")
            print("  cd site && npx astro build && cd .. && "
                  "python3 scripts/appdata.py --from site/dist/api")
            return 1

    drift = 0
    unreachable = []
    for name in FEEDS:
        path = DATA / f"{name}.json"
        old = path.read_bytes() if path.exists() else b""
        try:
            new = fetch(name, args.source)
        except Exception as e:
            # A feed that cannot be fetched used to print one line and leave
            # exit 0 behind, so release.py printed "could not fetch" as its
            # progress message and archived anyway: an upload with whatever
            # bundle the last release left, silently. Failing here is the
            # whole point of a release step.
            print(f"{name}: could not fetch ({e})")
            unreachable.append(name)
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
    if unreachable:
        print("\n%d of %d feeds could not be read, so the bundle is whatever "
              "the last refresh left." % (len(unreachable), len(FEEDS)))
        print("A local build answers the same question without the network:")
        print("  cd site && npx astro build && cd .. && "
              "python3 scripts/appdata.py --from site/dist/api")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
