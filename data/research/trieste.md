# Trieste research notes (2026-08-05)

## Regional source: Friuli Venezia Giulia HAS one, and it is good

`http://decreti.regione.fvg.it/Storage/2025_71/ALLEGATO1%20AL%20DPREG%20071-2025.PDF`
"ALLEGATO A - Elenco regionale degli alberi monumentali 2025", DPReg 071/2025, 34 pages, all four provinces.

Columns: PROGR | ID SCHEDA | PROVINCIA | COMUNE | LOCALITA | LATITUDINE SU GIS | LONGITUDINE SU GIS |
SPECIE NOME SCIENTIFICO | SPECIE NOME VOLGARE | CIRCONFERENZA FUSTO (cm) | ALTEZZA (m) |
CRITERI DI MONUMENTALITA | NUMERO ELEMENTI.

What it adds over MASAF:
- **LOCALITA**, a real place name ("Parco Miramare", "Giardini Muzio De Tommasini", "Giardino Sartorio",
  "Villa Revoltella"). MASAF's national sheet has no such field, so this is what turns a coordinate into a walk.
- **CRITERI DI MONUMENTALITA**, the reason for designation, a) age/size b) form c) ecological
  d) botanical rarity e) vegetal architecture f) landscape g) historic/cultural/religious.
- **NUMERO ELEMENTI**, which separates single trees from groups (Miramare's Arbutus unedo entry is 59 elements).
- Coordinates in DMS, independent transcription from the MASAF decimal ones.

What it does NOT have: **no age field and no vitality field**, same gap as MASAF. So FVG is a Lazio-grade
list minus the age and minus the removed-trees sheet. There is also a 2020 edition
(`decreti.regione.fvg.it/Storage/2020_98/Allegato1%20al%20DPReg%20098-2020.pdf`) which can be diffed
against 2025 to find removals, which is the closest thing to a vitality signal.
An open-data mirror exists at dati.friuliveneziagiulia.it/Turismo/FVG-Alberi-Monumentali/wci5-zqtv but its
Socrata API refuses anonymous reads ("You must be logged in"), so the decree PDF is the usable channel.

## Trieste comune: 48 register entries. Two clusters.

### Cluster A: Parco di Miramare, 12 entries inside 300 m, park free to enter
| id scheda | species | girth | height | criteria |
|---|---|---|---|---|
| 11/L424 | Sequoia sempervirens | 425 | 30 | a,e,f,g |
| 24/L424 | Sequoia sempervirens | 401 | 27 | a,e,f,g |
| 03/L424 | Cupressus macrocarpa | 410 | 18 | a,b,e,f,g |
| 18/L424 | Pinus halepensis | 368 | 25 | a,b,e,f,g |
| 19/L424 | Pinus halepensis | 334 | 20 | a,b,e,f,g |
| 20/L424 | Pinus halepensis | 324 | 16 | a,b,e,f,g |
| 22/L424 | Pinus halepensis | 310 | 19 | a,e,f,g |
| 17/L424 | Pinus halepensis | 305 | 25 | a,e,f,g |
| 21/L424 | Pinus halepensis | 213 | 10 | a,b,e,f,g |
| 06/L424 | Pinus sabiniana | 250 | 20 | a,d,e,f,g |
| 01/L424 | Arbutus andrachne | 204 | 12 | a,b,d,e,f |
| 02/L424 | Quercus ilex | 267-230-250 | 28 | a,b,e,f,g |
| 23/L424 | Insieme omogeneo di Arbutus unedo, 59 elements | 90 med / 120 max | 8 | BLOCKED, not a point |

### Cluster B: Giardini Muzio De Tommasini, 13 entries inside ~250 m, free public park
9 Platanus acerifolia (542/34, 525/31, 520/28, 465/35, 460/27, 437/30, 424/27, 423/29, 408/33),
3 Aesculus hippocastanum (335/23, 335/23, 317/22), 1 Quercus ithaburensis subsp. macrolepis (179/18, criterion d only).

**Register defect found:** entries 38/L424 (423 cm, 29 m) and 75/L424 (424 cm, 27 m) carry the *identical*
coordinate 45 39 16,95 / 13 47 4,32. Same failure mode as Caserta. Both are recorded as leads, neither published.

## Verified for publication

### tri_001 The Redwood of Miramare — Sequoia sempervirens, 425 cm, 30 m
Register 11/L424/TS/06, 45.70421 / 13.71343 (45 42 15,14 / 13 42 48,33).
Second source: the Miramare state museum's own park pages and its "Giganti verdi" guided walk on the park's
monumental trees. Park laid out from spring 1856 for Archduke Maximilian, so c. 170 years.
Access free, park open daily. Precision: confirmed (register DMS and MASAF decimal agree).

### tri_002 The Monterey Cypress of Miramare — Cupressus macrocarpa, 410 cm, 18 m
Register 03/L424/TS/06, 45.70527 / 13.71578. Criteria a,b,e,f,g.

### tri_003 The Grey Pine of Miramare — Pinus sabiniana, 250 cm, 20 m
Register 06/L424/TS/06, 45.70553 / 13.71362. Criterion d, botanical rarity, plus g.

### tri_004 The Greek Strawberry Tree of Miramare — Arbutus andrachne, 204 cm, 12 m
Register 01/L424/TS/06, 45.70502 / 13.71237. Criteria a,b,d,e,f. Largest recorded in Italy's register.

### tri_005 The Great Plane of the Giardino Pubblico — Platanus x acerifolia, 542 cm, 34 m
Register 73/L424/TS/06, 45.65417 / 13.78502. Largest trunk in the comune of Trieste.
Garden built 1854-1864; municipal sources put the oldest specimens at over 170 years.

### tri_006 The Horse Chestnut of the Giardino Pubblico — Aesculus hippocastanum, 335 cm, 23 m
Register 36/L424/TS/06, 45.65444 / 13.78442.

### tri_007 The Valonia Oak of the Giardino Pubblico — Quercus ithaburensis subsp. macrolepis, 179 cm, 18 m
Register 65/L424/TS/06, 45.65525 / 13.78543. Designated on botanical rarity ALONE, the only entry in the
whole Trieste list with criterion d) and nothing else.

