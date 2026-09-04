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
| 1 | Rome | 183.96 | 358,876 | 30 | 9 | 2 | 32 | 30 | measured |
| 2 | Amsterdam | 98.99 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 3 | Lisbon | 78.84 | 201,877 | 35 | 10 | 3 | 68 | 30 | measured |
| 4 | Barcelona | 66.58 | 346,477 | 56 | 12 | 7 | 180 | 30 | measured |
| 5 | Singapore | 59.57 | 967,821 | 28 | 3 | 3 | 165 | 30 | measured |
| 6 | Milan | 40.88 | 212,705 | 22 | 9 | 2 | 25 | 30 | measured |
| 7 | Seville | 51.10 | 170,545 | 43 | 6 | 2 | - | 20 | measured |
| 8 | Florence | 38.25 | 184,099 | 23 | 8 | 1 | 27 | 30 | measured |
| 9 | Brisbane | 45.84 | 162,602 | 19 | 1 | 2 | 189 | 30 | measured |
| 10 | Vienna | 41.17 | 283,090 | 32 | 13 | 5 | 376 | 30 | measured |
| 11 | London | 51.10 | 718,291 | 23 | 10 | 1 | - | 30 | measured |
| 12 | Prague | 39.71 | 303,350 | 18 | 13 | 3 | 30 | 30 | measured |
| 13 | Malaga | 35.62 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 14 | Tenerife | 35.04 | - | 4 | 1 | - | - | 20 | measured |
| 15 | Naples | 25.40 | 198,913 | 24 | 3 | 3 | 46 | 20 | measured |
| 16 | Hilo | 37.96 | - | 6 | - | 1 | 16 | 20 | measured |
| 17 | Paris | 33.29 | 524,268 | 31 | 9 | 4 | 129 | 30 | measured |
| 18 | Portland | 33.29 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 19 | New York | 43.80 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 20 | Madeira | 28.91 | - | 10 | 1 | 1 | - | 20 | measured |
| 21 | Alicante | 23.94 | 77,454 | 15 | 3 | 2 | 44 | 20 | measured |
| 22 | Sardinia | 25.70 | - | 5 | 2 | - | 8 | 20 | measured |
| 23 | Palermo | 21.32 | 124,310 | 21 | 7 | 1 | 37 | 20 | measured |
| 24 | Brussels | 27.74 | 176,863 | 30 | 4 | 1 | 436 | 30 | measured |
| 25 | Fukuoka | 25.40 | 77,485 | 15 | 7 | 1 | - | 20 | measured |
| 26 | Copenhagen | 36.50 | 218,621 | 16 | 1 | 2 | - | 30 | measured |
| 27 | Leiden | 19.27 | 33,227 | 12 | 4 | 1 | 129 | 20 | measured |
| 28 | Birmingham | 37.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 29 | Dublin | 21.02 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 30 | Venice | 19.86 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 31 | Valencia | 17.52 | 162,209 | 24 | 2 | 2 | 350 | 30 | measured |
| 32 | Palma de Mallorca | 19.86 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 33 | Nijmegen | 16.06 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 34 | Bologna | 16.94 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 35 | Kyoto | 19.86 | 142,353 | 17 | 8 | 2 | - | 20 | measured |
| 36 | Crete | 30.66 | - | 4 | 2 | - | - | 20 | measured |
| 37 | Berlin | 18.10 | 412,181 | 19 | 11 | 1 | 195 | 30 | measured |
| 38 | Sintra | 13.43 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 39 | Seattle | 25.70 | 398,724 | 6 | - | - | - | 30 | measured |
| 40 | Madrid | 15.77 | 274,553 | 17 | 10 | 2 | - | 20 | measured |
| 41 | Munich | 16.64 | 224,067 | 45 | 14 | 6 | 80 | 30 | measured |
| 42 | Utrecht | 12.26 | 67,963 | 33 | 4 | 2 | 345 | 20 | measured |
| 43 | Chicago | 23.94 | 485,769 | 6 | - | - | - | 30 | measured |
| 44 | Oahu | 15.77 | - | 11 | 1 | - | 160 | 20 | measured |
| 45 | Athens | 23.07 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 46 | Toronto | 23.07 | 411,011 | 6 | - | - | - | 30 | measured |
| 47 | Bath | 23.07 | 144,950 | 5 | 1 | 1 | - | 20 | measured |
| 48 | Las Vegas | 22.78 | - | 11 | - | 2 | - | 30 | measured |
| 49 | Krakow | 15.18 | 140,824 | 34 | 3 | 3 | 198 | 30 | measured |
| 50 | Jacksonville | 22.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 51 | Asheville | 20.89 | - | - | - | - | - | 10 | predicted (travel demand) |
| 52 | Tokyo | 11.10 | 394,702 | 16 | 8 | 1 | 6 | 20 | measured |
| 53 | Seoul | 19.27 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 54 | Boise | 20.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 55 | Long Beach | 20.48 | - | - | - | - | - | 10 | predicted (travel demand) |
| 56 | Little Rock | 20.40 | - | - | - | - | - | 10 | predicted (travel demand) |
| 57 | Boston | 19.27 | 385,902 | 11 | 1 | 1 | - | 30 | measured |
| 58 | New Orleans | 19.86 | 256,232 | 4 | 2 | 1 | - | 20 | measured |
| 59 | Porto | 9.93 | 120,415 | 27 | 14 | 2 | 40 | 20 | measured |
| 60 | Edinburgh | 19.27 | 292,981 | 16 | 4 | 1 | - | 30 | measured |
| 61 | The Hague | 9.64 | 236,723 | 29 | 1 | 5 | 166 | 20 | measured |
| 62 | Austin | 19.27 | 226,631 | 5 | - | - | - | 20 | measured |
| 63 | Cagliari | 10.22 | 51,351 | 10 | 1 | 2 | 15 | 20 | measured |
| 64 | Indianapolis | 18.28 | - | - | - | - | - | 10 | predicted (travel demand) |
| 65 | Oakland | 18.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 66 | Fort Lauderdale | 18.43 | - | - | - | - | - | 10 | predicted (travel demand) |
| 67 | Groningen | 9.34 | 31,401 | 20 | - | 2 | 72 | 20 | measured |
| 68 | Lexington | 18.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 69 | Reno | 18.19 | - | - | - | - | - | 10 | predicted (travel demand) |
| 70 | Perth | 17.81 | 180,478 | 6 | 1 | 1 | - | 30 | measured |
| 71 | Des Moines | 18.11 | - | - | - | - | - | 10 | predicted (travel demand) |
| 72 | Daytona Beach | 17.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 73 | Melbourne | 11.68 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 74 | Reykjavik | 14.89 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 75 | Chattanooga | 16.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 76 | Sydney | 16.06 | 305,304 | 6 | - | - | - | 30 | measured |
| 77 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 78 | Spokane | 15.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 79 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 80 | Pittsburgh | 15.18 | - | - | - | - | - | 10 | predicted (travel demand) |
| 81 | Huntsville | 15.35 | - | - | - | - | - | 10 | predicted (travel demand) |
| 82 | Geneva | 10.22 | 162,269 | 21 | 4 | 4 | 131 | 20 | measured |
| 83 | Strasbourg | 10.22 | 154,700 | 10 | 1 | 2 | 66 | 30 | measured |
| 84 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 85 | West Palm Beach | 14.98 | - | - | - | - | - | 10 | predicted (travel demand) |
| 86 | Vilnius | 9.93 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 87 | Monterey | 14.58 | - | - | - | - | - | 10 | predicted (travel demand) |
| 88 | Saint Petersburg | 14.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 89 | St. Louis | 14.80 | - | - | - | - | - | 10 | predicted (travel demand) |
| 90 | Cyprus | 14.31 | - | 4 | - | - | - | 20 | measured |
| 91 | Eindhoven | 7.30 | - | 7 | - | 1 | 195 | 20 | measured |
| 92 | Budapest | 14.02 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 93 | Bordeaux | 9.64 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 94 | Tampa | 14.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 95 | Cadiz | 8.76 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 96 | Arnhem | 6.72 | 31,478 | 9 | 1 | 1 | 196 | 20 | measured |
| 97 | Sorrento | 6.72 | 40,049 | 6 | - | 1 | 20 | 20 | measured |
| 98 | Cincinnati | 13.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 99 | Lansing | 13.02 | - | - | - | - | - | 10 | predicted (travel demand) |
| 100 | Dallas | 12.85 | - | 8 | 1 | 1 | - | 30 | measured |
| 101 | Quebec City | 8.47 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 102 | Detroit | 12.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 103 | Tallinn | 8.18 | 124,888 | 4 | 2 | 1 | 42 | 20 | measured |
| 104 | Tulsa | 12.03 | - | - | - | - | - | 10 | predicted (travel demand) |
| 105 | Montreal | 12.26 | 315,322 | 7 | - | 1 | - | 30 | measured |
| 106 | Trieste | 5.84 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 107 | Denver | 11.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 108 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 109 | San Jose | 11.39 | - | - | - | - | - | 10 | predicted (travel demand) |
| 110 | Sacramento | 11.32 | - | - | - | - | - | 10 | predicted (travel demand) |
| 111 | Jersey City | 10.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 112 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 113 | Glasgow | 10.51 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 114 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 115 | Milwaukee | 10.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 116 | Warsaw | 7.01 | 197,929 | 19 | 3 | 2 | 1446 | 30 | measured |
| 117 | Istanbul | 9.20 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 118 | Salt Lake City | 10.31 | - | - | - | - | - | 10 | predicted (travel demand) |
| 119 | Atlanta | 10.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 120 | Washington DC | 9.34 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 121 | Anchorage | 10.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 122 | Nuremberg | 6.72 | 161,614 | 12 | 1 | 1 | 38 | 20 | measured |
| 123 | Raleigh | 10.07 | - | - | - | - | - | 10 | predicted (travel demand) |
| 124 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 125 | Cleveland | 9.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 126 | El Paso | 9.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 127 | Lyon | 6.42 | 136,951 | 13 | 3 | 1 | 156 | 20 | measured |
| 128 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 129 | Miami | 9.48 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 130 | Turku | 9.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 131 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 132 | Houston | 9.34 | - | 4 | - | - | - | 30 | measured |
| 133 | Maastricht | 4.67 | 47,763 | 14 | - | 1 | 137 | 20 | measured |
| 134 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 135 | Canberra | 9.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 136 | Pisa | 5.85 | 52,174 | - | - | - | - | 10 | predicted (travel demand) |
| 137 | Nashville | 8.93 | - | - | - | - | - | 10 | predicted (travel demand) |
| 138 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 139 | Dubrovnik | 8.18 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 140 | Ann Arbor | 8.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 141 | Salamanca | 5.50 | 47,897 | - | - | - | 1 | 10 | predicted (travel demand) |
| 142 | Graz | 5.55 | 65,717 | 12 | 3 | 1 | 87 | 20 | measured |
| 143 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 144 | Helsinki | 6.72 | 148,908 | 8 | 1 | - | 9 | 30 | measured |
| 145 | Rotterdam | 4.09 | 104,938 | 12 | - | 2 | 83 | 20 | measured |
| 146 | Oxford | 7.88 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 147 | Oslo | 7.01 | 181,113 | 4 | - | - | - | 20 | measured |
| 148 | Braga | 4.38 | 34,522 | 4 | 1 | - | 8 | 20 | measured |
| 149 | Mexico City | 7.45 | 566,583 | 9 | 1 | - | - | 30 | measured |
| 150 | Cork | 5.26 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 151 | Albuquerque | 7.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 152 | Minneapolis | 7.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 153 | Pamplona | 4.96 | 128,065 | 6 | - | - | 1 | 20 | measured |
| 154 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 155 | Catania | 4.38 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 156 | Potsdam | 4.96 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 157 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 158 | Guimaraes | 3.80 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 159 | Baltimore | 7.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 160 | Brno | 4.67 | 63,714 | 8 | 2 | 2 | 34 | 20 | measured |
| 161 | Lucca | 3.50 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 162 | Venlo | 3.50 | - | 7 | - | 1 | 144 | 20 | measured |
| 163 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 164 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 165 | Granada | 4.38 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 166 | Osaka | 4.38 | 163,112 | 5 | 1 | - | - | 30 | measured |
| 167 | Cordoba | 4.38 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 168 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 169 | Kauai | 5.84 | - | 6 | 1 | - | 8 | 20 | measured |
| 170 | Bilbao | 4.38 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 171 | Leipzig | 4.38 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 172 | Sapporo | 4.38 | 88,633 | 6 | - | - | - | 20 | measured |
| 173 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 174 | Kamakura | 4.09 | 33,492 | 6 | - | - | - | 20 | measured |
| 175 | Girona | 3.80 | 51,072 | 7 | - | - | - | 20 | measured |
| 176 | Trento | 3.21 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 177 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 178 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 179 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 180 | Bristol | 6.13 | 163,983 | 5 | 1 | - | - | 20 | measured |
| 181 | Hobart | 4.09 | 81,734 | 10 | - | 2 | 455 | 20 | measured |
| 182 | Poznan | 4.09 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 183 | Como | 2.92 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 184 | Dordrecht | 2.92 | - | 8 | - | 2 | 103 | 20 | measured |
| 185 | Tilburg | 2.92 | - | 7 | - | 1 | 84 | 20 | measured |
| 186 | Turin | 2.92 | 147,456 | 11 | 7 | 2 | 30 | 20 | measured |
| 187 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 188 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 189 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 190 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 191 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 192 | Verona | 3.21 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 193 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 194 | Riga | 5.26 | 108,918 | 5 | - | - | - | 20 | measured |
| 195 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 196 | Caserta | 2.63 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 197 | Delft | 2.63 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 198 | Bratislava | 3.50 | 132,162 | 6 | - | 1 | 26 | 30 | measured |
| 199 | Cardiff | 5.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 200 | Santa Fe | 5.17 | - | - | - | - | - | 10 | predicted (travel demand) |
| 201 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 202 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 203 | Lausanne | 4.90 | 68,242 | - | - | - | - | 10 | predicted (travel demand) |
| 204 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 205 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 206 | Bari | 2.92 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 207 | Los Angeles | 4.67 | 665,559 | 8 | 2 | - | - | 30 | measured |
| 208 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 209 | Frankfurt | 3.21 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 210 | Hong Kong | 3.21 | 689,212 | 10 | 2 | 1 | 505 | 20 | measured |
| 211 | Salzburg | 3.21 | 107,243 | 5 | - | - | 34 | 20 | measured |
| 212 | Ljubljana | 4.67 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 213 | San Francisco | 4.67 | 361,111 | 6 | - | 1 | - | 30 | measured |
| 214 | Alkmaar | 2.34 | - | 7 | - | 1 | 79 | 20 | measured |
| 215 | Heerlen | 2.34 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 216 | Leeuwarden | 2.34 | - | 8 | - | 1 | 61 | 20 | measured |
| 217 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 218 | Hawaii | 4.09 | - | 6 | - | 1 | 6 | 30 | measured |
| 219 | Aarhus | 4.38 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 220 | Vancouver | 4.38 | 351,552 | 4 | - | - | - | 30 | measured |
| 221 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 222 | Perugia | 2.34 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 223 | Nice | 4.38 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 224 | Toulouse | 2.92 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 225 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 226 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 227 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 228 | Apeldoorn | 2.04 | - | 9 | - | 2 | 80 | 20 | measured |
| 229 | Haarlem | 2.04 | 33,960 | 21 | - | 2 | 277 | 20 | measured |
| 230 | Helmond | 2.04 | - | 7 | - | 1 | 55 | 20 | measured |
| 231 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 232 | Zurich | 3.80 | 140,788 | 4 | - | - | - | 20 | measured |
| 233 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 234 | Nantes | 3.83 | 67,689 | - | - | - | - | 10 | predicted (travel demand) |
| 235 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 236 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 237 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 238 | Parma | 2.04 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 239 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 240 | Philadelphia | 3.50 | 405,294 | 1 | - | - | - | 20 | measured |
| 241 | Luxembourg City | 2.34 | 64,851 | 10 | - | 2 | 18 | 20 | measured |
| 242 | Amersfoort | 1.75 | - | 8 | 1 | 1 | 181 | 20 | measured |
| 243 | Assen | 1.75 | - | 9 | - | 2 | 67 | 20 | measured |
| 244 | Bergamo | 1.75 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 245 | Den Bosch | 1.75 | 39,682 | 11 | 1 | 1 | 119 | 20 | measured |
| 246 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 247 | Busan | 3.31 | 94,737 | - | - | - | - | 10 | predicted (travel demand) |
| 248 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 249 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 250 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 251 | San Antonio | 3.32 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 252 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 253 | Genoa | 1.75 | 145,206 | 12 | 1 | 1 | 11 | 20 | measured |
| 254 | Fort Worth | 3.28 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 255 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 256 | Cambridge | 3.21 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 257 | Cologne | 3.21 | 191,812 | 5 | - | 1 | - | 30 | measured |
| 258 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 259 | Menorca | 2.04 | - | 6 | - | - | 2 | 20 | measured |
| 260 | Sao Paulo | 2.96 | 911 | - | - | - | - | 10 | predicted (travel demand) |
| 261 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 262 | Maui | 2.92 | - | 4 | - | - | 3 | 20 | measured |
| 263 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 264 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 265 | Stockholm | 2.34 | 188,184 | 4 | 3 | - | - | 30 | measured |
| 266 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 267 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 268 | Hoorn | 1.46 | - | 8 | - | 1 | 52 | 20 | measured |
| 269 | Ibiza | 1.85 | - | 1 | - | - | 4 | 10 | predicted (travel demand) |
| 270 | Savannah | 2.92 | 128,162 | 2 | - | - | - | 20 | measured |
| 271 | Modena | 1.75 | 51,698 | 5 | - | 1 | 3 | 20 | measured |
| 272 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 273 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 274 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 275 | Coimbra | 1.46 | 34,962 | 4 | - | - | 5 | 20 | measured |
| 276 | Gdansk | 1.75 | 4,908 | 6 | 4 | - | 288 | 20 | measured |
| 277 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 278 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 279 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 280 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 281 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 282 | Tarragona | 1.46 | 32,396 | 4 | - | - | - | 20 | measured |
| 283 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 284 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 285 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 286 | Auckland | 2.34 | 152,056 | 5 | 1 | - | - | 20 | measured |
| 287 | Charleston | 2.34 | 155,987 | 2 | 1 | - | - | 20 | measured |
| 288 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 289 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 290 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 291 | Bangkok | 2.34 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 292 | Roosendaal | 1.17 | - | 8 | - | 1 | 116 | 20 | measured |
| 293 | Zwolle | 1.17 | - | 7 | - | 1 | 57 | 20 | measured |
| 294 | Hallstatt | 1.99 | 47,271 | - | - | - | - | 10 | predicted (travel demand) |
| 295 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 296 | Padua | 1.17 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 297 | Cesky Krumlov | 1.46 | 28,582 | 6 | 2 | - | 11 | 20 | measured |
| 298 | Ottawa | 1.46 | - | 8 | - | 1 | 119 | 20 | measured |
| 299 | Sofia | 1.46 | 138,710 | 4 | - | - | - | 30 | measured |
| 300 | Wroclaw | 1.46 | 123,894 | 5 | 1 | 1 | 121 | 20 | measured |
| 301 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 302 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 303 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 304 | Belgrade | 1.90 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 305 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 306 | Kanazawa | 1.17 | 25,778 | 7 | 1 | 1 | 2 | 20 | measured |
| 307 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 308 | Naha | 1.17 | 24,466 | 6 | - | - | 1 | 20 | measured |
| 309 | Deventer | 0.88 | - | 7 | - | 1 | 213 | 20 | measured |
| 310 | Enschede | 0.88 | - | 7 | 1 | 1 | 82 | 20 | measured |
| 311 | Hilversum | 0.88 | - | 6 | - | 1 | 122 | 20 | measured |
| 312 | Hiroshima | 1.17 | 129,791 | 8 | 1 | 2 | - | 20 | measured |
| 313 | Thessaloniki | 1.75 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 314 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 315 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 316 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 317 | Buenos Aires | 1.61 | 333,331 | 4 | 1 | - | - | 30 | measured |
| 318 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 319 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 320 | Freiburg | 1.54 | 92,752 | 7 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 321 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 322 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 323 | Ronda | 0.88 | 51,510 | 6 | - | - | 9 | 20 | measured |
| 324 | Antwerp | 1.46 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 325 | Belfast | 1.46 | 224,315 | 4 | - | 1 | - | 20 | measured |
| 326 | Bruges | 1.46 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 327 | Assisi | 0.88 | 30,278 | 6 | 1 | 2 | 6 | 20 | measured |
| 328 | Segovia | 0.88 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 329 | Rothenburg ob der Tauber | 1.17 | 39,879 | 4 | - | 1 | 8 | 20 | measured |
| 330 | Nagoya | 0.88 | 83,437 | 6 | - | - | 1 | 20 | measured |
| 331 | Dresden | 0.88 | 113,624 | 5 | 1 | 1 | - | 20 | measured |
| 332 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 333 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 334 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 335 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 336 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 337 | Kansas City | 1.17 | - | 4 | - | 1 | - | 30 | measured |
| 338 | York | 1.17 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 339 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 340 | Zaragoza | 0.73 | 87,580 | 7 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 341 | Setubal | 0.58 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 342 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 343 | Ferrara | 0.58 | 27,490 | 5 | 1 | 1 | 7 | 20 | measured |
| 344 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 345 | Regensburg | 0.88 | 51,930 | 5 | - | 1 | 4 | 20 | measured |
| 346 | Brighton | 0.88 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 347 | Liverpool | 0.88 | 248,189 | 2 | - | - | - | 20 | measured |
| 348 | Manchester | 0.88 | 316,438 | 5 | - | - | - | 30 | measured |
| 349 | Heidelberg | 0.67 | 75,837 | 6 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 350 | Ghent | 0.59 | 82,757 | 6 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 351 | Lima | 0.51 | 132,792 | 5 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 352 | Rouen | 0.54 | 72,334 | 12 | - | 1 | 6 | 10 | published, never ranked (may be uncrawled) |
| 353 | Breda | 0.29 | 36,579 | 4 | - | 1 | 119 | 20 | measured |
| 354 | Bucharest | 0.58 | 136,836 | 4 | - | 1 | - | 20 | measured |
| 355 | Gothenburg | 0.58 | 119,991 | 5 | - | 1 | - | 20 | measured |
| 356 | Leuven | 0.58 | 40,645 | 4 | - | - | - | 20 | measured |
| 357 | Rio de Janeiro | 0.58 | 279,431 | 6 | - | - | - | 30 | measured |
| 358 | San Diego | 0.58 | 214,939 | 4 | - | 1 | - | 20 | measured |
| 359 | Split | 0.58 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 360 | Phoenix | 0.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 361 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 362 | Yakushima | 0.29 | - | 1 | - | - | 1 | 20 | measured |
| 363 | Matera | 0.25 | 67,033 | 4 | - | - | 2 | 10 | published, never ranked (may be uncrawled) |
| 364 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 365 | Bamberg | 0.29 | 28,716 | 5 | 3 | 1 | 10 | 20 | measured |
| 366 | Stuttgart | 0.29 | 112,789 | 7 | - | - | - | 20 | measured |
| 367 | Hamburg | 0.29 | 191,221 | 6 | - | 1 | - | 30 | measured |
| 368 | Beijing | 0.29 | 269,737 | 6 | - | - | - | 30 | measured |
| 369 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 370 | Taipei | 0.29 | 143,193 | 4 | - | - | - | 30 | measured |
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

