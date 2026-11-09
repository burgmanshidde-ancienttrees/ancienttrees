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

**Settled 2026-08-19, after two corrections the same morning.** Both are Hidde's
and the second overrides the first, so read them in order.

1. **OPEN THE UNOPENED CITIES FIRST.** He said it after looking at the list
   itself: "persoonlijk denk ik dat deze steden zonder register toch starten
   interessanter is dan verdiepen... deze zsm naar 10 krijgen." He named
   Seattle, Dallas, Houston, Cologne, Perth, Sydney, Las Vegas, Frankfurt,
   Bilbao, Dubai, Kansas City, Mexico City, Vancouver, Manchester, Taipei,
   Buenos Aires and Hawaii: all ranked, all at zero trees, most with no
   register behind them. The reasoning is in the numbers he was reading. A new
   city taken to 10 is a page that can start ranking; a thirtieth tree in Rome
   is marginal.

   **This means from-zero web research is ON for these**, which is normally off.
   Rule one (d) has always allowed it when Hidde names the city, and he has.
   Expect them to cost web-research rates rather than register rates, and use
   the 80/20 rule hard: a city that will not give up four good trees cheaply is
   not a city to grind on.

2. **Then deepen, to these targets.** Superseded again on 2026-09-23: Hidde
   said "kijk naar hoe groot een stad is en stel daar het plafond op, ik denk
   dat het zo simpel is", and it is. The ceiling is population, not whether
   Search Console has confirmed the city yet; confirmation now only moves the
   queue's *order* (via `score`), never the *ceiling*. `target_for()` in
   scripts/city_queue.py is the one place this number is computed:

   | population | target |
   |---|---:|
   | under 50,000 | 10 |
   | 50,000 to 250,000 | 20 |
   | 250,000 to 1m | 30 |
   | 1m to 5m | 60 |
   | over 5m | 100 |

   His three calibration points: Baarn (24,528) stops at 10, Copenhagen
   (602,481) at 30, Tokyo (14,047,594) at 100. A city whose population could
   not be resolved keeps the prior behaviour rather than silently dropping to
   10. This retires the prior state-keyed table (new/unconfirmed -> 10,
   confirmed -> 20, confirmed BIG -> 30), which read a big city that Search
   Console had not yet confirmed as capped at 10: that conflated two
   different questions, how many trees a place could hold and where the next
   hour of work goes, and only the second should key off measured demand.

