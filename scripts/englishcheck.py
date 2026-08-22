#!/usr/bin/env python3
"""British spelling, and the sentence shapes that read as translated English.

Hidde, 2026-08-22: "kom ik toch echt veel scheve Engelse zinnen tegen
voornamelijk in het product. Kun je gewoon British English aanhouden en alles
eens nalopen op slechte zinsvormen?" TONE_OF_VOICE.md already says "a bit more
Dutch, a bit less American" about the register; it has never said which
spelling, so both have been shipping side by side.

This finds two different things and keeps them apart:

  SPELLING   American forms with a British equivalent. Mechanical, safe to fix
             in bulk, and the only half a script can be sure about.
  SHAPE      the constructions that make a sentence read as translated: a
             sentence opening with "Also", a dangling "which is why" fragment,
             stacked "that that", "the most X-est", "more better", a comma
             splice before "and then", "informations", "in the moment", and
             the Dutch word order that survives translation ("Here you find",
             "There stands", "It concerns").

The second half is deliberately conservative: it flags candidates for a human
to read, never rewrites. A false positive costs a glance; a bulk rewrite of
prose nobody read costs a voice.

    python3 scripts/englishcheck.py             # product copy (site/src, ios)
    python3 scripts/englishcheck.py --stories   # the tree stories as well
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# American -> British. Only pairs where the British form is unambiguous and the
# American one is not also a different word (no "program", which is correct for
# software; no "meter", which is an instrument).
SPELLING = {
    "color": "colour", "colors": "colours", "colored": "coloured",
    "favorite": "favourite", "favorites": "favourites",
    "neighbor": "neighbour", "neighbors": "neighbours",
    "neighborhood": "neighbourhood", "neighborhoods": "neighbourhoods",
    "honor": "honour", "honored": "honoured", "harbor": "harbour",
    "labor": "labour", "rumor": "rumour", "odor": "odour",
    "center": "centre", "centers": "centres", "centered": "centred",
    "meters": "metres", "kilometers": "kilometres", "liter": "litre",
    "theater": "theatre", "fiber": "fibre",
    "traveled": "travelled", "traveling": "travelling", "traveler": "traveller",
    "canceled": "cancelled", "modeling": "modelling", "labeled": "labelled",
    "signaled": "signalled", "marveled": "marvelled",
    "realize": "realise", "realized": "realised", "recognize": "recognise",
    "recognized": "recognised", "organize": "organise", "organized": "organised",
    "apologize": "apologise", "memorialize": "memorialise",
    "defense": "defence", "offense": "offence", "license": "licence",
    "practicing": "practising", "gray": "grey",
    "aging": "ageing", "plow": "plough", "mold": "mould", "smolder": "smoulder",
    "archeology": "archaeology", "archeological": "archaeological",
    "medieval": "mediaeval",   # both are current; flagged, never auto-fixed
}
# The one above that is a real choice rather than an error.
SOFT = {"medieval"}

SHAPES = [
    (r"\bAlso,? [a-z]", "a sentence opening with Also reads as a translated afterthought"),
    (r"\bHere you (?:can )?find\b", "Dutch word order: 'Here you find'"),
    (r"\bThere stands?\b", "Dutch word order: 'There stands'"),
    (r"\bIt concerns\b", "'Het betreft' translated straight through"),
    (r"\binformations\b", "information has no plural"),
    (r"\badvices\b", "advice has no plural"),
    (r"\bin the moment\b", "'at the moment', or just 'now'"),
    (r"\bthe most \w+est\b", "double superlative"),
    (r"\bmore \w+er\b", "double comparative"),
    (r"\bthat that\b", "stacked that"),
    (r"\bof the of\b", "duplicated preposition"),
    (r"\ba the\b|\bthe a\b", "two articles"),
    (r"\bwich\b|\bteh\b|\bhte\b", "typo"),
    (r"\bwhich is why\.", "a which-is-why fragment left hanging"),
    (r"\bare exist\b|\bis exist\b", "verb doubled"),
    (r"\bcan able to\b|\bcan to\b", "modal doubled"),
    (r"\bsince \d+ years\b", "'for N years', not 'since N years'"),
    (r"\bwith \d+ years old\b", "'aged N', or 'N years old'"),
    (r"\bmake a walk\b|\bmake a picture\b", "'take a walk', 'take a photograph'"),
    (r"\bhow does it look like\b", "'what does it look like'"),
    (r"\bnext to that\b", "'besides that' or just 'and'"),
    # The two that today's reading pass actually caught, kept so they cannot
    # return: a label truncated mid-thought, and the comma splice that a Dutch
    # ear does not hear.
    # Conjunctions only. An earlier version included prepositions and flagged
    # "the trees you stand in front of", which is correct English and better
    # than the alternative; a rule that corrects good writing is worse than no
    # rule.
    (r"\b(and|or|but|when)\s*$",
     "ends on a conjunction: a truncated label or a sentence that lost its end"),
    # A comma-splice pattern was tried and dropped the same hour: it flagged
    # "This map is missing far more cities than it has, and the trees that
    # matter most are the ones locals already know about", which is a correct
    # compound sentence. Two clauses joined by a comma and a conjunction are
    # not a splice, and no cheap regex tells the two apart.
]

# ONLY WHAT A READER SEES. The first version of this counted 183 American
# spellings and every one of them was code: SwiftUI's Color, .center alignment,
# the licence field in our own JSON. Renaming those would break the app and fix
# nothing a visitor reads.
#
# The rule that separates the two, and it is almost perfect on this codebase:
# reader-facing copy has a SPACE in it. An identifier does not. So this reads
# quoted strings and tag text, keeps the ones with a space and a real word, and
# throws away urls, keys, class lists and file paths.
SKIP_LINE = re.compile(r"^\s*(//|/\*|\*|#|import )")
STRING = re.compile(r'"([^"\\]{6,240})"')
TAGTEXT = re.compile(r">([^<>{}]{8,240})<")
NOT_COPY = re.compile(r"://|[{}<>$]|^[a-z0-9_.\-/]+$|^[A-Z_]+$|\bpx\b|^\s*[\d.,%\s]+$")


def visible_bits(text, is_markup):
    """Every string on the page a human could read, one per yield."""
    for m in STRING.finditer(text):
        v = m.group(1)
        if " " in v and not NOT_COPY.search(v):
            yield v
    if is_markup:
        for m in TAGTEXT.finditer(text):
            v = m.group(1).strip()
            if " " in v and not NOT_COPY.search(v):
                yield v


def files(stories):
    out = []
    for pat in ("site/src/**/*.astro", "site/src/**/*.ts", "site/public/**/*.html"):
        out += glob.glob(os.path.join(ROOT, pat), recursive=True)
    out += glob.glob(os.path.join(ROOT, "ios/AncientTrees/AncientTrees/**/*.swift"), recursive=True)
    if stories:
        out += glob.glob(os.path.join(ROOT, "data/cities/*.json"))
    return sorted(out)


def main():
    stories = "--stories" in sys.argv
    spell, shape = [], []
    for path in files(stories):
        rel = os.path.relpath(path, ROOT)
        try:
            text = open(path, encoding="utf-8").read()
        except Exception:
            continue
        markup = path.endswith((".astro", ".html"))
        for n, line in enumerate(text.splitlines(), 1):
            if SKIP_LINE.match(line):
                continue
            for bit in visible_bits(line, markup):
                low = bit.lower()
                for us, uk in SPELLING.items():
                    if re.search(r"\b%s\b" % us, low):
                        spell.append((rel, n, us, uk, bit[:100], us in SOFT))
                for pat, why in SHAPES:
                    if re.search(pat, bit):
                        shape.append((rel, n, why, bit[:110]))
    print("SPELLING: %d American forms" % len(spell))
    for rel, n, us, uk, line, soft in spell[:40]:
        print("  %-52s %s -> %s%s" % ("%s:%d" % (rel, n), us, uk, "  (a choice, not an error)" if soft else ""))
    if len(spell) > 40:
        print("  ... and %d more" % (len(spell) - 40))
    print("\nSHAPE: %d candidates for a human to read" % len(shape))
    for rel, n, why, line in shape[:40]:
        print("  %-52s %s" % ("%s:%d" % (rel, n), why))
        print("      %s" % line)
    return 1 if spell or shape else 0


if __name__ == "__main__":
    sys.exit(main())
