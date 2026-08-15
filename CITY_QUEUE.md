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
| 1 | Palermo | 40.62 | 124,310 | 10 | 7 | 2 | 44 | 20 | measured |
| 2 | Amsterdam | 36.63 | 294,030 | 20 | 7 | 2 | 5239 | 20 | measured |
| 3 | Rome | 32.39 | 358,876 | 29 | 9 | 2 | 32 | 30 | measured |
| 4 | Barcelona | 24.69 | 346,477 | 46 | 12 | 7 | 183 | 30 | measured |
| 5 | Prague | 27.34 | 303,350 | 17 | 13 | 3 | 29 | 30 | measured |
| 6 | Lisbon | 15.93 | 201,877 | 33 | 10 | 3 | 66 | 20 | measured |
| 7 | Vienna | 19.91 | 283,090 | 25 | 13 | 5 | 375 | 20 | measured |
| 8 | Toronto | 23.84 | 411,011 | - | - | - | - | 10 | predicted (travel demand) |
| 9 | Dublin | 13.54 | 240,850 | 17 | 4 | 2 | 12 | 20 | measured |
| 10 | Montreal | 22.81 | 315,322 | - | - | - | - | 10 | predicted (travel demand) |
| 11 | Brussels | 15.13 | 176,863 | 20 | 4 | 1 | 436 | 20 | measured |
| 12 | Munich | 14.60 | 224,067 | 29 | 13 | 6 | 76 | 20 | measured |
| 13 | Aarhus | 20.92 | 52,722 | - | - | - | - | 10 | predicted (travel demand) |
| 14 | Sydney | 19.69 | 305,304 | - | - | - | - | 10 | predicted (travel demand) |
| 15 | Brisbane | 12.73 | 162,602 | - | - | - | 186 | 10 | predicted (travel demand) |
| 16 | Frankfurt | 18.06 | 150,379 | - | - | - | - | 10 | predicted (travel demand) |
| 17 | Bologna | 10.35 | 146,161 | 12 | 7 | 2 | 9 | 20 | measured |
| 18 | Boston | 16.46 | 385,902 | 10 | 1 | 1 | - | 30 | measured |
| 19 | Perth | 16.42 | 180,478 | - | - | - | - | 10 | predicted (travel demand) |
| 20 | Cadiz | 10.88 | 79,226 | 5 | 4 | 1 | - | 10 | measured |
| 21 | Kyoto | 10.09 | 142,353 | 18 | 8 | 2 | - | 20 | measured |
| 22 | Vilnius | 14.80 | 113,188 | - | - | - | - | 10 | predicted (travel demand) |
| 23 | Melbourne | 9.64 | 267,898 | 8 | - | 1 | 382 | 10 | predicted (travel demand) |
| 24 | Los Angeles | 14.41 | 665,559 | - | - | - | - | 10 | predicted (travel demand) |
| 25 | Cambridge | 14.33 | 97,974 | 5 | 2 | 1 | - | 10 | measured |
| 26 | Berlin | 9.29 | 412,181 | 18 | 11 | 1 | 195 | 30 | measured |
| 27 | Bari | 8.65 | 86,456 | - | - | - | 4 | 10 | predicted (travel demand) |
| 28 | Seattle | 12.43 | 398,724 | - | - | - | - | 10 | predicted (travel demand) |
| 29 | Porto | 6.11 | 120,415 | 27 | 5 | 2 | 40 | 20 | measured |
| 30 | Cologne | 12.17 | 191,812 | - | - | - | - | 10 | predicted (travel demand) |
| 31 | Girona | 7.87 | 51,072 | - | - | - | - | 10 | predicted (travel demand) |
| 32 | Bilbao | 7.72 | 133,133 | - | - | - | - | 10 | predicted (travel demand) |
| 33 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 34 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 35 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 36 | Antwerp | 10.62 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 37 | Tokyo | 6.37 | 394,702 | 10 | 8 | - | 7 | 30 | measured |
| 38 | Hamburg | 10.27 | 191,221 | - | - | - | - | 10 | predicted (travel demand) |
| 39 | Athens | 10.09 | 235,429 | 12 | 6 | 2 | - | 20 | measured |
| 40 | Mexico City | 9.97 | 566,583 | - | - | - | - | 10 | predicted (travel demand) |
| 41 | Bratislava | 9.95 | 132,162 | - | - | - | - | 10 | predicted (travel demand) |
| 42 | Venice | 6.28 | 267,527 | 11 | 6 | 1 | 4 | 10 | published, never ranked (may be uncrawled) |
| 43 | Sintra | 6.11 | 46,889 | 5 | 3 | 1 | 6 | 10 | measured |
| 44 | Budapest | 9.82 | 283,807 | 12 | 1 | 3 | - | 20 | measured |
| 45 | Nice | 9.82 | 136,877 | 10 | 6 | 2 | - | 20 | measured |
| 46 | Vancouver | 9.47 | 351,552 | - | - | - | - | 10 | predicted (travel demand) |
| 47 | Lyon | 9.29 | 136,951 | 9 | 3 | 1 | - | 20 | measured |
| 48 | Manchester | 9.06 | 316,438 | - | - | - | - | 10 | predicted (travel demand) |
| 49 | Seville | 4.51 | 170,545 | 20 | 6 | 2 | - | 20 | measured |
| 50 | Pisa | 5.85 | 52,174 | - | - | - | - | 10 | predicted (travel demand) |
| 51 | Bristol | 8.76 | 163,983 | 5 | 1 | - | - | 20 | measured |
| 52 | Leipzig | 8.60 | 121,319 | - | - | - | - | 10 | predicted (travel demand) |
| 53 | Taipei | 8.38 | 143,193 | - | - | - | - | 10 | predicted (travel demand) |
| 54 | Salamanca | 5.50 | 47,897 | - | - | - | 1 | 10 | predicted (travel demand) |
| 55 | Hiroshima | 5.55 | 129,791 | - | - | - | - | 10 | predicted (travel demand) |
| 56 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 57 | San Francisco | 8.08 | 361,111 | - | - | - | - | 10 | predicted (travel demand) |
| 58 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 59 | Buenos Aires | 7.33 | 333,331 | - | - | - | - | 10 | predicted (travel demand) |
| 60 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 61 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 62 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 63 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 64 | London | 6.74 | 718,291 | 23 | 10 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 65 | Tallinn | 6.47 | 124,888 | - | - | - | - | 10 | predicted (travel demand) |
| 66 | Liverpool | 6.46 | 248,189 | - | - | - | - | 10 | predicted (travel demand) |
| 67 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 68 | Dresden | 6.41 | 113,624 | - | - | - | - | 10 | predicted (travel demand) |
| 69 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 70 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 71 | Rio de Janeiro | 6.36 | 279,431 | - | - | - | - | 10 | predicted (travel demand) |
| 72 | Freiburg | 6.18 | 92,752 | - | - | - | - | 10 | predicted (travel demand) |
| 73 | Gothenburg | 5.95 | 119,991 | - | - | - | - | 10 | predicted (travel demand) |
| 74 | Beijing | 5.73 | 269,737 | - | - | - | - | 10 | predicted (travel demand) |
| 75 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 76 | Bruges | 5.60 | 106,902 | - | - | - | - | 10 | predicted (travel demand) |
| 77 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 78 | San Diego | 5.53 | 214,939 | - | - | - | - | 10 | predicted (travel demand) |
| 79 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 80 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 81 | Philadelphia | 5.34 | 405,294 | - | - | - | - | 10 | predicted (travel demand) |
| 82 | Dubrovnik | 5.31 | 119,586 | 4 | 1 | 1 | - | 20 | measured |
| 83 | Milan | 2.64 | 212,705 | 18 | 9 | 2 | 25 | 10 | published, never ranked (may be uncrawled) |
| 84 | Sapporo | 3.51 | 88,633 | - | - | - | - | 10 | predicted (travel demand) |
| 85 | Leiden | 3.45 | 33,227 | 6 | 4 | 1 | - | 10 | measured |
| 86 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 87 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 88 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 89 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 90 | Lausanne | 4.90 | 68,242 | - | - | - | - | 10 | predicted (travel demand) |
| 91 | Riga | 4.90 | 108,918 | - | - | - | - | 10 | predicted (travel demand) |
| 92 | Graz | 4.84 | 65,717 | - | - | - | - | 10 | predicted (travel demand) |
| 93 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 94 | Nagoya | 3.17 | 83,437 | - | - | - | 1 | 10 | predicted (travel demand) |
| 95 | Miami | 4.74 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 96 | Auckland | 4.67 | 152,056 | - | - | - | - | 10 | predicted (travel demand) |
| 97 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 98 | New Orleans | 4.43 | 256,232 | - | - | - | - | 10 | predicted (travel demand) |
| 99 | Florence | 2.21 | 184,099 | 22 | 7 | 3 | 27 | 10 | published, never ranked (may be uncrawled) |
| 100 | Naha | 2.84 | 24,466 | - | - | - | 1 | 10 | predicted (travel demand) |
| 101 | Glasgow | 4.29 | 253,705 | 4 | 2 | - | - | 10 | published, never ranked (may be uncrawled) |
| 102 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 103 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 104 | Belfast | 4.15 | 224,315 | - | - | - | - | 10 | predicted (travel demand) |
| 105 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 106 | Stuttgart | 4.08 | 112,789 | - | - | - | - | 10 | predicted (travel demand) |
| 107 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 108 | Kanazawa | 2.53 | 25,778 | - | - | - | 2 | 10 | predicted (travel demand) |
| 109 | Nantes | 3.83 | 67,689 | - | - | - | - | 10 | predicted (travel demand) |
| 110 | Osaka | 2.54 | 163,112 | 4 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 111 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 112 | Malaga | 2.51 | 117,780 | 10 | 5 | 2 | - | 10 | published, never ranked (may be uncrawled) |
| 113 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 114 | Bath | 3.72 | 144,950 | 5 | 1 | 1 | - | 20 | measured |
| 115 | Zurich | 3.72 | 140,788 | 4 | - | - | - | 20 | measured |
| 116 | Sorrento | 1.94 | 40,049 | - | - | - | 20 | 10 | predicted (travel demand) |
| 117 | Strasbourg | 2.45 | 154,700 | 10 | 1 | 2 | 66 | 10 | published, never ranked (may be uncrawled) |
| 118 | Naples | 1.83 | 198,913 | 17 | 3 | 2 | 46 | 10 | published, never ranked (may be uncrawled) |
| 119 | Austin | 3.65 | 226,631 | - | - | - | - | 10 | predicted (travel demand) |
| 120 | Warsaw | 2.40 | 197,929 | 5 | 3 | - | 1441 | 10 | published, never ranked (may be uncrawled) |
| 121 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 122 | Rothenburg ob der Tauber | 3.08 | 39,879 | - | - | - | 8 | 10 | predicted (travel demand) |
| 123 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 124 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 125 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 126 | Brighton | 3.40 | 114,108 | - | - | - | - | 10 | predicted (travel demand) |
| 127 | Busan | 3.31 | 94,737 | - | - | - | - | 10 | predicted (travel demand) |
| 128 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 129 | Segovia | 2.17 | 30,968 | - | - | - | 1 | 10 | predicted (travel demand) |
| 130 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 131 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 132 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 133 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 134 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 135 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 136 | Savannah | 3.05 | 128,162 | - | - | - | - | 10 | predicted (travel demand) |
| 137 | Ljubljana | 2.98 | 125,046 | 4 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 138 | Turin | 1.49 | 147,456 | 10 | 7 | 2 | 30 | 10 | published, never ranked (may be uncrawled) |
| 139 | Sao Paulo | 2.96 | 911 | - | - | - | - | 10 | predicted (travel demand) |
| 140 | Madrid | 1.96 | 274,553 | 17 | 10 | 2 | - | 10 | published, never ranked (may be uncrawled) |
| 141 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 142 | Nuremberg | 1.94 | 161,614 | 10 | - | 1 | 39 | 10 | published, never ranked (may be uncrawled) |
| 143 | Poznan | 1.89 | 65,666 | 6 | - | 1 | 397 | 10 | published, never ranked (may be uncrawled) |
| 144 | Stockholm | 2.82 | 188,184 | 4 | 3 | - | - | 10 | published, never ranked (may be uncrawled) |
| 145 | Sofia | 2.81 | 138,710 | 4 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 146 | Bordeaux | 1.86 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 147 | Groningen | 1.86 | 31,401 | 5 | - | 1 | - | 10 | measured |
| 148 | Maastricht | 1.86 | 47,763 | 5 | - | - | - | 10 | measured |
| 149 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 150 | Modena | 1.77 | 51,698 | - | - | - | 3 | 10 | predicted (travel demand) |
| 151 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 152 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 153 | Rotterdam | 1.81 | 104,938 | 5 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 154 | Salzburg | 2.71 | 107,243 | - | - | - | - | 10 | predicted (travel demand) |
| 155 | Heidelberg | 2.69 | 75,837 | - | - | - | - | 10 | predicted (travel demand) |
| 156 | Caserta | 1.33 | 14,783 | 10 | - | 1 | 51 | 10 | measured |
| 157 | Washington DC | 2.65 | 606,731 | 14 | 1 | 2 | - | 30 | measured |
| 158 | Copenhagen | 2.62 | 218,621 | 13 | - | 2 | - | 10 | published, never ranked (may be uncrawled) |
| 159 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 160 | Kamakura | 1.74 | 33,492 | - | - | - | - | 10 | predicted (travel demand) |
| 161 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 162 | Ronda | 1.68 | 51,510 | - | - | - | 1 | 10 | predicted (travel demand) |
| 163 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 164 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 165 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 166 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 167 | Seoul | 2.41 | 206,265 | 8 | 5 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 168 | Fukuoka | 1.54 | 77,485 | 11 | 7 | 1 | 1 | 10 | published, never ranked (may be uncrawled) |
| 169 | Breda | 1.59 | 36,579 | 4 | - | 1 | - | 10 | measured |
| 170 | Luxembourg City | 2.39 | 64,851 | - | - | - | - | 10 | predicted (travel demand) |
| 171 | Brno | 1.58 | 63,714 | 7 | - | 2 | 30 | 10 | published, never ranked (may be uncrawled) |
| 172 | Padua | 1.36 | 54,592 | 10 | 4 | 1 | 12 | 10 | published, never ranked (may be uncrawled) |
| 173 | Ghent | 2.36 | 82,757 | - | - | - | - | 10 | predicted (travel demand) |
| 174 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 175 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 176 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 177 | Coimbra | 1.44 | 34,962 | - | - | - | 5 | 10 | predicted (travel demand) |
| 178 | Portland | 1.53 | 217,222 | 10 | 1 | 1 | 262 | 10 | published, never ranked (may be uncrawled) |
| 179 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 180 | Belgrade | 2.26 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 181 | Helsinki | 2.25 | 148,908 | 8 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 182 | Charleston | 2.21 | 155,987 | - | - | - | - | 10 | predicted (travel demand) |
| 183 | Rouen | 2.17 | 72,334 | - | - | - | 1 | 10 | predicted (travel demand) |
| 184 | Tarragona | 1.45 | 32,396 | - | - | - | - | 10 | predicted (travel demand) |
| 185 | Edinburgh | 2.13 | 292,981 | 15 | 4 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 186 | Leuven | 2.05 | 40,645 | - | - | - | - | 10 | predicted (travel demand) |
| 187 | Pamplona | 1.35 | 128,065 | - | - | - | 1 | 10 | predicted (travel demand) |
| 188 | Lima | 2.03 | 132,792 | - | - | - | - | 10 | predicted (travel demand) |
| 189 | Hallstatt | 1.99 | 47,271 | - | - | - | - | 10 | predicted (travel demand) |
| 190 | Utrecht | 1.32 | 67,963 | 5 | 4 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 191 | Wroclaw | 1.27 | 123,894 | 4 | - | 1 | 122 | 10 | published, never ranked (may be uncrawled) |
| 192 | Istanbul | 1.90 | 333,027 | 14 | 4 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 193 | Como | 0.96 | 82,645 | 9 | 2 | 1 | 23 | 10 | published, never ranked (may be uncrawled) |
| 194 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 195 | Cordoba | 1.06 | 74,675 | 10 | 2 | 2 | 3 | 10 | measured |
| 196 | Bangkok | 1.86 | 222,206 | 5 | - | 1 | - | 20 | measured |
| 197 | Hobart | 1.23 | 81,734 | 10 | - | 2 | 455 | 10 | published, never ranked (may be uncrawled) |
| 198 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 199 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 200 | Oslo | 1.76 | 181,113 | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 201 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 202 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 203 | Geneva | 1.13 | 162,269 | 6 | 4 | 1 | 129 | 10 | published, never ranked (may be uncrawled) |
| 204 | York | 1.69 | 118,066 | 6 | 2 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 205 | Cesky Krumlov | 1.36 | 28,582 | - | - | - | 11 | 10 | predicted (travel demand) |
| 206 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 207 | Gdansk | 1.06 | 4,908 | 4 | 2 | - | 228 | 10 | measured |
| 208 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 209 | Nijmegen | 1.05 | 42,338 | 5 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 210 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 211 | Cagliari | 0.92 | 51,351 | 7 | - | 2 | 9 | 10 | published, never ranked (may be uncrawled) |
| 212 | Matera | 1.00 | 67,033 | - | - | - | 2 | 10 | predicted (travel demand) |
| 213 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 214 | Cork | 0.97 | 101,405 | 5 | 2 | - | - | 10 | published, never ranked (may be uncrawled) |
| 215 | Reykjavik | 1.38 | 166,789 | 4 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 216 | Alicante | 0.67 | 77,454 | 9 | - | 1 | 44 | 10 | published, never ranked (may be uncrawled) |
| 217 | Bucharest | 1.33 | 136,836 | 4 | - | 1 | - | 20 | measured |
| 218 | Chicago | 1.33 | 485,769 | 6 | - | - | - | 30 | measured |
| 219 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 220 | Parma | 0.80 | 40,425 | 5 | - | 1 | 7 | 10 | published, never ranked (may be uncrawled) |
| 221 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 222 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 223 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 224 | Regensburg | 1.18 | 51,930 | - | - | - | 2 | 10 | predicted (travel demand) |
| 225 | Oxford | 1.21 | 111,583 | 5 | 1 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 226 | Paris | 0.80 | 524,268 | 25 | 9 | 3 | 129 | 30 | measured |
| 227 | Genoa | 0.66 | 145,206 | 10 | 1 | 1 | 11 | 10 | published, never ranked (may be uncrawled) |
| 228 | Palma de Mallorca | 0.71 | 84,075 | 5 | - | 1 | 8 | 10 | published, never ranked (may be uncrawled) |
| 229 | Zaragoza | 0.73 | 87,580 | 7 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 230 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 231 | Bamberg | 0.97 | 28,716 | - | - | - | 10 | 10 | predicted (travel demand) |
| 232 | Delft | 0.74 | 31,293 | 4 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 233 | Assisi | 0.68 | 30,278 | - | - | - | 6 | 10 | predicted (travel demand) |
| 234 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 235 | Toulouse | 0.73 | 112,721 | 10 | - | 1 | 34 | 10 | published, never ranked (may be uncrawled) |
| 236 | Trieste | 0.53 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 237 | Valencia | 0.53 | 162,209 | 16 | 2 | 2 | 350 | 20 | measured |
| 238 | Braga | 0.62 | 34,522 | 4 | - | - | 8 | 10 | published, never ranked (may be uncrawled) |
| 239 | Quebec City | 1.01 | 124,358 | 6 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 240 | Hong Kong | 0.66 | 689,212 | 10 | 2 | 1 | 505 | 30 | measured |
| 241 | Split | 0.97 | 132,399 | 4 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 242 | Granada | 0.60 | 86,361 | 10 | 3 | 2 | 4 | 10 | published, never ranked (may be uncrawled) |
| 243 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 244 | Catania | 0.57 | 58,252 | 4 | - | 1 | 5 | 10 | published, never ranked (may be uncrawled) |
| 245 | Lucca | 0.45 | 52,271 | 10 | 3 | 1 | 27 | 10 | published, never ranked (may be uncrawled) |
| 246 | Verona | 0.53 | 77,646 | 8 | 4 | 2 | 3 | 10 | measured |
| 247 | Krakow | 0.53 | 140,824 | 4 | 3 | 1 | 213 | 20 | measured |
| 248 | New York | 0.80 | 1,124,326 | 20 | 5 | 2 | - | 50 | measured |
| 249 | Singapore | 0.53 | 967,821 | 10 | 3 | 1 | 165 | 50 | measured |
| 250 | Potsdam | 0.51 | 51,727 | 6 | - | 1 | 30 | 10 | published, never ranked (may be uncrawled) |
| 251 | Haarlem | 0.50 | 33,960 | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 252 | Trento | 0.38 | 56,455 | 10 | 1 | 1 | 20 | 10 | published, never ranked (may be uncrawled) |
| 253 | Arnhem | 0.46 | 31,478 | 4 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 254 | Guimaraes | 0.32 | 26,203 | 6 | 1 | 1 | 19 | 10 | published, never ranked (may be uncrawled) |
| 255 | Perugia | 0.29 | 42,572 | 10 | - | 2 | 19 | 10 | published, never ranked (may be uncrawled) |
| 256 | Den Bosch | 0.36 | 39,682 | 11 | 1 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 257 | Thessaloniki | 0.53 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 258 | Bergamo | 0.27 | 52,933 | 8 | 1 | 1 | 17 | 10 | measured |
| 259 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 260 | The Hague | 0.27 | 236,723 | 5 | 1 | 1 | - | 20 | measured |
| 261 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 262 | Ferrara | 0.21 | 27,490 | 5 | - | 1 | 7 | 10 | published, never ranked (may be uncrawled) |
| 263 | Setubal | 0.19 | 22,582 | 10 | 1 | 2 | 13 | 10 | published, never ranked (may be uncrawled) |
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

