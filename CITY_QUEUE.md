# CITY_QUEUE: the one list, the one order, and how far to take a city

Written 2026-08-11 because Hidde said what everyone could see: "there are
multiple city prioritisations living amongst each other". There were six, and
they disagreed. This file replaces all of them. If another document names a
city order, it is stale and this one wins.

## The rule, derived from our own numbers rather than chosen

**Rewritten 2026-08-15, and it replaces the fame-penalty rule this file was
founded on.** Hidde asked whether Wikipedia pageviews really represent an
English-speaking tourist. They do not, and testing that question properly took
the old rule down with it. Both halves of the score were checked against the
one outcome we care about, `impressions_10d` from the Search Console readback,
on the 55 published cities Google has actually indexed:

| proxy | rank correlation with our impressions |
|---|---:|
| English Wikipedia pageviews (the old demand term) | +0.23 |
| **English Wikivoyage pageviews** (the new one) | **+0.33** |
| English share of pageviews (the anglophone idea) | +0.11 |

**Demand is travel intent, not fame.** `travel` (English Wikivoyage pageviews,
`scripts/travel_demand.py`) is the size term. Someone reading a Wikivoyage
article is planning a trip; someone reading Wikipedia is settling an argument.
Potsdam is famous for a conference and nobody packs a bag for it, which is
exactly the city the old proxy sent us to.

**The fame penalty is gone, and this file was wrong about it.** The founding
claim was "the more famous a city is, the worse we do there", drawn from ten
cities in a digest, and it paid out as a band multiplying contested cities by
1.08 and quiet ones by 2.50. On all 111 published cities it does not survive.
Split by travel demand into thirds:

| travel demand | cities | impressions per 100k travel views | clicks |
|---|---:|---:|---:|
| low | 37 | 206 | 12 |
| middle | 37 | 224 | 23 |
| high | 37 | 184 | 33 |

Impressions are flat and clicks run the other way outright. So the predicted
yield is now **flat**: we stopped penalising fame and deliberately did not
start rewarding it, because those click counts are small and half the site is
still unindexed. The old ten-city table was not a lie, it was a sample.

**The anglophone hypothesis was tested and failed**, and is recorded here so it
is not proposed again. Ranking by how English-dominant a city's readership is
scores +0.11, which is nothing, and our six best pages (Palermo, Amsterdam,
Rome, Prague, Barcelona, Vienna) are all in countries that read about
themselves in their own language. Measured on published pages, anglophone
cities earn 1.33 impressions per tree against 1.43 everywhere else: a wash.
English speakers do not read in English about where they live, they TRAVEL to
continental Europe, and Wikivoyage catches that while a language ratio cannot.

So the score is **travel demand times realised yield**, and yield comes from
evidence in this order:

1. **Measured**, where Search Console has spoken: what the city actually earns
   per 1,000 travel views, normalised so the median measured city sits at 1.0.
   53 cities.
2. **Published and never ranked** scores 0.25. This is now the shakiest rule
   here rather than the firmest, and it should be read with suspicion: it was
   written when a live page taking no clicks read as evidence of no demand, and
   we have since learned that 346 pages sit "Discovered - currently not
   indexed". London, Edinburgh, Portland, Hobart and Quebec City all show zero
   while never having been crawled, which is evidence of no crawl, not of low
   yield. Kept because demoting a page we cannot see is still the safer error;
   revisit the moment indexing improves.
3. **Predicted** for unpublished places: flat, at travel demand times 1.0.

`ease` is unchanged and still multiplies the order of work: a city with a
register nearby is cheap to open, measured at 0.4k tokens per tree against 27k
for research from zero.

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
being places Western tourists actually go; each carries measured demand
(**English Wikivoyage pageviews since 2026-08-15**, fetched per city, never
guessed; the Wikipedia figure it replaced is kept in the `demand` column for
comparison and is no longer what the rank is built on). The rank multiplies score
(demand times realised yield, clicks once measured) by an ease factor of 1.0 to
2.0: half for a country whose register story is proven (Portugal, Italy, Japan,
Ireland, Spain, the Dutch municipal pattern), half for register supply already
imported near the city. The boundary that keeps ease honest, from the Vienna-50
mistake of 2026-08-12: **ease multiplies the order of work, never the target.**
A register says cheap, not good.

