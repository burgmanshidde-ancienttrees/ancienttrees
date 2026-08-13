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

1. **The sprint: every ranked city to 10 trees, as fast as possible, and
   nothing deepens while it runs** (Hidde, 2026-08-13: "ik zou ook voorrang
   willen geven in deze top 250 tot de 10 brengen en niet verdiepen"). A page
   must exist before Google can judge it, so breadth to 10 outranks every
   deepening everywhere: stage 2 work is dispatched only when stage 1 has
   nothing left that can be moved cheaply. `python3 scripts/city_queue.py
   --next` prints the sprint first and says so.
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
| 2 | Vienna | 5.00 | 283,090 | 25 | 13 | 5 | 375 | 20 | measured |
| 3 | Los Angeles | 7.19 | 665,559 | - | - | - | - | 10 | predicted (thin competition) |
| 4 | Portland | 4.78 | 217,222 | 10 | - | 1 | 262 | 10 | predicted (thin competition) |
| 5 | Funchal | 4.36 | 174,351 | - | - | - | - | 10 | predicted (thin competition) |
| 6 | Sintra | 4.00 | 46,889 | 5 | 3 | 1 | 6 | 10 | measured |
| 7 | Rio de Janeiro | 6.15 | 279,431 | - | - | - | - | 10 | predicted (thin competition) |
| 8 | Miami | 6.13 | 278,558 | - | - | - | - | 10 | predicted (thin competition) |
| 9 | Mexico City | 6.12 | 566,583 | - | - | - | - | 10 | predicted (thin competition) |
| 10 | Prague | 6.00 | 303,350 | 17 | 13 | 3 | - | 30 | measured |
| 11 | Shanghai | 6.10 | 277,140 | - | - | - | - | 10 | predicted (thin competition) |
| 12 | Kyoto | 4.00 | 142,353 | 18 | 8 | 2 | - | 20 | measured |
| 13 | Nuremberg | 4.04 | 161,614 | - | - | - | 37 | 10 | predicted (thin competition) |
| 14 | Lisbon | 3.00 | 201,877 | 33 | 10 | 3 | 66 | 20 | measured |
| 15 | Palermo | 3.00 | 124,310 | 8 | 7 | 2 | 45 | 20 | measured |
| 16 | Beijing | 5.93 | 269,737 | - | - | - | - | 10 | predicted (thin competition) |
| 17 | Jakarta | 5.91 | 268,596 | - | - | - | - | 10 | predicted (thin competition) |
| 18 | Melbourne | 5.89 | 267,898 | - | - | - | - | 10 | predicted (thin competition) |
| 19 | Bordeaux | 3.91 | 156,201 | - | - | - | 182 | 10 | predicted (thin competition) |
| 20 | Strasbourg | 3.87 | 154,700 | - | - | - | 66 | 10 | predicted (thin competition) |
| 21 | New Orleans | 5.64 | 256,232 | - | - | - | - | 10 | predicted (thin competition) |
| 22 | Liverpool | 5.46 | 248,189 | - | - | - | - | 10 | predicted (thin competition) |
| 23 | Bilbao | 3.33 | 133,133 | - | - | - | - | 10 | predicted (thin competition) |
| 24 | Austin | 4.99 | 226,631 | - | - | - | - | 10 | predicted (thin competition) |
| 25 | Cape Town | 4.98 | 199,169 | - | - | - | - | 10 | predicted (thin competition) |
| 26 | Delhi | 4.95 | 225,133 | - | - | - | - | 10 | predicted (thin competition) |
| 27 | Belfast | 4.93 | 224,315 | - | - | - | - | 10 | predicted (thin competition) |
| 28 | Hiroshima | 3.24 | 129,791 | - | - | - | - | 10 | predicted (thin competition) |
| 29 | Pamplona | 3.20 | 128,065 | - | - | - | 1 | 10 | predicted (thin competition) |
| 30 | Ho Chi Minh City | 4.85 | 193,859 | - | - | - | - | 10 | predicted (thin competition) |
| 31 | Cologne | 4.80 | 191,812 | - | - | - | - | 10 | predicted (thin competition) |
| 32 | Kuala Lumpur | 4.79 | 191,800 | - | - | - | - | 10 | predicted (thin competition) |
| 33 | Hamburg | 4.78 | 191,221 | - | - | - | - | 10 | predicted (thin competition) |
| 34 | San Diego | 4.73 | 214,939 | - | - | - | - | 10 | predicted (thin competition) |
| 35 | Marseille | 4.55 | 182,033 | - | - | - | - | 10 | predicted (thin competition) |
| 36 | Perth | 4.51 | 180,478 | - | - | - | - | 10 | predicted (thin competition) |
| 37 | Sarajevo | 4.51 | 205,074 | - | - | - | - | 10 | predicted (thin competition) |
| 38 | Tel Aviv | 4.45 | 177,885 | - | - | - | - | 10 | predicted (thin competition) |
| 39 | Toronto | 4.44 | 411,011 | - | - | - | - | 10 | predicted (thin competition) |
| 40 | Cairo | 4.40 | 176,137 | - | - | - | - | 10 | predicted (thin competition) |
| 41 | Philadelphia | 4.38 | 405,294 | - | - | - | - | 10 | predicted (thin competition) |
| 42 | Seattle | 4.31 | 398,724 | - | - | - | - | 10 | predicted (thin competition) |
| 43 | Toulouse | 2.82 | 112,721 | - | - | - | 33 | 10 | predicted (thin competition) |
| 44 | Manila | 4.17 | 166,894 | - | - | - | - | 10 | predicted (thin competition) |
| 45 | Como | 2.07 | 82,645 | 7 | - | 1 | 23 | 10 | predicted (thin competition) |
| 46 | Brisbane | 4.07 | 162,602 | - | - | - | - | 10 | predicted (thin competition) |
| 47 | Amsterdam | 2.00 | 294,030 | 20 | 7 | 2 | 5239 | 20 | measured |
| 48 | Barcelona | 2.00 | 346,477 | 46 | 12 | 7 | 183 | 30 | measured |
| 49 | Rome | 2.00 | 358,876 | 25 | 9 | 2 | 32 | 30 | measured |
| 50 | Charleston | 3.90 | 155,987 | - | - | - | - | 10 | predicted (thin competition) |
| 51 | San Francisco | 3.90 | 361,111 | - | - | - | - | 10 | predicted (thin competition) |
| 52 | Alicante | 1.94 | 77,454 | - | - | - | 44 | 10 | predicted (thin competition) |
| 53 | Syracuse | 2.57 | 102,833 | - | - | - | - | 10 | predicted (thin competition) |
| 54 | Auckland | 3.80 | 152,056 | - | - | - | - | 10 | predicted (thin competition) |
| 55 | Vancouver | 3.80 | 351,552 | - | - | - | - | 10 | predicted (thin competition) |
| 56 | Frankfurt | 3.76 | 150,379 | - | - | - | - | 10 | predicted (thin competition) |
| 57 | Singapore | 2.42 | 967,821 | 7 | 3 | 1 | 165 | 10 | published, never ranked |
| 58 | Dubai | 3.61 | 334,167 | - | - | - | - | 10 | predicted (thin competition) |
| 59 | Buenos Aires | 3.60 | 333,331 | - | - | - | - | 10 | predicted (thin competition) |
| 60 | Taipei | 3.58 | 143,193 | - | - | - | - | 10 | predicted (thin competition) |
| 61 | Santiago de Compostela | 2.34 | 93,477 | - | - | - | - | 10 | predicted (thin competition) |
| 62 | Palma de Mallorca | 2.10 | 84,075 | - | - | - | 8 | 10 | predicted (thin competition) |
| 63 | Adelaide | 3.48 | 139,166 | - | - | - | - | 10 | predicted (thin competition) |
| 64 | Corfu | 3.48 | 139,334 | - | - | - | - | 10 | predicted (thin competition) |
| 65 | Mumbai | 3.45 | 319,236 | - | - | - | - | 10 | predicted (thin competition) |
| 66 | Manchester | 3.42 | 316,438 | - | - | - | - | 10 | predicted (thin competition) |
| 67 | Bari | 2.16 | 86,456 | - | - | - | 4 | 10 | predicted (thin competition) |
| 68 | Montreal | 3.41 | 315,322 | - | - | - | - | 10 | predicted (thin competition) |
| 69 | Jerusalem | 3.40 | 314,788 | - | - | - | - | 10 | predicted (thin competition) |
| 70 | Limerick | 2.26 | 90,379 | - | - | - | - | 10 | predicted (thin competition) |
| 71 | Sapporo | 2.22 | 88,633 | - | - | - | - | 10 | predicted (thin competition) |
| 72 | Lima | 3.32 | 132,792 | - | - | - | - | 10 | predicted (thin competition) |
| 73 | Wellington | 3.31 | 132,267 | - | - | - | - | 10 | predicted (thin competition) |
| 74 | Bratislava | 3.30 | 132,162 | - | - | - | - | 10 | predicted (thin competition) |
| 75 | Galway | 2.20 | 88,162 | - | - | - | - | 10 | predicted (thin competition) |
| 76 | Sydney | 3.30 | 305,304 | - | - | - | - | 10 | predicted (thin competition) |
| 77 | Ravenna | 2.16 | 86,471 | - | - | - | 1 | 10 | predicted (thin competition) |
| 78 | Savannah | 3.20 | 128,162 | - | - | - | - | 10 | predicted (thin competition) |
| 79 | Nagoya | 2.09 | 83,437 | - | - | - | 1 | 10 | predicted (thin competition) |
| 80 | Rhodes | 3.18 | 127,205 | - | - | - | - | 10 | predicted (thin competition) |
| 81 | Tallinn | 3.12 | 124,888 | - | - | - | - | 10 | predicted (thin competition) |
| 82 | Quebec City | 3.11 | 124,358 | - | - | - | - | 10 | predicted (thin competition) |
| 83 | Wroclaw | 3.10 | 123,894 | - | - | - | - | 10 | predicted (thin competition) |
| 84 | Zagreb | 3.07 | 122,890 | - | - | - | - | 10 | predicted (thin competition) |
| 85 | Hobart | 2.04 | 81,734 | - | - | - | 455 | 10 | predicted (thin competition) |
| 86 | Leipzig | 3.03 | 121,319 | - | - | - | - | 10 | predicted (thin competition) |
| 87 | Gothenburg | 3.00 | 119,991 | - | - | - | - | 10 | predicted (thin competition) |
| 88 | Munich | 2.00 | 224,067 | 22 | 13 | 3 | 74 | 20 | measured |
| 89 | Nice | 3.00 | 136,877 | 10 | 8 | 2 | - | 20 | measured |
| 90 | Hanoi | 2.93 | 117,396 | - | - | - | - | 10 | predicted (thin competition) |
| 91 | Brighton | 2.85 | 114,108 | - | - | - | - | 10 | predicted (thin competition) |
| 92 | Dresden | 2.84 | 113,624 | - | - | - | - | 10 | predicted (thin competition) |
| 93 | Vilnius | 2.83 | 113,188 | - | - | - | - | 10 | predicted (thin competition) |
| 94 | Stuttgart | 2.82 | 112,789 | - | - | - | - | 10 | predicted (thin competition) |
| 95 | New York | 2.81 | 1,124,326 | 20 | 5 | 2 | - | 10 | published, never ranked |
| 96 | Santiago | 2.79 | 111,647 | - | - | - | - | 10 | predicted (thin competition) |
| 97 | Trento | 1.41 | 56,455 | 7 | - | 1 | 19 | 10 | predicted (thin competition) |
| 98 | Marrakech | 2.78 | 111,098 | - | - | - | - | 10 | predicted (thin competition) |
| 99 | Kathmandu | 2.72 | 108,896 | - | - | - | - | 10 | predicted (thin competition) |
| 100 | Riga | 2.72 | 108,918 | - | - | - | - | 10 | predicted (thin competition) |
| 101 | Salzburg | 2.68 | 107,243 | - | - | - | - | 10 | predicted (thin competition) |
| 102 | Bruges | 2.67 | 106,902 | - | - | - | - | 10 | predicted (thin competition) |
| 103 | Basel | 2.65 | 105,838 | - | - | - | - | 10 | predicted (thin competition) |
| 104 | Christchurch | 2.62 | 104,874 | - | - | - | - | 10 | predicted (thin competition) |
| 105 | Malmo | 2.60 | 103,940 | - | - | - | - | 10 | predicted (thin competition) |
| 106 | Hong Kong | 1.72 | 689,212 | 6 | 2 | - | 505 | 10 | published, never ranked |
| 107 | Matera | 1.68 | 67,033 | - | - | - | - | 10 | predicted (thin competition) |
| 108 | Bergamo | 1.32 | 52,933 | 7 | - | 1 | 17 | 10 | predicted (thin competition) |
| 109 | Busan | 2.37 | 94,737 | - | - | - | - | 10 | predicted (thin competition) |
| 110 | Catania | 1.46 | 58,252 | - | - | - | 5 | 10 | predicted (thin competition) |
| 111 | Freiburg | 2.32 | 92,752 | - | - | - | - | 10 | predicted (thin competition) |
| 112 | Inverness | 2.30 | 92,195 | - | - | - | - | 10 | predicted (thin competition) |
| 113 | Bern | 2.27 | 90,627 | - | - | - | - | 10 | predicted (thin competition) |
| 114 | Cusco | 2.19 | 87,732 | - | - | - | - | 10 | predicted (thin competition) |
| 115 | Siena | 1.44 | 57,436 | - | - | - | - | 10 | predicted (thin competition) |
| 116 | Cagliari | 1.28 | 51,351 | - | - | - | 9 | 10 | predicted (thin competition) |
| 117 | Perugia | 1.06 | 42,572 | 8 | - | 2 | 19 | 10 | predicted (thin competition) |
| 118 | Valletta | 2.11 | 84,342 | - | - | - | - | 10 | predicted (thin competition) |
| 119 | Faro | 1.39 | 55,645 | - | - | - | - | 10 | predicted (thin competition) |
| 120 | Bergen | 2.07 | 82,940 | - | - | - | - | 10 | predicted (thin competition) |
| 121 | Ghent | 2.07 | 82,757 | - | - | - | - | 10 | predicted (thin competition) |
| 122 | Jaipur | 2.06 | 82,569 | - | - | - | - | 10 | predicted (thin competition) |
| 123 | Kobe | 1.37 | 54,798 | - | - | - | - | 10 | predicted (thin competition) |
| 124 | Colombo | 2.01 | 80,386 | - | - | - | - | 10 | predicted (thin competition) |
| 125 | Modena | 1.29 | 51,698 | - | - | - | 3 | 10 | predicted (thin competition) |
| 126 | Seville | 1.00 | 170,545 | 16 | 6 | 2 | - | 20 | measured |
| 127 | Paris | 1.31 | 524,268 | 25 | 9 | 3 | 129 | 10 | published, never ranked |
| 128 | Ronda | 1.29 | 51,510 | - | - | - | 1 | 10 | predicted (thin competition) |
| 129 | Pisa | 1.30 | 52,174 | - | - | - | - | 10 | predicted (thin competition) |
| 130 | Girona | 1.28 | 51,072 | - | - | - | - | 10 | predicted (thin competition) |
| 131 | Heidelberg | 1.90 | 75,837 | - | - | - | - | 10 | predicted (thin competition) |
| 132 | Rouen | 1.81 | 72,334 | - | - | - | 1 | 10 | predicted (thin competition) |
| 133 | Lille | 1.84 | 73,435 | - | - | - | - | 10 | predicted (thin competition) |
| 134 | Oaxaca | 1.82 | 72,955 | - | - | - | - | 10 | predicted (thin competition) |
| 135 | Salamanca | 1.20 | 47,897 | - | - | - | 1 | 10 | predicted (thin competition) |
| 136 | London | 1.80 | 718,291 | 23 | 10 | 1 | - | 10 | published, never ranked |
| 137 | Zadar | 1.79 | 71,549 | - | - | - | - | 10 | predicted (thin competition) |
| 138 | Agra | 1.77 | 70,904 | - | - | - | - | 10 | predicted (thin competition) |
| 139 | Antalya | 1.77 | 70,688 | - | - | - | - | 10 | predicted (thin competition) |
| 140 | Izmir | 1.75 | 69,826 | - | - | - | - | 10 | predicted (thin competition) |
| 141 | Dublin | 1.00 | 240,850 | 17 | 4 | 2 | 12 | 20 | measured |
| 142 | Trier | 1.73 | 69,369 | - | - | - | - | 10 | predicted (thin competition) |
| 143 | Lausanne | 1.71 | 68,242 | - | - | - | - | 10 | predicted (thin competition) |
| 144 | Stratford-upon-Avon | 1.71 | 68,555 | - | - | - | - | 10 | predicted (thin competition) |
| 145 | Nantes | 1.69 | 67,689 | - | - | - | - | 10 | predicted (thin competition) |
| 146 | Chiang Mai | 1.66 | 66,541 | - | - | - | - | 10 | predicted (thin competition) |
| 147 | Heraklion | 1.66 | 66,359 | - | - | - | - | 10 | predicted (thin competition) |
| 148 | Lucerne | 1.66 | 66,356 | - | - | - | - | 10 | predicted (thin competition) |
| 149 | Parma | 1.01 | 40,425 | - | - | - | 7 | 10 | predicted (thin competition) |
| 150 | Graz | 1.64 | 65,717 | - | - | - | - | 10 | predicted (thin competition) |
| 151 | Poznan | 1.64 | 65,666 | - | - | - | - | 10 | predicted (thin competition) |
| 152 | Cartagena | 1.63 | 65,066 | - | - | - | - | 10 | predicted (thin competition) |
| 153 | Luxembourg City | 1.62 | 64,851 | - | - | - | - | 10 | predicted (thin competition) |
| 154 | Tokyo | 0.99 | 394,702 | 10 | 8 | - | 7 | 10 | published, never ranked |
| 155 | Aix-en-Provence | 1.61 | 64,524 | - | - | - | - | 10 | predicted (thin competition) |
| 156 | Montpellier | 1.61 | 64,238 | - | - | - | - | 10 | predicted (thin competition) |
| 157 | Avignon | 1.60 | 64,047 | - | - | - | - | 10 | predicted (thin competition) |
| 158 | Mostar | 1.60 | 63,907 | - | - | - | - | 10 | predicted (thin competition) |
| 159 | Potsdam | 1.29 | 51,727 | - | - | - | 12 | 10 | predicted (thin competition) |
| 160 | Brno | 1.59 | 63,714 | - | - | - | - | 10 | predicted (thin competition) |
| 161 | Washington DC | 1.52 | 606,731 | 14 | 1 | 2 | - | 10 | published, never ranked |
| 162 | Berlin | 1.00 | 412,181 | 18 | 11 | 1 | 195 | 30 | measured |
| 163 | Brussels | 1.00 | 176,863 | 16 | 4 | 1 | 436 | 20 | measured |
| 164 | Cadiz | 1.00 | 79,226 | 5 | 4 | 1 | - | 10 | measured |
| 165 | Sorrento | 1.00 | 40,049 | - | - | - | - | 10 | predicted (thin competition) |
| 166 | Innsbruck | 1.47 | 58,742 | - | - | - | - | 10 | predicted (thin competition) |
| 167 | Braga | 0.86 | 34,522 | - | - | - | 8 | 10 | predicted (thin competition) |
| 168 | Annecy | 1.42 | 56,859 | - | - | - | - | 10 | predicted (thin competition) |
| 169 | Coimbra | 0.87 | 34,962 | - | - | - | 5 | 10 | predicted (thin competition) |
| 170 | Regensburg | 1.30 | 51,930 | - | - | - | 2 | 10 | predicted (thin competition) |
| 171 | Fes | 1.34 | 53,696 | - | - | - | - | 10 | predicted (thin competition) |
| 172 | Canterbury | 1.33 | 53,301 | - | - | - | - | 10 | predicted (thin competition) |
| 173 | Taormina | 0.83 | 33,169 | - | - | - | 5 | 10 | predicted (thin competition) |
| 174 | Aarhus | 1.32 | 52,722 | - | - | - | - | 10 | predicted (thin competition) |
| 175 | Guimaraes | 0.66 | 26,203 | 4 | 1 | 1 | 19 | 10 | predicted (thin competition) |
| 176 | Kilkenny | 0.86 | 34,550 | - | - | - | - | 10 | predicted (thin competition) |
| 177 | Lagos | 0.86 | 34,452 | - | - | - | - | 10 | predicted (thin competition) |
| 178 | Kamakura | 0.84 | 33,492 | - | - | - | - | 10 | predicted (thin competition) |
| 179 | Kotor | 1.22 | 48,982 | - | - | - | - | 10 | predicted (thin competition) |
| 180 | Tarragona | 0.81 | 32,396 | - | - | - | - | 10 | predicted (thin competition) |
| 181 | Chicago | 1.21 | 485,769 | 6 | - | - | - | 10 | published, never ranked |
| 182 | Chania | 1.18 | 47,379 | - | - | - | - | 10 | predicted (thin competition) |
| 183 | Hallstatt | 1.18 | 47,271 | - | - | - | - | 10 | predicted (thin competition) |
| 184 | Delft | 0.78 | 31,293 | 4 | - | 1 | - | 10 | predicted (thin competition) |
| 185 | Segovia | 0.77 | 30,968 | - | - | - | 1 | 10 | predicted (thin competition) |
| 186 | Rothenburg ob der Tauber | 1.00 | 39,879 | - | - | - | 8 | 10 | predicted (thin competition) |
| 187 | Assisi | 0.76 | 30,278 | - | - | - | - | 10 | predicted (thin competition) |
| 188 | Colmar | 1.14 | 45,517 | - | - | - | - | 10 | predicted (thin competition) |
| 189 | Ferrara | 0.69 | 27,490 | - | - | - | 7 | 10 | predicted (thin competition) |
| 190 | Dijon | 1.09 | 43,526 | - | - | - | - | 10 | predicted (thin competition) |
| 191 | Merida | 1.09 | 43,735 | - | - | - | - | 10 | predicted (thin competition) |
| 192 | Stirling | 1.09 | 43,558 | - | - | - | - | 10 | predicted (thin competition) |
| 193 | Killarney | 0.72 | 28,763 | - | - | - | - | 10 | predicted (thin competition) |
| 194 | Milan | 0.53 | 212,705 | 18 | 9 | 2 | 25 | 10 | published, never ranked |
| 195 | Venice | 0.67 | 267,527 | 11 | 6 | 1 | 4 | 10 | published, never ranked |
| 196 | Madrid | 0.69 | 274,553 | 17 | 10 | 2 | - | 10 | published, never ranked |
| 197 | Leuven | 1.02 | 40,645 | - | - | - | - | 10 | predicted (thin competition) |
| 198 | Dubrovnik | 1.00 | 119,586 | 4 | 1 | 1 | - | 20 | measured |
| 199 | Lyon | 1.00 | 136,951 | 9 | 3 | 1 | - | 20 | measured |
| 200 | Naples | 0.50 | 198,913 | 17 | 3 | 2 | 46 | 10 | published, never ranked |
| 201 | Setubal | 0.56 | 22,582 | 10 | 1 | 2 | 13 | 10 | predicted (thin competition) |
| 202 | Kanazawa | 0.64 | 25,778 | - | - | - | 2 | 10 | predicted (thin competition) |
| 203 | Naha | 0.61 | 24,466 | - | - | - | 1 | 10 | predicted (thin competition) |
| 204 | Florence | 0.46 | 184,099 | 22 | 7 | 3 | 27 | 10 | published, never ranked |
| 205 | Queenstown | 0.92 | 36,672 | - | - | - | - | 10 | predicted (thin competition) |
| 206 | George Town | 0.90 | 36,080 | - | - | - | - | 10 | predicted (thin competition) |
| 207 | The Hague | 0.59 | 236,723 | 5 | 1 | 1 | - | 10 | published, never ranked |
| 208 | Yogyakarta | 0.87 | 34,842 | - | - | - | - | 10 | predicted (thin competition) |
| 209 | Bamberg | 0.72 | 28,716 | - | - | - | 10 | 10 | predicted (thin competition) |
| 210 | Bodrum | 0.85 | 33,918 | - | - | - | - | 10 | predicted (thin competition) |
| 211 | Istanbul | 0.83 | 333,027 | 14 | 4 | 1 | - | 10 | published, never ranked |
| 212 | Valencia | 0.41 | 162,209 | 16 | 2 | 2 | 350 | 10 | published, never ranked |
| 213 | Nafplio | 0.78 | 31,193 | - | - | - | - | 10 | predicted (thin competition) |
| 214 | Gyeongju | 0.76 | 30,260 | - | - | - | - | 10 | predicted (thin competition) |
| 215 | Windsor | 0.76 | 30,452 | - | - | - | - | 10 | predicted (thin competition) |
| 216 | Caserta | 0.37 | 14,783 | 7 | - | 1 | 51 | 10 | predicted (thin competition) |
| 217 | Turin | 0.37 | 147,456 | 10 | 7 | 2 | 30 | 10 | published, never ranked |
| 218 | Edinburgh | 0.73 | 292,981 | 15 | 4 | 1 | - | 10 | published, never ranked |
| 219 | Siem Reap | 0.72 | 28,696 | - | - | - | - | 10 | predicted (thin competition) |
| 220 | Versailles | 0.72 | 28,926 | - | - | - | - | 10 | predicted (thin competition) |
| 221 | Cesky Krumlov | 0.71 | 28,582 | - | - | - | - | 10 | predicted (thin competition) |
| 222 | Aveiro | 0.46 | 18,255 | - | - | - | - | 10 | predicted (thin competition) |
| 223 | Denpasar | 0.69 | 27,679 | - | - | - | - | 10 | predicted (thin competition) |
| 224 | Genoa | 0.36 | 145,206 | 10 | - | 1 | 11 | 10 | published, never ranked |
| 225 | Glasgow | 0.63 | 253,705 | 4 | 2 | - | - | 10 | published, never ranked |
| 226 | Interlaken | 0.62 | 24,936 | - | - | - | - | 10 | predicted (thin competition) |
| 227 | Luang Prabang | 0.61 | 24,534 | - | - | - | - | 10 | predicted (thin competition) |
| 228 | Osaka | 0.41 | 163,112 | 4 | 1 | - | - | 10 | published, never ranked |
| 229 | Kandy | 0.60 | 24,159 | - | - | - | - | 10 | predicted (thin competition) |
| 230 | Obidos | 0.39 | 15,685 | - | - | - | - | 10 | predicted (thin competition) |
| 231 | Trieste | 0.29 | 117,233 | 8 | - | 2 | 43 | 10 | published, never ranked |
| 232 | Evora | 0.38 | 15,345 | - | - | - | - | 10 | predicted (thin competition) |
| 233 | Bangkok | 0.56 | 222,206 | 5 | - | 1 | - | 10 | published, never ranked |
| 234 | Copenhagen | 0.55 | 218,621 | 13 | - | 2 | - | 10 | published, never ranked |
| 235 | Mechelen | 0.52 | 20,707 | - | - | - | - | 10 | predicted (thin competition) |
| 236 | Seoul | 0.52 | 206,265 | 8 | 5 | 1 | - | 10 | published, never ranked |
| 237 | Warsaw | 0.49 | 197,929 | 5 | 3 | - | - | 10 | published, never ranked |
| 238 | Stockholm | 0.47 | 188,184 | 4 | 3 | - | - | 10 | published, never ranked |
| 239 | Takayama | 0.31 | 12,456 | - | - | - | - | 10 | predicted (thin competition) |
| 240 | Oslo | 0.45 | 181,113 | 4 | - | - | - | 10 | published, never ranked |
| 241 | Thessaloniki | 0.45 | 180,145 | 4 | - | 1 | - | 10 | published, never ranked |
| 242 | Malaga | 0.29 | 117,780 | 10 | 5 | 2 | - | 10 | published, never ranked |
| 243 | Bologna | 0.25 | 146,161 | 12 | 8 | 2 | 9 | 20 | measured |
| 244 | Reykjavik | 0.42 | 166,789 | 4 | - | 1 | - | 10 | published, never ranked |
| 245 | Geneva | 0.41 | 162,269 | 6 | 4 | 1 | - | 10 | published, never ranked |
| 246 | Rotterdam | 0.26 | 104,938 | 5 | - | 1 | - | 10 | published, never ranked |
| 247 | Ubud | 0.39 | 15,531 | - | - | - | - | 10 | predicted (thin competition) |
| 248 | Cork | 0.25 | 101,405 | 5 | 2 | - | - | 10 | published, never ranked |
| 249 | Helsinki | 0.37 | 148,908 | 8 | 1 | - | - | 10 | published, never ranked |
| 250 | Zaragoza | 0.22 | 87,580 | 7 | - | 1 | - | 10 | published, never ranked |
| 251 | Bath | 0.36 | 144,950 | 5 | 1 | 1 | - | 10 | published, never ranked |
| 252 | Granada | 0.22 | 86,361 | 10 | 3 | 2 | 4 | 10 | published, never ranked |
| 253 | Krakow | 0.35 | 140,824 | 4 | 3 | 1 | - | 10 | published, never ranked |
| 254 | Sofia | 0.35 | 138,710 | 4 | 1 | - | - | 10 | published, never ranked |
| 255 | Zurich | 0.35 | 140,788 | 4 | - | - | - | 10 | published, never ranked |
| 256 | Bucharest | 0.34 | 136,836 | 4 | - | 1 | - | 10 | published, never ranked |
| 257 | Cordoba | 0.19 | 74,675 | 10 | 2 | 2 | 3 | 10 | published, never ranked |
| 258 | Bled | 0.33 | 13,126 | - | - | - | - | 10 | predicted (thin competition) |
| 259 | Split | 0.33 | 132,399 | 4 | - | 1 | - | 10 | published, never ranked |
| 260 | Ljubljana | 0.31 | 125,046 | 4 | - | 1 | - | 10 | published, never ranked |
| 261 | Fukuoka | 0.19 | 77,485 | 11 | 7 | 1 | 1 | 10 | published, never ranked |
| 262 | Nara | 0.19 | 7,556 | 9 | 4 | 2 | - | 10 | predicted (thin competition) |
| 263 | Verona | 0.19 | 77,646 | 8 | 4 | 2 | 3 | 10 | published, never ranked |
| 264 | York | 0.30 | 118,066 | 6 | 2 | 1 | - | 10 | published, never ranked |
| 265 | Oxford | 0.28 | 111,583 | 5 | 1 | 1 | - | 10 | published, never ranked |
| 266 | Lucca | 0.13 | 52,271 | 10 | 3 | 1 | 27 | 10 | published, never ranked |
| 267 | Utrecht | 0.17 | 67,963 | 5 | 4 | 1 | - | 10 | published, never ranked |
| 268 | Antwerp | 0.25 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 269 | Athens | 0.25 | 235,429 | 12 | 6 | 2 | - | 20 | measured |
| 270 | Belgrade | 0.25 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 271 | Boston | 0.25 | 385,902 | 10 | 1 | 1 | - | 30 | measured |
| 272 | Bristol | 0.25 | 163,983 | 5 | 1 | - | - | 20 | measured |
| 273 | Budapest | 0.25 | 283,807 | 12 | 1 | 3 | - | 20 | measured |
| 274 | Cambridge | 0.25 | 97,974 | 5 | 2 | 1 | - | 10 | measured |
| 275 | Hoi An | 0.24 | 9,730 | - | - | - | - | 10 | predicted (thin competition) |
| 276 | Padua | 0.14 | 54,592 | 9 | 4 | 1 | 12 | 10 | published, never ranked |
| 277 | Maastricht | 0.12 | 47,763 | 5 | - | - | - | 10 | published, never ranked |
| 278 | Nijmegen | 0.11 | 42,338 | 5 | - | 1 | - | 10 | published, never ranked |
| 279 | Den Bosch | 0.10 | 39,682 | 11 | - | 1 | - | 10 | published, never ranked |
| 280 | Breda | 0.09 | 36,579 | 4 | - | 1 | - | 10 | published, never ranked |
| 281 | Phuket | 0.14 | 5,487 | - | - | - | - | 10 | predicted (thin competition) |
| 282 | Arnhem | 0.08 | 31,478 | 4 | - | - | - | 10 | published, never ranked |
| 283 | Gdansk | 0.12 | 4,908 | 4 | 2 | - | - | 10 | predicted (thin competition) |
| 284 | Groningen | 0.08 | 31,401 | 5 | - | 1 | - | 10 | published, never ranked |
| 285 | Haarlem | 0.08 | 33,960 | 4 | - | - | - | 10 | published, never ranked |
| 286 | Leiden | 0.08 | 33,227 | 6 | 4 | 1 | - | 10 | published, never ranked |
| 287 | Toledo | 0.08 | 3,149 | - | - | - | - | 10 | predicted (thin competition) |
| 288 | Baarn | 0.06 | 2,502 | 5 | 1 | 1 | - | 10 | predicted (thin competition) |
| 289 | Nikko | 0.05 | 1,926 | - | - | - | - | 10 | predicted (thin competition) |
| 290 | Bogota | 0.04 | 1,623 | - | - | - | - | 10 | predicted (thin competition) |
| 291 | Sao Paulo | 0.02 | 911 | - | - | - | - | 10 | predicted (thin competition) |
| 292 | San Sebastian | 0.01 | 367 | - | - | - | - | 10 | predicted (thin competition) |
| 293 | Bucaco | 0.00 | 132 | 6 | 1 | 1 | 29 | 10 | predicted (thin competition) |

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

