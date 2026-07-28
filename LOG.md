# LOG

What the autonomous runs did, newest first. One entry per run that actually changed something. Hidde reads this to catch up, and says good or bad.

Format, deliberately short:

```
## 2026-07-27 — Assumption audit, on Hidde's parting instruction ("denk na of er meer van dit soort nergens op gebaseerde aannames in je instructies staan")

The trigger: the "no tracking" promise turned out to be an assumption copied from a Polarsteps teardown that Polarsteps itself does not live by (they run cookies and Mixpanel). Audited CLAUDE.md, PRINCIPLES.md, COMPETITION.md, GO_TO_MARKET.md for the same shape: claims hardened into rules without evidence or without Hidde's decision.

**Corrected on my own authority (each is Hidde's own later ruling, or a verified fact, catching up with older text):**
- CLAUDE.md header no longer states "2 trees free per city, €19,99/year" as the model; it now points at the recorded "interim paywall line is still undecided", which had contradicted it for days.
- Mandate goal 2 no longer hardcodes "a few thousand euro a month"; Hidde called that loose talk on 2026-07-26 and parked it. Direction stays, amount undecided.
- Rung 6's queue rationale no longer cites week-one Search Console country data as evidence (noise-level, per Hidde's volume-honesty ruling); the language-match argument stands alone.
- PRINCIPLES.md #7 rewritten: the durable privacy promise is no ads, no ad-tracking, no data sale, which is what Polarsteps actually promises; cookieless counting is in per Hidde's same-day ruling.

**FOR HIDDE, four judgment calls found by the audit, none urgent:**
1. **The queue formula "tourist footfall times tree-oldness decides" is unfalsifiable.** It justified UK-first and Japan-first within 24 hours, which means it decides nothing. Recommendation: replace it with the rule Japan now has: every coverage wave gets a demand scan before building. Say yes and a run rewrites the sentence.
2. **"Using MonumentalTrees is miserable, that is the entire opening"** is the foundational positioning claim and has never been tested with a user. Probably true, cheap to sanity-check someday (five people, one task). Flagging for awareness, not action.
3. **PRINCIPLES #4 claims Polarsteps "is criticised for" its signup wall**: secondhand, unverified. Worth softening to "forces account creation before value" (verifiable) unless a source exists.
4. **PRINCIPLES #5 states sharing-as-growth-loop as law**; there is zero evidence yet. It is a good hypothesis and the flywheel will test it; suggest labelling it as hypothesis so a future run doesn't build on it as fact.

Pattern to name, for future runs and sessions: the failure mode is never the observation ("Polarsteps sells privacy"), it is the silent promotion from observation to rule without a source or an owner decision in between. When adopting anything from a teardown, read the competitor's own source first; when recording a rule, record whose decision it was.

## YYYY-MM-DD HH:MM — what it did in one line
- What changed (files, pages, cities)
- Why, if it was a judgement call
- FOR HIDDE: only when something genuinely needs him. Otherwise leave it out.
```

If an entry has no `FOR HIDDE` line, nothing is waiting on you. That is the normal case.

---

# Open with Hidde

Standing list. Everything else in this file is history; this block is what is actually waiting. Refreshed 2026-07-27.

### Nothing right now
The three items this list used to carry are all resolved: the budget ceiling is recorded in CLAUDE.md hard rule 5, the design pass shipped (Direction A, Gabarito, mark 3A, live as of this evening's session), and collections publish without approval since blueprint v1.3. The last mandatory gate you sat in is gone, exactly as you designed it.

## 2026-07-28 — Istanbul: one pin genuinely upgraded (Ahtapot Çınar), five stay honest, one untried government domain flagged

- Same session. Istanbul is the furthest-behind of the eight lead cities on the depth-exit-test bar, so it got a pin-focused pass alongside today's photo work. One real upgrade: **ist_002, The Ahtapot Çınar**, moved from approximate to confirmed. OpenStreetMap carries a node named "Yatık Çınar", which is the tree's own registry name, matching this entry's own already-cited source (dogadakiler.com titles its page "Yatik-Cinar-Anit-Agac"); two independent sources naming the same tree the same way, about 47m from the old pin. Full honesty note, including that the OSM node itself has no survey provenance, is in the tree's data and in CURATION.md.
- The other five approximate pins (ist_001, ist_004, ist_007, ist_008, ist_009) stay approximate. Each dead end is a real source that knows the tree but doesn't hand over a coordinate: two of anitagac.istanbul's own detail pages confirm the right registry entry by name but load coordinates via client-side JavaScript this session's fetch tools can't execute, not an absence of data, just current unreachability. Full per-tree detail in CURATION.md so a future pass doesn't retry the same five searches.
- Istanbul now at 5/10 approximate (from 6), 2/10 photos (unchanged, this was pin work).
- Followed up with a photo-only pass on Istanbul's 8 gaps using the same Wikidata SPARQL technique that worked for Rome and Barcelona: genuine dead end across all 8, because unlike those two cities, none of Istanbul's trees have their own Wikidata item at all for the query to find. Recording so a future pass doesn't expect the Rome/Barcelona result here. One open (not dead) thread: ist_004 has two CC-BY iNaturalist photos nearby, not yet confirmed as the specific tree. Full detail in CURATION.md. No data changed.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-28 — Amsterdam's photo gaps tried with the same new technique: still exhausted, but two real leads found blocked by auth, not by absence

- Same session as the entry below. Applied the Wikidata SPARQL geo-query technique that worked for Rome and Barcelona to Amsterdam's three remaining gaps (Heimanseik, Vondelpark Poplar, Amstelkade Olive Willow); no result, these are now genuinely exhausted dead ends across a wide range of techniques over many sessions.
- Two things worth knowing rather than re-discovering: Amsterdam released ~800,000 of its own Mapillary panoramas as open CC-BY-SA data, which would plausibly cover both a park-path tree and a street tree, but Mapillary needs an API token this session doesn't have. Wikimedia's Commons structured-data query endpoint now requires OAuth login even to read, blocking one more technique. Neither is a dead end, both are a credentials problem for whoever next wants to spend a session on Amsterdam's last three photos.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-28 — Two real photo leads found (Rome, Barcelona) via a new technique, held back one step short of published

Visitors: 65 visits, 99 page views over 7 days (21-27 July: 8, 9, 10, 7, 4, 10, 17), the strongest closing day yet.

- No reader submissions, site healthy, nothing published found wrong. Depth-exit-test bar still not met: Amsterdam 7/10 photos, Lisbon 6/10, Rome 6/10, Barcelona 7/10, Istanbul 2/10 photos and 6 approximate pins. Amsterdam's own gaps are confirmed dead ends across many prior passes, so this run targeted Rome, Lisbon and Barcelona, the next-closest to the floor, with a genuinely new technique: Wikidata SPARQL geo-queries for images tagged near each tree, instead of re-running the Wikimedia/iNaturalist/Flickr/Openverse searches already exhausted on these gaps.
- **Two real candidates found**, both well-sourced on paper: Rome's Ginkgo of Villa Sciarra (rom_001), via Rome's own official monumental-tree register on Wikidata, exact address match, CC BY-SA 4.0 photo from Wiki Loves Monuments Italia 2021. Barcelona's Holm Oak of Carrer de l'Encarnacio (bcn_001), a CC BY-SA 4.0 photo of the public garden built around the tree, confirmed as the right site by a companion photo showing "SALVEM L'ALZINA" graffiti, the exact campaign this tree's own story already names.
- **Neither is marked `approved`.** This run's tooling could not fetch or render image files directly, so I could not personally view either photo to confirm it actually shows the tree rather than just the right site, the same gap a run flagged yesterday evening. Both are recorded as `found_needs_check` with the URL, licence and attribution already filled in, so the only work left is looking at two images. Lisbon's four remaining gaps and Rome/Barcelona's other three stay genuine dead ends, full detail in CURATION.md.
- FOR HIDDE, only if you're passing a phone or laptop near this anyway: two photos are one look away from clearing Rome and Barcelona's floors. `data/cities/rome.json` tree `rom_001` and `data/cities/barcelona.json` tree `bcn_001`, both `photo.status: "found_needs_check"`. If the image matches the tree, flip that field to `"approved"`. Not blocking, a future run will keep trying too.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Kyoto's Hosen-in pine gets a photo; Naples, Florence, Barcelona photo dead ends closed out with new techniques

Visitors: 64 visits, 98 page views over 7 days (21-27 July: 8, 9, 10, 7, 4, 10, 16), a new high for a single day.

- Rung 0/0b/3 checks first: no reader submissions (CSV still header row only), site healthy at session start, and a fresh news search for fallen/felled trees turned up nothing matching a tree this site actually publishes.
- Checked the depth-exit-test bar directly: still short on Amsterdam (7/10 photos), Lisbon (6/10), Rome (6/10) and Istanbul (2/10 photos, 6 approx). All four have had many genuine dead-end passes today already across Wikimedia, iNaturalist, Flickr, Openverse and national registries, so rather than re-run identical searches, spent this pass on cities with a genuinely untried angle instead.
- **Naples (worst photo coverage on the site, 1/10)**: closed out the two techniques an earlier pass today flagged as worth trying but hadn't. Campania's own regional monumental-trees register turned out to have photos for six of the eight remaining trees, but its licence is a bespoke non-commercial "Copyfree" term, not open, so it's a dead end for photos (a good coordinate/fact source, not a photo source). Wiki Loves Monuments Italia has nothing Naples-tree-specific. One close call at the Sant'Andrea delle Dame cloister (two genuinely open-licensed Commons photos) correctly not approved: both are dominated by the cloister's palms, with only a small, unidentifiable sliver of another tree in frame, not confidently the registered holm oak. Naples stays at 1/10.
- **Florence (4/10 photos)**: same two techniques tried on its remaining 6 gaps. Tuscany's own RAMI registry has photos for five of the six trees, same non-open licence problem. One near miss: intoscana.it has a photo of the Cedar Above Pegasus itself, but the page carries no licence statement at all, so it's unusable by default. Florence stays at 4/10.
- **Kyoto (6/10 photos) got a real find**: famous named temple trees are often much better photographed than ordinary park trees, and it paid off once. The Five-Needle Pine of Hosen-in now has an approved photo, Commons file "宝泉院_01.JPG", CC BY-SA 3.0 (Maechan0360), viewed directly: the temple's own signature framed-garden shot, an unambiguous match. Kyoto now at 7/10. Two more candidates (Daigo-ji's and Kamigamo's famous weeping cherries) are real, correctly-licensed photos of the right temple, but neither temple has just one named cherry and neither caption ties the photo to this project's specific named tree, so both stay honestly unapproved rather than guessed; a future pass with a source naming the specific tree in either photo could close these.
- **Barcelona's Silk Tree of the Ciutadella (bcn_008)** got its first dedicated individual photo search since it replaced the old La Rambla ensemble; confirmed real via Barcelona's own municipal tree catalogue, but no open-licensed photo exists. Barcelona stays at 7/10.
- Full per-tree detail (sources tried, exact rejection reasons) in CURATION.md so none of this gets re-tried expecting a different result.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Dead-tree sweep: both confirmed carcasses replaced, plus a second one found in Dublin, plus a real redirect bug fixed

Visitors: 63 visits, 97 page views over 7 days (21-27 July: 8, 9, 10, 7, 4, 10, 15), the strongest closing day of the week.

- Ran the dead-tree sweep the CURATION.md entry from earlier today set up. Both entries Hidde had flagged CONFIRMED dead got real living replacements, same ids so nothing changes shape underneath them: **Queen Elizabeth's Oak** (fallen 1991, Greenwich) is now **The Sweet Chestnut of Greenwich Park**, one of ~50 survivors of Charles II's own 1660s tree-planting scheme and individually recognised as a Great Tree of London. **Stock im Eisen** (a nailed dead trunk behind glass in Vienna since ~1440) is now **The Ginkgo of the Schubert Monument**, planted around 1900 in Stadtpark and protected as Naturdenkmal Nr. 569 since 1973.
- Checking Dublin's four suspects from the sweep list turned up a real second violation nobody had flagged: **The Sculpted Cypress** was a genuinely dead 200-year-old Monterey cypress carved into art after it died, the identical failure shape as Stock im Eisen. Replaced with **The Many-Trunked Holm Oak of St Anne's Park**, an oddly multi-trunked specimen GPS-located via a government heritage-tree dataset. Dublin's other three suspects (Hungry Tree, Addison's Walk, Champion Planes) are all genuinely alive.
- **A real bug found while doing this carefully**: renaming a tree changes its public URL (the site derives URLs from tree names, not ids), so the "same id, no URL breaks" reasoning that was supposed to justify these swaps was only half true. Checked whether the swap this reasoning was modelled on, Barcelona's bcn_008 from yesterday, actually held up: it didn't. Its old URL has been quietly 404ing for a full day. Fixed properly this time: added a small redirect list to `build_site.py` and populated it for all four renames done to date, including the retroactive Barcelona fix. All four now redirect correctly.
- Continued past Dublin and checked every remaining suspect across all 25 other flagged cities in the same session, since each turned out to be a fast read once viewed directly (the suspect list was built from a keyword scan for death-adjacent words, and almost every hit was a false positive: a war, a felled neighbour, a cemetery, a dead king, none of it about the entry's own tree). **One more real violation found: Rome's Quercia del Tasso.** Its own story had already hedged without saying so plainly; Italian coverage of a 2025 exhibition on the tree confirms it is now dead wood propped in a wall on the Gianicolo. Replaced with **The Ginkgo of Villa Sciarra**, planted around 1900 by an American diplomat, one of Rome's ~20 official monumental trees. Also had to pull it from the "Ancient Oaks of Europe" collection, which a ginkgo doesn't belong in.
- Everything else checked out clean. One borderline case worth watching rather than fixing: Berlin's Bellevue Oak is alive but its own story already says "this is not a thriving tree, it is a dying one" under active conservation care. Passes the rule as written; flagged in CURATION.md in case it doesn't for much longer.
- **The dead-tree sweep Hidde's rule set up is now fully closed.** All 64 flagged items checked; four real violations found across the whole site (Queen Elizabeth's Oak, Stock im Eisen, the Sculpted Cypress, the Quercia del Tasso), all four replaced with living trees, same ids, working redirects. Nothing left to sweep.
- With every content rung satisfied, moved to the product lane (PRODUCT_TODO.md). **Item 3, the copy audit, checked clean**: ran its own done-when greps against a fresh 516-page build, zero hits on every banned claim and tone word. **Item 4's remaining slate closed out where honest**: shipped a seventh collection, **Trees That Outlived Their City** (7 trees that survived fire, war or revolution destroying what stood around them: Sensoji's firebombed ginkgo, the Cheapside Plane, two more Tokyo shrine survivors, two Tiergarten/Bellevue Berlin trees, the Buffon Plane), grounded entirely in this site's own already-verified stories. Left "Trees Older Than 1000 Years" explicitly unbuilt: only 3 trees on the whole site clear 1000 years on a conservative estimate, short of the 4+ the idea's own trigger wants, and the two Athens olives that would pad the count to 5 both have a conservative low end (300 and 700 years) nowhere near 1000 despite an eye-catching high end. Padding would be exactly the number-chasing hard rule 8 exists to prevent, so it stays queued until a fourth city earns its way in honestly.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — The interim identity shipped: Direction A, Gabarito, the 3A oak, live

- Hidde's own "live" landed minutes after the entry below was written: `scripts/build_site.py` now carries the new identity for real (Gabarito as the single type family in place of the three-font mix, Direction A's palette, mark 3A in the top bar and as favicon, emphasis via weight and colour only). Confirmed directly in this checkout, not just described secondhand.
- This closes the "Open with Hidde" item the entries below were still carrying as open; refreshed that section to say so.

## 2026-07-27 — Session with Hidde: interim identity chosen, top-10 city trips settled, Japan queued, live analytics wired

- **Design pass delivered in session**: three full direction boards, then six logo variants; Hidde chose Direction A ("Growth Rings": Gabarito as the single family, warmed paper/pine/moss palette, gold accent) with mark 3A, the broad painterly oak, explicitly as an interim identity ("ooit vernieuwen met een echte designer"). Applied to the generator: one type family everywhere (Instrument Serif, Plus Jakarta and Shantell Sans removed), emphasis via weight and colour, 3A in the top bar and as SVG favicon. Built, all contracts green, 511 pages. Shipped live minutes later, see the entry above.
- **Top 10 tree city trips of Europe** researched (3 agents + clustering analysis of all 33 live cities), walk-weighted at Hidde's direction, Europe-scoped; ranking and leads in CURATION.md. Palermo, Cadiz and Sintra approved as new city pages (targeted exception in CLAUDE.md rung 6).
- **Japan wave queued** ahead of UK dense, gated on a pre-wave demand scan; grounds in GO_TO_MARKET.md, deliberately not built on week-one metrics after Hidde called that out.
- **Daily data digest live end-to-end**: DATA.md, written 05:15 UTC daily. Search Console reads via OAuth (Hidde authorised in session after Google blocked service-account keys); Cloudflare section stays honestly zero because the domain never routed through Cloudflare (nameserver move attempted, DNSSEC/TransIP walls, parked). First real entry verified in CI.
- **Money rule** replaced the €50 ceiling: no spending without Hidde's approval, no fixed ceiling otherwise, condition: start earning.

## 2026-07-27 — LOG.md's format example accidentally contained a real entry; moved it into the actual log

- Found while reading LOG.md to catch up before this run's own work: the session entry above (identity/Japan/digest) was sitting inside the fenced code block meant only to illustrate the entry format, ahead of even the "Open with Hidde" section. A real, dated entry with its own FOR HIDDE line, in the one place a future run's careless read (or Hidde's own skim) would treat it as instructional example text rather than actual history and easily miss it.
- Moved it out to a normal dated entry in the newest-first list and restored the format block to just the placeholder. Minutes later Hidde's own "live" push made the FOR HIDDE flag moot; see the entry above.

## 2026-07-27 — A photo-hunting pass with a new source (Openverse's API): Barcelona, Florence and one Micheli Yew, one Venice dead end confirmed twice over

- Visitors: 58 visits, 91 page views over 7 days (21-27 July: 8, 9, 10, 7, 4, 10, 10), a real uptick from yesterday's flat run of low-single-digit closing days. No submissions (CSV still header row only). Site built clean at the start, nothing published found wrong.
- Checked the depth-exit-test bar directly from the data rather than trusting memory: Amsterdam 7/10 photos (0 approx), Lisbon 6/10 (0), Rome 7/10 (0), Barcelona 6/10 (0), Tokyo 8/10 (1), Paris 8/10 (0), London 10/10 (2), Istanbul 2/10 (6 approx), still furthest behind. Every remaining photo gap on these cities had already had multiple dead-end passes today across Wikimedia, iNaturalist, Flickr and general search, so rather than re-run the same searches, queried Openverse's API directly (federates Flickr/Wikimedia/other open repositories with server-side licence filtering), a technique not yet tried in dedicated form today. Extended the same technique to Florence and Venice once the exit-test cities were exhausted.
- **Barcelona's Magnolia of the Maternity Gardens (bcn_007) gets a photo**: two CC BY-SA 2.0 Flickr photos by Josep Trepat Font, titled in Catalan with the tree's own name. Viewed directly before approving: a magnolia in white bloom against the Modernista hospital building the story describes, matching the entry's June-July `best_time` too. Barcelona now at 7/10 photos.
- **Florence's Micheli Yew (flo_001) gets a photo too**: CC BY-SA 2.5, captioned with the tree's own garden and species, viewed directly to confirm the dense dark crown the story describes. Florence now at 4/10 photos. A near-miss on the same city worth recording: a Pegasus statue by the same sculptor named in the Cedar Above Pegasus entry (flo_008) turned up, but viewing it directly showed an open lawn with no cedar and no walled terrace, and its own file date (1852-53) doesn't match this entry's 1865, a second statue by the same sculptor elsewhere in the Boboli Gardens. Correctly left unused.
- **Venice's Cypresses of San Michele Cemetery (ven_002)** got the same candidate an earlier pass today had already rejected (a magnolia-and-statues courtyard shot with cypresses only at the frame edges), reached independently through Commons category browsing rather than Openverse itself. Viewing it again reproduces the same rejection, useful as confirmation. Venice stays 4/10.
- Everything else tried this pass (Rome's remaining 3, Barcelona's other 3, Lisbon's 4, Amsterdam's 3, Istanbul's 8, Florence's other 5, Venice's other 4) stayed a genuine dead end, several near-misses caught and correctly not used (non-commercial licenses on an Orto Botanico shot and a Labyrinth cedar, a wrong Certosa/San Lazzaro/Forte Marghera search). Full detail in CURATION.md so a future pass doesn't retry Openverse on these same trees expecting a different result.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — A third collections pass: the great planes of Europe

- One more item 4 pass. Of the 43 plane trees across the site, picked ten with the most distinctive individual stories, one per city, deliberately avoiding the three planes already anchoring today's other new collections (Istanbul's Bahçeköy plane, Prague's Beethoven Plane and Rome's Adonis all already appear in "The Oldest Tree in Every Country We Map") so the two pages don't read as reruns of each other.
- **The Great Planes of Europe**: Dublin's Hungry Tree (swallowing a Victorian bench), Vienna's Mozart-Platane, Paris's Buffon Plane, Brussels' Oriental Plane of Parc Leopold, Bologna's Oriental Plane of Piazza Malpighi, Naples' Platano of San Severino (regrown from a felled root since 1959), Milan's Platano di Indro, London's Cheapside Plane, Amsterdam's Leidsebosje Planes (floated sideways on rafts in 1925 rather than felled), and Verona's Plane Tree of Piazza Indipendenza. Every entry grounded in this project's own already-verified story text, nothing new researched. A script confirmed all 10 resolve to a real Platanus tree with no accidental duplicates against the other 7 collections beyond the single expected overlap (London's Cheapside Plane, already in the original 10-tree collection, same as several other cross-collection overlaps already on the site). 8 public collections now.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — The same collection-link bug was on city pages too, fixed the same way

