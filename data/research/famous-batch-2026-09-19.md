# Famous-tree batch, 2026-09-19

Source: `famous_demand.py --gap` (read in other languages, unwritten in
English: the thin-competition end, which is where the distribution rule says
we can rank). NOT `--next`, which grouped by country and offered 12 Lithuanian
oaks at 5-16 reads a month each.

Already checked against published trees by name and by distance.
**La Pochota (Mexico, 108/mo) was dropped: already live in Chiapa de Corzo,
0.1 km away, same name.**

| # | Tree | Country | Reads/mo | Pin | Container |
|---|---|---|---:|---|---|
| 1 | Lulin Sacred Tree | Taiwan | 213 | none | own place, find the pin |
| 2 | TV-eken | Sweden | 119 | none | own place, find the pin |
| 3 | Xiangyang Famous Tree | Taiwan | 113 | yes | joins Chishang, 28.3 km |
| 4 | Najevnik Linden Tree | Slovenia | 101 | none | own place, find the pin |
| 5 | Figueira das Lagrimas | Brazil | 98 | none | own place, find the pin |
| 6 | Oak of Bataszek | Hungary | 82 | yes | own place, 144 km from anything |
| 7 | Araucaria madre | Chile | 67 | none | own place, find the pin |
| 8 | Okuteshinmeijinja no osugi | Japan | 59 | none | own place, find the pin |
| 9 | Zlatolist Plane Tree | Bulgaria | 57 | none | own place, find the pin |
| 10 | Tilleul de Turenne | France | 56 | none | own place, find the pin |
| 11 | Rotomanty | Finland | 52 | yes | joins Lohja, 19.5 km |

Claims pushed: chishang, lohja.

## What the pass must not assume
- A Commons category is a research list, never an import. One German lead's
  own category mixed photographs of two unrelated trees.
- Two independent sources for existence, species and age, as everywhere.
- A tree standing alone must pass the destination test (2026-08-31): would
  somebody travel specifically for THIS ONE TREE. Being a good tree is not
  the test. One that fails stays a lead.
- Hard rule 10 in full: a withheld location stays withheld, somebody's home
  stays out, and `access` says honestly what the visitor will meet.

## Findings
(appended by the pass as they complete)

**Environment note, read before trusting anything below.** This pass ran in a
sandbox where WebFetch and curl are blocked at the network-policy level for
every external host tested (Wikipedia in any language, Wikimedia Commons,
Wikidata, archive.org, even google.com: all `connect_rejected`/`EGRESS_BLOCKED`,
not a timeout or a single hanging host, so nothing goes on
`fetch-blocklist.json`, this is total). Only WebSearch works, and it returns a
synthesised AI summary over search snippets, which BRIEF_RESEARCH.md's own
Cyprus-olive lesson says is a lead, never a source, because it has already
invented figures that were not on the page. I could not fetch a single primary
page this pass to check a figure against the pixels of the source. So: every
number below is WebSearch-mediated, cross-checked only by asking multiple
differently-worded queries and keeping what several independent phrasings
agree on, every entry ships `curation_status: "flagged"`, and none of this
should be read as meeting the normal two-fetched-sources bar. A pass that CAN
fetch should re-verify every figure here before it ships to a city file.

### 4. Najevnik Linden Tree (Najevska lipa), Slovenia — VERIFIES

