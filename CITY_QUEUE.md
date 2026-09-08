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

2. **Then deepen, to these targets.** The 50 tier lasted about an hour and he
   killed it: "we willen helemaal geen 50 bomen in bath mss max 20. kunnen we
   vanaf nu gewoon voor 30 grote bomen streven bij grote stad en bevestigd."

   | state | target |
   |---|---:|
   | new city or village, not confirmed by Search Console | 10 |
   | confirmed city | 20 |
   | confirmed BIG city (8,000+ travel demand) | 30 |

   Thirty remarkable trees is already a lot of city. A page that needs fifty is
   a page padded past the point where every entry deserves its spot, and
   exclusivity is the product. Bath is the worked example: it ranks well, which
   is why an impressions-only rule briefly handed it 50, but it is a small city
   and stops at 20.

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
| 1 | Rome | 156.75 | 358,876 | 30 | 9 | 2 | 32 | 30 | measured |
| 2 | Lisbon | 84.05 | 201,877 | 35 | 11 | 3 | 68 | 30 | measured |
| 3 | Milan | 79.46 | 212,705 | 22 | 9 | 2 | 25 | 30 | measured |
| 4 | Barcelona | 75.36 | 346,477 | 56 | 12 | 7 | 180 | 30 | measured |
| 5 | Brussels | 98.54 | 176,863 | 31 | 4 | 1 | 436 | 30 | measured |
| 6 | Amsterdam | 68.59 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 7 | Singapore | 48.79 | 967,821 | 28 | 3 | 3 | 165 | 30 | measured |
| 8 | Seville | 46.13 | 170,545 | 43 | 6 | 2 | - | 20 | measured |
| 9 | Leiden | 34.78 | 33,227 | 20 | 4 | 1 | 129 | 20 | measured |
| 10 | London | 56.03 | 718,291 | 23 | 10 | 1 | - | 30 | measured |
| 11 | Florence | 31.64 | 184,099 | 23 | 8 | 1 | 27 | 30 | measured |
| 12 | Brisbane | 41.06 | 162,602 | 20 | 1 | 2 | 186 | 30 | measured |
| 13 | Arnhem | 28.74 | 31,478 | 38 | 1 | 3 | 200 | 20 | measured |
| 14 | Prague | 37.68 | 303,350 | 21 | 13 | 3 | 29 | 30 | measured |
| 15 | Vienna | 31.64 | 283,090 | 32 | 13 | 5 | 376 | 30 | measured |
| 16 | Madeira | 28.50 | - | 10 | 1 | 1 | - | 20 | measured |
| 17 | Berlin | 31.16 | 412,181 | 20 | 11 | 1 | 195 | 30 | measured |
| 18 | Palermo | 22.46 | 124,310 | 21 | 7 | 1 | 37 | 20 | measured |
| 19 | Paris | 29.95 | 524,268 | 31 | 9 | 4 | 129 | 30 | measured |
| 20 | Tenerife | 29.47 | - | 4 | 1 | - | - | 20 | measured |
| 21 | Alicante | 22.22 | 77,454 | 16 | 3 | 2 | 44 | 20 | measured |
| 22 | Oahu | 27.53 | - | 11 | 1 | - | 160 | 20 | measured |
| 23 | New York | 35.75 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 24 | Portland | 27.05 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 25 | Valencia | 20.05 | 162,209 | 25 | 2 | 2 | 350 | 30 | measured |
| 26 | Birmingham | 37.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 27 | Sardinia | 19.32 | - | 5 | 2 | - | 8 | 20 | measured |
| 28 | Kyoto | 21.01 | 142,353 | 17 | 8 | 2 | - | 20 | measured |
| 29 | Sintra | 16.18 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 30 | Hilo | 24.15 | - | 6 | - | 1 | 16 | 20 | measured |
| 31 | Los Angeles | 29.95 | 665,559 | 8 | 2 | - | - | 30 | measured |
| 32 | The Hague | 15.46 | 236,723 | 31 | 1 | 5 | 167 | 20 | measured |
| 33 | Fukuoka | 20.05 | 77,485 | 15 | 7 | 1 | - | 20 | measured |
| 34 | Krakow | 20.29 | 140,824 | 34 | 3 | 3 | 198 | 30 | measured |
| 35 | Dublin | 17.39 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 36 | Nijmegen | 14.97 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 37 | Boston | 26.57 | 385,902 | 11 | 1 | 1 | - | 30 | measured |
| 38 | Austin | 26.57 | 226,631 | 5 | - | - | - | 20 | measured |
| 39 | Haarlem | 12.56 | 33,960 | 21 | - | 2 | 277 | 20 | measured |
| 40 | Copenhagen | 23.19 | 218,621 | 16 | 1 | 2 | - | 30 | measured |
| 41 | Seattle | 23.19 | 398,724 | 6 | - | - | - | 30 | measured |
| 42 | Munich | 15.46 | 224,067 | 45 | 14 | 6 | 80 | 30 | measured |
| 43 | Jacksonville | 22.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 44 | Porto | 11.35 | 120,415 | 27 | 14 | 2 | 40 | 20 | measured |
| 45 | Utrecht | 11.35 | 67,963 | 33 | 4 | 2 | 345 | 20 | measured |
| 46 | Malaga | 14.97 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 47 | Palma de Mallorca | 13.53 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 48 | Geneva | 14.73 | 162,269 | 21 | 4 | 4 | 131 | 20 | measured |
| 49 | Naples | 10.87 | 198,913 | 24 | 3 | 3 | 46 | 20 | measured |
| 50 | Cordoba | 13.53 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 51 | Asheville | 20.89 | - | - | - | - | - | 10 | predicted (travel demand) |
| 52 | Boise | 20.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 53 | Long Beach | 20.48 | - | - | - | - | - | 10 | predicted (travel demand) |
| 54 | Little Rock | 20.40 | - | - | - | - | - | 10 | predicted (travel demand) |
| 55 | Dordrecht | 10.14 | - | 13 | - | 2 | 105 | 20 | measured |
| 56 | Athens | 19.80 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 57 | Bologna | 10.39 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 58 | Reykjavik | 16.42 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 59 | Indianapolis | 18.28 | - | - | - | - | - | 10 | predicted (travel demand) |
| 60 | Venice | 10.39 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 61 | Vilnius | 12.56 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 62 | Oakland | 18.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 63 | Fort Lauderdale | 18.43 | - | - | - | - | - | 10 | predicted (travel demand) |
| 64 | Edinburgh | 18.36 | 292,981 | 16 | 4 | 1 | - | 30 | measured |
| 65 | Budapest | 17.63 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 66 | Lexington | 18.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 67 | Reno | 18.19 | - | - | - | - | - | 10 | predicted (travel demand) |
| 68 | Des Moines | 18.11 | - | - | - | - | - | 10 | predicted (travel demand) |
| 69 | Perth | 17.63 | 180,478 | 6 | 1 | 1 | - | 30 | measured |
| 70 | Cagliari | 9.66 | 51,351 | 10 | 1 | 2 | 15 | 20 | measured |
| 71 | Chicago | 17.87 | 485,769 | 6 | - | - | - | 30 | measured |
| 72 | Las Vegas | 17.87 | - | 11 | - | 2 | - | 30 | measured |
| 73 | Cadiz | 11.35 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 74 | Daytona Beach | 17.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 75 | Houston | 17.39 | - | 4 | - | - | - | 30 | measured |
| 76 | Oslo | 15.22 | 181,113 | 4 | - | - | - | 20 | measured |
| 77 | Melbourne | 11.35 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 78 | Tokyo | 8.94 | 394,702 | 17 | 8 | 1 | 6 | 20 | measured |
| 79 | Chattanooga | 16.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 80 | Crete | 16.42 | - | 4 | 2 | - | - | 20 | measured |
| 81 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 82 | Spokane | 15.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 83 | Strasbourg | 10.63 | 154,700 | 10 | 1 | 2 | 66 | 30 | measured |
| 84 | New Orleans | 15.94 | 256,232 | 4 | 2 | 1 | - | 20 | measured |
| 85 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 86 | Pittsburgh | 15.18 | - | - | - | - | - | 10 | predicted (travel demand) |
| 87 | Sorrento | 7.73 | 40,049 | 6 | - | 1 | 20 | 20 | measured |
| 88 | Huntsville | 15.35 | - | - | - | - | - | 10 | predicted (travel demand) |
| 89 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 90 | West Palm Beach | 14.98 | - | - | - | - | - | 10 | predicted (travel demand) |
| 91 | Monterey | 14.58 | - | - | - | - | - | 10 | predicted (travel demand) |
| 92 | Saint Petersburg | 14.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 93 | St. Louis | 14.80 | - | - | - | - | - | 10 | predicted (travel demand) |
| 94 | San Francisco | 14.49 | 361,111 | 6 | - | 1 | - | 30 | measured |
| 95 | Tampa | 14.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 96 | Hawaii | 12.56 | - | 6 | - | 1 | 6 | 30 | measured |
| 97 | Leeuwarden | 7.00 | - | 9 | - | 1 | 60 | 20 | measured |
| 98 | Toronto | 13.53 | 411,011 | 6 | - | - | - | 30 | measured |
| 99 | Cyprus | 13.28 | - | 4 | - | - | - | 20 | measured |
| 100 | Granada | 8.45 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 101 | Cincinnati | 13.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 102 | Bath | 13.28 | 144,950 | 5 | 1 | 1 | - | 20 | measured |
| 103 | Lansing | 13.02 | - | - | - | - | - | 10 | predicted (travel demand) |
| 104 | Helmond | 6.28 | - | 13 | - | 1 | 55 | 20 | measured |
| 105 | Montreal | 12.56 | 315,322 | 7 | - | 1 | - | 30 | measured |
| 106 | Detroit | 12.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 107 | Tulsa | 12.03 | - | - | - | - | - | 10 | predicted (travel demand) |
| 108 | Dallas | 12.08 | - | 8 | 1 | 1 | - | 30 | measured |
| 109 | Trento | 6.04 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 110 | Bordeaux | 7.97 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 111 | Istanbul | 10.26 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 112 | Denver | 11.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 113 | Cork | 7.73 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 114 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 115 | San Jose | 11.39 | - | - | - | - | - | 10 | predicted (travel demand) |
| 116 | Sacramento | 11.32 | - | - | - | - | - | 10 | predicted (travel demand) |
| 117 | Jersey City | 10.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 118 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 119 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 120 | Luxembourg City | 7.25 | 64,851 | 10 | 2 | 2 | 18 | 20 | measured |
| 121 | Milwaukee | 10.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 122 | Salt Lake City | 10.31 | - | - | - | - | - | 10 | predicted (travel demand) |
| 123 | Atlanta | 10.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 124 | Anchorage | 10.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 125 | Osaka | 6.52 | 163,112 | 6 | 1 | - | - | 30 | measured |
| 126 | Washington DC | 9.18 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 127 | Raleigh | 10.07 | - | - | - | - | - | 10 | predicted (travel demand) |
| 128 | Philadelphia | 9.66 | 405,294 | 1 | - | - | - | 20 | measured |
| 129 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 130 | Seoul | 9.18 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 131 | Ottawa | 6.52 | - | 8 | - | 1 | 119 | 20 | measured |
| 132 | Cleveland | 9.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 133 | El Paso | 9.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 134 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 135 | Miami | 9.48 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 136 | Girona | 5.56 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 137 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 138 | Kamakura | 5.80 | 33,492 | 6 | - | - | - | 20 | measured |
| 139 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 140 | Groningen | 4.59 | 31,401 | 20 | 1 | 2 | 72 | 20 | measured |
| 141 | Quebec City | 6.04 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 142 | Warsaw | 6.04 | 197,929 | 19 | 3 | 2 | 1446 | 30 | measured |
| 143 | Pisa | 5.85 | 52,174 | - | - | - | - | 10 | predicted (travel demand) |
| 144 | Nashville | 8.93 | - | - | - | - | - | 10 | predicted (travel demand) |
| 145 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 146 | Glasgow | 8.21 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 147 | Leipzig | 5.80 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 148 | Maastricht | 4.35 | 47,763 | 15 | - | 1 | 135 | 20 | measured |
| 149 | Salzburg | 5.80 | 107,243 | 9 | - | 2 | 34 | 20 | measured |
| 150 | Tallinn | 5.80 | 124,888 | 4 | 2 | 1 | 42 | 20 | measured |
| 151 | Parma | 4.83 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 152 | Pamplona | 5.56 | 128,065 | 6 | - | - | 1 | 20 | measured |
| 153 | Ann Arbor | 8.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 154 | Kauai | 7.25 | - | 6 | 1 | - | 8 | 20 | measured |
| 155 | Salamanca | 5.50 | 47,897 | - | - | - | 1 | 10 | predicted (travel demand) |
| 156 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 157 | Caserta | 4.11 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 158 | Eindhoven | 4.11 | - | 11 | - | 2 | 195 | 20 | measured |
| 159 | Tilburg | 4.11 | - | 16 | - | 2 | 84 | 20 | measured |
| 160 | Sydney | 7.97 | 305,304 | 7 | - | - | - | 30 | measured |
| 161 | Bari | 4.83 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 162 | Lyon | 5.31 | 136,951 | 13 | 3 | 1 | 156 | 20 | measured |
| 163 | Albuquerque | 7.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 164 | Venlo | 3.86 | - | 7 | - | 1 | 144 | 20 | measured |
| 165 | Minneapolis | 7.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 166 | Riga | 7.49 | 108,918 | 5 | - | - | - | 20 | measured |
| 167 | Hobart | 5.07 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 168 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 169 | Nice | 7.49 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 170 | Madrid | 4.59 | 274,553 | 17 | 10 | 2 | - | 20 | measured |
| 171 | Dubrovnik | 7.00 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 172 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 173 | Sapporo | 4.83 | 88,633 | 6 | - | - | - | 20 | measured |
| 174 | Baltimore | 7.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 175 | Como | 3.62 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 176 | Turin | 3.62 | 147,456 | 11 | 7 | 2 | 30 | 20 | measured |
| 177 | Coimbra | 3.86 | 34,962 | 4 | - | - | 5 | 20 | measured |
| 178 | Braga | 3.86 | 34,522 | 4 | 1 | - | 8 | 20 | measured |
| 179 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 180 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 181 | Graz | 4.59 | 65,717 | 12 | 3 | 1 | 87 | 20 | measured |
| 182 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 183 | Catania | 3.86 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 184 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 185 | Nuremberg | 4.35 | 161,614 | 12 | 1 | 1 | 38 | 20 | measured |
| 186 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 187 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 188 | Enschede | 3.14 | - | 7 | 1 | 1 | 82 | 20 | measured |
| 189 | Hoorn | 3.14 | - | 8 | - | 1 | 52 | 20 | measured |
| 190 | Zwolle | 3.14 | - | 7 | - | 1 | 57 | 20 | measured |
| 191 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 192 | Vancouver | 6.04 | 351,552 | 4 | - | - | - | 30 | measured |
| 193 | Menorca | 3.86 | - | 6 | - | - | 2 | 20 | measured |
| 194 | Bergamo | 2.90 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 195 | Rotterdam | 2.90 | 104,938 | 12 | - | 2 | 83 | 20 | measured |
| 196 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 197 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 198 | Oxford | 5.56 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 199 | Guimaraes | 2.90 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 200 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 201 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 202 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 203 | Segovia | 3.38 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 204 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 205 | Trieste | 2.66 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 206 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 207 | Hong Kong | 3.50 | 689,212 | 10 | 2 | 1 | 505 | 20 | measured |
| 208 | Cardiff | 5.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 209 | Ljubljana | 5.07 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 210 | Santa Fe | 5.17 | - | - | - | - | - | 10 | predicted (travel demand) |
| 211 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 212 | Mexico City | 4.83 | 566,583 | 9 | 1 | - | - | 30 | measured |
| 213 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 214 | Bratislava | 3.38 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 215 | Lausanne | 4.90 | 68,242 | - | - | - | - | 10 | predicted (travel demand) |
| 216 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 217 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 218 | Stuttgart | 4.11 | 112,789 | 7 | - | - | - | 20 | measured |
| 219 | Amersfoort | 2.42 | - | 8 | 1 | 1 | 181 | 20 | measured |
| 220 | Heerlen | 2.42 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 221 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 222 | Brno | 3.14 | 63,714 | 8 | 2 | 2 | 34 | 20 | measured |
| 223 | Hiroshima | 3.14 | 129,791 | 17 | 1 | 3 | - | 20 | measured |
| 224 | Potsdam | 3.14 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 225 | Maui | 4.35 | - | 4 | - | - | 3 | 20 | measured |
| 226 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 227 | Bristol | 4.59 | 163,983 | 6 | 1 | - | - | 20 | measured |
| 228 | Helsinki | 3.62 | 148,908 | 10 | 1 | - | 12 | 30 | measured |
| 229 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 230 | Stockholm | 3.38 | 188,184 | 5 | 3 | - | - | 30 | measured |
| 231 | Savannah | 4.35 | 128,162 | 2 | - | - | - | 20 | measured |
| 232 | Toulouse | 2.90 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 233 | Alkmaar | 2.17 | - | 7 | - | 1 | 79 | 20 | measured |
| 234 | Den Bosch | 2.17 | 39,682 | 12 | 1 | 1 | 118 | 20 | measured |
| 235 | Hilversum | 2.17 | - | 6 | - | 1 | 122 | 20 | measured |
| 236 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 237 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 238 | Aarhus | 4.11 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 239 | Verona | 2.42 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 240 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 241 | Perugia | 2.17 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 242 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 243 | Zurich | 3.86 | 140,788 | 6 | - | - | - | 20 | measured |
| 244 | Bilbao | 2.66 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 245 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 246 | Cambridge | 3.86 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 247 | Delft | 1.93 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 248 | Deventer | 1.93 | - | 10 | - | 1 | 213 | 20 | measured |
| 249 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 250 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 251 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 252 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 253 | Tarragona | 2.17 | 32,396 | 4 | - | - | - | 20 | measured |
| 254 | Frankfurt | 2.42 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 255 | Genoa | 1.93 | 145,206 | 12 | 1 | 1 | 11 | 20 | measured |
| 256 | Padua | 1.93 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 257 | Poznan | 2.42 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 258 | Manchester | 3.62 | 316,438 | 5 | - | - | - | 30 | measured |
| 259 | Modena | 2.17 | 51,698 | 5 | 1 | 1 | 3 | 20 | measured |
| 260 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 261 | Charleston | 3.38 | 155,987 | 2 | 1 | - | - | 20 | measured |
| 262 | Busan | 3.31 | 94,737 | - | - | - | - | 10 | predicted (travel demand) |
| 263 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 264 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 265 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 266 | Assen | 1.69 | - | 9 | - | 2 | 67 | 20 | measured |
| 267 | Cologne | 3.38 | 191,812 | 5 | - | 1 | - | 30 | measured |
| 268 | Lucca | 1.69 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 269 | San Diego | 3.38 | 214,939 | 4 | - | 1 | - | 20 | measured |
| 270 | Kanazawa | 2.17 | 25,778 | 7 | 1 | 1 | 2 | 20 | measured |
| 271 | San Antonio | 3.32 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 272 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 273 | Nagoya | 2.17 | 83,437 | 6 | 1 | - | 1 | 20 | measured |
| 274 | Naha | 2.17 | 24,466 | 6 | - | - | 1 | 20 | measured |
| 275 | Fort Worth | 3.28 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 276 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 277 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 278 | Sao Paulo | 2.96 | 911 | - | - | - | - | 10 | predicted (travel demand) |
| 279 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 280 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 281 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 282 | Buenos Aires | 2.90 | 333,331 | 4 | 1 | - | - | 30 | measured |
| 283 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 284 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 285 | Auckland | 2.90 | 152,056 | 5 | 1 | - | - | 20 | measured |
| 286 | Apeldoorn | 1.45 | - | 10 | - | 2 | 80 | 20 | measured |
| 287 | Belfast | 2.90 | 224,315 | 4 | - | 1 | - | 20 | measured |
| 288 | Bruges | 2.90 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 289 | Kansas City | 2.90 | - | 4 | - | 1 | - | 30 | measured |
| 290 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 291 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 292 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 293 | Beijing | 2.66 | 269,737 | 7 | 1 | - | - | 30 | measured |
| 294 | Rio de Janeiro | 2.66 | 279,431 | 6 | - | - | - | 30 | measured |
| 295 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 296 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 297 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 298 | Hamburg | 2.42 | 191,221 | 6 | 1 | 1 | - | 30 | measured |
| 299 | Cesky Krumlov | 1.69 | 28,582 | 6 | 2 | - | 11 | 20 | measured |
| 300 | Gdansk | 1.69 | 4,908 | 6 | 4 | - | 288 | 20 | measured |
| 301 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 302 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 303 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 304 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 305 | Bangkok | 2.42 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 306 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 307 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 308 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 309 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 310 | Ghent | 2.17 | 82,757 | 6 | 1 | 1 | - | 20 | measured |
| 311 | Hallstatt | 1.99 | 47,271 | - | - | - | - | 10 | predicted (travel demand) |
| 312 | Canberra | 2.28 | - | 1 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 313 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 314 | Setubal | 1.21 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 315 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 316 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 317 | Matera | 1.21 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 318 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 319 | Liverpool | 1.93 | 248,189 | 2 | - | - | - | 20 | measured |
| 320 | Thessaloniki | 1.93 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 321 | Ibiza | 1.21 | - | 1 | - | - | 4 | 20 | measured |
| 322 | Bucharest | 1.84 | 136,836 | 4 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 323 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 324 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 325 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 326 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 327 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 328 | Taipei | 1.69 | 143,193 | 4 | - | - | - | 30 | measured |
| 329 | Ronda | 0.97 | 51,510 | 6 | - | - | 9 | 20 | measured |
| 330 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 331 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 332 | Heidelberg | 1.45 | 75,837 | 6 | 1 | 1 | - | 20 | measured |
| 333 | Rouen | 1.45 | 72,334 | 12 | - | 1 | 6 | 20 | measured |
| 334 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 335 | Assisi | 0.97 | 30,278 | 6 | 1 | 2 | 6 | 20 | measured |
| 336 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 337 | Dresden | 0.97 | 113,624 | 5 | 1 | 1 | - | 20 | measured |
| 338 | Sofia | 0.97 | 138,710 | 4 | - | - | - | 30 | measured |
| 339 | Wroclaw | 0.97 | 123,894 | 5 | 1 | 1 | 121 | 20 | measured |
| 340 | Belgrade | 1.45 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 341 | Gothenburg | 1.45 | 119,991 | 5 | - | 1 | - | 20 | measured |
| 342 | Rothenburg ob der Tauber | 1.21 | 39,879 | 4 | - | 1 | 8 | 20 | measured |
| 343 | Roosendaal | 0.72 | - | 8 | - | 1 | 116 | 20 | measured |
| 344 | Regensburg | 1.21 | 51,930 | 5 | - | 1 | 4 | 20 | measured |
| 345 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 346 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 347 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 348 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 349 | Antwerp | 1.21 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 350 | Brighton | 1.21 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 351 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 352 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 353 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 354 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 355 | Split | 0.97 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 356 | York | 0.97 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 357 | Nantes | 0.96 | 67,689 | 1 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 358 | Zaragoza | 0.48 | 87,580 | 7 | - | 1 | - | 20 | measured |
| 359 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 360 | Bamberg | 0.48 | 28,716 | 5 | 3 | 1 | 10 | 20 | measured |
| 361 | Phoenix | 0.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 362 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 363 | Breda | 0.24 | 36,579 | 4 | - | 1 | 119 | 20 | measured |
| 364 | Leuven | 0.48 | 40,645 | 4 | - | - | - | 20 | measured |
| 365 | Ferrara | 0.24 | 27,490 | 5 | 1 | 1 | 7 | 20 | measured |
| 366 | Yakushima | 0.24 | - | 1 | - | - | 1 | 20 | measured |
| 367 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 368 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 369 | George Town | 0.28 | 36,080 | - | - | - | - | 10 | predicted (travel demand) |
| 370 | Freiburg | 0.24 | 92,752 | 7 | 1 | 1 | - | 20 | measured |
| 371 | Allentown | 0.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 372 | Turku | 0.24 | - | 1 | - | - | - | 30 | measured |
| 373 | Oss | 0.11 | - | 6 | - | - | 48 | 10 | published, never ranked (may be uncrawled) |
| 374 | Queenstown | 0.16 | 36,672 | - | - | - | - | 10 | predicted (travel demand) |
| 375 | Buffalo | 0.15 | - | - | - | - | - | 10 | predicted (travel demand) |
| 376 | San Juan | 0.15 | - | - | - | - | - | 10 | predicted (travel demand) |
| 377 | Halifax | 0.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 378 | Memphis | 0.08 | - | - | - | - | - | 10 | predicted (travel demand) |

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

