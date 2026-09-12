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
| 1 | Rome | 119.46 | 358,876 | 31 | 9 | 2 | 32 | 30 | measured |
| 2 | Brussels | 138.22 | 176,863 | 31 | 4 | 1 | 436 | 30 | measured |
| 3 | Milan | 90.73 | 212,705 | 24 | 11 | 3 | 25 | 30 | measured |
| 4 | Lisbon | 88.11 | 201,877 | 35 | 16 | 3 | 68 | 30 | measured |
| 5 | Barcelona | 81.70 | 346,477 | 56 | 13 | 7 | 180 | 30 | measured |
| 6 | Amsterdam | 59.61 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 7 | Seville | 49.64 | 170,545 | 43 | 9 | 2 | - | 20 | measured |
| 8 | Arnhem | 37.52 | 31,478 | 39 | 3 | 3 | 204 | 20 | measured |
| 9 | Singapore | 49.64 | 967,821 | 34 | 4 | 3 | 165 | 30 | measured |
| 10 | Florence | 36.10 | 184,099 | 23 | 8 | 1 | 27 | 30 | measured |
| 11 | Brisbane | 41.56 | 162,602 | 20 | 2 | 2 | 186 | 30 | measured |
| 12 | Oahu | 41.33 | - | 21 | 2 | 3 | 163 | 20 | measured |
| 13 | Tenerife | 40.38 | - | 4 | 2 | - | - | 20 | measured |
| 14 | Berlin | 37.29 | 412,181 | 21 | 12 | 1 | 195 | 30 | measured |
| 15 | London | 47.02 | 718,291 | 23 | 12 | 1 | - | 30 | measured |
| 16 | Los Angeles | 52.25 | 665,559 | 8 | 2 | - | - | 30 | measured |
| 17 | Paris | 36.10 | 524,268 | 31 | 9 | 4 | 129 | 30 | measured |
| 18 | Vienna | 34.44 | 283,090 | 32 | 14 | 5 | 376 | 30 | measured |
| 19 | Palermo | 24.94 | 124,310 | 21 | 9 | 1 | 37 | 20 | measured |
| 20 | Prague | 33.25 | 303,350 | 30 | 15 | 4 | 31 | 30 | measured |
| 21 | Valencia | 23.04 | 162,209 | 31 | 3 | 2 | 350 | 30 | measured |
| 22 | Leiden | 22.32 | 33,227 | 20 | 6 | 1 | 129 | 20 | measured |
| 23 | Madeira | 25.41 | - | 10 | 1 | 1 | - | 20 | measured |
| 24 | Birmingham | 37.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 25 | Alicante | 18.53 | 77,454 | 16 | 3 | 2 | 44 | 20 | measured |
| 26 | Portland | 21.85 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 27 | New York | 28.50 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 28 | Nijmegen | 15.91 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 29 | Kyoto | 20.19 | 142,353 | 18 | 11 | 2 | - | 20 | measured |
| 30 | Dublin | 17.58 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 31 | Haarlem | 15.20 | 33,960 | 21 | - | 2 | 277 | 20 | measured |
| 32 | Austin | 29.93 | 226,631 | 5 | 2 | - | - | 20 | measured |
| 33 | Munich | 19.95 | 224,067 | 45 | 15 | 6 | 80 | 30 | measured |
| 34 | The Hague | 14.73 | 236,723 | 31 | 2 | 5 | 167 | 20 | measured |
| 35 | Malaga | 19.24 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 36 | Krakow | 19.00 | 140,824 | 34 | 7 | 3 | 198 | 30 | measured |
| 37 | Sintra | 14.25 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 38 | Copenhagen | 26.84 | 218,621 | 16 | 2 | 2 | - | 30 | measured |
| 39 | Reykjavik | 22.32 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 40 | Dordrecht | 12.59 | - | 20 | 1 | 2 | 105 | 20 | measured |
| 41 | Boston | 23.27 | 385,902 | 11 | 2 | 1 | - | 30 | measured |
| 42 | Fukuoka | 15.68 | 77,485 | 15 | 9 | 1 | - | 20 | measured |
| 43 | Tokyo | 12.83 | 394,702 | 17 | 8 | 1 | 6 | 20 | measured |
| 44 | Palma de Mallorca | 14.49 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 45 | Vilnius | 15.91 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 46 | Helmond | 11.64 | - | 18 | - | 2 | 55 | 20 | measured |
| 47 | Geneva | 15.20 | 162,269 | 21 | 5 | 4 | 131 | 20 | measured |
| 48 | Jacksonville | 22.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 49 | Houston | 22.33 | - | 4 | - | - | - | 30 | measured |
| 50 | Oslo | 19.47 | 181,113 | 4 | - | - | - | 20 | measured |
| 51 | Sardinia | 12.11 | - | 5 | 4 | - | 8 | 20 | measured |
| 52 | Cordoba | 13.78 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 53 | Cork | 14.25 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 54 | Leeuwarden | 10.45 | - | 41 | - | 2 | 61 | 20 | measured |
| 55 | Asheville | 20.89 | - | - | - | - | - | 10 | predicted (travel demand) |
| 56 | Long Beach | 20.48 | - | - | - | - | - | 10 | predicted (travel demand) |
| 57 | New Orleans | 20.43 | 256,232 | 4 | 2 | 1 | - | 20 | measured |
| 58 | Little Rock | 20.40 | - | - | - | - | - | 10 | predicted (travel demand) |
| 59 | Ottawa | 13.54 | - | 19 | - | 3 | 122 | 20 | measured |
| 60 | Granada | 12.83 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 61 | Bath | 19.71 | 144,950 | 5 | 2 | 1 | - | 20 | measured |
| 62 | Porto | 9.74 | 120,415 | 27 | 14 | 2 | 40 | 20 | measured |
| 63 | San Francisco | 19.00 | 361,111 | 6 | 1 | 1 | - | 30 | measured |
| 64 | Dallas | 19.00 | - | 8 | 1 | 1 | - | 30 | measured |
| 65 | Oakland | 18.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 66 | Lexington | 18.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 67 | Reno | 18.19 | - | - | - | - | - | 10 | predicted (travel demand) |
| 68 | Des Moines | 18.11 | - | - | - | - | - | 10 | predicted (travel demand) |
| 69 | Edinburgh | 17.57 | 292,981 | 16 | 5 | 1 | - | 30 | measured |
| 70 | Daytona Beach | 17.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 71 | Las Vegas | 17.58 | - | 11 | - | 2 | - | 30 | measured |
| 72 | Cadiz | 11.16 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 73 | Chicago | 17.10 | 485,769 | 6 | - | - | - | 30 | measured |
| 74 | Cagliari | 9.03 | 51,351 | 14 | 1 | 2 | 15 | 20 | measured |
| 75 | Chattanooga | 16.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 76 | Athens | 16.15 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 77 | Perth | 16.15 | 180,478 | 6 | 3 | 1 | - | 30 | measured |
| 78 | Utrecht | 8.08 | 67,963 | 27 | 6 | 2 | 340 | 20 | measured |
| 79 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 80 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 81 | Hilo | 11.88 | - | 6 | - | 1 | 16 | 20 | measured |
| 82 | Huntsville | 15.35 | - | - | - | - | - | 10 | predicted (travel demand) |
| 83 | Melbourne | 10.21 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 84 | Strasbourg | 10.21 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 85 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 86 | West Palm Beach | 14.98 | - | - | - | - | - | 10 | predicted (travel demand) |
| 87 | Hawaii | 13.30 | - | 6 | - | 1 | 6 | 30 | measured |
| 88 | Saint Petersburg | 14.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 89 | Seattle | 14.25 | 398,724 | 6 | 1 | - | - | 30 | measured |
| 90 | St. Louis | 14.80 | - | - | - | - | - | 10 | predicted (travel demand) |
| 91 | Tampa | 14.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 92 | Budapest | 13.54 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 93 | Tallinn | 9.26 | 124,888 | 6 | 3 | 1 | 42 | 20 | measured |
| 94 | Nice | 13.54 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 95 | Venice | 7.36 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 96 | Cincinnati | 13.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 97 | Philadelphia | 12.82 | 405,294 | 1 | - | - | - | 20 | measured |
| 98 | Cyprus | 13.06 | - | 4 | - | - | - | 20 | measured |
| 99 | Hoorn | 6.65 | - | 8 | - | 1 | 52 | 20 | measured |
| 100 | Lansing | 13.02 | - | - | - | - | - | 10 | predicted (travel demand) |
| 101 | Osaka | 8.08 | 163,112 | 6 | 1 | - | - | 30 | measured |
| 102 | Detroit | 12.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 103 | Parma | 6.89 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 104 | Tilburg | 5.94 | - | 20 | - | 3 | 87 | 20 | measured |
| 105 | Bordeaux | 7.84 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 106 | Luxembourg City | 7.84 | 64,851 | 10 | 5 | 2 | 18 | 20 | measured |
| 107 | Denver | 11.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 108 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 109 | Enschede | 5.70 | - | 7 | 1 | 1 | 82 | 20 | measured |
| 110 | San Jose | 11.39 | - | - | - | - | - | 10 | predicted (travel demand) |
| 111 | Menorca | 7.36 | - | 6 | - | - | 2 | 20 | measured |
| 112 | Sacramento | 11.32 | - | - | - | - | - | 10 | predicted (travel demand) |
| 113 | Jersey City | 10.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 114 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 115 | Istanbul | 9.74 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 116 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 117 | Sorrento | 5.46 | 40,049 | 7 | - | 1 | 20 | 20 | measured |
| 118 | Trento | 5.46 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 119 | Milwaukee | 10.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 120 | Salt Lake City | 10.31 | - | - | - | - | - | 10 | predicted (travel demand) |
| 121 | Atlanta | 10.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 122 | Anchorage | 10.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 123 | Montreal | 10.21 | 315,322 | 11 | - | 2 | - | 30 | measured |
| 124 | Raleigh | 10.07 | - | - | - | - | - | 10 | predicted (travel demand) |
| 125 | Caserta | 4.99 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 126 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 127 | Kamakura | 6.18 | 33,492 | 6 | - | - | - | 20 | measured |
| 128 | Cleveland | 9.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 129 | Bologna | 5.23 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 130 | El Paso | 9.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 131 | Girona | 5.70 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 132 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 133 | Leipzig | 6.41 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 134 | Miami | 9.48 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 135 | Sydney | 9.26 | 305,304 | 7 | 1 | - | - | 30 | measured |
| 136 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 137 | Madrid | 5.70 | 274,553 | 17 | 11 | 2 | - | 20 | measured |
| 138 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 139 | Nashville | 8.93 | - | - | - | - | - | 10 | predicted (travel demand) |
| 140 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 141 | Amersfoort | 4.28 | - | 14 | 1 | 2 | 181 | 20 | measured |
| 142 | Naples | 4.28 | 198,913 | 24 | 3 | 3 | 46 | 20 | measured |
| 143 | Ann Arbor | 8.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 144 | Bari | 4.99 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 145 | Crete | 8.31 | - | 4 | 3 | - | - | 20 | measured |
| 146 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 147 | Salzburg | 5.46 | 107,243 | 9 | 3 | 2 | 34 | 20 | measured |
| 148 | Zwolle | 4.04 | - | 14 | - | 1 | 55 | 20 | measured |
| 149 | Lyon | 5.23 | 136,951 | 13 | 4 | 1 | 156 | 20 | measured |
| 150 | Albuquerque | 7.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 151 | Hobart | 4.99 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 152 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 153 | Coimbra | 4.04 | 34,962 | 4 | - | - | 5 | 20 | measured |
| 154 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 155 | Glasgow | 6.89 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 156 | Segovia | 4.51 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 157 | Helsinki | 5.70 | 148,908 | 12 | 2 | 1 | 13 | 30 | measured |
| 158 | Heerlen | 3.56 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 159 | Riga | 6.89 | 108,918 | 5 | 2 | - | - | 20 | measured |
| 160 | Pamplona | 4.51 | 128,065 | 6 | - | - | 1 | 20 | measured |
| 161 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 162 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 163 | Seoul | 6.41 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 164 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 165 | Venlo | 3.33 | - | 7 | - | 1 | 144 | 20 | measured |
| 166 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 167 | Ljubljana | 6.41 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 168 | Toronto | 6.41 | 411,011 | 6 | - | - | - | 30 | measured |
| 169 | Warsaw | 4.28 | 197,929 | 26 | 3 | 3 | 1408 | 30 | measured |
| 170 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 171 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 172 | Dubrovnik | 5.94 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 173 | Washington DC | 5.70 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 174 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 175 | Como | 3.09 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 176 | Eindhoven | 3.09 | - | 16 | - | 4 | 195 | 20 | measured |
| 177 | Vancouver | 5.94 | 351,552 | 4 | - | - | - | 30 | measured |
| 178 | Padua | 3.09 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 179 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 180 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 181 | Bergamo | 2.85 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 182 | Turin | 2.85 | 147,456 | 11 | 7 | 2 | 30 | 20 | measured |
| 183 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 184 | Maui | 5.22 | - | 4 | - | - | 3 | 20 | measured |
| 185 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 186 | Cambridge | 5.46 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 187 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 188 | Spokane | 3.92 | - | 13 | - | 2 | 18 | 10 | published, never ranked (may be uncrawled) |
| 189 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 190 | Bratislava | 3.56 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 191 | Nuremberg | 3.56 | 161,614 | 12 | 1 | 1 | 38 | 20 | measured |
| 192 | Stuttgart | 4.04 | 112,789 | 6 | 1 | - | - | 20 | measured |
| 193 | Charleston | 5.22 | 155,987 | 2 | 1 | - | - | 20 | measured |
| 194 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 195 | Ibiza | 3.33 | - | 1 | - | - | 4 | 20 | measured |
| 196 | Deventer | 2.61 | - | 12 | - | 1 | 213 | 20 | measured |
| 197 | Groningen | 2.61 | 31,401 | 21 | 1 | 2 | 76 | 20 | measured |
| 198 | Santa Fe | 5.17 | - | - | - | - | - | 10 | predicted (travel demand) |
| 199 | Hong Kong | 3.44 | 689,212 | 10 | 4 | 1 | 505 | 20 | measured |
| 200 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 201 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 202 | Boise | 5.07 | - | 4 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 203 | Hiroshima | 3.32 | 129,791 | 17 | 5 | 3 | - | 20 | measured |
| 204 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 205 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 206 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 207 | Genoa | 2.61 | 145,206 | 13 | 2 | 1 | 10 | 20 | measured |
| 208 | Kanazawa | 3.09 | 25,778 | 7 | 2 | 1 | 2 | 20 | measured |
| 209 | Belfast | 4.75 | 224,315 | 4 | - | 1 | - | 20 | measured |
| 210 | Nagoya | 3.09 | 83,437 | 6 | 1 | - | 1 | 20 | measured |
| 211 | Zurich | 4.51 | 140,788 | 6 | - | - | - | 20 | measured |
| 212 | Indianapolis | 4.57 | - | 1 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 213 | Beijing | 4.63 | 269,737 | 7 | 1 | - | - | 30 | measured |
| 214 | Brno | 3.09 | 63,714 | 8 | 5 | 2 | 34 | 20 | measured |
| 215 | Quebec City | 3.09 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 216 | Rio de Janeiro | 4.63 | 279,431 | 6 | - | - | - | 30 | measured |
| 217 | Sapporo | 3.09 | 88,633 | 6 | - | - | - | 20 | measured |
| 218 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 219 | Hamburg | 4.28 | 191,221 | 6 | 1 | 1 | - | 30 | measured |
| 220 | Stockholm | 3.56 | 188,184 | 6 | 4 | - | - | 30 | measured |
| 221 | Kauai | 3.80 | - | 6 | 1 | - | 8 | 20 | measured |
| 222 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 223 | Braga | 2.38 | 34,522 | 4 | 2 | - | 8 | 20 | measured |
| 224 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 225 | Alkmaar | 2.14 | - | 7 | - | 1 | 79 | 20 | measured |
| 226 | Apeldoorn | 2.14 | - | 10 | - | 2 | 80 | 20 | measured |
| 227 | Hilversum | 2.14 | - | 6 | 1 | 1 | 122 | 20 | measured |
| 228 | San Diego | 4.28 | 214,939 | 4 | 1 | 1 | - | 20 | measured |
| 229 | Toulouse | 2.85 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 230 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 231 | Aarhus | 4.04 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 232 | Guimaraes | 2.14 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 233 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 234 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 235 | Catania | 2.38 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 236 | Bristol | 4.04 | 163,983 | 6 | 2 | - | - | 20 | measured |
| 237 | Mexico City | 3.80 | 566,583 | 9 | 2 | - | - | 30 | measured |
| 238 | Perugia | 2.14 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 239 | Verona | 2.38 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 240 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 241 | Pittsburgh | 3.80 | - | 4 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 242 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 243 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 244 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 245 | Maastricht | 1.90 | 47,763 | 18 | - | 2 | 135 | 20 | measured |
| 246 | Rotterdam | 1.90 | 104,938 | 12 | - | 2 | 83 | 20 | measured |
| 247 | Savannah | 3.80 | 128,162 | 2 | 1 | - | - | 20 | measured |
| 248 | Bangkok | 3.68 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 249 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 250 | Monterey | 3.64 | - | 3 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 251 | Liverpool | 3.56 | 248,189 | 2 | 1 | - | - | 20 | measured |
| 252 | Manchester | 3.56 | 316,438 | 5 | - | - | - | 30 | measured |
| 253 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 254 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 255 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 256 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 257 | San Antonio | 3.32 | - | 4 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 258 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 259 | Fort Worth | 3.28 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 260 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 261 | Tarragona | 1.90 | 32,396 | 4 | 2 | - | - | 20 | measured |
| 262 | Auckland | 3.09 | 152,056 | 5 | 2 | - | - | 20 | measured |
| 263 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 264 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 265 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 266 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 267 | Tulsa | 3.01 | - | 1 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 268 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 269 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 270 | Buenos Aires | 2.85 | 333,331 | 4 | 2 | - | - | 30 | measured |
| 271 | Den Bosch | 1.43 | 39,682 | 12 | 2 | 1 | 118 | 20 | measured |
| 272 | Bruges | 2.85 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 273 | Cologne | 2.85 | 191,812 | 5 | - | 1 | - | 30 | measured |
| 274 | Graz | 1.90 | 65,717 | 12 | 7 | 1 | 87 | 20 | measured |
| 275 | Kansas City | 2.85 | - | 4 | - | 1 | - | 30 | measured |
| 276 | Potsdam | 1.90 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 277 | Matera | 1.66 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 278 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 279 | Modena | 1.66 | 51,698 | 5 | 1 | 1 | 3 | 20 | measured |
| 280 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 281 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 282 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 283 | Taipei | 2.61 | 143,193 | 4 | 1 | - | - | 30 | measured |
| 284 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 285 | Ghent | 2.38 | 82,757 | 6 | 1 | 1 | - | 20 | measured |
| 286 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 287 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 288 | Naha | 1.66 | 24,466 | 6 | - | - | 1 | 20 | measured |
| 289 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 290 | Dresden | 1.66 | 113,624 | 5 | 5 | 1 | - | 20 | measured |
| 291 | Gdansk | 1.66 | 4,908 | 6 | 4 | - | 288 | 20 | measured |
| 292 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 293 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 294 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 295 | Heidelberg | 2.14 | 75,837 | 6 | 1 | 1 | - | 20 | measured |
| 296 | Assen | 1.19 | - | 10 | - | 2 | 66 | 20 | measured |
| 297 | Delft | 1.19 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 298 | Trieste | 1.19 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 299 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 300 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 301 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 302 | Regensburg | 2.14 | 51,930 | 5 | - | 1 | 4 | 20 | measured |
| 303 | Canberra | 2.28 | - | 1 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 304 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 305 | Pisa | 1.46 | 52,174 | 4 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 306 | Setubal | 1.19 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 307 | Belgrade | 2.14 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 308 | Thessaloniki | 2.14 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 309 | Salamanca | 1.37 | 47,897 | 4 | - | 1 | 1 | 10 | published, never ranked (may be uncrawled) |
| 310 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 311 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 312 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 313 | Breda | 0.95 | 36,579 | 10 | - | 2 | 118 | 20 | measured |
| 314 | Roosendaal | 0.95 | - | 8 | - | 1 | 116 | 20 | measured |
| 315 | Minneapolis | 1.88 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 316 | Bucharest | 1.84 | 136,836 | 4 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 317 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 318 | Baltimore | 1.77 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 319 | Zaragoza | 1.19 | 87,580 | 7 | - | 1 | - | 20 | measured |
| 320 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 321 | Bilbao | 1.19 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 322 | Cesky Krumlov | 1.19 | 28,582 | 6 | 3 | - | 11 | 20 | measured |
| 323 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 324 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 325 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 326 | Leuven | 1.66 | 40,645 | 4 | - | - | - | 20 | measured |
| 327 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 328 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 329 | Rouen | 1.43 | 72,334 | 12 | - | 1 | 6 | 20 | measured |
| 330 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 331 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 332 | Yakushima | 0.95 | - | 1 | - | - | 1 | 20 | measured |
| 333 | Gothenburg | 1.43 | 119,991 | 5 | - | 1 | - | 20 | measured |
| 334 | York | 1.43 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 335 | Poznan | 0.95 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 336 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 337 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 338 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 339 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 340 | Oxford | 1.19 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 341 | Ronda | 0.71 | 51,510 | 6 | 1 | - | 9 | 20 | measured |
| 342 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 343 | Brighton | 1.19 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 344 | Assisi | 0.71 | 30,278 | 6 | 1 | 2 | 6 | 20 | measured |
| 345 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 346 | Frankfurt | 0.71 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 347 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 348 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 349 | Lucca | 0.48 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 350 | Nantes | 0.96 | 67,689 | 1 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 351 | Busan | 0.83 | 94,737 | 2 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 352 | Rothenburg ob der Tauber | 0.71 | 39,879 | 4 | - | 1 | 8 | 20 | measured |
| 353 | Ferrara | 0.48 | 27,490 | 5 | 3 | 1 | 7 | 20 | measured |
| 354 | Sao Paulo | 0.74 | 911 | 1 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 355 | Wroclaw | 0.48 | 123,894 | 5 | 1 | 1 | 121 | 20 | measured |
| 356 | Split | 0.71 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 357 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 358 | Hallstatt | 0.50 | 47,271 | 5 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 359 | Phoenix | 0.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 360 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 361 | Cardiff | 0.48 | - | 4 | - | 1 | - | 20 | measured |
| 362 | Fort Lauderdale | 0.47 | - | 4 | - | - | - | 30 | measured |
| 363 | Turku | 0.48 | - | 1 | - | - | - | 30 | measured |
| 364 | Antwerp | 0.47 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 365 | Sofia | 0.24 | 138,710 | 4 | - | - | - | 30 | measured |
| 366 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 367 | Bamberg | 0.24 | 28,716 | 5 | 4 | 1 | 10 | 20 | measured |
| 368 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 369 | George Town | 0.28 | 36,080 | - | - | - | - | 10 | predicted (travel demand) |
| 370 | Freiburg | 0.24 | 92,752 | 7 | 2 | 1 | - | 20 | measured |
| 371 | Allentown | 0.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 372 | Lausanne | 0.24 | 68,242 | 8 | - | 1 | - | 20 | measured |
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

