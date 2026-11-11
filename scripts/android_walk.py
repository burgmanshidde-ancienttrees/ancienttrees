#!/usr/bin/env python3
"""android_walk.py - the Android walks (androidTest/) on the emulator.

FlowWalk.kt walks the iPhone's flows (ios FlowWalk.swift) with the same
identifiers, ButtonWalk.kt taps every button on the iPhone's screens (ios
ButtonWalk.swift), and SignedInRoundTrip.kt saves on the real test account.
Takes the emulator lock (emulator_lock.py) so no other session stops the app
mid-walk, prints one line per test, and pulls the frames each step left into
out/android-walk/ so the judging is reading a strip of pictures.

    python3 scripts/android_walk.py                     # every walk
    python3 scripts/android_walk.py --only FlowWalk     # one class
    python3 scripts/android_walk.py --only FlowWalk#settings
    python3 scripts/android_walk.py --no-build
Exit 1 when a test fails.

The debug build is installed over whatever is on the phone; a build signed with
another key (a release build) is uninstalled first, as android_parity.py does.
CI runs the same tests through gradle's connectedDebugAndroidTest (android.yml).
"""
import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from emulator_lock import emulator  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SDK = pathlib.Path.home() / "Library" / "Android" / "sdk"
ADB = str(SDK / "platform-tools" / "adb")
JBR = "/Applications/Android Studio.app/Contents/jbr/Contents/Home"
PACKAGE = "app.ancienttrees.android"
RUNNER = PACKAGE + ".test/androidx.test.runner.AndroidJUnitRunner"
APKS = ROOT / "android/app/build/outputs/apk"
OUT = ROOT / "out" / "android-walk"


def test_session():
    """The test account's session (scripts/test_session.py), or "" without the service key."""
    env = dict(os.environ)
    # On the Mac the service key lives in ~/.ancienttrees-supabase.env (never in the repo).
    keys = pathlib.Path.home() / ".ancienttrees-supabase.env"
    if "SUPABASE_SERVICE_KEY" not in env and keys.exists():
        for line in keys.read_text().splitlines():
            k, _, v = line.strip().removeprefix("export ").partition("=")
            if k and v:
                env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "test_session.py")], capture_output=True, text=True, env=env)
    line = r.stdout.strip().splitlines()[-1] if r.returncode == 0 and r.stdout.strip() else ""
    return line if line.count("|") == 3 else ""


def adb(*a, **kw):
    return subprocess.run([ADB, *a], capture_output=True, text=True, **kw)


def install(apk):
    r = adb("install", "-r", "-t", str(apk))
    if "Success" in r.stdout:
        return
    if "INCOMPATIBLE" in r.stdout + r.stderr or "signatures do not match" in r.stdout + r.stderr:
        print("another build's signature on the phone; uninstalling it for the debug build")
        adb("uninstall", PACKAGE)
        r = adb("install", "-r", "-t", str(apk))
    if "Success" not in r.stdout:
        sys.exit(f"adb install {apk.name} failed:\n{r.stdout[-800:]}{r.stderr[-800:]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=[], help="Class or Class#method, e.g. FlowWalk#settings")
    ap.add_argument("--no-build", action="store_true")
    ap.add_argument("--screens", help="ButtonWalk only: these screens, e.g. map,tree")
    a = ap.parse_args()
    env = dict(os.environ, JAVA_HOME=JBR, ANDROID_HOME=str(SDK))
    if not a.no_build:
        r = subprocess.run(["./gradlew", "-q", "assembleDebug", "assembleDebugAndroidTest"], cwd=ROOT / "android",
                           env=env, capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit("build failed:\n" + r.stdout[-2000:] + r.stderr[-2000:])
    # SIGNED IN FOR REAL (SignedInRoundTrip.kt): the test account, never a fake.
    session = test_session()
    print("signed-in round trip: " + ("on the test account" if session else "skipped, no service key"))
    cmd = ["shell", "am", "instrument", "-w", "-r"]
    if session:
        # Quoted for the device shell: the session carries "|" between its parts.
        cmd += ["-e", "AT_SESSION", "'" + session + "'"]
    if a.screens:
        cmd += ["-e", "screens", a.screens]
    if a.only:
        cmd += ["-e", "class", ",".join("app.ancienttrees." + o for o in a.only)]
    cmd.append(RUNNER)
    with emulator("android_walk"):
        install(APKS / "debug" / "app-debug.apk")
        install(APKS / "androidTest" / "debug" / "app-debug-androidTest.apk")
        for perm in ("ACCESS_FINE_LOCATION", "ACCESS_COARSE_LOCATION"):
            adb("shell", "pm", "grant", PACKAGE, "android.permission." + perm)
        adb("shell", "run-as", PACKAGE, "rm", "-rf", "files/walk")
        r = adb(*cmd, timeout=3600)
        # The frames each step left (FlowWalk.shoot), out of the app's own files.
        if OUT.exists():
            shutil.rmtree(OUT)
        OUT.mkdir(parents=True)
        tar = subprocess.run([ADB, "exec-out", "run-as", PACKAGE, "tar", "c", "-C", "files", "walk"], capture_output=True)
        if tar.stdout:
            subprocess.run(["tar", "x", "-C", str(OUT), "--strip-components", "1"], input=tar.stdout)
    failed = 0
    test = None
    for line in r.stdout.splitlines():
        m = re.match(r"INSTRUMENTATION_STATUS: (test|class|stack)=(.*)", line)
        if m and m.group(1) == "test":
            test = m.group(2)
        m = re.match(r"INSTRUMENTATION_STATUS_CODE: (-?\d+)", line)
        if m and test and m.group(1) in ("0", "-1", "-2", "-3", "-4"):
            code = m.group(1)
            word = {"0": "ok  ", "-3": "skip", "-4": "skip"}.get(code, "FAIL")
            failed += word == "FAIL"
            print(f"{word} {test}")
            test = None
    for m in re.finditer(r"INSTRUMENTATION_STATUS: stack=(.*?)(?=INSTRUMENTATION_STATUS)", r.stdout, re.S):
        print("   " + m.group(1).strip().splitlines()[0][:300])
    if "Process crashed" in r.stdout or "INSTRUMENTATION_RESULT: shortMsg" in r.stdout:
        print("the app process ended mid-walk (crash, or something stopped it)")
        failed += 1
    print(f"frames: {OUT} ({len(list(OUT.glob('*.png')))})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
