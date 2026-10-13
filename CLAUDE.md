# Ancient Trees: project instructions

This file is the working rules only. The reasoning, dates, quotes and worked examples behind every rule live in **RULINGS.md** (the full text of this file as it stood on 2026-10-12, under the same headings) and in DECISIONS.md. Read those when a rule's edge is unclear; do not load them by default. When a new ruling lands, its rule goes here in one or two lines and its story goes to RULINGS.md or DECISIONS.md.

Every script check named in this file is a ratchet: removing one needs Hidde.

## What this is

Ancient Trees (ancienttrees.app, plus an iOS app) maps the remarkable old trees worth walking to. Owner: Hidde, a designer in the Netherlands. The system researches, verifies and publishes; readers correct. Hidde sets direction and is not the quality gate.

**The product is four verbs: find, walk, collect, season.** North star: *I am somewhere, I open it, it knows where I am, it shows me a cool tree nearby and a walk past a few, tells me why they are special, and I tick off the ones I visit.* Features outside the four verbs need his explicit yes.
- The map and "trees near me" are the product and lead everywhere. Cities, species, countries, parks and collections are SEO acquisition: keep them, never let them crowd out the core.
- Nothing is gated today, but premium is the destination. Copy never says "free forever", "no accounts" or "always". Claims that survive a paywall (every tree free to explore, no ads) are fine.
- Phase 1 (now): traction on the website, collecting people and data. Phase 2: app and money. Test for any work: does it collect people, collect data, or win traction? If none, it waits.
- Goal 1: get someone to walk to a specific tree and enjoy it. Goal 2: earn money. Goal 1 wins conflicts. Tiebreaker 3: the richer database (store provenance with every fact; never let the schema assume "city").

## Files

```
data/cities/        one JSON per published place          data/leads/       candidates + blocked, never rendered
data/collections/   collections (Contract D)              data/registers/   imported official registers
data/species/       species intros (Contract F)           data/research/    pass notes, appended as found
data/countries/     country intros (Contract G)           data/city-queue.json  rank, score, target per city
CITY_QUEUE.md       the single city order and how far     SEO_GEO_BLUEPRINT.md  page contracts (Hidde edits only)
TONE_OF_VOICE.md    story voice, Paris calibrates         PRODUCT_COPY.md   words inside the product
drafts/PITCH_VOICE.md  copy a stranger reads              CONVENTIONS.md    looked-up interaction conventions
BRIEF_RESEARCH.md / BRIEF_WRITING.md  pass rulebooks      DATA.md           daily digest (read the newest entry only)
LOG.md              what each run did, newest first       CURATION.md       what could not be verified (3 days; older in archive/)
DECISIONS.md / RULINGS.md  the why                        REVIEW.md         fresh-eyes findings
```

## Tree schema

Reference: data/cities/london.json. Per tree: `id`, `name`, `species` ("Common (Latin)"), `age_estimate`, `age_min`, `age_max`, `age_basis` (`source|derived`), `location` {address, latitude, longitude, neighbourhood}, `story` (150 to 250 words), `verified_sources`, `access`, `transport`, `photo` {url, license, attribution, attribution_url?, status `missing|found_needs_check|approved|held`}, optional `photos` (further photographs, same licence terms as the lead), `curation_status`, `location_precision` (`confirmed|approximate`, always set honestly). Optional: `girth_cm`, `height_m` (from a register or plaque, never our prose), `best_time` {months, label, kind}, `recognise`, `location_site`, `official_register`, `pin_source`, `verify_notes`.
- `attribution_url`: the photographer's name renders as the link (creditLinkParts in site/src/lib/images.ts; feed `credit_url`).
- A reader's photograph carries `source: "contributor"` and `contributor_user_id` together, always (preflight refuses one without the other; photo_takedown.py depends on it).

## How runs fire

