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

## 2026-11-10 session: build 42's map sheet, the Airbnb way, on main (PR 40)

- **What changed in the product:** the map's list, as Hidde decided on 11-08. At full height it is the page: no grip, no empty count strip, the list starts right under the search field (the sheet now covers the map behind the field too), and the floating Map pill is the way back. The pill drops the list to a new lowest stop where only the count bar stays ("22 trees") and the tab bar hides, so the map has the screen; a tap or a swipe on the bar brings both back. The opening peek (count plus the top of the first photo, his 08-22 ruling) is unchanged, so the tab bar is there at launch. Every city and country map is the map tab, so they follow; My trees keeps its stops. /explore on a phone drops the same strip (sheet reaches the bar, grip and count go) and gains the Map pill in all eight languages (UIStrings.mapPill). CONVENTIONS.md "A results list over a map, Airbnb's way".
- **Checked:** appfit 0 findings on 156 screens across 4 phones (iOS 18.6 and 26.5); FlowWalk (with a new map-pill-and-back flow) and the sheet tests green on the SE and the 17 Pro; ButtonWalk, SweepFrames and appsweep gained map-bar; /explore checked at 375 with the new CSS on the live page, the site built in CI.
- **For Hidde:** build 42 is not archived or uploaded; `scripts/release.py` when you want it in TestFlight, then judge the sheet on your phone. Android takes it from the Swift (data/android-parity.json: map, map-full, new map-bar).

## 2026-11-10 Android: Continue with Apple

