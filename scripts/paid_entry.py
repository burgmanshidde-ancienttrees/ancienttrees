#!/usr/bin/env python3
"""Mark which trees stand behind a ticket, as a FIELD rather than as a guess.

Hidde, 2026-08-24: give trees behind a ticket their own mark on the pin, say at
the top of the tree page where to buy one, and keep them out of the walks.

All three need to know which trees those are, and `access` is free prose. A
keyword sweep over it matches 302 trees and is wrong: three Hobart entries
saying "Free, public botanical garden ... gold-coin donation" match on the word
entry. Putting a ticket badge on a free garden is worse than having no badge,
because it tells somebody to pay for something that costs nothing.

So this writes `paid_entry` onto the tree, and only where the prose is
unambiguous: it names money, or it says paid entry in so many words, AND it does
not also say free. 160 of 1,842 trees at the time of writing. The 40 that say
both are printed for a person, never guessed.

    python3 scripts/paid_entry.py            # what it would do
    python3 scripts/paid_entry.py --write    # do it
    python3 scripts/paid_entry.py --review   # the ambiguous ones, for a pass
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MONEY = re.compile(r'[€£$]\s?\d|\b\d+(?:[.,]\d+)?\s?(?:euro|eur|pound|dollar)\b', re.I)
PAID = re.compile(r'\b(paid entry|entry fee|admission fee|admission charge|'
                  r'ticket(?:ed)? (?:required|needed|entry)|requires a ticket|'
                  r'entrance fee)\b', re.I)
FREE = re.compile(r'^\s*free\b|\bfree (?:entry|access|to enter|and open)\b|'
                  r'\bno charge\b|\bgratis\b', re.I)


def verdict(access):
    """True, False, or None when a person has to decide."""
    a = access or ""
    says_paid = bool(MONEY.search(a) or PAID.search(a))
    says_free = bool(FREE.search(a))
    if says_paid and says_free:
        return None
    return says_paid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--review", action="store_true")
    args = ap.parse_args()

    paid, ambiguous, changed, files = 0, [], 0, 0
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        touched = False
        for t in d.get("trees", []):
            v = verdict(t.get("access"))
            if v is None:
                ambiguous.append((t["id"], (t.get("access") or "")[:100]))
                continue
            if v:
                paid += 1
            # bool(), or every free tree counts as a change: a missing
            # field reads as None and None != False.
            if bool(t.get("paid_entry")) != v:
                if v:
                    t["paid_entry"] = True
                else:
                    t.pop("paid_entry", None)
                changed += 1
                touched = True
        if touched and args.write:
            files += 1
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(d, fh, ensure_ascii=False, indent=2)
                fh.write("\n")

    if args.review:
        print("%d trees say both free and a fee. A person decides these:\n" % len(ambiguous))
        for i, a in ambiguous:
            print("  %-10s %s" % (i, a))
        return 0

    print("%d behind a ticket, %d ambiguous, %d field(s) %s"
          % (paid, len(ambiguous), changed, "written" if args.write else "would change"))
    if not args.write and changed:
        print("python3 scripts/paid_entry.py --write")
    if ambiguous:
        print("python3 scripts/paid_entry.py --review   # the %d nobody may guess" % len(ambiguous))
    return 0


if __name__ == "__main__":
    sys.exit(main())
