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

**The pool was audited and widened on 2026-08-17, in two ways, both on Hidde's questions.**

**First, cities that were simply never in it.** He asked whether we were missing American cities, and we were: 15 in a 293-city list, while the United States is our largest English-speaking source of visitors. Then he asked whether there were more, and there were. The audit was done against the most-read English WIKIVOYAGE articles of the last three months, 1,684 of them, diffed against this list, because that is the same metric the score already uses and it does not depend on anyone remembering a city. **41 places were added**: eleven American (Las Vegas enters at rank 22, above New York; Dallas and Houston in the forties), six Canadian (Halifax at 10,562 travel demand), three Finnish, two Australian, and the islands below. The cause of the gap is worth naming so it does not return: the pool was originally assembled by hand around European city-break tourism, so places that are not city breaks (Dallas, Houston, Kansas City, Winnipeg) never entered it. The audit is repeatable and should be re-run when the list feels stale; the method's one limit is that Wikivoyage's top list is truncated, so it finds the big holes and not the tail.

**Second, ISLANDS are now in the pool, and they are ranked by a rule that travel demand alone gets wrong** (Hidde, 2026-08-17: "ook kan ik me voorstellen dat eilanden interessant zijn en mss verdienen die een andere aanpak"). Seventeen entered, carrying `kind: "island"`. On travel demand they look mediocre, Santorini highest at 9,628 and Yakushima at 1,134, which would put most of them past rank 100. Two things the number cannot see argue the other way. **Competition is close to zero**: nobody writes in English about the old trees of La Gomera, and thin competition is where this site actually ranks. And **the product fit is better than any city's**: on a city page we compete with museums and restaurants for a visitor's afternoon, while on an island where people came to walk, we are the thing they came for. The trees carry the rest of the argument, since these are destinations in themselves: Yakushima's Jomon Sugi (UNESCO, thousands of years old), Tenerife's Drago Milenario, Sicily's Hundred Horse Chestnut, the laurel forests of La Gomera and Madeira that survived the Tertiary.

