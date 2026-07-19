# CURATION — items awaiting Hidde's review

Newest entries on top. When you approve a city, its status moves to `curated` and each tree to `hidde_approved`.

## 2026-07-19 — Species pages (new Contract F, blueprint v1.1)

- Blueprint bumped to v1.1 with your approval: new Contract F for species pages, a semi-automated browse facet. Auto-generated tree list, hand-written intro, publish-gated at 3+ trees plus an intro so nothing thin ships.
- Live now: /species index, /species/london-plane (5 trees, 3 cities), /species/caucasian-wingnut (3 trees, Amsterdam). Each tree page links to its species page; "Species" added to the top nav.
- NEEDS YOUR APPROVAL: the two species intros (data/species/london-plane.json, caucasian-wingnut.json), freshly written in the Paris style.
- Data-quality note for a future pass: London's oaks are split across two labels, "Pedunculate Oak" (2) and "English Oak" (2), which are the same species (Quercus robur). Normalising them to one label would unlock an oak species page (4 trees). Left as-is for now to avoid a risky auto-merge.
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
