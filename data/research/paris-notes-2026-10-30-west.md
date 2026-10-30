# Paris west batch, verification notes, 2026-10-30

Delivery: data/research/paris-verified-west.json (14 trees, par_061 to par_074). Rejects: four leads appended to data/leads/paris.json.

## Method and sources
- Open register: opendata.paris.fr dataset arbresremarquablesparis (183 rows, queried by idbase). Its planting field uses 1700-01-01 as "unknown".
- The city's own printed fact sheet per tree: https://capgeo.sig.paris.fr/PdfEtImages/ArbresRemarquables/PDF/<id>.pdf (works with curl, 135397 returns HTTP 500; its sheet is 135378.pdf, which covers a pair of Batignolles planes). Sheets carry planting years the open data lacks, and slightly different girths and heights (older or newer survey, not stated). Both figures are in verify_notes; girth_cm is the open-data figure.
- Brochure of the city's 2015 A.R.B.R.E.S. label and Bagatelle: https://cdn.paris.fr/paris/2022/03/17/1a401337e814deb12f69b7a7506d272c.pdf (2019 version c993cac3... also exists).
- paris.fr Bagatelle and Batignolles pages (hours, fees), paris.fr "A l'ombre des plus beaux arbres du bois de Boulogne" page (Grande Cascade cedar, Bagatelle planes).
- Alive: scripts/lifecheck.py; it finds any iNaturalist or Commons item within a radius, so it is area evidence, never tree-specific. Ranelagh walnut and the Tir aux Pigeons catalpa had NONE.

## Decisions
- Ensembles: none folded. Pairs at Batignolles (68 m), Auteuil (80 m) and Bagatelle (125 m) are different species or trunks, one entry each; the two Avenue Foch planes are 650 m apart.
- Pins: "confirmed" where the register point is corroborated or the specimen is alone in its species in a small garden (Champ de Mars by the Waymarking coordinate 20 m away, Batignolles wingnut, both Auteuil trees, Bagatelle sequoia near the Pagoda per a Commons geotag and paris.fr). Group or row trees stay "approximate".
- Age doubts for the writer: Bagatelle sequoia dated 1850 by the city although the species reached Europe only in 1853 to 1854 (general knowledge, not checked on a page); Batignolles plane 1850 vs 1840 in the sheet; Auteuil ginkgo 1895 predates the garden's 1898 creation; Louise Michel walnut 1900 vs the square's later layout (not checked). Do not bridge any of these.
- Cedar species conflict (atlantica in inventory, libani on label, sheet and paris.fr).
- Champ de Mars plane: sheet says "au bord de l'eau", a pond lies at the tower base (unchecked). 2022 activist plane (208 years, planted 1814) is not tied to this trunk by any source.

## Not delivered
- Avenue Foch planes 111331 and 114166, row trees, no way to tell apart (leads).
- Montsouris plane 112897, planted 1935 by the sheet (lead).
- Tir aux Pigeons catalpa 2009236, no alive evidence, access unclear (lead).

## Hosts
- capgeo.sig.paris.fr works (one HTTP 500 on 135397.pdf). paris.fr/lieux/jardin-des-serres-d-auteuil-1822 is a 404, the real slug is 1780. No hanging host met. Overpass not tried (dead per the brief).
