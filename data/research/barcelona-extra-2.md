# Barcelona, second deepening pass (2026-08-05), the Montjuic walk

Deliverable: `data/research/barcelona-extra-2.json`, six trees, ids bcn_017 to bcn_022.
`data/cities/barcelona.json` was NOT edited.

Goal set in the brief: open one clean new walk in a single neighbourhood rather than
scatter. Chosen: **Montjuic**, because it is the only untouched cluster in Barcelona
that is (a) somewhere travellers already go, (b) dense enough to walk, and (c) mostly
free, which the two published Montjuic trees (bcn_005, bcn_006) are not, they sit
behind the botanical garden's paid gate.

Candidate screen: `data/registers/barcelona-ail.json` filtered to units == 1,
ownership not private, and inside the Poble-sec / Montjuic ring. Cross-checked against
OpenStreetMap, which carries the same municipal catalogue as independently surveyed
nodes, and against the Generalitat's monumental-tree register, which is a genuinely
separate authority.

## What shipped

| id | tree | year | pin | photo |
|---|---|---|---|---|
| bcn_017 | Lagunaria, Jardins del Teatre Grec | 1923 | confirmed | approved |
| bcn_018 | Bunya Pine, Jardins del Teatre Grec | 1920 | confirmed | none, only image is CC BY-NC |
| bcn_019 | Coral Tree, Teatre Grec to Laribal path | 1923 | approximate | approved |
| bcn_020 | Tipu Tree, placa Carles Buigas | 1925 | approximate | none |
| bcn_021 | Narrow-Leaved Ash, Sot de l'Estany | not recorded | approximate | none, see below |
| bcn_022 | Sycamore, Sot de l'Estany | not recorded | approximate | none, see below |

Two photos approved, both viewed as pixels before approval, both Commons CC BY-SA 3.0
by pere prlpz. Well inside the three-per-pass ceiling.

The walk: the three Teatre Grec trees stand within 130 m of each other; the Tipu Tree
is 450 m north at the foot of the hill by the Magic Fountain; the two monumental trees
in the Sot de l'Estany are 600 m south and join bcn_005 and bcn_006 in the same ravine.
Montjuic goes from two trees behind one paid gate to eight, four of them free.

**bcn_021 and bcn_022 complete a claim the published page already makes.** Barcelona's
intro says the Catalan government's monumental designation belongs to only four trees
in the city, all four in the Sot de l'Estany. Two of the four were already published
(bcn_005 wingnut, bcn_006 green ash). These are the other two, so the quartet is whole.

## OSM cross-check (Overpass, 2026-08-05)

| Register entry | Register coord | OSM node | Offset | OSM species |
|---|---|---|---|---|
| Lagunaria dels jardins del Teatre Grec | 41.36980, 2.15944 | 4492855030 | 0 m | Lagunaria patersonia |
| Araucaria del Teatre Grec | 41.37038, 2.15920 | 4506691425 | 6 m | Araucaria bidwillii |
| Eritrina dels jardins del Teatre Grec | 41.36928, 2.15860 | 4492857600 | 12 m | Erythrina lysistemon (!) |
| Huingan del carrer Joaquim Blume | 41.37211, 2.15533 | 4506714524 | 9 m | Schinus polygamus (!) |
| Tipuana de la placa Carles Buigas | 41.37208, 2.15334 | none | n/a | n/a |
| Araucaria de l'av. Francesc Ferrer i Guardia | 41.36966, 2.14873 | none within 400 m | n/a | n/a |
| Freixe and Fals platan del Jardi Botanic | see below | none | n/a | n/a |

## Access finding that applies to three entries

The Jardins del Teatre Grec close to the public every year for the Grec festival.
Barcelona's own facility record states it flatly: "Amb motiu del Festival Grec els
jardins romandran tancats al public entre els dies 15 de juny i 7 d'agost", which is
why the garden's own URL slug carries "tancat". Hours otherwise are 08.00 to 21.00 from
1 April to 31 October and 08.00 to 19.00 from 1 November to 31 March. Every Teatre Grec
entry says this, because the closure covers exactly the weeks a summer visitor comes,
and it is also why bcn_017's `best_time` is June alone rather than June and July.
Source: guia.barcelona.cat/es/detall/jardins-del-teatre-grec_99329085040.html

## Two species disputes, handled differently

**The coral tree (bcn_019) shipped, flagged, with the dispute as the story.** Three
sources give three names: barcelona.cat and bcnsostenible say *Erythrina corallodendron*,
our import of the city's open data says *Erythrina falcata*, OSM node 4492857600 says
*Erythrina lysistemon*. The species field follows the municipal record and the Commons
category, which is the majority and the only reading carrying a descriptive assessment,
and the story names all three out loud. Existence, position and age are not in doubt.

**The huingan (carrer Joaquim Blume) did not ship,** and is now a lead. The register
says *Schinus longifolia*, OSM says *Schinus polygamus*, and huingan, the common name
the city itself uses, is the Chilean name for *S. polygama*. With the build now failing
rather than warning on species naming, a contested binomial is not worth the risk for a
tree 8 m tall. One good leaf photograph resolves it and it ships.

