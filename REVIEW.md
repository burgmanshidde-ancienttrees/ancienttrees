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
## 2026-11-08

Web half: last 24 hours were data (app-only trees, Lyon +10, Chicago, Salt Lake City, claims). No em dashes in site/dist HTML. Standing findings are unchanged.

- WARN site/dist/explore.html still says "Each pin opens a tree with its age, its species, why it is worth the walk, and directions" (count now "4169 trees in 834 places"), while app-only pins open a card with no story. Third review to see it. Hard rule 2 / "a decision that changes what the product does also changes what the product says". Replacement: "Each pin opens a tree; some stories are in the app." Translations too.
- WARN site/src/pages/contribute.astro:17 and :401 still say "verified against independent sources" / "check every tip against independent sources". False since "Good reader input IS the source" (2026-10-12). Fourteenth review in a row.
- NOTE the open question from 11-07 stands: data/walk-routes.json routing through app-only trees that have no page is still unchecked.

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

## 2026-10-28

Web half: the last 24 hours were the second-ambassador line, the Crann guest article drafts, Ede and Canberra registers, the Venice cedar redirect and enrichment of Lisbon, Bamberg and Potsdam. Nothing user-facing on the site changed except the redirect. Findings:

- WARN (ninth review to see it) meta description prints a planting or event year as an age: `grep` of site/dist finds 94 pages with `content="A 17xx-20xx-year-old ..."` (e.g. /riverside/roosevelt-palm "A 1903-year-old", /cork/1870-magnolia-of-fota, /seattle/wedgwood-scarlet-oak, /leiden/old-plane-of-the-plantsoen). Hard rule 2, Verify (a derived age states its basis). `grep -c "year-old" scripts/qa.py` is 0: nothing refuses it. Build the qa.py check on built HTML first (a year 1700 to 2025 directly before "-year-old"), then fix the meta template.
- WARN site/src/pages/contribute.astro:17 and :401 still say "Every submission is verified against independent sources before it goes live" / "We check every tip against independent sources". Made false by CLAUDE.md "Good reader input IS the source" (2026-10-12) and the 2026-10-21 Tangier ruling. Third review in a row. Replacement: "We check every submission before it goes live; a good photograph with a GPS fix is enough to start a page." Fix the translations too.

App half (iPhone SE, six collect-flow screens: away, compare, describe, identify, intro, place):

- WARN APP collect-describe.png ("A tree in Amsterdam"): the top 55 percent of the screen is an empty white block where the photograph should be, with the Back chevron and the more button floating in it. A person who just took a photograph sees no photograph of their own tree on the screen that describes it. Show the picture they took, or collapse the hero when there is none. A session, not a night run.
- NOTE APP collect-identify.png: the sheet says "You are standing among trees we map. Pick the one in your photograph." and lists exactly one tree, so the plural and "pick" promise a choice that is not there. The compare screen's "Nobody has established which lime it is, so tell us if you know" is a good line; the identify copy could read "We map a tree near you. Is this the one?" when there is a single candidate.
- NOTE APP collect-place.png: the city label "Amsterdam" is drawn directly under the pin and overlaps the pin's shaft, so the place a person is dragging towards is partly covered by the map's own label.
- collect-away, collect-intro: the same "Add a tree" sheet over the map and over a tree photograph; reads consistently, nothing contradicted.

## 2026-10-27

Web half: the last 24 hours were the second-ambassador line (AmbassadorLine.astro, web and app), the About Wilder line, the Porto Copper Beech retirement, eight nature-magazine sources and outreach work. Built output has no em dashes on porto.html; the new `ambassadorJoin`/`ambassadorJoinTitle` strings exist in all eight languages and read fine ("Become an ambassador for X"). Findings:

- WARN (eighth review to see it) meta description prints a planting or event year as an age: built pages say "A 1903-year-old Mexican Fan Palm" (/riverside/roosevelt-palm), "A 1914-year-old Redwood" (/riverside/chicago-white-sox-redwood-tree); a grep of built HTML finds at least 94 description metas of the form "A 17xx-20xx-year-old". Hard rule 2 (never fabricate tree facts), Verify (a derived age states its basis). scripts/qa.py contains no "year-old" check at all, so nothing refuses it. Write the qa.py check on built HTML first (refuse a year 1700 to 2025 directly before "-year-old"), then fix the meta template.
- WARN site/src/pages/contribute.astro:17 and :401 still say "Every submission is verified against independent sources before it goes live" / "We check every tip against independent sources" (also built into contribute.html twice and toronto/oldest-tree.html). Made false by CLAUDE.md "Good reader input IS the source" (2026-10-12) and the 2026-10-21 decision that a good photograph with GPS goes live with no written source. Second review in a row. Replacement: "We check every submission before it goes live; a good photograph with a GPS fix is enough to start a page." Fix the translations too.

App half (six screenshots: tree, tree without photo, walk, city, city map): the second-ambassador line is not visible in these shots (Aachen has no ambassador), so it was not judged. Findings:

- WARN APP tree.png (Łódź "Dąb Fabrykant"): the Back label and the share and report icons are drawn in green straight over the leafy hero photograph and nearly disappear (Back reads as a ghost). A person cannot see how to go back. Needs a scrim or a backing circle as on Apple Maps/AllTrails photo headers; a session, not a night run.
- NOTE APP city.png / city-map-full.png (Aachen): a place page titled "1 tree in Aachen" is offered in the app although CLAUDE.md says a place under four trees gets no place page. Check this is intentional for the app list or that the Aachen entry is a stale fixture.

## 2026-10-26

Web half (Monday): last 24 hours were the eight small places from photo-batch-2, the three Texas trees, the Albertshausen Bildeiche, the Wikimedia query fix and outreach/digest work. Read the built Albertshausen, Tamatoriyama, Bregenz pages and metas: no em dashes in the sampled new pages, ages stated with basis. Findings:

