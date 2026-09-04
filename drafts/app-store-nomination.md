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
en
```

**Corrected 2026-09-04.** This field said `en, nl, es, it, de, pt, fr, ja`,
which is the WEBSITE. The app has one known region, `en` (project.pbxproj), and
the live App Store record agrees: `languageCodesISO2A` is `["EN"]`. Seven
languages is a true fact about ancienttrees.app and a false one about the thing
Apple would be featuring.

## Supplemental Materials

```
https://ancienttrees.app
```

## Description  (911/1000)

Only the App Store team sees this. It is a pitch to Apple's editors, not the
public listing, so it never repeats the feature list they already have.

```
Some of the trees in your city were standing before the city was. Ancient Trees takes you to them.

Open it anywhere and the map fills with the ones around you, every pin drawn as its own species, so an oak reads as an oak and a ginkgo as a ginkgo before you tap anything. Tap one and you get what it is, how old it is, why it was left standing while everything around it came down, and directions to the trunk.

What that buys somebody is an afternoon outside. You walk into a churchyard you had never walked into, ten minutes from your door, and stand under something that has been alive for four hundred years.

The ones you have stood in front of become your collection. You follow other people and see the trees they have found, and one nobody has mapped you photograph where you stand.

Out this month, with 2,474 trees so far: fifty-six of them in Barcelona, one of them on the green of a Dorset village.
```

**Rewritten 2026-09-04 to argue FOR the app, on Hidde's correction:** "moet
die niet meer overhalend naar de redactie zijn van super cool we brengen mensen
naar buiten om de natuur te zien en laten bomen met elkaar delen". The version
before it described what the app contains and stopped there, which reads as a
feature list to somebody deciding whether to put it on a shelf. What was
missing was the third paragraph: what the thing DOES to a person's Saturday.

Two additions, both checked against the shipped build first. The afternoon
outside is the project's own goal 1 stated plainly, and it shows rather than
claims, which is the whole of PITCH_VOICE.md. Following other people and seeing
their trees is real in build 9: `Screens/FindPeople.swift` carries Follow and
Following, and the profile panel on the store shows followers and following
counts. What is NOT claimed is sending a tree to somebody by link, which is
1.0.1.

**Written against the seven screenshots that are on the store**, fetched back
from Apple rather than from `out/appstore/` (Hidde, 2026-09-04: "baseer t maar
op de plaatjes die we hebben meegestuurd"). An editor reads this text with those
panels beside it, so every sentence here has to be visible in one of them:

| Panel | Caption on it | The sentence it carries |
|---|---|---|
| 0 hero | Trees worth the walk, wherever you are | "takes you to them" |
| 1 map | Find remarkable old trees wherever you are | the map filling with what is around you, and the per-species pins, which are visibly different silhouettes in that frame |
| 2 city | See every old tree in a city | Lisbon, 33 trees, ages on every card |
| 3 tree | Read what makes it worth the walk | what it is, how old, why it was left standing, Take me there |
| 4 discover | Browse by city, country or species | (left out: the description is not a feature list) |
| 5 my trees | Collect the trees you have stood in front of | "you tick off the ones you have stood in front of" |
| 6 add | Add a tree nobody has mapped yet | photographing one where you stand |

Panel 6's own words are "Every tree you photograph joins your collection", which
is why the last clause says it joins your collection AND reaches us, rather than
saying it lands on the map.

**Checked against the build that is actually on the store, 2026-09-04**, which
is 1.0, build 9, released 2 September. Two sentences did not survive it, and
both were the same error the drafts below already record: written from the
website rather than from the binary.

- **The photograph.** It said an added tree "goes on the map for everybody"
  with your own photograph. In the shipped build the collect sheet reads "Your
  photograph is yours and nobody else sees it", and an added tree gets "we will
  look at it for the map". Publishing a contributor's photograph with their
  name is real, but it lands in 1.0.1; a nomination naming it would describe an
  app Apple cannot open. Replaced with the build's own promise: you photograph
  it, you tell us what it is, we read every one.
- **Seven languages.** True of the website, false of the app. See Localization
  above.

**Scored 8.5 on a blind read**, by a reader who saw the text and none of this
conversation.

**Two things were cut late and both were the point.** An earlier draft scored
8.5 on a paragraph about a ginkgo turning gold and a walk between trees. The
shipped app has NEITHER: `Kit/Launch.swift` hides walks, the season story and
Plus behind arguments that are off for every real user, because they are what
the paid tier introduces. I had written from the website and the plan instead
of the build, in a document addressed to Apple. And the maker's name is out:
"dont mention me ever". Both are checks in pitchcheck.py now rather than
things to remember.

**What is left is only what a user can actually do today:** the map with a
drawn pin per species, a tree's story and age and directions, ticking off what
you have stood under, and adding a tree with your own photograph.

## Helpful Details  (488/500)

```
Made by one person in the Netherlands who loves old trees.

Every tree is verified against two independent sources before it goes on the map, and a location we cannot state precisely says so on the page instead of sending somebody to the wrong spot. A pin you can trust is the difference between a good afternoon and a wasted one.

Readers send us trees we have missed and corrections to the ones we have. We answer every one.

ancienttrees.app carries the same trees, in seven languages.
```

**Corrected 2026-09-04, same reason as the Description.** This block claimed
that photographs sent from the app appear on the tree's page with the sender's
name under them, which is 1.0.1 and not the build on the store; and it ended
"Seven languages, written not translated" as though the app were, when the
website is. The language line now says whose seven languages they are.

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

- 2,474 trees, 362 places, 25 countries (scripts/stats.py, 2026-09-04)
- 570 trees in 192 places peak in September, October or November
- 83 ginkgos in 60 places across 22 countries, 77 of them peaking in Oct/Nov
- The Ankerwycke Yew and the Totteridge Yew are live and their ages are what
  their pages say
- Seven languages live ON THE WEBSITE; the app has one, `en`
- The store record for 6806177833: version 1.0, released 2026-09-02, `EN`
- `python3 scripts/pitchcheck.py drafts/app-store-nomination.md` is clean

## One line to decide yourself

"Made by one person in the Netherlands" is true of who owns and runs this. If
you would rather not lead on it, cut the line; the rest stands alone.

## A second nomination, later

This one is the introduction, so it is broad on purpose. The narrower angle,
the ginkgos turning gold in November, is what a second nomination is for, and
you may send as many as you like.
