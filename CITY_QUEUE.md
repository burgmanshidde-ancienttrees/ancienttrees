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
| 1 | Brussels | 178.01 | 176,863 | 31 | 4 | 1 | 436 | 30 | measured |
| 2 | Milan | 103.01 | 212,705 | 25 | 11 | 3 | 25 | 30 | measured |
| 3 | Rome | 100.33 | 358,876 | 31 | 10 | 2 | 32 | 30 | measured |
| 4 | Lisbon | 90.83 | 201,877 | 35 | 16 | 3 | 68 | 30 | measured |
| 5 | Barcelona | 83.04 | 346,477 | 56 | 13 | 7 | 180 | 30 | measured |
| 6 | Amsterdam | 67.45 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 7 | Arnhem | 46.02 | 31,478 | 39 | 3 | 3 | 204 | 20 | measured |
| 8 | Singapore | 56.25 | 967,821 | 34 | 4 | 3 | 165 | 30 | measured |
| 9 | Florence | 41.40 | 184,099 | 26 | 9 | 1 | 27 | 30 | measured |
| 10 | Seville | 54.06 | 170,545 | 43 | 9 | 2 | - | 20 | measured |
| 11 | Tenerife | 53.33 | - | 4 | 2 | - | - | 20 | measured |
| 12 | Oahu | 53.09 | - | 21 | 2 | 3 | 163 | 20 | measured |
| 13 | Los Angeles | 67.21 | 665,559 | 8 | 2 | - | - | 30 | measured |
| 14 | Palermo | 34.34 | 124,310 | 21 | 9 | 1 | 37 | 20 | measured |
| 15 | Brisbane | 44.56 | 162,602 | 20 | 2 | 2 | 186 | 30 | measured |
| 16 | Berlin | 42.86 | 412,181 | 23 | 14 | 2 | 195 | 30 | measured |
| 17 | London | 54.06 | 718,291 | 23 | 12 | 1 | - | 30 | measured |
| 18 | Paris | 40.18 | 524,268 | 31 | 9 | 4 | 129 | 30 | measured |
| 19 | Vienna | 38.48 | 283,090 | 32 | 14 | 5 | 376 | 30 | measured |
| 20 | Valencia | 28.73 | 162,209 | 31 | 3 | 2 | 350 | 30 | measured |
| 21 | Prague | 37.26 | 303,350 | 30 | 19 | 4 | 31 | 30 | measured |
| 22 | Alicante | 23.62 | 77,454 | 21 | 4 | 2 | 44 | 20 | measured |
| 23 | Leiden | 23.13 | 33,227 | 20 | 6 | 1 | 129 | 20 | measured |
| 24 | Madeira | 24.35 | - | 10 | 1 | 1 | - | 20 | measured |
| 25 | Dublin | 22.40 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 26 | Birmingham | 37.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 27 | Portland | 23.86 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 28 | Kyoto | 22.89 | 142,353 | 18 | 12 | 2 | - | 20 | measured |
| 29 | Haarlem | 17.78 | 33,960 | 21 | - | 2 | 277 | 20 | measured |
| 30 | Krakow | 23.62 | 140,824 | 34 | 7 | 3 | 198 | 30 | measured |
| 31 | Copenhagen | 33.36 | 218,621 | 16 | 2 | 2 | - | 30 | measured |
| 32 | The Hague | 17.53 | 236,723 | 31 | 2 | 5 | 167 | 20 | measured |
| 33 | Nijmegen | 17.29 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 34 | Boston | 33.12 | 385,902 | 11 | 2 | 1 | - | 30 | measured |
| 35 | New York | 30.20 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 36 | Malaga | 22.89 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 37 | Munich | 20.94 | 224,067 | 45 | 15 | 6 | 80 | 30 | measured |
| 38 | Helmond | 15.58 | - | 18 | - | 2 | 55 | 20 | measured |
| 39 | Vilnius | 20.46 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 40 | Sintra | 15.34 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 41 | Austin | 30.20 | 226,631 | 5 | 2 | - | - | 20 | measured |
| 42 | Tokyo | 16.07 | 394,702 | 21 | 8 | 1 | 5 | 20 | measured |
| 43 | New Orleans | 28.73 | 256,232 | 4 | 2 | 1 | - | 20 | measured |
| 44 | Reykjavik | 24.59 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 45 | Dordrecht | 13.88 | - | 20 | 1 | 2 | 105 | 20 | measured |
| 46 | Houston | 26.79 | - | 4 | - | - | - | 30 | measured |
| 47 | Palma de Mallorca | 16.07 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 48 | Geneva | 17.53 | 162,269 | 21 | 5 | 4 | 131 | 20 | measured |
| 49 | Dallas | 25.81 | - | 9 | 1 | 1 | - | 30 | measured |
| 50 | Oslo | 21.92 | 181,113 | 4 | - | - | - | 20 | measured |
| 51 | Cork | 16.56 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 52 | Fukuoka | 15.83 | 77,485 | 15 | 9 | 1 | - | 20 | measured |
| 53 | Bath | 24.35 | 144,950 | 5 | 2 | 1 | - | 20 | measured |
| 54 | Porto | 11.93 | 120,415 | 27 | 15 | 2 | 40 | 20 | measured |
| 55 | Ottawa | 15.83 | - | 19 | - | 3 | 122 | 20 | measured |
| 56 | Las Vegas | 23.38 | - | 11 | - | 2 | - | 30 | measured |
| 57 | Jacksonville | 22.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 58 | Granada | 13.88 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 59 | San Francisco | 21.43 | 361,111 | 6 | 1 | 1 | - | 30 | measured |
| 60 | Cordoba | 13.88 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 61 | Leeuwarden | 10.71 | - | 41 | - | 2 | 61 | 20 | measured |
| 62 | Asheville | 20.89 | - | - | - | - | - | 10 | predicted (travel demand) |
| 63 | Long Beach | 20.48 | - | - | - | - | - | 10 | predicted (travel demand) |
| 64 | Little Rock | 20.40 | - | - | - | - | - | 10 | predicted (travel demand) |
| 65 | Chicago | 19.97 | 485,769 | 6 | - | - | - | 30 | measured |
| 66 | Sardinia | 10.96 | - | 5 | 4 | - | 8 | 20 | measured |
| 67 | Edinburgh | 19.24 | 292,981 | 16 | 5 | 1 | - | 30 | measured |
| 68 | Utrecht | 9.74 | 67,963 | 27 | 6 | 2 | 340 | 20 | measured |
| 69 | Melbourne | 12.66 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 70 | Oakland | 18.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 71 | Cadiz | 11.93 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 72 | Strasbourg | 12.18 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 73 | Lexington | 18.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 74 | Reno | 18.19 | - | - | - | - | - | 10 | predicted (travel demand) |
| 75 | Des Moines | 18.11 | - | - | - | - | - | 10 | predicted (travel demand) |
| 76 | Perth | 17.53 | 180,478 | 6 | 3 | 1 | - | 30 | measured |
| 77 | Seattle | 17.05 | 398,724 | 6 | 1 | - | - | 30 | measured |
| 78 | Daytona Beach | 17.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 79 | Tallinn | 11.20 | 124,888 | 8 | 3 | 2 | 42 | 20 | measured |
| 80 | Chattanooga | 16.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 81 | Nice | 16.32 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 82 | Cagliari | 8.77 | 51,351 | 14 | 1 | 2 | 15 | 20 | measured |
| 83 | Athens | 15.83 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 84 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 85 | Cyprus | 15.58 | - | 4 | - | - | - | 20 | measured |
| 86 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 87 | Hoorn | 7.79 | - | 8 | - | 1 | 52 | 20 | measured |
| 88 | Venice | 8.52 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 89 | Huntsville | 15.35 | - | - | - | - | - | 10 | predicted (travel demand) |
| 90 | Hawaii | 13.64 | - | 6 | - | 1 | 6 | 30 | measured |
| 91 | Enschede | 7.55 | - | 7 | 1 | 1 | 82 | 20 | measured |
| 92 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 93 | West Palm Beach | 14.98 | - | - | - | - | - | 10 | predicted (travel demand) |
| 94 | Saint Petersburg | 14.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 95 | Osaka | 9.50 | 163,112 | 6 | 1 | - | - | 30 | measured |
| 96 | St. Louis | 14.80 | - | - | - | - | - | 10 | predicted (travel demand) |
| 97 | Hilo | 11.20 | - | 6 | - | 1 | 16 | 20 | measured |
| 98 | Tilburg | 7.31 | - | 20 | - | 3 | 87 | 20 | measured |
| 99 | Budapest | 13.64 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 100 | Philadelphia | 13.64 | 405,294 | 1 | - | - | - | 20 | measured |
| 101 | Caserta | 7.06 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 102 | Tampa | 14.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 103 | Luxembourg City | 9.25 | 64,851 | 10 | 5 | 2 | 18 | 20 | measured |
| 104 | Bordeaux | 9.01 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 105 | Cincinnati | 13.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 106 | Parma | 7.31 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 107 | Lansing | 13.02 | - | - | - | - | - | 10 | predicted (travel demand) |
| 108 | Detroit | 12.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 109 | Istanbul | 10.71 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 110 | Amersfoort | 6.09 | - | 14 | 1 | 2 | 181 | 20 | measured |
| 111 | Sorrento | 6.09 | 40,049 | 7 | - | 1 | 20 | 20 | measured |
| 112 | Madrid | 7.31 | 274,553 | 17 | 11 | 2 | - | 20 | measured |
| 113 | Trento | 5.84 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 114 | Denver | 11.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 115 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 116 | San Jose | 11.39 | - | - | - | - | - | 10 | predicted (travel demand) |
| 117 | Sacramento | 11.32 | - | - | - | - | - | 10 | predicted (travel demand) |
| 118 | Jersey City | 10.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 119 | Menorca | 7.31 | - | 6 | - | - | 2 | 20 | measured |
| 120 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 121 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 122 | Milwaukee | 10.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 123 | Sydney | 10.23 | 305,304 | 7 | 1 | - | - | 30 | measured |
| 124 | Bologna | 5.60 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 125 | Salt Lake City | 10.31 | - | - | - | - | - | 10 | predicted (travel demand) |
| 126 | Atlanta | 10.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 127 | Anchorage | 10.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 128 | Cambridge | 10.23 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 129 | Glasgow | 9.50 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 130 | Raleigh | 10.07 | - | - | - | - | - | 10 | predicted (travel demand) |
| 131 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 132 | Cleveland | 9.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 133 | Zwolle | 4.87 | - | 16 | - | 2 | 56 | 20 | measured |
| 134 | El Paso | 9.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 135 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 136 | Montreal | 9.50 | 315,322 | 11 | - | 2 | - | 30 | measured |
| 137 | Miami | 9.48 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 138 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 139 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 140 | Seoul | 8.52 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 141 | Nuremberg | 6.09 | 161,614 | 12 | 1 | 1 | 38 | 20 | measured |
| 142 | Washington DC | 8.28 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 143 | Crete | 9.01 | - | 4 | 3 | - | - | 20 | measured |
| 144 | Kamakura | 5.60 | 33,492 | 6 | - | - | - | 20 | measured |
| 145 | Nashville | 8.93 | - | - | - | - | - | 10 | predicted (travel demand) |
| 146 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 147 | Eindhoven | 4.38 | - | 16 | - | 4 | 195 | 20 | measured |
| 148 | Leipzig | 5.84 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 149 | Lyon | 5.84 | 136,951 | 13 | 4 | 1 | 156 | 20 | measured |
| 150 | Salzburg | 5.84 | 107,243 | 9 | 3 | 2 | 34 | 20 | measured |
| 151 | Girona | 5.11 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 152 | Ann Arbor | 8.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 153 | Coimbra | 4.63 | 34,962 | 4 | - | - | 5 | 20 | measured |
| 154 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 155 | Heerlen | 4.14 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 156 | Bari | 4.87 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 157 | Segovia | 5.11 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 158 | Albuquerque | 7.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 159 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 160 | Ljubljana | 7.31 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 161 | Padua | 3.90 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 162 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 163 | Turin | 3.65 | 147,456 | 11 | 7 | 2 | 30 | 20 | measured |
| 164 | Venlo | 3.65 | - | 7 | - | 1 | 144 | 20 | measured |
| 165 | Warsaw | 4.87 | 197,929 | 39 | 3 | 4 | 1407 | 30 | measured |
| 166 | Hong Kong | 4.75 | 689,212 | 10 | 4 | 1 | 505 | 20 | measured |
| 167 | Helsinki | 5.60 | 148,908 | 12 | 2 | 1 | 13 | 30 | measured |
| 168 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 169 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 170 | Como | 3.41 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 171 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 172 | Hobart | 4.38 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 173 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 174 | Ibiza | 4.14 | - | 1 | - | - | 4 | 20 | measured |
| 175 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 176 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 177 | Apeldoorn | 3.17 | - | 10 | - | 2 | 80 | 20 | measured |
| 178 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 179 | Dubrovnik | 5.84 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 180 | Vancouver | 5.84 | 351,552 | 4 | - | - | - | 30 | measured |
| 181 | Deventer | 2.92 | - | 12 | - | 1 | 213 | 20 | measured |
| 182 | San Diego | 5.84 | 214,939 | 4 | 1 | 1 | - | 20 | measured |
| 183 | Stockholm | 4.63 | 188,184 | 6 | 4 | - | - | 30 | measured |
| 184 | Zurich | 5.60 | 140,788 | 6 | - | - | - | 20 | measured |
| 185 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 186 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 187 | Riga | 5.60 | 108,918 | 5 | 2 | - | - | 20 | measured |
| 188 | Kauai | 4.87 | - | 6 | 1 | - | 8 | 20 | measured |
| 189 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 190 | Bratislava | 3.65 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 191 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 192 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 193 | Stuttgart | 4.14 | 112,789 | 6 | 1 | - | - | 20 | measured |
| 194 | Spokane | 3.92 | - | 13 | - | 2 | 18 | 10 | published, never ranked (may be uncrawled) |
| 195 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 196 | Alkmaar | 2.68 | - | 7 | - | 1 | 79 | 20 | measured |
| 197 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 198 | Pamplona | 3.41 | 128,065 | 6 | - | - | 1 | 20 | measured |
| 199 | Santa Fe | 5.17 | - | - | - | - | - | 10 | predicted (travel demand) |
| 200 | Maui | 4.87 | - | 4 | - | - | 3 | 20 | measured |
| 201 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 202 | Hiroshima | 3.41 | 129,791 | 17 | 5 | 3 | - | 20 | measured |
| 203 | Beijing | 5.11 | 269,737 | 7 | 1 | - | - | 30 | measured |
| 204 | Bristol | 5.11 | 163,983 | 6 | 2 | - | - | 20 | measured |
| 205 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 206 | Boise | 5.07 | - | 4 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 207 | Perugia | 2.68 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 208 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 209 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 210 | Verona | 2.92 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 211 | Genoa | 2.68 | 145,206 | 13 | 2 | 1 | 10 | 20 | measured |
| 212 | Groningen | 2.44 | 31,401 | 21 | 1 | 2 | 76 | 20 | measured |
| 213 | Maastricht | 2.44 | 47,763 | 19 | - | 2 | 135 | 20 | measured |
| 214 | Naples | 2.44 | 198,913 | 24 | 3 | 3 | 46 | 20 | measured |
| 215 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 216 | Nagoya | 3.17 | 83,437 | 6 | 1 | - | 1 | 20 | measured |
| 217 | Rio de Janeiro | 4.75 | 279,431 | 6 | - | - | - | 30 | measured |
| 218 | Toronto | 4.63 | 411,011 | 6 | - | - | - | 30 | measured |
| 219 | Guimaraes | 2.44 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 220 | Hamburg | 4.38 | 191,221 | 6 | 1 | 1 | - | 30 | measured |
| 221 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 222 | Kanazawa | 2.92 | 25,778 | 7 | 2 | 1 | 2 | 20 | measured |
| 223 | Charleston | 4.38 | 155,987 | 2 | 1 | - | - | 20 | measured |
| 224 | Braga | 2.44 | 34,522 | 4 | 2 | - | 8 | 20 | measured |
| 225 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 226 | Mexico City | 4.14 | 566,583 | 9 | 2 | - | - | 30 | measured |
| 227 | Bangkok | 4.38 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 228 | Belfast | 4.38 | 224,315 | 4 | - | 1 | - | 20 | measured |
| 229 | Hilversum | 2.19 | - | 6 | 1 | 1 | 122 | 20 | measured |
| 230 | Quebec City | 2.92 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 231 | Rotterdam | 2.19 | 104,938 | 12 | - | 2 | 83 | 20 | measured |
| 232 | Toulouse | 2.92 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 233 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 234 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 235 | Catania | 2.44 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 236 | Liverpool | 4.14 | 248,189 | 2 | 1 | - | - | 20 | measured |
| 237 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 238 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 239 | Brno | 2.68 | 63,714 | 8 | 5 | 2 | 34 | 20 | measured |
| 240 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 241 | Bergamo | 1.95 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 242 | Den Bosch | 1.95 | 39,682 | 12 | 2 | 1 | 118 | 20 | measured |
| 243 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 244 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 245 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 246 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 247 | Sapporo | 2.44 | 88,633 | 6 | - | - | - | 20 | measured |
| 248 | Aarhus | 3.41 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 249 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 250 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 251 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 252 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 253 | Manchester | 3.41 | 316,438 | 5 | - | - | - | 30 | measured |
| 254 | Savannah | 3.41 | 128,162 | 2 | 1 | - | - | 20 | measured |
| 255 | Taipei | 3.41 | 143,193 | 4 | 1 | - | - | 30 | measured |
| 256 | San Antonio | 3.32 | - | 4 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 257 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 258 | Dresden | 2.19 | 113,624 | 5 | 5 | 1 | - | 20 | measured |
| 259 | Fort Worth | 3.28 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 260 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 261 | Auckland | 3.17 | 152,056 | 5 | 2 | - | - | 20 | measured |
| 262 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 263 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 264 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 265 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 266 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 267 | Heidelberg | 2.68 | 75,837 | 6 | 1 | 1 | - | 20 | measured |
| 268 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 269 | Assen | 1.46 | - | 10 | - | 2 | 66 | 20 | measured |
| 270 | Delft | 1.46 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 271 | Graz | 1.95 | 65,717 | 12 | 7 | 1 | 87 | 20 | measured |
| 272 | Kansas City | 2.92 | - | 4 | - | 1 | - | 30 | measured |
| 273 | Buenos Aires | 2.80 | 333,331 | 4 | 2 | - | - | 30 | measured |
| 274 | Matera | 1.70 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 275 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 276 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 277 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 278 | Ghent | 2.44 | 82,757 | 6 | 1 | 1 | - | 20 | measured |
| 279 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 280 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 281 | Naha | 1.70 | 24,466 | 6 | - | - | 1 | 20 | measured |
| 282 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 283 | Belgrade | 2.56 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 284 | Potsdam | 1.70 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 285 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 286 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 287 | Tarragona | 1.46 | 32,396 | 4 | 2 | - | - | 20 | measured |
| 288 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 289 | Bruges | 2.44 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 290 | Thessaloniki | 2.44 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 291 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 292 | Regensburg | 2.19 | 51,930 | 5 | - | 1 | 4 | 20 | measured |
| 293 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 294 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 295 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 296 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 297 | Canberra | 2.28 | - | 1 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 298 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 299 | Pisa | 1.46 | 52,174 | 4 | - | 1 | - | 20 | measured |
| 300 | Zaragoza | 1.46 | 87,580 | 7 | - | 1 | - | 20 | measured |
| 301 | Cologne | 2.19 | 191,812 | 5 | - | 1 | - | 30 | measured |
| 302 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 303 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 304 | Modena | 1.22 | 51,698 | 5 | 1 | 1 | 3 | 20 | measured |
| 305 | Pittsburgh | 1.95 | - | 4 | - | 1 | - | 20 | measured |
| 306 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 307 | Breda | 0.97 | 36,579 | 10 | - | 2 | 118 | 20 | measured |
| 308 | Roosendaal | 0.97 | - | 8 | - | 1 | 116 | 20 | measured |
| 309 | Trieste | 0.97 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 310 | Bucharest | 1.84 | 136,836 | 4 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 311 | Gdansk | 1.22 | 4,908 | 12 | 4 | 1 | 307 | 20 | measured |
| 312 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 313 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 314 | Setubal | 0.97 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 315 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 316 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 317 | York | 1.70 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 318 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 319 | Ronda | 0.97 | 51,510 | 6 | 1 | - | 9 | 20 | measured |
| 320 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 321 | Rouen | 1.46 | 72,334 | 12 | - | 1 | 6 | 20 | measured |
| 322 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 323 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 324 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 325 | Baltimore | 1.46 | - | 4 | - | - | - | 20 | measured |
| 326 | Fort Lauderdale | 1.46 | - | 4 | - | - | - | 30 | measured |
| 327 | Oxford | 1.46 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 328 | Bilbao | 0.97 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 329 | Lucca | 0.73 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 330 | Minneapolis | 1.46 | - | 4 | - | - | - | 20 | measured |
| 331 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 332 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 333 | Ferrara | 0.73 | 27,490 | 5 | 3 | 1 | 7 | 20 | measured |
| 334 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 335 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 336 | Brighton | 1.22 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 337 | Leuven | 1.22 | 40,645 | 4 | - | - | - | 20 | measured |
| 338 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 339 | Assisi | 0.73 | 30,278 | 6 | 1 | 2 | 6 | 20 | measured |
| 340 | Yakushima | 0.73 | - | 1 | - | - | 1 | 20 | measured |
| 341 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 342 | Salamanca | 0.73 | 47,897 | 4 | - | 1 | 1 | 20 | measured |
| 343 | Frankfurt | 0.73 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 344 | Poznan | 0.73 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 345 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 346 | Gothenburg | 0.97 | 119,991 | 5 | - | 1 | - | 20 | measured |
| 347 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 348 | Tulsa | 0.97 | - | 1 | - | - | - | 20 | measured |
| 349 | Busan | 0.83 | 94,737 | 2 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 350 | Cesky Krumlov | 0.49 | 28,582 | 6 | 3 | - | 11 | 20 | measured |
| 351 | Lausanne | 0.73 | 68,242 | 8 | 1 | 1 | - | 20 | measured |
| 352 | Sofia | 0.49 | 138,710 | 4 | - | - | - | 30 | measured |
| 353 | Wroclaw | 0.49 | 123,894 | 5 | 1 | 1 | 121 | 20 | measured |
| 354 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 355 | Rothenburg ob der Tauber | 0.49 | 39,879 | 4 | - | 1 | 8 | 20 | measured |
| 356 | Phoenix | 0.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 357 | Cardiff | 0.49 | - | 4 | - | 1 | - | 20 | measured |
| 358 | Indianapolis | 0.49 | - | 1 | - | - | - | 30 | measured |
| 359 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 360 | Antwerp | 0.49 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 361 | Monterey | 0.49 | - | 3 | - | - | - | 20 | measured |
| 362 | Split | 0.49 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 363 | Turku | 0.49 | - | 1 | - | - | - | 30 | measured |
| 364 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 365 | Bamberg | 0.24 | 28,716 | 5 | 4 | 1 | 10 | 20 | measured |
| 366 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 367 | George Town | 0.28 | 36,080 | - | - | - | - | 10 | predicted (travel demand) |
| 368 | Hallstatt | 0.24 | 47,271 | 5 | 1 | - | - | 20 | measured |
| 369 | Freiburg | 0.24 | 92,752 | 7 | 2 | 1 | - | 20 | measured |
| 370 | Sao Paulo | 0.24 | 911 | 1 | - | - | - | 20 | measured |
| 371 | Allentown | 0.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 372 | Nantes | 0.24 | 67,689 | 1 | 1 | - | - | 20 | measured |
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

