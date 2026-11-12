# REVIEW — the fresh-eyes findings

Written daily by the Fresh-eyes review workflow (06:10 UTC): a separate,
empty context reads the last day's changes and the built site against the
corpus, and writes findings here, newest first. It never fixes anything.

Severities: **BLOCKER** (the site is wrong or broken; runs treat as rung 2),
**WARN** (drift or risk; rung 3), **NOTE** (worth knowing, no action forced).
"FOR HIDDE" appears only on judgment calls no run may make alone.

An empty day says "Nothing found." A reviewer that never finds anything is
suspect; a reviewer that finds fifteen nitpicks a day is worse.

---

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-10](archive/REVIEW-2026-10.md)
- [2026-09](archive/REVIEW-2026-09.md)
- [2026-08](archive/REVIEW-2026-08.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
<!-- archive-index -->
## 2026-11-12

Web half: the last 24 hours were Cardiff and Windsor trees into the app, an add-photo fix, Android release prep. No em dashes in site/dist. Standing findings unchanged.

- WARN site/dist/explore.html still says "Each pin opens a tree with its age, its species, why it is worth the walk, and directions from where you are" while app-only pins open a card with no story. Sixth review. Hard rule 2 and "a decision that changes what the product does also changes what the product says". Replacement: "Each pin opens a tree; some stories are in the app." Translations too.
- WARN site/dist/contribute.html (source site/src/pages/contribute.astro) still says "verified against independent sources" / "check every tip against independent sources", twice. False since "Good reader input IS the source" (2026-10-12). Seventeenth review. Replacement: "We read every submission before it is kept."
- NOTE data/cities/windsor.json wsr_002 story: "An iNaturalist record from August 2026 falls within range of the spot, though nobody has checked that it shows this particular oak." Narrates our process and states a non-fact; "Public copy never narrates our process". Drop the sentence.
- NOTE the 11-07 question stands: data/walk-routes.json routing through app-only trees that have no page is unchecked.

App half (iPhone SE: people, photo-viewer, place-pin, profile-edit, profile-signed-in, profile):

- NOTE APP profile-edit.png: Country is pre-filled "United States" with the Name still empty, so a new account shows a country nobody chose, and it is public with the profile. Show it empty until picked, or fill it from the device region and say so. For a session.
- NOTE APP profile.png and profile-signed-in.png: "Ancient Trees Plus" sits under the HELP heading beside Send feedback and Rate the app. The section title disagrees with what the row is (an offer). For a session; the paywall line is Hidde's (hard list 2).
- NOTE APP place-pin.png: two marks stand on the map, the drop pin and the tree disc beneath it, so "until the pin sits on the tree" is ambiguous about which one moves. For a session.
- Nothing wrong found on people.png and photo-viewer.png (credit and licence shown).

## 2026-11-11 code (full)

- APP-BUG-shared-photo-url-force-unwrap, ios/AncientTrees/AncientTrees/Screens/SharedTreeView.swift:108: shared tree photo URL from a server file name is force-unwrapped.

## 2026-11-11

Web half: the last 24 hours were Android parity work, one maps fix (atCanMap() asks for maplibregl, qa holds it) and data. No em dashes in site/dist HTML. Standing findings are unchanged.

- WARN site/dist/explore.html still says "Each pin opens a tree with its age, its species, why it is worth the walk, and directions from where you are" while app-only pins open a card with no story. Fifth review. Hard rule 2 and "a decision that changes what the product does also changes what the product says". Replacement: "Each pin opens a tree; some stories are in the app." Translations too.
- WARN site/src/pages/contribute.astro:17 and :401 (built into contribute.html) still say "verified against independent sources" / "check every tip against independent sources". False since "Good reader input IS the source" (2026-10-12). Sixteenth review in a row. Replacement: "We read every submission before it is kept."
- NOTE the 11-07 question stands: data/walk-routes.json routing through app-only trees that have no page is unchecked.

App half (iPhone SE: feedback, map-bar, map-full, map-pin, map, own-tree; map-full and map read like map-bar):

- NOTE APP feedback.png: "We check every vote, correction and tip" again (third review). Live-first (2026-10-24) means photos and notes are public before a check. "We read every vote, correction and tip" holds for all. For a session.
- NOTE APP map-pin.png: standing since 11-09. The map is on Amsterdam while the open card is "Dąb Fabrykant (the Factory Owner's Oak, als…", a Polish tree not in view. New this time: the card title is cut mid-word at two lines ("als…"), so the name a person reads is a fragment; a short display name or a third line would hold it. Also the locate button sits over a pin at the right edge and the pin shows through it.
- NOTE APP own-tree.png: "Amsterdam" under the title is underlined like a link while nothing around it is; the hero is a flat illustrated placeholder for a tree with no photo. Probably the designed empty state; flagging only the underline.

## 2026-11-10 compliance

First review, a session audit on Hidde's ask ("wees een lawyer en geef ons een audit"). Fixed the same day: the privacy page rewritten to what the product does (every account has a public profile, notes and the new-from-visitors row are public, shared links), plus who decides, legal bases, retention, processors, rights and the Autoriteit Persoonsgegevens; the terms (16 and over, profiles, notes, names in the visitors row); photo credits on the website link the licence and the source; first mails must carry a way to say no (mailcheck). Open, in data/compliance.json:
- profiles-33-flipped-public (Hidde): 33 private accounts made public on 2026-10-29 without asking.
- profiles-public-by-default (Hidde): no choice at sign-up.
- controller-identity (Hidde): no surname or KvK on the privacy page.
- posthog-without-consent (Hidde): app analytics with the account number, no consent, no retention.
- mailed-photos-before-yes (Hidde): mailed photos go live before the permission.
- mail-words-quoted-without-asking (Hidde): sentences from mails quoted on pages.
- app-credits-without-links (session): the app's credit line has no licence or source link.

## 2026-11-09

Web half: the last 24 hours were data (Vienna, San Francisco, Porto write pass, Upper Austria register), one web-errors fix and build 41. No em dashes in site/dist HTML. Standing findings are unchanged.

- WARN site/dist/explore.html still says "Each pin opens a tree with its age, its species, why it is worth the walk, and directions from where you are" while app-only pins open a card with no story ("Read its story in the app", APP_ONLY_PINS). Fourth review. Hard rule 2 and "a decision that changes what the product does also changes what the product says". Replacement: "Each pin opens a tree; some stories are in the app." Translations too.
- WARN site/src/pages/contribute.astro:17 and :401 still say "verified against independent sources" / "check every tip against independent sources". False since "Good reader input IS the source" (2026-10-12). Fifteenth review in a row. Replacement: "We read every submission before it is kept."
- NOTE the open question from 11-07 stands: data/walk-routes.json routing through app-only trees that have no page is unchecked.
- NOTE (Monday, corpus rot) CLAUDE.md's north star still says "a walk past a few" and the ladder still lists walks and Season while DECISIONS 2026-11-04 set Walks, Season and Plus aside in the app. Suggest one line under "What this is": "walks and season are dark in the app since 2026-11-04; the web keeps them".
- NOTE (Monday, copy reading) the strings added to i18n.ts and signin-strings.ts this week were skimmed; nothing ungrammatical found. No new AI_SHAPES to suggest.

App half (iPhone SE: early-adopter, explore, feedback, map-full, map-pin, map; map-full and map were skimmed, they read like map-pin):

- NOTE APP feedback.png: "We check every vote, correction and tip" again (see 11-08). Live-first (2026-10-24) means photos and notes are public before a check. "We read every vote, correction and tip" holds for all. For a session.
- NOTE APP map-pin.png: the map is on Amsterdam while the open card is "Dąb Fabrykant" with a Polish name, a tree that is not in view, behind a sheet that hides the pin it belongs to. Probably the sweep opening a tree by id; if a person can reach this (a deep link or search from far away), the map should fly to the tree.
- NOTE APP early-adopter.png: the profile shows "Paris ambassador" over an Amsterdam map for the test account. Fixture, nothing a visitor sees.
- explore.png: nothing found (Discover's "529 trees at their best this month · 11 within 20 km of you" is consistent with the cards below).

## 2026-11-08

Web half: last 24 hours were data (app-only trees, Lyon +10, Chicago, Salt Lake City, claims). No em dashes in site/dist HTML. Standing findings are unchanged.

- WARN site/dist/explore.html still says "Each pin opens a tree with its age, its species, why it is worth the walk, and directions" (count now "4169 trees in 834 places"), while app-only pins open a card with no story. Third review to see it. Hard rule 2 / "a decision that changes what the product does also changes what the product says". Replacement: "Each pin opens a tree; some stories are in the app." Translations too.
- WARN site/src/pages/contribute.astro:17 and :401 still say "verified against independent sources" / "check every tip against independent sources". False since "Good reader input IS the source" (2026-10-12). Fourteenth review in a row.
- NOTE the open question from 11-07 stands: data/walk-routes.json routing through app-only trees that have no page is still unchecked.

App half (iPhone SE: collection-tab, collection-tab-full, collection, contribute, directions, early-adopter-sheet; the three collection shots read the same, so two were skimmed):

- NOTE APP contribute.png: the sign-in sheet says "We check every vote, correction and tip" while the same reader-input rule is "live first, then checked" (CLAUDE.md, 2026-10-24); a photo or note is public before anyone checks it. Only the three kinds named are checked-first, so it is not false, but "We read every vote, correction and tip" would hold for all. For a session.
- NOTE APP early-adopter-sheet.png: "you are one of them" is a claim to every viewer, and the sheet sits over a map with no sign of who is signed in; confirm it only opens for a granted badge. Nothing contradicted on screen.
- directions.png, collection-tab.png: nothing found.

## 2026-11-07

Web half: the last 24 hours were data (walk routes, vendored photos, 16 app-only places, Préfargier duplicate) plus the New from visitors order. No em dashes in site/dist HTML.

- WARN site/dist/explore.html:281 says "4169 trees in 834 places" and "Each pin opens a tree with its age, its species, why it is worth the walk, and directions", while app-only pins open a card with no story ("Read its story in the app"). Second review to see it; the count now also disagrees with yesterday's 4047. Hard rule 2 / "a decision that changes what the product does also changes what the product says". Replacement: "Each pin opens a tree; some stories are in the app." Translations too.
- WARN site/src/pages/contribute.astro:17 and :401 still say "verified against independent sources" / "check every tip against independent sources". False since "Good reader input IS the source" (2026-10-12). Thirteenth review in a row.
- NOTE the standing "year printed as age" finding needs its regex narrowed: 103 pages match `content="A (17|18|19|20)[0-9]{2}-year-old`, but some are real ages (Te Matua Ngahere, "A 2000-year-old Kauri", is a sourced age, not a year). A qa check must compare against age_basis, not the digits.
- NOTE data/walk-routes.json (3d3fe5b0e, +684): still unchecked whether walks route through app-only trees that have no page (open since 11-06).

App half (iPhone SE: collect-describe, collect-identify, collect-intro, collect-place, collect-ticked, collect-voted):

- NOTE APP collect-describe.png: the new-tree page opens with a blank white hero of about half the screen above "A tree in Amsterdam", and the Species row is cut by the Save tree bar so its Add control is not visible. A reader sees an empty box and a half row; a placeholder or a shorter hero would show what the page is. For a session.
- NOTE APP collect-identify.png: "Pick the one in your photograph" and "Not sure which? Tap (i) to compare" are shown over a list of one tree, so there is nothing to pick between or compare. Say it with one candidate ("Is this the one?"). For a session.
- NOTE APP collect-place.png: the map's "Amsterdam" place label prints straight through the drag pin's stem, so the pin tip cannot be read against the label it sits on. For a session.
- NOTE APP collect-ticked.png / collect-voted.png: "Lime, 128 years old" is the planting age of a 1898 commemorative tree, shown without its basis (the story says "around 128"). Honest enough, but the sheet states it as the tree's age. collect-intro and the thumbs-up note field read consistently, nothing contradicted.

## 2026-11-06

Web half: the last 24 hours were app-only trees as pins (6522ad63a), vendored photos, walk routes, Android waitlist field. No em dashes found in the sampled built HTML.

- WARN site/dist/explore.html:139 says "4047 trees in 785 places" and "Each pin opens a tree with its age, its species, why it is worth the walk, and directions", but api/pins.json now draws 4,615 pins (568 cards carry the app-only flag `a`:1) and those open a card with no page and no story ("Read its story in the app"). The count and the promise disagree with the map after APP_ONLY_PINS (6522ad63a). Hard rule 2 / "A decision that changes what the product does also changes what the product says". Replacement: count the pins, and say "Each pin opens a tree; some stories are in the app." Translations too. Same sweep: grep site/src for other "N trees" / "opens a tree" lines on country, state and city maps.
- WARN (eighteenth review to see it) meta description prints a planting or event year as an age: 96 pages still match `content="A (17|18|19|20)[0-9]{2}-year-old`. Hard rule 2, Verify (a derived age states its basis).
- WARN site/src/pages/contribute.astro:17 and :401 still say "verified against independent sources" / "check every tip against independent sources". False since "Good reader input IS the source" (2026-10-12). Twelfth review in a row.
- NOTE APP city.png / city-map-full.png (Aachen, iPhone SE): the place has one tree, yet the sheet shows "Highlights" with The Forster Linde and then "The one tree" with the same Forster Linde right below. The same tree twice on one screen; a one-tree place needs no Highlights row. For a session.
- NOTE APP tree-nophoto.png (Maastricht): "The Caucasian Wingnut and Weeping Silver Lime of Waldeckpark" shows one "Years old 96-106", one girth 4.67 m and one species (Caucasian Wingnut) for a two-species title. A reader cannot tell which tree the figures describe. Hard rule 2 (precision the data does not have). For a session.
- NOTE APP collect-compare.png: reads well ("Nobody has established which lime it is, so tell us if you know"); collect-away.png and tree.png show nothing contradicted.
- NOTE data/walk-routes.json (3e19fba30, +30,190 lines in one commit): routes were rebuilt because new trees turned them into straight lines. With app-only trees now pins, check walks do not route through trees that have no page.

## 2026-11-05

Web half: the last 24 hours were the Plus question (web strings in eight languages, "I'd like to…", Skip, pick up to two: consistent with each other), card bookmark CSS, earned-back pause, health.py. No em dashes anywhere in site/dist HTML. Standing faults re-checked on the built site:

- WARN (seventeenth review to see it) meta description prints a planting or event year as an age: `grep -rlE 'content="A (17|18|19|20)[0-9]{2}-year-old' site/dist` still finds 96 pages (e.g. /waipoua-forest/te-matua-ngahere, /kamakura/great-ginkgo-of-tsurugaoka-hachimangu, /hong-kong/stone-wall-trees-of-forbes-street). Hard rule 2, Verify (a derived age states its basis). Build the qa.py check on built HTML first, then fix the meta template.
- WARN site/src/pages/contribute.astro:17 and :401 still say "Every submission is verified against independent sources before it goes live" / "We check every tip against independent sources". False since "Good reader input IS the source" (2026-10-12). Eleventh review in a row. Replacement: "We check every submission before it goes live; a good photograph with a GPS fix is enough to start a page." Translations too.

App half (iPhone SE: review-ask, search, signin-email, signin, species-pick, species):

- NOTE APP search.png: the species row for "lis" reads "Elm, listed as Lombarts' Elm" with "Ulmus 'Lombartsii' · 1 tree"; a reader sees a common name that points at itself under another name, and a one-tree cultivar ranked above European White Elm. Same alias-list family as tree.png on 11-03. Show one name; for a session.
- NOTE APP species.png: captured mid-transition, the Aleppo Pine page is overlaid by the launch splash tagline ("Trees worth the walk, wherever you are.") ghosting through the body text. Probably a sweep timing artefact, not shipped behaviour, but the sweep reviewed a screen no person sees; wait for the splash to leave before the shot.
- signin, signin-email, review-ask, species-pick: read consistently ("Sign in to keep this one", "An account keeps what you collect and save", "Growing near you first"); nothing contradicted. signin-email shows the same first sheet as signin, not an email step (sweep never advances), so it reviews nothing new.

## 2026-11-04 code (full)

Nothing new in the code. Read this run: web scripts tree-actions-js, visited-sync-js, share-js, tree-notes-js, map-filters-js, collection-js (ids/visited); app force-unwrap and request-path scan across Screens and Kit. Not read in full: the rest of the app Screens and the larger web scripts (signin-js, add-photo-js, my-trees-js, worthit-js, profile-js, people-js, map.ts). Seen and not reported (too narrow to be sure): atPushVisited drops a tick if the visited list is still in flight (seen is null); SharedTreeView.swift:108 force-unwraps a URL built from a server filename.

## 2026-11-04

Web half: the last 24 hours were research data and one app tweak (PlaceMapPage), plus the earned-back switch; nothing new in site/dist to read. Re-checked the standing faults on the built site:

- WARN (sixteenth review to see it) meta description prints a planting or event year as an age: `grep -rlE 'content="A (17|18|19|20)[0-9]{2}-year-old' site/dist` still finds 96 pages (e.g. /waipoua-forest/te-matua-ngahere, /kamakura/great-ginkgo-of-tsurugaoka-hachimangu). Hard rule 2, Verify (a derived age states its basis). Build the qa.py check on built HTML first, then fix the meta template.
- WARN site/src/pages/contribute.astro:17 and :401 still say "Every submission is verified against independent sources before it goes live" / "We check every tip against independent sources". False since "Good reader input IS the source" (2026-10-12). Tenth review in a row. Replacement: "We check every submission before it goes live; a good photograph with a GPS fix is enough to start a page." Translations too.

App half (iPhone SE: collect-compare, collect-describe, collect-identify, collect-intro, collect-place, collect-ticked):

- NOTE APP collect-compare, -describe, -identify, -intro and -place are the same "Add a tree" sheet over a tree photograph; none shows the step its filename names. The sweep never leaves the entry sheet (probably no camera in the simulator), so five of the six screens in this rotation review nothing. A session should seed those steps or drop the names.
- NOTE APP collect-ticked: reads well ("You found The Wilhelminalinde", "Lime, 128 years old", "Was it worth the trip?"); the title wraps to two lines on the SE, acceptable. Nothing contradicted.

## 2026-11-03

Web half: the last 24 hours were data (Lyon, Andalucia, Central Italy, California, northern England and Wales, southern Thailand; Spoleto and Vallombrosa are held for the pace, so not in the build). No em dashes in the built Lyon pages sampled. Findings:
App half (iPhone SE: tree, walk-begin, walk, city-map-full, city, collect-away):

- NOTE APP tree.png: the "Back", share and report controls are green on the green oak foliage and nearly vanish, so a person sees no clear way out of the tree page. Same fault as own-tree.png on 10-31; a session, not a night run. The title also carries the whole alias list, "Dąb Fabrykant (the Factory Owner's Oak, also called Jagosz)", over three lines on the SE; the first name alone would read cleaner (same truncation family as map-pin on 10-31).
- NOTE APP city.png / city-map-full.png: the sheet says "1 tree in Aachen" directly under the title "Aachen", and the ambassador row beside it reads "Aachen is looking for an ambassador. Help us improve this list." for a list of one tree; the promise is larger than the page. Consider whether a one-tree place needs the row.
- walk-begin, walk, collect-away: read consistently ("0 of 6 seen", "7 min, 0.6 km", "Photograph a tree you are standing in front of"); nothing contradicted.


- WARN (fifteenth review to see it) meta description prints a planting or event year as an age: `grep -rlE 'content="A (17|18|19|20)[0-9]{2}-year-old' site/dist` finds 96 pages, and the new Lyon page /lyon/anne-frank-chestnut says "A 2014-year-old Horse Chestnut" while its own story says it is barely twelve. Hard rule 2, Verify (a derived age states its basis). Nothing in qa.py refuses it. Build the check on built HTML first, then fix the meta template.
- WARN /lyon/pedunculate-oak-of-rue-viret: meta and og description read "A Pedunculate Oak in Villeurbanne (Les Poulettes, Lyon. Villeurbanne's official tree register calls this pedunculate oak rare, and it means it plainly", an unclosed parenthesis and a cut mid-sentence with no ellipsis. SEO_GEO_BLUEPRINT P2 (answer first, readable snippet). Check the location string for a missing closing bracket and cut at a sentence end.
- WARN site/src/pages/contribute.astro:17 and :401 still say "Every submission is verified against independent sources before it goes live" / "We check every tip against independent sources". False since "Good reader input IS the source" (2026-10-12) and the Tangier ruling. Ninth review in a row. Replacement: "We check every submission before it goes live; a good photograph with a GPS fix is enough to start a page." Translations too.

## 2026-11-02

Web half: the last 24 hours were data (Bergamo Gorlago cork oak, Porto wall, register scouting, lastmod). No em dashes in the built bergamo page. Findings:

- WARN (fourteenth review to see it) meta description prints a planting or event year as an age: `grep -rlE 'content="A (17|18|19|20)[0-9]{2}-year-old' site/dist` still finds 95 pages. Hard rule 2, Verify (a derived age states its basis). Nothing in qa.py refuses it. Build the check on built HTML first, then fix the meta template.
- WARN site/src/pages/contribute.astro:17 and :401 still say "Every submission is verified against independent sources before it goes live" / "We check every tip against independent sources". False since "Good reader input IS the source" (2026-10-12) and the 2026-10-21 Tangier ruling. Eighth review in a row. Replacement: "We check every submission before it goes live; a good photograph with a GPS fix is enough to start a page." Translations too.
- NOTE Monday copy reading (English added in the last 7 days in i18n.ts: "Which kind of tree?", "Any species", "No species by that name.", "Seasons", "Photographed in all four seasons", "Share your photo", "Become an ambassador"): grammatical, idiomatic, nothing machine-shaped. No new copycheck shape to add.
- NOTE APP search.png ("lis"): the species row reads "Elm, listed as Lombarts' Elm" with the bold match on the second half; a person sees the same name twice with an unexplained "listed as". Check that the alias label reads as a name, not a template. Lisbon/Minneapolis/Alishan/Liškiava/Indianapolis rows read consistently.
- NOTE APP tree-nophoto.png: the capture is only the splash ("Trees worth the walk, wherever you are."), no tree screen, so the photo-less tree page was not seen tonight. species.png also caught the splash fading over the Aleppo Pine page (text legible beneath it, "20 on the map"); a sweep timing fault, not a product fault, but it means the species page was not seen clean. signin.png ("Sign in to keep this one", Apple/Google/email, Terms and Privacy) reads consistently; signin-email and species-pick not opened.
- Monday corpus-rot audit and the decision-drift grep were not done in this run (time); a session should do them.



Web half: the last 24 hours were data (Dublin Marlay Park, Frankfurt Naturdenkmal trees, New York Douglaston, Porto/Portugal scouting, digest). No em dashes in the built dublin, frankfurt, new-york pages; their meta descriptions read true. Findings:

- WARN (thirteenth review to see it) meta description prints a planting or event year as an age: `grep -rlE 'content="A (17|18|19|20)[0-9]{2}-year-old' site/dist` finds 95 pages. Hard rule 2, Verify (a derived age states its basis). `grep -c "year-old" scripts/qa.py` is still 0, so nothing refuses it. Build the qa.py check on built HTML first, then fix the meta template.
- WARN site/src/pages/contribute.astro:17 and :401 still say "Every submission is verified against independent sources before it goes live" / "We check every tip against independent sources". Made false by CLAUDE.md "Good reader input IS the source" (2026-10-12) and the 2026-10-21 Tangier ruling. Seventh review in a row. Replacement: "We check every submission before it goes live; a good photograph with a GPS fix is enough to start a page." Fix the translations too.

App half (iPhone SE: place-pin, profile-edit, profile-signed-in, profile, refused, review-ask):

- NOTE APP profile-edit.png: "Your name" shows an empty field with the placeholder "The name people see", while the Settings row for the same account (profile-signed-in.png) shows the name "test". CLAUDE.md (Privacy and accounts) says every account has a profile name from the moment it exists, so a person sees the same account with a name in one place and none in the other. A session should check whether the field is meant to start with the current name.
- place-pin, profile, refused, review-ask: read consistently, nothing contradicted (the splash photo carries its CC BY-SA 2.0 credit).

## 2026-10-31

Web half: the last 24 hours changed one user-facing file, the flag fill on every signed-in visit (site/src/lib/signin-js.ts); the rest was data (Fort Worth and Canberra held by the pace, Portugal scouting, sightings, Rio Frio). No em dashes in the built English HTML. The flag change reads only the stored session's expiry and writes only while the flag is empty; nothing contradicts hard rule 11. Findings:

- WARN (twelfth review to see it) meta description prints a planting or event year as an age: `grep -rlE 'content="A (17|18|19|20)[0-9]{2}-year-old' site/dist` still finds 94 pages (e.g. /riverside/roosevelt-palm, /cork/1870-magnolia-of-fota, /seattle/wedgwood-scarlet-oak). Hard rule 2, Verify (a derived age states its basis). `grep -c "year-old" scripts/qa.py` is still 0, so nothing refuses it. Build the qa.py check on built HTML first, then fix the meta template.
- WARN site/src/pages/contribute.astro:17 and :401 still say "Every submission is verified against independent sources before it goes live" / "We check every tip against independent sources". Made false by CLAUDE.md "Good reader input IS the source" (2026-10-12) and the 2026-10-21 Tangier ruling. Sixth review in a row. Replacement: "We check every submission before it goes live; a good photograph with a GPS fix is enough to start a page." Fix the translations too.

App half (iPhone SE: map-pin, map, own-tree, paywall, people, photo-viewer):

- WARN APP paywall.png: the title "Unlock every walk" and the button "Tell me when this opens" sit beside "Plus is not open yet", so the headline promises an unlock the sheet then says is not there. Say what it is ("Walks are coming to Plus") or drop the verb. CLAUDE.md "promising what is not there"; copy for a session (PRODUCT_COPY.md), and pricing stays unshown on the hard list.
- NOTE APP own-tree.png: the "Back" chevron and the top-right control are dark green on the green hero illustration and are nearly invisible, so a person sees no way out except the system gesture. A session, not a night run.
- NOTE APP map-pin.png: the card title is cut mid-name, "Dąb Fabrykant (the Factory Owner's Oak, als...", so the alias is truncated into nonsense; show the first name only or let it wrap to a second line.
- map, people, photo-viewer: read consistently, nothing contradicted (photo-viewer shows the licence line "Śryż (CC BY-SA 4.0)").

## 2026-10-30

Web half: the last 24 hours were Portugal places (Monchique, Vale do Pereiro, Sao Bras de Alportel, Madeira, Porto, Coimbra), Las Vegas UNLV photographs, three photo-less trees live, the pace and photo-gate changes, and the flag at sign-in. No em dashes in the built pages sampled (monchique, vale-do-pereiro, sao-bras-de-alportel, las-vegas, canberra); the three new Portugal place descriptions read true and state a source for the age. Findings:

- WARN (eleventh review to see it) meta description prints a planting or event year as an age: `grep` of site/dist finds 94 pages with `content="A 17xx-20xx-year-old ..."` (e.g. /riverside/roosevelt-palm). Hard rule 2, Verify (a derived age states its basis). `grep -c "year-old" scripts/qa.py` is still 0, so nothing refuses it and prose has not held for eleven days. Build the qa.py check on built HTML first (a year 1700 to 2025 directly before "-year-old"), then fix the meta template.
- WARN site/src/pages/contribute.astro:17 and :401 still say "Every submission is verified against independent sources before it goes live" / "We check every tip against independent sources". Made false by CLAUDE.md "Good reader input IS the source" (2026-10-12) and the 2026-10-21 Tangier ruling. Fifth review in a row. Replacement: "We check every submission before it goes live; a good photograph with a GPS fix is enough to start a page." Fix the translations too.

App half (iPhone SE: directions, early-adopter, early-adopter-sheet, explore, feedback, map-full):

- NOTE APP map-full.png: the floating "Map" pill sits over the second card in the list and cuts through the "Canadian Poplar" title and its subtitle on the photo-less card, so a person cannot read what the card says. A session, not a night run.
- NOTE APP explore.png: "767 trees at their best this month" carries a "13 within 20 km of you" count while the card's tag says "Baarn"; fine if the location is Baarn, but the Discover tab title and the tab label "My trees" still differ from the "Your trees" sheet noted on 10-29 (unchanged).
- directions, early-adopter, early-adopter-sheet, feedback: read consistently, nothing contradicted.

## 2026-10-29

Web half: the last 24 hours changed no site pages beyond the profile bar (face opens the profile), find-people on the web and outreach/mail-voice files. No em dashes in built English HTML. Findings:

- WARN (tenth review to see it) meta description prints a planting or event year as an age: `grep` of site/dist finds 94 pages with `A 17xx-20xx-year-old` (e.g. /riverside/roosevelt-palm). Hard rule 2, Verify (a derived age states its basis). `grep -c "year-old" scripts/qa.py` is still 0, so nothing refuses it and prose has not held for ten days. Build the qa.py check on built HTML first (a year 1700 to 2025 directly before "-year-old"), then fix the meta template.
- WARN site/src/pages/contribute.astro:17 and :401 still say "Every submission is verified against independent sources before it goes live" / "We check every tip against independent sources". Made false by CLAUDE.md "Good reader input IS the source" (2026-10-12) and the 2026-10-21 Tangier ruling. Fourth review in a row. Replacement: "We check every submission before it goes live; a good photograph with a GPS fix is enough to start a page." Fix the translations too.

App half (iPhone SE: collect-ticked, collect-voted, collection-tab, collection, contribute):

- NOTE APP collection-tab.png: the tab is labelled "My trees" but the sheet under it is titled "Your trees" (and the subtitle says "Register and sign in", the sign-in sheet elsewhere says "Sign in"). Same screen, three wordings; pick one noun and verb. A session, not a night run.
- NOTE APP collect-voted.png: the note field placeholder "Leave a note: share something you'd like the next visitors to read about this tree" uses a colon reveal and runs two sentences into one; "Share something the next visitor should know about this tree" says the same. PRODUCT_COPY.md register.
- collect-ticked, collection (intro splash), contribute (sign-in sheet): read consistently, nothing contradicted.