- Android's sign-in sheet now has the iPhone's dark "Continue with Apple" pill, first, Apple's logo at the leading edge (the website's own paths), then Google and email, 10 apart, in all eight languages (the website's words). Checked on the emulator: the sheet matches the iPhone's.
- Route: Supabase's ordinary Apple OAuth redirect, the website's route, opened in a Custom Tab (androidx.browser, Android's own in-app browser, the iPhone's ASWebAuthenticationSession), back on ancienttrees://auth-callback. Google moved into the same Custom Tab. So an account made with Apple on an iPhone opens on Android: the web Services ID is grouped with the app, so Apple gives the same account id.
- Configuration checked, nothing for Hidde: `authorize?provider=apple&redirect_to=ancienttrees://auth-callback` answers 302 to appleid.apple.com (Services ID app.ancienttrees.web), and ancienttrees://auth-callback is already on the redirect allow-list (the iPhone's Google route uses it).
- Not tested end to end: that needs a real Apple ID in the Custom Tab, and the emulator's Chrome stopped at its first-run screen. The tap opening Chrome on Supabase's URL is checked. First real check: Hidde's own Apple account on an Android phone.
- A first Apple sign-in on Android gets a generated profile name, as the website's redirect fallback does (the redirect carries no name); Edit profile changes it.
- data/android-parity.json: Apple is off the forced list; the "Sign in" entry now names only the real difference (a Custom Tab instead of Apple's own sheet).

## 2026-11-10 daily publish (scheduled task): 25 trees into the app

- **What went on main (490dc095d), app only under APP FIRST, no web page or place page:** Cleveland 5, Ann Arbor 3, Lansing 2, Sacramento 2, Santa Cruz 2 (build_source_led_2026_11_09.py), ten churchyard yews in Surrey, Sussex and Hampshire, one place each (Crowhurst, Tandridge, Wilmington, Corhampton, Stedham, Dunsfold, Charlwood, Coldwaltham, Tangmere, Itchen Abbas), and the Eastham Yew as Liverpool's lvp_004 (build_uk_under_ten.py limited to Liverpool, out/tmp/build_uk_under_ten_liverpool.py). None has a photograph. city_names and preflight 0 problems; the 25 is this task's own limit.
- **Checked:** /liverpool 200, /cleveland 404, as APP FIRST wants (before the deploy that carries them). The 25 still need to be seen in the app feed after the next deploy.
- **Still waits, 3 trees, one more day:** build_uk_under_ten.py: the Bute Park Tulip Tree (crd_010, Cardiff) and Windsor's two (wsr_001, wsr_002, a new place). Brighton's three in that builder are live already, so run it limited to cardiff and windsor. No claims stood on today's places.

## 2026-11-10 Android type and icons (session android-type-icons)

- **Android's text now sets in Inter and its icons are Material Symbols Rounded**, the open set and face closest to the iPhone's SF Symbols and SF Pro (Hidde: "maak het zo veel hetzelfde"). Every text goes through ui/Text.kt, which adds SF's tracking per size and weight; every icon comes from ui/Symbols.kt, generated glyph for glyph by android/generate_symbols.py. Back (←), share and the overflow (⋮) take Android's form from the same set, per Airbnb's line. Tab icons, the tree page's top bar, Take me there and the action bar circles are sized to the iPhone's (SF point size times 4/3).
- Libraries: Inter 4.1 (OFL, bundled font files, subset to Latin, Greek and Cyrillic) and Material Symbols Rounded 0.48.0 (Apache 2.0, generated into Kotlin), neither touches reader data. AndroidX material-icons-extended is gone.
- A check so it cannot drift back: `python3 scripts/android_parity.py --check`, run by qa.py on every push.
- Icons left the forced-differences list in data/android-parity.json; DECISIONS.md 2026-11-10.

## 2026-11-10 Android measures what people do, like the iPhone

- Android now sends the iPhone's PostHog events to the same project with the same properties (account/Measure.kt, a port of Kit/Measure.swift): app_open, tab, tree_opened (tree, near), tree_saved, tree_visited, sync_failed, sighting_recorded, directions, share_tapped (map_card, tree, collect, your_photo, profile), location, plus-open, plus-answer, plus-tellme. `os` reads "Android 15" beside "iOS 26", so scripts/posthog.py and the digest count both phones with no change; a debug install says `build: debug` and the digest leaves it out as it does for Xcode installs.
- No PostHog SDK, on purpose: the iPhone deliberately uses none (Measure.swift: the package brings its own networking, session replay and flags we do not want), so Android sends the same one HTTP POST, the way Supa.kt talks to the server. Nothing added to the build.
- Emulators stay silent unless `-measure` is passed, the iPhone's simulator rule, so parity shots and CI walks are never counted.
- On the phone: the install id and the offline queue under the iPhone's keys (measure.install.v1, measure.queue.v1), both already ruled `device` in data/cross-device.json.
- Privacy page: "the app and iOS version" now reads "the version of the app and of your phone's system (iOS or Android)". privacycheck.py green.
- The tree page's last parity difference (tree_opened not sent) is closed in data/android-parity.json.
- Not on Android because the iPhone feature is not there yet: sync_skipped (Android cannot heart signed out; it asks to sign in first).

## 2026-11-10 Android app links: assetlinks.json

- The site now publishes `/.well-known/assetlinks.json` for `app.ancienttrees.android`, so Android can verify the manifest's `autoVerify` filter and open ancienttrees.app links in the app, as the iPhone does with apple-app-site-association.
- It carries one fingerprint today: the debug key on Hidde's Mac (~/.android/debug.keystore, SHA-256 D8:7C:...:2C:09), which signs every build installed on the emulator from this Mac. There is no upload or release key in the repo yet; CI's debug APKs are signed with a throwaway key and stay browser-only.
- **For Hidde, once:** when the first build goes to Play, Play Console > Setup > App signing shows the "App signing key certificate" SHA-256 (and the upload key's). Both get added to `sha256_cert_fingerprints` in site/public/.well-known/assetlinks.json; until then a Play-installed app opens shared links in the browser.

## 2026-11-10 night run, second attempt

- Write pass: 2 Vienna trees merged (vie_060, vie_061, app-only). 15 pending trees refused on standing holds (rule 10, no trunk named, duplicates); the 7 READY leads need a verify pass first.
- Verify pass on Sintra: one flagged tree, sin_009 (Moreton Bay fig, Cascais, approximate pin) in data/research/sintra-verified.json, not yet written (under six candidates). The Sintra claim stands until it is merged.
- Coimbra claim stands: cbr_007 is verified and unwritten.
- Housekeeping: stale duplicate entries in several research files (Cardiff, Cyprus, Tenerife, Ronda) keep `passcheck.py --pending` pointing at a held shelf.

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-11](archive/LOG-2026-11.md)
- [2026-10](archive/LOG-2026-10.md)
- [2026-09](archive/LOG-2026-09.md)
- [2026-08](archive/LOG-2026-08.md)
- [2026-07](archive/LOG-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.

## 2026-11-10 write pass: two Vienna Prater trees go into the app, everything else on the shelf is still held

- **Product:** vie_060, the Prater Meadow Oak on the Kaiserallee (Naturdenkmal 867, 4.66 m round, more than twice any oak within 45 m, confirmed pin), and vie_061, the Heustadelwasser Lime (ND 868, 2.95 m, confirmed pin, best_time July flowers), are written and merged into data/cities/vienna.json. Under APP FIRST both are app-only. Their stories hedge the inventory planting years (1841, 1913) as estimates. The lime's story says plainly that we have not confirmed a public path to the trunk, and points readers to the water's side, where the register says it is seen from afar.
- **Refused, all held by earlier passes for closed-list reasons that nothing new has answered:** asp_001 and asp_002 (beech trunks known only by locality, so they cannot be told apart), ssb_002 and ssb_003 (same, silver firs), brd_001 (hospital courtyard behind a gate, hard rule 10), frk_027 (schoolyard, no viewing point sourced), inn_007 (pin on a private address), cbu_001 (a doline at 1,612 m with no route), dmr_002 (no sign it has stood since a 2019 decline report), sgz_005 and not_002 (no path or land tenure), not_003 (church grounds, access unknown), tmt_001 (a register group with access unknown), kcm_005 (no recognition line, photo or confirmed pin, so the build refuses it), sfo_012 (the same tree as live sfo_004). Taiwan's "pending" row is a `_notes` object, not a tree.
- **READY leads not written:** all seven are unverified finding aids. The St. Louis elm and willow are single-source and one is ticketed, the Tucson fig and jacaranda carry an unconfirmed champion claim and no story, the Windsor oaks are three register rows from 2008, the Segovia sequoia is one of six similar trunks behind a fence, and the Vienna Grimmelshausengasse oak has no age or girth. Each needs a verify pass first.
- Preflight: 0 problems; pace check clean.

## 2026-11-10 night run (18:37 window): nothing shipped, shelf dry

Rungs 1 and 2 clear: no sightings waiting, and health.py clear apart from an orange web-error type ("maplibregl is not defined", inline script). The refill step sent a verify agent to Coimbra and it found 0 trees. The four unmined register candidates were already live or leads. The council's Anexo VII tree list (Edital 198/2023) came back as a PDF this runner cannot read, noted on the Quinta das Lágrimas lead. The seven READY leads were already worked earlier today, so there was no write pass. Phoenix scouting was retried with no new angle reachable here, so it stays stalled with "retried" set to 2026-11-10. The Coimbra claim was left in place because cbr_007 sits verified but unmerged. Preflight reports 0 problems, but it also lists 4 reader submissions with no written verdict (`python3 scripts/judgement.py --open`), which I did not look at. For Hidde: nothing. A session with a PDF text tool could mine Anexo VII for Coimbra trees.

## 2026-11-10 session: Android search, tree page and draft at parity with the iPhone (parity batch 10)

- **Product (Android, not in any store):** search shows your recent searches when signed in (read from and written to the account's `recent_searches`, the same rows the iPhone and the website use; a cross per row and Clear all), and a town we hold no trees in now gets the grey card, the towns and the nearest tree we hold (Bern: card, Bern in Switzerland, the Linden of Morat 27 km). The tree page's collect sheet has Remove from collected, done at once with Undo that puts the tick back on its first day, and the collected date line. A tree being added has Move the pin and Merge with another tree in its menu; MergeChooser is ported from the Swift.
- **Library (hard list 5):** the town lookup uses Android's own `android.location.Geocoder` where the iPhone uses Apple's MKLocalSearch: a platform library, no new service.
- **Differences left:** tree_opened is not measured on Android (no PostHog key path there yet); own-tree's menu still lacks Move the pin and Merge (the screens exist now; it needs the account passed in and the server fold).
- **Parity:** 37 of 39 screens; map and map-full wait for build 42's sheet in the Swift. Shots in out/parity/android (search-recent, search-town, collect-sheet, collect-describe-menu, merge-chooser, merge-confirm, draft-placepin).

## 2026-11-10 session: Android directions, review ask, contribute and feedback ported from the iPhone (parity session 9)

- **Product (Android, not in any store):** the last four sheets are the iPhone's, ported from Kit/Directions.swift, Kit/ReviewPrompt.swift, Screens/Contribute.swift and the BrandSheet look. Take me there asks once which maps app and remembers it on the phone, Settings has the Directions row to change it; Send feedback opens the feedback form in the app (no longer the website); the tree page's report menu uses the same form; the review question comes after three different trees looked at, at a pause, with every timing rule of the iPhone (3, 10 and 25 trees, a week apart, three asks per install, 120 days and a newer version after a Yes).
- **Forced differences (data/android-parity.json):** no Apple Maps on Android, so the question offers Google Maps or Another maps app (Android's own chooser, which reaches Waze and every maps app). Yes on the review question opens Google Play's own review card (the Play review library, Hidde 2026-11-10: "prima doe dat"). The question before it stays as on the iPhone, behind the new remote switch `android_review_question` in data/app-switches.json, because Google's guide asks for no question before its card: switched off, the card comes alone at the same moments.
- **Same server path as the iPhone:** the form writes the same `submissions` row (kind tree, city, correction or feedback; page the tree's url or "app-profile"). Only the maps choice and the review counters live on the phone, both registered in data/cross-device.json as the iPhone's are.
- **Parity:** directions, review-ask, contribute and feedback side by side in out/parity/index.html, all four at parity. The signed-in form has no sweep frame on either phone; looked at on Android with -signed-in.
- **Shared pieces touched (kept small):** MainActivity (the root's two questions, tree pages counted for the review ask, a new tick counted two seconds later), Settings (the Directions row, Send feedback, -contribute and -feedback), TreeDetail (its report form replaced by the shared one, walkTo through Directions), account/Feedback.kt (one Submission.send), scripts/android_parity.py (the four frames).
- **Tests:** SheetsRulesTest (milestones, the quiet week, the yes rule, the sweep's silence, the links).

## 2026-11-10 session: Android screens linked into one app, flow walk on the emulator

- **Routes:** a link from the website opens the app's own screen (WebLink.kt, the iPhone's WebLink.swift and ContentView.open): a tree's page, a city or country on the map, species and collection pages, Explore, /open?tree= and ?city=, /profile?u=, and an app-only tree's /<city>#tree=<id>; what the app has no screen for goes back to the browser. The camera in the tab bar and Discover's add-a-tree now ask to sign in BEFORE the collect sheet, as on the iPhone (Hidde, 2026-10-12: "first login than overlay"); every gate reads the server-confirmed account state.
- **Flow walk:** android/app/src/androidTest/FlowWalk.kt, run by `python3 scripts/android_walk.py`: tabs reach every place, a tree opens and back leaves it, Want to visit and the camera ask to sign in first, a website link opens its tree. All five green on the emulator; CI compiles it.
- **Emulator lock:** another session's `am force-stop` crashed a walk mid-run, so `scripts/emulator_lock.py` now serialises the one emulator; android_parity.py and android_walk.py take it.
- **For Hidde, later:** links from the website open the app only once ancienttrees.app publishes `.well-known/assetlinks.json` with the Play signing key, which exists once the Play account does. Until then they open in the browser.
## 2026-11-10 session: Porto's ambassador badge moves from Miguel to Carlos

- **Product:** Carlos (request row 529, the Porto button on 2026-10-24) is now Porto's ambassador. Miguel keeps Guimarães, Braga, Calvos and Vales. Hidde: "Yes, swap them". Carlos asked three days before Miguel did and before the request-is-the-yes rule (2026-11-02), so his badge had never been granted; Miguel got Porto with his batch of five on 10-28.
- **Shown on the Porto page:** Carlos's profile still has its generated name, "Tall Ginkgo 7498", so that is what the page shows until he changes it in Edit profile.
- Done with `ambassador.grant` / `ambassador.revoke` and a sync (data/ambassadors.json). The heads-up mails for Porto start from a fresh baseline on the next knock, so the first knock mails him nothing.

## 2026-11-10 session: Android places and species ported from the iPhone (parity session 8)

- **Product (Android, not in any store):** a city on the map now has the iPhone's white box under its Highlights: the named ambassador with "Become one too", or "Become the <place> ambassador", which asks for an account first and then the same explainer and receipt; and "Help create Ancient Trees Plus" under the trees with the three-step question (open idea, up to two of four shuffled options or something else, then Tell me), sent to plus_answers and plus_waitlist as the iPhone does, gone once answered and switched off from the server like the iPhone (data/app-switches.json). The species page (Species.swift): mark, name, Latin in italics, how many on the map, what the species is, then its trees with photographs first; it opens from a tree page's species, from Discover's species tiles and from its See all list (before, those sent you to the map's filter). The tree page's "Approximate location" line opens the map to move the pin (PlacePin.swift), which sends a correction exactly as the iPhone does. The species chooser (SpeciesChooser.swift) with "Not on the map yet" and "Use what you typed" is now one screen for your own tree, the draft and the sweep; the map's Species filter shows each species' Latin and other names the same way.
- **Parity:** city, city-map-full, place-pin, species and species-pick side by side in out/parity/index.html, all five parity; what still differs is in data/android-parity.json (the Material map pin as crosshair, the bar's plain Close, a failed ambassador request on the sheet instead of a snackbar, Android's back arrow).
- **Shared pieces touched (kept small):** MapTab's place list draws the box and the Plus row for a searched city (two calls and two parameters), MainActivity (the species page and the pin map as pushed pages, the place host for the box, `-open=city:`, `-open=species:`, `-placepin`, `-speciespick`), TreeDetail (two optional actions: species and pin), PinPicker (an optional locate control), DraftTree and OwnTree now call the shared chooser, the feed reads each species' paragraph and the full names list. Strings in eight languages (strings_places.xml). The Plus answered flag is the one thing kept on the phone, as on the iPhone (data/cross-device.json android:device/plus.answered.v1).
- **Tests:** SpeciesPagesTest (the paragraph, an unmapped kind found by another name, a genus first with its sp. form).

## 2026-11-10 session: Android sign-in and profile ported from the iPhone (parity session 7)

- **Product (Android, not in any store):** sign-in, Settings and everything about people are now the iPhone's, ported from SignIn.swift, GoogleButton.swift, Profile.swift, ProfileEditor.swift, PrivacySettings.swift, People.swift, PersonProfile.swift, PermissionRecovery.swift, AmbassadorBadge.swift and Kit/Profiles.swift, EarlyAdopter.swift, SuggestedPeople.swift. The sign-in sheet: the app icon, the iPhone's headline per reason, Continue with Google and Continue with email as cream pills, the typed address and "Check your email" with Open Gmail or Open Mail. Settings from the gear on My trees: your card, Preferences (Distances, Location, Privacy settings), Help, About, Account (Sign out asks, Delete account explains and asks for DELETE), the version. Your profile editor (photo, name, country), Privacy settings with the Public profile switch and its question, Find people with Share your profile and Suggested, the follower lists, a person's public profile with badges and their two lanes, report and block, the early-adopter tag and its one-time sheet, and the location recovery sheet after a no.
- **Same server path as the iPhone:** profiles, follows, ambassadors, blocks, reports, rpc/follow_counts, rpc/public_profile, rpc/suggested_photographers, the avatars bucket and the auth user's early_adopter_seen. Nothing kept on the phone: the blocked list lives in memory and is read back from the server (the iPhone also keeps it on the phone). No new library: Google still signs in through the browser.
- **Parity:** nine frames side by side in out/parity/index.html. Parity: signin, signin-email, refused, profile-edit, early-adopter, early-adopter-sheet. In progress, differences in data/android-parity.json: Settings has no Plus row yet and Send feedback opens the website until those screens are ported; Find people has no pull to refresh yet. Forced: no Apple sign-in, no Directions row, the Play Store for a rating, Android's Settings path.
- **Shared pieces touched (kept small):** MainActivity (one Profiles, Moderation and ProfileRoutes; My trees' gear, face, people and follow counts now open these screens; Discover's names open the profile in the app, no longer the website), BrandSheet (an optional points list and a gold tile), My trees' header reads Profiles.kt and draws the tags row (its stopgap profile read is gone), AccountSheets loses the old sign-in sheet. Strings in eight languages from android/generate_profile_strings.py.
- **Tests:** ProfilesTest (short names, generated names, the early-adopter rule, flags, the sweep's routes, the demo account).

## 2026-11-10 session: Android My trees and your own tree ported from the iPhone (parity session 6)

- **Product (Android, not in any store):** the My trees tab is now the iPhone's, ported from Collect.swift and CollectedTile.swift: the live map of your collection under the same sheet as the map tab, the gear that fills in as the list becomes the page, the chevron-down back at full height, your picture, name, flag and follower counts with Find people beside them, the Collected and Want to visit tabs, country chips, the three-across grid with each tile's city, Want to visit's ghost tiles and "Find trees near you", the day-zero mission, and signed out the same page emptied with one green Sign in. A tree you added opens its own page (TreeDetail.swift with `mine`): your photograph, the city near it, Age, Girth and Species to add in green, "What makes this tree special?", More photographs with camera or library, the ellipsis menu (change name, species, age, girth; remove, asked first) and one action, Share this tree, which makes the unlisted page on the tap.
- **Hard rule 11:** nothing about your collection is kept on the phone. Saves and visits (with their dates, for newest first), your sightings, the trees you sent through the website and your profile row are read from the account when the app starts and after a collect; your own photographs are fetched with your token and held in a memory cache (account/MyTrees.kt).
- **Parity:** collection-tab, collection-tab-full and own-tree side by side in out/parity/index.html, all three marked parity; the open differences are in data/android-parity.json (own pins without your photo, the profile controls leading to the account sheet until the profile session lands, Move the pin and Merge not yet in the menu, the full sheet slightly see-through).
- **Shared pieces touched (kept small):** MainActivity (tab 2 draws My trees, Discover's See all opens it on Want to visit, a tree of your own opens on top, reloads after a collect), LaunchArgs (`-open=mine:`, `-mine-demo`, `-lane=want`, `-collected=`, `-saved=`), Saves gains the dates, MapSheet gains an optional chevron-down at full height (the map tab passes none, so it is unchanged), TreePlaceHeader and RecentreButton in MapTab and four small helpers in TreeDetail became `internal`. Strings in eight languages (strings_mytrees.xml). MyTreesTest covers the date shapes, names, your tree as a page and the share link.

## 2026-11-10 night run (window from 12:04 UTC)

Rungs 1 to 3 clear (no reader photos or notes, health.py green). Rung 5: the Fort Worth claim had no register candidates, so one write pass took the READY leads instead. 5 trees merged and preflight-clean: ftw_024, ftw_026 (Fort Worth), tus_015 (Tucson), vie_062 (Vienna), ind_005 (Indianapolis); app-only under APP FIRST. 7 READY leads held with reasons (nothing visible, paid-share limit, past the day-trip limit, multi-tree lead). Fort Worth claim released with --force (ftw_021 is a flagged near-duplicate of ftw_001).

## 2026-11-10 session: Android collect flow ported from the iPhone (parity session 5)

- **Product (Android, not in any store):** the camera in the tab bar now opens the iPhone's collect flow, ported from CollectSheet.swift, CollectIntro.swift, PinPicker.swift, SpeciesChooser.swift and the draft mode of TreeDetail.swift: "Add a tree" with Take a photograph and Choose from your photos (up to four at once); "Where does it stand?" with the map under a fixed pin when the photograph does not say; "Which one is it?" with the nearby trees, their distance and compass direction, the recognition line, the compare button, the far list with search when our pin is off, "Add a new tree" and "I am not sure which"; "Is this the one" with our photograph, How do I find it and the rough-pin lines; the payoff with "Was it worth the trip?", the note field under the thumb, Done or Add note, and Share this tree; "Thank you, that helps" for the unsure answer; and a new tree goes straight to its own page as a draft (name, age, girth, species from the list, what makes it special) with Save tree at the foot. The tree page's collect sheet gains Choose from your photos, and Add a photo opens the flow's own "Add a photo". Every word in all eight languages.
- **Same server path as the iPhone, signed in for real:** the photograph to the `sightings` and `shared-sightings` buckets, further photographs as `<id>-extra-<n>.jpg`, the `sightings` row with where the phone stood, the `visited` tick, a far pick's pin correction and the unsure shortlist as `correction` submissions, a saved new tree as a `tree` submission from app:collect. Nothing stays on the phone: a draft lives in memory until Save (hard rule 11).
- **Parity:** all eight collect frames side by side in out/parity/index.html; intro, away, ticked, voted and compare match; place, identify and describe have their open differences listed in data/android-parity.json (locate arrow on the pin map, your own trees in the list, the draft's menu and add-photo tile). New forced differences: Android's photo picker strips a photograph's location, so a library photograph always asks for the pin; the bottom sheet runs full width.
- **Shared pieces touched (kept small):** MainActivity (the tab bar camera, the tree page's camera and library hand over to the flow, the sheet and the draft page drawn), LaunchArgs (`-collect` and its steps, `-signed-in` for the sweep), TreePageActions gains two optional actions, Feedback.kt gains `Submission.tree`, android_parity.py lists the collect frames.

## 2026-11-10 session: Android Discover ported from the iPhone (parity session 4)

- **Product (Android, not in any store):** the Discover tab is now the iPhone's, ported from Home.swift, CollectedTile.swift, HeroCover.swift, Heroes.swift, NewFromVisitors.swift, IndexPages.swift and the open seat of AmbassadorBadge.swift. In order: the title and the search field that slides away reading down and comes back on any scroll up; the season hero ("Autumn is here", the nearest tree at its best whose photograph was taken in its season, the place named when it is far) or the stock hero; At their best now; New from visitors with the 44-point name line (public name to everyone, a tap signed out asks for a sign-in); the favourite cities with the city you stand in first; the open ambassador seat as a plain button (sign in, explainer, Apply, receipt); The records; Lists with an opinion (in-season first, one face per photograph); Tree countries; Want to visit full or empty; By species in three rows that slide together; Tree islands; The map is still growing; and the endless grid of more trees near you. See all opens the cities, countries, species and oldest-tree pages; a list opens its own page; a place lands on the map. The launch cover (2.4 seconds or a tap) is ported too, and the location question now comes half a second after it, as on the iPhone. Strings in all eight languages.
- **Open differences** (data/android-parity.json "explore"): species and profiles open the map filter and the website until their screens are ported; Add a tree and Want to visit's See all use what Android has today; list pages use rows until TreeCard lands from the tree-page session.
- **Shared files touched, minimally:** the feed reader learns taken_month, girth_cm, collection faces and months, country and species faces, favourites, islands and ambassadors (snapshot format bumped); MapTab takes a place handed over from Discover; MainActivity gets the real Discover tab. appsweep's explore frame passes -no-cover, so the iPhone shot is Discover rather than the cover.
- **Tests:** ShelvesTest (seven cases from buildShelves' rulings: the season word in the south, the hero shows the season it names, the city you are in leads, oldest by the low end, in-season lists first, the tail).

## 2026-11-10 session: Android tree page and tree card ported from the iPhone (parity session 3)

- **Product (Android, not in any store):** the tree page is now the iPhone's, ported from TreeDetail.swift and what it uses: the photograph full width with swipe, dots and a last grey "Your photo here" page; the little map in its corner that swaps with the photograph; a tree without a photograph opens on the map with the "No photograph yet" card; the page sliding over the photograph; back, share and report over it; Add a photo pill; the name, "district, city" and the worth-it thumb; the facts card (years old, girth, species, approximate location line, ticket band); Seasons; the story folded to six lines with "more"; notes from people who stood there (read, write, edit, delete, signed in only); Getting there; Something's wrong with its six chips; Discover more; the photo credit; the bar with Take me there and its distance, Collect, and the bookmark (Collect leads within 200 m, gives way past 250 m). Also the full-screen photo viewer (zoom, swipe, drag down to close) and the report form. The map's tree card is TreeCard ported whole. Every word in all eight languages.
- **Parity:** map-pin and photo-viewer side by side with no unexplained difference; tree and tree-nophoto match the iPhone shot for shot, with the parts that lead to unported screens listed in data/android-parity.json (your own trees, Choose from your photos, the pin picker, city/species/country pages).
- **Shared pieces touched (kept small):** BrandSheet.kt (port of Kit/BrandSheet.swift, new), PlainText in Theme.kt (SwiftUI's line height and tracking; Material's body style made every line wider and taller), RemoteImage gains fit and a stand-in, MapTab takes a `go` request, LaunchArgs reads `-photo`, the feed reads `girth_cm` (snapshot format bumped).
- **Nothing kept on the phone:** votes, reports and notes live on the server and in memory for the session only (hard rule 11).

## 2026-11-10 session: Android map tab ported from the iPhone (parity session 2)

- **Product (Android, not in any store):** the map tab is now the iPhone's, ported from MapTab.swift, BottomSheet.swift, TreeMap.swift, TreeRow.swift, TreeCard.swift, TreePlaceSheet.swift, MapSearch.swift and SpeciesPicker.swift. The sheet has the iPhone's four stops and its drag rules (below full the sheet moves, at full the list scrolls, down from the top of the list brings it back), a tap on the peek raises it, and a flick lands on the nearest stop. Search field fixed at the top, the four chips (Want to visit and Collected ask for sign-in first), the count under the grip, Highlights shelf, a Collected shelf, every tree in view as a row, the tapped pin's card with share and close, the Map pill at full height, the locate arrow and the location-off chip riding the sheet. The search page has the iPhone's lanes, Near you and Places worth a trip, and a picked city or country shows only its own trees until a finger moves the map or the cross clears it. The map opens on the person, else Dam square, with a blue dot that follows; it aims into the strip between the chips and the sheet.
- **Speed:** the catalogue is read row by row instead of as one 11.5 MB object, rows are read on every core, and a binary snapshot of our own catalogue makes later launches skip the JSON. On the one-core emulator under a loaded Mac the first read still takes about ten seconds; a real phone is not measured yet.
- **Parity:** `scripts/android_parity.py` now takes the iPhone sweep's own arguments (appsweep picks the subject trees, so map-pin is lod_001 on both), stands Android at Dam square like the sweep, waits for the catalogue instead of guessing, and has a search frame. map, map-full, map-pin and search sit side by side in out/parity/index.html; every remaining difference is listed in data/android-parity.json (among them: build 42's Airbnb sheet is decided in this LOG on 11-08 but not in the Swift on main yet, so Android follows the Swift; recent searches, the town lookup, the location recovery sheet, your own trees and the bookmark snackbar are not ported yet).

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-11](archive/LOG-2026-11.md)
- [2026-10](archive/LOG-2026-10.md)
- [2026-09](archive/LOG-2026-09.md)
- [2026-08](archive/LOG-2026-08.md)
- [2026-07](archive/LOG-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
## 2026-11-10 session: Android finishing pass, 33 of 39 screens at parity

- **New in the app:** the snackbar (Added to Want to visit with View, Removed with Undo, You are signed in; SaveHeart.swift); your own trees on the map in your own photograph and first on the Collected shelf (TreeMap.setMine, MineTile); the Plus row in Settings and pull to refresh on Find people; TreeCard on the collection page and the oldest-trees list, the ambassador sheet on BrandSheet and hidden for your own places; on collect, the locate arrow on the place map, your own trees within 30 m at the top of the list, and on the draft the ⋯ menu, the add-photo tile, the city link and Share after Save.
- **Fixed:** a sheet opened before signing in (the city's Plus "Tell me") now asks the server for the session when it is used, instead of a sign-in captured earlier.
- **Machinery:** scripts/gradle_locked.py, one Android build at a time on the Mac (three agents built in parallel without exhausting memory).
- **Left (in-progress):** map and map-full (build 42's sheet waits on iOS; first-launch read time unmeasured on a phone), search (recent searches, a town without trees), tree and tree-nophoto (review prompt and tree_opened measurement; Remove from collected with Undo), collect-describe (Move the pin and Merge in the draft menu; the short wait after Save, hard rule 11).
- **Not verified on the emulator:** it would not start from a session ("qemu_thread_create: Resource temporarily unavailable"); every piece was checked by build, unit tests and the Swift side by side. The flow walk on main still waits for Hidde to start the emulator from Android Studio.

## 2026-11-10 session: PR 30 merged; the flow walk on main waits for a free Mac

- **Merged:** PR 30 (screens linked into one app, flow walk, emulator lock), its build green. The walk was green on its branch (all five steps, under the lock).
- **Not run on main yet:** no emulator was running, and starting one failed ("qemu_thread_create: Resource temporarily unavailable", about 70 MB of free memory with several sessions and Android Studio open). Run `python3 scripts/android_walk.py` once the emulator is up again.

## 2026-11-10 session: Android, the basic app in one go (Hidde: "kun jij niet ondertussen al beginnen aan de hele app te bouwen")

- **New in `android/`, PRs 14 to 18:** species silhouettes in the pins (generated from site/src/lib/species-icons.ts by android/generate_species_icons.py) and the same-spot stack that spreads on a tap; Gabarito titles; sign in with Google in the browser or an emailed link, both on ancienttrees://auth-callback, the stored token spent with the server before anybody counts as signed in (data/cross-device.json `android:auth/session.refresh`); Want to go hearts on the server; sign out and delete account (delete_user()); Collect this tree with the camera within 3 km, writing the same sightings, storage and visited rows as the iPhone; the Seasons row on a tree page; the account sheet's Collected and Want to visit lanes. Copy taken from the website's own translations where they exist (signin-strings.ts, i18n.ts), the rest written for eight languages.
- **Left out on purpose:** walks and the at-its-best chip, set aside in the iPhone app on 2026-11-04 (DECISIONS.md). New tree from a photograph with no tree of ours near, the photo library route, notes, public profiles and follows: not in this round.
- **Dependencies:** AndroidX only (material-icons-extended, exifinterface); no Supabase client, no Google sign-in SDK.
- **Verified:** android.yml green per PR (unit tests: feed contract against the live site, pins and stack against lib/map.ts, sessions, collect rows, seasons).
- **Not verified:** nothing has run on a device. Unknowns: Google's return to the app, the emailed link opening it, the camera round trip and upload, how the sheets look at 375 px.
- **For Hidde:** in the emulator, the first things to try are signing in with Google and with email, a heart, and Collect (the emulator's camera works; its location can be set in the emulator's extended controls).

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

