#!/usr/bin/env python3
"""appsweep.py - photograph every screen of the iOS app, on the smallest phone
and on a large one, so nothing ships that nobody has looked at.

Hidde, 2026-08-20: "ik zie zoveel fout gaan op UX gebied uitlijning etc. hoe
zorgen we er voor dat we een process hebben dat je alleen dingen live zet die je
naloopt op dat gebied en dit niet meer voorkomt?"

The honest answer to that was not another rule. The website has four QA layers
and one of them MEASURES whether a page fits a phone; the app had nothing at all
between an edit and his telephone, which is why he found every one of these and
the machine found none. The per-change eyes rule (CLAUDE.md, 2026-08-14) already
said to look at the pixels, and it did not hold for the app, because looking
meant remembering a five-step simctl recipe every single time. This is that
recipe, once, as a command.

    python3 scripts/appsweep.py                 # build, sweep both phones
    python3 scripts/appsweep.py --no-build      # reuse the last build
    python3 scripts/appsweep.py --only tree     # one screen, while iterating

It writes <out>/<device>/<screen>.png and <out>/manifest.json. Looking at the
PNGs is the point and is not automated: a script can prove a button is on the
screen, it cannot tell you the screen is ugly. What IS automated lives in
appfit.py, which measures the mechanical half from the element frames.

WHY THE SMALLEST PHONE. The iPhone SE is 375 points wide, the same width the
website's own fit check uses, and it is where text wraps to a third line and a
row of chips runs off the edge. A layout that survives the SE survives anything.
It is created on demand: the simulator list on this Mac has no SE by default.

WHY LAUNCH ARGUMENTS RATHER THAN TAPS. simctl cannot tap. Every screen in this
app is reachable with -tab, -open, -signin, -paywall, -primer and -contribute,
which is debug scaffolding that exists for exactly this reason. A screen that
cannot be opened by an argument is a screen that ships unseen, so when you add
one, add its argument too.
"""

import argparse
import json
import os
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP_DIR = ROOT / "ios" / "AncientTrees"
DATA = APP_DIR / "AncientTrees" / "Data"
BUNDLE = "app.ancienttrees.AncientTrees"

# The smallest phone Apple still sells a simulator for, and a big one. Two
# widths catch nearly everything: a layout breaks at the narrow end by running
# off the edge, and at the wide end by stranding a control in an ocean of space.
DEVICES = [
    ("iPhone SE (sweep)", "com.apple.CoreSimulator.SimDeviceType.iPhone-SE-3rd-generation"),
    ("iPhone 17 Pro", "com.apple.CoreSimulator.SimDeviceType.iPhone-17-Pro"),
]

# Amsterdam. A fixed origin keeps the sweep off the location dialog (which
# simctl cannot dismiss, and which would then sit over every later screenshot)
# and keeps "near you" showing the same trees from one day to the next.
ORIGIN = "-at=52.3731,4.8922"


def sh(*args, check=True, capture=True):
    return subprocess.run(args, check=check,
                          capture_output=capture, text=True)


def pick_subjects():
    """Real ids out of the bundled feed, chosen for their worst case.

    Hardcoding ids would rot the first time a tree is renamed. Choosing the
    LONGEST name is deliberate: a layout that survives the longest title in the
    catalogue survives the other 1544, and a screenshot of a tree called "Oak"
    proves nothing about the one called "The Amur Cork Trees and Crimean Linden
    of Bernardinai Garden".
    """
    trees = json.loads((DATA / "trees.json").read_text())["trees"]
    walks = json.loads((DATA / "walks.json").read_text())["walks"]
    browse = json.loads((DATA / "browse.json").read_text())

    with_photo = [t for t in trees if t.get("photo")]
    without = [t for t in trees if not t.get("photo")]
    longest = lambda xs: max(xs, key=lambda t: len(t["name"]))

    walk = walks[0]
    return {
        "tree": longest(with_photo)["id"],
        "tree_nophoto": longest(without)["id"],
        "city": trees[0]["city_slug"],
        "species": browse["species"][0]["name"],
        "collection": browse["collections"][0]["slug"],
        "walk": f'{walk.get("city_slug") or walk.get("city")}|{walk["name"]}',
    }


