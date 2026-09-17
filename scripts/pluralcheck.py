#!/usr/bin/env python3
"""A count typed into a string with the plural hardcoded is a bug on the day the count is 1.

The bug class recurred three times before this existed. 2026-09-10:
MapSearch.swift, "1 trees" for a single-tree place under Places. 2026-09-12:
Home.swift's CityView header and its homepage city shelf, both "1 trees" on
a single-tree city (fixed with a shared helper, `treesLabel()` in
Kit/Models.swift). The same afternoon this check was written: Walks.swift's
walk-list row and Home.swift's walk card both interpolated "\\(count) trees"
with no singular branch at all, one screen away from the two the reviewer had
already caught, because the reviewer reads screenshots and neither of those
had a single-tree walk in the fixture data to expose it.

Every one of these read fine to the person who wrote it, because English
plurals are invisible until the count is exactly 1, which is also always the
count nobody tests with. PRINCIPLES.md #9: text a loop generates is guilty
until read aloud.

Kit/Models.swift's `treesLabel(_ n: Int) -> String` is the fix; an inline
`n == 1 ? "1 tree" : "\\(n) trees"` passes too, because it says the same
thing without needing the helper's import. What fails is the bare
interpolation with the plural word hardcoded onto it.

Run it: python3 scripts/pluralcheck.py
"""

import pathlib
import re
import sys

APP = pathlib.Path(__file__).resolve().parent.parent / "ios" / "AncientTrees" / "AncientTrees"

# `\(anything.count) trees` or `\(anything.count) walks`, the plural word
# literally in the string. A line that also says `treesLabel` or checks
# `== 1` has already handled it, so those are not findings.
BARE_PLURAL = re.compile(r'\\\([^()]*\.count\)\s+(trees|walks|places|cities)\b')
HANDLED = re.compile(r"treesLabel|walksLabel|placesLabel|citiesLabel|==\s*1\b")


def main() -> int:
    findings = []
    for path in sorted(APP.rglob("*.swift")):
        rel = path.relative_to(APP).as_posix()
        for n, line in enumerate(path.read_text().splitlines(), 1):
            if line.lstrip().startswith("//"):
                continue
            if BARE_PLURAL.search(line) and not HANDLED.search(line):
                findings.append((rel, n, line.strip()))

    if not findings:
        print("no bare plural: every count-into-string interpolation handles 1")
        return 0

    print(f"{len(findings)} string(s) hardcode a plural onto a count that can be 1:\n")
    for rel, n, line in findings:
        print(f"  {rel}:{n}\n      {line}")
    print("\nUse treesLabel(n) (Kit/Models.swift) or an inline "
          '`n == 1 ? "1 thing" : "\\(n) things"`.')
    return 1


if __name__ == "__main__":
    sys.exit(main())
