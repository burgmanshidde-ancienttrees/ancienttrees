

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-08](archive/CURATION-2026-08.md)
- [2026-07](archive/CURATION-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
<!-- archive-index -->
## 2026-08-15 - Potsdam's staged register candidates are all in Berlin, not Potsdam

`data/research/potsdam-register-candidates.json` (7 entries, stocked by `prepare.py`) all sit at Jagdschloss Glienicke, Schlossgarten Glienicke or Volkspark Klein-Glienicke, district Steglitz-Zehlendorf, postcode 141xx: administratively Berlin, not Potsdam, however close to the border (Glienicke Brucke, the actual city line, sits metres away). Not shipped anywhere this pass: attributing them to Potsdam would misstate which city a visitor is in, and Berlin (already published, 18/30 trees) is a Google-confirmed stage-2 city, so deepening it is paused while stage-1 cities like Potsdam still have real supply elsewhere. Left for whoever revisits Potsdam or Berlin next: worth checking whether `prepare.py`'s candidate-staging picks trees by raw distance to a city's centre point without checking which municipality/postcode they actually fall in, since that would explain the mismatch and might affect other border cities too.

## 2026-08-15 - Zaragoza's prison laurel: the strongest history in the register, and it is dead

Checked as a candidate to close Zaragoza's gap (a READY-flagged lead per `leads.py`, which does not read the `why` field). The Bay Laurel of the old Carcel de Torrero grew inside the prison compound, between the infirmary, a module and the north wall, visible above the walls from the street; prisoners tended it and it became, by more than one account, a symbol of the world outside for people who could not leave. It is the strongest single story the Zaragoza register holds, ahead of anything currently published.

It died. The prison was demolished afterward and the plot redeveloped; the site is now a small square the neighbourhood renamed Plaza del Laurel in the tree's memory, currently in poor repair (a 2020s rat-infestation complaint is the most recent thing written about the square). Blocked in `data/leads/zaragoza.json` per the dead-tree rule, which does not bend for a good story. Recorded here because it is worth knowing rather than re-finding: a future pass on Zaragoza should not spend time on this one again.

Also touched, not resolved: the Field Elms of Camino de Enmedio, La Cartuja, where a 2005 source flagged one of two registered elms as endangered by nearby concreting. A current hiking-trail description still lists an elm and a mulberry along that exact lane, which is real corroboration that something survives, but not which of the two register entries it is. Left as a lead rather than guessed at.

## 2026-08-14 - Two feedback submissions on Baarn's brn_005: already fixed, both look like test rows

Supabase `submissions` held two new `kind: feedback` rows (ids 2 and 3, both created 06:52-06:53 UTC today), both reporting brn_005 (The American Oak of the Pekingtuin, Baarn) as "wrong location". Row 3 is explicitly suffixed "[TEST ROW, session 2026-08-14, safe to ignore]"; row 2 is byte-identical content submitted 23 seconds earlier without the marker, almost certainly the same in-session test of the new vote/report feature (LOG.md's same-day entry: "the full interaction chain was tested live including a real Supabase insert (201, marked TEST ROW)"). Checked the live data anyway rather than assume: brn_005's location was already fixed on 2026-08-13 (see that date's entry below), pin moved to the correct oak at 52.209694,5.292861, on-site checked, story now explicitly distinguishes it from the ringed tree 60m away. Nothing to fix. Marked both ids processed in `data/submissions-processed.json` alongside the original id 1.

## 2026-08-13 - Baarn's Pekingtuin oak: the ring belongs to a different tree, and the pin was on the wrong one

Ground truth from Hidde, who walked into the Pekingtuin on 2026-08-11 and photographed what is actually there. Two true facts had been welded into one false claim, which is the error this file exists for.

- **What was right.** Dutch Wikipedia's line stands and his photograph agrees with it: an Amerikaanse eik planted around 1850, 5.52 metres round, in a free municipal park five minutes from Baarn station. The 2021 poetry ring is real, and so is the poem by Ewoud M. Rosenthal.
- **What was wrong, and it is the location.** Our story said the ring marks off THIS oak's root plate, and the pin (52.20956, 5.29203) sat at the ring. The ring stands around a smaller tree with dark purple foliage, and the oak stands about 60 metres east at 52.209694, 5.292861. No source ever connected the two; the connection was our own inference from a news article about the ring plus a Wikipedia sentence about the oak. A reader following the old pin would have arrived at a modest tree in a steel circle and concluded we had never been there.
- **How it got a confirmed pin.** `data/research/baarn-pins.json` (the pin pass) states plainly that the ring could NOT be located in aerial imagery at that resolution and left the pin approximate. A later pass upgraded it to confirmed citing PDOK aerial imagery in which "the ~6m 2021 protective ring is individually visible around the standing tree". That is a claim built on exactly the evidence a previous pass had recorded as unavailable, and it is the mechanism worth remembering: our own earlier finding was in the file and nothing made anyone read it.

Fixed: pin moved to the oak and now genuinely confirmed, story rewritten to describe the oak and to place the ring honestly on its own tree, `how_to_recognise` added because the two trees are the one pair in this park anybody could confuse, and the entry now carries the project's first owner-supplied photograph (site/public/photos/, credited to Ancient Trees rather than to a person, per PRINCIPLES #10).

## 2026-08-13 - Porto's ginkgo photo: the grant is in writing, and the OTHER post's photos are not his

Paulo Araújo answered in writing that we may use the ginkgo photograph, with one caveat that had to be checked rather than assumed: only that photo on the page is his, the other text and its photographs are not. He has written about this tree twice, so the caveat lands exactly on us.

- **Live and covered.** `photos1.blogger.com/img/291/1346/480/Ginkgo-amarela.jpg` (por_018) is the lead image of the post "Alerta amarelo", 5 December 2005, published by Paulo Araújo, and the only photo credit on that page is "Fotos: © Paulo V. Araújo". Fetched and read directly. His yes covers this photo, which is the one already on the page.
- **Never usable, do not re-hunt.** The other post about the same tree, "Golden time - Ginkgo" (December 2004), credits its photographs "Fotos: manueladlramos-0412". Those belong to a third person who has granted nothing. A future photo pass looking for a better ginkgo image will find them first, because they are the prettier set; they stay off the site regardless.

DECISIONS.md's 2026-08-11 entry stands unchanged: one photo, one permission, not a new licence category, and every other photo on the site still needs a verified open licence.

## 2026-08-13 - Munich: fixed four trees published twice under different ids

Found while looking for cheap-end write work (`scripts/leads.py --ready`): Munich's
2026-08-12 Naturdenkmal writing pass re-wrote four Schlosspark Nymphenburg register
entries (Copper Beech, Large-leaved Lime, Fern-leaved Beech, Weeping Beech) that were
already live as muc_011-014, giving each of the four physical trees a second id
(muc_015-018), a second page, thinner data (no address, no age, no best_time) and a
duplicate story. Confirmed by exact coordinate match, not guesswork. Removed the four
newer duplicates from `data/cities/munich.json`, kept the better-documented originals,
added redirect stubs (`site/src/lib/redirect-map.ts` REMOVED_TREE_SLUGS) so the four
now-gone URLs resolve to `/munich` rather than 404, and merged the photo candidates
`data/photo-queue.json` had already found for two of the duplicates onto the surviving
ids (muc_015->muc_011, muc_016->muc_012, muc_017->muc_013), since those candidates are
genuinely of the same trees.

Root cause: the four source leads in `data/leads/munich.json` were never marked
resolved after the first write, so `leads.py`'s READY count still offered them as
unwritten. Marked all four `[RESOLVED 2026-08-13, delivered as muc_0XX]`. Also found,
by the same coordinate check, four more Munich leads that duplicate already-published
trees under different names (White Ash/Maximiliansplatz -> muc_019, Beech/
Flaucheranlagen -> muc_021, two Englischer Garten limes -> muc_020/muc_022) with no
live duplicate page this time, just a dormant landmine for the next write pass; marked
those resolved too. Checked every other published city for the same coordinate-collision
pattern: none found, everything else that shares a rounded coordinate is genuinely
distinct neighbouring trees (species differ).

Munich now 22 to 18 trees. Build and `qa.py` green (1325 pages; the sitemap
`lastmod` warning is the shallow git checkout in this environment, not a content
problem). Ran `tree_index.py` (1045 highlighted, down from 1049, correctly).

## 2026-08-12 - Den Bosch: 4 to 11 trees, two new clusters, the oldest-tree answer changes

Finished the writing pass that a prior session left open (dbo_005 to dbo_011, verified facts already in data/research/den-bosch-verified.json, only stories missing). Two new clusters: Sint Janskerkhof/Casinotuin (5 trees, dbo_005-009, within 300m of the already-published Bastion Oranje maple) and Pettelaarse Schans (2 trees, dbo_010/011, a former fort mound across town, below the 3-tree walk floor so they stand as honest standalone entries rather than a chip). The write pass caught and I fixed three things before shipping: two `how_to_recognise` fields carried internal process labels ("FLAGGED FOR AMBIGUITY:") that would have rendered verbatim to visitors under "Which one is it?", two `transport` fields read as an instruction to us ("checking a local bus... may cut this shorter") rather than to a visitor, and two new trees used `Platanus x hispanica` where the site's other 79 London Planes use `Platanus x acerifolia`, which would have failed the build's hard-rule-9 one-scientific-name-per-common-name check.

The oldest-tree answer changes: dbo_005, the Plane of Sint Janskerkhof (roughly 170 years, register-only, flagged), beats the previous answer, the Bastion Oranje Norway maple (roughly 120 years) by margin even at each range's overlap. Updated intro, meta_description, question_answer/meta/context and the FAQ's first two entries to match; all three age/count fields (four trees, three verified entries, the maple as oldest) were previously baked into hand-written city-page copy exactly like the Netherlands-country-page bug REVIEW.md flagged as a BLOCKER on 2026-08-02, so this was corrected before it could repeat that class of error live.

Computed the walk directly: one cluster of 9 trees (all published trees except the two Pettelaarse Schans ones), 2.9km, 39 minutes. Ran `tree_index.py` (19,401 trees tracked). Build and `qa.py` both green (1205 pages). Released the `den-bosch` claim in data/in-flight.json.

## 2026-08-12 - Kyoto: the two HELD Gyoen trees ship, 16 to 18 trees

`data/leads/kyoto.json` held two written-and-ready stories (kyo_015 the carriage-turning cherry, kyo_017 the Shimodachiuri camphor) HELD since 2026-08-11/12 on an identical placeholder coordinate, both copied from the already-published Demizu-guchi hackberry's own point rather than surveyed. Resolved via Nominatim/OSM: Seisho-mon gate (kyo_015's actual reference point, confirmed "southwest of Seisho-mon" by an independent web source) at 35.0258332/135.7610189, Shimodachiuri-gomon (kyo_017's own story already names it directly, and OSM has the gate tagged as a building) at 35.0195774/135.7595584, 0.71km apart. Both ship `location_precision: approximate` (gate-area estimates, the same honest convention kyo_011 already uses, not a GPS fix on the trunk). Corrected kyo_017's species to the site's canonical "Camphor Tree (Cinnamomum camphora)" and shortened kyo_015's name (the "Kurumagaeshi-zakura (the carriage-turning cherry), Kyoto Gyoen" form tripped the 60-char title limit at build time).

Also fixed a real live gap found along the way: kyo_016 and kyo_018 (shipped 2026-08-11) had no `access`/`transport` fields at all, rendering as blank rows on their pages. Added both.

Recomputed the walk rather than trusting the old copy: Kyoto Gyoen now forms two walks (5 trees/1.0km, 4 trees/1.2km), 9 trees total in or beside the park, up from "five within 1.1km, one walk". Rewrote intro/meta_description/question_meta/two FAQ answers for the new 18-tree, 13-free-of-18 totals.

Deliberately left alone: kyo_017's real coordinate sits ~25m from the already-published kyo_011's own pin despite both stories placing the trees a short walk apart; kyo_011 may itself be imprecise but that's a separate live tree, not touched on today's evidence alone, recorded in leads/kyoto.json's new `shipped` section for a future pass. Build and `qa.py` green together with Den Bosch, 1420 pages. Ran `tree_index.py` (19,401 trees, 941 highlighted).

## 2026-08-12 - Rome and Bologna: a dead landmark blocked, a genuine new tree shipped

Rome's passcheck brief printed a Wikidata discovery candidate, "Quercia del Tasso" on the Janiculum, CC0 image attached, not already in our data. Checked before touching anything: it is dead, a dried husk held up by a retaining wall (struck by lightning 1843, arson-damaged 2011). Blocked in `data/leads/rome.json` so it is never re-surfaced as a live candidate. Rome's three other non-flagged MASAF register entries near the Celimontana cluster turned out to be the same three trees already correctly blocked as access-restricted (the closed San Sisto nursery). Rome's register is genuinely picked clean right now, confirmed rather than assumed.

Bologna's register held one genuine, cheap addition: a grey walnut (Juglans cinerea, "Noce Cenerino"), the only one of its species on Italy's entire national monumental-trees register, sitting about 230m from the already-published bol_007 ginkgo, both inside the university's Orto Botanico on Via Irnerio. Two independent press sources (a Bologna news site and a tourism guide, both citing the garden's own curator and a university professor running a 2025 five-year conservation project) corroborate species, height and that it is alive now, under active care for age-related decline rather than dead. Girth disagrees between sources (register 420cm, press 471cm) and both figures are recorded rather than one picked as a winner. Shipped as bol_011. This crosses the 3-tree minimum for a second Bologna walk that didn't exist before: bol_001 (Montagnola), bol_007, bol_011, 1.1km, 15 minutes. Bologna: 10 to 11 trees, one walk to two. A second register entry (Cedro dell'Atlante, Villa delle Rose, 545cm girth) was left as a lead in a new `data/leads/bologna.json`, genuine but too far from any existing cluster to join a walk. Build and `qa.py` green (1421 pages). Ran `photo_hunt.py --recheck` and `tree_index.py` on both cities.

## 2026-08-10 - Berlin's Charlottenburg/Lietzensee cluster: documented, and why it isn't a walk yet

ber_016 (Lietzensee Plane), ber_017 (Lietzensee Wingnut) and ber_018 (Karpfenteich Elm, Schlosspark Charlottenburg) were verified and merged into data/cities/berlin.json by a night run whose LOG.md entry was never finished (a permission-list bug broke builds right around then; see LOG.md 2026-08-10). Logging the gap now since the data was already live. `plan_walks()` confirms these four Charlottenburg-area trees (with the already-published ber_004 Swamp Cypress) do not form a computed walk: Lietzensee's pair sits 170m apart, the palace-park pair sits 66m apart, but the two pairs are 1.9km apart, just past the 900m walk-clustering radius, so each pair alone is one tree short of the 3-tree floor. Two register-only leads in the same palace garden (Echte Mispel and Kirschpflaume, both "Eigenart, landeskundliche Gründe" designations, no age, no second source found across three separate checks now) were judged too marginal to ship just to force a third tree into the cluster. Stays an honest gap: Berlin has two real destinations in the same corner of the city, Lietzensee and Schlosspark Charlottenburg, about a 25 minute walk apart, but no single page walk connects them yet.

## 2026-08-09 - Baarn wacht op de veldcheck van de eigenaar (het staande protocol)

Hidde loopt de Baarn-route deze week na als eerste grondwaarheid-audit van de
pijplijn. Wat zijn wandeling kan opleveren, vastgelegd zodat een run of sessie
het herkent als het binnenkomt: (1) per boom pin/toegang/verhaal-tegen-de-
werkelijkheid, elke afwijking is kalibratie voor 870+ bomen die dezelfde
pijplijn maakte; (2) foto's van informatiebordjes bij Groeneveld en het
Cantonspark tellen als de tweede bron die de tien wachtende kandidaten
ontgrendelt (Staatsbosbeheer/parkbordjes zijn bronnen); (3) eigen foto's van
de vijf bomen via het formulier lossen het gedocumenteerde fotogat op (veertig
open kandidaten bekeken, nul bruikbaar; het gat is bezoekersvormig); (4) de
Groeneveld-vooreik heeft naast een bron ook een verzamelpunt-oordeel nodig
(het is een eikengroep in driehoeksverband). Zijn identiteitsoordelen tellen
als lezersinzending-bewijs, zoals bij de tulpenbomenfoto die zo Baarns eerste
beeld werd.

## 2026-08-09 - Paris's Latin Quarter walk grows 6 to 7 trees, 24 to 25 published

Added par_027, the Amur Cork Tree of Square Michel-Foucault, delivered as a lead in data/leads/paris.json ("same tiny garden as par_014, so a future pass could verify and add it with zero new walking distance"). Fetched paris.fr's own equipment page for the square directly (confirms 1925 planting, a lightning scar, and that the two named squares share one 24/7-open pocket garden) and French Wikipedia's Square Auguste-Mariette-Pacha article (14m tall, 1.80m circumference as of 2011). Checked whether these count as two independent sources per the register-pitfalls discipline: they do not, Wikipedia's own footnote cites the same paris.fr "Les arbres remarquables" page for its measurements, and a direct query of the structured opendata.paris.fr register confirms this tree has no entry there at all. Shipped anyway, single-source and flagged, per CLAUDE.md Step 2's explicit allowance, with the non-independence stated plainly in verified_sources rather than dressed up as two sources. No exact GPS pin found for the tree within the garden, so it reuses par_014's coordinates and ships location_precision: approximate. The Latin Quarter walk (formerly "Jardin des Plantes") grows 6 to 7 trees, still 2.9km. meta_description and question_meta updated from "23 more" to "24 more" (the exact stale-count bug class REVIEW.md flagged twice this week on Paris and Vienna). No photo candidate found on the first sweep; honest gap. Build and qa.py both green (1112/1325 pages).

## 2026-08-09 - New York's Central Park cluster confirmed exhausted, correctly left at 5

Dispatched a verify pass to grow New York's Ramble/Mall/CPW walk past its current 5 trees. Result: 0 new trees. All 5 NYC Parks "Great Trees" register entries within the cluster are already published; the Conservancy's self-guided Ramble tour, oak-society map, and storm-damage press coverage produced only one thin lead (a second, likely-young, undated Camperdown Elm in the East Green, whose only real story hook duplicates the far stronger and older Prospect Park specimen already on the site). Recorded in data/leads/new-york.json rather than shipped. Left at 5 rather than padding, per doctrine.

## 2026-08-09 - Berlin's Pfaueninsel register cluster confirmed exhausted

Cross-checked data/registers/berlin-naturdenkmale.json directly against the Pfaueninsel walk's centroid: all 5 Naturdenkmal entries within 1km are already published (ber_011 through ber_015, the last two added earlier today). Remaining leads in data/leads/berlin.json sit in Charlottenburg/Lietzensee (1.7km+) or Kladow (4-5km, a different Havel bank reachable only by a different ferry route), too far to fold into this walk. No further growth possible here without a fresh web-research pass; not attempted this session given the exhausted state is already well documented.

## 2026-08-09 - Budapest and Copenhagen photo gaps: 14 images viewed, zero approvals, one hold

Viewing pass over the queued Commons candidates for bud_004, bud_006, bud_007, bud_008 and cop_005 (bud_001, bud_002 and bud_003 were already closed by the 2026-08-08 pass and were not re-judged). 14 images looked at as actual pixels, throttled to one request every 3.2 seconds, no rate limiting. Nothing met the Cadiz standard. Both cities still publish zero photographs, and these particular hunts are now documented dead ends on Commons: do not re-sweep them.

What the candidates actually were, because the pattern is worth keeping. Commons geosearch in dense European city centres returns the BUILDING, not the tree: all seven bud_007 candidates are interiors and courtyards of the Henszlmann utca 7 apartment block (balconies, a tiled floor, a staircase, an etched glass door), roughly 100m from Karolyi kert; cop_005's single candidate is a photograph of the Bomhoffs Have street sign; bud_006's is a close-up of pink Cercis flowers on a trunk, which is neither the right species nor the right kind of shot.

The Taban trail candidates (bud_004) are a specific trap worth remembering, because they look correct on metadata and fail on pixels. Twelve photographs from the Tabani Botanikai Tanosveny, correctly named Morus alba, correctly geotagged, one of them 80 metres from our pin. Viewed, they are a young staked weeping mulberry with three support posts and a sapling's foliage against blown-out sky. The nature trail's labelled stations are recent plantings, not the veteran tree the entry is about. A pass that had approved from the filename would have shipped a sapling as an ancient mulberry.

The one real find is a hold, not an approval. bud_008's two candidates are LBM1948 slides from August 1988, described by the uploader as an old black locust at Szechenyi Istvan ter, which matches the entry on species and place. The second of them (`Budapest, arboles 1988 03`) is the only image in the whole batch that meets the Cadiz composition test outright: the whole tree, a deeply fissured leaning trunk and the crown both readable, daylight, colour, Gresham Palace behind it. It fails on one thing only, that it is 38 years old, with period cars parked in frame, and nothing in the pixels confirms this Robinia still stands or still looks like this. Robinia pseudoacacia is not a long-lived species. Publishing it would risk promising a visitor something that is not there, which is the never-cuttable rule, so it is written into budapest.json as status `held`: kept in the file with its exact licence and attribution (CC BY-SA 4.0, LBM1948), off the site, verified as non-rendering. The first candidate from the same series was rejected outright, being exposed for the sky with the whole lower trunk in near-black shadow.

Flagging the judgement rather than burying it: the corpus bans "archival imagery" and illustrates it with a 1904 stereograph. A 1988 amateur colour slide of a living tree sits in a genuinely grey zone, and a run should not quietly widen a rule Hidde wrote. The hold preserves the work either way. If he reads a 38-year-old colour photograph as acceptable, bud_008 becomes Budapest's first published photo with a one-word status change; if not, it stays an honest gap. Note the 2026-08-08 pass rejected a sibling slide from this same series for bud_003 on the same 1988 grounds, so treating them consistently matters.

## 2026-08-09 - Licence hygiene: edi_003's confirmed pin rested on forbidden ATI data, downgraded

The Edinburgh pin pass discovered that the Cammo Ash's confirmed coordinate was set by an early pass that queried the Woodland Trust ATI FeatureServer directly, before the licence gate was understood. Per the standing rule (no ATI data in any form until written permission arrives), the pin is downgraded to approximate with a note; the coordinate stays as approximate knowledge, the confirmation claim is withdrawn. If the Woodland Trust grants permission, this is the first tree to re-confirm. Checked the rest of Edinburgh's confirmed pins: edi_005's confirmation comes from a non-ATI source and stands.

## 2026-08-09 - DC pin audit: a possible wrong pin flagged on the FDR cork trees

The Venice-model pin pass over Washington DC's eight approximate pins reached zero confirmed upgrades, which is itself information: the 1912 cherries' pin turns out to BE the surveyed marker position (the honest ceiling), the Survey Lodge catalpas tightened to ~20m via the OSM building footprint, and Battery Kemble and the Arboretum are documented as legitimate park-level ceilings. The one actionable find: wdc_010's pin sits roughly 185m NORTH of the FDR Memorial's OSM boundary polygon, which means either the pin or the polygon is wrong. Nobody moved anything without ground truth; a follow-up pass (or any visitor) should establish where the cork trees actually stand. Until then the pin stays approximate, which the page already warns about next to its directions button.



<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-07](archive/CURATION-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
<!-- archive-index -->
## 2026-08-09 - Lisbon's Estrela walk grows 5 to 6 trees, 20 to 21 published

Delivered a lead already sitting in `data/leads/lisbon.json` since 2026-08-05: the Tipuana tipu at Praça São João Bosco (ICNF processo AIP11066049I), held back before only for lacking a second source and an access check. Found the second source (Junta de Freguesia da Estrela's own article on a March 2018 ICNF-supervised structural pruning of this exact tree) and confirmed access: it stands in Jardim da Parada dos Prazeres, a public roundabout garden facing the Prazeres Cemetery. Named carefully to avoid a real trap: this garden is a different place from lis_016/lis_017's "Jardim da Parada" (Jardim Teófilo Braga, 500m north), despite sharing the nickname, a confusion the corpus already flags once in lis_016's own notes. Shipped as **lis_021**, age flagged (register-only, no independent age source; girth 3.42m, height 23.5m, crown 34m, classified January 2019). Estrela walk now 6 trees, 2.1km, 28 minutes (was 5, 1.6km). A register-twin pair of 150-year Celtis australis 730m away (KNJ1/279, KNJ1/280) was NOT shipped: their address, "Quintal do n.º 79", reads as a private back garden rather than public land, so held on hard rule 10 grounds and moved to leads rather than blocked outright, in case access can be confirmed later. Photo swept (0 candidates, honest gap). Cost: about 40k tokens, 1 tree.

Also checked Vienna's lead walk (5 trees, below the 6-8 aim) for similar unshipped near-cluster candidates: none exist. `data/leads/vienna.json` already recorded the two nearest options (two more Rathauspark planes) as deliberately rejected ("three planes in one park is padding") and a Josefstädterstraße ginkgo as access-unconfirmed. Left as is rather than re-litigating a documented call.

## 2026-08-09 - New York's Reservoir cluster opens, a real second walk, 17 to 20 published

Dispatched a verify pass at four leads a prior session had found near the Jacqueline Kennedy Onassis Reservoir but not pursued (too far, 1.1-2km, from the Ramble/Mall cluster to join it). Verified against each other instead: **nyc_018** (American Elm, East 97th Street entrance, NYC Parks Great Trees register id=46 plus Untapped Cities and Westside Rag, age only "dates to the 1800s"), **nyc_019** (London Plane of the Reservoir, register id=43 plus two more sources, the "possibly planted 1862" claim correctly attributed to one writer's guess rather than a record), **nyc_020** (Yoshino Cherries of the Reservoir, register id=42, one ensemble entry per the register's own treatment, a 1912 gift from Japan predating Washington DC's more famous planting the same year, honestly flagged that no source confirms whether today's 35 trees are originals or replacements). All three sit 170-750m apart, forming a genuine second walk 1.1km from the existing cluster. The Evodia lead (Heckscher Playground, south end of the park) was distance-checked and confirmed too far (2.3km) to join either walk, stays a lead. Wrote `data/parks/central-park-new-york.json` to clear the 5+ tree park-page gate the new count crossed (7 Central Park trees now). City copy (meta description, FAQ free-to-visit count) updated seventeen to twenty trees. Cost: about 109k tokens, 3 trees.

## 2026-08-09 - Amsterdam: the Vondelpark lead turns out to be a mis-pinned tree already published, corrected in place

Dispatched a verify pass at Vondelpark's dense cluster of officially protected trees (data/registers/amsterdam-bijzondere-bomen.json), aimed at growing Amsterdam's thin 3-tree second walk. The strongest-looking candidate, a matched pair of 1863 London planes at over 7 metres girth each (register ids 504491/510594, 25m apart), turned out on verification to already be published: **ams_002**, "The Leidsebosje Planes," whose story (moved 1925 for a bridge widening, 7m+ girth, woodcutter sculpture) matches exactly. Its pin, however, sat about 93 metres from the register's own tree-level coordinates. Corrected to the midpoint of the two register points and downgraded `location_precision` from `confirmed` to `approximate`, since one pin still cannot exactly mark two trunks 25m apart, with a note recording the correction and its reasoning. Two other candidate groups near the same cluster (five 1881 planes in a 40m line, eight 1948 bald cypresses in a tight grove) were confirmed as avenues/groves and correctly left unshipped. A genuine 1960 elm pair and a mixed maple/willow/ash trio lack a second source and are recorded as leads for a future pass with photo-based verification. Zero new trees this pass; one real precision fix. Also noted for the standing register-pitfalls list: this register's `champion_tree` field reads `true` on effectively every entry checked, so it is not a usable superlative filter without independent checking.

## 2026-08-09 - Edinburgh's RBGE walk grows 5 to 7 trees, 13 to 15 published

Picked up a claim the previous session left unfinished (Edinburgh, claimed but never delivered). Verify pass found two more genuinely remarkable, individually identifiable trees inside the Royal Botanic Garden Edinburgh, both joining the existing Inverleith cluster: **edi_014**, one of five RBGE dawn redwoods grown from the historic 1948 seed consignment that ended the species' presumed extinction (flagged: no dated recent evidence this exact Chinese Hillside specimen is alive, only an actively maintained catalogue entry), and **edi_015**, the UK & Ireland champion Sorbus hemsleyi by girth, corroborated by an independent, dated (August 2023) source. The RBGE walk now routes 7 trees, 1.7 km, 23 minutes, real Google Maps geometry, up from 5. Six more RBGE candidates stayed leads (Monkey Puzzle E24, two glasshouse palms, Coast Redwoods, and two too-young plantings), none cleared the two-source or maturity bar this pass. Fixed a pre-existing stale count bug while in the file: the intro still said "ten" trees against an actual 13 (now 15), caught and corrected in intro, meta_description and the free-to-visit FAQ answer. Photo sweep run afterward (photo_hunt.py --recheck): edi_015 picked up 2 open-licence candidates, queued for a viewing pass; the other 4 photo-less Edinburgh trees stay an honest gap. Cost: 95k tokens, 2 trees published.

## 2026-08-09 - Berlin's Pfaueninsel walk grows 3 to 5, and a live title bug is fixed

Queried `data/registers/berlin-naturdenkmale.json` directly for candidates within 2.5km of the Pfaueninsel cluster (52.4315, 13.1207) instead of relying on passcheck's city-centre-based brief, which is 20km off for this cluster and useless for it. Found two new register-designated trees genuinely near the walk: **ber_014**, "The Ferry Landing Plane", a London plane on the mainland side of the ferry crossing (free, no ferry ticket needed, unlike the rest of the cluster), and **ber_015**, "The Cut-Leaf Oak of Pfaueninsel", a rare cut-leaf variety (Quercus petraea var. laciniata) 45m from the already-published Great Oak, confirmed as a genuinely distinct tree rather than a register duplicate. Both single-sourced (the official register only) and shipped `flagged` per CLAUDE.md Step 2's explicit one-source rule. The walk now routes 5 trees, 1.8km, 24 minutes, up from 3. A third candidate, a copper beech at Villa Dr. Fraenkel in Kladow, was checked for walkability and found to sit across the Havel with no walking connection; kept as a lead for a possible future Kladow-side cluster rather than forced into this one.

**Found and fixed a live bug while adding these two trees**: age_token() in build_site.py fell back to the Python string "None" when a tree had no age_estimate digits and null age_min, which had already shipped "None Year Old" literally in the `<title>` and `og:title` of three published pages (Zaragoza's Yew of the Paraninfo, Barcelona's Mastic of Hort de l'Avi, Paris's Plane of Quai Saint-Bernard), invisible unless you read raw HTML. Fixed at the source (age_token returns None instead of the string "None"; both title-building call sites now skip the age-bearing template candidates when age is unknown) and added a qa.py check for "None Year" in rendered text so this class of bug can't ship silently again. All three pre-existing pages and both new Berlin trees verified clean after rebuild.

## 2026-08-09 - New York's Central Park walk grows 4 to 5

Followed up the strongest lead already on file: the Cedar of Lebanon near Conservatory Water, previously undelivered for having only one source. Found a genuine second source (a 2016 garden blog) that corroborates the Central Park Conservancy's own plant page and adds a dedication detail, though the two disagree on whether it is one specimen or a small grove; delivered as **nyc_017**, "The Cedar of Lebanon Grove near Conservatory Water", flagged, with the discrepancy stated plainly rather than picked. At 370-780m from the existing four-tree cluster, it is the closest addition this walk has had; walk grows to 5 trees, 1.7km, 23 minutes. Confirmed and blocked the Shakespeare Garden mulberry (blew down 2006, removed, no replacement) and the Strawberry Fields grove (not a single collectible point) along the way. The Reservoir/97th Street/Evodia leads stay recorded as a seed for a possible separate, more northerly Central Park cluster; still too far from this walk to fold in.

## 2026-08-09 - Dublin gets a second walk: the National Botanic Gardens, 7 trees from one register query

Trinity's leads were exhausted (checked earlier this week: Quatercentenary Oak too young, Sessile Oak beside the Flatiron unlocated, Giant Redwood too young, Oregon Maples confirmed dead), so instead of forcing more out of a dry cluster, queried `data/registers/ireland-heritage-trees.json` (GBIF Heritage Trees of Ireland, CC BY 4.0, 2009 field survey) within 500m of dub_004 (Addison's Walk, National Botanic Gardens Glasnevin), a tree the site already had but had never exploited as a cluster seed. Found six more designated "Exceptional specimen trees" within 200m, all delivered: **dub_012** Atlas Cedar (register-only, IUCN Endangered in the wild), **dub_013** Dawn Redwood (register-only, the same 1941 living-fossil rediscovery story used for Edinburgh's edi_014), **dub_014** Caucasian Elm (two sources; Trees and Shrubs Online confirms a named cultivar, 'Glasnevin', was propagated from cuttings of this exact tree), **dub_015** Bald Cypress (register-only; corrected the species' canonical name to match Berlin's ber_004, hard rule 9 would otherwise have failed the build on "Swamp Cypress" vs "Bald Cypress"), **dub_016** "Ireland's Largest Tree of Heaven" (two sources; a genuine age dispute between the register's band and general Ailanthus lifespan stated openly, neither figure picked), **dub_017** Hybrid Strawberry Tree (weakest of the six, a likely-but-not-certain photo match).

Dublin now has two walks: Trinity unchanged at 3 trees, and a new Glasnevin walk at 7 trees, 0.7km, 9 minutes. Growing this cluster to 7 trees crossed the park-page publish gate (Contract H, 5+ trees plus a hand-written intro), so wrote `data/parks/national-botanic-gardens-dublin.json` to unblock the build rather than leave it print-warning forever. City copy (intro, meta_description, both FAQ answers) updated from eleven to seventeen trees.

Session viewing pass (the CI proxy cannot; judged against the Cadiz standard, throttled at 3.2s/request, no 429s). Approved: nyc_011 The Great Elm of Central Park West, CC0 iNaturalist by Daniel Atha (NYBG botanist), geocoded to exactly the entry's CPW/W77 corner; the first NYC photo in three passes. Rejected 47: street scenes where no tree is the subject, phenology close-ups (bark, buds, leaves in hand), wrong-species observation records, night shots.

TWO PHOTO HUNTS NOW EXHAUSTED, do not re-run:
- dub_005 (Provost's Plane, Dublin): all ten Commons geosearch hits are Grafton Street scenes, Molly Malone, a tram. The gap needs a NEW source (reader photo, or Trinity's own media office via the outreach lane), not another sweep.
- par_017 (Anne Frank Chestnut, Paris): all nine candidates are OTHER cities' Anne Frank trees (Yad Vashem, Bedford, Utrecht, Bournemouth, the fallen Amsterdam original). Same conclusion: only a new source closes it.

One process note kept honest: 17 of the 47 rejections were made on file coordinates/description rather than pixels (a Bournemouth chestnut cannot be the Paris tree whatever its pixels show); each such verdict says so in the queue. The look-at-pixels rule exists to stop blind approvals and none of those were blind.

## 2026-08-07 - Paris verify pass: 3 more trees for the Latin Quarter/Marais cluster, not yet written

Verify-only pass (data/research/paris-verified.json, not merged into paris.json yet, a write pass still needed). 3 trees, 1 flagged: par_016 (Twisted Beech, Square des Arenes de Lutece, confirmed pin, ~120yo), par_017 (Anne Frank Chestnut, Jardin Anne Frank, confirmed pin, symbolic-significance qualifier like par_007, a girth discrepancy between two sources left for the writer to note rather than resolved silently), par_018 (Fig of Square Georges Cain, confirmed pin but flagged: repeatedly described as "over a century old" with no sourced planting year). All three extend the existing Latin Quarter/Jardin des Plantes/Marais cluster (300m to 1.2km from par_001/007/013/014/015). 4 register candidates blocked as duplicates of already-published trees. One lead not shipped: a Quai de l'Horloge weeping willow whose identity is genuinely confused with a different, more famous willow at Square du Vert-Galant in the same search results, with one source's 1750 planting date not biologically credible for the species; needs a primary-source fetch this session's egress couldn't reach.

## 2026-08-07 - Paris deepens to 13 trees, a second Latin Quarter pocket

Merged the 3 already-verified trees from data/research/paris-verified.json (par_013-015) into paris.json: the Caucasian Elm of Square Samuel Paty (Zelkova carpinifolia, no individual age documented, the 1782 Paris-introduction date is species history only and the story says so plainly), the Oriental Planes of Square Michel-Foucault (two trunks, 470cm and 415cm girth, a few metres apart in one small garden, delivered as one entry per the collectible-point rule rather than two near-identical pages), and the Plane of Quai Saint-Bernard (weakest of the three, the register places a 380cm plane at this spot but nothing beyond the register singles out this exact trunk from others along the same quay; the story flags this honestly in the prose itself).

par_013 and par_014 sit 100m apart and 318-342m from the existing par_001 (Robinier of Square Rene-Viviani), forming a tight new pocket in the Latin Quarter around the Sorbonne and Notre-Dame. par_015 sits 587-641m from the existing Jardin des Plantes cluster (par_002, par_004). Fixed the city's own stale "ten"/"nine more" count-promise copy in five places (intro, meta_description, question_meta, two FAQ answers), caught by the build's count-promise check before it would have shipped a false count. All 3 photos are honest `missing` gaps for a future photo_hunt.py pass; none hunted this pass (write/merge only).

One lead recorded from this pass, not yet in data/leads/paris.json: the same pocket garden at Square Michel-Foucault also holds an Amur cork tree planted 1925 with a lightning scar and a trunk that balls up beneath the branches (per paris.fr), a strong future candidate in an already-walkable cluster.

## 2026-08-07 - Photo queue: 3 approved, 1 held, and an egress block worth flagging

Judged 24 of the photo queue's 337 candidates (the only ones reachable this session; see below). Approved pad_002 (Padua, Orto Botanico plane, identity corroborated by the garden's own trunk label visible in a sibling photo from the same iNaturalist observation, "PLATANO ORIENTALE ... A.1680"), pad_003 (Padua, Orto Botanico ginkgo, same-observation label "GINKGO BILOBA ... A.1750"), and tor_006 (Turin, Eridano-bank plane, geotagged 12m from the confirmed pin, nearest other monumental plane 374m away). Held lis_013 (Lisbon, Principe Real strangler fig): a genuinely good photo, but the square holds three similar figs and the entry is defined as "the thickest of the three," so attaching an unconfirmed one would be a guess dressed as fact, same pattern as the Margaret Island hold. 20 rejected, mostly leaf/bark close-ups and straight-up canopy shots (iNaturalist is a species-ID site, not a photography one; yield was 3 of 24).

**This session's egress proxy returns 403 on CONNECT to `upload.wikimedia.org` and `api.openverse.org`**, not a timeout or a flaky host, an outright block. That took 313 of the queue's 337 candidates off the table, including all 18 Wikidata-sourced ones this run was pointed at (17 turned out to already be judged by an earlier pass the same day; only seo_008, Seoul's Jogyesa Pagoda Tree, is genuinely still open). Left unjudged rather than approved blind. Worth an allowlist fix if future sessions in this environment keep landing on photo work, since it silences over 90 percent of the queue every time.

## 2026-08-07 - New York gets its first walkable cluster (Central Park)

New York's original 10 trees, scattered one per borough-park, had zero clusters (checked directly, 900m single-link radius produces ten singletons). No US national tree register exists, but NYC Parks runs its own official "Great Trees of New York City" register (started 1985, expanded 2024), and it turned out to solve the problem the same way a European register would.

Verified and published 3 trees around the existing nyc_002 (Black Tupelo of the Ramble): nyc_011 the Great Elm of Central Park West (one of 23 elms left on the park's west side by a 1985 New York Times count, out of roughly 500 originally planted), nyc_012 the Elms on the Rocks (two register-listed elms folded into one entry, growing out of a Manhattan schist outcrop), and nyc_013 the Elm Allee of Literary Walk (an ensemble entry for the Mall's famous elm promenade, judged against the Meiji Jingu Gaien collectible-ensemble precedent). Caught and corrected a real age myth along the way: press coverage implies the Mall's elms date to the park's 1858 design, but Central Park Conservancy's own material states the current row is the THIRD planting, from the 1920s, after the first two failed to soil compaction. Softened a superlative per hard rule 8 ("largest grove of American elms in the world" to the Conservancy's own "one of the largest remaining plantations"). All three flagged: no source dates any of them precisely, and pins are approximate (landmark/street reference points, not surveyed trunk coordinates).

The three sit within 600m of the existing anchor, forming a real computed walk (1.4km, 19 minutes, confirmed in the built page's own WALKS data), New York's first. 5 more leads (a second, more northerly Central Park cluster around the Reservoir) recorded in data/leads/new-york.json. Fixed two stale count-promises in New York's own copy ("eight more" / "nine more Great Trees"), caught by the build's own check. Cost: 55k verify + 8k write for 3 trees, ~21k/tree, close to the 15k target thanks to the register.

## 2026-08-07 - Edinburgh's approximate pins: three dead ends worth recording

Dispatched a precision-only pass on Edinburgh's 8 approximate pins (out of 10 trees), the largest single gap of any published lead city. Zero upgraded to confirmed, an honest result, but three specific leads are worth recording so a future pass does not repeat them: **edi_002** (Sweet Chestnut of the Botanics) has 4 Castanea sativa accessions in RBGE's own Garden Explorer database but none labelled "Pond Lawn" or carrying a planting date, so none can be matched to this specific named tree without a better source. **edi_004** (Cedar of Lebanon at the Botanics) has one nearby iNaturalist observation tagged Cedrus libani, but it is a single computer-vision identification with no second identifier and no research-grade consensus, too thin to trust given this exact tree already had one prior misidentification caught by an earlier pass (it was briefly approved as an Atlas Cedar by mistake). **edi_001** (Craigmillar Castle Yews) has a Canmore grid-reference designation but the individual-tree page redirects to trove.scot, which 403s every fetch attempt; the wider Historic Environment Scotland Garden and Designed Landscape polygon is not tree-level precision. edi_006 through edi_010 were not reached in depth this pass.

## 2026-08-07 - Berlin gets its first walkable cluster (3 Pfaueninsel oaks)

Berlin's original 10 trees span 29km with no two closer than 0.66km apart and only Tegel Forest's Dicke Marie/Humboldt Oak pair even that close, so the city had no walk at all against the phase's "deep enough" bar (one complete walk of 4-8 trees inside roughly 2km). No German register is imported (fragmented per-Bundesland, no verified open licence), so this was web research: named-place search on Pfaueninsel, Peacock Island, a small ferry-only UNESCO-listed park with four legally designated Naturdenkmal oaks.

Verified and published 3 (ber_011 The Great Oak of Pfaueninsel, ber_012 the Tuereiche/Door Oak, ber_013 the Pond Oak north of the Wasservogelteich), all `flagged`: ber_011's two sources agree on girth (565-567cm) and location but neither dates the tree directly, so the age is a wide, honest 200-400 year bracket from the island's own landscaping history (Friedrich Wilhelm II's gardeners deliberately kept century-old oaks when building the royal garden from 1793). ber_012's two sources give identical dimensions, likely one underlying survey rather than two independent looks, and carry a genuine unresolved species conflict (Quercus petraea vs Quercus robur) stated plainly in the data and the story rather than picked. ber_013 was pinned via a stranger's geotagged 2024 Commons photo matching the official register's bearing-and-distance description to within about 10m.

The three sit 140-950m apart (single-link chained through the 900m walk-cluster radius), forming a real computed walk: 1.4km, 19 minutes, confirmed in the built page's own WALKS data. A fourth registered oak (ND 6-101/B, near the ferry landing) and a separate Charlottenburg/Lietzensee thread (5 more register-only leads, no coordinates, no second source) stayed unresolved in data/leads/berlin.json for a future pass; two follow-up passes tried and failed to close ND 6-101/B (no Commons geotag, no working Berlin Geoportal endpoint within the time box).

Cost was high for the yield, roughly 183k tokens across three verify passes for 3 trees (61k/tree against the 15k target), because Berlin has no register to lean on; recorded honestly in data/agent-costs.json rather than smoothed over. Fixed two stale "ten trees" count-promises in Berlin's own intro and FAQ copy (caught by the build's own check) and updated the "free to visit" FAQ answer, since the Pfaueninsel oaks need a paid ferry crossing (6 euros) the same way the Treskow Plane needs a zoo ticket, four of Berlin's 13 trees now behind some ticket rather than one.

## 2026-08-07 - Rome deepens to 20 trees, an Esquilino pocket opens

Merged the 4 already-verified trees from data/research/rome-verified.json (rom_017-020) into rome.json: the Magnolia of Via Corsini (Rome's oldest per RAMI, ~275 years, planted mid-1700s as part of the Corsini palace garden before the neighbouring Orto Botanico existed as a public institution), the Cedar of Lebanon of Villa Torlonia (the thickest cedar on Rome's monumental register, no dated planting record so the story states an honest 150-220 year estimate tied to the site's own history rather than a document), the Podocarp of Piazza Vittorio (a botanical rarity, undocumented age stated plainly), and the Chir Pine of Colle Oppio (brought from the Himalaya by Giuseppe Tucci, already standing at the garden's 1936 opening above the Domus Aurea, alive and healthy per a late-2025 register check but the story also states the honest risk that the ruin's own redesign has previously floated removing tall trees above it for root damage).

rom_017 joined the existing Monteverde/Trastevere walk (7 to 8 trees, 109m from rom_003). rom_019 and rom_020 are 534m apart, a genuine seed for a second, Esquilino/Colosseo walk, but sit one tree under the site's walk-formation minimum, so they render as honest unclustered dots for now rather than a forced walk. A future pass adding one more nearby verified tree (the Podocarp of Villa Sciarra's neighbourhood, or the unresolved Villa Torlonia stone pine noted in the verify_notes) would complete it. All 4 fixed the city's own stale tree-count copy (sixteen to twenty, in the intro, meta_description, question_meta and one FAQ answer), caught by the build's count-promise check before it would deploy. No photos hunted this pass (write/merge only); all 4 are honest `missing` gaps for photo_hunt.py.

## 2026-08-06 - Porto deepens to 17 trees, three University of Porto quintas

Verified and published 7 new trees (por_011 to por_017) off Portugal's ICNF register, extending Porto's walk east from the two existing gardens into three adjoining University of Porto sites along a roughly 720m corridor: the FAUP architecture campus (a Copper Beech, the grounds themselves an Alvaro Siza pilgrimage site for architects), Casa Primo Madeira/Quinta Primo Madeira (an Atlas Cedar, a Tulip Tree, a London Plane, restored by architect Fernando Tavora), and Palacete Burmester on the Faculty of Sciences campus, a few hundred metres from the already-published Botanical Garden cluster (a Horse Chestnut and a European Yew, both undated by the register and left that way in the story rather than guessed).

One tree, the Camphor Tree of Via Panoramica, stands on a privately owned plot beside a public scenic road; shipped with an explicit, unsoftened access note (viewed from the pavement, the land itself is not open, the municipal source itself flags the plot has development potential) rather than blocked outright, since the tree itself is genuinely visible and reachable-to-stand-in-front-of from public ground, which is what hard rule 10 actually tests. Two same-species trees at Palacete Burmester (a second Himalayan Cedar, a second Tulip Tree) held back as leads only to avoid crowding the page with duplicates of species Porto already publishes, not a quality failure.

Fixed Porto's own count-promise copy in the same pass: the intro, meta_description, question_meta and two FAQ answers all said "ten trees" or "two gardens", caught by the build's own contract check (the same class of bug the country-page and Lisbon fixes caught earlier today) rather than by eye. Also set an explicit `oldest_tree_id` (por_001, the well-documented 250-year Casa Tait tulip tree) because the mechanical highest-age_max winner would otherwise have been por_017, the undated yew whose own story says printing a number for it would be dishonest.

## 2026-08-06 - Padova opens (9 trees), Barcelona deepens (32 trees), and Andalusia's rediam register is confirmed structurally rural

**Padova published, 9 trees inside a 1.25 km walk.** Finished the verification the last session had left sitting unpublished (data/research/padova-verified.json existed, no data/cities/padova.json did): a write-stories pass turned it into prose, merged into a new city file, and added the missing data/city-list.json entry (its absence was why the first build silently dropped the city with zero errors). Four trees in the 1545 Orto Botanico (the Goethe Palm at ~440 years, an Oriental Plane, a grafted Ginkgo, a 1786 Magnolia), a magnolia in the Sant'Antonio basilica cloister, two planes and a leaning hackberry in Parco Treves, a folded twin-tree Sophora entry in Piazza Capitaniato. All `curation_status: "flagged"` entries keep their hedge in the prose per BRIEF_WRITING.md: pad_007's age is inferred from its neighbour, pad_008 explicitly does NOT repeat an uncorroborated storm anecdote from an earlier unverified lead. 0 photos this pass (writing/merging only, no hunt run). Full verify_notes archived in data/research/padova-verified.json before they were stripped for the story field.

**Barcelona deepened from 22 to 32 trees**, the two untouched clusters an earlier pass had flagged but never evaluated: the Palau de Pedralbes/Torre Girona gardens (a stone pine predating the royal palace built around it, a 23-tree Himalayan cedar grove, a genuinely rare Barbary Thuja, three Torre Girona specimens whose register "Privat" ownership tag turned out to be stale, the garden transferred to municipal public management in 2019) and the Vil.la Amelia gardens in Sarria (a London Plane, a Tasmanian Blue Gum, a Peruvian Pepper, a 14-unit Canary Island Palm double avenue). Two multi-unit register entries (the cedars, the palms) were judged collectible ensembles on the same precedent as bcn_010 and the Meiji Jingu Gaien avenue, both flagged for an unmeasured spread or a source count discrepancy rather than for collectibility itself.

**The rediam "place" field is the register's PROVINCE, not the city, and it makes most of the Andalusia backlog candidates unusable as they stand.** Checked before dispatching anything: backlog.py's top Spain "new page" candidate, a 7-tree cluster labelled "Huelva" (2.9 km spread), sits at 37.88,-6.52, about 70 km north of Huelva city itself, and every tree in it is named "de El Chaparral" or similar, i.e. a named Cortijo (rural farmhouse/estate), a strong signal of private agricultural land rather than a public city garden. The Cordoba, Almeria and Malaga clusters lower on the same list show the identical pattern (comment in scripts/backlog.py itself: "the Andalusian register files by province, so these double as both"). This confirms and extends what the prior session already found and logged in LOG.md for the same reason. Not re-researched or published; recorded here so a future run does not re-discover the same 70 km gap from scratch. Deepening a city the register already ties to real, walkable, verifiably public coordinates (as Barcelona's municipal AIL register does) is the safer and cheaper move until Andalusia's entries are checked tree-by-tree against a real city radius.

## 2026-08-06 - Photo pass across five image-less cities: Krakow 3, the other four empty

A dedicated photo pass over the five published cities that had zero photographs between them (Krakow, Budapest, Zurich, Oslo, Reykjavik). Cap of three per city, Cadiz standard applied, every candidate downloaded and viewed as pixels before any decision. Krakow is now done; the other four are recorded here as dead ends so no future run repeats the same searches.

**Krakow: 3 approved, 1 honest gap.** Polish Wikipedia's `Pomniki przyrody w Krakowie` turned out to be the single best source for this: it is a full table of the city's 362 natural monuments with a Commons image against most rows, which is where all three came from. kra_001 the Jagiellonian Oak (Jerzy Opiola, CC BY-SA 4.0, whole tree, blue sky, garden labels visible at the base); kra_002 the Henryk Oak (Janusz Krzyzek, CC BY-SA 4.0, golden-hour roadside shot, the register row for ul. Zakopianska 121 confirms the identity, which a web search independently tied to Dab Henryk); kra_004 the Sniadecki Dogwoods (Janusz Krzyzek, CC BY-SA 4.0). A second dogwood file shows the multi-stem base with the `JANA SNIADECKIEGO` plaque legible, which is what confirmed the identity, but its crown is cut off so the whole-tree frame was taken instead.

**kra_003, Poland's oldest black locust, stays missing.** There is no photograph of it anywhere under an open licence: it is absent from the Wikipedia monument table, absent from `Category:Plants in botanical garden in Krakow`, and the only Commons black locust in Krakow is a different tree on ul. Smolensk. Do not re-run this hunt.

**Budapest: 0 approved, 5 gaps.** Two finds, neither usable. The `Tabani eperfa mentese` photos (Saly Noemi, CC BY-SA 4.0) are the right tree but were shot during the 2021 FOKERT rescue: flat grey light, a tarpaulin over the trunk in one and a work crew filling the frame in the other. `Tabani Botanikai Tanosveny. Szederfa (Morus alba)` is a young sapling shot upward into the canopy, not the ancient mulberry. The two `Margitsziget-GiantPlaneTree` files (Illustratedjc, CC BY-SA 4.0) are genuinely excellent photographs of an enormous plane, and they were rejected anyway: the description says only "a very large Plane tree on Budapest's Margaret Island", there is no EXIF GPS, and Overpass shows the island has at least three separately named notable planes (Het Vezer platan, Borika faja, A Margitsziget legmagasabb platanfaja), so attaching one to bud_001 or bud_005 would have been a guess dressed as a fact. Worth revisiting only if someone geolocates those two files. Nothing at all exists for the Buda Castle pagoda tree or the Erzsebet ter black locust.

**Zurich: 0 approved, 4 gaps.** The Lindenhof limes have two Commons files (Roland zh, CC BY-SA 3.0) but both are shot upward from below the retaining wall on Fortunagasse, bare, with no trunk base and no whole-tree read. Platzspitz is heavily photographed and every geosearch hit is the park bandstand, the Landesmuseum or the Street Parade, never the 1780 planes as a subject. iNaturalist has nothing within 300m of either sequoia (Belvoirpark, Hohlstrasse) or of the Platzspitz planes; its single Lindenhof lime observation is a leaf close-up.

**Oslo: 0 approved, 4 gaps.** Nothing on Commons for Munch-eika under any spelling, and iNaturalist returns zero open-licence observations within 300m of all four trees. Birkelunden and Slottsparken geosearches return the fountain, the tram stop, the flea market and the palace, no tree as a subject.

**Reykjavik: 0 approved, 4 gaps, as expected.** The only relevant find is iNaturalist observation 34381075, a CC0 Scandosorbus intermedia standing 10 metres from the rey_001 pin, so it is certainly the Vikurgardur whitebeam, but all three of its photos are hand-held leaf-and-berry close-ups. Commons has nothing for the Holavallagardur larch, the City Hall maple or the Ellidaarholmi spruce.

The pattern across all five: Poland and Hungary have strong Wikipedia coverage of protected trees, but only Poland attaches whole-tree photographs to it. For the other four cities the supply ladder is exhausted and the next photograph will realistically come from a reader submission, not from another search.

## 2026-08-06 — Guimaraes opens: 4 trees, register-first, exactly at the floor

Guimaraes (UNESCO World Heritage historic centre, Portugal), found via `scripts/backlog.py --new`: a 14-tree ICNF register cluster within 3.4 km, untouched by any prior session. Dispatched a bounded research pass off the register leads; full incremental record in `data/research/guimaraes.md`.

**4 shipped**: the twin plane trees on the lawn below the Paco dos Duques (confirmed, ~165y), eighteen camellias across two parterres at the Palacio Vila Flor folded into one ensemble entry (confirmed, ~195y, Guimaraes' oldest and part of Portugal's own Camellia Route), three Himalayan cedars at the gates of the Atouguia municipal cemetery folded into one entry (confirmed on the one dated tree at ~115y, the other two undated), and the olive tree in the cloister of Nossa Senhora da Oliveira, carrying the city's founding miracle legend (1342) but shipped `flagged` since no source ties this specific trunk to that date and the register itself gives no age.

**3 held back, all judgment calls, recorded in `data/leads/guimaraes.json`**: Casa de Margaride (an 2024 Portuguese Tree of the Year camellia among rare 18th/19th-century cultivars) and Casa da Covilha (the single oldest dated tree in the whole Guimaraes register set, 300y) are both private estates with owner-guided visits only, no standing public hours found, so held on hard rule 10 rather than guessed open. Santa Marinha da Costa (an oak beside a baroque water tank in a former monastery, now a hotel) was the research pass's own recommendation to ship, but is held back on review: the property's own material says the grounds were restored "for guests and visitors," which is suggestive but not a clear public-access statement, and the rule is leave it out when in doubt. Its register age (290y, applied across a conjunto that includes eucalyptus, a 19th-century introduction to Portugal) was unreliable regardless.

**Photos**: 2 candidates found for the plane trees (Wikimedia Commons, CC BY-SA 3.0, matched pair, geotagged), but no image-rendering tooling was available this session to view the pixels, so both stay `found_needs_check` per the Cadiz rule rather than approved on a filename. Worth a look by a session that can render images.

Site rebuilt (1,097 pages), all contracts validated, `scripts/qa.py` clean. `scripts/tree_index.py` re-run.

## 2026-08-05 — two species with no season on record

Giant Sequoia and Moreton Bay Fig carry no flowers, fruit or autumn colour in
data/phenology/, so their 25 tree pages now show a plain sentence instead of a
year chart. For the sequoia that is probably right: it has no moment a visitor
would notice. For the Moreton Bay Fig it is a gap, not a fact, because the tree
does fruit and the fallen figs stain pavements in Palermo, Seville and Valencia.
Needs two sources and a month range before it can be filled. Not urgent: an
honest blank beats an invented season.

## 2026-08-05 — the Old Lions of Kew, a collectible-point question

lon_009 carried the species "Multiple species including Japanese Pagoda Tree
(Styphnolobium japonicum)", which broke the hard rule 9 check because it is not
a species name. Set to Japanese Pagoda Tree, since the scientific name in the
entry already commits to one species. The underlying question is bigger and is
NOT settled here: the story itself says the five Old Lions span the Kew site
rather than clustering, which is the same test the Rambla planes failed. Worth
a decision: either the entry becomes the single pagoda tree at its pin, or the
Old Lions come off the page.

## 2026-08-05 — Zaragoza researched and deliberately not published

Four trees verified on a 1.65 km walk, and the page is held back, because the
source that made the city cheap is also the reason it cannot ship yet. The
city's 2006 book "Arboles Singulares de Zaragoza" carries 68 fichas with GPS,
dimensions and ownership per tree, and it is not a list of living trees: an
arborist reviewing it reckoned nearly half were gone or in poor condition by
2012. Two of the nine checked in this pass are confirmed dead. Ficha 54, the
Parque Bruil hackberry, dried out, was carved into a sculpture in 2017 and the
sculpture itself was felled in 2022; it was going to be the lead entry. Ficha
12, the Parque Bruil honey locust, fell in the winter of 2014 and had already
been written into the file before the check came back.

So only one of the four has dated proof of life, and the floor is four verified
trees. The research is kept in data/research/zaragoza.json and
data/leads/zaragoza-register.json (68 fichas, no open licence: the book states
copyright over its texts and photographs, so it stays out of data/registers/).

Two more cautions in the file: the book's coordinates are ED50, and a naive
conversion puts every pin about 200 metres northeast of its tree, so both values
are stored with the wrong one named; and three fichas print another tree's GPS
string, which is why every pin is approximate.

**The cheapest way to unblock Zaragoza** is the 2019 "Arbol Singular Urbano de
Zaragoza" catalogue, reported as 56 trees plus 15 conjuntos. No run has found
the document yet. Inclusion in it would be the city confirming what still
stands, which is exactly what the 2006 book cannot do.

## 2026-08-06 — the 26 unchecked photos, approved on sight by Hidde

They had been live for weeks with status `found_needs_check`, which reads as
"kept back" in CLAUDE.md and in fact renders on the site. Rather than pull a
page's only image over a risk a reader can report, they were put in front of
Hidde as one contact sheet in the site's own card crop, and he judged them all
good enough. Status is now `approved` across the board.

Worth knowing what that approval is and is not: it is a human looking at 26
thumbnails at once, not 26 individual verifications against the Cadiz standard.
If one of them turns out to be the wrong tree or a bark close-up, it was
approved on a glance and can go without ceremony. The three the reviewer was
asked to look at hardest were the Trsteno planes at Dubrovnik (an arboretum,
where a park view is the likely failure), the cedars of Parc Beaulieu in Geneva,
and Florence's zelkova.

## 2026-08-06 — black and white photos were live, and the rule had no check

Hidde spotted a greyscale photograph on Rome's Cedar of the Garibaldi Mausoleum.
The rule is from 2026-07-31 and is unambiguous ("liever geen foto dan zwart-wit"),
and nothing enforced it, so a pass approved one and it sat there.

`scripts/photo_colour_check.py` now measures it instead: it fetches each live
photo at thumbnail size and computes mean saturation, and anything under 12 is
greyscale in practice. Two came out certain and are removed, rom_007 and
ant_001. One is borderline and left alone for a human look: Florence flo_002,
the cork oak of the Giardino dei Semplici, at 10.7, which reads as a very
desaturated colour photograph rather than a black and white one.

Caveat on that scan, and it matters for whoever runs it next: Wikimedia returned
HTTP errors for a large share of the fetches, so this pass covered only part of
the 306. Run it again with a slower request rate and a proper user agent before
concluding the site is clean. Making it a build check is the obvious next step
and was not done today, because a build that fetches 300 images on every run is
the wrong shape; it belongs in the daily digest or in qa.py behind a flag.