def screens(sub):
    """Every screen, with the arguments that open it and how long it needs.

    The wait is per screen because they are not equal: a tab root is drawn as
    soon as the catalogue is read, while the map has to fetch tiles over the
    network before there is anything worth photographing.
    """
    return [
        ("map",           ["-tab=0"], 7),
        ("explore",       ["-tab=1"], 4),
        ("collect-intro", ["-collect"], 5),
        ("collect-away",  ["-collect", "-at=52.03,5.91"], 6),
        ("search",        ["-search=lis"], 5),
        ("walk-begin",    ["-begin=amsterdam|Plantage"], 7),
        ("yours",         ["-tab=3"], 4),
        ("profile",       ["-tab=3", "-open=profile:x"], 5),
        ("tree",          ["-tab=0", f'-open=tree:{sub["tree"]}'], 6),
        ("tree-nophoto",  ["-tab=0", f'-open=tree:{sub["tree_nophoto"]}'], 5),
        ("city",          ["-tab=0", f'-open=city:{sub["city"]}'], 5),
        ("species",       ["-tab=0", f'-open=species:{sub["species"]}'], 5),
        ("collection",    ["-tab=0", f'-open=collection:{sub["collection"]}'], 5),
        ("walk",          ["-tab=0", f'-open=walk:{sub["walk"]}'], 7),
        ("signin",        ["-tab=0", "-signin"], 5),
        ("paywall",       ["-tab=0", "-paywall"], 5),
        ("primer",        ["-tab=0", "-primer"], 5),
        ("contribute",    ["-tab=4", "-contribute"], 5),
    ]


def udid_for(name, devicetype):
    out = sh("xcrun", "simctl", "list", "devices", "-j").stdout
    for runtime, devices in json.loads(out)["devices"].items():
        for d in devices:
            if d["name"] == name and d.get("isAvailable"):
                return d["udid"]
    print(f"  creating {name}")
    return sh("xcrun", "simctl", "create", name, devicetype).stdout.strip()


def boot(udid):
    state = json.loads(sh("xcrun", "simctl", "list", "devices", "-j").stdout)
    for devices in state["devices"].values():
        for d in devices:
            if d["udid"] == udid and d["state"] == "Booted":
                return
    sh("xcrun", "simctl", "boot", udid, check=False)
    sh("xcrun", "simctl", "bootstatus", udid, check=False, capture=False)


def build(dd):
    # Refuses when another session is live in this checkout; silent otherwise.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from worktree_guard import guard
    guard("building the app")
    print("building")
    r = subprocess.run(
        ["xcodebuild", "-scheme", "AncientTrees",
         "-destination", "platform=iOS Simulator,name=iPhone 17 Pro",
         "-derivedDataPath", str(dd), "build"],
        cwd=APP_DIR, capture_output=True, text=True)
    if r.returncode != 0:
        # The interesting lines are the errors, not the 3000 lines of compile.
        for line in r.stdout.splitlines():
            if "error:" in line or "BUILD FAILED" in line:
                print("  " + line)
        sys.exit("build failed")
    print("  ok")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None, help="where the PNGs go")
    ap.add_argument("--no-build", action="store_true")
    ap.add_argument("--only", default=None, help="one screen name")
    ap.add_argument("--device", default=None, help="one device name")
    args = ap.parse_args()

    scratch = os.environ.get("CLAUDE_SCRATCHPAD", "/tmp")
    out = pathlib.Path(args.out or f"{scratch}/appsweep")
    dd = pathlib.Path(scratch) / "dd"
    out.mkdir(parents=True, exist_ok=True)

    if not args.no_build:
        build(dd)
    app = dd / "Build/Products/Debug-iphonesimulator/AncientTrees.app"
    if not app.exists():
        sys.exit(f"no build at {app}; run without --no-build")

    sub = pick_subjects()
    plan = [s for s in screens(sub) if not args.only or s[0] == args.only]
    devices = [d for d in DEVICES if not args.device or d[0] == args.device]

    manifest = {"subjects": sub, "shots": []}
    for name, devicetype in devices:
        udid = udid_for(name, devicetype)
        slug = name.replace(" ", "-").replace("(", "").replace(")", "")
        print(f"\n{name}")
        boot(udid)
        sh("xcrun", "simctl", "install", udid, str(app))
        (out / slug).mkdir(exist_ok=True)

        for screen, extra, wait in plan:
            sh("xcrun", "simctl", "terminate", udid, BUNDLE, check=False)
            sh("xcrun", "simctl", "launch", udid, BUNDLE, ORIGIN, *extra)
            time.sleep(wait)
            path = out / slug / f"{screen}.png"
            sh("xcrun", "simctl", "io", udid, "screenshot", "--type=png", str(path))
            print(f"  {screen:<14} {path.stat().st_size // 1024} KB")
            manifest["shots"].append({"device": name, "screen": screen,
                                      "args": extra, "path": str(path)})

    (out / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"\n{len(manifest['shots'])} screenshots in {out}")
    print("Now LOOK at them. That is the point of the command.")


if __name__ == "__main__":
    main()