```json
{
  "id": "naj_001",
  "name": "Najevnik Linden Tree",
  "species": "Small-leaved Lime (Tilia cordata)",
  "age_estimate": "roughly 700-790 years",
  "age_min": 700, "age_max": 790,
  "girth_cm": 1070,
  "height_m": 24,
  "location": {
    "address": "By the Najevnik homestead, Ludranski Vrh, above Črna na Koroškem, Carinthia (Koroška) region, Slovenia",
    "latitude": 46.4341,
    "longitude": 14.8640,
    "neighbourhood": "Ludranski Vrh"
  },
  "verified_sources": [
    "https://www.rtvslo.si/news-in-english/an-ancient-linden-tree-still-brings-people-together/332092",
    "https://sl.wikipedia.org/wiki/Najevska_lipa",
    "https://www.crna.si/index.php/naravne-znamenitosti/187-najevska-lipa (municipal tourism board)"
  ],
  "access": "Free, no ticket or appointment. Reached by a maintained forest/gravel road a few km from the centre of Črna na Koroškem; stands beside the road near the Najevnik farm, described by the municipal tourism board as a signed natural attraction rather than anything requiring the farm's permission.",
  "transport": "No public transit; a short drive (roughly 4-5km on local/forest roads) from Črna na Koroškem, which itself is reached by regional road from Dravograd/Slovenj Gradec.",
  "location_precision": "approximate",
  "curation_status": "flagged",
  "verify_notes": "The thickest tree of any species in Slovenia (national champion by girth), and one of its oldest, with its own Slovenian and English Wikipedia pages plus a dedicated municipal tourism page (Občina Črna na Koroškem) and RTV Slovenija feature ('An ancient linden tree still brings people together'). Age and girth are consistent across three independently phrased WebSearch results: circumference once measured 11.24m, now 10.70m after old bark decayed on part of the trunk; height 24m; age estimated 700-790 years, explicitly because the trunk is hollow so a ring count is impossible (a genuinely derived-from-nothing-precise estimate, kept broad per the brief). DESTINATION TEST: passes clearly, it is a named national champion tree with its own signed tourist trail from the village (a hiking route is literally named 'Črna na Koroškem - Najevska lipa'). ACCESS: stands beside a public forest road near (not inside) the Najevnik farm; the municipality's own tourism material treats it as an open natural attraction with driving directions, no gate or appointment mentioned in any source. HARD RULE 10: no source withholds or blurs its position; not inside anyone's private yard, a farm 'nearby' rather than a farm's own dooryard. Coordinates are the SETTLEMENT (Ludranski Vrh) centroid from Wikipedia, not the tree itself, hence approximate; a later pass with map access should pin the actual trunk from the tourism board's own map/GPS point (visit-crna.si and crna.si both host a map listing I could not open this pass). ALIVE: RTV Slovenija's feature and the municipal page both read as current/maintained descriptions rather than historical; no dated recent photo confirmed directly, so kept flagged rather than fully confirmed alive."
}
```

### 5. Figueira das Lágrimas, Brazil — ALREADY PUBLISHED, drop from queue

**Not a new candidate.** `data/cities/sao-paulo.json` already carries this exact
tree as `spa_001`, "Figueira das Lagrimas (Fig Tree of Tears)", at
-23.60604,-46.59858, which matches this lead's own name exactly (Estrada das
Lágrimas, Sacomã, São Paulo; species Ficus organensis; the CONPRESP-listed
1822/Dom Pedro I independence-route fig). The famous-batch source list missed
this because the lead file carries no lat/lon for it, so the usual
distance-based dedupe (used correctly to drop La Pochota, per the brief) had
nothing to compare against. Same fix applies: drop it from
`data/leads/_famous-brazil.json`'s open list, or mark it `published` there, so
a future `famous_demand.py` run does not resurface it. Nothing to append to a
city file; nothing new was found. (For the record, in case the existing page
needs updating later: WebSearch converges on age ~240 years, with an older,
looser estimate of 360-400 years for "the original tree" before decline;
heritage-listed by CONPRESP in 2016; a second Ficus benjamina has grown up
beside/through the original since 1977; the site was revitalised and reopened
to the public in recent years per ipirangafeelings.com.br. Whether the live
page already reflects this is for whoever reads this note next to check.)

### 6. Oak of Bátaszék, Hungary — VERIFIES, strong candidate

