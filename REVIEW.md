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

## 2026-10-24

Web half: last 24 hours were mostly night-run logs, the Airbnb-style pin change (map.ts, TreeMap.swift), the Sicily collection and the new Messina fig (reader tip). Read the built Messina tree page and checked the built site for the age-meta fault. Not a Monday, so no corpus or copy audit. Two findings.

- WARN (repeat of 10-22 and 10-23, fifth review to see it) meta description still prints a planting year as an age: a grep of site/dist for `description" content="...(15xx-20xx)-year-old` matches about 110 tree pages (/riverside/roosevelt-palm, /seattle/wedgwood-scarlet-oak, /cardiff/raoul-wallenberg-tree, /cork/1870-magnolia-of-fota, /leiden/old-plane-of-the-plantsoen and more). Hard rule 2 and Verify (derived ages state their basis). Prose findings have not held this for two months; it needs the qa.py check on built HTML first (refuse a four-digit year from 1500 to 2025 directly before "-year-old" in a description meta).
- WARN /messina/moreton-bay-fig-of-villa-mazzini (meta description, og:description, twitter:description): "A Moreton Bay Fig 25.1 metres round in Centro, Messina" states the register's girth as fact, while the page's own story, intro and FAQ say the girth is disputed (14.5 m by a 2020 paper, 25.13 by the register) and the city meta says "14.5 to 25 metres round". The tree-level meta takes girth_cm alone and drops the conflict (never sharpen a vague source; Verify: conflict is stated). Say "14.5 to 25 metres round" or drop the number. The meta also ends in a bare "…" mid-sentence ("Sicily's register of monumental…").
- NOTE same page: the story quotes the reader's word as `'miricanu` with an opening quote mark and no closing one, twice (story and city question_context). Reads like a typo; either `'Miricanu'` or the word without quotes. Also og:image points at upload.wikimedia.org although commit a78b2cbcb vendored the photograph onto our own domain; the page may be serving the hotlink for social cards only.

App half (iPhone SE: paywall, people, photo-viewer, place-pin, profile-edit, profile-signed-in):
- WARN APP paywall ("Unlock every walk", "Plus is not open yet"): the "Also included" list names "Add your own photographs. Photograph a tree nobody has photographed yet, and your photo can go on its page" as a Plus feature, while DECISIONS/CLAUDE.md (2026-10-24, "live first, then checked") make a reader's photograph public the moment it is sent, for anyone. A screen that sells it as a paid perk promises a gate the product does not have, and contradicts the free-to-contribute stance. Drop the row or move it out of the paid list. For a session (copy on a decided product).
- NOTE APP profile-edit: a new, empty profile shows "Country: United States" with a flag preselected and the footnote "Its flag shows after your name". A default the person never chose will put a US flag beside every new name that is saved unchanged, including readers elsewhere. Worth a look: an empty "Choose" state, or the device region only if the person confirms.
- NOTE APP place-pin: the disabled "The tree is here" button and the footer "You need an account to send this" both read fine, but the title "Where is it really?" asks a question the body then answers as an instruction; no fault found, listed only because the sheet gives a signed-out person no sign-in route on this screen.
- paywall footer, people, photo-viewer (credit "Śryż (CC BY-SA 4.0)" visible, licence stated) and Settings read consistently; no promise the product cannot keep beyond the above.

## 2026-10-23

Web half: read the last 24 hours of commits (demand cut, Sources/AI line, about page, photo vendoring, photo-live mail) and sampled built pages. The "written with AI, readers correct it" line renders on tree pages; no em dashes on about or London; no "free forever" or "no accounts" anywhere in site/dist. Not a Monday, so no corpus or copy audit. One finding, a repeat.

- WARN (repeat of 2026-10-22) meta description "A 1903-year-old Mexican Fan Palm" still ships on /riverside/roosevelt-palm, "1914-year-old Redwood" on /riverside/chicago-white-sox-redwood-tree, "1950-year-old Dawn Redwood" on the Queen's Quarter, Belfast Dawn Redwood page, and others: a planting year printed as an age (hard rule 2, Verify: derived ages state their basis). Nothing in the last 24 hours touched `metaLead`/`ageToken()`, and the qa.py check on built HTML that yesterday's entry asked for has not landed. This is the fourth review to see this shape (08-10, 08-28, 09-13, 10-22); prose findings do not hold it, so it needs the check first: refuse `\b(1[0-9]|20)\d\d-year-old` in a description meta (about 200 pages match the pattern, most legitimately 1000 or 1100; the true errors are years 1500 to 2025).

App half (iPhone SE, six screens: Discover, Feedback sign-in sheet, map list, map pin, map, own tree):
- NOTE APP map list (map-full.png): the floating "Map" pill sits on top of the second card and covers its subtitle ("N… t" is cut mid-word under the pill), so the card reads as broken. A person sees an unreadable line; appfit does not measure a control over card text. For a session, not a night run (visual work).
- NOTE APP Discover (explore.png): the banner says "765 trees at their best this month · 13 within 20 km of you" while the shelf below leads with Baarn trees and the map screens sit on Amsterdam; nothing contradicts, but the 13 depends on a location the screen never states. Worth a look only if the count is not from a real fix.
- The Feedback sheet, own-tree and map screens read consistently; no promise the product cannot keep.



Web half: read the new Riverside, Mobile, Thomasville, Oroville and Logan Canyon pages and the Roosevelt Palm and Boyington Oak tree pages; no em dashes on any of them. Not a Monday, so no corpus or copy audit. One real finding.

- WARN /riverside/roosevelt-palm (meta description, og, twitter): "A 1903-year-old Mexican Fan Palm in Victoria Avenue, Riverside." The data says age_estimate "planted in 1903", and a planting year is printed as an age (hard rule 2; Verify: a derived estimate states its basis). Same fault in the built HTML of 65 tree pages, e.g. /riverside/chicago-white-sox-redwood-tree ("1914-year-old"), /oroville/mother-orange-tree ("1850-year-old"), /seattle/wedgwood-scarlet-oak ("1920-year-old"), /cardiff/raoul-wallenberg-tree ("1985-year-old"), /leiden/old-plane-of-the-plantsoen ("1800-year-old"). `metaLead` (site/src/lib/i18n.ts:612) trusts whatever `ageToken()` (site/src/lib/tree-copy.ts:16) hands it; the sentence-has-no-"years" guard exists in the no-range branch but pages with age_min/age_max take the in-range branch, where a year inside a wide band passes, or the meta takes its age from another path. The 2026-08-10, 08-28 and 09-13 reviews found the same shape. Wanted: a qa.py check on built HTML refusing `\b(1[0-9]|20)\d\d-year-old`, and the token refusing a number with no "year" after it in the sentence. Meta should read "Planted in 1903".

## 2026-10-22 (app half)

App half (collection-tab, collection, contribute, directions, early-adopter-sheet, early-adopter; iPhone SE). Two findings.

- NOTE APP: collection-tab and early-adopter, the sub-tab reads "Want to visit" while CLAUDE.md and the headline numbers call the list "Want to go" (PRODUCT_COPY.md: one name for one list). Raised on 10-21 and still there.
- NOTE APP: contribute, the sign-in sheet over "Tell us" promises "Every vote, correction and tip gets checked and answered", and the sheet behind says "Sending needs a free account". An answer to every tip is a promise the pipeline keeps only when a reader's verdict is written (check_every_submission_got_a_verdict covers submissions, not votes), and "free account" sits oddly beside premium as the destination (CLAUDE.md: copy never says "free forever"; "free" alone is allowed, so only worth a look).
- NOTE APP: collection and directions are the same photograph full-bleed with no map or tree behind it, so "directions" shows the sheet over a tree photo rather than a tree page; early-adopter shows a fixture profile ("test", Paris ambassador) so it is not judged.

## 2026-10-21

Web half: read /lisbon and the new Goethe-Institut dragon tree page (reader find, no sender name, no em dashes, access stated), /bamberg and two of its tree pages, plus london, aachen and paris for banned words. Two findings.

- WARN /lisbon (meta_description, og): "a nearly 2,850-year-old olive, a dragon tree nobody can age, and thirty-five more" names two trees plus thirty-five, 37, while data/cities/lisbon.json holds 36 trees after lis_037 went in; the count is over by one (SEO blueprint count promises; CLAUDE.md "when a place grows, its intro and meta grow with it"). Say "thirty-four more". question_meta ("and thirty-five more" after the olive) is right at 36.
- NOTE /bamberg/great-lime-of-teuchatz (title, meta): "350 Year Old Tree" / "A 350-year-old" takes the low end of a legend-dated "roughly 350 to 400 years, if a local legend holds" (Verify: never sharpen a vague source). "Up to about 400 years" or the range would match the data.
- NOTE /hallstatt/obertraun-dorfeibe (title, meta): "200 Year Old Tree" / "A 200-year-old" sharpens the data's "roughly 200 years" with age_max 260 (Verify: never sharpen a vague source). Say "Roughly 200 years old".

## 2026-10-21 (app half)

App half (collect-describe, collect-identify, collect-intro, collect-place, collect-ticked, collection-tab-full; iPhone SE). Unlike yesterday, identify, place and ticked now show their own screens: "Which one is it?", "Where does it stand?" and "You found ..." read clearly and agree with themselves.

- WARN APP: collect-describe is still the "Add a tree" start sheet (identical to collect-intro, over a photograph), so the describe step of the flow was not seen tonight; the sweep stops one screen early or the screen is not reachable.
- NOTE APP: collection-tab-full, the sub-tab reads "Want to visit" while CLAUDE.md and the headline numbers call the list "Want to go"; one name for one list (PRODUCT_COPY.md). The two Collected tiles are the same placeholder drawing with only "Amsterdam" on them, so a collector cannot tell which tree is which (fixture data, so only worth a look if real trees without photographs render this way).
- NOTE APP: collect-identify, the Wilhelminalinde row ends "Just off the Kalverstraat beside the Amsterdam Museum, 2.5..." so the line is cut inside a figure and the reader cannot tell what 2.5 was; end the clamp on a word or drop the trailing number.
- NOTE APP: collect-ticked reads "You found The Wilhelminalinde" with a capital mid-sentence ("the Wilhelminalinde"), and "Lime, 128 years old" is a bare figure for a tree whose age is a planting date (Verify: state the basis; "planted 1898" or "about 128 years").

## 2026-10-20

Web half: read /freiburg (count now 8, intro "Seven are natural monuments; the eighth is a reader's find" agrees with the list), the new Schönberg Beech page (reader find, no sender name, no em dashes) and the moved Kam Tin Tree House. Two findings.

- NOTE /hong-kong/kam-tin-tree-house (title, meta): "100 Year Old Tree" / "A 100-year-old" takes the low end of the data's 100 to 150 and the source's "over 100 years" (Verify: never sharpen a vague source). "Over 100 years old" matches the body.
- NOTE /hong-kong/kam-tin-tree-house (species vs story): the species line says "Indian Laurel Fig (Ficus microcarpa)" while the story calls it "a Chinese banyan", two names for one tree on one page (hard rule 9, one canonical common name). Say "Indian Laurel Fig" or explain once that it is the banyan.

## 2026-10-20 (app half)

- WARN APP: collect-compare, collect-describe, collect-identify, collect-intro, collect-place and collect-ticked are six screenshots of the same "Add a tree" sheet over different background photographs. None shows the screen its name promises (compare, describe, identify, intro, place, ticked), so either the sweep never navigates past the sheet or the flow is not reachable; the collect flow was not seen tonight and appsweep's `--check-lists` would not notice.

## 2026-10-19

Web half: read the Roehampton Lucombe Oak (new photograph), /lisbon after the Campo Santana yew retirement, no em dashes, CC BY-SA credit present. Two findings.

- WARN /lisbon (meta_description and question_meta): "an olive, a dragon tree ... and thirty-five more" while the page lists 35 trees in total, so the count is stale after the lis_014 retirement and over by two (SEO blueprint count promises; CLAUDE.md "when a place grows, its intro and meta grow with it", same for shrinking). Should say thirty-three more (or the olive and thirty-four more in question_meta).
- NOTE /london/roehampton-lucombe-oak (title and meta): "250 Year Old Tree" / "250-year-old" sharpens the story's own "somewhere between 200 and 260 years" to the guide's single estimate (Verify: never sharpen a vague source). "Up to about 250 years old" would match the body.

## 2026-10-19 (app half)

App half (tree, walk-begin, walk, city-map-full, city, collect-away; iPhone SE). The splash, both walks, the Add a tree sheet and the map read clearly and agree with themselves.

- NOTE APP: city (Aachen), the card says "1,000 years" without "roughly", while the only source says "more than 800 years" (1852) and the page says "roughly 1,000"; a bare figure reads as measured (Verify: never sharpen a vague source). Show the data's "roughly 1,000 years" or the range.

## 2026-10-18

Web half: read leipzig (index and Menzellinde), vienna, baarn, london and salt-lake-city as built; no em dashes, no leaked code. Two findings.

- WARN /leipzig (meta description and og): "19 protected trees in Leipzig" while the page lists 22 trees (data/cities/leipzig.json has 22) and `question_meta` says "21 more", so the count is stale after the three new trees (CLAUDE.md "when a place grows, its intro and meta grow with it"; checkParkCountPromises style fault). Update the count in `meta_description`.
- NOTE /leipzig/menzellinde (meta description): "A 200-year-old Small-leaved Lime" sharpens the source's "roughly 200 to 300 years" (age_min 200, age_max 300) to its low end, the same pattern as the 10-15 Cardón note (Verify: never sharpen a vague source). "A lime of 200 to 300 years" matches the body.

## 2026-10-18 (app half)

App half (search, signin, signin-email, species, species-pick, tree-nophoto; iPhone SE). The two sign-in sheets, species-pick, the Aleppo Pine species page and the photo-less tree page read clearly and agree with themselves.

- WARN APP: search, typing "lis" returns a species row "Elm" whose subtitle is a sentence cut off mid-word ("the city register lists American Elm, Ulmus amer...") and a second "Elm, listed as Lombarts' Elm". The query matched the word "lists/listed" in register wording, so a person searching for Lisbon sees two elm rows that look like data leaking into the results; a species row should show its Latin name and tree count like the Lombarts' row does.
- NOTE APP: tree-nophoto, the "Years old" box reads "96-106" with a hyphen and no unit beside it, while the title and the rest of the screen speak in plain words; fine as data, but it sits as a precise-looking range for an age the page cannot have measured (check it is the register's range, not derived).

---

## 2026-10-17

Web half: read the four new Berlin photographs (Fontanesia, katsura, coffeetree, Tiergarten beech) as built in site/dist, plus the 30 vendored photographs. The Fontanesia page serves the vendored /photos/ber_042 file, carries its CC0 attribution, has no em dashes. Nothing found.

## 2026-10-17 (app half)

App half (map, own-tree, paywall, people, photo-viewer, place-pin; iPhone SE; the same six as 10-15, so the rotation repeated). map, own-tree, people, photo-viewer (credit shown) and place-pin read clearly and agree with themselves.

- WARN APP: paywall, still unchanged from the 10-15 finding: "Add your own photographs" sits under "Also included" in "Unlock every walk", though readers add photographs for nothing today (nothing is gated, CLAUDE.md). FOR HIDDE: which items are Plus is his line (hard list 2).

---

## 2026-10-16

Web half: read the Cardiff Wallenberg tree (species corrected to tree of heaven by the parks officer, 8c0522dfb) and the three new London photographs (Battersea strawberry tree, Carshalton plane, Gunnersbury mulberry) as built in site/dist. No em dashes, the story, recognition line and meta agree with the new species, each photo carries its CC BY-SA credit, and the Cardiff page still says honestly that the pin is approximate. Nothing found.

## 2026-10-16 (app half)

App half (directions, early-adopter sheet, early-adopter profile, discover, feedback sign-in, map-full; iPhone SE). Directions, the early-adopter sheet and profile (tag, flag and "Paris ambassador" read together cleanly) and the feedback sign-in agree with themselves.

- WARN APP: map-full, the expanded sheet opens with a blank band of about 140 px between the handle and the first card, so the first screen of results is mostly empty, and the floating "Map" pill sits on top of the second card's title ("Ca... lar") and hides it. A person would read the gap as content that failed to load. Worth a look at what the pill is for when the sheet is full, since the Map tab already sits in the bar below it.
- NOTE APP: discover, the hero says "Autumn is here" and "748 trees at their best this month", but the first two cards under "At their best now" are full summer green with no colour. The count is from `best_time` data and may be right (flowers, fruit, bare silhouette all count), but the card photographs do not show it, so the promise reads thinner than the number. A label on each card naming why it is at its best would close the gap.

---

## 2026-10-15

Web half: read the new Seville Cardón of the Expo (sev_044) as built, and checked seville, munich, chicago, roosendaal, oss and potsdam in site/dist for em dashes: none. The Cardón page carries the reader's 200 to 300 years beside the press's 1,500, as the ruling asks, and its access line says honestly that the ground is private but open.

- WARN /seville/cardon-of-the-expo (Sources): the same official register is listed twice, "Inventario de Arboles Singulares de la Ciudad de Sevilla (Ayuntamiento de Sevilla, 2022), no. ficha 27" and "Inventario de Arboles Singulares de la Ciudad de Sevilla (2022), Ayuntamiento de Sevilla, ficha 27", so one source reads as two (CLAUDE.md "two independent sources" is about counting honestly). The string appears 54 times in data/cities/seville.json, so it is likely the register-match step adding a second spelling of an entry already there. Suggest register_match.py skip a register already named in `verified_sources`.
- NOTE /seville/cardon-of-the-expo (meta description and og:description): "A 200-year-old Cardón" states the low end of a reader's range as a plain fact, while the page body says "200 to 300 years" and the press says 1,500. A snippet should not sharpen a vague basis (CLAUDE.md Verify, "never sharpen a vague source"); "A 200 to 300 year old" would match the page.

## 2026-10-15 (app half)

App half (map, own-tree, paywall, people, photo-viewer, place-pin; iPhone SE). map, own-tree, people, photo-viewer and place-pin read clearly and agree with themselves (the photograph's credit shows where CC BY-SA asks for it).

- WARN APP: paywall, "Unlock every walk" lists "Add your own photographs: Photograph a tree nobody has photographed yet, and offer it for its page" under "Also included". The same app lets anyone add a tree and a photograph today (2026-10-14 commits: collecting needs a photograph, the Add a tree sheet), and CLAUDE.md says nothing is gated, so the screen sells something readers already have for nothing and "promises something that is not there" as a paid benefit. The sheet also says "Plus is not open yet", which is honest, but the list should name only what Plus will add. FOR HIDDE: which items are paywall and which stay free is his line (hard list 2).
- NOTE APP: map, the bottom sheet's first card is hidden behind the tab bar at rest (only a sliver of the photograph shows under "21 trees"), so the sheet's content is mostly covered on the SE. Likely the collapsed detent; worth a look that a person can tell the sheet lifts.

---

## 2026-10-14

Web half: read the rebuilt /about (d82aab58) in site/dist, and sampled amsterdam, seattle, bruges, riga, kimotsuki and riga/kaltini-oak. No em dashes, no surname on /about, no leaked code in the text of the pages sampled.

- WARN /about ("Where the trees come from"): "The stories are written with AI and corrected by people who know the trees." DECISIONS.md 2026-10-14 declined "drafted by AI, checked by humans" because no person checks every story before it ships; "corrected by people who know the trees" reads as the same promise (hard rule 2 spirit, CLAUDE.md "every claim true of the product"). Suggest "and readers who know the trees correct them".
- WARN verified_sources entries with an annotation after the URL keep appearing in the enrichment passes of the last day (data/cities/jerceni.json:52 "https://lv.wikipedia.org/wiki/... (circumference 9.2 to 9.4 m ...)", data/cities/cooper-creek.json:52 "https://trusttrees.org.au/... (National Trust ... last measured 1 Oct 2014)"). Same family as the 2026-10-13 Roosendaal finding: the href contains spaces and a parenthesis, so the Sources link breaks. A grep finds the pattern in 250+ city files. Suggest `enrich.py --apply` split the URL from the note (note to `verify_notes`) and qa refuse a source string with a space after a URL.
- NOTE /about: the page says "Every tree page has a button to tell me what's wrong or to add your photo"; the built tree page I opened (riga/kaltini-oak) shows "Add a photo", and I did not find a separate what's-wrong button in its text. Worth a check that both exist on every tree page.

## 2026-10-14 (app half)

App half could not run: /tmp/appshots-list.txt is empty and /tmp/appshots-note.txt says "no screenshots under /tmp/appshots".

---

