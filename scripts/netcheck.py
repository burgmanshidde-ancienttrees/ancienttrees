#!/usr/bin/env python3
"""One door to the network, and a check that keeps it one.

The app talks to the network through Kit/Net.swift and nothing else. That is
not tidiness: URLSession.shared cannot be intercepted, so a call made directly
on it is a call no test can ever take the network away from. Every failure a
walking app actually meets, no signal, a stall, a 500, a stale session, is
unreachable for that call and stays unreachable forever.

This exists because it happened within hours of the door being built. Eighteen
calls were routed through Net on 2026-08-27 and two files that landed on main
the same afternoon (SightingSync, WorthIt) carried nine more, written against
the old habit by a session that had never heard of the new one. Nothing said
so; the tests simply did not cover them.

Run it: python3 scripts/netcheck.py
"""

import pathlib
import re
import sys

APP = pathlib.Path(__file__).resolve().parent.parent / "ios" / "AncientTrees" / "AncientTrees"
DOOR = "Kit/Net.swift"
PATTERN = re.compile(r"URLSession\.shared\s*\.\s*(data|upload|download|dataTask|uploadTask)")


def main() -> int:
    findings = []
    for path in sorted(APP.rglob("*.swift")):
        rel = path.relative_to(APP).as_posix()
        if rel == DOOR:
            continue                      # the door itself is allowed through it
        for n, line in enumerate(path.read_text().splitlines(), 1):
            if line.lstrip().startswith("//"):
                continue                  # a comment may name it
            if PATTERN.search(line):
                findings.append((rel, n, line.strip()))

    if not findings:
        print("one network door: every call goes through Net")
        return 0

    print(f"{len(findings)} call(s) go round Kit/Net.swift, so no test can take "
          f"the network away from them:\n")
    for rel, n, line in findings:
        print(f"  {rel}:{n}\n      {line}")
    print("\nUse Net.data / Net.upload / Net.dataTask instead. Net is a plain "
          "pass-through in a release build, so this costs nothing.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