- While checking whether the question-page fix from the previous entry had a twin elsewhere, found one: `build_city_page`'s "More like this" line had the identical `collections[0]` bug, live on the actual built output. Tokyo and Amsterdam's city pages both claimed "Several of these trees also appear in Europe's Ancient Oaks You Can Actually Visit", false for both, since neither city has an oak in that collection.
- Fixed the same way as the question-page bug: filters to collections that actually include one of the city's own trees, and now states the real count ("One of these trees" vs "N of these trees") instead of a blanket "Several". Verified by hand across five built city pages (Tokyo now correctly points at the ginkgo collection, Amsterdam and Naples each correctly say "One of these trees", Paris says "5 of these trees" matching its actual count in the 400-years collection, Berlin says "2" matching its oak collection count).
- Also dropped an unused `collections` parameter from `build_tree_page`, found while tracing the bug: it was threaded through the whole call chain but never read inside the function. No output change, confirmed by an identical page count before and after.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — A second collections pass: the oldest tree in every country we map

- Continued the product lane straight after the last entry; depth work stayed at today's exhausted state (confirmed again on Istanbul specifically, see below), so time went to another item 4 pass rather than a sixth re-try of the same dead ends.
- **The Oldest Tree in Every Country We Map**, drafted and published directly: one entry per country, the single oldest verified tree this site has in each of the 15 countries it currently covers. Mechanically derived (a script picked the max `age_max` per country, cross-checked against every entry's own already-published age framing so disputed ones stay honestly disputed, e.g. Athens' olive keeps its 300-2,500 year range rather than the eye-catching 2,500 figure alone). All 15 kept rather than trimmed to the usual 5-12: the title promises "every country," so cutting any would break the promise the collection makes. A script confirmed all 15 entries resolve to a real tree in the right country with no duplicates before publishing. 7 public collections now, up from 6.
- **Istanbul's remaining 6 approximate pins and 8 photo gaps got one more delegated pass**, independent of today's earlier registry work: same anitagaclar.gov.tr/anitagac.istanbul licensing dead end confirmed from a fresh angle (no explicit reuse licence stated anywhere on either site, silence isn't a licence), and one new candidate source (konusanagac.com, İBB's own "talking trees" site, which has an entry naming the Beykoz Çayırı plane) turned out to be DNS-dead, not merely unlicensed. No data changed; Istanbul stays at 2/10 photos, 6/10 approximate. Recording this so a future pass doesn't retry the same two leads expecting a different result.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — A real bug fixed: question pages linked the same collection to every city regardless of relevance, plus two more collections

- Visitors: 0 visits recorded this week (scripts/visitors.py returned an empty window, 2026-07-20 to 2026-07-27). No submissions (CSV still header row only).
- Checked the depth-exit-test cities directly, same as every pass today: Amsterdam (7/10 photos, 0 approx), Rome, Barcelona and Istanbul (2/10 photos, 6 approx) are all still at today's earlier exhausted dead ends. Lisbon got one genuine new photo this pass (below). The bar stays unmet; today's many passes have made this a stable, not-worth-relitigating state, so time went to product work instead.
- **Lisbon's Tipu of Jardim de São Bento (lis_005) gets a photo**: two CC BY-SA 4.0 angles on Wikimedia Commons, by the same photographer, tied to the tree's own Portuguese name and garden. Lisbon now at 6/10. Its other four gaps and Amsterdam's three stay confirmed dead ends after another honest attempt each; full detail in CURATION.md.
- **A real bug, found while reading a built question page rather than just its contract pass**: every city's "oldest tree" question page linked the same hardcoded collection (`ancient-oaks-of-europe`, first alphabetically) with the same hardcoded sentence naming "the yew, the oaks", regardless of whether that city had a single tree in it. Tokyo and Amsterdam's pages, for instance, both claimed their oldest tree's "peers" were collected among Europe's oaks, which is false for both. `build_question_page` was picking `collections[0]` unconditionally instead of checking which collections actually include the city. Fixed: it now filters to collections containing one of the city's own trees, uses a generic sentence that fits any collection, and falls back to the honest generic `/collections` link when none apply (as it always did for cities in no collection). Verified directly on the built output: 23 city question pages now link a genuinely relevant collection, 10 fall back honestly, and Tokyo's/Naples's pages check out by hand as sane. This closes PRODUCT_TODO item 6 completely (the city-page half shipped earlier today).
- **Two more collections drafted from PRODUCT_TODO item 4's slate**, published directly per the no-approval regime (no `needs_curation` step, unlike this morning's two): **Europe's Most Remarkable Yews** (8 yews, 7 cities, full inclusion of every yew on the site, Taxus baccata, oldest to youngest from London's Totteridge Yew down to Madrid's three-trunked specimen) and **Wisteria and Blossom Worth a Spring Trip** (11 trees, 9 cities, every entry already carrying a real sourced spring `best_time`, ordered by bloom month from Seville's February orange blossom to May's chestnut avenues). Both grounded entirely in this project's own already-verified tree data; nothing new researched. A script check confirmed every listed tree exists with the claimed species/best_time property before publishing. 6 public collections now, up from 4.
- Also corrected a stale CURATION.md note: the two collections drafted this morning were flagged NEEDS YOUR APPROVAL there, but LOG.md's own "Open with Hidde" list already recorded that regime as gone; they'd been flipped to published and are live. CURATION.md just hadn't caught up. Nothing collection-related is waiting on you.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Two collection drafts (oaks first, as promised), plus a real bug: collections were never actually gated behind your approval

- Visitors: 52 visits, 81 page views over 7 days (21-27 July: 8, 9, 10, 7, 4, 10, 4), flat, in line with the week's pattern. No submissions (CSV still header row only).
- Checked the depth-exit-test cities directly: Amsterdam (7/10 photos), Lisbon (5/10), Rome (7/10), Barcelona (6/10) each have had multiple exhaustive photo-only dead-end passes today already (Wikimedia geosearch, iNaturalist, Flickr, Openverse, direct image viewing); Istanbul (2/10 photos, 6 approximate) had a thorough registry pass today too. Every marquee-Europe city has had at least one depth pass today as well. Re-running identical searches would be the "looping forever" the mandate warns against, so moved to the product lane (rung 7).
- Drafted two collections from the slate item 3 above promised ("ancient oaks first"): **Europe's Ancient Oaks You Can Actually Visit** (9 oaks, 7 cities: Berlin, Munich, London, Brussels, Rome, Madrid, Barcelona) and **The Ginkgos Worth a November Trip** (10 ginkgos, 9 cities, all with a real, sourced `best_time` in autumn). Every entry grounded in this project's own already-verified data, nothing new researched. Both saved as `needs_curation` per Contract D.
- **NEEDS YOUR APPROVAL** (full detail in CURATION.md): both new collections above.
- **A real bug found while wiring the second one in**: the two collections shipped earlier (Europe's 10 Most Remarkable Ancient Trees; Trees Older Than 400 Years) were still `needs_curation` and, on checking the actual generated site, were fully public anyway, linked from the homepage, every city page and every question page, and present in the sitemap. Contract D says a draft is "nothing linked publicly until Hidde approves"; the build script never enforced that, so both have been live and indexable since they shipped without you ever saying yes.
- Fixed it in `scripts/build_site.py`: collections now split into public (status not `needs_curation`) and draft. Only public ones feed the homepage, city pages, question pages and the `/collections` index and its sitemap entry. Drafts still get a real page at a stable URL, so you or a future run can read them, but noindexed and excluded from the sitemap and every internal link, the same pattern already used for the account prototype. Question and city pages that lose their collection link now fall back to a generic, honest link to `/collections` instead, so no page drops below its contract minimum.
- **Net effect**: `/collections` currently shows an honest "none public yet" note, and all four collections (2 old, 2 new) sit unlinked pending your review. If you're happy with either of the two that were already live, flip its `status` to anything other than `needs_curation` (`curated`, matching how city approval already works) and the next rebuild republishes it, sitemap and all. That is a one-word, fully reversible change either way.
- FOR HIDDE: four collection drafts are waiting on your yes/no, two brand new (oaks, ginkgos) and two that turn out to have been public without you ever approving them (most remarkable trees; 400+ years). Read CURATION.md's latest entries; approving is exactly as cheap as it's always been meant to be, a status flip.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — City pages now link species pages where 3+ trees share one, PRODUCT_TODO item 6 (half)

- Contract F already had every tree page link its own species page; the other half of item 6, city pages linking a species page when 3+ of their own trees share it, was never built. Added it to `build_city_page`: counts species per city, links any with 3+ members and a qualifying species page, in a new "Species on this list" line above the collection link.
- Five cities cleared the 3+ bar with a species page already published: Amsterdam (Caucasian Wingnut), Berlin and Munich (Pedunculate Oak), London and Prague (London Plane). Verified by grepping the built HTML directly rather than assuming: exactly these five city pages now carry the link, and all five hrefs resolve (`validate_internal_links` passed).
- Question pages' and city pages' collection link now falls back to a generic `/collections` link when no public collection exists yet (both currently in that state, see the entry above); this was necessary to keep question pages above their 3-link contract minimum once the collection link could no longer be assumed present.
- Left undone for a future pass: item 6's other half, "question pages should link a relevant collection where one exists," is already true when one exists, but none currently do (all four are drafts pending your review above).
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Seasonality completion pass: 10 trees get an honest `best_time`, PRODUCT_TODO item 5 done

- Continued the product lane after the collections/gating work above. Wrote a count script per PRODUCT_TODO item 5's own done-when: every ginkgo, wisteria, wingnut, horse chestnut and magnolia should carry `best_time`; no evergreen should. It found 10 showpiece-species trees across 9 cities missing the field (mostly ginkgos that never got one when their siblings elsewhere did) and 0 real evergreen violations (the script's first pass flagged 2 bald cypresses, Milan's Il Sacerdote and Seville's Cypress of the Glorieta de Bécquer, but Taxodium distichum is genuinely deciduous, one of the few conifers that drops its needles, so their existing autumn best_time entries are correct, not a bug).
- Filled all 10, grounded in each tree's own story text where it already stated a season (Kyoto's inverted ginkgo, Lisbon's Praça Paiva Couceiro ginkgo, Barcelona's magnolia, both already describing their own bloom or colour) and in well documented genus-wide facts applied consistently across the site otherwise (ginkgo's uniform November gold; horse chestnut's May candle flowers; wingnut's summer fruit chains, the exact example CLAUDE.md itself gives). One judgement call: Vienna's Twin Giants pairs a ginkgo with an evergreen sequoia under one protection order; gave it a best_time that names only the ginkgo half turning gold, rather than implying the whole entry peaks, honest to the mixed-species reality the entry's own species field already states.
- Count script now shows 0 missing among qualifying species and 0 real evergreens with the field. Full list in CURATION.md is unnecessary here since nothing was flagged or uncertain; every addition is grounded in existing verified data, and none required new research.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Bologna: 2 more pins confirmed, one a real 550m cemetery-address error

- Continued after Malaga. Bologna's remaining 6 approximate pins had already had three passes today and yesterday using Italy's national/regional tree registries, so tried OSM tree nodes and named cemetery features instead, the technique that just worked for Malaga.
- The Himalayan Cedar of Villa Ghigi resolved cleanly via an OSM node carrying its own MASAF registry reference and a Commons category naming Bologna specifically, closing a Vallerano-mixup risk this entry had already flagged. The Cypress of Carducci's Tomb turned out to have a real bug, not just imprecision: its pin was the cemetery's main-gate address, 550m from the poet's actual grave, which has its own precisely sourced Wikidata coordinate this entry's already-cited sources already tie the tree to directly.
- Two more (Piazza Minghetti's plane, the Botanical Garden's ginkgo) got real OSM matches but stayed honestly `approximate`, since neither node is individually named or registry-linked to the specific tree. Two stay genuinely unresolved (the Montagnola's plane ensemble, the San Michele in Bosco camphor).
- Bologna now at 3/10 approximate pins (from 6). Photos unchanged.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Malaga: 5 of 10 approximate pins resolved, its pin dimension untouched since original research

- Continued after New York. Nearly every below-floor city had already had a same-day depth pass except Malaga's pins specifically (its photos had a dead-end pass today, but pins had never been worked at all since original research), and three of its ten trees sat on one shared garden-centroid coordinate, an obvious sign at least two were wrong.
- OpenStreetMap turned out to carry individually species-tagged tree nodes inside La Concepcion garden and Parque de Malaga, the same technique that has paid off in several other cities this week. Fixed: the Hackberry of the Cypress Cottage (370m, an exact species match 8m from an independent geocode of the building it's named for), the Rare Cassia of Malaga Park (160m, a rare-species exact match), El Barrilito (confirmed via a fountain named after the tree's own nickname, no coordinate change needed), the Fig of the Picasso Gardens (55m, via a sculpture two sources date and place exactly), and the school avocado (6m, via its building footprint).
- The Tallest Araucaria in the Province got a real but partial fix: no tree node exists for it, but the garden's own page places it beside a waterfall, of which the garden has two about 50m apart; pinned to their midpoint and kept honestly `approximate` rather than guessing which one, but it's no longer sharing an identical coordinate with two other trees.
- Two stay genuinely unresolved (the Transplanted Olive, the Native Oak of Malaga Park): no source placed either more precisely than the garden/park already on file, and Andalucia's own regional singular-tree catalogue explicitly excludes cultivated garden specimens like the olive.
- Malaga now at 5/10 approximate pins (from 10). Photos unchanged at 3/10.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — New York: the Clove Lakes Colossus pin corrected 1.5km via NYC's own open tree dataset

- Visitors: 51 visits, 80 page views over 7 days (21-27 July: 8, 9, 10, 7, 4, 10, 3), flat, in line with the week's pattern. No submissions (CSV still header row only). Nothing published found wrong; build was clean at the start.
- Checked the depth-exit-test cities directly first: Amsterdam, Lisbon, Rome and Barcelona have each had exhaustive photo-only dead-end passes today; Istanbul had a thorough registry/GIS pin pass today too. Moved to New York next per rung 5's oldest-first order, since same-day work there turned out thinner than assumed.
- Delegated a fresh research pass across New York's 6 approximate pins and 7 missing photos. Most of it reconfirmed today's earlier photo dead ends (nothing licence-clean and tree-identifiable on Wikimedia, iNaturalist or Flickr; a promising Wikimedia "Tupelo Meadow" photo pair was viewed directly and turned out to be a generic wide shot, correctly rejected). One real find: NYC Open Data's Forestry Tree Points dataset (not tried by today's earlier OSM-based pass) has exactly one tulip tree citywide with a 93-inch trunk diameter, an exact match to the Clove Lakes Colossus's own reported circumference, independently corroborated by an iNaturalist observation 10m away and sitting right at Clove Lakes Park's actual mapped northern boundary. Moved the pin 1.5km and set `confirmed`.
- New York now at 5/10 approximate pins (from 6). Photos stay at 3/10, genuinely exhausted today.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Munich: all 9 remaining approximate pins fixed at once, via its own tree-protection law

- Checked Munich's real numbers directly instead of trusting an old log line, and found it was actually at 9 of 10 approximate pins, its worst dimension by far given 8/10 photos already approved. All nine are named, individually law-protected trees, so this was worth real effort rather than an honest structural limit.
- The fix came from a source already cited on every one of these entries without anyone having pulled its coordinates before: German Wikipedia's list of Munich's legally protected Naturdenkmal trees. Two entries returned suspiciously similar coordinates at first glance, which could have meant a copy-paste error in that table. Checked it two different ways before trusting it: geocoding one tree's own street address independently, and separately following a written direction ("200m northwest of the Monopteros temple") from one of this project's own approved photo captions. Both checks landed within 100m of what the table said, which was enough to trust it and also revealed the *old* stored pins were the actual errors, off by as much as 1.6km in a few cases.
- Moved and confirmed all nine. Munich is now the first Naturdenkmal-heavy city on this site with zero approximate pins.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Naples: a pin confirmed via its neighbours in the same cloister; Barcelona and Milan's remaining gaps checked, no change needed

- Barcelona's four remaining photo gaps (already dead ends from yesterday) got one more fresh iNaturalist pass: a near-miss CC0 photo of the right species turned up 390m away, but Barcelona has around 1,100 of these trees citywide, so proximity alone isn't enough to call it the same specific catalogued specimen. Correctly left unused.
- Milan's one still-pending photo (the Ginkgo of Brera) got a direct look using the image-viewing trick from the Rome pass: confirms what an earlier, more cautious pass already suspected, an ambiguous shot that can't be confidently called a ginkgo by eye, from a casual-grade observation with no community confirmation. Left unresolved rather than approved on weak evidence.
- Naples got a real fix: Campania's regional government registry doesn't have an entry for the Holm Oak of Sant'Andrea delle Dame itself, but it does have two for the palms and camphor sharing its exact cloister, both pointing to the same spot, about 45m from this project's own pin. Good enough to confirm the location. One tempting registry match for a different camphor tree in the same garden was checked and correctly rejected: the circumference figures didn't agree closely enough to be confident it's the same tree.
- Naples now at 2/10 approximate pins (from 3).
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Rome: Adonis finally gets a photo, via a workaround for images this session couldn't otherwise view

- Continued to Rome after Istanbul. Its four remaining photo gaps had all been tried hard before; one, the Twin Planes of the Eleven Fountains, was stuck specifically because an earlier pass found a plausible photo but couldn't open it to check what was actually in frame.
- Found a workaround worth remembering for future runs: fetching a raw image URL through WebFetch fails to produce a text description, but it does save the image to a local file, which the Read tool can then open and view directly. Used it to finally settle the Twin Planes candidate (a stone urn, not the trees, correctly rejected) and, more usefully, to confirm a 2009 photo of a large hollow-trunked oriental plane in Villa Borghese's plane grove as a genuine match for Adonis's own described hollow trunk, even though the file doesn't name Adonis specifically among the grove's nine survivors. Approved as an honest illustration of the tree and its grove, same standard as other ensemble photos already live on the site.
- The other two gaps (the Cork Oak of the Orangery, the Aleppo Pine of Celimontana) stay genuine dead ends: fresh iNaturalist queries filtered server-side to open licences only, at both trees' exact registry coordinates, came back empty or non-open.
- Rome now at 7/10 photos (from 6).
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Istanbul: two more pins tightened to individual age-matched trees, Beykoz Çayırı upgraded to confirmed

- Visitors: 50 visits, 79 page views over 7 days (21-27 July: 8, 9, 10, 7, 4, 10, 2), flat, in line with the pattern this whole week. No submissions (CSV still header row only). Nothing published found wrong; build was clean at the start.
- Re-tried Amsterdam's three photo gaps and Lisbon's five first, per rung 5's order, since both are close to the depth-exit-test photo floor: fresh Dutch/Portuguese-language searches, Wikimedia geosearch and direct iNaturalist API queries confirmed the same dead ends many prior passes have already recorded rather than finding anything new. Moved to Istanbul, which has real untried ground on both dimensions.
- Pushed further into the national monumental-tree GIS layer a prior pass found earlier today (turkiye_anit_agaclari), this time pulling actual per-tree coordinates instead of just campus/farm/park anchors. Two Bahçeköy pins (the Oldest Plane, the Ahtapot Çınar) moved 1.9km and 500m respectively to individually registered trees whose ages match this project's own sourced figures almost exactly (1,382 vs "1,300-1,400"; 579 vs "up to 580"). Both stay `approximate` rather than `confirmed`: the registry mislabels both records' species as a plane hybrid too young a lineage to reach that age, most likely a data error in the registry rather than a reason to doubt the tree, but a real discrepancy worth being honest about rather than papering over.
- One pin had no such conflict: the Plane Trees of Beykoz Çayırı matched three individually registered trees on species, count and age all at once, no caveat needed. Moved 260m to their centroid and upgraded to `confirmed`.
- Checked the registry's own photo links properly rather than just noting they're sometimes dead: they resolve to anitagaclar.gov.tr, an official government domain whose general terms restrict reuse to personal/informational use, not an open licence. Correctly left unused, same as monumentaltrees.com. Fresh photo hunts (Wikimedia, iNaturalist API, general web) on Istanbul's 8 remaining gaps found nothing usable.
- Istanbul now at 6/10 approximate pins (from 7) and 2/10 photos (unchanged).
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Istanbul: found the real data behind its monument-tree registry, 4 pins meaningfully tightened

- Istanbul has been the furthest-behind of the eight lead cities all day. Past runs kept hitting anitagac.istanbul's map as an unreadable JavaScript wall. Traced it back to what actually powers it: a public ArcGIS Online feature service covering all of Turkey's monumental trees, directly queryable over a normal API. Used it (plus OpenStreetMap and direct geocoding) to move four pins closer to the truth: the Oldest Plane of Bahçeköy (~1.3km, to the real forestry-faculty campus), the Ahtapot Çınar (~1.2km, to the farm its own address already names), the Plane Trees of Beykoz Çayırı (~1km, to a meadow two independent sources now agree on) and the Ata Fıstık Çamı (~170m, tightened on a matching age record).
- One dead end worth flagging so nobody chases it again: the same registry's photo links looked promising, but the domain behind a third of them has expired and now redirects to an unrelated gambling site. Not a licensing problem, the links are simply gone.
- A fifth fix on a follow-up look: the Cypresses of Karacaahmet, already an honest nine-tree ensemble entry, got real independent confirmation, exactly 8 individually protected cypresses clustered within 300m of the existing pin, close enough to move it to `confirmed`.
- Istanbul now at 7/10 approximate pins (from 8). Photos (2/10) untouched this pass; pins were the win today.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Verona: a new registry source confirms the Piazza Indipendenza plane's pin exactly

- Continued to Verona after Antwerp. Found a new source (ilregistrodeglialberi.it, a per-tree registry aggregator, unlike the unreliable spreadsheet a prior pass had already flagged) that gives GPS coordinates for the Plane Tree of Piazza Indipendenza matching this entry's own circumference and height figures exactly. Refined the pin about 30m and set `confirmed`. Two more entries (a second Himalayan cedar, a cypress and mulberry that plausibly match existing ensemble entries) were checked on the same source and correctly left alone: either a real mismatch or no coordinates published.
- Verona now at 6/8 approximate pins (from 7). Photos untouched, still 2/8.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Antwerp: a real 800m pin fix on a national record-holding poplar; four photo gaps stayed honest dead ends

- Visitors: 49 visits, 78 page views over 7 days (21-27 July: 8, 9, 10, 7, 4, 10, 1), flat. No submissions (CSV still header row only).
- Checked the depth-exit-test count directly: Amsterdam (7/10 photos, 0 approx), Lisbon (5/10, 0), Istanbul (2/10, 8 approx) and Rome (6/10, 0) all still short of the 8-photo floor, each already tried hard many times today by earlier runs; a fresh pass on Amsterdam's three photo gaps and Istanbul's two anitagac.istanbul-sourced pins confirmed rather than changed those findings, so moved on rather than re-loop.
- **Antwerp got a real fix**: the Canadian Poplar of Eric Sasselaan, among the tallest trees recorded in the city, had its pin about 800m from the actual street. The Flanders heritage inventory has the exact object (measurements match precisely) but its map is JS-rendered and unreadable this session; geocoded the street itself instead and matched it to OpenStreetMap's own road geometry, which curves through the old fortress moat exactly as the source describes. Moved, stays honestly `approximate` since this is a street anchor, not a surveyed trunk point.
- Tried hard on Antwerp's four remaining photo gaps (two national champion trees in Hertoghepark, Middelheim's cut-leaf horse chestnut, the Stadspark millennium ginkgo) and the zoo's historic grounds entry: viewed every promising candidate directly rather than trusting a filename or caption, and rejected all of them honestly (a general park-fence photo, an ordinary chestnut with the wrong leaf shape, a licence that doesn't qualify, and a striking zoo gate photo that just isn't a photo of the tree cover the story is about). Antwerp stays at 5/10 photos, now 6/10 approximate (from 7).
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Brussels: a fourth wrong-location pin found today, the Chêne Joséphine off by 1.5km

