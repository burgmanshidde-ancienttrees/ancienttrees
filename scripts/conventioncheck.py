#!/usr/bin/env python3
"""A new interaction has to name the product it was copied from.

CLAUDE.md has carried the convention check since 2026-08-01 and its sharper
form since 2026-08-20 ("altijd conventies volgen geen eigen ideeen"). On
2026-08-28 it was broken again anyway: asked what happens to a photograph
already on the camera roll, a session invented a three-way policy fork instead
of spending two minutes reading what iNaturalist does. Hidde: "kijk naar
conventies aub en ga dit niet zelf zitten ontwerpen", and then, the part this
file answers, "can we add that to our forever work process so i dont have to
ask it every time".

Written three times is written twice too many, so this is the ratchet: a lesson
that turns up on two different days becomes a check.

WHAT IT CHECKS, and it is deliberately dumb. A file ADDED under a screens or
components directory must say, somewhere in its opening comment, which product
its interaction came from. It does not judge the answer, and it cannot: no
script knows whether Airbnb really does it that way. It only refuses the case
where nobody wrote a reference down at all, which is exactly the shape of
designing from your own head.

WHAT IT DELIBERATELY IGNORES: files that were merely CHANGED. The rule is about
new interactions and has never covered copy tweaks, styling, or reuse of a
pattern the site already has, and a check that fires on every edit is a check
that gets bypassed within a week.

Escape hatch, on purpose: a header line saying "Convention: none, because X"
passes. The point is to force the sentence to exist, not to win the argument.

    python3 scripts/conventioncheck.py              # against origin/main
    python3 scripts/conventioncheck.py --base HEAD~3
    python3 scripts/conventioncheck.py path/to/File.swift   # one file
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Where a new user-facing interaction lands. Data, helpers and tests are not
# interactions and are not covered.
WATCHED = (
    "ios/AncientTrees/AncientTrees/Screens/",
    "site/src/components/",
)

# The opening comment, generously read: Swift and Astro both put it at the top.
HEADER_LINES = 60

# Either an explicit line, or the name of a product we are allowed to copy.
# The list is the standing references from CLAUDE.md plus the ones already
# cited in CONVENTIONS.md; add to it when a new reference is genuinely used.
MARKERS = re.compile(
    r"convention|CONVENTIONS\.md|"
    r"alltrails|google maps|airbnb|picturethis|inaturalist|seek|"
    r"strava|geocaching|apple|apple's|untappd|komoot|citymapper|"
    r"the system (camera|share sheet|picker)",
    re.I,
)


def sh(*args):
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                              timeout=20).stdout
    except Exception:
        return ""


def added_files(base):
    out = sh("git", "diff", "--name-only", "--diff-filter=A", base, "HEAD")
    return [p for p in out.splitlines() if p.startswith(WATCHED)]


def names_a_reference(path):
    f = ROOT / path
    if not f.exists():
        return True  # deleted again since; nothing to judge
    head = "\n".join(f.read_text(errors="replace").splitlines()[:HEADER_LINES])
    return bool(MARKERS.search(head))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    base = "origin/main"
    if "--base" in sys.argv:
        base = sys.argv[sys.argv.index("--base") + 1]
        args = [a for a in args if a != base]

    files = args or added_files(base)
    if not files:
        return 0

    missing = [p for p in files if not names_a_reference(p)]
    if not missing:
        print(f"conventioncheck: {len(files)} new interaction file(s), all name a reference")
        return 0

    print("conventioncheck: a new interaction that names no reference\n")
    for p in missing:
        print(f"  {p}")
    print("""
Say in the file's opening comment which product this interaction was copied
from and what that product does. If you have not looked yet, look now: the
answer is usually two minutes of reading and it is the rule Hidde has given
twice (2026-08-01, and 2026-08-20 "altijd conventies volgen geen eigen ideeen").

Already looked it up? Add the entry to CONVENTIONS.md and cite it here.
Genuinely no precedent? Write "Convention: none, because ..." and say why.""")
    return 1


if __name__ == "__main__":
    sys.exit(main())
