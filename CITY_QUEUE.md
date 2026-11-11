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
| 1 | Lisbon | 87.51 | 201,877 | 37 | 21 | 3 | 67 | 30 | measured |
| 2 | Seville | 103.05 | 170,545 | 44 | 12 | 2 | - | 30 | measured |
| 3 | Palermo | 64.61 | 124,310 | 27 | 13 | 3 | 38 | 30 | measured |
| 4 | Tokyo | 70.33 | 394,702 | 22 | 16 | 1 | 5 | 100 | measured |
| 5 | Berlin | 76.88 | 412,181 | 63 | 51 | 5 | 195 | 60 | measured |
| 6 | Singapore | 64.61 | 967,821 | 34 | 7 | 3 | 165 | 100 | measured |
| 7 | Tenerife | 56.43 | - | 9 | 6 | - | - | 30 | measured |
| 8 | San Francisco | 44.16 | 361,111 | 12 | 3 | 1 | 26 | 30 | measured |
| 9 | New York | 58.88 | 1,124,326 | 98 | 10 | 8 | - | 100 | measured |
| 10 | Malaga | 43.34 | 117,780 | 10 | 5 | 1 | - | 30 | measured |
| 11 | Munich | 42.53 | 224,067 | 63 | 35 | 8 | 74 | 60 | measured |
| 12 | Paris | 41.71 | 524,268 | 58 | 15 | 8 | 129 | 60 | measured |
| 13 | Amsterdam | 30.26 | 294,030 | 27 | 7 | 2 | 5488 | 30 | measured |
| 14 | Kyoto | 33.53 | 142,353 | 18 | 14 | 2 | - | 60 | measured |
| 15 | Fukuoka | 33.53 | 77,485 | 18 | 11 | 1 | - | 60 | measured |
| 16 | Copenhagen | 46.62 | 218,621 | 49 | 41 | 6 | - | 30 | measured |
| 17 | Austin | 45.80 | 226,631 | 12 | 5 | 1 | - | 30 | measured |
| 18 | Porto | 22.90 | 120,415 | 32 | 16 | 3 | 40 | 30 | measured |
| 19 | London | 37.62 | 718,291 | 48 | 37 | 1 | - | 100 | measured |
| 20 | Alicante | 22.08 | 77,454 | 21 | 4 | 2 | 44 | 30 | measured |
| 21 | Monterey | 44.16 | - | 3 | 2 | - | - | 10 | measured |
| 22 | Rome | 22.08 | 358,876 | 32 | 10 | 2 | 31 | 60 | measured |
| 23 | Brisbane | 28.62 | 162,602 | 20 | 5 | 2 | 186 | 60 | measured |
| 24 | Venice | 22.90 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 25 | Oahu | 39.26 | - | 32 | 8 | 4 | - | 30 | measured |
| 26 | Birmingham | 37.53 | - | - | - | - | - | 60 | predicted (travel demand) |
| 27 | Dublin | 20.45 | 240,850 | 19 | 4 | 2 | 12 | 30 | measured |
| 28 | Milan | 17.17 | 212,705 | 30 | 14 | 3 | 25 | 60 | measured |
| 29 | Barcelona | 16.36 | 346,477 | 58 | 20 | 7 | 177 | 60 | measured |
| 30 | Los Angeles | 31.08 | 665,559 | 19 | 3 | 1 | - | 60 | measured |
| 31 | Seoul | 28.62 | 206,265 | 8 | 5 | 1 | - | 100 | measured |
| 32 | Coimbra | 16.36 | 34,962 | 6 | - | - | 5 | 20 | measured |
| 33 | Charleston | 27.81 | 155,987 | 4 | 1 | - | - | 20 | measured |
| 34 | Kanazawa | 17.99 | 25,778 | 7 | 3 | 1 | 2 | 30 | measured |
| 35 | Cambridge | 26.99 | 97,974 | 10 | 2 | 1 | - | 20 | measured |
| 36 | Prague | 17.99 | 303,350 | 30 | 21 | 4 | 31 | 60 | measured |
| 37 | Madrid | 16.36 | 274,553 | 18 | 11 | 2 | - | 60 | measured |
| 38 | Florence | 13.09 | 184,099 | 29 | 9 | 1 | 27 | 30 | measured |
| 39 | Reykjavik | 22.90 | 166,789 | 4 | 3 | 1 | - | 20 | measured |
| 40 | Seattle | 24.53 | 398,724 | 30 | 3 | 4 | - | 30 | measured |
| 41 | Boston | 22.90 | 385,902 | 40 | 3 | 4 | - | 30 | measured |
| 42 | Athens | 22.08 | 235,429 | 12 | 7 | 2 | - | 30 | measured |
| 43 | Philadelphia | 21.26 | 405,294 | 9 | 1 | - | - | 60 | measured |
| 44 | Portland | 14.72 | 217,222 | 33 | 2 | 3 | 306 | 30 | measured |
| 45 | Long Beach | 20.48 | - | - | - | - | - | 30 | predicted (travel demand) |
| 46 | Little Rock | 20.40 | - | - | - | - | - | 20 | predicted (travel demand) |
| 47 | Luxembourg City | 13.09 | 64,851 | 10 | 8 | 2 | 18 | 20 | measured |
| 48 | Naples | 9.81 | 198,913 | 31 | 5 | 3 | 47 | 30 | measured |
| 49 | The Hague | 9.81 | 236,723 | 26 | 4 | 5 | 166 | 30 | measured |
| 50 | Edinburgh | 18.81 | 292,981 | 21 | 10 | 1 | - | 30 | measured |
| 51 | Perth | 17.99 | 180,478 | 6 | 4 | 1 | - | 60 | measured |
| 52 | Reno | 18.19 | - | - | - | - | - | 30 | predicted (travel demand) |
| 53 | Des Moines | 18.11 | - | - | - | - | - | 20 | predicted (travel demand) |
| 54 | Sardinia | 9.81 | - | 7 | 6 | - | 10 | 60 | measured |
| 55 | Valencia | 9.00 | 162,209 | 31 | 4 | 2 | 350 | 30 | measured |
| 56 | New Orleans | 17.99 | 256,232 | 8 | 6 | 1 | - | 30 | measured |
| 57 | Daytona Beach | 17.66 | - | - | - | - | - | 20 | predicted (travel demand) |
| 58 | Krakow | 11.45 | 140,824 | 38 | 11 | 3 | 198 | 30 | measured |
| 59 | Montreal | 17.17 | 315,322 | 14 | 2 | 2 | - | 60 | measured |
| 60 | Bologna | 9.00 | 146,161 | 12 | 7 | 1 | 9 | 30 | measured |
| 61 | Cagliari | 9.00 | 51,351 | 14 | 1 | 2 | 14 | 20 | measured |
| 62 | Leeuwarden | 8.18 | - | 34 | - | 2 | 61 | 20 | measured |
| 63 | Santa Cruz | 16.06 | - | 2 | - | - | - | 10 | predicted (travel demand) |
| 64 | Melbourne | 10.63 | 267,898 | 16 | 1 | 2 | 403 | 100 | measured |
| 65 | Huntsville | 15.35 | - | - | - | - | - | 20 | predicted (travel demand) |
| 66 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 67 | West Palm Beach | 14.98 | - | - | - | - | - | 20 | predicted (travel demand) |
| 68 | Madeira | 9.00 | - | 11 | 2 | 1 | - | 30 | measured |
| 69 | Saint Petersburg | 14.83 | - | - | - | - | - | 100 | predicted (travel demand) |
| 70 | Amersfoort | 7.36 | - | 21 | 1 | 2 | 181 | 20 | measured |
| 71 | Antwerp | 14.72 | 128,289 | 10 | 4 | 1 | - | 30 | measured |
| 72 | Bath | 14.72 | 144,950 | 9 | 2 | 2 | - | 20 | measured |
| 73 | Dallas | 14.72 | - | 12 | 2 | 1 | - | 60 | measured |
| 74 | San Diego | 14.72 | 214,939 | 13 | 1 | 2 | - | 60 | measured |
| 75 | Utrecht | 7.36 | 67,963 | 30 | 9 | 2 | 339 | 30 | measured |
| 76 | Brussels | 9.81 | 176,863 | 35 | 4 | 2 | 436 | 60 | measured |
| 77 | Osaka | 9.00 | 163,112 | 6 | 1 | - | - | 60 | measured |
| 78 | Trieste | 6.54 | 117,233 | 36 | 1 | 3 | 43 | 20 | measured |
| 79 | Lansing | 13.02 | - | 2 | - | - | - | 20 | predicted (travel demand) |
| 80 | Cadiz | 8.18 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 81 | Washington DC | 11.45 | 606,731 | 34 | 8 | 4 | - | 30 | measured |
| 82 | Detroit | 12.53 | - | - | - | - | - | 30 | predicted (travel demand) |
| 83 | Toronto | 12.27 | 411,011 | 6 | - | - | - | 60 | measured |
| 84 | Geneva | 8.18 | 162,269 | 21 | 6 | 4 | 131 | 20 | measured |
| 85 | Palma de Mallorca | 7.36 | 84,075 | 6 | 2 | 1 | 8 | 30 | measured |
| 86 | Zurich | 11.45 | 140,788 | 6 | 2 | - | - | 30 | measured |
| 87 | Segovia | 7.36 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 88 | Bristol | 11.45 | 163,983 | 22 | 2 | 2 | - | 30 | measured |
| 89 | Leiden | 5.72 | 33,227 | 19 | 6 | 1 | 129 | 20 | measured |
| 90 | Sacramento | 11.32 | - | 2 | - | - | - | 30 | predicted (travel demand) |
| 91 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 60 | predicted (travel demand) |
| 92 | Christchurch | 7.36 | 104,874 | 6 | 2 | 1 | 466 | 30 | measured |
| 93 | Leipzig | 7.36 | 121,319 | 29 | 24 | 4 | - | 30 | measured |
| 94 | Sapporo | 7.36 | 88,633 | 6 | 1 | - | - | 60 | measured |
| 95 | Vienna | 7.36 | 283,090 | 61 | 25 | 6 | 358 | 60 | measured |
| 96 | Dubai | 11.02 | 334,167 | - | - | - | - | 60 | predicted (travel demand) |
| 97 | Jersey City | 10.08 | - | - | - | - | - | 30 | predicted (travel demand) |
| 98 | Hong Kong | 6.95 | 689,212 | 21 | 6 | 2 | 505 | 100 | measured |
| 99 | Genoa | 5.72 | 145,206 | 13 | 2 | 1 | 10 | 30 | measured |
| 100 | Stuttgart | 9.00 | 112,789 | 11 | 7 | - | - | 30 | measured |
| 101 | Anchorage | 10.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 102 | Freiburg | 9.81 | 92,752 | 8 | 4 | 1 | - | 20 | measured |
| 103 | Raleigh | 10.07 | - | - | - | - | - | 30 | predicted (travel demand) |
| 104 | Arnhem | 4.91 | 31,478 | 32 | 3 | 3 | 202 | 20 | measured |
| 105 | Rotterdam | 4.91 | 104,938 | 17 | 1 | 2 | 83 | 30 | measured |
| 106 | Hawaii | 9.81 | - | 8 | - | 1 | - | 60 | measured |
| 107 | Hiroshima | 6.54 | 129,791 | 33 | 5 | 2 | - | 60 | measured |
| 108 | Kauai | 9.81 | - | 9 | 2 | 1 | - | 20 | measured |
| 109 | Las Vegas | 9.81 | - | 11 | 6 | 2 | - | 30 | measured |
| 110 | Ottawa | 6.54 | - | 21 | - | 3 | 122 | 60 | measured |
| 111 | Vilnius | 6.54 | 113,188 | 12 | 4 | 1 | 34 | 30 | measured |
| 112 | Cleveland | 9.76 | - | 5 | - | 1 | - | 30 | predicted (travel demand) |
| 113 | El Paso | 9.70 | - | - | - | - | - | 30 | predicted (travel demand) |
| 114 | Chicago | 8.18 | 485,769 | 46 | 2 | 5 | 9 | 60 | measured |
| 115 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 116 | Hamburg | 9.00 | 191,221 | 6 | 4 | 1 | - | 60 | measured |
| 117 | Edmonton | 9.38 | - | - | - | - | - | 60 | predicted (travel demand) |
| 118 | Winnipeg | 9.21 | - | - | - | - | - | 30 | predicted (travel demand) |
| 119 | Granada | 5.72 | 86,361 | 11 | 4 | 2 | 4 | 20 | measured |
| 120 | Ibiza | 5.72 | - | 1 | - | - | 4 | 20 | measured |
| 121 | Spokane | 6.54 | - | 18 | - | 2 | 18 | 20 | measured |
| 122 | Tampere | 8.78 | - | - | - | - | - | 30 | predicted (travel demand) |
| 123 | Cork | 5.72 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 124 | Ann Arbor | 8.55 | - | 3 | - | 1 | - | 20 | predicted (travel demand) |
| 125 | Budapest | 8.18 | 283,807 | 13 | 2 | 3 | - | 60 | measured |
| 126 | Catania | 4.91 | 58,252 | 4 | 3 | 1 | 5 | 30 | measured |
| 127 | Adelaide | 8.14 | 139,166 | - | - | - | - | 60 | predicted (travel demand) |
| 128 | Alkmaar | 4.09 | - | 11 | - | 2 | 79 | 20 | measured |
| 129 | Caserta | 4.09 | 14,783 | 24 | - | 1 | 51 | 20 | measured |
| 130 | Eindhoven | 4.09 | - | 17 | - | 3 | 195 | 20 | measured |
| 131 | Fort Worth | 8.18 | - | 26 | - | 2 | - | 30 | measured |
| 132 | Groningen | 4.09 | 31,401 | 17 | - | 2 | 76 | 20 | measured |
| 133 | Indianapolis | 8.18 | - | 5 | 1 | - | - | 30 | measured |
| 134 | Sintra | 4.09 | 46,889 | 8 | 6 | 1 | 6 | 30 | measured |
| 135 | Stockholm | 6.54 | 188,184 | 8 | 7 | - | - | 30 | measured |
| 136 | Cordoba | 4.91 | 74,675 | 17 | 2 | 2 | 3 | 30 | measured |
| 137 | Oxford | 7.36 | 111,583 | 7 | 1 | 1 | - | 20 | measured |
| 138 | Sydney | 7.36 | 305,304 | 7 | 1 | - | - | 100 | measured |
| 139 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 20 | predicted (travel demand) |
| 140 | Nagoya | 4.91 | 83,437 | 6 | 2 | - | 1 | 60 | measured |
| 141 | Oslo | 6.54 | 181,113 | 4 | 3 | - | - | 30 | measured |
| 142 | Gdansk | 4.91 | 4,908 | 12 | 5 | 1 | 307 | 30 | measured |
| 143 | Graz | 4.91 | 65,717 | 17 | 10 | 2 | 87 | 30 | measured |
| 144 | Bergen | 7.30 | 82,940 | - | - | - | - | 30 | predicted (travel demand) |
| 145 | Helsinki | 5.72 | 148,908 | 12 | 3 | 1 | 13 | 30 | measured |
| 146 | Ronda | 4.09 | 51,510 | 10 | 1 | - | 10 | 10 | measured |
| 147 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 20 | predicted (travel demand) |
| 148 | Siena | 4.62 | 57,436 | - | - | - | - | 20 | predicted (travel demand) |
| 149 | Ghent | 6.54 | 82,757 | 8 | 2 | 1 | - | 30 | measured |
| 150 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 20 | predicted (travel demand) |
| 151 | Frankfurt | 4.51 | 150,379 | 28 | 11 | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 152 | Zagreb | 6.42 | 122,890 | - | - | - | - | 30 | predicted (travel demand) |
| 153 | Beijing | 6.54 | 269,737 | 7 | 1 | - | - | 100 | measured |
| 154 | Boise | 6.54 | - | 4 | - | 1 | - | 20 | measured |
| 155 | Maui | 6.54 | - | 5 | 2 | - | - | 20 | measured |
| 156 | Venlo | 3.27 | - | 7 | - | 1 | 144 | 20 | measured |
| 157 | Istanbul | 5.72 | 333,027 | 14 | 4 | 1 | - | 100 | measured |
| 158 | Bogota | 6.39 | 1,623 | - | - | - | - | 100 | predicted (travel demand) |
| 159 | Shanghai | 6.38 | 277,140 | - | - | - | - | 100 | predicted (travel demand) |
| 160 | Funchal | 3.77 | 174,351 | - | - | - | - | 20 | predicted (travel demand) |
| 161 | Tallinn | 4.09 | 124,888 | 9 | 3 | 2 | 42 | 30 | measured |
| 162 | Mexico City | 5.72 | 566,583 | 9 | 2 | - | - | 100 | measured |
| 163 | Belfast | 5.72 | 224,315 | 8 | 2 | 1 | - | 30 | measured |
| 164 | Cologne | 5.72 | 191,812 | 5 | - | 1 | - | 60 | measured |
| 165 | Cyprus | 5.72 | - | 15 | - | - | - | 60 | measured |
| 166 | York | 5.72 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 167 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 168 | Jacksonville | 5.69 | - | 2 | 2 | - | - | 30 | published, never ranked (may be uncrawled) |
| 169 | Girona | 3.27 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 170 | Avignon | 5.54 | 64,047 | - | - | - | - | 20 | predicted (travel demand) |
| 171 | Verona | 3.27 | 77,646 | 8 | 4 | 1 | 3 | 30 | measured |
| 172 | Galway | 3.65 | 88,162 | - | - | - | - | 20 | predicted (travel demand) |
| 173 | Phuket | 5.46 | 5,487 | - | - | - | - | 30 | predicted (travel demand) |
| 174 | Rovaniemi | 5.38 | - | - | - | - | - | 20 | predicted (travel demand) |
| 175 | Lagos | 3.43 | 34,452 | - | - | - | - | 100 | predicted (travel demand) |
| 176 | Asheville | 5.22 | - | 4 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 177 | Lund | 5.14 | - | - | - | - | - | 20 | predicted (travel demand) |
| 178 | Kobe | 3.40 | 54,798 | - | - | - | - | 60 | predicted (travel demand) |
| 179 | Fort Lauderdale | 4.61 | - | 4 | - | - | 4 | 20 | published, never ranked (may be uncrawled) |
| 180 | Aarhus | 4.91 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 181 | Heraklion | 4.96 | 66,359 | - | - | - | - | 20 | predicted (travel demand) |
| 182 | Marseille | 4.96 | 182,033 | - | - | - | - | 30 | predicted (travel demand) |
| 183 | Bordeaux | 3.27 | 156,201 | 10 | - | 2 | 211 | 30 | measured |
| 184 | Brno | 3.27 | 63,714 | 8 | 7 | 2 | 34 | 30 | measured |
| 185 | Bruges | 4.91 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 186 | Crete | 4.91 | - | 4 | 3 | - | - | 30 | measured |
| 187 | Dresden | 3.27 | 113,624 | 32 | 25 | 1 | - | 30 | measured |
| 188 | Kansas City | 4.91 | - | 4 | - | 1 | - | 30 | measured |
| 189 | Nuremberg | 3.27 | 161,614 | 20 | 8 | 2 | 37 | 30 | measured |
| 190 | Warsaw | 3.27 | 197,929 | 39 | 20 | 4 | 1407 | 60 | measured |
| 191 | Breda | 2.45 | 36,579 | 11 | 1 | 2 | 120 | 20 | measured |
| 192 | Dordrecht | 2.45 | - | 17 | 1 | 2 | 105 | 20 | measured |
| 193 | Haarlem | 2.45 | 33,960 | 21 | 2 | 2 | 277 | 20 | measured |
| 194 | Nijmegen | 2.45 | 42,338 | 20 | 1 | 3 | 159 | 20 | measured |
| 195 | Trento | 2.45 | 56,455 | 10 | 2 | 1 | 20 | 20 | measured |
| 196 | Lexington | 4.56 | - | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 197 | Guimaraes | 2.45 | 26,203 | 9 | 1 | 1 | 19 | 20 | measured |
| 198 | Oakland | 4.70 | - | 4 | 1 | - | - | 30 | published, never ranked (may be uncrawled) |
| 199 | Basel | 4.59 | 105,838 | - | - | - | - | 20 | predicted (travel demand) |
| 200 | Key West | 3.95 | - | 2 | 1 | - | 7 | 10 | published, never ranked (may be uncrawled) |
| 201 | Tasmania | 4.41 | - | - | - | - | - | 30 | predicted (travel demand) |
| 202 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 20 | predicted (travel demand) |
| 203 | Sofia | 2.81 | 138,710 | 4 | - | - | - | 60 | published, never ranked (may be uncrawled) |
| 204 | San Sebastian | 2.80 | 367 | - | - | - | - | 20 | predicted (travel demand) |
| 205 | Chattanooga | 4.17 | - | 2 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 206 | Bari | 2.45 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 207 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 30 | predicted (travel demand) |
| 208 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 209 | Salt Lake City | 2.58 | - | 20 | - | 2 | 29 | 20 | published, never ranked (may be uncrawled) |
| 210 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 211 | Niagara Falls | 3.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 212 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 100 | predicted (travel demand) |
| 213 | St. Louis | 3.70 | - | 6 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 214 | Bratislava | 2.45 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 215 | Salzburg | 2.45 | 107,243 | 21 | 12 | 3 | 33 | 20 | measured |
| 216 | Strasbourg | 2.45 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 217 | Wellington | 3.60 | 132,267 | - | - | - | - | 20 | predicted (travel demand) |
| 218 | Tampa | 3.52 | - | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 219 | Montpellier | 3.47 | 64,238 | - | - | - | - | 30 | predicted (travel demand) |
| 220 | Cape Town | 3.29 | 199,169 | - | - | - | - | 60 | predicted (travel demand) |
| 221 | Rhodes | 3.42 | 127,205 | - | - | - | - | 20 | predicted (travel demand) |
| 222 | Glasgow | 3.27 | 253,705 | 10 | 6 | - | - | 30 | measured |
| 223 | Cincinnati | 3.33 | - | 8 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 224 | San Antonio | 3.32 | - | 5 | 1 | 1 | - | 60 | published, never ranked (may be uncrawled) |
| 225 | Chania | 3.30 | 47,379 | - | - | - | - | 20 | predicted (travel demand) |
| 226 | Bergamo | 1.64 | 52,933 | 9 | 2 | 1 | 17 | 20 | measured |
| 227 | Enschede | 1.64 | - | 13 | 1 | 1 | 82 | 20 | measured |
| 228 | Helmond | 1.64 | - | 19 | - | 2 | 54 | 20 | measured |
| 229 | Hilversum | 1.64 | - | 6 | 1 | 1 | 122 | 20 | measured |
| 230 | Sorrento | 1.64 | 40,049 | 7 | - | 1 | 20 | 10 | measured |
| 231 | Brighton | 3.27 | 114,108 | 9 | 3 | 1 | - | 20 | measured |
| 232 | Houston | 3.27 | - | 12 | - | 1 | - | 60 | measured |
| 233 | Rio de Janeiro | 3.27 | 279,431 | 6 | - | - | - | 100 | measured |
| 234 | Savannah | 3.27 | 128,162 | 3 | 1 | - | - | 20 | measured |
| 235 | Santiago | 3.25 | 111,647 | - | - | - | - | 100 | predicted (travel demand) |
| 236 | Tulsa | 3.01 | - | 1 | - | - | 3 | 30 | published, never ranked (may be uncrawled) |
| 237 | Bangkok | 2.86 | 222,206 | 6 | 1 | 1 | 5 | 100 | measured |
| 238 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 30 | predicted (travel demand) |
| 239 | Lucerne | 3.10 | 66,356 | - | - | - | - | 20 | predicted (travel demand) |
| 240 | Miami | 2.37 | 278,558 | 11 | 1 | - | 15 | 30 | published, never ranked (may be uncrawled) |
| 241 | Malmo | 3.07 | 103,940 | - | - | - | - | 30 | predicted (travel demand) |
| 242 | Lille | 3.06 | 73,435 | - | - | - | - | 20 | predicted (travel demand) |
| 243 | Padua | 1.64 | 54,592 | 14 | 8 | 1 | 12 | 20 | measured |
| 244 | Corsica | 3.00 | - | - | - | - | - | 30 | predicted (travel demand) |
| 245 | Mechelen | 2.93 | 20,707 | - | - | - | - | 20 | predicted (travel demand) |
| 246 | Turin | 1.49 | 147,456 | 11 | 10 | 2 | 30 | 30 | published, never ranked (may be uncrawled) |
| 247 | Sao Paulo | 2.86 | 911 | 1 | - | - | - | 100 | measured |
| 248 | Chiang Mai | 2.85 | 66,541 | 1 | - | - | 2 | 60 | published, never ranked (may be uncrawled) |
| 249 | Parma | 1.64 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 250 | Denver | 2.91 | - | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 251 | Belgrade | 2.86 | 178,116 | 5 | 5 | - | - | 60 | measured |
| 252 | San Jose | 2.85 | - | 2 | - | - | - | 60 | published, never ranked (may be uncrawled) |
| 253 | Poznan | 1.89 | 65,666 | 10 | - | 1 | 397 | 30 | published, never ranked (may be uncrawled) |
| 254 | Tarragona | 1.64 | 32,396 | 3 | 1 | - | - | 20 | measured |
| 255 | Milwaukee | 2.66 | - | 6 | - | 1 | 2 | 30 | published, never ranked (may be uncrawled) |
| 256 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 257 | Syracuse | 1.75 | 102,833 | - | - | - | - | 20 | predicted (travel demand) |
| 258 | Cartagena | 2.58 | 65,066 | - | - | - | - | 30 | predicted (travel demand) |
| 259 | Atlanta | 2.57 | - | 11 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 260 | Bern | 2.51 | 90,627 | - | - | - | - | 20 | predicted (travel demand) |
| 261 | Busan | 2.45 | 94,737 | 2 | - | - | - | 60 | measured |
| 262 | Vancouver | 2.45 | 351,552 | 7 | - | - | - | 30 | measured |
| 263 | Bali | 2.49 | - | 5 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 264 | Bilbao | 1.64 | 133,133 | 4 | 1 | 1 | - | 30 | measured |
| 265 | Hobart | 1.64 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 266 | Lyon | 1.64 | 136,951 | 34 | 4 | 6 | 178 | 30 | measured |
| 267 | Potsdam | 1.64 | 51,727 | 18 | 8 | 3 | 16 | 20 | measured |
| 268 | Wroclaw | 1.64 | 123,894 | 5 | 2 | 1 | 121 | 30 | measured |
| 269 | Nice | 2.45 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 270 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 271 | Faro | 1.62 | 55,645 | - | - | - | - | 20 | predicted (travel demand) |
| 272 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 273 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 274 | Cusco | 2.35 | 87,732 | - | - | - | - | 30 | predicted (travel demand) |
| 275 | Limerick | 1.57 | 90,379 | - | - | - | - | 20 | predicted (travel demand) |
| 276 | Trier | 1.56 | 69,369 | - | - | - | 154 | 20 | predicted (travel demand) |
| 277 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 20 | predicted (travel demand) |
| 278 | Pisa | 1.46 | 52,174 | 4 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 279 | Nashville | 2.23 | - | 8 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 280 | Hanoi | 2.15 | 117,396 | 2 | - | - | - | 100 | published, never ranked (may be uncrawled) |
| 281 | Taipei | 2.09 | 143,193 | 4 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 282 | Salamanca | 1.37 | 47,897 | 4 | 1 | 1 | 1 | 20 | published, never ranked (may be uncrawled) |
| 283 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 284 | Tilburg | 1.03 | - | 17 | - | 3 | 86 | 20 | published, never ranked (may be uncrawled) |
| 285 | Ischia | 1.32 | - | - | - | - | 2 | 20 | predicted (travel demand) |
| 286 | Albuquerque | 1.96 | - | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 287 | Izmir | 1.88 | 69,826 | - | - | - | - | 60 | predicted (travel demand) |
| 288 | Minneapolis | 1.88 | - | 4 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 289 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 290 | Baltimore | 1.77 | - | 4 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 291 | Auckland | 1.17 | 152,056 | 5 | 2 | - | 977 | 60 | published, never ranked (may be uncrawled) |
| 292 | Dijon | 1.72 | 43,526 | - | - | - | - | 20 | predicted (travel demand) |
| 293 | Annecy | 1.69 | 56,859 | - | - | - | - | 20 | predicted (travel demand) |
| 294 | Ljubljana | 1.64 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 295 | Pittsburgh | 1.64 | - | 12 | - | 1 | - | 30 | measured |
| 296 | Apeldoorn | 0.82 | - | 8 | - | 2 | 80 | 20 | measured |
| 297 | Como | 0.82 | 82,645 | 9 | 3 | 1 | 23 | 20 | measured |
| 298 | Delft | 0.82 | 31,293 | 12 | - | 1 | 60 | 20 | measured |
| 299 | Deventer | 0.82 | - | 12 | - | 1 | 213 | 20 | measured |
| 300 | Hilo | 1.64 | - | 9 | - | 2 | - | 10 | measured |
| 301 | Leuven | 1.64 | 40,645 | 4 | - | - | - | 20 | measured |
| 302 | Liverpool | 1.64 | 248,189 | 4 | 3 | - | - | 30 | measured |
| 303 | Lucca | 0.82 | 52,271 | 16 | 4 | 1 | 27 | 20 | measured |
| 304 | Maastricht | 0.82 | 47,763 | 16 | - | 2 | 135 | 20 | measured |
| 305 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 306 | Roosendaal | 0.82 | - | 20 | - | 2 | 138 | 20 | measured |
| 307 | Mostar | 1.58 | 63,907 | - | - | - | - | 20 | predicted (travel demand) |
| 308 | Perugia | 0.82 | 42,572 | 16 | 1 | 2 | 19 | 20 | measured |
| 309 | Quebec City | 1.01 | 124,358 | 6 | - | 1 | 494 | 30 | published, never ranked (may be uncrawled) |
| 310 | Gothenburg | 1.49 | 119,991 | 5 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 311 | Setubal | 0.82 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 312 | Braga | 0.82 | 34,522 | 4 | 2 | - | 8 | 20 | measured |
| 313 | Malta | 1.45 | - | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 314 | Ferrara | 0.82 | 27,490 | 5 | 3 | 1 | 7 | 20 | measured |
| 315 | Matera | 0.82 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 316 | Pamplona | 0.82 | 128,065 | 25 | - | 3 | 9 | 20 | measured |
| 317 | Antalya | 1.31 | 70,688 | - | - | - | - | 60 | predicted (travel demand) |
| 318 | Cardiff | 1.27 | - | 12 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 319 | Yakushima | 0.82 | - | 2 | 2 | - | 1 | 10 | measured |
| 320 | Santa Fe | 1.29 | - | 3 | - | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 321 | Colmar | 1.28 | 45,517 | - | - | - | - | 20 | predicted (travel demand) |
| 322 | Bodrum | 1.26 | 33,918 | - | - | - | - | 20 | predicted (travel demand) |
| 323 | Menorca | 0.82 | - | 6 | - | - | 2 | 20 | measured |
| 324 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 325 | Canberra | 0.82 | - | 8 | 1 | 1 | 132 | 30 | measured |
| 326 | Cesky Krumlov | 0.82 | 28,582 | 6 | 3 | - | 11 | 10 | measured |
| 327 | Lausanne | 1.23 | 68,242 | 8 | 1 | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 328 | Toulouse | 0.82 | 112,721 | 10 | - | 1 | 34 | 30 | measured |
| 329 | Evora | 0.78 | 15,345 | - | - | - | - | 20 | predicted (travel demand) |
| 330 | Zaragoza | 0.73 | 87,580 | 7 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 331 | Okinawa | 0.71 | 24,466 | 6 | - | - | 1 | 30 | published, never ranked (may be uncrawled) |
| 332 | Dubrovnik | 0.99 | 119,586 | 4 | 4 | - | 2 | 10 | published, never ranked (may be uncrawled) |
| 333 | Split | 0.97 | 132,399 | 5 | - | 1 | 2 | 20 | published, never ranked (may be uncrawled) |
| 334 | Azores | 0.65 | - | 7 | 2 | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 335 | Rothenburg ob der Tauber | 0.82 | 39,879 | 5 | 1 | 1 | 8 | 10 | measured |
| 336 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 60 | predicted (travel demand) |
| 337 | Innsbruck | 0.63 | 58,742 | 6 | 2 | 1 | 39 | 20 | published, never ranked (may be uncrawled) |
| 338 | Heidelberg | 0.82 | 75,837 | 7 | 1 | 1 | - | 20 | measured |
| 339 | Kotor | 0.86 | 48,982 | 1 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 340 | Buenos Aires | 0.82 | 333,331 | 4 | 2 | - | - | 60 | measured |
| 341 | Riga | 0.82 | 108,918 | 5 | 2 | - | - | 30 | measured |
| 342 | Bucharest | 0.82 | 136,836 | 4 | - | 1 | - | 60 | measured |
| 343 | Manchester | 0.82 | 316,438 | 5 | 1 | - | - | 30 | measured |
| 344 | Nantes | 0.82 | 67,689 | 1 | 1 | - | - | 30 | measured |
| 345 | Thessaloniki | 0.82 | 180,145 | 4 | - | 1 | - | 30 | measured |
| 346 | Turku | 0.82 | - | 1 | 1 | - | - | 20 | measured |
| 347 | Kandy | 0.78 | 24,159 | 1 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 348 | Modena | 0.44 | 51,698 | 5 | 1 | 1 | 3 | 20 | published, never ranked (may be uncrawled) |
| 349 | Den Bosch | 0.36 | 39,682 | 11 | 2 | 1 | 118 | 20 | published, never ranked (may be uncrawled) |
| 350 | Assen | 0.35 | - | 9 | - | 2 | 66 | 20 | published, never ranked (may be uncrawled) |
| 351 | Heerlen | 0.35 | - | 8 | 1 | 2 | 53 | 20 | published, never ranked (may be uncrawled) |
| 352 | Kamakura | 0.44 | 33,492 | 6 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 353 | Zwolle | 0.35 | - | 15 | - | 3 | 58 | 20 | published, never ranked (may be uncrawled) |
| 354 | Inverness | 0.69 | 92,195 | 1 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 355 | Corfu | 0.68 | 139,334 | 8 | - | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 356 | Gran Canaria | 0.42 | - | 10 | 4 | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 357 | Hallstatt | 0.50 | 47,271 | 7 | 4 | - | 4 | 10 | published, never ranked (may be uncrawled) |
| 358 | Hoorn | 0.30 | - | 12 | - | 2 | 52 | 20 | published, never ranked (may be uncrawled) |
| 359 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 100 | published, never ranked (may be uncrawled) |
| 360 | Rouen | 0.54 | 72,334 | 12 | - | 1 | 6 | 20 | published, never ranked (may be uncrawled) |
| 361 | Phoenix | 0.55 | - | - | - | - | - | 60 | predicted (travel demand) |
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