3. **The 80/20 rule governs everything above** (his words: "eeuwig tokens
   gebruiken tot deze max te halen is niet de strategie... als het er wat
   minder zijn maar het wordt te moeilijk om de volgende te vinden ga gewoon
   door"). A target is a ceiling and a stopping point, never a quota. Cadiz at
   5 is finished work.

4. **The queue re-ranks itself daily** from the digest's Search Console
   readback, so a city that starts performing climbs on its own.

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
| 1 | Seville | 94.62 | 170,545 | 44 | 12 | 2 | - | 30 | measured |
| 2 | Palermo | 62.74 | 124,310 | 27 | 13 | 3 | 38 | 30 | measured |
| 3 | Lisbon | 61.71 | 201,877 | 37 | 21 | 3 | 67 | 30 | measured |
| 4 | Tokyo | 65.82 | 394,702 | 22 | 16 | 1 | 5 | 100 | measured |
| 5 | Berlin | 75.08 | 412,181 | 63 | 51 | 5 | 195 | 60 | measured |
| 6 | Tenerife | 60.68 | - | 9 | 6 | - | - | 30 | measured |
| 7 | Singapore | 58.62 | 967,821 | 34 | 7 | 3 | 165 | 100 | measured |
| 8 | New York | 67.88 | 1,124,326 | 97 | 10 | 8 | - | 100 | measured |
| 9 | Malaga | 36.00 | 117,780 | 10 | 5 | 1 | - | 30 | measured |
| 10 | Munich | 36.00 | 224,067 | 63 | 35 | 8 | 74 | 60 | measured |
| 11 | Fukuoka | 34.97 | 77,485 | 18 | 11 | 1 | - | 60 | measured |
| 12 | Paris | 34.97 | 524,268 | 58 | 15 | 8 | 129 | 60 | measured |
| 13 | San Francisco | 34.97 | 361,111 | 12 | 3 | 1 | 26 | 30 | measured |
| 14 | Amsterdam | 25.71 | 294,030 | 27 | 7 | 2 | 5488 | 30 | measured |
| 15 | Porto | 23.66 | 120,415 | 32 | 16 | 3 | 40 | 30 | measured |
| 16 | Kyoto | 29.83 | 142,353 | 18 | 14 | 2 | - | 60 | measured |
| 17 | Copenhagen | 43.20 | 218,621 | 49 | 41 | 6 | - | 30 | measured |
| 18 | London | 38.05 | 718,291 | 48 | 37 | 1 | - | 100 | measured |
| 19 | Alicante | 21.60 | 77,454 | 21 | 4 | 2 | 44 | 30 | measured |
| 20 | Monterey | 43.20 | - | 3 | 2 | - | - | 10 | measured |
| 21 | Rome | 21.60 | 358,876 | 32 | 10 | 2 | 31 | 60 | measured |
| 22 | Austin | 41.14 | 226,631 | 12 | 5 | 1 | - | 30 | measured |
| 23 | Coimbra | 21.60 | 34,962 | 6 | - | - | 5 | 20 | measured |
| 24 | Birmingham | 37.53 | - | - | - | - | - | 60 | predicted (travel demand) |
| 25 | Brisbane | 24.68 | 162,602 | 20 | 5 | 2 | 186 | 60 | measured |
| 26 | Venice | 19.54 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 27 | Dublin | 18.51 | 240,850 | 19 | 4 | 2 | 12 | 30 | measured |
| 28 | Oahu | 30.86 | - | 32 | 8 | 4 | - | 30 | measured |
| 29 | Madrid | 18.51 | 274,553 | 18 | 11 | 2 | - | 60 | measured |
| 30 | Boston | 28.80 | 385,902 | 40 | 3 | 4 | - | 30 | measured |
| 31 | Cambridge | 28.80 | 97,974 | 10 | 2 | 1 | - | 20 | measured |
| 32 | Los Angeles | 24.68 | 665,559 | 19 | 3 | 1 | - | 60 | measured |
| 33 | Florence | 12.34 | 184,099 | 29 | 9 | 1 | 27 | 30 | measured |
| 34 | Philadelphia | 22.63 | 405,294 | 9 | 1 | - | - | 60 | measured |
| 35 | Seattle | 22.63 | 398,724 | 30 | 3 | 4 | - | 30 | measured |
| 36 | Luxembourg City | 15.43 | 64,851 | 10 | 8 | 2 | 18 | 20 | measured |
| 37 | Prague | 15.43 | 303,350 | 30 | 21 | 4 | 31 | 60 | measured |
| 38 | Charleston | 22.63 | 155,987 | 4 | 1 | - | - | 20 | measured |
| 39 | The Hague | 11.31 | 236,723 | 26 | 4 | 5 | 166 | 30 | measured |
| 40 | Reykjavik | 19.54 | 166,789 | 4 | 3 | 1 | - | 20 | measured |
| 41 | Kanazawa | 14.40 | 25,778 | 7 | 3 | 1 | 2 | 30 | measured |
| 42 | Barcelona | 10.29 | 346,477 | 58 | 20 | 7 | 177 | 60 | measured |
| 43 | Milan | 10.28 | 212,705 | 30 | 14 | 3 | 25 | 60 | measured |
| 44 | Long Beach | 20.48 | - | - | - | - | - | 30 | predicted (travel demand) |
| 45 | Little Rock | 20.40 | - | - | - | - | - | 20 | predicted (travel demand) |
| 46 | Seoul | 18.51 | 206,265 | 8 | 5 | 1 | - | 100 | measured |
| 47 | Bologna | 10.29 | 146,161 | 12 | 7 | 1 | 9 | 30 | measured |
| 48 | Athens | 18.51 | 235,429 | 12 | 7 | 2 | - | 30 | measured |
| 49 | Edinburgh | 18.51 | 292,981 | 21 | 10 | 1 | - | 30 | measured |
| 50 | Amersfoort | 9.26 | - | 21 | 1 | 2 | 181 | 20 | measured |
| 51 | Valencia | 9.26 | 162,209 | 31 | 4 | 2 | 350 | 30 | measured |
| 52 | Bath | 18.51 | 144,950 | 9 | 2 | 2 | - | 20 | measured |
| 53 | Portland | 12.34 | 217,222 | 33 | 2 | 3 | 306 | 30 | measured |
| 54 | Reno | 18.19 | - | - | - | - | - | 30 | predicted (travel demand) |
| 55 | Des Moines | 18.11 | - | - | - | - | - | 20 | predicted (travel demand) |
| 56 | Daytona Beach | 17.66 | - | - | - | - | - | 20 | predicted (travel demand) |
| 57 | Cagliari | 9.26 | 51,351 | 14 | 1 | 2 | 14 | 20 | measured |
| 58 | Leeuwarden | 8.23 | - | 34 | - | 2 | 61 | 20 | measured |
| 59 | Montreal | 16.46 | 315,322 | 14 | 2 | 2 | - | 60 | measured |
| 60 | New Orleans | 16.46 | 256,232 | 8 | 6 | 1 | - | 30 | measured |
| 61 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 62 | Washington DC | 14.40 | 606,731 | 34 | 8 | 4 | - | 30 | measured |
| 63 | Huntsville | 15.35 | - | - | - | - | - | 20 | predicted (travel demand) |
| 64 | Sardinia | 8.23 | - | 7 | 6 | - | 10 | 60 | measured |
| 65 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 66 | Segovia | 9.26 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 67 | West Palm Beach | 14.98 | - | - | - | - | - | 20 | predicted (travel demand) |
| 68 | Saint Petersburg | 14.83 | - | - | - | - | - | 100 | predicted (travel demand) |
| 69 | St. Louis | 14.80 | - | - | - | - | - | 30 | predicted (travel demand) |
| 70 | Perth | 14.40 | 180,478 | 6 | 4 | 1 | - | 60 | measured |
| 71 | Toronto | 14.40 | 411,011 | 6 | - | - | - | 60 | measured |
| 72 | Naples | 7.20 | 198,913 | 31 | 5 | 3 | 47 | 30 | measured |
| 73 | San Diego | 14.40 | 214,939 | 13 | 1 | 2 | - | 60 | measured |
| 74 | Krakow | 9.26 | 140,824 | 38 | 11 | 3 | 198 | 30 | measured |
| 75 | Sapporo | 9.26 | 88,633 | 6 | 1 | - | - | 60 | measured |
| 76 | Cincinnati | 13.33 | - | - | - | - | - | 30 | predicted (travel demand) |
| 77 | Lansing | 13.02 | - | - | - | - | - | 20 | predicted (travel demand) |
| 78 | Cadiz | 8.23 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 79 | Detroit | 12.53 | - | - | - | - | - | 30 | predicted (travel demand) |
| 80 | Brussels | 8.23 | 176,863 | 35 | 4 | 2 | 436 | 60 | measured |
| 81 | Hiroshima | 8.23 | 129,791 | 33 | 5 | 2 | - | 60 | measured |
| 82 | Antwerp | 12.34 | 128,289 | 10 | 4 | 1 | - | 30 | measured |
| 83 | Arnhem | 6.17 | 31,478 | 32 | 3 | 3 | 202 | 20 | measured |
| 84 | Hawaii | 12.34 | - | 8 | - | 1 | - | 60 | measured |
| 85 | Kauai | 12.34 | - | 9 | 2 | 1 | - | 20 | measured |
| 86 | Las Vegas | 12.34 | - | 11 | 6 | 2 | - | 30 | measured |
| 87 | Trieste | 6.17 | 117,233 | 36 | 1 | 3 | 43 | 20 | measured |
| 88 | Madeira | 7.20 | - | 11 | 2 | 1 | - | 30 | measured |
| 89 | Zurich | 11.31 | 140,788 | 6 | 2 | - | - | 30 | measured |
| 90 | Hong Kong | 7.71 | 689,212 | 21 | 6 | 2 | 505 | 100 | measured |
| 91 | Sacramento | 11.32 | - | - | - | - | - | 30 | predicted (travel demand) |
| 92 | Bristol | 11.31 | 163,983 | 22 | 2 | 2 | - | 30 | measured |
| 93 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 60 | predicted (travel demand) |
| 94 | Dubai | 11.02 | 334,167 | - | - | - | - | 60 | predicted (travel demand) |
| 95 | Cork | 7.20 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 96 | Vilnius | 7.20 | 113,188 | 12 | 4 | 1 | 34 | 30 | measured |
| 97 | Budapest | 10.28 | 283,807 | 13 | 2 | 3 | - | 60 | measured |
| 98 | Indianapolis | 10.29 | - | 1 | 1 | - | - | 30 | measured |
| 99 | Catania | 6.17 | 58,252 | 4 | 3 | 1 | 5 | 30 | measured |
| 100 | Jersey City | 10.08 | - | - | - | - | - | 30 | predicted (travel demand) |
| 101 | Dallas | 10.29 | - | 12 | 2 | 1 | - | 60 | measured |
| 102 | Leiden | 5.14 | 33,227 | 19 | 6 | 1 | 129 | 20 | measured |
| 103 | Rotterdam | 5.14 | 104,938 | 17 | 1 | 2 | 83 | 30 | measured |
| 104 | Anchorage | 10.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 105 | Raleigh | 10.07 | - | - | - | - | - | 30 | predicted (travel demand) |
| 106 | Hamburg | 9.26 | 191,221 | 6 | 4 | 1 | - | 60 | measured |
| 107 | Cleveland | 9.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 108 | Ibiza | 6.17 | - | 1 | - | - | 4 | 20 | measured |
| 109 | Chicago | 8.23 | 485,769 | 46 | 2 | 5 | 9 | 60 | measured |
| 110 | El Paso | 9.70 | - | - | - | - | - | 30 | predicted (travel demand) |
| 111 | Osaka | 6.17 | 163,112 | 6 | 1 | - | - | 60 | measured |
| 112 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 113 | Edmonton | 9.38 | - | - | - | - | - | 60 | predicted (travel demand) |
| 114 | Nagoya | 6.17 | 83,437 | 6 | 2 | - | 1 | 60 | measured |
| 115 | Genoa | 5.14 | 145,206 | 13 | 2 | 1 | 10 | 30 | measured |
| 116 | Christchurch | 6.17 | 104,874 | 6 | 2 | 1 | 466 | 30 | measured |
| 117 | Gdansk | 6.17 | 4,908 | 12 | 5 | 1 | 307 | 30 | measured |
| 118 | Geneva | 6.17 | 162,269 | 21 | 6 | 4 | 131 | 20 | measured |
| 119 | Leipzig | 6.17 | 121,319 | 29 | 24 | 4 | - | 30 | measured |
| 120 | Melbourne | 6.17 | 267,898 | 16 | 1 | 2 | 403 | 100 | measured |
| 121 | Ottawa | 6.17 | - | 21 | - | 3 | 122 | 60 | measured |
| 122 | Vienna | 6.17 | 283,090 | 58 | 25 | 6 | 371 | 60 | measured |
| 123 | Winnipeg | 9.21 | - | - | - | - | - | 30 | predicted (travel demand) |
| 124 | Stockholm | 7.20 | 188,184 | 8 | 7 | - | - | 30 | measured |
| 125 | Tampere | 8.78 | - | - | - | - | - | 30 | predicted (travel demand) |
| 126 | Ann Arbor | 8.55 | - | - | - | - | - | 20 | predicted (travel demand) |
| 127 | Adelaide | 8.14 | 139,166 | - | - | - | - | 60 | predicted (travel demand) |
| 128 | Boise | 8.23 | - | 4 | - | 1 | - | 20 | measured |
| 129 | Utrecht | 4.11 | 67,963 | 30 | 9 | 2 | 339 | 30 | measured |
| 130 | Oslo | 7.20 | 181,113 | 4 | 3 | - | - | 30 | measured |
| 131 | Cordoba | 5.14 | 74,675 | 17 | 2 | 2 | 3 | 30 | measured |
| 132 | Graz | 5.14 | 65,717 | 17 | 10 | 2 | 87 | 30 | measured |
| 133 | Ghent | 7.20 | 82,757 | 8 | 2 | 1 | - | 30 | measured |
| 134 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 20 | predicted (travel demand) |
| 135 | Sydney | 7.20 | 305,304 | 7 | 1 | - | - | 100 | measured |
| 136 | Bergen | 7.30 | 82,940 | - | - | - | - | 30 | predicted (travel demand) |
| 137 | Belfast | 7.20 | 224,315 | 8 | 2 | 1 | - | 30 | measured |
| 138 | Istanbul | 6.17 | 333,027 | 14 | 4 | 1 | - | 100 | measured |
| 139 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 20 | predicted (travel demand) |
| 140 | Siena | 4.62 | 57,436 | - | - | - | - | 20 | predicted (travel demand) |
| 141 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 20 | predicted (travel demand) |
| 142 | Frankfurt | 4.51 | 150,379 | 28 | 11 | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 143 | Zagreb | 6.42 | 122,890 | - | - | - | - | 30 | predicted (travel demand) |
| 144 | Granada | 4.11 | 86,361 | 11 | 4 | 2 | 4 | 20 | measured |
| 145 | Bogota | 6.39 | 1,623 | - | - | - | - | 100 | predicted (travel demand) |
| 146 | Shanghai | 6.38 | 277,140 | - | - | - | - | 100 | predicted (travel demand) |
| 147 | Aarhus | 6.17 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 148 | Funchal | 3.77 | 174,351 | - | - | - | - | 20 | predicted (travel demand) |
| 149 | Alkmaar | 3.09 | - | 11 | - | 2 | 79 | 20 | measured |
| 150 | Breda | 3.09 | 36,579 | 11 | 1 | 2 | 120 | 20 | measured |
| 151 | Caserta | 3.09 | 14,783 | 24 | - | 1 | 51 | 20 | measured |
| 152 | Eindhoven | 3.09 | - | 17 | - | 3 | 195 | 20 | measured |
| 153 | Haarlem | 3.09 | 33,960 | 21 | 2 | 2 | 277 | 20 | measured |
| 154 | Sintra | 3.09 | 46,889 | 8 | 6 | 1 | 6 | 30 | measured |
| 155 | Trento | 3.09 | 56,455 | 10 | 2 | 1 | 20 | 20 | measured |
| 156 | Brno | 4.11 | 63,714 | 8 | 7 | 2 | 34 | 30 | measured |
| 157 | Cyprus | 6.17 | - | 15 | - | - | - | 60 | measured |
| 158 | Dresden | 4.11 | 113,624 | 32 | 25 | 1 | - | 30 | measured |
| 159 | Fort Worth | 6.17 | - | 24 | - | 2 | - | 30 | measured |
| 160 | Kansas City | 6.17 | - | 4 | - | 1 | - | 30 | measured |
| 161 | Tallinn | 4.11 | 124,888 | 9 | 3 | 2 | 42 | 30 | measured |
| 162 | York | 6.17 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 163 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 164 | Jacksonville | 5.69 | - | 2 | 2 | - | - | 30 | published, never ranked (may be uncrawled) |
| 165 | Avignon | 5.54 | 64,047 | - | - | - | - | 20 | predicted (travel demand) |
| 166 | Galway | 3.65 | 88,162 | - | - | - | - | 20 | predicted (travel demand) |
| 167 | Phuket | 5.46 | 5,487 | - | - | - | - | 30 | predicted (travel demand) |
| 168 | Rovaniemi | 5.38 | - | - | - | - | - | 20 | predicted (travel demand) |
| 169 | Ronda | 3.09 | 51,510 | 10 | 1 | - | 10 | 10 | measured |
| 170 | Lagos | 3.43 | 34,452 | - | - | - | - | 100 | predicted (travel demand) |
| 171 | Asheville | 5.22 | - | 4 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 172 | Beijing | 5.14 | 269,737 | 7 | 1 | - | - | 100 | measured |
| 173 | Bruges | 5.14 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 174 | Lund | 5.14 | - | - | - | - | - | 20 | predicted (travel demand) |
| 175 | Palma de Mallorca | 3.09 | 84,075 | 6 | 2 | 1 | 8 | 30 | measured |
| 176 | Kobe | 3.40 | 54,798 | - | - | - | - | 60 | predicted (travel demand) |
| 177 | Fort Lauderdale | 4.61 | - | 4 | - | - | 4 | 20 | published, never ranked (may be uncrawled) |
| 178 | Heraklion | 4.96 | 66,359 | - | - | - | - | 20 | predicted (travel demand) |
| 179 | Marseille | 4.96 | 182,033 | - | - | - | - | 30 | predicted (travel demand) |
| 180 | Mexico City | 4.63 | 566,583 | 9 | 2 | - | - | 100 | measured |
| 181 | Lexington | 4.56 | - | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 182 | Oakland | 4.70 | - | 4 | 1 | - | - | 30 | published, never ranked (may be uncrawled) |
| 183 | Stuttgart | 4.11 | 112,789 | 11 | 7 | - | - | 30 | measured |
| 184 | Bratislava | 3.09 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 185 | Salzburg | 3.09 | 107,243 | 21 | 12 | 3 | 33 | 20 | measured |
| 186 | Strasbourg | 3.09 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 187 | Basel | 4.59 | 105,838 | - | - | - | - | 20 | predicted (travel demand) |
| 188 | Key West | 3.95 | - | 2 | 1 | - | 7 | 10 | published, never ranked (may be uncrawled) |
| 189 | Tasmania | 4.41 | - | - | - | - | - | 30 | predicted (travel demand) |
| 190 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 20 | predicted (travel demand) |
| 191 | Freiburg | 4.11 | 92,752 | 8 | 4 | 1 | - | 20 | measured |
| 192 | Sofia | 2.81 | 138,710 | 4 | - | - | - | 60 | published, never ranked (may be uncrawled) |
| 193 | San Sebastian | 2.80 | 367 | - | - | - | - | 20 | predicted (travel demand) |
| 194 | Glasgow | 4.11 | 253,705 | 10 | 6 | - | - | 30 | measured |
| 195 | Chattanooga | 4.17 | - | 2 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 196 | Bergamo | 2.06 | 52,933 | 9 | 2 | 1 | 17 | 20 | measured |
| 197 | Enschede | 2.06 | - | 13 | 1 | 1 | 82 | 20 | measured |
| 198 | Groningen | 2.06 | 31,401 | 17 | - | 2 | 76 | 20 | measured |
| 199 | Helmond | 2.06 | - | 19 | - | 2 | 54 | 20 | measured |
| 200 | Nijmegen | 2.06 | 42,338 | 20 | 1 | 3 | 159 | 20 | measured |
| 201 | Sorrento | 2.06 | 40,049 | 7 | - | 1 | 20 | 10 | measured |
| 202 | Venlo | 2.06 | - | 7 | - | 1 | 144 | 20 | measured |
| 203 | Cologne | 4.11 | 191,812 | 5 | - | 1 | - | 60 | measured |
| 204 | Crete | 4.11 | - | 4 | 3 | - | - | 30 | measured |
| 205 | Houston | 4.11 | - | 12 | - | 1 | - | 60 | measured |
| 206 | Maui | 4.11 | - | 5 | 2 | - | - | 20 | measured |
| 207 | Savannah | 4.11 | 128,162 | 3 | 1 | - | - | 20 | measured |
| 208 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 30 | predicted (travel demand) |
| 209 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 210 | Guimaraes | 2.06 | 26,203 | 9 | 1 | 1 | 19 | 20 | measured |
| 211 | Helsinki | 3.09 | 148,908 | 12 | 3 | 1 | 13 | 30 | measured |
| 212 | Salt Lake City | 2.58 | - | 20 | - | 2 | 29 | 20 | published, never ranked (may be uncrawled) |
| 213 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 214 | Niagara Falls | 3.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 215 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 100 | predicted (travel demand) |
| 216 | Sao Paulo | 3.60 | 911 | 1 | - | - | - | 100 | measured |
| 217 | Parma | 2.06 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 218 | Wellington | 3.60 | 132,267 | - | - | - | - | 20 | predicted (travel demand) |
| 219 | Tarragona | 2.06 | 32,396 | 3 | 1 | - | - | 20 | measured |
| 220 | Tampa | 3.52 | - | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 221 | Girona | 2.06 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 222 | Montpellier | 3.47 | 64,238 | - | - | - | - | 30 | predicted (travel demand) |
| 223 | Verona | 2.06 | 77,646 | 8 | 4 | 1 | 3 | 30 | measured |
| 224 | Canberra | 2.28 | - | 8 | 1 | 1 | 132 | 30 | published, never ranked (may be uncrawled) |
| 225 | Cape Town | 3.29 | 199,169 | - | - | - | - | 60 | predicted (travel demand) |
| 226 | Rhodes | 3.42 | 127,205 | - | - | - | - | 20 | predicted (travel demand) |
| 227 | San Antonio | 3.32 | - | 5 | 1 | 1 | - | 60 | published, never ranked (may be uncrawled) |
| 228 | Chania | 3.30 | 47,379 | - | - | - | - | 20 | predicted (travel demand) |
| 229 | Santiago | 3.25 | 111,647 | - | - | - | - | 100 | predicted (travel demand) |
| 230 | Tulsa | 3.01 | - | 1 | - | - | 3 | 30 | published, never ranked (may be uncrawled) |
| 231 | Busan | 3.09 | 94,737 | 2 | - | - | - | 60 | measured |
| 232 | Oxford | 3.09 | 111,583 | 7 | 1 | 1 | - | 20 | measured |
| 233 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 30 | predicted (travel demand) |
| 234 | Vancouver | 3.09 | 351,552 | 7 | - | - | - | 30 | measured |
| 235 | Lucerne | 3.10 | 66,356 | - | - | - | - | 20 | predicted (travel demand) |
| 236 | Belgrade | 3.09 | 178,116 | 5 | 5 | - | - | 60 | measured |
| 237 | Bilbao | 2.06 | 133,133 | 4 | 1 | 1 | - | 30 | measured |
| 238 | Bordeaux | 2.06 | 156,201 | 10 | - | 2 | 211 | 30 | measured |
| 239 | Brighton | 3.09 | 114,108 | 6 | 3 | 1 | - | 20 | measured |
| 240 | Hobart | 2.06 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 241 | Nice | 3.09 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 242 | Potsdam | 2.06 | 51,727 | 18 | 8 | 3 | 16 | 20 | measured |
| 243 | Warsaw | 2.06 | 197,929 | 39 | 20 | 4 | 1407 | 60 | measured |
| 244 | Miami | 2.37 | 278,558 | 11 | 1 | - | 15 | 30 | published, never ranked (may be uncrawled) |
| 245 | Malmo | 3.07 | 103,940 | - | - | - | - | 30 | predicted (travel demand) |
| 246 | Lille | 3.06 | 73,435 | - | - | - | - | 20 | predicted (travel demand) |
| 247 | Corsica | 3.00 | - | - | - | - | - | 30 | predicted (travel demand) |
| 248 | Mechelen | 2.93 | 20,707 | - | - | - | - | 20 | predicted (travel demand) |
| 249 | Turin | 1.49 | 147,456 | 11 | 10 | 2 | 30 | 30 | published, never ranked (may be uncrawled) |
| 250 | Chiang Mai | 2.85 | 66,541 | 1 | - | - | 2 | 60 | published, never ranked (may be uncrawled) |
| 251 | Denver | 2.91 | - | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 252 | San Jose | 2.85 | - | 2 | - | - | - | 60 | published, never ranked (may be uncrawled) |
| 253 | Spokane | 2.06 | - | 18 | - | 2 | 18 | 20 | measured |
| 254 | Poznan | 1.89 | 65,666 | 10 | - | 1 | 397 | 30 | published, never ranked (may be uncrawled) |
| 255 | Milwaukee | 2.66 | - | 6 | - | 1 | 2 | 30 | published, never ranked (may be uncrawled) |
| 256 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 257 | Syracuse | 1.75 | 102,833 | - | - | - | - | 20 | predicted (travel demand) |
| 258 | Cartagena | 2.58 | 65,066 | - | - | - | - | 30 | predicted (travel demand) |
| 259 | Atlanta | 2.57 | - | 11 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 260 | Bern | 2.51 | 90,627 | - | - | - | - | 20 | predicted (travel demand) |
| 261 | Bali | 2.49 | - | 5 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 262 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 263 | Faro | 1.62 | 55,645 | - | - | - | - | 20 | predicted (travel demand) |
| 264 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 265 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 266 | Cusco | 2.35 | 87,732 | - | - | - | - | 30 | predicted (travel demand) |
| 267 | Limerick | 1.57 | 90,379 | - | - | - | - | 20 | predicted (travel demand) |
| 268 | Trier | 1.56 | 69,369 | - | - | - | 154 | 20 | predicted (travel demand) |
| 269 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 20 | predicted (travel demand) |
| 270 | Pisa | 1.46 | 52,174 | 4 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 271 | Nashville | 2.23 | - | 8 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 272 | Hanoi | 2.15 | 117,396 | 2 | - | - | - | 100 | published, never ranked (may be uncrawled) |
| 273 | Pittsburgh | 2.06 | - | 12 | - | 1 | - | 30 | measured |
| 274 | Taipei | 2.09 | 143,193 | 4 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 275 | Salamanca | 1.37 | 47,897 | 4 | 1 | 1 | 1 | 20 | published, never ranked (may be uncrawled) |
| 276 | Apeldoorn | 1.03 | - | 8 | - | 2 | 80 | 20 | measured |
| 277 | Bucharest | 2.06 | 136,836 | 4 | - | 1 | - | 60 | measured |
| 278 | Delft | 1.03 | 31,293 | 12 | - | 1 | 60 | 20 | measured |
| 279 | Deventer | 1.03 | - | 12 | - | 1 | 213 | 20 | measured |
| 280 | Dordrecht | 1.03 | - | 17 | 1 | 2 | 105 | 20 | measured |
| 281 | Hilo | 2.06 | - | 9 | - | 2 | - | 10 | measured |
| 282 | Hilversum | 1.03 | - | 6 | 1 | 1 | 122 | 20 | measured |
| 283 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 284 | Leuven | 2.06 | 40,645 | 4 | - | - | - | 20 | measured |
| 285 | Lucca | 1.03 | 52,271 | 16 | 4 | 1 | 27 | 20 | measured |
| 286 | Maastricht | 1.03 | 47,763 | 16 | - | 2 | 135 | 20 | measured |
| 287 | Roosendaal | 1.03 | - | 20 | - | 2 | 138 | 20 | measured |
| 288 | Tilburg | 1.03 | - | 17 | - | 3 | 86 | 20 | published, never ranked (may be uncrawled) |
| 289 | Ischia | 1.32 | - | - | - | - | 2 | 20 | predicted (travel demand) |
| 290 | Albuquerque | 1.96 | - | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 291 | Izmir | 1.88 | 69,826 | - | - | - | - | 60 | predicted (travel demand) |
| 292 | Perugia | 1.03 | 42,572 | 16 | 1 | 2 | 19 | 20 | measured |
| 293 | Como | 0.96 | 82,645 | 9 | 3 | 1 | 23 | 20 | published, never ranked (may be uncrawled) |
| 294 | Padua | 1.03 | 54,592 | 14 | 8 | 1 | 12 | 20 | measured |
| 295 | Buenos Aires | 1.83 | 333,331 | 4 | 2 | - | - | 60 | published, never ranked (may be uncrawled) |
| 296 | Minneapolis | 1.88 | - | 4 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 297 | Setubal | 1.03 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 298 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 299 | Baltimore | 1.77 | - | 4 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 300 | Ferrara | 1.03 | 27,490 | 5 | 3 | 1 | 7 | 20 | measured |
| 301 | Auckland | 1.17 | 152,056 | 5 | 2 | - | 977 | 60 | published, never ranked (may be uncrawled) |
| 302 | Bari | 1.03 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 303 | Matera | 1.03 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 304 | Pamplona | 1.03 | 128,065 | 25 | - | 3 | 9 | 20 | measured |
| 305 | Dijon | 1.72 | 43,526 | - | - | - | - | 20 | predicted (travel demand) |
| 306 | Annecy | 1.69 | 56,859 | - | - | - | - | 20 | predicted (travel demand) |
| 307 | Bangkok | 1.54 | 222,206 | 6 | 1 | 1 | 5 | 100 | measured |
| 308 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 309 | Yakushima | 1.03 | - | 2 | 2 | - | 1 | 10 | measured |
| 310 | Liverpool | 1.61 | 248,189 | 3 | 3 | - | - | 30 | published, never ranked (may be uncrawled) |
| 311 | Mostar | 1.58 | 63,907 | - | - | - | - | 20 | predicted (travel demand) |
| 312 | Lyon | 1.03 | 136,951 | 34 | 4 | 6 | 178 | 30 | measured |
| 313 | Nuremberg | 1.03 | 161,614 | 20 | 8 | 2 | 37 | 30 | measured |
| 314 | Quebec City | 1.03 | 124,358 | 6 | - | 1 | 494 | 30 | measured |
| 315 | Toulouse | 1.03 | 112,721 | 10 | - | 1 | 34 | 30 | measured |
| 316 | Wroclaw | 1.03 | 123,894 | 5 | 2 | 1 | 121 | 30 | measured |
| 317 | Gothenburg | 1.49 | 119,991 | 5 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 318 | Malta | 1.45 | - | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 319 | Antalya | 1.31 | 70,688 | - | - | - | - | 60 | predicted (travel demand) |
| 320 | Cardiff | 1.27 | - | 12 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 321 | Santa Fe | 1.29 | - | 3 | - | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 322 | Colmar | 1.28 | 45,517 | - | - | - | - | 20 | predicted (travel demand) |
| 323 | Bodrum | 1.26 | 33,918 | - | - | - | - | 20 | predicted (travel demand) |
| 324 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 325 | Rothenburg ob der Tauber | 1.03 | 39,879 | 5 | 1 | 1 | 8 | 10 | measured |
| 326 | Lausanne | 1.23 | 68,242 | 8 | 1 | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 327 | Evora | 0.78 | 15,345 | - | - | - | - | 20 | predicted (travel demand) |
| 328 | Heidelberg | 1.03 | 75,837 | 7 | 1 | 1 | - | 20 | measured |
| 329 | Braga | 0.62 | 34,522 | 4 | 2 | - | 8 | 20 | published, never ranked (may be uncrawled) |
| 330 | Menorca | 0.73 | - | 6 | - | - | 2 | 20 | published, never ranked (may be uncrawled) |
| 331 | Zaragoza | 0.73 | 87,580 | 7 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 332 | Okinawa | 0.71 | 24,466 | 6 | - | - | 1 | 30 | published, never ranked (may be uncrawled) |
| 333 | Dubrovnik | 0.99 | 119,586 | 4 | 4 | - | 2 | 10 | published, never ranked (may be uncrawled) |
| 334 | Ljubljana | 1.03 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 335 | Riga | 1.03 | 108,918 | 5 | 2 | - | - | 30 | measured |
| 336 | Manchester | 1.03 | 316,438 | 5 | 1 | - | - | 30 | measured |
| 337 | Thessaloniki | 1.03 | 180,145 | 4 | - | 1 | - | 30 | measured |
| 338 | Turku | 1.03 | - | 1 | 1 | - | - | 20 | measured |
| 339 | Split | 0.97 | 132,399 | 5 | - | 1 | 2 | 20 | published, never ranked (may be uncrawled) |
| 340 | Azores | 0.65 | - | 7 | 2 | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 341 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 60 | predicted (travel demand) |
| 342 | Nantes | 0.96 | 67,689 | 1 | 1 | - | - | 30 | published, never ranked (may be uncrawled) |
| 343 | Innsbruck | 0.63 | 58,742 | 6 | 2 | 1 | 39 | 20 | published, never ranked (may be uncrawled) |
| 344 | Kotor | 0.86 | 48,982 | 1 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 345 | Kandy | 0.78 | 24,159 | 1 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 346 | Modena | 0.44 | 51,698 | 5 | 1 | 1 | 3 | 20 | published, never ranked (may be uncrawled) |
| 347 | Den Bosch | 0.36 | 39,682 | 11 | 2 | 1 | 118 | 20 | published, never ranked (may be uncrawled) |
| 348 | Assen | 0.35 | - | 9 | - | 2 | 66 | 20 | published, never ranked (may be uncrawled) |
| 349 | Heerlen | 0.35 | - | 8 | 1 | 2 | 53 | 20 | published, never ranked (may be uncrawled) |
| 350 | Kamakura | 0.44 | 33,492 | 6 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 351 | Zwolle | 0.35 | - | 15 | - | 3 | 58 | 20 | published, never ranked (may be uncrawled) |
| 352 | Inverness | 0.69 | 92,195 | 1 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 353 | Corfu | 0.68 | 139,334 | 8 | - | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 354 | Gran Canaria | 0.42 | - | 10 | 4 | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 355 | Hallstatt | 0.50 | 47,271 | 7 | 4 | - | - | 10 | published, never ranked (may be uncrawled) |
| 356 | Hoorn | 0.30 | - | 12 | - | 2 | 52 | 20 | published, never ranked (may be uncrawled) |
| 357 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 100 | published, never ranked (may be uncrawled) |
| 358 | Rouen | 0.54 | 72,334 | 12 | - | 1 | 6 | 20 | published, never ranked (may be uncrawled) |
| 359 | Phoenix | 0.55 | - | - | - | - | - | 60 | predicted (travel demand) |
| 360 | Cesky Krumlov | 0.34 | 28,582 | 6 | 3 | - | 11 | 10 | published, never ranked (may be uncrawled) |
| 361 | Rio de Janeiro | 0.51 | 279,431 | 6 | - | - | - | 100 | measured |
| 362 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 363 | Killarney | 0.30 | 28,763 | 1 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 364 | Canterbury | 0.40 | 53,301 | 4 | 1 | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 365 | Zadar | 0.38 | 71,549 | 1 | - | - | 1 | 20 | published, never ranked (may be uncrawled) |
| 366 | Toledo | 0.24 | 3,149 | - | - | - | - | 20 | predicted (travel demand) |
| 367 | Anuradhapura | 0.32 | - | 1 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 368 | Regensburg | 0.30 | 51,930 | 8 | 2 | 1 | 3 | 20 | published, never ranked (may be uncrawled) |
| 369 | Bamberg | 0.24 | 28,716 | 9 | 7 | 1 | 12 | 20 | published, never ranked (may be uncrawled) |
| 370 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 371 | Assisi | 0.17 | 30,278 | 6 | 1 | 2 | 6 | 10 | published, never ranked (may be uncrawled) |
| 372 | Stratford-upon-Avon | 0.27 | 68,555 | 2 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 373 | La Palma | 0.17 | - | 4 | 3 | - | - | 20 | published, never ranked (may be uncrawled) |
| 374 | Allentown | 0.24 | - | - | - | - | - | 20 | predicted (travel demand) |
| 375 | Oss | 0.11 | - | 5 | - | - | 48 | 20 | published, never ranked (may be uncrawled) |
| 376 | Queenstown | 0.16 | 36,672 | - | - | - | - | 10 | predicted (travel demand) |
| 377 | Buffalo | 0.15 | - | - | - | - | - | 10 | predicted (travel demand) |
| 378 | San Juan | 0.15 | - | - | - | - | - | 10 | predicted (travel demand) |
| 379 | Halifax | 0.08 | - | - | - | - | - | 30 | predicted (travel demand) |
| 380 | Memphis | 0.08 | - | - | - | - | - | 30 | predicted (travel demand) |
| 381 | George Town | 0.07 | 36,080 | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |

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

