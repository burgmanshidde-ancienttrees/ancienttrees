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
| 1 | Palermo | 68.53 | 124,310 | 22 | 11 | 2 | 37 | 30 | measured |
| 2 | Seville | 79.72 | 170,545 | 44 | 12 | 2 | - | 30 | measured |
| 3 | Lisbon | 57.35 | 201,877 | 37 | 21 | 3 | 67 | 30 | measured |
| 4 | Tokyo | 60.14 | 394,702 | 22 | 16 | 1 | 5 | 100 | measured |
| 5 | Tenerife | 68.53 | - | 4 | 4 | - | - | 30 | measured |
| 6 | Berlin | 61.54 | 412,181 | 63 | 51 | 5 | 195 | 60 | measured |
| 7 | Singapore | 61.54 | 967,821 | 34 | 7 | 3 | 165 | 100 | measured |
| 8 | New York | 58.74 | 1,124,326 | 29 | 10 | 2 | - | 100 | measured |
| 9 | Fukuoka | 33.57 | 77,485 | 18 | 11 | 1 | - | 60 | measured |
| 10 | Paris | 32.17 | 524,268 | 58 | 15 | 8 | 129 | 60 | measured |
| 11 | Rome | 23.78 | 358,876 | 31 | 10 | 2 | 32 | 60 | measured |
| 12 | Copenhagen | 43.36 | 218,621 | 49 | 41 | 6 | - | 30 | measured |
| 13 | Alicante | 22.38 | 77,454 | 21 | 4 | 2 | 44 | 30 | measured |
| 14 | Munich | 29.37 | 224,067 | 63 | 35 | 8 | 74 | 60 | measured |
| 15 | Monterey | 41.96 | - | 3 | 2 | - | - | 10 | measured |
| 16 | Austin | 39.16 | 226,631 | 10 | 4 | 1 | - | 30 | measured |
| 17 | Coimbra | 20.98 | 34,962 | 6 | - | - | 5 | 20 | measured |
| 18 | Malaga | 25.18 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 19 | San Francisco | 25.18 | 361,111 | 12 | 3 | 1 | 26 | 30 | measured |
| 20 | Birmingham | 37.53 | - | - | - | - | - | 60 | predicted (travel demand) |
| 21 | Dublin | 20.98 | 240,850 | 19 | 4 | 2 | 12 | 30 | measured |
| 22 | Porto | 18.18 | 120,415 | 29 | 16 | 2 | 42 | 30 | measured |
| 23 | London | 30.77 | 718,291 | 32 | 25 | 1 | - | 100 | measured |
| 24 | Boston | 33.57 | 385,902 | 13 | 3 | 2 | - | 30 | measured |
| 25 | Amsterdam | 16.78 | 294,030 | 27 | 7 | 2 | 5488 | 30 | measured |
| 26 | Brisbane | 20.98 | 162,602 | 20 | 5 | 2 | 186 | 60 | measured |
| 27 | Luxembourg City | 20.98 | 64,851 | 10 | 8 | 2 | 18 | 20 | measured |
| 28 | Kyoto | 19.58 | 142,353 | 18 | 14 | 2 | - | 60 | measured |
| 29 | Cambridge | 27.97 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 30 | Madrid | 16.78 | 274,553 | 18 | 11 | 2 | - | 60 | measured |
| 31 | Venice | 13.99 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 32 | The Hague | 12.59 | 236,723 | 26 | 4 | 5 | 166 | 30 | measured |
| 33 | Portland | 16.78 | 217,222 | 33 | 2 | 3 | 306 | 30 | measured |
| 34 | Bologna | 12.59 | 146,161 | 12 | 7 | 1 | 9 | 30 | measured |
| 35 | Jacksonville | 22.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 36 | Bath | 22.38 | 144,950 | 5 | 2 | 1 | - | 20 | measured |
| 37 | Kanazawa | 13.99 | 25,778 | 7 | 3 | 1 | 2 | 30 | measured |
| 38 | Asheville | 20.89 | - | - | - | - | - | 20 | predicted (travel demand) |
| 39 | Long Beach | 20.48 | - | - | - | - | - | 30 | predicted (travel demand) |
| 40 | Little Rock | 20.40 | - | - | - | - | - | 20 | predicted (travel demand) |
| 41 | Leeuwarden | 9.79 | - | 34 | - | 2 | 61 | 20 | measured |
| 42 | Oakland | 18.81 | - | - | - | - | - | 30 | predicted (travel demand) |
| 43 | Lexington | 18.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 44 | Reno | 18.19 | - | - | - | - | - | 30 | predicted (travel demand) |
| 45 | Des Moines | 18.11 | - | - | - | - | - | 20 | predicted (travel demand) |
| 46 | Sardinia | 9.79 | - | 7 | 6 | - | 10 | 60 | measured |
| 47 | Daytona Beach | 17.66 | - | - | - | - | - | 20 | predicted (travel demand) |
| 48 | Krakow | 11.19 | 140,824 | 38 | 11 | 3 | 198 | 30 | measured |
| 49 | Prague | 11.19 | 303,350 | 30 | 21 | 4 | 31 | 60 | measured |
| 50 | Montreal | 16.78 | 315,322 | 14 | 2 | 2 | - | 60 | measured |
| 51 | Oahu | 16.78 | - | 21 | 8 | 3 | - | 30 | measured |
| 52 | Chattanooga | 16.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 53 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 54 | Washington DC | 13.99 | 606,731 | 21 | 8 | 4 | - | 30 | measured |
| 55 | Huntsville | 15.35 | - | - | - | - | - | 20 | predicted (travel demand) |
| 56 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 57 | West Palm Beach | 14.98 | - | - | - | - | - | 20 | predicted (travel demand) |
| 58 | Saint Petersburg | 14.83 | - | - | - | - | - | 100 | predicted (travel demand) |
| 59 | St. Louis | 14.80 | - | - | - | - | - | 30 | predicted (travel demand) |
| 60 | Charleston | 13.99 | 155,987 | 3 | 1 | - | - | 20 | measured |
| 61 | Edinburgh | 13.99 | 292,981 | 21 | 9 | 1 | - | 30 | measured |
| 62 | Tampa | 14.10 | - | - | - | - | - | 30 | predicted (travel demand) |
| 63 | Hawaii | 13.99 | - | 6 | - | 1 | - | 60 | measured |
| 64 | Kauai | 13.99 | - | 6 | 1 | - | - | 20 | measured |
| 65 | New Orleans | 13.99 | 256,232 | 8 | 6 | 1 | - | 30 | measured |
| 66 | Amersfoort | 6.99 | - | 21 | 1 | 2 | 181 | 20 | measured |
| 67 | Barcelona | 6.99 | 346,477 | 58 | 20 | 7 | 177 | 60 | measured |
| 68 | Naples | 6.99 | 198,913 | 24 | 5 | 3 | 46 | 30 | measured |
| 69 | Trieste | 6.99 | 117,233 | 36 | 1 | 3 | 43 | 20 | measured |
| 70 | Madeira | 8.39 | - | 11 | 2 | 1 | - | 30 | measured |
| 71 | Stockholm | 11.19 | 188,184 | 8 | 7 | - | - | 30 | measured |
| 72 | Cincinnati | 13.33 | - | - | - | - | - | 30 | predicted (travel demand) |
| 73 | Chicago | 11.19 | 485,769 | 38 | 2 | 3 | 9 | 60 | measured |
| 74 | Lansing | 13.02 | - | - | - | - | - | 20 | predicted (travel demand) |
| 75 | Athens | 12.59 | 235,429 | 12 | 7 | 2 | - | 30 | measured |
| 76 | Cork | 8.39 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 77 | Gdansk | 8.39 | 4,908 | 12 | 5 | 1 | 307 | 30 | measured |
| 78 | Leipzig | 8.39 | 121,319 | 29 | 24 | 4 | - | 30 | measured |
| 79 | Detroit | 12.53 | - | - | - | - | - | 30 | predicted (travel demand) |
| 80 | Seoul | 11.19 | 206,265 | 8 | 5 | 1 | - | 100 | measured |
| 81 | Chiang Mai | 11.42 | 66,541 | - | - | - | 2 | 60 | predicted (travel demand) |
| 82 | Denver | 11.66 | - | - | - | - | - | 30 | predicted (travel demand) |
| 83 | Seattle | 11.19 | 398,724 | 30 | 3 | 4 | - | 30 | measured |
| 84 | Los Angeles | 11.19 | 665,559 | 11 | 3 | - | - | 60 | measured |
| 85 | Toronto | 11.19 | 411,011 | 6 | - | - | - | 60 | measured |
| 86 | San Jose | 11.39 | - | - | - | - | - | 60 | predicted (travel demand) |
| 87 | Sacramento | 11.32 | - | - | - | - | - | 30 | predicted (travel demand) |
| 88 | Antwerp | 11.19 | 128,289 | 10 | 4 | 1 | - | 30 | measured |
| 89 | Boise | 11.19 | - | 4 | - | 1 | - | 20 | measured |
| 90 | San Diego | 11.19 | 214,939 | 6 | 1 | 1 | - | 60 | measured |
| 91 | Arnhem | 5.59 | 31,478 | 32 | 3 | 3 | 202 | 20 | measured |
| 92 | Florence | 5.59 | 184,099 | 27 | 9 | 1 | 27 | 30 | measured |
| 93 | Milan | 5.59 | 212,705 | 30 | 14 | 3 | 25 | 60 | measured |
| 94 | Utrecht | 5.59 | 67,963 | 30 | 9 | 2 | 339 | 30 | measured |
| 95 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 60 | predicted (travel demand) |
| 96 | Reykjavik | 9.79 | 166,789 | 4 | 3 | 1 | - | 20 | measured |
| 97 | Dubai | 11.02 | 334,167 | - | - | - | - | 60 | predicted (travel demand) |
| 98 | Milwaukee | 10.63 | - | - | - | - | - | 30 | predicted (travel demand) |
| 99 | Hong Kong | 6.99 | 689,212 | 21 | 6 | 2 | 505 | 100 | measured |
| 100 | Jersey City | 10.08 | - | - | - | - | - | 30 | predicted (travel demand) |
| 101 | Hamburg | 9.79 | 191,221 | 6 | 4 | 1 | - | 60 | measured |
| 102 | Atlanta | 10.29 | - | - | - | - | - | 30 | predicted (travel demand) |
| 103 | Anchorage | 10.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 104 | Budapest | 9.79 | 283,807 | 13 | 2 | 3 | - | 60 | measured |
| 105 | Genoa | 5.59 | 145,206 | 13 | 2 | 1 | 10 | 30 | measured |
| 106 | Raleigh | 10.07 | - | - | - | - | - | 30 | predicted (travel demand) |
| 107 | Belfast | 9.79 | 224,315 | 5 | 2 | 1 | - | 30 | measured |
| 108 | Cleveland | 9.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 109 | El Paso | 9.70 | - | - | - | - | - | 30 | predicted (travel demand) |
| 110 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 111 | Catania | 5.59 | 58,252 | 4 | 3 | 1 | 5 | 30 | measured |
| 112 | Edmonton | 9.38 | - | - | - | - | - | 60 | predicted (travel demand) |
| 113 | Winnipeg | 9.21 | - | - | - | - | - | 30 | predicted (travel demand) |
| 114 | Nashville | 8.93 | - | - | - | - | - | 30 | predicted (travel demand) |
| 115 | Ibiza | 5.59 | - | 1 | - | - | 4 | 20 | measured |
| 116 | Tampere | 8.78 | - | - | - | - | - | 30 | predicted (travel demand) |
| 117 | Istanbul | 7.69 | 333,027 | 14 | 4 | 1 | - | 100 | measured |
| 118 | Philadelphia | 8.39 | 405,294 | 4 | 1 | - | - | 60 | measured |
| 119 | Cordoba | 5.59 | 74,675 | 16 | 2 | 2 | 3 | 30 | measured |
| 120 | Osaka | 5.59 | 163,112 | 6 | 1 | - | - | 60 | measured |
| 121 | Aarhus | 8.39 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 122 | Perth | 8.39 | 180,478 | 6 | 4 | 1 | - | 60 | measured |
| 123 | Sydney | 8.39 | 305,304 | 7 | 1 | - | - | 100 | measured |
| 124 | Ann Arbor | 8.55 | - | - | - | - | - | 20 | predicted (travel demand) |
| 125 | Nagoya | 5.59 | 83,437 | 6 | 2 | - | 1 | 60 | measured |
| 126 | Alkmaar | 4.20 | - | 11 | - | 2 | 79 | 20 | measured |
| 127 | Eindhoven | 4.20 | - | 17 | - | 3 | 195 | 20 | measured |
| 128 | Enschede | 4.20 | - | 13 | 1 | 1 | 82 | 20 | measured |
| 129 | Valencia | 4.20 | 162,209 | 31 | 4 | 2 | 350 | 30 | measured |
| 130 | York | 8.39 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 131 | Brno | 5.59 | 63,714 | 8 | 7 | 2 | 34 | 30 | measured |
| 132 | Brussels | 5.59 | 176,863 | 35 | 4 | 2 | 436 | 60 | measured |
| 133 | Geneva | 5.59 | 162,269 | 21 | 6 | 4 | 131 | 20 | measured |
| 134 | Hiroshima | 5.59 | 129,791 | 33 | 5 | 2 | - | 60 | measured |
| 135 | Melbourne | 5.59 | 267,898 | 16 | 1 | 2 | 403 | 100 | measured |
| 136 | Strasbourg | 5.59 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 137 | Vienna | 5.59 | 283,090 | 58 | 25 | 6 | 371 | 60 | measured |
| 138 | Adelaide | 8.14 | 139,166 | - | - | - | - | 60 | predicted (travel demand) |
| 139 | Albuquerque | 7.83 | - | - | - | - | - | 30 | predicted (travel demand) |
| 140 | Spokane | 5.59 | - | 14 | - | 2 | 18 | 20 | measured |
| 141 | Cagliari | 4.20 | 51,351 | 14 | 1 | 2 | 14 | 20 | measured |
| 142 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 20 | predicted (travel demand) |
| 143 | Bergen | 7.30 | 82,940 | - | - | - | - | 30 | predicted (travel demand) |
| 144 | Ronda | 4.20 | 51,510 | 6 | 1 | - | 9 | 10 | measured |
| 145 | Cyprus | 6.99 | - | 4 | - | - | - | 60 | measured |
| 146 | Palma de Mallorca | 4.20 | 84,075 | 6 | 2 | 1 | 8 | 30 | measured |
| 147 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 20 | predicted (travel demand) |
| 148 | Siena | 4.62 | 57,436 | - | - | - | - | 20 | predicted (travel demand) |
| 149 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 20 | predicted (travel demand) |
| 150 | Frankfurt | 4.51 | 150,379 | 28 | 11 | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 151 | Yakushima | 4.20 | - | 2 | 2 | - | 1 | 10 | measured |
| 152 | Zagreb | 6.42 | 122,890 | - | - | - | - | 30 | predicted (travel demand) |
| 153 | Bogota | 6.39 | 1,623 | - | - | - | - | 100 | predicted (travel demand) |
| 154 | Shanghai | 6.38 | 277,140 | - | - | - | - | 100 | predicted (travel demand) |
| 155 | Oslo | 5.59 | 181,113 | 4 | 3 | - | - | 30 | measured |
| 156 | Sapporo | 4.20 | 88,633 | 6 | 1 | - | - | 60 | measured |
| 157 | Vilnius | 4.20 | 113,188 | 12 | 4 | 1 | 34 | 30 | measured |
| 158 | Funchal | 3.77 | 174,351 | - | - | - | - | 20 | predicted (travel demand) |
| 159 | Dallas | 6.15 | - | 12 | 2 | 1 | - | 60 | published, never ranked (may be uncrawled) |
| 160 | Mexico City | 5.59 | 566,583 | 9 | 2 | - | - | 100 | measured |
| 161 | Ghent | 5.59 | 82,757 | 8 | 2 | 1 | - | 30 | measured |
| 162 | Zurich | 5.59 | 140,788 | 6 | 2 | - | - | 30 | measured |
| 163 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 164 | Bergamo | 2.80 | 52,933 | 9 | 2 | 1 | 17 | 20 | measured |
| 165 | Breda | 2.80 | 36,579 | 11 | 1 | 2 | 120 | 20 | measured |
| 166 | Caserta | 2.80 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 167 | Dordrecht | 2.80 | - | 17 | 1 | 2 | 105 | 20 | measured |
| 168 | Groningen | 2.80 | 31,401 | 17 | - | 2 | 76 | 20 | measured |
| 169 | Haarlem | 2.80 | 33,960 | 21 | 2 | 2 | 277 | 20 | measured |
| 170 | Rotterdam | 2.80 | 104,938 | 17 | 1 | 2 | 83 | 30 | measured |
| 171 | Sintra | 2.80 | 46,889 | 7 | 6 | 1 | 6 | 30 | measured |
| 172 | Sorrento | 2.80 | 40,049 | 7 | - | 1 | 20 | 10 | measured |
| 173 | Trento | 2.80 | 56,455 | 10 | 2 | 1 | 20 | 20 | measured |
| 174 | Beijing | 5.59 | 269,737 | 7 | 1 | - | - | 100 | measured |
| 175 | Bristol | 5.59 | 163,983 | 12 | 2 | 1 | - | 30 | measured |
| 176 | Las Vegas | 5.59 | - | 11 | 6 | 2 | - | 30 | measured |
| 177 | Avignon | 5.54 | 64,047 | - | - | - | - | 20 | predicted (travel demand) |
| 178 | Galway | 3.65 | 88,162 | - | - | - | - | 20 | predicted (travel demand) |
| 179 | Phuket | 5.46 | 5,487 | - | - | - | - | 30 | predicted (travel demand) |
| 180 | Rovaniemi | 5.38 | - | - | - | - | - | 20 | predicted (travel demand) |
| 181 | Lagos | 3.43 | 34,452 | - | - | - | - | 100 | predicted (travel demand) |
| 182 | Kansas City | 5.26 | - | 4 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 183 | Santa Fe | 5.17 | - | - | - | - | - | 20 | predicted (travel demand) |
| 184 | Lund | 5.14 | - | - | - | - | - | 20 | predicted (travel demand) |
| 185 | Kobe | 3.40 | 54,798 | - | - | - | - | 60 | predicted (travel demand) |
| 186 | Fort Lauderdale | 4.61 | - | 4 | - | - | 4 | 20 | published, never ranked (may be uncrawled) |
| 187 | Parma | 2.80 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 188 | Heraklion | 4.96 | 66,359 | - | - | - | - | 20 | predicted (travel demand) |
| 189 | Marseille | 4.96 | 182,033 | - | - | - | - | 30 | predicted (travel demand) |
| 190 | Tarragona | 2.80 | 32,396 | 3 | 1 | - | - | 20 | measured |
| 191 | Stuttgart | 4.20 | 112,789 | 11 | 7 | - | - | 30 | measured |
| 192 | Indianapolis | 4.57 | - | 1 | 1 | - | - | 30 | published, never ranked (may be uncrawled) |
| 193 | Basel | 4.59 | 105,838 | - | - | - | - | 20 | predicted (travel demand) |
| 194 | Key West | 3.95 | - | 2 | 1 | - | 7 | 10 | published, never ranked (may be uncrawled) |
| 195 | Tasmania | 4.41 | - | - | - | - | - | 30 | predicted (travel demand) |
| 196 | Cadiz | 2.80 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 197 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 20 | predicted (travel demand) |
| 198 | Busan | 4.20 | 94,737 | 2 | - | - | - | 60 | measured |
| 199 | Sofia | 2.81 | 138,710 | 4 | - | - | - | 60 | published, never ranked (may be uncrawled) |
| 200 | Bilbao | 2.80 | 133,133 | 4 | 1 | 1 | - | 30 | measured |
| 201 | Bratislava | 2.80 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 202 | Brighton | 4.20 | 114,108 | 6 | 3 | 1 | - | 20 | measured |
| 203 | Christchurch | 2.80 | 104,874 | 6 | 2 | 1 | 466 | 30 | measured |
| 204 | Cologne | 4.20 | 191,812 | 5 | - | 1 | - | 60 | measured |
| 205 | Dresden | 2.80 | 113,624 | 32 | 25 | 1 | - | 30 | measured |
| 206 | Hobart | 2.80 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 207 | Nice | 4.20 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 208 | Ottawa | 2.80 | - | 21 | - | 3 | 122 | 60 | measured |
| 209 | Potsdam | 2.80 | 51,727 | 18 | 8 | 3 | 16 | 20 | measured |
| 210 | Salzburg | 2.80 | 107,243 | 21 | 12 | 3 | 33 | 20 | measured |
| 211 | San Sebastian | 2.80 | 367 | - | - | - | - | 20 | predicted (travel demand) |
| 212 | Warsaw | 2.80 | 197,929 | 39 | 20 | 4 | 1407 | 60 | measured |
| 213 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 30 | predicted (travel demand) |
| 214 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 215 | Pittsburgh | 3.80 | - | 12 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 216 | Salt Lake City | 2.58 | - | 6 | - | 1 | 39 | 20 | published, never ranked (may be uncrawled) |
| 217 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 218 | Niagara Falls | 3.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 219 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 100 | predicted (travel demand) |
| 220 | Wellington | 3.60 | 132,267 | - | - | - | - | 20 | predicted (travel demand) |
| 221 | Belgrade | 3.50 | 178,116 | 5 | 5 | - | - | 60 | measured |
| 222 | Montpellier | 3.47 | 64,238 | - | - | - | - | 30 | predicted (travel demand) |
| 223 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 224 | Cape Town | 3.29 | 199,169 | - | - | - | - | 60 | predicted (travel demand) |
| 225 | Rhodes | 3.42 | 127,205 | - | - | - | - | 20 | predicted (travel demand) |
| 226 | San Antonio | 3.32 | - | 5 | 1 | 1 | - | 60 | published, never ranked (may be uncrawled) |
| 227 | Chania | 3.30 | 47,379 | - | - | - | - | 20 | predicted (travel demand) |
| 228 | Santiago | 3.25 | 111,647 | - | - | - | - | 100 | predicted (travel demand) |
| 229 | Tulsa | 3.01 | - | 1 | - | - | 3 | 30 | published, never ranked (may be uncrawled) |
| 230 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 30 | predicted (travel demand) |
| 231 | Lucerne | 3.10 | 66,356 | - | - | - | - | 20 | predicted (travel demand) |
| 232 | Miami | 2.37 | 278,558 | 7 | - | - | 15 | 30 | published, never ranked (may be uncrawled) |
| 233 | Malmo | 3.07 | 103,940 | - | - | - | - | 30 | predicted (travel demand) |
| 234 | Lille | 3.06 | 73,435 | - | - | - | - | 20 | predicted (travel demand) |
| 235 | Corsica | 3.00 | - | - | - | - | - | 30 | predicted (travel demand) |
| 236 | Mechelen | 2.93 | 20,707 | - | - | - | - | 20 | predicted (travel demand) |
| 237 | Turin | 1.49 | 147,456 | 11 | 10 | 2 | 30 | 30 | published, never ranked (may be uncrawled) |
| 238 | Sao Paulo | 2.80 | 911 | 1 | - | - | - | 100 | measured |
| 239 | Glasgow | 2.80 | 253,705 | 6 | 4 | - | - | 30 | measured |
| 240 | Vancouver | 2.80 | 351,552 | 7 | - | - | - | 30 | measured |
| 241 | Poznan | 1.89 | 65,666 | 10 | - | 1 | 397 | 30 | published, never ranked (may be uncrawled) |
| 242 | Apeldoorn | 1.40 | - | 8 | - | 2 | 80 | 20 | measured |
| 243 | Bruges | 2.80 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 244 | Bucharest | 2.80 | 136,836 | 4 | - | 1 | - | 60 | measured |
| 245 | Crete | 2.80 | - | 4 | 3 | - | - | 30 | measured |
| 246 | Deventer | 1.40 | - | 12 | - | 1 | 213 | 20 | measured |
| 247 | Fort Worth | 2.80 | - | 22 | - | 1 | - | 30 | measured |
| 248 | Helmond | 1.40 | - | 19 | - | 2 | 54 | 20 | measured |
| 249 | Hilo | 2.80 | - | 6 | - | 1 | - | 10 | measured |
| 250 | Houston | 2.80 | - | 11 | - | 1 | - | 60 | measured |
| 251 | Leiden | 1.40 | 33,227 | 19 | 6 | 1 | 129 | 20 | measured |
| 252 | Leuven | 2.80 | 40,645 | 4 | - | - | - | 20 | measured |
| 253 | Lucca | 1.40 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 254 | Maastricht | 1.40 | 47,763 | 16 | - | 2 | 135 | 20 | measured |
| 255 | Maui | 2.80 | - | 4 | 2 | - | - | 20 | measured |
| 256 | Nijmegen | 1.40 | 42,338 | 20 | 1 | 3 | 159 | 20 | measured |
| 257 | Roosendaal | 1.40 | - | 20 | - | 2 | 138 | 20 | measured |
| 258 | Venlo | 1.40 | - | 7 | - | 1 | 144 | 20 | measured |
| 259 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 260 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 261 | Corfu | 2.71 | 139,334 | - | - | - | - | 20 | predicted (travel demand) |
| 262 | Bali | 2.49 | - | 5 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 263 | Syracuse | 1.75 | 102,833 | - | - | - | - | 20 | predicted (travel demand) |
| 264 | Cartagena | 2.58 | 65,066 | - | - | - | - | 30 | predicted (travel demand) |
| 265 | Setubal | 1.40 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 266 | Padua | 1.36 | 54,592 | 14 | 8 | 1 | 12 | 20 | published, never ranked (may be uncrawled) |
| 267 | Braga | 1.40 | 34,522 | 4 | 2 | - | 8 | 20 | measured |
| 268 | Bern | 2.51 | 90,627 | - | - | - | - | 20 | predicted (travel demand) |
| 269 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 270 | Faro | 1.62 | 55,645 | - | - | - | - | 20 | predicted (travel demand) |
| 271 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 272 | Lyon | 1.60 | 136,951 | 13 | 4 | 1 | 156 | 30 | published, never ranked (may be uncrawled) |
| 273 | Girona | 1.40 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 274 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 275 | Bari | 1.40 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 276 | Cusco | 2.35 | 87,732 | - | - | - | - | 30 | predicted (travel demand) |
| 277 | Limerick | 1.57 | 90,379 | - | - | - | - | 20 | predicted (travel demand) |
| 278 | Matera | 1.40 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 279 | Verona | 1.40 | 77,646 | 8 | 4 | 1 | 3 | 30 | measured |
| 280 | Trier | 1.56 | 69,369 | - | - | - | 154 | 20 | predicted (travel demand) |
| 281 | Turku | 2.31 | - | 1 | 1 | - | - | 20 | published, never ranked (may be uncrawled) |
| 282 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 20 | predicted (travel demand) |
| 283 | Manchester | 2.26 | 316,438 | 5 | 1 | - | - | 30 | published, never ranked (may be uncrawled) |
| 284 | Pisa | 1.46 | 52,174 | 4 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 285 | Hanoi | 2.15 | 117,396 | 2 | - | - | - | 100 | published, never ranked (may be uncrawled) |
| 286 | Granada | 1.40 | 86,361 | 9 | 4 | 2 | 4 | 20 | measured |
| 287 | Bordeaux | 1.40 | 156,201 | 10 | - | 2 | 211 | 30 | measured |
| 288 | Canberra | 1.40 | - | 8 | 1 | 1 | 132 | 30 | measured |
| 289 | Graz | 1.40 | 65,717 | 17 | 10 | 2 | 87 | 30 | measured |
| 290 | Nuremberg | 1.40 | 161,614 | 20 | 8 | 2 | 37 | 30 | measured |
| 291 | Quebec City | 1.40 | 124,358 | 6 | - | 1 | 494 | 30 | measured |
| 292 | Tallinn | 1.40 | 124,888 | 9 | 3 | 2 | 42 | 30 | measured |
| 293 | Toulouse | 1.40 | 112,721 | 10 | - | 1 | 34 | 30 | measured |
| 294 | Wroclaw | 1.40 | 123,894 | 5 | 2 | 1 | 121 | 30 | measured |
| 295 | Taipei | 2.09 | 143,193 | 4 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 296 | Salamanca | 1.37 | 47,897 | 4 | 1 | 1 | 1 | 20 | published, never ranked (may be uncrawled) |
| 297 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 298 | Tilburg | 1.03 | - | 17 | - | 3 | 86 | 20 | published, never ranked (may be uncrawled) |
| 299 | Ischia | 1.32 | - | - | - | - | 2 | 20 | predicted (travel demand) |
| 300 | Izmir | 1.88 | 69,826 | - | - | - | - | 60 | predicted (travel demand) |
| 301 | Como | 0.96 | 82,645 | 9 | 3 | 1 | 23 | 20 | published, never ranked (may be uncrawled) |
| 302 | Buenos Aires | 1.83 | 333,331 | 4 | 2 | - | - | 60 | published, never ranked (may be uncrawled) |
| 303 | Minneapolis | 1.88 | - | 4 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 304 | Hilversum | 0.93 | - | 6 | 1 | 1 | 122 | 20 | published, never ranked (may be uncrawled) |
| 305 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 306 | Baltimore | 1.77 | - | 4 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 307 | Killarney | 1.20 | 28,763 | 1 | 1 | - | - | 10 | predicted (travel demand) |
| 308 | Helsinki | 1.40 | 148,908 | 12 | 3 | 1 | 13 | 30 | measured |
| 309 | Auckland | 1.17 | 152,056 | 5 | 2 | - | 977 | 60 | published, never ranked (may be uncrawled) |
| 310 | Dijon | 1.72 | 43,526 | - | - | - | - | 20 | predicted (travel demand) |
| 311 | Annecy | 1.69 | 56,859 | - | - | - | - | 20 | predicted (travel demand) |
| 312 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 313 | Canterbury | 1.59 | 53,301 | - | - | - | - | 20 | predicted (travel demand) |
| 314 | Liverpool | 1.61 | 248,189 | 2 | 2 | - | - | 30 | published, never ranked (may be uncrawled) |
| 315 | Mostar | 1.58 | 63,907 | - | - | - | - | 20 | predicted (travel demand) |
| 316 | Bangkok | 1.40 | 222,206 | 5 | 1 | 1 | 5 | 100 | measured |
| 317 | Heidelberg | 1.40 | 75,837 | 7 | 1 | 1 | - | 20 | measured |
| 318 | Malta | 1.45 | - | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 319 | Zadar | 1.53 | 71,549 | - | - | - | - | 20 | predicted (travel demand) |
| 320 | Savannah | 1.52 | 128,162 | 3 | 1 | - | - | 20 | published, never ranked (may be uncrawled) |
| 321 | Oxford | 1.40 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 322 | Gothenburg | 1.49 | 119,991 | 5 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 323 | Delft | 0.74 | 31,293 | 12 | - | 1 | 60 | 20 | published, never ranked (may be uncrawled) |
| 324 | Regensburg | 1.40 | 51,930 | 8 | 2 | 1 | 3 | 20 | measured |
| 325 | Freiburg | 1.40 | 92,752 | 8 | 4 | 1 | - | 20 | measured |
| 326 | Ljubljana | 1.40 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 327 | Riga | 1.40 | 108,918 | 5 | 2 | - | - | 30 | measured |
| 328 | Nantes | 1.40 | 67,689 | 1 | 1 | - | - | 30 | measured |
| 329 | Thessaloniki | 1.40 | 180,145 | 4 | - | 1 | - | 30 | measured |
| 330 | Antalya | 1.31 | 70,688 | - | - | - | - | 60 | predicted (travel demand) |
| 331 | Cardiff | 1.27 | - | 4 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 332 | Colmar | 1.28 | 45,517 | - | - | - | - | 20 | predicted (travel demand) |
| 333 | Bodrum | 1.26 | 33,918 | - | - | - | - | 20 | predicted (travel demand) |
| 334 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 335 | Lausanne | 1.23 | 68,242 | 8 | 1 | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 336 | Evora | 0.78 | 15,345 | - | - | - | - | 20 | predicted (travel demand) |
| 337 | Menorca | 0.73 | - | 6 | - | - | 2 | 20 | published, never ranked (may be uncrawled) |
| 338 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 339 | Zaragoza | 0.73 | 87,580 | 7 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 340 | Okinawa | 0.71 | 24,466 | 6 | - | - | 1 | 30 | published, never ranked (may be uncrawled) |
| 341 | La Palma | 0.70 | - | - | - | - | - | 20 | predicted (travel demand) |
| 342 | Dubrovnik | 0.99 | 119,586 | 4 | 4 | - | 2 | 10 | published, never ranked (may be uncrawled) |
| 343 | Azores | 0.65 | - | 3 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 344 | Split | 0.97 | 132,399 | 4 | - | 1 | 2 | 20 | published, never ranked (may be uncrawled) |
| 345 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 60 | predicted (travel demand) |
| 346 | Innsbruck | 0.63 | 58,742 | 6 | 2 | 1 | 39 | 20 | published, never ranked (may be uncrawled) |
| 347 | Rothenburg ob der Tauber | 0.77 | 39,879 | 5 | 1 | 1 | 8 | 10 | published, never ranked (may be uncrawled) |
| 348 | Segovia | 0.54 | 30,968 | 6 | - | 1 | 5 | 20 | published, never ranked (may be uncrawled) |
| 349 | Kandy | 0.78 | 24,159 | 1 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 350 | Gran Canaria | 0.42 | - | 5 | 4 | - | - | 30 | published, never ranked (may be uncrawled) |
| 351 | Modena | 0.44 | 51,698 | 5 | 1 | 1 | 3 | 20 | published, never ranked (may be uncrawled) |
| 352 | Den Bosch | 0.36 | 39,682 | 11 | 2 | 1 | 118 | 20 | published, never ranked (may be uncrawled) |
| 353 | Assen | 0.35 | - | 9 | - | 2 | 66 | 20 | published, never ranked (may be uncrawled) |
| 354 | Heerlen | 0.35 | - | 8 | 1 | 2 | 53 | 20 | published, never ranked (may be uncrawled) |
| 355 | Kamakura | 0.44 | 33,492 | 6 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 356 | Rio de Janeiro | 0.70 | 279,431 | 6 | - | - | - | 100 | measured |
| 357 | Zwolle | 0.35 | - | 15 | - | 3 | 58 | 20 | published, never ranked (may be uncrawled) |
| 358 | Guimaraes | 0.32 | 26,203 | 8 | 1 | 1 | 19 | 20 | published, never ranked (may be uncrawled) |
| 359 | Hallstatt | 0.50 | 47,271 | 7 | 4 | - | - | 10 | published, never ranked (may be uncrawled) |
| 360 | Hoorn | 0.30 | - | 12 | - | 2 | 52 | 20 | published, never ranked (may be uncrawled) |
| 361 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 100 | published, never ranked (may be uncrawled) |
| 362 | Rouen | 0.54 | 72,334 | 12 | - | 1 | 6 | 20 | published, never ranked (may be uncrawled) |
| 363 | Pamplona | 0.34 | 128,065 | 25 | - | 3 | 9 | 20 | published, never ranked (may be uncrawled) |
| 364 | Perugia | 0.29 | 42,572 | 12 | - | 2 | 19 | 20 | published, never ranked (may be uncrawled) |
| 365 | Phoenix | 0.55 | - | - | - | - | - | 60 | predicted (travel demand) |
| 366 | Cesky Krumlov | 0.34 | 28,582 | 6 | 3 | - | 11 | 10 | published, never ranked (may be uncrawled) |
| 367 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
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

