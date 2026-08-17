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
- Most registers have no age field at all. That is what the section below is for.
- The register's total will not match the municipality's own count; never quote
  either as a count of what exists.

## Try the Wikipedia registry join FIRST, before any generic searching

The cheapest technique this project has found. It has now paid off on three
cities in three days and each time it had to be re-explained in the brief, so
it lives here instead.

**A national register is often missing exactly what a page needs.** Poland's
GDOS list carries no age, no girth and no names. Lithuania's municipal register
403s to every fetcher. But the local-language Wikipedia frequently reproduces
the CITY's own register document, with address, girth and designation year per
tree, and its ids join straight to the register rows we already hold.

    Krakow    "Pomniki przyrody w Krakowie", joined by INSPIRE code
              -> real measurements for 115 of 155 candidates, whole pass 55k
    Warsaw    same article for Warsaw, 561 rows
              -> addresses and girths for 6 candidates the register left bare
    Vilnius   Lithuanian articles on the protected objects
              -> confirmed or killed 8 of 10 candidates in one search each

**Fetch the WIKITEXT, not the rendered page.** The Warsaw pass found the
rendered table scrambles row alignment under its image cells, which silently
pairs a girth with the wrong tree.

**And the reason it beats the register even when the register has the fields:
the footnotes.** A register records what is designated, and nothing in it says
a tree has fallen down. The Wikipedia reproductions carry the removals inline,
which is where every dead tree caught this week was caught: Krakow's two
storm-felled monuments, Warsaw's Sowinski Linden (blown down 1986, not found in
a 2004 survey, delisted 2012, and live on our site until it was), and Vilnius's
two delisted entries. If you skip this step you will publish a dead tree.

Search terms that worked: "Pomniki przyrody w <city>", "<city> gamtos paveldo
objektai", and the local-language phrase the law itself uses, which is usually
better than any translation of "tree register".

## Where no register exists: OSM tree nodes, and the island rules

Found on the first island pass, Tenerife, 2026-08-17, and it generalises to
anywhere rural.

**OpenStreetMap tags individual famous trees as `natural=tree` nodes**, and for
the Drago Milenario and both Vilaflor pines those nodes gave tree-level
coordinates that matched the descriptive sources exactly. Free, fast, and it
substitutes for the one thing a register normally provides and a tourist-board
page never does: a pin. Query it through Nominatim or Wikidata rather than
scraping. It is a COORDINATE source and nothing more; it says nothing about
whether the tree is alive, reachable or worth the walk.

**And where a region has no register, its island or provincial government often
publishes a monumental-tree list anyway.** The Canaries have no approved
regional catalogue (the 2006 draft was never adopted, and only Gran Canaria has
an insular one, from 2021, which does not cover Tenerife). But the Cabildo de
Tenerife runs its own monumental-tree portal, which named twelve trees island
wide. Two notes: it is JavaScript-rendered, so plain curl returns nothing
useful and a rendering fetch is needed; and a list like this is a lead list
rather than a designation, so the two-source bar still applies in full.

**Islands cluster by CAR, not on foot, and the page must say so.** Tenerife is
80 km end to end. Its four trees are three separate stops: two pines 150 m
apart at one viewpoint, then 15 to 20 km to the next. That is an honest day
with a hire car and it is not a walk. Do not describe it as one, do not use
"afternoon" for a set that spans the island, and put the real driving distance
in the record. The clustering doctrine still holds, it just measures in
kilometres by road instead of metres on foot.

**Expect island passes to cost register-free rates.** Tenerife ran at ordinary
web-research cost, not the 0.4k per tree a real register gives. The compensation
is on the other side: nobody writes about these trees in English, so the
competition for the page is close to nothing.

## Age: estimate it when you can, ask the reader when you cannot

A missing age never holds a tree back, and it never has. What changed on
2026-08-16 is the other half: **estimating is allowed and wanted, and an
estimate is not an invention.**

An estimate is DERIVED and says what from. These count, in this order:

1. **Girth plus a published growth rate for the species.** This is how every
   register in the world dates a tree. Record the girth in `girth_cm` whether
   or not you use it, ALWAYS, even when the tree already has an age: it is the
   input the whole database is missing (13 trees of 1223 carry one), and it is
   the field that turns dating into a script instead of a judgement.
2. **A documented planting date for this specimen.** For this one, not for the
   garden around it. See the trap below.
3. **A vague age from a real source, repeated as vaguely as the source gave
   it.** "Several hundred years" stays "several hundred years" and never
   becomes "roughly 350".

What is none of these is a number that feels right, and that is fabrication
under hard rule 2 whatever it gets called.

A derived age is BROAD. The honest output of a growth-rate calculation is a
century-wide band: `age_min` 300, `age_max` 500, `age_estimate` "roughly 400
years". Narrowing it to look confident is the same error as a faked pin.
Put the working in `verify_notes` ("5m girth, oak on good soil"), never in
`age_estimate`, which is a chip label.

**The trap, and it will be right in front of you: the bridge claim.** "The
park was laid out in 1864, so this linden is 160 years old" joins two true
facts into a claim neither source makes. A park's planting date is the most
tempting bridge there is, because it is always available and always plausible,
and this exact move once shifted a pin sixty metres onto the wrong tree. It
only works when a source says THIS TREE belongs to that planting. Otherwise
leave the two facts as two facts and let the writer say the tree stands in a
garden replanted in 1864 without saying it dates from it.

