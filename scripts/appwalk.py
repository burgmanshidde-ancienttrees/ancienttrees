#!/usr/bin/env python3
"""appwalk.py - walk the app's FLOWS with a finger and bring back the frames.

Hidde, 2026-08-27: "hoe kunnen we jou een fatsoenlijke ui en ux test laten doen
dat je alles doorloopt en zelf oordeelt of het werkt zoals conventionele flows
werken".

The gap he is pointing at is real and it has a shape. appsweep.py opens every
screen with a launch argument and photographs it, so every screen in this app is
a FIRST FRAME and no screen is ever arrived at. appfit.py measures those frames.
Neither can see the whole class of fault that only exists between two screens,
and that is where the morning's bugs were: a button asking for a tab that no
longer exists, so tapping your own name in Settings landed on the map with no
bar and no way back.

    python3 scripts/appwalk.py                # build, walk, collect the frames
    python3 scripts/appwalk.py --no-build     # reuse the last build

It runs AncientTreesUITests/FlowWalk, which taps and swipes through each flow,
writes a PNG after every step and asserts ONE thing: that there is always a way
back. Then it copies the pictures here, in order, named flow__NN-step.png, so
the judging is reading a strip of frames.

WHAT IT DOES NOT DO, said plainly so nobody trusts it further than it goes. It
does not judge. Whether a flow matches the convention, whether a control is in
the right place, whether the app feels right: that is a pair of eyes on these
frames, and the eyes are the point. The machine's half is that the frames exist
and that no step ends in a room with no door.
"""

import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP_DIR = ROOT / "ios" / "AncientTrees"
FOLDER = "appwalk"


def run(device_udid, out):
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from worktree_guard import guard
    guard("walking the app's flows")

    device_dir = pathlib.Path.home() / "Library/Developer/CoreSimulator/Devices" / device_udid
    # Clear yesterday's frames out of the container first: the test writes into
    # a clone's temporary directory and a stale file from an earlier run reads
    # as a step that happened today.
    for stale in device_dir.rglob(f"{FOLDER}/*.png"):
        stale.unlink()

    print("walking the flows, this takes a few minutes")
    r = subprocess.run(
        ["xcodebuild", "test",
         "-scheme", "AncientTrees",
         "-destination", f"platform=iOS Simulator,id={device_udid}",
         "-only-testing:AncientTreesUITests/FlowWalk",
         # The clone is thrown away with its files unless this is off, which is
         # the same trap appfit.py records: the test passes and leaves nothing.
         "-parallel-testing-enabled", "NO",
         "CODE_SIGNING_ALLOWED=NO", "CODE_SIGNING_REQUIRED=NO",
         "CODE_SIGN_IDENTITY="],
        cwd=APP_DIR, capture_output=True, text=True)

    frames = sorted(device_dir.rglob(f"{FOLDER}/*.png"))
    if not frames:
        for line in (r.stdout + r.stderr).splitlines():
            if "error:" in line or "TEST FAILED" in line:
                print("  " + line)
        sys.exit("the walk left no frames behind")

    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.png"):
        f.unlink()
    for f in frames:
        shutil.copy2(f, out / f.name)

    # The assertion failures are the machine's half and they belong on the
    # console, not buried in a result bundle nobody opens.
    faults = [l.strip() for l in (r.stdout + r.stderr).splitlines()
              if "XCTAssertTrue failed" in l or "no tab bar" in l]
    print(f"\n{len(frames)} frames in {out}")
    for f in sorted({p.name.split('__')[0] for p in out.glob('*.png')}):
        n = len(list(out.glob(f"{f}__*.png")))
        print(f"  {f}: {n} steps")
    if faults:
        print("\nDEAD ENDS:")
        for f in faults:
            print("  " + f)
        return 1
    print("\nEvery step left a way back. Now LOOK at the frames: the machine "
          "cannot tell you whether the flow is any good.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="iPhone 17 Pro")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import appsweep
    udid = appsweep.udid_for(args.device, dict(appsweep.DEVICES).get(args.device, ""))
    out = pathlib.Path(args.out) if args.out else ROOT / "out" / FOLDER
    sys.exit(run(udid, out))


if __name__ == "__main__":
    main()
