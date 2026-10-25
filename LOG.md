# LOG

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-10](archive/LOG-2026-10.md)
- [2026-09](archive/LOG-2026-09.md)
- [2026-08](archive/LOG-2026-08.md)
- [2026-07](archive/LOG-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.

## 2026-10-25, forty-first attempt (nothing shipped)

Nothing changed in the product. Same state: no claims, inbox empty, 3 READY leads blocked by the own-supply pause, health.py's exit 1 is the push-skipped smoke and deploy runs (a scheduled deploy was in progress, not a break).

## 2026-10-25, fortieth attempt (nothing shipped)

Nothing changed in the product. No claims, inbox empty, 3 READY leads still under the supply pause, all 3 open Reddit items already drafted. health.py's exit 1 is again the push-skipped smoke and deploy runs; a scheduled deploy was in progress.

## 2026-10-25 (late attempt): outreach rung

Nothing shipped on the site. No claims standing, inbox empty, health.py's only flag is smoke "skipped" (log-only pushes skip it; Build and deploy succeeded, not a break). The 3 READY leads (Oxford x2, Madrid) are own supply, which is paused. Pulled private store, harvested r/lisbon and r/sicily (0 new comments), 3 open items all already have drafted replies; rebuilt the preview.
For Hidde: 3 Reddit replies in drafts/batch-community-preview.md (the r/lisbon Santa Iria photo reply is the one that matters: asks permission to use the photograph).

## 2026-10-25, thirty-ninth attempt (nothing shipped)

Nothing changed in the product. Inbox empty, harvest 0 new comments, all 3 open Reddit items already drafted, same 3 photo-less READY leads under the supply pause. health.py exit 1 is the push-skipped smoke test, answered. For Hidde: 3 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25, thirty-eighth attempt (nothing shipped)

Re-checked: no claims, same 3 photo-less READY leads (Oxford x2, Madrid) held by the own-supply pause, `enrich.py --next` has nothing. No new work found; nothing dispatched.

## 2026-10-25, thirty-seventh attempt (nothing shipped)

Re-checked, nothing workable: no claims standing, no reader photographs waiting, health.py's "skipped" deploys are push-skips by design (the 12:36 dispatch succeeded). The 3 READY leads (Oxford x2, Madrid) are own supply, paused under recovery mode, so not written. `enrich.py --next` says nothing to do. The 3 open Reddit items already have drafted replies; preview refreshed, nothing new to push. For Hidde: 3 Reddit replies in drafts/batch-community-preview.md.

## 2026-10-25, thirty-sixth attempt (nothing shipped)

State re-checked. No claims standing. No photographs waiting. health.py's two "skipped" flags (Smoke test, Build and deploy) are push-triggered runs that skip by design; the dispatched deploy at 12:36 succeeded, so the site is not stuck. READY has 3 leads (oxford 2, madrid 1) but own supply is paused, so they wait. Community lane: 3 open Reddit items all already carry drafted replies, harvest found no new comments, preview rebuilt. For Hidde: 3 Reddit replies in drafts/batch-community-preview.md. No mail batch started because this batch waits for his word.

## 2026-10-25, thirty-fifth attempt (nothing shipped)

Nothing changed in the product. Inbox empty, harvest 0 new comments, watch queued 0 threads, all 3 open Reddit items already drafted (batch waits for Hidde, so no mail batch). Same 3 photo-less READY leads under paused own supply, no write pass. health.py exit 1 is the push-skipped smoke test; the scheduled deploy succeeded.

## 2026-10-25, thirty-fourth attempt (nothing shipped)

Nothing changed in the product. No claims, inbox empty, the same 3 photo-less READY leads wait under the supply pause. The skipped Build and deploy / Smoke test runs are push no-ops, answered in health.py. All 3 open Reddit items already have drafted replies and a batch waits for Hidde, so no mail batch was started.

## 2026-10-25 night run, rung 4 (communities)

No claims standing. The 3 READY leads (Oxford x2, Madrid) are our own trees without an approved photograph, so they wait under the supply pause. Health: the skipped deploys are push no-ops, the scheduled build succeeded. Reddit: harvested, watched (1 new thread queued), 3 replies drafted, previewed and pushed to the private store.

For Hidde: 3 Reddit replies in drafts/batch-community-preview.md (r/lisbon Santa Iria photo permission, two r/marijuanaenthusiasts redwood threads).
<!-- archive-index -->
## 2026-10-25, thirty-third attempt (nothing shipped)

Nothing changed in the product. No claims, inbox empty, same 3 photo-less READY leads (Oxford 2, Madrid 1) under paused own supply, so no write pass. health.py exit 1 is only the skipped smoke test (bot push); the deploy succeeded 0.8h ago. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25, thirty-second attempt (nothing shipped)

Nothing changed in the product. Inbox empty, harvest 0 new comments, both open Reddit items already drafted, same 3 photo-less READY leads (Oxford 2, Madrid 1) under paused own supply, so no write or verify pass. health.py exit 1 is the push-skipped smoke test (scheduled run 09:18 succeeded); answered with `health.py --answer`. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25, thirty-first attempt (nothing shipped)

No claims standing, inbox empty, same 3 photo-less READY leads (Oxford 2, Madrid 1) under the paused own supply, both open Reddit items already drafted. Staged-city verify would only add leads that cannot go live under the pause, so none dispatched. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25, thirtieth attempt (nothing shipped)

No claims standing. Same 3 READY leads (Oxford 2, Madrid 1), own supply under the pause and no photographs, so no write pass. Nothing new since the twenty-ninth attempt; Reddit drafts still wait for Hidde.

## 2026-10-25, twenty-ninth attempt

Nothing shipped. No claims standing; 3 READY leads (Oxford 2, Madrid 1) are our own supply and wait under the pause. Inbox empty. Smoke and deploy "skipped" on bot pushes only; the scheduled deploys succeed, so not broken. Reddit: 2 open items both already drafted, preview rebuilt, harvest and watch found nothing new.
For Hidde: 2 Reddit replies in drafts/batch-community-preview.md (r/lisbon Santa Iria photo ask, r/marijuanaenthusiasts Grizzly Giant).

## 2026-10-25 night run, twenty-eighth attempt (nothing shipped)

Nothing changed in the product. Inbox empty, harvest 0 new comments, the 2 open Reddit items already drafted (preview rebuilt, store pushed), no archive-group mail ready. Same 3 photo-less READY leads under paused own supply, enrich says nothing to do. health.py exit 1 is the by-design skipped smoke test (smoke.yml skips claude[bot] pushes); answered with `health.py --answer`. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25 night run, twenty-seventh attempt (nothing shipped)

No claims standing, inbox empty. READY leads are 3 of our own (Oxford x2, Madrid x1), none with a photograph, so own supply pause and ADD_NEEDS_PHOTO keep them from going live; no write pass dispatched. health.py's "Smoke test / Build and deploy skipped" is a false alarm: log-only pushes skip by path filter, the last scheduled deploy (04:55) succeeded.

## 2026-10-25 night run, twenty-sixth attempt (nothing shipped)

Nothing changed in the product. No claims, inbox empty, same 3 photo-less READY leads under paused own supply, both open Reddit items already drafted. health.py exit 1 is only the push-skipped smoke and build runs; the last scheduled deploy succeeded. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25 night run, twenty-fifth attempt (nothing shipped)

Nothing changed in the product. No claims, inbox empty, same 3 photo-less READY leads (own supply paused), 2 Reddit items already drafted, health.py exit 1 is still only the skipped smoke test. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25 night run, twenty-fourth attempt (nothing shipped)

Nothing changed in the product. Inbox empty, harvest 0 new comments, the 2 open Reddit items already drafted. health.py exit 1 is only the push-skipped smoke test (deploy succeeded 2h ago). Own supply paused, 3 READY leads photo-less, so no write or verify pass. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25 night run, twenty-third attempt (nothing shipped)

Nothing changed in the product. Pulled, no claims standing, same 3 photo-less READY leads (Oxford 2, Madrid 1) under paused own supply, so no write pass. Stirling register already retried twice (10-22, 10-23) with no register to find, so not a third time. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25 night run, twenty-second attempt (nothing shipped)

Nothing changed in the product. No claims, inbox empty, same 3 photo-less READY leads (own supply paused). The skipped deploys are push-triggered no-ops; the last dispatched deploy succeeded. The 2 Reddit items are still drafted. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25 night run, twenty-first attempt (nothing shipped)

Nothing changed in the product. No claims, inbox empty, 3 READY leads (Oxford 2, Madrid 1) are photo-less and own supply is paused, so no write pass (under six anyway). Staged cities only feed a paused supply. The 2 open Reddit items already carry drafts. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25 night run, twentieth attempt (nothing shipped)

Nothing changed in the product. Inbox empty, harvest 0 new comments, watch 0 new threads; the 2 open Reddit items are drafted, preview rebuilt and pushed, so no mail batch started. health.py exit 1 is only the push-skipped smoke test. Own supply paused, 3 READY leads photo-less, staged cities walled. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25 night run, nineteenth attempt (nothing shipped)

Nothing changed in the product. No claims, sightings inbox empty, the 3 READY leads still cannot ship under paused own supply. Community lane re-run: harvest found 0 new comments, the 2 open items (r/lisbon Santa Iria photo, r/marijuanaenthusiasts Grizzly Giant) already carry drafts, preview refreshed and pushed. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md. iOS run 40144403493 for the pill fix was still in progress.

## 2026-10-24 night run, eighteenth attempt (nothing shipped)

No claims standing, sightings inbox empty, 3 READY leads (Oxford x2, Madrid) have no approved photograph and own supply is paused. The iOS run for the pill fix (40144403493) is in progress; the earlier failure was the appfit issue it fixes. The Reddit batch still waits on Hidde, so no mail batch started.

## 2026-10-24 night run, seventeenth attempt (nothing shipped)

Nothing changed in the product. Sightings inbox is empty, both open Reddit items already carry drafted replies (r/lisbon Santa Iria photo, r/marijuanaenthusiasts Grizzly Giant), no claims stood. The 3 READY leads (Oxford x2, Madrid) cannot ship under the paused own supply. Graz and Nuremberg were claimed and released: 0 of 7 and 3 of 16 leads carry a coordinate, so a verify pass would fail on the pin. Both are walls for 48h. Stage 1 and 2 cities have no placed supply either. Open: the iOS workflow shows FAILED since 2026-10-24 (not investigated this attempt).

## 2026-10-25 night run, sixteenth attempt: nothing shipped

Sightings inbox empty. health.py: the deploy "skipped" runs are cancelled by newer pushes (one deploy running), and the ios.yml failure is the pill fix the fifteenth attempt pushed, now rebuilding. Reddit harvest and watch found nothing new; the 2 open items (r/lisbon Santa Iria photo, r/marijuanaenthusiasts Grizzly Giant) are already drafted and the preview is rebuilt, no mail batch started while that batch waits. Own supply is paused, so READY leads and staged cities were not dispatched.

For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-24 night run, fifteenth attempt: one app fix, no trees

The iOS run failed appfit on the new Add a photo pill: its touch target (inset -4 on all sides) put the button's right edge at W-16 against the page's W-20. Now the target grows vertically only (TreeDetail.swift addPhotoRow); not rebuilt here (no Xcode), the next ios.yml run confirms. Site deploy skips were concurrency, one deploy is running. READY leads (3) and every staged city only make trees of our own, which are paused, so no verify or write pass was dispatched. Community drafts unchanged.

For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-24 night run, fourteenth attempt: nothing shipped

No claims standing. 3 READY leads (Oxford 2, Madrid 1) have no approved photograph, and own supply is paused, so none can go live. Sightings inbox empty. Community queue: 2 open items, both already drafted (r/lisbon Santa Iria photo, r/marijuanaenthusiasts Grizzly Giant); preview rebuilt, nothing new to push. Stirling register retry already done on 10-22 and 10-23 with no new angle, left stalled.

For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-24 night run, thirteenth attempt (short)

Nothing shipped; no product change. Checked: no claims standing, sighting inbox empty, no new Reddit comments. The 3 READY leads (Oxford x2, Madrid) have no approved photograph and own supply is paused, so they wait. health.py's smoke/deploy flags predate the 44px Add-a-photo fix (92166dd74); the 23:22 deploy succeeded and pushes are skipped by design.
For Hidde: 2 Reddit replies in drafts/batch-community-preview.md (r/lisbon Santa Iria photo ask, r/marijuanaenthusiasts Grizzly Giant).
The iOS workflow still reads failure (0.8h ago): log not read this attempt.

## 2026-10-24 23:44 window

- Rung 2: the smoke test was red because the new "Add a photo" pill on tree pages was 36px tall at 375px (floor 44). Now 44px on phones (style.css, `.addphoto-btn.tonal`), pushed as 92166dd74. Reader inbox empty. Not yet re-verified by a smoke run; the next smoke run will say.
- Rung 4: harvested 22 new Reddit comments (r/lisbon, r/sicily). The Sicily tips (Ortigia ficus, Villa Bellini, Agrigento olive) are already leads; 20 items closed with a reason. Two replies drafted. community.py had repeated rows per id, so a verdict closed only one copy and the preview listed the same reply four times; now one row per id and verdicts cover all. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md (the r/lisbon Santa Iria photo asks permission to use it; the Grizzly Giant thread).

## 2026-10-24, night run, twelfth attempt: nothing shipped

Nothing changed in the product. Same state as the eleventh: no claims, inbox empty, 3 READY leads (Oxford x2, Madrid) held by the supply pause, last real deploy green. For Hidde: paste supabase/tree-notes.sql to clear the Postbox check.

## 2026-10-24, night run, eleventh attempt: nothing shipped

Nothing changed in the product. No claims, inbox empty, 3 READY leads still held by the supply pause, site healthy (the "skipped" builds are log-only pushes; Postbox check is still only the unpasted tree_notes.sql). Reddit queue is the same as the tenth attempt: replies drafted, waiting for Hidde. The window's remaining work is Hidde's to unblock, not a run's.

## 2026-10-24, night run, tenth attempt (rung 4, community)

- No claims standing. 3 READY leads (Oxford x2, Madrid x1) left unwritten on purpose: own supply is paused under recovery mode.
- Reddit: harvested and watched, all 17 open items closed. 4 replies drafted for Hidde, left unposted. The Grizzly Giant draft had a wrong history claim (Grant and the 1864 act), so I rewrote it with no claim in it. 8 items closed with `--done`, each with its reason.
- For Hidde: 4 Reddit replies in drafts/batch-community-preview.md.
- For Hidde: Postbox check fails only because supabase/tree-notes.sql has never been pasted (sqlcheck: table tree_notes). Paste it and the check goes green.
- No mail batch started this run.

## 2026-10-24 20:05 window (ninth attempt): nothing shipped

Nothing changed in the product. Inbox empty. health.py still flags the Postbox check from 11:35; its log shows only sqlcheck naming tree_notes.sql as not pasted (the already-answered case, no site fault). The Reddit harvest found 0 new comments in r/lisbon and r/sicily, so the commenter still has not posted a tree location. READY is the same 3 own leads under the supply pause. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md still wait.

## 2026-10-24 eighth attempt: nothing shipped

Nothing changed in the product. No claims, inbox empty, READY is the same 3 own leads (oxford 2, madrid 1) under the supply pause, so no write pass. health.py's skipped builds and Postbox failure are the ones already answered. No new angle.

## 2026-10-24 seventh attempt: nothing shipped

Nothing changed in the product. No claims standing, inbox empty, READY is still 3 own leads (oxford 2, madrid 1) under the supply pause. The Reddit queue came back with the same duplicates and no tree tip. Nothing new to act on.

## 2026-10-24 sixth attempt: nothing shipped

Nothing changed in the product. No claims standing, inbox empty, READY is 3 own leads (oxford 2, madrid 1) held by the supply pause. health.py's skipped builds (log-only pushes) and Postbox failure were already answered; a deploy dispatched 16:49 is still running. No new angle on any rung, so I did not repeat earlier work.

## 2026-10-24 17:09 window (fifth attempt): nothing shipped

Nothing changed in the product. The inbox is empty, and health.py's 'skipped' builds and the Postbox failure are the ones already answered. Own supply is paused and READY is still 3 own leads. `private_store.py pull` brought back the Reddit queue with 17 open items, duplicates again, though the harvest found 0 new comments. None carries a tree tip, and the r/lisbon commenter has still not posted a location. I did not re-close the queue, because the next pull restores it. The queue and the pull need a fix: `--done` loses its effect once a pull restores the duplicates. For Hidde: the 2 Reddit replies in drafts/batch-community-preview.md still wait.

## 2026-10-24 (fourth attempt): nothing shipped, state re-checked

Nothing changed in the product. No claims standing, inbox empty, health.py's 'skipped' builds are log-only pushes (path filters) and the Postbox failure was already answered. READY is still 3 own leads (oxford 2, madrid 1) under a paused supply. The Stirling register retry has been tried on 10-15, 10-22 and 10-23 with no new angle, so I did not repeat it. Open for the next run: check the r/lisbon thread for the commenter's tree location; the 997 leads needing only a source could feed a verify pass on a staged US city (fort-worth, portland, san-francisco), which is leads-only work while supply is paused.

## 2026-10-24 (third attempt): Reddit queue closed for real, no trees

Nothing shipped to the product. No claims were standing; 3 READY leads (oxford 2, madrid 1) are own trees, and own supply is paused. The inbox was empty. `private_store.py pull` had restored the Reddit queue with duplicate ids, so the earlier `--done` calls were lost and `--done` only touched the first of two copies. I deduplicated data/outreach-community.json and closed everything without a tip. Two items stay open: the Santa Iria cypress photo ask (Hidde posts it) and the Grizzly Giant reply (the stale Grant draft is gone). One r/lisbon commenter (19riuyxs4wn0g) still owes a location; check that thread. Pushed to the private store.
For Hidde: 2 Reddit replies in drafts/batch-community-preview.md.

## 2026-10-24 (late window): Reddit queue closed, no trees

Nothing shipped to the product. No claims were standing. Only 3 READY leads (oxford 2, madrid 1), under the six-candidate minimum for a pass, and own supply is paused. The sightings inbox was empty. Reddit: 12 open items, 3 with drafts, the other 9 closed with `--done` (no tip, no location). I rewrote the Grizzly Giant draft, which wrongly put 1903 "earlier than Grant"; it was Roosevelt who camped with Muir. For Hidde: 3 Reddit replies in drafts/batch-community-preview.md. Archive-ask lead from the thread: digarb.hku.hk (HKU Hong Kong tree registry) and Gigantes Verdes (Portugal) as contacts.

## 2026-10-24 17:00 UTC, night run: Reddit queue worked, no tree made

Nothing changed in the product. Rung 1: no reader photographs waiting. Rung 2: the Postbox check failure of 11:35 was only sqlcheck saying tree_notes.sql was not pasted yet; the table has been live since, so I recorded the answer with health.py. Rung 4: harvested r/lisbon (32 comments) and r/sicily (none new), closed 11 open items with a reason (no tree tip in any of them) and drafted nothing new. Two earlier drafts wait.
For Hidde: 2 Reddit replies in drafts/batch-community-preview.md (the Santa Iria cypress photo ask in r/lisbon, the Grizzly Giant comment in r/marijuanaenthusiasts). Because that batch waits for his word, I left the mail batch and the archive asks alone tonight.
Nothing else was open: enrichment says nothing to do, no recognition lines are stuck, own supply is paused, and the only page gap is one species page that Google would not see anyway. Photo hunts for Google are off the ladder. One r/lisbon commenter says they will come back with the location of a tree; the next run should check that thread.

## 2026-10-24, session with Hidde: every website map shows the same tree card

- **Live with this deploy:** a tap on a tree on /explore (every language), the country and state maps and your profile map now shows the same Airbnb card as the city map, instead of jumping straight to the tree page. On a phone the card sits over the map above the sheet's peek; on a desktop it sits beside the pin. The card opens the tree and its heart saves.
- **How it stays one thing:** the tap lives once, in site/src/lib/map-card-js.ts, and every map calls it. qa.py `check_one_tree_card_on_every_map()` fails the deploy if a map builds its own card, opens a popup for a tree, or jumps straight to a page. Tested against the old code: it refuses all five map scripts.
- Checked through a proxy of the live site at 375px and desktop, on /explore and /lisbon: opening, closing with a map tap, the heart asking to sign in, and the pin released on close. The country and profile maps use the same function as /explore and were not opened in the proxy.

## 2026-10-24 late window: Reddit queue closed

- Nothing new is live on the site. The 3 READY leads (2 Oxford, 1 Madrid) are our own trees, so they wait under the supply pause (a new tree of our own needs an approved photograph). No claims were standing.
- Reddit: 15 open items, 13 closed (no tree tip, private land, or a pointer only), 2 replies drafted. The r/lisbon photo-permission reply and the Grizzly Giant reply are left unsent.
- For Hidde: 2 Reddit replies in drafts/batch-community-preview.md.

## 2026-10-24, 13:47 window (Sonnet): nothing new, nothing shipped

No trees shipped, on purpose: own supply is paused. Rung 1 empty (0 photographs waiting). Rung 2: health.py still lists the Postbox failure, the skipped smoke test and the unpasted tree-notes.sql migration; all three were answered earlier and need Hidde's Supabase login. Rung 4: harvest found 0 new comments; the 2 drafted Reddit replies already wait in drafts/batch-community-preview.md. Backup lane: Stirling is a RETRY target but was retried 10-22 and 10-23 with no register found, so not repeated. Nothing else on the ladder has work under recovery mode.

## 2026-10-24, last attempt (Sonnet): nothing shippable, nothing broken

Shipped no trees, on purpose. Own supply is paused, so the 3 READY leads (2 Oxford, 1 Madrid) wait. No claims were standing, no reader photographs waiting, `enrich.py --next` has nothing, and the `archive` outreach group has 0 ready.
- health.py's "Build and deploy keeps failing" is stale. The pal_001 feed-count failure was the 11:40 and 12:01 builds, before images.ts let source `mine` through `showable()`. The 12:25 build with the fix succeeded and the later runs skipped (LOG-only commits). Answered with `health.py --answer`.
- Still open, not touched: the Postbox check failure (1.8h old) and one migration not pasted into the database (`python3 scripts/sqlcheck.py` names it). Both need a look by someone with those logins.

## 2026-10-24, late attempt (Sonnet)

- Shipped no trees: own supply is paused, and the 3 READY leads (2 Oxford, 1 Madrid) are our own trees, so they wait.
- Deploy: health.py showed the pal_001 feed-count failure, but the 12:25 build with the images.ts fix succeeded; the newest run is a skipped log-only commit. No action needed.
- vendor_photos.py: 1 photograph vendored (pal_022).
- Reddit: closed 5 open items (no tree, no ask). 2 replies drafted. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md (the r/lisbon Santa Iria photo offer and the Grizzly Giant thread).
- Still open: the r/lisbon thread on the cypress with the metal frame and the Santa Iria location. The Postbox check failure was answered earlier.
## 2026-10-24 night run (13:15 window): rung 4, Reddit read, two replies drafted

**Nothing changed in the product this window.** Rung 1 empty (0 photographs waiting). Health: the Postbox check failure and the "migration not pasted" line are one cause, supabase/tree-notes.sql, already FOR HIDDE; answered with `health.py --answer`. Rung 4: harvest found 0 new comments, watch found 9 new posts; the 13 open items closed with a reason each, except two with a reply. **For Hidde: 2 Reddit replies in drafts/batch-community-preview.md:** (1) the r/Lisbon commenter's photograph of the Santa Iria olive (I looked at it: a big old olive with the information panel, our lis_036, which has no photograph yet), a reply asking if we may use it on the page; (2) the Grizzly Giant thread in r/marijuanaenthusiasts, a light reply that also gently corrects the 1903 camp (Roosevelt with Muir, not Grant), check that fact before posting. No new tree leads (the Evansville reserve and the Santa Iria image gave no placeable new tree). Mail batch: none drafted, the 10-23 batches still wait for his word; the `archive` group has 0 ready in contacts_db, no feeder yet. Own supply paused, enrichment says nothing to do, recognise --stuck and pagegaps have nothing worth a window (one species page, noindex under the strict cut).

## 2026-10-24 session: the tree page rebuilt, web and app (Hidde: "bouw alles")

**What changed in the product:** the tree page follows the day's benchmark (CONVENTIONS.md 2026-10-24 entries). Without a photograph the hero is the map with one card at its foot ("No photograph yet. Been here? Yours would be the first on this page." and Add a photo). Under the title only the district and the park link, the crumb at the top keeps the path. The story folds to about six lines with Read more. "Getting there" is one block with a heading: address, how to recognise it (its own row, the eye), access only when there is something to meet (1,266 "Free, public park" lines now say nothing), transport. New section "From people who stood here": one note per person per tree, dated, public the moment it is written, the name only from a public profile, else "A visitor"; empty, it borrows the nearest tree's real note, else a ghost example; one button, "Leave a note for the next visitor", the prompt inside the sheet. Eight languages. Same sections in the app (branch tree-page-app, next build): map hero, folded story, Getting there, notes with the BrandSheet, `-notesdemo` for the sweep, SignedOutWalk.testNoteAsks.

**Machinery:** supabase/tree-notes.sql (table, RLS, GRANT, `tree_notes_for()`); scripts/tree_notes.py (`--new --seen`, `--hide <code> <tree_id> "why"`) runs at every knock. **Live first for photographs:** `sightings_publish.py --live-first` at every knock puts a reader's photograph in the strip of a tree that already has a lead (photo-less pages keep the judged path, since the strip's first picture would become the hero); `--unstrip <sighting_id>` undoes one, the judge's approve promotes, hold or reject removes; the digest's machine part lists each with its undo. Schema accepts `source: "mine"` (the Piazza Marina fig had broken every build since 10:01).

