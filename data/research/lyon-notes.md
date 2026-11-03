
## 2026-11-02 parks and gardens pass (Lyon, verify agent)

- Method: the Metropole de Lyon open street-tree inventory (WFS layer abr_arbres_alignement.abrarbre, 112,439 trees, Licence Ouverte) queried for circonference_cm >= 300 (417 rows). It also contains park trees managed by the Metropole ("Espace vert"), but NOT the Ville de Lyon's own parks: Tete d'Or, Gerland, Jardin des Plantes trees are not in it. Delivered 10 trees to data/research/lyon-verified-parks.json (all confirmed pins from surveyed points, all flagged register only).
- Tete d'Or: the Archives municipales de Lyon children's document (perisco_arbres.pdf) says 8,800 trees, planes of 40 m, Cedars of Lebanon, tulip trees, ginkgos, bald cypresses; no individual specimen is named or measured. The city's walking guide to remarkable trees exists (Felicien Lesec, Altissima; trail booklet at the park reception) but its content is not online. No new Tete d'Or tree can be verified without it. Four are already live.
- The Metropole "Au fil des arbres" guides (Lyon 2 Carnot, Lyon 8, Croix-Rousse, Bron, Tassin cedars, Villeurbanne Tonkin) are species-level: no specimen ages or girths. Only the Bron guide names a specific tree (stop 23, cedar on Place Weingarten).
- Inventory planting years are estimates (round decades, 1850, 1900) and often inconsistent with girth (a 545 cm plane "planted 1950"); never used as ages.
- Hosts: overpass-api.de refused connection and overpass.kumi.systems timed out (OSM natural=tree check not done). Commons geosearch returns 429 after about 5 quick calls. Commons has no trunk-level photographs near any delivered tree.
- Not covered for lack of a verifiable named tree: Parilly, Lacroix-Laval, Feyssine, Blandan, Loyasse, Guillotiere cemetery, Saint-Martin d'Ainay, Ile Barbe church precinct, Jardin du Rosaire. Next step if wanted: the Ville de Lyon park tree inventory (ask the city or its data portal) and the Tete d'Or booklet.

# Lyon PLU-H register pass 2026-11-02 (verify agent)
- Overpass blocked (406/timeouts); OSM natural=tree check impossible, so no pin is confirmed. Commons geosearch, iNaturalist API and Panoramax API (api.panoramax.xyz, no token) all answered.
- Panoramax gives dated street imagery within 60 m (life trace of the place, not of the trunk); one viewed frame (Chemin Ferrand) showed a lane with mixed trees, nothing identifiable.
- No tree-specific Commons photographs found near any candidate; iNaturalist had no matching genus observation within 15 m of any.
- 12 entries delivered to data/research/lyon-verified-register.json, all approximate and flagged; France covered-country gate (photo or confirmed pin) unmet, so dispatcher decides. Strongest: Square Ferrié (7 register rows, public square), Quai Clemenceau planes (more than 30 m, over 150 years), Square de Villevert cedar cluster (Albigny-sur-Saône) with 5 more Atlas cedars on the quay.
- Most UNC register rows are private plots or residences and were skipped, not logged.
