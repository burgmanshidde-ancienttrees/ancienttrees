# Published tree walks: Germany, France, Benelux and Central Europe

Date: 2026-08-05. Scouting only. No trees researched, no city file written.

**What this is.** Which German, French, Dutch, Belgian, Czech and Hungarian cities already
publish their own tree-by-tree route or per-tree designation list. The reason it exists is
Setubal: a parish there publishes a walking route naming each tree with species, place, age
and height, and one fetch of it independently corroborated nine of our ten entries. That is
the most expensive part of a research pass, the second source, solved in a single request.
Registers give scattered trees; a published route gives a walk, an order and a second source
at once.

**How to read a block.** "Route exists: YES" means the source names trees INDIVIDUALLY with a
location. A page that tells you to wander a park and admire the old trees is recorded as NO,
on purpose: a false positive costs a later run more than a blank does. WEAK means something
real exists but is a tourist article, a newspaper listicle, or a list without locations.

**Standing rule for anything found here.** These are sources to cite and verify against, never
to copy from. No text, no photographs. A licence is noted only where the page states one.

Searched in German, French, Dutch, Czech and Hungarian. English searches miss nearly all of it.

Cities in scope, biggest first: Berlin, Paris, Vienna, Hamburg, Munich, Amsterdam, Brussels,
Prague, Budapest, Lyon, Marseille, Bordeaux. Hamburg, Marseille and Bordeaux are not published
by us and have no imported register, so for those a published route decides whether the city is
worth opening at all. The rest we already publish, so a route deepens an existing page cheaply.

---

_(sweep in progress, blocks appended as each city is checked)_

---

## Berlin — YES, and it is the richest find in this sweep

**Route exists: YES (a per-tree designation list, not a walk).**

**Source 1, the usable one.** German Wikipedia, `Liste der Naturdenkmale in Berlin`, split into
twelve per-Bezirk sub-lists (Mitte, Friedrichshain-Kreuzberg, Pankow, Charlottenburg-Wilmersdorf,
Spandau, Steglitz-Zehlendorf, Tempelhof-Schöneberg, Neukölln, Treptow-Köpenick,
Marzahn-Hellersdorf, Lichtenberg, Reinickendorf). Publisher: Wikipedia volunteers, but the
content is transcribed from the Land Berlin ordinance and geoportal, so it is a mirror of an
official register rather than a blog.
https://de.wikipedia.org/wiki/Liste_der_Naturdenkmale_in_Berlin

**What a row carries.** Checked the Mitte sub-list directly. Columns are: official ND id
(e.g. 1-3/B), German species name, Latin binomial, street address with a site description
("lawn at the corner of Schumannstraße/Luisenstraße"), coordinates with geohack links,
the legal ground for protection (Schönheit, Seltenheit, Eigenart), and a photo linked to
Wikimedia Commons. Mitte alone runs to roughly 60 tree entries.

**What it does NOT carry: age, and no girth either.** That is the single gap, and it is the
expensive one for us, because our schema wants an age estimate and hard rule 2 forbids
inventing it. Expect to need a second source per tree for age (Bezirk pages, monumentaltrees
for verification only, local press).

**Scale.** 708 natural monument objects across Berlin as of April 2025, of which 70 are
glacial boulders and roughly 638 are trees.

**Official layer underneath it.** Land Berlin geoportal / daten.berlin.de publishes
"Schutzgebiete und Schutzobjekte nach Naturschutzrecht Berlin" as WFS, which contains
Naturdenkmale both as areas and as point objects. Licence NOT yet read; a separate dataset,
Baumbestand Berlin (street and park trees), is dl-de/zero-2-0, but that is a full inventory and
hard rule 10 plus the register-layer rules forbid bulk-importing it. Only the Naturdenkmal
selection qualifies.
https://daten.berlin.de/datensaetze/schutzgebiete-und-schutzobjekte-nach-naturschutzrecht-berlin-inklusive-natura-2000-wfs-c36fe3f2

**Walkable?** Not as published: it is city-wide, spread over twelve boroughs. But it has
coordinates on every row, which means `scripts/cluster_register.py` can do the walk-finding
for us, exactly as it did on Portugal's 124 trees. Berlin should produce several genuine
clusters (Tiergarten/Mitte, Pankow, Steglitz-Zehlendorf all look dense).

