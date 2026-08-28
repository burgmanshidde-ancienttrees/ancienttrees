#!/usr/bin/env python3
"""Refill the writable pile: recover a lead's genus from the tree's own name.

The problem this exists for, measured 2026-08-28. The cheapest lane in the whole
project is CLAUDE.md rule 1(a), "write what is already verified": a lead needs
only a name, a species and a position before a story can be written, and every
other field is optional by ruling. That pile was ~300 leads on 08-12. It was 54
on 08-28, about three write passes from dry, while 1,593 leads sat one field
short. 1,321 of them were short of exactly one thing: the species.

Where those trees come from explains why. 744 arrived from famous_trees.py, which
walks Commons' named-tree categories, and Commons names a category after the
tree, not after its taxon. So the field is empty for a reason that has nothing to
do with how well the tree is known: most of them arrive with photographs already
attached.

Registers cannot fix it. Measured across all 50 imported registers, 13,323 rows
carry both a coordinate and a species, and only 15 of the 776 positioned leads
had one within 30 metres: the registers and the famous lists cover different
countries.

The tree's own name can, because a tree called Bühler-Linde is a lime and one
called 1000jährige Eibe Gutau is a yew. That is a reading of the name rather than
a guess about the tree, and it reaches the genus and no further: a name says
Eiche, never Quercus petraea. CLAUDE.md's 2026-08-13 ruling covers exactly this
case ("if you dont know just put live and put the question for the users"), so
the output is "Oak (Quercus sp.)" with the uncertainty recorded on the lead.

    python3 scripts/refill.py             # report, writes nothing
    python3 scripts/refill.py --write     # fill and save

Idempotent: a lead that already has a species is never touched, so anything a
pass established by hand always wins. It fills LEADS and never data/cities, so
nothing here publishes anything; a write pass still looks at every tree.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import leads as L  # noqa: E402

LEXICON = os.path.join(ROOT, "data", "genus-names.json")


def lexicon():
    with open(LEXICON, encoding="utf-8") as fh:
        genera = json.load(fh)["genera"]
    single, phrases = {}, []
    for genus, spec in genera.items():
        for w in spec["words"]:
            w = w.lower()
            if " " in w:
                phrases.append((w, genus, spec["common"]))
            else:
                single.setdefault(w, (genus, spec["common"]))
    # Longest phrase first, so "dragon tree" is not beaten by a shorter entry.
    phrases.sort(key=lambda p: -len(p[0]))
    return single, phrases


def genus_of(name, single, phrases):
    """(genus, common) read out of a tree's name, or None.

    Word boundaries only. Substring matching turns Eglantine into a lime and
    Palmerston into a palm, and a wrong species on a lead is worse than an empty
    one because it looks answered.
    """
    low = str(name or "").lower()
    for w, genus, common in phrases:
        if w in low:
            return genus, common
    for token in re.split(r"[^0-9a-zà-öø-ÿ]+", low):
        if token in single:
            return single[token]
    return None


def refill(write=False):
    single, phrases = lexicon()
    blocking = L.rules()["blocking"]
    filled, by_genus, examples = 0, {}, []
    touched = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "leads", "*.json"))):
        try:
            doc = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(doc, dict):
            continue
        changed = False
        for entry in (doc.get("leads") or []):
            if not isinstance(entry, dict) or entry.get("species"):
                continue
            if L.classify(entry, blocking) is not None or L.is_done(entry):
                continue
            got = genus_of(entry.get("name"), single, phrases)
            if not got:
                continue
            genus, common = got
            entry["species"] = f"{common} ({genus} sp.)"
            # The writer has to know this came from the name, because the page
            # owes the reader the question. Without it a genus reads on the page
            # exactly like a species somebody established.
            entry["species_basis"] = "genus read from the tree's own name; ask the reader which species"
            filled += 1
            changed = True
            by_genus[genus] = by_genus.get(genus, 0) + 1
            if len(examples) < 12:
                examples.append((os.path.basename(path)[:-5], entry.get("name", "")[:40], common))
        if changed:
            touched[path] = doc
    if write:
        for path, doc in touched.items():
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(doc, fh, ensure_ascii=False, indent=1)
                fh.write("\n")
    return filled, by_genus, examples, len(touched)


def main():
    write = "--write" in sys.argv
    filled, by_genus, examples, files = refill(write)
    print(f"{filled} lead(s) given a genus from their own name, across {files} file(s)"
          + ("" if write else "   [report only, nothing written; pass --write]"))
    if by_genus:
        top = sorted(by_genus.items(), key=lambda kv: -kv[1])[:10]
        print("\n  most common:")
        for genus, n in top:
            print(f"    {n:4d}  {genus}")
        print("\n  examples:")
        for city, name, common in examples:
            print(f"    {city:22s} {name:42s} -> {common}")
    if not filled:
        print("  nothing to fill. Add words to data/genus-names.json and re-run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