```json
{
  "id": "bat_001",
  "name": "Oak of Bátaszék",
  "species": "Downy Oak (Quercus pubescens)",
  "age_estimate": "roughly 300-400 years",
  "age_min": 300, "age_max": 400,
  "girth_cm": 460,
  "height_m": 17.5,
  "location": {
    "address": "Beside the St. Urban's Chapel (Szent Orbán-kápolna), on the Orbán-hegy rural area about 2km southwest of the town centre, Bátaszék, Tolna County, Hungary",
    "latitude": 46.17004,
    "longitude": 18.70022,
    "neighbourhood": "Orbán-hegy"
  },
  "verified_sources": [
    "https://hu.wikipedia.org/wiki/B%C3%A1tasz%C3%A9ki_molyhos_t%C3%B6lgy",
    "https://www.turistamagazin.hu/hir/bataszeki-molyhos-tolgy-2022-02-25",
    "https://evfaja.hu/fa/2015/bataszek-legoregebb-faja-telepules-buszkesege"
  ],
  "access": "Free, open countryside; a signed visitor/pilgrimage destination beside a small chapel, no gate or ticket mentioned in any source. An annual pilgrimage on St. Urban's Day (25 May) douses the trunk in wine for a good grape harvest, per Bátaszék's own town website and a regional feature (csodalatosmagyarorszag.hu).",
  "transport": "No public transit found this pass; roughly 2km from Bátaszék town centre by road, walkable or a short drive/cycle.",
  "location_precision": "approximate",
  "curation_status": "flagged",
  "verify_notes": "WON Hungary's own 'Tree of the Year' (Az Év Fája) in 2015, then went on to win the EUROPEAN Tree of the Year competition in 2016, beating every other country's nominee: the single strongest superlative in this whole batch and a clean pass of the destination test on its own (it is literally the officially most-loved tree in Europe that year). Age (300-400yr) and girth (450-470cm, sources vary by ~20cm, likely different measurement years) consistent across three independently worded searches. Species is Quercus pubescens (downy/pubescent oak), the oldest tree in Bátaszék by every source. ACCESS: stands in open rural land beside a small wayside chapel, described everywhere as a visitor attraction with an annual public pilgrimage tradition (wine poured on the trunk for St. Urban's Day, patron saint of vintners), not on anyone's private land. HARD RULE 10: no withheld location, not a dwelling. Coordinates are from our own lead file (46.17004, 18.70022), plausible for '2km SW of Bátaszék' but not independently confirmed against a map this pass, kept approximate. ALIVE: sources describing the 2022 Turista Magazin piece and ongoing annual pilgrimage read as current; no explicit 2026-dated confirmation found."
}
```

### 7. Araucaria Madre, Chile — VERIFIES, pin needs a later fix

```json
{
  "id": "aum_001",
  "name": "Araucaria Madre",
  "species": "Monkey Puzzle Tree (Araucaria araucana)",
  "age_estimate": "disputed: park signage says roughly 1,800 years, published research suggests the species tops out nearer 1,000",
  "age_min": 600, "age_max": 1800,
  "girth_cm": 670,
  "height_m": 50,
  "location": {
    "address": "Along the Los Carpinteros interpretive trail, Captrén sector, Conguillío National Park, Melipeuco commune, Araucanía Region, Chile",
    "latitude": -38.674,
    "longitude": -71.607,
    "neighbourhood": "Sector Captrén"
  },
  "verified_sources": [
    "https://es.wikipedia.org/wiki/Araucaria_Madre",
    "https://mma.gob.cl/la-araucaria-mas-antigua-del-pais-tiene-1-021-anos/ (Chilean Ministry of the Environment)",
    "https://laderasur.com/articulo/araucaria-madre-guardiana-ancestral-de-la-region-de-la-araucania/"
  ],
  "access": "Paid entry (CONAF national park fee) and a marked trail (sources give 3-5km for the Los Carpinteros/Laguna Captrén trail, a moderate walk, not a permit-gated trek), which is the price-and-schedule case this project treats as a yes, not a private-permission case.",
  "transport": "No public transit to the park entrance found this pass; reached by car via Curacautín (northern/Captrén access) or Melipeuco (southern access), then the marked trail on foot.",
  "location_precision": "approximate",
  "curation_status": "flagged",
  "verify_notes": "Chile's national tree (Araucaria araucana), individually named and signposted as the largest and oldest specimen on a trail built specifically to see it and its neighbouring giants, inside the country's most-visited araucaria national park. DESTINATION TEST: passes, it is a specifically named, trail-marked attraction people travel to Conguillío in part to see. AGE DISPUTE, recorded rather than picked: CONAF's own park signage has said ~1,800 years for years; Chile's Ministry of the Environment (mma.gob.cl) reports that the first scientific study confirming any Araucaria araucana over 1,000 years old was only published in 2017, dating the oldest verified individual (not stated as necessarily this same tree) at 1,021 years, and other sources (Ladera Sur) give a looser 600-1,000-year range for this specimen. A later writing pass should present this honestly as a contested figure rather than pick 1,800. SIZE: height ~50m converges across sources; girth given directly as 6.7m circumference in one source and as 2.2m diameter in another (2.2m x pi = ~691cm, close enough to the stated 6.7m to be the same figure, not two different ones; used the directly-stated circumference). ACCESS: CONAF-run national park, standard entrance fee, a maintained trail, nothing private or gated beyond the ordinary park fee. COORDINATES: I could not fetch a page or GPS track with the tree's own position this pass (Wikiloc has exact GPX tracks for 'Sendero Araucaria Madre' but I could not open them); the point given is a rough estimate for the Laguna Captrén / Captrén sector of the park from general geography, NOT read off any specific source, and should be treated as barely better than 'somewhere in this park sector' until a pass that can open a map or a GPX track fixes it. ALIVE: multiple 2025-dated articles (revistaaraucania.cl, May 2025) describe it in the present tense as a current attraction."
}
```

