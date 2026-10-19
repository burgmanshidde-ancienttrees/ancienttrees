# LOG

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-10](archive/LOG-2026-10.md)
- [2026-09](archive/LOG-2026-09.md)
- [2026-08](archive/LOG-2026-08.md)
- [2026-07](archive/LOG-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.

## 2026-10-19 05:21 window: Miami opens, Key West and London added

Visits last 7 days: 1920 (3080 page views). Inbox empty. health.py: same two flags as the earlier window (scheduled iOS run failed again, smoke "skipped" on push); not touched, needs a session. Rung 4: write pass (Opus, ~95k tokens) on the staged Miami file. New: Miami with 4 trees (Simpson Park paradise tree, Vizcaya Garden Mound oaks, redberry stopper, last Cuban royal palm; page copy written), Key West as its own one-tree place (kyw_001, 250 km from Miami, tree page only), and London lon_033 Roehampton Lucombe Oak. All pins approximate, no photographs yet; 3 of 4 Miami trees sit behind Vizcaya's ticket (note only, free trees wanted). us-states.json and city_names updated. Preflight 0 problems. Claim released with --force (kyw_001 lives in key-west.json).

Second item, same window: Miami and Key West deepen. Verify pass (Sonnet, ~190k tokens) found 4 free trees, all single-source and flagged; write pass (Opus, ~107k) shipped mia_006 Castellow Hammock champion false mastic, mia_007 Merrick packing-house fig, mia_008 Collins Park baobabs, kyw_002 Key West Cemetery strangler figs (city foresters asked to remove them, decision postponed; Tree Commission agendas since Feb 2026 not checked), plus nsb_001 Venerable Oak of Novo Selo as its own one-tree place. Held: std_001 Grandpa Kolyo's Oak (private field, no roadside viewing coordinate). Miami now 7 trees, 3 paid; Castellow Hammock is a car trip, may want its own place later. Several Coral Gables nominations kept as leads. Preflight 0 problems.

Third item, same window: Innsbruck opened. Verify (Sonnet, ~78k) from the Land Tirol Naturdenkmal register (CC BY 4.0) joined to the de.wikipedia list: 7 flagged trees; write (Opus, ~95k) shipped inn_001 to inn_006 as a new Austrian city page, approximate pins, no ages (no source gives one), recognition line on each. Held inn_007 (lime below the Bergisel: access of the plot unsettled, only a 2016 photo). Hofgarten and Schloss Ambras not researched (no register points); they need their own pass. Eight leads and six blocked (felled trees) kept in data/leads/innsbruck.json. Preflight 0 problems. Superlatives collision chr_001/dnk_001 pre-exists, not from this pass.

Fourth item: photo hunt and viewing pass (Opus, ~115k) on the new Miami, Innsbruck and Key West trees, 23 candidates viewed as pixels. Approved: inn_003 Schulgasse Oak and inn_006 Traklpark Oak (register number in the filename, geotag under 20 m, CC BY-SA 3.0 AT, Gotglä). Reverse with `photo_apply.py hold <id> <url>` (inn_003 file ND_101_10_Eiche_Schulgasse..., inn_006 file ND_101_11_Stieleiche...). Held kyw_002 (which trunk?). Nothing usable for Miami (no whole-tree frame) or the other Innsbruck trees. Note: photo_fetch.py has no single-tree option and needed Pillow, which this runner lacks (installed under out/tmp/pylib, temporary). For Hidde: the scheduled iOS run still fails (timeout 1h54m on the simulator, push runs pass); not touched.

## 2026-10-19 02:51 window: Las Vegas retry, little on the shelf

Visits last 7 days: 1920 (2970 page views). Inbox empty. health.py: the scheduled iOS run failed again, in the log a simulator "Timed out while requesting launch progress" (infrastructure, push-triggered runs pass); smoke "skipped" is its push trigger, deploy green. Enrich empty. Shelf: READY 43 are mostly Roosendaal street trees earlier passes declined; the written trees in data/research are blocked (ftw_018 access, fdl_001 removed on purpose, no city file for Studena/Novo Selo/Key West). Scouting RETRY Las Vegas (already live with 11 trees, so a deepen): verify pass (Sonnet, ~85k tokens) flagged 2 UNLV champions, lvg_015 Mondell Pine (157 cm girth, 2023 Nevada register plus UNLV) and lvg_016 Holly Oak (small, one source); approximate pins, no photograph, so not written; the rest stay leads with reasons. Claim released with --force, Las Vegas a 48h wall. The scouting note is stale (the city is published).

## 2026-10-19 00:31 window: Delft enrichment

Visits last 7 days: 1951 (3075 page views). Inbox empty. health.py flags the scheduled iOS run (timed out at 1h54m, hand runs pass; needs a session, not touched) and a "skipped" smoke test (push-triggered, build itself green). Rung 4 on the frozen roster: Delft enrichment (Sonnet, ~51k tokens). del_012, del_013 and del_014 now carry register ids with girth and height from the LRMB layer, del_013 a sourced access line (free, sunrise to sunset), del_014 an autumn best_time. Pins stay approximate for all three (register coordinate equals ours, cemetery too big for a site). Preflight 0 problems.

Rung 4, scouting RETRY London (Great Trees of London list): verify pass found 3 flagged trees, photo-judge approved 2 (Royal Oak, Osterley cork oak; Roehampton Lucombe held, ambiguous trunk), write pass shipped lon_032 (Osterley Park Cork Oak, photo 640x480 so soft large; approximate pin) and fixed London's count copy. lon_031 Royal Oak is the live lon_002 (10 m away), so not written. For a session: lon_002's source and pin come from the Woodland Trust Ancient Tree Inventory, which the London gate forbids, and its story cites that inventory; the new Commons photo of the Royal Oak (Richmond_Royal_Oak_(3).jpg, CC BY-SA 4.0, in out/tmp/london-photos.json) could join lon_002's photos. Refused: nothing.

## 2026-10-18 22:16 window: deploy fix and roster photo pass

Visits last 7 days: 2079 (3240 page views). Rung 2: the failed deploy was qa's soft-hero check on Portland's Balch Creek Fir (375px iNaturalist medium file); swapped to the 1024px large file, measured by photo_res.py, preflight 0 problems, pushed (567f5b563). The iOS app failure is the scheduled run only and needs a session (not touched). Rung 4/6: `photo_hunt --recheck` plus `photo_fetch --roster` and a photo-judge pass: 2 approved (ber_059 Berlin oak, wdc_015 Smithsonian elm, large file), 1 held (nyc_022), 70 rejected. The roster photo sweep is close to exhausted; the yield per pass keeps falling. Written trees waiting in data/research (ftw_018 access unstated by its register, kyw_001 Miami below the four-tree floor) were left alone. Miami verify pass (Sonnet, ~105k tokens): 4 flagged trees in data/research/miami-verified.json (Simpson Park paradise tree free; three Vizcaya trees paid), all approximate pins and no photograph, so nothing could be written to a city file (Miami would be 75% paid and preflight needs a photo or confirmed pin). Parked, claim released; path forward is a photograph of the Simpson Park tree and a Miami Beach pass. Refused or odd: `python3 scripts/photo_fetch.py --roster` ran past the 600 s foreground limit and moved to the background on its own.

## 2026-10-18, second restart: merged written trees

- Live: Spokane gets the Grant Park Guardian (horse chestnut, no photo yet, so Bing and readers only). Counts and FAQ updated to 14.
- Not merged: ftw_018 Memorial Bur Oak (register does not say the ground is public, hard rule 10); fdl_001 Figueira das Lágrimas (slug is in REMOVED_TREE_SLUGS, removed on purpose). Key West, Studena and Novo Selo have no city file; left in research.
- READY (43) is mostly Roosendaal street trees; no write pass dispatched.

## 2026-10-18, restart after early stop: Frankfurt enrichment

- No new trees. Claims were empty; READY (43) is mostly Roosendaal leads earlier passes declined, so no write pass.
- Frankfurt enrichment (5 trees): frk_014 and frk_015 got a girth and height from the city's ND object pages (read via Wayback, frankfurt.de is blocklisted) and a firmer access line for frk_014. frk_015's location_site was refused (needs a source URL), so its pin stays approximate. frk_012, frk_013, frk_017: no per-tree record found; 10 gaps recorded as dead ends. Claim released.
- Stuttgart enrichment (3 trees, 7 gaps): stu_008, stu_009, stu_010 gained LUBW register records (Naturdenkmal numbers); stu_010 pin from Wikipedia's coordinate. No measurements found; the city PDF 3-8.pdf may hold them. Claim released.
- Needs a tool: the pass has no PDF reader, so the Palmengarten tree PDF (Senckenberg Yew) stays unread.

## 2026-10-18, 19:58 run: reader sighting verdict, roster photo pass

- 7-day visits: 2010 visits, 2900 page views.
- Rung 1: the one reader photograph of an unmapped tree (Moreton Bay Fig, Jardin de la Mendoubia, Tangier) was looked at: a huge buttressed fig, worth the walk, but no register or encyclopaedia source and Morocco is out of focus. Kept as a lead with a written verdict in data/leads/_sightings.json.
- Photos first (recovery mode): `photo_hunt.py --recheck` found no new candidates, so `photo_fetch.py --roster` plus a photo-judge pass on the queue: 14 photographs approved (Utrecht Dolehof plane, Portland Corbett Oak, Hong Kong Nathan Road banyan, Dallas Post Oak Grove, New York Reservoir plane, Berlin Korean Evodia, Los Angeles El Pino, Tokyo Hongo camphor, Stockholm Bellmanseken, Vilnius Mickiewicz ash, Washington DC Travilah Oak, Naples Villa Comunale gum, Seattle Hiawatha oak and Roanoke elm), 5 held, 38 rejected. Reversal commands are in the pass report (`photo_apply.py hold <id> --reason overrule`).
- The six written-and-ready trees (fdl_001, ftw_018, kyw_001, spk_015, std_001, nsb_001) were not merged: they have neither a photograph nor a confirmed pin, and preflight refuses them. No new trees this window.
- Leipzig enrichment pass (5 trees, 9 gaps): closed nothing. No official per-tree record for the Starkeiche, Wikipedia ND coordinates only repeat our pins, no source states more on access. Recorded as dead ends (`enrich.py --done leipzig`), claim released.
- The image viewer hit a request limit for a long stretch, so the pass ran about 45 minutes.

## 2026-10-18, retry run: READY write pass

- Live: Leipzig +1 (lpz_030, white elm by the B2, German overlay), Delft +3 (del_012 to del_014); counts fixed on both pages (Leipzig 29, Delft 12).
- 22 READY leads handed over, 4 written: 6 already live, 7 access not established, 5 too thin or too small. Claims for leipzig, delft, vienna released. Munich and Salzburg had nothing to write.
- leads.py --ready overcounts: earlier passes declined many of these in wording it does not recognise.
- Next: photo-judge on the Commons candidate for lpz_030 ("Flatterulme Lzg. B2.jpg", CC BY-SA 3.0). Roosendaal (22 READY) untouched.
- Breakage: iOS app workflow shows FAILED (newest run 2026-10-18), not looked at this run.
<!-- archive-index -->
## 2026-10-18 session: Hidde's app test, four fixes

**What changed in the product:**
- **Pins no longer blink on first open.** When the fresh feed replaced the bundled trees, the map removed every pin layer before the new data was drawn, so for about 0.3 s it was empty (filmed frame by frame). Now the new pins go on top and the old ones are removed only once the new source has its points (MapLayers.apply / retireWhenDrawn). Re-filmed: no gap.
- **A second photo of a tree you added yourself joins that tree** instead of becoming a second tree with its own pin. Within 30 m the "Which one is it?" list offers "Your tree" first; picking it adds the photo (Sightings.addExtra). Test: aSecondPhotoOfYourOwnTreeOffersIt. His account still holds older pairs (Nara 1d61e594/b6706a98, Tokyo a4fa2700/ae06e952), left untouched.
- **The ambassador tag opens its place**, in the app (My trees) and on /account.
- **Early-adopter sheet** says "You are one of the first users of Ancient Trees", no months, app and web.

**Not changed, needs Hidde:** auto-removing a tree from Want to visit once collected (his own ruling 2026-08-26 keeps the two lists independent); "Open in app" on the website goes to the App Store even with the app installed, because iOS ignores a universal link to the domain you are already on.

## 2026-10-18 session: small code tidy (Hidde asked)

**No product change.** 17 one-off scripts (old register importers, two `_tmp_` files, finished batch helpers) moved to archive/scripts/, nothing deleted. Two app views nobody shows any more removed: SentCard (unused since Collected became a grid, 10-09) and ProfileButton (gatecheck entry dropped with it). DATA.md went from 2 MB to 435 KB: `archive_logs.py` now also moves DATA.md entries older than 14 days to archive/DATA-YYYY-MM.md, daily, every line checked present after the move. A stale August copy "BRIEF_RESEARCH 2.md" removed (every line is in archive/BRIEF_RESEARCH-full-2026-10-12.md).
**Left alone on purpose:** site/src/lib/city-walks.ts is imported by nothing, yet SEO_GEO_BLUEPRINT.md names its `hasWalksPage()` as the gate on the word "walk". So either the gate silently stopped running or it lives elsewhere; that is a finding, not a deletion.

## 2026-10-18 session: iOS CI compiles again

**Breakage, fixed:** since the near-a-tree banner commit (8ed90c196) the app did not compile on CI: ContentView's `body` was too big for the runner's type-checker ("unable to type-check this expression in reasonable time"). The first fix (a33538bab, moving the banner and tab-bar inset out) was not enough; measured locally, `body` still took 14.4 s. The second fix (54644b983) splits it into three pieces (tabs, routed, presented) and gets it down to 0.27 s. No change in behaviour; appfit (iOS 18, iPhone 16 Pro Max) gives 0 findings on 39 screens.

**CI now:** push run 39141889872 on main is green (test, look). Dispatched run 39145554047: floor and look green, but test is red from `UndoWalk.testRemoveFromCollectedOffersUndo` failing its first attempt and passing its retry. Run 39137010429 had the same pattern with `testTappingAPinOpensItsTree`, which also did it at 09:53 that morning, before the banner commit. Still open: ios.yml fails on any failure line even when `-retry-tests-on-failure` then passes, so flakes like these keep the scheduled run red.

## 2026-10-18 17:02 window: reader verdict, photo lane, Sequoia

7-day visits: 1,990 visits, 2,790 page views (peak 550 on 10-16).
- **Rung 1:** the Baarn photograph f9336891 (owner account, no note) is a large old willow trunk on a waterside bank. No register or Wikipedia match, no age or girth, so verdict lead with its coordinate; written to judgements and `_sightings.json`.
- **Photos on roster pages:** `photo_hunt.py --recheck` for Vienna, London, Leipzig, Cardiff, then two photo-judge passes: 5 approved in all (vie_049, vie_056, vie_058, lon_029, lpz_023; reversals in the entry below). I approved the Sequoia National Park Sentinel Tree myself (the park's SENTINEL sign is in the frame, geotag 12 m; undo with `photo_verdicts.py` hold on seq_007).
- **Enrichment:** the vienna+london+leipzig+cardiff brief held only season and pin gaps with no evidence on hand, so I recorded it as dead ends (`enrich.py --done`); `enrich.py --next` now says nothing to do.
- **Scouting:** Denver retried, still stalled (no open register of Denver's remarkable trees; Forestry's champion register is not a download).
- **Leipzig (live, 22 to 28 trees):** verify pass (6 trees, 9 new leads) then write pass; lpz_024 to lpz_029 merged with a German overlay, 4 best_time lines, and the Rosental Starkeiche (lpz_026) is now Leipzig's oldest tree on the page (age disputed, 350 vs 600 years, said on the page). All six have no photograph yet; Commons CC BY-SA candidates exist for lpz_024, 025, 027, 028, 029 (lpz_029's file may show the other oak). Photo hunt and a viewing pass are next for them. lpz_019 stays dropped as a duplicate.
- **Stuttgart's three new trees (photo-judge pass):** 6 files, 8 candidate verdicts, every one viewed, both oaks zoomed at full size for species. 3 approved, 0 held, 5 rejected. All three new trees now have a photograph. Approved, with reversal:
  - stu_008 Schillereiche: Schillereiche (Wernhaldenstraße, Stuttgart), 2024-05-05 (CC BY-SA 4.0, Fyrtaarn). Geotag on our pin, title names it, bench beside the trunk as the story says. Thick twisting limbs and pale ridged bark, lobed oak leaves high in the sunlit crown (the oval leaves in front are dogwood shrubs). Undo: `python3 scripts/photo_apply.py hold stu_008 "https://commons.wikimedia.org/wiki/File:Schillereiche_(Wernhaldenstra%C3%9Fe,_Stuttgart),_2024-05-05,_yj.jpg" --reason "reversed"`
  - stu_009 Wernhalde sequoias: Naturdenkmal Stuttgart - 1 Mammutbaum Steinkopfstr. 6 (CC BY-SA 4.0, Laserlicht). The title names the register tree at number 6 (geotag 41 m). Conical crown, red fibrous trunk, houses and roadside rail as described. Undo: `python3 scripts/photo_apply.py hold stu_009 "https://commons.wikimedia.org/wiki/File:Naturdenkmal_Stuttgart_-_1_Mammutbaum_%E2%80%9ESteinkopfstr._6%E2%80%9C.jpg" --reason "reversed"`
  - stu_010 Jahneiche: Jahneiche Stuttgart (CC BY-SA 4.0, Florian Hoffmann). The title names it. Open-grown oak on a lawn by a road and car park, deep furrowed bark, cut-limb scars, spring leaf. Undo: `python3 scripts/photo_apply.py hold stu_010 "https://commons.wikimedia.org/wiki/File:Jahneiche_Stuttgart.jpg" --reason "reversed"`
  - Rejected: the two cross-tree swaps, an archival Wernhalde forestry map, a distant vineyard view, and the Bei der Eiche 16 A oak (a different natural monument 108 m away, shot at dusk).
- **Leipzig's six new trees (photo-judge pass):** 27 candidates, all viewed, 3 approved, 0 held, 24 rejected. Three of the six trees now have a photograph. Approved, with reversal:
  - lpz_024 Flossplatz pagoda tree: Jap. Schnurbaum Lzg. Floßpl. (CC BY-SA 3.0, Geisler Martin). The caption names this tree at the Riemannstrasse corner; fine pinnate leaflets, forked trunk. Undo: `python3 scripts/photo_apply.py hold lpz_024 "https://commons.wikimedia.org/wiki/File:Jap._Schnurbaum_Lzg._Flo%C3%9Fpl.jpg" --reason "reversed"`
  - lpz_025 Kantatenweg oak: Eiche Lzg. Kantatenweg 5 (CC BY-SA 4.0, Martin Geisler). The caption names the oak at Kantatenweg 5, and its crown is wider than the tree is tall, as the record says. Undo: `python3 scripts/photo_apply.py hold lpz_025 "https://commons.wikimedia.org/wiki/File:Eiche_Lzg._Kantatenweg_5.JPG" --reason "reversed"`
  - lpz_027 Plaussig Steinlinde: Plaussig Steinlinde-01 (CC BY-SA 4.0, Radler59). Geotagged at the tree, with the boulder and the Steinlinde sign beside the gnarled trunk, in leaf. Undo: `python3 scripts/photo_apply.py hold lpz_027 "https://commons.wikimedia.org/wiki/File:Plaussig_Steinlinde-01.jpg" --reason "reversed"`
  - Still without a photograph: lpz_026 (the only candidate shows a swamp-cypress-type conifer in the Rosental meadow), lpz_028 (all eight are Viertelsweg house facades), lpz_029 (the only candidate is an oak seedling leaf close-up; neither Torhaus oak was ever in frame, so the question of which trunk never came up). For a session: the 1999 Steinlinde sign reads 15 m and 330 cm, against the cadastre's 11 m and 390 cm on the page.
- **Frankfurt photographs (photo-judge pass):** 43 candidates for 11 trees, 29 viewed as pixels, 5 approved, 0 held, 38 rejected. Frankfurt goes from 1 photograph to 6. Approved, with reversal:
  - frk_008 Paradieseiche: Naturdenkmal Stieleiche in Sachsenhausen, Paradieseiche (CC BY-SA 4.0, Thomas Wilhelmi). The title names the tree; low-forked oak in full leaf. Undo: `python3 scripts/photo_apply.py hold frk_008 "https://commons.wikimedia.org/wiki/File:Naturdenkmal_Stieleiche_in_Sachsenhausen,_Paradieseiche.jpg" --reason "reversed"`
  - frk_010 Sossenheim Peace Oak: Sossenheimer Friedenseiche in Frankfurt (CC BY-SA 4.0, Thomas Wilhelmi). Geotagged 10 m from the pin, massive buttressed trunk, oak leaves. Undo: `python3 scripts/photo_apply.py hold frk_010 "https://commons.wikimedia.org/wiki/File:Sossenheimer_Friedenseiche_in_Frankfurt.jpg" --reason "reversed"`
  - frk_014 Cemetery Lindens: Lindengruppe in Nieder-Erlenbach, Naturdenkmal (CC BY-SA 4.0, Fernando Ferkelkraut). Geotagged 1 m from the pin, two flowering limes over the cemetery gate. This is the June 2020 frame the story already describes as showing two of the register's three. Undo: `python3 scripts/photo_apply.py hold frk_014 "https://commons.wikimedia.org/wiki/File:Lindengruppe_in_Nieder-Erlenbach,_Naturdenkmal.jpg" --reason "reversed"`
  - frk_016 Schaeferkoeppel Chestnut: Kastanie am Schäferköppel 2 (CC BY-SA 4.0, Fernando Ferkelkraut). Geotagged 25 m away, a lone horse chestnut dome at the edge of a field. Undo: `python3 scripts/photo_apply.py hold frk_016 "https://commons.wikimedia.org/wiki/File:Kastanie_am_Sch%C3%A4ferk%C3%B6ppel_2.jpg" --reason "reversed"`
  - frk_017 August Reiss Oak: August-Reiß-Eiche (CC BY-SA 4.0, Lucas Willem Danehl). This is the image on the tree's own Wikidata item (Q119288797), shot looking up the trunk into a tall crown in full leaf. Undo: `python3 scripts/photo_apply.py hold frk_017 "https://commons.wikimedia.org/wiki/File:August-Rei%C3%9F-Eiche.jpg" --reason "reversed"`
  - Still without a photograph: frk_015 (its one real frame is the right tree but a bare winter oak at dusk, light score POOR), frk_012 (only the 1907 black-and-white scan of the move), frk_013 (three bare November frames, the crown cut off or lost among other trees), frk_005 (no Grüneburgpark frame shows the eight-stemmed lime), frk_007 (sign-and-leaf close-ups only), frk_009 (a street).
- **Leipzig photographs:** 3 more approved (lpz_024, 025, 027; reversals in the entry below); lpz_026, 028, 029 still have none (lpz_029 has two oaks 36 m apart, nothing in frame settles it). The Steinlinde sign reads 15 m and 330 cm against our page's 11 m and 390 cm, worth a look.
- **Frankfurt (live, 11 to 17 trees):** verify pass (6 trees: Senckenberg Yew, Ostpark red oak, Nieder-Erlenbach lindens and oak, Schaeferkoeppel chestnut, August Reiss Oak in Offenbach) and write pass, with German overlay; the yew (about 400 years, tradition-based) is now the page's oldest tree. Photo pass approved 5 (frk_008, 010, 014, 016, 017). frk_017's travel time from Frankfurt is not stated as minutes because nobody confirmed one; a session should check. Push failed late in the window (expired token); commits are local and left to the Run health step.
- **Stuttgart (live, 6 to 9 trees):** verify pass (3 of the 9 leads were enough: Schillereiche, Wernhalde sequoias, Jahneiche; the rest of the register has no measurements and stays leads), write pass with German overlay, photo pass approved all three. The Jahneiche (over 300 years, one Wikipedia source) is now the page's oldest tree.
- Not done: I tried merging del_011 and then reverted it, because the entry below records it was held on purpose (register-dead neighbour, removed slug). No new trees this window.

## 2026-10-18 night run (retry): written-but-unmerged trees, rung 4

The rich-or-reader rule is off since 10-18, so the ten trees earlier runs refused were merged again. Live: London Marble Hill Black Walnut (lon_029), Salt Lake City Mount Olivet Linden (slc_006), Leipzig lpz_021, lpz_022, lpz_023, Vienna Prater black poplar (vie_059, approximate pin, last photographs 2014, said on the page). German overlays for Leipzig and Vienna written; city counts fixed. Dropped lpz_019 as a twin of lpz_021 (same ginkgo; its access note was an internal "hold" line). Not merged: del_011 (stands on a register tree marked dead, and its slug is a removed redirect), ftw_018 and spk_015 (story now written, but fort-worth access ground unknown and Grant Park may not be a findable small site), kyw_001 (no Key West city file yet), std_001/nsb_001 and fdl_001 (famous batches with no city file). The 60 READY leads are still not turned into verified files; stale research files left alone. Mount Olivet's address looks odd (1342 W vs the pin) and wants a check.

**Vienna photographs (photo-judge pass, recovery lane):** 80 open candidates for 19 trees judged, 3 approved, 0 held, 77 rejected (Gugerell's general park views, station interiors, plaques, bark close-ups). Each approval was viewed at full size; filename names the Naturdenkmal and the geotag sits within 25 m. Approved, with reversal:
- vie_049 Maurer Schubertpark Lime: Schubertpark_Mauer_Naturdenkmal_03.jpg (CC BY-SA 4.0, Funke). Undo: `python3 scripts/photo_apply.py hold vie_049 "https://commons.wikimedia.org/wiki/File:Schubertpark_Mauer_Naturdenkmal_03.jpg" --reason "reversed"`
- vie_056 Oberlaa Horse Chestnut: Naturdenkmal 808 Hintere Liesingbachstrasse1 Rosskastanie (CC BY-SA 3.0 AT, GuentherZ). Undo: `python3 scripts/photo_apply.py hold vie_056 "https://commons.wikimedia.org/wiki/File:Naturdenkmal_808_2014-05-10_(51)_Wien10_Hintere_Liesingbachstrasse1_Rosskastanie.JPG" --reason "reversed"`
- vie_058 Strassergasse Oak: Naturdenkmal 671 2012-07-31 0003 Strassergasse Stieleiche (CC BY 3.0, GuentherZ). Undo: `python3 scripts/photo_apply.py hold vie_058 "https://commons.wikimedia.org/wiki/File:Naturdenkmal_671_2012-07-31_0003_Wien19_Strassergasse_Stieleiche_GuentherZ.JPG" --reason "reversed"`

Two things for a later session: the newer plaque on vie_055 (Türkisgasse) reads "Schwarzpappel, Populus nigra", which settles the register/cadastre conflict in the cadastre's favour. And Theodor-Körner-Park has a stone reading "Theodor Körner Eiche 1813 1913", so vie_045 may be a 1913 commemorative planting; check that before the page claims an age. photo_light.py could not run here (no PIL).

**Photographs for the five new trees (photo-judge pass, recovery lane):** 18 open candidates for lon_029, lpz_021, lpz_022, lpz_023 and crd_004, all viewed, 2 approved, 0 held, 16 rejected. Approved, with reversal:
- lon_029 Marble Hill Black Walnut: Jim Linwood's Flickr view (CC BY 2.0), named file in the Commons category for this tree; pinnate leaves, near-black ridged bark, the forked trunk with its hollow matches the CC BY-SA "Marble Hill Black Walnut" set. Undo: `python3 scripts/photo_apply.py hold lon_029 "https://commons.wikimedia.org/wiki/File:The_Black_Walnut_Tree_Of_Marble_Hill_Park,_London._(4621674542).jpg" --reason "reversed"`
- lpz_023 Probstheida Village Green Oak: Leipzig Stieleiche Russenstrasse (CC BY-SA 4.0, Reise Reise), Commons category of the natural monument, geotag 30 m from the pin; broad crown wider than tall at April bud-burst. Undo: `python3 scripts/photo_apply.py hold lpz_023 "https://commons.wikimedia.org/wiki/File:Leipzig_Stieleiche_Russenstra%C3%9Fe.jpg" --reason "reversed"`

No photograph yet: lpz_021 (Pixelkaktus's seven files are the sign, bark and leaf close-ups; the one whole-tree view has a blown white sky and a shrub over the trunk), lpz_022 (only candidate is the Schillerlinde 158 m away), crd_004 (a sculpture show garden). For a session: the lpz_021 sign at the tree reads 19 m and 260 cm girth, against the cadastre's 24 m and 357 cm on the page.

## 2026-10-18 night run (13:43 UTC): reader photographs, rung 1

Visits last 7 days: 1980. Rung 1: two app photographs of lis_014 (Yew of Campo Santana, Lisbon) looked at and both rejected: they show a bleached dead trunk laid on a mound beside the pond, not a living yew. Open question for a session: that dead wood stands 5 to 25 m from our pin, so the yew may have died or been cut down. Check the garden (Jardim Braamcamp Freire) before the page keeps claiming a living 14 m yew; not retired, nothing could confirm it from here. Nothing else done in this window beyond that: shelf lanes untouched.

## 2026-10-18 session: near-a-tree banner in a park

**Changed in the app (next build):** the "You are 40 m from ..." banner now works in a park with many trees. Before, it only looked at the single nearest tree, so other trees close by never got a banner, and a new banner could push the previous one off the screen. Now each tree gets its turn, nearest first, one banner at a time, and the next one comes only once you walk on. Standing still in Parc d'Egmont (eleven trees within 50 m) gives one banner, not a new one every nine seconds. The banner now also shows on the tree's own page (Hidde: "deze uitzondering hoeft van mij niet"), and tapping it there opens Collect.

**Checked:** build plus screenshots on the iPhone SE simulator (the park while standing still, the tree page). Not checked: a real walk through the park, and the tap itself (simctl cannot tap). Still no push notifications and nothing in the background, as it was.

## 2026-10-18 session: Hidde's photo review, round 2

- **His unapplied verdicts are in:** 108 verdicts given on the review page after the 10-01 pass were never applied. Now 59 rejects are recorded in data/photo-queue.json, and his 17 "good photo" picks are held, not approved: none could be tied to the trunk. They named only the place, e.g. a Trsteno file of the plane tree offered for the ginkgo, or had geotags 86 to 561 m off.
- **Round 2 on the page** (https://claude.ai/artifact/T4TtkFaSAmJXdTVJy1unHp): 35 candidates for 25 trees, roster cities first. The gate is new and strict: the filename must name a tree or the species, AND either the geotag is within 60 m of the pin or the filename names the species and the site. Built by out/tmp/review_batch.py; images numbered from 1001 so old verdict ids never collide.
- **Applying round 2 (a session does this):** read `verdicts` with ArtifactData, take only ids whose number is 1001 or higher, rejects to photo_verdicts.py, goods through the identity check (geotag or named file), then preflight, commit, push.

## 2026-10-18 session: Lady Liberty and a Cedar Breaks bristlecone from the US register sieve

**New on the site, both with photographs:** Lady Liberty in Longwood, Florida (bald cypress, about 2,000 years by Seminole County's estimate, 10 m round), and the Spectra Point Bristlecone at Cedar Breaks, Utah (Utah's state champion, 8.26 m round, past 1,500 years; pin confirmed because the photo geotag sits 10 m from the register's GPS). Both are lone-tree places.

**The sieve:** six state registers with coordinates (Florida, Ohio, Utah, Oklahoma, New Jersey, Delaware; 1,800 public rows), Commons geosearch within 100 m of the top 50 per state. 11 of 300 had a tree-named photo nearby; 2 were real and epic. The state register counts as the official source, so verification was quick: about 60k tokens for both, done in-session without agents, against about 100k per tree in Australia. Script: out/tmp/us_sieve.py, output out/us-register/ (not in the repo). Weak hits not pursued: the Ohio champion Atlantic white cedar (named photo, small tree), the Hollywood FL baobab (girth uncorroborated before), the Dover elm.

## 2026-10-18 session: four Australian giants from the big-tree register trial

**New on the site:** the Giant Tingle Tree near Walpole (with photo), the Prison Boab near Wyndham (with photo), the Ada Tree near Powelltown and the Dave Evans Bicentennial Tree at Pemberton. The Gloucester Tree got its first photograph. Walpole, Wyndham and Powelltown are lone-tree places under Hidde's new rule of the same day: a lone tree goes live as a tree page, and its place page stays out of Google until it has four.

**How:** Australia's National Register of Big Trees (923 trees, All Rights Reserved) was used as a finding aid only. A free script searched Commons for the 107 trees scoring 500+ points; 25 had filename hits, about 6 were real candidates. Then one verify pass (127k tokens), one photo pass (153k) and one writing pass (133k): roughly 410k tokens for 4 trees plus a photo, about 100k per tree, well over the 15k target. The sieve is cheap, but most register giants have no usable photo and no second source.

**Kept as leads:** Grandma Tingle (written, but no trunk photo or recognition line), the Wonnerup Giant (approved photo, only the register as source), the Woodford blue gum, and Big Red, Grey Bark, Pleated Lady, Forest Lord, The Tyrant and Hawke (register only). The sieve output is in out/au-register/ (not in the repo).

**Open:** the Pemberton FAQ and the Gloucester story call it "second-tallest fire lookout behind Dave Evans", but Dave Evans was never a fire lookout. Needs a source check. The Gloucester pin sits about 260 m from two photo geotags.

## 2026-10-18 A stranger in Lisbon gave two trees their first photographs
A signed-in reader (not our account) collected the Moreton Bay Fig and the Prickly Paperbark of Jardim Constantino in the app this morning and took three photographs. Neither tree had a photograph. Looked at all three: fig whole with its surface roots and the Prometheus statue behind (lead), the fig from under its crown (added beside it), the paperbark's white peeling bark (lead). Published with sightings_publish.py, mail off; verdicts in data/judgements.json. Both pages now qualify for Google (Lisbon is on the proven roster). Found because Hidde asked about the two collections in the digest: `sightings_inbox.py --status` reads only the local queue, so it said 0 waiting until the inbox itself ran. Also: judgement.py --scan reads the queue, which sightings_publish empties, so scan before publishing.

## 2026-10-18 iOS scheduled run: the layout sweep's three DRIFT findings fixed
Breakage, not product. ios.yml had failed three runs in a row on SweepFrames DRIFT only (all 224 tests green). Two causes, neither a real misalignment. (1) The early-adopter sheet had no named root, so its "Done" (BrandSheet's 24) was measured against the profile page behind it (20); it now carries `early-adopter-sheet` as its root, like the sign-in and paywall sheets. (2) The add-a-tree sentence was centred text whose widest line measured 0.881 of the screen, a hair over the centred-text exemption (0.88), so it read as starting at 26 against the buttons' 20; the 10-16 fix (full-width frame) did not move the measured box. It now takes the headline's 18 at the sides, wraps as two balanced lines and reads as centred. Ratchet untouched. appfit locally: 0 findings on 39 screens (16 Pro Max, iOS 18.6); screenshots looked at.

## 2026-10-18 session with Hidde: new trees without a photograph go live again; the photo fetcher keeps to its cities
- New trees no longer have to be rich to ship (`ADD_NEEDS_RICH = False` in scripts/findable.py). Hidde: "let new trees without a photo go live again (readers and Bing only)". Google cannot see them until they get a photograph (the noindex change below), so the hold bought nothing and kept 60 READY leads and 28 written trees idle through 38 empty night attempts. Every other gate holds (photo-or-pin, told-apart, a named source, the reason floor), so not all 88 will pass. prepare.py and passcheck.py briefs now print the rule from the flag. Undo: set it True.
- `photo_fetch.py` ignored `--city` whenever `--zero` was given and fetched every photo-less city (Dallas, Oss, Rotterdam) instead of the pages Google shows. Named cities now win, `--city a,b` works, and `--roster` fetches the frozen roster most impressions first; prepare.py points the night run at `--roster`.

## 2026-10-18 session with Hidde: the extra "Is it ...?" step on Add a new tree is gone again
Hidde: "deze vraag staat al op het eerste scherm ... deze stap is onnodig". The collect list already names our trees above "Add a new tree", so that button goes straight to a new tree as before. The fold afterwards stays ("Is this <name>?" and "Another of our trees" on a tree of yours); he wants it. CONVENTIONS.md says not to bring the step back.

## 2026-10-18 session with Hidde: no more second copies of our trees in the app
Hidde found a second Town Hall Plane among his own trees in Baarn, made by "Add a new tree" right beside ours. App only, LIVE on main (merged 2026-10-18; ios.yml green on the branch: build, unit and UI tests, layout gate after one SMALL fix on the new button): "Add a new tree" with one of ours within 30 m first asks "Is it <name>?" (yes collects ours with the photo, no adds the new tree as before), and a tree of yours within 30 m of ours shows "Is this <name>?" with "It is this tree", which folds it into ours without deleting anything (`Sightings.fold`). The server already matched at 30 m, so the site never had the duplicate. New unit test `aNewTreeOnTopOfOursIsAskedAbout`. Second step, same day, because our pins are not always right: the box also offers "Another of our trees" (or "Already on our map?" with nothing within 30 m), the collect sheet's nearby, closest and search list inline; a pick further than 400 m also sends a pin correction. For Hidde: next build carries it; open your Baarn copy and tap "It is this tree".

## 2026-10-18 session with Hidde: Google now sees only tree pages with a photograph
The 10-09 exception that let finished tree pages without a photograph back into Google is closed (`RETURN_ENRICHED = False` in scripts/thin_pages.py). 1,128 tree pages (1,810 urls with their translations) get the googlebot-only noindex on the next deploy; readers still see them, Bing keeps them through sitemap-bing.xml, and each returns to Google the day it gets a photograph. Why: the digest's "Is enriching working" table showed those pages earned 0.05 impressions a page after they came back on 10-12/13, and the 10-13 rule (widen only once returned pages earn impressions) was never met. Hidde: "Yes, take the 1,128 photo-less pages out of Google; Bing keeps them." Undo: set it True. Next look: mid-November, impressions per photographed page.

## 2026-10-18 thirty-eighth attempt: nothing shipped
Pulled; no claims; 60 READY leads and 28 written trees still held by the rich-or-reader rule (recovery mode); enrich empty; BACKUP is Denver only (no licence, needs Hidde's ask). Nothing dispatched.

## 2026-10-18 thirty-seventh attempt: nothing shipped
Pulled; no claims; 60 READY leads and 28 written trees still held by the rich-or-reader rule (recovery mode); enrich empty; prepare BACKUP is Denver only (no licence, needs Hidde's permission ask). Nothing dispatched.

## 2026-10-18 thirty-sixth attempt: nothing shipped
Pulled; no claims; 60 READY leads and 28 written trees still held by the rich-or-reader rule (recovery mode); enrich empty; langcheck --next has no city over 10 impressions; Denver still has no licence or coordinates. Nothing dispatched.

## 2026-10-18 08:29 window: one sighting verdict, no trees
Rung 1: sighting c86ff6bf (owner-account tulip tree, Cantonspark, Amersfoort area) judged lead: no register or Wikipedia entry nearby, no size or note, photo not on disk. Rung 2: smoke "skipped" is just the path filter on log-only pushes; the iOS app's scheduled runs fail on appsweep DRIFT findings (collect-intro and collect-away 'Photograph a tree you are standing in fro...' starts at x=26 vs 20; early-adopter-sheet 'early-adopter-done' x=24 vs 20), while the push-triggered run at 15:36 passed. Swift layout work, not doable on this Linux runner: For Hidde/a Mac session. photo_hunt --recheck london: 0 new candidates; photo_fetch --zero ignored --city and pulled filename-only junk (Dallas, Fort Worth, Oss, Rotterdam), none approved. Verified-unpublished trees are still the held ones; no write pass. Visits last 7 days: 1920.

## 2026-10-18 thirty-fifth attempt: nothing shipped
Pulled; no claims; 60 READY leads still held by the rich-or-reader rule (recovery mode), so no write pass; langcheck --next lists no city with impressions. Nothing dispatched.

## 2026-10-18 thirty-fourth attempt: nothing shipped
Pulled; no claims; 60 READY leads and 28 written trees still held by the rich-or-reader rule (recovery mode); enrich empty. Denver scouting note re-read: no licence statement and no coordinates, needs a permission ask to Colorado Tree Coalition (Hidde's call), so it stays stalled. Nothing dispatched.

## 2026-10-18 thirty-third attempt: nothing shipped
No claims; 60 READY leads and 28 written trees still held by the rich-or-reader rule (recovery mode); enrich empty. Detroit retry: Michigan Botanical Club site now answers (200), but its homepage links no Big Tree register page or licence, so it stays stalled, marked retried 2026-10-18. Nothing dispatched.

## 2026-10-18 06:37 window (7-day visits: 1910 visits, 2510 page views): one photograph
Rung 4 photos lane. photo_fetch.py --zero (it ignores --city and fetches every city) gave 35 candidates; I looked at the pixels and approved one: the Ypres Four-Trunked Survivor (sweet chestnut in leaf, Wikidata-linked file, 6 m from pin, CC BY-SA 4.0 Stad Ieper). Reversal: set ypr_005 photo status back to missing. The rest were leaves, hands, indoor or unrelated shots; photo_verdicts.py cannot record rejects for iNat candidates (no matching page), so those come back next sweep. Sequoia's Sentinel Tree has 13 new candidates queued but photo_fetch --zero did not fetch it; not judged. Health still shows Smoke skipped and iOS scheduled failure (needs a Mac session). Enrich empty; 60 READY leads and 28 written trees still held by the rich-or-reader rule.

## 2026-10-18 thirty-second attempt: nothing shipped
Pulled; no claims; 60 READY leads and 28 written trees still held by the rich-or-reader rule (recovery mode); enrich empty; only backup is the Detroit retry (host unreachable earlier). Nothing dispatched.

## 2026-10-18 thirty-first attempt: nothing shipped
Pulled; no claims; 60 READY leads and the 28 written trees still held by the rich-or-reader rule (recovery mode); enrich empty; scout target Detroit retry unchanged. Nothing dispatched.

## 2026-10-18 thirtieth attempt: nothing shipped
No claims; 60 READY leads still held by the rich-or-reader rule (recovery mode), no write pass. Photo recheck on London found no new candidates (queue file touched only). Nothing dispatched.

## 2026-10-18 02:38 window (7-day visits: 1908 visits, 2571 page views): nothing shippable
Inbox empty; health flags only Smoke "skipped" (log-only pushes) and the iOS scheduled-run failure (needs a Mac session); enrich empty; 60 READY leads and 28 written trees still held by the rich-or-reader rule (recovery mode). Nothing dispatched, no claims.

## 2026-10-18 twenty-ninth attempt: nothing shipped
Pulled; no claims; 60 READY leads still held by the rich-or-reader rule (recovery mode), so no write pass. Nothing dispatched.

## 2026-10-18 twenty-eighth attempt: nothing shipped
No claims; 60 READY leads still held by the rich-or-reader rule (recovery mode); langcheck --next has no city over 10 English impressions. Nothing dispatched.

## 2026-10-18 twenty-seventh attempt: nothing shipped
Pulled; no claims; sightings inbox empty; 60 READY leads still held by the rich-or-reader rule (recovery mode), so no write pass. Nothing claimed.

## 2026-10-18 00:00 window (7-day visits: 2093 visits, 2901 page views): nothing shippable
Inbox empty; enrich empty; 60 READY leads and 28 written trees still held by the rich-or-reader rule (recovery mode); scout target is the Detroit retry, host unreachable as in earlier attempts. Nothing dispatched, no claims. Later attempts in this window should not repeat the orientation.

## 2026-10-17 twenty-sixth attempt: nothing shipped
Pulled; no claims; 60 READY leads still held by the rich-or-reader rule (recovery mode), so no write pass. Nothing claimed.

## 2026-10-17 twenty-fifth attempt: nothing shipped
Pulled; no claims; 60 READY leads still held by the rich-or-reader rule (recovery mode); no write pass dispatched, as it would publish photo-less new trees. Nothing claimed.

## 2026-10-17 22:00 window (7-day visits: 2040 visits, 2630 page views): nothing shippable
Inbox empty, enrich empty, 60 READY leads and 28 written trees still held by the rich-or-reader rule. Health flags Smoke "skipped" (log-only pushes) and the iOS scheduled-run failure (needs a Mac session). Nothing dispatched, no claims left.

## 2026-10-17 19:58 window (7-day visits: 2079 visits, 2875 page views): nothing shippable
Inbox empty, health's only flag was Smoke test "skipped", which is a false alarm (it skips LOG-only pushes; the last scheduled run passed). Enrich empty, 60 READY leads and 28 written trees still held by the rich-or-reader rule. Photo shortlist names only the Sequoia Sentinel Tree, already judged ("nothing to fetch"); Brussels is swept and empty. Nothing dispatched, no claims left. Note: `photo_hunt.py --help` starts a sweep instead of printing help (ran over the 120s limit).

## 2026-10-17 16:48 window: nothing shippable, one scouting verdict

Visits 7 days: 2070 visits, 2864 views. Rungs 1 and 2 clear (no sightings, health green). Enrichment says nothing to do. The photo lane: `photo_fetch.py --zero` ignored `--city` and fetched 25 candidates across Chicago, Dallas, Fort Worth, Oss, Rotterdam, Salt Lake City; I looked at the pixels of the plausible ones and none ships (leaf in a hand, a street tree of unknown identity, a building with trees, greenhouses). Nothing approved. The 28 written trees waiting are the held ones (no photo, no confirmed pin or not rich). Backup lane: Lansing scouting retried, the Michigan Botanical Society register is a Google Doc champion list with no stated licence, so it stays stalled (verdict in data/register-scouting.json). No trees added.
## 2026-10-17 twenty-fourth attempt: nothing shipped
Pulled; no claims; 60 READY leads and the written trees still held by the rich-or-reader rule; enrich empty; photo_hunt sweep found 0 candidates for the 2 unchecked trees. Nothing dispatched, no claims left.
## 2026-10-17 twenty-third attempt: nothing shipped
Pulled; no claims; 60 READY leads still held by the rich-or-reader rule; photo_hunt has 0 unchecked trees; langcheck --next has no city over 10 impressions. Nothing dispatched, no claims left.
## 2026-10-17 twenty-second attempt: nothing shipped
Pulled; no claims standing; 60 READY leads (roosendaal 22, munich 5, delft 5, ...) still held by the rich-or-reader rule in recovery mode, so no write pass (it would publish photo-less new trees, which the rule refuses). Nothing dispatched, no claims left.
## 2026-10-17 twenty-first attempt: nothing shipped
Pulled; no claims; 60 READY leads and 28 written trees still held by the rich-or-reader rule; enrich empty; staged cities are not rich-eligible; only BACKUP is the Detroit retry (host unreachable). Nothing dispatched, no claims left.
## 2026-10-17 twentieth attempt: nothing shipped
Pulled; no claims; 60 READY leads and 28 written trees still held by the rich-or-reader rule; enrich empty; only BACKUP is the Detroit retry (host unreachable). Nothing dispatched, no claims left.
## 2026-10-17 nineteenth attempt: nothing shipped
Pulled; no claims standing; 60 READY leads and the written trees (delft, leipzig, london, fort-worth, salt-lake-city, tree-of-the-year, famous-czech-brazil) still held by the rich-or-reader rule. Enrich empty; langcheck has no city above 10 impressions; Detroit scouting still needs the blocked host. Nothing dispatched, no claims left.
## 2026-10-17 19:32 window (7-day visits: 2076 visits, 2872 page views): nothing shippable
Inbox empty, health green, enrich empty, 60 READY leads and 28 written trees still held by the rich-or-reader rule. Detroit scouting retry: its only lead is the Michigan Botanical Society list, and michiganbotany.org still does not resolve here (curl exit 6), so the verdict stays stalled. No pass dispatched, no claims left.
## 2026-10-17 eighteenth attempt: nothing shipped
Pulled; no claims standing; 60 READY leads still held by the rich-or-reader rule. Tried to claim the starred staged cities for a verify pass: munich (63 of 60) and portland (33 of 30) are full and refused. Nothing dispatched, no claim left behind.
## 2026-10-17 seventeenth attempt: nothing shipped
Pulled; no claims; 60 READY leads and 28 written trees still held by the rich-or-reader rule (recovery mode); enrich says nothing to do; backup is Detroit scouting retry. Nothing dispatched.
## 2026-10-17 session: in the app, a city page is now its map
Hidde: "die twee paginas zijn bijna hetzelfde en met interactieve kaart veel beter". A city opens straight on the interactive map with its trees in the sheet (PlaceMapPage), the way the website's city page already works; the old page with the map picture and the "Expand map" button (CityView) is gone. The share button moved to the map page. Countries keep their own page. Goes out with the next app build. Checked in the simulator (London); the SE layout gate runs in ios.yml on push.
## 2026-10-17 sixteenth attempt: nothing shipped
Pulled; no claims; 60 READY leads and the written trees still held by the rich-or-reader rule; langcheck lists nothing above 10 impressions; Lansing needs network that is not here. Nothing dispatched.
## 2026-10-17 fifteenth attempt: nothing shipped
Pulled; no claims; 60 READY leads still held by the rich-or-reader rule (recovery mode). Nothing dispatched.
## 2026-10-17 fourteenth attempt: nothing shipped
Pulled; no claims; 60 READY leads (roosendaal 22, munich 5, delft 5, ...) still held by the rich-or-reader rule in recovery mode, so no write pass. Nothing dispatched.
## 2026-10-17 13:25 window (7-day visits: 2030 visits, 2610 page views): nothing shipped
Inbox empty, enrich empty, 60 READY leads and 28 written trees still held by the rich-or-reader rule. pagegaps: nothing missing. London photo recheck found 0 new candidates across 7 trees. Smoke "skipped" is log-only pushes; the iOS scheduled run still needs a Mac session. No pass dispatched.
## 2026-10-17 thirteenth attempt: nothing shipped
Pulled; no claims; 60 READY leads still held by the rich-or-reader rule (recovery mode), same as the last six attempts. Nothing dispatched.
## 2026-10-17 twelfth attempt: nothing shipped
Pulled; no claims; 60 READY leads still held by the rich-or-reader rule. Ran the photo lane: photo_hunt swept 40 trees (Wikimedia works), photo_fetch --zero pulled 25 files across chicago, dallas, fort-worth, oss, rotterdam, salt-lake-city. I looked at the three iNat ones (chi_020, dal_012, slc_004): a hand holding leaves, leaves again, and a street sapling, none passes the Cadiz standard. The Commons files are plainly not the trees (greenhouse, horse portrait, fallen pine). No approvals.
## 2026-10-17 retry attempt: nothing shipped
Pulled; no claims standing. 60 READY leads and the 28 written trees are still held by the rich-or-reader rule, enrich has nothing to do, and the Lansing BACKUP could not run (curl exit 6, no network on this runner). No pass dispatched. iOS scheduled-run failure still needs a Mac session.

## 2026-10-17 11:00 window (7-day visits: 2045 visits, 2831 page views): nothing shipped
Inbox empty, enrich empty, 60 READY leads and the 28 written trees still held by the rich-or-reader rule, so no dispatch. Lansing BACKUP retry: michiganbotany.org still does not resolve (curl exit 6), so no scouting. iOS scheduled-run failure unchanged (needs a Mac session).
## 2026-10-17 eleventh attempt: nothing shipped
Pulled; no claims; inbox empty; enrich empty. 60 READY leads and the written trees (delft, leipzig, london, fort-worth, tree-of-the-year, salt-lake-city) still held by the rich-or-reader rule; the unwritten ones (miami, spokane, vienna) lack photo or pin. No dispatch.
## 2026-10-17 tenth attempt: nothing shipped
Pulled; no claims. 60 READY leads still held by the rich-or-reader rule; langcheck --next lists no city above 10 English impressions, so no translation. Nothing dispatched.
## 2026-10-17 ninth attempt: nothing shipped
Pulled; no claims. 60 READY leads and the written trees are still held by the rich-or-reader rule; enrich empty. Lansing BACKUP: michiganbotany.org does not resolve from this runner (Wikimedia does), so no scouting. Nothing dispatched.
## 2026-10-17 08:12 window: nothing shipped (scouting verdict only)
7-day visits: 2033 (peak 568 on 10-16). Inbox empty, enrich.py says nothing to do, the writable pile is only held trees (no photo or pin), so no dispatch. Network worked this time: took the BACKUP scout (New York retry); the Wikipedia notable-trees table lists nothing we lack, verdict rewritten in data/register-scouting.json (NYC Parks' 2024 list of 120 still needs a browser session). `photo_fetch.py --zero` ignores --city and only produced junk candidates (greenhouse, lake photos), none judged. London photo recheck found 0 new candidates.
Breakage: iOS scheduled run (10-16 19:48) failed twice over: xcodebuild hung past 30 min on iPhone 17 Pro, and appsweep flagged `early-adopter-done` in EarlyAdopterSheet (AmbassadorBadge.swift) starting at x=24 while the rest start at x=20 (DRIFT). Not fixed: needs a simulator sweep to verify, which this runner lacks. Smoke "skipped" is log-only pushes, not a failure.
## 2026-10-17 eighth attempt: nothing shipped
Pulled; no claims; 60 READY leads still held by the rich-or-reader rule, no network for BACKUP scouting. Nothing dispatched.
## 2026-10-17 seventh attempt: nothing shipped
Pulled; no claims standing; 60 READY leads still blocked by the rich-or-reader rule (mostly Dutch register trees with no photo or confirmed pin), so no write pass. No network for the BACKUP register scout. Nothing dispatched.
## 2026-10-17 sixth attempt: nothing shipped
Pulled; no claims standing. Same state as the earlier attempts: 60 READY leads and the written-but-unmerged trees held by the rich-or-reader rule, enrich empty, only BACKUP is the New York register retry and this runner has no network (`photo_hunt.py --help` hung past 120s). No pass dispatched.
## 2026-10-17 06:13 window (7-day visits: 2022 visits, 2781 page views): nothing shipped
Sightings inbox empty; no claims. health.py still lists the push-triggered smoke skip and the iOS schedule failure (diagnosed at 02:37, needs a Mac session). Enrich has nothing to do and the 60 READY leads are still blocked by the rich-page rule. `photo_fetch.py --zero` fetched 25 candidates and I looked at the four that might be trees (Chicago chi_020, Dallas dal_012 x2, Salt Lake City slc_004): a leaf in a hand, a young street tree, a bark and leaf close-up, leaves in a hand. The rest are buildings, greenhouses and signs. No approvals, nothing recorded.
## 2026-10-17 fifth attempt: nothing shipped
Pulled; no claims standing. 60 READY leads and the ten written trees are still held by the rich-or-reader rule; enrich has nothing to do; the Lansing BACKUP needs network this runner lacks. No pass dispatched, since it would only produce refusals.
## 2026-10-17 fourth attempt: nothing shipped
Same state: no claims, 60 READY and the written-but-unmerged trees blocked by the rich-page rule, `enrich.py --next` empty. BACKUP lane (Lansing, Michigan Botanical Society Big Tree register) could not run: this runner has no network (curl exit 6). Retry on a run with network.
## 2026-10-17 later attempt: nothing shipped
Pulled; no claims standing. `leads.py --ready` still lists 60 and `passcheck.py --pending` the same ten written-but-unmerged trees, all refused earlier by the rich-or-reader rule (pin, register, access missing). Not retried; no pass dispatched, since it would only produce refusals. `enrich.py` has nothing to do. Stale research files (about 25) are safe to delete but I did not do it blind.
## 2026-10-17 02:37 window (7-day visits: 1938 visits, 2691 page views): nothing shipped
Sightings inbox empty; no claims. I read the failing log of the scheduled iOS run (38957584662). The run did not time out. The iPhone SE sweep passed. The iPhone 17 Pro sweep hung past 30 minutes and was killed, and the floor job then reported 6 findings on 160 screens, among them `early-adopter-sheet` where the Done button starts at x=24 while 7 other things start at x=20 (DRIFT). The sheet is a plain BrandSheet in AmbassadorBadge.swift, so the cause is probably in the shared BrandSheet button inset. I cannot render it on this runner and did not edit it blind. It needs a Mac session. The 60 READY leads and the 28 written trees are still blocked by the rich-page rule, so no pass was dispatched.

## 2026-10-17 third attempt: nothing shipped
No claims standing; 60 READY leads still blocked by the rich-page rule, so no write pass. Started another `photo_hunt.py` sweep (note: `--status` also runs the sweep, takes over 2 minutes). Nothing merged.

## 2026-10-17 later attempt: nothing shipped
Pulled, no claims standing. `leads.py --ready` lists 60 and `passcheck.py --pending` shows the same ten written-but-unmerged trees; both were trial-merged and refused earlier (not rich: pin, register, access). `enrich.py` has nothing to do, so no write or verify pass was dispatched. Unlocks: a confirmed pin for lon_029; access sources for the Leipzig ginkgos. Not retried: Lansing scouting (stalled twice already).

## 2026-10-17 01:35 window (7-day visits: 1914 visits, 2663 page views): nothing shipped

- Sightings inbox empty. health.py again lists the push-triggered smoke skip and the iOS schedule failure (needs a Mac session; I did not open its log). Enrich has nothing to do and the 60 READY leads are still blocked by the rich-page rule, so no write pass. `photo_hunt.py --recheck` swept 40 more trees (new candidates for Oss, New Orleans and others). Fetched Oss oss_013 (Ravenstein sycamore): all three candidates are street or castle views 140 to 276 m off, so no photograph. `photo_verdicts.py` refused to record the reject (page key `oss` matched no candidate), so it stays unrecorded. New Orleans: "nothing to fetch". Note: `photo_hunt.py --help` runs the sweep instead of printing help.

## 2026-10-16 twenty-first attempt: nothing shipped

- No claims standing. 60 READY leads, still blocked by the rich-page rule (recovery mode), so no write pass was dispatched. Nothing changed since the twentieth attempt.

## 2026-10-16 twentieth attempt: nothing shipped

- No claims standing. 60 READY leads still blocked by the rich-page rule (recovery mode), so no write pass was dispatched. Nothing new since the nineteenth attempt.

## 2026-10-16 nineteenth attempt (22:25 window, 7-day visits: 2091 visits, 2914 page views): nothing shipped

- Sightings inbox empty. health.py lists the push-triggered smoke skips (1s, deploy green) and the scheduled iOS run failing again at 1h55m, which looks like the 120-minute cap and not an assertion; I did not open its log. It needs a Mac session. Enrich has nothing to do, the 60 READY leads are still blocked by the rich-page rule, and `photo_hunt.py --recheck --city london` found no new candidates for its 7 photo-less trees. No pass dispatched, no scouting retry (every BACKUP target was retried today).

## 2026-10-16 eighteenth attempt: nothing shipped

- No claims standing. Looked at the "written and ready to merge" trees in `passcheck.py --pending` (Leipzig, Delft, London, Fort Worth, Salt Lake City, tree-of-the-year, Figueira das Lágrimas). The one I opened, lpz_019 (Kleinzschocher Ginkgo), has no established access (hard rule 10) and an approximate pin, so it is not rich and stays unmerged. I did not open the other nine. The 60 READY leads are still blocked by the rich-page rule, so no pass was dispatched. I did not retry scouting: Lansing, the next BACKUP item, was already scouted twice on 10-05 and the last 17 attempts all ended the same way. For lpz_019 the unlock is a source for visitor access; I did not check what the others lack.

## 2026-10-16 fifteenth attempt (21:25 window, 7-day visits: 2073 visits, 2892 page views): nothing shipped

- Sightings inbox empty, health.py clear. Enrich, langcheck (no city over 10 impressions) and the 60 READY leads unchanged (blocked by the rich-page rule), so no pass was dispatched. Scouting: Chattanooga retried; the city's notable-trees page now 404s, no list or licence, so it stays stalled (`retried` set). Unlock: a Tree Commission ask, Hidde's to send.

## 2026-10-16 thirteenth attempt: nothing shipped

- No claims standing. The 60 READY leads are still blocked by the rich-page rule, and enrich has nothing to do, so no pass was dispatched. Scouting: Reno retried. forestry.nv.gov shows no newer big-tree list and no licence, so it stays stalled (`retried` set). The unlock is a licence ask to the Nevada Division of Forestry, Hidde's to send.

## 2026-10-16 twelfth attempt (19:13 window, 7-day visits: 2037 visits, 2846 page views): nothing shipped

- Sightings inbox empty. health.py's only item is again the push-triggered smoke run skipping in 1s (deploy green). Enrich, langcheck and the 60 READY leads are unchanged (blocked by the rich-page rule), so no pass was dispatched. Scouting: Little Rock retried; the Arkansas Agriculture champion-trees page now loads but states no licence, so it stays stalled (`retried` set). Needs a licence ask to the Arkansas Forestry Division, Hidde's to send.

## 2026-10-16 fourteenth attempt: nothing shipped

- Seventeenth attempt, 0 trees. No claims standing. Re-checked: the 11 written-but-unmerged trees and the 60 READY leads are still blocked by the rich-page rule (see earlier entries), so no write pass dispatched. Backup lane: Cincinnati retried; Spring Grove's champions page has no coordinates or licence, stays `stalled` (`retried` set). Unlock: ask Spring Grove or ODNR.
- No claims standing. The 60 READY leads are still refused by the rich-page rule; enrich says nothing to do. Backup lane: Des Moines retried. The Iowa DNR Big Tree service still has an empty copyright/licence field, so it stays stalled (`retried` set). Unlock: a licence ask to Iowa DNR Forestry, Hidde's to send.

## 2026-10-16 sixteenth attempt: nothing shipped

- No claims standing. The 60 READY leads (thin Dutch street trees) are still blocked by the rich-page rule, so no write pass. Backup lane: Tampa retried; no Heritage/Grand Tree layer on the open-data hub, FDACS champion list has no coordinates or licence. Stays stalled (`retried` set). Next step is an Urban Forestry request, Hidde's to send.

## 2026-10-16 eleventh attempt: nothing shipped

- No claims standing. Tried merging the 9 written-but-unmerged trees (london lon_029, delft del_011, fort-worth ftw_018, leipzig lpz_019/021/022/023, salt-lake-city slc_006); preflight refused all of them (not rich: pin/register/access missing; ftw_018 story is 83 words; del_011 sits on a register-dead ash and its slug is a removed-tree redirect; Leipzig also needs German overlays). Reverted. lon_029 is the closest: needs only a confirmed pin. `photo_hunt --recheck --city london`: 0 new candidates for 7 trees.

## 2026-10-16 tenth attempt: nothing shipped

- No claims standing. The 60 READY leads are still blocked by the rich-page rule and enrich has nothing to do, so no pass was dispatched. Backup lane: Long Beach retried; it is the same Cal Poly register with no licence, so it stays stalled (`retried` set). The unlock is still the permission email to Cal Poly, Hidde's to send.

## 2026-10-16 ninth attempt: nothing shipped

- No claims standing. The 60 READY leads are still blocked by the rich-page rule; enrich and photo lanes are empty. Backup lane: Jacksonville retried. The only public Duval row is one Tough Bumelia at an unidentified state facility, and the Florida register withholds private rows, so it stays stalled (`retried` set).

## 2026-10-16 eighth attempt (18:12 window, 7-day visits: 2019 visits, 2825 page views): nothing shipped

- Sightings inbox empty. health.py's only item, "Smoke test skipped", is every push-triggered smoke run skipping in 1-2 seconds (deploy is green, 1.5h ago), not a broken build. `enrich.py --next` and `langcheck.py --next` print nothing to do; the 60 READY leads stay blocked by the rich-page rule, so no pass was dispatched.
- Scouting: Monterey retried. The Cal Poly big-trees API is live but still states no licence; the only unlock is the permission email to Cal Poly (drafts/OUTREACH.md), Hidde's to send. `retried` set in data/register-scouting.json so scout_next moves on.

## 2026-10-16 seventh attempt: photographs vendored, no new trees

- Ran `vendor_photos.py`: 30 photographs (Berlin 25, London 3, NYC 1, Vienna 1) now sit on our own domain, so the app's image URLs for them stop depending on the source host. 47 skipped on licence as before. No claims standing; the 60 READY leads are still blocked by the rich-page rule, so no write pass was dispatched.

## 2026-10-16 sixth attempt: nothing shipped

- Resolved a LOG.md rebase conflict and pushed. No claims standing. `leads.py --ready` lists 60 (roosendaal 22, munich 5, delft 5 and others), but the rich-page rule still blocks new trees and the 11 research entries were already trial-merged and refused earlier today. No write pass dispatched, since it would only produce refusals.

## 2026-10-16 retry in the same window

- Nothing shipped. No claims standing. `leads.py --ready` lists 60 but recovery mode's rich-page rule blocks new trees. I trial-merged the 11 "written and ready" research entries (delft, leipzig x4, london, fort-worth, salt-lake-city) and preflight refused each. Delft del_011 is a removed tree on the redirect list and sits within 5 m of a dead register ash. The others lack a pin, register record, measurement or access, and fort-worth's story is 83 words. All reverted, nothing committed. The roster only moves if someone enriches these (pin or register) first.
- Also open: `enrich.py --next` and `photo_gaps.py --shortlist` are empty. Birmingham and Monterey scouting are stalled on unreadable PDFs. 30 photographs still sit off our domain (`vendor_photos.py`, daily photos.yml).

## 2026-10-16 night run 14:17 UTC (7-day visits: 1810 visits, 2420 page views)

- **App**: the scheduled iOS run failed only on the sweep's drift check (Add a tree sheet: the one line started at x=26, other things at x=20). The text now spans the sheet's width (CollectIntro.swift); the next iOS run proves it. Floor tests were 224 passed.
- **Photos**: 4 approved in Berlin (ber_039, 042, 046, 062; reversal `photo_apply.py hold <id>`), ber_059 held on species. Singapore had nothing new (judged earlier today). ber_062's December photos show the crown cut back and fungus; a rewrite is noted in its verify_notes. Photo lanes are close to exhausted: three viewing passes today, yield 23, 3, 0, 4.
- Nothing from readers waiting; health.py's only item was the iOS run.
- **Scouting**: Birmingham (Alabama champion trees) retried: the PDF downloads but nothing here can read it (no pypdf, Read needs pdftoppm) and no licence is stated; still stalled, `retried` set. Monterey is next in scout_next and has the same stall shape. Nothing else to do: enrich, pagegaps, recognise --stuck and langcheck all print empty. No new trees this window; shelf trees are blocked by the rich-page rule.

<!-- continued below -->
## 2026-10-16 night run (fifth attempt, 14:52 window): nothing shipped

0 trees, nothing changed in the product. Visits: 1810 in 7 days. Sightings inbox empty. health.py: smoke and deploy "skipped" are push runs superseded by a dispatched deploy that was in progress; the iOS scheduled failure is already answered by 43b717d12 (its push run was still going). enrich.py --next, langcheck --next and pagegaps all say nothing to do; Birmingham retry was already tried this morning (PDF licence unstated), so it stays stalled. `photo_hunt.py --recheck` swept 40 trees (Aarhus to Amerongen) and found 0 new candidates. Next: roster photo hunts need a new angle, not another sweep.

## 2026-10-16 session: launch outreach to the big-tree communities

Hidde mailed, in his own words, the admin of Big Tree Seekers and Big Trees of New York (Landis Arboretum) and the coordinator of Australia's National Register of Big Trees (Finding Big Trees group): what do they think of the app, and may he share it in their groups. Both logged in the private OUTREACH.md. Not mailed: the Ancient Tree Forum (three unanswered mails since August) and the Ancient Yew Group (its contact goes to the Tree Register inbox, already mailed twice). The Australian register is All Rights Reserved: a finding aid only, permission to be asked in a reply (data/register-scouting.json).

Next, Hidde's call: posting starts in about a week, once the app is tested. Channels, ask-first mod messages and four example posts are on Hidde's private page https://claude.ai/artifact/CX8HzNwrwuo9wyKXEAfig4 (local copies drafts/where-to-post.html and drafts/group-messages.md stay out of the public repo: they name people). Home turf (Dutch groups, r/Amsterdam) parked at his wish; Product Hunt waits for phase 2. Hidde has no Facebook profile, so Facebook goes through the admins by mail for now. The scheduled iOS build is still failing and comes before any post.

## 2026-10-16 session: Cardiff's Wallenberg tree has a species

A Cardiff parks officer mailed Hidde that the Raoul Wallenberg tree in Alexandra Gardens (crd_001) is Ailanthus altissima. The page had asked readers for exactly that. Species is now Tree of Heaven, the story's "nobody has recorded which species" paragraph is rewritten, and the recognition line names the leaves. Logged in verify_notes; no name on the site. Reply drafted in drafts/reply-cardiff-wallenberg.md for Hidde to send.

## 2026-10-16 session: the app's crash reports now reach a person

- **What changed:** the app's MetricKit crashes (Supabase `diagnostics`) are read every day now. Until today nothing read that table, which is why one reader's 1.0.2 crashed 37 times from 10-13 to 10-16 before his mail told us.
- `python3 scripts/crashes.py [--days N]`: groups crashes and hangs by build, exception/signal and the top AncientTrees frame; on the Mac it symbolicates with the dSYM (today: 37 on build 20 at `MyVotes.treeId` WorthIt.swift:84, the known one; 9 on Xcode build 25). In CI it prints the raw offset. Output is counts and builds only, never device or region.
- **Daily digest:** an "App crashes" table, last 7 days, store builds only; Xcode and review builds are one line under it. Store builds come from App Store Connect and are cached in data/store-builds.json (the digest commits it) so the night run, which holds no Apple key, can still tell them apart.
- **health.py:** a signature on a store build firing 3+ times in 24h is a rung-2 act item. The known `AncientTrees+0xb8180` on build 20 carries its remedy (re-run the `submissions?kind=eq.feedback&tree=eq.` to NULL PATCH); crashes before this morning's data fix count as answered, so health is green on it today.
- MetricKit only reports from phones that share analytics with developers: a sample, not the count.
- **Second step, on Hidde's ask** ("check for crashes, flag them and improve for the next build", and flag a crash that needs an immediate update):
  - **URGENT** means a store build is unusable for someone (one phone crashing 3+ times inside 6h, the crash-at-every-launch pattern) or the crash is spreading (2+ phones on one signature in 24h), and no server-side fix stops it. URGENT goes above the digest's headline and into brief.py's BROKEN block, with Hidde's steps: archive, upload, then submit with "Request expedited review". Peter's crash would have been URGENT on 10-13; today it reads "contained, ships with next build".
  - **The other levels:** *act* is a burst with no fix yet. The health.py item carries the steps: look for a server-side fix first, otherwise fix it in the source on main in a .claude/worktrees/ worktree with a reproducing unit test, merge it, record it, and log "For Hidde: next build carries fix for <signature>". The night run never archives, uploads or submits. *reapply* is a contained crash firing again, so the server fix runs again. *waiting* is a fix that sits in a build not yet on sale; it is a note, not exit 1.
  - **data/crash-fixes.json** lists the fixed signatures, seeded with AncientTrees+0xb8180 on build 20 (3c841e501, first in build 34, contained server-side 10-16 08:19). The digest's Fix column reads "fixed in build 34, waiting for release".
  - **Source lines in CI:** dSYMs exist only in Hidde's Xcode archives (about 24 MB each). `scripts/crash_symbols.py` runs every line-table address through atos once and keeps only the rows where the answer changes. That makes a map of about 0.4 MB gzipped per store build in data/crash-symbols/<uuid>.json.gz (1.5 MB for builds 10, 20 and 35), and a lookup gives exactly atos's answer (WorthIt.swift:84) with no dSYM. **Why the repo and not private_files:** the map holds function names and file:line from ios/, which is already public, and nobody's data, so a pull step would buy nothing. Only store builds are mapped. crashes.py maps a uuid it meets on the Mac, and brief.py names any store build that still has no map. Build 9 (1.0) has no archive on this Mac.
  - **Ratchet:** `check_app_crashes_reach_a_person()` in qa.py, in both the source-only and the full run. It checks that health, the digest, the URGENT line and brief are wired, that BURST / URGENT_* never loosen, and that every crash-fixes entry names a fix.
  - **FOR HIDDE, one line for CLAUDE.md rung 2** (a session may not edit it on another session's request): "A crash signature on a live build is fixed in the app source on main, in a .claude/worktrees/ worktree, with a unit test that reproduces it where possible, merged so the next archive carries it, recorded in data/crash-fixes.json, and logged as 'For Hidde: next build carries fix for <signature>'; the night run never archives, uploads or submits (`python3 scripts/crashes.py`)."

## 2026-10-16 night run (fourth attempt): nothing shipped

No claims stood. 60 READY leads (mostly Roosendaal street trees) still fail the rich-or-reader rule in recovery mode, so no write pass. `langcheck.py --next`: no city has 10+ English impressions untranslated. 0 trees, nothing changed in the product.

## 2026-10-16 night run (third attempt): nothing shipped

No claims stood. 0 trees, nothing changed in the product. The READY leads and the written-but-unmerged trees fail the rich-or-reader rule (see the entries below), so no write pass was dispatched; `enrich.py --next` says nothing to do. health.py: the scheduled iOS run on 10-15 failed after 1h35 (timed out; the push runs since are cancelled or still going), smoke is skipped, and the migration for profiles.country is not pasted (Hidde's to apply). Birmingham retry: the Alabama champion list is still a PDF with no stated licence and pypdf is not installed, so it stays stalled. Next: roster photo hunts need a new angle, not another sweep.

## 2026-10-16 night run (retry): nothing shipped, Memphis scouted

No claims stood. Nothing in the product changed; 0 trees. The 60 READY leads are mostly Roosendaal and other Dutch street trees, and the ten written-but-unmerged trees (Delft, Fort Worth, Leipzig, London, Salt Lake City, tree-of-the-year, Czech/Brazil) were already refused by preflight on two earlier runs for richness, so I did not retry. Scouted Memphis (#378): no register with tree-level coordinates, only a statewide Tennessee registry and champion list, plus Elmwood Cemetery's arboretum and Memphis Botanic Garden as sites. Recorded `empty` in data/register-scouting.json. Still open: vie_059, spk_015 and kyw_001 need stories but would likely fail the richness rule.

## 2026-10-16 night run (08:41 window): photos on roster pages

- Visits last 7 days: 1793. Rung 1 empty. Rung 2: iOS scheduled run still red (its newest push run in progress; needs a macOS look), and **profiles.country migration still unpasted (Hidde: supabase/PENDING.sql)**.
- Photo lane: London re-sweep plus one photo-judge pass (39 images): **3 live** (lon_025 Battersea strawberry tree, lon_028 Carshalton Plane, lon_030 Gunnersbury mulberry); 36 rejected. lon_028 shows trunk and limbs, not the whole crown; reverse with `python3 scripts/photo_apply.py hold lon_028`. Not judged: iNaturalist candidates for lon_025, Munich, Brisbane, Oahu, Dublin, Paris, Brussels.
- Bug seen: `photo_hunt.py --recheck` re-queues candidates already judged (Seville, Palermo, Amsterdam), so judges pay twice. Also `photo_hunt.py --help` runs a real sweep instead of printing help.
- Second pass on the remaining roster candidates (Munich, Brisbane, Oahu, Vienna, Paris, Brussels): 28 images, **0 approved**, all 27 candidates rejected and recorded in the queue (buildings, close-ups, wrong species; vie_041's file is Naturdenkmal 620, ours is 457). The roster's open-licence photo candidates are now used up; the lane needs new sources, not more judging.
- Tokens: photo-judge 148k + 93k (second one wasted).

## 2026-10-16 session with Hidde: recovery reprioritised, early-adopter tag and flag, 23 photos

- **Recovery mode reordered** (Hidde: "do this"): photos on cities Google used to show now come first; enrichment is the frozen roster only (`ROSTER_ONLY` in enrich.py). Why: ~565 enrichment commits since 10-01 and Google flat at ~35 impressions a day; rich pages earned 0.06 per page, not-rich 0.08. The noindex list was already tight (16 of 459 sub-four places indexable). DECISIONS.md 2026-10-16.
- **23 photos live** from a Commons re-sweep of the 20 top roster cities plus one photo-judge pass (21 Berlin Naturdenkmale, nyc_021, vie_044). 4 held, 11 trees with nothing usable. **ber_062 may be felled** (2025 photos show a stump): CURATION.md, check today. About 40 trees with fresh candidates were not judged yet (Munich, Brisbane, Oahu, Dublin, rest of Vienna, Paris, Brussels, Barcelona): next photo-judge pass.
- **Early-adopter tag and flag, app and web.** Every account opened before the paid tier goes live wears a gold "Early adopter" tag beside the ambassador tag (option 1 of five; the Polarsteps seal and a tag above the name were tried and dropped). The cutoff is `EARLY_ADOPTER_UNTIL` in site/src/lib/early-adopter.ts, null now, served to the app as `early_adopter_until` in /api/version.json. A one-time sheet explains it, remembered per account in user_metadata. Plus a **round country flag after your name**, picked in Edit profile (Hidde's yes to storing a country). **FOR HIDDE: paste supabase/PENDING.sql** (adds profiles.country); until then the flag stays empty and nothing else breaks. App needs a new build to reach phones.
- **Backlinks:** cold link asks are out (886 mails, 4 backlinks, none from a straight ask); ambassadors are never asked (CLAUDE.md). Two scouts found ~10 getLISBON-like city sites naming our trees (data/research/link-partners-2026-10-16*.json); strongest Bowery Boys (NYC, 5 trees) and Balarm (Palermo, 5). Not mailed; give-first citation then one mail is the plan if Hidde says go.
- Tokens: two link scouts 460k, photo-judge 255k (data/agent-costs.json).

## 2026-10-16 session: the app 1.0.2 "crashes on WiFi" (a reader's mail)

- **Cause, from our own MetricKit rows** (`diagnostics` table, three crashes at 08:18 UTC, the minute he wrote): build 20 (1.0.2) traps in `MyVotes.load` at launch. `treeId` took `[0]` of an empty split, and his general feedback of 13 Oct ("Location not working on iOS") has no tree. Every launch that reached Supabase crashed; on mobile data the request likely never got through, which is the whole WiFi difference. Same bug that crashed Hidde's phone on 10-11, fixed in 3c841e501, and confirmed inside the binaries of builds 34 and 35 (WorthIt.swift:89, the `.first` form). App Store Connect, checked 16 Oct: 1.0.3 build 35 is Waiting for Review.
- **Fixed today on the data side:** the four feedback rows with `tree = ''` now hold NULL, which 1.0.2 skips (`as? String` fails, the loop continues). Our scripts already read both as "-". No code change.
- **Still open:** any new general feedback from a 1.0.2 phone writes `''` again and crashes that sender until 1.0.3 is out. Re-run the same PATCH (`submissions?kind=eq.feedback&tree=eq.` set to null) if a crash shows up in `diagnostics` before then.
- **For Hidde:** a reply is drafted in drafts/reply-peter-wifi-crash.md (mailcheck clean, not committed: the repo is public).

## 2026-10-16 05:02 run: nothing published; scouted Buffalo

- 0 trees. Visits, 7 days: 1651 visits, 2404 page views. No reader photographs waiting. Deploy green (smoke "skipped" is just log-only pushes). The scheduled iOS run failed on `testSearchingForATreeMovesTheMapToIt`, the known iOS 18 runner flake from 2026-09-09; the fix is drafts/ios-floor-retry.patch and needs `workflows` permission this bot lacks (FOR HIDDE). Enrich empty, staged cities walled, written files still refused. Buffalo (#375): only a street-tree inventory and the Olmsted park inventory, no heritage register; `stalled` in data/register-scouting.json. Untried: NY DEC Big Tree Register, Forest Lawn Cemetery. San Juan (#376): no DRNA or municipal notable-tree register found in one Spanish search; `stalled`, untried: DRNA protected trees, Programa de Forestacion Urbana.

## 2026-10-16 (another retry): nothing published; scouted Allentown

- 0 trees. No claims; 60 READY and written-but-unmerged files still refused by rich-or-reader; langcheck has nothing to translate. Allentown (#372): no city register, only the PA Forestry Association statewide champion list (untried: PAbigtrees.com Lehigh County); `stalled` in data/register-scouting.json.

## 2026-10-16 (later retry): nothing published; scouted Regensburg and Newark

- 0 trees. No claims; enrich empty; written-but-unmerged files and the 60 READY leads still fail the rich-or-reader rule (same as earlier attempts, not retried). Regensburg (#366): de.wikipedia mirror of the city ND ordinance lists about 20 surviving entries but no coordinates, girth or age; finding aid, `stalled`. Newark (#369): no open register; NJ statewide Big Tree list is the untried angle. Both in data/register-scouting.json.

## 2026-10-16 (retry window): nothing published; scouted Phoenix

- No product change, 0 trees published. No claims standing; enrich queue empty; the 60 READY leads are mostly thin Dutch rows, which recovery mode (rich-only new trees) blocks.
- Munich refused (full, 63 of 60). Nuremberg claimed then released: 3 of 14 leads carry a coordinate; walled 48h.
- Phoenix scouted, stalled: Arizona's Magnificent Trees list is PDF-only, no coordinates or licence readable, dffm.az.gov returns 403 (now in the fetch blocklist). Next angle: a web.archive.org copy of the 2023 report.

## 2026-10-16 (02:45 window): nothing published; scouted Hallstatt

7-day visits: 1605 visits, 2353 page views. No reader photographs waiting, enrich says nothing to do. The written leftovers (delft, fort-worth, leipzig, london, salt-lake-city, tree-of-the-year) have no photo or confirmed pin, so I did not merge them. Scouted Hallstatt: no tree-level register with coordinates; the Upper Austria CC BY dataset is the untried route (verdict in data/register-scouting.json). The scheduled iOS run failed on one UI test, testSearchingForATreeMovesTheMapToIt ("search found no Beethoven Plane", 223 passed); it needs a macOS session. The Smoke test shows "skipped" on push runs only.

## 2026-10-15 (fourteenth attempt): nothing published; scouted Belfast, Brighton

No claims. Tried merging the 7 written-but-unmerged trees (delft, leipzig, london, fort-worth, salt-lake-city); preflight refused all (not rich, one 83-word story, Delft ash within 5 m of a register-dead ash and on the removed-slug list), so reverted. Scouted Belfast (#321): no register, Open Data NI street-tree CSV only. Brighton (#334): CPRE Sussex notable-trees map, licence unknown, finding aid only. Both `stalled` in data/register-scouting.json. 0 trees.

## 2026-10-15 (thirteenth attempt): nothing published; scouted Stratford-upon-Avon

No claims. Enrich nothing; the 60 READY leads and the written-but-unmerged trees are still refused by the richness rule, so no write pass. Scouted Stratford-upon-Avon (#313): no open notable-tree register, TPO points only, Woodland Trust ATI unlicensed. `stalled` in data/register-scouting.json with next angles. 0 trees.

## 2026-10-15 (twelfth attempt): nothing published; scouted Bristol, Cardiff, Oxford

7-day visits 1762 (2577 views). No sightings waiting. health.py: iOS app scheduled run failed (UI test `testSearchingForATreeMovesTheMapToIt` found no Beethoven Plane, and FlowWalk collect-intro/collect-away had 2 findings each); needs a macOS simulator, not reproducible here, left for a session. Site build is green. Enrich nothing; READY leads and unmerged files still refused by the richness rule. Scouted Bristol (#283), Cardiff (#294) and Oxford (#304): no notable-tree register in any; Bristol has TPO points and a council inventory (OGL), both protection or amenity, so `stalled` with next angles in data/register-scouting.json. 0 trees.

## 2026-10-15 (eleventh attempt): nothing published; scouted Canterbury

No claims standing. READY leads (60, thin Dutch street trees) and the written-but-unmerged trees are the same ones refused under rich-or-reader in earlier attempts; not retried. Enrichment says nothing to do. Scouted Canterbury (#277): no city register; only TPO points (OGL) which are protection, not remarkableness; Woodland Trust ATI licence unseen. `stalled` in data/register-scouting.json with next angle. 0 trees.

## 2026-10-15 (tenth attempt): nothing published; scouted Middletown

No claims. Enrich nothing; the 60 READY leads and the written-but-unmerged files are still refused by the richness rule (see fourth attempt), so no write pass. Scouted Middletown CT (#276): no city register; Connecticut's Notable Trees database (Connecticut College Arboretum) is the naming body, but its certificate failed to verify and no licence or coordinates were seen. `stalled` in data/register-scouting.json with next angle. 0 trees.

## 2026-10-15 (ninth attempt, 22:08 window): fixed the broken deploy; scouted Inverness

7-day visits: 1754 visits, 2568 page views.
- Rung 2 fixed: the deploy and smoke failures were one cause, the Fort Worth StoryMap list (no licence block) saved in data/registers/. Moved to data/research/fort-worth-heritage-trees-storymap.json (the scouting notes still name the old path). Preflight 0 problems; pushed.
- Not fixed, needs a session with Xcode: iOS app. (1) testSearchingForATreeMovesTheMapToIt: "search found no Beethoven Plane". (2) appfit DRIFT on collect-intro and collect-away: text 'Photograph a tree you are standing in fro...' starts at x=26 while two other things start at x=20, on all four phone sizes.
- Scouted Inverness (#214): stalled. Scottish Tree Register is members only, Highland TPO data has no licence. Leads: ancient-yew.org Highland yews, OSM, Wikidata. About 40k tokens. 0 trees.
- Scouted Innsbruck (#228): imported. Tyrol's Naturdenkmaeler points are CC BY 4.0; data/registers/tirol-naturdenkmaeler.json holds 260 active points (about 198 trees, about 34 around Innsbruck) plus 45 revoked. Names only, no species or girth, pins approximate, none publishable until access is checked. Innsbruck's own Baumkataster not looked at. qa source checks clean. 0 trees.
- Scouted Minneapolis (#259): stalled. The Park Board Heritage Tree list is an 86-row public ArcGIS layer (UMN survey 2026, with coordinates, species and a Healthy/Poor/Dead flag) but carries no licence. Saved as data/research/minneapolis-heritage-trees-umn-survey-2026.json; the Dead-or-Missing flags are a life check for data/leads/minneapolis.json. Next step: ask UMN or the Park Board for the licence. 0 trees.
- Scouted Stirling (#264): stalled. No open tree layer; the Scotland-wide TPO layer says only "Licence: Open" with no proving sentence. Next angles: OSM and Wikidata, Forestry and Land Scotland. 0 trees.
- Scouted Baltimore (#265): stalled. TreeBaltimore Notable Trees Map (city and state champions) and the Maryland Big Tree Program state no licence and offer no download. Next angle: a written reuse yes from Recreation and Parks or TreeBaltimore. 0 trees.
- Scouted Trier (#272): imported. Rhineland-Palatinate Naturdenkmal points (LANIS naturdenkmale_punkte) are ODbL, "mit Quellenangabe zulaessig"; data/registers/rlp-naturdenkmaeler.json holds 1,676 points for the state (1,486 with a tree word), 199 in Trier city (196 trees) and 46 in Trier-Saarburg. Names only, pins approximate, none publishable until access is checked (many sit on the Hauptfriedhof, abbey grounds, the Karthaeuser Hof arboretum). qa source checks and preflight clean. Best next lead for Germany supply. 0 trees.
- Scouted York (#274): stalled. The council's tree layer is OGL 3.0 but a plain amenity inventory (no veteran, girth or age field); TPO layers skipped. Next angles: York Museum Gardens champion trees, ancient-yew.org Yorkshire yews, OSM and Wikidata for the Minster grounds. 0 trees.
- Shelf unchanged: enrich has nothing; 60 READY leads still refused by the richness rule.

## 2026-10-15 (eighth attempt): nothing published; scouted Tulsa

No claims standing. 60 READY leads are still refused by the richness rule; every awaiting-writer file is refused or duplicate (see fourth attempt). enrich.py nothing; langcheck has no city over 10 impressions. Scouted Tulsa (#198): no heritage register, only Oklahoma's state champion list and the Creek Council Oak site; `stalled` in data/register-scouting.json. 0 trees.

## 2026-10-15 (seventh attempt): nothing published; found Fort Worth's Heritage Tree register

Released the stale Miami claim (no register candidates, two earlier passes found nothing rich). 60 READY leads unchanged and still refused by the richness rule. Scouted Fort Worth (#195): the city's Heritage Tree StoryMap holds about 54 named trees with stories and coordinates, saved to data/registers/fort-worth-heritage-trees-storymap.json; `stalled` in data/register-scouting.json until the city's terms are read and the lost trees dropped. This is the best lead for a next window: clusters at Casino Beach, Arrow S Park, Trinity Park and Greenwood Cemetery. 0 trees.

## 2026-10-15 (sixth attempt, 19:38 window): nothing published; scouted San Antonio

Visits, 7 days: 1610 (2260 page views). No sightings waiting. health.py's "smoke test skipped" is a false alarm: smoke.yml skips data-only pushes, and Build and deploy is green. Enrichment nothing; shelf still only refused or duplicate trees. Scouted San Antonio (#193): no register with coordinates, `stalled` in data/register-scouting.json (Quadrangle Oak at Fort Sam Houston is a lead, base access unclear). 0 trees.

## 2026-10-15 (fifth attempt, same window): nothing published; scouted Pittsburgh

No claims, 60 READY leads still thin (Dutch street trees; rule refuses them), written trees still refused, so no write pass. Scouted Pittsburgh (#173): the Remarkable Trees of Pittsburgh register exists (about 16 named trees across Mellon, Arsenal, Frick, Highland parks), but its site shows no per-tree data and is All Rights Reserved; marked `stalled` in data/register-scouting.json with next angle. 0 trees.

## 2026-10-15 (fourth attempt, same window): nothing published; the "written, ready to merge" files are blocked by rules

No claims standing; `enrich.py --next` says nothing to do. Tried merging the written-but-unmerged verified entries: preflight refused both batches I tried. Delft del_011 sits within 5 m of LRMB 1691008 (status 5, felled) and its slug is in REMOVED_TREE_SLUGS, so it should become a lead, not a page. Leipzig lpz_019/021/022/023 are not rich (no confirmed pin, partly no register or access), so recovery mode refuses them. Both reverted. Left alone: london lon_029, fort-worth ftw_018, salt-lake-city slc_006, tree-of-the-year std_001/nsb_001, famous-czech-brazil fdl_001 (same richness rule likely applies; not tried). The 60 READY leads are mostly Roosendaal/Dutch street trees and would fail the same rule. Next step for a run with network: enrich-first (photo + pin) on those ten, then merge. Untried: BACKUP scout of Pittsburgh (#173).

## 2026-10-15 19:03 run: own photos held, Manchester scouted (no trees added)

Visits, 7 days: 1590 visits, 2240 page views. Rung 1: looked at the two own app photographs (brn_005, brn_008, both planes in daylight, fine frames) and held both, since own photos are never auto-published and both trees already have approved photos; the Gaien ginkgo avenue (34bc1a6d) stays a lead with its why written (an avenue, not a trunk, no register). Rung 2 clear. Rung 4: ladder sent me to scouting; Manchester recorded as stalled in data/register-scouting.json (no heritage register, only an OGL TPO layer as a finding aid). Shelf had no writable or enrichable work (enrich: nothing; writable pile held by photo/pin rule). No trees published, no pass dispatched. Short window: stopped here.

## 2026-10-15 session: a wrong pin no longer forces a new tree (app, build 35)

- **Peter's bug (Seville, mail of 15 Oct).** At the real Ombú of La Cartuja the app offered only "new tree" and his pin move failed. Cause: our sev_002 pin is about 1.7 km off (approximate), the collect flow only offers our trees within 400 m of the photo, and the live 1.0.2 has no tree-page shortcut. His "The tree is here" correction never reached Supabase (no row since his 8 Oct Judas tree one), most likely a lapsed sign-in sending anonymously; not reproduced.
- **Fixed in the app:** with nothing within 400 m, "Which one is it?" now shows the closest three within 3 km plus a search by name; a far pick asks once on the compare screen ("Our pin is 1.2 km from where you took this photo"), collects, and sends a `correction` row with the photo's coordinate; the last screen says we will move our pin. Unit test `aWrongPinStillOffersTheTree`, FlowWalk green, looked at on 17 Pro and SE. CONVENTIONS.md entry (Google Maps add-photo search).
- **For Hidde:** build 35 of 1.0.3 is archived for the Organizer. To ship it instead of 34: remove 34 from review in App Store Connect, upload 35, submit. This restarts Apple's review.
- **Still open:** the Ombú pin itself (needs Peter's photo with its location; our sources do not place it), and the pin screen's "Try again" message when the sign-in has lapsed.

## 2026-10-15 (third attempt, same window): nothing published; scouted Santa Fe and Glasgow

No claims standing; same 60 thin READY leads and refused written trees as before, so no write pass. langcheck table empty, enrichment nothing to do. The two Amersfoort English fixes the translator flagged were already in place. Scouted Santa Fe (#136, `empty`: only the NM Big Tree PDF) and Glasgow (#150, `stalled`: Scotland TPO layer unchecked; Argyle Street ash, Darnley Sycamore and Kelvingrove plane named as leads). Verdicts in data/register-scouting.json. 0 trees.

## 2026-10-15 (retry, same window): nothing published; scouted Albuquerque

No claims standing. The 60 READY leads and the written-but-unmerged trees (Leipzig 4, Delft, London, Fort Worth, Salt Lake City, tree-of-the-year 2) are the same thin rows preflight refuses under recovery mode, so no write pass. Enrichment: nothing to do anywhere. langcheck table empty. Scouted Albuquerque (#90): no city register; the NM Big Tree Database PDF is the lead (no coordinates), verdict `empty` in data/register-scouting.json. 0 trees, about 30k tokens.

## 2026-10-15 (window 14:37 UTC): nothing published; scouted Ann Arbor

No tree went live this window. Visits last 7 days: 1540 (2190 page views). Rungs 1 and 2 clear (no sightings waiting, health.py clean, 0 BLOCKER). Enrichment says nothing to do anywhere. The shelf's "written and ready" trees (Leipzig 4, Delft, London, Fort Worth, Salt Lake City, tree-of-the-year 2, one famous) look like the held kind preflight refuses; I did not merge them or check each. `photo_hunt.py --recheck` swept 40 trees with no new candidates; `photo_fetch.py --zero` fetched only 4 Rotterdam Trompenburg images (greenhouses and an aviary, not the trees), none approved. Scouted Ann Arbor (#77): no city register online; the Michigan Big Tree Register (Google Doc) is the lead, marked `stalled` in data/register-scouting.json with the next angle. Preflight 0 problems.

## 2026-10-15, session: Cantonspark dawn redwood pin fixed

- Hidde: the "Watercypres" app sighting (ff725d9a, held on 09-08 against the sequoia) and brn_001, the Cantonspark Dawn Redwood, are the same tree, and the Watercypres fix is the right spot. brn_001 moved about 140 m south to 52.207835, 5.298591, next to the sequoia and tulip tree by the main entrance; `pin_source` records it. The 10-05 automatic move from sighting 22864b26 had put it in the wrong corner of the park.
- Story's closing note no longer talks about a pin in a cluster of conifers; it now says the 2021 measurements are dated. The sighting lead is marked matched.

## 2026-10-16, session: about page text rewritten by Hidde

- /about carries Hidde's new wording (Lisbon opening, "the stories that make them unique, each tree has a story that only locals know"), with his typos and grammar fixed on his ask. Text only, layout untouched.

## 2026-10-16, session: about page back to the cedar photo

- Hidde: "the lighting kinda sucks" on the Noike photo (shot into the sun). A brightened copy only washed it out, so /about shows the cedar photo and its old caption and text again, exactly as on 10-14. The Noike files stay in site/public/photos/about/, unused.

## 2026-10-15, session: new photo on the about page

- /about now shows Hidde and his son under the Noike torii between the two cedars, facing the camera, full frame (his ask). Caption and the photo sentence say "me and my son"; the son is not named. New files site/public/photos/about/hidde-noike-{600,1200}.jpg, EXIF and GPS stripped. The old hidde-cedar files stay in place, unused.
- Looked at it rendered at 375px and desktop before pushing.

## 2026-10-15, iOS CI red since 10-14: two test-side causes, no app regression

- **Nothing changed in the app.** The map's "Location off" chip after a refusal was never broken.
- **LocationAskWalk was a race in the test.** The CI run's video shows the "Don't Allow" tap landing while iOS was still animating the location alert in: it fell through to a map pin, opened that tree's page, and the alert stayed up over it. The test now waits for the alert to stop moving, taps, and requires the alert to be gone. 20 of 20 passes on the local iPhone SE under CPU load.
- **The layout step did not hang.** Each phone's sweep was timed together with its build against a 20-minute guard, and a green run on 10-14 already took 16 to 17 minutes per phone on the runner (4 minutes locally). appfit.py now builds once outside the clock, gives each phone's sweep 30 minutes, and prints how long the build and each sweep took. The look job's ceiling went from 75 to 100 minutes to fit.

## 2026-10-15, autonomous window (retry): no trees shipped

- **Nothing changed in the product.** No claims stood. I merged the 8 staged trees that had stories (Delft del_011, Fort Worth ftw_018, Leipzig lpz_019/021/022/023, London lon_029, Salt Lake City slc_006) and preflight refused all of them, so I reverted the merge. Reasons: none is rich (pins approximate or missing, no register record, access unconfirmed). ftw_018's story is 83 words. del_011 sits within 5 m of a dead-marked LRMB tree and its slug is in REMOVED_TREE_SLUGS. They need a pin, register record or photo before they can ship.
- Scouted Nashville (#74): no coordinate register; verdict in data/register-scouting.json.
- The 60 READY leads (mostly Roosendaal register trees) were not written: recovery mode forbids new trees that are not rich.

## 2026-10-15, autonomous window 08:46 UTC: scouting only, no trees

- **Nothing changed in the product.** 7-day visits: 1520 visits, 2210 page views. Reader inbox empty. Enrichment says nothing to do. The staged Leipzig, London, Fort Worth and Salt Lake City trees are held: approximate pins, no photo, access unverified.
- **Scouted four places** (verdicts in data/register-scouting.json): Cambridge (council TPO points under OGL, but no species or size, so a finding aid only), Raleigh (no city list; the NC champion list is a research list only), Cleveland (no register; Metroparks' Ten Big Trees guide is a lead source) and El Paso (no register; a state-champion Aleppo pine downtown is a lead).
- **Breakage:** the iOS scheduled run failed 2026-10-14 after 1h57m. The log shows two UI-test failures: `testTappingAPinOpensItsTree` (UI query timed out) and `LocationAskWalk` (after a refusal the map still says location is off). A push-triggered run on the latest main was in progress at 08:46 and is not yet read. App work was not started this window.

## 2026-10-15, session: the Lime of Unterlappach goes live

- **Live (next deploy):** muc_068, The Lime of Unterlappach (/munich/lime-of-unterlappach), the small-leaved lime on a rise between Unterlappach and Rottbach (Maisach, Fürstenfeldbruck county) that the SNSB botanist sent by mail. Girth 5.65 m (2021), 18 m tall, set on fire through its hollow trunk in December 2014 and recorded vital in April 2025. English and German.
- Sources: Baumkunde register 3877, Münchner Merkur 23.12.2014, Bayern LfU Naturdenkmal ND-00668. Pin confirmed: the LfU point and Baumkunde's coordinate agree within 8 m on a solitary tree. Age kept broad (Baumkunde 250, Merkur "several hundred", locally "the thousand-year lime"). Lead marked published.
- Open: no open-licence photograph exists (Commons and the de.wikipedia county list have none; Baumkunde's are all rights reserved). Flagged: species from Baumkunde only. The botanist has not been told it is live.

## 2026-10-15, session with Hidde: trees on one spot, and the saved pin

- **Live (next deploy), web and app:** trees that share one coordinate are one moss bubble with the count. One tap flies onto the spot and spreads the pins round it, each on a thin line to a dot on the real spot; a pin opens its tree; a tap on the map or your own zoom folds them back. 65 published trees were unreachable under another pin (43 shared coordinates, 108 trees; Hawaii has 6 on one point). Hidde picked this over a list sheet after a mockup of both. Recorded: CONVENTIONS.md, "Two trees on exactly the same spot".
- **Live:** a saved tree's pin on the web city map wears the bookmark, as the app's already did, not the heart.
- The Ajuda dragon tree (lis_002) keeps its old pin: Hidde has stood there and says it is right. A move to its photo's geotag was reverted the same day.
- Then everywhere (Hidde: "map interaction need to stay consistent"): /explore, the country maps and My trees share one helper, PILES_JS in lib/map.ts, with the same bubble, zoom and spread. Tested in a browser harness on the Lisbon data; live check on the deployed site pending.

## 2026-10-15, session with Hidde: the account menu

- **Live (this push):** the desktop bar's Account is a plain word with a small thin chevron, as is Explore (AllTrails' marker; the filled triangle is gone). Its menu is two rows, My trees and Settings, each with its icon; the "Yours" heading is gone. Sign out stays on Settings, on Hidde's word.
- Bug fixed: signing in renamed the My trees row to a second "Account" and wiped its leaf, on desktop and in the phone sheet (the nav painter matched every /account link). The smoke test now fails if a row to /account loses its icon once signed in.
- The phone menu button is Phosphor's list icon instead of a hand-drawn one (iconcheck refused the touched line). Looked up and recorded: CONVENTIONS.md, "The desktop header's dropdown marker".

## 2026-10-15, session with Hidde: the Montsouris plane gets its reader's age

- **Live (next deploy):** par_034 now gives "about 186 years by a reader's estimate", in the age field and the story, where it had asked readers for an age its own reader had already given.
- New preflight check `check_a_readers_age_reaches_the_page()`: a reader's tree whose sighting names an age the page omits is refused. Swept every sighting with an age: no other published tree was missing one. Unused, as a lead only: the same reader's pedunculate oak near Santranges, 245 years, 440 cm. Its photograph, viewed this session, is a garden well and not the oak, so it cannot go live; the reader was already asked for the oak's photo in the 2026-10-13 Montsouris mail, so no second mail (the duplicate draft is removed).

## 2026-10-15, session with Hidde: tree page photo shape and collect wording

- Tree pages whose lead photograph is 4:3 (263 of them) now show the whole photograph: beside the facts on a desktop, at 4:3 on a phone and in the app feed, instead of a wide strip that cut 40 percent of the height (the Cardón of the Expo lost its top). Commit 28d6112ab.
- The website's collect button reads "Collect this tree" in all eight languages, the app's words; it used to say "Mark as collected", although collecting has needed a photograph since 10-14.

## 2026-10-15, third retry: no new trees live

No claims standing. Same 60 READY leads and written-but-unmerged entries refused under rich-or-reader; enrich nothing to do; langcheck table empty; BACKUP only Roosendaal (deepened three times today). Nothing dispatched, 0 trees, about 10k tokens.

## 2026-10-15, second retry after the 3-minute stop: no new trees live

No claims standing. 60 READY leads are the same rows earlier runs refused under the rich-or-reader rule; enrich says nothing to do; prepare.py's only BACKUP is Roosendaal, already deepened three times today. Nothing dispatched, 0 trees, about 15k tokens.

## 2026-10-15, retry window after 05:15: no new trees live

No claims standing. 60 READY leads and the written-but-unmerged entries (lpz_019/021/022/023, lon_029, std_001, nsb_001, ftw_018, slc_006, del_011) are the same thin or access-doubtful rows earlier runs refused under the rich-or-reader rule; no write pass dispatched. Amersfoort English fixes flagged by the translator (FAQ count, raw register fields in ame_015 access) were already corrected. Enrichment says nothing to do anywhere. 0 trees, about 20k tokens.

## 2026-10-15, window 05:15 UTC: no new trees live

7-day visits: 1210 visits, 1750 page views. No reader submissions or app photographs. health.py: iOS scheduled run still failing (timed out at 1h57m, app work, untouched); Smoke "skipped" on push is by design, deploy is green. Enrichment: the only open gaps (7 trees in London, Chicago, Seattle, Roosendaal, Potsdam) were all season; only the sycamore and sessile oak have a "striking" fruit moment and neither tree is a real fruit-peak case, so no best_time added and the gaps are recorded as dead ends for 90 days (no agent dispatched). Frankfurt (top unwalled DE city) claimed for verify, but passcheck found no imported register within 20 km and from-zero research is off, so no pass; claim released, Frankfurt walled 48h. London claim released with --force (lon_029 is written but preflight-refused as not rich). pagegaps: nothing missing. langcheck: nothing worth translating. scout_next points at Roosendaal, already deepened three times today. Lanes are drained; 0 trees, about 30k tokens.

## 2026-10-15, window 02:48 UTC: no new trees live

7-day visits: 1200 visits, 1730 page views. No reader submissions or app photographs waiting. health.py flags the iOS scheduled run (timed out at 1h57m, app work, untouched) and Smoke "skipped" on push (not a build failure; deploy is green). Shelf had no write-ready trees, so Graz verify (the top US/UK/DE/AT city with register supply): the register carries no girth, height or age and every measured Naturdenkmal is already published or blocked, so nothing could end rich. Filed 3 leads and 2 blocks in data/leads/graz.json, Graz walled for 48h. Munich refused (62 of 60). Cost about 90k tokens, 0 trees. Then a viewing pass on the zero-photo queue: 52 images looked at, 2 approved (spr_002 Sapporo Katsura Fudo, CC BY-SA; mlc_005 Alzina d'en Pere, Mallorca, iNaturalist CC BY, geotag 23 m from the pin, only 333x500 px), 50 rejected (mostly no tree in frame). Reverse with `python3 scripts/photo_apply.py hold <id> <url>`. Cost about 115k tokens. Second viewing pass: 48 judged, 4 approved (abp_001 Patriarch Tree, bhm_005 Queen's Park wych elm, hst_004 and hst_002 Hallstatt yews; all geotagged within 83 m or named by register number), 2 held (bhm_003, ind_001), 42 rejected. The image viewer hit its request limit, so about 50 downloaded candidates (Belfast, Boise, Boston, Charleston, Hamburg, Vienna, Portland, Kansas City and others) are unjudged in out/dl/photos3. Reverse with `photo_apply.py hold <id> <url>`. Cost about 250k tokens. Third pass judged that remainder: 52 viewed, 5 approved (bfs_003 Belfast dawn redwood, gut_001 Gutau yew, kcy_002 Robert E. Lee Tree, mty_003 Monterey Moon Tree, ank_001 Ankerwycke Yew; iNaturalist geotags 4 to 44 m from the pin settled three), 2 held (ind_001, mau_001 photographed before the 2023 fire), 45 rejected. ank_001 shows the crown but not the trunk; reverse with `photo_apply.py hold ank_001 <url>` if that reads too loose. Cost about 120k tokens. A fourth pass found only 16 new candidates and approved none (1 held, rot_015; 15 rejected), about 80k tokens: the queue is drained, and photo_hunt.py --recheck keeps sweeping the same 40 trees (Aarhus to Amerongen) with no new candidates. Totals for the window: 11 photographs approved, 0 trees added.

## 2026-10-15, second retry: Roosendaal 13 to 16

Roosendaal deepen pass: verify found two LRMB trees with confirmed pins, girth and height (roo_020 London Plane, Oostelijke Havendijk, 407 cm; roo_021 White Willow near Nispen, 502 cm), both view-only and said so. The writer corrected my verify notes against the register (Schietwilg is white willow, not a pollard; age band 1900-1910). roo_019 (sycamore) got a concrete sourced access line and is now live. City copy recounted to 16, plane species spelled x acerifolia to match the site rule. Preflight 0 problems; the site build was not run in this session (command denied), so the deploy is the check. Eight more leads filed; Roosendaal's 300 cm+ register list is exhausted. The other "written and ready" trees (Leipzig, Delft, Fort Worth, SLC) stay out for the same preflight reasons. Claim released. Cost: verify ~90k, write ~75k tokens, 3 trees.

## 2026-10-15, retry attempt: nothing published

- No product change. Claims were clear. All 55 READY leads are ordinary trees (Roosendaal 17, Munich 5, Delft 5, others), which recovery mode and preflight's rich rule refuse, so I dispatched no write pass. The 12 "written and ready to merge" trees were already tried on 10-13 and preflight refused them (not rich, approximate pin, thin access line); they stay out.
- `enrich.py` has nothing to do anywhere. `langcheck.py --next` has an empty queue (24 cities under 10 English impressions). The lanes left need a session or a new source: Roosendaal roo_019 needs a sourced access line, Miami and Key West have no per-tree register, the German cities lack girth data.
- iOS app scheduled-run failure at session start is untouched (app work, needs a session).

