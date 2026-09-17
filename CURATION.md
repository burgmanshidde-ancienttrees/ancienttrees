


**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-08](archive/CURATION-2026-08.md)
- [2026-07](archive/CURATION-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-09](archive/CURATION-2026-09.md)
- [2026-08](archive/CURATION-2026-08.md)
- [2026-07](archive/CURATION-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
<!-- archive-index -->
## 2026-09-17 (continuation 11) - Enschede/Helmond write pass merged, Alkmaar verify dispatched

Followed the run prompt's "write pass first, whenever there is one to do" rule.
`prepare.py` showed 3 fully verified trees sitting unmerged (ens_014, ens_015
in `data/research/enschede-verified.json`; hlm_019 in
`data/research/helmond-verified.json`, all left by continuation 10). Claimed
both cities for write, dispatched a write-stories pass, and merged the result:
**Enschede 13 -> 15 trees, Helmond 18 -> 19 trees.** Fixed one species-name
drift at merge time (the writer delivered "Common Hornbeam", the site already
uses "Hornbeam (Carpinus betulus)" everywhere else) and updated both cities'
count promises (meta_description, question_meta, question_context, and
Helmond's "are they free to visit" FAQ, which listed every access group by
name and needed the new Croylaan oak added to it, since it is council land
beside a public road rather than inside the private castle grounds it
approaches).

With the shelf otherwise thin (48 cities staged for verify but none with an
unmerged write ready), dispatched a fresh verify pass on **Alkmaar** (7/20
trees, 361 unmined Dutch LRMB register candidates, real demand at 12
impressions/10d) rather than touching Enschede or Helmond again in parallel,
to avoid two agents writing the same delivery file at once. Brief steered it
toward forming a new tight walkable cluster rather than adding scattered
singletons to a city that already spans 10.9 km.

## 2026-09-17 (continuation 10) - Tallinn register pool confirmed exhausted a second time, claim released

Resumed a window an earlier attempt stopped in with 4 claims standing
(helmond, enschede, tallinn, eindhoven, all verify). Enschede and Helmond
each already had a `-verified.json` file with a story-ready tree
(ens_014, ens_015, hlm_019) sitting unmerged; dispatched a write-stories
pass on those rather than re-verifying.

Read Tallinn's brief before dispatching a verify pass on it, per the
"finish it or release it" rule. The remaining 52 unmined register
candidates are almost entirely ornamental cultivars already carrying a
`lead:` verdict from the 2026-09-12/13 passes (copper beeches, globe
maples, pyramid oaks, weeping cultivars, none with an age or story), one
dead tree, and 3 already-BLOCKED entries. The Wikidata sweep's 6
candidates are the same already-blocked black poplar plus outliers
10-20km out. Nothing here clears the bar. Released the claim rather than
burn a 40-minute pass re-confirming what the 2026-09-12/13 passes already
found; `city_queue.py --next` should move past Tallinn now that this is
on record twice.

## 2026-09-17 (continuation 9) - Houston and Vancouver: write pass on 5 bought-and-paid-for trees, city grows to 6 and 7

A prior attempt this window stopped with two write claims still standing on
data/in-flight.json (Vancouver, Houston) whose verify work had already landed
(064ae72a). Released the stale claims, deleted the now-merged enschede-verified.json
research file (its only entry, ens_013, was already published), then re-claimed
both for a write pass.

**5 fully verified register trees written and merged**: hou_005 (The Rienzi
Yaupon, a yaupon holly grown to tree height in the Museum of Fine Arts' Rienzi
garden, state champion class) and hou_006 (The Russ Pitman Mexican White Oak,
Bellaire) from the Texas Big Tree Registry; van_005 (The Dunbar Street Beech),
van_006 (The West 20th Avenue Sweet Chestnut) and van_007 (The Blenheim Street
Oak) from Vancouver's Heritage Register cross-checked against the city's
separate street-tree inventory. None has a documented age; all five say so
plainly and ask the reader. Houston grows from 4 to 6 trees, Vancouver from 4
to 7.

Normalised 3 species-field collisions the write pass correctly left alone
(verified fields): "Spanish Chestnut" -> "Sweet Chestnut" (Castanea sativa,
matching 23 other published trees), "Mexican White Oak / Monterrey Oak" ->
"Mexican White Oak" (matching 2 others), and van_007's multi-clause dispute
field shortened to the existing convention "Oak (Quercus sp.)" (the dispute
itself stays fully told in the story and how_to_recognise).

Fixed the count-promise copy both cities' new trees broke (Houston's intro/
meta_description/question_meta said "four"/"three more", Vancouver's said
"Full list of 4"/"the four"/"All four"), rebuilt clean, qa.py and preflight.py
both pass (0 problems).

**Also fixed in passing: Houston was missing from data/city-list.json
entirely**, since the city was first opened (0339be59), despite its page
being live and built. This is why feed.xml.ts's `updateFirstSeen()` (which
iterates city-list.json's `cities` array) had never stamped hou_001-004 into
data/first-seen.json either, though the pages themselves built fine via a
different, direct-directory-scan path. Added the missing entry (status
published, trees 6) and corrected Vancouver's stale `trees: 4`. Also bumped
united-states.json's meta_description tree count (249 -> 251) since the two
new Houston trees pushed it stale immediately.

Both claims released. Cost logged to data/agent-costs.json (write, 5 trees,
133k tokens).

## 2026-09-17 (continuation 8) - Ischia settled to a leads verdict, Marthalen Oak photographed, two register-backed verify passes dispatched (Vancouver, Houston)

**Ischia given the same leads-file treatment as Ravenna**: 3 MASAF candidates
2.3-17km apart, below both the six-candidate verify floor and the four-tree
page floor. Written to `data/leads/ischia.json`; `city_queue.py --next` no
longer recommends it.

