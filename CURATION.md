# CURATION — items awaiting Hidde's review

Newest entries on top. When you approve a city, its status moves to `curated` and each tree to `hidde_approved`.

## 2026-07-21 — Paris quality-floor improvement (pins resolved, one photo added)

- Paris was below the quality floor set in CLAUDE.md's priority ladder (8 of 10 trees `location_precision: approximate`, only 2 of 10 with a photo), and LOG.md's 2026-07-21 09:00 entry had already flagged it as the top priority once every pin's real precision was made honest. This run improved Paris instead of starting a sixth city.
- All 8 approximate pins resolved to `confirmed`:
  - Five city-managed trees (Great Plane of Parc Monceau, Sequoia of Buttes-Chaumont, Caucasian Elm of Avenue Foch, Plane of Parc Montsouris, Sophora of Buttes-Chaumont) matched against the Ville de Paris open tree registry (opendata.paris.fr, dataset `les-arbres`), which tags officially classified "remarkable" trees with measured circumference and height. Each match was the sole tree of its species flagged remarkable within its park/avenue, and physical dimensions were cross-checked against the story's own figures before accepting the coordinates.
  - Three Jardin des Plantes trees (Cedar of Jussieu, Second Robinier, Buffon Plane) are not in that city registry: the Jardin des Plantes is grounds of the Museum national d'Histoire Naturelle, not a city park, so Paris's own tree dataset does not cover it. Resolved instead via OpenStreetMap, which has each as an individually mapped, named heritage-tree node (`Cedre de Jussieu`, `Robinier de Robin`, `Platane de Buffon`). The Buffon Plane's OSM tag ("Plante par Buffon en 1785") and the Cedar's (`start_date: 1734`) matched the sourced planting years exactly; the Second Robinier's identity was cross-checked against a local history blog describing Vespasien Robin's 1636 planting at the same spot.
  - Worth remembering for any future Paris (or botanical-garden-adjacent city) work: `opendata.paris.fr` covers city-managed street and park trees only, not institutional grounds like the Jardin des Plantes, the Bois de Boulogne's arboretum, or similar.
  - The Sequoia's older "only one detailed source" flag is also cleared: sequoias.eu's national giant-sequoia survey independently confirms the tree (40m / 485cm circumference vs. the registry's 33m / 553cm; figures differ by measurement date but agree this is the same exceptional specimen).
- One photo added: the Great Plane of Parc Monceau, Public Domain, Tangopaso via Wikimedia Commons, found_needs_check for your approval. Confirmed as the right tree from the category description (planted 1814, 31m tall, matching the story exactly). This brings Paris to 3 of 10 photos, clearing the photo floor.
- 7 trees still have no photo (Second Robinier, Buffon Plane, Sequoia of Buttes-Chaumont, Elm of Saint-Gervais, Caucasian Elm of Avenue Foch, Plane of Parc Montsouris, Sophora of Buttes-Chaumont): searched Wikimedia Commons categories for Buttes-Chaumont and Jardin des Plantes plants, nothing usable turned up this round. Worth another pass in a future improvement round.

## 2026-07-20 — Rome (full research run, nightly workflow)

- 10 trees researched from scratch and written to `data/cities/rome.json`. Italy's national monumental tree law (10/2013) and the RAMI registry (ilregistrodeglialberi.it) made age and coordinate data unusually solid for several of these; Rome alone has 65 nationally registered monumental trees, more than any other Italian city.
- 7 flagged, for source or precision reasons, never for doubt about a tree's existence:
  - **The Quercia del Tasso** (Gianicolo): local legend claims 1000 years; no dendrologist has ever dated it and no source gives species below genus level. Story treats the 1000-year figure explicitly as folklore; age_min/age_max here (300-420) are a conservative documented-history floor, not a real estimate. Current physical condition after a 2011 arson attack needs an on-the-ground check.
  - **Adonis** (Villa Borghese): planting is well documented as "early 1600s" but no source gives a specific year; exact coordinates are for the Valle dei Platani generally, not the specific trunk.
  - **The Twin Planes of the Eleven Fountains** (Orto Botanico): two trees presented as one entry, matching how the garden itself presents them. Age is foresters' general estimate (300-400 years), no per-tree planting date found.
  - **The Cedar of the Belvedere** (Villa Doria Pamphilj): age genuinely disputed between two sources by up to 170 years, 150 years per the national registry vs. 300+ years per a detailed planting history. Presented as a range. Coordinates are an approximation within a very large park.
  - **The Leccio of the Lake** (Villa Borghese): same pattern, registry measurement (176 years) vs. traditional account (up to 300 years) tied to an 1784 garden redesign. Presented as a range.
  - **The Cedar of Celimontana** and **The Aleppo Pine of Celimontana** (Villa Celimontana): both are nationally registered as monumental, but no source gives either a planting date or age figure, only the registry's qualitative designation. Ages here are conservative undocumented placeholders (100+ years), not sourced estimates. Coordinates for both are approximate.
- 4 photos found on Wikimedia Commons with valid open licenses, all marked found_needs_check for your approval: Adonis / Valle dei Platani plane trees (CC BY-SA 3.0, Patafisik), the Leccio of the Lake (CC BY-SA 4.0, Albarubescens), the Fitolacca of the Capitoline (CC BY-SA 4.0, Albarubescens), the Cedar of Celimontana (CC BY-SA 4.0, Beatrice).
- 6 photos missing, none found on Wikimedia Commons after searching.
- One candidate dropped after research: **Quercia del Lupo**, a ~350-500 year old oak in Villa Borghese documented since a 1650s garden memoir, collapsed in a storm in 2018. Multiple outlets (RomaToday, Il Messaggero, Fanpage) confirm the collapse, but none confirm whether any remains are still visible on site, unlike London's Queen Elizabeth's Oak. Rather than direct visitors to a spot that may now be empty, it is referenced only in Adonis's story as context. Worth a follow-up if on-the-ground status can be confirmed.
- One candidate dropped for being outside city scope: the ~2,600-year-old Ulivone di Canneto Sabino, popularly called Europe's oldest olive tree, is in Fara in Sabina, province of Rieti, roughly 50 km from Rome and well outside the "100 cities" scope, same pattern as Lisbon's Santa Iria de Azóia olive.
- One candidate dropped for insufficient sourcing: an ippocastano (horse chestnut) on Via delle Tre Pile, listed on Rome's official monumental tree PDF, but the PDF could not be parsed for text and no secondary source gave an age or precise position. Worth a retry if the municipal PDF becomes accessible.
- Villa Torlonia's cedar of Lebanon (Via Nomentana) was investigated and dropped: the only registry entries found for a "Villa Torlonia" cedar turned out to be a different Villa Torlonia in Frascati, a separate town, not the Via Nomentana villa in Rome itself.
- No superlative claims beyond city-level ones ("oldest tree in Rome") checked against other published city pages; none conflict. The intro's "65 monumental trees, more than any other Italian city" claim is sourced to a 2025 RomaToday article comparing Rome to Naples and Caserta.
- Suggested follow-up: the official comune.roma.it monumental trees PDF (`Elenco_degli_alberi.pdf`) returned as unparseable binary data on this run; a future run with better PDF extraction could resolve several of the flagged coordinates and ages above, plus surface the ippocastano candidate.

## 2026-07-20 — Open design decision: illustrated tree art

- Hidde wants the map pins in a **painterly illustrated style** (reference: mobile-game key art, "look at the tree behind the lettering, not the font"): layered foliage in several greens, gnarled branches, depth. Not the current flat single-colour silhouettes.
- The current set is also under-differentiated: six of Lisbon's ten trees fall back to the same broadleaf shape (ombú, tipu, coral tree, nettle tree, silk floss, rubber fig). Only olive, dragon tree, cypress and ginkgo get their own.
- Hidde's own suggestion, and the right fix: key the icons off **leaf shape** rather than crown shape. Leaves differ far more at pin size, and every tree already carries a species.
- Not started; queued for the next working session so he can react to a first pass.

## 2026-07-20 — Lisbon (full research run, nightly workflow)

- 10 trees researched from scratch and written to `data/cities/lisbon.json`. Portugal has a national legal registry for "árvores de interesse público" (trees of public interest, Law 53/2012, run by ICNF), which made sourcing unusually solid for several of these compared to earlier cities.
- 6 flagged, for source or precision reasons, never for doubt about a tree's existence:
  - **Ajuda Dragon Tree**: age genuinely disputed, 258 years (documented transplant date, 1768) vs 400 years (popular rounding assuming an earlier undocumented origin). Presented as a range.
  - **Cypress of Príncipe Real**: Portuguese press/heritage consensus says ~150 years; monumentaltrees.com (checked for verification only, per the hard rule) states it was planted around 1740, implying ~285 years. Unresolved; went with the more corroborated figure.
  - **Ombú of Largo do Limoeiro**: most sources say 100 years, but a local history blog shows the tree already mature in 1910 municipal archive photos, implying closer to 115.
  - **Nettle Tree of Avenida de Berlim**: exact position at the avenue junction and the nearest metro walk time are approximate, need on-the-ground confirmation.
  - **Ginkgo of Praça Paiva Couceiro**: no source gives a precise planting date, only "over a century."
  - **Paineira of Jardim Alfredo Keil**: this specimen is one of six trees individually classified within a nine-tree ensemble registered together in 2017; no source dates this one tree specifically.
- 1 tree, **The Giant Rubber Tree of Mouraria**, is included despite being young (est. under 40 years) and having no official classification: a rubber fig that escaped a broken pot and grew between two building facades, a genuine local landmark by the "visually spectacular" qualifying criterion in CLAUDE.md rather than age. Labelled "Urban curiosity" on the city page so visitors know what to expect, same pattern as London's "Fallen monument" label.
- 3 photos found on Wikimedia Commons with valid open licenses, all marked found_needs_check for your approval: Ajuda Dragon Tree (CC BY 4.0, Dguendel), Cypress of Príncipe Real (CC BY-SA 3.0, Alatryste), Ombú of Largo do Limoeiro (CC BY 2.0, kenward).
- 7 photos missing, none found on Wikimedia Commons after searching.
- Two candidate trees were dropped for being outside Lisbon municipality: the ~2,850-year-old olive tree of Santa Iria de Azóia is in Loures, and the "Whistler Tree" cork oak is in Palmela (Alentejo), both roughly 30+ minutes outside city limits and not part of the "100 cities" scope.
- Two more candidates were dropped for access uncertainty rather than fact quality: a 364-year-old plane tree at Hospital Pulido Valente (would be Lisbon's second oldest tree, but public access to the hospital garden could not be confirmed) and two dragon trees in Carnide/Olivais on plots that may now be private residential land. Worth a follow-up in a future improvement round if public access can be verified on the ground.
- No superlative claims beyond city-level ones ("oldest tree in Lisbon") checked against other published city pages; none conflict.
- Suggested follow-up: the ICNF's national registry of trees of public interest (dados.gov.pt, "Arvoredo de Interesse Público") likely has exact coordinates and possibly precise ages for every classified tree in Lisbon; direct fetches of the dataset and of monumentaltrees.com's Lisbon pages were blocked (403) this run. A future pass with direct access to either could resolve most of the flagged age uncertainties above.

## 2026-07-19 — Species pages (new Contract F, blueprint v1.1)

- Blueprint bumped to v1.1 with your approval: new Contract F for species pages, a semi-automated browse facet. Auto-generated tree list, hand-written intro, publish-gated at 3+ trees plus an intro so nothing thin ships.
- Live now: /species index, /species/london-plane (5 trees, 3 cities), /species/caucasian-wingnut (3 trees, Amsterdam). Each tree page links to its species page; "Species" added to the top nav.
- NEEDS YOUR APPROVAL: the two species intros (data/species/london-plane.json, caucasian-wingnut.json), freshly written in the Paris style.
- Oak labels normalised (2026-07-19): the four Quercus robur trees were split across "Pedunculate Oak" and "English Oak". Both are valid, so I settled on the nationality-neutral "Pedunculate Oak" (English Oak reads oddly for the Amsterdam and future non-English oaks). Two London tree pages now show "Pedunculate Oak" instead of "English Oak"; same species, same scientific name. This unlocked /species/pedunculate-oak (4 trees, Amsterdam + London). CLAUDE.md hard rule 9 now tells nightly runs to keep species names canonical.
- NEEDS YOUR APPROVAL: the oak species intro (data/species/pedunculate-oak.json).
- Backlog change: single-species collection ideas (e.g. "The Great Planes of Europe's Cities") are now folded into the species pages to avoid duplicate content. Collections stay for cross-species themes only.

## 2026-07-19 — Amsterdam (full research run, nightly workflow)

- 10 trees researched from scratch and written to `data/cities/amsterdam.json`, replacing the name-only skeleton. All 10 pre-identified names from the chat handover checked out as real, verifiable trees, though several needed name corrections (see below).
- 8 flagged, all for source or precision reasons, never for doubt about the tree's existence:
  - **Heimanseik** (Amsterdam's oldest tree, ~275 years, Artis Park): exact position within the park is approximate.
  - **Vondelpark Poplar**: sources disagree on planting date (park-founding era ~1870 vs a specific 1885); age range widened.
  - **Hortus cycad**: age (~300 years) is sourced from the Hortus's own garden records; no independent third party confirms it. Also: dropped the "Spinoza cycad" name from the original handover notes, no source connects this plant to Spinoza.
  - **Olifantsiep**: two independent sources give slightly different planting decades (1900-1915).
  - **Lomanstraat X-trees**: species is the regionally typical London plane but not explicitly confirmed; a local legend about the trees surviving WWII firewood shortages is flagged in the story itself as unverified.
  - **Amstelkade olijfwilg**: exact species within Elaeagnus not pinned down; the two sources found both trace back substantially to the same original trade-press article.
  - **Amstelveld wingnuts**: strong sourcing on the 2006-2010 felling-permit fight (went to the Raad van State), but no source gives a precise planting date.
  - **Rijksmuseum wingnut**: one source says planted 1885, another implies 1907; went with 1907 as it matches Cuypers' documented 1884-1916 garden construction, but flagged as unresolved.
- 2 photos found on Wikimedia Commons with valid open licenses, both marked found_needs_check for your approval: Leidsebosje Planes (CC0 1.0, Ceescamel) and Wertheimpark Wingnut (CC BY-SA 4.0, Ceescamel).
- 8 photos missing, none found on Wikimedia Commons after searching.
- **Swap from the original handover list**: "Frederiksplein vleugelnoot" was dropped. Research found no specific named tree there, just a generic mention that wingnuts grow "among other locations" including Frederiksplein, no age, no independent second source. Replaced with the **Rijksmuseum Wingnut**, planted by the museum's own architect Pierre Cuypers and preserved through the 2013 renovation, which has real sourcing (bomenbieb.nl, Dutch Wikipedia).
- Also corrected: "Artis oak" is properly named the **Heimanseik**, after naturalist Eli Heimans who wrote about it in 1903.
- No superlative claims beyond city-level ones already used elsewhere on the site ("tallest/thickest tree in Amsterdam", "Amsterdam's oldest tree") checked against other published city pages; none conflict.
- Suggested follow-up: monumentaltrees.com almost certainly holds precise coordinates for several of these (Olifantsiep, Vondelpark poplar, Leidsebosje, Wertheimpark) but returned HTTP 403 on every direct fetch attempt this run. Worth a manual browse for exact pins in a future improvement-mode pass.

## 2026-07-19 — Second collection: Europe's 10 Most Remarkable Ancient Trees

- NEEDS YOUR APPROVAL: data/collections/europes-most-remarkable-trees.json. Ten trees, five London and five Paris, freshly written notes per entry.
- The intro says explicitly that the list is editorial and will shift as new cities join the map; that honesty is deliberate (P7) and gives the page a natural freshness cycle (P6).
- Live with the awaiting-curation banner until you sign off. The /collections index picked it up automatically.

## 2026-07-19 — Tone of voice document (draft v1.0)

- NEEDS YOUR APPROVAL: TONE_OF_VOICE.md, distilled from the existing style rules, the Paris run and the quality round. Includes four draft word bans beyond the existing ones (majestic, stunning, iconic, a testament to).
- NEEDS YOUR MATERIAL for v1.1: samples of your own writing (posts, mails, fragments, Dutch or English) to tune the voice to sound like you. No deadline; the Paris standard carries until then.

## 2026-07-19 — Site rebuilt to the four SEO_GEO_BLUEPRINT layers

- The generator now builds all four content layers with build-time validation: 20 tree pages, 2 question pages, 2 city pages, 1 collection, about page. A page that violates a contract fails the whole build.
- URLs moved to the contract pattern (/london instead of /cities/london) before the domain goes live; old URLs redirect.
- NEEDS YOUR APPROVAL: the first collection, "Trees Older Than 400 Years You Can Actually Visit" (data/collections/trees-older-than-400-years.json). Six entries, hand-drafted intro. Contract D says collections are editorial products, so this one ships with an awaiting-curation banner until you sign off.
- NEEDS YOUR APPROVAL: city FAQ blocks and question page answers, all newly written.
- DEFERRED BY HIDDE (2026-07-19): the about page. Contract E and P5 (verifiable entity) want one eventually for trust with Google and AI engines; revisit when the site has traffic. The Person schema stays on every page, without a profile link for now.
- NEEDS YOUR INPUT: correction and suggestion links now point to hello@ancienttrees.app. That mailbox does not exist yet; your TransIP hosting package can host it.
- Known gap vs blueprint: no og:image map-cards yet (Contract global rules); needs an image generation step later.

## 2026-07-19 — Quality round London and Paris (after external review)

- Paris is now the quality bar for every future city.
- Fact corrections Paris (Robinier of Square Rene-Viviani): Notre-Dame age phrasing softened to "had already stood for centuries"; the incorrect 1871 fire claim replaced, the story now names the Commune and the 2019 fire separately.
- Fact corrections London: Richmond Park claim softened to "one of the largest collections of ancient oaks in Europe"; the historically dubious Henry VIII "every tenth tree" law removed from the Royal Oak story; Wordsworth reference corrected to "in his 1800 poem Poor Susan".
- Opening lines of London trees 2, 4, 7 and 8 rewritten in the Paris style (curiosity-first).
- Barney the Plane moved to position 10 and stays flagged: the next nightly run must verify the exact location within Barn Elms via two sources and find a tree-specific story. Until then the story itself names the caveat.
- Queen Elizabeth's Oak (dead since 1991) now carries a "Fallen monument" label on the city page so visitors know what to expect.
- Both cities now open with a 60-100 word intro paragraph; the intro field is a fixed part of the city template from now on.
- Two new rules added to CLAUDE.md: superlative claims get cross-checked against other city pages before publication, and story length is now 150-250 words.

## 2026-07-15 — Paris (test run of the nightly workflow)

- 10 trees researched and written, saved to `data/cities/paris.json`
- 7 flagged, mostly for one reason: the tree is confirmed to stand in a given park by two sources, but the exact spot inside the park still needs confirmation. Wrong pin placement kills trust, so these stay flagged until coordinates are verified on the ground or via the Paris open data tree registry.
- 1 flagged for source depth: the Buttes-Chaumont sequoia has only one detailed source so far
- 2 photos found on Wikimedia Commons with valid open licenses (Robinier Rene-Viviani: CC BY-SA 3.0, Cedar of Jussieu: public domain), both marked found_needs_check for your approval
- 8 photos missing
- Suggested follow-up: the Paris open data portal (opendata.paris.fr) has a per-tree registry with exact coordinates for all 200,000 street and park trees. One improvement-mode run could resolve most flagged locations.

## 2026-07-15 — London (imported from earlier research)

- 10 trees imported into the new schema at `data/cities/london.json`
- 2 flagged: The Fulham Palace Oak (photo verification), Barney the Plane (location not confirmed by two sources)
- 10 photos missing: no open-license photo URLs were carried over from the original research, all need a Wikimedia Commons search
- 8 of 10 trees are missing verified source URLs (the original research named sources like Atlas Obscura and Wikimedia Commons but did not record links). These need backfilling before publication.
- Note: Queen Elizabeth's Oak (lon_005) is dead and recumbent since 1991. Decide whether a dead tree belongs in a top 10.

## 2026-07-15 — Amsterdam (skeleton only, not ready for review)

- 10 tree names carried over from chat research, no data behind them yet
- Status stays `pending` so the nightly workflow picks Amsterdam up for a full research run
- Nothing to curate yet
