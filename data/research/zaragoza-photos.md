# Zaragoza: Aragón register + photo hunt (2026-08-05)

## TASK A — Aragón "árboles y arboledas singulares": RESOLVED

Not on the CKAN portal at all. It lives in the IGEAR/IDEAragon GeoServer.

**Working download URLs (GeoJSON, WGS84, no key):**

- 45 singular TREES:
  `https://icearagon.aragon.es/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=VISOR2D:ARBOLESSINGULARES_ES24&outputFormat=application/json&srsName=EPSG:4326`
- 13 singular GROVES (arboledas, polygons):
  `https://icearagon.aragon.es/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=Medio_Natural:rz_arboledassingulares_es24&outputFormat=application/json&srsName=EPSG:4326`

Both saved to `data/registers/aragon-arboles-singulares.geojson` and
`data/registers/aragon-arboledas-singulares.geojson`.

Discovery path, for the record: opendata.aragon.es CKAN API lives at
`/api/3/action/...` (the `/datos/api/...` path returns the Liferay HTML shell) and has
ZERO tree datasets. The catalogue record is in GeoNetwork instead:
`https://icearagon.aragon.es/geonetwork/srv/api/records/RZ.ArbolesSingulares_ES24` /
`RZ.ArboledasSingulares_ES24`, whose only stated link is the generic
`http://idearagon.aragon.es/descargas`. The GeoServer base
`https://icearagon.aragon.es/geoserver/wfs` is undocumented in the metadata; its
GetCapabilities (2.6 MB) is what yields the real typeNames.

**Licence, verbatim from the GeoNetwork record:**

> "Creative Commons Attribution (cc-by) Esta obra está bajo una licencia de Creative
> Commons Attribution 4.0 Internacional"

And the IGEAR blanket statement, verbatim from a sibling record:

> "La información del sector público de la Comunidad Autónoma de Aragón se regirá, con
> carácter general, por la Ley estatal 37/2007, de 16 de noviembre, sobre reutilización
> de la información del sector público. Todos los conjuntos de datos que ofrece el
> Instituto Geográfico de Aragón, si no se indica lo contrario, se publican bajo los
> términos de la licencia Creative Commons Reconocimiento CC-BY 4.0."

So: CC BY 4.0, usable, attribution to Instituto Geográfico de Aragón (IGEAR) /
Gobierno de Aragón.

