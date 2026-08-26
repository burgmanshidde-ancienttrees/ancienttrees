#!/usr/bin/env python3
"""What may never appear in anything a reader sees. One file, both platforms.

The same argument as scripts/layout_rules.py, which Hidde made about the layout
gates on 2026-08-20 ("kun je vervolgens zorgen dat de CI voor app en web
dezelfde kwaliteit nastreven") and asked again about the whole QA form on
2026-08-25 ("gebruiken we de juiste zelfde patronen voor app en web, zijn we
consistent en doen we geen dubbel werk?").

The answer for THIS pair was no. Hard rule 3 says never use an em dash anywhere
and CLAUDE.md Step 3 bans four filler words, and both were gated on the website
only: `BANNED_WORDS` lived inside scripts/qa.py, which reads site/dist and has
never seen a line of Swift. The app was clean when this was written, which is
luck rather than a check.

So the list lives here, qa.py reads it for the rendered site and copycheck.py
reads it for the app's strings. Adding a word bans it on both surfaces at once,
which is the point: a bar written down twice is two bars.
"""

# CLAUDE.md, Step 3. Not a matter of taste: these are the words that make a
# sentence sound like every other travel page on the internet.
BANNED_WORDS = ["hidden gem", "must-see", "breathtaking", "nestled"]

# Hard rule 3, which says ANYWHERE and means it.
EM_DASH = "—"

# PROMISES ABOUT WHAT WE WILL NEVER DO. Hidde, 2026-08-26, finding "No ads,
# and nothing follows you around" in copy I wrote for him: "i dont like this
# stop saying that, were going to use google analytics once, why do you keep
# making these false promises." He is right twice over. It is his call whether
# this project ever runs analytics, ads or a paywall (hard rules 2 and 5), so
# a promise in our copy takes that call away from him; and CLAUDE.md records
# that the site has never carried a no-tracking claim, which was still true
# until I put one on the sponsor page an hour before he caught it.
#
# The distinction that keeps this usable: a PRESENT-TENSE FACT is fine and is
# what the privacy page is for ("we use a cookieless counter"). A promise
# about the future is not, and neither is an absolute that reads as one.
PROMISE_PHRASES = [
    "nothing follows you around", "no tracking", "we do not track",
    "we don't track", "never track", "no ads ever", "no ads, ever",
    "free forever", "forever free", "always free", "will always be free",
    "we will never", "we will always", "nothing else, ever",
]


def offences(text):
    """Every banned thing in one string, as (what, why) pairs."""
    out = []
    low = text.lower()
    for word in BANNED_WORDS:
        if word in low:
            out.append((word, "banned filler word (CLAUDE.md Step 3)"))
    if EM_DASH in text:
        out.append(("em dash", "hard rule 3: never, anywhere"))
    for phrase in PROMISE_PHRASES:
        if phrase in low:
            out.append((phrase, "promise about what we will never do: that call "
                                "is Hidde's, so state a present fact instead"))
    return out
