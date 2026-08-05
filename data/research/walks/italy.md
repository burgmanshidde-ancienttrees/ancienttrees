# Italy scouting sweep: published tree walks and tree-by-tree lists

Scouted 2026-08-05. Searching in Italian. URLs only, no text or images copied.
Structural note for the whole country, established while checking Rome: Italy's
national monumental-tree regime (legge 10/2013, D.M. 23/10/2014) makes every
REGION publish a machine-readable "elenco degli alberi monumentali" with
coordinates. That is a register, not a walk, but it is the cheapest second
source available anywhere in this project so far. Where a region's PDF is
text-layer rather than scanned, it parses in seconds.

## Rome
- Route exists: YES (two published walking itineraries) + GOLD register underneath
- URL(s):
  - Walk article, Roma Capitale's own site, "Passeggiate tra gli alberi secolari" (2023-11-21): https://www.comune.roma.it/web/it/notizia.page?contentId=NWS1110626
  - Companion article "Incontri con gli alberi monumentali, quali sono e dove trovarli": https://www.comune.roma.it/web/it/notizia.page?contentId=NWS1195295
  - Official register landing page: https://www.comune.roma.it/web/it/scheda-servizi.page?contentId=INF208568
  - Lazio regional list, Determinazione G14412 of 03/11/2025 (1.4 MB, 25 pp, TEXT LAYER, parses cleanly): https://www.comune.roma.it/web-resources/cms/documents/QL20250108430ALL_1___APPROV._E_REV._ELENCO_AMI_REGIONALE__DET_G14412___03.11.2025_1.pdf
  - Older 2018 determinazione: https://www.comune.roma.it/web-resources/cms/documents/QL_DD_1495_2018.pdf
  - Tabella (199 KB): https://www.comune.roma.it/web-resources/cms/documents/La_01092025_G11057_Tabella.pdf
  - Elenco_degli_alberi.pdf on the same site is a 5-page SCAN with no text layer, skip it: https://www.comune.roma.it/web-resources/cms/documents/Elenco_degli_alberi.pdf
- Publisher: comune (Roma Capitale, Dipartimento Tutela Ambientale) for the walks; Regione Lazio for the register
- Coverage: GOLD, on both counts. The register PDF I parsed holds 212 numbered
  rows for Lazio, of which 57 sit in the comune of Roma. Every row carries:
  ID code, province, comune, named locality (villa or street, e.g. "Via delle
  Tre Pile", "Scalinata del Campidoglio", "Villa Sciarra - Viale Adolfo...",
  "Villa Celimontana - Viale..."), latitude and longitude in DMS, a yes/no
  flag, scientific name, Italian common name, girth in cm, height in m, and the
  designation criteria (age/size, form, botanical rarity, landscape value,
  historic-cultural-religious value). No age in years, and no vitality field.
  The two walk articles name roughly 10 trees individually with species and
  place: Phytolacca dioica on the Cordonata del Campidoglio, Paulownia
  tomentosa at Piazza della Chiesa Nuova, the Ginkgo biloba pair at Via
  Terenzio / Via Fabio Massimo in Prati, Podocarpus + Himalayan Cedar + Ginkgo
  at Villa Sciarra, Cedar of Lebanon at the Ossario Garibaldino, plus Cedar of
  Lebanon and Holm Oak at Villa Borghese and the Oriental Planes of Valle del
  Graziano.
- Walkable: the Campidoglio-to-Prati route is one afternoon on foot; the
  Gianicolo/Villa Sciarra route is a second, separate afternoon. The 57-entry
  register is spread across the whole comune and is not a walk.
- Official designation list rather than a tourist article? BOTH. The walks are
  the comune's own articles, not a newspaper listicle; the register is the
  statutory regional list.
- Judgement: the single best Italian city found in this sweep. The register
  gives species, coordinates, girth and height for 57 Rome trees in one
  parseable document, and the comune's own walk articles independently name and
  place about ten of them, which is exactly the two-source pair a research pass
  needs. A pass here should be well under an hour. Easily 10 trees surviving a
  two-source bar, and the Gianicolo/Villa Sciarra cluster alone is a walkable
  set of 5 or 6. Caveat: no ages anywhere, so age still needs per-tree work.

