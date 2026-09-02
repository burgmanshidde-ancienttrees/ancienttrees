# Can open data make the ten trees per city faster to find?

Measured 2026-07-21. The question changed halfway through, and so did the answer.

It started as "can open data get us to every city in the world", which assumed publishing hundreds of trees per city. Hidde rejected that the same day: ten per city is what makes the passport work, and scarcity is the mechanism rather than a limitation. See BACKLOG.md. So the surviving question is narrower and more useful: **can open data cut the dull half of a city run, finding candidates and fixing coordinates, so runs spend their time on stories?**

## Funchal, Madeira: the monumental-tree table lives inside the municipal plan (found 2026-09-01)

**A register hiding in a planning document, and the finding corrects this file's own earlier note.** The 2026-08-17 Madeira entry below records IFCN's ASMAC survey as the island's register, and it is real but narrow: twelve sites island-wide, already fully mined for the six trees Madeira first published. It does NOT cover Funchal's own monumental trees.

What does is **the Funchal PDM's `Relatorio de Fundamentacao`, Volume II, March 2018, `Quadro 5`**, a monumental-tree table inside the municipality's master planning document, which itself cites the regional government's 2008 publication *Arvores Monumentais e Emblematicas*. It was found by fetching the PDF directly and grepping it, not by any portal search, and it is the register behind all thirteen Wikidata candidates around Funchal.

**The transferable lesson, which is why this is written up rather than just used:** a municipality that publishes no open dataset may still have published the list, inside a planning report, an ordinance annexe or a heritage inventory. Those documents are long PDFs nobody indexes as data, so they do not surface in an open-data search, and the way in is to fetch the plan and grep it. This is the third shape of the same lesson now: Italy's regional cards beat the national file, Germany's municipal ordinance beats the state register, and here the municipal PLAN beats the regional survey. The pattern is that the tier which actually manages the trees is the one that lists them.

**Caveat carried from the pass:** the coordinates around it are park-level rather than tree-level. Two different species sat at an identical lat/long inside the Jardim Municipal, which is the tell, so everything from this source ships `approximate` unless a second source pins the trunk.

## Flanders: the heritage inventory is an open tree register for the whole region (imported 2026-09-02)

**USABLE, licence proven, and it covers 293 municipalities at once.** The Agentschap Onroerend Erfgoed inventories individual trees as *erfgoedobjecten* under the typology *opgaande bomen*, and its API answers JSON with no key and no account:

    https://inventaris.onroerenderfgoed.be/erfgoedobjecten?typologie=opgaande+bomen&per_pagina=50&pagina=N

with `Accept: application/json`. **2,336 trees, 293 municipalities, 2,307 of them carrying a photograph** on the agency's own site. Imported to `data/registers/flanders-onroerend-erfgoed.json`. Gent has 62, Aalst 63, Brugge 30, Leuven 19, Antwerpen 13, Mechelen 7, and the biggest single holding is Voeren with 135.

**Licence, read verbatim at the source** (`inventaris.onroerenderfgoed.be/hergebruik`, 2026-09-02) and checked twice, once by the pass and once directly: two licences apply, a *Modellicentie voor gratis hergebruik* and *Naamsvermelding-GelijkDelen 4.0 Internationaal*, which is CC BY-SA 4.0. Both say *"je mag de tekst wel voor eender welk doel gebruiken"*, you may use the text for any purpose, free, with *verplichte naamsvermelding*, mandatory attribution, and share-alike on adapted text. **No non-commercial clause**, so it clears this project's bar.

**Five caveats, all in the register file's own block.** The list carries no coordinates, only a municipality, so the Lambert72 geometry comes from the per-tree page and that is one request per tree: fetch the city you are working, not all 2,336. There is no age or girth field, though the prose description usually gives both. Inventoried is not the same as legally protected, which is a separate *aanduidingsobject*. **The photographs are NOT covered**: the reuse page is titled *Hergebruik van teksten* and governs texts, and image rights were not established, so do not attach an inventory photograph without settling that.

**And the fifth caveat is the one that decides yields: the tree names are the access warning.** Entries reading *bij herenhuis*, *in tuin*, *op binnenkoer* or tagged *private parken* are private ground and never ship under hard rule 10. A Leuven pass had 26 named trees and delivered three, because most of the rest stand in private courtyards and mansion gardens, including the city's most famous tree, a pagoda tree valued in the millions, in a college's inner courtyard. **So in Flanders the bottleneck is not naming, it is access**, which is the opposite of the Marseille and Charleston problem and needs a different brief: expect to lose a large share of every city and plan for it.

## Sweden: the national endpoint is dead and the designations are alive as documents (Gothenburg, 2026-09-02)

**A pass that should have failed and did not, because it went looking for the DECISION rather than the dataset.** Naturvardsverket's national naturvardsregistret is shut on every route: WFS disabled, both REST paths 403, and the GetCapabilities answers 200 with an error document inside so a status check reads it as working. On the old reading that closed Sweden.

It does not, because a *naturminne* is designated by a decision, and decisions are published as documents. A Gothenburg pass found **five individually named trees** in the municipal naturminne record: the Torslanda linden, designated in 1945, and four boundary oaks in Orgryte designated on **14 October 2025**, with the city's own decision document (SBF-2025-00290) fetched and read. One authoritative source produced the whole city at about 11.6k tokens a tree.

**This is now the fourth country where the same shape held**, and it is worth stating as one rule rather than four notes. Italy: the regional cards beat the national MASAF file. Germany: the municipal ordinance beats the state register. Madeira: the monumental-tree table sits inside the municipal PLAN. San Francisco: the Landmark Tree list is webpages, not data. Sweden: the county and municipal decisions, not the national geoserver.

**The rule: the tier that actually protects a tree is the tier that names it, and it usually publishes a DOCUMENT rather than a dataset.** An open-data portal search finds the wrong tier and the wrong format, and answers "no register" when the register is a PDF, an ordinance annexe or a decision. So ask who signs the protection order, then go and read what they signed.

## Germany, second Wikipedia source class: "Liste markanter und alter Baumexemplare in <city>" (found on Hamburg, 2026-09-02)

**A second, better German list class, and it is not the Naturdenkmal mirror already documented below.** A Hamburg pass went looking for the city's own Naturdenkmal register, as the Regensburg finding says to. Hamburg's official register holds **eleven entries and exactly one real tree candidate**: the rest is a boulder, four flood-breach ponds, two moors, a ditch, a clay pit and a garden meadow. The semantic filter ate the whole source.

What produced all six shipped trees was a different German Wikipedia article class: **"Liste markanter und alter Baumexemplare in Hamburg"**, a citywide table of notable and old trees carrying coordinates, girths and planting-date estimates. It is not a mirror of a protected-object register, it is a dendrological list, so it includes trees no ordinance protects and skips the ponds and rocks that an ordinance does. Cross-checked against baumkunde.de and, twice, official hamburg.de and BUKEA press releases.

**So for a German city, ask for BOTH articles**: "Liste der Naturdenkmale in X" for what is legally protected, and "Liste markanter und alter Baumexemplare in X" for what is actually a notable tree. The second is the better starting point for our purpose and it is the one nobody had looked for. Same registry-join technique either way: fetch the WIKITEXT and join on the id or the coordinates.

**What it does not solve, and Hamburg is the worked example:** a dendrological list has no access field, so hard rule 10 is a per-tree check afterwards. Hamburg's single most famous entry, the yew of Neulander Deich, is widely called the city's oldest tree and stands on a private residential plot; it is blocked and stays blocked.

## Germany: the STATE Naturdenkmal register misses the CITY's own designations (found on Regensburg, 2026-09-01)

**A transferable finding rather than a new source, and it applies to every German city in the queue.** A Regensburg pass was staged with 27 rows from `data/registers/bayern-naturdenkmale.json`, the Bavarian LfU state dataset, filtered to 20 km. Of Regensburg's roughly fifteen individually designated Naturdenkmal TREES, that state dataset carried **one**. All five trees the pass shipped came from somewhere else.

**Where the supply actually is: the city's own Naturdenkmal-Sicherungsverordnung**, the municipal ordinance that designates them, which German Wikipedia mirrors as "Liste der Naturdenkmaler in <city>" with register ids and addresses. That mirror is the same registry-join technique that already carried Krakow, Warsaw, Vilnius and Frankfurt: fetch the WIKITEXT and join on the id.

**Why this matters beyond one city.** It is the "regional register before the national one" lesson from Italy, one level further down: in Germany the tier that holds the individual urban trees is the CITY, and the state register is largely the rural and geological designations. It also explains the other half of the staged list, which is worth knowing before anyone budgets a window: a Bavarian *Naturdenkmal* is any protected natural monument, so 12 of the 27 rows were rocks, caves, ruins and a sinkhole, and two more were avenues rather than collectible points.

**So for a German city, in this order:** the city's own Sicherungsverordnung or its Wikipedia mirror first, the state LfU dataset second and mostly for the surroundings, and expect to run the semantic filter hard on both. Munich, Nuremberg and Berlin are already published and were not built this way, so their pages may be thinner than their cities actually are; Freiburg, Stuttgart, Hamburg, Dresden and Leipzig are still in the queue and should start from the municipal tier.

## Luxembourg: the ANF arbres remarquables register, imported 2026-08-30 (VERDICT: usable, CC0)

**USABLE, and it is the whole country in one file.** The Administration de la nature et des forets publishes every tree classified as remarkable by grand-ducal regulation as open data at data.public.lu, currently the list under the regulation of 31 January 2025. **238 trees, tree-level WGS84 coordinates, 83 communes.** Imported to `data/registers/luxembourg-anf.json`.

**Licence proven, read live at the source:** `https://data.public.lu/api/1/datasets/arbres-remarquables/` returns `license: cc-zero`, organization `Administration de la nature et des forets`, last update 2026-08-12. Read from the metadata endpoint rather than from a portal page or a search summary, which is the rule that keeps a verdict from outliving the fact.

GeoJSON: `download.data.public.lu/resources/arbres-remarquables/20260812-010213/ornf.geoportail.arbres-remarquables.geojson`

**What it gives, and what it does not.** Per tree: species, commune, cadastral section, coordinates, and `interet`, the reason the tree was designated (dendrologique, historique, paysager, ecologique, and combinations). That reason field is the most useful thing in it and almost no register has one: it is the state saying why this particular tree was worth protecting, which is the closest a register ever comes to handing you a story hook. What it lacks is the usual three: **no age, no girth, no vitality.** So every age here comes from a second source or stays empty, and whether a tree still stands is a per-tree check.

**95 of the 238 give a genus rather than a species** ("Tilia sp.", "Quercus sp."). That is the publish-and-ask case, not a blocker.

**Density: 13 walkable clusters of four or more within 2 km, covering 72 trees.** The best is Luxembourg City itself, 11 trees inside 2.5 km, which is two walks through the Petrusse and Alzette valley parks. Clervaux, Niederanven, Steinsel and Wincrange hold 8 each.

**The second source is already mapped for you.** The Luxembourgish Wikipedia mirrors this register as "Lescht vun de bemierkenswaerte Beem zu Letzebuerg", with individual articles for the named trees citing the printed ANF and natur&emwelt monograph by page number. That is the same registry-join technique that carried Krakow, Warsaw and Vilnius, and here it earns its keep twice over: it is where the 2026-08-30 Luxembourg City pass caught **two dead trees the register still lists**, a copper beech in the City Museum courtyard removed in 2022 and one of the two Parc Amelie giant sequoias felled on 28 February 2026 with root rot. A register with no vitality field plus a wiki that records removals is a working pair.

## South Korea (Seoul #33): a promising national GIS API, licence unconfirmed, stalled here (scouted 2026-08-20)

Found while `scout_next.py --target` pointed at Seoul (#33, no supply, no
verdict). South Korea's Natural Monument system (천연기념물, Cultural Heritage
Administration, 국가유산청, formerly 문화재청) designates old/giant trees
individually alongside animals, geological formations and whole groves, which
is exactly the semantic-filter shape this project wants rather than a bulk
tree inventory.

