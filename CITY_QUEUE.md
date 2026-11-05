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
| 1 | Palermo | 67.45 | 124,310 | 22 | 11 | 2 | 37 | 30 | measured |
| 2 | Seville | 84.31 | 170,545 | 44 | 12 | 2 | - | 30 | measured |
| 3 | Tokyo | 71.06 | 394,702 | 22 | 16 | 1 | 5 | 100 | measured |
| 4 | Lisbon | 63.83 | 201,877 | 37 | 21 | 3 | 67 | 30 | measured |
| 5 | New York | 69.86 | 1,124,326 | 29 | 10 | 2 | - | 100 | measured |
| 6 | Tenerife | 63.83 | - | 4 | 4 | - | - | 30 | measured |
| 7 | Berlin | 63.83 | 412,181 | 63 | 51 | 5 | 195 | 60 | measured |
| 8 | Singapore | 61.43 | 967,821 | 34 | 7 | 3 | 165 | 100 | measured |
| 9 | Fukuoka | 38.54 | 77,485 | 18 | 11 | 1 | - | 60 | measured |
| 10 | Munich | 36.13 | 224,067 | 63 | 35 | 8 | 74 | 60 | measured |
| 11 | Alicante | 25.29 | 77,454 | 21 | 4 | 2 | 44 | 30 | measured |
| 12 | Copenhagen | 46.97 | 218,621 | 49 | 41 | 6 | - | 30 | measured |
| 13 | Paris | 32.52 | 524,268 | 58 | 15 | 8 | 129 | 60 | measured |
| 14 | Malaga | 31.32 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 15 | Porto | 22.88 | 120,415 | 29 | 16 | 2 | 42 | 30 | measured |
| 16 | Brisbane | 30.11 | 162,602 | 20 | 5 | 2 | 186 | 60 | measured |
| 17 | San Francisco | 28.91 | 361,111 | 12 | 3 | 1 | 26 | 30 | measured |
| 18 | Rome | 21.68 | 358,876 | 31 | 10 | 2 | 32 | 60 | measured |
| 19 | Kyoto | 27.70 | 142,353 | 18 | 14 | 2 | - | 60 | measured |
| 20 | London | 36.13 | 718,291 | 32 | 25 | 1 | - | 100 | measured |
| 21 | Amsterdam | 19.27 | 294,030 | 27 | 7 | 2 | 5488 | 30 | measured |
| 22 | Coimbra | 20.48 | 34,962 | 6 | - | - | 5 | 20 | measured |
| 23 | Birmingham | 37.53 | - | - | - | - | - | 60 | predicted (travel demand) |
| 24 | Monterey | 36.13 | - | 3 | 2 | - | - | 10 | measured |
| 25 | Dublin | 20.48 | 240,850 | 19 | 4 | 2 | 12 | 30 | measured |
| 26 | Boston | 33.72 | 385,902 | 13 | 3 | 2 | - | 30 | measured |
| 27 | Austin | 33.72 | 226,631 | 10 | 4 | 1 | - | 30 | measured |
| 28 | Cambridge | 28.91 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 29 | Luxembourg City | 19.27 | 64,851 | 10 | 8 | 2 | 18 | 20 | measured |
| 30 | Madrid | 16.86 | 274,553 | 18 | 11 | 2 | - | 60 | measured |
| 31 | The Hague | 13.25 | 236,723 | 26 | 4 | 5 | 166 | 30 | measured |
| 32 | Venice | 14.45 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 33 | Oahu | 24.09 | - | 21 | 8 | 3 | - | 30 | measured |
| 34 | Jacksonville | 22.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 35 | Bath | 21.68 | 144,950 | 5 | 2 | 1 | - | 20 | measured |
| 36 | Portland | 14.45 | 217,222 | 33 | 2 | 3 | 306 | 30 | measured |
| 37 | Asheville | 20.89 | - | - | - | - | - | 20 | predicted (travel demand) |
| 38 | Long Beach | 20.48 | - | - | - | - | - | 30 | predicted (travel demand) |
| 39 | Little Rock | 20.40 | - | - | - | - | - | 20 | predicted (travel demand) |
| 40 | Bologna | 10.84 | 146,161 | 12 | 7 | 1 | 9 | 30 | measured |
| 41 | Amersfoort | 9.64 | - | 21 | 1 | 2 | 181 | 20 | measured |
| 42 | Montreal | 19.27 | 315,322 | 14 | 2 | 2 | - | 60 | measured |
| 43 | Oakland | 18.81 | - | - | - | - | - | 30 | predicted (travel demand) |
| 44 | Kanazawa | 12.04 | 25,778 | 7 | 3 | 1 | 2 | 30 | measured |
| 45 | Edinburgh | 18.07 | 292,981 | 21 | 10 | 1 | - | 30 | measured |
| 46 | Perth | 18.07 | 180,478 | 6 | 4 | 1 | - | 60 | measured |
| 47 | Lexington | 18.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 48 | Reno | 18.19 | - | - | - | - | - | 30 | predicted (travel demand) |
| 49 | Des Moines | 18.11 | - | - | - | - | - | 20 | predicted (travel demand) |
| 50 | Krakow | 12.04 | 140,824 | 38 | 11 | 3 | 198 | 30 | measured |
| 51 | Daytona Beach | 17.66 | - | - | - | - | - | 20 | predicted (travel demand) |
| 52 | Philadelphia | 16.86 | 405,294 | 4 | 1 | - | - | 60 | measured |
| 53 | Seattle | 16.86 | 398,724 | 30 | 3 | 4 | - | 30 | measured |
| 54 | Athens | 16.86 | 235,429 | 12 | 7 | 2 | - | 30 | measured |
| 55 | Seoul | 15.66 | 206,265 | 8 | 5 | 1 | - | 100 | measured |
| 56 | Arnhem | 8.43 | 31,478 | 32 | 3 | 3 | 202 | 20 | measured |
| 57 | Barcelona | 8.43 | 346,477 | 58 | 20 | 7 | 177 | 60 | measured |
| 58 | Florence | 8.43 | 184,099 | 27 | 9 | 1 | 27 | 30 | measured |
| 59 | Leeuwarden | 8.43 | - | 34 | - | 2 | 61 | 20 | measured |
| 60 | Milan | 8.43 | 212,705 | 30 | 14 | 3 | 25 | 60 | measured |
| 61 | Chattanooga | 16.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 62 | Prague | 10.84 | 303,350 | 30 | 21 | 4 | 31 | 60 | measured |
| 63 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 64 | Toronto | 15.66 | 411,011 | 6 | - | - | - | 60 | measured |
| 65 | Washington DC | 12.04 | 606,731 | 33 | 8 | 4 | - | 30 | measured |
| 66 | Huntsville | 15.35 | - | - | - | - | - | 20 | predicted (travel demand) |
| 67 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 68 | West Palm Beach | 14.98 | - | - | - | - | - | 20 | predicted (travel demand) |
| 69 | Saint Petersburg | 14.83 | - | - | - | - | - | 100 | predicted (travel demand) |
| 70 | St. Louis | 14.80 | - | - | - | - | - | 30 | predicted (travel demand) |
| 71 | Charleston | 14.45 | 155,987 | 3 | 1 | - | - | 20 | measured |
| 72 | Hiroshima | 9.64 | 129,791 | 33 | 5 | 2 | - | 60 | measured |
| 73 | Naples | 7.23 | 198,913 | 24 | 5 | 3 | 46 | 30 | measured |
| 74 | Sapporo | 9.64 | 88,633 | 6 | 1 | - | - | 60 | measured |
| 75 | Trieste | 7.23 | 117,233 | 36 | 1 | 3 | 43 | 20 | measured |
| 76 | Kauai | 14.45 | - | 6 | 1 | - | - | 20 | measured |
| 77 | San Diego | 14.45 | 214,939 | 6 | 1 | 1 | - | 60 | measured |
| 78 | Tampa | 14.10 | - | - | - | - | - | 30 | predicted (travel demand) |
| 79 | Madeira | 8.43 | - | 11 | 2 | 1 | - | 30 | measured |
| 80 | Reykjavik | 12.04 | 166,789 | 4 | 3 | 1 | - | 20 | measured |
| 81 | Cincinnati | 13.33 | - | - | - | - | - | 30 | predicted (travel demand) |
| 82 | Sardinia | 7.23 | - | 7 | 6 | - | 10 | 60 | measured |
| 83 | Lansing | 13.02 | - | - | - | - | - | 20 | predicted (travel demand) |
| 84 | Cork | 8.43 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 85 | Hong Kong | 8.43 | 689,212 | 21 | 6 | 2 | 505 | 100 | measured |
| 86 | Detroit | 12.53 | - | - | - | - | - | 30 | predicted (travel demand) |
| 87 | Catania | 7.23 | 58,252 | 4 | 3 | 1 | 5 | 30 | measured |
| 88 | Los Angeles | 12.04 | 665,559 | 11 | 3 | - | - | 60 | measured |
| 89 | Hawaii | 12.04 | - | 6 | - | 1 | - | 60 | measured |
| 90 | Las Vegas | 12.04 | - | 11 | 6 | 2 | - | 30 | measured |
| 91 | New Orleans | 12.04 | 256,232 | 8 | 6 | 1 | - | 30 | measured |
| 92 | Stockholm | 9.64 | 188,184 | 8 | 7 | - | - | 30 | measured |
| 93 | Chiang Mai | 11.42 | 66,541 | - | - | - | 2 | 60 | predicted (travel demand) |
| 94 | Denver | 11.66 | - | - | - | - | - | 30 | predicted (travel demand) |
| 95 | San Jose | 11.39 | - | - | - | - | - | 60 | predicted (travel demand) |
| 96 | Chicago | 9.64 | 485,769 | 38 | 2 | 3 | 9 | 60 | measured |
| 97 | Sacramento | 11.32 | - | - | - | - | - | 30 | predicted (travel demand) |
| 98 | Cadiz | 7.23 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 99 | Budapest | 10.84 | 283,807 | 13 | 2 | 3 | - | 60 | measured |
| 100 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 60 | predicted (travel demand) |
| 101 | Cagliari | 6.02 | 51,351 | 14 | 1 | 2 | 14 | 20 | measured |
| 102 | Dubai | 11.02 | 334,167 | - | - | - | - | 60 | predicted (travel demand) |
| 103 | Nagoya | 7.23 | 83,437 | 6 | 2 | - | 1 | 60 | measured |
| 104 | Brussels | 7.23 | 176,863 | 35 | 4 | 2 | 436 | 60 | measured |
| 105 | Gdansk | 7.23 | 4,908 | 12 | 5 | 1 | 307 | 30 | measured |
| 106 | Leipzig | 7.23 | 121,319 | 29 | 24 | 4 | - | 30 | measured |
| 107 | Melbourne | 7.23 | 267,898 | 16 | 1 | 2 | 403 | 100 | measured |
| 108 | Antwerp | 10.84 | 128,289 | 10 | 4 | 1 | - | 30 | measured |
| 109 | Milwaukee | 10.63 | - | - | - | - | - | 30 | predicted (travel demand) |
| 110 | Jersey City | 10.08 | - | - | - | - | - | 30 | predicted (travel demand) |
| 111 | Atlanta | 10.29 | - | - | - | - | - | 30 | predicted (travel demand) |
| 112 | Anchorage | 10.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 113 | Raleigh | 10.07 | - | - | - | - | - | 30 | predicted (travel demand) |
| 114 | Cleveland | 9.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 115 | El Paso | 9.70 | - | - | - | - | - | 30 | predicted (travel demand) |
| 116 | Boise | 9.64 | - | 4 | - | 1 | - | 20 | measured |
| 117 | Rotterdam | 4.82 | 104,938 | 17 | 1 | 2 | 83 | 30 | measured |
| 118 | Utrecht | 4.82 | 67,963 | 30 | 9 | 2 | 339 | 30 | measured |
| 119 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 120 | Ibiza | 6.02 | - | 1 | - | - | 4 | 20 | measured |
| 121 | Osaka | 6.02 | 163,112 | 6 | 1 | - | - | 60 | measured |
| 122 | Edmonton | 9.38 | - | - | - | - | - | 60 | predicted (travel demand) |
| 123 | Winnipeg | 9.21 | - | - | - | - | - | 30 | predicted (travel demand) |
| 124 | Christchurch | 6.02 | 104,874 | 6 | 2 | 1 | 466 | 30 | measured |
| 125 | Geneva | 6.02 | 162,269 | 21 | 6 | 4 | 131 | 20 | measured |
| 126 | Vilnius | 6.02 | 113,188 | 12 | 4 | 1 | 34 | 30 | measured |
| 127 | Hamburg | 8.43 | 191,221 | 6 | 4 | 1 | - | 60 | measured |
| 128 | Nashville | 8.93 | - | - | - | - | - | 30 | predicted (travel demand) |
| 129 | Tampere | 8.78 | - | - | - | - | - | 30 | predicted (travel demand) |
| 130 | Genoa | 4.82 | 145,206 | 13 | 2 | 1 | 10 | 30 | measured |
| 131 | Ghent | 8.43 | 82,757 | 8 | 2 | 1 | - | 30 | measured |
| 132 | Sydney | 8.43 | 305,304 | 7 | 1 | - | - | 100 | measured |
| 133 | Ann Arbor | 8.55 | - | - | - | - | - | 20 | predicted (travel demand) |
| 134 | Belfast | 8.43 | 224,315 | 5 | 2 | 1 | - | 30 | measured |
| 135 | Adelaide | 8.14 | 139,166 | - | - | - | - | 60 | predicted (travel demand) |
| 136 | Istanbul | 7.23 | 333,027 | 14 | 4 | 1 | - | 100 | measured |
| 137 | Oslo | 7.23 | 181,113 | 4 | 3 | - | - | 30 | measured |
| 138 | Albuquerque | 7.83 | - | - | - | - | - | 30 | predicted (travel demand) |
| 139 | Cordoba | 4.82 | 74,675 | 16 | 2 | 2 | 3 | 30 | measured |
| 140 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 20 | predicted (travel demand) |
| 141 | Aarhus | 7.23 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 142 | Bergen | 7.30 | 82,940 | - | - | - | - | 30 | predicted (travel demand) |
| 143 | Brno | 4.82 | 63,714 | 8 | 7 | 2 | 34 | 30 | measured |
| 144 | Dallas | 7.23 | - | 12 | 2 | 1 | - | 60 | measured |
| 145 | Dresden | 4.82 | 113,624 | 32 | 25 | 1 | - | 30 | measured |
| 146 | Strasbourg | 4.82 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 147 | Vienna | 4.82 | 283,090 | 58 | 25 | 6 | 371 | 60 | measured |
| 148 | York | 7.23 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 149 | Alkmaar | 3.61 | - | 11 | - | 2 | 79 | 20 | measured |
| 150 | Breda | 3.61 | 36,579 | 11 | 1 | 2 | 120 | 20 | measured |
| 151 | Caserta | 3.61 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 152 | Eindhoven | 3.61 | - | 17 | - | 3 | 195 | 20 | measured |
| 153 | Haarlem | 3.61 | 33,960 | 21 | 2 | 2 | 277 | 20 | measured |
| 154 | Valencia | 3.61 | 162,209 | 31 | 4 | 2 | 350 | 30 | measured |
| 155 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 20 | predicted (travel demand) |
| 156 | Siena | 4.62 | 57,436 | - | - | - | - | 20 | predicted (travel demand) |
| 157 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 20 | predicted (travel demand) |
| 158 | Frankfurt | 4.51 | 150,379 | 28 | 11 | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 159 | Spokane | 4.82 | - | 14 | - | 2 | 18 | 20 | measured |
| 160 | Zagreb | 6.42 | 122,890 | - | - | - | - | 30 | predicted (travel demand) |
| 161 | Bogota | 6.39 | 1,623 | - | - | - | - | 100 | predicted (travel demand) |
| 162 | Shanghai | 6.38 | 277,140 | - | - | - | - | 100 | predicted (travel demand) |
| 163 | Funchal | 3.77 | 174,351 | - | - | - | - | 20 | predicted (travel demand) |
| 164 | Zurich | 6.02 | 140,788 | 6 | 2 | - | - | 30 | measured |
| 165 | Cyprus | 6.02 | - | 4 | - | - | - | 60 | measured |
| 166 | Ronda | 3.61 | 51,510 | 6 | 1 | - | 9 | 10 | measured |
| 167 | Palma de Mallorca | 3.61 | 84,075 | 6 | 2 | 1 | 8 | 30 | measured |
| 168 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 169 | Avignon | 5.54 | 64,047 | - | - | - | - | 20 | predicted (travel demand) |
| 170 | Galway | 3.65 | 88,162 | - | - | - | - | 20 | predicted (travel demand) |
| 171 | Phuket | 5.46 | 5,487 | - | - | - | - | 30 | predicted (travel demand) |
| 172 | Beijing | 5.42 | 269,737 | 7 | 1 | - | - | 100 | measured |
| 173 | Bratislava | 3.61 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 174 | Graz | 3.61 | 65,717 | 17 | 10 | 2 | 87 | 30 | measured |
| 175 | Ottawa | 3.61 | - | 21 | - | 3 | 122 | 60 | measured |
| 176 | Salzburg | 3.61 | 107,243 | 21 | 12 | 3 | 33 | 20 | measured |
| 177 | Rovaniemi | 5.38 | - | - | - | - | - | 20 | predicted (travel demand) |
| 178 | Lagos | 3.43 | 34,452 | - | - | - | - | 100 | predicted (travel demand) |
| 179 | Santa Fe | 5.17 | - | - | - | - | - | 20 | predicted (travel demand) |
| 180 | Lund | 5.14 | - | - | - | - | - | 20 | predicted (travel demand) |
| 181 | Mexico City | 4.82 | 566,583 | 9 | 2 | - | - | 100 | measured |
| 182 | Kobe | 3.40 | 54,798 | - | - | - | - | 60 | predicted (travel demand) |
| 183 | Fort Lauderdale | 4.61 | - | 4 | - | - | 4 | 20 | published, never ranked (may be uncrawled) |
| 184 | Heraklion | 4.96 | 66,359 | - | - | - | - | 20 | predicted (travel demand) |
| 185 | Marseille | 4.96 | 182,033 | - | - | - | - | 30 | predicted (travel demand) |
| 186 | Indianapolis | 4.82 | - | 1 | 1 | - | - | 30 | measured |
| 187 | Bergamo | 2.41 | 52,933 | 9 | 2 | 1 | 17 | 20 | measured |
| 188 | Bristol | 4.82 | 163,983 | 12 | 2 | 1 | - | 30 | measured |
| 189 | Dordrecht | 2.41 | - | 17 | 1 | 2 | 105 | 20 | measured |
| 190 | Enschede | 2.41 | - | 13 | 1 | 1 | 82 | 20 | measured |
| 191 | Fort Worth | 4.82 | - | 22 | - | 1 | - | 30 | measured |
| 192 | Groningen | 2.41 | 31,401 | 17 | - | 2 | 76 | 20 | measured |
| 193 | Kansas City | 4.82 | - | 4 | - | 1 | - | 30 | measured |
| 194 | Leiden | 2.41 | 33,227 | 19 | 6 | 1 | 129 | 20 | measured |
| 195 | Savannah | 4.82 | 128,162 | 3 | 1 | - | - | 20 | measured |
| 196 | Sintra | 2.41 | 46,889 | 7 | 6 | 1 | 6 | 30 | measured |
| 197 | Sorrento | 2.41 | 40,049 | 7 | - | 1 | 20 | 10 | measured |
| 198 | Trento | 2.41 | 56,455 | 10 | 2 | 1 | 20 | 20 | measured |
| 199 | Venlo | 2.41 | - | 7 | - | 1 | 144 | 20 | measured |
| 200 | Basel | 4.59 | 105,838 | - | - | - | - | 20 | predicted (travel demand) |
| 201 | Key West | 3.95 | - | 2 | 1 | - | 7 | 10 | published, never ranked (may be uncrawled) |
| 202 | Tasmania | 4.41 | - | - | - | - | - | 30 | predicted (travel demand) |
| 203 | Parma | 2.41 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 204 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 20 | predicted (travel demand) |
| 205 | Sofia | 2.81 | 138,710 | 4 | - | - | - | 60 | published, never ranked (may be uncrawled) |
| 206 | San Sebastian | 2.80 | 367 | - | - | - | - | 20 | predicted (travel demand) |
| 207 | Tarragona | 2.41 | 32,396 | 3 | 1 | - | - | 20 | measured |
| 208 | Stuttgart | 3.61 | 112,789 | 11 | 7 | - | - | 30 | measured |
| 209 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 30 | predicted (travel demand) |
| 210 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 211 | Pittsburgh | 3.80 | - | 12 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 212 | Salt Lake City | 2.58 | - | 6 | - | 1 | 31 | 20 | published, never ranked (may be uncrawled) |
| 213 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 214 | Niagara Falls | 3.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 215 | Granada | 2.41 | 86,361 | 9 | 4 | 2 | 4 | 20 | measured |
| 216 | Yakushima | 2.41 | - | 2 | 2 | - | 1 | 10 | measured |
| 217 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 100 | predicted (travel demand) |
| 218 | Freiburg | 3.61 | 92,752 | 8 | 4 | 1 | - | 20 | measured |
| 219 | Sao Paulo | 3.61 | 911 | 1 | - | - | - | 100 | measured |
| 220 | Busan | 3.61 | 94,737 | 2 | - | - | - | 60 | measured |
| 221 | Wellington | 3.60 | 132,267 | - | - | - | - | 20 | predicted (travel demand) |
| 222 | Bilbao | 2.41 | 133,133 | 4 | 1 | 1 | - | 30 | measured |
| 223 | Hobart | 2.41 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 224 | Potsdam | 2.41 | 51,727 | 18 | 8 | 3 | 16 | 20 | measured |
| 225 | Tallinn | 2.41 | 124,888 | 9 | 3 | 2 | 42 | 30 | measured |
| 226 | Warsaw | 2.41 | 197,929 | 39 | 20 | 4 | 1407 | 60 | measured |
| 227 | Brighton | 3.61 | 114,108 | 6 | 3 | 1 | - | 20 | measured |
| 228 | Cologne | 3.61 | 191,812 | 5 | - | 1 | - | 60 | measured |
| 229 | Crete | 3.61 | - | 4 | 3 | - | - | 30 | measured |
| 230 | Leuven | 3.61 | 40,645 | 4 | - | - | - | 20 | measured |
| 231 | Nice | 3.61 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 232 | Montpellier | 3.47 | 64,238 | - | - | - | - | 30 | predicted (travel demand) |
| 233 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 234 | Cape Town | 3.29 | 199,169 | - | - | - | - | 60 | predicted (travel demand) |
| 235 | Rhodes | 3.42 | 127,205 | - | - | - | - | 20 | predicted (travel demand) |
| 236 | San Antonio | 3.32 | - | 5 | 1 | 1 | - | 60 | published, never ranked (may be uncrawled) |
| 237 | Chania | 3.30 | 47,379 | - | - | - | - | 20 | predicted (travel demand) |
| 238 | Santiago | 3.25 | 111,647 | - | - | - | - | 100 | predicted (travel demand) |
| 239 | Tulsa | 3.01 | - | 1 | - | - | 3 | 30 | published, never ranked (may be uncrawled) |
| 240 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 30 | predicted (travel demand) |
| 241 | Lucerne | 3.10 | 66,356 | - | - | - | - | 20 | predicted (travel demand) |
| 242 | Miami | 2.37 | 278,558 | 7 | - | - | 15 | 30 | published, never ranked (may be uncrawled) |
| 243 | Malmo | 3.07 | 103,940 | - | - | - | - | 30 | predicted (travel demand) |
| 244 | Lille | 3.06 | 73,435 | - | - | - | - | 20 | predicted (travel demand) |
| 245 | Belgrade | 3.01 | 178,116 | 5 | 5 | - | - | 60 | measured |
| 246 | Corsica | 3.00 | - | - | - | - | - | 30 | predicted (travel demand) |
| 247 | Mechelen | 2.93 | 20,707 | - | - | - | - | 20 | predicted (travel demand) |
| 248 | Turin | 1.49 | 147,456 | 11 | 10 | 2 | 30 | 30 | published, never ranked (may be uncrawled) |
| 249 | Poznan | 1.89 | 65,666 | 10 | - | 1 | 397 | 30 | published, never ranked (may be uncrawled) |
| 250 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 251 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 252 | Corfu | 2.71 | 139,334 | - | - | - | - | 20 | predicted (travel demand) |
| 253 | Bali | 2.49 | - | 5 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 254 | Syracuse | 1.75 | 102,833 | - | - | - | - | 20 | predicted (travel demand) |
| 255 | Cartagena | 2.58 | 65,066 | - | - | - | - | 30 | predicted (travel demand) |
| 256 | Padua | 1.36 | 54,592 | 14 | 8 | 1 | 12 | 20 | published, never ranked (may be uncrawled) |
| 257 | Bern | 2.51 | 90,627 | - | - | - | - | 20 | predicted (travel demand) |
| 258 | Glasgow | 2.41 | 253,705 | 6 | 4 | - | - | 30 | measured |
| 259 | Vancouver | 2.41 | 351,552 | 7 | - | - | - | 30 | measured |
| 260 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 261 | Faro | 1.62 | 55,645 | - | - | - | - | 20 | predicted (travel demand) |
| 262 | Bruges | 2.41 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 263 | Bucharest | 2.41 | 136,836 | 4 | - | 1 | - | 60 | measured |
| 264 | Hilo | 2.41 | - | 6 | - | 1 | - | 10 | measured |
| 265 | Houston | 2.41 | - | 11 | - | 1 | - | 60 | measured |
| 266 | Maui | 2.41 | - | 4 | 2 | - | - | 20 | measured |
| 267 | Apeldoorn | 1.20 | - | 8 | - | 2 | 80 | 20 | measured |
| 268 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 269 | Delft | 1.20 | 31,293 | 12 | - | 1 | 60 | 20 | measured |
| 270 | Deventer | 1.20 | - | 12 | - | 1 | 213 | 20 | measured |
| 271 | Helmond | 1.20 | - | 19 | - | 2 | 54 | 20 | measured |
| 272 | Lucca | 1.20 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 273 | Maastricht | 1.20 | 47,763 | 16 | - | 2 | 135 | 20 | measured |
| 274 | Nijmegen | 1.20 | 42,338 | 20 | 1 | 3 | 159 | 20 | measured |
| 275 | Roosendaal | 1.20 | - | 20 | - | 2 | 138 | 20 | measured |
| 276 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 277 | Cusco | 2.35 | 87,732 | - | - | - | - | 30 | predicted (travel demand) |
| 278 | Limerick | 1.57 | 90,379 | - | - | - | - | 20 | predicted (travel demand) |
| 279 | Perugia | 1.20 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 280 | Trier | 1.56 | 69,369 | - | - | - | 154 | 20 | predicted (travel demand) |
| 281 | Guimaraes | 1.20 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 282 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 20 | predicted (travel demand) |
| 283 | Pisa | 1.46 | 52,174 | 4 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 284 | Hanoi | 2.15 | 117,396 | 2 | - | - | - | 100 | published, never ranked (may be uncrawled) |
| 285 | Setubal | 1.20 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 286 | Taipei | 2.09 | 143,193 | 4 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 287 | Salamanca | 1.37 | 47,897 | 4 | 1 | 1 | 1 | 20 | published, never ranked (may be uncrawled) |
| 288 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 289 | Tilburg | 1.03 | - | 17 | - | 3 | 86 | 20 | published, never ranked (may be uncrawled) |
| 290 | Girona | 1.20 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 291 | Bangkok | 1.81 | 222,206 | 5 | 1 | 1 | 5 | 100 | measured |
| 292 | Ischia | 1.32 | - | - | - | - | 2 | 20 | predicted (travel demand) |
| 293 | Bari | 1.20 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 294 | Matera | 1.20 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 295 | Pamplona | 1.20 | 128,065 | 25 | - | 3 | 9 | 20 | measured |
| 296 | Verona | 1.20 | 77,646 | 8 | 4 | 1 | 3 | 30 | measured |
| 297 | Izmir | 1.88 | 69,826 | - | - | - | - | 60 | predicted (travel demand) |
| 298 | Como | 0.96 | 82,645 | 9 | 3 | 1 | 23 | 20 | published, never ranked (may be uncrawled) |
| 299 | Segovia | 1.20 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 300 | Buenos Aires | 1.83 | 333,331 | 4 | 2 | - | - | 60 | published, never ranked (may be uncrawled) |
| 301 | Minneapolis | 1.88 | - | 4 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 302 | Hilversum | 0.93 | - | 6 | 1 | 1 | 122 | 20 | published, never ranked (may be uncrawled) |
| 303 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 304 | Baltimore | 1.77 | - | 4 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 305 | Bordeaux | 1.20 | 156,201 | 10 | - | 2 | 211 | 30 | measured |
| 306 | Canberra | 1.20 | - | 8 | 1 | 1 | 132 | 30 | measured |
| 307 | Lyon | 1.20 | 136,951 | 13 | 4 | 1 | 156 | 30 | measured |
| 308 | Nuremberg | 1.20 | 161,614 | 20 | 8 | 2 | 37 | 30 | measured |
| 309 | Quebec City | 1.20 | 124,358 | 6 | - | 1 | 494 | 30 | measured |
| 310 | Toulouse | 1.20 | 112,721 | 10 | - | 1 | 34 | 30 | measured |
| 311 | Wroclaw | 1.20 | 123,894 | 5 | 2 | 1 | 121 | 30 | measured |
| 312 | Auckland | 1.17 | 152,056 | 5 | 2 | - | 977 | 60 | published, never ranked (may be uncrawled) |
| 313 | Dijon | 1.72 | 43,526 | - | - | - | - | 20 | predicted (travel demand) |
| 314 | Annecy | 1.69 | 56,859 | - | - | - | - | 20 | predicted (travel demand) |
| 315 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 316 | Canterbury | 1.59 | 53,301 | - | - | - | - | 20 | predicted (travel demand) |
| 317 | Liverpool | 1.61 | 248,189 | 2 | 2 | - | - | 30 | published, never ranked (may be uncrawled) |
| 318 | Mostar | 1.58 | 63,907 | - | - | - | - | 20 | predicted (travel demand) |
| 319 | Malta | 1.45 | - | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 320 | Zadar | 1.53 | 71,549 | - | - | - | - | 20 | predicted (travel demand) |
| 321 | Helsinki | 1.20 | 148,908 | 12 | 3 | 1 | 13 | 30 | measured |
| 322 | Gothenburg | 1.49 | 119,991 | 5 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 323 | Heidelberg | 1.20 | 75,837 | 7 | 1 | 1 | - | 20 | measured |
| 324 | Antalya | 1.31 | 70,688 | - | - | - | - | 60 | predicted (travel demand) |
| 325 | Cardiff | 1.27 | - | 4 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 326 | Colmar | 1.28 | 45,517 | - | - | - | - | 20 | predicted (travel demand) |
| 327 | Regensburg | 1.20 | 51,930 | 8 | 2 | 1 | 3 | 20 | measured |
| 328 | Bodrum | 1.26 | 33,918 | - | - | - | - | 20 | predicted (travel demand) |
| 329 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 330 | Lausanne | 1.23 | 68,242 | 8 | 1 | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 331 | Ljubljana | 1.20 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 332 | Oxford | 1.20 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 333 | Riga | 1.20 | 108,918 | 5 | 2 | - | - | 30 | measured |
| 334 | Evora | 0.78 | 15,345 | - | - | - | - | 20 | predicted (travel demand) |
| 335 | Manchester | 1.20 | 316,438 | 5 | 1 | - | - | 30 | measured |
| 336 | Thessaloniki | 1.20 | 180,145 | 4 | - | 1 | - | 30 | measured |
| 337 | Turku | 1.20 | - | 1 | 1 | - | - | 20 | measured |
| 338 | Braga | 0.62 | 34,522 | 4 | 2 | - | 8 | 20 | published, never ranked (may be uncrawled) |
| 339 | Menorca | 0.73 | - | 6 | - | - | 2 | 20 | published, never ranked (may be uncrawled) |
| 340 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 341 | Zaragoza | 0.73 | 87,580 | 7 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 342 | Okinawa | 0.71 | 24,466 | 6 | - | - | 1 | 30 | published, never ranked (may be uncrawled) |
| 343 | La Palma | 0.70 | - | - | - | - | - | 20 | predicted (travel demand) |
| 344 | Dubrovnik | 0.99 | 119,586 | 4 | 4 | - | 2 | 10 | published, never ranked (may be uncrawled) |
| 345 | Azores | 0.65 | - | 3 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 346 | Split | 0.97 | 132,399 | 4 | - | 1 | 2 | 20 | published, never ranked (may be uncrawled) |
| 347 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 60 | predicted (travel demand) |
| 348 | Nantes | 0.96 | 67,689 | 1 | 1 | - | - | 30 | published, never ranked (may be uncrawled) |
| 349 | Innsbruck | 0.63 | 58,742 | 6 | 2 | 1 | 39 | 20 | published, never ranked (may be uncrawled) |
| 350 | Rothenburg ob der Tauber | 0.77 | 39,879 | 5 | 1 | 1 | 8 | 10 | published, never ranked (may be uncrawled) |
| 351 | Kandy | 0.78 | 24,159 | 1 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 352 | Gran Canaria | 0.42 | - | 5 | 4 | - | - | 30 | published, never ranked (may be uncrawled) |
| 353 | Modena | 0.44 | 51,698 | 5 | 1 | 1 | 3 | 20 | published, never ranked (may be uncrawled) |
| 354 | Den Bosch | 0.36 | 39,682 | 11 | 2 | 1 | 118 | 20 | published, never ranked (may be uncrawled) |
| 355 | Assen | 0.35 | - | 9 | - | 2 | 66 | 20 | published, never ranked (may be uncrawled) |
| 356 | Heerlen | 0.35 | - | 8 | 1 | 2 | 53 | 20 | published, never ranked (may be uncrawled) |
| 357 | Kamakura | 0.44 | 33,492 | 6 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 358 | Zwolle | 0.35 | - | 15 | - | 3 | 58 | 20 | published, never ranked (may be uncrawled) |
| 359 | Hallstatt | 0.50 | 47,271 | 7 | 4 | - | - | 10 | published, never ranked (may be uncrawled) |
| 360 | Hoorn | 0.30 | - | 12 | - | 2 | 52 | 20 | published, never ranked (may be uncrawled) |
| 361 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 100 | published, never ranked (may be uncrawled) |
| 362 | Rio de Janeiro | 0.60 | 279,431 | 6 | - | - | - | 100 | measured |
| 363 | Rouen | 0.54 | 72,334 | 12 | - | 1 | 6 | 20 | published, never ranked (may be uncrawled) |
| 364 | Phoenix | 0.55 | - | - | - | - | - | 60 | predicted (travel demand) |
| 365 | Cesky Krumlov | 0.34 | 28,582 | 6 | 3 | - | 11 | 10 | published, never ranked (may be uncrawled) |
| 366 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 367 | Killarney | 0.30 | 28,763 | 1 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 368 | Ferrara | 0.21 | 27,490 | 5 | 3 | 1 | 7 | 20 | published, never ranked (may be uncrawled) |
| 369 | Toledo | 0.24 | 3,149 | - | - | - | - | 20 | predicted (travel demand) |
| 370 | Anuradhapura | 0.32 | - | 1 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 371 | Bamberg | 0.24 | 28,716 | 9 | 7 | 1 | 12 | 20 | published, never ranked (may be uncrawled) |
| 372 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 373 | Assisi | 0.17 | 30,278 | 6 | 1 | 2 | 6 | 10 | published, never ranked (may be uncrawled) |
| 374 | George Town | 0.28 | 36,080 | - | - | - | - | 30 | predicted (travel demand) |
| 375 | Allentown | 0.24 | - | - | - | - | - | 20 | predicted (travel demand) |
| 376 | Oss | 0.11 | - | 5 | - | - | 48 | 20 | published, never ranked (may be uncrawled) |
| 377 | Queenstown | 0.16 | 36,672 | - | - | - | - | 10 | predicted (travel demand) |
| 378 | Buffalo | 0.15 | - | - | - | - | - | 10 | predicted (travel demand) |
| 379 | San Juan | 0.15 | - | - | - | - | - | 10 | predicted (travel demand) |
| 380 | Halifax | 0.08 | - | - | - | - | - | 30 | predicted (travel demand) |
| 381 | Memphis | 0.08 | - | - | - | - | - | 30 | predicted (travel demand) |

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