- nightly.yml knocks every two hours; `.github/workflows/knock.yml` dispatches when nothing started for two hours. Windows are 120 minutes, up to four attempts. Self-chaining stays off unless Hidde turns it on.
- The weekly budget is the real limit (roughly 1,000 to 1,400 machine minutes in seven days, shared with Hidde). `python3 scripts/run_health.py --week`. Brake: two usage-limit deaths in six hours stop extensions. `WEEK_BUDGET_MINUTES` 1400 and `DAY_BUDGET_MINUTES` 200 are Hidde's numbers.
- **The window is the job**: after every merged item go back to the shelf until 25 minutes remain. Commit the smallest complete step first.
- Shell: one command per Bash call. No `&&`, pipes into a second binary, heredocs, loops, or multi-statement `python3 -c`; write a script to out/tmp/ and run it. Keep every path inside the repo. (`check_run_prompt_forbids_compound_commands()`.)
- A run does not push builds; it dispatches one deploy at the end of its window.

## Step 0: pick the work (the ladder)

Take the first rung that applies. Append what you did to LOG.md, newest first.

1. **Reader submissions and app photographs.** `python3 scripts/sightings_inbox.py --status`; every verdict written with `python3 scripts/judgement.py`. See "Reader input".
2. **The site is broken.** `python3 scripts/health.py` (exit 1 = act). A REVIEW.md BLOCKER is answered, not obeyed: check its evidence first. Record with `health.py --answer <date> "<what>"`. A finding that turns on a host in data/fetch-blocklist.json needs a session; never retire a tree to clear an unverifiable BLOCKER.
3. **Something published is wrong** (fallen tree, wrong pin, false fact). Wrong costs trust; vague does not, if it says so.
4. **Enrichment and new coverage**, under Google recovery mode below. City order lives in CITY_QUEUE.md only (`python3 scripts/city_queue.py --next`). `python3 scripts/scout_next.py --target` says BUILD or SCOUT. Out of focus (Hidde): Israel, Africa, India, Russia (`out_of_focus` in data/register-scouting.json, which also holds every scouting verdict).
5. **Register-layer countries**, licence-led (see "Registers").
6. **Photos and depth** on published cities with demand (`photo_gaps.py --shortlist`; `--coverage` for the old list). One photograph per city is an aim, but only once a city has five trees.
7. **Recognition lines**: `python3 scripts/recognise.py --stuck`, `--brief <city> [--gaps]`, `--apply lines.json`. Restatement only, from what the entry already holds (BRIEF_WRITING.md).
8. **Page gaps**: `python3 scripts/pagegaps.py`. Intros may be machine-written, from that subject's own trees (P3).
9. **Product work**: top unblocked item in PRODUCT_TODO.md, under its rules (reversible, verified by build output or grep, no visual taste, nothing from the hard list).

When nothing is left to verify or write: scout a register or translate a page (`prepare.py --status` BACKUP block). A window never ends empty while either names work.

## Google recovery mode (since 2026-10-01, outranks the supply rules; Hidde lifts it)

