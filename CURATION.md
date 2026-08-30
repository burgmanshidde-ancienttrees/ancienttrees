

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-08](archive/CURATION-2026-08.md)
- [2026-07](archive/CURATION-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.

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

## 2026-08-23 - Finished an abandoned write claim: Warsaw +2, Berlin +1, Turin held

A prior attempt this same window claimed berlin, warsaw and turin for a write pass at 08:19, then never touched them, doing unrelated work instead and leaving the claim standing. `leads.py --ready` showed 3 candidates each in all three, but most turned out thinner than the READY label suggests (that check only confirms name+species+position, not sourcing or access), so this pass verified each individually rather than writing all 9.

**Warsaw (+2, 7 to 9):** The Szustra Oaks (war_009, five oaks registered as one 1978 designation) and the SGGW Oak (war_010, declared 1974, standing on the site of the university's original 1923-1956 Mokotow campus before it moved to Ursynow). Both single-sourced from the register, both flagged, second sources used only for setting/access (the park's own page and zabytek.pl for the Szuster estate; SGGW's own history page for the campus). A third Warsaw lead, the Karol Oak, stayed a lead: far from the existing cluster and never researched past the register.

**Berlin (+1, 18 to 19):** The Copper Beech of the Fraenkel Garden (ber_019), Naturdenkmal ND 5-56/B in the public Landhausgarten Dr. Max Fraenkel at Kladow (reopened to the public 2016). Register point sat 270m from the garden's own mapped grounds, so the pin uses the garden's centroid instead, marked approximate. Added the missing German translation entry (data/i18n/de/berlin.json), since the DE build fails hard on any untranslated tree. A second Berlin lead, an oak at Fuerstenbrunner Weg 30, turned out to sit in the Villenkolonie Westend, a private villa district (OSM classes the point a residential house); blocked on hard rule 10, no evidence the plot is public ground. A third, a weeping-beech-and-common-beech pair sharing one averaged coordinate that is actually ~400m from each in reality, stays a lead: publishing one pin for two trees 400m apart would fake precision.

**Turin (0, still 10):** Both candidates researched turned out not shippable. The Plane of Parco di Villa Rey is on the grounds of ASI's (Automotoclub Storico Italiano) national headquarters, open only for scheduled FAI/Open House events or by appointment, not walk-in public; blocked on hard rule 10's first test. The wide plane east of the Po (reg_id 006/L219/TO/01, 640cm girth, oddly short at 14m, likely pollarded) still has no name and no second source; a reverse geocode of its coordinate returned "Villa Rey" as the nearest OSM feature but the point sits 1.8km from Villa Rey's own registered tree, so that is probably just sparse tagging on the Sassi hillside rather than evidence of the actual site. Left as a lead with the geocode note for whoever picks it up with better local knowledge.

Released all three claims. Build and qa.py both pass (qa's one remaining failure, sitemap lastmod, is the pre-existing shallow-checkout environment issue, unrelated). preflight.py and superlatives.py both clean.

FOR HIDDE: nothing blocks. The 8 unclaimed minutes this window's first attempt left on the table went into finishing what it started rather than opening anything new.

## 2026-08-23 - Seville deepened 20 to 37 from its own municipal catalogue

`leads.py --ready` showed 26 candidates sitting in `data/leads/seville.json`, all from the city's own 2022 Inventario de Arboles Singulares (the same municipal catalogue four already-published Seville trees, sev_017 to sev_020, already draw on), each carrying real dendrometry and vitality fields rather than a bare species-and-location line. Seville clears the demand bar this rung requires (50 ten-day impressions), so deepening an already-at-target city (20/20) was in scope. Wrote 17 of the 26: 5 thicken the Parque de María Luisa cluster (an araucaria, two planes, a stone pine, a bald cypress), 4 more join the Real Alcázar cluster (a windmill palm, a bougainvillea trained as a small tree, a European fan palm, a cycad correctly described as not actually a palm), and 8 stand alone across the city (a cemetery cypress, a 42 m eucalyptus with two named pests, a Triana fig, a mulberry by an Expo-park farmstead, a Senegal date palm, a university-campus Canary pine, a 32 m tipu tree, and Parasenegalia visco, a South American species almost never planted in Europe). Held back the remaining 9: 7 rated only "Regular" condition and one (a lagunaria) the leads file's own note says needs a second source before it ships, both left for a future pass; the last (a ficus at a private nursing home's garden) was dropped outright, since Hermanitas de los Pobres' grounds fail hard rule 10's access test. Species naming needed one fix mid-build: Chamaerops humilis had to match Padua's existing "European Fan Palm / Saint Peter's Palm" rather than a shorter name I'd written, per hard rule 9. Fixed the city's question_meta and one FAQ answer, both of which still counted the old 20. All 17 single-sourced from the catalogue, flagged, no photos.

FOR HIDDE: nothing blocks.

## 2026-08-23 - Four Dutch cities open at once: Heerlen, Oss, Roosendaal, Sittard-Geleen

A write pass on `python3 scripts/leads.py --ready` found four fully-verified, story-less LRMB register files sitting staged (`data/research/{heerlen,oss,roosendaal,sittard-geleen}-verified.json`), 30 candidate trees between them, all above the 4-tree floor. Wrote stories for all four and published them as new cities, 28 trees total.

**Heerlen (8):** two oaks on the wooded Terworm/Eyckholt estate grounds, a neighbourhood oak from the 1920s mining-colony era, a lime banded to the 1600s with no other history recorded, the plane everyone in town calls the Oak of Terworm (probably planted in 1749 for an heir's birth), a tulip tree in a former miners' park, a castle-drive ginkgo, a town-hall catalpa. hee_003's species had to move from "Oak (Quercus sp.)" to "Oak (Quercus, species not established)" mid-build: hard rule 9 caught it colliding with Austin's unrelated "Live Oak (Quercus sp.)" entries under the same Latin string.

**Oss (6):** two village limes and a named-by-year (1928) sycamore in Macharen, a churchyard beech in Haren, a horse chestnut in Oss itself, and Megen's "Lulboom", a 1937 royal wedding lime the register itself records twice as adjoining entries; folded into one story rather than two, since a visitor sees one planting.

**Roosendaal (7):** a rare Oriental plane and a horse chestnut sharing De Kring square, a catalpa and a London plane framing one building on Burgerhoutsestraat, a beech behind a restaurant, a fast-growing poplar on a car park, a second chestnut by the Van Loonpark pond. Its own park lime, the register's original fifth candidate there, was declared dead in 1998 per the register's own site_history and never shipped, per the never-dead-trees rule.

**Sittard-Geleen (7):** three Geleen trees tracing the district's mining-era growth (a station red oak, a street sycamore, and an oak the register's own surveyor is rooting for against a housing development on the neighbouring plot), plus a poet's-garden copper beech and ash, and a Stadspark pin oak and tulip tree.

All 28 single-sourced LRMB, all flagged, no photos. Build and qa.py both pass.

FOR HIDDE: nothing blocks.

## 2026-08-23 - Cork 5 to 13, on a newly-scouted national register

`scripts/scout_next.py --target` pointed at Cork for register scouting (published, but no register supply on file and no scouting verdict, because the register itself had never been logged in `data/register-scouting.json` despite already being live). Found `data/registers/ireland-heritage-trees.json` (Heritage Trees of Ireland, National Biodiversity Data Centre, CC-BY 4.0, 724 trees island-wide) was already imported and in use on 2026-08-08/09 for Dublin, with a working Irish Grid to lat/long converter at `scripts/irish_grid.py`; a first pass here nearly re-imported and overwrote it as a fresh find before the "M" in `git status` (not "??") caught it. Re-used the existing conversion instead. Cork's page already draws on Blarney and Fota, so those two sites' public status was established; checked the register's Blarney/Fota entries against the 5 already-published trees, skipped two near-certain duplicates within 60m (a yew and a Western Red Cedar, same species, same site as cor_001/cor_002, confirmed by converting their coordinates), and shipped six new Fota trees (a camphor tree, a spiral-needled Japanese cedar cultivar, a Canary Island date palm, a New Zealand tanekaha, a holm oak, a coast redwood) plus two new Blarney trees (a Cappadocian maple, a beech), all with real converted coordinates. All single-sourced from the register, flagged. Fixed the city's meta_description and question_meta, which still said "five" and "four more". Logged the missing scouting verdict. Two more register clusters (Doneraille Park, The Gearagh nature reserve) turned up but sit 35-40 minutes from Cork city, past the day-trip boundary, so they wait in `data/leads/cork.json`. The register covers all of Ireland and has runway left for Galway, Limerick, Killarney, Kilkenny and Belfast, checked against each city's existing coverage first.

FOR HIDDE: nothing blocks.

## 2026-08-23 - Haarlemmermeer opens with 8, register exhausted

Finished the verify pass CURATION.md's previous entry had dispatched but left unrun: the 6 unmined Hoofddorp/Vijfhuizen/Badhoevedorp candidates from the LRMB register (`data/leads/haarlemmermeer-register.json`). Checked each against hard rule 10: a wingnut on the Markt (kept alive on the municipality's own condition when the shopping centre around it was built), a lime planted for Queen Wilhelmina's 1923 jubilee, a London plane in front of a notary's office (Hoofddorp's oldest registered tree, 1880s), and a weeping beech whose own 2024 register inspection says it "feels very unhappy" squeezed onto a ring-road corner all cleared the access test and shipped. A sixth, a maple on the Nieuwemeerdijk in Badhoevedorp, ships as view-only per the Hobart precedent: private front garden, but the register's own text says it is clearly visible from the road; its story also flags that the register contradicts itself on the planting date (1895 in the descriptive note, 1910-1920 in the structured field). A seventh, a beech at a private garden corner in Hoofddorp, stayed blocked for lack of any visibility evidence (`data/leads/haarlemmermeer.json`). Also set names on the three previously-written Nieuw-Vennep trees, which a prior write pass had left null. City now ships at 8 trees, all single-sourced LRMB, all flagged; no photos. Register supply for this gemeente is exhausted; a ninth tree would need a reader tip or a from-zero web sweep neither of which is warranted right now.

FOR HIDDE: nothing blocks.

## 2026-08-23 - Assen opens with 9, all LRMB register, all flagged

Finished a write pass a prior attempt this window had claimed and left half done (one story written, eight to go, in `data/research/assen-verified.json`). All nine trees come from the Landelijk Register Monumentale Bomen, single-sourced throughout, so every entry ships `curation_status: flagged`. Three share the private Overcingel estate (a horse chestnut in the register's top ereklasse, a hollowed oak with a 27m-to-14m veteran crown reduction, a bald cypress reduced to regrowth after its main trunk broke), two share a hidden pocket garden behind Nieuw Echten reached via a footpath between two front doors on Alteveerstraat (a weeping beech, a copper beech), and the remaining four stand in a deer park, the former Vredeveld estate (now Valkenstijn park), a private front garden visible from Beilerstraat (registered as the heaviest oak in Assen), and the former grounds of the Port Natal psychiatric hospital (now the Wilhelmina Ziekenhuis). No photos (`status: missing` throughout); no `best_time` on the weeping beech, the broken cypress or the two ageing/declining oaks (ass_002, ass_003), since none has a peak worth the badge this year. Build and qa.py both pass; qa's one failure (sitemap lastmod, shallow git checkout) is a pre-existing environment issue unrelated to this city. `data/city-queue.json`'s Assen stub flipped to published/9 trees.

FOR HIDDE: nothing blocks.

## 2026-08-23 (night) - Amsterdam 31 to 39, Zaanstad opens with 4, Haarlemmermeer held at 3

A write pass staged 15 register-sourced trees (a prior verify pass's shelf, all LRMB, all single-source flagged) across three Dutch cities; this session merged the output. Amsterdam gained 8 trees, all in Amstelveen (Broersepark, the Amsterdamse Bos, several street plantings), taking it from 31 to 39; its stale "31"/"21 free" copy and Dutch translation overlay (nl/amsterdam.json) both updated to match, since the build enforces full per-tree translation coverage on any city with an nl file. Zaanstad opened as a new city with 4 trees spread across Zaandam, Westzaan and Assendelft (a cemetery copper beech with a self-contradicting age in its own register entry, a plane that outlived the industrial Zaan waterfront, two declining horse chestnuts), full Contract C copy written from scratch. Haarlemmermeer's 3 written Nieuw-Vennep trees stay held in data/research/, one short of the 4-tree floor (2 of its original 5 register candidates were correctly blocked earlier on access grounds); a follow-up verify pass is dispatched on 6 unmined Hoofddorp candidates (a market-square wingnut, two planes, a weeping beech, two private-garden beeches needing an access check) to open a second cluster and clear the floor.

Also fixed a real bug found along the way: `scripts/city_queue.py`'s regeneration step (not `--next`, which was fine) crashed with a `KeyError: 'basis'` on the two 2026-08-22 stub queue entries for Zaanstad and Haarlemmermeer, which lack the field every properly-scored entry has. Two lines used `c["basis"]` instead of the `.get()` pattern the rest of the function already uses; fixed, queue regenerates clean now that Zaanstad is a live city.

Zero photo hunting or judging this run (night-runner egress rule); all 12 published trees carry an honest `missing` photo status.

FOR HIDDE: nothing blocks.

## 2026-08-22 (night) - Oahu published, 5 trees, all in one garden

A verify pass claimed earlier in the window found 5 trees, all inside Foster
Botanical Garden in downtown Honolulu (a baobab, a Bodhi tree grown from a
Bodh Gaya cutting, a kapok older than the garden itself, a cannonball tree
and a quipo), all within a five minute walk of each other. A write pass
turned them into stories and the city went live at /oahu with 5 of a target
10. No photos yet (all `status: missing`). One tree (hnl_003, the Hillebrand
Kapok) is flagged for an unresolved girth disagreement between two sources,
kept honest in the prose rather than resolved by picking one. hnl_004 (the
Cannonball Tree) has no recorded planting date; the story asks the reader
for it rather than hedging around the gap. Roughly 51 more register-listed
Exceptional Trees sit within 20km, still unmined by any pass (`passcheck.py
--brief Oahu`), so this city has plenty of cheap runway toward its target
of 10 for a future verify pass.

## 2026-08-22 (night) - A tree named after the wrong genus, and it needs the redirect work first

**kyo_016 is called "Chinkapin oak (Sudajii) of Omiya Gate" and is not an
oak.** Its own `species` field says Japanese Chinquapin, *Castanopsis
sieboldii*. Chinkapin oak is *Quercus muehlenbergii*, a North American oak,
and Castanopsis is not a Quercus at all. The name and the species field on the
same entry contradict each other, and the name is what a reader sees as the
page title. Sudajii is correct and is the Japanese name for the Castanopsis.

**Not fixed, and the reason is the same one blocking the umlaut URLs.** A tree
slug is derived from its name, so correcting this moves a published, indexed
URL, and the redirect machinery covers city slugs only. This now belongs with
the 17 tree URLs missing a letter (the German ß and Icelandic eth entries
recorded earlier today): one small feature, tree-slug redirects, unblocks all
eighteen fixes at once. Doing any of them without it trades a factual error
for a dead link, which is the worse of the two.

**Fixed in place, since neither touches a URL:**

- `kyo_013` sent visitors to "Keihan Marutamachi Station", which does not
  exist. The Keihan station is Jingu-Marutamachi; plain Marutamachi is the
  Karasuma subway stop roughly a kilometre west, on the far side of Kyoto
  Gyoen. A directions field pointing at the wrong station is the one class of
  error this project says it cannot afford, so this one did not wait.
- `kyo_015` said Kyoto Gyoen has been public ground "since the court left for
  Tokyo in 1877" while `kyo_012` dates the court's departure to 1869 and the
  clearing of the plots to 1877. The two events are separate now.

**Reported by the Kyoto pass and NOT acted on, because each needs a source in
hand rather than a judgement:**

- `kyo_001` "Hanayama's former minister Ieatsu" is very likely Kazan'in Ieatsu,
  a court noble, with 花山院 read as a place rather than as his surname.
- `kyo_009` "fuseki-dai sugi" mis-romanises fukujo-daisugi, and "Goshomigoyo"
  matches no term the pass could identify.
- `kyo_015` names "the Kyoto nurseryman Sano Toujiro" while `kyo_005` names
  "Sano Toemon XV" of the same sakuramori family. If those are one family, two
  of our pages are quietly telling one story about two people.
- `kyo_018` says another tree is "about a kilometre and a half north"; our own
  pins put it 945 metres away. Both pins are approximate, so this may be the
  pins rather than the prose.

## 2026-08-22 (evening) - The Vienna duplicate was invisible, and 17 URLs are missing a letter

**The vie_024 / vie_028 duplicate is resolved, and it turned out to cost
nothing.** Both entries carried the identical name "The Plane of Alser
Strasse", and `treeSlugsForCity` derives a slug from the NAME, so the two
collided on one URL and only one of them ever rendered. Checked against the
live site: `/vienna/plane-of-alser-strae` serves vie_028's story, and vie_024
has never had a page at all. So retiring vie_024 moved no published URL and
hard rule 3 never applied; the staging note from this morning was written
before anyone looked at what the slug function actually does. Removed from the
city file and from the German overlay. Vienna is 30 trees.

**Finding it exposed a bigger one. `slugify` silently drops any character
NFKD cannot decompose, and German ß is one of them.** The function normalises
to NFKD, strips combining marks, then strips everything non-ASCII. Scandinavian
å and ö survive that, because NFKD splits them into a letter plus a mark. ß has
no decomposition, so it is simply deleted, and "Strasse" becomes "strae".

17 live tree URLs are affected: Munich 11, Reykjavik 3, Vienna 2, Copenhagen 1.

    munich/norway-maple-of-herrnstrae     should be  ...herrnstrasse
    vienna/cemetery-plane-of-singerstrae  should be  ...singerstrasse
    reykjavik/whitebeam-of-vikurgarur     should be  ...vikurgardur   (eth)
    reykjavik/spruce-of-elliaarholmi      should be  ...ellidaarholmi (eth)

The fix is four lines, a transliteration table applied before normalising:
ss for ß, o for ø, ae for æ, oe for œ, l for ł, d for ð and đ, th for þ. Polish
ł has no live victims yet and will the moment a Wrocław street name reaches a
tree.

**Not applied here, deliberately, and this time hard rule 3 really does
apply**: unlike the duplicate, these URLs exist, are in the sitemap and are
what Google has indexed. Changing them needs redirects, and the redirect
machinery that exists (`RENAMED_CITY_SLUGS` in site/src/lib/redirect-map.ts)
covers CITY slugs, not tree slugs. So this is a small feature plus a data
migration, not a four-line patch, and it deserves its own session rather than
the tail of a long one.

Worth doing though: "leinthalerstrae" is not a word in any language, nobody
searches it, and it reads as a broken page to a German speaker, which is the
audience the German pages were just built for.

## 2026-08-22 (later) - Reader-facing fields were carrying notes we wrote to ourselves

The Palermo translation pass found it, and it is the most embarrassing thing
in today's batch because it was live and visible: the `access` and
`transport` fields render straight to visitors, and in 21 cities they were
carrying instructions to the writer and internal tree ids.

The worst examples, all live before this:

- `pal_010` access: "Confirm current opening hours and whether the fig's part
  of the grounds needs a booked visit before publishing a specific time."
- `pal_016` access: "State the caveat plainly and tell readers to check
  current hours before visiting rather than quoting an unverified schedule."
- `gnv_002`, `gnv_003`, `gnv_004` access: "Not confirmed this pass." /
  "Not established this pass."
- `com_006` access: "Same schedule as the Villa del Grumello cedar (com_005)".
  A reader has no idea what com_005 is.

63 fields across 18 cities were cleaned mechanically: internal ids stripped,
"this pass" removed, spacing repaired. Toulouse (11), Padua (10) and Nuremberg
(9) were the worst. Nothing factual changed; every hedge survives, it just
stopped narrating our own process, which CLAUDE.md's ratchet already lists as
one of the seven things that became build checks.

**And that is the finding: the build check did not catch this.** qa.py checks
rendered text for builder-speak, and these fields went through it. Worth a
look at whether it only checks story prose and not the short fields.

**A second checker gap, same session.** `scripts/superlatives.py` reports
"468 superlative claims, no two trees claiming the same crown" while
`mad_005` says the cypress is "both the oldest and the tallest tree" in the
Royal Botanic Garden and `mad_006` said the elm "wins on height" there and
called it "the garden's tallest resident". The checker matches phrasing, so a
paraphrase walks straight past it. Fixed the content (the cypress states 32
metres flatly, the elm only "over 30" with the measurements admitted to
disagree, so the elm's claim yielded), but the check still cannot see the
class.

That makes two contradictions in one day that a translation pass found and an
automated check missed, after the Paris girth pair. The pattern is that our
checks match strings and the errors are semantic. Worth deciding whether the
fresh-eyes reviewer should be pointed at superlatives specifically.

**Still open from earlier today:** vie_024 and vie_028 remain one tree under
two ids, staged because retiring an entry moves a published URL.

## 2026-08-22 - Six translation passes found four errors in our own English

Six overlays landed in one batch (Italian Rome, Dutch Amsterdam, German
Vienna, Portuguese Lisbon, French Paris, Japanese Tokyo). The translations are
the smaller half of what they produced. Rendering a story into another
language turns out to be a fresh-eyes review of the English, because a
translator cannot skim: every clause has to be understood before it can be
carried across, and the ones that do not survive that are the ones that were
never quite true.

**Fixed the same session, all live before this:**

- `tokyo` intro said the oldest tree "predates the Kamakura shogunate". Our own
  figure for tok_001 is 750 years, so about 1276, and the shogunate began in
  1185. The tree cannot predate it. Now "dates from the Kamakura period",
  which our own number supports.
- `tok_005` called Tokyo Tower "a 1930s landmark". It opened in 1958. The
  sentence has been rebuilt around the real date.
- `par_005` said the Monceau plane has "a waistline of seven metres" while
  `par_014` said "the thickest plane in Paris, in Parc Monceau, measures eight
  metres around", about the same tree. Both were wrong AND they contradicted
  each other on the site. par_005's own notes carry the Ville de Paris
  register figure, 645 cm. Both now say that.
- `par_009` said a tree planted in 1840 "was a 30 year old tree" in the 1860s.

**Not fixed, needs a check I cannot do offline:**

- `tok_009` credited the Meiji Jingu Gaien avenue to "Origeshi Yoshinobu",
  which is not a plausible romanisation. The Japanese pass reads it as
  Orishimo Yoshinobu (折下吉延) with high confidence, and that is very likely
  right, but I could not verify it from our own sources and hard rule 2 does
  not bend for a likely-right name. The garbled name is REMOVED rather than
  replaced, so the sentence now says "the landscape architect who laid it
  out". Restore the name once somebody confirms it; the Japanese overlay
  carries 折下吉延 already.

**BLOCKER-class, staged for the next session because it changes public URLs:**

- `vie_024` and `vie_028` are the same tree. Identical coordinates to the
  metre, the same Naturdenkmal register_id 3257866, the same Baumkataster
  baum_id 126884, the same 1894 planting and the same 315 cm girth, both named
  "The Plane of Alser Strasse". A visitor can collect one trunk twice, which
  is the exact fault the Potsdam and Berlin Pfaueninsel oaks were retired for
  on 2026-08-16. It was NOT retired on the spot because removing an entry
  moves a published URL, and hard rule 3 puts that above speed; it needs the
  slug and redirect handled deliberately rather than at the end of a long
  session.

**Two contradictions the passes flagged that are real and still open:**

- `amsterdam`: the intro calls the 35 m elm the city's tallest tree while
  ams_003 gives a poplar 38.5 m and leaves "is anything taller" open. Both
  renderings are faithful to the English, so the Dutch page now carries the
  same tension.
- `vienna` vie_006 asserts the 1783 reading in two sentences after presenting
  1783 versus 1876 as an open dispute. The German attaches those sentences to
  the older reading explicitly, which is better than the English does it.

**And a schema gap worth naming before it is discovered as a bug:**
`how_to_recognise` and `best_time` have no slot in the overlay format, so those
reader-facing lines render in ENGLISH on a translated page. Five Paris trees
carry a recognition line, and par_032's is load-bearing ("The square has two
enormous planes. This is the one the register pins..."). The French pass
folded three best_time moments into its prose as a workaround, which is a
reasonable stopgap and not a fix.

## 2026-08-22 (session, continued) - Vienna 28 to 31: Rathauspark's third plane, past its 30 target

Three trees, all confirmed-public: vie_029 completes Rathauspark's three-plane 1973 protection set (an earlier pass held it back as "padding"; it is the third of a designation that already exists as a trio, not a fourth plane added for its own sake). vie_030 (Black Pine, Ebner-Eschenbach-Park) and vie_031 (Sessile Oak, Prater/Belvedereallee) both needed checking against several genuinely private neighbours in the same register clusters (Wahring courtyard trees, Meiereistrasse sculptor's-studio planes) before shipping; those stayed blocked with sourced reasons in data/leads/vienna.json. Fixed two stale count promises preflight caught (meta_description "Twenty-eight", question_meta "twenty-six more"). Walk now 10.6 km (up from 10.1, still multiple clusters across a large city, each cluster itself tight). Vienna is now 1 over its 30 target, which CLAUDE.md treats as normal, not padding, since nothing was added to hit a number.

## 2026-08-22 (session, continued) - Haarlem 9 to 13: the Statenbolwerk stretch of De Bolwerken, one storm-felled beech found and blocked

## 2026-08-22 (session, continued) - Haarlem 9 to 13: the Statenbolwerk stretch of De Bolwerken, one storm-felled beech found and blocked

A verify pass tightened Haarlem's existing Kenaupark cluster rather than widening the walk: four new trees (haa_010 to haa_013) all sit 220-375 m from the nearest existing tree, in the Statenbolwerk section of De Bolwerken, the older (1828) Zocher-designed green ring the Kenaupark cluster (1865) sits inside. A ginkgo added to the lawn in the 1910s, an oak pair marking a path entrance (species left honestly undetermined, robur or petraea, since the register does not say), a four-beech ensemble, and a Caucasian wingnut in a private villa garden shipped as view-only per hard rule 10 (visible from the public footpath, register itself marks it visitable/visible, access line says plainly what a visitor does and does not get).

The pass also caught a real thing worth recording: a separate, single copper beech 200 m away at Statenbolwerk 2 was blown down by storm Eunice in February 2022 (two independent Dutch sources), and is now correctly BLOCKED in data/leads/haarlem.json rather than sitting there to be rediscovered and nearly shipped by a future pass. A second, similarly-old green beech nearby was left as a lead rather than verified, on the writer's own judgement that confusion risk with the fallen tree could not be ruled out this pass.

Updated two stale count promises preflight.py caught (question_meta "the full nine", an FAQ answer claiming "all nine stand" free and open): now 13, and the FAQ answer now says honestly that 12 of 13 are open access, the wingnut being the one view-only exception. Walk still spans 3.3 km, unchanged: the new trees tightened the cluster rather than widening it. Build, qa.py, superlatives.py and preflight.py all clean.

## 2026-08-22 (session) - Florence 22 to 23: one Boboli Gardens cypress, oldest-tree pin kept on the documented yew

A verify pass steered away from Florence's already-exhausted cheap leads (Bobolino stone pine etc., checked twice on 2026-08-21 and still single-sourced) and toward fresh, unmined MASAF register candidates instead. It found one: flo_023, The Cypress of the Boboli Gardens, Mediterranean Cypress, 357 cm girth, verified via matching MASAF/RAMI register codes 9 m apart. RAMI's own register states an age of "roughly 375 years, calculated from a registered birth year" but the underlying documentary basis was not found independently, so `curation_status: flagged` and the story hedges the figure as an estimate rather than a fact.

That estimate (age_max 400) technically exceeds flo_001's documented 306-year yew, which would have silently flipped the /florence/oldest-tree page's answer to a hedged register guess instead of a precisely documented 1720 planting. Set `oldest_tree_id: "flo_001"` explicitly (same mechanism Amsterdam's cycad uses) rather than let the raw age_max win: flo_001's whole point, already made in the page's own question_context, is that its age is not a guess. Build, qa.py and superlatives.py all clean (qa's one sitemap complaint is the sandbox's shallow git clone, unrelated).

Also this session: redacted Hidde's personal Gmail address from LOG.md (same PRINCIPLES.md #10 issue REVIEW.md flagged in CURATION.md and a run had already fixed there), wrote the Norway Maple species page intro (the one page gap pagegaps.py found), ran a free photo API sweep (40 more trees checked), and dispatched Haarlem and Vienna verify passes (register deepening, both still running/pending write at time of writing).

## 2026-08-22 (session) - The nine most-visited tree pages, checked; Newton's pin was 180 metres wrong

Hidde asked whether the pages people actually see carry errors. A verify pass
took the nine tree pages with the most Search Console traffic and checked five
things each: alive, pin, bridge claims, species and age, access. Four real
problems, all fixed the same hour.

**Newton's Apple Tree, Cambridge, is the serious one.** 113 impressions in ten
days, zero clicks, and a pin marked `confirmed` that sat at 52.20689, 0.115113,
an exact six-decimal match for Nominatim's centroid of Trinity College as a
whole. The tree stands outside the Great Gate, about 180 metres east. Two
independent checks agree: the geotag of our own approved photograph of this
tree (Geograph 5599349) and the CB2 1TQ postcode centroid from our own address
line. Moved to the photograph's coordinate. This is exactly the failure the
project says it cannot afford, it survived on a well-read page, and no check we
own would have caught it, because a plausible coordinate inside the right city
looks like every other coordinate.

**Amsterdam's Last Elm of Stationsplein carried an unflagged conflict.** Our
age band (about 120 years) comes from the national register's 1900-1910
planting band; De Correspondent quotes the city's own head tree consultant
giving 1889, backed by a 1906 archive photograph. Fifteen years apart, both
real. Recorded in verify_notes, published age left with the register, neither
picked as winner, per the two-source rule.

**Two smaller ones.** Green-Wood's own great-trees page has 404ed since we
cited it, so the citation now points at the Internet Archive snapshot rather
than nothing; and Singapore's Bodhi tree story said Captain Pearl planted the
hill with nutmeg, where NParks and Wikipedia both say pepper.

**What did NOT need fixing, which is worth as much:** Bath's plane, Malaga's
ficus avenue, the Athens holm oak, Dublin's sequoia and the Parc Monceau plane
all held up, pins included; the Paris one matched the city's own tree registry
to the metre.

Two upgrades left on the table, both cheap and both real: Green-Wood indexes
the sassafras as Section 54, between Forest and Locust Avenues, which would
turn an approximate pin into a confirmed one, and Dublin's sequoia still has no
tree-level coordinate.

## 2026-08-22 (session) - Munich 30 to 44: finished a write pass an earlier attempt in this window claimed and left unwritten

A prior attempt in this same usage window claimed Munich for a write pass (14 register-only leads verified and staged in `data/research/munich-verified.json`) and then stopped after 10 minutes without dispatching the pass. This session picked the claim up, dispatched `write-stories` on the 14 trees (muc_035-048), merged the result into `data/cities/munich.json`, and released the claim.

All 14 come from Munich's 2021 Naturdenkmalverordnung, single-source, no age and no girth on any of them; each ships flagged with an honest invitation for a reader to supply a date or a measurement. Caught and fixed one species-naming slip before merging: the writer delivered muc_035 as "Sycamore Maple (Acer pseudoplatanus)" against the corpus canonical "Sycamore (Acer pseudoplatanus)" (10 existing trees use the canonical form); renamed before merge so hard rule 9 and the build's one-species-one-name check don't trip. `best_time` set on 3 of 14 (muc_037 red oak, muc_040 beech, muc_042 maple), kept scarce since Munich already carries 17 best_times across its other 30 trees.

Build and `qa.py` both clean except one pre-existing false positive: `qa.py`'s sitemap lastmod check fails locally because this sandbox's git checkout is shallow (4 commits only), which flattens every page's last-source-commit date to today; this is a checkout-depth artifact, not a data problem, and doesn't reproduce on the real CI checkout.

Munich: 30 to 44 trees, still one published city, still needs a photo push (14/44 have one). Deleted `data/research/munich-verified.json` (fully merged).

## 2026-08-22 (session) - Nijmegen 11 to 12, one tree, and the rest recorded as leads/blocked

Finished the verify claim the previous attempt in this window left standing
(scout_next --target still said BUILD Nijmegen: 159 unjudged register trees,
nothing to scout). Picked 4 single-tree candidates from the LRMB register
around the centre, all confirmed via the register's own `n_trees` field to
be individual specimens rather than rows: several nearby cemetery entries
(n_trees 4, 12, 14, 28) were excluded before dispatch for exactly that
reason, they are avenue/row plantings, not collectible points.

**Shipped: nij_012, The Wilhelminaboom of Hertogplein** (Lime, species not
otherwise identified). A lime planted 1 September 1898 for Wilhelmina's
coronation, ringed by a wrought-iron fence whose crowns were removed by the
Germans and restored in 1948. Sources genuinely conflict on whether the
tree standing today is the 1898 original: Dutch Wikipedia says the old lime
"has made way for another"; a 2025 local-history blog describes today's
tree without mentioning any replacement; the register's own planted_band
(1880s) predates the 1898 date the narrative sources give. Delivered all
three facts rather than picking a winner, `age_estimate` left blank, marked
`flagged`. This is the bridge-claim trap almost in reverse: rather than
join the facts into a tidy story, the story says plainly that nobody has
reconciled them.

**2 leads, 1 blocked**, all in `data/leads/nijmegen.json`. The blocked one
(a beech on "Beukenlaan", Landgoed Brakkestein) would have been the oldest
candidate in the batch, planted_band 1700-1750, but the register's own
place name and the park's Rijksmonument description confirm it sits on a
beech-lined avenue with no individual recognition, the avenue exclusion
BRIEF_RESEARCH.md names explicitly.

`rijksmonumenten.nl` added to the fetch blocklist: hangs on individual
monument pages, both WebFetch and curl with a browser UA.

**Second pass, same session: Nijmegen 12 to 13.** Two more clusters: the
Brakkenstein manor house (extends the existing Sterrenbos cluster, ~900m
away) and Park Leeuwenstein, a west-side park on the site of a demolished
19th-century villa. The manor-house pair (a chestnut and a beech, both
1830-1840) went to leads, no second source names either individually.

**Shipped: nij_013, The Beverboom of Park Leeuwenstein** (Magnolia sp.,
exact species unconfirmed). Register-dated to the 1880s, roughly 140
years. Its neighbour, the park's giant sequoia, was caught DEAD (fell in
the storm of 18 January 2018, two independent sources) and blocked before
it could ship, exactly the vitality check the register itself cannot do.
Species stays an open question on the page: "beverboom" is old Dutch for
Magnolia, but whether this specimen is Magnolia virginiana or the
Magnolia acuminata a 2023 local survey lists for the same park was not
settled this pass.

**Third pass, same session: Nijmegen 13 to 14.** Two new stops, both
previously unrepresented: Hees (a church square about 3km west of the
centre) and Lent (Nijmegen-Noord, across the Waal, annexed by the city
in 1998).

**Shipped: nij_014, The Pastorie Chestnut of Lent** (Horse Chestnut,
Aesculus hippocastanum). A genuine tree-level match: the national heritage
register's own listing for the parish complex names "an old chestnut tree"
on the specific square the LRMB register also pins by coordinate, not an
inferential join. Not flagged.

Hees's church-square beech and plane (Schependomlaan/Korte Bredestraat)
went to leads: the square itself is confirmed by local history, but no
source names either individual tree, and monumentaltrees.com's own page
for this exact spot 403'd on every fetch attempt. Two more hangs added to
the blocklist: reliwiki.nl and Nijmegen's own municipal tree WFS endpoint.

**Photo viewing pass, same session: Nijmegen's first photograph.** Ran
`photo_hunt.py --city nijmegen` (free, API-only) to seed candidates, then a
session viewing pass judged 42 candidates across the city's 8 photo-less
trees against the Cadiz standard. 1 approved: **nij_009, the Kabouterboom**,
identity settled by hard data rather than by name (the Commons file's own
GPS sits 25m from our pin, and its caption states an 850cm girth, exactly
matching our `girth_cm`). 41 rejected, 0 held. Seven trees (nij_001,
nij_002, nij_003, nij_004, nij_008, nij_012, nij_014) are now documented
Commons dead ends: the nationally-famous names (Julianaboom, Wilhelminaboom,
Sterrenbos) kept returning other towns' same-named trees, and should not be
re-swept without a genuinely new source.

One thing worth a future verify pass rather than a photo pass: two 2020s
photographs of Hertogplein show the square rebuilt with young trees and no
crowned iron fence visible, which is the recognition feature nij_012's story
leans on. Checked it: the fence itself, "sierhek Wilhelminaboom", is its own
listed national monument (monumentenregister.cultureelerfgoed.nl/monumenten/516445),
and the crown-replacement ceremony is a standing yearly tradition on 24
July per the Wonen in Nijmegen blog, so it is not something that gets
quietly removed. Reads as the two photographs simply not framing it,
resolved, no correction made.

Released the Brisbane claim the earlier attempt left standing (558 unnamed
"significant landscape trees" candidates, no names to work from yet, not
today's priority per scout_next). Salzburg's claim belongs to a separate,
still-live night run and was left alone.

## 2026-08-22 (night run) - Submissions 11-36: Hidde's own QA of the rebuilt worthit widget, not reader input

26 new rows in `submissions`, all `kind: feedback`, all from one `user_id`
that resolves to his own account (checked via
`/auth/v1/admin/users`). The pattern makes it unambiguous: rapid vote/undo
cycles on three trees (Rome's rom_001 Ginkgo of Villa Sciarra, Amsterdam's
ams_004 Wertheimpark Wingnut, Utrecht's utr_005 Onder de Linden), several
pairs under 20ms apart, which no human thumb produces. Timestamps land the
same day the WorthIt widget was revised (worthit-js.ts's own 2026-08-21
comment), so this reads as his own click-through test of the toggle/undo/
chip behaviour right after shipping it, not field feedback.

One row (id 14) is a genuine chip click, "report: could not reach it" on
rom_001. Checked against our own data anyway: `access` already says "Free,
open access, Villa Sciarra public park", a well documented public park, so
nothing here suggests the pin or access line is actually wrong. Read together
with the rest of the sequence, this is almost certainly a test click rather
than a real "I stood at a locked gate" report. Not treated as a correction;
no page changed. If a second, distinct report on rom_001 arrives later, per
the standing rule it reopens the question rather than being waved off by this
entry.

All 26 ids appended to `data/submissions-processed.json`. `outcome: holds` was
also set on all 26 rows via the service key by a concurrent run's identical
check; no `reply_text` set on any of them (nothing to answer; the generic
thank-you, if it fires, is harmless since the address is his own).

## 2026-08-21 (session) - Bucaco: the Fundacao's nine plaques, read and merged

The files arrived within the hour: nine PDFs of the Trilho das Arvores Notaveis
plaques (2019, texts validated with the University of Aveiro) and three
photographs. The nine plaques match our nine remaining Bucaco trees exactly,
one each.

**What they gave us.** A measured girth for all nine, which is the field this
project is shortest of (13 trees carried one before today): 240 cm on
Wellington's Olive up to 865 cm on King Regnans. Heights for four. Two facts
worth a story edit later: the cork oak "appears to have never been corked", and
the plaque calls King Regnans the tallest tree in the forest at about 73 m.
Sources and verify_notes on all nine now cite the plaque by number.

**One correction avoided, and it is the lesson.** The Portuguese layer of the
PDFs mangles digits through its embedded font: the cypresses' planting year
extracts as "1_44". Read as 1844 it would have demolished a correct page,
because our story says the plaque dates the Cedro de Sao Jose to between 1628
and 1650. The ENGLISH layer of the same plaque is clean: "planted around 1644".
So the plaque confirms our page rather than contradicting it. Recorded at the
top of data/research/bucaco-plaques.md for the next run.

**One conflict recorded rather than resolved.** Plaque 07 dates the First Fall
cypress to around 1644 (about 380 years), while the state measurement from 2016
that our page cites reads about three centuries. Two official sources seventy
years apart; the published age still follows the dated state measurement and
the verify_note carries the plaque's figure. The girth settles the identity at
least: the plaque's 5.26 m against the 5.25 m already in our story.

**Three photographs are live** on Wellington's Olive, the Bunya Pine and the
Santa Teresa redwood, all three of which had none. Rotated, resized to 1600 px
and recompressed from 3 MB originals, hosted by us like the Baarn oak. Credited
to the Fundacao Mata do Bucaco, with the provenance in the photo note: they are
NOT under an open licence, they were sent to us by the body that manages the
forest. Hidde's call, 2026-08-21: "we mogen de foto's gebruiken, anders
versturen ze die niet." The written confirmation is still asked for in
drafts/reply-bucaco.md, which now also tells them what we did with the files.

## 2026-08-21 (session) - Bucaco: the Fundacao's biologist answers, and the Santo Elias redwoods come off

The Fundacao Mata do Bucaco replied to our outreach and had its own biologist
check the app. Three things came back.

**Every tree we list there is classified of public interest**, and each carries
an information plaque whose text was validated by the University of Aveiro and
the Fundacao. They sent the plaque PDFs and photographs by WeTransfer. That is
a second, authoritative source for the whole Bucaco page, better than anything
a research pass can assemble remotely, and it is the first time a forest's own
managers have handed us their field data.

**They asked for the Santo Elias redwoods to be removed** (bsc_005, "The
Redwoods of Santo Elias"): it is not possible to travel to them, which is why
the notable-trees trail does not sign them. Done the same day. Our page said
"free on foot" and marked the pin confirmed, so we were promising a walk that
cannot be made, which is the one error this site does not leave standing. The
entry moved to data/leads/bucaco.json as blocked with the reason, the old URL
redirects to the city page (REMOVED_TREE_SLUGS), and the intro and FAQ now say
nine trees rather than ten. The walk re-routes itself, since walk-routes.json
is keyed on the ordered tree ids.

**What is owed:** the plaque texts and photographs may not be published until
the Fundacao says so in writing, with a credit line they choose. Draft reply
asking exactly that is in drafts/reply-bucaco.md (mailcheck clean); it also
asks which tree on their trail visitors look for that we do not have yet.
FOR HIDDE: the WeTransfer link expires after seven days, so forward the files
or the link when you can.

## 2026-08-21 - Submission #10: "not worth it" vote on Paris par_001 (the Robinier of Square Rene-Viviani), no action

A reader used the worth-it control to mark the Robinier not worth the visit,
with no reason chip and no name/email on the row. Re-read the tree entry: it
is genuinely the oldest tree in Paris (1601), two independent sources, free
public square, `location_precision: confirmed`. The likely cause is the
physical experience rather than a factual error: the story already says
plainly that concrete props hold up its heaviest limbs, ivy hides much of
the trunk, and the on-site plaque undersells it. That is an honest account
of an underwhelming-looking tree with a genuinely remarkable history, not a
location or vitality problem, so nothing on the page needed to change.
Marked processed in `data/submissions-processed.json` (id 10). No email on
the row, so no reply owed.

## 2026-08-21 (session) - Florence's two cheapest leads (Bobolino pine, Simone Weil cypress) checked, confirmed still single-sourced

Both are held back only for want of a second source per data/leads/florence.json
(the pine stands 25m from live flo_007, the cypress 90m from the same cluster,
so either would be a genuinely zero-cost addition if a second source existed).
Fetched the comune di Firenze's own press release on its 29 monumental trees
directly (ambiente.comune.fi.it and comune.firenze.it) rather than trusting
the search summary, which initially and wrongly implied the comune page names
the pine (it does not; only "Cedro dell'incenso" appears on the Bobolino park
page itself). The press release does confirm the pine and Cedar of Lebanon at
Bobolino by name, but also states plainly that the municipal census IS the
data submitted to the Region and merged into the national MASAF Geoportale:
"la Regione Toscana ha gia completato l'inserimento dei dati sul Geoportale
ministeriale". So the comune announcement and the MASAF register are the same
designation act reported twice, one source, exactly as the leads file already
warned. intoscana.it's article repeats the same municipal announcement,
likewise not independent. No RAMI per-tree page or municipal park inventory
entry found for either tree. Left both as leads; the earlier pass's judgement
was correct. Also checked the Giardino dell'Iris strawberry tree (corbezzolo):
confirmed independently that the garden opens only 2-20 May each year, free,
which settles its access caveat if it ever ships, but found no dedicated
second source for the tree itself either. No changes made; recorded so a
future Florence pass does not re-run these same three searches.

## 2026-08-21 (session) - Munich 29 to 30, Vienna 27 to 28: one register lead each, closing the earlier "not worth a fresh pass" finding

Follows up on the same day's "Rome, Florence and Vienna's leads.py READY
counts checked, not written from" entry below, which correctly declined a
whole write pass on Vienna's remaining 8 leads but flagged one of them,
the Alser Strasse plane, as "verifies fine" on its own terms, just weaker
than the six shipped in an earlier pass. That is a legitimate single-tree
addition rather than a pass worth dispatching for its own sake, so it went
in directly: `vie_028`, London Plane, girth 315cm, Vienna's Baumkataster
gives a documented 1894 planting date (about 130 years), single register
source plus the city's own tree inventory, `curation_status: flagged`,
`location_precision: confirmed`, no photo. Took Vienna from 27 to 28
against a target of 30; the remaining leads (a Prater ginkgo with
unconfirmed courtyard access, a third Rathauspark plane, two young
Kugeltrompetenbaum specimens) stay leads for the reasons already on record.

Munich was one tree short of its target (29 of 30) with 15 READY leads,
all legally protected single trees on public land per the city's 2021
Naturdenkmalverordnung, most failing only on age (the ordinance carries no
age or girth column). Picked the Nymphenburg lime at Nordliches
Schlossrondell 8 for clustering: it sits about 0.7km from the existing
muc_007/011-014 Nymphenburg walk. Confirmed by a second source (Wochenanzeiger
Muenchen, 12 Oct 2011, naming this specific tree among eleven declared that
year), which the register-only leads file did not carry. Ships as `muc_034`,
`curation_status: flagged` (no age), `location_precision: approximate`. A
Commons photo (CC BY-SA 4.0, self-published 2020, filename matches this
tree and its Naturdenkmal designation by name) was found via the API and
set to `found_needs_check`; not viewed here, this runner's egress blocks
upload.wikimedia.org.

Both cities' route still walks clean (Munich 2.0km/24min, Vienna
2.0km/25min per `route_walks.py`). Vienna's meta_description updated from
"Twenty-seven" to "Twenty-eight". Full detail in LOG.md.

## 2026-08-21 (night run) - Milan 19 to 21, Brussels 26 to 30: leads.py READY trees, all flagged, no photos

Both were single-source-only register trees that a past pass had correctly
found and correctly left in leads.json as thin rather than blocked; per
CLAUDE.md's ruling that a judgement call about thinness never blocks
publication, both got written up. Milan: two MASAF-register London planes
(Viale Montesanto, 38m; Piazzale Libia, 35m), each single-sourced,
`curation_status: flagged`, no age (the Italian register carries no age
field). Brussels: the Parc d'Egmont pyramidal holly (140cm girth, second
largest of its cultivar in the region) plus the three trees a July 2019
survey added to that park's register entry (a pagoda tree, a weeping ash,
a thornless honey locust), the latter three sharing one approximate
coordinate since the register itself recorded a group point rather than
one per trunk. All 6 flagged, all photo-less. Both cities' count-promising
copy (intro/meta/faq/question block) updated. Full detail in LOG.md.

## 2026-08-21 (night run) - Rome, Florence and Vienna's leads.py READY counts checked, not written from

`prepare.py`'s shelf summary and `city_queue.py --next` both pointed at Rome
(4 ready), Florence (1 ready) and Vienna (10 ready, later 8 after the fix
below) as cheap write-only passes: below target, register-rich, leads.py
says READY. Read the actual lead entries behind all three before claiming
tokens for a write pass, and none were genuinely ready:

- **Rome's 4** each carry a `[SKIPPED 2026-08-14 by the write pass]` note
  explaining a real reason none matches `data/block-reasons.json`'s patterns:
  beyond the 30-minute day-trip boundary, an unresolved post-fire vitality
  check, or a planted grove with no individual specimen (not a collectible
  point). Correctly excluded before; still correctly excluded now.
- **Florence's 1** is an unverified RAMI-only list (3 species) needing its
  own second source per its own text, i.e. exactly the "not verified yet"
  case the two-source bar exists for, not a done story waiting to be typed.
- **Vienna's list** was mostly a bug: entries already noted "verified and
  delivered to data/research/vienna-verified.json as vie_026" (no literal
  "delivered AS" match) were slipping past `leads.py`'s DONE regex and
  showing as fresh candidates. Fixed in `scripts/leads.py` (widened DONE to
  catch "delivered to" as well), dropping Vienna's count from 10 to 8. The
  remaining 8 are real leads a past pass deliberately left out for legitimate,
  non-blocking reasons (a third plane in a park that already has two, access
  still unconfirmed on a Prater ginkgo, a weaker specimen off the main walk),
  none of which is a fresh six-candidate pass worth dispatching on its own.

None of this changes the shelf's headline numbers being genuinely useful for
*some* cities (see the Milan/Brussels write pass below, dispatched instead):
the lesson is that `leads.py`'s READY count is a start, not a verdict, and a
run should read the `why`/`why_not_published`/`why_not_yet` text before
claiming a city on the strength of the number alone.

## 2026-08-21 (night run) - Bari's 4th tree checked and still not found

Bari has 3 fully verified, written trees (`data/research/bari-verified.json`)
sitting one short of the 4-tree floor: an ombu and a "mangiafumo" (ponytail
palm) in Piazza Umberto I gardens, and the Pine of Carrassi. The in-city
register supply is exhausted (2026-08-20) and the two closest day-trip
candidates (La Grave carobs, Sovereto pine) were already blocked. This pass
checked the last three unchecked day-trip candidates from Puglia's regional
register, all in Molfetta (24-29km, well inside the 30-minute rail day-trip
boundary at 21-25 minutes each way): the Torre di Pettine eucalyptus, the
Navarino roverella and the Macchia Clemente carob. All three moved to
blocked in `data/leads/bari.json`: the eucalyptus sits 300m+ from any
mapped road (Overpass check), the roverella adjoins a privately walled,
ruined masseria with no source placing the tree relative to the wall, and
the carob sits in a private-house contrada with no source confirming it is
the same tree as the unrelated, definitely-public carrubo secolare in
Molfetta's Parco Lama Martina (joining those two would be the bridge-claim
error). That exhausts the regional register's day-trip supply for Bari.
Bari stays unpublished, 3 trees, until a reader submission, a from-zero
web sweep, or Hidde widening the day-trip boundary produces a 4th. Claim
released. Logged in data/agent-costs.json as a zero-yield verify pass.

