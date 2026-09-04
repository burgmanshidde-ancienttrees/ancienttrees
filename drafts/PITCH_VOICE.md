# Pitch copy: the calibration set

What this is. TONE_OF_VOICE.md governs tree stories and page copy;
PRODUCT_COPY.md governs the twenty words somebody reads while holding the app.
Neither covers PITCH copy: an App Store description, a featuring nomination, a
press note, the sponsor page, the paragraph in an outreach mail that says what
this is. That is the register I write worst, and on 2026-09-04 Hidde said so
in the plainest terms available: "your copy writing skills it suck... your
sentences make no sense and are beside the point not up to a mountain wtf".

Paris calibrates tone. Cadiz calibrates photographs. This file calibrates a
pitch, and it works the same way: not by rules, by pairs.

## The one habit under all of it

**I write as though winning an argument rather than showing something.**

Every failure below is that habit wearing a different coat. I define by
denying ("not a mountain, just a tree"), I prove we are unique by naming
competitors ("there are databases and there are hiking apps, but nothing
that"), I lead with counts because counts feel like evidence. All three are
moves you make when you expect to be doubted. Nobody doubted anything. The
reader is a stranger who owes us nothing and is deciding, in one sentence,
whether this is interesting.

A pitch is not a defence. It shows one true, specific thing and lets the
reader draw the conclusion.

## The pairs, from the featuring nomination, 2026-09-04

**Opening**

- NO: "Ancient Trees exists to get people outside. Not up a mountain, just to
  something extraordinary and alive."
  Nobody mentioned a mountain. The sentence argues with an alternative the
  reader never had in mind, and it spends the most valuable line in the text
  doing it.
- YES: "Most people have walked past a thousand-year-old tree without knowing
  it."
  One thing, true of the reader, and it makes them want the next sentence.

**Claiming to be unlike anything**

- NO: "Nothing else does this. There are tree databases written for botanists
  and there are hiking apps, but nothing that walks you to one extraordinary
  tree."
  Three clauses of other people's products. A reader learns what we are NOT.
- YES: Show the thing that nothing else does and say nothing about the field.
  "The app tells you which tree, what you are looking at, and why it is worth
  the walk."

**Naming the thing**

- NO: "New app: find the remarkable old trees near you."
  A category label glued to the front. Hidde: "klinkt droog."
- YES: "Explore remarkable old trees around you."
  His own. Explore rather than find, because finding is a search and exploring
  is an afternoon outside. Around rather than near, because near is a distance
  and around is where you are standing in the middle of something.

**Leading with what we built**

- NO: opening on 2,472 trees, 362 places, 25 countries, two independent
  sources.
  That is our pride and our method. It belongs at the end as one line, or
  nowhere.
- YES: the counts as the last line, after the reader already wants it.

**Ornament instead of a sentence**

- NO: "for whoever stands there next", "which week yours is having".
  Both sound like writing. Neither says anything a plain phrase would not.
- YES: say the plain thing. Ornament earns its place only when it carries a
  fact nothing else carries.

## What to do instead, in order

1. **First sentence: the reader or the world, never us and never the market.**
   If it contains "we", the product name, a count, or a competitor, rewrite it.
2. **One concrete thing before any general claim.** A named tree, a specific
   November, a churchyard. The general claim then reads as earned instead of
   asserted.
3. **Say what it is, not what it is not.** If a sentence needs "not", "unlike",
   "rather than" or "but nothing", the point can be made positively.
4. **The counts and the method go last, or go.**
5. **Read it as a stranger who owes you nothing.** Every line that survives
   that reading is a line that shows something.

## What the reference apps actually do, read 2026-09-04

Fetched from the App Store rather than remembered, the same way CONVENTIONS.md
handles interactions. These are the four this project already treats as
standing references, and the point of writing them down is that a lookup I have
to repeat is a lookup I will skip.

**Their opening sentences, verbatim:**

- **Merlin Bird ID** (Cornell Lab): "What's that bird? Ask Merlin, the world's
  leading app for birds."
- **AllTrails**: "Whether you hike, bike, run, or walk, AllTrails is your
  companion and guide to the outdoors."
- **Seek by iNaturalist**: "Use the power of image recognition technology to
  identify the plants and animals all around you."
- **komoot**: "Turn your next ride, hike, or run into an adventure with
  komoot."

**What all four have in common, and it is the thing to copy:**

1. **The reader is in the first clause, before the product name.** Merlin opens
   on the question the user already has. AllTrails opens on what you do.
   komoot opens on your next ride. Seek opens on an imperative aimed at you.
   Not one of them opens with the company or with a count.
2. **A verb near the front.** Ask, Turn, Use. Three of the four are
   imperatives.
3. **Numbers arrive late and carry scale, never the argument.** AllTrails
   mentions 500,000 trails inside a feature section, not in the opening.
4. **"All around you" is the standard phrase, not an invention.** Seek uses it
   word for word. Hidde reached for "around you" over my "near you" on
   2026-09-04 and it turns out to be the convention.
5. **Then capitalised section headings with feature bullets.** Every one of
   them. A long App Store description is a scannable list after the first
   paragraph, not continuous prose.

**The one place they contradict my check, and the check is the thing that is
wrong.** Merlin's second paragraph reads "Merlin is unlike any other bird
app, it's powered by eBird, the world's largest database of bird sightings".
That is uniqueness by denial, which pitchcheck.py flags. The difference is
real and worth keeping: Merlin earns it by attaching a hard fact in the same
breath, and it is the SECOND paragraph, after the reader already knows what
the thing is. So the rule is not "never contrast", it is **never open on a
contrast, and never leave one unpaid by a fact.** "There are databases for
botanists and there are hiking apps, but nothing that..." pays nothing.

## How this file grows

The same rule the rest of the corpus runs on: when he corrects the same kind
of sentence twice, the pair goes in here and, if it can be grepped, into
`scripts/pitchcheck.py`. A pair is worth more than a rule, because I can
imitate a pair and I can argue my way around a rule.
