# CITY_QUEUE: the one list, the one order, and how far to take a city

Written 2026-08-11 because Hidde said what everyone could see: "there are
multiple city prioritisations living amongst each other". There were six, and
they disagreed. This file replaces all of them. If another document names a
city order, it is stale and this one wins.

## The rule, derived from our own numbers rather than chosen

Search Console says something consistent and slightly uncomfortable: **the more
famous a city is, the worse we do there.** Clicks per 100,000 English Wikipedia
pageviews, measured on the cities that have appeared in a digest:

| city | demand | CTR | clicks per 100k views |
|---|---:|---:|---:|
| Porto | 120k | 13.9% | 4.15 |
| Lisbon | 202k | 5.1% | 3.96 |
| Cadiz | 79k | 12.5% | 2.53 |
| Kyoto | 142k | 3.8% | 2.11 |
| Vienna | 283k | 4.5% | 1.41 |
| Bologna | 146k | 7.4% | 1.37 |
| Prague | 303k | 4.7% | 1.32 |
| Amsterdam | 294k | 1.3% | 1.02 |
| Rome | 359k | 1.2% | 0.56 |
| Athens | 235k | 4.0% | 0.43 |

Everybody writes about Rome's trees and nobody writes about Porto's, so we rank
in Porto and we do not rank in Rome. Depth does not fix that: Rome is our
deepest page at 24 trees and takes zero clicks on 165 impressions.

So the score is **demand times our realised yield**, and yield comes from
evidence in this order:

1. **Measured**, where Search Console has spoken. Ten cities.
2. **Published and never once ranked** counts as measured too, and it is the
   correction that matters most. New York, London, Paris, Berlin, Chicago,
   Washington DC, Boston, Singapore and Hong Kong are all live, several are
   deep, and not one has ever appeared in a digest's top pages. Absence of
   clicks on a published page is evidence, not missing data. They score at 0.25.
3. **Predicted** for unpublished places, from the band: 2.50 under 200k views,
   2.20 up to 280k, 1.08 above (contested).

## How far to take a city, and when to stop

The floor is unchanged: four verified trees or no page.

**A lot of cities at 10 to 25 trees, and deepen later.** Hidde, 2026-08-12:
"ik denk dat we veel beter een hoop steden met 10-25 bomen en dan later
verdiepen." So the `target` column is one ceiling for everyone who has something
to work with, and it is 25. Breadth is the phase, and a good afternoon does not
scale with a city's population.

    supply = register trees within 5 km + leads already ready to write

| supply | target | what it means |
|---|---:|---|
| under 10 | none | the city gets whatever verifies, usually 4 to 10 |
| 10 or more | 25 | the first-version ceiling, the same everywhere |

Of 95 live cities, 68 have almost nothing cheap within reach and 27 do, so for
two thirds of the map the count is settled by what exists rather than by
ambition. Regenerate with `python3 scripts/city_queue.py`.

**Past 25 is deepening, not a target.** It is a later decision, taken on a city
that has actually shown demand, and taken with Hidde. A city already past it is
finished rather than over budget: Barcelona publishes 46 and nothing is ever
removed to meet a number.

**The first version of this column was wrong, and the record is kept because the
mistake is instructive.** It banded the target by how much supply sat nearby and
handed 50 to cities with 200+ supply and measured demand, 30 to the rest. That
gave Vienna 50 and Barcelona 30: comparable supply, opposite targets, decided by
whether Search Console had spoken rather than by anything about their trees, and
Barcelona is the city he had called the mega city. His reply was one line:
"maar waarom in godsnaam 50 doel bij wenen". The fault underneath is worth
remembering whenever a number gets scaled by a register count: **a register
measures how EASY trees are to find, never how GOOD they are.** Amsterdam's
4,993 nearby entries are a municipal inventory, not 4,993 trees that clear our
bar.

**Three things the target is not.** Not a quota: the bar per tree does not move
and padding stays forbidden, so a city that runs out of trees clearing the bar
is finished below its target. Not a floor. And a dash is not missing data, it is
the answer: no cheap supply, so no push, which is why Prague sits third on
demand with no target.

