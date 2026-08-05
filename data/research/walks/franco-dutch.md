# Published tree walks and tree-by-tree lists: France, Belgium, Netherlands

Scouting sweep, 2026-08-05. URLs only, no text or images copied.

## Paris
- Route exists: YES (and better: an official designation dataset AND a published walk)
- URL(s):
  - Open data: https://opendata.paris.fr/explore/dataset/arbresremarquablesparis/ (API: https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/arbresremarquablesparis/records)
  - Official interactive map linked from https://www.paris.fr/pages/l-arbre-a-paris-199 (ArcGIS experience viewer)
  - Published walking route: https://www.paris.fr/pages/promenez-vous-parmi-les-arbres-au-coeur-de-paris-20627
  - Photo feature: https://www.paris.fr/photos/13-arbres-classes-remarquables-25
  - Jardin des Plantes own list: https://www.jardindesplantesdeparis.fr/fr/arbres-remarquables
  - A.R.B.R.E.S. label + Metropole du Grand Paris map/routes (138 labelled trees in Grand Paris): https://www.enlargeyourparis.fr/balades/arbres-remarquables
- Publisher: city (Direction des Espaces Verts et de l'Environnement, Ville de Paris) for the dataset and the walk; national NGO A.R.B.R.E.S. for the label layer; museum for Jardin des Plantes
- Coverage: GOLD. 185 records, verified live via the API on 2026-08-05. Every tree is named individually and carries: common name (com_nom_usuel, e.g. "Arbre aux quarante ecus"), Latin name (com_nom_latin), planting year (com_annee_plantation, often "Inconnue"), street address (com_adresse), arrondissement, girth in cm, height in m, lat/lon point coordinates, a prose summary and descriptive field (com_resume, com_descriptif), the council deliberation number and date that designated it, the A.R.B.R.E.S. label year where applicable, plus com_url_pdf, com_url_photo1 and com_copyright1. This is not a "admire the old trees" article; it is per-tree with coordinates. The paris.fr walk is the separate, softer thing: one day-long route from Place des Vosges to Square Rene-Viviani naming about six stops (Place des Vosges limes and horse chestnuts, rue des Rosiers Indian lilacs, Place Saint-Gervais elm, Ile Saint-Louis poplars, Square Jean-XXIII tamarisks and silk floss tree, Square Rene-Viviani robinia dated 1601), some of which are groups rather than single collectible points.
- Walkable: the dataset is city-wide, so cluster it with scripts/cluster_register.py. The paris.fr walk itself is one afternoon on foot across the Marais / Ile de la Cite / Latin Quarter.
- Official designation list rather than a tourist article? YES. Designation is by council deliberation (com_delib_num / com_delib_date), and a second, independent designation layer exists via the A.R.B.R.E.S. national label.
- Licence: Open Database License (ODbL), stated in the dataset metadata (license_url http://opendatacommons.org/licenses/odbl/). Attribution + share-alike on derived databases; no non-commercial clause. Note com_copyright1 governs the photos separately, check per photo.
- Judgement: the single best French source found, and it makes a Paris pass close to free: designation, species, girth, planting year and coordinates in one API call, with the paris.fr walk usable as the independent second source for the trees along it and A.R.B.R.E.S. as the second source for the labelled ones. Easily 10 trees surviving a two-source bar, probably 40+; the real work becomes choosing a walkable cluster, not finding trees. Last modified 2026-07-31, so it is maintained.

## Brussels
- Route exists: YES, three separate usable things: a regional designation inventory, a CC BY open dataset, and actual published named walks
- URL(s):
  - Open data (City of Brussels commune only): https://opendata.brussels.be/explore/dataset/bruxelles_arbres_remarquables/ (API: https://opendata.brussels.be/api/explore/v2.1/catalog/datasets/bruxelles_arbres_remarquables/records)
  - Regional inventory, per-tree pages: https://sites.heritage.brussels/fr/inventaire/ and https://sites.heritage.brussels/index.php?section=trees&lg=fr ; individual trees resolve at https://sites.heritage.brussels/fr/trees/[id] (NL: /nl/trees/[id])
  - Legal inventory list: https://erfgoed.brussels/links/inventarissen/lijst-wettelijke-inventaris-opmerkelijke-bomen/view
  - Background article: https://patrimoine.brussels/decouvrir/publications/notre-revue-par-article/no-9-parcs-et-jardins/l2019inventaire-des-arbres-remarquables
  - Ixelles commune, three published tree walks: https://www.ixelles.be/site/878-Les-balades-des-arbres-remarquables
  - The walks themselves (Wood Wide Web): https://www.woodwideweb.be/fr/walk/6.html (Etangs d'Ixelles), /7.html, /8.html (Boondael, Tenbosch-Lepoutre); atlas: https://www.woodwideweb.be/fr/atlas.html
  - Bruxelles Environnement guided-walk agenda and dossier: https://environnement.brussels/blog-citoyen/dossiers/arbres-remarquables-la-rencontre-des-geants-verts-de-bruxelles
- Publisher: region (Direction du Patrimoine culturel, Bruxelles Urbanisme et Patrimoine / heritage.brussels) for the inventory and the dataset; commune (Ixelles) plus NGO (32shoot asbl / Wood Wide Web) for the walks; region (Bruxelles Environnement) for guided walks
- Coverage: GOLD for the register, SILVER for the walks.
  - Dataset verified live 2026-08-05: 582 records, each with French, Dutch and Latin name, legal status ("Inscrit a l'inventaire legal"), rarity flag, trunk circumference in METRES (note the units trap: values read 3.16, 5.11), crown diameter, a photo URL on heritage.brussels, a per-tree page URL in both languages, and a lat/lon point. No age or planting year field, so age is the one thing a research pass still has to source elsewhere.
  - The regional inventory behind it is much larger: roughly 5,150 trees surveyed since 2002, about 7,500 in the database, about 3,500 on the legal inventory across all 19 communes. The 582 in open data are the City of Brussels commune only.
  - Ixelles walks: three routes, 10 individually named trees each, each with a species (common + Latin) and a street address, plus per-tree information sheets, published in FR, NL and EN. Named-tree-with-location kind, not the worthless kind. No age or girth on the walk pages.
  - Wood Wide Web atlas: about 120 geolocated remarkable trees in Brussels with narrative portraits; collaborative, so treat as a lead source not a register.
- Walkable: the Ixelles walks are explicitly one afternoon, roughly 30 minutes of total walking between 10 stops. The open dataset is commune-wide and needs clustering.
- Official designation list rather than a tourist article? YES for the inventory and the dataset (legal inventory status per tree). The Ixelles walks are official-commune but curated, not a designation list.
- Licence: CC BY 4.0, stated in the opendata.brussels metadata (https://creativecommons.org/licenses/by/4.0/deed.fr), publisher heritage.brussels, last modified 2026-08-05. Fully compatible with our reuse bar. Wood Wide Web states no licence, only "(c) 32shoot asbl" , cite, never copy. The heritage.brussels photo URLs are NOT covered by the CC BY on the dataset by default; check each before using.
- Judgement: makes a Brussels pass cheap. Register plus an independent commune-published walk means two-source verification is basically free for the Ixelles trees, and the legal-inventory status is a strong designation signal for the rest. Easily 10 trees surviving a two-source bar; the Ixelles Etangs route alone is a ready-made walkable cluster. The gap to fill by hand is AGE, which neither the dataset nor the walks carry. Note sites.heritage.brussels returns 403 to plain fetching; use the opendata API instead.

## Amsterdam
- Route exists: YES, a real published walking booklet, free, and in a 2025 edition
- URL(s):
  - Free PDF, verified downloadable 2026-08-05 (HTTP 200, 5.1 MB, 40 pages): https://www.bomenstichting.nl/images/1808/Monumentale_bomen_Amsterdam.pdf
  - Its landing page: https://www.bomenstichting.nl/winkel/boeken-en-brochures/langs-monumentale-bomen-in-het-centrum-van-amsterdam.html
  - City map of monumental and valuable trees: https://maps.amsterdam.nl/bomen_bijzonder/ (HTTP 200) and https://maps.amsterdam.nl/bomen/
  - Amsterdam-Noord audio route "Reuzen van Noord" (Tolhuistuin, GPS app): https://www.rodi.nl/amsterdam-noord/205841/audioroute-langs-monumentale-bomen
  - Bomenroute De Pijp: https://www.wandelzoekpagina.nl/bomenroutes/depijp.php
  - Tuinpark Ons Buiten walk: http://www.ons-buiten.nl/bezoekers/wandeltuin/wandeltuin.html
- Publisher: NGO (de Bomenstichting) in collaboration with the Gemeente Amsterdam; city for the maps
- Coverage: STRONG but with one caveat. "Langs monumentale bomen in het centrum van Amsterdam" is the 7th revised edition, 2025, selecting 30 monumental trees in the centre out of the 257 Amsterdam has on the national monumental-tree register. It is the named-tree-with-location kind. CAVEAT verified this run: the Amsterdam PDF has NO extractable text layer (pypdf returns empty strings on every page), so a run must read it as images or transcribe by eye. Its sister booklet for Utrecht, same publisher and format, DOES extract, and its per-tree entries carry: Dutch name, Latin name, PLANTJAAR (planting year, e.g. 1840, 1870, 1900), the location by bastion or street, the city tree-map id number, and a short prose paragraph. Assume the Amsterdam booklet follows that format.
- Walkable: one afternoon, city centre. (The Utrecht sibling is an explicit 5 km loop; the Amsterdam one is a centre walk of the same shape.)
- Official designation list rather than a tourist article? Partly. The booklet is a curated NGO+city walk, not a designation list. The designation layer is separate: the Landelijk Register van Monumentale Bomen (monumentalebomen.nl) and the city's own bijzondere-bomen map.
- Licence: none stated on the free PDF. maps.amsterdam.nl carries the city's usual open terms but they are not asserted on the page itself, so check before importing. REMEMBER the standing constraint in CLAUDE.md: the NL national register is CC-BY-NC and stays a lead list, never an import.
- Judgement: Amsterdam is already published in our data, so the value here is backfill: the booklet is an independent second source with a planting year for around 30 centre trees, which is exactly the field our NL entries are thinnest on. Would make a re-verification pass cheap. Blocked only by needing eyes on the PDF rather than a parser.

## BONUS: the Netherlands-wide index of published tree routes
Not a city block, but the highest-value single find of this sweep for NL and worth its own note.

de Bomenstichting maintains a national index of published walking and cycling routes along monumental trees, at
https://www.bomenstichting.nl/bomen-in-uw-buurt/wandelen-en-fietsen-langs-monumentale-bomen.html

Cities listed there, with our own coverage status in brackets:
- Amsterdam (published), free PDF above
- Breda (published): https://degoudencirkelbreda.nl/wp-content/uploads/Langs-monumentale-bomen-in-Breda.pdf
- Delft (published): book "Langs bijzondere Delftse bomen", http://www.eburon.nl/langs_bijzondere_delftse_bomen (paid book, not a free source)
- Den Haag (published): book "Langs Haagse bomen", http://www.eburon.nl/langs_haagse_bomen (paid book)
- 's-Hertogenbosch (published as den-bosch): https://www.boomenbosch.nl/?pid=3
- Rotterdam (published): https://www.rotterdam.nl/bomenroute , an augmented-reality route over about twenty monumental and special trees; the page itself does not list them, so the trees must be dug out of the linked "Monumentale bomen" pages
- Utrecht (published): https://www.bomenstichting.nl/images/1808pdf/Langs_monumentale_bomen_Utrecht_LR.pdf , VERIFIED GOLD this run: 21 pages, a 5 km route through the Zocherpark-Singel ring, 30 individually described trees, each with Dutch and Latin name, planting year, location and the city tree-map id. Also on izi.TRAVEL and in the IVN Route app. Made with IVN, Gilde Utrecht, gemeente Utrecht and the Bomenstichting.
- Dordrecht (not covered): https://www.bomenstichting.nl/images/1808pdf/boekje_Monumentale_bomen_Dordrecht.pdf
- Hengelo (not covered): https://www.bomenstichting.nl/images/1808pdf/fietsroute-monumentale-bomen-Hengelo.pdf (cycling)
- Enschede (not covered): two cycling routes, docplayer copies only
- Maassluis (not covered): https://bomenvanmaassluis.nl/
- Dronten (not covered): https://www.dronterland.nl/bezoeken/bomenroute
- Also Den Ham, Vorden, Weert, Zwolle: small places, several offline-only or paid

Judgement: this single page is the cheapest second-source generator we have found for the Netherlands. The free PDFs (Utrecht, Breda, Dordrecht, Hengelo, Amsterdam) are per-tree with species, place and often planting year, which is the exact shape that turns an NL verification pass from an hour into minutes. The paid Eburon books for Delft and Den Haag are NOT usable as a source. Dordrecht is the only non-covered city here with a free per-tree PDF and enough size to earn a page.

## Lyon
- Route exists: WEAK. A designation layer and a journalist's map, but no published tree-by-tree walking route by the city.
- URL(s):
  - Ville de Lyon page (403 to plain fetching, opens in a browser): https://www.lyon.fr/actualite/nature-en-ville/les-arbres-remarquables-de-lyon , mirrored on every arrondissement mairie site, e.g. https://mairie6.lyon.fr/actualite/nature-en-ville/les-arbres-remarquables-de-lyon
  - City press PDF on the 2024 A.R.B.R.E.S. labelling: https://www.lyon.fr/sites/lyonfr/files/content/documents/2024-11/16-10%20-%20Label%20arbres%20remarquables%20-%20la%20Ville%20de%20Lyon%20recompensee%20pour%20la%20richesse%20de%20son%20patrimoine%20arbore.PDF (accent-encoded in the original URL)
  - A.R.B.R.E.S. association on the Tete d'Or labelling: https://www.arbres.org/la-dda-a-lyon-et-labellisation-du-parc-de-la-tete-d-or.htm
  - PLU-H point prescription "espace boise classe ponctuel / arbre remarquable", Metropole de Lyon: https://data.grandlyon.com/portail/fr/jeux-de-donnees/prescriptions-relatives-a-qualite-cadre-vie-espace-boise-classe-ponctuel-arbre-remarquable-plu-h-m/info
  - Journalist-built map of Grand Lyon remarkable trees: https://www.mediacites.fr/decryptage/lyon/2025/08/26/cedre-tilleul-tulipier-a-la-recherche-des-arbres-remarquables-du-grand-lyon/ (paywalled press, use as a lead only)
- Publisher: city (Ville de Lyon), metropolis (data.grandlyon.com, PLU-H), national NGO (A.R.B.R.E.S.), press (Mediacites)
- Coverage: MIXED. The city says it has identified roughly fifty exceptional trees across its arboreal heritage, and in October 2024 four were given the national "Arbre Remarquable de France" label, each named individually with species and park: a Pin de Bunge in Parc de la Tete d'Or, a horse chestnut in Parc de la Garde (5e), a Japanese pagoda tree in Parc de Gerland (7e), a Cedar of the Atlas in Parc de la Chapelle (9e). Parc de la Tete d'Or itself carries the "ensemble arbore remarquable" label. That is four named trees plus a park, not a list of fifty; the fifty is asserted, not published tree by tree in any page found this run. The PLU-H layer gives designated points but is a planning prescription, so expect coordinates without species or age.
- Walkable: no. The four labelled trees are in four parks spread across the city, which is exactly the Kyoto failure mode.
- Official designation list rather than a tourist article? Partly: the A.R.B.R.E.S. label and the PLU-H prescription are official designations; there is no published city inventory page.
- Licence: data.grandlyon.com serves under Licence Ouverte for most layers (not verified per-layer this run; the catalog API path used for Bordeaux returned 404 on Grand Lyon, so a different endpoint is needed). Mediacites is paywalled press, not a licence.
- Judgement: would NOT make a Lyon pass cheap. Lyon is already published in our data, and this sweep found no second source that hands over species, age and place together. The four 2024-labelled trees are worth adding or verifying because A.R.B.R.E.S. is a clean independent second source, but a wholesale Lyon backfill still needs ordinary research. Perhaps 4 to 6 trees would survive a two-source bar off these sources alone.

## Marseille
- Route exists: NO.
- URL(s): open data portal searched, https://data.ampmetropole.fr , API query for "arbre" returns 0 datasets (verified 2026-08-05). Only park and garden polygons exist: https://data.ampmetropole.fr/explore/dataset/parc-et-jardin-bd-topo-zone-dactivite-ou-dinteret/
- Publisher: n/a
- Coverage: nothing. No municipal remarkable-tree list, no published route, no tree-by-tree page found. Searching found only Wikipedia articles on individual parks (Parc Borely, Parc du 26e Centenaire), which name the park and not its trees.
- Walkable: n/a
- Official designation list rather than a tourist article? No list of either kind.
- Licence: n/a
- Judgement: a Marseille pass gets NO help from a published route or register. It would be ordinary city-by-city research, park list first per the Step 1 method. Recording this as a genuine blank so the next run does not repeat the search. The remaining untried angle is the A.R.B.R.E.S. national label filtered to Bouches-du-Rhone on arbres.org, which this sweep did not have time to check.

## Bordeaux
- Route exists: NO route, but a large official designation layer with a fatal gap.
- URL(s):
  - PLUi point prescriptions, contains "Arbre isole remarquable": https://opendata.bordeaux-metropole.fr/explore/dataset/p_presc_p/ (API verified 2026-08-05)
  - Full municipal tree inventory, 79,796 trees: https://opendata.bordeaux-metropole.fr/explore/dataset/ec_arbre_p/
  - Portal landing page on the tree heritage: https://opendata.bordeaux-metropole.fr/pages/patrimoine-arbore-bordeaux/
- Publisher: metropolis (Bordeaux Metropole)
- Coverage: 1,763 records in p_presc_p match "arbre", labelled "Arbre isole remarquable", each with lat/lon, an ident, a validity date and a link to the PLUi regulation PDF. VERIFIED THIS RUN. The fatal gap: the records carry NO species, NO name, NO age, NO girth. It is a planning designation and a dot, nothing more. ec_arbre_p is the full 79,796-tree street inventory, which hard-rule territory in CLAUDE.md excludes from the register layer outright (never bulk municipal inventories, only what a register itself designates as remarkable).
- Walkable: 1,763 points across the whole metropolis of 28 communes, so clustering is possible but meaningless without knowing which tree is which.
- Official designation list rather than a tourist article? YES, it is a legal PLUi designation. But a designation without attributes.
- Licence: Licence Ouverte (Etalab), stated in the dataset metadata. Compatible with our reuse bar.
- Judgement: does NOT make a Bordeaux pass cheap for curated pages, because a pin with no species and no age fails our bar on its own and gives a second source for nothing. It is genuinely interesting for the LAYER-2 register track though: an officially designated, openly licensed, coordinate-bearing set of 1,763 remarkable trees, which is exactly what layer 2 is for, as long as the dot honestly says "designated in the PLUi, unverified by us" and carries no species claim. Worth logging in OPEN_DATA_SURVEY.md. Same pattern probably repeats in every French metropolis with a PLUi in ODS format, including Lyon's PLU-H, so this is a France-wide lead, not a Bordeaux one.

## Not reached
Not covered in this sweep: no city on the brief was skipped. Paris, Brussels, Amsterdam, Lyon, Marseille and Bordeaux were all checked. Untried angles left for a later run: the A.R.B.R.E.S. national label list on arbres.org filtered by departement (would give named, labelled trees for Marseille, Lyon, Bordeaux and every other French city in one place), the Grand Lyon data API on its correct endpoint, and the 18 Brussels communes outside the Ville de Bruxelles that are in the regional inventory but not in the open dataset.