**Judgement.** This makes a Berlin pass cheap on existence, species and location, and leaves
age as the one thing to hunt. Coordinates plus a Commons photo already attached to many rows is
a rarity in this project. Two-source bar: existence and species clear it immediately (Wikipedia
row plus the Bezirk's own Naturdenkmal page, and several Bezirke publish their own lists, e.g.
Charlottenburg-Wilmersdorf and Mitte on berlin.de). Age will survive on maybe a third to a half.
Realistically 10 of 10 shippable for Berlin, with several already-photographed.

---

## Paris — YES, and it is the single cleanest source in this sweep

**Route exists: YES (an official per-tree register, machine-readable).**

**Source.** Ville de Paris open data, dataset `arbresremarquablesparis`, published by the
Direction des Espaces Verts et de l'Environnement. Queried the API directly rather than the
web page.
https://opendata.paris.fr/explore/dataset/arbresremarquablesparis/table/
API: `https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/arbresremarquablesparis/records`

**Licence: Open Database License (ODbL), stated in the dataset metadata.** That is
attribution plus share-alike on the database, which needs a read before any import; it is not
one of the flat-refusal non-commercial licences.

**Size: 185 records** (last modified 2026-07-31, so it is maintained).

**What a row carries, verified against two real records.** Coordinates (lat/lon), Latin
binomial with taxonomic authority, French common name, site name (Square Georges Cain, Parc
Montsouris), street address, arrondissement, domain type (garden / cemetery / street /
school), trunk circumference in cm, height in m, planting year, the reason it is classified,
a written description of the individual tree, the council deliberation number and date that
classified it, whether it carries the A.R.B.R.E.S. NGO label, a per-tree PDF, and a photo URL.

**Two cautions, both already-known register failure modes.**
1. `arbres_dateplantation` is a corrupt sentinel: both sampled rows carry
   "1700-01-01T00:09:21" which is a placeholder, not a planting date. The usable field is
   `com_annee_plantation`, which honestly says "Inconnue" when unknown. Do not read the
   datetime field as an age. This is exactly the ICNF units error in a different costume.
2. The photos are `Clément Dorval / Ville de Paris` copyright, NOT covered by the ODbL on the
   data. They are a lead for what the tree looks like, never a publishable image. Photos still
   come from Commons/iNaturalist/Flickr per Step 4.

**Walkable?** Distribution is the good kind: 131 in gardens, 37 in the Bois de Vincennes and
Bois de Boulogne, 14 street trees, 9 in cemeteries. With coordinates on every row,
`cluster_register.py` will find real walks (Buttes-Chaumont, the Marais squares, Montsouris,
Père-Lachaise, Jardin des Plantes).

**Judgement.** Paris is already published by us, so this is a deepening source rather than a
new city, and it is the cheapest second source we will find anywhere in France: girth and
height per tree make an age estimate defensible, and the deliberation number is a hard
citation. Two-source bar: essentially everything here clears existence, species and location on
the register alone plus a Commons or A.R.B.R.E.S. cross-check. It also gives Paris an obvious
route to grow past ten if we ever want it.

---

## Germany-wide: the second Wikipedia series, and it is the one that carries age

Found while chasing Hamburg, and it changes the German picture, so it is recorded here once
rather than repeated per city.

Germany has TWO parallel Wikipedia list series, and they are not the same thing:

1. **`Liste der Naturdenkmale in [Land/Stadt]`** — a transcription of the legal protection
   ordinance. Complete, official, address and coordinates, species in Latin. **No age, no
   girth.** Good for existence and location, useless for the age field.
2. **`Liste markanter und alter Baumexemplare in [Bundesland]`** — a curated list of the
   notable and old individual trees. **Columns: photo, tree's own name, genus/species, trunk
   girth with the year it was measured, height in m, approximate age with planting date where
   known, location with neighbourhood, park or street name AND coordinates, district, and a
   characteristics column carrying the superlatives.** Index page:
   https://de.wikipedia.org/wiki/Liste_markanter_und_alter_Baumexemplare_in_Deutschland
   with per-Bundesland pages for all sixteen Länder.

Series 2 is the richer one for us because it is per-tree, named, aged and measured, which is
our exact schema. Its own header is honest about the weakness: most ages are estimates or
local tradition, and only a few are dated by core sample or documents, with the standing
warning that villages routinely call a 400-year linden a thousand-year linden. That is fine,
it is precisely what `age_min`/`age_max` and a flagged status exist for, but it means series 2
is a lead list needing a second source on age, not an authority on it.

