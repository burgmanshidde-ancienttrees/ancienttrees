# CURATION — items awaiting Hidde's review

Newest entries on top. When you approve a city, its status moves to `curated` and each tree to `hidde_approved`.

## 2026-07-20 — Rome (full research run, nightly workflow)

- 10 trees researched from scratch and written to `data/cities/rome.json`. Rome holds more officially classified monumental trees than any Italian city, so most entries rest on the municipal/regional monumental-tree material plus a second independent source. A city you know a little, so worth a look when you have time.
- 9 flagged, 1 clean (`ai_generated`). As with earlier cities, flags are about age precision, exact in-park coordinates, or legend, never doubt that the tree exists:
  - **Quercia del Tasso** (Gianicolo): the headline "oldest tree in Rome," but honestly the hardest to pin down. Age is legendary (linked to Tasso, who died 1595, when it was already mature; the "~1000 years" figure is tradition). It is now a fire-damaged, propped remnant protected as a natural monument, not a full standing tree. Species follows the common description as a leccio (holm oak) but the sources I reached do not firmly confirm it. I set it as the oldest (age_max 600) so it heads the question page, and wrote the answer to say plainly that it is oldest "by tradition."
  - **Orange Tree of Santa Sabina** (Aventine): the 1220 / Saint Dominic planting is religious tradition, and the tree in the cloister today is a descendant, not the original. Access is unusual: the tree is in a private cloister, viewed through a hole in the basilica portico wall. Included for the strong association and the well-known peephole ritual, with the legend labelled as such.
  - **Villa Borghese planes, Villa Borghese leccio, Pamphili cedar, Villa Sciarra ginkgos, Pincio pines, Villa Celimontana Aleppo pine**: all flagged mainly because the exact coordinates of a specific specimen inside a large park are approximate and need on-the-ground confirmation. The Pincio pines and (to a degree) the Quercia del Tasso are treated as ensembles/associations rather than one measured trunk.
  - **Ombú of the Campidoglio**: planting date is early 1900s (most sources say 1911, 50th anniversary of Italian unity, in memory of emigrants to Argentina); some accounts mention more than one Odescalchi ombú nearby, so I specified the one on the Cordonata by the Cola di Rienzo statue.
- Species names kept canonical per hard rule 9: "Oriental Plane (Platanus orientalis)" (deliberately distinct from London Plane), "Ombú (Phytolacca dioica)" spelled to match Lisbon's so the two group on a future species page, "Holm Oak (Quercus ilex)" for the two lecci, "Ginkgo (Ginkgo biloba)" matching Lisbon.
- 0 photos this run. Wikimedia Commons was unreachable (both WebFetch and direct curl returned 403 via the egress proxy), so rather than guess a URL or license I left all 10 photos `missing`. A photo pass is the obvious follow-up once Commons is reachable; Rome's monumental trees are very well photographed under open licenses, so this should be a rich harvest.
- Trees deliberately dropped: the big "Cedro di Villa Torlonia" that tops several "monumental trees" lists is in **Frascati**, a separate comune ~20 km outside the city, not Rome proper, so it was excluded to avoid a location error. The legendary **Ficus Ruminalis** (Romulus and Remus) no longer exists and was excluded. A ~2,000-year-old olive sometimes attached to "Rome" appears to sit outside the city and could not be pinned to a public in-city location.
- Superlative check: the only superlative is the city-level "oldest tree in Rome," framed carefully ("by tradition") and not in conflict with other published city pages.
- Suggested follow-up for a future pass with direct site access: the official Roma Capitale / Regione Lazio monumental-tree registers (PDF and the ilregistrodeglialberi.it entries) were blocked (403) this run and would give exact GPS and circumference/age for most of these, resolving the coordinate and age flags.

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