## The Generalitat register, which nobody had used here before

Catalan Wikipedia's *Llista d'arbres monumentals de Catalunya* mirrors the Generalitat's
own monumental-tree files and carries all four Montjuic trees with codes, coordinates
and dimensions (height x girth x crown):

- MA-13.931.01 Noguera Alada de Montjuic, *Pterocarya x rehderiana*, 32.0 x 3.8 x 27.0, 41.367002 / 2.151885
- MA-13.931.02 Freixe de Montjuic, *Fraxinus angustifolia*, 29.0 x 2.5 x 15.4, 41.366939 / 2.151886
- MA-13.931.03 Freixe America de Montjuic, *Fraxinus pennsylvanica*, 32.0 x 3.16 x 24.0, 41.367127 / 2.151752
- MA-13.931.04 Platan Fals de Montjuic, *Acer pseudoplatanus*, 30.0 x 1.38 x 12.0, 41.366884 / 2.151851

All four stand inside a 30 m circle at the bottom of the quarry pit. Because the
individual trees are 7 m apart and the two official coordinate sets differ by 18 to
22 m, both new ravine pins are marked **approximate** on purpose: the pin gets someone
into the right corner and the garden's own labels do the rest.

### A pin correction for bcn_005 that this pass did not act on

OSM carries **two** wingnut nodes in the ravine, 52 m apart:

- node 4506713800 at 41.367055 / 2.152202, tagged `Arbre Monumental (MA-13.931.01)`
- node 6924253587 at 41.36731 / 2.15273, tagged `Arbres d'interes local... Sector de l'estany`

bcn_005 currently uses the second. The Generalitat's own coordinate for MA-13.931.01
is 41.367002 / 2.151885, which is 27 m from the first node and 78 m from the one we
publish. **bcn_005's pin is probably about 70 m off and should move toward the
Generalitat coordinate.** Not changed here because the brief forbids editing
barcelona.json; recorded so the next pass gets it for free.

### And a photo problem worth keeping

The Generalitat published a photograph of each monumental tree on Commons under its
`attribution-gencat` open licence, licence-reviewed in 2017. Both were viewed directly
and neither was used:

- *File:Freixe de Montjuic.jpg* is a dark shaded ravine in which an araucaria takes the
  foreground and no ash is identifiable. Fails the Cadiz standard on every count.
- *File:Platan Fals de Montjuic.jpg* shows a slender tree with **pinnate compound
  leaves**, which is an ash. *Acer pseudoplatanus* has palmate lobed leaves. Either the
  file is mislabelled or the photographer shot the wrong trunk in a ravine where the ash
  stands seven metres away. The identification of bcn_022 rests on two official
  registers, not on this photograph, so the entry stands and the photo does not.

## Sources that carried the pass

- **catacultural.com/jardins-del-teatre-grec** is the second source for all three Teatre
  Grec trees and it is independent of the city: it names each one and says where it
  stands ("a l'esquerra de l'amfiteatre, a sota del restaurant" for the lagunaria,
  "abans d'arribar al mirador" for the araucaria, "al cami que comunica els Jardins del
  Teatre Grec amb els Jardins Laribal" for the coral tree). Worth remembering as a type:
  a local culture blog that walks a garden tree by tree is the cheapest second source
  there is, and it is the same pattern as the Setubal roteiro.
- **museuciencies.cat** on the April 2025 monumental declaration, for the four-degree
  microclimate figure and the tallest-in-Catalonia claim.
- **ca.wikipedia Llista d'arbres monumentals de Catalunya**, which mirrors the
  Generalitat files and is the fastest way into them.
- Reminder that held all pass: barcelona.cat, guia.barcelona, ajuntament.barcelona.cat
  and bcnsostenible are four renderings of one municipal record, not four sources.

## How much of the register is left

208 entries in `data/registers/barcelona-ail.json`. After this pass:

- 29 sit within 60 m of a tree we publish or propose
- 61 are named in `data/leads/barcelona.json` as leads or blocked
- **118 are genuinely untouched**, never published and never screened

Where the 118 are: Sarria-Sant Gervasi 34, Les Corts and Pedralbes 17, Eixample 13,
Sant Andreu 13, Nou Barris 10, Horta-Guinardo 9, Sant Marti 8, Ciutat Vella 7,
Gracia 5, Sants-Montjuic 1.

**Montjuic is now finished**: one untouched entry left in the whole district. The next
walk is the Pedralbes and Sarria block, which the earlier pass already flagged as the
strongest untouched cluster in the city, and it is now the largest by a wide margin.

## If these six get merged

Barcelona goes from 16 trees to 22, so the copy that promises a count has to move with
it. `meta_description` currently ends "and fifteen more"; the build's count-promise
check fails the deploy on that. The oldest-tree copy needs no change: nothing here
competes with the Gracia holm oak or the Park Guell olive, and bcn_021 and bcn_022
carry no age at all.
