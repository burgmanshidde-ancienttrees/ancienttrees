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
| 1 | Prague | 1201.20 | 303,350 | 30 | 21 | 4 | 31 | 60 | measured |
| 2 | Brussels | 48.05 | 176,863 | 35 | 4 | 2 | 436 | 60 | measured |
| 3 | Tenerife | 29.57 | - | 4 | 4 | - | - | 30 | measured |
| 4 | Munich | 25.87 | 224,067 | 62 | 32 | 8 | 76 | 60 | measured |
| 5 | Birmingham | 37.53 | - | - | - | - | - | 60 | predicted (travel demand) |
| 6 | Cambridge | 36.96 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 7 | Porto | 18.48 | 120,415 | 27 | 17 | 2 | 40 | 30 | measured |
| 8 | Yakushima | 18.48 | - | 2 | - | - | 1 | 10 | measured |
| 9 | Seville | 18.48 | 170,545 | 43 | 11 | 2 | - | 30 | measured |
| 10 | Brisbane | 18.48 | 162,602 | 20 | 2 | 2 | 186 | 60 | measured |
| 11 | Seattle | 22.18 | 398,724 | 16 | 1 | 2 | - | 30 | measured |
| 12 | Jacksonville | 22.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 13 | Alicante | 11.09 | 77,454 | 21 | 4 | 2 | 44 | 30 | measured |
| 14 | Alkmaar | 11.09 | - | 11 | - | 2 | 79 | 20 | measured |
| 15 | Barcelona | 11.09 | 346,477 | 56 | 14 | 7 | 180 | 60 | measured |
| 16 | Paris | 14.78 | 524,268 | 31 | 11 | 4 | 129 | 60 | measured |
| 17 | Asheville | 20.89 | - | - | - | - | - | 20 | predicted (travel demand) |
| 18 | Long Beach | 20.48 | - | - | - | - | - | 30 | predicted (travel demand) |
| 19 | Little Rock | 20.40 | - | - | - | - | - | 20 | predicted (travel demand) |
| 20 | Oakland | 18.81 | - | - | - | - | - | 30 | predicted (travel demand) |
| 21 | Madeira | 11.09 | - | 10 | 1 | 1 | - | 30 | measured |
| 22 | Lexington | 18.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 23 | Reno | 18.19 | - | - | - | - | - | 30 | predicted (travel demand) |
| 24 | Des Moines | 18.11 | - | - | - | - | - | 20 | predicted (travel demand) |
| 25 | Key West | 15.81 | - | - | - | - | 7 | 10 | predicted (travel demand) |
| 26 | Daytona Beach | 17.66 | - | - | - | - | - | 20 | predicted (travel demand) |
| 27 | Chattanooga | 16.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 28 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 29 | New York | 14.78 | 1,124,326 | 27 | 6 | 2 | - | 100 | measured |
| 30 | Huntsville | 15.35 | - | - | - | - | - | 20 | predicted (travel demand) |
| 31 | San Francisco | 14.78 | 361,111 | 8 | 2 | 1 | - | 30 | measured |
| 32 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 33 | West Palm Beach | 14.98 | - | - | - | - | - | 20 | predicted (travel demand) |
| 34 | Saint Petersburg | 14.83 | - | - | - | - | - | 100 | predicted (travel demand) |
| 35 | St. Louis | 14.80 | - | - | - | - | - | 30 | predicted (travel demand) |
| 36 | Amsterdam | 7.39 | 294,030 | 27 | 7 | 2 | 5488 | 30 | measured |
| 37 | Leeuwarden | 7.39 | - | 34 | - | 2 | 61 | 20 | measured |
| 38 | Lisbon | 7.39 | 201,877 | 36 | 17 | 3 | 67 | 30 | measured |
| 39 | Milan | 7.39 | 212,705 | 30 | 14 | 3 | 25 | 60 | measured |
| 40 | Oahu | 14.78 | - | 21 | 7 | 3 | - | 30 | measured |
| 41 | Roosendaal | 7.39 | - | 8 | - | 1 | 116 | 20 | measured |
| 42 | Sorrento | 7.39 | 40,049 | 7 | - | 1 | 20 | 10 | measured |
| 43 | Tampa | 14.10 | - | - | - | - | - | 30 | predicted (travel demand) |
| 44 | Cincinnati | 13.33 | - | - | - | - | - | 30 | predicted (travel demand) |
| 45 | Tokyo | 7.39 | 394,702 | 22 | 15 | 1 | 5 | 100 | measured |
| 46 | Lansing | 13.02 | - | - | - | - | - | 20 | predicted (travel demand) |
| 47 | Dublin | 7.39 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 48 | Detroit | 12.53 | - | - | - | - | - | 30 | predicted (travel demand) |
| 49 | Miami | 9.48 | 278,558 | - | - | - | 15 | 30 | predicted (travel demand) |
| 50 | Denver | 11.66 | - | - | - | - | - | 30 | predicted (travel demand) |
| 51 | Kyoto | 7.39 | 142,353 | 18 | 12 | 2 | - | 60 | measured |
| 52 | Venice | 6.28 | 267,527 | 11 | 6 | 2 | 4 | 30 | published, never ranked (may be uncrawled) |
| 53 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 60 | predicted (travel demand) |
| 54 | San Jose | 11.39 | - | - | - | - | - | 60 | predicted (travel demand) |
| 55 | Kanazawa | 7.39 | 25,778 | 7 | 2 | 1 | 2 | 30 | measured |
| 56 | Sacramento | 11.32 | - | - | - | - | - | 30 | predicted (travel demand) |
| 57 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 60 | predicted (travel demand) |
| 58 | Berlin | 7.39 | 412,181 | 63 | 23 | 5 | 195 | 60 | measured |
| 59 | Leipzig | 7.39 | 121,319 | 19 | 19 | 3 | - | 30 | measured |
| 60 | Tallinn | 7.39 | 124,888 | 9 | 3 | 2 | 42 | 30 | measured |
| 61 | Dubai | 11.02 | 334,167 | - | - | - | - | 60 | predicted (travel demand) |
| 62 | Milwaukee | 10.63 | - | - | - | - | - | 30 | predicted (travel demand) |
| 63 | Jersey City | 10.08 | - | - | - | - | - | 30 | predicted (travel demand) |
| 64 | Atlanta | 10.29 | - | - | - | - | - | 30 | predicted (travel demand) |
| 65 | Anchorage | 10.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 66 | Raleigh | 10.07 | - | - | - | - | - | 30 | predicted (travel demand) |
| 67 | Bali | 9.95 | - | - | - | - | - | 60 | predicted (travel demand) |
| 68 | Cleveland | 9.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 69 | El Paso | 9.70 | - | - | - | - | - | 30 | predicted (travel demand) |
| 70 | Las Vegas | 9.64 | - | 11 | - | 2 | - | 30 | published, never ranked (may be uncrawled) |
| 71 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 72 | Edmonton | 9.38 | - | - | - | - | - | 60 | predicted (travel demand) |
| 73 | Winnipeg | 9.21 | - | - | - | - | - | 30 | predicted (travel demand) |
| 74 | Singapore | 6.12 | 967,821 | 34 | 7 | 3 | 165 | 100 | published, never ranked (may be uncrawled) |
| 75 | Chicago | 7.39 | 485,769 | 16 | - | - | 11 | 60 | measured |
| 76 | Nashville | 8.93 | - | - | - | - | - | 30 | predicted (travel demand) |
| 77 | Tampere | 8.78 | - | - | - | - | - | 30 | predicted (travel demand) |
| 78 | London | 7.39 | 718,291 | 27 | 19 | 1 | - | 100 | measured |
| 79 | Ann Arbor | 8.55 | - | - | - | - | - | 20 | predicted (travel demand) |
| 80 | Adelaide | 8.14 | 139,166 | - | - | - | - | 60 | predicted (travel demand) |
| 81 | Albuquerque | 7.83 | - | - | - | - | - | 30 | predicted (travel demand) |
| 82 | Charleston | 7.39 | 155,987 | 3 | 1 | - | - | 20 | measured |
| 83 | Cyprus | 7.39 | - | 4 | - | - | - | 60 | measured |
| 84 | Edinburgh | 7.39 | 292,981 | 16 | 5 | 1 | - | 30 | measured |
| 85 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 20 | predicted (travel demand) |
| 86 | Arnhem | 3.70 | 31,478 | 32 | 3 | 3 | 202 | 20 | measured |
| 87 | Breda | 3.70 | 36,579 | 11 | 1 | 2 | 120 | 20 | measured |
| 88 | Delft | 3.70 | 31,293 | 10 | - | 1 | 62 | 20 | measured |
| 89 | Groningen | 3.70 | 31,401 | 17 | - | 2 | 76 | 20 | measured |
| 90 | Lucca | 3.70 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 91 | Rome | 3.70 | 358,876 | 31 | 10 | 2 | 32 | 60 | measured |
| 92 | Sintra | 3.70 | 46,889 | 5 | 3 | - | 6 | 30 | measured |
| 93 | The Hague | 3.70 | 236,723 | 28 | 3 | 5 | 169 | 30 | measured |
| 94 | Bath | 7.39 | 144,950 | 5 | 2 | 1 | - | 20 | measured |
| 95 | Hawaii | 7.39 | - | 6 | - | 1 | - | 60 | measured |
| 96 | Kauai | 7.39 | - | 6 | 1 | - | - | 20 | measured |
| 97 | Minneapolis | 7.39 | - | 4 | - | - | - | 30 | measured |
| 98 | Monterey | 7.39 | - | 3 | 1 | - | - | 10 | measured |
| 99 | New Orleans | 7.39 | 256,232 | 8 | 5 | 1 | - | 30 | measured |
| 100 | Savannah | 7.39 | 128,162 | 3 | 1 | - | - | 20 | measured |
| 101 | Los Angeles | 7.20 | 665,559 | 11 | 2 | - | - | 60 | published, never ranked (may be uncrawled) |
| 102 | Bergen | 7.30 | 82,940 | - | - | - | - | 30 | predicted (travel demand) |
| 103 | Guimaraes | 3.70 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 104 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 20 | predicted (travel demand) |
| 105 | Siena | 4.62 | 57,436 | - | - | - | - | 20 | predicted (travel demand) |
| 106 | Cagliari | 3.70 | 51,351 | 14 | 1 | 2 | 14 | 20 | measured |
| 107 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 20 | predicted (travel demand) |
| 108 | Frankfurt | 4.51 | 150,379 | 11 | 1 | - | - | 30 | published, never ranked (may be uncrawled) |
| 109 | Zagreb | 6.42 | 122,890 | - | - | - | - | 30 | predicted (travel demand) |
| 110 | Bogota | 6.39 | 1,623 | - | - | - | - | 100 | predicted (travel demand) |
| 111 | Shanghai | 6.38 | 277,140 | - | - | - | - | 100 | predicted (travel demand) |
| 112 | Funchal | 3.77 | 174,351 | - | - | - | - | 20 | predicted (travel demand) |
| 113 | Verona | 3.70 | 77,646 | 8 | 4 | 1 | 3 | 30 | measured |
| 114 | Dallas | 6.15 | - | 12 | 1 | 1 | - | 60 | published, never ranked (may be uncrawled) |
| 115 | Palma de Mallorca | 3.70 | 84,075 | 5 | 1 | 1 | 8 | 30 | measured |
| 116 | Houston | 6.11 | - | 11 | - | 1 | - | 60 | published, never ranked (may be uncrawled) |
| 117 | Toronto | 5.96 | 411,011 | 6 | - | - | - | 60 | published, never ranked (may be uncrawled) |
| 118 | Assisi | 3.70 | 30,278 | 6 | 1 | 2 | 6 | 10 | measured |
| 119 | Madrid | 3.70 | 274,553 | 17 | 11 | 2 | - | 60 | measured |
| 120 | Granada | 3.70 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 121 | Malta | 5.79 | - | - | - | - | - | 30 | predicted (travel demand) |
| 122 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 123 | Fukuoka | 3.70 | 77,485 | 18 | 11 | 1 | - | 60 | measured |
| 124 | Montreal | 5.70 | 315,322 | 13 | 1 | 2 | - | 60 | published, never ranked (may be uncrawled) |
| 125 | Hiroshima | 3.70 | 129,791 | 33 | 5 | 2 | - | 60 | measured |
| 126 | Krakow | 3.70 | 140,824 | 38 | 8 | 3 | 198 | 30 | measured |
| 127 | Lyon | 3.70 | 136,951 | 13 | 4 | 1 | 156 | 30 | measured |
| 128 | Melbourne | 3.70 | 267,898 | 16 | 1 | 2 | 403 | 100 | measured |
| 129 | Nuremberg | 3.70 | 161,614 | 18 | 5 | 2 | 37 | 30 | measured |
| 130 | Ottawa | 3.70 | - | 21 | - | 3 | 122 | 60 | measured |
| 131 | Quebec City | 3.70 | 124,358 | 6 | - | 1 | 494 | 30 | measured |
| 132 | Vienna | 3.70 | 283,090 | 55 | 19 | 6 | 369 | 60 | measured |
| 133 | Vilnius | 3.70 | 113,188 | 12 | 1 | 1 | 34 | 30 | published, never ranked (may be uncrawled) |
| 134 | Avignon | 5.54 | 64,047 | - | - | - | - | 20 | predicted (travel demand) |
| 135 | Galway | 3.65 | 88,162 | - | - | - | - | 20 | predicted (travel demand) |
| 136 | Phuket | 5.46 | 5,487 | - | - | - | - | 30 | predicted (travel demand) |
| 137 | Spokane | 3.92 | - | 13 | - | 2 | 18 | 20 | published, never ranked (may be uncrawled) |
| 138 | Rovaniemi | 5.38 | - | - | - | - | - | 20 | predicted (travel demand) |
| 139 | Aarhus | 5.23 | 52,722 | 7 | 1 | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 140 | Lagos | 3.43 | 34,452 | - | - | - | - | 100 | predicted (travel demand) |
| 141 | Kansas City | 5.26 | - | 4 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 142 | Santa Fe | 5.17 | - | - | - | - | - | 20 | predicted (travel demand) |
| 143 | Lund | 5.14 | - | - | - | - | - | 20 | predicted (travel demand) |
| 144 | Kobe | 3.40 | 54,798 | - | - | - | - | 60 | predicted (travel demand) |
| 145 | Boise | 5.07 | - | 4 | - | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 146 | Fort Lauderdale | 4.61 | - | 4 | - | - | 4 | 20 | published, never ranked (may be uncrawled) |
| 147 | Sydney | 4.92 | 305,304 | 7 | 1 | - | - | 100 | published, never ranked (may be uncrawled) |
| 148 | Heraklion | 4.96 | 66,359 | - | - | - | - | 20 | predicted (travel demand) |
| 149 | Marseille | 4.96 | 182,033 | - | - | - | - | 30 | predicted (travel demand) |
| 150 | Stuttgart | 3.70 | 112,789 | 6 | 1 | - | - | 30 | measured |
| 151 | Indianapolis | 4.57 | - | 1 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 152 | Basel | 4.59 | 105,838 | - | - | - | - | 20 | predicted (travel demand) |
| 153 | Portland | 3.06 | 217,222 | 33 | 1 | 3 | 306 | 30 | published, never ranked (may be uncrawled) |
| 154 | Glasgow | 4.29 | 253,705 | 5 | 3 | - | - | 30 | published, never ranked (may be uncrawled) |
| 155 | Boston | 4.28 | 385,902 | 13 | 2 | 2 | - | 30 | published, never ranked (may be uncrawled) |
| 156 | Florence | 2.21 | 184,099 | 27 | 9 | 1 | 27 | 30 | published, never ranked (may be uncrawled) |
| 157 | Valencia | 2.21 | 162,209 | 31 | 4 | 2 | 350 | 30 | published, never ranked (may be uncrawled) |
| 158 | Tasmania | 4.41 | - | - | - | - | - | 30 | predicted (travel demand) |
| 159 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 20 | predicted (travel demand) |
| 160 | Reykjavik | 3.70 | 166,789 | 4 | 3 | 1 | - | 20 | measured |
| 161 | Sofia | 2.81 | 138,710 | 4 | - | - | - | 60 | published, never ranked (may be uncrawled) |
| 162 | San Sebastian | 2.80 | 367 | - | - | - | - | 20 | predicted (travel demand) |
| 163 | Perth | 4.10 | 180,478 | 6 | 3 | 1 | - | 60 | published, never ranked (may be uncrawled) |
| 164 | Rouen | 3.70 | 72,334 | 12 | - | 1 | 6 | 20 | measured |
| 165 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 30 | predicted (travel demand) |
| 166 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 167 | Washington DC | 3.68 | 606,731 | 16 | 1 | 3 | - | 30 | published, never ranked (may be uncrawled) |
| 168 | Eindhoven | 1.99 | - | 17 | - | 3 | 195 | 20 | published, never ranked (may be uncrawled) |
| 169 | Osaka | 2.54 | 163,112 | 6 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 170 | Azores | 2.62 | - | - | - | - | - | 20 | predicted (travel demand) |
| 171 | Pittsburgh | 3.80 | - | 4 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 172 | Budapest | 3.70 | 283,807 | 13 | 2 | 3 | - | 60 | measured |
| 173 | Sao Paulo | 3.70 | 911 | 2 | - | - | - | 100 | measured |
| 174 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 175 | Niagara Falls | 3.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 176 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 100 | predicted (travel demand) |
| 177 | Athens | 3.70 | 235,429 | 12 | 7 | 2 | - | 30 | measured |
| 178 | Vancouver | 3.70 | 351,552 | 7 | - | - | - | 30 | measured |
| 179 | Malaga | 2.51 | 117,780 | 9 | 5 | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 180 | Bratislava | 2.49 | 132,162 | 7 | 1 | 1 | 26 | 30 | published, never ranked (may be uncrawled) |
| 181 | Beijing | 3.70 | 269,737 | 7 | 1 | - | - | 100 | measured |
| 182 | Leuven | 3.70 | 40,645 | 4 | - | - | - | 20 | measured |
| 183 | Manchester | 3.70 | 316,438 | 5 | - | - | - | 30 | measured |
| 184 | Strasbourg | 2.45 | 154,700 | 10 | 2 | 2 | 66 | 30 | published, never ranked (may be uncrawled) |
| 185 | Wellington | 3.60 | 132,267 | - | - | - | - | 20 | predicted (travel demand) |
| 186 | Naples | 1.83 | 198,913 | 24 | 3 | 3 | 46 | 30 | published, never ranked (may be uncrawled) |
| 187 | Bari | 2.16 | 86,456 | 5 | 1 | - | 8 | 30 | published, never ranked (may be uncrawled) |
| 188 | Rotterdam | 1.81 | 104,938 | 16 | - | 2 | 83 | 30 | published, never ranked (may be uncrawled) |
| 189 | Salt Lake City | 2.58 | - | 5 | - | 1 | 20 | 20 | published, never ranked (may be uncrawled) |
| 190 | Warsaw | 2.40 | 197,929 | 39 | 20 | 4 | 1407 | 60 | published, never ranked (may be uncrawled) |
| 191 | Bologna | 1.90 | 146,161 | 12 | 7 | 1 | 9 | 30 | published, never ranked (may be uncrawled) |
| 192 | Stockholm | 2.82 | 188,184 | 8 | 4 | - | - | 30 | published, never ranked (may be uncrawled) |
| 193 | Montpellier | 3.47 | 64,238 | - | - | - | - | 30 | predicted (travel demand) |
| 194 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 195 | Cape Town | 3.29 | 199,169 | - | - | - | - | 60 | predicted (travel demand) |
| 196 | Rhodes | 3.42 | 127,205 | - | - | - | - | 20 | predicted (travel demand) |
| 197 | Girona | 1.97 | 51,072 | 7 | 3 | - | - | 20 | published, never ranked (may be uncrawled) |
| 198 | Bangkok | 3.32 | 222,206 | 5 | 1 | 1 | - | 100 | published, never ranked (may be uncrawled) |
| 199 | San Antonio | 3.32 | - | 4 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 200 | Chania | 3.30 | 47,379 | - | - | - | - | 20 | predicted (travel demand) |
| 201 | Fort Worth | 3.28 | - | 18 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 202 | Hilo | 3.27 | - | 6 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 203 | Santiago | 3.25 | 111,647 | - | - | - | - | 100 | predicted (travel demand) |
| 204 | Tulsa | 3.01 | - | 1 | - | - | 3 | 30 | published, never ranked (may be uncrawled) |
| 205 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 30 | predicted (travel demand) |
| 206 | Lucerne | 3.10 | 66,356 | - | - | - | - | 20 | predicted (travel demand) |
| 207 | Malmo | 3.07 | 103,940 | - | - | - | - | 30 | predicted (travel demand) |
| 208 | Lille | 3.06 | 73,435 | - | - | - | - | 20 | predicted (travel demand) |
| 209 | Cologne | 3.04 | 191,812 | 5 | - | 1 | - | 60 | published, never ranked (may be uncrawled) |
| 210 | Ljubljana | 2.98 | 125,046 | 4 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 211 | Corsica | 3.00 | - | - | - | - | - | 30 | predicted (travel demand) |
| 212 | Mechelen | 2.93 | 20,707 | - | - | - | - | 20 | predicted (travel demand) |
| 213 | Turin | 1.49 | 147,456 | 11 | 7 | 2 | 30 | 30 | published, never ranked (may be uncrawled) |
| 214 | Bilbao | 1.93 | 133,133 | 4 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 215 | Trieste | 1.43 | 117,233 | 36 | 1 | 3 | 43 | 20 | published, never ranked (may be uncrawled) |
| 216 | Helsinki | 2.25 | 148,908 | 12 | 2 | 1 | 13 | 30 | published, never ranked (may be uncrawled) |
| 217 | Poznan | 1.89 | 65,666 | 10 | - | 1 | 397 | 30 | published, never ranked (may be uncrawled) |
| 218 | Hong Kong | 1.85 | 689,212 | 10 | 4 | 1 | 505 | 100 | measured |
| 219 | Philadelphia | 2.67 | 405,294 | 4 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 220 | San Diego | 2.77 | 214,939 | 6 | 1 | 1 | - | 60 | published, never ranked (may be uncrawled) |
| 221 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 222 | Gdansk | 1.82 | 4,908 | 12 | 4 | 1 | 307 | 30 | published, never ranked (may be uncrawled) |
| 223 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 224 | Copenhagen | 2.62 | 218,621 | 49 | 41 | 6 | - | 30 | published, never ranked (may be uncrawled) |
| 225 | Hamburg | 2.57 | 191,221 | 6 | 3 | 1 | - | 60 | published, never ranked (may be uncrawled) |
| 226 | Corfu | 2.71 | 139,334 | - | - | - | - | 20 | predicted (travel demand) |
| 227 | Maastricht | 1.34 | 47,763 | 16 | - | 2 | 135 | 20 | published, never ranked (may be uncrawled) |
| 228 | Mexico City | 2.49 | 566,583 | 9 | 2 | - | - | 100 | published, never ranked (may be uncrawled) |
| 229 | Utrecht | 1.32 | 67,963 | 30 | 7 | 2 | 339 | 30 | published, never ranked (may be uncrawled) |
| 230 | Syracuse | 1.75 | 102,833 | - | - | - | - | 20 | predicted (travel demand) |
| 231 | Seoul | 2.41 | 206,265 | 8 | 5 | 1 | - | 100 | published, never ranked (may be uncrawled) |
| 232 | Cartagena | 2.58 | 65,066 | - | - | - | - | 30 | predicted (travel demand) |
| 233 | Gran Canaria | 1.67 | - | - | - | - | - | 30 | predicted (travel demand) |
| 234 | Padua | 1.36 | 54,592 | 12 | 4 | 1 | 12 | 20 | published, never ranked (may be uncrawled) |
| 235 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 20 | predicted (travel demand) |
| 236 | Bern | 2.51 | 90,627 | - | - | - | - | 20 | predicted (travel demand) |
| 237 | Nice | 2.46 | 136,877 | 10 | 6 | 2 | - | 30 | published, never ranked (may be uncrawled) |
| 238 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 239 | Faro | 1.62 | 55,645 | - | - | - | - | 20 | predicted (travel demand) |
| 240 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 241 | Dresden | 1.60 | 113,624 | 32 | 14 | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 242 | Brno | 1.58 | 63,714 | 8 | 5 | 2 | 34 | 30 | published, never ranked (may be uncrawled) |
| 243 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 244 | Palermo | 1.18 | 124,310 | 21 | 9 | 1 | 37 | 30 | published, never ranked (may be uncrawled) |
| 245 | Cusco | 2.35 | 87,732 | - | - | - | - | 30 | predicted (travel demand) |
| 246 | Limerick | 1.57 | 90,379 | - | - | - | - | 20 | predicted (travel demand) |
| 247 | Turku | 2.31 | - | 1 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 248 | Canberra | 2.28 | - | 1 | 1 | - | - | 30 | published, never ranked (may be uncrawled) |
| 249 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 20 | predicted (travel demand) |
| 250 | Pisa | 1.46 | 52,174 | 4 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 251 | Istanbul | 1.85 | 333,027 | 14 | 4 | 1 | - | 100 | measured |
| 252 | Nijmegen | 1.05 | 42,338 | 20 | 1 | 3 | 159 | 20 | published, never ranked (may be uncrawled) |
| 253 | Taipei | 2.09 | 143,193 | 4 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 254 | Salamanca | 1.37 | 47,897 | 4 | - | 1 | 1 | 20 | published, never ranked (may be uncrawled) |
| 255 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 256 | Tilburg | 1.03 | - | 17 | - | 3 | 86 | 20 | published, never ranked (may be uncrawled) |
| 257 | Ischia | 1.32 | - | - | - | - | 2 | 20 | predicted (travel demand) |
| 258 | Oslo | 1.76 | 181,113 | 4 | 1 | - | - | 30 | published, never ranked (may be uncrawled) |
| 259 | Izmir | 1.88 | 69,826 | - | - | - | - | 60 | predicted (travel demand) |
| 260 | Como | 0.96 | 82,645 | 9 | 2 | 1 | 23 | 20 | published, never ranked (may be uncrawled) |
| 261 | Wroclaw | 1.27 | 123,894 | 5 | 1 | 1 | 121 | 30 | published, never ranked (may be uncrawled) |
| 262 | Buenos Aires | 1.83 | 333,331 | 4 | 2 | - | - | 60 | published, never ranked (may be uncrawled) |
| 263 | Hilversum | 0.93 | - | 6 | 1 | 1 | 122 | 20 | published, never ranked (may be uncrawled) |
| 264 | Bucharest | 1.84 | 136,836 | 4 | - | 1 | - | 60 | published, never ranked (may be uncrawled) |
| 265 | Hobart | 1.23 | 81,734 | 11 | 1 | 2 | 455 | 20 | published, never ranked (may be uncrawled) |
| 266 | Austin | 1.82 | 226,631 | 10 | 3 | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 267 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 268 | Baltimore | 1.77 | - | 4 | - | - | - | 30 | published, never ranked (may be uncrawled) |
| 269 | Christchurch | 1.21 | 104,874 | 6 | - | 1 | 466 | 30 | published, never ranked (may be uncrawled) |
| 270 | Graz | 1.21 | 65,717 | 16 | 8 | 2 | 87 | 30 | published, never ranked (may be uncrawled) |
| 271 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 272 | Auckland | 1.17 | 152,056 | 5 | 2 | - | 977 | 60 | published, never ranked (may be uncrawled) |
| 273 | Sardinia | 0.97 | - | 5 | 4 | - | 8 | 60 | published, never ranked (may be uncrawled) |
| 274 | Dijon | 1.72 | 43,526 | - | - | - | - | 20 | predicted (travel demand) |
| 275 | Trier | 1.56 | 69,369 | - | - | - | - | 20 | predicted (travel demand) |
| 276 | Annecy | 1.69 | 56,859 | - | - | - | - | 20 | predicted (travel demand) |
| 277 | Geneva | 1.13 | 162,269 | 21 | 5 | 4 | 131 | 20 | published, never ranked (may be uncrawled) |
| 278 | York | 1.69 | 118,066 | 6 | 2 | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 279 | Zurich | 1.59 | 140,788 | 6 | 1 | - | - | 30 | published, never ranked (may be uncrawled) |
| 280 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 281 | Canterbury | 1.59 | 53,301 | - | - | - | - | 20 | predicted (travel demand) |
| 282 | Liverpool | 1.61 | 248,189 | 2 | 2 | - | - | 30 | published, never ranked (may be uncrawled) |
| 283 | Freiburg | 1.54 | 92,752 | 7 | 2 | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 284 | Rio de Janeiro | 1.59 | 279,431 | 6 | - | - | - | 100 | published, never ranked (may be uncrawled) |
| 285 | Mostar | 1.58 | 63,907 | - | - | - | - | 20 | predicted (travel demand) |
| 286 | Zadar | 1.53 | 71,549 | - | - | - | - | 20 | predicted (travel demand) |
| 287 | Bristol | 1.52 | 163,983 | 6 | 2 | - | - | 30 | published, never ranked (may be uncrawled) |
| 288 | Gothenburg | 1.49 | 119,991 | 5 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 289 | Cork | 0.97 | 101,405 | 13 | 2 | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 290 | Parma | 0.80 | 40,425 | 5 | - | 1 | 7 | 20 | published, never ranked (may be uncrawled) |
| 291 | Dordrecht | 0.71 | - | 17 | 1 | 2 | 105 | 20 | published, never ranked (may be uncrawled) |
| 292 | Thessaloniki | 1.42 | 180,145 | 4 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 293 | Bruges | 1.40 | 106,902 | 4 | - | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 294 | Cadiz | 0.90 | 79,226 | 5 | 4 | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 295 | Amersfoort | 0.67 | - | 18 | 1 | 2 | 181 | 20 | published, never ranked (may be uncrawled) |
| 296 | Cardiff | 1.27 | - | 4 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 297 | Sapporo | 0.88 | 88,633 | 6 | - | - | - | 60 | published, never ranked (may be uncrawled) |
| 298 | Antalya | 1.31 | 70,688 | - | - | - | - | 60 | predicted (travel demand) |
| 299 | Colmar | 1.28 | 45,517 | - | - | - | - | 20 | predicted (travel demand) |
| 300 | Antwerp | 1.26 | 128,289 | 10 | 4 | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 301 | Bodrum | 1.26 | 33,918 | - | - | - | - | 20 | predicted (travel demand) |
| 302 | Riga | 1.23 | 108,918 | 5 | 2 | - | - | 30 | published, never ranked (may be uncrawled) |
| 303 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 304 | Lausanne | 1.23 | 68,242 | 8 | 1 | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 305 | Oxford | 1.21 | 111,583 | 5 | 1 | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 306 | Evora | 0.78 | 15,345 | - | - | - | - | 20 | predicted (travel demand) |
| 307 | Genoa | 0.66 | 145,206 | 13 | 2 | 1 | 10 | 30 | published, never ranked (may be uncrawled) |
| 308 | Nagoya | 0.79 | 83,437 | 6 | 1 | - | 1 | 60 | published, never ranked (may be uncrawled) |
| 309 | Maui | 1.17 | - | 4 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 310 | Bergamo | 0.57 | 52,933 | 8 | 1 | 1 | 17 | 20 | published, never ranked (may be uncrawled) |
| 311 | Bordeaux | 0.76 | 156,201 | 10 | - | 2 | 211 | 30 | published, never ranked (may be uncrawled) |
| 312 | Braga | 0.62 | 34,522 | 4 | 2 | - | 8 | 20 | published, never ranked (may be uncrawled) |
| 313 | Menorca | 0.73 | - | 6 | - | - | 2 | 20 | published, never ranked (may be uncrawled) |
| 314 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 315 | Zaragoza | 0.73 | 87,580 | 7 | - | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 316 | Toulouse | 0.73 | 112,721 | 10 | - | 1 | 34 | 30 | published, never ranked (may be uncrawled) |
| 317 | Leiden | 0.54 | 33,227 | 17 | 6 | 1 | 129 | 20 | published, never ranked (may be uncrawled) |
| 318 | Okinawa | 0.71 | 24,466 | 6 | - | - | 1 | 30 | published, never ranked (may be uncrawled) |
| 319 | Apeldoorn | 0.53 | - | 8 | - | 2 | 80 | 20 | published, never ranked (may be uncrawled) |
| 320 | La Palma | 0.70 | - | - | - | - | - | 20 | predicted (travel demand) |
| 321 | Dubrovnik | 0.99 | 119,586 | 4 | 1 | - | 2 | 10 | published, never ranked (may be uncrawled) |
| 322 | Belfast | 1.04 | 224,315 | 5 | 1 | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 323 | Salzburg | 0.68 | 107,243 | 21 | 8 | 3 | 33 | 20 | published, never ranked (may be uncrawled) |
| 324 | Haarlem | 0.50 | 33,960 | 21 | 1 | 2 | 277 | 20 | published, never ranked (may be uncrawled) |
| 325 | Catania | 0.57 | 58,252 | 4 | 3 | 1 | 5 | 30 | published, never ranked (may be uncrawled) |
| 326 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 60 | predicted (travel demand) |
| 327 | Split | 0.97 | 132,399 | 4 | - | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 328 | Nantes | 0.96 | 67,689 | 1 | 1 | - | - | 30 | published, never ranked (may be uncrawled) |
| 329 | Venlo | 0.48 | - | 7 | - | 1 | 144 | 20 | published, never ranked (may be uncrawled) |
| 330 | Rothenburg ob der Tauber | 0.77 | 39,879 | 4 | - | 1 | 8 | 10 | published, never ranked (may be uncrawled) |
| 331 | Luxembourg City | 0.60 | 64,851 | 10 | 5 | 2 | 18 | 20 | published, never ranked (may be uncrawled) |
| 332 | Crete | 0.86 | - | 4 | 3 | - | - | 30 | published, never ranked (may be uncrawled) |
| 333 | Segovia | 0.54 | 30,968 | 6 | - | 1 | 5 | 20 | published, never ranked (may be uncrawled) |
| 334 | Brighton | 0.85 | 114,108 | 6 | 1 | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 335 | Busan | 0.83 | 94,737 | 2 | - | - | - | 60 | published, never ranked (may be uncrawled) |
| 336 | Belgrade | 0.83 | 178,116 | 5 | 5 | - | - | 60 | published, never ranked (may be uncrawled) |
| 337 | Potsdam | 0.51 | 51,727 | 9 | - | 1 | 21 | 20 | published, never ranked (may be uncrawled) |
| 338 | Enschede | 0.38 | - | 13 | 1 | 1 | 82 | 20 | published, never ranked (may be uncrawled) |
| 339 | Trento | 0.38 | 56,455 | 10 | 1 | 1 | 20 | 20 | published, never ranked (may be uncrawled) |
| 340 | Heidelberg | 0.67 | 75,837 | 6 | 1 | 1 | - | 20 | published, never ranked (may be uncrawled) |
| 341 | Ibiza | 0.46 | - | 1 | - | - | 4 | 20 | published, never ranked (may be uncrawled) |
| 342 | Modena | 0.44 | 51,698 | 5 | 1 | 1 | 3 | 20 | published, never ranked (may be uncrawled) |
| 343 | Den Bosch | 0.36 | 39,682 | 11 | 2 | 1 | 118 | 20 | published, never ranked (may be uncrawled) |
| 344 | Ronda | 0.42 | 51,510 | 6 | 1 | - | 9 | 10 | published, never ranked (may be uncrawled) |
| 345 | Assen | 0.35 | - | 10 | - | 2 | 66 | 20 | published, never ranked (may be uncrawled) |
| 346 | Heerlen | 0.35 | - | 8 | 1 | 2 | 53 | 20 | published, never ranked (may be uncrawled) |
| 347 | Kamakura | 0.44 | 33,492 | 6 | - | - | - | 20 | published, never ranked (may be uncrawled) |
| 348 | Zwolle | 0.35 | - | 15 | - | 3 | 58 | 20 | published, never ranked (may be uncrawled) |
| 349 | Coimbra | 0.36 | 34,962 | 5 | - | - | 5 | 20 | published, never ranked (may be uncrawled) |
| 350 | Cordoba | 0.41 | 74,675 | 16 | 2 | 2 | 3 | 30 | published, never ranked (may be uncrawled) |
| 351 | Deventer | 0.31 | - | 12 | - | 1 | 213 | 20 | published, never ranked (may be uncrawled) |
| 352 | Ghent | 0.59 | 82,757 | 8 | 1 | 1 | - | 30 | published, never ranked (may be uncrawled) |
| 353 | Hoorn | 0.30 | - | 12 | - | 2 | 52 | 20 | published, never ranked (may be uncrawled) |
| 354 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 100 | published, never ranked (may be uncrawled) |
| 355 | Tarragona | 0.36 | 32,396 | 4 | 2 | - | - | 20 | published, never ranked (may be uncrawled) |
| 356 | Helmond | 0.29 | - | 19 | - | 2 | 54 | 20 | published, never ranked (may be uncrawled) |
| 357 | Hallstatt | 0.50 | 47,271 | 5 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 358 | Pamplona | 0.34 | 128,065 | 14 | - | 1 | 9 | 20 | published, never ranked (may be uncrawled) |
| 359 | Perugia | 0.29 | 42,572 | 12 | - | 2 | 19 | 20 | published, never ranked (may be uncrawled) |
| 360 | Phoenix | 0.55 | - | - | - | - | - | 60 | predicted (travel demand) |
| 361 | Cesky Krumlov | 0.34 | 28,582 | 6 | 3 | - | 11 | 10 | published, never ranked (may be uncrawled) |
| 362 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 363 | Matera | 0.25 | 67,033 | 4 | - | - | 2 | 20 | published, never ranked (may be uncrawled) |
| 364 | Ferrara | 0.21 | 27,490 | 5 | 3 | 1 | 7 | 20 | published, never ranked (may be uncrawled) |
| 365 | Toledo | 0.24 | 3,149 | - | - | - | - | 20 | predicted (travel demand) |
| 366 | Setubal | 0.19 | 22,582 | 10 | 1 | 2 | 13 | 20 | published, never ranked (may be uncrawled) |
| 367 | Regensburg | 0.30 | 51,930 | 5 | 1 | 1 | 4 | 20 | published, never ranked (may be uncrawled) |
| 368 | Caserta | 0.16 | 14,783 | 20 | - | 1 | 51 | 20 | published, never ranked (may be uncrawled) |
| 369 | Bamberg | 0.24 | 28,716 | 6 | 4 | 1 | 11 | 20 | published, never ranked (may be uncrawled) |
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

