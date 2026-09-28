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
| 1 | Oahu | 72.62 | - | 21 | 5 | 3 | 163 | 30 | measured |
| 2 | Lisbon | 53.87 | 201,877 | 36 | 16 | 3 | 67 | 30 | measured |
| 3 | Amsterdam | 48.41 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 4 | Barcelona | 48.41 | 346,477 | 56 | 14 | 7 | 180 | 60 | measured |
| 5 | Singapore | 61.20 | 967,821 | 34 | 7 | 3 | 165 | 100 | measured |
| 6 | Rome | 37.67 | 358,876 | 31 | 10 | 2 | 32 | 60 | measured |
| 7 | Palermo | 36.82 | 124,310 | 21 | 9 | 1 | 37 | 30 | measured |
| 8 | New York | 64.10 | 1,124,326 | 20 | 5 | 2 | - | 100 | measured |
| 9 | Seville | 44.15 | 170,545 | 43 | 10 | 2 | - | 30 | measured |
| 10 | Tokyo | 35.63 | 394,702 | 22 | 15 | 1 | 5 | 100 | measured |
| 11 | Tenerife | 41.08 | - | 4 | 4 | - | - | 30 | measured |
| 12 | Berlin | 38.19 | 412,181 | 33 | 23 | 3 | 195 | 60 | measured |
| 13 | Munich | 35.12 | 224,067 | 45 | 15 | 6 | 80 | 60 | measured |
| 14 | Dublin | 28.64 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 15 | Alicante | 24.89 | 77,454 | 21 | 4 | 2 | 44 | 30 | measured |
| 16 | Bath | 43.47 | 144,950 | 5 | 2 | 1 | - | 20 | measured |
| 17 | Brussels | 28.30 | 176,863 | 35 | 4 | 2 | 436 | 60 | measured |
| 18 | Porto | 21.14 | 120,415 | 27 | 15 | 2 | 40 | 30 | measured |
| 19 | Brisbane | 27.79 | 162,602 | 20 | 2 | 2 | 186 | 60 | measured |
| 20 | Paris | 27.79 | 524,268 | 31 | 9 | 4 | 129 | 60 | measured |
| 21 | Malaga | 27.45 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 22 | Vienna | 27.45 | 283,090 | 32 | 19 | 5 | 376 | 60 | measured |
| 23 | Birmingham | 37.53 | - | - | - | - | - | 60 | predicted (travel demand) |
| 24 | Pamplona | 21.31 | 128,065 | 14 | - | 1 | 9 | 20 | measured |
| 25 | Los Angeles | 32.05 | 665,559 | 10 | 2 | - | - | 60 | measured |
| 26 | Cadiz | 21.31 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 27 | Cagliari | 17.73 | 51,351 | 14 | 1 | 2 | 15 | 20 | measured |
| 28 | Portland | 21.48 | 217,222 | 24 | 1 | 2 | 306 | 30 | measured |
| 29 | Arnhem | 15.68 | 31,478 | 39 | 3 | 3 | 204 | 20 | measured |
| 30 | Austin | 31.03 | 226,631 | 9 | 2 | 1 | - | 30 | measured |
| 31 | Houston | 30.69 | - | 6 | - | - | - | 60 | measured |
| 32 | Edinburgh | 29.49 | 292,981 | 16 | 5 | 1 | - | 30 | measured |
| 33 | Prague | 19.95 | 303,350 | 30 | 21 | 4 | 31 | 60 | measured |
| 34 | Milan | 14.83 | 212,705 | 30 | 14 | 3 | 25 | 60 | measured |
| 35 | Sintra | 14.83 | 46,889 | 5 | 3 | - | 6 | 30 | measured |
| 36 | London | 25.06 | 718,291 | 23 | 16 | 1 | - | 100 | measured |
| 37 | Florence | 14.66 | 184,099 | 27 | 9 | 1 | 27 | 30 | measured |
| 38 | The Hague | 14.32 | 236,723 | 31 | 2 | 5 | 167 | 30 | measured |
| 39 | New Orleans | 28.30 | 256,232 | 8 | 5 | 1 | - | 30 | measured |
| 40 | Palma de Mallorca | 16.20 | 84,075 | 5 | 1 | 1 | 8 | 30 | measured |
| 41 | Valencia | 13.13 | 162,209 | 31 | 4 | 2 | 350 | 30 | measured |
| 42 | Sao Paulo | 25.14 | 911 | 1 | - | - | - | 100 | measured |
| 43 | Madrid | 15.85 | 274,553 | 17 | 11 | 2 | - | 60 | measured |
| 44 | Chicago | 24.55 | 485,769 | 6 | - | - | - | 60 | measured |
| 45 | Dallas | 23.18 | - | 12 | 1 | 1 | - | 60 | measured |
| 46 | Nijmegen | 11.59 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 47 | Jacksonville | 22.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 48 | Athens | 22.16 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 49 | Krakow | 15.00 | 140,824 | 38 | 8 | 3 | 198 | 30 | measured |
| 50 | Monterey | 21.82 | - | 3 | 1 | - | - | 10 | measured |
| 51 | Venice | 11.59 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 52 | Asheville | 20.89 | - | - | - | - | - | 20 | predicted (travel demand) |
| 53 | Long Beach | 20.48 | - | - | - | - | - | 30 | predicted (travel demand) |
| 54 | Little Rock | 20.40 | - | - | - | - | - | 20 | predicted (travel demand) |
| 55 | Glasgow | 18.75 | 253,705 | 5 | 3 | - | - | 30 | measured |
| 56 | Boston | 18.41 | 385,902 | 12 | 2 | 2 | - | 30 | measured |
| 57 | San Francisco | 18.75 | 361,111 | 6 | 1 | 1 | - | 30 | measured |
| 58 | Oakland | 18.81 | - | - | - | - | - | 30 | predicted (travel demand) |
| 59 | Utrecht | 9.21 | 67,963 | 30 | 7 | 2 | 339 | 30 | measured |
| 60 | Sardinia | 10.23 | - | 5 | 4 | - | 8 | 60 | measured |
| 61 | Warsaw | 12.27 | 197,929 | 39 | 14 | 4 | 1407 | 60 | measured |
| 62 | Lexington | 18.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 63 | Reno | 18.19 | - | - | - | - | - | 30 | predicted (travel demand) |
| 64 | Des Moines | 18.11 | - | - | - | - | - | 20 | predicted (travel demand) |
| 65 | Daytona Beach | 17.66 | - | - | - | - | - | 20 | predicted (travel demand) |
| 66 | Coimbra | 9.55 | 34,962 | 5 | - | - | 5 | 20 | measured |
| 67 | Cork | 11.59 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 68 | Seattle | 16.71 | 398,724 | 8 | 1 | 1 | - | 30 | measured |
| 69 | Hobart | 11.25 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 70 | Fukuoka | 10.91 | 77,485 | 15 | 9 | 1 | - | 60 | measured |
| 71 | Chattanooga | 16.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 72 | Washington DC | 14.66 | 606,731 | 15 | 1 | 3 | - | 30 | measured |
| 73 | Ottawa | 10.74 | - | 21 | - | 3 | 122 | 60 | measured |
| 74 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 75 | Reykjavik | 13.64 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 76 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 77 | Kanazawa | 10.23 | 25,778 | 7 | 2 | 1 | 2 | 30 | measured |
| 78 | Haarlem | 7.84 | 33,960 | 21 | 1 | 2 | 277 | 20 | measured |
| 79 | Madeira | 9.38 | - | 10 | 1 | 1 | - | 30 | measured |
| 80 | Huntsville | 15.35 | - | - | - | - | - | 20 | predicted (travel demand) |
| 81 | Leeuwarden | 7.67 | - | 41 | - | 2 | 61 | 20 | measured |
| 82 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 83 | Montreal | 15.00 | 315,322 | 13 | 1 | 2 | - | 60 | measured |
| 84 | West Palm Beach | 14.98 | - | - | - | - | - | 20 | predicted (travel demand) |
| 85 | Saint Petersburg | 14.83 | - | - | - | - | - | 100 | predicted (travel demand) |
| 86 | St. Louis | 14.80 | - | - | - | - | - | 30 | predicted (travel demand) |
| 87 | Naples | 7.33 | 198,913 | 24 | 3 | 3 | 46 | 30 | measured |
| 88 | Vilnius | 9.72 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 89 | Osaka | 9.04 | 163,112 | 6 | 1 | - | - | 60 | measured |
| 90 | Tampa | 14.10 | - | - | - | - | - | 30 | predicted (travel demand) |
| 91 | Las Vegas | 13.98 | - | 11 | - | 2 | - | 30 | measured |
| 92 | Spokane | 9.89 | - | 13 | - | 2 | 18 | 20 | measured |
| 93 | Amersfoort | 6.82 | - | 18 | 1 | 2 | 181 | 20 | measured |
| 94 | Kyoto | 8.69 | 142,353 | 18 | 12 | 2 | - | 60 | measured |
| 95 | Philadelphia | 12.96 | 405,294 | 4 | 1 | - | - | 60 | measured |
| 96 | Granada | 8.52 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 97 | Cincinnati | 13.33 | - | - | - | - | - | 30 | predicted (travel demand) |
| 98 | Copenhagen | 12.79 | 218,621 | 42 | 34 | 6 | - | 30 | measured |
| 99 | Liverpool | 13.30 | 248,189 | 2 | 1 | - | - | 30 | measured |
| 100 | Leipzig | 8.69 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 101 | Lansing | 13.02 | - | - | - | - | - | 20 | predicted (travel demand) |
| 102 | Ibiza | 8.01 | - | 1 | - | - | 4 | 20 | measured |
| 103 | Detroit | 12.53 | - | - | - | - | - | 30 | predicted (travel demand) |
| 104 | Eindhoven | 6.14 | - | 21 | - | 4 | 195 | 20 | measured |
| 105 | Geneva | 8.18 | 162,269 | 21 | 5 | 4 | 131 | 20 | measured |
| 106 | Melbourne | 8.01 | 267,898 | 16 | - | 2 | 403 | 100 | measured |
| 107 | Cyprus | 11.76 | - | 4 | - | - | - | 60 | measured |
| 108 | Sorrento | 5.97 | 40,049 | 7 | - | 1 | 20 | 10 | measured |
| 109 | Denver | 11.66 | - | - | - | - | - | 30 | predicted (travel demand) |
| 110 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 60 | predicted (travel demand) |
| 111 | San Jose | 11.39 | - | - | - | - | - | 60 | predicted (travel demand) |
| 112 | Sacramento | 11.32 | - | - | - | - | - | 30 | predicted (travel demand) |
| 113 | Jersey City | 10.08 | - | - | - | - | - | 30 | predicted (travel demand) |
| 114 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 60 | predicted (travel demand) |
| 115 | Dubai | 11.02 | 334,167 | - | - | - | - | 60 | predicted (travel demand) |
| 116 | Sydney | 10.74 | 305,304 | 7 | 1 | - | - | 100 | measured |
| 117 | Pittsburgh | 10.57 | - | 4 | - | 1 | - | 30 | measured |
| 118 | Milwaukee | 10.63 | - | - | - | - | - | 30 | predicted (travel demand) |
| 119 | Strasbourg | 6.99 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 120 | Verona | 6.14 | 77,646 | 8 | 4 | 1 | 3 | 30 | measured |
| 121 | Salt Lake City | 10.31 | - | - | - | - | - | 20 | predicted (travel demand) |
| 122 | Atlanta | 10.29 | - | - | - | - | - | 30 | predicted (travel demand) |
| 123 | Anchorage | 10.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 124 | Boise | 10.23 | - | 4 | - | 1 | - | 20 | measured |
| 125 | Leiden | 5.11 | 33,227 | 20 | 6 | 1 | 129 | 20 | measured |
| 126 | Raleigh | 10.07 | - | - | - | - | - | 30 | predicted (travel demand) |
| 127 | Bali | 9.95 | - | - | - | - | - | 60 | predicted (travel demand) |
| 128 | Seoul | 9.21 | 206,265 | 8 | 5 | 1 | - | 100 | measured |
| 129 | Segovia | 6.14 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 130 | Cleveland | 9.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 131 | El Paso | 9.70 | - | - | - | - | - | 30 | predicted (travel demand) |
| 132 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 133 | Maastricht | 4.77 | 47,763 | 19 | - | 2 | 135 | 20 | measured |
| 134 | Stockholm | 7.67 | 188,184 | 8 | 4 | - | - | 30 | measured |
| 135 | Miami | 9.48 | 278,558 | - | - | - | - | 30 | predicted (travel demand) |
| 136 | Edmonton | 9.38 | - | - | - | - | - | 60 | predicted (travel demand) |
| 137 | Girona | 5.46 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 138 | Winnipeg | 9.21 | - | - | - | - | - | 30 | predicted (travel demand) |
| 139 | Budapest | 8.69 | 283,807 | 13 | 1 | 3 | - | 60 | measured |
| 140 | Nashville | 8.93 | - | - | - | - | - | 30 | predicted (travel demand) |
| 141 | Bari | 5.28 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 142 | Crete | 8.86 | - | 4 | 3 | - | - | 30 | measured |
| 143 | Tampere | 8.78 | - | - | - | - | - | 30 | predicted (travel demand) |
| 144 | Tallinn | 5.80 | 124,888 | 9 | 3 | 2 | 42 | 30 | measured |
| 145 | Ann Arbor | 8.55 | - | - | - | - | - | 20 | predicted (travel demand) |
| 146 | Adelaide | 8.14 | 139,166 | - | - | - | - | 60 | predicted (travel demand) |
| 147 | Quebec City | 5.46 | 124,358 | 6 | - | 1 | 494 | 30 | measured |
| 148 | Groningen | 4.09 | 31,401 | 21 | 1 | 2 | 76 | 20 | measured |
| 149 | Toronto | 8.01 | 411,011 | 6 | - | - | - | 60 | measured |
| 150 | Charleston | 7.84 | 155,987 | 3 | 1 | - | - | 20 | measured |
| 151 | Zurich | 7.67 | 140,788 | 6 | 1 | - | - | 30 | measured |
| 152 | Parma | 4.43 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 153 | Dubrovnik | 7.50 | 119,586 | 4 | 1 | - | 2 | 10 | measured |
| 154 | Dordrecht | 3.92 | - | 20 | 1 | 2 | 105 | 20 | measured |
| 155 | Leuven | 7.84 | 40,645 | 4 | - | - | - | 20 | measured |
| 156 | Albuquerque | 7.83 | - | - | - | - | - | 30 | predicted (travel demand) |
| 157 | Luxembourg City | 5.11 | 64,851 | 10 | 5 | 2 | 18 | 20 | measured |
| 158 | Cambridge | 7.50 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 159 | Enschede | 3.75 | - | 15 | 1 | 2 | 82 | 20 | measured |
| 160 | Minneapolis | 7.50 | - | 4 | - | - | - | 30 | measured |
| 161 | Savannah | 7.50 | 128,162 | 3 | 1 | - | - | 20 | measured |
| 162 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 20 | predicted (travel demand) |
| 163 | Helsinki | 5.80 | 148,908 | 12 | 2 | 1 | 13 | 30 | measured |
| 164 | Bergen | 7.30 | 82,940 | - | - | - | - | 30 | predicted (travel demand) |
| 165 | Hawaii | 6.48 | - | 6 | - | 1 | 6 | 60 | measured |
| 166 | Caserta | 3.58 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 167 | Nice | 7.16 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 168 | Tilburg | 3.58 | - | 20 | - | 3 | 87 | 20 | measured |
| 169 | Zwolle | 3.58 | - | 20 | - | 4 | 58 | 20 | measured |
| 170 | Sapporo | 4.77 | 88,633 | 6 | - | - | - | 60 | measured |
| 171 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 20 | predicted (travel demand) |
| 172 | Siena | 4.62 | 57,436 | - | - | - | - | 20 | predicted (travel demand) |
| 173 | Guimaraes | 3.58 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 174 | Istanbul | 5.97 | 333,027 | 14 | 4 | 1 | - | 100 | measured |
| 175 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 20 | predicted (travel demand) |
| 176 | Vancouver | 6.65 | 351,552 | 7 | - | - | - | 30 | measured |
| 177 | Bologna | 3.58 | 146,161 | 12 | 7 | 1 | 9 | 30 | measured |
| 178 | Hong Kong | 4.43 | 689,212 | 10 | 4 | 1 | 505 | 100 | measured |
| 179 | Oslo | 5.80 | 181,113 | 4 | - | - | - | 30 | measured |
| 180 | Zagreb | 6.42 | 122,890 | - | - | - | - | 30 | predicted (travel demand) |
| 181 | Perth | 6.31 | 180,478 | 6 | 3 | 1 | - | 60 | measured |
| 182 | Bogota | 6.39 | 1,623 | - | - | - | - | 100 | predicted (travel demand) |
| 183 | Shanghai | 6.38 | 277,140 | - | - | - | - | 100 | predicted (travel demand) |
| 184 | Funchal | 3.77 | 174,351 | - | - | - | - | 20 | predicted (travel demand) |
| 185 | Frankfurt | 3.92 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 186 | Lyon | 3.92 | 136,951 | 13 | 4 | 1 | 156 | 30 | measured |
| 187 | Cordoba | 3.75 | 74,675 | 16 | 2 | 2 | 3 | 30 | measured |
| 188 | Bergamo | 2.90 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 189 | Catania | 3.41 | 58,252 | 4 | 3 | 1 | 5 | 30 | measured |
| 190 | Malta | 5.79 | - | - | - | - | - | 30 | predicted (travel demand) |
| 191 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 192 | Bristol | 5.63 | 163,983 | 6 | 2 | - | - | 30 | measured |
| 193 | Genoa | 3.07 | 145,206 | 13 | 2 | 1 | 10 | 30 | measured |
| 194 | Avignon | 5.54 | 64,047 | - | - | - | - | 20 | predicted (travel demand) |
| 195 | Galway | 3.65 | 88,162 | - | - | - | - | 20 | predicted (travel demand) |
| 196 | Phuket | 5.46 | 5,487 | - | - | - | - | 30 | predicted (travel demand) |
| 197 | Padua | 2.90 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 198 | Rovaniemi | 5.38 | - | - | - | - | - | 20 | predicted (travel demand) |
| 199 | Lagos | 3.43 | 34,452 | - | - | - | - | 100 | predicted (travel demand) |
| 200 | Menorca | 3.41 | - | 6 | - | - | 2 | 20 | measured |
| 201 | Santa Fe | 5.17 | - | - | - | - | - | 20 | predicted (travel demand) |
| 202 | Lund | 5.14 | - | - | - | - | - | 20 | predicted (travel demand) |
| 203 | Yakushima | 3.24 | - | 2 | - | - | 1 | 10 | measured |
| 204 | Kobe | 3.40 | 54,798 | - | - | - | - | 60 | predicted (travel demand) |
| 205 | Heraklion | 4.96 | 66,359 | - | - | - | - | 20 | predicted (travel demand) |
| 206 | Marseille | 4.96 | 182,033 | - | - | - | - | 30 | predicted (travel demand) |
| 207 | Bordeaux | 3.24 | 156,201 | 10 | - | 2 | 211 | 30 | measured |
| 208 | Helmond | 2.39 | - | 20 | - | 2 | 54 | 20 | measured |
| 209 | Manchester | 4.77 | 316,438 | 5 | - | - | - | 30 | measured |
| 210 | Taipei | 4.77 | 143,193 | 4 | 1 | - | - | 60 | measured |
| 211 | Beijing | 4.69 | 269,737 | 7 | 1 | - | - | 100 | measured |
| 212 | Nuremberg | 3.07 | 161,614 | 12 | 1 | 1 | 38 | 30 | measured |
| 213 | Basel | 4.59 | 105,838 | - | - | - | - | 20 | predicted (travel demand) |
| 214 | Alkmaar | 2.22 | - | 14 | - | 2 | 79 | 20 | measured |
| 215 | Den Bosch | 2.22 | 39,682 | 12 | 2 | 1 | 118 | 20 | measured |
| 216 | Hoorn | 2.22 | - | 12 | - | 2 | 52 | 20 | measured |
| 217 | Lucca | 2.22 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 218 | Tasmania | 4.41 | - | - | - | - | - | 30 | predicted (travel demand) |
| 219 | Ljubljana | 4.26 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 220 | Salzburg | 2.90 | 107,243 | 12 | 3 | 2 | 34 | 20 | measured |
| 221 | Toulouse | 2.90 | 112,721 | 10 | - | 1 | 34 | 30 | measured |
| 222 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 20 | predicted (travel demand) |
| 223 | Cologne | 4.26 | 191,812 | 5 | - | 1 | - | 60 | measured |
| 224 | San Sebastian | 2.80 | 367 | - | - | - | - | 20 | predicted (travel demand) |
| 225 | Salamanca | 2.73 | 47,897 | 4 | - | 1 | 1 | 20 | measured |
| 226 | Como | 2.05 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 227 | Deventer | 2.05 | - | 12 | - | 1 | 213 | 20 | measured |
| 228 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 30 | predicted (travel demand) |
| 229 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 230 | Heidelberg | 3.58 | 75,837 | 6 | 1 | 1 | - | 20 | measured |
| 231 | Kauai | 3.41 | - | 6 | 1 | - | 8 | 20 | measured |
| 232 | Azores | 2.62 | - | - | - | - | - | 20 | predicted (travel demand) |
| 233 | Nagoya | 2.56 | 83,437 | 6 | 1 | - | 1 | 60 | measured |
| 234 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 235 | Cardiff | 3.75 | - | 4 | - | 1 | - | 30 | measured |
| 236 | Niagara Falls | 3.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 237 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 100 | predicted (travel demand) |
| 238 | Apeldoorn | 1.88 | - | 10 | - | 2 | 80 | 20 | measured |
| 239 | Delft | 1.88 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 240 | Trieste | 1.88 | 117,233 | 36 | 1 | 3 | 43 | 20 | measured |
| 241 | Wellington | 3.60 | 132,267 | - | - | - | - | 20 | predicted (travel demand) |
| 242 | Hilo | 2.73 | - | 6 | - | 1 | 16 | 10 | measured |
| 243 | Bratislava | 2.39 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 244 | Perugia | 1.88 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 245 | Ronda | 2.05 | 51,510 | 6 | 1 | - | 9 | 10 | measured |
| 246 | Montpellier | 3.47 | 64,238 | - | - | - | - | 30 | predicted (travel demand) |
| 247 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 248 | Cape Town | 3.29 | 199,169 | - | - | - | - | 60 | predicted (travel demand) |
| 249 | Rhodes | 3.42 | 127,205 | - | - | - | - | 20 | predicted (travel demand) |
| 250 | Tulsa | 3.41 | - | 1 | - | - | - | 30 | measured |
| 251 | Assen | 1.70 | - | 10 | - | 2 | 66 | 20 | measured |
| 252 | Venlo | 1.70 | - | 7 | - | 1 | 144 | 20 | measured |
| 253 | Gdansk | 2.22 | 4,908 | 12 | 4 | 1 | 307 | 30 | measured |
| 254 | Graz | 2.22 | 65,717 | 13 | 7 | 2 | 87 | 30 | measured |
| 255 | San Antonio | 3.32 | - | 4 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 256 | Chania | 3.30 | 47,379 | - | - | - | - | 20 | predicted (travel demand) |
| 257 | Mexico City | 3.07 | 566,583 | 9 | 2 | - | - | 100 | measured |
| 258 | Santiago | 3.25 | 111,647 | - | - | - | - | 100 | predicted (travel demand) |
| 259 | Tarragona | 1.88 | 32,396 | 4 | 2 | - | - | 20 | measured |
| 260 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 30 | predicted (travel demand) |
| 261 | Stuttgart | 2.39 | 112,789 | 6 | 1 | - | - | 30 | measured |
| 262 | Oxford | 3.07 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 263 | Hallstatt | 2.73 | 47,271 | 5 | 1 | - | - | 10 | measured |
| 264 | Lucerne | 3.10 | 66,356 | - | - | - | - | 20 | predicted (travel demand) |
| 265 | Bilbao | 2.05 | 133,133 | 4 | - | 1 | - | 30 | measured |
| 266 | Malmo | 3.07 | 103,940 | - | - | - | - | 30 | predicted (travel demand) |
| 267 | Lille | 3.06 | 73,435 | - | - | - | - | 20 | predicted (travel demand) |
| 268 | Roosendaal | 1.53 | - | 8 | - | 1 | 116 | 20 | measured |
| 269 | Freiburg | 2.90 | 92,752 | 7 | 2 | 1 | - | 20 | measured |
| 270 | Corsica | 3.00 | - | - | - | - | - | 30 | predicted (travel demand) |
| 271 | Mechelen | 2.93 | 20,707 | - | - | - | - | 20 | predicted (travel demand) |
| 272 | Aarhus | 2.90 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 273 | Matera | 1.70 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 274 | Ghent | 2.73 | 82,757 | 8 | 1 | 1 | - | 30 | measured |
| 275 | Poznan | 1.89 | 65,666 | 10 | - | 1 | 397 | 30 | published, never ranked (may be uncrawled) |
| 276 | Brno | 1.88 | 63,714 | 8 | 5 | 2 | 34 | 30 | measured |
| 277 | Dresden | 1.88 | 113,624 | 5 | 5 | 1 | - | 30 | measured |
| 278 | Indianapolis | 2.73 | - | 1 | - | - | - | 30 | measured |
| 279 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 280 | Kansas City | 2.73 | - | 4 | - | 1 | - | 30 | measured |
| 281 | San Diego | 2.73 | 214,939 | 6 | 1 | 1 | - | 60 | measured |
| 282 | York | 2.73 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 283 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 284 | Heerlen | 1.36 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 285 | Corfu | 2.71 | 139,334 | - | - | - | - | 20 | predicted (travel demand) |
| 286 | Ferrara | 1.53 | 27,490 | 5 | 3 | 1 | 7 | 20 | measured |
| 287 | Syracuse | 1.75 | 102,833 | - | - | - | - | 20 | predicted (travel demand) |
| 288 | Cartagena | 2.58 | 65,066 | - | - | - | - | 30 | predicted (travel demand) |
| 289 | Gran Canaria | 1.67 | - | - | - | - | - | 30 | predicted (travel demand) |
| 290 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 20 | predicted (travel demand) |
| 291 | Bern | 2.51 | 90,627 | - | - | - | - | 20 | predicted (travel demand) |
| 292 | Setubal | 1.36 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 293 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 294 | Fort Lauderdale | 2.39 | - | 4 | - | - | - | 20 | measured |
| 295 | Faro | 1.62 | 55,645 | - | - | - | - | 20 | predicted (travel demand) |
| 296 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 297 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 298 | Pisa | 1.53 | 52,174 | 4 | - | - | - | 20 | measured |
| 299 | Cusco | 2.35 | 87,732 | - | - | - | - | 30 | predicted (travel demand) |
| 300 | Limerick | 1.57 | 90,379 | - | - | - | - | 20 | predicted (travel demand) |
| 301 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 20 | predicted (travel demand) |
| 302 | Bangkok | 2.22 | 222,206 | 5 | 1 | 1 | - | 100 | measured |
| 303 | Lausanne | 2.22 | 68,242 | 8 | 1 | 1 | - | 20 | measured |
| 304 | Nantes | 2.22 | 67,689 | 1 | 1 | - | - | 30 | measured |
| 305 | Hamburg | 2.05 | 191,221 | 6 | 1 | 1 | - | 60 | measured |
| 306 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 307 | Belfast | 2.05 | 224,315 | 5 | - | 1 | - | 30 | measured |
| 308 | Hilversum | 1.02 | - | 6 | 1 | 1 | 122 | 20 | measured |
| 309 | Trento | 1.02 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 310 | Turin | 1.02 | 147,456 | 11 | 7 | 2 | 30 | 30 | measured |
| 311 | Ischia | 1.32 | - | - | - | - | 2 | 20 | predicted (travel demand) |
| 312 | Izmir | 1.88 | 69,826 | - | - | - | - | 60 | predicted (travel demand) |
| 313 | Riga | 1.88 | 108,918 | 5 | 2 | - | - | 30 | measured |
| 314 | Bruges | 1.88 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 315 | Regensburg | 1.70 | 51,930 | 5 | 1 | 1 | 4 | 20 | measured |
| 316 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 317 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 318 | Cesky Krumlov | 1.19 | 28,582 | 6 | 3 | - | 11 | 10 | measured |
| 319 | Baltimore | 1.70 | - | 4 | - | - | - | 30 | measured |
| 320 | Dijon | 1.72 | 43,526 | - | - | - | - | 20 | predicted (travel demand) |
| 321 | Trier | 1.56 | 69,369 | - | - | - | - | 20 | predicted (travel demand) |
| 322 | Belgrade | 1.70 | 178,116 | 5 | 5 | - | - | 60 | measured |
| 323 | Rotterdam | 0.85 | 104,938 | 16 | - | 2 | 83 | 30 | measured |
| 324 | Annecy | 1.69 | 56,859 | - | - | - | - | 20 | predicted (travel demand) |
| 325 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 326 | Canterbury | 1.59 | 53,301 | - | - | - | - | 20 | predicted (travel demand) |
| 327 | Mostar | 1.58 | 63,907 | - | - | - | - | 20 | predicted (travel demand) |
| 328 | Zaragoza | 1.02 | 87,580 | 7 | - | 1 | - | 30 | measured |
| 329 | Auckland | 1.02 | 152,056 | 5 | 2 | - | 977 | 60 | measured |
| 330 | Braga | 0.85 | 34,522 | 4 | 2 | - | 8 | 20 | measured |
| 331 | Wroclaw | 1.02 | 123,894 | 5 | 1 | 1 | 121 | 30 | measured |
| 332 | Zadar | 1.53 | 71,549 | - | - | - | - | 20 | predicted (travel demand) |
| 333 | Modena | 0.85 | 51,698 | 5 | 1 | 1 | 3 | 20 | measured |
| 334 | Breda | 0.68 | 36,579 | 11 | - | 2 | 120 | 20 | measured |
| 335 | Fort Worth | 1.36 | - | 5 | - | - | - | 30 | measured |
| 336 | Split | 1.36 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 337 | Turku | 1.36 | - | 1 | - | - | - | 20 | measured |
| 338 | Antalya | 1.31 | 70,688 | - | - | - | - | 60 | predicted (travel demand) |
| 339 | Colmar | 1.28 | 45,517 | - | - | - | - | 20 | predicted (travel demand) |
| 340 | Hiroshima | 0.85 | 129,791 | 33 | 5 | 2 | - | 60 | measured |
| 341 | Bodrum | 1.26 | 33,918 | - | - | - | - | 20 | predicted (travel demand) |
| 342 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 343 | Evora | 0.78 | 15,345 | - | - | - | - | 20 | predicted (travel demand) |
| 344 | Rio de Janeiro | 1.19 | 279,431 | 6 | - | - | - | 100 | measured |
| 345 | Rouen | 1.02 | 72,334 | 12 | - | 1 | 6 | 20 | measured |
| 346 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 347 | Buenos Aires | 1.02 | 333,331 | 4 | 2 | - | - | 60 | measured |
| 348 | La Palma | 0.70 | - | - | - | - | - | 20 | predicted (travel demand) |
| 349 | Potsdam | 0.68 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 350 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 60 | predicted (travel demand) |
| 351 | Brighton | 0.85 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 352 | Canberra | 0.85 | - | 1 | 1 | - | - | 30 | measured |
| 353 | Thessaloniki | 0.85 | 180,145 | 4 | - | 1 | - | 30 | measured |
| 354 | Bamberg | 0.68 | 28,716 | 5 | 4 | 1 | 10 | 20 | measured |
| 355 | Kamakura | 0.51 | 33,492 | 6 | - | - | - | 20 | measured |
| 356 | Maui | 0.68 | - | 4 | - | - | 3 | 20 | measured |
| 357 | Rothenburg ob der Tauber | 0.51 | 39,879 | 4 | - | 1 | 8 | 10 | measured |
| 358 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 100 | published, never ranked (may be uncrawled) |
| 359 | Assisi | 0.34 | 30,278 | 6 | 1 | 2 | 6 | 10 | measured |
| 360 | Phoenix | 0.55 | - | - | - | - | - | 60 | predicted (travel demand) |
| 361 | Okinawa | 0.34 | 24,466 | 6 | - | - | 1 | 30 | measured |
| 362 | Christchurch | 0.34 | 104,874 | 6 | - | 1 | 466 | 30 | measured |
| 363 | Sofia | 0.34 | 138,710 | 4 | - | - | - | 60 | measured |
| 364 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 365 | Toledo | 0.24 | 3,149 | - | - | - | - | 20 | predicted (travel demand) |
| 366 | Busan | 0.34 | 94,737 | 2 | - | - | - | 60 | measured |
| 367 | Antwerp | 0.34 | 128,289 | 10 | 4 | 1 | - | 30 | measured |
| 368 | Bucharest | 0.34 | 136,836 | 4 | - | 1 | - | 60 | measured |
| 369 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 370 | George Town | 0.28 | 36,080 | - | - | - | - | 30 | predicted (travel demand) |
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

