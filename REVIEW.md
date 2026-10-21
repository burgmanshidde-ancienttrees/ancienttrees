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
## 2026-10-21

Web half: read /lisbon and the new Goethe-Institut dragon tree page (reader find, no sender name, no em dashes, access stated), /bamberg and two of its tree pages, plus london, aachen and paris for banned words. Two findings.

- WARN /lisbon (meta_description, og): "a nearly 2,850-year-old olive, a dragon tree nobody can age, and thirty-five more" names two trees plus thirty-five, 37, while data/cities/lisbon.json holds 36 trees after lis_037 went in; the count is over by one (SEO blueprint count promises; CLAUDE.md "when a place grows, its intro and meta grow with it"). Say "thirty-four more". question_meta ("and thirty-five more" after the olive) is right at 36.
- NOTE /bamberg/great-lime-of-teuchatz (title, meta): "350 Year Old Tree" / "A 350-year-old" takes the low end of a legend-dated "roughly 350 to 400 years, if a local legend holds" (Verify: never sharpen a vague source). "Up to about 400 years" or the range would match the data.
- NOTE /hallstatt/obertraun-dorfeibe (title, meta): "200 Year Old Tree" / "A 200-year-old" sharpens the data's "roughly 200 years" with age_max 260 (Verify: never sharpen a vague source). Say "Roughly 200 years old".

## 2026-10-21 (app half)

App half (collect-describe, collect-identify, collect-intro, collect-place, collect-ticked, collection-tab-full; iPhone SE). Unlike yesterday, identify, place and ticked now show their own screens: "Which one is it?", "Where does it stand?" and "You found ..." read clearly and agree with themselves.

- WARN APP: collect-describe is still the "Add a tree" start sheet (identical to collect-intro, over a photograph), so the describe step of the flow was not seen tonight; the sweep stops one screen early or the screen is not reachable.
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

## 2026-10-13

Web half: read the new Roosendaal pages as built (copper beech of Nispen cemetery, Julianalinde, the London plane of De Kring in the data) and the Copenhagen FAQ edit (cf54927a, 98729e46: 41 + 8 = 49 trees, the counts agree; the built copenhagen/index.html in site/dist still carries the older text, so that page was read from data/cities). No em dashes or banned words in site/dist/roosendaal.

