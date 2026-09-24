#!/usr/bin/env python3
"""Refuse a hand-drawn icon.

Hidde, 2026-09-24: "can you never ever draw icons by hand and remember not to
do that ever again". Said after a tree-page mockup whose share, report, tick
and walk icons I had drawn myself, and it turned out the live site was built
the same way: every icon an SVG path somebody typed to look roughly like the
app's SF Symbol, which is why web and app never matched.

The icon set is Phosphor (MIT), vendored as Phosphor's own files under
site/src/icons/phosphor/, chosen by Hidde the same day because every glyph has
an outline and a filled twin, the way SF Symbols does. SF Symbols themselves
cannot be used: Apple's licence limits them to apps on Apple platforms.

What this refuses: a line ADDED under site/src/ (outside site/src/icons/) that
carries SVG geometry: a <path>, <circle>, <line>, <polyline>, <polygon>,
<rect> or <ellipse>, or a d="M..." attribute. It reads the diff against
origin/main, so the icons already hand-drawn on the site are not blocked by it
today; they are replaced as their pages are rebuilt, and each one removed is
one fewer the next check has to tolerate.

Graphics that are not icons (the season chart, species line art, a provider's
official logo) are listed in data/icon-allow.json with the reason, so an
exception is a decision rather than a silence. Removing this check needs Hidde.

    python3 scripts/iconcheck.py            # against origin/main
    python3 scripts/iconcheck.py <base-ref>
"""
import json, re, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALLOW = ROOT / "data/icon-allow.json"
GEOMETRY = re.compile(r"<(path|circle|line|polyline|polygon|rect|ellipse)\b|\bd=[\"']\s*[Mm]")


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    allow = json.loads(ALLOW.read_text()) if ALLOW.exists() else {}
    try:
        diff = subprocess.run(
            ["git", "diff", "--unified=0", "--no-color", base, "--", "site/src"],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError as e:
        print(f"iconcheck: could not diff against {base}: {e.stderr.strip()}")
        return 0
    bad, current = [], None
    for line in diff.splitlines():
        if line.startswith("+++ "):
            current = line[6:] if line.startswith("+++ b/") else None
            continue
        if not current or not line.startswith("+") or line.startswith("+++"):
            continue
        if current.startswith("site/src/icons/") or current in allow:
            continue
        if GEOMETRY.search(line):
            bad.append((current, line[1:].strip()[:110]))
    if not bad:
        return 0
    print("REFUSED: hand-drawn icon geometry added (Hidde, 2026-09-24: never draw icons by hand).")
    for f, l in bad:
        print(f"  {f}: {l}")
    print("\nTake the icon from site/src/icons/phosphor/ (fetch the file from")
    print("cdn.jsdelivr.net/npm/@phosphor-icons/core@2.1.1/assets/<weight>/<name>.svg).")
    print("If this is a chart or artwork rather than an icon, list the file in")
    print("data/icon-allow.json with the reason.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