**This replaces "a city is finished at three walks" as the stopping rule.** The
three-walk line survives where it was always right, which is what the PAGE leads
with: a reader gets the best three walks, and trees beyond them stay published,
on the map, collectible, listed below. Barcelona's 46 across 7 walks was never
wrong as data, only as presentation. A walk is still 4 to 8 stops averaging at
least 3 stops per kilometre; below that it is a hike, and Cadiz still reads
better at 5 trees in 0.9 km than Barcelona does at 46.

Nothing here re-opens whether a tree may be published: per the 2026-08-10
ruling, only the hard rules and an unstatable location can stop that.

Deep enough, per Hidde 2026-08-08, unchanged: at least one complete walk of 4
to 8 trees inside roughly 2 km, photographs on most of that walk, honest pins
(labelled honestly, NOT confirmed), season data where it is real.

## Ready to run: Lisbon and Porto from the ICNF register

Parked 2026-08-11 at Hidde's request ("ik heb momenteel niet de tokens om
Portugal aan te vullen, kun je het opslaan als to do voor morgen"). The
expensive half is the writing; the free half is already done and on disk.

**The measurement.** The ICNF register holds 555 trees with coordinates under
CC BY 4.0. Seventy-seven of them are trees we already publish. **478 are
unused**, and they sit where we already win: 44 in Lisboa, 21 in Porto, the two
best-converting pages on the site.

**The candidates are generated and waiting** in
`data/research/portugal-register-candidates.json`: every entry carries species,
age, girth, height and a surveyed coordinate straight from the register, so a
pass does no discovery at all. Lisbon has 24 of 44 fully populated, Porto 15 of
21. New ids start at `lis_022` and `por_019`.

**What the pass still has to do,** because the register cannot: confirm each
tree is alive, and confirm the public can actually reach it. Hard rule 10 is
the live risk here, not a theoretical one: Porto's 300-year tulip tree on Rua
Joao de Deus stands in a school yard and must not ship. Register ages are the
age at last measurement, so add the years since and say so.

**Cost.** Yesterday's 18-tree Barcelona batch ran at 11.9k tokens per published
tree, the cheapest the project has measured. Thirty trees across the two cities
is therefore roughly 360k, in two batches of about fifteen, one per city, so
each pass amortises one city's context.

**Why this outranks opening a new city.** Every added tree is its own page on a
precise, uncontested query, and measured CTR on tree pages runs 12 to 50
percent against about 1 percent on big-city pages. The three-walk cap does not
block it: the cap limits walks presented, not trees published.

## The order

Work top-down. Reader submissions and a broken site still outrank everything.

**The source is `data/city-queue.json`, not this table.** Hidde asked for one
source file carrying the priority of the 100 cities and the tree target per city
(2026-08-12), and this is the rendering of it. Everything measurable in the row
(trees, photos, walks, register, target) is recomputed by
`python3 scripts/city_queue.py` and written into the json first; `score`,
`demand` and `basis` are the session-decided columns and live there too.
`data/city-list.json` is generated from the same source as the inventory the
site and scripts read. Editing a row here by hand makes a second source again,
so qa.py fails the deploy when the table and the json disagree.

