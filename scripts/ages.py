#!/usr/bin/env python3
"""Derive a broad age band from a trunk girth, for trees that carry no age.

The third sibling of girths.py and heights.py, and the one they were both
feeding. CLAUDE.md, 2026-08-16, on Hidde's ruling that an age may be estimated:

    "an estimate is DERIVED and says what from; an invention is not. Girth plus
    a published growth rate for that species is dendrology, and it is how every
    register in the world dates a tree."

and, a few lines further down, on why nothing had ever run:

    "the day there are a few hundred of them the estimating becomes a script
    that runs over all of them at once instead of a judgement made one tree at
    a time."

There are 1,354 girths now, so this is that script.

    python3 scripts/ages.py --report   # say what would happen, write nothing
    python3 scripts/ages.py            # write it

Re-runnable, and it never touches a tree that already states an age from any
source. A figure somebody measured or wrote down always beats arithmetic.

THE METHOD is Mitchell's rule, which is what the field actually uses: a trunk
puts on a roughly constant amount of GIRTH each year, so age is girth divided
by that rate. The rate is not one number and pretending it is would be the
whole error. A broadleaf in open parkland runs near 2.5 cm of girth a year and
the same species in woodland shade nearer 1.5, so the honest output of the sum
is a BAND a factor of 1.7 wide, and it is published as a band. Narrowing it to
a single number to look confident is the same error as a faked pin.

    age_min = girth_cm / 2.5      the fast, open-grown end
    age_max = girth_cm / 1.5      the slow, shaded end

WHAT IT REFUSES, which is most of the pile and is the point. The rate above is
published for TEMPERATE BROADLEAVES and for nothing else, so the allow list
below is a closed list of genera rather than a default with exceptions. 219
published trees carry a girth and no age; 37 of them come through this list and
the two bounds below. The other 182 are refused with a reason written into the
ledger, because a refusal somebody can read is what stops the next run
rediscovering it.

The four classes that are refused on purpose:

  Conifers, and the gymnosperms generally. The published rate is not theirs,
  and the worst of them is the YEW, whose growth all but stops for centuries
  and which every guide to this method names as the species it cannot do. A
  Mitchell age on a yew is a number with no relationship to the tree.

  Subtropical and tropical species: figs, camphor, rain trees, Metrosideros.
  No dormant season, so the premise of an annual increment does not hold.

  The fast growers, where 2.5 cm a year is not the ceiling but the floor:
  plane, poplar, willow, wingnut, ailanthus. These would be aged at several
  times their real age, and a plane is our second commonest girth-bearing
  species, so this refusal costs twelve trees and is still right.

  Ensembles. A girth is one trunk and the entry describes several, so the sum
  would age the group from whichever stem somebody happened to measure.

And two bounds on the answer itself. A band whose OLD end lands under a century
is refused: below that the arithmetic is saying "this tree is young", which is
a guess we have no business publishing and which makes the page worse rather
than better (preflight's note_a_young_tree_is_not_ancient is the same rule seen
from the other side). And a trunk over 6 m round is refused, for a reason we
measured rather than assumed; see below.

HOW OFTEN IT IS RIGHT, measured 2026-09-11 against the 300 published trees that
carry BOTH a girth and an age somebody wrote down. The band contains their
stated age 6 times in 10. The misses are not scattered, which is the useful
part: a quarter of them are us being TOO YOUNG, and they crowd into the big
trunks, because girth growth slows sharply once a tree is genuinely old and a
linear rule cannot see that. Sorted by girth, we under-age 6 to 23 percent of
trees below 5 m round and 30 to 45 percent of those above 6 m. Hence the cap.
The Stelmuze Oak is the shape of the failure: 13 m round, this sum says 500 to
900 years, its own country says 1,500 to 2,000.

Two honesty notes on that 6-in-10. It is soft in both directions, because a
good few of the ages it is checked against were themselves derived from a girth
by a register doing this same arithmetic, and others are traditional figures
rather than measurements (most of the Japanese cherries in that set). And the
rate was NOT tuned to make the number look better: widening the slow end to
1 cm a year takes agreement to 74 percent, and 1 cm a year is outside what the
sources publish, so fitting our own data would have been the fabrication this
script exists to avoid. The rate comes from the literature, the cap comes from
the evidence, and the agreement is reported rather than optimised.

HOW IT SAYS WHAT IT IS. Three places, none of them optional:

  age_basis "girth", the machine-readable flag. site/src/lib/tree-copy.ts reads
  it and refuses to quote a derived age as a flat number in a page title, the
  way it already refuses a disputed one. A band in the data must not become a
  fact in a heading.

  age_estimate carries the basis in its own sentence, after the comma. The tree
  page prints the part before the first comma in the facts chip and the whole
  string in the Age estimate row, so the reader meets the number first and the
  basis with it, and no rendering had to be built for that.

  verify_notes, for the next person to work on the tree.

Sources for the rate, read 2026-09-11:
  https://ati.woodlandtrust.org.uk/how-to-record/recording-guide/how-to-record-the-girth-of-a-tree/
  https://www.ancienttreeforum.org.uk/wp-content/uploads/2015/03/ATHmeasureleaflet1.pdf
  https://en.wikipedia.org/wiki/Tree_girth_measurement
  CONVENTIONS.md, "Asking a contributor how thick a tree is"
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "data", "research", "ages-from-girth.json")

# Girth in cm per year. Both ends published for temperate broadleaves: open
# parkland near the first, woodland shade near the second.
FAST, SLOW = 2.5, 1.5

# Temperate broadleaf genera and species the rate is published for. A closed
# list: anything not named here is refused, which is why it reads as a list of
# ordinary European park trees and not as a taxonomy.
ALLOW = (
    "Quercus robur", "Quercus petraea", "Quercus pubescens", "Quercus cerris",
    "Quercus frainetto", "Quercus dalechampii",
    "Tilia", "Fagus sylvatica", "Aesculus", "Castanea sativa",
    "Fraxinus", "Acer", "Ulmus", "Carpinus", "Juglans", "Celtis australis",
    "Morus", "Sorbus", "Betula", "Alnus", "Prunus", "Pyrus", "Malus",
    "Corylus", "Liriodendron", "Liquidambar", "Nyssa",
)

# An entry that describes more than one trunk. The girth belongs to one of
# them and the sum would quietly claim it for all.
ENSEMBLE = re.compile(
    r"\b(oaks|trees|limes|lindens|elms|beeches|planes|cedars|pines|yews|"
    r"chestnuts|mulberries|maples|poplars|willows|cypresses|olives|avenue|"
    r"alley|row|grove|pair|twins|double)\b", re.I)

MAX_GIRTH_CM = 600
MIN_OLD_END = 100


def scientific(species):
    """The name inside the parentheses, which hard rule 9 makes the arbiter."""
    m = re.search(r"\(([^)]*)\)", species or "")
    return (m.group(1) if m else (species or "")).strip()


def step(value):
    return 25 if value < 200 else 50


def floor_to(value):
    s = step(value)
    return int(value // s * s)


def ceil_to(value):
    s = step(value)
    return int(-(-value // s) * s)


def metres(girth_cm):
    return ("%.2f" % (girth_cm / 100.0)).rstrip("0").rstrip(".")


def judge(tree):
    """(age_min, age_max) when the method applies, else (None, reason)."""
    girth = tree.get("girth_cm")
    if not girth:
        return None, "no girth"
    if tree.get("age_estimate") or tree.get("age_min") or tree.get("age_max"):
        return None, "already carries an age"
    sci = scientific(tree.get("species"))
    if not any(sci.startswith(a) for a in ALLOW):
        return None, "species outside the published rate: %s" % (sci or "unnamed")
    if ENSEMBLE.search(tree.get("name") or ""):
        return None, "entry describes more than one trunk"
    if girth > MAX_GIRTH_CM:
        return None, ("girth %d cm is past where the linear rule holds; we "
                      "measurably under-age trunks this size" % girth)
    lo, hi = floor_to(girth / FAST), ceil_to(girth / SLOW)
    if hi < MIN_OLD_END:
        return None, "band tops out at %d years, which is not an age worth publishing" % hi
    return (lo, hi), None


def sentence(lo, hi, girth):
    return ("roughly %d to %d years, judged from a trunk %s m round"
            % (lo, hi, metres(girth)))


def main():
    report = "--report" in sys.argv
    written, refused, ledger = [], [], []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        with open(path, encoding="utf-8") as fh:
            city = json.load(fh)
        touched = False
        for tree in city.get("trees", []):
            if not tree.get("girth_cm"):
                continue
            band, why = judge(tree)
            if band is None:
                if why not in ("no girth", "already carries an age"):
                    refused.append((tree.get("id"), city.get("city"), why))
                continue
            lo, hi = band
            said = sentence(lo, hi, tree["girth_cm"])
            row = {"id": tree.get("id"), "city": city.get("city"),
                   "name": tree.get("name"), "species": tree.get("species"),
                   "girth_cm": tree["girth_cm"], "age_min": lo, "age_max": hi}
            ledger.append(row)
            written.append("%-20s %-34s %5d cm  %4d-%-4d  %s"
                           % (city.get("city", "")[:20],
                              scientific(tree.get("species"))[:34],
                              tree["girth_cm"], lo, hi, tree.get("name", "")[:34]))
            if report:
                continue
            tree["age_estimate"] = said
            tree["age_min"], tree["age_max"] = lo, hi
            tree["age_basis"] = "girth"
            note = ("Age derived from girth, not from a source: %d cm at "
                    "Mitchell's 2.5 to 1.5 cm of girth a year for an open-grown "
                    "to shaded temperate broadleaf. Any measured or documented "
                    "age replaces this outright." % tree["girth_cm"])
            tree["verify_notes"] = ((tree.get("verify_notes") or "").strip()
                                    + (" " if tree.get("verify_notes") else "")
                                    + note).strip()
            touched = True
        if touched and not report:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(city, fh, ensure_ascii=False, indent=2)
                fh.write("\n")

    for line in written:
        print(line)
    print("\n%d trees %s an age band from girth; %d refused."
          % (len(written), "would take" if report else "took", len(refused)))
    tally = {}
    for _, _, why in refused:
        key = why.split(":")[0]
        tally[key] = tally.get(key, 0) + 1
    for key in sorted(tally, key=lambda k: -tally[k]):
        print("  %4d  %s" % (tally[key], key))

    if not report:
        with open(LEDGER, "w", encoding="utf-8") as fh:
            json.dump({"method": "Mitchell's rule, %s to %s cm of girth a year"
                                 % (FAST, SLOW),
                       "written": ledger,
                       "refused": [{"id": i, "city": c, "why": w}
                                   for i, c, w in refused]},
                      fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print("\nLedger: %s" % os.path.relpath(LEDGER, ROOT))


if __name__ == "__main__":
    main()