**Fields carried (trees layer):** objectid, sitecode, sitename, legalfoundationdate,
legalfoundationdocument (link to the BOA decree PDF), sitedesignation ("Natural
Monument"), siteprotectionclassification, designationscheme (IUCN), designation,
codeara, inspireid, localid, namespace, latitude, longitude, utmx, utmy, observations,
esactivo.

**The two things we needed, and neither is there:**
- **NO age field.** Nothing even adjacent (no girth, no height, no measurement date).
- **NO species field.** Species is only inferable from the vernacular `sitename`
  ("Tejo de la Espata", "Haya de la Caseta de Pascual", "Sabina de Villamayor").
- `observations` is null on all 45 rows.

**Zaragoza municipality: ZERO entries.** The register is a rural/protected-nature
instrument, not an urban one. Nearest entries to the city centre:

| km from centre | name | lat | lon |
|---|---|---|---|
| 15.0 | Sabina de Villamayor | 41.70441 | -0.72469 |
| 30.0 | Pino de Valdenavarro | 41.91600 | -0.94219 |
| 38.1 | Sabina Filada Jorge | 41.75176 | -0.45146 |
| 41.1 | Sabina Cascarosa | 41.64587 | -0.39339 |

Villamayor de Gállego at 15 km is technically inside the day-trip boundary but it is a
lone sabina with no cluster around it.

**Verdict:** the file is worth keeping as a layer-2 register for Aragón as a region, and
it is the one open register that covers the province, but it does NOT help Zaragoza's
city page. It gives no age, no species and no urban trees. Zaragoza's ages have to come
from the municipal side (the Ayuntamiento's own "árboles singulares de Zaragoza"
catalogue) or from press, not from here.

## TASK B — photos: ZERO approved. Three honest gaps, and one blocker found.

Sources swept: Commons text search (Parque Bruil, Paraninfo Zaragoza, Calle Asalto
Zaragoza, Centro Cívico Salvador Allende, árbol Zaragoza, Celtis australis Zaragoza),
Commons geosearch 400 m around 41.6497/-0.8674, Openverse (which only mirrors the same
Commons files), iNaturalist geosearch 1 km around Parque Bruil and a bbox over the whole
city centre.

**Commons geosearch around Parque Bruil returns nothing but a Mapillary streetview dump**
(60+ files, all `File:Mapillary (OpYg-YEIRPGx t6WluCwOQ) (robot8a) 2018-07-30 ...jpg`,
CC BY-SA 4.0). Dashcam frames. Not photographs of anything in particular. Do not re-run
this geosearch expecting different results.

**iNaturalist: zero observations within 1 km of Parque Bruil.** The whole city-centre bbox
holds 13 CC-licensed plant observations and every one is a weed or a herb (Malva,
Lythrum, Oxalis, Tribulus). No tree portraits at all. Zaragoza is an iNaturalist desert.

### 1. Almez / Celtis australis, Parque Bruil — NO QUALIFYING PHOTO (and read the blocker)

Everything looked at, and why each fails:

- `File:Parque Bruil 2.jpg` (CC BY-SA 4.0, SimónK) — general park view, a dozen trees, no
  subject. Reject.
- `File:Parque Bruil 7.jpg` (CC BY-SA 4.0, SimónK) — a paved path under canopy, benches.
  Reject.
- `Parque Bruil` (old mill), `3` (ping-pong), `5` (stone sculpture), `6` (playground),
  `8` (football pitch), `9` (skate rink), `10` (swings), `11` (basketball court) — all
  amenity snapshots by the same uploader on one June 2017 walk. None is a tree portrait.
- `File:Homenaje a la Biodiversidad Parque Bruil.jpg` (CC BY-SA 4.0, Campeones 2008,
  2020-08-19) — LOOKED AT. Technically a good image: daylight, colour, sharp, subject
  fills the frame, survives a card crop. And unusable, for two reasons below.

**THE BLOCKER, and it is the most important thing on this page.** That image is the *dead*
almez: a bare trunk carved by sculptor José Llorente in 2017 into "Homenaje a la
Biodiversidad", with owls, a heron and a squirrel cut into the stubs of its limbs. It is
a carcass, so it fails the living-tree rule outright. Worse, it no longer exists:
Parques y Jardines felled the sculpture in July 2022 after xylophagous insects rotted the
wood (arainfo.org, "El Ayuntamiento de Zaragoza tala la escultura del almez del Parque
Bruil"; fabz.es carries the neighbourhood complaint).

**But there is a second, living almez in the same park, and it is a much better tree than
the one on our list.** Sources: hoyaragon.es, aragondigital.es, and the official
Árbol del Año page at `https://www.xn--arbolybosquedelao-uxb.es/almez-del-parque-bruil-zaragoza/`.

- Alive and in good condition. Verbatim: "Si hoy en día luce frondoso y fuerte es gracias
  a un éxito colectivo."
- Age, verbatim and honestly vague: "No hay datos exactos, pero se trata seguramente de
  árbol centenario (según expertos en arboricultura)."
- Girth 4.05 m at 1.30 m. Height 15 m.
- Catalogued as an Árbol Singular Urbano de Zaragoza in 2019; the *other* almez was
  catalogued by the plenary of 28 October 2005.
- **Third in Spain in the national Árbol del Año 2026 vote**, on a popular vote, after
  appearing on RTVE's La Revuelta in November 2025.
- It stands in what were the 19th-century gardens of Don Juan Bruil's estate.

Action for whoever writes zar_001: write it about the LIVING almez, cite the Árbol del Año
page plus hoyaragon, use "centenarian, no exact figure" rather than a number, and mention
the carved dead one only as context inside the story. Do NOT let the 2017 sculpture become
the entry, and do NOT use its photo.

### 2. Tejo / Taxus baccata, Paraninfo Universitario — NO QUALIFYING PHOTO

- `File:Paraninfo Zaragoza 1.JPG` through `5.JPG` (CC BY-SA 3.0, Ajzh2074, all shot
  2013-01-25) — LOOKED AT no. 1: the building facade square-on across the street, January,
  the two street trees in frame bare and cut off at the edges. Building photo. Reject.
- `File:Paraninfo de Zaragoza, fachada Este.jpg` (CC BY-SA 4.0, SimónK, 2017-07-27) —
  LOOKED AT. Well exposed summer colour, but the subject is unambiguously the brick east
  facade; foliage occupies the left margin only and the centre band is entirely masonry.
  Fails the card crop and fails "the tree is the subject". Reject.
- Nothing in Commons is shot inside the railings where the yew stands.

### 3. Gleditsia triacanthos, Parque Bruil — NO QUALIFYING PHOTO

Same Commons set as no. 1. Even if a honey locust appears somewhere in `Parque Bruil 2.jpg`
or `7.jpg`, no individual is identifiable, which fails the "plausibly the specific tree"
test. Reject.

### 4. Plátano / Platanus x hispanica, Calle Asalto — NO QUALIFYING PHOTO

- `File:Calle del Asalto, Zaragoza.jpg` (CC BY-SA 2.0, Juan E De Cristofaro, 2008) —
  LOOKED AT. An aerial down onto the street from a tower, heavily vignetted and
  colour-processed. Fifty trees, none identifiable. Reject.
- The other `Calle Asalto` hits are Barcelona's Calle Asalto and Fortepan archive
  black-and-white, both wrong on both counts.

### 5. Pinus pinea, Centro Cívico Salvador Allende — NO QUALIFYING PHOTO

- `File:Centro cívico Salvador Allende (Zaragoza).jpg` (CC BY-SA 3.0, Escarlati, 2008) —
  LOOKED AT. The old Matadero courtyard with its fountain and statue. Not a tree in the
  frame. Reject.
- Every other "Matadero Municipal" hit is a different town (Mallén, Don Benito,
  Cochabamba, Azul).

### Summary

Zaragoza has no usable open-licence tree photography. Five trees hunted, zero approved,
and the strict standard is what caught it: the single technically-good image in the whole
sweep is a photograph of a dead carved trunk that was cut down four years ago. Approving
from filenames or descriptions would have shipped it.

Photo supply here has to come from UGC or from a Commons uploader who actually walks the
park. Do not re-run this hunt.

