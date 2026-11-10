# LOG


**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-11](archive/LOG-2026-11.md)
- [2026-10](archive/LOG-2026-10.md)
- [2026-09](archive/LOG-2026-09.md)
- [2026-08](archive/LOG-2026-08.md)
- [2026-07](archive/LOG-2026-07.md)

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-11](archive/LOG-2026-11.md)
- [2026-10](archive/LOG-2026-10.md)
- [2026-09](archive/LOG-2026-09.md)
- [2026-08](archive/LOG-2026-08.md)
- [2026-07](archive/LOG-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
<!-- archive-index -->
## 2026-11-10 session: compliance audit, privacy page and terms brought up to date, weekly compliance light

- Privacy page rewritten to what the product does: every account has a profile, public unless switched off, and what a public profile shows (Collected and Want to go included); notes on trees and the "new from visitors" row are public with a public profile's name; shared links; suggested people. Added what GDPR article 13 requires and the page lacked: who decides, why we may use each kind of data, how long we keep it, who handles it (Supabase, PostHog, Google, Apple, Resend, ImprovMX, GitHub, OpenFreeMap), rights and the Autoriteit Persoonsgegevens, 16 and over.
- Terms: 16 and over, profiles public by default, notes public, a name beside a photo in the visitors row; the false "nothing beside it says who took it, ever" and "your collection is shown to nobody" are gone.
- Photo credits on the website: the photographer's name links to the source page (Commons, iNaturalist, Geograph, or attribution_url) and the licence label to its deed (CreditLine.astro). CC 2.0 and 3.0 give no grace period for a missing link, which is what claim agencies invoice.
- First outreach mails must end with a way to say no: mailcheck refuses one without it, and OUTREACH_STRATEGY.md says so. The batches of 11-01 to 11-06 had none.
- So this stops depending on Hidde asking: scripts/privacycheck.py on every push (a new table needs its privacy sentence), a weekly compliance review in review.yml (BRIEF_COMPLIANCE.md), and a compliance part in the Next version light of Web and iOS (quality.py). The light is orange now, on purpose: six points wait for Hidde in data/compliance.json.
- For Hidde: compliance, 6 points wait for your word (data/compliance.json): the 33 accounts made public on 10-29, public by default at sign-up, your full name or KvK on the privacy page, PostHog without consent, mailed photos live before the yes, mail sentences quoted without asking.

## 2026-11-10 session: Android, the map opens where you are

- **New in `android/` (PR 13):** location asked on the first open with no screen of ours before it; a "Location off · Use my location" chip while it is off (Settings after a refusal); a my-location button above the sheet; a bottom sheet listing the trees in view with the count (the website's treesInView), nearest first with distance in km or miles by region, as iOS and web write it. Strings in eight languages. New: androidx material-icons-extended (AndroidX); location through MapLibre's engine on Android's own location, no Play services.
- **Verified:** android.yml green, 18 unit tests (distance, units, the list, the feed contract, pin numbers).
- **Not verified:** nothing on a device or emulator yet.
- **Next Android session:** species shapes in the pins, the same-spot stack, brand font; then walks, sign-in, collect, season.

## 2026-11-10 session: Highlights cards light their pin; Lindenbaum U-Bahn claim softened

- City page, desktop: pointing at a Highlights photo card now lights its pin, as the list cards below already did (Airbnb's list). Paired by tree id. The explore map has no card-to-pin hover at all yet (its pins are map layers); not done.
- Frankfurt, Eschersheimer Linde: the U-Bahn bend rests on one unreferenced de.wikipedia sentence, frankfurt.de is silent. Story, FAQ, transport, recognition line, intro and meta (EN and DE) now say "by local account" or name the station instead; "under Eschersheimer Landstrasse" is gone. verify_notes records why.

## 2026-11-10 night run (07:37 UTC): nothing shipped

- Rung 1 empty (no photographs or notes waiting). health.py: live site behind main, only 6 of 12 knocks delivered; dispatched a deploy at the end. Writable pile is 10 weak leads (Tucson campus accessions, a Vienna register pair), so refill: San Francisco verify pass (sixth on that register) found 0 new trees; all nine unmined rows were already judged. Wall set for 48h. Phoenix scouting retry was already retried 2026-11-04 (not importable), so nothing new there. pagegaps lists only species, park and Thailand pages, which STRICT_CUT and the trim keep out of Google, so skipped.
- For the next run: the unmined-lead pile needs sources (930 leads), but no machine fills that; the 28 held trees go through the daily publish.

## 2026-11-09 daily publish (scheduled task): 25 trees into the app

- **What went on main (c6b78d493), app only under APP FIRST, no web page or place page:** Cincinnati 8, St. Louis 6, Indianapolis +3 (ind_002 to 004), Lexington (Kentucky) 2, Huntsville (Alabama) 2, Birmingham (Alabama) 1, Brighton +3 (bhm_007 to 009). None has a photograph yet. Preflight 0 problems; the 25 is this task's own limit, the pace counts nothing while APP FIRST holds. Done from a worktree on the newest main, because the shared checkout was 62 commits behind.
- **Not checked live yet:** three deploys in a row were cancelled by newer pushes from other sessions (42685153978, 42685786418). Before any deploy carrying them: /brighton 200, /cincinnati 404, as APP FIRST wants. The 25 still need to be seen in /api/cards.json after the next deploy that finishes.
- **Copy changed:** build_us_empty_cities.py writes "Four remarkable trees" into Indianapolis's meta and makes ind_002 the hero; preflight refused the count (the web shows only the Kile Oak). Meta now names no number, the hero stays ind_001, intro and FAQ keep the builder's four-tree text for the app. Indianapolis has no web place page at one web tree. When its trees get pages, the meta and hero can follow.
- **Still waits, 28 trees, about two days at 25 a day:** build_uk_under_ten.py: Eastham Yew (Liverpool), Bute Park Tulip Tree (Cardiff), Windsor's two; build_source_led_2026_11_09.py: Cleveland 5, Ann Arbor 3, Lansing 2, Sacramento 2, Santa Cruz 2, ten south-east England yews. The earlier "queue empty" no longer holds, so the daily task stays on. No claims stood on today's places.

## 2026-11-09, six source-led runs: 25 trees written and held for the app

Written and waiting for the daily publish: Cleveland 5, Ann Arbor 3, Lansing 2 (East Lansing), Sacramento 2, Santa Cruz 2, ten churchyard yews in Surrey, Sussex and Hampshire, and a second Windsor tree (`python3 scripts/build_source_led_2026_11_09.py`; Windsor through build_uk_under_ten.py). Tested with city_names and preflight, 0 problems, reverted.

Held: Detroit's two Elmwood Cemetery trees (no pin; tour maps are image-only PDFs), Kansas City's Vaile smoketree (cannot be told apart, access unclear). Reno, Boise and Des Moines gave nothing placeable. Long Beach's figs are already live as lax_016, marked hold.

What paid: the Ancient Yew Group's find-a-yew table by county with its site-file PDFs (about 30 more 7 m+ leads with coordinates in data/research/southeast-england-yews-notes-2026-11-09.md). What did not: state champion lists alone; most rows are private land or carry no location. Transport lines on the UK yews give straight-line distances worked out from the pins, not sourced routes; US lines say routes were not checked. About 1.3M tokens, about 52k a tree.


## 2026-11-09, Manchester: one more pass, nothing that ships

Manchester stays at 5 trees. Every Tree Register record for the area names the Woodland Trust's Ancient Tree Inventory as recorder, which is closed to us, and none is a Manchester park tree. manchester.gov.uk answers 403, so the council's rare-trees list keeps its one source and no coordinates. Rejects in data/leads/manchester.json. No further pass without someone opening the council pages in a real browser. About 119k tokens.


## 2026-11-09 Six empty top-60 US cities: 22 trees written and held in the builder

22 trees verified and written, nothing published yet: Cincinnati 8 (all Spring Grove champions), St. Louis 6 (Tower Grove Park, Bellefontaine, Missouri Botanical Garden, 2 of 6 ticketed), Indianapolis +3 to 4 (Temple Oak, Nowland Oak, Statehouse Moon Tree), Lexington, Kentucky 2, Huntsville, Alabama 2, Birmingham, Alabama 1. The bar of ten was not reached anywhere: supply ran out and nothing was padded. Slugs carry the state where the name is shared (birmingham-alabama, huntsville-alabama, lexington-kentucky). `python3 scripts/build_us_empty_cities.py` puts them in data/cities (`--only` for a slice); then city_names.py, preflight.py. Tested on main: preflight 0 problems, no new shared crown, test files reverted.

Negatives: Birmingham has no named old trees online beyond the hawthorn (Bham Now says as much); Lexington's famous bur oaks are dead; Crown Hill's and Lexington Cemetery's tree-map PDFs were read by OCR and hold species walks, no sizes. Bellefontaine's elm (stl_001) was last reported standing in February 2025, and its story says so. Huntsville's Hays pins are preserve-level. About 1.21M tokens, 55k a tree.


## 2026-11-09, UK under ten: six more trees written and held, one verified file rescued

Six trees verified on 11-04 are written and wait for the daily publish (app only): Brighton's Tabletop Elm, Den Haag Elm and Patcham Peace Yew, the Eastham Yew for Liverpool, the Nursery Lawn Tulip Tree in Cardiff, and the Signing Oak as Windsor's first tree. `python3 scripts/build_uk_under_ten.py`, tested with city_names and preflight (0 problems), reverted. Four more Cardiff trees from the same verify pass went live with the 11-06 night run.

Count on main with the held trees: Glasgow 10, Cardiff 13, Brighton 9, Liverpool 4, York 6, Manchester 5, Stratford 2, Windsor 1. York and Stratford found nothing that ships on one pass each; Manchester was walled and not retried. Honest supply ran out here; the next angle is a browser on the Tree Register's county champion lists.

Breakage: the 11-06 night run overwrote data/research/brighton-verified.json with an empty list while the three Brighton trees sat uncommitted in it; recovered from the agent transcript into brighton-verified-2.json. Windsor's Tree Register oaks stay leads, because those records say they were copied from the Woodland Trust inventory. city_names.py matched Windsor to Legoland; data/city-aliases.json now names it Windsor.


## 2026-11-09 session: Northern Ireland and Highlands run, the bookkeeping

**What changed in the product:** nothing new today. The 19 trees of this run are already live: 16 app-only in the 2026-11-06 publish (311725714), plus Belfast's three (bfs_006 to 008). Castlewellan 4, Ardkinglas 2, one each at Florence Court, Crom, the Dark Hedges, Rostrevor, Armagh, Gosford, Reelig Glen, Inverness, Glen Affric and Benmore. Six have a photograph.
**Found empty:** Aviemore, Rothiemurchus and all of Speyside: no named, placeable tree (three leads in data/leads/aviemore.json; a granny pine needs a geotagged photo of the trunk or an OSM node). Beauly Priory's elm fell on 2023-01-05. Fort William, Oban, the Great Glen, Dornoch and the Black Isle gave nothing individual. Mount Stewart, Castle Ward and Tollymore stayed leads; the Forest Service book "Northern Ireland's Remarkable Trees" (Wayback copy of remarkabletrees.org) is the angle left for them.
**Waiting in data/research/uk-ni-highlands-places.json:** Belfast's rewritten place copy, unused while its new trees are app-only. Use it when they get pages.
**Cost:** about 1.15M tokens for 19 trees, about 60k a tree, far over the 15k target; from-zero work in the Highlands costs that and yields little. The writing pass died on the usage limit at its last step, with everything already on disk.
## 2026-11-09 session: US Southwest run closed (31 trees, live in the app since 11-05)

- **What changed in the product:** nothing new today. The daily publish of 2026-11-05 (b7345d923) already took this run's trees into the app, and a night run added the last three Tucson trees on 11-07 (c137f38ce). Tucson 14, Boulder 5, Santa Fe 3, Prescott 3, and one each in Scottsdale, Glendale, Albuquerque, Denver, Flagstaff, Sedona: 31 trees, two with a photograph so far (tus_002, bld_003). Today only the paperwork reached main: leads, notes, the register verdict and the costs.
- **Arizona's Magnificent Trees is not importable:** the report we could read (2022, mirrored at air.arizona.edu) is a booklet of 23 highlights with no licence, no coordinates and no full list; dffm.az.gov still answers 403. Finding aid only.
- **What yielded:** the University of Arizona arboretum's GIS (heritage and champion flags, per-tree points) and the City of Boulder's notable-tree story map. Both are worth looking for elsewhere: a campus or city GIS beats from-zero search.
- **What did not:** Phoenix proper 0, Tubac and Tumacacori 0, Denver 1 (Fairmount's PDF is a numbered map with no key), Albuquerque 1. Salt Lake City was not touched, as asked. These cities stay under the ten-tree bar of 2026-11-04 and another from-zero pass should not run without a new angle; leads are in data/leads/.
- **Holds overruled:** the writing pass held tus_007, tus_013 and tus_014 (young, no visible reason); the night run of 11-07 wrote and merged them anyway, which fits "a judgement about good enough never blocks publication".
- **Breakage:** the writing pass died on the weekly usage limit on 11-04 after saving all its work, so its token count is unknown and it is not in agent-costs.json. Verification cost 1,166,027 tokens for 31 trees, about 38k a tree before writing, more than twice the 15k target. The six claims expired unreleased; none remain.

## 2026-11-09 session: the Plus question starts counting at zero

The three answers so far and the one "tell me" (Rome web was our own account, the two app answers could not be told apart from a test) are left out of `plus_answers.py` and the digest, Hidde: "haal deze uit de telling". They stay in the database; the list is data/plus-answers-not-counted.json, by created_at. The first real answer now reads as answer 1.

## 2026-11-09 session: two small fixes before the Guardian piece

**What changed in the product.** The list beside the explore map fetches its photographs at once instead of after the map's last street tile, so a slow phone or a busy tile host no longer leaves grey Highlights. Readers' photographs on our own domain got 500 and 1000 px copies (47 trees, 48 missing files of each kind together 96 written, manifest rebuilt): the homepage's New from visitors row was loading masters of up to 1 MB for a 180 px tile. Hidde: "Ja, fix ze".

**Spike check, nothing else needed changing.** Live pages, map, rollback and the hourly check are fine; a first explore visit is about 1 MB compressed. No real load test, on purpose: it would test GitHub's and OpenFreeMap's servers, not ours, and risks being throttled just before the piece. Not verified: OpenFreeMap's and Supabase's limits under load. A blank map in the app's browser pane is the hidden pane (it pauses drawing), not the site.

## 2026-11-09 session: /cities no longer lists places under four trees

Hidde: "alles onder 'places with fewer than four trees' mag wat mij betreft weg." The section, its counts and its styles are gone from /cities (it was only on the English page). Those places keep their map pin, search entry, country-page row and page. The grid of cities is unchanged.

## 2026-11-09 session: Barcelona, the Sot de l'Estany is closed

The Amics del Jardí Botànic wrote that the Sot de l'Estany has been shut since the July landslides, reopening unconfirmed for January 2028, and the Sot de la Masia stays open. The access line of the four trees they named (wingnut, green ash, narrow-leaved ash, sycamore) now opens with that, as does the hornbeam's, which stands in the same Sot though they did not name it; the city FAQ answer says so too. When it reopens, take the closure sentences out of access (verify_notes on each says so). Reply drafted, not sent: drafts/reply-pere-vives-2026-11-09.md.

## 2026-11-09 session: Discover's ambassador row

**App, in the next build (42):** the ambassador row on Discover opens again. On build 41 a tap reached the button and the sheet was asked for, but iOS never showed it: Discover's outer LazyVStack had thrown the row away and rebuilt it. Logged on Hidde's iPhone, confirmed fixed there with a VStack ("hij doet t nu wel"). Build 41 in the store still has the bug.

**Same pattern elsewhere:** a scan of every sheet in the app found one more, the share row on Find people; its three sheets now hang on the list, not the row (simulator: the row opens its sheet). The scan reads code only and looks for this one pattern.

**Testing gap:** no simulator walk showed it (Debug and Release, real test account, moving GPS, reopening). The earlier "confirmed on build 41" closure of 2026-11-09 was too early.

## 2026-11-09 session: the Mozart-Platane leads with Hannah Mayr's photograph

Vienna vie_005: her photograph (sent by mail, permission to use with her name) is the lead, GuentherZ's Commons photo moved to the strip. She has no account on the address we wrote to, so it is credited by name with `source: mail`, not linked as a contributor. The page counts as unique to us (`unique_photo()`). Her reply is drafted in drafts/reply-hannah-mayr-2026-11-09.md, waiting for his yes.

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-11](archive/LOG-2026-11.md)
- [2026-10](archive/LOG-2026-10.md)
- [2026-09](archive/LOG-2026-09.md)
- [2026-08](archive/LOG-2026-08.md)
- [2026-07](archive/LOG-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
## 2026-11-09, session: nearest stop and walking time off every page and app

**Product:** the transport line is gone from tree pages in all languages and, through the feed, from every installed iOS and Android build. Take me there stays as the route. The data stays in data/cities/; undo is two lines. Blueprint v1.27 (Hidde: "Ja, haal ze weg").

## 2026-11-09, session: three Munich trees corrected after a local expert's review

**Product:** the Krüner Eiche now says about 250 to 300 years (was about 600, against the 250 in a source we already cited), the Röth-Linde around 450 and a Nationalerbe tree since 14 October, the Englischer Garten beech 230 to 300 and no longer "older than the park". Stops corrected (Westpark, Westfriedhof, Studentenstadt), English and German, plus the Munich intro, FAQ and the oak collection note.

**Found:** the transport lines are outside verification and two of two checked were wrong; 98% of trees carry one. Hidde is weighing whether to keep them at all (SEO_GEO_BLUEPRINT.md names transport in the page body, so that is his edit). No platform error rate has been measured.

## 2026-11-08 session: Android, first working slice

- **New in `android/`:** native Kotlin and Compose app on MapLibre. Reads the same feeds as the iPhone with the iPhone's bundled catalogue as floor (read from ios/.../Data, no second copy); map with pins and dots under the Airbnb rule; a tapped tree's card, then its page with story, credit, Take me there, Getting there; strings in eight languages. New product dependency beyond AndroidX and Compose: only MapLibre. Images and JSON use what Android ships.
- **Verified:** android.yml (changes under android/ only) builds the app and passes the unit tests on Linux, including the app's parser against the live feeds and the pin numbers against lib/map.ts.
- **Not verified:** nothing has run on a device or emulator, so the look, taps, and loading the 11.5 MB catalogue on a cheap phone are unknown.
- **Gaps for the next sessions:** location and trees near me (the map opens on Europe), species shapes in the pins, the same-spot stack (one spot, two trees), brand font, walks, sign-in, collect, season, Play Store. No gradlew or wrapper jar committed; CI installs Gradle 8.14.3.
- **For Hidde:** Android Studio only when asked for the first look; Play account and closed test stay his.


## 2026-11-09, 07:00 window (night run)

- Rung 1 clear. Rung 2: the same two open app BUG rows (Discover ambassador seat, map pin blink), still needing the Mac and simulator; left open. Health also wants a deploy dispatch (main is ahead of the live build).
- Shelf under the write floor. Refill: San Francisco verify pass, 0 new trees (nine unmined rows already judged; Big Trees champion `ca-bigtrees-442` has no second source, stays a lead). Wall. The SF claim stays until sfo_012, 014, 015 are written.
- Scouting RETRY, Hallstatt: fetched the Upper Austria Naturdenkmaeler INSPIRE GML (446 polygon sites, names and Bescheid dates, no species or measurements). It names real trees near Hallstatt, Bad Goisern and Bad Ischl (yews, a thousand-year lime, lime groups). Then imported the same window: licence line (CC BY 4.0, read from data.europa.eu) in OPEN_DATA_SURVEY.md, `scripts/import_ooe_naturdenkmaeler.py` (UTM33 to WGS84 checked against two known yews), `data/registers/ooe-naturdenkmaeler.json` (349 tree-named sites, `publish_dots` False, centroids approximate). Hallstatt already publishes its headline monuments, so the yield is for unmapped Upper Austria places (Linz, Steyr, Wels). The deploy dispatch was refused (HTTP 403, token cannot dispatch workflows), so main stays ahead of the live build until the next push-triggered or scheduled build.
- For Hidde: nothing needing him.

## 2026-11-09, 01:22 window (night run)

- Rung 1 clear (no photographs, no notes). Rung 2: fixed two web error types from old browsers (Safari before 14 `matchMedia.addListener`, browsers without `<dialog>.showModal`); invisible change, commit 303f6bab9. Not built or smoke-run here (no site build in this runner).
- Open app BUG rows (Discover ambassador seat ignores a tap; map pins blink after fresh install) need a Mac to reproduce and test; left open, not guessed at.
- Shelf: the writable pile is about 21 trees across scattered places plus one READY lead (Segovia). Braga claimed and released at once (5 leads, under the six minimum), so it is a 48h wall. Vienna verify pass: 2 trees (Prater oak vie_060, Heustadelwasser lime vie_061, access flagged), 4 leads. The claim stays until the two are written; release is refused until they are merged.
- Health also asks for a deploy dispatch and a nightly knock (GitHub dropped 6 of 12 crons).
- For Hidde: nothing needing him.

## 2026-11-08 (window from 18:55 UTC): nothing new published

Rung 1 empty (no sightings, no notes). Rung 2: health shows two open app BUG rows found by Hidde (the Discover ambassador seat ignoring a tap, map pins blinking on a fresh install). Both are Swift UI bugs that need the simulator and a UI test, which this Linux runner cannot run, so I left them open. For Hidde: both still need a session on the Mac.
The writable shelf is empty: the only unwritten trees sit in files with fewer than six candidates, and the rest of the "awaiting a writer" list is stale files. I claimed Guimaraes for a verify pass. It verified 0 trees, because every register row is already live, a lead or blocked. The Moreira de Conegos stone pine is real but has no evidence of public access. Guimaraes is a wall for 48h.

## 2026-11-08 night run (window from 16:29 UTC)

- **Porto gets the three protected trees of Quinta de Villar d'Allen** (write pass, scripts/build_write_2026_11_08b.py, app-only under APP FIRST): por_032 the 40-metre bunya pine, por_033 the blue Atlas cedar with a 20-metre crown three metres from it, por_034 the Japanese umbrella pine with a register girth of 3.15 m about 20 m away. Each story leads with its own fact so the three do not read as one template; ages carried as the register's ~150 with a 120 to 180 band, nothing bridged from the 1839 estate date. Access line rewritten from the cited council page ("Visitas guiadas aos jardins: mediante marcação prévia", listed for visitors), since preflight read the bare "by prior appointment" as permission; hard rule 10 counts a bookable tour as yes. No best_time (all three evergreen). Porto 32 trees. Preflight 0 problems. An earlier attempt at this pass stopped early with no story written; this one finished it, and also commits that attempt's uncommitted verify output (porto-verified.json, the leads file).
- **Salt Lake City reaches its target of 20** (rung 5, US first): wrote and merged slc_019 (Lavalle hawthorn) and slc_020 (red horse chestnut), both on the University of Utah campus beside the champion cork oak, ash and zelkova. Both are app-only under APP FIRST. Preflight 0 problems.
- Rungs 1 and 3 empty (no reader photos or notes waiting). Rung 2: health.py shows the two open app bugs found by people on 11-08 (ambassador seat, pin blink). Their fixes are on the merged QA branch, and only a Mac or iOS CI run can close the rows, so I left them open. The iOS app workflow's scheduled failures need a session to read the run logs.
- **Segovia scouted** (scout_next target): premise was off, the city already has 6 trees and its Castilla y León register is imported. One new lead (El Espinar sequoia, AS-SG-22, access unconfirmed), verdict `imported` in data/register-scouting.json.
- **For Hidde:** seg_003 (Andromeda parterre sequoia, AS-SG-09) is published, but our own blocked lead says a 2020 news report has Patrimonio Nacional felling "the Andromeda sequoia". A second search today found no such report and says four sequoias stand in that parterre, so it is unsettled which one went. Left published; a session should settle it with a dated photo or Patrimonio Nacional.
- The shelf has no writable pile left (0 READY leads). The remaining verified files are mostly stale, as passcheck says.
- **Three trees in, app-only under APP FIRST** (write pass, scripts/build_write_2026_11_08.py): gui_009 the stone pine on the acropolis of the Citania de Briteiros (Guimaraes, 9 trees), hnl_024 the Waikiki Aquarium banyan (Oahu, 32; its hold lifted under hard rule 10, since inside or outside the ticketed aquarium anyone can reach it, and the access line now says so), and the Penacova wisteria pergola as a new one-tree place, penacova/pcv_001 (was cbr_007, outside Coimbra's day-trip bound). Preflight 0 problems.
- Still held, each for its earlier pass's reason, which still stands: asp_001/002, ssb_002/003, cbu_001 (register points in forest, no tell), dmr_002 (no sighting since 2019), ftw_024/026 (no tell), frk_027 and inn_007 (schoolyard and private yard), brd_001 and cdl_001 (hospital and kindergarten courtyards), not_002/003 and sgz_005 (access unknown), tmt_001 (register group), sfo_012 (duplicate of sfo_004, fold in), sgz_003 (its access line still reads as a booking that needs permission; ships once a source says the Ocuri tours are open to anyone). The Segovia El Espinar sequoia lead is not verified (six similar trunks, access and life open), so it was not written.

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
## 2026-11-08 session: build 41 archived

- **In the Organizer, 1.0.4 (41), from 4a8884293 with ios.yml green on that commit** (run 42484867118) and the catalogue refreshed to 4,690 trees and 407 walks. Carries branch claude/gifted-cerf-cbp95i (merged to main) and New from visitors' name at 44 points to tap (the iOS 18 floor's last SMALL; appfit 0 findings on the SE, iOS 18). The floor job does not run on a push, so it is first read on the next schedule.
- **Not seen rendered:** the New from visitors row after that fix, it sits below the fold on the SE. Asked of Hidde's phone round.
- **Open:** test account's line in data/our-accounts.json (BACKLOG, build 41 step 3), so the digest still counts apptest@ as new.
- **For Hidde:** Organizer, the top 1.0.4 (41), Distribute App; TestFlight round; submit with phased release. The two 1.0.4 (40) archives of 14:14 and 14:34 are not for upload.

## 2026-11-08 session: build 41 scope, and the map sheet the Airbnb way for build 42

- **Decided (Hidde, "eens"):** build 41 ships today's fixes only (Discover's ambassador seat, the pin blink, plus what other sessions readied: New from visitors, Plus under the trees). The map sheet change below is **build 42**, on its own branch, judged by Hidde in TestFlight.
- **Build 42, the map sheet as Airbnb draws it** (Hidde's screenshots, 2026-11-08: "er zit veel loze ruimte boven in de lijst als je hem naar boven scrollt - zullen we Airbnb nadoen"): at full height the list is the page, starting right under the search field, no grip and no empty count strip; the floating "Map" pill brings the map back. This reverses his 2026-10-10 and 10-13 ruling to keep the strip at full height (its reason, the strip as the handle back down, is carried by the Map pill now). At the lowest stop only the count bar stays ("58 trees") and the tab bar hides, so the map takes the screen; a tap or swipe brings both back. Web explore drops the same empty strip in the same change. FlowWalk's map flow and ButtonWalk's sheet steps move with it.

## 2026-11-08 session: the app's QA, signed in for real, every button tapped, red stops a build

- **Why:** Hidde kept finding holes ("hoe staat dat er in z'n totaliteit voor", "waarom testen we in Gods naam alleen uitgelogd"). Measured with the new `scripts/app_coverage.py`: 201 named app controls, 63 named by any UI test; every "signed-in" test ran on a fake session that cannot write; the app run had been red since 11-06 and builds went out anyway.
- **Built, on branch claude/gifted-cerf-cbp95i, through CI on GitHub's Mac runners:** ButtonWalk.swift + buttonwalk.yml (every button on 13 screens, signed out and in, must change something; daily). A real test account (`scripts/test_session.py`, apptest@ancienttrees.app, fresh random password per run, profile private, session masked and handed over as AT_TEST_SESSION, Debug builds only) and SignedInRoundTrip.swift (save a tree, reopen, still saved; remove, reopen, gone). `release.py` refuses to archive while the newest finished ios.yml run on main is not green (`--despite-red "<why>"` is Hidde's). Rules in CLAUDE.md QA.
- **Open:** add the test account's line to data/our-accounts.json from the first run's log; make main's app run green (FlowWalk tree-card, the map sheet's ambassador seat signed out).

## 2026-11-08 session: Discover's ambassador seat does not answer a tap (build 40)

- **Breakage:** on Hidde's phone (build 40, iOS 27) the "Den Bosch is looking for an ambassador" row on Discover does nothing when tapped, though it shows the chevron (no request sent). It became a sheetTap (onTapGesture) instead of a Button on 11-05 (27a6c23), for the map's sheet; that is the only change to it since it worked.
- **Fix, on branch claude/gifted-cerf-cbp95i, not built:** `AmbassadorWantedRow(inSheet: false)` on Discover is a plain Button again; the map sheet's seat keeps sheetTap. New UI test AmbassadorAskWalk: the seat on Discover (-at= Cadiz) signed out and signed in, the city sheet's seat signed in at both heights, with no coordinate-tap fallback (SignedOutWalk tapped only the sheet's seat, only signed out, and falls back to a coordinate tap, which is why no run caught it).
- **For Hidde:** the next Mac session builds, runs AmbassadorAskWalk and merges before build 41. If the city sheet's seat fails too, sheetTap itself is broken on a real tap, and the other sheetTap rows (Plus, followers, sign-in, the seen tick, place links) need the same look; the failing FlowWalk "tree-card" step from the night runs may be the same cause.

## 2026-11-08 night run (01:03 window), short

Rung 1: nothing waiting (0 photographs, no new tree notes). Rung 2: health.py exit 1 on the iOS app. Its scheduled runs fail on one UI test, `FlowWalk.testEveryFlowLeavesAWayBack`, step "open-the-first-tree" (FlowWalk.swift:135): the `tree-card` button at y 727 cannot be scrolled into view (kAXErrorCannotComplete), on iOS 26 and the iOS 18 floor alike. Not reproducible on this Linux runner, so not fixed. It may mean the sheet no longer raises on the tap, or the bigger catalogue changed the first card. For a Mac session. Web errors ORANGE: ResizeObserver loop notice, a harmless browser message, not acted on.
Rung 5: Sintra verify pass (claimed, run, released): 0 new trees, every unmined register row is already live, blocked or outside Sintra; Monserrate swamp cypress still has no independent source or pin. Sintra is a wall for 48h. Nothing published this window.


## 2026-11-08 night run (window 00:57 UTC): nothing published

Product: nothing changed. Rung 1 empty (no sightings waiting, no new notes). Preflight says 4 submissions have no written verdict, but `judgement.py --open` lists only rows that already carry a verdict, so I could not find them; a session should look. Rung 2: health.py exits 1 only for the scheduled iOS run (failed 11-07 20:39 after 54 min, third scheduled failure in a row; the failed assertions are in the xcresult artifact, which this Linux runner cannot open). The web error is a ResizeObserver loop notice, browser noise, orange not red.
Shelf: READY leads 0, so I refilled with a verify pass on Sintra. It added nothing: register candidates all live, blocked or belong to Cascais/Lisbon; the Monserrate swamp cypress and Pena sequoias stay leads on one effective source (jardimformoso returned 429). Sintra is a wall for 48h, claim released.
For Hidde: iOS scheduled runs keep failing; look at the xcresult artifact of run 42412097686.

## 2026-11-08 daily publish (scheduled task): Lyon +10 into the app, queue empty

- **What went live (9b09e3009), app only under APP FIRST, no web page:** Lyon lyo_026 to lyo_035 from data/research/lyon-verified-2.json, written 11-02 to 11-04 and the last unmerged set on the shelf: Square Ferrié's cedars, copper beeches and red oak, the Jardin des Chartreux hickory (species asked of the reader), the weeping blue cedar of Square Henri Dor and the planes of Quai Clemenceau and Saint-Côme-Saint-Damien (Caluire), the unpruned planes of Collonges, the Balmont planes (La Duchère), the Écully town hall cedars. All Métropole register trees, flagged, approximate pins, no photograph, each with a recognition line. Grafted with the live intro, meta and FAQ untouched (out/tmp/graft_lyon.py); one typo fixed in the hickory story. Preflight 0 problems; the pace counts nothing while APP FIRST holds. /lyon 200; the new trees have no page of their own to check. No claims stood.
- **Still waits:** nothing writable. The five written trees left on the shelf are held with their reasons: cbr_007 (Penacova, outside the day-trip limit, not worth the walk), cdl_001 (Mastrinka, access unproven), sgz_003 (Ocuri, access line needs "anyone can book"), hnl_024 (ticketed aquarium, fence unknown), phl_020 (paid share). Salt Lake City's slc_019/020 are verified, not written.
- **Daily publish: queue empty.** For Hidde: the daily task "publish-held-trees-daily" can be switched off under Scheduled; new trees now reach the app straight from the night run's write passes.
- Breakage: the first push timed out connecting to GitHub (network, not the hook); the retry went through.

## 2026-11-07 night run (third attempt, same window): nothing published

Released the leipzig claim: its brief lists 0 candidates (no imported register covers it), so it is a wall for 48h. Munich's brief also has no coordinates or candidates (from-zero research needs Hidde's ask), so no claim. `leads.py --ready` is 0; the only unwritten verified files are Salt Lake City's two small trees (under the six-candidate floor, claim still held until it expires) and singles in other cities. Remaining ladder rungs need a Mac session (iOS schedule failures) or Hidde's word. Translation backup (Perugia, it) is blocked while TRANSLATIONS_OUT holds.

## 2026-11-07 night run (18:07 window): Salt Lake City verify, nothing published

Rung 2: health.py exits 1 on the iOS scheduled run (3 failures in a row, ~1h28m each; the log shows XCUITest "Failed to scroll to visible ... tree-card" AX errors, then timeout). It needs a Mac and the app worktree, so it is a session's, not this runner's. Web errors ORANGE: one ResizeObserver loop message, benign, left alone. Rung 1 empty. Shelf: prepare.py says refill; portland refused (full). Claimed salt-lake-city (18 of 20), verify agent delivered slc_019 (Lavalle Hawthorn) and slc_020 (Red Horsechestnut), both University of Utah register trees, flagged, approximate pins, no photo, small trees. Under the six-candidate floor for a write pass, so not written; claim left in place (release refused until merged, correctly) and expires in 4 hours. Cost: about 85k tokens for 2 unpublished trees.

## 2026-11-07 night run (13:20 window), second attempt

- Nothing new published. Coimbra verify pass found nothing: its 4 unmined candidates are already live (cbr_001 to 004) or leads; two leads added (botanic garden eucalyptus and deodar, black poplar access; uc.pt 403). Left cbr_007 (Penacova wisteria pergola, 3.25 m tall) unmerged: not a tree worth the walk; claim force-released, Coimbra is a wall for 48h. `leads.py --ready` is 0. Perugia translation claimed then released unrun, since TRANSLATIONS_OUT pauses new translation passes (BACKUP block still offers one). Brighton register retry not run (wall, verified empty within 48h). Next: staged Portuguese and German cities (guimaraes, porto, setubal, sintra, bamberg, munich).

- Rungs 1 and 2: no reader photos or notes waiting. health.py: iOS app red on its schedule (UI test `tree-card` "Failed to scroll to visible", AX error, run takes 1h28m; app-side, needs a Mac session, not fixed here). Web errors orange (one ResizeObserver message, under the red threshold).
- Rung 5, write pass on the verified shelf: 7 trees merged and app-only under APP FIRST (Fort Worth 2, Tucson 3, Chattanooga 1, New York 1), preflight 0 problems. About 15 more were held again with reasons in their verified files (can't be told apart, access not established, dead or duplicate). sgz_003 (Ocuri wild olive) is written but its access line needs "anyone can book the tour" before it can ship.
- Salt Lake City (top of the US queue): verify pass on the Utah Big Tree register, 4 trees (three Murray City arboretum champions plus a Jordan River willow), written and merged as slc_015 to slc_018, app-only, preflight 0 problems, claim released. City intro/meta still say five or six trees (app-only trees make no page text change). Note: data/agent-costs.json holds two lists under the key "2026-11-04"; json loaders drop the first, so anything that rewrites the file through json loses entries.
- Miami: verify pass found nothing new (wall for 48h, claim force-released since the one "unmerged" entry is a Key West tree from an older pass). Chicago: 3 Bunker Hill Woods register trees (county champions, GPS-fixed, confirmed pins) verified and merged as chi_045 to chi_047, app-only, preflight 0 problems.
- London and Key West: the two "verified, unwritten" trees were already live (lon_031 duplicates lon_002, the Royal Oak, now in blocked leads; kyw_001 already in key-west.json), so nothing written; London (0 of 30 leads have a coordinate) and Key West are walls for 48h. Open point: lon_002's live story cites the Woodland Trust Ancient Tree Inventory, a source CLAUDE.md says we never touch; a session should check that line. Shelf for the US and UK is now thin: remaining verified files hold only held trees (see their notes). Stopped here with the queue's cheap supply spent.

## 2026-11-07 session: the digest, New from visitors, a stuck deploy

- **What changed in the product.** New from visitors (web homepage, app Discover) now orders by when the photograph was taken, each person's newest first, so the first eleven tiles are eleven people (Préfargier, Cramond, Paris lead; Reykjavik was on top because status rewrites touch `updated_at`). A generated profile name ("Green Fig 1965") prints and links like any name; only a private profile says "A visitor" (Hidde: "just give the link to their made up name"). supabase/new-from-visitors.sql pasted by Hidde and checked; web checked live; the app part ships with build 41. The Préfargier cedars showed the reader's photograph twice (lead and strip): strip copy removed, and live-first now skips a sighting that is already the lead (`is_lead` in sightings_publish.py). Checked live.
- **Digest.** The quality block, when anything is not green, is the full table Hidde approved on 11-04 (every row with its question, a light and a word per cell, Backup a row). Hidde: "keep the quality thing like this from now on".
- **Breakage, fixed.** Every deploy this morning failed QA on four photographs without a measured width (La Palma 3, Lanzarote 1; the Yaiza ombu's url was the Commons page, now the file). Live again.
- **Open.** iOS: FlowWalk testEveryFlowLeavesAWayBack cannot scroll to the tree card at the bottom of the screen (iOS 18 and newest, both retries), plus layout findings on city (2) and Explore (4); likely 11-06's Discover changes; fix before build 41. Moderation gap, Hidde to decide: New from visitors shows live-first strip photographs nobody has looked at yet. Plus answers so far are tests ("test" from Rome web). Hidde asked whether "Something else" should require text; open.

## 2026-11-07 (second retry window): nothing published, the shelf is dry

READY is 0. Spokane has 1 unmined register candidate and Coimbra 4 (under the six-candidate floor), so no verify pass was dispatched. Spokane claimed then released (wall 48h). Coimbra not claimed; cbr_007 sits verified in data/research/coimbra-verified.json awaiting a story. Brighton register already retried 11-04 and 11-06, still stalled. Perugia translation skipped while TRANSLATIONS_OUT holds. Next: a scout of a new US or UK register, or Coimbra's cbr_007 in the next write pass.

## 2026-11-07 (retry window): READY leads held, Fort Worth verify found one thin tree

All 29 READY leads were tagged SKIPPED with reasons (access, dead, no single tree, no source). Fort Worth verify delivered ftw_027 (flagged, thin alive evidence), not merged; claim released with --force, wall for 48h. Nothing new published by this attempt. Next: the staged Portuguese and German cities, or the Brighton register retry.

## 2026-11-07 (write pass): 21 written trees into the app, 16 new places

**What went live, app only under APP FIRST (no web page or place page):** the written backlog of 11-02 to 11-04 that had no builder, now `scripts/build_backlog_2026_11_07.py`. Thailand: Ayutthaya 2 (the Buddha-head fig at Wat Mahathat, the bodhi gate of Wat Phra Ngam), Chiang Mai (the city-pillar yang na), Sukhothai (the Wat Si Chum mango), Tha Maka (the shrine in the tree hollow). George Town (the 1871 Penang baobab). Montenegro: Kotor (the Trg od Kina poplar) and Bar (the Stara Maslina, published as mtn_001). Croatia: Kaštela (the Gomilica oak). Portugal: Horta 2. Spain: La Palma 4, Lanzarote 1. Italy: Lecce, Vernole, Martina Franca, Milo (Fornazzo), Zafferana Etnea. Place copy for 11 places written this pass (data/research/backlog-places-2026-11-07.json); La Palma and Lanzarote's `recognise` lines moved to `how_to_recognise`; La Palma's dragon trees renamed Dragon Tree to match Cádiz. city_names.py run (Milo and Tha Maka unresolved). Preflight 0 problems; qa.py could not run (no site/dist here).
**Held, unchanged:** cdl_001 Mastrinka (access), tus_013/014, nyc_085, hnl_024, sgz_003, cbr_007 Penacova (outside the day-trip limit).
**READY leads:** all 29 were register rows, OSM nodes or trees an earlier pass had already declined (no access, life or tree-level source, campus, burned, whole parks). None was written; each now carries `[SKIPPED 2026-11-07 by the write pass: why]`, so `leads.py --ready` reads 0.

## 2026-11-07 (06:01 window): New York enrichment, nothing new published

Rung 1 empty. Rung 2: health.py still exit 1 for the iOS app (scheduled run red: `testEveryFlowLeavesAWayBack` cannot scroll to the `tree-card` button on iOS 18, plus layout findings on city and explore), which needs a Mac reproduction, so left for a session. The live site is behind main and knocks were 6 of 12; I did not dispatch either. The shelf has nothing writable: New York's remaining verified files are the held duplicates nyc_029 and nyc_094 and the mislabelled nyc_085 (claim taken in error, released with --force), and Brighton is a 48h wall. Enrichment on New York: five access lines (nyc_034, 035, 074, 075, 076, gardens' own posted hours); Green-Wood nyc_140 and nyc_141 have no readable per-tree record (JS tree finder), and the season gaps were not researched, so 20 gaps are dead ends for 90 days. No trees added, nothing counts toward the pace.

## 2026-11-07 (01:31 window): San Francisco verify, US/UK write pass, enrichment; nothing new published

Rung 1 empty (no sightings, no notes). Rung 2: health.py exit 1 for the iOS app (scheduled run red: UI test fails to scroll to the `tree-card` button on iOS 18, plus two city-screen layout findings, 98 and 133 elements) and 6 of 12 knocks delivered; the iOS fix needs a Mac reproduction, so left for a session. Then: San Francisco verify (4th pass) found nothing, the register is exhausted, and its 3 verified entries are duplicates of live trees (sfo_012 of sfo_004, sfo_014 of sfo_003, sfo_015 of sfo_006); claim released, wall for 48h. A US/UK write pass found nothing writable: most files are stale, Fort Worth ftw_024 to ftw_026 cannot be told apart on the ground, and hold reasons were recorded (Fort Worth, Brindisi, Isole Tremiti). nyc_085 needs a verify pass to fix its species field (a black oak and willow oak hybrid, not Swamp White Oak) before it can ship. Enrichment on Tenerife, Rome, Palermo and Oahu: one access line for pal_027; 17 gaps closed as dead ends (the Honolulu register rounds to about 1 km, season files hold nothing above "nice"). No trees added, so nothing counts toward the pace. Seen: sfrecpark.org hangs on curl -m 20. About 15 research files hold only published trees and could be deleted.

## 2026-11-07 (third attempt): Braga verify, nothing published

Pulled and checked claims first. `leads.py --ready` held 29 leads, all out of focus (Malta, Bali, Sicily, Cyprus and similar) or declined by the earlier write pass, so I wrote none. A verify pass on Braga found no new tree: the four in-city candidates are live and the two Tibães trees (brg_004, brg_005) stay held because the cerca closure is unconfirmed (host unreachable, Wayback still 2026-09-24). Braga is now a wall for 48h. Fort Worth's claim stands with 3 candidates, under the six needed for a write pass. The Perugia translation was not taken because TRANSLATIONS_OUT pauses new translation passes. Next: re-check Tibães after a Wayback snapshot dated past 7 Nov, and the Agaete fig verify.

## 2026-11-07 (retry attempt, verify on Fort Worth): 3 candidates, nothing published

A verify pass on Fort Worth delivered 3 one-source trees from the city's heritage layer to data/research/fort-worth-verified.json: ftw_024 Casino Beach Pecan, ftw_025 Monticello Park Live Oak, ftw_026 Todd Island Post Oak Grove. All have approximate pins and no photograph, and the alive checks are thin. They are not merged or written yet, because that pass sits under the six-candidate minimum for a write. The fort-worth claim in data/in-flight.json is still standing (release refuses until ftw_021 and the new ids merge); it expires in 4 hours. Portland refused a claim (33 of 30). Next: a write pass once the Fort Worth batch reaches six, or a Perugia Italian translation from BACKUP.

## 2026-11-07 (write pass on READY leads): nothing published

The write pass found no tree it could write honestly. Gran Canaria's six Osorio trees need a permit from the Cabildo's Servicio de Medio Ambiente, so hard rule 10 holds them unless Hidde rules that a free permit counts as bookable. The other Gran Canaria leads are remote, groups, or have no life check. In Italy, Portugal and Washington DC the READY leads were register rows or held pins, with no access source, sighting or facts beyond the numbers. All 59 are kept as leads, each with a one-line reason (`write_pass_2026_11_07`), so `leads.py --ready` dropped from 84 to 29. The 18 unwritten trees in data/research/*-verified.json are all held by earlier passes. The best candidate for a verify pass is the white fig of the Huerto de las Flores in Agaete: public, easy access, seen alive recently. The Cabildo ficha loops on redirects for WebFetch, so it needs another way in.

## 2026-11-07 (night run, 00:22 window): nothing published

Rung 1 empty (no sightings, no tree notes). Rung 2: health.py exit 1 on the iOS app (scheduled run 2026-11-06 21:55, failed) and on 5 of 12 knocks delivered. The iOS failures are real layout findings from the 11-06 app work, not infrastructure: city screen on iPhone 17 Pro, `highlight-card` and an Image end 66 points past the 402pt edge (CLIPPED); explore on iPhone SE (iOS 18.6), four `visitor-name` buttons are 78 by 16, under Apple's 44 by 44 (SMALL); iOS 18 test `testEveryFlowLeavesAWayBack` could not scroll to `tree-card`. I cannot build or sweep the app on this runner, so I changed no Swift. For Hidde: next app session should fix the three before build 41.
Supply: the shelf is thin. Of the "written and ready to merge" files, the Tucson, New York 3 (nyc_085) and Oahu ones are held trees the pipeline already declines, so I did not merge them. `scout_next.py --target` says RETRY Brighton while prepare.py lists Brighton as a wall verified empty in the last 48h; I did not retry it. Nothing was claimed, written or committed apart from this entry.

