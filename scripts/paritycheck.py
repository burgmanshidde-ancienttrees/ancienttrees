#!/usr/bin/env python3
"""A line removed from one surface must not survive on the other.

Hidde, 2026-09-11, finding "Exact location. The pin marks the trunk." still on
the website a week after he had it taken out of the app: "zorg dat deze pagina
gelijk wordt getrokken met de app", and then "zorg dat dit volgende keer wel
gelijk app en web doet."

The both-surfaces rule in CLAUDE.md already said a feature is designed for app
and web at once. It did not hold, for the reason every remembered rule in this
project stops holding: nothing checked it at the moment it mattered. The line
was byte-identical on both surfaces, so a machine could have caught it in a
second, and that is what this does.

WHAT IT LOOKS FOR. A user-facing string literal REMOVED from one surface in the
range being pushed, which is not still present somewhere else on that same
surface (so a string that merely moved is not a removal), and which still
appears in the other surface's source. The app side reads Swift literals in
Text, Label, Button and similar; the web side reads the values in
site/src/lib/i18n.ts and text typed into .astro markup.

WHAT IT DELIBERATELY DOES NOT DO. Judge whether the removal was right, or catch
a string that was reworded rather than removed. Those need a person. It also
stays quiet about anything in data/parity-allow.json, which is where a string
goes that lives on one surface ON PURPOSE (the sponsor page is web-only by
design), with the reason written beside it, so an exception is a decision and
not a silence.

Usage:
  python3 scripts/paritycheck.py                   # the range being pushed (origin/main..HEAD)
  python3 scripts/paritycheck.py --range A..B      # any range
  python3 scripts/paritycheck.py --since 21        # a sweep of the last N days, report only

Exit 1 in range mode when a hit is found, so the pre-push hook can refuse it.
A sweep never fails: it reports history, and history is not the push's fault.
"""
import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = "ios/AncientTrees/AncientTrees"
WEB = "site/src"
ALLOW = os.path.join(ROOT, "data", "parity-allow.json")
MIN_LEN = 14   # shorter literals ("Done", "Cancel") match everywhere and mean nothing

SWIFT_LIT = re.compile(r'(?:Text|Label|Button|LocalizedStringKey|accessibilityLabel)\(\s*"([^"\\]{%d,})"' % MIN_LEN)
TS_VALUE = re.compile(r'^\s*[A-Za-z]+:\s*"([^"\\]{%d,})",?\s*$' % MIN_LEN)
ASTRO_TEXT = re.compile(r'>\s*([A-Z][^<>{}]{%d,}?)\s*<' % MIN_LEN)


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout


def removed(diff, surface):
    out = set()
    for line in diff.splitlines():
        if not line.startswith("-") or line.startswith("---"):
            continue
        body = line[1:]
        if surface == "app":
            out.update(SWIFT_LIT.findall(body))
        else:
            m = TS_VALUE.match(body)
            if m:
                out.add(m.group(1))
            out.update(t.strip() for t in ASTRO_TEXT.findall(body))
    return out


COMMENT = re.compile(r'^\s*(//|/\*|\*|#|\{/\*)')


def present(literal, path, only_ext=None):
    """Files under `path` where the literal appears OUTSIDE a comment.

    Two things the first sweep counted as copy and are not. A comment quoting
    retired copy is how a decision records WHY it was retired, and counting it
    made the check report the app still showing a line it had removed a week
    earlier. And the app bundles a snapshot of the catalogue (Data/*.json), so a
    tree NAME the website dropped is data in transit, not a sentence anybody
    wrote into the app: on the app side only Swift source counts.
    """
    r = subprocess.run(["grep", "-rnF", "--", literal, path], cwd=ROOT,
                       capture_output=True, text=True)
    files = set()
    for row in r.stdout.splitlines():
        fname, _, rest = row.partition(":")
        _, _, text = rest.partition(":")
        if only_ext and not fname.endswith(only_ext):
            continue
        if COMMENT.match(text):
            continue
        files.add(fname)
    return sorted(files)


def allowed():
    try:
        with open(ALLOW, encoding="utf-8") as fh:
            return {e["text"] for e in json.load(fh).get("one_surface_only", [])}
    except (OSError, ValueError):
        return set()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--range", default="origin/main..HEAD")
    ap.add_argument("--since", type=int, help="sweep the last N days instead of a range")
    args = ap.parse_args()

    if args.since:
        spec = ["log", "-p", f"--since={args.since}.days"]
    else:
        spec = ["diff", args.range]
    app_diff = git(*spec, "--", APP)
    web_diff = git(*spec, "--", WEB)

    ok_list = allowed()
    hits = []
    for literal in sorted(removed(app_diff, "app")):
        if literal in ok_list or present(literal, APP, ".swift"):
            continue
        where = present(literal, WEB)
        if where:
            hits.append(("the app", "the website", literal, where))
    for literal in sorted(removed(web_diff, "web")):
        if literal in ok_list or present(literal, WEB):
            continue
        where = present(literal, APP, ".swift")
        if where:
            hits.append(("the website", "the app", literal, where))

    if not hits:
        print("parity: nothing removed from one surface survives on the other")
        return 0
    print(f"parity: {len(hits)} line(s) taken out of one surface and still on the other")
    for gone, still, literal, where in hits:
        print(f'  removed from {gone}, still on {still}: "{literal}"')
        for w in where:
            print(f"      {w}")
    print("\nTake it out of both, or, if it lives on one surface on purpose, add it to\n"
          "data/parity-allow.json with the reason. The rule is CLAUDE.md's both-surfaces rule.")
    return 0 if args.since else 1


if __name__ == "__main__":
    sys.exit(main())
