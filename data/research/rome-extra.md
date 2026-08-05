# Rome, deepening pass (2026-08-05)

Adding to the ten already published in data/cities/rome.json. Ids continue at rom_011.
Goal: thicken the existing walks, not scatter.

## Source question answered first: does Lazio publish per-tree cards like Campania?

**No.** Checked 2026-08-05:

- `dati.lazio.it` dataset "Elenco alberi monumentali della Regione Lazio": a shapefile plus PDF verbali of the regional commission. No per-tree HTML card.
- `regione.lazio.it/cittadini/agricoltura/foreste/alberi-monumentali`: one xlsx,
  https://www.regione.lazio.it/sites/default/files/2025-11/Elenco-alberi-monumentali.xlsx (Nov 2025, 212 trees in Lazio, 65 in comune di Roma).
- `comune.roma.it` INF208568: links three PDFs, no per-tree data.

**But the Lazio xlsx is worth more than MASAF for Italian work, for three reasons:**

1. It carries the **monumentality criteria per tree** (a = age/size, b = form and bearing, c = ecological value, d = botanical rarity, e = vegetal architecture, f = landscape value, g = historical/cultural/religious value). MASAF drops this. It tells you *why* a tree was designated, which is exactly what a story needs and what separates a genuinely remarkable tree from a merely large one.
2. It carries a **NOTE column** with real content: which trees are policormico (multi-stemmed, so the girth column is a list of stems, not one trunk), which coordinates were corrected and when, and per-tree events (e.g. sheet 60/H501, the Pioppo del Risaro, "nel 2025 ha subito un incendio").
3. **Sheet 2 is "Alberi monumentali eliminati"**, the removed list, with the reason. This is the vitality layer no national register has. Five Roma trees are on it, all "Albero morto", including 18/H501 Pino domestico at Villa Torlonia. Region-wide, 17 removed as dead.

Neither register has an age field. Age in Rome therefore stays the expensive part, exactly as in Naples and Caserta. Where no documented planting date exists, entries below say so instead of inventing one, following the precedent already set by rom_008 and rom_009.

Second source used repeatedly below: Roma Capitale's own municipal page NWS1195295, which walks the city's monumental trees one at a time and is independent of the register in authorship though not in designation.

## Register vs our published pins

All ten published Rome trees checked against the 65 MASAF entries in the comune. **No pin disagrees by more than 50 m.** Detail in the report.

---

## VERIFIED, SHIPPING

### rom_011 Himalayan Cedar, Villa Sciarra (Istituto Italiano di Studi Germanici)
41.883386, 12.464731 | Lazio sheet 10/H501/RM/12 | girth conflict: MASAF 500 cm vs Lazio regional 330 cm, height 20 m
Criteria: a) age/size, b) form and bearing, e) **vegetal architecture** (one of only two Roma trees given that criterion)
Sources: Lazio regional register + comune.roma.it NWS1195295 ("Cedar of the Himalayas, Institut of German Studies, selected for bearing and importance in the architectural project") + abitarearoma.it
Age: undocumented. Wurts planting era (1902-1928) is the documented context, not a dated record. FLAGGED.
Access: free, Villa Sciarra public park. 130 m from rom_001.

### rom_012 Podocarp, Villa Sciarra
41.883350, 12.463692 | Lazio sheet 09/H501/RM/12 | 200 cm girth, 18 m
Criteria: **d) botanical rarity only.** The register designated it for rarity, not size or age, and the entry says so.
Sources: Lazio register + comune.roma.it NWS1195295 ("a splendid and enormous Podocarpus") + abitarearoma.it ("raro esemplare di Podocarpo, il pino con cui i buddisti ornavano i loro templi")
Age: undocumented. FLAGGED.
Access: free. 20 m from rom_001, on the same viale.

### rom_013 London Plane, Piazza San Cosimato
41.887222, 12.469639 | Lazio sheet 57/H501/RM/12 | 565 cm girth, 20 m. Largest plane in central Rome's register.
Sources: Lazio register + Il Messaggero, "Piazza San Cosimato, Trastevere adotta il suo platano" + archidiap.com's study of the piazza
Story hook: residents had it tomographed by forest agronomists to check the trunk's internal soundness, and it shades the children's play area.
Age: undocumented; the piazza took its present form in the 1880s. FLAGGED.
Access: free, public square. Links the Villa Sciarra walk to the Orto Botanico walk.

