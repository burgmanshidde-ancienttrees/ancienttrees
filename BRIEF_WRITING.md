# The writing pass rulebook

A writing pass turns verified facts into publishable tree entries, 15 to 20
trees per pass, across cities. Batching is the point: the tone calibration is
read once and amortized over every story, which is what makes writing cost a
few thousand tokens per tree instead of twenty.

Input: one or more `data/research/<slug>-verified.json` files (arrays of tree
objects with `verify_notes` and `verified_sources`, no `story`).

**Whoever briefs you must run `python3 scripts/passcheck.py --pending` first**,
and you should check it yourself before writing a word. A research file is not
proof that work is outstanding: on 2026-08-08 a brief asked for seven trees
when only three were real, because nyc_011-013 and ams_011 had already been
written and merged that morning and nobody had deleted the stale files. If an
id already exists in data/cities, it is finished: do not write it again, say so
and move on. Prose written over good live copy is worse than prose not written.
Output: the same files with `story` and, where honest, `best_time` filled in,
and `verify_notes` removed. You change no other field: the facts are already
verified, and prose that contradicts a verified field is a writing error.

Read TONE_OF_VOICE.md in full before the first story (it is short; Paris is the
calibration standard). Do not read CLAUDE.md.

## The story

150 to 250 words. Direct, specific, slightly vivid: Scott Galloway meets nature
writing. Lead with the most surprising fact in `verify_notes`. Include what the
tree has witnessed historically. Where sources disagree, the story says so in
plain words; stating a range or a dispute honestly reads better than false
confidence.

Never use: "hidden gem", "must-see", "breathtaking", "nestled". Never use em
dashes, anywhere, in any field. No fill-in-the-city-name templating: every
story is written from this tree's own facts.

Flagged trees keep their hedged phrasing: "by that tradition", "a 1913 monument
claims", "somewhere between". The flag is in the data; the honesty must also be
in the prose.

## Age: carry the basis, or carry the question

Where `verify_notes` gives an ESTIMATED age, the story says what it is estimated
from, in a clause rather than a paragraph: "about five metres round, which puts
it near four hundred years". An estimate that arrives in the prose as a bare
number reads as a measurement, and that is the thing we are not allowed to fake.
Keep the band as wide as the notes give it; do not tidy "300 to 500" into "400".

Where there is no age at all, do NOT hedge the whole story into mush and do not
apologise for the gap. Say it plainly once and turn it into an invitation, which
is what the site runs on everywhere else: nobody has dated this one, and if you
know, tell us. One sentence, near the end.

And never bridge to an age. If the notes say the garden was replanted in 1864
and say nothing about when this tree went in, the story may put the tree in that
garden and may not date it from that replanting. Two sourced facts joined into a
third that neither source states is this project's most expensive writing error;
it is what the "no bridge claims" rule exists for.

## best_time, only when real

A tree gets `best_time` only when it has a genuine seasonal peak a visitor
would notice on the day: blossom, autumn colour, fruit or mast underfoot, or a
veteran's bare winter architecture. One per tree, its strongest moment:

```json
"best_time": {"months": [11], "kind": "autumn colour", "label": "late November, when the ginkgo turns gold"}
```

`kind` is one of: `flowers`, `fruit`, `autumn colour`, `catkins`,
`fresh leaves`, `bare silhouette`. The label says what actually happens, not
just a month. An evergreen or a tree that looks the same all year gets no
`best_time` at all: scarcity is what makes the badge worth anything, and an
empty field is a correct answer.

## Species names

One canonical common name per species, nationality-neutral, matching what other
cities already use (Quercus robur is "Pedunculate Oak", never "English Oak";
Platanus x acerifolia is "London Plane"). If unsure, grep data/cities/ for the
Latin name and copy the existing common name; the build fails on one species
under two names.

## Write each story to the file as you finish it, never all at the end

The verification rulebook has said this since a Padova pass died and lost
everything; the writing rulebook never did, and on 2026-08-17 that cost a pass.
A Singapore writer read both rulebooks, both live city files and eight verified
trees, said "now I have everything I need, let me write the eight stories", and
was killed by the harness watchdog for producing no output for 600 seconds. It
had in fact finished all eight and they were on disk, so the work survived by
luck rather than by design: had it written them in one final edit, the whole pass
would have been lost.

**So: finish one story, write it into the delivery file, then start the next.**
Valid JSON after every write. Eight stories generated in one silent stretch is
ten minutes of no output, which the watchdog cannot tell apart from a dead agent,
and it is the one shape of failure this stage is exposed to.

It also makes a killed pass resumable rather than wasted. The next attempt reads
the file, sees which ids already carry a `story`, and writes only the rest.

## What happens after you

The main session merges your output into the city files, fixes any count
promises in existing copy, rebuilds and runs QA. You do not merge, build or
commit. Return the filled-in cost line your brief asks for.
