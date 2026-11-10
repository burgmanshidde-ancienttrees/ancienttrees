#!/usr/bin/env python3
"""gradle_locked.py - one Android build at a time on this Mac.

Several sessions and agents build the Android app in their own worktrees, and
each Gradle build takes gigabytes; on 2026-11-10 the Mac ran short enough that
the emulator could not start. This runs ./gradlew in the android/ folder of the
worktree it lives in, holding a lock beside the emulator's, with a 2 GB heap and
no daemon left behind.

    python3 scripts/gradle_locked.py assembleDebug testDebugUnitTest
"""
import fcntl
import os
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCK = pathlib.Path.home() / "Library" / "Caches" / "ancienttrees-gradle.lock"
JBR = "/Applications/Android Studio.app/Contents/jbr/Contents/Home"


def main():
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    with open(LOCK, "a+") as f:
        told = False
        while True:
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if not told:
                    print("another Android build is running; waiting", flush=True)
                    told = True
                time.sleep(5)
        env = dict(os.environ, JAVA_HOME=JBR, ANDROID_HOME=str(pathlib.Path.home() / "Library/Android/sdk"))
        cmd = ["./gradlew", "--no-daemon", "-q", "-Dorg.gradle.jvmargs=-Xmx2g"] + sys.argv[1:]
        return subprocess.run(cmd, cwd=ROOT / "android", env=env).returncode


if __name__ == "__main__":
    sys.exit(main())
