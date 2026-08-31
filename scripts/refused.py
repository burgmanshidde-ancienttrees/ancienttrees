#!/usr/bin/env python3
"""Run the app's tests with permission actually refused.

WHY A SCRIPT RATHER THAN A LAUNCH ARGUMENT. A launch argument would test our
own stand-in for a refusal. This revokes the permission on the simulator, so
the app's real Core Location code takes its real refused branch, which is the
only version of this worth trusting.

Nothing else in this repository ever enters that state: every UI test launches
with -at=, a fixed location that always works. That is the right default for
testing everything else, and it meant the most common real-world state on a
phone had never been entered once.

WHAT A SIMULATOR CANNOT DO, said plainly: it has no camera, so "camera refused"
cannot be reached here at all. That decision is a pure function instead, tested
in MyTreesTests under WhenPermissionIsRefused.

Usage:  python3 scripts/refused.py [--device "iPhone 17" | --udid UDID]
"""

import argparse
import json
import subprocess
import sys

BUNDLE = "app.ancienttrees.AncientTrees"
PROJECT = "ios/AncientTrees/AncientTrees.xcodeproj"


def sh(*args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)


def udid_for(name):
    data = json.loads(sh("xcrun", "simctl", "list", "devices", "-j").stdout)
    for runtime in data.get("devices", {}).values():
        for d in runtime:
            if d.get("name") == name and d.get("isAvailable"):
                return d["udid"]
    return None


def device_label(udid):
    """"iPhone SE (sweep) iOS 18.6", read back from simctl for this udid."""
    data = json.loads(sh("xcrun", "simctl", "list", "devices", "-j").stdout)
    for runtime, devices in data.get("devices", {}).items():
        for d in devices:
            if d["udid"] == udid:
                os_name = runtime.rsplit(".", 1)[-1].replace("iOS-", "iOS ")
                os_name = os_name.replace("-", ".")
                # appsweep's own devices already carry the version in the name,
                # so saying it twice reads as a bug in the reader rather than
                # tidiness in the writer.
                if os_name in d["name"]:
                    return d["name"]
                return f"{d['name']} ({os_name})"
    return None


def privacy(udid, action, service):
    r = sh("xcrun", "simctl", "privacy", udid, action, service, BUNDLE)
    if r.returncode != 0:
        print(f"note: could not {action} {service}: {r.stderr.strip()}")
    return r.returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="iPhone 17")
    # CI already chose a simulator by UDID from what the runner actually has,
    # and asking for one by name there is how an earlier workflow ended up
    # requesting a runtime the machine did not have.
    ap.add_argument("--udid")
    args = ap.parse_args()

    udid = args.udid or udid_for(args.device)
    if not udid:
        print(f"no simulator named {args.device}")
        return 1

    sh("xcrun", "simctl", "boot", udid)

    # The NAME OF THE DEVICE ACTUALLY USED, not the default that --udid
    # overrode. It printed "iPhone 17" while running on an iOS 18.6 SE on
    # 2026-08-31, which is the worst kind of log line in a repository full of
    # checks: one that reports a different thing from the one it measured.
    print(f"refusing location and photos on {device_label(udid) or udid}")
    privacy(udid, "revoke", "location")
    privacy(udid, "revoke", "photos")

    try:
        r = subprocess.run(
            ["xcodebuild", "test",
             "-project", PROJECT, "-scheme", "AncientTrees",
             "-destination", f"id={udid}",
             "-only-testing:AncientTreesUITests/RefusedWalk",
             "-parallel-testing-enabled", "NO",
             "CODE_SIGNING_ALLOWED=NO"],
            capture_output=True, text=True)
    finally:
        # ALWAYS put it back. A simulator left with location refused makes
        # every other test in this repository fail in a way that looks like a
        # bug in the app, which is a debugging afternoon nobody needs.
        print("restoring permissions")
        privacy(udid, "reset", "location")
        privacy(udid, "reset", "photos")

    for line in r.stdout.splitlines():
        if "Test Case" in line and ("passed" in line or "failed" in line):
            print("  " + line.strip())
        if ".swift:" in line and "error:" in line:
            print("  " + line.strip())

    print("PASSED" if r.returncode == 0 else "FAILED")
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
