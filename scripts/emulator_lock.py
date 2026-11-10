#!/usr/bin/env python3
"""emulator_lock.py - one session at a time on the one Android emulator.

Found 2026-11-10: a flow walk failed with "Process crashed" because another
session ran `am force-stop app.ancienttrees.android` on the same emulator in the
middle of it. Several Android sessions share Hidde's one emulator, so every
script that installs, starts or photographs the app takes this lock first and
waits while another holds it. The lock is the operating system's (flock), so a
session that dies lets go by itself.

    from emulator_lock import emulator
    with emulator("android_parity"):
        ...

    python3 scripts/emulator_lock.py --who      # who holds it now
"""
import contextlib
import fcntl
import os
import pathlib
import sys
import time

LOCK = pathlib.Path.home() / "Library" / "Caches" / "ancienttrees-emulator.lock"


@contextlib.contextmanager
def emulator(who, wait_minutes=30):
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    f = open(LOCK, "a+")
    deadline = time.time() + wait_minutes * 60
    told = False
    while True:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except BlockingIOError:
            if not told:
                f.seek(0)
                print(f"emulator busy ({f.read().strip() or 'unknown'}); waiting", flush=True)
                told = True
            if time.time() > deadline:
                f.close()
                sys.exit(f"emulator still busy after {wait_minutes} minutes")
            time.sleep(5)
    f.seek(0)
    f.truncate()
    f.write(f"{who}, pid {os.getpid()}, since {time.strftime('%H:%M:%S')}\n")
    f.flush()
    try:
        yield
    finally:
        f.seek(0)
        f.truncate()
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()


if __name__ == "__main__":
    if "--who" in sys.argv:
        print(LOCK.read_text().strip() if LOCK.exists() and LOCK.read_text().strip() else "free")