- WARN (seventh review to see it) meta description still prints a planting year as an age: built pages still say "A 1870-year-old Campbell's Magnolia" (/cork/1870-magnolia-of-fota), "A 1800-year-old London Plane" (/leiden/old-plane-of-the-plantsoen), "A 1920-year-old Scarlet Oak" (/seattle/wedgwood-scarlet-oak); a grep for a 15xx to 20xx year before "-year-old" in description metas matches about 110 pages (many legitimately 1500-year-old yews, the planting-year ones are the errors). scripts/qa.py has no check for it (grep "year-old" finds nothing). Hard rule 2, Verify (derived age states its basis). Prose has not held this for two months: write the qa.py check on built HTML first (refuse a year 1700 to 2025 directly before "-year-old" unless age_basis is source), then fix the template.
- WARN site/src/pages/contribute.astro:17 (meta/intro) and :401: "Every submission is verified against independent sources before it goes live" / "We check every tip against independent sources". Made false by CLAUDE.md Verify, "Good reader input IS the source" (2026-10-12) and the 2026-10-21 decision that a stranger's good photo with GPS goes live with no written source. Replacement: "We check every submission before it goes live; a good photograph with a GPS fix is enough to start a page." Check the translations of the same strings.
- NOTE site/src/pages/feed.xml.ts:108: "each verified against its sources" has the same drift in milder form; "each with its sources" is true for reader-found trees too.

Monday corpus audit (suggestions only):
- NOTE CLAUDE.md "Digest reports" is one paragraph of roughly 5,000 words that says itself "the rest of this paragraph is the history of each block". Move everything after that sentence to RULINGS.md/DECISIONS.md; the working rules (daily order, Monday set, readers' words whole) fit in ten lines.
- NOTE CLAUDE.md "Google recovery mode" restates the photo-only rule three times (own supply bullet, "A new tree of our own ships only with an approved photograph", Indexing) and still says "Rungs 5 to 7 mean depth on the kept set, never new pages" beside "Own supply ships again". Merge into one bullet and drop the pause/lift history (2026-10-22/25) into DECISIONS.md.
- NOTE CLAUDE.md "Ambassadors" paragraph mixes the mail-rest rule, the sent_drafts rule and the ambassador commands; split so the one-week rest is findable from the Outreach rung.

Copy audit (English added to i18n.ts in 7 days): "Know an old tree here? Add the first one.", "Nothing matches “{q}”...", the notes strings and the home strings read grammatical and idiomatic. NOTE "Saving..." uses three full stops where the rest of the file uses the plain word; harmless. No new AI shape found that copycheck misses.

App half (iPhone SE: review-ask, search, signin-email, signin, species-pick, species):
- NOTE APP review-ask.png is not a review ask: it is the welcome screen ("Trees worth the walk, wherever you are.") with no sheet, so that screen got no look tonight. Sweep fault, for a session.
- NOTE APP signin-email.png is again pixel-identical to signin.png (three buttons, no email field), second night running: the email step has not been seen by any review since 10-25. A session should check the sweep taps "Continue with email".
- NOTE APP signin sheet: "Sign in to keep this one" over a bare tree photograph with no tree named, so a person who arrived from a map or search cannot tell which "one". Fine from a tree page; worth a look from other entry points.
- search, species-pick, species read consistently: no contradiction, no clipped photograph, counts plausible (Lisbon 37 trees, Aleppo Pine 20 on the map).

## 2026-10-25

Web half: last 24 hours were the Add a photo / notes-card move on the tree page (web and app), the one shared map card, digest changes and night-run logs. Read the built Totteridge yew page for the new grey photo and notes cards (present, strings match i18n.ts) and checked the built site for em dashes (none in three sampled pages). Not a Monday, so no corpus or copy audit.

- WARN (sixth review to see it) meta description still prints a planting year as an age: 106 built tree pages match `description" content="...(15xx-20xx)-year-old`. Worst reading: /cork/1870-magnolia-of-fota says "A 1870-year-old Campbell's Magnolia" (the tree is named for its planting year, so it is about 156), /leiden/old-plane-of-the-plantsoen "A 1800-year-old London Plane", /seattle/wedgwood-scarlet-oak "A 1920-year-old Scarlet Oak". Also "A 1870" is ungrammatical. Hard rule 2 (never fabricate tree facts) and Verify (a derived age states its basis). Prose findings have not held this for two months and grep finds no check for it in scripts/qa.py: it needs a qa.py check on built HTML first (refuse a four-digit year from 1500 to 2025 directly before "-year-old" in any description meta), then the fix at the meta template.

App half (iPhone SE: profile/Settings, refused, review-ask, search, signin-email, signin):
- NOTE APP search ("lis"): the species row reads "Elm, listed as Lombarts' Elm" with "Ulmus 'Lombartsii'" under it. "listed as" is a data label leaking into a reader-facing species name (Hard rule 9: one canonical common name per species). Either the canonical name alone or the cultivar name; the bold run also spans "listed as Lombarts' Elm" although only "lis" matched.
- NOTE APP signin-email.png is pixel-identical to signin.png (the three-button sheet over the same background, no email field), so the "Continue with email" step was not captured and the email screen got no look tonight. Sweep fault, not a product fault; a session should check the sweep taps the button.
- NOTE APP Settings sign-in row: "Register and sign in to add and save trees." Two verbs for one act, and "add" sits oddly beside the 2026-10-24 live-first rule (a reader's photograph is public when sent). If photographs and notes need an account, say so in one verb ("Sign in to add and save trees"); if they do not, the line promises a gate that is not there.
- Other four screens read fine: no contradiction, no clipped photograph, no stray count.