- WARN /roosendaal/* and at least seven other built pages (`verified_sources` strings in data/cities/roosendaal.json, e.g. lines 199-200, 316-318): an aerial-imagery note was stored as a URL ("https://service.pdok.nl/hwh/luchtfotorgb/wms/v1_0 (Actueel_orthoHR, leafless spring frame, viewed 2026-10-13)") and renders as a Sources bullet "service.pdok.nl" whose href contains spaces and a parenthesis, so the link is broken and names nothing a reader can check. The register's ArcGIS query URL is also printed twice (once as the register line, again as a bare "services-eu1.arcgis.com" bullet) and opens raw JSON. Same family as the 2026-10-12 file-name finding: code leaking as text in Sources. Suggest note-only entries live in `verify_notes` or `pin_source`, and the register link not be repeated as a plain source.
- WARN /roosendaal/copper-beech-of-nispen-cemetery and /roosendaal/julianalinde-of-nispen (`transport`, data/cities/roosendaal.json:292, 333): the visitor-facing travel line ends "650 m from the Julianalinde (roo_013)" / "(roo_012)", an internal tree id printed as text. The Nearby card on the same page says 640 m, so the page also states the distance twice with two values.
- WARN same pages (`access`): "Register: visitable ja, visible ja, openbaar ja, owner a religious body (parish)" puts Dutch register field values and a column list into the English access line; "No cemetery hours found" is fine, the "ja" list is not a sentence a visitor can use. Suggest "The register lists it as visible and open to visit."
- NOTE /roosendaal London plane of De Kring and the Oriental plane: `location_precision` is "confirmed" with the evidence being an aerial frame viewed on 2026-10-13 (CLAUDE.md burn list names "aerial imagery or equivalent evidence" for pin passes; `check_pin_upgrades()` should be the judge of whether that counts, I did not run it).

## 2026-10-13 (app half)

App half (collect-identify, collect-intro, collect-place, collect-ticked, collection-tab-full, collection-tab; iPhone SE).

- WARN APP: collect-intro, collect-place and collect-ticked are three more frames of the same "Add a tree" sheet (Take a photograph / Choose from your photos) over different backdrops; none shows a place step or a ticked state, so the screens they are named for ship unlooked-at. Same fault as 2026-10-12 (collect-away/compare/describe), still open: the sweep does not reach the later steps of the add flow.
- WARN APP: collect-identify, "Which one is it?" with "Pick the one in your photograph" offers a single candidate, 325 m south, under the line "You are standing among trees we map", and its own description says "Nobody has established which lime it is, so tell us if you know." A choice of one that admits it may not be the tree, 325 m away, contradicts the sentence above it and is the data-model-sentence-in-a-row fault logged for search on 2026-10-10. Suggest the step not show when only one candidate exists or the row drop the "nobody has established" line.
- NOTE APP: collection-tab-full, the Collected grid shows two identical placeholder tree tiles labelled only "Amsterdam" (different backdrop colours, no tree names), so a person cannot tell which two trees they collected. Likely fixture data without photographs; if real collected trees without a photo look like this, the tile needs the tree's name.

## 2026-10-12

Web half: read the header search commit (baf8726c: strings in all eight languages, home and map hide the icon by CSS), the cookie bar copy, the register-matching commit (52ec9b7f) as built on turin and rouen, and scanned portland, trento, alicante, rouen, kaunas, oslo, setubal, valencia and barcelona for em dashes and banned words: none found.

- WARN /turin/plane-of-the-giardini-cavour (and at least nine other built tree pages; source: 52ec9b7f, `verified_sources` in data/cities/*.json): register_match.py appended internal file names to the public Sources list, so a visitor reads "piemonte-alberi-monumentali.json, no. 003/L219/TO/01" as a bullet beside the real links (rouen carries "rouen-foret-arbres-remarquables.json, no. 6" in the data). That is code leaking as text, and it names no reader-checkable source. Suggest storing the register's public URL plus the number, or rendering the number without the file name.
- WARN tree pages with a reader photograph (site/src/lib/i18n.ts, `photoDeleteBody`, from d6b02f57): the "Delete this photo?" sheet says "If it is already on the tree's page, it stays there." A person who taps Delete photo on their own picture is told it stays public, so the button promises removal it does not do. Either the label should say what it does ("Remove from My trees") or deletion has to reach the page; the takedown route (photo_takedown.py) is the path that actually removes it. Same sentence is in all eight languages.
- NOTE docs (Monday audit, limited to the cut CLAUDE.md and a spot read of GO_TO_MARKET.md): CLAUDE.md names Phase 1 as traction and Phase 2 as app and money, while GO_TO_MARKET.md (written 2026-07-21) uses its own Phase 1 "first pulse. A few hundred real visitors"; two phase schemes under one word. Suggest GO_TO_MARKET.md say which of its phases map to CLAUDE.md's, or drop its numbering. No other rot found in the files read; PRINCIPLES.md, PRODUCT_IA.md, BACKLOG.md and DECISIONS.md were not audited in depth.
- NOTE copy (Monday English reading): the English strings added this week (cookie bar, "Search a city or tree", "Delete this photo?", "Photo deleted") read well and are idiomatic.

## 2026-10-12 (app half)

App half (city-map-full, city-map, city, collect-away, collect-compare, collect-describe): the Aachen list, its map and the ambassador row read clearly and agree with each other (1 tree, one pin, one card).

- WARN APP: collect-away, collect-compare and collect-describe are three frames of the same first step, the "Add a tree" sheet with Take a photograph and Choose from your photos (over three different backdrops). Today's commit 1f67ab01 rebuilt exactly those steps (you found it, thank you, is this the one) on the new sheet layout, and the sweep still does not reach them, so the redesigned screens ship unlooked-at. A session should check the sweep's route to each step.
- NOTE APP: `city` is the full-screen splash photograph and tagline ("Trees worth the walk, wherever you are."), not a city screen; the same capture fault was logged for profile-signed-in on 2026-10-08, so a frame named for a screen is again showing the launch image.

---

## 2026-10-10

Web half: read brighton, glasgow, london, krakow and florence (titles, meta descriptions and ages agree; no em dashes or banned words) and the Brighton Preston Twins story after today's edit.

- WARN /brighton, the Preston Twins (data/cities/brighton.json, story and verify_notes): the story states two claims our own verify_notes say the sources contradict, softened only by "local accounts" and "by local account": the elms planted "on land ... under the Bishop of Chichester" c.1613 (the notes record the manor passing to the Crown by 1561 and the Shirleys leasing it by 1613) and Brighton being "the first council in the UK" to inoculate elms (the notes record DutchTrig first used at Seaford in 2016). Hard rule 2 / bridge-claim rule: a hedge does not make a claim we hold evidence against safe to print. Suggest dropping both or stating the disagreement outright.
- NOTE (carry-over from 2026-10-09, still live): city pages still print "visited in {city}" (site/src/lib/i18n.ts:500) beside the new Collected wording.

## 2026-10-10 (app half)

App half (profile, refused, review-ask, search, signin-email, signin): Settings, the location-refused sheet and the sign-in sheet read clearly and agree with each other.

- WARN APP: search ("lis"), the Species row "Elm" shows the subtitle "the city register lists American Elm, Ulmus amer..." (truncated) where every other row shows a tree count; a sentence explaining our data model is leaking into a result row, and the next row ("Elm, listed as Lombarts' Elm") reads as a duplicate species. A reader cannot tell what either row will open.
- NOTE APP: signin-email is pixel-identical to signin (the three-button sheet), so the sweep frame does not show the email step it is named for; that screen ships unlooked-at.

## 2026-10-09

Web half: read salt-lake-city (new, 5 trees; title, meta, intro and counts agree, the Liberty Park and Temple Square stories say plainly that no planting date is sourced) and the Temple Square Wych Elm page; scanned seville, barcelona, amsterdam, singapore, munsterland and salt-lake-city for em dashes and banned words, none found.

- WARN /salt-lake-city and every city page (site/src/lib/i18n.ts:500 `visitedOf`, site/src/pages/[city].astro:292): the progress line still reads "0 of 5 visited in Salt Lake City" while today's commit c3f83988 renamed Seen to Collected everywhere and the tick to "Mark as collected". The same page now says Collected on the cards and "visited" in the counter, two words for one act. Suggest "collected in {city}" in all eight languages.

## 2026-10-09 (app half)

App half (paywall, people, photo-viewer, place-pin, profile-edit, profile-signed-in): the paywall says plainly that Plus is not open and nothing is charged, the pin-correction sheet, Find people, the photo viewer with its CC BY-SA credit and Settings (now "0 collected") read clearly and agree with each other. Nothing found.

## 2026-10-08

Web half: read vienna (50), delft (11), chicago (16) and nuremberg (18); titles agree with the city files and none carries em dashes or banned words.

- WARN /delft (data/cities/delft.json lines 5-6): the title says "11 to See" but the page intro and the meta description both still say "Eight verified ancient trees", a stale count after Delft gained three trees today. This is the self-contradiction CLAUDE.md names ("when a place grows, its intro and meta grow with it"; hard-coded counts in copy). The count-promise check apparently does not see the word "Eight" in a hand-written intro or meta.

## 2026-10-08 (app half)

App half (people, photo-viewer, place-pin, profile-edit, profile-signed-in, profile): people, the pin-correction sheet, the photo viewer and Settings read clearly and agree with each other.

- NOTE APP: profile-signed-in shows only the full-screen hero photograph and tagline ("Trees worth the walk, wherever you are.") with no profile content at all, so the frame does not show what its name promises. Probably the sweep caught the splash before the screen loaded, but a signed-in screen that can be photographed as a splash is worth a look for a session.

---

## 2026-10-07

Web half: read utrecht (30 trees; title, meta and the ginkgo and linden ages agree with the city file) and the Oude Hortus Ginkgo page, and scanned utrecht, vienna, tokyo, warsaw and munich for em dashes and banned words. Nothing found on the web half.

App half (explore, feedback, map-full, map, own-tree, paywall): discover, map, the feedback sign-in and the paywall read clearly and agree with each other.

- WARN APP: map-full, the floating "Map" pill sits on top of the second card's title ("The Weteringp... ch Elm") and hides part of the name; the pill should sit clear of the list. This control was the odd one out in the 2026-09 sweeps too.
- NOTE APP: own-tree shows a large flat drawn tree as the hero of a reader's own tree, with no sentence saying no photograph exists; CLAUDE.md allows the silhouette only beside that sentence. Probably the sweep fixture has no photo, but a real tree added without one would read the same.

