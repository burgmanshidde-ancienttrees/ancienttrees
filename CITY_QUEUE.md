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
| 1 | Brussels | 171.10 | 176,863 | 35 | 4 | 2 | 436 | 30 | measured |
| 2 | Lisbon | 84.36 | 201,877 | 36 | 16 | 3 | 67 | 30 | measured |
| 3 | Milan | 83.65 | 212,705 | 30 | 12 | 3 | 25 | 30 | measured |
| 4 | Barcelona | 77.71 | 346,477 | 56 | 14 | 7 | 180 | 30 | measured |
| 5 | Pamplona | 86.74 | 128,065 | 14 | - | 1 | 9 | 20 | measured |
| 6 | Amsterdam | 69.15 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 7 | Oahu | 82.70 | - | 21 | 2 | 3 | 163 | 20 | measured |
| 8 | Rome | 61.07 | 358,876 | 31 | 10 | 2 | 32 | 30 | measured |
| 9 | Florence | 48.48 | 184,099 | 27 | 9 | 1 | 27 | 30 | measured |
| 10 | Tenerife | 61.07 | - | 4 | 2 | - | - | 20 | measured |
| 11 | Singapore | 56.56 | 967,821 | 34 | 6 | 3 | 165 | 30 | measured |
| 12 | Palermo | 41.35 | 124,310 | 21 | 9 | 1 | 37 | 20 | measured |
| 13 | Seville | 52.28 | 170,545 | 43 | 9 | 2 | - | 20 | measured |
| 14 | Arnhem | 39.69 | 31,478 | 39 | 3 | 3 | 204 | 20 | measured |
| 15 | Berlin | 44.44 | 412,181 | 33 | 23 | 3 | 195 | 30 | measured |
| 16 | Brisbane | 42.30 | 162,602 | 20 | 2 | 2 | 186 | 30 | measured |
| 17 | Los Angeles | 60.36 | 665,559 | 8 | 2 | - | - | 30 | measured |
| 18 | Tokyo | 32.79 | 394,702 | 21 | 10 | 1 | 5 | 20 | measured |
| 19 | Paris | 39.21 | 524,268 | 31 | 9 | 4 | 129 | 30 | measured |
| 20 | Valencia | 29.23 | 162,209 | 31 | 4 | 2 | 350 | 30 | measured |
| 21 | Vienna | 37.79 | 283,090 | 32 | 18 | 5 | 376 | 30 | measured |
| 22 | Alicante | 27.57 | 77,454 | 21 | 4 | 2 | 44 | 20 | measured |
| 23 | London | 46.58 | 718,291 | 23 | 14 | 1 | - | 30 | measured |
| 24 | Prague | 35.65 | 303,350 | 30 | 21 | 4 | 31 | 30 | measured |
| 25 | Malaga | 34.70 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 26 | Philadelphia | 40.40 | 405,294 | 1 | - | - | - | 20 | measured |
| 27 | New York | 35.17 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 28 | Dublin | 21.86 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 29 | Birmingham | 37.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 30 | Krakow | 24.24 | 140,824 | 38 | 8 | 3 | 198 | 30 | measured |
| 31 | Portland | 24.24 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 32 | Haarlem | 18.06 | 33,960 | 21 | 1 | 2 | 277 | 20 | measured |
| 33 | Boston | 34.22 | 385,902 | 11 | 2 | 1 | - | 30 | measured |
| 34 | Vilnius | 23.29 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 35 | Austin | 34.70 | 226,631 | 5 | 2 | - | - | 20 | measured |
| 36 | Copenhagen | 31.84 | 218,621 | 16 | 2 | 2 | - | 30 | measured |
| 37 | Dallas | 33.27 | - | 9 | 1 | 1 | - | 30 | measured |
| 38 | Cork | 21.63 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 39 | Leiden | 16.16 | 33,227 | 20 | 6 | 1 | 129 | 20 | measured |
| 40 | The Hague | 16.16 | 236,723 | 31 | 2 | 5 | 167 | 20 | measured |
| 41 | Madeira | 18.77 | - | 10 | 1 | 1 | - | 20 | measured |
| 42 | Houston | 30.89 | - | 4 | - | - | - | 30 | measured |
| 43 | Porto | 15.21 | 120,415 | 27 | 15 | 2 | 40 | 20 | measured |
| 44 | Kyoto | 19.49 | 142,353 | 18 | 12 | 2 | - | 20 | measured |
| 45 | Bath | 29.47 | 144,950 | 5 | 2 | 1 | - | 20 | measured |
| 46 | Nijmegen | 14.73 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 47 | Ottawa | 19.01 | - | 21 | - | 3 | 122 | 20 | measured |
| 48 | Reykjavik | 24.48 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 49 | Munich | 18.77 | 224,067 | 45 | 15 | 6 | 80 | 30 | measured |
| 50 | Helmond | 14.02 | - | 18 | - | 2 | 55 | 20 | measured |
| 51 | Utrecht | 13.78 | 67,963 | 27 | 7 | 2 | 340 | 20 | measured |
| 52 | Sintra | 13.55 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 53 | New Orleans | 27.09 | 256,232 | 4 | 2 | 1 | - | 20 | measured |
| 54 | Geneva | 17.82 | 162,269 | 21 | 5 | 4 | 131 | 20 | measured |
| 55 | Granada | 16.87 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 56 | Palma de Mallorca | 15.45 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 57 | Venice | 14.02 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 58 | Fukuoka | 16.40 | 77,485 | 15 | 9 | 1 | - | 20 | measured |
| 59 | Las Vegas | 24.24 | - | 11 | - | 2 | - | 30 | measured |
| 60 | Cordoba | 14.73 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 61 | Jacksonville | 22.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 62 | Cadiz | 14.50 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 63 | Leeuwarden | 10.46 | - | 41 | - | 2 | 61 | 20 | measured |
| 64 | Asheville | 20.89 | - | - | - | - | - | 10 | predicted (travel demand) |
| 65 | Long Beach | 20.48 | - | - | - | - | - | 10 | predicted (travel demand) |
| 66 | Dordrecht | 10.22 | - | 20 | 1 | 2 | 105 | 20 | measured |
| 67 | Little Rock | 20.40 | - | - | - | - | - | 10 | predicted (travel demand) |
| 68 | Edinburgh | 19.72 | 292,981 | 16 | 5 | 1 | - | 30 | measured |
| 69 | Oslo | 17.59 | 181,113 | 4 | - | - | - | 20 | measured |
| 70 | San Francisco | 19.01 | 361,111 | 6 | 1 | 1 | - | 30 | measured |
| 71 | Sardinia | 10.69 | - | 5 | 4 | - | 8 | 20 | measured |
| 72 | Cagliari | 10.22 | 51,351 | 14 | 1 | 2 | 15 | 20 | measured |
| 73 | Nice | 19.01 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 74 | Oakland | 18.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 75 | Seattle | 18.06 | 398,724 | 6 | 1 | - | - | 30 | measured |
| 76 | Athens | 18.06 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 77 | Lexington | 18.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 78 | Reno | 18.19 | - | - | - | - | - | 10 | predicted (travel demand) |
| 79 | Des Moines | 18.11 | - | - | - | - | - | 10 | predicted (travel demand) |
| 80 | Daytona Beach | 17.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 81 | Chicago | 17.59 | 485,769 | 6 | - | - | - | 30 | measured |
| 82 | Melbourne | 11.64 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 83 | Tilburg | 8.56 | - | 20 | - | 3 | 87 | 20 | measured |
| 84 | Strasbourg | 11.17 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 85 | Chattanooga | 16.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 86 | Osaka | 10.69 | 163,112 | 6 | 1 | - | - | 30 | measured |
| 87 | Perth | 16.16 | 180,478 | 6 | 3 | 1 | - | 30 | measured |
| 88 | Madrid | 9.98 | 274,553 | 17 | 11 | 2 | - | 20 | measured |
| 89 | Caserta | 8.08 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 90 | Enschede | 8.08 | - | 13 | 1 | 1 | 82 | 20 | measured |
| 91 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 92 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 93 | Huntsville | 15.35 | - | - | - | - | - | 10 | predicted (travel demand) |
| 94 | Cyprus | 14.97 | - | 4 | - | - | - | 20 | measured |
| 95 | Hoorn | 7.60 | - | 8 | - | 1 | 52 | 20 | measured |
| 96 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 97 | West Palm Beach | 14.98 | - | - | - | - | - | 10 | predicted (travel demand) |
| 98 | Saint Petersburg | 14.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 99 | St. Louis | 14.80 | - | - | - | - | - | 10 | predicted (travel demand) |
| 100 | Bordeaux | 9.74 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 101 | Coimbra | 7.84 | 34,962 | 4 | - | - | 5 | 20 | measured |
| 102 | Tampa | 14.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 103 | Cincinnati | 13.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 104 | Hawaii | 11.88 | - | 6 | - | 1 | 6 | 30 | measured |
| 105 | Lansing | 13.02 | - | - | - | - | - | 10 | predicted (travel demand) |
| 106 | Tallinn | 8.56 | 124,888 | 9 | 3 | 2 | 42 | 20 | measured |
| 107 | Detroit | 12.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 108 | Istanbul | 10.34 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 109 | Denver | 11.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 110 | Cambridge | 11.64 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 111 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 112 | Eindhoven | 5.70 | - | 16 | - | 4 | 195 | 20 | measured |
| 113 | San Jose | 11.39 | - | - | - | - | - | 10 | predicted (travel demand) |
| 114 | Glasgow | 10.69 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 115 | Sacramento | 11.32 | - | - | - | - | - | 10 | predicted (travel demand) |
| 116 | Jersey City | 10.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 117 | Ibiza | 7.13 | - | 1 | - | - | 4 | 20 | measured |
| 118 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 119 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 120 | Sorrento | 5.47 | 40,049 | 7 | - | 1 | 20 | 20 | measured |
| 121 | Milwaukee | 10.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 122 | Menorca | 6.89 | - | 6 | - | - | 2 | 20 | measured |
| 123 | Crete | 10.46 | - | 4 | 3 | - | - | 20 | measured |
| 124 | Monterey | 10.46 | - | 3 | 1 | - | - | 20 | measured |
| 125 | Washington DC | 9.51 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 126 | Salt Lake City | 10.31 | - | - | - | - | - | 10 | predicted (travel demand) |
| 127 | Atlanta | 10.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 128 | Seoul | 9.51 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 129 | Parma | 5.70 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 130 | Anchorage | 10.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 131 | Raleigh | 10.07 | - | - | - | - | - | 10 | predicted (travel demand) |
| 132 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 133 | Sydney | 9.74 | 305,304 | 7 | 1 | - | - | 30 | measured |
| 134 | Budapest | 9.51 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 135 | Cleveland | 9.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 136 | El Paso | 9.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 137 | Leipzig | 6.42 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 138 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 139 | Bari | 5.70 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 140 | Amersfoort | 4.75 | - | 18 | 1 | 2 | 181 | 20 | measured |
| 141 | Miami | 9.48 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 142 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 143 | Luxembourg City | 6.18 | 64,851 | 10 | 5 | 2 | 18 | 20 | measured |
| 144 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 145 | Segovia | 5.70 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 146 | Como | 4.52 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 147 | Groningen | 4.52 | 31,401 | 21 | 1 | 2 | 76 | 20 | measured |
| 148 | Helsinki | 7.13 | 148,908 | 12 | 2 | 1 | 13 | 30 | measured |
| 149 | Nashville | 8.93 | - | - | - | - | - | 10 | predicted (travel demand) |
| 150 | Zurich | 8.56 | 140,788 | 6 | - | - | - | 20 | measured |
| 151 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 152 | Ann Arbor | 8.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 153 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 154 | Hobart | 5.47 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 155 | Padua | 4.28 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 156 | Perugia | 4.28 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 157 | Warsaw | 5.23 | 197,929 | 39 | 5 | 4 | 1407 | 30 | measured |
| 158 | Albuquerque | 7.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 159 | Ljubljana | 7.60 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 160 | Heerlen | 3.80 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 161 | Zwolle | 3.80 | - | 16 | - | 2 | 56 | 20 | measured |
| 162 | Hong Kong | 4.99 | 689,212 | 10 | 4 | 1 | 505 | 20 | measured |
| 163 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 164 | Salzburg | 4.99 | 107,243 | 9 | 3 | 2 | 34 | 20 | measured |
| 165 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 166 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 167 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 168 | Hilo | 5.23 | - | 6 | - | 1 | 16 | 20 | measured |
| 169 | Charleston | 6.65 | 155,987 | 2 | 1 | - | - | 20 | measured |
| 170 | Lyon | 4.52 | 136,951 | 13 | 4 | 1 | 156 | 20 | measured |
| 171 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 172 | Bangkok | 6.77 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 173 | Trento | 3.33 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 174 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 175 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 176 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 177 | Yakushima | 4.04 | - | 1 | - | - | 1 | 20 | measured |
| 178 | Vancouver | 6.18 | 351,552 | 4 | - | - | - | 30 | measured |
| 179 | Stockholm | 4.99 | 188,184 | 6 | 4 | - | - | 30 | measured |
| 180 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 181 | Montreal | 6.18 | 315,322 | 13 | 1 | 2 | - | 30 | measured |
| 182 | San Diego | 6.18 | 214,939 | 4 | 1 | 1 | - | 20 | measured |
| 183 | Savannah | 6.18 | 128,162 | 2 | 1 | - | - | 20 | measured |
| 184 | Turin | 3.09 | 147,456 | 11 | 7 | 2 | 30 | 20 | measured |
| 185 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 186 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 187 | Alkmaar | 2.85 | - | 7 | - | 1 | 79 | 20 | measured |
| 188 | Apeldoorn | 2.85 | - | 10 | - | 2 | 80 | 20 | measured |
| 189 | Nuremberg | 3.80 | 161,614 | 12 | 1 | 1 | 38 | 20 | measured |
| 190 | Girona | 3.33 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 191 | Genoa | 3.09 | 145,206 | 13 | 2 | 1 | 10 | 20 | measured |
| 192 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 193 | Hamburg | 5.23 | 191,221 | 6 | 1 | 1 | - | 30 | measured |
| 194 | Beijing | 5.47 | 269,737 | 7 | 1 | - | - | 30 | measured |
| 195 | Bristol | 5.47 | 163,983 | 6 | 2 | - | - | 20 | measured |
| 196 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 197 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 198 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 199 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 200 | Deventer | 2.61 | - | 12 | - | 1 | 213 | 20 | measured |
| 201 | Maastricht | 2.61 | 47,763 | 19 | - | 2 | 135 | 20 | measured |
| 202 | Santa Fe | 5.17 | - | - | - | - | - | 10 | predicted (travel demand) |
| 203 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 204 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 205 | Maui | 4.75 | - | 4 | - | - | 3 | 20 | measured |
| 206 | Graz | 3.33 | 65,717 | 12 | 7 | 1 | 87 | 20 | measured |
| 207 | Belfast | 4.99 | 224,315 | 4 | - | 1 | - | 20 | measured |
| 208 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 209 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 210 | Bologna | 2.61 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 211 | Catania | 2.85 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 212 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 213 | Verona | 2.85 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 214 | Naples | 2.38 | 198,913 | 24 | 3 | 3 | 46 | 20 | measured |
| 215 | Toronto | 4.52 | 411,011 | 6 | - | - | - | 30 | measured |
| 216 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 217 | Split | 4.52 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 218 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 219 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 220 | Assen | 2.14 | - | 10 | - | 2 | 66 | 20 | measured |
| 221 | Boise | 4.28 | - | 4 | - | 1 | - | 30 | measured |
| 222 | Hilversum | 2.14 | - | 6 | 1 | 1 | 122 | 20 | measured |
| 223 | Taipei | 4.28 | 143,193 | 4 | 1 | - | - | 30 | measured |
| 224 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 225 | Rio de Janeiro | 4.16 | 279,431 | 6 | - | - | - | 30 | measured |
| 226 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 227 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 228 | Kanazawa | 2.61 | 25,778 | 7 | 2 | 1 | 2 | 20 | measured |
| 229 | Pisa | 2.61 | 52,174 | 4 | - | 1 | - | 20 | measured |
| 230 | Heidelberg | 3.56 | 75,837 | 6 | 1 | 1 | - | 20 | measured |
| 231 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 232 | Belgrade | 3.92 | 178,116 | 5 | 5 | - | - | 20 | measured |
| 233 | Dresden | 2.61 | 113,624 | 5 | 5 | 1 | - | 20 | measured |
| 234 | Kauai | 3.33 | - | 6 | 1 | - | 8 | 20 | measured |
| 235 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 236 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 237 | Kamakura | 2.38 | 33,492 | 6 | - | - | - | 20 | measured |
| 238 | Den Bosch | 1.90 | 39,682 | 12 | 2 | 1 | 118 | 20 | measured |
| 239 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 240 | Rotterdam | 1.90 | 104,938 | 12 | - | 2 | 83 | 20 | measured |
| 241 | Venlo | 1.90 | - | 7 | - | 1 | 144 | 20 | measured |
| 242 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 243 | Mexico City | 3.45 | 566,583 | 9 | 2 | - | - | 30 | measured |
| 244 | Guimaraes | 1.90 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 245 | Riga | 3.56 | 108,918 | 5 | 2 | - | - | 20 | measured |
| 246 | Matera | 2.14 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 247 | Bratislava | 2.38 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 248 | Brno | 2.38 | 63,714 | 8 | 5 | 2 | 34 | 20 | measured |
| 249 | Quebec City | 2.38 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 250 | Sapporo | 2.38 | 88,633 | 6 | - | - | - | 20 | measured |
| 251 | Dubrovnik | 3.33 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 252 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 253 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 254 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 255 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 256 | Fort Lauderdale | 3.33 | - | 4 | - | - | - | 30 | measured |
| 257 | Liverpool | 3.33 | 248,189 | 2 | 1 | - | - | 20 | measured |
| 258 | Bergamo | 1.66 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 259 | Delft | 1.66 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 260 | San Antonio | 3.32 | - | 4 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 261 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 262 | Fort Worth | 3.28 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 263 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 264 | Oxford | 3.09 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 265 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 266 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 267 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 268 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 269 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 270 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 271 | Aarhus | 2.85 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 272 | Ferrara | 1.66 | 27,490 | 5 | 3 | 1 | 7 | 20 | measured |
| 273 | Nagoya | 1.90 | 83,437 | 6 | 1 | - | 1 | 20 | measured |
| 274 | Hiroshima | 1.90 | 129,791 | 17 | 5 | 3 | - | 20 | measured |
| 275 | Toulouse | 1.90 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 276 | Buenos Aires | 2.73 | 333,331 | 4 | 2 | - | - | 30 | measured |
| 277 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 278 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 279 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 280 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 281 | Cologne | 2.61 | 191,812 | 5 | - | 1 | - | 30 | measured |
| 282 | York | 2.61 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 283 | Braga | 1.43 | 34,522 | 4 | 2 | - | 8 | 20 | measured |
| 284 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 285 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 286 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 287 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 288 | Potsdam | 1.66 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 289 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 290 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 291 | Pittsburgh | 2.38 | - | 4 | - | 1 | - | 20 | measured |
| 292 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 293 | Lucca | 1.19 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 294 | Thessaloniki | 2.38 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 295 | Trieste | 1.19 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 296 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 297 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 298 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 299 | Regensburg | 2.14 | 51,930 | 5 | 1 | 1 | 4 | 20 | measured |
| 300 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 301 | Salamanca | 1.43 | 47,897 | 4 | - | 1 | 1 | 20 | measured |
| 302 | Zaragoza | 1.43 | 87,580 | 7 | - | 1 | - | 20 | measured |
| 303 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 304 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 305 | Spokane | 1.43 | - | 13 | - | 2 | 18 | 20 | measured |
| 306 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 307 | Baltimore | 1.90 | - | 4 | - | - | - | 20 | measured |
| 308 | Breda | 0.95 | 36,579 | 10 | - | 2 | 118 | 20 | measured |
| 309 | Kansas City | 1.90 | - | 4 | - | 1 | - | 30 | measured |
| 310 | Lausanne | 1.90 | 68,242 | 8 | 1 | 1 | - | 20 | measured |
| 311 | Minneapolis | 1.90 | - | 4 | - | - | - | 20 | measured |
| 312 | Roosendaal | 0.95 | - | 8 | - | 1 | 116 | 20 | measured |
| 313 | Bucharest | 1.84 | 136,836 | 4 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 314 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 315 | Naha | 1.19 | 24,466 | 6 | - | - | 1 | 20 | measured |
| 316 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 317 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 318 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 319 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 320 | Cardiff | 1.66 | - | 4 | - | 1 | - | 20 | measured |
| 321 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 322 | Hallstatt | 1.43 | 47,271 | 5 | 1 | - | - | 20 | measured |
| 323 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 324 | Ronda | 0.95 | 51,510 | 6 | 1 | - | 9 | 20 | measured |
| 325 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 326 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 327 | Gothenburg | 1.49 | 119,991 | 5 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 328 | Auckland | 1.43 | 152,056 | 5 | 2 | - | - | 20 | measured |
| 329 | Brighton | 1.43 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 330 | Nantes | 1.43 | 67,689 | 1 | 1 | - | - | 20 | measured |
| 331 | Frankfurt | 0.95 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 332 | Gdansk | 0.95 | 4,908 | 12 | 4 | 1 | 307 | 20 | measured |
| 333 | Setubal | 0.71 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 334 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 335 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 336 | Antwerp | 1.26 | 128,289 | 10 | 4 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 337 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 338 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 339 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 340 | Leuven | 1.19 | 40,645 | 4 | - | - | - | 20 | measured |
| 341 | Tarragona | 0.71 | 32,396 | 4 | 2 | - | - | 20 | measured |
| 342 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 343 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 344 | Wroclaw | 0.71 | 123,894 | 5 | 1 | 1 | 121 | 20 | measured |
| 345 | Freiburg | 0.95 | 92,752 | 7 | 2 | 1 | - | 20 | measured |
| 346 | Ghent | 0.95 | 82,757 | 8 | 1 | 1 | - | 20 | measured |
| 347 | Indianapolis | 0.95 | - | 1 | - | - | - | 30 | measured |
| 348 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 349 | Tulsa | 0.95 | - | 1 | - | - | - | 20 | measured |
| 350 | Stuttgart | 0.71 | 112,789 | 6 | 1 | - | - | 20 | measured |
| 351 | Rothenburg ob der Tauber | 0.71 | 39,879 | 4 | - | 1 | 8 | 20 | measured |
| 352 | Assisi | 0.48 | 30,278 | 6 | 1 | 2 | 6 | 20 | measured |
| 353 | Bilbao | 0.48 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 354 | Poznan | 0.48 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 355 | Sofia | 0.48 | 138,710 | 4 | - | - | - | 30 | measured |
| 356 | Sao Paulo | 0.59 | 911 | 1 | - | - | - | 20 | measured |
| 357 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 358 | Phoenix | 0.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 359 | Rouen | 0.48 | 72,334 | 12 | - | 1 | 6 | 20 | measured |
| 360 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 361 | Busan | 0.48 | 94,737 | 2 | - | - | - | 20 | measured |
| 362 | Canberra | 0.48 | - | 1 | 1 | - | - | 30 | measured |
| 363 | Manchester | 0.48 | 316,438 | 5 | - | - | - | 30 | measured |
| 364 | Turku | 0.48 | - | 1 | - | - | - | 30 | measured |
| 365 | Modena | 0.24 | 51,698 | 5 | 1 | 1 | 3 | 20 | measured |
| 366 | Cesky Krumlov | 0.24 | 28,582 | 6 | 3 | - | 11 | 20 | measured |
| 367 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 368 | Bamberg | 0.24 | 28,716 | 5 | 4 | 1 | 10 | 20 | measured |
| 369 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 370 | George Town | 0.28 | 36,080 | - | - | - | - | 10 | predicted (travel demand) |
| 371 | Allentown | 0.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 372 | Bruges | 0.24 | 106,902 | 4 | - | 1 | - | 20 | measured |
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