---

## Pass completed 2026-08-05 (second session, first died mid-pass)

**data/research/trieste.json** written with 8 trees, **data/leads/trieste.json** with 29 leads and 10 blocked.
All 47 register entries for the comune are accounted for: 8 published, 29 leads, 10 blocked.

### The second source problem, solved by one newspaper
The register (MASAF national + FVG regional decree) is ONE source, not two: same designation, two publications.
The independent source for Trieste is **Il Piccolo's survey of the city's 48 monumental trees**,
`https://www.ilpiccolo.it/cronaca/alberi-antichi-trieste-tutela-gootn505`. It carries the ages the registers
lack and it names individual trees:
- London plane, Viale al Cacciatore / rotonda del Boschetto: **over 200 years, the oldest tree in the city**
- Bagolaro, Piazza Hortis: over 180 years, fenced in 2025, ~17,000 euro of drainage work
- Largest tree in the Giardino Pubblico: ~180 years, girth "approaches 530 cm" (register says 542)
- Vallonea oak, Giardino Pubblico: "probably the only one in the entire region"
- Pinus sabiniana, Miramare: named as the "pino fantasma"
- Ownership split: 26 municipal, 14 in the Giardino Pubblico, 13 at Miramare

Second sources for the gardens themselves: comune di Trieste and verdepubblico pages (Giardino Pubblico
begun 1854 by Muzio de Tommasini, ~320 trees from 5 continents, planes planted by him personally, the only
vallonea oak in FVG); cultura.gov.it and it.wikipedia for Miramare (park begun spring 1856 by Maximilian,
exotic conifers imported within ten years).

### tri_008 added this pass — The Plane of the Boschetto Roundabout
Register 54/L424/TS/06, Platanus x acerifolia, 510 cm, 25 m, 45.654428 / 13.799328, locality Viale al
Cacciatore. **The oldest tree in Trieste**, so it drives the question page. 1.2 km straight uphill from the
Giardino Pubblico along Via Giulia, which turns the city trees into a real four-tree walk instead of one park.
Its companion 55/L424 (440 cm) stands 25 m away, recorded as a lead. Pin approximate: the pair cannot be told
apart from the register data alone.

### tri_006 folded, per the Setubal twin rule
36/L424 and 39/L424 are both 335 cm and 23 m, 30 m apart. Published as one entry describing both;
39/L424 and the third chestnut 37/L424 (317 cm) are leads. Pin approximate.

### Flagged, and why
- **tri_002 Monterey Cypress**: both registers say Cupressus macrocarpa, a popular park description says
  Cupressus sempervirens while giving the same 18 m height. Register used, conflict stated in the story.
- **tri_004 Greek Strawberry Tree**: register only. No municipal or popular source names an Arbutus andrachne
  at Miramare; the park's own material talks about the corbezzolo (A. unedo) stand, which is the 59-element
  entry 23/L424 and is blocked as not a point.
- **tri_006 Horse Chestnut**: age inferred from the garden's 1854 foundation, nothing dates these individually.

### PHOTOS: dead end, do not re-run this hunt
Zero usable photos for all eight. What was searched and what is there:
- `Category:Parco di Miramare` — **empty**. `Category:Boschetto del Ferdinandeo` — **empty**.
- `Category:Trees in Trieste` — 4 files, none a tree portrait (a sunset, the castle, two views).
- `Category:Giardino pubblico Muzio de' Tommasini` — 18 files, 15 of which are busts, a pond, a bandstand
  and a police post. One tree photo only.
- Three candidates were downloaded and **looked at**, all rejected against the Cadiz standard:
  - `"Sua Altezza"Sequoia - panoramio.jpg`, CC BY-SA 3.0, Fulvio Bacchia, GPS 45.704153/13.713459 which is
    **7 m from the tri_001 pin**, so it is almost certainly the right tree. Rejected anyway: it is a
    look-straight-up-the-trunk shot. Fine redwood bark, but the tree is not readable and a wide card crop
    gives a band of trunk. The best near-miss on the list if the standard is ever revisited.
  - `Giardino Muzio de Tommasini - Ippocastano.jpg`, CC BY-SA 4.0, Wilrooij, GPS 55 m from the tri_006 twins.
    Rejected: shot on 1 December, overcast, underexposed to near-silhouette, tree almost bare, and the GPS is
    too far off to say which chestnut it is.
  - `Drammatic .....Sequoia - panoramio.jpg`, CC BY-SA 3.0. Rejected: GPS is 150 m from either registered
    redwood, so the subject cannot be established.
Next place to look is iNaturalist and Flickr geosearch on the two park polygons, not Commons.