## Milan
- Route exists: YES, and better than a route: 13 individual tree pages on the comune's own site, plus a labelled tree trail in Parco Sempione
- URL(s):
  - Index of the 13 monumental trees, each linking to its own page: https://www.comune.milano.it/argomenti/ambiente-e-animali/gli-alberi-monumentali-a-milano
  - Example single-tree page: https://www.comune.milano.it/argomenti/ambiente-e-animali/gli-alberi-monumentali-a-milano/il-platano-del-1773-a-villa-litta
  - Green itineraries hub, 11 walks: https://www.comune.milano.it/argomenti/ambiente-e-animali/itinerari-nel-verde
  - Parco Sempione tree trail (two routes, 21 labelled plants on the first): https://www.comune.milano.it/argomenti/ambiente-e-animali/itinerari-nel-verde/parco-sempione-alla-scoperta-degli-alberi
  - Its guide PDF: https://www.comune.milano.it/documents/20118/496742/Parco+Sempione-percorsi+alberi-guida.pdf/2d3ce384-1e5c-a2e3-3fe0-cd418c7a017f
  - Its route map PDF: https://www.comune.milano.it/documents/20118/496742/Parco+Sempione-percorsi+alberi-mappa.pdf/45a92ae2-b260-8520-2aa7-b2db577db2db
  - Older municipal list PDF: https://www.comune.milano.it/documents/20126/1588721/Primo+Elenco+Alberi+Monumentali+Milano.pdf
  - City-metropolitan overview: https://www.cittametropolitana.mi.it/pianificazione_territoriale/paesaggio/Studi-e-approfondimenti/alberi-monumentali.html
  - Note: comune.milano.it returns 403 to plain fetchers. It serves fine with a normal browser user-agent.
- Publisher: comune (Comune di Milano, Area Verde + Guardie Ecologiche Volontarie)
- Coverage: GOLD, the richest per-tree pages found in this sweep. All 13 trees
  are NAMED INDIVIDUALLY, each with its own URL, its municipio, a street
  address, a written description, and latitude/longitude embedded in the page
  HTML (verified: the Villa Litta plane returns 45.516844, 9.167862). Several
  carry real measurements and a dendrochronologically dated age rather than an
  estimate: the Villa Litta plane is dated to 1773 from a counted section, at
  32 m tall and 228 cm trunk diameter. The 13: bagolaro and platano and
  cipresso calvo and "platano della biodiversita" and "platano grande" at the
  Giardini Montanelli, platano and bagolaro at Villa Belgiojoso (Villa Reale
  di Palestro), platano del 1773 and platano "siamese" at Villa Litta, the
  platano del Giardino Bazlen, La "Pianta" di Affori, the quercia of Piazza
  XXIV Maggio, the noce del Caucaso in Parco Sempione, and the bagolaro of
  Villa Marietti Radice Fossati. The Parco Sempione trail is a separate thing:
  physically labelled trees with steel-nailed tags, two routes, first one has
  21 plants, guide and map both downloadable.
- Walkable: mixed and it clusters well. Giardini Montanelli (5 trees) plus
  Villa Belgiojoso (2) are adjacent, so that is a seven-tree afternoon in
  Municipio 1 on its own, with Parco Sempione and Piazza XXIV Maggio reachable.
  Villa Litta and Affori are Municipio 9, a separate northern cluster of 3.
- Official designation list rather than a tourist article? Yes, the comune's own
  designated set, presented per tree rather than as a table.
- Judgement: makes a Milan pass very cheap. Coordinates, address, dimensions
  and in some cases a dated age come from the municipality itself, and the
  Lombardy regional list plus Parco Sempione guide give the second source. All
  13 would plausibly survive a two-source bar; the constraint is our own
  ten-per-city cap and the cluster rule, not evidence. The Montanelli /
  Belgiojoso / Sempione cluster is the obvious walk.