**The pool narrowed on 2026-08-15: high-income destinations only, for now.**
Hidde, in two messages minutes apart: "Let's keep India out of the top 250 for
now. It's a huge country I don't want to focus on now", then "I want to focus on
cities for rich tourists." The rule is about the country VISITED rather than the
wealth of the visitor, and his own India cut is what settles that: Agra and
Jaipur are visited by affluent Westerners in large numbers and he cut them
anyway. Implemented in `scripts/rescore.py` on the World Bank income
classification, because it is a published citable line rather than a list
somebody felt good about: high income full weight, upper-middle half weight
(Thailand, Mexico, Brazil, Turkey, South Africa and the Balkans survive,
halved), low and lower-middle **paused**. Nineteen unpublished cities left the
list, the biggest being Ho Chi Minh City, Marrakech, Delhi, Ubud and Siem Reap.
Paused is not deleted: the row, its travel demand and its register supply all
stay, a published city is never unranked this way (hard rule 3), and lifting it
is deleting a line from one table. **A run may not add or remove a country
there.** The cost is real and is not hidden: several paused cities are places
the product would serve well, and this is a focus decision rather than a verdict
on them.

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
| 1 | Rome | 50.55 | 358,876 | 29 | 9 | 2 | 32 | 30 | measured |
| 2 | Palermo | 43.76 | 124,310 | 10 | 7 | 2 | 44 | 20 | measured |
| 3 | Amsterdam | 37.51 | 294,030 | 20 | 7 | 2 | 5239 | 20 | measured |
| 4 | Barcelona | 26.91 | 346,477 | 46 | 12 | 7 | 183 | 30 | measured |
| 5 | Lisbon | 25.82 | 201,877 | 33 | 10 | 3 | 66 | 20 | measured |
| 6 | Prague | 32.62 | 303,350 | 17 | 13 | 3 | 29 | 30 | measured |
| 7 | Naples | 22.02 | 198,913 | 17 | 3 | 2 | 46 | 20 | measured |
| 8 | Vienna | 27.72 | 283,090 | 25 | 13 | 5 | 375 | 20 | measured |
| 9 | Malaga | 27.18 | 117,780 | 10 | 5 | 2 | - | 20 | measured |
| 10 | Florence | 19.30 | 184,099 | 22 | 7 | 3 | 27 | 20 | measured |
| 11 | Dublin | 20.38 | 240,850 | 17 | 4 | 2 | 12 | 20 | measured |
| 12 | Paris | 22.83 | 524,268 | 25 | 9 | 3 | 129 | 30 | measured |
| 13 | Valencia | 15.49 | 162,209 | 16 | 2 | 2 | 350 | 20 | measured |
| 14 | Porto | 13.86 | 120,415 | 27 | 5 | 2 | 40 | 20 | measured |
| 15 | London | 25.82 | 718,291 | 23 | 10 | 1 | - | 50 | measured |
| 16 | Milan | 11.96 | 212,705 | 18 | 9 | 2 | 25 | 20 | measured |
| 17 | Toronto | 23.84 | 411,011 | - | - | - | - | 10 | predicted (travel demand) |
| 18 | Brussels | 15.49 | 176,863 | 20 | 4 | 1 | 436 | 20 | measured |
| 19 | Montreal | 22.81 | 315,322 | - | - | - | - | 10 | predicted (travel demand) |
| 20 | Geneva | 14.95 | 162,269 | 6 | 4 | 1 | 129 | 20 | measured |
| 21 | Munich | 14.68 | 224,067 | 29 | 13 | 6 | 76 | 20 | measured |
| 22 | New York | 21.74 | 1,124,326 | 20 | 5 | 2 | - | 50 | measured |
| 23 | Seville | 10.87 | 170,545 | 20 | 6 | 2 | - | 20 | measured |
| 24 | Boston | 20.38 | 385,902 | 10 | 1 | 1 | - | 30 | measured |
| 25 | Bologna | 11.69 | 146,161 | 12 | 7 | 2 | 9 | 20 | measured |
| 26 | Sydney | 19.69 | 305,304 | - | - | - | - | 10 | predicted (travel demand) |
| 27 | Cambridge | 19.57 | 97,974 | 5 | 2 | 1 | - | 10 | measured |
| 28 | Granada | 12.23 | 86,361 | 10 | 3 | 2 | 4 | 10 | measured |
| 29 | Singapore | 12.50 | 967,821 | 10 | 3 | 1 | 165 | 50 | measured |
| 30 | Tokyo | 11.14 | 394,702 | 10 | 8 | - | 7 | 30 | measured |
| 31 | Frankfurt | 18.06 | 150,379 | - | - | - | - | 10 | predicted (travel demand) |
| 32 | Sintra | 11.14 | 46,889 | 5 | 3 | 1 | 6 | 10 | measured |
| 33 | Kyoto | 11.69 | 142,353 | 18 | 8 | 2 | - | 20 | measured |
| 34 | Nice | 17.12 | 136,877 | 10 | 6 | 2 | - | 20 | measured |
| 35 | Perth | 16.42 | 180,478 | - | - | - | - | 10 | predicted (travel demand) |
| 36 | Bath | 14.95 | 144,950 | 5 | 1 | 1 | - | 20 | measured |
| 37 | Berlin | 9.78 | 412,181 | 18 | 11 | 1 | 195 | 30 | measured |
| 38 | Cadiz | 9.78 | 79,226 | 5 | 4 | 1 | - | 10 | measured |
| 39 | Los Angeles | 14.41 | 665,559 | - | - | - | - | 10 | predicted (travel demand) |
| 40 | Edinburgh | 14.13 | 292,981 | 15 | 4 | 1 | - | 20 | measured |
| 41 | Bari | 8.65 | 86,456 | - | - | - | 4 | 10 | predicted (travel demand) |
| 42 | Washington DC | 13.59 | 606,731 | 14 | 1 | 2 | - | 30 | measured |
| 43 | Budapest | 13.32 | 283,807 | 12 | 1 | 3 | - | 20 | measured |
| 44 | The Hague | 8.70 | 236,723 | 5 | 1 | 1 | - | 20 | measured |
| 45 | Venice | 8.15 | 267,527 | 11 | 6 | 1 | 4 | 20 | measured |
| 46 | Seattle | 12.43 | 398,724 | - | - | - | - | 10 | predicted (travel demand) |
| 47 | Cologne | 12.17 | 191,812 | - | - | - | - | 10 | predicted (travel demand) |
| 48 | Girona | 7.87 | 51,072 | - | - | - | - | 10 | predicted (travel demand) |
| 49 | Bilbao | 7.72 | 133,133 | - | - | - | - | 10 | predicted (travel demand) |
| 50 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 51 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 52 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 53 | Antwerp | 10.87 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 54 | Bristol | 10.60 | 163,983 | 5 | 1 | - | - | 20 | measured |
| 55 | Dubrovnik | 10.33 | 119,586 | 4 | 1 | 1 | - | 20 | measured |
| 56 | Lyon | 10.33 | 136,951 | 9 | 3 | 1 | - | 20 | measured |
| 57 | Hamburg | 10.27 | 191,221 | - | - | - | - | 10 | predicted (travel demand) |
| 58 | Mexico City | 9.97 | 566,583 | - | - | - | - | 10 | predicted (travel demand) |
| 59 | Bratislava | 9.95 | 132,162 | - | - | - | - | 10 | predicted (travel demand) |
| 60 | Istanbul | 9.65 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 61 | Vancouver | 9.47 | 351,552 | - | - | - | - | 10 | predicted (travel demand) |
| 62 | Krakow | 6.25 | 140,824 | 4 | 3 | 1 | 213 | 20 | measured |
| 63 | Athens | 9.24 | 235,429 | 12 | 6 | 2 | - | 20 | measured |
| 64 | Manchester | 9.06 | 316,438 | - | - | - | - | 10 | predicted (travel demand) |
| 65 | Seoul | 8.97 | 206,265 | 8 | 5 | 1 | - | 20 | measured |
| 66 | Pisa | 5.85 | 52,174 | - | - | - | - | 10 | predicted (travel demand) |
| 67 | Leipzig | 8.60 | 121,319 | - | - | - | - | 10 | predicted (travel demand) |
| 68 | Taipei | 8.38 | 143,193 | - | - | - | - | 10 | predicted (travel demand) |
| 69 | Salamanca | 5.50 | 47,897 | - | - | - | 1 | 10 | predicted (travel demand) |
| 70 | Hiroshima | 5.55 | 129,791 | - | - | - | - | 10 | predicted (travel demand) |
| 71 | Leiden | 5.44 | 33,227 | 6 | 4 | 1 | - | 10 | measured |
| 72 | Madrid | 5.44 | 274,553 | 17 | 10 | 2 | - | 20 | measured |
| 73 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 74 | San Francisco | 8.08 | 361,111 | - | - | - | - | 10 | predicted (travel demand) |
| 75 | Padua | 4.62 | 54,592 | 10 | 4 | 1 | 12 | 10 | measured |
| 76 | Turin | 3.81 | 147,456 | 10 | 7 | 2 | 30 | 20 | measured |
| 77 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 78 | Oslo | 7.34 | 181,113 | 4 | - | - | - | 20 | measured |
| 79 | Buenos Aires | 7.33 | 333,331 | - | - | - | - | 10 | predicted (travel demand) |
| 80 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 81 | Graz | 4.84 | 65,717 | - | - | - | 87 | 10 | predicted (travel demand) |
| 82 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 83 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 84 | Utrecht | 4.62 | 67,963 | 5 | 4 | 1 | - | 10 | measured |
| 85 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 86 | Liverpool | 6.46 | 248,189 | - | - | - | - | 10 | predicted (travel demand) |
| 87 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 88 | Dresden | 6.41 | 113,624 | - | - | - | - | 10 | predicted (travel demand) |
| 89 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 90 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 91 | Rio de Janeiro | 6.36 | 279,431 | - | - | - | - | 10 | predicted (travel demand) |
| 92 | Freiburg | 6.18 | 92,752 | - | - | - | - | 10 | predicted (travel demand) |
| 93 | Hong Kong | 4.08 | 689,212 | 10 | 2 | 1 | 505 | 30 | measured |
| 94 | Reykjavik | 5.98 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 95 | Gothenburg | 5.95 | 119,991 | - | - | - | - | 10 | predicted (travel demand) |
| 96 | Setubal | 3.26 | 22,582 | 10 | 1 | 2 | 13 | 10 | measured |
| 97 | Beijing | 5.73 | 269,737 | - | - | - | - | 10 | predicted (travel demand) |
| 98 | Cork | 3.81 | 101,405 | 5 | 2 | - | - | 20 | measured |
| 99 | Oxford | 5.71 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 100 | Portland | 3.81 | 217,222 | 10 | 1 | 1 | 282 | 20 | measured |
| 101 | Rotterdam | 3.81 | 104,938 | 5 | - | 1 | - | 20 | measured |
| 102 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 103 | Bruges | 5.60 | 106,902 | - | - | - | - | 10 | predicted (travel demand) |
| 104 | Vilnius | 3.70 | 113,188 | 7 | - | 1 | 34 | 10 | published, never ranked (may be uncrawled) |
| 105 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 106 | San Diego | 5.53 | 214,939 | - | - | - | - | 10 | predicted (travel demand) |
| 107 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 108 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 109 | Zurich | 5.44 | 140,788 | 4 | - | - | - | 20 | measured |
| 110 | Philadelphia | 5.34 | 405,294 | - | - | - | - | 10 | predicted (travel demand) |
| 111 | Aarhus | 5.23 | 52,722 | 7 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 112 | Haarlem | 3.53 | 33,960 | 4 | - | - | - | 10 | measured |
| 113 | Sapporo | 3.51 | 88,633 | - | - | - | - | 10 | predicted (travel demand) |
| 114 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 115 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 116 | Verona | 3.26 | 77,646 | 8 | 4 | 2 | 3 | 10 | measured |
| 117 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 118 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 119 | Lausanne | 4.90 | 68,242 | - | - | - | - | 10 | predicted (travel demand) |
| 120 | Lucca | 2.45 | 52,271 | 10 | 3 | 1 | 27 | 10 | measured |
| 121 | Riga | 4.90 | 108,918 | - | - | - | - | 10 | predicted (travel demand) |
| 122 | Glasgow | 4.89 | 253,705 | 4 | 2 | - | - | 20 | measured |
| 123 | Groningen | 3.26 | 31,401 | 5 | - | 1 | - | 10 | measured |
| 124 | Maastricht | 3.26 | 47,763 | 5 | - | - | - | 10 | measured |
| 125 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 126 | Nagoya | 3.17 | 83,437 | - | - | - | 1 | 10 | predicted (travel demand) |
| 127 | Brisbane | 3.18 | 162,602 | 10 | - | 1 | 186 | 10 | published, never ranked (may be uncrawled) |
| 128 | Miami | 4.74 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 129 | Auckland | 4.67 | 152,056 | - | - | - | - | 10 | predicted (travel demand) |
| 130 | Split | 4.62 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 131 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 132 | New Orleans | 4.43 | 256,232 | - | - | - | - | 10 | predicted (travel demand) |
| 133 | Zaragoza | 2.72 | 87,580 | 7 | - | 1 | - | 10 | measured |
| 134 | Trieste | 2.17 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 135 | Naha | 2.84 | 24,466 | - | - | - | 1 | 10 | predicted (travel demand) |
| 136 | Como | 2.17 | 82,645 | 9 | 2 | 1 | 23 | 10 | measured |
| 137 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 138 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 139 | Belfast | 4.15 | 224,315 | - | - | - | - | 10 | predicted (travel demand) |
| 140 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 141 | Nijmegen | 2.72 | 42,338 | 5 | - | 1 | - | 10 | measured |
| 142 | Stuttgart | 4.08 | 112,789 | - | - | - | - | 10 | predicted (travel demand) |
| 143 | York | 4.08 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 144 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 145 | Kanazawa | 2.53 | 25,778 | - | - | - | 2 | 10 | predicted (travel demand) |
| 146 | Nantes | 3.83 | 67,689 | - | - | - | - | 10 | predicted (travel demand) |
| 147 | Copenhagen | 3.81 | 218,621 | 13 | - | 2 | - | 20 | measured |
| 148 | Caserta | 1.90 | 14,783 | 10 | - | 1 | 51 | 10 | measured |
| 149 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 150 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 151 | Bordeaux | 2.45 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 152 | Den Bosch | 2.45 | 39,682 | 11 | 1 | 1 | - | 10 | measured |
| 153 | Osaka | 2.45 | 163,112 | 4 | 1 | - | - | 20 | measured |
| 154 | Warsaw | 2.45 | 197,929 | 5 | 3 | - | 1441 | 20 | measured |
| 155 | Austin | 3.65 | 226,631 | - | - | - | - | 10 | predicted (travel demand) |
| 156 | Melbourne | 2.41 | 267,898 | 12 | - | 2 | 397 | 10 | published, never ranked (may be uncrawled) |
| 157 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 158 | Rothenburg ob der Tauber | 3.08 | 39,879 | - | - | - | 8 | 10 | predicted (travel demand) |
| 159 | Bergamo | 1.90 | 52,933 | 8 | 1 | 1 | 17 | 10 | measured |
| 160 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 161 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 162 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 163 | Brighton | 3.40 | 114,108 | - | - | - | - | 10 | predicted (travel demand) |
| 164 | Busan | 3.31 | 94,737 | - | - | - | - | 10 | predicted (travel demand) |
| 165 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 166 | Segovia | 2.17 | 30,968 | - | - | - | 1 | 10 | predicted (travel demand) |
| 167 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 168 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 169 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 170 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 171 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 172 | Guimaraes | 1.63 | 26,203 | 6 | 1 | 1 | 19 | 10 | measured |
| 173 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 174 | Savannah | 3.05 | 128,162 | - | - | - | - | 10 | predicted (travel demand) |
| 175 | Cordoba | 1.90 | 74,675 | 15 | 2 | 2 | 3 | 10 | measured |
| 176 | Sao Paulo | 2.96 | 911 | - | - | - | - | 10 | predicted (travel demand) |
| 177 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 178 | Nuremberg | 1.94 | 161,614 | 10 | - | 1 | 39 | 10 | published, never ranked (may be uncrawled) |
| 179 | Breda | 1.90 | 36,579 | 4 | - | 1 | - | 10 | measured |
| 180 | Poznan | 1.89 | 65,666 | 10 | - | 1 | 397 | 10 | published, never ranked (may be uncrawled) |
| 181 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 182 | Modena | 1.77 | 51,698 | - | - | - | 3 | 10 | predicted (travel demand) |
| 183 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 184 | Chicago | 2.72 | 485,769 | 6 | - | - | - | 30 | measured |
| 185 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 186 | Salzburg | 2.71 | 107,243 | - | - | - | - | 10 | predicted (travel demand) |
| 187 | Heidelberg | 2.69 | 75,837 | - | - | - | - | 10 | predicted (travel demand) |
| 188 | Trento | 1.36 | 56,455 | 10 | 1 | 1 | 20 | 10 | measured |
| 189 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 190 | Kamakura | 1.74 | 33,492 | - | - | - | - | 10 | predicted (travel demand) |
| 191 | Belgrade | 2.58 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 192 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 193 | Ronda | 1.68 | 51,510 | - | - | - | 1 | 10 | predicted (travel demand) |
| 194 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 195 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 196 | Genoa | 1.36 | 145,206 | 10 | 1 | 1 | 11 | 20 | measured |
| 197 | Thessaloniki | 2.45 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 198 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 199 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 200 | Tallinn | 1.62 | 124,888 | 4 | - | 1 | 42 | 10 | published, never ranked (may be uncrawled) |
| 201 | Fukuoka | 1.54 | 77,485 | 11 | 7 | 1 | 1 | 10 | published, never ranked (may be uncrawled) |
| 202 | Luxembourg City | 2.39 | 64,851 | - | - | - | - | 10 | predicted (travel demand) |
| 203 | Brno | 1.58 | 63,714 | 7 | - | 2 | 30 | 10 | published, never ranked (may be uncrawled) |
| 204 | Ghent | 2.36 | 82,757 | - | - | - | - | 10 | predicted (travel demand) |
| 205 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 206 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 207 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 208 | Coimbra | 1.44 | 34,962 | - | - | - | 5 | 10 | predicted (travel demand) |
| 209 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 210 | Charleston | 2.21 | 155,987 | - | - | - | - | 10 | predicted (travel demand) |
| 211 | Rouen | 2.17 | 72,334 | - | - | - | 1 | 10 | predicted (travel demand) |
| 212 | Bangkok | 2.17 | 222,206 | 5 | - | 1 | - | 20 | measured |
| 213 | Tarragona | 1.45 | 32,396 | - | - | - | - | 10 | predicted (travel demand) |
| 214 | Leuven | 2.05 | 40,645 | - | - | - | - | 10 | predicted (travel demand) |
| 215 | Pamplona | 1.35 | 128,065 | - | - | - | 1 | 10 | predicted (travel demand) |
| 216 | Gdansk | 1.36 | 4,908 | 4 | 2 | - | 228 | 10 | measured |
| 217 | Strasbourg | 1.36 | 154,700 | 10 | 1 | 2 | 66 | 20 | measured |
| 218 | Lima | 2.03 | 132,792 | - | - | - | - | 10 | predicted (travel demand) |
| 219 | Hallstatt | 1.99 | 47,271 | - | - | - | - | 10 | predicted (travel demand) |
| 220 | Wroclaw | 1.27 | 123,894 | 4 | - | 1 | 122 | 10 | published, never ranked (may be uncrawled) |
| 221 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 222 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 223 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 224 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 225 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 226 | Cesky Krumlov | 1.36 | 28,582 | - | - | - | 11 | 10 | predicted (travel demand) |
| 227 | Delft | 1.09 | 31,293 | 4 | - | 1 | - | 10 | measured |
| 228 | Hobart | 1.09 | 81,734 | 10 | - | 2 | 455 | 10 | measured |
| 229 | Perugia | 0.82 | 42,572 | 10 | - | 2 | 19 | 10 | measured |
| 230 | Toulouse | 1.09 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 231 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 232 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 233 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 234 | Matera | 1.00 | 67,033 | - | - | - | 2 | 10 | predicted (travel demand) |
| 235 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 236 | Quebec City | 1.01 | 124,358 | 6 | - | 1 | 494 | 10 | published, never ranked (may be uncrawled) |
| 237 | Bucharest | 1.36 | 136,836 | 4 | - | 1 | - | 20 | measured |
| 238 | Helsinki | 1.36 | 148,908 | 8 | 1 | - | - | 20 | measured |
| 239 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 240 | Parma | 0.80 | 40,425 | 5 | - | 1 | 7 | 10 | published, never ranked (may be uncrawled) |
| 241 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 242 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 243 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 244 | Regensburg | 1.18 | 51,930 | - | - | - | 2 | 10 | predicted (travel demand) |
| 245 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 246 | Bamberg | 0.97 | 28,716 | - | - | - | 10 | 10 | predicted (travel demand) |
| 247 | Assisi | 0.68 | 30,278 | - | - | - | 6 | 10 | predicted (travel demand) |
| 248 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 249 | Ljubljana | 1.09 | 125,046 | 4 | - | 1 | - | 20 | measured |
| 250 | Braga | 0.62 | 34,522 | 4 | - | - | 8 | 10 | published, never ranked (may be uncrawled) |
| 251 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 252 | Sorrento | 0.49 | 40,049 | 4 | - | - | 20 | 10 | published, never ranked (may be uncrawled) |
| 253 | Arnhem | 0.54 | 31,478 | 4 | 1 | - | - | 10 | measured |
| 254 | Potsdam | 0.51 | 51,727 | 4 | - | 1 | 26 | 10 | published, never ranked (may be uncrawled) |
| 255 | Alicante | 0.27 | 77,454 | 9 | - | 1 | 44 | 10 | measured |
| 256 | Sofia | 0.54 | 138,710 | 4 | 1 | - | - | 20 | measured |
| 257 | Stockholm | 0.54 | 188,184 | 4 | 3 | - | - | 20 | measured |
| 258 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 259 | Cagliari | 0.27 | 51,351 | 7 | - | 2 | 9 | 10 | measured |
| 260 | Palma de Mallorca | 0.27 | 84,075 | 5 | - | 1 | 8 | 10 | measured |
| 261 | Catania | 0.27 | 58,252 | 4 | - | 1 | 5 | 10 | measured |
| 262 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 263 | Ferrara | 0.21 | 27,490 | 5 | - | 1 | 7 | 10 | published, never ranked (may be uncrawled) |
| 264 | George Town | 0.28 | 36,080 | - | - | - | - | 10 | predicted (travel demand) |
| 265 | Queenstown | 0.16 | 36,672 | - | - | - | - | 10 | predicted (travel demand) |

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

