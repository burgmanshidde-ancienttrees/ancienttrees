# Florence deepening pass, 2026-08-05 (register-led)

## IMPORTANT CONTEXT FOUND FIRST

`data/cities/florence.json` ALREADY EXISTS and is published with 10 trees (ids flo_001..flo_010).
This pass is therefore NOT a new city. It is a DEEPENING pass on an existing one, driven by the MASAF
register (data/registers/italy-masaf.json, 29 entries for comune Firenze).

Existing file's weakness, measured: only flo_001/002/003 sit in the Orto Botanico cluster.
flo_004 (Ippodromo 11.2075), flo_005 (Cascine 11.2280), flo_006 (Salviatino 11.2942),
flo_010 (Villa Vogel 11.2065) are scattered across ~9 km of metropolis. 7 of 10 flagged,
6 of 10 with no photo.

The register shows the real cluster: **seven MASAF-registered monumental trees inside the
Orto Botanico / Giardino dei Semplici**, all within ~200 m of each other. The existing page
publishes only three of them.

Second source used throughout: RAMI (ilregistrodeglialberi.it), the same independent register
already cited by flo_001-003. Third: ascuoladaglialberi.net/firenze/ (Tuscany survey).

## MASAF register, comune Firenze, Orto Botanico cluster (7 entries)

| sheet | species | girth cm | height m | lat,lon |
|---|---|---|---|---|
| 01/D612/FI/09 | Quercus suber | 457 | 35.0 | 43.778444,11.261303 |
| 02/D612/FI/09 | Taxus baccata | 344 | 15.0 | 43.778389,11.261444 |
| 03/D612/FI/09 | Pinus brutia | 382 | 33.5 | 43.778444,11.261111 |
| 04/D612/FI/09 | Zelkova serrata | 453 | 25.0 | 43.778694,11.260361 |
| 05/D612/FI/09 | Taxodium mucronatum | 670 | 21.0 | 43.778361,11.262556 |
| 06/D612/FI/09 | Zelkova carpinifolia | 610 | 30.0 | 43.778750,11.261944 |
| 07/D612/FI/09 | Cedrus deodara | 418 | 28.0 | 43.778556,11.262611 |

Already published: suber (flo_002), baccata (flo_001), mucronatum (flo_003).
Missing from the page: **brutia, serrata, carpinifolia, deodara**.

## VERIFIED TREES (appended as verified)

### 1. Zelkova carpinifolia, Olmo del Caucaso , VERIFIED, 2 sources
- MASAF 06/D612/FI/09: girth 610 cm, height 30.0 m, 43.778750,11.261944
- RAMI 6488 (survey 14 Oct 2021): girth 5.75 m, height **10.00 m**, planted **1827**,
  "199 anni" estimated, GPS 43.778827,11.261576. Note: "Vecchio olmo del Caucaso presente
  nella collezione dendrologica del Giardino dei semplici". Underwent **severe crown reduction
  in the past to control a Dutch elm disease outbreak**.
- ascuoladaglialberi.net/firenze: "Zelkova crenata, Orto Botanico, 185 anni, danneggiata da
  eventi naturali."
- REGISTER TRAP CAUGHT: MASAF says 30 m tall, RAMI's 2021 survey says 10 m. That is not a
  contradiction, it is the pollarding. MASAF's height is stale. Publish the 2021 figure and say why.
- Age: planted 1827 -> **199 years as of 2026**. Three sources cluster 185-199. Solid.
- Alive: yes (2021 survey, catalogued, publicly accessible).
- Girth: two figures, 610 (MASAF) vs 575 (RAMI 2021 at 130 cm). Different measuring height. Use ~5.8-6.1 m.

### 2. Zelkova serrata, Olmo giapponese , VERIFIED but AGE CONFLICTS, flag
- MASAF 04/D612/FI/09: girth 453 cm, height 25.0 m, 43.778694,11.260361
- RAMI 6499 (survey 14 Oct 2021): girth 4.40 m at 130 cm, height 26.00 m,
  GPS 43.778691,11.260302, health "Sufficiente", "Interessante e raro esemplare monumentale".
  Planted early 1800s, attributed to **Ottaviano Targioni Tozzetti** (same director who planted
  the cork oak in 1805). Estimated over 200 years.
  Growth series on record: **3.30 m (1980), 3.89 m (2001), 4.40 m (2021)**.