**The productive combination is the two together:** series 1 proves it is officially protected
and pins it, series 2 names it, ages it and measures it. Two independent sources on existence
and species in one afternoon of fetching, per Bundesland.

**Worth a proper import pass of its own: yes, for series 2, and it is bigger than this sweep.**
It is a national, per-tree, coordinate-bearing corpus that a script can parse the same way
`cluster_register.py` handles Portugal. It is not an official register though, so under the
register-layer rules it does NOT qualify as the single trusted source a government register
does; it feeds layer 1 as a lead list, with the Land ordinance as the official half.

---

## Hamburg — YES, on a real list, though small

**Route exists: YES (a per-tree list, not a walk).** And this is the city where the answer
decides whether to open a page at all, so it matters that the answer is yes.

**Source 1, the useful one.** `Liste markanter und alter Baumexemplare in Hamburg`, German
Wikipedia (series 2 above).
https://de.wikipedia.org/wiki/Liste_markanter_und_alter_Baumexemplare_in_Hamburg
**23 trees**, each with photo, name, species, trunk girth with measurement year, height,
approximate age, location with coordinates, and district. Ages run 410 to 1000 years, girths
3 to 8.3 metres. Spread across Altona (4, several in Jenischpark), Hamburg-Mitte (3, including
the oldest linden), Eimsbüttel (5), Hamburg-Nord (4), Harburg (1), Wandsbek (1).

**Source 2, official but nearly empty for our purposes.** Hamburg's BUKEA lists only **eleven**
Naturdenkmale for the entire city, and most are not trees at all: they are bracks (tidal
ponds), a moor, a clay pit, and the Alter Schwede glacial boulder. Only two are trees or
tree-adjacent: the yew at Neuländer Deich in Harburg (given as over 200 years by the city,
500 to 1000 by other sources, probably 800 to 850, so a genuine source conflict to state
plainly per P7) and the Garten de l'Aigles in Hamburg-Nord.
https://www.hamburg.de/politik-und-verwaltung/behoerden/bukea/themen/naturschutz/naturdenkmale-52292
There is a downloadable "Liste der Naturdenkmale (2015)" PDF and an interactive protected-areas
map. Hamburg's full Baumkataster (every tree on public land) exists as open data and is
explicitly NOT usable: bulk municipal inventories are excluded by the register-layer rules.

**Ohlsdorf cemetery: recorded as WEAK, deliberately.** 400 hectares, 36,000 trees, over 2,000
of them past 100 years, some 450 species, and it does run a Naturlehrpfad with twenty-plus
interpretive boards from the main entrance at Fuhlsbüttler Straße 756. But the published
material describes the trail and the totals, not individual trees with locations, so it fails
this sweep's own test. It is a strong place to look during an actual Hamburg pass and a
plausible cluster anchor; it is not a second source.
https://www.friedhof-hamburg.de/besucher/park-und-kultur/natur/

**Walkable?** Partly. Jenischpark in Altona is an obvious cluster of its own, Eimsbüttel's five
are a second, and the Harburg yew is a lone outlier across the Elbe. Coordinates on every row
means clustering can be run rather than guessed.

**Judgement.** Hamburg is worth opening. 23 candidates against a four-tree floor and a
ten-tree default is comfortable headroom, the list already carries age and girth, and about
half the rows have a photo attached. Expect maybe 12 to 15 to survive a two-source bar once
the Naturdenkmal ordinance, the Hamburg tree-history pages and local press are cross-checked,
which is more than enough. The one genuine risk is series 2's age inflation, so treat every
"thousand-year" claim as a range to verify.

---

## Munich — YES, and unusually, the primary source is the municipal law itself

**Route exists: YES (an official per-tree ordinance, plus a mirrored list and a map).**

**Source 1, official and primary.** The Naturdenkmalverordnung in Munich's own Stadtrecht,
which IS the list: it names each monument with species, location and quality criteria, because
in Munich the protection is legally attached to named individual trees.
https://stadt.muenchen.de/rathaus/stadtrecht/vorschrift/910/version2/0.html
**117 natural monuments covering 200 individual trees**, and in Munich these are exclusively
trees ("ortsbildprägende Bäume"), no boulders or ponds diluting the count. Each is marked on
the ground by a small triangular sign, white with a green border and a black eagle, which is
a genuinely useful detail for a visitor and for confirming you found the right tree.

