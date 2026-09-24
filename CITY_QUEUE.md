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
| 1 | Pamplona | 92.64 | 128,065 | 14 | - | 1 | 9 | 20 | measured |
| 2 | Oahu | 89.65 | - | 21 | 2 | 3 | 163 | 30 | measured |
| 3 | Lisbon | 61.00 | 201,877 | 36 | 16 | 3 | 67 | 30 | measured |
| 4 | Brussels | 69.96 | 176,863 | 35 | 4 | 2 | 436 | 60 | measured |
| 5 | Barcelona | 51.86 | 346,477 | 56 | 14 | 7 | 180 | 60 | measured |
| 6 | Amsterdam | 49.39 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 7 | Singapore | 62.23 | 967,821 | 34 | 7 | 3 | 165 | 100 | measured |
| 8 | Rome | 39.73 | 358,876 | 31 | 10 | 2 | 32 | 60 | measured |
| 9 | Arnhem | 37.27 | 31,478 | 39 | 3 | 3 | 204 | 20 | measured |
| 10 | Tokyo | 40.78 | 394,702 | 22 | 10 | 1 | 5 | 100 | measured |
| 11 | Berlin | 48.87 | 412,181 | 33 | 23 | 3 | 195 | 60 | measured |
| 12 | Palermo | 36.39 | 124,310 | 21 | 9 | 1 | 37 | 30 | measured |
| 13 | Tenerife | 44.30 | - | 4 | 4 | - | - | 30 | measured |
| 14 | Seville | 41.13 | 170,545 | 43 | 9 | 2 | - | 30 | measured |
| 15 | Alicante | 30.23 | 77,454 | 21 | 4 | 2 | 44 | 30 | measured |
| 16 | New York | 50.63 | 1,124,326 | 20 | 5 | 2 | - | 100 | measured |
| 17 | Prague | 37.09 | 303,350 | 30 | 21 | 4 | 31 | 60 | measured |
| 18 | Portland | 34.45 | 217,222 | 20 | 1 | 2 | 301 | 30 | measured |
| 19 | Vienna | 33.22 | 283,090 | 32 | 18 | 5 | 376 | 60 | measured |
| 20 | Milan | 24.43 | 212,705 | 30 | 14 | 3 | 25 | 60 | measured |
| 21 | Bath | 47.29 | 144,950 | 5 | 2 | 1 | - | 20 | measured |
| 22 | Munich | 29.88 | 224,067 | 45 | 15 | 6 | 80 | 60 | measured |
| 23 | Austin | 44.30 | 226,631 | 5 | 2 | - | - | 30 | measured |
| 24 | Brisbane | 29.53 | 162,602 | 20 | 2 | 2 | 186 | 60 | measured |
| 25 | Porto | 21.45 | 120,415 | 27 | 15 | 2 | 40 | 30 | measured |
| 26 | Paris | 28.30 | 524,268 | 31 | 9 | 4 | 129 | 60 | measured |
| 27 | Malaga | 28.13 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 28 | Florence | 20.39 | 184,099 | 27 | 9 | 1 | 27 | 30 | measured |
| 29 | Birmingham | 37.53 | - | - | - | - | - | 60 | predicted (travel demand) |
| 30 | Valencia | 18.11 | 162,209 | 31 | 4 | 2 | 350 | 30 | measured |
| 31 | Los Angeles | 33.05 | 665,559 | 8 | 2 | - | - | 60 | measured |
| 32 | Dublin | 19.69 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 33 | Cagliari | 17.40 | 51,351 | 14 | 1 | 2 | 15 | 20 | measured |
| 34 | London | 26.89 | 718,291 | 23 | 14 | 1 | - | 100 | measured |
| 35 | Philadelphia | 29.53 | 405,294 | 1 | - | - | - | 60 | measured |
| 36 | Sintra | 15.29 | 46,889 | 5 | 3 | - | 6 | 30 | measured |
| 37 | Krakow | 20.21 | 140,824 | 38 | 8 | 3 | 198 | 30 | measured |
| 38 | Utrecht | 14.77 | 67,963 | 27 | 7 | 2 | 340 | 30 | measured |
| 39 | Edinburgh | 28.83 | 292,981 | 16 | 5 | 1 | - | 30 | measured |
| 40 | Cadiz | 18.28 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 41 | Dallas | 27.77 | - | 9 | 1 | 1 | - | 60 | measured |
| 42 | Monterey | 27.77 | - | 3 | 1 | - | - | 10 | measured |
| 43 | Houston | 27.07 | - | 6 | - | - | - | 60 | measured |
| 44 | Sao Paulo | 25.93 | 911 | 1 | - | - | - | 100 | measured |
| 45 | New Orleans | 24.96 | 256,232 | 6 | 2 | 1 | - | 30 | measured |
| 46 | Venice | 13.18 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 47 | Palma de Mallorca | 14.06 | 84,075 | 5 | 1 | 1 | 8 | 30 | measured |
| 48 | Cork | 15.47 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 49 | Jacksonville | 22.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 50 | Fukuoka | 14.41 | 77,485 | 15 | 9 | 1 | - | 60 | measured |
| 51 | Nijmegen | 10.90 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 52 | The Hague | 10.90 | 236,723 | 31 | 2 | 5 | 167 | 30 | measured |
| 53 | Chicago | 21.45 | 485,769 | 6 | - | - | - | 60 | measured |
| 54 | Haarlem | 10.72 | 33,960 | 21 | 1 | 2 | 277 | 20 | measured |
| 55 | Madrid | 13.18 | 274,553 | 17 | 11 | 2 | - | 60 | measured |
| 56 | Glasgow | 20.04 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 57 | Asheville | 20.89 | - | - | - | - | - | 20 | predicted (travel demand) |
| 58 | Long Beach | 20.48 | - | - | - | - | - | 30 | predicted (travel demand) |
| 59 | Athens | 20.04 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 60 | Little Rock | 20.40 | - | - | - | - | - | 20 | predicted (travel demand) |
| 61 | Boston | 19.34 | 385,902 | 11 | 2 | 1 | - | 30 | measured |
| 62 | Warsaw | 13.36 | 197,929 | 39 | 5 | 4 | 1407 | 60 | measured |
| 63 | Sardinia | 11.07 | - | 5 | 4 | - | 8 | 60 | measured |
| 64 | Las Vegas | 19.69 | - | 11 | - | 2 | - | 30 | measured |
| 65 | Coimbra | 10.55 | 34,962 | 4 | - | - | 5 | 20 | measured |
| 66 | Kyoto | 12.30 | 142,353 | 18 | 12 | 2 | - | 60 | measured |
| 67 | Oakland | 18.81 | - | - | - | - | - | 30 | predicted (travel demand) |
| 68 | Lexington | 18.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 69 | Reno | 18.19 | - | - | - | - | - | 30 | predicted (travel demand) |
| 70 | Des Moines | 18.11 | - | - | - | - | - | 20 | predicted (travel demand) |
| 71 | Daytona Beach | 17.66 | - | - | - | - | - | 20 | predicted (travel demand) |
| 72 | Madeira | 10.37 | - | 10 | 1 | 1 | - | 30 | measured |
| 73 | Ottawa | 11.43 | - | 21 | - | 3 | 122 | 60 | measured |
| 74 | Copenhagen | 16.17 | 218,621 | 42 | 34 | 6 | - | 30 | measured |
| 75 | Chattanooga | 16.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 76 | San Francisco | 16.17 | 361,111 | 6 | 1 | 1 | - | 30 | measured |
| 77 | Geneva | 10.90 | 162,269 | 21 | 5 | 4 | 131 | 20 | measured |
| 78 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 79 | Leiden | 7.91 | 33,227 | 20 | 6 | 1 | 129 | 20 | measured |
| 80 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 81 | Washington DC | 14.06 | 606,731 | 15 | 1 | 3 | - | 30 | measured |
| 82 | Huntsville | 15.35 | - | - | - | - | - | 20 | predicted (travel demand) |
| 83 | Reykjavik | 13.18 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 84 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 85 | Vilnius | 10.02 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 86 | West Palm Beach | 14.98 | - | - | - | - | - | 20 | predicted (travel demand) |
| 87 | Saint Petersburg | 14.83 | - | - | - | - | - | 100 | predicted (travel demand) |
| 88 | St. Louis | 14.80 | - | - | - | - | - | 30 | predicted (travel demand) |
| 89 | Granada | 8.96 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 90 | Tampa | 14.10 | - | - | - | - | - | 30 | predicted (travel demand) |
| 91 | Tilburg | 6.86 | - | 20 | - | 3 | 87 | 20 | measured |
| 92 | Kanazawa | 8.79 | 25,778 | 7 | 2 | 1 | 2 | 30 | measured |
| 93 | Seattle | 13.01 | 398,724 | 6 | 1 | - | - | 30 | measured |
| 94 | Osaka | 8.61 | 163,112 | 6 | 1 | - | - | 60 | measured |
| 95 | Cincinnati | 13.33 | - | - | - | - | - | 30 | predicted (travel demand) |
| 96 | Lansing | 13.02 | - | - | - | - | - | 20 | predicted (travel demand) |
| 97 | Hobart | 8.61 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 98 | Montreal | 12.66 | 315,322 | 13 | 1 | 2 | - | 60 | measured |
| 99 | Parma | 7.03 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 100 | Detroit | 12.53 | - | - | - | - | - | 30 | predicted (travel demand) |
| 101 | Groningen | 6.15 | 31,401 | 21 | 1 | 2 | 76 | 20 | measured |
| 102 | Melbourne | 8.09 | 267,898 | 16 | - | 2 | 403 | 100 | measured |
| 103 | Eindhoven | 5.98 | - | 21 | - | 4 | 195 | 20 | measured |
| 104 | Denver | 11.66 | - | - | - | - | - | 30 | predicted (travel demand) |
| 105 | Bari | 6.86 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 106 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 60 | predicted (travel demand) |
| 107 | San Jose | 11.39 | - | - | - | - | - | 60 | predicted (travel demand) |
| 108 | Sacramento | 11.32 | - | - | - | - | - | 30 | predicted (travel demand) |
| 109 | Jersey City | 10.08 | - | - | - | - | - | 30 | predicted (travel demand) |
| 110 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 60 | predicted (travel demand) |
| 111 | Leipzig | 7.38 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 112 | Dubai | 11.02 | 334,167 | - | - | - | - | 60 | predicted (travel demand) |
| 113 | Sorrento | 5.45 | 40,049 | 7 | - | 1 | 20 | 10 | measured |
| 114 | Pittsburgh | 10.55 | - | 4 | - | 1 | - | 30 | measured |
| 115 | Milwaukee | 10.63 | - | - | - | - | - | 30 | predicted (travel demand) |
| 116 | Naples | 5.27 | 198,913 | 24 | 3 | 3 | 46 | 30 | measured |
| 117 | Segovia | 6.50 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 118 | Salt Lake City | 10.31 | - | - | - | - | - | 20 | predicted (travel demand) |
| 119 | Atlanta | 10.29 | - | - | - | - | - | 30 | predicted (travel demand) |
| 120 | Ibiza | 6.50 | - | 1 | - | - | 4 | 20 | measured |
| 121 | Anchorage | 10.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 122 | Amersfoort | 5.10 | - | 18 | 1 | 2 | 181 | 20 | measured |
| 123 | Spokane | 7.38 | - | 13 | - | 2 | 18 | 20 | measured |
| 124 | Raleigh | 10.07 | - | - | - | - | - | 30 | predicted (travel demand) |
| 125 | Budapest | 9.67 | 283,807 | 12 | 1 | 3 | - | 60 | measured |
| 126 | Bali | 9.95 | - | - | - | - | - | 60 | predicted (travel demand) |
| 127 | Cleveland | 9.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 128 | El Paso | 9.70 | - | - | - | - | - | 30 | predicted (travel demand) |
| 129 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 130 | Leeuwarden | 4.75 | - | 41 | - | 2 | 61 | 20 | measured |
| 131 | Miami | 9.48 | 278,558 | - | - | - | - | 30 | predicted (travel demand) |
| 132 | Edmonton | 9.38 | - | - | - | - | - | 60 | predicted (travel demand) |
| 133 | Winnipeg | 9.21 | - | - | - | - | - | 30 | predicted (travel demand) |
| 134 | Crete | 9.14 | - | 4 | 3 | - | - | 30 | measured |
| 135 | Nashville | 8.93 | - | - | - | - | - | 30 | predicted (travel demand) |
| 136 | Hoorn | 4.39 | - | 12 | - | 2 | 52 | 20 | measured |
| 137 | Sydney | 8.61 | 305,304 | 7 | 1 | - | - | 100 | measured |
| 138 | Tampere | 8.78 | - | - | - | - | - | 30 | predicted (travel demand) |
| 139 | Bordeaux | 5.80 | 156,201 | 10 | - | 2 | 211 | 30 | measured |
| 140 | Toronto | 8.44 | 411,011 | 6 | - | - | - | 60 | measured |
| 141 | Yakushima | 5.45 | - | 2 | - | - | 1 | 10 | measured |
| 142 | Zurich | 8.26 | 140,788 | 6 | 1 | - | - | 30 | measured |
| 143 | Ann Arbor | 8.55 | - | - | - | - | - | 20 | predicted (travel demand) |
| 144 | Seoul | 7.91 | 206,265 | 8 | 5 | 1 | - | 100 | measured |
| 145 | Guimaraes | 4.39 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 146 | Adelaide | 8.14 | 139,166 | - | - | - | - | 60 | predicted (travel demand) |
| 147 | Stockholm | 6.50 | 188,184 | 6 | 4 | - | - | 30 | measured |
| 148 | Tallinn | 5.45 | 124,888 | 9 | 3 | 2 | 42 | 30 | measured |
| 149 | Savannah | 8.09 | 128,162 | 2 | 1 | - | - | 20 | measured |
| 150 | Maastricht | 4.04 | 47,763 | 19 | - | 2 | 135 | 20 | measured |
| 151 | Catania | 4.75 | 58,252 | 4 | 3 | 1 | 5 | 30 | measured |
| 152 | Dubrovnik | 7.56 | 119,586 | 4 | 1 | - | 2 | 10 | measured |
| 153 | Strasbourg | 5.27 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 154 | Charleston | 7.73 | 155,987 | 2 | 1 | - | - | 20 | measured |
| 155 | Cyprus | 7.73 | - | 4 | - | - | - | 60 | measured |
| 156 | Albuquerque | 7.83 | - | - | - | - | - | 30 | predicted (travel demand) |
| 157 | Dordrecht | 3.87 | - | 20 | 1 | 2 | 105 | 20 | measured |
| 158 | Cambridge | 7.73 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 159 | Verona | 4.57 | 77,646 | 8 | 4 | 1 | 3 | 30 | measured |
| 160 | Menorca | 4.92 | - | 6 | - | - | 2 | 20 | measured |
| 161 | Leuven | 7.56 | 40,645 | 4 | - | - | - | 20 | measured |
| 162 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 20 | predicted (travel demand) |
| 163 | Boise | 7.38 | - | 4 | - | 1 | - | 20 | measured |
| 164 | Helsinki | 5.80 | 148,908 | 12 | 2 | 1 | 13 | 30 | measured |
| 165 | Bergen | 7.30 | 82,940 | - | - | - | - | 30 | predicted (travel demand) |
| 166 | Christchurch | 4.83 | 104,874 | - | - | - | 444 | 30 | predicted (travel demand) |
| 167 | Potsdam | 4.75 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 168 | Quebec City | 4.75 | 124,358 | 6 | - | 1 | 494 | 30 | measured |
| 169 | Genoa | 3.87 | 145,206 | 13 | 2 | 1 | 10 | 30 | measured |
| 170 | Nice | 7.03 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 171 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 20 | predicted (travel demand) |
| 172 | Siena | 4.62 | 57,436 | - | - | - | - | 20 | predicted (travel demand) |
| 173 | Istanbul | 6.06 | 333,027 | 14 | 4 | 1 | - | 100 | measured |
| 174 | Vancouver | 6.68 | 351,552 | 7 | - | - | - | 30 | measured |
| 175 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 20 | predicted (travel demand) |
| 176 | Caserta | 3.34 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 177 | Helmond | 3.34 | - | 20 | - | 2 | 54 | 20 | measured |
| 178 | Liverpool | 6.68 | 248,189 | 2 | 1 | - | - | 30 | measured |
| 179 | Oslo | 5.80 | 181,113 | 4 | - | - | - | 30 | measured |
| 180 | Girona | 3.87 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 181 | Luxembourg City | 4.39 | 64,851 | 10 | 5 | 2 | 18 | 20 | measured |
| 182 | Sapporo | 4.39 | 88,633 | 6 | - | - | - | 60 | measured |
| 183 | Zagreb | 6.42 | 122,890 | - | - | - | - | 30 | predicted (travel demand) |
| 184 | Bogota | 6.39 | 1,623 | - | - | - | - | 100 | predicted (travel demand) |
| 185 | Shanghai | 6.38 | 277,140 | - | - | - | - | 100 | predicted (travel demand) |
| 186 | Beijing | 6.33 | 269,737 | 7 | 1 | - | - | 100 | measured |
| 187 | Bristol | 6.33 | 163,983 | 6 | 2 | - | - | 30 | measured |
| 188 | Hong Kong | 4.22 | 689,212 | 10 | 4 | 1 | 505 | 100 | measured |
| 189 | Lyon | 4.22 | 136,951 | 13 | 4 | 1 | 156 | 30 | measured |
| 190 | Funchal | 3.77 | 174,351 | - | - | - | - | 20 | predicted (travel demand) |
| 191 | Perth | 5.98 | 180,478 | 6 | 3 | 1 | - | 60 | measured |
| 192 | Enschede | 2.99 | - | 15 | 1 | 2 | 82 | 20 | measured |
| 193 | Minneapolis | 5.98 | - | 4 | - | - | - | 30 | measured |
| 194 | Padua | 3.16 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 195 | Hawaii | 5.27 | - | 6 | - | 1 | 6 | 60 | measured |
| 196 | Malta | 5.79 | - | - | - | - | - | 30 | predicted (travel demand) |
| 197 | Ljubljana | 5.63 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 198 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 199 | Avignon | 5.54 | 64,047 | - | - | - | - | 20 | predicted (travel demand) |
| 200 | Cordoba | 3.52 | 74,675 | 16 | 2 | 2 | 3 | 30 | measured |
| 201 | Galway | 3.65 | 88,162 | - | - | - | - | 20 | predicted (travel demand) |
| 202 | Phuket | 5.46 | 5,487 | - | - | - | - | 30 | predicted (travel demand) |
| 203 | Rovaniemi | 5.38 | - | - | - | - | - | 20 | predicted (travel demand) |
| 204 | Lagos | 3.43 | 34,452 | - | - | - | - | 100 | predicted (travel demand) |
| 205 | Salzburg | 3.52 | 107,243 | 9 | 3 | 2 | 34 | 20 | measured |
| 206 | Bologna | 2.81 | 146,161 | 12 | 7 | 1 | 9 | 30 | measured |
| 207 | Santa Fe | 5.17 | - | - | - | - | - | 20 | predicted (travel demand) |
| 208 | Lund | 5.14 | - | - | - | - | - | 20 | predicted (travel demand) |
| 209 | Kobe | 3.40 | 54,798 | - | - | - | - | 60 | predicted (travel demand) |
| 210 | Heraklion | 4.96 | 66,359 | - | - | - | - | 20 | predicted (travel demand) |
| 211 | Marseille | 4.96 | 182,033 | - | - | - | - | 30 | predicted (travel demand) |
| 212 | Bergamo | 2.46 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 213 | Zwolle | 2.46 | - | 16 | - | 2 | 56 | 20 | measured |
| 214 | Bangkok | 4.66 | 222,206 | 5 | 1 | 1 | - | 100 | measured |
| 215 | Indianapolis | 4.57 | - | 1 | - | - | - | 30 | measured |
| 216 | Basel | 4.59 | 105,838 | - | - | - | - | 20 | predicted (travel demand) |
| 217 | Alkmaar | 2.29 | - | 14 | - | 2 | 79 | 20 | measured |
| 218 | Den Bosch | 2.29 | 39,682 | 12 | 2 | 1 | 118 | 20 | measured |
| 219 | Tasmania | 4.41 | - | - | - | - | - | 30 | predicted (travel demand) |
| 220 | Manchester | 4.39 | 316,438 | 5 | - | - | - | 30 | measured |
| 221 | Taipei | 4.39 | 143,193 | 4 | 1 | - | - | 60 | measured |
| 222 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 20 | predicted (travel demand) |
| 223 | Cologne | 4.22 | 191,812 | 5 | - | 1 | - | 60 | measured |
| 224 | Como | 2.11 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 225 | Hilversum | 2.11 | - | 6 | 1 | 1 | 122 | 20 | measured |
| 226 | Dresden | 2.81 | 113,624 | 5 | 5 | 1 | - | 30 | measured |
| 227 | San Sebastian | 2.80 | 367 | - | - | - | - | 20 | predicted (travel demand) |
| 228 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 30 | predicted (travel demand) |
| 229 | Pisa | 2.64 | 52,174 | 4 | - | - | - | 20 | measured |
| 230 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 231 | Nantes | 4.04 | 67,689 | 1 | 1 | - | - | 30 | measured |
| 232 | Bilbao | 2.64 | 133,133 | 4 | - | 1 | - | 30 | measured |
| 233 | Toulouse | 2.64 | 112,721 | 10 | - | 1 | 34 | 30 | measured |
| 234 | Stuttgart | 2.99 | 112,789 | 6 | 1 | - | - | 30 | measured |
| 235 | Azores | 2.62 | - | - | - | - | - | 20 | predicted (travel demand) |
| 236 | San Diego | 3.87 | 214,939 | 4 | 1 | 1 | - | 60 | measured |
| 237 | Turin | 1.93 | 147,456 | 11 | 7 | 2 | 30 | 30 | measured |
| 238 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 239 | Niagara Falls | 3.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 240 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 100 | predicted (travel demand) |
| 241 | Cardiff | 3.69 | - | 4 | - | 1 | - | 30 | measured |
| 242 | Bratislava | 2.46 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 243 | Split | 3.69 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 244 | Wellington | 3.60 | 132,267 | - | - | - | - | 20 | predicted (travel demand) |
| 245 | Fort Lauderdale | 3.52 | - | 4 | - | - | - | 20 | measured |
| 246 | Assen | 1.76 | - | 10 | - | 2 | 66 | 20 | measured |
| 247 | Heerlen | 1.76 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 248 | Tulsa | 3.52 | - | 1 | - | - | - | 30 | measured |
| 249 | York | 3.52 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 250 | Montpellier | 3.47 | 64,238 | - | - | - | - | 30 | predicted (travel demand) |
| 251 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 252 | Cape Town | 3.29 | 199,169 | - | - | - | - | 60 | predicted (travel demand) |
| 253 | Rhodes | 3.42 | 127,205 | - | - | - | - | 20 | predicted (travel demand) |
| 254 | San Antonio | 3.32 | - | 4 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 255 | Perugia | 1.76 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 256 | Chania | 3.30 | 47,379 | - | - | - | - | 20 | predicted (travel demand) |
| 257 | Hilo | 2.46 | - | 6 | - | 1 | 16 | 10 | measured |
| 258 | Santiago | 3.25 | 111,647 | - | - | - | - | 100 | predicted (travel demand) |
| 259 | Oxford | 3.16 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 260 | Nagoya | 2.11 | 83,437 | 6 | 1 | - | 1 | 60 | measured |
| 261 | Salamanca | 2.11 | 47,897 | 4 | - | 1 | 1 | 20 | measured |
| 262 | Mexico City | 2.99 | 566,583 | 9 | 2 | - | - | 100 | measured |
| 263 | Delft | 1.58 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 264 | Heidelberg | 2.81 | 75,837 | 6 | 1 | 1 | - | 20 | measured |
| 265 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 30 | predicted (travel demand) |
| 266 | Freiburg | 2.99 | 92,752 | 7 | 2 | 1 | - | 20 | measured |
| 267 | Ghent | 2.99 | 82,757 | 8 | 1 | 1 | - | 30 | measured |
| 268 | Lucerne | 3.10 | 66,356 | - | - | - | - | 20 | predicted (travel demand) |
| 269 | Regensburg | 2.81 | 51,930 | 5 | 1 | 1 | 4 | 20 | measured |
| 270 | Malmo | 3.07 | 103,940 | - | - | - | - | 30 | predicted (travel demand) |
| 271 | Ferrara | 1.76 | 27,490 | 5 | 3 | 1 | 7 | 20 | measured |
| 272 | Lille | 3.06 | 73,435 | - | - | - | - | 20 | predicted (travel demand) |
| 273 | Corsica | 3.00 | - | - | - | - | - | 30 | predicted (travel demand) |
| 274 | Mechelen | 2.93 | 20,707 | - | - | - | - | 20 | predicted (travel demand) |
| 275 | Gdansk | 1.93 | 4,908 | 12 | 4 | 1 | 307 | 30 | measured |
| 276 | Kauai | 2.46 | - | 6 | 1 | - | 8 | 20 | measured |
| 277 | Lucca | 1.41 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 278 | Trieste | 1.41 | 117,233 | 36 | 1 | 3 | 43 | 20 | measured |
| 279 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 280 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 281 | Corfu | 2.71 | 139,334 | - | - | - | - | 20 | predicted (travel demand) |
| 282 | Ronda | 1.58 | 51,510 | 6 | 1 | - | 9 | 10 | measured |
| 283 | Matera | 1.58 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 284 | Belgrade | 2.64 | 178,116 | 5 | 5 | - | - | 60 | measured |
| 285 | Nuremberg | 1.76 | 161,614 | 12 | 1 | 1 | 38 | 30 | measured |
| 286 | Syracuse | 1.75 | 102,833 | - | - | - | - | 20 | predicted (travel demand) |
| 287 | Hamburg | 2.46 | 191,221 | 6 | 1 | 1 | - | 60 | measured |
| 288 | Cartagena | 2.58 | 65,066 | - | - | - | - | 30 | predicted (travel demand) |
| 289 | Gran Canaria | 1.67 | - | - | - | - | - | 30 | predicted (travel demand) |
| 290 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 20 | predicted (travel demand) |
| 291 | Bern | 2.51 | 90,627 | - | - | - | - | 20 | predicted (travel demand) |
| 292 | Riga | 2.46 | 108,918 | 5 | 2 | - | - | 30 | measured |
| 293 | Deventer | 1.23 | - | 12 | - | 1 | 213 | 20 | measured |
| 294 | Trento | 1.23 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 295 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 296 | Faro | 1.62 | 55,645 | - | - | - | - | 20 | predicted (travel demand) |
| 297 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 298 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 299 | Cusco | 2.35 | 87,732 | - | - | - | - | 30 | predicted (travel demand) |
| 300 | Limerick | 1.57 | 90,379 | - | - | - | - | 20 | predicted (travel demand) |
| 301 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 20 | predicted (travel demand) |
| 302 | Frankfurt | 1.41 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 303 | Kansas City | 2.11 | - | 4 | - | 1 | - | 30 | measured |
| 304 | Thessaloniki | 2.11 | 180,145 | 4 | - | 1 | - | 30 | measured |
| 305 | Roosendaal | 1.05 | - | 8 | - | 1 | 116 | 20 | measured |
| 306 | Tarragona | 1.23 | 32,396 | 4 | 2 | - | - | 20 | measured |
| 307 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 308 | Ischia | 1.32 | - | - | - | - | 2 | 20 | predicted (travel demand) |
| 309 | Izmir | 1.88 | 69,826 | - | - | - | - | 60 | predicted (travel demand) |
| 310 | Belfast | 1.93 | 224,315 | 4 | - | 1 | - | 30 | measured |
| 311 | Rio de Janeiro | 1.85 | 279,431 | 6 | - | - | - | 100 | measured |
| 312 | Auckland | 1.23 | 152,056 | 5 | 2 | - | 977 | 60 | measured |
| 313 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 314 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 315 | Breda | 0.88 | 36,579 | 10 | - | 2 | 118 | 20 | measured |
| 316 | Rotterdam | 0.88 | 104,938 | 12 | - | 2 | 83 | 30 | measured |
| 317 | Dijon | 1.72 | 43,526 | - | - | - | - | 20 | predicted (travel demand) |
| 318 | Trier | 1.56 | 69,369 | - | - | - | - | 20 | predicted (travel demand) |
| 319 | Annecy | 1.69 | 56,859 | - | - | - | - | 20 | predicted (travel demand) |
| 320 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 321 | Canterbury | 1.59 | 53,301 | - | - | - | - | 20 | predicted (travel demand) |
| 322 | Hallstatt | 1.41 | 47,271 | 5 | 1 | - | - | 10 | measured |
| 323 | Braga | 0.88 | 34,522 | 4 | 2 | - | 8 | 20 | measured |
| 324 | Graz | 1.05 | 65,717 | 12 | 7 | 1 | 87 | 30 | measured |
| 325 | Hiroshima | 1.05 | 129,791 | 33 | 5 | 2 | - | 60 | measured |
| 326 | Lausanne | 1.58 | 68,242 | 8 | 1 | 1 | - | 20 | measured |
| 327 | Mostar | 1.58 | 63,907 | - | - | - | - | 20 | predicted (travel demand) |
| 328 | Zadar | 1.53 | 71,549 | - | - | - | - | 20 | predicted (travel demand) |
| 329 | Buenos Aires | 1.41 | 333,331 | 4 | 2 | - | - | 60 | measured |
| 330 | Modena | 0.88 | 51,698 | 5 | 1 | 1 | 3 | 20 | measured |
| 331 | Brighton | 1.41 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 332 | Bruges | 1.41 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 333 | Apeldoorn | 0.70 | - | 10 | - | 2 | 80 | 20 | measured |
| 334 | Sofia | 0.88 | 138,710 | 4 | - | - | - | 60 | measured |
| 335 | Wroclaw | 0.88 | 123,894 | 5 | 1 | 1 | 121 | 30 | measured |
| 336 | Antalya | 1.31 | 70,688 | - | - | - | - | 60 | predicted (travel demand) |
| 337 | Setubal | 0.70 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 338 | Colmar | 1.28 | 45,517 | - | - | - | - | 20 | predicted (travel demand) |
| 339 | Bodrum | 1.26 | 33,918 | - | - | - | - | 20 | predicted (travel demand) |
| 340 | Rothenburg ob der Tauber | 1.05 | 39,879 | 4 | - | 1 | 8 | 10 | measured |
| 341 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 342 | Evora | 0.78 | 15,345 | - | - | - | - | 20 | predicted (travel demand) |
| 343 | Kamakura | 0.70 | 33,492 | 6 | - | - | - | 20 | measured |
| 344 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 345 | Maui | 1.05 | - | 4 | - | - | 3 | 20 | measured |
| 346 | Okinawa | 0.71 | 24,466 | 6 | - | - | 1 | 30 | published, never ranked (may be uncrawled) |
| 347 | Aarhus | 1.05 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 348 | Baltimore | 1.05 | - | 4 | - | - | - | 30 | measured |
| 349 | Busan | 1.05 | 94,737 | 2 | - | - | - | 60 | measured |
| 350 | La Palma | 0.70 | - | - | - | - | - | 20 | predicted (travel demand) |
| 351 | Brno | 0.70 | 63,714 | 8 | 5 | 2 | 34 | 30 | measured |
| 352 | Canberra | 1.05 | - | 1 | 1 | - | - | 30 | measured |
| 353 | Cesky Krumlov | 0.70 | 28,582 | 6 | 3 | - | 11 | 10 | measured |
| 354 | Turku | 1.05 | - | 1 | - | - | - | 20 | measured |
| 355 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 60 | predicted (travel demand) |
| 356 | Bamberg | 0.70 | 28,716 | 5 | 4 | 1 | 10 | 20 | measured |
| 357 | Rouen | 0.70 | 72,334 | 12 | - | 1 | 6 | 20 | measured |
| 358 | Venlo | 0.35 | - | 7 | - | 1 | 144 | 20 | measured |
| 359 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 100 | published, never ranked (may be uncrawled) |
| 360 | Assisi | 0.35 | 30,278 | 6 | 1 | 2 | 6 | 10 | measured |
| 361 | Phoenix | 0.55 | - | - | - | - | - | 60 | predicted (travel demand) |
| 362 | Bucharest | 0.53 | 136,836 | 4 | - | 1 | - | 60 | measured |
| 363 | Gothenburg | 0.53 | 119,991 | 5 | - | 1 | - | 30 | measured |
| 364 | Zaragoza | 0.35 | 87,580 | 7 | - | 1 | - | 30 | measured |
| 365 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 366 | Toledo | 0.24 | 3,149 | - | - | - | - | 20 | predicted (travel demand) |
| 367 | Fort Worth | 0.35 | - | 4 | - | - | - | 30 | measured |
| 368 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 369 | George Town | 0.28 | 36,080 | - | - | - | - | 30 | predicted (travel demand) |
| 370 | Poznan | 0.18 | 65,666 | 10 | - | 1 | 397 | 30 | measured |
| 371 | Allentown | 0.24 | - | - | - | - | - | 20 | predicted (travel demand) |
| 372 | Oss | 0.11 | - | 6 | - | - | 48 | 20 | published, never ranked (may be uncrawled) |
| 373 | Antwerp | 0.18 | 128,289 | 10 | 4 | 1 | - | 30 | measured |
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

