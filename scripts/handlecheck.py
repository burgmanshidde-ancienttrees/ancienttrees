#!/usr/bin/env python3
"""One sheet handle in the app, ours.

Hidde, 2026-10-10: "wederom dat grijze balkje bovenaan de overlay slider
verkeerd uitgelijnd, dat gebeurt zo vaak, kun je dat niet meer doen". The
system's drag indicator sits 5 points from the sheet's edge; the app's handle
(BrandSheetHandle in Kit/Style.swift) sits 12 points down, the website's
place. Four sheets still showed the system's and one showed ours, so the same
grey bar sat in two places depending on which sheet was open.

This refuses any Swift file that asks the system for its visible indicator.
A sheet gets its handle from `.brandSheetHandle()`, and nowhere else.
Removing this check needs Hidde.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "ios" / "AncientTrees"
BAD = re.compile(r"\.presentationDragIndicator\(\s*\.(visible|automatic)\s*\)")


def main() -> int:
    hits = []
    for f in sorted(ROOT.rglob("*.swift")):
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip().startswith("//"):
                continue
            if BAD.search(line):
                hits.append(f"{f.relative_to(ROOT.parent.parent)}:{n}: {line.strip()}")
    if hits:
        print("handlecheck: a sheet shows the system's drag indicator; use .brandSheetHandle() instead")
        print("\n".join(hits))
        return 1
    print("handlecheck: every sheet wears the one handle")
    return 0


if __name__ == "__main__":
    sys.exit(main())
