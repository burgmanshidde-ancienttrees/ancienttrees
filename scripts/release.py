#!/usr/bin/env python3
"""Build the archive TestFlight should get, from code that is actually current.

WHY THIS EXISTS. On 2026-08-30 build 4 reached Hidde's phone without the splash
screen, without the photograph band above Discover, and without the line under
"Build your tree collection". Nothing was broken: all three had landed the
evening before and the archive was made from a checkout that had not pulled.
A release build of the same code carries all four hero photographs.

Xcode archives what is on the disk. The machine pushes all day. Those two facts
meet every time somebody clicks Archive, and "remember to pull" is an
instruction that had already failed twice by then.

So this is the sequence, in the order that cannot be got wrong:

    1. refuse a dirty ios/ working tree
    2. refuse a checkout behind origin/main, and say by how much
    3. refresh the bundled catalogue, which is a documented release step
    4. raise the build number, so the upload cannot collide with the last one
    5. run the tests that need no simulator time
    6. archive into the Organizer, where Distribute App can reach it

It stops at the archive on purpose. Uploading is Hidde's: it is his account,
his name on the listing, and the one step that reaches Apple.

    python3 scripts/release.py            # check, build, archive
    python3 scripts/release.py --check    # only say whether we are current
"""

import argparse
import json
import datetime
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = os.path.join(ROOT, "ios", "AncientTrees", "AncientTrees.xcodeproj")
PBX = os.path.join(PROJECT, "project.pbxproj")


def sh(*args, **kw):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, **kw)


def die(msg, fix=None):
    print("STOP: " + msg)
    if fix:
        print("      " + fix)
    sys.exit(1)


def check_current():
    dirty = sh("git", "status", "--porcelain", "--", "ios/").stdout.strip()
    if dirty:
        die("ios/ has uncommitted changes, so the archive would not match any commit.",
            "commit or stash them first:\n" + dirty[:400])

    sh("git", "fetch", "-q", "origin", "main")
    behind = sh("git", "rev-list", "--count", "HEAD..origin/main").stdout.strip()
    ahead = sh("git", "rev-list", "--count", "origin/main..HEAD").stdout.strip()
    if behind and behind != "0":
        missing = sh("git", "log", "--oneline", "-8", "HEAD..origin/main").stdout
        die(f"this checkout is {behind} commit(s) behind origin/main, which is exactly "
            f"how build 4 shipped without its splash screen.",
            "run `git pull` and try again. What you would be missing:\n" + missing)
    if ahead and ahead != "0":
        print(f"note: {ahead} commit(s) here are not pushed yet. Archiving them is fine, "
              f"but nothing else can reproduce this build until you push.")
    head = sh("git", "log", "--format=%h %s", "-1").stdout.strip()
    print(f"current with origin/main: {head}")
    return head


def uploaded_build():
    """The highest build App Store Connect already holds, or None.

    The docstring below used to say there was no way to ask. There is now: an
    API key landed on 2026-09-03 for asc_downloads.py, and this is the same
    read-only gear under hard rule 5's carve-out. It matters because the guess
    was already wrong on 2026-09-04: the project file said 8 while App Store
    Connect held 9, so the next archive would have been another build 9 and the
    upload would have been refused after the whole archive was made.

    Silent about a missing key on purpose. Somebody without the credentials
    still gets the old behaviour and the old warning, rather than a stop.
    """
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from asc_auth import bearer_token
        import urllib.request

        token = bearer_token()
        url = ("https://api.appstoreconnect.apple.com/v1/builds"
               "?filter[app]=6806177833&limit=20&sort=-uploadedDate")
        req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token})
        with urllib.request.urlopen(req, timeout=25) as r:
            data = json.load(r)
        nums = [int(b["attributes"]["version"]) for b in data.get("data", [])
                if str(b.get("attributes", {}).get("version", "")).isdigit()]
        return max(nums) if nums else None
    except Exception as exc:
        print(f"note: could not ask App Store Connect for the last build ({exc.__class__.__name__}). "
              f"Falling back to the project file's number.")
        return None


