# Ancient Trees — Project Instructions

## What this project is

Ancient Trees is a discovery platform that maps the most remarkable ancient trees of the world's great cities, up to ten per city and never padded. The owner is Hidde, a designer and tree enthusiast based in the Netherlands. The system researches, verifies and publishes; readers correct. Hidde sets direction, he is not the quality gate.

The end product: a website (ancienttrees.app) with an interactive map and one SEO page per city ("10 Most Beautiful Ancient Trees in [City]"), later followed by an iOS app with a freemium model. Where the paid line falls is undecided and Hidde's alone: see "The interim paywall line is still undecided" below, and hard rule 2.

## The value proposition

This is the core, and everything else serves it. Written 2026-07-24 by Hidde because the proposition had been drifting toward SEO and coverage, which are how people arrive, not why they stay. When anything here conflicts with an SEO or coverage instinct elsewhere, this wins.

**Ancient Trees is for people who love being outdoors and love trees.** The promise is simple: wherever you are, it shows you the remarkable old trees near you, gives you a short walk that strings a few together and tells you why each is worth seeing, and lets you collect the ones you have stood in front of. The feeling it sells is a good afternoon outside, looking up at something epic and old.

The one-sentence north star: *I am somewhere, I open it, it knows where I am, it shows me a cool tree nearby and a walk past a few, tells me why they are special, and I tick off the ones I visit.*

**The product is four verbs, settled with Hidde on 2026-07-26: find, walk, collect, season.** Find cool trees near you; walk a route past them; collect them with badges and points as the game; see them at their best with the season radar. Features outside these four (trip planners, audio guides, personal records, standalone themed routes) are parked ideas, not the product, and are not built without his explicit yes.

What this means for how we build:
- **The map and "trees near me" are the product.** They lead everywhere, the homepage first.
- **Cities, species and collections are acquisition, not the point.** They are SEO landing pages that bring people in from search. Keep them, they work, but they are the front door, not the house. On the homepage they sit below the value proposition, never in place of it.
- **Collections stay** (for example "the ten most remarkable trees of Europe"). A real SEO strategy, kept and on the backlog as such, secondary to the core. Not to be deleted.
- **The destination is: see the trees around you, walk them, collect them.** Accounts and an app are the vehicle. On 2026-07-26 Hidde opened the account track early, deliberately: build the app's collect-and-account backend now and wear it on the web, so the thinking and infrastructure exist before iOS. The conditions and current state live in "Where this is going" below.
- **Nothing is premium for now, but premium is the destination, and copy must never promise otherwise.** "Free today" is a growth tactic while we win users; the recorded end state is an account base with a premium tier and eventually an app (see "Where this is going"). So the site never says "free forever", "no accounts" or "always" anything: it simply does not gate today. Claims that survive the paywall (every tree free to explore, no ads, no tracking) are fine; claims the paywall would break are not. This distinction exists because a run once turned the sequencing into identity copy, and Hidde caught it.

When a page, a feature or a line of copy does not serve "have a good afternoon outside seeing epic trees near you," it is decoration or acquisition, and it must not crowd out the core.

## Repository structure

```
/data/cities/          — one JSON file per city (see schema below)
/data/collections/     — one JSON file per collection page (hand-curated, Contract D)
/data/species/         — one JSON file per species page intro (hand-written, gates Contract F)
/data/countries/       — one JSON file per country page intro (hand-written, gates Contract G)
/data/city-list.json   — the prioritized list of 100 cities with status
/site/                 — static site generator (Astro or similar)
/scripts/              — automation scripts
/CURATION.md           — log of what could not be verified, and notes worth keeping. Not a to-do list for Hidde.
/SEO_GEO_BLUEPRINT.md  — page contracts (titles, schema, internal links, content minima). No page ships without conforming to it.
/TONE_OF_VOICE.md      — the voice for all stories and page copy. Paris is the calibration standard.
/LOG.md                — what each autonomous run did. Hidde's catch-up file.
```

## The tree data schema

Every city file follows this exact structure (see data/cities/london.json for the reference example):

```json
{
  "city": "London",
  "country": "United Kingdom",
  "status": "needs_curation | curated | published",
  "trees": [
    {
      "id": "lon_001",
      "name": "The Totteridge Yew",
      "species": "European Yew (Taxus baccata)",
      "age_estimate": "2000 years",
      "age_min": 1000,
      "age_max": 2000,
      "location": {
        "address": "...",
        "latitude": 51.6323,
        "longitude": -0.2002,
        "neighbourhood": "..."
      },
      "story": "150-250 words. Specific, historical, vivid. No filler.",
      "verified_sources": ["url1", "url2"],
      "access": "Free / paid entry / restricted",
      "transport": "Nearest station + walk time",
      "photo": {
        "url": null,
        "license": null,
        "attribution": null,
        "status": "missing | found_needs_check | approved"
      },
      "curation_status": "ai_generated | hidde_approved | flagged",
      "location_precision": "confirmed | approximate"
    }
  ]
}
```

## The research workflow (autonomous run)

Runs chain themselves around the clock via GitHub Actions. **The capacity doctrine, ruled by Hidde 2026-07-28, replacing night-runs-only:** the goal is optimal use of his subscription, not politeness by clock. Concretely: the chain runs day and night; opening a working session fires a presence beacon (SessionStart hook dispatches the Presence workflow) that pauses the daytime chain for 4 hours so Hidde's own conversations get the window; every check fails OPEN into working, because his rule is that silence means the machine runs. Attempts that hit the usage limit die in seconds and cost nothing. Commit the smallest complete step first, always: a cutoff must cost minutes, not items. DATA.md's daily entry carries the utilization meter (attempts versus got-through) so nobody has to guess whether the limits are being used.

Each run, do exactly this, in order:

### Step 0 — Read state and pick the work

Read `/data/city-list.json` and the published city files, then take the first item on this ladder that applies. Do one thing per run and do it properly; a half-researched city is worse than none.

