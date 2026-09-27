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
| 1 | Oahu | 76.65 | - | 21 | 5 | 3 | 163 | 30 | measured |
| 2 | Lisbon | 51.04 | 201,877 | 36 | 16 | 3 | 67 | 30 | measured |
| 3 | Barcelona | 49.04 | 346,477 | 56 | 14 | 7 | 180 | 60 | measured |
| 4 | Amsterdam | 47.70 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 5 | Singapore | 63.09 | 967,821 | 34 | 7 | 3 | 165 | 100 | measured |
| 6 | Rome | 39.83 | 358,876 | 31 | 10 | 2 | 32 | 60 | measured |
| 7 | Palermo | 37.82 | 124,310 | 21 | 9 | 1 | 37 | 30 | measured |
| 8 | New York | 64.26 | 1,124,326 | 20 | 5 | 2 | - | 100 | measured |
| 9 | Berlin | 45.02 | 412,181 | 33 | 23 | 3 | 195 | 60 | measured |
| 10 | Tenerife | 43.34 | - | 4 | 4 | - | - | 30 | measured |
| 11 | Seville | 43.01 | 170,545 | 43 | 10 | 2 | - | 30 | measured |
| 12 | Tokyo | 34.81 | 394,702 | 22 | 15 | 1 | 5 | 100 | measured |
| 13 | Brussels | 36.99 | 176,863 | 35 | 4 | 2 | 436 | 60 | measured |
| 14 | Alicante | 25.61 | 77,454 | 21 | 4 | 2 | 44 | 30 | measured |
| 15 | Munich | 32.80 | 224,067 | 45 | 15 | 6 | 80 | 60 | measured |
| 16 | Bath | 47.70 | 144,950 | 5 | 2 | 1 | - | 20 | measured |
| 17 | Dublin | 26.61 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 18 | Arnhem | 22.93 | 31,478 | 39 | 3 | 3 | 204 | 20 | measured |
| 19 | Paris | 28.79 | 524,268 | 31 | 9 | 4 | 129 | 60 | measured |
| 20 | Vienna | 28.79 | 283,090 | 32 | 19 | 5 | 376 | 60 | measured |
| 21 | Pamplona | 25.27 | 128,065 | 14 | - | 1 | 9 | 20 | measured |
| 22 | Porto | 21.09 | 120,415 | 27 | 15 | 2 | 40 | 30 | measured |
| 23 | Brisbane | 27.95 | 162,602 | 20 | 2 | 2 | 186 | 60 | measured |
| 24 | Malaga | 27.61 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 25 | Birmingham | 37.53 | - | - | - | - | - | 60 | predicted (travel demand) |
| 26 | Milan | 17.57 | 212,705 | 30 | 14 | 3 | 25 | 60 | measured |
| 27 | Austin | 34.14 | 226,631 | 9 | 2 | - | - | 30 | measured |
| 28 | Portland | 23.10 | 217,222 | 24 | 1 | 2 | 306 | 30 | measured |
| 29 | Cagliari | 18.58 | 51,351 | 14 | 1 | 2 | 15 | 20 | measured |
| 30 | Los Angeles | 32.80 | 665,559 | 10 | 2 | - | - | 60 | measured |
| 31 | Prague | 22.43 | 303,350 | 30 | 21 | 4 | 31 | 60 | measured |
| 32 | Florence | 16.07 | 184,099 | 27 | 9 | 1 | 27 | 30 | measured |
| 33 | Cadiz | 20.08 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 34 | Houston | 30.46 | - | 6 | - | - | - | 60 | measured |
| 35 | Edinburgh | 29.62 | 292,981 | 16 | 5 | 1 | - | 30 | measured |
| 36 | Valencia | 14.06 | 162,209 | 31 | 4 | 2 | 350 | 30 | measured |
| 37 | Sintra | 13.89 | 46,889 | 5 | 3 | - | 6 | 30 | measured |
| 38 | London | 22.76 | 718,291 | 23 | 16 | 1 | - | 100 | measured |
| 39 | New Orleans | 26.11 | 256,232 | 8 | 5 | 1 | - | 30 | measured |
| 40 | Sao Paulo | 24.60 | 911 | 1 | - | - | - | 100 | measured |
| 41 | Palma de Mallorca | 15.23 | 84,075 | 5 | 1 | 1 | 8 | 30 | measured |
| 42 | Madrid | 15.56 | 274,553 | 17 | 11 | 2 | - | 60 | measured |
| 43 | The Hague | 12.55 | 236,723 | 31 | 2 | 5 | 167 | 30 | measured |
| 44 | Krakow | 16.40 | 140,824 | 38 | 8 | 3 | 198 | 30 | measured |
| 45 | Chicago | 24.43 | 485,769 | 6 | - | - | - | 60 | measured |
| 46 | Dallas | 22.76 | - | 12 | 1 | 1 | - | 60 | measured |
| 47 | Jacksonville | 22.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 48 | Athens | 22.26 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 49 | Nijmegen | 11.21 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 50 | Monterey | 21.76 | - | 3 | 1 | - | - | 10 | measured |
| 51 | Venice | 11.55 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 52 | Asheville | 20.89 | - | - | - | - | - | 20 | predicted (travel demand) |
| 53 | Long Beach | 20.48 | - | - | - | - | - | 30 | predicted (travel demand) |
| 54 | Little Rock | 20.40 | - | - | - | - | - | 20 | predicted (travel demand) |
| 55 | Boston | 19.41 | 385,902 | 12 | 2 | 1 | - | 30 | measured |
| 56 | Utrecht | 9.87 | 67,963 | 30 | 7 | 2 | 339 | 30 | measured |
| 57 | Glasgow | 18.74 | 253,705 | 5 | 3 | - | - | 30 | measured |
| 58 | Oakland | 18.81 | - | - | - | - | - | 30 | predicted (travel demand) |
| 59 | Warsaw | 12.22 | 197,929 | 39 | 14 | 4 | 1407 | 60 | measured |
| 60 | Lexington | 18.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 61 | Reno | 18.19 | - | - | - | - | - | 30 | predicted (travel demand) |
| 62 | Des Moines | 18.11 | - | - | - | - | - | 20 | predicted (travel demand) |
| 63 | Philadelphia | 17.07 | 405,294 | 4 | 1 | - | - | 60 | measured |
| 64 | Daytona Beach | 17.66 | - | - | - | - | - | 20 | predicted (travel demand) |
| 65 | San Francisco | 17.07 | 361,111 | 6 | 1 | 1 | - | 30 | measured |
| 66 | Cork | 11.38 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 67 | Fukuoka | 11.05 | 77,485 | 15 | 9 | 1 | - | 60 | measured |
| 68 | Sardinia | 9.37 | - | 5 | 4 | - | 8 | 60 | measured |
| 69 | Chattanooga | 16.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 70 | Hobart | 11.05 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 71 | Haarlem | 8.20 | 33,960 | 21 | 1 | 2 | 277 | 20 | measured |
| 72 | Washington DC | 14.73 | 606,731 | 15 | 1 | 3 | - | 30 | measured |
| 73 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 74 | Reykjavik | 13.72 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 75 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 76 | Montreal | 15.73 | 315,322 | 13 | 1 | 2 | - | 60 | measured |
| 77 | Huntsville | 15.35 | - | - | - | - | - | 20 | predicted (travel demand) |
| 78 | Seattle | 14.73 | 398,724 | 8 | 1 | 1 | - | 30 | measured |
| 79 | Las Vegas | 15.06 | - | 11 | - | 2 | - | 30 | measured |
| 80 | Naples | 7.53 | 198,913 | 24 | 3 | 3 | 46 | 30 | measured |
| 81 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 82 | West Palm Beach | 14.98 | - | - | - | - | - | 20 | predicted (travel demand) |
| 83 | Saint Petersburg | 14.83 | - | - | - | - | - | 100 | predicted (travel demand) |
| 84 | St. Louis | 14.80 | - | - | - | - | - | 30 | predicted (travel demand) |
| 85 | Ottawa | 9.71 | - | 21 | - | 3 | 122 | 60 | measured |
| 86 | Madeira | 8.70 | - | 10 | 1 | 1 | - | 30 | measured |
| 87 | Tampa | 14.10 | - | - | - | - | - | 30 | predicted (travel demand) |
| 88 | Leeuwarden | 7.03 | - | 41 | - | 2 | 61 | 20 | measured |
| 89 | Coimbra | 7.53 | 34,962 | 5 | - | - | 5 | 20 | measured |
| 90 | Kyoto | 8.87 | 142,353 | 18 | 12 | 2 | - | 60 | measured |
| 91 | Osaka | 8.87 | 163,112 | 6 | 1 | - | - | 60 | measured |
| 92 | Copenhagen | 13.22 | 218,621 | 42 | 34 | 6 | - | 30 | measured |
| 93 | Leiden | 6.86 | 33,227 | 20 | 6 | 1 | 129 | 20 | measured |
| 94 | Kanazawa | 8.70 | 25,778 | 7 | 2 | 1 | 2 | 30 | measured |
| 95 | Cincinnati | 13.33 | - | - | - | - | - | 30 | predicted (travel demand) |
| 96 | Granada | 8.37 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 97 | Leipzig | 8.70 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 98 | Melbourne | 8.70 | 267,898 | 16 | - | 2 | 403 | 100 | measured |
| 99 | Lansing | 13.02 | - | - | - | - | - | 20 | predicted (travel demand) |
| 100 | Vilnius | 8.54 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 101 | Detroit | 12.53 | - | - | - | - | - | 30 | predicted (travel demand) |
| 102 | Spokane | 9.04 | - | 13 | - | 2 | 18 | 20 | measured |
| 103 | Liverpool | 12.05 | 248,189 | 2 | 1 | - | - | 30 | measured |
| 104 | Amersfoort | 6.02 | - | 18 | 1 | 2 | 181 | 20 | measured |
| 105 | Sorrento | 6.02 | 40,049 | 7 | - | 1 | 20 | 10 | measured |
| 106 | Denver | 11.66 | - | - | - | - | - | 30 | predicted (travel demand) |
| 107 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 60 | predicted (travel demand) |
| 108 | San Jose | 11.39 | - | - | - | - | - | 60 | predicted (travel demand) |
| 109 | Sacramento | 11.32 | - | - | - | - | - | 30 | predicted (travel demand) |
| 110 | Geneva | 7.53 | 162,269 | 21 | 5 | 4 | 131 | 20 | measured |
| 111 | Jersey City | 10.08 | - | - | - | - | - | 30 | predicted (travel demand) |
| 112 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 60 | predicted (travel demand) |
| 113 | Ibiza | 7.03 | - | 1 | - | - | 4 | 20 | measured |
| 114 | Dubai | 11.02 | 334,167 | - | - | - | - | 60 | predicted (travel demand) |
| 115 | Eindhoven | 5.36 | - | 21 | - | 4 | 195 | 20 | measured |
| 116 | Maastricht | 5.36 | 47,763 | 19 | - | 2 | 135 | 20 | measured |
| 117 | Milwaukee | 10.63 | - | - | - | - | - | 30 | predicted (travel demand) |
| 118 | Pittsburgh | 10.38 | - | 4 | - | 1 | - | 30 | measured |
| 119 | Salt Lake City | 10.31 | - | - | - | - | - | 20 | predicted (travel demand) |
| 120 | Atlanta | 10.29 | - | - | - | - | - | 30 | predicted (travel demand) |
| 121 | Anchorage | 10.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 122 | Cyprus | 9.87 | - | 4 | - | - | - | 60 | measured |
| 123 | Raleigh | 10.07 | - | - | - | - | - | 30 | predicted (travel demand) |
| 124 | Sydney | 9.87 | 305,304 | 7 | 1 | - | - | 100 | measured |
| 125 | Boise | 10.04 | - | 4 | - | 1 | - | 20 | measured |
| 126 | Bali | 9.95 | - | - | - | - | - | 60 | predicted (travel demand) |
| 127 | Segovia | 6.19 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 128 | Cleveland | 9.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 129 | El Paso | 9.70 | - | - | - | - | - | 30 | predicted (travel demand) |
| 130 | Parma | 5.36 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 131 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 132 | Strasbourg | 6.36 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 133 | Miami | 9.48 | 278,558 | - | - | - | - | 30 | predicted (travel demand) |
| 134 | Dordrecht | 4.69 | - | 20 | 1 | 2 | 105 | 20 | measured |
| 135 | Edmonton | 9.38 | - | - | - | - | - | 60 | predicted (travel demand) |
| 136 | Tilburg | 4.69 | - | 20 | - | 3 | 87 | 20 | measured |
| 137 | Winnipeg | 9.21 | - | - | - | - | - | 30 | predicted (travel demand) |
| 138 | Stockholm | 7.36 | 188,184 | 8 | 4 | - | - | 30 | measured |
| 139 | Budapest | 8.70 | 283,807 | 13 | 1 | 3 | - | 60 | measured |
| 140 | Groningen | 4.52 | 31,401 | 21 | 1 | 2 | 76 | 20 | measured |
| 141 | Verona | 5.36 | 77,646 | 8 | 4 | 1 | 3 | 30 | measured |
| 142 | Nashville | 8.93 | - | - | - | - | - | 30 | predicted (travel demand) |
| 143 | Seoul | 8.20 | 206,265 | 8 | 5 | 1 | - | 100 | measured |
| 144 | Girona | 5.19 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 145 | Quebec City | 5.86 | 124,358 | 6 | - | 1 | 494 | 30 | measured |
| 146 | Tampere | 8.78 | - | - | - | - | - | 30 | predicted (travel demand) |
| 147 | Crete | 8.70 | - | 4 | 3 | - | - | 30 | measured |
| 148 | Ann Arbor | 8.55 | - | - | - | - | - | 20 | predicted (travel demand) |
| 149 | Guimaraes | 4.35 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 150 | Zurich | 8.03 | 140,788 | 6 | 1 | - | - | 30 | measured |
| 151 | Adelaide | 8.14 | 139,166 | - | - | - | - | 60 | predicted (travel demand) |
| 152 | Toronto | 8.03 | 411,011 | 6 | - | - | - | 60 | measured |
| 153 | Dubrovnik | 7.70 | 119,586 | 4 | 1 | - | 2 | 10 | measured |
| 154 | Bari | 4.85 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 155 | Albuquerque | 7.83 | - | - | - | - | - | 30 | predicted (travel demand) |
| 156 | Tallinn | 5.19 | 124,888 | 9 | 3 | 2 | 42 | 30 | measured |
| 157 | Cambridge | 7.70 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 158 | Leuven | 7.70 | 40,645 | 4 | - | - | - | 20 | measured |
| 159 | Nice | 7.70 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 160 | Charleston | 7.36 | 155,987 | 3 | 1 | - | - | 20 | measured |
| 161 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 20 | predicted (travel demand) |
| 162 | Enschede | 3.68 | - | 15 | 1 | 2 | 82 | 20 | measured |
| 163 | Minneapolis | 7.36 | - | 4 | - | - | - | 30 | measured |
| 164 | Savannah | 7.36 | 128,162 | 3 | 1 | - | - | 20 | measured |
| 165 | Bergen | 7.30 | 82,940 | - | - | - | - | 30 | predicted (travel demand) |
| 166 | Sapporo | 4.85 | 88,633 | 6 | - | - | - | 60 | measured |
| 167 | Helsinki | 5.52 | 148,908 | 12 | 2 | 1 | 13 | 30 | measured |
| 168 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 20 | predicted (travel demand) |
| 169 | Siena | 4.62 | 57,436 | - | - | - | - | 20 | predicted (travel demand) |
| 170 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 20 | predicted (travel demand) |
| 171 | Zwolle | 3.35 | - | 20 | - | 4 | 58 | 20 | measured |
| 172 | Yakushima | 4.18 | - | 2 | - | - | 1 | 10 | measured |
| 173 | Zagreb | 6.42 | 122,890 | - | - | - | - | 30 | predicted (travel demand) |
| 174 | Catania | 3.85 | 58,252 | 4 | 3 | 1 | 5 | 30 | measured |
| 175 | Bordeaux | 4.35 | 156,201 | 10 | - | 2 | 211 | 30 | measured |
| 176 | Luxembourg City | 4.35 | 64,851 | 10 | 5 | 2 | 18 | 20 | measured |
| 177 | Lyon | 4.35 | 136,951 | 13 | 4 | 1 | 156 | 30 | measured |
| 178 | Bogota | 6.39 | 1,623 | - | - | - | - | 100 | predicted (travel demand) |
| 179 | Shanghai | 6.38 | 277,140 | - | - | - | - | 100 | predicted (travel demand) |
| 180 | Hawaii | 5.69 | - | 6 | - | 1 | 6 | 60 | measured |
| 181 | Caserta | 3.18 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 182 | Perth | 6.19 | 180,478 | 6 | 3 | 1 | - | 60 | measured |
| 183 | Vancouver | 6.19 | 351,552 | 7 | - | - | - | 30 | measured |
| 184 | Padua | 3.35 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 185 | Oslo | 5.52 | 181,113 | 4 | - | - | - | 30 | measured |
| 186 | Funchal | 3.77 | 174,351 | - | - | - | - | 20 | predicted (travel demand) |
| 187 | Hong Kong | 4.10 | 689,212 | 10 | 4 | 1 | 505 | 100 | measured |
| 188 | Istanbul | 5.27 | 333,027 | 14 | 4 | 1 | - | 100 | measured |
| 189 | Genoa | 3.18 | 145,206 | 13 | 2 | 1 | 10 | 30 | measured |
| 190 | Malta | 5.79 | - | - | - | - | - | 30 | predicted (travel demand) |
| 191 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 192 | Bergamo | 2.85 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 193 | Bristol | 5.69 | 163,983 | 6 | 2 | - | - | 30 | measured |
| 194 | Bologna | 3.01 | 146,161 | 12 | 7 | 1 | 9 | 30 | measured |
| 195 | Avignon | 5.54 | 64,047 | - | - | - | - | 20 | predicted (travel demand) |
| 196 | Frankfurt | 3.68 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 197 | Galway | 3.65 | 88,162 | - | - | - | - | 20 | predicted (travel demand) |
| 198 | Phuket | 5.46 | 5,487 | - | - | - | - | 30 | predicted (travel demand) |
| 199 | Menorca | 3.51 | - | 6 | - | - | 2 | 20 | measured |
| 200 | Rovaniemi | 5.38 | - | - | - | - | - | 20 | predicted (travel demand) |
| 201 | Lagos | 3.43 | 34,452 | - | - | - | - | 100 | predicted (travel demand) |
| 202 | Beijing | 5.27 | 269,737 | 7 | 1 | - | - | 100 | measured |
| 203 | Santa Fe | 5.17 | - | - | - | - | - | 20 | predicted (travel demand) |
| 204 | Lund | 5.14 | - | - | - | - | - | 20 | predicted (travel demand) |
| 205 | Kobe | 3.40 | 54,798 | - | - | - | - | 60 | predicted (travel demand) |
| 206 | Den Bosch | 2.51 | 39,682 | 12 | 2 | 1 | 118 | 20 | measured |
| 207 | Helmond | 2.51 | - | 20 | - | 2 | 54 | 20 | measured |
| 208 | Hoorn | 2.51 | - | 12 | - | 2 | 52 | 20 | measured |
| 209 | Cordoba | 3.18 | 74,675 | 16 | 2 | 2 | 3 | 30 | measured |
| 210 | Heraklion | 4.96 | 66,359 | - | - | - | - | 20 | predicted (travel demand) |
| 211 | Marseille | 4.96 | 182,033 | - | - | - | - | 30 | predicted (travel demand) |
| 212 | Salzburg | 3.18 | 107,243 | 12 | 3 | 2 | 34 | 20 | measured |
| 213 | Kauai | 4.02 | - | 6 | 1 | - | 8 | 20 | measured |
| 214 | Basel | 4.59 | 105,838 | - | - | - | - | 20 | predicted (travel demand) |
| 215 | Manchester | 4.52 | 316,438 | 5 | - | - | - | 30 | measured |
| 216 | Ljubljana | 4.35 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 217 | Tasmania | 4.41 | - | - | - | - | - | 30 | predicted (travel demand) |
| 218 | Lucca | 2.18 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 219 | Taipei | 4.35 | 143,193 | 4 | 1 | - | - | 60 | measured |
| 220 | Salamanca | 2.85 | 47,897 | 4 | - | 1 | 1 | 20 | measured |
| 221 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 20 | predicted (travel demand) |
| 222 | San Sebastian | 2.80 | 367 | - | - | - | - | 20 | predicted (travel demand) |
| 223 | Heidelberg | 3.68 | 75,837 | 6 | 1 | 1 | - | 20 | measured |
| 224 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 30 | predicted (travel demand) |
| 225 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 226 | Alkmaar | 2.01 | - | 14 | - | 2 | 79 | 20 | measured |
| 227 | Toulouse | 2.68 | 112,721 | 10 | - | 1 | 34 | 30 | measured |
| 228 | Hilo | 3.01 | - | 6 | - | 1 | 16 | 10 | measured |
| 229 | Azores | 2.62 | - | - | - | - | - | 20 | predicted (travel demand) |
| 230 | Cardiff | 3.85 | - | 4 | - | 1 | - | 30 | measured |
| 231 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 232 | Niagara Falls | 3.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 233 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 100 | predicted (travel demand) |
| 234 | Nuremberg | 2.51 | 161,614 | 12 | 1 | 1 | 38 | 30 | measured |
| 235 | Cologne | 3.68 | 191,812 | 5 | - | 1 | - | 60 | measured |
| 236 | Como | 1.84 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 237 | Deventer | 1.84 | - | 12 | - | 1 | 213 | 20 | measured |
| 238 | Trieste | 1.84 | 117,233 | 36 | 1 | 3 | 43 | 20 | measured |
| 239 | Tulsa | 3.68 | - | 1 | - | - | - | 30 | measured |
| 240 | Wellington | 3.60 | 132,267 | - | - | - | - | 20 | predicted (travel demand) |
| 241 | Bilbao | 2.34 | 133,133 | 4 | - | 1 | - | 30 | measured |
| 242 | Bratislava | 2.34 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 243 | Montpellier | 3.47 | 64,238 | - | - | - | - | 30 | predicted (travel demand) |
| 244 | Perugia | 1.84 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 245 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 246 | Cape Town | 3.29 | 199,169 | - | - | - | - | 60 | predicted (travel demand) |
| 247 | Rhodes | 3.42 | 127,205 | - | - | - | - | 20 | predicted (travel demand) |
| 248 | Apeldoorn | 1.67 | - | 10 | - | 2 | 80 | 20 | measured |
| 249 | Delft | 1.67 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 250 | Roosendaal | 1.67 | - | 8 | - | 1 | 116 | 20 | measured |
| 251 | San Antonio | 3.32 | - | 4 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 252 | Freiburg | 3.18 | 92,752 | 7 | 2 | 1 | - | 20 | measured |
| 253 | Nagoya | 2.18 | 83,437 | 6 | 1 | - | 1 | 60 | measured |
| 254 | Stuttgart | 2.51 | 112,789 | 6 | 1 | - | - | 30 | measured |
| 255 | Chania | 3.30 | 47,379 | - | - | - | - | 20 | predicted (travel demand) |
| 256 | Mexico City | 3.10 | 566,583 | 9 | 2 | - | - | 100 | measured |
| 257 | Santiago | 3.25 | 111,647 | - | - | - | - | 100 | predicted (travel demand) |
| 258 | Oxford | 3.18 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 259 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 30 | predicted (travel demand) |
| 260 | Lucerne | 3.10 | 66,356 | - | - | - | - | 20 | predicted (travel demand) |
| 261 | Tarragona | 1.84 | 32,396 | 4 | 2 | - | - | 20 | measured |
| 262 | Malmo | 3.07 | 103,940 | - | - | - | - | 30 | predicted (travel demand) |
| 263 | Lille | 3.06 | 73,435 | - | - | - | - | 20 | predicted (travel demand) |
| 264 | Assen | 1.51 | - | 10 | - | 2 | 66 | 20 | measured |
| 265 | Hilversum | 1.51 | - | 6 | 1 | 1 | 122 | 20 | measured |
| 266 | Gdansk | 2.01 | 4,908 | 12 | 4 | 1 | 307 | 30 | measured |
| 267 | San Diego | 3.01 | 214,939 | 6 | 1 | 1 | - | 60 | measured |
| 268 | York | 3.01 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 269 | Corsica | 3.00 | - | - | - | - | - | 30 | predicted (travel demand) |
| 270 | Mechelen | 2.93 | 20,707 | - | - | - | - | 20 | predicted (travel demand) |
| 271 | Ferrara | 1.67 | 27,490 | 5 | 3 | 1 | 7 | 20 | measured |
| 272 | Nantes | 2.85 | 67,689 | 1 | 1 | - | - | 30 | measured |
| 273 | Ronda | 1.67 | 51,510 | 6 | 1 | - | 9 | 10 | measured |
| 274 | Pisa | 1.84 | 52,174 | 4 | - | - | - | 20 | measured |
| 275 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 276 | Aarhus | 2.68 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 277 | Fort Lauderdale | 2.68 | - | 4 | - | - | - | 20 | measured |
| 278 | Indianapolis | 2.68 | - | 1 | - | - | - | 30 | measured |
| 279 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 280 | Corfu | 2.71 | 139,334 | - | - | - | - | 20 | predicted (travel demand) |
| 281 | Trento | 1.34 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 282 | Turin | 1.34 | 147,456 | 11 | 7 | 2 | 30 | 30 | measured |
| 283 | Syracuse | 1.75 | 102,833 | - | - | - | - | 20 | predicted (travel demand) |
| 284 | Cartagena | 2.58 | 65,066 | - | - | - | - | 30 | predicted (travel demand) |
| 285 | Gran Canaria | 1.67 | - | - | - | - | - | 30 | predicted (travel demand) |
| 286 | Matera | 1.51 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 287 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 20 | predicted (travel demand) |
| 288 | Bern | 2.51 | 90,627 | - | - | - | - | 20 | predicted (travel demand) |
| 289 | Hallstatt | 2.18 | 47,271 | 5 | 1 | - | - | 10 | measured |
| 290 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 291 | Faro | 1.62 | 55,645 | - | - | - | - | 20 | predicted (travel demand) |
| 292 | Ghent | 2.34 | 82,757 | 8 | 1 | 1 | - | 30 | measured |
| 293 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 294 | Regensburg | 2.18 | 51,930 | 5 | 1 | 1 | 4 | 20 | measured |
| 295 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 296 | Cusco | 2.35 | 87,732 | - | - | - | - | 30 | predicted (travel demand) |
| 297 | Limerick | 1.57 | 90,379 | - | - | - | - | 20 | predicted (travel demand) |
| 298 | Bangkok | 2.34 | 222,206 | 5 | 1 | 1 | - | 100 | measured |
| 299 | Heerlen | 1.17 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 300 | Kansas City | 2.34 | - | 4 | - | 1 | - | 30 | measured |
| 301 | Brno | 1.51 | 63,714 | 8 | 5 | 2 | 34 | 30 | measured |
| 302 | Dresden | 1.51 | 113,624 | 5 | 5 | 1 | - | 30 | measured |
| 303 | Graz | 1.51 | 65,717 | 13 | 7 | 2 | 87 | 30 | measured |
| 304 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 20 | predicted (travel demand) |
| 305 | Lausanne | 2.18 | 68,242 | 8 | 1 | 1 | - | 20 | measured |
| 306 | Hamburg | 2.01 | 191,221 | 6 | 1 | 1 | - | 60 | measured |
| 307 | Setubal | 1.17 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 308 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 309 | Ischia | 1.32 | - | - | - | - | 2 | 20 | predicted (travel demand) |
| 310 | Izmir | 1.88 | 69,826 | - | - | - | - | 60 | predicted (travel demand) |
| 311 | Modena | 1.17 | 51,698 | 5 | 1 | 1 | 3 | 20 | measured |
| 312 | Riga | 1.84 | 108,918 | 5 | 2 | - | - | 30 | measured |
| 313 | Belfast | 1.84 | 224,315 | 5 | - | 1 | - | 30 | measured |
| 314 | Belgrade | 1.84 | 178,116 | 5 | 5 | - | - | 60 | measured |
| 315 | Split | 1.84 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 316 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 317 | Christchurch | 1.21 | 104,874 | 6 | - | 1 | 466 | 30 | published, never ranked (may be uncrawled) |
| 318 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 319 | Dijon | 1.72 | 43,526 | - | - | - | - | 20 | predicted (travel demand) |
| 320 | Trier | 1.56 | 69,369 | - | - | - | - | 20 | predicted (travel demand) |
| 321 | Baltimore | 1.67 | - | 4 | - | - | - | 30 | measured |
| 322 | Annecy | 1.69 | 56,859 | - | - | - | - | 20 | predicted (travel demand) |
| 323 | Bruges | 1.67 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 324 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 325 | Canterbury | 1.59 | 53,301 | - | - | - | - | 20 | predicted (travel demand) |
| 326 | Mostar | 1.58 | 63,907 | - | - | - | - | 20 | predicted (travel demand) |
| 327 | Zadar | 1.53 | 71,549 | - | - | - | - | 20 | predicted (travel demand) |
| 328 | Zaragoza | 1.00 | 87,580 | 7 | - | 1 | - | 30 | measured |
| 329 | Braga | 0.84 | 34,522 | 4 | 2 | - | 8 | 20 | measured |
| 330 | Cesky Krumlov | 1.00 | 28,582 | 6 | 3 | - | 11 | 10 | measured |
| 331 | Potsdam | 1.00 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 332 | Breda | 0.67 | 36,579 | 11 | - | 2 | 120 | 20 | measured |
| 333 | Turku | 1.34 | - | 1 | - | - | - | 20 | measured |
| 334 | Venlo | 0.67 | - | 7 | - | 1 | 144 | 20 | measured |
| 335 | Antalya | 1.31 | 70,688 | - | - | - | - | 60 | predicted (travel demand) |
| 336 | Colmar | 1.28 | 45,517 | - | - | - | - | 20 | predicted (travel demand) |
| 337 | Auckland | 0.84 | 152,056 | 5 | 2 | - | 977 | 60 | measured |
| 338 | Bodrum | 1.26 | 33,918 | - | - | - | - | 20 | predicted (travel demand) |
| 339 | Hiroshima | 0.84 | 129,791 | 33 | 5 | 2 | - | 60 | measured |
| 340 | Rio de Janeiro | 1.26 | 279,431 | 6 | - | - | - | 100 | measured |
| 341 | Sofia | 0.84 | 138,710 | 4 | - | - | - | 60 | measured |
| 342 | Wroclaw | 0.84 | 123,894 | 5 | 1 | 1 | 121 | 30 | measured |
| 343 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 344 | Buenos Aires | 1.17 | 333,331 | 4 | 2 | - | - | 60 | measured |
| 345 | Evora | 0.78 | 15,345 | - | - | - | - | 20 | predicted (travel demand) |
| 346 | Thessaloniki | 1.17 | 180,145 | 4 | - | 1 | - | 30 | measured |
| 347 | Rouen | 1.00 | 72,334 | 12 | - | 1 | 6 | 20 | measured |
| 348 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 349 | Kamakura | 0.67 | 33,492 | 6 | - | - | - | 20 | measured |
| 350 | La Palma | 0.70 | - | - | - | - | - | 20 | predicted (travel demand) |
| 351 | Brighton | 1.00 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 352 | Rotterdam | 0.50 | 104,938 | 16 | - | 2 | 83 | 30 | measured |
| 353 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 60 | predicted (travel demand) |
| 354 | Bamberg | 0.67 | 28,716 | 5 | 4 | 1 | 10 | 20 | measured |
| 355 | Rothenburg ob der Tauber | 0.67 | 39,879 | 4 | - | 1 | 8 | 10 | measured |
| 356 | Maui | 0.67 | - | 4 | - | - | 3 | 20 | measured |
| 357 | Bucharest | 0.67 | 136,836 | 4 | - | 1 | - | 60 | measured |
| 358 | Canberra | 0.67 | - | 1 | 1 | - | - | 30 | measured |
| 359 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 100 | published, never ranked (may be uncrawled) |
| 360 | Phoenix | 0.55 | - | - | - | - | - | 60 | predicted (travel demand) |
| 361 | Assisi | 0.33 | 30,278 | 6 | 1 | 2 | 6 | 10 | measured |
| 362 | Okinawa | 0.33 | 24,466 | 6 | - | - | 1 | 30 | measured |
| 363 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 364 | Toledo | 0.24 | 3,149 | - | - | - | - | 20 | predicted (travel demand) |
| 365 | Busan | 0.33 | 94,737 | 2 | - | - | - | 60 | measured |
| 366 | Antwerp | 0.33 | 128,289 | 10 | 4 | 1 | - | 30 | measured |
| 367 | Fort Worth | 0.33 | - | 5 | - | - | - | 30 | measured |
| 368 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 369 | George Town | 0.28 | 36,080 | - | - | - | - | 30 | predicted (travel demand) |
| 370 | Poznan | 0.17 | 65,666 | 10 | - | 1 | 397 | 30 | measured |
| 371 | Allentown | 0.24 | - | - | - | - | - | 20 | predicted (travel demand) |
| 372 | Oss | 0.11 | - | 6 | - | - | 48 | 20 | published, never ranked (may be uncrawled) |
| 373 | Gothenburg | 0.17 | 119,991 | 5 | - | 1 | - | 30 | measured |
| 374 | Queenstown | 0.16 | 36,672 | - | - | - | - | 10 | predicted (travel demand) |
| 375 | Buffalo | 0.15 | - | - | - | - | - | 10 | predicted (travel demand) |
| 376 | San Juan | 0.15 | - | - | - | - | - | 10 | predicted (travel demand) |
| 377 | Halifax | 0.08 | - | - | - | - | - | 30 | predicted (travel demand) |
| 378 | Memphis | 0.08 | - | - | - | - | - | 30 | predicted (travel demand) |

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