| # | city | score | demand | trees | photos | walks | register | target | basis |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Lisbon | 7.99 | 201,877 | 33 | 10 | 3 | 66 | 25 | measured |
| 2 | Porto | 5.00 | 120,415 | 27 | 5 | 2 | 40 | 25 | measured |
| 3 | Prague | 4.00 | 303,350 | 17 | 13 | 3 | - | - | measured |
| 4 | Vienna | 3.99 | 283,090 | 22 | 13 | 4 | 377 | 25 | measured |
| 5 | Amsterdam | 3.00 | 294,030 | 20 | 7 | 2 | 4993 | 25 | measured |
| 6 | Kyoto | 3.00 | 142,353 | 18 | 8 | 2 | - | - | measured |
| 7 | New York | 2.81 | 1,124,326 | 20 | 5 | 2 | - | - | published, never ranked |
| 8 | Singapore | 2.42 | 967,821 | 7 | 3 | 1 | - | - | published, never ranked |
| 9 | Galway | 2.20 | 88,162 | - | - | - | - | - | predicted (thin competition) |
| 10 | Nagoya | 2.09 | 83,437 | - | - | - | - | - | predicted (thin competition) |
| 11 | Jaipur | 2.06 | 82,569 | - | - | - | - | - | predicted (thin competition) |
| 12 | Rome | 2.01 | 358,876 | 24 | 9 | 2 | 32 | 25 | measured |
| 13 | Bologna | 2.00 | 146,161 | 11 | 8 | 2 | 8 | - | measured |
| 14 | Cadiz | 2.00 | 79,226 | 5 | 4 | 1 | - | - | measured |
| 15 | London | 1.80 | 718,291 | 23 | 10 | 1 | - | - | published, never ranked |
| 16 | Agra | 1.77 | 70,904 | - | - | - | - | - | predicted (thin competition) |
| 17 | Hong Kong | 1.72 | 689,212 | 6 | 2 | - | - | - | published, never ranked |
| 18 | Chiang Mai | 1.66 | 66,541 | - | - | - | - | - | predicted (thin competition) |
| 19 | Washington DC | 1.52 | 606,731 | 14 | 1 | 2 | - | - | published, never ranked |
| 20 | Kobe | 1.37 | 54,798 | - | - | - | - | - | predicted (thin competition) |
| 21 | Paris | 1.31 | 524,268 | 25 | 9 | 3 | 128 | 25 | published, never ranked |
| 22 | Chicago | 1.21 | 485,769 | 6 | - | - | - | - | published, never ranked |
| 23 | Salamanca | 1.20 | 47,897 | - | - | - | - | - | predicted (thin competition) |
| 24 | Berlin | 1.03 | 412,181 | 18 | 11 | 1 | 114 | 25 | published, never ranked |
| 25 | Athens | 1.01 | 235,429 | 12 | 6 | 2 | - | - | measured |
| 26 | Tokyo | 0.99 | 394,702 | 10 | 8 | - | 7 | - | published, never ranked |
| 27 | Boston | 0.96 | 385,902 | 10 | 1 | 1 | - | - | published, never ranked |
| 28 | Barcelona | 0.87 | 346,477 | 46 | 12 | 7 | 183 | 25 | published, never ranked |
| 29 | Coimbra | 0.87 | 34,962 | - | - | - | - | - | predicted (thin competition) |
| 30 | Braga | 0.86 | 34,522 | - | - | - | - | - | predicted (thin competition) |
| 31 | Kamakura | 0.84 | 33,492 | - | - | - | - | - | predicted (thin competition) |
| 32 | Istanbul | 0.83 | 333,027 | 14 | 4 | 1 | - | - | published, never ranked |
| 33 | Edinburgh | 0.73 | 292,981 | 15 | 4 | 1 | - | - | published, never ranked |
| 34 | Budapest | 0.71 | 283,807 | 12 | 1 | 3 | - | - | published, never ranked |
| 35 | Madrid | 0.69 | 274,553 | 17 | 10 | 2 | - | - | published, never ranked |
| 36 | Denpasar | 0.69 | 27,679 | - | - | - | - | - | predicted (thin competition) |
| 37 | Venice | 0.67 | 267,527 | 11 | 6 | 1 | 4 | - | published, never ranked |
| 38 | Kanazawa | 0.64 | 25,778 | - | - | - | - | - | predicted (thin competition) |
| 39 | Glasgow | 0.63 | 253,705 | 4 | 2 | - | - | - | published, never ranked |
| 40 | Dublin | 0.60 | 240,850 | 17 | 4 | 2 | 12 | 25 | published, never ranked |
| 41 | The Hague | 0.59 | 236,723 | 5 | 1 | 1 | - | - | published, never ranked |
| 42 | Munich | 0.56 | 224,067 | 22 | 13 | 3 | - | 25 | published, never ranked |
| 43 | Bangkok | 0.56 | 222,206 | 5 | - | 1 | - | - | published, never ranked |
| 44 | Copenhagen | 0.55 | 218,621 | 13 | - | 2 | - | - | published, never ranked |
| 45 | Milan | 0.53 | 212,705 | 18 | 9 | 2 | 25 | 25 | published, never ranked |
| 46 | Seoul | 0.52 | 206,265 | 8 | 5 | 1 | - | - | published, never ranked |
| 47 | Naples | 0.50 | 198,913 | 17 | 3 | 2 | 46 | 25 | published, never ranked |
| 48 | Warsaw | 0.49 | 197,929 | 5 | 3 | - | - | - | published, never ranked |
| 49 | Stockholm | 0.47 | 188,184 | 4 | 3 | - | - | - | published, never ranked |
| 50 | Florence | 0.46 | 184,099 | 22 | 7 | 3 | 27 | 25 | published, never ranked |
| 51 | Oslo | 0.45 | 181,113 | 4 | - | - | - | - | published, never ranked |
| 52 | Thessaloniki | 0.45 | 180,145 | 4 | - | 1 | - | - | published, never ranked |
| 53 | Belgrade | 0.45 | 178,116 | 4 | 4 | - | - | - | published, never ranked |
| 54 | Brussels | 0.44 | 176,863 | 16 | 4 | 1 | 371 | 25 | published, never ranked |
| 55 | Seville | 0.43 | 170,545 | 16 | 6 | 2 | - | 25 | published, never ranked |
| 56 | Reykjavik | 0.42 | 166,789 | 4 | - | 1 | - | - | published, never ranked |
| 57 | Bristol | 0.41 | 163,983 | 5 | 1 | - | - | - | published, never ranked |
| 58 | Osaka | 0.41 | 163,112 | 4 | 1 | - | - | - | published, never ranked |
| 59 | Geneva | 0.41 | 162,269 | 6 | 4 | 1 | - | - | published, never ranked |
| 60 | Valencia | 0.41 | 162,209 | 16 | 2 | 2 | 347 | 25 | published, never ranked |
| 61 | Helsinki | 0.37 | 148,908 | 8 | 1 | - | - | - | published, never ranked |
| 62 | Turin | 0.37 | 147,456 | 8 | 7 | 2 | 32 | 25 | published, never ranked |
| 63 | Genoa | 0.36 | 145,206 | 10 | - | 1 | 11 | 25 | published, never ranked |
| 64 | Bath | 0.36 | 144,950 | 5 | 1 | 1 | - | - | published, never ranked |
| 65 | Krakow | 0.35 | 140,824 | 4 | 3 | 1 | - | - | published, never ranked |
| 66 | Zurich | 0.35 | 140,788 | 4 | - | - | - | - | published, never ranked |
| 67 | Sofia | 0.35 | 138,710 | 4 | 1 | - | - | - | published, never ranked |
| 68 | Lyon | 0.34 | 136,951 | 9 | 3 | 1 | - | - | published, never ranked |
| 69 | Nice | 0.34 | 136,877 | 10 | 8 | 2 | - | - | published, never ranked |
| 70 | Bucharest | 0.34 | 136,836 | 4 | - | 1 | - | - | published, never ranked |
| 71 | Split | 0.33 | 132,399 | 4 | - | 1 | - | - | published, never ranked |
| 72 | Antwerp | 0.32 | 128,289 | 10 | 4 | 1 | - | - | published, never ranked |
| 73 | Ljubljana | 0.31 | 125,046 | 4 | - | 1 | - | - | published, never ranked |
| 74 | Palermo | 0.31 | 124,310 | 8 | 7 | 2 | 45 | 25 | published, never ranked |
| 75 | Dubrovnik | 0.30 | 119,586 | 4 | 1 | 1 | - | - | published, never ranked |
| 76 | York | 0.30 | 118,066 | 6 | 2 | 1 | - | - | published, never ranked |
| 77 | Malaga | 0.29 | 117,780 | 10 | 5 | 2 | - | - | published, never ranked |
| 78 | Trieste | 0.29 | 117,233 | 8 | - | 2 | 43 | 25 | published, never ranked |
| 79 | Oxford | 0.28 | 111,583 | 5 | 1 | 1 | - | - | published, never ranked |
| 80 | Rotterdam | 0.26 | 104,938 | 5 | - | 1 | - | - | published, never ranked |
| 81 | Cork | 0.25 | 101,405 | 5 | 2 | - | - | - | published, never ranked |
| 82 | Cambridge | 0.24 | 97,974 | 5 | 2 | 1 | - | - | published, never ranked |
| 83 | Zaragoza | 0.22 | 87,580 | 4 | - | 1 | - | - | published, never ranked |
| 84 | Granada | 0.22 | 86,361 | 10 | 3 | 2 | 4 | - | published, never ranked |
| 85 | Verona | 0.19 | 77,646 | 8 | 4 | 2 | 3 | - | published, never ranked |
| 86 | Fukuoka | 0.19 | 77,485 | 11 | 7 | 1 | 1 | - | published, never ranked |
| 87 | Cordoba | 0.19 | 74,675 | 7 | 2 | 2 | 3 | 25 | published, never ranked |
| 88 | Utrecht | 0.17 | 67,963 | 5 | 4 | 1 | - | - | published, never ranked |
| 89 | Padua | 0.14 | 54,592 | 9 | 4 | 1 | 12 | 25 | published, never ranked |
| 90 | Phuket | 0.14 | 5,487 | - | - | - | - | - | predicted (thin competition) |
| 91 | Lucca | 0.13 | 52,271 | 6 | 3 | 1 | 27 | 25 | published, never ranked |
| 92 | Maastricht | 0.12 | 47,763 | 5 | - | - | - | - | published, never ranked |
| 93 | Sintra | 0.12 | 46,889 | 5 | 3 | 1 | 6 | - | published, never ranked |
| 94 | Nijmegen | 0.11 | 42,338 | 5 | - | 1 | - | - | published, never ranked |
| 95 | Den Bosch | 0.10 | 39,682 | 11 | - | 1 | - | - | published, never ranked |
| 96 | Breda | 0.09 | 36,579 | 4 | - | 1 | - | - | published, never ranked |
| 97 | Haarlem | 0.08 | 33,960 | 4 | - | - | - | - | published, never ranked |
| 98 | Leiden | 0.08 | 33,227 | 6 | 4 | 1 | - | - | published, never ranked |
| 99 | Arnhem | 0.08 | 31,478 | 4 | - | - | - | - | published, never ranked |
| 100 | Groningen | 0.08 | 31,401 | 5 | - | 1 | - | - | published, never ranked |

## What this replaces

All of these named a city order and are now superseded. Deleting them is the
point of this file; leaving them is how six orders happened.

- CLAUDE.md Step 0 rung 4, "the recorded wave order" (data-led, register-first).
- CLAUDE.md "TOP OF THE QUEUE, ruled 2026-08-09: Porto and Lisbon". Not
  contradicted, absorbed: they come out 1 and 2 on the measured evidence.
- CLAUDE.md "Current focus, 2026-08-06: the tourist-city rollout, London
  first", and its phase-1 list of ten.
- CLAUDE.md "The working order, re-ruled 2026-08-06", the five numbered pairs.
- .github/workflows/nightly.yml, which carries its own order in the run prompt
  ("Barcelona, Rome, Paris, Berlin, Amsterdam, New York...") and its own focus
  countries ("Spain, Japan, Portugal. Italy is next").
- data/city-list.json ranks 1-25, which are rollout-25.json's order.

Two things survive untouched because they are not orderings: the London gate
(no Woodland Trust data without written permission) and the small-city stop
insofar as it means not opening new villages, which this list enforces anyway
by scoring them near zero.

