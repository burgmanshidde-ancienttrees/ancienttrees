#!/usr/bin/env python3
"""Grep the app's user-facing sentences for the way I keep writing them badly.

Hidde, 2026-08-24, on "Walk to it and photograph it. That is how a tree gets
added.": "wtf zo'n slechte zin... You can add a tree by taking a photograph and
adding details ofzo." Then the question that matters more than the fix: "hoe
zorgen dat je standaard zinnen beter worden?"

THE DIAGNOSIS, because it is one habit and not a list of accidents. This
codebase is written in short, declarative, aphoristic sentences, because that is
the right register for recording a decision: "A pin that admits it is vague is a
finished first version." That register leaks into what the READER sees, where it
is wrong. A comment states a conclusion; a sentence in the app has to tell a
person what they can do.

The failing sentence had all three symptoms at once: two bare imperatives, then
a passive summary in which nobody does anything ("a tree gets added"), then an
aphorism pretending to be help ("That is how"). His rewrite puts the reader back
in as the subject: "You CAN add a tree BY taking a photograph."

    python3 scripts/copycheck.py            # every user-facing string
    python3 scripts/copycheck.py --fix-help # what to write instead

WHAT THIS CANNOT DO is judge a sentence. It catches the tics I repeat, which is
worth more than nothing and much less than reading the copy out loud. Extend the
list the next time he corrects the same thing twice.
"""
import argparse
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import copy_rules  # noqa: E402
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = ROOT / "ios" / "AncientTrees" / "AncientTrees"

# Strings a person reads. Text("..."), Label("...", ...), Button("...").
STRING = re.compile(r'(?:Text|Label|Button)\(\s*"((?:[^"\\]|\\.){12,})"')

TICS = [
    # The promise nobody may make. Hidde, 2026-08-26, deciding the free
    # launch: "kun je wel nergens beloftes in de app of ergens op het product
    # doen dat het altijd gratis blijft? Die belofte kunnen we gewoon niet
    # maken." qa.py has guarded the website's copy against forever-claims
    # since the paywall rule; the app's strings had no such guard until now.
    (re.compile(r"\b(?:free forever|forever free|always (?:be )?free|"
                r"altijd gratis|blijft gratis|gratis blijven|"
                r"never (?:pay|charge)|we will never|we will always)\b", re.I),
     "forever-promise: pricing is Hidde's and undecided, stay vaguer"),
    # The aphorism pretending to be help. A conclusion is not an instruction.
    (re.compile(r"\bThat is (?:how|what|why|the)\b", re.I),
     "aphorism: states a conclusion where the reader wants an instruction"),
    # Nobody does anything. If a person acts, name the person.
    (re.compile(r"\b(?:gets|get|is|are|was|were|be)\s+"
                r"(?:added|done|collected|shown|kept|sent|saved|removed|counted)\b", re.I),
     "passive: nobody is doing this, so say who does"),
    # Two commands where an offer belongs. Body copy that opens with a bare
    # verb reads as an order; a BUTTON opening with one is correct, which is
    # why this only fires on strings long enough to be a sentence.
    (re.compile(r"^(?:Walk|Take|Photograph|Tap|Go|Find|Look|Open|Press)\b[^.?!]{20,}"),
     "command: opens with an order; offer it instead (\"You can ...\")"),
    # Our own machinery, in the reader's face.
    (re.compile(r"\b(?:the (?:feed|catalogue|register|database)|our data|the data)\b", re.I),
     "machinery: names our plumbing rather than what they get"),
]

HELP = """Write it the way he rewrote it:

  bad   Walk to it and photograph it. That is how a tree gets added.
  good  You can add a tree by taking a photograph of it and filling in what you know.

Three things changed, and they are the whole rule:
  1. The READER is the subject. "You can ..." not "Walk to it".
  2. ONE sentence that carries the method, joined with "by".
  3. No summary line afterwards. If the sentence worked, it needs no moral.

Buttons are the exception and stay imperative: "Add a tree", "Take a photo".
"""


def strings():
    for f in sorted(APP.rglob("*.swift")):
        src = f.read_text(encoding="utf-8")
        for m in STRING.finditer(src):
            line = src[:m.start()].count("\n") + 1
            yield f.relative_to(ROOT), line, m.group(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix-help", action="store_true")
    args = ap.parse_args()
    if args.fix_help:
        print(HELP)
        return 0

    hits = []
    for path, line, text in strings():
        # THE HARD BANS FIRST, and they are not a matter of style: an em dash
        # anywhere breaks hard rule 3 and the four filler words break Step 3.
        # Both were gated on the website only until 2026-08-25, because the list
        # lived inside qa.py, which reads site/dist and has never seen a line of
        # Swift (Hidde, same day: "gebruiken we de juiste zelfde patronen voor
        # app en web?"). It lives in scripts/copy_rules.py now and both read it.
        banned = copy_rules.offences(text)
        if banned:
            what, why = banned[0]
            hits.append((path, line, text, f"{why}: {what!r}"))
            continue
        # Interpolated strings are mostly numbers and names; the tics live in
        # the prose around them and this still sees that.
        for pattern, why in TICS:
            if pattern.search(text):
                hits.append((path, line, text, why))
                break

    for path, line, text, why in hits:
        print(f"{path}:{line}: {why}")
        print(f"    {text[:110]}")
    if hits:
        print(f"\n{len(hits)} sentence(s). python3 scripts/copycheck.py --fix-help")
    else:
        print("no known tics in the app's user-facing strings.")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
