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
| 1 | Oahu | 82.20 | - | 21 | 5 | 3 | 163 | 30 | measured |
| 2 | Lisbon | 55.48 | 201,877 | 36 | 16 | 3 | 67 | 30 | measured |
| 3 | Barcelona | 51.76 | 346,477 | 56 | 14 | 7 | 180 | 60 | measured |
| 4 | Amsterdam | 47.02 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 5 | Singapore | 61.23 | 967,821 | 34 | 7 | 3 | 165 | 100 | measured |
| 6 | Brussels | 58.69 | 176,863 | 35 | 4 | 2 | 436 | 60 | measured |
| 7 | Rome | 38.56 | 358,876 | 31 | 10 | 2 | 32 | 60 | measured |
| 8 | Pamplona | 44.65 | 128,065 | 14 | - | 1 | 9 | 20 | measured |
| 9 | Berlin | 48.54 | 412,181 | 33 | 23 | 3 | 195 | 60 | measured |
| 10 | Palermo | 35.52 | 124,310 | 21 | 9 | 1 | 37 | 30 | measured |
| 11 | Tokyo | 38.56 | 394,702 | 22 | 15 | 1 | 5 | 100 | measured |
| 12 | Arnhem | 34.50 | 31,478 | 39 | 3 | 3 | 204 | 20 | measured |
| 13 | Tenerife | 44.31 | - | 4 | 4 | - | - | 30 | measured |
| 14 | Seville | 41.78 | 170,545 | 43 | 9 | 2 | - | 30 | measured |
| 15 | New York | 54.12 | 1,124,326 | 20 | 5 | 2 | - | 100 | measured |
| 16 | Prague | 37.21 | 303,350 | 30 | 21 | 4 | 31 | 60 | measured |
| 17 | Alicante | 27.57 | 77,454 | 21 | 4 | 2 | 44 | 30 | measured |
| 18 | Portland | 32.81 | 217,222 | 20 | 1 | 2 | 301 | 30 | measured |
| 19 | Vienna | 31.63 | 283,090 | 32 | 19 | 5 | 376 | 60 | measured |
| 20 | Bath | 46.68 | 144,950 | 5 | 2 | 1 | - | 20 | measured |
| 21 | Munich | 30.78 | 224,067 | 45 | 15 | 6 | 80 | 60 | measured |
| 22 | Paris | 27.91 | 524,268 | 31 | 9 | 4 | 129 | 60 | measured |
| 23 | Brisbane | 27.74 | 162,602 | 20 | 2 | 2 | 186 | 60 | measured |
| 24 | Porto | 20.80 | 120,415 | 27 | 15 | 2 | 40 | 30 | measured |
| 25 | Austin | 40.93 | 226,631 | 5 | 2 | - | - | 30 | measured |
| 26 | Malaga | 26.89 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 27 | Milan | 19.79 | 212,705 | 30 | 14 | 3 | 25 | 60 | measured |
| 28 | Dublin | 21.99 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 29 | Florence | 18.94 | 184,099 | 27 | 9 | 1 | 27 | 30 | measured |
| 30 | Birmingham | 37.53 | - | - | - | - | - | 60 | predicted (travel demand) |
| 31 | Los Angeles | 34.17 | 665,559 | 8 | 2 | - | - | 60 | measured |
| 32 | Valencia | 16.91 | 162,209 | 31 | 4 | 2 | 350 | 30 | measured |
| 33 | Cadiz | 20.30 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 34 | Cagliari | 16.41 | 51,351 | 14 | 1 | 2 | 15 | 20 | measured |
| 35 | Edinburgh | 29.77 | 292,981 | 16 | 5 | 1 | - | 30 | measured |
| 36 | Utrecht | 14.38 | 67,963 | 30 | 7 | 2 | 339 | 30 | measured |
| 37 | Krakow | 18.94 | 140,824 | 38 | 8 | 3 | 198 | 30 | measured |
| 38 | London | 23.85 | 718,291 | 23 | 16 | 1 | - | 100 | measured |
| 39 | Monterey | 27.74 | - | 3 | 1 | - | - | 10 | measured |
| 40 | Sintra | 13.36 | 46,889 | 5 | 3 | - | 6 | 30 | measured |
| 41 | Sao Paulo | 25.03 | 911 | 1 | - | - | - | 100 | measured |
| 42 | Dallas | 25.37 | - | 9 | 1 | 1 | - | 60 | measured |
| 43 | Houston | 25.03 | - | 6 | - | - | - | 60 | measured |
| 44 | The Hague | 12.01 | 236,723 | 31 | 2 | 5 | 167 | 30 | measured |
| 45 | Madrid | 14.55 | 274,553 | 17 | 11 | 2 | - | 60 | measured |
| 46 | New Orleans | 23.00 | 256,232 | 6 | 2 | 1 | - | 30 | measured |
| 47 | Jacksonville | 22.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 48 | Venice | 12.35 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 49 | Palma de Mallorca | 13.19 | 84,075 | 5 | 1 | 1 | 8 | 30 | measured |
| 50 | Athens | 21.31 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 51 | Nijmegen | 10.82 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 52 | Philadelphia | 20.30 | 405,294 | 1 | - | - | - | 60 | measured |
| 53 | Chicago | 20.97 | 485,769 | 6 | - | - | - | 60 | measured |
| 54 | Asheville | 20.89 | - | - | - | - | - | 20 | predicted (travel demand) |
| 55 | Haarlem | 10.32 | 33,960 | 21 | 1 | 2 | 277 | 20 | measured |
| 56 | Long Beach | 20.48 | - | - | - | - | - | 30 | predicted (travel demand) |
| 57 | Little Rock | 20.40 | - | - | - | - | - | 20 | predicted (travel demand) |
| 58 | Warsaw | 13.53 | 197,929 | 39 | 5 | 4 | 1407 | 60 | measured |
| 59 | Boston | 19.28 | 385,902 | 11 | 2 | 1 | - | 30 | measured |
| 60 | Glasgow | 19.28 | 253,705 | 5 | 2 | - | - | 30 | measured |
| 61 | Fukuoka | 12.35 | 77,485 | 15 | 9 | 1 | - | 60 | measured |
| 62 | Oakland | 18.81 | - | - | - | - | - | 30 | predicted (travel demand) |
| 63 | Lexington | 18.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 64 | Reno | 18.19 | - | - | - | - | - | 30 | predicted (travel demand) |
| 65 | Des Moines | 18.11 | - | - | - | - | - | 20 | predicted (travel demand) |
| 66 | Coimbra | 9.81 | 34,962 | 5 | - | - | 5 | 20 | measured |
| 67 | Sardinia | 9.98 | - | 5 | 4 | - | 8 | 60 | measured |
| 68 | Kyoto | 11.50 | 142,353 | 18 | 12 | 2 | - | 60 | measured |
| 69 | Cork | 11.84 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 70 | Daytona Beach | 17.66 | - | - | - | - | - | 20 | predicted (travel demand) |
| 71 | Las Vegas | 17.25 | - | 11 | - | 2 | - | 30 | measured |
| 72 | Chattanooga | 16.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 73 | Washington DC | 14.88 | 606,731 | 15 | 1 | 3 | - | 30 | measured |
| 74 | Copenhagen | 15.73 | 218,621 | 42 | 34 | 6 | - | 30 | measured |
| 75 | San Francisco | 15.90 | 361,111 | 6 | 1 | 1 | - | 30 | measured |
| 76 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 77 | Granada | 9.98 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 78 | Ottawa | 10.49 | - | 21 | - | 3 | 122 | 60 | measured |
| 79 | Geneva | 10.32 | 162,269 | 21 | 5 | 4 | 131 | 20 | measured |
| 80 | Huntsville | 15.35 | - | - | - | - | - | 20 | predicted (travel demand) |
| 81 | Leiden | 7.61 | 33,227 | 20 | 6 | 1 | 129 | 20 | measured |
| 82 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 83 | West Palm Beach | 14.98 | - | - | - | - | - | 20 | predicted (travel demand) |
| 84 | Saint Petersburg | 14.83 | - | - | - | - | - | 100 | predicted (travel demand) |
| 85 | St. Louis | 14.80 | - | - | - | - | - | 30 | predicted (travel demand) |
| 86 | Madeira | 8.80 | - | 10 | 1 | 1 | - | 30 | measured |
| 87 | Osaka | 9.30 | 163,112 | 6 | 1 | - | - | 60 | measured |
| 88 | Seattle | 13.87 | 398,724 | 6 | 1 | - | - | 30 | measured |
| 89 | Reykjavik | 12.35 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 90 | Tampa | 14.10 | - | - | - | - | - | 30 | predicted (travel demand) |
| 91 | Montreal | 13.70 | 315,322 | 13 | 1 | 2 | - | 60 | measured |
| 92 | Parma | 7.44 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 93 | Cincinnati | 13.33 | - | - | - | - | - | 30 | predicted (travel demand) |
| 94 | Kanazawa | 8.63 | 25,778 | 7 | 2 | 1 | 2 | 30 | measured |
| 95 | Sorrento | 6.60 | 40,049 | 7 | - | 1 | 20 | 10 | measured |
| 96 | Lansing | 13.02 | - | - | - | - | - | 20 | predicted (travel demand) |
| 97 | Vilnius | 8.63 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 98 | Detroit | 12.53 | - | - | - | - | - | 30 | predicted (travel demand) |
| 99 | Eindhoven | 6.26 | - | 21 | - | 4 | 195 | 20 | measured |
| 100 | Hobart | 7.95 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 101 | Melbourne | 7.78 | 267,898 | 16 | - | 2 | 403 | 100 | measured |
| 102 | Denver | 11.66 | - | - | - | - | - | 30 | predicted (travel demand) |
| 103 | Budapest | 11.16 | 283,807 | 13 | 1 | 3 | - | 60 | measured |
| 104 | Groningen | 5.75 | 31,401 | 21 | 1 | 2 | 76 | 20 | measured |
| 105 | Tilburg | 5.75 | - | 20 | - | 3 | 87 | 20 | measured |
| 106 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 60 | predicted (travel demand) |
| 107 | San Jose | 11.39 | - | - | - | - | - | 60 | predicted (travel demand) |
| 108 | Sacramento | 11.32 | - | - | - | - | - | 30 | predicted (travel demand) |
| 109 | Jersey City | 10.08 | - | - | - | - | - | 30 | predicted (travel demand) |
| 110 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 60 | predicted (travel demand) |
| 111 | Naples | 5.58 | 198,913 | 24 | 3 | 3 | 46 | 30 | measured |
| 112 | Segovia | 6.93 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 113 | Dubai | 11.02 | 334,167 | - | - | - | - | 60 | predicted (travel demand) |
| 114 | Leipzig | 7.27 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 115 | Amersfoort | 5.41 | - | 18 | 1 | 2 | 181 | 20 | measured |
| 116 | Ibiza | 6.77 | - | 1 | - | - | 4 | 20 | measured |
| 117 | Pittsburgh | 10.49 | - | 4 | - | 1 | - | 30 | measured |
| 118 | Milwaukee | 10.63 | - | - | - | - | - | 30 | predicted (travel demand) |
| 119 | Salt Lake City | 10.31 | - | - | - | - | - | 20 | predicted (travel demand) |
| 120 | Atlanta | 10.29 | - | - | - | - | - | 30 | predicted (travel demand) |
| 121 | Anchorage | 10.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 122 | Bari | 6.09 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 123 | Leeuwarden | 5.07 | - | 41 | - | 2 | 61 | 20 | measured |
| 124 | Raleigh | 10.07 | - | - | - | - | - | 30 | predicted (travel demand) |
| 125 | Liverpool | 9.98 | 248,189 | 2 | 1 | - | - | 30 | measured |
| 126 | Bali | 9.95 | - | - | - | - | - | 60 | predicted (travel demand) |
| 127 | Spokane | 7.10 | - | 13 | - | 2 | 18 | 20 | measured |
| 128 | Cleveland | 9.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 129 | El Paso | 9.70 | - | - | - | - | - | 30 | predicted (travel demand) |
| 130 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 131 | Cyprus | 9.30 | - | 4 | - | - | - | 60 | measured |
| 132 | Miami | 9.48 | 278,558 | - | - | - | - | 30 | predicted (travel demand) |
| 133 | Edmonton | 9.38 | - | - | - | - | - | 60 | predicted (travel demand) |
| 134 | Winnipeg | 9.21 | - | - | - | - | - | 30 | predicted (travel demand) |
| 135 | Charleston | 8.80 | 155,987 | 2 | 1 | - | - | 20 | measured |
| 136 | Nashville | 8.93 | - | - | - | - | - | 30 | predicted (travel demand) |
| 137 | Tampere | 8.78 | - | - | - | - | - | 30 | predicted (travel demand) |
| 138 | Guimaraes | 4.57 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 139 | Seoul | 8.12 | 206,265 | 8 | 5 | 1 | - | 100 | measured |
| 140 | Crete | 8.63 | - | 4 | 3 | - | - | 30 | measured |
| 141 | Toronto | 8.46 | 411,011 | 6 | - | - | - | 60 | measured |
| 142 | Ann Arbor | 8.55 | - | - | - | - | - | 20 | predicted (travel demand) |
| 143 | Maastricht | 4.23 | 47,763 | 19 | - | 2 | 135 | 20 | measured |
| 144 | Adelaide | 8.14 | 139,166 | - | - | - | - | 60 | predicted (travel demand) |
| 145 | Sydney | 8.12 | 305,304 | 7 | 1 | - | - | 100 | measured |
| 146 | Dubrovnik | 7.78 | 119,586 | 4 | 1 | - | 2 | 10 | measured |
| 147 | Cambridge | 8.12 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 148 | Strasbourg | 5.41 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 149 | Helsinki | 6.43 | 148,908 | 12 | 2 | 1 | 13 | 30 | measured |
| 150 | Zurich | 7.78 | 140,788 | 6 | 1 | - | - | 30 | measured |
| 151 | Catania | 4.74 | 58,252 | 4 | 3 | 1 | 5 | 30 | measured |
| 152 | Verona | 4.74 | 77,646 | 8 | 4 | 1 | 3 | 30 | measured |
| 153 | Stockholm | 6.26 | 188,184 | 6 | 4 | - | - | 30 | measured |
| 154 | Sapporo | 5.24 | 88,633 | 6 | - | - | - | 60 | measured |
| 155 | Albuquerque | 7.83 | - | - | - | - | - | 30 | predicted (travel demand) |
| 156 | Yakushima | 4.90 | - | 2 | - | - | 1 | 10 | measured |
| 157 | Luxembourg City | 5.07 | 64,851 | 10 | 5 | 2 | 18 | 20 | measured |
| 158 | Quebec City | 5.07 | 124,358 | 6 | - | 1 | 494 | 30 | measured |
| 159 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 20 | predicted (travel demand) |
| 160 | Caserta | 3.72 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 161 | Hoorn | 3.72 | - | 12 | - | 2 | 52 | 20 | measured |
| 162 | Leuven | 7.44 | 40,645 | 4 | - | - | - | 20 | measured |
| 163 | Savannah | 7.44 | 128,162 | 2 | 1 | - | - | 20 | measured |
| 164 | Bordeaux | 4.90 | 156,201 | 10 | - | 2 | 211 | 30 | measured |
| 165 | Tallinn | 4.90 | 124,888 | 9 | 3 | 2 | 42 | 30 | measured |
| 166 | Bergen | 7.30 | 82,940 | - | - | - | - | 30 | predicted (travel demand) |
| 167 | Dordrecht | 3.55 | - | 20 | 1 | 2 | 105 | 20 | measured |
| 168 | Minneapolis | 7.10 | - | 4 | - | - | - | 30 | measured |
| 169 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 20 | predicted (travel demand) |
| 170 | Siena | 4.62 | 57,436 | - | - | - | - | 20 | predicted (travel demand) |
| 171 | Girona | 4.06 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 172 | Potsdam | 4.57 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 173 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 20 | predicted (travel demand) |
| 174 | Boise | 6.77 | - | 4 | - | 1 | - | 20 | measured |
| 175 | Enschede | 3.38 | - | 15 | 1 | 2 | 82 | 20 | measured |
| 176 | Istanbul | 5.92 | 333,027 | 14 | 4 | 1 | - | 100 | measured |
| 177 | Lyon | 4.40 | 136,951 | 13 | 4 | 1 | 156 | 30 | measured |
| 178 | Zagreb | 6.42 | 122,890 | - | - | - | - | 30 | predicted (travel demand) |
| 179 | Bristol | 6.43 | 163,983 | 6 | 2 | - | - | 30 | measured |
| 180 | Bogota | 6.39 | 1,623 | - | - | - | - | 100 | predicted (travel demand) |
| 181 | Shanghai | 6.38 | 277,140 | - | - | - | - | 100 | predicted (travel demand) |
| 182 | Funchal | 3.77 | 174,351 | - | - | - | - | 20 | predicted (travel demand) |
| 183 | Menorca | 4.06 | - | 6 | - | - | 2 | 20 | measured |
| 184 | Hong Kong | 4.14 | 689,212 | 10 | 4 | 1 | 505 | 100 | measured |
| 185 | Oslo | 5.41 | 181,113 | 4 | - | - | - | 30 | measured |
| 186 | Nice | 6.09 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 187 | Vancouver | 5.92 | 351,552 | 7 | - | - | - | 30 | measured |
| 188 | Padua | 3.21 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 189 | Perth | 5.75 | 180,478 | 6 | 3 | 1 | - | 60 | measured |
| 190 | Malta | 5.79 | - | - | - | - | - | 30 | predicted (travel demand) |
| 191 | Helmond | 2.88 | - | 20 | - | 2 | 54 | 20 | measured |
| 192 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 193 | Hawaii | 5.07 | - | 6 | - | 1 | 6 | 60 | measured |
| 194 | Beijing | 5.67 | 269,737 | 7 | 1 | - | - | 100 | measured |
| 195 | Avignon | 5.54 | 64,047 | - | - | - | - | 20 | predicted (travel demand) |
| 196 | Cordoba | 3.55 | 74,675 | 16 | 2 | 2 | 3 | 30 | measured |
| 197 | Galway | 3.65 | 88,162 | - | - | - | - | 20 | predicted (travel demand) |
| 198 | Phuket | 5.46 | 5,487 | - | - | - | - | 30 | predicted (travel demand) |
| 199 | Rovaniemi | 5.38 | - | - | - | - | - | 20 | predicted (travel demand) |
| 200 | Ljubljana | 5.24 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 201 | Salzburg | 3.55 | 107,243 | 12 | 3 | 2 | 34 | 20 | measured |
| 202 | Lagos | 3.43 | 34,452 | - | - | - | - | 100 | predicted (travel demand) |
| 203 | Genoa | 2.88 | 145,206 | 13 | 2 | 1 | 10 | 30 | measured |
| 204 | Santa Fe | 5.17 | - | - | - | - | - | 20 | predicted (travel demand) |
| 205 | Lund | 5.14 | - | - | - | - | - | 20 | predicted (travel demand) |
| 206 | Kobe | 3.40 | 54,798 | - | - | - | - | 60 | predicted (travel demand) |
| 207 | Heraklion | 4.96 | 66,359 | - | - | - | - | 20 | predicted (travel demand) |
| 208 | Marseille | 4.96 | 182,033 | - | - | - | - | 30 | predicted (travel demand) |
| 209 | Taipei | 4.90 | 143,193 | 4 | 1 | - | - | 60 | measured |
| 210 | Indianapolis | 4.74 | - | 1 | - | - | - | 30 | measured |
| 211 | Bergamo | 2.37 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 212 | Den Bosch | 2.37 | 39,682 | 12 | 2 | 1 | 118 | 20 | measured |
| 213 | Bologna | 2.54 | 146,161 | 12 | 7 | 1 | 9 | 30 | measured |
| 214 | Cardiff | 4.57 | - | 4 | - | 1 | - | 30 | measured |
| 215 | Basel | 4.59 | 105,838 | - | - | - | - | 20 | predicted (travel demand) |
| 216 | Manchester | 4.57 | 316,438 | 5 | - | - | - | 30 | measured |
| 217 | Tasmania | 4.41 | - | - | - | - | - | 30 | predicted (travel demand) |
| 218 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 20 | predicted (travel demand) |
| 219 | San Sebastian | 2.80 | 367 | - | - | - | - | 20 | predicted (travel demand) |
| 220 | Nagoya | 2.71 | 83,437 | 6 | 1 | - | 1 | 60 | measured |
| 221 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 30 | predicted (travel demand) |
| 222 | Alkmaar | 2.03 | - | 14 | - | 2 | 79 | 20 | measured |
| 223 | Cologne | 4.06 | 191,812 | 5 | - | 1 | - | 60 | measured |
| 224 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 225 | Key West | 3.95 | - | - | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 226 | Azores | 2.62 | - | - | - | - | - | 20 | predicted (travel demand) |
| 227 | Pisa | 2.54 | 52,174 | 4 | - | - | - | 20 | measured |
| 228 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 229 | Niagara Falls | 3.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 230 | Bilbao | 2.54 | 133,133 | 4 | - | 1 | - | 30 | measured |
| 231 | Toulouse | 2.54 | 112,721 | 10 | - | 1 | 34 | 30 | measured |
| 232 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 100 | predicted (travel demand) |
| 233 | Tulsa | 3.72 | - | 1 | - | - | - | 30 | measured |
| 234 | Zwolle | 1.86 | - | 20 | - | 4 | 58 | 20 | measured |
| 235 | Wellington | 3.60 | 132,267 | - | - | - | - | 20 | predicted (travel demand) |
| 236 | Stuttgart | 2.71 | 112,789 | 6 | 1 | - | - | 30 | measured |
| 237 | Bratislava | 2.37 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 238 | Frankfurt | 2.37 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 239 | Nuremberg | 2.37 | 161,614 | 12 | 1 | 1 | 38 | 30 | measured |
| 240 | Ferrara | 2.03 | 27,490 | 5 | 3 | 1 | 7 | 20 | measured |
| 241 | Montpellier | 3.47 | 64,238 | - | - | - | - | 30 | predicted (travel demand) |
| 242 | Fort Lauderdale | 3.38 | - | 4 | - | - | - | 20 | measured |
| 243 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 244 | Cape Town | 3.29 | 199,169 | - | - | - | - | 60 | predicted (travel demand) |
| 245 | Rhodes | 3.42 | 127,205 | - | - | - | - | 20 | predicted (travel demand) |
| 246 | Como | 1.69 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 247 | Deventer | 1.69 | - | 12 | - | 1 | 213 | 20 | measured |
| 248 | Hilversum | 1.69 | - | 6 | 1 | 1 | 122 | 20 | measured |
| 249 | Nantes | 3.38 | 67,689 | 1 | 1 | - | - | 30 | measured |
| 250 | Ghent | 3.21 | 82,757 | 8 | 1 | 1 | - | 30 | measured |
| 251 | San Antonio | 3.32 | - | 4 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 252 | Bangkok | 3.30 | 222,206 | 5 | 1 | 1 | - | 100 | measured |
| 253 | Chania | 3.30 | 47,379 | - | - | - | - | 20 | predicted (travel demand) |
| 254 | Dresden | 2.20 | 113,624 | 5 | 5 | 1 | - | 30 | measured |
| 255 | Santiago | 3.25 | 111,647 | - | - | - | - | 100 | predicted (travel demand) |
| 256 | York | 3.21 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 257 | Perugia | 1.69 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 258 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 30 | predicted (travel demand) |
| 259 | Hilo | 2.37 | - | 6 | - | 1 | 16 | 10 | measured |
| 260 | Lucerne | 3.10 | 66,356 | - | - | - | - | 20 | predicted (travel demand) |
| 261 | Salamanca | 2.03 | 47,897 | 4 | - | 1 | 1 | 20 | measured |
| 262 | Malmo | 3.07 | 103,940 | - | - | - | - | 30 | predicted (travel demand) |
| 263 | Lille | 3.06 | 73,435 | - | - | - | - | 20 | predicted (travel demand) |
| 264 | Assen | 1.52 | - | 10 | - | 2 | 66 | 20 | measured |
| 265 | Delft | 1.52 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 266 | Heerlen | 1.52 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 267 | Lucca | 1.52 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 268 | Turin | 1.52 | 147,456 | 11 | 7 | 2 | 30 | 30 | measured |
| 269 | Corsica | 3.00 | - | - | - | - | - | 30 | predicted (travel demand) |
| 270 | Freiburg | 2.88 | 92,752 | 7 | 2 | 1 | - | 20 | measured |
| 271 | Mechelen | 2.93 | 20,707 | - | - | - | - | 20 | predicted (travel demand) |
| 272 | Mexico City | 2.71 | 566,583 | 9 | 2 | - | - | 100 | measured |
| 273 | Matera | 1.69 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 274 | Gdansk | 1.86 | 4,908 | 12 | 4 | 1 | 307 | 30 | measured |
| 275 | Regensburg | 2.54 | 51,930 | 5 | 1 | 1 | 4 | 20 | measured |
| 276 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 277 | Oxford | 2.71 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 278 | Kauai | 2.37 | - | 6 | 1 | - | 8 | 20 | measured |
| 279 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 280 | Corfu | 2.71 | 139,334 | - | - | - | - | 20 | predicted (travel demand) |
| 281 | San Diego | 2.71 | 214,939 | 4 | 1 | 1 | - | 60 | measured |
| 282 | Roosendaal | 1.35 | - | 8 | - | 1 | 116 | 20 | measured |
| 283 | Trento | 1.35 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 284 | Trieste | 1.35 | 117,233 | 36 | 1 | 3 | 43 | 20 | measured |
| 285 | Heidelberg | 2.37 | 75,837 | 6 | 1 | 1 | - | 20 | measured |
| 286 | Belgrade | 2.62 | 178,116 | 5 | 5 | - | - | 60 | measured |
| 287 | Syracuse | 1.75 | 102,833 | - | - | - | - | 20 | predicted (travel demand) |
| 288 | Cartagena | 2.58 | 65,066 | - | - | - | - | 30 | predicted (travel demand) |
| 289 | Ronda | 1.52 | 51,510 | 6 | 1 | - | 9 | 10 | measured |
| 290 | Gran Canaria | 1.67 | - | - | - | - | - | 30 | predicted (travel demand) |
| 291 | Tarragona | 1.52 | 32,396 | 4 | 2 | - | - | 20 | measured |
| 292 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 20 | predicted (travel demand) |
| 293 | Bern | 2.51 | 90,627 | - | - | - | - | 20 | predicted (travel demand) |
| 294 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 295 | Faro | 1.62 | 55,645 | - | - | - | - | 20 | predicted (travel demand) |
| 296 | Riga | 2.37 | 108,918 | 5 | 2 | - | - | 30 | measured |
| 297 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 298 | Kansas City | 2.37 | - | 4 | - | 1 | - | 30 | measured |
| 299 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 300 | Cusco | 2.35 | 87,732 | - | - | - | - | 30 | predicted (travel demand) |
| 301 | Limerick | 1.57 | 90,379 | - | - | - | - | 20 | predicted (travel demand) |
| 302 | Hamburg | 2.20 | 191,221 | 6 | 1 | 1 | - | 60 | measured |
| 303 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 20 | predicted (travel demand) |
| 304 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 305 | Ischia | 1.32 | - | - | - | - | 2 | 20 | predicted (travel demand) |
| 306 | Thessaloniki | 2.03 | 180,145 | 4 | - | 1 | - | 30 | measured |
| 307 | Breda | 1.01 | 36,579 | 11 | - | 2 | 120 | 20 | measured |
| 308 | Izmir | 1.88 | 69,826 | - | - | - | - | 60 | predicted (travel demand) |
| 309 | Aarhus | 1.86 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 310 | Setubal | 1.01 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 311 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 312 | Christchurch | 1.21 | 104,874 | 6 | - | 1 | 466 | 30 | published, never ranked (may be uncrawled) |
| 313 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 314 | Graz | 1.18 | 65,717 | 13 | 7 | 2 | 87 | 30 | measured |
| 315 | Dijon | 1.72 | 43,526 | - | - | - | - | 20 | predicted (travel demand) |
| 316 | Trier | 1.56 | 69,369 | - | - | - | - | 20 | predicted (travel demand) |
| 317 | Annecy | 1.69 | 56,859 | - | - | - | - | 20 | predicted (travel demand) |
| 318 | Bruges | 1.69 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 319 | Split | 1.69 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 320 | Modena | 1.01 | 51,698 | 5 | 1 | 1 | 3 | 20 | measured |
| 321 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 322 | Canterbury | 1.59 | 53,301 | - | - | - | - | 20 | predicted (travel demand) |
| 323 | Mostar | 1.58 | 63,907 | - | - | - | - | 20 | predicted (travel demand) |
| 324 | Braga | 0.85 | 34,522 | 4 | 2 | - | 8 | 20 | measured |
| 325 | Zadar | 1.53 | 71,549 | - | - | - | - | 20 | predicted (travel demand) |
| 326 | Auckland | 1.01 | 152,056 | 5 | 2 | - | 977 | 60 | measured |
| 327 | Hiroshima | 1.01 | 129,791 | 33 | 5 | 2 | - | 60 | measured |
| 328 | Rio de Janeiro | 1.44 | 279,431 | 6 | - | - | - | 100 | measured |
| 329 | Baltimore | 1.35 | - | 4 | - | - | - | 30 | measured |
| 330 | Apeldoorn | 0.68 | - | 10 | - | 2 | 80 | 20 | measured |
| 331 | Rotterdam | 0.68 | 104,938 | 16 | - | 2 | 83 | 30 | measured |
| 332 | Belfast | 1.35 | 224,315 | 5 | - | 1 | - | 30 | measured |
| 333 | Lausanne | 1.35 | 68,242 | 8 | 1 | 1 | - | 20 | measured |
| 334 | Antalya | 1.31 | 70,688 | - | - | - | - | 60 | predicted (travel demand) |
| 335 | Colmar | 1.28 | 45,517 | - | - | - | - | 20 | predicted (travel demand) |
| 336 | Brno | 0.85 | 63,714 | 8 | 5 | 2 | 34 | 30 | measured |
| 337 | Cesky Krumlov | 0.85 | 28,582 | 6 | 3 | - | 11 | 10 | measured |
| 338 | Sofia | 0.85 | 138,710 | 4 | - | - | - | 60 | measured |
| 339 | Bodrum | 1.26 | 33,918 | - | - | - | - | 20 | predicted (travel demand) |
| 340 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 341 | Buenos Aires | 1.18 | 333,331 | 4 | 2 | - | - | 60 | measured |
| 342 | Evora | 0.78 | 15,345 | - | - | - | - | 20 | predicted (travel demand) |
| 343 | Hallstatt | 1.01 | 47,271 | 5 | 1 | - | - | 10 | measured |
| 344 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 345 | Kamakura | 0.68 | 33,492 | 6 | - | - | - | 20 | measured |
| 346 | La Palma | 0.70 | - | - | - | - | - | 20 | predicted (travel demand) |
| 347 | Rothenburg ob der Tauber | 0.85 | 39,879 | 4 | - | 1 | 8 | 10 | measured |
| 348 | Wroclaw | 0.68 | 123,894 | 5 | 1 | 1 | 121 | 30 | measured |
| 349 | Brighton | 1.01 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 350 | Turku | 1.01 | - | 1 | - | - | - | 20 | measured |
| 351 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 60 | predicted (travel demand) |
| 352 | Busan | 0.85 | 94,737 | 2 | - | - | - | 60 | measured |
| 353 | Bamberg | 0.68 | 28,716 | 5 | 4 | 1 | 10 | 20 | measured |
| 354 | Zaragoza | 0.51 | 87,580 | 7 | - | 1 | - | 30 | measured |
| 355 | Rouen | 0.68 | 72,334 | 12 | - | 1 | 6 | 20 | measured |
| 356 | Maui | 0.68 | - | 4 | - | - | 3 | 20 | measured |
| 357 | Canberra | 0.68 | - | 1 | 1 | - | - | 30 | measured |
| 358 | Venlo | 0.34 | - | 7 | - | 1 | 144 | 20 | measured |
| 359 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 100 | published, never ranked (may be uncrawled) |
| 360 | Assisi | 0.34 | 30,278 | 6 | 1 | 2 | 6 | 10 | measured |
| 361 | Phoenix | 0.55 | - | - | - | - | - | 60 | predicted (travel demand) |
| 362 | Bucharest | 0.51 | 136,836 | 4 | - | 1 | - | 60 | measured |
| 363 | Gothenburg | 0.51 | 119,991 | 5 | - | 1 | - | 30 | measured |
| 364 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 365 | Toledo | 0.24 | 3,149 | - | - | - | - | 20 | predicted (travel demand) |
| 366 | Fort Worth | 0.34 | - | 4 | - | - | - | 30 | measured |
| 367 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 368 | George Town | 0.28 | 36,080 | - | - | - | - | 30 | predicted (travel demand) |
| 369 | Okinawa | 0.17 | 24,466 | 6 | - | - | 1 | 30 | measured |
| 370 | Poznan | 0.17 | 65,666 | 10 | - | 1 | 397 | 30 | measured |
| 371 | Allentown | 0.24 | - | - | - | - | - | 20 | predicted (travel demand) |
| 372 | Oss | 0.11 | - | 6 | - | - | 48 | 20 | published, never ranked (may be uncrawled) |
| 373 | Antwerp | 0.17 | 128,289 | 10 | 4 | 1 | - | 30 | measured |
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

