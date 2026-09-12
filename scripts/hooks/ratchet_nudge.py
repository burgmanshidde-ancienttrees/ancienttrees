#!/usr/bin/env python3
"""When Hidde states a RULE, turn it into a check before replying to it.

Hidde, 2026-09-12, having just been shown that the worth-it vote was on none
of the 907 translated tree pages: "hoe zorg ik dat je dat onthoudt waar
opschrijven." It is the right question and it had an uncomfortable answer. He
had already given that rule, on 2026-09-02, in plain words: "alle paginas en
talen moeten consistent blijven." It went into CLAUDE.md, it was read at the
start of every run for ten days, and it did not hold, because a sentence in a
corpus cannot refuse a push.

CLAUDE.md has known this since 2026-08-11 (Trigger 2): record a correction in
the form that ACTS, a script first and a note last, because "a note I must
remember to consult is nearly worthless; a check that runs is not." The
trouble is that the trigger is itself a note, so remembering to apply it
depends on the thing it says does not work.

So this stands in the doorway. It fires on a message that reads like a
standing rule rather than a task, and asks the one question that converts a
sentence into a gate: what refuses the next push that breaks this? It never
blocks, never answers, and never decides what the check should be.

Deliberately narrow, same as the other two nudges in this folder. It wants a
word that makes a rule PERMANENT ("altijd", "voortaan", "nooit meer",
"onthoud"), because this project talks in imperatives all day and a hook that
fires on every message is a hook nobody reads.
"""

import json
import re
import sys

PERMANENT = re.compile(
    r"\b(altijd|voortaan|nooit meer|vanaf nu|elke keer|iedere keer|standaard|"
    r"consistent|onthoud|onthouden|blijvend|forever|always|never again|"
    r"from now on|every time|each time|remember (this|that)|make sure you)\b",
    re.I)

RULE = re.compile(
    r"\b(zorg dat|zorg ervoor|moet(en)? (je|we|het|alle)|regel|afspraak|"
    r"werkwijze|proces|hoe zorg ik|hoe voorkomen we|hoe onthoud|waar opschrijven|"
    r"rule|process|workflow|how do (i|we) (make sure|stop|prevent)|"
    r"how do you remember|where (do i|should i) write)\b", re.I)

NUDGE = """RATCHET (scripts/hooks/ratchet_nudge.py, fires when a message reads like a standing rule)

This sounds like a rule meant to hold from now on, not a task. Before writing
the reply, answer one question out loud:

    WHAT REFUSES THE NEXT PUSH THAT BREAKS THIS?

Then build that, in this order (CLAUDE.md, Trigger 2, 2026-08-11):

1. A CHECK that runs. scripts/qa.py for anything visible in the built site,
   scripts/preflight.py for the data, scripts/hooks/pre-push for anything that
   costs under a second, a test for the app. Verify it BOTH ways: green as it
   stands, and red when the fault is put back.
2. Failing that, a file the workflow already reads, and say which run reads it.
3. A sentence in CLAUDE.md LAST, and only beside one of the first two.

A rule he has now given twice is evidence that prose does not hold it. Do not
answer with where he should write it down; answer with what now stops it, and
say plainly if the honest answer is that nothing does yet.
"""


def main():
    try:
        prompt = json.load(sys.stdin).get("prompt", "")
    except Exception:
        return 0
    if PERMANENT.search(prompt) and RULE.search(prompt):
        print(NUDGE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
