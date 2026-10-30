# Paris east batch, verify pass 2026-10-30

Candidates: 22 rows in data/research/paris-top40-candidates.json with batch "east" (21 distinct trees; register 2002365 appears twice). Folded into 14 collectible points: 8 delivered (par_038 to par_045), 6 register-only approximate points kept as leads, plus 2 extra leads found on the way.

Sources used: Ville de Paris register (open data, one source); paris.fr park and square pages (Buttes-Chaumont, Square Carnot, Ile de Bercy, Pere Lachaise faune et flore); Ville de Paris "arbres remarquables" tree sheets (cdn.paris.fr PDFs of 2019/07/24, black walnut sheet and island sheets); OSM natural=tree nodes via Nominatim reverse (Overpass is dead from here); lifecheck.py (iNaturalist observations near each point: not tree-specific).

Findings
- OSM tree nodes sit on the register points of: Square Carnot planes and weeping beech, Ile de Bercy planes (3 of 5), Bercy park plane, Chapeau rouge ash. Those pins are confirmed. All other register points land on paths or lawn: approximate.
- Species conflicts: Buttes-Chaumont planes (register x hispanica, paris.fr feature orientalis); Pere Lachaise cedar (register Cedrus atlantica, paris.fr libani). Girth differences are measurement dates.
- Ensembles: Buttes-Chaumont 3 planes = 1 entry; Square Carnot twin planes = 1 entry, weeping beech 55 m away = own entry (foldable); Ile de Bercy 5 planes = 1 entry (island is the destination).
- Register-only entries are flagged. Oaks (1815 Fort Neuf, 1784 Minimes), Gravelle cedar, Vaillant plane and two Daumesnil planes are leads: no second source, no pin evidence.
- paris.fr hours table read: Buttes-Chaumont 7:00 to 20:00 now (later in summer); Square Carnot 24/24; Ile de Bercy closed from noon on 31 Oct 2026 for events. Parc floral (paid) is not involved in this batch: none of the east candidates stands inside it.
- Hosts: no new hang. cdn.paris.fr PDFs fetch fine (use pypdf, pdftotext absent). Several paris.fr /lieux/ ids guessed from memory 404; use the search result URLs.
- Search summaries were used only as pointers; every figure recorded was seen on a fetched page or PDF.
