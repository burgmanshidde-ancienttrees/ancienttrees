#!/usr/bin/env python3
"""play_shots.py - the phone screenshots Google Play asks for, from the release build.

Play takes 2 to 8 phone screenshots with sides between 320 and 3840 px and the
long side at most twice the short one; 1080 by 1920 (9:16) also qualifies for
Play's larger placements. A phone emulator is 1080 by 2400, past the 2:1 limit,
so the screen is set to 1080x1920 for the shots and set back afterwards.

The scenes are the iPhone listing's (scripts/appstore_shots.py, his choices of
2026-08-29 and 2026-10-14): the map in Rome, the Ficus of Alameda Apodaca in
Cadiz (free, outdoors, the sea behind it), Barcelona (no ambassador's name on
it), and Discover. Signed out, real trees. The release build reads no launch
arguments, so each scene is reached the way a person reaches it: the emulator's
position set with `geo fix`, and the website's own links (/open?tree=,
/open?city=, WebLink.kt) handed to the app.

    python3 scripts/android_release.py --apk     # first, for the apk
    python3 scripts/play_shots.py                # into out/play/phone-*.png
Takes the emulator lock.
"""
import pathlib
import subprocess
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from emulator_lock import emulator  # noqa: E402
from android_release_walk import adb, tap_text, PKG  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out" / "play"
ACTIVITY = PKG + "/app.ancienttrees.MainActivity"

# name, (lat, lng), link or tab label, seconds to wait
SCENES = [
    ("phone-1-map", (41.8967, 12.4822), "tap:Back to my location", 12),
    ("phone-2-tree", (36.5366, -6.3010), "https://ancienttrees.app/open?tree=cad_001", 14),
    ("phone-3-city", (41.3874, 2.1686), "https://ancienttrees.app/open?city=barcelona", 18),
    ("phone-4-discover", (41.8967, 12.4822), "tab:Discover", 14),
]


def geo(lat, lng):
    # The console's geo fix takes longitude first.
    adb("emu", "geo", "fix", str(lng), str(lat))


def main():
    from PIL import Image
    apks = sorted(OUT.glob("ancient-trees-*.apk"), key=lambda p: p.stat().st_mtime)
    if not apks:
        sys.exit("no release apk: run android_release.py --apk first")
    with emulator("play_shots"):
        adb("uninstall", PKG)
        if adb("install", "-r", str(apks[-1])).returncode:
            sys.exit("install failed")
        adb("shell", "pm", "grant", PKG, "android.permission.ACCESS_FINE_LOCATION")
        adb("shell", "pm", "grant", PKG, "android.permission.ACCESS_COARSE_LOCATION")
        adb("shell", "wm", "size", "1080x1920")
        try:
            for name, (lat, lng), how, wait in SCENES:
                adb("shell", "am", "force-stop", PKG)
                geo(lat, lng)
                time.sleep(2)
                if how and how.startswith("https://"):
                    adb("shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", how, "-n", ACTIVITY)
                else:
                    adb("shell", "monkey", "-p", PKG, "-c", "android.intent.category.LAUNCHER", "1")
                    if how and how.startswith(("tab:", "tap:")):
                        time.sleep(12)
                        # The map keeps where it last looked; the arrow brings it to the new position.
                        tap_text(how.partition(":")[2])
                time.sleep(wait)
                path = OUT / f"{name}.png"
                with open(path, "wb") as f:
                    subprocess.run([str(pathlib.Path.home() / "Library/Android/sdk/platform-tools/adb"),
                                    "exec-out", "screencap", "-p"], stdout=f)
                size = Image.open(path).size
                ok = size == (1080, 1920)
                print(f"{path.relative_to(ROOT)} {size[0]}x{size[1]}" + ("" if ok else "  WRONG SIZE"))
        finally:
            adb("shell", "wm", "size", "reset")


if __name__ == "__main__":
    main()
