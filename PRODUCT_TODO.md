## THE NIGHT-RUN QUEUE, rewritten 2026-08-05 after eight passes ran

**Run `python3 scripts/backlog.py` before writing any brief.** Three passes have
now been sent to "open" a city that was already live (Napoli, Firenze, Munich),
every time because a queue entry said new and nobody checked. Do not trust this
list, including this line.

Done in the 2026-08-05 session and not to be repeated: Trieste and Turin opened;
Lisbon, Barcelona, Milan, Naples, Vienna, Brussels, Munich, Seville and Prague
deepened; Zaragoza researched and deliberately held back (see CURATION.md).

1. **Photo backfill, and it is now the biggest gap on the site.** 301 of 678
   trees carry a photo, and ten pages have none at all: Krakow, Maastricht,
   Oslo, Reykjavik, Groningen, Zurich, Arnhem, Budapest, Nijmegen, Breda. Three
   per city maximum. Commons is exhausted for Capodimonte, the Trieste parks and
   the Orto Botanico di Napoli, all documented; go to iNaturalist per-observation
   licences, Flickr filtered to CC, and Openverse instead. Note the Naples pass
   found a real trap: an iNaturalist observation can be CC BY-NC while its photo
   is CC BY, and the photo licence governs. Check the API, do not assume.
2. **Valencia, deepen.** Five municipal walking routes over 508 geolocated
   monumental trees, four of which already contain trees we publish.
3. **Madrid, deepen.** The regional catalogue is a parsable list of 280 trees, 59
   in the city, and its exclusion annex doubles as a dead-tree list.
4. **Barcelona, third pass.** 118 of its 208 register trees are still untouched.
   Pedralbes and Sarria is the largest block left, 51 trees between them.
5. **Porto, deepen.** 41 register trees against 10 published, and the council has
   already clustered the city into eight guided walks.
6. **Genoa, new.** Liguria states CC BY outright, the clearest licence in Italy,
   and 25 geolocated stops were found. Its best cluster is only four trees, so
   check it clears the floor before committing a window.
7. **Palermo, deepen.** 38 register trees against 8 published, but the regional
   PDF 404s and the geoportal has a broken TLS chain, so budget time for access.
   Verify the Piazza Marina ficus first: it was reported seriously ill in March
   2026.
8. **Guimaraes, Perugia, Padova, Como, Trento, Cagliari, Viana do Castelo**: the
   remaining dense clusters in places people travel to, 8 to 14 trees each.

**Vitality is now the standing risk, not coverage.** Four dead trees were caught
this session in registers that still list them as live: a Naples plane down
since 2022, Milan's Villa Litta plane felled in 2015 and still described in the
present tense by the comune in June 2026, Seville's Encarnacion ficus felled
sixteen months after its own catalogue was published, and two of nine checked
Zaragoza entries. Only three sources anywhere carry a vitality field: Seville's
municipal catalogue (four condition fields per tree), Piemonte's register
(removal status inline), and Lazio's (a second sheet of removed trees). Assume
every other register is silent on whether the tree still stands.

**Not worth a pass, recorded so nobody spends a window finding out again:**
Hamburg has eleven natural monuments and exactly one is a tree. Marseille's open
data returns zero tree datasets. Bilbao has five designated specimens in all of
Bizkaia and the flagships sit beyond the day-trip boundary. Venice's whole
regional register is about 110 trees and the provincial ones are mainland.
Bordeaux designates 1,763 points with no species, name or age.

## DONE 2026-08-05: Italy and Andalusia are imported

