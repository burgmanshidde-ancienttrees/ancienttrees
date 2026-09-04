#!/usr/bin/env python3
"""Grep a PITCH for the way I keep writing one badly.

Hidde, 2026-09-04, on a featuring nomination: "your copy writing skills it
suck... your sentences make no sense and are beside the point not up to a
mountain wtf". Then the question worth more than the fix: "i want you to
figure out a way to forever improve you copy output".

THE DIAGNOSIS, because it is one habit rather than a list of accidents. I
write as though winning an argument instead of showing something. I define by
denying ("not up a mountain, just a tree"), I prove we are unique by naming
competitors ("there are databases and there are hiking apps, but nothing
that"), and I lead with counts because a count feels like evidence. Those are
the moves of somebody expecting to be doubted. Nobody doubted anything. It is
the same defensive habit my own notes already record, appearing in the one
register that had no check: not a tree story (TONE_OF_VOICE.md), not an app
string (PRODUCT_COPY.md and copycheck.py), but a PITCH. An App Store
description, a featuring nomination, a press note, the sponsor page, the
paragraph in a mail that says what this is.

The pairs live in drafts/PITCH_VOICE.md, which is the calibration set the way
Paris calibrates tone and Cadiz calibrates photographs. This file is the half
a machine can check.

    python3 scripts/pitchcheck.py drafts/app-store-nomination.md
    python3 scripts/pitchcheck.py --text "Not up a mountain, just a tree."
    cat something.txt | python3 scripts/pitchcheck.py -

Exit 1 when it finds something. WHAT IT CANNOT DO is tell you a sentence is
boring, and that is most of the problem, so this never replaces reading the
thing as a stranger who owes you nothing.
"""
import argparse
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import copy_rules  # noqa: E402

# Everything above a --- separator is a header for us, not copy for a reader,
# the same convention mailcheck.py uses.
BODY_SPLIT = re.compile(r"^---\s*$", re.M)

TICS = [
    # THE UNASKED CONTRAST. "Ancient Trees exists to get people outside. Not up
    # a mountain, just to something extraordinary." Nobody mentioned a
    # mountain. The sentence argues with an alternative the reader never had,
    # and it spends the most valuable line in the text doing it.
    (re.compile(r"(?:^|[.!?]\s+|,\s+)not\s+(?:up\s+)?(?:a|an|the|to)\s+[a-z][a-z ]{2,28},\s*(?:just|but|only|merely)\b", re.I),
     "the unasked contrast",
     "you are arguing with an alternative the reader never had in mind. Say "
     "what it IS."),

    # UNIQUENESS BY DENIAL. Three clauses about other people's products teach
    # the reader what we are not. Show the thing instead and say nothing about
    # the field.
    (re.compile(r"\b(nothing else (?:does|comes|is)|no other app|no app that|"
                r"unlike (?:other|any|every)|but nothing that|"
                r"there are .{5,60} and there are )\b", re.I),
     "uniqueness by denial",
     "you are proving we are unique by describing competitors. Show the thing "
     "nothing else does and leave the field out of it."),

    # THE CATEGORY PREFIX. "New app: find the remarkable old trees near you."
    # A label glued to the front of a sentence that was fine on its own.
    (re.compile(r"^\s*(new app|introducing|announcing|presenting|meet the app)\b[:,]", re.I | re.M),
     "category prefix",
     "a label glued to the front. Hidde on this exact line: 'klinkt droog'. "
     "The sentence after the colon is usually the whole thing."),

    # LEADING WITH OURSELVES. Checked on the first sentence only, because a
    # count in the last line is right and a count in the first is us talking
    # about us before the reader has any reason to care.
    (None, "the first sentence is about us",
     "a pitch's first sentence belongs to the reader or the world. Move the "
     "counts, the method and the product name down."),

    # ORNAMENT INSTEAD OF A SENTENCE. Phrases that sound like writing and say
    # nothing a plain phrase would not.
    (re.compile(r"\b(for whoever .{3,30} next|which week yours is having|"
                r"that is the whole idea|that is how .{3,40} (?:gets|get) )", re.I),
     "ornament instead of a sentence",
     "this sounds like writing rather than saying something. Plain phrase."),

    # THE APHORISM AS A CLOSER. The corpus register leaking into copy: a
    # summary line that states a conclusion the reader was about to draw.
    (re.compile(r"[.!?]\s+That is (?:the|what|why|how|all)\b", re.I),
     "aphorism as a closer",
     "you are summarising a point the reader already had. Cut the line."),
]

