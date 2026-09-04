#!/usr/bin/env python3
"""Put the calibration in front of the copy, not after it.

Hidde, 2026-09-04, having watched me write four drafts of one nomination:
"your copy writing skills it suck... your sentences make no sense and are
beside the point not up to a mountain wtf". Then the ask that matters more
than any single rewrite: "i want you to figure out a way to forever improve
you copy output".

Why a hook and not a note. This project already proved the difference twice:
eight memory notes about his mail voice failed to stop the eighth mistake,
while scripts/mailcheck.py fixed it the day it existed, and CLAUDE.md records
the rule that came out of it ("a note I must remember to consult is nearly
worthless; a check that runs is not"). The failure I am fixing here happens in
the FIRST DRAFT, in conversation, before any file exists to check. So this
fires on his message and prints the calibration into the context before a
sentence is written.

Deliberately narrow, the same discipline as convention_nudge.py: it needs a
word naming PITCH copy specifically. This project talks about text, stories
and pages all day, and a hook that fires on every message is a hook nobody
reads. Tree stories and app strings are not this: they have TONE_OF_VOICE.md
and PRODUCT_COPY.md, and both are already good.
"""

import json
import re
import sys

# The register that has no other check: something a stranger reads to decide
# whether this is interesting.
PITCH = re.compile(
    r"\b(app ?store|nominat\w+|featuring|persbericht|press release|pitch|"
    r"tagline|slogan|marketing|advertentie|campagne|campaign|"
    r"beschrijving|description|subtitle|ondertitel|promo\w*|"
    r"sponsor\w*|landing ?page|homepage ?copy|about ?page|"
    r"listing|store ?copy|store ?tekst)\b", re.I)

# Asking for words rather than about them.
WRITING = re.compile(
    r"\b(schrijf|herschrijf|maak|bedenk|verzin|tekst|copy|woorden|zin|zinnen|"
    r"write|rewrite|draft|wording|word it|phrase|better|beter|"
    r"invullen|vullen|fill in|wat moet ik|what should i|"
    r"klinkt|sounds|leest|reads)\b", re.I)

NUDGE = """PITCH COPY (scripts/hooks/pitch_nudge.py, fires on messages about pitch copy)

This looks like copy a stranger reads to decide whether we are interesting,
which is the register I write worst. Before drafting a sentence:

1. READ drafts/PITCH_VOICE.md. Two things are in it and both are for
   imitating rather than reasoning from. PAIRS: the bad line beside the good
   one, from the times he corrected me. And the REFERENCE OPENINGS, verbatim
   from Merlin, AllTrails, Seek and komoot, which every one of them starts on
   the reader rather than on the company. Copy the shape of one of those.

2. The one habit to catch yourself doing: writing as though winning an
   argument instead of showing something. Defining by denying ("not up a
   mountain, just a tree"), proving we are unique by naming competitors
   ("there are databases and there are hiking apps, but nothing that"),
   leading with counts because a count feels like evidence. Nobody doubted
   anything. Show one true specific thing and let the reader conclude.

3. The first sentence belongs to the reader or the world. Never us, never the
   product name, never a number, never the market.

4. RUN `python3 scripts/pitchcheck.py <file>` or `--text "..."` on the draft
   BEFORE showing it to him. It catches the tics; it cannot tell you a
   sentence is dull, so also read it once as a stranger who owes you nothing.
"""


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    text = (payload.get("prompt") or "")[:4000]
    if PITCH.search(text) and WRITING.search(text):
        print(NUDGE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
