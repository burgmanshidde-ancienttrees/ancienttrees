#!/usr/bin/env python3
"""android_parity.py - the iPhone and Android side by side, screen by screen.

Hidde, 2026-11-10: "ik wil dat je de ios build 42 exact na bouwt qua interactie
en alles ik wil niet alles weer opnieuw aan je moeten vertellen". The iOS app is
the specification (DECISIONS.md 2026-11-10); a screen is done when its iOS and
Android screenshots of the same state sit side by side with no difference
nobody can name a reason for. This makes those pairs and the page he reads.

    python3 scripts/android_parity.py                    # every frame
    python3 scripts/android_parity.py --only tree map    # some frames
    python3 scripts/android_parity.py --no-ios           # reuse the iPhone shots
    python3 scripts/android_parity.py --no-build         # reuse the Android build

iPhone shots come from scripts/appsweep.py (the same launch arguments,
SweepFrames.swift), on the iPhone 17 Pro. Android shots come from the running
emulator through adb, launched with the same arguments (LaunchArgs.kt). The
status per screen, its open differences and the differences Android forces live
in data/android-parity.json, which this page shows and never writes.

Writes out/parity/index.html, out/parity/ios/*.png, out/parity/android/*.png.
"""
import argparse
import html
import json
import os
import pathlib
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out" / "parity"
STATUS = ROOT / "data" / "android-parity.json"
SDK = pathlib.Path.home() / "Library" / "Android" / "sdk"
ADB = str(SDK / "platform-tools" / "adb")
JBR = "/Applications/Android Studio.app/Contents/jbr/Contents/Home"
PACKAGE = "app.ancienttrees.android"
ACTIVITY = PACKAGE + "/app.ancienttrees.MainActivity"
IOS_DEVICE = "iPhone 17 Pro"
# appsweep.py stands every frame at Dam square unless the frame names its own
# place, so the Android frame does too.
ORIGIN = "-at=52.3731,4.8922"

# name -> the iPhone's launch arguments, taken from appsweep.py itself (which
# picks real subject trees out of the bundled feed: the longest name with a
# photograph, and so on), so both phones open the very same state. The same
# arguments go to Android; LaunchArgs.kt reads the ones it knows.
sys.path.insert(0, str(ROOT / "scripts"))
import appsweep  # noqa: E402

FRAMES = {name: list(args) for name, args, _ in appsweep.screens(appsweep.pick_subjects())}
# The screens with an Android port, in the order the page shows them.
PORTED = ["map", "map-full", "map-pin", "search", "tree", "tree-nophoto", "photo-viewer", "signin",
<<<<<<< HEAD
          "explore", "collection-tab", "collection-tab-full", "own-tree", "profile",
=======
          "explore", "collection-tab", "profile", "profile-signed-in", "profile-edit", "signin-email", "refused",
          "people", "early-adopter", "early-adopter-sheet",
>>>>>>> d5f7b2ae3 (Android: sign-in and profile ported from the iPhone (parity session 7), work in progress)
          "collect-intro", "collect-away", "collect-place", "collect-identify", "collect-ticked", "collect-voted",
          "collect-compare", "collect-describe"]


def run(cmd, **kw):
    return subprocess.run(cmd, check=False, text=True, capture_output=True, **kw)


def ios(frames, build):
    out = OUT / "ios-sweep"
    for i, name in enumerate(frames):
        cmd = [sys.executable, str(ROOT / "scripts" / "appsweep.py"), "--only", name,
               "--device", IOS_DEVICE, "--out", str(out)]
        if not build or i > 0:
            cmd.append("--no-build")
        r = run(cmd)
        shot = next(out.rglob(f"{name}.png"), None)
        if shot:
            shutil.copy(shot, OUT / "ios" / f"{name}.png")
        else:
            print(f"ios {name}: no screenshot\n{r.stdout[-400:]}{r.stderr[-400:]}")


