# Bucaco (Mata Nacional do Bucaco), Mealhada, Portugal — research notes

Slug chosen: **bucaco**. Reason: all 29 ICNF-classified trees in the concelho of Mealhada stand
inside the walled Mata Nacional do Bucaco, freguesia of Luso. Nobody searches "Mealhada trees";
they search Bussaco / Bucaco / Bucaco Forest / Palace Hotel do Bussaco. English Wikipedia titles
its article "Bucaco Forest". Mealhada is the administrative unit only, and the town of Mealhada
is 10 km away from the trees. Page is named after the place a visitor actually goes.

Cluster: 29 register entries, all within ~440 m of each other around the Mosteiro / Palace Hotel
and the Vale dos Fetos. Tightest cluster in the whole ICNF register.

## Place-level facts (verified)
- 105 ha, 1,450 x 950 m, enclosed by a 5 km perimeter wall. More than 250 tree and shrub species,
  "one of the finest dendrological collections in Europe". (en.wikipedia.org/wiki/Bucaco_Forest)
- Benedictines from the 6th century; Discalced Carmelites took the site in 1628 and built the
  convent, the chapels and the wall. Two papal bulls are cut into stone at the main gate: Gregory XV
  (1623) forbidding women to enter, Urban VIII (1643) threatening excommunication for damaging a tree.
  (en.wikipedia.org/wiki/Serra_do_Bucaco, en.wikipedia.org/wiki/Bucaco_Forest)
- Battle of Bussaco, 27 September 1810: Wellington's Anglo-Portuguese army beat Massena here.
- Monastery dissolved 1834, site passed to the state. Neo-Manueline palace built 1888-1905, now a hotel.
- On UNESCO's tentative World Heritage list since 2004.
- Certified as a "therapeutic forest" in July 2026, first on the Iberian Peninsula, fourth worldwide,
  valid to 2031. (en.wikipedia.org/wiki/Serra_do_Bucaco)
- Cyclone Gong, January 2013: felled 10 notable trees, damaged 6 of the 86 then standing, and wrecked
  about 40 percent of the forest. Every vitality question here dates from that storm.
  (RTP/Lusa 2015-01-16; Publico 2013-01-23)

## Register traps checked
- girth_m and height_m are METRES. Values of 5.5 and 8.65 are trunk circumferences in metres.
- age_register is age at LAST MEASUREMENT. Most Bucaco entries were measured in 2016, so add 10 years.
- No age field in the Mealhada set holds a year rather than a duration: values are 100, 136, 137, 140,
  147, 150, 153, 300, 372. All read as durations, none as a calendar year. Sanity check passed.
- Twins present and folded: two sequoias at 40.37580/-8.36147 and 40.37589/-8.36147, 10 m apart,
  processos AIP01110429I and AIP01110437I, both 45 m, girths 5.64 and 5.67, both "diante da Ermida de
  Santo Elias". One visitor sight, one entry.
- The register's 29 is not a count of what exists: the Fundacao Mata do Bucaco counted 86 notable trees
  before the 2013 storm. Never quote either as a total.

---

## OUTCOME

6 trees shipped to data/research/bucaco.json, 15 leads and 7 blocked to data/leads/bucaco.json.
All 29 register processos accounted for. 1 photo, found_needs_check.

## VERIFIED TREES

### 1. King Regnans, the mountain ash (Eucalyptus regnans) — buc_004
- Register: AIP01110418I, "no cimo do Vale de Sao Silvestre", 40.37730513, -8.363180258.
  girth 8.65 m, height 72.9 m, crown 26 m, age 136 at 2016 measurement, so about 146 now.
- Second source: myplanet.pt "Eucaliptos de interesse publico" places it at the top of the Vale dos
  Fetos, calls it the largest of its species measured to date in Portugal, ~72.6 m, planted about 1880.
- Third source: Giant Trees Foundation, "L'eucalipto di Bussaco - King Regnans", laser-measured
  64.90 m, girth 8.46 m, estimated age 131, "currently the 4th tallest tree in Europe".
- HEIGHT DISAGREEMENT, must be stated on the page: register/myplanet ~72-73 m, Giant Trees
  Foundation 64.90 m by instrument. Use the range, name the disagreement.
- NOT the tallest in Europe: that is a Karri (Eucalyptus diversicolor) at 73 m in the Mata Nacional de
  Vale de Canas, Coimbra, measured by GTF in 2017. Hard rule 8 checked.
- Alive: measured by ICNF 2016, classified 2018, GTF measurement post-dates the storm.
- location_precision: confirmed (register coordinate, named singular tree, on the Estrada da Mata bend).

