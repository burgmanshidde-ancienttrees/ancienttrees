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

## 2026-11-06 (night session: New from visitors on the web homepage)

Live on ancienttrees.app: the homepage's "New from visitors" row, right under the intro line and above the favourite cities (where the app puts it, before the cities). Design shown to Hidde first and approved, with his one change: every name in the row stands on one height, so tile titles stop at two lines. Same data as the app (new_from_visitors(), one tile per tree, from four tiles), the shelf card plus a 16px avatar and the name, "A visitor" for no public profile or a generated name; a tap on a name opens the profile, signed out it opens sign-in (checked live). Heading in all eight languages. Card data is baked at build for the 48 trees with a visitor's photo, so a photo newer than the last deploy shows from the next one. Checked live at 375px and desktop, 12 tiles today.

## 2026-11-06 (evening session: build 40 and the map's Airbnb search)

Build 40 (1.0.4) archived from ad9e052c1 by scripts/release.py and tested on Hidde's phone (iOS 27); he uploads it. In it: Discover no longer goes empty after an island tile (a NavigationLink pushed the empty place page, iOS 27 kept it); one tapped tree's card raises no further; the map's search works as Airbnb's map, app and web: a searched place shows only its pins, count and trees until you drag, zoom or tap the cross, and the cross leaves the camera where it is; the sheet's count is small and centred under the grip; a searched city's ambassador box sits under the Highlights; your own and collected trees are a "Collected" shelf under the Highlights; Discover's second row "New from visitors" (supabase/new-from-visitors.sql, pasted by Hidde; names only from public profiles, generated names show "A visitor", our own accounts left out; CLAUDE.md records that the name shows signed out, the profile asks to sign in). Web explore carries the same search and shelf (live, France checked). Not done: "New from visitors" on the web homepage; a tile shows the tree's lead photo, which is not always the visitor's own.

## 2026-11-06 (late window, second attempt)

Shipped 7 app-only trees: Powerscourt's tallest Douglas fir (new place enniskerry), Hackberry of Terenzano (Florence), Ashburn red mulberry (leesburg), and four in Cardiff (crd_009, 011, 012, 013). Most "READY" leads were not: 17 were declined with reasons recorded in the lead files so `leads.py --ready` stops offering them; the 401 "awaiting a writer" figure is mostly stale research files of trees already live. San Francisco verify found nothing new (register exhausted by three passes); its claim stays until sfo_014/015 are merged or it expires (4 h). Still open: the failing scheduled workflows (deploy, iOS) were not looked at this attempt.

## 2026-11-06 night window (20:13 UTC start)

Rung 1: one reader photograph (three Atlas cedars of Préfargier, 0 m from the pin, daylight) viewed and judged `add`; it was already in the strip live-first, so nothing changed. Rung 2: the failing deploy was the 8 unmeasured photographs, already fixed by `photo_res.py` in 8f18f37a3 (0 unmeasured now, deploy in flight); iOS runs are being cancelled by Hidde's pushes, not failing on their own. Rung 5: New York verify on the 13 READY leads found most already judged by earlier passes; one tree shipped, app-only (nyc_143 Willow Oak of Herbert Street, census-pinned, 271 cm girth), the Quincy St elm confirmed a stump and blocked. Bath enrichment: height, girth, access and sources on the four Sydney Gardens trees, three pins and all registers recorded as dead ends. Brighton scouting retry found nothing new (council Stanmer list has no coordinates; the yew, Preston Twin, Brace elm and cedar are already live); 5 leads and 1 block added, Brighton walled for 48h.
Prepare's 7-day visits line was not in its output. No tool call was refused. Open for a session: `reader_words.py` lists 3 Barcelona notes (amicsjbb tall-tree sentence) not yet quoted on bcn_005, bcn_021, bcn_022.

## 2026-11-06 late session: the Plus question moves under the trees

**What changed in the product.** "Help create Ancient Trees Plus" no longer sits in the white box under a city's intro, where on a phone it was the first thing after the city's name. It now has its own box under the trees: on the city page (English and every kept translation) after the "Know one we missed? Tell us" line, in /explore's list for a searched city after the last row, and in the app's map list for a searched city after the last tree. The ambassador row stays on top. Hidde, before the Guardian piece: "ja ik denk dat dit beter is dan kunnen we altijd nog meer op de voorgrond zetten als nodig", after a mockup of London on web phone, desktop and app. Answers so far: 1 (his own test), so no measurement was disturbed. The `plus_ask` switch and the answered-here flag still remove the row, and its empty box goes with it (`.plus-under` in style.css; `PlusUnderBox` in PlaceAmbassadors.swift). The app change ships with the next build.

