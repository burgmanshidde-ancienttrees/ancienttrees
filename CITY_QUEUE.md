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
| 1 | Lisbon | 89.30 | 201,877 | 37 | 22 | 3 | 67 | 30 | measured |
| 2 | Seville | 103.76 | 170,545 | 44 | 12 | 2 | - | 30 | measured |
| 3 | Palermo | 62.09 | 124,310 | 27 | 13 | 3 | 38 | 30 | measured |
| 4 | Berlin | 78.25 | 412,181 | 63 | 51 | 5 | 195 | 60 | measured |
| 5 | Tokyo | 61.24 | 394,702 | 22 | 16 | 1 | 5 | 100 | measured |
| 6 | Singapore | 58.68 | 967,821 | 34 | 7 | 3 | 165 | 100 | measured |
| 7 | Tenerife | 55.28 | - | 9 | 6 | - | - | 30 | measured |
| 8 | San Francisco | 45.93 | 361,111 | 12 | 3 | 1 | 26 | 30 | measured |
| 9 | Munich | 44.23 | 224,067 | 63 | 35 | 8 | 74 | 60 | measured |
| 10 | Malaga | 43.38 | 117,780 | 10 | 5 | 1 | - | 30 | measured |
| 11 | Amsterdam | 31.47 | 294,030 | 27 | 7 | 2 | 5488 | 30 | measured |
| 12 | New York | 56.13 | 1,124,326 | 98 | 10 | 8 | - | 100 | measured |
| 13 | Paris | 40.82 | 524,268 | 58 | 15 | 8 | 129 | 60 | measured |
| 14 | Fukuoka | 32.32 | 77,485 | 18 | 11 | 1 | - | 60 | measured |
| 15 | Porto | 24.66 | 120,415 | 32 | 16 | 3 | 40 | 30 | measured |
| 16 | Copenhagen | 45.93 | 218,621 | 49 | 41 | 6 | - | 30 | measured |
| 17 | Kyoto | 29.77 | 142,353 | 18 | 14 | 2 | - | 60 | measured |
| 18 | London | 39.12 | 718,291 | 48 | 37 | 1 | - | 100 | measured |
| 19 | Alicante | 22.96 | 77,454 | 21 | 4 | 2 | 44 | 30 | measured |
| 20 | Rome | 22.11 | 358,876 | 32 | 10 | 2 | 31 | 60 | measured |
| 21 | Brisbane | 28.07 | 162,602 | 20 | 5 | 2 | 186 | 60 | measured |
| 22 | Venice | 22.96 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 23 | Austin | 39.12 | 226,631 | 12 | 5 | 1 | - | 30 | measured |
| 24 | Monterey | 39.12 | - | 3 | 2 | - | - | 10 | measured |
| 25 | Birmingham | 37.53 | - | - | - | - | - | 60 | predicted (travel demand) |
| 26 | Dublin | 21.26 | 240,850 | 19 | 4 | 2 | 12 | 30 | measured |
| 27 | Milan | 17.86 | 212,705 | 30 | 14 | 3 | 25 | 60 | measured |
| 28 | Barcelona | 17.01 | 346,477 | 58 | 20 | 7 | 177 | 60 | measured |
| 29 | Oahu | 34.02 | - | 32 | 8 | 4 | - | 30 | measured |
| 30 | Los Angeles | 30.62 | 665,559 | 19 | 3 | 1 | - | 60 | measured |
| 31 | Charleston | 28.92 | 155,987 | 4 | 1 | - | - | 20 | measured |
| 32 | Seoul | 26.37 | 206,265 | 8 | 5 | 1 | - | 100 | measured |
| 33 | Reykjavik | 23.81 | 166,789 | 4 | 3 | 1 | - | 20 | measured |
| 34 | Prague | 17.86 | 303,350 | 30 | 21 | 4 | 31 | 60 | measured |
| 35 | Seattle | 25.51 | 398,724 | 30 | 3 | 4 | - | 30 | measured |
| 36 | Coimbra | 14.46 | 34,962 | 6 | - | - | 5 | 20 | measured |
| 37 | Cambridge | 25.52 | 97,974 | 10 | 2 | 1 | - | 20 | measured |
| 38 | Florence | 11.91 | 184,099 | 29 | 9 | 1 | 27 | 30 | measured |
| 39 | Philadelphia | 22.11 | 405,294 | 9 | 1 | - | - | 60 | measured |
| 40 | Kanazawa | 14.46 | 25,778 | 7 | 3 | 1 | 2 | 30 | measured |
| 41 | Athens | 21.26 | 235,429 | 12 | 7 | 2 | - | 30 | measured |
| 42 | Boston | 20.41 | 385,902 | 40 | 3 | 4 | - | 30 | measured |
| 43 | Madrid | 12.76 | 274,553 | 18 | 11 | 2 | - | 60 | measured |
| 44 | Long Beach | 20.48 | - | - | - | - | - | 30 | predicted (travel demand) |
| 45 | Naples | 10.21 | 198,913 | 31 | 5 | 3 | 47 | 30 | measured |
| 46 | The Hague | 10.21 | 236,723 | 26 | 4 | 5 | 166 | 30 | measured |
| 47 | Luxembourg City | 13.61 | 64,851 | 10 | 8 | 2 | 18 | 20 | measured |
| 48 | Little Rock | 20.40 | - | - | - | - | - | 20 | predicted (travel demand) |
| 49 | Edinburgh | 18.71 | 292,981 | 21 | 10 | 1 | - | 30 | measured |
| 50 | Perth | 18.71 | 180,478 | 6 | 4 | 1 | - | 60 | measured |
| 51 | Sardinia | 10.21 | - | 7 | 6 | - | 10 | 60 | measured |
| 52 | Valencia | 9.36 | 162,209 | 31 | 4 | 2 | 350 | 30 | measured |
| 53 | New Orleans | 18.71 | 256,232 | 8 | 6 | 1 | - | 30 | measured |
| 54 | Reno | 18.19 | - | - | - | - | - | 30 | predicted (travel demand) |
| 55 | Des Moines | 18.11 | - | - | - | - | - | 20 | predicted (travel demand) |
| 56 | Daytona Beach | 17.66 | - | - | - | - | - | 20 | predicted (travel demand) |
| 57 | Cagliari | 9.36 | 51,351 | 14 | 1 | 2 | 14 | 20 | measured |
| 58 | Leeuwarden | 8.50 | - | 34 | - | 2 | 61 | 20 | measured |
| 59 | Krakow | 11.06 | 140,824 | 38 | 11 | 3 | 198 | 30 | measured |
| 60 | Montreal | 16.16 | 315,322 | 14 | 2 | 2 | - | 60 | measured |
| 61 | Bologna | 8.50 | 146,161 | 12 | 7 | 1 | 9 | 30 | measured |
| 62 | Madeira | 9.36 | - | 11 | 2 | 1 | - | 30 | measured |
| 63 | Huntsville | 15.35 | - | - | - | - | - | 20 | predicted (travel demand) |
| 64 | Brussels | 10.21 | 176,863 | 35 | 4 | 2 | 436 | 60 | measured |
| 65 | Melbourne | 10.21 | 267,898 | 16 | 1 | 2 | 403 | 100 | measured |
| 66 | Portland | 10.21 | 217,222 | 33 | 2 | 3 | 306 | 30 | measured |
| 67 | Dallas | 15.31 | - | 12 | 2 | 1 | - | 60 | measured |
| 68 | San Diego | 15.31 | 214,939 | 13 | 1 | 2 | - | 60 | measured |
| 69 | Amersfoort | 7.65 | - | 21 | 1 | 2 | 181 | 20 | measured |
| 70 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 71 | West Palm Beach | 14.98 | - | - | - | - | - | 20 | predicted (travel demand) |
| 72 | Saint Petersburg | 14.83 | - | - | - | - | - | 100 | predicted (travel demand) |
| 73 | Osaka | 9.36 | 163,112 | 6 | 1 | - | - | 60 | measured |
| 74 | Antwerp | 14.46 | 128,289 | 10 | 4 | 1 | - | 30 | measured |
| 75 | Bath | 13.61 | 144,950 | 9 | 2 | 2 | - | 20 | measured |
| 76 | Leiden | 6.80 | 33,227 | 19 | 6 | 1 | 129 | 20 | measured |
| 77 | Trieste | 6.80 | 117,233 | 36 | 1 | 3 | 43 | 20 | measured |
| 78 | Utrecht | 6.80 | 67,963 | 30 | 9 | 2 | 339 | 30 | measured |
| 79 | Toronto | 12.76 | 411,011 | 6 | - | - | - | 60 | measured |
| 80 | Geneva | 8.50 | 162,269 | 21 | 6 | 4 | 131 | 20 | measured |
| 81 | Palma de Mallorca | 7.65 | 84,075 | 6 | 2 | 1 | 8 | 30 | measured |
| 82 | Detroit | 12.53 | - | - | - | - | - | 30 | predicted (travel demand) |
| 83 | Zurich | 11.91 | 140,788 | 6 | 2 | - | - | 30 | measured |
| 84 | Segovia | 7.65 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 85 | Cadiz | 7.65 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 86 | Leipzig | 7.65 | 121,319 | 29 | 24 | 4 | - | 30 | measured |
| 87 | Vilnius | 7.65 | 113,188 | 12 | 4 | 1 | 34 | 30 | measured |
| 88 | Washington DC | 10.21 | 606,731 | 34 | 8 | 4 | - | 30 | measured |
| 89 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 60 | predicted (travel demand) |
| 90 | Bristol | 11.06 | 163,983 | 22 | 2 | 2 | - | 30 | measured |
| 91 | Dubai | 11.02 | 334,167 | - | - | - | - | 60 | predicted (travel demand) |
| 92 | Genoa | 5.95 | 145,206 | 13 | 2 | 1 | 10 | 30 | measured |
| 93 | Stuttgart | 9.36 | 112,789 | 11 | 7 | - | - | 30 | measured |
| 94 | Freiburg | 10.21 | 92,752 | 8 | 4 | 1 | - | 20 | measured |
| 95 | Jersey City | 10.08 | - | - | - | - | - | 30 | predicted (travel demand) |
| 96 | Anchorage | 10.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 97 | Las Vegas | 10.21 | - | 11 | 6 | 2 | - | 30 | measured |
| 98 | Arnhem | 5.10 | 31,478 | 32 | 3 | 3 | 202 | 20 | measured |
| 99 | Christchurch | 6.80 | 104,874 | 6 | 2 | 1 | 466 | 30 | measured |
| 100 | Ottawa | 6.80 | - | 21 | - | 3 | 122 | 60 | measured |
| 101 | Rotterdam | 5.10 | 104,938 | 17 | 1 | 2 | 83 | 30 | measured |
| 102 | Vienna | 6.80 | 283,090 | 61 | 25 | 6 | 358 | 60 | measured |
| 103 | Raleigh | 10.07 | - | - | - | - | - | 30 | predicted (travel demand) |
| 104 | Chicago | 8.51 | 485,769 | 46 | 2 | 5 | 9 | 60 | measured |
| 105 | Hamburg | 9.36 | 191,221 | 6 | 4 | 1 | - | 60 | measured |
| 106 | El Paso | 9.70 | - | - | - | - | - | 30 | predicted (travel demand) |
| 107 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 108 | Hong Kong | 6.38 | 689,212 | 21 | 6 | 2 | 505 | 100 | measured |
| 109 | Granada | 5.95 | 86,361 | 11 | 4 | 2 | 4 | 20 | measured |
| 110 | Ibiza | 5.95 | - | 1 | - | - | 4 | 20 | measured |
| 111 | Edmonton | 9.38 | - | - | - | - | - | 60 | predicted (travel demand) |
| 112 | Spokane | 6.80 | - | 18 | - | 2 | 18 | 20 | measured |
| 113 | Winnipeg | 9.21 | - | - | - | - | - | 30 | predicted (travel demand) |
| 114 | Sapporo | 5.95 | 88,633 | 6 | 1 | - | - | 60 | measured |
| 115 | Tampere | 8.78 | - | - | - | - | - | 30 | predicted (travel demand) |
| 116 | Catania | 5.10 | 58,252 | 4 | 3 | 1 | 5 | 30 | measured |
| 117 | Indianapolis | 8.51 | - | 5 | 1 | - | - | 30 | measured |
| 118 | Alkmaar | 4.25 | - | 11 | - | 2 | 79 | 20 | measured |
| 119 | Caserta | 4.25 | 14,783 | 24 | - | 1 | 51 | 20 | measured |
| 120 | Eindhoven | 4.25 | - | 17 | - | 3 | 195 | 20 | measured |
| 121 | Fort Worth | 8.50 | - | 26 | - | 2 | - | 30 | measured |
| 122 | Groningen | 4.25 | 31,401 | 17 | - | 2 | 76 | 20 | measured |
| 123 | Hawaii | 8.50 | - | 8 | - | 1 | - | 60 | measured |
| 124 | Kauai | 8.50 | - | 9 | 2 | 1 | - | 20 | measured |
| 125 | Sintra | 4.25 | 46,889 | 8 | 6 | 1 | 6 | 30 | measured |
| 126 | Adelaide | 8.14 | 139,166 | - | - | - | - | 60 | predicted (travel demand) |
| 127 | Budapest | 7.65 | 283,807 | 13 | 2 | 3 | - | 60 | measured |
| 128 | Cordoba | 5.10 | 74,675 | 17 | 2 | 2 | 3 | 30 | measured |
| 129 | Oxford | 7.65 | 111,583 | 7 | 1 | 1 | - | 20 | measured |
| 130 | Oslo | 6.80 | 181,113 | 4 | 3 | - | - | 30 | measured |
| 131 | Graz | 5.10 | 65,717 | 17 | 10 | 2 | 87 | 30 | measured |
| 132 | Hiroshima | 5.10 | 129,791 | 33 | 5 | 2 | - | 60 | measured |
| 133 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 20 | predicted (travel demand) |
| 134 | Ronda | 4.25 | 51,510 | 10 | 1 | - | 10 | 10 | measured |
| 135 | Bergen | 7.30 | 82,940 | - | - | - | - | 30 | predicted (travel demand) |
| 136 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 20 | predicted (travel demand) |
| 137 | Siena | 4.62 | 57,436 | - | - | - | - | 20 | predicted (travel demand) |
| 138 | Maui | 6.80 | - | 5 | 2 | - | - | 20 | measured |
| 139 | Venlo | 3.40 | - | 7 | - | 1 | 144 | 20 | measured |
| 140 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 20 | predicted (travel demand) |
| 141 | Frankfurt | 4.51 | 150,379 | 28 | 11 | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 142 | Zagreb | 6.42 | 122,890 | - | - | - | - | 30 | predicted (travel demand) |
| 143 | Helsinki | 5.10 | 148,908 | 12 | 3 | 1 | 13 | 30 | measured |
| 144 | Bogota | 6.39 | 1,623 | - | - | - | - | 100 | predicted (travel demand) |
| 145 | Beijing | 6.38 | 269,737 | 7 | 1 | - | - | 100 | measured |
| 146 | Shanghai | 6.38 | 277,140 | - | - | - | - | 100 | predicted (travel demand) |
| 147 | Tallinn | 4.25 | 124,888 | 9 | 3 | 2 | 42 | 30 | measured |
| 148 | Stockholm | 5.10 | 188,184 | 8 | 7 | - | - | 30 | measured |
| 149 | Funchal | 3.77 | 174,351 | - | - | - | - | 20 | predicted (travel demand) |
| 150 | Ghent | 5.95 | 82,757 | 8 | 2 | 1 | - | 30 | measured |
| 151 | Sydney | 5.95 | 305,304 | 7 | 1 | - | - | 100 | measured |
| 152 | Belfast | 5.95 | 224,315 | 8 | 2 | 1 | - | 30 | measured |
| 153 | Cologne | 5.95 | 191,812 | 5 | - | 1 | - | 60 | measured |
| 154 | Mexico City | 5.53 | 566,583 | 9 | 2 | - | - | 100 | measured |
| 155 | Girona | 3.40 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 156 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 157 | Verona | 3.40 | 77,646 | 8 | 4 | 1 | 3 | 30 | measured |
| 158 | Jacksonville | 5.69 | - | 2 | 2 | - | - | 30 | published, never ranked (may be uncrawled) |
| 159 | Avignon | 5.54 | 64,047 | - | - | - | - | 20 | predicted (travel demand) |
| 160 | Galway | 3.65 | 88,162 | - | - | - | - | 20 | predicted (travel demand) |
| 161 | Phuket | 5.46 | 5,487 | - | - | - | - | 30 | predicted (travel demand) |
| 162 | Rovaniemi | 5.38 | - | - | - | - | - | 20 | predicted (travel demand) |
| 163 | Lagos | 3.43 | 34,452 | - | - | - | - | 100 | predicted (travel demand) |
| 164 | Asheville | 5.22 | - | 4 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 165 | Aarhus | 5.10 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 166 | Lund | 5.14 | - | - | - | - | - | 20 | predicted (travel demand) |
| 167 | Boise | 5.10 | - | 4 | - | 1 | - | 20 | measured |
| 168 | Bordeaux | 3.40 | 156,201 | 10 | - | 2 | 211 | 30 | measured |
| 169 | Breda | 2.55 | 36,579 | 11 | 1 | 2 | 120 | 20 | measured |
| 170 | Brno | 3.40 | 63,714 | 8 | 7 | 2 | 34 | 30 | measured |
| 171 | Bruges | 5.10 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 172 | Cork | 3.40 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 173 | Crete | 5.10 | - | 4 | 3 | - | - | 30 | measured |
| 174 | Cyprus | 5.10 | - | 15 | - | - | - | 60 | measured |
| 175 | Dordrecht | 2.55 | - | 17 | 1 | 2 | 105 | 20 | measured |
| 176 | Haarlem | 2.55 | 33,960 | 21 | 2 | 2 | 277 | 20 | measured |
| 177 | Kansas City | 5.10 | - | 4 | - | 1 | - | 30 | measured |
| 178 | Kobe | 3.40 | 54,798 | - | - | - | - | 60 | predicted (travel demand) |
| 179 | Nijmegen | 2.55 | 42,338 | 20 | 1 | 3 | 159 | 20 | measured |
| 180 | Nuremberg | 3.40 | 161,614 | 20 | 8 | 2 | 37 | 30 | measured |
| 181 | Warsaw | 3.40 | 197,929 | 39 | 20 | 4 | 1407 | 60 | measured |
| 182 | York | 5.10 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 183 | Fort Lauderdale | 4.61 | - | 4 | - | - | 4 | 20 | published, never ranked (may be uncrawled) |
| 184 | Heraklion | 4.96 | 66,359 | - | - | - | - | 20 | predicted (travel demand) |
| 185 | Marseille | 4.96 | 182,033 | - | - | - | - | 30 | predicted (travel demand) |
| 186 | Guimaraes | 2.55 | 26,203 | 9 | 1 | 1 | 19 | 20 | measured |
| 187 | Istanbul | 4.25 | 333,027 | 14 | 4 | 1 | - | 100 | measured |
| 188 | Lexington | 4.56 | - | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 189 | Oakland | 4.70 | - | 4 | 1 | - | - | 30 | published, never ranked (may be uncrawled) |
| 190 | Basel | 4.59 | 105,838 | - | - | - | - | 20 | predicted (travel demand) |
| 191 | Key West | 3.95 | - | 2 | 1 | - | 7 | 10 | published, never ranked (may be uncrawled) |
| 192 | Tasmania | 4.41 | - | - | - | - | - | 30 | predicted (travel demand) |
| 193 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 20 | predicted (travel demand) |
| 194 | Bari | 2.55 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 195 | Sofia | 2.81 | 138,710 | 4 | - | - | - | 60 | published, never ranked (may be uncrawled) |
| 196 | San Sebastian | 2.80 | 367 | - | - | - | - | 20 | predicted (travel demand) |
| 197 | Chattanooga | 4.17 | - | 2 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 198 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 30 | predicted (travel demand) |
| 199 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 200 | Santa Cruz | 4.01 | - | 2 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 201 | Salt Lake City | 2.58 | - | 20 | - | 2 | 29 | 20 | published, never ranked (may be uncrawled) |
| 202 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 203 | Niagara Falls | 3.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 204 | Bratislava | 2.55 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 205 | Dresden | 2.55 | 113,624 | 32 | 25 | 1 | - | 30 | measured |
| 206 | Gdansk | 2.55 | 4,908 | 12 | 5 | 1 | 307 | 30 | measured |
| 207 | Salzburg | 2.55 | 107,243 | 21 | 12 | 3 | 33 | 20 | measured |
| 208 | Strasbourg | 2.55 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 209 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 100 | predicted (travel demand) |
| 210 | St. Louis | 3.70 | - | 6 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 211 | Wellington | 3.60 | 132,267 | - | - | - | - | 20 | predicted (travel demand) |
| 212 | Tampa | 3.52 | - | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 213 | Montpellier | 3.47 | 64,238 | - | - | - | - | 30 | predicted (travel demand) |
| 214 | Cape Town | 3.29 | 199,169 | - | - | - | - | 60 | predicted (travel demand) |
| 215 | Rhodes | 3.42 | 127,205 | - | - | - | - | 20 | predicted (travel demand) |
| 216 | Brighton | 3.40 | 114,108 | 9 | 3 | 1 | - | 20 | measured |
| 217 | Helmond | 1.70 | - | 19 | - | 2 | 54 | 20 | measured |
| 218 | Hilversum | 1.70 | - | 6 | 1 | 1 | 122 | 20 | measured |
| 219 | Houston | 3.40 | - | 12 | - | 1 | - | 60 | measured |
| 220 | Savannah | 3.40 | 128,162 | 3 | 1 | - | - | 20 | measured |
| 221 | Trento | 1.70 | 56,455 | 10 | 2 | 1 | 20 | 20 | measured |
| 222 | Cincinnati | 3.33 | - | 8 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 223 | San Antonio | 3.32 | - | 5 | 1 | 1 | - | 60 | published, never ranked (may be uncrawled) |
| 224 | Chania | 3.30 | 47,379 | - | - | - | - | 20 | predicted (travel demand) |
| 225 | Bangkok | 2.98 | 222,206 | 6 | 1 | 1 | 5 | 100 | measured |
| 226 | Lansing | 3.25 | - | 2 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 227 | Santiago | 3.25 | 111,647 | - | - | - | - | 100 | predicted (travel demand) |
| 228 | Tulsa | 3.01 | - | 1 | - | - | 3 | 30 | published, never ranked (may be uncrawled) |
| 229 | Padua | 1.70 | 54,592 | 14 | 8 | 1 | 12 | 20 | measured |
| 230 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 30 | predicted (travel demand) |
| 231 | Lucerne | 3.10 | 66,356 | - | - | - | - | 20 | predicted (travel demand) |
| 232 | Sao Paulo | 2.98 | 911 | 1 | - | - | - | 100 | measured |
| 233 | Miami | 2.37 | 278,558 | 11 | 1 | - | 15 | 30 | published, never ranked (may be uncrawled) |
| 234 | Malmo | 3.07 | 103,940 | - | - | - | - | 30 | predicted (travel demand) |
| 235 | Lille | 3.06 | 73,435 | - | - | - | - | 20 | predicted (travel demand) |
| 236 | Parma | 1.70 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 237 | Corsica | 3.00 | - | - | - | - | - | 30 | predicted (travel demand) |
| 238 | Mechelen | 2.93 | 20,707 | - | - | - | - | 20 | predicted (travel demand) |
| 239 | Rio de Janeiro | 2.98 | 279,431 | 6 | - | - | - | 100 | measured |
| 240 | Turin | 1.49 | 147,456 | 11 | 10 | 2 | 30 | 30 | published, never ranked (may be uncrawled) |
| 241 | Chiang Mai | 2.85 | 66,541 | 1 | - | - | 2 | 60 | published, never ranked (may be uncrawled) |
| 242 | Tarragona | 1.70 | 32,396 | 3 | 1 | - | - | 20 | measured |
| 243 | Denver | 2.91 | - | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 244 | San Jose | 2.85 | - | 2 | - | - | - | 60 | published, never ranked (may be uncrawled) |
| 245 | Poznan | 1.89 | 65,666 | 10 | - | 1 | 397 | 30 | published, never ranked (may be uncrawled) |
| 246 | Sacramento | 2.83 | - | 2 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 247 | Milwaukee | 2.66 | - | 6 | - | 1 | 2 | 30 | published, never ranked (may be uncrawled) |
| 248 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 249 | Syracuse | 1.75 | 102,833 | - | - | - | - | 20 | predicted (travel demand) |
| 250 | Busan | 2.55 | 94,737 | 2 | - | - | - | 60 | measured |
| 251 | Glasgow | 2.55 | 253,705 | 10 | 6 | - | - | 30 | measured |
| 252 | Cartagena | 2.58 | 65,066 | - | - | - | - | 30 | predicted (travel demand) |
| 253 | Nagoya | 1.70 | 83,437 | 6 | 2 | - | 1 | 60 | measured |
| 254 | Atlanta | 2.57 | - | 11 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 255 | Belgrade | 2.55 | 178,116 | 5 | 5 | - | - | 60 | measured |
| 256 | Bilbao | 1.70 | 133,133 | 4 | 1 | 1 | - | 30 | measured |
| 257 | Lyon | 1.70 | 136,951 | 34 | 4 | 6 | 178 | 30 | measured |
| 258 | Nice | 2.55 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 259 | Potsdam | 1.70 | 51,727 | 18 | 8 | 3 | 16 | 20 | measured |
| 260 | Wroclaw | 1.70 | 123,894 | 5 | 2 | 1 | 121 | 30 | measured |
| 261 | Bern | 2.51 | 90,627 | - | - | - | - | 20 | predicted (travel demand) |
| 262 | Bali | 2.49 | - | 5 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 263 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 264 | Cleveland | 2.44 | - | 5 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 265 | Faro | 1.62 | 55,645 | - | - | - | - | 20 | predicted (travel demand) |
| 266 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 267 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 268 | Cusco | 2.35 | 87,732 | - | - | - | - | 30 | predicted (travel demand) |
| 269 | Limerick | 1.57 | 90,379 | - | - | - | - | 20 | predicted (travel demand) |
| 270 | Trier | 1.56 | 69,369 | - | - | - | 154 | 20 | predicted (travel demand) |
| 271 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 20 | predicted (travel demand) |
| 272 | Pisa | 1.46 | 52,174 | 4 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 273 | Nashville | 2.23 | - | 8 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 274 | Hanoi | 2.15 | 117,396 | 2 | - | - | - | 100 | published, never ranked (may be uncrawled) |
| 275 | Ann Arbor | 2.14 | - | 3 | - | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 276 | Taipei | 2.09 | 143,193 | 4 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 277 | Salamanca | 1.37 | 47,897 | 4 | 1 | 1 | 1 | 20 | published, never ranked (may be uncrawled) |
| 278 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 279 | Tilburg | 1.03 | - | 17 | - | 3 | 86 | 20 | published, never ranked (may be uncrawled) |
| 280 | Ischia | 1.32 | - | - | - | - | 2 | 20 | predicted (travel demand) |
| 281 | Albuquerque | 1.96 | - | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 282 | Izmir | 1.88 | 69,826 | - | - | - | - | 60 | predicted (travel demand) |
| 283 | Minneapolis | 1.88 | - | 4 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 284 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 285 | Baltimore | 1.77 | - | 4 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 286 | Auckland | 1.17 | 152,056 | 5 | 2 | - | 977 | 60 | published, never ranked (may be uncrawled) |
| 287 | Ljubljana | 1.70 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 288 | Pittsburgh | 1.70 | - | 12 | - | 1 | - | 30 | measured |
| 289 | Vancouver | 1.70 | 351,552 | 7 | - | - | - | 30 | measured |
| 290 | Dijon | 1.72 | 43,526 | - | - | - | - | 20 | predicted (travel demand) |
| 291 | Apeldoorn | 0.85 | - | 8 | - | 2 | 80 | 20 | measured |
| 292 | Como | 0.85 | 82,645 | 9 | 3 | 1 | 23 | 20 | measured |
| 293 | Delft | 0.85 | 31,293 | 12 | - | 1 | 60 | 20 | measured |
| 294 | Deventer | 0.85 | - | 12 | - | 1 | 213 | 20 | measured |
| 295 | Enschede | 0.85 | - | 13 | 1 | 1 | 82 | 20 | measured |
| 296 | Hilo | 1.70 | - | 9 | - | 2 | - | 10 | measured |
| 297 | Liverpool | 1.70 | 248,189 | 4 | 3 | - | - | 30 | measured |
| 298 | Lucca | 0.85 | 52,271 | 16 | 4 | 1 | 27 | 20 | measured |
| 299 | Maastricht | 0.85 | 47,763 | 16 | - | 2 | 135 | 20 | measured |
| 300 | Sorrento | 0.85 | 40,049 | 7 | - | 1 | 20 | 10 | measured |
| 301 | Annecy | 1.69 | 56,859 | - | - | - | - | 20 | predicted (travel demand) |
| 302 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 303 | Perugia | 0.85 | 42,572 | 16 | 1 | 2 | 19 | 20 | measured |
| 304 | Mostar | 1.58 | 63,907 | - | - | - | - | 20 | predicted (travel demand) |
| 305 | Setubal | 0.85 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 306 | Braga | 0.85 | 34,522 | 4 | 2 | - | 8 | 20 | measured |
| 307 | Quebec City | 1.01 | 124,358 | 6 | - | 1 | 494 | 30 | published, never ranked (may be uncrawled) |
| 308 | Gothenburg | 1.49 | 119,991 | 5 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 309 | Ferrara | 0.85 | 27,490 | 5 | 3 | 1 | 7 | 20 | measured |
| 310 | Malta | 1.45 | - | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 311 | Matera | 0.85 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 312 | Pamplona | 0.85 | 128,065 | 25 | - | 3 | 9 | 20 | measured |
| 313 | Antalya | 1.31 | 70,688 | - | - | - | - | 60 | predicted (travel demand) |
| 314 | Menorca | 0.85 | - | 6 | - | - | 2 | 20 | measured |
| 315 | Cardiff | 1.27 | - | 13 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 316 | Santa Fe | 1.29 | - | 3 | - | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 317 | Colmar | 1.28 | 45,517 | - | - | - | - | 20 | predicted (travel demand) |
| 318 | Canberra | 0.85 | - | 8 | 1 | 1 | 132 | 30 | measured |
| 319 | Cesky Krumlov | 0.85 | 28,582 | 6 | 3 | - | 11 | 10 | measured |
| 320 | Hobart | 0.85 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 321 | Toulouse | 0.85 | 112,721 | 10 | - | 1 | 34 | 30 | measured |
| 322 | Bodrum | 1.26 | 33,918 | - | - | - | - | 20 | predicted (travel demand) |
| 323 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 324 | Lausanne | 1.23 | 68,242 | 8 | 1 | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 325 | Evora | 0.78 | 15,345 | - | - | - | - | 20 | predicted (travel demand) |
| 326 | Bergamo | 0.57 | 52,933 | 9 | 2 | 1 | 17 | 20 | published, never ranked (may be uncrawled) |
| 327 | Zaragoza | 0.73 | 87,580 | 7 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 328 | Okinawa | 0.71 | 24,466 | 6 | - | - | 1 | 30 | published, never ranked (may be uncrawled) |
| 329 | Dubrovnik | 0.99 | 119,586 | 4 | 4 | - | 2 | 10 | published, never ranked (may be uncrawled) |
| 330 | Rothenburg ob der Tauber | 0.85 | 39,879 | 5 | 1 | 1 | 8 | 10 | measured |
| 331 | Split | 0.97 | 132,399 | 5 | - | 1 | 2 | 20 | published, never ranked (may be uncrawled) |
| 332 | Azores | 0.65 | - | 7 | 2 | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 333 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 60 | predicted (travel demand) |
| 334 | Heidelberg | 0.85 | 75,837 | 7 | 1 | 1 | - | 20 | measured |
| 335 | Innsbruck | 0.63 | 58,742 | 6 | 2 | 1 | 39 | 20 | published, never ranked (may be uncrawled) |
| 336 | Buenos Aires | 0.85 | 333,331 | 4 | 2 | - | - | 60 | measured |
| 337 | Riga | 0.85 | 108,918 | 5 | 2 | - | - | 30 | measured |
| 338 | Kotor | 0.86 | 48,982 | 1 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 339 | Bucharest | 0.85 | 136,836 | 4 | - | 1 | - | 60 | measured |
| 340 | Leuven | 0.85 | 40,645 | 4 | - | - | - | 20 | measured |
| 341 | Manchester | 0.85 | 316,438 | 5 | 1 | - | - | 30 | measured |
| 342 | Nantes | 0.85 | 67,689 | 1 | 1 | - | - | 30 | measured |
| 343 | Thessaloniki | 0.85 | 180,145 | 4 | - | 1 | - | 30 | measured |
| 344 | Turku | 0.85 | - | 1 | 1 | - | - | 20 | measured |
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
| 355 | Hallstatt | 0.50 | 47,271 | 7 | 4 | - | 4 | 10 | published, never ranked (may be uncrawled) |
| 356 | Hoorn | 0.30 | - | 12 | - | 2 | 52 | 20 | published, never ranked (may be uncrawled) |
| 357 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 100 | published, never ranked (may be uncrawled) |
| 358 | Rouen | 0.54 | 72,334 | 12 | - | 1 | 6 | 20 | published, never ranked (may be uncrawled) |
| 359 | Phoenix | 0.55 | - | - | - | - | - | 60 | predicted (travel demand) |
| 360 | Roosendaal | 0.26 | - | 20 | - | 2 | 138 | 20 | published, never ranked (may be uncrawled) |
| 361 | Windsor | 0.50 | 30,452 | 2 | - | - | - | 10 | predicted (travel demand) |
| 362 | Killarney | 0.30 | 28,763 | 1 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 363 | Yakushima | 0.28 | - | 2 | 2 | - | 1 | 10 | published, never ranked (may be uncrawled) |
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

