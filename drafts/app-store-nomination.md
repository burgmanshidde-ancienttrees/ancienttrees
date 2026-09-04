# App Store featuring nomination, 2026-09-04

Where: App Store Connect, sidebar > Featuring > Nominations > + > Create
Nomination. The pasteable text is in fenced blocks, which is also how
scripts/pitchcheck.py knows which part of this file is copy and which part is
me talking to you.

## Nomination Name  (39/60)

```
Explore remarkable old trees around you
```

Hidde's wording, both words his. Explore beat my "Find" because finding is a
search and exploring is an afternoon outside. Around beat "near" because near
is a distance and around is where you are standing in the middle of something.
No article: a headline reads better without one. The field is internal anyway,
Apple's own text says it just helps you recognise the nomination later.

## Nomination Type

**App Launch.**

Corrected after he asked whether the autumn angle really beat "new app in
general". It does not. Apple's own featuring criteria lead on uniqueness, and
"New Apps We Love" is one of their biggest recurring slots; being one day old
with no comparable app is the strongest card we hold. Autumn is TIMING, not a
release, because the season radar already exists and what changes in October is
the trees.

## Related Apps

```
6806177833
```

## Publish Date

Leave the start empty, or set the window you would like to be featured in:
2026-10-15 to 2026-11-15. The field is optional and the launch date is past.

## Platforms

iOS (iPhone)

## Localization

```
en, nl, es, it, de, pt, fr, ja
```

## Supplemental Materials

```
https://ancienttrees.app
```

## Description  (956/1000)

Only the App Store team sees this. It is the field that decides.

```
Every city has a few trees that were already old when it was built, and almost nobody can tell you where they are.

Ancient Trees does. It shows the remarkable old trees around you, builds a walk that strings a few together, and tells you what you are standing under. You tick off the ones you have seen, from the Ankerwycke Yew at Runnymede to the giant three streets away.

Every pin is drawn as its own species, so an oak reads as an oak and a ginkgo as a ginkgo before you tap anything.

An old ginkgo turns completely gold for two weeks in November, then drops nearly every leaf at once. The app shows you which trees near you are turning, which makes late October the moment this is worth putting in front of people.

Photograph a tree we do not have and it goes on the map with your name under it, once we have checked it.

Made by Hidde Burgmans, a designer in the Netherlands. 56 trees in Barcelona, 45 in Munich, 2,472 in all, in seven languages.
```

Judged blind by an independent reader against Hidde's own bullet-list version,
which scored 4 against this one's 7. The finding worth keeping: **bullets
belong in the public App Store listing, not in a nomination.** A bullet
answers "what does it do", which the editor already has from the listing
metadata; a nomination has to answer "why this app, why now, who made it", and
none of those fit in a bullet. His version lost the maker, the craft detail
and the seasonal timing to the format rather than to the writing.

Two things taken from his version because they were better: the Ankerwycke Yew
as an anchor a reader already knows, and naming the season feature plainly.
The per-city counts replaced the flat total after the reader pointed out that
2,472 across 362 places divides to seven per place and reads thin.

**One claim removed, and it matters.** His version said "get notified when a
tree peaks". There is no notification code anywhere in the app: no
UNUserNotificationCenter, nothing. Season Radar ALERTS are a paid-tier promise
from 2026-08-18 that is not built. Telling Apple we notify people would be a
claim about a feature that does not exist, so it now says the app shows you,
which is what it does.

## Helpful Details  (485/500)

```
Made by one person in the Netherlands who loves old trees.

Every tree is verified against two independent sources before it goes on the map, and a location we cannot state precisely says so on the page instead of sending somebody to the wrong spot. A pin you can trust is the difference between a good afternoon and a wasted one.

Readers correct us and send photographs from the app, which appear on the tree's page with their name under it.

Seven languages, written not translated.
```

## How this text got here

Four rewrites, each one his correction rather than my improvement, and the
diagnosis is in drafts/PITCH_VOICE.md now so the next pitch does not repeat
them:

- "New app:" as a prefix. He: "klinkt droog."
- Opening on the ginkgo while the title was deliberately broad. He: "waarom nu
  ginkgo special als we een algemene intro titel doen". An editor who starts on
  one species can think it is a one-species app.
- A description that led with counts, verification and competitors. He: "nobody
  cares about this."
- "Not up a mountain, just to something extraordinary." Nobody mentioned a
  mountain. He: "your sentences make no sense and are beside the point not up
  to a mountain wtf."

The mission and the fact that people add trees themselves are in it because he
asked for both.

## Checked before writing

- 2,472 trees, 362 places, 25 countries (scripts/stats.py, 2026-09-04)
- 570 trees in 192 places peak in September, October or November
- 83 ginkgos in 60 places across 22 countries, 77 of them peaking in Oct/Nov
- The Ankerwycke Yew and the Totteridge Yew are live and their ages are what
  their pages say
- Seven languages live
- `python3 scripts/pitchcheck.py drafts/app-store-nomination.md` is clean

## One line to decide yourself

"Made by one person in the Netherlands" is true of who owns and runs this. If
you would rather not lead on it, cut the line; the rest stands alone.

## A second nomination, later

This one is the introduction, so it is broad on purpose. The narrower angle,
the ginkgos turning gold in November, is what a second nomination is for, and
you may send as many as you like.