**Source 2, the readable mirror.** `Liste der Naturdenkmäler in München`, German Wikipedia,
organised by Stadtbezirk.
https://de.wikipedia.org/wiki/Liste_der_Naturdenkm%C3%A4ler_in_M%C3%BCnchen
Columns: designation with common and scientific species name and the number of trees in the
monument, district plus running number, street address with site description, coordinates in
DMS, the owner and cadastral parcel, the protection rationale, and a photo with Commons links.
**Age and girth are not columns**; they turn up occasionally inside the rationale text.

**Source 3, a map.** stadtgeschichte-muenchen.de runs an interactive Naturdenkmäler map.
Private/association publisher, so a cross-check rather than an authority.
https://stadtgeschichte-muenchen.de/naturdenkmal/naturdenkmal_karte.php

**No Baumlehrpfad or published walking route found for Munich.** Searched in German; the
results are all register and ordinance, no route. So Munich is a register city, not a walk city.

**Walkable?** Organised by Stadtbezirk with coordinates, so clustering is mechanical.
Altstadt-Lehel, Ludwigsvorstadt-Isarvorstadt and Maxvorstadt all appear in the first districts
of the table, which is promising for one central walk; the Englischer Garten and Nymphenburg
are the obvious second and third anchors.

**Caution: the ownership column matters here more than anywhere else in this sweep.** Munich's
list records the owner and cadastral parcel per monument, which means it will openly show
which protected trees stand on private land. Hard rule 10 applies without argument: those are
excluded regardless of how good the tree is. The upside is that Munich, uniquely, tells us
which ones rather than making us guess.

**Judgement.** Munich makes existence, species and location cheap and legally solid, and the
Bavarian `Liste markanter und alter Baumexemplare in Bayern` (series 2) is the natural partner
for age and girth. Two-source bar: existence and species clear at once; age needs the Bayern
list or local press per tree. 200 individual trees against a ten-tree page is enormous
headroom, so Munich's real work is selection and the private-land filter, not discovery.

---

## Vienna — YES, official, open-licensed and with the collectible-point filter built in

**Route exists: YES (an official per-tree register, CC BY 4.0, with coordinates).**

**Source 1, the machine-readable one.** `Naturdenkmäler Standorte Wien` on data.gv.at,
published by Stadt Wien as point geometry.
https://www.data.gv.at/katalog/dataset/stadt-wien_naturdenkmlerstandortewien
**Licence: CC BY 4.0**, Vienna's standard open-data licence, stated on the portal. That is
comfortably inside our register-layer rule (attribution, commercial reuse allowed).
Fields: NATNR (monument number), ARTBEZ (common plant name), WISSBEZ (botanical name), BEZ
(district), ADRESSE (address), ND_TYP (type code).

**ND_TYP is quietly the most valuable field in this whole sweep.** It classifies each monument
into eleven types: individual tree, tree group, tree row, avenue, wood, meadow, special
plant/animal habitat, water body, geological exposure, cultural-historical object, other. That
means the collectible-point test from CLAUDE.md, one identifiable tree rather than an avenue,
can be applied by filtering a column instead of by judgement per row. Nowhere else in this
sweep does a register hand us that.

**Source 2, the human-readable one.** Stadt Wien publishes a page per Bezirk.
https://www.wien.gv.at/umweltschutz/naturschutz/gebiet/naturdenkmaeler/bezirk-01.html
Checked the 1st district directly: 12 entries, each with address, common and botanical species
name and the monument number, at Burggarten, Rathauspark, Stadtpark and Volksgarten. Same
pattern for the other districts. **No age, no dimensions, no photo** on these pages.

**Scale: 434 natural monuments city-wide**, from the Stadtpark ginkgo to the Schönbrunner
Allee in Meidling, and not all of them trees, which is what ND_TYP sorts out.

**Also noted, not needed.** Vienna's Baumkataster (every public tree, with species, planting
year, trunk and crown diameter and estimated height) is online at
wien.gv.at/umweltgut/public/. It is a full municipal inventory so it must never be bulk
imported, but as a per-tree lookup for a shortlisted Naturdenkmal it is a legitimate second
source for planting year and dimensions, which is exactly the gap the ND register leaves.
That pairing makes Vienna's age problem solvable without leaving the city's own data.
An ÖAW-linked phone app (ndque.st) maps the protected trees, and the ground signs are yellow.

