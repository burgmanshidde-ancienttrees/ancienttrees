#!/usr/bin/env python3
"""Say which checkout of this repo to build in, and remove the ones to forget.

Hidde, 2026-09-25, on finding two projects in Xcode's welcome window
(~/Documents/Ancienttrees/ios and ~/Documents/ancienttrees-release/ios): "kun
jij 1 doen ik heb het nooit gemaakt". He had not made it. A SESSION made it,
with the command worktree_guard.py prints, and that is the whole bug: a
`git worktree add ../ancienttrees-<name> HEAD` sits on a DETACHED HEAD at the
commit it was born on. It never moves again. Nothing in it is wrong, nothing is
dirty, `git status` is clean and reassuring, and every build out of it ships the
app as it was on the day somebody needed a spare checkout. Xcode then remembers
both folders forever, side by side, with no hint which is which.

So the old advice ("pick one") asked the wrong thing of the wrong person. Which
one to keep is not a preference, it is a fact about the repository, and a fact
is a script's job.

    python3 scripts/checkouts.py         # what is on this machine, change nothing
    python3 scripts/checkouts.py --fix   # remove the stale ones, bring the keeper current

WHAT --fix WILL NOT DO. It never removes a checkout carrying uncommitted work or
a commit that is not on origin/main, because that is somebody's unpushed
afternoon and deleting it is the one kind of mistake this project cannot undo.
It says what it found and stops.

It finds two different kinds of second checkout, because the symptom in Xcode is
identical and the cure is not: a linked WORKTREE (one repository, several
working directories, removed with `git worktree remove`) and a separate CLONE
(its own repository, which git knows nothing about and which is only ever found
by looking at the neighbouring folders).
"""