**The Marthalen Oak (Zurich's mar_001) now has a photograph**, the one
candidate `photo_gaps.py --shortlist` printed today. Six of eight queued
candidates carry a geotag matching our pin within metres, all CC BY 3.0 from
the same photographer (Kurt Spalinger-Røes) via a 2015 Panoramio upload.
Approved the full-height shot (panoramio (2), 2332x4992) as the lead: the oak
is unmistakably taller than the surrounding beeches, in leaf, good daylight.
Added the trunk-plaque close-up (panoramio (1)) as a second photo per the
2026-09-12 `photos` field: it independently confirms the exact figures our
story already cites from the Ortsmuseum (34m tall, 5.60m round, ~360 years),
which is about as strong a corroboration as a photograph can give. Added
`height_m: 34` from the same plaque.

**Two register-backed verify passes dispatched** on cities from Hidde's 2026-08-19
named-cities list (from-zero web research explicitly on, growing toward the
10-tree target): Vancouver (15 remaining unmined leads from the City of
Vancouver Heritage Register, an Open Government Licence source already used
for its 4 published trees) and Houston (10 unmined Texas Big Tree Registry
leads, non-commercial licence so lead-only, needs an independent second
source per tree). Both claimed in data/in-flight.json; results pending.

## 2026-09-17 (continuation 7) - Ravenna settled to a leads-file verdict, a photo-queue cleanup pass, one new photo (Montreal)

**Ravenna given a written leads-file verdict**, closing a gap the 2026-09-17
continuation-5 fix (`settled_verdict()` in city_queue.py) didn't yet cover:
Ravenna had been checked and passed over as too thin five separate times
(2026-09-11, 09-12, 09-13, 09-16, this pass) but never got a `data/leads/`
file of its own, so it kept resurfacing on `city_queue.py --next`'s OPENABLE
list. Wrote `data/leads/ravenna.json` with the verdict (4 MASAF register
candidates, one near the centre and three 17-19km out, none forming a
walkable cluster, below the six-candidate floor); re-ran `city_queue.py`
(no flags) to regenerate data/city-queue.json/CITY_QUEUE.md/city-list.json/
LEDGER.html, and Ravenna now prints under SETTLED rather than OPENABLE.

Also checked Ischia (register=2, 3 unmined candidates 2.3-17km apart, same
thin-and-spread shape, not written to a leads file this pass since only one
brief was read) and Ottawa/Caserta/Tilburg (all already fully judged-negative
photo queues from earlier passes, not fresh gaps).

**Photo queue cleanup: a viewing pass on the biggest zero-photo cities'
queued candidates**, per the 2026-09-01 ruling that a night run may take a
viewing pass. `leads.py --ready` was empty (0 READY) at session start, so
this filled the window instead of a write pass. Fetched and judged every
unjudged candidate for Leeuwarden (41 trees, 0 photos, the single biggest
gap), Haarlem, Maastricht, Eindhoven, Zwolle, Spokane, Rotterdam, Hobart and
Rouen: 39 rejected, 2 held (Haarlem's Kenaupark lime: two candidates show
the right park but at least two similar bare limes stand near the same
lawn, and our own how_to_recognise line singles this one out as "the
youngest," which no photograph can confirm without a nameplate), 1 approved
(Montreal's mtl_013, the McGill Katsura: an iNaturalist courtyard photo
whose own coordinate sits about 13m from our pin, species independently
confirmed by the same observation's leaf close-up).

The pattern worth recording for the next pass: nearly every queued
candidate for these cities was a false positive from name/address matching
rather than an actual photo of the tree, in three repeatable shapes. Dutch
municipal heritage-building surveys (Commons titles like "Zwolle GM
<street address>" or "<Street> N, Zwolle") photograph the FACADE at a
monument's address, not the street tree beside it; all 12 of Zwolle's
candidates and 2 of Haarlem's were this. Archival black-and-white material
(a 1910 postcard, RCE facade surveys, a glass-plate lane scan, funeral and
ceremony photos) came up repeatedly and is banned outright regardless of
subject. And keyword collisions produced outright wrong subjects: a
different, famous Californian redwood matched on "redwood," a Bonnie-and-
Clyde mugshot matched on "Champion," a gravestone matched on the
deceased's own park-adjacent name.

Rebuilt (`npx astro build`, needed a fresh `npm install`, no node_modules
this session) and ran `scripts/qa.py`: 8887 pages, clean. `preflight.py`:
0 problems.

Released a standing claim rather than starting fresh: an earlier attempt in
this same window had already run a verify pass and left its finding on disk
(`data/research/enschede-verified.json`), uncommitted. One candidate: ens_013,
"The Sweet Birch of the Oosterbegraafplaats" (Betula lenta), the fourth
register-designated tree on the Oosterbegraafplaats cemetery alongside
ens_008/009/010 (Hungarian Oak, Sweet Gum, Oriental Spruce). Netherlands
LRMB register nr 1692854 is the primary source (dendrological grounds, no
age or planting history recorded); monumentaltrees.com independently lists
the same specimen and was used only to corroborate species, girth (234cm)
and height (~18m), never as the sole source, per hard rule 1. No age is
documented anywhere, so `age_estimate` stays empty rather than guessed, same
as ens_010's spruce.

Wrote the story myself (one tree, below the six-candidate write-pass
batching floor) and merged it into data/cities/enschede.json. Fixed the
city's meta_description and question_meta, both of which still said twelve
trees. Ran a full `npx astro build` and `scripts/qa.py` against the built
output (both needed a fresh `npm install`, site/ had no node_modules this
session): 5745 pages built, QA clean. preflight.py and superlatives.py also
pass clean (one unrelated pre-existing FAIL on preflight was the enschede
count itself, now fixed; everything else it prints is pre-existing NOTEs
elsewhere in the corpus). Photo still missing (13 of 13 for this city).

Also confirmed rather than re-investigated: the two rung-2 alerts from
session start are both already-known non-issues. Weekly analysis's failure
on 2026-09-14 matches the documented usage-limit-death fingerprint exactly
(1 turn, 0 cost, <1s) and `scripts/health.py` says so outright; the iOS
app's newest failure (2026-09-16) is the same already-documented flaky tap
race in `FlowWalk.swift` (`testEveryFlowLeavesAWayBack` failing to find
"person-more"), already recorded as FOR HIDDE (needs a workflow-scoped push
token this bot's token does not have) as recently as 2026-09-16. Neither
needed new work.

## 2026-09-17 (continuation) - Florence 26 -> 27; city_queue.py stops re-recommending settled dead ends

Picked up two claims an earlier attempt in this window left standing. Vilnius's
verify work (register confirmed exhausted) was already done and logged in the
entry below; released the claim, nothing further to do.

**Florence 26 -> 27**, flo_027, "The Hackberries of Piazza Vasari" (Mediterranean
Hackberry, three MASAF register twins folded into one entry per the register-
twins rule, girth 407cm). Resolves a stale "Three Hackberries of the Cascine"
lead: the name was wrong (Piazza Giorgio Vasari in Campo di Marte, not the
actual Cascine park 4-5km away), and settles an "alive now" question that had
stalled two earlier passes: RFI announced felling 21 trees in this garden in
November 2025 for a railway-bridge rebuild, but La Nazione states plainly the
historic/monumental trees were excluded, and RAMI's own page shows the pinned
tree measured healthy on 14 Oct 2025, weeks before the felling. Four sources.
Also checked and closed: the Isolotto poplar candidate turned out to already
be published (flo_026, same MASAF sheet id, missed by the dispatched pass's
own search); two more candidates confirmed comune Fiesole, not Florence
(matching two already-flagged Wikidata wrong_city leads). Story written and
merged by the session (one tree, below the six-candidate write-pass batching
floor); Italian overlay (data/i18n/it/florence.json) updated in the same
commit, including the stale "26 giganti" count in its title/meta_description.

**city_queue.py --next was re-recommending cities an earlier pass had already
settled as dead ends**, discovered while picking a new-coverage target: Dubai
and Taormina each carry a written verdict in their own `data/leads/*.json`
file (no publishable supply; every register tree on private hotel grounds),
but neither note was ever read by the queue script, so both kept printing as
openable. This exact rediscovery is logged across at least seven sessions
since 2026-09-08 (Taormina alone: 09-08, 09-11, 09-12, 09-13 x3, 09-16).
Added `settled_verdict()` to scripts/city_queue.py: it matches a leads file by
slug and checks its `note` for verdict phrasing already in use ("VERDICT:",
"kept so nobody re-run", "do not re-run/re-research this"); settled cities
move to a new SETTLED section instead of OPENABLE/NAMED BY HIDDE/movable.
While checking the remaining OPENABLE list, found the same failure one layer
deeper: Trier's supply (9 register rows, 4 Wikidata candidates) is entirely
cross-border Luxembourg trees (Rosport-Mompach, Mertert, Manternach,
Echternach, Berdorf, Flaxweiler communes, 10.7-21km out), matched by raw
distance with no jurisdiction check, the same mistake already recorded for
Florence/Fiesole. Wrote a settled verdict for Trier too. The remaining
OPENABLE cities (Adelaide, Zagreb, Lagos, Ravenna, Niagara Falls, Wellington,
Mechelen, Gran Canaria, Kilkenny, Ischia, Izmir, Stirling, Canterbury, Evora,
Stratford-upon-Avon, La Palma) all sit at 0-2 register rows plus 1-8 Wikidata
leads, well below the six-candidate floor; not dispatched.

Confirmed the iOS app's newest CI failure (`testEveryFlowLeavesAWayBack`,
floor job, 2026-09-16) is the same documented flaky tap race already recorded
in FlowWalk.swift's own comments and `drafts/ios-floor-retry.patch` (FOR
HIDDE: the fix needs a `workflow`-scoped push token this bot does not have,
reconfirmed 2026-09-16). Not re-attempted.

`python3 scripts/qa.py`, `preflight.py` and `superlatives.py` all pass clean.

## 2026-09-17 - Milan 29 -> 30, target reached; Vilnius register confirmed exhausted

Two parallel verify passes on the depth-allowed roster (DATA.md 2026-09-15: alicante and krakow were already at/above target despite showing in the queue's "staged for verify" list, so picked the two below instead, both below target with real register supply).

**Milan** delivered one tree, mil_030, Il Bagolaro di Villa Ghirlanda: a Celtis australis, 445cm girth, 34m tall, in the public park of Villa Ghirlanda Silva at Cinisello Balsamo (about 8km north of central Milan), where 19th-century garden theorist Ercole Silva first tried out the English-garden style he then wrote a book about. Two sources (MASAF register plus a directly-fetched 2023 local news piece on the comune's own sensory-map project). This closes Milan at its CITY_QUEUE.md target of 30; the near-centre register (10 rows within 2.3km) is fully exhausted, all duplicates or already-blocked. Story written and merged by the session (not a write-stories pass, since one tree does not clear the six-candidate batching floor); intro/meta_description/question_meta count references updated (29 -> 30), Italian overlay (data/i18n/it/milan.json) translated and updated in the same commit so the build's overlay-completeness gate did not go red. Build and qa.py both pass.

**Vilnius** delivered zero new trees: the register (40 candidates within 20km) was already fully mined by three prior passes (08-16, 08-17, 08-31). This pass closed two open judgement calls instead: a maple circle in the P.Vileišis palace courtyard moved lead->blocked (the courtyard's own Lithuanian Wikipedia page says it's locked, inaccessible), and the Presidential park oaks moved lead->blocked (public park, but every visitor is searched by security at entry, hard rule 10's own "guard who checks: no" case). Two stale/duplicate leads closed. Vilnius stays at 14 trees; nothing left to mine there without a fresh register or a Hidde-named from-zero pass.

Also processed 2 reader submissions (#111, #112) and logged both passes to data/agent-costs.json.

## 2026-09-17 - Submissions #111, #112 (Taketa): two more GPS-only pins at Oka Castle, same submitter as #110

Same reader (user_id a8ca51da-...) who sent #110 from the Oguni/Taketa border
yesterday, now two pins a day later, 290m apart, both landing inside the Oka
Castle ruins (Oka-jo) national historic site in Taketa, Oita: 32.96713,131.40504
and 32.96912,131.40796. Both kind `tree`, app Collect flow, no name, no
species, no girth, no `why`, and no matching row in the `sightings` table for
either tree id, so no photo ever arrived despite the app's copy promising one
travels with the add.

Checked data/registers/japan-bunkacho.json: nothing within 25km of either
point. Web search confirms the coordinates are Oka Castle itself; its
documented trees are planted cherry and maple for seasonal colour (one of
Japan's 100 best cherry-viewing spots), not a named ancient specimen, and no
giant tree at the site turned up in English or Japanese search. An Overpass
check for natural=tree within 400m of both points timed out (server
overloaded, consistent with the standing blocklist note) and was not retried.

Does not clear the bar: no second source, no species, no name, no photo,
nothing to verify beyond two coordinates. Filed as leads
(data/leads/taketa.json) rather than published. Both submissions rows set to
outcome `open_question` with a reply asking for a photo or the species;
rows 111 and 112 marked processed.

Reader submission (kind `tree`, app's Collect flow, no name/species/girth given).
The pin (33.04561, 131.29971) was tagged "Oguni" by the app, but that is just
the nearest city in our own database (25.6km from ogn_001): reverse geocoding
(Nominatim) places the actual point in Taketa, Oita, a prefecture over from
Oguni-machi, Kumamoto. Went looking for a documented tree there anyway, in
case it was a known giant cedar mismapped by the app: found and checked the
national register's Amida Sugi (阿弥陀杉, Kurofuchi, Oguni-machi, designated
1934, ~1600yr claimed, 38m, girth 10.65m per bunkacho + a second source), but
that tree sits demonstrably elsewhere (its own listed address is nowhere near
this pin) and the Japan giant-tree/bunkacho register has nothing within 19km
of the submitted point. Overpass has no named tree node there either, only
generic woodland polygons. No photo was sent with this one.

Does not clear the bar: no second source, no species, no name, nothing to
verify beyond the coordinate. Filed as a lead rather than published (kept in
mind for a future Taketa pass if more evidence ever turns up), outcome set to
`open_question` on the submissions row, reply asks for a photo or the species.
Row 110 marked processed.

## 2026-09-13 (continuation 34) - New place: Portalegre (Portugal), the Plane Tree of Rossio, single-famous-tree exception

Same window, continuing down `famous_demand.py --gap`'s list past the Belgrade
tree. "Plane tree of rossio" (Portugal, 75 views/mo, 2 langs, pin yes) turned
out to be **Plátano do Rossio**, in Portalegre, Alentejo, not Lisbon's Rossio
as the name first suggested (the lead's own coordinate, 39.296/-7.430, is
40km southeast of Lisbon and matched Portalegre's own Rossio square via
Nominatim). No published tree within 100km, so its own place.

An exceptionally well-documented single tree: planted 1838 by the town's own
physician-botanist José Maria Grande, Portugal's first tree ever classified
a Monument of Public Interest (1938), winner of the national Árvore
Portuguesa do Ano contest for 2021 and 4th in the European final. Two
independent sources (Portuguese Wikipedia, the Portalegre municipal
council's own visitor page) plus three corroborating 2020-2021 press pieces
(Público, LusoJornal, Gazeta Rural) on the award.

Flagged rather than silently resolved: Wikipedia gives 5.26m girth/27m
canopy from older records, the municipality and the press all converge on
7m/37m from the 2020-2021 measurements; used the more recent, more widely
corroborated figures and said so in `verify_notes`. Also flagged: the
classification year moves by one across sources (1938 vs 1939), used the
earlier without resolving by guessing. Photo (João Martins, CC BY-SA 4.0)
is a strong Cadiz-standard shot, in leaf, showing the tree's distinctive
20 support props clearly. Full build (5656 pages) and `qa.py` (8788 pages)
both clean.

## 2026-09-13 (continuation 33) - Belgrade 4 -> 5: the Vračar tavern-keeper's plane

Same window, continuing down `famous_demand.py --gap`'s list after La Pochota.
Next candidate with real supply, "Platan na Vračaru" (Serbia, 114 views/mo,
already pinned), had no coordinate in the lead file for the linked entry
"Platan na Vračaru" itself but the lead's sibling record ("Platan na
Vračaru") named an exact address (Makenzijeva 73, Belgrade), which put it
0.98km from the existing bel_001 (Cvetni Trg oak), inside Belgrade's already-
published 7.3km walk. Deepened Belgrade rather than opening a new place.

Verified: the town's own green-space manager, Zelenilo-Beograd (~170 years,
3.90m girth, 27m tall), and Serbian Wikipedia, which cites the 2002 Belgrade
City Assembly protection order (Official Gazette 5/2002) but gives slightly
different figures (~150 years, 3.67m girth). Recorded the discrepancy in
`verify_notes` rather than picking one silently; used the official manager's
numbers as primary. Geocoded the address via Nominatim, which returned the
"Trandafilović" restaurant by name at the tree's own site, matching every
source's description of the tree standing in that restaurant's garden.
`location_precision: confirmed`.

Photo (Ljiljana Sundać, CC BY-SA 4.0, Wikimedia Commons) is a bare winter
shot, the only kind available for this tree on Commons: still meets the
Cadiz standard on composition, exposure and framing, just not the in-leaf
tiebreaker. Fixed intro (was 117 words, Contract C caps at 100) and the FAQ's
stale "all four" after adding the fifth tree. Full build (5653 pages) and
`qa.py` (8780 pages) both clean.

## 2026-09-13 (continuation 32) - New place: Chiapa de Corzo (Mexico), La Pochota, single-famous-tree exception

With `city_queue.py --next`'s OPENABLE list exhausted (see the previous two
entries), moved to the famous-tree track: `famous_demand.py --gap` (trees
read about in other languages and unwritten in English, the thin-competition
end of the list). Top of the list by demand with an actual pin was **La
Pochota**, a giant kapok (Ceiba pentandra) in the main plaza of Chiapa de
Corzo, Chiapas, 386km from our nearest published tree (Santa María del Tule),
too far to join any city.

Verified against Spanish Wikipedia, a July 2026 Sol del Soconusco news piece
on the 33rd anniversary of its 1993 protection declaration, and INAH (Mexico's
national heritage institute): the town was founded beside this tree in 1528,
a 1945 arson fire destroyed roughly a third of the crown (one scorched limb
survived and is still growing), and Chiapas declared it the state's first
Historic and Notable Tree in 1993, a status shared nationally with only two
others (the Árbol del Tule and Mexico City's Árbol de la Noche Triste).

Two things flagged honestly rather than repeated as fact: age is "at least
500 years" per the state's own 2026 notice, not the "thousand-year tree" of
local folklore, since nobody has cored it (`age_min: 500, age_max: 600`).
And several Mexican press pieces describe it as "over 60 metres tall", which
no survey supports and which the tree's own silhouette against the plaza's
two-storey arcades in its own lead photograph contradicts, so no `height_m`
is recorded at all. Photo (Wolfgang Sauber, CC BY-SA 3.0, Wikimedia Commons)
meets the Cadiz standard: fills the frame, in leaf, well exposed, trunk and
crown both readable. `city-aliases.json` gets a `no_other_names` entry (no
English exonym). Preflight caught a real hard-rule-9 violation on first pass
("Kapok / Ceiba" as a second common name beside existing "Kapok" trees in
Lima/Oahu), fixed to "Kapok" alone. Full build (5652 pages) and `qa.py`
(8779 pages) both clean before committing.

## 2026-09-13 (continuation 30) - New place: Gornja Stubica (Croatia), the Gupčeva lipa, single-famous-tree exception

With the Tallinn claim finished and released, `city_queue.py --next`'s
OPENABLE-today list was checked for anything not already documented as thin
today: Adelaide and Zagreb (#154/#173, one Wikidata candidate each) were the
highest-ranked untouched options. Zagreb's one candidate, an oak nicknamed
"Dedek" in Maksimir park, was already recorded blocked in
`data/leads/zagreb.json`: it fell in a storm on 2026-05-16, confirmed by two
Croatian news sources, and its clone saplings have not been replanted at the
site. That same leads file had already flagged the real find and left a note
for later: a second, unrelated Zagreb-area register row ("Lipa na
Medvednici") turned out to be a false positive, a mountain peak not a tree,
but the pass that caught it in August had also surfaced a genuine one nearby:
**Gupčeva lipa**, a linden in Gornja Stubica, in the Zagorje hills, tied by
Croatian tradition to Matija Gubec gathering his followers there before the
1573 Peasant Revolt, one of the defining events of Croatian history. That
pass had explicitly left it for "a future pass to evaluate as its own place."

Verified it properly this pass. Two independent sources (Krapinsko-zagorska
County's own nature-protection page and Croatian Wikipedia) agree on a 2021
survey (4.90m girth, 9m height, no exact age) and the historical tradition;
neither is in Croatia's own 12-entry national monument register. An OSM node
tagged "Gupčeva lipa" matches the Wikidata coordinate within metres, so
`location_precision: confirmed`. Age set honestly as a floor rather than a
figure: "at least 450 years" (the 1573 anchor), flagged, no invented
precision on top. Checked the execution detail in the story (Gubec crowned
with red-hot iron, quartered, February 1573) against English Wikipedia and
ExecutedToday.com before using it; both agree.

Published as its own place, **Gornja Stubica**, one tree (`gst_001`), under
the single-famous-tree exception of 2026-08-31 (would somebody travel
specifically for this one tree, given a national historical association):
Zagreb itself gets nothing added, since its only candidate is dead. Ran
`city_names.py` (no English exonym, correctly). `preflight.py` (0 problems),
`superlatives.py` (no crown conflicts), full build (5649 pages) and `qa.py`
(8771 pages, links resolve, page reachable via the generated Croatia country
page) all passed before committing.

## 2026-09-13 (continuation 29) - Finished the standing Tallinn verify claim: 8 -> 9 trees, the Skoone Bastion Lindens

Followed the resume checklist: `passcheck.py --claims` showed Tallinn standing
(verify, by night-run, 137 min left), an earlier attempt in this window had
already fetched eight pages to disk (Eesti Loodus 2002, KesKus 2006, a
Postimees 2022 piece, Tallinn's own register pages, a Harku municipality page,
two Cloudflare-blocked dead ends) but delivered nothing and committed nothing.
`leads.py --ready` was empty, so the claim was the whole job.

Read what was already fetched rather than re-fetching. Eesti Loodus's 2002
survey of Estonian city lindens, already the source for the published Kelch's
Linden (tln_001), also names old western lindens surviving at Rannamägi park
on the former Skoone bastion, first recorded on Tallinn's 1728 town plan as a
row of 19-20 trees following the bastion's cavalier edge. KesKus (2006, Heldur
Sander) gives the full history and cites a real 1999 University of Tartu
dendrochronology study (Alar Läänelaid): the two thickest of four cored
lindens measured 129cm and 111cm in diameter and were ring-dated to roughly
390 and 300 years, implying planting near 1609 and 1699. The 1609 figure
predates the bastion's own 1683 construction start, a discrepancy neither
source resolves and which the new tree's story states plainly rather than
explaining away. Postimees (2022) independently confirms the row is alive and
vigorous, not a historical footnote: it reports the trees' roots pushing apart
a 300-year-old stone passage buried in the bastion beneath them. Two
independent published sources, no register entry within 500m of the site (the
EELIS register has nothing here). Shipped as **tln_009, The Skoone Bastion
Lindens**, an ensemble entry (a compact, singular row with one obvious place
to stand) rather than pretending to isolate one trunk, since no source
distinguishes the dated trees from their neighbours; `location_precision:
approximate`, pinned to the park (OSM: Rannamägi, confirmed via Nominatim).

Updated the city's intro, meta_description, question_meta, question_context
and three FAQ answers for the new count and to fold the new tree into the
"can I see them in one walk" and "are they free" answers (yes; it sits within
the same Old Town cluster as Kelch's Linden and the Huecki Lindens). Kept the
"generally called the oldest tree in Tallinn" hedge on Kelch's Linden
unchanged and never claimed the new tree as a citywide superlative, since its
age is a single dendro study applied to an ensemble rather than one named,
locatable trunk; `superlatives.py` confirms no two pages claim the same
crown. `preflight.py` (1 FAIL fixed: a stale meta_description tree count),
full site build (5646 pages, clean) and `qa.py` (8763 pages, links resolve,
text clean) all passed before committing.

Also recorded two findings from the same fetch batch that are NOT Tallinn:
Harku vald's own website (a neighbouring municipality, not researched this
pass) confirms its Rabakivi tamm has died completely (blocked, never
re-research) and its Pilladu tamm is alive and protected (a lead for a future
Harku page or day-trip addition). Both filed in `data/leads/tallinn.json`.

Released the Tallinn claim. Checked `health.py`: `ios.yml`'s newest finished
run is still the failing 2026-09-13 one already noted by the prior
continuation (a UI test timing flake, no `ios/` code changed since the last
green run); nothing new to add. No sightings, no new submissions.

## 2026-09-13 (continuation 28) - Finished an inherited _famous-belgium claim: 6 new single-tree places, 2 Ghent additions, 1 held, 1 duplicate caught

Picked up a verify pass (`_famous-belgium`, claimed by an earlier attempt
this window, 134 min still on its clock) that had produced 10 verified
trees in `data/research/famousbelgium-verified.json` but never been
written up or merged. Ran a write-stories pass on it, then judged the
single-famous-tree destination test (CLAUDE.md 2026-08-31) on each
result rather than merging all ten.

**Published as new standalone places** (each below the 4-tree floor
under the exception, since none clusters with a published city or with
each other): Bonnerue (`bnr_001`, Li Béni Hesse, one of Belgium's
largest beeches, damaged, undated), Xhoris (`xho_001`, Tilleul des
Lognards, a nail tree protected since 1965 on the GR571 trail), Macon
(`mom_001`, Tilleul de Macon, its own French Wikipedia article, shaped
into three tiers on twelve posts, protected since 1942), Waremme
(`wrm_001`, Arbre de la Liberté, planted 22 September 1797), Jalhay
(`gos_001`, Les Sept Frères de Gospinal, Belgium's largest multi-trunk
oak, near the Hautes Fagnes) and 's-Gravenvoeren (`gvo_001`, Nagelboom,
a nail tree and former European Tree of the Year finalist).

**Merged into Ghent** rather than given their own pages, both within
the day-trip boundary: `gnt_007` (Dorpslinde van Massemen, Belgium's
Tree of the Year 2016, dendro-dated 378-440 years, ~13.6km from Ghent
centre, De Lijn bus) and `gnt_008` (the Solitaire Plane of Prudens Van
Duyseplein, 1.4km from centre). Ghent now has 8 trees.

**Held back**: the Remarkable Lime of Chantemelle (`cha_001`), verified
and written but carrying nothing beyond a bare Wallonia heritage
reference number, no age, no girth, no story. Fails the destination
test on its own evidence ("that is most of the file"); returned to
`data/leads/_famous-belgium.json` as blocked with the verified record's
git location noted for a later pass if a distinguishing fact surfaces.

**Caught a duplicate**: the Peace Oak of Wondelgem (`wdg_001`) is the
same tree as the already-published `gnt_006`, 75m off pin, same
planting year, same heritage object. Not merged; its one new fact (a
2026 Stad Gent renovation news item) was folded into `gnt_006` as a
third source instead.

**Two mechanical fixes along the way**: an id collision (`mac_001`
already belongs to Macugnaga, Italy; reassigned to `mom_001`) and four
species fields corrected to the site's one canonical common name (hard
rule 9): Large-leaved Lime, Horse Chestnut, London Plane, all previously
written with a non-canonical qualifier.

No photos on any of the 8 new/merged trees; an honest gap, left for a
photo pass. `_famous-belgium.json` still holds 14 further leads for a
future verify pass.

## 2026-09-13 (continuation 27) - Venice/Venlo/Verona photo hunts: dead ends documented; Vienna's Rathauspark trio completed

Venice's ven_011 (Palm of San Servolo), Venlo's vnl_001 and vnl_007, and
Verona's ver_006 (Yew and Laurel Wood of Giardino Giusti) all keep their
honest photo gaps. Candidates from the free `photo_hunt.py --recheck`
sweep: ven_011's one candidate is a good daylight photo but the San
Servolo building facade owns the centre band, not the palm, and the
crown shape reads as the wrong Phoenix species besides. vnl_001 and
vnl_007's four candidates are all archival B&W or a 1944 aerial
reconnaissance frame with no individual tree visible. ver_006's three
candidates are all general Giardino Giusti views (the cypress avenue,
the fountain parterre) rather than the yew and laurel wood the story
names; none show a resolvable yew trunk or crown. All 7 recorded
`judged`/rejected in `data/photo-queue.json` so a future sweep does not
re-serve them.

Vienna's Rathauspark now has photos of all three of its individually
protected planes (Naturdenkmal 564/566/567, designated together in
1973): vie_026 (ND 567) and vie_029 (ND 566) approved this pass, joining
vie_006 (ND 564, already published). The two were previously
indistinguishable in our own data past a register_id; a photographer's
geotags (GuentherZ, two photos taken the same day, 2010-08-25) settled
which pin is which within a metre-scale margin, and the resolution is
now recorded in both trees' `verify_notes`. vie_027 (Plane of
Hugelgasse) also got a photo, named for its own register address.
vie_018, vie_019, vie_020, vie_021 and vie_022 keep honest gaps: 14 of
their 21 rejected candidates were Schonbrunn palace geosearch noise
750-800m from the actual pins (Commons' geosearch returns anything near
a popular landmark, not photos of a specific tree), one was the wrong
Natural Monument entirely (ND 179, the Japanese pagoda tree our own
story already records as destroyed by war), and two right-tree
candidates (Burggasse's elm) failed on `photo_light.py`'s exposure score
under an overcast sky.

Also: `note_a_reader_photograph_is_not_a_reason()` in preflight.py was
firing a WARN on kyo_017/kyo_019 for lacking age+measurement despite
both carrying their own city/park government source; refined the check
to treat a verified source as a reason too, same as an age or a
measurement, rather than flip it to a build-breaking FAIL on two
legitimately-sourced trees. And 21 pages (long place names: national
parks, German/Slovak compounds, American "City, State") were falling
through to a bare "Ancient Trees in X" title with no count or age hook;
added a compact fallback that rescues 20 of the 21 (Chapel Hill, North
Carolina genuinely does not fit). Full detail in LOG.md.

## 2026-09-13 (continuation 3) - 3 submissions processed: 1 pin correction applied, 2 empty test rows

Submission 104 (kind: correction, Baarn, brn_001 the Cantonspark Dawn
Redwood): the reader moved the pin 175 m from the published position, which
our pin already carried as `approximate`. Checked the arithmetic (haversine
on the two coordinate pairs confirms ~176 m) and checked it against three
"Watercypres"-labelled sightings held on 2026-09-08 as ambiguous between
brn_001, brn_002 and an unmapped specimen (`data/leads/_sightings.json`,
ff725d9a and siblings): the corrected position sits ~34 m from that earlier
photo, well inside the same cluster. Per the 2026-09-08 rule (a reader's GPS
fix beats a pin we already call approximate), moved brn_001 to
52.20753,5.298514 and rewrote the address, the honest note and the
recognise line, which still said "main entrance" under the old pin. Kept
`location_precision: approximate` rather than promoting to confirmed: the
corrected spot sits only ~51 m from brn_002 (the giant sequoia) in the old
pinetum, and the underlying species-identity ambiguity from 09-08 was never
resolved, only narrowed. Outcome `changed` recorded on the row.

Submissions 102 and 103 (kind: tree, both Fukuoka, both from the same GPS
point, no name, no why, no species): 103's paired sighting (d0e24fa3) was
already looked at and logged as a feature test (feet on a bed, no tree,
commit 8c23a6bf); 102 has no sighting row in Supabase at all, so no photo
ever backed it. Both outcomes recorded `holds`; nothing to publish or chase.

All three rows are the `a8ca51da` account, which `data/our-accounts.json`
already identifies as Hidde's own (sha1 matches "Hidde's own account"), so
`contributor_reply.py`'s `ours.is_ours` filter means the reply_text set on
each row will never actually mail him.

## 2026-09-13 (continuation 2) - Breda's bre_010 photo hunt: dead end, documented

`photo_gaps.py --shortlist` printed one candidate for The Plane of
Valkenberg's Edge (bre_010, no photo). Looked at the pixels of all three
candidates in its queue entry: "Gevallen blad van een boom in het gras.jpg"
is a single fallen leaf on grass, no tree in frame at all (and categorised
as maple, while bre_010 is a London Plane); the other two ("Lake-Valkenberg-
Breda.jpg", "Stadspark-Valkenberg-Breda.jpg") are wide park/canal views
already rejected once for the neighbouring bre_003 on 2026-08-13 for the
same reason, no single tree identifiable as the subject. All three recorded
`judged`/rejected in `data/photo-queue.json` so a future sweep does not
re-serve them. Photo-less gap stays honest and open; the other 260
photo-less published cities have not cleared the five-tree threshold that
makes them eligible for this rung.

Also checked Taormina, Ravenna, Trier and Niagara Falls against
`city_queue.py --next`'s "openable today" list for new coverage: all four
are documented dead ends or too thin to open. Taormina's five register
trees are all blocked on access (same hotel grounds, already recorded
2026-08-31/2026-09-08). Ravenna and Niagara Falls have only one in-town
register/wikidata candidate each, the rest 15+ km away. Trier's nine
"nearby" register rows are all Luxembourg entries 10-20 km distant, not
Trier supply. None cleared the four-tree floor's worth of real, walkable
candidates. `scout_next.py --target` confirms nothing left to scout this
window either (BUILD, not SCOUT, and nothing left at the top to build from).

## 2026-09-13 (continuation) - Tokyo 17 -> 21, kyo_017 gets its first photo

Finished a standing verify claim on Tokyo: 4 trees added (tok_018 The Great
Zelkova of Nerima Hakusan Shrine, tok_019 The Great Ginkgo of Oji Shrine,
tok_020 The Kaya of Zenyo-ji, tok_021 The Child-Rearing Ginkgo of Zoshigaya
Kishimojin), all flagged (age estimates are tradition, and two carry an
honest unresolved girth discrepancy between sources rather than a picked
winner), 0 photos. 3 register/Wikidata candidates turned out to be
duplicates of trees already published; 2 blocked (an avenue with no single
surviving specimen worth the walk, a school with no evidence of public
access); 6 left as unresearched leads in `data/leads/tokyo.json`. Japanese
overlay (`data/i18n/ja/tokyo.json`) translated and grown to match.

Separately, a reader photograph (Hidde's own account, filed like any other
per the 2026-09-08 rule) closed kyo_017's photo gap after a viewing pass:
two duplicate frames and one mismatched photo of a different tree entirely
(taken 19 seconds earlier on the same walk, at the same app-recorded
coordinate, which is the known CollectSheet own-pin gap rather than
evidence either way) were sorted from the one that actually matches the
recognise line's gate and wall.

Two new Fukuoka submissions (Hidde's own account) came in mid-session: one
photographed a tree 818m from anything we publish, filed as a lead; the
other has no synced photo yet and was left for a later run to pick up.

## 2026-09-13 - Milan 24 -> 25: the fourth Villa Litta plane, written

Write pass on the single verified tree in `data/research/milan-verified.json`,
**mil_025 La Pianta di Manzoni** (London Plane, Parco di Villa Litta Modignani,
Affori). 1 tree added, 1 flagged, 1 photo missing. `location_precision:
confirmed`, on MASAF's sheet-14 point and a long-standing OSM node agreeing to
within 8 m.

The whole writing job here was keeping one bridge claim out of the prose, in a
city that has already been served a BLOCKER for exactly that failure. The tree's
local name is Manzoni's; Villa Litta was Count Trivulzio's salon in the
nineteenth century and local histories name Alessandro Manzoni among its
visitors. **No source joins those two facts**, so the story does not either. It
states the name, states the salon, says in plain words that nobody has recorded
why the tree carries the name, and asks the reader who knows. That is the
publish-and-ask pattern rather than a hedge.

Two other honesty points carried from `verify_notes` into the prose rather than
left in the data:

- **Girth 410 cm is not register data.** MASAF's sheet 14 has no girth field
  filled at all (`girth_cm` is null in our own import). The 4.1 m comes from a
  2020 OSM edit whose note cites a plaque near the tree, so the story attributes
  it to a plaque copied down by a passer-by rather than to a survey. The height,
  28 m, is the register's own and is presented as such.
- **No age, and none derived.** Nothing publishes one, and this register carries
  no age field for any entry it holds, which the story says rather than
  apologising for. No derivation from the park's own 1700s planting era, which
  would have been the bridge claim its sibling mil_015 deliberately avoided.

No `best_time`: a single plane with no documented peak, and the park's fused
Siamese pair (mil_015) already holds the bare-silhouette badge in this city.

Count promises fixed on both language sides, all of them already stale before
this tree: the English intro still said twenty-three at 24 trees, the meta
description and free-to-visit FAQ twenty-four, `question_meta` twenty-three
more; the Italian overlay's title, meta description, intro, `question_meta` and
FAQ all still said 23. Italian translation for mil_025 written the same day,
because preflight refuses a short overlay outright rather than degrading one
page.

Still open in `data/leads/milan.json`: **MASAF sheet 15** (257 m from mil_015, no
girth, no name, no OSM node at its coordinate) stays a lead, and the verify pass
added a new one, the Parco Nord Milano *Patriarchi del Parco* trail map, which
names 30 specimens and gives no coordinate, girth or age for any of them.

## 2026-09-13 - Alicante 19 -> 21: two press-corroborated pairs written up

Write pass on the two verified trees the Alicante verify pass left in
`data/research/alicante-verified.json`. Both are groups rather than single
trunks, both rest on the same 2013 Diario Información survey of the city's
biggest and oldest trees, and both carry `curation_status: flagged`.

- **ali_020 The Centenary Elms of Panteón de Quijano** (Field Elm), the same
  small fenced garden as the already-published ali_017 araucaria, which is why
  `passcheck --pending` flagged it as a possible duplicate at 0 m. Checked by
  hand: different species, different trees, one park-level coordinate, so it
  ships as its own entry on `location_precision: approximate`, matching
  ali_017. Honest gaps stated on the page rather than filled: nobody has
  published how many elms stand here, no girth, no height, no register entry
  of their own, and the page asks the reader for the count. Age is the
  source's own language, nineteenth century and centenary, and is NOT derived
  from the garden's own 1855-1857 build date, which is the bridge claim the
  verify notes flagged. Last explicit confirmation of life is the 2013
  article's account of the 1990 trunk-rot surgery, hence flagged.
- **ali_021 The Silky Oaks of Passeig de Canalejas** (Grevillea robusta), two
  Generalitat register entries (3070 and 3071) about 11 m apart, folded into
  one entry on the twin rule, `confirmed` pin at the midpoint. The register's
  two girths disagree by more than triple (1.05 m against 3.75 m) for a pair
  the newspaper treats as matched; heights agree (19 m and 18 m). The story
  says both figures and leaves the discrepancy unexplained rather than picking
  a winner. No age derived from girth: the species grows fast, so the century
  is the newspaper's word and nothing more. The paseo's 1886 design date is in
  the prose as a fact about the promenade, explicitly not as a planting date.

Neither tree gets a `best_time`: the field elm phenology file peaks at `nice`,
and no species file exists for Grevillea robusta. Both photos `missing`, both
free and open, both carry a `how_to_recognise` line. Spanish overlay written
for both the same day (a short overlay refuses the whole build). Count
promises fixed in the city intro, meta_description, question_context and the
Spanish title. Build clean, `qa.py` clean (8,697 pages), `preflight.py` 598
cities and 0 problems.

## 2026-09-13 - Gdansk 6 -> 12: the Park Oliwski dendrological cluster written up

Write pass on the six verified trees the Gdansk verify pass left in
`data/research/gdansk-verified.json`. All six stand in Park Oliwski im. Adama
Mickiewicza in Oliwa, within a few hundred metres of each other, which turns a
page of four scattered singletons into an actual afternoon's walk. All six are
free, public park, `location_precision: confirmed`, and all six carry
`curation_status: flagged` from the verify pass.

- **gda_007 The Maples of Hugo Conwentz** (Field Maple): register twins folded
  into one entry, 245/180 cm. Designated 26 Feb 2026, the newest natural
  monument on the whole Gdansk list. The verify notes flagged the Conwentz
  biography as needing an independent check before use, so the story attributes
  it ("widely credited with") rather than asserting it, and says outright that
  the register does not explain why these trees carry his name.
- **gda_008 The Ginkgo of Park Oliwski**, 201 cm. No age anywhere; left empty
  and turned into a question on the page rather than a girth-derived guess.
- **gda_009 The Cucumber Magnolia of Park Oliwski**, 271 cm. No age; no growth
  rate published for Magnolia acuminata at this latitude to derive one from,
  stated plainly.
- **gda_010 The Three-Trunked Katsura of Park Oliwski**, stems 168/189/158 cm.
  No age, but the species ceiling is real and is in the story: Cercidiphyllum
  japonicum reached Western collections only after 1865.
- **gda_011 The Giant Thuja of Park Oliwski**, 219 cm, the headline tree of a
  four-tree register group (two yews and a Nootka cypress beside it). No age.
- **gda_012 The Ivy Elm of Park Oliwski**, 420 cm, by the pond, protected 1988
  under a register name that describes the flowering ivy on it. Age 150-250
  years, girth-derived, kept broad and said to be girth-derived.

**Photos: 6 of 6 missing.** The verify notes cite a named Commons file for four
of them (833. ginko biloba gdansk.jpg, 837. magnolia gdansk oliwa.jpg, 838.
grujecznik gdansk oliwa.jpg, 836 skupienie oliwa.jpg, Wiaz z kwitnacym
bluszczem.JPG), so this is a live photo lane rather than a dead end: it needs a
viewing pass, not a new hunt. Not attempted here, photo hunting is not a write
pass's job.

**best_time set on 3 of 6, left empty on 3.** Ginkgo (Oct/Nov gold), katsura
(October, the fallen leaves smell of burnt sugar) and the ivy elm (late Sept
into Oct, when the ivy flowers and pulls in wasps and late bees). The thuja is
evergreen and gets none; the maples and the magnolia have no moment strong
enough to spend the badge on.

**Two species common names harmonised** to what other city files already use:
"Katsura Tree" -> "Katsura (Cercidiphyllum japonicum)" and "Western Redcedar" ->
"Western Red Cedar (Thuja plicata)". The Latin names, which are the verified
fact, are untouched; the build fails on one species under two common names.

**Count promises fixed** across the page: intro, meta_description,
question_meta and the "Are these trees free to visit?" FAQ all still said six.
The first intro rewrite overran Contract C's 60-100 word cap at 158 words and
preflight caught it; cut back to 97.

**The Lawson Cypress lead in `data/leads/gdansk.json` was NOT written.** Its own
note says "not verified this pass", and a write pass verifies nothing. It is a
good candidate in the same walkable cluster, 212 cm, register 830, and it needs
a verify pass rather than a writer. Left in the leads file untouched.

## 2026-09-13 - Berlin 21 -> 23: a wingnut resolved, and the Queen's own oak found beside it

Dispatched a register-backed verify pass on Berlin (target 30, real
unmined supply: 546 Naturdenkmale rows + 648 Wikidata candidates), flagged
by a prior continuation today as the best-supplied unexhausted deepen
target on the whole queue. Focused on the Tiergarten Englischer Garten
cluster, ~13 Naturdenkmal entries within 400m of the already-published
ber_010 (Giant Sequoia), because it was already proven walkable.

**ber_022, The Englischer Garten Wingnut** (Caucasian Wingnut): the register
(1-39/B) plus an independent 2022 blog.inberlin.de article that names and
locates the same tree "near the teahouse", within ~4m of the OSM-mapped
Teehaus. No age documented anywhere, flagged and stated plainly rather than
guessed.

**ber_023, The Queen's Oak of the Englischer Garten** (Northern Red Oak,
not a register tree): two independent Tagesspiegel articles agree Queen
Elizabeth II personally planted it on 27 May 1965 during her first visit to
West Berlin, sapling reportedly from Windsor Castle stock. No exact
coordinate in either source, so `location_precision: approximate`, pin
centred on the Teehaus.

The rest of the cluster (Metasequoia, Libanon-Eiche, Silber-Linde,
Flatter-Ulme, Japanischer Kuchenbaum x2, Stiel-Eiche, Robinia) stayed
single-sourced: the register, Wikidata and de.wikipedia's district list all
trace to the same 2021 government ordinance (confirmed by fetching the
ordinance itself), which carries no age or girth field. Caught and
discarded a WebSearch-summary fabrication in the process: a claimed
"circumference 1825" for the Libanon-Eiche was actually a Flurstueck
(land parcel) number repeated identically across five unrelated trees, not
a measurement.

Wrote both stories (write-stories pass, small batch), added the German
i18n overlay entries for both (title count 21 -> 23; `de/berlin` had been
the only translated overlay for this city and would otherwise have
refused the whole build per Contract J). `preflight.py`, `i18ncheck.py`
and a full `npx astro build` all clean. Cost: ~95k verify + ~40k write,
2 trees, logged in `data/agent-costs.json`.

## 2026-09-13 - Sintra: sixth consecutive verify pass confirms exhaustion, 0 trees

Dispatched a verify pass on Sintra (target 20, was at 5, real ICNF register
supply looked promising at first glance: 30 unmined of 49 candidates within
20km). Every candidate within the walkable radius turned out to be either
already published or already `blocked` in `data/leads/sintra.json` by one of
the five prior passes. Checked genuinely new angles this time rather than
re-running the register sweep: serradesintra.net's grandes-arvores page (its
one named entry, "Feteira da Rainha," is a place, not a tree), Monserrate's
other official recanto pages (generic, no individual specimens), the Feteira
da Rainha recanto itself (a "tuia-gigante" likely already published as
sin_001, plus an uncorroborated travel-article claim of "two enormous
sequoias" left as an open lead, no measurement or pin), Convento dos
Capuchos (a WebSearch AI-summary invented specific ash/plane trees there;
neither the official page nor English Wikipedia mentions them, caught and
discarded per the search-summary-is-a-lead-never-a-source rule), and Jardim
da Preta (a legend about a viewpoint, not a tree). Appended a dated note to
`data/leads/sintra.json` so a seventh pass does not re-walk this ground.

**Honest conclusion: Sintra's five published trees are likely near its
ceiling at the current evidence bar**, short of the target of 20, unless a
future pass gets working access to monumentaltrees.com's Monserrate page or
a source individually names and measures a Sintra sequoia, ash or box
specimen. Cost: ~78k tokens, 0 trees, logged in data/agent-costs.json.

## 2026-09-12 (continuation 19) - Zwolle 14 -> 16, two flagged trees finished from a stranded verify pass

Found `data/research/zwolle-verified.json` uncommitted at session start: 2 fully
verified trees (zwo_015 the Plume Elm of Potgietersingel, zwo_016 Huis de
Paddestoel's Swamp Cypress), produced by an earlier attempt in this window that
stopped without writing them up. Both single-register-sourced, both flagged.
zwo_015's species is genuinely unsettled between the register's own two passes
(Ulmus x hollandica vs Ulmus sp.); page asks the reader. zwo_016's address in
the register (Herenweg 33) does not match its own coordinate (near Herenweg
131-133); the verify pass's reverse-geocoding and a 1991 archive photo caption
resolve this as almost certainly a register typo rather than two trees, cross-
checked against the municipality's own 2015 list which carries only one
Taxodium on the whole street. Wrote both stories and recognition lines
directly rather than dispatching a write-stories agent for 2 trees. Also
released a stale "Berlin verify" claim from the same earlier attempt, which
produced no output (Berlin's recognition lines, committed separately, were
unrelated finished work, already applied).

## 2026-09-12 (continuation 12) - Breda bre_010 photo candidate rejected after looking at it

`photo_gaps.py --shortlist`'s only candidate this pass was "File:Gevallen
blad van een boom in het gras.jpg" for bre_010 (The Plane of Valkenberg's
Edge). Fetched and viewed the actual pixels: it is a close-up of a single
fallen leaf lying on grass, not a photograph of the tree at all (the
Commons description confirms it, "fallen leaf of a tree on the grass").
Fails the Cadiz standard outright. Left bre_010's photo status as
`missing`; do not re-surface this filename for this tree.

## 2026-09-12 (continuation 11) - Finished an earlier attempt's Amersfoort/Breda claims; week budget nearly spent

Inherited two standing register-verify claims (breda, amersfoort) whose
work was already complete but uncommitted: Amersfoort 8 -> 14 trees,
Breda 4 -> 10 trees, both from the Landelijk Register Monumentale Bomen
(2024 edition), each new tree flagged (single register source). Ran
preflight, superlatives and a full astro build (clean, 5514 pages, exit
0) before committing, then released both claims. Also found and
committed a park page for Ottawa's Dominion Arboretum that an earlier
commit (5e92ac33) had written but never staged.

Checked `leads.py --ready`: only 3 candidates, and all 3 turn out to be
false positives on inspection (Genoa's was explicitly declined for
padding risk, Prague's is still blocked on unconfirmed access, Lagos's
is a negative-research-result record, not a tree). Nothing to dispatch
a write pass on.

Checked `city_queue.py --next` for a new city to open: Taormina and
Ravenna, the two highest-ranked options with register supply, are both
already documented dead ends (2026-09-11 entry above). Everything else
openable today (Adelaide, Zagreb, Lagos, Niagara Falls, Wellington,
Mechelen, Gran Canaria, Kilkenny, Izmir, Stirling, Canterbury, Evora,
Stratford-upon-Avon, La Palma) has only 1-2 Wikidata leads each, below
the six-candidate floor for a single-city pass; a batched pass across
several of them is the shape that would work but was not started this
attempt.

Stopped here rather than start one: `run_health.py --week` read
4855/5000 minutes with roughly 145 left, shared with Hidde's own usage.
Starting a new multi-city research pass risked either eating most of
what remains of the week's shared budget or dying mid-way on the usage
limit, which is a worse outcome than a short, clean attempt that shipped
14 finished trees across two cities.

## 2026-09-12 (continuation 10) - Ottawa 14 -> 19; Helmond register pass found only duplicates

Ottawa: 5 new trees from the NCC "A Living Legacy" register, all in the
Dominion Arboretum, verified with two sources each (register plus Friends
of the Central Experimental Farm's CelebriTrees tour or an independent
species page) and public access confirmed rather than assumed. Full detail
in LOG.md.

Helmond: a register-backed verify pass on 5 unmined LRMB candidates within
the existing walk found all 5 are exact-coordinate duplicates of already-
published trees (hlm_011/012/013/015/018) under new register-adjacent ids.
Not published. Recorded in data/leads/helmond.json (status: duplicate, with
the register id of the live twin each one matches) so a future pass does
not re-mine these same rows expecting new trees. This is a passcheck gap
worth naming: its "unmined" candidate list did not flag these five as
near-duplicates the way it correctly flags others "within 80m of a live
tree", and nobody has yet worked out why those five specifically slipped
through.

## 2026-09-11 (continuation 8) - Prague 27 -> 30: three Praha 8 oaks from the AOPK register

Finished a standing verify claim on Prague left by the previous attempt in
this window (claimed, never researched). Mined the unmined AOPK register
rows 5-7km northeast of the centre: prg_028 The Oak Behind the Ranger's
Lodge, Cimicky haj (Bohnice, girth 381cm, deliberately the living half of a
once-paired oak whose bigger, more famous neighbour is confirmed dead per
Czech Wikipedia's own extinct-oaks category), prg_029 The Oak of Pod
Labutkou Street (Liben, girth 314cm, an ordinary street oak with an
unusually intact ground-level crown), prg_030 The Oak of Kobylisy
(Sidliste Dablice, girth 436cm, the largest tree in a housing-estate park
on the site of a former military range). All three register+cs.wikipedia
sourced, flagged rather than confirmed on two fully independent sources,
all free and unrestricted. One new lead added: Cedr atlasky Na Balkane
(Atlas cedar, Prague's only protected one), inside a tennis club whose
public-facing offer does not settle whether the tree itself is reachable
without booking a court.

The write pass had transliterated every Czech place name to plain ASCII
(Cimicky haj, Pod Labutkou, Strelnicna, Liben, Dablice); restored proper
diacritics before merging, checked directly against the register's own
name_cz field (Cimicky haj, Pod Labutkou, Strelnicna, Libe, Dablice) rather
than from memory. Also fixed two stale tree-count mentions in the city's
own copy (meta_description and question_meta both still said 27).

**A qa.py failure fixed along the way, unrelated to Prague**: two orphaned
Lisbon photo files (lis_005's `-500`/`-1000` sized copies, saved under a
slug with an extra "the-" that matched neither the tree's own photo.url nor
photo-manifest.json). Confirmed no reference anywhere in data, scripts or
site/src, deleted them, qa.py clean again.

**A photo viewing pass on Tilburg's one fetchable candidate** (biggest gap
on `photo_gaps.py --shortlist`) rejected on sight: the matched file was a
fallen Ginkgo leaf in the grass, not til_018's Flowering Ash. Recorded via
photo_verdicts.py.

**REVIEW.md's two open WARNs from today's fresh-eyes review turned out
already fixed**, just not rebuilt: the broken empty `<figcaption>Photo:
</figcaption>` on reader-app photos with no attribution, and the three
self-repeating tree-page titles ("The X: X in City"). Read the current
source for both (PhotoFigure.astro/images.ts, and `[city]/[tree].astro`'s
`nameEchoesSpecies` guard) and confirmed the fixes are in place and the
built site is clean; nothing further to do.

**Taormina and Ravenna checked and passed over for new coverage.**
Taormina's register is a documented dead end (all in-town candidates
blocked on hotel-grounds access, confirmed again by re-reading its own
leads file rather than re-researching). Ravenna's four register candidates
are 17-19km apart with no walkable cluster and only one close to the
centre, below the six-candidate minimum for a pass. Claimed Rome instead
(30 trees, the single highest-impression depth-allowed city per the latest
digest) for a verify pass on its own unmined near-centre register
candidates; see the next entry for the result.

## 2026-09-11 (continuation) - Milan 23 -> 24 trees; Alicante's register confirmed exhausted; Finch Arboretum park page

Dispatched two parallel verify passes (isolated worktrees) on Alicante and
Milan, both deepen targets with real Search Console demand and register
supply that `passcheck.py --brief` reported as substantially unmined.

**Both briefs turned out to be stale.** Alicante's "43 unmined" candidates
all cross-matched by coordinate to leads already resolved by five prior
passes (published, held, or blocked); the register there is genuinely
exhausted, confirmed independently a third time. Milan's "52 unmined"
candidates likewise all resolved to duplicates, already-blocked entries
(the children-only Villa Belgiojoso garden), or one already-published
tree, except for one genuinely open pair. `passcheck.py`'s "unmined" count
does not currently discount leads a prior pass has already resolved by
coordinate; both agents caught this themselves rather than trusting the
brief, cross-checked the full register against `data/leads/` before
reporting, and left sharper notes behind so a future brief-reader does not
repeat the check. Worth a fix in `passcheck.py --brief` itself: whoever
next touches it should have it subtract resolved leads from the "unmined"
count before printing it, so the number means what it says.

**Milan, 23 -> 24 trees.** mil_024, "I Platani di Villa Litta Modignani":
two more MASAF-registered planes in the same park as the already-published
Siamese pair (mil_015) and La Pianta di Affori (mil_009), folded into one
entry per the register-twins rule (12m apart). Single-sourced and flagged;
the register puts the larger at 43m, which the story flags honestly as
possibly the tallest tree on the page rather than asserting it, since a
differently-dated citation of the same underlying MASAF dataset (an
it.wikipedia rescrape) gives smaller, disagreeing figures for the same
park and neither is silently preferred. Wrote the story and its Italian
overlay translation in-session (Milan ships in Italian; the build refuses
an incomplete overlay). Fixed two Contract C overruns preflight caught
(question_meta length, a stale "twenty-three" count in the FAQ paid-entry
answer). Build, qa.py, i18ncheck.py and preflight.py all clean.

**Alicante, unchanged at 16.** No new trees; the one open lead (a possible
third fig near the Castillo de Santa Barbara elevator entrance, referenced
in a single 2026-08-04 news event) had its coordinates sharpened via
Overpass but still fails the two-source bar. Left as a lead for a future
pass with photo-comparison tooling.

**New park page**, earned by this session's earlier Spokane write pass
pushing Finch Arboretum's tree count to 6: `data/parks/john-a-finch-
arboretum-spokane.json` (Contract H). `pagegaps.py` clean afterward.

Both agent cost lines logged in `data/agent-costs.json`. Both claims
released.

## 2026-09-11 (continuation) - Spokane deepened to 13; four other claimed READY leads declined after reading them

`leads.py --ready` listed 8 trees across five cities (spokane 4, hallstatt 1,
lagos-pt 1, genoa 1, prague 1) as needing only a story. Claimed all five, then
read every underlying lead in `data/leads/` before writing anything, since the
tool's own docstring warns it is a proxy (any pass leaving prose counts as
"source evidence", not a guarantee the tree should ship). Four of the five
turned out not to be ready on inspection; writing them as-is would have shipped
either a non-tree, a padding risk the previous pass had already flagged, or a
hard-rule-10 access question three prior attempts had failed to settle.

**Spokane, 9 -> 13 trees**, the only city whose leads genuinely needed only
prose. All four are Spokane Heritage Tree Register entries, single-sourced and
flagged per Step 2's rule that one source ships rather than holds a tree back:
spk_011 The Towering Norwegian (Norway spruce, ~123ft, register's own second-
tallest-in-the-city claim), spk_012 Powerful Pine (Mexican pinyon, one of the
state's largest, an odd transplant for the Inland Northwest), spk_013 Chief
Garry Park Champion (sycamore, a state size candidate, its own story
distinguishing it from a different variegated sycamore maple HistoryLink names
in Browne's Addition so the two are never merged), spk_014 The Littleleaf
Linden (Moore-Turner Heritage Gardens cluster, ~110 years, species left
genuinely open on the page because the register's own record contradicts
itself, title says littleleaf, description says American). Fixed a species-
naming collision before merging (spk_013 had drafted as "Sycamore Maple",
hard rule 9 wants the one name ~20 other cities already use, "Sycamore") and
two Contract C overruns (intro, meta_description) plus one how_to_recognise
overrun (spk_014) that preflight caught. Build, qa.py, superlatives.py and
preflight.py all clean. Claim released.

**Hallstatt, declined.** The one READY lead, a copper beech (Blutbuche) near
the Gosau forestry office, is 9km from Hallstatt centre in a different village,
with no age or girth, and the pass that found it explicitly deferred all three
Gosau candidates (this beech plus a wych elm and a school linden, all within
100m of each other) for "a future pass that covers Gosau" as its own cluster.
It only surfaced as READY because its "not pursued this pass" phrasing sits
mid-sentence rather than at the start, which is what `leads.py`'s
NOT_READY_MARKER regex actually matches (worth a look for whoever next touches
that script; not fixed here). Shipping one third of a deferred three-tree
cluster alone, under the wrong city, would pre-empt that future pass for no
gain. Left as a lead.

**Lagos (PT), declined.** The single "READY" entry is not a tree: it is the
previous pass's own negative-result note ("No further register or named
candidates found in Lagos town itself"), with `species: "n/a"`. It cleared
`leads.py`'s readiness check only because the note itself counts as source
evidence and nothing checks that `species` is a real species. Nothing to
write; the note already records where a future pass should look next
(the named parish churches, Ponta da Piedade, a direct approach to Camara
Municipal de Lagos).

**Genoa, declined.** The one READY lead is a second Cinnamomum glanduliferum
at Villa Durazzo Pallavicini, and the lead's own text already argues against
shipping it: the park already holds one Cinnamomum-family tree (gnv_009) and
a second one of the same genus stands nearby (gnv_004), so a third this close
together "risks reading as padding rather than a distinct entry unless it's
visibly a different, separately worthwhile specimen." No new evidence this
pass that it is. Left as a lead pending a reason to treat it as distinct.

**Prague, declined.** The one READY lead, an oak at the Dejvice sports ground
(Dub na sportovisti v Dejvicich), has been checked for public access three
times across three separate passes (2026-09-10 x2, plus the Czech Wikipedia
read) and every attempt came back the same way: it stands at a fence between
a kindergarten and a sports ground, no source establishes a public path
reaches that specific edge, and hard rule 10 says leave it out on a guess.
Its own `why` field documents this in full and ends "Leave as a lead until a
street-level photo or map shows a public way actually touching that NE
fence." Shipping it now would have overridden that finding on no new
evidence. Left as a lead; needs a street-level photo, not another search.

Claims released for all five cities. Logged spokane's pass in
`data/agent-costs.json`.

## 2026-09-11 (continuation) - Baltimore and Boise open at 4 trees each

Committing verify+write work an earlier attempt in this window had already staged
but not merged (city files sat untracked, claims still held). Checked both files
against the research standard before shipping rather than trusting the claim:
both clear the four-tree floor, every tree has honest sourcing (two of Baltimore's
four and one of Boise's four are single-sourced and flagged accordingly, per
Step 2's rule that a single source ships rather than holds a tree back), and
location_precision is set honestly (confirmed where a source gives a trunk-level
fix, approximate everywhere else).

**Baltimore, 4 trees.** The Ruxton Liberty Tree (bal_001), a 350-380 year old
white oak on private land, viewable from the public road at Dunlora Road and
Bellona Avenue, its owners paying for 5,000 gallons of weekly watering to keep it
alive; the Frederick Douglass Elm (bal_002) near Camden Yards, an undated English
elm carrying an unproven but honestly-labelled local tradition that Douglass
planted it as an enslaved child; and two Cylburn Arboretum champions, a cockspur
hawthorn (bal_003, single-sourced, flagged) and a paperbark maple (bal_004,
two sources). Both arboretum trees carry only park-level coordinates
(location_precision: approximate) since neither this pass nor the Maryland Big
Tree Program's JS-rendered database gave an exact spot; a future pass with a
JS-capable fetch could tighten both. Photos missing on all four, an honest gap.

**Boise, 4 trees.** Three Idaho state/city champions from the University of
Idaho's Big Tree Program register (largest bur oak, largest Kentucky coffeetree,
both in Julia Davis Park; largest giant sequoia, moved a quarter mile by flatbed
in 2017 so St. Luke's Hospital could expand without felling it) plus a horse
chestnut sapling grafted from the Amsterdam tree Anne Frank watched from the
annex window, one of only eleven such grafts in the US, now older than the storm-
felled 2010 parent. None of the three champions carry a documented age (Idaho's
register measures size, not years, stated honestly on the page rather than
guessed). Photos missing on all four.

Also ran, since both cities had never been resolved in other languages:
`scripts/city_names.py` (found local-name variants for both, no action needed
beyond the alias file update), `scripts/city_queue.py` (re-ranked, rebuilt
CITY_QUEUE.md and LEDGER.html), `scripts/tree_index.py` (67,610 trees indexed),
`scripts/superlatives.py` (364 claims, no collisions), full Astro build and
`scripts/qa.py` (8550 pages, clean). Both claims released. Note: city-list.json's
rebuild only updates rows already present in the file and does not add new ones,
so Baltimore and Boise do not yet appear there; harmless since nothing but
brief.py reads city/status from it and CITY_QUEUE.md (the actual order) carries
both correctly, but worth a look if a future session is touching that script.

## 2026-09-11 (continuation) - Tallinn deepened to 6: the Tammesalu Oak, Tallinn's thickest tree

Verify pass on Tallinn (5 trees, rank 109, real demand: 36 impressions in the
10-day window) found the Kadriorg register candidates were mostly already-leaded
ornamental cultivars on residential streets, but a dendrologist's press ranking
(Postimees 2017, corroborated by Loodusajakiri 2024 and Kadriorg Park's own site)
named Tallinn's single thickest tree: an oak in the old Tammesalu grove, already
substantial when Peter the Great bought the land in 1714, predating both Kadriorg
Palace and the park built around it. Two measurements eight years apart (637cm
2016, 648cm 2024) give a consistent, well-sourced girth-based age estimate of
300-400 years. Shipped as tln_006, `location_precision: approximate` (no source
gives a trunk-level GPS fix, only "the grove's northeastern part, by Kirdetiik
pond"). Wrote the story in-session and updated the city's intro, meta description,
question page and FAQ, all of which hard-coded "five trees" and needed the count
bumped to six; preflight caught the resulting word-count overruns (intro, story,
question_context) and a stale "three more" in question_meta, all fixed before
commit. Three more single-sourced leads (2 candidate oldest-tree oaks, 1
cemetery-park oak) banked in `data/leads/tallinn.json` for a future pass. Build,
qa.py and preflight.py all clean. Claim released, logged in
`data/agent-costs.json`.

## 2026-09-11 (continuation) - Sorrento deepen pass: register confirmed exhausted, 0 trees

Dispatched a verify pass on Sorrento (7 trees live, rank 111, real demand: 27
impressions/2 clicks in the 10-day window) since the MASAF register still showed
"31 unmined" candidates in passcheck's brief. Cross-referencing every candidate by
coordinate and MASAF sheet_id (rather than by name, the method that let these keep
resurfacing as "unmined") found every close-in row is either already published or
already blocked under a different name in `data/leads/sorrento.json` (the Antico
Parco del Principe trio, the Grand Hotel Parco dei Principi grounds, the Via Carlo
Amalfi cedar, the Villa Thuja eucalyptus), and every distant row belongs to a
different comune (Vico Equense, Castellammare di Stabia, Agerola, Pompei, Ravello).
Independently confirms the 2026-09-09 deepen pass's identical finding: this
register is exhausted at Sorrento's radius. The one open lead, a pine on Via
Bagnulo with a disputed August 2026 collapse report, stays unresolved after a
second independent check (a Positanonews AI search summary fabricated a sentence
not in the actual article; the real 2020 piece raises the risk prior without
settling which tree fell). Two new wrong-container leads recorded for a future
Vico Equense page. Claim released, no trees added. Logged in `data/agent-costs.json`.

## 2026-09-11 (continuation) - Two unprocessed submissions (100, 101): a third GPS-only Kyoto lead, a plain worth-it vote

Submission #100 (kind `tree`, `page: app:collect`, same account as 98/99): another
bare GPS pin near Kyoto Gyoen with no name, species or photo, 914m from the nearest
published tree (kyo_016/kyo_019, Omiya Gate). Same shape as the two already recorded
2026-09-10, so recorded the same way: added as a thin lead to `data/leads/kyoto.json`,
`outcome: open_question` set on the row, and this time a `reply_text` was actually
composed (the account is answerable and the prior two were left without one), asking
for a name, species or photo. Submission #101 (kind `feedback`, `why: "worth it"`) on
Tamba's tmb_001: a plain positive vote, no free-text complaint, nothing to check
against sources. Set `outcome: holds`, no reply needed, matching the standing pattern
(Utrecht #63, Amsterdam #40, Sardinia #39, Rome). Both ids added to
`data/submissions-processed.json`.

## 2026-09-11 (continuation) - Lausanne, Minneapolis, Salamanca, Spokane opened; Monterey deepened to 3

Merged the results of a verify pass an earlier attempt this window left
uncommitted: Lausanne 8 trees flagged (7 approximate pins, 1 confirmed;
several with disputed ages between the city's own register and its tourist
office, printed as disagreements rather than resolved), Salamanca 4 (1 with
no age at all, stated plainly), Minneapolis 4 (mostly city-park champions
with thin single-newspaper sourcing, flagged), Spokane 6 (3 old-growth
Douglas firs resting on one 2019 newspaper feature, flagged; 3 more from the
city's own Heritage Tree Registry cross-checked against a 2012 HistoryLink
survey). Wrote the 5 stories the verify pass had left undone via a
write-stories agent, then wrote each city's page-level content (intro,
meta_description, the oldest-tree question page, FAQ) from the same verified
facts and merged all four into `data/cities/`.

Also added mty_002 (Old Veteran of Point Lobos) and mty_003 (Moon Tree of
Friendly Plaza) to the already-published Monterey, previously trimmed to
just the Lone Cypress by a prior continuation the same day pending "a 4th
tree or an independent fame case." Treated this as ordinary city growth
(Monterey already has a page) rather than a new below-floor decision;
flagged in LOG.md as a judgement call in case Hidde reads the close call
differently.

Released the Boise and Baltimore claims: both still sit at 2 verified trees
with nothing that clearly clears the "would someone travel for this one
tree" bar (Boise's moved sequoia and Baltimore's Liberty Tree are good local
stories, not obviously destination-tier), so both stay banked in their
research files rather than shipping padded or under a stretched exception.
Lagos-PT (1 tree, unconfirmed public access) stays banked too.

## 2026-09-11 (continuation 4) - 4 stranded verify passes shipped under the single-famous-tree exception: Indianapolis, Sao Paulo, Busan, Monterey

Continuing the same window's earlier finding (6 cities banked below the 4-tree
floor with finished stories, logged in the prior LOG.md entry). Re-checked
`passcheck.py --pending` and found 4 more sitting in the same state that the
prior continuation had not resolved: Indianapolis (1), Sao Paulo (1), Busan
(2) and Monterey (3), all fully verified and written, none merged because
none reaches four.

Rather than leave these banked again, applied the 2026-08-31 single-famous-tree
exception (DECISIONS.md) to each on its own merits, following the precedent of
Kasukabe/Aguas de Moura/Rumskulla (single trees) and Zilina (a 3-tree page
shipped whole under the same exception):

- **Indianapolis** (ind_001, the Kile Oak): largest bur oak in the metro,
  protected by one family's promise since 1928, an international visitor
  guestbook kept since then. Ships alone.
- **Sao Paulo** (spa_001, Figueira das Lagrimas): reportedly the oldest
  documented tree in a city of 12 million, heritage-listed since 1989, real
  historical weight (soldiers and students said goodbye here). Ships alone.
- **Busan** (bsn_001/002): both independently designated South Korean Natural
  Monuments (No. 168 and No. 270), not a hero-plus-filler page; each one
  clears the fame bar on its own. Fixed a hard-rule-9 collision on the way in
  (bsn_002's species said "Black Pine / Japanese Black Pine", two names for
  Pinus thunbergii; corrected to the one already used for Hiroshima and
  Kagoshima's designated pines).
- **Monterey**: trimmed from 3 candidates to just mty_001, the Lone Cypress,
  a registered trademark and (by any account) the most photographed tree on
  the California coast, comfortably the clearest single-tree case of the
  four. Held mty_002 (Old Veteran of Point Lobos) and mty_003 (Moon Tree) back
  in `data/research/monterey-verified.json`, already written, for a future
  pass to add once the city has a 4th tree or its own independent fame case.

This is a judgement call, flagged as such because it is a close one: the
exception's worked examples (Angel Oak, Castagno dei Cento Cavalli, Bartram's
Ginkgo) are solitary trees, and Busan bends that to two independently-famous
trees at two different sites in the same city rather than one ensemble. The
Zilina precedent (a hero plus two companions) suggests this is within the
exception's intended range rather than outside it, but it is Hidde's to
overrule if he reads it differently.

Left Baltimore (2), Boise (2), Lausanne (3), Minneapolis (3), Salamanca (3),
Spokane (3) and Lagos-PT (1) banked as before: none of their hero trees read
as clearly "would somebody travel specifically for this" (Boise's moved
sequoia and Baltimore's Liberty Tree are good local stories but not
obviously destination-tier), and Lagos-PT's cork oak additionally has
unconfirmed public access, which would need resolving before it could ship
under any rule. A future pass should either find each of these a tree to
close the floor, or make an explicit fame case the way this entry did.

Regenerated `data/tree-index.json`, ran `preflight.py` (0 problems after
fixing the Busan species name and a stale Zwolle tree-count/meta_description
left over from the Zwolle merge in the next entry), `superlatives.py` (no
collisions), full `astro build` and `qa.py`.

## 2026-09-10 (continuation 8, photo follow-up)

Ran `photo_hunt.py`'s free API sweep against the 40 oldest photo-less trees; five of the day's new single-tree places (Lecina, Mendaza, Cabeza del Buey, Muxika, Cerro Veronese) turned up candidates. Fetched and looked at all 15 images by eye against the Cadiz standard. **5 approved**, all CC BY-SA with named authors: Lecina (a wide shot with people for scale, matches the platform/wall setting), Mendaza (shows the hollow trunk and buttresses precisely), Cabeza del Buey (the elm grove in leaf with support props visible), Muxika (the low-branching crown structure), Cerro Veronese (crown and trunk in the piazza). 1 held (Lecina's second candidate, a good wide crown shot, kept as backup rather than shipped since one photo per tree ships). 3 rejected: two of Cabeza del Buey's candidates were an interpretive sign and a commemorative plaque, not the tree; one of Muxika's was a leaf close-up.

**The Cabeza del Buey sign photo turned out to carry a real measurement we did not have**: "PERÍMETRO DEL TRONCO: 7 metros" (girth), matching the age band and height already on file. Added as a fourth source (an on-site interpretive panel is a primary source, photographed and Commons-hosted under CC BY-SA) and filled `girth_cm: 700`; adjusted the story, FAQ context word count stayed within Contract B's 150-200 range after the edit.

## 2026-09-10 (continuation 8) - Finished a standing write claim, 3 new single-tree places from `_famous-spain`, and a rung-2 build fix

An earlier attempt in this window stopped early having claimed `_famous-spain` for a write pass and written only one of its four verified trees (Lecina, left uncommitted). Finished the remaining three directly rather than dispatching a fresh write-stories pass, since three trees is under BRIEF_WRITING.md's usual batch size and the facts were already sitting verified in `data/research/_famous-spain-verified.json`.

All four are new single-tree places under the 2026-08-31 destination exception, each carrying a national or European recognition that makes the destination test easy: **Lecina** (Carrasca Milenaria, European Tree of the Year 2021, 104,264 votes), **Mendaza** (Encina Tres Patas, a hollow holm oak on three buttress legs, Spain's 2007 longevity award), **Cabeza del Buey** (the Centenary Elms of the Ermita de Belen, a seven-tree grove that survived Dutch elm disease, Spain's Tree of the Year 2017), and **Muxika** (Urkietako Artea, a holm oak far outside its usual range, one of only two centenarian holm oaks in Biscay). Muxika's verify_notes flagged a weaker destination case (no international award, just a local protection decree) and a placement question (too far from Bilbao for a day-trip fold-in); per the standing rule that a judgement call about fame never blocks publication, it shipped as its own place rather than being held.

**Caught an id collision before it shipped:** the verified file carried the Cabeza del Buey elms as `cdb_001`, which collides with Cordoba's existing `cdb_` prefix (18 trees). Renamed to `ebe_001` (Ermita de Belen).

preflight caught four real problems on the first pass, all fixed: Ulmus minor needed one canonical common name (Field Elm, matching Paris and Parma, not the Common Elm the verify pass had used), two meta_descriptions over the 155-char limit, and Cabeza del Buey's question_context 28 words over Contract B's 150-200 range.

**Rung 2: Build and deploy was failing (caught via `health.py`), fixed before anything else.** The prior push (Cerro Veronese / Genoa) had added Florence's `flo_021` with `access` and `transport` filled in English but not in the Italian overlay; `i18ncheck.py` gates the deploy on exactly this. Filled both fields in `data/i18n/it/florence.json`, confirmed clean.

Build (5334 pages), preflight (0 problems), superlatives (355 claims, no collisions) and qa.py (1 pre-existing sitemap/lastmod discrepancy, same one continuation 7 flagged as unrelated) all clean. Released the `_famous-spain` claim and emptied the now-fully-written verified file.

## 2026-09-10 (continuation 7)

**Photo viewing pass, 0 approvals, but 4 of 5 fetched cities duplicated continuation 6's pass from minutes earlier in the same window.** Dispatched `photo_fetch.py --zero` against `photo_gaps.py --shortlist` (Leeuwarden, Tilburg, Helmond, Maastricht, Eindhoven, Budapest, Kamakura) without checking CURATION.md first, which would have shown continuation 6 had just fetched and judged Leeuwarden, Helmond, Kamakura and Maastricht (plus Tilburg/Budapest, empty) with the identical result. Independently confirmed 0 usable on all four (16 images: a horse statue, a museum facade, a garden fountain, Stolperstein memorial plaques, a fortress wall, a shrine crowd scene, a torii gate with no tree as the subject), which is the same filename/geosearch-matching noise CLAUDE.md already documents, but the confirmation cost a fetch pass that should not have run. **Eindhoven is the one new result**: 3 candidates for ein_012 (The Catalpa of the Van Abbemuseum), also all wrong subject (horse statue, fountain, museum facade). The gap: "photo" kind passes have no claim mechanism the way verify/write do, so nothing stopped two runs an hour apart reaching for the same shortlist. Not re-hunted further; recorded so a third pass does not repeat any of these six cities.

**Fonte Colombo and Macugnaga (Italy, from `_famous-italy-verified.json`) held rather than published.** Re-checked both this pass (fresh web search): Fonte Colombo's "Tree of Perfect Gaiety" downy oak still has only one real source (a Commons file description); no second source found despite two searches across two passes. Macugnaga's Old Lime is a genuine, two-sourced heritage tree but reads as a nice tree in a town people visit for other reasons (Monte Rosa hiking/skiing) rather than a destination in its own right; held on the single-famous-tree test rather than the sourcing bar. Both remain in `data/leads/_famous-italy.json` as `held` with the reasoning; `_famous-italy-verified.json` trimmed to just these two.

**A dead-register tree reached a write pass and was caught before push.** Dordrecht's Van Baerleplantsoen plane (LRMB nr 1680276) shipped as dor_021, then `preflight.py`'s `check_register_says_the_tree_is_gone()` (added earlier the same day, after the Utrecht incident) flagged that the register's own status column marks this entry 5, Dood/geveld: dead. Reverted the tree, marked the lead blocked. The actual gap was upstream: `leads.py --ready` had offered this candidate as clean because its READY classifier never read the register's own status field. Fixed in `scripts/leads.py` (checks `register_nr` against the LRMB dead list before classifying anything READY); on its first run this also reclassified 20 other leads corpus-wide from READY/NEARLY to correctly blocked, not just the one that had already gone out.

## 2026-09-10 (continuation 6) - Recognition-line backlog closed to zero; a photo shortlist viewing pass found nothing usable

Closed the recognition-line backlog (CLAUDE.md rung 7, "every tree gets one
eventually") to zero: 110 trees across 104 cities, the last alphabetical tail
from Nedvedice through Zywiec, all restated from species/girth/height/setting
/access/story already on file, none of it new research. `recognise.py --stuck`
was already at zero; this closes the wider gap, not just the trees with nothing
else to go on. Build (5296 pages), preflight (0 problems) clean.

Also released three stale claims found standing at the top of the window
(brisbane, milan, taormina), all already documented dead ends this same week:
Milan's register verify pass has returned zero twice, Brisbane is on its fifth
zero-yield deepen attempt, Taormina's in-comune register trees are confirmed
private hotel grounds (four times over).

**Photo shortlist viewing pass, 8 cities, 0 usable.** `photo_gaps.py --shortlist`
named one candidate per photo-less city (leeuwarden, tilburg, helmond,
maastricht, budapest, delft, dallas, kamakura); fetched and looked at the
closest-distance candidate for leeuwarden, helmond and kamakura by eye rather
than trusting the filename match. All three were wrong: a bird sculpture (De
Zeven Snippen) for Helmond's Copper Beech, a wide shot of Kenchoji's main hall
for the Junipers of Kenchoji it was nominally matched to, and a canal cityscape
for Leeuwarden's Julianaboom. The remaining five cities' top candidates read the
same way by filename alone (a Stolperstein memorial plaque for Maastricht, a
sculpture and building photos for Tilburg, nothing queued at all for Budapest/
Delft/Dallas) and were not fetched, since the pattern was already established.
This is filename-matching noise of the kind CLAUDE.md already documents
(Cagliari, Copenhagen); a `photo_hunt.py --recheck` API sweep across all 8
cities' 40 unchecked trees afterward found almost nothing new (0 new
candidates on 36 of 40, one new candidate each on two Molenstraat Cemetery
trees, four new on the Copper Beech of the Kromme Steenweg), confirming the
Commons coverage for this batch is close to genuinely exhausted rather than
merely unhunted.

## 2026-09-10 (continuation 5) - Fort Lauderdale opened (4 trees), Daytona Beach stays closed

Daytona Beach (#65): scouted, empty. Its county's only register supply (2 Florida Champion Trees, Volusia County) sits 20+ km out with no public transport, too thin and too far to open the city. New entry in `data/register-scouting.json`.

Fort Lauderdale (#57): opened with 4, all at Flamingo Gardens (Davie), all flagged for missing age since the Florida Champion Tree register scores size into points rather than dates. A fifth candidate, a Hollywood baobab the register lists at 10.6m round, was held rather than shipped: no second source could be reached to corroborate that specific figure (monumentaltrees.com's matching page is Cloudflare-gated, no Wayback snapshot). Kept as a note in OPEN_DATA_SURVEY.md. The page is currently 100% paid entry (Flamingo Gardens admission); free candidates exist nearby in Broward County's remaining register rows for a future pass.

## 2026-09-10 (continuation 4) - Finished stranded Berlin/Prague/Oahu passes; Dordrecht's Oosterse plataan stays a lead

Berlin +1, Prague +4, Oahu +2 (see LOG.md for the trees): all three verified against preflight and superlatives, no gaps beyond the usual honest ones (Berlin's beech and both new Prague oaks have no photo yet). Dordrecht's Van Baerleplantsoen Oosterse plataan (LRMB register nr 1680276, planting band 1830-1840, no girth or height) is still a single-source candidate: the municipality's 2020 Bomenlijst PDF that would corroborate it serves a bot challenge live and did not OCR from the Wayback copy, on two separate attempts now. Stays in `data/leads/dordrecht.json`; needs either a readable copy of that PDF or a fresh search on "Van Baerleplantsoen" plus a species word.

## 2026-09-10 (continuation 3) - Leeuwarden 34 -> 41, plus a 116-tree recognition-line sweep across 30 cities, and git push broke partway through

**Leeuwarden 34 -> 41.** `scout_next.py --target` pointed back at Leeuwarden (44 unjudged register trees still in hand). Claimed it, dispatched a verify pass on the closest unmined LRMB candidates: 7 delivered (lee_035-041: pollard limes at the Liauckama House, an adoption beech and twin beeches at two almshouses, a Caucasian wingnut the register calls Friesland's champion of its species, a second plane in the Old City Cemetery, a silver lime at Sophiaplantsoen, a beech at Diaconessenpark), 5 blocked (1 confirmed felled in the register's own history text, 4 marked `visitable=nee`). The pass caught a WebSearch summary inventing a girth and age for one candidate, sourced to a scanned 1991 PDF with no extractable text, and correctly discarded it rather than publishing a fabricated measurement. Dispatched a write pass on the 7; at merge, fixed three species-name collisions the build caught (lee_039's plane renamed to match lee_004's "London Plane", lee_035 and lee_037/041 stripped of variant common names against the site's established "Common Lime" and "European Beech"), and updated the tree-count copy (34 -> 41) in the intro and meta description. `preflight.py` 0 problems, build clean, claim released.

**A 116-tree recognition-line sweep, 30 cities, done directly rather than through a dispatched pass.** The sitewide gap (384 trees with no `how_to_recognise`) had no city above 4 missing, so this was pure restatement work per BRIEF_WRITING.md: species, girth, height, setting and what each story already says, nothing invented. In four batches: Tilburg, Nijmegen, Kanazawa, Granada, Delft, Cagliari, Brno, Belgrade (32); Zilina, Ypres, Zaanstad, Yabu, Washington DC, Tarragona, Sydney, Stockholm, Sardinia, Plunge, Oss, Matera, Los Angeles, Kauai, Higashiomi (45); Helsinki, Glasgow, Eindhoven, Caserta, Brzoza, Bruges, Boston (21); Zurich (Marthalen/Boezberg), York, Wessobrunn, Waipoua Forest, Uda, Sorrento, Shokawa, Savannah, San Diego (18). Gap now 268. `preflight.py` clean after every batch, build clean.

**FOR HIDDE: git push broke partway through this run and was still broken when it ended, the same failure LOG.md recorded earlier today: "remote: Invalid username or token. Password authentication is not supported for Git operations."** Fetch works fine, only push fails, confirming it is the installation token rather than anything in this checkout. Every commit below is sitting local in the shared runner checkout; nothing is lost, and they will reach GitHub the moment push works again, whether the harness refreshes the token on its own (as it apparently did earlier today, per the entry below) or the GitHub App installation needs a look.

## 2026-09-10 (continuation) - Finished four claims an earlier attempt in this window left standing: Dordrecht +4, Montreal +4, Granada (es) and Kamakura (ja) committed

The previous attempt in this window stopped after 23 minutes having shipped
nothing, with 97 of its 120 minutes unspent. `passcheck.py --claims` found
four standing claims, all with fully- or partly-finished work already on
disk: dordrecht (verify), montreal (verify), granada (translate-es), kamakura
(translate-ja). Finished all four rather than releasing them.

**Dordrecht (verify, released): +4 trees, 16 -> 20.** dor_017 and dor_018
(the plane and horse chestnut of the Willem Kes Plantsoen, Bomenridders
route corroborated) already had stories from the earlier attempt. dor_019
(Huis van Gijn garden plane) and dor_020 (Huis van Gijn garden variegated
maple) were verified but storyless; dispatched a write-stories pass for
those two plus four Montreal trees. Fixed the tree-count copy (meta
description, question_meta, the free-vs-paid FAQ) from sixteen to twenty and
added `paid_entry: true` on dor_019/020 (Huis van Gijn charges for garden
access), which preflight's paid-entry-mismatch check caught.

**Montreal (verify, released): +4 trees, 7 -> 11.** mtl_008 (Second Oak of
Summit Woods, Westmount, a separate peak of the same massif), mtl_010 (Class
of '49 Tulip Tree), mtl_011 (Roddick Gates Black Walnut) and mtl_012 (the
purple-leaved European beech by Redpath Hall, corrected to "Copper Beech" at
merge: the astro build caught it claiming a second common name against
graz/leipzig's "Copper Beech" for the same cultivar, hard rule 9). Rewrote
the city's intro, meta description, question_meta, question_context and the
"one walk" FAQ to describe the new shape: six trees on Mont-Royal itself,
four in a walkable McGill-campus cluster (was one, the ginkgo, now four),
one on Westmount's own summit as a separate short outing.

**mtl_009, the McKenna Cottonwoods, held back rather than shipped.**
`passcheck.py --pending` flagged it as sitting exactly 0m from the
already-published mtl_004, a different species (cottonwood vs Austrian
pine). Refetched the source page directly: it gives no coordinate at all for
this tree, only a cemetery block and headstone number, so the verify pass
had filled the coordinate field with the cemetery's generic main-entrance
point, identical to mtl_004's. Publishing it would have sent a reader to the
wrong tree at the one field that cannot be corrected after the fact. Folded
into `data/leads/montreal.json` with the block/headstone detail preserved,
ready the moment someone can place it on a cemetery section map. The
"passcheck flags mtl_010 too" question was also checked by hand: different
species (ginkgo vs tulip tree), two independently documented specimens 46m
apart on a large campus, not a duplicate, written as normal.

**Granada (es) and Kamakura (ja): both already hand-quality, both
committed.** `i18ncheck.py` clean on both, overlay coverage complete (9/9
Granada trees, 6/6 Kamakura trees), no action needed beyond verifying and
releasing the claim.

**A gap closed in `scripts/leads.py`'s READY classification.** Sampling the
three "READY" Eindhoven leads by hand found all three were actually
declined, in language the `NOT_READY_MARKER` regex did not catch: "second
source not found" (word order reversed from the existing "no second
source"), "do not ship on the register alone", and a register whose own
location field is marked uncertain. Added three patterns; Eindhoven's three
leads now correctly classify as BLOCKED instead of READY. None were written
up.

Full rebuild and `preflight.py`/`qa.py`/`superlatives.py`/`i18ncheck.py` all
clean (the sitemap-lastmod QA warning is the same shallow-clone sandbox
artifact noted in earlier entries, not a content problem). All four claims
released. `data/agent-costs.json` logged for the write pass.

## 2026-09-10 - Two Kyoto submissions (98, 99): GPS only, not enough to identify a tree

Submissions #98 and #99 in the `submissions` table, kind `tree`, `page: app:collect`,
both from the same account (Hidde's own, burgmans.hidde@gmail.com, the same one
behind the Nara and Baarn sightings) via the contribute form on 2026-09-10. Both
carry nothing but a GPS fix ("standing at the tree") and a city name: no name, no
species, no note, no photo. #98 sits at 35.00566, 135.77446 (Higashiyama, ~600m
from kyo_005, near Kennin-ji/central Gion). #99 sits at 35.00522, 135.77953
(Higashiyama, 183m from kyo_005, plausibly inside Maruyama Park or the adjoining
Chion-in/Shoren-in grounds, but too wide a net at that distance to name a specific
tree honestly). Recorded as two thin leads in `data/leads/kyoto.json` rather than
guessed at; neither can be verified or published from coordinates alone. Both ids
added to `data/submissions-processed.json`. Needs a name, species or photograph to
become a real candidate; a future pass or the submitter can close the gap.

## 2026-09-10 - Finishing four claims an earlier attempt left standing, plus the deploy break it was sitting next to

Started from `python3 scripts/passcheck.py --claims`: valencia (verify, 25 min
left), cordoba (write, 147 min), utrecht (photo, 147 min), arnhem (photo, 147
min), all held by the previous night-run. Finished or advanced all four
rather than releasing them unfinished, per the standing instruction that an
unfinished claim is the strongest predictor of a wasted window.

**Valencia (verify -> write, released):** the earlier verify pass had left 3
verified trees in `data/research/valencia-verified.json` numbered vlc_027-029,
which collided with 3 Botanic Garden trees a concurrent pass had already
published under those exact ids. Renumbered to vlc_030-032 (confirmed free via
`passcheck.py --brief valencia`), then dispatched a write-stories pass. Added:
the Norfolk Pine of Vila de Sant Josep (Burjassot, a separate municipality
4.3km out, labelled honestly as a day-trip stop rather than folded into
Valencia proper), the Canary Palm of Gran Via (flagged for the red palm
weevil risk reported on the same avenue), and the Fig of the Hort de les
Camelies (flagged for a thin second source and 3.3km distance from the
published cluster). Valencia now 31 trees, was 28. The write pass caught two
stale tree-count promises (question_meta, the access FAQ's free-count) in
both the English and the Spanish overlay and fixed them same pass. Claim
released.

**Cordoba (write claim, actually a translation; released):** no
`cordoba-verified.json` existed, so there was no story-writing work standing
behind this claim. What was actually sitting uncommitted was a complete,
hand-quality Spanish overlay (`data/i18n/es/cordoba.json`, rung 0b: Spanish
holds a ROLL OUT verdict and Cordoba's English page already earns
impressions), all 16 trees translated, `i18ncheck.py` clean. Committed as is.
Claim released; the mismatch between the claimed kind and the actual work
product is worth naming so a future `--claim` call names the true kind.

**Krakow (unclaimed, found alongside these):** a general photo-judge sweep
sitting in the same uncommitted diff had approved 2 Krakow photos (the
Straszewskiego ash, the Karmelicka elm) among ~30 rejects across several
cities. Applied and vendored (`vendor_photos.py`); both were still pointing
at upload.wikimedia.org, which is how the app's images start failing per the
session-start warning.

**Utrecht (photo, in progress):** the same sweep had judged some but not all
candidates for Utrecht's queue and found one approval already sitting
unapplied: the Liberation Beech of Servaasbolwerk (utr_015), a copper beech
positively identified by its own memorial sign. Applied and vendored.
Dispatched a further photo-judge batch on the remaining unjudged Utrecht/
Arnhem candidates before releasing either claim; see the next entry once it
reports back.

**The actual rung-2 item: Build and deploy was failing**, and it had nothing
to do with any of the above. `gh run view --log-failed` on the newest failed
run showed `scripts/i18ncheck.py` refusing the build over 6 missing
access/transport fields in `data/i18n/it/florence.json` (flo_016, flo_018,
flo_019), left behind by the 2026-09-09 Florence backfill that filled those
fields in English and never touched the Italian overlay. Translated and
filled the three missing pairs. `i18ncheck.py`, `preflight.py`, `astro
build` and `qa.py` all clean afterward.

## 2026-09-10 (continuation) - Alicante verify claim: register radius confirmed exhausted, one new news-sourced lead recorded, zero delivered

Dispatched the standing `alicante` verify claim (picked up from an earlier
attempt in this same window rather than left to expire). Re-confirmed
independently that the register radius is exhausted exactly as the
2026-09-09 entry above already recorded: all 43 "unmined" candidates in
`passcheck.py --brief alicante`'s printed list resolve to already-published
trees or already-recorded leads/blocked entries in `data/leads/alicante.json`.

Found one genuinely new thread via local news search (a source class outside
the register): an August 2026 emergency-pruning story (todoalicante.es,
cope.es, elperiodic.com, alicantepress.com, all one underlying event) about a
"ficus centenario" near the Castillo de Santa Barbara elevator tunnel,
Avenida Juan Bautista Lafora, roughly 100-150m from the published ali_011
(Paseito de Ramiro figs). No girth, height or exact address given, and two
nearby OSM `denotation=natural_monument` nodes carry no species tag and are
not in the Valencia register. Genuinely unresolved whether this is ali_011
described loosely or a third, uncaptured fig, so recorded as a lead with
both OSM node ids and what a future pass needs (a photo comparison or a
street-level look) rather than guessed at. Claim released; zero trees
added to Alicante this pass (still 16, target 20).

## 2026-09-10 (continuation) - Recognition lines: Tokyo (15), Madrid (15), Palermo (14) written

Rung 7 work (recognise.py --stuck was 0, but the wider "every tree eventually"
backlog stood at 1004 trees missing `how_to_recognise` across the site).
Dispatched three write-stories passes in parallel, one per city, each given
the full `recognise.py --brief <city>` output and told to restate only,
never invent. All three applied cleanly: `recognise.py --apply`, then
`preflight.py` (565 cities, 0 problems) and an astro build, all clean.
Longest line 236 characters, under the 240 limit; no em dashes anywhere.

**One pre-existing issue surfaced, not fixed this pass:** Palermo's pal_015
story claims to be "the smallest and shortest of the figs on this list" at
8.2m round, but pal_002 (the Falcone Tree, a memorial fig) is 2.91m round,
genuinely smaller. The recognition-line pass for pal_002 and pal_015
deliberately avoided repeating pal_015's false superlative in the new lines,
but the story text itself still says it. Worth a one-line story edit in a
future pass.

Remaining recognition-line backlog after this pass: roughly 960 trees
across the rest of the site (was 1004; Tokyo, Madrid and Palermo's combined
44 are now written). Biggest remaining: Bucaco (13), Fukuoka (12), Dublin
(12), Warsaw (12), Istanbul (12), Groningen (12), Florence (12), Cordoba
(11), Rouen (11), Padua (11).

## 2026-09-09 (continuation 3) - Florence: backfilled 3 thin entries rather than duplicating them, caught before it shipped

Claimed Florence (rank #13, register-backed room to grow toward its 30-tree
target) for verify. Dispatched a pass against four single-sourced leads in
`data/leads/florence.json` (the Bobolino stone pine, the Giardino Simone
Weil Monterey cypress, the Monte alle Croci cypress, the Via Giramondino
Aleppo pine), each blocked only for want of a second source. Found RAMI
(ilregistrodeglialberi.it) per-tree pages for three of the four, each
carrying an independent site-visit survey (its own GPS, a re-measured
height, a vitality call, sometimes a dated photo) that genuinely
corroborates the MASAF national register designation rather than repeating
it, plus a comune di Firenze elenco announcement as a third confirmation.

**The write pass caught what the verify pass missed: all three were already
published**, as flo_016, flo_018 and flo_019, matched one to one on their
MASAF designation codes. Good process working as intended: BRIEF_WRITING.md
told the writer not to ship a duplicate over good live copy, it refused,
and it flagged exactly the right next step instead. Retargeted as a
backfill: the three live entries were thin (empty access, address,
transport, single bare-string source, `location_precision: approximate`)
against what this pass had just found. Filled all three from the verified
research, added the RAMI and comune sources, and moved `location_precision`
to `confirmed` on the strength of RAMI's own independent survey GPS
matching the register point to 5 decimal places. Lightly edited each story
where it flatly said "one source" or "no corroboration", since that
sentence is now false and would sit on the page telling a reader something
untrue; kept the storytelling voice and trimmed flo_018 back under 250
words after the edit. The Monte alle Croci cypress's access field carries
the comune's own restoration-phasing caveat (only the lower section to the
Rose Garden entrance was confirmed reopened as of Dec 2024), written as a
plain fact for the visitor rather than an instruction to ourselves, which
the write pass flagged as a TONE_OF_VOICE.md v1.1 issue in the verify
record's draft wording.

The fourth lead (Giardino Simone Weil Monterey cypress) did not clear the
bar: RAMI's only Monterey cypress in Florence is a different, already-
blocked tree at the Arcetri Observatory. Left as a lead with the search
documented so a future pass does not repeat it. Build, preflight and qa all
pass. Claim released. No new tree count change (still 23 trees), but three
pages are now real pages instead of near-empty placeholders.

## 2026-09-09 (continuation 2) - Milan +1 (22 -> 23): resolved a lead stuck since 2026-08-06, confirmed the city's official register is exhausted

Milan is rank #3 in CITY_QUEUE.md with room to grow toward its 30-tree target
(rung 4/CITY_QUEUE.md stage 2 deepening, register-backed so cheap). Claimed
for verify. Four prior verify passes (2026-08-06 through 2026-09-07) had
already worked the near-centre MASAF register candidates to exhaustion; this
pass independently re-confirmed that rather than trusting the note, then
found one new angle: the comune di Milano's own monumental-tree pages moved
to a new URL path (`/aree-tematiche/verde/manutenzione-progettazione/
alberi-monumentali/...`) that is not 403ing the way the old path was.

That closed the long-standing single-sourced "Two further planes inside the
Giardini Montanelli" lead: **mil_023, Il Platano Grande dei Giardini
Montanelli**, 625 cm girth, one of the widest trunks the city has measured,
crown split by lightning and cabled back together, a woodpecker cavity in
the burn scar, a Universita Bicocca microfauna study, and a healed-over
attempt to saw into the trunk. Age is undocumented in both sources; derived
a broad 100-200 year band by analogy with two sibling planes in the same
garden already published from girth, stated as an estimate rather than a
fact. One numeric discrepancy recorded rather than resolved: the comune's
own page states a 260cm diameter (about 817cm circumference) against the
register's 625cm girth for the same sheet id.

Cross-checking the comune's own 13-tree official monumental list against
our data closed the loop: **Milan's official municipal register is now
fully exhausted**, all 13 sheet ids accounted for (11 published, 2 already
blocked as the children-only Villa Belgiojoso garden). The wider MASAF
national register still carries additional Milan-area rows beyond this
official 13 (e.g. the Villa Litta Modignani plane pair at ~4.7km, a Parco
Sempione cedar with a documented felling risk); those remain leads in
`data/leads/milan.json`, unchanged, needing a source beyond the register
alone. Updated the Italian translation overlay (`data/i18n/it/milan.json`)
with mil_023 and the count fix (22 -> 23), since Milan/it already earns
impressions and every change ships in every language. Intro/meta/FAQ counts
fixed in both languages; the English intro had been stuck at "Twenty-one
trees" against a meta description already saying twenty-two, a pre-existing
mismatch fixed in passing. Build, preflight and qa all pass. Claim released.

## 2026-09-09 (continuation) - Leeuwarden +8 (18 -> 26), third verify+write pass on the same claim today, released

The standing `leeuwarden` verify claim (made 22:12 UTC by an earlier attempt
in this same window, which pivoted to finishing Valencia instead and never
did the work) was picked up and finished rather than released unworked. This
is the third time today Leeuwarden has been deepened; the register-candidate
pile is now genuinely thin, so this was a bounded 30-minute pass rather than
another full sweep.

Three trees from the Diakonessenhuis garden cluster (lee_019 red horse
chestnuts, lee_020 white horse chestnuts, lee_021 London plane, LRMB register,
planted 1880-1890): the former hospital (closed 1987) became apartments in
1988-1990 and its garden survives as Diaconessenpark. Checked current access
from OpenStreetMap rather than assuming from the register's mixed owner field
(2 of 3 entries say owner=particulier): the courtyard is tagged as a public
park with paved, gate-free footways past all three trees, so shipped as open.
lee_020's register history flags a real health problem, a cavity with fungal
infection and bleeding canker; said so plainly in the story rather than
hiding it, per the standing "alive but declining is fine to say" rule.

Five more from named-but-previously-uncoordinated HCL brochure and IVN
walking-page entries, each single-sourced and geocoded to their named
landmark rather than a trunk, so all ship `location_precision: approximate`
and `curation_status: flagged`: lee_022 the Crimean Linden of Blokhuisplein
(dated 1954), lee_023 the Cedar of Lebanon at the Gabbema Gasthuis (dated
1906, access left as "visible from the street, unconfirmed" since it's an
almshouse like the already-blocked Sint Anthony Gasthuis trees), lee_024 the
leaning, propped Black Locust of Westerpark (dated 1924, named twice in the
same brochure), and two Silver Limes (lee_025 Druifstreek, lee_026 Eewal)
from IVN's own page, both undated, age left empty per the ask-the-reader rule
rather than guessed.

`data/leads/leeuwarden.json` updated: the 6 leads these trees resolve moved
into a `resolved_2026-09-09` section explaining each outcome; 7 unresolved
leads (two cemetery trees, two Vosseparkje elms, a Vosseparkje poplar and oak,
a PDF-garbled tree name, a possible beech) and the 2 blocked Sint Anthony
Gasthuis entries are untouched. City intro/meta/FAQ text updated from
eighteen to twenty-six trees. Species normalised: the two Silver Limes
arrived as "Tilia tomentosa" / "Silver Linden" and were renamed to the
canonical "Silver Lime" already used by 9 other trees and data/species/
silver-lime.json (hard rule 9). Build, preflight and qa all pass. Claim
released.

Left in `data/leads/leeuwarden.json`, not chased this pass: the municipal
"Lijst van monumentale en waardevolle bomen" PDF likely carries addresses for
the remaining 7 leads, but its font has no ToUnicode CMap and this
environment has no PDF text-extraction library and no pip install
permission, so regex extraction on the decompressed content streams produced
only garbled glyph codes. A future pass with PDF tooling should re-fetch it.

## 2026-09-09 (continuation) - Valencia +3 (25 -> 28): finished a stranded verify+write pass, closed a species gap, released the claim

Picked up this window's own standing Valencia verify claim: the working tree
already held a complete, unmerged write pass (3 new trees fully sourced and
written into data/cities/valencia.json, plus how_to_recognise lines) from an
earlier attempt in the same window that stopped without committing. Verified
the work rather than redoing it, fixed what was wrong, and shipped it.

**The three trees, all in the Jardi Botanic de la Universitat de Valencia**,
sourced from the regional monumental-tree register plus the garden's own
virtual species catalogue (two independent sources each): vlc_027 a
Brachychiton populneus (register nickname "Arbre botella del Botanic II"),
vlc_028 a Pecan (Carya illinoinensis, 32.9m/3.88m girth), vlc_029 a Common
Persimmon (Diospyros virginiana, dioecious, cannot fruit alone). None carries
an age; each says so once and asks the reader, per the standing rule.

**Two fixes before merging.** The new tree's species field said "Kurrajong
(Brachychiton populneus)"; Barcelona and Caserta already use "Bottle Tree" for
this species, so hard rule 9 requires one canonical name and it was renamed
to match (preflight had this as the sole FAIL). And the city's own count
copy was stale: question_meta said "twenty-four more" (25-tree count) and the
FAQ said "the other ten" share the paid Jardi Botanic; both updated to
twenty-seven/thirteen for the new 28-tree total.

**Paid share is now 13 of 28 (46%), further over the roughly-a-third ceiling
from CLAUDE.md's Amsterdam/Leiden ruling** (it was already 40% before this
batch). All three new trees sit in the same paid garden as most of Valencia's
existing depth, so this pass pushed the wrong direction; `check_paid_share()`
flags it as a NOTE, not a FAIL, but the next Valencia work should prioritise
FREE trees (Jardines del Parterre/Glorieta figs, street and park trees)
over further Jardi Botanic depth.

**Wrote the Spanish overlay for all three** (data/i18n/es/valencia.json),
translated by hand, including the species-name fix and the same count
corrections in the Spanish title/question_meta/FAQ; i18ncheck.py clean.
`check_overlay_coverage()` in preflight is a hard FAIL otherwise.

**Closed the species-page gap this created.** Adding the species-name fix put
Bottle Tree (Brachychiton populneus) at 3 trees site-wide (Barcelona, Caserta,
Valencia), which is pagegaps.py's threshold; wrote
`data/species/bottle-tree.json` (Contract F) in the same pass rather than
leaving it for a later run.

Build, qa.py (8097 pages), preflight (0 FAIL), superlatives.py (347 claims, no
collisions), tree_index.py and route_walks.py all clean. No token count for
this pass is logged to data/agent-costs.json: the write agent that produced
the 3 trees ran in an earlier, unlogged attempt in this window and its report
never landed, so a number here would be invented rather than measured.
Released the valencia claim.

The leeuwarden claim (also standing from an earlier attempt, register
candidates staged but unverified) is untouched this entry; see the next one
if a verify pass ran on it before the window closed.

## 2026-09-09 (continuation) - Sorrento verify claim finished: 0 new trees, register candidates exhausted at this radius

Picked up the standing sorrento verify claim (by night-run, from an earlier
attempt in this window). Dispatched a verify agent on all 19 MASAF register
candidates within 20km. Result: every close-in candidate was an exact
sheet-id/coordinate duplicate of a tree already live or already recorded as
a lead/blocked entry (the Grand Hotel Parco dei Principi cluster, the Antico
Parco del Principe trio, the Via Bagnulo pine, the Riviera Massa olive
group). The one genuinely unexamined candidate, Eucalitto blu of Matignano
(2.9km), turned out to be in Vico Equense on a private residence's boundary
wall (Villa Thuja) with no source confirming street visibility, so it's
blocked on both container and access. Two more distant candidates (a
mulberry and an olive in Massa Lubrense) filed as leads for a future
Massa Lubrense page rather than researched further. Sorrento's register
supply is exhausted at this pass's scope; not worth another verify pass
without a new source. Released the claim.

## 2026-09-09 (continuation) - Leeuwarden +3 (15 -> 18), finished the second verify claim

Two earlier attempts in this window had stopped early with time still on
the clock; `passcheck.py --claims` showed a standing Leeuwarden verify
claim from the second of them, with 329 unmined register candidates and
an empty `data/research/leeuwarden-verified.json`. Dispatched a verify
pass focused on the close-in Vosseparkje/Westerpark cluster (~1km from
the Prinsentuin cluster already published) plus one central single-tree
candidate. It found second independent sources, mostly Historisch
Centrum Leeuwarden and IVN walking-tour PDFs, for 3 trees the earlier
register sweep had filed as single-source leads: a Caucasian wingnut
(130cm girth, flagged, the two sources place its immediate setting
slightly differently), a grey poplar dated to 1909 by name, and an
oriental plane by the former Beursgebouw, a different tree from the
already-published Stationsplein plane 800m away. Wrote all 3 stories and
recognition lines, merged, fixed the city's meta_description and intro
(both said "fifteen", now "eighteen"). 3 more Vosseparkje leads (two
feather elms, a Canadian poplar, a Caucasian/Persian oak) still lack a
second source; an unidentified golden-leaved companion tree beside the
wingnut and an unpinned leaning acacia (brochure stop VIII) are new
leads. Released the claim. qa.py and preflight.py both clean.

## 2026-09-09 - Leeuwarden +6 (9 -> 15), from a stranded verify claim

Wrote up 6 trees a prior attempt's verify pass had already fully sourced:
the Wilhelminaboom and Julianaboom (two royal commemorative limes on
Raadhuisplein and at the Jacobijnerkerkhof, both corroborated between the
Landelijk Register Monumentale Bomen and the gemeente/HCL 2022 walking
brochure), a horse chestnut and an oriental plane on the same brochure's
top-10 list, a Leopoldii maple in Rengerspark dated to the park's own 1904
opening, and a copper beech at Willemskade that used to be a fused pair:
the register's own history records the southern half felled in 2026 after
a fungus weakened its base, and the story says so plainly rather than
repeating the older IVN guide that still calls it a pair. All 6 flagged
where the two sources only roughly agree (a year or a decade band); none
invented. 0 flagged as unverifiable, 0 photos found this pass (none
hunted; out of scope for a write pass). 14 further leads from the same
register sweep sit in `data/leads/leeuwarden.json` for later, mostly
Vosseparkje register trees needing a second source and two twin-plane/
weeping-beech candidates near already-published trees that need walking
and pinning separately rather than guessing a coordinate from prose.

## 2026-09-09 - Cagliari +3, Sorrento +1: finished the stranded write claims from a prior attempt's git-push failure

Picked up the two claims left standing after an earlier attempt in this
window died on an expired git-push token (see LOG.md). Both cities'
verified research was already sitting on disk unmerged:
`data/research/cagliari-verified.json` (3 Orto Botanico specimens) and
`data/research/sorrento-verified.json` (1 tree, the Rovere of Vallone San
Giuseppe). Dispatched a write-stories pass across both in one context,
merged, fixed count-promising copy (intro/question_meta/question_context/
faq) in both cities and in Cagliari's Italian translation overlay
(`data/i18n/it/cagliari.json`, which needed the three new trees added too
or the build fails on `translatedTreePaths`'s "no translation" check).
Two word-count contract violations surfaced only at build time (intro
over 100 words, question_context over 200) in both languages and needed
trimming after the fact; worth remembering for future writes that touch
an already-live page's summary copy, since the writer only sees the
brief, not the live contract bars.

Normalised two species-name collisions the writer flagged rather than
silently resolved: `cag_013` from "Canary Islands Dragon Tree" to the
canonical "Dragon Tree (Dracaena draco)" (11 other live trees already use
the short form) and `cag_011` from "...subsp. columnaris" to the plain
"Moreton Bay Fig (Ficus macrophylla)" used everywhere else on the site.

Cagliari: 10 -> 13 trees, 8 of 13 now within 1.5km of each other in the
centre (the Orto Botanico's three sit 0.55-1.3km from the existing
Piazza Matteotti/Giardini Pubblici cluster). Sorrento: 6 -> 7, the new
oak a separate 25-30 minute uphill walk rather than joining the existing
Villa Fondi/cemetery cluster. Both flagged (derived ages: the three
botanical-garden trees have no register entry at all and are dated from
the garden's own claim that its notable specimens are founding-era,
1866; the Sorrento oak repeats "secolare" as vaguely as its regional
source gives it and notes nothing newer than a 2008 survey confirms it
still stands).

## 2026-09-09 - Dordrecht: finished the stranded verify claim, +3 trees

Continuation of an earlier attempt in the same window that stopped after
claiming Dordrecht for verify and downloading PDOK aerial imagery for nine
register candidates plus a Bomenstichting PDF booklet, without writing any
verdict. Picked the claim back up, judged the aerial evidence, cross-checked
against two independent sources (the Bomenridders Dordrecht walking route at
indordrecht.nl and, for the museum garden trees, the Dordrechts Museum's own
garden page) and shipped three: dor_014 (Oak-leaved Hornbeam, Park
Merwestein, a genuine two-leaf-shape cultivar and stop 8 of the city's own
walking route), dor_015 (three London Planes in the Dordrechts Museum
garden, dated to the museum's 1842 founding period) and dor_016 (three
beeches in the same garden, girths 315/300/300 cm, ages disputed by the
register's own admission). Dordrecht is now 16 trees.

Left unresolved rather than guessed at: three register candidates
("binnentuin" inner-courtyard trees behind Botgenstraat/Spuistraat,
Botgenstraat/Pelserstraat and the AMRO bank on Stationsweg) where aerial
imagery could not settle whether the ground is genuinely open to the public,
recorded as leads in data/leads/dordrecht.json with the specific aerial
evidence so a future pass does not re-fetch the same imagery. Also not
reached this pass: the Weizigtpark oak, Amerikaanse es near Merwesteinpark's
Vrieseweg entrance, the Kromhout canalside oak, two more planes (Baerleplantsoen,
Begraafplaats Dubbeldam) and the Huis van Gijn museum garden trees, all still
open in data/research/dordrecht-register-candidates.json.

The out_dordrecht_bomen.pdf the earlier attempt downloaded (the
Bomenstichting's "Langs monumentale bomen in Dordrecht" booklet) turned out
to carry no extractable text layer in this environment (WebFetch read it as
binary, and a manual zlib stream-extraction attempt found only image data,
not text streams); poppler-utils is not installed and apt-get/pip both need
approval this run does not have. Its content was not needed this pass since
web sources covered the same trees, but a future pass with rendering tools
available could still get more out of it.

## 2026-09-09 - Brisbane: sixth deepen attempt, still zero new trees

A verify pass hardened two open leads rather than repeating dead searches.
Bald Hills Hoop Pines: an Overpass query on the private school's own internal
driveways/footways confirms every one is `access=private` or `access=permit`,
turning the access block from an absence of evidence into a positive one; it
stays a lead. Toowong Cemetery's Ann Hill hoop pine: a WebSearch summary
claiming her grave is "marked by an urn-topped column opposite the brick tool
shed" turned out to be a fabrication when the actual source page
(museumofbrisbane.com.au) was fetched directly and contained no such
sentence; discarded per the search-summary-is-a-lead-never-a-source rule, and
the tree stays unpinned. New ground checked and closed: Kangaroo Point (no
named tree on Council's own trail page) and a Milton fig heritage listing
that turned out to be the already-published bne_020. One new lead recorded:
Indooroopilly Golf Club's own detailed ancient-trees page names real
100+-year specimens by golf hole, but gives no coordinates and sits on a
private members' course with only paid, booked visitor access, so it does
not clear hard rule 10 this pass. Five to six passes over the same ground
have now found everything the City Botanic Gardens/Eagle Street, Newstead
and Toowong clusters have to give; the 558-point significant-landscape-tree
overlay remains unusable without names or species. Do not re-run this hunt
without a reader submission or a genuinely new source.

## 2026-09-09 - Alicante's register radius is exhausted

A verify pass re-checked all 44 candidates in the Valencia region register
within 4.4km of Alicante's centre (up from 23 rows checked on 2026-09-07,
same conclusion). Every one is already published (16 trees), folded into a
documented grove (Portal de Elche fig grove, Pintor Aparicio olive/euphorbia
group), held as a lead with a specific reason (unresolved access, single
source, an avenue rather than a collectible point), or blocked (a private
Parque el Botanico trunk, a felled-elm cluster). Zero new trees deliverable
from this register without a non-register source (local news survey, a
second walking brochure, reader submissions). Do not re-run this hunt.

## 2026-09-10 - Photo lanes measured empty, and two famous trees with no photograph

Recorded after three rounds of photo passes over two days so no later window
goes back to them.

**Exhausted on Commons, confirmed by repeat passes.** Frankfurt's Palmengarten
returned glasshouse interiors, ferns and pond views on THREE separate passes;
both its copper beeches keep an honest gap. Helsinki's Kaisaniemi botanic
garden and Hamburg do the same, as does Craigends, whose yew grove holds only
understorey and moss-tangle shots. Cordoba's Patio de los Naranjos returns the
Mezquita's arcade. Nuremberg's Kontumazgarten returns its benches and paths.

**Two famous trees have no usable photograph there at all.** The **Ankerwycke
Yew** at Runnymede: two bole-only frames, one of which says so in its own
title, and a distant winter waterside view. The **Castagno dei Cento Cavalli**
at Sant'Alfio: its best-known image on Commons is an eighteenth-century Houel
painting, and the only other frames are a burr close-up and a low-resolution
under-canopy view. Both need a new source or a reader, not another sweep.

**Where photographs DO come from, measured across the three rounds.** Places we
publish for a single named, protected veteran. One pass counted it exactly: 13
of its 16 approvals came from those, 3 of 12 from big-city parks, and none at
all from Rome or Paris. Such a tree is photographed whole, in daylight, by
somebody who came for it, and it carries its own evidence into the frame: a
Naturdenkmal sign, a pomnik plaque, a shimenawa, a natural-monument stele, or a
register number in the filename.

**Two identity questions answered rather than obeyed, both raised twice.**
Nuremberg's two Hallerwiese planes are NOT mislabelled: the city's own 2020
Naturdenkmal ordinance records two planes there as ND-3, and the lime the sweep
keeps finding is our own nbg_001 on the same lawn, which already carries a
photograph from the identical series. And Higashiomi's Minamihanazawa hananoki
is alive: the photograph shows vigorous regrowth around a tarpaulin-wrapped
stump, which is what our first sentence already says. Both are recorded in the
trees' verify_notes.

## 2026-09-09 - Photo pass over the named candidates, and three trees called Kabouterboom

A sweep and a viewing pass over the candidates whose Commons FILENAME names
the tree, rather than over the zero-photo cities, which is where the yield
turned out to be. Recorded so the next pass starts from the findings rather
than the pile.

**The Hague's Kabouterboom is not the famous one.** The two RCE photographs
the sweep offered for hag_005 are captioned "de Kabouterboom, een tamme
kastanje en de dikste boom van Nederland", and the interpretation sign in
frame reads Geldersch Landschap en Kasteelen: that is the sweet chestnut
near Rozendaal in Gelderland, not our Pedunculate Oak in Haagse Hout. A
third candidate was a Kabouterboom in Nijmegen. Three trees carry the name,
ours is the least known of them, and it is a candidate for a recognition
line for exactly that reason (rung 7).

**Valencia vlc_014 and Milan mil_018 are held, not rejected.** Both are good
photographs whose subject cannot be tied to our trunk: the Glorieta holds
three catalogued Ficus macrophylla and neither file says which, and Milan's
plane sits 70 m from the pin with three other named planes within 300 m.
Either becomes approvable the moment anything names the trunk.

**One file offered to several trees, for the third time.** A Miramare
castle photograph reached tri_001, tri_002 and tri_003; an iNaturalist
observation reached both Ottawa lindens; a Genoa villa file was downloaded
four times for four trees and matched the species of none. That is now a
filter in `photo_fetch.py` rather than a note.

**What the loose matching drags in, so nobody re-judges it:** a church named
after an olive tree (Guimaraes, and it scored highest of the whole batch),
butterflies whose French names contain oak and birch (Brussels), a family
grave for "Ciechomski's Pear" (Warsaw), a Suffolk cottage named Sideways
(Setubal), and the right species on the wrong continent again and again:
Valencia's Kashmir cypresses are in San Diego, Oxford's mulberry is in
Tallinn, Paris's Anne Frank chestnut pulled saplings from three countries.

## 2026-09-08 (continuation) - Photo hunt exhausted for 24 trees: Alkmaar, Apeldoorn, Assen, Bangkok, Deventer, Dordrecht, Emmen, Haarlem, Maastricht

`photo_fetch.py` plus a viewing pass looked at every Commons candidate the
sweep could find for alk_005, apd_002, apd_008, ass_001, ass_002, ass_004,
ass_007, dev_003, dev_006, dor_001, dor_004, dor_010, dor_011, emm_001,
emm_005, emm_008, haa_005, haa_007, haa_008, maa_007, maa_012, maa_013 and
maa_014 (23 trees, plus bkk_003 held rather than exhausted). None had a
usable photograph: the pool was almost entirely archival black-and-white
material, street/house facades matched on address rather than tree, and
wide park or estate views with no single tree as the subject. All recorded
in `data/photo-queue.json` as rejected/exhausted, not to be re-hunted on
the Commons sweep alone; they need a reader submission or a genuinely new
source. **bkk_003, The Bodhi Tree of Wat Phra Kaew**, is `held`: a good
daylight photograph of the right species, but its geotag sits 60m from our
pin and its setting does not match "beside Prasat Phra Thep Bidon", so it
needs a second look before it can be trusted to be the same tree.

Also confirmed: the fetch sweep's filename-matching can attach one file to
several different trees sharing a place name (an Overcingel gate photo
queued against 3 Assen trees, a 1925 reburial photo against 2 Maastricht
trees) and can cross municipality lines on a shared street name (2 Deventer
candidates were actually in Olst). Worth fixing in `photo_gaps.py`'s
matching logic at some point; not attempted this pass.

## 2026-09-08 (continuation, previous attempt stopped after 50 min with 70 min unspent) - 13 bomenbieb.nl trees merged and committed: 5 new Dutch places, 8 folded into published cities

Picked up an uncommitted verify+write pass left on disk by the previous
attempt in this window, claimed as `_bomenbieb-netherlands` verify. All
13 trees were already fully researched and written (`data/research/
bomenbiebnetherlands-verified.json`), the leads file already marked
each one delivered; nothing had been committed, built or QA'd. Ran
`preflight.py` (0 problems), `astro build` (5130 pages) and `qa.py`
(8026 pages) clean, then committed.

**5 new single-tree places**, all bomenbieb.nl plus the national
register (LRMB) as the second source:
- **Borculo**: The Elm of Heure, European White Elm, ~175-195yr.
- **Giethoorn** (Dwarsgracht hamlet): The Ash of Dwarsgracht, European
  Ash, ~195-215yr, roots have raised the farmhouse De Essenbelt.
- **Harderwijk**: The Linnaeus Ginkgo, Ginkgo, 270+yr, unconfirmed
  local tradition ties it to Linnaeus's 1735 studies there.
- **Heinkenszand**: The Weeping Beech, Fagus sylvatica 'Pendula',
  ~155-165yr.
- **Oostkapelle**: The Lime of Kasteel Westhove, age disputed between
  two sources (1000-1400 signage vs a post-16th-century replanting),
  stated honestly as unproven rather than picked.

**8 trees folded into published cities**: Rhenen (rhe_002, Lime of
Achterberg, ~350-400yr), Arnhem (arn_039, Yew of Brantsenpark,
~300-400yr, also given a Dutch i18n overlay), Groningen (gro_021, Oak
of the Hunenborg, approximate pin, standing beside a hunebed), Utrecht
(utr_034, Dike Lime of Tull en 't Waal, ~225-275yr), Assen (ass_010,
Thick Oak of Beilen, ~250-350yr), Deventer (dev_011 Tree of Heaven of
Lunetteplein ~135-145yr, dev_012 Marshaven Poplar ~115-125yr), Emmen
(emm_008, Variegated Maple of Coevorden Castle, ~135-145yr).

All 13 flagged (single-sourced-plus-register rather than two fully
independent narrative sources), all photos missing, honest gaps. The
leads file (`data/leads/_bomenbieb-netherlands.json`) also picked up
several access/species notes from re-checking LRMB against bomenbieb
entries that stayed leads: a plane at Oldenaller blocked on the
register's own `visitable: nee`, an espalier pear cluster at
Grubbenvorst now understood as three register trees rather than one,
and an Amsterdam olifantsiep-adjacent tree still stuck on one source
after a second ArcGIS attempt failed to find a queryable endpoint.

**Separately noticed, not fixed this pass**: `data/city-list.json` has
no entries at all for Assen or Rhenen, despite both cities having been
live for a while (assen.json, rhenen.json existed before this
session). Their tree counts there were never tracked. Left as a gap
for whichever pass next touches that file's generation, since fixing
it meant guessing whether other cities are missing too and this pass
had no time budget for that audit.

## 2026-09-08 (continuation, previous attempt stopped after 17 min with 103 min unspent) - Radomsko, Stokaičiai, Pajūris opened; a coordinate copy-error caught before it shipped

Picked up per the standing instruction: two earlier attempts in this window
had claimed `_famous-japan` (write), `_famous-lithuania` (write) and
`_famous-poland` (verify) and left completed-but-uncommitted work on disk.
Merged and released `_famous-japan` first (4 single-tree places:
Aizuwakamatsu, Iida, Kitakata, Oyodo), then `_famous-poland`'s verify
output (1 tree, rad_001).

Dispatched a write pass on the remaining READY leads across cities (2
Lithuania, 1 Poland, 1 Utrecht):

- **Radomsko** (Poland, 1 tree, flagged: 0): The Insurgents' Linden,
  three limes planted 1863 on the grave of three killed insurgents,
  fused into one trunk, 5.33m round, extensive 2021-2022 conservation
  surgery.
- **Stokaičiai** (Lithuania, 1 tree, flagged: 1): The Visbarai Pine,
  single-sourced, no age.
- **Pajūris** (Lithuania, 1 tree, flagged: 1): The Akmenynė Oak,
  single-sourced (a second source confirms existence but not
  measurements), no age.
- **Utrecht's "Peer" lead was a duplicate, not a new tree.** Its
  coordinate (52.08586, 5.12903) was an exact copy of utr_018's own
  coordinate, a transcription bug caught by passcheck.py's duplicate
  detector before anything shipped. The register's real row for that
  entry (LRMB nr 1678119) gives 52.086488, 5.118036, which turned out
  to be the ALREADY-PUBLISHED utr_031 (The Old Pear of the
  Geertebolwerk). Folded its species (tightened to the canonical
  "European Pear (Pyrus communis)") and measurements (girth_cm 182,
  height_m 11) into utr_031 instead of shipping a second page for one
  tree. Fixed the coordinate in the source lead file too.

All three new places carry full page copy (intro, meta, FAQ) per
Contracts B/C. `city_names.py` run for all three; Stokaičiai's own
match resolved to the containing district rather than the village and
was moved to `unresolved_names` rather than shipped as a wrong alias.
`preflight.py` (556 cities, 0 problems), `astro build` (5090 pages) and
`qa.py` (7959 pages) all clean.

**Also fixed, rung 2:** `ios.yml`'s scheduled iOS-18-floor job has
failed since this morning on a false-positive tap-target FAIL
(`Button 'mytrees-who'` 62 by 14) that a 2026-09-06 fix (an identifier
plus `.accessibilityElement(children: .contain)`) only closed on iOS 26,
not iOS 18. Nothing reads that identifier, so removed it and the now-
unneeded `.contain` rather than trading one false positive for another.
Could not build or run a simulator in this sandbox (Linux, no Xcode);
the scheduled job will confirm. Vendored the one photograph the session
brief flagged as not yet on our own domain (utr_015). Recorded
REVIEW.md's 2026-09-08 superlatives.py WARN as answered (already fixed
in `bfaa50f3` by an earlier attempt this window).

**Verified and wrote up Sweden** (rung 0c, `famous_demand.py --next`):
9 candidates, 3 shipped (Ekerö/Ekebyhovseken, Sweden's largest
deciduous tree by volume, two sources' girth figures both stated
honestly rather than picked; Trollskogen/Trolleken, Öland's oldest oak,
no girth or height found so left absent; Sjukhuseken added to
Stockholm as sto_006, honestly framed as a declining hollow veteran
rather than a pristine specimen), 2 confirmed dead and blocked
(Hagstaeken Huddinge, felled Dec 2025; Lojstaeken, dead since 2001), 4
held for a follow-up pass (genuine designated monuments, one source
each so far). Also fixed Stockholm's intro, stale at "the four" since
before this pass. `preflight.py` (558 cities, 0 problems), `astro
build` (5106 pages) and `qa.py` (7976 pages) all clean.

## 2026-09-08 (continuation 5) - Two new Lithuanian places from a stranded write pass: Vytogala and Pagramantis Regional Park

Merged completed-but-uncommitted work from an earlier attempt in this
window: a `_famous-lithuania` write pass (data/research/famouslithuania-verified.json,
5 trees, full stories) that had been assembled into two new city files
but never committed.

- **Vytogala** (1 tree, single-famous-tree exception): the Vytogala
  Independence Oaks, four oaks around a memorial stone on the birthplace
  of Stasys Girenas, who flew the Lituanica across the Atlantic in 1933.
  Three planted in 1928 for the tenth anniversary of Lithuanian
  independence, the fourth a 1989 replacement. Two sources, girth
  recorded for two of the four, no photo.
- **Pagramantis Regional Park** (4 trees): the Gudlaukis oak (6.30m
  round, hollow, ~600 years by local tradition), the Geniai oak (5.6 to
  5.8m, undated, largest healthy oak in the register pair), the
  Tamosaiciai cemetery oak (4.3m, undated) and the Andriejaiciai oak
  (5m, 300+ years by local tradition, old crosses at its foot). All four
  are Lithuanian state-protected natural heritage objects, listed
  February 2016. No photos.

All 5 trees carry age gaps left honest (local-tradition estimates
stated as such, or left empty with a reader question) rather than
invented, per the estimate-vs-invention rule. `preflight.py` (0
problems), `astro build` (5078 pages) and `qa.py` (7903 pages) all
clean. Also fixed a `lastmod.py` bug found earlier this session: the
translated-tree hash was including fields (`how_to_recognise`,
`curation_status`, `submitted_by`) that `TranslatedTreePage.astro`
never reads, so an English-only edit to one of those fields restamped
every language variant's sitemap entry though nothing translated had
changed; re-derived `data/lastmod.json` against the fix.

Released the `_famous-lithuania` claim. ~30 scattered single-oak leads
from the same batch remain unresearched for a future pass. Nothing
flagged for Hidde.

## 2026-09-08 (continuation 4) - _famous-slovakia refilled, one new place, one live page corrected

Two more parallel verify passes, this time on `_famous-slovakia`. Batch A
delivered 4 candidates; batch B delivered 0 (3 confirmed avenues/rows,
now blocked as non-collectible-points, one genuine pear tree that failed
the single-tree-destination test, kept as a lead).

The write pass then found 3 of batch A's 4 were **already published**:
the Bosaca apple and pear (bsa_001, bsa_002) and the Velke Borove pine
(vbo_001) all exist in data/cities already, under names close enough
that the lead file's own duplicate-name matching missed them (the pear's
lead was "Pink pear from Bosaca", the live tree is "The Pink Pear of
Zabudisova"). `passcheck.py --pending` caught it before any duplicate
prose was written; no harm done beyond the verify pass's own tokens.

Only Komjatice's plane tree was genuinely new. Published as komjatice.json
(kom_001): Slovakia's most commonly cited thickest trunk (930cm, though
the story says plainly that Myjava's hollow lime measures wider), Tree
of the Year 2012, European Tree of the Year top-5 in 2013.

**The duplicate-work near-miss paid for itself**: the verify pass fetched
pravda.sk and teraz.sk directly for the Bosaca pear and got "about 200
years" from both, independently confirming a figure the live page had
explicitly left open as unverifiable ("those articles are no longer
reachable"). That also flips which of Bosaca's two trees is older (the
pear at ~200y, not the apple at ~130y), so corrected bsa_002's age fields
and story, and every city-level field on bosaca.json that named the old
answer: intro, meta_description, question_meta/answer/context,
oldest_tree_id, and two FAQ entries. This is rung-3 work (something
published being imprecise), found as a byproduct of rung-4 work.

Preflight and the Astro build both clean after all of it.
<!-- archive-index -->
## 2026-09-08 (continuation 3) - 8 new single-tree French places from the famous-trees batch

Refilled the shelf with two verify passes on `_famous-france`'s remaining
unsourced leads (batch A: 5 candidates, batch B: 4 candidates, run in
parallel), then a write pass on the 8 that verified. All 8 are standalone
rural French trees, none part of a city cluster, each judged against the
single-famous-tree-destination test in its own `verify_notes`.

Published as 8 new city files, one tree each: Magescq (Chene de Nerthe,
mgs_001), Nicorps (If commun de Nicorps, nic_001), Jauze (If de Jauze,
jau_001), Pesselieres (Le Sully de Pesselieres, pes_001), Feternes (Tilleul
de Chateauvieux, fet_001), Bracon (Tilleul de Grange Sauvaget, bra_001),
Reaumont (Tilleul de Reaumont, rea_001), Chatenay-Malabry (Cedre pleureur
de la Vallee-aux-Loups, cma_001). Tilleul de Joux blocked instead (private
chateau grounds, no evidence of routine public access); both verify passes
reached that verdict independently.

Fixed two writer-side issues before merging: a species-name collision
(both yews delivered as "Common Yew", the site's existing convention is
"European Yew") and an over-60-char tree-page title (Bracon's tree name
carried a redundant French-name parenthetical). Ran `city_names.py` for
search aliases afterward and it produced one wrong one: "bracon" ->
"Arbois", the exact proximity-matching failure its own docstring warns
about (Bracon and Arbois are distinct Jura communes 7.4km apart, not the
same place under two names). Removed that entry from both `search_names`
and `wikipedia_titles`; kept the other 4 (chatenay-malabry, feternes,
magescq, reaumont), which look like genuine local-language spellings of
the same place.

Also, separately: a viewing pass on the Commons photo sweep gave 4 more
single-tree pages (previously photo-less) their first photograph -
Allouville-Bellefosse's Chene Chapelle, Aberford's Nellie's Tree, Aguas de
Moura's Whistler Cork Oak (the 2018 European Tree of the Year) and
Albersdorf's Funffingerlinde - plus the Oak of Hersberg in Altrier. 12
mismatched candidates rejected (wrong commune, a trail sign, generic
village/castle shots, Helmond's two candidates 600m+ from the pins).

And rung 1: 3 reader photographs of Baarn's Cantonspark Giant Sequoia held
rather than approved (matched by distance only; the reader's own
"Watercypres" label and the foliage in all three point to the Dawn Redwood
128m away instead), 2 leads turned out to be indoor test shots through a
window, and a striking unidentified multi-stemmed tree by a stream in Nara
kept as a lead for a verify pass.

## 2026-09-08 (continuation 2) - 40 recognition lines across 8 cities, worst-first by impressions

Week still had headroom, so continued past the Sant'Alfio work. New coverage
was thin everywhere checked: `city_queue.py --next`'s OPENABLE cities mostly
carry 1-2 Wikidata leads each, well under a single verify pass's 6-candidate
floor, and Florida's champion-tree register (the only one covering Daytona
Beach, scout_next.py's suggested target) was already fully scouted and
recorded as a dead end for exactly this reason in an earlier Jacksonville
pass. Rather than force a thin pass, moved to rung 7: `recognise.py --stuck`
(270 trees with no photo, no recognition line, and a government-designated
neighbour within 25m).

Wrote and applied 40 lines, worst-first by search impressions: Lisbon (2),
Barcelona (6), Singapore (7), Vienna (6), Leiden (11), Paris (3), Florence
(4), Prague (1). All restatement from each tree's own story and verify
data per BRIEF_WRITING.md's rule (species, girth, height, setting, what
already distinguishes it from its stuck neighbour), nothing new claimed.
Several pairs needed the "which one" answer directly: Leiden's two Siebold
zelkovas (single-trunk vs five-stemmed), Vienna's oak and yew twelve
metres apart at Schönbrunn (deciduous vs evergreen), the two Bobolino
cedars in Florence (cedar of Lebanon vs the horned incense cedar).
`recognise.py --stuck` backlog: 270 to 230.

**Also fixed a real fabrication risk in `leads.py`**: four Nara trees
retired the same day they were published (zero verified sources, see the
prior continuation's brief) were showing up as READY again within the
hour, because their own `why` field IS the retirement note and
`has_source_evidence()` read its mere presence as proof a pass had
looked at the tree. Added a `retired_id` check to `classify()` so a
retired lead short-circuits straight to BLOCKED. Also cleared two stale,
fully-consumed verify-pass leftovers (`famousslovakia-verified.json`,
`famoustaiwan-verified.json`) sitting uncommitted since the prior
continuation.

Build (5023 pages), qa.py (7779 pages) and preflight.py (536 cities, 0
problems) all clean. No FOR HIDDE items.
## 2026-09-08 (continuation) - Sant'Alfio grows from 1 tree to 3: the two chestnut/birch neighbours that had no home

Continuation of an attempt that stopped after 34 minutes with 86 of its
window unspent. No claims standing, `leads.py --ready` empty. Deleted
two stale, already-consumed research files sitting uncommitted from the
prior attempt: `famousslovakia-verified.json` (all 5 trees confirmed
live under bosaca/senica/stary-smokovec/velke-borove) and
`famoustaiwan-verified.json` (an empty array, its one candidate already
shipped as bilu.json weeks ago).

Then `city_queue.py --next` and `scout_next.py --target` for new
coverage; Taormina's own register supply is exhausted (all five in-town
trees blocked on the Excelsior Palace's private grounds, per
`data/leads/taormina.json`). But `data/leads/santalfio-etna.json` held
two more fully-verified trees, from the same 2026-08-30 pass that had
already shipped the Hundred-Horse Chestnut alone under the single-tree
exception, explicitly left for later ("A Sant'Alfio page of its own
once four trees clear the bar on that slope; these three are already
three of them"). Wrote their stories and added them to santalfio.json:

- **sal_002, The Ship's Chestnut** (Castagno della Nave): ~1,800 years
  by one source, a second only confirms "over a thousand"; 500m uphill
  from the Hundred-Horse Chestnut. Stands on private land but at the
  path's edge, described by the source as clearly visible without
  entering the property, the view-only-tree allowance. Flagged for the
  age and the access read.
- **sal_003, The Etna Birch of Magazzeni** (Betula aetnensis): a
  glacial-relict endemic growing at 1010m, well below its usual
  1450-2000m band. No age source exists, so the field stays empty and
  the story asks the reader rather than guess. Girth (205cm) and
  height (12m) corroborated across the national and a regional
  register. Flagged: no source confirms a marked path to this specific
  tree, though it stands in open forest with no gate.

Both carry a `how_to_recognise` line (bark colour/base shape are
restatements of verify_notes, not new claims). Rewrote the city intro
to reflect three trees instead of one, kept within the 60-100 word
Contract C range. Still below the 4-tree floor at 3, which is fine:
the page already shipped under the single-tree exception and growing
it with genuinely verified neighbours is normal work, not padding.

Build (5023 pages), qa.py (7779 pages) and preflight.py (536 cities,
0 problems) all clean. No FOR HIDDE items.
## 2026-09-08 - Finished the standing _famous-slovakia and _famous-taiwan claims; a stranded Poland write also merged

Continuation of an earlier attempt that stopped after 10 min with 110 of
its window unspent. `passcheck.py --claims` showed two standing,
`_famous-taiwan` and `_famous-slovakia`, both verify, with uncommitted
output already on disk. `famoustaiwan-verified.json` was an empty array:
that pass's one candidate, the Bilu Sacred Tree, had already shipped as
bilu.json in an earlier commit, so the claim was pure orientation cost.
Released it. `famousslovakia-verified.json` held 5 fully verified trees
with no story; `passcheck.py --pending` also surfaced a fully-written but
unmerged `famouspoland-verified.json` (3 trees) from an even earlier
session.

**5 new single-tree/small-cluster Slovak places, all under the
2026-08-31 single-tree-destination exception (national Strom roka
contest wins standing in for global fame, per the Amt Neuhaus
precedent):**
- **Bošáca** (new, bsa_001/bsa_002): two national Tree of the Year
  fruit trees 350m apart in the Zabudišová hillside hamlet, an heirloom
  apple (2017 winner, 6th in Europe) and a rare pink-fleshed pear (2015
  winner, 3rd in Europe). Reassigned from the verify pass's `bsc_001`/
  `bsc_002` ids, which collided with live Bucaco (Portugal) trees;
  `passcheck.py --pending` caught it before merge.
- **Veľké Borové** (new, vbo_001): Slovakia's first-ever Tree of the
  Year (2004), a Scots pine estimated 250-350 years old. Flagged: no
  dated sighting since a geocache route to it was archived in 2014, so
  the page says plainly that its current status is unconfirmed rather
  than assume the best.
- **Starý Smokovec** (new, sms_001): the Smokovec Beech, "Tree of
  Lovers," a weeping beech (~80 years) in the centre of the High Tatras'
  main resort town, 2021 Tree of the Year.
- **Senica** (new, sen_001): the White Mulberry of Senica, ~210 years,
  the town's own Tree of the City (2010) and national Tree of the Year
  (2014), 8th of 14 in the 2015 European final.

**Brzoza, Poland (new, brp_001/002/003):** an oak and two limes standing
within 15m of each other in state forest north of Toruń, all made nature
monuments in one 2014 council resolution. Renumbered from the verify
pass's placeholder `xxx_003/004/005` ids. None of the three carries a
documented age; two of three rest on a single source and are flagged.
Ships below the 4-tree floor as a genuine below-floor cluster rather than
one tree, per the exception's "local documentation, not global fame"
standard.

`city_names.py` run for the 4 new Slovak places (Brzoza's own name is a
common Polish toponym and could not be resolved to one Wikipedia article;
left unresolved rather than guessed). Build (5021 pages), qa.py (7777
pages, 0 problems) and preflight.py (536 cities, 0 problems) all clean.
Deleted 3 stale `data/research/*-verified.json` files whose contents were
already fully merged (bilu, brisbane, famouspoland).

## 2026-09-07 (continuation 9) - Finished the _bomenbieb-netherlands and _famous-germany claims

**Maastricht +1 (maa_015), Deventer +1 (dev_010), Tilburg +1 (til_016).**
Three bomenbieb.nl leads (Meerssen tulip tree, Wilp trumpet tree,
Oisterwijk's Marialinde) were fully verified and written but sat
unmerged; `passcheck.py --brief` placed all three inside an existing
city's radius rather than as new places.

**16 new German single-tree places from `_famous-germany`.** hmb_001
(Himmelsberg, a lime trained into a dance floor, on a 2001 postage
stamp) and lnd_001 (Linderhof, spared by Ludwig II for the terrace
gardens) were already fully verified with no story. The remaining 26
leads on that file (all `status: lead`) went to a `verify` pass: 14
shipped as new single-tree places (bargischow, horn-bremen, eichigt,
niedenstein, neuenrade, peesten, frankenthal-sachsen, polchow,
schlettau, wilparting, baldenhain, limmersdorf, neudrossenfeld,
ottendorf-gaedheim), 10 held as real-but-ordinary Dorflinden/
Gerichtslinden, 2 blocked as dead (Kandelaberlinde Dorla, felled 2023;
Winterlinde am Friedhof Eschelbronn, felled 2019, caught from a stray
`tmp_eschelbronn.txt` an earlier attempt had fetched and never
processed). Every one of the file's 53 leads now carries a status;
none are left as a bare `lead`.

## 2026-09-07 (continuation 7) - Leiden 18 to 20: two Hortus trees a prior write pass left unmerged

`leiden-lrmb-written.json` carried 8 written trees; the prior continuation
merged 6 (12 to 18) and left lei_012 (Fern-leaved Beech of the Nut Field)
and lei_013 (Grafted Ash of the Hortus) on disk. Both were fully verified
and written, needed only merging, `paid_entry: true` (missing, caught by
preflight against their Hortus siblings) and count-line fixes (eighteen to
twenty, eight to ten, English and Dutch). Leiden: 18 to 20 trees, both new
ones paid Hortus entries (paid-entry share unchanged at 50%). Deleted both
now-empty research files. Build, qa.py and preflight clean.

## 2026-09-07 (continuation 6) - Leiden 12 to 18: 6 free trees from the Dutch LRMB register

Same window as the Berlin and Milan passes below, after both came back
thin. Checked `city_queue.py --next`'s stage-2 deepening list for a
better-quality register than Berlin's (no age field) or Milan's
(near-centre supply exhausted): Leiden's Dutch LRMB register carries a
planted-decade band directly on every entry and had 399 unmined
candidates within 20km. Dispatched a verify pass, deliberately steered
toward free public trees since Leiden already sat at a high paid-entry
share (8 of 12, 67%).

**6 trees shipped, all free**: two London Planes and a weeping willow
clustered around the Van der Werff statue in Van der Werfpark, a
Caucasian wingnut in the Plantsoen that won a public "X-factor" tree
election in 2009 (160 votes to a copper beech's 83), a 3-tree Persian
Ironwood ensemble in the same park that turns out to be the actual type
planting for the cultivar Parrotia persica 'Het Plantsoen', now sold by
nurseries across Europe, and an elm inside the 11th-century Burcht
mound, one of the country's surviving monumental elms amid the ongoing
Dutch elm disease die-off. 2 blocked (a beech at a private townhouse, a
9-tree maple grove that fails the single-collectible-point test), 4 left
as leads. Wrote all 6 stories directly (single-city batch, judged too
small for a cross-city write pass) and their Dutch overlay translation,
since Leiden ships an nl page and the build refuses a translated city
missing trees the English page holds.

**One pin upgraded**: lei_005 (the Beets Beech of the Burcht) moved from
approximate to confirmed using the LRMB register's own tree-level
coordinate for the same tree, matched by name and place. Fixed five
stale "twelve trees" count promises across both languages (title, meta
description, intro, question page, FAQ) and trimmed both intros back
into Contract C's 60-100 word range after a first draft ran long.
Leiden: 18 trees, paid-entry share down from 67% to 44%. Build, QA,
preflight and superlatives all clean. Claim released.

## 2026-09-07 (continuation 5b) - Milan verify pass repeated: still 0, duplicated continuation 3's own finding

After Berlin's low yield, dispatched a Milan verify pass on the strength
of `city_queue.py --next` showing 25 register candidates and real room
to target (22 of 30). It came back with 0 trees, independently
re-confirming near-centre supply is exhausted: 17 already published, 3
already blocked, 3 already tracked as leads. Only afterwards did a check
of this file surface **continuation 3, earlier the same day, already
found and logged the identical result** ("Milan's near-centre register
supply is genuinely exhausted"). This is exactly the waste
`grep -ri "<place>" CURATION.md archive/` exists to prevent and this pass
skipped that check before dispatching. ~171k tokens for a
re-confirmation, partially offset by one real new attempt (RAMI lookup
on the Villa Litta ambiguity, still unresolved, documented in
`data/leads/milan.json` for whoever tries next with a browser session).
Claim released, logged.

## 2026-09-07 (continuation 5) - Berlin verify pass: 561 register candidates, 1 shipped (ber_020)

Continued a window a still earlier attempt had stopped after 15 minutes
having shipped 0 trees, with 105 of 120 minutes unspent.
`passcheck.py --claims` showed a standing Berlin verify claim (589
Naturdenkmal register candidates within 20km, 561 unmined, plus 284
Wikidata candidates). Dispatched a verify pass to finish it rather than
re-claim or abandon it.

Yield was low and the reason is a genuine register gap, not an unworked
city: `berlin-naturdenkmale.json` carries no age or girth field at all,
and for nearly every unmined candidate the only apparent "second source"
was de.wikipedia's district Naturdenkmal list, which traces to the same
government ordinance as the register itself (confirmed by exact
coordinate matching), so per this project's own established precedent it
does not count as independent. monumentaltrees.com, which resolved most
of Berlin's earlier leads, 403'd throughout with no usable Wayback
snapshots.

**1 tree shipped: ber_020, the Podbielski Oak**, the only tree standing
anywhere on the Olympiastadion's 810x320m grounds, named in 1914 for
Prussian cavalry general Victor von Podbielski. Two independent sources
disagree on its history: de.wikipedia implies continuity from a
~200-year-old original, golocal.de says the 1913 original was felled with
the old Deutsches Stadion and a replacement planted in 1936 (~90 years).
Delivered flagged, both readings stated rather than a winner picked, per
the Dicke Marie precedent already on this city's own page. Species also
carries an unresolved minor conflict (register says Quercus petraea, a
Commons photo filename suggests Quercus robur), noted but not resolved.
Wrote the story myself (1 tree, below the threshold for a write-stories
batch) and its German overlay translation (`data/i18n/de/berlin.json`,
title count 19 to 20 Naturdenkmäler). Berlin now 20 trees, 12 with photos.

7 clusters recorded as new open leads in `data/leads/berlin.json`
(Johannaplatz yews, Wallotstrasse/Königsallee beeches, a 13-tree Tiergarten
exotic cluster, a TU Berlin arboretum, a Dahlem churchyard lime, Grunewald
forest oaks, Heinrich-von-Kleist-Park), none confirmed dead ends, each
missing either an independent source or an access confirmation. Claim
released. Build, QA and preflight all clean.

## 2026-09-07 (continuation 4) - Prague write pass merged (+3); Nara reader sightings closed out (+4), 11 submissions answered

Resumed a window a still earlier attempt had stopped after 57 minutes
having shipped 5 trees elsewhere, with 63 of 120 minutes unspent.
`passcheck.py --claims` showed a standing Prague verify claim with real
output on disk (`data/research/prague-verified.json`, 3 trees fully
verified, no story yet). Dispatched a write-stories pass on those 3
(prg_019 Hungarian Oak of Italska Street, prg_020 Oak of U Malvazinky,
prg_021 Plane of Jezerka Park), merged into `data/cities/prague.json`
(18 to 21), fixed 3 stale count promises in the page copy (eighteen to
twenty-one, sixteen more to twenty more, four planes to six), and one in
`data/countries/czech-republic.json` (49 to 52 trees). Claim released.

**11 unprocessed reader submissions were sitting in Supabase, all from
this morning, all Hidde walking Nara with the app's "add a tree" camera
flow.** A still-earlier continuation (see below) had already fetched and
matched the 8 that carried photographs via `sightings_inbox.py`, filing
them to `data/leads/_sightings.json`, but had dispatched a background
research agent to identify them that never delivered: the session that
started it ended first, the same Nara-loss pattern as 2026-08-03. Nothing
had reached `data/research/`.

Looked at all 8 photographs directly. Two ("I'm not sure which one it
is") turned out to be the same Roben-sugi already published as nra_010,
photographed seconds apart from the shot already approved as its page
photo, not a new tree. The remaining 4 distinct trees (one cedar beside a
small shrine near Nigatsu-do, a leaning cedar by the approach road, a
broad tree by a park pond and pavilion, and a large ginkgo beside a
temple wall in Suimon-cho, the last shot three times) went to a fresh
verify pass with the photos, GPS and visual descriptions as the brief.

**None of the four cleared the two-independent-source bar**: web and
Japanese-language searches (municipal giant-tree lists, temple pages,
OSM/Overpass reverse geocoding) found no named, individually documented
tree at any of the four spots, only the photograph itself as evidence.
Per Step 2 ("if sources conflict or only one source exists, include the
tree but flag it"), published all four rather than leaving them in
research limbo: nra_011 through nra_014, all `curation_status: flagged`,
`location_precision: approximate`, no invented age, girth or name beyond
a descriptive one, species left honestly uncertain on nra_013 and access
phrased as view-only on nra_014 (temple ownership of the wall unclear).
Each story ends by inviting the reader to name the exact spot. A
title-length build break on nra_014's first-draft name (65 chars) was
caught by the build and fixed before merging (renamed to fit under 60).
Nara's meta_description count promise fixed (nine more to thirteen).

Closed the loop on all 11 submissions via the service key: outcome set
on each (`changed` for the 4 new trees and the first of the 3 ginkgo
duplicates, `holds` with a composed reply for the 2 Roben-sugi
duplicates and the other 2 ginkgo duplicates, `open_question` for one
sighting whose photo never uploaded, `holds` for a worth-it vote on
nra_005 and its undo). Custom replies checked clean against
`mailcheck.py` before writing them to the rows; `contributor_reply.py`'s
own scheduled run sends them. All 11 row ids appended to
`data/submissions-processed.json`. `data/leads/_sightings.json` updated
to `published`/`duplicate` with the resulting tree ids so a future pass
does not re-litigate them.

Build (4897 pages), qa.py, preflight.py (0 problems) and superlatives.py
(702 claims, no collisions) all clean. `city_queue.py` rerun to keep
`CITY_QUEUE.md`/`city-list.json` current. Nothing FOR HIDDE.

## 2026-09-07 (continuation 3) - Milan verify pass: 0 new (supply fully mined); Nara reader sightings processed, one photo held, deeper research dispatched

Resumed a window a still earlier, unlogged attempt had stopped after 48
minutes with 5 trees already shipped elsewhere and 72 of 120 minutes
unspent. `passcheck.py --claims` showed two standing claims from that
attempt, both verify passes claimed but never delivered: milan (empty
delivery file) and prague (delivery file present but empty, `[]`).
`leads.py --ready` had only the 1 Voorburg elm already known to be below
the no-pass-under-six floor. Dispatched verify agents on both claimed
cities per their passcheck briefs.

**Milan: 0 new trees, and it is a real answer, not a stall.** All 14
register candidates within reach of the walk were cross-matched against
the live city file, the leads file and the blocked list: every one
already published, already blocked (Villa Belgiojoso's children-only
garden), or the one known single-source lead (a 625cm Montanelli plane).
A fresh attempt to find a second source for that plane via RAMI
(ilregistrodeglialberi.it) traced the record's own AMI code back to a
*different*, already-published Milan plane, so it stays a lead. Milan's
near-centre register supply is genuinely exhausted; logged to
`data/agent-costs.json`, claim released.

**Reader sightings: Hidde walked Nara this morning and used the app's
own "add a tree" flow repeatedly.** `sightings_inbox.py` picked up 1
photo queued against an existing tree (a second photo of nra_010, the
Roben-sugi) and 6 fresh leads with no match in `data/cities`.
Downloaded every photo from the private bucket and looked at the pixels
before deciding anything, per the Cadiz standard:

- The second nra_010 photo shows a much thicker, deeply furrowed,
  steel-propped trunk than a photo of a ~60-year-old 1967 replacement
  tree would suggest, and it cannot be confirmed as the same specimen
  as the currently-approved photo without more evidence. Held rather
  than swapped in (`sightings_publish.py`, verdict recorded).
- Visual triage of the remaining leads found at least 3-4 genuinely
  distinct large trees Hidde photographed nowhere near each other
  (a large cedar by a small shrine ~99m from nra_010, another leaning
  cedar by a gravel road, and what looks like a row of large trees
  along a temple precinct wall near central Nara/Kofuku-ji), plus one
  distant meadow view too far to read. None are register candidates,
  so a normal verify pass cannot place them: dispatched a research
  agent with the photos and my visual notes to identify and verify
  what it can, deliver to
  `data/research/nara-sightings-verified.json`. Result not in yet.

Nothing committed to a city file yet; this entry covers the processing
so far. See the next entry(ies) for what the Prague and Nara passes
returned. Nothing FOR HIDDE.

## 2026-09-07 (continuation 2) - Merged a stranded write pass: Deventer +1, The Hague +1, Kasukabe and Aguas de Moura new (single-famous-tree), plus 2 photo approvals

A prior attempt in this same window had already claimed and finished a
write-stories pass on 5 targets (`the-hague`, `deventer`, `rumskulla`,
`kasukabe`, `aguas-de-moura`), and a photo-judge viewing pass on 18
photo-less cities, but stopped after 24 minutes without committing
either. `passcheck.py --claims` showed the 5 claims still standing
(133 min left); `git status` showed the actual finished output sitting
uncommitted: 2 new single-tree city files, 2 existing cities each +1
tree, and 2 approved photographs already vendored into
`data/cities/*.json`. Verified each city file (word counts, sources,
`location_precision`) before trusting it, ran `preflight.py` (0
problems) and a full `astro build` + `qa.py` (had to rebuild once,
because `vendor_photos.py` had written the two new photo files into
`site/public/photos` mid-build and the first build had already copied
`public/` before they landed; second build picked them up, QA passed
clean at 7488 pages).

- **Deventer +1** (dev_009): The White Willow of Wilp, from the
  Bomenbieb Netherlands register.
- **The Hague +1** (hag_033): The Wych Elm of Park Middenburg, same
  register.
- **Kasukabe, Japan** (new, ksk_001, single-famous-tree exception):
  Ushijima no Fuji, the Great Wisteria of Ushijima, Japan's only
  wisteria at Special National Natural Monument rank, roughly 1,200
  years old. The garden built around it opens only mid-April to
  early May.
- **Aguas de Moura, Portugal** (new, agm_001, single-famous-tree
  exception): the Whistler Cork Oak (Sobreiro Assobiador).
- **Rumskulla, Sweden** (new, rkm_001, single-famous-tree exception):
  Rumskullaeken, the Kvill Oak.
- Photo-judge viewing pass approved 2 of 47 candidates viewed as pixels:
  the Molkenkur linden in Heidelberg (hei_001, CC BY-SA 4.0) and the
  Olive of San Martin de Porres in Lima (lim_002, CC BY-SA 4.0, the
  city's longest-lived tree, previously photo-less).

Released all 5 claims after merging. `city_queue.py` re-run to fold the
two new cities into CITY_QUEUE.md and city-list.json (now 247 entries).
Nothing flagged for Hidde.

## 2026-09-07 (continuation) - Finished 4 stranded write-story passes: Pelham, Itoshiro, Yangpyeong ship; Osaka +1

An earlier attempt this window stopped after 14 minutes having shipped
nothing, with 106 of 120 minutes unspent. Checking claims and READY leads
(both empty of new work) turned up something more valuable sitting
uncommitted on disk from an even earlier, unrelated attempt: four fully
verified AND fully written trees (`data/research/comfort-maple-verified.json`,
`ginkgo-of-yongmunsa-temple-verified.json`, `itoshiro-no-osugi-verified.json`,
`myokokuji-no-sotetsu-verified.json`) that a write-stories pass had already
finished, never merged, never committed.

- **Pelham, Ontario, Canada** (new, pel_001): the Comfort Maple, widely
  reckoned Canada's oldest sugar maple and possibly Ontario's oldest tree
  of any species, with an entire conservation area built around it.
  Photo found and viewed against the Cadiz standard (full tree, autumn
  colour, well exposed, CC BY-SA 2.0, Flickr via Commons) and approved.
- **Itoshiro, Gifu, Japan** (new, ita_001): the Itoshiro Osugi, a
  ~1,800-year cedar and the only Special National Natural Monument tree
  in the prefecture, reached by 420 purpose-built steps. Photo viewed and
  approved (whole tree, daylight, the trailhead sign visibly confirms the
  age/girth figures used in the story).
- **Yangpyeong, South Korea** (new, ymp_001): the Ginkgo of Yongmunsa
  Temple, reckoned Korea's tallest ginkgo, Natural Monument No. 30. Photo
  viewed and approved (full crown in autumn gold, matching the best_time
  label exactly; KOGL Type 1, already precedented via Seoul's photos).
- **Osaka +6th tree** (osa_006): Myokoku-ji's cycad colony ("the Homesick
  Cycad") in neighbouring Sakai, 20-25 minutes by Nankai train from
  Namba, inside the day-trip boundary. Two photo candidates were viewed
  and both rejected (one a black-and-white archival print with a person
  in it, one a satellite/aerial map, neither a photograph of the plant
  itself), so it ships `photo.status: missing`. Updated Osaka's intro
  (which had also drifted stale: it said "three of the four" trees were
  camphors against an actual five, now corrected to "four of the six"),
  one FAQ answer, and the Japanese translation overlay (new osa_006
  entry, intro/FAQ text updated to match, trimmed to the 250-character
  Contract C limit for Japanese).

**famouspoland-verified.json (the Brzoza trio, xxx_003-005) got stories
too, but stays HELD.** Below the 4-tree floor with no evidence of the
wider fame the single-tree exception requires (a municipal legal
designation and a forest-district webpage, not a tourist destination).
Kept as finished research, not thrown away, for whenever a container
opens.

**Continued the standing `_bomenbieb-netherlands` verify claim** (a
`night-run` claim from a "shelf refill, next batch" pass, 146 minutes
left when picked up): the earlier attempt's followup file had only
gotten through 1 of its assigned 18. Before dispatching more research,
cross-checked all 17 remaining against the CURRENT full corpus by actual
coordinates rather than trusting the batch's own stale `nearest_ours`
field, and caught 2 that had already shipped under different names from
this same lead pile the day before (`zwarte els paleis loo` = apd_010,
`kasteellinden nijenrode` = bkl_001, both exact 0m coordinate matches),
now marked `duplicate` with the reason on record so nobody re-researches
them. Dispatched a verify agent on the remaining 15 (Voorburg, Amsterdam,
two in Wilp, Meerssen, Houten, Grubbenvorst, Oisterwijk, Achterberg, De
Steeg, Zutphen, Midlaren, Tull en 't Waal, Slochteren, Putten); result
not yet in as this entry is written.

Build (4878 pages), qa.py and superlatives.py (697 claims, no crown
collisions) all clean. Pushed as `ab570643`.

## 2026-09-07 - Finished the standing _famous-france and _famous-poland verify claims: 5 trees, 3 new single-tree places plus one into Ghisonaccia

Resumed into a window an earlier attempt had stopped 12 minutes in with 108
of 120 minutes unspent. `passcheck.py --claims` showed two standing verify
claims (`_famous-france`, `_famous-poland`, both by night-run) with real
uncommitted output on disk: `data/research/famousfrance-verified.json` (4
trees) and `famouspoland-verified.json` (5 trees), fully verified with
sources and coordinates but no stories, so `leads.py --ready` correctly
showed 0.

Filtered to what should actually become a page before dispatching a
write-stories pass, since two of the nine did not clear the bar: **the
Fontenay Abbey plane tree**, whose own verify_notes recommend against a
standalone page (a garden feature of an already-famous UNESCO abbey,
people travel for the abbey rather than the tree), and **the Brzoza
trio** (an oak and two limes near Torun, legally designated together but
with no evidence of the wider fame the 2026-08-31 single-tree exception
requires, only a municipal resolution and a forest-district webpage).
Both are kept as fully-verified research rather than discarded: Fontenay
back in `famousfrance-verified.json`, the Brzoza three in
`famouspoland-verified.json`, for whenever a container opens (a Marmagne
page with other trees; a Torun page; further evidence of fame).

The other five got stories from a write-stories pass and were assembled
into containers by hand:

- **U Listincu** joined the existing Ghisonaccia page as arb_002. Its own
  story already alluded to it ("the person who had already had
  Ghisonaccia's other old tree, a mastic reckoned at a thousand years,
  officially recognised"), so this closes a reference the page had been
  carrying unfulfilled. Ghisonaccia is now 2 trees; oldest_tree_id moved
  to arb_002 (700-1000 years vs arb_001's 200-250), intro/meta/question
  page/FAQ all rewritten for two trees.
- **Chene de Venon** (vno_001), a new single-tree place near Grenoble: a
  solitary "vegetation lighthouse" oak visible across the whole valley,
  French Arbre remarquable since 2017, ~100 people at its recognition
  ceremony. Genus left unresolved (Quercus sp.), publish-and-ask.
- **The Saman of Habitation Ceron** (lpr_001), a new place, Le Precheur,
  Martinique: the park's headline attraction, survived the 1902 Pelee
  eruption. Used the real commune name rather than the whole island,
  matching the Venon/Rogalin/Sant'Alfio precedent of precise village-level
  containers rather than a broad island page built for one tree. Country
  set to France (Martinique is an overseas department), matching how
  Corsica is treated. Its pin sits 6499km from the nearest other French
  tree, which is real geography (island vs mainland/Corsica), not a data
  error; added `lpr_001` to preflight's `CHECKED_BY_HAND` set alongside
  the existing Pirangi do Norte precedent.
- **Lech's Oak and Rus's Oak** (rog_001, rog_002), a new place, Rogalin,
  Poland: two of a legendary named trio (Lech, Czech, Rus) beside Rogalin
  Palace; Rus is dendrochronologically dated to 800-850 years (Institute
  of Dendrology, Kornik, 2019), the oldest dated oak in Poland, Lech has
  no dated age and the story says so plainly. The dead third oak, Czech,
  appears only as context, never as its own entry, per the never-dead-tree
  rule. Two distinct trees, two entries, not folded into one (unlike
  Breukelen's indistinguishable lime pair), since each has its own
  well-sourced, independent story.

All four leads files updated with `status: published` and the tree id, so
a future dedupe check reads them as done rather than re-litigating them
(confirmed via `preflight.py`'s own "may already be published" NOTE, which
now correctly flags all four against the new entries). Regenerated
city-list.json/CITY_QUEUE.md, full Astro build (7435 pages), qa.py clean,
preflight.py clean (0 problems after the CHECKED_BY_HAND fix),
superlatives.py clean (694 claims, no collisions). Released both claims.

Also checked rung 2 (site broken): the site itself is fully green (smoke,
deploy, digest, review). The iOS app gate is red, on its fourth
consecutive failed fix attempt for `testTappingAPinOpensItsTree` across
several hours of CI time by (presumably) other continuations; did not
duplicate that effort. REVIEW.md's two 2026-09-06 WARNs (business-rule
phrasing in three FAQ answers, a contradiction in Contribute.swift) were
both already fixed by an earlier pass; verified rather than re-fixed.

`passcheck.py --pending` also surfaced 7 other already-verified
single-tree files still needing only a story (Comfort Maple, Yongmunsa
ginkgo, Itoshiro no Osugi, Myokoku-ji sotetsu, Rumskullaeken, Ushijima no
Fuji, Whistler Cork Oak): bought and paid for, worth a write pass next.

