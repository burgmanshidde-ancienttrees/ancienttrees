#!/usr/bin/env python3
"""The daily retro: what a day cost, what it bought, and what it taught.

Hidde, 2026-08-06: "kunnen we deze leercyclus coderen in onze werkwijze zodat we
elke dag wat beter worden". This is that loop, and it only works because it
measures rather than remembers. Impressions of a day are always kinder than its
arithmetic: the day this was written felt like the best one the project has had,
and the numbers say research got 73 percent more expensive per tree.

Reads data/agent-costs.json (one row per dispatched pass, written when its
report comes back) and git, and prints the day. Append the output to RETRO.md.

    python3 scripts/retro.py               yesterday and today
    python3 scripts/retro.py 2026-08-05    one day
"""
import json
import os
import subprocess
import sys
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COSTS = os.path.join(ROOT, "data", "agent-costs.json")


def sh(*args):
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                              timeout=60).stdout
    except Exception:
        return ""


def trees_at(rev):
    """How many published trees existed at a commit."""
    listing = sh("git", "ls-tree", "-r", "--name-only", rev, "--", "data/cities/").split()
    total = 0
    for f in listing:
        if not f.endswith(".json"):
            continue
        raw = sh("git", "show", f"{rev}:{f}")
        try:
            total += len(json.loads(raw).get("trees") or [])
        except Exception:
            pass
    return total


def day_bounds(day):
    first = sh("git", "log", f"--until={day} 00:00", "-1", "--format=%H").strip()
    last = sh("git", "log", f"--until={day} 23:59", "-1", "--format=%H").strip()
    return first, last


def report(day):
    costs = json.load(open(COSTS)) if os.path.exists(COSTS) else {"days": {}}
    rows = costs.get("days", {}).get(day, [])
    first, last = day_bounds(day)
    before = trees_at(first) if first else 0
    after = trees_at(last) if last else before
    gained = after - before
    commits = len([l for l in sh("git", "log", f"--since={day} 00:00",
                                 f"--until={day} 23:59", "--format=%h").splitlines() if l])

    out = [f"## {day}", ""]
    out.append(f"Published trees {before} to {after} ({gained:+d}), {commits} commits.")
    if not rows:
        out += ["", "No agent costs recorded for this day. If passes ran, they were not logged, "
                    "and an unlogged pass is a day the loop cannot learn from."]
        return "\n".join(out)

    research = [r for r in rows if r["kind"] == "research"]
    scout = [r for r in rows if r["kind"] == "scout"]
    r_tok = sum(r["tokens"] for r in research)
    r_trees = sum(r["trees"] for r in research)
    s_tok = sum(r["tokens"] for r in scout)

    out += ["", "| kind | passes | tokens | trees | per tree |", "|---|---|---|---|---|"]
    if research:
        out.append(f"| research | {len(research)} | {r_tok:,} | {r_trees} | "
                   f"{r_tok // max(r_trees, 1):,} |")
    if scout:
        out.append(f"| scouting | {len(scout)} | {s_tok:,} | 0 | n/a |")
    out.append(f"| **total** | {len(rows)} | {sum(r['tokens'] for r in rows):,} | {r_trees} | |")

    dear = sorted(research, key=lambda r: -(r["tokens"] / max(r["trees"], 1)))[:3]
    out += ["", "**Most expensive per tree.** The tail is where the lesson usually is."]
    for r in dear:
        per = f"{r['tokens'] // r['trees']:,} each" if r["trees"] else "nothing shipped"
        out.append(f"- {r['target']}: {r['tokens']:,} tokens, {r['trees']} trees, {per}. {r['note']}")

    # Two different failures, kept apart on purpose. Tokens that bought nothing
    # at all, and passes sent out on a false premise: the second still produced
    # work, so pricing it as waste would flatter neither the day nor the fix.
    w = sum(r.get("wasted", 0) for r in rows)
    if w:
        out += ["", f"**Tokens that bought nothing: {w:,}, "
                    f"{w * 100 // sum(r['tokens'] for r in rows)} percent of the day.**"]
        for r in rows:
            if r.get("wasted"):
                out.append(f"- {r['target']}: {r['wasted']:,}. {r['note']}")
    wrong = [r for r in rows if r.get("brief_wrong")]
    if wrong:
        out += ["", f"**Briefs sent on a false premise: {len(wrong)}.** Each pass caught it "
                    f"itself and pivoted, so the cost is a detour rather than a loss, but three "
                    f"in one day is a mechanism problem rather than an attention problem."]
        for r in wrong:
            out.append(f"- {r['target']}: {r['note']}")
    return "\n".join(out)


def main():
    days = sys.argv[1:] or [str(date.today() - timedelta(days=1)), str(date.today())]
    print("\n\n".join(report(d) for d in days))
    print("\nAppend this to RETRO.md, newest first. A lesson that appears on two "
          "different days stops being a note and becomes a build check.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
