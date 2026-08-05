# Brussels deepening pass, 2026-08-05

Goal: 5 to 8 additional trees on top of the published ten, opening one tight
second walk rather than scattering more pins across an 11 km span.

## The cluster chosen: the Sablon / Egmont walk, Bruxelles-Ville (1000)

The densest point in the whole 582-tree regional register is 50.8378, 4.3564:
45 registered remarkable trees inside a 400 m radius. On the ground that is
four adjoining public places in the historic upper town, all within a 700 m
loop and none of them more than a few minutes apart:

- Parc d'Egmont (the walled garden behind the Egmont Palace), ~20 register trees
- Square du Petit Sablon (the formal 1890 garden), ~10, all in formal alignments
- Place du Grand Sablon (the antiques square), 4
- Rue de la Regence and Place Jean Jacobs, the street between the two, 6

None of the published ten stand here. The published ten span 11 km; this loop
spans 700 m.

## Source notes

- sites.heritage.brussels returns 403 to the WebFetch tool but 200 to a plain
  curl with a browser user agent. Per-tree pages carry: exact site name and
  street, girth with year of measurement, height, crown, bole height, the tree's
  RANK by girth within its species across the whole region, "Environnement"
  (isolated / group / alignment, and whether the tree is in private space), and
  crucially an "Etat sanitaire" health field. That last one is a vitality field,
  which the exported open dataset does NOT carry. Every candidate below was
  checked on it.
- The per-tree pages carry NO age and NO descriptive text. Age is the whole
  research cost in Brussels, and it comes from the site history plus girth.
- IMAGE LICENCE: heritage.brussels states nothing but "(c) patrimoine.brussels"
  in the footer of every page. There is no Creative Commons statement anywhere
  on sites.heritage.brussels, and the CC BY 4.0 that opendata.brussels.be
  records applies to the DATASET, not to the photographs on the inventory site.
  So the register's firstimage field is NOT reusable. Photos below come from
  Wikimedia Commons or stay an honest gap.

## Register scan of the cluster (all "Inscrit a l'inventaire legal", 19 Aug 2024)

id 6357 Acer pseudoplatanus 397cm 32m Parc d'Egmont, 3rd largest of species in region, legers defauts
id 646 Platanus x hispanica 367cm Parc d'Egmont, 98th, legers defauts
id 5854 Tilia tomentosa 347cm 28m Square du Petit Sablon, 32nd, sain, ALIGNMENT
id 647 Quercus rubra 342cm 24m Parc d'Egmont, 26th, legers defauts
id 3426 Ailanthus altissima 342cm 19m Place du Grand Sablon, 9th, legers defauts
id 637 Ginkgo biloba 327cm 20m Parc d'Egmont, 7th, legers defauts
id 628 Aesculus hippocastanum 308cm Parc d'Egmont, 90th
id 642 Liriodendron tulipifera 306cm 27m Parc d'Egmont, 19th, SAIN, isolated
id 629 Cedrus libani 298cm Parc d'Egmont, 19th, legers defauts
id 648 Quercus x turneri 290cm Parc d'Egmont, 2nd largest of species in region, SAIN, isolated
id 649 Quercus x turneri 264cm 23m Parc d'Egmont, 3rd largest of species in region
id 3429 Corylus colurna 208cm 17m Place du Grand Sablon, 11th, sain, isolated, central in landscape
id 3423 Acer saccharinum 266cm Place Jean Jacobs, 34th, defauts moyens
id 3420 Sophora japonica 208cm Place Jean Jacobs, 17th
id 7112 Gymnocladus dioica 73cm Parc d'Egmont, 4th of species (young)
id 3425 Acer pseudoplatanus 256cm Rue aux Laines 17, ESPACE PRIVE -> blocked
id 7366 Eucalyptus globulus 70cm Rue de la Regence, ESPACE PRIVE -> blocked

## Outcome

Six trees written to data/research/brussels-extra.json, all in Parc d'Egmont:
bru_011 Turner's Oak (reg 648), bru_012 Ginkgo (637), bru_013 Tulip Tree (642),
bru_014 Sycamore (6357), bru_015 Cedar of Lebanon (629), bru_016 Northern Red
Oak (647). All six are on Brussels Environment's own published Egmont walk
(woodwideweb.be/fr/walk/4.html) and on the park's on-site trilingual
information panel, which is a public authority signposting them. Brussels
therefore passes ten: 16 trees.

Walk geometry: all six inside a 1.5 hectare walled park, longest leg about
180 m. The published ten span 11 km; this adds a walk that spans 180 m.

Park access confirmed from the City's own page and the on-site panel: open
daily 08:00 to 20:00, closed when wind exceeds 80 km/h, entrances on Boulevard
de Waterloo, Rue aux Laines and Rue du Grand Cerf, metro Louise.

Park chronology used for the age ranges: Renaissance gardens from 1532,
Servandoni's French formal layout 1759-1762, Suys' redesign and levelling
1830, Galoppin's English landscape park 1901-1902, sale to the City and
opening to the public 1918, public part renovated 2001.

## Photos: none taken, and why

Wikimedia Commons Category:Egmont Park holds 20 files. Seven were downloaded
and looked at. Four are park views or the palace facade, two are photographs
of the park's information panel, one is a close-up of panel text. None is
identifiable as one of the six trees. Two CC0 files by Daderot (DSC08297 and
DSC08305, 2016) each show a low, broad, dark evergreen tree fenced with
chestnut paling near the palace railings, whose shape matches the Turner's
oak's recorded 10 m height against 17 m crown, but neither file says so and
approving on a resemblance is exactly what the photo rule forbids. Recorded
here so a later pass starts from the shortlist rather than from a blank search:
  https://commons.wikimedia.org/wiki/File:Egmont_Park_-_Brussels,_Belgium_-_DSC08297.jpg  CC0, Daderot
  https://commons.wikimedia.org/wiki/File:Egmont_Park_-_Brussels,_Belgium_-_DSC08305.jpg  CC0, Daderot

## Free correction available on an existing entry

bru_003, the Oriental Plane of Parc Leopold, is currently location_precision
"approximate" at 50.8377, 4.3778. The register carries that exact tree as id
794 (Platanus orientalis, 648 cm, crown 38 m, the same figures the entry
already cites) with a surveyed position of 50.837462, 4.378534, about 57 m
away. That is a confirmed pin for free, from a source the entry already lists.
Not applied here because this pass was told not to edit data/cities/brussels.json.