- ascuoladaglialberi.net: "Zelkova serrata, Orto Botanico via La Pira, 120 anni".
- CONFLICT: 200+ vs 120 years. The growth series (2.7 cm girth/year over 41 years) does not
  settle it but leans old. FLAG and publish a wide range.
- Alive: yes, health "sufficiente" 2021.

### BREAKTHROUGH SOURCE: the garden's own monumental-trees page
https://www.sma.unifi.it/vp-363-alberi-monumentali.html (Sistema Museale di Ateneo, UniFI)
covers all seven MASAF trees with planting years. This is an independent second source for
every tree in the cluster, and it is the garden's own record, so it outranks the aggregators.

- Taxus baccata: planted **1720** by Pier Antonio Micheli, "l'esemplare piu antico dell'Orto", male tree.
- Quercus suber: planted **1805** by Ottaviano Targioni Tozzetti, never stripped for cork.
- Zelkova serrata: planted **1891**. Widest canopy of any tree in the garden.
- Zelkova crenata (= carpinifolia): planted **first half of the 1800s**. Heavily pruned in
  the **1980s** to fight a fungal disease.
- Taxodium mucronatum: planted **1884**, from **seed sent by the Palermo botanical garden**.
  Considered **Italy's largest living specimen**. Damaged by lightning 2014.
- Cedrus deodara: recorded in the garden from **1880**. "dimensioni imponenti", drooping branches.
- Pinus halepensis subsp. brutia: present from the late 1800s, **moved to its present spot in 1922**.
  Flag-shaped crown, requires constant monitoring.

### 3. Cedrus deodara, Cedro dell'Himalaya , VERIFIED, 2 sources
- MASAF 07/D612/FI/09: girth 418 cm, height 28.0 m, 43.778556,11.262611
- sma.unifi.it: in the garden since 1880 -> **about 146 years**
- Alive, publicly accessible on the garden ticket. No conflict between sources.

### 4. Pinus halepensis subsp. brutia, Pino bruzio , VERIFIED, 2 sources
- MASAF 03/D612/FI/09: girth 382 cm, height 33.5 m, 43.778444,11.261111
- sma.unifi.it: present late 1800s, repositioned **1922**, flag-shaped crown under monitoring
- Regione Toscana monumental census (via search): 384 cm girth, 33.4 m height. Matches MASAF
  to within 2 cm and 10 cm, so the MASAF figures are corroborated independently.
- Tallest tree in the cluster at 33.5 m. Age ~130-140 years, but the 1922 move means the
  tree is older than its position. Say so.

### RESOLVED: the flo_003 age flag
The existing page flags the Montezuma cypress at 115-145 years because RAMI said 1884 and
ascuoladaglialberi said 115 years. The garden's own record says **1884, from Palermo seed**.
Two independent sources now agree on 1884, so 142 years can be stated and the flag lifted.
The "Italy's largest living specimen" claim is the garden's own and is a superlative worth
softening on the page (hard rule 8): publish as "the garden calls it Italy's largest".

### REGISTER TRAPS CAUGHT THIS PASS
1. **Stale height.** MASAF gives the Caucasian zelkova 30 m. The 2021 RAMI survey gives 10 m.
   Both are right for their date: the tree was heavily pruned in the 1980s for fungal disease.
   MASAF's height predates the surgery. Never quote it.
2. **Age at last measurement.** RAMI's "199 anni" is dated 14 Oct 2021, i.e. 194 at survey.
   Planting year 1827 is the durable fact; ages are derived from it, not copied.
3. **Wrong attribution in an aggregator.** RAMI credits the Zelkova serrata to Targioni Tozzetti
   and "early 1800s". The garden itself says 1891, which is 86 years after Targioni Tozzetti
   planted the cork oak. The garden wins. Do not repeat RAMI's date.
4. **Register total is not a count of what exists.** MASAF lists 29 entries for comune Firenze.
   RAMI lists 146 for the same comune. Neither is "how many monumental trees Florence has".