### rom_014 Horse Chestnut, Via delle Tre Pile, Campidoglio
41.893403, 12.482189 | Lazio sheet 01/H501/RM/12 | 345 cm girth, 20 m
Criteria: a) age/size, f) landscape value
Sources: Lazio register + comune.roma.it NWS1195295 (names it on the right of the Cordonata, on via delle Tre Pile)
PHOTO: Commons has a set from Wiki Loves Monuments Italia.
Age: undocumented. FLAGGED. 51 m from rom_010, the ombu on the other side of the same staircase.

### rom_015 Cedar of Lebanon, Villa Borghese, Viale del Lago
41.915147, 12.483475 | Lazio sheet 22/H501/RM/12 | 410 cm girth, 22 m
Sources: Lazio register + comune.roma.it NWS1195295 ("Cedar of Lebanon, Villa Borghese viale del Lago, accompanied by a monumental holm oak")
The municipal page describes it as a pair with our rom_006. 70 m apart.
Age: undocumented. FLAGGED.

### rom_016 Coast Redwood, Villa Borghese, Pincio
41.911639, 12.479611 | Lazio sheet 68/H501/RM/12 | 420 cm girth, 30 m
**SINGLE SOURCE.** No municipal, press or garden-history source names this individual tree; Roma Capitale's monumental-tree page covers only the batch registered up to 2018 and this is sheet 68. Shipped flagged with the uncertainty stated in the story's own last sentences, and pinned `approximate` because nothing independent corroborates the coordinate.
Superlative caught before it shipped: it is NOT the tallest tree on Rome's register. The Aleppo pine at Villa Celimontana, our own rom_009, is 34 m; two more reach 32 m and one 31 m. Written as "among the five tallest" instead.

### Dropped from the shortlist, and why

- **Mediterranean Hackberry pair, Parco degli Scipioni and Viale delle Mura Latine** (66 and 65/H501). Register-only, no second source found. Goes to leads; the pair would make a real two-tree cluster 1.2 km from Villa Celimontana.
- **Southern Magnolia, Via Corsini** (67/H501). 109 m from rom_003, so it would have been the cheapest win of the pass, but the botanical garden's own monumental-tree list does not include it and the address is shared with the Corsini palace grounds. Access unresolved, so leads.
- **Chir Pine, Colle Oppio** (71/H501). The best story in the whole Roman register (brought back from the Himalaya by the Tibetologist Giuseppe Tucci, standing at the garden's 1936 inauguration, roots crushing the Domus Aurea nymphaeum below). Vitality unresolved: 2018 press framing is that the giant was dying and was propagated, and the Domus Aurea garden redesign involves removing exactly these tall trees. Still on the November 2025 active list. Needs its own pass.
- **The four trees at the Semenzaio di San Sisto** (28, 29, 30, 73/H501), 280 m from Villa Celimontana and therefore the obvious thickeners. **Blocked: the nursery is not normally open to the public**, only for occasional booked guided visits. This is the single most useful negative result of the pass, because those coordinates look like an easy urban cluster in any register-first workflow.
- **Cedar of Lebanon and Stone Pine, Villa Torlonia** (19 and 75/H501). The cedar is six metres around, the thickest on Rome's register, and Roma Capitale calls it colossal, so it clears the evidence bar on two sources. Held back only on clustering: 3.5 km out, a new walk rather than a thickened one. Should ship as a Torlonia pair.

---

## Superlative check (hard rule 8)

rome.json already claims: Adonis is "the oldest confirmed tree in the city"; the Valle dei Platani planes are "the only urban stand of ancient oriental planes left in the West"; Rome has "more monumental trees than any other Italian city". Nothing here contradicts those. Two new superlatives are used, both bounded to the register and stated as such: "the thickest plane trunk on Rome's monumental register" (565 cm, checked against all 65 comune entries, next is 553 cm; the larger Valle dei Platani and Fontane Oscure figures are group maxima for a different species) and "among the five tallest trees on the register" for the redwood, after the "tallest" version was checked and found false.

## Counts, for whoever quotes them next

65 register entries in the comune of Roma. That is not a count of monumental trees in Rome: six are groups rather than single trees, 22 stand inside the Tenuta di Castelporziano presidential estate, four are inside a closed municipal nursery, and one more, sheet 18, is dead and on the removal list while still sitting in the national file. rome.json's intro currently says 65 and its FAQ says 65; both are defensible as "registered trees" but neither should ever be phrased as trees a visitor can go and see.