### 8. Okuteshinmeijinja no ōsugi, Japan — DEAD, blocked

**Never ships.** This is the Great Cedar (大杉/ōsugi) of Shinmei Shrine in
Ōkute (大湫町), Mizunami City, Gifu Prefecture, on the old Nakasendō highway.
Two independent sources agree it **toppled in heavy rain on 11 July 2020**:
the local Ōkute-chō community council's own site (okute-shuku.jp, which has
run ongoing coverage of the fallen tree and a fundraising/support group for
what remains) and an independent blog covering the Nakasendō post towns
(maruho-design.com). A portion of the trunk is preserved on the shrine grounds
for visitors to see, but the living tree is gone, which is exactly the
Queen-Elizabeth's-Oak/Stock-im-Eisen case CLAUDE.md names as failing the
'must be alive' bar: a preserved remnant is not a collectible entry. Also
worth recording for whoever revisits Ōkute: sources disagree sharply on its
age at death, prefectural-monument-era estimates around 1,300 years versus a
2020 scientific (carbon-14) study putting it at roughly 670 years, itself
called out as unusually old for a Honshu cedar; not that it matters for
publication, but a future pass should not resurrect the 1,300-year figure as
fact if this ever gets reconsidered as a 'notable remains' story element
elsewhere. BLOCKED, reason: dead (fell 2020-07-11); a preserved trunk stump
remains but is not a living, collectible tree.

### 9. Zlatolist Plane Tree, Bulgaria — VERIFIES

