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
| 1 | Rome | 184.82 | 358,876 | 30 | 9 | 2 | 32 | 30 | measured |
| 2 | Amsterdam | 86.42 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 3 | Lisbon | 80.43 | 201,877 | 35 | 10 | 3 | 68 | 30 | measured |
| 4 | Barcelona | 66.45 | 346,477 | 56 | 12 | 7 | 180 | 30 | measured |
| 5 | Singapore | 56.76 | 967,821 | 28 | 3 | 3 | 165 | 30 | measured |
| 6 | Milan | 40.21 | 212,705 | 22 | 9 | 2 | 25 | 30 | measured |
| 7 | Seville | 49.06 | 170,545 | 43 | 6 | 2 | - | 20 | measured |
| 8 | Florence | 37.08 | 184,099 | 23 | 8 | 1 | 27 | 30 | measured |
| 9 | Brisbane | 45.06 | 162,602 | 19 | 1 | 2 | 189 | 30 | measured |
| 10 | Brussels | 41.93 | 176,863 | 30 | 4 | 1 | 436 | 30 | measured |
| 11 | Vienna | 39.07 | 283,090 | 32 | 13 | 5 | 376 | 30 | measured |
| 12 | London | 49.34 | 718,291 | 23 | 10 | 1 | - | 30 | measured |
| 13 | Prague | 37.93 | 303,350 | 18 | 13 | 3 | 30 | 30 | measured |
| 14 | Madeira | 34.23 | - | 10 | 1 | 1 | - | 20 | measured |
| 15 | Paris | 33.37 | 524,268 | 31 | 9 | 4 | 129 | 30 | measured |
| 16 | Alicante | 23.96 | 77,454 | 15 | 3 | 2 | 44 | 20 | measured |
| 17 | Portland | 31.94 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 18 | Tenerife | 30.23 | - | 4 | 1 | - | - | 20 | measured |
| 19 | Hilo | 34.80 | - | 6 | - | 1 | 16 | 20 | measured |
| 20 | Palermo | 22.53 | 124,310 | 21 | 7 | 1 | 37 | 20 | measured |
| 21 | New York | 38.79 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 22 | Malaga | 29.09 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 23 | Sardinia | 23.96 | - | 5 | 2 | - | 8 | 20 | measured |
| 24 | Naples | 20.54 | 198,913 | 24 | 3 | 3 | 46 | 20 | measured |
| 25 | Birmingham | 37.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 26 | Fukuoka | 24.24 | 77,485 | 15 | 7 | 1 | - | 20 | measured |
| 27 | Bologna | 18.54 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 28 | Kyoto | 21.68 | 142,353 | 17 | 8 | 2 | - | 20 | measured |
| 29 | Venice | 18.54 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 30 | Copenhagen | 31.37 | 218,621 | 16 | 1 | 2 | - | 30 | measured |
| 31 | Leiden | 16.54 | 33,227 | 12 | 4 | 1 | 129 | 20 | measured |
| 32 | Dublin | 18.82 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 33 | Valencia | 15.97 | 162,209 | 25 | 2 | 2 | 350 | 30 | measured |
| 34 | Sintra | 14.83 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 35 | Palma de Mallorca | 17.68 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 36 | Berlin | 19.39 | 412,181 | 19 | 11 | 1 | 195 | 30 | measured |
| 37 | Munich | 18.54 | 224,067 | 45 | 14 | 6 | 80 | 30 | measured |
| 38 | Seattle | 25.10 | 398,724 | 6 | - | - | - | 30 | measured |
| 39 | Crete | 25.67 | - | 4 | 2 | - | - | 20 | measured |
| 40 | Athens | 23.67 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 41 | Oahu | 15.97 | - | 11 | 1 | - | 160 | 20 | measured |
| 42 | Porto | 11.98 | 120,415 | 27 | 14 | 2 | 40 | 20 | measured |
| 43 | Utrecht | 11.69 | 67,963 | 33 | 4 | 2 | 345 | 20 | measured |
| 44 | The Hague | 11.41 | 236,723 | 29 | 1 | 5 | 166 | 20 | measured |
| 45 | Jacksonville | 22.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 46 | Krakow | 15.12 | 140,824 | 34 | 3 | 3 | 198 | 30 | measured |
| 47 | Chicago | 21.68 | 485,769 | 6 | - | - | - | 30 | measured |
| 48 | Boston | 20.54 | 385,902 | 11 | 1 | 1 | - | 30 | measured |
| 49 | Asheville | 20.89 | - | - | - | - | - | 10 | predicted (travel demand) |
| 50 | Boise | 20.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 51 | New Orleans | 20.54 | 256,232 | 4 | 2 | 1 | - | 20 | measured |
| 52 | Long Beach | 20.48 | - | - | - | - | - | 10 | predicted (travel demand) |
| 53 | Little Rock | 20.40 | - | - | - | - | - | 10 | predicted (travel demand) |
| 54 | Toronto | 19.96 | 411,011 | 6 | - | - | - | 30 | measured |
| 55 | Nijmegen | 9.98 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 56 | Tokyo | 10.55 | 394,702 | 16 | 8 | 1 | 6 | 20 | measured |
| 57 | Austin | 19.39 | 226,631 | 5 | - | - | - | 20 | measured |
| 58 | Seoul | 17.68 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 59 | Indianapolis | 18.28 | - | - | - | - | - | 10 | predicted (travel demand) |
| 60 | Madrid | 11.69 | 274,553 | 17 | 10 | 2 | - | 20 | measured |
| 61 | Geneva | 12.55 | 162,269 | 21 | 4 | 4 | 131 | 20 | measured |
| 62 | Arnhem | 9.41 | 31,478 | 9 | 1 | 1 | 196 | 20 | measured |
| 63 | Oakland | 18.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 64 | Fort Lauderdale | 18.43 | - | - | - | - | - | 10 | predicted (travel demand) |
| 65 | Edinburgh | 17.97 | 292,981 | 16 | 4 | 1 | - | 30 | measured |
| 66 | Las Vegas | 18.25 | - | 11 | - | 2 | - | 30 | measured |
| 67 | Lexington | 18.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 68 | Reno | 18.19 | - | - | - | - | - | 10 | predicted (travel demand) |
| 69 | Des Moines | 18.11 | - | - | - | - | - | 10 | predicted (travel demand) |
| 70 | Perth | 17.68 | 180,478 | 6 | 1 | 1 | - | 30 | measured |
| 71 | Strasbourg | 11.98 | 154,700 | 10 | 1 | 2 | 66 | 30 | measured |
| 72 | Daytona Beach | 17.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 73 | Reykjavik | 15.12 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 74 | Cagliari | 9.41 | 51,351 | 10 | 1 | 2 | 15 | 20 | measured |
| 75 | Melbourne | 11.41 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 76 | Chattanooga | 16.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 77 | Groningen | 8.27 | 31,401 | 20 | - | 2 | 72 | 20 | measured |
| 78 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 79 | Spokane | 15.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 80 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 81 | Pittsburgh | 15.18 | - | - | - | - | - | 10 | predicted (travel demand) |
| 82 | Huntsville | 15.35 | - | - | - | - | - | 10 | predicted (travel demand) |
| 83 | Budapest | 14.55 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 84 | Sydney | 14.83 | 305,304 | 6 | - | - | - | 30 | measured |
| 85 | Bath | 15.12 | 144,950 | 5 | 1 | 1 | - | 20 | measured |
| 86 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 87 | West Palm Beach | 14.98 | - | - | - | - | - | 10 | predicted (travel demand) |
| 88 | Vilnius | 9.98 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 89 | Monterey | 14.58 | - | - | - | - | - | 10 | predicted (travel demand) |
| 90 | Saint Petersburg | 14.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 91 | St. Louis | 14.80 | - | - | - | - | - | 10 | predicted (travel demand) |
| 92 | Eindhoven | 7.13 | - | 7 | - | 1 | 195 | 20 | measured |
| 93 | Tampa | 14.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 94 | Cadiz | 8.56 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 95 | Cincinnati | 13.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 96 | Dallas | 13.12 | - | 8 | 1 | 1 | - | 30 | measured |
| 97 | Sorrento | 6.56 | 40,049 | 6 | - | 1 | 20 | 20 | measured |
| 98 | Cyprus | 12.83 | - | 4 | - | - | - | 20 | measured |
| 99 | Lansing | 13.02 | - | - | - | - | - | 10 | predicted (travel demand) |
| 100 | Detroit | 12.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 101 | Tulsa | 12.03 | - | - | - | - | - | 10 | predicted (travel demand) |
| 102 | Bordeaux | 7.99 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 103 | Denver | 11.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 104 | Istanbul | 10.12 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 105 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 106 | Montreal | 11.41 | 315,322 | 7 | - | 1 | - | 30 | measured |
| 107 | San Jose | 11.39 | - | - | - | - | - | 10 | predicted (travel demand) |
| 108 | Sacramento | 11.32 | - | - | - | - | - | 10 | predicted (travel demand) |
| 109 | Jersey City | 10.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 110 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 111 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 112 | Lyon | 7.13 | 136,951 | 13 | 3 | 1 | 156 | 20 | measured |
| 113 | Milwaukee | 10.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 114 | Glasgow | 9.98 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 115 | Salt Lake City | 10.31 | - | - | - | - | - | 10 | predicted (travel demand) |
| 116 | Atlanta | 10.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 117 | Tallinn | 6.85 | 124,888 | 4 | 2 | 1 | 42 | 20 | measured |
| 118 | Trieste | 5.13 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 119 | Anchorage | 10.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 120 | Raleigh | 10.07 | - | - | - | - | - | 10 | predicted (travel demand) |
| 121 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 122 | Warsaw | 6.56 | 197,929 | 19 | 3 | 2 | 1446 | 30 | measured |
| 123 | Cleveland | 9.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 124 | El Paso | 9.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 125 | Houston | 9.70 | - | 4 | - | - | - | 30 | measured |
| 126 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 127 | Miami | 9.48 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 128 | Oslo | 8.27 | 181,113 | 4 | - | - | - | 20 | measured |
| 129 | Turku | 9.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 130 | Quebec City | 6.27 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 131 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 132 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 133 | Canberra | 9.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 134 | Maastricht | 4.56 | 47,763 | 14 | - | 1 | 137 | 20 | measured |
| 135 | Pisa | 5.85 | 52,174 | - | - | - | - | 10 | predicted (travel demand) |
| 136 | Nashville | 8.93 | - | - | - | - | - | 10 | predicted (travel demand) |
| 137 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 138 | Rotterdam | 4.28 | 104,938 | 12 | - | 2 | 83 | 20 | measured |
| 139 | Trento | 4.28 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 140 | Ann Arbor | 8.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 141 | Nuremberg | 5.70 | 161,614 | 12 | 1 | 1 | 38 | 20 | measured |
| 142 | Salamanca | 5.50 | 47,897 | - | - | - | 1 | 10 | predicted (travel demand) |
| 143 | Pamplona | 5.42 | 128,065 | 6 | - | - | 1 | 20 | measured |
| 144 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 145 | Girona | 4.85 | 51,072 | 7 | - | - | - | 20 | measured |
| 146 | Kamakura | 5.13 | 33,492 | 6 | - | - | - | 20 | measured |
| 147 | Graz | 5.42 | 65,717 | 12 | 3 | 1 | 87 | 20 | measured |
| 148 | Granada | 5.13 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 149 | Tilburg | 3.99 | - | 7 | - | 1 | 84 | 20 | measured |
| 150 | Dubrovnik | 7.42 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 151 | Albuquerque | 7.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 152 | Mexico City | 7.27 | 566,583 | 9 | 1 | - | - | 30 | measured |
| 153 | Sapporo | 5.13 | 88,633 | 6 | - | - | - | 20 | measured |
| 154 | Minneapolis | 7.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 155 | Osaka | 4.85 | 163,112 | 5 | 1 | - | - | 30 | measured |
| 156 | Oxford | 7.42 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 157 | Washington DC | 6.85 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 158 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 159 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 160 | Cork | 4.85 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 161 | Kauai | 6.27 | - | 6 | 1 | - | 8 | 20 | measured |
| 162 | Braga | 3.99 | 34,522 | 4 | 1 | - | 8 | 20 | measured |
| 163 | Baltimore | 7.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 164 | Los Angeles | 6.85 | 665,559 | 8 | 2 | - | - | 30 | measured |
| 165 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 166 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 167 | Bilbao | 4.56 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 168 | Brno | 4.56 | 63,714 | 8 | 2 | 2 | 34 | 20 | measured |
| 169 | Potsdam | 4.56 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 170 | Catania | 3.99 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 171 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 172 | Helsinki | 5.42 | 148,908 | 8 | 1 | - | 9 | 30 | measured |
| 173 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 174 | Hobart | 4.28 | 81,734 | 10 | - | 2 | 455 | 20 | measured |
| 175 | Leipzig | 4.28 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 176 | Riga | 6.27 | 108,918 | 5 | - | - | - | 20 | measured |
| 177 | San Francisco | 6.27 | 361,111 | 6 | - | 1 | - | 30 | measured |
| 178 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 179 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 180 | Verona | 3.71 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 181 | Haarlem | 3.14 | 33,960 | 21 | - | 2 | 277 | 20 | measured |
| 182 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 183 | Cordoba | 3.71 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 184 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 185 | Hawaii | 5.13 | - | 6 | - | 1 | 6 | 30 | measured |
| 186 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 187 | Como | 2.85 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 188 | Dordrecht | 2.85 | - | 8 | - | 2 | 103 | 20 | measured |
| 189 | Lucca | 2.85 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 190 | Turin | 2.85 | 147,456 | 11 | 7 | 2 | 30 | 20 | measured |
| 191 | Poznan | 3.71 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 192 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 193 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 194 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 195 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 196 | Philadelphia | 5.13 | 405,294 | 1 | - | - | - | 20 | measured |
| 197 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 198 | Bristol | 5.13 | 163,983 | 5 | 1 | - | - | 20 | measured |
| 199 | Ljubljana | 5.13 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 200 | Vancouver | 5.13 | 351,552 | 4 | - | - | - | 30 | measured |
| 201 | Cardiff | 5.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 202 | Santa Fe | 5.17 | - | - | - | - | - | 10 | predicted (travel demand) |
| 203 | Caserta | 2.57 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 204 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 205 | Venlo | 2.57 | - | 7 | - | 1 | 144 | 20 | measured |
| 206 | Luxembourg City | 3.42 | 64,851 | 10 | - | 2 | 18 | 20 | measured |
| 207 | Salzburg | 3.42 | 107,243 | 5 | - | - | 34 | 20 | measured |
| 208 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 209 | Lausanne | 4.90 | 68,242 | - | - | - | - | 10 | predicted (travel demand) |
| 210 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 211 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 212 | Guimaraes | 2.57 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 213 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 214 | Perugia | 2.57 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 215 | Bari | 2.85 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 216 | Bratislava | 3.14 | 132,162 | 7 | - | 1 | 26 | 30 | measured |
| 217 | Frankfurt | 3.14 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 218 | Parma | 2.57 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 219 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 220 | Alkmaar | 2.28 | - | 7 | - | 1 | 79 | 20 | measured |
| 221 | Bergamo | 2.28 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 222 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 223 | Menorca | 2.85 | - | 6 | - | - | 2 | 20 | measured |
| 224 | Aarhus | 4.28 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 225 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 226 | Genoa | 2.28 | 145,206 | 12 | 1 | 1 | 11 | 20 | measured |
| 227 | Coimbra | 2.28 | 34,962 | 4 | - | - | 5 | 20 | measured |
| 228 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 229 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 230 | Hong Kong | 2.71 | 689,212 | 10 | 2 | 1 | 505 | 20 | measured |
| 231 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 232 | Amersfoort | 2.00 | - | 8 | 1 | 1 | 181 | 20 | measured |
| 233 | Heerlen | 2.00 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 234 | Nice | 3.99 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 235 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 236 | Nantes | 3.83 | 67,689 | - | - | - | - | 10 | predicted (travel demand) |
| 237 | Zurich | 3.71 | 140,788 | 4 | - | - | - | 20 | measured |
| 238 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 239 | Toulouse | 2.57 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 240 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 241 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 242 | Modena | 2.28 | 51,698 | 5 | - | 1 | 3 | 20 | measured |
| 243 | Stockholm | 2.85 | 188,184 | 4 | 3 | - | - | 30 | measured |
| 244 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 245 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 246 | Busan | 3.31 | 94,737 | - | - | - | - | 10 | predicted (travel demand) |
| 247 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 248 | Apeldoorn | 1.71 | - | 9 | - | 2 | 80 | 20 | measured |
| 249 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 250 | Cologne | 3.42 | 191,812 | 5 | - | 1 | - | 30 | measured |
| 251 | Delft | 1.71 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 252 | Den Bosch | 1.71 | 39,682 | 11 | 1 | 1 | 119 | 20 | measured |
| 253 | Hoorn | 1.71 | - | 8 | - | 1 | 52 | 20 | measured |
| 254 | Leeuwarden | 1.71 | - | 8 | - | 1 | 61 | 20 | measured |
| 255 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 256 | Zwolle | 1.71 | - | 7 | - | 1 | 57 | 20 | measured |
| 257 | San Antonio | 3.32 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 258 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 259 | Fort Worth | 3.28 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 260 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 261 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 262 | Cambridge | 3.14 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 263 | Sao Paulo | 2.96 | 911 | - | - | - | - | 10 | predicted (travel demand) |
| 264 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 265 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 266 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 267 | Maui | 2.85 | - | 4 | - | - | 3 | 20 | measured |
| 268 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 269 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 270 | Auckland | 2.85 | 152,056 | 5 | 1 | - | - | 20 | measured |
| 271 | Charleston | 2.85 | 155,987 | 2 | 1 | - | - | 20 | measured |
| 272 | Tarragona | 1.71 | 32,396 | 4 | - | - | - | 20 | measured |
| 273 | Assen | 1.43 | - | 9 | - | 2 | 67 | 20 | measured |
| 274 | Helmond | 1.43 | - | 7 | - | 1 | 55 | 20 | measured |
| 275 | Hilversum | 1.43 | - | 6 | - | 1 | 122 | 20 | measured |
| 276 | Savannah | 2.85 | 128,162 | 2 | - | - | - | 20 | measured |
| 277 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 278 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 279 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 280 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 281 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 282 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 283 | Manchester | 2.57 | 316,438 | 5 | - | - | - | 30 | measured |
| 284 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 285 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 286 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 287 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 288 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 289 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 290 | Stuttgart | 2.00 | 112,789 | 7 | - | - | - | 20 | measured |
| 291 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 292 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 293 | Hallstatt | 1.99 | 47,271 | - | - | - | - | 10 | predicted (travel demand) |
| 294 | Enschede | 1.14 | - | 7 | 1 | 1 | 82 | 20 | measured |
| 295 | Kansas City | 2.28 | - | 4 | - | 1 | - | 30 | measured |
| 296 | Roosendaal | 1.14 | - | 8 | - | 1 | 116 | 20 | measured |
| 297 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 298 | Kanazawa | 1.43 | 25,778 | 7 | 1 | 1 | 2 | 20 | measured |
| 299 | Naha | 1.43 | 24,466 | 6 | - | - | 1 | 20 | measured |
| 300 | Cesky Krumlov | 1.43 | 28,582 | 6 | 2 | - | 11 | 20 | measured |
| 301 | Gdansk | 1.43 | 4,908 | 6 | 4 | - | 288 | 20 | measured |
| 302 | Sofia | 1.43 | 138,710 | 4 | - | - | - | 30 | measured |
| 303 | Wroclaw | 1.43 | 123,894 | 5 | 1 | 1 | 121 | 20 | measured |
| 304 | Bangkok | 2.14 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 305 | Padua | 1.14 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 306 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 307 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 308 | Bruges | 2.00 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 309 | Rio de Janeiro | 2.00 | 279,431 | 6 | - | - | - | 30 | measured |
| 310 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 311 | Buenos Aires | 1.85 | 333,331 | 4 | 1 | - | - | 30 | measured |
| 312 | Segovia | 1.14 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 313 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 314 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 315 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 316 | Rothenburg ob der Tauber | 1.43 | 39,879 | 4 | - | 1 | 8 | 20 | measured |
| 317 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 318 | Belfast | 1.71 | 224,315 | 4 | - | 1 | - | 20 | measured |
| 319 | Hiroshima | 1.14 | 129,791 | 8 | 1 | 2 | - | 20 | measured |
| 320 | Ottawa | 1.14 | - | 8 | - | 1 | 119 | 20 | measured |
| 321 | Thessaloniki | 1.71 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 322 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 323 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 324 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 325 | Setubal | 0.86 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 326 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 327 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 328 | Ronda | 0.86 | 51,510 | 6 | - | - | 9 | 20 | measured |
| 329 | Antwerp | 1.43 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 330 | Belgrade | 1.43 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 331 | York | 1.43 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 332 | Assisi | 0.86 | 30,278 | 6 | 1 | 2 | 6 | 20 | measured |
| 333 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 334 | Nagoya | 0.86 | 83,437 | 6 | - | - | 1 | 20 | measured |
| 335 | Dresden | 0.86 | 113,624 | 5 | 1 | 1 | - | 20 | measured |
| 336 | Breda | 0.64 | 36,579 | 4 | - | 1 | 119 | 10 | published, never ranked (may be uncrawled) |
| 337 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 338 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 339 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 340 | Ghent | 1.14 | 82,757 | 6 | - | 1 | - | 20 | measured |
| 341 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 342 | Beijing | 1.14 | 269,737 | 6 | - | - | - | 30 | measured |
| 343 | Deventer | 0.57 | - | 7 | - | 1 | 213 | 20 | measured |
| 344 | Liverpool | 1.14 | 248,189 | 2 | - | - | - | 20 | measured |
| 345 | San Diego | 1.14 | 214,939 | 4 | - | 1 | - | 20 | measured |
| 346 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 347 | Zaragoza | 0.73 | 87,580 | 7 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 348 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 349 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 350 | Matera | 0.57 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 351 | Regensburg | 0.86 | 51,930 | 5 | - | 1 | 4 | 20 | measured |
| 352 | Brighton | 0.86 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 353 | Gothenburg | 0.86 | 119,991 | 5 | - | 1 | - | 20 | measured |
| 354 | Taipei | 0.86 | 143,193 | 4 | - | - | - | 30 | measured |
| 355 | Ibiza | 0.46 | - | 1 | - | - | 4 | 10 | published, never ranked (may be uncrawled) |
| 356 | Rouen | 0.57 | 72,334 | 12 | - | 1 | 6 | 20 | measured |
| 357 | Lima | 0.51 | 132,792 | 5 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 358 | Leuven | 0.57 | 40,645 | 4 | - | - | - | 20 | measured |
| 359 | Split | 0.57 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 360 | Phoenix | 0.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 361 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 362 | Yakushima | 0.29 | - | 1 | - | - | 1 | 20 | measured |
| 363 | Ferrara | 0.21 | 27,490 | 5 | 1 | 1 | 7 | 10 | published, never ranked (may be uncrawled) |
| 364 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 365 | Bamberg | 0.29 | 28,716 | 5 | 3 | 1 | 10 | 20 | measured |
| 366 | Heidelberg | 0.29 | 75,837 | 6 | - | 1 | - | 20 | measured |
| 367 | Hamburg | 0.29 | 191,221 | 6 | - | 1 | - | 30 | measured |
| 368 | Freiburg | 0.29 | 92,752 | 7 | - | 1 | - | 20 | measured |
| 369 | Bucharest | 0.29 | 136,836 | 4 | - | 1 | - | 20 | measured |
| 370 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 371 | George Town | 0.28 | 36,080 | - | - | - | - | 10 | predicted (travel demand) |
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

