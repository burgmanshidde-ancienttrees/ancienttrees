# How to write the sentences a reader sees

Written 2026-08-24, after Hidde read "Walk to it and photograph it. That is how
a tree gets added." and asked the question that matters more than the fix: "kun
je zorgen dat je een andere manier van schrijven gebruikt voor tekst voor in het
product, kun je jezelf daar een laag overheen gooien?"

This file is that layer. It is short on purpose, and it is about UI strings
only: buttons, cards, empty states, sheets, settings rows. TONE_OF_VOICE.md
governs stories and page copy and is his to change; this governs the twenty
words a person reads while holding the thing.

## Why my default is wrong here

This codebase is written in short, declarative, aphoristic sentences, because
that is the right register for recording a decision. "A pin that admits it is
vague is a finished first version." Good sentence. Wrong genre.

A comment states a CONCLUSION. A string in the app tells a person what they CAN
DO. When the first register leaks into the second you get orders and morals
where somebody wanted help, which is exactly what happened:

> bad **Walk to it and photograph it. That is how a tree gets added.**
> good **You can add a tree by taking a photograph of it and filling in what you know.**

Three faults in eleven words: two bare imperatives, a passive summary in which
nobody does anything, and an aphorism pretending to be instruction.

## The five rules

1. **The reader is the subject.** "You can ..." rather than "Walk to it".
2. **One sentence, joined with "by".** The method belongs inside the offer, not
   in a second sentence after it.
3. **No summary line.** If the sentence worked it needs no moral. "That is how",
   "This is what", "That is the point": all cut.
4. **Name who acts.** We delete, we keep, we look at every one. Never "is
   removed", "gets added", "are kept".
5. **Never name our machinery.** Not the feed, the catalogue, the register, the
   database. Say what they get.

6. **Do not explain our side of the deal.** Not at the moment somebody is
   deciding to act. "You can add any tree by photographing it, whether we map it
   or not" spends its last six words on our catalogue, which is our problem and
   not the reader's reason to lift a phone. Hidde: "mijn god waarom zou je dat
   laatste zeggen... begin niet over het mappen, dat is voor later." Say what
   they get: **Every tree you photograph joins your collection.**

Buttons are the exception and stay imperative: **Add a tree**, **Take a photo**,
**Show the way**. Two or three words, a verb first, no sentence.

## Never write a number where nothing can update it

Hidde, 2026-08-26, on a sponsor bio I wrote with "1,841 trees in 171 cities"
in it: "dont use the number it will get outdated quickly and remember not to
use it at static places."

The website may quote a count because it regenerates one on every build and
`check_tree_count_claims()` in qa.py refuses one that overstates. Nothing else
we write regenerates. A string inside a shipped app binary is fixed until the
next release. An App Store description, a Ko-fi bio, a social profile or a
store screenshot is fixed until somebody remembers to log in and edit it,
which is to say fixed forever.

So: **counts live only where a build puts them.** Everywhere else, write what
the thing IS. "I map the most remarkable old trees of the world's cities"
never goes stale; "1,841 trees" is wrong within the week. An outreach mail is
the one exception, and only because it is a moment in time rather than a
standing page: `outreach_compose.py` fills its counts from the data at the
moment of sending.

`copycheck.py` refuses a literal count in an app string. Nothing can grep an
external profile, which is why this is written here.

## A live count is a number, not a sentence

Hidde, 2026-08-27, on "1 person keeps this tree" under a tree's name: "een hele
rare zin, zet gewoon bij thumb hoeveel mensen thumb up of down hebben gedaan
verder niet."

The sentence reads oddly for a reason worth naming, because the instinct that
wrote it will write it again. A count wants to be prose here: singular and
plural need different words, "1 person" and "2 people", and once you are
choosing between two wordings you have written a sentence about a number
instead of showing the number. And a sentence claims more than a figure does.
"1 person keeps this tree" says something about the tree; "1" beside a heart
says how many, which is all we know.

So: **a live count belongs ON the control it is about, as a figure.** Beside the
thumb, beside the heart, on the tab. Never a line of prose somewhere else on the
page saying the same thing in words. That is also the convention everywhere a
count is shown at all, from YouTube to Google Maps to a review page.

Two things this does not touch. Static counts are the section above and stay
banned outright. And a figure of ZERO is not shown: a lone 0 under a tree we
chose to publish reads as a verdict when it is only an empty table (his own
rule for the save count, 2026-08-26, "pas van 1 tellen").

## Before it ships

`python3 scripts/copycheck.py` greps every user-facing string for these tics.
It cannot judge a sentence and it catches the five habits above, which is worth
more than nothing and much less than reading the line out loud. When he corrects
the same thing twice, add it to the list there rather than to memory.