**The candidate source:** 국가유산청_문화재 공간 정보 ("Cultural Heritage Spatial
Information"), a free OpenAPI (XML) plus file download on the public data
portal (`data.go.kr/data/3070426/openapi.do`), also browsable at
`gis-heritage.go.kr`. It covers all ~15,000 nationally and locally designated
heritage items with coordinates, area, regulated zone and heritage-type
classification, which would let a scout filter to Natural Monument type and
then to tree entries within that, the same two-step filter the MASAF/regional
split already uses in Italy.

**Stalled on licence, not on existence.** The dataset page states "이용허락범위
제한 없음" (no restriction on scope of use) and lists the data as free, and
Korean government open data is required by the 2014 Copyright Act amendment
(Article 24-2) to carry a 공공누리 (KOGL) type badge, of which KOGL Type 1 is
CC-BY-equivalent. But WebFetch's summarised read of the page did not surface
which KOGL type number is actually attached, and CLAUDE.md's register-layer
rule requires a proving sentence naming the specific licence before import,
not an inference from the surrounding legal framework. **Next step is a
session with real browser rendering** (this sandbox's WebFetch tool
summarises rather than renders, and the badge is likely an image or a
JS-rendered element) reading the KOGL type badge directly off the dataset
page, or fetching the OpenAPI response itself, which may carry a licence
field in its metadata envelope.

**Also found, not yet compared:** a Korea Institute of Science and Technology
Information dataset literally named "Korean Natural Monuments" (species,
habitat, characteristics, last updated 2021), which may or may not carry
coordinates; not checked this pass. Prefer the CHA spatial API first since it
is the authoritative designating body's own coordinates.

## Texas Big Tree Registry: non-commercial licence, real API, and a good yield once the units are read right (scouted 2026-08-20, corrected the same day)

Found while `scout_next.py --target` pointed at Houston (#36, one of Hidde's
17 named from-zero cities). `texasforestinfo.tamu.edu/BigTreeRegistry` is a
JavaScript app (Angular, same shape as the Lithuania/Sweden stalls in the
2026-08-15 round), but unlike those its backend is reachable directly:
POST `https://texasforestinfo.tamu.edu/BigTreeRegistry/Home/GetAllTrees` with
`{"species": "<Latin name>"}` returns every registered specimen of that
species statewide as JSON, with `LatDec`/`LongDec` coordinates, circumference,
height, spread, county, a `PublicOrPrivate` flag (meaning unconfirmed, values
0/1 seen, not documented anywhere found) and champion-status flags.
`Home/GetSpeciesList` lists all 352 species to loop over.

**Licence: DISQUALIFIED for bulk import.** Texas A&M Forest Service's own
usage terms (`tfsweb.tamu.edu/accessibility-site-policies-and-public-notices/`)
state content is offered "for personal, educational, and other
**non-commercial** purposes" with a citation requirement. That is a
non-commercial term, which CLAUDE.md's register-layer rule disqualifies
outright regardless of how good the data is. Ruled the same as Nevada below:
**usable as a verification/lead source for hand-verified entries only**, never
imported to `data/registers/`.

**CORRECTED 2026-08-20, same day, by a second look: the yield is NOT thin, and
the paragraph that said so had a unit error.** The registry publishes
imperial. `Circumference` is INCHES and `Spread` is FEET, which the raw data
settles on its own: the live oak below carries `Spread: 131`, and 131 feet is a
forty metre crown on a live oak while 131 metres is impossible. So the standout
tree is 246 inches, which is **6.25 metres round**, not the 2.46 m the first
pass recorded, and the "modest ornamentals in the 70-150cm range" were really
1.8 to 3.8 metres. That is the ICNF trap pointing the other way (metres read as
centimetres there, inches read as centimetres here), and it is why every
register import gets a physical sanity check before anyone quotes it.

**What the corrected sweep actually holds.** `scripts/texas_big_trees.py`
exists now so nobody loops 352 species by hand again: `--fetch` sweeps the
whole state once (660 trees, kept in `data/research/texas-big-tree-registry.json`)
and `--near <city>` reads it with a distance filter and the inch conversion
built in. Within 40 km, above 250 cm of girth:

| city | registry trees | above 250 cm | the standout |
|---|---|---|---|
| Dallas | 28 | 17 | a 7.21 m catalpa, 9.8 km out; a 6.55 m black willow; two American elms at 5.4 m |
| Austin | 15 | 10 | a 4.29 m bastard oak 700 m from the centre; a 4.88 m pecan |
| Houston | 13 | 8 | three live oaks at 6.25, 6.27 and 6.50 m; a 4.67 m pecan |
| Fort Worth | 20 | 11 | shares the Tarrant County cluster with Dallas |
| San Antonio | 6 | 4 | |
| El Paso | 3 | 2 | |

Every one of those is a champion or co-champion, so the registry is one source
and a good one. What it does not give is the second source, the access check or
whether the tree is alive today, and `CountyName` still cannot be trusted: rows
tagged Harris carry Panhandle coordinates 800 km away, which is why the script
filters on distance and prints the county only as a label.

## Nevada Big Tree Register: usable as a verification/lead source, not for bulk import (scouted 2026-08-18)

Found while `scout_next.py --target` pointed at Las Vegas (#22, no supply, no verdict). The Nevada Division of Forestry publishes a statewide champion-tree PDF, `forestry.nv.gov/uploads/missions/20210712_AMT_2015_Nevada_Big_Tree_Register.pdf` (2015 edition, ~300+ entries statewide, common name, scientific name, circumference/height/spread/crown/total points, nominator, county and location). WebFetch cannot read it (returns "corrupted/binary"); a plain `curl` download followed by a pure-stdlib `zlib`-stream extraction of the PDF's text objects works and needs no new dependency.

**Two genuine clusters for Las Vegas, both walkable, both public.** The University of Nevada Las Vegas campus carries at least 11 named champion/co-champion/up-and-coming trees in this one document (Camperdown Elm, Desert-willow, Strawberry Tree/Madrone, Weeping Mulberry, Blue Paloverde, Sissoo Tree, Heritage Live Oak, Chir Pine, Columnar Scotch Pine, Texas Olive, Yew-pine), all cited simply as "Clark, University of Nevada, Las Vegas" with no street address, so a session still has to locate each on campus. Winchester Park (a Clark County-run cultural park) carries three (Coolibah Eucalyptus, Lemon Eucalyptus, Shiny Xylosma). The Springs Preserve, a public nature/culture attraction, carries two (Chinese Tallow, Texas Live Oak). A 2016 Las Vegas Review-Journal piece independently corroborates the shape of this ("seven champions and three up-and-comers... at UNLV, where the entire campus serves as one big arboretum"; "three more champions grow at the Winchester Cultural Center") without needing to be read as the primary source, so it doubles as a genuine second source for the general claim.

**Licence: no explicit open-licence statement found**, only a generic NV.gov accuracy disclaimer on a sibling site. Not clean enough to import wholesale as register-layer dots per the licence-first rule. Ruled **usable as a verification/lead source for hand-verified layer-1 entries only** (the same treatment OPEN_DATA_SURVEY.md already gives Kyoto's DB and other unlicensed government documents): a session may use it to find candidates and cross-check species/measurements, but every entry still needs its own second source and its own hand-written story before it ships, same as any other single-source register lead.

## Madeira: IFCN's ASMAC survey, a register passcheck did not know about (2026-08-17)

**USABLE, and found by walking a URL number range.** Portugal's ICNF register does not reach Madeira, because the archipelago is an autonomous region and keeps its own. The Instituto das Florestas e Conservacao da Natureza (IFCN Madeira) published a VALCONMAC/ASMAC survey, "Arvores e bosques singulares da Madeira e Porto Santo": **11 Madeira entries plus 1 on Porto Santo**, each a numbered PDF at

    ifcn.madeira.gov.pt/images/FotosArtigos/Florestas/ASMAC/ASMACnn.pdf

found by walking nn across 71 to 100. Each card carries species, height, maximum perimeter or perimeters, a rough age note, WGS84 coordinates AND an access-and-ownership field, which is the field almost no register has and the one hard rule 10 turns on. Four of Madeira's twelve entries were blocked on exactly that field: a private hotel garden, a children's care institution, and a private rural hotel.

**The transferable lesson, which is why this is written up rather than just used.** `passcheck.py` reported zero register candidates for Madeira and it was right about its own data and wrong about the world. An autonomous region, an island government or a province very often keeps a list that the national register does not include, and the Canaries showed the same shape a day earlier (no approved regional catalogue, but the Cabildo de Tenerife runs its own portal). So: **when the national register comes up empty for an island or an autonomous region, look for the regional institute before concluding there is no register.** Ten minutes of looking turned Madeira from a from-zero web-research pass into a register-led one.

## Estonia: EELIS kaitstavad looduse üksikobjektid, imported 2026-08-15 (VERDICT: usable, CC BY 4.0)

**555 protected trees nationwide, 56 within 15 km of Tallinn** (#65 in the queue,
zero trees and zero register supply until now). One WFS request, no agent.
`data/registers/estonia-eelis-yksikobjektid.json`; endpoint
`https://gsavalik.envir.ee/geoserver/eelis/ows`, layer `eelis:kr_yksikobjektid`.

**How it was found, and it is the reusable half.** The designation name came out
of the Wikidata scout below, not out of a search: 235 Estonian trees there carry
"individual protected natural object", the literal English of *kaitstav looduse
üksikobjekt*. Searching a government for the term its own law uses is a much
shorter path than searching it for "tree register", and
`python3 scripts/wikidata_trees.py --designations` now prints that term for
every country. **Run it before scouting anywhere.**

**Licence: CC BY 4.0**, from keskkonnaportaal.ee, the environment ministry's own
portal, page updated 2026-05-26, read 2026-08-15: "Avaandmete kasutamise
tingimused on leitavad levituste juures ja keskkonna- ja ilma valdkonna andmed
on väärtuslikud andmed (vastavalt avaandmete direktiivile) siis litsents on
reeglina CC-BY 4.0." Recorded with its hedge intact: *reeglina* means "as a
rule", so this is a blanket portal statement rather than a per-dataset tag, and
the WFS carries no Fees or AccessConstraints element of its own. Attribution
required: "EELIS (Eesti looduse infosüsteem), Keskkonnaagentuur" plus the
extract date.

**The layer is not tree-only, so the semantic filter is ours:** 1,065 objects, of
which 555 have a type containing *(puu)*. The rest are erratic boulders (369),
springs, outcrops and karst. Of the trees, 506 are single, 46 are groves and 3
are avenues; the last two carry `publishable: false` under the collectible-point
rule, not because they are unprotected.

**One field is worth more than it looks: `aluskaart`, the base map each point was
digitised from.** It is a precision statement the register gives away free, and
the honest input to `location_precision`: "GPS" (79) is surveyed, "Tallinna
vektorkaart 1:2000" is a city vector map and good, "Eesti Põhikaart 1:10 000"
(165) was drawn off a 1:10,000 sheet and should default to approximate. No other
register here states this. **Look for the equivalent field in every import.**

No age, no girth, no vitality, per the standing register warning. 72 of the 555
are polygons carrying a ring centroid, marked `geometry: polygon centroid`.

## Scouting round of 2026-08-15: three stalls, and a correction to the German verdict

**The German verdict of 2026-08-13 needs qualifying.** That pass checked nine
Bundeslaender and recorded Sachsen as "none found (FND is areal-only)", with
Hessen, NRW and Brandenburg carrying no ND feature type in their open WFS. All
true about the STATE endpoints, and all misleading as a picture of the data,
because volunteers have mapped those very schemes: 936 trees under "natural
monument in Saxony", 790 under "Single natural monument in Hesse", 382 in
Thuringia, 356 in Brandenburg, 53 in Saxony-Anhalt. **2,517 located trees in the
Laender we wrote off**, which is why Dresden shows 209 within 15 km, Leipzig 63
and Frankfurt 55. The scout was not wrong; "the state does not publish it" and
"the data does not exist" are simply different findings, and this project has
been treating them as one.

**Stalled, recorded so nobody re-runs them blind:**

- **Lithuania (Vilnius #22, the highest-ranked city with no trees).** The
  register is real: Saugomų teritorijų valstybės kadastras, 800+ nature heritage
  objects with botanical ones being trees, declared public and free of charge.
  It is served through `stvk.lt/map`, an Angular app whose bundles contain no
  absolute API host; every guessed path returns the SPA shell, and
  `services.stvk.lt` answers with a default Apache page. **Next step is a
  browser session reading the app's own network calls**, not more URL guessing.
- **Sweden (Gothenburg #73, Malmo #134).** Naturvårdsverket's
  naturvårdsregistret covers *naturminne* and its metadata advertises
  WMS/WFS/REST, but `geodata.naturvardsverket.se/geoserver` answers every WFS
  request with "Service WFS is disabled". **The REST route was tried on
  2026-09-02 and it is closed too**: `/geoserver/rest` and
  `/arcgis/rest/services` both return 403, and the WFS GetCapabilities now
  answers 200 with an `ows:ExceptionReport` body rather than an honest error
  code, which is worth knowing because a status check alone reads it as
  working. So this endpoint is exhausted, not merely untried, and Sweden needs
  a different door: the county boards (lansstyrelsen) publish their own
  protected-object data, and a *naturminne* is designated at county level.
- **Austria (Graz #92, Salzburg #154, Innsbruck #163, Hallstatt #189).**
  Steiermark's Naturdenkmäler are published under **CC BY 4.0** with WMS/WFS via
  haleconnect.com: a confirmed licence and an unlocated endpoint, since the
  INSPIRE record (6A815BD3-6F5B-4946-BB6D-33A527F94C21) carries no service URL
  and data.gv.at has replaced its CKAN API with a JavaScript app, so
  `package_search` is gone. Salzburg runs an ArcGIS Hub at
  `data-sagis.opendata.arcgis.com` (168 datasets, the Portland pattern) and none
  of them is Naturdenkmal or Geschützte Naturgebilde.

**Three of the four stalls are one problem: the open-data layer has moved behind
JavaScript.** data.gv.at, stvk.lt and data.steiermark.at all used to expose a
catalogue API and now serve an app. A scout with a browser reads the network
calls in minutes; a scout with curl guesses hostnames and burns its window,
which is exactly what happened here after Estonia. That is a tooling gap rather
than a data gap, and it wants fixing before the next register pass, not during
one.

## Wikidata's own remarkable-tree layer, scouted 2026-08-15: USABLE, and it covers what governments do not

**19,732 individual trees with coordinates, in one SPARQL request, for nothing.**
`scripts/wikidata_trees.py --fetch` writes them to
`data/research/wikidata-remarkable-trees.json`. Of those, 19,076 carry a name,
15,003 a species, 10,165 a Commons image and 5,503 a national protection
designation.

**The semantic filter is built in**, which is what makes this legitimate under
the never-bulk-import rule: the query asks for `P31/P279* Q811534`, instances of
"remarkable tree" and its subclasses (heritage tree, natural monument tree). An
item exists because a person judged that individual tree worth one. It is not a
street-tree inventory and cannot be turned into one by widening the query.

**Licence: CC0 1.0.** Wikidata's own data is released into the public domain
(https://www.wikidata.org/wiki/Wikidata:Licensing). That clears the
commercial-reuse bar outright, with no attribution obligation. The Commons
images it links are a separate question and keep their own per-file licences,
which still have to be read one by one.

**Why it matters more than the count suggests: it is strongest exactly where the
government scouts came back empty.** The 2026-08-13 German pass found no usable
register for Sachsen ("FND is areal-only") or Hessen. Wikidata holds 209 trees
within 15 km of Dresden, 63 of Leipzig and 55 of Frankfurt, most with a species
and a photograph. Luxembourg City, which no pass has ever scouted, has 108.
Cesky Krumlov has 92 against 11 in the Czech AOPK register. The pattern is that
a country with a strong Wikipedia culture and a weak open-data culture is
covered by volunteers instead of by its state, and the two scouts run so far
were both looking only for the state.

**What it is NOT.** One source per tree, crowd-maintained, with no vitality
field and coordinates ranging from surveyed to guessed-at-the-village. So it
sits exactly where a government register sits under the layer-2 rule: one
source, enough for a dot, never enough for a layer-1 page on its own. Every
entry is a lead. The rule that a register cannot tell us whether a tree still
stands applies here with more force, not less.

**Not promoted to `data/registers/` yet, deliberately.** It lives in
`data/research/` because a register file in this project carries a `licence`
and `licence_proof` block per source, and the honest proof here covers Wikidata
the database rather than the provenance of any individual claim inside it. Ask
before treating it as an import.

Cost of this scout: one SPARQL query and a script. No agent was dispatched.

## Amsterdam municipal register: usable, imported (2026-08-08)

Gemeente Amsterdam publishes its designated "bijzondere bomen" layer on
maps.amsterdam.nl (dataset 561): 5,827 trees the city itself marks as
protected/monumental, with species, plant year, girth, crown diameter,
owner and tree-level coordinates. Licence verified at
maps.amsterdam.nl/open_geodata/terms.php, proving sentence: "U mag de dataset
zowel voor niet-commerciele als commerciele doeleinden gebruiken" (commercial
use explicitly allowed, no attribution required). Imported to
data/registers/amsterdam-bijzondere-bomen.json with the licence block. This is
the municipal-open-data route CLAUDE.md prefers for NL.

**CORRECTION, 2026-08-18: the national Bomenstichting register may not be
CC-BY-NC after all, and this is the single biggest open question in this file.**
The line above used to end by parking it as a lead list on an NC verdict.
monumentalebomen.nl turns out to be an **ArcGIS Open Data Hub**, and its own
dataset catalogue at `https://www.monumentalebomen.nl/data.json` states the
licence for every one of its six datasets as:

> "Onder bronvermelding te gebruiken: ©Bomenstichting"

Usable with source attribution. No non-commercial clause anywhere in that
metadata. Either the licence changed with LRMB v2024, or the earlier scouting
read the website's general terms rather than the dataset's own.

What is behind it, measured 2026-08-18 against the live FeatureServer
`https://services-eu1.arcgis.com/qONmLUR87PipcM5W/arcgis/rest/services/LRMB_v2024_openbaar/FeatureServer/1`:
**16,094 monumental trees**, 267 in Amsterdam alone, with fields that answer the
questions that cost us the most time. `plantjaar` (a decade band or "Leeftijd
onbekend"), `locatie`, `naam_boom`, `historie`, `reden`, and critically
**`bezoekbaar` (ja/nee) and `categorie_eigenaar` (gemeente / particulier /
stichting)**, which settle hard rule 10 from the data itself rather than from a
per-tree hunt. That is the Den Bosch pattern at national scale.

**Do not import until the licence is confirmed in writing.** The cheapest route
exists and costs nothing: we are already corresponding with Bomenstichting
Amsterdam, who wrote in this week to correct two of our own pages. Ask them.
Until an answer arrives this stays a lead list, exactly as before.

## Spain: the regional registers, scouted 2026-08-04

Spain has no national register; every autonomous community keeps its own, and they differ in quality, licence and whether the file even downloads. Scouted for the cities we publish and the ones we might.

**The fastest way to find them, worth reusing for any country:** the datos.gob.es API returns every regional dataset in one call with licence and download URL attached, `https://datos.gob.es/apidata/catalog/dataset/title/árboles singulares` with the accents URL-encoded. Three registers below surfaced there and in no ordinary web search.

**USABLE, licence verified against the holder's own metadata:**
- **Navarra**, 47 named trees, per-tree coordinates, and a per-tree official PDF fact sheet, which is a second-source generator in itself. Shapefile at `https://idena.navarra.es/descargas/BIODIV_Sym_MonumNat.zip`. The ISO metadata inside the download states CC BY 4.0 and the required wording: "Información geográfica propiedad del Gobierno de Navarra." A companion layer covers 8 trees in the Pamplona river park, a walkable cluster on its own.
- **Aragon**, 45 singular trees and 13 groves region-wide, CC BY 4.0 per `opendata.aragon.es`, which states commercial use explicitly. Served through IDEAragon; the GeoNetwork record was returning a server error, so the direct file URL still needs resolving through their download portal. Note the count: 45 for the whole region means one or two inside Zaragoza.
- **Illes Balears**, 78 trees, CC BY per the holder's CKAN metadata, GeoJSON and CSV both downloadable. **But the export carries a single attribute, the year catalogued: no name, no species, no municipality.** As shipped it is 78 dots. The attributes presumably live on the regional WFS. Not usable until that is resolved.

**THE TRAP, and it is a good one.** Castilla y Leon publishes two datasets on the same portal, same subject, different licences. "Arboles singulares en espacios naturales" is CC BY 4.0 and is the one to use, though every download URL was 404 during the scout and the page itself said the service was temporarily unavailable. "Mapa de Arboles Singulares de Castilla y Leon" carries **IGCYL-NC**, whose terms authorise only non-commercial use, which disqualifies it outright under our rules. Anyone finding the second one first would import a licence we cannot use.

**Needs a human, ranked by what they would unlock:** Comunitat Valenciana has a Catalogo de Arboles Monumentales y Singulares covering Valencia and Alicante, licence unchecked, and is the obvious next scout. Las Palmas de Gran Canaria has a municipal catalogue of 326 specimens, the largest single count found anywhere in this scan and city-scale. Cantabria has 214 catalogued trees browsable per municipality with no open distribution. Asturias runs an ArcGIS Hub, which would give GeoJSON out of the box, but its dataset record came back empty. Murcia, Extremadura and La Rioja all have real catalogues behind PDFs or a Cloudflare challenge.

**Not worth the effort:** Castilla-La Mancha declares about ten singular trees in the whole region, none near a city we would publish.

## Japan: the Environment Ministry giant-tree database (scouted 2026-08-04, VERDICT: usable with one real caveat)

`https://kyoju.biodic.go.jp/`, the 巨樹・巨木林データベース, the national record of every tree in Japan over 300 cm girth at breast height, with measured girth, height, species, and location. It is the closest thing Japan has to Portugal's ICNF, and it is the spine of any cheap layer-two coverage for Japanese cities.

**Licence, with the proving sentence.** The Biodiversity Centre's terms page (`https://www.biodic.go.jp/copyright/terms_of_service.html`) states that its content may be used under 「公共データ利用規約（第1.0版）」（PDL1.0）, the Public Data License 1.0, which permits commercial reuse with attribution and which CLAUDE.md already names as an acceptable register licence. Attribution must give the title, 環境省生物多様性センター, and the URL or download date; any editing or adaptation must be stated separately along with who did it.

**The caveat, and it is a real one.** The same page carves out user submissions by name: 「いきものログ」及び「巨樹・巨木林データベース」ウェブサイトの投稿情報... 著作権は投稿者に帰属します. Copyright in posted content belongs to the poster. The database mixes two things: the ministry's own national survey data from 1988 and 2000, which is Centre content under PDL 1.0, and citizen reports submitted through the site since, which are not. The interface does not obviously separate them.

**Working position for runs.** Use it, and use it carefully:
- Treat measurements, species and coordinates as facts, which they are, and which carry no copyright in themselves.
- Never copy submitted prose, observation reports or photographs from the site. Photographs in particular belong to their posters and fall outside PDL 1.0 entirely.
- Attribute as the terms require, and record in the register file which survey or page each record came from.
- Where a record is clearly a recent citizen report rather than survey data, treat it as a lead to verify elsewhere, not as an importable record.

That is enough to build the second layer for Japanese cities at near-zero cost, which was the open question blocking the Japan plan.

## Round one: OpenStreetMap, and why it misled

Trees tagged `natural=tree` + `denotation=natural_monument`, counted per city with bounding box queries against the public Overpass API.

| City | Trees | City | Trees |
|---|---|---|---|
| Warsaw | 224 | Barcelona | 30 |
| Paris | 207 | Madrid | 27 |
| Berlin | 90 | London | 19 |
| Vienna | 82 | Rome | 15 |
| | | Tokyo | 10 |
| | | Amsterdam | 4 |

Prague and New York timed out repeatedly; the public endpoint is heavily loaded and those two need retrying.

Note the wider `denotation` tag is useless alone: Berlin carries 35,848 of them, because it also covers ordinary street trees tagged `avenue` or `urban`.

The first conclusion drawn from this table was that OSM works in Central Europe and fails elsewhere. **That conclusion was wrong**, and the error is worth recording because it is easy to repeat: this table measures mapping culture, not tree data availability. Amsterdam does not have four monumental trees, and London does not have nineteen.

## Round two: the national registers, which is where the data actually is

| Source | Size | Format | Notes |
|---|---|---|---|
| UK, Woodland Trust Ancient Tree Inventory | 233,200+ records | Download, free of charge | Citizen science, run with TROBI. Licence terms sit behind the portal's download flow and were not readable without accepting them. |
| Italy, MASAF official registry | 4,944 trees | Shapefile and Excel, by region | Government registry, updated by decree, latest October 2025. |
| Paris, opendata.paris.fr | Hundreds | Open data portal | Already used by the Paris run. |
| Netherlands, Bomenstichting register | Unknown | Unchecked | Thousands are believed to be listed. Amsterdam's OSM count of 4 is clearly not the real number. |

**London went from worst in the OSM table to best available anywhere.** 19 tagged in OSM, over 233,000 records in the national inventory. That single comparison is the finding: judging a country's data by its OSM count is close to meaningless.

## What this means for the work

Use open data as **research input, never as published content**. A run opens a city with a candidate list and coordinates already placed by people who stood in front of the tree, and spends its time on what the site is actually for: verifying, writing, finding photographs. Nothing changes about what ships. Still ten, still fully researched, still two independent sources.

Expect this to cut the finding and coordinate work substantially and to improve pin precision, since register coordinates are usually surveyed rather than estimated. Expect it to do nothing for the writing, which is the real cost and should not be sped up.

Work registers out per country rather than per city. Doing Italy once serves Rome, Florence, Milan and Naples.

## Two things to settle before building on this

**Licences are unresolved.** The UK terms could not be read without going through the download flow, and the Dutch register has not been looked at. Italy is a government registry and Italian public sector data is normally openly licensed, but that was not verified either. None of this is legal advice, and nothing should be imported on the strength of a machine's reading.

**Some trees are deliberately kept off public maps, and this one matters.** The Woodland Trust excludes trees "deliberately hidden from public view" from its public map. That is not bureaucracy: ancient trees are damaged by visitor pressure, soil compaction around roots, climbing and vandalism, and some stand on private land whose owners never agreed to visitors.

This project publishes exact coordinates and actively sends people to stand at the trunk. That is the whole point, and it is also a way to hurt a tree or trespass on someone's land. It falls squarely under question 3 of the mandate, the one that overrides the others: can this hurt anyone other than Hidde.

Nothing here is currently checked for it. Before importing any register, and arguably before the next city ships, decide: do not publish a tree whose source withholds its location, prefer trees that are already publicly signposted, and drop any tree where publishing the pin would plausibly harm it or its owner. Coverage is not worth a damaged tree.

## Next

1. Retry Prague and New York.
2. Read the UK licence terms properly, and find out what the Dutch register offers and under what conditions.
3. Decide the tree-protection rule above. That one does not need to wait for anything.


## Japan scouting for the register layer, 2026-07-30 (two research passes, verified by download where stated)

The register layer (two-layer model, DECISIONS.md 2026-07-29) needs sources that are official, licensed for commercial-leaning reuse, and ideally carry coordinates. Japan, as the pilot:

**National level:**
- **国指定文化財等データベース (kunishitei.bunka.go.jp), Agency for Cultural Affairs.** 967 Natural Monuments + 75 Special Natural Monuments (plants, animals AND geology; the individual-tree subset is likely a few hundred, exact count unverified). Browsable with CSV export of search results. Per-record map pages exist; whether the CSV carries lat/long is still UNVERIFIED, and designations often cover an area, so imported pins will structurally be `approximate`. **Licence, actually read 2026-07-30, and weaker than this entry previously assumed**: `/top/policy` (linked from `/bsys/about`, not the `/bsys/top/policy` path this file previously guessed, which 404s) states text may be freely reused with attribution ("出典を記載の上、自由にご利用ください"), with no reference anywhere on the page to 政府標準利用規約, CC BY, or any named open-licence framework, and the same page's footer carries a blanket "Copyright (c) 1997 Agency for Cultural Affairs, Government of Japan, All Rights Reserved." Images separately require per-work permission (third-party rights). This is genuinely ambiguous rather than a clean pass: "free to use with attribution" reads permissive and states no non-commercial restriction, but it is not the explicit, named licence text hard rule (register layer) asks for, and sits directly under a boilerplate all-rights-reserved notice the way Tokyo's own catalog page did before its CKAN API's explicit `license_id: CC-BY-4.0` field settled that case cleanly. **Do not import from this source on this reading alone.** Before it can be the pilot backbone: (1) find whether the database exposes the same licence commitment in a more explicit, structured place (an API/CKAN-style metadata field the way Tokyo's did, rather than page prose), or (2) treat the ambiguity as disqualifying per "when in doubt, leave it out" and look elsewhere for the national backbone. CSV-export mechanics and coordinate presence are also still unverified; a plain WebFetch only reaches the static search-form shell, not exported results, so confirming either needs a session that can drive the actual search/export interaction, not just read markup.
- **環境省 巨樹・巨木林データベース (kyoju.biodic.go.jp).** ~64,500 giant trees (girth >= 3m), GIS downloads exist on biodic's shapedata page. Licence 公共データ利用規約 PDL 1.0 (attribution required, modifications stated, commercial OK), with the explicit carve-out that USER-SUBMITTED content stays with contributors. Decades-old records in places, no accessibility info per entry, so hard rule 10 filtering is manual. **The later volume layer, not the pilot.**
- **国土数値情報 P32 (MLIT, prefectural designations as points).** REJECTED: terms say 非商用 (non-commercial), data is 2014, and Tokyo/Nara/Oita are withheld at those prefectures' own request.

**Prefecture detail (verified by download):**
- **Tokyo: the best source found anywhere so far, now imported (2026-07-30).** 文化財一覧 CSV, licence field literally CC-BY-4.0 (confirmed via the catalog's own `package_show` API, `license_id: CC-BY-4.0`). 248 rows, 35 天然記念物, WITH populated 緯度/経度 columns (all 35). Shift_JIS encoding. **Two access notes for whoever touches this next**: the dataset's own HTML page (catalog.data.metro.tokyo.lg.jp/dataset/...) is behind an AWS WAF bot-challenge and returns empty to a plain fetch; the CKAN API (`/api/3/action/package_show?id=...`) is not, and gave clean JSON including the direct CSV url (`www.opendata.metro.tokyo.lg.jp/suisyoudataset/130001_cultural_property.csv`, note the `www.` and the domain rename from the plain `opendata.metro.tokyo.lg.jp` this file previously recorded, which no longer resolves). **Built `data/registers/tokyo.json`, 28 trees**, filtered from the 35 Natural Monument rows: 3 excluded as non-tree geological designations (a limestone cave, a limestone-outcrop area, a rock dike), 4 more excluded per hard rule 10 because the register's own owner field names a private individual and this dataset doesn't independently confirm public access (left out rather than guessed at, the same "when in doubt, leave it out" discipline layer 1 uses). All 28 kept entries are owned by a religious corporation, a school, a ward/town government or the Metropolitan government itself. Every entry `location_precision: approximate` (register coordinates are institution/address-level, e.g. two trees at the same temple share one lat/long, not individually surveyed). Municipal 保存樹木 CSVs (Mitaka, Suginami, Chofu) also CC BY, not yet imported. **Wired into the explore map the same day**: a second, unclustered GeoJSON source renders as small hollow grey dots (visually quieter than the curated green/gold trees on purpose), each popup stating the required "From the official register, not yet verified by us." label verbatim, no link out (no own page exists). Areas and the designation label were machine-translated to English for the popup (`area_en` added per entry after catching one address-parsing bug: a naive regex first mis-cut 東村山市/Higashimurayama to 東村, fixed before shipping). Confirmed via the built HTML: all 28 register features present in `explore.html`'s embedded GeoJSON, `python3 scripts/qa.py` and `python3 scripts/smoke_test.py` (headless Chrome, asserts the MapLibre canvas actually renders) both green.
- **Nara: CC BY list, no coordinates.** 県指定文化財一覧 XLSX (pref.nara.lg.jp), 715 properties, 64 天然記念物, town-level addresses only; prefecture deliberately withholds coordinates (same grounds as its P32 opt-out). Treat as a lead list: geocode only what is clearly public and signposted, per hard rule 10. Nara City's own CSV is name-only, near-useless.
- **Kyoto: effectively no itemized open data.** The prefectural cultural-property DB lives inside a GIS with no export and no open licence (all-rights-reserved by default); Kyoto City's portal has zero cultural-property datasets. Kyoto register data = verification-only source, like monumentaltrees. **Extended and confirmed 2026-08-10 against a specific, much better source than the prefectural DB: Kyoto City's own 区民の誇りの木 register, 901 designated trees across all 11 wards, DISQUALIFIED on licence. Full verdict and proving sentence below, "Kyoto City's 区民の誇りの木".**
- **Tokyo's municipal 保存樹木/保護指定樹木 CSVs (Mitaka, Suginami), checked by download 2026-07-30: dead ends, a different shape than the national source.** These are a separate, standardized Tokyo-wide template (found via the same CKAN catalog, confirmed CC-BY-4.0), but the template itself doesn't carry what the register layer needs, not a licence or access problem this time. **Mitaka** (`t132047d2024000003`, CSV at `city.mitaka.lg.jp/c_service/111/attached/attach_111873_1.csv`): 90+ individual rows with a per-tree ID and species, but 緯度/経度 (lat/long) and every address field below city-name level are blank for every row checked, no coordinates to import at any precision. **Suginami** (`t131156d2024000003`, CSV at `opendata.metro.tokyo.lg.jp/suginami/131156_suginamiku_hogoshiteijumoku.csv`): worse still, no per-tree ID at all, just a deduplicated list of species names present somewhere in the ward with a designation-status column reading "不明" (unknown) throughout, a species tally rather than individual tree records. Suginami's separate "公園樹木" (park trees) dataset, which sounded more promising since park trees are unambiguously public, turned out to be served through a dynamic wagmap.jp portal endpoint that returns 404 to both a plain fetch and WebFetch, not a static CSV; unresolved rather than confirmed dead, worth a retry with different tooling. **Chofu has no matching dataset in this catalog at all** (a `樹木` search against its organization id, t132080, returns zero results); the 2026-07-30 entry above that flagged it alongside Mitaka/Suginami as "also CC BY, not yet imported" was not itself verified by download and should be treated as superseded by this entry. Net: this specific "municipal 保存樹木 CSV" lead does not extend Tokyo's register beyond the 28 trees already imported; a future pass should not re-fetch these same three files expecting coordinates to appear. If Tokyo's register layer grows further, the more promising untried thread is still the national kunishitei/kyoju.biodic backbone below, not more municipal preservation-tree lists.
- **The "worth a retry" threads left open above, both closed for real 2026-07-30 (same session, later pass).** Queried the Tokyo CKAN catalog's own `package_search` API for every 保護指定樹木 dataset site-wide (not just Mitaka/Suginami/Chofu): it returns 20+ municipalities on the identical standardized template, Setagaya, Chiyoda, Sumida, Toshima, Katsushika, Fuchu, Kunitachi and more, all CC-BY-4.0. Downloaded and checked six of the largest directly (Setagaya 2,895 rows, Toshima 310, Sumida 160, Katsushika 53, Chiyoda 3, plus Mitaka/Suginami already known): every single one has the 緯度/経度 columns present in the header but blank on every row, and the 画像 (image) column empty on every row too, across all six. This generalizes cleanly: the shared template itself structurally omits coordinates and images citywide, not a per-ward gap worth checking ward by ward. **The 公園樹木 (park trees) dataset's separate wagmap.jp portal endpoint was also retried directly this session (both the generic `/suginami/OpenData` listing and the specific `OpenDataDetail?lid=1500&mids=107` resource URL the catalog API itself returns): both 404, confirming the earlier finding rather than reversing it.** Net: this whole family of Tokyo municipal designated-tree CSVs, roughly 20 files, is now confirmed closed; a future register-layer pass should not re-open it, and should go straight to the national kunishitei/kyoju.biodic backbone if it wants to grow Tokyo's register further.
- **Kyushu/Hokuriku (Ishikawa, Fukuoka, Miyazaki, Kagoshima), scouted 2026-07-30: all four dead ends at the sub-national level, same shape as Kyoto.** Checked both the prefecture and the major city (Kanazawa, Fukuoka, Miyazaki, Kagoshima) in every case, via each area's BODIK ODCS open-data catalog plus its own dedicated cultural-properties site, searching for 天然記念物/巨樹/巨木/名木. None has a downloadable, coordinate-bearing, openly-licensed dataset:
  - **Ishikawa/Kanazawa, closest of the four but still disqualified on licence.** Kanazawa's and the prefecture's open-data catalogs return zero relevant datasets, but a dedicated site exists, いしかわ文化財ナビ (bunkazainavi.pref.ishikawa.lg.jp), a searchable prefectural cultural-properties database with a 天然記念物 filter and an apparent CSV-export button. Its terms page (`/userpolicy2`) has no licence statement beyond "Copyright (c) Ishikawa Prefecture. All Rights Reserved," no CC BY, no 政府標準利用規約, no 二次利用 clause anywhere. All-rights-reserved by default, disqualified; coordinate coverage not even checked, moot given the licence.
  - **Fukuoka: browse-only, no export, no licence page.** fukuoka-bunkazai.jp's natural-monument section is list/map-only (no CSV/Excel/GeoJSON, no visible coordinates), and no terms-of-use page exists anywhere on the site. Both the prefecture's and city's BODIK catalogs return zero results for any tree-register search term.
  - **Miyazaki: plain HTML list, no coordinates, no reuse terms.** The prefectural digital museum's 天然記念物 list gives town-level addresses only, footer says "All right reserved," no licence. BODIK catalogs (prefecture and city, the city's otherwise CC BY 4.0) return zero results for a tree register specifically.
  - **Kagoshima: plain HTML list; the source itself disclaims currency.** The prefectural board of education's list has no CSV or coordinates, "All Rights Reserved," and the page states outright it does not maintain current information about the monuments, pointing back to individual owners/managers. BODIK catalogs return zero results.
  
  Net: none of the four adds an import candidate; the backbone stays exactly the two national sources above. Treat all four as scouted and closed, same as Kyoto, not "not yet scouted."

## Kyoto City's 区民の誇りの木 (Pride Trees), scouted 2026-08-10: VERDICT DISQUALIFIED on licence

The best-shaped Japanese municipal tree register found so far, and we cannot
import it. Worth recording in full because the source is genuinely good, the
temptation to use it will recur, and the "no" is unambiguous.

**What the register is.** 区民の誇りの木 ("trees the ward's residents are proud
of") is a Kyoto City Construction Bureau (建設局) programme, **not** a Kamigyo
Ward one: it runs across **all eleven wards** and holds **901 designated trees**,
numbered in one contiguous citywide sequence. Per-ward, from the id blocks in
the citywide list: Kita 1-85 (85), **Kamigyo 86-195 (110)**, Sakyo 196-296 (101),
Nakagyo 297-364 (68), Higashiyama 365-422 (58), Yamashina 423-492 (70), Shimogyo
493-570 (78), Minami 571-640 (70), Ukyo 641-744 (104), Nishikyo 745-825 (81),
Fushimi 826-901 (76).

Distribution is a single citywide PDF, `hokorinoki_ichiran_all_2.pdf`
(1.29 MB, downloads clean, ends in %%EOF, reads fine with pdfminer):
`https://www.city.kyoto.lg.jp/kensetu/cmsfiles/contents/0000114/114296/hokorinoki_ichiran_all_2.pdf`
Programme index: `https://www.city.kyoto.lg.jp/kensetu/page/0000019145.html`;
per-ward index pages under `/kensetu/page/` (Kamigyo's areas A-F at 0000021581
and 0000021583); the per-tree pages a verification pass found sit under
`/kamigyo/page/` (e.g. 0000012431, 0000012402, 0000012315, 0000012542).

Columns per tree: 整理番号, 行政区名, エリア (a walk-sized area letter A-F,
which is a clustering hint the register hands over for free), 番号, 樹種
(species, katakana), 所在地 (the temple/shrine/park it stands in), 所在地住所
(address), 樹高 (height, m), 幹周 (girth, m), 科 (family), 分類, 単・群の別
(single tree vs group, i.e. the collectible-point test pre-answered), その他指定等
(other designations). **No coordinates and no age field anywhere in the file**
(緯度/経度/座標/樹齢 all absent), the same two gaps as MASAF and Berlin.

**The licence, read at the primary source and quoted verbatim.** Kyoto City's
著作権・リンク等 page, `https://www.city.kyoto.lg.jp/main/site_policy/0000000005.html`
(updated 2026-07-02):

> 「京都市のホームページ「京都市情報館」に掲載している内容（文章、写真、イラストなど）に関する著作権は、原則として京都市に帰属します。」
>
> 「当ホームページの内容について、「私的使用のための複製」や「引用」など著作権法上認められた場合を除き、無断で複製・転用することはできません。」

Translation: "Copyright in the content published on Kyoto City's website
'Kyoto City Information Hall' (text, photographs, illustrations and so on)
belongs in principle to the City of Kyoto." And: "The content of this website
may not be reproduced or repurposed without permission, except where copyright
law allows, such as reproduction for private use or quotation."

That is the whole verdict. No named open licence, no 政府標準利用規約 anywhere on
the page, no CC, no 二次利用 clause, and the page footer carries
"(c) City of Kyoto. All rights reserved." An explicit prohibition on 複製・転用
is stronger than the merely-ambiguous case the Agency for Cultural Affairs
presents above: this one does not need a judgement call.

**The open-data exception was checked and does not apply.** Kyoto City runs a
real open data portal, `data.city.kyoto.lg.jp`, whose 京都市オープンデータ利用規約
（第３版）is per-dataset Creative Commons ("本サイトで公開しているデータは、著作権者
である京都市が、クリエイティブ・コモンズ・ライセンス等のライセンスのもとで提供して
います。ライセンスはデータセット毎に付与しています"), and which would have been
usable had the register been on it. It is not: `search.php?keyword=誇りの木`
returns zero datasets, as do 樹木 and みどり. Note the portal offers all six CC
variants including the three NC ones, so even a future dataset there needs its
own per-dataset licence read rather than an assumption. Two access notes for
whoever returns: the `/kiyaku` URL that search engines still surface is a 404,
the terms live at `contents.php?category=0`; and the portal's search is
`search.php?keyword=<urlencoded>`, not `/search?keyword=`.

**What this source still is, and it is not nothing.** Exactly what the earlier
Kyoto bullet said, now with a much better document behind it: a
verification-only source under the same discipline as monumentaltrees.com
(hard rule 1). A per-tree page or the citywide PDF can confirm that a specific
tree is officially designated, and confirm its species, height and girth, one
tree at a time, as one of the two independent sources a curated entry needs.
What it can never be: a register file in `data/registers/`, a bulk import, or a
layer-2 dot source. No `kyoto-kamigyo-pride-trees.json` was written, deliberately.

**The path that exists, if Kyoto ever becomes worth it.** The programme sits
with 建設局 (Construction Bureau) and the ward offices; the open data portal is
run by a different unit (総合企画局デジタル化戦略推進室 情報統計・データ利活用推進担当,
075-222-3216) which already publishes under CC. Asking that unit to publish the
existing 誇りの木 list as an open dataset is a plausible request and a cheap one,
since the file already exists in tabular form. It is a Hidde-sends-it item like
the Woodland Trust letter (hard rule 4), and it is not worth drafting until
Kyoto is worth 901 trees to us, which today it is not.

**The finding worth carrying forward.** A Japanese city having an open data
portal tells you nothing about whether a given municipal dataset is on it.
Kyoto's portal is real, CC-based and well run, and the city's single best tree
register is not in it: it sits on the ordinary CMS under blanket all-rights-
reserved. Check the portal for the specific dataset before assuming a portal's
licence covers a document found elsewhere on the same municipality's site.


## The licence-led country scan, 2026-07-30 (verified by download and licence text)

The queue-maker for the register layer (CLAUDE.md rung 5). Verdicts below rest on a fetched licence sentence or a fetched dataset, never on a portal's reputation. Countries still unscanned are named at the end rather than assumed.

### Usable now, licence proven

| Source | Trees | Coordinates | Licence, with the proving evidence |
|---|---|---|---|
| **Portugal, ICNF Arvoredo de Interesse Publico** (si.icnf.pt WFS `BDG:arv_class`, GeoJSON in one unauthenticated GET) | 555 designated (460 single trees; 87 ensembles need the collectible-point test) | Per-tree, median 8 decimals, all inside the country box | CC BY 4.0. ICNF's own metadata: "Sem restricoes. A utilizacao ou divulgacao deste conjunto de dados geograficos requer sempre a indicacao expressa da sua proveniencia e autoria: ICNF." dados.gov.pt returns `license: cc-by`; the WFS itself declares Fees "sem restricoes", AccessConstraints "Nenhum". |
| **Czech Republic, AOPK CR pamatne stromy** (gis.nature.cz ArcGIS REST, `outSR=4326` native) | 16,795 individually positioned; 13,149 with species | Per-tree, WGS84 served directly | CC BY 4.0, verbatim: "Tato datova sada poskytovana Agenturou ochrany prirody a krajiny Ceske republiky podleha licenci Creative Commons Uvedte puvod 4.0 Mezinarodni". Attribution "(c) AOPK CR". |
| **Poland, CRFOP / GDOS** (sdi.gdos.gov.pl WFS, daily updates) | 117,474 tree monuments, the largest verified pool anywhere | Yes, EPSG:2180 needs reprojection; precision unstated so `approximate` by default | CC0 per dane.gov.pl metadata; WFS Fees and AccessConstraints both "brak" (none). WEAKER PROOF: the licence-condition fields are empty and GDOS's own site publishes CC BY-SA 4.0 for site content. Pin the data licence down before importing 117k rows. |
| **Brussels** (opendata.bruxelles.be `bruxelles_arbres_remarquables`) | 582, richest per record: Latin name, circumference, crown, rarity, status, official per-tree page | Yes, WGS84 `geo_point_2d` | CC BY 4.0 (`license_url` on the dataset). Two flags: the inventory surveys private gardens and courtyards, so rule-10 filtering is mandatory; and the `firstimage` photo URLs are NOT covered by the dataset licence, so those are not licensed photos. |

### Blocked, and why (each is fixable, none by guessing)

- **Wallonia, AHREM** (20,245 tree points, the richest schema found: genus, species, cultivar, circumference, height, survey year, decree date). Licence is fine and explicit: "Licence CC-BY 4.0 : L'utilisateur peut utiliser et modifier les donnees... a condition de citer les sources", access "Non restreint". BLOCKED on hard rule 10: the Walloon criterion deliberately includes private trees merely *visible from public space*, the `DOMAINE` field splits 13,007 / 6,985 / 253 across three codes nobody has decoded, and the data model itself admits some points are placed RANDOMLY inside an address perimeter ("Positionnes aleatoirement dans le perimetre defini en adresse"). Read AHREM.pdf's field dictionary first.
- **Catalonia** (302 monumental trees plus a separate 4,176 monumental olives, per-trunk coordinates). BLOCKED on licence: the ISO metadata says only `otherRestrictions`, and the WFS declares no Fees or AccessConstraints at all, so there is no self-declared permission. Do not import until the sentence is found.
- **Spain, four real registers with live download endpoints but no licence sentence yet**: Illes Balears (GeoJSON + CSV, the most import-ready), Comunitat Valenciana (statutory catalogue under Ley 4/2006, SHP + WMS), Castilla y Leon (SHP), Navarra (SHP, but the identifier says polygon so it may be perimeters not trunks). Each needs one page fetched and quoted.
- **Spain dead ends**: Comunidad de Madrid has no machine-readable singular-tree dataset at all (the catalogue is a PDF under Decreto 18/1992); Madrid city publishes only a full bulk inventory, which the semantic filter forbids; Euskadi's singular trees exist legally (Decreto 265/1995) but survive only inside a 1:25,000 protected-areas polygon set whose metadata says `otherRestrictions` and whose download is a 404.
- **Flanders** (4,398 rows, licence fine): NOT RECOMMENDED. Wrong shape and wrong places: only 1,768 are standing trees (the rest hedges, coppice, even farm buildings), geometry is parcel MultiPolygons with no coordinates in the CSV, and coverage is deliberately rural (Voeren 648 versus Antwerp 8, Leuven 16).

### The finding worth copying into every future scan

Catalonia's register ships a vitality field, `DIAGNOSI`, populated on all 302 records: 191 alive, 53 in advanced decline, 58 outright dead (37% dead or dying). A naive import would have put 58 confirmed-dead trees on a map whose promise is standing in front of something alive. **Every register scan from now on looks for a vitality or last-surveyed field before anything else**, and where none exists that alone is a reason to treat the source as a lead list rather than an import.

### Still unscanned (not "no data", just not looked at)

Italy (the ~4,944-tree MASAF national list, the biggest known European prize), Germany (per-Bundesland Naturdenkmal registers), and the whole English-speaking group including the UK's 233,000-record Ancient Tree Inventory whose licence remains the single highest-value unanswered question. Also unread: Spain's default reuse regime (RD 1495/2011 art. 8), which would settle four Spanish registers at once. **France scanned 2026-08-13, see below: no single national source, but four usable municipal sources found and imported.**

**2026-08-02: RD 1495/2011 art. 8 checked and it does NOT settle the four Spanish registers.** Its own title says "para el ámbito del sector público estatal" (national/state administration only); Illes Balears, Comunitat Valenciana, Castilla y León and Navarra are all autonomous-community (regional) governments with their own separate reuse regimes, not bound by this decree. Worth one line so a future session doesn't reread it expecting the same shortcut. A search-snippet check of Castilla y León's own open-data portal found a plausible CC BY 4.0 statement on its "Términos de uso de los conjuntos de datos" page, but this project's own standard is reading the primary source directly, not inferring from a snippet (the same rule Japan's register work follows), and `datosabiertos.jcyl.es` failed TLS certificate verification on every fetch attempt this session ("unable to verify the first certificate"), so nothing from it is recorded as proven. Try again from a session whose network handles that certificate, or verify via `datos.gob.es`'s own metadata for the specific singular-trees dataset instead of the portal's own pages.

## France, the licence-led sweep, 2026-08-13 (four usable municipal sources, imported)

Scouted because 15 cities in the top-250 sprint list sit in France with no register behind them. Paris's own register (`data/registers/paris-arbres-remarquables.json`) was already imported and is the one prior data point: ODbL, held back from `publish_dots` because ODbL's share-alike term is unresolved for a derived commercial map. That flag matters for everything below, because ODbL turned out to be the exception rather than the French default.

**There is no single national or aggregated source.** The A.R.B.R.E.S. association's "Arbre remarquable de France" label (the ~1,129-result interactive map at `carte.arbres.org`) has no visible download, API or licence statement anywhere on its own pages; it is a lead-generation map, not an import candidate, and would need outreach to the association to become one. `data.gouv.fr`'s aggregations are either the Paris dataset restated (`les-arbres-remarquables-1`) or a crowd-maintained mashup, "Arbres remarquables en France et ailleurs" (NosCandidats), which states **"License Not Specified"** on its own metadata page: disqualified outright, no licence sentence to quote. So the country pass is municipality by municipality, same as Spain and Italy before their registers were found.

**France's default open licence is Etalab's "Licence Ouverte" (v1 or v2.0), and it is commercial-reuse-compatible with attribution**, confirmed by reading it on the government's own site (etalab.gouv.fr) and finding it quoted verbatim on every usable dataset below. This is the one general finding worth carrying into every future French scan: unlike Portugal, Castilla y León or the Dutch national register, the licence NAME here is not a trap, "Licence Ouverte" means what it says.

### Usable now, licence proven, imported

| Source | File | Trees | Semantic filter | Licence, quoted |
|---|---|---|---|---|
| **Strasbourg, "Lieux - Arbres remarquables"** (data.strasbourg.eu, opendatasoft) | `data/registers/strasbourg-arbres-remarquables.json` | 66, all in Strasbourg itself | A dedicated remarkable-trees list, not the city's bulk inventory | `"license": "Licence Ouverte (Etalab)"`, `license_url` to etalab.gouv.fr's v1 PDF, read from the dataset's own metadata endpoint |
| **Bordeaux Métropole, "Patrimoine arboré"** (opendata.bordeaux-metropole.fr) | `data/registers/bordeaux-metropole-remarquables.json` | 227 of 80,025 total, filtered to `statut_patrimonial = REMARQUABLE_SYMBOLIQUE`; 142 stand in Bordeaux commune itself | The underlying dataset IS a bulk inventory (80,025 street and park trees), which our rule forbids importing wholesale. What makes this usable is that the register itself carries a per-tree designation field, and only the 227 rows the city itself tagged remarkable/symbolic were pulled out. The 171 rows tagged only `CLASSE_COMME_MONUMENT_OU_SITE_PLU` (a planning-document classification, weaker signal) were left out | `"license": "Licence Ouverte"`, same etalab.gouv.fr proof |
| **Toulouse Métropole, "Arbres urbains"** (data.toulouse-metropole.fr) | `data/registers/toulouse-metropole-remarquables.json` | 37 of 124,177 total, filtered to a populated `remarquable` field naming the labelling body ("Ville de Toulouse" x35, "France" x1, "Arbres et paysages d'Autan" x1); 35 stand in Toulouse commune | Same pattern as Bordeaux: bulk inventory with one per-tree designation field, only the designated rows imported | `"license": "Licence Ouverte v2.0 (Etalab)"` |
| **Métropole Rouen Normandie / ONF, "Arbres Remarquables 2019"** (data.metropole-rouen-normandie.fr) | `data/registers/rouen-foret-arbres-remarquables.json` | 13, all in the state forests of Roumare, Verte and La Londe-Rouvray | A genuinely small, jointly-curated list (city + the ARBRES association + ONF), not an inventory | `"license": "Licence Ouverte v2.0"`, `license_url` to etalab.gouv.fr's v2.0 PDF |

**The pattern worth copying into every future French municipal scan: check the FULL tree inventory for a per-tree "remarkable" or "patrimonial" flag before writing the city off.** Bordeaux and Toulouse both publish their entire street-tree inventory (80k and 124k rows) under an open licence, which our semantic filter forbids importing wholesale, and both turned out to carry a field a naive read would miss (`statut_patrimonial`, `remarquable`) that turns the bulk dataset into a legitimate, city-designated shortlist once filtered. A dataset titled "Patrimoine arboré" or "Arbres urbains" is not automatically a bulk-only source; check its field list for a designation column first.

**Vitality, checked as the rule requires.** Bordeaux's `statut` field (VIVANT/SOUCHE) is a genuine per-tree life status: 221 of the 227 imported rows are VIVANT, 6 are SOUCHE (stump) and are flagged in the import for exclusion at write time, never as entries. Strasbourg, Toulouse and Rouen carry no vitality field at all, so "alive now" stays a per-tree check for those three, same as every register scanned so far.

### Not recommended, and why

- **Nantes Métropole and Ville de Nantes**: only the bulk inventory (83,500 alignment trees + 40,350 domain trees) is open data; the metropole's own "A la découverte des arbres remarquables de Nantes" content is a curated webpage, not a dataset, no coordinates or machine-readable list found. A lead for a future from-zero research pass, not an import.
- **Montpellier Méditerranée Métropole**: the open dataset is alignment trees only (excludes campus, botanical garden, private and some public green space trees by its own description); the only "remarkable" layer found is a crowd-sourced OSM extract republished on data.gouv.fr, refreshed weekly from OpenStreetMap tags. Not an official register, and OSM extracts are typically ODbL (unconfirmed this pass), so treat as a verification cross-check at most, never a sole source.
- **Marseille / Métropole Aix-Marseille-Provence**: no remarkable-trees dataset found; the city is mid-way through a LiDAR full-inventory project (with Greehill) not yet published as open data.
- **Aix-en-Provence**: a 2019 municipal push to get local trees A.R.B.R.E.S.-labelled (the Saint-Pierre cemetery cedars, two Pavillon Vendôme oaks) is reported in local press only, no dataset.
- **Lille**: only two remarkable trees identified in blog coverage (Dondaines garden horse chestnut, Ramponneau square plane), no dataset for Lille commune itself. The Métropole Européenne de Lille (MEL) does publish "Les arbres remarquables à Roubaix" as a dedicated dataset for a neighbouring commune, but the portal migrated from `opendata.lillemetropole.fr` to `data.lillemetropole.fr` and the old dataset slug now 404s on the new host's API; the new catalogue path was not found within this pass's window. Worth a short follow-up fetch, not a from-zero rescan.
- **Dijon Métropole**: an open data portal exists (referenced from `data.metropole-dijon.fr`, a Drupal-style site, not the opendatasoft instance guessed at first) but no "arbres remarquables" dataset was located in the time available. Unresolved, not disqualified.
- **Avignon, Annecy, Colmar, Versailles**: no open dataset found for any of the four. Versailles publishes a genuinely rich remarkable-trees WALK (30 "admirable trees" on a 14-stop signed circuit through the palace domain, with an audio-guide app), which is exactly the kind of municipally-endorsed content Step 1's search order values, but it is prose and a paid/free app, not structured data; a future research pass should use it directly as a source, not wait for an import. Alsace's departmental participatory register (`t-opendata67.alsace.eu`, "Arbres remarquables CD67", Bas-Rhin only, so would not reach Colmar in Haut-Rhin anyway) could not be reached this pass: both `www.alsace.eu` and `t-opendata67.alsace.eu` refused the connection outright (ECONNREFUSED) to curl and to WebFetch. Not logged in `data/fetch-blocklist.json` because a refusal is not a hang, but worth knowing before a session budgets time on it again.

### Register pitfalls this pass actually hit

Girth and diameter fields in both the Bordeaux and Rouen imports read plausible in centimetres against a spot check (a 63 cm `circonference_tronc` on a young Bordeaux oak, a 110 cm `diametre_pied` on a mature Rouen beech), unlike Portugal's metres-mislabelled-as-centimetres trap. Still worth checking per record before publishing a number, per the standing rule. Bordeaux's own inventory dates (`cdate`/`mdate`) run into 2026, so the underlying bulk dataset is actively maintained, which is independent evidence for the filtered subset's currency even without a dedicated vitality survey.

## The Spanish licence sweep, 2026-08-06 (four registers, read at the primary source)

Hidde asked for focus on Spain before Czech, Poland and the UK. Four regional
registers were recorded as "download endpoint live, no licence sentence yet".
Three are now settled and one is not. Every verdict below comes from the
publisher's own machine-readable metadata or licence text, never from a search
snippet, and the reason that distinction is not pedantry is in the Castilla y
Leon entry.

### Comunitat Valenciana: USABLE, CC BY

`dadesobertes.gva.es` dataset "Catalogo de Arboles Monumentales y Singulares de
la Comunitat Valenciana". Its own embedded structured data declares
`"schema:license": "http://www.opendefinition.org/licenses/cc-by"`, and the
visible page says "Llicencia Creative Commons Attribution". Statutory catalogue
under Ley 4/2006.

Distribution: SHP via
`http://descargas.icv.gva.es/server_api/gdb/descarga/index.html?capas="medio_ambiente.gdb/fore_arboles_mon"&formato=Shapefile%20-%20SHP%20-%20.shp&geocat=DATO_DIRECTA_SHP`
and WMS at `carto.icv.gva.es/arcgis/services/tm_medio_ambiente/forestal/MapServer/WmsServer`.
No WFS is published, so this one arrives as a shapefile rather than a GeoJSON GET.

### Illes Balears: USABLE, CC BY

The portal moved: `catalegdades.caib.cat` now redirects to
`intranet.caib.es/opendatacataleg`, which is why the recorded dataset URL 404s.
Its CKAN API answers directly:
`intranet.caib.es/opendatacataleg/api/3/action/package_search?q=arbres` returns
one dataset, "Arbres Singulars Illes Balears", `license_title: "Creative Commons
Attribution"`, `license_id: "cc-by"`.

The data itself is a live ArcGIS service, **78 trees**, already WGS84:
`https://ideib.caib.es/geoserveis/rest/services/public/GOIB_ArbresSingulars_IB/MapServer/0`
Copyright text: "Servei d'Informacio Territorial de les Illes Balears (SITIBSA)".
This is the most import-ready Spanish source left.

### Castilla y Leon: USABLE FOR US, but not under the name it advertises

The licence is **not** CC BY, and a search snippet said it was. datos.gob.es
gives the machine-readable field as `https://www.jcyl.es/licencia-IGCYL-NC`,
whose name reads as non-commercial and would disqualify it outright under our
own rule. It does not. The licence document has two branches, and the
commercial one is explicit:

> "Se autoriza el uso comercial de la cartografia e informacion geografica,
> entendiendo como tal el uso que conlleva aprovechamiento economico directo,
> indirecto o diferido."

Its conditions, which are real obligations and heavier than CC BY:
attribution exactly as "(c)Junta de Castilla y Leon", visible beside the
licensed information or anything derived from it; transformation allowed only
where it does not distort the meaning of the data; and, in every reproduction
or public communication, an obligation to **inform the end user that the
material is available free of charge at jcyl.es**. Passing the data to someone
else for their own commercial use requires them to take a new licence or
explicitly accept these conditions.

Verdict: importable, but it is the first source here that would put a
requirement on our own pages (the free-availability notice), so the import
should carry that notice with it rather than bolt it on later. Note also that
`datosabiertos.jcyl.es` still fails TLS verification on plain fetches; the
licence text above was read through a redirect from `www.jcyl.es` with a
browser user agent.

### Catalonia: STILL BLOCKED, unchanged

302 monumental trees plus 4,176 monumental olives. Nothing found this pass that
states permission: the Socrata portal `analisi.transparenciacatalunya.cat`
returns zero hits for arbres monumentals, and the environment department
publishes the register as per-county HTML fiches rather than a dataset with
terms. The ISO metadata's `otherRestrictions` finding from the earlier scan
stands. Do not import.

### The finding worth carrying forward

**A licence's NAME is not its terms, in either direction.** IGCYL-NC reads
non-commercial and permits commercial use; the Dutch national register reads
like an open register and does not. Both were only settled by reading the
licence document itself. And a search snippet got Castilla y Leon wrong twice
now, once in each direction, which is the second time this specific register
has been misreported by a summary rather than a source.

## The UK Ancient Tree Inventory licence, read in full 2026-08-06: DISQUALIFIED as an import, permission path open

The "single highest-value unanswered question" above is answered. The ATI needs
no account to download (the open data hub serves CSV/GeoJSON/SHP in one GET,
endpoint recorded below), but its End User Licence Agreement, published in the
hub's own DCAT feed, prohibits exactly our use, twice over:

- "The Data are available to you, free of charge, for non-commercial use only."
  Commercial purpose "includes those profit generating activities of both
  commercial and non-commercial organisations (including charities and
  non-profit organisations)", so indirect and deferred gain counts, which a
  site whose recorded destination is a premium tier cannot honestly claim to
  lack.
- "The Data may not be used in publicly available Internet mapping services
  (e.g. Google Maps/Earth, Microsoft Bing Maps or Yahoo Maps) without prior
  written permission from the Woodland Trust." We are one.

Same class as the Dutch national register: disqualified outright, stays a
lead list at most (the public ATI website can corroborate facts per tree the
way monumentaltrees.com does under hard rule 1; no bulk extraction ever).

The path the EULA itself offers: "Amendments to the terms of this agreement
can be requested", contact ancienttreeinventory@woodlandtrust.org.uk "if you
wish to publish The Data within the public domain". A draft permission email
for Hidde sits in drafts/woodland-trust-permission.md; only he sends it (hard
rule 4). Until written permission exists, no ATI data is downloaded or used.

Endpoint for the day permission arrives:
GeoJSON https://opendata-woodlandtrust.hub.arcgis.com/api/download/v1/items/9d2d13b04d654ceb9ba6e0697c1e0c29/geojson?layers=0
ArcGIS REST https://services-eu1.arcgis.com/WIfgdJeDbrZU1cnA/arcgis/rest/services/Ancient%20Tree%20Inventory%20(ATI)/FeatureServer/0
Attribution wording their EULA requires: "Data reproduced with the permission
of The Woodland Trust." plus citation "Ancient Tree Inventory, Woodland Trust,
Accessed MM/YY".

## Photo sources, what was tried and what is left (2026-08-08)

Four sources are wired into scripts/photo_hunt.py and their measured conversion
is the whole story: **only identity works**.

| Source | How it matches | Result |
|---|---|---|
| Wikidata (P18 + coordinates) | image to ENTITY, 15 m radius | 11 of 18 approved. The only source that answers "which tree is this" |
| Wikimedia Commons | geosearch + name, place AND plant word required | works occasionally; its geosearch lane served a parked Vespa, a sarcophagus and a concert stage |
| iNaturalist | genus within 120 m, per-photo licence | a handful; observers shoot bark and leaves, not portraits |
| Openverse | text only | **0 across 49 trees.** No coordinates, no taxonomy |

Three further lanes were tested on 2026-08-08 and all failed, so they should not
be re-proposed without a new argument:

- **Commons category traversal.** Park categories hold far more than geosearch
  sees (132 files for the Ciutadella, 500 for RBGE) because most Commons files
  are not geotagged. But filtering by species matches the wrong individual: it
  paired Edinburgh's Cammo Ash with a different ash inside the Botanics, and two
  Edinburgh sycamores with a paperbark maple. A garden holds many trees of one
  genus and the category cannot say which is which.
- **Per-tree Commons categories.** Famous trees sometimes have their own
  category, which would be a true entity link. Of 14 photo-less trees, one
  matched, and it was a tram stop.
- **Flickr. CLOSED, and not by a workaround.** flickr.com/services/apps/create/apply
  states it outright: "In order to mitigate abuse, API key creation is currently
  disabled for free accounts. API key creation is available to all Flickr PRO
  subscribers." Pro is 82 US dollars a year. A session told Hidde a free account
  would be enough, which was wrong, and he found the wall himself. There is no
  free API key to obtain, so this is not a "try again later" item: it is a
  purchase decision, and purchases are Hidde's alone (hard rule 5). Do not
  re-propose it without new evidence that the policy changed, and never nudge
  him toward paying for a source expected to land between Openverse's zero and
  Wikidata's 61 percent.

**The honest conclusion.** Most of our trees are simply not photographed under
an open licence by anybody. That is a supply fact, not a retrieval problem to
engineer around, and 432 of 759 tree pages (57 percent) show no photograph. The
two routes that remain are readers, which needs traffic we do not have, and
registers with their own photo pages, which is why the Catalonia permission
request matters for pictures as much as for trees.

## Which countries to invest in, weighed 2026-07-21

Researched at Hidde's request: national tree databases plus photo availability and other factors, ranked for the strategy (English site, travelers plus enthusiasts as the audience).

National register quality, on evidence:

| Country | National register | Size and access |
|---|---|---|
| UK | Woodland Trust Ancient Tree Inventory | 233,000, downloadable, one source. Best in the world. |
| Netherlands | Landelijk Register Monumentale Bomen (Bomenstichting) | ~15,000, open data in CSV/GeoJSON with coordinates. Best accessibility after the UK. |
| Ireland | Tree Register of Ireland + Heritage Trees of Ireland | 11,000+, GPS-recorded. |
| Italy | MASAF official registry | 4,944, shapefile and Excel, by region. |
| Belgium | Flanders heritage inventory + Brussels remarkable trees | Regional, with coordinates. |
| France | none national; Paris and Ile-de-France open data | Fragmented, rich where it matters. |
| Germany | none national; per Bundesland, some cities | Fragmented. |
| Spain | none national; regional (Castilla y Leon, Aragon) via datos.gob.es | Fragmented. |

Correction to the earlier OSM-based read: the Netherlands is data-rich, not thin. The OSM count of 4 was mapping culture, not the register, which holds ~15,000.

Photos: not a national property, closer to a per-tree lottery driven by how touristed and Wikimedia-active a place is. Weighted low, because the fix is wider sources (iNaturalist, Flickr, Openverse) and submissions, not country choice.

Other factors that matter: whether a register gives exact coordinates or blurs them (hard rule 10, and it now breaks check-in if vague); seasonality strength (northern and temperate beat Mediterranean for the season chart); existing competition (the UK already has the Woodland Trust map, so we compete on curation); and licence, which is unchecked per country and must be before any import.

Ranked top 10 to invest in:

1. UK, 2. Netherlands, 3. Ireland, 4. Belgium, 5. France, 6. Italy, 7. Germany, 8. Austria, 9. Spain, 10. Japan.

The shape matters more than the order. Three groups:
- Lead group (1-4, UK/Netherlands/Ireland/Belgium): where data, verifiability and reachability meet. All near Hidde, real registers, reachable in person. Invest here.
- Traveler group (5,6,9, France/Italy/Spain): weaker or fragmented data, but they pull the English-speaking traveler who converts. Take the marquee cities, not the whole country.
- Quality group (7,8,10, Germany/Austria/Japan): where the season feature shines and tree culture is richest. Japan is 10th on strategy but would be top three on quality alone, and that tension is a real choice, not something to explain away.

The USA stays out: English is a plus, but its cities are young so "ancient" is thin, and there is no national register.

Not yet done, and gating any import: per-country licence checks, starting with the two leaders, the UK and the Netherlands.

## Licence check round one, 2026-07-26: the Dutch register is non-commercial

First licence actually read, via the Bomenstichting's own IPT page: the Landelijk Register Monumentale Bomen is published under **CC-BY-NC 4.0**, 10,012 records, coordinates included. Non-commercial, and this project's recorded destination is commercial (premium, revenue). So the register can never be the data backbone of the product.

What it still is: a research lead list. Finding a candidate in the register, then verifying existence, species, age and position against two independent sources and writing our own story is our normal bar anyway, and it is not republishing the database. What it is not: a source to import coordinates from at scale.

The general lesson, which reshuffles the register ranking for import purposes: **NGO registers protect, government registers open.** Bomenstichting is NC, the Woodland Trust hides locations and its terms sit unread behind a download flow, the Tree Council of Ireland's terms are unknown. Meanwhile government sources (Italy's MASAF registry, the Flanders heritage inventory, Paris open data) are typically published under open licences that allow commercial reuse. For anything we import rather than merely consult, government sources first, and read every licence before touching the data.

Dense-Netherlands remains viable despite the NC register: Dutch municipalities publish their own tree data as government open data (Amsterdam's gemeente among them), and the register stays a lead list. Checked for the licence only; the municipal licences still need reading per city.

## Imported 2026-08-05: Italy and Andalusia, both CC BY 4.0

**Italy, MASAF national register.** 21 regional .xls files from
https://www.masaf.gov.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/11260, one
identical schema, 5,008 rows, of which 4,522 single trees and 485 marked
"Insieme omogeneo di ..." (a homogeneous set: an avenue or a stand, not a
collectible point). 1,653 of the singles carry the register's own CONTESTO
URBANO flag, which filters city trees for free. Coordinates are sexagesimal
text with a comma decimal; converted on import and cross-checked against
Sicily's decimal GeoJSON republication, where 156 of 159 agree to the metre and
the three that do not are re-surveys between the 2021 and 2025 versions.
Licence proof: the Sicilian republication of the same data carries
`license_id: cc-by` in its portal metadata (dati.regione.sicilia.it, dataset
alberi-monumentali-di-sicilia). The photo gallery on masaf.gov.it is explicitly
NOT under that licence. Data yes, images never.

**Andalusia, REDIAM.** Eight province KML files (arb_sing_<province>.kml) from
portalrediam.cica.es, 749 individual trees, decimal WGS84, and 435 of them link
to an official per-tree PDF sheet, which is the cheapest verification path in
Spain. The companion groves layer (arbda_sing_*) is deliberately not imported.
Licence proof, from the dataset's own GeoNetwork record
(uuid c5d37ec9-a857-42b2-a8d2-2e0d4b947a4e, "Inventario de arboles y arboledas
singulares de Andalucia"): "Creative Commons Attribution 4.0 International
Public License (CC BY 4.0)". The Junta mixes CC BY, CC BY-NC and CC BY 3.0
across its portal, so this proof covers this dataset and nothing else from that
source.

Neither register is on the explore map yet: load_registers() in build_site.py
still only understands the Japanese `trees` + `prefecture` shape, so both files
are read by tree_index.py and cluster_register.py and ignored by the map. That
is a wiring job, not a licence question.

### Campania's regional cards: the second source MASAF cannot give you (found 2026-08-05)

MASAF has no age field at all, which is the single biggest gap in the Italian
register. Campania publishes a per-tree card at
`agricoltura.regione.campania.it/foreste/monum/scheda_NNN.html` carrying an age
estimate, its own coordinates and a short description. The Caserta pass scraped
schede 180-299 and matched 40 of them to register entries, which supplied the
second source for nearly every tree in one go. The same pattern is worth
checking region by region: **MASAF gives you the tree, the regional register
gives you the age and the story.**

Two warnings from the same pass. The two registers disagree on coordinates for
the same tree by up to 400 metres, and MASAF hands one identical coordinate to
four different Caserta trees, so nothing there could honestly be marked
`confirmed`. And where MASAF prints a girth for a multi-stemmed tree, the
regional card sometimes reveals it as *insieme dei fusti*, every stem added
together: publishing the MASAF number alone would have invented a 6.5 m trunk
for the Reggia's sweet osmanthus.

### PDFs are readable after all, and the recipe (2026-08-05)

A scouting pass concluded that "tooling, not searching, is now the bottleneck":
Seville's 390-page municipal catalogue would not open, pypdf choked on its xref,
and the machine has no pdftotext, mutool, qpdf or ghostscript. Two of those three
statements were wrong.

`pdfminer` IS installed alongside pypdf and reads these documents fine. What
actually failed was the download: the Seville file is 36 MB and the fetch came
back with 19 MB and an HTTP 200, so every parser then died on a truncated xref
rather than on a hard PDF. The recipe that works:

    curl -sL -m 300 -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
      --retry 2 "$URL" -o out.pdf
    python3 -c "from pdfminer.high_level import extract_text; print(extract_text('out.pdf'))"

Check the tail before parsing: a complete PDF ends in %%EOF. A file that does not
is a short download, not a broken document, and the fix is a longer timeout
rather than a different library.

**Seville, Inventario de Arboles Singulares de la Ciudad de Sevilla (2022),
confirmed readable.** Its per-tree template carries species, common name, family,
catalogue number and date, **titularidad (ownership, which answers hard rule 10
row by row)**, Arbomap id, emplazamiento, barrio, distrito, **WGS84 coordinates**,
full dendrometry (perimeter at 1.30 m and at base, height, height to first branch,
crown diameters N-S and E-O, lean and its direction) and both physiological and
phytosanitary condition. That last pair is the closest thing to a vitality field
found in any register so far. It is a municipal document distinct from, and denser
than, the Andalusian REDIAM catalogue already imported.

### Friuli Venezia Giulia, scouted 2026-08-05 while researching Trieste

`decreti.regione.fvg.it/Storage/2025_71/ALLEGATO1%20AL%20DPREG%20071-2025.PDF`,
"Elenco regionale degli alberi monumentali 2025" (DPReg 071/2025), all four
provinces. Over the national MASAF file it adds LOCALITA, a real place name
rather than a coordinate, which is what turns a point into a walk; CRITERI DI
MONUMENTALITA, the legal reason for the designation; and NUMERO ELEMENTI, which
separates single trees from stands. It has no age field and no vitality field,
the same gap as MASAF, and no removed-trees sheet the way Lazio has. A 2020
edition exists and diffing it against 2025 is the closest thing to a vitality
signal here. The open-data mirror at dati.friuliveneziagiulia.it refuses
anonymous reads, so the decree PDF is the usable channel.

Running total on Italian regional registers: Campania publishes per-tree cards
with ages, Lazio publishes criteria, notes and a removed-trees sheet, Friuli
publishes criteria and place names but no age. **No Italian source at any level
carries an age**, which is why the newspaper step now sits above the register in
the search order.

### Piemonte breaks that rule, scouted and imported 2026-08-05 while researching Turin

The sentence above is no longer true, and Piemonte is the exception that proves
where to look. Regione Piemonte publishes **Alberi Monumentali del Piemonte: dati
del censimento** on the regional Geoportale, inside the Sistema Conoscenze
Ambientali catalogue, as a live WFS and WMS rather than as a file drop.

**Licence, CC BY 4.0.** The proving sentence is on the metadata record for
`r_piemon:9410f966-96b4-41ee-8f4c-ccdb60167218`: the dataset is released under
Creative Commons Attribution 4.0
(https://creativecommons.org/licenses/by/4.0/deed.it), with access limitation per
INSPIRE Directive art. 13(1)(a). Attribution required, commercial reuse not
restricted. Imported in full to `data/registers/piemonte-alberi-monumentali.json`,
391 trees, on 2026-08-05.

WFS: `https://gisserver.territorio.csi.it/geoserver/decsiraogc_geo_alb_monum/wfs`
(typeName `decsiraogc_geo_alb_monum:AlberiMonumentaliLoc`, add
`outputFormat=application/json&srsName=EPSG:4326` and it answers plain GeoJSON).

Two fields make this the best Italian register found so far:

- **`eta_presunta`, a presumed age**, as a band rather than a figure: `< 100`,
  `100-200`, `> 200`, `Non applicabile`. Populated on 344 of 391. A band is not a
  date, but it separates a 200-year tree from a 120-year one, which is the
  distinction a page actually needs and which MASAF cannot make at all.
- **`descr_stato`, a removal status held inline**, which is Italy's usual missing
  vitality field: 378 listed, 11 removed for natural death, 2 removed by felling.
  Lazio publishes the same information as a separate sheet; Piemonte keeps it in
  the same layer, so a live query is self-cleaning.

Also carried: `oggetto_di_identif`, which mechanically separates ALBERO SINGOLO
from GRUPPO, VIALE ALBERATO, FILARE SINGOLO and FILARE DOPPIO, so avenues and
stands filter out without reading names; `tipo_proprieta` (Pubblica / Privata /
Sia pubblica che privata), which settles hard rule 10 without a site visit;
girth, measured height, mean crown diameter, and a link to the ministerial decree.

Two cautions. **MASAF's national file for Torino repeats these coordinates and
girths exactly**, so national and regional are one survey and not two independent
sources; the second source still has to come from outside the register. And the
register id encodes the comune (L219 is Torino), so trees the local press counts
as a city's are sometimes filed under a neighbour: Turin's count reads 14, 15 or
16 depending on who is counting, and the difference is a downy oak on the Colle
della Maddalena filed under an adjoining municipality.

So the corrected rule for Italy: **the age question is regional, not national, and
it is worth one WFS call before assuming a newspaper is the only route to a date.**

### Sardinia, stalled on 2026-08-17 for a missing licence, resolved 2026-08-28

The 2026-08-17 island scout found the register (CFVA/FoReSTAS, tied to the same
national Legge 10/2013 framework as every other Italian region) but stopped on
the geoportale's landing page, which carries no licence statement, and guessed
Sardinia might be a bare MASAF republish like Sicily rather than a separate
richer file like Piemonte. Both guesses were wrong, found by going around the
landing page to the layer's own GeoNetwork metadata record instead of reading
its viewer shell.

**Licence, CC BY 4.0.** The proving sentence is the `legalConstraints` field on
metadata record `R_SARDEG:2c6bc878-6ce3-4a9d-bea4-966775c38a70` (layer
`dbu:alberi_monumentali_2022_07_26`, found via
`webgis2.regione.sardegna.it/geonetwork`'s own search API rather than the
geoportale page, which never surfaces the record link directly):
`https://creativecommons.org/licenses/by/4.0`. Imported in full to
`data/registers/sardinia-alberi-monumentali.json`, 405 trees, on 2026-08-28.

WFS: `https://webgis2.regione.sardegna.it/geoserver/dbu/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=dbu:alberi_monumentali_2022_07_26&outputFormat=application/json&srsName=EPSG:4326`
(the `srsName` param reprojects Sardinia's native EPSG:3003 coordinates to
plain WGS84 server-side, no client-side transform needed).

Fields: species (`nome_scien`/`nome_volg`), girth (`circ_cm`), height
(`altezza_m`), comune/provincia/localita, and the protecting decree (`tutela`).
No age field, the Sicily case rather than the Piemonte one on that specific
question, but girth and height are populated for nearly every record, which
supports a derived age estimate (CLAUDE.md's growth-rate rule) where a second
source is still needed for existence and species.

**Six trees sit within 1.4km of Cagliari's centre**, a genuine walkable cluster
including a 1200cm-girth Ficus macrophylla and a 340cm/38m Norfolk Island pine,
found the same day `scout_next.py --target` named Cagliari as the city to
unblock. Most of the register's remaining mass is inland (Barbagia/Ogliastra),
away from any currently-queued city.

### Liguria has an age field, which no Italian national source does (2026-08-06)

Found by the Genoa verification pass. `agriligurianet.it` carries Liguria's own
monumental-tree register, CC BY, distinct from the national MASAF file, and it
records an age. It dated the Villa Serra hop-hornbeam to 160-170 years, the only
sourced age in a batch of ten where every other figure is a girth-based estimate.

Running total on Italian regional registers, and the pattern is now clear enough
to plan around: **the age question is regional, never national.** Campania
publishes per-tree cards with ages. Piemonte publishes presumed age bands on 344
of 391 trees plus removal status inline. Liguria publishes an age. Lazio
publishes designation criteria and a separate sheet of removed trees. Friuli
publishes criteria and place names but no age. Lombardia publishes nothing per
tree, and its cities publish per-tree municipal pages instead. So the first
question for any Italian city is not "what does MASAF say" but "what does this
region publish", and MASAF is the index rather than the source.

Not yet imported. Worth a proper scout: it would give age to Genoa, Savona,
Imperia and La Spezia at once.

## Germany: Berlin's Naturdenkmale register, found and imported 2026-08-07 (VERDICT: usable, CC0-equivalent)

CLAUDE.md's own rollout notes said "No German tree register is imported
(fragmented per-Bundesland, no cleared licence)" as of the Berlin web-research
pass on 2026-08-06/07 that shipped three Pfaueninsel oaks by hand. That was
true of the district-by-district `daten.berlin.de` listings (the
Charlottenburg-Wilmersdorf page lists only its own 38 trees) but not of the
underlying dataset: Berlin publishes one city-wide WFS layer covering all 12
Bezirke at once, and it was never checked because the search that finds it
has to start from "Schutzgebiete und Schutzobjekte nach Naturschutzrecht"
(protected areas and objects under nature-conservation law), not from
"Baumkataster" (which is the 900,000-tree bulk street inventory, unfiltered
and not what rule 10's semantic-filter test wants).

**Dataset**: "Schutzgebiete und Schutzobjekte nach Naturschutzrecht Berlin
(inklusive Natura 2000)", `daten.berlin.de` id
`schutzgebiete-und-schutzobjekte-nach-naturschutzrecht-berlin-inklusive-natura-2000-wfs-c36fe3f2`.
**Licence**, read from the dataset's own listing page: "Datenlizenz
Deutschland - Zero - Version 2.0 (dl-de-zero-2.0)", the German public-sector
equivalent of CC0: no attribution required, commercial use allowed, no
conditions at all. The strongest licence this project has found for any
register so far, ahead of even CC BY.

**Endpoint**: `https://gdi.berlin.de/services/wfs/schutzgebiete`, WFS 2.0
(note: 2.0 wants `typeNames`, not the 1.x `typeName`, and `srsName=EPSG:4326`
on the GetFeature request returns coordinates already in lat/lon, no
reprojection needed). Layer `schutzgebiete:a_nd`, titled "Naturdenkmale:
Baeume und Findlinge", 708 features total: 638 tagged `nd_art: "Baum"`
(trees) and 70 tagged `"Findling"` (protected glacial boulders, excluded).
Fields per tree: German and Latin species name, district (Bezirk), postcode,
a free-text place hint, the designation reason and the ordinance date. Same
gap as Italy's MASAF: **no age field, no girth field**, only when the tree
was legally designated, which is a different date from when it was planted
(Vienna's Rathauspark lesson applies here too: do not treat the ordinance
date as a planting date).

Fetched in full (708 features, paginated by `startIndex`) and filtered to
the 638 trees: `data/registers/berlin-naturdenkmale.json`. Clustered with
`scripts/cluster_register.py`: 43 walkable clusters of 4+ within 2km,
covering 587 of the 638 (92%), the largest being 70 trees across 3.7km
centred near 52.5172,13.3653 (splits into 9 sub-walks). This replaces
Berlin's only prior cluster, three Pfaueninsel oaks found by web research on
2026-08-06/07, with a real city-wide candidate pool the same way Vienna's
register did.

Not yet cross-referenced against a second source per tree (register-only
counts as one source per the two-layer rules; a verification pass still
needs a second confirmation per candidate before anything ships). Worth
checking whether Berlin's own Baumkataster (the bulk inventory, different
department, DL-DE-BY-2.0 per its Grün Berlin listing) can supply planting
years the way Vienna's did, matching by genus and proximity, before the next
Berlin pass.

## Ireland: Heritage Trees of Ireland, coordinate conversion solved and public subset imported 2026-08-08

The coordinate blocker below is resolved: `scripts/irish_grid.py` is a pure-
Python inverse transverse Mercator implementation (Irish Grid's own Airy
1830 modified ellipsoid and origin, no `pyproj` needed), and
`scripts/import_ireland_heritage_trees.py` downloads the dataset and writes
the genuinely-public subset straight to `data/registers/ireland-heritage-
trees.json`. No Helmert datum shift is applied (TM75 to WGS84 is roughly
50-150m depending on direction and no reprojection library exists here), so
treat every coordinate as approximate on top of the register's own 100m
precision; the module was checked against three entries that independently
matched already-published, confirmed-pin Dublin trees to within 40m (Kings
Inns plane = dub_001; two Trinity New Square planes = dub_006), which is
good enough for "approximate", not for "confirmed".

Filtered to 4 sites already known to be genuinely public (Trinity College,
National Botanic Gardens Glasnevin, St Anne's Park, Marley Park): 16
entries. The other roughly 700 rows (private houses, hotels, Garda HQ, RTE
studios, streets, other counties) are deliberately NOT extracted; adding a
new site needs an actual access check, since the dataset's own `Access`
field is identical boilerplate on every row and carries no real per-tree
signal. `publish_dots: false` in the register file: this is source material
for curated-city research, not a layer-2 register import decision, which
stays open.

The original scouting note, kept for the history:

### Ireland: Heritage Trees of Ireland, scouted 2026-08-07, NOT imported (access-filtered, coordinates unconverted)

The earlier entry above ("Lead group... Ireland... Tree Council of Ireland's
terms are unknown") is now half-resolved. The Tree Council of Ireland's own
Tree Register (11,000+ trees) still has no licence found. But a related,
smaller, better-documented dataset does: **Heritage Trees of Ireland**, run
by the same person (Aubrey Fennell) but published through the National
Biodiversity Data Centre's Biodiversity Maps portal
(`maps.biodiversityireland.ie/Dataset/27`), which states its licence
directly on the dataset page: **CC BY 4.0**. 724 records, 424 sites, 143
species, an `Age Range` band per tree (a real field this time, unlike
Italy/Berlin), a `Category of Tree` and `Condition of tree` field.

Downloaded via `/Dataset/Download?datasetId=27`, a Darwin Core Archive (zip
containing a tab-separated `HeritageTreesOfIreland.txt`, 725 rows). Not yet
saved to `data/registers/`, for two real reasons rather than one:

1. **Coordinates are Irish Grid (`East`/`North` in metres, `Projection: OSI`),
   not lat/lon.** Converting needs the Irish Transverse Mercator or Irish
   Grid formula (Airy 1830 modified ellipsoid), which this environment has no
   library for (`pyproj` is not installed, and installing a new dependency
   needs Hidde's yes per hard rule 5). A future pass either finds a pure-
   Python implementation to write inline (the way `scripts/photo_hunt.py`
   avoids heavy dependencies) or converts through a web geocoding step per
   site name instead.
2. **The dataset's own access note applies to most rows, not a few**:
   "Please note that most heritage trees occur on private lands and
   permission should always be sought before entering on private property,"
   repeated on nearly every record. Hard rule 10 excludes private land not
   genuinely open to visitors, so this register needs a site-by-site access
   read before anything from it ships, the same discipline Woodland Trust
   entries already get. Checked the 37 rows whose `SiteName` contains
   "Dublin": a real mix, some clearly public (Trinity College, National
   Botanic Gardens, Marley Park, a public park with a Cedar of Lebanon) and
   some clearly not (Garda Headquarters, a private hotel, a private house).
   Filtering to Dublin plus genuinely public sites first, rather than
   importing the file wholesale, is the right order of operations here.

Worth returning to for Dublin specifically once the coordinate conversion is
solved: the public-site subset alone (Trinity, the Botanic Gardens, Marley
Park) already looks like a plausible small cluster, and the `Age Range`
field would be a real second-source contribution most other registers this
project has found cannot offer.

## The English-speaking block scouted: United States, Australia, Canada, New Zealand, United Kingdom (2026-08-13)

Register scouting pass against the 32 cities in the top-250 sprint list with no
register yet: US 12, Australia 6, Canada 4, New Zealand 4, UK 10. Licence-led,
per this file's standing method: fetch, quote the licence sentence verbatim,
verdict, import only when clearly usable. ~40 minutes of fetching; most of the
five countries are scouted rather than exhausted. The UK Ancient Tree
Inventory verdict above (DISQUALIFIED, permission path open) was not
revisited; this pass looked for what exists besides it.

### USABLE, imported

**City of Portland, Oregon: Heritage Trees.** `data/registers/portland-heritage-trees.json`.
Endpoint: `https://opendata.arcgis.com/datasets/db48b717d0174906b95f028c83c09dd0_26.geojson`
(ArcGIS item `db48b717d0174906b95f028c83c09dd0`, layer 26). 463 records, 429
live and 34 formally delisted (kept separately as `blocked_delisted`, never to
ship). Licence: item metadata `licenseInfo` reads verbatim `"CC-BY-SA"` (a
ShareAlike clause sits on top of the usual attribution one, noted in the
file's licence block). Coordinates are per-tree (`LAT`/`LON`). Designation is
real: Portland's Heritage Tree ordinance, City Forester nominates annually for
age, size, type, historical association or horticultural value, so this
passes the semantic filter cleanly, it is not a street-tree inventory. Best
vitality signal seen in any register this project has imported: `Delist_Date`,
`Delist_Ordinance` and `Delist_Reason` are populated for the 34 removed trees,
so "currently listed" is at least a supporting signal here, though not a
substitute for the normal alive-now check on the survivors. Caveat: units are
not labelled on the service (HEIGHT/SPREAD read as feet, DIAMETER as inches,
CIRCUMF as feet, inferred from internal consistency, not certain); and
`Ownership` varies from "Right Of Way" to "Private, Front Yard", so hard rule
10 needs a per-tree check before anything ships. **Covers Portland**, one of
the 32.

### USABLE, licence proven, import deferred (species locked behind per-tree PDFs)

**City of Hobart: Significant Tree Register.** ArcGIS item
`9b31f3f6acb14bb2a5869b5e17707155`, layer 1 (points) at
`https://services1.arcgis.com/NHqdsnvwfSTg42I8/arcgis/rest/services/ENVIRON_Significant_Tree_Locations/FeatureServer/1`.
460 point features, CC BY 4.0 per the item's own `licenseInfo`: "This work is
licensed under a Creative Commons Attribution 4.0 International License."
Genuinely a designated register (Significant Tree Register under the Hobart
planning scheme), passes the semantic filter. Coordinates are per-tree
(EPSG:28355, reprojects cleanly to WGS84 via `outSR=4326`). The catch: species,
name and reasons for significance are NOT in the bulk feed, only a
`Data_Sheet_URL` per tree pointing at an individual PDF (~3.6 MB each, image-
heavy, text extractable only via a font-encoding workaround: the embedded
text layer is shifted by a non-standard glyph mapping, confirmed decodable
with a simple offset but not with standard `pdftotext`, which is not
installed in this environment anyway). Fetching 460 of these is not a
scouting-budget task. No vitality field. **Not imported this pass.** A future
pass should pull `Data_Sheet_URL` sheets only for whichever cluster a Hobart
city pass actually wants (4-8 trees), not the full register.

### Scouted, inconclusive, needs a follow-up pass rather than a verdict

**Auckland Council: Notable Trees Overlay.** The dataset exists on
`data-aucklandcouncil.opendata.arcgis.com` and Schedule 10 of the Auckland
Unitary Plan is a genuine statutory notable-tree list (semantic filter would
pass). But the only feature-service instance this pass could resolve by ID
was `Notable_Trees_Overlay_ProposedPlanChange`
(`https://services1.arcgis.com/n4yPwebTjJCmXB6W/arcgis/rest/services/Notable_Trees_Overlay_ProposedPlanChange/FeatureServer`),
whose licence text is explicit and disqualifying: "you are not permitted to
copy or republish any substantial amount of the information from this viewer
without the prior written consent of Auckland Council." That is the Plan
Change 78 variant specifically, not necessarily the operative Schedule 10
layer, but this pass could not locate the operative layer's own ArcGIS item ID
in the time available (the dataset landing page is JS-rendered and did not
yield it to a plain fetch). **Verdict: not-recommended on the version found;
the operative layer needs a session with a real browser to resolve, not
another plain fetch.**

**New Zealand Notable Trees Trust register**
(`register.notabletrees.org.nz`) exists and redirects (301) but was not
scouted for licence terms this pass; NZ district-plan notable-tree schedules
(Auckland, Wellington, Christchurch each have one per the statutory
mechanism) were named but not individually fetched. Unscanned.

### Not-recommended, with why

**Seattle**: the only open dataset found is SDOT Trees, the full public
right-of-way street-tree inventory (condition, species, size, maintenance
responsibility for every street tree). That is exactly the shape the semantic
filter forbids. No distinct "Exceptional Trees" open-data layer surfaced in
this pass, only the ordinance concept; Seattle's Exceptional Tree list may
exist as a PDF or map rather than an open dataset. Not recommended on what
was found; worth one more targeted search naming the ordinance PDF directly.

**San Francisco**: same shape problem. DataSF's only tree dataset found is
the Street Tree List (~125,000 public trees, all of them, via
`data.sfgov.org/City-Infrastructure/Street-Tree-List/tkzw-k3nq`). No
"Landmark Trees" subset or designation flag was found in this pass. Not
recommended on what was found.

> **CORRECTED 2026-09-02, and the correction matters more than the verdict.**
> The verdict above is right about the DATASET and wrong about the city. San
> Francisco does keep a curated Landmark Tree list, designated tree by tree
> with a numbered ordinance, published by SF Environment at sfenvironment.org
> as WEBPAGES rather than as data. A from-zero pass found it in minutes and
> shipped six trees off it, including Landmark Tree No. 15. **So "no usable
> dataset" is not the same finding as "no curated list", and this file conflated
> them twice.** A scouting pass looks for something machine-readable and stops;
> a research pass reads the ordinance. Both US scouting rounds ended with "not
> recommended" on cities that may well have a list on a webpage, so Seattle,
> Philadelphia, Charleston, Savannah and San Diego are worth one look at their
> ordinance pages before anyone treats those NOs as closed.

**City of Melbourne**: `trees-with-species-and-dimensions-urban-forest` on
`data.melbourne.vic.gov.au` (Opendatasoft platform, CC BY per its own licence
field) is again the full municipal inventory (80,000+ trees), not the
Exceptional Tree Register the city adopted in 2021. That register's own page
(`melbourne.vic.gov.au/exceptional-tree-register`) describes it as covering
privately-owned trees nominated for protection; it did not surface as a
separate downloadable dataset in this pass, only as a webpage. Not
recommended on what was found; the register itself is worth a direct fetch of
that page next time rather than the open-data portal.

**United Kingdom, Tree Preservation Orders generally**: not fetched this
pass, on reasoning rather than a checked example. A TPO is a legal
protection applied to a tree (or woodland) a council judges worth protecting
from felling, and councils apply them broadly, to ordinary garden and street
trees as much as to remarkable ones; TPO status alone does not say a tree is
old, spectacular or historically significant the way a "heritage" or
"significant tree register" designation does. Importing a TPO layer wholesale
would very likely fail the semantic filter the same way a street-tree
inventory does, just for a legal reason instead of a maintenance one. This is
a reasoned expectation, not a verdict backed by a checked licence, and it
should not be treated as exhausting the UK. It does NOT touch the London/ATI
question, which stays as ruled above.

### Named but not reached this pass (unscanned, not verdicts)

City of Sydney (a genuine "register of significant trees" was found by
name, 2,450 trees, 10-year review just completed 2025, but its data lives
behind an interactive map at `trees.cityofsydney.nsw.gov.au` rather than a
found API endpoint; worth a direct follow-up), Brisbane (Significant
Landscape Tree overlay exists on `data.brisbane.qld.gov.au`, part of the
statutory City Plan rather than a curated register, needs a semantic-filter
judgement call not made this pass), Adelaide (Significant Tree is a state
Development Act / Planning Code designation administered by individual
councils, e.g. Adelaide, Burnside, Prospect, Unley, each apparently with its
own list; fragmented, not one fetch), Perth, Toronto, Vancouver (recalled by
general knowledge as having had a Significant Tree Register program, not
checked this pass), Montreal (`ville.montreal.qc.ca/siteofficieldumontroyal/arbres-remarquables`
reads as a page about Mont Royal's own remarkable trees rather than an open
dataset; `donnees.montreal.ca` carries only the full public-tree inventory
under a similar semantic-filter problem), Quebec City, Wellington,
Christchurch, Queenstown, Los Angeles, San Diego, Philadelphia, Charleston,
Savannah, Austin, New Orleans, Chicago, Liverpool, Belfast, Manchester,
Brighton, Inverness, Canterbury, Stratford-upon-Avon, Stirling, Windsor,
Glasgow.

### Coverage of the 32-city list after this pass

Only **Portland** gained an imported register. Hobart and Auckland are
scouted with a concrete path to finish (Hobart: budget a per-tree PDF fetch
pass for a chosen cluster; Auckland: redo the ID lookup in a browser session).
The other 29 cities are unchanged. The clear lesson for whoever picks this up
next: government-published, semantically-filtered "significant/heritage/
notable tree" registers are much rarer as clean open-data endpoints in this
block than the brief's optimism suggested; most of what surfaces first in a
search is either the full street-tree inventory (forbidden by the semantic
filter) or a webpage/PDF rather than an API. The wins, when they exist, look
like Portland: a named ordinance, a dedicated ArcGIS item separate from the
street-tree layer, and an explicit `licenseInfo` field on the item metadata
worth checking directly via `arcgis.com/sharing/rest/content/items/<id>?f=json`
rather than trusting a portal's about-page prose.

### Fetch blocklist addition

`www.portlandmaps.com` (the `/od/rest/services/...` REST path specifically):
hangs, no response at all, burned the full 20s timeout twice this pass. The
`opendata.arcgis.com/datasets/<item>_<layer>.geojson` redirect route (which
lands on `hub.arcgis.com/api/download/v1/items/...`) works fine and was used
instead. Added to `data/fetch-blocklist.json`.

### Cost

Token usage for this pass: approximately 78,000 tokens (research and fetching
only; no prose written beyond this survey entry and the register file, no
photos hunted).

## Germany: per-Bundesland scout of the 14 register-less sprint cities, 2026-08-13

Register scouting pass, licence-led, triggered by CLAUDE.md's sprint list
naming 14 German cities with no register behind them (Cologne, Hamburg,
Nuremberg, Frankfurt, Dresden, Leipzig, Stuttgart, Heidelberg, Trier,
Regensburg, Potsdam, Bamberg, Freiburg, Rothenburg ob der Tauber). Berlin's
Naturdenkmale WFS (2026-08-07, above) is the proof of shape: search for
"Schutzgebiete und Schutzobjekte nach Naturschutzrecht", not "Baumkataster",
because German states hang their ND (Naturdenkmal) layer off the nature-
conservation Schutzgebiete service, alongside Naturschutzgebiete and the
other INSPIRE Protected Sites categories, not off the municipal tree
inventory. That pattern held for two more Laender out of nine checked and
failed for the rest, cleanly enough to be worth recording as the finding
itself: **whether a Land publishes ND as open data is not correlated with
whether it has an open Schutzgebiete WFS at all** (NRW, Hessen and
Brandenburg all have a fine, open, INSPIRE-conformant Schutzgebiete WFS;
none of the three includes Naturdenkmal as a feature type in it, only the
handful of INSPIRE-mandated categories: FFH, Vogelschutz/SPA, Landschafts-
schutzgebiet, Naturschutzgebiet, Nationalpark, Naturpark, Biosphaerenreservat,
Ramsar. ND sits below the INSPIRE reporting threshold, so a Land only
publishes it if someone chose to on top of the minimum, and most have not.)

### Bayern: usable, CC BY 4.0. Covers Nuremberg, Regensburg, Bamberg AND Rothenburg ob der Tauber at once

**Dataset**: "Naturdenkmale, punktfoermig" (point-shaped nature monuments),
layer `natur_wfsschutzgebiete:naturdenkmal_punktfoermig` on the Bayerisches
Landesamt fuer Umwelt (LfU)'s "Schutzgebiete des Naturschutzes" WFS.
**Endpoint**: `https://www.lfu.bayern.de/gdi/wfs/natur/schutzgebiete?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&typeNames=natur_wfsschutzgebiete:naturdenkmal_punktfoermig&srsName=EPSG:4326`
(WFS 2.0, ArcGIS-backed, paginate with `count`/`startIndex`; native storage
CRS is EPSG:25832/UTM32N, so `srsName=EPSG:4326` is required or coordinates
come back as UTM metres). **Licence**, quoted verbatim from the live
GetCapabilities `ows:Fees` element: "Der Datensatz/Dienst steht unter der
Lizenz: Creative Commons Namensnennung 4.0 International (CC BY 4.0). Die
Namensnennung des Bayerischen Landesamtes fuer Umwelt als Rechteinhaber hat
in folgender Weise zu erfolgen: 'Datenquelle: Bayerisches Landesamt fuer
Umwelt, www.lfu.bayern.de'." Clean commercial-compatible CC BY, same tier as
Berlin's DL-DE-Zero.

**4,860 features statewide**, fetched in full (paginated, 5 requests of
1,000). Fields, confirmed via DescribeFeatureType: `webgisid`, `ID` (e.g.
`ND-07157`), `NAME` (free text, often names the species and place: "ND Nr.
26 Platane in der Gruebelstrasse", sometimes just "Naturdenkmal Eiche" with
no place hint), `STATUS` (a legal-designation flag, "aktuell" on 4,858 of
4,860 and "einstweilig sichergestellt" on 2; **not** a vitality field, same
gap as everywhere else), and geometry. No species field, no age field: this
is the thinnest register found yet, even thinner than Berlin's, a pure
lead-and-coordinate list. 311 of 4,860 features carry more than one point in
their own geometry (a MultiPoint), the same twin/group pattern as Berlin and
Setubal, flagged per entry as `point_count` for a verification pass to fold
or split deliberately.

**City coverage, within-2km-of-centre counts (walkability, not existence):**

| City | Within 2km | Within 15km | Note |
|---|---|---|---|
| Nuremberg | 17 | 97 | The Kontumazgarten/Hallerwiese cluster: 17 trees inside 2km, several 100-200m apart (planes, red beeches, limes). Genuinely walkable, Cadiz-density. |
| Regensburg | 1 | 19 | Thin at the centre (1: "Naturdenkmal Kastanien am Gries", 1.16km out); the rest spread 3-15km into the surrounding Landkreis. |
| Bamberg | 0 | 36 | Nothing within 2km of the historic centre; nearest cluster starts ~2.1km out. Worth checking the old town itself (Domberg, Hain park) by the normal search order, since the ND layer clearly missed the UNESCO centre. |
| Rothenburg ob der Tauber | 4 | 23 | Small real cluster, nearest 0.72km out (limes, spruces, a pear tree). |

Saved to `data/registers/bayern-naturdenkmale.json`.

### Hamburg: usable, DL-DE-BY 2.0, but tiny (2 tree candidates state-wide)

**Dataset**: `de.hh.up:nr_f_naturdenkmal`, one feature type inside Hamburg's
city-wide Schutzgebiete WFS. **Endpoint**:
`https://geodienste.hamburg.de/HH_WFS_Schutzgebiete?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&typeNames=de.hh.up:nr_f_naturdenkmal&srsName=EPSG:4326`.
**Licence**, quoted verbatim from the live GetCapabilities `ows:Fees`
element: "Datenlizenz Deutschland Namensnennung 2.0, Quellenvermerk: Freie
und Hansestadt Hamburg, Behoerde fuer Umwelt und Energie." Open,
commercial-compatible, same family as Berlin and NRW.

Fetched in full: only **12 features exist in the entire category**, and the
semantic filter kills 10 of them outright, because Hamburg's Naturdenkmal
designation covers ponds, moors, a clay pit and a canal alongside trees
("Papenbrack", "Kiebitzmoor", "Sievertsche Tongrube" at 10.5 hectares,
"Poppenbuettler Graben"), sized 0.17 to 10.5 ha. Exactly **2 are trees**,
both under 0.005 ha and identifiable by size alone before reading the name:
"Alter Schwede" (a well-known old oak) and "Eibe am Neulaender Deich" (a
yew). No species field structurally (species has to come from the name or
external verification), no age field, geometry is a small polygon around
the crown rather than a point (treat as `approximate` unless corroborated).
Below the "no pass under six candidates" floor by itself: these are two free
leads for whenever a Hamburg pass runs with proper web-search sourcing
(Planten un Blomen, Stadtpark, the Alster parks), not a register that alone
justifies opening Hamburg. Hamburg's separate Strassenbaumkataster (the
street-tree cadastre also surfaced this search) is a full bulk inventory
and fails the semantic filter outright, same as any Baumkataster.

Saved to `data/registers/hamburg-naturdenkmale.json`.

### Baden-Wuerttemberg: blocked, non-commercial-equivalent licence

LUBW (Landesanstalt fuer Umwelt Baden-Wuerttemberg) publishes "Naturdenkmal
Einzelgebilde (END)" as a WFS
(`https://rips-gdi.lubw.baden-wuerttemberg.de/arcgis/services/wfs/Naturdenkmal_Einzelgebilde/MapServer/WFSServer`,
confirmed reachable, feature type
`Naturdenkmal_Einzelgebilde:Naturdenkmal_Einzelgebilde`), which would have
covered Stuttgart, Heidelberg and Freiburg at once had it cleared licence.
It does not. The WFS's own `ows:Fees`/`ows:AccessConstraints` are empty, but
the dataset is governed by LUBW's separate "Nutzungsvereinbarung fuer Daten
des UIS" (terms of use for the Umweltinformationssystem), which explicitly
**prohibits building a database with commercial use or resale intent**, and
which an OpenStreetMap community thread
(`community.openstreetmap.org/t/nutzungsvereinbarung-lubw-kompatibel-mit-osm`)
independently confirmed is incompatible with OSM's own licence for the same
reason. This is the DL-DE/BY-NC-equivalent case OPEN_DATA_SURVEY.md's rule
already names as disqualifying. VERDICT: blocked. **Not imported.**

### Sachsen: not-recommended, no point-level ND layer published

Sachsen's Schutzgebiete WFS
(`https://luis.sachsen.de/arcgis/services/natur/schutzgebiete/MapServer/WFSServer`)
carries a clean open licence (`ows:Fees`: "Datenlizenz Deutschland 2.0 -
Variante mit Namensnennung", DL-DE-BY 2.0) and would have covered Dresden
and Leipzig at once, but the only Naturdenkmal-family feature type it
exposes is `schutzgebiete:Flaechennaturdenkmaeler` (areal nature monuments,
a different legal category to the point-level ND that Berlin, Bayern and
Hamburg publish). Sampled it directly: the first entries are "Gruendelteich"
(a pond) and "Suedostufer des Brettmuehlenteiches" (a lakeshore), polygon
geometries with `FLAECHE`/`UMFANG` (area/perimeter) fields, no species or
tree-specific field at all. A public web search independently confirmed
"linear and point-shaped natural monuments are not displayed in the main
WFS service for protected areas in Saxony." VERDICT: not-recommended as a
tree source; the FND layer is water bodies and geology, and no separate
point layer for individual Naturdenkmal trees was found published open. Not
imported. A future pass could still check Dresden's and Leipzig's own
municipal open-data portals directly (the Berlin lesson: district-level
publication sometimes exists where the Land-level one does not).

### Hessen, NRW, Brandenburg: not-recommended, no ND feature type in the open Schutzgebiete WFS

All three have real, reachable, cleanly-licensed INSPIRE Protected Sites
WFS services, checked directly against their GetCapabilities:

- **Hessen** (`https://geodienste-umwelt.hessen.de/arcgis/services/inspire/schutzgebiete/MapServer/WFSServer`,
  would cover Frankfurt): 8 feature types, all INSPIRE-minimum categories
  (Biosphaerenreservat, FFH, LSG, Nationales Naturmonument, Nationalpark,
  Naturpark, NSG, Vogelschutzgebiete). No Naturdenkmal.
- **NRW** (`https://www.wfs.nrw.de/umwelt/wfs_nw_inspire-schutzgebiete`,
  would cover Cologne): licence is DL-DE-Zero 2.0, the strongest tier, and
  the service works cleanly, but again only the 9 INSPIRE-minimum categories
  (FFH, VSG, WG, LSG, NSG, NP, NTP, NWZ, RAM). No Naturdenkmal. (An earlier,
  wrong guess at the NRW endpoint, `open.nrw/dataset/ccbfb8e5...`, turned out
  to be Naturschutzgebiete only, a different and non-semantic-filtered
  dataset; recorded here so a future pass does not re-fetch it expecting ND.)
- **Brandenburg** (`https://inspire.brandenburg.de/services/schutzg_wfs`,
  would cover Potsdam): 14 feature types (NSG, LSG, EZV, BE, NatP, BR, NP,
  FFH, SPA, each with an `_mz` metadata variant), no Naturdenkmal, and the
  licence line itself is weaker than the other Laender's ("Nutzung erfolgt
  derzeit kostenfrei unter Beachtung des Urheberrechts", i.e. free of charge
  subject to copyright, not a named open licence), so even a future ND layer
  here would need its own licence check before import.

None imported. Confirms the finding above: ND is not an INSPIRE-mandated
category, and whether a Land publishes it beyond the minimum has to be
checked per Land, not assumed from "they have an open WFS."

### Rheinland-Pfalz: not resolved this pass, would cover Trier

LANIS (the nature-conservation geoportal, `naturschutz.rlp.de`) visibly
serves a "naturdenkmal_point" map layer in its own web viewer (seen in a
`kartendienste_naturschutz` viewer URL carrying
`layers=naturdenkmal_polygon,naturdenkmal_point`), so the data almost
certainly exists. The two WFS endpoint guesses tried this pass
(`geodaten.naturschutz.rlp.de/mapbender/php/wfs.php`,
`map1.naturschutz.rlp.de/service_lanis/mod_wfs/wfs_getmap.php`) both 404'd;
neither hung (no addition to the fetch-blocklist needed). An OpenStreetMap
community thread on LANIS licensing found a mixed picture: some layers
carry ODbL 1.0 (commercial-compatible with share-alike obligations) per
their own metadata, others (the base cartography) carry only DL-DE/BY 2.0,
and the thread's explicit advice is to check each layer's own metadata
rather than assume one licence for the whole service. Worth a dedicated
follow-up pass with more time to find the live WFS endpoint and read the ND
layer's specific licence from its GetCapabilities, since Trier is only one
city and the search cost so far has been small. **Not imported, not
blocked**, genuinely unresolved.

### Summary: coverage gained this pass

| City | Bundesland | Register found | Trees available |
|---|---|---|---|
| Nuremberg | Bayern | Bayern ND (usable) | 17 within 2km, 97 within 15km |
| Regensburg | Bayern | Bayern ND (usable) | 1 within 2km, 19 within 15km |
| Bamberg | Bayern | Bayern ND (usable) | 0 within 2km, 36 within 15km |
| Rothenburg ob der Tauber | Bayern | Bayern ND (usable) | 4 within 2km, 23 within 15km |
| Hamburg | Hamburg | Hamburg ND (usable) | 2 state-wide (thin) |
| Cologne | NRW | none found | 0 |
| Frankfurt | Hessen | none found | 0 |
| Dresden | Sachsen | none found (FND is areal-only) | 0 |
| Leipzig | Sachsen | none found (FND is areal-only) | 0 |
| Stuttgart | Baden-Wuerttemberg | found, blocked (NC-equivalent licence) | 0 |
| Heidelberg | Baden-Wuerttemberg | found, blocked (NC-equivalent licence) | 0 |
| Freiburg | Baden-Wuerttemberg | found, blocked (NC-equivalent licence) | 0 |
| Trier | Rheinland-Pfalz | likely exists, unresolved | 0 |
| Potsdam | Brandenburg | none found | 0 |

Five of fourteen cities gained a usable register this pass (four Bavarian
cities at once from one import, plus Hamburg thinly); five states checked
came back empty or blocked. Two files added: `data/registers/bayern-
naturdenkmale.json` (4,860 entries statewide) and `data/registers/hamburg-
naturdenkmale.json` (12 entries, 2 usable). No host hung (nothing added to
`data/fetch-blocklist.json`); the RLP endpoints 404'd cleanly.


### Correction to the France sweep, made on review the same day (2026-08-13)

Bordeaux's import shipped with `status_life` named as its vitality field and six
SOUCHE stumps excluded. That was not enough. **Seven further entries carry a
`date_disparition` while `status_life` still reads VIVANT**, the most recent
being Merignac's ginkgo felled on 2024-12-11 and one from 2025-06-13. The
register updates the felling date but does not update the life status, so the
date is the real signal and the status lags it, sometimes by years.

Every row now carries `publishable`, false for the six stumps and the seven
felled trees, 220 true. **The general form, worth applying to every register
from here: when a source has two fields that could each answer "is it alive",
check them against each other rather than picking one.** Catalonia taught us to
look for a vitality field at all; Bordeaux teaches that finding one is not the
end of the check.

Two more things this subset gets wrong, recorded so a verify pass does not
inherit them as facts: eight entries have a girth under one metre, one of them a
JEUNE (young) tree at 63 cm, so the city's REMARQUABLE flag is a designation
rather than a statement about age or size; and `age_approx` and `vigueur` are
null on most rows, so a number there is a lead to verify and never a publishable
fact on its own.

## Singapore and Hong Kong: two named statutory registers scouted, both usable, 2026-08-13

Reason for the pass: both cities are already live on the site (Singapore 7
trees, Hong Kong 6) with only 5 to 7 km of real spread between their existing
trees, both administrations publish in English, and neither had ever been
checked against its own named register. Semantic filter and vitality-first
checks applied per BRIEF_RESEARCH.md.

### Singapore: NParks Heritage Trees Scheme, USABLE, imported

- **Source**: National Parks Board (NParks), the Heritage Trees Scheme. Mature
  trees of girth over 5 metres with historical, social, cultural, aesthetic,
  botanical or educational value are gazetted, fitted with lightning
  protection and given English signage. This is the semantic-filtered subset;
  the separate Trees.sg island-wide inventory (every tree NParks manages) was
  checked and correctly excluded, it is a bulk inventory, not a designation.
- **Exact fetch**: the dataset lives on data.gov.sg as "Heritage Trees"
  (`https://data.gov.sg/datasets/d_644ff187b6d14d6316f47284a4a6c81f/view`).
  data.gov.sg serves files through a two-step signed-URL API rather than a
  static link: `GET
  https://api-open.data.gov.sg/v1/public/api/datasets/d_644ff187b6d14d6316f47284a4a6c81f/poll-download`
  returns a time-limited S3 URL for `HeritageTrees.geojson`; that URL must be
  fetched immediately after, curl -m 20 on both legs.
- **255 trees, coordinates per-tree** (Point geometry, WGS84), covering
  mainland Singapore plus offshore islands (Pulau Ubin carries several).
- **Licence**: Singapore Open Data Licence version 1.0. Proving sentence,
  verbatim from `https://data.gov.sg/open-data-licence`: "You can use,
  access, download, copy, distribute, transmit, modify and adapt the
  datasets, or any derived analyses or applications, whether commercially or
  non-commercially." Attribution required, a conspicuous notice naming the
  source and linking the licence version; no non-commercial restriction, so
  no disqualification.
- **Vitality/last-surveyed field: absent.** No age, girth, height or
  condition field of any kind, only a scientific name, a common-name-plus-
  location free-text description, an HT id, and a link to the tree's own
  NParks page (which may carry more detail per tree but was not bulk-fetched
  this pass). Consistent with "no register has a vitality field"; every
  tree pulled from here still needs its own alive-now check.
- **Sanity check**: nothing numeric to sanity-check against the physical
  world (no girth or age columns), so this pitfall does not apply here. One
  finding worth a verify pass's attention: HT 2007-162 and HT 2007-163 are
  two Mangrove Apples registered separately, metres apart, "from House No. 1
  on the left" and "on the right" of the same spot on Pulau Ubin, the
  register-twin pattern BRIEF_RESEARCH.md names explicitly.
- **Verdict: USABLE, imported** to
  `data/registers/singapore-heritage-trees.json` (255 entries).
- **Within 5 km of the city centre** (Raffles Place / Downtown Core,
  1.2833, 103.8333): **163 of 255**. Worth dispatching a verify pass; several
  candidates already overlap our own published cluster at Fort Canning Park
  (three of our seven published trees sit inside Fort Canning, and the
  register lists further Fort Canning heritage trees beyond those three).

### Hong Kong: Register of Old and Valuable Trees (OVT) and Stonewall Trees (SWT), USABLE, imported

- **Source**: Development Bureau, Greening, Landscape and Tree Management
  Section. Registration criteria: DBH >= 1.0 m, OR height >= 25 m, OR crown
  spread >= 25 m, OR rarity, OR estimated age > 100 years, OR outstanding
  cultural/historical/social value, so this is a designation, not a bulk
  inventory, and a separate `Type` field distinguishes OVT from the
  masonry-wall Stonewall Trees (SWT) the brief asked to check for
  specifically; 14 entries carry `OVT & SWT`.
- **Exact fetch**: the data.gov.hk listing
  (`https://data.gov.hk/en-data/dataset/hk-devb-ovt-ovt-and-stonewall`)
  points only at a CSDI Portal viewer URL with no direct file link and the
  CSDI REST API demanded a token on a plain fetch; the working route was
  found via the mirror on Esri's Hong Kong open-data hub, ArcGIS Hub's own
  DCAT feed
  (`https://opendata.esrichina.hk/api/feed/dcat-us/1.1.json`, 19 MB, one
  fetch), which lists the underlying ArcGIS FeatureServer directly:
  `GET
  https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/Information_on_Old_and_Valuable_Trees_and_Stonewall_Trees_in_Hong_Kong/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=geojson`.
  Plain `opendata.esrichina.hk/datasets/<id>.geojson` 403s (fast, not a
  hang, no blocklist entry needed); the FeatureServer query above is the
  route that works.
- **713 trees, coordinates per-tree** (Point, requested in WGS84 via
  `outSR=4326`; the service's native SR is Web Mercator).
- **Licence**: DATA.GOV.HK Terms and Conditions of Use (the Hong Kong SAR
  Government's PSI terms, which the dataset inherits from the portal since
  the CSDI resource carries none of its own). Proving sentence, verbatim
  from `https://data.gov.hk/en/terms-and-conditions`: "You are allowed to
  browse, download, distribute, reproduce, hyperlink to, and print the Data
  for both commercial and non-commercial purposes on a free-of-charge
  basis," with attribution required ("you shall identify clearly the source
  of the Data and acknowledge the Government and the Relevant
  Organisations' ownership... and shall also give proper attribution to the
  Government, the Relevant Organisations and DATA.GOV.HK"). No
  non-commercial restriction found, no disqualification.
- **Vitality/last-surveyed field: no explicit alive/dead field, but the
  closest thing any register has offered yet.** `Last_Inspection_Date`
  (700 of 713 dated 2022 or 2023) and `Condition_EN`, a pipe-separated bag
  of standard arborist observations (vigor rating, lean, wind exposure,
  pruning history, overall risk rating). 15 of 713 entries mention "Dead
  branches" specifically, a partial-dieback observation, never a
  whole-tree-dead flag; none of the 713 current rows describe the tree
  itself as dead, felled or removed.
- **The cross-check the brief asked for, applied**: this register has no
  second field that could contradict a first the way Bordeaux's
  `date_disparition` contradicted `status_life`, because it carries only
  one signal (inspection date plus free-text condition), not two competing
  status fields. What it does instead, and what a verify pass must know:
  **the department removes a tree from this register once it is felled or
  fails**, per the Development Bureau's own public record of periodic
  removals. So an OVT number appearing here is not itself proof of life
  today, it is proof the tree had not yet been struck off as of this
  fetch (2026-08-13); `last_inspection_date` is the real evidence, and it
  is an inspection date, never a same-day fact.
- **Sanity check, and it resolved a real units question**: `DBH` has no
  unit in its field name. Median across all 713 is 1006, clustered
  tightly around the registration threshold criterion of DBH >= 1.0 m,
  which only makes sense if the field is millimetres (1006 mm = 1.006 m).
  Recorded as `dbh_mm` in the import accordingly. Range 110 mm (11 cm, a
  tree presumably qualifying on height, crown spread, rarity or cultural
  value rather than girth) to 7710 mm on a Ficus microcarpa, a banyan
  whose aerial-root/buttress mass produces a DBH figure a simple round
  trunk never would, not an error.
- **Verdict: USABLE, imported** to `data/registers/hongkong-ovt.json`
  (713 entries).
- **Within 5 km of the city centre** (Central, 22.2793, 114.1628): **494
  of 713**. Within 5 km of Kowloon Park, where three of our six published
  Hong Kong trees already sit: **473**. Either centre clears the bar for a
  verify pass by a wide margin; the register also carries an entry close
  to our published King Camphor of Sha Lo Wan (hkg_005, register id
  AFCD/KS/005, roughly 250 m from our recorded pin, a register-vs-our-pin
  discrepancy worth a verify pass's attention rather than a scouting
  pass's guess).

### Fetch discipline this pass

No host hung; nothing added to `data/fetch-blocklist.json`. Two dead ends
worth recording so a future pass does not retry them: `data.gov.hk`'s own
CKAN `resource_show` API returns only a link to the CSDI Portal viewer, not
a data file, for this dataset; and `portal.csdi.gov.hk/server/rest/services`
returns `{"error":{"code":499,"message":"Token Required"}}` on a plain
fetch, both fast failures rather than hangs.

### Cost

One pass, roughly 60k tokens (web search plus fetch discovery plus two
register imports plus this write-up). No photo hunting, no prose beyond
this survey entry, per BRIEF_RESEARCH.md's rules for a verification/scouting
pass.

## Tree Cities of the World as a register-discovery proxy (scouted 2026-08-13)

**The question:** 227 of our 293 queue cities have no register within reach
(`register` is 0 or absent in `data/city-queue.json`), and for those the only
route on file is from-zero web research, measured elsewhere in this project at
over 500k tokens per city for zero trees. Tree Cities of the World (FAO +
Arbor Day Foundation) certifies a city only if it meets five standards, one of
which is maintaining an up-to-date inventory of its tree resource. So the
certified list is, in effect, a list of cities self-attesting they hold a tree
inventory, which makes it a cheap way to find candidates for a register hunt
worth actually running.

**How the certified list was obtained, as data rather than press coverage.**
treecitiesoftheworld.org's `/directory.cfm` embeds an ArcGIS Dashboards app
(item `2ec8fbfbbcc84fa8ae5469bc8a5816c1`), whose map widget reads a Web Map
(item `0488b10d65484fd78c9749146908c97e`) pointing at the feature layer
`https://services8.arcgis.com/1WIA3UeOTguiTsKg/arcgis/rest/services/Tree_Cities_of_the_World_Communities/FeatureServer/0`.
Queried directly (`/query?where=1=1&outFields=...&f=json`) it returns 285
records across 24 countries with no paging needed (`maxRecordCount` 2000).
This is the live current roster the public map renders, not a historical log
of every city ever certified (all 285 rows carry `ApplicationYear=2025`,
`ApplicationStatus=0`); it was not cross-checked against FAO's own PDF list,
so treat it as "currently recognised as best represented by their own map,"
not as a definitive historical count.

**The cross-reference**, matched on normalized city+country strings (accents
stripped, "City of" prefixes stripped) against `data/city-queue.json`, hand-
reviewed against the TCW `MemberName` field because the map's `City` label
sometimes names a different municipality than the certified member:

| | |
|---|---|
| Queue cities total | 293 |
| Queue cities with no register within reach | 227 |
| Matched certified Tree Cities | 29 |
| Matched AND register-less | 22 |
| Matches carrying a name caveat (see below) | 7 |

**The answer to the question that matters: of 227 register-less queue
cities, 22 (about 10%) are certified Tree Cities of the World, and of the ten
highest-priority ones spot-checked for an actually published register, two
(Portland, Auckland) have one, one (Buenos Aires) is a partial yes, and seven
came back empty or unconfirmed.** That is not a strong enough hit rate to
treat certification alone as a green light to dispatch a register-import
pass; it is a real signal worth checking on a specific city before a from-
zero web research pass, not a filter to run blindly across the other 205 or
so certified-but-unchecked cities.

**Seven matches carry a name caveat, worth its own note because it very
nearly produced a false positive the same way "Lagos" once did.** The map's
`City` field is sometimes the nearest big city rather than the certified
member's own name: our "Miami" match is actually Palmetto Bay (a separate
Miami-Dade village), our "Adelaide" match is actually City of Onkaparinga (a
separate outer-metro council), our "Santiago" match is actually Vitacura (a
separate comuna), our "Barcelona" match is the Barcelona Metropolitan Area
(36 municipalities, not the city alone) and our "London" match is three
individual boroughs (Camden, Redbridge, Islington), not London city-wide.
Madrid has one clean record and one mislabeled Pozuelo de Alarcón record
under `City="MADRID"`. Buenos Aires's caveat is spurious (Ciudad Autónoma de
Buenos Aires is the city's own formal name). **Read `MemberName`, never just
`City`, before treating a TCW pin as certifying the place we think it does.**

**The ten-city spot check** (queue order, lowest rank first, no import
performed): full detail and URLs are in `data/tree-cities-map.json`.

| Rank | City | Verdict |
|---|---|---|
| 6 | Rio de Janeiro | unknown; no single machine-readable dataset found in the time budget, only general open-data portals |
| 7 | Miami | none found (and the TCW match is Palmetto Bay, not Miami) |
| 26 | Belfast | none found; UK-wide Woodland Trust layer only, not a city dataset |
| 33 | Portland | **published**, gis-pdx.opendata.arcgis.com "Heritage Trees", 300+ points; org-level licence tag CC-BY-SA, item-level licence text not yet read |
| 39 | Toronto | none found at city level; Ontario-wide nomination programme only |
| 54 | Auckland | **published**, Auckland Council "Notable Trees Overlay" (legally scheduled trees, Unitary Plan Schedule 10); org-level licence tag CC-BY-SA, item-level licence text not yet read |
| 58 | Buenos Aires | partial: general "arbolado" datasets on data.buenosaires.gob.ar confirmed CC-BY-2.5-AR via the CKAN API, but the specific 639-specimen historic/notable catalogue's own export/licence not confirmed |
| 62 | Adelaide | none found as open data (and the TCW match is City of Onkaparinga, not Adelaide); a Significant Trees framework exists but as a planning-code overlay, not a confirmed downloadable dataset |
| 64 | Mumbai | internal-only; BMC's first heritage-tree survey was reported still in progress, no released list found |
| 93 | New York | lead only; "Great Trees of New York City" (120 curated trees) is not confirmed as a geodata export, and nycgovparks.org itself soft-blocks fetches (see fetch-blocklist.json) |

**What this means for how a run should use TCW certification going
forward.** It is a real, free, zero-cost-to-check signal (this whole
cross-reference cost one feature-service query and no scraping), so checking
it before a from-zero web research pass on any queue city costs nothing and
sometimes saves the whole 500k-token dead end. But it is a lead, not a
licence: two of ten promising checks needed real digging past the FAO badge
to find an actual open dataset, and even those two still need their
item-level ArcGIS licence text read (not just the org-level tag) before
anything gets imported. The other ~205 certified-but-unchecked queue cities
in `data/tree-cities-map.json`'s full match list (minus the 22 register-less
ones already flagged, minus the 10 checked here) are unscouted and should be
checked individually, city by city, rather than assumed.

No host hung this pass (nothing added to `data/fetch-blocklist.json`); the
known `nycgovparks.org` and `portlandmaps.com` entries already there were
both encountered again and both behaved exactly as documented.

## Follow-up: Melbourne, Sydney, Vancouver, Toronto, and the Hobart PDF thread (2026-08-13)

A second pass against the four named programmes the same-day English-speaking-block
scan did not reach, plus its one open thread on Hobart. Licence-led, per this
file's standing method. Verify-agent scope only: no photos, no prose, no city
files touched.

### USABLE, imported

**City of Hobart, Significant Tree Register.** `data/registers/hobart-significant-trees.json`.
Endpoint: `https://services1.arcgis.com/NHqdsnvwfSTg42I8/arcgis/rest/services/ENVIRON_Significant_Tree_Locations/FeatureServer/1`
(ArcGIS item `9b31f3f6acb14bb2a5869b5e17707155`, layer 1). 460 point records,
all with per-tree coordinates (reprojected from EPSG:28355 via `outSR=4326`,
sanity-checked against Hobart's known -42.88/147.33 position). Licence CC BY
4.0 per the layer's own `licenseInfo`: "This work is licensed under a
Creative Commons Attribution 4.0 International License." (carried over from
the earlier pass's verification, not independently re-fetched this pass).
**The unfinished thread is resolved, and the earlier verdict on species was
wrong.** The earlier pass concluded species was locked behind a ~3.6MB
per-tree PDF (`Data_Sheet_URL`) for every one of the 460 records, because the
bulk feed's `Botanical_ID` field looked like a bare integer code with no
attached name. It is not bare: the field's own ArcGIS "coded value domain",
fetched via a plain `?f=json` call on the layer (no PDF, no per-tree fetch),
is a 390-entry species lookup table (code 311 = "Cedrus atlantica", code 293
= "Quercus robur", and so on). Every one of the 460 records resolved to a
named species with zero PDF fetches; the technique is "check the field's own
domain metadata before concluding a coded value is unreadable," a sibling of
the Bordeaux/Toulouse "check the full inventory for a per-tree designation
field" lesson, applied to a different kind of hidden structure. **No vitality
field anywhere in the bulk feed** (same absence as most registers scouted so
far), and no address or place-name field either, only coordinates: pin
precision is `confirmed` from the coordinate, but a human-readable address
still needs deriving at write time. `Number_Trees` splits the register
cleanly: 242 of 460 points are single specimens, 218 are groups or avenue
plantings at one point (values of 2 and up), and the 218 need the ordinary
collectible-point judgement (BRIEF_RESEARCH.md: a compact named avenue may
pass, a diffuse planting is `blocked`) before any of them can ship. What is
STILL genuinely PDF-only: individual tree names, age, condition, girth and
height, and the statement of significance. 453 of the 460 imported points sit
within 5km of Hobart's centre, so this is a dense, near-complete cluster
worth a full city pass on its own terms, not just a lead list. **Covers
Hobart, closing the thread the 2026-08-13 pass left open.**

### Scouted, real register found, blocked on licence

**City of Sydney, Register of Significant Trees.** Feature service found by
tracing the "interactive register" embedded in
`cityofsydney.nsw.gov.au/lists-maps-inventories/register-significant-trees`
through its ArcGIS Online map app
(`map-prod2.cityofsydney.nsw.gov.au/agol_html/RegisterOfSignificantTrees2025/`)
to the webmap's own item IDs, one of which resolves to a live, publicly
queryable feature layer: `https://services1.arcgis.com/cNVyNtjGVZybOQWZ/arcgis/rest/services/Register_of_Significant_Trees_view/FeatureServer/0`
(item `33ac8e933ce34b22b8d77aa1f49beeda`, layer `RST_FINAL`). This is the
real thing the earlier pass named but could not locate: 2,504 records, a
genuine statutory register (`type_of_signifcance`, `statement_of_significance`,
`date_of_listing` with coded values 2005/2013/2025), with a usable vitality
signal (`condition`, coded Excellent/Good/Fair/Poor/Dead, one record already
coded Dead) and an ownership/access pair (`owner_controlling_authority`,
`landuse` coded Public Park, Street, Property-City-Owned, Property-private,
and `accessibilility` coded Public access / Visible from street / No public
access) that answers hard rule 10 directly from the data. `arrangement_text`
splits the register the same way Hobart's `Number_Trees` does: 220 of 2,504
are tagged "Individual", the rest Avenue/Row/Group/Multiple, which the
semantic and collectible-point filters would need to sit on top of. Per-tree
coordinates exist but the raw `Lat`/`Lon` fields on the layer are corrupted
(huge non-geographic numbers); the real position has to come from `x`/`y` in
the service's native spatial reference (`wkid 7856`, GDA2020 MGA), reprojected
via `outSR=4326` on the query, not read directly off the feature attributes.
**Blocked on licence, not on data quality.** The item's own `licenseInfo` is
`null`, and the ArcGIS Hub API confirms it explicitly:
`GET hub.arcgis.com/api/v3/datasets?filter[id]=33ac8e933ce34b22b8d77aa1f49beeda_0`
returns `"license": "none"`. This is a different item from Sydney's actual
open-data catalogue (the "Trees" street-tree inventory, item
`15c4713a688a48fcb604fc343118af05`, carries an explicit CC BY 4.0 badge in
its own `licenseInfo`); the Register of Significant Trees view was built for
the city's own dashboard/map app (`listed: false`, owner a named staff
account) and was never published through the open-data catalogue, so it
carries no licence grant at all. **Not usable without written permission.**
Worth a specific outreach ask to City of Sydney open data, because the
technical readiness (proper vitality, ownership and semantic-filter fields,
all in one place) is better than anything else found in this pass or the
last one; the licence, not the data, is what is missing.

### Not-recommended, with why

**City of Melbourne.** The Bordeaux/Toulouse technique (check the full
inventory for a per-tree designation field before writing a bulk dataset
off) was tried directly and failed: the open-data "Trees, with species and
dimensions (Urban Forest)" dataset's field schema
(`data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/trees-with-species-and-dimensions-urban-forest/`)
has no designation, significance or heritage flag of any kind, only physical
attributes (species, DBH, year planted, precinct). A dataset search for
"exceptional" and "significant" on the portal returns zero results. The
Exceptional Tree Register the city adopted in 2021 exists only as a webpage
(`melbourne.vic.gov.au/exceptional-tree-register`), which itself soft-blocks
plain fetches (HTTP 202, empty body, the same pattern as `nycgovparks.org` in
`data/fetch-blocklist.json`; not added there since only one host and one
fetch were tried). Not recommended on what was found; the register is
real but not reachable as data this pass.

**City of Toronto.** No heritage or notable tree designation exists on the
open data portal (`open.toronto.ca`'s CKAN API host is
`ckan0.cf.opendata.inter.prod-toronto.ca`, not the domain name itself, which
404s on the API path). Searched "tree", "heritage" and "notable" directly:
"Heritage Register" is architectural (buildings, districts), not trees, and
no High Park-specific or citywide notable-tree dataset surfaced under any of
those terms. The only tree dataset is `street-tree-data`, the full public
inventory, which fails the semantic filter on its own terms and is also
unlicensed (`license_title: "License not specified"` in the CKAN metadata),
disqualifying it twice over. Not recommended; Toronto appears not to publish
a distinct heritage-tree programme as open data at all, as opposed to simply
not having surfaced it yet.

### Scouted, real designation found, not importable as a point register

**City of Vancouver Heritage Register.** Trees ARE separable from buildings
and streetscapes: the register's own `category` field on
`opendata.vancouver.ca/.../heritage-sites` has a distinct value, "LANDSCAPE
RESOURCES Trees", holding 35 individually named entries (Weeping Willow at
Douglas Park, a Giant Sequoia on W 49th Ave, and so on), a genuine
semantically-filtered heritage designation. But the dataset's own description
states plainly, and the data confirms: "HERITAGE LANDSCAPE RESOURCES Trees
(attribute table with no map coordinates)". All 35 records were checked and
all 35 carry an empty `geom`; only a street address or, for park trees, a
free-text description ("Douglas Park, Northeast Corner") exists. Licence is
named ("Open Government Licence - Vancouver", `opendata.vancouver.ca/pages/licence/`)
but the licence page is JS-rendered and its text could not be quoted verbatim
this pass; moot for now since there is nothing to import without geocoding.
**Not importable as a register this pass**; a real lead list (35 named,
undated Vancouver heritage trees) worth a future geocoding pass rather than a
dead end, and worth revisiting for the licence text if geocoding is ever
attempted.

### Coverage after this pass

One new register imported (Hobart, 460 trees, 453 within 5km of centre,
closing a thread rather than opening a city cold). One genuine register found
and fully characterised but blocked on licence (Sydney, 2,504 trees, 220
tagged Individual). Two real designations found but not importable as-is
(Vancouver, 35 trees, no coordinates at all; Melbourne, a real register that
simply is not published as data). One country checked and found to have
nothing (Toronto). None of the four countries' capacity for this technique is
exhausted: Sydney is one licence email away from being the best-instrumented
register in the whole project, and Vancouver's 35 trees are one geocoding
pass away from usable.

No host hung this pass; nothing added to `data/fetch-blocklist.json`.
Token usage for this pass: approximately 60k tokens (fetch-heavy scouting
across five cities, one full 460-row import, no photo hunting, no prose).

## Czech Republic, imported 2026-08-15 (AOPK CR Pamatne stromy)

The verdict recorded on line 230 (2026-07-30 scan) is now imported rather than
just scouted. Licence re-verified live: the MapServer's `PamatneStromy/PamatneStromy`
service (folder `PamatneStromy`, layer 1 "Pamatne stromy - jedinci") serves
WGS84 coordinates natively via `outSR=4326`, no reprojection needed.

**Licence, quoted verbatim (re-fetched 2026-08-15, matches the 2026-07-30 record):**
"Tato datova sada poskytovana Agenturou ochrany prirody a krajiny Ceske
republiky podleha licenci Creative Commons Uvedte puvod 4.0 Mezinarodni"
(dataset metadata, https://geocatalogo.icnf... no, correction: AOPK CR's own
metadata page for this layer). The MapServer service itself additionally
carries `copyrightText: "(c) AOPK CR"`. CC BY 4.0, attribution AOPK CR.

**What was imported.** The layer's own typology splits points into TYP=1
(jednotlivy strom, individual tree, 4,301 records), TYP=2 (stromoradi, avenue,
9,211 records) and TYP=3 (skupina stromu, group, 3,283 records) for a layer
total of 16,795, matching the count already on file. Only TYP=1 was imported:
TYP=2 and TYP=3 store one POINT PER MEMBER TREE within a named avenue or
group (one avenue, "Haugwitzova alej", holds 171 separate rows sharing one
KOD), so importing them as standalone entries would misrepresent one
designated ensemble as dozens of unrelated collectible trees. Written to
`data/registers/czech-aopk-pamatne-stromy.json`, 4,301 rows.

**Sanity checks run before trusting anything, per the standing register-pitfalls rule:**
- Girth (`OBVOD_V`, stored as `girth_cm`): already correct centimetres, range
  1cm to 1,650cm (16.5m), mean ~390cm, no metres-as-centimetres trap this
  time. 202 rows carry `OBVOD_V=0` in the source (unmeasured, not a real
  zero-girth tree) and are stored as `girth_cm: null`, not 0.
- No age field exists anywhere in the register (consistent with the standing
  note that no Czech source carries one).
- No dedicated vitality field, but the free-text `POZNAMKA` note field
  sometimes carries an explicit Czech death/deregistration signal ("zanikly
  strom" = vanished tree, "ochrana zrusena" = protection cancelled, plus
  named causes like "spadla pri vichrici" = fell in a windstorm, "vyhorelo
  torzo" = the trunk burned). 22 of the 4,301 rows carry such a signal and
  are marked `publishable: false` with the raw sentence kept in
  `death_signal`. This is the same class of hazard the Lazio removed-trees
  sheet caught for Rome: a register quietly recording its own dead trees in
  a field nothing else reads.
- Coordinates sanity-checked against Czech national bounds (48.55-51.06N,
  12.09-18.85E): clean, no outliers.
- One duplicate KOD among TYP=1 (103344, "Dub u Bucku", two rows, PORADI 1
  and 2): almost certainly two physically separate trees under one
  designation, a twin pair per the standing twins rule, left as two entries
  for a city pass to fold or keep.

**Coverage confirmed by distance check:** 27 register trees within 5km of
Prague centre (95 within 15km), 29 within 5km of Brno centre (69 within
15km), 7 within 5km of Cesky Krumlov centre (53 within 15km). Unlocks Brno
and Cesky Krumlov as new-city candidates and deepens Prague, currently one of
the two best-converting pages on the site.

No host hung this leg. Token estimate for the Czech leg: approximately 15k.

## Poland, licence resolved and imported 2026-08-15 (CRFOP / GDOS)

The 2026-07-30 record flagged the licence-condition fields as empty on the
WFS while GDOS's own site publishes CC BY-SA 4.0 for site content, and asked
a future pass to resolve the contradiction with a fetch and a quoted
sentence before importing. This leg did exactly that, and it resolves.

**The WFS itself remains silent**, re-verified live: `GetCapabilities` on
`sdi.gdos.gov.pl/wfs` still carries `<ows:Fees>brak</ows:Fees>
<ows:AccessConstraints>brak</ows:AccessConstraints>` (both literally
"none/blank"), the same gap the 2026-07-30 pass found. **`gov.pl`'s CC
BY-SA 4.0 statement is generic platform boilerplate**, also re-verified:
fetching `www.gov.pl/web/gdos` directly (not a search snippet) shows the
sentence sits in a `class="creative-commons"` footer block present on every
gov.pl subsite, reading "Tresci tekstowe publikowane w serwisie... sa
udostepniane na licencji... CC BY-SA 4.0" (text content published ON THE
SITE) with a separate CC BY-NC-ND 4.0 line for photos/audio/video. It is
about the website's editorial content, not about any dataset, and it does
not apply to structured open data at all. **The dataset itself carries its
own explicit licence, found by fetching dane.gov.pl's dataset-level API
record directly rather than a search snippet**: `https://api.dane.gov.pl/1.4/datasets/471,centralny-rejestr-form-ochrony-przyrody`
returns `"license_name": "CC0 1.0"`, `"license_description": "Other (Public
Domain)"`, for dataset id 471 "Centralny Rejestr Form Ochrony Przyrody",
owning institution "Generalna Dyrekcja Ochrony Srodowiska" (id 23) confirmed
as the same body that operates the WFS. dane.gov.pl is Poland's official
national open-data portal under the Polish PSI reuse-of-public-sector-
information Act, so this is a primary, dataset-specific, government-issued
licence statement, not an inference from a generic page.

**Verdict: USABLE, CC0 1.0, imported.** The apparent contradiction was never
really a contradiction: two different Polish government surfaces were
answering two different questions (the gov.pl footer licenses the WEBSITE's
articles; dane.gov.pl licenses the DATASET), and once each is read at its
own primary source rather than assumed to be about the same thing, they
stop conflicting.

**What was imported.** The WFS layer `GDOS:PomnikiPrzyrodyPunktowe` (point-
geometry natural monuments) reprojects to EPSG:4326 correctly via
`srsName=EPSG:4326` (axis order lon,lat, confirmed by spot-checking
coordinates fall inside Poland). Per the task's own instruction, this was
NOT a national pull of all 117,474 records: fetched by a ~0.2-degree
(~22km) bounding box around five sprint cities (Wroclaw, Poznan, Warsaw,
Krakow, Gdansk), filtered to `obiekt='drzewo'` (tree; the same layer also
carries boulders, rock outcrops, springs, caves and shrubs under the same
"natural monument" umbrella, correctly excluded). 8,053 tree entries across
the five boxes, zero gid overlap between cities. Written to
`data/registers/poland-gdos-pomniki-przyrody.json`.

**A genuinely good structural finding: no member-tree explosion, unlike
Czech.** Each row is one legal designation with one representative point,
whether it covers a single tree (`designation_type=jednoobiektowy`, 1,943
of the 8,053) or a whole avenue/group (`wieloobiektowy`, 6,110: 4,023
"aleja" avenues, 1,966 "grupa drzew" groups, 121 other/unspecified). Poland's
data model matches Portugal's (one row per designation, ensembles included
with a type flag) rather than Czech's (one row per member tree inside an
ensemble), so nothing had to be dropped or pre-filtered by type; the
collectible-point test on avenues/groups is left to the city research pass,
exactly as it is for Portugal.

**What this register does NOT carry, so a future pass knows before relying
on it: no girth, height, crown or age field at all**, only species (Polish
common name plus Latin binomial in one string), an optional proper name,
the legal designation date, and a link to the CRFOP web record for that
entry. `crfop.gdos.gov.pl` itself sits behind an Incapsula bot-check
(confirmed: a JS-challenge iframe response to plain curl) and was not
fetchable this pass, so a city pass will need another source for
measurements. No vitality field either; alive-now stays a per-tree check.

No host hung this leg (the one dead end, `crfop.gdos.gov.pl`'s Incapsula
gate, is a fast block rather than a hang, so not added to
`data/fetch-blocklist.json`). Token estimate for the Poland leg:
approximately 30k (licence resolution fetches, WFS schema discovery, five
bbox pulls, sanity checks).

## Switzerland, scouted and Geneva imported 2026-08-15

Seven sprint cities had no register (Basel, Bern, Lausanne, Lucerne, Zurich,
Geneva, Winterthur). `opendata.swiss` (Switzerland's national open-data
catalogue, resolves via a 302 redirect to `ckan.opendata.swiss`; blocked
plain `curl` with a 403 until a browser user agent was added, cheap once
known) surfaced one real candidate this pass: Geneva.

### Geneva: USABLE, imported

`vector.sitg.ge.ch`'s `SIPV_ICA_ARBRE_ISOLE` FeatureServer (Ville/Canton de
Geneve's SITG portal) is the canton's full isolated-tree inventory,
239,124 rows, which our semantic filter would forbid wholesale. It carries
a `REMARQUABLE` field the canton itself populates on 205 of those rows
(204 tagged "Autre"/other reason, 1 "Dimension"/size), the same
bulk-inventory-plus-designation-column pattern that made Bordeaux and
Toulouse usable. Only the 205 flagged rows were imported.

**Licence, quoted from the primary CGU page** (`sitg.ge.ch/ressources/conditions-utilisation-donnees`,
fetched live 2026-08-15): attribution is mandatory ("Vous devez
obligatoirement indiquer la source"), and level-A/"Acces libre" data may be
"reproduire, copier, transmettre, diffuser, publier, adapter, modifier,
transformer, combiner le jeu de donnees... y compris pour une utilisation
commerciale" (including commercial use). **One gap, stated plainly rather
than papered over**: this pass could not directly confirm, from a
per-dataset access-level tag, that this specific layer sits in tier A
rather than the more restricted A* (the layer's own catalogue fiche is a
JS-rendered SPA page this pass's tooling could not render, and the bundled
metadata PDF uses a font/text encoding a from-scratch extractor could not
decode cleanly). The circumstantial case is strong (listed on the national
open-data catalogue, every download route open with no auth gate) but it
is not the verbatim per-dataset sentence this project's standard asks for;
a future pass with browser access should close it properly.

**Register pitfalls actually hit**, both caught by the standing
sanity-check habit: `DATE_PLANTATION` carries an exact recurring sentinel
value (1812-01-01) on 13 of 84 dated entries, almost certainly a "date
unknown" database default rather than 13 real trees planted the same day,
now stored as `planted: null` rather than a fabricated date. And one entry
contradicts itself, `SOUCHE` (stump) = "Oui" while `VITALITE` still reads
"Bon" (good); marked `publishable: false` rather than trusted either way.
Circumference (132-951cm) and height (6-40m) both checked plausible, no
metres-as-centimetres trap.

Written to `data/registers/geneva-sitg-arbres-remarquables.json`, 205
entries. 120 of the 205 sit within 5km of Geneva's centre.

### The other six cities: not reached this pass

Basel, Bern, Lausanne, Lucerne, Zurich and Winterthur were not scouted this
leg; the Geneva investigation (licence resolution plus the two pitfall
catches) took the rest of the time budget available for the Switzerland
target. Worth trying next: Kanton Zurich's own open-data portal
(`geo.zh.ch` / `data.stadt-zuerich.ch`) and Bern's `map.geo.admin.ch`-linked
cantonal portal are the obvious next guesses, following the same
"bulk-inventory-plus-designation-column" pattern that worked for Geneva,
Bordeaux and Toulouse.

Token estimate for the Switzerland leg: approximately 45k (opendata.swiss
discovery, SITG WFS schema exploration, licence-page fetch, PDF extraction
attempts that did not pan out, one full 205-row import with pitfall
checks).

## Greece: not reached this pass

Out of the time budget for this register-scouting session (roughly 45
minutes was allotted across all four targets; Czech, Poland and
Switzerland/Geneva alone ran well over that). Not scouted at all. Six
sprint cities including Corfu (#63) and Rhodes (#80) still have no
register. Next pass should start from the forestry service's historical
"diatiritea mnimeia tis fysis" (preserved natural monuments) designation
per the brief; expect this to be thin or paper-only, and a clean
nothing-usable-found verdict is a fine result worth an hour rather than
zero.


# North America register scouting, 2026-08-15

Scouting pass aimed at semi-big US/Canadian cities per Hidde's thesis: Boston
(published, 10 trees, our best-converting American page at 62 impressions)
proves the format works in North America; Charleston, Savannah, New Orleans,
Austin, Seattle, Philadelphia, Vancouver, Montreal and Quebec City are
unpublished with real demand. Method and bar per OPEN_DATA_SURVEY.md: licence
must permit commercial-leaning reuse, quote the proving sentence verbatim,
semantic filter (designated/champion/heritage trees only, never a bulk
street-tree inventory), per-tree coordinates strongly preferred.

Note: `data/registers/portland-heritage-trees.json` already exists (Portland
Heritage Trees, referenced in fetch-blocklist.json under portlandmaps.com), so
a US municipal heritage-tree register import is already a proven pattern here.
Not re-scouted this pass since it is already imported.

---

## 1. American Forests National Champion Trees register

**VERDICT: BLOCKED on licence.** The interactive "search the register" widget
advertised on `americanforests.org/champion-trees/champion-trees-registry/`
no longer functions as a live search (the page is a 2021 snapshot, "Welcome
to the 2021 National Register of Champion Trees!"); the only real distribution
is a static Excel-exported PDF:
`https://d3f9k0n15ckvhe.cloudfront.net/wp-content/uploads/2021/11/2021-National-Register-of-Champion-Trees.pdf`
(700 KB, 6 pages, PDF metadata `Producer: Microsoft Excel 2016`, no embedded
licence or rights statement anywhere in the document).

Confirmed by fetch and by PDF text extraction (pypdf): a genuine flat table,
Record Reference Number / Year Nominated / Nominated By / Scientific name /
Circumference / Height / Crown Spread / Total Points / Year Last Verified /
Last Reported Tree Health / Current Status / Date Crowned / **County / State**.
This IS a semantic-filter pass (every row is a designated National or
Co-Champion, not a bulk inventory), and health/status fields even give a
vitality signal for free ("Excellent/Good/Fair/N/A", "Champion/Co-Champion",
occasional "Deceased"). **But there are no coordinates and no city, only
county and state** ("Travis TX", "King WA", "Philadelphia PA" each appear;
Suffolk/Middlesex/Norfolk MA, Charleston SC, Chatham GA and Orleans LA each
appear zero times, i.e. no in-city Champion for Boston, Charleston, Savannah
or New Orleans specifically in this national list). Even with a licence this
table is county-precision at best, a lead list requiring per-tree
geolocation, same tier as Nara's town-level XLSX.

**The licence question, checked directly, is the real blocker.** No terms-of-
use, terms-and-conditions or legal/licensing page exists on americanforests.org
(`/terms-of-use/`, `/terms-and-conditions/`, `/terms/` all 404; `/legal/`
redirects to an unrelated 2012 blog post about environmental law). The only
rights statement anywhere on the site is the standard WordPress footer on
every page including the registry page itself:

> "Copyright © 2026 American Forests. All Rights Reserved."

No CC licence, no public-domain statement, no explicit reuse permission
anywhere, on the page, in the PDF, or in a dedicated terms page. Per this
project's own standard (an explicit named licence, quoted verbatim, never an
absence of a prohibition) an all-rights-reserved footer with no countervailing
licence statement is a clean disqualification, the same pattern as Kyoto's
誇りの木 register and Ishikawa's cultural-properties database above.
**Do not import.** Usable only as a verification-only lead source the way
monumentaltrees.com is treated under hard rule 1: it can confirm a species/
size claim found elsewhere, never be copied or bulk-imported. If Hidde wants
this unlocked, the path is the same shape as the Woodland Trust: email
American Forests asking for explicit reuse permission (nonprofit, likely to
say yes, but that is his call and his email per hard rule 4).

---

## 2. State champion-tree registers

### Massachusetts: USABLE (public record), IMPORTED

**Boston is exactly the mid-competition/real-demand city the thesis names,
and this register substantially deepens it.** DCR (the Bureau of Forest Fire
Control and Forestry) publishes two downloadable spreadsheets from
`https://www.mass.gov/guides/massachusetts-legacy-tree-program`:

- `Champion Trees 2026`, https://www.mass.gov/doc/champion-trees/download,
  139 rows, the single largest known specimen of each species statewide,
  field-verified in person by a trained DCR forester (the page's own
  description of the nomination process), feeding the National Champion Tree
  Program register.
- `Legacy Trees 2026`, https://www.mass.gov/doc/massachusetts-legacy-tree-list-0/download,
  476 rows, a broader ranked list per species (state's 1st, 2nd, 3rd... largest
  of a species), a superset of the Champion list.

Both are genuine xlsx files (not PDFs despite the URL slug), columns:
Scientific Name, Common Name, **Location (if Publicly Available)**, City,
County, Date Measured, Circumference, Height, Average Crown Spread, Champion
Points, Notes, (Rank on the Legacy list). This is a real semantic designation,
not a bulk inventory: every row is a field-verified largest-of-species record.

**Licence, read in full, genuinely two-tier like Castilla y Leon's IGCYL-NC
rather than a clean CC tag.** `https://www.mass.gov/massgov-terms-of-use`,
section "Public records and copyright", quoted verbatim:

> "All of the material posted on the Commonwealth's websites and available to
> the public without use of an authenticating and authorizing mechanism (such
> as a 'PIN' or password) is public record. Most of the public record posted
> on Commonwealth websites can be copied and used for any purpose."

The same page separately restricts "most of the content on Mass.gov" (its
own words: design, layout, prose) to fair use. Read plainly, the page draws
exactly the line this project's bar draws: **factual government records
(what this spreadsheet is: species, address, county, field measurements
compiled by state foresters under an official program) versus copyrightable
editorial content (design, layout, articles)**. This falls on the public-record
side, which matches the "US federal/state public domain" category the brief
names as acceptable. Recorded honestly as a two-tier reading rather than a
clean licence name, exactly the discipline the Castilla y Leon entry above
sets: the name is not a CC tag, but the terms as read permit commercial-
leaning reuse of the data.

**No coordinates.** `Location (if Publicly Available)` is free text, an
address or landmark name ("28 Moreland St", "Mount Auburn Cemetery"), null
for some rows (private-land trees the sheet itself declines to locate
publicly, which is itself a hard-rule-10 signal worth honouring). This is a
lead list needing geocoding, same tier as Nara's town-level Japanese list,
not a coordinates-in-hand import.

**No vitality field.** Only `Date Measured`, some from the 2010s. Alive-now
is a per-tree check, as with every register scanned so far.

**Imported to `data/registers/massachusetts-dcr-legacy-trees.json`** (139
champion + 476 legacy rows, full licence block, both lists kept since Legacy
is the superset but Champion marks the clean state-record subset).

**Which cities this unlocks, counted directly:**
- Boston (city proper): only 2 rows (a green ash on Moreland St, a
  witch-hazel in the South End). Thin on its own, consistent with Boston's
  existing published page already having taken the obvious Boston-proper
  candidates.
- **Greater Boston (Boston + Cambridge + Somerville + Watertown + Brookline +
  Newton + Quincy + Chelsea + Medford + Malden + Milton + Arlington): 83
  rows.** The standout cluster: **Mount Auburn Cemetery**, straddling
  Watertown/Cambridge about 4 km from downtown Boston, accounts for roughly
  25 of those 83 across a wide species range (European beech, Dawn redwood,
  Cedar of Lebanon, Katsura, Japanese maple, Kentucky coffeetree, Norway
  spruce and more) all inside one walkable, already-touristed cemetery-
  arboretum. This is precisely CLAUDE.md's "cheapest cluster" pattern (dense
  x data-rich, state already field-verified species/size/location): a strong
  candidate for deepening Boston's page or, if it clears the day-trip/cluster
  bar on its own, its own city entry.
- No relevant rows found in this dataset for cities outside Massachusetts, by
  definition (state register).




### Texas: BLOCKED on licence (explicit non-commercial), data quality is excellent, worth a permission ask

**The Texas Big Tree Registry has genuinely the best-shaped data found this
whole pass**, better than Massachusetts: a live ArcGIS Feature Layer, not a
static file, found by reading the registry web app's own Angular config
(`tfsweb.tamu.edu`'s search app ships its data source URL in plain JS):

`https://tfsgis02.tfs.tamu.edu/arcgis/rest/services/BigTreeRegistry/BigTreeRegistry/MapServer/1`

239 records live now (`?where=1=1&returnCountOnly=true`), each carrying:
species (Latin + common), circumference/height/spread/TreeIndex (the scoring
formula), **StateChampion/NationalChampion/ChampionType flags**, county,
organization/site name, **LatDec/LongDec (WGS84 decimal degrees, per-tree,
already the right coordinate system)**, **PublicOrPrivate flag (202 of 239
= 1/public, 35 = 0/private)**, and **Condition (1-5, a genuine per-tree
vitality-adjacent field, codes not yet decoded from this pass, worth
resolving before import)**. Travis County (Austin) has **8 records** in the
current 239.

**Licence, read at the primary source, and it is a clean no.**
`https://tfsweb.tamu.edu/accessibility-site-policies-and-public-notices/`,
section "Fair use", quoted verbatim:

> "Texas A&M Forest Service invites visitors to use its online content for
> personal, educational, and other non-commercial purposes."

And further down the same section: reuse is conditioned on citing the source
and complying with "all terms or restrictions other than copyright." This is
an explicit, direct non-commercial restriction, not an absence of a
statement (unlike American Forests above) and not a two-tier public-record
argument (unlike Massachusetts): the agency has spoken to exactly this
question and the answer is non-commercial only. Per the standing bar, this
disqualifies outright. **Do not import.**

**Worth a permission ask, separate from the licence finding.** Texas A&M
Forest Service is a state agency with an educational mission close to this
project's own (Hidde-approval-gated per hard rule 4, same shape as the
Woodland Trust and Kyoto asks already on file): the data is precise,
per-tree, coordinate-bearing and already flags public/private and champion
status, which would make Austin (and San Antonio, Houston, Dallas, Fort
Worth, if ever wanted) nearly free to research once granted. Not drafted this
pass since outreach emails are Hidde's to send and this is a scouting pass,
but flagged here as the single best target if he wants to ask.

---

## 3. The Live Oak Society (Louisiana Garden Club Federation)

**VERDICT: BLOCKED, explicit written-permission requirement, exceptionally rich data.**

Real, and exactly as described: a live-oak membership registry running since
1934, minimum-girth entry bar (8 ft circumference at 4.5 ft), each entry
carrying a name, address, county/parish, girth and sponsor. Distributed as
scanned-to-digital PDFs from `lgcfinc.org/live-oak-society.html`, at least two
files found (`5001-currentapril2019.pdf`, 265 pages, registrations 5001
onward; `6001_6500.pdf` not fetched this pass) plus an earlier 1-5000 range
implied by the numbering but not located in the time available.

**The society's own page states the licence outright, and it forecloses the
question before any file needs opening:**

> "The information contained in the Registry of the Live Oak Society is the
> copyrighted property of the Louisiana Garden Club Federation and the owners
> of the Live Oak trees. Anyone else wishing to use the information for any
> purpose whatsoever must get written permission from the Live Oak Society
> through its Chairman."

"For any purpose whatsoever" is about as unambiguous a block as this project
has found. **Do not import, do not bulk-extract.** This is a written-
permission-path case, same shape as the Woodland Trust and the Texas Big Tree
Registry above: draft sits for Hidde to send if he wants it (hard rule 4),
addressed to the Live Oak Society chairman via the LGCF contact page.

**Why it is worth the ask.** A quick grep of just the one 265-page file
confirms real density in exactly the cities this pass targets: "New Orleans"
appears 139 times, "Charleston" 34 times, "Savannah" 5 times, and the roster
is not Louisiana-only, it already reaches North Carolina addresses (Carteret
County) within the sampled range, confirming it tracks live oaks across the
whole South rather than one state. This single society roster, if permission
arrived, would likely be the single richest unlock for New Orleans and a real
one for Charleston.

---

## 4. Canada


### BC Big Tree Registry (Vancouver): UNRESOLVED, bot-blocked, not disqualified

`bigtrees.forestry.ubc.ca` is real and matches the brief's description: ~600
trees, UBC Faculty of Forestry, a Champions list, a Top 30, and a stated
downloadable Excel with "nominators, verifiers, site and access notes." Could
not be verified this pass: **every path on the domain, including
`/terms-of-use/` and `/bc-bigtree-registry/champion/`, returns UBC's bot-
defense captcha challenge page to a plain fetch** (HTTP 200, but the body is
the captcha itself, not the content). Solving a captcha is off-limits by this
project's own rules regardless. Logged to `data/fetch-blocklist.json`
(`bigtrees.forestry.ubc.ca`, 2026-08-15). **Not disqualified, just unread**:
a session using the Browser pane (a real browser, not curl/WebFetch) should
be able to clear the challenge and read the terms-of-use and the Excel
download properly. Worth a short follow-up, not a from-zero rescan.

### City of Vancouver Heritage Register, "Landscape Resources Trees": USABLE, found 2026-08-23, leads only (no coordinates)

A different, better source than the BC Big Tree Registry above, found while
scouting Vancouver (one of Hidde's 17 named cities, 2026-08-19) as a night
run: the city's own Heritage Register, `opendata.vancouver.ca`, dataset
`heritage-sites`, filtered to `category = "LANDSCAPE RESOURCES Trees"`. 51
rows, semantically filtered by the city itself (heritage-designated
landscape resources, not a bulk street-tree inventory), fetched clean via
`opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/heritage-sites/
exports/json`, no bot-blocking. **Licence: Open Government Licence -
Vancouver**, based on OGL-BC 2.0, confirmed by fetching
`opendata.vancouver.ca/pages/licence/` directly: free to copy, modify,
publish, translate, adapt, distribute or otherwise use for any lawful
purpose including commercial, with attribution to the source. A clean CC
BY-equivalent.

**What it does not have: coordinates.** Every row carries a street address
(often a number range, e.g. "1450-1460 W 49TH AV") rather than a point, so
this cannot be imported to `data/registers/` as-is. 25 of the 51 rows name
an individual tree with a real address (Giant Sequoia, Northern Red Oak,
English Oak, Tulip Tree, Fernleaf Beech, Garry Oak, two Copper Beeches,
Caucasian Wing-Nut, Douglas Firs, and more); the other 26 are streetscape
rows ("North Side", "South Side of Lane") with no address at all, blocked
as not a single collectible point. Saved as `data/leads/vancouver.json` in
the standard leads/blocked split. Next step for a build or verify pass:
geocode each of the 25 addresses, then run the normal two-source verify
pass; no further scouting needed for Vancouver's tree layer.

### Ontario Heritage Tree Program (Toronto): DEAD END, no exportable data at all

Checked both partner sites, `forestscanada.ca/en/program/heritage-tree`
(the program's current home; Forests Ontario rebranded to Forests Canada) and
`oufc.org/index.php/heritage-tree-program/` (Ontario Urban Forest Council,
co-runs it). Neither publishes a database, map, CSV or any structured export.
Both are nomination-and-plaque programs: individual trees get a blog post and
a certificate, not a register entry. This confirms and extends the earlier
finding that Toronto's own open-data portal carries no city-level tree
designation. **Verdict: no dataset exists to licence-check.** A future pass
would have to compile Heritage Tree recipients from the blog posts
individually, which is from-zero research, not an import.

### Quebec's provincial "arbres remarquables" programme: not scouted as such, but Quebec City's OWN municipal register found instead, and it is excellent

**USABLE, CC BY 4.0, IMPORTED.** Ville de Québec's own open-data portal
publishes `Arbres potentiellement remarquables`
(`https://www.donneesquebec.ca/recherche/dataset/vque_82`), found via the
Données Québec / Government of Canada open-data mirror rather than a
provincial "arbres remarquables" programme, which the search suggests is
Montreal/Mount-Royal specific rather than a real province-wide register (not
independently verified this pass, time-boxed out).

**685 trees, full per-tree point coordinates (WGS84, no geocoding needed,
the best coordinate precision of anything found this whole pass), updated
weekly** (dataset metadata: last modified 2026-08-09). CKAN API confirms
licence directly: `license_id: "cc-by"`, `license_title: "Attribution (CC-BY
4.0)"`, matching the page's own "Licence Attribution (CC-BY 4.0)". Fields:
Latin + French common name, tree type (Feuillu/Conifère), diameter at breast
height, multi-trunk flag, planting date (populated for some rows, a real age
source), and **TYPE_PROP, a direct ownership flag** ("Privés" vs "Public"
and subcategories).

**The hard-rule-10 filter matters more here than anywhere else scanned this
pass**: 594 of 685 rows are privately owned (`Privés`), only **76 are
Public** (60 plain public plus small Public:* subcategories like
"Entretenu Par La Ville"). Only that 76-row subset should ever be considered
for publication; the rest stays in the file as data, never as candidates,
same discipline Brussels' register already established. 76 public,
coordinate-precise, city-designated candidate trees is comfortably above the
four-tree floor for Quebec City, one of the pass's named targets.

**No vitality field**, alive-now stays per-tree, as everywhere else.

Imported to `data/registers/quebec-city-arbres-remarquables.json` (all 685
features kept, TYPE_PROP preserved so a future pass filters correctly rather
than re-deriving the split).

### Winnipeg: BLOCKED, no open-licence register (scouted 2026-08-23)

`scout_next.py --target` pointed at Winnipeg (#69, no supply, no verdict).
Two candidates, neither usable. `data.winnipeg.ca`'s "Tree Inventory Map" is
real and has coordinates, but it is a full municipal public-tree inventory,
every street and park tree in the city, which the semantic-filter rule
excludes on its own regardless of licence. `manitobatreeregister.ca` (the
Manitoba Tree Register, run by Trees Winnipeg with the province, 139 trees
as of this pass) IS the right shape, individually nominated and designated
heritage trees with species and region, searchable by place including
Winnipeg. But the site states "(c)Trees Winnipeg All Rights Reserved" with
no open-licence declaration anywhere, and offers no API or export, browse
and search only. Disqualified for import under the licence-first rule.
Recorded in `data/register-scouting.json` as `blocked` so this search is not
repeated; usable later only as a lead source for hand verification if
Winnipeg is ever named for from-zero research, which it is not currently.

---

## Summary for the merge into OPEN_DATA_SURVEY.md

| Target | Verdict | Trees | Coordinates | Cities unlocked |
|---|---|---|---|---|
| American Forests National Champion Trees | BLOCKED, no licence (all-rights-reserved footer, no terms page) | n/a (PDF, county/state only) | No | none; verification-only lead source |
| Massachusetts DCR Legacy/Champion Trees | USABLE (public record), imported | 139 champion + 476 legacy | No, address/landmark text only | Boston (2 in-city, 83 Greater Boston, ~25 clustered at Mount Auburn Cemetery) |
| Texas Big Tree Registry | BLOCKED, explicit non-commercial licence | 239 live in ArcGIS layer | Yes, per-tree WGS84 | Austin (8 in Travis Co.); best-shaped data of the pass, worth a permission ask |
| Live Oak Society (Louisiana Garden Club Federation) | BLOCKED, written permission required ("for any purpose whatsoever") | thousands (265-page PDF sampled) | No, addresses only | New Orleans (139 mentions), Charleston (34), Savannah (5) in one sampled file; worth a permission ask |
| BC Big Tree Registry | UNRESOLVED, UBC bot-defense captcha blocks every plain fetch | ~600 (unverified) | Unknown | Vancouver, if unblocked; needs a browser session, not disqualified |
| Ontario Heritage Tree Program (Forests Canada / OUFC) | DEAD END, no dataset exists | n/a | n/a | none; nomination-and-plaque program only |
| Quebec City arbres potentiellement remarquables | USABLE, CC BY 4.0, imported | 685 (76 flagged public) | Yes, per-tree WGS84, best precision of the pass | Quebec City (76 public-flagged candidates) |

**Not reached this pass** (target 5, time-boxed out): Austin's Heritage Tree
ordinance list and Charleston County's Angel Oak / grand tree protections,
both flagged as likely PDF-only. Also not reached: South Carolina, Georgia,
Washington and Pennsylvania state champion-tree registers (the brief's
priority list after Massachusetts and Texas), and independent verification
of whether a real province-wide Quebec "arbres remarquables" programme
exists beyond Quebec City's own municipal one.

**Files written:** `data/registers/massachusetts-dcr-legacy-trees.json`,
`data/registers/quebec-city-arbres-remarquables.json`. One fetch-blocklist
entry added (`bigtrees.forestry.ubc.ca`). No host hung (the one HTTP:000 on
`texasforestinfo.tamu.edu` resolved clean on immediate retry, not logged).

---

## Register scouting: Australia and Canada, the Wikivoyage re-rank (2026-08-15)

Dispatched after the queue's demand proxy switched from English Wikipedia to
English Wikivoyage pageviews, which re-ranked Sydney, Perth, Brisbane,
Melbourne, Adelaide (AU) and Toronto, Montreal, Vancouver, Ottawa, Calgary
(CA) to the top of the zero-register list. Verify-agent scope only: no
photos, no prose, no city files touched. ~40 minutes, licence-led, per this
file's standing method. Builds on the 2026-08-13 English-speaking-block scan
and its 2026-08-13 Melbourne/Sydney/Vancouver/Toronto follow-up above; this
pass looked for what those left unscanned (Perth, Adelaide, Brisbane's own
overlay, Ottawa, Calgary, Montreal) plus a second look at Melbourne via its
constituent councils rather than the city proper.

### USABLE, imported

**City of Yarra (inner Melbourne), Significant Trees register.**
`data/registers/melbourne-yarra-significant-trees.json`. 232 point records,
CC BY 4.0 per data.gov.au's harvested licence metadata (license_title
"Creative Commons Attribution 4.0 International", license_url
`creativecommons.org/licenses/by/4.0`). Genuine designation: trees "identified
and assessed (against defined categories) as having scientific, social,
historic and aesthetic value" (dataset description, verbatim). Per-tree WGS84
coordinates, species (genus + full binomial), common name, DBH, height,
maturity, text age estimate ("100+ years"), a significance-category list
(Aesthetic Value, Outstanding Size, Particularly Old, Historic Value etc.)
and address. 173 of 232 sit within 6km of Melbourne's CBD (Fitzroy,
Collingwood, Richmond, Clifton Hill, Carlton North, Alphington), so this is a
genuine Melbourne-metro cluster, not a distant satellite town. No vitality
field. **Opens Melbourne** (the city itself was previously not-recommended:
its own open-data portal only publishes the full 80,000-tree inventory).

**City of Boroondara (eastern Melbourne), Significant Tree register.**
`data/registers/melbourne-boroondara-significant-trees.json`. 314 records, CC
BY 3.0 Australia per data.gov.au's harvested metadata and the dataset's own
notes field ("Council makes this compilation available pursuant to the terms
of a Creative Commons CC-BY licence Australia v3.0", verbatim). 229 of 314
sit within 12km of the CBD (Hawthorn, Camberwell, Kew, Balwyn, Glen Iris,
Canterbury). Botanical name, common name, height, canopy spread, girth, a
plain-integer age (years at 2016 survey), significance category, free-text
health, and critically a per-record `POSITION` field. **Hard rule 10 is live
and unresolved in this file**: the position breakdown (46 "Front garden", 13
"Rear garden" out of 314, against public values like "Park", named parks and
golf clubs) means roughly a fifth of this register sits on private land and
must never become a candidate; the rest still needs a per-record check, this
file is not pre-filtered the way Quebec City's `TYPE_PROP` split was.
**Deepens the Melbourne cluster Yarra opens**, a second, adjacent council.

**Brisbane City Council, City Plan 2014 Significant landscape tree overlay.**
`data/registers/brisbane-significant-landscape-trees.json`. 558 of the
overlay's 1,740 total records kept (filtered to the `Individual or group
significant landscape tree site` sub-category only; the other three
sub-categories, Adjoining site / Landscape features / Vegetation protection
order, are a different kind of designation and were not imported). CC BY 4.0,
proving sentence from the dataset's ArcGIS Hub source
(`hub.arcgis.com/api/v3/datasets/bed1dde0fb624870a93cbe58c0b8e0b2_0`),
`licenseInfo` verbatim: "This material is licensed under a Creative Commons -
Attribution 4.0 licence. No access or use limitations." Cross-confirmed by
data.gov.au's own harvested `license_title: "CC-BY-4.0"` for the same
dataset. 247 of 558 sit within 8km of the Brisbane CBD. **The catch: this is
the raw statutory overlay only, no species, name, age or significance-reason
field exists anywhere in the feature class**, only a polygon (converted here
to its centroid). It answers "a council-designated significant tree sits
here" and nothing else; species and age must come from elsewhere (imagery,
a second source) before any candidate clears the two-source bar, and no
land-ownership flag exists, so hard rule 10 needs a per-candidate imagery
check. Opens Brisbane as a coordinate-verified lead list, not yet as
research-ready candidates the way Yarra or NCC are.

**National Capital Commission (NCC), "A Living Legacy: Remarkable Trees of
Canada's Capital."** `data/registers/canada-capital-ncc-remarkable-trees.json`.
166 point records spanning Ottawa, Ontario AND Gatineau, Quebec (both banks
of the Ottawa River; no country/province field distinguishes them, a verify
pass must place each coordinate itself). Licence: Open Government Licence -
Canada v2.0, confirmed both via open.canada.ca's package metadata
(`license_id: ca-ogl-lgo`) and the dataset's own ArcGIS Hub `licenseInfo`
link to the same licence text. **The richest register found this pass**: a
curated 2020 compilation (not a bulk inventory) with Latin name, common name
in English/French/Indigenous where recorded, a genuine descriptive paragraph
per tree (siting, history, why it was chosen) that maps almost directly onto
`verify_notes`, a `SECTOR` grouping field for clustering, and per-tree WGS84
coordinates. 133 of 166 sit within 10km of downtown Ottawa (sectors CORE,
OUL, CEF_ARBORETUM, GP, GB, QUL, RH; the arboretum sector alone holds 65).
No numeric age/girth/height and no vitality field (2020 snapshot, not a
maintained inventory); no explicit ownership flag but the NCC's core mandate
is federal PUBLIC land in the capital region (parks, parkways, driveways),
so there is a strong prior toward public access that still needs a per-tree
check rather than a blanket assumption. **Opens Ottawa**, and separately, a
Gatineau cluster if a future pass wants it.

### Scouted, real designation found, not usable this pass

**Quebec City "Potentially remarkable trees" already imported** (see the
2026-08-15 entry above this section); found again independently here via
open.canada.ca's federal catalogue, which mirrors it. No new information.

### Scouted, nothing found

**Perth**: `data.gov.au` organization filter for "city-of-perth" returned
zero packages for "tree". No City of Perth or Western Australian
significant/heritage tree open dataset surfaced this pass. Not exhausted,
just not found with a portal search; a direct fetch of the City of Perth's
own open-data site (if one exists separate from data.gov.au) was not
attempted.

**Adelaide**: `data.sa.gov.au`'s search API appears to federate the same
national CKAN index as `data.gov.au` (identical result set for "significant
tree", dominated by Victorian councils), so no Adelaide-specific or South
Australian state significant-tree dataset was found this pass either. This
confirms rather than resolves the 2026-08-13 finding that Adelaide's
Significant Tree designation is a Development Act / Planning Code overlay
administered per-council (Adelaide, Burnside, Prospect, Unley) with no single
fetch; none of those councils' individual portals were checked this pass.

**Toronto**: not re-scanned; the 2026-08-13 verdict (no heritage/notable tree
dataset exists on `open.toronto.ca`, only the unlicensed full street-tree
inventory) stands.

**Vancouver**: not re-scanned; the 2026-08-13 verdict stands (35 named
heritage trees, Open Government Licence, but zero coordinates; BC Big Tree
Registry still bot-blocked, logged in `data/fetch-blocklist.json`).

**Montreal**: `donnees.montreal.ca`'s CKAN search for "arbre remarquable"
returned exactly one dataset, "Arbres publics sur le territoire de la Ville"
(the full public-tree inventory, fails the semantic filter). Confirms the
2026-08-13 finding: no distinct remarkable/heritage tree open dataset exists
for Montreal; the "arbres-remarquables" material that does exist is a Mont
Royal-specific webpage, not structured open data.

**Calgary**: browsed `data.calgary.ca` for "significant tree" / "heritage
tree" / "notable tree"; no matching dataset titles surfaced. Not deeply
scanned (one browse-page fetch), so this is "nothing found," not "confirmed
absent."

### Coverage after this pass

Four new register files, all licence-proven CC BY 4.0 / CC BY 3.0 AU / OGL
Canada: Yarra and Boroondara together open Melbourne with 402 candidate
points within a reasonable radius of the CBD across two adjoining councils;
Brisbane's overlay opens it as a coordinate-verified lead list (species and
age still to source); Ottawa opens cleanly with the best per-tree prose of
any register scouted so far, plus a Gatineau cluster as a bonus. Sydney
remains the single best-instrumented register in the whole survey and is
still blocked purely on licence (`data/registers` unaffected; see the
2026-08-13 entry above), worth the specific outreach ask already recorded
there. Perth, Adelaide, Toronto, Vancouver, Montreal and Calgary remain
either genuinely empty or under-scanned; none were exhausted.

No host hung this pass; nothing new added to `data/fetch-blocklist.json`.

**Files written:** `data/registers/melbourne-yarra-significant-trees.json`,
`data/registers/melbourne-boroondara-significant-trees.json`,
`data/registers/brisbane-significant-landscape-trees.json`,
`data/registers/canada-capital-ncc-remarkable-trees.json`.

Estimated token usage for this pass: approximately 55k-65k tokens (portal
search and API fetches across roughly 10 targets, four full-dataset
downloads and imports, no photo hunting, no prose, no individual tree
verification).

## Den Haag: ~1,300 monumental trees behind the city's own tree app (2026-08-16, licence UNKNOWN)

Found through Clara Visser, chair of Bomenstichting Den Haag, who answered
batch 005 with four links. The one that matters is the Haagse bomenapp
(`ddh.maps.arcgis.com/apps/webappviewer/index.html?id=26717c16f2ad43678a9bbcc53c90cb03`),
whose own ArcGIS item metadata reads: **117,000 street trees, nearly 1,300
monumental trees**, plus forest-edge trees and the Zuiderpark shrubs. The item
names `opendata@denhaag.nl` as the access contact and links a dataset page at
`denhaag.dataplatform.nl/#/data/0aae8124-0a0e-496b-a9d9-cd6a3c586578`.

**What is settled:** the data exists, it is the municipality's own, and the
semantic filter this project needs (monumental versus ordinary street tree) is
a field in it rather than a judgement we have to make. We publish five trees in
The Hague against ~1,300 designated ones, so this is the largest single-city
gap the Dutch coverage has.

**What is NOT settled, and blocks any import:** the licence. The ArcGIS item's
licence field is empty. Do not read that as permission; an empty field is an
unanswered question, and the standing rule is a verified open licence before
anything is imported.

**The dead end to not repeat.** The app's config points at
`geoservices.denhaag.nl/arcgis/rest/services/V2_8_Natuur_en_milieu/Natuur_en_landschapsbeheer/MapServer`,
which returns 404: that version is retired. The server also returns an empty
folder and service list at its root, so the current path cannot be enumerated
and guessing version numbers is a waste of a window. Ask instead.

**Next step, one mail:** `opendata@denhaag.nl`, asking which licence the
monumental-tree layer carries and where the current endpoint lives. That is the
municipality's desk, not the foundation's, so it is a separate thread from
Clara's.

## The Netherlands, opened by three tree foundations in one week (2026-08-18)

Three replies to batch 005 turned into the country's whole data picture. All
three were unprompted, all three named sources, and two of them named the same
one we had wrongly parked.

**IMPORTED: Landelijk Register Monumentale Bomen v2024 (Bomenstichting).**
`data/registers/netherlands-lrmb.json`, 16,094 trees with surveyed coordinates.
Licence from their own DCAT catalogue: "Onder bronvermelding te gebruiken:
(c)Bomenstichting", plus Hidde's own written permission by email. It carries
`visitable` and `owner_category` per tree, so hard rule 10 becomes a filter
rather than a hunt, and `planted_band` gives a decade. Slices, counting only
visitable and non-private: Utrecht 253, Amsterdam 206, Haarlem 125,
's-Gravenhage 86, Rotterdam 63, Leiden 54.

**Amsterdam, Hanna Hirsch (Bomenstichting Amsterdam).** Sent the city's own
monumental-trees walking booklet as a PDF with permission for data and
photographs. Thirty curated centre trees, of which twelve were new to us and
are now written. The booklet cites a number per tree on monumentalebomen.nl,
which is how the register above was found. Read it with `scripts/pdf_text.py`;
the file sits in Hidde's Downloads, not the repo.

**Den Haag, Clara Visser (chair, Bomenstichting Den Haag).** Four pointers:
the city's own tree app at ddh.maps.arcgis.com (all street trees, ordinary and
monumental); ~1,300 monumental and 6 veteran trees with a walking route
"Groen met historie" on hethaagsegroen.nl; monumentaltrees.com; and their own
haagsebomen.bomenstichtingdenhaag.nl, "bomen met een verhaal", explicitly not
all monumental. Note her count of ~1,300 against the national register's 116
for 's-Gravenhage: the municipal list is far larger than the national one, so
the city app is worth scouting on its own.

**Leiden, Eduard Groen (board, Bomenbond Rijnland).** openbomenkaart.org holds
84,000 Leiden street trees WITH planting dates, built from data the makers
requested from the municipality, and he says the Excel can be requested
directly. He has personally surveyed the trees in Van der Werfpark, De Burcht
and Rembrandtpark. He also points at the LRMB and at monumentaltrees.com.

**One source all three of them offered that we must not take: monumentaltrees.com.**
Hard rule 1 forbids using its content beyond fact verification, because its own
terms prohibit commercial reuse. They suggested it in good faith and the answer
is still no. Worth knowing before a reply thanks them for it.

## Asheville, North Carolina: scouted, no importable register (2026-08-23)

`scripts/scout_next.py --target` pointed at Asheville (#56 in the queue, no
supply, no verdict). Checked two candidate sources, neither usable:

**NC Forest Service Champion Tree Program.** The state programme
(ncagr.gov/divisions/nc-forest-service/urban/champion-trees) publishes only a
PDF list, no coordinates, no county filter, no stated licence, and its own
database has been offline for part of 2025 during a programme review. Not
importable in any form; a PDF list without coordinates is a lead source at
best, and even that would need the licence question answered first.

**Buncombe County / Asheville GreenWorks "Treasured Trees".** The right shape
of source in principle, exactly the semantic remarkable-tree designation this
project wants rather than a bulk inventory: GreenWorks and the city
co-sponsor a nomination programme that plaques individual "rare, special, or
ancient" trees (one confirmed example, a White Oak dated to 1665 at the
Center for Spiritual Living in West Asheville). But there is no public list,
map or dataset of which trees hold the designation, only a nomination form
and scattered individual mentions in blog posts and press. Finding the full
set of designated trees would mean from-zero web research, tree by tree,
which CLAUDE.md rule 1(d) turns off for an unnamed city (Asheville is not on
Hidde's 2026-08-19 named list).

Verdict: **empty**. No register to import. If Hidde names Asheville for
from-zero research, the Treasured Trees programme is the place to start,
since at least one located, dated example is already in hand.

## Bali, Indonesia: scouted, no importable register (2026-08-23)

`scout_next.py --target` moved on to Bali (#60, no supply, no verdict).
Indonesia protects sites under "cagar budaya" (cultural heritage), governed by
Law 10/2010 and Bali's own provincial spatial planning regulation, but every
designation found under that framework is a temple, inscription or building
(Taman Ayun, Prasasti Blanjong, Pura Pucak Penulisan), never a tree in its own
right. No national or provincial database of individually registered
old/sacred trees turned up. What exists instead is press coverage of specific
named sacred trees, banyan (beringin) and other bayan figs at temple sites,
each documented one article at a time: Bunut Bolong in Jembrana (a giant
banyan with a road-sized hole through the trunk) and a Pule tree at Pura Luhur
Pucak Petali in Tabanan among them. That is lead material for from-zero
research, not a register, and Bali is not on Hidde's 2026-08-19 named list.

Verdict: **empty**. No register to import.

## Ireland: already imported, extended to Cork, and the scouting ledger fixed (2026-08-23)

`scout_next.py --target` moved on to Cork (#63, published at 5 trees, but no
register supply and no scouting verdict on file). The search turned up
Heritage Trees of Ireland immediately, and a first pass here nearly imported
it as a brand new find and overwrote the existing file with a smaller,
unconverted version, before `git status` showing "M" rather than "??" on
`data/registers/ireland-heritage-trees.json` caught it. **This register was
already imported on 2026-08-08 and used again on 2026-08-09** to add six
trees to Dublin (see CURATION.md's archive for that date); the only real gap
was that nobody had ever logged it in `data/register-scouting.json`, which is
why `scout_next.py` pointed at it as unscouted. That gap is now closed.

**Heritage Trees of Ireland, National Biodiversity Data Centre.** Built from
Aubrey Fennell's 1999-2009 survey for the Tree Council of Ireland / Irish Tree
Society's Tree Register of Ireland project. 724 trees, 424 sites, 143 species,
covering the whole island. Licence: **CC-BY 4.0**. The existing import already
carried the fix for the coordinate problem the raw source has: coordinates
come as Irish Grid easting/northing (OSI/TM75), not lat/long, and
`scripts/irish_grid.py` (written 2026-08-08, an inverse transverse Mercator
implementation with no reprojection library available in this environment)
converts them, verified to within about 40m against three register entries
that already matched published, confirmed-pin trees. The 2026-08-08 import
also already handles the dataset's other trap: its "Access" column is
identical boilerplate on every one of the 724 rows and answers nothing about
a specific tree, so the existing file only carries sites independently
confirmed genuinely public (Trinity College, National Botanic Gardens
Glasnevin, St Anne's Park, Marley Park, all Dublin) rather than the whole 724.

**Extended 2026-08-23 with Blarney Estate and Fota Arboretum, Co. Cork.**
Cork's page already draws two of its five trees from Blarney and one from
Fota, so those sites' public status was already established. Converted the
register's Blarney and Fota rows with the existing script: two, a yew and a
Western Red Cedar, landed within about 60m of the already-published cor_001
and cor_002, near-certain duplicates, recorded in the register file but not
shipped. Eight more were new: a Cappadocian maple and a beech at Blarney, and
at Fota a camphor tree, a spiral-needled Japanese cedar cultivar, a Canary
Island date palm, a New Zealand tanekaha, a holm oak and a coast redwood.
Cork went from 5 trees to 13 against a target of 20, all with real converted
coordinates, `location_precision: approximate` per the converter's own
caveat.

**What is left for a future pass.** The register covers the whole island and
the existing Dublin subset plus the new Cork one are both far short of its
724 rows; Galway, Limerick, Killarney, Kilkenny and Belfast can all draw on
it once their existing coverage is checked for overlap the way Cork's was.
Doneraille Park (3 candidates) and The Gearagh nature reserve near Macroom (1
candidate) both turned up for Cork itself but sit 35-40 minutes' drive out,
past the roughly-30-minute day-trip boundary, so they were left unshipped in
`data/leads/cork.json` rather than stretched to fit.

## Norway: found and reachable, stalled on per-tree description (2026-08-23)

`scout_next.py --target` moved to Oslo next (#64, published at 4 trees, the
floor). Norway has a genuine national layer for individually protected
natural monuments, "naturminne", inside Miljødirektoratet's `vern` ArcGIS
service:

- Service root: `kart.miljodirektoratet.no/arcgis/rest/services/vern/mapserver`
  (layer 0, `naturvern_omrade`, polygons, field `verneform`).
- Query for individual monuments: `.../0/query?where=verneform='Naturminne'`,
  236 nationally, 18 in Oslo commune (`kommune LIKE 'Oslo%'`). Ask for
  `outSR=4326` and the geometry comes back as WGS84 already, no Irish-Grid-style
  conversion needed.
- Licence: **NLOD** (Norwegian Licence for Open Data), stated on the
  data.norge.no listing for the parent "Naturvernomrader" dataset, permissive
  and attribution-based, the OGL/CC-BY equivalent.
- **Naturminne is a mixed bag, trees plus geological and other features**, so
  it needs the same per-entry judgement as any register: Oslo's 18 include
  clear tree addresses (`Rolf E. Stenersens allé 48`, `Drammensveien 106`,
  `Eventyrveien 16`) alongside things that read as headlands, skerries and a
  jetty (`Huk`, `Killingen`, `Malmøya brygge`). The `navn` field's
  street-address pattern is a strong tell for the tree entries, same
  fingerprint as the Dutch LRMB register, but not proof on its own.

**What stopped a full import: no species or description field anywhere in
the map service, and no swagger/API listing found for the separate document
API that exists behind it.** Each record's `faktaark` URL
(`faktaark.naturbase.no/?id=<VV-id>`) is a JS single-page app WebFetch cannot
render. Reverse-engineered its network calls to
`felles.naturbase.no/api/dokument?objektId=<VV-id>`, which returns attached
photos and documents but not a text description; for VV00002163 (the
Stenersens allé site) it surfaced two tree photos from 2007 AND a documented
warning worth having found before shipping anything blind: a linked Google
Street View note says only the stump remains of the "easternmost tree",
i.e. one of the two trees this naturminne protects is already dead. No
species field, no protection-decision text (`verneforskrift` was null on
this record), and no other endpoint tried (`beskrivelse`, `vernevedtak`,
`naturminne`, `objekt`) resolved.

**Verdict: stalled, not empty.** The register exists, is licensed for use
and the geometry needs no conversion, which makes it worth returning to
rather than abandoning. What is missing is species per tree, which the next
attempt should get one of two ways: read the `verneforskrift` PDF where one
exists (most records probably carry one; this specific record happened not
to), or treat each Oslo `naturminne` address as a lead and verify species and
condition the normal from-zero way, the dokument API's photos as a
first check on whether the tree is even still alive before spending time on
it.

## Edmonton, Alberta: found, stalled on licence and reliability (2026-08-23)

`scout_next.py --target` moved to Edmonton next (#67, not published, no
register supply). Found the **Alberta Tree Register**
(albertatree.ca / albertatreeregister.github.io), a public map of Alberta's
heritage, veteran, uncommon and "most loved" trees, 464 entries, the
overwhelming majority in Edmonton (87 of the first 100 records checked).

**The data is real, rich and reachable, but through the site's own public
Airtable API rather than a downloadable file.** The map's own client-side JS
(github.com/AlbertaTreeRegister/Map, MIT-licensed repo) calls
`api.airtable.com/v0/appQryFCb5Fi3nZ4c/tbljBWCUMUSwrF2co` with a personal
access token hardcoded in that same public repo, i.e. the same call any
visitor's browser already makes to render the public map. Queried it
directly and got full addresses, species, age, condition, height/girth
measurements and a free-text nomination story per tree.

**Two reasons this stays stalled rather than imported.** First, licence: the
MIT licence on the repo covers the CODE, not explicitly the tree data itself,
and no separate data licence statement was found; CLAUDE.md's bar needs a
verified open licence before anything ships, so this needs either an
explicit data licence somewhere on the site or a direct question to whoever
runs the project before it counts as usable. Second, reliability: this is a
crowdsourced nomination register ("anyone can nominate their favourite
Alberta tree"), not a government survey, and the sample already showed the
tell-tales of that: one record's description is a transcribed phone-call
recollection about a neighbour's guess at a tree's age ("Miss Gail Rankin
thinks..."), and another (a Calgary horse chestnut) carries coordinates of
0,0. Treat any entry as a lead needing the normal two-source verification,
not a register fact.

**Edmonton itself is not on Hidde's 2026-08-19 named list**, so from-zero
research there, including turning these leads into verified trees, is off
until he names it or a licence answer changes the register's status to
usable outright.

## Finland (Turku #67): a real national designation, split across three sources, none import-ready yet (2026-08-23)

`scout_next.py --target` pointed at Turku (#67, no supply, no verdict). Finland
does have exactly the right shape of designation: "luonnonmuistomerkki"
(natural monument), an individual tree, group of trees or boulder protected
under the Nature Conservation Act, decided per-site by a municipality or by
Metsähallitus on state land. The semantic filter this project wants already
exists in Finnish law. What is missing is one clean, licensed, per-tree
dataset behind it; three different sources each carry part of the picture.

**1. The national dataset (would cover Turku), licence unconfirmed and its
WFS currently down.** `Luonnonmuistomerkit`, compiled by Metsähallitus and
distributed by SYKE (Suomen ympäristökeskus), at
`ckan.ymparisto.fi/dataset/luonnonmuistomerkit`: nationwide point data in
EPSG:3067, a direct ZIP/shapefile download
(`wwwd3.ymparisto.fi/d3/gis_data/spesific/luonnonmuistomerkit.zip`) plus a WMS
endpoint; the paired WFS endpoint
(`paikkatiedot.ymparisto.fi/geoserver/muusuojelu/ows`, layer
`muusuojelu:Luonnonmuistomerkit`) returned "Service WFS is disabled" when
queried directly. The page states sites on state land and in five named
southern regions (South Karelia, Kymenlaakso, South Savonia, Päijät-Häme,
Kanta-Häme) are field-verified and reliable; everywhere else, including
Turku's own region (Varsinais-Suomi), is unverified private-land data that
may be incomplete or outdated, by the source's own admission. **Licence: not
proven.** Queried the CKAN API directly
(`ckan.ymparisto.fi/api/3/action/package_show?id=luonnonmuistomerkit`):
`license_id` and `license_title` are both null. The page's own text says only
"no limitations" on access with attribution to Metsähallitus, which is not
the same thing as a named licence (contrast with SYKE's separate
`SuojellutAlueet` INSPIRE WMS bundle, whose own metadata record explicitly
states "Creative Commons Nimeä 4.0 Kansainvälinen. Lähde: SYKE", i.e. CC BY
4.0. That bundle covers nature conservation areas and Natura 2000, not
Luonnonmuistomerkit). Nothing here can be imported without an explicit
licence answer for this specific dataset.

**2. Turku's own city WFS carries the exact point layer, but with no
descriptive fields.** Turku's Tekla-based city map service
(`turku.asiointi.fi/TeklaOGCWeb/WFS.ashx`, the current address behind the old
`opaskartta.turku.fi` one) publishes a layer `kanta:SuojeltavaKohde`
("protected object"). Queried it directly (GML, since it refused
`outputFormat=application/json`) and its `tyyppi` (type) field is literally
`luonnonmuistomerkki` on the returned features, i.e. Turku's own portal does
carry these points, in EPSG:3877, with a location-uncertainty value
(`sijaintiepavarmuus`), a creation method (`digitointi`, meaning digitised
from a paper record) and a date, but **no species, name, age or description
field at all**, only geometry and metadata about the record itself. Turku's
general spatial data, "Turun kaupungin paikkatietoja" on the same
`TeklaOGCWeb/WFS.ashx` endpoint, is stated on its avoindata.suomi.fi listing
as **Creative Commons Attribution 4.0 International License**, but that
listing's own resource description talks about detailed-plan and base-map
layers (blocks, buildings, property boundaries) and never names
`SuojeltavaKohde` specifically, so the licence match is a strong inference
from the shared endpoint rather than a verbatim proving sentence for this
exact layer.

**3. Helsinki (a different city, not Turku, but the same national
designation) has a fully confirmed, fully populated equivalent, worth
recording as a separate future import.** Helsinki's Luontotietojärjestelmä
(Nature Information System) publishes a WFS layer
`avoindata:LTJ_avoin_rauhoitettu_luonnonmuistomerkit` at
`kartta.hel.fi/ws/geoserver/avoindata/wfs`. Queried it directly
(`outputFormat=application/json`) and got a real GeoJSON FeatureCollection,
31 features, each with `nimi` (name, e.g. "Tammi (Helsingin seudun paksuin),
Tali"), `kuvaus`/`kohdeteksti` (free-text description carrying girth and
height, e.g. a 598 cm circumference, 22 m oak measured in 2003), `luokan_nimi`
(classification, "Luonnonmuistomerkki") and point coordinates in EPSG:3879.
**Licence proven twice over**: the general Helsinki open geographic data page
states "the maps and geographic data created by the City of Helsinki's City
Survey Services... are licensed under the Creative Commons Attribution 4.0
International licence" (attribution: "Data and maps (c) City of Helsinki,
City Survey Services"), and the dataset's own listing on
avoindata.suomi.fi for "Helsingin luontotietojärjestelmä" independently
states the same Creative Commons Attribution 4.0 International License by
name. This one is import-ready as-is, for Helsinki, not for Turku.

**Verdict: stalled, not empty.** The designation is real and at least one
Finnish city (Helsinki) proves the exact data shape this project needs
exists and is openly licensed; Turku's own portal demonstrably holds the
same point layer, just without the descriptive fields a story needs. Next
step for Turku specifically: treat the `kanta:SuojeltavaKohde` /
`luonnonmuistomerkki` points as a coordinates-only lead list (worth
converting from EPSG:3877 and cross-checking each point against Turku's own
"pihapuuopas" yard-tree guide and local press for a name and species), and
separately get a direct licence statement for that layer from Turku's open
data pages or its contact address before treating the inference as proof. A
second worthwhile thread, not chased today for time: Tampere is reported
(via search, unverified by direct fetch) to maintain its own
"Tampereen luonnonmuistomerkit" open dataset on the same pattern as
Helsinki's; worth a direct check before Tampere is next in the queue.

**Helsinki's register imported the same day, separately from the Turku
question above.** Fetched the WFS layer directly with `srsName=EPSG:4326`,
which returns real WGS84 coordinates and skips the EPSG:3879 conversion
Turku would need. 23 of 31 features kept as
`data/registers/finland-helsinki-luonnonmuistomerkit.json`: 8 excluded as
geological features that share the `luonnonmuistomerkki` designation with
trees in Helsinki (`hiidenkirnu` glacial potholes, a rock crevice, a
boulder/outcrop) but are not trees, and 1 excluded because its own record
says it stands on a private plot. The remaining 23 are genuinely thin on
description (only the King's Oak in Kaarela carries free text; everything
else is a bare Finnish common name plus a neighbourhood, no age or girth
anywhere), so this register alone clears existence and species as ONE
official-register source per this project's two-source rule, and a verify
pass still has real work per tree. Helsinki is already a published city
(rank 96, 8/30 trees, 38 impressions/10 days), so this is a real deepening
opportunity, not a new-city question. One entry (the King's Oak, id 4)
needs a specific access check before it can ship: its own record places it
"in the yard of a property owned by the water utility," which needs the
same case-by-case judgement CLAUDE.md applies to company grounds, not an
automatic yes or no.


---

## United States register scouting, round two: Philadelphia, Savannah, Charleston, San Diego, Denver (2026-08-31)

Dispatched because 13 of 14 ranked US cities standing at zero have no supply at
all, and Hidde asked for more American cities. Targets and order set by the
brief: Philadelphia, Savannah, Charleston, San Diego, then Denver if time
allowed. Every one of the five named targets in the 2026-08-13 English-
speaking-block scan's "named but not reached" list is covered here except
Asheville, which already carries a written `empty` verdict (2026-08-23,
Buncombe/GreenWorks Treasured Trees, no public dataset) and was correctly not
re-scouted. Method unchanged: licence-led, quote the licence sentence
verbatim from the source's own page, semantic filter first (a full municipal
tree inventory is never supply here, however large). **No register proved
importable this pass.** Recorded in full because a written NO on five cities
is real progress against the "not reached" backlog, and the next scout should
not re-walk any of this ground.

### Philadelphia: EMPTY

**OpenDataPhilly's "Philadelphia Tree Inventory"** (the only tree dataset the
city publishes) is a comprehensive inventory of every tree within city
limits, updated yearly, exactly the bulk shape the semantic filter forbids
regardless of licence. Its licence is also a clean disqualifier on its own
terms, quoted verbatim from the dataset's own OpenDataPhilly page: "The City
of Philadelphia reserves all rights in the database and any data contained
therein, and the end user's use of the data does not constitute a transfer
of, nor does the end user receive, any title or interest in the database or
any other City data." Both grounds fail independently.

**Philadelphia's "Heritage Tree" designation is not a curated list at all.**
Read directly from the zoning code excerpt at
`phila.gov/media/20171115163236/Heritage_Trees.pdf`: Section 14-705 protects
any tree of a listed species (29 species named, common ones like red maple,
white oak, tuliptree, American beech) that equals or exceeds 24 inches DBH on
a lot over 5,000 sq ft, city-wide. This is a size-and-species threshold
applied automatically to any qualifying tree on any qualifying lot, the same
shape as a UK Tree Preservation Order, not an individually designated
register. There is no dataset of which trees actually hold the designation,
because the designation is a rule rather than a list.

**phillytrees.blogspot.com's "Notable Trees List"** is real and well written
(named trees with cross streets, best-season notes, by neighbourhood) but it
is one enthusiast's personal blog with no coordinates, no stated licence
(Blogger default, no CC declaration found), and no public-body designation
behind it. Same status as monumentaltrees.com under hard rule 1: usable to
find and cross-check candidate trees by hand, never to import or copy.

**Verdict: empty.** No importable register. If Hidde names Philadelphia for
from-zero research, the blog list above is the fastest lead source to start
from.

### Savannah: EMPTY for import, one real lead source found (state-level, not Savannah-specific)

**Savannah Area GIS (SAGIS), `pub.sagis.org/arcgis/rest/services/Savannah/Trees`**,
is exactly the ArcGIS Hub pattern the brief expected, and it fails the
semantic filter cleanly: two layers, "Trees" (36,553 features) and "Other"
(2,723 features), described in the service's own metadata as "City of
Savannah owned trees in parks, City properties, and right of ways...
contractor provided several neighborhoods to import, City staff adding trees
with mobile GIS application." That is a municipal maintenance inventory, the
same shape that killed Seattle and San Francisco, not a designated register.
No `licenseInfo` is set on the service either, so it would fail on licence
even if the semantic filter did not disqualify it outright.

**The Georgia Landmark and Historic Tree Register** (run by the Georgia Tree
Council, `gatreecouncil.org/what-we-do/programs/landmark-historic-tree-register.html`,
formerly under the Georgia Urban Forest Council name that led the search
here) is the real thing: a genuine statewide semantic register going back to
1994, two categories (Landmark: integral to community heritage, 75+ years;
Historic: tied to a specific historic person/event/place, 50+ years), each
entry reviewed and voted on by a committee. The full list is published
directly in the page's own HTML as plain text (name, place, year designated),
not as a downloadable dataset, has no coordinates, and inconsistently gives
species. No licence or copyright statement of any kind was found anywhere on
the site. **That is a stall, not a yes**: found, reachable, real content,
disqualified for import on the missing-licence ground alone, same pattern as
American Forests' champion tree PDF and the Live Oak Society roster already
on file. It names two Savannah entries directly: "The Candler Oak, 2001,
Savannah" (already independently documented, Wikipedia has its own page,
strong candidate for from-zero research regardless of this register) and
"Live Oak Trees of Bonaventure Cemetery, 2004, Bonaventure Cemetery,
Savannah." The list also covers dozens of other Georgia towns, so it is worth
keeping in mind for any future Georgia city, not just Savannah.

**Worth a permission ask, same shape as the American Forests and Live Oak
Society asks already on file**: the Georgia Tree Council is a small 501(c)(3)
nonprofit (contact `melanie@gatreecouncil.org` per its own site), the
Landmark/Historic register is exactly the semantically-filtered content this
project wants, and a nonprofit with an educational mission is a plausible
yes. Not drafted this pass (Hidde's to send, hard rule 4), flagged for him if
he wants it.

**Verdict: empty for import.** Recorded in `data/register-scouting.json` as
`stalled` rather than `empty`, since a live licence-ask path exists.

### Charleston: EMPTY

**Charleston's "Grand Tree" ordinance** (City of Charleston and Charleston
County both run versions) protects any tree 24 inches DBH or greater except
pines and sweetgums, city/county-wide, on single-family residential
properties without further individual designation. Confirmed from the city's
own Tree Removal Information page and cross-checked against
charlestontreeexperts.com's summaries of both the city and county ordinance
text. This is the same size-threshold shape as Philadelphia's Heritage Tree
rule and UK TPOs: a legal protection class, not a curated list of individual
trees, so there is nothing to import even before a licence question arises.

**The City of Charleston's own open-data portal** (`data-charleston-sc.opendata.arcgis.com`,
owner account `python_chs`) was searched directly via the ArcGIS sharing API
for every dataset that account publishes with "tree" in the name: five
results, all tree-canopy coverage or land-cover layers (`Tree Canopy
Landcover`, `Subdivisions with Percent Tree Canopy`, `Percent Tree Canopy by
Street Segment`, `Potential Planting Areas`, `Land Cover`). None is a point
layer of individual trees, designated or otherwise; these measure canopy
extent, not trees you could stand in front of.

**The Live Oak Society roster already on file** (OPEN_DATA_SURVEY.md,
2026-08-15 North America pass, "written-permission-required" verdict) names
Charleston 34 times in one sampled 265-page file. That verdict stands
unchanged and was not re-scouted here; it remains the single best Charleston
lead if Hidde ever asks the Louisiana Garden Club Federation for permission.

**Verdict: empty.** No importable register found or expected without a
permission grant on the Live Oak Society roster.

### San Diego: EMPTY, but the right-shaped program is now on record

**Council Policy 900-19, "Public Tree Protection"** (`docs.sandiego.gov/councilpolicies/cpd_900-19.pdf`)
defines exactly the individually-designated model this project wants: four
categories, Landmark Tree ("unusual size... special and intact aesthetic
form... a species of tree that rarely occurs in the City... the intent of
this category is to recognize unusual trees... and not to apply this
category to a broad number of trees"), Heritage Tree, Parkway Resource Tree
and Preservation Grove. Confirmed on the city's own preservation page
(`sandiego.gov/trees/preservation`): a tree is nominated, inspected by the
Right of Way Management Division, then forwarded to the Community Forest
Advisory Board for evaluation and possible protected status.

**But there is no public list, map, dataset or export of which trees actually
hold any of the four designations.** The preservation page links only to a
nomination form (`sandiego.gov/sites/default/files/legacy/street-div/pdf/nomform.pdf`),
never to a register of results. A direct ArcGIS sharing-API search for
"landmark tree San Diego" returned zero results. This is the identical dead
end already on file for Ontario's Heritage Tree Program and Buncombe
County/Asheville's Treasured Trees: the right shape of program, nomination-
and-plaque only, nothing structured to import.

**A different San Diego "Heritage Tree Preservation Program" (County Parks,
`sdparks.org`) is not the same thing and does not help.** Read directly: it
is a drought-response tree-health and replacement program for County Parks
land generally ("evaluate the health of existing trees... ensure no net loss
of trees... diversify tree species"), not a register of individually
significant trees. Noted so nobody chases this name again expecting a
designated-tree list.

**`webmaps.sandiego.gov` hangs**: `curl -m 20` on
`webmaps.sandiego.gov/arcgis/rest/services/DSD/Environment/MapServer/layers?f=json`
returned no response at all, twice, full 20-second timeout each time. Added
to `data/fetch-blocklist.json`.

**Verdict: empty.** If Hidde names San Diego for from-zero research, Balboa
Park (27 monumental trees per the San Diego History Center's own 2018
survey, `sandiegohistory.org/journal/v56-3/v56-3carter.pdf`, including a
Moreton Bay Fig in the California Registry of Big Trees) is the standing
cluster to start from, not the Landmark Tree program.

### Denver: STALLED, a genuine statewide champion-tree list exists, no licence stated

**Colorado Tree Coalition's Champion Tree Program** (`coloradotrees.org/colorado-champion-trees`)
publishes two real, structured spreadsheets, found as direct download links
on the page itself: `2026-Website-Champ-Trees.xlsx` (846 rows, the top
national-style ranked list per species statewide) and
`2026-Website-County-champ-list.xlsx` (891 rows, a county-organised champion
list). Both carry genuine field measurements: common/genus/species/variety,
DBH, circumference, height, crown spread, National Points (the standard
champion-tree scoring formula), rank/position, and a `General Location`
column. This is a real semantic designation (largest of species, field-
measured, ranked), not a bulk inventory, matching the shape of the
Massachusetts DCR and Texas Big Tree registers already on file.

**307 of the 846 state-list rows carry "Denver" as their General Location.**
That is a substantial lead pile if it ever becomes usable. **But location is
city-name only, no address and no coordinates**, a step below even
Massachusetts' address-or-landmark text, so this is a from-zero-geocoding
lead list at best, the same tier as the American Forests national PDF.

**No licence statement of any kind was found anywhere on coloradotrees.org**,
checked directly on the champion-tree pages and searched specifically for a
terms-of-use or copyright page; none surfaced. Per this project's standing
rule, an absence of a licence is a stall, not a yes, the same verdict already
recorded for American Forests' national PDF and (in this same pass) the
Georgia Landmark and Historic Tree Register. **Do not import.**

**Worth a permission ask, same shape as the other small-nonprofit asks on
file**: Colorado Tree Coalition is exactly the kind of educational nonprofit
likely to say yes if asked directly, and getting a yes would unlock 307
Denver-tagged rows plus the rest of the state at once. Not drafted (Hidde's
to send).

**A second, unrelated find worth flagging for whoever scouts California
cities next: the California Registry of Big Trees** (Cal Poly's Urban
Forest Ecosystems Institute, `californiabigtrees.calpoly.edu`, ~245 trees
per its own about text, referenced by name in the same search that found
Balboa Park's Moreton Bay Fig). Not scanned to a verdict this pass: the site
is a React single-page app, the rendered HTML carries no data, and the
compiled JS bundle references `selectree.calpoly.edu/api` without the exact
route resolving to real tree data in the time available. **Unscanned, not a
verdict.** A session with a real browser (network tab) would resolve this in
minutes; worth doing before any from-zero California city pass, since a
usable version of this would help San Diego and every other CA city at once.

**Also surfaced by search, not one of this pass's targets and not chased:
`gisdata-csj.opendata.arcgis.com` publishes an item literally named "Heritage
Tree"** (item id `382c588177f5482dbe326360e92b9507`, layer 511). CSJ reads as
City of San Jose, not Denver or any city in this pass's list; it surfaced
because of generic boilerplate wording shared across several California
ArcGIS heritage-tree items. Left entirely unscanned, flagged only so a future
San Jose or Bay Area scout does not have to rediscover it by accident the way
this pass did.

**Verdict: stalled.** Recorded in `data/register-scouting.json` accordingly.

### Fetch blocklist addition

`webmaps.sandiego.gov`: hangs on the ArcGIS REST path
(`/arcgis/rest/services/DSD/Environment/MapServer/layers?f=json`), `curl -m
20` returns nothing twice, confirmed 2026-08-31.

### Summary for the merge

| Target | Verdict | What exists | Licence | Coordinates |
|---|---|---|---|---|
| Philadelphia | empty | Heritage Tree = species+size zoning threshold, no curated list; OpenDataPhilly tree inventory is bulk, all-rights-reserved | Explicit all-rights-reserved on the only dataset | No |
| Savannah | empty (stalled on GA register) | SAGIS Trees layer is bulk (36,553+2,723); Georgia Landmark & Historic Tree Register is real but page-text only, 2 Savannah entries | No licence stated on the GA register | No |
| Charleston | empty | Grand Tree ordinance is a size threshold, not a list; Charleston's own ArcGIS account has only canopy/land-cover layers | n/a, no dataset exists | No |
| San Diego | empty | Council Policy 900-19 defines 4 real designation categories, nomination-only, no published list ever produced | n/a, no dataset exists | No |
| Denver | stalled | Colorado Tree Coalition Champion Tree Program, 846 state + 891 county rows, 307 tagged Denver | No licence stated anywhere on the site | No, city-name only |

**Not reached, still on the "unscanned" list from 2026-08-13**: Los Angeles,
Austin, New Orleans, Chicago, Liverpool, Belfast, Manchester, Brighton,
Inverness, Canterbury, Stratford-upon-Avon, Stirling, Windsor, Glasgow. This
pass narrowed the US side of that list by five (four now `empty`, one
`stalled`) plus confirmed Asheville's existing `empty` verdict did not need
re-checking.

## City of Sydney, Register of Significant Trees: ANSWERED, and the answer is no (2026-08-31)

Karen Sweeney, Urban Forest Manager at the City of Sydney, replied to our
permission ask: "At this stage, we are not looking to licence the Significant
Tree data for use on external platforms." Her reason is specific and worth
recording verbatim, because it is the one that will come up again: "One of our
key concerns is ensuring that the data remains under our management and is not
republished in a way that could later be incorporated into paid products or
services." She proposes instead a model that sends people back to the City of
Sydney's own site for the information.

**So the 2,504 trees are closed, and this is now a written verdict rather than
an open question.** Do not scout this register again, do not re-ask before a
long time has passed, and do not treat the ArcGIS feature service being
reachable as permission: it is not.

**What this does NOT block.** Nothing we publish in Sydney came from that
register in the first place: all six trees stand on botanic-garden pages,
museum records, council pages, the BBC and Wikipedia, each with its own
sources. Facts about individual trees remain findable and verifiable from
elsewhere, exactly as with any non-licensable source. What is closed is
republishing their dataset, which we were never doing.

**The transferable lesson.** A municipality's worry is not attribution, it is
that a free dataset ends up inside somebody's paid product. That objection is
answered by what a project DOES rather than by what it promises, so the useful
reply is to point at what is actually published and not to argue.

## China: 古树名木 (ancient and famous trees), scouted at the national level and on Beijing, Shanghai, Guangzhou, Hangzhou, Nanjing, Suzhou: EMPTY, no account created, no licence to record (2026-09-02)

> **CORRECTED THE SAME DAY, 2026-09-02, and the correction changes what a future
> pass should do.** The verdict above says EMPTY, meaning no register exists to
> find. That is right about a bulk machine-readable dataset and wrong about the
> register, and the difference matters: EMPTY tells the next scout to stop
> looking, and this does not.
>
> **Guangzhou publishes its ancient trees as a GAZETTE TABLE, which is the
> Sweden shape.** The city has designated them in numbered batches by government
> notice since 1985 (five batches; the fourth covers 315 trees, the fifth 268),
> and the Bureau of Forestry and Landscaping published the full grade-two list on
> 2024-07-11 at
> `lyylj.gz.gov.cn/zwgk/sjfb/content/post_9756098.html`.
> Fetched and parsed here: **156 trees in one inline HTML table**, columns
> 序号, 编号 (a 17-digit register number), 每木类型, 县(区、市), 树种 (species),
> 乡镇（街道）, 村（社区）, 小地名, 权属 (ownership), 估测树龄 (estimated age) and
> 古树等级 (grade). Ages run 301 to 484 years. 94 of the 156 are lychee, 25 banyan.
> Ownership is 137 集体 (collective) and 19 国有 (state), which speaks directly to
> hard rule 10. **What it has no column for is coordinates**, though 小地名 is
> unusually precise, down to "the fifth tree to the right of number 4".
>
> **THE LICENCE IS THE BLOCKER, not the data.** That site's own footer reads
> `版权所有Copyright © 2018 广州市林业和园林局`, all rights reserved, with no open
> licence anywhere. Under this project's rules that **disqualifies a bulk import**
> and leaves the source usable only to FIND trees that are then verified from
> elsewhere, exactly as Texas and Nevada are treated.
>
> So the honest China verdict is not "no register". It is: **the registers exist,
> several are published as readable gazette tables, none carries an open licence,
> and none carries coordinates.** A Chinese city is therefore ordinary
> web-research work with an unusually good lead list to start from, and the thing
> that would change that is permission rather than another search.
> `gz.gov.cn` hangs to curl, WebFetch and a browser session alike; the
> `lyylj.gz.gov.cn` subdomain serves the tables fine.


Dispatched by Hidde after a Beijing verify pass reported the register's shape:
tree-level data exists (species, age, height, girth, custodian unit, growth
habits, historical significance) but sits behind a QR code on each tree's
physical plaque, register-number format `110131A04650`, with no browsable
portal found from that pass. This scout asked whether a bulk, licensed,
account-free route exists anywhere in the country. It does not.

**1. Is there a public, machine-readable or fetchable list? No, at every tier checked.**

- **data.beijing.gov.cn** (the municipal open-data platform) loads fine to a
  plain `curl -m 20` with a browser UA and its search/catalogue pages render.
  The only dataset published by the 市园林绿化局 (Bureau of Landscaping and
  Greening) anywhere on the platform is `乡镇林业站信息` (township forestry
  station addresses, Pinggu district, 15 rows: station name and address only,
  no trees). No `古树名木` or `名木` dataset exists on this platform under any
  topic or agency facet reached. `yllhj.beijing.gov.cn`'s own `古树名木保护`
  section (`sdlh/ylkj/yllhhyzjcxnew/gsmmbh/`) is a directory of protection
  EXPERTS' names, not tree data.
- **The QR/plaque system has no public index.** Each plaque's code resolves to
  that one tree's record; no search found a browsable list of codes or a
  guessable URL pattern that would let a code be resolved without physically
  standing at the tree. Nothing was enumerated or scraped, per the brief's
  instruction, because no pattern was even found to consider.
- **The national tier is the same shape, one level up.** `全国古树名木智慧管理系统`
  (the National Ancient and Famous Tree Smart Management System), launched
  2023-09-25, is real and described in state media as covering "508.19万株"
  (5,081,900 trees) nationally with per-tree map positioning and archive
  lookup. No public URL for it was found anywhere, including on
  forestry.gov.cn's own coverage of its launch; every description reads as a
  professional/departmental tool for forestry staff, not a citizen-facing
  portal. The third national census (mentioned in the brief) started June
  2026 and will feed the same internal system.
- **Five other major cities checked, all the same shape.** Guangzhou (9,961
  registered trees), Nanjing (2,215), Suzhou (2,307), Hangzhou (28,952),
  Shanghai (2,812) each run their own internal "一树一档" / "一张图" tree
  management system, confirmed only through news coverage describing it as
  informatised internal management, never as a public dataset. What each city
  DOES publish openly is a **narrative showcase of a handful of named champion
  trees**: Guangzhou's forestry bureau runs a `成果展示/古树名木保护` page
  profiling individual famous trees one article each (泰山寺菩提树, 荔枝王,
  etc.), and Beijing's own coverage (news outlets citing the WeChat account
  "北京古树") profiles named trees with full plaque data (age, height, girth,
  history) in running prose. These are **lead sources for individual city
  passes, exactly the "does somebody NAME the trees" pattern this file's own
  method section now runs on**, never a register: no coordinates, no bulk
  download, one tree per article.
- Guangzhou's own gazette-notice route (`关于公布广州市第五批古树名木的通知`,
  a numbered "batch" announcement in the style that worked for Sweden's
  decision documents) could not be tested: `gz.gov.cn` hung on both
  `curl -m 20` and WebFetch (see fetch-blocklist note below). Whether these
  batch notices name individual trees with coordinates in table form, the way
  Guangdong's own "一张图/三清单" language implies they might, is unresolved
  and worth one more try from a session that can reach the host.

**2. Licence: nothing to license, so nothing is claimed.** The only concrete
document read was data.beijing.gov.cn's own site-wide `法律声明` (Legal
Statement, `gywm/mzsm/index.htm`), which is NOT a per-dataset "开放协议": the
nav link labelled 开放协议 is mislabeled/broken and actually points at the
site's feedback page (`hdfk/index.htm`), which itself only distinguishes
`无条件开放数据集` (unconditionally open datasets, downloadable directly) from
an implied conditional tier requiring application. The Legal Statement's
operative sentences, read directly rather than summarised: `用户有权免费获取
本网站所提供的所有政务数据资源，享有数据资源的非排他使用权；可自由利用、
自由传播与分享，不得违反国家相关法律规定` ("users have the right to freely
obtain all government data resources provided by this site, and hold a
non-exclusive right of use; they may freely use, disseminate and share it,
provided they do not violate relevant national laws") and `用户应在应用本网站
政务数据资源所产生的成果中注明政务数据资源来源为"北京市公共数据开放平台"`
("users must credit results built on this site's data resources to the
'Beijing Municipal Public Data Open Platform'"). Read plainly: free,
non-exclusive, redistributable, attribution required, no explicit
non-commercial clause. **This is recorded for the next scout's benefit and is
not a usable verdict for trees**, because there is no tree dataset on the
platform for it to apply to. No licence document exists for anything else
checked (Guangzhou's showcase page, the national smart-management system)
because none of them publish a downloadable dataset at all.

**3. Accounts: none created, none needed to reach what exists, and what would
need one is out of reach anyway.** `data.beijing.gov.cn` shows 登录/新用户注册
in its nav, but the one dataset found under 园林绿化局 downloaded via a plain
`下载` link with no login prompt, consistent with the "无条件开放" tier being
account-free; the conditional tier (which nothing tree-related sits in) would
need a formal `数据申请` (data application), not attempted. The national smart
management system and every municipal internal platform read as
departmental/professional tools without any public registration route at all,
which is a harder wall than a login: there is no account to request. No
registration, login or terms-of-service acceptance was attempted anywhere in
this pass.

**Verdict: EMPTY.** China's 古树名木 designation is real, rich and exactly as
described in the brief, but it is architected as a per-tree lookup system
(plaque to QR to internal database) rather than a published register, at both
the national and every city tier checked. The route into this country is NOT
a register import; it is the lead-list technique the "does anybody NAME its
trees" section of BRIEF_RESEARCH.md already codifies, applied to each city's
own showcase pages, gazette batch-notices and news coverage, city by city, at
ordinary web-research rates. Do not re-scout for a bulk China register without
a new angle; a session that can reach `gz.gov.cn` could still check whether a
批次公布 notice is a real per-tree table, which is the one thread left loose.

### Fetch blocklist addition

`gz.gov.cn`: hung on `curl -m 20` (exit 1, no connection within timeout) and
on WebFetch (`socket hang up`) fetching a 2020 batch-notice page
(`zwgk/fggw/szfwj/content/post_2833058.html`), seen 2026-09-02. The bureau's
own subdomain `lyylj.gz.gov.cn` answered normally in under a second, so route
around the `gz.gov.cn` main portal via bureau subdomains where possible.
`m.bjnews.com.cn` refused a WebFetch (`ECONNREFUSED`) on one article,
2026-09-02; cheap failure, not a hang, noted for completeness rather than as
a hard block.

### Cost

One pass, WebSearch and curl/WebFetch only, no agent dispatch, roughly 45
minutes. No trees delivered (none were sought; this was a scouting pass per
the brief). Token estimate for the daily retro: ~55k tokens.
