#!/usr/bin/env python3
"""Apply a viewing pass's verdicts in one serialised sweep.

A viewing pass is dispatched several at a time, and the obvious design has each
pass write its own results. That design is wrong here: every pass would be
read-modify-writing the same data/photo-queue.json, and the last writer wins, so
the cheapest judgements in the project would be silently thrown away. So passes
RETURN their verdicts and this applies them, one file at a time, in one process.

    python3 scripts/photo_verdicts.py verdicts-a.json verdicts-b.json

Input is a JSON array of {tree_id, page, verdict, reason}, verdict being
approve, hold or reject. Recording a rejection matters as much as recording an
approval: an unrecorded reject is an image the next pass pays to judge again.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = os.path.join(ROOT, "scripts", "photo_apply.py")


def main():
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not files:
        print(__doc__)
        return 1
    rows = []
    for f in files:
        rows += json.load(open(f))

    counts, failed = {"approve": 0, "hold": 0, "reject": 0}, []
    seen_approved = set()
    for r in rows:
        verdict, tid = r.get("verdict"), r.get("tree_id")
        if verdict not in counts:
            continue
        # One photograph per tree: a second approval for a tree already served
        # would overwrite the first for no gain.
        if verdict == "approve":
            if tid in seen_approved:
                continue
            seen_approved.add(tid)
        cmd = ["python3", APPLY, verdict, tid, r.get("page") or "",
               "--reason", (r.get("reason") or "")[:200]]
        out = subprocess.run(cmd, capture_output=True, text=True)
        if out.returncode != 0:
            failed.append((tid, r.get("page"), out.stdout.strip() or out.stderr.strip()))
            continue
        counts[verdict] += 1
        if verdict in ("approve", "hold"):
            print(out.stdout.rstrip())

    print(f"\napproved {counts['approve']}, held {counts['hold']}, "
          f"rejected {counts['reject']}, failed {len(failed)}")
    for tid, page, why in failed:
        print(f"  FAILED {tid}  {why}  {page}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