def bump_build(explicit=None):
    """Raise the build number past everything Apple already has.

    The project file is not the record of what has been UPLOADED. Xcode's
    "Manage Version and Build Number" increments at distribution time and does
    not write back here, so the file said 2 while TestFlight already held 4, and
    the first run of this script produced a build 3 that App Store Connect would
    have refused as lower than one it already had (2026-08-30). It happened
    again on 2026-09-04, file at 8 against Apple's 9.

    So the number comes from Apple when it can, from the file plus one when it
    cannot, and from --build N when somebody says so.
    """
    with open(PBX, encoding="utf-8") as fh:
        src = fh.read()
    found = sorted({int(m) for m in re.findall(r"CURRENT_PROJECT_VERSION = (\d+);", src)})
    if not found:
        die("no CURRENT_PROJECT_VERSION in the project file.")
    if explicit is not None:
        nxt = explicit
    else:
        live = uploaded_build()
        if live is not None:
            nxt = max(found[-1], live) + 1
            print(f"App Store Connect holds build {live}; this project file says {found[-1]}.")
        else:
            nxt = found[-1] + 1
            print("note: this is the project file's number plus one. If TestFlight already "
                  "holds a higher build, pass --build N; Xcode's own increment does not "
                  "write back here.")
    src = re.sub(r"CURRENT_PROJECT_VERSION = \d+;",
                 f"CURRENT_PROJECT_VERSION = {nxt};", src)
    with open(PBX, "w", encoding="utf-8") as fh:
        fh.write(src)
    print(f"build number {found[-1]} -> {nxt}")
    return nxt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="only report whether this checkout is current")
    ap.add_argument("--build", type=int,
                    help="the build number to use, when TestFlight is ahead of the "
                         "project file (Xcode's own increment does not write back)")
    args = ap.parse_args()

    head = check_current()
    if args.check:
        return 0

    print("\nrefreshing the bundled catalogue")
    r = sh(sys.executable, "scripts/appdata.py")
    print("  " + (r.stdout.strip().splitlines() or ["(nothing to do)"])[-1])

    build = bump_build(args.build)

    print("\nrunning the tests that need no simulator time")
    r = subprocess.run(
        ["xcodebuild", "test", "-project", PROJECT, "-scheme", "AncientTrees",
         "-destination", "platform=iOS Simulator,name=iPhone 17",
         "-only-testing:AncientTreesTests", "CODE_SIGNING_ALLOWED=NO"],
        cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        fails = [l for l in r.stdout.splitlines() if "failed" in l.lower()][:6]
        die("the unit tests failed, so this build is not going anywhere.",
            "\n".join(fails) or "read the log with the same command by hand")
    print("  tests pass")

    day = datetime.date.today().isoformat()
    dest = os.path.expanduser(f"~/Library/Developer/Xcode/Archives/{day}")
    os.makedirs(dest, exist_ok=True)
    path = os.path.join(dest, f"AncientTrees build {build}.xcarchive")
    print(f"\narchiving to {path}")
    r = subprocess.run(
        ["xcodebuild", "-project", PROJECT, "-scheme", "AncientTrees",
         "-configuration", "Release", "-destination", "generic/platform=iOS",
         "-archivePath", path, "archive", "-allowProvisioningUpdates"],
        cwd=ROOT, capture_output=True, text=True)
    if "** ARCHIVE SUCCEEDED **" not in r.stdout:
        errs = [l for l in r.stdout.splitlines() if "error:" in l][:6]
        die("the archive failed.", "\n".join(errs) or r.stderr[-500:])

    app = os.path.join(path, "Products", "Applications", "AncientTrees.app")
    heroes = len([f for f in os.listdir(app) if f.startswith("hero-")]) if os.path.isdir(app) else 0
    print(f"  archived. {heroes} hero photographs in the bundle"
          + (" <- ZERO, the splash and the Discover band will be blank" if not heroes else ""))

    print(f"""
Build {build} is in your Organizer, from {head}.

  Window -> Organizer -> Archives -> Distribute App -> App Store Connect

Uploading is yours: it is your account and the one step that reaches Apple.""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
