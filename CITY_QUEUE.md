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
| 1 | Rome | 175.03 | 358,876 | 30 | 9 | 2 | 32 | 30 | measured |
| 2 | Amsterdam | 76.12 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 3 | Lisbon | 76.12 | 201,877 | 35 | 11 | 3 | 68 | 30 | measured |
| 4 | Barcelona | 64.47 | 346,477 | 56 | 12 | 7 | 180 | 30 | measured |
| 5 | Milan | 59.55 | 212,705 | 22 | 9 | 2 | 25 | 30 | measured |
| 6 | Brussels | 64.47 | 176,863 | 31 | 4 | 1 | 436 | 30 | measured |
| 7 | Singapore | 50.75 | 967,821 | 28 | 3 | 3 | 165 | 30 | measured |
| 8 | Seville | 46.60 | 170,545 | 43 | 6 | 2 | - | 20 | measured |
| 9 | Brisbane | 42.98 | 162,602 | 19 | 1 | 2 | 189 | 30 | measured |
| 10 | London | 52.04 | 718,291 | 23 | 10 | 1 | - | 30 | measured |
| 11 | Florence | 30.55 | 184,099 | 23 | 8 | 1 | 27 | 30 | measured |
| 12 | Prague | 39.10 | 303,350 | 18 | 13 | 3 | 30 | 30 | measured |
| 13 | Vienna | 35.47 | 283,090 | 32 | 13 | 5 | 376 | 30 | measured |
| 14 | Leiden | 26.15 | 33,227 | 12 | 4 | 1 | 129 | 20 | measured |
| 15 | Portland | 33.14 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 16 | Madeira | 28.48 | - | 10 | 1 | 1 | - | 20 | measured |
| 17 | Paris | 30.03 | 524,268 | 31 | 9 | 4 | 129 | 30 | measured |
| 18 | Alicante | 22.27 | 77,454 | 16 | 3 | 2 | 44 | 20 | measured |
| 19 | Palermo | 21.49 | 124,310 | 21 | 7 | 1 | 37 | 20 | measured |
| 20 | Tenerife | 27.96 | - | 4 | 1 | - | - | 20 | measured |
| 21 | Arnhem | 21.23 | 31,478 | 37 | 1 | 3 | 198 | 20 | measured |
| 22 | New York | 35.73 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 23 | Hilo | 30.55 | - | 6 | - | 1 | 16 | 20 | measured |
| 24 | Sardinia | 21.23 | - | 5 | 2 | - | 8 | 20 | measured |
| 25 | Birmingham | 37.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 26 | Kyoto | 23.30 | 142,353 | 17 | 8 | 2 | - | 20 | measured |
| 27 | Valencia | 18.12 | 162,209 | 25 | 2 | 2 | 350 | 30 | measured |
| 28 | Berlin | 23.30 | 412,181 | 19 | 11 | 1 | 195 | 30 | measured |
| 29 | Malaga | 23.04 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 30 | Fukuoka | 22.27 | 77,485 | 15 | 7 | 1 | - | 20 | measured |
| 31 | Sintra | 16.57 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 32 | Dublin | 17.87 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 33 | Oahu | 20.71 | - | 11 | 1 | - | 160 | 20 | measured |
| 34 | Copenhagen | 28.48 | 218,621 | 16 | 1 | 2 | - | 30 | measured |
| 35 | Naples | 14.76 | 198,913 | 24 | 3 | 3 | 46 | 20 | measured |
| 36 | Bologna | 15.28 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 37 | Krakow | 18.12 | 140,824 | 34 | 3 | 3 | 198 | 30 | measured |
| 38 | Venice | 13.98 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 39 | Palma de Mallorca | 15.28 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 40 | Boston | 23.82 | 385,902 | 11 | 1 | 1 | - | 30 | measured |
| 41 | Seattle | 23.82 | 398,724 | 6 | - | - | - | 30 | measured |
| 42 | Porto | 12.17 | 120,415 | 27 | 14 | 2 | 40 | 20 | measured |
| 43 | The Hague | 11.65 | 236,723 | 29 | 1 | 5 | 166 | 20 | measured |
| 44 | Munich | 15.53 | 224,067 | 45 | 14 | 6 | 80 | 30 | measured |
| 45 | Crete | 23.04 | - | 4 | 2 | - | - | 20 | measured |
| 46 | Austin | 22.78 | 226,631 | 5 | - | - | - | 20 | measured |
| 47 | Jacksonville | 22.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 48 | Athens | 21.75 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 49 | Nijmegen | 10.87 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 50 | Utrecht | 10.87 | 67,963 | 33 | 4 | 2 | 345 | 20 | measured |
| 51 | Asheville | 20.89 | - | - | - | - | - | 10 | predicted (travel demand) |
| 52 | Boise | 20.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 53 | Long Beach | 20.48 | - | - | - | - | - | 10 | predicted (travel demand) |
| 54 | Little Rock | 20.40 | - | - | - | - | - | 10 | predicted (travel demand) |
| 55 | Edinburgh | 19.16 | 292,981 | 16 | 4 | 1 | - | 30 | measured |
| 56 | Indianapolis | 18.28 | - | - | - | - | - | 10 | predicted (travel demand) |
| 57 | Oakland | 18.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 58 | Fort Lauderdale | 18.43 | - | - | - | - | - | 10 | predicted (travel demand) |
| 59 | Chicago | 18.64 | 485,769 | 6 | - | - | - | 30 | measured |
| 60 | Las Vegas | 18.64 | - | 11 | - | 2 | - | 30 | measured |
| 61 | Lexington | 18.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 62 | Reno | 18.19 | - | - | - | - | - | 10 | predicted (travel demand) |
| 63 | New Orleans | 18.12 | 256,232 | 4 | 2 | 1 | - | 20 | measured |
| 64 | Des Moines | 18.11 | - | - | - | - | - | 10 | predicted (travel demand) |
| 65 | Toronto | 17.61 | 411,011 | 6 | - | - | - | 30 | measured |
| 66 | Daytona Beach | 17.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 67 | Cagliari | 9.32 | 51,351 | 10 | 1 | 2 | 15 | 20 | measured |
| 68 | Geneva | 11.39 | 162,269 | 21 | 4 | 4 | 131 | 20 | measured |
| 69 | Melbourne | 11.39 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 70 | Vilnius | 11.39 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 71 | Los Angeles | 16.05 | 665,559 | 8 | 2 | - | - | 30 | measured |
| 72 | Chattanooga | 16.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 73 | Tokyo | 8.80 | 394,702 | 17 | 8 | 1 | 6 | 20 | measured |
| 74 | Budapest | 15.79 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 75 | Strasbourg | 10.87 | 154,700 | 10 | 1 | 2 | 66 | 30 | measured |
| 76 | Reykjavik | 13.98 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 77 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 78 | Spokane | 15.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 79 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 80 | Pittsburgh | 15.18 | - | - | - | - | - | 10 | predicted (travel demand) |
| 81 | Huntsville | 15.35 | - | - | - | - | - | 10 | predicted (travel demand) |
| 82 | Perth | 14.76 | 180,478 | 6 | 1 | 1 | - | 30 | measured |
| 83 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 84 | Houston | 15.02 | - | 4 | - | - | - | 30 | measured |
| 85 | West Palm Beach | 14.98 | - | - | - | - | - | 10 | predicted (travel demand) |
| 86 | Monterey | 14.58 | - | - | - | - | - | 10 | predicted (travel demand) |
| 87 | Saint Petersburg | 14.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 88 | Seoul | 13.72 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 89 | St. Louis | 14.80 | - | - | - | - | - | 10 | predicted (travel demand) |
| 90 | Tampa | 14.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 91 | Cadiz | 8.80 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 92 | Bath | 13.46 | 144,950 | 5 | 1 | 1 | - | 20 | measured |
| 93 | Groningen | 6.73 | 31,401 | 20 | - | 2 | 72 | 20 | measured |
| 94 | Cincinnati | 13.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 95 | Cyprus | 12.95 | - | 4 | - | - | - | 20 | measured |
| 96 | Lansing | 13.02 | - | - | - | - | - | 10 | predicted (travel demand) |
| 97 | Madrid | 7.77 | 274,553 | 17 | 10 | 2 | - | 20 | measured |
| 98 | Detroit | 12.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 99 | Haarlem | 6.21 | 33,960 | 21 | - | 2 | 277 | 20 | measured |
| 100 | Oslo | 10.87 | 181,113 | 4 | - | - | - | 20 | measured |
| 101 | Tulsa | 12.03 | - | - | - | - | - | 10 | predicted (travel demand) |
| 102 | Montreal | 12.17 | 315,322 | 7 | - | 1 | - | 30 | measured |
| 103 | Bordeaux | 8.03 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 104 | Dordrecht | 5.96 | - | 8 | - | 2 | 103 | 20 | measured |
| 105 | Denver | 11.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 106 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 107 | Eindhoven | 5.70 | - | 11 | - | 2 | 195 | 20 | measured |
| 108 | Dallas | 11.39 | - | 8 | 1 | 1 | - | 30 | measured |
| 109 | San Jose | 11.39 | - | - | - | - | - | 10 | predicted (travel demand) |
| 110 | Sacramento | 11.32 | - | - | - | - | - | 10 | predicted (travel demand) |
| 111 | Jersey City | 10.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 112 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 113 | Sydney | 10.87 | 305,304 | 7 | - | - | - | 30 | measured |
| 114 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 115 | Sorrento | 5.44 | 40,049 | 6 | - | 1 | 20 | 20 | measured |
| 116 | Milwaukee | 10.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 117 | San Francisco | 10.36 | 361,111 | 6 | - | 1 | - | 30 | measured |
| 118 | Istanbul | 9.19 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 119 | Lyon | 6.99 | 136,951 | 13 | 3 | 1 | 156 | 20 | measured |
| 120 | Salt Lake City | 10.31 | - | - | - | - | - | 10 | predicted (travel demand) |
| 121 | Atlanta | 10.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 122 | Anchorage | 10.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 123 | Glasgow | 9.58 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 124 | Raleigh | 10.07 | - | - | - | - | - | 10 | predicted (travel demand) |
| 125 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 126 | Trento | 4.92 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 127 | Cleveland | 9.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 128 | El Paso | 9.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 129 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 130 | Miami | 9.48 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 131 | Granada | 5.96 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 132 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 133 | Nuremberg | 6.21 | 161,614 | 12 | 1 | 1 | 38 | 20 | measured |
| 134 | Quebec City | 6.21 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 135 | Tallinn | 6.21 | 124,888 | 4 | 2 | 1 | 42 | 20 | measured |
| 136 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 137 | Pisa | 5.85 | 52,174 | - | - | - | - | 10 | predicted (travel demand) |
| 138 | Nashville | 8.93 | - | - | - | - | - | 10 | predicted (travel demand) |
| 139 | Maastricht | 4.40 | 47,763 | 14 | - | 1 | 137 | 20 | measured |
| 140 | Venlo | 4.40 | - | 7 | - | 1 | 144 | 20 | measured |
| 141 | Pamplona | 5.70 | 128,065 | 6 | - | - | 1 | 20 | measured |
| 142 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 143 | Kamakura | 5.44 | 33,492 | 6 | - | - | - | 20 | measured |
| 144 | Philadelphia | 8.29 | 405,294 | 1 | - | - | - | 20 | measured |
| 145 | Ann Arbor | 8.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 146 | Warsaw | 5.70 | 197,929 | 19 | 3 | 2 | 1446 | 30 | measured |
| 147 | Salamanca | 5.50 | 47,897 | - | - | - | 1 | 10 | predicted (travel demand) |
| 148 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 149 | Cork | 5.44 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 150 | Braga | 4.40 | 34,522 | 4 | 1 | - | 8 | 20 | measured |
| 151 | Girona | 4.66 | 51,072 | 7 | - | - | - | 20 | measured |
| 152 | Albuquerque | 7.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 153 | Kauai | 6.73 | - | 6 | 1 | - | 8 | 20 | measured |
| 154 | Sapporo | 5.18 | 88,633 | 6 | - | - | - | 20 | measured |
| 155 | Helmond | 3.88 | - | 7 | - | 1 | 55 | 20 | measured |
| 156 | Tilburg | 3.88 | - | 15 | - | 2 | 85 | 20 | measured |
| 157 | Trieste | 3.88 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 158 | Dubrovnik | 7.25 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 159 | Minneapolis | 7.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 160 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 161 | Washington DC | 6.73 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 162 | Leipzig | 4.92 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 163 | Luxembourg City | 4.92 | 64,851 | 10 | - | 2 | 18 | 20 | measured |
| 164 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 165 | Baltimore | 7.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 166 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 167 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 168 | Riga | 6.73 | 108,918 | 5 | - | - | - | 20 | measured |
| 169 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 170 | Graz | 4.40 | 65,717 | 12 | 3 | 1 | 87 | 20 | measured |
| 171 | Verona | 3.88 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 172 | Mexico City | 6.21 | 566,583 | 9 | 1 | - | - | 30 | measured |
| 173 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 174 | Bari | 3.88 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 175 | Parma | 3.62 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 176 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 177 | Hawaii | 5.70 | - | 6 | - | 1 | 6 | 30 | measured |
| 178 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 179 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 180 | Rotterdam | 3.11 | 104,938 | 12 | - | 2 | 83 | 20 | measured |
| 181 | Turin | 3.11 | 147,456 | 11 | 7 | 2 | 30 | 20 | measured |
| 182 | Oxford | 5.96 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 183 | Bilbao | 3.88 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 184 | Hobart | 3.88 | 81,734 | 11 | - | 2 | 455 | 20 | measured |
| 185 | Potsdam | 3.88 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 186 | Salzburg | 3.88 | 107,243 | 5 | - | - | 34 | 20 | measured |
| 187 | Vancouver | 5.70 | 351,552 | 4 | - | - | - | 30 | measured |
| 188 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 189 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 190 | Zwolle | 2.85 | - | 7 | - | 1 | 57 | 20 | measured |
| 191 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 192 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 193 | Helsinki | 4.40 | 148,908 | 10 | 1 | - | 12 | 30 | measured |
| 194 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 195 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 196 | Osaka | 3.37 | 163,112 | 5 | 1 | - | - | 30 | measured |
| 197 | Catania | 3.11 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 198 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 199 | Coimbra | 2.85 | 34,962 | 4 | - | - | 5 | 20 | measured |
| 200 | Cardiff | 5.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 201 | Caserta | 2.59 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 202 | Hoorn | 2.59 | - | 8 | - | 1 | 52 | 20 | measured |
| 203 | Santa Fe | 5.17 | - | - | - | - | - | 10 | predicted (travel demand) |
| 204 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 205 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 206 | Poznan | 3.37 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 207 | Ljubljana | 4.92 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 208 | Lausanne | 4.90 | 68,242 | - | - | - | - | 10 | predicted (travel demand) |
| 209 | Guimaraes | 2.59 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 210 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 211 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 212 | Stuttgart | 4.14 | 112,789 | 7 | - | - | - | 20 | measured |
| 213 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 214 | Menorca | 3.11 | - | 6 | - | - | 2 | 20 | measured |
| 215 | Bergamo | 2.33 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 216 | Bristol | 4.66 | 163,983 | 6 | 1 | - | - | 20 | measured |
| 217 | Leeuwarden | 2.33 | - | 8 | - | 1 | 61 | 20 | measured |
| 218 | Lucca | 2.33 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 219 | Nice | 4.66 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 220 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 221 | Aarhus | 4.40 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 222 | Hong Kong | 2.98 | 689,212 | 10 | 2 | 1 | 505 | 20 | measured |
| 223 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 224 | Perugia | 2.33 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 225 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 226 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 227 | Heerlen | 2.07 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 228 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 229 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 230 | Cordoba | 2.59 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 231 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 232 | Brno | 2.59 | 63,714 | 8 | 2 | 2 | 34 | 20 | measured |
| 233 | Frankfurt | 2.59 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 234 | Hiroshima | 2.59 | 129,791 | 15 | 1 | 3 | - | 20 | measured |
| 235 | Modena | 2.33 | 51,698 | 5 | - | 1 | 3 | 20 | measured |
| 236 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 237 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 238 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 239 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 240 | Amersfoort | 1.81 | - | 8 | 1 | 1 | 181 | 20 | measured |
| 241 | Den Bosch | 1.81 | 39,682 | 11 | 1 | 1 | 119 | 20 | measured |
| 242 | Savannah | 3.62 | 128,162 | 2 | - | - | - | 20 | measured |
| 243 | Bratislava | 2.33 | 132,162 | 7 | - | 1 | 26 | 30 | measured |
| 244 | Ottawa | 2.33 | - | 8 | - | 1 | 119 | 20 | measured |
| 245 | Toulouse | 2.33 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 246 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 247 | Busan | 3.31 | 94,737 | - | - | - | - | 10 | predicted (travel demand) |
| 248 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 249 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 250 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 251 | Cambridge | 3.37 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 252 | Cologne | 3.37 | 191,812 | 5 | - | 1 | - | 30 | measured |
| 253 | Manchester | 3.37 | 316,438 | 5 | - | - | - | 30 | measured |
| 254 | Stockholm | 2.59 | 188,184 | 4 | 3 | - | - | 30 | measured |
| 255 | San Antonio | 3.32 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 256 | Segovia | 2.07 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 257 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 258 | Maui | 3.11 | - | 4 | - | - | 3 | 20 | measured |
| 259 | Fort Worth | 3.28 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 260 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 261 | Nagoya | 2.07 | 83,437 | 6 | - | - | 1 | 20 | measured |
| 262 | Naha | 2.07 | 24,466 | 6 | - | - | 1 | 20 | measured |
| 263 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 264 | Sao Paulo | 2.96 | 911 | - | - | - | - | 10 | predicted (travel demand) |
| 265 | Alkmaar | 1.55 | - | 7 | - | 1 | 79 | 20 | measured |
| 266 | Como | 1.55 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 267 | Delft | 1.55 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 268 | Enschede | 1.55 | - | 7 | 1 | 1 | 82 | 20 | measured |
| 269 | Hilversum | 1.55 | - | 6 | - | 1 | 122 | 20 | measured |
| 270 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 271 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 272 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 273 | Tarragona | 1.81 | 32,396 | 4 | - | - | - | 20 | measured |
| 274 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 275 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 276 | Zurich | 2.85 | 140,788 | 6 | - | - | - | 20 | measured |
| 277 | Auckland | 2.85 | 152,056 | 5 | 1 | - | - | 20 | measured |
| 278 | Genoa | 1.55 | 145,206 | 12 | 1 | 1 | 11 | 20 | measured |
| 279 | Bruges | 2.85 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 280 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 281 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 282 | Cesky Krumlov | 1.81 | 28,582 | 6 | 2 | - | 11 | 20 | measured |
| 283 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 284 | Charleston | 2.59 | 155,987 | 2 | 1 | - | - | 20 | measured |
| 285 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 286 | San Diego | 2.59 | 214,939 | 4 | - | 1 | - | 20 | measured |
| 287 | Assen | 1.29 | - | 9 | - | 2 | 67 | 20 | measured |
| 288 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 289 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 290 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 291 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 292 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 293 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 294 | Padua | 1.29 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 295 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 296 | Setubal | 1.29 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 297 | Kanazawa | 1.55 | 25,778 | 7 | 1 | 1 | 2 | 20 | measured |
| 298 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 299 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 300 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 301 | Gdansk | 1.55 | 4,908 | 6 | 4 | - | 288 | 20 | measured |
| 302 | Hallstatt | 1.99 | 47,271 | - | - | - | - | 10 | predicted (travel demand) |
| 303 | Turku | 2.31 | - | 1 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 304 | Canberra | 2.28 | - | 1 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 305 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 306 | Deventer | 1.04 | - | 7 | - | 1 | 213 | 20 | measured |
| 307 | Roosendaal | 1.04 | - | 8 | - | 1 | 116 | 20 | measured |
| 308 | Beijing | 2.07 | 269,737 | 7 | - | - | - | 30 | measured |
| 309 | Belfast | 2.07 | 224,315 | 4 | - | 1 | - | 20 | measured |
| 310 | Kansas City | 2.07 | - | 4 | - | 1 | - | 30 | measured |
| 311 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 312 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 313 | Buenos Aires | 1.94 | 333,331 | 4 | 1 | - | - | 30 | measured |
| 314 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 315 | Ghent | 1.81 | 82,757 | 6 | - | 1 | - | 20 | measured |
| 316 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 317 | Rio de Janeiro | 1.81 | 279,431 | 6 | - | - | - | 30 | measured |
| 318 | Thessaloniki | 1.81 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 319 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 320 | Matera | 1.04 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 321 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 322 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 323 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 324 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 325 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 326 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 327 | Apeldoorn | 0.78 | - | 9 | - | 2 | 80 | 20 | measured |
| 328 | Sofia | 1.04 | 138,710 | 4 | - | - | - | 30 | measured |
| 329 | Bangkok | 1.55 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 330 | Rothenburg ob der Tauber | 1.29 | 39,879 | 4 | - | 1 | 8 | 20 | measured |
| 331 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 332 | Ronda | 0.78 | 51,510 | 6 | - | - | 9 | 20 | measured |
| 333 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 334 | Antwerp | 1.29 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 335 | Gothenburg | 1.29 | 119,991 | 5 | - | 1 | - | 20 | measured |
| 336 | Liverpool | 1.29 | 248,189 | 2 | - | - | - | 20 | measured |
| 337 | York | 1.29 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 338 | Breda | 0.64 | 36,579 | 4 | - | 1 | 119 | 10 | published, never ranked (may be uncrawled) |
| 339 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 340 | Assisi | 0.78 | 30,278 | 6 | 1 | 2 | 6 | 20 | measured |
| 341 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 342 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 343 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 344 | Belgrade | 1.17 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 345 | Dresden | 0.78 | 113,624 | 5 | 1 | 1 | - | 20 | measured |
| 346 | Wroclaw | 0.78 | 123,894 | 5 | 1 | 1 | 121 | 20 | measured |
| 347 | Rouen | 1.04 | 72,334 | 12 | - | 1 | 6 | 20 | measured |
| 348 | Regensburg | 1.04 | 51,930 | 5 | - | 1 | 4 | 20 | measured |
| 349 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 350 | Zaragoza | 0.73 | 87,580 | 7 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 351 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 352 | Brighton | 1.04 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 353 | Taipei | 1.04 | 143,193 | 4 | - | - | - | 30 | measured |
| 354 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 355 | Nantes | 0.96 | 67,689 | 1 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 356 | Ibiza | 0.46 | - | 1 | - | - | 4 | 10 | published, never ranked (may be uncrawled) |
| 357 | Lima | 0.51 | 132,792 | 5 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 358 | Heidelberg | 0.52 | 75,837 | 6 | - | 1 | - | 20 | measured |
| 359 | Hamburg | 0.52 | 191,221 | 6 | - | 1 | - | 30 | measured |
| 360 | Phoenix | 0.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 361 | Leuven | 0.52 | 40,645 | 4 | - | - | - | 20 | measured |
| 362 | Split | 0.52 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 363 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 364 | Yakushima | 0.26 | - | 1 | - | - | 1 | 20 | measured |
| 365 | Ferrara | 0.21 | 27,490 | 5 | 1 | 1 | 7 | 10 | published, never ranked (may be uncrawled) |
| 366 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 367 | Bamberg | 0.26 | 28,716 | 5 | 3 | 1 | 10 | 20 | measured |
| 368 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 369 | George Town | 0.28 | 36,080 | - | - | - | - | 10 | predicted (travel demand) |
| 370 | Freiburg | 0.26 | 92,752 | 7 | - | 1 | - | 20 | measured |
| 371 | Bucharest | 0.26 | 136,836 | 4 | - | 1 | - | 20 | measured |
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

