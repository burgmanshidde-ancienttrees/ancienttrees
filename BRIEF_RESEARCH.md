# The verification pass rulebook

Everything a verification pass needs, in one file. Do not read CLAUDE.md, LOG.md
or the rest of the corpus: your brief plus this file is the whole job. This file
exists because passes used to carry 86KB of project history each, and the
history is not what verifies a tree.

## What you are doing

Ancient Trees maps remarkable old trees people can walk to. Your job is the
factual half only: confirm which candidate trees are real, alive, remarkable and
visitable, and pin them. Someone else writes the prose later, from your notes.
You do NOT write stories. You do NOT hunt photos. You do NOT edit city files.

A tree qualifies if it is genuinely old OR visually spectacular OR historically
significant, AND publicly accessible. A register saying "protected" is not by
itself "worth the walk": judge each one.

## The bar, per tree

1. **Alive now.** Best evidence is a dated photo, news item or observation from
   the last few years. If confirmation is thin, deliver it anyway with
   `curation_status: "flagged"` and say in `verify_notes` what is missing. A
   tree you KNOW is dead is never delivered. No register has a vitality field;
   this check is always yours.
2. **Two independent sources** for existence, species and age. One official
   register counts as one source. If sources conflict, deliver both figures in
   `verify_notes` and flag; never pick a winner silently.
3. **The exact spot.** `location_precision: "confirmed"` only when you can place
   the individual tree (tree-level coordinates from a register, a mapped photo,
   satellite-visible crown). Park-level or shrine-level knowledge is
   `"approximate"`, and that is a finished, publishable answer. Faking precision
   is the one mistake this project cannot afford.

## Hard limits that never bend

- Never fabricate. An unverifiable claim is dropped or flagged, never smoothed.
- monumentaltrees.com: verification only, never copy text, photos or coordinates
  as the sole source.
- Never deliver a tree whose location its source deliberately withholds, or one
  on private land not genuinely open to visitors. When in doubt, leave it out
  and record why in `blocked`.
- A tree within ~30 minutes by public transport of the centre counts, labeled
  with its real place name and true travel time. Never present it as in-town.
- An entry must be one collectible point: one identifiable tree, or a compact
  famous ensemble with one obvious place to stand. An avenue or a whole wood is
  `blocked`, reason recorded.
- Register twins: entries metres apart that a visitor sees as one thing fold
  into one entry; note the folded register ids in `verify_notes`.

## Register pitfalls, each has already happened

- Units: a girth column may be metres or centimetres regardless of its name.
  Sanity-check every number against the physical world (a 2.84 cm trunk is not
  a tree).
- A year sitting in an age field (olive, "age 2009") is corruption, not an age.
- A register age is the age at last measurement: add the years since, say so.
- The register's total will not match the municipality's own count; never quote
  either as a count of what exists.

## Fetch discipline

Every fetch gets a hard timeout: `curl -m 20`, or `timeout=` on urllib. Your
brief lists hosts known to hang or block, with workarounds; believe it. A host
that hangs on you once: note it in your report so it joins the blocklist.

## Delivery: append as you go, never only at the end

Passes have died mid-run and lost everything they had not written down. Append
each tree to the delivery file named in your brief THE MOMENT it verifies,
valid JSON after every append.

**So work one candidate through to done before starting the next.** Researching
all of them in parallel and writing at the end is what makes a pass worth
nothing when it is cut off: a Padova pass died after 25 fetches across eight
candidates and left an empty repository, while the same effort spent depth-first
would have banked three finished trees. Finish one, append it, then move on.

One object per tree:

```json
{
  "id": "xxx_001",
  "name": "The common name people use",
  "species": "Common Name (Latin name)",
  "age_estimate": "roughly 400 years",
  "age_min": 300, "age_max": 500,
  "location": {"address": "...", "latitude": 0.0, "longitude": 0.0, "neighbourhood": "..."},
  "verified_sources": ["url1", "url2"],
  "access": "Free / paid entry / restricted, with the honest caveat if any",
  "transport": "Nearest station or stop + walk time",
  "location_precision": "confirmed | approximate",
  "curation_status": "ai_generated | flagged",
  "verify_notes": "Raw facts for the writer: what makes it remarkable, what it witnessed, disagreements between sources, the anecdote worth leading with. Bullet-style is fine."
}
```

`verify_notes` is the writer's only input besides the sources, so put the good
material there: the surprising fact, the history, the dispute. Facts only, no
polished prose.

`age_estimate` is a chip label, not a sentence: "roughly 400 years", "over a
century", "not documented". Put any caveat, dispute or reasoning in
`verify_notes` for the story to carry instead. Paris shipped five trees on
2026-08-08 whose `age_estimate` was a full clause ("not documented;
comparable Corylus colurna elsewhere in Paris date to the 1860s-1880s"),
which reads as prose where the page needs a scannable fact.

Candidates that fail only on evidence or count go to the `leads` list of
`data/leads/<slug>.json` (create or extend it, keep existing entries); trees
that must never ship (dead, private, withheld location, not a collectible
point) go to its `blocked` list with the reason in one line.

## Stop condition

Report what you have after roughly 40 minutes; do not run to completeness.
Never hold a whole city back on your own judgement: deliver what verifies,
record the rest. With your report, return the filled-in cost line your brief
asks for (your total token usage), so the daily retro can price the pass.

## Aerial imagery as evidence (standing tool, Hidde's idea, 2026-08-09)

Openly licensed aerial imagery is a legitimate source for three things, and
only three:
1. **Position**, when the tree is individually identifiable: a distinctive
   crown (the only evergreen giant in a bare winter park), a documented
   structure at the trunk (Baarn's Pekingtuin oak was CONFIRMED because its
   ~6m protective ring is visible in the national aerial survey), a lone tree
   in a plaza. "A big crown roughly where the park is" identifies nothing.
2. **Continued presence**, when the imagery is DATED and recent: a standing
   crown in this year's national survey is real evidence; undated commercial
   basemaps prove nothing about today.
3. **Absence**: a stump or bare gap where a documented large crown should be
   is a strong death signal worth chasing in news sources.

What imagery can NEVER do: species, age, or "alive today" from undated or
stale layers. It is one source among the two, never both.

Where to look, in order: national open orthophoto programmes, which are dated
and licensed (Netherlands: PDOK Actueel_orthoHR WMS, 7.5cm, yearly; France:
IGN; Spain: PNOA; Denmark and others have equivalents); then Esri World
Imagery (check the capture-date metadata per tile area). Google Maps/Earth
tiles are ToS-restricted for automated fetching: do not scrape them.
Always cite the imagery source and its capture vintage in the evidence.
