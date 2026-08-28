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
    # A count typed into a string. Hidde, 2026-08-26, reading a Ko-fi bio I
    # had written for him with "1,841 trees in 171 cities" in it: "dont use
    # the number it will get outdated quickly and remember not to use it at
    # static places." The website generates its counts on every build and
    # qa.py's check_tree_count_claims guards them; a string inside a shipped
    # binary regenerates never, so it starts going stale the day it ships and
    # cannot be corrected without a release. Same for anything we hand to a
    # place we do not build: an App Store description, a store screenshot, a
    # sponsor bio, a social profile. Interpolated counts are fine and are the
    # point, so this only sees literal digits.
    (re.compile(r"\b\d{2,3}(?:[,.]\d{3})*\s+"
                r"(?:trees|cities|countries|species|photographs|walks)\b", re.I),
     "hardcoded count: it goes stale where nothing regenerates it; "
     "interpolate it or leave the number out"),
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


# A CLAIM ABOUT WHAT WE DO WITH SOMEBODY'S DATA, which is the one kind of
# sentence that rots without anybody touching it.
#
# Added 2026-08-28 after Hidde caught "Your location stays on your phone. We
# never send it anywhere" on the permission screen and then asked the right
# question: "can you check the copy of the app if there are any other promises
# like this that are old." There were. The same afternoon turned up SIX copies
# of the same falsehood, written when they were true and left standing when the
# app changed under them: the privacy manifest, the release checklist Hidde
# types his App Store answers from, Sightings.swift, the location primer, and
# "We store your email address and the trees you collect. Nothing else." on
# both the sign-in and the account screen, against eight declared data types.
#
# Nothing here can tell whether a promise is TRUE. What it can do is refuse the
# ABSOLUTE FORM, because that is what makes the rot expensive: a qualified
# sentence ages into being imprecise, and "never", "nothing else" and "stays on
# your phone" age into being a lie, on the screen where somebody decides
# whether to trust us. Say what we hold and let the list be the limit.
#
# Deliberately narrow: it fires on absolutes ABOUT DATA, never on "nothing
# matches that yet" or "nobody has photographed this one".
DATA_WORDS = re.compile(
    r"\b(location|position|photograph|photo|picture|email|address|name|data|"
    r"collection|trees you|we store|we hold|we keep)\b", re.I)

# WHAT WE HOLD, not what we send. "One email. Nothing else." is a promise
# about our own behaviour on a waitlist, which we control and can keep; "We
# store your email address. Nothing else." is a claim about a data model that
# changes underneath the sentence. Only the second kind rots on its own, so the
# closed absolutes need a holding verb beside them before they count.
HOLDING = re.compile(r"\b(store|stores|hold|holds|keep|keeps|save[sd]?|"
                     r"we have|is kept|are kept)\b", re.I)

DATA_ABSOLUTES = [
    (re.compile(r"nothing else", re.I), True,
     "an absolute about what we hold: say what we hold instead, so the list is the limit"),
    (re.compile(r"\b(only|just) (your|the) (email|address)\b", re.I), True,
     "an absolute about what we hold: name the things instead"),
    # These two need no holding verb: they are the claim, whole.
    (re.compile(r"never (send|sends|leaves?|leave|share|shares|publish|publishes)", re.I), False,
     "a never about somebody's data: it was true when written and the app moves"),
    (re.compile(r"stays? (on|in) (your|this) (phone|device)", re.I), False,
     "this stopped being true on 2026-08-27; say who can see it instead"),
]


def data_promise(text):
    """The offence, or None. Both halves have to be present."""
    if not DATA_WORDS.search(text):
        return None
    holds = bool(HOLDING.search(text))
    for pattern, needs_holding, why in DATA_ABSOLUTES:
        if pattern.search(text) and (holds or not needs_holding):
            return why
    return None


SITE = ROOT / "site" / "src"
# Anything long enough to be a sentence, in quotes of either kind. Deliberately
# looser than the Swift pattern: the website writes its copy in .astro props,
# in i18n tables and in template literals, and a rule that only reads one of
# those would miss the translation of the sentence it just caught.
COMMENT = re.compile(r"^\s*(//|\*|/\*).*$", re.M)
SITE_STRING = re.compile(r"""["'`]((?:[^"'`\\\n]|\\.){25,300})["'`]""")


def strings():
    for f in sorted(APP.rglob("*.swift")):
        src = f.read_text(encoding="utf-8")
        for m in STRING.finditer(src):
            line = src[:m.start()].count("\n") + 1
            yield f.relative_to(ROOT), line, m.group(1)


def site_sentences():
    """The website's copy, for the data-promise rule only.

    BOTH SURFACES, because the sentence this rule exists for was on both and
    was corrected on one first (2026-08-28). The app's sign-in sheet said "We
    store your email address and the trees you collect. Nothing else"; the
    website's sign-in modal said "We store only your email address, for sign-in
    links and nothing else", and its Spanish translation said it again. A check
    that only reads Swift would have called that afternoon finished.

    Only the data-promise rule runs here. The tics are about the app's own
    register, and TONE_OF_VOICE governs the website's prose.
    """
    if not SITE.exists():
        return
    for f in sorted(list(SITE.rglob("*.astro")) + list(SITE.rglob("*.ts"))):
        src = f.read_text(encoding="utf-8")
        # A COMMENT IS NOT COPY. Without this, every note explaining why a
        # sentence was wrong quotes the sentence and trips the rule that
        # caught it, which is a checker that punishes writing down the reason.
        # Blanked rather than deleted so the line numbers stay true.
        src = COMMENT.sub(lambda m: " " * len(m.group(0)), src)
        for m in SITE_STRING.finditer(src):
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
        promise = data_promise(text)
        if promise:
            hits.append((path, line, text, promise))
            continue
        for pattern, why in TICS:
            if pattern.search(text):
                hits.append((path, line, text, why))
                break

    for path, line, text in site_sentences():
        promise = data_promise(text)
        if promise:
            hits.append((path, line, text, promise))

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
