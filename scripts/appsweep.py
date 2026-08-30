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
import re
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
    plan = [
        ("map",           ["-tab=0"], 7),
        ("map-full",      ["-tab=0", "-sheet=full"], 7),
        ("explore",       ["-tab=1"], 4),
        ("collect-intro", ["-collect"], 5),
        ("collect-away",  ["-collect", "-at=52.03,5.91"], 6),
        # The step a photograph with no location of its own leads to. 8, like
        # place-pin: it is a map and it has tiles to fetch.
        ("collect-place", ["-collect", "-collect-place"], 8),
        ("search",        ["-search=lis"], 5),
        # 12, not 7. This walk has no cached route, so since 2026-08-25 it
        # asks Valhalla for one before the line can be drawn, and on the SE the
        # old wait photographed a white screen. A blank screenshot in this
        # folder is worse than a slow sweep: somebody goes looking for a bug
        # that is a stopwatch.
        ("walk-begin",    ["-begin=amsterdam|Plantage"], 12),
        # Tab 3 is the Collection and tab 4 is Profile since 2026-08-24, when
        # the bar went to five slots so the camera could have a middle.
        #
        # "collection-tab", not "collection". This entry and the curated
        # collection PAGE below it were both called "collection" from the day
        # the tab was renamed, and since the file is named after the screen the
        # second one silently overwrote the first: the Collection tab, which is
        # where the cards and the lane picker live, had not been photographed
        # once. Two screens with one name is the same failure as a screen no
        # argument can open, and the check below now refuses it.
        ("collection-tab", ["-tab=2"], 4),
        ("profile",       ["-tab=2", "-settings"], 5),
        ("tree",          ["-tab=0", f'-open=tree:{sub["tree"]}'], 6),
        ("tree-nophoto",  ["-tab=0", f'-open=tree:{sub["tree_nophoto"]}'], 5),
        ("city",          ["-tab=0", f'-open=city:{sub["city"]}'], 5),
        ("city-map",      ["-tab=0", f'-open=citymap:{sub["city"]}'], 7),
        ("species",       ["-tab=0", f'-open=species:{sub["species"]}'], 5),
        ("collection",    ["-tab=0", f'-open=collection:{sub["collection"]}'], 5),
        ("walk",          ["-tab=0", f'-open=walk:{sub["walk"]}'], 7),
        ("place-pin",     ["-tab=0", f'-open=tree:{sub["tree"]}', "-placepin"], 8),
        ("species-pick",  ["-tab=0", f'-open=tree:{sub["tree"]}', "-speciespick"], 8),
        # The which-maps-app question, which is a dialog and still a screen:
        # it is the first thing a person meets after tapping Take me there.
        ("directions",    ["-tab=0", "-directions"], 5),
        ("signin",        ["-tab=0", "-signin"], 5),
        ("paywall",       ["-tab=0", "-paywall"], 5),
        ("primer",        ["-tab=0", "-primer"], 5),
        # WITH -settings, because these three sheets are owned by the Settings
        # screen and Settings stopped being the tab: it is pushed from the gear
        # on My trees now. Without it the argument lands on a screen that never
        # reads it, and all three photographed My trees instead, silently, from
        # the day Profile moved (found 2026-08-28).
        ("contribute",    ["-tab=2", "-settings", "-contribute"], 5),
        ("feedback",      ["-tab=2", "-settings", "-feedback"], 5),
        ("profile-edit",  ["-tab=2", "-profile-edit"], 5),
        # WITH ROWS IN IT (-people-demo), because an empty list cannot show
        # the report and block controls, and those are the two the App Store
        # checks by tapping.
        ("people",        ["-tab=2", "-signed-in", "-people", "-people-demo"], 5),
    ]
    names = [p[0] for p in plan]
    dupes = sorted({n for n in names if names.count(n) > 1})
    if dupes:
        # Not a warning. The output file is named after the screen, so a
        # duplicate name means one of the two screens is never looked at while
        # the folder still shows a picture with its name on it.
        raise SystemExit("appsweep: two screens share a name, so one is never "
                         "photographed: " + ", ".join(dupes))
    return plan


