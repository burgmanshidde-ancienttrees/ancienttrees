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

## Description  (886/1000)

Only the App Store team sees this. It is the field that decides.

```
Every city has a few trees that were already old when it was built, and almost nobody can tell you where they are.

Ancient Trees does. It shows you the remarkable old trees around you, gives you a walk that strings a few of them together, and tells you what you are standing under. You tick off the ones you have seen.

Every pin on the map is drawn as its own species, so an oak reads as an oak and a ginkgo as a ginkgo before you tap anything.

An old ginkgo turns completely gold for two weeks in November, then drops almost every leaf at once, and the app tells you when yours is turning. That makes late October the moment this is worth putting in front of people.

Photograph an epic tree we do not have and it goes on the map with your name under it, once we have checked it.

Made by Hidde Burgmans, a designer in the Netherlands. 2,472 trees in 362 places, in seven languages.
```

Six drafts, the last three judged by an independent reader who saw only the
text and nothing of the conversation, scoring 5 then 7 out of 10 for whether
an Apple editor would shortlist it. What that reader caught and I could not:
an opening promise of "twenty minutes away" that our own 2,472 trees
contradict; a claim that every tree is researched by hand, which an editor
multiplies out and reads as generated; a sentence of pure mood; and no visual
idea for an editor to build a card around. The species-drawn pins fixed the
last one and are true: 15 drawn shapes in site/src/lib/species-icons.ts.

Two things I could not fix for you. **Your name** is in it because an editor
cannot write a card about an anonymous maker; cut it if you would rather not.
And **no iOS platform hook**, because we have no widget, App Intent or Watch
app to name and I will not invent one. The season radar is the widget that
should exist, and that is a real product note rather than a copy note.

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