Google demoted the site on 09-28 (scaled-content shape). Until Search Console shows recovery:
- **Enrichment comes first**: `python3 scripts/enrich.py --next`, `--brief <city>[+<city>...]`, `--apply` (since 2026-10-13 every city is in scope, the proven roster first; cities under six gaps travel together in one pass) (refuses a measurement or access line without a source). `--brief` first runs `scripts/register_match.py`, which copies register numbers and measurements from data/registers/ by pin and genus, so a pass only gets what needs judgement. Per tree, in order: photograph, measurements plus official register link, visiting facts, a real best_time, a recognition line. The night run may approve photographs (look at the pixels, exposure score, a geotag or filename that settles which trunk, otherwise `held`); the digest lists each approval with its reversal command.
- **No new tree unless its page is rich or a reader added it** (`enriched()` in scripts/findable.py; `check_a_new_tree_is_rich_or_a_readers()`; baseline data/rich-baseline.json).
- **Indexing**: a tree page is in Google only with a photograph (`INDEX_NEEDS_PHOTO = True` in scripts/thin_pages.py) or when it is enriched in a proven city (`RETURN_PER_BUILD` 40). Photo-less tree pages carry a googlebot-only noindex and go to sitemap-bing.xml (`GOOGLE_ONLY_WEAK_TREES`; `check_the_noindex_split_holds()`). data/noindex.json is recomputed before every build.
- Adding is not indexing: `ADD_NEEDS_FINDABLE = False` (findable.py), `PROVEN_ONLY = False`, `OPEN_FIRST` off (passcheck.py). Proven cities (data/depth-roster-frozen.json) still lead `city_queue.py --next`.
- Findable = photo, confirmed pin, or a small named site (`location_site`, at most 50 m radius, never a park or campus) plus a recognition line. The rule lives once in scripts/findable.py.
- No new place below four trees (`check_no_new_thin_places()`; frozen list data/thin-places-frozen.json). Trees into existing places beat new places. When a place grows, its intro and meta grow with it.
- No new page types or templated sets. Fallback pages (English text on a language URL) are gone and redirect (redirect-map.ts, `cityHref()` in i18n.ts). Translations continue for pages whose English twin has impressions.
- `check_index_grows_with_the_trees()` (qa.py): at most 1.5 indexable pages per tree and 80 new indexable urls per deploy. Outlives recovery mode.
- Accident guard only: `check_publishing_pace()` at 60 new trees in 24 hours. Past 10 a day, passcheck prints a depth note, never a refusal.
- Focus countries (`FOCUS_COUNTRIES` in passcheck.py): US, UK, Ireland, Japan, France, Spain, Portugal, Italy, Germany, Netherlands, Belgium, Luxembourg, Austria, Switzerland, Denmark, Norway, Sweden, Australia, Canada. Supply first where visitors are: US, UK, Germany (`SUPPLY_FOCUS`, a note). Depth is allowed on any published page.

## Supply, cheapest first

1. US pages Google already shows (top of `city_queue.py --next`). The California Big Trees register and Live Oak Society are finding aids.
2. Open an unopened ranked city that already has supply (register rows, READY leads, Wikidata candidates), to four or five trees, then move on.
3. Translate a page whose English twin earns impressions, picked by measured impressions, never fame (`python3 scripts/langcheck.py [--next]`; translate agent).
4. Famous trees (`data/leads/_famous-*.json`): `python3 scripts/famous_demand.py [--next|--gap]`; check `famous_map.py` first. A Commons category is a research list, never an import.
5. Write READY leads (`python3 scripts/leads.py`); `prepare.py` runs `scripts/refill.py` (genus from the tree's name via data/genus-names.json; widen it when READY is under 60).
6. Register-backed verify, then importing a new register.
7. From-zero web research on a city only when Hidde names the city.

Depth (photos, pins, best_time) goes only to cities DATA.md's newest entry lists under "Depth is allowed on these cities", plus the frozen roster during recovery. The `photo_hunt.py --recheck` sweep is free anywhere.

## Research: the assembly line

- **Brief**: `python3 scripts/passcheck.py --brief <place>` (never write a brief from memory). **Claim** before dispatch (data/in-flight.json, expires after 4 hours): `passcheck.py --claim <place> --kind verify|write|photo`, commit and push, then dispatch; `--release` when merged. `python3 scripts/backlog.py` checks what is live or in flight by distance, never by name.
- **Two kinds of pass, never both**: `verify` agent (Sonnet; BRIEF_RESEARCH.md; facts plus verify_notes, no prose, no photos) and `write-stories` agent (Opus; BRIEF_WRITING.md; 15 to 20 trees across cities). `photo-judge` (Opus) for viewing passes. No pass under six expected candidates.
- Log every pass in data/agent-costs.json; run `python3 scripts/retro.py` into RETRO.md. Target: 15k tokens per published tree or less.
- **Expensive work gets discussed with Hidde before it starts**: state cost and expected return. Small bounded work excepted. Usage is in tokens, never money.
- Briefs say: write findings to disk as found, ask for what ships, time-box to about forty minutes, keep rejects.
- **Keep everything**: every tree a run meets goes to data/leads/ (leads, or blocked with a one-line reason), registers to data/registers/, notes to data/research/. Unverified is a reason not to publish, never to throw away.
- Before researching a place: `grep -ri "<place>" CURATION.md archive/`. Every fetch has a hard timeout (`curl -m 20`); a host that hangs goes in data/fetch-blocklist.json.
- Burn list (no dispatch without a new angle): photo hunts on sources marked `exhausted`, from-zero city research without an owner ask, pin passes without register coordinates, aerial imagery or equivalent evidence.

**Search order**: (1) name the city's historic parks, gardens, churchyards, temple and shrine precincts, cemeteries, then search each in the local language; (2) the city's own published tree route; (3) the local newspaper's monumental-tree survey; (4) the official register (regional before national, e.g. Italy's regions over MASAF); (5) generic sweep in English and the local language; (6) cross-check (monumentaltrees.com for facts only, Atlas Obscura, park authorities).

