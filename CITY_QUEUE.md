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

**The staircase, ruled by Hidde 2026-08-13, and it is the whole phase-1 plan in
four lines.** Goal of phase 1: as many people to the website as possible, which
means as many pages as high in Google as possible. Therefore:

1. **The sprint: every top-100 city to 10 trees, as fast as possible.** A page
   must exist before Google can judge it, so breadth to 10 outranks every
   deepening everywhere. `python3 scripts/city_queue.py --next` prints this
   stage first.
2. **Then deepen only what Google confirms**, up the staircase by city size:

   | size (demand proxy) | target |
   |---|---:|
   | stadje, under 100k pageviews | 10 |
   | grote stad, 100k to 300k | 20 |
   | mega stad, 300k to 700k | 30 |
   | metropool, over 700k | 50 |

   Confirmed means Search Console shows the city 10+ impressions, which the
   daily digest writes back into the queue on its own; an unconfirmed city
   stays at 10 whatever its size.

3. **The 80/20 rule governs reaching any target** (his words: "eeuwig tokens
   gebruiken tot deze max te halen is niet de strategie... als het er wat
   minder zijn maar het wordt te moeilijk om de volgende te vinden ga gewoon
   door"). A target is a ceiling and a stopping point, never a quota: the
   moment the next tree gets hard to find, the city is done for now and the
   run moves to the next one. Cadiz at 5 is finished work.

4. **The queue re-ranks itself daily.** The data digest feeds Search Console
   back into `data/city-queue.json` (a measured city's score is its clicks in
   the window; ranking without clicks scores 0.25), so a Palermo that starts
   performing climbs on its own and nothing waits for Hidde.

What the target is NOT, unchanged: never a quota, never a floor, and the bar
per tree never moves. A city above its target (Barcelona at 46) is finished,
with nothing ever removed. Padding stays forbidden. Nothing here re-opens
whether a tree may be published: only the hard rules and an unstatable location
stop that (2026-08-10).

**Superseded on the way here, kept because the mistakes instruct:** the
supply-banded 20/30/50 of 2026-08-12 (killed with "maar waarom in godsnaam 50
doel bij wenen": a register measures how EASY trees are to find, never how GOOD
they are), a flat 25 for everyone (same day), and 10-then-25-on-confirmation
(same evening, refined into the staircase above). "A city is finished at three
walks" survives only as what the PAGE leads with: readers get the best three
walks, everything else stays published, on the map, collectible, listed below.

Deep enough, per Hidde 2026-08-08, unchanged: at least one complete walk of 4
to 8 trees inside roughly 2 km, photographs on most of that walk, honest pins
(labelled honestly, NOT confirmed), season data where it is real.

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
| 1 | Prague | 6.00 | 303,350 | 17 | 13 | 3 | - | 30 | measured |
| 2 | Vienna | 5.00 | 283,090 | 22 | 13 | 4 | 377 | 20 | measured |
| 3 | Kyoto | 4.00 | 142,353 | 18 | 8 | 2 | - | 20 | measured |
| 4 | Porto | 4.00 | 120,415 | 27 | 5 | 2 | 40 | 20 | measured |
| 5 | Sintra | 4.00 | 46,889 | 5 | 3 | 1 | 6 | 10 | measured |
| 6 | Lisbon | 3.00 | 201,877 | 33 | 10 | 3 | 66 | 20 | measured |
| 7 | Nice | 3.00 | 136,877 | 10 | 8 | 2 | - | 20 | measured |
| 8 | Palermo | 3.00 | 124,310 | 8 | 7 | 2 | 45 | 20 | measured |
| 9 | New York | 2.81 | 1,124,326 | 20 | 5 | 2 | - | 10 | published, never ranked |
| 10 | Singapore | 2.42 | 967,821 | 7 | 3 | 1 | - | 10 | published, never ranked |
| 11 | Galway | 2.20 | 88,162 | - | - | - | - | 10 | predicted (thin competition) |
| 12 | Nagoya | 2.09 | 83,437 | - | - | - | - | 10 | predicted (thin competition) |
| 13 | Jaipur | 2.06 | 82,569 | - | - | - | - | 10 | predicted (thin competition) |
| 14 | Amsterdam | 2.00 | 294,030 | 20 | 7 | 2 | 4993 | 20 | measured |
| 15 | Barcelona | 2.00 | 346,477 | 46 | 12 | 7 | 183 | 30 | measured |
| 16 | Munich | 2.00 | 224,067 | 22 | 13 | 3 | - | 20 | measured |
| 17 | Rome | 2.00 | 358,876 | 24 | 9 | 2 | 32 | 30 | measured |
| 18 | London | 1.80 | 718,291 | 23 | 10 | 1 | - | 10 | published, never ranked |
| 19 | Agra | 1.77 | 70,904 | - | - | - | - | 10 | predicted (thin competition) |
| 20 | Hong Kong | 1.72 | 689,212 | 6 | 2 | - | - | 10 | published, never ranked |
| 21 | Chiang Mai | 1.66 | 66,541 | - | - | - | - | 10 | predicted (thin competition) |
| 22 | Washington DC | 1.52 | 606,731 | 14 | 1 | 2 | - | 10 | published, never ranked |
| 23 | Kobe | 1.37 | 54,798 | - | - | - | - | 10 | predicted (thin competition) |
| 24 | Paris | 1.31 | 524,268 | 25 | 9 | 3 | 128 | 10 | published, never ranked |
| 25 | Chicago | 1.21 | 485,769 | 6 | - | - | - | 10 | published, never ranked |
| 26 | Salamanca | 1.20 | 47,897 | - | - | - | - | 10 | predicted (thin competition) |
| 27 | Berlin | 1.00 | 412,181 | 18 | 11 | 1 | 114 | 30 | measured |
| 28 | Brussels | 1.00 | 176,863 | 16 | 4 | 1 | 371 | 20 | measured |
| 29 | Cadiz | 1.00 | 79,226 | 5 | 4 | 1 | - | 10 | measured |
| 30 | Dublin | 1.00 | 240,850 | 17 | 4 | 2 | 12 | 20 | measured |
| 31 | Dubrovnik | 1.00 | 119,586 | 4 | 1 | 1 | - | 20 | measured |
| 32 | Lyon | 1.00 | 136,951 | 9 | 3 | 1 | - | 20 | measured |
| 33 | Seville | 1.00 | 170,545 | 16 | 6 | 2 | - | 20 | measured |
| 34 | Tokyo | 0.99 | 394,702 | 10 | 8 | - | 7 | 10 | published, never ranked |
| 35 | Coimbra | 0.87 | 34,962 | - | - | - | - | 10 | predicted (thin competition) |
| 36 | Braga | 0.86 | 34,522 | - | - | - | - | 10 | predicted (thin competition) |
| 37 | Kamakura | 0.84 | 33,492 | - | - | - | - | 10 | predicted (thin competition) |
| 38 | Istanbul | 0.83 | 333,027 | 14 | 4 | 1 | - | 10 | published, never ranked |
| 39 | Edinburgh | 0.73 | 292,981 | 15 | 4 | 1 | - | 10 | published, never ranked |
| 40 | Denpasar | 0.69 | 27,679 | - | - | - | - | 10 | predicted (thin competition) |
| 41 | Madrid | 0.69 | 274,553 | 17 | 10 | 2 | - | 10 | published, never ranked |
| 42 | Venice | 0.67 | 267,527 | 11 | 6 | 1 | 4 | 10 | published, never ranked |
| 43 | Kanazawa | 0.64 | 25,778 | - | - | - | - | 10 | predicted (thin competition) |
| 44 | Glasgow | 0.63 | 253,705 | 4 | 2 | - | - | 10 | published, never ranked |
| 45 | The Hague | 0.59 | 236,723 | 5 | 1 | 1 | - | 10 | published, never ranked |
| 46 | Bangkok | 0.56 | 222,206 | 5 | - | 1 | - | 10 | published, never ranked |
| 47 | Copenhagen | 0.55 | 218,621 | 13 | - | 2 | - | 10 | published, never ranked |
| 48 | Milan | 0.53 | 212,705 | 18 | 9 | 2 | 25 | 10 | published, never ranked |
| 49 | Seoul | 0.52 | 206,265 | 8 | 5 | 1 | - | 10 | published, never ranked |
| 50 | Naples | 0.50 | 198,913 | 17 | 3 | 2 | 46 | 10 | published, never ranked |
| 51 | Warsaw | 0.49 | 197,929 | 5 | 3 | - | - | 10 | published, never ranked |
| 52 | Stockholm | 0.47 | 188,184 | 4 | 3 | - | - | 10 | published, never ranked |
| 53 | Florence | 0.46 | 184,099 | 22 | 7 | 3 | 27 | 10 | published, never ranked |
| 54 | Oslo | 0.45 | 181,113 | 4 | - | - | - | 10 | published, never ranked |
| 55 | Thessaloniki | 0.45 | 180,145 | 4 | - | 1 | - | 10 | published, never ranked |
| 56 | Reykjavik | 0.42 | 166,789 | 4 | - | 1 | - | 10 | published, never ranked |
| 57 | Geneva | 0.41 | 162,269 | 6 | 4 | 1 | - | 10 | published, never ranked |
| 58 | Osaka | 0.41 | 163,112 | 4 | 1 | - | - | 10 | published, never ranked |
| 59 | Valencia | 0.41 | 162,209 | 16 | 2 | 2 | 347 | 10 | published, never ranked |
| 60 | Helsinki | 0.37 | 148,908 | 8 | 1 | - | - | 10 | published, never ranked |
| 61 | Turin | 0.37 | 147,456 | 8 | 7 | 2 | 32 | 10 | published, never ranked |
| 62 | Bath | 0.36 | 144,950 | 5 | 1 | 1 | - | 10 | published, never ranked |
| 63 | Genoa | 0.36 | 145,206 | 10 | - | 1 | 11 | 10 | published, never ranked |
| 64 | Krakow | 0.35 | 140,824 | 4 | 3 | 1 | - | 10 | published, never ranked |
| 65 | Sofia | 0.35 | 138,710 | 4 | 1 | - | - | 10 | published, never ranked |
| 66 | Zurich | 0.35 | 140,788 | 4 | - | - | - | 10 | published, never ranked |
| 67 | Bucharest | 0.34 | 136,836 | 4 | - | 1 | - | 10 | published, never ranked |
| 68 | Split | 0.33 | 132,399 | 4 | - | 1 | - | 10 | published, never ranked |
| 69 | Ljubljana | 0.31 | 125,046 | 4 | - | 1 | - | 10 | published, never ranked |
| 70 | York | 0.30 | 118,066 | 6 | 2 | 1 | - | 10 | published, never ranked |
| 71 | Malaga | 0.29 | 117,780 | 10 | 5 | 2 | - | 10 | published, never ranked |
| 72 | Trieste | 0.29 | 117,233 | 8 | - | 2 | 43 | 10 | published, never ranked |
| 73 | Oxford | 0.28 | 111,583 | 5 | 1 | 1 | - | 10 | published, never ranked |
| 74 | Rotterdam | 0.26 | 104,938 | 5 | - | 1 | - | 10 | published, never ranked |
| 75 | Antwerp | 0.25 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 76 | Athens | 0.25 | 235,429 | 12 | 6 | 2 | - | 20 | measured |
| 77 | Belgrade | 0.25 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 78 | Bologna | 0.25 | 146,161 | 11 | 8 | 2 | 8 | 20 | measured |
| 79 | Boston | 0.25 | 385,902 | 10 | 1 | 1 | - | 30 | measured |
| 80 | Bristol | 0.25 | 163,983 | 5 | 1 | - | - | 20 | measured |
| 81 | Budapest | 0.25 | 283,807 | 12 | 1 | 3 | - | 20 | measured |
| 82 | Cambridge | 0.25 | 97,974 | 5 | 2 | 1 | - | 10 | measured |
| 83 | Cork | 0.25 | 101,405 | 5 | 2 | - | - | 10 | published, never ranked |
| 84 | Granada | 0.22 | 86,361 | 10 | 3 | 2 | 4 | 10 | published, never ranked |
| 85 | Zaragoza | 0.22 | 87,580 | 4 | - | 1 | - | 10 | published, never ranked |
| 86 | Cordoba | 0.19 | 74,675 | 7 | 2 | 2 | 3 | 10 | published, never ranked |
| 87 | Fukuoka | 0.19 | 77,485 | 11 | 7 | 1 | 1 | 10 | published, never ranked |
| 88 | Verona | 0.19 | 77,646 | 8 | 4 | 2 | 3 | 10 | published, never ranked |
| 89 | Utrecht | 0.17 | 67,963 | 5 | 4 | 1 | - | 10 | published, never ranked |
| 90 | Padua | 0.14 | 54,592 | 9 | 4 | 1 | 12 | 10 | published, never ranked |
| 91 | Phuket | 0.14 | 5,487 | - | - | - | - | 10 | predicted (thin competition) |
| 92 | Lucca | 0.13 | 52,271 | 6 | 3 | 1 | 27 | 10 | published, never ranked |
| 93 | Maastricht | 0.12 | 47,763 | 5 | - | - | - | 10 | published, never ranked |
| 94 | Nijmegen | 0.11 | 42,338 | 5 | - | 1 | - | 10 | published, never ranked |
| 95 | Den Bosch | 0.10 | 39,682 | 11 | - | 1 | - | 10 | published, never ranked |
| 96 | Breda | 0.09 | 36,579 | 4 | - | 1 | - | 10 | published, never ranked |
| 97 | Arnhem | 0.08 | 31,478 | 4 | - | - | - | 10 | published, never ranked |
| 98 | Groningen | 0.08 | 31,401 | 5 | - | 1 | - | 10 | published, never ranked |
| 99 | Haarlem | 0.08 | 33,960 | 4 | - | - | - | 10 | published, never ranked |
| 100 | Leiden | 0.08 | 33,227 | 6 | 4 | 1 | - | 10 | published, never ranked |

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