Hidde pasted supabase/tree-notes.sql the same afternoon (the first try ran an old tab's SQL and failed on an `events` column; a clean tab succeeded) and the block shows on the ginkgo page. The app's tree page is merged to main, carried by the next build.

**Not done:** the collect sheet's optional "What did you see?" field (CONVENTIONS.md names Strava and Polarsteps as the reference for the next build); the night run does not yet quote a visitor's note into a story (reader_words.py reads sightings only).

## 2026-10-24 session: three UNLV trees get photographs from the campus grounds superintendent

**What changed:** the weeping mulberry, Camperdown elm and Texas olive in Las Vegas have photographs mailed by UNLV's grounds superintendent (answering our 10-07 mail), uncredited per the mailed-photo ruling, pins moved to his coordinates and confirmed (two geotags agree within 20 m). They now count as reader content, so the three pages and /las-vegas go back into Google. Two colon reveals in those stories rewritten. `outreach_inbox.py --save-from <address>` now saves one matched sender's attachments to out/mail-photos/. **For Hidde:** reply drafted in drafts/reply-james-kearney-2026-10-24.md; he says more photos follow.

## 2026-10-24 session: the night run asks for photo archives, no more Commons hunting for Google

**What changed:** rung 4 now drafts archive asks after Reddit: societies, photographers and ambassadors who hold photographs of our trees that are on no open site, asked to let us use them, credited (new group `archive` in OUTREACH_STRATEGY.md and contacts_db.py, first among the groups). Commons photo sweeps only when nothing else is left, for readers. Why: one archive gave Copenhagen 32 pages in Google, all readers together 51 photos. **For the night run:** the `archive` group has no feeder script yet; start from the warm repliers (society 12, garden 6), the ambassadors and the societies in data/outreach-contacts-*.json, and log what a feeder would need.

## 2026-10-24 session: the reader cut, Google sees only pages with reader content

**What changed:** Google is now asked to show only tree pages with something a reader gave us (a unique photo, a reader's photo in the strip, a reader-found tree) and the place pages of cities where one tree has it, plus home and the site's own pages (Hidde: "ik ga liever te ver en voeg langzaam weer dingen toe"). 105 tree pages and 27 place pages in 34 cities stay, down from 598 tree pages; 1,413 more pages carry the googlebot noindex, Bing keeps everything. `READER_ONLY` in scripts/thin_pages.py, one flag back. A reader's photograph on a tree returns its page by itself. **For the night run:** Commons photos no longer put a page in Google; the photo lane prepares the first step back (data/index-kept.json still names the demand cut's 108 cities), reader input is what grows the index. **Not verified locally:** qa.py needs the Astro build, so the split check runs in CI on deploy.

## 2026-10-24 session: the night run reads Reddit for Hidde (rung 4)

**What changed:** the night run's ladder has a new rung 4, communities and outreach, above enrichment while recovery mode holds (Hidde: "refocus the nightrun on outreach and local community posts if you find an effective way"). Why: Google Analytics shows 3 to 6 people a day before the r/Lisbon post and 11 and 15 on 10-22 and 10-23, while 7 night runs on 10-23 made 0 trees. `scripts/community.py` reads every comment under his posts and new threads about an old tree (four tree subs plus the city subs he posted in) from the Arctic Shift archive, since Reddit refuses us. The run turns tips into leads, drafts replies into drafts/batch-community-preview.md (private), and he posts them; it never posts and never keeps a username. Then one mail batch draft a night through OUTREACH_STRATEGY.md's daily rhythm when none waits for his word. **First pass:** r/Lisbon 19 comments, 12 already answered by him, 7 open, one a photograph of the Santa Iria olive he asked for; 10 threads, two worth a reply (the Grizzly Giant, which we have; Evansville's tulip poplars, a tip). Renumbered: enrichment is rung 5, registers 6, photos 7, recognition 8, page gaps 9, product 10. **Gap:** the archive holds the r/sicily post but none of its comments yet, so an empty harvest proves nothing. Not done here: no reply drafted, that is the night run's first job.

## 2026-10-24 night run, restart after early stop

Nothing new live. No standing claims. READY leads were 3 (Oxford 2, Madrid 1), own supply is paused and they have no photographs, so none written. Ran the kept-set photo sweep (`photo_hunt.py --recheck`) and a photo-judge pass over the 35 trees with unjudged candidates (Singapore, Amsterdam, Chicago, Utrecht, Budapest): 712 candidates, 0 approved, 1 held (sgp_027, earlier closer-geotag hold kept). Commons is spent for the kept set; further photos need iNaturalist or readers. Not done: iOS app workflow shows FAILED (newest finished run 10-23), not investigated this attempt.
## 2026-10-24 which tree gets the full pin: photograph, then readers' saves (live, web and app)

Hidde, looking at the new maps: "it looks good tbh" and, on the order, "i think photo and likes are the best way." The likes are readers' Want to go saves, which never reached the build. scripts/tree_saves.py counts them per tree from Supabase (counts only, our own accounts left out) into data/tree-saves.json, nightly from data-digest.yml; lib/saves.ts reads it, every map's features carry `pr` from one `pinPriority(hasPhoto, saves)` in lib/map.ts, the app feed carries `saves` and TreeMap.swift uses the same arithmetic (qa holds them equal). First count today: 38 trees saved by readers, 39 saves, so for now the photograph decides almost everywhere and the count grows with the people.

## 2026-10-24 session: r/sicily's second day, the Villino Favaloro fig live

**In the product:** /palermo/white-fig-of-villino-favaloro (pal_022), a reader tip from the thread: a white fig (Ficus virens), 10 m round and 20 m tall by MASAF and the Regione Siciliana list, sheet 18/G273/PA/19. It leans out of the closed garden of the Basile villa on Piazza Virgilio and is seen from the street. BlogSicilia 2023 is the second source. A CC BY 4.0 Commons photograph by Esculapio, taken 2026-10-02, was looked at and approved, and it is also the life check. The reader's words are quoted on the page in English and Italian. It is in the Sicily collection (now 14 trees). Pin is approximate, register point by the railings. **Leads:** the Ficuzza oak (Palermo leads, no register row), the Ortigia fig and the Zimmiti cactus (Syracuse), and the "Innari" olive (Sardinia file, place unknown). **For Hidde:** replies for the five new comments are in drafts/reddit-sicily-replies-2026-10-24.md. Chloe_Lifter's "How old is this tree?" gets no draft because it is unclear which tree it means. The build runs in CI only, so the page has not been looked at rendered yet.


## 2026-10-24 later attempt in the 08:34 window: nothing shipped

- No claims standing, inbox empty, READY still 3 own trees without photographs (supply paused), so no write pass. iOS red is still the 30-minute `xcodebuild` hang on the large phone (run 40017321068); needs a Mac session.
- `photo_hunt.py --recheck` swept 40 trees in the kept set: 0 new candidates. Photo queue holds nothing newly judgeable.

## 2026-10-24 08:34 window: nothing shipped

- Inbox empty. health.py exit 1 is the same iOS hang plus the push-skipped smoke test. Supply paused, READY is 3 photo-less own trees, so no write pass.
- `photo_hunt.py --recheck` found 0 new candidates; `photo_fetch.py --roster` fetched 2 (lux_009, iNat leaf and seedling close-ups). I looked at both and they are not the tree; `photo_verdicts.py` refused the reject ("no candidate matching luxembourg-city"), so nothing was recorded. Not debugged.

## 2026-10-24 night run, restart after early stop: nothing shipped

- No claims standing, sighting inbox empty. READY leads are 3 (Oxford 2, Madrid 1), all our own trees, held by SUPPLY_PAUSED and ADD_NEEDS_PHOTO, so no write pass.
- iOS red is the known SweepFrames xcodebuild hang (killed at 30 min, run 40013002762); needs a Mac session. Smoke "skipped" is the normal push-skip.

## 2026-10-24 night run (02:55): nothing shipped

- Inbox empty, READY still 3 photo-less own trees (supply paused), prepare.py shelf unchanged. health.py exit 1 is the same iOS appfit hang (run 40017321068) plus a skipped smoke test; no source fix possible from Linux. Stirling RETRY not repeated: already stalled twice on 10-23. Nothing new since the sixteenth attempt; waiting on Search Console or a reader's tree.
## 2026-10-23 night run, sixteenth attempt: nothing shipped

- No claims standing, inbox empty, READY is 3 photo-less own trees (oxford 2, madrid 1) and `SUPPLY_PAUSED` is True, so no write pass. `enrich.py --next`, `recognise.py --stuck` and `pagegaps.py` all report nothing to do. The 54 "awaiting a writer" trees cannot go live while supply is paused.
- I reran `photo_hunt.py --recheck` against the fifteenth entry's note: 0 new candidates again. Stirling was retried twice today already, still stalled. iOS failure is the same appfit hang, nothing new.
- Do not rerun any of the above until Search Console moves or a reader's tree arrives.
## 2026-10-23 night run, fifteenth attempt (22:50): nothing shipped

- Inbox empty, READY the same 3 photo-less own trees (supply paused). health.py exit 1 is only the iOS app: both failed runs (40013002762, 40017321068) died in appfit's `xcodebuild test` hanging past 30 minutes on the iPhone SE simulator, then the 110-minute cap; the appsweep after it produced 40 screenshots. A runner hang, no assertion failure, and the run before succeeded, so no source fix is possible from this runner. For Hidde: nothing yet; if the next scheduled iOS run hangs too, the SweepFrames step needs a look on the Mac.
- I reran `photo_hunt.py --recheck` against the fourteenth entry's note: 40 trees, 0 new candidates, as predicted. Do not rerun.
- Open lane remains `scout_next.py --target` (RETRY Stirling).
## 2026-10-23 night run, fourteenth attempt: nothing shipped, one finding

- Claims none, inbox empty, READY is the same 3 own trees without photographs (supply paused). `enrich.py --next`: nothing anywhere. `photo_gaps.py --shortlist`: nothing queued, every candidate already judged.
- Correction to the thirteenth entry: `photo_hunt.py --recheck` re-asks the same first 40 trees by design, and the "1025 unchecked" line counts the recheck pool. Plain `photo_hunt.py` says 0 unchecked: the kept set is fully swept. Photo lane is exhausted until new uploads appear; do not rerun it.
- `scout_next.py --target` names RETRY Stirling (#266): the one open lane for the next window.
## 2026-10-23 night run, thirteenth attempt: nothing shipped

- No claims standing; sightings inbox empty. READY leads are 3 (Oxford 2, Madrid 1), all our own trees without a photograph, so `ADD_NEEDS_PHOTO` and the paused own supply keep them waiting.
- `photo_hunt.py --recheck` run twice: both swept the same 40 kept-set trees (ali, ams, arn), 0 new candidates; the sweep does not advance past them. A session with time should look at why the other ~985 unchecked photo-less trees are never reached.

## 2026-10-23 night run, twelfth attempt (19:44 window): nothing published

Rungs 1 and 2 clear (0 reader photos waiting, health.py clean, 0 BLOCKER). Own supply is paused, enrichment says nothing to do, `recognise.py --stuck` and `pagegaps.py` are empty. `photo_hunt.py --recheck` swept 40 kept-set trees: 0 new candidates, so no viewing pass. Scout target Stirling was already retried earlier today (still stalled), so I did not repeat it. Nothing refused in the shell.

## 2026-10-24 every map draws pins the Airbnb way, never counted bubbles (live, web and app)

Hidde, an hour after the city map got bubbles: "je wil ook niet nodeloos bubbels openklikken ... kun je deze interactie bij airbnb onderzoeken". Airbnb and Google Maps never pile a results map into counted bubbles (benchmark in CONVENTIONS.md); shown Lisbon both ways, he chose: "Doe de Airbnb-manier overal ... Web en app." Now on every map (city, /explore, country and state, My trees, the app): every tree drawn, a full pin where none stands within 40 px (lib/map.ts PIN_DISTANCE, TreeMap.swift pinDistance), photograph first, a dot for the rest, a tap always opens the tree, nothing zooms for you. The app's own grid clusterer is gone; MapLibre's symbol collision places the pins there and on the circle-pin maps, the city map does the pass over its DOM pins. The one bubble left is a same-spot stack, from zoom 14 only (STACK_ZOOM, stackZoom). Checked on mocks of the live pages at 375px and desktop (Lisbon 18 pins and 18 dots at the opening zoom; explore 98 pins and 2,731 dots over Europe; Italy; My trees filled and hollow) and in the simulator (Lisbon, the Ajuda stack); the app built twice and its unit tests pass. qa `check_every_map_shows_pins_the_same_way()` refuses a clustered source, the old grid, or the two numbers drifting. DECISIONS.md 2026-10-24, CLAUDE.md one line. Not done: the night's three cluster tests were replaced by three pin-rule tests; a walk through the UI test sweep on CI will say whether the grid tap still lands.

## 2026-10-24 city map piles its own trees like every other map (live)

Hidde, on /lisbon (36 trees): the city map drew every species pin over the others zoomed out while /explore, the country maps, My trees and the app showed counted bubbles ("kunnen we die interacties gelijk houden?"). The city map now carries a clustered source of its own trees that decides which DOM pins show and draws the same moss bubble with the count, from the shared numbers in lib/map.ts (radius 13, distance 40, piles to zoom 14); a tap zooms to where the bubble parts, past zoom 14 the species pins and the same-spot stacks are back, and a selected tree flies to 15.5 so its pin never lands inside a bubble. Checked on a mockup of the live pages at 375px and desktop: Lisbon 6+2+16+10 plus two pins, Palermo, London 27 in six piles plus five, Bruges one 2 beside two pins. qa `check_every_web_map_piles_with_the_same_numbers()` refuses a map file writing those numbers as literals. CONVENTIONS.md "How close two pins have to be" got the dated line. Seen in passing, not fixed: /london at 375px opens at zoom 8.4, below FAR, so the live page shows one 32 bubble and no pins until you zoom in.

## 2026-10-23 night run, eleventh attempt: nothing live, photo lane nearly empty

No claims stood. READY is still 3 (Oxford 2, Madrid 1) and own supply is paused, so no write pass. `photo_fetch.py --roster` had only four images left to look at, and I viewed them: 3 rejected (seedling leaves twice at lux_009, a dark horse chestnut for the plane tri_032), 1 held (tri_003: a good giant sequoia 89 m from the pin where the entry says Ghost Pine, so trunk and species need a check). Approved 0. The sweep of the kept set is close to exhausted; the next lever is checking tri_003 or Hidde lifting the pause.

## 2026-10-23 night run, tenth attempt: nothing published

No claims stood. READY is still 3 (Oxford 2, Madrid 1), none with a photograph, so own-supply rules stop them. `photo_hunt.py --recheck` swept the same first 40 kept-set trees (Alicante, Amsterdam, Arnhem) again: 0 new candidates, so the sweep order needs to advance before it is worth running again. Nothing dispatched.

## 2026-10-23 night run, ninth attempt: nothing published

Resolved a LOG.md rebase conflict with the city-map entry and pushed. No claims stood. READY is 3 (Oxford 2, Madrid 1), none with a photograph, so `ADD_NEEDS_PHOTO` and `SUPPLY_PAUSED` stop a write pass from shipping them. enrich.py reports nothing to do, the Stirling register was retried earlier today, and a verify pass on a staged city would only add leads that cannot go live. Nothing dispatched.

## 2026-10-23 night run, eighth attempt: nothing published

Inbox empty, health.py clear. `photo_hunt.py --recheck` swept 40 more kept-set trees (Alicante, Amsterdam, Arnhem), 0 new candidates. Own supply is paused and READY is 3 without photos; scout_next names Stirling, already retried today. Nothing dispatched.

## 2026-10-23 night run, seventh attempt: nothing published

No claims stood. READY is still 3 (Oxford 2, Madrid 1, no photos, supply paused). Staged-city and refill advice only adds leads while `SUPPLY_PAUSED` holds; Stirling register already retried today. Nothing dispatched.

## 2026-10-23 night run, sixth attempt: nothing published, photo lane checked

No claims stood. READY is 3 (Oxford 2, Madrid 1, no photos, supply paused). `photo_hunt.py --recheck` swept 40 kept-set trees (Alicante, Amsterdam, Arnhem), 0 new candidates. A photo-judge pass found every fetchable candidate in the kept set already judged; 720 unjudged are last-resort (no geotag, or 30 to 100 m off the pin). It viewed the 7 nearest, all wrong subjects, 8 rejects recorded (6de16587b). No approvals. Next photo step is a by-name sweep on the 35 trees left, not another viewing pass. Pillow was missing on the runner and was installed.

## 2026-10-23 night run, fifth attempt: nothing published

Sightings 0. health.py again flags "deploy skipped", which is pushes superseding each other (the latest deploys were in progress, not failed). Supply is still paused, READY is 3 without photos, and the 92 staged cities would only add leads. Nothing dispatched, nothing refused by the shell.

## 2026-10-23 night run, fourth attempt: nothing published

No claims stood. READY is 3 (Oxford 2, Madrid 1, no photos, supply paused, so no write pass). Enrichment and page gaps: nothing to do. prepare.py's staged-city and refill advice assumes supply is open; with `SUPPLY_PAUSED` a verify pass would only add leads, and the walls already hold the likely cities. Stirling already retried three times today, not repeated. Nothing dispatched.

## 2026-10-23 night run, third attempt: nothing published

No claims stood. READY is still 3 (Oxford 2, Madrid 1, no photos). The written batches parked earlier (photo-batch-2: 10, texas-famous: 4) are own supply, so they stay unmerged while `SUPPLY_PAUSED` holds. Sightings 0, enrichment nothing to do. health.py's "deploy skipped" is only cancelled or skipped runs from pushes landing close together, not a failing build.

## 2026-10-23 night run, second attempt: nothing published

No claims stood, READY is 3 (Oxford 2, Madrid 1, no photos, supply paused). `photo_hunt.py --recheck` swept 40 more trees, no new candidates. Claimed Bamberg for a verify pass, found it already holds its 9 trees and only 6 open leads, released it (now a 48h wall in data/walls.json). Munich is full (63 of 60). Stirling register retry was done in the first attempt. Nothing worth dispatching while supply is paused.

## 2026-10-23 night run (14:28 UTC window): nothing published, supply paused

Rung 1 and 2 clear (0 sightings waiting, health green). Own supply is paused, so no tree work. Ran `photo_hunt.py --recheck` (40 trees swept, no new candidates) and fetched the only four queued candidates: two Luxembourg sycamore saplings (not the tree), a giant-sequoia photo for the Trieste Ghost Pine (species mismatch) and a worm's-eye chestnut for the Trieste plane (wrong species, no frame). All four rejected, nothing approved. Enrichment, recognition lines and page gaps all say nothing to do. Scouted Stirling again (rung 5): only Inchmahome yews/oaks and the Bridge of Allan sequoia as leads, still stalled, note in data/register-scouting.json. READY leads (Oxford 2, Madrid 1) have no photo, so they wait. Nothing refused by the shell.

## 2026-10-24 session: map list comes down again with no trees in view

App: a raised list on the map stayed stuck once no trees were in view (Hidde's report). The empty-list lock now stops raising only, never lowering (BottomSheet.swift). Checked on the iPhone 17 Pro simulator: raised over Amsterdam, panned to Ruigoord, dragged down to peek, and an upward swipe still leaves it down. For Hidde: next build carries this fix.

## 2026-10-24 session: the six weeks concentrate on Lisbon

After the cold-start research (reports/Kip ei start van content apps.md: nine apps, every one grew contributors in one dense place with a few named people), Hidde chose Lisbon ("Yes, Lisbon"). GO_TO_MARKET.md carries the revised plan and the measure: Lisbon trees with a stranger's photograph, 5 today, ten by 2026-12-05. Lisbon stands at 36 trees, 18 approved photos, 32 confirmed pins; Commons is judged out for the 18 photo-less trees (every candidate rejected by 10-19), so photographs come from people. A search pass found fifteen people and bodies who already photograph Lisbon's trees (drafts/lisbon-ten.md, local: Commons uploaders, three juntas, Gigantes Verdes, a tree-walk organiser), and ten first mails are drafted in drafts/lisbon-ten-mails.md, one tree each, for Hidde to send two or three a week. Side finding: JF Penha de França's felling notice of 10-20 on Praça Paiva Couceiro is a white poplar, not our ginkgo (lis_008 stands). Instagram: six posts drafted as a business card (drafts/instagram-first-six.md).

## 2026-10-24 session: Wilder's article is out, four followed links

wilder.pt published the Lisbon interview on 2026-10-23 (Ines Sequeira): links to the home page, /lisbon, /porto and /contribute, all followed, no App Store link. The second press placement ever and the first with links. Watched by backlinks.py, contacts_db marks Wilder linked, details in drafts/OUTREACH.md. Nothing in the product changed; the digest's GA and Portugal download rows are where it shows from 10-25.

## 2026-10-24 session: Show HN posted

Hidde posted "Show HN: I'm mapping the old trees worth walking to (3,800 so far)" at 15:04 Dutch time, news.ycombinator.com/item?id=50208440, from his own account; first comment in his About-page voice with the AI paragraph in his own framing (drafts/show-hn.md, local). Measure over the week: points and comments on the item, visitors with referrer news.ycombinator.com in Google Analytics, submissions and accounts. OUTREACH_STRATEGY's "later or not at all" was replaced on his word on 10-23.

## 2026-10-23 session: Reddit threads (r/Lisbon, r/sicily), a Sicily collection, the Messina fig live

**In the product:** /collections/sicilys-most-remarkable-trees (13 trees: Palermo, Catania, Sant'Alfio, Messina) as the page Hidde's r/sicily post links to in its edit; out of Google like every collection under the strict cut. /messina/the-moreton-bay-fig-of-villa-mazzini is the first tree from a Reddit tip to go live: regional register sheet 05/F158/ME/19 (25.13 m round) plus LetteraEmme 2020, a CC BY-SA Commons photograph with the board in front of the trunk, looked at. **Rule:** a stranger's public tip is a reader's tree under the supply pause (`found_by_reader.tip`, findable.reader_added; CLAUDE.md). **Outreach:** a post is for people, not tips, the name goes in every thread (OUTREACH_STRATEGY.md); HIS_VOICE got his AI line and the no-photo-ask-by-reflex lesson. **Leads:** Seia (Souto da Lapa chestnuts, the tipster's photos were off the internet), Agrigento (7 Valle dei Templi register trees, a walk; the Borgo Giallonardo olive blocked on hotel grounds), Syracuse, Pozzallo. r/sicily gave 8 places in two hours and no accounts; GA referrals to check tomorrow for both subs.

## 2026-10-23 session: Mapillary tried as a photo source

Two trees looked at in the viewer (Catania figs, Den Bosch plane): coverage at both, frames from dashcams and walks where the tree is at the edge or out of shot. Verdict in OPEN_DATA_SURVEY.md: a dated life check, rarely a photograph; the API needs a free token Hidde would have to create. Nothing in the product changed.

## 2026-10-23 session: the Season Radar case, answered; Plus parked; one digest row
Made the case that Season Radar (a dated push) is the retention hook and the paid feature (docs/season-radar-case.md, conventions looked up in CONVENTIONS.md: Weathernews 紅葉Ch., eBird, Audubon, AllTrails, Strava, Apple; mockup beside the reference in a preview). Hidde was not convinced and was right: return is a monthly, trip-shaped thing, season is content, and the open question is the Plus step once people upload trees, which is parked until free traction (DECISIONS.md 2026-10-23). Today's cohorts: 103 stranger phones, 60 opened on one day only; back within 7 days 1 in 3 in September, 1 in 5 in October (not the 1 in 13 quoted on 10-22). **Digest: unchanged in the end.** A row under "Phones back within 30 days" (how many of those saved, ticked or photographed a tree in those 30 days) was built, widened and removed within the hour on Hidde's word ("slechte titel en vraag me af of dit nou het getal is"): his seven headline numbers already say whether there is free traction. What the exercise did settle: of the 23 phones back on three days or more, 10 gave something and 13 never, so the session's line that "the ones who come back are the ones who contribute" was wrong. Nothing in the product changed.

## 2026-10-23 night run, fourth attempt: nothing new, said plainly
Nothing changed on the site. No claims, READY leads still the same 3 (photo-less, supply paused). `photo_hunt.py --recheck` swept 40 more kept-set trees (Alicante, Amsterdam, Arnhem): 0 new candidates. Stirling already retried yesterday. Remaining kept-set photo-less trees: about 985, same sweep next run.

## 2026-10-23 night run, third attempt: two species intros
Wrote the two missing species intros (Sugar Maple, Eastern White Pine) from the site's own trees; `pagegaps.py --check` now clean. Bing only while the strict cut holds. Not built or qa-run here (no site/dist). Nothing else workable: claims empty, READY leads photo-less under the supply pause, enrich empty.

## 2026-10-23 night run, second attempt: nothing to do, said plainly
Nothing changed on the site. No claims standing. READY leads (3: Oxford x2, Madrid) have no approved photograph and own supply is paused (`SUPPLY_PAUSED`), so no write pass. Written-and-ready batches (photo-batch-2, texas-famous) are held by the same pause. `enrich.py --next` and `photo_gaps.py --shortlist` empty; pagegaps only species pages, which the strict cut keeps out of Google. Stirling register retried yesterday and stays stalled. iOS fix (FlowWalk) is running in CI. Open for Hidde: when own supply restarts, photo-batch-2 (10 trees) and texas-famous (4) are ready to merge.

## 2026-10-23 night run (09:00 UTC): photo recheck on the kept set, nothing live
Nothing changed on the site. Rung 1 empty (0 sightings). Rung 2: the iOS app failure of 10-22 is a FlowWalk assertion (search-to-a-tree has no way back after the first result); a fix commit is already running in CI, so left alone. Own supply is paused, so I ran `photo_hunt.py --recheck` (no new candidates) and `photo_fetch.py --roster`, which fetched 7 images for Luxembourg, Como and Trieste. I looked at them: a sycamore seedling, a magnolia and a statue, a dark chestnut shot, and a giant sequoia against our Monterey Cypress. All 8 candidate urls rejected via photo_verdicts.py (the `page` field must hold the candidate url, not the city). prepare.py printed no 7-day visits line.

## 2026-10-23 session: readers' photos lead the page, and readers hear when theirs is live

What changed in the product: a reader's photograph now becomes the LEAD on a tree's page, the old lead moving into the strip ("if google appreciates them as lead better then make them lead"; `unique_photo()` reads the lead only). Applied to the three trees that had one as an extra only (cma_001, lis_030, tkc_001). And a reader whose photograph goes live gets a mail: the first at once, later ones bundled, at most one per 30 days (text he approved in drafts/photo-live-mail.md; sent by nightly.yml's mail step). The weeping cedar's reader is queued for the first one. Hidde agreed on the cedar (judgement filed). The red iOS check is one flaky test (search-to-a-tree in FlowWalk, 229 of 230 pass); not fixed.

## 2026-10-23 session: source batch sent, Season Radar session started

Hidde: "verstuur een batch!" The source batch of ten (people-run sites our tree pages cite, link ask) went out, then on his second word press round 4 (ten regional desks) and tourism batch 2 (Porto, The Hague, Ede, Cagliari): 24 mails today. Every desk from the 10-20 press list is now mailed; round 5 needs new desks from the kept set. Sent log and contacts database in the private store. A separate session makes the case for Season Radar as the retention lever, honestly, with references; nothing built.

## 2026-10-23 second restart: nothing to ship

No claims; READY still 3 leads without photographs; inbox empty; supply paused. `photo_hunt.py --recheck` found 0 new candidates in its 40-tree slice. `vendor_photos.py` still cannot downscale bne_004 and chi_023 (no Pillow on this runner). Deploy dispatch refused (HTTP 403 from this token), so the live site stays behind main until the next scheduled build. For Hidde: nothing.

## 2026-10-23 restart attempt: nothing to ship, and why

No claims standing. READY holds 3 leads (two Oxford, one Madrid), none with an approved photograph. The 15 written trees (photo-batch-2, texas-famous, ftw_018) and the 11 held city files are not waiting on the pace cap any more: own supply is paused (SUPPLY_PAUSED), per data/research/held-pace-2026-10-22/README.md, so merging them would break the 10-22 ruling. Stirling register was retried earlier today. Refill and verify lanes add leads only, and the shelf already holds more than the paused supply can use. No trees added.

## 2026-10-23 03:00 window: photo sweep and vendoring, no new trees

- Rung 1 inbox empty. Rung 2: Smoke skipped (push condition) and iOS failure (FlowWalk, needs a Mac) answered in health.py. Supply paused and READY leads lack photographs, so no write pass.
- `photo_hunt.py --recheck` swept 40 kept-set trees; photo-judge viewed 13 files for 16 trees, approved none (park-wide aerials, sculptures, a mineral; The Hague beech has no geotag). Kept-set queue has no unjudged candidates left.
- `vendor_photos.py` put 22 photographs on our own domain; bne_004 and chi_023 failed to downscale (Pillow missing on this runner), still to vendor.
- For Hidde: nothing.

## 2026-10-22 restart attempt: nothing shipped, no claims standing

No claims standing. READY has 3 leads (2 Oxford, 1 Madrid): the Oxford ones are approximate pins with no photograph (one a young oak, one a 2008 sighting needing a life check), so `ADD_NEEDS_PHOTO` and the supply pause keep them out. Staged cities need a verify pass but own supply is paused; Stirling was already retried. Nothing useful to dispatch under the rules.

## 2026-10-22 late attempt: nothing shipped, Stirling retried

No standing claims. READY is Oxford 2 and Madrid 1, both without an approved photograph, and own supply is paused, so no write pass. Enrichment: nothing to do. BACKUP register retry, Stirling: Wikidata within 25 km holds only the Wallace Oak (Torwood, Falkirk), already a lead in glasgow.json. Verdict stays stalled, note updated. Honest result: nothing useful left on the ladder under recovery mode.

## 2026-10-22 22:55 window: iOS failure read, nothing shipped

Rung 2: health.py flags the iOS app run of 20:24 (1h48m). Log: 229 passed, 1 failed, `testEveryFlowLeavesAWayBack`: flow "search-to-a-tree" has no tab bar, back button or dismiss after "first-result". No ios/ commit since the green run of 11:34 (only a test string), so this is a data/feed change or a flaky tap, not an app edit; it cannot be reproduced on this Linux runner and the night run never builds the app. For Hidde or a Mac session: rerun ios.yml once; if it fails again, look at the first search result's tree screen (the SearchFlow in FlowWalk). Reader inbox empty, READY leads still only Oxford 2 and Madrid 1 (own supply paused), enrichment says nothing to do. No deploy dispatch attempted (403 earlier).

## 2026-10-22 session: three outreach batches on Hidde's desk for 10-23

Press round 4 (the ten regional desks left from 10-20, autumn hook where the page has it), a source batch of ten people-run sites our pages cite, and tourism batch 2 (Porto, The Hague, Ede, Cagliari). All drafted, mailcheck and dry runs clean, every link 200, previews in drafts/batch-*-2026-10-23-preview.md (private, pushed to the private store). Nothing sent; his word goes into approved_word first. Inbox read: nothing waits for a reply.

## 2026-10-22 r/Lisbon thread read: replies drafted, Gigantes Verdes scouted

- Hidde's r/Lisbon post (16 upvotes, 2.3K views after 8h). New since the last pass: a commenter posted a photo of the Santa Iria olive (lis_036, no photo yet); others pointed to Gigantes Verdes, a volunteer big-tree map. Replies for him to post are in drafts/reddit-lisbon.md (photo permission ask first, then the tracking question, the cork oak, a grandparent memory to quote on lis_003 with consent).
- Gigantes Verdes (Associação VERDE): all rights reserved per their terms, so blocked as a source to import, a finding aid only; recorded in data/register-scouting.json. Permission would be an outreach mail, only if Hidde wants it.

## 2026-10-22 fifth attempt: nothing shipped, nothing live changed

- No claims standing. READY leads: 3 (oxford x2, madrid x1), but own supply is paused and none has an approved photograph, so none can ship. Awaiting-a-writer files are the same story, plus several duplicate-by-coordinate flags (las-vegas, london, munich, new-york, taiwan, washington-dc) that passcheck --pending says to fold by hand.
- `photo_hunt.py --recheck` swept 40 kept-set trees: 0 new candidates. `photo_fetch.py --roster` fetched only 7 images (luxembourg-city, como, trieste), too few for a photo-judge pass.
- Stirling register retry (BACKUP): its note's next angle is Wikidata/OSM nodes, a research hunt with low yield while supply is paused. Not started; status left as stalled.
- Deploy not dispatched (403 in earlier attempts).

## 2026-10-22 fourth attempt: nothing to ship, deploy still not dispatched

No product change. No claims stood. Reader inbox empty. READY leads are only Oxford 2 and Madrid 1 (own supply, paused, no write pass). `photo_hunt.py --recheck` swept the kept set again: 0 new candidates, nothing left unchecked. The Brisbane hero fix (bd86678a6) is on main, but both push-triggered deploys were "skipped" and `gh workflow run deploy.yml` returns 403 from this token, so the site is still not confirmed rebuilt. For Hidde: dispatch Build and deploy once (or let the next knock do it) and check that it goes green.

## 2026-10-22 19:41 window: deploy fix (Brisbane hero), nothing else to publish

Rung 2: the Build and deploy run of 18:05 failed on qa's soft-hero check (Brisbane hero, the City Botanic Gardens banyan, was the 500px iNaturalist rendition while 3648px photos sit elsewhere in the city). Switched that same photograph to its 1024px `large.jpg` rendition (checked 200 OK) in data/cities/brisbane.json, preflight 0 problems, pushed as bd86678a6. The push's deploy run came back "skipped" in 9s, so the site is not yet confirmed rebuilt: the next run should check `gh run list --workflow=deploy.yml` and dispatch a deploy if it is still red. qa.py cannot run here (no site/dist, build is refused). No reader submissions waiting. `photo_hunt.py --recheck` swept 40 kept-set trees: 0 new candidates. Enrichment says nothing to do; own supply is paused, so the 54 awaiting-writer trees and READY leads were not touched. Nothing else shipped.

## 2026-10-22 third attempt: Minneapolis register retried, nothing shipped

No product change. No claims stood. READY leads (Oxford 2, Madrid 1) are own supply and own supply is paused, so no write pass. Retried the BACKUP register: the MPRB Heritage Tree page renders now but gives no licence, says trees may be on private land, and offers only a Google My Map; still not imported (note and "retried" date in data/register-scouting.json). Next angle: mail MPRB for the list and licence; Hidde sends.

## 2026-10-22 photo viewing pass pj2 on the kept set: nothing approved, 70 rejects recorded

No product change: no tree gained a photograph. 32 images looked at as pixels (Arnhem arn_004/005/007/008/021/026/027/028, Florence flo_007/016, Kagoshima kag_011, Baarn brn_007, Utrecht utr_006/007/031, Nijmegen nij_019/020, The Hague hag_024/027/028/030, Vienna vie_035/036, Singapore sgp_015, Amsterdam ams_016/027, Brisbane bne_005/013); 70 tree-candidate rejects written to data/photo-queue.json so none is judged again. Approvals: none, so no reversal commands. The swept Arnhem candidates are sculptures (Pluto, VLUCHT) with trees as background; the rest are monuments, information panels, buildings, swans, overviews, two black-and-white archival street scenes, and an iNaturalist bunya pine offered for the Cook and Hoop Pines. One near miss worth a lead: "Firenze, giardini del bobolino, 10.jpg" is a fine multi-stemmed red-barked cupressaceous conifer in the Bobolino, not our cedar or stone pine. Remaining unjudged rows in kept-set cities are mostly last-resort radius hits (Mapillary, street files); not worth a pass without a better sweep. Preflight 0 problems.

## 2026-10-22 later attempt: nothing shipped, nothing claimed

No claims standing. Three READY leads (two Oxford, one Madrid) have no approved photograph and own supply is paused, so none ships. Health clear, reader inbox empty. `photo_hunt --recheck` swept 40 kept-set trees (Alicante, Amsterdam, Arnhem): 4 new candidates in Arnhem, but `photo_fetch` says nothing to fetch for them, so no viewing pass was worth the tokens. Manchester register retried: still none; two named-tree leads noted in data/register-scouting.json (Heaton Park eucalyptus, Alexandra Park Railway Poplar), each needs a second source. No trees added.

## 2026-10-22 night window (from 17:39 UTC): reader photo, photo sweep

Rung 1: a reader's photograph of the Weeping Cedar of the Vallée-aux-Loups (cma_001) looked at, same tree, daylight and colour, added beside the lead photo; the verdict record had to be stubbed by hand in data/judgements.json because sightings_publish.py had already cleared the queue entry (judgement.py --scan found nothing). Health clear. Own supply is paused, so rung 6: photo_hunt --recheck on the kept set, then a photo-judge pass: 26 images viewed, 1 approved (bne_004, Brisbane banyan, iNaturalist CC BY, 500px only), 32 rejects recorded; most kept-set candidates are generic park files shared by several trees. To check: msl_003 Krüsellinde may have been missed in a 2020 photo (life check). Prepare's REFILL note is moot while supply is paused. Not pushed (credential note); Run health pushes.

## 2026-10-22 session: the night runs under the demand cut

Own supply paused (Hidde: "moeten we de nachtruns nog aanpassen dan?"): preflight now refuses a new tree of our own (check_own_supply_is_paused, SUPPLY_PAUSED in findable.py); a reader's tree still ships. thin_pages.py writes data/index-kept.json, the cities with a page still in Google; enrich.py --next and photo_hunt.py (without --city) take their queue from it instead of the 259-city roster. The 12 trees held past the pace cap stay in data/research/held-pace-2026-10-22/ (README says why). CLAUDE.md recovery mode says so.

## 2026-10-22 session: the demand cut, hreflang, the sources line

Google: the 09-28 fall sits inside the September 2026 spam update (24 Sep to 8 Oct), no core update since May. Demand cut added to scripts/thin_pages.py (DEMAND_CUT 50): 720 more pages carry the googlebot noindex, 598 English tree pages in 101 cities and 84 place pages stay in Google, every unique-photo page and reader-found tree kept; Bing keeps everything. hreflang now names only indexable alternates. The Sources line on every tree page says the story was written with AI and readers correct it, in eight languages. The recrawl sitemap was already live since 10-01 (robots.txt names it), nothing for Hidde to submit. Preflight 0 problems; the Astro build runs in CI on this push. Each change is its own commit.

## 2026-10-22 session: about page tightened

About page: "huge" from four to one, "marvel" from two to one, and the sources line now says what is true ("written with AI, and readers who know the trees correct them" instead of "corrected by people who know the trees"). A comment marks where the Wilder (wilder.pt) article link goes once it is published; Hidde wants it linked (2026-10-22). Hidde's own text otherwise untouched.

## 2026-10-22 night run (third retry): cap at 73 of 60, nothing shipped

No claims standing. Only 3 READY leads, none with an approved photograph. Tried goliad.json into data/cities again: preflight fails on `check_publishing_pace()` (73 new trees in 24 hours, cap 60) and the missing data/us-states.json entry; moved it back out to out/tmp/. The 15 written trees still wait for the count to drop. Manchester register retry not attempted (the TPO layer is protection, not remarkable status, per the scouting note). No trees added.

## 2026-10-22 night run (second retry): cap still holds, Inverness retried

No claims standing; 3 READY leads (two Oxford, one Madrid) have no approved photograph so none ships. 15 written trees (photo-batch-2 10, texas-famous 4, ftw_018) wait only on the 24-hour pace cap, as do the 11 held city files in data/research/held-pace-2026-10-22/ (add college-station, coppell, goliad to data/us-states.json when restoring). Inverness register retry: Wikidata has no tree items inside it, still stalled, noted. Munich photo recheck repeated the earlier result (muc_022, 026, 027, 037 candidates await a photo-judge pass). No trees added.

## 2026-10-22 night run (retry, 15:00): photo lane while the pace cap holds

Resolved a LOG.md rebase conflict. The pace cap still holds 54 verified trees, so I added no verify or write passes. Munich photo recheck found 7 new candidates (muc_022, 026, 027, 037); a photo-judge pass was dispatched on them. Tulsa register retry: still no county list, only the Creek Council Oak, noted in data/register-scouting.json. No trees added.

## 2026-10-22 session: product list checked against the product

Hidde asked how current the open list is. Item 19 ("I have seen this one" behaves differently on web) is gone from PRODUCT_TODO.md: that control no longer exists, collecting is by photograph on web and app since 2026-10-10/14 (Collect this tree, camera then seal, one sheet). Item 17 (Hide My Email second account) now carries a count: 9 of 36 accounts use an Apple relay address, 1 of them has saves; no duplicate proven. Checked afterwards: Apple sign-in is already live on the web (2026-09-17) and the web route answers, so Apple on both surfaces is one account; the only unclosable case is Google on the web plus hidden Apple in the app, which needs a merge flow. Noted on the item. Nothing in the product changed.

## 2026-10-22 night run (14:49 window): nothing publishable, pace cap

Rungs 1 and 2 clear (no reader photos, health green). Tried to merge the three Texas places; preflight refused on the pace cap (75 new trees in 24 hours against 60) and the missing us-states entries, so I moved them out of data/cities again (now in out/tmp/, copies still in data/research/texas-places/). Photo recheck sweeps on Munich and Paris found 6 new Munich candidates; the only one fetched (Luitpoldpark, muc_027) shows a stand of bare trees, not this one, so nothing approved. enrich.py says nothing to do. No trees added; this window did nothing useful beyond confirming the cap.

## 2026-10-22 night run (retry attempt): pace cap holds 12 trees

Eleven new city files an earlier attempt left uncommitted (bregenz, college-station, coppell, goliad, hagerum, hochosterwitz, leonstein, ogi, sakurai, shikokuchuo, winterswijk; 12 trees, all with approved photographs) failed preflight: 84 new trees in 24 hours against the cap of 60, and three Texas places (college-station, coppell, goliad) missing from data/us-states.json. Moved to data/research/held-pace-2026-10-22/ to restore tomorrow: add the three states, move the files back, run preflight. Nothing else was writable: 3 READY leads (two Oxford, one Madrid) wait on photos, and every claim was already free.

## 2026-10-22 night run (12:29 UTC window): enrichment leiden+frankfurt+regensburg

Rungs 1 to 3 clear (no sightings waiting, health green). Rung 4: enrichment pass on 7 trees; one gap closed (frk_023 Bethmannpark Ginkgo girth 484 cm, height 26 m from Baumkunde.de, a private register, noted as such), 10 gaps dead-ended for 90 days. Preflight 0 problems.

Then a verify pass on San Francisco (top US city under target with supply): nothing shippable. No unmined register row has an open-licence photograph (Commons and iNaturalist searched at each coordinate) and the rest are private yards. Three leads added to data/leads/san-francisco.json (Dr. Hurd Manzanita may be sidewalk-visible, Cook St Norfolk Pine view-only, five private-yard trees re-confirmed blocked). SF is a wall for new trees until photos exist; a photo sweep is the route.

Scouting retry on Oxford (scout_next RETRY): still stalled. No Wikidata trees, no open register; leads only (Headington Hill Park butternut and oak, Addison's Walk oak, Iffley horse chestnut, felled Tolkien pine blocked) in data/leads/oxford.json, none with a coordinate and open photo. oxford-tree-trails.org timed out at 20 s (not blocklisted). Window ended on walls: nothing new published this run; the real route is photo sweeps, not more verify passes.

## 2026-10-22 session: US photo push, nothing to approve

Hidde asked how our US supply looks after three US downloads in a day. Verdict: plenty of trees (456 in 76 places, second after the Netherlands) but 90 photographs, so most US tree pages sit outside Google. The cities Google shows are nearly bare: Oahu 5/21, New York 8/28, Houston 0/11, Chicago 1/38, Portland 2/33, Dallas 1/12.

- `photo_hunt.py --recheck` over all 32 US roster cities (free API sweep). Only 15 trees had candidates nobody had judged; the rest were rejected in earlier passes.
- One photo-judge pass on those 15 (94k tokens): 0 approved. All 18 images were off-subject; ten champion trees in Chicago and Pittsburgh all drew the same 1941 "Champion" train postcard. "champion" is now a not-distinctive word in photo_hunt.py.
- Read: Commons is exhausted for the US photo gap. The next real source is a new one (Flickr CC, state champion-tree registers with photos, or readers), not another sweep.

## 2026-10-22 (session with Hidde): Madrid's Guia Verde read, four leads

Madrid's tourist office answered the 10-20 tourism mail by pointing at the city's new Guia Verde de Madrid (2026 PDF on madrid.es). Read it: mostly parks in general, few single trees. Four new leads in data/leads/madrid.json, best the Castellana elm opposite the Hotel Villa Magna, "Madrid's oldest street tree" (18 m, 380 cm, singular under the 1997 PGOU); it needs a second source, a trunk pin and an open photo. The guide's photos are all rights reserved. Register lead: the 1997 PGOU catalogue of arboles singulares. Reply draft asking who at the city could release the photos: drafts/reply-madrid-turismo-2026-10-22.md, sent on Hidde's "verstuur" the same day.

## 2026-10-22 (session with Hidde): ten famous trees with photos written, parked behind the pace guard

- **Ready, not live:** 10 trees with approved Commons photos, 8 new places, ready in data/research/photo-batch-2-places/ (winterswijk, leonstein, hochosterwitz, bregenz, ogi, hagerum, shikokuchuo, sakurai) plus kna_002 Tate-no-Omayumi for Koriyama in data/research/photo-batch-2-verified.json. Preflight passes on them except `check_publishing_pace()` (82 in 24 hours). **Next run once the count drops:** move the eight files into data/cities/, append kna_002 (from the verified file, without `_city`, `_slug`, `alive_basis`, `country`, `place`, `place_note`) to data/cities/koriyama.json, preflight, merge. The night run's three Texas files (data/research/texas-places/) go first, they were parked earlier.
- **Found gone despite a good photo:** Birr Castle grey poplar (blew down 2014), the Québec cannonball elm (felled 2021), and the Everseiche looks dead in a July 2025 photo. A photo is not a life check.
- **Held:** Häradseken (no public path known on Gotland farmland), Mogadouro (no written source), Hamerenne (private front garden).
- **Waste, said plainly:** the four Texas trees were verified and written twice. A night run took this LOG's "next lane: Texas" an hour before my claim, and my claim was named `photo-batch-2`, so neither side could see the other. A claim should name the place or list it covers. Cost of the pass: verify 226k, write 175k, for 10 trees, about 40k a tree.

## 2026-10-22 (session with Hidde): Hong Kong OVT photo sweep, low yield

- We hold 698 of the 713 OVT/SWT register trees (data/registers/hongkong-ovt.json) and publish 21. A Commons geosearch (40 m) on the 50 biggest unpublished ones found open-licence files near 33, but they are street-photography series ("SS2", "Px3") of roads, shops and statues; the five most promising, viewed, held no whole-tree photograph (aerial roots close-up, a statue, a street with the banyan in the background, privet flowers). Treat Commons geosearch on Hong Kong OVT trees as exhausted; script and results in out/tmp/hk_ovt_sweep.py and out/tmp/hk-ovt-photos.json (not committed).
- Better routes, both waiting on Hidde: a reader's photo ask in r/HongKong in his voice (as in r/Lisbon), and Gavin Scott Coates, who made HKU's Digital Arboretum (digarb.hku.hk, suggested by a commenter on his r/Lisbon post) and is the Gavin Sally Bunker of leafy.hk introduced on 2026-10-14; Hidde contacts him on WhatsApp himself, so no mail. Kowloon Park alone holds seven big unpublished OVT figs, a walk if photos turn up.

## 2026-10-22 (session with Hidde): 481 colon reveals out of the indexed stories

- **Product:** every colon reveal in the 1,183 stories Google indexes is rewritten (481 sentences, 218 place files): a full stop or a comma and a plain clause, every fact and number unchanged (the apply script refused any sentence whose numbers changed), every story still 150 to 250 words. Translations, now out of Google, keep their older wording.
- **Guard:** preflight's `check_no_colon_reveal_in_an_indexed_story()` refuses the shape in any story with an approved photograph; BRIEF_WRITING.md and CLAUDE.md (Stories) say so. **For the night run:** approving a photograph on a tree whose story has one means rewriting that sentence in the same commit.
- **Reddit:** Hidde posted his own r/Lisbon post with a reader's photo (118 views, 1 upvote in the first hour, no comments yet). Replies are in drafts/reddit-lisbon.md.

## 2026-10-22 (session with Hidde): what Google sees on the indexed pages, five checks

- **Fixed, live with the next deploy:** (1) 118 paid trees told Google `isAccessibleForFree: true` because "under 6 free" sat in their access line; paid_entry now decides first, English and translated pages. (2) 280 sources written "url (note)" rendered as one broken link; the link is now the url alone (site/src/lib/tree-sources.ts). (3) 23 dead source links repointed: Luxembourg's dated register download to the dataset page (9 trees), four renamed Wikipedia lists (Graz, Innsbruck, Berlin-Mitte, Kopčany; 14 sources). Innsbruck inn_003 and inn_006 had every link dead and now have a live one.
- **Measured, nothing to fix:** shared text on 60 indexed tree pages is a median 31%, and it is all interface (sheet buttons and dialogs), no story sentence on 20%+ of pages. JSON-LD is clean (WebSite, Organization, TouristAttraction, BreadcrumbList).
- **For the night run:** `python3 scripts/source_links.py` (new) lists about 40 remaining dead source links on indexed trees, one per tree; repoint each (the host's search, the Wayback Machine), never drop a tree's last source. PageSpeed Insights answered 429 today (keyless quota); retry `python3 scripts/pagespeed.py` another day.
- **Colon reveals:** done the same afternoon on Hidde's "waar wacht je op", see the entry above.

## 2026-10-22 (session with Hidde): translations out of Google too

- **Product (Hidde: "translation uit de index halen dan?"):** every translation of a place or tree page (654 urls) joins the strict cut, googlebot tag only, Bing keeps them (`TRANSLATIONS_OUT` in scripts/thin_pages.py). Four translations a digest showed before 09-28 stay. Google's index goes to about 1,450 English pages, nearly all photographed trees plus roster places.
- **For the night run:** new translation passes pause while `TRANSLATIONS_OUT` holds (CLAUDE.md, recovery mode); the BACKUP lane is register scouting.

## 2026-10-22 (session with Hidde): readers' words on the page; iOS test green again; Baarn line refused

- **Product:** the Montsouris plane (par_034, English and French) and the Hammundeseiche (fwd_001) now quote their readers instead of paraphrasing them. New `scripts/reader_words.py` lists every stranger's note on a live tree that no story quotes yet (0 left today); sightings_publish.py prints it after publishing. Rule in CLAUDE.md, Reader input.
- **Fixed:** iOS CI failed on one unit test still looking for the pre-copy-sweep wording ("Allowing photos"); the test reads the new sentence. App unchanged.
- **Mail:** mailcheck refuses "I live in Baarn" without what he does in the same sentence, and "minutes from Amsterdam" (Hidde: "when will you remember that this sentence is weird"). drafts/group-messages.md (untracked, names people) now opens with a status table: Fred Breglia and Samuel Mitchell were mailed on 10-16, the Ancient Tree Forum is not mailed again; only the four Reddit mod messages are open. Hidde's Reddit account is new, so he comments for a week before the first post.

## 2026-10-22 (session with Hidde): the strict cut, 367 more pages out of Google

- **Product (Hidde: "ik ga liever te ver nu met meer kans op herstel en dat we dan langzaam weer toe laten"; "alleen uit Google, Bing houdt ze"):** every species (197), park (49), collection (19), state (10) and country page, the place pages of cities off the frozen roster, and translations there now carry the googlebot noindex. Bing keeps them via sitemap-bing.xml. 367 paths, `STRICT_CUT` in scripts/thin_pages.py (group 5 in data/noindex.md). Kept: the roster, anything a digest's top pages showed before 09-28, and every photographed tree page in English. Google's index goes from about 2,450 urls to about 2,080, nearly all photographed trees plus roster places.
- **Ratchet widened with Hidde's yes:** qa's `check_the_noindex_split_holds()` lets the strict cut's listing and place pages carry the googlebot tag (it allowed tree pages only); question pages still never may. The recrawl and Bing sitemaps skip listed paths the build did not make (six listing files with too few trees).
- **Not verified locally** (no local build): the deploy's qa run is the first full check of the tags.
- **Letting back:** only once Search Console shows recovery, in steps, places and countries first, then species, each step after the previous one earns impressions.
- **Press, wait (Hidde: "laten we maar even wachten we zijn met beide in contact geweest"):** no follow-up to Omrop Fryslân (Wybren, last mail 10-15) and no news pitch to Omroep Brabant (link ask 10-15) until Hidde says so.

## 2026-10-22 night run (fourth attempt): nothing shipped, pace guard still at 75

- Shipped nothing. Tried the three Texas place files (college-station, coppell, goliad) again: preflight still fails only `check_publishing_pace()` at 75 new trees in 24 hours (cap 60), so I reverted the move. Next run once the count drops: move the three files from data/research/texas-places/ into data/cities/, add the slugs to data/us-states.json ("Texas"), preflight, merge.
- READY leads: 0. san-francisco photo recheck: 8 trees, 0 new candidates. The san-francisco claim stands (sfo_012, sfo_013 need stories, which add new trees, so they wait on the same guard).

## 2026-10-22 night run (third attempt): enrichment only, new trees still behind the pace guard

- Nothing READY. Everything awaiting a writer is either already published (stale files), a duplicate, or adds new trees, which the pace guard (75 in 24 hours, cap 60) still refuses; so no new trees this window. The san-francisco claim stays (sfo_012, sfo_013 still need stories; release refused until merged).
- Seattle enrichment: 9 SDOT street trees, pin-only gaps with no photograph and no register page; recorded as dead ends (`enrich.py --done seattle`). Dispatched an enrichment verify pass on leiden+frankfurt+regensburg (answer to out/enrich/leiden+frankfurt+regensburg.answer.json).

## 2026-10-22 night run (second attempt): three Texas place files built, held by the pace guard

- Nothing was READY. Verified and wrote four famous Texas trees that already had open photos (Century Tree, Houston Campsite Oak, Cart War Oak, Rio Frio Landmark Oak). Three have approved photographs and full place files, parked in `data/research/texas-places/` (college-station, coppell, goliad; ids clg_001, cpl_001, gld_001). They pass preflight except `check_publishing_pace()` (75 new trees in 24 hours, cap 60), so they were not published. Next run once the count drops: move the three files into data/cities/, add the three slugs to data/us-states.json ("Texas"), run preflight, merge, then release no claim (none held).
- Rio Frio oak (txf_004) is written but held: its photo has no geotag and was shot from inside the fenced land. Kept in data/research/texas-famous-verified.json, story intact, until a roadside photo turns up.
- San Francisco deepen pass: sfo_012 (Cork Oak, Landmark Tree 15) and sfo_013 (Moreton Bay Fig, view-only) verified, no photographs, so they wait for a photo (ADD_NEEDS_PHOTO). Claim on san-francisco stays until they merge or the claim expires. 4 leads kept. sfenvironment.org and citizenportal.ai return 403.
- inn_007 skipped: pin on a building, probably private yard, no photo.

## 2026-10-22 night run (09:06 UTC window): photos and scouting, no tree added

- Ladder: no reader photos waiting, health clear. Nothing writable: the one written tree (ftw_018) has no confirmed photo path and the other "awaiting a writer" files are stale or duplicates. prepare.py 7-day visits line not shown by this run's output.
- Photo sweep Chicago (36 trees, 6 new candidates) and Seattle (27, 2 new): sweeps otherwise exhausted. Viewing pass on the 19 roster-fetched images (hong-kong, pittsburgh, luxembourg-city, como, trieste, dresden): 0 approved, 18 rejected (wrong species, close-ups, felled twin, non-tree). Chicago and Seattle candidates were not fetched by `photo_fetch.py --roster` (it said nothing to fetch for them); next run should check why.
- Chicago enrichment: only season gaps left, recorded as dead ends (`enrich.py --done chicago`). Catania scouted: same dataset as the national MASAF list, 3 to 4 trees round Villa Bellini, verdict `exhausted` in register-scouting.json.
- Left open: the Texas famous-trees batch (4 trees with an open photo) for the next run.

## 2026-10-22 (session with Hidde): a new tree of our own needs a photograph

- **Rule (Hidde):** "we should only focus on trees with photos". It reverses 10-18's photo-less trees for Bing. New preflight FAIL `check_a_new_tree_has_a_photograph()` (`ADD_NEEDS_PHOTO` in scripts/findable.py): a new tree needs a lead photo with status `approved`, a reader's tree is exempt, and the 3,880 trees live today are in data/photo-baseline.json. Tested on a copy: quiet on today's data, fires on a new photo-less tree, passes one with a photo and a reader's. CLAUDE.md (Google recovery mode) and DECISIONS.md updated.
- **For the night run:** READY leads in `leads.py` are mostly photo-less register rows, and writing them now fails preflight. Run `photo_hunt.py` on a place before you verify or write it, and take leads that already carry an open photo first (data/leads/_famous-*.json, about 130 with a pin).
- **Next lane (Hidde: "if the texas trees seem valuable lets try that one"):** Famous Trees of Texas (data/research/texas-famous-trees.json, 93 not yet live). A photo sweep runs first; the trees with an open photo go to a check in batches of 20.

## 2026-10-22 session with Hidde: no ambassador tag on app Settings

Live on main for the next app build: the Settings card shows name and address only; the ambassador tag stays on My trees and the public profile (Hidde: "op de setting pagina ... mag die weg"). Built and looked at in the simulator, signed in as a Paris ambassador. The website's settings page never had it.

## 2026-10-22 session with Hidde: copy drift guard

The Monday fresh-eyes review (review.yml 6b) now also reads the week's new strings for machine-written shapes (and proposes regexes for copycheck's `AI_SHAPES`) and reads that week's DECISIONS.md entries against all product copy for sentences they made false. CLAUDE.md, How to work: a decision that changes the product greps the product for the old claim in the same session; the product-copy skill gained that step. Applied to today's photo rule: nothing on the site contradicts it.

## 2026-10-22 session with Hidde: copy sweep live on both surfaces

Hidde: "voer alle voorstellen door in alle talen, behalve de titels/meta en de voorwaarden". 68 sentences rewritten (commits 5466b4bdd web, 0ab9b8183 app plus web), every language a string exists in: colon reveals, morals ("A map of scattered pins is a list"), Dutch tense ("tell us and we correct it"), "the button wakes up", the badge promise on the home page, and the "verified against two independent sources" claims on /explore, /support, /contribute and /press, which stopped being true when a reader's photo with GPS became a source. Left for Hidde: homeTitle, homeDescription, citiesDescription, exploreDescription (Google recovery) and /terms. Kept on purpose: "Made for people who love being outside" on the home page (his own line). One /app sentence stays as it was, because it shares a line with a hand-drawn icon and iconcheck refuses any edit to that line until the icon is replaced. App strings ship with the next build.

Shared-checkout accident: another session's staged change (a new tree of our own needs a photograph: CLAUDE.md, DECISIONS.md, its LOG entry, findable.py, preflight.py, data/photo-baseline.json) went into 0ab9b8183 under the copy-sweep message. Complete and as that session intended, only the label is wrong. Its own LOG entry below describes it.

## 2026-10-22 session with Hidde: product copy guard, app pitch rewritten

Hidde found "The walking routes, your saved trees, and the collection of the ones you have stood in front of: the Ancient Trees app." on city pages ("loopt scheef en lijkt door ai geschreven"). Live now, in all seven languages: the three app-pitch bodies, their titles, the home page's "Tick off the trees you visit." and the /app meta. Guard: copycheck.py gained `AI_SHAPES` (colon reveal, whether-you're, defining by denying, "the ones you have stood"), which run on web and app; a PostToolUse hook (scripts/hooks/copy_after_edit.py) runs it on every edit of a copy file; new project skill `.claude/skills/product-copy/`. Also fixed copycheck's comment blanking, which ate blank lines and shifted every site line number. A sweep found 68 more crooked sentences (30 certain), in drafts/copy-sweep.html (proposals in out/tmp/copy-sweep.json), waiting for Hidde's go. Not yet seen rendered: no local build, so checked after deploy.

## 2026-10-22 session with Hidde: a reply-mail skill

Hidde asked whether a skill would help with mails. The rules for a reply lived in seven places (HIS_VOICE.md, five memory notes, mailcheck.py), loaded only when a session remembered. New project skill `.claude/skills/reply-mail/SKILL.md` bundles them in order: read the voice file and the thread, do the fix first, the reply shape, the never-list, a de-AI cutting pass, mailcheck, show with the full mail above the draft. It points at the existing files and rewrites none of them. Loads from the next session on.

## 2026-10-22 session with Hidde: press round 3 and tourism batch 1 sent
- Hidde: "verstuur beide". Twenty mails out through outreach_send.py: ten regional desks (press round 3, roster cities in the US, UK and Germany, one tree and one sourced fact each) and ten official visit-the-city sites (tourism batch 1, the map as a resource for their parks page). Every link checked live before sending; no repeats, nobody on the do-not-contact list. Logged in drafts/OUTREACH.md (private); link check on 2026-10-29 is in OUTREACH_STRATEGY.md's dates.
- Prof. Roloff answered the 10-20 link ask with a no (too many such requests); his thank-you reply draft waits for Hidde to send.

## 2026-10-22 (session with Hidde): 15 famous US trees live from their Commons photographs

- **Product:** first batch of Hidde's 2026-10-21 call ("bomen met fotos zijn interessant, die mogen live"). 15 named US trees from Wikidata, each with an open-licence Commons photo looked at in session: Adam and Genesis (new place Mountain Home State Forest), the Hart Tree (Kings Canyon, now four), Bennett Juniper, Jardine Juniper, the Chandelier Tree (Leggett), Boyington Oak (Mobile), Friendship Oak (Long Beach, Mississippi), The Big Oak (Thomasville), The Big Tree (Goose Island State Park), Mother Orange Tree (Oroville), and Riverside as a new four-tree place (Parent Navel Orange, White Sox Redwood, Roosevelt Palm, a landmark sycamore). The Roosevelt Palm photo is held (six palms, trunk unknown).
- **Blocked, kept as leads:** King Arthur (dead, Castle Fire 2020), Seven Sisters Oak (private front yard), Duffie Oak and Council Oak (access unsettled), Fairmount bald cypresses (plural, no pin).
- **Pace cap:** past the 60-a-day guard (73 in 24 hours with the night runs' 58), as a one-off on Hidde's word: "Ja, zet ze nu live, eenmalig over de grens van 60." The guard stays.
- **Cost:** verify 186k, write 158k tokens, about 23k per tree, over the 15k target; five dropouts and a rewrite of the place contexts after Contract B refused them. Weak alive evidence is stated on the pages (Genesis burned, Jardine no dated sighting since 2020, the sycamore one source).
- **Next batch** when Hidde says: the other ~130 pinned photo leads in data/leads/_famous-*.json.

## 2026-10-22 night run (06:36 UTC window): Leiden +2, seven READY leads held

Rung 1 empty (0 photographs waiting). Rung 2: the health "Smoke test skipped" flag is a 1-second if-condition skip on every push while Build and deploy succeeded, answered with health.py --answer. Write pass on the 9 READY leads: lei_025 (Endegeest linden) and lei_026 (Jan Wolkers's oak) live in Leiden (17 to 19, Oegstgeest day-trip trees, nl overlay done). The other seven held with reasons (Pittsburgh x4 no honest recognition line or access, Wilhelmina linden unconfirmed standing, Pelgrimvaderskerk beech no access source, Insingen linden too thin). Photo sweep on 17 roster trees (Chicago, Frankfurt, Leiden, Regensburg): 13 trees viewed, none approved (railway postcard, castle facades, wrong plane). Fort Worth scouting retried: the city's arcgis item has no licence line, still stalled. Chicago +10 (28 to 38, chi_030 to chi_039, FPCC champion register, flagged, no photos); existing Chicago claims that the new walnut and pin oak outdid were corrected. Seattle +9 (21 to 30, target reached; sea_022 to sea_030 from the city's Heritage register, one source each, approximate pins, no photos, address-level recognition lines; sea_025 renamed to Sweet Chestnut to match other cities).

## 2026-10-22 night run (02:55 UTC window): photograph sweep, one approval

- **Live:** the Presidio Centennial Tree (San Francisco) now has a photograph (BrokenSphere, CC BY-SA 3.0; reversal `python3 scripts/photo_apply.py hold sfo_011`). Rung 1 empty, health.py's only flags were push-skipped deploys (a dispatched deploy was running). `photo_hunt.py --recheck` on glasgow, san-francisco, washington-dc, pittsburgh found little; a viewing pass over 40 fetched files rejected 39 (wrong subject or species). Next time: queue the named Commons files for the Yamaki Pine (wdc_025: "Japanese White Pine 'Hiroshima Survivor', 30 April 2012.JPG", Sage Ross CC BY-SA, viewed and fits). Nothing written: the one written tree waiting, ftw_018, is held on unknown access.
- **Also live:** the Yamaki Pine (wdc_025) now has a photograph (Sage Ross, CC BY-SA 3.0, queued from the named Commons file and viewed; reversal `python3 scripts/photo_apply.py hold wdc_025`).
- **Chicago 21 to 28:** seven Forest Preserves of Cook County champion trees (bur oak Harms Woods, sycamore Riverside Lawn, black oak Willow Springs, American elm Schiller Woods with an approximate pin and the story says so, bald cypress McGinnis Slough, swamp white oak Spears Woods, silver maple Harms Flatwoods). One register source each, flagged; none has a photograph yet, so Bing and readers only. Superlatives on chi_008/chi_017/chi_018 corrected where the new trees changed them. Preflight 0 problems.
- **Frankfurt 21 to 23:** the Bethmannpark ginkgo (2015 measurement, said so) and the Leonhard-Eissnert-Park oak (in Offenbach-Bieber, labelled; the two measurers disagree on species and age and the page says so). German overlay updated. Frankfurt's supply is spent (the pass found only these two plus six leads); flurbaum.de/f-stadt.html is a new dated, measured lead source. Pending: more of the pass's leads need a second source.
- **Photo approval (night run):** chi_023 Bur Oak of Harms Woods, Ben Redding (iNaturalist, CC BY): the observation's fix sits 11 m from the register's GNSS pin and the lone big oak fills the frame (bare, winter). Reversal `python3 scripts/photo_apply.py hold chi_023`. Other sweeps (frk_023 park view, chi_027 crown and cone close-ups) left unapproved.
- **Page gap:** Swamp White Oak species intro written (pagegaps.py now says nothing missing).
- **Where it stopped:** Chicago and Frankfurt moved; the rest of the shelf is thin (9 READY leads are young or weak, Pittsburgh and Leiden; famous lane's top is Lithuania, outside the focus countries). Washington DC has only a duplicate in its verified file (wdc_017 = wdc_012).
- **Enrichment pass** on glasgow+san-francisco+washington-dc+pittsburgh (11 trees): closed nothing, 18 gaps recorded as dead ends (`enrich.py --done`). Pittsburgh champions have no sizes in the Shade Tree Commission minutes; remarkabletreespgh.com returns a stub to automated fetches (a browser session could read the champion measurements). Claims released (washington-dc with --force: wdc_017 is a 0 m duplicate of wdc_012, not a pending tree).

## 2026-10-22 night run, later attempt: San Francisco +1, Studena new

- **Live:** San Francisco 10 to 11: the Presidio Centennial Tree (1876 blue gum, approximate pin, no photograph yet; Commons has two CC BY-SA candidates to check). New one-tree place Studena (Grandpa Kolyo's Oak, Tree of the Year), out of Google until four. Preflight 0 problems. san-francisco claim released.
- **Held:** ftw_018 (public ground unknown), inn_007 (pin on a private building), Pittsburgh READY four (school grounds, indistinguishable pins), Rothenburg/Rotterdam/Leiden (walls). Leiden Jan Wolkersboom oak could ship once its wall expires.
- **Open:** city_names.py cannot resolve Studena (no Wikipedia article); sfo_011 transport still says "(stop not verified)".

## 2026-10-22 night run (01:38 UTC window): Potsdam +3 trees

- **Live:** Potsdam goes from 15 to 18 trees: the pollarded linden of Fahrland, the Babelsberger Strasse oak and the Nattwerder lindens (register-only, no photographs yet, confirmed pins). German overlay and counts updated. Preflight 0 problems. 7-day visits line not printed by prepare.py this run.
- **Live:** Frankfurt 20 to 21: the Jahn Oak in Offenbach (confirmed pin, CC0 photograph looked at and approved, so Google can show it). Rumpenheim ginkgos stay a lead (approximate pin, not findable). frankfurt.de returned 403 for three more candidates (Untermainkai ironwoods, zoo bald cypresses, Liebfrauenschule mulberry). Portland refused to claim: already over its target.
- **Photo:** pot_017 (Babelsberger Strasse oak) approved after viewing: Commons "Haplochromis", CC BY-SA 4.0, on-pin geotag, the Wikidata photo. Four others rejected (sapling, wrong street, plaque, pavement shot of a possibly different trunk). Reversal: `photo_apply.py hold pot_017 <url> --reason revert`. photo_light.py cannot run here (no Pillow), judged by eye.
- **Live:** Pittsburgh 4 to 12 trees. The scout retry found that remarkabletreespgh.com's map is a Google My Map whose KML holds 16 tree-level points; used as facts only (the site is All Rights Reserved). Six of the new trees have confirmed pins, two (black locust, American elm) approximate with size-based recognition lines; four more (sycamore, crabapple, two pin oaks) went back to leads. The sycamore, crabapple and oaks, plus the KDKA claim, need a second source. Las Vegas and Ann Arbor scouting retried (Las Vegas already published; Ann Arbor's big-tree page has no licence or per-tree data, stays stalled).
- **Live:** Glasgow 5 to 6: the Wallace Yew at Elderslie (day trip, age disputed and said so, confirmed GPS pin, Commons geograph photograph approved after viewing; reversal `photo_apply.py hold gla_006 <url> --reason revert`). For a later pass: lifecheck the Darnley Sycamore after storm Eowyn.
- **Live:** Regensburg 6 to 8: Wutzlhofen Oak and Unterisling Oaks (confirmed OSM pins, no photographs yet, ages stated as the ordinance's figures). rgb_001 (Herzogspark plane) gained girth 620 cm, 31 m and age 150 to 200 years from the Baumkunde register; oldest tree on the page is now rgb_007. Six more Naturdenkmal rows (ND 3, 23, 27, 28, 29, 48) still have no coordinate; the runner has no PDF reader, which blocks the city's planning PDF.
- **Live:** Washington DC 20 to 21: the Yamaki Pine (a 400-year-old potted bonsai at the National Arboretum, said plainly; age is the family's and foundation's account). Three more verified (Lincoln Memorial elm, Roosevelt Island bald cypress, Congressional Cemetery swamp white oak) are held leads for lack of a photo or findable pin. wdc_017 stays unwritten (duplicate of wdc_012), so that claim was released with --force.
- **Live:** San Antonio 4 to 5: the Alamo Pecan (one source, last dated mention 2015, planting date given as the horticulturist's undocumented account; the pin marks the rear lawn, said on the page). Taco Land live oak held (restaurant lot, nothing after 2021). Fort Sam Houston's Quadrangle Oak blocked for access.
- **Wall:** Leiden verified empty again: Endegeest linden and Wolkers oak are strong but have no photograph or confirmed pin (NL rule), kept as leads. Rothenburg ob der Tauber verified empty (near register trees already live or blocked; Bettwar and Insingen lindens stay leads), walled 48h.
- **Health:** the Smoke test BLOCKER is the push-trigger skip (1s, by its condition), Build and deploy succeeded; answered with health.py --answer. No reader submissions waiting.

## 2026-10-22 night run (22:59 UTC window): three photographs approved

- **Live:** photographs on nyc_028 (Kingsland weeping beech), dre_028 (fingered horse chestnut), dre_010 (white elm, Königsbrücker Strasse); nyc_028 now has a photo, so Google can show it. dre_017 held: pre-2025 photos of a twin oak pair, one felled June 2025. Reversal: `photo_apply.py hold <id> <url> --reason revert`. About 60 iNaturalist candidates remain unjudged in the queue.
- **Nothing else:** health.py flagged only that GitHub dropped 6 of 12 knocks. Spokane claimed then released (1 unmined row, under the six-candidate floor). No write pass: the writable pile is 1 READY lead plus held trees. A second viewing pass looked at the other 61 candidates and approved none (wrong subject or species, close-ups, or trunk ambiguity). Tooling note: photo_apply.py matches iNaturalist candidates by observation url, so verdicts for photos of one observation can land on the wrong one; feed it thumb urls. The sweep also re-adds about 93 already-judged candidates.
- **Scout:** Chicago retried, stays stalled on licence. The Forest Preserves of Cook County champion layer (106 rows with GNSS coordinates) carries no licence and a sensitive-areas notice; those trees are already leads. Whether a county layer with no reuse restriction counts as open is Hidde's call; nothing imported. Leipzig claimed and released (1 tree to target).
- **Enrichment:** New York + San Francisco + Heidelberg pass. sfo_010's girth 383 cm (DataSF DBH 48 in) was already on the page, nothing new; hei_007 got its LUBW Naturdenkmal ids (82210001208/9; the LUBW page itself timed out, ids rest on the Wikipedia list). nyc_028 closed nothing: the landmarked 1847 beech died in 1998, so the LPC record and 14 ft girth are not applied to the replacement. 8 gaps dead-ended for 90 days. nycgovparks.org serves a captcha to automated fetches. Langcheck and pagegaps both have nothing to do.