**Register checks**: units are not what the column says; corrupt fields look plausible (a year in an age column); twins metres apart fold into one entry; register totals do not match a municipality's; a register age is at last measurement; no register knows whether a tree still stands (`scripts/lifecheck.py`).

**Selection**:
- A tree qualifies if genuinely old OR visually spectacular OR historically significant, AND publicly accessible. At every site ask which trunk is worth the visit, not which has the name; record an unnamed veteran beside a famous young tree as a lead with a coordinate. `note_a_young_tree_is_not_ancient()`.
- Walkable clusters over famous singletons: four to eight trees inside about two kilometres is a walk. `scripts/cluster_register.py`. Rank by cheapest cluster, not cheapest tree.
- Day-trip boundary: within about 30 minutes by public transport, labelled with its real place and travel time.
- Count follows the trees: floor four, ceiling is the target in data/city-queue.json, never padded, never held back for being ninth in line. When a city passes ten, titles stop saying ten.
- Alive only. A tree known dead never ships and one reported dead is checked and removed the same day; thin confirmation is stated on the page, not a reason to hold a city. Replacements reuse the id.
- At most about a third of a city behind a ticket (`check_paid_share()`, a note); fix by adding free trees. Retire with `python3 scripts/retire.py <city> <id>... --reason "why"` (moves to leads, adds the redirect, deletes photos, prints stale counts).
- A collectible point: one tree, or an ensemble only when the ensemble is the destination with one place to stand.
- Single-famous-tree places (below four) are paused during recovery.

## Verify

- Two independent sources for existence, species and age, and a placeable location; or one official register (anywhere, and the owner of the ground) plus a life check. Conflict or single source: publish flagged with a note.
- Ages: missing or approximate is fine. A derived estimate (girth and growth rate, documented planting) states its basis and stays broad; never sharpen a vague source. Never bridge a park's planting date to a tree without a source saying so. No basis: leave empty and ask the reader. Capture `girth_cm` and `height_m` whenever a source gives them (`scripts/heights.py` fills from imported registers).
- **Unknown species or field: publish and ask the reader on the page** ("Oak (Quercus sp.)"). Never for location.
- **A judgement about whether a tree is good enough never blocks publication.** The closed list of what does: the hard rules (fabrication, known dead, unlicensed photo, withheld or private location) and a location that cannot be stated honestly.
- `location_precision` set honestly on every tree. A confirmed pin needs evidence (`check_pin_upgrades()`).
- Nothing ships with none of photo, findable pin or recognition line (`check_a_tree_can_be_told_apart()`).
- Every published tree names a source (`check_every_tree_names_a_source()`); a reader may ADD a tree with none, and it waits as a lead.
- **Good reader input IS the source** (Hidde, 2026-10-12): a stranger's tree goes live with no written source when their photograph shows a tree worth the walk (Cadiz standard), their GPS fix confirmed the pin, and the account is not ours. Unknown species as the genus, short story, nothing invented. Gate: `reader_found()` in preflight (`found_by_reader.sighting_id`). A reader photo tagged to the wrong tree of ours is a new tree, not a hold (`plm_006`).
- Photo-or-pin for new trees worldwide in preflight; trees live on 2026-10-01 are in data/photo-or-pin-baseline.json.
- `note_a_reader_photograph_is_not_a_reason()`: a reader photograph alone with no age or measurement is not a reason.

## Which trees get a page

The floor is a reason somebody standing there can see: big, tall or old for its species; a one-sentence story with a source; or visible spectacle. Protected or registered is not a reason. `python3 scripts/species_size.py` scores against the species worldwide (best of girth, sourced age, height; never summed); the cut is the city's target. People are a source: two accounts within 30 m, or one contributor plus a source, or one contributor whose photo shows a visibly big tree. Scarcity is a feature.

