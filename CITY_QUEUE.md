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
| 1 | Brussels | 181.38 | 176,863 | 31 | 4 | 1 | 436 | 30 | measured |
| 2 | Milan | 100.04 | 212,705 | 25 | 11 | 3 | 25 | 30 | measured |
| 3 | Lisbon | 83.21 | 201,877 | 35 | 16 | 3 | 68 | 30 | measured |
| 4 | Barcelona | 77.83 | 346,477 | 56 | 14 | 7 | 180 | 30 | measured |
| 5 | Rome | 73.86 | 358,876 | 31 | 10 | 2 | 32 | 30 | measured |
| 6 | Amsterdam | 65.21 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 7 | Oahu | 66.85 | - | 21 | 2 | 3 | 163 | 20 | measured |
| 8 | Pamplona | 64.75 | 128,065 | 6 | - | - | 1 | 20 | measured |
| 9 | Arnhem | 47.22 | 31,478 | 39 | 3 | 3 | 204 | 20 | measured |
| 10 | Florence | 43.71 | 184,099 | 26 | 9 | 1 | 27 | 30 | measured |
| 11 | Tenerife | 56.80 | - | 4 | 2 | - | - | 20 | measured |
| 12 | Singapore | 53.76 | 967,821 | 34 | 6 | 3 | 165 | 30 | measured |
| 13 | Seville | 52.36 | 170,545 | 43 | 9 | 2 | - | 20 | measured |
| 14 | Palermo | 38.33 | 124,310 | 21 | 9 | 1 | 37 | 20 | measured |
| 15 | Berlin | 43.94 | 412,181 | 23 | 17 | 2 | 195 | 30 | measured |
| 16 | Los Angeles | 62.64 | 665,559 | 8 | 2 | - | - | 30 | measured |
| 17 | Brisbane | 41.37 | 162,602 | 20 | 2 | 2 | 186 | 30 | measured |
| 18 | London | 51.66 | 718,291 | 23 | 14 | 1 | - | 30 | measured |
| 19 | Paris | 38.10 | 524,268 | 31 | 9 | 4 | 129 | 30 | measured |
| 20 | Valencia | 28.52 | 162,209 | 31 | 4 | 2 | 350 | 30 | measured |
| 21 | Alicante | 26.65 | 77,454 | 21 | 4 | 2 | 44 | 20 | measured |
| 22 | Vienna | 35.53 | 283,090 | 32 | 18 | 5 | 376 | 30 | measured |
| 23 | Prague | 34.59 | 303,350 | 30 | 21 | 4 | 31 | 30 | measured |
| 24 | Malaga | 30.62 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 25 | Leiden | 22.67 | 33,227 | 20 | 6 | 1 | 129 | 20 | measured |
| 26 | Tokyo | 24.31 | 394,702 | 21 | 8 | 1 | 5 | 20 | measured |
| 27 | Dublin | 22.67 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 28 | Krakow | 25.94 | 140,824 | 38 | 8 | 3 | 198 | 30 | measured |
| 29 | Portland | 25.71 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 30 | New York | 33.66 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 31 | Birmingham | 37.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 32 | Philadelphia | 35.53 | 405,294 | 1 | - | - | - | 20 | measured |
| 33 | Boston | 34.59 | 385,902 | 11 | 2 | 1 | - | 30 | measured |
| 34 | Vilnius | 23.61 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 35 | Haarlem | 17.53 | 33,960 | 21 | - | 2 | 277 | 20 | measured |
| 36 | Copenhagen | 32.02 | 218,621 | 16 | 2 | 2 | - | 30 | measured |
| 37 | Kyoto | 21.50 | 142,353 | 18 | 12 | 2 | - | 20 | measured |
| 38 | Nijmegen | 16.36 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 39 | The Hague | 16.36 | 236,723 | 31 | 2 | 5 | 167 | 20 | measured |
| 40 | Dallas | 31.79 | - | 9 | 1 | 1 | - | 30 | measured |
| 41 | Houston | 31.32 | - | 4 | - | - | - | 30 | measured |
| 42 | New Orleans | 30.85 | 256,232 | 4 | 2 | 1 | - | 20 | measured |
| 43 | Madeira | 18.47 | - | 10 | 1 | 1 | - | 20 | measured |
| 44 | Cork | 20.34 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 45 | Munich | 20.34 | 224,067 | 45 | 15 | 6 | 80 | 30 | measured |
| 46 | Helmond | 14.73 | - | 18 | - | 2 | 55 | 20 | measured |
| 47 | Reykjavik | 24.31 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 48 | Ottawa | 18.47 | - | 19 | - | 3 | 122 | 20 | measured |
| 49 | Bath | 27.35 | 144,950 | 5 | 2 | 1 | - | 20 | measured |
| 50 | Dordrecht | 13.56 | - | 20 | 1 | 2 | 105 | 20 | measured |
| 51 | Sintra | 13.56 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 52 | Austin | 26.18 | 226,631 | 5 | 2 | - | - | 20 | measured |
| 53 | Fukuoka | 16.83 | 77,485 | 15 | 9 | 1 | - | 20 | measured |
| 54 | Palma de Mallorca | 15.43 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 55 | Porto | 12.62 | 120,415 | 27 | 15 | 2 | 40 | 20 | measured |
| 56 | Las Vegas | 24.31 | - | 11 | - | 2 | - | 30 | measured |
| 57 | Granada | 15.19 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 58 | Venice | 12.86 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 59 | Geneva | 15.43 | 162,269 | 21 | 5 | 4 | 131 | 20 | measured |
| 60 | Utrecht | 11.45 | 67,963 | 27 | 7 | 2 | 340 | 20 | measured |
| 61 | Jacksonville | 22.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 62 | Cadiz | 14.26 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 63 | Leeuwarden | 10.99 | - | 41 | - | 2 | 61 | 20 | measured |
| 64 | Oslo | 18.93 | 181,113 | 4 | - | - | - | 20 | measured |
| 65 | Cordoba | 13.79 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 66 | Asheville | 20.89 | - | - | - | - | - | 10 | predicted (travel demand) |
| 67 | Long Beach | 20.48 | - | - | - | - | - | 10 | predicted (travel demand) |
| 68 | Little Rock | 20.40 | - | - | - | - | - | 10 | predicted (travel demand) |
| 69 | Edinburgh | 19.63 | 292,981 | 16 | 5 | 1 | - | 30 | measured |
| 70 | San Francisco | 19.17 | 361,111 | 6 | 1 | 1 | - | 30 | measured |
| 71 | Nice | 19.17 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 72 | Seattle | 18.23 | 398,724 | 6 | 1 | - | - | 30 | measured |
| 73 | Oakland | 18.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 74 | Lexington | 18.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 75 | Reno | 18.19 | - | - | - | - | - | 10 | predicted (travel demand) |
| 76 | Des Moines | 18.11 | - | - | - | - | - | 10 | predicted (travel demand) |
| 77 | Sardinia | 10.05 | - | 5 | 4 | - | 8 | 20 | measured |
| 78 | Melbourne | 11.92 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 79 | Cagliari | 9.58 | 51,351 | 14 | 1 | 2 | 15 | 20 | measured |
| 80 | Chicago | 17.76 | 485,769 | 6 | - | - | - | 30 | measured |
| 81 | Daytona Beach | 17.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 82 | Perth | 17.06 | 180,478 | 6 | 3 | 1 | - | 30 | measured |
| 83 | Strasbourg | 11.22 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 84 | Chattanooga | 16.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 85 | Athens | 16.13 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 86 | Tilburg | 8.18 | - | 20 | - | 3 | 87 | 20 | measured |
| 87 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 88 | Madrid | 9.82 | 274,553 | 17 | 11 | 2 | - | 20 | measured |
| 89 | Enschede | 7.95 | - | 7 | 1 | 1 | 82 | 20 | measured |
| 90 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 91 | Hoorn | 7.71 | - | 8 | - | 1 | 52 | 20 | measured |
| 92 | Huntsville | 15.35 | - | - | - | - | - | 10 | predicted (travel demand) |
| 93 | Cyprus | 14.96 | - | 4 | - | - | - | 20 | measured |
| 94 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 95 | West Palm Beach | 14.98 | - | - | - | - | - | 10 | predicted (travel demand) |
| 96 | Saint Petersburg | 14.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 97 | St. Louis | 14.80 | - | - | - | - | - | 10 | predicted (travel demand) |
| 98 | Bordeaux | 9.58 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 99 | Tampa | 14.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 100 | Caserta | 6.78 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 101 | Osaka | 8.65 | 163,112 | 6 | 1 | - | - | 30 | measured |
| 102 | Cincinnati | 13.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 103 | Lansing | 13.02 | - | - | - | - | - | 10 | predicted (travel demand) |
| 104 | Tallinn | 8.65 | 124,888 | 9 | 3 | 2 | 42 | 20 | measured |
| 105 | Budapest | 12.15 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 106 | Hawaii | 11.22 | - | 6 | - | 1 | 6 | 30 | measured |
| 107 | Detroit | 12.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 108 | Parma | 6.78 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 109 | Denver | 11.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 110 | Luxembourg City | 7.71 | 64,851 | 10 | 5 | 2 | 18 | 20 | measured |
| 111 | Cambridge | 11.45 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 112 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 113 | San Jose | 11.39 | - | - | - | - | - | 10 | predicted (travel demand) |
| 114 | Sacramento | 11.32 | - | - | - | - | - | 10 | predicted (travel demand) |
| 115 | Jersey City | 10.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 116 | Sorrento | 5.61 | 40,049 | 7 | - | 1 | 20 | 20 | measured |
| 117 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 118 | Menorca | 7.25 | - | 6 | - | - | 2 | 20 | measured |
| 119 | Istanbul | 9.70 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 120 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 121 | Milwaukee | 10.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 122 | Salt Lake City | 10.31 | - | - | - | - | - | 10 | predicted (travel demand) |
| 123 | Atlanta | 10.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 124 | Crete | 10.28 | - | 4 | 3 | - | - | 20 | measured |
| 125 | Anchorage | 10.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 126 | Raleigh | 10.07 | - | - | - | - | - | 10 | predicted (travel demand) |
| 127 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 128 | Glasgow | 9.35 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 129 | Washington DC | 8.88 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 130 | Cleveland | 9.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 131 | Segovia | 6.08 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 132 | El Paso | 9.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 133 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 134 | Ibiza | 6.08 | - | 1 | - | - | 4 | 20 | measured |
| 135 | Sydney | 9.35 | 305,304 | 7 | 1 | - | - | 30 | measured |
| 136 | Miami | 9.48 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 137 | Coimbra | 5.14 | 34,962 | 4 | - | - | 5 | 20 | measured |
| 138 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 139 | Amersfoort | 4.67 | - | 14 | 1 | 2 | 181 | 20 | measured |
| 140 | Seoul | 8.65 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 141 | Zwolle | 4.67 | - | 16 | - | 2 | 56 | 20 | measured |
| 142 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 143 | Leipzig | 6.08 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 144 | Nashville | 8.93 | - | - | - | - | - | 10 | predicted (travel demand) |
| 145 | Como | 4.44 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 146 | Padua | 4.67 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 147 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 148 | Hilo | 6.54 | - | 6 | - | 1 | 16 | 20 | measured |
| 149 | Ann Arbor | 8.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 150 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 151 | Montreal | 7.95 | 315,322 | 11 | - | 2 | - | 30 | measured |
| 152 | Eindhoven | 3.97 | - | 16 | - | 4 | 195 | 20 | measured |
| 153 | Groningen | 3.97 | 31,401 | 21 | 1 | 2 | 76 | 20 | measured |
| 154 | Perugia | 4.21 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 155 | Bari | 4.67 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 156 | Albuquerque | 7.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 157 | Zurich | 7.25 | 140,788 | 6 | - | - | - | 20 | measured |
| 158 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 159 | Heerlen | 3.74 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 160 | Hobart | 4.91 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 161 | Helsinki | 5.84 | 148,908 | 12 | 2 | 1 | 13 | 30 | measured |
| 162 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 163 | Venlo | 3.51 | - | 7 | - | 1 | 144 | 20 | measured |
| 164 | Monterey | 7.01 | - | 3 | - | - | - | 20 | measured |
| 165 | Warsaw | 4.67 | 197,929 | 39 | 3 | 4 | 1407 | 30 | measured |
| 166 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 167 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 168 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 169 | Lyon | 4.44 | 136,951 | 13 | 4 | 1 | 156 | 20 | measured |
| 170 | Nuremberg | 4.44 | 161,614 | 12 | 1 | 1 | 38 | 20 | measured |
| 171 | Salzburg | 4.44 | 107,243 | 9 | 3 | 2 | 34 | 20 | measured |
| 172 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 173 | San Diego | 6.54 | 214,939 | 4 | 1 | 1 | - | 20 | measured |
| 174 | Trento | 3.27 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 175 | Hong Kong | 4.32 | 689,212 | 10 | 4 | 1 | 505 | 20 | measured |
| 176 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 177 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 178 | Girona | 3.74 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 179 | Bangkok | 6.31 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 180 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 181 | Alkmaar | 3.04 | - | 7 | - | 1 | 79 | 20 | measured |
| 182 | Apeldoorn | 3.04 | - | 10 | - | 2 | 80 | 20 | measured |
| 183 | Turin | 3.04 | 147,456 | 11 | 7 | 2 | 30 | 20 | measured |
| 184 | Ljubljana | 5.84 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 185 | Vancouver | 5.84 | 351,552 | 4 | - | - | - | 30 | measured |
| 186 | Bristol | 5.84 | 163,983 | 6 | 2 | - | - | 20 | measured |
| 187 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 188 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 189 | Deventer | 2.80 | - | 12 | - | 1 | 213 | 20 | measured |
| 190 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 191 | Genoa | 3.04 | 145,206 | 13 | 2 | 1 | 10 | 20 | measured |
| 192 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 193 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 194 | Spokane | 3.92 | - | 13 | - | 2 | 18 | 10 | published, never ranked (may be uncrawled) |
| 195 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 196 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 197 | Charleston | 5.14 | 155,987 | 2 | 1 | - | - | 20 | measured |
| 198 | Santa Fe | 5.17 | - | - | - | - | - | 10 | predicted (travel demand) |
| 199 | Belfast | 5.14 | 224,315 | 4 | - | 1 | - | 20 | measured |
| 200 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 201 | Maastricht | 2.57 | 47,763 | 19 | - | 2 | 135 | 20 | measured |
| 202 | Braga | 2.80 | 34,522 | 4 | 2 | - | 8 | 20 | measured |
| 203 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 204 | Stockholm | 3.97 | 188,184 | 6 | 4 | - | - | 30 | measured |
| 205 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 206 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 207 | Hamburg | 4.67 | 191,221 | 6 | 1 | 1 | - | 30 | measured |
| 208 | Maui | 4.67 | - | 4 | - | - | 3 | 20 | measured |
| 209 | Beijing | 4.91 | 269,737 | 7 | 1 | - | - | 30 | measured |
| 210 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 211 | Yakushima | 3.04 | - | 1 | - | - | 1 | 20 | measured |
| 212 | Bologna | 2.57 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 213 | Hilversum | 2.34 | - | 6 | 1 | 1 | 122 | 20 | measured |
| 214 | Naples | 2.34 | 198,913 | 24 | 3 | 3 | 46 | 20 | measured |
| 215 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 216 | Graz | 3.04 | 65,717 | 12 | 7 | 1 | 87 | 20 | measured |
| 217 | Quebec City | 3.04 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 218 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 219 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 220 | Toronto | 4.21 | 411,011 | 6 | - | - | - | 30 | measured |
| 221 | Boise | 4.21 | - | 4 | - | 1 | - | 30 | measured |
| 222 | Assen | 2.10 | - | 10 | - | 2 | 66 | 20 | measured |
| 223 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 224 | Heidelberg | 3.74 | 75,837 | 6 | 1 | 1 | - | 20 | measured |
| 225 | Kamakura | 2.57 | 33,492 | 6 | - | - | - | 20 | measured |
| 226 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 227 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 228 | Catania | 2.34 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 229 | Rio de Janeiro | 3.97 | 279,431 | 6 | - | - | - | 30 | measured |
| 230 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 231 | Verona | 2.34 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 232 | Nagoya | 2.57 | 83,437 | 6 | 1 | - | 1 | 20 | measured |
| 233 | Bratislava | 2.57 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 234 | Dresden | 2.57 | 113,624 | 5 | 5 | 1 | - | 20 | measured |
| 235 | Hiroshima | 2.57 | 129,791 | 17 | 5 | 3 | - | 20 | measured |
| 236 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 237 | Toulouse | 2.57 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 238 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 239 | Riga | 3.74 | 108,918 | 5 | 2 | - | - | 20 | measured |
| 240 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 241 | Kauai | 3.27 | - | 6 | 1 | - | 8 | 20 | measured |
| 242 | Bergamo | 1.87 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 243 | Delft | 1.87 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 244 | Den Bosch | 1.87 | 39,682 | 12 | 2 | 1 | 118 | 20 | measured |
| 245 | Dubrovnik | 3.51 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 246 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 247 | Guimaraes | 1.87 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 248 | Mexico City | 3.39 | 566,583 | 9 | 2 | - | - | 30 | measured |
| 249 | Matera | 2.10 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 250 | Brno | 2.34 | 63,714 | 8 | 5 | 2 | 34 | 20 | measured |
| 251 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 252 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 253 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 254 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 255 | Aarhus | 3.27 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 256 | San Antonio | 3.32 | - | 4 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 257 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 258 | Fort Worth | 3.28 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 259 | Rotterdam | 1.64 | 104,938 | 12 | - | 2 | 83 | 20 | measured |
| 260 | Savannah | 3.27 | 128,162 | 2 | 1 | - | - | 20 | measured |
| 261 | Taipei | 3.27 | 143,193 | 4 | 1 | - | - | 30 | measured |
| 262 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 263 | Kanazawa | 2.10 | 25,778 | 7 | 2 | 1 | 2 | 20 | measured |
| 264 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 265 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 266 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 267 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 268 | Split | 3.04 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 269 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 270 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 271 | Pisa | 1.87 | 52,174 | 4 | - | 1 | - | 20 | measured |
| 272 | Oxford | 2.80 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 273 | Ferrara | 1.64 | 27,490 | 5 | 3 | 1 | 7 | 20 | measured |
| 274 | Potsdam | 1.87 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 275 | Sapporo | 1.87 | 88,633 | 6 | - | - | - | 20 | measured |
| 276 | Buenos Aires | 2.69 | 333,331 | 4 | 2 | - | - | 30 | measured |
| 277 | Liverpool | 2.80 | 248,189 | 2 | 1 | - | - | 20 | measured |
| 278 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 279 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 280 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 281 | Belgrade | 2.69 | 178,116 | 5 | 5 | - | - | 20 | measured |
| 282 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 283 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 284 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 285 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 286 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 287 | Stuttgart | 1.87 | 112,789 | 6 | 1 | - | - | 20 | measured |
| 288 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 289 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 290 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 291 | Pittsburgh | 2.34 | - | 4 | - | 1 | - | 20 | measured |
| 292 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 293 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 294 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 295 | Lucca | 1.17 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 296 | Trieste | 1.17 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 297 | Regensburg | 2.10 | 51,930 | 5 | - | 1 | 4 | 20 | measured |
| 298 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 299 | Salamanca | 1.40 | 47,897 | 4 | - | 1 | 1 | 20 | measured |
| 300 | Zaragoza | 1.40 | 87,580 | 7 | - | 1 | - | 20 | measured |
| 301 | Thessaloniki | 2.10 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 302 | York | 2.10 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 303 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 304 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 305 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 306 | Baltimore | 1.87 | - | 4 | - | - | - | 20 | measured |
| 307 | Fort Lauderdale | 1.87 | - | 4 | - | - | - | 30 | measured |
| 308 | Cologne | 1.87 | 191,812 | 5 | - | 1 | - | 30 | measured |
| 309 | Lausanne | 1.87 | 68,242 | 8 | 1 | 1 | - | 20 | measured |
| 310 | Minneapolis | 1.87 | - | 4 | - | - | - | 20 | measured |
| 311 | Breda | 0.93 | 36,579 | 10 | - | 2 | 118 | 20 | measured |
| 312 | Roosendaal | 0.93 | - | 8 | - | 1 | 116 | 20 | measured |
| 313 | Bucharest | 1.84 | 136,836 | 4 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 314 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 315 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 316 | Gdansk | 1.17 | 4,908 | 12 | 4 | 1 | 307 | 20 | measured |
| 317 | Setubal | 0.93 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 318 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 319 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 320 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 321 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 322 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 323 | Hallstatt | 1.40 | 47,271 | 5 | 1 | - | - | 20 | measured |
| 324 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 325 | Ronda | 0.93 | 51,510 | 6 | 1 | - | 9 | 20 | measured |
| 326 | Tarragona | 0.93 | 32,396 | 4 | 2 | - | - | 20 | measured |
| 327 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 328 | Ghent | 1.40 | 82,757 | 8 | 1 | 1 | - | 20 | measured |
| 329 | Auckland | 1.40 | 152,056 | 5 | 2 | - | - | 20 | measured |
| 330 | Naha | 0.93 | 24,466 | 6 | - | - | 1 | 20 | measured |
| 331 | Brighton | 1.40 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 332 | Frankfurt | 0.93 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 333 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 334 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 335 | Antwerp | 1.26 | 128,289 | 10 | 4 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 336 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 337 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 338 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 339 | Leuven | 1.17 | 40,645 | 4 | - | - | - | 20 | measured |
| 340 | Assisi | 0.70 | 30,278 | 6 | 1 | 2 | 6 | 20 | measured |
| 341 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 342 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 343 | Poznan | 0.70 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 344 | Wroclaw | 0.70 | 123,894 | 5 | 1 | 1 | 121 | 20 | measured |
| 345 | Rouen | 0.93 | 72,334 | 12 | - | 1 | 6 | 20 | measured |
| 346 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 347 | Cardiff | 0.93 | - | 4 | - | 1 | - | 20 | measured |
| 348 | Indianapolis | 0.93 | - | 1 | - | - | - | 30 | measured |
| 349 | Bruges | 0.93 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 350 | Kansas City | 0.93 | - | 4 | - | 1 | - | 30 | measured |
| 351 | Nantes | 0.93 | 67,689 | 1 | 1 | - | - | 20 | measured |
| 352 | Tulsa | 0.93 | - | 1 | - | - | - | 20 | measured |
| 353 | Bilbao | 0.47 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 354 | Gothenburg | 0.70 | 119,991 | 5 | - | 1 | - | 20 | measured |
| 355 | Manchester | 0.70 | 316,438 | 5 | - | - | - | 30 | measured |
| 356 | Sofia | 0.47 | 138,710 | 4 | - | - | - | 30 | measured |
| 357 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 358 | Rothenburg ob der Tauber | 0.47 | 39,879 | 4 | - | 1 | 8 | 20 | measured |
| 359 | Phoenix | 0.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 360 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 361 | Freiburg | 0.47 | 92,752 | 7 | 2 | 1 | - | 20 | measured |
| 362 | Turku | 0.47 | - | 1 | - | - | - | 30 | measured |
| 363 | Modena | 0.23 | 51,698 | 5 | 1 | 1 | 3 | 20 | measured |
| 364 | Sao Paulo | 0.35 | 911 | 1 | - | - | - | 20 | measured |
| 365 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 366 | Cesky Krumlov | 0.23 | 28,582 | 6 | 3 | - | 11 | 20 | measured |
| 367 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 368 | Bamberg | 0.23 | 28,716 | 5 | 4 | 1 | 10 | 20 | measured |
| 369 | George Town | 0.28 | 36,080 | - | - | - | - | 10 | predicted (travel demand) |
| 370 | Allentown | 0.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 371 | Busan | 0.23 | 94,737 | 2 | - | - | - | 20 | measured |
| 372 | Canberra | 0.23 | - | 1 | 1 | - | - | 30 | measured |
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

