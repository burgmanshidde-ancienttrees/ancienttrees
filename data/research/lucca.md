# Lucca research notes (2026-08-05)

Register: MASAF national register of monumental trees, CC BY 4.0. 36 entries in the comune of Lucca,
of which 20 fall inside a 1.6 km circle on the walled city. NOTE: 36 is the register's count for the
whole municipality, not a count of what exists; LuccaInDiretta (2024-09-20) reports the same 36 and
says it is 20 more than the first 2014 census.

## Second sources found

- turismo.lucca.it "Gli alberi delle Mura di Lucca" — the comune's own tourism site publishes a tree
  itinerary along the walls. Covers the Cedar of Lebanon (Paolo Volpi, planted 1822), the North
  American cypress planted by Cesare Bicchi (director from 1860), the holm oaks on the Torre Guinigi,
  and the species planted bastion by bastion. This is the "city publishes its own tree route" case.
- LuccaInDiretta 2024-09-20, "Sono 36 gli alberi monumentali nel territorio del Comune di Lucca" —
  gives PLANTING DATES per tree in the Orto Botanico: Cedar of Lebanon 1822 (stock from the Pisa
  botanical garden c.1814), Pinus laricio 1822, Magnolia 1830, two Sequoia sempervirens c.1850,
  Ginkgo biloba 1862, Buxus balearica 1880, Cinnamomum glanduliferum 1888, Tilia tomentosa 1900.
  Also: seven holm oaks on the Torre Guinigi, documented in 14th-century Lucca artwork; 3 monumental
  trees on the walls (Monterey cypress at San Regolo, two planes at Porta San Donato and the cycle path).
- Villa Bottini: Comune di Lucca and Wikipedia. Garden is municipal property, open to the public, free.

## Register traps checked

- Girth column is centimetres and reads correctly against the physical world (655 cm = 6.55 m for the
  cedar; matches a 200-year-old Cedrus libani).
- turismo.lucca.it writes "5.76 m diameter" for the cedar, which is the SEQUOIA's girth figure in the
  register and is a diameter/circumference mix-up either way. Register girth used, not the news figure.
- No age field in the register at all for Italy. Ages here come from the planting dates in the
  LuccaInDiretta piece, which are garden records, so they are planting years and not estimates.
- Two sequoias registered 44 m apart in the same garden: not twins, but one entry pinned on the larger
  with the second recorded as a folded lead.
- Register has no vitality field: each tree checked as still standing.

## Verified trees

### luc_001 Cedar of Lebanon, Orto Botanico — VERIFIED
Register 26/E715/LU/09, 655 cm girth, 20 m, 43.841497/10.510886. Planted 1822 by Paolo Volpi, the
garden's first director, with Count Bernardino Orsetti; stock traced to the Pisa botanical garden.
Garden founded 1820 by Maria Luisa di Borbone. Two independent sources on species and date.
Access: paid entry to the Orto Botanico. location_precision confirmed.

### luc_002 Coast redwood, Orto Botanico — VERIFIED
Register 34/E715/LU/09, 576 cm girth, 35 m, 43.841428/10.511661. Second redwood 31/E715/LU/09,
500 cm, ~44 m away. LuccaInDiretta: both planted c.1850. Tallest tree inside the walls.

### luc_003 Ginkgo, Orto Botanico — VERIFIED
Register 27/E715/LU/09, no girth recorded, 26 m, 43.841792/10.511214. Planted 1862 per LuccaInDiretta.
best_time: autumn colour.

### luc_004 Monterey cypress, Baluardo San Regolo — VERIFIED
Register 09/E715/LU/09, 355 cm, 28 m, 43.840556/10.511053. One of three monumental trees on the walls.
turismo.lucca.it credits Cesare Bicchi, garden director from 1860, with the North American cypress by
the bastion. Free, on the public wall promenade.

### luc_005 Holm oaks of the Torre Guinigi — VERIFIED, ensemble entry
Register 25/E715/LU/09, "Insieme omogeneo di Quercus ilex", Via Guinigi/Via Sant'Andrea, altitude 44 m
(the tower roof, not the street). Seven trees per LuccaInDiretta and turismo.lucca.it. Collectible-point
test: passes. The ensemble is the destination, it is compact, and there is exactly one place to stand.
Age: the planting tradition is medieval and shown in Sercambi's 15th-century chronicle; the living oaks
are later replantings and no source dates them, so the story says so. Paid entry to the tower.

### luc_006 Atlas cedar, Villa Bottini — VERIFIED
Register 08/E715/LU/09, 700 cm girth, 30 m, 43.844058/10.510469. Thickest registered trunk in the
comune of Lucca. Villa Bottini garden is municipal and free to enter. Dedicated on 25 April 2021 to
don Renzo Tambellini in Lucca's Giardino dei Giusti, alongside a Calocedrus for don Guido Staderini
and a plane for don Sirio Niccolai (La Nazione). Undated; Cedrus atlantica only reached European
gardens around 1840, which is the ceiling.

## Outcome, 2026-08-05

Six trees published to data/research/lucca.json, in walk order: Cedar of Lebanon, redwood and ginkgo
in the Orto Botanico, Monterey cypress on the San Regolo bastion above it, Atlas cedar at Villa
Bottini, holm oaks on the Torre Guinigi. Total walk about 800 m, entirely inside the walls.
Three flagged (cypress and Villa Bottini cedar on age, Guinigi oaks on age).
Three photos, all Wikimedia Commons, all viewed before approval; the ginkgo, the cypress and the
Villa Bottini cedar have honest gaps. Everything not published is in data/leads/lucca.json:
10 leads and 5 blocked.

Renumbering note: the file order is the walk order, so the ids do not match the order in which they
were verified above. luc_004 in the final file is the Monterey cypress, luc_005 the Guinigi oaks,
luc_006 the Villa Bottini cedar.

Corrections found along the way, worth keeping:
- turismo.lucca.it prints the Cedar of Lebanon at "5.76 m diameter". That is a diameter/girth error AND
  it is the sequoia's girth figure from the register. Register measurement used.
- Ginkgo: the garden itself dates the lightning strike to the post-war years, not to 1950 exactly.
  Earlier draft said "around 1950" on the strength of a search snippet; corrected against the garden.
- 36 register entries for the comune against 52 monumental trees in a municipal census reported by
  quinewslucca.it. Not reconciled. Never quote either as a count of what exists.
