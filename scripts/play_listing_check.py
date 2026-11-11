#!/usr/bin/env python3
"""play_listing_check.py - the Google Play listing draft, counted and pitch-checked.

Reads drafts/play-store-listing.md: under each "## <language>" heading the
fenced blocks are, in order, the app name, the short description and the full
description. Play refuses a name over 30 characters, a short description over
80 and a full description over 4000, and says only that a field is too long,
so this counts them first. Every English block also goes through
scripts/pitchcheck.py, and every block in every language through the em dash
and forever-promise rules (CLAUDE.md: never "free forever", "no accounts",
"always"; never an em dash).

    python3 scripts/play_listing_check.py
Exit 1 on any finding.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DRAFT = ROOT / "drafts" / "play-store-listing.md"
LIMITS = [("name", 30), ("short", 80), ("full", 4000)]
FORBIDDEN = ["—", "free forever", "no accounts", "always"]


def sections(text):
    out = {}
    for part in re.split(r"^## ", text, flags=re.M)[1:]:
        head, _, body = part.partition("\n")
        blocks = re.findall(r"```\n(.*?)\n```", body, flags=re.S)
        if blocks:
            out[head.strip()] = blocks
    return out


def main():
    bad = 0
    for lang, blocks in sections(DRAFT.read_text()).items():
        if len(blocks) != 3:
            print(f"{lang}: {len(blocks)} blocks, want name, short and full")
            bad += 1
            continue
        for (field, limit), text in zip(LIMITS, blocks):
            n = len(text)
            flag = "" if n <= limit else "  TOO LONG"
            print(f"{lang[:32]:32} {field:5} {n:4}/{limit}{flag}")
            bad += bool(flag)
            for word in FORBIDDEN:
                if word in text.lower():
                    print(f"  {lang}: {field} contains {word!r}")
                    bad += 1
            if lang.startswith("English"):
                r = subprocess.run([sys.executable, str(ROOT / "scripts" / "pitchcheck.py"), "--text", text],
                                   capture_output=True, text=True)
                if r.returncode:
                    print(r.stdout.strip())
                    bad += 1
    print("clean" if not bad else f"{bad} finding(s)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