## Naples
- Route exists: WEAK as a *walk*, GOLD as a per-tree register with photos
- URL(s):
  - Regione Campania monumental trees hub: https://agricoltura.regione.campania.it/foreste/monum/alberi_monumentali_index.html
  - Full searchable list, whole dataset embedded in the page as a JS array so it parses trivially: https://agricoltura.regione.campania.it/foreste/monum/alberi_monumentali_elenco.html
  - Interactive map: https://agricoltura.regione.campania.it/foreste/monum/alberi_monumentali_map.html
  - Example per-tree scheda: https://agricoltura.regione.campania.it/foreste/monum/scheda_19.html
  - Regione Campania open data catalogue entry (licence not readable via plain fetch, check in a browser before any import): https://dati.regione.campania.it/catalogo/datasetdetail/alberi-monumentali-della-campania
  - Orto Botanico di Napoli "piante notevoli" route (site was refusing connections at scout time, retry): http://www.ortobotanico.unina.it/OBN4/mv/percorsi/piante_notevoli.htm and http://www.ortobotanico.unina.it/OBN4/mv/percorsi/percorsi.htm
  - Orto Botanico current site, has a WebGIS of its trees: https://www.ortobotaniconapoli.it/it/visitare/aree-espositive-serre-musei.html
  - Blog itinerary (private publisher, treat as a lead only): https://cosedinapoli.com/itinerari/gli-alberi-monumentali-di-napoli-storia-identita-e-paesaggio/
- Publisher: region (Regione Campania, UOD Foreste) for the register; university botanic garden for the garden route; a blog for the "itinerary"
- Coverage: GOLD on data. I parsed the list page: 417 rows for Campania, of
  which 55 sit in the comune of Napoli, each NAMED BY LOCATION with scientific
  name, Italian common name and a linked scheda. Each scheda carries: comune,
  GPS coordinates, altitude, species, trunk circumference, height, a written
  historical/botanical description, and a photo (photo licence NOT stated,
  do not assume reuse). Age is prose inside the description, not a field.
  The Naples 55 cluster strikingly: 12 at Capodimonte across its several
  gardens, 9 in the Orto Botanico, 6 at the Mostra d'Oltremare, 5 around
  Piazza Vittoria in Chiaia, 3 in the Accademia di Belle Arti cloister, 2 at
  the Incurabili, 2 at Sant'Andrea delle Dame. Species are the interesting
  part: Ficus macrophylla, Jubaea chilensis, camphor trees, Podocarpus,
  Melaleuca, a Montezuma cypress, a Taxus baccata, Phytolacca dioica.
  What does NOT exist: a published municipal walking route. The only
  "itinerary" found is a blog article.
- Walkable: several genuinely tight clusters rather than one route. Chiaia /
  Piazza Vittoria is a five-tree square. Capodimonte is a park you walk anyway.
  The historic centre gives Accademia + Incurabili + Sant'Andrea delle Dame +
  Orto Botanico within a walk. So a Naples page can be two or three real walks.
- Official designation list rather than a tourist article? Yes, the regional
  statutory list.
- Judgement: cheap pass, but the second source has to come from somewhere other
  than a municipal walk, because Naples has not published one. The region gives
  source one with coordinates and measurements; source two will be the Orto
  Botanico's own pages for the garden trees, and per-tree local sources for the
  rest. Expect 10 to survive comfortably. Best target cluster: the historic
  centre cloisters plus the Orto Botanico.

## Palermo
- Route exists: WEAK. A commercial guided tour exists, no free published tree-by-tree route. The regional register is strong but I could not open the current PDF.
- URL(s):
  - Regione Siciliana monumental trees landing page, the stable entry point: https://www.regione.sicilia.it/istituzioni/regione/strutture-regionali/assessorato-territorio-ambiente/comando-corpo-forestale-regione-siciliana/ambiente/altri-contenuticorpo-forestale-regione-siciliana/alberi-monumentali-regione-siciliana
  - The PDF it advertises (updated 17/07/2026) 404s on direct request and curl gets an HTML page instead, so the filename on the landing page must be re-read each time rather than hardcoded: .../sites/default/files/2026-07/elenco_degli_alberi_monumentali_di_sicilia_aggiornato_al_17.07.2026.pdf
  - Sicily tourism geoportal layer "Alberi Monumentali di Sicilia" (TLS certificate chain is broken, would not verify): https://geoportale.osservatorioturistico.regione.sicilia.it/alberi-monumentali-di-sicilia/
  - Third-party mirror of the regional list: https://www.lasiciliainrete.it/elenco-alberi-monumentali-sicilia/
  - Commercial guided walk "Radici Monumentali" by the Terradamare co-op, a real route but a paid tour rather than a published list: https://terradamare.org/itinerario-radici-monumentali-palermo/
  - Orto Botanico di Palermo map: https://www.ortobotanico.palermo.it/mappa-dellorto-botanico-di-palermo/
  - Comune di Palermo tourism page for the Orto Botanico: https://turismo.comune.palermo.it/palermo-welcome-luogo-dettaglio.php?tp=68&det=23&id=151