```json
{
  "id": "zla_001",
  "name": "Zlatolist Plane Tree",
  "species": "Oriental Plane (Platanus orientalis)",
  "age_estimate": "roughly 1,300 years (widely repeated, not independently derived this pass)",
  "age_min": 1000, "age_max": 1300,
  "girth_cm": 600,
  "height_m": 29,
  "location": {
    "address": "Courtyard of the Church of St. George the Victorious (Sveti Georgi), village of Zlatolist, Sandanski Municipality, Blagoevgrad Province, Bulgaria",
    "latitude": 41.46389,
    "longitude": 23.43694,
    "neighbourhood": "Zlatolist"
  },
  "verified_sources": [
    "https://bg.wikipedia.org/wiki/%D0%97%D0%BB%D0%B0%D1%82%D0%BE%D0%BB%D0%B8%D1%81%D1%82%D0%BA%D0%B8_%D1%87%D0%B8%D0%BD%D0%B0%D1%80",
    "https://bnt.bg/bg/a/hramat-sveti-georgi-v-zlatolist-vyara-i-legendi (Bulgarian National Television)",
    "https://pirinsko.com/vekovniqt-chinar-na-prepodobna-stojna-dyrvoto-koeto-slusha-choveshkite-mechti-185710/"
  ],
  "access": "Free, open church courtyard. BNT (national broadcaster) describes the church and tree as one of the most visited sites in Bulgaria, with thousands of Bulgarian and foreign pilgrims and tourists visiting year-round; this is a village parish church rather than an enclosed monastery, and every source treats it as a standing pilgrimage/tourism destination rather than a restricted site.",
  "transport": "No public transit found this pass; a village in Sandanski municipality, reached by car/tour bus (excursion operators run day trips from Melnik/Sandanski that include it).",
  "location_precision": "approximate",
  "curation_status": "flagged",
  "verify_notes": "Named among Bulgaria's best-loved trees ('Ancient Trees Speak Up' category, 2014 national competition) and tied to the legend of the Venerable Stoyna, a clairvoyant figure locally compared to Baba Vanga, which draws sustained pilgrim traffic specifically to this churchyard tree. DESTINATION TEST: passes, this is a named, legend-carrying tree that is explicitly the reason (along with the church) people travel to an otherwise small village. Age (~1,300 years) is repeated across Bulgarian sources but I found no stated derivation (no growth-rate or ring-count basis given), so treat it as a repeated traditional figure rather than a scientifically derived one; kept broad. Height 28-30m and base circumference 6m converge across sources. ACCESS/HARD RULE 10: stands in the courtyard of a functioning parish church that multiple sources (including the national broadcaster) describe as one of the country's most-visited pilgrimage sites, open to the public; this is the churchyard case CLAUDE.md treats as a yes, not the enclosed-monastery case that needs evidence. Coordinates are the VILLAGE centroid from Wikipedia, not the tree/church itself, hence approximate. ALIVE: described in present tense by a 2026-current-looking BNT feature and by recent-dated travel/blog posts; no explicit dated photo checked this pass."
}
```

### 10. Tilleul de Turenne, France — VERIFIES

```json
{
  "id": "tdt_001",
  "name": "Tilleul de Turenne",
  "species": "Small-leaved Lime (Tilia cordata)",
  "age_estimate": "at least 700 years (from girth, not a precise figure)",
  "age_min": 700, "age_max": 900,
  "girth_cm": 800,
  "height_m": 20,
  "location": {
    "address": "Beside the town hall (mairie), Fontaine, Territoire de Belfort, France",
    "latitude": 47.6589,
    "longitude": 6.9977,
    "neighbourhood": "Fontaine village centre"
  },
  "verified_sources": [
    "https://fr.wikipedia.org/wiki/Tilleul_de_Turenne",
    "https://www.francebleu.fr/emissions/c-est-arrive-pres-de-chez-vous/y-a-t-il-un-rapport-entre-turenne-un-militaire-du-17-eme-et-le-tilleul-de-turenne-qui-se-trouve-a-fontaine-3578609",
    "https://www.annuaire-mairie.fr/arbre-remarquable-tilleul-de-turenne.html"
  ],
  "access": "Free, in the open village centre next to the town hall; a public 'site classé' monument, no restriction found.",
  "transport": "No public transit found this pass; Fontaine is a small commune near Belfort, France.",
  "location_precision": "approximate",
  "curation_status": "flagged",
  "verify_notes": "Note the name is misleading: this is NOT the Château de Turenne in Corrèze (a completely different place 500km away, which multiple search results initially surfaced as a false lead, worth flagging for whoever writes the container/place page so it does not get mixed up). It is in Fontaine, Territoire de Belfort, named because Marshal Turenne is said to have stopped under it on 29 December 1674 before defeating Imperial forces at Mulhouse, then made Fontaine his headquarters until the Battle of Turckheim (5 January 1675); this history is repeated consistently by Wikipedia, a France Bleu radio segment specifically asking 'is there a link between Marshal Turenne and this tree', and a remarkable-trees directory. Officially protected as a 'site classé' (French listed-site status) since 15 April 1911 for its artistic/picturesque character, one of the oldest such classifications a tree in this batch carries. DESTINATION TEST: passes, it has its own Wikipedia page, a named hiking route ('Le Tilleul de Turenne par le Bois du Fay'), and a century-old heritage listing specifically for the tree. Age is stated as 'at least 700 years' derived from girth (>8m at the base) rather than any documentary record; kept broad and open-ended on the top end since no source gives one. ACCESS: stands in the open beside the town hall, described everywhere as a freely accessible village landmark, no gate or fee. Coordinates are the mairie's own GPS point (the tree is described as immediately beside it), not the tree's own surveyed position, hence approximate. ALIVE: no explicit 2026-dated confirmation found this pass, but nothing suggests decline or removal either; a later pass should get a recent dated source before shipping as confirmed."
}
```

