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

## Description  (699/1000)

Only the App Store team sees this, which is the thing that took longest to
land: it is a pitch to Apple's editors, not the public listing. An editor
already has the feature list from the submission form, so a bullet list of
features spends the whole budget re-typing what they have.

```
Some of the trees in your city were standing before the city was. Ancient Trees takes you to them.

An old ginkgo turns completely gold for two weeks in November and then drops nearly every leaf at once. The app tells you which trees near you are turning this week, and builds a walk that strings a few of them together. There are about eight weeks in the year when a tree is worth crossing town for, and they start now.

Every pin on the map is drawn as its own species, so an oak reads as an oak and a ginkgo as a ginkgo before you tap anything. You tick off the ones you have stood under.

Made by Hidde Burgmans, a designer in the Netherlands, in seven languages, with 2,472 trees mapped so far.
```

**Scored 8.5 by an independent reader** who saw only the text and none of this
conversation, after eight drafts scoring 7, 6, 7.5, 7.5, 7.5 and 7.5. What
that reader found and I could not: an opening that set up a negative so the
app could answer it, a "researched by hand" claim that reads as generated once
multiplied by the tree count, city counts that invite an unflattering
division, a line explaining the app's value to a professional whose job is
spotting value, and a closing paragraph where the seasonal urgency arrived
stapled to a bio. The last fix was moving that urgency into the paragraph
where the season already lives.

**What it deliberately does not say.** No notification claim: there is no
notification code in the app, and Season Radar alerts are an unbuilt paid-tier
promise. No iOS platform hook: no widget, App Intent or Watch app exists to
name. The species pin art is the one craft detail, and it is real, 15 drawn
shapes in site/src/lib/species-icons.ts.

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