- Publisher: region (Corpo Forestale, Regione Siciliana) for the register; a tourism co-op for the walk; the university for the garden
- Coverage: register is real and large. The regional page itself states 334
  monumental trees across 71 comuni, 76 of them in urban settings, with 133 in
  the province of Palermo, 54 Catania, 37 Agrigento; a separate source counts
  43 in the comune of Palermo, the highest of any Italian city centre. I could
  NOT verify the per-row fields because both PDF routes failed at scout time,
  so whether it carries coordinates, girth and height like Lazio and Campania
  is UNCONFIRMED. The Terradamare tour names stops individually (Palazzo
  Butera jacaranda roots, the Ficus macrophylla of Piazza Marina) but it is a
  sales page for a guided walk, not a list. The Piazza Marina ficus itself is
  exceptionally well documented, including a March 2026 Il Post piece on the
  tree being seriously ill, which matters: check its condition before shipping.
- Walkable: yes, and the historic-centre cluster is excellent. Piazza Marina /
  Villa Garibaldi, Villa Giulia, the Orto Botanico and Palazzo Butera sit in
  one seafront-adjacent quarter, an easy afternoon.
- Official designation list rather than a tourist article? Yes for the register,
  no for the route.
- Judgement: a good city with a frustrating access problem. Fix the PDF fetch
  first (read the current filename off the landing page, or use the geoportal
  with certificate verification handled), then the pass is cheap. 10 trees
  should survive easily given 43 designated in the comune. Flag: verify the
  Piazza Marina ficus is still alive and standing before it ships, per the
  living-tree rule.

## Florence
- Route exists: NO published tree walk. But the comune publishes a clean 29-tree table with coordinates, which is worth more.
- URL(s):
  - Comune di Firenze "Piante Monumentali citta di Firenze" PDF, dated 2024-12, TEXT LAYER, parses in seconds: https://ambiente.comune.fi.it/sites/ambiente.comune.fi.it/files/2024-12/Piante%20Monumentali%20citt%C3%A0%20di%20Firenze.pdf
  - Its parent page, also linking a "Mappa del verde": https://ambiente.comune.fi.it/pagina/giardini-e-aree-verdi/il-patrimonio-arboreo
  - Comune press release on the count rising from 12 to 29: https://www.comune.fi.it/comunicati-stampa/alberi-monumentali-sono-29-le-piante-sotto-tutela
  - Regione Toscana monumental trees page (regional list, 165 plants after the 2024 update): https://www.regione.toscana.it/-/alberi-monumentali-1
  - Citta Metropolitana planning annex, old 1982-derived material, low value: https://www.cittametropolitana.fi.it/wp-content/uploads/Elenco_Alberi_monumentali.pdf
  - Feel Florence historic gardens itinerary, gardens only, names no trees, WORTHLESS as a source: https://www.feelflorence.it/en/experiences-itineraries/walk-through-historic-gardens-city
- Publisher: comune (Direzione Ambiente) for the list; region for the wider register; the DMO for the useless garden article
- Coverage: GOLD list, no walk. I parsed the PDF: exactly 29 rows for the
  comune of Firenze, columns PROGR, ID SCHEDA, PROVINCIA, COMUNE, LOCALITA,
  LATITUDINE and LONGITUDINE in DMS, ALTITUDINE, urban-context yes/no,
  scientific name, Italian common name, trunk circumference in cm, height in m,
  monumentality criteria, a proposed-declaration flag, and crucially PROPRIETA
  (ownership). That last column is the one that matters for us: at least 14 of
  the 29 are marked Privata, including all seven in the Orto Botanico and the
  Villa Gamberaia pine, so hard rule 10 has to be applied row by row rather
  than assumed. No age column. Locations cluster: 7 in the Orto Botanico
  (Giardino dei Semplici, Via Micheli), 4 in the Parco delle Cascine, 3 around
  Bobolino / Viale Machiavelli, plus Villa della Petraia, Giardino dell'Iris,
  Villa di Rusciano, Palazzo Pitti, Via dei Pepi, Isolotto, Mantignano.
