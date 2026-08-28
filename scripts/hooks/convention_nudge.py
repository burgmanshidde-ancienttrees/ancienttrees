#!/usr/bin/env python3
"""Put the convention check in front of the answer, not after it.

The failure this catches happens in CONVERSATION, before a single file is
touched, which is why no build check could ever have seen it. Hidde asks what
happens when somebody wants to add a tree from a photograph already on their
camera roll; the honest first move is two minutes reading how iNaturalist does
it, and instead a session invents three options and presents them as a design.
He then has to say "kijk naar conventies aub en ga dit niet zelf zitten
ontwerpen", which is the third time that rule has been given.

So this fires on his message, when the message looks like it is about an
interaction, and prints one paragraph into the context before the answer is
written. It never blocks and it never answers for me; it is a reminder standing
in the one doorway the mistake walks through.

Kept deliberately narrow. It needs BOTH a build or question intent AND a word
naming an interaction, because this project talks about photographs, maps and
cities all day and a hook that fires on every message is a hook nobody reads.
"""

import json
import re
import sys

INTENT = re.compile(
    r"\b(kunnen we|kun je|kunnen jullie|wat als|zou het|zouden we|laten we|"
    r"moeten we|hoe zou|ik wil|ik zou willen|"
    r"can we|could we|what if|should we|let'?s|how would|i want|i'?d like|"
    r"bouw|maak|ontwerp|build|design|add)\b", re.I)

INTERACTION = re.compile(
    r"\b(knop|button|scherm|screen|flow|sheet|picker|kiezer|formulier|form|"
    r"menu|tab|swipe|tap|veeg|upload|uploaden|dialog|modal|onboarding|"
    r"paywall|inloggen|sign ?in|sign ?up|login|interactie|interaction|"
    r"ux|gebaar|gesture|zoekveld|search field|fotorol|camera roll|"
    r"galerij|gallery|op de kaart (aangeven|zetten|aanwijzen)|"
    r"toevoegen aan de kaart|pin (zetten|slepen|neerzetten)|drop a pin|"
    r"notificatie|notification|deelknop|share)\b", re.I)

NUDGE = """CONVENTION CHECK (scripts/hooks/convention_nudge.py, fires on messages about an interaction)

This message looks like it is about an interaction a person performs. Before
proposing ANY design, options or trade-offs of your own:

1. Read CONVENTIONS.md. If the interaction is already in there, cite it and use it.
2. If it is not, look up how the reference products actually do it (AllTrails,
   Google Maps, Airbnb, PictureThis are the standing ones; iNaturalist, Seek,
   Strava and Apple's own guidance where they fit better) and say what they do,
   with the source.
3. Only then design, and only for the part where our situation genuinely differs.

Inventing options and presenting them as a choice is the failure this exists to
stop (Hidde, 2026-08-20: "altijd conventies volgen geen eigen ideeen"). Add what
you looked up to CONVENTIONS.md so the next session does not repeat the search.
"""


def main():
    try:
        prompt = json.load(sys.stdin).get("prompt", "")
    except Exception:
        return 0
    if INTENT.search(prompt) and INTERACTION.search(prompt):
        print(NUDGE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
