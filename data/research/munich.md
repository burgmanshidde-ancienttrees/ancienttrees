# Munich register pass, 2026-08-05

**Munich was already published on 2026-07-25** (10 trees, `muc_` prefix, 10/10 photos, zero
approximate pins). This pass did not open a city. It mined the full Naturdenkmal ordinance
into `data/leads/munich.json` and answered the question that decides how cheap every other
German city is.

## What Munich's list actually is

Two sources, and unusually the primary one is the municipal law itself.

1. **Naturdenkmalverordnung, Munich Stadtrecht, 21 July 2021.** The protection is legally
   attached to named individual trees, so the ordinance IS the list.
   https://stadt.muenchen.de/rathaus/stadtrecht/vorschrift/910/version2/0.html
2. **`Liste der Naturdenkmäler in München`, German Wikipedia**, the readable mirror,
   organised by Stadtbezirk. This is the one to parse.

**Parsed cleanly: 116 of the 117 monuments, covering 196 individual trees, every one with
coordinates, all inside the Munich bounding box.** Columns: designation with common and
scientific name and the number of trees, Stadtbezirk plus running number, street address with
site description, coordinates, owner and cadastral parcel, protection rationale, Commons photo.
The coordinates are published as decimal degrees despite the column being labelled DMS, so no
conversion is needed and none was done.

## The three filters, and how much each one costs

Of 116 monuments, only 34 survive as candidates. The filters matter more than the list:

| Filter | Removed | Note |
|---|---|---|
| Private ownership (hard rule 10) | **51** | The ownership column is machine-readable, value `privat`. 44 percent of Munich's protected trees are on private land. |
| Group monuments (not a collectible point) | 12 | The designation column carries a leading count: `6 Eiben`, `8 Eiben`, `5 Platanen`. This is why 117 monuments cover 196 trees. |
| Public owner but no public access | 8 | The filter nobody plans for. `Schulhof`, `Innenhof`, `im Hof des Landratsamtes`, `Innenhof des Klinikums`, `rückwärtiger Garten`. **Owned by Stadt München and still not somewhere a visitor may walk.** Ownership and access are different things and the ordinance records only the first. |
| Already published by us | 11 rows | Matched by distance, not by name. |

## Vitality: checked, and Munich hands it over

The Wikipedia list carries a second table, `Ehemalige und abgegangene Naturdenkmäler`, five
entries, with reasons in plain text: one replaced by a young tree, one `Baum ist nicht mehr
vorhanden`, one burnt in 2004 with `nichts mehr von dem Naturdenkmal vorhanden`. This is the
vitality field no register normally has.

**Checked all five against all 10 published Munich trees by coordinate. None match.** Nothing
we publish in Munich is dead or delisted. That check is now cheap to repeat.

## Age is the real cost here, and the Bavarian list does not fix it

The sweep note predicted `Liste markanter und alter Baumexemplare in Bayern` would supply age
and girth. **It does not, for Munich.** The Bayern list is a rural list of village lindens and
oaks; searched in full, it contains exactly **one** tree inside the city: the Röth-Linde, which
we already publish. It does usefully corroborate it (`6,24 m` girth, `300` years, and the
characteristics column says `ältester Baum Münchens`), which is a real second source for the
oldest-tree dispute already recorded on that page. Beyond that one tree it is empty for Munich.

That is why 6 of our 10 published Munich trees carry an honest `undated` age, and why all 34
leads do too. The ordinance has no age column and no girth column.

## The better age source, found this pass: baumkunde.de

**`baumkunde.de/baumregister/`** is a per-tree German register with numbered entries carrying
species, trunk girth with measurement year, height, an age estimate, coordinates and a named
contributor. Worked example, fetched and confirmed: the Sommerlinde at the Badenburger See in
Nymphenburg, register 4054, gives `4.2 m` girth measured 1 November 2014, `19.0 m` height and
an estimated age of **180 years**. That figure is independently plausible: Sckell redesigned
the park into an English landscape park 1799 to 1823, so a tree of about 190 years today sits
exactly on that planting.