- Walkable: two decent clusters. Bobolino / Viale Machiavelli / Palazzo Pitti /
  Via del Monte alle Croci is one Oltrarno afternoon; Parco delle Cascine is a
  second. The Orto Botanico is seven trees in one paying garden, which is a
  single stop rather than a walk and needs its access noted.
- Official designation list rather than a tourist article? Yes, the comune's own
  statutory list.
- Judgement: cheap and reliable for data, but Florence has published no route,
  so the second source is per-tree work (Orto Botanico's own pages, Villa
  Bardini/Boboli material, Regione Toscana). Roughly 10 should survive, but the
  private-ownership column will cut into the pool honestly. Best target: the
  Oltrarno cluster, since the Orto Botanico trees are private and ticketed.

## Venice
- Route exists: NO. And the register underneath is thin for this city specifically.
- URL(s):
  - Regione del Veneto monumental trees: https://www.regione.veneto.it/web/economia-e-sviluppo-montano/alberi-monumentali and https://www.regione.veneto.it/web/enti-locali/alberi-monumentali
  - DGR 1325 of 25/10/2022, Allegato A, the three-year programme (12 pp, text layer, but it is POLICY not a list): https://bur.regione.veneto.it/BurvServices/pubblica/Download.aspx?name=Dgr_1325_22_AllegatoA_487954.pdf&type=9&storico=False
  - Comune di Venezia verde pubblico: https://www.comune.venezia.it/it/content/verde-pubblico-0
  - Third-party aggregation: https://www.alberimonumentali.info/regioni/veneto
- Publisher: region; comune has nothing tree-specific published
- Coverage: WEAK. The whole Veneto register is small, 88 declared plus 22
  proposed, around 110, against 57 in Rome alone. The DGR gives a per-province
  count and the province of Venezia holds 35, and the province is mostly
  mainland: the examples the region itself highlights are the oak of Fossalta
  di Portogruaro and trees in Belluno and Padua, not the historic city. The
  DGR document I parsed is a programme, not a table: no species rows, no
  coordinates. Notably its action D is "Individuazione di una rete di percorsi
  interessati da Alberi Monumentali", a network of monumental-tree routes the
  region intends to identify, which means the route does not yet exist. Nothing
  found that names Venice trees individually.
- Walkable: unknown, and probably the wrong question. The 35 provincial trees
  are spread across the mainland municipality; the islands themselves are the
  least treed part of any major Italian city.
- Official designation list rather than a tourist article? The register is
  official but I could not obtain a per-tree table for the comune.
- Judgement: the weakest of the big seven. Venice would be an expensive pass
  with an uncertain payoff, and it is the one city where the four-tree floor is
  genuinely at risk in the historic centre. If it is ever attempted, start from
  the Giardini della Biennale, Sant'Elena, San Servolo/San Francesco del
  Deserto and the Mestre parks, and expect per-tree research rather than a
  register lift. Deprioritise behind Rome, Milan, Naples, Florence and Bologna.

## Bologna
- Route exists: WEAK. Guided-event pages and blogs, no published tree-by-tree route. The regional data layer is good.
- URL(s):
  - Regione Emilia-Romagna interactive monumental-tree cartography and data service: https://ambiente.regione.emilia-romagna.it/it/parchi-natura2000/servizi/s-dati-alberi-monumentali
  - The same dataset on the European Data Portal, which is where to read the licence before importing: https://data.europa.eu/data/datasets/r_emiro-e19dc9e1-4c5a-4255-a241-5dce5130df69?locale=it
  - Citta Metropolitana di Bologna list page: https://www.cittametropolitana.bo.it/turismo/Newsletter_16_febbraio_2024/Elenco_degli_alberi_monumentali
  - RAMI, a national NGO tree register with a Bologna page, useful as an independent cross-check for ANY Italian city: https://ilregistrodeglialberi.it/italia/emilia-romagna/bologna/bologna
  - Guided-event page "Bologna all'ombra dei giganti verdi": https://www.culturabologna.it/events/bologna-all-ombra-dei-giganti-verdi
  - Biblioteca Salaborsa's Bologna Online cartigli on historic gardens, good written history per garden: https://www.bibliotecasalaborsa.it/bolognaonline/i-cartigli-di-bologna-edifici-storici-giardini-e-canali/giardini
