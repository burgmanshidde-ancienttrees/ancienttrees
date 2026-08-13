#!/usr/bin/env python3
"""Check every imported register for rows that contradict their own status.

Written 2026-08-13, the day three registers in a row turned out to say a tree
was alive in one field and gone in another:

  - Catalonia (2026-07-30) shipped a DIAGNOSI field on all 302 records: 191
    alive, 53 in advanced decline, 58 outright dead. That is where the survey's
    "look for a vitality field before anything else" rule came from.
  - Bordeaux (this morning) carries `status_life` VIVANT on seven trees that
    also carry a `date_disparition`, one felled in June 2025. The register
    updates the felling date and does not update the status.
  - Portland (this afternoon) excludes removed trees by `Delist_Date`, and
    21 further rows state a removal in their free-text `notes` while passing
    that filter. The city's own 2026 delisting ordinance then confirmed two
    more that the register had not caught up with at all.

Three on one day is past the ratchet's threshold, so it is a script rather than
a fourth note. Run it after importing any register, and before briefing a pass
against one:

    python3 scripts/registercheck.py

What it does NOT do: decide whether a tree is alive. It finds rows where the
source disagrees with itself, which is a prompt to look, not a verdict. Only a
verification pass confirms a tree stands.

**Free text flags, structured fields block.** This is the rule the Portland pass
forced, over three tries, and it is the useful part of the whole exercise:

  - A first cut keyed on the word "dead" and blocked a living pin oak whose note
    reads "some dead wood ~5% canopy", a health observation on a healthy tree.
  - A second cut keyed on "cut down" and blocked the Rockey Elm, whose note reads
    "condemned to be cut down by the Portland City Council in 1963, but a devoted
    group of tree lovers saved its life". That tree's whole story is that it
    survived, and we nearly deleted it for surviving.

So a status field, a delist date and an ownership field may set
`publishable: false` on their own. Prose may only set `check_alive: true`, which
asks a pass to look. Anything else is a machine reading a sentence it cannot
parse and throwing away a tree for it.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# A statement that the tree is GONE. Not health language: "dead wood",
# "deadwood", "dead branches" and "dead end" are all about living trees.
GONE = re.compile(
    r"\bremoved\b|\bfelled\b|\bcut down\b|\bdelisted\b|\bstump only\b|"
    r"\bno longer (?:present|standing|exists)\b|\btree (?:is )?dead\b|\bdied\b",
    re.I,
)
# Prose that talks about removal while describing a tree that is still there.
# Every one of these was a real false positive on Portland's register, and each
# would have deleted a living tree: a rescue story, a health note, and an
# orchard remnant described as the last one remaining.
SURVIVED = re.compile(
    r"\bsaved\b|\bspared\b|\breprieve\b|\bcondemned\b|\bthreatened\b|"
    r"\bwas to be\b|\blast remaining\b|\bonly (?:one|tree|elm|remaining)\b|"
    r"\bstill (?:stands|standing)\b|\bdead ?wood\b",
    re.I,
)
# Fields that assert the tree is fine.
ALIVE_VALUES = {"vivant", "alive", "aktuell", "live", "good", "healthy", "standing"}
# Fields whose mere presence means the tree is gone.
GONE_FIELDS = ("date_disparition", "delist_date", "removal_date", "date_removed",
               "felled", "date_felled")


def rows_of(doc):
    if isinstance(doc, list):
        return doc
    for key in ("entries", "trees", "rows", "data"):
        if isinstance(doc.get(key), list):
            return doc[key]
    return []


def check(path):
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    rows = rows_of(doc)
    out = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        alive = [k for k, v in r.items()
                 if isinstance(v, str) and v.strip().lower() in ALIVE_VALUES]
        gone_field = [k for k in GONE_FIELDS if r.get(k)]
        gone_text = [k for k, v in r.items()
                     if isinstance(v, str) and k not in ("species", "common_name", "name")
                     and GONE.search(v) and not SURVIVED.search(v)]
        if (gone_field or gone_text) and r.get("publishable") is not False:
            out.append((r.get("name") or r.get("common_name") or r.get("species") or "?",
                        (alive[0] + "=" + r[alive[0]]) if alive else "no status field",
                        (gone_field + gone_text)[0]))
    return rows, out


def main():
    problems = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "registers", "*.json"))):
        rows, bad = check(path)
        name = os.path.basename(path)
        if not bad:
            print("  ok    %-42s %d rows" % (name, len(rows)))
            continue
        problems += len(bad)
        print("  CHECK %-42s %d of %d rows contradict themselves" % (name, len(bad), len(rows)))
        for label, alive, field in bad[:4]:
            print("          %-30s %-24s gone per %s" % (str(label)[:30], alive[:24], field))
        if len(bad) > 4:
            print("          ... and %d more" % (len(bad) - 4))
    print("\n%d row(s) need a look. Mark each `publishable: false` once confirmed, "
          "or true if the source is simply noisy." % problems)
    return 0


if __name__ == "__main__":
    sys.exit(main())