**Walkable?** The 1st district alone gives four park anchors within a fifteen-minute walk, and
Vienna's Ring parks are as compact as Cadiz. This is a genuine cluster city.

**Judgement.** Vienna is already published by us; this deepens it very cheaply and could carry
it past ten honestly. Best-structured municipal source in the sweep after Paris, and unlike
Paris the licence is plain CC BY rather than ODbL. Two-source bar: register plus Baumkataster
covers existence, species, location and planting year for most shortlisted trees without a
single web search.

---

## Amsterdam — YES, and it is the closest thing in this sweep to the Setubal case

**Route exists: YES (an actual published walking booklet, tree by tree).**

**Source 1, the walk.** `Langs monumentale bomen in het centrum van Amsterdam`, published by
de Bomenstichting in collaboration with the Gemeente Amsterdam. **7th revised edition, 2025**,
first published 2015, which means it is maintained rather than abandoned. **30 trees selected
from the city centre**, each named with species and planting date; the examples visible on the
publisher's page are the Wilhelminaboom in the Kalverstraat (planted 1898) and a Caucasian
wingnut in the Rijksmuseum garden (planted 1885).
https://www.bomenstichting.nl/winkel/boeken-en-brochures/langs-monumentale-bomen-in-het-centrum-van-amsterdam.html
It is sold in the Bomenstichting web shop **and offered as a free download** from the same
shop page. The exact PDF URL was not captured in this pass; a research run should pull it from
the shop page. Whether the 30 trees form one continuous route or several is not stated on the
news page and should be checked in the PDF itself.

**Why this is the Setubal shape.** A named publisher, thirty individual trees, species and a
planting year per tree, city-centre and therefore walkable, produced with the municipality. If
this delivers what the sample entries suggest, it corroborates most of an Amsterdam page in
one fetch, and planting dates are the strongest kind of age evidence we ever get.

**Source 2, official and mapped.** The Gemeente Amsterdam digital tree map covers every tree
under municipal management and its legend can filter by age. Full inventory, so no bulk
import, but a fine per-tree lookup. The national Bomenstichting register at
monumentalebomen.nl records **257 monumental trees in Amsterdam**; note that the Dutch national
register is CC-BY-NC and stays a lead list only, per OPEN_DATA_SURVEY.md and the register-layer
licence rule. Nothing changes there.

**Source 3, more routes, weaker.** wandelzoekpagina.nl hosts a set of Dutch bomenroutes
including a De Pijp route; IVN Amsterdam and a Noord audio route exist too. Volunteer and
hobby publishers, so WEAK on their own, useful as corroboration.
https://www.wandelzoekpagina.nl/bomenroutes

**Walkable?** Yes, by construction: the booklet is a centre walk.

**Judgement.** The single most actionable find in this sweep for a city we already publish.
Amsterdam is one of our eleven live Dutch cities and the Netherlands is currently parked in
favour of Spain, Japan and Portugal, so this is not urgent, but it is a stored win: when the
Netherlands reopens, Amsterdam's second-source problem is already solved and 30 candidates
with planting dates are sitting there. Expect most of the 30 to clear a two-source bar, since
the booklet is co-published by the municipality that owns the trees.

---

## Brussels — YES, official, CC BY 4.0, and with one serious catch

**Route exists: YES (an official scientific inventory, machine-readable).**

**Source.** `bruxelles_arbres_remarquables` on the Brussels open data portal, published by
**heritage.brussels** (the Direction du Patrimoine Culturel, Urban.brussels), which has been
running a scientific inventory of the region's remarkable trees since 2002.
https://opendata.brussel.be/explore/dataset/bruxelles_arbres_remarquables/table/
API: `https://opendata.brussel.be/api/explore/v2.1/catalog/datasets/bruxelles_arbres_remarquables`

**Licence: CC BY 4.0**, stated in the dataset metadata. Clean.

**Size: 582 records** for the Ville de Bruxelles commune specifically, last modified
2026-08-05, so it is live. Region-wide the inventory database holds around 7,500 trees studied
since 2002, of which roughly 3,500 are on the legal inventory. The 582 is the City-of-Brussels
slice, which is the walkable one anyway.