### CLUSTER GEOMETRY (this is the whole point)
All seven trees sit inside the Giardino dei Semplici, within a box roughly
43.77836-43.77875 N, 11.26036-11.26261 E. That is about **185 m east to west and 43 m north
to south**. Seven MASAF-registered monumental trees inside two hundred metres, on one ticket.
By the measure used across the 81 published cities, this is the densest cluster on the site.
The existing florence.json publishes only three of the seven and then scatters the other
seven entries across 9 km of metropolis.

## DELIVERABLES OF THIS PASS (corrected mid-pass)

An earlier draft of this pass wrote `data/research/firenze.json` as a full city object, on the
assumption that Firenze was an unbuilt city. That was wrong and the file has been deleted.
The correct deliverables are:

- `data/research/florence-extra.json`, a JSON ARRAY of 5 tree objects, ids flo_011 to flo_015,
  in the schema used inside data/cities/florence.json. Nothing in data/cities/ was edited.
- `data/leads/florence.json`, leads and blocked in two kinds, plus a non-lead section recording
  the four off-cluster trees already live on the page.

### The five, and why each one
- flo_011 Zelkova carpinifolia, flo_012 Zelkova serrata, flo_013 Pinus brutia, flo_014 Cedrus
  deodara: all four are MASAF-registered trees INSIDE the Giardino dei Semplici, where the page
  already has flo_001, flo_002 and flo_003. They take the garden from 3 trees to 7 within a
  185 m strip on one ticket, which makes it the tightest cluster on the site.
- flo_015 Calocedrus decurrens, the Albero degli Sposi: 45 m from the live flo_007 in the
  Giardino del Bobolino, so it thickens the southern hillside stop rather than opening a new one.

### Count warning
10 published + 5 = **15 trees**. Florence passes ten, so the page title and the question page
must stop promising ten. Flagged, not fixed.

### Authority-citation trap: checked, clean
Per the warning from the Naples pass, every year met in this pass was checked for being a
taxonomic authority citation rather than a record. None of the dates used here are: 1720, 1805,
1827, 1880, 1884, 1891 and 1922 all come from the garden's own archive as reported on
sma.unifi.it, and 1865-1877 is the comune's construction date for the Bobolino garden.
"Taxus baccata L." carries no year in any source used here.

### Superlative conflicts found and handled
- An earlier draft called the Pinus brutia the tallest tree in the garden. It is not: MASAF gives
  the cork oak 35.0 m against its 33.5 m. Claim removed.
- The garden credits the Zelkova serrata with the widest crown in the collection, while the live
  flo_002 story credits the cork oak with "one of the widest". The zelkova claim is attributed to
  the garden rather than asserted, and the clash is recorded in the entry's notes for the merge.
- flo_003's live claims ("widest trunk of any tree in the city", 670 cm) are untouched and
  unchallenged: nothing added here exceeds 610 cm.

### Two things a human should decide
1. **Deodar naming.** flo_014 uses "Himalayan Cedar (Cedrus deodara)", the site majority (5 vs 3),
   but the live flo_008 in this same city says "Deodar Cedar". As it stands Florence's two
   deodars land on different species pages, which hard rule 9 exists to prevent. One-line fix to
   the live file, deliberately not made here.
2. **The four off-cluster live trees** (flo_004, flo_005, flo_006, flo_010), 2.7 to 4.5 km out.
   Listed with distances in data/leads/florence.json. Not touched.

### Photo budget: 3 used, all viewed at 960 px before judging
- flo_011 Zelkova crenata 01 by Line1.jpg, CC BY-SA 3.0, Line1: APPROVED. Massive fluted trunk
  fills the frame, crown readable, daylight, colour, survives the wide card crop.
- flo_013 Pinus brutia 01 by Line1.jpg, CC BY-SA 3.0, Line1: APPROVED. Whole tree against sky,
  trunk and flag crown both legible.
- flo_012 Zelkova serrata 01 by Line1.jpg, CC BY-SA 3.0, Line1: found_needs_check. Tree is the
  subject and the mosaic bark matches the story, but it is framed tighter than Cadiz wants.
- REJECTED after viewing: Cedrus deodara 01 by Line1.jpg (dark, backlit, tree unreadable) and
  Zelkova serrata a Firenze.JPG (a man hugging the trunk is the subject, not the tree).