- Publisher: region (Emilia-Romagna, Parchi e Natura 2000) for the data; comune/culture bodies for events; NGO for RAMI
- Coverage: mixed, and the counts disagree, which is itself worth recording.
  Emilia-Romagna's regional set is around 136 trees with a much larger number
  of "protections" (658) after a December 2023 regional law. For the comune of
  Bologna the national AMI list carries only 7 to 9 specimens depending on the
  source, while the NGO register RAMI counts 36. Named individual trees do turn
  up in the garden writing rather than in a list: "Il Solitario", a sequoia in
  the Giardini Margherita at 520 cm girth and 37.4 m, plus the oak grove, the
  holm oaks, bald cypresses on the pond edge and a notable Maclura, all in the
  same 26 hectare park opened in 1879. A separate 2024 survey found 76 old
  trees in the Bolognese Apennines, outside the city.
- Walkable: the Giardini Margherita alone is a compact cluster and would carry
  half a page, with the historic centre gardens reachable on foot.
- Official designation list rather than a tourist article? The regional
  cartography is official; there is no municipal walking route.
- Judgement: workable but not cheap. Only 7 to 9 nationally designated trees in
  the comune means the four-tree floor is met but ten is not reachable from the
  register alone, so RAMI plus the Salaborsa garden histories would have to
  carry the rest, and RAMI is an NGO register, not a government one. Expect 5
  to 7 surviving a two-source bar. Giardini Margherita is the walk.

## Turin
- Route exists: YES, and it is the single best published WALK found in this sweep.
- URL(s):
  - "Gli alberi monumentali di Torino - Un filo verde nel cuore di Torino", published by Turismo Torino e Provincia as a verified partner on Outdooractive, with GPX/KML/FIT download: https://www.outdooractive.com/it/route/percorso-urbano/provincia-di-torino/gli-alberi-monumentali-di-torino-un-filo-verde-nel-cuore-di-torino/804381643/
  - Citta di Torino verde pubblico hub (the monumental-tree subpage was NOT reachable from here at scout time, the general alberi page has no list): http://www.comune.torino.it/verdepubblico/alberi/
  - Referenced but unverified official list URL: www.comune.torino.it/verdepubblico/alberi-monumentali/
  - Circoscrizione 2 tree material: https://decentramento.comune.torino.it/circ2/cm/pages/ServeBLOB.php/L/IT/IDPagina/2144
  - Census news: https://www.torinoclick.it/territorio/censimento-alberi-monumentali/
- Publisher: the official regional tourist board, Turismo Torino e Provincia
- Coverage: GOLD as a route. It names all 15 trees on Piemonte's regional list
  for the city INDIVIDUALLY, each with species, the exact place, and its
  measured height, in the pattern "Platano - Parco del Valentino (nei pressi
  della Fontana 12 mesi) - 39,5 m" and "Ginkgo (Ginkgo Biloba) - Giardini
  Cavour - 27 m". Stops run through Piazza Castello, the Giardini Reali,
  Palazzo Carignano, Giardini Cavour, Parco del Valentino, the Borgo Medievale
  and Villa Rey. No ages and no girths, and no coordinates per tree, but the
  GPX carries the geometry. Plane trees dominate.
- Walkable: 13.9 km, about 4 hours, graded easy and family-suitable. That is a
  long afternoon rather than a short one, and it splits cleanly: the centre
  (Piazza Castello, Giardini Reali, Cavour) is one tight cluster, the Valentino
  another, Villa Rey the outlier across the Po.
- Official designation list rather than a tourist article? Both at once, which
  is the useful bit: it is the tourist board rendering the regional
  designation list as a route.
- Judgement: the cheapest city on this list to research after Rome and Milan.
  One page gives species, place and height for all 15 designated trees, and the
  Piemonte regional register supplies the second source. Comfortably 10
  surviving a two-source bar. Take the centre plus Valentino as two walks and
  leave Villa Rey out or label its travel time honestly. Caveat: heights only,
  so ages need per-tree work, and the comune's own monumental-tree page did not
  resolve at scout time and should be found before the pass.