def udid_for(name, devicetype):
    out = sh("xcrun", "simctl", "list", "devices", "-j").stdout
    for runtime, devices in json.loads(out)["devices"].items():
        for d in devices:
            if d["name"] == name and d.get("isAvailable"):
                return d["udid"]
    print(f"  creating {name}")
    return sh("xcrun", "simctl", "create", name, devicetype).stdout.strip()


def booted(udid):
    state = json.loads(sh("xcrun", "simctl", "list", "devices", "-j").stdout)
    for devices in state["devices"].values():
        for d in devices:
            if d["udid"] == udid and d["state"] == "Booted":
                return True
    return False


def boot(udid, patience=180):
    """Boot the device and wait, but never forever.

    `simctl bootstatus` HAS NO TIMEOUT and can wedge on a device that is
    already booted, which is not theoretical: a night run started one at
    00:03 on 2026-08-28 and it was still sitting there at 11:20 the next
    morning, at nought per cent CPU, holding the build lock. Every app build
    on this machine had been refused for eleven hours and nothing said so,
    because the guard that refused them was doing its job correctly.

    Two of them were waiting on the same device by then, which is how the
    wedge is usually reached in the first place.

    So: ask bootstatus, with a deadline, and then ask the device itself. The
    list command always answers, and a device that reports Booted IS booted
    whatever bootstatus has decided to do about it. This is the same rule
    CLAUDE.md already sets for fetching: a hang costs a whole window, a
    refusal costs a second, so everything that can hang gets a deadline.
    """
    if booted(udid):
        return
    sh("xcrun", "simctl", "boot", udid, check=False)
    try:
        subprocess.run(["xcrun", "simctl", "bootstatus", udid],
                       timeout=patience, capture_output=True)
    except subprocess.TimeoutExpired:
        print(f"  bootstatus did not return in {patience}s, asking the device instead")
    except Exception:
        pass
    if not booted(udid):
        print("  the simulator did not come up; carrying on and letting the "
              "build say so rather than waiting any longer")


def bundled_data_note():
    """Say how far the app's bundled catalogue is behind the live site.

    A NOTE and never a failure: the night runs publish trees daily, so this
    drifts by design and a red build every morning would be noise. It prints
    here because this is the moment somebody is looking at the app, and on
    2026-08-24 that copy was five days and 436 trees behind while a screenshot
    of the city screen quietly disagreed with the website about the same walk.
    """
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import appdata
        drift = []
        for name in appdata.FEEDS:
            path = appdata.DATA / ("%s.json" % name)
            old = path.read_bytes() if path.exists() else b""
            try:
                new = appdata.fetch(name)
            except Exception:
                return
            if old != new:
                n_old, _ = appdata.counted(old)
                n_new, _ = appdata.counted(new)
                drift.append("%s %s->%s" % (name, n_old, n_new))
        if drift:
            print("note: bundled catalogue is behind the live site (%s)"
                  % ", ".join(drift))
            print("      python3 scripts/appdata.py   # a fresh install reads this")
    except Exception:
        pass


SWEEPFRAMES = (ROOT / "ios" / "AncientTrees" / "AncientTreesUITests"
               / "SweepFrames.swift")


def check_lists():
    """The two screen lists must be the same list, and twice they were not.

    CLAUDE.md has said since 2026-08-20 that "the screen list in appsweep.py and
    in SweepFrames.swift are kept the same list", because a screen no argument
    can open is a screen that ships unseen. On 2026-08-25 they disagreed in both
    directions: this file called tab 3 "collection" (which collided with the
    curated collection PAGE and overwrote its photograph) while SweepFrames still
    called it "yours", and this file had a search screen SweepFrames had never
    heard of. So the app was photographing a screen it did not measure and
    measuring a screen under a different name.

    A sentence in a document could not hold that. This can: it reads both lists
    and refuses when they differ.

    Returns a list of complaints, empty when the two agree.
    """
    mine = [p[0] for p in screens(pick_subjects())]
    text = SWEEPFRAMES.read_text(encoding="utf-8")
    # Stop at the line that closes the literal, not at the first "]": the type
    # annotation itself carries two of them.
    after = text.split("private static let screens", 1)[-1]
    lines = []
    for line in after.splitlines()[1:]:
        if line.strip() == "]":
            break
        lines.append(line)
    block = "\n".join(lines)
    theirs = re.findall(r'\(\s*"([a-z0-9-]+)"', block)
    out = []
    for name in mine:
        if name not in theirs:
            out.append(f"appsweep photographs '{name}' and SweepFrames.swift "
                       f"does not measure it")
    for name in theirs:
        if name not in mine:
            out.append(f"SweepFrames.swift measures '{name}' and appsweep does "
                       f"not photograph it")
    return out


