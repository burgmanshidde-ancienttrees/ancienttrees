#!/usr/bin/env python3
"""The website's copy rules, applied to the app's own strings.

The site has qa.py refusing em dashes, banned words and builder-speak in
rendered pages; the app had nothing, which is how "Nobody has published a
photograph of this tree under a licence we can use" shipped as hero copy on
every photo-less tree (found 2026-08-20). This scans the string literals in
the app target's Swift files, comments excluded, and fails on what the site
would refuse:

- em dashes (hard rule 3)
- the banned words from TONE_OF_VOICE.md
- builder-speak: explaining our own publishing or licence rules to the reader
- forever-promises, which are Hidde's pricing calls, not copy

Run: python3 scripts/appcopy.py         exits 1 on findings, 0 clean.
No CI hook for the app runs this automatically yet; it belongs in any app
session's finishing moves next to appfit.py.
"""
import pathlib
import re
import sys

APP = pathlib.Path(__file__).resolve().parent.parent / "ios/AncientTrees/AncientTrees"

PATTERNS = [
    ("em dash", re.compile("—")),
    ("banned word", re.compile(r"hidden gem|must-see|breathtaking|nestled", re.I)),
    ("builder-speak", re.compile(
        r"licence we can use|license we can use|our (own )?(rules|sources|curation)|"
        r"verified by us|our research|editorial (process|standard)", re.I)),
    ("forever-promise", re.compile(r"free forever|forever free|always free|never (pay|charge)", re.I)),
]

STRING = re.compile(r'"((?:[^"\\]|\\.)*)"')


def strings_in(line: str):
    code = line.split("//")[0] if not line.lstrip().startswith("//") else ""
    return STRING.findall(code)


def main() -> int:
    findings = []
    for path in sorted(APP.rglob("*.swift")):
        for n, line in enumerate(path.read_text().splitlines(), 1):
            for s in strings_in(line):
                for label, pat in PATTERNS:
                    if pat.search(s):
                        findings.append((path.relative_to(APP.parent.parent.parent), n, label, s[:80]))
    for f in findings:
        print(f"{f[0]}:{f[1]}  [{f[2]}]  \"{f[3]}\"")
    if findings:
        print(f"\n{len(findings)} finding(s). The site's qa would refuse these; so does this.")
        return 1
    print("app copy clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
