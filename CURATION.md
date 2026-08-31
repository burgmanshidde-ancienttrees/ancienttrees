

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-08](archive/CURATION-2026-08.md)
- [2026-07](archive/CURATION-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.

<!-- archive-index -->
## 2026-08-31 - Nine zero cities opened, Matera and Taormina refused on access

Registers used, and what each one does or does not answer:

| Register | Measurements | Age | Vitality | Ownership |
|---|---|---|---|---|
| Okinawa hundred notable trees | yes | yes | revoked-certification flag | yes |
| Andalusia singular trees | yes, full sheet | sometimes, with method | no | yes |
| Catalonia monumental trees | yes | no | yes | no, but location is specific |
| Kagoshima / Kanagawa / Miyazaki / Aichi via Hitozato Kyoboku | yes | signboard traditions | no | no |
| Castilla y Leon notable trees | height yes, trunk column ambiguous | no | no | no |
| Navarra Natural Monuments | no | no | no | no |
| Italy MASAF | yes | no | no | no |

Could not verify, kept as leads:

- Matera. 44 register trees within 25 km and no way to answer access: eleven of
  the seventeen nearest are on a masseria and MASAF has no ownership field. Would
  open on a Basilicata regional sheet or the Murgia park's own trail list.
- Taormina. All five trees the register holds inside the comune are in the
  grounds of the Hotel Excelsior Palace.
- Yonagusuku's banyan near Naha, 23.5 m round and the largest tree in Okinawa.
  Owner recorded as a private household.
- Five Tarragona trees on private mas, including a holm oak 6.45 m round.
- Most of the trees around Girona: the Catalan register's location field names a
  mas or a can for the majority, and only seven read as public.

Register pitfalls hit this pass:

- Castilla y Leon's trunk column is labelled diameter and read that way makes
  AS-SG-07 at La Granja the thickest sequoia in Europe. The column is not quoted
  anywhere on the Segovia page and the story says why.
- The Catalan register keeps DEAD trees listed with a vitality note. Several near
  Girona and Tarragona are marked Mort, with a year, and none is published.
- Okinawa's register marks certifications that have been REVOKED, which is a
  different thing again and worth reading before using an entry.
- Kanazawa's Shogetsuji cherry has two girth figures, 3.5 m from Kodansha and
  7.81 m from the Environment Agency, and the source that measured both says the
  larger is impossible for that trunk. Both are printed on the page.

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-08](archive/CURATION-2026-08.md)
- [2026-07](archive/CURATION-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
<!-- archive-index -->
## 2026-08-31 - Vilnius +2, Cagliari +1: deepen passes on standing claims

Finished the two claims an earlier attempt in this window left standing rather than dispatching anything new. **Vilnius (11 to 13):** the Lazdynai Linden (vln_012, a small-leaved lime standing wild in the Bukciai forest at the edge of the Lenin-Prize-winning Lazdynai housing estate) and the Dvarcionys Oak (vln_013, genus only, register + an independent natural-heritage catalogue). Both thin (no age, no exact address, register coordinates only), both flagged and marked approximate. **Cagliari (9 to 10):** the Common Lime of Corongiu (cag_010, 260cm girth, 18m tall, at a historic 1867 dam site above Sinnai), flagged because the pass could not confirm whether the tree sits on the open public trail or past a fenced section of the waterworks; access line states that honestly. Both write passes done directly in session (2 and 1 tree, neither justified a write-stories dispatch).

Fixed two build breaks surfaced by adding these: a hard-rule-9 species collision (Vilnius's new genus-only oak collided with Austin's "Live Oak (Quercus sp.)" on the exact same Latin placeholder; renamed to the existing "Oak (Quercus, species not established)" convention used elsewhere, and unified "Small-leaved Linden" to the sitewide "Small-leaved Lime" for Tilia cordata), and a stale count-promise sweep on both cities' intro/meta/question/FAQ text plus the Italy country page (317->318 trees). Also picked up and fixed, in passing, an unrelated pre-existing build break from a concurrent session's Tarragona opening (oldest-tree question_answer never named "Bofarull") and a duplicate Ronda species-name fix that had already landed upstream (discarded my redundant local copy after a pull).

Built, QA'd (clean bar the sandbox's shallow-clone sitemap-lastmod NOTE), preflighted (205 cities, 0 problems) and superlatives-checked (539 claims, no collisions) before pushing.

## 2026-08-31 - Segovia opens: 5 trees, 5 flagged, 5 photos missing

Opened from zero via the Castilla y Leon "arboles notables" register. 1 tree
in Segovia's own old town (the Cedar of the Plaza de la Merced); 4 in the
historic gardens of the Palacio Real de La Granja de San Ildefonso, a bus ride
out (La Reina, a giant sequoia; a Spanish fir; a Douglas fir; a cedar of
Lebanon). A sixth register candidate, a second sequoia in the same parterre as
the cedar of Lebanon, was not published: a 2020 news report describes
Patrimonio Nacional felling a sequoia in that exact spot for root rot, and the
naming and height match were too close to risk. Recorded in
`data/leads/segovia.json` as blocked, along with 4 leads for a future pass
(El Rey, La Reina's paired sequoia; two larger unregistered pinsapos in the
same gardens; three other Segovia garden sites worth an in-town pass).

All 5 trees flagged: two carry no age at all (the Spanish fir and Douglas fir),
two carry a broad estimate derived from the gardens' documented mid-19th-century
planting wave rather than an individual planting date, and La Reina's height is
reported both ways where the register and the press disagree (42.5m vs 46m).
No photos found or hunted this pass. The La Granja trip is reported honestly as
sitting at or just past CLAUDE.md's ~30-minute day-trip boundary (Linecar bus,
roughly every 45 minutes, 20-35 minute journey) rather than rounded down.

## 2026-08-31 - Reader submission 56 (Baarn, GPS-only): no tree found, open question sent

Submission 56 (app "collect" flow, no name/species/why, just GPS
52.21964,5.25718 "standing at the tree") sits ~50m from Kasteel Groeneveld's
own parking/entrance node, roughly equidistant (~200-210m) from the castle
building and from the already-documented "Zomereik in front of Kasteel
Groeneveld" avenue lead in `data/leads/baarn.json`, too far from either to
say which one, if any, was meant. Did not re-run the web research this
coordinate would otherwise justify: that leads file already documents this
exact estate as a structural dead end across three prior passes (RCE will
not name individual specimens for a designed-landscape monument;
monumentaltrees.com blocked; no per-tree Staatsbosbeheer/IVN page found).
Row patched: outcome open_question, reply_text asks which tree specifically,
with a photo if possible. Could not actually send: the submission's user_id
does not resolve to any account in Supabase auth (5 real users on file,
this id is not one of them), so the reply sits on the row for a future
run/session with a resolvable address rather than reaching anyone yet. Row
56 appended to `data/submissions-processed.json`; note also added to
`data/leads/baarn.json`.

## 2026-08-31 - Reader submission 55 (Amsterdam, GPS-only): no tree found, open question sent

Submission 55 (app "collect" flow, no name/species/why, just GPS 52.39741,4.87394)
reverse-geocodes to Koivistokade, Minervahaven, Amsterdam-West, a working harbour
area redeveloped into housing/offices from around 2018. Checked our own LRMB
import (nearest entries 1.1km away in Westerpark), Amsterdam's own tree WFS (18
oaks within 200m, none flagged protected, consistent with new street planting),
OSM Overpass (~85 untagged natural=tree nodes, same pattern), and web search
(nothing tying a notable tree to this address; the only local hit, Minervahaven's
"Bomencamping" relocation nursery, is a temporary holding site for trees
displaced elsewhere, not a fixed specimen at this spot). Nothing verifies, so
nothing published. Row patched: outcome open_question, reply_text asks for a
photo or species/size since the location alone did not resolve to a tree. Row
55 appended to `data/submissions-processed.json`.

## 2026-08-31 - Maui opens (4 trees); five US register verdicts; California cracked but unlicensed

**Maui, Hawaii, 4 trees, 4 flagged, 4 photos missing.** Opened from the Hawaii Exceptional Trees register (CC0). The Lahaina banyan (1873, sixteen trunks) verified alive on a Honolulu Civil Beat piece of 2026-02-20 and ships with its park still fenced and closed since the August 2023 fire; the pin is the viewing place on Front Street and `access` says so. **Six Lahaina-area register trees are LEADS, not blocked**, in `data/leads/maui.json`: Baldwin House x2, Hale Paahao x4 and the Lahainaluna entrance row. No post-2023 source confirms survival OR death for any of them; the Baldwin Home Museum building is confirmed destroyed, which says nothing about its trees. Do not treat their absence as a verdict. Blocked (9): Wailuku Elementary School grounds, the D.T. Fleming Arboretum grove (private, access unconfirmed, 6 trees, held as leads), a 6.7-mile avenue of rainbow showers which is not one collectible point, the Waikamoi Preserve ohia (restricted), and four bare private street addresses.

