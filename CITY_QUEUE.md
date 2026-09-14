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
| 1 | Brussels | 187.04 | 176,863 | 31 | 4 | 1 | 436 | 30 | measured |
| 2 | Milan | 109.66 | 212,705 | 25 | 11 | 3 | 25 | 30 | measured |
| 3 | Lisbon | 89.16 | 201,877 | 35 | 16 | 3 | 68 | 30 | measured |
| 4 | Rome | 88.39 | 358,876 | 31 | 10 | 2 | 32 | 30 | measured |
| 5 | Barcelona | 84.81 | 346,477 | 56 | 14 | 7 | 180 | 30 | measured |
| 6 | Amsterdam | 65.33 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 7 | Arnhem | 50.99 | 31,478 | 39 | 3 | 3 | 204 | 20 | measured |
| 8 | Florence | 44.58 | 184,099 | 26 | 9 | 1 | 27 | 30 | measured |
| 9 | Oahu | 59.44 | - | 21 | 2 | 3 | 163 | 20 | measured |
| 10 | Tenerife | 57.65 | - | 4 | 2 | - | - | 20 | measured |
| 11 | Singapore | 55.85 | 967,821 | 34 | 6 | 3 | 165 | 30 | measured |
| 12 | Seville | 54.83 | 170,545 | 43 | 9 | 2 | - | 20 | measured |
| 13 | Palermo | 36.90 | 124,310 | 21 | 9 | 1 | 37 | 20 | measured |
| 14 | Los Angeles | 67.13 | 665,559 | 8 | 2 | - | - | 30 | measured |
| 15 | Brisbane | 46.38 | 162,602 | 20 | 2 | 2 | 186 | 30 | measured |
| 16 | Berlin | 44.58 | 412,181 | 23 | 17 | 2 | 195 | 30 | measured |
| 17 | London | 54.06 | 718,291 | 23 | 14 | 1 | - | 30 | measured |
| 18 | Valencia | 30.49 | 162,209 | 31 | 4 | 2 | 350 | 30 | measured |
| 19 | Paris | 39.46 | 524,268 | 31 | 9 | 4 | 129 | 30 | measured |
| 20 | Prague | 37.92 | 303,350 | 30 | 21 | 4 | 31 | 30 | measured |
| 21 | Vienna | 37.15 | 283,090 | 32 | 18 | 5 | 376 | 30 | measured |
| 22 | Leiden | 25.11 | 33,227 | 20 | 6 | 1 | 129 | 20 | measured |
| 23 | Alicante | 24.60 | 77,454 | 21 | 4 | 2 | 44 | 20 | measured |
| 24 | Malaga | 27.93 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 25 | Madeira | 25.11 | - | 10 | 1 | 1 | - | 20 | measured |
| 26 | Dublin | 22.55 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 27 | Haarlem | 19.22 | 33,960 | 21 | - | 2 | 277 | 20 | measured |
| 28 | Boston | 36.90 | 385,902 | 11 | 2 | 1 | - | 30 | measured |
| 29 | Birmingham | 37.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 30 | The Hague | 18.70 | 236,723 | 31 | 2 | 5 | 167 | 20 | measured |
| 31 | Krakow | 24.60 | 140,824 | 38 | 8 | 3 | 198 | 30 | measured |
| 32 | Vilnius | 24.60 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 33 | Kyoto | 23.32 | 142,353 | 18 | 12 | 2 | - | 20 | measured |
| 34 | New York | 31.77 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 35 | Copenhagen | 34.08 | 218,621 | 16 | 2 | 2 | - | 30 | measured |
| 36 | Nijmegen | 17.68 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 37 | Portland | 23.57 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 38 | Tokyo | 19.22 | 394,702 | 21 | 8 | 1 | 5 | 20 | measured |
| 39 | Helmond | 16.91 | - | 18 | - | 2 | 55 | 20 | measured |
| 40 | Munich | 21.01 | 224,067 | 45 | 15 | 6 | 80 | 30 | measured |
| 41 | Reykjavik | 26.13 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 42 | Dordrecht | 14.86 | - | 20 | 1 | 2 | 105 | 20 | measured |
| 43 | New Orleans | 29.72 | 256,232 | 4 | 2 | 1 | - | 20 | measured |
| 44 | Austin | 28.18 | 226,631 | 5 | 2 | - | - | 20 | measured |
| 45 | Sintra | 14.09 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 46 | Palma de Mallorca | 16.40 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 47 | Houston | 27.16 | - | 4 | - | - | - | 30 | measured |
| 48 | Oslo | 23.57 | 181,113 | 4 | - | - | - | 20 | measured |
| 49 | Bath | 26.13 | 144,950 | 5 | 2 | 1 | - | 20 | measured |
| 50 | Las Vegas | 26.13 | - | 11 | - | 2 | - | 30 | measured |
| 51 | Ottawa | 17.17 | - | 19 | - | 3 | 122 | 20 | measured |
| 52 | Dallas | 25.62 | - | 9 | 1 | 1 | - | 30 | measured |
| 53 | Cork | 16.65 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 54 | Geneva | 16.40 | 162,269 | 21 | 5 | 4 | 131 | 20 | measured |
| 55 | Porto | 12.04 | 120,415 | 27 | 15 | 2 | 40 | 20 | measured |
| 56 | Granada | 14.86 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 57 | Philadelphia | 22.55 | 405,294 | 1 | - | - | - | 20 | measured |
| 58 | Fukuoka | 15.12 | 77,485 | 15 | 9 | 1 | - | 20 | measured |
| 59 | Cordoba | 14.86 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 60 | Jacksonville | 22.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 61 | Leeuwarden | 11.27 | - | 41 | - | 2 | 61 | 20 | measured |
| 62 | Utrecht | 11.02 | 67,963 | 27 | 7 | 2 | 340 | 20 | measured |
| 63 | Chicago | 21.52 | 485,769 | 6 | - | - | - | 30 | measured |
| 64 | San Francisco | 21.01 | 361,111 | 6 | 1 | 1 | - | 30 | measured |
| 65 | Edinburgh | 20.50 | 292,981 | 16 | 5 | 1 | - | 30 | measured |
| 66 | Asheville | 20.89 | - | - | - | - | - | 10 | predicted (travel demand) |
| 67 | Cadiz | 13.32 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 68 | Long Beach | 20.48 | - | - | - | - | - | 10 | predicted (travel demand) |
| 69 | Little Rock | 20.40 | - | - | - | - | - | 10 | predicted (travel demand) |
| 70 | Melbourne | 13.32 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 71 | Strasbourg | 12.81 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 72 | Oakland | 18.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 73 | Seattle | 17.94 | 398,724 | 6 | 1 | - | - | 30 | measured |
| 74 | Lexington | 18.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 75 | Reno | 18.19 | - | - | - | - | - | 10 | predicted (travel demand) |
| 76 | Venice | 9.99 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 77 | Des Moines | 18.11 | - | - | - | - | - | 10 | predicted (travel demand) |
| 78 | Perth | 17.42 | 180,478 | 6 | 3 | 1 | - | 30 | measured |
| 79 | Daytona Beach | 17.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 80 | Nice | 17.42 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 81 | Sardinia | 9.48 | - | 5 | 4 | - | 8 | 20 | measured |
| 82 | Enschede | 8.46 | - | 7 | 1 | 1 | 82 | 20 | measured |
| 83 | Tilburg | 8.46 | - | 20 | - | 3 | 87 | 20 | measured |
| 84 | Cyprus | 16.40 | - | 4 | - | - | - | 20 | measured |
| 85 | Cagliari | 8.97 | 51,351 | 14 | 1 | 2 | 15 | 20 | measured |
| 86 | Chattanooga | 16.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 87 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 88 | Athens | 15.63 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 89 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 90 | Osaka | 9.99 | 163,112 | 6 | 1 | - | - | 30 | measured |
| 91 | Huntsville | 15.35 | - | - | - | - | - | 10 | predicted (travel demand) |
| 92 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 93 | West Palm Beach | 14.98 | - | - | - | - | - | 10 | predicted (travel demand) |
| 94 | Hoorn | 7.43 | - | 8 | - | 1 | 52 | 20 | measured |
| 95 | Saint Petersburg | 14.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 96 | St. Louis | 14.80 | - | - | - | - | - | 10 | predicted (travel demand) |
| 97 | Caserta | 7.17 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 98 | Parma | 7.94 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 99 | Luxembourg City | 9.48 | 64,851 | 10 | 5 | 2 | 18 | 20 | measured |
| 100 | Tampa | 14.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 101 | Bordeaux | 9.22 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 102 | Tallinn | 9.22 | 124,888 | 9 | 3 | 2 | 42 | 20 | measured |
| 103 | Cincinnati | 13.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 104 | Budapest | 12.55 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 105 | Lansing | 13.02 | - | - | - | - | - | 10 | predicted (travel demand) |
| 106 | Madrid | 7.94 | 274,553 | 17 | 11 | 2 | - | 20 | measured |
| 107 | Hawaii | 11.27 | - | 6 | - | 1 | 6 | 30 | measured |
| 108 | Detroit | 12.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 109 | Amersfoort | 6.15 | - | 14 | 1 | 2 | 181 | 20 | measured |
| 110 | Sorrento | 6.15 | 40,049 | 7 | - | 1 | 20 | 20 | measured |
| 111 | Istanbul | 10.76 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 112 | Denver | 11.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 113 | Hilo | 8.71 | - | 6 | - | 1 | 16 | 20 | measured |
| 114 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 115 | San Jose | 11.39 | - | - | - | - | - | 10 | predicted (travel demand) |
| 116 | Sacramento | 11.32 | - | - | - | - | - | 10 | predicted (travel demand) |
| 117 | Jersey City | 10.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 118 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 119 | Menorca | 7.17 | - | 6 | - | - | 2 | 20 | measured |
| 120 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 121 | Cambridge | 10.76 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 122 | Trento | 5.38 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 123 | Milwaukee | 10.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 124 | Crete | 10.50 | - | 4 | 3 | - | - | 20 | measured |
| 125 | Salt Lake City | 10.31 | - | - | - | - | - | 10 | predicted (travel demand) |
| 126 | Atlanta | 10.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 127 | Anchorage | 10.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 128 | Washington DC | 9.22 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 129 | Raleigh | 10.07 | - | - | - | - | - | 10 | predicted (travel demand) |
| 130 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 131 | Sydney | 9.74 | 305,304 | 7 | 1 | - | - | 30 | measured |
| 132 | Cleveland | 9.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 133 | El Paso | 9.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 134 | Seoul | 8.97 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 135 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 136 | Glasgow | 8.97 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 137 | Miami | 9.48 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 138 | Segovia | 5.89 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 139 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 140 | Leipzig | 6.15 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 141 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 142 | Nashville | 8.93 | - | - | - | - | - | 10 | predicted (travel demand) |
| 143 | Lyon | 5.89 | 136,951 | 13 | 4 | 1 | 156 | 20 | measured |
| 144 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 145 | Zwolle | 4.36 | - | 16 | - | 2 | 56 | 20 | measured |
| 146 | Montreal | 8.71 | 315,322 | 11 | - | 2 | - | 30 | measured |
| 147 | Bari | 5.12 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 148 | Bologna | 4.61 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 149 | Ann Arbor | 8.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 150 | Coimbra | 4.61 | 34,962 | 4 | - | - | 5 | 20 | measured |
| 151 | Nuremberg | 5.64 | 161,614 | 12 | 1 | 1 | 38 | 20 | measured |
| 152 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 153 | Girona | 4.87 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 154 | Eindhoven | 4.10 | - | 16 | - | 4 | 195 | 20 | measured |
| 155 | Heerlen | 4.10 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 156 | Ibiza | 5.12 | - | 1 | - | - | 4 | 20 | measured |
| 157 | Hong Kong | 5.38 | 689,212 | 10 | 4 | 1 | 505 | 20 | measured |
| 158 | Albuquerque | 7.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 159 | Padua | 4.10 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 160 | Venlo | 3.84 | - | 7 | - | 1 | 144 | 20 | measured |
| 161 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 162 | Helsinki | 5.89 | 148,908 | 12 | 2 | 1 | 13 | 30 | measured |
| 163 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 164 | Hobart | 4.87 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 165 | Como | 3.59 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 166 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 167 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 168 | Salzburg | 4.61 | 107,243 | 9 | 3 | 2 | 34 | 20 | measured |
| 169 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 170 | Apeldoorn | 3.33 | - | 10 | - | 2 | 80 | 20 | measured |
| 171 | San Diego | 6.66 | 214,939 | 4 | 1 | 1 | - | 20 | measured |
| 172 | Turin | 3.33 | 147,456 | 11 | 7 | 2 | 30 | 20 | measured |
| 173 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 174 | Stockholm | 5.12 | 188,184 | 6 | 4 | - | - | 30 | measured |
| 175 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 176 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 177 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 178 | Warsaw | 4.10 | 197,929 | 39 | 3 | 4 | 1407 | 30 | measured |
| 179 | Deventer | 3.07 | - | 12 | - | 1 | 213 | 20 | measured |
| 180 | Kamakura | 3.84 | 33,492 | 6 | - | - | - | 20 | measured |
| 181 | Zurich | 5.89 | 140,788 | 6 | - | - | - | 20 | measured |
| 182 | Pamplona | 3.84 | 128,065 | 6 | - | - | 1 | 20 | measured |
| 183 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 184 | Ljubljana | 5.64 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 185 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 186 | Alkmaar | 2.82 | - | 7 | - | 1 | 79 | 20 | measured |
| 187 | Groningen | 2.82 | 31,401 | 21 | 1 | 2 | 76 | 20 | measured |
| 188 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 189 | Vancouver | 5.38 | 351,552 | 4 | - | - | - | 30 | measured |
| 190 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 191 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 192 | Spokane | 3.92 | - | 13 | - | 2 | 18 | 10 | published, never ranked (may be uncrawled) |
| 193 | Stuttgart | 4.10 | 112,789 | 6 | 1 | - | - | 20 | measured |
| 194 | Bratislava | 3.59 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 195 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 196 | Kauai | 4.61 | - | 6 | 1 | - | 8 | 20 | measured |
| 197 | Perugia | 2.82 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 198 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 199 | Santa Fe | 5.17 | - | - | - | - | - | 10 | predicted (travel demand) |
| 200 | Hamburg | 4.87 | 191,221 | 6 | 1 | 1 | - | 30 | measured |
| 201 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 202 | Braga | 2.82 | 34,522 | 4 | 2 | - | 8 | 20 | measured |
| 203 | Bangkok | 5.12 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 204 | Bristol | 5.12 | 163,983 | 6 | 2 | - | - | 20 | measured |
| 205 | Maastricht | 2.56 | 47,763 | 19 | - | 2 | 135 | 20 | measured |
| 206 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 207 | Nagoya | 3.33 | 83,437 | 6 | 1 | - | 1 | 20 | measured |
| 208 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 209 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 210 | Guimaraes | 2.56 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 211 | Maui | 4.61 | - | 4 | - | - | 3 | 20 | measured |
| 212 | Belfast | 4.87 | 224,315 | 4 | - | 1 | - | 20 | measured |
| 213 | Rio de Janeiro | 4.87 | 279,431 | 6 | - | - | - | 30 | measured |
| 214 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 215 | Verona | 2.82 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 216 | Riga | 4.61 | 108,918 | 5 | 2 | - | - | 20 | measured |
| 217 | Genoa | 2.56 | 145,206 | 13 | 2 | 1 | 10 | 20 | measured |
| 218 | Beijing | 4.61 | 269,737 | 7 | 1 | - | - | 30 | measured |
| 219 | Hiroshima | 3.07 | 129,791 | 17 | 5 | 3 | - | 20 | measured |
| 220 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 221 | Toronto | 4.36 | 411,011 | 6 | - | - | - | 30 | measured |
| 222 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 223 | Catania | 2.56 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 224 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 225 | Quebec City | 2.82 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 226 | Toulouse | 2.82 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 227 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 228 | Hilversum | 2.05 | - | 6 | 1 | 1 | 122 | 20 | measured |
| 229 | Naples | 2.05 | 198,913 | 24 | 3 | 3 | 46 | 20 | measured |
| 230 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 231 | Mexico City | 3.84 | 566,583 | 9 | 2 | - | - | 30 | measured |
| 232 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 233 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 234 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 235 | Brno | 2.56 | 63,714 | 8 | 5 | 2 | 34 | 20 | measured |
| 236 | Graz | 2.56 | 65,717 | 12 | 7 | 1 | 87 | 20 | measured |
| 237 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 238 | Dubrovnik | 3.59 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 239 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 240 | Heidelberg | 3.33 | 75,837 | 6 | 1 | 1 | - | 20 | measured |
| 241 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 242 | Aarhus | 3.59 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 243 | Liverpool | 3.59 | 248,189 | 2 | 1 | - | - | 20 | measured |
| 244 | Savannah | 3.59 | 128,162 | 2 | 1 | - | - | 20 | measured |
| 245 | Bergamo | 1.79 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 246 | Den Bosch | 1.79 | 39,682 | 12 | 2 | 1 | 118 | 20 | measured |
| 247 | Kanazawa | 2.31 | 25,778 | 7 | 2 | 1 | 2 | 20 | measured |
| 248 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 249 | Sapporo | 2.31 | 88,633 | 6 | - | - | - | 20 | measured |
| 250 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 251 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 252 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 253 | Taipei | 3.33 | 143,193 | 4 | 1 | - | - | 30 | measured |
| 254 | San Antonio | 3.32 | - | 4 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 255 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 256 | Fort Worth | 3.28 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 257 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 258 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 259 | Charleston | 3.07 | 155,987 | 2 | 1 | - | - | 20 | measured |
| 260 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 261 | Assen | 1.54 | - | 10 | - | 2 | 66 | 20 | measured |
| 262 | Delft | 1.54 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 263 | Rotterdam | 1.54 | 104,938 | 12 | - | 2 | 83 | 20 | measured |
| 264 | Buenos Aires | 2.95 | 333,331 | 4 | 2 | - | - | 30 | measured |
| 265 | Dresden | 2.05 | 113,624 | 5 | 5 | 1 | - | 20 | measured |
| 266 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 267 | Manchester | 3.07 | 316,438 | 5 | - | - | - | 30 | measured |
| 268 | Potsdam | 2.05 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 269 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 270 | Matera | 1.79 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 271 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 272 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 273 | Yakushima | 1.79 | - | 1 | - | - | 1 | 20 | measured |
| 274 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 275 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 276 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 277 | Ghent | 2.56 | 82,757 | 8 | 1 | 1 | - | 20 | measured |
| 278 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 279 | Oxford | 2.56 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 280 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 281 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 282 | Monterey | 2.56 | - | 3 | - | - | - | 20 | measured |
| 283 | Thessaloniki | 2.56 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 284 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 285 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 286 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 287 | Belgrade | 2.43 | 178,116 | 5 | 5 | - | - | 20 | measured |
| 288 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 289 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 290 | Pisa | 1.54 | 52,174 | 4 | - | 1 | - | 20 | measured |
| 291 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 292 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 293 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 294 | Naha | 1.54 | 24,466 | 6 | - | - | 1 | 20 | measured |
| 295 | Zaragoza | 1.54 | 87,580 | 7 | - | 1 | - | 20 | measured |
| 296 | Cologne | 2.31 | 191,812 | 5 | - | 1 | - | 30 | measured |
| 297 | Canberra | 2.28 | - | 1 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 298 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 299 | Tarragona | 1.28 | 32,396 | 4 | 2 | - | - | 20 | measured |
| 300 | Pittsburgh | 2.05 | - | 4 | - | 1 | - | 20 | measured |
| 301 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 302 | Minneapolis | 2.05 | - | 4 | - | - | - | 20 | measured |
| 303 | Breda | 1.02 | 36,579 | 10 | - | 2 | 118 | 20 | measured |
| 304 | Trieste | 1.02 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 305 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 306 | Regensburg | 1.79 | 51,930 | 5 | - | 1 | 4 | 20 | measured |
| 307 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 308 | Gdansk | 1.28 | 4,908 | 12 | 4 | 1 | 307 | 20 | measured |
| 309 | Setubal | 1.02 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 310 | Bucharest | 1.84 | 136,836 | 4 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 311 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 312 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 313 | Bruges | 1.79 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 314 | York | 1.79 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 315 | Ferrara | 1.02 | 27,490 | 5 | 3 | 1 | 7 | 20 | measured |
| 316 | Ronda | 1.02 | 51,510 | 6 | 1 | - | 9 | 20 | measured |
| 317 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 318 | Rouen | 1.54 | 72,334 | 12 | - | 1 | 6 | 20 | measured |
| 319 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 320 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 321 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 322 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 323 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 324 | Baltimore | 1.54 | - | 4 | - | - | - | 20 | measured |
| 325 | Fort Lauderdale | 1.54 | - | 4 | - | - | - | 30 | measured |
| 326 | Kansas City | 1.54 | - | 4 | - | 1 | - | 30 | measured |
| 327 | Lucca | 0.77 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 328 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 329 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 330 | Auckland | 1.28 | 152,056 | 5 | 2 | - | - | 20 | measured |
| 331 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 332 | Lausanne | 1.28 | 68,242 | 8 | 1 | 1 | - | 20 | measured |
| 333 | Leuven | 1.28 | 40,645 | 4 | - | - | - | 20 | measured |
| 334 | Modena | 0.77 | 51,698 | 5 | 1 | 1 | 3 | 20 | measured |
| 335 | Split | 1.28 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 336 | Antwerp | 1.26 | 128,289 | 10 | 4 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 337 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 338 | Assisi | 0.77 | 30,278 | 6 | 1 | 2 | 6 | 20 | measured |
| 339 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 340 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 341 | Salamanca | 0.77 | 47,897 | 4 | - | 1 | 1 | 20 | measured |
| 342 | Bilbao | 0.77 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 343 | Cesky Krumlov | 0.77 | 28,582 | 6 | 3 | - | 11 | 20 | measured |
| 344 | Poznan | 0.77 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 345 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 346 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 347 | Boise | 1.02 | - | 4 | - | 1 | - | 30 | measured |
| 348 | Gothenburg | 1.02 | 119,991 | 5 | - | 1 | - | 20 | measured |
| 349 | Roosendaal | 0.51 | - | 8 | - | 1 | 116 | 20 | measured |
| 350 | Tulsa | 1.02 | - | 1 | - | - | - | 20 | measured |
| 351 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 352 | Busan | 0.83 | 94,737 | 2 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 353 | Frankfurt | 0.51 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 354 | Sofia | 0.51 | 138,710 | 4 | - | - | - | 30 | measured |
| 355 | Wroclaw | 0.51 | 123,894 | 5 | 1 | 1 | 121 | 20 | measured |
| 356 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 357 | Hallstatt | 0.51 | 47,271 | 5 | 1 | - | - | 20 | measured |
| 358 | Phoenix | 0.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 359 | Cardiff | 0.51 | - | 4 | - | 1 | - | 20 | measured |
| 360 | Indianapolis | 0.51 | - | 1 | - | - | - | 30 | measured |
| 361 | Brighton | 0.51 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 362 | Turku | 0.51 | - | 1 | - | - | - | 30 | measured |
| 363 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 364 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 365 | Bamberg | 0.26 | 28,716 | 5 | 4 | 1 | 10 | 20 | measured |
| 366 | Rothenburg ob der Tauber | 0.26 | 39,879 | 4 | - | 1 | 8 | 20 | measured |
| 367 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 368 | George Town | 0.28 | 36,080 | - | - | - | - | 10 | predicted (travel demand) |
| 369 | Freiburg | 0.26 | 92,752 | 7 | 2 | 1 | - | 20 | measured |
| 370 | Sao Paulo | 0.26 | 911 | 1 | - | - | - | 20 | measured |
| 371 | Nantes | 0.26 | 67,689 | 1 | 1 | - | - | 20 | measured |
| 372 | Allentown | 0.24 | - | - | - | - | - | 10 | predicted (travel demand) |
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