**No basis at all: leave `age_estimate` empty, say so in `verify_notes`, and
let the page ask the reader.** Somebody with a tape measure answers it in one
message, and a correspondent is worth more than a number. Empty beats invented;
empty no longer beats derived.

## Why passes stall, and the four rules that came out of it

Three verification passes died on 2026-08-17 with the same message, "no progress
for 600s". Two of them were on Crete and one on Yakushima. What they had in
common is worth more than the individual failures.

**The proximate cause is a hanging network call.** The watchdog fires after ten
minutes of silence, and a fetch that never returns produces exactly ten minutes
of silence. All three stalled with their last words mid-reach: "Now the Plane
Tree of Gortyn", "Wikidata has an entry. Let me pull its coordinates." A hard
timeout on curl does not help when the hang is inside a fetch tool, which is why
these rules are about EXPOSURE rather than about timeouts.

1. **At most four named candidates per pass.** The passes that completed this
   week (Copenhagen with three, Tenerife with four, every register-led city)
   were short and specific. The two that died carried five or more names plus
   an open invitation to find others. A fifth candidate is a second pass, not a
   longer one.

2. **Two attempts on a source, then move on and say so.** Record the host and
   what it did in `verify_notes`, and go to the next tree. A tree with one
   source and an honest note is worth more than a pass that never returns.

3. **Prefer searching to fetching.** A search returns a summary quickly; a fetch
   opens a connection to someone else's server and waits. Fetch when you need
   an exact figure off a specific page, not to browse.

4. **Append after every single tree, without exception.** This is the rule that
   saved the week. Crete's first pass died having written two trees, and both
   survived; its second died having written none. Yakushima's died at three, and
   all three survived. Everything recovered from those three failures was
   recovered because the file was already on disk.

**And one framing rule for whoever writes the brief.** Crete's second pass spent
its opening turns arguing with itself about whether it was the researcher or a
dispatcher, and died before doing anything. A brief must say plainly: you are
the verification pass, you do this research yourself, you dispatch nothing.

## Fetch discipline

Every fetch gets a hard timeout: `curl -m 20`, or `timeout=` on urllib. Your
brief lists hosts known to hang or block, with workarounds; believe it. A host
that hangs on you once: note it in your report so it joins the blocklist.

## Delivery: append as you go, never only at the end

Passes have died mid-run and lost everything they had not written down. Append
each tree to the delivery file named in your brief THE MOMENT it verifies,
valid JSON after every append.

**Do the work yourself. Do not dispatch sub-agents.** A Geneva pass on
2026-08-17 delegated a side question about one park to a child agent, waited on
it, and was killed by the harness watchdog having banked nothing. The child's
research came back fine and was useless, because the pass that needed it was
gone. A second attempt, told to bank immediately, died the same way. Delegation
inside a pass buys nothing here: you are already the specialist, and every minute
spent waiting on a child is a minute of no output, which is exactly what gets a
pass killed.

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
  "girth_cm": 520,
  "location": {"address": "...", "latitude": 0.0, "longitude": 0.0, "neighbourhood": "..."},
  "verified_sources": ["url1", "url2"],
  "access": "Free / paid entry / restricted, with the honest caveat if any",
  "transport": "Nearest station or stop + walk time",
  "location_precision": "confirmed | approximate",
  "curation_status": "ai_generated | flagged",
  "verify_notes": "Raw facts for the writer: what makes it remarkable, what it witnessed, disagreements between sources, the anecdote worth leading with. Bullet-style is fine."
}
```

**`girth_cm` is in that list because leaving it out of it did not work.** The age
section below has asked for it since 2026-08-16 and three consecutive passes still
delivered nothing: Toronto recorded one of four, Singapore none of eight from
NParks pages that publish them, Bratislava none. Advice in prose gets read and
forgotten; a field in the object you are filling in gets filled in. Record it
whenever any source gives a girth, a circumference or a diameter, converting
diameter with pi, and do it even when the tree already has an age. It is the input
the whole database is short of, 33 trees of 1299 carry one, and the day there are
a few hundred the age estimating becomes a script instead of a judgement made one
tree at a time. Where the figure is a buttressed mass or a stem count rather than
a trunk, still record it and say so in `verify_notes`, so the writer cannot repeat
it as a trunk measurement.

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

## monumentaltrees.com as a verification source (codified 2026-08-09, Hidde's push)

Hard rule 1 forbids their content (photos, text, bulk data) and explicitly
permits fact verification. In practice that means three allowed uses:
1. **Second source**: a tree found elsewhere (register, news, institution) may
   be corroborated by its monumentaltrees record for existence, species,
   location and measurements. Never the sole source, and never the discovery
   engine: we find trees elsewhere, they may confirm them.
2. **Photo identity**: LOOK at their photos to confirm which tree a candidate
   image shows. Never republish or download their imagery.
3. **Names and measurements as cross-checks.**

Two hard edges: their server 403s automated fetches, deliberately, so this is
measured single-page browser-session work, never bulk scraping; and wholesale
extraction of their database is forbidden by their disclaimer and by EU
database right, whatever the technical route. The long play is Hidde's
outreach mail to the site's owner (OUTREACH.md tier 3c), which can turn the
grey edge into a partnership.
