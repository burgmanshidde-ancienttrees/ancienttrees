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