Both landed in one session. `data/registers/italy-masaf.json` (5,007 entries with
coordinates, 4,522 single trees, 1,653 of them urban by the register's own flag)
and `data/registers/andalucia-rediam.json` (749 trees, 435 with an official PDF
sheet). Licence proofs in OPEN_DATA_SURVEY.md. Re-runnable with
`scripts/import_masaf.py` and `scripts/import_rediam.py`.

Two tools were broken and are fixed: the .xls parser lost every string past the
1,077th, so species names came back as numbers; and cluster_register.py never
returned on 5,007 points and now uses a grid index.

## THE QUEUE, re-sorted 2026-08-05 on Hidde's ruling: places people search for first

Regenerate the whole picture with `python3 scripts/backlog.py`. It matches clusters to
published cities by distance rather than by name (Napoli is Naples, Firenze is
Florence, and matching those by string sent two passes out to cities that were
already live), and it sorts on whether the place is one people travel to before
sorting on how many trees are in the cluster.

**Depth is where the volume is now.** 46 of the 56 major cities anyone would name
are already published, so the biggest untapped supply is not new pages, it is the
register trees standing next to pages we already have:

| city | we publish | register holds nearby |
|---|---|---|
| Barcelona | 16 | 202 |
| Lisbon | 12 | 70 |
| Naples | 12 | 58 |
| Milan | 10 | 48 |
| Porto | 10 | 41 |
| Palermo | 8 | 38 |
| Caserta | 7 | 41 |
| Lucca | 6 | 29 |

**New pages worth opening, best first.** `t` marks a place people travel to.

| n | across | | place |
|---|---|---|---|
| 22 | 2.8 km | t | Trieste (plus a second cluster of 12 within 300 m, the densest in the register) |
| 14 | 3.4 km | t | Guimaraes |
| 14 | 3.3 km | t | Como / Cernobbio |
| 12 | 3.2 km | t | Perugia (plus 7 within 100 m) |
| 11 | 2.0 km | t | Padova |
| 10 | 3.6 km | t | Torino |
| 9 | 3.5 km | t | Trento |
| 8 | 1.4 km | t | Viana do Castelo |
| 12 | 2.6 km | t | Sorrento |
| 7 | 1.5 km | t | Cagliari |

Two warnings on that list. A cluster labelled "Roma" with 14 trees is the southern
edge of the comune at Castelporziano, twenty kilometres out and on presidential
estate land: check access before anyone researches it. And Turin is the one big
city on the list, which is the point Hidde made: the small dense clusters make good
walks but they do not pull users.

**The next big-city wave is an import job, not a research job.** Of the ten major
cities still missing (Bilbao, Zaragoza, Turin, Genoa, Pisa, Siena, Catania,
Hamburg, Marseille, Bordeaux), only Turin, Genoa and Catania have any register
supply, and Pisa and Siena have zero entries in the Italian national register.
Madrid, Valencia, Bilbao and Zaragoza need a Spanish register we have not imported;
Valencia's 482-tree GeoJSON is already located and is the cheapest of those.
Hamburg needs a German Naturdenkmal register, Marseille and Bordeaux a French one.
Scout the licence first, per the rule in CLAUDE.md.

Reading the counts: cluster size is candidate supply, not what ships. A walk is four
to eight trees, the floor of four verified stands, and a cluster that thins out under
verification gets no page.

## One small SEO win from the competitor comparison (2026-07-31, corrected 2026-08-01)

DONE 2026-08-02 (built in run): `scripts/daily_digest.py` now pulls a wider (25-row) query batch and adds a "Content lead" line to the GSC section: the highest-impression query whose text matches no known city, country or species name. Deterministic string match against `data/cities`, `data/countries` and `data/species`, collection titles deliberately excluded (their words are generic enough to swallow real gaps). No page gets built from it. Verified with synthetic GSC payloads (`known_terms()`/`find_content_gap()`/`gsc_section()` all return correct results), since no live GSC secrets are available in this environment to exercise it against real queries; grep `Content lead:` in `DATA.md` once a real gap query appears.

**Query mining line in the daily digest**: extend scripts/daily_digest.py's GSC section with one line: the top query (by impressions, 10d) that has NO matching page on the site, as a standing content lead ("albero roma" found us before we had anything Italian). Deterministic string match against the sitemap's slugs is enough; no page gets built from it automatically.

(The FAQPage-schema item that briefly stood here was withdrawn: question pages have carried a full FAQPage stack since the original blueprint build, verified in output 2026-08-01 with four Q&A pairs per page. Lesson repeated: grep before queueing.)

## Contract G renderer: country pages (added 2026-07-31, blueprint v1.5 approved)

DONE 2026-08-01 (built in session, with eyes): Build build_country_page() per Contract G exactly: root-level country slug (build fails on any clash with a city slug), title/meta/H1/answer-first per the table, hand-written intro from data/countries/[slug].json (page does not build without it), country map with the existing city-chooser panel, city photo cards via city_face(), oldest-tree block, schema stack, link minima, and the city-breadcrumb upgrade (country crumb becomes a link when the country page exists). Verify by build output and qa.py; the first shippable country is the Netherlands. Design language for the city cards and any ranked list: the PictureThis Top-50 form Hidde showed 2026-08-01 (photo left, large rank numeral, name plus species line, chevron), which is also the restyle direction for collection pages when their turn comes.

# Product work for autonomous runs

The queue a run may draw from when every content rung in CLAUDE.md Step 0 is satisfied. Rules of this lane, and they are strict because a CI run cannot see the page it changes:

- Only reversible work. Every item must leave `(cd site && npx astro build)` passing with all contracts validated (the Python renderer this once meant, build_site.py, was deleted 2026-08-09).
- Every item carries a **done when** that a blind run can verify with build output, grep, or a script, not with eyes.
- No visual-taste work here: no logo, icon art, layout aesthetics or colour changes. Those need a session with eyes (Hidde's, or a browser-equipped session). No hard-list items, ever: no accounts, payments, dependencies, brand, blueprint or tone-of-voice edits.
- One item per pass, finished and committed before the next. Log in LOG.md. When judgement wobbles, the mandate's three questions decide.
- **Mobile check on every visual change (PRINCIPLES.md #4):** verified at 375px before shipping, same pass, no exceptions.
- **Human-first check on every template change (PRINCIPLES.md #9):** any block a loop generates gets read as a stranger would read it before it ships. Repeated boilerplate phrases inside loops are a bug even when every contract passes.

## Queue, in order

### 1. The account track, opened by Hidde 2026-07-26 (supersedes the earlier supersession)
Collect returns to the web as the app's rehearsal: login UX (magic link, Slack-style states) is being built in-session behind an AUTH_ENABLED flag, unlinked and noindexed until Hidde's Supabase project and privacy page exist. Runs: do not wire any backend beyond what the session wired 2026-07-28 (real magic-link against Hidde's Supabase, page still unlinked), do not link the page, do not touch the flag. HARD PRECONDITION before the login ever links publicly: the self-service delete option the privacy page promises must exist and work (Supabase has no client-side self-delete; it needs an edge function with the service key, which is session work with Hidde present). The game design (points, badges, sets) is being settled with Hidde in conversation. Sign-in was end-to-end tested 2026-07-28: first machine-tested with a disposable inbox (mail in 4s, valid session), then field-tested by Hidde himself ("hij doet het hoor"), which also confirms deliverability to a real mailbox. Two auth users exist: Hidde and one disposable test account (attest...@web-library.net), the latter to be removed the moment the delete function exists.

### 2. DONE 2026-07-26, built in session: the season radar page
A page at `/in-season` (linked from the Season act on the homepage once it exists): every tree whose `best_time.months` contains the current build month, grouped by city, each with its label phrase and a link. Static is fine: the site rebuilds many times a day, so "this month" stays true. Month with nothing in season shows the nearest upcoming moments instead of an empty page (empty states teach, PRINCIPLES.md).
Shipped as /in-season: current month plus the two coming months, grouped by city, linked from the homepage Season act, contracts green. Runs keep it honest simply by rebuilding the site. Skip to item 3.

### 2b. DONE 2026-07-27, built in session: the daily data digest
Shipped end-to-end the same day: DATA.md exists, the Data digest workflow (05:15 UTC daily + manual dispatch) writes one entry per day with Cloudflare zone numbers (currently honest zeros: the domain does not route through Cloudflare; nameserver move to Cloudflare was attempted and parked, see CURATION.md) and LIVE Search Console numbers via the OAuth route Hidde authorised in session. Secrets GSC_CLIENT_ID / GSC_CLIENT_SECRET / GSC_REFRESH_TOKEN are in CI. Verified: run 30293823091 wrote a complete entry with real GSC data. Runs should read DATA.md each morning and may sharpen its templated conclusion line when something real happens. Original spec follows for reference.
Hidde: "ik zou graag ook een dagelijkse conclusie van je krijgen naast de changelog wat de google console en cloudflare zegt. wat is de data geweest van de afgelopen dag en wat zijn de veranderingen."

Build: a new root file `DATA.md`, newest entries on top, one dated entry per day, written by the first run of each calendar day. Each entry: yesterday's numbers, the change against the day before, a 7-day trend, and ONE plain-language conclusion sentence (what this means, in the tone a busy owner reads cold). No graphs, no padding; a day with nothing notable says so in one line.

Sources, strictly stdlib urllib (hard rule 5, no new dependencies):
- **Cloudflare**: GraphQL Analytics API using the `CLOUDFLARE_ANALYTICS_TOKEN` secret, CONFIRMED present on the repo since 2026-07-26 (verified via `gh secret list` in session 2026-07-27, so do not wait on it; zone listed via the API with the same token). Pull for yesterday: requests, unique visitors, top 5 paths, top 5 countries.
- **Search Console**: (historical note, superseded the same evening by the OAuth route above, which is LIVE) an earlier attempt was parked; what it established, so nobody walks the dead ends again: (1) service-account KEY files are impossible on his account: Google's secure-by-default enforces `iam.managed.disableServiceAccountKeyCreation` and his no-organization consumer project cannot override it (Manage policy requires org-level permissions he cannot obtain); (2) a service account named `digest` already exists in his project "My First Project" with the Search Console API enabled, both harmless to leave; (3) the working route, when he ever wants 10 minutes, is OAuth: consent screen (External, published), Desktop client, one-time consent click in his browser with a local loopback catcher run from a session on his Mac, then refresh-token exchange as a plain HTTPS POST (stdlib), secrets set via gh. Until then: whenever a fresh manual GSC export lands in the repo, fold its numbers into that day's entry with the export date clearly stated. Never present stale export numbers as current.
- **Volume honesty, standing rule from the same session**: while volume is tiny, the conclusion sentence must say so plainly ("nog steeds ruis-niveau, geen conclusies uit te trekken") rather than narrate noise as trend. Hidde explicitly called out strategy built on week-one metrics.

**Done when:** `DATA.md` exists; the digest step runs in CI, writes a dated entry when the token secret is present, and skips with a single honest LOG.md line when it is not; a second run the same day does not duplicate the entry; entries render valid markdown (spot-check by grep on the date header format).

### 2c. SESSION-RESERVED (needs eyes, runs keep out): Phase A of PRODUCT_IA.md
The verb nav with the Explore dropdown, the homepage grid compressed to a directory block, tree-page actions above the story plus nearby-trees footer, and the humanity sweep of all loop-generated blocks (PRINCIPLES.md #9) in the same pass. Built in preview first, shipped on Hidde's look. Runs: do not attempt; template-anatomy work without eyes is how machine-logic blocks happen.

### 3. CHECKED 2026-07-27, clean: copy audit against the value proposition and the durable-claims rule
Walk every template string in `scripts/build_site.py` against CLAUDE.md's value proposition and the rule that copy may only promise what the paywall will survive. Remove drifted or filler copy; tighten to the tone of voice.
Ran the done-when's own greps against a full rebuild of `site/dist` (516 pages): zero hits for "free forever", "always free", "never pay", "no accounts" as a promise; zero hits for the banned tone words (hidden gem, must-see, breathtaking, nestled); zero em dashes. Nothing to fix. Re-run this same check after future copy changes to `build_site.py` rather than assuming it still holds.
**Done when:** grep finds no "free forever", "always free", "no accounts" (as a promise), "never pay" anywhere in generated pages; spot-grep of banned tone words ("hidden gem", "must-see", "breathtaking", "nestled", em dashes) stays zero across `site/dist`.

### 4. The collections programme, promoted by Hidde 2026-07-26
Collections are the highest-leverage SEO pages we have (broad queries, zero new research, they recombine the 328 verified trees) and each one is designed as a future badge set: finite, completable, 5 to 12 trees across cities. Search Console already shows us ranking accidentally for "ancient oaks" (position 26) and "old trees" with no page aimed at either.

Draft up to two per pass from this slate, best query-fit first: ~~Ancient oaks of Europe~~; **Trees older than 1000 years, blocked honestly**: only 3 trees on the site clear 1000 years at a conservative (not just legendary-high) age estimate (London's Totteridge Yew, Istanbul's Bahçeköy plane, Kyoto's Heian Cedar); BACKLOG.md's own trigger wants 4+, and Athens' two candidate olives (ath_002, ath_004) both have a conservative low end under 1000 (300 and 700 respectively) despite eye-catching high ends, so padding the count with those would be exactly the kind of number-chasing hard rule 8 warns against. Revisit once a fourth city produces a tree whose age doesn't depend on picking the generous end of a dispute. ~~The ginkgos worth a November trip~~; ~~Europe's most remarkable yews~~; **~~Trees that outlived their city~~, DONE 2026-07-27**: 7 trees that survived fire, war or revolution destroying what stood around them (Sensoji's firebombed ginkgo, the Cheapside Plane, two more Tokyo shrine trees, two Tiergarten/Bellevue Berlin trees, the Buffon Plane), grounded entirely in existing story text, script-checked; ~~The great planes of Europe~~; ~~Wisteria and blossom worth a spring trip~~; ~~The oldest tree in every country we map~~; **~~Trees Planted by Kings and Their Gardeners~~, DONE 2026-07-29**: 13 trees genuinely planted by, for, or on the direct order of a named monarch/royal appointee (an emperor's transplanted camphor, two shoguns' own plantings, Henri IV's herbalist and his son both raising Paris's two oldest trees, Queen Victoria's Irish sequoia), drawn from BACKLOG.md idea #2. Roughly 45 royal-word candidates read in full against the actual bar (planted by/for/on a monarch's order, not merely standing in a royal park or mentioned near one); most rejected as incidental (London's Royal Oak predates its royal enclosure, the Evelyn Mulberry's own text doubts the Peter-the-Great legend, Vienna's Sisi-Platane is just named after a habit). Every superlative reused verbatim from each tree's own existing story, none invented fresh. **~~Trees With a Known Planting Date~~, DONE 2026-07-29**: 14 trees whose actual planting year (not an age estimate backed into a year) is on record, from BACKLOG.md idea #1, spanning Florence's 1720 Micheli Yew to Antwerp's 1994 liberation-anniversary linden. Deliberately zero overlap with the Kings collection (a 32+-candidate pool made that easy); explicitly excluded legend-based "said to have planted" claims and ring-count-inferred ages disguised as planting dates, the exact distinction this idea's bar turns on. Ground every entry in existing verified data only. **Correction, 2026-07-29: "Trees That Survived Wars and Fires" is not actually open.** It shipped 2026-07-27 under a different title, "Trees That Outlived Their City" (same idea, same bar, see the entry above and data/collections/BACKLOG.md idea #3, struck through there since that date); this slate line was stale, restating it as still-open would have meant drafting a near-duplicate collection. Every Priority-1 idea in data/collections/BACKLOG.md is now shipped or honestly blocked, Most Valuable Trees included: checked 2026-07-29 (a dedicated research pass across all 34 other published cities), still only 2 qualifying entries (both London), below the 5-entry publishable floor; parked until a new city adds a genuinely valued tree, not to be re-run without new coverage first. Do not re-open this line as "needs new research" without checking BACKLOG.md idea #4's own current status first. Priority-2 ideas (data/collections/BACKLOG.md #6-7) are recombination-only but thin on qualifying trees today: Churchyard Yews found only 1 of 9 site-wide yews actually standing in a churchyard (London's Totteridge) when checked 2026-07-29, well under a publishable minimum; Trees Older Than 1,000 Years is the same 3-tree gap already recorded two sentences up. Both wait on new cities, not a research pass on existing data. One future slate item, recorded 2026-07-26 when Hidde asked "why not the US": Live Oaks of the American South, unlockable once New Orleans (queued) and ideally Savannah or Charleston are built. The US already consumes our European pages (third country in week-one Search Console without one promoted US city); full US city coverage stays behind Europe because ancient is thin there, its cities are car cities, and its SERPs are the hardest, but the South's live oaks are the honest exception.

Since blueprint v1.3 (2026-07-27) collections publish without owner approval, under the research standard: every entry script-checked against the tree data, superlatives per hard rule 8, voice per TONE_OF_VOICE.md. Announce each new collection in LOG.md like any other work.
**Done when (per pass):** up to two new collection JSONs validate, build and are linked; a check script confirms every listed tree exists with the claimed property (age, species); the LOG.md entry exists.

### 5. DONE 2026-07-28, built in session: seasonality completion pass
Every qualifying tree across all 33 cities gets an honest `best_time` (species with a real peak only; evergreens get none, per Step 3's rules).
The required genera (ginkgo, wisteria, wingnut, horse chestnut, magnolia) were already fully covered by prior sessions. This pass found and closed a narrower real gap: Bald Cypress, Black Locust, Black Mulberry, Japanese Pagoda Tree, European Beech and Northern Red Oak each had `best_time` on some entries and not identical-species siblings with the same genuine peak. Added it to 13 trees, each written fresh from its own story, not copied. Left Oriental Plane and Pedunculate Oak alone deliberately: most entries of both correctly have no `best_time`, since neither species carries a single specific worth-the-trip moment the way the others do; a lopsided ratio there is the no-filler rule working, not a gap. Full detail in CURATION.md 2026-07-28.
**Done when:** a count script shows every ginkgo, wisteria, wingnut, horse chestnut, magnolia and deciduous-showpiece species carries `best_time`, and no evergreen (yew, holm oak, cypress, cedar, pine, camphor, olive) does.

### 6. DONE 2026-07-27, built across two passes: internal linking for collections and species pages
Question pages should link a relevant collection where one exists; species pages should be linked from every tree of that species (already contract-checked) and from city pages where 3+ trees share a species.
Species linking shipped first (5 cities). The collection-linking half turned up a real bug on the way: both the question page and the city page were picking the same first collection unconditionally regardless of whether the city actually had a tree in it, with hardcoded copy ("the yew, the oaks", "Several of these trees") that was false for most cities. Fixed both to filter by actual membership and state the real count. Verified on built output: 23 question pages and every city with a collection tree now link a genuinely relevant one, the rest fall back to a generic `/collections` link. Nothing left in this item.