### 2. Eucalyptus globulus by the Palace Hotel road — buc_003
- Register: AIP01110419I, "proximo do viveiro florestal", 40.37711408, -8.365778012.
  girth 7.15 m, height 45 m, crown 32 m, age 140 at 2016, so about 150 now.
- Second source: myplanet.pt, "on the access road to the Bussaco Palace Hotel", 45 m, about 140 years,
  "classified for its great ornamental and landscape value". Height and age match exactly.
- location_precision: confirmed.

### 3. Cedro de Sao Jose (Cupressus lusitanica) — buc_006. THE VITALITY CALL, WRITTEN OUT
- Register: AIP01110430I, "no adro da Ermida de Sao Jose", 40.37477269, -8.367172464.
  girth 5.5 m, height 14 m, crown 6 m, age 372 at 2016 measurement.
- FIRST READ, WRONG: Publico (2013-01-23) and RTP/Lusa (2015-01-16) both write about this tree in the
  past tense after cyclone Gong of January 2013, and a search summary asserted flatly that it did not
  survive. Register height of 14 m against a historic 32.9 m looked like a broken remnant. I had it
  blocked as a dead tree.
- WHAT TURNED IT: (a) ICNF measured it in 2016 and classified it in 2018, and the RTP report of that
  decree states that none of the classified specimens showed poor vegetative or sanitary condition;
  (b) a Portuguese species article says it was significantly damaged by Gong but survived, and calls it
  the oldest still existing in the Mata; (c) a Wikimedia Commons photograph dated 17 September 2023,
  which I downloaded and viewed at full size and then cropped into the crown: a shattered silvered
  trunk with dead limb stubs, inside an ornate circular iron railing, carrying living green foliage
  above the break.
- SECOND SOURCE, THE STRONGEST KIND: a 2020 Commons photograph of the forest's own plaque at the foot
  of the tree, read directly off the image: "CEDRO DE S. JOSE / Plantado entre 1628 e 1650 / Com mais
  de 350 anos, e o cedro mais antigo da Mata do Bussaco". That is on-site signage, independent of ICNF,
  giving planting window and status. The register's 372 years at 2016 falls inside it.
- Species fact worth the page: Philip Miller described Cupressus lusitanica in 1768 from specimens he
  saw at Bucaco, which is why a Mexican cypress is named after Portugal and why the Portuguese call it
  cedro-do-bucaco. The register's own species authority string still reads "Cupressus lusitanica Miller".
- SHIPPED, flagged, with the storm damage stated in the story, because a visitor who walks 500 m
  expecting a spire and finds a broken trunk has been misled. Photo: CC BY-SA 4.0, Soniapampa, 2023,
  left at found_needs_check because the upward angle means the crown does not read as a tree shape.

## BLOCKED (see data/leads/bucaco.json)
- "adernal e outras especies" (AIP01110427C): a mixed stand of Phillyrea latifolia and other species at
  Cruz Alta. Not a collectible point. The adernal is still worth knowing: its world distribution is a
  few hectares here.
- Two alamedas of tree ferns (Dicksonia antarctica), one alameda of seven green ashes, and three
  alamedas of Atlas cedars along the Estrada da Mata verge (8, 7 and 10 trees, dimensions averaged
  across each row). Avenues and rows, explicitly non-collectible.

## DOUBT WORTH A HUMAN READING
- Wellington's olive rests on a match, not on a statement. The register lists an olive at the Largo do
  Mosteiro with no age; independent sources say Wellington's tree is an olive at the former convent,
  now standing in the middle of the road there. Species and position agree, but no source says the
  classified tree IS the Wellington tree. Published as tradition and flagged.
- Three of six entries are flagged, all on age rather than existence. Bucaco's individual trees are
  poorly covered in Portuguese media outside the Sao Jose cedar and the giant eucalypts, so the second
  source is usually the forest's general literature rather than a tree-specific one.
- Zero best_time on this page. Bucaco's classified trees are overwhelmingly evergreen exotics, so no
  entry has an honest seasonal peak. The sycamore maple by the Lago da Fonte (36 m, deciduous) is the
  obvious candidate and sits in leads awaiting a second source.
- King Regnans height: register 72.9 m, Giant Trees Foundation laser 64.90 m. Published as a range.
  Checked against hard rule 8: Europe's tallest is the Vale de Canas karri near Coimbra at about 73 m,
  so no superlative was claimed here beyond the foundation's own attributed "fourth tallest in Europe".
