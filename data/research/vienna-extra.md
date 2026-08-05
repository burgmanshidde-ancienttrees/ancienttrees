# Vienna deepening pass, 2026-08-05

Goal: 5 to 8 additional trees that thicken the walks the published ten already
make, drawn from the Naturdenkmal register (data/registers/wien-naturdenkmale.json,
762 declared monuments, 394 single trees) and dated against the Baumkataster
(data.wien.gv.at WFS, layer ogdwien:BAUMKATOGD, published by MA 42 / MA 28,
a different department from the one that runs the monument register).

## The method, so a later pass does not rediscover it

BBOX on the Baumkataster WFS only works with longitude first, despite
srsName=EPSG:4326 and WFS 1.1.0 nominally wanting lat first. The earlier
Vienna run's note that BBOX "returned zero features" is that, not a projection
problem. Working filter:

    CQL_FILTER=BBOX(SHAPE,minlon,minlat,maxlon,maxlat,'EPSG:4326')

Then match the nearest Baumkataster point of the same genus within 25 m of the
register point. Fields that matter: PFLANZJAHR (planting year), STAMMUMFANG
(trunk girth in cm), BAUMHOEHE and KRONENDURCHMESSER (CLASS CODES, not metres,
the readable range is in the _TXT twin field, so BAUMHOEHE 6 means 26-30 m).
Publishing the raw class number as a measurement would be the Portuguese
girth-in-metres mistake all over again.

## How well the two registers agree

50 single-tree monuments sit within 2.2 km of Stephansplatz. 22 of them, 44
percent, have a Baumkataster record of the same genus within 25 m, and 18 of
those carry a usable planting year (four record 0, "not defined"). The 28
misses are not errors, they are a coverage boundary: the Baumkataster is the
CITY's tree register, so it stops at the fence of the federal gardens
(Volksgarten, Burggarten, Augarten, Schoenbrunn all return zero features),
at private courtyards (Singerstrasse 11, Josefstaedterstrasse 17,
Bennogasse 10) and at school and institutional grounds. Where both do cover a
tree the position agreement is startling: median offset 1.3 m, worst case
10.7 m, and eleven of the 22 agree to within a metre.

On age the two corroborate the published city file rather than contradicting
it, twice:

- Mozart-Platane (vie_005), Naturdenkmal 3247601 = BAUM_ID 11097: PFLANZJAHR
  1780, girth 638 cm, height 26-30 m, crown 19-21 m, city tree number N2001.
  The published story says Jacquin planted it "around 1780" and the trunk is
  "roughly six metres around". Both land exactly.
- Stadtpark ginkgo (vie_002), 3257652 = BAUM_ID 194202: PFLANZJAHR 1896,
  girth 295 cm, against a published "planted around 1900".

One caution and one flag:

- In city PARKS the planting year is often the park's own construction year
  rather than a record about the tree. All four Rathauspark monuments read
  1873 or 1876, which is when the park was laid out. Treat a park PFLANZJAHR
  as "no older than", not as a document. Street trees (MA 28) look more
  individual: the Mozart plane's 1780 and the Landesgerichtsstrasse plane's
  1815 are both odd, specific years that no park schedule would produce.
- FLAG, not fixed here: vie_006 "The Founding Plane of Rathauspark" is
  Naturdenkmal 3257649 = BAUM_ID 146731, and the Baumkataster dates it 1876,
  not the 1783 the published story asserts. Its three sibling monuments in the
  same park read 1873. Someone should re-check the "tree catalogue number 252,
  planted 1783" claim against the source it came from.

## Shipped in vienna-extra.json (6 trees, vie_011 to vie_016)

All six sit on the Ring walk the published ten already start, and they turn a
four-stop line into a ten-stop one:

  Schoenbornpark lime (vie_011)
    -> 350 m -> Landesgerichtsstrasse plane (vie_012)
    -> 500 m -> Rathauspark: published vie_006 + fern-leaved beech (vie_013)
    -> 380 m -> Grete-Rehor-Park ironwood (vie_014)
    -> 250 m -> published vie_007 Volksgarten
    -> 950 m -> published vie_001 Singerstrasse
    -> 450 m -> Stadtpark: wingnut (vie_015), published vie_002 ginkgo,
                pagoda tree (vie_016)

Every hop is under a kilometre and most are a five minute stroll.

| id | tree | ND id | BAUM_ID | planted | girth |
|---|---|---|---|---|---|
| vie_011 | Large-leaved Lime, Schoenbornpark | 3257637 | 220685 | 1839 | 489 cm |
| vie_012 | Oriental Plane, Landesgerichtsstrasse | 3257520 | 130254 | 1815 | 445 cm |
| vie_013 | Fern-leaved Beech, Rathauspark | 3257648 | 146749 | 1873 | 600 cm |
| vie_014 | Persian Ironwood, Grete-Rehor-Park | 3257543 | 225310 | 1940 | 460 cm |
| vie_015 | Caucasian Wingnut, Stadtpark | 3257447 | 194189 | 1921 | 308 cm |
| vie_016 | Japanese Pagoda Tree, Stadtpark | 3257446 | 193786 | 1860 | 444 cm |

## FLAG: Vienna passes ten

10 published + 6 here = 16. Before vienna-extra.json is merged into
data/cities/vienna.json, the copy that promises ten has to stop:

- `intro`: "The ten below range from a plane tree..." and "All ten are free to see."
- `meta_description`: "Ten remarkable trees, all free to visit."
- `faq[1].a`: "All ten trees on this list are free to see."
- the page title and the question page, per the count check in
  scripts/build_site.py, which FAILS the build rather than warning.

Not fixed here, per the brief.

## Photos

Three viewed, three approved, which is the per-pass ceiling: the Rathauspark
fern-leaved beech (Michael Kranewitter, CC BY-SA 3.0 AT), the Schmerlingplatz
Persian ironwood and the Stadtpark pagoda tree (both Thomas Ledl, CC BY-SA
3.0 AT). Two more were viewed and rejected rather than approved: the
Schoenbornpark lime, where the trunk hides behind the pond's rockwork, and
two GuentherZ files that turned out to be photographs of the monument plaque
rather than of the tree. The plaques were still worth opening, since the
wingnut's reads "Nr. 280 Kaukasische Fluegelnuss" and independently confirms
which tree carries that designation.

## Leads and blocked

data/leads/vienna.json, 34 leads and 8 blocked. The one lead worth a run on
its own: Naturdenkmal 3257933, a ginkgo the Baumkataster dates to 1864 and
measures at 408 cm, inside the Prater administration grounds at
Vivariumstrasse 17. Older and thicker than the Stadtpark ginkgo we already
publish. Whether anyone can walk to it was not established.
