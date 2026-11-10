#!/usr/bin/env python3
"""android_owner.py - one session per Android screen, never two.

Hidde, 2026-11-10, after the tree page and Discover were each started twice by
two sessions at once: "overzie jij het nog gebeuren en niet dingen dubbel?" One
session (the android-basis session) starts Android sessions, and before it does,
it claims the screens here. A claim on a screen that already has an owner is
refused, so the second start is stopped by this script, not by memory.

    python3 scripts/android_owner.py --list
    python3 scripts/android_owner.py --claim tree tree-nophoto --session local_x --name android-parity-tree
    python3 scripts/android_owner.py --release tree tree-nophoto

The owner lives in data/android-parity.json beside each screen's status, which
android_parity.py already reads. Exit 1 when a claim is refused.
"""
import argparse
import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATUS = ROOT / "data" / "android-parity.json"


def load():
    return json.loads(STATUS.read_text())


def save(d):
    STATUS.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def claim(d, screens, session, name, today=None):
    """The screens claimed, or the list of (screen, owner) that refuse the claim."""
    taken = [(s, d[s]["owner"]) for s in screens if s in d and d[s].get("owner")
             and d[s]["owner"].get("session") != session]
    if taken:
        return taken
    for s in screens:
        d.setdefault(s, {"status": "not-ported", "differences": []})
        d[s]["owner"] = {"session": session, "name": name,
                         "since": today or datetime.date.today().isoformat()}
    return []


def release(d, screens):
    for s in screens:
        if s in d:
            d[s].pop("owner", None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--claim", nargs="*")
    ap.add_argument("--release", nargs="*")
    ap.add_argument("--session")
    ap.add_argument("--name", default="")
    a = ap.parse_args()
    d = load()
    if a.claim:
        if not a.session:
            sys.exit("--claim needs --session")
        taken = claim(d, a.claim, a.session, a.name)
        if taken:
            for s, o in taken:
                print(f"REFUSED {s}: owned by {o.get('name') or o.get('session')} since {o.get('since')}")
            sys.exit(1)
        save(d)
        print("claimed: " + ", ".join(a.claim))
    if a.release:
        release(d, a.release)
        save(d)
        print("released: " + ", ".join(a.release))
    if a.list or not (a.claim or a.release):
        for s, v in d.items():
            if s.startswith("_"):
                continue
            o = v.get("owner")
            who = f"{o.get('name') or o.get('session')} since {o.get('since')}" if o else "free"
            print(f"{s:20} {v.get('status', '?'):12} {who}")


if __name__ == "__main__":
    main()