### 11. Rotomänty, Finland — VERIFIES, container correction needed

```json
{
  "id": "rot_001",
  "name": "Rotomänty",
  "species": "Scots Pine (Pinus sylvestris)",
  "age_estimate": "roughly 200 years",
  "age_min": 180, "age_max": 220,
  "girth_cm": 300,
  "height_m": 18,
  "location": {
    "address": "Beside a gravel road off the Lahnajärvi exit of the Turku-Helsinki motorway (E18/VT1), Suomusjärvi area, Salo, Finland (not Lohja; see note)",
    "latitude": 60.38159,
    "longitude": 23.72527,
    "neighbourhood": "Suomusjärvi (former municipality, merged into Salo in 2009)"
  },
  "verified_sources": [
    "https://fi.wikipedia.org/wiki/Rotom%C3%A4nty",
    "https://www.outinthenature.com/visiting-impressive-rotomanty-pine-tree-in-suomusjarvi-salo/",
    "https://retkipaikka.fi/5-vavisuttavan-upeaa-puuta-suomessa-naita-puujarkaleita-kannattaa-kayda-halaamassa/"
  ],
  "access": "Free, public. A short gravel-road detour from the motorway exit, one car's worth of parking near the tree; no facilities on site, no fee, no permission needed. Accessible when there is no snow on the ground per the English-language visitor writeups.",
  "transport": "No public transit found; reached by car, a short detour off the Turku-Helsinki motorway at the Lahnajärvi exit.",
  "location_precision": "confirmed",
  "curation_status": "flagged",
  "verify_notes": "CONTAINER NOTE, important: this tree is administratively in Salo (Suomusjärvi, a former municipality merged into Salo in 2009), NOT Lohja, and every source I found places it there. Our own brief's table listed it as joining a Lohja container at 19.5km; checking the coordinates against both towns, it does sit closer to Lohja (roughly 24km) than to Salo centre (roughly 33km), so a Lohja day-trip container is defensible under the day-trip rule, but the location fields must say Suomusjärvi/Salo honestly (as done above) and not imply the tree is in Lohja itself. Flagging this explicitly so whoever builds the container does not write 'Lohja' into the address. DESTINATION TEST: passes on strength of coverage as a specifically named attraction: it appears in a Retkipaikka feature titled roughly '7 awe-inspiring magnificent trees in Finland worth visiting' alongside the country's genuinely famous giant trees, plus a dedicated English-language visitor writeup (Out in the Nature) and a Finland-tourism nature-sites page, both describing it as a specific destination with driving directions. SIZE VS AGE: at ~200 years it is younger than almost everything else in this batch, but qualifies on the brief's 'visually spectacular' branch rather than age: its ~300cm girth is described as 'half again' thicker than a typically large Finnish pine (compare Finland's official largest forest pine, the Keisarinmänty, at 548cm and ~400 years, for scale; Rotomänty is not a record-holder, just an unusually thick specimen for its age, which is what earns it write-ups). Protected as a natural monument since 1959, one of Finland's older individual-tree protections. ACCESS/HARD RULE 10: roadside detour off a public motorway exit, no permission, no gate, in every source. Coordinates are our own lead file's pin, which converges with the described location (motorway exit + gravel road + Suomusjärvi), so I have kept location_precision as confirmed rather than downgrading it, but I did not independently verify it against a fresh map this pass. ALIVE: writeups read as current visitor accounts (Out in the Nature site reads as a live travel blog with recent-style content) though no explicit 2026 date found."
}
```

