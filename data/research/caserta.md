# Caserta, Italy — research pass 2026-08-05

## Sources
1. MASAF national register of monumental trees (CC BY 4.0), 51 entries for comune Caserta.
   Local copy: data/registers/italy-masaf.json, sheet ids nn/B963/CE/15. Girth + height + coords, NO age.
2. Campania regional register of monumental trees (L.R. 2016), per-tree cards at
   https://agricoltura.regione.campania.it/foreste/monum/scheda_NNN.html — gives eta presunta (age),
   own GPS, and a description. Independent publication, but the girth figures match MASAF exactly,
   so the two share a measurement lineage: corroboration is strongest on existence/species/place,
   and age comes from the regional card alone.
3. Reggia di Caserta official site (reggiadicaserta.cultura.gov.it) for the English Garden history,
   the 2021 monumental-tree recognition, and ticketing.

## Register traps checked
- Girth is cm in both registers. 775 cm = 7.75 m: physically plausible for a broad old cedar. OK.
- MASAF lists the Osmanthus at 650 cm flat. The regional card qualifies it: "650 cm (insieme dei
  fusti)" = the stems added together, not one trunk. MASAF's number alone would have been wrong.
  Same qualifier on all "insieme omogeneo" entries, which are stands/avenues, not single trees.
- Ages are "eta presunta" as recorded at the 2020 card update, so 200 anni = about 200 years, and
  ">150" is a floor, not a figure. Written as such.
- Coordinates disagree between the two registers for the same tree (Cedrus libani 464 cm:
  MASAF 41.095917,14.331278 vs Campania 41.0975,14.33103, ~180 m apart), and several MASAF entries
  share one identical coordinate (41.093339,14.330278 is given for the 775 cm cedar, the sequoia,
  the zelkova and a plane). Neither register places the trunk. => location_precision "approximate"
  for every tree on this page. Do not mark confirmed.
- 51 register entries for the comune, of which 8 are "insieme omogeneo" (stands/avenues). Never
  quote 51 as a count of monumental trees in Caserta.

## Cluster
Two knots inside the Parco Reale:
- KNOT A "il Palco", flat ground south of the lake in the English Garden, 41.0926-41.0934 /
  14.3296-14.3306. Roughly 15 registered single trees inside ~150 m. This is the walk.
- KNOT B, upper English Garden by the Bagno di Venere and the lake, 41.0955-41.0978 /
  14.3303-14.3320. ~600 m further north.
Everything else (Cimitero Comunale, Piazza Vanvitelli, San Leucio, Briano, Casola, Centurano) is
1-3 km away and outside the park: different walk, not this cluster.

## Verified trees (appended as completed)

PUBLISHED (7), all in the English Garden, all location_precision "approximate":
1. cas_001 Cedar of Lebanon, 775 cm / 16 m, >150 yrs. MASAF 18/B963 + scheda 213.
   Thickest trunk in the whole Caserta register.
2. cas_002 London Plane "that grew sideways", 260 cm / 9 m, crown 25 m, >150 yrs.
   MASAF 21/B963 + scheda 216. Below the 4 m species threshold and registered anyway; the
   regional card calls it among the most beautiful and most photographed in the garden.
   best_time: bare silhouette, Jan-Feb.
3. cas_003 European Yew of the Bagno di Venere, 392 cm / 20 m. MASAF 34/B963 + scheda 245
   + the Reggia's own Bath of Venus page (genuine third-party corroboration: "the waters
   surrounding it spring from the base of a monumental Yew tree"). FLAGGED on age: the card's
   age field says 150 but its text says the tree was already adult when placed here in the
   1790s. Set as oldest_tree_id, with the contradiction stated on the page.
4. cas_004 Douglas Fir, 580 cm / 40 m. MASAF 12/B963 + scheda 185. FLAGGED on age: 200 years
   dates the planting to ~1826, and Douglas's first seed reached Europe in 1827.
5. cas_005 Sweet Osmanthus, 650 cm / 10 m. MASAF 42/B963 + scheda 269. Register trap caught:
   MASAF prints 650 cm as girth, the regional card qualifies it "insieme dei fusti", stems
   combined. best_time: flowers, Sep-Oct.
6. cas_006 Camphor, 370 cm / 38 m, ~200 yrs. MASAF 26/B963 + scheda 237. Located by the card
   to "il Palco o prateria bassa, a sud-est, lato Puccianiello".
7. cas_007 Cork Oak, 420 cm / 28 m, >150 yrs. MASAF 23/B963 + scheda 218. Card notes smaller
   cork oaks self-seeded around it.

NOT PUBLISHED: 39 leads + 5 blocked in data/leads/caserta.json.
Headline calls:
- Monterey Cypress (485 cm) pulled to leads. A monumental Cupressus macrocarpa in this same
  English Garden fell in the December 2019 storms; the Reggia says four other specimens remain.
  Neither register has a vitality field, so I cannot tell whether the registered tree is the
  one that fell.
- Cephalotaxus fortunei (450 cm / 25 m) pulled to leads: those figures are far outside the
  species' normal range and look like a register error or a misidentification.
- Phillyrea latifolia (420 cm) same doubt, and its regional card carries the holm-oak stand's
  coordinate from 2 km away.
- Zelkova pulled: MASAF says carpinifolia, the regional card says "serrata / carpinifolia".
  Species must be settled for hard rule 9.
- Maclura "sdraiata" pulled: the girth field literally reads "lying down". Alive? Unknown.
- 5 blocked, all non-collectible groups: 8-camphor row, 25 holm oaks, Castelluccia magnolia
  stand, 3 Italian cypresses, cemetery cypress group.

PHOTOS: none. Commons has no identified portrait of any of these trees. The only near-misses
are Bath of Venus shots (CC BY-SA 4.0), and both were viewed: the subject is the marble Venus
and the grotto, not a tree, so they fail the Cadiz standard. Honest gap.

ACCESS: paid. Royal Park + English Garden ticket 9 EUR (+1 EUR online); a 3 EUR park-only
ticket exists but excludes the English Garden. Closed Tuesdays. The garden is ~2.5 km up the
axis from the palace gate; a paid electric shuttle runs the length.