- Same technique, same result: the Chêne Joséphine's own already-cited source (woodwideweb.be, ID 1139, specifically about this tree) states its own GPS reading, 1.5km from where this project had it pinned, an apparent slip from an early research pass rather than honest vagueness. Cross-checked independently against Nominatim's geocode of the park itself, which agrees within 70m. Moved and confirmed. Fourth genuinely-wrong pin found today (Athens, Vienna, Madrid, now Brussels) and the largest error of the four, which makes the "check each entry against its own cited source" pass feel less like a coincidence and more like a real, underused check.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Madrid: a third wrong-location pin found today (Trillo Holm Oak, 600m off), one more tightened

- The Holm Oak of the Trillo Roundabout was pinned from a converted DMS reading that turned out to be 600m from the real tree. An OpenStreetMap node individually named "Encina del Trillo," tagged as a regional natural monument with an exact crown-diameter match to this entry's own story, gave the real position. Moved and confirmed. This is the third genuinely-wrong (not just imprecise) pin caught today, after Athens and Vienna, worth a FOR HIDDE note: it may be worth a dedicated systematic pass cross-checking DMS-converted and third-party-sourced pins across the older cities, rather than finding these one at a time as depth work happens to reach each city.
- Also tightened the Himalayan Cedar of the Crystal Palace's pin about 160m to the Palacio de Cristal building itself.
- Noting for whichever run picks this up next rather than flagging for Hidde (this is ours to decide and act on): three genuinely-wrong pins turning up in one day just from incidental depth passes suggests a dedicated sweep, re-checking every approximate/DMS-derived pin against its own already-cited sources city by city, would likely pay for itself. Reversible, no contract change needed, a good candidate for a future run with room to spare.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Porto: 3 pins tightened off a shared whole-garden estimate to their actual buildings

- Four Palácio de Cristal entries were all sitting on the exact same coordinates, a whole-garden centroid, even though two name a specific building. Geocoded Casa Tait and Quinta da Macieirinha independently and moved three entries (the Magnolia, the Camellias, the Plane) to their real buildings, 140-150m each. They stay `approximate` rather than `confirmed`, since Porto's own classified-trees register doesn't cover them yet (still under formal review), so this is a tighter estimate, not a survey. Six photo gaps tried hard, all genuine dead ends (all-rights-reserved or CC BY-NC only).
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Seville: a pin corrected via a newly-found OSM technique (named glorietas), one photo confirmed by eye

- Moved to Seville next (5/10 photos, 7/10 approximate, never touched by a depth pass). New lead: Parque de María Luisa's many named clearings (glorietas) are individually mapped in OpenStreetMap. Matched and moved the Fig of the Glorieta de Goya's pin about 190m to the named feature, and found a Commons photo whose own caption ("gran ficus en el centro") and content are an unambiguous match, approved. Two other glorieta-named entries checked against the same rich OSM coverage came up genuinely absent, left alone rather than guessed.
- Seville now at 6/10 photos (from 5) and 6/10 approximate (from 7).
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Prague: one pin independently confirmed via Wikidata, one photo lead checked and correctly rejected

- Kept applying the technique that just paid off twice on Athens and Vienna: check each remaining approximate pin against whatever source the entry already cites. Prague's Field Maple of the Seminary Garden already cited a Wikidata item about this specific tree; its raw coordinate data matches the stored pin almost exactly, so this one gets upgraded to `confirmed` rather than corrected. Neruda's Pear Tree has no such source and stays honestly approximate.
- Also chased Neruda's Pear Tree's missing photo: one Commons candidate looked promising by filename (mentions "Nerudy") but turned out, once viewed directly, to be a generic playground photo, the filename referring to the adjacent street rather than this tree. Correctly not used. Prague stays at 9/10 photos.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Vienna: another wrong-location pin fixed (Ginkgo of Schönbrunn, 700m off), sourced from the city's own monument register

- Checked Vienna since it was already close to done (10/10 photos, 2/10 approximate). One of the two remaining approximate pins, the Ginkgo of Schönbrunn, turned out to be a genuine location error rather than honest vagueness: the entry's own already-cited source, Vienna's official Naturdenkmal register (published as a Wikipedia table), gives this specific protected tree (Nr. 110, matching on every fact: 1781 import, oldest ginkgo in Austria, protected since 1939) its own coordinates in Schönbrunn's Botanical Garden, about 700m from where this project had it pinned near the Wagenburg. Moved the pin and corrected the story/transport text to match. Vienna now at 10/10 photos and 1/10 approximate (a genuine ~4.5km avenue, the only remaining one).
- Re-tried Berlin's one remaining photo gap (Steinlanke Oak) with three fresh techniques (OSM, iNaturalist, Commons geosearch); all confirm the earlier finding rather than change it, no open-licensed photo exists for this specific remote tree. Left as is rather than loop on it again.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Athens: a real wrong-location bug caught, Kaisariani Monastery's pin was 3.6km off

- Caught while sanity-checking the rest of Athens' approximate pins right after the pass below, rather than moving straight to the next city. The Trees of Kaisariani Monastery (ath_010) was pinned nowhere near the actual monastery, off by roughly 3.6km. Three independent sources (Wikipedia's own coordinates, Nominatim, an individually-named OpenStreetMap building) agree within metres on the real position; moved the pin there. This is a "something published is wrong" fix, not depth polish: the old pin would have sent someone up the wrong side of Mount Hymettus. The story and transport directions were already correct, so this was a pure coordinate bug, not a research error.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Athens: 2 approximate pins resolved to confirmed, 2 photos found and viewed by eye