**Fields, read from the API.** id, common name in French and in Dutch, Latin name, a first
image, legal status in French and Dutch, a rarity flag, trunk circumference, crown diameter,
whether it is a coppice (cepée), a per-tree detail URL in both languages, and both a geo point
and a geo shape. **No age field**, but circumference plus species gets an estimate a long way,
and the per-tree URL pages on sites.heritage.brussels carry written notes and photos.

**The catch, and it is a hard rule 10 catch.** The inventory was surveyed in private spaces as
well as public ones: gardens and interior courtyards. So this dataset contains trees in
people's back gardens, precisely mapped, published by a heritage authority. Those must not
ship, no matter how good. Any Brussels import has to filter on public accessibility before
anything else, and where accessibility is unclear the tree is left out. This is the one source
in the sweep that actively requires that discipline rather than merely benefitting from it.

**Also.** An interactive regional inventory map at arbres-inventaire.irisnet.be, and a public
dossier page on environnement.brussels. reflexcity.net lists the legally classified trees.

**Walkable?** Yes. 582 trees in one commune with point geometry is a clustering problem, not a
discovery problem, and the Parc de Bruxelles, the Botanique, Laeken and the Bois de la Cambre
edge are obvious anchors.

**Judgement.** Already published by us, so this deepens it cheaply, and it is one of only three
sources in the sweep with a stated open licence (Vienna CC BY, Paris ODbL, Brussels CC BY).
Two-source bar: the inventory plus each tree's own heritage.brussels page is effectively two
official documents on the same tree, which is thinner than two independent sources; a third,
non-heritage source is worth having for anything headline. Realistic yield after the
private-land filter is still comfortably more than ten.

---

## Prague — YES, several ways, including a real audio walking trail

**Route exists: YES (an official register, a database site, and one genuine signed trail).**

**Source 1, the register.** `Seznam památných stromů v Praze` on Czech Wikipedia, mirroring the
national památný strom (memorial tree) protection.
https://cs.wikipedia.org/wiki/Seznam_pam%C3%A1tn%C3%BDch_strom%C5%AF_v_Praze
**201 protected trees in Prague** currently; the city's own environment portal gives 196 under
protection as of January 2025, so the two counts differ slightly, which is the usual
register-versus-municipality mismatch and must be reconciled before any page quotes a total.

**Source 2, the city's own table and map.** Prague's environment portal (envis.praha.eu)
publishes a Památné stromy Prahy table and a numbered map where clicking a tree opens its
detail.
https://envis.praha.eu/publikace_zp/CD_PamstromPrahy2011/stromy_p/stromy_t2.htm
https://envis.praha.eu/publikace_zp/CD_PamstromPrahy2011/stromy_p/mapa_strom.htm
https://praha.eu/web/portalzp/pamatne-stromy
Note the 2011 in the path: this is a published CD-era dataset, so it is authoritative on what
was protected then and needs a currency check per tree.

**Source 3, the specialist database.** prazskestromy.cz, a ten-year-old Prague trees database
with a memorial-trees section and a map, plus five printed maps covering the parts of the city.
Association/NGO publisher, so a cross-check rather than an authority, but it is the deepest
Prague-specific tree resource found.
https://www.prazskestromy.cz/stromy/pamatne-stromy/

**Source 4, an actual walk, and it is the Setubal shape.** Praha 12 publishes a naučná
audiostezka starting in Cholupice and ending in Komořany, **8 km, past eight memorial oaks and
one memorial linden**, individually identified.
https://www.praha12.cz/pojdte-poznat-pamatne-stromy-prahy-12/d-36622
Caveat: Praha 12 is outer south Prague, so this is a suburban walk, not a centre one. Nine
trees is close to a full page on its own, and 8 km is longer than our four-to-eight-tree,
two-kilometre walk standard, so it would be a cluster to trim rather than adopt whole.

**Also regional.** Arnika's map of významné a památné stromy for Central Bohemia and Prague.
https://arnika.org/soubory/mapy/mapa-stromu/map.html

**Walkable?** Both: the register spreads over the whole city, but the Praha 12 trail is
pre-clustered and Prague's centre parks (Petřín, Kampa, Stromovka) are dense.

**Judgement.** Prague is already published by us and this is a cheap deepening with an unusual
bonus, a ready-made nine-tree route. No licence was read on any of these sources, so an import
needs that first; for citation-and-verify use, which is what a curated city pass does, licence
is not a blocker. Two-source bar: the Wikipedia register, the city portal table and
prazskestromy.cz are three genuinely different publishers, so most candidates should clear it.

