# Published tree walks: Spain and Portugal

Date: 2026-08-05. Scouting only. No trees researched, no city file written.

**What this is.** Which Spanish and Portuguese cities already publish their own tree-by-tree
route or per-tree designation list. The reason it exists is Setubal: a parish there publishes
a walking route naming each tree with species, place, age and height, and one fetch of it
independently corroborated nine of our ten entries. That is the most expensive part of a
research pass, the second source, solved in a single request. Registers give scattered trees;
a published route gives a walk, an order and a second source at once.

**How to read a block.** "Route exists: YES" means the source names trees INDIVIDUALLY with a
location. A page that tells you to wander a park and admire the old trees is recorded as NO,
on purpose: a false positive costs a later run more than a blank does. WEAK means something
real exists but is a tourist article, a newspaper listicle, or a list without locations.

**Standing rule for anything found here.** These are sources to cite and verify against, never
to copy from. No text, no photographs. A licence is noted only where the page states one.

Searched in Spanish, Catalan, Galician and Portuguese. English searches miss nearly all of it.

---

## Madrid: YES, and the catalogue is open after all

**Route or per-tree list exists: YES.** Two separate things, and both are official.

**1. The regional catalogue names every tree individually, and 59 of them stand in the
municipality of Madrid.** The brief said Madrid's catalogue "sits in a PDF" and is therefore
closed. That is half right and the wrong half. The PDF is a real text PDF, not a scan: it
extracts cleanly with pypdf, six pages, name plus scientific name plus municipality plus
reason for listing, per tree.

- Official: ORDEN 68/2015, de 20 de enero, Consejería de Medio Ambiente y Ordenación del
  Territorio. http://www.bocm.es/boletin/CM_Orden_BOCM/2015/02/04/BOCM-20150204-8.PDF
  Publisher: Boletín Oficial de la Comunidad de Madrid. Legal basis Decreto 18/1992.
  Caveat: this order is the DELTA only, the 2015 exclusions (Anexo I) and additions
  (Anexo II), not the standing 280. Its exclusion list is worth as much as its addition
  list to us, because it is a register saying which trees are dead or gone: the Eucalipto
  del Parque del Retiro, the Pino Carrasco El Pantalones and the Ciprés Fúnebre de los
  Jardines de Herrero Palacios were all struck in Madrid municipality. Under the
  living-tree rule that is a pre-filtered do-not-publish list handed to us.
- The consolidated 280-tree list, in a form a run can actually parse in one command:
  https://es.wikipedia.org/wiki/Árboles_singulares_de_la_Comunidad_de_Madrid
  A sortable wikitable, columns Número / Denominación común / Nombre científico /
  Municipio / Coordenadas / Motivo de catalogación / Wikidata id / Imagen. 280 rows, and
  59 have Madrid as the municipality. Coordinates are filled on only a minority of rows.
  Wikipedia is not a source under our two-source bar, it is an index; the BOCM order and
  the individual Wikidata items behind many rows are what a run cites.

**2. The Ayuntamiento publishes an actual numbered botanical trail in the Retiro.** The
Senda Botánica del Buen Retiro: seven independent routes, between 10 and 20 trees each,
around 80 trees in total, run by the Centro de Educación Ambiental de El Retiro. Eight of
the Retiro's trees are catalogued Árboles Singulares under the regional catalogue, and the
council's own guided walk "Las maravillas del Retiro" is built around them (the Ahuehuete
del Parterre and the cypresses at the Palacio de Cristal pond are named in the council's
own description). There is a matching Casa de Campo document, "Principales árboles
singulares del parque de la Casa de Campo", from the Casa de Campo environmental centre.
- https://diario.madrid.es/cieaelretiro/senda-botanica-del-retiro/ (Ayuntamiento de Madrid)
- https://diario.madrid.es/cieacasadecampo/wp-content/uploads/sites/61/2020/03/Principales-árboles-singulares-del-parque-de-la-Casa-de-Campo.pdf
- **Access note for the next run: diario.madrid.es sits behind Akamai and returns 403 to
  both WebFetch and curl, with any user agent.** The content is public, the fetcher is
  blocked. Open these two in a browser session rather than burning a run's window
  rediscovering the block. bocm.es and es.wikipedia.org both fetch fine.