**Status: a lead source, not an authority.** It is community-compiled, not a government
register, so under the register-layer rules it does not carry a tree on its own. But as the
*second* source on age, paired with the ordinance for existence, species and location, it is
the missing half of the German two-source problem. Worth a proper look on its own; it is
national, per-tree and numbered, which is what a script can walk.

## The cluster worth writing: Schlosspark Nymphenburg

Five clean candidates, plus `muc_007` (the Dörfchen oak) which we already publish, giving a
**six-tree walk inside one park, spread 1.3 km, free entry, all daylight-photographed on
Commons already**. This is the best density in Munich by a distance.

| Species | Coordinates | Where | Commons image |
|---|---|---|---|
| Copper Beech (Fagus sylvatica f. purpurea) | 48.15403, 11.49411 | 25 m south of the Badenburg | `Nymphenburg Blutbuche Badenburg-1.jpg` |
| Large-leaved Lime (Tilia platyphyllos) | 48.15455, 11.49324 | 50 m northwest of the Badenburg, on the lake shore | `Naturdenkmal Sommerlinde am Badenburger See im Winter.jpg` |
| Fern-leaved Beech (Fagus sylvatica f. asplenifolia) | 48.15528, 11.50042 | fork in the path 50 m south of the Amalienburg | `Schlosspark Nymphenburg Naturdenkmal Farnblaettrige Buche-1.jpg` |
| Weeping Beech (Fagus sylvatica f. pendula) | 48.15755, 11.49961 | south of the Schwanenbrücke | `Hängebuche im Schlosspark Nymphenburg.jpg` |
| Small-leaved Lime (Tilia cordata) | 48.16022, 11.50802 | Nördliches Schlossrondell 8, rear garden | `Naturdenkmal Winterlinde Schlossrondell München.jpg` |

Three cautions for whoever writes these:

- **The Schlossrondell lime is the weak one.** `rechts im hinteren Gartenteil` of a building on
  the Rondell reads as a rear garden, not open park. Confirm access on the ground evidence
  before it ships, or drop it and ship five.
- **The Fern-leaved Beech name collides.** `muc_006` is already "The Fern-leaved Beech", in the
  Englischer Garten. Two trees of the same cultivar in one city need distinct names.
- **The lime by the lake has a real winter case.** Its own protection reason is `Bizarrer und
  knorriger Wuchs`, bizarre and gnarled growth, and the Commons photograph the register links
  is deliberately a winter shot. That is a genuine `bare silhouette` best_time, not an invented
  one. But the photo is bare-winter, which the Cadiz standard would want checked against the
  "daylight, colour, tree fills the frame" test before approval.

## Two other clusters, weaker

- **Altstadt-Lehel and Au-Haidhausen, 8 candidates across 2.9 km.** Too spread to be one walk,
  but it splits: St.-Anna-Platz, the Wilhelmsgymnasium green and the Herrnschule hornbeam sit
  within 700 m of each other in Lehel.
- **Nymphenburg's yews are the ones to regret.** Two monuments, `6 Eiben` and `8 Eiben`, both
  described as probably unique in the city at that size, both blocked as groups rather than
  collectible points. Correct call, and worth recording that the call was made deliberately.

## How cheap is the rest of Germany

Cheaper than this pass makes it look, with one caveat.

- **Existence, species, location, protection and ownership: nearly free.** Every German city
  and Landkreis has a `Liste der Naturdenkmale in [X]` on Wikipedia in this same wikitext table
  shape. The parser written for this pass is generic; it took one pass to build and will run on
  any of them.
- **The private-land and access filters are also free**, because the ownership column and the
  site description are both in the table. Munich is not special here, it is the pattern.
- **Age is never in these tables**, in any Bundesland. That is the whole cost of a German city,
  and it is per tree. The two ways out are `Liste markanter und alter Baumexemplare in
  [Bundesland]` (rich, but rural: it missed Munich almost entirely, so expect it to be thin for
  any big city) and baumkunde.de (per-tree, urban, has ages, but community-sourced).
- **Bavaria publishes nothing wider that helps.** No state-level open tree register with ages
  was found. The Land-level Wikipedia series is the widest thing there is.

So a German city is cheap to *scope* and expensive to *date*, and the honest option already
established on Munich's own live page is to ship with the register's protection rationale and
an explicit undated statement, which is what 6 of its 10 trees already do.
