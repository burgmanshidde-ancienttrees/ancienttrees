# LOG

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-10](archive/LOG-2026-10.md)
- [2026-09](archive/LOG-2026-09.md)
- [2026-08](archive/LOG-2026-08.md)
- [2026-07](archive/LOG-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
<!-- archive-index -->
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

## 2026-10-14, window 23:30 UTC, second attempt: no new trees live

Write pass on the 55 READY leads published nothing: none passes the rich-or-reader rule (no girth, pin or photo; Roosendaal and Delft notes decline them; Barcelona's Huingan is already live as bcn_041 and still shows READY because the name check misses it). Batenburg's chestnut would be rich but is one tree in a new place below four. Miami verify (third pass) found nothing for Miami; one Key West tree (kyw_001, Firehouse Museum mamey, Florida champion, 328 cm) is in data/research/miami-verified.json, flagged, no photo, no recognition line, so not published; three more Key West leads filed (the mangrove is a private house). New refusing hosts: overpass-api.de, wlrn.org, keysweekly.com. Claim released. Cost: write pass about 75k tokens, 0 trees; verify about 130k, 0 live. Next: a photo or pin pass on Roosendaal/Munich, or a Key West recognition line plus two more rich trees to reach four.

## 2026-10-14, window 23:30 UTC: deploy repaired

7-day visits: 1621 visits, 2340 page views. No reader submissions. Rung 2: the site build had failed since a London tree was recorded as "London Plane (Platanus x hispanica)" while every other city says x acerifolia (hard rule 9, checkSpeciesNames). Changed that one species field in london.json to x acerifolia, preflight 0 problems, pushed; deploy should go green on the next push. iOS scheduled failure (SweepFrames layout drift) untouched, app work. No trees added: the window opened 23:30 and the checkout was 8 commits behind main until pulled.

## 2026-10-15, second retry: Roosendaal 13 to 16

Roosendaal deepen pass: verify found two LRMB trees with confirmed pins, girth and height (roo_020 London Plane, Oostelijke Havendijk, 407 cm; roo_021 White Willow near Nispen, 502 cm), both view-only and said so. The writer corrected my verify notes against the register (Schietwilg is white willow, not a pollard; age band 1900-1910). roo_019 (sycamore) got a concrete sourced access line and is now live. City copy recounted to 16, plane species spelled x acerifolia to match the site rule. Preflight 0 problems; the site build was not run in this session (command denied), so the deploy is the check. Eight more leads filed; Roosendaal's 300 cm+ register list is exhausted. The other "written and ready" trees (Leipzig, Delft, Fort Worth, SLC) stay out for the same preflight reasons. Claim released. Cost: verify ~90k, write ~75k tokens, 3 trees.

## 2026-10-15, retry attempt: nothing published

- No product change. Claims were clear. All 55 READY leads are ordinary trees (Roosendaal 17, Munich 5, Delft 5, others), which recovery mode and preflight's rich rule refuse, so I dispatched no write pass. The 12 "written and ready to merge" trees were already tried on 10-13 and preflight refused them (not rich, approximate pin, thin access line); they stay out.
- `enrich.py` has nothing to do anywhere. `langcheck.py --next` has an empty queue (24 cities under 10 English impressions). The lanes left need a session or a new source: Roosendaal roo_019 needs a sourced access line, Miami and Key West have no per-tree register, the German cities lack girth data.
- iOS app scheduled-run failure at session start is untouched (app work, needs a session).

## 2026-10-14, night run (window 22:25 UTC): Roosendaal 10 to 13 trees

7-day visits: 1621 visits, 2340 page views. No reader submissions. iOS app scheduled run failed on layout drift in the SweepFrames check (collect-intro 'Photograph a tree you are standing in fro...' on iPhone SE iOS 18.x); app work, not touched here. Roosendaal deepen pass: verify found four LRMB trees, three merged as roo_016 (Lebanon Cedar, Villa Van Gilse garden, confirmed pin), roo_017 and roo_018 (Paterstuin cedar and chestnut, small-site pin); roo_019 (Nispen sycamore) refused by preflight because its access line is not concrete, story kept in the verified file, needs a sourced access line. Eight lead entries filed. City copy recounted to 13. Preflight 0 problems.

Oss reopened with five LRMB register trees (oss_001, 007, 011, 012, 013), all rich (confirmed PDOK pin, register link, measurement, concrete access). It had been removed on 2026-10-12 only because the live count fell below the four-tree floor; the oss to den-bosch city redirect and two retired tree slugs are removed from redirect-map.ts so /oss serves again. data/leads/oss.json still holds the old removed copies of oss_001 and oss_007. Preflight 0 problems.

Potsdam: pot_010 (Sessile Oak of Paetowstrasse, Naturdenkmal 39, confirmed pin, 450 cm) merged with German overlay; a Commons photo exists but was not viewed. Vienna (one possibly dead poplar, cadastre WFS empty) and Spokane (one park-entrance tree, parks are not small sites) gave nothing publishable and are walled 48h; the Spokane Grant Park Guardian chestnut is the call for a session if an entrance should count. Oss and Roosendaal enrichment gaps (season only, no real peak) closed as dead ends. pagegaps: nothing missing.

Photo viewing pass 4: 41 images viewed, 5 approved (pot_005 Sacrow oak, pot_006 Bassinplatz oak, pot_008 Schiffbauergasse oak, pot_010 Paetowstrasse oak, stu_007 Hohenheim plane, the weakest: trunk hidden by shrubs), 66 rejected, none held. Reverse one with `python3 scripts/photo_apply.py reject <id> <commons url> --reason "..."`. Pillow is not installed on the runner, so photo_light.py scored nothing and exposure was judged by eye.

Chicago 16 to 21: five Cook County Forest Preserves champion trees (chi_018 to chi_022, Thatcher Woods and National Grove), register-only and flagged, GPS-fix pins confirmed, free sunrise to sunset; chi_016 dropped as a duplicate of chi_019. Remaining ~70 Chicago leads are isolated champions with no cluster near live trees. Miami verify (third pass, no rich tree) filed nothing and is not worth a fourth without a reader photograph at a champion stop.

London 27 to 29: lon_028 the Carshalton Plane (39.6 m, 7.6 m girth, Forestry Commission remeasure August 2026; third tallest, not tallest in Britain, said on the page) and lon_030 the Gunnersbury Park Black Mulberry (fruit July to August best_time, small-site pin). lon_029 Marble Hill Black Walnut is written but preflight refuses it (approximate pin, no site, no photo): it ships once a photograph or small site is found. Woodland Trust data was not touched. Washington DC: nothing publishable (Douglass white oak wdc_017 held: pin is borrowed from the magnolia, no recent alive evidence; Northampton white oak fell July 2024); walled 48h.

Seattle 16 to 19: sea_017 Roanoke Park white elm, sea_018 Ross Playground bigleaf maple, sea_019 Wallingford pin oak (SDOT Heritage register rows in free parks, register-only, flagged, pins are the register's coordinates). San Francisco: nothing can end rich (Public Works list has no per-tree record, measurement or coordinate); walled.

Heidelberg and Regensburg: nothing publishable; the Naturdenkmal sources give no girth or height and only map-centre coordinates. Unblock: a municipal Baumkataster export or a reader's measurement (Commons photos exist for the Heidelberg Aukopf and Muenchelstrasse oaks and the Regensburg Tegernheimer oak). Window total: Roosendaal +3, Oss reopened (5), Potsdam +1, Chicago +5, London +2, Seattle +3 = 19 trees, 5 photographs approved.

## 2026-10-14, retry attempt: nothing published

Released the standing Leipzig claim: its brief shows no imported register within 20 km, and its four written trees (lpz_019, 021, 022, 023) are the kind preflight refuses as not rich. Leipzig is a wall for 48h. The 53 READY leads are thin register rows (Roosendaal, Oss, Munich, Delft and others), refused by the same rule. langcheck has no city over 10 English impressions to translate. No agent dispatched, because no candidate can end rich. Still open: the iOS app workflow failed on 2026-10-14 and its log was not read.

## 2026-10-14, night run (window 20:46 UTC): nothing shipped, two passes found no work

7-day visits: 1460 visits, 2060 page views. No reader submissions or app photographs waiting. health.py's "skipped" deploys were push runs superseded by a dispatched deploy still running; the iOS failure is Build 34, a rerun was in progress (not touched).
- Enrichment: claimed six cities (Minami-Alps, Minamiaso, Miriam Vale, Mito, Nago, Nanjing). A parallel run had already closed those gaps before the verify agent ran, so the brief was empty. `enrich.py --next` says nothing to do anywhere. Claims released. `www.xhby.net` hung at 20 s (not yet in the blocklist).
- Refill: verify pass on Rothenburg ob der Tauber (22 unmined register candidates). The Bavarian Naturdenkmal register has no girth, height or age, so none could end rich. Bettwar ND 49 and 50 filed as leads. Rothenburg is a wall for 48h.
- Not merged on purpose: the "written and ready to merge" trees (Leipzig, Oss, Delft, Fort Worth, others) are the ones preflight refuses. Four research files hold duplicates or id clashes needing a hand check: chicago chi_016, munich muc_062, taiwan a28_001, philippines phl_003.
- Git: one push was rejected and the rebase conflicted in data/in-flight.json; resolved by keeping my claims.
- Photos: `photo_hunt.py --recheck` found nothing new, so a photo-judge pass viewed 49 images for 32 trees already in the queue: 15 approved (mls_003, zyw_001, tor_008, nap_019, kra_035, tor_010, sqk_001, sto_005, vyt_001, com_008, stk_001, yab_003, trs_001, wis_001, tre_004), 4 held, 30 rejected. Reverse one with `python3 scripts/photo_apply.py reject <id> <page> --reason "..."` (form inferred, not run). Light score was blank (Pillow missing here), so exposure was judged by eye.
- `gh workflow run deploy.yml` was refused (HTTP 403, token cannot dispatch), so the photo approvals go live with the next deploy that runs. Stopped after the photo pass at 21:25 UTC; the lanes left (refill needs a rich register, 51 READY leads are ordinary street trees) have no cheap work.

## 2026-10-14, late retry: Trieste in Italian

- **Trieste now has an Italian page**: title, intro, oldest-tree question page and all 36 trees (data/i18n/it/trieste.json). i18ncheck and preflight clean. It was the only city over 10 English impressions still untranslated.
- Needs a fix in the English: tri_009 ("outlived the square's own name twice over" reads as nonsense); tri_023 to tri_027 age field says about 130 years but the stories say 115 to 170.
- Left the 51 READY leads unwritten on purpose (ordinary street trees, recovery mode wants new trees rich). enrich.py has nothing left anywhere.
- Not touched: the iOS workflow failure from session start.

## 2026-10-14, retry of the 19:17 window: Como in Italian

- **Como now has an Italian page**: title, intro, question page and all 9 trees (data/i18n/it/como.json). i18ncheck and preflight clean. Taken as the translate backup because `enrich.py --next` said nothing to do anywhere. Italian is still unproven and Como has 12 English impressions, so this is a small bet.
- Removed two lines of our own working notes from the public English access text of com_005 and com_009.
- Left the 51 READY leads unwritten on purpose: most are ordinary street and car-park trees (Roosendaal, Sittard), and recovery mode allows no new tree unless its page is rich.
- Not touched: the iOS workflow failure flagged at session start (`gh run list --workflow=ios.yml -L 5`).

## 2026-10-14 night run (19:17 UTC window): red deploy fixed, two Roosendaal trees

7-day visits: 1,440 visits, 2,030 page views.

- **Fixed the red deploy.** Seville sev_044 (the mailed cactus photo) was approved but the gate dropped it: no attribution and no `source: "contributor"`. It now carries `source: "contributor"` and `unlinked: true` (no account id exists for a mailed photo; preflight allows exactly that pair). Pushed as f20ac2c7.
- **New trees: Roosendaal roo_014 (Oak of Nispen) and roo_015 (Beatrixlinde of Nispen).** Both from the LRMB register with girth, height and a lone-crown pin like roo_012 and roo_013. Neither has a photo yet. Roosendaal is now ten trees, four of them in Nispen.
- **Leipzig, nothing published.** The city's open Baumkataster WFS (`geodienste.leipzig.de/l3/OpenData/wfs`, layer `OpenData:Baeume`) gives girth and height per Naturdenkmal tree, which is a new lane. Three stories were written (Ginkgo of Kleinzschocher, Elm of Poelitzstrasse, Oak of Probstheida) and preflight refused all three: approximate pin, no photo. The Commons photos I fetched are sign close-ups and an ivy-covered worm's-eye view, so all three are held as leads. Eight Naturdenkmal leads are on private ground. New lead: the two Torhaus Doelitz oaks (570 and 550 cm).
- **Photos:** `photo_hunt.py --recheck` swept 40 trees; `photo_fetch.py --zero` fetched candidates for 13 cities; the ones I viewed were leaf close-ups and building shots, none approved.
- **Breakage, not mine to fix from here:** the iOS workflow failed on 2026-10-14 (run 38611221113) because simulator creation took about 40 minutes and `xcodebuild test` was killed after a 20-minute hang. It is infrastructure; the app code did not fail an assertion.
- **Enrichment, 8 of 10 trees:** Gliniak (Wszebora) register id and measurements, Grybiskes saugoma.lt record, Higashine kunishitei record, Himmelsberg Naturdenkmalbuch number, girth and height for Granit, Hel, Hino and Hniszow. Higashiomi and Horn-Lehe stayed dead ends (5 gaps recorded for 90 days).
- **Enrichment, second batch, 5 of 10 trees:** Lipka linden (AOPK 8409, girth and height), Agency for Cultural Affairs records for Kagoji, Renchakuji and Itoshiro, Kuningamand register id. Jauze, Junihon-yasu and Boole Tree stayed dead ends.
- **Enrichment, third batch, 5 of 10 trees:** AOPK records for Kotel and Lazy (Lazy with girth and height), Kitamoto and Kitakata records (Kitakata with girth and height), Ksiaz CRFOP id (second-hand, labelled so). I withheld the Kremnica girth: it came from a Tree of the Year nomination, not a register, and the height of measurement is unstated.
- **Enrichment, fourth batch, 4 of 10 trees:** Miharu, Maibara and Lohja authority pages (heights), Magescq commune page (girth at 1.3 m and height). Open question for a session: the Lohja city page puts its tree in the Paavola school yard, while our access line says nature reserve and trail; the two descriptions differ and are not reconciled.
- **Enrichment, fifth batch, 7 of 10 trees:** Agency for Cultural Affairs records for Mitsue, Mito, Nago (girth and height), Neba and Nichinan; Queensland Heritage Register id (Miriam Vale fig); AOPK id (Pernstejn yew). Withheld the Mitsue girth (eye-height figure at designation, not 1.3 m). Open for a session: the Nichinan record calls its yew a prostrate kyaraboku (Taxus cuspidata var. nana), so our species field may want a look.
- **Enrichment, sixth batch, 3 of 10 trees:** Oguni ginkgo and Ono Suwa cedars (Agency records with girth, cedars with height), Odawara city record. Yield is falling. Open for a session: Ottendorf (Gaedheim) was removed from the Naturdenkmal list in 2006; the tree itself may be gone or merely delisted, which nobody has checked.
- **Enrichment, seventh batch, 6 of 10 trees:** Polchow (Naturdenkmal 61, girth and height via de.wikipedia citing the DDG record), Pelham and Pemberton heritage records with heights, Radomsko CRFOP id, Poleski National Park ticket prices, Prosec USOP code. Withheld: Radomsko and Przybudki measurements (individual-run register, encyclopedia), Prosec's Wikidata pin (not tree-level).
- **Enrichment, eighth batch, 1 of 10:** Rumskulla (Kvill oak) girth from the county reserve page. **Needs a session:** the Witch's Spruce of Rambynas (rmb_001) is reported dead by 15min.lt and Diena. It was the place's only tree, so I first reverted, then found the Oss precedent (b0913b37) and did the same: `retire.py` (tree to leads, REMOVED_TREE_SLUGS), `["rambynas", "silale"]` added to RENAMED_CITY_SLUGS so /rambynas and its tree URL redirect to Silale (nearest published Lithuanian place), city file removed, preflight 0 problems on 719 cities. I could not run the build, so the next deploy is the proof; if it is red, look at redirect-map.ts and qa first.
- **Enrichment, ninth batch, 5 of 10:** Agency records for the Shimizu cycad, Shingu nagi and Narao akou (with a 50 m shrine-path site), Sicilian monumental-tree code for the Sant'Alfio chestnut, an October-November best_time for the Sittard copper beech from the species file. Shingu's eye-height girth withheld.
- **Wrong pin fixed (rung 3): Stokaiciai stk_001 (Visbaru pine).** Our longitude was 22.221519; the state protected-areas page and lt.wikipedia both say 22.033 (same latitude), about 12 km west. Moved to 55.378358, 22.033334 and set to approximate (the old "confirmed" had no pin_source). The tree is alive but in poor condition (2022 survey: lower trunk broken; the district council declined to delist it in 2024). Also this batch: Tatobity and Teleci AOPK records with girth and height, Tillamook Heritage Tree page, Toga record, Ambrosius-egen protection record, Stokaiciai register id. Trainiskis's listed tree is the young clone of the delisted fallen oak.
- **Enrichment, eleventh batch, 4 of 10:** Untermerzbach ND id, Villamudria register id and height, best_time for the Vorden lime (June-July) and Vepriai oak (Sept-Oct) from the species files. Open for a session: (1) Velp's Philemon oak has an LRMB coordinate 29 m from our pin (LRMB 1677461) that `--apply` refused without a source URL, and Baucis, its pair, fell in storm Ciaran in 2023, so check the Velp copy does not call it living; (2) es.wikipedia says the Villamudria oak is inside a double fence, our access line says walk up to it.
- **Enrichment, twelfth batch, 7 of 10:** Westerlo, Wolfheze, Yamanashi, Yoshida and Zalgiriai records; girth and height for Zalgiriai and Zwieslerwaldhaus; Yamanashi girth from the Environment Ministry database. Open: the Zwieslerwaldhaus GPS fix (49.098683, 13.230611, about 45 m from our pin, from the Nationalerbe-Baeume page) was refused by `--apply` for lacking a source URL.
- **Translation:** Lucca into Italian (13 English impressions), all 14 trees, i18ncheck clean. `enrich.py --next` now says nothing to do anywhere for non-roster cities; pagegaps is empty.
- Species note: roo_015 reads "American Lime (Tilia americana 'Nova')" while Chicago and Minneapolis say American Basswood. Rule 9 says one common name; worth aligning on a later pass.

## 2026-10-14 session: app 1.0.3 (build 34) submitted to Apple

- Hidde submitted 1.0.3 build 34 for review this evening.
- In it: collecting needs a photograph (app and web), always "Which one is it?" before a tree is collected, the email sign-in link opens the app (ancienttrees:// scheme), a confirmation after saving a new tree, a new draft keeps its photo (one sightings store per launch), lighter opening photos (his Itoshima camphor, the Unsplash camphor, General Sherman with credit), camera icons on the collect controls, sign-in buttons aligned, calmer sheets throughout.
- Store: seven new screenshots (6.9 and 6.5 inch, asc_screenshots.py), Hidde's Lisbon description and plain What's new in nine languages, promotional text "Autumn is here...", English subtitle "Find remarkable trees near you", English keywords rebuilt from search data, a header image (Unsplash camphor). Search Results asset left empty on purpose (screenshots sell better there).
- Open: the double "Open in Ancient Trees?" prompt on the email link (which mail app?); whether to keep the second photo permission (save to Photos).

## 2026-10-14 session: a reader's cactus goes live in Seville

- **New tree, sev_044 The Cardón of the Expo** (Pachycereus pringlei, Isla de la Cartuja): Mexico's gift for Expo '92, flown in 1992 from the Valle de los Gigantes. A reader replied to our mail with a geotagged photograph; the tree was already in Seville's 2022 catalogue (ficha 27) but sat blocked in leads on titularidad 'Particular'. The photo shows it on an open paved street corner, so it ships. Pin confirmed from the photo's GPS (14 m from the catalogue's). Spanish overlay written, question_meta counts bumped (en/es).
- The reader's mailed photograph is on the page, uncredited. Hidde ruled the same evening that a photo mailed to us is ours to use (now in CLAUDE.md Photos). Reply drafted in drafts/reply-peter-kalnai-seville.md.
- Age left broad: catalogue and press say 1,500 years, the reader 200 to 300.

## 2026-10-14 late run: finished a stranded enrichment claim

An earlier attempt claimed friedewald+galenbeck+giethoorn+gjerrild+gutau+haarlemmermeer+hainich and never dispatched. I ran the verify agent and applied it: five trees improved (Hammundeseiche, Betteleiche and Gutau yew measurements, Gutau Naturdenkmal id nd292, Svalebøgen Dansk Træregister record 181 with girth, Galenbeck linden measurements). I dropped the agent's suggested Haarlemmermeer sycamore best_time (private front garden, season kept scarce). Claim released, preflight 0 problems. The 59 READY leads were not written: recovery mode allows no new tree unless its page is rich. The next enrichment batch (gliniak and nine others) was refused at claim because Poland, Bulgaria and Lithuania are outside the focus countries, so it was left alone.

## 2026-10-14 14:50 run: reader photos judged, one enrichment pass

Visits, 7 days: 1569 visits, 2266 page views. Rung 1: two app photographs were waiting, both ours. The Cantonspark redwood one is a laptop, rejected (wrong subject). The Noike cedars one is a good cedar by the torii, held because it is ours and the tree already has an approved photo. Rung 4: munich refused (62 of 60 trees), so I took enrichment instead: lulin+maebashi+martinique+maxaranguape+mendaza+millena+moffat+mrakotin+msecke-zehrovice. Six trees got facts: two Maebashi national monument records with girth, Lulin, Mendaza, Mrakotin and Msecke Zehrovice measurements, AOPK ids for the Czech two. The other four had no usable source and 13 gaps are dead-ended. Preflight 0 problems. No refused commands.

Second pass: muxika+myjava+newtown+nicorps+nihonmatsu+nisia-floresta+nyingchi+ofunato+okuizumo. Ten trees got records or measurements (Nihonmatsu's two national monuments, Myjava, Nicorps, Takezaki, Brimmon, Urkieta, Nisia Floresta, Ofunato, Nyingchi); 9 gaps dead-ended. The Nicorps churchyard location_site was refused by enrich.py (no source URL), so that pin stays open. Preflight 0 problems.

Third pass: ondategi+ora+oyodo+parry-kauri-park+peruc+pianello+pirangi+pisz-forest+plauginiai-forest. Eight trees improved: Plauginiai's two oaks, both Parry Kauri Park kauris (NZ Tree Register records), Peruc, the Perkun Oak, the Oyodo zelkova (with access) and the Ora osmanthus (September to October flowers best_time). Ondategi, Pianello and Pirangi found nothing citable; 8 gaps dead-ended. Preflight 0 problems.

Fourth pass: port-renfrew+portalegre+prety+ramsau-bei-berchtesgaden+rannee+reyersviller+runa+s-gravenvoeren+sachsenbrunn. Eight trees improved: Big Lonely Doug and Red Creek Fir measured, the Portalegre plane, the Hindenburglinde and Sachsenbrunn Tanzlinde (both with a June to July flowers best_time), Rannée's heritage record, Reyersviller girth, and the 's-Gravenvoeren chestnut (Flemish register plus a 25 m location_site). Préty and Runa gave nothing; 11 gaps dead-ended. Rannée's record lists the oak's ground as private; its access line is not yet checked against that. Preflight 0 problems.

Fifth pass: santa-maria-del-tule+schlagsdorf+schlettau+seja+sliven+soreze+sremski-karlovci+st-georgen-im-attergau+stoutenburg+suzuka. Four trees improved (Tule churchyard entry price and hours, Sēja oak, Sorèze beech and St. Georgen lime measurements); six had no citable source and 19 gaps are dead-ended. The Tule price comes from a news report, not an official page. Preflight 0 problems.

Sixth pass: tata+telgte+toba+tombeboeuf+trollskogen+tullamore+ueki+urvaste+vainiai+valentin-tineo. Seven trees improved with a record link or girth and height (Tata, Toba, Ueki, Vainiai, Valentin, Tullamore, Urvaste). Telgte and Trollskogen had no citable source. The agent did not research Tombeboeuf, yet `--apply` dead-ended its gaps for 90 days: a retry of Tombeboeuf (pin, register) is worth a look before then. 15 gaps dead-ended. Preflight 0 problems.

Eighth pass: xhoris+yvignac-la-tour+zaanstad+zadeikoniai+zaragoza+zarzecze+zywiec+aachen. Four trees improved: the Xhoris lime (Wallonia heritage inventory record), the Yvignac yew (girth and a 40 m churchyard location_site; its "Arbre remarquable" register link is only the commune's page), the Žadeikoniai oak (Lithuanian cadastre id, measurements quoted from pasvalia.lt), and Aachen's Forster Linde (city Naturdenkmal page, base girth left out). Zywiec, Zarzecze and the Zuiddijk beech found nothing; 10 gaps dead-ended. That is the end of the unproven-city enrich list for now. Preflight 0 problems.

Ninth pass (the list wrapped back to A): aberford+aga+aguas-de-moura+albersdorf+allouville-bellefosse+amt-neuhaus+antwerp+aosta+arita+asago. Four trees improved: Agas Shogun Sugi (national monument record, girth and height), the Albersdorf Fünffingerlinde (county Naturdenkmal list entry, girth from baumkunde.de, a community register), the Amt Neuhaus oak girth, the Arita ginkgo record (no measurement: only old shaku units). Six found nothing; 7 gaps dead-ended. Preflight 0 problems.

Tenth pass: atami+aubers+bad-staffelstein+baldenhain+bansko+bargischow+bedomin+boetersheim+bohunovice+bonnerue. Four trees improved: Bohunovice (AOPK record, 2004 measurements), Bargischow (DDG Champion Trees record, measured May 2025), and girths from Wikipedia for Bad Staffelstein and Bonnerue (thinner sourcing). Six searched without result; 8 gaps dead-ended. The remaining enrich gaps are mostly single season or access gaps in small cities, so the yield per pass is now about four trees for 55 to 85k tokens. Preflight 0 problems.

Eleventh pass: bracon+braga+braziukai+brielow+calvos+canicosa-de-la-sierra+casta+chapel-hill-north-carolina+chishang+cieletniki. Five trees got girth and height (Braziūkai, Brielow, Časta with its protected-tree id S 456 from sk.wikipedia, Cielętniki, Canicosa); the Časta register page itself was not opened. Bracon, Chapel Hill and Chishang found nothing; 9 gaps dead-ended. Preflight 0 problems.

Twelfth pass: columbia-missouri+concoret+cooper-creek+coos-bay+coromandel-forest-park+crecy-en-ponthieu+debina+den-hout+drnava+dubinne. Seven trees improved: Columbia (Missouri Dept of Conservation girth and height), Concoret, Coos Bay (height from a 2022 Native Tree Society measurement, and the access line now says the trail was closed by wildfire per the BLM page), Dębina (CRFOP id from pl.wikipedia), Den Hout (register id 1680745 taken from nl.wikipedia's link, whose title says "Heilige Eik van Oosterhout": worth a glance), Drnava, Dubinné (girth and height from a TASR article; its age disagrees with the village page, 500 vs 800 years). Cooper Creek, Coromandel and Crécy found nothing; 8 gaps dead-ended. Preflight 0 problems.

Thirteenth pass: effeltrich+eichigt+eisolzried+estry+fara-in-sabina+felsomocsolad+feternes+fontaine-belfort+fortingall+frankenthal-sachsen. Only two register entries: Eisolzried (Naturdenkmal 174.113-05, number read on de.wikipedia) and the Fontaine Turenne lime (Site classé SC_90_001, 1911; the id came from search text because the DREAL PDF could not be read, and fr.wikipedia confirms the 1911 listing, so check the id if it matters). Eight trees found nothing; 8 gaps dead-ended. Yield is down to two trees for 58k tokens. Preflight 0 problems.

Photo pass (photo_hunt --recheck, then a viewing pass on 30 trees, 190k tokens): 14 photographs approved (kun_010, pky_001, pky_002, chc_002, koz_001, mna_001, vni_003, vni_001, mko_001, kzk_001, gos_002, zil_001, zil_003, gen_015), 4 held, 36 rejected. The held ones: chc_001 (forked trunk, the story describes a corkscrew) and lux_005 (photos predate the February 2026 felling of the larger sequoia, so which trunk survives is unclear). Trunk was settled by a geotag at our pin or by a sign or plaque in the frame, listed in the agent's notes. Reversal for any approval: `python3 scripts/photo_apply.py hold <tree_id>`. Preflight 0 problems.

Second photo pass (205k tokens, 30 trees, mostly Japan, Germany, Spain and register-backed EU): 19 approved (zwi_001, lec_001, unn_001, ynh_001, yab_004, yos_001, tob_001, fjk_003, tga_001, stu_002, grk_001, hag_020, tor_009, tku_001, cst_001, szb_012, grz_012, wro_005, brq_005), 2 held (iga_001, a twin-stemmed tree that does not look like the recorded girth; frb_001, a panorama where Waldtraut cannot be told from its neighbours), 32 rejected. Of the 19, 12 are in focus countries. stu_002 has no geotag; its filename names the Hutteneiche. zwi_001 is only 740 px wide, soft as a hero. Fault worth fixing: `photo_apply.py` could not read image sizes for ten approvals (the size marker sits past the 400 KB it reads), so the pass filled them with `photo_res.py`; every approved block has width and height now, but the next approval with a large EXIF header will hit it again. Image reads hit request limits for a stretch, so about 17 downloaded files were never judged and stay in the queue. Preflight 0 problems.

Seventh pass: vales+vassununga+veryn+viljandi+vir+visnova+waipoua-forest+wojslawice+wuppertal. Four trees improved: Tāne Mahuta and Te Matua Ngahere (NZ Tree Register records, 2002 laser girth and height), the Wojsławice beech (girth and height from the city of Wrocław), the Viljandi oak access line. I dropped the agent's chestnut-season best_time for Vales, since no source ties that tree to the harvest. Wuppertal, Vír, Višňová, Veryn and Vassununga were researched with no citable record; 15 gaps dead-ended. Preflight 0 problems.

## 2026-10-14 session: the digest leaves our own Google searches out

Nothing changed in the product. The follow-up below is done: the daily digest now takes `site:` searches and operator searches (a query starting with + or %, or carrying +"...", also inurl:/intitle:) out of every per-page Google number before anything reads them. The rule lives once in `own_search()` in scripts/ours.py; `drop_own_searches()` in scripts/daily_digest.py subtracts those page x query rows at fetch time, so "Depth is allowed", "Google, from the new floor", "Is enriching working", the top queries and pages, and the city queue (promote) all read the cleaned numbers. A stranger's `-site:reddit.com` stays theirs; anonymised impressions stay. The Google table now says how many impressions were left out. `daily_digest.py --selftest` covers the Prague shape and runs in data-digest.yml before the entry is written. Not covered: the day-by-day totals (no query split per day) and the previous window in the paused trend section. Next digest: Prague stays under Depth-allowed only if readers, not we, give it 10+ impressions.

## 2026-10-14 session: Prague's Google numbers are mostly ours

Nothing changed in the product. The digest showed /prague at 294 impressions, position 5.6, 0 clicks, which looked like the one city Google still shows. `seo_diagnose.py` now takes `SC_PATH` (workflow input `path`) for one place close up; run for /prague (28 days):
- The biggest query is `site:ancienttrees.app prague` (19 impressions on each of 8 pages): someone checking our index, not a reader. The rest are operator searches (`+"oldest" "pear" "on record" "park"`), which is what a research agent types.
- 117 of the impressions are Dutch mobile, 60 Japanese mobile, 33 US desktop. Hidde's phone, from home and from Japan, fits that exactly.
- So Prague is not escaping the demotion; it is the city we look at ourselves. The 8 real clicks to /prague came before 09-28. The Google floor across the site is the true reading.
- Follow-up, not done: the digest should drop `site:` and operator queries (and their impressions) before any city reaches "Depth is allowed" or "proven" on Google's word.

## 2026-10-14 session: the iOS 18 floor is green again

- Fixed: the scheduled iOS app check failed twice on 10-13 on the iOS 18 iPhone SE (FlowWalk could not find Follow in Find people; on the earlier run SignedOutWalk got no sign-in sheet). Cause: screens that tests open with a launch argument (Find people, Contribute, Feedback, Edit profile, Sign out, Species) asked iOS for their sheet on the very first frame, and a busy machine drops that request silently. Reproduced on the Mac under CPU load (failed on try 13 of 40); now raised once the screen is up and asked again if dropped (Kit/LaunchSheet.swift): 40 of 40 under the same load. No effect for readers: these arguments exist only for tests and screenshots.
- SignedOutWalk.testSeenTickAsks (failed on this Mac) opens the map sheet directly instead of tapping a spot that on the SE lands between the count and the first card.
- The floor job now keeps its own test results (they were overwritten before upload, so a red run had no screenshot), and a dispatch can rerun named tests on iOS 18 alone in ~25 minutes: `gh workflow run ios.yml -f floor_only=AncientTreesUITests/FlowWalk`.
- Verified: dispatched run 38541980903, all three jobs green (iOS 18: 223 passed, 0 failed). The brief's "keeps failing on its schedule" clears after the next scheduled run (17:00 UTC) passes.
- Open: NameTests.testNoAnswerFromTheServerAsksNobody crashed once on this Mac (malloc "pointer being freed was not allocated" in the host app); CI has not seen it.

## 2026-10-14 session: the About page has a maker

**Live:** /about opens with Hidde's own story (Lisbon, the Palermo ficus, "not an expert, but a fan"), his photo at a Japanese cedar beside it (above it on a phone, EXIF stripped) and info@ancienttrees.app, written by him. The four process sections were cut; one sentence on sources and AI remains. The menu's "Sponsor this project" became "About"; a sponsor button now sits under his story, and Sponsor stays in the footer. Seen live at 375px and desktop, menu open. Blueprint v1.26, DECISIONS.md 2026-10-14; qa allows the first name on /about only.

**Inbox:** six replies drafted in drafts/batches/replies-2026-10-14.json (status draft, waiting for his word): Bauer (Koeln) is held for a careful reply now the About page exists; Jeanne (Helmond), Groeger (Munich), Kerry (Brighton), Pere Fraga (Menorca), Jon Pattee (optional). The Unterlappach lime lead got its baumkunde source.

## 2026-10-14 session: the collect flow, from Hidde's test

- Saving a tree you added: a confirmation sheet ("Added to your trees", its name, Done) before the page; was a 1.5 s HUD he never saw.
- Camera near our trees: always "Which one is it?" now, no silent match (parks have several trees inside 80 m). Only a camera opened from a tree page claims directly.
- "Which one is it?": "Add a new tree" (under it "It is none of these") replaces "None of these"; recognition lines cut to two lines, full line behind the compare button.
- "You found": no footnote, milestone line centred, "I am not sure it was this one" removed (you picked the tree a tap before).
- The near-a-tree banner hides while a sheet is open.
- All in the simulator; FlowWalk updated. Not yet on his phone.

## 2026-10-14 night run, 09:13 window

- Visits last 7 days: 1,350. Rung 1 empty, rung 2 clear (health.py), so rung 4 enrichment.
- Enrichment of Indianapolis, Iwata, Jachymov, Jerceni, Jihlava, Kasukabe, Kawago, Kawatana, Kawazu (10 trees): register records for Jachymov, Jihlava, Kasukabe, Kawago, Kawatana, Kawazu, Kitahama; girth and height for eight; Iwata wisteria (April) and Jihlava copper beech (autumn) best_time. Open: Indianapolis and Jerceni register, Kasukabe pin. Preflight 0 problems.
- Second batch (Kimotsuki, Knappfors, Koenigslutter, Komjatice, Kopcany, Kozaki, Lecina, Les Clayes-sous-Bois, Letenye, Liernu): Kimotsuki and Kozaki got national natural monument records, Lecina its Aragon singular-tree sheet, all three with measurements. The other seven stay open (only Wikipedia, press or Tree of the Year figures, withheld); 17 gaps dead-ended. Preflight 0 problems.

## 2026-10-14 session: digest top is readers only

- Live: the daily digest opens with the trees readers gave, each linked to its page when live. The night run's photo approvals moved lower, to their own table, with their overrule commands. Our own rows and the lines that counted our testing are gone from the digest. Today's entry was rewritten that way.
- Found: a reader (10-13) says iOS location cannot be turned on in Settings. Cause: the app only asks when the "Location off" chip or the recentre button is tapped, so until then iPhone Settings shows no Location row.
- On main for the next app drop: the app asks for location on the first open (map first, then iOS's own question), the chip stays while it is off, and Profile > Preferences > Location (On/Off) asks or opens Settings. LocationAskWalk guards it; the full suite on the iOS 18 SE passed apart from three tests that also fail without this change (search and Undo were flaky and passed on rerun; SignedOutWalk.testSeenTickAsks fails locally on main too). The reader got a reply with today's workaround (row 405).
- The digest now costs far fewer tokens: sessions show it as a page (scripts/show_digest.py), the frozen roster is one line, and the photo overrule is `photo_apply.py hold <id>`. That overrule never worked for most night-run approvals (upload url vs the queue's Commons page url); it matches by file name now, 30 of 30.
- Not fixed: FlowWalk's find-people flow fails only on GitHub's iOS 18 runner and passes locally; the floor job saves no xcresult to look at.

## 2026-10-14 night run, 03:09 window

- Visits last 7 days: 1,495. Rung 1 empty; rung 2 unchanged (iOS scheduled failure needs a simulator; smoke "skipped" is the push-trigger default).
- Setúbal enrichment: the two-tree pages (Largo Marquês de Pombal grevilleas, Bocage school poplars) got their ICNF register ids (KNJ1/519 and 520, KNJ1/526 and 527); no measurement set because each page covers a pair with different heights; four season gaps dead-ended. Preflight 0 problems.

- Fujikawaguchiko, Giessen, Hokuto: 11 trees got register records and measurements (Yamanashi prefecture and Minobu town pages for the cedar, ginkgos and two Hokuto trees; Gießen's Naturdenkmal list via a 2016 archive copy, dated in the register name). Shinden cherry access rewritten from the tourism association page. The Negoya zelkova site was refused by apply (no source URL), so that pin stays open. 5 gaps dead-ended. Preflight 0 problems.

- Hōraiji, Jalhay, Plungė, Priekulė: 8 trees enriched. Aichi big-tree pages gave girth and height for the Kasa sugi and Nezu no Ki (their coordinates sit 360 to 470 m from our pins, over the 300 m limit, so not taken); Les Sept Frères got its 2012 classification decree (press circumferences left out); four Lithuanian trees got saugoma.lt records; Simonaitytė's beech got museum hours and prices plus an October to November colour season. 10 gaps dead-ended. Preflight 0 problems.

- Rouen, São Paulo, Tamba, Wrocław: four Wielka Wyspa oaks got newer girth and height (przyrodniczo.pl survey; the older register figure stays in measure_source, 1.30 m assumed), the Kashiwara zelkova got its city page and height. **Published error fixed:** São Paulo listed the Figueira das Lágrimas twice (spa_001 and fdl_001, the latter pinned 3 km from the tree); fdl_001 is retired to leads with a redirect, the city now has one tree and its intro already said so. 15 gaps dead-ended. Preflight 0 problems.

- Žilina, Český Krumlov, Chikubushima, Dengfeng, Fort Lauderdale: 12 trees enriched. Žilina's lindens and maple got their Slovak register ids (S 187, S 188; figures via sk.wikipedia because the register pages need JavaScript; the maple's register names it sugar maple but gives the Latin for silver maple, open). Two Krumlov lindens got a June flowering season and the monastery garden its ticket prices and October tour days. Four Fort Lauderdale trees got their Florida Champion Tree Register ids. Dengfeng had only a news article, nothing taken. 9 gaps dead-ended. Preflight 0 problems.

- Ghisonaccia, Gonzales, Heerlen, Hilversum: 6 trees enriched. The two Ghisonaccia cork oaks got their Arbres Remarquables label ids (1420, 84). **Published access corrected:** the Arburacellu's label record lists the ground as private, so its access line now says to look from the lane instead of "no gate". Sam Houston Oak access says private, viewed from CR 361. Heerlen lime got a June to July flowering season; Hilversum's two 1937 trees a 30 m site. The Terworm ginkgo (hee_008) is "Afgekeurd" (rejected) in the Dutch register, no measurement taken, left published but unconfirmed. 9 gaps dead-ended. Preflight 0 problems.

- Kaunas, Koriyama, Krka, Morioka, Pesselières, Rhenen: 5 trees enriched. Akatsu katsura, Ishiwari cherry and the Ryūgen-ji katsura got their Bunka-chō national monument records (katsura girth 930 cm, height 25 m); Ishiwari got court hours and an April blossom season; Krka mulberry girth 475 cm and park hours; Achterberg lime its Dutch register entry (604 cm, 10 m). **Published access corrected:** the Akatsu katsura line said "rural road/trail"; it is 8 km up a mountain track, about 50 minutes by car from Koriyama South IC. Kaunas oaks, Sully lime and Koningstafel oaks found nothing usable (17 gaps dead-ended). Preflight 0 problems.

- Siquijor, Stratfield Saye, Veliki Preslav, Villeneuve, Achnacarry, Alishan: 4 trees enriched. The two Alishan giants got the scenic area authority's pages (45 m tall; girth computed from the stated 4 to 4.1 m diameter, labelled fused multi-stem); **Sianglin's pin corrected** by 285 m to the authority's coordinate. Veliki Preslav mulberry got a 40 m square site, Siquijor's balete a 4 m iNaturalist pin. The agent's Achnacarry answer (Woodland Trust Ancient Tree Inventory record) was dropped on the data rule; separately, the Achnacarry pin (Tree of the Year GPS) and Wikipedia's coordinate sit about 1.8 km apart and need a session to settle. Alishan's Sianglin age (authority now says 626 years for the main stem) not yet compared with our page. 17 gaps dead-ended. Preflight 0 problems.

- Bristlecone Pine Forest, Berga-Elster, Breukelen, Brunswick (Georgia), Brzoza, Busan: 6 trees enriched. **Published access corrected:** the Patriarch Grove line now carries the Forest Service fee ($3 per person, $6 per car) and the usual mid-May to September season. Nijenrode limes got their Dutch register number and height. The three Brzoza trees got Polish register ids with girths and heights taken from Wikidata statements that cite the register (the register host returns 403, so these are not read from the register itself; worth a recheck if the host opens). Busan's crape myrtles got their Heritage Service record. Berga oak, Lover's Oak and the Suyeong pine found nothing usable. crfop.gdos.gov.pl and brunswickga.org added to the fetch blocklist (403, refuse fast). 12 gaps dead-ended. Preflight 0 problems.

- Canberra, Dęblin, Fonte Colombo, Fontenay Abbey, Fortaleza, Fribourg: 4 trees enriched. Fontenay's access line now carries the abbey's own 2025 tariff (11.50 EUR) and opening hours; Fortaleza's baobab got the 1951 federal decree protecting it as its register record; Canberra pine (20 m) and Dęblin oak (28 m) got heights. Fribourg: a descendant of the Morat linden was planted in spring 2026 about 100 m from the old site (Route des Alpes junction); our page describes the 1984 tree at the Place de l'Hôtel-de-Ville, which watson says is still there, so it stands as written. If we ever add the 2026 tree it is a separate point. 15 gaps dead-ended. Preflight 0 problems.

- Guaíba, Guernica, Haarlemmermeer, Iida, Innimond, Jericoacoara: 5 trees enriched, plus a published fact fixed. **Species corrected:** the Badhoevedorp roadside tree (hrl_010) was published as "Maple (Acer sp.)" with a story asking readers to name it; the Dutch register record (read live) says Gewone esdoorn, Acer pseudoplatanus, so it is now a sycamore and the story says so. Iida's two cherries got their city natural-monument pages (Yasutomi: Nagano prefectural monument 1967, girth about 5.4 m, height about 20 m); Innimond lime girth 580 cm (association blog, not an authority); Guaíba's cypress a square as site. Guernica and Jericoacoara found nothing. plainedelain-tourisme.com added to the fetch blocklist (403). 12 gaps dead-ended. Preflight 0 problems.

- Kozy, Le Guerno, Lebec, Longlou, Lozorno, Luís Correia: 3 trees enriched. **Published access corrected:** the Lebec oak line said "open daily 9am-4pm"; the State Parks page says the grounds are sunrise to sunset, $6 per vehicle, visitor center Tuesday to Saturday 9 to 4. Longlou's beeches got their Walloon heritage code (from the Wikipedia list row; the record itself did not load) and an access line that no longer says "open at all times" inside a nature reserve; its story already says the old trees are near the end and young ones were planted in 1993. Lozorno's pin is now sourced to the Tree of the Year GPS. Kozy, Le Guerno, Luís Correia: only a photo site, press figures or nothing, so nothing taken. 16 gaps dead-ended. Preflight 0 problems.

- Lukavice, Mâcon, Malacky, Maria Aurora, Martinsville, Mélykút: 5 trees enriched, plus a species fixed. **Species corrected:** the Lukavice oak (Czech Tree of the Year 2024) was "Oak (Quercus sp.)" with a story asking readers which oak; the nature conservation register record (DRUSOP 101608) says dub letní, the pedunculate oak, with girth 710 cm and height 31 m, so species and the story's last line now say so. Zámrsk lime got its group record (no measurement), Mâcon lime its Walloon exceptional-heritage code (from the French Wikipedia reference, the record page does not render) and a June flowering season, Malacky oak girth 660 cm and height 20 m (Ekopolis), Mélykút's Judas tree the church hill as a 50 m site. Open for a session: the Maria Aurora access line cites an APECO page that returns 404 and its entry fee is unconfirmed; Lukavice has a second protected oak (DRUSOP 101601) that may be a separate tree worth a lead; Martinsville's Devil's Tree park ownership is conflicted (Somerset County park in Bridgewater vs Bernards Township). 12 gaps dead-ended. Preflight 0 problems.

- Neuenrade, Oberndorf bei Salzburg, Princeton, Ramsau am Dachstein, Raudonė, Římov: 3 trees enriched. Neuenrade's lime got its Märkischer Kreis Naturdenkmal number, a June flowering season and girth 620 cm / height 18 m (Baumkunde.de, measured 2021, a finding aid repeated by the Wikipedia list, so worth a second look if an authority page appears); Raudonė's lime its state register page; Římov's lime its Czech register number, the church grounds as a 50 m site and a June season. Open: the Ramsau Feistererhof maple is not the register's "Naturdenkmal Ahornbaum" (that stands at Hotel Pehab-Kirchenwirt), so no record attached; the Mercer Oak in Princeton is a successor grown from a 1981 acorn and planted around 2000, close to "a young tree is not ancient". 11 gaps dead-ended. Preflight 0 problems.

- Rudy, Sankt Vith, Shokawa, Solingen, Uda, Veľké Borové: 7 trees enriched. St. Vith's Antoniusbaum got its Ostbelgien heritage record (ID 31049, about 20 m, read through an archive copy; it is a protected-landscape entry with no species); Shokawa's cherry and the Mumaya pines their Takayama city natural-monument list entries (pine girth withheld: one figure for a trio); Solingen's Kaiserlinde Naturdenkmal 51; Uda's two cherries height and girth from the tourism association (no designation named for Matabei); Veľké Borové pine girth 460 cm from sk.wikipedia's Strom roka table. Open: Shokawa-zakura may be two trees (Korin-ji 5.94 m, Shoren-ji 4.85 m) described as one; Rudy oaks and Yatsufusa cedar need a session. Push credential expired at 04:10, commits are local for Run health to push. 12 gaps dead-ended. Preflight 0 problems.

- Waremme, Weywertz, Wrexham, Wye Mills, Zehdenick, Aberford: 6 trees enriched. The Waremme and Weywertz limes got Walloon remarkable-tree records with girth and height (Waremme's match to the register rests on position and species, 19 m away: an inference); Wrexham's oak a 24 m height (the council's 6.1 m circumference is not stated at 1.3 m, so no girth); Zehdenick's tree its Naturdenkmal number ND 228; Wye Oak State Park its hours. **Published access corrected:** Aberford's "publicly accessible woodland" said too much, the Parlington Estate is commercially owned and out of bounds off its rights of way, and the line now says so and that we have not confirmed the tree is on the path. Open: Weywertz's register point is 137 m from our approximate pin (refused for a missing source URL; species there is Tilia cordata, ours says Tilia sp.); Waremme's register says Tilia platyphyllos; Waremme's address number 6 not checked. 12 gaps dead-ended. Preflight 0 problems.

- Aizuwakamatsu, Argoules, Athens (Georgia), Azeitão, Bad Blumau, Bátaszék: 3 trees enriched. The Takase zelkova got its city cultural-property page with girth 10.45 m at eye level and height 24.64 m (the prefecture page's 12.5 m is a lower-trunk figure, not used). The Azeitão olives are three registered trees (ICNF KNJ1/152 to 154, classified 29 October 1959), not the unregistered trio the page hedged about; one story sentence now says so, the 1996 council claim stays hedged. Bad Blumau's oak got a daily-access line and 30 m height. Open: the Aizuwakamatsu zelkova's age (city page says about 500 years, prefecture about 1,000) and Bad Blumau's (register 500 to 600 against "1000-year-old") should be checked against what those pages state. 10 gaps dead-ended. Preflight 0 problems.

- Bioul, Bojnice, Borculo, Bulat-Pestivien, Cabeza del Buey, Căjvana: 4 trees enriched, plus a wrong pin fixed. **Pin corrected:** the Căjvana oak (Tree of the Year 2018, "confirmed") was pinned 1.4 km east of the tree; the ro.wikipedia coordinate (47.70195, 25.96787, read live) and a Commons geotag put it in the town centre, so the pin moved and records a correction in pin_source. The oak also got girth 11.01 m at 1.30 m and height 20.1 m (the 2011 radiocarbon study as quoted on ro.wikipedia; heights elsewhere say 22 to 23 m) and an access line from strada Principală 864. Borculo's elm access now says it is seen from the street on a private estate; Bulat-Pestivien's pin has a Wikidata source; Cabeza del Buey's elm grove got the Junta's Singular Trees page (a page about the group). Bioul and Bojnice found nothing. 9 gaps dead-ended. Preflight 0 problems.
- Căpeni, Česká Lípa, Châtenay-Malabry, Cheile Cibinului, Chiapa de Corzo, Chirk: 2 trees enriched (cedar height 14 m; copper beech small-park site), the rest dead-ended (11 gaps). Open: Česká Lípa's source note says designated 2010-10-15 while cs.wikipedia says added 16 February 2006 (AOPK 104688); Căpeni county (Covasna vs Harghita) not checked; La Pochota's 8 July 1993 declaratoria could go in verify_notes.
- Cínovec, Colindres, Collm, Cooper Creek, Coppenbrügge, Curinga: 2 trees enriched. The Collm lime got girth 11.05 m at 1.30 m (October 2022). **Published access corrected:** the Dig Tree line said "around AU$11"; the site's October 2025 report says $20 per vehicle, valid six months; it also got height 12 m and its Queensland Heritage Register number 601073 (the register's per-tree URL now redirects to its home page). The Curinga register code the agent offered was read from a search summary and an unreadable scan, so it was not applied. Cínovec is a 2007 sapling of a lost original, honest on its page but young for this site; Hidde's call whether it stays. 10 gaps dead-ended. Preflight 0 problems.
- Daruvar, Dunkeld, Eraul, Erdmannrode, Farnham, Ferrara: 3 trees enriched. Daruvar's ginkgo got the county protected-areas authority's page (park-architecture monument, 1967) and the palace entrance as a 40 m site; Eraul's holm oak the Navarra MN1 sheet (read through an archive copy) with height 10.2 m and a girth of 471 cm derived from the stated 1.5 m diameter at 1.3 m, labelled as derived; Erdmannrode's linden Hessen Naturdenkmal 3632900 and a June season. Dunkeld and Farnham: the only measurements are Woodland Trust data, not used. Open: Eraul's confirmed pin may be about 265 m off the register's UTM point (the Basque Wikipedia says 500 m east of the village on the Abartzuza track); a session should check. 7 gaps dead-ended. Preflight 0 problems.
- Fish Lake, Flinders Ranges, Frýdlant, Garmen, Gifu, Groton: 4 trees enriched. The Cazneaux Tree got its National Trust of South Australia register number 239 and height 29 m (both from en.wikipedia; the Trust's page was not reached; the 11.4 m girth is a base figure, left out); Frýdlant's beech its Czech register id 101922 with girth 422 cm and height 27 m (cs.wikipedia and Wikidata; the measuring height is not stated, the Czech convention is 1.3 m); Zagradski plane height 24 m; Gifu cherry height 9 m. Pando and the Groton mulberry found nothing. 9 gaps dead-ended. Preflight 0 problems.
- Gümeli, Hampton, Heede, Henryków Lubański, Herchies, Higashiagatsuma: 2 trees enriched. Heede's lime got Naturdenkmal ND EL 00024 (from the de.wikipedia list), girth 17.5 m at 1.30 m (nationalerbe-baeume.de, December 2018; de.wikipedia says 15.39 m, so the sources conflict) and a June flowering season; Higashiagatsuma's tree its national natural monument record (1933; the register's 14 m 1933 girth and Wikipedia's 9.10 m disagree, so none recorded). Open: Gümeli's age (media 4,112 years, a 2017 dendrochronology study 1,950 to 2,000) should be checked against the story; Henryków's yew is on a private farmstead behind an electric fence, so its "free, view-only" line needs a look against the viewing-place rule. 9 gaps dead-ended. Preflight 0 problems.
- Higashimiyoshi, Hilvarenbeek, Himi, Hochneukirchen-Gschaidt, Hronsek, Ichinohe: 7 trees enriched. The Great Camphor of Kamo got its Special Natural Monument record with girth 16.72 m at 1.30 m and height 26 m (town page, measured 2007; the register's own 12 m is at 1.5 m); the Black Kate witch tree its Dutch register number 1678572 (from the nl.wikipedia citation, the Bomenstichting page 404s) and an October to November colour season; Himi's two trees, Hochneukirchen's lime (WB-032, from the de.wikipedia list row), Ichinohe's two trees got records, heights or seasons. Hronsek found nothing. 4 gaps dead-ended. Preflight 0 problems.
- **Window summary (03:09 to about 04:50):** nine enrichment passes, about 60 trees given register records, measurements, access facts or pins. Published errors fixed on the way: São Paulo's Figueira das Lágrimas was listed twice (one retired to leads); Căjvana pin 1.4 km off; Sianglin pin 285 m off; species were wrong or unknown on the Badhoevedorp tree (now sycamore) and the Lukavice oak (now pedunculate oak); access was overstated at Lebec, Aberford, Akatsu katsura, Arburacellu, Patriarch Grove and Longlou. An agent answer built on Woodland Trust Ancient Tree Inventory data (Achnacarry) was dropped. Push credential expired at 04:10; commits from then are local for Run health to push. Needs a session: Achnacarry pin (Tree of the Year GPS and Wikipedia's coordinate 1.8 km apart), Shokawa-zakura possibly two trees, Weywertz pin (register point 137 m off), Ramsau maple (not the register's Naturdenkmal), Fribourg's 2026 descendant tree.

## 2026-10-14 night run, 00:24 window

- Visits last 7 days: 1,491. Rung 1 empty. Rung 2: iOS scheduled run failed on one test, `testEveryFlowLeavesAWayBack` (tap on "person-follow" button found no match); needs a simulator session, not fixable from this runner. Smoke "skipped" is the push-trigger default.
- Enrichment: Bošáca had no register record or authority measurement for its three trees (6 gaps dead-ended). Malsfeld got LAGIS register links on three lindens (Berndshausen, Dagobertshausen, Ostheim); LAGIS is a historical court-site database, not a tree-protection register. Preflight 0 problems.
- Münsterland: Asbeck lime height 18 m (Legden municipal page), Krüsellinde register id I. A 1 (taken from the de.wikipedia list of the Kreis Steinfurt ordinance, not the image-only PDF); a proposed Heidenbaum flower season was dropped as unsourced for that tree; 5 gaps dead-ended.
- Rothenburg ob der Tauber: no authority record or measurement for the four trees (only community-register figures); 6 gaps dead-ended.