## 2026-11-06 daily publish (scheduled task): 22 US and UK trees into the app

- **What went live (311725714), app only under APP FIRST, no web page or place page:** Philadelphia +5 (phl_005..009: Bartram yellowwood, Woodlands zelkova, Laurel Hill cutleaf linden, Hobson Street scholar tree, Washington Square sycamore; build_us_philadelphia.py `--only philadelphia`). Northern Ireland estates 10 and the Highlands 6 from build_uk_ni_highlands.py (`--only` without Belfast, whose live file the builder would rewrite): Castlewellan 4, Florence Court, Crom, Dark Hedges, Rostrevor (Old Homer), Armagh (King Tree), Gosford, Ardkinglas 2, Glen Affric, Benmore, Reelig Glen, Inverness. Cardiff +1: the Bute Park Wellingtonia, car_003 in cardiff-verified.json, grafted as crd_008 (marked `published_as` there). Preflight clean; the pace counts nothing while APP FIRST holds, so the 25 was this task's own limit. Live and checked after deploy 42289614506: 22 of 22 in /api/cards.json as pins, none with a page link; /philadelphia 200, /castlewellan 404 (no place page, as APP FIRST wants).
- **Breakage:** the first deploy failed QA on 8 approved Commons photos without a measured width (the NI/Highlands builder copies no size); photo_res.py fixed it (8f18f37a3, another session committed the same fix first). The next was stopped by pagecheck timing out on /london, fixed by another session in pagecheck itself. build_uk_ni_highlands.py should run photo_res.py after it next time.
- **Copy kept, on purpose:** the Philadelphia builder replaces intro, meta and FAQ with "nine trees"; preflight refused it (the web page shows 4, the five new ones are app-only), so Philadelphia and Cardiff keep their committed copy. When a tree there gets a reader's addition and its page, the count words need updating.
- **Held in the files, not waiting:** phl_020 (paid share), tus_013/tus_014 (no visible reason), hnl_024 (fence unknown), nyc_085 (species mislabel). No claims stood.
- **Still waits, about 34 written trees (no builder; each wants a graft like Cardiff's):** Spain/Portugal: La Palma 4, Horta 2, Lanzarote 1, Coimbra 1, Grazalema 1. France: Lyon 10 (lyon-verified-2.json). Italy: Lecce, Martina Franca, Vernole, Zafferana Etnea, Milo. Rest: Ayutthaya 2, Kotor 2, Croatia central Dalmatia 2, Chiang Mai, George Town, Sukhothai, Tha Maka. At 25 a day: about two more days, then the queue is empty.

## 2026-11-06 evening session: the explore map crashed the tab

**Breakage, fixed.** Since 476ee80 (this afternoon's "the map names the place in view") /explore crashed the browser tab a few seconds after loading (Chrome "Error code 5"), on desktop and phone, anywhere on the map; Hidde hit it looking at the United Kingdom. Cause: the new trees list painted its save hearts with `atPaintSaves`, which on explore refilters the map, which redraws the list, forever. The list now paints the hearts alone (`atPaintSaveButtons`, tree-actions-js.ts). Found by pausing the live page in a debugger; the live page with the same patch stayed up at 1280 and 375 px with "United Kingdom" and its rows. The /united-kingdom page itself never crashed. db1416a2f.

**How it slipped through, and what now stops it** (Hidde: "doe het"). qa.py and preflight read files and never run the JavaScript; the smoke test runs Chrome but after the site is live, and its hang on /explore was read as a fault of the test (d3983b8). Three parts, all live with this push: (1) `scripts/pagecheck.py` opens nine pages (explore over the UK among them) in Chrome at desktop and phone width and fails on a crash, a hang or an error from our own scripts; deploy.yml runs it before the upload, so a broken build never replaces a working site. Run against the live site before the fix, it failed exactly the four explore lines and passed the rest. (2) rollback.yml puts back the previous build in about five minutes without building (uploads now kept seven days). (3) pages-live.yml runs the same check on the live site every hour into the quality line and health.py. Ratchet: `check_the_pages_run_before_they_go_live()`. The deploy gets a few minutes longer.

## 2026-11-06 session: the Guardian, app-only trees as web pins, press images

**What changed in the product.** Every app-only tree (568) now stands on the web maps as a pin, with a card: photo when it has one, name, species, age, place, save, and "Read its story in the app" (the one get-the-app control). Still no page, sitemap, search or places line, so Google gets nothing new to crawl (`APP_ONLY_PINS` in site/src/lib/app-first.ts, `mapTrees()` in trees.ts; qa's app-first check reads the switch). Checked live: 568 of 568 on the map, 0 cards with a page link, 0 in search; the card looked at on desktop and at 390 px. The Android waitlist sheet's email field was a 192 px oval on phones; now 45 px. App: demo switches `-followers=`, `-following=`, `-avatar=` for press and store screenshots.

**Why.** Joe Pinner (Guardian environment desk, Scott Trust trainee) interviewed Hidde today; the piece is expected around Monday. Half the UK was missing from the web map (131 web, 122 app-only), and most mobile readers are on Android. Hidde: "put all pins live of the app only trees".

**Then, on his word ("lift limit once! this is exceptional curcumstance"):** every app-only UK tree got its page, 122 at once, through data/app-first-released.json (read by findable.app_only() and app-first.ts). Live and checked: 122 of 122 in search, London 48, Bristol 22 ("Twenty-two" in its intro and meta), Cambridge 10, Canterbury, Wolverhampton and Sheffield have place pages for the first time; the pages carry the googlebot noindex. APP FIRST and the 25-a-day pace hold for every other tree.

**Open, Hidde's call.** Holding iOS 1.0.4 until after the spike (submit with manual release). Press images are in out/press/for-joe (gitignored out/).

**Breakage.** The pins deploy collided twice with another session's deploy; a newer run carrying the same commit went live, the older one was cancelled so it could not overwrite it.

## 2026-11-06 night run (window from 13:37 UTC): rung 1, one reader photograph

- Looked at the reader's two frames for the Three Atlas Cedars of Préfargier (prf_001): the first is the right tree (three joined crowns, gravel path, bench), the second is an information board. Verdict `add`; publish reported the photograph already in the strip, so nothing new went live. Preflight: 0 problems.
- Stopped there: this run did no enrichment, writing or scouting. The queue's next items (Bath enrichment, 106 READY leads) are untouched.

## 2026-11-06 session: the Préfargier cedars live; deploy unblocked twice

- **What changed:** a reader's tree, the Three Atlas Cedars of Préfargier (La Tène, canton of Neuchâtel, prf_001), live on Hidde's yes from their app photograph, note and GPS fix (scripts/build_la_tene.py, id prefix prf since ltn is Lorton's). One tree, so no place page. Story keeps to what the photograph shows; their note quoted. Not done: submission #627's outcome and the reader's mail are left to the knock (tree_approved.py).
- **Breakage:** the 08:51 and 09:15 deploys failed on night-run data: `age_estimate: null` in Bisceglie and Foresta Umbra (schema wants a string or no key), 25 unmeasured photos (`photo_res.py`), and two Commons strip photos without width/height in Balfron and Canterbury (feedshape refuses a null for installed apps). All fixed; preflight now refuses a null plain-string field and a strip photo without a size at the push.
- Hidde's test note on bcn_012 is live; the digest leaves our own accounts' notes out on purpose.

## 2026-11-06 session: Cramond reader photo live, "embrace reader content"

- **What changed:** the reader's app photo of the Rockface Sycamore of Cramond (edi_008), held on 11-04 as a wide path scene, is in the tree's strip beside the Cramond Association lead (verdict `add`; undo `sightings_publish.py --unstrip 4b28d99e-e0f2-4572-b851-23dd79e73031`).
- **New rule (Hidde):** "we should embrace all user generated content", "as long as its sort of the tree - we can be picky later". A reader photo that roughly shows the tree goes in the strip; a weaker frame than the lead is never a hold. In CLAUDE.md (Reader input) and the photo-judge agent.

## 2026-11-06 night run (second attempt): held sets published, app only

- **Published from the shelf (all written 11-02/11-04, held for a pace that does not count app-only trees):** Croatian coast 10 (Pula 2, Rab, Lun, Split, Zadar, Brac, Hvar, Cara, Orebic), Greek islands (Corfu 8, Kefalonia 1, Paros 1), Lampang 1, Thai south (Ko Pha Ngan, Kantang, Krabi, Takua Pa), Puglia (Palagiano, Vico del Gargano, Foresta Umbra, Bisceglie), Glasgow +4, Cannock Chase 3, Milton Keynes 2, Balfron 1. Preflight clean on the commit; the qa.py build check did not run (no site/dist on this runner).
- **Not published:** Wolverhampton (4 trees, id prefix `wol` clashes with Woolland: needs a new prefix), and Scone, Blair Atholl, Meikleour (build_uk.py makes them as separate places but Dunkeld already holds the same three trees and photos). The four generated files sit in out/tmp/. build_uk.py also rewrites Edinburgh, Dunkeld and Glasgow wholesale and drops later photo width/height fields, so only Glasgow's additions were kept. A rerun of the builder needs those three checked out of git afterwards.
- **Still unmerged but written:** Ayutthaya 2, Chiang Mai, Coimbra, Cardiff, George Town, Horta 2, Kotor 2, La Palma 4, Lanzarote, Lecce, Martina Franca, Milo, Stirling, Sukhothai, Tha Maka, Vernole, Zafferana Etnea and others; no builder for them, they want a graft into the live city files.
- **Not done:** `leads.py --ready` (106) is inflated by leads an earlier pass declined, so no write pass was dispatched on it. Verified but still unwritten: Aspromonte 2, Brindisi, Castelbuono, Chattanooga, Dartmoor, Frankfurt, Innsbruck, Isole Tremiti, Noto 2, San Francisco, Serra San Bruno 2, Taiwan.

## 2026-11-06 night run (06:46 window): rung 5, New York and the UK into the app

- **Rung 1:** nothing waiting (no photographs, no tree notes).
- **Rung 2:** Postbox check fails because supabase/plus-answers.sql (`plus_answers.other_text`) was never pasted: **For Hidde: paste supabase/plus-answers.sql into Supabase.** iOS app failed on its schedule (3 in a row): the "floor" job (iOS 18 alignment sweep) reports right-edge TRAIL findings on the `directions-apple` button (directions sheet) and the `review-yes` button (review ask) at the small-phone size. That is a visible app layout change and needs a Mac session with the sweep; this runner cannot render it. Only 5 of 12 knocks delivered.
- **New York:** write pass on 29 verified Great Trees (new-york-2/3/4), merged via build_us_newyork_2026_11_06.py, species aligned to the canonical names (Small-leaved Lime, Weeping Beech, Wild Cherry, Fern-leaved Beech, Persian Ironwood). New York now 95. Held: nyc_085 (Parks species mislabel), nyc_094 and nyc_029 (duplicates of the Camperdown Elm). Six botanic-garden trees have paid-entry wording in access but no `paid_entry` flag (a preflight note).
- **UK:** the written West, North and South sets held since 11-04 for the pace (the pace does not count app-only trees) merged: 42 places incl. Westonbirt, Canterbury, Stratford, Exeter, Sheffield, Wells, the Cotswold and Welsh yews. Preflight 0 problems. Five new places have no Wikipedia match for their names (Discoed, Llanfaredd, Lorton, Martindale, Wells), a look rather than a guess.
- **Italy and Spain:** build_italy_south (Agrigento 8, Palazzolo Acreide, Noto, Ragusa, Benevento, Portici, Castellammare, Monte Faito, Sila, Serra San Bruno), build_italy_central (Spoleto 6, Vallombrosa 4) and build_andalucia (Cazorla 5, Grazalema, Alpujarras, Aracena) merged, app only. The scripts' rewrite of the Granada, Malaga, Ronda, Naples and Palermo meta and FAQ was dropped (count-promise failures); their trees went in afterwards, see below. Three Andalucia files had `curation_status: verified` (set to flagged) and Cazorla's "Turpentine Tree" became Terebinth. Four more stories written (Oahu banyan, Penacova wisteria, two Tucson) but left unmerged: the Tucson pair carry an earlier hold, Penacova is outside the day-trip limit, the Waikiki banyan's ticket status is unclear.
- **Canaries, Azores, Algarve:** Santa Cruz de Tenerife 9 (ids renamed sct_ to stz_, since Scottsdale holds sct), Angra do Heroismo 2 and Tavira 1 merged, app only. Granada 2, Malaga 1 and Ronda 4 then grafted into their live pages with the live copy untouched (the builds' grown meta and FAQ promise more trees than the web shows while the new ones are app-only; Naples, Palermo, Azores already held theirs). Not done: the Tenerife and Azores grown intros.
- **READY leads are inflated:** a write pass over the 23 READY leads in Washington DC and New York found 22 that an earlier pass had already declined in its own words (dead, young, private, no pin, duplicate), so `leads.py --ready` overstates the writable pile. Only the Fort C.F. Smith tulip tree (wdc_042, approximate pin, no photo) shipped, Washington DC now 34. Those 22 want marking as declined in their lead files.

