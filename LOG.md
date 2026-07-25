# LOG

What the autonomous runs did, newest first. One entry per run that actually changed something. Hidde reads this to catch up, and says good or bad.

Format, deliberately short:

```
## YYYY-MM-DD HH:MM — what it did in one line
- What changed (files, pages, cities)
- Why, if it was a judgement call
- FOR HIDDE: only when something genuinely needs him. Otherwise leave it out.
```

If an entry has no `FOR HIDDE` line, nothing is waiting on you. That is the normal case.

---

# Open with Hidde

Standing list. Everything else in this file is history; this block is what is actually waiting.

### 1. ~~Make the submission form~~ — DONE 2026-07-21

Form is live and wired in. Every contribution button on the site points at it, and
runs read the published CSV (email column excluded, so no address ever reaches a
run or the public sheet). Form: `SUBMISSION_FORM_URL`, responses:
`SUBMISSIONS_CSV_URL`, both in `scripts/build_site.py`.

Only thing left on Hidde: nothing, until submissions arrive. Then he may want to
mail the people who left an address to say their tree went live. That list lives
in the private column of his own spreadsheet.

### 2. Illustrated icons (needs Hidde's eye, do it together)

Map pins should move to the painterly style he asked for, and to leaf shapes so species actually differ. Six of Lisbon's ten trees still share one broadleaf silhouette. Deliberately not started alone: it is taste work.

### 3. Unanswered question

He said "je kan niet de website gratis maken". Everything so far assumes the opposite: the site stays free forever because it is the entire acquisition engine (blueprint P9), and the app is what people pay for. Worth settling, because it changes a lot.

### 4. Later, not now

Analytics once there is traffic, and cookieless to avoid a consent banner. Search Console reading needs his Google credentials; no data worth reading yet.

---

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
