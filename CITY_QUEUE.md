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
| 1 | Lisbon | 49.91 | 201,877 | 36 | 17 | 3 | 67 | 30 | measured |
| 2 | Barcelona | 48.54 | 346,477 | 56 | 14 | 7 | 180 | 60 | measured |
| 3 | Amsterdam | 45.44 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 4 | New York | 81.24 | 1,124,326 | 27 | 6 | 2 | - | 100 | measured |
| 5 | Singapore | 55.42 | 967,821 | 34 | 7 | 3 | 165 | 100 | measured |
| 6 | Rome | 39.93 | 358,876 | 31 | 10 | 2 | 32 | 60 | measured |
| 7 | Palermo | 37.18 | 124,310 | 21 | 9 | 1 | 37 | 30 | measured |
| 8 | Prague | 49.57 | 303,350 | 30 | 21 | 4 | 31 | 60 | measured |
| 9 | Berlin | 48.54 | 412,181 | 62 | 23 | 5 | 195 | 60 | measured |
| 10 | Oahu | 70.91 | - | 21 | 7 | 3 | - | 30 | measured |
| 11 | Seville | 45.10 | 170,545 | 43 | 11 | 2 | - | 30 | measured |
| 12 | Tokyo | 35.11 | 394,702 | 22 | 15 | 1 | 5 | 100 | measured |
| 13 | Dublin | 35.46 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 14 | Tenerife | 39.93 | - | 4 | 4 | - | - | 30 | measured |
| 15 | Porto | 28.23 | 120,415 | 27 | 15 | 2 | 40 | 30 | measured |
| 16 | Munich | 36.49 | 224,067 | 50 | 22 | 7 | 79 | 60 | measured |
| 17 | Brussels | 34.08 | 176,863 | 35 | 4 | 2 | 436 | 60 | measured |
| 18 | Brisbane | 33.39 | 162,602 | 20 | 2 | 2 | 186 | 60 | measured |
| 19 | Malaga | 32.36 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 20 | Paris | 29.60 | 524,268 | 31 | 11 | 4 | 129 | 60 | measured |
| 21 | Alicante | 21.69 | 77,454 | 21 | 4 | 2 | 44 | 30 | measured |
| 22 | Cagliari | 21.34 | 51,351 | 14 | 1 | 2 | 14 | 20 | measured |
| 23 | Vienna | 25.82 | 283,090 | 32 | 19 | 5 | 376 | 60 | measured |
| 24 | Birmingham | 37.53 | - | - | - | - | - | 60 | predicted (travel demand) |
| 25 | Madrid | 22.72 | 274,553 | 17 | 11 | 2 | - | 60 | measured |
| 26 | Houston | 35.11 | - | 8 | - | - | - | 60 | measured |
| 27 | Bath | 34.42 | 144,950 | 5 | 2 | 1 | - | 20 | measured |
| 28 | The Hague | 17.21 | 236,723 | 31 | 3 | 5 | 167 | 30 | measured |
| 29 | Cadiz | 22.03 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 30 | Sintra | 16.87 | 46,889 | 5 | 3 | - | 6 | 30 | measured |
| 31 | Chicago | 33.05 | 485,769 | 6 | - | - | - | 60 | measured |
| 32 | Florence | 16.18 | 184,099 | 27 | 9 | 1 | 27 | 30 | measured |
| 33 | Milan | 15.84 | 212,705 | 30 | 14 | 3 | 25 | 60 | measured |
| 34 | Austin | 31.67 | 226,631 | 9 | 3 | 1 | - | 30 | measured |
| 35 | Los Angeles | 30.29 | 665,559 | 10 | 2 | - | - | 60 | measured |
| 36 | Portland | 19.97 | 217,222 | 24 | 1 | 2 | 306 | 30 | measured |
| 37 | London | 24.44 | 718,291 | 23 | 16 | 1 | - | 100 | measured |
| 38 | Nijmegen | 14.11 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 39 | San Francisco | 27.54 | 361,111 | 6 | 1 | 1 | - | 30 | measured |
| 40 | Edinburgh | 27.20 | 292,981 | 16 | 5 | 1 | - | 30 | measured |
| 41 | Athens | 26.85 | 235,429 | 12 | 7 | 2 | - | 30 | measured |
| 42 | Dallas | 26.85 | - | 12 | 1 | 1 | - | 60 | measured |
| 43 | Palma de Mallorca | 15.49 | 84,075 | 5 | 1 | 1 | 8 | 30 | measured |
| 44 | New Orleans | 25.47 | 256,232 | 8 | 5 | 1 | - | 30 | measured |
| 45 | Valencia | 12.05 | 162,209 | 31 | 4 | 2 | 350 | 30 | measured |
| 46 | Krakow | 15.49 | 140,824 | 38 | 8 | 3 | 198 | 30 | measured |
| 47 | Jacksonville | 22.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 48 | Utrecht | 11.36 | 67,963 | 30 | 7 | 2 | 339 | 30 | measured |
| 49 | Asheville | 20.89 | - | - | - | - | - | 20 | predicted (travel demand) |
| 50 | Boston | 19.97 | 385,902 | 12 | 2 | 2 | - | 30 | measured |
| 51 | Arnhem | 10.33 | 31,478 | 39 | 3 | 3 | 204 | 20 | measured |
| 52 | Long Beach | 20.48 | - | - | - | - | - | 30 | predicted (travel demand) |
| 53 | Little Rock | 20.40 | - | - | - | - | - | 20 | predicted (travel demand) |
| 54 | Venice | 11.02 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 55 | Monterey | 19.97 | - | 3 | 1 | - | - | 10 | measured |
| 56 | Pamplona | 11.70 | 128,065 | 14 | - | 1 | 9 | 20 | measured |
| 57 | Coimbra | 10.67 | 34,962 | 5 | - | - | 5 | 20 | measured |
| 58 | Hobart | 12.74 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 59 | Oakland | 18.81 | - | - | - | - | - | 30 | predicted (travel demand) |
| 60 | Seattle | 17.90 | 398,724 | 16 | 1 | 2 | - | 30 | measured |
| 61 | Liverpool | 18.59 | 248,189 | 2 | 2 | - | - | 30 | measured |
| 62 | Madeira | 11.02 | - | 10 | 1 | 1 | - | 30 | measured |
| 63 | Lexington | 18.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 64 | Reno | 18.19 | - | - | - | - | - | 30 | predicted (travel demand) |
| 65 | Des Moines | 18.11 | - | - | - | - | - | 20 | predicted (travel demand) |
| 66 | Ottawa | 12.05 | - | 21 | - | 3 | 122 | 60 | measured |
| 67 | Fukuoka | 11.70 | 77,485 | 16 | 10 | 1 | - | 60 | measured |
| 68 | Sardinia | 9.98 | - | 5 | 4 | - | 8 | 60 | measured |
| 69 | Haarlem | 8.95 | 33,960 | 21 | 1 | 2 | 277 | 20 | measured |
| 70 | Leeuwarden | 8.95 | - | 41 | - | 2 | 61 | 20 | measured |
| 71 | Daytona Beach | 17.66 | - | - | - | - | - | 20 | predicted (travel demand) |
| 72 | Naples | 8.61 | 198,913 | 24 | 3 | 3 | 46 | 30 | measured |
| 73 | Cyprus | 16.87 | - | 4 | - | - | - | 60 | measured |
| 74 | Reykjavik | 14.80 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 75 | Chattanooga | 16.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 76 | Vilnius | 11.02 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 77 | Montreal | 16.52 | 315,322 | 13 | 1 | 2 | - | 60 | measured |
| 78 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 79 | Warsaw | 10.67 | 197,929 | 39 | 20 | 4 | 1407 | 60 | measured |
| 80 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 81 | Granada | 9.98 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 82 | Huntsville | 15.35 | - | - | - | - | - | 20 | predicted (travel demand) |
| 83 | Las Vegas | 15.15 | - | 11 | - | 2 | - | 30 | measured |
| 84 | Leiden | 7.57 | 33,227 | 20 | 6 | 1 | 129 | 20 | measured |
| 85 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 86 | West Palm Beach | 14.98 | - | - | - | - | - | 20 | predicted (travel demand) |
| 87 | Saint Petersburg | 14.83 | - | - | - | - | - | 100 | predicted (travel demand) |
| 88 | St. Louis | 14.80 | - | - | - | - | - | 30 | predicted (travel demand) |
| 89 | Eindhoven | 7.23 | - | 21 | - | 4 | 195 | 20 | measured |
| 90 | Maastricht | 7.23 | 47,763 | 19 | - | 2 | 135 | 20 | measured |
| 91 | Melbourne | 9.64 | 267,898 | 16 | - | 2 | 403 | 100 | measured |
| 92 | Verona | 8.61 | 77,646 | 8 | 4 | 1 | 3 | 30 | measured |
| 93 | Tampa | 14.10 | - | - | - | - | - | 30 | predicted (travel demand) |
| 94 | Cork | 9.29 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 95 | Boise | 13.77 | - | 4 | - | 1 | - | 20 | measured |
| 96 | Ibiza | 8.61 | - | 1 | - | - | 4 | 20 | measured |
| 97 | Cincinnati | 13.33 | - | - | - | - | - | 30 | predicted (travel demand) |
| 98 | Lansing | 13.02 | - | - | - | - | - | 20 | predicted (travel demand) |
| 99 | Leipzig | 8.61 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 100 | Osaka | 8.26 | 163,112 | 6 | 1 | - | - | 60 | measured |
| 101 | Kanazawa | 8.26 | 25,778 | 7 | 2 | 1 | 2 | 30 | measured |
| 102 | Detroit | 12.53 | - | - | - | - | - | 30 | predicted (travel demand) |
| 103 | Dordrecht | 6.20 | - | 20 | 1 | 2 | 105 | 20 | measured |
| 104 | Spokane | 8.95 | - | 13 | - | 2 | 18 | 20 | measured |
| 105 | Sydney | 12.05 | 305,304 | 7 | 1 | - | - | 100 | measured |
| 106 | Budapest | 11.70 | 283,807 | 13 | 2 | 3 | - | 60 | measured |
| 107 | Copenhagen | 11.70 | 218,621 | 49 | 41 | 6 | - | 30 | measured |
| 108 | Strasbourg | 7.92 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 109 | Amersfoort | 5.85 | - | 18 | 1 | 2 | 181 | 20 | measured |
| 110 | Denver | 11.66 | - | - | - | - | - | 30 | predicted (travel demand) |
| 111 | Sao Paulo | 11.02 | 911 | 1 | - | - | - | 100 | measured |
| 112 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 60 | predicted (travel demand) |
| 113 | San Jose | 11.39 | - | - | - | - | - | 60 | predicted (travel demand) |
| 114 | Sacramento | 11.32 | - | - | - | - | - | 30 | predicted (travel demand) |
| 115 | Kyoto | 7.23 | 142,353 | 18 | 12 | 2 | - | 60 | measured |
| 116 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 60 | predicted (travel demand) |
| 117 | Girona | 6.54 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 118 | Dubai | 11.02 | 334,167 | - | - | - | - | 60 | predicted (travel demand) |
| 119 | Sorrento | 5.51 | 40,049 | 7 | - | 1 | 20 | 10 | measured |
| 120 | Yakushima | 6.88 | - | 2 | - | - | 1 | 10 | measured |
| 121 | Glasgow | 10.33 | 253,705 | 5 | 3 | - | - | 30 | measured |
| 122 | Milwaukee | 10.63 | - | - | - | - | - | 30 | predicted (travel demand) |
| 123 | Washington DC | 9.64 | 606,731 | 15 | 1 | 3 | - | 30 | measured |
| 124 | Jersey City | 10.08 | - | - | - | - | - | 30 | predicted (travel demand) |
| 125 | Helmond | 5.16 | - | 20 | - | 2 | 54 | 20 | measured |
| 126 | Salt Lake City | 10.31 | - | - | - | - | - | 20 | predicted (travel demand) |
| 127 | Atlanta | 10.29 | - | - | - | - | - | 30 | predicted (travel demand) |
| 128 | Anchorage | 10.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 129 | Oslo | 8.95 | 181,113 | 4 | 1 | - | - | 30 | measured |
| 130 | Raleigh | 10.07 | - | - | - | - | - | 30 | predicted (travel demand) |
| 131 | Philadelphia | 9.64 | 405,294 | 4 | 1 | - | - | 60 | measured |
| 132 | Bali | 9.95 | - | - | - | - | - | 60 | predicted (travel demand) |
| 133 | Geneva | 6.54 | 162,269 | 21 | 5 | 4 | 131 | 20 | measured |
| 134 | Luxembourg City | 6.54 | 64,851 | 10 | 5 | 2 | 18 | 20 | measured |
| 135 | Cleveland | 9.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 136 | El Paso | 9.70 | - | - | - | - | - | 30 | predicted (travel demand) |
| 137 | Caserta | 4.82 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 138 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 139 | Miami | 9.48 | 278,558 | - | - | - | - | 30 | predicted (travel demand) |
| 140 | Edmonton | 9.38 | - | - | - | - | - | 60 | predicted (travel demand) |
| 141 | Frankfurt | 6.20 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 142 | Seoul | 8.61 | 206,265 | 8 | 5 | 1 | - | 100 | measured |
| 143 | Crete | 9.29 | - | 4 | 3 | - | - | 30 | measured |
| 144 | Nice | 9.29 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 145 | Parma | 5.16 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 146 | Winnipeg | 9.21 | - | - | - | - | - | 30 | predicted (travel demand) |
| 147 | Cordoba | 5.85 | 74,675 | 16 | 2 | 2 | 3 | 30 | measured |
| 148 | Bologna | 4.82 | 146,161 | 12 | 7 | 1 | 9 | 30 | measured |
| 149 | Enschede | 4.48 | - | 15 | 1 | 2 | 82 | 20 | measured |
| 150 | Groningen | 4.48 | 31,401 | 21 | 1 | 2 | 76 | 20 | measured |
| 151 | Zwolle | 4.48 | - | 20 | - | 4 | 58 | 20 | measured |
| 152 | Nashville | 8.93 | - | - | - | - | - | 30 | predicted (travel demand) |
| 153 | Tampere | 8.78 | - | - | - | - | - | 30 | predicted (travel demand) |
| 154 | Zurich | 8.26 | 140,788 | 6 | 1 | - | - | 30 | measured |
| 155 | Ann Arbor | 8.55 | - | - | - | - | - | 20 | predicted (travel demand) |
| 156 | Charleston | 8.26 | 155,987 | 3 | 1 | - | - | 20 | measured |
| 157 | Adelaide | 8.14 | 139,166 | - | - | - | - | 60 | predicted (travel demand) |
| 158 | Quebec City | 5.51 | 124,358 | 6 | - | 1 | 494 | 30 | measured |
| 159 | Sapporo | 5.51 | 88,633 | 6 | - | - | - | 60 | measured |
| 160 | Segovia | 5.16 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 161 | Stockholm | 6.54 | 188,184 | 8 | 4 | - | - | 30 | measured |
| 162 | Albuquerque | 7.83 | - | - | - | - | - | 30 | predicted (travel demand) |
| 163 | Nuremberg | 5.16 | 161,614 | 12 | 1 | 1 | 38 | 30 | measured |
| 164 | Delft | 3.79 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 165 | Savannah | 7.57 | 128,162 | 3 | 1 | - | - | 20 | measured |
| 166 | Taipei | 7.57 | 143,193 | 4 | 1 | - | - | 60 | measured |
| 167 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 20 | predicted (travel demand) |
| 168 | Bergen | 7.30 | 82,940 | - | - | - | - | 30 | predicted (travel demand) |
| 169 | Istanbul | 6.37 | 333,027 | 14 | 4 | 1 | - | 100 | measured |
| 170 | Perth | 6.88 | 180,478 | 6 | 3 | 1 | - | 60 | measured |
| 171 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 20 | predicted (travel demand) |
| 172 | Siena | 4.62 | 57,436 | - | - | - | - | 20 | predicted (travel demand) |
| 173 | Apeldoorn | 3.44 | - | 10 | - | 2 | 80 | 20 | measured |
| 174 | Hawaii | 6.88 | - | 6 | - | 1 | - | 60 | measured |
| 175 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 20 | predicted (travel demand) |
| 176 | Tallinn | 4.48 | 124,888 | 9 | 3 | 2 | 42 | 30 | measured |
| 177 | Guimaraes | 3.44 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 178 | Zagreb | 6.42 | 122,890 | - | - | - | - | 30 | predicted (travel demand) |
| 179 | Cambridge | 6.54 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 180 | Manchester | 6.54 | 316,438 | 5 | - | - | - | 30 | measured |
| 181 | Helsinki | 5.16 | 148,908 | 12 | 2 | 1 | 13 | 30 | measured |
| 182 | Hong Kong | 4.30 | 689,212 | 10 | 4 | 1 | 505 | 100 | measured |
| 183 | Bogota | 6.39 | 1,623 | - | - | - | - | 100 | predicted (travel demand) |
| 184 | Shanghai | 6.38 | 277,140 | - | - | - | - | 100 | predicted (travel demand) |
| 185 | Vancouver | 6.20 | 351,552 | 7 | - | - | - | 30 | measured |
| 186 | Funchal | 3.77 | 174,351 | - | - | - | - | 20 | predicted (travel demand) |
| 187 | Deventer | 3.10 | - | 12 | - | 1 | 213 | 20 | measured |
| 188 | Dubrovnik | 5.85 | 119,586 | 4 | 1 | - | 2 | 10 | measured |
| 189 | Lucca | 3.10 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 190 | Minneapolis | 6.20 | - | 4 | - | - | - | 30 | measured |
| 191 | Tilburg | 3.10 | - | 20 | - | 3 | 87 | 20 | measured |
| 192 | Venlo | 3.10 | - | 7 | - | 1 | 144 | 20 | measured |
| 193 | Malta | 5.79 | - | - | - | - | - | 30 | predicted (travel demand) |
| 194 | Bari | 3.44 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 195 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 196 | Avignon | 5.54 | 64,047 | - | - | - | - | 20 | predicted (travel demand) |
| 197 | Como | 2.75 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 198 | Galway | 3.65 | 88,162 | - | - | - | - | 20 | predicted (travel demand) |
| 199 | Phuket | 5.46 | 5,487 | - | - | - | - | 30 | predicted (travel demand) |
| 200 | Rovaniemi | 5.38 | - | - | - | - | - | 20 | predicted (travel demand) |
| 201 | Lagos | 3.43 | 34,452 | - | - | - | - | 100 | predicted (travel demand) |
| 202 | Nagoya | 3.44 | 83,437 | 6 | 1 | - | 1 | 60 | measured |
| 203 | Santa Fe | 5.17 | - | - | - | - | - | 20 | predicted (travel demand) |
| 204 | Lund | 5.14 | - | - | - | - | - | 20 | predicted (travel demand) |
| 205 | Kobe | 3.40 | 54,798 | - | - | - | - | 60 | predicted (travel demand) |
| 206 | Genoa | 2.75 | 145,206 | 13 | 2 | 1 | 10 | 30 | measured |
| 207 | Heraklion | 4.96 | 66,359 | - | - | - | - | 20 | predicted (travel demand) |
| 208 | Marseille | 4.96 | 182,033 | - | - | - | - | 30 | predicted (travel demand) |
| 209 | Aarhus | 4.82 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 210 | Indianapolis | 4.82 | - | 1 | - | - | - | 30 | measured |
| 211 | Assen | 2.41 | - | 10 | - | 2 | 66 | 20 | measured |
| 212 | Den Bosch | 2.41 | 39,682 | 12 | 2 | 1 | 118 | 20 | measured |
| 213 | Hoorn | 2.41 | - | 12 | - | 2 | 52 | 20 | measured |
| 214 | Kauai | 4.82 | - | 6 | 1 | - | - | 20 | measured |
| 215 | Graz | 3.10 | 65,717 | 13 | 7 | 2 | 87 | 30 | measured |
| 216 | Lyon | 3.10 | 136,951 | 13 | 4 | 1 | 156 | 30 | measured |
| 217 | Toulouse | 3.10 | 112,721 | 10 | - | 1 | 34 | 30 | measured |
| 218 | Basel | 4.59 | 105,838 | - | - | - | - | 20 | predicted (travel demand) |
| 219 | Toronto | 4.48 | 411,011 | 6 | - | - | - | 60 | measured |
| 220 | Padua | 2.41 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 221 | Bristol | 4.48 | 163,983 | 6 | 2 | - | - | 30 | measured |
| 222 | Tasmania | 4.41 | - | - | - | - | - | 30 | predicted (travel demand) |
| 223 | Hallstatt | 3.79 | 47,271 | 5 | 1 | - | - | 10 | measured |
| 224 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 20 | predicted (travel demand) |
| 225 | Ghent | 4.13 | 82,757 | 8 | 1 | 1 | - | 30 | measured |
| 226 | San Sebastian | 2.80 | 367 | - | - | - | - | 20 | predicted (travel demand) |
| 227 | Salamanca | 2.75 | 47,897 | 4 | - | 1 | 1 | 20 | measured |
| 228 | Roosendaal | 2.07 | - | 8 | - | 1 | 116 | 20 | measured |
| 229 | Cologne | 4.13 | 191,812 | 5 | - | 1 | - | 60 | measured |
| 230 | Bordeaux | 2.75 | 156,201 | 10 | - | 2 | 211 | 30 | measured |
| 231 | Brno | 2.75 | 63,714 | 8 | 5 | 2 | 34 | 30 | measured |
| 232 | Gdansk | 2.75 | 4,908 | 12 | 4 | 1 | 307 | 30 | measured |
| 233 | Stuttgart | 3.10 | 112,789 | 6 | 1 | - | - | 30 | measured |
| 234 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 30 | predicted (travel demand) |
| 235 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 236 | Hamburg | 3.79 | 191,221 | 6 | 1 | 1 | - | 60 | measured |
| 237 | Azores | 2.62 | - | - | - | - | - | 20 | predicted (travel demand) |
| 238 | Cardiff | 3.79 | - | 4 | - | 1 | - | 30 | measured |
| 239 | Ljubljana | 3.79 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 240 | Oxford | 3.79 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 241 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 242 | Niagara Falls | 3.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 243 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 100 | predicted (travel demand) |
| 244 | Wellington | 3.60 | 132,267 | - | - | - | - | 20 | predicted (travel demand) |
| 245 | Heidelberg | 3.10 | 75,837 | 6 | 1 | 1 | - | 20 | measured |
| 246 | Montpellier | 3.47 | 64,238 | - | - | - | - | 30 | predicted (travel demand) |
| 247 | Alkmaar | 1.72 | - | 14 | - | 2 | 79 | 20 | measured |
| 248 | Beijing | 3.44 | 269,737 | 7 | 1 | - | - | 100 | measured |
| 249 | Bergamo | 1.72 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 250 | Kansas City | 3.44 | - | 4 | - | 1 | - | 30 | measured |
| 251 | Trieste | 1.72 | 117,233 | 36 | 1 | 3 | 43 | 20 | measured |
| 252 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 253 | Cape Town | 3.29 | 199,169 | - | - | - | - | 60 | predicted (travel demand) |
| 254 | Rhodes | 3.42 | 127,205 | - | - | - | - | 20 | predicted (travel demand) |
| 255 | San Antonio | 3.32 | - | 4 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 256 | Chania | 3.30 | 47,379 | - | - | - | - | 20 | predicted (travel demand) |
| 257 | Santiago | 3.25 | 111,647 | - | - | - | - | 100 | predicted (travel demand) |
| 258 | Perugia | 1.72 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 259 | Freiburg | 3.10 | 92,752 | 7 | 2 | 1 | - | 20 | measured |
| 260 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 30 | predicted (travel demand) |
| 261 | Setubal | 1.72 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 262 | Mexico City | 2.93 | 566,583 | 9 | 2 | - | - | 100 | measured |
| 263 | Bratislava | 2.07 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 264 | Bruges | 3.10 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 265 | Dresden | 2.07 | 113,624 | 13 | 9 | 1 | - | 30 | measured |
| 266 | Lucerne | 3.10 | 66,356 | - | - | - | - | 20 | predicted (travel demand) |
| 267 | Salzburg | 2.07 | 107,243 | 12 | 3 | 2 | 34 | 20 | measured |
| 268 | Malmo | 3.07 | 103,940 | - | - | - | - | 30 | predicted (travel demand) |
| 269 | Lille | 3.06 | 73,435 | - | - | - | - | 20 | predicted (travel demand) |
| 270 | Corsica | 3.00 | - | - | - | - | - | 30 | predicted (travel demand) |
| 271 | Mechelen | 2.93 | 20,707 | - | - | - | - | 20 | predicted (travel demand) |
| 272 | Belgrade | 2.93 | 178,116 | 5 | 5 | - | - | 60 | measured |
| 273 | Modena | 1.72 | 51,698 | 5 | 1 | 1 | 3 | 20 | measured |
| 274 | Poznan | 1.89 | 65,666 | 10 | - | 1 | 397 | 30 | published, never ranked (may be uncrawled) |
| 275 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 276 | Tulsa | 2.75 | - | 1 | - | - | - | 30 | measured |
| 277 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 278 | Corfu | 2.71 | 139,334 | - | - | - | - | 20 | predicted (travel demand) |
| 279 | Menorca | 1.72 | - | 6 | - | - | 2 | 20 | measured |
| 280 | Syracuse | 1.75 | 102,833 | - | - | - | - | 20 | predicted (travel demand) |
| 281 | Zaragoza | 1.72 | 87,580 | 7 | - | 1 | - | 30 | measured |
| 282 | Bilbao | 1.72 | 133,133 | 4 | - | 1 | - | 30 | measured |
| 283 | Cartagena | 2.58 | 65,066 | - | - | - | - | 30 | predicted (travel demand) |
| 284 | Gran Canaria | 1.67 | - | - | - | - | - | 30 | predicted (travel demand) |
| 285 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 20 | predicted (travel demand) |
| 286 | Bern | 2.51 | 90,627 | - | - | - | - | 20 | predicted (travel demand) |
| 287 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 288 | Faro | 1.62 | 55,645 | - | - | - | - | 20 | predicted (travel demand) |
| 289 | Belfast | 2.41 | 224,315 | 5 | 1 | 1 | - | 30 | measured |
| 290 | Lausanne | 2.41 | 68,242 | 8 | 1 | 1 | - | 20 | measured |
| 291 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 292 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 293 | Catania | 1.38 | 58,252 | 4 | 3 | 1 | 5 | 30 | measured |
| 294 | Cusco | 2.35 | 87,732 | - | - | - | - | 30 | predicted (travel demand) |
| 295 | Limerick | 1.57 | 90,379 | - | - | - | - | 20 | predicted (travel demand) |
| 296 | Ronda | 1.38 | 51,510 | 6 | 1 | - | 9 | 10 | measured |
| 297 | Matera | 1.38 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 298 | Tarragona | 1.38 | 32,396 | 4 | 2 | - | - | 20 | measured |
| 299 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 20 | predicted (travel demand) |
| 300 | Pisa | 1.38 | 52,174 | 4 | - | - | - | 20 | measured |
| 301 | Auckland | 1.38 | 152,056 | 5 | 2 | - | 977 | 60 | measured |
| 302 | Fort Worth | 2.07 | - | 5 | - | - | - | 30 | measured |
| 303 | Hilo | 2.07 | - | 6 | - | 1 | - | 10 | measured |
| 304 | San Diego | 2.07 | 214,939 | 6 | 1 | 1 | - | 60 | measured |
| 305 | Hilversum | 1.03 | - | 6 | 1 | 1 | 122 | 20 | measured |
| 306 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 307 | Rotterdam | 1.03 | 104,938 | 16 | - | 2 | 83 | 30 | measured |
| 308 | Trento | 1.03 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 309 | Ischia | 1.32 | - | - | - | - | 2 | 20 | predicted (travel demand) |
| 310 | Izmir | 1.88 | 69,826 | - | - | - | - | 60 | predicted (travel demand) |
| 311 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 312 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 313 | Bangkok | 1.72 | 222,206 | 5 | 1 | 1 | - | 100 | measured |
| 314 | Dijon | 1.72 | 43,526 | - | - | - | - | 20 | predicted (travel demand) |
| 315 | Trier | 1.56 | 69,369 | - | - | - | - | 20 | predicted (travel demand) |
| 316 | Annecy | 1.69 | 56,859 | - | - | - | - | 20 | predicted (travel demand) |
| 317 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 318 | Canterbury | 1.59 | 53,301 | - | - | - | - | 20 | predicted (travel demand) |
| 319 | Mostar | 1.58 | 63,907 | - | - | - | - | 20 | predicted (travel demand) |
| 320 | Cesky Krumlov | 1.03 | 28,582 | 6 | 3 | - | 11 | 10 | measured |
| 321 | Hiroshima | 1.03 | 129,791 | 33 | 5 | 2 | - | 60 | measured |
| 322 | Potsdam | 1.03 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 323 | Zadar | 1.53 | 71,549 | - | - | - | - | 20 | predicted (travel demand) |
| 324 | Gothenburg | 1.49 | 119,991 | 5 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 325 | Thessaloniki | 1.42 | 180,145 | 4 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 326 | Pittsburgh | 1.38 | - | 4 | - | 1 | - | 30 | measured |
| 327 | Breda | 0.69 | 36,579 | 11 | 1 | 2 | 120 | 20 | measured |
| 328 | Heerlen | 0.69 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 329 | Leuven | 1.38 | 40,645 | 4 | - | - | - | 20 | measured |
| 330 | Nantes | 1.38 | 67,689 | 1 | 1 | - | - | 30 | measured |
| 331 | Turku | 1.38 | - | 1 | - | - | - | 20 | measured |
| 332 | Antalya | 1.31 | 70,688 | - | - | - | - | 60 | predicted (travel demand) |
| 333 | Colmar | 1.28 | 45,517 | - | - | - | - | 20 | predicted (travel demand) |
| 334 | Bodrum | 1.26 | 33,918 | - | - | - | - | 20 | predicted (travel demand) |
| 335 | Bamberg | 1.03 | 28,716 | 5 | 4 | 1 | 10 | 20 | measured |
| 336 | Braga | 0.69 | 34,522 | 4 | 2 | - | 8 | 20 | measured |
| 337 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 338 | Evora | 0.78 | 15,345 | - | - | - | - | 20 | predicted (travel demand) |
| 339 | Rouen | 1.03 | 72,334 | 12 | - | 1 | 6 | 20 | measured |
| 340 | Regensburg | 1.03 | 51,930 | 5 | 1 | 1 | 4 | 20 | measured |
| 341 | Assisi | 0.69 | 30,278 | 6 | 1 | 2 | 6 | 10 | measured |
| 342 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 343 | La Palma | 0.70 | - | - | - | - | - | 20 | predicted (travel demand) |
| 344 | Okinawa | 0.69 | 24,466 | 6 | - | - | 1 | 30 | measured |
| 345 | Antwerp | 1.03 | 128,289 | 10 | 4 | 1 | - | 30 | measured |
| 346 | Christchurch | 0.69 | 104,874 | 6 | - | 1 | 466 | 30 | measured |
| 347 | Split | 1.03 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 348 | Wroclaw | 0.69 | 123,894 | 5 | 1 | 1 | 121 | 30 | measured |
| 349 | York | 1.03 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 350 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 60 | predicted (travel demand) |
| 351 | Rothenburg ob der Tauber | 0.77 | 39,879 | 4 | - | 1 | 8 | 10 | published, never ranked (may be uncrawled) |
| 352 | Rio de Janeiro | 0.86 | 279,431 | 6 | - | - | - | 100 | measured |
| 353 | Baltimore | 0.69 | - | 4 | - | - | - | 30 | measured |
| 354 | Fort Lauderdale | 0.69 | - | 4 | - | - | - | 20 | measured |
| 355 | Kamakura | 0.44 | 33,492 | 6 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 356 | Brighton | 0.69 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 357 | Bucharest | 0.69 | 136,836 | 4 | - | 1 | - | 60 | measured |
| 358 | Maui | 0.69 | - | 4 | - | - | - | 20 | measured |
| 359 | Turin | 0.34 | 147,456 | 11 | 7 | 2 | 30 | 30 | measured |
| 360 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 100 | published, never ranked (may be uncrawled) |
| 361 | Ferrara | 0.34 | 27,490 | 5 | 3 | 1 | 7 | 20 | measured |
| 362 | Phoenix | 0.55 | - | - | - | - | - | 60 | predicted (travel demand) |
| 363 | Buenos Aires | 0.52 | 333,331 | 4 | 2 | - | - | 60 | measured |
| 364 | Sofia | 0.34 | 138,710 | 4 | - | - | - | 60 | measured |
| 365 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 366 | Toledo | 0.24 | 3,149 | - | - | - | - | 20 | predicted (travel demand) |
| 367 | Busan | 0.34 | 94,737 | 2 | - | - | - | 60 | measured |
| 368 | Riga | 0.34 | 108,918 | 5 | 2 | - | - | 30 | measured |
| 369 | Canberra | 0.34 | - | 1 | 1 | - | - | 30 | measured |
| 370 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 371 | George Town | 0.28 | 36,080 | - | - | - | - | 30 | predicted (travel demand) |
| 372 | Allentown | 0.24 | - | - | - | - | - | 20 | predicted (travel demand) |
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

