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
| 1 | Prague | 69.15 | 303,350 | 30 | 21 | 4 | 31 | 60 | measured |
| 2 | Lisbon | 50.01 | 201,877 | 36 | 17 | 3 | 67 | 30 | measured |
| 3 | Amsterdam | 49.14 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 4 | Barcelona | 48.27 | 346,477 | 56 | 14 | 7 | 180 | 60 | measured |
| 5 | New York | 89.59 | 1,124,326 | 27 | 6 | 2 | - | 100 | measured |
| 6 | Rome | 41.32 | 358,876 | 31 | 10 | 2 | 32 | 60 | measured |
| 7 | Palermo | 40.88 | 124,310 | 21 | 9 | 1 | 37 | 30 | measured |
| 8 | Singapore | 53.06 | 967,821 | 34 | 7 | 3 | 165 | 100 | measured |
| 9 | Berlin | 46.97 | 412,181 | 62 | 23 | 5 | 195 | 60 | measured |
| 10 | Seville | 44.79 | 170,545 | 43 | 11 | 2 | - | 30 | measured |
| 11 | Dublin | 38.71 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 12 | Oahu | 64.37 | - | 21 | 7 | 3 | - | 30 | measured |
| 13 | Tokyo | 35.66 | 394,702 | 22 | 15 | 1 | 5 | 100 | measured |
| 14 | Munich | 38.71 | 224,067 | 52 | 24 | 7 | 78 | 60 | measured |
| 15 | Tenerife | 34.79 | - | 4 | 4 | - | - | 30 | measured |
| 16 | Porto | 25.22 | 120,415 | 27 | 15 | 2 | 40 | 30 | measured |
| 17 | Brussels | 31.31 | 176,863 | 35 | 4 | 2 | 436 | 60 | measured |
| 18 | Brisbane | 29.14 | 162,602 | 20 | 2 | 2 | 186 | 60 | measured |
| 19 | Malaga | 29.14 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 20 | Paris | 29.14 | 524,268 | 31 | 11 | 4 | 129 | 60 | measured |
| 21 | Cagliari | 23.48 | 51,351 | 14 | 1 | 2 | 14 | 20 | measured |
| 22 | Alicante | 21.31 | 77,454 | 21 | 4 | 2 | 44 | 30 | measured |
| 23 | The Hague | 20.01 | 236,723 | 31 | 3 | 5 | 167 | 30 | measured |
| 24 | Houston | 40.01 | - | 8 | - | - | - | 60 | measured |
| 25 | Birmingham | 37.53 | - | - | - | - | - | 60 | predicted (travel demand) |
| 26 | Vienna | 24.79 | 283,090 | 32 | 19 | 5 | 376 | 60 | measured |
| 27 | Bath | 36.10 | 144,950 | 5 | 2 | 1 | - | 20 | measured |
| 28 | San Francisco | 34.79 | 361,111 | 6 | 1 | 1 | - | 30 | measured |
| 29 | Cadiz | 22.61 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 30 | Madrid | 21.75 | 274,553 | 17 | 11 | 2 | - | 60 | measured |
| 31 | Milan | 17.40 | 212,705 | 30 | 14 | 3 | 25 | 60 | measured |
| 32 | Sintra | 16.96 | 46,889 | 5 | 3 | - | 6 | 30 | measured |
| 33 | Austin | 33.05 | 226,631 | 10 | 3 | 1 | - | 30 | measured |
| 34 | Florence | 16.09 | 184,099 | 27 | 9 | 1 | 27 | 30 | measured |
| 35 | Nijmegen | 16.09 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 36 | Portland | 20.01 | 217,222 | 32 | 1 | 3 | 303 | 30 | measured |
| 37 | New Orleans | 28.70 | 256,232 | 8 | 5 | 1 | - | 30 | measured |
| 38 | Athens | 27.83 | 235,429 | 12 | 7 | 2 | - | 30 | measured |
| 39 | London | 23.92 | 718,291 | 27 | 19 | 1 | - | 100 | measured |
| 40 | Edinburgh | 27.40 | 292,981 | 16 | 5 | 1 | - | 30 | measured |
| 41 | Valencia | 13.48 | 162,209 | 31 | 4 | 2 | 350 | 30 | measured |
| 42 | Los Angeles | 26.09 | 665,559 | 11 | 2 | - | - | 60 | measured |
| 43 | Utrecht | 13.05 | 67,963 | 30 | 7 | 2 | 339 | 30 | measured |
| 44 | Chicago | 26.09 | 485,769 | 6 | - | - | - | 60 | measured |
| 45 | Palma de Mallorca | 15.22 | 84,075 | 5 | 1 | 1 | 8 | 30 | measured |
| 46 | Dallas | 25.22 | - | 12 | 1 | 1 | - | 60 | measured |
| 47 | Jacksonville | 22.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 48 | Leeuwarden | 11.31 | - | 41 | - | 2 | 61 | 20 | measured |
| 49 | Hobart | 14.79 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 50 | Krakow | 14.35 | 140,824 | 38 | 8 | 3 | 198 | 30 | measured |
| 51 | Cyprus | 20.88 | - | 4 | - | - | - | 60 | measured |
| 52 | Asheville | 20.89 | - | - | - | - | - | 20 | predicted (travel demand) |
| 53 | Arnhem | 10.44 | 31,478 | 39 | 3 | 3 | 204 | 20 | measured |
| 54 | Monterey | 20.88 | - | 3 | 1 | - | - | 10 | measured |
| 55 | Ottawa | 13.92 | - | 21 | - | 3 | 122 | 60 | measured |
| 56 | Long Beach | 20.48 | - | - | - | - | - | 30 | predicted (travel demand) |
| 57 | Little Rock | 20.40 | - | - | - | - | - | 20 | predicted (travel demand) |
| 58 | Coimbra | 10.87 | 34,962 | 5 | - | - | 5 | 20 | measured |
| 59 | Haarlem | 10.00 | 33,960 | 21 | 1 | 2 | 277 | 20 | measured |
| 60 | Seattle | 19.14 | 398,724 | 16 | 1 | 2 | - | 30 | measured |
| 61 | Venice | 10.87 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 62 | Montreal | 19.57 | 315,322 | 13 | 1 | 2 | - | 60 | measured |
| 63 | Granada | 12.18 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 64 | Naples | 9.57 | 198,913 | 24 | 3 | 3 | 46 | 30 | measured |
| 65 | Pamplona | 11.31 | 128,065 | 14 | - | 1 | 9 | 20 | measured |
| 66 | Oakland | 18.81 | - | - | - | - | - | 30 | predicted (travel demand) |
| 67 | Liverpool | 18.27 | 248,189 | 2 | 2 | - | - | 30 | measured |
| 68 | Eindhoven | 9.13 | - | 21 | - | 4 | 195 | 20 | measured |
| 69 | Lexington | 18.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 70 | Reno | 18.19 | - | - | - | - | - | 30 | predicted (travel demand) |
| 71 | Des Moines | 18.11 | - | - | - | - | - | 20 | predicted (travel demand) |
| 72 | Fukuoka | 11.74 | 77,485 | 17 | 11 | 1 | - | 60 | measured |
| 73 | Daytona Beach | 17.66 | - | - | - | - | - | 20 | predicted (travel demand) |
| 74 | Boston | 16.53 | 385,902 | 12 | 2 | 2 | - | 30 | measured |
| 75 | Chattanooga | 16.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 76 | Reykjavik | 14.35 | 166,789 | 4 | 2 | 1 | - | 20 | measured |
| 77 | Madeira | 10.00 | - | 10 | 1 | 1 | - | 30 | measured |
| 78 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 79 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 80 | Dordrecht | 7.83 | - | 20 | 1 | 2 | 105 | 20 | measured |
| 81 | Melbourne | 10.44 | 267,898 | 16 | - | 2 | 403 | 100 | measured |
| 82 | Vilnius | 10.44 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 83 | Huntsville | 15.35 | - | - | - | - | - | 20 | predicted (travel demand) |
| 84 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 85 | West Palm Beach | 14.98 | - | - | - | - | - | 20 | predicted (travel demand) |
| 86 | Sardinia | 8.26 | - | 5 | 4 | - | 8 | 60 | measured |
| 87 | Saint Petersburg | 14.83 | - | - | - | - | - | 100 | predicted (travel demand) |
| 88 | St. Louis | 14.80 | - | - | - | - | - | 30 | predicted (travel demand) |
| 89 | Leiden | 7.39 | 33,227 | 20 | 6 | 1 | 129 | 20 | measured |
| 90 | Copenhagen | 13.92 | 218,621 | 49 | 41 | 6 | - | 30 | measured |
| 91 | Tampa | 14.10 | - | - | - | - | - | 30 | predicted (travel demand) |
| 92 | Kanazawa | 9.13 | 25,778 | 7 | 2 | 1 | 2 | 30 | measured |
| 93 | Maastricht | 6.96 | 47,763 | 19 | - | 2 | 135 | 20 | measured |
| 94 | Yakushima | 8.70 | - | 2 | - | - | 1 | 10 | measured |
| 95 | Leipzig | 9.13 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 96 | Warsaw | 9.13 | 197,929 | 39 | 20 | 4 | 1407 | 60 | measured |
| 97 | Cincinnati | 13.33 | - | - | - | - | - | 30 | predicted (travel demand) |
| 98 | Sydney | 13.05 | 305,304 | 7 | 1 | - | - | 100 | measured |
| 99 | Verona | 7.83 | 77,646 | 8 | 4 | 1 | 3 | 30 | measured |
| 100 | Budapest | 12.61 | 283,807 | 13 | 2 | 3 | - | 60 | measured |
| 101 | Strasbourg | 8.70 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 102 | Helmond | 6.52 | - | 20 | - | 2 | 54 | 20 | measured |
| 103 | Lansing | 13.02 | - | - | - | - | - | 20 | predicted (travel demand) |
| 104 | Detroit | 12.53 | - | - | - | - | - | 30 | predicted (travel demand) |
| 105 | Cork | 8.26 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 106 | Amersfoort | 6.09 | - | 18 | 1 | 2 | 181 | 20 | measured |
| 107 | Boise | 12.18 | - | 4 | - | 1 | - | 20 | measured |
| 108 | Spokane | 8.70 | - | 13 | - | 2 | 18 | 20 | measured |
| 109 | Philadelphia | 11.31 | 405,294 | 4 | 1 | - | - | 60 | measured |
| 110 | Ibiza | 7.39 | - | 1 | - | - | 4 | 20 | measured |
| 111 | Denver | 11.66 | - | - | - | - | - | 30 | predicted (travel demand) |
| 112 | Washington DC | 10.44 | 606,731 | 16 | 1 | 3 | - | 30 | measured |
| 113 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 60 | predicted (travel demand) |
| 114 | San Jose | 11.39 | - | - | - | - | - | 60 | predicted (travel demand) |
| 115 | Bologna | 6.09 | 146,161 | 12 | 7 | 1 | 9 | 30 | measured |
| 116 | Sacramento | 11.32 | - | - | - | - | - | 30 | predicted (travel demand) |
| 117 | Sorrento | 5.65 | 40,049 | 7 | - | 1 | 20 | 10 | measured |
| 118 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 60 | predicted (travel demand) |
| 119 | Girona | 6.52 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 120 | Luxembourg City | 7.39 | 64,851 | 10 | 5 | 2 | 18 | 20 | measured |
| 121 | Dubai | 11.02 | 334,167 | - | - | - | - | 60 | predicted (travel demand) |
| 122 | Parma | 6.09 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 123 | Osaka | 6.96 | 163,112 | 6 | 1 | - | - | 60 | measured |
| 124 | Milwaukee | 10.63 | - | - | - | - | - | 30 | predicted (travel demand) |
| 125 | Jersey City | 10.08 | - | - | - | - | - | 30 | predicted (travel demand) |
| 126 | Enschede | 5.22 | - | 15 | 1 | 2 | 82 | 20 | measured |
| 127 | Frankfurt | 6.96 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 128 | Las Vegas | 10.44 | - | 11 | - | 2 | - | 30 | measured |
| 129 | Quebec City | 6.96 | 124,358 | 6 | - | 1 | 494 | 30 | measured |
| 130 | Zwolle | 5.22 | - | 20 | - | 4 | 58 | 20 | measured |
| 131 | Salt Lake City | 10.31 | - | - | - | - | - | 20 | predicted (travel demand) |
| 132 | Atlanta | 10.29 | - | - | - | - | - | 30 | predicted (travel demand) |
| 133 | Anchorage | 10.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 134 | Cordoba | 6.52 | 74,675 | 16 | 2 | 2 | 3 | 30 | measured |
| 135 | Kyoto | 6.52 | 142,353 | 18 | 12 | 2 | - | 60 | measured |
| 136 | Raleigh | 10.07 | - | - | - | - | - | 30 | predicted (travel demand) |
| 137 | Bali | 9.95 | - | - | - | - | - | 60 | predicted (travel demand) |
| 138 | Glasgow | 9.57 | 253,705 | 5 | 3 | - | - | 30 | measured |
| 139 | Cleveland | 9.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 140 | Stockholm | 7.83 | 188,184 | 8 | 4 | - | - | 30 | measured |
| 141 | El Paso | 9.70 | - | - | - | - | - | 30 | predicted (travel demand) |
| 142 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 143 | Nice | 9.57 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 144 | Caserta | 4.78 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 145 | Miami | 9.48 | 278,558 | - | - | - | - | 30 | predicted (travel demand) |
| 146 | Edmonton | 9.38 | - | - | - | - | - | 60 | predicted (travel demand) |
| 147 | Winnipeg | 9.21 | - | - | - | - | - | 30 | predicted (travel demand) |
| 148 | Nuremberg | 6.09 | 161,614 | 14 | 2 | 1 | 39 | 30 | measured |
| 149 | Nashville | 8.93 | - | - | - | - | - | 30 | predicted (travel demand) |
| 150 | Oslo | 7.83 | 181,113 | 4 | 1 | - | - | 30 | measured |
| 151 | Tampere | 8.78 | - | - | - | - | - | 30 | predicted (travel demand) |
| 152 | Delft | 4.35 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 153 | Hawaii | 8.70 | - | 6 | - | 1 | - | 60 | measured |
| 154 | Zurich | 8.26 | 140,788 | 6 | 1 | - | - | 30 | measured |
| 155 | Ann Arbor | 8.55 | - | - | - | - | - | 20 | predicted (travel demand) |
| 156 | Geneva | 5.65 | 162,269 | 21 | 5 | 4 | 131 | 20 | measured |
| 157 | Seoul | 7.83 | 206,265 | 8 | 5 | 1 | - | 100 | measured |
| 158 | Adelaide | 8.14 | 139,166 | - | - | - | - | 60 | predicted (travel demand) |
| 159 | Charleston | 7.83 | 155,987 | 3 | 1 | - | - | 20 | measured |
| 160 | Albuquerque | 7.83 | - | - | - | - | - | 30 | predicted (travel demand) |
| 161 | Hong Kong | 5.22 | 689,212 | 10 | 4 | 1 | 505 | 100 | measured |
| 162 | Apeldoorn | 3.91 | - | 10 | - | 2 | 80 | 20 | measured |
| 163 | Deventer | 3.91 | - | 12 | - | 1 | 213 | 20 | measured |
| 164 | Groningen | 3.91 | 31,401 | 21 | 1 | 2 | 76 | 20 | measured |
| 165 | Tilburg | 3.91 | - | 20 | - | 3 | 87 | 20 | measured |
| 166 | Venlo | 3.91 | - | 7 | - | 1 | 144 | 20 | measured |
| 167 | Perth | 7.39 | 180,478 | 6 | 3 | 1 | - | 60 | measured |
| 168 | Guimaraes | 3.91 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 169 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 20 | predicted (travel demand) |
| 170 | Bergen | 7.30 | 82,940 | - | - | - | - | 30 | predicted (travel demand) |
| 171 | Helsinki | 5.65 | 148,908 | 12 | 2 | 1 | 13 | 30 | measured |
| 172 | Cambridge | 6.96 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 173 | Savannah | 6.96 | 128,162 | 3 | 1 | - | - | 20 | measured |
| 174 | Segovia | 4.35 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 175 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 20 | predicted (travel demand) |
| 176 | Siena | 4.62 | 57,436 | - | - | - | - | 20 | predicted (travel demand) |
| 177 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 20 | predicted (travel demand) |
| 178 | Istanbul | 5.87 | 333,027 | 14 | 4 | 1 | - | 100 | measured |
| 179 | Bari | 3.91 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 180 | Zagreb | 6.42 | 122,890 | - | - | - | - | 30 | predicted (travel demand) |
| 181 | Crete | 6.52 | - | 4 | 3 | - | - | 30 | measured |
| 182 | Sapporo | 4.35 | 88,633 | 6 | - | - | - | 60 | measured |
| 183 | Bogota | 6.39 | 1,623 | - | - | - | - | 100 | predicted (travel demand) |
| 184 | Shanghai | 6.38 | 277,140 | - | - | - | - | 100 | predicted (travel demand) |
| 185 | Funchal | 3.77 | 174,351 | - | - | - | - | 20 | predicted (travel demand) |
| 186 | Vancouver | 6.09 | 351,552 | 7 | - | - | - | 30 | measured |
| 187 | Kauai | 6.09 | - | 6 | 1 | - | - | 20 | measured |
| 188 | Como | 3.04 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 189 | Den Bosch | 3.04 | 39,682 | 12 | 2 | 1 | 118 | 20 | measured |
| 190 | Lucca | 3.04 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 191 | Lyon | 3.91 | 136,951 | 13 | 4 | 1 | 156 | 30 | measured |
| 192 | Tallinn | 3.91 | 124,888 | 9 | 3 | 2 | 42 | 30 | measured |
| 193 | Malta | 5.79 | - | - | - | - | - | 30 | predicted (travel demand) |
| 194 | Aarhus | 5.65 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 195 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 196 | Avignon | 5.54 | 64,047 | - | - | - | - | 20 | predicted (travel demand) |
| 197 | Dubrovnik | 5.22 | 119,586 | 4 | 1 | - | 2 | 10 | measured |
| 198 | Galway | 3.65 | 88,162 | - | - | - | - | 20 | predicted (travel demand) |
| 199 | Phuket | 5.46 | 5,487 | - | - | - | - | 30 | predicted (travel demand) |
| 200 | Hallstatt | 4.78 | 47,271 | 5 | 1 | - | - | 10 | measured |
| 201 | Rovaniemi | 5.38 | - | - | - | - | - | 20 | predicted (travel demand) |
| 202 | Nagoya | 3.48 | 83,437 | 6 | 1 | - | 1 | 60 | measured |
| 203 | Salamanca | 3.48 | 47,897 | 4 | - | 1 | 1 | 20 | measured |
| 204 | Lagos | 3.43 | 34,452 | - | - | - | - | 100 | predicted (travel demand) |
| 205 | Bordeaux | 3.48 | 156,201 | 10 | - | 2 | 211 | 30 | measured |
| 206 | Gdansk | 3.48 | 4,908 | 12 | 4 | 1 | 307 | 30 | measured |
| 207 | Graz | 3.48 | 65,717 | 13 | 7 | 2 | 87 | 30 | measured |
| 208 | Minneapolis | 5.22 | - | 4 | - | - | - | 30 | measured |
| 209 | Roosendaal | 2.61 | - | 8 | - | 1 | 116 | 20 | measured |
| 210 | Taipei | 5.22 | 143,193 | 4 | 1 | - | - | 60 | measured |
| 211 | Santa Fe | 5.17 | - | - | - | - | - | 20 | predicted (travel demand) |
| 212 | Lund | 5.14 | - | - | - | - | - | 20 | predicted (travel demand) |
| 213 | Kobe | 3.40 | 54,798 | - | - | - | - | 60 | predicted (travel demand) |
| 214 | Heraklion | 4.96 | 66,359 | - | - | - | - | 20 | predicted (travel demand) |
| 215 | Marseille | 4.96 | 182,033 | - | - | - | - | 30 | predicted (travel demand) |
| 216 | Bristol | 4.78 | 163,983 | 6 | 2 | - | - | 30 | measured |
| 217 | Manchester | 4.78 | 316,438 | 5 | - | - | - | 30 | measured |
| 218 | Basel | 4.59 | 105,838 | - | - | - | - | 20 | predicted (travel demand) |
| 219 | Brno | 3.04 | 63,714 | 8 | 5 | 2 | 34 | 30 | measured |
| 220 | Ghent | 4.35 | 82,757 | 8 | 1 | 1 | - | 30 | measured |
| 221 | Indianapolis | 4.35 | - | 1 | - | - | - | 30 | measured |
| 222 | Tasmania | 4.41 | - | - | - | - | - | 30 | predicted (travel demand) |
| 223 | Alkmaar | 2.17 | - | 14 | - | 2 | 79 | 20 | measured |
| 224 | Bergamo | 2.17 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 225 | Hoorn | 2.17 | - | 12 | - | 2 | 52 | 20 | measured |
| 226 | Trieste | 2.17 | 117,233 | 36 | 1 | 3 | 43 | 20 | measured |
| 227 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 20 | predicted (travel demand) |
| 228 | Sofia | 2.81 | 138,710 | 4 | - | - | - | 60 | published, never ranked (may be uncrawled) |
| 229 | San Sebastian | 2.80 | 367 | - | - | - | - | 20 | predicted (travel demand) |
| 230 | Hamburg | 3.91 | 191,221 | 6 | 1 | 1 | - | 60 | measured |
| 231 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 30 | predicted (travel demand) |
| 232 | Freiburg | 3.91 | 92,752 | 7 | 2 | 1 | - | 20 | measured |
| 233 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 234 | Oxford | 3.91 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 235 | Genoa | 2.17 | 145,206 | 13 | 2 | 1 | 10 | 30 | measured |
| 236 | Setubal | 2.17 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 237 | Azores | 2.62 | - | - | - | - | - | 20 | predicted (travel demand) |
| 238 | Cologne | 3.91 | 191,812 | 5 | - | 1 | - | 60 | measured |
| 239 | Heidelberg | 3.48 | 75,837 | 6 | 1 | 1 | - | 20 | measured |
| 240 | Pittsburgh | 3.80 | - | 4 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 241 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 242 | Niagara Falls | 3.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 243 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 100 | predicted (travel demand) |
| 244 | Beijing | 3.70 | 269,737 | 7 | 1 | - | - | 100 | measured |
| 245 | Wellington | 3.60 | 132,267 | - | - | - | - | 20 | predicted (travel demand) |
| 246 | Modena | 2.17 | 51,698 | 5 | 1 | 1 | 3 | 20 | measured |
| 247 | Ljubljana | 3.48 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 248 | Kansas City | 3.48 | - | 4 | - | 1 | - | 30 | measured |
| 249 | Montpellier | 3.47 | 64,238 | - | - | - | - | 30 | predicted (travel demand) |
| 250 | Stuttgart | 2.61 | 112,789 | 6 | 1 | - | - | 30 | measured |
| 251 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 252 | Cape Town | 3.29 | 199,169 | - | - | - | - | 60 | predicted (travel demand) |
| 253 | Rhodes | 3.42 | 127,205 | - | - | - | - | 20 | predicted (travel demand) |
| 254 | Menorca | 2.17 | - | 6 | - | - | 2 | 20 | measured |
| 255 | San Antonio | 3.32 | - | 4 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 256 | Chania | 3.30 | 47,379 | - | - | - | - | 20 | predicted (travel demand) |
| 257 | Zaragoza | 2.17 | 87,580 | 7 | - | 1 | - | 30 | measured |
| 258 | Padua | 1.74 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 259 | Perugia | 1.74 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 260 | Dresden | 2.17 | 113,624 | 13 | 9 | 1 | - | 30 | measured |
| 261 | Salzburg | 2.17 | 107,243 | 12 | 3 | 2 | 34 | 20 | measured |
| 262 | Santiago | 3.25 | 111,647 | - | - | - | - | 100 | predicted (travel demand) |
| 263 | Toulouse | 2.17 | 112,721 | 10 | - | 1 | 34 | 30 | measured |
| 264 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 30 | predicted (travel demand) |
| 265 | Cardiff | 3.04 | - | 4 | - | 1 | - | 30 | measured |
| 266 | Lucerne | 3.10 | 66,356 | - | - | - | - | 20 | predicted (travel demand) |
| 267 | Toronto | 3.04 | 411,011 | 6 | - | - | - | 60 | measured |
| 268 | Malmo | 3.07 | 103,940 | - | - | - | - | 30 | predicted (travel demand) |
| 269 | Lille | 3.06 | 73,435 | - | - | - | - | 20 | predicted (travel demand) |
| 270 | Belgrade | 3.04 | 178,116 | 5 | 5 | - | - | 60 | measured |
| 271 | Lausanne | 3.04 | 68,242 | 8 | 1 | 1 | - | 20 | measured |
| 272 | Corsica | 3.00 | - | - | - | - | - | 30 | predicted (travel demand) |
| 273 | Mechelen | 2.93 | 20,707 | - | - | - | - | 20 | predicted (travel demand) |
| 274 | Matera | 1.74 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 275 | Poznan | 1.89 | 65,666 | 10 | - | 1 | 397 | 30 | published, never ranked (may be uncrawled) |
| 276 | Mexico City | 2.61 | 566,583 | 9 | 2 | - | - | 100 | measured |
| 277 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 278 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 279 | Corfu | 2.71 | 139,334 | - | - | - | - | 20 | predicted (travel demand) |
| 280 | Pisa | 1.74 | 52,174 | 4 | - | - | - | 20 | measured |
| 281 | Syracuse | 1.75 | 102,833 | - | - | - | - | 20 | predicted (travel demand) |
| 282 | Belfast | 2.61 | 224,315 | 5 | 1 | 1 | - | 30 | measured |
| 283 | Fort Worth | 2.61 | - | 5 | - | - | - | 30 | measured |
| 284 | Hilo | 2.61 | - | 6 | - | 1 | - | 10 | measured |
| 285 | Tulsa | 2.61 | - | 1 | - | - | - | 30 | measured |
| 286 | Assen | 1.30 | - | 10 | - | 2 | 66 | 20 | measured |
| 287 | Rotterdam | 1.30 | 104,938 | 16 | - | 2 | 83 | 30 | measured |
| 288 | Trento | 1.30 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 289 | Cartagena | 2.58 | 65,066 | - | - | - | - | 30 | predicted (travel demand) |
| 290 | Gran Canaria | 1.67 | - | - | - | - | - | 30 | predicted (travel demand) |
| 291 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 20 | predicted (travel demand) |
| 292 | Bern | 2.51 | 90,627 | - | - | - | - | 20 | predicted (travel demand) |
| 293 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 294 | Faro | 1.62 | 55,645 | - | - | - | - | 20 | predicted (travel demand) |
| 295 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 296 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 297 | Cusco | 2.35 | 87,732 | - | - | - | - | 30 | predicted (travel demand) |
| 298 | Limerick | 1.57 | 90,379 | - | - | - | - | 20 | predicted (travel demand) |
| 299 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 20 | predicted (travel demand) |
| 300 | Catania | 1.30 | 58,252 | 4 | 3 | 1 | 5 | 30 | measured |
| 301 | Ronda | 1.30 | 51,510 | 6 | 1 | - | 9 | 10 | measured |
| 302 | Bruges | 2.17 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 303 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 304 | Ischia | 1.32 | - | - | - | - | 2 | 20 | predicted (travel demand) |
| 305 | Bangkok | 1.96 | 222,206 | 5 | 1 | 1 | - | 100 | measured |
| 306 | Izmir | 1.88 | 69,826 | - | - | - | - | 60 | predicted (travel demand) |
| 307 | Bilbao | 1.30 | 133,133 | 4 | - | 1 | - | 30 | measured |
| 308 | Hiroshima | 1.30 | 129,791 | 33 | 5 | 2 | - | 60 | measured |
| 309 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 310 | Sao Paulo | 1.74 | 911 | 1 | - | - | - | 100 | measured |
| 311 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 312 | Breda | 0.87 | 36,579 | 11 | 1 | 2 | 120 | 20 | measured |
| 313 | Hilversum | 0.87 | - | 6 | 1 | 1 | 122 | 20 | measured |
| 314 | Leuven | 1.74 | 40,645 | 4 | - | - | - | 20 | measured |
| 315 | San Diego | 1.74 | 214,939 | 6 | 1 | 1 | - | 60 | measured |
| 316 | Dijon | 1.72 | 43,526 | - | - | - | - | 20 | predicted (travel demand) |
| 317 | Trier | 1.56 | 69,369 | - | - | - | - | 20 | predicted (travel demand) |
| 318 | Annecy | 1.69 | 56,859 | - | - | - | - | 20 | predicted (travel demand) |
| 319 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 320 | Canterbury | 1.59 | 53,301 | - | - | - | - | 20 | predicted (travel demand) |
| 321 | Mostar | 1.58 | 63,907 | - | - | - | - | 20 | predicted (travel demand) |
| 322 | Braga | 0.87 | 34,522 | 4 | 2 | - | 8 | 20 | measured |
| 323 | Zadar | 1.53 | 71,549 | - | - | - | - | 20 | predicted (travel demand) |
| 324 | Gothenburg | 1.49 | 119,991 | 5 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 325 | Rouen | 1.30 | 72,334 | 12 | - | 1 | 6 | 20 | measured |
| 326 | Tarragona | 0.87 | 32,396 | 4 | 2 | - | - | 20 | measured |
| 327 | Thessaloniki | 1.42 | 180,145 | 4 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 328 | Assisi | 0.87 | 30,278 | 6 | 1 | 2 | 6 | 10 | measured |
| 329 | Okinawa | 0.87 | 24,466 | 6 | - | - | 1 | 30 | measured |
| 330 | Antalya | 1.31 | 70,688 | - | - | - | - | 60 | predicted (travel demand) |
| 331 | Antwerp | 1.30 | 128,289 | 10 | 4 | 1 | - | 30 | measured |
| 332 | Auckland | 0.87 | 152,056 | 5 | 2 | - | 977 | 60 | measured |
| 333 | Bratislava | 0.87 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 334 | Cesky Krumlov | 0.87 | 28,582 | 6 | 3 | - | 11 | 10 | measured |
| 335 | Christchurch | 0.87 | 104,874 | 6 | - | 1 | 466 | 30 | measured |
| 336 | Potsdam | 0.87 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 337 | Split | 1.30 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 338 | Turku | 1.30 | - | 1 | - | - | - | 20 | measured |
| 339 | Wroclaw | 0.87 | 123,894 | 5 | 1 | 1 | 121 | 30 | measured |
| 340 | Colmar | 1.28 | 45,517 | - | - | - | - | 20 | predicted (travel demand) |
| 341 | Bodrum | 1.26 | 33,918 | - | - | - | - | 20 | predicted (travel demand) |
| 342 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 343 | Evora | 0.78 | 15,345 | - | - | - | - | 20 | predicted (travel demand) |
| 344 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 345 | La Palma | 0.70 | - | - | - | - | - | 20 | predicted (travel demand) |
| 346 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 60 | predicted (travel demand) |
| 347 | Nantes | 0.96 | 67,689 | 1 | 1 | - | - | 30 | published, never ranked (may be uncrawled) |
| 348 | Regensburg | 0.87 | 51,930 | 5 | 1 | 1 | 4 | 20 | measured |
| 349 | Rothenburg ob der Tauber | 0.77 | 39,879 | 4 | - | 1 | 8 | 10 | published, never ranked (may be uncrawled) |
| 350 | Baltimore | 0.87 | - | 4 | - | - | - | 30 | measured |
| 351 | Fort Lauderdale | 0.87 | - | 4 | - | - | - | 20 | measured |
| 352 | Brighton | 0.87 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 353 | Maui | 0.87 | - | 4 | - | - | - | 20 | measured |
| 354 | Rio de Janeiro | 0.87 | 279,431 | 6 | - | - | - | 100 | measured |
| 355 | York | 0.87 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 356 | Heerlen | 0.43 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 357 | Turin | 0.43 | 147,456 | 11 | 7 | 2 | 30 | 30 | measured |
| 358 | Ferrara | 0.43 | 27,490 | 5 | 3 | 1 | 7 | 20 | measured |
| 359 | Kamakura | 0.44 | 33,492 | 6 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 360 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 100 | published, never ranked (may be uncrawled) |
| 361 | Phoenix | 0.55 | - | - | - | - | - | 60 | predicted (travel demand) |
| 362 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 363 | Busan | 0.43 | 94,737 | 2 | - | - | - | 60 | measured |
| 364 | Riga | 0.43 | 108,918 | 5 | 2 | - | - | 30 | measured |
| 365 | Bucharest | 0.43 | 136,836 | 4 | - | 1 | - | 60 | measured |
| 366 | Canberra | 0.43 | - | 1 | 1 | - | - | 30 | measured |
| 367 | Toledo | 0.24 | 3,149 | - | - | - | - | 20 | predicted (travel demand) |
| 368 | Bamberg | 0.24 | 28,716 | 5 | 4 | 1 | 10 | 20 | published, never ranked (may be uncrawled) |
| 369 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 370 | George Town | 0.28 | 36,080 | - | - | - | - | 30 | predicted (travel demand) |
| 371 | Allentown | 0.24 | - | - | - | - | - | 20 | predicted (travel demand) |
| 372 | Buenos Aires | 0.22 | 333,331 | 4 | 2 | - | - | 60 | measured |
| 373 | Oss | 0.11 | - | 6 | - | - | 48 | 20 | published, never ranked (may be uncrawled) |
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