## Stories

150 to 250 words, TONE_OF_VOICE.md, SEO_GEO_BLUEPRINT.md (P2 answer first, P3 no templating). Lead with the most surprising fact; what it witnessed. Never "hidden gem", "must-see", "breathtaking", "nestled", never em dashes. **No bridge claims**: when a sentence says two things are the same thing or one causes the other, one source must say so. **Never ask a reader to do anything that harms the tree** (peel bark, snap a twig, climb it, carve), and do not swap in a warning: just leave it out; a fact stays a fact ("its sap runs red"), never an instruction (Hidde, 2026-10-12; `check_no_invitation_to_harm_the_tree()`). Write the superlative you believe with its source; two of our pages must not claim the same crown (`python3 scripts/superlatives.py`).

**Season**: phenology per species in data/phenology/ with `intensity` (`unseen|nice|striking|worth the trip`); no calendar below 25N; no file means no calendar. `best_time` only for a real peak (flowers, fruit, autumn colour, catkins, fresh leaves, or bare silhouette for veterans whose shape is the point), one per tree, scarce. Lowest-priority depth: never research phenology from scratch in a window.

## Photos

- Open licence only (CC0, CC BY, CC BY-SA, Unsplash), attribution recorded. Never monumentaltrees.com, Google Maps, or AI imagery presented as a photo. Visible credit only where the licence requires it.
- **The Cadiz standard**: the tree fills the frame, neither distant nor a bark close-up, in leaf beats bare (tiebreaker only), daylight and colour (`python3 scripts/photo_light.py`; POOR ends a stock candidate), survives the centre card crop. **Look at the pixels before approving.** Possibly the wrong trunk: `held`. Better nothing than a random tree.
- A photograph a person sent is never refused on the light score: if it is this tree, in daylight and colour, it ships.
- Machinery: `photo_hunt.py` (API sweep into data/photo-queue.json), `photo_fetch.py --zero --out <dir> --per-tree 3`, `photo_verdicts.py`, `photo_last_resort.py`, `famous_trees.py` (research list only). Wikimedia rate-limits: about one fetch per three seconds; buckets 250/330/500/960. Every rendered image goes through `img_srcset()`.
- Filename matching decides what to look at, never what ships; a geotag settles which trunk.
- Never ask Hidde to photograph or visit anything.

## Reader input