**Coverage and fields.** 280 regionally catalogued trees, 56 species, 68 municipalities,
of which 59 trees in Madrid city. Per tree: common name, scientific name, municipality,
reason for listing. Ages and dimensions are NOT in the catalogue and have to come from
elsewhere per tree. Most tree names encode their own location ("Cedro del Líbano del Museo
del Prado", "Madroño de la Plaza de la Lealtad"), which is why this is usable at all: the
name is the pin, to street level, before any geocoding.

**Walkable as one afternoon: yes, and unusually well.** Grouping the 59 by the place in
their own names:
- Paseo del Prado axis, one continuous walk: Real Jardín Botánico holds 8 catalogued trees
  (Butia, Ciprés, Olmo del Cáucaso / Zelkova carpinifolia, Palmera Canaria, Parrotia
  persica, Pino Carrasco, Pino Llorón, Tejo), and within a few hundred metres sit the
  Cedro del Líbano del Museo del Prado, the Picea del Himalaya de la Plaza de Murillo, the
  Almez del Paseo del Prado, the Madroño de la Plaza de la Lealtad, two Butia on the Paseo
  de Recoletos and the Gingo del Palacio de Buenavista.
- El Retiro, adjoining it: 8 catalogued trees, plus the council's own 80-tree numbered
  trail on top.
- Campo del Moro: 6 (Pino Carrasco, Pino Piñonero, Roble, Secuoya, two Tejos).
- Parque de la Fuente del Berro: 4 (Cedro del Atlas, Cedro del Líbano, Ciprés de Portugal,
  Enebro de Siria).
The Botánico plus Prado plus Retiro group alone is over twenty catalogued trees inside two
kilometres, on flat ground. That is denser than Cadiz, which is our calibration set for
what a good afternoon feels like.

**Judgement. Madrid is already published, with 10 trees, so this is a deepening job and
not an opening one.** Correcting the brief on its own premise: data/cities/madrid.json
exists and holds mad_001 to mad_010. Six of them already sit on exactly the Prado axis
described above (Ahuehuete del Parterre, Himalayan Cedar and bald cypresses at the Crystal
Palace, the Velázquez yew, the Botánico cypress and Caucasian elm). So the catalogue does
not unblock Madrid, it does three cheaper things:

1. **It second-sources what is already live.** Every Madrid entry that matches a
   Denominación in the catalogue gains an official government citation for existence and
   species at the cost of one PDF fetch. That is the Setubal effect, applied to a page we
   already ship.
2. **It fixes the two weak pins and the two outliers in one move.** mad_008 (Aleppo Pine
   of Campo del Moro) and mad_010 (Stone Pine of the Priest's House, Barajas) are both
   `approximate`, and mad_007 sits in the Casa de Campo. Those three are the trees that
   make Madrid read as a scatter rather than a walk. There are more than a dozen
   catalogued replacements inside the Botánico and along the Prado, so the swap improves
   both the cluster and the pin honesty without lowering the bar.
3. **It is the growth path past ten.** 59 catalogued trees in the municipality against 10
   published means Madrid is the clearest candidate in Spain for a city that legitimately
   grows past its ten, per the count-follows-the-trees doctrine. The remaining 49 belong
   in data/leads/madrid.json, not in a new search.

Expect essentially all of a second walk to survive a two-source bar, because the Real
Jardín Botánico and the Retiro environmental centre both document their own specimens in
addition to the BOCM order.

**What the brief got wrong, worth recording.** "Madrid city publishes only a full bulk
inventory, which our rules forbid" is true of datos.madrid.es and irrelevant, because the
designation list we need is the Comunidad's, not the city's, and it is semantic rather
than bulk: 59 named trees, not 300,000 street trees. No rule blocks it, and Madrid was
never blocked in the first place: it shipped.

---

## Barcelona: YES, and it is the best-structured of the eight

**Route exists: YES**, several, and they are neighbourhood-sized rather than city-sized,
which is exactly the shape we want.

- **Mapa Barcelona + Sostenible**, https://www.bcnsostenible.cat, a municipal
  sustainability initiative of the Ajuntament that hosts user-contributed but
  council-published itineraries. Three tree itineraries found, and the site's structure
  implies more:
  - "Arbres singulars de Sarrià: de la Casa Orlandai als Caputxins", 9 stops covering
    15-plus trees, roughly one hour on foot. Per stop: scientific name and address. Some
    entries carry real measurements, for example a Celtis at Can Miralles given as 105
    years old and a Cedrus atlantica with a trunk 306 cm across at 130 cm height. Prepared
    by M. Josep Tort.
    https://www.bcnsostenible.cat/web/itinerari/arbres-singulars-de-sarria-de-la-casa-orlandai-als-caputxins-1
  - "Arbres singulars de Sarrià de Dalt", the continuation, covering two school grounds
    and Parc Joan Reventós.
    https://www.bcnsostenible.cat/web/itinerari/arbres-singulars-de-sarria-de-dalt-1
  - "Ruta dels arbres de la Prosperitat", Nou Barris, organised by Casa de l'Aigua,
    authors Joan Catafal and Alberto Sanagustín. Species with street names throughout.
    https://bcnsostenible.cat/web/itinerari/ruta-dels-arbres-de-la-prosperitat
  - **Every itinerary offers CSV and Excel export of its points.** That is a machine-
    readable walking route with coordinates, published by a municipal initiative, which is
    the single most useful thing found in this whole sweep.
- The underlying designation list is the **Catàleg d'Arbres i Palmeres d'Interès Local**
  of the Ajuntament, 213 trees, ordinance basis 1983, still actively extended (5 trees
  added April 2026). We already hold this as data/registers/barcelona-ail.json.

**Walkable: yes, by construction.** These are one-hour neighbourhood walks, not regional
lists.

**Judgement.** Barcelona already ships 16 trees, and it is the one city where a route
would not mainly buy verification, because the AIL register already gives us that. What it
buys is the thing the register cannot: **which trees belong on the same afternoon, decided
by people who walk them.** Sarrià and Nou Barris are both districts our 16 do not touch
at all (our trees sit in Gràcia, Park Güell, Horta, Montjuïc, Les Corts, Ciutat Vella and
Sant Martí). So the value here is a second and third Barcelona walk in districts we have
nothing in, drawn straight off a CSV. Verification is cheap because the AIL catalogue
cross-checks it. Realistic yield: 6 to 10 more Barcelona trees clearing a two-source bar,
though note these are itineraries with named authors rather than council-authored
documents, so the itinerary is the lead and the AIL catalogue entry is the source.

---

## Valencia: YES, the strongest official route in Spain

**Route exists: YES.** The Ajuntament de València runs a project called "Árboles
Monumentales y Singulares de la Ciudad de València", and its output is not a list, it is
**five named walking routes covering 508 catalogued monumental and singular trees, every
one geolocated.** Publisher: Ajuntament de València, Servicio de Parques y Jardines, with
the Observatorio Municipal del Arbolado.

The five routes, each anchored on a specific set of gardens rather than the whole city:
1. "La vuelta al mundo", Jardines de Viveros
2. "Testigos de la Historia", the medieval wall and the parks around it
3. "Un viaje por el Mediterráneo", Parque de la Rambleta
4. "Un paseo por la Alameda", Alameda, Avenida Blasco Ibáñez, Jardín de Monforte
5. "Más allá de los mares", Jardines de Ayora through to the Antiguas Atarazanas

Sources:
- https://www.valencia.es/cas/agenda-de-la-ciudad/-/content/ruta-de-los-arboles-monumentales-de-valencia (Ajuntament)
- https://jardins.valencia.es/es/blog/descubre-valencia-traves-de-cinco-rutas-de-arboles-monumentales (Ajuntament, Jardins de València)
- https://www.visitvalencia.com/que-hacer-valencia/rutas-por-la-ciudad/ruta-arboles-monumentales (city tourist board)
- Regional layer above it: Catálogo de Árboles Monumentales y Singulares de la Comunitat
  Valenciana, held by CIEF, Generalitat Valenciana.
  https://mediambient.gva.es/es/web/cief/cataleg-d-arbres-monumentals-i-singulars
- The routes are delivered through an app, "València Green Routes", which is where the
  geolocation actually lives. **Not yet checked whether the underlying data is
  downloadable or open-licensed.** That is the one open question and the first thing the
  next run should test, because 508 geolocated municipal trees under a workable licence
  would be a register-layer import, not just a city page source.

**Fields.** Species, approximate age and location per tree in the route write-ups (a
400-year-old olive at La Rambleta, a 300-year-old olive at the Jardín de Monforte are the
worked examples). Ages are given as approximations, which is the honest form anyway.

**Walkable: yes, five separate afternoons.** This is the cluster model already solved by
the municipality.

**Judgement.** Valencia is already published with 10 trees, and this is the single best
deepening target of the eight. Four of our ten already sit inside these routes (El Titan
at the Parterre, the Monforte ginkgo, the Rambleta olive, the Botanical Garden Kashmir
cypress), so the routes confirm our own clustering was right, and 508 against 10 says
Valencia is the other Spanish city that can honestly grow past ten. Verification is cheap
and two-sourced by construction: municipal route plus the Generalitat's regional
catalogue. Expect nearly everything shortlisted to survive a two-source bar. Worth noting
for the season work: the two olives give real fruit peaks, and the September-peak gap the
shelf simulation found is exactly what an olive harvest fills.

---

## Seville: YES, a first-class municipal inventory, but the host would not answer

**Route exists: YES**, as a per-tree inventory with a map viewer rather than as a fixed
walking order.

**Inventario de Árboles y Arboledas Singulares de Sevilla**, approved 2022, the city's
first: **56 individual trees and 28 arboledas (groves)**. Publisher: Ayuntamiento de
Sevilla, Servicio de Parques y Jardines, built under the Plan Director del Arbolado with
Tecnigral and with the late José Elías Bonells. Selection criteria stated as age, spread,
height, rarity of species, aesthetic value and growth form. It went through a public
participation phase and is intended to become a catálogo enforced by municipal ordinance.

- Landing page: https://www.sevilla.org/servicios/medio-ambiente-parques-jardines/arboles-singulares-de-sevilla
- The inventory PDF itself:
  https://www.sevilla.org/servicios/medio-ambiente-parques-jardines/arboles-singulares-de-sevilla/inventario-de-arboles-singulares-de-sevilla_redux.pdf
- Interactive guide: https://www.sevilla.org/servicios/medio-ambiente-parques-jardines/arboles-singulares-de-sevilla/guia-interactiva
- A GIS viewer places every tree and grove on the map, and IDE.Sevilla carries the tree
  and palm inventories as data resources.
- Secondary: AMJA (Asociación de Amigos de los Jardines del Alcázar) summarises the
  catalogue, https://amja.es/catalogo-de-arboles-singulares-de-sevilla/
- Regional layer we already hold: Junta de Andalucía, Árboles y Arboledas Singulares de
  Andalucía, Sevilla volume,
  https://www.juntadeandalucia.es/medioambiente/portal/documents/20151/748568/documento_completo_sevilla.pdf
  (this is the provincial catalogue behind data/registers/andalucia-rediam.json; the
  municipal inventory above is a different and denser list for the city itself)

**Access note for the next run: www.sevilla.org refused the connection outright from this
environment**, ECONNREFUSED at the TCP level for both WebFetch and curl, which is not a
bot block but a network-level unreachability. The URLs above come from search indexing and
from the council's own 2022 press release, which did resolve, so they are real but
unverified by fetch. Retry from a browser session or a different network before concluding
anything is missing. The Junta de Andalucía PDF is on a different host and should fetch.

**Walkable: yes.** A known itinerary runs through the Parque de María Luisa and its
surroundings, taking in the Prado de San Sebastián, Jardines de Murillo, Jardín de las
Delicias, the Casino and Teatro Lope de Vega grounds, the Jardines de San Telmo and the
university rectorate. That is one continuous walk holding a large share of the 56.

**Judgement.** Seville already ships 10 trees, so this is deepening, and it is worth doing
because the municipal inventory is a stronger and more local source than the provincial
Andalusian catalogue we currently lean on. It second-sources the existing page in one
fetch and supplies a María Luisa cluster for growth. Expect a high survival rate under the
two-source bar, since municipal inventory plus provincial catalogue is two independent
official bodies. Blocked only on the host being reachable.

---

## Zaragoza: YES, and it is the best single document found in this sweep

**Route exists: YES**, as a full municipal per-tree catalogue, and it is richer than the
ICNF register we already work from in Portugal.

**"Árboles Singulares de Zaragoza"**, first edition March 2006, published by the
Ayuntamiento de Zaragoza (Oficina Agenda 21 Local, Gabinete de Educación Ambiental).
ISBN 84-8069-409-2. Scientific supervision by Juan Pablo Martínez Rica of the Instituto
Pirenaico de Ecología, CSIC. GPS coordinates supplied by the council's own Servicio de
Información Geográfica.

- https://www.zaragoza.es/contenidos/medioambiente/arboles_singulares.pdf
  187 pages, 25 MB, a real text PDF: extracts cleanly with pypdf. Note for the next run:
  it exceeds WebFetch's 10 MB limit, so curl it to disk and parse locally rather than
  fetching it.
- Second, shorter council document at
  https://www.zaragoza.es/contenidos/medioambiente/cda/arbolessingulares.pdf
  (Centro de Documentación del Agua y el Medio Ambiente), not yet opened.
- Legal frame above it: Ordenanza de Protección del Arbolado Urbano de Zaragoza, plus the
  Gobierno de Aragón's Catálogo de árboles y arboledas singulares, 57 entries region-wide,
  https://www.aragon.es/red-natural-de-aragon/arboles-y-arboledas-singulares/catalogo

**Coverage and fields. 57 numbered tree fichas, and every single one carries GPS.**
Measured by parsing the PDF, not estimated. Per ficha:
- Common name, scientific name, other local names
- Barrio, and a Localización precise to a street, a park or a named building
- Entorno, a description of the immediate setting
- **Propietario, stated as "Suelo público" or private with the owner named.** 48 of the 57
  are public, 8 private. That is hard rule 10 pre-answered by the publisher, per tree,
  which no other source in this sweep does.
- Full dimensions: girth at base, girth at 1.30 m, trunk height, total height, crown
  diameter, with the year of measurement given (2004 or 2005)
- Motivo de la singularidad, and Estado de conservación
- Free notes, often the tree's history

**Two cautions, both of the kind the Portugal lessons predicted.** The measurements are
from 2004-2005, so they are twenty years stale and any figure we quote must say so. And
the catalogue records conservation state, not vitality today: 2006 is long enough ago that
whether each tree still stands is a per-tree check the document cannot do for us. It also
gives no ages, only dimensions, so age has to come from elsewhere per tree. Girths are in
metres, stated as metres, so the ICNF unit trap does not apply here, but check anyway.

**Walkable: partly, and the barrio field is what makes it decidable.** Entries span the
whole municipality including outlying barrios like San Gregorio and Monzalbarba, but Casco
Histórico, Parque Bruil, Universidad and San José entries cluster tightly. Running
scripts/cluster_register.py over the extracted GPS would settle this in one command; the
coordinates are UTM (zone 30, ED50 era given the 2006 date) and need converting to WGS84
before anything is pinned. That conversion is the one real piece of work.

**Judgement. Zaragoza should be opened, and it is a cheap city, not a thin one.** The
brief's premise that Zaragoza has "thin register supply" is wrong: 57 individually
documented trees with coordinates, dimensions and ownership is better supply than most
cities we have published. A pass here is verification plus writing, not searching. On a
two-source bar: the municipal catalogue is one source, the Aragón regional catalogue
covers a subset as the second, and the well-known individual specimens the book itself
flags (the pino de San Juan de la Peña, the tilo del Barrio Oliver, the cedro de la calle
Marqués de la Cadena, the laurel de la Cárcel) will have local press and heritage coverage
as a second. Realistic yield: comfortably 10 from the 48 public entries, once the
still-alive check is done. The 8 private ones are excluded outright and go straight to
blocked in data/leads/zaragoza.json with the reason already written for us.

---

## Lisbon: WEAK

**Route exists: WEAK.** Something real exists in several places, but nothing that is both
free, official, tree-by-tree and fetchable.

- **"Árvores na Cidade: Roteiro das árvores classificadas de Lisboa"**, 2nd edition, by
  Graça Amaral Neto Saraiva and Ana Ferreira de Almeida, published 2018 by APAP
  (Associação Portuguesa dos Arquitectos Paisagistas). https://apap.pt/produto/arvores-na-cidade/
  This is exactly the Setubal-shaped thing, a route guide to Lisbon's classified trees,
  and it is **a printed book for sale, not a web page.** Held by the Lisbon municipal
  libraries (https://blx.cm-lisboa.pt). It cannot be fetched or cited from, and buying it
  is a spending decision that belongs to Hidde under hard rule 5. Recorded so a later run
  does not rediscover it and stall.
- **Percurso das árvores at the Quinta dos Condes dos Arcos**, Olivais, run by the Escola
  de Jardinagem: 28 notable trees, about 1.5 km, roughly two hours, starting at a
  grevillea and ending at a ginkgo. Genuinely tree-by-tree and genuinely a walk, but it is
  a single estate rather than the city, and it is an on-site guided route rather than a
  published per-tree document.
- **CML "Guia Ilustrado de Vinte e Cinco Árvores de Lisboa"**, Câmara Municipal de Lisboa,
  on Issuu. **This is a NO by our test**: it is a guide to 25 common tree SPECIES of the
  city, not 25 individual trees. A later run will find it and think it is a jackpot; it is
  not. Recorded here to save that run the disappointment.
- **CML Geodados "Arvoredo"**, https://geodados-cml.hub.arcgis.com/datasets/arvoredo, with
  CSV, KML, GeoJSON and WFS. This is the municipal tree inventory, i.e. bulk, and bulk
  municipal inventories are exactly what the register-layer rules forbid importing. The
  usable slice is the classified subset, and classified trees for Portugal already come to
  us through ICNF, which we hold as data/registers/portugal-icnf.json. Process types
  KNJ1 isolated / KNJ2 groves / KNJ3 avenues / KNJ4 trees by historic buildings / KNJ6
  shrubs are the ICNF classification codes and are the right filter if anyone does mine it.

**Judgement.** Lisbon already ships 12 trees and this sweep does not cheapen it much. The
APAP book is the one thing that would, and it is behind a purchase. Do not spend a window
here; the marginal Lisbon tree is better found through the sacred-ground and named-place
search that already turned up the Jardim da Estrela gap.

---

## Porto: WEAK, and the route is announced rather than published

**Route exists: WEAK.**

- The Câmara Municipal do Porto's environment service states that Porto holds **228 trees
  or tree groups classified as of Public Interest** (2020 figure), across the three ICNF
  classes: isolated tree, maciço, alameda.
  https://ambiente.cm-porto.pt/arvoredo/arvores-de-interesse-publico
  **The page does not list them individually.** It names examples only: the ginkgo on the
  Passeio das Virtudes, the araucaria in the Jardim da Cordoaria, the tulip tree at Casa
  Tait, the palms of the Passeio Alegre, the plane avenue in the Cordoaria.
- News item confirming growth: "Porto tem mais 21 árvores de interesse público",
  https://ambiente.cm-porto.pt/destaque/porto-tem-mais-21-arvores-de-interesse-publico
- **The roteiro is an intention, not a document.** RTP reported the council wanting to
  create a route of classified trees in digital or paper form, explicitly framing tree
  heritage as equal to an architectural monuments route.
  https://www.rtp.pt/noticias/pais/camara-do-porto-pretende-criar-roteiro-de-arvores-classificadas_n750341
  Worth re-checking in a year; if it lands it would be a strong source.
- An academic PDF, "Árvores de Interesse Público da cidade do Porto", is indexed at
  https://core.ac.uk/download/pdf/143400655.pdf but **404s on the fileserver host CORE
  redirects to.** Not verified. It is the most likely per-tree document for Porto and is
  worth one more attempt from a browser or through the originating repository.
- The Jardim Botânico do Porto arboretum documents its own centenarians (a Texas
  madroño and three Java cedars estimated at 120 to 150 years), which is an
  institution-level second source for anything inside it.

**Judgement.** Porto ships 10 trees already and the per-tree backbone we would use is
ICNF, which we hold. The council pages give named examples but no list, so this does not
turn Porto into a cheap pass. The two things worth doing, both small: retry the CORE PDF,
and use the five named council examples as a cross-check on our existing ten.

---

## Bilbao: NO

**Route exists: NO.** This is a genuine blank, and recording it is the point.

- The Basque Government's catalogue of Árboles Singulares, created under the Ley de
  Conservación de la Naturaleza del País Vasco after a study in the early 1990s, holds
  **25 trees for the entire autonomous community**, and they are overwhelmingly rural:
  holm oak, oak, yew, lime, Douglas fir, sequoia, ginkgo, ash, cork oak, stone pine. A
  printed Catálogo de Árboles Singulares exists from the Departamento de Urbanismo,
  Vivienda y Medio Ambiente, ISBN 9788475428253, again a book rather than a web resource.
  The Spanish Wikipedia article on it is a redirect with no table, unlike Madrid's.
- The much-cited "ruta por los 5 árboles singulares de Bizkaia" covers five trees across
  the whole province, none of them in Bilbao city.
- **Bilbao's own inventory of singular trees does not appear to have been published.** It
  was commissioned in 2021 as a clause inside a parks maintenance contract
  (https://www.deia.eus/bilbao/2021/05/05/inventario-arboles-singulares-bilbao-preservara-1964769.html);
  no resulting document was found. Worth re-checking later, because if it was completed it
  would change this verdict entirely.
- What does exist is unofficial: a Sestao botany blog with a three-part series on
  interesting Bilbao trees, and a Bizkaia landscape blog. Named individual trees do appear
  in secondary reporting, notably a camphor tree by the monument pond and a Brachychiton
  populneum near the duck pond in the Parque de Doña Casilda, an oak in Sarriko park, and
  a podocarp, an Erythrina crista-galli and jacarandas around Abandoibarra. The Parque
  Doña Casilda has over 80 tree species catalogued. The council's own park microsite
  (vivirlosparques, Doña Casilda) rendered empty when fetched.
- A book, "Rutas para descubrir árboles monumentales", presented in Bilbao via Ecologistas
  en Acción, offers 35 itineraries, but across the whole territory rather than the city.

**Judgement. Do not open Bilbao on the strength of a route, because there is not one.**
It could still be opened the ordinary way: Doña Casilda alone plausibly holds a walkable
cluster, and Abandoibarra is next to it. But every tree would need building from scratch
against a two-source bar with blogs as the starting point, which is the expensive kind of
pass, and the four-tree floor is a real risk. Rank it below Zaragoza and well below the
deepening work on Madrid, Valencia and Seville.

---

## Coverage of this sweep

All eight cities in the brief were reached: Madrid, Barcelona, Valencia, Seville, Lisbon,
Porto, Bilbao, Zaragoza. No city was skipped for time.

**Fetch blocks encountered, recorded so nobody repeats them.** diario.madrid.es returns
403 to any user agent (Akamai). www.sevilla.org refuses the TCP connection outright from
this environment. cultural.valencia.es refuses connections. www.labienal.com has a broken
certificate chain. core.ac.uk's redirect target 404s. bocm.es, es.wikipedia.org,
zaragoza.es, bcnsostenible.cat, valencia.es, jardins.valencia.es, ambiente.cm-porto.pt and
amja.es all fetched fine.

**One open question worth a run's attention:** whether the data behind Valencia's 508
geolocated monumental trees, delivered through the "València Green Routes" app, is
downloadable under a workable licence. If it is, that is a register-layer import of a size
comparable to Barcelona's, and it is the highest-value unknown left in Iberia.