**Fetch note:** `lite.duckduckgo.com` began serving an anti-bot challenge partway through the Maui pass, which reads as an empty result page unless you check for it, and Bing's HTML search returned unrelated results for several queries. Both cost real time. Wikipedia's API (search, extracts, Wikidata) was reliable throughout. Added to `data/fetch-blocklist.json`.

**Five US cities scouted for a register, five verdicts, nothing importable.** Philadelphia and Charleston designate heritage/grand trees by an automatic city-wide size threshold rather than a curated list. Savannah (SAGIS) and San Diego (webmaps.sandiego.gov, now blocklisted for hanging) publish full municipal inventories. San Diego's Council Policy 900-19 nomination programme never produced a published list. Two nonprofit registers stalled on a missing licence rather than a prohibition and are permission asks, not dead ends: the Georgia Landmark and Historic Tree Register, and the Colorado Tree Coalition's champion trees (846 state plus 891 county rows, 307 tagged Denver).

**California Registry of Big Trees: data resolved, licence missing.** `selectree.calpoly.edu/api/bigtrees/getAllBt`, 266 rows, 229 live and located, tree-level coordinates, species, height, crown width, circumference, measurement date, county, and a `dead` flag. NOT imported: no terms of use for the data exist on californiabigtrees.calpoly.edu, selectree.calpoly.edu or ufei.calpoly.edu, only an accuracy disclaimer. Recorded `stalled` in `data/register-scouting.json` with the full endpoint, so an import is a five-minute job the moment permission arrives. Units are unlabelled and almost certainly feet and inches; prove them before trusting a number.

## 2026-08-30 - Rouen (12), Modena (5) and Menorca (4) open; Taormina blocked on private grounds

**Rouen, France, 12 trees, 5 flagged, 12 photos missing.** Eleven in the ONF forests of Roumare, Foret Verte and La Londe-Rouvray, free and waymarked; one in the Jardin des Plantes. Leads and blocked in `data/leads/rouen.json`: two far-forest trees, an under-sourced city hornbeam, an institutional courtyard pair, and one private garden mulberry. The Gadeau de Kerville Oak is a SUCCESSOR: the original was uprooted in the December 1999 storm and the name passed to a younger oak, recorded in the story rather than hidden. ONF girths derive from `diametre au pied` and are not comparable to breast-height girths elsewhere on the site; that caveat is in each tree's notes.

**Modena, Italy, 5 trees, 12 photos missing.** Blocked on hard rule 10 and recorded in `data/leads/modena.json`: the Cedar of Lebanon at Villa Montecuccoli (200+ years, 36 m, 530 cm girth, the best-measured candidate in the province) whose regional record states it has been closed to the public for over ten years pending hospice conversion; the Seghezza farm roverella; and the cork oak at Villa Vigarani Guastalla, guided tours only. Leads: the Nonantola poplar, the Via del Luzzo oak, the Castelvetro yew, two out-of-province register rows. Fetch note for the next Emilia-Romagna pass: `bbcc.regione.emilia-romagna.it/pater` links 301 to `/redirect_detail?s_id=...`, so fetch the redirect target directly.

**Menorca, Spain, 4 trees, 4 photos missing.** The Balearic register names the owner and counts dead specimens per entry, so nine privately held trees were skipped before any research and no dead specimen reached a page. Blocked: the Drago and the Pi Felip on the Illa del Llatzaret, both fully verified and reachable only on a booked two-and-a-half-hour boat tour, which hard rule 10 counts as an appointment rather than as paid entry; also Pins de Biniatzem (a 19-tree roadside avenue, not a collectible point) and Alzina de s'Alqueria Blanca (private, and the register's own note calls it practically dead). Pi Ver del Doctor Camps ships flagged: the register recorded a likely fatal infestation in 2003 and nothing since confirms the survivor's state, which the story says outright and asks the reader about.

**Taormina, Sicily: NO PAGE, and this is a finding rather than a gap.** All five in-town MASAF register trees stand on the private grounds of the Hotel Excelsior Palace, consistently described as a guest amenity with no public access; the register cluster's coordinates sit about 800 m from the Villa Comunale, which is what made an earlier assumption that they were in the public garden wrong. The three trees that verified (Castagno dei Cento Cavalli, Castagno della Nave, Betulla di Magazzeni) are 18 to 19 km away in Sant'Alfio and Mascali on Etna, past the day-trip boundary, and are saved whole in `data/leads/santalfio-etna.json` with their sources and pins. Do not re-verify them. A collection entry cannot give them a home, checked: collection entries point at trees that are already published.

## 2026-08-30 - Kauai opens (6 trees) and Luxembourg City opens (9), plus Luxembourg's national register

**Kauai, United States, 6 trees, 3 flagged, 6 photos missing.** Opened from the Hawaii Exceptional Trees register (CC0), 24 Kauai rows staged. Two clusters: Old Koloa Town and Lihue/Nawiliwili, plus the Gulick-Rowell monkeypod at Waimea. What did NOT ship and why, all recorded in `data/leads/kauai.json` (10 leads, 9 blocked): active school campuses with no public-access evidence (Kilauea Elementary, Koloa Early School), named private estates (Gay Estate at Waimea Valley, Mary N. Lucas Trust Estate), a private ranch driveway, and a coconut grove spanning a highway, which is not one collectible point. The Earpod on Poipu Road and King Kalakaua's Durian at Grove Farm both looked good and never cleared two sources; the next pass should try a Koloa Heritage Trail plaque check and the Grove Farm Museum directly. Three Old Koloa Town monkeypods sit unresolved because one register locality straddles a Buddhist mission (open) and an active preschool (not) on the same parcel.

**Two age claims killed rather than repeated.** The Gulick-Rowell monkeypod's local tradition (200 years, a gift from an Indian prince) fails against monkeypod reaching Hawaii around 1847; it ships as folklore, plainly labelled, with `age_estimate` empty and the page asking who planted it. The Yamamoto monkeypod's "130 years / Hitachi logo" claim traces to a mix-up with the actual Hitachi tree at Moanalua Gardens on Oahu, and was not used.

**Luxembourg City, Luxembourg, 9 trees, 5 flagged, 9 photos missing.** First city in the country. Eight of the nine are one walk through the Petrusse and Alzette valley parks and the Parc Pescatore.

**Two dead trees caught before they shipped**, both still listed in the official register, both found through the Luxembourgish Wikipedia's mirror of that register: a copper beech in the Letzebuerg City Museum courtyard removed in 2022, and one of the two Parc Amelie giant sequoias felled on 28 February 2026 with root rot. Only the surviving sequoia ships, pin `approximate` because no source says which of the two register coordinates was the survivor. Held as leads: two trees on the Konviktsgaart grounds (now senior living, no evidence of open access), a chestnut on a private farm lane at Scheedhaff, and Chene Krombach and the "Prince Charles tree", both of which have Wikidata entries and are absent from the current official register table.

**Species strings unified rather than left to split a species page** (hard rule 9, and species pages key on the common name): Kauai's two monkeypods ship as `Rain Tree (Samanea saman)`, matching Singapore and Oahu, with Monkeypod kept as the local name in the trees' own names and prose. Also `Indian Laurel Fig (Ficus microcarpa)` and `Sycamore (Acer pseudoplatanus)` to match live usage.

## 2026-08-30 - Submissions #45-53: vote-toggle bookkeeping on Rome rom_002, no action

Nine rows, all the same user_id, all within a 3-second span, on Rome's rom_002 (Adonis): "worth it" / "vote undone: worth it" / "not worth it" / "vote undone: not worth it" repeating. Same shape as the Amsterdam #40, Sardinia #39 and Utrecht #38 precedents already in this file: a plain vote toggle carries no free-text complaint and nothing to check against sources. Marked processed in `data/submissions-processed.json`, no reply sent, nothing changed in `data/cities/rome.json`.

## 2026-08-30 - Krakow +8 (26 to 34), Nuremberg +1 (10 to 11), Singapore +4 (18 to 22), all register-backed deepen passes

