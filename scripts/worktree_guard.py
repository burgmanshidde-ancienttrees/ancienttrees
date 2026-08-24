#!/usr/bin/env python3
"""Refuse to build the iOS app in a checkout another session is also editing.

Hidde, 2026-08-24, on hearing what the MapLibre port cost: "laten we die les
sowieso doorvoeren over git worktree."

What happened, 2026-08-23. Two sessions were working in this one checkout at the
same time. Halfway through the port, `SpotSheet.swift` was staged as deleted and
`SpotIntro.swift` removed from the working tree by the OTHER session, and every
build in this one failed with errors about code nobody here had touched. It took
an hour to work out that the bug was not in the code. The fix was to move into a
`git worktree` at HEAD, and it worked immediately.

WHY THIS IS A SCRIPT AND NOT A NOTE. A note saying "build app changes in a
worktree" has to be remembered at the exact moment somebody is head-down in a
build failure, which is the moment nobody reads notes. The corpus already
records the lesson twice (CURATION.md 2026-08-23, the ios-app-workflow memory)
and it would have been three by the next collision.

WHY IT REFUSES SO RARELY. A blanket "always use a worktree" would fire on every
build, and a check that fires when there is no danger gets bypassed by reflex
and then means nothing. The hazard is CONCURRENCY, not the main checkout, so
this fires only when another session is demonstrably live: a second transcript
in ~/.claude/projects/<this repo> written to in the last twenty minutes. On a
normal solo afternoon it prints nothing at all.

It also reports the fingerprint of the damage itself, which is worth more than
the prediction: staged deletions under ios/ mean somebody else's index is in
your build, and saying so up front turns a confusing hour into one line.

    from worktree_guard import guard
    guard("building the app")        # exits 1 with the fix when unsafe

    python3 scripts/worktree_guard.py    # say what it sees, change nothing
"""

import os
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _git(*args):
    try:
        r = subprocess.run(["git", "-C", str(ROOT)] + list(args),
                           capture_output=True, text=True, timeout=20)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def in_linked_worktree():
    """True when this checkout is a `git worktree add` one, not the original.

    A linked worktree's .git is a FILE pointing into the main repo's
    worktrees/ directory; the main checkout's is a directory. That is the whole
    test, and it needs no configuration."""
    d = _git("rev-parse", "--git-dir")
    return "/worktrees/" in d or "\\worktrees\\" in d


def other_live_sessions(minutes=20):
    """Other Claude Code sessions writing to this project right now.

    Each session appends to its own transcript at
    ~/.claude/projects/<path-with-slashes-as-dashes>/<uuid>.jsonl while it runs,
    so a file touched in the last few minutes is a session with its hands on
    this checkout. Ours is one of them, hence the subtraction.

    Returns a count. Best-effort by design: if the directory layout ever
    changes this returns 0 and the guard falls silent, because a build tool
    that dies over its own telemetry is worse than the collision it prevents.
    """
    slug = "-" + str(ROOT).strip("/").replace("/", "-")
    d = pathlib.Path.home() / ".claude" / "projects" / slug
    if not d.is_dir():
        return 0
    cutoff = time.time() - minutes * 60
    try:
        live = [p for p in d.glob("*.jsonl") if p.stat().st_mtime > cutoff]
    except OSError:
        return 0
    return max(0, len(live) - 1)


def foreign_staged_deletions():
    """Staged deletions under ios/, the exact fingerprint of the 08-23 mess.

    An index that says a Swift file is gone while the build still expects it is
    what produced an hour of errors about code nobody had touched."""
    out = _git("diff", "--cached", "--name-status", "--", "ios/")
    return [line.split("\t", 1)[1] for line in out.splitlines()
            if line.startswith("D") and "\t" in line]


def worktree_command(name="app-work"):
    return ("git worktree add ../ancienttrees-%s HEAD  "
            "# then work there, and `git worktree remove` it when merged" % name)


def report():
    """What the guard sees, as (ok, lines)."""
    lines = []
    ok = True
    if in_linked_worktree():
        lines.append("in a linked worktree: safe, whatever else is running.")
        return True, lines
    others = other_live_sessions()
    gone = foreign_staged_deletions()
    if gone:
        ok = False
        lines.append("%d Swift file(s) are STAGED AS DELETED in this index: %s"
                     % (len(gone), ", ".join(p.split("/")[-1] for p in gone[:4])))
        lines.append("that is another session's index in your build, and it is "
                     "what an hour of unexplainable compile errors looks like.")
    if others:
        ok = False
        lines.append("%d other Claude session(s) have written to this checkout "
                     "in the last 20 minutes." % others)
    if ok:
        lines.append("main checkout, no other session live: fine to build here.")
    return ok, lines


def guard(what="building the app"):
    """Refuse the build when this checkout is shared. Call before xcodebuild."""
    if os.environ.get("ALLOW_SHARED_CHECKOUT"):
        return
    ok, lines = report()
    if ok:
        return
    print("STOP: not safe %s in this checkout." % what, file=sys.stderr)
    for line in lines:
        print("  " + line, file=sys.stderr)
    print("\n  " + worktree_command(), file=sys.stderr)
    print("\n  (ALLOW_SHARED_CHECKOUT=1 overrides, and the last time somebody "
          "wanted to, they were wrong.)", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    ok, lines = report()
    for line in lines:
        print(("ok: " if ok else "unsafe: ") + line)
    if not ok:
        print("\n" + worktree_command())