FIRST_SENTENCE = re.compile(r"^\s*(.{10,400}?[.!?])(?:\s|$)", re.S)
ABOUT_US = re.compile(r"\b(we|our|us|ancient trees)\b|\d", re.I)

# Below this, a block is a value (an app id, locale codes, a url, a headline),
# not a pitch with an opening to get wrong.
PROSE_WORDS = 25


FENCE = re.compile(r"^```[a-z]*\n(.*?)^```", re.M | re.S)


def body_of(text):
    """The copy a stranger will read, not the notes around it.

    A working document (drafts/app-store-nomination.md) is instructions to
    Hidde WRAPPING the copy, and checking the whole file flagged my own heading
    as a bad first sentence. So: if the file fences its copy, only the fenced
    blocks are copy. That is ordinary markdown and it makes the document more
    useful anyway, because a fenced block is the thing you paste.

    With no fences, everything after a --- header is the copy, the same
    convention mailcheck.py uses; with neither, the whole file.
    """
    fenced = [b.strip() for b in FENCE.findall(text)]
    if fenced:
        return fenced
    parts = BODY_SPLIT.split(text, maxsplit=1)
    return [parts[1] if len(parts) > 1 else text]


def check(text, label="text"):
    """(tic, why, excerpt) for everything found.

    Each block of copy is judged on its own, because each has its own first
    sentence. A fenced block that is a value rather than prose (an app id, a
    list of locale codes, a url) has no first sentence to get wrong, so the
    opening test only runs on blocks long enough to be a pitch.
    """
    hits = []
    for body in body_of(text):
        for pattern, tic, why in TICS:
            if pattern is None:
                continue
            for m in pattern.finditer(body):
                excerpt = " ".join(m.group(0).split())[:90]
                hits.append((tic, why, excerpt))
        if len(body.split()) >= PROSE_WORDS:
            m = FIRST_SENTENCE.search(body.strip())
            if m and ABOUT_US.search(m.group(1)):
                hits.append(("the first sentence is about us",
                             TICS[3][2],
                             " ".join(m.group(1).split())[:90]))
        for word, why in copy_rules.offences(body):
            hits.append(("banned in all copy", why, word))
    return hits


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", nargs="?", help="file to check, or - for stdin")
    ap.add_argument("--text", help="check this string instead of a file")
    a = ap.parse_args()

    if a.text is not None:
        text, label = a.text, "--text"
    elif a.path == "-":
        text, label = sys.stdin.read(), "stdin"
    elif a.path:
        text, label = pathlib.Path(a.path).read_text(encoding="utf-8"), a.path
    else:
        print(__doc__)
        return 1

    hits = check(text, label)
    if not hits:
        print(f"pitchcheck: {label} is clean of the tics I repeat. "
              f"Now read it as a stranger who owes you nothing, which is the "
              f"half no script can do (drafts/PITCH_VOICE.md).")
        return 0
    print(f"pitchcheck: {len(hits)} problem(s) in {label}")
    for tic, why, excerpt in hits:
        print(f"  {tic.upper()}")
        print(f"    {excerpt!r}")
        print(f"    {why}")
    print("\nThe pairs that show what to write instead: drafts/PITCH_VOICE.md")
    return 1


if __name__ == "__main__":
    sys.exit(main())