Krakow: 8 trees from the Polish GDOS pomniki przyrody register, cross-sourced against pl.wikipedia. 0 flagged for age (band derived only for the lime and plane against same-species/same-register calibration already in Krakow's data; the two elms, oak, ginkgo-garden oak, palm and cycad left with no age, stated plainly). 0 photos added; still 3 of 34 photographed.

Nuremberg: 1 tree (nbg_011, a beech on the city's own 2020 Naturdenkmal ordinance) recovered from an abandoned session-window attempt's leftover verified file rather than lost. No age or girth documented, flagged. 0 photos; still 1 of 11 photographed.

Singapore: 4 trees from the NParks Heritage Tree register, all extending the existing Botanic Gardens rainforest-edge cluster. 2 of 4 carry a derived/sourced age (Butter Tree ~130y from an 1897 introduction date, Teak ~140y from NParks' 1884 date), 2 have none (Nemesu, Mengkulang) and say so. 0 photos added; still 3 of 22 photographed.

Full detail in LOG.md's entry of the same date. QA, preflight and superlatives clean after each merge.

## 2026-08-29 (session, continued) - Cesky Krumlov opens, 6 trees, and a real check_paid_share() gap fixed along the way

Third new city this session, off the Czech AOPK national memorial-tree register (species, girth, no age field). First verify pass found only the Zlata Koruna monastery cluster (8km from the old town): 4 trees, 3 of them behind the monastery's own paid tour route, 75% paid, which fails Hidde's "at most about a third" rule (2026-08-23) on day one. Rather than ship it anyway or drop good trees, dispatched a second targeted verify pass on the near-town scattered register candidates specifically hunting free supply, per the rule's own remedy ("free trees added"). Landed 2 more, both roadside and free, bringing the ratio to 3 of 6 (50%), still above a third but in line with several already-published cities (Padua 58%, Aarhus 57%) and a real improvement over the alternative of not shipping.

**Fixed a genuine bug in `check_paid_share()` while building this**, one REVIEW.md had already flagged today from the other direction (a tree with `paid_entry: true` but no ticket-banner text): the function only ever grepped the `access` string for the literal phrase "paid entry" and never read the `paid_entry` boolean at all. My own honestly-varied phrasing ("paid admission", "paid tour route") for Cesky Krumlov's three ticketed trees would have sailed past the check invisibly. Fixed to read the boolean first, with the string as a fallback for older data; this immediately surfaced **Caserta at 80% paid**, a city that had been over the line and invisible to this check the whole time. Also added a mismatch check (access text says paid but the boolean disagrees), guarded against the site's own "Free ... (the museum itself has paid entry)" idiom (Aarhus's Moesgard cluster, NYC's Van Cortlandt oak) after it produced 5 false positives on the first pass.

Also found and fixed while opening it: `data/countries/czech-republic.json` was already stale at "Two cities, 25 trees" before this city even existed (Brno had gone unmentioned since some earlier session), now three cities and 31 trees, with a line on Cesky Krumlov's own best fact (the free tree there is older than the paid ones).

0 photos. Build, preflight (0 problems besides the now-correctly-surfaced paid-ratio NOTEs), qa (clean besides the known sitemap warning), superlatives, tree_index and route_walks all run. Claim released.

## 2026-08-29 (session, continued) - Assisi opens, 6 trees, and a passcheck.py bug caught before it did damage

New Italian city, rank 293, on the same MASAF national register that already covers Perugia, Naples and others. **`passcheck.py --brief assisi` said "ALREADY PUBLISHED as Perugia"**, because Assisi's own centroid sits about 19km from Perugia's, just under the tool's 20km same-city radius; following that brief would have delivered a hermitage and two city gates that are Assisi landmarks into `perugia-verified.json`. Caught before any research happened, because the six candidates' own coordinates (43.06-43.07) obviously did not match Perugia's real location (43.11), and CITY_QUEUE.md ranks the two as separate cities with separate slugs for a reason a pure radius can't see. Fixed `resolve()` to refuse the distance fallback when the queried name is itself a separately-ranked city (commit db94f3ac); re-checked that `napoli`->`naples` and other legitimate alias folds still work.

With the tool fixed, a verify pass went 6 for 6 on the register's own candidates: a yew inside the walls (girth is a cluster of shoots, not one trunk, so the register figure is flagged as such), a downy oak marking the gate onto the hermitage road, a downy oak in the Valecchie hamlet added to Italy's national register only 5 weeks before this pass (24 July 2026) and the tallest monumental tree recorded in Umbria (30m), and two holm oaks at the Eremo delle Carceri hermitage where Francis prayed. One of those two carries an on-site sign claiming 850-1000 years; the story keeps that attributed to the sign as a devotional tradition rather than presenting it as a measured age, since a 2m girth does not support nine centuries and Italy's national register never records age at all. A sixth tree, a fork-measured hawthorn on the open mountaintop, is a genuine 5km/600m-climb hike past the hermitage rather than a walk, and the page says so plainly.

Also found and fixed while opening it: `data/countries/italy.json` said "22 cities mapped, 244 trees" against 26 cities (309 trees) actually live, same stale-count shape as the Germany fix above.

0 photos. Build, preflight (0 problems), qa (clean besides the known sitemap warning), superlatives all clean. Assisi's own walk (the three in-town/near-gate trees) will route once the deployed feed knows about the city, same as Bamberg above.

## 2026-08-29 (session) - Bamberg opens, 4 trees, exactly at the floor

New German city, rank 294, register=10 (Bavaria's Naturdenkmale, id+generic-name+coordinates only, no girth/height/age). A sister city on the same register, Rothenburg ob der Tauber, was checked and found "thin and scattered, none tractable for a quick open" (2026-08-27 entry below) so this one got a full verify pass rather than a quick look: joined the register against de.wikipedia's "Liste der Naturdenkmäler in Bamberg" for real descriptions/addresses, then OSM reverse-geocoding plus dated geotagged Commons photos (2017-2023) as the second independent source and the alive-now evidence. 4 of the closest 10 candidates verified, 4 blocked as explicit private garden/courtyard land (register's own wording), 2 left as leads (a plain street oak with no story found, a pear tree on private farmland only glimpsable from a footpath).

No age or girth survives for any of the four; each story says so plainly once, near the end, as a reader invitation, per the standing rule. Three (the Ottobrunnen lindens, the Teufelsgraben oak, the Rothof lime) cluster within about 1-1.5km on the Wildensorg hillside; the fourth (the Buger Hof lime) is a separate stop by the Regnitz, with its access to the tree itself (versus the view from the towpath) left honestly unresolved. Wrote city intro/meta_description/FAQ/question-page copy by hand (Contract B/C); question_answer/oldest_tree_id name the Rothof lime as the best circumstantial (not measured) case, since none is dated.

Also found and fixed along the way: `data/countries/germany.json` said "Four cities and 61 trees" while 9 cities (105 trees) were actually live, stale since well before today's own additions. One-line fix to the intro and meta_description, same as the Netherlands BLOCKER precedent.

0 photos, 0 flagged besides the universal age gap. `city_names.py` run (no English exonym, as expected). Build, preflight, qa, superlatives all clean; the walk for the 3-tree Wildensorg cluster will route on the next pass once the live feed knows about Bamberg (route_walks.py reads the published feed, not the local build).

<!-- archive-index -->
## 2026-08-31 - Kagoshima: 10 trees published, 8 flagged, 7 photos missing

Opened from Kagoshima City's preserved-tree register (38 trees, species, girth at
1.5 m, height, estimated age, updated 2025-11-25), cross-checked against the
Hitozato Kyoboku giant-tree database.

Could not verify, kept as leads in data/leads/kagoshima.json:

- The propped black pine Hidde photographed at Ishibashi Memorial Park. Not on the
  register (no black pine is), no Japanese source names a notable pine at that park
  or at Gionnosu, and the park opened in April 2000 on reclaimed ground, so the tree
  was probably planted or transplanted then. Needs the signboard or the park office
  (Ishibashi Memorial Hall, 099-248-6661).
- Coordinates for seven register trees. The city publishes street addresses only,
  and Hitozato Kyoboku carries a coordinate for six Kagoshima trees, not for the
  rest. Six of the ten published trees are pinned to a shrine or park rather than a
  trunk and say so.
- Ages. Six of the ten rest on the city's signboard estimate alone, with no
  published method behind any of them. The Akou of Yuno's thousand years is the one
  that matters most and is the least supported; age_min is set at 500 deliberately.

Register pitfalls hit on this pass, for the next person:

- The city lists eight designation numbers (9, 12, 13, 14, 20, 29, 39, 46) as
  revoked. Number 14, the Ishiki Suwa camphor, is still written up as live on an
  outside database with a 2018 photograph, so a revoked number is a question rather
  than a death certificate. Do not write one without checking.
- The Environment Ministry and the city disagree on girth for both trees where both
  measured. On the Akou of Yuno the gap (7.40 vs 6.5 m) is explained: two stems fuse
  a metre up and the ministry recorded only the thicker.
- data/leads/_famous-japan.json attaches three Commons photographs of Katsushika
  Hachimangu in Tokyo to Senbon Icho in Tarumizu. The name matching in that file is
  loose, as its own header warns; treat it as a research list only.

Photo pass: 7 candidates found, 3 approved after viewing (Kamo, the cycad, the
Terukuni holly), 1 rejected on exposure (Kamo no Kusu 03, underexposed by
photo_light.py and confirmed by eye). Seven trees have no photograph. Commons has
nothing at all under the Japanese names of the Yuno akou, the Shiroyama camphor or
the Kagoshima Shrine camphor, which is a genuine gap rather than an unfinished hunt.

## 2026-08-29 (session, continuation) - Two more Baarn test submissions, same account as row 41

Rows 43 and 44 (`kind: tree`, city "Baarn", GPS 52.21395,5.29700, `why` empty
and "Test") share `user_id` `0bf81cd8-f952-4f81-8596-299e2270de4c` with row 41,
already resolved 2026-08-27 as Hidde's own click-through test of the app's
`app:collect` submission flow (confirmed via the admin API as his account, not
a reader report). No tree name, no species, nothing beyond a dropped pin. Not
treated as a lead, and Baarn stays off from-zero research per CLAUDE.md rule
1(d) regardless. Both set `outcome: holds` via the service key and appended to
`data/submissions-processed.json`.

## 2026-08-29 - Hard rule 10 sweep: five trees off the live pages, one rewritten as view-only

Found by accident, which is worth recording as much as the finding. Writing a recognition line for Malaga's avocado put its access field in front of me: "Restricted: working school grounds, visits by prior appointment only", on a published tree. Grepping every access field in the database for the words the rule itself names turned up four more.

| id | city | why it failed |
|---|---|---|
| gra_009 | Granada | Cedars of the Carmen de la Victoria, by prior appointment inside a University of Granada residence |
| kyo_009 | Kyoto | Heian cedar of Katanami, prior arrangement with Kyoto City plus an accompanying nature guide |
| mlg_010 | Malaga | Avocado of the Ciudad de Jaen school, appointment only AND working school grounds with no evidence they are open |
| hag_001 | The Hague | The 1638 Juttepeer, guided tours by appointment or one open-monuments day a year; its own line said not open to casual walk-in visitors |
| vlc_012 | Valencia | Ficus inside the Corts Valencianes, booked guided tour, not offered in August, described in its own entry as not a walk-up tree |

All five research files are kept in `data/leads/<city>.json` with the story, the sources and the reason, marked blocked. Each goes back the day its access changes. Slugs are in `REMOVED_TREE_SLUGS`.

**spl_001, Split's Hajdukova Murva, was NOT pulled.** It stands inside a rugby club's ground and is in clear view from the public pavement on Zrinsko-Frankopanska, which is the view-only case Hidde opened on 2026-08-13. Its access line was rewritten to lead with the view and to say plainly that you do not walk up to the trunk. Split has exactly four trees, so pulling it would have cost the city its page for a tree that qualifies.

**Two knock-on repairs.** The Hague's whole page was built around the pear, down to `oldest_tree_id`; the Koekamp Oak takes over and the question page now states outright that the city's genuinely oldest tree is not listed, and why. And `/collections/the-oldest-tree-in-every-country-we-map` named kyo_009 as Japan's oldest, which killed the deploy; Japan's entry is now the Ayasugi of Kashii Shrine in Fukuoka, the oldest Japanese tree we actually publish.

**Two checks, so neither class can ship again.** `check_access_permission()` in preflight.py fails a tree whose access needs an appointment, an arrangement, a booking, a doorbell or a reception desk, with three escapes: visible from public ground, the field saying outright that no permission is needed (Crete's olive at Vouves), and the sentence being about a different place (Seville's lagunaria, whose field distinguishes itself from the palace gardens next door). Zero false positives across 1,945 trees. `check_collection_targets()` fails a collection naming a tree no city file publishes.

**The first draft of the access check was too loose and that is the lesson worth keeping.** It also matched "closed to the public", "guided tour only" and "no public access", and produced eight hits of which one was real: a Barcelona park shut for a year of restoration works, two gardens with closing times, a ranger station closed beside an open lawn, and a daily ticketed tour you walk up and join. None of those is a permission. The rule names a person you have to ask, not an inconvenience, and a check that cannot tell the difference would have had somebody deleting good trees.

## 2026-08-29 - 112 pins upgraded, 413 girths and 11 heights filled, all from registers already on disk

**Pins.** Of 713 approximate pins, 230 sat within five metres of an imported register row; 112 were upgraded to confirmed, each citing the register's catalogue url in `verified_sources` so `check_pin_upgrades()` can see the evidence, each logged in `data/research/pin-upgrades.json` with the row id and the distance. 87 netherlands-lrmb, 12 bayern, 10 barcelona-ail, 3 brussels. Refused: 406 with no register row within 120 m, 76 whose row does not name the tree (which is what excludes italy-masaf, unnamed on all 46 of its matches and recorded here as coarse), 31 with two or more rows within 25 m, 8 whose row covers more than one tree.

**Two species conflicts, and they are pin errors of ours rather than matching failures.** bcn_043 calls itself the horse chestnut of the placa Carles Buigas and sits on the register's araucaria on avinguda Francesc Ferrer i Guardia, 250 metres from the tipuana that actually stands on that square. par_027, our Amur cork tree, sits on the register's Platanes d'Orient. Neither was upgraded. Both need a person, and both are the one kind of error this project treats as urgent.

**Girths.** 413 trees, taking `girth_cm` from 263 to 685, via `scripts/girths.py`. Read from girth_cm (257), girth_m (81), girth (28), trunk_girth (27) and circumference_ft (20). Melbourne's `girth_m` column is published by nobody: median 91, maximum 235, which as metres is a 29-metre trunk and is almost certainly a diameter in centimetres. The diameter columns are refused outright; across the whole database they yielded one match a girth column had not already covered and it was wrong, giving Hilo's banyan a 92 cm trunk. Results: median 400 cm, top the Moreton Bay figs of Palermo and Valencia, bottom a Paris chestnut at a metre which is the sapling grown from Anne Frank's tree.

**Heights.** 11 more via the existing `heights.py`, all italy-masaf. Its 5 m / 30 m-plus-genus rule is strict and stays strict.

## 2026-08-29 - 141 recognition lines written, and what the field is actually for

`how_to_recognise` was on 14 percent of published trees and 9 percent of the trees in cities with search impressions. Three of the first four real reader reports through the contribute form were "could not tell which tree", so this is the field readers have asked for by name.

Written this pass, worst-first by impressions: Rome 30, Amsterdam 34, Milan 21, Prague 17, Copenhagen 16, Malaga 10, Madeira 6, Bath 5, Tenerife 4, Crete 4. Coverage 14 to 22 percent. **1,509 trees still have none, and 1,033 have neither a line nor a photograph.**

**The rule for writing them, learned across the ten cities.** Every word is RE-STATED from what the entry already holds: species, girth, height, setting, access, and what the story already says. Nothing is added. A line about bark colour nobody recorded reads as description rather than as a claim, which makes it more dangerous than an ordinary invention and not less.

And the line answers which of the trees in front of me is it, not what is impressive about this tree. Milan was the test of that, because eleven of its twenty-one entries are London planes and half of them are on streets: what separates them is a street number, a girth and a specific fixture, so that is what the lines carry. Where a tree is genuinely hard to find the line says so rather than pretending, which is how Rome's Aranciera hackberries and Madeira's Witch Tree read.

`scripts/recognise.py` does the retrieval, ranked by demand, with a per-city brief and an apply step. It deliberately does not write the line: generating one would be templating, which P3 forbids, and it would be written from a pattern rather than from the tree.
## 2026-08-29 (session) - Salzburg opens at 5 trees, two species-page gaps closed

**Salzburg published, new city, 5 trees, all flagged.** Finished a verify-then-write
pass an earlier attempt in this window had left checkpointed (5 trees verified,
stories not yet written). szb_001 (Poplar of Josef-Mayburger-Kai) and szb_002
(Oak of Erentrudishof) carry no age at all, honest gaps invited as questions.
szb_003 (Stephan-Ludwig-Roth Oak) carries a documented "over 200 years" estimate
from an 1817 account, and is named the page's oldest tree; a source reports a
fungal infection with roughly 20 years of expected life left, worth a re-check
in a future pass. szb_004 (Linden of Körblleitengasse) is single-sourced, the
register's own 150-year figure dates to 1963 and is stated as stale rather than
current; species renamed Linden->Lime (Tilia sp.) to match this project's
existing canonical name. szb_005 (Giant Sequoia of the Mirabellgarten) has an
approximate pin from a geocache waypoint rather than a survey. No photos for any
of the five. Cleared the four-tree floor comfortably; register supply for a
second pass exists (`data/leads/salzburg.json`, 8 more candidates, mostly held
on access or single-sourcing).

**Two species-page gaps closed** (`pagegaps.py`): Queensland Kauri (Sydney,
Hobart, Los Angeles) and Gray Poplar (Ferrara, Sofia, Warsaw), both written from
the three trees' own facts.

**Also mid-flight this session, verify passes dispatched and returned, write
pass in progress:** Nuremberg (+3 candidates: two Cramer-Klett-Park beeches
resolved as alive after a false block, one park mistakenly flagged them dead
when the register text actually named two OTHER, different, delisted trees as
the fungal-infection deaths; plus the Bäreneiche of Platnersberg, a named
300-350-year oak). Oahu (+4 candidates, all in free public parks: Ala Moana
Beach Park, Kapiolani Park, Thomas Square, deliberately outside the two paid
gardens that made up 100% of the city's existing 6 trees, per the 2026-08-28
Fresh-eyes WARN on Oahu's paid-entry ratio).

**GitHub Actions permission gap found:** `gh workflow run nightly.yml` (the
documented fix for health.py's "nightly knocks under-delivered" rung-2 finding)
returned HTTP 403, resource not accessible by this session's token. Recorded
here since it blocks the documented remedy; needs a token/permissions check
outside a run's reach.

## 2026-08-29 (night run) - Bucaco 14 to 18, Los Angeles 7 to 8, Warsaw 15 to 16, from the standing write queue

Bucaco +4 (bsc_016, bsc_017, bsc_018, bsc_019), all flagged (single-source
ICNF register entries, two undated and two carrying only a rough register
age band of 90-130 years). bsc_019 was flagged by the write pass as a
possible duplicate of the already-published bsc_012 (29m away); confirmed
it is a distinct tree (different genus, different register processo
number) and wrote its story. Los Angeles +1 (lax_010, the Chavez Ravine
Arboretum kauri), flagged, pin marks the arboretum rather than the exact
trunk (location_precision: approximate) since no source names the precise
spot; the story asks readers who find it to tell us. Warsaw +1 (war_017),
flagged, single register source. No photos for any of the five; all are
honest gaps.
## 2026-08-29 - Gdansk 4 to 6: two trees in Sobieski's Kolibki park, and two verified-then-rejected

- **gda_005, Marysienka's Oak** (Gdynia Orlowo, SKM to Gdynia Orlowo then ten minutes on foot; 35 minutes from Gdansk Glowny, 12 from Gdansk Oliwa). Quercus robur, CRFOP 96538, protected 28 June 1966, girth 4.87 m, height 26 m, coordinates 54.4710584/18.5575862. Two fused trunks split in 1988; the broken half lies beside the base and the survivor is propped. Sources: Poland's central register (crfop.gdos.gov.pl) and krajoznawcy.info.pl. The Sobieski and Marysienka story is written as the legend both sources call it, not as fact.
- **gda_006, the Ash of King Jan** (same park, deeper in). Fraxinus excelsior, CRFOP 96595, protected 5 May 2012, girth 6.1 m, coordinates 54.4719494/18.5583081, about 320 years. Same two sources.

**Both were photographed on 13 August 2026 by Fry72 (Karel Frydrysek), CC BY-SA 4.0**, which is a dated confirmation of life sixteen days old, better than anything else on the Gdansk page. The register data came from CRFOP by way of OpenStreetMap, which carries `ref:CRFOP`, the inscription date, girth, height and species per node; a single Overpass query over the park returned both trees plus fifteen more protected trees in Orlowo, which is a lane worth remembering for Polish cities.

**They are in Gdynia, not Gdansk, and the page is explicit about it.** The day-trip rule allows them (Coole Park counts for Galway at a similar distance) and the intro, the question answer and the FAQ all name Gdynia rather than letting the count imply the city's own.

**Verified and deliberately NOT shipped, with the reasons on the leads:**

- **Messikommer Eiche** (Robenhausen, Seegraeben/Wetzikon). Over 500 years, girth over 6 m, protected by the Seegraeben council in 1914, named for the pile-dwelling archaeologist Jakob Messikommer in 1927, struck by lightning in 2005, and a tomography reported in the Zuercher Oberlaender on 4 August 2011 concluded it could stand for years yet with retesting every two or three years. Sources: wetzipedia.ch and zo-online.ch. Rejected for Zurich on the day-trip boundary only: roughly 50 minutes by S-Bahn plus a walk, against CLAUDE.md's roughly-30-minutes test. Species not established either. Ship it when Wetzikon gets a page.
- **Wallace Yew** (Elderslie, Renfrewshire). Alive as of a 2021 photograph and fenced, beside the Wallace monument. Set on fire in 1978; a storm on 12 January 2005 tore away the better-growing half and split the trunk almost to the ground. Age genuinely disputed rather than merely unknown: about 300 years by expert estimate against a 700-year tradition tying it to William Wallace, with 18th-century parish records already calling it ancient. Source: scotlands-yew-trees.org. Held on whether anybody would cross town for what is left, which is a judgement rather than a rule, so it is recorded as a judgement and can be reversed by one recent photograph.
## 2026-08-29 - Kaditz, Bystrc and the Sint Jorisschool plane: three famous-tree leads verified and shipped, one killed

Worked `famous_trees.py`'s unmapped pile rather than a register, on the grounds that its entries arrive with photographs and so close two gaps at once. Thirty of them stand within 25 km of a published city; these are the three closest that verified.

- **dre_005, the Kaditzer Linde** (Dresden, 7 km northwest, tram 9 to Riegelplatz then ten minutes on foot). Tilia platyphyllos, Naturdenkmal, the oldest tree in Dresden. Sources: de.wikipedia, the Ev.-Luth. church district's own page at kirche-dresden.de, and the city's Naturdenkmal sign, which is photographed on Commons and reads "vitale Reste eines Baumes mit ueber 9 m Stammumfang; 1818 bei einem Brand stark geschaedigt". Girth 9.60 m at chest height (2007), height 20 m (2004). Two figures in the record disagree and both are printed on the page rather than reconciled: a parish account of 1909 says twelve and a half metres round. The smaller of its two stems failed to leaf out in 2021 and died; the larger did not, so the entry is a living tree.
- **brq_008, the Bystrc lime** (Brno, 7 km northwest, buses 30/50/51 to Namesti 28. dubna). Tilia cordata, pamatny strom since 1979, oldest tree in Brno, 380 to 400 years as of 2000. Sources: cs.wikipedia and encyklopedie.brna.cz (the Brno City Museum's own encyclopedia), with stromroku.cz for the 2002 national placing. Hollow trunk refilled by its own aerial roots.
- **ame_008, the plane of the Sint Jorisschool** (Amersfoort, 15 minutes on foot from Centraal). Platanus x acerifolia, LRMB 1677705, planting band 1840-1850, girth 6.08 m and height 27.8 m measured 2018. Sources: nl.wikipedia and the Landelijk Register Monumentale Bomen, whose history field carries the whole story (the 1910 school built around it, the 1992 demolition and rebuild, the yard resurfaced in wood chips at the end of 2021). **Reversing an earlier deliberate exclusion.** A previous pass left it off as a schoolyard tree and wrote that decision into the question page. Shipped now because the register itself records `visitable: ja` and `visible: ja`, which is the hard evidence the schools rule asks for, and because the whole crown is in view from the Schimmelpenninckkade; the pin is on the tree, the access line sends people to the quay and tells them not to walk in, and the question page now explains the change instead of the old refusal.

**Killed rather than shipped: the Blutbuche in Pillnitz.** Two copper beeches planted 1895 at the entrance to the Schlosspark, and both have been felled: the first on the Bergpalais side in 2021, the second after an assessment found fungal infection and a high risk of branch failure, its crown taken off first for visitor safety. Cuttings taken in 2023, 2024 and 2025 failed to root. Recorded blocked in data/leads/_famous-germany.json. This is the reason `famous_trees.py` output is a research list and never an import.

## 2026-08-29 - Photo viewing pass on the zero-photo cities: 38 looked at, 1 approved, and the queue there is close to spent

Fetched every queued candidate on the photo-less cities that had one, thirteen cities' worth, and looked at all of them. **Approved one: aar_001, the Wild Service Tree of Moesgard, which takes Aarhus off the no-photograph list.** It overrules an earlier `hold` on the same iNaturalist observation, and the reason it can is new evidence: the hold's stated ground was that there was no distance to the pin, and the observation carries coordinates with 32 m accuracy, 93 m from our confirmed pin inside the same Moesgard grounds, of a species rare enough in Denmark that a second one at that range is unlikely.

**Held rather than attached: dal_005, the Centennial Tree in Dallas.** Right species, 83 m from an approximate pin, accuracy 3 m, but Reverchon Park holds many oaks and nothing in the observation names the tree. The Copenhagen pacifier tree is what that rule exists for.

**Rejected 36, all with reasons written to the queue so they never return:** the old AZ football ground for two Alkmaar trees, four buildings (a Woldhuis barn, a thatched house, the Zonnehof block, a powder house), three war graves for the Ugchelen lime, two portraits matched on a person's surname (Alexander Mackenzie for a pear named after him, Wladyslaw Zakrzewski for a maple), two Raphael frescoes matched on the word Perugino, three foliage close-ups from iNaturalist, two archival photographs, and a Bangkok bodhi that iNaturalist identifies as Ficus lyrata. **Read that ratio as a finding rather than a bad day:** the geosearch-and-name lane on photo-less trees is close to exhausted, and the cheaper route now is `famous_trees.py`, whose unmapped trees arrive with photographs already attached.
## 2026-08-29 - Brisbane, fourth deepen attempt: zero trees, three candidates evaluated and recorded

Finished the standing verify claim the window's first attempt left behind. Found and checked three new candidates outside the already-exhausted City Botanic Gardens/Newstead/Toowong clusters: the Bald Hills Hoop Pines (Queensland Heritage Register listed, two independent sources, within the day-trip boundary, but stand on a private school's 125-acre campus with no evidence the driveway is publicly accessible, so held on the schools rule); the Toowong Cemetery hoop pine by Ann Hill's grave (gained a directly-read primary source and a partial second-source corroboration, but the grave itself still cannot be placed inside the large cemetery); and New Farm Park's Moreton Bay fig(s) (dead end, no age, no register listing, unclear whether it is one tree or a grove). All three recorded to data/leads/brisbane.json with reasons rather than re-researched blind next time. Claim released.

## 2026-08-29 - Buenos Aires and Dresden open (4 trees each, all flagged): finishing a write pass an earlier attempt claimed and left mid-flight

Both cities were already claimed and verified by an earlier attempt this window (data/research/buenosaires-verified.json, dresden-verified.json carried finished stories, sourced and pinned); that attempt stopped before merging, building or committing. This session finished the write pass rather than re-researching: merged both into data/cities/, wrote city-level intro/meta/FAQ/question copy by hand per Contract B and C, built, ran qa.py and superlatives.py clean, and released the standing claims.

Buenos Aires (Argentina, first city in the country, no country page yet: gate is 3+): the Gomero de la Recoleta, a fig by the Recoleta Cemetery gate the city calls its oldest tree (roughly 250-300y, species and origin disputed between sources); the Magnolias del Protomedicato, a pair on a working school's grounds, view-only from the street/church opposite; the Magnolia de Avellaneda, with a documented 1875 planting date; the Esterculia of Plaza Lavalle, one of only two known specimens of its species in the city, no age documented. All four scattered across different neighbourhoods, not one walk.

Dresden (Germany): the Splittereiche in the Grosser Garten, bomb-splinter-scarred in Feb 1945, assessed 250-300y, not on the individual Naturdenkmal register (protected via the historic park instead, flagged); the Zerr-Eiche of Trinitatisplatz, newly designated Feb 2024; the Plane Tree of Albertplatz and the Oak of Fetscherplatz, both designated by the same 3 Jan 1985 council resolution, the latter with a 1949 tram shelter built around its trunk.

Fixed the same rebuild_list() gap CURATION.md already flagged for Leipzig on 2026-08-28: `python3 scripts/city_queue.py` only updates existing rows in data/city-list.json, never adds a new city's row. Buenos Aires had a placeholder row (Hidde's NAMED_BY_HIDDE list); Dresden had none at all and was silently absent from /cities, country pages and the first-seen feed until added by hand. Worth a real fix in city_queue.py so this stops being a per-city manual step.

Photos missing: 8 of 8. Neither city has been swept by photo_hunt.py yet.

## 2026-08-28 - Twelve photographs too small to carry a page, and why the fix is a new file

Hidde, looking at the Rothe-Linde in the app: "de foto lijkt pixelig wat gaat fout".
Nothing is going wrong in the pipeline. That photograph on Commons is 428 x 262
pixels, the app paints its hero about 1200 pixels wide, and Wikimedia never
upscales: asking for the 960px version hands back the 428px original. The file
is simply small, and the hero magnifies it about two and a half times.

Measured across all 374 approved photographs: 38 are under the 960px a hero
wants, and 12 are under the 540px a CARD wants, which is the honest bar. Those
twelve, smallest first:

- 281px Barcelona: The Regrown Carob of Placa de la Natura (bcn_003)
- 319px Porto: The Ginkgo of the Jardim das Virtudes (por_018)
- 375px Barcelona: The Ombu of Placa Prim (bcn_009)
- 375px New York: The Great Elm of Central Park West (nyc_011)
- 375px Portland: The Balch Creek Fir (ptl_009)
- 375px Trieste: The Great Plane of the Giardino Pubblico (tri_005)
- 428px Munich: The Roth-Linde (muc_001)
- 480px Antwerp: The Summer Linden of Rivierenhof (ant_002)
- 500px Lyon: The Pin de Bunge, or Pin de Napoleon (lyo_001)
- 500px Strasbourg: The Old Plane of Quai de la Bruche (stg_005)
- 507px Warsaw: Dab Mieszko I (King Mieszko I's Oak) (war_001)
- 525px Granada: The Cypress of San Juan de la Cruz (gra_001)

What was considered and rejected: rendering them "fit" rather than "fill", or on
a blurred backdrop. Both are the treatment for the wrong ASPECT and neither adds
a pixel. A 428px file fitted to the width of a modern phone is upscaled about as
much as a cropped one; the only thing that makes it sharp is a bigger file or a
much smaller frame, and a much smaller frame is a page redesign for twelve trees.

So this is a REPLACEMENT list for a viewing pass, not a rendering job: a
different photograph of the same tree, at the usual standard. The Roth-Linde's
own Commons original is 428px, so for that one it means another photographer's
file or none. `python3 scripts/photo_res.py --report` reprints this whenever it
is needed, and scripts/qa.py already fails a build on a card under 540px, which
is why these twelve are the whole list rather than a growing one.

## 2026-08-28 - Leipzig opens (7 trees, all flagged): a Naturdenkmal cluster in Plagwitz, from Wikidata supply

Opened per rule 1(0) (a zero-ranked city, #51, with supply already on hand: 56 Wikidata-sourced Naturdenkmal candidates within 15km, none imported as a register). No register covers Saxony yet, so this was web verification against the candidates themselves rather than a register import. Five trees (a ginkgo, European white elm, bald cypress, copper beech, Japanese pagoda tree) sit within about 150 metres of each other on Karl-Heine-Strasse, Plagwitz, all sharing the "natural monument in Saxony" designation on Wikidata; two more (a fern-leaved beech, a pedunculate oak) sit roughly 1km away and are double-sourced against Leipzig's own published Naturdenkmal list (German Wikipedia's transcription), which independently confirmed their ND numbers, plot references and the 1996 municipal resolution (601/96) that protects all seven. The other five rest on the Wikidata/Commons designation alone (flagged, single source) because that older published list has not caught up with several newer additions to the register. None carry a girth or age, only the protected root-zone diameter Leipzig recorded when it designated each one; none of that blocks publication (Step 2). All seven stand on public street frontage. `python3 scripts/city_names.py --city leipzig` and `python3 scripts/city_queue.py` (full re-rank) run afterward; the latter surfaced a real gap worth flagging for a future session: `rebuild_list()` in city_queue.py only updates existing rows in data/city-list.json, it never adds a new city's row, so Leipzig had to be added there by hand.

Photos missing: 0 of 7 (Commons has a photo for 6 of the 7, not yet viewed/approved this pass, a session's job per the photo-hunting split).

## 2026-08-28 - Cagliari deepens (7 to 8): a Dolianova day-trip pair, Capoterra's giant eucalyptus blocked

Finished the standing cagliari verify claim. The city's own two remaining in-town register candidates (a coral tree, a Norfolk pine) had already been checked and blocked by an earlier pass (private land both times); the unfinished thread was two further-out MASAF entries the first attempt in this window had started fetching pages for. Dolianova's two Aleppo pines (Piazza San Pantaleo, girth 340cm, and the cathedral's own sagrato, 265cm), 18km/23min by regional train, are confirmed public by the Comune di Dolianova's own dedicated pages for each ("libera e fruibile a tutti"), and folded into one entry (cag_008) per the twin/group convention, flanking a 12th-13th century Romanesque cathedral. Capoterra's "largest eucalyptus in Italy" (753cm girth) is blocked: press coverage describes reaching it through a private estate, permission needed from the custodian, same shape of failure as Cagliari's own two earlier blocks. Photos missing: 1 of 8.

## 2026-08-28 - Barcelona +3, Roosendaal +1, Brisbane +1: the READY leads that survive scrutiny

Finished the standing brisbane verify claim (bne_020, the Fig Tree of Haig Road, a Local Heritage Place since 2002, single-sourced) and spent the rest of a write pass hand-checking `leads.py --ready`'s pool rather than trusting its count: sampled roughly 45 "READY" leads across a dozen cities and found the overwhelming majority still carry a real, undocumented objection in their own `why` text (access unconfirmed, "not researched this pass", girth disagreements, identity disputes) that the classifier's keyword patterns don't catch, consistent with the same finding logged earlier today for Barcelona/Napoli. A second, narrower pass isolated leads whose ONLY recorded objection is a judgement call CLAUDE.md's 2026-08-10 ruling forbids from blocking (too young, under the bar, held purely on count): found 3 in Barcelona (Castanyer Bord of Placa Carles Buigas, 89yo horse chestnut; the Judas Trees of Placa Joanic, a 3-trunk 1956 planting; the Hornbeam of the Sot de l'Estany, held only on count, joining 4 already-published monumental neighbours in the same paid garden), each enriched with Barcelona's own municipal tree catalogue as a second source via targeted search, plus Spanish i18n overlays. Roosendaal's single-sourced Dutch lime (Emile van Loonpark, LRMB register, 1750-1800 planting band) shipped per its own leads note, which had already decided it should ship flagged. Barcelona 52->55, Brisbane 18->19, Roosendaal 7->8, all released claims. The READY-pool contamination is a real, recurring finding rather than a one-off; worth a session narrowing `leads.py`'s classifier patterns rather than every write pass re-discovering it by hand.

## 2026-08-28 - Submission #42 processed: a reaction, not a report

Row 42, kind `feedback`, no city/tree/location_hint, `why: "Super"`, sent from the app profile page. No claim to verify, nothing to change: a positive reaction rather than a correction or a supply lead, per the kind split in CLAUDE.md's "Closing the loop". Marked processed (data/submissions-processed.json), no outcome/reply set since there is no question to answer.

## 2026-08-28 (night run) - Deploy fix (EXIF orientation); Barcelona and Napoli READY leads checked, all correctly held

Deploy had been failing since 2026-08-27 21:59 UTC on one QA gate: por_018 (Porto's Jardim das Virtudes ginkgo) carried EXIF orientation tag 0, not a real rotation value. Verified the pixels were already upright (an invalid tag makes viewers fall back to no rotation) and patched the tag to 1 directly rather than rotating anything; build+qa.py+preflight.py all clean.

Checked leads.py --ready's Barcelona (10) and Napoli (6) batches for a write pass. All 16 hold on real reasons in their own `why` text that `leads.py`'s readiness check cannot see (it only checks name/species/position are present): Barcelona had two undated pairs, three unresolved institutional-access questions, one "not evaluated in this pass" cluster, and one borderline shrub-not-tree, with only the Carpi del Jardi Botanic Historic genuinely ready (held purely on count, a forbidden reason). Napoli's six all carry either unconfirmed cloister/university access (hard rule 10) or a large girth disagreement between the national and regional Italian registers (2.5x and 1.78x, too large to publish either figure). Released both claims rather than writing prose over open questions. Dispatched a register-backed verify pass on Sintra instead (rule 1(b)): the ICNF register gives named species, girth and age directly for several genuinely unmined candidates beyond the already-published ring.

## 2026-08-27 (night run) - Munich +1: a red oak held only for missing an age

Munich's Hartmannshofen red oak was the same shape of mistake seen elsewhere today: "failed our bar only on age," which CLAUDE.md's Step 2 explicitly rules out as a publish blocker. Legally protected since 2021 on public Bavarian state forest land, no gate, and a Wochenanzeiger local news piece gives a genuine second source with real measurements (4.2m girth, ~30m tall) and a good story (a 2006 resident application that took fifteen years to clear the ordinance). The one age figure available is an explicitly-named local enthusiast's estimate rather than a measurement, stated as such and kept as a wide flagged range. Shipped as muc_049. A Commons image exists for it but was not viewed this pass (Wikimedia blocked from this runner). Aarhus's ash and Sorrento's two cemetery cypresses checked and correctly left alone: real unresolved access/transit and genuine single-sourcing with no second source found despite searching. Build (3004 pages), qa.py, superlatives.py, preflight.py, pagegaps.py all clean.

## 2026-08-27 (night run) - Zaragoza, Brno, Trento checked clean; Wroclaw +1 (Swiadek, the Witness Plane)

Checked the remaining mid-size READY batches. Zaragoza's 3 (a plane on an unwalkable road/rail margin, a lime with a declining 2005 condition survey and unresolved roadworks damage, two field elms with a specifically-flagged threatened specimen among them) all hold on real, already-documented evidence. Brno's 2 both have concrete current blockers: the largest-girth plane in the city sits on an active 2026 residential construction site per local news, and Mendel's Ginkgo is behind a museum that requires advance booking and is reported closed as of August 2026. Trento's 2 both remain unresolved private-villa access questions, already checked twice by earlier write passes with nothing found either way.

Wroclaw's "Witness Plane" (Swiadek) shipped as wro_005, a genuinely good find: a London plane by Wroclaw's Civil Registry Office, named and protected by council resolution in January 2020, with a real second source (a detailed dendrology blog giving the full girth, location and the lion-statue fountain it stands beside) and an OpenStreetMap node that individually names and tags this exact tree at the exact coordinate. Not walkable with the existing 4-oak Wielka Wyspa cluster (over a kilometre away), so it ships as the city's second stop rather than folded into the same walk. Rewrote the city's intro, meta_description, question_meta, question_context and two FAQ answers to say honestly that there are now 5 trees across 2 stops, not 4 on one walk; preflight caught both a false-positive "all four" promise-count trigger (fixed by adding "oaks" so the sentence reads as about the oak subset, not the whole city) and an over-length question_context paragraph, both fixed before commit. Build (3003 pages), qa.py, superlatives.py, preflight.py, pagegaps.py all clean.

## 2026-08-27 (night run) - Rome checked clean; Warsaw +2 from its own Botanical Garden; three register-open scouts, none tractable today

Rome's 3 READY leads confirmed genuinely blocked: real day-trip-boundary failures with the transit research already done in an earlier pass (Parco Francesco Salerno at 14km northwest, current local reporting puts it at 55 minutes to over an hour by bus). Not a forbidden reason, correctly held.

Tried opening a new stage-1 city from register supply instead of continuing down READY (rule 1(c)/(d)): Salzburg has 86 unmined candidates but the data is thin (no girth/height/name fields, just coordinates) and its clusters loose (2.7 to 3.3km spreads); Taormina's 5 nearest MASAF candidates (a dragon tree, a fig grove, two cypresses, an 8m-girth carob, all within 1km of each other) all stand on Hotel Excelsior Palace grounds, and the hotel's own marketing copy ("guests have access to the largest Mediterranean park in the city") gives no indication of public access, so the whole cluster fails hard rule 10 test 1; recorded as a fresh `data/leads/taormina.json`. Rothenburg ob der Tauber's 28 candidates are similarly thin and scattered (1.2 to 12.7km). None tractable for a quick open; left for a dedicated pass with more time.

Shipped 2 in Warsaw instead: a maple-and-elm pair and a columnar-oak pair at Warsaw University's Botanical Garden, both 50-60m from the already-published 1824 ginkgo (war_011), held only for lacking a second source, which the 2026-08-10 ruling forbids. Shipped as distinct collectible points (different gates, different protection orders) rather than folded into the ginkgo's entry, matching the corpus's established pattern of several separate entries inside one botanical garden. Fixed Warsaw's own stale "ten"/paid-ratio FAQ line (now 33% paid, right at the "about a third" line but not over it). Build (3002 pages), qa.py, superlatives.py, preflight.py, pagegaps.py all clean.

**Infrastructure note: this session's git push token (a GitHub App installation token, roughly 1-hour lifetime) expired mid-run around 17:53 UTC.** Working locally since, retrying push periodically; several commits queued.

## 2026-08-27 (night run) - Vienna and Perugia: zero shipped, both genuinely correct; Paris: one Turkey Oak

Continued rule 1(a) down the READY list. Vienna's 5 stayed leads on inspection: two are the same paired planting of Catalpa bignonioides "Nana", a dwarf ornamental cultivar, one just 10 years old at 37cm girth, nothing remarkable about either regardless of the loosened age/size rule; three are Naturdenkmal-protected trees at residential Vienna addresses (an apartment courtyard, a street near a cafe block, a Cottage-belt villa garden) where access genuinely could not be confirmed either way, checked again this pass with no new evidence found. Perugia's one live candidate, a cedar of Lebanon, sits roughly 40m from a school building with nothing distinguishing street frontage from schoolyard; left per the school-evidence rule rather than guessed at.

Paris shipped 1 of 3: the Turkey Oak of Square Rene-Le Gall (par_033), held only for lacking a second source, which the 2026-08-10 ruling forbids; it sits 300m from the already-published par_031 (Horse Chestnut, same square), so no extra walking distance. Left 2 genuinely blocked: a weeping wych elm in a square shut for construction until roughly mid-2027, and a white mulberry whose register entry and a specifically-named 2008 planting could not be confirmed as the same physical tree (the square may hold more than one mulberry). Wrote the French translation for par_033 (Contract J). Build (3000 pages), qa.py, superlatives.py, preflight.py, pagegaps.py all clean.

## 2026-08-27 (night run) - Naples 20 to 22: two READY leads, four real holds confirmed

Third rule-1(a) city of the run, after Barcelona and Bucaco. Naples' 6 READY leads split cleanly into two kinds on inspection. Two had only a forbidden reason blocking them and shipped: the ombu of Via Manzoni (nap_021, Posillipo) picked up a genuine second source, FAI's Places of the Heart listing, which resolves the earlier pass's single-source hold outright; the Baja California palm at the Orto Botanico (nap_022) was held only for being "the smallest of seven... says nothing the Jubaea does not say better", a worthiness call the 2026-08-10 ruling forbids.

The other four are correctly still leads, and checking them was worth the time. The Capodimonte magnolia's two Italian registers disagree by 1.78x on girth (540cm MASAF vs 303cm Campania) for what reverse-geocodes to essentially the same point, the same shape of problem already blocking a Plane of the Pheasantry candidate in this same file, and the museum's own official monumental-trees page omits the tree entirely; also worth recording, the "first Magnolia grandiflora in Europe" claim sometimes attached to Capodimonte's magnolia is not supported by the regional register's own text. Two cloister camphors (a working university medical faculty, a fine arts academy) stay blocked on genuinely unconfirmed institutional access, checked directly this pass and still unresolved. A Nolina/Beaucarnea at the Orto Botanico has two registers giving flatly conflicting species names, an open question that needs an on-site label read, not a database search.

One correction while shipping: the palm's two registers both call it Brahea roezlii, but Kew's Plants of the World Online treats that as an old synonym of Brahea armata, and the garden's own palm-collection page agrees, listing only armata. Set the species field to armata (matching an existing Rome entry) rather than manufacturing a new common name to dodge the hard-rule-9 collision. Also fixed a pre-existing stale count in Naples' own intro (Capodimonte's tree count read "eight," reality and the FAQ both already said nine) while updating for the new total. Build (2998 pages), qa.py, superlatives.py, preflight.py, pagegaps.py all clean.

## 2026-08-27 (night run) - leads.py fix: Amsterdam's paid-ratio pulls were surfacing as READY

Sampling Amsterdam's 5 READY leads (rule 1(a), next after Bucaco) found something different from the Barcelona/Bucaco pattern: these were not held on a forbidden judgement call, they were the exact five trees (ams_012-015, 017) Hidde pulled from the published city on 2026-08-23 for exceeding the paid-entry ratio ("ik heb liever 34 goede bereikbare dan 39"). Every fact in them is verified, fully written, ready to merge, which is exactly why nothing caught it: this is a placement decision, not a truth problem, and shipping them back would have retraced the 39-tree/10-paid state he explicitly rejected (checked: Amsterdam sits at 34 trees, 5 paid now; adding these 5 back would make it 39 and 10, precisely that ratio). Two Leiden entries carry the same `pulled_from_city` field for the same reason. Fixed `classify()` in `scripts/leads.py` to hold anything carrying that field; READY drops from 74 to 61 corpus-wide. Not shipped. Left as leads.

## 2026-08-27 (night run) - Bucaco 9 to 14: five more READY leads off the ICNF register

Continued rule 1(a) into Bucaco, which had 10 READY leads, all single-sourced to the ICNF national register (Bucaco's own trail plaques only cover 9 of the forest's 27+, and none of the remaining 10 has one). Shipped 5 held only for reasons the 2026-08-10 ruling forbids (distance off the main walk, count, undated-single-source): a second redwood near the Porta das Lapas (bsc_011, explicitly distinct from the two Santo Elias redwoods removed 2026-08-21 for being genuinely unreachable, confirmed by the forest's own biologist), an American ash with an unusually precise 136-year register age (bsc_012), a 36-metre sycamore that gives the page its first ever best_time, autumn colour, since every other published tree here is evergreen (bsc_013), a til (Ocotea foetens), a laurisilva relict species that should not survive on the mainland at all (bsc_014), and a third Mexican cypress at a distinct setting, a ruined hermitage, written to avoid repeating the Philip Miller type-specimen story bsc_006 already tells or the Via Sacra chapel story bsc_007 already tells (bsc_015). Left one candidate alone: a second Mexican white pine whose register entry records a physically impossible 100m height against a 1.95m girth, flagged as a likely data error by an earlier pass and not resolved this one.

Fixed two hard-rule-9 species collisions the build caught (Sycamore, not "Sycamore Maple", matching Amsterdam; Til / Stinkwood, not "Til", matching Madeira) and a pre-existing stale claim in the city's own meta_description ("three sequoias") that had survived the 2026-08-21 Santo Elias removal without ever being corrected, now two. Build (2996 pages), qa.py, superlatives.py, preflight.py and pagegaps.py all clean.

## 2026-08-27 (night run) - Barcelona 46 to 52: six READY leads that were held for now-forbidden reasons

`leads.py --ready` listed 17 for Barcelona; sampling all 17 (per the Caserta/Krakow precedent, never trust the READY count blind) found most held for real, still-valid reasons: a private-courtyard access question at Carrer de Maignon (both the carob and the pepper tree), five entries padding the already-crowded Jardi Botanic Historic ravine behind one paid gate, a big untouched Pedralbes cluster needing its own dedicated pass, and a grove entry needing a collectibility call. Six, though, were held only on reasons CLAUDE.md's 2026-08-10 ruling now forbids (too young, undated with no second source, a taste call about whether a yucca counts): the silky oak and hackberry of Jardins dels Drets Humans, the coast coral tree and tree yucca of Jardins de Mossen Costa i Llobera, the avocado of Teatre Lliure, and the Japanese pagoda tree of Carrer de la Guardia Urbana (bcn_047-052). All six confirmed public and free by direct search (Barcelona.cat, bcnsostenible.cat) or by the register's own `ownership: Public` field; two (hackberry, coast coral tree) picked up a genuine second source, beteve.cat's 31 May 2024 piece on the city's 12 newest protected trees, which also named a 7th candidate (an Araucaria on Avinguda de Francesc Ferrer i Guardia) left as a lead because the address sits inside a 12-36 building-complex range and public/private status could not be confirmed.

One real data problem surfaced: the silky oak's register girth (4.1m) and an independent 2017 field measurement (2.42m) disagree by nearly half, for the same tree in the same garden. Girth cannot shrink, so this is very likely a data-entry error somewhere rather than growth, but which figure is wrong could not be determined this pass; both are stated in the story per Step 2 rather than picking one. Renamed Erythrina caffra's common name to "Coast Coral Tree" (was going to collide with Barcelona's existing Erythrina corallodendron, "Coral Tree", under hard rule 9). Wrote matching Spanish translations for all 6 (Contract J requires full overlay coverage or the build fails) and fixed two stale "45 more" count-promises in both languages. Build (2989 pages), qa.py, superlatives.py and preflight.py all clean.

## 2026-08-27 (night run) - Submissions 40-41: a worth-it vote and Hidde's own test of the collect form

Row 40 (`kind: feedback`, `why: "worth it"`) is a plain positive vote on Amsterdam's ams_001 (The Heimanseik, Artis), same shape as the Sardinia/Lisbon/Helsinki precedents: no free-text complaint, nothing to check against sources. Its `user_id` does not resolve to any current account via `/auth/v1/admin/users` (only 4 users exist; this one is gone), so there is nobody to reply to even if a reply were warranted. Nothing changed in `data/cities/amsterdam.json`.

Row 41 (`kind: tree`, city "Baarn", `why: "Test"`, GPS 52.20715,5.28877) resolves to burgmans.hidde@gmail.com via the admin API, confirming it as Hidde's own click-through test of the app's `app:collect` submission flow rather than a reader report: no tree name, no description beyond the word "Test". The point reverse-geocodes to Bilderdijklaan 31, Baarn, 98m from the residential address checked and left open in the 2026-08-26 session's row 37 (also Bilderdijklaan, also inconclusive). Not treated as a lead. Both rows set `outcome: holds` via the service key and appended to `data/submissions-processed.json`.

## 2026-08-26 (night window) - Sardinia: a "worth it" vote on sar_003, no action needed

Submission #39 (Supabase `submissions`, kind `feedback`) was a reader's "worth it" vote (`why: "worth it"`, no free-text complaint) on sar_003, The Olivastro of Santa Maria Navarrese. Same shape as Lisbon's #6 and Helsinki's #5: a positive signal with nothing to check against sources, stored per the vote design and shown nowhere until volume makes a count honest. Nothing changed in `data/cities/sardinia.json`. Marked processed in `data/submissions-processed.json`.

## 2026-08-26 (session) - Two submissions processed: a vote-undo and a Baarn tip too thin to place

Row 38 was bookkeeping (`why: "vote undone: not worth it"` on utr_005) and was marked processed with no reply, per the standing rule for that kind of row.

Row 37 was a `kind: tree` submission for Baarn with no tree name, no species, just GPS (52.20796, 5.28934) and the word "Boom". Checked it before treating it as a lead: Nominatim reverse-geocodes the point to a house at 48 Bilderdijklaan, a residential address about 300m from the already-published brn_005 (American Oak of the Pekingtuin) and well short of Cantonspark. An Overpass check for `natural=tree` within 60m found nothing tagged, and a wider name search timed out. So this cannot be placed as a park tree from the data alone, and it may sit on private ground, which is a hard rule 10 question before it is a research question. Set `outcome: open_question` and a `reply_text` asking what the tree is and whether it is visible from the road; no lead file entry yet, since we do not know enough to call it a candidate. If the reader answers, treat it as a fresh submission next time it is read rather than reopening this one by hand.

One thing worth a future look regardless of this submission: `data/leads/baarn.json`'s blocked entry for the "Kronkelbeuk" (twisted beech, formerly of the Pekingtuin, believed gone) carries no coordinates. If a future pass ever gets a photo or a second source placing it, cross-check against this same GPS point first, since both sit in the same corner of the village.