- Submissions: Supabase `submissions` table (only with SUPABASE_SERVICE_KEY), processed ids in data/submissions-processed.json. A submission is a lead, verified to the same bar. **Never put a sender's name on the site.** Set `outcome` (`changed|holds|open_question`) and, when answerable, `reply_text` (transported by `scripts/contributor_reply.py` after mailcheck; `THANK_YOU = False`). A "could not tell which tree" report is fixed with a recognition line or trunk photo. `report detail:` rows pair with the earlier chip row; `vote undone` rows are bookkeeping. Log the exchange in `verify_notes`.
- App photographs: `scripts/sightings_inbox.py` (queue in data/sighting-queue.json, files in out/sightings/; `--judge` for Hidde's look). Check `species_match` and `description_match` yourself; doubt is a hold. A tree with a lead photo takes the reader's as `add`; `approve` when it has none; `reject` only for wrong tree, wrong subject or a bad frame. Apply with `python3 scripts/sightings_publish.py verdicts.json --send`, never by hand (`MAIL_WHEN_LIVE = False`). A sighting matching nothing is a lead in data/leads/_sightings.json. Our own photos queue as `mine`, never auto-published or credited.
- **A stranger's submission is never judged blind** (Hidde, 2026-10-13, on the Montsouris plane: "this stuff is golden"): open the photograph and read the note before lead or hold; a run that cannot view it leaves the verdict open. A note with a story is the start of the page, not a reason to wait. Then look for the trunk in the city's own tree inventory. `check_a_reader_verdict_looked_at_the_photograph()`.
- A reader's GPS fix within 300 m replaces an approximate pin automatically (`move_pin()`, records `pin_source`); never touches a confirmed pin.
- `check_every_submission_got_a_verdict()`. A reader's added tree going live earns one congratulation mail (`python3 scripts/tree_approved.py --send`).

## Registers (layer 2)

Official designated-remarkable trees only, never full inventories, as honestly labelled dots with no own pages. Licence first, compatible with commercial reuse, proving sentence recorded in OPEN_DATA_SURVEY.md; re-read a licence verdict that blocks a country (the NL register is CC with attribution). Coordinates default to approximate. In a country with 100+ trees a new tree needs a photo or confirmed pin, US exempt (`check_covered_countries_want_a_photo_or_a_pin()`). Tier/game design is parked.

## Ambassadors

komoot Pioneer convention: one person, one place, a badge. Most come from outreach (drafts/OUTREACH.md), not the app. `python3 scripts/ambassador.py`: `--invite-scan --send` (one invitation per person and place, signed Ancient Trees, never as Hidde), `--grant` only after their answer, `--public` for the separate consent to be named, `--grant-named`, `--link-address`, `--sync`, `--requests --send`, `--asked`, `--heads-up --send`. An organisation beside a name needs their explicit yes. Visitors are asked for their hometown. Apple relay bounces: check the Sign in with Apple email registration first. No other automatic mails.

## Privacy and accounts

- **People's addresses never live in the repository** (it is public): outreach files sync through the `private_files` table with `python3 scripts/private_store.py sync|pull|push`; a run that cannot pull sends nothing. `check_people_s_addresses_stay_out_of_the_repo()`.
- **The server decides who is signed in; nothing a person does is kept on the device** (hard rule 11). Every gate goes through `atCollection.gate` (web) or a server refresh (app). Checks: `check_a_stored_session_is_verified_with_the_server()`, `check_every_gate_asks_the_server()`, `check_nothing_is_stored_locally()`, `stale_session_is_refused()`, `signed_out_controls_ask()`, `every_button_asks_or_does_nothing()`, SignedOutWalk.swift, `scripts/crossdevice.py` with data/cross-device.json, `scripts/gatecheck.py`. A new account control joins `signed_out_controls_ask()` in the same change.
- Postbox needs an account: supabase/postbox-needs-an-account.sql, watched by postbox.yml.

## How to work

- **Distribution first**: before doing work, say what will bring anyone to it (demand via `scripts/demand.py` plus a reason we can rank). Depth goes to pages with impressions. Measure in impressions and clicks, not trees.
- **Ship rough, ship wide, fix later.** Cuttable: precision (if labelled), age, photo coverage, completeness, polish, extra sources. Never cuttable: fabrication, faked precision, unlicensed photos, promising what is not there, withheld or private locations. **Location is the one field that carries the product**; 95 percent is the shipping standard elsewhere.
- Deciding without a rule: does it serve goal 1 or 2; can Hidde undo it; can it hurt anyone else (overrides). If the first two pass and the third is clear, do it without asking and log it.
- Hidde's incoming thoughts: check the corpus, name in one line what it touches or contradicts, then build, park or push back. He outranks the corpus; a contradiction is said out loud.
- Two triggers: after about three exchanges on a detail, name in one sentence what it does for the goals; when Hidde corrects something, record it before the next reply as a check first, a read file second, a memory note last. A lesson seen on two days becomes a build check.
- Search evidence is a run's to act on: build or retarget a page for a real Search Console query within an existing contract. Check the built site first; a query matching an existing page is a ranking problem.
- Walk the user's timeline before building anything that accumulates: first minute, day seven and thirty, second device, the gap, the failure.
- **Merge your own work**: verify, merge to main, push, log it as live. Never hand Hidde git plumbing (`scripts/handoffcheck.py`). FOR HIDDE is only for what genuinely needs him.
- LOG.md is his catch-up channel: lead with what changed in the product, keep breakage separate, say plainly when a run did nothing useful.

**Design-time checks (one line each, not phases):**
- **Convention check**: for a new interaction, grep CONVENTIONS.md's `^## ` headings and read only the matching entry (never the whole 200 KB file), else look up how AllTrails, Google Maps, Airbnb, PictureThis, komoot do it, and copy it. Use official assets (Apple, Google sign-in). Never invent a control. `scripts/conventioncheck.py` (new Screens/ or components/ files name a reference).
- **Whole-page check**: what does this displace or duplicate, and how does a visitor arrive here (qa fails orphan pages).
- **Trio**: Product, UX (375px, honest), Tech (boring, reversible).
- **Both surfaces by default**: a feature ships on web and app in the same change. A decision travels as data in the feed, never as a rule implemented twice (answers in the feed, rules on the server). `scripts/crosscheck.py`, `scripts/paritycheck.py` (data/parity-allow.json, data/cross-surface-allow.json), `check_faces_travel_to_the_app()`.
- **Every language**: strings in `UIStrings` (site/src/lib/i18n.ts) for es/it/nl/de/pt/fr/ja. `check_translated_components_have_no_typed_text()`, `check_overlay_coverage()`, `check_every_language_gets_the_same_controls()` (open gaps in data/lang-gaps.json).
- **One sheet for every overlay**: BrandSheet (app) / Sheet.astro (web); news is the snackbar. `scripts/sheetcheck.py`, data/sheet-allow.json.
- **Copy layers**: product strings follow PRODUCT_COPY.md (`scripts/copycheck.py`); pitch copy follows drafts/PITCH_VOICE.md (`scripts/pitchcheck.py`); his mail voice drafts/HIS_VOICE.md (`scripts/mailcheck.py`). Public copy never narrates our process. **Copy-check your own copy before showing it** (Hidde, 2026-10-13): grammar, tense, repeated words or thanks, and every claim true of the product (an ask the reader cannot do is false); the scripts catch rules, not this.

## QA

1. Build checks (Astro build refuses contract violations) and `scripts/qa.py` plus preflight.py on every push; enable hooks with `git config core.hooksPath scripts/hooks`.
2. Smoke test (smoke.yml): pages execute, 375px fit, BAND alignment, signed-out controls.
3. Fresh-eyes reviewer (review.yml) daily into REVIEW.md, app screenshots rotated; Monday corpus audit.
4. **Eyes rule**: a session looks at every changed user-facing element rendered, at 375px and desktop, before calling it done. Composition walk every two weeks.
- App: `scripts/appsweep.py` (every screen, SE and large phone, every installed iOS runtime; `--check-lists`), `scripts/appfit.py`, `scripts/appwalk.py` (FlowWalk), StressWalk, `scripts/refused.py`, Faults.swift (`-fault=offline|slow|server|expired|garbage`), `scripts/netcheck.py` (all network through Kit/Net.swift), UpgradeTests, LiveFeedContract.swift and `scripts/feedshape.py`. ios.yml is on health.py's watched list. App work in a git worktree (`scripts/worktree_guard.py`). For the app only, push before the sweep so Hidde can walk it in parallel; the sweep still runs and is reported.
- Ratchet checks in qa.py also include: `check_auth_corpus_agreement()` (reads hard rule 1 below), `check_no_strategy_in_workflows()` (workflow prompts carry mechanics, not strategy), `check_inline_scripts_parse()`, `check_the_session_is_known_before_anything_asks()`, `check_the_digest_never_shows_bots()`, `check_park_words_match()` (preflight), checkParkCountPromises (count-promises.ts).

## Learning loop

Other machinery: `scripts/brief.py` (session-start brief, names broken gates), `scripts/stats.py`, `scripts/daily_digest.py`, `scripts/smoke_test.py`, `scripts/layout_rules.py` (shared thresholds), `scripts/archive_logs.py` (moves LOG.md and CURATION.md entries older than three days to archive/, daily from data-digest.yml), `scripts/outreach_send.py`, hooks `convention_nudge.py`, `pitch_nudge.py`, `ratchet_nudge.py` in scripts/hooks/. data/ambassadors.json, data/copy-tests.json, data/city-list.json.

Before a brief: `passcheck.py`. Log costs. `retro.py` daily. Copy tests: `scripts/seolearn.py` (paused in the digest, see Digest reports) and `scripts/copytest.py --tick` (one test per surface, no early verdicts, head phrase never varies, promotion is a data change). Starting a copy test is a run's call (blueprint v1.17); new page types, contracts, schema or link minima still need Hidde.

## Digest reports

Always tables, at most two sentences of reading. In order: **the trees strangers sent that Hidde has not inspected** (`reader_trees_to_inspect()`, Hidde 2026-10-13; listed until he answers with `judgement.py --feedback`; a session presenting the digest runs `python3 scripts/inspect_readers.py` and opens the page with photographs and their words in the preview (`preview_start {name: "inspect"}`; recreate preview/serve_inspect.py from the script docstring if /private/tmp was cleared), which never go in the public DATA.md), what readers gave that went live (`readers_gave_section()`), search window day by day for 7 days with totals, product funnel, signups (waitlist, accounts, saves, submissions split into tree/city versus feedback/correction), what was decided on submissions (`judgement_lines()`), our own search terms (zero-result terms are requests), site visits from Cloudflare (bucketed to tens, no bots ever, no bot column), Google Analytics beside it (`ga_section()`, scripts/ga_report.py; only visitors who accepted the cookie bar, so a sample, not the count), the night shift over the last 24 hours with cities touched, app events (PostHog), App Store first-time downloads (`scripts/asc_downloads.py`) plus a source table (`split_by_source()`), Bing (`scripts/bing_search.py`). Tiny volumes are said plainly, never narrated as trends. **Paused until Google comes back** (Hidde, 2026-10-12): winning and losing pages, the grouping-pages table (`grouped_pages_lines()`) and seolearn's what-converts pass (`GOOGLE_DETAIL = False` in scripts/daily_digest.py); set True when Search Console recovers.

## Place names

Publish in English (Florence, Naples, Turin, Padua); addresses and register names keep local spelling. No archaic exonyms (Livorno, not Leghorn). Pairs in data/city-aliases.json. A renamed live city adds its old slug to `RENAMED_CITY_SLUGS` in site/src/lib/redirect-map.ts.

## The hard list

1. **Accounts: OPENED** by Hidde on 2026-08-14. We store an email address and saves, nothing else; any new personal-data column or table needs his yes; deletion keeps working end to end; no personal data renders on the site.
2. No taking payments or setting prices. The paywall line he set (DECISIONS.md 2026-08-18: €19.95 a year, 7-day trial, Season Radar alerts, walks, personal log, offline) is not shown on the website until he says so.
3. Nothing irreversible in public: no retiring indexed URLs without a redirect, no deleting data, no force-push, no giving up a domain.
4. Never speak as Hidde or contact anyone as him. Drafts only; automated mails are signed Ancient Trees.
5. No new dependency or third-party service in the product without his yes. Gear for us (free, read-only, never touching reader data or the built site) a run may adopt and log. No accounts created, terms accepted or logins as him.
Also his alone: SEO_GEO_BLUEPRINT.md, TONE_OF_VOICE.md, the brand.

## Hard rules

1. Never use content, photos or text from monumentaltrees.com beyond fact verification.
2. Never fabricate tree facts. A wrong location kills trust permanently.
3. Never use em dashes anywhere.
4. Photos need verified open licences with attribution recorded.
5. No spending without Hidde's explicit approval, ever.
6. Revenue over beauty: before features ahead of validation, ask "Have we validated that real people will pay for this?"
7. Never ship a page that does not conform to SEO_GEO_BLUEPRINT.md; changing that document needs Hidde and a version bump.
8. Superlatives: write what you believe, say where the number comes from; two of our pages never claim the same crown.
9. One canonical common name per species, nationality-neutral, matching other cities (Pedunculate Oak, London Plane).
10. Public trees only, never a location its source withholds. Ships when: no one's permission is needed to get in (paid entry and bookable tours count as yes; a doorbell or reception desk does not), `access` says honestly what they will meet, and it is not somebody's home. View-only trees ship with the pin on the viewing place. Schools only with evidence the grounds are open. Churchyards and temple precincts yes; enclosed convents, cloisters and institutions no unless a source says otherwise.
11. **Nothing a person does is saved on the device, and the device never decides who is signed in.** The device may hold only what data/cross-device.json marks `device` (session token, pending intent, unsent drafts, device settings). See "Privacy and accounts".