def android(frames, build):
    if build:
        env = dict(os.environ, JAVA_HOME=JBR, ANDROID_HOME=str(SDK))
        r = run(["./gradlew", "-q", "assembleDebug"], cwd=ROOT / "android", env=env)
        if r.returncode != 0:
            sys.exit("android build failed:\n" + r.stdout[-2000:] + r.stderr[-2000:])
        run([ADB, "install", "-r", str(ROOT / "android/app/build/outputs/apk/debug/app-debug.apk")])
        # After an install the system UI restarts the app by itself a moment
        # later, without our extras (a CLEAR_TASK start from systemui, API 37):
        # let that happen before the first frame.
        run([ADB, "shell", "am", "start", "-W", "-n", ACTIVITY])
        time.sleep(10)
    for name in frames:
        run([ADB, "shell", "am", "force-stop", PACKAGE])
        args = FRAMES[name]
        if not any(a.startswith("-at=") for a in args):
            args = args + [ORIGIN]
        # am splits --esa on commas; a comma inside one argument (-at=lat,lng)
        # is written \, and the whole list quoted for the device's shell.
        joined = ",".join(a.replace(",", "\\,") for a in args)
        run([ADB, "logcat", "-c"])
        run([ADB, "shell", "am", "start", "-W", "-n", ACTIVITY, "--esa", "args", "'" + joined + "'"])
        # Until the app says its catalogue is read (MainActivity logs it), then
        # time for the tiles and the photographs.
        for _ in range(90):
            if "catalogue" in run([ADB, "logcat", "-d", "-s", "AncientTrees"]).stdout:
                break
            time.sleep(1)
        time.sleep(8)
        png = subprocess.run([ADB, "exec-out", "screencap", "-p"], capture_output=True)
        (OUT / "android" / f"{name}.png").write_bytes(png.stdout)


def page(frames):
    status = json.loads(STATUS.read_text()) if STATUS.exists() else {}
    forced = status.get("_android_forced", [])
    rows = []
    for name in frames:
        s = status.get(name, {})
        diffs = "".join(f"<li>{html.escape(d)}</li>" for d in s.get("differences", [])) or "<li>none listed</li>"
        rows.append(f"""
<section>
  <h2>{html.escape(name)} <span class="st {html.escape(s.get('status', 'not-ported'))}">{html.escape(s.get('status', 'not-ported'))}</span></h2>
  <div class="pair">
    <figure><img src="ios/{name}.png" alt=""><figcaption>iPhone</figcaption></figure>
    <figure><img src="android/{name}.png" alt=""><figcaption>Android</figcaption></figure>
  </div>
  <h3>Open differences</h3><ul>{diffs}</ul>
</section>""")
    forced_html = "".join(f"<li><b>{html.escape(f['what'])}</b>: {html.escape(f['why'])}</li>" for f in forced)
    (OUT / "index.html").write_text(f"""<!doctype html><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Android next to iPhone</title>
<style>
body{{font:15px/1.45 -apple-system,system-ui,sans-serif;margin:0 auto;max-width:980px;padding:16px;color:#26301E}}
h1{{font-size:26px}} h2{{font-size:20px;margin-top:40px}} h3{{font-size:15px;margin:12px 0 4px}}
.pair{{display:flex;gap:16px}} figure{{margin:0;flex:1}} img{{width:100%;border:1px solid #E6E6E6;border-radius:12px}}
figcaption{{text-align:center;color:#5C6350;font-size:13px}}
.st{{font-size:12px;padding:2px 8px;border-radius:99px;background:#F2F2F2;vertical-align:middle}}
.st.parity{{background:#EDF3E3;color:#4A6B2A}} .st.not-ported{{background:#FBE9E7;color:#B22222}}
</style>
<h1>Android next to iPhone</h1>
<p>Each screen in the same state on both phones. A difference without a reason is a bug.</p>
<h3>What Android itself forces</h3><ul>{forced_html}</ul>
{''.join(rows)}
""")
    print(f"page: {OUT / 'index.html'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--no-ios", action="store_true")
    ap.add_argument("--no-android", action="store_true")
    ap.add_argument("--no-build", action="store_true")
    a = ap.parse_args()
    frames = a.only or [f for f in PORTED if f in FRAMES]
    for d in ("ios", "android"):
        (OUT / d).mkdir(parents=True, exist_ok=True)
    if not a.no_android:
        android(frames, build=not a.no_build)
    if not a.no_ios:
        ios(frames, build=not a.no_build)
    page(frames)


if __name__ == "__main__":
    main()
