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
