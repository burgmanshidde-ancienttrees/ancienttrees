# Napoli research pass, 2026-08-05

## IMPORTANT: Naples already exists as a published city
`data/cities/naples.json` holds 10 trees, all `curation_status: flagged`, status `needs_curation`.
This pass is a register-grounded rebuild of the walkable core. Id collisions must be resolved
before merging: see the mapping note at the bottom.

## Cluster chosen: Real Bosco di Capodimonte
134 hectares, free entry, open 07:00-19:30 (Apr-Sep). The Giardino dei Principi reopened to the
public on 4 June 2025 after restoration. Six register trees are independently described on the
museum's own site (capodimonte.cultura.gov.it), which is the second source for each.

Walk as finally chosen: Porta Grande -> Giardino dei Principi -> Real Fruttiera. 7 trees, all
inside one free park. The Giardini Principessa Jolanda leg was dropped late in the pass; see
"DEAD TREE FOUND" below for why.

## Sources in play
- MASAF national register (data/registers/italy-masaf.json, comune Napoli, 53 entries) = source 1
- https://capodimonte.cultura.gov.it/gli-alberi-monumentali-del-real-bosco-di-capodimonte/ = source 2
- https://capodimonte.cultura.gov.it/un-giardino-storico/

## CORRECTION FOUND IN LIVE DATA
`nap_004` on the live page reads "documented since 1753". That is not a date: the museum page
writes the species as "Taxus baccata L. 1753", which is Linnaeus's authority citation in Species
Plantarum. The same trap sits in "Cinnamomum camphora (L.) J. Presl, 1825". Neither is a planting
date and neither should be published as one.

## Verified trees

### 1. Camphor of the Giardino dei Principi (Cinnamomum camphora)
- MASAF sheet 42/F839/NA/15, girth 830 cm, height 15 m, 40.86884, 14.25249
- Museum: planted "around the early 1800s", arrived directly from China, canopy about 400 sq m,
  "one of the largest and most majestic trees of the entire royal site and among the principal
  camphor trees of Europe"
- Museum quotes 670 cm at 130 cm height against MASAF's 830 cm. Breast height vs base, the same
  pattern seen in Setubal. Publish the range honestly.
- Two sources. ALIVE, free access. location_precision confirmed.

### 2. Yew of the Giardino dei Principi (Taxus baccata)
- MASAF sheet 44/F839/NA/15, girth 250 cm, height 10 m, 40.86844, 14.25271
- Museum: 10 m, 250 cm, sculptural trunk and emerging roots, one of the few native species in the
  garden. Figures match MASAF exactly.
- No age anywhere. Do not invent one, and do not repeat the 1753 error.
- Two sources. ALIVE, free access. confirmed.

### 3. Montezuma Cypress of the Giardino dei Principi (Taxodium huegelii / mucronatum)
- MASAF sheet 41/F839/NA/15, girth 300 cm, height 15 m, 40.86870, 14.25258
- Museum: 18 m x 3 m, "one of the first specimens of the species to arrive in Naples" in the 1800s,
  identified by Michele Tenore, director of the Naples botanical garden. Girth matches; height
  differs (15 vs 18), so state it loosely.
- Two sources. ALIVE, free access. confirmed.

### 4. Paperbark of the Giardino dei Principi (Melaleuca styphelioides)
- MASAF sheet 39/F839/NA/15, girth 75 cm, height 9 m, 40.86890, 14.25383
- Museum: planted mid-nineteenth century, "a true rarity", found only in the Bourbon royal sites
  of Naples.
- Smallest girth in the Naples register at 75 cm. It is listed for rarity, not size. Say so.
- Two sources. ALIVE, free access. confirmed.

### 5. Swamp Mahogany near Porta Grande (Eucalyptus robusta)
- MASAF sheet 43/F839/NA/15, girth 330 cm, height 35 m, 40.86664, 14.25215
- Museum: 30 m, "the largest exotic specimen of the entire Real Bosco", places it in the Real Bosco
  near Porta Grande, which matches the MASAF coordinate better than MASAF's own locality string
  (MASAF files it under "Giardino dei Principi", 250 m away). Second source corrects the register.
