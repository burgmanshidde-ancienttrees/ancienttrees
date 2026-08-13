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

**The pool is Western tourism, the order is three factors multiplied** (Hidde,
2026-08-13: "een top 250 gebaseerd op westers toerisme... potentie qua toerisme
+ bewezen google prestatie + gemak in opstellen"). Candidates enter the list for
being places Western tourists actually go; each carries measured demand (English
Wikipedia pageviews, fetched per city, never guessed). The rank multiplies score
(demand times realised yield, clicks once measured) by an ease factor of 1.0 to
2.0: half for a country whose register story is proven (Portugal, Italy, Japan,
Ireland, Spain, the Dutch municipal pattern), half for register supply already
imported near the city. The boundary that keeps ease honest, from the Vienna-50
mistake of 2026-08-12: **ease multiplies the order of work, never the target.**
A register says cheap, not good.

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
| 1 | Porto | 4.00 | 120,415 | 27 | 5 | 2 | 40 | 20 | measured |
| 2 | Vienna | 5.00 | 283,090 | 22 | 13 | 4 | 377 | 20 | measured |
| 3 | Sintra | 4.00 | 46,889 | 5 | 3 | 1 | 6 | 10 | measured |
| 4 | Prague | 6.00 | 303,350 | 17 | 13 | 3 | - | 30 | measured |
| 5 | Kyoto | 4.00 | 142,353 | 18 | 8 | 2 | - | 20 | measured |
| 6 | Lisbon | 3.00 | 201,877 | 33 | 10 | 3 | 66 | 20 | measured |
| 7 | Palermo | 3.00 | 124,310 | 8 | 7 | 2 | 45 | 20 | measured |
| 8 | Liverpool | 5.46 | 248,189 | - | - | - | - | 10 | predicted (thin competition) |
| 9 | Belfast | 4.93 | 224,315 | - | - | - | - | 10 | predicted (thin competition) |
| 10 | Cologne | 4.80 | 191,812 | - | - | - | - | 10 | predicted (thin competition) |
| 11 | Pamplona | 3.20 | 128,065 | - | - | - | - | 10 | predicted (thin competition) |
| 12 | Hamburg | 4.78 | 191,221 | - | - | - | - | 10 | predicted (thin competition) |
| 13 | Portland | 4.78 | 217,222 | - | - | - | - | 10 | predicted (thin competition) |
| 14 | San Diego | 4.73 | 214,939 | - | - | - | - | 10 | predicted (thin competition) |
| 15 | Marseille | 4.55 | 182,033 | - | - | - | - | 10 | predicted (thin competition) |
| 16 | Perth | 4.51 | 180,478 | - | - | - | - | 10 | predicted (thin competition) |
| 17 | Sarajevo | 4.51 | 205,074 | - | - | - | - | 10 | predicted (thin competition) |
| 18 | Brisbane | 4.07 | 162,602 | - | - | - | - | 10 | predicted (thin competition) |
| 19 | Nuremberg | 4.04 | 161,614 | - | - | - | - | 10 | predicted (thin competition) |
| 20 | Amsterdam | 2.00 | 294,030 | 20 | 7 | 2 | 4993 | 20 | measured |
| 21 | Barcelona | 2.00 | 346,477 | 46 | 12 | 7 | 183 | 30 | measured |
| 22 | Rome | 2.00 | 358,876 | 24 | 9 | 2 | 32 | 30 | measured |
| 23 | Bordeaux | 3.91 | 156,201 | - | - | - | - | 10 | predicted (thin competition) |
| 24 | Charleston | 3.90 | 155,987 | - | - | - | - | 10 | predicted (thin competition) |
| 25 | Strasbourg | 3.87 | 154,700 | - | - | - | - | 10 | predicted (thin competition) |
| 26 | Syracuse | 2.57 | 102,833 | - | - | - | - | 10 | predicted (thin competition) |
| 27 | Frankfurt | 3.76 | 150,379 | - | - | - | - | 10 | predicted (thin competition) |
| 28 | Adelaide | 3.48 | 139,166 | - | - | - | - | 10 | predicted (thin competition) |
| 29 | Corfu | 3.48 | 139,334 | - | - | - | - | 10 | predicted (thin competition) |
| 30 | Manchester | 3.42 | 316,438 | - | - | - | - | 10 | predicted (thin competition) |
| 31 | Jerusalem | 3.40 | 314,788 | - | - | - | - | 10 | predicted (thin competition) |
| 32 | Limerick | 2.26 | 90,379 | - | - | - | - | 10 | predicted (thin competition) |
| 33 | Sapporo | 2.22 | 88,633 | - | - | - | - | 10 | predicted (thin competition) |
| 34 | Wellington | 3.31 | 132,267 | - | - | - | - | 10 | predicted (thin competition) |
| 35 | Bratislava | 3.30 | 132,162 | - | - | - | - | 10 | predicted (thin competition) |
| 36 | Galway | 2.20 | 88,162 | - | - | - | - | 10 | predicted (thin competition) |
| 37 | Bari | 2.16 | 86,456 | - | - | - | - | 10 | predicted (thin competition) |
| 38 | Ravenna | 2.16 | 86,471 | - | - | - | - | 10 | predicted (thin competition) |
| 39 | Rhodes | 3.18 | 127,205 | - | - | - | - | 10 | predicted (thin competition) |
| 40 | Palma de Mallorca | 2.10 | 84,075 | - | - | - | - | 10 | predicted (thin competition) |
| 41 | Nagoya | 2.09 | 83,437 | - | - | - | - | 10 | predicted (thin competition) |
| 42 | Tallinn | 3.12 | 124,888 | - | - | - | - | 10 | predicted (thin competition) |
| 43 | Quebec City | 3.11 | 124,358 | - | - | - | - | 10 | predicted (thin competition) |
| 44 | Como | 2.07 | 82,645 | - | - | - | - | 10 | predicted (thin competition) |
| 45 | Wroclaw | 3.10 | 123,894 | - | - | - | - | 10 | predicted (thin competition) |
| 46 | Leipzig | 3.03 | 121,319 | - | - | - | - | 10 | predicted (thin competition) |
| 47 | Gothenburg | 3.00 | 119,991 | - | - | - | - | 10 | predicted (thin competition) |
| 48 | Munich | 2.00 | 224,067 | 22 | 13 | 3 | - | 20 | measured |
| 49 | Nice | 3.00 | 136,877 | 10 | 8 | 2 | - | 20 | measured |
| 50 | Alicante | 1.94 | 77,454 | - | - | - | - | 10 | predicted (thin competition) |
| 51 | Brighton | 2.85 | 114,108 | - | - | - | - | 10 | predicted (thin competition) |
| 52 | Dresden | 2.84 | 113,624 | - | - | - | - | 10 | predicted (thin competition) |
| 53 | Vilnius | 2.83 | 113,188 | - | - | - | - | 10 | predicted (thin competition) |
| 54 | Stuttgart | 2.82 | 112,789 | - | - | - | - | 10 | predicted (thin competition) |
| 55 | Toulouse | 2.82 | 112,721 | - | - | - | - | 10 | predicted (thin competition) |
| 56 | New York | 2.81 | 1,124,326 | 20 | 5 | 2 | - | 10 | published, never ranked |
| 57 | Kathmandu | 2.72 | 108,896 | - | - | - | - | 10 | predicted (thin competition) |
| 58 | Riga | 2.72 | 108,918 | - | - | - | - | 10 | predicted (thin competition) |
| 59 | Salzburg | 2.68 | 107,243 | - | - | - | - | 10 | predicted (thin competition) |
| 60 | Bruges | 2.67 | 106,902 | - | - | - | - | 10 | predicted (thin competition) |
| 61 | Basel | 2.65 | 105,838 | - | - | - | - | 10 | predicted (thin competition) |
| 62 | Christchurch | 2.62 | 104,874 | - | - | - | - | 10 | predicted (thin competition) |
| 63 | Malmo | 2.60 | 103,940 | - | - | - | - | 10 | predicted (thin competition) |
| 64 | Matera | 1.68 | 67,033 | - | - | - | - | 10 | predicted (thin competition) |
| 65 | Singapore | 2.42 | 967,821 | 7 | 3 | 1 | - | 10 | published, never ranked |
| 66 | Busan | 2.37 | 94,737 | - | - | - | - | 10 | predicted (thin competition) |
| 67 | Inverness | 2.30 | 92,195 | - | - | - | - | 10 | predicted (thin competition) |
| 68 | Bern | 2.27 | 90,627 | - | - | - | - | 10 | predicted (thin competition) |
| 69 | Catania | 1.46 | 58,252 | - | - | - | - | 10 | predicted (thin competition) |
| 70 | Cusco | 2.19 | 87,732 | - | - | - | - | 10 | predicted (thin competition) |
| 71 | Siena | 1.44 | 57,436 | - | - | - | - | 10 | predicted (thin competition) |
| 72 | Trento | 1.41 | 56,455 | - | - | - | - | 10 | predicted (thin competition) |
| 73 | Valletta | 2.11 | 84,342 | - | - | - | - | 10 | predicted (thin competition) |
| 74 | Faro | 1.39 | 55,645 | - | - | - | - | 10 | predicted (thin competition) |
| 75 | Bergen | 2.07 | 82,940 | - | - | - | - | 10 | predicted (thin competition) |
| 76 | Ghent | 2.07 | 82,757 | - | - | - | - | 10 | predicted (thin competition) |
| 77 | Jaipur | 2.06 | 82,569 | - | - | - | - | 10 | predicted (thin competition) |
| 78 | Kobe | 1.37 | 54,798 | - | - | - | - | 10 | predicted (thin competition) |
| 79 | Hobart | 2.04 | 81,734 | - | - | - | - | 10 | predicted (thin competition) |
| 80 | Colombo | 2.01 | 80,386 | - | - | - | - | 10 | predicted (thin competition) |
| 81 | Seville | 1.00 | 170,545 | 16 | 6 | 2 | - | 20 | measured |
| 82 | Bergamo | 1.32 | 52,933 | - | - | - | - | 10 | predicted (thin competition) |
| 83 | Paris | 1.31 | 524,268 | 25 | 9 | 3 | 128 | 10 | published, never ranked |
| 84 | Pisa | 1.30 | 52,174 | - | - | - | - | 10 | predicted (thin competition) |
| 85 | Modena | 1.29 | 51,698 | - | - | - | - | 10 | predicted (thin competition) |
| 86 | Ronda | 1.29 | 51,510 | - | - | - | - | 10 | predicted (thin competition) |
| 87 | Cagliari | 1.28 | 51,351 | - | - | - | - | 10 | predicted (thin competition) |
| 88 | Girona | 1.28 | 51,072 | - | - | - | - | 10 | predicted (thin competition) |
| 89 | Heidelberg | 1.90 | 75,837 | - | - | - | - | 10 | predicted (thin competition) |
| 90 | Lille | 1.84 | 73,435 | - | - | - | - | 10 | predicted (thin competition) |
| 91 | Oaxaca | 1.82 | 72,955 | - | - | - | - | 10 | predicted (thin competition) |
| 92 | Rouen | 1.81 | 72,334 | - | - | - | - | 10 | predicted (thin competition) |
| 93 | London | 1.80 | 718,291 | 23 | 10 | 1 | - | 10 | published, never ranked |
| 94 | Salamanca | 1.20 | 47,897 | - | - | - | - | 10 | predicted (thin competition) |
| 95 | Zadar | 1.79 | 71,549 | - | - | - | - | 10 | predicted (thin competition) |
| 96 | Agra | 1.77 | 70,904 | - | - | - | - | 10 | predicted (thin competition) |
| 97 | Antalya | 1.77 | 70,688 | - | - | - | - | 10 | predicted (thin competition) |
| 98 | Dublin | 1.00 | 240,850 | 17 | 4 | 2 | 12 | 20 | measured |
| 99 | Trier | 1.73 | 69,369 | - | - | - | - | 10 | predicted (thin competition) |
| 100 | Hong Kong | 1.72 | 689,212 | 6 | 2 | - | - | 10 | published, never ranked |
| 101 | Lausanne | 1.71 | 68,242 | - | - | - | - | 10 | predicted (thin competition) |
| 102 | Stratford-upon-Avon | 1.71 | 68,555 | - | - | - | - | 10 | predicted (thin competition) |
| 103 | Nantes | 1.69 | 67,689 | - | - | - | - | 10 | predicted (thin competition) |
| 104 | Chiang Mai | 1.66 | 66,541 | - | - | - | - | 10 | predicted (thin competition) |
| 105 | Heraklion | 1.66 | 66,359 | - | - | - | - | 10 | predicted (thin competition) |
| 106 | Lucerne | 1.66 | 66,356 | - | - | - | - | 10 | predicted (thin competition) |
| 107 | Graz | 1.64 | 65,717 | - | - | - | - | 10 | predicted (thin competition) |
| 108 | Poznan | 1.64 | 65,666 | - | - | - | - | 10 | predicted (thin competition) |
| 109 | Cartagena | 1.63 | 65,066 | - | - | - | - | 10 | predicted (thin competition) |
| 110 | Luxembourg City | 1.62 | 64,851 | - | - | - | - | 10 | predicted (thin competition) |
| 111 | Tokyo | 0.99 | 394,702 | 10 | 8 | - | 7 | 10 | published, never ranked |
| 112 | Aix-en-Provence | 1.61 | 64,524 | - | - | - | - | 10 | predicted (thin competition) |
| 113 | Montpellier | 1.61 | 64,238 | - | - | - | - | 10 | predicted (thin competition) |
| 114 | Avignon | 1.60 | 64,047 | - | - | - | - | 10 | predicted (thin competition) |
| 115 | Mostar | 1.60 | 63,907 | - | - | - | - | 10 | predicted (thin competition) |
| 116 | Brno | 1.59 | 63,714 | - | - | - | - | 10 | predicted (thin competition) |
| 117 | Perugia | 1.06 | 42,572 | - | - | - | - | 10 | predicted (thin competition) |
| 118 | Parma | 1.01 | 40,425 | - | - | - | - | 10 | predicted (thin competition) |
| 119 | Washington DC | 1.52 | 606,731 | 14 | 1 | 2 | - | 10 | published, never ranked |
| 120 | Berlin | 1.00 | 412,181 | 18 | 11 | 1 | 114 | 30 | measured |
| 121 | Brussels | 1.00 | 176,863 | 16 | 4 | 1 | 371 | 20 | measured |
| 122 | Cadiz | 1.00 | 79,226 | 5 | 4 | 1 | - | 10 | measured |
| 123 | Sorrento | 1.00 | 40,049 | - | - | - | - | 10 | predicted (thin competition) |
| 124 | Innsbruck | 1.47 | 58,742 | - | - | - | - | 10 | predicted (thin competition) |
| 125 | Annecy | 1.42 | 56,859 | - | - | - | - | 10 | predicted (thin competition) |
| 126 | Fes | 1.34 | 53,696 | - | - | - | - | 10 | predicted (thin competition) |
| 127 | Canterbury | 1.33 | 53,301 | - | - | - | - | 10 | predicted (thin competition) |
| 128 | Aarhus | 1.32 | 52,722 | - | - | - | - | 10 | predicted (thin competition) |
| 129 | Coimbra | 0.87 | 34,962 | - | - | - | - | 10 | predicted (thin competition) |
| 130 | Regensburg | 1.30 | 51,930 | - | - | - | - | 10 | predicted (thin competition) |
| 131 | Braga | 0.86 | 34,522 | - | - | - | - | 10 | predicted (thin competition) |
| 132 | Kilkenny | 0.86 | 34,550 | - | - | - | - | 10 | predicted (thin competition) |
| 133 | Lagos | 0.86 | 34,452 | - | - | - | - | 10 | predicted (thin competition) |
| 134 | Potsdam | 1.29 | 51,727 | - | - | - | - | 10 | predicted (thin competition) |
| 135 | Kamakura | 0.84 | 33,492 | - | - | - | - | 10 | predicted (thin competition) |
| 136 | Taormina | 0.83 | 33,169 | - | - | - | - | 10 | predicted (thin competition) |
| 137 | Kotor | 1.22 | 48,982 | - | - | - | - | 10 | predicted (thin competition) |
| 138 | Tarragona | 0.81 | 32,396 | - | - | - | - | 10 | predicted (thin competition) |
| 139 | Chicago | 1.21 | 485,769 | 6 | - | - | - | 10 | published, never ranked |
| 140 | Chania | 1.18 | 47,379 | - | - | - | - | 10 | predicted (thin competition) |
| 141 | Hallstatt | 1.18 | 47,271 | - | - | - | - | 10 | predicted (thin competition) |
| 142 | Segovia | 0.77 | 30,968 | - | - | - | - | 10 | predicted (thin competition) |
| 143 | Assisi | 0.76 | 30,278 | - | - | - | - | 10 | predicted (thin competition) |
| 144 | Colmar | 1.14 | 45,517 | - | - | - | - | 10 | predicted (thin competition) |
| 145 | Dijon | 1.09 | 43,526 | - | - | - | - | 10 | predicted (thin competition) |
| 146 | Merida | 1.09 | 43,735 | - | - | - | - | 10 | predicted (thin competition) |
| 147 | Stirling | 1.09 | 43,558 | - | - | - | - | 10 | predicted (thin competition) |
| 148 | Killarney | 0.72 | 28,763 | - | - | - | - | 10 | predicted (thin competition) |
| 149 | Milan | 0.53 | 212,705 | 18 | 9 | 2 | 25 | 10 | published, never ranked |
| 150 | Venice | 0.67 | 267,527 | 11 | 6 | 1 | 4 | 10 | published, never ranked |
| 151 | Ferrara | 0.69 | 27,490 | - | - | - | - | 10 | predicted (thin competition) |
| 152 | Madrid | 0.69 | 274,553 | 17 | 10 | 2 | - | 10 | published, never ranked |
| 153 | Leuven | 1.02 | 40,645 | - | - | - | - | 10 | predicted (thin competition) |
| 154 | Dubrovnik | 1.00 | 119,586 | 4 | 1 | 1 | - | 20 | measured |
| 155 | Lyon | 1.00 | 136,951 | 9 | 3 | 1 | - | 20 | measured |
| 156 | Naples | 0.50 | 198,913 | 17 | 3 | 2 | 46 | 10 | published, never ranked |
| 157 | Rothenburg ob der Tauber | 1.00 | 39,879 | - | - | - | - | 10 | predicted (thin competition) |
| 158 | Kanazawa | 0.64 | 25,778 | - | - | - | - | 10 | predicted (thin competition) |
| 159 | Florence | 0.46 | 184,099 | 22 | 7 | 3 | 27 | 10 | published, never ranked |
| 160 | Naha | 0.61 | 24,466 | - | - | - | - | 10 | predicted (thin competition) |
| 161 | George Town | 0.90 | 36,080 | - | - | - | - | 10 | predicted (thin competition) |
| 162 | The Hague | 0.59 | 236,723 | 5 | 1 | 1 | - | 10 | published, never ranked |
| 163 | Yogyakarta | 0.87 | 34,842 | - | - | - | - | 10 | predicted (thin competition) |
| 164 | Bodrum | 0.85 | 33,918 | - | - | - | - | 10 | predicted (thin competition) |
| 165 | Istanbul | 0.83 | 333,027 | 14 | 4 | 1 | - | 10 | published, never ranked |
| 166 | Valencia | 0.41 | 162,209 | 16 | 2 | 2 | 347 | 10 | published, never ranked |
| 167 | Nafplio | 0.78 | 31,193 | - | - | - | - | 10 | predicted (thin competition) |
| 168 | Gyeongju | 0.76 | 30,260 | - | - | - | - | 10 | predicted (thin competition) |
| 169 | Windsor | 0.76 | 30,452 | - | - | - | - | 10 | predicted (thin competition) |
| 170 | Turin | 0.37 | 147,456 | 8 | 7 | 2 | 32 | 10 | published, never ranked |
| 171 | Edinburgh | 0.73 | 292,981 | 15 | 4 | 1 | - | 10 | published, never ranked |
| 172 | Bamberg | 0.72 | 28,716 | - | - | - | - | 10 | predicted (thin competition) |
| 173 | Siem Reap | 0.72 | 28,696 | - | - | - | - | 10 | predicted (thin competition) |
| 174 | Cesky Krumlov | 0.71 | 28,582 | - | - | - | - | 10 | predicted (thin competition) |
| 175 | Aveiro | 0.46 | 18,255 | - | - | - | - | 10 | predicted (thin competition) |
| 176 | Denpasar | 0.69 | 27,679 | - | - | - | - | 10 | predicted (thin competition) |
| 177 | Genoa | 0.36 | 145,206 | 10 | - | 1 | 11 | 10 | published, never ranked |
| 178 | Glasgow | 0.63 | 253,705 | 4 | 2 | - | - | 10 | published, never ranked |
| 179 | Interlaken | 0.62 | 24,936 | - | - | - | - | 10 | predicted (thin competition) |
| 180 | Luang Prabang | 0.61 | 24,534 | - | - | - | - | 10 | predicted (thin competition) |
| 181 | Osaka | 0.41 | 163,112 | 4 | 1 | - | - | 10 | published, never ranked |
| 182 | Kandy | 0.60 | 24,159 | - | - | - | - | 10 | predicted (thin competition) |
| 183 | Trieste | 0.29 | 117,233 | 8 | - | 2 | 43 | 10 | published, never ranked |
| 184 | Evora | 0.38 | 15,345 | - | - | - | - | 10 | predicted (thin competition) |
| 185 | Bangkok | 0.56 | 222,206 | 5 | - | 1 | - | 10 | published, never ranked |
| 186 | Copenhagen | 0.55 | 218,621 | 13 | - | 2 | - | 10 | published, never ranked |
| 187 | Mechelen | 0.52 | 20,707 | - | - | - | - | 10 | predicted (thin competition) |
| 188 | Seoul | 0.52 | 206,265 | 8 | 5 | 1 | - | 10 | published, never ranked |
| 189 | Warsaw | 0.49 | 197,929 | 5 | 3 | - | - | 10 | published, never ranked |
| 190 | Stockholm | 0.47 | 188,184 | 4 | 3 | - | - | 10 | published, never ranked |
| 191 | Oslo | 0.45 | 181,113 | 4 | - | - | - | 10 | published, never ranked |
| 192 | Thessaloniki | 0.45 | 180,145 | 4 | - | 1 | - | 10 | published, never ranked |
| 193 | Malaga | 0.29 | 117,780 | 10 | 5 | 2 | - | 10 | published, never ranked |
| 194 | Bologna | 0.25 | 146,161 | 11 | 8 | 2 | 8 | 20 | measured |
| 195 | Reykjavik | 0.42 | 166,789 | 4 | - | 1 | - | 10 | published, never ranked |
| 196 | Geneva | 0.41 | 162,269 | 6 | 4 | 1 | - | 10 | published, never ranked |
| 197 | Rotterdam | 0.26 | 104,938 | 5 | - | 1 | - | 10 | published, never ranked |
| 198 | Ubud | 0.39 | 15,531 | - | - | - | - | 10 | predicted (thin competition) |
| 199 | Cork | 0.25 | 101,405 | 5 | 2 | - | - | 10 | published, never ranked |
| 200 | Helsinki | 0.37 | 148,908 | 8 | 1 | - | - | 10 | published, never ranked |
| 201 | Zaragoza | 0.22 | 87,580 | 4 | - | 1 | - | 10 | published, never ranked |
| 202 | Bath | 0.36 | 144,950 | 5 | 1 | 1 | - | 10 | published, never ranked |
| 203 | Granada | 0.22 | 86,361 | 10 | 3 | 2 | 4 | 10 | published, never ranked |
| 204 | Krakow | 0.35 | 140,824 | 4 | 3 | 1 | - | 10 | published, never ranked |
| 205 | Sofia | 0.35 | 138,710 | 4 | 1 | - | - | 10 | published, never ranked |
| 206 | Zurich | 0.35 | 140,788 | 4 | - | - | - | 10 | published, never ranked |
| 207 | Bucharest | 0.34 | 136,836 | 4 | - | 1 | - | 10 | published, never ranked |
| 208 | Cordoba | 0.19 | 74,675 | 7 | 2 | 2 | 3 | 10 | published, never ranked |
| 209 | Bled | 0.33 | 13,126 | - | - | - | - | 10 | predicted (thin competition) |
| 210 | Split | 0.33 | 132,399 | 4 | - | 1 | - | 10 | published, never ranked |
| 211 | Ljubljana | 0.31 | 125,046 | 4 | - | 1 | - | 10 | published, never ranked |
| 212 | Fukuoka | 0.19 | 77,485 | 11 | 7 | 1 | 1 | 10 | published, never ranked |
| 213 | Verona | 0.19 | 77,646 | 8 | 4 | 2 | 3 | 10 | published, never ranked |
| 214 | York | 0.30 | 118,066 | 6 | 2 | 1 | - | 10 | published, never ranked |
| 215 | Oxford | 0.28 | 111,583 | 5 | 1 | 1 | - | 10 | published, never ranked |
| 216 | Lucca | 0.13 | 52,271 | 6 | 3 | 1 | 27 | 10 | published, never ranked |
| 217 | Utrecht | 0.17 | 67,963 | 5 | 4 | 1 | - | 10 | published, never ranked |
| 218 | Antwerp | 0.25 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 219 | Athens | 0.25 | 235,429 | 12 | 6 | 2 | - | 20 | measured |
| 220 | Belgrade | 0.25 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 221 | Boston | 0.25 | 385,902 | 10 | 1 | 1 | - | 30 | measured |
| 222 | Bristol | 0.25 | 163,983 | 5 | 1 | - | - | 20 | measured |
| 223 | Budapest | 0.25 | 283,807 | 12 | 1 | 3 | - | 20 | measured |
| 224 | Cambridge | 0.25 | 97,974 | 5 | 2 | 1 | - | 10 | measured |
| 225 | Padua | 0.14 | 54,592 | 9 | 4 | 1 | 12 | 10 | published, never ranked |
| 226 | Maastricht | 0.12 | 47,763 | 5 | - | - | - | 10 | published, never ranked |
| 227 | Nijmegen | 0.11 | 42,338 | 5 | - | 1 | - | 10 | published, never ranked |
| 228 | Freiburg | 0.16 | 6,384 | - | - | - | - | 10 | predicted (thin competition) |
| 229 | Den Bosch | 0.10 | 39,682 | 11 | - | 1 | - | 10 | published, never ranked |
| 230 | Austin | 0.14 | 5,525 | - | - | - | - | 10 | predicted (thin competition) |
| 231 | Breda | 0.09 | 36,579 | 4 | - | 1 | - | 10 | published, never ranked |
| 232 | Phuket | 0.14 | 5,487 | - | - | - | - | 10 | predicted (thin competition) |
| 233 | Versailles | 0.13 | 5,045 | - | - | - | - | 10 | predicted (thin competition) |
| 234 | Arnhem | 0.08 | 31,478 | 4 | - | - | - | 10 | published, never ranked |
| 235 | Groningen | 0.08 | 31,401 | 5 | - | 1 | - | 10 | published, never ranked |
| 236 | Haarlem | 0.08 | 33,960 | 4 | - | - | - | 10 | published, never ranked |
| 237 | Leiden | 0.08 | 33,227 | 6 | 4 | 1 | - | 10 | published, never ranked |
| 238 | Savannah | 0.11 | 4,331 | - | - | - | - | 10 | predicted (thin competition) |
| 239 | Izmir | 0.04 | 1,525 | - | - | - | - | 10 | predicted (thin competition) |
| 240 | Nikko | 0.02 | 649 | - | - | - | - | 10 | predicted (thin competition) |
| 241 | Queenstown | 0.03 | 1,005 | - | - | - | - | 10 | predicted (thin competition) |
| 242 | Hoi An | 0.01 | 518 | - | - | - | - | 10 | predicted (thin competition) |
| 243 | Obidos | 0.01 | 249 | - | - | - | - | 10 | predicted (thin competition) |
| 244 | Takayama | 0.01 | 408 | - | - | - | - | 10 | predicted (thin competition) |

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

