#!/usr/bin/env python3
"""Do the translated UI strings fit the limits the BUILD enforces?

Written 2026-09-17. The build already catches this: Base.astro throws on a
title over TITLE_MAX or a description over DESC_MAX, and it did, on the German
map title at 65 characters. What it cost was the feedback loop. A full build is
five minutes, Astro stops at the FIRST page that throws, and eleven titles were
over in six languages, so finding them one build at a time would have been most
of an hour.

So this is not a new rule, it is the same rule read a second earlier. It parses
the TABLE in site/src/lib/i18n.ts and measures the same two fields for every
language before anything is built.

The cause is worth recording because it will recur: a translation brief that
does not state a length limit will come back over it, in every language at
once, because the languages this site serves run longer than English. German
and French ran 10 to 20 percent over on the same sentence. Any brief asking for
a title or a meta description states the limit.

Usage:
  python3 scripts/uistrings_check.py
"""
import json
import re
import sys

I18N = "site/src/lib/i18n.ts"
TITLE_MAX = 60
DESC_MAX = 155
# Only the keys that actually become a <title> or a <meta description>. An
# earlier version matched on the suffix and flagged appPitchTreeTitle, which is
# a heading inside a card and has no such limit. A check that cries wolf about
# a string the build is happy with teaches people to ignore it.
TITLE_KEYS = ("citiesTitle", "exploreTitle", "homeTitle")
DESC_KEYS = ("citiesDescription", "exploreDescription", "homeDescription")


def main():
    try:
        src = open(I18N, encoding="utf-8").read()
    except OSError:
        print("run me from the repo root")
        return 1
    start = src.find("const TABLE")
    if start < 0:
        print("no TABLE in %s" % I18N)
        return 1
    table = src[start:]

    problems = []
    for m in re.finditer(r'^  "?(\w{2})"?:\s*\{(.*?)^  \},', table, re.S | re.M):
        lang, block = m.group(1), m.group(2)
        for km in re.finditer(r'^    (\w+):\s*"((?:[^"\\]|\\.)*)",', block, re.M):
            # json.loads unescapes \" and \\ without touching UTF-8. An
            # earlier version used unicode_escape, which mangles every
            # multi-byte character and reported Japanese titles as three times
            # their real length: 23 characters read as 69.
            try:
                val = json.loads('"' + km.group(2) + '"')
            except ValueError:
                continue
            key = km.group(1)
            limit = TITLE_MAX if key in TITLE_KEYS else (
                DESC_MAX if key in DESC_KEYS else None)
            if limit and len(val) > limit:
                problems.append((lang, key, len(val), limit, val[:56]))

    for lang, key, n, limit, head in sorted(problems, key=lambda p: -p[2]):
        print("  %-3s %-22s %3d > %d  %s..." % (lang, key, n, limit, head))
    if problems:
        print("\n%d string(s) over the limit the build enforces. Astro stops at the"
              % len(problems))
        print("first one, so fix them all before spending another build on it.")
        return 1
    print("UI strings: every title and description inside the build's own limits.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