def build(dd):
    bundled_data_note()
    # Refuses when another session is live in this checkout; silent otherwise.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from worktree_guard import guard
    guard("building the app")
    print("building")
    # A hard timeout, added 2026-08-30 alongside the identical fix in
    # appfit.py's run_test(): an unguarded xcodebuild call there ran a
    # 110-minute CI job to its own timeout instead of failing in the few
    # minutes a build normally takes. Same shape here, same fix.
    try:
        r = subprocess.run(
            ["xcodebuild", "-scheme", "AncientTrees",
             "-destination", "platform=iOS Simulator,name=iPhone 17 Pro",
             "-derivedDataPath", str(dd), "build"],
            cwd=APP_DIR, capture_output=True, text=True, timeout=1200)
    except subprocess.TimeoutExpired:
        sys.exit("xcodebuild build hung past 20 minutes and was killed")
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
    ap.add_argument("--check-lists", action="store_true",
                    help="only check that appsweep and SweepFrames agree")
    args = ap.parse_args()

    drift = check_lists()
    if drift:
        for d in drift:
            print("  " + d)
        sys.exit("the sweep and the layout gate disagree about which screens exist")
    if args.check_lists:
        print("the sweep and the layout gate agree on every screen")
        return 0

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

    # A NAME THAT MATCHES NOTHING IS A TYPO, NOT AN EMPTY SWEEP.
    #
    # Both filters used to fall through silently, so `--device "iPhone SE"`
    # (the list says "iPhone SE (sweep)") built the whole app, photographed
    # nothing, printed "0 screenshots" and exited 0, with "Now LOOK at them"
    # underneath. In a command whose entire reason to exist is that somebody
    # looks at the output, nought is the loudest possible answer and it was
    # being reported as the quietest.
    if not devices:
        sys.exit("no device called %r. The list is: %s"
                 % (args.device, ", ".join(d[0] for d in DEVICES)))
    if not plan:
        sys.exit("no screen called %r. The list is: %s"
                 % (args.only, ", ".join(s[0] for s in screens(sub))))

    manifest = {"subjects": sub, "shots": []}
    for name, devicetype in devices:
        udid = udid_for(name, devicetype)
        slug = name.replace(" ", "-").replace("(", "").replace(")", "")
        print(f"\n{name}")
        boot(udid)
        sh("xcrun", "simctl", "install", udid, str(app))
        # Wipe the device's folder first. A screen that leaves the sweep list
        # leaves its LAST PNG behind, and a stale screenshot in a folder you
        # are about to judge is worse than a missing one: on 2026-08-25 this
        # directory still held a four-tab "Your trees" screen from a build days
        # old, sitting next to today's five-tab ones. The whole point of this
        # command is that what you look at is what you just built.
        (out / slug).mkdir(exist_ok=True)
        # Only on a FULL sweep. With --only the other screens are not being
        # re-shot, so wiping them would leave one photograph and a claim that
        # the rest do not exist, which is a different way of misleading the
        # person looking (found immediately after adding the wipe).
        if not args.only:
            for stale in (out / slug).glob("*.png"):
                stale.unlink()

        for screen, extra, wait in plan:
            sh("xcrun", "simctl", "terminate", udid, BUNDLE, check=False)
            sh("xcrun", "simctl", "launch", udid, BUNDLE, ORIGIN, "-reset-blocks", *extra)
            time.sleep(wait)
            path = out / slug / f"{screen}.png"
            sh("xcrun", "simctl", "io", udid, "screenshot", "--type=png", str(path))
            print(f"  {screen:<14} {path.stat().st_size // 1024} KB")
            manifest["shots"].append({"device": name, "screen": screen,
                                      "args": extra, "path": str(path)})

    (out / "manifest.json").write_text(json.dumps(manifest, indent=1))
    if not manifest["shots"]:
        sys.exit("the sweep photographed nothing at all, so there is nothing to look at")
    print(f"\n{len(manifest['shots'])} screenshots in {out}")
    print("Now LOOK at them. That is the point of the command.")


if __name__ == "__main__":
    main()