What this does NOT change: an island enters as an ordinary place in this one list and ships under the existing contracts. Nothing here creates a new page type, which would need Hidde's yes under hard rule 7. The schema already allows it, because it is keyed on coordinates rather than on the word city, which was the point of the third goal.

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
| 1 | Rome | 40.93 | 358,876 | 29 | 9 | 2 | 32 | 30 | measured |
| 2 | Palermo | 36.41 | 124,310 | 14 | 7 | 2 | 43 | 20 | measured |
| 3 | Amsterdam | 30.03 | 294,030 | 20 | 7 | 2 | 5239 | 20 | measured |
| 4 | Barcelona | 28.80 | 346,477 | 46 | 12 | 7 | 183 | 30 | measured |
| 5 | Lisbon | 23.65 | 201,877 | 33 | 10 | 3 | 66 | 20 | measured |
| 6 | Prague | 26.95 | 303,350 | 17 | 13 | 3 | 29 | 30 | measured |
| 7 | Florence | 18.72 | 184,099 | 22 | 7 | 3 | 27 | 20 | measured |
| 8 | Vienna | 23.45 | 283,090 | 25 | 13 | 5 | 375 | 20 | measured |
| 9 | Naples | 15.84 | 198,913 | 20 | 3 | 3 | 46 | 20 | measured |
| 10 | Dublin | 17.48 | 240,850 | 17 | 4 | 2 | 12 | 20 | measured |
| 11 | Paris | 19.33 | 524,268 | 30 | 9 | 4 | 129 | 30 | measured |
| 12 | Malaga | 18.31 | 117,780 | 10 | 5 | 2 | - | 20 | measured |
| 13 | Valencia | 12.55 | 162,209 | 16 | 2 | 2 | 350 | 20 | measured |
| 14 | Milan | 11.93 | 212,705 | 19 | 9 | 2 | 25 | 20 | measured |
| 15 | London | 23.24 | 718,291 | 23 | 10 | 1 | - | 50 | measured |
| 16 | Brussels | 15.02 | 176,863 | 23 | 4 | 1 | 436 | 20 | measured |
| 17 | Porto | 11.11 | 120,415 | 27 | 5 | 2 | 40 | 20 | measured |
| 18 | Bath | 21.60 | 144,950 | 5 | 1 | 1 | - | 20 | measured |
| 19 | Singapore | 14.40 | 967,821 | 18 | 3 | 2 | 165 | 50 | measured |
| 20 | Geneva | 14.19 | 162,269 | 14 | 4 | 3 | 133 | 20 | measured |
| 21 | Cambridge | 19.75 | 97,974 | 5 | 2 | 1 | - | 10 | measured |
| 22 | Sydney | 19.69 | 305,304 | - | - | - | - | 10 | predicted (travel demand) |
| 23 | Las Vegas | 19.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 24 | Boston | 18.92 | 385,902 | 10 | 1 | 1 | - | 30 | measured |
| 25 | New York | 18.10 | 1,124,326 | 20 | 5 | 2 | - | 50 | measured |
| 26 | Frankfurt | 18.06 | 150,379 | - | - | - | - | 10 | predicted (travel demand) |
| 27 | Perth | 16.42 | 180,478 | - | - | - | - | 10 | predicted (travel demand) |
| 28 | Granada | 9.67 | 86,361 | 10 | 3 | 2 | 4 | 10 | measured |
| 29 | Seville | 7.61 | 170,545 | 20 | 6 | 2 | - | 20 | measured |
| 30 | Madrid | 9.87 | 274,553 | 17 | 10 | 2 | - | 20 | measured |
| 31 | Los Angeles | 14.41 | 665,559 | - | - | - | - | 10 | predicted (travel demand) |
| 32 | Bari | 8.65 | 86,456 | - | - | - | 8 | 10 | predicted (travel demand) |
| 33 | Budapest | 14.19 | 283,807 | 12 | 1 | 3 | - | 20 | measured |
| 34 | Bologna | 8.02 | 146,161 | 12 | 7 | 2 | 9 | 20 | measured |
| 35 | Munich | 9.05 | 224,067 | 29 | 13 | 6 | 76 | 20 | measured |
| 36 | Sintra | 8.23 | 46,889 | 5 | 3 | 1 | 6 | 10 | measured |
| 37 | Washington DC | 13.16 | 606,731 | 14 | 1 | 2 | - | 30 | measured |
| 38 | The Hague | 8.64 | 236,723 | 5 | 1 | 1 | - | 20 | measured |
| 39 | Venice | 8.02 | 267,527 | 11 | 6 | 1 | 4 | 20 | measured |
| 40 | Seattle | 12.43 | 398,724 | - | - | - | - | 10 | predicted (travel demand) |
| 41 | Hawaii | 12.39 | - | - | - | - | - | 10 | predicted (travel demand) |
| 42 | Dallas | 12.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 43 | Houston | 12.22 | - | - | - | - | - | 10 | predicted (travel demand) |
| 44 | Cologne | 12.17 | 191,812 | - | - | - | - | 10 | predicted (travel demand) |
| 45 | Tokyo | 7.20 | 394,702 | 10 | 8 | - | 7 | 30 | measured |
| 46 | Girona | 7.87 | 51,072 | - | - | - | - | 10 | predicted (travel demand) |
| 47 | Bilbao | 7.72 | 133,133 | - | - | - | - | 10 | predicted (travel demand) |
| 48 | Ottawa | 7.62 | - | - | - | - | 119 | 10 | predicted (travel demand) |
| 49 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 50 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 51 | Lyon | 7.40 | 136,951 | 10 | 3 | 1 | 159 | 20 | measured |
| 52 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 53 | Kyoto | 7.20 | 142,353 | 18 | 8 | 2 | - | 20 | measured |
| 54 | Nice | 10.90 | 136,877 | 10 | 6 | 2 | - | 20 | measured |
| 55 | Kansas City | 10.51 | - | - | - | - | - | 10 | predicted (travel demand) |
| 56 | Edinburgh | 10.49 | 292,981 | 15 | 4 | 1 | - | 20 | measured |
| 57 | Asheville | 10.45 | - | - | - | - | - | 10 | predicted (travel demand) |
| 58 | Hamburg | 10.27 | 191,221 | - | - | - | - | 10 | predicted (travel demand) |
| 59 | Berlin | 6.79 | 412,181 | 18 | 11 | 1 | 195 | 30 | measured |
| 60 | Bristol | 10.08 | 163,983 | 5 | 1 | - | - | 20 | measured |
| 61 | Mexico City | 9.97 | 566,583 | - | - | - | - | 10 | predicted (travel demand) |
| 62 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 63 | Padua | 5.55 | 54,592 | 10 | 4 | 1 | 12 | 10 | measured |
| 64 | Dubrovnik | 9.26 | 119,586 | 4 | 1 | 1 | 2 | 20 | measured |
| 65 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 66 | Vancouver | 9.47 | 351,552 | - | - | - | - | 10 | predicted (travel demand) |
| 67 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 68 | Seoul | 9.26 | 206,265 | 8 | 5 | 1 | - | 20 | measured |
| 69 | Turku | 9.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 70 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 71 | Canberra | 9.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 72 | Manchester | 9.06 | 316,438 | - | - | - | - | 10 | predicted (travel demand) |
| 73 | Cadiz | 5.96 | 79,226 | 5 | 4 | 1 | - | 10 | measured |
| 74 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 75 | Pisa | 5.85 | 52,174 | - | - | - | - | 10 | predicted (travel demand) |
| 76 | Leiden | 5.76 | 33,227 | 6 | 4 | 1 | - | 10 | measured |
| 77 | Leipzig | 8.60 | 121,319 | - | - | - | - | 10 | predicted (travel demand) |
| 78 | Copenhagen | 8.43 | 218,621 | 16 | - | 2 | - | 20 | measured |
| 79 | Taipei | 8.38 | 143,193 | - | - | - | - | 10 | predicted (travel demand) |
| 80 | Salamanca | 5.50 | 47,897 | - | - | - | 1 | 10 | predicted (travel demand) |
| 81 | Hiroshima | 5.55 | 129,791 | - | - | - | - | 10 | predicted (travel demand) |
| 82 | Krakow | 5.55 | 140,824 | 16 | 3 | 3 | 198 | 20 | measured |
| 83 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 84 | San Francisco | 8.08 | 361,111 | - | - | - | - | 10 | predicted (travel demand) |
| 85 | Antwerp | 8.02 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 86 | Oslo | 8.02 | 181,113 | 4 | - | - | - | 20 | measured |
| 87 | Istanbul | 7.92 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 88 | Reykjavik | 7.82 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 89 | Cork | 5.14 | 101,405 | 5 | 2 | - | - | 20 | measured |
| 90 | Osaka | 5.14 | 163,112 | 4 | 1 | - | - | 20 | measured |
| 91 | Toronto | 5.96 | 411,011 | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 92 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 93 | Oahu | 5.23 | - | - | - | - | 21 | 10 | predicted (travel demand) |
| 94 | Turin | 3.70 | 147,456 | 10 | 7 | 2 | 30 | 20 | measured |
| 95 | Buenos Aires | 7.33 | 333,331 | - | - | - | - | 10 | predicted (travel demand) |
| 96 | Kauai | 7.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 97 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 98 | Alicante | 3.50 | 77,454 | 10 | 2 | 1 | 44 | 10 | measured |
| 99 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 100 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 101 | Portland | 4.53 | 217,222 | 10 | 1 | 1 | 282 | 20 | measured |
| 102 | Utrecht | 4.53 | 67,963 | 5 | 4 | 1 | - | 10 | measured |
| 103 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 104 | Athens | 6.58 | 235,429 | 12 | 6 | 2 | - | 20 | measured |
| 105 | Zurich | 6.58 | 140,788 | 4 | - | - | - | 20 | measured |
| 106 | Liverpool | 6.46 | 248,189 | - | - | - | - | 10 | predicted (travel demand) |
| 107 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 108 | Dresden | 6.41 | 113,624 | - | - | - | - | 10 | predicted (travel demand) |
| 109 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 110 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 111 | Rio de Janeiro | 6.36 | 279,431 | - | - | - | - | 10 | predicted (travel demand) |
| 112 | Genoa | 3.50 | 145,206 | 10 | 1 | 1 | 11 | 20 | measured |
| 113 | Detroit | 6.26 | - | - | - | - | - | 10 | predicted (travel demand) |
| 114 | Freiburg | 6.18 | 92,752 | - | - | - | - | 10 | predicted (travel demand) |
| 115 | Hong Kong | 4.01 | 689,212 | 10 | 2 | 1 | 505 | 30 | measured |
| 116 | Gothenburg | 5.95 | 119,991 | - | - | - | - | 10 | predicted (travel demand) |
| 117 | Rotterdam | 3.91 | 104,938 | 5 | - | 1 | - | 20 | measured |
| 118 | Denver | 5.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 119 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 120 | Helsinki | 5.76 | 148,908 | 8 | 1 | - | - | 20 | measured |
| 121 | Beijing | 5.73 | 269,737 | - | - | - | - | 10 | predicted (travel demand) |
| 122 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 123 | Montreal | 5.70 | 315,322 | 7 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 124 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 125 | Sacramento | 5.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 126 | Bruges | 5.60 | 106,902 | - | - | - | - | 10 | predicted (travel demand) |
| 127 | Haarlem | 3.70 | 33,960 | 4 | - | - | - | 10 | measured |
| 128 | Vilnius | 3.70 | 113,188 | 10 | 1 | 1 | 34 | 10 | published, never ranked (may be uncrawled) |
| 129 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 130 | San Diego | 5.53 | 214,939 | - | - | - | - | 10 | predicted (travel demand) |
| 131 | Setubal | 3.09 | 22,582 | 10 | 1 | 2 | 13 | 10 | measured |
| 132 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 133 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 134 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 135 | Lucca | 2.67 | 52,271 | 10 | 3 | 1 | 27 | 10 | measured |
| 136 | Philadelphia | 5.34 | 405,294 | - | - | - | - | 10 | predicted (travel demand) |
| 137 | Aarhus | 5.23 | 52,722 | 7 | 1 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 138 | Sapporo | 3.51 | 88,633 | - | - | - | - | 10 | predicted (travel demand) |
| 139 | Salt Lake City | 5.16 | - | - | - | - | - | 10 | predicted (travel demand) |
| 140 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 141 | Glasgow | 5.14 | 253,705 | 4 | 2 | - | - | 20 | measured |
| 142 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 143 | Oxford | 5.14 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 144 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 145 | Cardiff | 5.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 146 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 147 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 148 | Warsaw | 3.29 | 197,929 | 7 | 3 | - | 1416 | 20 | measured |
| 149 | Lausanne | 4.90 | 68,242 | - | - | - | - | 10 | predicted (travel demand) |
| 150 | Riga | 4.90 | 108,918 | - | - | - | - | 10 | predicted (travel demand) |
| 151 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 152 | Nagoya | 3.17 | 83,437 | - | - | - | 1 | 10 | predicted (travel demand) |
| 153 | Palma de Mallorca | 2.88 | 84,075 | 5 | 1 | 1 | 8 | 10 | measured |
| 154 | Brisbane | 3.18 | 162,602 | 10 | 1 | 1 | 186 | 10 | published, never ranked (may be uncrawled) |
| 155 | Miami | 4.74 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 156 | Auckland | 4.67 | 152,056 | - | - | - | - | 10 | predicted (travel demand) |
| 157 | Guimaraes | 2.47 | 26,203 | 6 | 1 | 1 | 19 | 10 | measured |
| 158 | Groningen | 3.09 | 31,401 | 5 | - | 1 | - | 10 | measured |
| 159 | Maastricht | 3.09 | 47,763 | 5 | - | - | - | 10 | measured |
| 160 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 161 | Caserta | 2.26 | 14,783 | 14 | - | 2 | 51 | 10 | measured |
| 162 | Menorca | 2.93 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 163 | New Orleans | 4.43 | 256,232 | - | - | - | - | 10 | predicted (travel demand) |
| 164 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 165 | Naha | 2.84 | 24,466 | - | - | - | 1 | 10 | predicted (travel demand) |
| 166 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 167 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 168 | Belfast | 4.15 | 224,315 | - | - | - | - | 10 | predicted (travel demand) |
| 169 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 170 | Stuttgart | 4.08 | 112,789 | - | - | - | - | 10 | predicted (travel demand) |
| 171 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 172 | Salzburg | 2.71 | 107,243 | - | - | - | 33 | 10 | predicted (travel demand) |
| 173 | Como | 2.06 | 82,645 | 9 | 2 | 1 | 23 | 10 | measured |
| 174 | Breda | 2.67 | 36,579 | 4 | - | 1 | - | 10 | measured |
| 175 | Nijmegen | 2.67 | 42,338 | 5 | - | 1 | - | 10 | measured |
| 176 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 177 | Kanazawa | 2.53 | 25,778 | - | - | - | 2 | 10 | predicted (travel demand) |
| 178 | Nantes | 3.83 | 67,689 | - | - | - | - | 10 | predicted (travel demand) |
| 179 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 180 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 181 | Bratislava | 2.49 | 132,162 | 6 | - | 1 | 26 | 10 | published, never ranked (may be uncrawled) |
| 182 | Split | 3.70 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 183 | Trieste | 1.85 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 184 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 185 | Zaragoza | 2.26 | 87,580 | 7 | - | 1 | - | 10 | measured |
| 186 | Austin | 3.65 | 226,631 | - | - | - | - | 10 | predicted (travel demand) |
| 187 | Cordoba | 2.26 | 74,675 | 15 | 2 | 2 | 3 | 10 | measured |
| 188 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 189 | Rothenburg ob der Tauber | 3.08 | 39,879 | - | - | - | 8 | 10 | predicted (travel demand) |
| 190 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 191 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 192 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 193 | Bergamo | 1.85 | 52,933 | 8 | 1 | 1 | 17 | 10 | measured |
| 194 | Brighton | 3.40 | 114,108 | - | - | - | - | 10 | predicted (travel demand) |
| 195 | Bordeaux | 2.26 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 196 | Den Bosch | 2.26 | 39,682 | 11 | 1 | 1 | - | 10 | measured |
| 197 | Busan | 3.31 | 94,737 | - | - | - | - | 10 | predicted (travel demand) |
| 198 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 199 | Segovia | 2.17 | 30,968 | - | - | - | 1 | 10 | predicted (travel demand) |
| 200 | Bangkok | 3.29 | 222,206 | 5 | 1 | 1 | - | 20 | measured |
| 201 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 202 | Ljubljana | 3.29 | 125,046 | 4 | - | 1 | - | 20 | measured |
| 203 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 204 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 205 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 206 | Arnhem | 2.06 | 31,478 | 4 | 1 | - | - | 10 | measured |
| 207 | Strasbourg | 2.06 | 154,700 | 10 | 1 | 2 | 66 | 20 | measured |
| 208 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 209 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 210 | Savannah | 3.05 | 128,162 | - | - | - | - | 10 | predicted (travel demand) |
| 211 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 212 | Sao Paulo | 2.96 | 911 | - | - | - | - | 10 | predicted (travel demand) |
| 213 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 214 | Nuremberg | 1.94 | 161,614 | 10 | 1 | 1 | 39 | 10 | published, never ranked (may be uncrawled) |
| 215 | Ibiza | 1.85 | - | - | - | - | - | 10 | predicted (travel demand) |
| 216 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 217 | Modena | 1.77 | 51,698 | - | - | - | 3 | 10 | predicted (travel demand) |
| 218 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 219 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 220 | Heidelberg | 2.69 | 75,837 | - | - | - | - | 10 | predicted (travel demand) |
| 221 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 222 | Kamakura | 1.74 | 33,492 | - | - | - | - | 10 | predicted (travel demand) |
| 223 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 224 | Verona | 1.65 | 77,646 | 8 | 4 | 2 | 3 | 10 | measured |
| 225 | Ronda | 1.68 | 51,510 | - | - | - | 1 | 10 | predicted (travel demand) |
| 226 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 227 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 228 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 229 | Hobart | 1.65 | 81,734 | 10 | - | 2 | 455 | 10 | measured |
| 230 | Maui | 2.33 | - | - | - | - | 3 | 10 | predicted (travel demand) |
| 231 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 232 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 233 | Tallinn | 1.62 | 124,888 | 4 | 1 | 1 | 42 | 10 | published, never ranked (may be uncrawled) |
| 234 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 235 | Fukuoka | 1.54 | 77,485 | 11 | 7 | 1 | 1 | 10 | published, never ranked (may be uncrawled) |
| 236 | Luxembourg City | 2.39 | 64,851 | - | - | - | - | 10 | predicted (travel demand) |
| 237 | Trento | 1.23 | 56,455 | 10 | 1 | 1 | 20 | 10 | measured |
| 238 | Brno | 1.58 | 63,714 | 7 | 1 | 2 | 30 | 10 | published, never ranked (may be uncrawled) |
| 239 | Ghent | 2.36 | 82,757 | - | - | - | - | 10 | predicted (travel demand) |
| 240 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 241 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 242 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 243 | Coimbra | 1.44 | 34,962 | - | - | - | 5 | 10 | predicted (travel demand) |
| 244 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 245 | Belgrade | 2.26 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 246 | Chicago | 2.26 | 485,769 | 6 | - | - | - | 30 | measured |
| 247 | Sofia | 2.26 | 138,710 | 4 | 1 | - | - | 20 | measured |
| 248 | Stockholm | 2.26 | 188,184 | 4 | 3 | - | - | 20 | measured |
| 249 | Charleston | 2.21 | 155,987 | - | - | - | - | 10 | predicted (travel demand) |
| 250 | Rouen | 2.17 | 72,334 | - | - | - | 1 | 10 | predicted (travel demand) |
| 251 | Tarragona | 1.45 | 32,396 | - | - | - | - | 10 | predicted (travel demand) |
| 252 | Gdansk | 1.44 | 4,908 | 4 | 2 | - | 228 | 10 | measured |
| 253 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 254 | Leuven | 2.05 | 40,645 | - | - | - | - | 10 | predicted (travel demand) |
| 255 | Pamplona | 1.35 | 128,065 | - | - | - | 1 | 10 | predicted (travel demand) |
| 256 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 257 | Lima | 2.03 | 132,792 | - | - | - | - | 10 | predicted (travel demand) |
| 258 | Hallstatt | 1.99 | 47,271 | - | - | - | - | 10 | predicted (travel demand) |
| 259 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 260 | Bucharest | 1.85 | 136,836 | 4 | - | 1 | - | 20 | measured |
| 261 | Thessaloniki | 1.85 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 262 | York | 1.85 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 263 | Graz | 1.21 | 65,717 | 10 | - | 1 | 87 | 10 | published, never ranked (may be uncrawled) |
| 264 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 265 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 266 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 267 | Yakushima | 1.13 | - | - | - | - | 1 | 10 | predicted (travel demand) |
| 268 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 269 | Cesky Krumlov | 1.36 | 28,582 | - | - | - | 11 | 10 | predicted (travel demand) |
| 270 | Perugia | 0.82 | 42,572 | 10 | - | 2 | 19 | 10 | measured |
| 271 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 272 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 273 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 274 | Delft | 1.03 | 31,293 | 4 | - | 1 | - | 10 | measured |
| 275 | Matera | 1.00 | 67,033 | - | - | - | 2 | 10 | predicted (travel demand) |
| 276 | Toulouse | 1.03 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 277 | Sardinia | 0.97 | - | 5 | - | - | 4 | 10 | published, never ranked (may be uncrawled) |
| 278 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 279 | Cagliari | 0.82 | 51,351 | 7 | 1 | 2 | 9 | 10 | measured |
| 280 | Ferrara | 0.82 | 27,490 | 5 | 1 | 1 | 7 | 10 | measured |
| 281 | Tenerife | 0.89 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 282 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 283 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 284 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 285 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 286 | Regensburg | 1.18 | 51,930 | - | - | - | 2 | 10 | predicted (travel demand) |
| 287 | Cyprus | 1.18 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 288 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 289 | Bamberg | 0.97 | 28,716 | - | - | - | 10 | 10 | predicted (travel demand) |
| 290 | Madeira | 0.77 | - | 6 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 291 | Assisi | 0.68 | 30,278 | - | - | - | 6 | 10 | predicted (travel demand) |
| 292 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 293 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 294 | Catania | 0.62 | 58,252 | 4 | 3 | 1 | 5 | 10 | measured |
| 295 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 296 | Sorrento | 0.49 | 40,049 | 4 | - | - | 20 | 10 | published, never ranked (may be uncrawled) |
| 297 | Poznan | 0.62 | 65,666 | 10 | - | 1 | 397 | 10 | measured |
| 298 | Crete | 0.86 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 299 | Parma | 0.41 | 40,425 | 5 | - | 1 | 7 | 10 | measured |
| 300 | Quebec City | 0.41 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 301 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 302 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 303 | Braga | 0.21 | 34,522 | 4 | 1 | - | 8 | 10 | measured |
| 304 | Melbourne | 0.21 | 267,898 | 12 | - | 2 | 397 | 20 | measured |
| 305 | Potsdam | 0.21 | 51,727 | 4 | - | 1 | 26 | 10 | measured |
| 306 | Wroclaw | 0.21 | 123,894 | 4 | 1 | 1 | 122 | 20 | measured |
| 307 | George Town | 0.28 | 36,080 | - | - | - | - | 10 | predicted (travel demand) |
| 308 | Queenstown | 0.16 | 36,672 | - | - | - | - | 10 | predicted (travel demand) |
| 309 | Halifax | 0.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 310 | Memphis | 0.04 | - | - | - | - | - | 10 | predicted (travel demand) |

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

