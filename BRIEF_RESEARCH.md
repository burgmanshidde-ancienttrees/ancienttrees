# The verification pass rulebook

Your brief plus this file is the whole job. Do not read CLAUDE.md, LOG.md or the rest of the corpus. The worked examples behind each rule are in archive/BRIEF_RESEARCH-full-2026-10-12.md; open it only if a rule's edge is unclear.

## What you are doing

Confirm which candidate trees are real, alive, remarkable and visitable, and pin them. You do NOT write stories, hunt photos, edit city files, or dispatch sub-agents (a pass that waits on a child gets killed by the watchdog). You are the verification pass; do the research yourself.

A tree qualifies if genuinely old OR visually spectacular OR historically significant, AND publicly accessible. "Protected" alone is not "worth the walk".

## Before spending time on a candidate

- **Since 2026-10-09 a new tree ships only when its page is RICH, or a reader added it** (`check_a_new_tree_is_rich_or_a_readers`). Rich = all of: findable (photo, confirmed pin, or a small named site plus a recognition line); the official register record for THIS tree (`official_register` {name, url}); a measurement (girth_cm or height_m) with its source; concrete access (free or price, plus days or hours where published). A candidate that will end short goes to data/leads/ with what is missing. A reader's sighting is exempt from richness.
- **It must be able to end with a photograph or a confirmed pin.** Photo: an openly licensed picture of THIS tree (Commons file named after it or geotagged within ~150 m, iNaturalist, a register's CC photo). Pin: register coordinate, OSM tree node, aerial imagery on the trunk, or a GPS fix taken at the tree (a photograph's geotag, a reader's or our own app fix, a published GPS position). GPS is as good as it gets: it makes the pin confirmed, never approximate (Hidde, 2026-10-14). Neither in reach: lead, reason "no photo or exact pin in reach". Put candidates with a photo in hand first.
- **Find the naming body first.** The method needs somebody who already named individual trees: a council survey, heritage decree, champion register, association label, Wikipedia list. Found: the city works. None: expect two or three, say so up front.

## The bar, per tree

1. **Alive now.** Best: a dated photo, news item or observation from the last few years. Thin: deliver `flagged`, say what is missing. Known dead: never deliver. No register has a vitality field. `python3 scripts/lifecheck.py LAT LON` (or `--file`): RECENT is fine; OLD or NONE means flag and say so.
2. **Sources.** Two independent sources for existence, species and age; conflicts go into `verify_notes` with both figures, flagged. **One official register is enough anywhere**, and so is the owner or manager of the ground (botanic garden, park department, church, estate): do not hunt a second source; spend the time on alive, pin and access. Register-only is `flagged` with "register only" unless the register records vitality or was updated in the last five years. **In the US one credible source is enough** (government page, the ground's owner, American Forests, Live Oak Society, a university arboretum, a dated news report on this tree), flagged "one source". Finding aids (California Big Trees, Famous Trees of Texas, monumentaltrees.com, unclear-licence lists), blogs and listicles are never a source.
3. **Covered countries** (100+ trees: NL, Italy, Japan, Spain, Germany, France, Poland, Portugal, UK): a new tree needs a photo or confirmed pin, or it is a lead. US exempt.
4. **The exact spot.** `"confirmed"` only when you can place the individual tree (register tree coordinate, mapped photo, visible crown). Park or shrine level is `"approximate"`, a finished answer. Never fake precision. A register coordinate unless it lands on one clear crown is approximate.
5. **Or a small site.** On a small named site taken in at one glance (churchyard, cemetery gate, square, cloister, courtyard, library lawn; never a park, wood, campus or walk-through garden): `"location_site": {"name": "...", "radius_m": 30}` (50 at most), keep `approximate`, and note in `verify_notes` what tells this tree apart there, from sources only.
6. **Access** (hard rule 10). Registers include gardens and schoolyards and rarely say if you can walk up. Settle it from OpenStreetMap when no source says: `access=`, `foot=`, `highway=footway`, `designation=` tags near the tree (a permissive footpath 20 m from a golf-course tree ships; `access=private` on the only road does not). Evidence, not proof; never overrides a source or the absolutes.

## Hard limits

- Never fabricate. Unverifiable: drop or flag, never smooth.
- monumentaltrees.com: second source, photo identity (look, never download), names and measurements as cross-checks. Never the sole source or the discovery engine, never their text, photos or bulk data; single pages only, they 403 automation.
- Never a location its source withholds, never private land not open to visitors, never somebody's home. Schools only with evidence the grounds are open.
- Within ~30 minutes by public transport counts, with its real place name and travel time.
- One collectible point: one tree, or a compact famous ensemble with one place to stand. Avenue or wood: `blocked`.
- Twins metres apart fold into one entry; folded register ids in `verify_notes`.
- **A search summary is a pointer, never a source.** WebSearch's summary has invented measurements. Any figure you record must be seen on the fetched page; if only the summary has it, it does not exist.
- Sanity-check every number against the physical world (a "60 m" olive, a 2.84 cm trunk).

## Register pitfalls

Units are not what the column says (metres vs cm). A year in an age field is corruption. A register age is at last measurement: add the years since, say so. The register's total never matches the municipality's; never quote either as what exists. Prefer the regional register over the national one where both exist.

## Cheap techniques, try first

- **The Wikipedia registry join.** Local-language Wikipedia often reproduces the city's own register with address, girth and designation year per tree, joinable by register id ("Pomniki przyrody w <city>", "<city> gamtos paveldo objektai", the phrase the law uses). Fetch the WIKITEXT, not the rendered page (rendered tables misalign rows). Read the footnotes: they record trees that fell or were delisted, which registers never do. Skipping this publishes dead trees.
- **OSM `natural=tree` nodes** give tree-level coordinates for famous trees. Coordinates only, nothing about alive or access.
- **Island or provincial government lists** where no register exists (e.g. Cabildo de Tenerife; JavaScript-rendered, needs a rendering fetch). A lead list, two-source bar applies. Islands cluster by car: give real driving distances, never call it a walk.
- **Aerial imagery** (dated, open: PDOK in NL, IGN, PNOA, national orthophotos; Esri with capture date) for position when the tree is individually identifiable, continued presence when the layer is dated and recent, and absence (a gap where a crown was). Never species, age, or alive from stale layers. Never scrape Google tiles. Cite source and vintage.

## Age

Missing never holds a tree back. An estimate is DERIVED and says what from: (1) girth plus a published growth rate for the species; (2) a documented planting date for THIS specimen; (3) a vague source repeated as vaguely ("several hundred years" never becomes "roughly 350"). A derived age is broad (`age_min` 300, `age_max` 500, `age_estimate` "roughly 400 years"); the working goes in `verify_notes`. **No bridge claims**: a park laid out in 1864 does not date its linden unless a source says this tree belongs to that planting. No basis: leave it empty, say so, the page asks the reader.

## How to work so a pass finishes

- **At most four named candidates per pass.** Long lists plus "find others" is what killed every stalled pass.
- **Two attempts on a source, then move on** and note the host in `verify_notes`.
- **Prefer searching to fetching**; fetch only for an exact figure. Every fetch has a hard timeout (`curl -m 20`, `timeout=` on urllib). Believe the hang list in your brief; report any new host that hangs.
- **Depth first: finish one candidate, append it, then the next.** Append to the delivery file named in your brief the moment a tree verifies, valid JSON after every append.
- **Stop after roughly 40 minutes** and report what you have. Never hold a city back on your own judgement. Return the filled-in cost line your brief asks for (your total token usage); a pass without it cannot be priced.

## Delivery

One object per tree:

```json
{
  "id": "xxx_001",
  "name": "The common name people use",
  "species": "Common Name (Latin name)",
  "age_estimate": "roughly 400 years",
  "age_min": 300, "age_max": 500,
  "girth_cm": 520,
  "height_m": 24,
  "location": {"address": "...", "latitude": 0.0, "longitude": 0.0, "neighbourhood": "..."},
  "verified_sources": ["url1", "url2"],
  "official_register": {"name": "the authority's register", "url": "its page for THIS tree"},
  "access": "Free / paid entry / restricted, with days or hours where published",
  "transport": "Nearest station or stop + walk time",
  "location_precision": "confirmed | approximate",
  "location_site": {"name": "only for a small named site", "radius_m": 30},
  "curation_status": "ai_generated | flagged",
  "verify_notes": "Raw facts for the writer: what makes it remarkable, what it witnessed, disputes, the anecdote worth leading with."
}
```

- **`girth_cm` whenever any source gives a girth, circumference or diameter** (diameter times pi), even when the tree has an age. A buttressed mass or stem count is still recorded and labelled as such in `verify_notes`.
- `age_estimate` is a chip label ("roughly 400 years", "over a century", "not documented"), never a sentence.
- `verify_notes` is the writer's only input besides the sources: facts, not prose.
- Candidates that fail only on evidence or count go to `leads` in `data/leads/<slug>.json` (extend, keep existing entries); trees that must never ship (dead, private, withheld, not a collectible point) go to `blocked` with a one-line reason.
