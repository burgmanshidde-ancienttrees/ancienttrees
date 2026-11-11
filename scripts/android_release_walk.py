#!/usr/bin/env python3
"""android_release_walk.py - the release build (R8 on) opened on the emulator.

R8 renames and strips; a class it removed wrongly shows up only when the screen
that needs it opens. So this installs out/play/<the newest>.apk (made by
`android_release.py --apk`), opens the app signed out, taps every tab and a
tree, and fails on a crash in logcat. Screenshots go to out/play/walk/.
Launch arguments are read only by a debuggable build (LaunchArgs.kt), so the
walk goes by finger, finding each control in the UI Automator tree.

    python3 scripts/android_release_walk.py
Exit 1 on a crash or a control it cannot find. Takes the emulator lock.
"""
import pathlib
import re
import subprocess
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from emulator_lock import emulator  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
ADB = str(pathlib.Path.home() / "Library" / "Android" / "sdk" / "platform-tools" / "adb")
PKG = "app.ancienttrees.android"
OUT = ROOT / "out" / "play" / "walk"


def adb(*a, **kw):
    return subprocess.run([ADB, *a], capture_output=True, text=True, **kw)


def shot(name):
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{name}.png", "wb") as f:
        subprocess.run([ADB, "exec-out", "screencap", "-p"], stdout=f)


def tree():
    adb("shell", "uiautomator", "dump", "/sdcard/w.xml")
    return adb("shell", "cat", "/sdcard/w.xml").stdout


def tap_text(*labels):
    """Tap the first node whose text or content-desc is one of the labels."""
    xml = tree()
    for label in labels:
        for m in re.finditer(r'<node [^>]*>', xml):
            node = m.group(0)
            t = re.search(r' text="([^"]*)"', node).group(1)
            d = re.search(r' content-desc="([^"]*)"', node).group(1)
            if label in (t, d):
                b = re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', node)
                x1, y1, x2, y2 = map(int, b.groups())
                adb("shell", "input", "tap", str((x1 + x2) // 2), str((y1 + y2) // 2))
                return label
    return None


def crashed():
    log = adb("logcat", "-d", "-b", "crash").stdout
    return [l for l in log.splitlines() if PKG in l or "FATAL EXCEPTION" in l]


def main():
    apks = sorted((ROOT / "out" / "play").glob("ancient-trees-*.apk"), key=lambda p: p.stat().st_mtime)
    if not apks:
        sys.exit("no release apk: run android_release.py --apk first")
    apk = apks[-1]
    failures = []
    with emulator("android_release_walk"):
        adb("uninstall", PKG)
        r = adb("install", "-r", str(apk))
        if r.returncode:
            sys.exit("install failed: " + r.stderr)
        # The location question answered beforehand, as most people answer it; the
        # dialog itself is Android's, not ours.
        adb("shell", "pm", "grant", PKG, "android.permission.ACCESS_FINE_LOCATION")
        adb("shell", "pm", "grant", PKG, "android.permission.ACCESS_COARSE_LOCATION")
        adb("logcat", "-c", "-b", "all")
        adb("shell", "monkey", "-p", PKG, "-c", "android.intent.category.LAUNCHER", "1")
        time.sleep(12)
        shot("1-map")
        for i, labels in enumerate([("Discover",), ("My trees", "Profile", "You"), ("Map", "Explore")], start=2):
            hit = tap_text(*labels)
            time.sleep(5)
            shot(f"{i}-{(hit or labels[0]).lower().replace(' ', '-')}")
            print(("tapped " + hit) if hit else ("could not find " + "/".join(labels)))
            if not hit:
                failures.append("/".join(labels))
        # A tree from Discover: the first tile under "At their best now".
        tap_text("Discover")
        time.sleep(4)
        xml = tree()
        tiles = [m for m in re.finditer(r'<node [^>]*clickable="true"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', xml)]
        big = [t for t in tiles if (int(t.group(3)) - int(t.group(1))) > 300 and int(t.group(2)) > 500]
        if big:
            x1, y1, x2, y2 = map(int, big[0].groups())
            adb("shell", "input", "tap", str((x1 + x2) // 2), str((y1 + y2) // 2))
            time.sleep(6)
            shot("5-tree")
            adb("shell", "input", "swipe", "540", "1800", "540", "600", "400")
            time.sleep(2)
            shot("6-tree-scrolled")
            adb("shell", "input", "keyevent", "4")
            time.sleep(2)
        else:
            failures.append("a tree tile on Discover")
        alive = adb("shell", "pidof", PKG).stdout.strip()
        dead = crashed()
    if dead:
        print("\n".join(dead[:20]))
        failures.append("crash")
    if not alive:
        failures.append("the app is no longer running")
    print("screens: " + str(OUT.relative_to(ROOT)))
    print("release walk: " + ("ok" if not failures else "FAILED: " + ", ".join(failures)))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