### 2. TV-eken, Sweden — DEAD, blocked

**Never ships.** TV-eken (also called Radiohuseken), a centuries-old oak on
Oxenstiernsgatan outside Stockholm's TV-huset/Radiohuset, Östermalm, was felled
by the city traffic office on 25 November 2011 after being found to have
severe fungal rot. Confirmed by two independent Swedish sources agreeing on
date and cause (svt.se news coverage of the felling itself, and sv.wikipedia's
TV-eken article), plus a contemporary photo-report (cawamedia.press,
"TV-eken fälld, och ligger på Djurgården!"). Age at felling was disputed
between an arborist's estimate (350-450 years) and an older "unique oak
environments" study (500-1,000 years); moot now. Recorded here rather than
silently dropped so no future pass re-discovers and re-researches it. BLOCKED,
reason: dead (felled 2011).

### 1. Lulin Sacred Tree (鹿林神木), Taiwan — VERIFIES, thin sourcing

```json
{
  "id": "lul_001",
  "name": "Lulin Sacred Tree",
  "species": "Taiwan Red Cypress (Chamaecyparis formosensis)",
  "age_estimate": "roughly 2,700-2,800 years",
  "age_min": 2700, "age_max": 2800,
  "girth_cm": 2000,
  "height_m": 43,
  "location": {
    "address": "Roadside boardwalk trail off Provincial Highway 18 (the Xinzhong-heng/Alishan cross-island highway), near km 102, Xinyi Township, Nantou County, Taiwan, elevation approx. 2,350m",
    "latitude": 23.4819,
    "longitude": 120.855,
    "neighbourhood": "Tataka area, Yushan National Park periphery"
  },
  "verified_sources": [
    "https://www.mobile01.com/topicdetail.php?f=201&t=7053509",
    "https://kids.moa.gov.tw/view.php?func=knowledge&subfunc=kids_knowledge&category=B31&id=279",
    "https://woman.udn.com/woman/story/123162/8405403"
  ],
  "access": "Free, no permit. A short boardwalk trail (about 0.2km one way, ~15 min) leads from a marked trailhead right off Highway 18 to the tree. Distinct from the longer, permit-optional Lulin Mountain trail nearby (106.1K), which climbs to a different summit.",
  "transport": "No public transit; reached by car/scooter along Highway 18 between Alishan and Tataka. Nearest bus service is the Alishan-Tataka shuttle, then a walk along the road shoulder to km102 (distance to stop not confirmed this pass).",
  "location_precision": "approximate",
  "curation_status": "flagged",
  "verify_notes": "Officially ranked the SECOND-LARGEST sacred tree (神木) in Taiwan by government/tourism sources, which is the strongest single fact for the destination test: it is a named, ranked specimen people specifically stop for along a famous scenic highway, not an anonymous giant among many. Age (2,700-2,800yr) and girth (trunk circumference ~20m) are repeated consistently across three independently-worded WebSearch results, including one from a Ministry of Agriculture children's education page (kids.moa.gov.tw), but none were confirmed by directly reading the source page (see environment note above) so treat the age as a repeated published estimate, not independently derived. The 20m circumference is almost certainly a buttressed base measurement rather than breast-height girth (species is known for massive buttress flare); a later pass should say so plainly if it survives. Coordinates here are a rough estimate from the km102/2,350m elevation description and a single WebSearch-compiled lat/lon (23°28'55\"N 120°51'17\"E converted); NOT read off a map or register directly, hence approximate. DESTINATION TEST: passes, on the strength of the official ranking and its being a well-known roadside stop on a scenic highway route (multiple travel blogs treat it as a specific, named stop). ACCESS: public highway shoulder + short boardwalk, no fee, no permit found for the tree itself (permit systems found in search apply to separate mountain trails further along). ALIVE: no explicit recent dated confirmation found this pass; the trail and interpretive signage description implies current maintained access but this needs a dated photo/observation to firm up. A later pass with real fetch access should confirm via a dated source and get an exact coordinate rather than a road-km estimate."
}
```


