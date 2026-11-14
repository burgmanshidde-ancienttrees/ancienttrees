# LOG

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-11](archive/LOG-2026-11.md)
- [2026-10](archive/LOG-2026-10.md)
- [2026-09](archive/LOG-2026-09.md)
- [2026-08](archive/LOG-2026-08.md)
- [2026-07](archive/LOG-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
<!-- archive-index -->
## 2026-11-14 Leipzig write pass (session)

- **Leipzig: 1 tree written and live in the app** (lpz_031 the Great Oak of Leinestrasse in Doesen, Naturdenkmal ND 101, one of the six tree monuments Leipzig held before 1992; 5.30 m round; the allotment colony behind it is named after it). Age kept at 300 to 400 years from a 2009 caption, the cadastre's 1686 class named as a class and not a planting; the 24 m versus 28 m height conflict between the two city records stated in the story. Seen from the pavement, recognition line written, no best_time. App-only under APP FIRST. Meta description now says 30 trees; Leipzig is at its target of 30. A CC BY-SA Commons photo (MKBler, 2019) is named in the old verify notes for a photo-judge pass. Claim released.
- Nothing else in the US/UK/Germany pending list was writable. Detroit det_001 and det_002 are written but both have null coordinates and a hold, so they were not merged (no honest pin; they need a map point from the cemetery's tour PDFs or a reader fix). dmr_002 Meavy Oak is held (no sighting since 2019's "irreversible decline" report); frk_027 is held under hard rule 10 (schoolyard, no source shows it seen from the Peterskirchhof); sfo_012 is live sfo_004; car_001, nyc_031 and wol_001 are already live as crd_004, nyc_130 and wvh_001, so those research rows are stale.
- For the next session: Leipzig's question answer lists the Menzellinde (200 to 300 years) as next-oldest after the Starkeiche; lpz_031 at over 300 now arguably ranks between them, if it ever gets a web page.

## 2026-11-14 Fort Lauderdale write pass (session)

- **Fort Lauderdale: 6 trees written and live in the app** (ftl_005 Florida's champion baobab, 10.57 m round, and ftl_006 its challenger, both in ArtsPark at Young Circle, Hollywood, free; ftl_007 the state champion African mahogany in Plantation Woods Park, free, crown 38 m across; ftl_008 a challenger sandbox tree, ftl_009 a challenger gumbo limbo and ftl_010 the state champion candlenut, all three inside Flamingo Gardens, paid). App-only under APP FIRST, outside the pace. The two baobabs stay two entries: separate register records, separate measurements, 115 m apart, no single place to stand. No ages given (register measures size; baobab planting date disputed and stated so). Left out as unsourced: the Millennium Springs fountain, sandbox seed pods, gumbo-limbo bark. Species of ftl_007 set to the canonical "African Mahogany" used in Rio and Singapore. No best_time (no phenology files). Paid share now 7 of 10 (70%, a note); the free trees went some way, more free ones would help. City FAQ still says "all four" are paid at Flamingo Gardens, true of the web page's four. Claim released.

## 2026-11-14 write pass (session)

- **Miami: 2 trees written and live in the app** (mia_013 Fairchild's Tantancayo, the 1942 planting at the Vine Pergola and a former Florida champion; mia_014 Fairchild's Cannon Ball Tree, the 1938 gift from Jamaica's Hope Gardens). App-only under APP FIRST, so no web page and outside the pace. Species of mia_014 set to the canonical "Cannon Ball Tree" used in Oahu and Singapore. No best_time (no phenology file for either). Paid share: Miami now 6 of 13 behind a ticket (46%, a note), so the next Miami work is free trees. Claim released (forced: the refusal named kyw_001, which is live in key-west.json).
- Nothing else on the brief list was writable: sfo_012 is held as the same tree as live sfo_004 (fold its pin and girth there); car_001 (Cardiff) and wol_001 (Wolverhampton) claim ids of other live trees and car_002/003, wol_002, sfo_014/015 sit on live trees; chicago-2026-11, boston-common, boston-arboretum, wisconsin, washington-dc-2 and north-england-yews are fully published. Still unwritten elsewhere in the US/UK: dartmoor (1); detroit has 2 written and waiting on merge.

## 2026-11-14 00:36 run (night-run)

- **Chicago: 3 trees added** (chi_048 and chi_049 red oaks, chi_051 butternut, all Busse Forest South, Cook County champion register, confirmed GNSS pins, no photos). The verify pass delivered 10 rows but 7 were already live under other ids (chi_007/008/009/010/040/041/042); dropped from the research file. The butternut story states two facts outside the verify notes (endangered in Canada, canker first reported in Wisconsin 1967), both true but not yet sourced on the entry. For the next session: live stories chi_007, chi_014 and chi_037 count the ranked trees at Busse and now read too low.
- Rung 1: nothing waiting in the inbox or notes. Tip-668 (Villa Salina oak, Castel Maggiore) has no coordinate and its photographs are not on this runner, so its verdict stays open. Health: only red item was the live site being behind main; dispatching deploy at the end.
- Miami verify: only 2 new rows (mia_013 Fairchild tantancayo, mia_014 cannonball tree), both paid entry with approximate pins, so left staged in data/research/miami-verified.json unwritten (Miami would pass a third paid); claim mia stays until it expires. Stratford-upon-Avon scout: still stalled, no trees; next angle is the Ancient Yew Group Avon PDFs.
- Portland refused (full, 33 of 30); the writable pile is a few trees under the 6-tree floor.

## 2026-11-13 19:05 run (night-run)

- **Build fixed (rung 2).** Deploy had been red because the tip-668 sighting row (Villa Salina oak) carried a raw account id as its photo path's first part; now the `people.ref` code (commit c88e24ed7), qa source checks green. This runner's token could not dispatch deploy.yml or nightly.yml (HTTP 403), so the build waits for the next push or schedule. For Hidde: nothing, unless deploy stays red.
- Rung 1 and notes: nothing waiting. Prepare.py: 0 READY to write; Spokane claimed then released (1 unmined candidate of 19, wall for 48h), Porto refused (full at 32 of 30); Sintra, San Francisco, Guimaraes, Braga, Coimbra still walls.
- Scout: Newark retried, the NJ big-tree list answers 403 to curl, verdict rewritten in data/register-scouting.json. No trees added this window.

## 2026-11-13 night run (window from 17:38 UTC)

- Rung 1: tip-668, a reader's Villa Salina oak (Castel Maggiore, Bologna). Photo looked at: a tall oak in daylight. Regione Emilia-Romagna's 2023 monumental list matches the reader's 580 cm and 36 m. Held, not rejected: no coordinate from the reader, and no source says the park is open outside events. Ships once a GPS fix or an open-access source turns up. Verdict is written in data/leads/_sightings.json.
- Rung 5: Sintra verify pass found 0 new trees (register rows all judged or duplicates; one Monserrate eucalyptus lead with no girth or spot). Sintra and Braga are walls for 48h. Portland is full (33 of 30), so no claim.
- Health: only 5 of 12 knocks delivered in 24h (GitHub dropping the cron). Everything else green.
- Not done: `scripts/prepare.py` says the shelf is under its floor (930 leads need only a source), but the supply lanes I tried are empty. 

## 2026-11-13 session: outreach

- **Five mails sent** (Hidde's 'Verstuur alle vijf'): Rijnmond, Il Messaggero, Prima la Martesana, Turismo Lucca, Corse Orientale (europe-source-2026-11-13, Variant A). Rijnmond source on rot_002 fixed (dead AMP link).
- **US and UK wait for the Guardian piece, live Sunday 2026-11-15** (Hidde). Ready and held: us-uk-2026-11-13 (6) and us-uk-press-2026-11-13 (11). From Monday 11-16, in a session: swap the Wilder P.S. for the Guardian link once it is live, re-check every link, show Hidde, send on his word; Glasgow Live and Cambridge News are both Reach, so not the same day. Night runs leave them alone.
- Found: the Suffragette Oak story (gla_002) says "days after" the 1918 Act; the Act passed 6 February, the oak went in on 20 April. Not fixed yet.

## 2026-11-13 session: Supabase egress back under the free plan

Supabase mailed that the org passed the free plan's 5 GB egress this month (grace until 2026-12-13, then possible restrictions on accounts, saves and uploads). Hidde: no paying for now, and no smaller photographs ("fix maar").
- **Backup**: db-backup.yml takes every stored file once in 28 days and only changed files in the weeks between (`-new` artifacts; BACKUP_RESTORE.md says how to restore). Tested: a week costs 24 MB instead of 145.
- **Tiles**: `scripts/shared_thumbs.py` (night run, after sightings_link) keeps a 600 px copy of each shared photo in the new public bucket `shared-thumbs`; 127 made, 83 KB average against 934. Profile tiles on web, iOS and Android load it and fall back to the full copy; the shared tree page keeps the full photograph. iOS and Android take effect with their next builds.
- **Avatars**: two oversized ones re-encoded to 512 px (476 and 117 KB to 43 and 69); new uploads were already 512.
- **The real source, found after Hidde pasted the usage page** (6.0 GB used 10-28 to 11-13, about 375 MB a day, with 19 active users, so machines, not people): `private_store.py` read the whole private_files table (6.4 MB) four times a knock, about 160 MB a day. Now gzip (5.8 MB to 1.2 on the wire), and a push reads back only files changed since the last pull (snapshot in out/), so a quiet knock's pushes read nothing. `crashes.py` (health and quality: 6 MB of MetricKit payloads) asks for gzip too.
- Restriction comes from 2026-12-13 if the cycle 11-28 to 12-28 also passes 5 GB, so about 165 MB a day is the ceiling. Check the usage page around 2026-11-20 for the new daily level.

## 2026-11-13 night run (window from 07:04 UTC)

- **Braga: 4 new trees in the app** (Turiz oak, Pindela tulip tree, redwood and Douglas fir; app-only under APP FIRST, no web page; Pindela is booking-only, 15 km out, said in the stories). Preflight 0 problems. Rung 1 empty (no sightings, no notes); health.py: only the deploy is behind main and 6 of 12 knocks delivered (deploy dispatched at window end).
- Not done: Newark retry (scout_next), mail batch, sourcing.

## 2026-11-12 daily publish (scheduled task): queue empty

- **Daily publish: queue empty.** No builder newer than 11-10 and every held set has been on main since 11-11; preflight 0 problems, pace not touched. For Hidde: the daily task "publish-held-trees-daily" can be switched off under Scheduled.

## 2026-11-12 session: saved trees show on the map, corners in one style

- **A tree you saved is never a dot any more** (Hidde: four saved in Frankfurt and only two showed): on the website's city map saved trees take their full pin first (city-map-script.ts updatePins), and in the iPhone app they get the first pin priority and are never thinned out. Tested on the live Frankfurt page with a stand-in saved list: before, 3 of 4 bookmarks showed (the Goethe Ginkgo in Rödelheim was a dot).
- **All three pin corners now in the ticket's style** (Hidde: "trek ze allemaal eens naar de ticket stijl"): a white disc with a shadow and a filled icon. The bookmark is moss instead of red (it kept the heart's red; the cards' bookmark is moss), the collected tick is a filled check-circle (Phosphor on the web, Apple's checkmark.circle.fill in the app) instead of a line tick, the ticket stays blue but is now the same 15 disc in the app (was 17) and Phosphor's ticket fill on the web (was a hand-made rounded rectangle), the counterpart of the app's ticket.fill. Web and iPhone in the same change; the iPhone shows it from the next build.
- Fixed in passing: the city map painted the saved corners only if the saved list arrived after the map script; it now paints once on start as well.
- For Android: the same two changes (corner style, saved never a dot) before its first release.
- Benchmark in CONVENTIONS.md "A tree you saved, on every map" (AllTrails heart on the pin, Google Maps' list icons kept on the map, both looked at in the browser). Explore and country maps still carry no saved mark; not part of this change.

## 2026-11-12 session: "Approved" and own trees on a profile, in both apps

- **iPhone and Android now draw what the website's profile already shows (Hidde's approved design, CONVENTIONS.md "Your own trees on a public profile"):** on somebody's Collected grid an "Approved" capsule top-left on the trees they added that we took in (MineCard's moss capsule with the seal-check, at the city pill's size, 6 in), then their own trees with their shared photograph (or their name), each opening its shared page. Your own My trees grid marks your approved trees the same way, read from your own sightings rows. "Approved" in eight languages on Android.
- **Live**: merged to main (PR #59, 4a7eec1a0, all checks green). Hidde pasted supabase/approved-on-profiles.sql the same day, so public_profile returns `approved` and `own` now (7 readers have an approved tree); the iPhone shows it from the next build, Android from its first release. Unit tests on both phones decode a payload with and without the keys.
- **Deleting an account keeps the photographs of trees in both apps** (Hidde, 2026-11-12: "het hele idee is toch dat we de bomen houden als mensen hun account verwijderen"): the iPhone no longer empties the sightings bucket on delete (SightingSync.purge gone), only the avatar goes; Android now deletes the avatar too, which it never did. qa `check_a_deleted_account_keeps_its_photographs()` reads both apps' deleteAccount now (checked red with the purge put back, green without).
- Differences: Android opens an own tree's shared page in the browser (no shared-tree screen there yet; data/android-parity.json "people"). The iPhone's person page has no map, so the own tree's pin shows on the website's profile map only. Android gained the iPhone's `-open=person:<id>` launch argument; both apps take `-approved=<ids>` for the sweep.

## 2026-11-12 session: FNP interview done

- Hidde talked to Hans Hofele (Frankfurter Neue Presse) about the Eschersheimer Linde and the app. Print for sure, maybe online; Hans sends the PDF. Two promises recorded in drafts/OUTREACH.md "FNP interview, 2026-11-12": a mail when Android is out (new list "Tell when Android ships", for the session that publishes Android) and app screenshots with Hans's own photographs of the lime (his photos are not in the mail thread or the app inbox yet).
- Fixed: our press mail to the FNP linked /de/frankfurt/eschersheimer-linde, a 404 since the translation trim of 11-05. Every tree url of a trimmed translation (47 overlays) now redirects to its English tree page (redirect-map.ts, f9c78da5d); checked live.

## 2026-11-12 session: inbox, Valencia's photo ask sent

- **Sent (Hidde: "die naar valencia mag eruit"):** reply to the València parks service's tree heritage section, asking whether the photographs on their geoportal fichas of the monumental trees may go on our pages, credited "Ajuntament de València". Their yes would open photos for the Valencia page (31 trees, almost none photographed).
- **Sent (Hidde: "to cockie is goed"):** KNNV Utrecht, his own text; she is searching her archive and has a new tree book at the publisher.
- **Sent (Hidde: "Send it"):** Genziana Ricci, his text rendered in Italian in Ferrara (asks her favourite old tree between Bologna and Ferrara). No reply needed: Dorit's "gute Idee, das mache ich", Remember Singapore's polite no.

## 2026-11-12 session: four more trees get Rainer Lippert's photographs

- **Live with this deploy**: the Bethmannpark Ginkgo and the Schwanheim Old Oaks in Frankfurt, the Three Oaks of the Weinmeisterweg and the Roadside Oak of Sacrow in Potsdam now lead with his photograph, credited and linked, his 10-10 yes in `permission`. Three had no photo; Sacrow's Commons lead moved into the strip. All four were held on 10-25 on distance alone; matched today on his page text instead (the ginkgo's 4.84 m of 2015 is our girth exactly; his twin oak is our 650 cm trunk; his roadside oak toward Krampnitz is ours; Schwanheim is the same wood-pasture grove). Pixels looked at.
- A looser pass (any genus, 3 km) over our 318 German trees without a unique photo found nothing else: the other ten near pairs are different trees by his own girths and places. His site is mostly rural giants; our gaps are mostly city street trees he has not photographed.
- pot_011's story lost a colon reveal (English and German) now that it faces Google.

## 2026-11-12 session: Rainer Lippert's yes on file

- All 57 of Rainer Lippert's photographs (52 German trees) now carry his 2026-10-10 yes in `permission` {words, date}, as the 11-10 compliance rule asks; they were on the baseline before. Each links his monumentale-eichen.de page; none came from monumentaltrees.com (hard rule 1). His yes covers photos from his own site only.
- Open: 149 of 381 German trees have no approved photograph. The 10-25 coordinate pass over his whole site (1,838 oaks, 551 other pages) found no more matches among our trees; his monumentaltrees.com photos of trees not on his own site are outside his yes and would need a new ask.

## 2026-11-12 night run (window from 11:21 UTC): two app-only trees, San Francisco a wall

- Rung 1 and 2 clear (no sightings, no notes; health only notes that GitHub dropped 7 of 12 knocks). Shelf said refill: verify pass on San Francisco found nothing new (seventh pass, register exhausted; the six Bush Street blue gums have no size, age or pin source, so they stay a lead). San Francisco walled for 48h.
- Write pass over the pending files: merged kcm_005 (Vaile Mansion Smoketree, Kansas City, copy rewritten for five trees) and csc_001 (Moreton Bay fig, Cascais, new one-tree place). Both app-only under APP FIRST. 15 entries held or duplicates (sfo_012/014/015 duplicate live trees; frk_027 schoolyard; dmr_002 unconfirmed standing; inn_007 private plot; brd_001 and cdl_001 access unproven; sgz_003 needs an honest access line, story already written; det_001/002 no coordinates).
- Many `data/research/*-verified.json` files are stale (already published); not deleted.

## 2026-11-12 session: a sign-in ends where the tap was going

- **Fixed (Hidde: tapping Isabelle R. on the home page asked for a sign-in and then landed back on the home page):** the website's sign-in sheet now keeps the exact address it was opened on and, for a visitor's name, whose photograph was tapped; after Google, Apple or the mail link the page goes there and finishes the act, so the name opens the profile. The same cause broke Follow on somebody's profile: Supabase returns to the path without its query, so `/profile?u=X` came back as your own `/profile` and the follow was dropped. Both fixed in signin-js.ts (head relay) and visitors-row-js.ts. Checked in a fake browser (jsc): home, profile with query, an unrelated page, an off-site address refused.
- **Apps:** iPhone (Home.swift `openVisitor`) and Android (Discover.kt `openVisitor`) asked for a sign-in on the same name and then did nothing; the sign-in now re-asks the row with the new session and opens the profile, and the row reloads on any sign-in. Every other gate in both apps already finishes its act (save, collect, map filters, add photo).
- qa `check_a_sign_in_ends_where_the_tap_was_going()`; escaped bug ESC-2026-11-12-a-sign-in-asked-by-a-tap.
- **Tested with the test account (apptest@), live:** website home, tap a visitor's name signed out, sign in: lands on her profile (Isabel R.). Website profile, Follow signed out, sign in: back on her profile, Following, row on the server, removed after. iPhone simulator: name, sign in, her profile opens. Android: CI green, not walked on a device. **Breakage on the way:** the first version failed two deploys (qa: the head read the stored session before catching the token, fixed 669cf1c2f), and the home name first stopped one step short (the profile loader was not ready yet; it now retries when the page has loaded, 73c5a6c98).

## 2026-11-12 session: a website photograph now counts as collected

- **Fixed:** Add photo on a tree page ticked the tree as collected only when it came through the collect flow, so the Lisbon photographer's profile showed nothing under Collected. A photograph now ticks it whichever button sent it, as in the app (add-photo-js.ts; qa `check_web_add_photo_is_shared()` now also guards this; escaped bug ESC-2026-11-12). Her lis_021 was ticked on the account by hand (visited, 2026-11-10); her profile shows the tree with her photo and pin, looked at.
- **Checked, nothing missed:** /contribute's form never received a photograph (0 of 227 submissions; the insert with a photo works, tested as apptest and cleaned up). Strangers' web tree tips: 18, 17 from one German contributor, none since the 2026-09-24 sign-in wall (Hidde: leave the wall). 13 stranger accounts have ever added a photograph, 12 with one live.
- **Drafted, not sent:** drafts/reply-piero-unalberoalgiorno-2026-11-12.md, asking where the weeping sophora of his 11-01 website photo stands and what makes it special (no promise to map it). Waits for Hidde's yes.
- **A photograph is always a visit, every route (Hidde: "waar je hem ook vandaan komt"):** web, iPhone (CollectSheet.claim) and Android (Collector.collect) already tick at the photograph; the hole was readers' NEW trees, which get a tree id only when we publish them, so seven readers' own published trees (Tangier, Palermo, Paris, Freiburg, Lisbon x2, La Tène) plus one of ours were missing from Collected. Ticked now. `scripts/sightings_link.py` (every knock) ticks any photographed sighting on a tree that lacks it, dated the day it reached us, skipping photos a viewing pass rejected as the wrong tree. qa `check_a_photo_is_a_visit_on_every_surface()` refuses a push where the iPhone records a tree photo without the tick or Android sends one around `collect()`; verified red with each fault put back.

- **North star on top of the digest (Hidde: "een totaallijst ... bovenin"):** `north_star_line()` in daily_digest.py, above his numbers: strangers who ever uploaded a tree or photo of their own, and those who did on more than one day, each with this week's change, dated by the photo file's upload time (Hidde: "upload datum is relevanter"). Today: 13 (+2), 4 more than once (+0). **Broken since it was written, fixed:** the "Readers' contributions" row read `sightings.created_at`, a column that does not exist; the query failed silently and no app photograph was ever counted. It now counts the same upload days.
- **Own trees on a profile, checked:** your own view (iPhone My trees, web /account, Android) shows every tree you added, live or not. Somebody else's public profile shows only collected catalogue trees and Want to visit (`public_profile()` returns nothing else), so a reader's own tree we did not take into the map is invisible to others. Today that is no stranger's tree (the one unpublished, Tree Hugger's Santranges well, Hidde closed on 10-21); every other reader tree went live and is now ticked. Building the public half needs a change to public_profile() (a paste for Hidde) and the three profile screens; not started, waiting for his word.

- **North star on the digest page as two stat tiles with a 12-week sparkline each** (show_digest.py; Hidde: "visueler"). Local page only; DATA.md keeps the line.
- **Approved and own trees on a public profile, web half (Hidde approved the design, preview/inspect/approved-mock.html):** supabase/approved-on-profiles.sql (FOR HIDDE to paste: `sightings.added`, public_profile() returns `approved` and `own`); sightings_link.py marks `added` from the city files' found_by_reader every knock (says "FOR HIDDE" until the paste); /profile draws "Approved" top-left (style.css `.appr-chip`, the app's MineCard capsule at the city pill's size) and the person's own trees with their shared photograph, linked to /t?id=, and their pin; privacy page says so (privacycheck green); CONVENTIONS.md "Your own trees on a public profile". Live after the paste and a deploy. **Not done:** the iPhone and Android profile tiles. **Dropped:** a "Hide the exact spot" switch was designed and Hidde said no (a tree on a profile is for walking to; it would cost us the location we need); the column left the SQL before anyone pasted it, and the privacy page no longer mentions it.

- **A deleted account keeps its trees, published or not (Hidde: "als we een boom niet approven maar nog 2 andere m aanmelden we m alsnog goed kunnen keuren"):** the website's account deletion now removes only the avatar from storage (was: every photograph in the sightings bucket); the lead in data/leads/_sightings.json was already unlinked and kept (photo_takedown.py, since 09-04), now its private photo stays with it; `sightings_link.py` takes public shared-sightings copies of gone accounts down every knock (0 today). qa `check_a_deleted_account_keeps_its_photographs()` refuses the web purge coming back (verified both ways); privacy page, terms and CLAUDE.md say the trees stay, unlinked. **Not done:** the iPhone and Android deletion still purge the photos until their next build; sent to the running app session (Approved and own trees on app profiles) with the check to extend. **Supabase audit, read-only:** no duplicate tables (`wishes` is a view over saves); unused: view `shared_trees`, function `tree_save_counts`; loose files from the 08-27 deletion test week and Hidde's replaced photos. Nothing deleted: Hidde wants trees kept, so the clean-up waits for his word per item.

- **Sent (Hidde: "verstuur"):** Piero (un albero al giorno), a follow-up in his thread, Italian: his 11-01 website photo only reached us on 11-11, where does that weeping sophora stand and what makes it special. No promise to map it.
- **Live (Hidde pasted supabase/approved-on-profiles.sql):** sightings_link marked 7 reader-found trees `added`; public_profile returns `approved` for 7 readers (prf_001, lis_038, par_034, tng_001, plm_006, lis_037, frb_008) and `own` lists; the website draws Approved (looked at on Peter Kálnai's profile, Tangier fig). Moderated: the closed Santranges well (not a tree) set unshared so it is off Tree Hugger's public profile. Note for Hidde: his own public profile now shows his 29 own test trees with their pins. App PR #59 green but conflicting with main; its session was asked to rebase and merge.

## 2026-11-12 07:32 UTC night run (rung 2, short)

Rung 1 empty (no sightings, no new notes). health.py had one open APP BUG row: the shared tree's photo URL was force-unwrapped. Fixed in SharedTreeView.swift (percent-encoded, nil when invalid, 0d625d527) and the row set `fixed`. No Swift test: it cannot run on this Linux runner, so the row says so. Health is green apart from "5 of 12 knocks delivered", which is GitHub dropping the cron. I did not start tree work: the shelf wants a verify pass (930 leads one source short), which I did not take in this window. For Hidde: next iOS build carries this fix.


**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-11](archive/LOG-2026-11.md)
- [2026-10](archive/LOG-2026-10.md)
- [2026-09](archive/LOG-2026-09.md)
- [2026-08](archive/LOG-2026-08.md)
- [2026-07](archive/LOG-2026-07.md)

## 2026-11-12 session: Android opens faster, and its sheets grow like the iPhone's

What changed in the Android app:
- The map shows its first trees sooner. On the emulator with a release build, the first pins came after 9 to 13 s on a first launch and 4.5 to 7.5 s after that; now 3.1 s and 2.3 s (median of five each, measured with nothing else on the emulator; the older numbers were taken while other sessions shared it). The iPhone simulator on the same Mac takes 1.5 to 1.7 s and 1.1 to 1.3 s. Two causes fixed: the catalogue only started loading once the screen was drawn (it now starts with the app), and the map's style was fetched from the network every launch (it now comes from the copy on the phone, kept fresh in the background, with one built into the app for the very first launch).
- That leaves Android about 1.5 s behind on a first launch and 1.1 s on a relaunch, mostly MapLibre starting its map; a real phone has not been measured.
- Sign-in and the other fitted sheets now drag up to the full height and back, rubber-banding at the top, as on the iPhone (audit row 12). A drag down from the fitted height still closes them.

Breakage: none known. The emulator's swipe injector sometimes delivers the lift late, so a fast flick reads as a stop there; the logic was checked with flicks that arrived on time and with slow drags.

## 2026-11-11 session: Android's icons and type as the iPhone's

What changed in the Android app (the review's icon and type rows, out/parity-feel/visual-review-2026-11-11.md):
- Sheets: iOS 26 draws a fitted sheet at full width and scaled about 4 percent smaller; Android now does the same (Sheet.kt). That was the "Gabarito 4 percent too wide": outside sheets the titles already matched to 1 dp. Text breaks as Apple's does: a two-line text never ends on one word ("Are you enjoying / Ancient Trees?", "...and the / Privacy notice."), a longer one may.
- Species silhouettes are flat and one-tone, as the iPhone draws them; the wingnut no longer reads as a weeping crown. The ticket badge on paid-entry pins draws again (its glyph was off the disc).
- Glyphs: the My trees leaf, curved directions arrow, outline sparkles for Plus, the early adopter's sparkle, an empty speech bubble for Send feedback, the needle pin in the pin picker, building icon in search, the round flat flags (the iPhone's flag-icons set), and sizes and weights read from the Swift (chips, card bookmark, close cross, tile glyphs, sheet buttons, tree page camera and thumbs, season tiles, Settings rows and chevrons, gear and Find people).
- Type: search sets only the typed letters heavy, cultivar names upright, card meta lines 13 with the faint dot and the species giving way first, no more mid-word clipping of two-line card titles, navigation titles in Gabarito, Form sheets on the system's cool grey with 26 corners and the system's placeholder grey.

Not changed, on purpose: the My trees gear still fills as the sheet rises. The Swift does that (Hidde, 2026-10-08); the iPhone frames show it outline only because the progress never reaches the button there, an iPhone bug.

## 2026-11-11 session: photographs sent from the website never reached the inbox

- **Broken since 2026-09-23, fixed:** the website's Add photo inserted its sightings row without `shared`, the production column default is false, and the inbox and the photos page read shared rows only. So the only two photographs ever sent from a tree page (Padua 11-01, Lisbon 11-10) sat unseen, behind a "we look at every photograph" promise. add-photo-js.ts now sends `shared: true` as the app does; qa `check_web_add_photo_is_shared()` guards it (fails without the fix, checked); escaped bug ESC-2026-11-11-photographs-sent-from-a-tree-page-on-the, caught by that check. Live with the next deploy.
- **The two stranded photographs:** set shared on the account and judged after looking. Lisbon's lis_021 Tipuana, in full yellow flower in the roundabout garden, published as its first photograph (the "on the page" mail goes at the next knock). Padua's was a weeping pagoda tree in a private front garden, not Piazza Capitaniato: rejected as the wrong tree.
- **Nothing else missed:** the sightings bucket holds 48 files without a row; 45 are ours or a deleted test account, the three strangers' are from before the web upload existed or carry the app's uppercase file names.
- **Why the week was quiet:** 8 stranger photographs 11-01 to 11-05 (5 from one Paris visitor on 11-02), 1 since; no failed app syncs in PostHog. "Stop sharing the link" is still in 1.0.3's menu (gone from 1.0.4), but nobody used it.

## 2026-11-11 daily publish (scheduled task): the last 3 held trees into the app, queue empty

- **What went on main, app only under APP FIRST, no web page or place page:** the Bute Park Tulip Tree as Cardiff's crd_010 (13 trees) and Windsor's first two, the Signing Oak and the Canadian Memorial Avenue pin oak (wsr_001, wsr_002, a new place), from build_uk_under_ten.py limited to those two places (out/tmp/build_uk_under_ten_cardiff_windsor.py). city_names nothing to do, preflight 0 problems; app-only trees do not count against the pace.
- **Checked:** /cardiff 200, /windsor 404, as APP FIRST wants. No claims stood on either place.
- **Daily publish: queue empty.** Every builder since 11-02 is now on main; the trees still on the shelf are held for their own reasons (see the 11-08 entry). For Hidde: the daily task "publish-held-trees-daily" can be switched off under Scheduled; the night run's write passes put new trees straight into the app.

## 2026-11-11 session: Android's glass, and the last small controls

- **What changed in the product:** on Android 12 and later, the tab bar, its camera disc and the round buttons over a tree's photograph are frosted glass like the iPhone's: what lies behind them is blurred under a milky tint. Before Android 12 they keep the opaque ground they had. The one thing the glass cannot frost is the map itself, which MapLibre draws on its own GL surface. Photographs that are still loading wait on the iPhone's grey, row thumbnails on the moss tint, and the big tree card shows a white spinner. Until the catalogue is read the app shows the oak mark and a spinner, and after six seconds the iPhone's "taking longer than it should" line, in eight languages. A long press on Take a photograph opens the library, iNaturalist's shortcut.
- **Library:** Haze 1.7.2 (dev.chrisbanes.haze), the release built against this app's Compose 1.10 and Kotlin 2.2.21, for the backdrop blur (hard list 5). It moves androidx.activity to 1.12.2 and nothing else.
- **Kept as Android's (Airbnb's line):** spinner and toggle shapes.
- **Parity:** "Glass behind floating bars" is off `_android_forced`, with its source.

## 2026-11-11 session: Android has build 42's map sheet

- **What changed in the product:** on Android, as on the iPhone since PR 40, the map's list at full height is now the page under the search field, with no grip and no count. The Map pill drops it to a new lowest stop where only the count shows and the tab bar steps away, and a tap on that bar brings both back. A drag starts after 18 points and a flick is projected the way SwiftUI does (audit row 30). The grip, the count and the corners change with the sheet frame by frame. Every city and country map follows, since they are the map tab; My trees keeps its stops.
- **Checked:** map, map-full and map-bar shot on both phones and looked at side by side; pill, bar and flick walked on the emulator; a new FlowWalk step covers pill and back.
- **Open:** about 10 points less air above Highlights than the iPhone, left to the spacing measurer. The projection's quarter second is the commonly reported figure for SwiftUI, not read from Apple's source.
## 2026-11-11 session: Android ready for Google Play, waiting on Hidde's verified account

- **Release build**: `python3 scripts/android_release.py` builds the .aab with R8 on, signed with a new upload key that lives only on the Mac (`~/.ancienttrees-android-upload.jks`, passwords in `~/.ancienttrees-android.env`, never in the repo), checks the signature and copies it to out/play/. SHA-256 of the upload key `4F:42:47:55:68:02:7B:2D:4F:B6:ED:54:82:62:3B:00:84:B7:8B:B5:AB:5D:E1:9B:B2:CD:CF:32:6D:75:2F:F2`, now in assetlinks.json beside the debug key; Play App Signing's key joins after the first upload.
- **Runs**: the release APK installed on the emulator, map, Discover, My trees, a tree page and back, no crash (`scripts/android_release_walk.py`). No AD_ID permission in the merged manifest.
- **CI**: android.yml job `release` builds the release bundle unsigned on every Android change and fails on an AD_ID permission.
- **Drafts**: drafts/play-store-listing.md (eight languages, `scripts/play_listing_check.py` counts and pitch-checks), drafts/play-console-forms.md (Data safety, content rating, audience, ads, closed test), drafts/play-console-steps.md (his click list, Dutch). Graphics in out/play/ on the Mac: icon 512, feature graphic from the press logo, four phone shots 1080x1920 from the release build (`scripts/play_shots.py`).
- For Hidde: category and public contact address are his choice (in the listing draft); then the click list once Google has verified him.

## 2026-11-11 session: a map library that does not load no longer stops the page

Nothing changes for anyone whose map loads. When the MapLibre script never arrives or the browser cannot parse it (3 reports in 24 hours: /hong-kong on Chrome 75, /assen and a Waremme tree on Chrome 156), the rest of the page now keeps working and the map's buttons hide, as they already did without WebGL. `atCanMap()` in lib/map.ts asks for the library too; qa's `check_a_map_is_only_built_when_it_can_be()` holds it. Tested on a copy of the live Waremme page without the library: the old code threw this error, the new code throws nothing. The full qa needs the CI build; only the new check ran locally. web_errors stays red until these reports fall out of its 24 hours.
## 2026-11-11 session: Android moves like the iPhone (feel audit, PR 44 and this PR)

- **What changed in the product:** on Android a page now slides in over the one under it, and the back gesture drags it with your finger. Each tab keeps its own history and scroll, and re-tapping a tab goes back to its root. Sheets slide down before they go, and the fitted ones float as a card with the cream handle. The save and collect haptics are in. Photographs stay on disk between launches (256 MB, Android's own HTTP cache, no library). Collect steps cross-fade, the photo viewer and search slide up as covers, the snackbar leaves properly, carousels snap to the margin, pins no longer blink on a data swap, and the near-a-tree banner exists, with its light tap, in eight languages. The tree's own map is a pushed page, so back returns to the tree.
- **Under Airbnb's line (Hidde, 2026-11-10):** the press is Android's ripple clipped to the button, and the overscroll is Android's stretch, off on the tree page.
- **Checked:** android.yml build and walk; the emulator walk including the signed-in round trip; slowed frame sequences and normal-speed frames of push, back drag and cancel, sheet in and out, viewer up and down (out/feel/). The walk caught one crash of mine before merge (a map style transition set while a newer style loaded), fixed.
- **Not done:** audit row 12 (a fitted sheet that also drags to full height) needs its own sheet component, Material's has one fitted stop; most Low rows. data/android-parity.json `_feel` lists every row.

## 2026-11-11, night run, second attempt (no new trees)

Nothing visible changed in the product. The shelf is empty and the staged cities have almost no placed leads.
- The 7 READY leads (St. Louis 2, Tucson 2, Vienna, Windsor, Segovia) went to a write pass. All 7 were held, each with a reason: a ticketed garden over the one-third limit, no public access, no way to tell which trunk, or nothing visible as a reason to go. They are now `status: held` with `held_why`, so READY reads 0.
- Verify claims on Braga (5 leads), Graz (0 of 11 placed) and Nuremberg (3 of 16 placed) were released without dispatch. Braga is under six candidates and the other two have too few coordinates. All three are walls for 48 hours.
- Portland is full (33 of 30). The "awaiting a writer" pile is stale files of trees already published.
- Next run: a coordinate source for Graz or Nuremberg (a register with tree-level points), or a Windsor register retry.

## 2026-11-11 night run (window from 01:40 UTC)

Rungs 1 to 3: no reader photos or notes waiting; health.py's only finding is that REVIEW.md is 2 days old (`gh workflow run review.yml` refused from the runner, HTTP 403) and one new web error type ("maplibregl is not defined", 1 report, 1 page, below the red threshold). Rung 5, write lane: New York merged 1 tree (nyc_144, the Pagoda Tree by the Camperdown Elm, no photo, app-only under APP FIRST). The shelf's "awaiting a writer: 392" is mostly stale: 38 of 39 New York trees and all Chicago trees were already live, so the Chicago pass wrote nothing. For Hidde: prepare.py's awaiting-a-writer count overstates the shelf; the research files passcheck calls stale could be cleaned up. Not done: a verify pass on a staged Portugal, Germany or Austria city.

