#!/usr/bin/env python3
"""appstore_shots.py - the screenshots App Store Connect asks for.

Apple wants 6.9 inch iPhone screenshots, 1320 by 2868, and reuses them for every
smaller size, so one set is the whole requirement for an iPhone-only app. This
takes them from the simulator at exactly that size and checks the dimensions
before saying it is done, because a set that is one pixel off is refused at
upload with no explanation of which file.

    python3 scripts/appstore_shots.py            # build, boot, shoot
    python3 scripts/appstore_shots.py --no-build

They come out unframed and without captions, which is what a first submission
needs: a plain screenshot is allowed, and a designed frame with marketing copy
over it is a decision about how this app presents itself, which is Hidde's.

WHY THESE FIVE. They are the app's promise in order: the trees near you, one
tree worth crossing town for, the collection you build, the places to browse,
and a city laid out. Apple shows the first three in search results, so the
argument has to be made by then.
"""

import argparse
import os
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUNDLE = "app.ancienttrees.AncientTrees"
DEVICE = "iPhone 17 Pro Max"
WANT = (1320, 2868)
ORIGIN = "-at=52.3731,4.8922"

# name, launch arguments, seconds to wait before the shutter.
# WHAT IS ON THE SCREEN MATTERS AS MUCH AS THE SIZE, and the first version of
# this table got that wrong in three places out of five. It was right about
# every dimension and wrong about every subject, which is exactly the failure
# this script warns about at the end of its own run.
#
# What was wrong, on 2026-08-28, once somebody looked:
#   the tree page opened ams_005, the Cycad of the Hortus, which is a potted
#     plant in a glasshouse behind a paid ticket, and which CLAUDE.md itself
#     names as the thing that is not a tree
#   My trees was headed "test", because the demo session has no name and the
#     app falls back to the local part of its address
#   the city page led with the Heimanseik, whose card is a green panel reading
#     "No photograph yet" at the largest size on the screen
#
# So every subject here is now chosen and the reason is written down, because
# the data moves under it: a tree can lose its photograph, a city can gain one.
SHOTS = [
    # HIS OWN CHOICES, 2026-08-29. He photographed the app on his real phone
    # and sent seven frames back with "deze fotos heb ik gemaakt lijken me
    # beter", and he was right about every one of them. What made them better
    # was not the phone: it was the subjects. Cadiz and Lisbon instead of
    # Amsterdam, because their trees are photographed and their pages open on
    # pictures rather than on empty cards, and the sheet at card height so two
    # trees are visible under the map instead of a list covering it.
    ("1-map", ["-tab=0", "-sheet=card", "-at=36.5366,-6.3010"], 9),
    # The Ficus of Alameda Apodaca rather than S'Ozzastru, which he also chose
    # and which is the better photograph: its page carries a ticket notice, and
    # "you need a ticket" is the wrong promise on the second panel of a store
    # listing. This one is free, outdoors, and the sea is behind it.
    ("2-tree", ["-tab=0", "-open=tree:cad_001", "-at=36.5366,-6.3010"], 7),
    ("3-city", ["-tab=0", "-open=city:lisbon"], 8),
    ("4-discover", ["-tab=1"], 6),
    ("5-my-trees", ["-tab=2", "-signed-in", "-as=Hidde",
                    "-collected=cad_001,cad_002,cad_003",
                    "-at=36.5366,-6.3010"], 7),
    # The one panel that shows what a person DOES rather than what we hold, and
    # the only one he had that I could not make: it was not in the list.
    ("6-add", ["-tab=1", "-collect"], 6),
]


def sh(*args, check=True):
    return subprocess.run(args, capture_output=True, text=True, check=check)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-build", action="store_true")
    ap.add_argument("--out", default=str(ROOT / "out" / "appstore"))
    args = ap.parse_args()

    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import appsweep
    from worktree_guard import guard
    guard("taking the App Store screenshots")

    udid = appsweep.udid_for(DEVICE, "com.apple.CoreSimulator.SimDeviceType.iPhone-17-Pro-Max")
    appsweep.boot(udid)
    # Light, ordinary text size: the store is not the place to show either
    # setting off, and a screenshot at accessibility sizes reads as broken.
    sh("xcrun", "simctl", "ui", udid, "appearance", "light", check=False)
    sh("xcrun", "simctl", "ui", udid, "content_size", "medium", check=False)

    # NOT inside the repository. This folder is in iCloud Drive, which stamps
    # every file it manages with a fileprovider attribute, and codesign then
    # refuses the bundle with "resource fork, Finder information, or similar
    # detritus not allowed". Cost twenty minutes to find on 2026-08-27 and it
    # would have cost the same again to anybody who built here.
    dd = pathlib.Path(os.environ.get("CLAUDE_SCRATCHPAD", "/tmp")) / "at-appstore-dd"
    app = dd / "Build/Products/Debug-iphonesimulator/AncientTrees.app"
    if not args.no_build:
        appsweep.build(dd)
    if not app.exists():
        sys.exit(f"no built app at {app}; run without --no-build")
    sh("xcrun", "simctl", "install", udid, str(app))

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    bad = []
    for name, extra, wait in SHOTS:
        sh("xcrun", "simctl", "terminate", udid, BUNDLE, check=False)
        sh("xcrun", "simctl", "launch", udid, BUNDLE, ORIGIN, "-reset-blocks", *extra)
        time.sleep(wait)
        f = out / f"{name}.png"
        sh("xcrun", "simctl", "io", udid, "screenshot", str(f))
        size = sh("sips", "-g", "pixelWidth", "-g", "pixelHeight", str(f)).stdout
        w = int([l for l in size.splitlines() if "pixelWidth" in l][0].split(":")[1])
        h = int([l for l in size.splitlines() if "pixelHeight" in l][0].split(":")[1])
        ok = (w, h) == WANT
        print(f"  {name:12} {w}x{h} {'' if ok else '  WRONG SIZE'}")
        if not ok:
            bad.append(name)

    print(f"\n{len(SHOTS)} screenshots in {out}")
    if bad:
        sys.exit(f"wrong size: {', '.join(bad)}. Apple wants {WANT[0]}x{WANT[1]} for 6.9 inch.")
    print("Every one is 1320x2868, which is what App Store Connect asks for.")
    print("LOOK at them before uploading: a screenshot mid-load is still the right size.")


if __name__ == "__main__":
    main()
