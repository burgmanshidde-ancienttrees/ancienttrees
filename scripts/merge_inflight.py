#!/usr/bin/env python3
"""Git merge driver for data/in-flight.json: union the claims, never conflict.

This file is pure coordination state. Two writers each adding a claim is the
normal case, not a disagreement, and a text merge turns it into a conflict that
costs a session three round trips to resolve by hand. It cost exactly that three
times on 2026-08-22 while opening Dutch cities alongside the night runs.

So: take every claim from both sides, keyed on place plus kind plus holder, and
keep the later `until` when the same key appears twice. Everything outside
`claims` is documentation and comes from ours. Expired claims are dropped on the
way through, which is what passcheck would do on its next read anyway.

Wired up in .gitattributes. Falls back to a non-zero exit, which git treats as a
normal conflict, if anything at all is unexpected.
"""
import json, sys

def load(p):
    with open(p) as f:
        return json.load(f)

def key(c):
    return ((c.get("place") or "").lower(), c.get("kind"), c.get("by"))

def main(base, ours, theirs, out):
    try:
        o, t = load(ours), load(theirs)
    except Exception as e:
        print("merge_inflight: cannot parse (%s), falling back to a real conflict" % e,
              file=sys.stderr)
        return 1
    merged = dict(o)
    seen = {}
    for src in (t, o):                      # ours last, so ours wins a tie
        for c in src.get("claims", []) or []:
            k = key(c)
            if k not in seen or (c.get("until") or "") > (seen[k].get("until") or ""):
                seen[k] = c
    merged["claims"] = sorted(seen.values(), key=lambda c: (c.get("until") or "", str(key(c))))
    with open(out, "w") as f:
        json.dump(merged, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return 0

if __name__ == "__main__":
    # git calls: merge_inflight.py %O %A %B  and expects the result in %A
    base, ours, theirs = sys.argv[1], sys.argv[2], sys.argv[3]
    sys.exit(main(base, ours, theirs, ours))