## Genoa
- Route exists: NO city walk found. But Liguria has the only EXPLICITLY LICENSED open dataset in this sweep.
- URL(s):
  - Regione Liguria open data record for "Alberi monumentali ddg n.3342/2024": https://www.regione.liguria.it/open-data/item/42569-alberi-monumentali-ddg-3342-2024.html
  - Geoportal record for the previous decree: https://geoportal.regione.liguria.it/component/k2/item/839-alberi-monumentali-d-d-n-3881-2023.html
  - Regional service page: https://www.regione.liguria.it/servizi-2022/item/1205-alberi-monumentali.html
  - Agriligurianet: https://www.regione.liguria.it/component/flexicontent/weblink/16/1205/1.html
  - Tourist-board article, only 6 trees and none of them in Genoa city, WEAK: https://lamialiguria.it/itinerari/sei-alberi-monumentali-liguria/
  - Wikipedia's list, useful as a cross-check index: https://it.wikipedia.org/wiki/Alberi_monumentali_della_Liguria
- Publisher: region (Regione Liguria)
- Coverage: 145 entries region-wide after the seventh update (decree 3322 of
  20/05/2024): 129 single trees and 16 homogeneous groups. Data came from GPS
  survey at 1:5000 in Gauss-Boaga projection, gathered by the comuni and
  classified on the standard seven criteria. **The open-data page states the
  licence as CC BY**, which is the only explicit licence statement I found
  anywhere in this sweep and makes Liguria the first Italian region clearly
  usable for our register layer (record the proving sentence in
  OPEN_DATA_SURVEY.md before importing). I did not get a per-comune breakdown
  for Genoa itself, so the Genoa count is UNKNOWN. Note the 16 "insiemi
  omogenei": group entries fail our collectible-point test unless the ensemble
  itself is the destination.
- Walkable: unknown at scout time.
- Official designation list rather than a tourist article? Yes.
- Judgement: do the licence and dataset work here before the city work. Genoa
  as a city page is unproven, but Liguria as a register-layer country-level
  import is the most promising thing found today after Rome's Lazio PDF. The
  regional tourist board's own "six monumental trees" article names none in
  Genoa, which is mild evidence the city itself is thin.

## Cities NOT reached in this sweep
Catania, Pisa and Siena were not searched individually. Catania is partly
pre-covered by the Palermo block: it sits under the same Regione Siciliana
register, which credits the province of Catania with 54 monumental trees, so
the same broken-PDF access problem applies and should be solved once for both.
Pisa and Siena sit under the Regione Toscana register (165 plants region-wide
after the 2024 update) and would be scouted the same way Florence was, by
looking for a comune-published "Piante Monumentali" table first, since Florence
proves Tuscan comuni publish those with coordinates, girth, height and
ownership.

## Cross-cutting notes for whoever runs Italy next
- The national umbrella is MASAF's Elenco degli alberi monumentali d'Italia,
  seventh update D.M. 0579238 of 04/11/2024: https://www.masaf.gov.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/22282
- RAMI, ilregistrodeglialberi.it, is an independent NGO register covering the
  whole country and consistently counts MORE trees than the national list
  (36 in Bologna against 7 to 9). Useful as a second source and as a lead
  list, but it is not a government register and does not satisfy the layer-2
  "one official register" rule on its own.
- Regional lists are the real prize and their quality is uneven. Ranked by what
  I could actually verify today: Lazio (text PDF, DMS coordinates, girth,
  height) and Campania (per-tree HTML schede with GPS, girth, height, photo,
  whole dataset embedded as JS in one page) and Tuscany-via-Firenze (text PDF
  with coordinates AND an ownership column) are all directly parseable.
  Liguria is the only one stating CC BY. Sicily's PDF 404s and its geoportal
  has a broken certificate chain. Veneto publishes policy, not a table.
- None of these registers carries an age in years, and none carries a vitality
  field. Both remain per-tree work, exactly as CLAUDE.md warns.
- Ownership matters more in Italy than in Portugal or Spain: Florence marks at
  least 14 of its 29 as Privata. Read that column before shipping, per hard
  rule 10.