1. **Unprocessed submissions** (see Step 0b). Someone cared enough to send something, that outranks everything.
2. **The site is broken.** Build fails, a link is dead, a page violates a contract, the latest Smoke test workflow run is red, or REVIEW.md's newest entry holds a BLOCKER. Fix it before adding anything new. Same rung: if the Weekly analysis workflow has not run in 8+ days, dispatch it; and if the Data digest or Fresh-eyes review workflow has not run in 26+ hours (`gh run list --workflow=<file> -L 1`), dispatch it with `gh workflow run` — GitHub drops schedules silently, and the digest's own watchdog cannot report a digest that never ran.
3. **Something published is wrong**, as opposed to merely imprecise: a tree that has fallen, a pin in the wrong place, a fact that does not hold up. Wrong costs trust; vague does not, as long as it says so.
4. **New coverage: the Japan wave, then the recorded wave order.** Reopened by Hidde 2026-07-30 ("die hele kwaliteitsstop kan eraf, we gaan voor kwantiteit"); the depth exit test is retired, its history in DECISIONS.md.
   - **The order is data-led (Hidde, 2026-07-30): countries with good open register data are the interesting countries.** The licence-led register scan in OPEN_DATA_SURVEY.md is the queue-maker: where an open register with workable licence exists, that country moves up, for the register layer first and as the candidate pool for curated cities next. Japan stays in the queue without deadline or special priority (his ruling: "japan zou leuk zijn maar ook weer niet zo belangrijk"; the 2026-08-22 trip deadline is withdrawn, history in DECISIONS.md); its groundwork (Tokyo register live, national register scouted) keeps its head start. Among countries with comparably good data, English-speaking wins (Hidde, 2026-07-30: "engelssprekend zou logisch zijn", consistent with the recorded language-match argument: our pages are English and travelers search in English); after that the old geographic wave order (UK dense, Ireland, European capitals, NL-when-Dutch-exists) is the remaining tiebreaker.
   - The four-tree bar stands per city; counts per the doctrine in Step 1. NL pins from municipal open data where available, licence read first; the national NL register is CC-BY-NC and stays a lead list.
   - **Current focus, ruled by Hidde 2026-08-06 (evening, superseding the same morning's Rome/Lisbon/Porto ruling): the tourist-city rollout, London first.** His strategy, his words: "een paar hele grote steden een hele goede ervaring geven". Phase 1 is ten cities that combine maximum tourism, English-language search and tree stories: **London, Paris, New York, Rome, Amsterdam, Chicago, Washington DC, Boston, Barcelona, Berlin.** The UK is the first country to dominate, Europe the first continent. Lisbon and Rome he counts as the only current pages at decent scale; everything else in phase 1 is thin or absent. **Small-city work stops: no more Padua-or-Genoa-class cities** ("no longer waste time on padova of genoa"). Existing small pages stay live and get nothing new; reader submissions still outrank everything.
     - **London first, gated on the Woodland Trust's written permission, which only Hidde can request.** The ATI licence was read in full on 2026-08-06 (verdict and endpoints in OPEN_DATA_SURVEY.md): non-commercial only, and public internet mapping services are explicitly forbidden without prior written permission. No account or download changes that, so NO ATI data is downloaded or used until permission exists; the draft request sits in drafts/woodland-trust-permission.md for Hidde to send. Until then a run still does not research London by web sweep on its own; if Hidde wants London moving before permission arrives, authorising the expensive web-research path is his explicit call in session, not a run's. London's real state, corrected 2026-08-06: all 10 photos approved (the "London has no photos" claim was stale), stories fine, but no register and no walk, since its ten trees run from Totteridge to Kew. What London needs: a central walkable cluster.
     - The recorded pushbacks, so the course change is a decision and not a drift: London's demand evidence is still zero in Search Console; Chicago, DC and Boston are full builds with no scouted register; Porto (17-tree walk, 4 photos) is in no phase and stays the walk showcase in the background photo lane. Hidde heard all three and confirmed.
     - **"Deep enough" keeps its definition, unchanged: at least one complete walk of 4 to 8 trees inside roughly 2 km, photos on most of that walk, honest pins, season data.** Clarified by Hidde 2026-08-08, because a session had been reading it more strictly than he wrote it: **honest pins means labelled honestly, NOT confirmed.** An approximate pin that says it is approximate satisfies the bar, and a city is not held back for having them. His words: "im ok with honest pins, lets user improve them in the future." This is the always-cuttable list applied exactly as written, precision first, with readers as the correction layer that every tree page already invites. What is still never cuttable is the label itself: a pin marked confirmed when it is not remains the one mistake this project cannot afford.
     - **The working order, re-ruled by Hidde 2026-08-06 (his "record this please" on the ease-first swap): easy phase-2 cities pull forward, the three from-zero US builds wait for evidence.** The measured cost gap is roughly 4:1 (a from-zero US build is 250-350k tokens with no register; Vienna, with 16 trees, 13 photos and 394 register trees in reserve, may pass the bar in one pass). The order: **(1) Barcelona and Rome** (nearly done), **(2) Paris and Berlin** (cheap depth: 185 register trees and 460 Wikidata images respectively), **(3) Vienna and Edinburgh** (pulled forward from phase 2; Edinburgh compounds UK-first), **(4) Amsterdam and New York**, where **NYC is the US demand probe**: deepen it, watch Search Console, and **Chicago, Washington DC and Boston build only if NYC shows a signal**, staying parked if it stays silent, **(5) Dublin** (pulled forward), **(⚡) London jumps the whole queue the moment the Woodland Trust's written permission arrives.** This is the supply-side doctrine applied to the rollout: probe an expensive market with one city before betting three.
   - **Within that, cities people search for beat cheap villages (Hidde, 2026-08-05: "ik had wel op iets grotere steden gehoopt. hier trekken we geen gebruikers mee denk je niet?").** The cheapest cluster in the register is a village with a lot of designated trees and no traveller: Priverno has 46. So the queue sorts on whether the place is one people actually travel to first, then on density. `scripts/backlog.py` does this sort; its tourist list is hand-made and says so, and should be replaced by Search Console once that has enough history rather than extended by hand forever.
   - **And the honest shape of what is left: in the register countries, breadth in big cities is nearly finished.** 46 of the 56 major cities anyone would name are already published. Of the ten that are not, only Turin (16 registered trees, a walkable cluster of 10), Genoa (14) and Catania (5) have register supply at all; Pisa and Siena have zero entries in the national Italian register. **So the volume that pulls users is now depth, not breadth**: Barcelona publishes 16 against 202 registered nearby, Lisbon 12 against 70, Naples 12 against 58, Milan 10 against 48, Porto 10 against 41, Palermo 8 against 38. The next genuine big-city wave (Madrid, Valencia, Bilbao, Zaragoza, Hamburg, Marseille, Bordeaux) is a licence-and-import question, not a research question: Valencia's 482-tree GeoJSON is already located, and the rest need their registers scouted first.
   - **Hidde still owns the queue.** The data proposes, he disposes: a run may follow the recorded data-led order on its own, but reordering beyond it (skipping a country, pulling one forward on taste) stays his call alone.
   Country pages (Contract G, blueprint v1.5) ride with coverage: the renderer exists since 2026-08-01 and the Netherlands is live, so a country page now needs nothing but its hand-written intro in data/countries/[slug].json (species-page discipline, Paris-quality, unique, with an `article` field for countries that take "the"). The moment a country passes three published cities, write that intro and the page builds itself. Waiting with three or more cities right now: United Kingdom, Italy, Spain, Poland, France, Portugal, Japan.
5. **Register-layer countries, licence-led.** The parallel quantity track (see "The register layer" below): scout, import and map official registers, in the order the data itself allows; a run picks whichever of rung 4 and 5 it can move furthest in its window, trip cities always winning ties.
6. **Photos and depth on published cities.** The 8-of-10 photo target and pin work continue as the background lane, no longer gating anything (the 13 documented dead-end gaps from the depth phase wait for UGC or new sources; do not re-run exhausted hunts). Hunt photos for NEW cities during their research, hard, per Step 4; two honesty rules never bend: no photo without a verified open licence and attribution, and a genuinely unreachable target is recorded in CURATION.md, never looped on.
7. **Product work, when everything above is satisfied.** Draw the top unblocked item from `PRODUCT_TODO.md` and finish it completely. That lane exists because runs used to be allowed only to research trees while the product itself waited for a human session; Hidde closed that gap on 2026-07-26. Its rules live in the file and are strict, because a CI run cannot see the page it changes: reversible only, contracts must validate, every item verified by build output or grep rather than eyes, no visual-taste work and nothing from the hard list.

**The steady fortnight, agreed with Hidde 2026-07-31, review 2026-08-14.** Until then the course does not move: half of each day's runs backfill quality on the cities the quantity burst left thin (photos toward the 8-of-10 floor, vague pins down, the Portugal register corrections for Lisbon and Porto from data/registers/portugal-icnf.json, and best_time backfill where a real seasonal peak is missing from the data: September fruit peaks first, the shelf simulation showed Sep/Dec nearly empty. Honest peaks only, per Step 3; an empty month beats an invented one), the other half add new coverage per the data-led order. No strategy changes land before the review; new ideas go to BACKLOG.md. On 2026-08-14 the numbers decide the next phase: search clicks per week, and whether a single waitlist signup or reader submission exists.

**Quantity is the current phase, ruled by Hidde 2026-07-30 ("later weer kwaliteit toevoegen").** Coverage built the surface (33 cities by 2026-07-26, Google started serving); depth made the served pages deliver (pins near-flawless, 220 photos, the last gaps proven dead ends); now breadth resumes on both layers at once, curated cities and register countries. Quantity never buys from the never-cuttable list: verification, pin honesty, licences, living public trees and the four-tree bar are the product, not polish. Re-verify flagged items and check the news for fallen trees along the way; depth returns as the phase when the data says so and Hidde flips it.

This is only safe because of one thing, and it is not negotiable: **every tree ships with `location_precision` set honestly.** A pin that admits it is vague sends someone to the right park knowing they will have to look. A pin that fakes precision sends them to a spot where the tree is not, and that is the one mistake this project cannot afford. Precision is optional; honesty about precision is not. Never mark a pin confirmed to make a city look finished.

Append what you did to `LOG.md`, newest first, in the format that file describes.

### Step 1 — Research the city's trees (BE THOROUGH)

**The assembly line, ruled by Hidde 2026-08-06: tokens per tree must come down.** The 2026-08-05 retro measured 32,870 tokens per published tree against 19,000 the week before, and the diagnosis is structural: each pass carried a fixed cost of 150k to 200k regardless of yield, because one agent did five jobs (search, verify, write, hunt photos, format) and read 86KB of corpus before starting. Five changes, all binding:

1. **Every brief is generated, never written from memory: `python3 scripts/passcheck.py --brief <place>`.** It prints the paste-ready brief: live status, ids, the actual register candidates with coordinates, what earlier passes found or rejected, the hosts that hang. Three briefs left on a false premise on 2026-08-05 (Napoli, Firenze, Munich); a generated brief cannot, because it is built from the data the premise would contradict. The proof case came the same day the flag was written: the 2026-08-06 handover listed Valencia as "never done" while it was live with 10 trees.

   **And every pass is claimed before it is dispatched: `python3 scripts/passcheck.py --claim <place> --kind verify|write|photo`, then commit and push the claim, then dispatch.** Release with `--release <place>` when the output is merged. This exists because passcheck knew what was published and nothing knew what was being worked on: on 2026-08-06 a session write pass and a night run wrote the same nine Padova stories twenty minutes apart, 89k tokens for nothing. The claim lives in data/in-flight.json, expires after 4 hours on its own (a dead session never blocks a city), matches across name spellings (a claim on Padova blocks Padua), and passcheck refuses to print a brief for a claimed place. It is a courtesy lock, not a mutex: it is only visible once pushed, so the push is part of the claim, and it catches the minutes-apart collisions that actually happen here, not seconds-apart races.
2. **A pass is one of two kinds, never both.** A **verification pass** confirms alive, sources, species, age and pin, delivers structured facts with `verify_notes`, writes zero prose and hunts zero photos; its whole rulebook is `BRIEF_RESEARCH.md` and it does not read CLAUDE.md. A **writing pass** turns 15 to 20 verified trees ACROSS cities into stories in one context per `BRIEF_WRITING.md`, so the tone calibration is read once, not per city. The main session merges, rebuilds, runs QA and commits.
3. **Model tiering, mechanical since 2026-08-06 (Hidde: the line itself must pick the right AI).** The tiering lives in the agent definitions under `.claude/agents/`, not in anyone's memory: `verify` pins Sonnet (retrieval-heavy; never the smallest model, because verification is where the fabrication risk lives), `write-stories` and `photo-judge` pin Opus (judgement about what ships). Dispatch a pass by its agent name and the model follows; the generated brief prints which agent to use. Dispatching outside these agents is what needs a reason. Anything deterministic (clustering, register parsing, photo candidate retrieval) is a script and costs nothing.
4. **No pass under six expected candidates.** The fixed cost makes small passes expensive by definition; thin targets wait in the queue until a batch (neighbouring cities, one register) carries the overhead.
5. **Photo hunting leaves research passes entirely**, superseding the three-photos-per-pass rule of 2026-08-05: `scripts/photo_hunt.py` sweeps Commons by API into `data/photo-queue.json` (measured agent cost was 72k tokens per usable photo; the API sweep costs none), and a periodic viewing pass judges queued candidates against the Cadiz standard, 20 to 30 images in one context. The two honesty rules are untouched: verified licence and attribution always, and look at the pixels before approving.

The target on the meter: **at or under 15,000 tokens per published tree**, read weekly from RETRO.md. Every pass still logs to `data/agent-costs.json` (kinds now include `verify` and `write`); if the line does not come down, the werkwijze moves again, and that is a session decision with Hidde, not a run's.

**The current course, approved by Hidde 2026-08-03: register first, cluster over count, batch by country.** It replaces city-by-city web research for the three focus countries, because all three have an official register that gives species, age and often coordinates in one document.

- **Import the register once, then research becomes selection.** Spain: the Andalusian catalogue plus the municipal catalogues (Cordoba's held 54 trees with GPS, girth and dating in one PDF). Portugal: ICNF, already imported. Japan: the Environment Ministry's giant-tree database, which records every tree in the country over 300 cm girth with measurements, plus the national and prefectural Natural Monument designations. With the register in hand a city is "pick the best from an already-verified list and write", not "search the web", which is the difference between three hours and under one.
- **Choose walkable clusters, not famous singletons.** Measured 2026-08-03 across all 81 published cities: Cadiz spans 600 metres with all five trees inside two kilometres, York 100 metres, Rotterdam 900. Kyoto spans 35 km with one tree within two kilometres of any other, Hong Kong 45 km. Twenty cities have fewer than half their trees within walking distance of each other. That, not the count, is why Cadiz reads as a good afternoon and Kyoto does not. So: research a district at a time rather than a metropolis, and prefer a tree that joins a cluster over a marginally better one that stands alone. A large city gets several clusters of five to eight; a small one gets a single cluster of four to six. The ten-per-city default stands for now (Hidde, 2026-08-02), but within it, density wins ties.
- **Batch by country, not by city, in two passes (Hidde, 2026-08-03: "is de snelste route niet een run voor een heel land te doen, en dan per stad stuk voor stuk aanvullen").** The country pass is cheap because most of it is arithmetic rather than research: import the register, then run `python3 scripts/cluster_register.py data/registers/[file].json` to group every entry into what can actually be walked between. On Portugal's 124 registered trees that produces 9 walkable clusters covering 106 of them, with Lisbon falling out as three separate walks rather than one list. The city pass then starts from "verify these six trees around this point", which is a far smaller job than "find the ten best trees in this metropolis". What the script cannot do, and a run still must: decide whether a designated tree is actually remarkable, find the second source, and write it. A register says protected, not worth the walk.
- **How many trees a city gets, now that clusters decide it.** The floor is unchanged: four verified trees or no page. A walk is four to eight trees inside roughly two kilometres, because past eight it stops being an afternoon. A compact city is one cluster and is finished at five or six, which is why Cadiz ships five and reads better than cities with ten. A large city is several clusters, and the tenth tree should complete a second walk rather than add a lonely eleventh location on the far side of town. The ten-per-city default still caps things for now, but within it the count is an output of the clustering, not a target to fill.
- **The regional register before the national one, where both exist (learned across Caserta and Rome, 2026-08-05).** Italy's national MASAF file has no age field and no vitality field, which are the two things a page needs most. The regions fill both. Campania publishes a per-tree card at `agricoltura.regione.campania.it/foreste/monum/scheda_NNN.html` with an age estimate and a description; one scrape gave the second source for nearly every tree in Caserta. Lazio publishes an xlsx carrying the reason each tree was designated, a notes column saying which girth figures are stem lists rather than trunks, and **a second sheet of removed trees with reasons**, on which five Roma trees sit as dead while still live in the national file. So: find the regional list first, and treat the national register as the index rather than the source.
- **Three photos per city per pass, maximum (Hidde, 2026-08-05).** Photo hunting is the least productive hour in a research pass and it expands to fill whatever time it is given. Three good ones make the page; the rest is an honest gap that a later pass or a reader can close.
- **Photo gaps close faster.** Search Commons by name, by category and by geosearch for the shortlist only, then stop. Measured yield across three cities researched 2026-08-03: 2 usable photos of 12 candidates in Cordoba, 4 of 10 in Nara, 6 of 11 in Fukuoka. It is the least productive hour in a research pass.

**Search in this order (Hidde, 2026-08-02: the point is faster runs per city, not more searching).** Each step is narrower and higher-yield than the generic sweep, so most cities are done before the last step. Stop when the city has its trees; do not run every step for its own sake.

1. **Name the places first, then search the places.** Spend the first five minutes listing the city's historic parks, botanical gardens, palace and estate grounds, and its churchyards, cathedral closes, monasteries, convent gardens, temple and shrine precincts and old cemeteries. Wikipedia's city page, the municipal parks department and a tourist map give this list in minutes. Then search each named site plus a species word, in English and the local language (kerk, klooster, iglesia, ermita, chiesa, igreja, Kirche, jinja, taisha, -ji). This finds trees no listicle mentions, because the ground was protected and someone tended it for centuries; on sacred ground the tree often predates the building beside it. Evidence for both, measured on our own data: Lisbon's Jardim da Estrela (giant ficus, jacarandas) was missed entirely by the city-level sweep, and 146 of 546 published trees, 26 percent across 60 of 78 cities, already stand on sacred ground without anyone ever having searched for it on purpose.
2. **Ask whether the city has already published its own tree route (learned from Setubal, 2026-08-04).** Search for "[city] roteiro das arvores", "[stad] bomenroute", "[ciudad] ruta de arboles singulares", "[city] tree trail", plus the municipality's own environment or parks pages. Setubal's parish publishes a tree-by-tree walking route with species, place, age and height, which independently corroborated nine of our ten entries and solved the single most expensive part of a research pass, the second source, in one fetch. Many European municipalities do this and almost nobody links to it. Check it before any generic searching.
3. **The local newspaper's own survey of the city's monumental trees (learned from Trieste, 2026-08-05).** Search "[citta] alberi monumentali" plus the local title, "[stad] monumentale bomen" plus the regional paper, and the same in any language. A paper that has written a piece on "the city's oldest trees" names individual trees, gives ages, says which is oldest and reports what the council has done about them. Il Piccolo's survey of Trieste's 48 monumental trees supplied in one fetch the ages that neither the national nor the regional register carries, because no register anywhere has an age field for Italy. It is a source to verify against, never to copy from, and it usually beats step 4 outright.
4. **The official register, if the country has one.** A municipal or national list of protected/monumental trees is the fastest verification there is: it gives species, age and often coordinates in one document. OPEN_DATA_SURVEY.md records which countries have usable ones and under which licence.
5. **The generic sweep**, for whatever the first two missed: "[city] oldest trees", "[city] remarkable trees", "[city] monumental trees", "[city] famous historic trees", in English AND the local language.
6. **Cross-check and fill:** monumentaltrees.com for verification of age and location claims only (NEVER copy their photos or text), Atlas Obscura, local history blogs, park authority pages.

- A tree qualifies if it is: genuinely old OR visually spectacular OR historically significant, AND publicly accessible
- **The day-trip boundary (Hidde, 2026-08-01):** a tree within roughly 30 minutes by public transport of the city centre belongs on the city page, labeled honestly: the real place name in its location fields, the true travel time in transport. Blarney counts for Cork, Fota counts for Cork, Coole Park counts for Galway. What it does not allow: quietly presenting an out-of-town tree as standing in the city.

**The count follows the trees. Decided by Hidde 2026-07-26, reframed by him 2026-08-02.** Ten is the working default, not a law: "de enige reden waarom ik met 10 begin is SEO strategie en haalbaarheid... uiteindelijk is de visie dat er een behapbaar aantal bomen in de buurt te vinden zijn, geen exacte nummers". So ten stays the standard for new cities, because it makes a city completable in one research pass and it is what the page titles promise, but a city may grow past ten when genuinely remarkable trees turn up later or a reader sends one in. Growing a city is normal work, not an exception to argue for. What the reframing does NOT license: padding. The bar per tree is unchanged, and a city still ships the trees that clear it, never a number filled to look finished. When a city passes ten, its page title and question page must stop saying ten. The doctrine bends the number in both directions now, but only ever to follow the trees: a city with five hundred worthy candidates still ships exactly ten, because a finite, completable list is what makes collecting work (see BACKLOG.md on the rejected two-tier model). The doctrine bends the number downward only, never up. A capital with ten genuinely remarkable trees gets ten; a smaller city gets the five or eight that truly clear the bar; padding a list to reach ten is fabrication's polite cousin and forbidden (Verona shipping 8 was right). A place earns a page only when at least four trees survive verification; below that it gets no page yet, and its best tree can still appear in a collection. Exclusivity is the point: a collector wants every entry to deserve its spot, and a two-street village with one fine oak is a collection entry, not a city.

**An entry must be alive (Hidde, 2026-07-27: "we doen niet aan dode bomen").** The product is standing before something that has been alive for centuries; a carcass, stump or relic breaks that promise and makes the years-counter lie. A dead tree may appear inside a story as context, never as a collectible entry, however famous the remains (Queen Elizabeth's Oak in Greenwich and Vienna's Stock im Eisen both fail this test and are to be replaced; a fallen original honestly succeeded by a living replanting, like the Elm of Saint-Gervais, passes when the entry describes the living tree). **A tree we cannot re-confirm does not hold a city back (Hidde, 2026-08-06: "ik vind dat je heel spastisch bent over dode bomen. ja we willen die liever niet maar het hoeft niet een hele stad tegen te houden. een gebruiker mag ons ook ooit wijzen op deze is dood").** The rule above is about a dead tree as an ENTRY, not about a confidence threshold before a city may open. Zaragoza was held back because three of its four trees had no dated proof of life, and that was the rule applied harder than it says. Publish, and say what you know: where the source is old or the confirmation is thin, the page states it in the FAQ in plain words, names what has already been lost from that source, and asks the reader to tell us. Readers are the correction layer, which is the standing position everywhere else on this site. What does NOT change: a tree you know to be dead never ships, and a tree reported dead gets checked and removed the same day.

Runs: sweep CURATION.md's 2026-07-27 dead-tree suspect list, verify each against sources, and replace confirmed dead entries with living trees researched to the normal standard, one city per pass, with an honest note. Replacements reuse the old id and the page must redirect or the old URL stay resolvable, per the Barcelona bcn_008 precedent.

**An entry must be a collectible point (Hidde, 2026-07-26).** One identifiable tree, or an ensemble only when the ensemble itself is the destination: compact, famous for being exactly that, with one obvious place to stand. The Lomanstraat tunnel and the Meiji Jingu Gaien avenue pass; a thousand ordinary planes along a kilometre of La Rambla do not, there is nothing to stand at and nothing to have seen. Barcelona's bcn_008 failed this test as "The Plane Trees of La Rambla" and was replaced on 2026-07-26 with a genuinely singular tree, the Silk Tree of the Ciutadella (same id, so no URL broke). Apply the test to every future ensemble candidate.

**Work from the supply side, not from a quota (Hidde, 2026-08-04: "kunnen we niet beter op de bomen focussen die goedkoop tot onze beschikking liggen en die uitwerken ipv overal verplicht 10 bomen te maken").** He is right that the expensive tree is always the ninth in a thin city, while the first five are nearly free. One correction to his framing, and then it is exactly right: cheap and dense are different axes, and optimising for the cheapest TREE would give five fine trees in five different towns and a walk nowhere. **So rank by the cheapest CLUSTER, not the cheapest tree.**

The score is dense times data-rich: how many register trees sit within two kilometres of each other, multiplied by how many fields the register already fills per tree (species, name, age, girth, height), divided by the spread. A cluster of six inside 500 metres where the register gives species and age is the cheapest good city page that exists, because the state already made the selection and the research pass only has to verify and write.

Run it with the clustering script; the ranking as of 2026-08-04, all Portuguese because Portugal is the only register imported in full:

| Trees | Spread | Place |
|---|---|---|
| 29 | 0.9 km | Mealhada (Bucaco) |
| 13 | 2.0 km | Setubal (published 2026-08-04) |
| 14 | 3.4 km | Guimaraes |
| 8 | 1.4 km | Viana do Castelo |
| 6 | 0.5 km | Serpa |
| 6 | 0.6 km | Guarda |
| 5 | 0.1 km | Cascais |
| 5 | 1.2 km | Pacos de Ferreira |

**And the registers deepen published cities as cheaply as they open new ones**, which had not been noticed: Barcelona has 61 register trees within 3.8 km against the 10 we publish, Porto 26, Sintra 5. Adding to a city that already ranks is worth more than opening a city that does not.

**What this changes about the count.** Nothing about the floor, four verified trees or no page. But a city gets the trees its cluster actually holds: Cascais is five and finished, Serpa is six and finished, and neither should be padded toward ten. The ten in the page titles was always a cap, and from here it is not even a target.

**How to brief a research pass, and why the last one cost too much (2026-08-02/03).** Cordoba's research ran two and three quarter hours and came back with twelve candidates, an exhaustive list of rejects and a separate full photo sweep. Seven trees shipped. Nara's ran alongside it, was still going when the session closed, and was lost entirely, because a background agent lives in the session that started it. Both problems have the same shape: a brief that asks for everything, unbounded, with nothing written down until the end. So:

- **Write findings to disk as they are found, never only at the end.** A research pass appends each verified candidate to `data/research/[city].md` as it completes it. A pass that dies halfway then leaves half a city behind instead of nothing, and the next session continues rather than restarts.
- **Ask for what ships, not for everything.** Eight strong candidates is plenty for a ten-tree page; the ninth and tenth cost as much as the first eight and usually get cut.
- **Keep the rejects as data (Hidde, 2026-08-03: "we hebben ze uiteindelijk wss ooit nodig, ik verwacht dat het platform uiteindelijk alle remarkable trees van de wereld gaat mappen").** They go to `data/leads/[city].json`, never rendered, in two clearly separate kinds. **Leads** are trees that failed only on our evidence bar or on the count: undated, single-sourced, no photo, or simply ninth in line. Those are the raw material of the wider map, and a city that grows past ten starts here rather than from a blank search. **Blocked** are trees that must never ship whatever happens later: dead or gone, private land, an access-restricted site, a location its source withholds, or a non-collectible point like an avenue or a whole wood. Each blocked entry carries the reason, so a future pass reads why in one line instead of re-researching it and arriving at the same no. Cordoba's file is the worked example: eleven leads, seven blocked.

  **Widened by Hidde on 2026-08-05 into a standing rule: every tree a run comes across goes into the database, not only the ones a city pass rejected.** His words: "ik wil dat je alle bomen die je vangt in je onderzoek in je database opslaat vanaf nu, niet allemaal hoeven live te staan want sommige zullen misschien moeten worden geverifieerd, maar ik wil geen onderzoek meer voor niks zijn geweest." So a scouting sweep, a register scan, an Overpass query or a half-finished pass all land on disk before the session ends, in `data/leads/` when they are per-city candidates, in `data/registers/` when a register licence has been verified, and in `data/research/` when they are notes rather than trees. Nothing waits for the end of a pass: findings are appended as they are found, because two things have already been lost this way, a full Nara pass and a sweep agent whose four children finished after it had stopped. Publishing is a separate decision from keeping, and unverified is a fine reason not to publish and never a reason to throw away.
- **Photos are a second pass, on the shortlist only.** Hunting images for candidates that will not be published is the most expensive way to produce nothing.
- **Time-box it.** Say in the brief: report what you have after roughly forty minutes rather than continuing to completeness. An unbounded brief will always spend the whole window.
- **Prefer register-first countries when the window is short.** A national or municipal catalogue gives species, age and coordinates in one document; Portugal and Spain verify in minutes what takes an hour elsewhere.

**What registers get wrong, and what to check every time (learned on Portugal and Setubal, 2026-08-04).** A register is the cheapest source there is and it is not a clean one. Four checks, each of which has already caught a real error:

- **Units are not what the column says.** ICNF publishes trunk girth in metres; our import labelled the column girth_cm, so a 2.84 metre trunk read as under three centimetres and nobody noticed for days. Sanity-check every numeric field against the physical world before trusting it.
- **Fields go corrupt in ways that look plausible.** Three Setubal olives carry "2009" in the age column, a year sitting in a field that should hold a number of years. Publishing that unchecked would have given three ancient olives an age of nine.
- **Registers double-count what a visitor sees as one thing.** Three of Setubal's thirteen entries were twins: separately registered, metres apart, distinguishable only by girth. Shipping them separately would have produced near-identical pages. Fold twins into one entry that describes both, and record the folded ids as leads.
- **The register's total will not match the municipality's.** Setubal's council counts 21 classified trees against the 16 in the national register for the same municipality. Reconcile before any page quotes a national or city total, and never present a register count as a count of what exists.

Two more that follow from the same pass: an age in a register is the age at last measurement, so add the years since and say so; and no register anywhere carries a vitality field, so whether a tree still stands is always a per-tree check that the register cannot do for us.

**Where a week of tokens actually went, measured 2026-08-04.** The first full week of agent-driven work, totalled from the agents' own reported usage:

| Kind of work | Tokens | What it produced | Per unit |
|---|---|---|---|
| City research passes | ~620k | 32 published trees | 19k per tree |
| Photo hunting | ~145k | 2 usable photos | 72k per photo |
| Register scouting and import | ~460k | 1,048 known trees, plus a permanent map of what is usable per country | 0.4k per tree |
| Demand and SEO research | ~77k | the collection strategy, reusable | n/a |
| Wasted | ~250k | nothing | n/a |

Four conclusions, and they matter more than any single research technique:

1. **Scouting compounds; research does not.** Register work cost 460k once and now yields trees at near-zero forever, twenty-five times cheaper per tree than research and it keeps paying. Research costs its 19k per tree every single time. So an hour spent making the next hour cheaper beats an hour spent producing, and the instinct to "just do a city" is usually the expensive instinct.
2. **The waste was never in the work, it was in the coordination.** Roughly a fifth of the week bought nothing, and not one of those tokens was spent badly researching: a Nara pass died when the session closed because background agents live in the session that started them, a Fukuoka pass duplicated a night run already working the same city, and a photo hunt spent 145k to approve two images. All three are orchestration failures with cheap fixes, now recorded.
3. **Ask whether the task is judgement or retrieval before dispatching anything.** Retrieval is code and costs nothing: clustering a register, fetching a CSV, searching Commons by category. Judgement needs an agent: is this tree remarkable, does this source hold up, is this photo any good. The 72k-per-photo number is what it costs to make an agent do retrieval, and it is the single worst ratio the project has produced.
4. **A brief's cost is set by its stopping condition, not its length.** Adding "report what you have after roughly forty minutes" did more for Setubal's cost than every other instruction combined.

**Expensive work gets discussed before it starts (Hidde, 2026-08-04).** Before dispatching anything expected to run long or fan out wide, say in chat what it will cost and what it should return, and get his answer. This is his subscription and a research pass is not a free action: they run from 70k to 230k tokens each, and three in parallel is most of a working day's budget. Estimate, state it, then start. The exception is small bounded work whose cost is obviously trivial.

**Speed, as a standing instruction (Hidde, 2026-08-02: "sneller zou wel beter zijn").** A run's window is the scarce resource, so spend it on finding and verifying trees, not on re-deciding things that are already decided:

- **Check whether the city is already done or being done, before dispatching anything, and check it with `python3 scripts/backlog.py` rather than by eye.** `data/cities/[slug].json` existing means it shipped; the queue's status field and LOG.md's newest entries say what is in flight. On 2026-08-03 a night run published Fukuoka while a session research pass was already running on it, and the two overlapped on four trees out of ten. On 2026-08-05 two passes were sent out to "open" Napoli and Firenze while Naples and Florence had been live for weeks, because the queue was read by matching register place names against our own city names. **Never match places by name.** backlog.py matches on distance, which no language can fool, and it prints what is online, what would be a new page and what would deepen a live one.
- **Read this file's own history before researching a city.** CURATION.md records what was already tried and found empty. Cork was researched from zero three separate times before anyone checked; that is three windows spent on one city. **CURATION.md and LOG.md now hold one week; everything older sits in `archive/`, moved weekly by `scripts/archive_logs.py` and never deleted** (Hidde, 2026-08-08, on token cost: the two files had reached 1.6 MB in 24 days, and are 173 KB after). So the check is `grep -ri "<place>" CURATION.md archive/`, not CURATION.md alone: absence from the living file is not evidence a hunt is new.
- **Dispatch the search wide, verify narrow.** Candidate discovery parallelises well (one agent per city, or per park list); verification does not, because it is the part that must not be rushed. Two cities researched in parallel and verified carefully beats one city done end to end.
- **Photo hunting has a floor and a ceiling.** Hunt hard while a city is being written, then stop: a documented dead end in CURATION.md is a finished piece of work, and re-running an exhausted hunt is the single most repeated waste in this project's history.
- **Commit the smallest complete step first.** A city with four verified trees committed beats eight unverified in a session that gets cut off.
- **Never re-litigate a decision.** DECISIONS.md exists so a run can look up an answer in seconds instead of reasoning it out again.

### Step 2 — Verify each tree
For each candidate tree, cross-reference at least 2 independent sources for:
- Existence and species
- Approximate age
- Exact location (GPS coordinates)
If sources conflict or only one source exists, include the tree but set `curation_status: "flagged"` with a note explaining the uncertainty.

### Step 3 — Write the stories
150-250 words per tree (the Paris run of 2026-07-15 sets the standard; anything over 250 words gets shortened). Style rules:
- Direct, specific, slightly vivid. Scott Galloway meets nature writing.
- Lead with the most surprising fact.
- Include what the tree has "witnessed" historically.
- Never use: "hidden gem", "must-see", "breathtaking", "nestled".
- Never use em dashes.

Stories and any page copy must satisfy SEO_GEO_BLUEPRINT.md — in particular P2 (answer first, in the first two sentences where the page is a question/city page) and P3 (unique content, no fill-in-the-city-name templating) — and follow TONE_OF_VOICE.md, including its calibration examples and hard bans.

**Every tree carries a year calendar (Hidde, 2026-08-02: "elke boom een mooi overzicht met bladloos, blad, verkleuring, fruit, bloem, en die moeten gewoon kloppen").** The calendar shows the whole year, bare / in leaf / flowers / fruit / autumn colour, with the current month marked.

**What the curve draws, ruled by Hidde 2026-08-05: how much there is to SEE, not leaf cover.** The first version drew leaf cover, which made every evergreen a straight line, and a straight line says nothing ("nu, als het een groen blad heeft, dan is die lijn gewoon recht. Dat zegt ook niets"). So each moment carries a judgement in `intensity` on the species file, one of `unseen`, `nice`, `striking`, `worth the trip`, and that judgement is what gives the curve its height. A ginkgo flowers in April and nobody can tell; it turns gold in November and people cross town. `nice` is the default, deliberately the dull one, so a species nobody has judged yet gets no false peak. `worth the trip` is scarce for the same reason `best_time` is: 8 of 25 species carry one. Curves are never normalised per species, so an uneventful tree stays low, and a species where nothing rises above `unseen` gets no chart at all, only a plain sentence. The build refuses a species that records real moments and still draws a flat line. `best_time` is unchanged and now lives inside this chart as its marked peak, which is also where the "at its best right now" chip sits: the tree page used to stack two curve charts making the same promise.

It lives per species in `data/phenology/[species-slug].json`, not per tree, because phenology is a property of the species in a climate rather than a fact about an individual. The build shifts the months by latitude (a month early below 42N, a month late above 56N) and prints nothing at all below 25N, because the temperate pattern is simply wrong in the tropics and a wrong calendar is worse than none. Each phase may carry a short label saying what actually happens ("acorns drop, and a good mast year buries the ground in them"). The page states plainly that the weeks shift with the year.

A species with no file shows no calendar: an honest gap, exactly like a missing photo. 25 species covering 302 tree pages exist as of 2026-08-02; adding the rest is normal run work, oldest-species-first by tree count. Every entry needs a real source, and evergreens get an empty bare row rather than an invented one.

**Priority note, Hidde 2026-08-08: season data is the lowest-priority depth item, below photos.** His words: "don't waste too much time on finding the season of the tree, it's less important than photos and we can do it later." Setting `best_time` while writing a story, from a species file that already exists, stays free and welcome. Researching a species' phenology from scratch is not worth a research window in the current phase. Everything below still governs what a `best_time` may say when one is set; none of it is loosened, it is simply not chased.

**Set `best_time` when, and only when, a tree has a real seasonal peak.** Broadened by Hidde on 2026-08-02, because the first reading was too narrow: a peak is anything a visitor would notice and enjoy on the day, not only a burst of colour. Three families count:
- **Flower, leaf and colour**: blossom, autumn colour, catkins, fresh leaves. The original reading.
- **Fruit, nuts and mast**: acorns underfoot in October, conkers, sweet chestnuts you can gather, figs, the olive harvest, mulberries. Hidde: "deze boom heeft nog steeds vruchten, eikels, kastanjes, op een moment wat leuk is om te weergeven." Use `kind: fruit`.
- **Bare winter structure**: a veteran tree with real architecture is at its most legible in January, when the leaves are gone and the whole frame of it shows. Hidde: "geen bladeren in de winter wat leuk is om te weergeven." Use `kind: bare silhouette`. Only for trees whose shape is actually the point: a hollow, buttressed or wildly limbed veteran, never a young street tree.

Two limits keep this honest. **A tree gets one `best_time`, so pick its strongest moment**, and **scarcity is what makes the badge mean anything**: if every deciduous tree claimed both an autumn fruit peak and a winter silhouette, the "at its best right now" badge would light up permanently and stop being a reason to go anywhere. Give it to the trees where the moment is genuinely worth the trip and leave the rest empty.
 This is the single strongest reason a page gives someone to actually go, because it turns "nice" into "this weekend". A tree with a pronounced moment gets:

```json
"best_time": { "months": [11], "label": "late November, when the ginkgo turns gold" }
```

`months` is the list of month numbers when it is at its best and drives the "at its best right now" badge; `label` is the short phrase a reader sees, in the tone of voice. Set `kind` too (Hidde, 2026-07-29, the PictureThis point: say WHY it peaks): one of `flowers`, `fruit`, `autumn colour`, `catkins`, `fresh leaves`; it renders as an icon chip on the season block. The build derives a kind from unambiguous label words when the field is missing, and shows nothing when in doubt; an explicit field always beats derivation. Rules:
- Only add it when the moment is real and specific: blossom, autumn colour, a wingnut's summer catkins, a magnolia's ten days. An evergreen or an ancient yew that looks much the same all year gets no `best_time` at all. Forcing one on every tree is filler and defeats the point.
- Base it on the species and the local climate, and say what actually happens in the label, not just a month. "May, when it flowers" beats "May".
- Keep it honest: if a peak spans a range, use the real months. Guessing a precise week you cannot support is the same mistake as a fake pin.

### Step 4 — Find photos
Search Wikimedia Commons and other openly-licensed sources (CC0, CC-BY, CC-BY-SA only). Record the exact license and attribution. If no good photo exists, set photo status to `missing`. NEVER use photos from monumentaltrees.com, Google Maps, or any source without a clear open license.

**Every rendered image goes through `img_srcset()` (the image standard, Hidde 2026-07-31: "kunnen we deze image handling standaard maken").** thumb_url() maps Wikimedia (fixed buckets, capped at 960), Unsplash and iNaturalist to right-sized variants; scripts/qa.py fails the deploy if any img tag ships a full-resolution original, so a new render site cannot skip the helper unnoticed.

**Which photo, the Cadiz standard (Hidde, 2026-07-31: "alle fotos bij Cadiz zijn goed, je ziet goed de boom, niet te ver en niet te dicht ingezoomd, genoeg licht").** Cadiz is the calibration set for photo selection, the way Paris is for tone. A photo qualifies when: (1) the tree is unmistakably the subject and fills most of the frame, crown and trunk both readable; (2) it is neither a distant view where the tree has to be searched for, nor a close-up of bark or leaves; (3) it is taken in daylight, properly exposed and in colour: never a night shot, and never black-and-white or archival imagery, however atmospheric (Hidde, 2026-07-31: "liever geen foto dan zwart-wit"); a 1904 stereograph says museum, not go-there-this-afternoon; (4) it survives the card crop: pages crop images to wide cards, so the CENTRE band of the image must still show the tree, not the buildings beside it (the Falcone Tree took three attempts because rounds one and two failed exactly this). And the rule that makes the rest enforceable: **LOOK at the image before approving it. Render the actual file. Never approve from a filename, a description or a thumbnail guess; if tooling cannot display images this run, the photo stays `found_needs_check` for a run that can.** Which is not a hypothetical: measured 2026-08-07, the GitHub Actions runner's egress proxy blocks `upload.wikimedia.org` and `api.openverse.org`, while a local session reaches both normally. So the API sweep runs anywhere and the VIEWING PASS ONLY WORKS IN A SESSION. A night run that tries it loses its window. Correction recorded 2026-08-08, because the first version of this note blamed the wrong thing: Wikimedia is not unreachable and does not block us, it RATE-LIMITS. A burst of 29 image fetches got HTTP 429 after twelve; roughly one request every three seconds runs clean. A viewing pass throttles, and the CI problem is a proxy question rather than a source question. Read that honestly, because for a long time it was not true: `found_needs_check` **renders on the site**, so 26 photographs nobody had looked at were live when this was discovered on 2026-08-06. That stays the behaviour, because holding a page's only image back over a risk a reader can report contradicts the same day's ruling on dead trees. What it needs, and now has, is a third status: **`held` keeps a photo in the file and off the site**, for the case where showing it would be wrong rather than merely unchecked, such as a good photograph that might be of the wrong tree. Margaret Island in Budapest is the worked example: two excellent images of "a very large plane tree", on an island with three separately named notable planes, so attaching one would be a guess dressed as a fact. A tree with no qualifying photo keeps an honest gap; a mediocre photo is not a rough version of a good one. Hidde restated this on 2026-08-08, and his wording is the clearest the project has: "I don't think making a random picture of a tree to fill it up is a good idea, better nothing than that." So a photograph ships only when it is OF THIS TREE and meets the standard. Never a generic photograph of the species, never a nice view of the park it stands in, never a stock image dressed as a record. The species silhouette that a photo-less tree page carries is not an exception to this: it is line art, obviously a drawing rather than a photograph, and it appears beside a sentence saying in plain words that no photograph of this tree exists. If it ever starts reading as a substitute for the real thing, remove it rather than soften the rule.

**Credits: record always, display only when the licence requires it (Hidde, 2026-07-29).** CC BY and BY-SA photos keep their visible on-page credit, that is the licence's price and it never gets stripped; if a visible credit has to go, the photo changes to a source that needs none (Unsplash License), never the other way round. Decorative and marketing imagery (hero, app page) comes from no-credit-needed sources from the start.

**The owner is not a content source (Hidde, 2026-07-30: "stop met het mij vragen fotos te maken").** A run never asks Hidde to photograph, visit or field-verify anything; one owner does not scale and it is not his job. The supply ladder for a photo gap is: open-licence sources (below), then reader submissions (UGC, the flywheel), and otherwise the gap stays an honest gap in CURATION.md. AI imagery is allowed ONLY as clearly-labeled illustration (the parked dummy-image direction, BACKLOG.md); an AI-generated image presented as a photo of a real, specific tree is fabrication under hard rule 2 and never ships. Any paid generation tool needs his yes first (hard rule 5).

**Do not stop at Wikimedia.** Coverage there varies by country rather than by tree, which is why Tokyo came in at 7 photos out of 10 and London at 0. Same trees, different places to look. When Wikimedia comes up empty, try in this order:
- **iNaturalist**, which often has CC-licensed photographs with coordinates attached, useful for confirming a pin as well as illustrating it. Check the individual observation's licence, it varies per photo.
- **Flickr**, filtered to CC licences. Old and well photographed trees are often there under CC-BY.
- **Openverse**, which searches many open repositories at once.
- **The city or park authority's own site**, where the licence is sometimes explicitly open.

A photo does more for goal 1 than any paragraph, because it is what makes someone decide the walk is worth it. Hunt hard, but per the MVP mindset, never hold a city back for one.

### Step 5 — Commit and update state
- Save the city JSON file
- Update city-list.json (status: pending → needs_curation)
- Append to CURATION.md: city name, date, number of trees, number flagged, photos missing
- Commit with message: "Add [city]: 10 trees, X flagged, Y photos missing"
- Rebuild the site so the new city page goes live. The generated pages (city, tree, question, collection) must conform to the Layer 2 contracts in SEO_GEO_BLUEPRINT.md — titles, meta descriptions, schema, and internal link minima. A page that fails that validation does not deploy.

### Improvement mode (when all 100 cities have data)
Cycle through existing cities oldest-first and: hunt for missing photos, strengthen weak stories, re-verify flagged items, check for dead trees in the news.

### Collections (any time coverage allows)
Collections publish under the same regime as everything else since blueprint v1.3 (2026-07-27): the research standard, script-checked entries, superlatives per hard rule 8, readers as the correction layer. No owner approval; new collections are announced in LOG.md like any other work.

### The register layer (Hidde's two-layer model, approved 2026-07-29/30)

Above the curated cities sits a second, wider layer: **officially designated remarkable trees from government registers, shown as honestly-labeled dots on the map.** Hidde's framing: the app that shows all monumental trees becomes "the first connected tree register of the world", with our curated selection of the most epic trees on top. Layer 2 is coverage and demand-sensing; layer 1 stays the product. Rules for runs, all binding:

- **One official register counts as the source** for a layer-2 dot ("ik vertrouw de overheid wel"); the two-independent-sources bar keeps applying to everything in layer 1.
- **Semantic filter, never bulk import:** only trees a register itself designates as monumental/remarkable. Never full municipal tree inventories. Hard rule 10 applies in full: access-filtered, withheld or blurred locations respected, private land excluded.
- **Licence first:** a register is usable only with a verified open licence compatible with commercial-leaning reuse (CC BY, 政府標準利用規約 2.0, PDL 1.0). Non-commercial terms (NL national register, MLIT P32) disqualify a source outright. Record the proving sentence in OPEN_DATA_SURVEY.md before importing anything.
- **Honesty over polish:** register coordinates are often area-level; imported dots default to `location_precision: approximate` unless verified. Dots carry the label "from the official register, not yet verified by us", get NO own pages (thin-page risk) and are NOT collectible; the tier/game design is parked in BACKLOG.md until the mid-September checkpoint, and a run may not build any of it.
- **Pilot: Japan, riding with the wave.** Scouted sources and verdicts live in OPEN_DATA_SURVEY.md ("Japan scouting", 2026-07-30): Tokyo's CC BY CSV with coordinates is the first import candidate, the national Natural Monument register is the backbone (read its /top/policy in full first), Kyushu/Hokuriku prefectures still need scouting. Build order for runs: finish the scouting, then the data file (data/registers/), then the explore-map layer, smallest honest step first.

### Step 0b — Process reader submissions (before picking a new city)

Readers submit trees and whole cities through a public form. Hidde is deliberately not in this loop: submissions come straight to you.

Submissions arrive in the `submissions` table of Hidde's Supabase (the native form on /contribute, live since 2026-07-31). A run reads them ONLY when the SUPABASE_SERVICE_KEY env var is present (curl GET {SUPABASE_URL}/rest/v1/submissions with apikey+Bearer set to it); when the secret is absent, skip without complaint. Track processed rows by id in `data/submissions-processed.json`, same as always.

The old channel stays readable during the transition: if `SUBMISSIONS_CSV_URL` is set in scripts/build_site.py, fetch it at the start of every run. Each row is one submission. Skip any row whose id already appears in `data/submissions-processed.json`.

For each new submission:
1. Treat it as a research lead, never as fact. A submitter saying a tree is 500 years old is a claim to verify, not a source.
2. Apply the exact same bar as your own research: two independent sources for existence, species and age, and a location you can place precisely. The hard rules still apply in full, especially "never fabricate" and "photos need a verified open licence".
3. If it verifies: write the story in the tone of voice, add it to the right city file, and credit the submitter by the name they gave (`"submitted_by"` on the tree). If the city does not exist yet, create it as a new city file with the submitted trees, and set its status to `needs_curation`.
4. If it does not verify: do not publish it. Record it in CURATION.md under the submission's city with what is missing, so Hidde or a later run can pick it up.
5. Either way, append the row id to `data/submissions-processed.json` so it is never handled twice, and note the outcome in CURATION.md.

A submitted tree that verifies is worth more than a new city researched from scratch, because it proves someone cares about that city. Process submissions first, then continue with the next pending city if the usage window still allows.

## The mandate

This section exists so a run can decide for itself. Hidde is not watching, does not want to be the thing that starts the work, and will read `LOG.md` when he feels like it. Everything below is what he would say if you could ask him.

### What this is for

Two goals, deliberately ranked.

**1. Get someone to walk to a specific tree and enjoy standing in front of it.** Not "raise awareness of trees", not traffic. A named person, on a named street, looking up at a named tree that turned out to be worth the walk. Every feature, page and sentence is judged on whether it makes that more likely.

**2. Earn money.** Hidde does not need to get rich off this, but it should pay for itself and then some. (The "few thousand euro a month" figure that used to stand here was called loose talk by Hidde himself on 2026-07-26, GO_TO_MARKET.md "the revenue arithmetic: parked"; treat the amount as undecided, the direction as real.)

When the two conflict, goal 1 wins, because goal 2 does not exist without it. Nobody subscribes to a map that sent them to the wrong place.

Note what that does and does not imply. It does not mean polish before coverage: a map of five cities cannot get anyone outside who does not live in those five. It means never lying about what you have. A rough pin that admits it is rough still gets someone to the right park, and they can enjoy the hunt. A rough pin dressed up as exact gets them to a spot where the tree is not, and they do not come back. Build wide, label honestly.

**The bar under both: the experience has to be good.** MonumentalTrees has more trees than this project ever will, and it does not matter, because using it is miserable. That is the entire opening. So a page that is accurate but ugly, slow, confusing or joyless has not met the standard, even though every fact checks out.

Read that as a floor, not as a reason to stop and polish. The existing page template already clears it: a story worth reading, a map, a working directions button, nearby trees, an honest note when the pin is rough. Pouring a new city into that template gives you a good experience by default, so coverage and quality are not in conflict here. They only conflict when someone proposes rebuilding the template, and the answer to that is in the section above.

### Ship rough, ship wide, fix later

This project is unproven. Nobody has walked to a tree because of it, and nobody has paid for anything. Until that changes, the job is to put a lot of usable material in front of people quickly and find out whether any of it lands. Polish is what you do to something people already use.

**The default is the roughest version that is honest and useful.** Before any piece of work, ask: what is the smallest version that gets one person to a tree, or tells us whether anyone cares? Do that, ship it, move on.

Two lists, and the difference between them is the whole idea.

**Always cuttable, without discussion:**
- Precision. An approximate pin that says so is a finished first version.
- Photo coverage. Hunt hard for photos, they do more for goal 1 than any paragraph, but never hold a city back for them.
- Completeness. Eight good trees ship. The ninth can come later.
- Consistency and polish across pages, matching styles, tidy edge cases.
- A third and fourth source once two independent ones already agree.

**Never cuttable, at any speed:**
- Never fabricate. An invented fact is not a rough version of a real one.
- Never fake precision. Vague is fine when it says it is vague. See the honesty rule in Step 0.
- Never publish a photo without a verified open licence and attribution.
- Never promise the visitor something that is not there.
- Never publish a tree whose location its source deliberately withholds, or one on private land that is not open to visitors (hard rule 10). Speed is never bought from a tree's safety or someone's front garden.

Speed is bought from the first list only. Anything bought from the second is not a fast MVP, it is a broken product with a good excuse.

**The trap to watch for: a gate, threshold or floor that enforces polish before there is demand for it.** Ask what evidence says anyone is waiting on the other side; usually the honest answer is nobody, and the gate should not exist. It has already happened here once (the 2026-07-21 quality floor; the full story is PRINCIPLES.md #13).

Prefer work that produces a signal over work that improves something nobody has used. Hard rule 6 asks whether real people will pay; this section is how that question gets answered, by shipping enough for the question to be answerable at all.

None of this is permanent. It flips when there is evidence: real visitors, submissions arriving, someone paying. Then polish stops being premature and starts being the job.

### Walk the user's timeline before you build

Cheap, and it is not a gate: it costs a minute of thinking and blocks nothing. Before building anything a person keeps, returns to, or accumulates, say out loud what happens at each of these, and fix whatever the answer embarrasses you with:

- **The first minute.** This is the only part that gets tested by default, and it is almost never where the problem is.
- **Day seven, and day thirty.** Is it still there? Does it still make sense? Has it quietly grown wrong?
- **The second device.** They read on a laptop and walk with a phone. Does the thing follow them?
- **The gap.** They come back after three weeks away. What do they find, and is it what they left?
- **The moment it fails.** Not whether it can fail, but what the person loses when it does, and whether they saw it coming.

The lesson behind this list: knowing something does not help if nothing prompts you to ask. A feature whose value accrues over time has to be reasoned about over time, or the one property that matters is the one property never checked. (The worked example, the tree passport that Safari would have silently wiped, is PRINCIPLES.md #12.)

### How Hidde's incoming thoughts get processed (his own instruction, 2026-07-28)

He fires many thoughts, fast, and that is the point of him; the system's duty is the other half: **test every incoming idea against the recorded picture before absorbing it.** Concretely, for each thought: (1) check what CLAUDE.md, PRODUCT_IA.md, PRINCIPLES.md, DECISIONS.md and BACKLOG.md already say, (2) name in one line what it touches, strengthens or contradicts, (3) only then build, park or push back. An idea that contradicts the corpus is not wrong (he outranks the corpus), but the contradiction must be said out loud so changing course is a decision, never a drift. Speed comes after the check, not instead of it.

**The convention check (Hidde, 2026-08-01: "als we een nieuwe functie maken dat je eerst een conventie onderzoek doet - anders zijn we elke keer het wiel zelf aan het uitvinden en dat wil ik niet").** Before building any new user-facing interaction, first look at how the best consumer products do exactly that interaction (AllTrails, Google Maps, Airbnb, PictureThis are the standing references) and adopt the convention rather than inventing one. Novelty in interaction patterns is a cost, not a feature; users arrive trained by the products they already use. The proof case: both search fields were homegrown type-and-submit forms with a native datalist that iOS renders as a broken QuickType strip; the convention (live suggestions under the field, tap goes straight there) replaced them the day this rule was set. Sized deliberately small (Hidde's own worry, same day: "maken we alles te zwaar?"): it is one or two lines naming the reference and its pattern, not a research phase, and it applies to NEW interactions only, never to copy tweaks, styling or reuse of a pattern the site already has. It slots in before the trio check below and feeds its UX line.

**The whole-page check (Hidde, 2026-08-04: "whenever we ask for a new feature, you would only include it by looking at the whole and preferably the whole user experience").** Before adding anything to an existing page, read PRODUCT_IA.md for that page type and then look at the page as it actually stands, top to bottom, in the built output. Two failures on one morning forced this: a three-step band added to the homepage duplicated the four-verb section that PRODUCT_IA.md already described and said to tighten rather than repeat, and a mission paragraph landed directly under the value proposition, stacking two blocks of prose at the top. Both were visible in five seconds of reading the page whole, and neither was visible while looking only at the thing being added. The same morning showed the sibling failure: country pages were built and shipped without a single link pointing at them, because the question "how does anyone reach this" was never asked. So the check has two halves, and the second is the one that gets forgotten: **what does this displace or duplicate on the page, and how does a visitor arrive here at all.** It slots in beside the convention check below; like that one it is two lines of thinking, not a phase. **Half of it is now enforced rather than trusted:** scripts/qa.py fails the deploy on any page that no other page links to, which is exactly how the country pages sat live and unreachable for three days. The duplication half stays a matter of reading the page whole, because no script can tell that two sections make the same promise.

**The trio check (Hidde, 2026-07-28, the product-trio best practice sized for one AI):** every user-facing build choice gets looked at through three explicit lenses before building, one line each: Product (does it serve the verbs, the business direction, "ziel bomen, vorm AllTrails"), UX (the human outside on a phone: does it read as language, does it work at 375px, is it honest), Tech (the most boring reliable implementation, what breaks, is it reversible). For substantial pieces the three lines appear in chat before the build so an empty chair is visible up front; the day's proof was a nav shipped from the developer chair alone. Hidde is the standing PM; the lenses exist so execution never quietly drops one of the three.

### Search evidence is a run's to act on (Hidde, 2026-08-06)

"Ook hier zou ik je autonome rechten willen geven om dit soort SEO-inzichten op te halen en direct pagina's te bouwen." So a run may read Search Console, find a query the site does not serve, and build or retarget the page itself, without asking. No approval step, same as any other reversible call.

Two boundaries survive, and only two. A new page **type** still needs a contract in SEO_GEO_BLUEPRINT.md, and that document needs Hidde's yes (hard rule 7); a new page that fits an existing contract needs nothing. And the evidence has to be real: a query with impressions in Search Console, not a guess about what people might search.

**Check whether the page already exists before building one, and check it against the built site rather than the data files.** The first time this rule was used, the digest reported "ancient tree map" as a gap with 7 impressions and /explore already carried exactly that title and H1. The gap was in the detector, which only knew cities, countries and species and had never heard of the standing pages. A query matching a page we already have is not a gap, it is a ranking problem, and the two need opposite responses: one is a page to write, the other is a page to strengthen. That one turned out to be 142 words of mostly navigation on a page with 800 inbound links, which is a page search engines cannot read.

### Deciding on something nobody wrote a rule for

Most of what comes up is not in any list. Ask three questions, in order:

1. **Does it serve goal 1 or goal 2?** If neither, do not do it, however satisfying it looks. Activity is not progress.
2. **Can Hidde undo it?** Anything reversible is yours to decide. Ship it, write it in `LOG.md`, let him object afterwards. Being wrong in `LOG.md` is cheap.
3. **Can it hurt anyone other than Hidde?** Readers, submitters, people whose photos or data are involved. If yes, stop, whatever question 1 and 2 said. This is the only one that overrides the rest.

Then act. **When questions 1 and 2 pass and 3 is clear, do it, and do not ask.** Waiting for permission is the failure mode this project is built to avoid. Write down what you did and why, especially when the call was close.

Design, layout, features, page structure, copy, iconography and content all pass this test routinely. Hidde has said explicitly that until the product is proven he would rather you moved than checked. Take him at his word.

### The hard list

Five things stay closed no matter how well they score above, each for a reason that does not expire. If something is genuinely adjacent to one of these but not actually it, that is question 2 territory: go ahead and log it.

1. **No accounts, logins, or storage of personal data.** The moment real people's email addresses or profiles are involved, a mistake stops being Hidde's problem and becomes theirs, plus a GDPR liability in his name. Note this is the one item Hidde waved off and it stayed closed anyway: the loose phase is exactly when the foundation that data later flows into gets built, so it is the most expensive time to get wrong. A waitlist form that posts to Hidde is fine. A user table is not.
2. **No taking payments or setting prices.** Payment processors, subscriptions, plan tiers and the paywall line are Hidde's, because they involve his money, his tax position and a contract with a customer. Build features that could later be paid, price none of them.
3. **Nothing irreversible in public.** Retiring a URL Google has indexed, deleting data, force-pushing, giving up a domain. Reversible mistakes are how this project learns; unreversible ones are how it loses work permanently.
4. **Never speak as Hidde, never contact anyone as him.** No emails, no replies to submitters in his voice, no posts under his name. Write the draft, leave it for him.
5. **No new dependencies or third-party services** without Hidde's yes. Each one is a cost, a privacy question and something that can break the site while nobody is looking. The stack is deliberately boring: Python, static HTML, MapLibre, OpenFreeMap. On measurement, ruled by Hidde 2026-07-27 after learning Polarsteps itself runs cookies and Mixpanel: **cookieless analytics is allowed and wanted** (Cloudflare Web Analytics beacon: no cookies, no personal data, no consent banner needed). Ads, ad-tracking and selling visitor data are off today; opening any of them is Hidde's call alone, and per his 2026-07-28 ruling the public pages stay boring-standard about it: no forever-promises in copy, the privacy page states facts, not identity. Cookie-based product analytics becomes normal when the iOS app arrives, with proper consent, the Polarsteps model. Note the site itself never carried a "no tracking" claim in its copy (verified 2026-07-27), so no published promise is broken by any of this.

Also unchanged: **SEO_GEO_BLUEPRINT.md and TONE_OF_VOICE.md need Hidde's yes to edit** (hard rule 7), and so does **the brand**: name, domain, logo, core positioning.

### Where this is going: a paywall, and therefore accounts

Recorded 2026-07-21 at Hidde's request, so no future run has to rediscover it or argue him out of it.

**He intends to charge for this eventually.** Not donations alone, an actual paid tier. Nothing below is a reason to talk him out of that; it is the destination.

**And he is right that the passport cannot stay in LocalStorage forever.** Someone who has ticked off forty trees across three countries will not accept losing them, and they will lose them: browser storage goes when someone clears their data, does not exist in private browsing, never syncs between a phone and a laptop, and Safari on iOS deletes it outright after seven days without a visit. That last one breaks the exact case this feature exists for, a trip where you collect over weeks.

Those two facts are one fact. **A paywall requires accounts**, because an entitlement someone paid for cannot live in storage the browser is free to delete. So the hard list item on accounts is not permanent, and pretending otherwise would be dishonest about where this is heading.

What it does mean is that accounts are a project, not an afternoon. When it happens it brings a server, a database, someone's email address, a privacy policy, a data breach you can now have, subject access requests, and a bill. It also cannot be built without Hidde: it is his liability, his provider account and his name on the privacy policy.

So the sequence, and the reasoning behind it:

1. **Now: keep the passport local, and make losing it hard.** Let people export or back up what they have collected without an account. Cheap, no personal data, and it removes the worst failure before anyone has been burned by it.
2. **When there is evidence anyone wants this:** real visitors, submissions arriving, people actually ticking trees off. Then accounts and payment become the obvious next build rather than a bet.
3. **Never before then**, because an account system built for nobody is the most expensive way to learn there was nobody.

A run may not open this on its own. Building toward it is fine and welcome: keeping the passport data portable, keeping tree ids stable, avoiding anything that would make a later migration painful. Building the accounts themselves needs Hidde.

**Where the account track actually stands (2026-07-29).** The Supabase project exists on Hidde's own account (caimvxiyrtifilimlkqw.supabase.co); the privacy page is approved and carries no personal name (his 2026-07-28 ruling: "Ancient Trees" plus a contact address, with the recorded honesty note that GDPR formally wants a named controller; a registered trade name is the tidy fix later, his call). Magic-link sign-in works and is field-tested, but the page stays an unlinked, noindexed prototype (AUTH_ENABLED False) until account deletion works end-to-end: that is the gate Hidde set, because an account someone can open but not close is a liability in his name.

### The interim paywall line is still undecided

Hidde's instinct is that web and app should draw the line in roughly the same place: a lot free, with the genuinely good features behind a subscription. That points at content free everywhere (every tree, story and location, on both platforms, which is also what keeps the site indexable and serves goal 1) and payment attached to the features that get people out and bring them back: routes past several trees, a log of which ones you have visited, offline maps, a nudge when a tree near you is at its best.

It is not settled, and it contradicts the older `2 trees free per city at €19,99/year` idea (once written in this file, removed 2026-07-29; neither is a decision). Do not resolve this alone and do not build anything that forces the choice. Per hard rule 6, the question is not which model is nicer but whether anyone will pay at all, and there is no evidence yet either way. Work that pays off under every model, better trees, precise pins, photos, faster pages, is always the safer bet.

### What Hidde reads when he has been away

`LOG.md` is the only channel. Assume he has not looked in a week and opens it cold. Lead with what changed about the product, keep what broke separate and obvious, and only use `FOR HIDDE` when something genuinely cannot move without him. A run that quietly did nothing useful should say so plainly rather than dress up the attempt.

## Quality gate: the research standard, not Hidde

Hidde is not the quality gate and will not be at 1,000 trees. Do not write anything that promises human review. The bar is the standard you already apply: two independent sources for existence, species and age, and a location you can place. Readers are the correction layer.

That puts the weight on you, so two rules tighten:
- **Publish what verifies, flag what does not.** A tree you cannot confirm does not go live with confident phrasing. State the range, name the disagreement (P7).
- **Set `location_precision` on every tree**, `"confirmed"` or `"approximate"`. Approximate means you know the park or street but not the spot. The site shows a visible warning next to the directions button for approximate pins, because sending someone to wander a park is a broken promise. Never mark a pin confirmed to make a page look tidier.

`curation_status` and the `status` field on a city stay in the data as internal signal, but they no longer gate publication and no longer show on the site.

## The learning loop, coded rather than remembered (Hidde, 2026-08-06)

"Kunnen we deze leercyclus coderen in onze werkwijze zodat we elke dag wat beter worden." Three mechanisms, each replacing a rule that had already failed by being a rule.

1. **Before writing any research brief, run `python3 scripts/passcheck.py <place>`.** It says whether the place is already published and under what name, how many trees and photos it has, which id prefix it uses and the next free id, how many register trees sit within reach, and what a previous pass already put in leads. Three briefs went out on a false premise on 2026-08-05 (Napoli, Firenze, Munich), each time because a queue entry said new and the check that was written down twice was skipped twice. A rule that fails twice needs a mechanism, not a third writing.

2. **A host that hangs costs the whole window, so `data/fetch-blocklist.json` exists and every brief carries it.** `passcheck.py` prints it. Valencia died twice, ten minutes each time, on `cultural.valencia.es`, which does not refuse a connection but simply never answers. Our own sweep had recorded that host two days earlier, in a research file that nothing reads at the moment it matters, and the Madrid brief carried its fetch note while the Valencia brief did not. **Every fetch gets a hard timeout, `curl -m 20` or `timeout=` on urllib**, and any host that hangs once goes on the list with the date. A refusal costs a second; a hang costs a research pass.

3. **Log every pass's cost in `data/agent-costs.json` when its report comes back**: target, kind, tokens, trees that actually reached data/cities, a one-line note, and where it applies `wasted` (tokens that bought nothing) and `brief_wrong`. An unlogged pass is a day the loop cannot learn from.

4. **Run `python3 scripts/retro.py` and append the day to RETRO.md.** It prints tokens by kind, cost per tree, the three most expensive passes, and the two failure counts kept deliberately apart: tokens that bought nothing, and briefs sent on a false premise. The second is not priced, because those passes still produced work and pricing the detour would flatter neither the day nor the fix.

**The ratchet, and it is the point of the whole loop: a lesson that appears on two different days stops being a note and becomes a build check.** Six already exist by that route: copy promising a tree count the city does not have, one species under two common names, a register file with no licence block, a phenology curve that records real moments and still draws flat, a city published under its local name rather than the English one, and public copy that explains our own publishing rules to the reader instead of telling them what is there. When a walk or a retro finds a class of error twice, the fix ships with the check that makes it unshippable, and removing one of those checks needs Hidde.

**Place names: the site publishes in English, and the build enforces it.** Every page here is written in English and its readers search in English, so a city ships as Florence, Naples, Turin and Padua, never Firenze, Napoli, Torino or Padova. This is not a rule about prose: a tree's street address, the name of its register entry and any quoted source keep the local spelling, because that is what a visitor reads on the sign. The pairs live in `data/city-aliases.json`, which is the single source of truth read by both the build check and `passcheck.py`; the two need it in opposite directions, since matching a published city goes local-to-English while finding register candidates goes English-to-local. Most places have no English exonym and must not be given one (Bologna, Porto, Trieste, Setubal, Cordoba, Krakow), and reviving an archaic one is the same error pointing backwards, which is why Livorno is not Leghorn. Renaming a city that is already live means adding its old slug to `RENAMED_CITY_SLUGS` in build_site.py, which keeps the city page, its question page and every tree URL resolving; hard rule 3 forbids retiring a public URL outright.

## QA: four layers, ruled by Hidde 2026-07-29

The 2026-07-29 whole-product walk found a dead check-in button on all 345 tree pages, five broken photos and seven self-contradicting pages, all live. The lesson is structural, so QA is a standing work form:

1. **Build-time checks, every build.** build_site.py refuses contract violations, bare script text, File: page photo urls, and oldest-tree pages whose answer names a different tree than the page is built around. When a walk finds a new bug class, the fix ships WITH a check that makes it unshippable again; that ratchet is the point, and removing one of these checks needs Hidde.
2. **Machine gates on every push.** scripts/qa.py gates the deploy (internal links resolve, no em dashes or banned words in rendered text, image sources are real image urls); the separate Smoke test workflow renders key pages in headless Chrome and asserts the product works as executed (maps construct, buttons exist, no script source visible as text). A run's rung 2 includes checking that the latest "Smoke test" workflow run succeeded (`gh run list --workflow=smoke.yml -L 1`); a red smoke run means the site is broken.
3. **The fresh-eyes reviewer, daily.** A separate context with no builder memory reviews the last day's diffs and the built site against the corpus and writes findings to REVIEW.md (severity BLOCKER/WARN/NOTE), fixing nothing. Runs pick BLOCKERs up as rung 2 and WARNs as rung 3; Step 0 includes reading REVIEW.md's newest entry. On Mondays it also audits the corpus documents themselves for rot (stale snapshots, superseded sentences, contradictions, history that belongs in DECISIONS.md) and suggests removals; corpus edits are decided in session (Hidde, 2026-07-29). This layer exists because the builder verifying its own work is how the dead button shipped.
4. **The composition walk, periodic, with eyes.** Every page type at desktop and 375px, in a working session: every two weeks, and always straight after a visual system change. CI cannot judge composition, so this layer is never delegated to a run; runs do not do visual-taste work.

## Hidde's curation (optional, when he feels like it)

If he asks to curate, show him the top of CURATION.md and prioritize flagged items and photo approvals; his approval flips a city to `curated` and its trees to `hidde_approved`. Nothing waits on this.

## Hard rules

1. NEVER use content, photos, or text from monumentaltrees.com beyond fact verification. Their disclaimer prohibits commercial reuse.
2. NEVER fabricate tree facts. If you cannot verify age or location, flag it. A wrong location kills user trust permanently.
3. NEVER use em dashes anywhere.
4. Photos must have verified open licenses with attribution recorded.
5. Money, ruled by Hidde 2026-07-27, replacing the earlier €50/month ceiling: **no spending without his explicit approval, ever.** Beyond that there is no fixed monthly ceiling, on the one condition he stated himself: the project has to start earning. Keep runs efficient anyway; waste needs no budget to be wrong.
6. The goal is revenue, not a beautiful product nobody buys. If Hidde starts adding features before validation, remind him: "Have we validated that real people will pay for this?"
7. NEVER ship a page (tree, question, city, or collection) that doesn't conform to SEO_GEO_BLUEPRINT.md. Changes to that document itself require Hidde's explicit approval and a version bump.
8. Superlative claims ("oldest in Europe", "largest of its kind", "more than X and Y combined") must be checked against what other city pages already claim before publication. When in doubt, soften to "one of the oldest" or drop the claim.
9. Use one canonical common name per species so the species pages (Contract F) group correctly. When a species has multiple valid common names, pick the nationality-neutral one and match what other cities already use (e.g. Quercus robur is "Pedunculate Oak", never "English Oak"; Platanus x acerifolia is "London Plane"). The scientific name in parentheses is the tiebreaker for whether two trees are the same species.
10. **Publish public trees only, and never a location its source deliberately withholds.** Decided by Hidde on 2026-07-21. Some registers hide or blur the position of particular trees, and the Woodland Trust does this openly, because visitors damage ancient trees: soil compaction over the root plate, climbing, carving, and simple footfall. Others stand on private land whose owner never invited anyone. This site publishes exact coordinates and actively sends people to the trunk, which makes it capable of causing that harm rather than merely reporting it.

    So: if a source obscures a tree's location, treat that as a decision by people who know the tree and do not undo it, even where the position can be worked out from somewhere else. Do not publish a tree on private land unless it is genuinely open to visitors, and say what the access actually is. Prefer trees a city already signposts, because that is a public authority saying visitors are welcome. When in doubt, leave it out: there are far more qualifying public trees than this project will ever use, so this rule costs coverage that does not matter and prevents harm that cannot be undone.

    This is a question 3 rule in the sense of the mandate: it outranks goal 1, goal 2 and every argument about speed.

(The July handover snapshot and first-session goals that used to close this file were deleted 2026-07-29 on Hidde's yes: everything in them was either done or stale. Current state lives where it is generated: the session-start brief, LOG.md and DATA.md.)
