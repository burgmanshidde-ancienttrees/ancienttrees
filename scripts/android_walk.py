#!/usr/bin/env python3
"""android_walk.py - the Android flow walk (androidTest/FlowWalk.kt) on the emulator.

The routes between screens, walked with a finger, as ios FlowWalk.swift does:
tabs, a tree and back, a website link, and the sign-in gates on save and collect.
Takes the emulator lock (emulator_lock.py) so no other session stops the app
mid-walk, then prints one line per step.

    python3 scripts/android_walk.py
Exit 1 when a step fails.
"""
import glob
import os
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from emulator_lock import emulator  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SDK = pathlib.Path.home() / "Library" / "Android" / "sdk"
JBR = "/Applications/Android Studio.app/Contents/jbr/Contents/Home"


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


def main():
    env = dict(os.environ, JAVA_HOME=JBR, ANDROID_HOME=str(SDK))
    # SIGNED IN FOR REAL (SignedInRoundTrip.kt): the test account, never a fake.
    session = test_session()
    print("signed-in round trip: " + ("on the test account" if session else "skipped, no service key"))
    cmd = ["./gradlew", "-q", "connectedDebugAndroidTest"]
    if session:
        cmd.append("-Pandroid.testInstrumentationRunnerArguments.AT_SESSION=" + session)
    with emulator("android_walk"):
        r = subprocess.run(cmd, cwd=ROOT / "android", env=env, capture_output=True, text=True)
    failed = 0
    for f in glob.glob(str(ROOT / "android/app/build/outputs/androidTest-results/connected/debug/TEST-*.xml")):
        s = open(f).read()
        for m in re.finditer(r'<testcase name="([^"]+)"[^>]*?(/>|>(.*?)</testcase>)', s, re.S):
            bad = "<failure" in (m.group(3) or "")
            failed += bad
            print(("FAIL " if bad else "ok   ") + m.group(1))
        if "Process crashed" in s:
            print("the app process ended mid-walk (crash, or something stopped it)")
    if r.returncode != 0 and not failed:
        print(r.stdout[-1500:] + r.stderr[-1500:])
        return 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
