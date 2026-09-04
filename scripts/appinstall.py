#!/usr/bin/env python3
"""Build THIS checkout and put it on a simulator. One command, no path-picking.

WHY THIS EXISTS. On 2026-09-04 I spent half an hour testing a bug report
against a build from 25 August, because I picked a DerivedData folder by hand
out of the fourteen this project has accumulated and sorted them by clock time
without the date. Every conclusion from that test was worthless, including
"the button works", which is the one thing Hidde needed to be true or false.

Xcode's derived-data path is a hash nobody should be reading. So this builds
into `out/dd`, inside the repository, where there is exactly one, and installs
what it just built rather than what it found.

    python3 scripts/appinstall.py                 # build, install, launch
    python3 scripts/appinstall.py --args -signed-in -at=
    python3 scripts/appinstall.py --device "iPhone 17"

It boots the simulator if it has to, and it prints the build's own timestamp
before launching, so a stale binary announces itself instead of being assumed.
"""
import argparse
import os
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECT = ROOT / "ios" / "AncientTrees"
DD = ROOT / "out" / "dd"
BUNDLE = "app.ancienttrees.AncientTrees"


def sh(*cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def booted_or_boot(name_or_id):
    out = sh("xcrun", "simctl", "list", "devices", "available").stdout
    udid, booted = None, False
    for line in out.splitlines():
        if name_or_id in line and "(" in line:
            parts = line.strip().split("(")
            if len(parts) >= 2:
                udid = parts[1].split(")")[0]
                booted = "Booted" in line
                break
    if not udid:
        sys.exit(f"no simulator matching {name_or_id!r}. `xcrun simctl list devices` shows what there is.")
    if not booted:
        print(f"booting {name_or_id}")
        sh("xcrun", "simctl", "boot", udid)
        time.sleep(8)
    return udid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="iPhone 17")
    ap.add_argument("--args", nargs=argparse.REMAINDER, default=[],
                    help="launch arguments passed to the app, e.g. -signed-in -at=")
    a = ap.parse_args()

    udid = booted_or_boot(a.device)
    print("building this checkout")
    # The DEFAULT derived-data path, and then xcodebuild is ASKED where it put
    # the thing. Forcing a path of our own broke code signing, and picking one
    # by hand out of the fourteen folders Xcode has accumulated is the mistake
    # this whole file exists to prevent.
    r = subprocess.run(
        ["xcodebuild", "-scheme", "AncientTrees",
         "-destination", f"id={udid}", "build"],
        cwd=PROJECT, capture_output=True, text=True)
    if r.returncode != 0:
        for line in (r.stdout + r.stderr).splitlines():
            if ": error:" in line or "failed with a nonzero" in line:
                print(line)
        sys.exit("BUILD FAILED")

    settings = subprocess.run(
        ["xcodebuild", "-scheme", "AncientTrees",
         "-destination", f"id={udid}", "-showBuildSettings", "build"],
        cwd=PROJECT, capture_output=True, text=True).stdout
    built = next((l.split("=", 1)[1].strip() for l in settings.splitlines()
                  if l.strip().startswith("TARGET_BUILD_DIR")), None)
    if not built:
        sys.exit("xcodebuild would not say where it built.")
    app = pathlib.Path(built) / "AncientTrees.app"
    if not app.exists():
        sys.exit(f"built, but no app at {app}")
    stamp = time.strftime("%Y-%m-%d %H:%M:%S",
                          time.localtime(os.path.getmtime(app / "AncientTrees")))
    print(f"built  {stamp}")

    sh("xcrun", "simctl", "terminate", udid, BUNDLE)
    r = sh("xcrun", "simctl", "install", udid, str(app))
    if r.returncode != 0:
        sys.exit(r.stderr.strip() or "install failed")
    r = sh("xcrun", "simctl", "launch", udid, BUNDLE, *a.args)
    print(r.stdout.strip() or r.stderr.strip())
    print(f"running on {a.device} ({udid})")


if __name__ == "__main__":
    main()
