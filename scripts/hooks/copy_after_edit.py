#!/usr/bin/env python3
"""Run copycheck the moment a file with product copy is edited, not at push.

Hidde, 2026-10-22, after finding "The walking routes, your saved trees, and
the collection of the ones you have stood in front of: the Ancient Trees app."
live on every city page: "moeten we niet een skill of proces bouwen die zorgt
dat dit soort texten niet meer live komen?" The pre-push hook already runs
copycheck, but by then the sentence is written, translated seven times and
committed, and a refusal at push reads as an obstacle rather than a note.

PostToolUse on Edit and Write. Only for files that carry copy a visitor reads
(site/src/**/*.astro|ts, the app's Swift), and only the hits inside the file
just edited, so an old sentence elsewhere never nags an unrelated edit.
Silent when clean.
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
COPY_FILES = re.compile(r"(?:^|/)(?:site/src/.+\.(?:astro|ts)|ios/AncientTrees/AncientTrees/.+\.swift)$")


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    path = (payload.get("tool_input") or {}).get("file_path") or ""
    try:
        rel = str(pathlib.Path(path).resolve().relative_to(ROOT))
    except ValueError:
        return 0
    if not COPY_FILES.search(rel):
        return 0
    out = subprocess.run([sys.executable, str(ROOT / "scripts" / "copycheck.py")],
                         cwd=ROOT, capture_output=True, text=True, timeout=20).stdout
    lines = out.splitlines()
    mine = []
    for i, line in enumerate(lines):
        if line.startswith(rel + ":"):
            mine.append(line)
            if i + 1 < len(lines) and lines[i + 1].startswith("    "):
                mine.append(lines[i + 1])
    if not mine:
        return 0
    note = ("copycheck on the file you just edited (product-copy skill, step 3):\n"
            + "\n".join(mine)
            + "\nRewrite these before moving on, in every language.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                             "additionalContext": note}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