- Heights differ 30 vs 35 m. State about 30 metres and note the register's higher figure.
- Two sources. ALIVE, free access. confirmed.

### 6. Camphor of the Real Fruttiera / Giardino Torre (Cinnamomum camphora)
- MASAF sheet 40/F839/NA/15, girth 730 cm, height 18 m, 40.88014, 14.26141
- Museum: 20 m, 730 cm circumference, canopy over 450 sq m, stands at the centre beside a white
  marble fountain, arrived in the 1800s. Girth matches exactly.
- 1.4 km north of the Giardino dei Principi, still inside the free park.
- Two sources. ALIVE, free access. confirmed.

### 7. Cretan Date Palm, just inside the Porta Grande (Phoenix theophrasti)
- MASAF sheet 52/F839/NA/15, girth 380 cm, height 16 m, 40.86631, 14.25219
- Campania regional register scheda 249: identical 380 cm and 16 m, coordinate 40.866309, 14.251963
  (25 m apart), age 100 years at the record's last update (Dec 2019 / Jan 2020), so about 105 now.
  Arrived as a "ricordo di guerra" during Italy's early-1900s campaigns in the eastern Mediterranean.
  Trunk branched at the base, which the register calls atypical for the genus.
- Two sources. ALIVE, free access. confirmed.

## SECOND LIVE-DATA ERROR
Live `nap_003` (Eucalyptus robusta) carries the coordinates 40.86884, 14.25249, which are the
CAMPHOR's coordinates. Two different trees share one pin on the live site. The correct position is
40.86664, 14.25215, agreed by both the register and the museum's "near Porta Grande" placement.

## DEAD TREE FOUND, DO NOT PUBLISH
The monumental Platanus orientalis of the Giardini della Principessa Jolanda (MASAF 396 cm,
40.86681, 14.24842) is gone. A century-old plane on the Scale della Principessa Jolanda was split
in half by lightning and fell into the road in the storms of 23-24 August 2022, reported with
photographs by Carlo Restaino, councillor of the III Municipality. The register still lists it.
Blocked in data/leads/napoli.json.

Knock-on doubt: the Cedar of Lebanon and the camphor in the SAME garden are register-confirmed
(regional scheda 23, MASAF) but nothing published after August 2022 confirms they still stand, so
both are held as leads rather than published.

## PHOTOS: none
Wikimedia Commons geosearch at 400 m around the Giardino dei Principi returns museum interiors and
Paolo Monti's 1966 black-and-white series, both disqualified (B&W is banned, interiors are not the
tree). Category:Real Bosco di Capodimonte is empty. iNaturalist has 74 plant observations within
1.5 km and none of the seven species with an open photo licence. This is a documented dead end for
now; do not re-run it. UGC is the realistic route.

## Final set: 7 trees, ids chosen to PRESERVE live identity
| research id | tree | live file |
|---|---|---|
| nap_001 | Camphor of the Garden of the Princes | same tree, same id |
| nap_002 | Camphor of the Royal Fruit Garden | same tree, live calls it "Royal Orchard" |
| nap_003 | Swamp Mahogany by the Porta Grande | same tree, coordinates corrected |
| nap_004 | Yew of the Garden of the Princes | same tree, 1753 date removed |
| nap_005 | Montezuma Cypress | same tree, same id |
| nap_011 | Cretan Date Palm | NEW |
| nap_012 | Prickly Paperbark | NEW |

Live nap_006 to nap_010 are untouched by this pass. nap_006 (citrus grove) and nap_008 (pine
planted 1995) should be retired; reasons in data/leads/napoli.json under "blocked".

Walk: 6 of the 7 sit within 328 m of each other; nap_002 is 1.7 km north through the same park.