import argparse
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def git(*args, cwd=None, timeout=60):
    """(ok, output). Never raises: a missing checkout is an answer, not a crash."""
    try:
        r = subprocess.run(["git", "-C", str(cwd or ROOT)] + list(args),
                           capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0, (r.stdout + r.stderr).strip()
    except Exception as e:
        return False, str(e)


def first_commit(path):
    """The root commit, which is what makes two clones the same repository.

    A remote url would be the obvious test and it is the weaker one: a fork, a
    rename or an ssh-versus-https remote all read as different repositories
    while sharing every commit."""
    ok, out = git("rev-list", "--max-parents=0", "HEAD", cwd=path)
    return out.splitlines()[-1] if ok and out else None


def worktrees():
    """Every working directory git itself knows about, main one first."""
    ok, out = git("worktree", "list", "--porcelain")
    if not ok:
        return []
    found, cur = [], {}
    for line in out.splitlines():
        if line.startswith("worktree "):
            if cur:
                found.append(cur)
            cur = {"path": pathlib.Path(line[9:]), "detached": False, "branch": None}
        elif line.startswith("HEAD "):
            cur["head"] = line[5:]
        elif line.startswith("branch "):
            cur["branch"] = line[7:].replace("refs/heads/", "")
        elif line.strip() == "detached":
            cur["detached"] = True
    if cur:
        found.append(cur)
    return found


def clones(known):
    """Sibling folders that are the same repository but their own clone.

    Looked for beside this checkout and one level up, because that is where a
    person's projects live (~/Documents/x and ~/Documents/y) and where a
    worktree is created. Not a filesystem search: this has to cost nothing."""
    mine = first_commit(ROOT)
    seen = {p.resolve() for p in known}
    out = []
    for parent in {ROOT.parent, ROOT.parent.parent}:
        try:
            entries = sorted(parent.iterdir())
        except Exception:
            continue
        for d in entries:
            if not d.is_dir() or d.resolve() in seen:
                continue
            if not (d / ".git").exists():
                continue
            if first_commit(d) != mine or mine is None:
                continue
            seen.add(d.resolve())
            out.append(d)
    return out


def state(path):
    """Everything needed to judge one checkout, in one pass."""
    ok, dirty = git("status", "--porcelain", cwd=path)
    ok2, head = git("rev-parse", "HEAD", cwd=path)
    # Commits here that origin/main has never seen. This is the field that
    # decides whether a folder may be deleted, so it fails CLOSED: if the
    # question cannot be answered, the answer is "it has work".
    ok3, own = git("rev-list", "--count", "HEAD", "^origin/main", cwd=path)
    ok4, behind = git("rev-list", "--count", "HEAD..origin/main", cwd=path)
    return {
        "dirty": [l for l in dirty.splitlines() if l.strip()] if ok else ["unknown"],
        "head": head[:9] if ok2 else "unknown",
        "own": int(own) if ok3 and own.isdigit() else None,
        "behind": int(behind) if ok4 and behind.isdigit() else None,
    }


def describe(s):
    bits = [f"at {s['head']}"]
    bits.append("clean" if not s["dirty"] else f"{len(s['dirty'])} uncommitted file(s)")
    if s["own"] is None:
        bits.append("unpushed commits unknown")
    elif s["own"]:
        bits.append(f"{s['own']} commit(s) not on origin/main")
    if s["behind"]:
        bits.append(f"{s['behind']} behind origin/main")
    elif s["behind"] == 0:
        bits.append("current")
    return ", ".join(bits)


def removable(s):
    """May this folder be deleted without losing anything? Fails closed."""
    if s["dirty"]:
        return False, "it carries uncommitted changes"
    if s["own"] is None:
        return False, "cannot tell whether it holds unpushed commits"
    if s["own"]:
        return False, f"it holds {s['own']} commit(s) that are not on origin/main"
    return True, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true",
                    help="remove the stale checkouts and bring the keeper current")
    args = ap.parse_args()

    ok, _ = git("fetch", "-q", "origin", "main")
    if not ok:
        print("could not reach origin, so behind/ahead counts may be stale\n")

    wts = worktrees()
    if not wts:
        print("this does not look like a git checkout.")
        return 1
    keeper = wts[0]["path"]          # git lists the main working directory first
    extras = [w for w in wts[1:]]
    extra_clones = clones([w["path"] for w in wts])

    print(f"BUILD HERE   {keeper}")
    ks = state(keeper)
    print(f"             the main checkout, {describe(ks)}")
    if not extras and not extra_clones:
        print("\nnothing else on this machine. One folder, no confusion.")
    for w in extras:
        s = state(w["path"])
        kind = "worktree (detached, so it never follows main)" if w["detached"] \
            else f"worktree on branch {w['branch']}"
        print(f"\nFORGET THIS  {w['path']}")
        print(f"             {kind}, {describe(s)}")
        can, why = removable(s)
        print(f"             remove with: git worktree remove {w['path']}"
              if can else f"             KEEP FOR NOW: {why}")
    for d in extra_clones:
        s = state(d)
        print(f"\nFORGET THIS  {d}")
        print(f"             a separate clone, {describe(s)}")
        can, why = removable(s)
        print("             it is its own clone, so git cannot remove it: "
              f"delete the folder yourself once you are happy ({d})"
              if can else f"             KEEP FOR NOW: {why}")

    if not args.fix:
        if extras or extra_clones:
            print("\n  python3 scripts/checkouts.py --fix   # do it")
        return 0

    print("\n--- fixing")
    for w in extras:
        s = state(w["path"])
        can, why = removable(s)
        if not can:
            print(f"left alone: {w['path']} ({why})")
            continue
        ok, out = git("worktree", "remove", str(w["path"]))
        print(f"removed {w['path']}" if ok else f"could not remove {w['path']}: {out}")
    for d in extra_clones:
        # Never deleted from here. A clone is not git's to remove, and a folder
        # this script merely RECOGNISED is not a folder it should erase.
        print(f"not touched (its own clone, delete it yourself): {d}")

    ok, out = git("pull", "--ff-only", "origin", "main", cwd=keeper)
    after = state(keeper)
    if ok:
        print(f"{keeper}: at {after['head']}, "
              + ("current" if after["behind"] == 0 else f"{after['behind']} behind"))
    else:
        # --ff-only is the point: a checkout carrying its own commits is not
        # quietly merged into, it is reported.
        print(f"{keeper}: could not fast-forward, so nothing was moved\n{out}")
    print("\n--- the catalogue the app ships with")
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "appdata.py")],
                       cwd=str(keeper))
    if r.returncode != 0:
        print("the bundled catalogue did not refresh; a fresh install would be stale")
    return 0


if __name__ == "__main__":
    sys.exit(main())
