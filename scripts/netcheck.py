#!/usr/bin/env python3
"""One door to the network and one door to the token, and checks that keep them one.

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

The second check is the same shape, one door later. An access token lives an
hour, so reading `account.session?.accessToken` gives you whatever was minted
when somebody last signed in, and every write on their behalf then comes back
401. It fails SILENTLY, which is why it keeps happening: the control fills in,
the thumb goes green, and the row never arrives. Three times now, each in a
different file, each found by Hidde on his own phone rather than by anything
here. `Account.freshToken()` and `Account.freshSession()` are the door.

What this cannot see, said plainly so nobody trusts it further: the two-line
version, `let s = account.session` on one line and `s.accessToken` on the next.
It catches the shape that has actually shipped.

Run it: python3 scripts/netcheck.py
"""

import pathlib
import re
import sys

APP = pathlib.Path(__file__).resolve().parent.parent / "ios" / "AncientTrees" / "AncientTrees"
DOOR = "Kit/Net.swift"
PATTERN = re.compile(r"URLSession\.shared\s*\.\s*(data|upload|download|dataTask|uploadTask)")
TOKEN_DOOR = "Kit/Account.swift"
TOKEN_PATTERN = re.compile(r"\bsession\s*\??\.\s*accessToken")


def scan(door, pattern):
    """Every line outside `door` matching `pattern`, comments skipped."""
    out = []
    for path in sorted(APP.rglob("*.swift")):
        rel = path.relative_to(APP).as_posix()
        if rel == door:
            continue
        for n, line in enumerate(path.read_text().splitlines(), 1):
            if line.lstrip().startswith("//") or line.lstrip().startswith("///"):
                continue                  # a comment may name it
            if pattern.search(line):
                out.append((rel, n, line.strip()))
    return out


def stale_tokens() -> int:
    findings = scan(TOKEN_DOOR, TOKEN_PATTERN)
    if not findings:
        print("one token door: nothing reads a session's token straight")
        return 0
    print(f"\n{len(findings)} place(s) read an access token straight out of the "
          f"session. Those live an hour, so this fails silently for anybody "
          f"signed in longer than that:\n")
    for rel, n, line in findings:
        print(f"  {rel}:{n}\n      {line}")
    print("\nUse await account.freshToken(), or freshSession() when you need the "
          "user id too. Both refresh first and share one refresh between callers.")
    return 1


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
        return stale_tokens()

    print(f"{len(findings)} call(s) go round Kit/Net.swift, so no test can take "
          f"the network away from them:\n")
    for rel, n, line in findings:
        print(f"  {rel}:{n}\n      {line}")
    print("\nUse Net.data / Net.upload / Net.dataTask instead. Net is a plain "
          "pass-through in a release build, so this costs nothing.")
    stale_tokens()
    return 1


if __name__ == "__main__":
    sys.exit(main())