- Visitors: 48 visits, 77 page views over 7 days, flat (21-26 July: 8, 9, 10, 7, 4, 9). No submissions (CSV still header row only).
- Continued rung 5's marquee-Europe order. Amsterdam/Lisbon/Rome/Barcelona (photos only) and Istanbul (both) have each had many exhaustive dead-end passes today already; moved instead to Athens, which had only ever had a photo-only pass, its 10/10 approximate pins never actually attempted.
- Found real, previously untried ground: OpenStreetMap carries individually named nodes for two of Athens' single-specimen olives, the Sacred Olive of the Acropolis ("Holy olive tree", tagged `sacred_tree`) and the Olive Tree of Pisistratus ("Ελιά Πεισίστρατου", its own Greek name, tagged `tourism=attraction`). Moved both pins to confirmed (90m and 60m respectively), and could view Commons photos for both by eye this session: the Acropolis olive's photo confirmed the pin and also caught a small standing error, the story said "north side" of the Erechtheion when the tree actually stands in the Pandroseion on the temple's west side, now corrected. The Pisistratus olive's photo shows the tree's own on-site sign legible in frame, an unambiguous match, and got approved as a new photo.
- Also approved a public-domain courtyard photo for the Trees of Kaisariani Monastery (ensemble entry). Three other photo/pin gaps tried hard and stayed genuine dead ends (Plato's Academy's regrowth olive, the Transplanted Olive, the Holm Oak; full detail in CURATION.md, including why one tempting Plato's Academy photo was correctly rejected for showing the site rather than the specific tree).
- Athens now at 7/10 photos (from 5) and 8/10 approximate pins (from 10).
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Dublin: a second pin corrected, the Provost's Plane moved to Trinity's own stated address

- Continued straight on from the Sculpted Cypress fix below with the same "does a real named place match the story's own address" check on Dublin's other approximate pins. Trinity College's own published page states the Provost's Plane stands in "the Provost's Courtyard at No. 1 Grafton Street," and OpenStreetMap has the Provost's House building individually named at exactly that address. Moved the pin about 260m from a loose campus-area guess to the building itself, kept `approximate` since the tree is in the walled courtyard behind it, not at the front door.
- Checked two more Dublin approximate pins (Corkagh Park's Oak Avenue, Farmleigh's Great Sycamore) for the same kind of fix; neither has an individually mapped feature to anchor a tighter pin, correctly left alone.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Dublin: a real pin/story fix on the Sculpted Cypress; a thorough dead-end pass on Istanbul, Edinburgh and Dublin's national tree register

- Visitors: 48 visits, 77 page views over 7 days (21-26 July: 8, 9, 10, 7, 4, 9), flat. No submissions (CSV still header row only). Site healthy, nothing published was wrong at the start of this pass.
- This session could view images directly (fetch, then read the saved file), so used it to re-check the one outstanding pending photo site-wide (Milan's Ginkgo of Brera) and to finally look at leads several prior passes could only find, not view. Full detail in CURATION.md; short version: Istanbul's Çengelköy Plane photo lead is now a confirmed dead end (viewed all 7 candidate photos directly, none show the tree), and Küçük Çamlıca's named pine trees in OpenStreetMap are real but don't include the specific one this project needs (Ata Fıstık Çamı).
- **One real fix, not just a dead end**: Dublin's Sculpted Cypress (dub_007) had a genuine bug sitting in the data. A previous run's own verification note already knew, from the photo's Commons caption, that the sculpture stands at "the junction of Watermill Road and James Larkin Road," but the entry's story and address text still said "Clontarf Road," a road that doesn't actually meet Watermill Road anywhere near there, and the pin was never moved to match. Verified the correct junction independently via OpenStreetMap's own road geometry (it ends within 35m of the separately-mapped Bull Island Causeway, matching the same caption's "opposite Bull Island Causeway" detail) and fixed the story, address and pin, a real 700m correction.
- Istanbul's photo count stays at 2/10 (this pass closed a lead rather than opening one); Edinburgh and Dublin's other approximate pins stayed unchanged, tried hard via OpenStreetMap and Dublin City Council's own open tree dataset but none confirmable enough to change without guessing.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Florence and Naples: dead-end photo pass on both

- Continued rung 5's order after Bologna. Both cities have unusually low photo coverage (Florence 3/10, Naples 1/10) but every fresh Commons/iNaturalist search for their remaining named specimens came back empty this pass, a broader gap than a single missed search. No data changed; full list of what was tried is in CURATION.md so a future pass doesn't repeat it blind.

## 2026-07-27 — Bologna: 1 more pin corrected via Italy's national monumental tree registry

- Continued rung 5's order after Malaga. The Sequoia of the Giardini Margherita's own RAMI registry entry gives an identical 37.40m height and 5.20m circumference to this project's own sourced figures, a clean match; moved about 110m. Bologna now at 6/10 approximate pins (from 7). Two other gaps tried, stayed genuine dead ends.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Malaga: dead-end pass, one tempting photo caught and rejected

- Continued rung 5's order after Granada. Malaga's 7 photo gaps got a fresh try; one real candidate (La Concepcion's tallest araucaria) turned up but couldn't be pinned to the specific record tree among several in frame, the same problem that sank a Milan candidate earlier tonight, so not used. The other six gaps stayed genuine dead ends. No data changed; detail in CURATION.md.

## 2026-07-27 — Granada: dead-end pass, nothing usable found

- Continued rung 5's oldest-first order after Valencia. Granada was already flagged from original research as photo-poor; this pass tried fresh Commons/iNaturalist searches with image-viewing available and a new regional Andalusian tree inventory, all confirmed dead ends (the inventory only covers non-urban land, nowhere near Granada city). No data changed; full detail in CURATION.md so a future pass doesn't retry the same ground.

## 2026-07-27 — Valencia: 3 pins corrected via the region's own monumental-tree catalogue

- Continued rung 5's oldest-first order after Nice, to Valencia, untouched since original research (2/10 photos, 10/10 approximate). Photo hunting came up empty this pass, a genuine dead end.
- Found a real, previously untried source: the Generalitat Valenciana runs a live, queryable ArcGIS layer of its legally protected monumental trees, many entries carrying the tree's own popular name. Matched and moved three: El Titan (the Ficus del Parterre, ~400m, exact name match), the Olive Tree of La Rambleta (~1.1km, the only olive in the entire city dataset, age matching this entry's own figure), and the Eucalyptus of Benimamet (~790m, exact name and height match).
- Caught one near-miss before applying it: a catalogue entry sitting 40m from the Ripalda ficus's pin was tempting but named after a different historic palace entirely (Palacio de Raga, not Palacio de Ripalda); left alone rather than misapplied.
- Valencia now at 7/10 approximate pins (from 10). Photos still 2/10.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Nice: 6 photos found and confirmed by eye, reaching the 8-photo floor

- Continued rung 5's oldest-first order after Munich. Nice was at 2/10 photos; its 9/10 approximate pins are structural (island/garden ensembles like Venice, not a search gap).
- With image-viewing available this session, found and directly confirmed six photos: Matisse's Olive Tree (the grave's own inscription visible, tree canopy overhead), Jardin Albert 1er, the Aleppo Pine Forest of Mont Boron, Parc Vigier's palm row, the Promenade des Anglais's palms, and Villa Masséna's formal garden. One candidate for the Colline du Château grove was viewed and rejected (wrong subject, no relevant trees), so that single gap stays open.
- **Nice now at 8/10 photos, clearing the depth-exit-test floor.**
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Visual check on this session's photo backlog: Munich clears the 8-photo floor, three false matches caught

- This session could view images after all (a capability that comes and goes, per earlier notes), so rather than leave tonight's found_needs_check photos for a future run, checked every one by eye.
- Four confirmed and approved: Lyon's Pin de Bunge, Munich's Röth-Linde/Dörfchen oak/Oskar-von-Miller-Ring hackberries, and Venice's Giardini della Biennale. **Munich now stands at 8/10 photos, clearing the depth-exit-test floor.**
- Three rejected as false matches once actually viewed, all previously held on strong text/location matches alone: Milan's Il Sacerdote candidate showed multiple cypress trunks together (can't confirm it's the specific named one), Venice's San Michele candidate showed a magnolia and statues in a cloister (nothing like the cypress waterfront described), and Kyoto's Five-Needle Pine candidate (pending since an earlier pass today) turned out to be a photo of a Japanese maple at night, not a pine. All three reverted to missing.
- Worth flagging plainly: this is now several instances of a "strong textual match" (exact caption, exact coordinates) turning out wrong on an actual look. The found_needs_check status is doing real work catching these; a future run without image-viewing tools should keep using it rather than approving on metadata alone.
- Milan's Ginkgo of Brera photo stays at found_needs_check: viewable but genuinely ambiguous from its upward angle, not a clear enough species check either way.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Munich: 3 photo candidates found via the city's own Naturdenkmal register, pending visual check

- Continued rung 5's oldest-first order after Venice. Munich already met the pin bar (2/10 approximate); photos stood at 5/10.
- Munich's official list of protected trees links a Wikimedia Commons file for many entries directly, so this pass used the register itself rather than searching blind: found named, well-licensed candidates for the Röth-Linde, the Oak of the Dörfchen (Nymphenburg) and the Hackberries of Oskar-von-Miller-Ring. All three are held at `found_needs_check` since this session's tools couldn't open the images to confirm by eye, despite the strong textual match (the register's own linked file, explicitly captioned with the tree's name).
- Also cross-checked the Röth-Linde's pin against OpenStreetMap: a node tagged with its exact name sits within 5m of this project's own coordinates, confirming the pin was already right. A similar check on the Krüner Eiche found only an untagged nearby node, not usable as confirmation.
- If the three pending photos are confirmed by a future run with image-viewing tools, Munich clears the 8-photo depth-exit-test floor.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Venice: 2 photo candidates found, pending a visual check a future run should finish

- Continued rung 5's oldest-first order after Milan. Venice's 10/10 approximate pins are structural, not a search gap: every entry is an island, garden or fortress ensemble rather than a single named tree, so there is no trunk to pin more precisely than "this garden." Photos were the real gap, 3/10.
- Found two candidates, both held at `found_needs_check`: a CC BY-SA garden view of the Giardini della Biennale's own bridge, and a CC BY-SA Flickr-sourced view of San Michele cemetery island (likely showing the cypress-ringed approach the story describes, though the caption doesn't name cypresses explicitly). Neither could be viewed directly this session to confirm by eye.
- Five other photo gaps (San Lazzaro's cedar, the Certosa poplar, Villa Groggia's hackberries, San Servolo's olive, Forte Marghera) stayed genuine dead ends after real search.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Milan: 2 photo candidates found, pending a visual check a future run should finish

- Continued rung 5's oldest-first order after Lyon. Milan already met the pin-precision bar (2/10 approximate) but sat at 5/10 photos, needing 3 more.
- Found two strong candidates, both geotagged within metres of this project's own coordinates: a CC BY-SA Commons close-up of a bald cypress at Giardini Indro Montanelli (Il Sacerdote, mil_001) and a CC BY iNaturalist photo at the Orto Botanico di Brera (the ginkgo pair, mil_004). Both held at `found_needs_check` rather than approved: this session's tools couldn't open the image files to view them directly, and the cypress especially needs an eyes-on check since several cypresses share that stretch of water and the close-up doesn't itself prove it's the tallest, named one.
- Two remaining gaps (the Trotter oak, the Madonnina paulownia) stayed genuine dead ends, consistent with their access-restricted or self-seeded nature already on record.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Lyon: the Pin de Bunge's pin corrected ~300m via a newly-found OpenStreetMap arboretum inventory

- Visitors: 48 visits, 77 page views over 7 days (21-26 July: 8, 9, 10, 7, 4, 9), flat. No submissions (CSV still header row only).
- Amsterdam, Lisbon, Rome, Barcelona and Istanbul's remaining photo gaps are exhaustively documented as dead ends across many passes today and this week; rather than repeat identical searches, moved down rung 5's order to Lyon, which had never had a depth pass since its original research (7/10 approximate pins, 1/10 photos, the most headroom of any untouched marquee-Europe city).
- Found real, previously untried ground: OpenStreetMap's mapping of Parc de la Tête d'Or's arboretum is an individually-surveyed inventory (620 tagged tree nodes with species and measurements), not the sparse coverage seen elsewhere. The Pin de Bunge's node carries `denotation=natural_monument` and `species:fr=Pin Bunge, Pin Napoléon`, an exact match on both this tree's formal name and the local nickname already in its story. Moved ~300m to the confirmed position. The same inventory independently corroborated (not corrected) the Bald Cypress and Osage Orange pins already marked confirmed, matching their sourced circumference figures almost exactly.
- One candidate photo found for the Pin de Bunge (CC BY, iNaturalist, Julien Lepage, ~15m from the confirmed node), held at `found_needs_check` since this session's tools could not view the image directly to confirm it by eye.
- Four other gaps (Parc de la Garde chestnut, Parc de la Chapelle cedar, Île Barbe cedar, Parc de Gerland pagoda tree) tried and either genuinely lack species data in OSM or, for Gerland, hit a repeated timeout rather than a confirmed dead end. Full detail in CURATION.md so a future pass doesn't repeat the same ground blind.
- Lyon now at 6 of 10 approximate pins (from 7). Photos unchanged at 1/10 approved.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — New York: 2 approximate pins confirmed via OpenStreetMap (Hangman's Elm, Camperdown Elm)

- Same technique as the Kyoto pass just below, applied to New York, which hadn't had a pin pass since its original research. Both of NYC's own "Great Trees" landmarks used in this project's data turned out to be individually mapped in OpenStreetMap under their exact names, with planting years that independently match this project's own age claims. New York now at 6 of 10 approximate pins, from 8.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Kyoto: 2 real pin errors corrected via OpenStreetMap, one new photo candidate found

- Visitors: 48 visits, 77 page views over 7 days, flat (21-26 July: 8, 9, 10, 7, 4, 9). No submissions.
- Amsterdam, Lisbon, Istanbul, Rome and Barcelona's remaining photo gaps are now genuinely exhausted across many prior passes (confirmed again with one fresh Amsterdam attempt this run, no new ground). Moved to Kyoto, next in rung 5's marquee-Europe order with real headroom left.
- The OpenStreetMap named-tree-node technique that worked for Tokyo/Barcelona/Amsterdam found two exact name matches: the Taiko Weeping Cherry of Daigo-ji (moved ~185m to its real spot) and the Emperor's Gift Cherry of Kamigamo (moved ~165m, corrected from a pin that was already marked confirmed but was actually wrong, the same pattern as Amsterdam's Amstelveld find). Kyoto now at 2 of 10 approximate pins, from 3.
- Also found a plausible photo for the Five-Needle Pine of Hosen-in (a CC BY 3.0 shot of the specific garden built to frame this one tree), held at found_needs_check rather than approved since this session couldn't open the image to look at it directly.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Seville: 2 pins resolved via a newly found city tree inventory

- Berlin (next in the marquee-Europe order) turned out to already be in great shape, 9/10 photos and 0 approximate, so moved straight to Seville (9/10 approximate). sevilla.org's own catalogue is still down, but found a different Seville Parks and Gardens dataset on ArcGIS Hub covering the whole city's managed trees. Matched El Gran Capitán (a giant eucalyptus, by being the only one of its species in its garden) and the Figs of Plaza del Cristo de Burgos (by matching the exact count of four transplanted figs the story already describes). Two more checked and correctly left alone (a scattered hackberry ensemble with no way to isolate the "centennial" ones; a camphor tree genuinely outside this inventory).
- Seville now at 7/10 approximate pins (from 9). Photos unchanged at 5/10.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Brussels: 3 more pins resolved, one a real 700m correction

- Same regional tree registry that worked for Brussels on 2026-07-26 (two pins that day) resolved three more: the Botanical Garden's black mulberry, the Cinquantenaire's chestnut avenue (moved to the actual cluster of 11 recorded trees), and the Abbaye de la Cambre's pagoda tree, whose new registry match's trunk girth (313cm) is a tight match for the entry's own sourced 308cm measurement, a real 700m correction rather than just tightening.
- Two checked and correctly left alone: the Chene Josephine's only nearby match in this registry is a much smaller oak, not the same tree; the Kasterlinde stands in Dilbeek, outside Brussels-Capital Region, so this Brussels-only registry was never going to cover it.
- Brussels now at 5/10 approximate pins (from 8). Photos unchanged at 4/10.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-27 — Three unverified photos actually confirmed by eye (Rome, Amsterdam, Dublin); a stale CLAUDE.md note fixed

- Visitors: 48 visits, 77 page views over 7 days, flat. No submissions.
- This session could download and view images directly, a capability that comes and goes across runs. Used it to clear every `found_needs_check` photo left on the site: Rome's Cedar of the Belvedere (unmistakably a Cedar of Lebanon, matches the exact-GPS registry match already made), Amsterdam's Cycad of the Hortus (two cycads facing each other, matching the story's own detail about a male-female pair grown opposite each other), and Dublin's Great Sycamore of Farmleigh (a single huge, fenced, ancient sycamore matching the file's own Farmleigh caption). All three approved. Rome now 6/10 photos, Amsterdam 7/10, Dublin 5/10.
- Re-hunted Dublin's other 4 photo gaps and Rome's Adonis; all genuine dead ends, matching several prior passes' findings. Not looping further on those.
- Fixed a stale instruction in CLAUDE.md: it still told runs to replace Barcelona's bcn_008 for failing the collectibility rule, but that replacement (the Silk Tree of the Ciutadella) already happened on 2026-07-26. Updated the note so a future run doesn't re-investigate something already done.
- Depth-exit-test still not met: Istanbul (2/10 photos, 8 approximate) remains furthest behind and untouched this pass, already exhaustively covered on 2026-07-26. Amsterdam and Rome are now the closest of the eight to clearing the photo floor, one photo short of Lisbon's old lead.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Brussels: the regional tree registry came back online, 2 more pins resolved

- Followed straight on from the Antwerp pass with the same technique. A lead flagged earlier today, Brussels' regional "arbres remarquables" register, was unreachable (connection refused); this pass found the site back up and traced through to the actual data service.
- Resolved the Giant Sequoia of Parc de Woluwe (a real 1.1km correction, not just tightening) and the Purple Beech of Parc Tournay-Solvay. Tried the Douglas Fir of the Hippodrome too but genuinely could not tell which of 4 near-identical specimens nearby was the named tree, so left it alone rather than guess.
- Brussels now at 8/10 approximate (from 10). Full detail in CURATION.md.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Antwerp: 4 pins resolved (one a real 1.1km error); a genuine news sweep found nothing wrong

- Visitors: 47 visits, 76 page views over 7 days, flat. No submissions. Depth-exit-test bar still not met (Amsterdam, Lisbon, Rome, Barcelona need photos only; Istanbul needs both and stays furthest behind), so coverage stays frozen.
- Spent real effort chasing Istanbul's, Amsterdam's and Rome's last few photo/pin gaps with techniques not tried before (direct image download to view the two candidate Çengelköy photos, Europeana, Wiki Loves Monuments Turkey, the Turkish government registry, the Taşlı Çınar's flagged OSM leads). All came back genuine dead ends: this session's Bash tooling blocks outbound network fetches (`curl`) entirely with no user available to approve them, so the one open photo-identity question at Çengelköy still can't be resolved by viewing the image; the OSM leads turned out to be personal Google Photos links, not usable media. Nothing wasted twice, full detail in CURATION.md so a future run doesn't retry the same six things.
- Antwerp got its first depth pass since research (was 10/10 approximate). Found the city's own public tree inventory (geodata.antwerpen.be) and matched 4 trees by species or trunk-size uniqueness: the Copper Beech of Sint-Willibrorduskerk (a real correction, the old pin was 1.1km from the actual church), the Black Locust and the Peace Tree of the Grote Markt (both tightened), plus one genuine near-miss caught and correctly rejected (a candidate poplar with less than half the sourced tree's trunk size). Antwerp now at 6/10 approximate (from 10).
- Ran a news sweep for anything published having fallen or died, across the 24 cities not already checked today. Nothing had. One tree worth watching: Verona's Cedar of Piazza Bra was at real risk of being felled in mid-2025 but was saved and stabilised by October 2025; still standing, no change made.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Bologna: 3 of 10 approximate pins resolved via Italy's national tree registry

- Continued from the dead-end sweep below with Bologna (10/10 approximate, untouched today). Italy's national monumental tree registry, already used successfully on Rome, Naples and Verona, matched three trees by species and exact locality name: the Himalayan Cedar of the Rizzoli (moved ~130m, a real correction), the Oriental Plane of Piazza Malpighi and the Ginkgo of Piazza Cavour (both moved 15-22m, essentially confirming the existing estimates). Every match was cross-checked across two independent fetches before being applied, after an earlier pass today found this exact spreadsheet format can misread adjacent rows; one candidate (the Piazza Minghetti plane) came back three different, contradictory ways and was left alone rather than guessed.
- Bologna now at 7 of 10 approximate pins. Full detail in CURATION.md.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — A dead-end sweep: six depth targets tried with new techniques, one real lead found but unreachable, nothing published was wrong

- Visitors: 47 visits, 76 page views over 7 days, flat (21-26 July: 8, 9, 10, 7, 4, 9). No submissions. Site healthy.
- Re-verified the depth-exit-test count from the data directly: Tokyo, Paris and London already clear the bar (8+ photos, 2 or fewer approximate pins). Amsterdam, Lisbon, Rome and Barcelona each need photos only (6-7 of 10); Istanbul remains furthest behind on both counts. Coverage stays frozen.
- Tried a genuinely new technique (Wikimedia Commons geosearch by exact coordinate, rather than category or text search) on Amsterdam's three photo gaps, Rome's Adonis, Barcelona's Silk Tree and Lisbon's ginkgo. It surfaced candidates nobody had found before, but reading each file's own description confirmed the same problem already flagged: none identify the specific named tree. No photo approved.
- Istanbul's Overpass API is reachable again (no more 504s) but returned nothing matching any of its 8 remaining trees; three OSM nodes near the Taşlı Çınar carry an unread `image` tag, worth a future pass once Overpass stops timing out on single-node lookups.
- Edinburgh's photo gaps are now genuinely exhausted across every technique available this session, including a first try of the UK's Woodland Trust Ancient Tree Inventory (a large national register, checked as CC-BY-NC so lead-list-only): none of its records sit anywhere near our ten named specimens.
- Brussels: found a real, promising lead, a CC-BY-licensed regional tree inventory covering all 19 municipalities (unlike the City-of-Brussels-only dataset already tried, which doesn't cover most of our ten trees at all), but its host, `geodata.environnement.brussels`, refused every connection this session. Worth a retry with different network tooling, this is a lead, not a dead end.
- Checked the news for anything published here that has actually fallen or died: found real 2026 tree-collapse stories elsewhere (Rome's Colosseum pines, a Venice oak, London's Whitewebbs Oak) but none match a tree on this site.
- No data files changed. Full detail in CURATION.md, written so the next run doesn't re-spend today's searches on the same six gaps.

## 2026-07-26 — Madrid: 6 of 10 approximate pins resolved by matching OpenStreetMap's mapping of the region's own singular-tree register

- Continued down rung 5's list to Madrid, untouched today (4/10 photos, 10/10 approximate). Nine of its ten trees are on the Comunidad de Madrid's official singular-tree catalogue, and volunteers have separately mapped that catalogue into OpenStreetMap as individually named nodes, name-matching this project's own tree names closely enough to trust.
- Six pins moved to confirmed this way, distances ranging from 90m to 530m from the previous estimates: the Ahuehuete of the Parterre, the Three-Trunked Yew of the Velazquez Palace (an exact name match to its own Spanish Wikipedia article), the Bald Cypresses of the Crystal Palace Pond, the Cypress and the Caucasian Elm of the Royal Botanic Garden, and the Grandfather Cedar of Parque del Oeste.
- Four gaps stayed open: two trees on the singular-tree list have no matching OSM node yet (Himalayan Cedar, Aleppo Pine), one already had a reasonably tight pin from a sourced DMS reading (Holm Oak of the Trillo Roundabout), and one isn't on the regional catalogue at all (Stone Pine of El Capricho).
- Madrid now at 4/10 approximate pins (from 10). Photos untried and unchanged at 4/10, a fresh Commons search on the newly pinned trees found nothing.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Amsterdam: found a real 550m location error hiding behind an "approximate" flag, both pins now confirmed

- Visitors: 47 visits, 76 page views over 7 days (21-26 July: 8, 9, 10, 7, 4, 9), flat. No submissions.
- The Amstelveld wingnuts pin wasn't just imprecise, it was wrong: about 550m from the real square, confirmed against Wikipedia's Amstelkerk coordinates and OpenStreetMap geocoding. That's why an earlier pass's municipal-registry search near the old pin came back empty of anything matching, it was searching the wrong neighbourhood. Re-ran the search at the corrected location and it resolved cleanly: exactly three Pterocarya fraxinifolia in the square are registry-tagged "Monument" with a shared 1930 planting date, distinct from the dozens planted in 1945 onward, matching the sources' account of "three oldest, most valuable specimens" given underground root protection in the 2006-2010 felling dispute. Pin moved there, age corrected to 96 years, confirmed.
- The Hortus cycad's pin was a general garden street address; moved it to the Palm House building itself using OpenStreetMap building data, a real precision gain even though the photo-identity question (which of several cycads in the glasshouse) stays open.
- Amsterdam now has 0 approximate pins, from 2. Photos unchanged at 6/10 after another exhaustive, unsuccessful hunt for the same 3 gaps a prior pass today already tried; not retrying those with the same tools again.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Naples: worst-covered city gets its first depth pass, 6 of 10 pins resolved

- Naples (0/10 photos, 10/10 approximate since its 2026-07-25 research, never touched since) got its first depth pass. Found a new source: Campania's regional monumental-tree register, which gives GPS for most of Capodimonte's catalogued trees. Its own photos carry no stated licence so none were usable, but exact circumference/height matching resolved 6 pins: the Royal Orchard camphor (moved ~900m), the yew, the Montezuma cypress, the citrus grove, the Villa Comunale plane and the San Severino cloister platano, which also picked up a photo via a Commons caption that explicitly names the tree.
- One real correction along the way: the Robust Eucalyptus's registry match had an exact dimension match but placed it at Giardino dei Principi, not "near Porta Grande" as previously written; corrected the location and story rather than force the old description.
- Two things flagged rather than guessed at: the Garden of the Princes camphor has a registry candidate with a conflicting circumference (830cm vs this entry's 670cm), left unresolved; and a secondhand, unverified note that the Eucalyptus might actually be a different species per the museum's own page, worth checking directly next time.
- Naples now at 3/10 approximate (from 10) and 1/10 photos (from 0). Full detail in CURATION.md.
- Site rebuilt, all contracts validated, pushed across four commits.

## 2026-07-26 — Barcelona: one photo found via a direct heritage-ID match

- Barcelona's pins were already all confirmed; the only bar left was photos (5/10). Found a direct match for the Casa de la Misericordia palms, a Commons photo whose own title names the exact courtyard and cites the trees' Catalan heritage protection ID, GPS landing 15m from the stored pin. Approved.
- The other three gaps (Holm Oak of Encarnacio, Himalayan Cedar of the Labyrinth, Magnolia of the Maternity Gardens, Silk Tree of the Ciutadella) stayed genuine dead ends after a fresh iNaturalist/Commons/municipal-site try; all four are well-documented named trees, just without any open-licensed photo found anywhere.
- Barcelona now at 6/10 photos (from 5). Still short of the depth-exit-test floor of 8/10.
- This finishes a pass over all 8 depth-exit-test cities today: Tokyo, Paris and London already passed; Amsterdam, Lisbon, Istanbul, Rome and Barcelona all improved but none newly cleared the bar. Pin work is now largely done across the group (only Amsterdam's 2 and Istanbul's 8 remain); photos are the harder remaining gap everywhere except Istanbul, which needs both.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Rome: both approximate pins resolved

- Two independently-photographed "Cedro del Libano" images at Villa Doria Pamphilj, by different photographers, agree on one exact GPS point that also matches Italy's national tree registry (MASAF) to the hundredth of an arcsecond. That point is 1.2km from the Belvedere cedar's old pin, a real correction, not just tightening; moved to confirmed, with the matching photo held at found_needs_check pending a future pass that can view images directly. The Cedar of Celimontana's pin was confirmed the same way, using its own already-approved photo's embedded GPS, corroborated by two more photos and the neighbouring pine's registry point.
- Rome now at 0/10 approximate (from 2). Photos stay at 5/10 (1 pending a visual check); the other 4 gaps retried and stayed genuine dead ends. Full detail in CURATION.md.
- Moving to the rest of the lead group next per rung 5's order (Tokyo, Paris, London and Barcelona already clear the exit-test bar; marquee Europe continues oldest-first from Dublin/Barcelona/Athens/Porto/Kyoto/Verona/Naples).
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Istanbul: no data changed, but two dead domains and one licensing trap identified

- Followed up rung 5's two untried leads on Istanbul, still furthest-behind of the eight priority cities (2/10 photos, 8/10 approximate). konusanagac.com is confirmed genuinely dead (NXDOMAIN, not a transient issue) and avrupaanitagaclar.com has been hijacked to a gambling redirect; both should stop being retried. anadoluanitagaclar.com is real and structured but 403-blocked to every fetch tried, worth another attempt with different tooling. Also caught a near-miss before it became a mistake: anitagac.istanbul's tree pages do have real photos in static HTML (not JS-only, as previously assumed) but the site states no reuse licence anywhere, so none of them are usable despite being easy to hotlink.
- No photo or pin changed on any of the 8 open gaps; all retried and rejected on licence, distance, or lack of an identifying feature. Full detail in CURATION.md.
- Moving to Rome next per rung 5's order.

## 2026-07-26 — Lisbon: both approximate pins resolved, clearing half the exit-test bar

- Found a new source, Portugal's national registry of classified public-interest trees (ICNF), and used it to resolve both of Lisbon's remaining approximate pins. The Avenida de Berlim nettle tree moved by about 900m to the registry's own point, and its age corrected from a tourism-site "100 years" to the registry's measured 75 years in 2015 (~86 today), a real conflict resolved in favour of the direct government survey. The Jardim Alfredo Keil paineira's existing pin was confirmed against the registry's own ensemble point, 2m away.
- Lisbon now at 0/10 approximate (from 2). Photos stay at 5/10; the Nettle Tree's photo hunt was retried at its corrected coordinates and stayed a dead end, the other 4 gaps unchanged from earlier today.
- Moving to Istanbul next per rung 5's order, the furthest-behind of the eight priority cities.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Amsterdam: Amstelveld gets a modern photo, three more gaps confirmed genuinely exhausted

- Visitors: 47 visits, 76 page views over 7 days, flat (21st-26th: 8, 9, 10, 7, 4, 9). No submissions (CSV still just the header row). Continued rung 5's ladder at the top: Amsterdam, the reference city, still short of flawless before this pass (6/10 photos, 2/10 approximate).
- Swapped the Amstelveld wingnuts' approved photo from a 1973 archival image to a 2022 CC0 photo of the same square, viewed and confirmed directly. Re-hunted the remaining 4 gaps (Heimanseik, Vondelpark poplar and Amstelkade olive willow photos; Hortus cycad and Amstelveld pin ambiguities) with fresh techniques and found nothing further usable; recorded each as a genuine dead end in CURATION.md rather than looped on, per the "hunt hard, then move on" rule.
- Amsterdam stays at 6/10 photos (1 pending an identity check) and 2/10 approximate. Moving to Lisbon next per rung 5's order.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Verona: 1 more pin resolved, and a tool reliability limit caught before it caused harm

- Followed up the Rome pass by trying the same Italian national monumental-tree registry on Verona, the worst-covered published city (8 of 8 approximate). Resolved the Ginkgo of Piazza Indipendenza to confirmed, matched with high confidence since the registry's own measurements are the exact figures already in this entry's story from an earlier pass.
- Worth flagging: tried the same technique on two more Verona trees and on Naples, and caught this session's spreadsheet-reading tool giving contradictory answers across repeat fetches of the same file when rows look similar. Did not use any of those results. No wrong pin shipped, but a future run relying on this same technique should cross-check any match against a second independent fetch before trusting it, the same discipline this pass used to keep the Ginkgo result but drop the rest.
- Verona now at 7 of 8 approximate pins (from 8).
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Paris clears the depth-exit-test bar: 2 photos found

- Moved to the rest of the lead group after Amsterdam, Lisbon, Istanbul and Rome (Istanbul and Rome yielded no changes this round, recorded in CURATION.md). Paris needed photos only (6/10, pins already all confirmed).
- Found and verified two: the Second Robinier, whose own Commons caption names this exact 1636 tree rather than just the species, and the Sequoia of Buttes-Chaumont, whose photo's embedded GPS lands 10m from the stored pin.
- Paris now at 8/10 photos and 0/10 approximate, meeting the depth-exit-test bar from CLAUDE.md rung 6 for this city. Six of the eight priority cities now need work: Amsterdam (6/10 photos), Lisbon (5/10), Istanbul (2/10, 8 approximate), Rome (5/10). Tokyo and London already met the bar earlier.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Dublin: a wrong species caught, 3 pins resolved via a new Irish source

- Continued marquee Europe oldest-first (Dublin, city 12, was the worst-pinned city touched today: 9/10 approximate). Found a genuinely new source, GBIF's "Heritage Trees of Ireland" dataset, a 2009 nationwide field GPS survey, and used it to resolve 3 pins.
- **A real correction, not just imprecision**: the Champion Planes of New Square were recorded as London Plane, but the survey independently identifies the pair as Oriental Plane, a call also visible all along in the tree's own already-approved photo's Commons filename. Corrected the species.
- Dublin now at 6/10 approximate (from 9) and 4/10 photos (1 held at found_needs_check pending an identity check on a plausible but not certain candidate). Full detail in CURATION.md.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Barcelona's La Rambla entry replaced with a genuinely singular tree

- CLAUDE.md itself flags that Barcelona's "Plane Trees of La Rambla" entry fails the project's own collectible-point rule, an avenue of 250 ordinary street trees rather than one tree or a compact ensemble, with an explicit instruction to replace it next time a run touched Barcelona. That was this pass.
- New entry, same slot and id (bcn_008) so no URL changes: **The Silk Tree of the Ciutadella**, an Albizia julibrissin in Parc de la Ciutadella, individually catalogued since 1996, planted around 1896. The species usually lives 30-50 years; this one is roughly 130, hollowed at the trunk by decades of infection the city's own register states plainly, and still flowers every July regardless. Verified against the municipal catalogue and an independent news source before writing.
- No photo found for the new entry yet, and Barcelona's other 4 photo gaps also stayed open this pass, genuine dead ends after a real try. Full detail in CURATION.md.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Lisbon: one photo found, five stayed genuine dead ends

- Continued rung 5 after Amsterdam. Lisbon needed photos (4/10, floor is 8+) more than pins (already 2/10 approximate). Found and verified a CC BY-SA 4.0 photo for the Santo Amaro olive trees, matched by its own description and a heritage reference number to the exact four trees the story describes.
- The other 5 gaps (Tipu of São Bento, Coral Trees of Jardim da Luz, Nettle Tree of Avenida de Berlim, Ginkgo of Praça Paiva Couceiro, Rubber Tree of Mouraria) stayed genuine dead ends after trying Portuguese Wikipedia, Wiki Loves Monuments categories, Flickr CC and dados.gov.pt's actual dataset API (it turns out to be a WFS/WMS geoservice with no CSV download, not previously confirmed). Two near-misses caught and correctly rejected: candidate Tipuana tipu photos on Commons and Flickr turned out to be different specimens at different Lisbon addresses.
- Lisbon now at 5/10 photos (from 4). Full detail in CURATION.md.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Amsterdam: a wrong pin corrected by 350m, one photo held back on identity doubt

- Visitors: 44 visits, 70 page views over 7 days, flat (21st-26th: 8, 9, 10, 7, 4, 6). No new submissions (CSV still just the header row). Site healthy, build clean. Continued rung 5's depth ladder at the top: Amsterdam, the reference city, still short of flawless.
- **The Amstelkade Olive Willow's pin was actually wrong, not just approximate**: it was geocoded from a street address and sat about 350m from the tree's real position. Amsterdam's own municipal tree registry, queried directly and cross-checked myself, carries exactly one Elaeagnus angustifolia on that stretch of Amstelkade, planted 1948, matching the story's 78-year age claim and "unique in the Netherlands" line exactly. Moved to confirmed. Also fixed its neighbourhood field, which named the wrong part of Amsterdam-Zuid.
- Found a plausible CC BY 2.0 photo for the Hortus cycad but could not confirm it shows the specific 300-year-old specimen rather than one of the Palm House's other cycads, so it stays at `found_needs_check` rather than approved, honest uncertainty over a tidier-looking city page.
- Checked the Vondelpark poplar's pin against the same registry: two candidate monumental poplars sit 30m apart with no way to tell which the sources mean, so left its existing address-based pin alone rather than guess.
- Amsterdam now at 6/10 photos (1 pending identity check) and 2/10 approximate (the Hortus cycad, and the Amstelveld wingnuts' honest ensemble pin). Full detail in CURATION.md.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Rome: 2 pins resolved via Italy's national monumental tree registry

- Visitors: 43 visits, 69 page views over 7 days, flat (2026-07-20 to 2026-07-26: 8, 9, 10, 7, 4, 5). No new submissions, CSV still just the header row.
- Followed rung 5's order from the top: Amsterdam, Lisbon and Istanbul all got a genuine fresh attempt with new techniques (Amsterdam's own "special trees" GeoJSON layer, Lisbon's Commons categories and Portugal's national tree register, Istanbul's anıtağaç site source) and all three stayed dead ends, mostly for tooling reasons (files too large to fetch in full, a JS-rendered map with no exposed API) rather than the data genuinely not existing. Worth another look with better fetch tools. Full detail in CURATION.md.
- **Rome** paid off: found Italy's national monumental tree registry (MASAF), a downloadable per-region spreadsheet with individual GPS coordinates for every officially registered monumental tree. Matched Adonis and the Aleppo Pine of Celimontana each to their own single registry entry at the exact named site, moving both from park-wide estimates to confirmed pins (290m and 210m corrections). One near miss caught and rejected: a registry tree at the Cedar of the Belvedere's exact site turned out to be a stone pine, not this tree's cedar of Lebanon, so that pin stays approximate rather than borrow the wrong tree's coordinates.
- Rome now at 2 of 10 approximate pins (from 4). Photos unchanged at 5/10; fresh iNaturalist checks at the newly precise coordinates found nothing openly licensed. This Italian government registry is untried on Florence, Milan, Venice, Verona, Naples and Bologna, worth a future pass.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Kyoto's Munakata camphor resolved; Seville and Florence tried, genuinely stayed dead

- Visitors were checked at the start of this session (43 visits, 69 page views over 7 days, flat); no submissions.
- The Camphor of Munakata Shrine (Kyoto) matched to two independent iNaturalist observations of the species 20m apart, both consistent with the shrine's own corner of Kyoto Gyoen, resolving its pin and adding a photo, viewed directly before approval. Kyoto now 6/10 photos, 3/10 approximate.
- Seville's own official tree catalogue (56 singular trees) exists but its website is unreachable from this session's tools; Overpass also returned service timeouts on every attempt today, likely load from the many concurrent runs hitting it. Not a dead end so much as a today-only access problem, worth retrying. Florence's remaining 7 photo gaps were re-checked and confirmed genuinely exhausted, matching the earlier pass. Full detail in CURATION.md.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Athens: a pin tightened, a photo found, a near-miss caught and deliberately not used

- Continued marquee Europe after Porto: Athens, at 4/10 photos and 10/10 approximate. Geocoded the Plato's Academy archaeological park itself for a 360m pin tightening (stays approximate, it locates the park not the tree). Found and approved a photo for the Olive Woodland of Filopappou Hill via iNaturalist, viewed directly.
- Worth a flag: found a second, differently-addressed "Plato's olive tree" claim in a Greek Wikipedia article, several hundred metres from our tree's actual sourced location. Read as a distinct legend site, not used, to avoid conflating two different trees under one name. Full detail in CURATION.md.
- Athens now at 5 of 10 photos (from 4). The rest of today's attempts (Kefalari planes, Kaisariani, Zappeion, the Pisistratus olive) came up empty or were left alone on purpose; genuine tries, recorded so they aren't repeated blind.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Porto: 4 pins resolved, 2 photos found, one stale "under review" claim corrected

- Moved to the next untouched marquee-Europe city after Seville: Porto, barely worked so far (2/10 photos, 10/10 approximate).
- New source this pass: Porto's own municipal open-data portal publishes a GeoJSON of every legally classified tree in the city. Matched the Tulip Tree of Casa Tait and the Metrosidero of the Library to their own classification records by legal reference, resolving both pins. Along the way, caught something actually wrong rather than just imprecise: the Metrosidero's story said it was "currently under review for protection," true when a 2017 source was written but the classification actually completed in 2019; fixed.
- Also matched the Bischofia Trio and the Coast Redwood, both in the Botanical Garden, to the only iNaturalist observation of their species there, resolving both pins and adding both photos, each viewed directly before approval.
- Porto now at 4 of 10 photos (from 2) and 6 of 10 approximate pins (from 10). Four gaps (Magnolia, Plane, Texas Madrone, Atlas Cedar) tried and came up empty this pass, genuinely not yet found rather than unattempted. Full detail in CURATION.md.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Amsterdam/Lisbon/Istanbul/Rome dead-end sweep, plus the Great Elm's photo

- Visitors, 7 days: 43 visits, 69 page views, flat. No submissions. Site healthy. Started rung 5's depth ladder from the top (Amsterdam, Lisbon, Istanbul, Rome) concurrently with the marquee-Europe pass below; some overlap on Berlin, reconciled rather than duplicated.
- Genuine new-technique attempts on all four lead-group holdouts turned up nothing: Amsterdam's own open-data tree API blocked by auth (403, a new angle, now ruled out); direct iNaturalist API queries on Lisbon's remaining photo gaps; a full retry of the OSM named-tree-node technique on Istanbul now that Overpass is reachable again, genuinely empty this time rather than a service outage; Rome's photo gaps, with one near miss caught and correctly rejected (a CC0 iNaturalist cedar 200m from the Belvedere pin turned out to be Cedrus atlantica, not this tree's Cedrus libani). Full detail in CURATION.md, recorded so future runs do not repeat these exact searches.
- Closed the one photo gap the Berlin pass below left open: the Great Elm of Treptower Park now has a CC0 Wikimedia Commons photo, its file title naming the tree directly, geotagged within 15m of the registry coordinate the pass below already confirmed. Viewed directly and approved.

## 2026-07-26 — The machine is complete: eyes and a self-starting chain

- All three secrets are in: the runs now read their own visitor numbers at the start of every pass (first reading: 43 visits, 69 page views over seven days, a steady 4 to 10 a day), and from the next completed run onward every run dispatches its successor. No cron luck, no human trigger, around the clock, bounded only by the usage limit.
- Nothing structural waits on Hidde anymore. What remains his: FOR HIDDE approvals here, taste (logo parked at his call), the budget ceiling number for the hard rules (still open), and the end-of-August reassessment.

## 2026-07-26 — Seville depth check: no new ground

- Next in marquee-Europe order after Berlin, Vienna, Kyoto, Florence. Genuinely tried both angles (OSM named-tree nodes, iNaturalist/Commons photos) on Seville's 9 approximate pins and 5 missing photos; nothing cleared the bar (unnamed OSM nodes, CC-BY-NC-only iNaturalist observations). Detail in CURATION.md. No data changed.
- This closes out this session's run down the marquee-Europe list (Berlin, Vienna, Kyoto, Florence, Seville); a future run should continue with Porto, Athens and the rest, oldest-first, per rung 5.

## 2026-07-26 — Every found_needs_check photo on the site cleared in one pass

- Discovered this run's tools actually can open fetched images (fetch the URL, then read the saved file back) after believing otherwise. Went back through the whole site rather than just today's own work: 15 photos across Florence, Kyoto, Berlin, Dublin, Lyon, Munich, Nice, Valencia and Venice were sitting at `found_needs_check` from this run and earlier ones this week. Viewed every one directly. 14 clearly matched their tree and moved to `approved`; 1 (Venice's San Servolo olive) turned out to be a distant island aerial with no tree visible, moved honestly to `missing` instead of left stuck.
- Along the way, found and approved one new photo for Florence (a cork oak in the Giardino dei Semplici, via iNaturalist) and caught a real near-miss: a felled "200-year Cedar of Lebanon" in the news turned out to be at Boboli Gardens (Pitti Palace), not our similarly-named Giardino del Bobolino tree near Porta Romana. Different gardens, tree unaffected. Full detail in CURATION.md.
- Zero `found_needs_check` photos remain anywhere on the site as of this commit.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Vienna: 3 of 5 approximate pins resolved

- Continuing rung 5's marquee-Europe order, Vienna next (already at 10/10 photos). Its protected trees carry individual Naturdenkmal numbers, and two already-approved Commons photos turned out to be geotagged at the tree itself by their photographer (a Vienna monuments specialist), plus a German tree register (baumkunde.de) independently publishes GPS for named specimens. Used both to confirm 3 pins 80-150m tighter than the previous address-level estimates. Full detail in CURATION.md.
- Vienna now at 2 of 10 approximate pins (from 5): one stays an honest ensemble (a whole chestnut avenue), one (the Schönbrunn ginkgo) couldn't be independently re-verified this pass, a source went unreachable on retry.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Berlin: reached 8/10 photos and 0/10 approximate pins

- Continuing rung 5's marquee-Europe order past Kyoto, picked Berlin as the closest published city to fully clearing both bars (was 7/10 photos, 2/10 approximate).
- The Ginkgo of Schlosspark Britz matched an OpenStreetMap node carrying the estate's own tree-inventory reference number, and gained a photo from a Commons category dedicated to this exact natural-monument tree. The Great Elm of Treptower Park matched a national heritage-tree registry's own surveyed GPS point, a ~460m correction; its photo gap closed in the concurrent pass above. Full detail in CURATION.md.
- Berlin now clears the 80% photo floor (9/10, once the elm's photo above is counted) and has 0 approximate pins.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Kyoto: 2 pins resolved, 1 photo found, caught a species tag error rather than trusting the source

- Correction to this entry's first version: it misstated Kyoto's starting count as 4 approximate; it was actually 6, so resolving 2 left 4, not 2. Fixed in CURATION.md.
- With the eight lead-group cities heavily worked by concurrent runs today, followed rung 5's next instruction (marquee Europe/Japan, oldest-first) to Kyoto, the oldest still-approximate city after the lead group.
- The Land Boat Pine and the Reclining Dragon Pine both matched to OpenStreetMap nodes carrying their own Japanese names (陸舟の松, 遊龍松), moving each pin 40-60m to the tree's actual surveyed position. The dragon pine's OSM node also carried a species tag that contradicted our own sourcing (black pine vs. the five-needle pine two independent sources and the story itself describe); used the location, dropped the wrong species rather than overwrite good sourcing with a stranger's tag. Also found a Commons photo for the Inverted Ginkgo of Nishi Honganji, title-matched but not visually confirmable with this run's tools, so recorded `found_needs_check`. Full detail in CURATION.md.
- Kyoto now at 4 of 10 approximate pins (from 6) and 5 of 10 photos (from 4). The remaining two approximate trees (Hosen-in pine, Munakata camphor) are a genuine dead end for the OSM technique this pass: retried Overpass, both bounding boxes came back empty rather than timing out.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Depth sweep (Barcelona, Rome, Amsterdam, Istanbul, Lisbon): genuine attempts, no new ground this pass

- Visitors, 7 days: 43 visits, 69 page views (2026-07-20 to 2026-07-26: 8, 9, 10, 7, 4, 5 visits), flat and too low yet to point depth work at a specific tree from traffic alone.
- Several other runs were working the same ladder concurrently today: by the time this pass started, Tokyo, London, Amsterdam's Heimanseik and Barcelona's first four pins were already resolved (this session's own independent Tokyo attempt lost that race to a better-sourced version using OpenStreetMap named-tree nodes, which is the one that stands; no harm done, just discarded before pushing). Moved to what was still open.
- Tried genuinely, found nothing new: Barcelona's last 4 photo gaps (Commons, iNaturalist, Openverse, all empty), Rome's pins and photos (OSM tree nodes exist near all three target trees but none match on species or name, one iNaturalist near-match for the cork oak is fully unlicensed), Amsterdam's Amstelkade Olive Willow (OSM nodes nearby, none named or species-tagged). Full detail, including two Lisbon iNaturalist candidates rejected for being CC-BY-NC rather than an allowed license, in CURATION.md.
- Istanbul's OSM queries all hit HTTP 504 this pass, an Overpass service issue rather than a data dead end; worth retrying, not counted as exhausted.
- No data changed, nothing to rebuild or push beyond this log and CURATION.md.


## 2026-07-26 — Barcelona: found a genuine location error, not just imprecision

- Continuing the same session, next untouched lead city: Barcelona. Barcelona keeps its own official "Arbres d'interes local" catalogue, and OpenStreetMap carries it as individually tagged tree nodes, same trick as Tokyo and Amsterdam above.
- Worth flagging on its own: the Wingnut and Green Ash of the Sot de l'Estany weren't just approximate, their stored pin was about 830m outside the actual botanical garden. Found and fixed against a catalogue node literally labelled with the ravine sector by name. Also confirmed the Holm Oak and the Himalayan Cedar of the Labyrinth the same way.
- Found and visually verified two new photos via iNaturalist: the carob at Placa de la Natura (an observation titled with the tree's own name) and the ombu at Placa Prim.
- Barcelona: 6/10 photos (from 4), 1/10 approximate (from 5, La Rambla's plane ensemble, an honest permanent case). Precision bar cleared, photos still short of 8.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Amsterdam: one more pin, two backlogged photos cleared

- Continuing straight on from the Tokyo/London pass below in the same session. Applied the same OpenStreetMap named-tree-node trick to Amsterdam: found a node named "Heimanseik" (Quercus robur, start_date 1775) about 300m from the old general-park pin, upgraded to confirmed.
- Also cleared two photos that were stuck at `found_needs_check` because an earlier run's tools couldn't open image files to check them visually: this run's could (fetch the URL, then read the saved file back). Amsterdam's Lomanstraat canopy photo and Lisbon's Paineira bloom photo both checked out and are now approved. Worth knowing for future runs: the visual-check limitation a prior run flagged is not universal, worth trying before leaving something at found_needs_check.
- Amsterdam: 6/10 photos (from 5), 3/10 approximate (from 4). Still the furthest of the eight lead cities from clearing rung 6's exit test, which needs it at zero. The three left (a potted indoor cycad, a street tree whose only real source page 403s, and a 46-tree square that honestly is an ensemble) are genuinely hard rather than unattempted; detail in CURATION.md.
- Lisbon: 2/10 approximate (already at the bar), 4/10 photos (one upgraded, count otherwise unchanged).
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Tokyo and London now pass the depth exit test

- visitors.py: no Cloudflare account tag configured, skipped silently as instructed. No reader submissions either (checked the live CSV, still just the header row).
- Site was healthy and nothing published was wrong, so this run continued rung 5's depth work. A new technique paid off: OpenStreetMap carries contributor-mapped nodes for individually named notable trees (tagged with the tree's own name and species), separate from the generic street-tree layer, queryable via Overpass/Nominatim. Used it to resolve 3 of Tokyo's 4 remaining approximate pins (the Three Hundred Year Pine, the Sperm-Discovery Ginkgo, the Meoto Kusu) to confirmed, each corroborated by a second independent source. Tokyo: 8/10 photos, 1/10 approximate (the Meiji Jingu Gaien avenue, 146 trees, honestly stays an ensemble estimate).
- London's last blocker fell too: a second independent source (an Open Plaques entry for the tree's own Great Trees of London plaque) confirmed Barney the Plane's EXIF-derived pin was correct, upgrading it from approximate to confirmed. London: 10/10 photos, 2/10 approximate (Berkeley Square and the Old Lions of Kew, both honest multi-tree ensembles).
- **Tokyo and London both now individually clear rung 6's exit test bar (8+ photos, 2 or fewer approximate pins).** The bar still needs all eight lead cities passing, with Amsterdam at zero, before coverage reopens: Amsterdam, Lisbon, Istanbul, Rome, Paris and Barcelona remain short. Full numbers and reasoning in CURATION.md.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — London: Royal Oak pin confirmed via Woodland Trust registry, Berkeley Square sourcing fixed

- London already clears 8/10 photos; only its pin count blocked the exit test. The Royal Oak's own Woodland Trust Ancient Tree Inventory entry gives a precise, unobscured grid reference (checked directly against the hard-rule-10 Woodland Trust caveat before using it), converted and applied: a roughly 400m correction. Also backfilled two sources for the Berkeley Square Plane, which had shipped with none.
- London now at 2 of 10 approximate pins, at the exit test's own threshold. Full detail in CURATION.md.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Paris photo check: no new ground, closest city to the exit test

- Paris only needs 2 more photos to clear the 8/10 floor (already at 0 approximate pins). Checked Commons, iNaturalist, Flickr and the City of Paris's own remarkable-trees gallery for the 4 gaps; the gallery confirmed the right trees but isn't openly licensed, and nothing else cleared the bar. Stays at 6/10. Detail in CURATION.md.
- This is the one city genuinely close to passing rung 6's exit test on its own; worth a dedicated photo push in a future run since only 2 finds stand between it and done.

## 2026-07-26 — Istanbul and Rome depth checks: no new ground, both genuinely tried

- Continuing rung 5's order (Amsterdam, Lisbon, Istanbul, Rome) after the Lisbon pass above. Istanbul: this is the third genuine hunting pass on its photo gaps without a new find (after 2026-07-22 and 2026-07-23), and its own registry (anitagac.istanbul) embeds per-tree maps as JavaScript with no coordinates reachable from the page source, so pin precision couldn't be improved either. Rome: Italy's national tree registry has no search and 881 unpaginated Roma entries with no way to filter by villa, so a targeted lookup for the cedar at Villa Doria Pamphilj, the two trees at Villa Celimontana or Adonis wasn't reachable; Commons categories for both villas were checked directly and nothing confirms the specific named trees.
- No data changed in either city. Recorded in CURATION.md so a future run does not repeat the same searches without knowing they were tried, per the mandate's own warning against looping.
- This closes out rung 5's named order (Amsterdam, Lisbon, Istanbul, Rome) for this session; a future run should continue with the rest of the lead group and marquee Europe, oldest-first, as the rung directs.

## 2026-07-26 — Lisbon photo pass: 3/10 to 4/10

- Next in rung 5's order after Amsterdam. Genuine hunt across Commons, iNaturalist, Flickr and Openverse for all 7 missing photos; found 1, a CC0 iNaturalist photo of the Paineira in bloom. Full detail, including two rejected near-misses, in CURATION.md.
- Lisbon still well short of the 8/10 floor at 4/10; the remaining 6 gaps look like genuinely hard cases (an ensemble tree with no individual photography, a square nobody seems to have photographed with the tree in frame) rather than ones this pass skipped.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Amsterdam depth pass: 3 pins resolved to confirmed, photo hunt came up empty

- Continuing the phase opened earlier today: rung 6's exit test needs Amsterdam at 0 approximate pins and 8+ photos before new cities can reopen, so this run worked Amsterdam first as rung 5 directs.
- Resolved 3 of 7 approximate pins to confirmed against independent sources that pin the tree itself (a photo's own GPS EXIF, an iNaturalist observation's GPS reading, and an OpenStreetMap address geocode cross-checked against two written descriptions). Amsterdam now at 4 of 10 approximate, down from 7. Full detail, including why the other 4 stay approximate for now, in CURATION.md.
- One good catch while researching the Vondelpark poplar: a 2011 news item about a "big poplar" falling in the park turned out to be a different tree in a different part of the park, not this one. Confirmed independently that the Van Eeghenlaan poplar is still standing.
- Photo hunt across Commons, iNaturalist and general web for the 4 missing photos found nothing that cleared the licence bar. One near-miss caught: a cycad photo that looked right for the Hortus specimen turned out to be the same species at Leiden's Hortus, a different garden. Amsterdam stays at 6 of 10 photos.
- Not yet at the flawless bar (10 photos, 0 approximate) rung 5 asks for on Amsterdam specifically; the remaining 4 approximate pins and 4 missing photos are genuinely hard cases (an indoor potted plant, a zoo-internal position, two thin single-source street trees) rather than ones this pass didn't try. Left open for a future run.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-26 — Autonomy stack complete, waiting on two secrets

- Product lane opened (rung 7 + PRODUCT_TODO.md): runs now build the site, not only research trees. First up: the shareable my-trees page.
- Count doctrine live: ten is a cap, four verified trees minimum for a page. Verona's title lie (promised 10, had 8) fixed by making every count dynamic.
- Depth exit test + Netherlands wave queued; the machine transitions by itself.
- Checkpoint end of August recorded in GO_TO_MARKET.md with explicit healthy/failing criteria.
- FOR HIDDE, two secrets and one number, then nothing structural waits on you:
  1. `SELF_DISPATCH_TOKEN` (GitHub fine-grained token, Actions read/write, only this repo) → repo Settings > Secrets > Actions. Turns ~5 attempts/day into a continuous chain.
  2. `CLOUDFLARE_ANALYTICS_TOKEN` (Account Analytics: Read) → same place. Lets runs read the visitor trend themselves and write it here.
  3. The €50/month cost ceiling in the hard rules predates Claude Max. Say the new number and a run records it.

## 2026-07-26 — Phase 1 opened: Google serves us, runs flip from width to depth

- First Search Console export ever read: impressions 1 > 5 > 38 > 103 across four days, roughly doubling daily since the sitemap went in. First two clicks: the homepage, and Tokyo's Meiji Jingu Gaien ginkgo avenue (33% CTR from position 28, from Canada).
- City pages already rank page one: Amsterdam 7.9, Lisbon 7.7, Istanbul 8.0, Kyoto 8.3, Barcelona 9.7. Rome pulls the most impressions (18). Real target queries showing: "trees in rome", "oldest tree in lisbon", "ancient tree map" (position ~41, a query we should own). Mobile ranks and clicks; desktop does not yet.
- Per GO_TO_MARKET.md this is the Phase 1 trigger, so the phase flipped on evidence: new cities frozen at 33, runs now do depth on the cities search serves, Amsterdam to flawless first, then Lisbon, Istanbul, Rome. Ladder rungs 5 and 6 rewritten, workflow prompt aligned (it still said "resume coverage", the same two-truths mistake as 2026-07-22, caught this time).
- Also checked: the submission form is still empty (zero submissions), and Cloudflare Web Analytics needs reading under Analytics & Logs > Web Analytics, not Account home, which measures proxied traffic we deliberately do not have.
- FOR HIDDE: nothing blocks. If you want coverage reopened, flip rung 6 in CLAUDE.md; a run may not do it alone.

## 2026-07-25 — Verona: 33rd city live, 8 trees researched (shipped with 8, not 10)

- No submissions, site healthy, nothing published wrong. Rung 5: the next `pending` city, Verona. Verona's own documented tree heritage is thinner than Naples or Bologna's, only 3 trees on Italy's national register within the city itself, so after a genuine search only 8 trees held up to the two-source bar. Shipped with 8 rather than padding to 10, per CLAUDE.md's own "eight good trees ship" guidance.
- Headline find: the Cedar of Lebanon in Piazza Bra, beside the Arena, planted 1873, made real local news in mid-2025 when the city raced to stabilise its failing roots before Ferragosto, well covered across multiple Veronese outlets.
- One honesty call: the famous 600-year-old Cypress of Goethe in the Giardino Giusti was destroyed by a 2020 storm and no longer exists. The entry describes the avenue as it stands today (younger replanted cypresses plus older survivors), not the fallen original, and a set of pre-storm archival photos was deliberately not used since it would misrepresent what a visitor sees now, the same discipline as Naples's Pino di Posillipo.
- 2 of 10 photos found (both trees of Piazza Indipendenza), viewed directly before approval. Full detail in CURATION.md.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-25 — Bologna: 32nd city live, 10 trees researched

- No submissions, site healthy, nothing published wrong. Rung 5: the next `pending` city, Bologna. Eight of Italy's officially catalogued monumental trees stand within the city itself; this list draws on most of them plus two further well-documented specimens.
- Two more wrong-city near-misses caught this run (after Naples's Palermo ficus mixup): a Commons category literally named "Ginkgo di piazza Cavour" turned out to be a Turin tree, not Bologna's; and a Villa Ghigi cedar photo search surfaced a similarly named tree in Vallerano instead. Neither used. Also caught and fixed before commit: an early draft accidentally cited a Naples source (leftover from this same session's earlier research) for a Bologna tree; replaced with the correct source.
- 3 of 10 photos found (two platani and the cypress over poet Giosue Carducci's grave at the Certosa cemetery), all viewed directly before approval. 7 missing after a genuine search. Full detail in CURATION.md.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-25 — Naples: 31st city live, 10 trees researched

- No submissions, site healthy, nothing published wrong. Rung 5: the next `pending` city, Naples. Naples holds more officially catalogued monumental trees than any other Italian municipality, mostly concentrated at the Real Bosco di Capodimonte, the former Bourbon royal estate; six of the ten trees come from there, an honest reflection of where the city's tree heritage actually sits rather than a shortcut.
- Two honesty calls worth Hidde's attention: the Pino di Posillipo, one of the most photographed trees in the world in its day, died in 1984 and was replanted in 1995, so it is labelled a young replacement here, same as Edinburgh's Corstorphine sycamore; and the Platano di San Severino, felled in 1959 and regrown from its own root, is dated from that regrowth rather than the legendary original planting. One near-mixup avoided: a "ficus magnolioide" at Naples's own botanical garden kept surfacing conflated with Palermo's much more famous tree of the same name (a different tree, in a different pending city), so dropped it for a cleaner-sourced alternative rather than risk a wrong-city error.
- 0 of 10 photos found despite a genuine search across Commons and iNaturalist; full detail in CURATION.md, including why a strong-looking historical photo of the original Posillipo pine was deliberately not used.
- Site rebuilt, all contracts validated on the first pass, pushed.

## 2026-07-25 — Granada: 30th city live, 10 trees researched

- No submissions (CSV still header-only), site healthy, nothing published wrong. Rung 5: the next `pending` city after Malaga, Granada. No single municipal register exists for Granada's trees, so pieced this together from a magazine survey of twelve singular specimens, the Alhambra/Generalife's own heritage pages, and the UGR Botanical Garden's records.
- One real discrepancy resolved rather than smoothed over: the popular "500 year old" San Juan de la Cruz cypress story conflicts with an official Alhambra page describing a similarly named tree with specific measurements at a different property. Used the more conservative, precisely dated figure (roughly 440 years, tied to the poet's documented 1582-1588 residency) and flagged the discrepancy directly rather than picking whichever number sounded better.
- Two trees researched and dropped before publishing, both confirmed dead (a nettle tree at the Alhambra, gone since 2020; the original Generalife "Cipres de la Sultana", dead since the late 1980s, only its dry trunk preserved). A page for a tree nobody can actually see fails this project's whole point, so neither shipped.
- 1 of 10 photos found (the Cuarto Real robinia, via iNaturalist, viewed directly before approval). 9 missing after a genuine search. Full detail in CURATION.md.
- Site rebuilt (one meta description trimmed to fit), all contracts validated, pushed.

## 2026-07-25 — Photo-floor rung checked and closed out for now; Malaga: 29th city live, 10 trees researched

- Rung 4 (photos below 80%) checked first, focus region (UK, Netherlands) first per the 2026-07-22 decision. Re-hunted Edinburgh's 6 missing photos across Commons, Geograph, iNaturalist and Flickr; found nothing new, an exact third repeat of the 2026-07-23 hunt and 2026-07-24 recheck. That confirms rather than changes anything: every one of the lead-group and marquee-European cities already had at least one genuine dedicated photo hunt earlier this week. Re-running the same searches again would be the "looping forever" the mandate explicitly warns against, so treating the rung as exhausted for the existing 28 cities given currently findable sources, and moving to rung 5. Full detail and the two rejected near-misses in CURATION.md.
- Rung 5: the next `pending` city, Malaga. Researched via the city's own 2022 TreeTags scheme (ten municipally tagged trees, part of a European urban-tree awareness campaign) and the Jardin Botanico-Historico La Concepcion's own historic-plants records. 10 trees written and shipped. Throughline: almost everything on the list is an import, fig, ceiba, araucaria, avocado, arrived through 19th/20th century fashion and trade; the one native holm oak stands out precisely for being the exception.
- One access case handled honestly rather than dropped or force-fit: the Churriana avocado tree stands on working school grounds, visited by appointment rather than freely, and the access field says so plainly.
- 3 of 10 photos found on Wikimedia Commons, all fetched and viewed directly before approval (the Concepcion's olive, the Alameda's ficus avenue, El Barrilito's bottle trunk). 6 missing after a genuine search across Commons and iNaturalist. Full detail, sourcing caveats and the superlative claims kept with their hedges intact, in CURATION.md.
- Site rebuilt (two meta descriptions trimmed to fit the 155-character limit), all contracts validated, pushed.

## 2026-07-25 — Nice: 26th city live, 10 trees researched

- No reader submissions (CSV checked fresh: header row only). Site healthy, nothing published was wrong. Went to the next rung: the next `pending` city, Nice.
- 10 trees researched, written and shipped. Nice turned out to be the opposite kind of city from Venice and Munich: almost everything remarkable here is young and deliberate rather than old and undocumented; the city as a resort barely predates photography. The one real exception, and the throughline used for the city's own intro, is Cimiez, gardened without interruption since Franciscan monks arrived in 1546, whose olive grove is the only place in the city with trees plausibly over 400 years old.
- A genuine hard-rule-10 catch: two well-documented, roughly 500-year-old carob trees on a private Nice property carry an official regional "arbre remarquable" label, but a direct check found the trees explicitly described as not open for visits. Dropped them and used a different labelled tree instead, a strawberry tree at Château de Crémat, a Bellet vineyard estate that genuinely takes booked visitors.
- All 10 flagged honestly. 6 of 10 presented as explicit ensembles (a garden's founding planting, a documented reforestation campaign) rather than forcing a single named specimen where none is measured, the same honest pattern used for Antwerp's Den Brandt and Athens's cemetery cypresses. One superlative softened per hard rule 8: Parc Vigier's claim to have acclimatised France's first Canary Island date palm in 1864 rests on one detailed source with no second one found, so the story attributes the claim rather than stating it as fact.
- A small human find worth naming in case Hidde enjoys it: Henri Matisse is buried under an old olive tree on land next to the Cimiez monastery cemetery, a few minutes from the museum that holds his work.
- 2 of 10 photos found on Commons with matching filenames, both marked `found_needs_check` for the same tool-constraint reason as Venice and Munich this run (see those entries): images could not be opened and visually confirmed this session. 8 of 10 photos missing after a genuine search.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-25 — Valencia: 28th city live, 10 trees researched

- No reader submissions (CSV checked fresh: header row only). Site healthy, nothing published was wrong. Went to the next rung: the next `pending` city, Valencia.
- 10 trees researched, written and shipped. Valencia is exceptionally well documented for this project's purposes: a 2006 regional law protects over 2,400 monumental trees across the Comunitat Valenciana, more than any other Spanish region, and the city itself maps five named tree routes with individual tree profiles, on top of two local-history blogs that had already done real reporting on several of these trees' backstories.
- A real catch worth flagging: the tree originally slotted in as the tenth entry, a historic pine in Campanar and the last survivor of a forest that once stretched to Godella, turned out to have been cut down by the city's own gardeners in August 2019. Found this mid-research rather than after publishing, and swapped it out entirely for a still-living tree (a Kashmir cypress) rather than publish a tree that no longer exists.
- One quieter catch: an early source called three landmark palms on Calle Albacete "Washingtonia," a second, more specific source corrected the species to Phoenix canariensis, and the correction went in before publication rather than after.
- All 10 flagged honestly, none fabricated. Several of these trees have genuinely well-documented human stories, not just measurements: a fig planted by mistake for a magnolia in 1852 that's now Valencia's widest canopy, a palm moved across the city by truck in a single night with the mayor's permission to close the streets, a fig sapling that survived a demolition crew because the head gardener lied about what pruning would do to it.
- 2 of 10 photos found and used (a ficus in El Parterre, a ginkgo in Jardín de Monforte, both CC BY-SA, filenames naming the exact tree and garden), marked `found_needs_check` for the same tool-constraint reason as this run's other cities. 8 of 10 photos missing after a genuine search.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-25 — Lyon: 27th city live, 10 trees researched

- No reader submissions (CSV checked fresh: header row only). Site healthy, nothing published was wrong. Went to the next rung: the next `pending` city, Lyon.
- 10 trees researched, written and shipped. Lyon was the best-documented city this run has hit: the city publishes its own list of nationally labelled remarkable trees, and a French dendrology blog plus the International Dendrology Society's own reference site gave precise coordinates and measurements for several specimens, letting 3 of the 10 entries carry a fully confirmed pin rather than an approximate one, the most of any city on the site so far.
- Genuinely interesting catch, named honestly rather than smoothed over: Parc de la Chapelle's Atlas cedar carries a locally repeated claim of roughly 500 years and a real 2024 national label with solid measurements, but Cedrus atlantica wasn't introduced into French cultivation until the 1840s, which makes a true 500-year-old specimen hard to square with the species' own history in Europe. Presented as a stated local claim, not adopted as fact.
- All 10 flagged honestly, none fabricated. 2 of 10 presented as explicit ensembles where no individual tree is documented (a 1913 oak collection, an undated hillside garden), the same honest pattern used in Venice, Munich and Nice this run.
- 1 of 10 photos found and used (the Tête d'Or's Osage orange, CC BY 4.0), marked `found_needs_check` for the same tool-constraint reason as this run's other three cities. A matching Flickr photo of the park's Chinese pine was found and correctly rejected: All Rights Reserved, not a usable licence.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-25 — Small fix: Venice's one photo URL was a dead link

- Bundled into this commit rather than a separate one. While building Munich's photos (see below), realised the same hand-guessed Wikimedia hash-path mistake had already shipped in Venice's single photo (Giardini Papadopoli), one commit earlier. Recomputed the correct URL via MD5 of the actual filename and fixed it in place. No other change to that entry; still `found_needs_check`, not `approved`.

## 2026-07-25 — Munich: 25th city live, 10 trees researched

- No reader submissions (CSV checked fresh: header row only). Site healthy, nothing published was wrong, photo-floor rung still exhausted from the prior sweep. Went to the next rung: the next `pending` city, Munich.
- 10 trees researched, written and shipped. Munich turned out unusually well documented for this project: a city ordinance renewed 21 July 2021 individually registers 117 protected natural monuments (Naturdenkmäler) covering 200 trees, each with an official reason on record, a much stronger starting point than most cities have offered.
- Genuinely interesting honest disagreement, kept as a disagreement rather than resolved: two different trees are separately called Munich's oldest by different sources, a roughly 600-year-old oak (Krüner Eiche, per a district citizen assembly document) and a 300-350 year old linden (Röth-Linde, per a dedicated local news feature). Neither source checks its claim against the other, so this list doesn't either, and both the FAQ and question page state the conflict directly rather than picking a winner.
- All 10 flagged, all honestly: Munich's own register gives most trees broad, undated size or rarity claims rather than individual measured ages, and every entry says so plainly. One exception stands out for the opposite reason: the Reichs- und Friedenseiche has an exact plaque-documented planting date, 1 July 1871, planted by 12,000 Munich schoolchildren days after the Franco-Prussian War's peace treaty, one of the more precisely dated trees anywhere on the site.
- Caught and fixed a real bug before it shipped: constructed five Wikimedia Commons photo URLs by hand-guessing the hash-path segment of the file address instead of computing it, and every single guess was wrong, which would have shipped as five dead image links. Recomputed each via MD5 of the actual filename and spot-checked the method against a known-good existing entry (Milan's bagolaro photo) before using any of them. Worth a general note for future runs: don't hand-guess Wikimedia hash paths, compute them.
- 5 of 10 photos found on Commons with strong filename/category matches, all CC BY-SA, but all marked `found_needs_check` rather than `approved` since this run's tools still could not open image files to visually confirm content (same constraint as the Venice run above). 5 of 10 photos missing after a genuine search.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-25 — Venice: 24th city live, 10 trees researched

- No reader submissions (CSV checked: header row only, fetched fresh). Site healthy, nothing published was wrong. Checked the photo-floor rung next: every one of the 23 live cities already had a genuine dedicated hunting pass in the 2026-07-22/23/24 sweep, and the most recent Edinburgh recheck explicitly concluded re-running the same searches again would be the exact "looping forever" the mandate warns against. Treated that rung as exhausted for now and went to the next rung: the next `pending` city, Venice.
- 10 trees researched, written and shipped. The throughline, used as the city's own intro: Venice's historic islands are built on reclaimed marsh and packed with stone, leaving almost no ground for a tree to grow old by accident, so every remarkable tree here survives because someone deliberately made room for it, Napoleon's engineers draining marshland for a public garden in 1810, Armenian monks building a monastery garden from 1717, a cemetery planted with cypress the year it opened. Comune di Venezia's actual territory (the lagoon islands, the Lido, and the mainland districts of Mestre and Marghera) was used as the boundary, the same "Greater London" logic used for other cities, which is what put Forte Marghera on the mainland on the same list as San Lazzaro degli Armeni in the lagoon.
- All 10 trees flagged honestly. None fabricated. This is a harder city than most for individual tree ages: no source found gives any single Venice tree here its own measured age or exact planting date, only documented founding/construction dates for the gardens and islands they stand in (1717 for San Lazzaro's monastery garden, 1810 for the Napoleonic Gardens, 1813 for San Michele cemetery, 1834-35 for Giardini Papadopoli). Every entry states that gap plainly rather than borrowing the garden's founding date as if it were the tree's own age, and presents six of the ten as explicit ensembles (a species mix or a planted line, like Antwerp's Den Brandt or Athens's cemetery cypresses) rather than forcing a single named specimen where none is documented.
- One access note worth naming: San Lazzaro degli Armeni (paid guided tour only, 8 euro, one daily departure) and San Francesco del Deserto (free but reachable only by private boat from Burano, no public vaporetto stop) are both genuinely open to the public, just not a casual walk-in. Ca' Zenobio degli Armeni's garden is honestly marked as open mainly during scheduled exhibitions rather than year-round, closer to Prague's locked-garden precedent than a normal park.
- Photo hunt was constrained this run: this session's tools could not fetch or visually open image files (network downloads and the Read tool's remote-URL path both declined), so the direct-viewing discipline the last several runs established (catching the Berlin Kaisereiche mismatch, for example) could not be applied. One photo (Giardini Papadopoli, CC BY-SA 4.0, Didier Descouens) was strong enough on text alone, matching coordinates to the metre and a filename that translates as "trees", to include, but marked `found_needs_check` rather than `approved` since it was never actually opened. Three more candidates with plausible but unconfirmed subject matter (San Francesco del Deserto, San Servolo, Ca' Zenobio) are recorded in each tree's `notes` field with the exact filename, so a run with working image tools can finish the check in minutes rather than re-searching from zero. 6 of 10 photos missing after a genuine search.
- Site rebuilt, all contracts validated, pushed.
- FOR HIDDE: nothing blocking. Flagging only in case it recurs: this run's tools couldn't open image files to view them (see photo note above), which is a change from the last several runs. If a future run hits the same limit, its "approved" photo statuses are worth spot-checking rather than trusted outright.

## 2026-07-24 — Milan: 23rd city live, 10 trees researched

- No reader submissions (CSV checked: header row only, fetched fresh). Site was healthy, nothing published was wrong, so went straight to the next rung: the next `pending` city, Milan.
- 10 trees researched, written and shipped. The throughline: Milan has almost nothing medieval standing, having rebuilt itself too many times for old wood to survive by accident. What lasted did so because of a specific human decision, a university's planting records (the botanical garden's 1775 ginkgo pair, the city's oldest documented trees), a neighbourhood campaign (Brera residents saved a self-seeded paulownia from a car park in 2016), or a park that changed jobs entirely (a horse-racing track turned 1919 open-air school for sick children, still a working school today). Full detail in CURATION.md.
- One superlative caught and corrected: local press calls a red oak at Piazza XXIV Maggio "the oldest tree in Milan." It isn't, this list's own ginkgo pair is close to a century older and better documented, so the claim was dropped per hard rule 8 and the oak's real story (planted in 1924 by a father in memory of his son and the Alpini who died in the First World War) used instead.
- Two corrections caught mid-research, both prevented from shipping wrong: a popularly loved red oak, the Quercia di Montale, turned out to have fallen in 2019 (only its trunk survives as a deliberate biodiversity exhibit); a widely repeated "1773 plane tree of Villa Litta" turned out to have been felled in 2015 after disease, with only a preserved cross-section on display. Both dropped from the list of 10 and named honestly in the city's own FAQ instead. A third candidate, a thinly-sourced cedar with zero measurements and no second source, was swapped out during research for a much better-documented tree in the same slot.
- 6 of 10 trees flagged honestly (a genuine 16-year age dispute for the ginkgo pair, a real dendro-vs-legend gap for the Affori plane, and several single-sourced age figures), none fabricated.
- 5 of 10 photos found and visually confirmed on Wikimedia Commons. 5 missing after a genuine search, including two Flickr photos of the exact Brera paulownia that turned out to be All Rights Reserved.
- Site rebuilt, all contracts validated on the first pass, pushed.

## 2026-07-24 — Florence: 22nd city live, 10 trees researched

- No reader submissions (CSV checked: header row only). Site was healthy, nothing published was wrong, so went straight to the next rung: the next `pending` city, Florence.
- 10 trees researched, written and shipped, all with confirmed GPS pins this time (Italy's own regional monumental-tree registry, RAMI, gives an individually surveyed coordinate for every one of the 145 Florence trees it tracks, a stronger footing than most cities on this list have started from). The throughline: Florence's oldest documented trees sit in one institution, the Giardino dei Semplici botanical garden (founded 1545), which kept its own planting records; almost everything else on the list dates from the single decade in the 1860s-70s when Florence was briefly capital of unified Italy and architect Giuseppe Poggi built the parks and viewpoints (Piazzale Michelangelo, the Bobolino) that the city is still walking around today. Full detail in CURATION.md.
- Two real corrections caught mid-research, both prevented from shipping wrong rather than just vague: a much-repeated cedar landmark at Villa Fabbricotti turned out to have died in 2001 (only the trunk remains); a separately researched, officially-recognised monumental elm at Piazza Vittorio Veneto turned out to have died and been felled in July 2023, a fact several older tourism sources don't reflect. Both dropped entirely rather than published as living trees to visit.
- One hard-rule-10 exclusion: a regionally-registered monumental palm at Villa di Rusciano is explicitly marked "not accessible to the public" in its own registry entry, contradicting looser claims that the surrounding park is open; left off the list given the direct conflict.
- 8 of 10 trees flagged honestly, all for undocumented age rather than a fabricated one; one genuine age dispute (a Mexican cypress at the botanical garden, where two sources disagree by about 25 years) presented as a range rather than picking a number.
- 2 of 10 photos found and visually confirmed on Wikimedia Commons (the botanical garden's Montezuma cypress, and the ginkgo at Piazzale Michelangelo, which almost none of the millions who photograph that view each year seem to notice). 8 missing after a genuine search; Florence's own citizen-registry photos were not used since their licensing terms aren't a verified open licence.
- Site rebuilt, all contracts validated on the first pass, pushed.

## 2026-07-24 — Athens: 21st city live, 10 trees researched

- No reader submissions (CSV checked: header row only, confirmed by fetch). Site healthy, nothing published was wrong. Before starting new work, rechecked Edinburgh's 6 remaining photo gaps (still the weakest focus-region city at 4/10) in case anything had turned up since the 2026-07-23 pass; it hadn't, including two near-misses on iNaturalist that turned out, once checked at a tight 300m radius, not to actually be at the named site. No further hunting is planned there until something changes; continuing to re-search the same 20 cities' known gaps would be the exact "looping forever" the mandate warns against, and the last three runs already moved on for the same reason. Went to the next rung: the next `pending` city, Athens.
- 10 trees researched, written and shipped. The throughline that fell out of the research, and became the city's own intro: almost nothing standing in Athens is actually old wood. Three thousand years of destruction and rebuilding left little room for medieval trees to survive, so what the city has instead is continuity, an olive replanted on the spot Athena is mythologised to have grown the first one, another regrown from the root system of Plato's own Academy after a 1976 bus accident, and a deliberately planted 1950s olive woodland on Filopappou Hill (architect Dimitris Pikionis) now considered one of the century's landmark works of landscape architecture. Full detail in CURATION.md.
- One real research correction caught mid-way: an initial lead described Filopappou Hill's olive cover as centuries-old and gnarled from age. Two independent architecture-history sources instead date the whole woodland to Pikionis's 1954-1957 project, replacing a mostly bare, grazed hillside. Rewrote the entry honestly around the true, much younger age and the landscape-architecture story, which turned out more interesting than the invented alternative would have been.
- A second correction, caught while photo-hunting: the initial fourth entry (a generic pair of Acropolis cypresses, no individual age, included mainly as filler) was dropped entirely and replaced with a considerably stronger find, a specific, precisely located, well-photographed 700-1,500 year old olive tree that Greece's rail authority ERGOSE transplanted whole from a village near Aigio to a traffic island on Vasilissis Sofias Avenue in 2015, to save it from railway construction. Better sourced (5+ independent press outlets, an Agricultural University age assessment, a Commons photo visually confirmed) than what it replaced.
- The one tree with a genuinely disputed "oldest in Athens" claim, the Olive Tree of Pisistratus, is presented with its 1919 attestation (2,500+ years) stated but not adopted: modern radiocarbon dating of comparably old Mediterranean olives has repeatedly found real ages in the low hundreds, a test this specific tree has never had. Softened per hard rule 8 rather than repeating the "oldest olive on Earth" claim some tourism sources make for it.
- 4 of 10 photos found on Wikimedia Commons, every one fetched and viewed directly (not caption-matched) before approval: the Acropolis's sacred olive against the Erechtheion wall, the National Garden's holm oak, the ERGOSE-transplanted olive with its explanatory plaque, and the First Cemetery's entrance framed by cypresses. 6 missing after a real search across Commons, iNaturalist, Openverse and general web search; one candidate (a Kefalari park photo) was found but not used since its dominant trees read as conifers rather than the plane trees this entry describes.
- All 10 pins are approximate: park- or square-level addresses rather than a surveyed spot for each individual tree.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-24 — Porto: 20th city live, 10 trees researched

- No reader submissions (CSV checked: header row only). Site was healthy, nothing published was wrong, so went straight to the next rung: the next `pending` city, Porto.
- 10 trees researched, written and shipped. The throughline: almost everything remarkable here traces to 19th-century British port wine families who filled their Porto quintas with American, Asian and southern-hemisphere imports, plus the University of Porto's later absorption of one such estate into today's free Botanical Garden. Full detail in CURATION.md.
- One access-driven correction worth flagging: a municipal press release tied several classified trees, including a Himalayan cedar, to "Palacete Burmester Garden", a University of Porto building whose current public-access policy couldn't be confirmed. Dropped those rather than guess, and filled the Himalayan cedar slot instead with a specimen independently confirmed by photograph to grow in the fully public Palácio de Cristal gardens.
- 5 trees flagged honestly (missing ages, softened superlative claims, one single-sourced specimen kept because its underlying facts check out), none fabricated.
- Only 2 of 10 photos found and visually confirmed this round; several generic species stock photos were found and rejected for not being confirmed as the actual Porto specimen.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-24 — Seville: 19th city live, 10 trees researched

- No reader submissions (CSV checked: header row only). Site was healthy, nothing published was wrong, so went straight to the next rung: the next `pending` city, Seville.
- 10 trees researched, written and shipped. The throughline that fell out of the research: almost nothing in Seville is actually ancient. Most of its grandest trees, the Australian figs and eucalyptus, the ginkgos, date to two deliberate planting booms in the 1910s-1920s and the 1929 Ibero-American Exposition, not to any medieval or Moorish origin. Full detail in CURATION.md.
- One real research correction worth flagging: dropped a "500-600 year old orange tree planted by King Pedro I" after its only findable source (a since-removed city blog post) gave two different ages for itself in the same piece. Replaced it with a much better documented tree in the same gardens: a grove of ginkgos planted in 1910, 10 of 25 originals still alive today.
- 4 trees flagged honestly (thin or single sourcing, or an age that had to be stated as a range), none fabricated. Kept one single-sourced tree on the list anyway, a camphor tree said to be the only one in the city, since the underlying facts check out even though this specific specimen isn't cross-confirmed.
- 5 of 10 photos found on Wikimedia Commons, every one opened and viewed directly before approval rather than caption-matched. 5 missing after a real search, including one tree (the Gran Capitán eucalyptus, Seville's tallest) that turns out to have no dedicated photography anywhere, consistent with its own story: locally obscure despite being 50 metres tall.
- Four of the ten trees stand inside paid-admission sites (Real Alcázar, the Cartuja/CAAC, Seville Cathedral), noted plainly in each one's access field.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-24 — Berlin: 18th city live, 10 trees researched

- No reader submissions (CSV checked: header row only). Site was healthy, nothing published was wrong, and every one of the 17 already-published cities had already had a genuine photo-hunting pass this cycle (see the run of 2026-07-23 entries below), so per the ladder this run moved to the next rung: the next `pending` city, Berlin.
- 10 trees researched, written and shipped. Berlin protects around 600 trees as Naturdenkmäler, most of them oaks, and the throughline that fell out of the research is the Tegel Forest holding three of the city's own record-holders in one place: the oldest tree (Dicke Marie, honestly disputed at 500-900 years between two credible sources), the thickest (the Humboldteiche), and until a June 2025 storm felled it, the tallest too (the Burgsdorff-Lärche, researched then dropped once I found it was already dead, not something any source flagged up front). Full detail in CURATION.md.
- 7 of 10 photos found, all Wikimedia Commons. Caught one real near miss before it shipped: a file captioned for the Kaisereiche turned out, once actually opened and viewed, to show a giant sequoia trunk, not an oak. Swapped for a second, visually-confirmed photo of the right tree instead. A separate Ginkgo photo captioned for the Britz specimen turned out on the same check to be a different ginkgo in Pankow; dropped rather than used.
- One tree kept with an honest "declining" label rather than smoothed over: the Bellevue-Eiche in Köpenick, which Berlin's own district has literally called a "sterbende Eiche" (dying oak) in press coverage since 2015, when it was fenced off. Still alive, still under active conservation effort, story says so plainly.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-23 — Prague: 17th city live, 10 trees researched

- New city, the next `pending` in the tier-1 list after Vienna. Researched from Prague's official pamatny strom register (protecting individual trees since 1992, roughly 200 citywide), Czech Wikipedia's per-tree pages, and the city's own memorial-tree site (prazskestromy.cz).
- **9/10 photos found**, all Wikimedia Commons, all CC BY-SA 3.0 or 4.0, every URL checked and confirmed live before use. Only Neruda's Pear Tree came up empty after a real search.
- 4 trees flagged honestly: two disputed age ranges (the Beethoven Plane, Prague's likely-oldest visitable tree at 200-300 years depending on source, and the Karlovo namesti plane), one 80-year age disagreement (the Stromovka ginkgo), and one thinly-sourced entry (the Seminary Garden field maple, whose only sources trace to one underlying record). Details in CURATION.md.
- Two judgement calls on hard rule 10: dropped Prague's actual oldest tree, the 550-year Dub Karel oak at a private castle park in Kolodeje, and named it instead in the question-page context as the tree nobody can visit. Also researched then dropped a "400-year-old Prague Castle yew" lead that turned out, on closer checking, to be a different tree entirely: a yew in the Franciscan monastery's enclosed cloister courtyard, explicitly not open to the public. A second candidate (the Turbova estate yews in Kosire) was dropped on the same rule.
- One correction mid-research: a repeated "oldest white oak of its species in Czech Republic" claim for a Stromovka tree had no age, girth or precise location behind it anywhere, just the bare superlative. Dropped per hard rule 8, replaced with the better-documented Seminary Garden field maple.
- Kept one tree with a stated access caveat rather than dropping it: Neruda's Pear Tree is only in Prague's lower-tier "significant trees" list, not a legally protected memorial tree like the other nine, and the story says so plainly.
- Site rebuilt, all contracts validated on the first pass. Everything committed and pushed.

## 2026-07-23 — Vienna: 16th city live, 10 trees researched

- New city, the next `pending` in the tier-1 list. Researched from Vienna's official Naturdenkmal register (protecting individual trees since 1936, with an exact protection date for almost everything), Wikipedia's district-level Naturdenkmäler lists, and dedicated pages per tree.
- **10/10 photos found on the first pass**, tying London as the only other city to clear the 8/10 floor, thanks to two Viennese heritage photographers (GuentherZ, Michael Kranewitter) who have systematically documented the city's protected trees on Wikimedia Commons. All CC BY or CC BY-SA, licence and attribution recorded.
- 4 trees flagged honestly (an age or measurement that only one source gives, never a fabricated one). Details in CURATION.md.
- Two judgement calls worth flagging: dropped Vienna's actual oldest Naturdenkmal, a Roman-era yew grove remnant, because it sits on European Patent Office grounds and sources confirm it is "not publicly accessible" (hard rule 10); also dropped a 400-500 year old oak stand in the Lainzer Tiergarten because the fenced reserve containing it is guided-tour-only, specifically to protect the trees from visitor damage, which reads as the same spirit as rule 10 even on public land.
- One correction mid-research: an initially promising "thickest tree in Vienna" black poplar turned out to be a delisted, storm-felled tree (toppled 2015). Swapped for a well-documented pedunculate oak in the Prater instead rather than publish an uncertain or dead record-holder.
- Included one dead relic (Stock im Eisen, a nail-studded trunk not alive since roughly 1440) labelled clearly as a historic relic and excluded from the "oldest tree" answer, which goes to the oldest confirmed living tree instead.
- Site rebuilt, all contracts validated after a `question_meta` length fix. Everything committed and pushed.

## 2026-07-23 — New York: no new finds, closing this tier

- Last city in the Istanbul/Kyoto/New York tier. Genuine search across all 7 missing trees; nothing cleared the licence bar. New York stays at 3/10.
- This closes the whole tier for now: Tokyo 8/10 (floor cleared), Istanbul 2/10, Kyoto 4/10, New York 3/10. Every published city has now had at least one real photo-hunting pass this run.
- Everything from this session is committed and pushed. Good stopping point for the photo-floor work; next run can pick up improvement-mode cycling (oldest-published-first) or the next rung of the ladder.

## 2026-07-23 — Kyoto photo pass: 3/10 to 4/10

- Continuing the tier after Istanbul. Found 1: the Reclining Dragon Pine of Yoshimine-dera, via Commons's own dedicated category for the tree, visually confirmed against its documented trained horizontal form. Kyoto now at 4/10. Details in CURATION.md.
- Moving to New York next (3/10), the last city in this tier.

## 2026-07-23 — Istanbul: no new finds

- Next in the tier after Tokyo. Genuine search across all 8 missing trees; nothing cleared the licence bar, consistent with the same gap a prior run already hit here (anıtagac.istanbul has real photos of several of these but no stated reuse licence anywhere on the site). Recorded in CURATION.md; Istanbul stays at 2/10.
- Moving to Kyoto or New York next for the same tier's photo work.

## 2026-07-23 — Tokyo photo pass: 7/10 to 8/10 — second city to clear the floor

- With the marquee-European sweep closed, moved to the next tier (Istanbul, Kyoto, New York, Tokyo). Tokyo was closest to the 8/10 floor at 7/10.
- Found the one photo it needed: the Koishikawa Botanical Garden ginkgo tied to Hirase Sakugoro's 1896 sperm discovery, via a Commons category dedicated to that exact tree, and this time the tree itself is genuinely visible next to its own memorial stone (a near-identical-looking candidate was rejected in an earlier pass for showing only the marker). Checked the other 2 missing trees again with the same care; nothing else cleared the bar this pass.
- **Tokyo is now at 8/10, the second city on the site to clear the photo floor, after London.** Real evidence the target is reachable, not just a standard set for one city.
- Moving to Istanbul, Kyoto or New York next for the same tier's photo work when this run continues.

## 2026-07-23 — Madrid photo pass: 2/10 to 4/10, closing the marquee-European sweep

- Last city in this run's marquee-European pass. Found 2 CC BY-SA 4.0 photos via the Spanish Wikipedia's own singular-tree articles for the Real Jardín Botánico (the cypress and the Caucasian elm), both visually confirmed and GPS-close to this project's existing pins. Madrid now at 4/10.
- This closes the marquee-European-cities sweep started after Antwerp finished the lead group: Lisbon 3/10, Paris 6/10, Rome 5/10, Barcelona 4/10, Madrid 4/10. All below the 8/10 floor, all recorded honestly with what was tried and what wasn't found.
- Per the ladder, next photo-floor work would move to the next tier (Istanbul, Kyoto, New York, Tokyo), oldest-published first, once picked up again. Everything committed and pushed this run; a good stopping point.

## 2026-07-23 — Rome: no new finds; Barcelona photo pass: 2/10 to 4/10

- Continuing the marquee-European sweep. Rome (5/10) got a genuine search across its 5 missing trees; nothing cleared the licence bar, including a pond photo in Villa Doria Pamphilj checked and rejected for the same reason a prior run already flagged there (uncoordinated, can't confirm it's the same water feature as the Cedar of the Belvedere's own pin, in a park that's already had one cedar mixup).
- Barcelona (2/10) went better: found and approved 2, both from Wikimedia Commons's Jardí Botànic Vell (historic botanical garden) collection on Montjuïc, both visually confirmed as the actual named specimens rather than generic garden shots. Barcelona now at 4/10. Details in CURATION.md.
- Moving to Madrid next (2/10), the last marquee European city below floor.

## 2026-07-23 — Lisbon and Paris photo passes: no new finds, one lead flagged for Hidde

- Continuing the marquee-European-cities sweep after Antwerp closed the lead group. Lisbon (3/10) and Paris (6/10) each got a genuine search pass across Commons, iNaturalist, Flickr and Openverse for their remaining missing trees. Neither turned up anything that cleared the licence bar.
- Paris did turn up something worth a decision rather than a quiet skip: the City of Paris's own open-data photo set for remarkable trees has direct photos of the Buttes-Chaumont sequoia and sophora, both plausible matches, but each carries its own named copyright separate from the dataset's ODbL licence, so not verified open. Flagged for Hidde in CURATION.md in case he'd rather ask the city directly than have future runs keep circling it.
- Neither city's data changed this pass. Moving to Rome next (5/10), continuing oldest-published-first through the marquee European cities.

## 2026-07-23 — Antwerp photo pass: 0/10 to 5/10, and a real workflow upgrade

- Last lead-group city (Belgium), finishing the UK/Netherlands/Ireland/Belgium sweep the 2026-07-22 photo-floor decision started. Antwerp was the only lead-group city still fully unphotographed.
- Found and approved 5, all from the Flanders heritage agency's own image bank, CC BY 4.0: the Copper Beech of Sint-Willibrorduskerk, the Summer Linden of Rivierenhof, the Canadian Poplar of Eric Sasselaan, the Peace Tree of the Grote Markt, and a representative shot for the Park Trees of Den Brandt ensemble. Details and the one licence rejection (three Den Brandt Flickr photos, CC BY-NC-SA, not usable) in CURATION.md.
- Worth flagging clearly: this run actually looked at the photos rather than trusting captions and coordinates alone, fetching each candidate as a raw file and viewing it directly. Every prior photo pass in this project's history has noted "text workflow without image vision" as a real limitation and left ambiguous matches as `found_needs_check` rather than `approved`. That limitation turned out not to be true this run. Worth using on the whole site's backlog of unverified candidates and near-misses, not just new cities, since some rejected-for-caption-uncertainty photos might actually check out on sight.
- While correcting Rivierenhof's photo, caught its pin was about 480m off from the same heritage register's own coordinates for that tree; updated it, left as `approximate` since it's still not survey-grade.
- Also chased down a possible second, much older ginkgo that looked like it might belong in Antwerp's Stadspark instead of (or alongside) the current Millennium Ginkgo entry. Turned out to be a different park entirely (Tienen, not Antwerp) with the same common name. No change needed, recorded so nobody re-chases it.
- Antwerp at 5/10, below the floor, honestly. This closes the lead group: London 10/10, Edinburgh 4/10, Amsterdam 5/10, Dublin 3/10, Brussels 4/10, Antwerp 5/10. Moving to the marquee European cities next (Lisbon, Paris, Rome, Barcelona, Madrid), oldest-published first, and worth a second look with actual image verification rather than assuming prior passes already found everything findable.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-23 — Brussels photo pass: 0/10 to 4/10

- Second "rest of the lead group" city (Belgium), after Dublin. Found solid matches for the Kasterlinde (a Flanders heritage agency photo) and the Oriental Plane of Parc Leopold (captioned as this exact bicentennial tree), plus two good representative shots for the two ensemble entries (Bois de la Cambre, the Cinquantenaire chestnut avenue).
- Worth noting for a future run: Brussels' own official heritage inventory site (sites.heritage.brussels) returned a 403 to every fetch attempt this run, so its own tree photography, which likely exists given how thorough that register is, couldn't be checked. Worth another look with a different fetch approach.
- No open photo found for the remaining 6, including one near-miss caught properly: a purple beech candidate turned out to show ordinary gold autumn foliage, not the tree's actual purple leaves, so it wasn't used.
- Brussels at 4/10, below the floor, honestly. Antwerp next to finish the lead group, then the marquee European cities.

## 2026-07-23 — Dublin photo pass: 1/10 to 3/10

- First "rest of the lead group" city (Ireland) after UK and Netherlands. Found solid CC BY-SA matches for the St Anne's Park cypress sculpture and the Holm Oak Avenue, both pinned precisely by their Commons captions and categories.
- Found a third candidate, a plane tree at Trinity College, but couldn't confirm it's the New Square pair specifically rather than the separate Provost's Plane elsewhere on campus, so left it as found_needs_check instead of guessing.
- No photo anywhere open for the sequoia at the President's residence, the private-garden yew (expected, it's barely open to the public), Addison's Walk, the Provost's Plane itself, the Farmleigh sycamore, or the Corkagh oak avenue.
- Dublin at 3/10, below the floor, honestly. Moving to Brussels next, then Antwerp, to finish the lead group.

## 2026-07-23 — Amsterdam photo pass: 4/10 to 5/10 (plus one needing a visual check)

- Second focus-region city (Netherlands, after Edinburgh). Found a strong CC0 match for the Olifantsiep, whose Commons caption names its exact street corner. Found a public-domain candidate for the Lomanstraat tree tunnel too, but couldn't confirm from its description that the canopy effect is actually in frame, so left it as `found_needs_check` instead of approving it blind.
- No photo exists anywhere open for the Heimanseik (Artis keeps its own photography copyrighted), the Vondelpark poplar, the Hortus cycad, or the Amstelkade olive willow. For the cycad specifically, deliberately did not reach for a generic photo of the species from elsewhere, since this project already had to correct exactly that mistake once (a Kirstenbosch photo used for what should have been the Amsterdam specimen). Recorded all 4 as missing rather than stretched.
- Amsterdam at 5/10, below the floor, honestly.
- Moving to the rest of the lead group next (Dublin, Brussels, Antwerp), then the marquee European cities.

## 2026-07-23 — Edinburgh photo pass: 1/10 to 4/10, plus a live location fix

- Started the photo floor work from Hidde's 2026-07-22 decision (80% target, focus region UK/Netherlands first). Edinburgh was the weakest UK city, only London's already at 10/10.
- Hunted Commons/Geograph, iNaturalist, Flickr CC, Openverse and RBGE's own site for all 8 photo-less trees. Found and verified 3: the Sweet Chestnut, the Wentworth Elms of Holyroodhouse, and the Hermitage of Braid beech path (upgraded from a prior found_needs_check once re-verified against its Commons category and description).
- While verifying the Sweet Chestnut's photo, found the published entry had the wrong location: RBGE's own page for this tree says Pond Lawn, the data said Rock Garden. Fixed, since a wrong location is exactly the mistake this project can't afford.
- The other 6 (Cammo Ash, Cedar of Lebanon, Lauriston Castle monkey puzzles, St Cuthbert's Camperdown elm, the Cramond rockface sycamore, Corstorphine sycamore) have no open-licensed photo anywhere after a real search. Recorded in CURATION.md and left as missing rather than forced. Edinburgh sits at 4/10, below the floor, honestly.
- Moving to Amsterdam next for the same pass (Netherlands, focus region), then the rest of the lead group.

## 2026-07-22 15:35 — Antwerp: 15th city live, 10 trees researched

- Straight coverage after Brussels: no submissions, site healthy, nothing published wrong. Antwerp is a thinner data city than Brussels: no dedicated tree register, just Flanders' general heritage inventory, so most ages here are honest ranges (champion girths, protection dates) rather than planting records. Said so directly in the intro rather than dressing it up.
- Dropped one promising-looking candidate after checking it properly: the fig tree in the Rubenshuis garden has a genuine 1638 letter linking Rubens to fig trees in his own garden, but the tree standing there today is part of an explicit 2023 museum reconstruction, potted rather than planted, not a survivor. Including it would have implied a continuity that isn't real, so it's out.
- Also caught and fixed a location mixup mid-search: an early "540cm Canadian poplar" result was actually in Geraardsbergen, 40km away, not Antwerp. Found a genuinely Antwerp-located poplar of similar size at Eric Sasselaan instead.
- One young tree included on purpose: a Grote Markt linden planted in 1994 for the 50th anniversary of Antwerp's liberation, labelled "Youngest tree" so nobody mistakes precise 1994 dating for an old specimen.
- 0 of 10 photos found despite real searches; recorded honestly. Site rebuilt, all contracts validated, pushed.

## 2026-07-22 13:50 — Brussels: 14th city live, 10 trees researched

- Straight coverage after Edinburgh: no submissions, site healthy, nothing published wrong. Brussels turned out unusually well documented: the region has run its own official scientific inventory of remarkable trees since 2002, so most ages and girths here come from that register rather than estimation.
- Best story of the run: Parc du Cinquantenaire was built in 1880 for Belgium's 50th anniversary, and rather than planting saplings, city gardeners transplanted already mature trees in from an old cemetery and the Sonian Forest, so parts of the park looked centuries old on opening day. Used as the city's unifying thread.
- One correction worth flagging for whoever reads this next: a source claimed trees over 250 years old at the Boitsfort hippodrome, but that can't apply to the entry's own Douglas fir, since the species only reached Europe in 1827. Capped the age range instead of repeating an impossible number, the same discipline as catching a bad photo match.
- 0 of 10 photos found despite a real search; Brussels' trees are thoroughly documented in text but thinly photographed under open licenses. All 10 flagged missing honestly rather than guessed. The official inventory's own site likely has photos worth checking for licensing in a future pass.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-22 11:40 — Edinburgh: 13th city live, 10 trees researched

- Checked the ladder first: no reader submissions (CSV still just a header row), site builds clean, nothing published is wrong. Every one of the 12 live cities had already had a real photo-hunting pass earlier today (see the long run of entries below), each with genuine near-misses recorded, so doing it all again immediately would have been looping rather than progress. That put this run on coverage: the next pending city, Edinburgh.
- 10 trees, unifying thread is that Edinburgh's exposed hilltops rarely let a tree survive centuries in the open, so almost everything here owes its age to a wall someone built for other reasons: a castle courtyard, a botanic garden fence, a private estate, a churchyard, a royal palace garden.
- Judgement call worth flagging: dropped a strong candidate, the Robert Louis Stevenson yew at Colinton Manse (possibly the city's actual oldest tree, documented since 1638), because it stands in private grounds with no scheduled public access at all, only a glimpse over the churchyard wall. Different situation from Dublin's Old Glebe yew, which genuinely opens some weeks a year. Full reasoning in CURATION.md.
- 2 of 10 photos found and personally license-checked against their Commons file pages (Craigmillar Castle's yews, approved outright; the Hermitage of Braid's beech woodland, found_needs_check). 8 missing after real searches. One photo candidate for the Corstorphine sycamore was caught and rejected: its caption placed it at a different tree entirely (a conservation specimen at the Botanics, not the churchyard one).
- Site rebuilt, all contracts validated, pushed.

## 2026-07-22 09:45 — Kyoto: photo floor pass, 1/10 to 3/10

- Lead group and marquee-European cities are as far as prior runs could take them today, so moved to the next tier: Istanbul, Kyoto and New York. Kyoto (1/10) was oldest-published of the three and untouched this run, so went first.
- Found 2: the Weeping Cherry of Gion in Maruyama Park (CC BY 2.0, a Flickr-sourced Commons file with coordinates about 50m from the pin) and the Emperor's Camphor of Imakumano (CC BY-SA 4.0, a Commons file titled with the tree's own alternate name, "Shoryu Benzaiten," coordinates also about 50m from the pin). Both flagged `found_needs_check` since this is a text workflow without image vision.
- Kyoto now at 3/10. 7 remain missing after real searches, several with dedicated Commons categories that still turned up nothing tree-specific (Munakata Shrine's camphor, Nishi Honganji's famous inverted ginkgo, Sanbo-in's Taiko cherry). Left open rather than looped on.
- Site rebuilt, all contracts validated, pushed. Next: Istanbul or New York.

## 2026-07-22 09:15 — Tokyo photo pass: no new finds, honestly recorded

- Marquee-European sweep is closed out for this run, so checked the city closest to the floor overall: Tokyo at 7/10, needing just one more. Nothing cleared the bar this pass; one near-miss (a memorial-stone photo at Koishikawa Botanical Garden) checked and rejected since it documents the marker, not confirmed to show the tree itself.
- Recorded in CURATION.md so a future run knows this was tried. This closes a long run of photo-floor work: Amsterdam, Dublin, Lisbon, Paris, Rome, Barcelona and Madrid all got a genuine pass this session, plus this Tokyo check.

## 2026-07-22 08:55 — Madrid: photo floor pass, 1/10 to 2/10

- Last marquee-European city below floor after Barcelona. Found 1: the Bald Cypresses of the Crystal Palace Pond, CC BY-SA 4.0, the same photo already used on that tree's own Spanish Wikipedia article.
- Madrid now at 2/10. This closes the marquee-Europe sweep for this run: Lisbon, Paris, Rome, Barcelona and Madrid all got a genuine photo pass this session. None hit 8/10 outright, all moved forward, all gaps recorded honestly rather than papered over.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-22 08:25 — Barcelona: photo floor pass, 1/10 to 2/10

- Next oldest marquee-European city below floor after Rome, and the thinnest coverage in the queue at 1/10. Found 1: an aerial public-domain view of La Rambla's plane tree canopy, a good fit since that entry is already pinned as a 256-tree ensemble rather than a single specimen.
- Two near-misses rejected: a Carrer de la Encarnació street photo at the wrong building number with no tree visible, and Plaça de Prim's Commons files, none confirmed to show the ombú itself.
- Barcelona now at 2/10, smallest gain of the run so far. 8 stay missing after genuine attempts.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-22 07:55 — Rome: photo floor pass, 4/10 to 6/10

- Next oldest marquee-European city below floor after Paris. Found 2: the Quercia del Tasso (CC BY 2.0, also independently confirms the tree is a propped remnant, matching the existing honest framing) and the Cedar of the Garibaldi Mausoleum (CC BY-SA 4.0, GPS within 30m of the existing pin).
- One near-miss rejected: a Villa Doria Pamphilj cedar photo that looked right for the Cedar of the Belvedere but sits about 1.2km from that tree's pin in a large park with multiple documented cedars, likely a different specimen.
- Rome now at 6/10. 4 stay missing after genuine attempts, left open rather than looped on.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-22 07:20 — Paris: photo floor pass, 3/10 to 6/10

- Next oldest marquee-European city below the floor after Lisbon. Best hit rate of any photo pass this run: 3 of 7 missing trees found (the Buffon Plane, the Elm of Saint-Gervais, the Caucasian Elm of Avenue Foch), all clean matches with independently confirming detail in the file descriptions themselves.
- Paris now at 6/10, closest yet to the 8/10 floor. 4 stay missing after real attempts (the Second Robinier, the Sequoia of Buttes-Chaumont, the Parc Montsouris plane, the Sophora by the lake), left open rather than looped on.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-22 06:45 — Lisbon: photo floor pass, 3/10 to 5/10

- Lead group (London, Amsterdam, Dublin) is as far along as this run could get it; moved to marquee European cities next, oldest-first. Lisbon (3/10) was next.
- Found 2: the Praça Paiva Couceiro ginkgo (CC0) and the Jardim da Luz coral trees (CC BY-SA 4.0). One near-miss rejected: a silk floss tree photo that looked right by species and name but its coordinates put it 2.5km from the actual tree, a different specimen in a different neighbourhood.
- Lisbon now at 5/10, still short of the 8/10 floor. 5 trees remain `missing` after genuine attempts, left open for a future pass rather than looped on further.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-22 06:05 — Dublin photo pass: no new finds, honestly recorded

- Same rung as the Amsterdam pass just before it, continuing oldest-first down the focus region: Dublin (1/10) after Amsterdam (now 3/10). Searched Commons, iNaturalist and Flickr for all 9 missing trees.
- Nothing cleared the bar. Two near-misses checked and rejected: a general New Square photo that doesn't clearly show the champion plane trees themselves, and Aras an Uachtarain's well-documented Obama tree-planting photos, which are a different, newer tree from the one this city page needs.
- No file changes from the tree data itself; recorded in CURATION.md so a future run does not re-spend the same searches without knowing they were tried. Moving to the next focus-region city.

## 2026-07-22 05:40 — Amsterdam: photo floor pass, 2/10 to 3/10

- Hidde's new rung 4 (CLAUDE.md, decided 2026-07-22 while this run was already going): published cities below an 8-of-10 photo floor now outrank starting a new city, focus region first, oldest-first. Within the lead group, London is already at 10/10 and Dublin (just published this run, see below) was still ahead of me in the queue, so Amsterdam went first as the oldest lead-group city still below target.
- Found 1 of the 7 missing: a 1973 Nationaal Archief photo of the Amstelveld, CC0, correctly showing that square's trees but not a current-day image, so flagged rather than presented as-is. Amsterdam now at 3/10.
- The other 6 stayed `missing` after genuine searches, including two near-misses caught and rejected: a Hortus Botanicus cycad photo that doesn't identify which of the garden's several cycads it shows, and a same-species photo from Kirstenbosch, South Africa, that would have misrepresented a different continent's plant as the Amsterdam specimen.
- Did not reach the 8/10 floor this pass. Recorded in CURATION.md per the rule's own escape valve (record and move on rather than loop forever) and left open for a future pass. Continuing down the focus region: Dublin is next, since it also now sits below the same floor.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-22 04:20 — Dublin: 10 trees researched, twelfth city live

- Next pending city on the ladder, no reader submissions waiting and no city sitting at zero photos, so straight to coverage. Dublin joins the site with 10 trees in `data/cities/dublin.json`.
- The thread connecting all ten: Dublin's remarkable trees are civic and institutional rather than royal-forest survivors. A plane tree slowly eating a park bench at King's Inns, a giant sequoia Queen Victoria planted at the President's residence in 1861, two Georgian squares at Trinity, a dead cypress carved into a wildlife sculpture instead of felled, and three former private estates (Farmleigh, St Anne's, the Botanic Gardens) now open to everyone.
- 4 flagged, all for genuine reasons stated in the data: a disputed 500-700 year age range and unverified Swift legend for the oldest tree (a yew that only opens to the public a few weeks a year under a heritage tax scheme, disclosed honestly rather than glossed over); a chronology that doesn't add up for the Botanic Gardens' yew avenue; two Trinity College sources that disagree with each other on one plane tree's age; and a "220 years" claim for Farmleigh's oldest sycamore that traces to one repeated source rather than two independent ones.
- One near-miss worth recording: nearly used a walnut tree at a Tallaght priory (St Maelruain's Tree) as the oldest-tree candidate, but dropped it after research showed the site has no established public access, only a blogger's account of being personally let in by a groundskeeper. Not "genuinely open to visitors" under hard rule 10, so left out entirely rather than flagged.
- 1 photo found (the Hungry Tree, CC BY-SA 2.0 via Geograph), 9 missing after a real search across Commons, iNaturalist and Flickr for each named tree; nothing held the city back. The Hungry Tree is also the one pin marked `confirmed`, from a precise Wikipedia coordinate; the other nine are honestly `approximate`.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-22 03:10 — Istanbul: 0 photos to 2

- Same rung as the London pass just before it: a published city with zero photographs. Istanbul was the other one at zero. No reader submissions, site healthy.
- Only found 2 of 10 this time, and that is a coverage fact about Istanbul rather than a shortcut taken: Wikimedia Commons simply has far less documentation of Istanbul's monument trees than of London's. Searched Commons in English and Turkish, plus iNaturalist, Flickr and Openverse, before accepting that.
- Got: the Hüseyin Avni Dede Plane (its photo's own GPS lands about 50m from the existing pin, a nice bonus confirmation) and the Karacaahmet cypresses (a general shot of the cemetery's cypress canopy, honestly not tied to one of the nine specific protected trunks, matching that entry's existing caveat).
- The other 8 stay `missing`, per the mandate: photo coverage is always cuttable, so this moves on rather than digging further for a fifth or sixth find. Good candidates for a future improvement-mode pass.
- Site rebuilt, all contracts validated, pushed. Both zero-photo cities are cleared; Singapore is next.

## 2026-07-22 02:15 — London: 0 photos to 10

- No reader submissions (CSV checked: header row only, no data rows). Site build was healthy. That put rung 4 on top of the ladder: a published city with zero photographs, which outranks starting the next pending city (Singapore). London and Istanbul were both at zero; London went first as the older of the two.
- All 10 London trees now have a Wikimedia Commons photo with a checked licence (CC0, CC BY or CC BY-SA) and attribution, status `found_needs_check` pending your eye. Every file page and licence tag was independently verified, not taken on trust.
- Found a real fact error while at it: the Fulham Palace Oak was recorded as a Pedunculate Oak. It is a Holm Oak, per the Palace's own site plus an independent source, and quite possibly the oldest holm oak in the country. Fixed the species, age range and story, added two sources.
- Barney the Plane's pin got more precise (exact EXIF coordinates from a geotagged photo captioned with its name) but stays `location_precision: approximate` on purpose, since only one source names this specific tree so far.
- Site rebuilt, all contracts validated, pushed. Istanbul is next for the same zero-photo pass, then Singapore.

## 2026-07-22 01:00 — New York researched and live: 11 cities, 110 trees

- No reader submissions (CSV checked: header row only). Site healthy, nothing published was wrong, so went to the next rung: the next pending city, New York.
- 10 trees researched, written and shipped, deliberately two per borough. The throughline: NYC runs its own government Great Trees registry (since 1985, expanded 2024), and every tree here carries that official designation. Full detail and what's flagged in CURATION.md.
- One tree dropped after research, not before: Flushing's famous Weeping Beech, NYC's first living landmark, died in 1998 and got a public funeral. Would have been a great story on a dead tree; replaced with a living one from the same historic nursery grounds instead, same rule that's kept dead trees off other cities' lists as if they were alive.
- 2 of 10 photos found: the Camperdown Elm and the Queens Giant, both CC BY-SA on Wikimedia Commons. The Queens Giant photo's own GPS metadata gave an unusually precise, confirmed coordinate for the tree itself, one of the few trees on this whole site with a truly surveyed pin rather than an estimate.
- 8 of 10 pins approximate otherwise, honestly: most sources only gave building or park-level coordinates, not a surveyed point for the specific trunk.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-21 23:45 — Madrid researched and live: 10 cities, 100 trees

- No reader submissions (CSV checked: header row only). Site healthy, nothing published was wrong, so went to the next rung: the next pending city, Madrid.
- 10 trees researched, written and shipped. The throughline: almost every remarkable tree here is a foreign import planted by royal gardeners testing what could survive Madrid's climate, a Mexican cypress, a Himalayan cedar, an Atlas cedar, a Caucasus elm. Full detail and what's flagged in CURATION.md.
- Two research near-misses caught before they shipped, both location errors: a "1,000-year yew" and a "41-metre sequoia" that first looked like Madrid candidates turned out to be in Rascafria and El Escorial/Aranjuez, separate towns in the wider region, not Madrid city. A supposed Casa de Campo oak, "Encina del Mesto," turned out on checking coordinates to be a same-named tree in a different municipality entirely. All three swapped out or dropped rather than shipped on a name match.
- 1 of 10 photos found: the Ahuehuete, Madrid's presumed oldest tree, public domain via a university archive upload, confirmed to be the right tree by its file description.
- All 10 pins approximate this round, honestly: most sources gave building or park-level coordinates rather than a surveyed point for the tree itself, and no source closed that gap. Nothing here claims precision it doesn't have.
- One age dispute worth a look if you know Madrid: the Ahuehuete's popular 1633 planting date (390 years) versus city arborists' own ~200 year estimate. Presented as a range rather than picked.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-21 22:30 — Kyoto researched and live: 9 cities, 90 trees

- No reader submissions (CSV checked: header row only). Site healthy, nothing published was wrong, so went to the next rung: the next pending city, Kyoto.
- 10 trees researched, written and shipped. The throughline: unlike most cities so far, none of Kyoto's ten are wild trees that happened to survive in a park. All ten are cultivated specimens shaped by centuries of temple and shrine care, including a shogun's bonsai trained into a boat shape and a pine bent flat and named for a dragon in 1857. Full detail and what's flagged in CURATION.md.
- Caught a real near-miss before it shipped: Shimogamo Shrine's most famous sacred tree, revered as the oldest in its forest, turned out to have fallen down on 2026-06-16, a month before this run. Would have been an easy thing to miss and publish as living.
- 1 of 10 photos found: the ~600-year-old Land Boat Pine at Kinkaku-ji, CC BY-SA on Wikimedia Commons, confirmed by GPS metadata to be the right tree.
- 6 of 10 pins approximate, honestly: several temple trees only have building-level coordinates confirmed, not a surveyed point for the tree itself inside the grounds. One tree, a 1,200-year cedar in a remote forest northwest of the city, turned out to have real restricted access (prior arrangement with the city and a guide required); included anyway with that stated plainly in the access field rather than smoothed over.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-21 21:15 — Barcelona researched and live: 8 cities, 80 trees

- No reader submissions (CSV checked: header row only). Site was healthy, nothing published was wrong, so went to the next rung: the next pending city, Barcelona.
- 10 trees researched, written and shipped. The throughline: Barcelona keeps two tree registries, a broad municipal catalogue and a much stricter Catalan government "monumental" list held by only four trees citywide, all four sharing one ravine in the historic botanical garden, declared together in April 2025. Used that as the city intro.
- Two of the ten grew up inside Park Guell before Gaudi built it: one still roots beneath the viaduct's stone columns, the other is a 1907 regrowth shoot from a much bigger carob that died back, ringed by its own dead wood. Full detail and what's flagged in CURATION.md.
- 1 of 10 photos found: a public-domain 1904 photo of the viaduct carob, confirmed as the right tree. Caught a near-miss on tree #1's photo, a similarly named Wikimedia file turned out to be a different holm oak entirely on checking the file page directly; not used.
- 5 of 10 pins approximate, honestly: two botanical-garden trees and one Laberint d'Horta tree have only the park's entrance coordinates, not a surveyed point inside the fenced ravine; the Encarnacio oak has no surveyed lat/long in any source; the Rambla plane trees are pinned as the ensemble they are, not one tree standing in for 256.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-21 20:00 — Istanbul researched and live: 7 cities, 70 trees

- No reader submissions yet (checked the CSV, header row only). Site was healthy (build clean, contracts passing), nothing published was wrong, so went straight to the next pending city per the ladder: Istanbul.
- 10 trees researched, written and shipped. Istanbul's oldest tree, a 1,300-1,400 year old plane, turned up in an unlikely place: a university forestry research forest in Bahçeköy, not a palace or a mosque. Two more protected monumental trees share that same forest.
- The throughline that fell out of the research: Istanbul's grandest, most photographed old trees mostly did not make it. The plane said to have witnessed the 1453 conquest inside Topkapı Palace died by 1928; Dolmabahçe's palace planes were felled for canker disease in 2022. What survived instead is unglamorous: a working forest, a bazaar entrance where a poet has sat under the same tree since 1964, a cemetery, a storm-toppled plane in Çengelköy that city crews nursed back to life after 2017. Used that as the city intro.
- One judgement call worth flagging: several sources described a Çengelköy plane as "780 years old" with a 1993 death under a falling branch. I could not confirm that claim and this storm-survivor tree are the same specimen, so I dropped the unverifiable parts and told the story I could actually source: uprooted by a 2017 storm, replanted and still recovering. Better story, and true.
- 4 of 10 flagged for disputed ages or thin sourcing (two of the Bahçeköy forest trees, the Karacaahmet cemetery cypresses, the Florya mastic tree). Full detail in CURATION.md.
- 0 of 10 photos found this round. Searched Wikimedia Commons for every tree; nothing came back as a confident match to the specific named tree, so all ten are `missing` rather than guessed. Worth another pass, especially Küçük Çamlıca, Büyükada and Beyazıt, which are touristy enough that photos likely exist somewhere.
- 8 of 10 pins approximate (forest, park, cemetery or meadow locations with no street-level source for the exact tree), 2 confirmed. No pin claims more precision than it has.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-21 18:30 — Tokyo researched and live: 6 cities, 60 trees

- No reader submissions yet (checked the CSV, header row only). Site was healthy (build clean, contracts passing), nothing published was wrong, so went straight to the next pending city per the ladder.
- Tokyo: 10 trees researched, written and shipped. Zenpukuji's 750-year-old ginkgo leads as Tokyo's oldest living tree; Sensoji's war-scarred ginkgo, Ueno Toshogu's 600-year camphor, and Meiji Jingu's ginkgo avenue and camphor couple round out the list. Full detail and what's flagged is in CURATION.md.
- The throughline that fell out of the research: Tokyo has burned down repeatedly (1657, 1868, 1923, 1945), and five of the ten surviving trees are ginkgos, a species whose wood resists catching fire. Used that as the city intro instead of a generic "remarkable trees of Tokyo" opener.
- 7 of 10 photos found on Wikimedia Commons (open licenses, awaiting your approval like always). 3 missing, none faked.
- 6 of 10 pins confirmed, 4 approximate (all cases of a tree inside a large garden or spanning an avenue rather than a single small address). No pin claims more precision than it has.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-21 17:00 — The funnel, thought through properly

Hidde asked for this while away. Written to be read cold.

**The funnel today, honestly:**

1. Someone finds the site. Nobody does. No distribution has happened, and the domain is new, so organic search will take months, not weeks.
2. They land on a city or tree page. These are good: story, map, directions, nearby trees.
3. They read.
4. They walk to a tree. Nothing bridges this, and it is where the product lives or dies.
5. They return, or pay. No mechanism, no evidence anyone would.

**The leak nobody is looking at is step 3 to 4.** Everyone is worried about step 1, and step 1 is real, but it is not the part we control. Someone reads about the Heimanseik at 22:00 on a Tuesday, thinks "nice", and never goes. The whole product is a destination read indoors, while the value only happens outdoors, on another day. Nothing currently carries the intent across that gap.

Three things close it, in order of how much they help:
- **A reason to go now.** Seasonality is the strongest and we have none of it: catkins, blossom, autumn colour, the month a given tree is worth the trip. That is knowledge nobody else has, it is cheap to research alongside the trees themselves, and it converts "nice" into "this weekend".
- **A way to keep it.** Saving a tree or a route for later, in LocalStorage, no account. Cheap, and it is the only thing that survives closing the tab.
- **The walk.** Built 2026-07-21. Turns ten scattered facts into one afternoon.

**On measurement, which is what makes the rest answerable.** Cloudflare analytics went live today, so within days we will know whether anyone arrives at all and which pages they land on. That is the first real signal this project has ever had. Note what it cannot see: whether anyone actually walked. Nothing on a website can see that, and pretending otherwise would be the wrong thing to build.

**The uncomfortable conclusion.** Every funnel improvement below step 1 multiplies a number that is currently zero. Distribution is the only step that changes the zero, and it cannot be automated: it needs Hidde to tell actual people this exists, once. Until that happens, more cities is the right work (it builds the SEO base that pays off in months) but it produces no learning at all. Runs should keep going wide, and nobody should mistake that for progress on the question of whether anyone cares.

FOR HIDDE: one post, one link, to any group of people who like trees or like Amsterdam. That is the whole ask, and it is worth more than the next twenty cities.

## 2026-07-21 10:15 — Paris pulled above the quality floor instead of starting city six

- Priority ladder in CLAUDE.md (rung 3, quality floor) beat rung 4 (next pending city, Tokyo): with the honest `location_precision` count from the previous run, Paris and Amsterdam were both below floor, and Paris was worse (8 of 10 approximate, 2 of 10 photos).
- Resolved all 8 approximate Paris pins to confirmed. Five city park/avenue trees matched against the Ville de Paris open tree registry (opendata.paris.fr); the three Jardin des Plantes trees aren't in that dataset at all (the garden belongs to the Museum national d'Histoire Naturelle, not the city) so those came from OpenStreetMap's individually named heritage-tree nodes instead, cross-checked against sourced planting dates.
- Added one photo (Great Plane of Parc Monceau, Public Domain), clearing Paris's photo floor too.
- Paris now has 0 approximate pins and 3 of 10 photos. Full detail in CURATION.md.
- Amsterdam is still below floor (7 of 10 approximate, 2 of 10 photos) and is next in line for the same treatment, ahead of Tokyo.

## 2026-07-21 09:00 — Every pin now says honestly how precise it is

- Set `location_precision` explicitly on all 50 trees. It was set on none of them, despite CLAUDE.md requiring it on every tree.
- The site had been guessing instead: `location_is_approximate()` sniffed free-text notes for ten hardcoded phrases like "exact position". Trees whose notes described a rough pin in any other wording rendered as confident pins with no warning.
- Six trees were lying to visitors that way. Adonis in Villa Borghese is the clearest: its note says the coordinates point at the Valle dei Platani generally, "not Adonis's specific trunk", and the page showed no warning. Same for the Hortus cycad, the Amstelveld wingnuts, the Rijksmuseum wingnut, the Belvedere cedar and Barney.
- Replaced the keyword guessing with the field alone, and made a missing field count as approximate. A warning nobody needed costs a visitor nothing; a missing one costs them a wasted walk.
- Result: 25 of 50 pins are approximate. That is high, and it is the real number. It also says where the improvement runs should go first: Paris (8 of 10) and Amsterdam (7 of 10).

## 2026-07-21 — Working agreement set up

- Added this log, plus a priority ladder and decision boundary in CLAUDE.md, so runs know what to work on and what to leave alone.
- Nothing about the site itself changed.
- FOR HIDDE: the boundary is in CLAUDE.md under "What runs decide alone". If anything in the "ask first" column feels too strict or too loose, move it. That list is the whole steering wheel.
