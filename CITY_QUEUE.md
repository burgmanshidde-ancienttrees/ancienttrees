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
| 1 | Pamplona | 89.15 | 128,065 | 14 | - | 1 | 9 | 20 | measured |
| 2 | Oahu | 85.93 | - | 21 | 2 | 3 | 163 | 30 | measured |
| 3 | Brussels | 77.44 | 176,863 | 35 | 4 | 2 | 436 | 60 | measured |
| 4 | Lisbon | 56.72 | 201,877 | 36 | 16 | 3 | 67 | 30 | measured |
| 5 | Amsterdam | 48.91 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 6 | Barcelona | 48.74 | 346,477 | 56 | 14 | 7 | 180 | 60 | measured |
| 7 | Singapore | 55.87 | 967,821 | 34 | 7 | 3 | 165 | 100 | measured |
| 8 | Rome | 39.91 | 358,876 | 31 | 10 | 2 | 32 | 60 | measured |
| 9 | Palermo | 38.38 | 124,310 | 21 | 9 | 1 | 37 | 30 | measured |
| 10 | Tokyo | 42.62 | 394,702 | 22 | 10 | 1 | 5 | 100 | measured |
| 11 | Arnhem | 37.53 | 31,478 | 39 | 3 | 3 | 204 | 20 | measured |
| 12 | Tenerife | 44.15 | - | 4 | 4 | - | - | 30 | measured |
| 13 | Berlin | 44.49 | 412,181 | 33 | 23 | 3 | 195 | 60 | measured |
| 14 | Seville | 39.06 | 170,545 | 43 | 9 | 2 | - | 30 | measured |
| 15 | Alicante | 29.21 | 77,454 | 21 | 4 | 2 | 44 | 30 | measured |
| 16 | Milan | 28.02 | 212,705 | 30 | 14 | 3 | 25 | 60 | measured |
| 17 | Prague | 37.02 | 303,350 | 30 | 21 | 4 | 31 | 60 | measured |
| 18 | New York | 48.57 | 1,124,326 | 20 | 5 | 2 | - | 100 | measured |
| 19 | Portland | 34.30 | 217,222 | 20 | 1 | 2 | 301 | 30 | measured |
| 20 | Vienna | 31.08 | 283,090 | 32 | 18 | 5 | 376 | 60 | measured |
| 21 | Bath | 45.34 | 144,950 | 5 | 2 | 1 | - | 20 | measured |
| 22 | Florence | 21.57 | 184,099 | 27 | 9 | 1 | 27 | 30 | measured |
| 23 | Austin | 42.11 | 226,631 | 5 | 2 | - | - | 30 | measured |
| 24 | Malaga | 27.68 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 25 | Brisbane | 27.17 | 162,602 | 20 | 2 | 2 | 186 | 60 | measured |
| 26 | Munich | 27.00 | 224,067 | 45 | 15 | 6 | 80 | 60 | measured |
| 27 | Philadelphia | 38.72 | 405,294 | 1 | - | - | - | 60 | measured |
| 28 | Paris | 26.49 | 524,268 | 31 | 9 | 4 | 129 | 60 | measured |
| 29 | Porto | 19.19 | 120,415 | 27 | 15 | 2 | 40 | 30 | measured |
| 30 | Valencia | 19.19 | 162,209 | 31 | 4 | 2 | 350 | 30 | measured |
| 31 | Birmingham | 37.53 | - | - | - | - | - | 60 | predicted (travel demand) |
| 32 | Los Angeles | 31.93 | 665,559 | 8 | 2 | - | - | 60 | measured |
| 33 | Utrecht | 15.96 | 67,963 | 27 | 7 | 2 | 340 | 30 | measured |
| 34 | Dublin | 18.34 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 35 | London | 26.83 | 718,291 | 23 | 14 | 1 | - | 100 | measured |
| 36 | Krakow | 19.53 | 140,824 | 38 | 8 | 3 | 198 | 30 | measured |
| 37 | Cagliari | 15.45 | 51,351 | 14 | 1 | 2 | 15 | 20 | measured |
| 38 | Sintra | 13.92 | 46,889 | 5 | 3 | - | 6 | 30 | measured |
| 39 | Cadiz | 17.66 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 40 | Edinburgh | 26.83 | 292,981 | 16 | 5 | 1 | - | 30 | measured |
| 41 | Monterey | 27.17 | - | 3 | 1 | - | - | 10 | measured |
| 42 | Houston | 26.83 | - | 6 | - | - | - | 60 | measured |
| 43 | Venice | 14.26 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 44 | Dallas | 25.81 | - | 9 | 1 | 1 | - | 60 | measured |
| 45 | The Hague | 12.74 | 236,723 | 31 | 2 | 5 | 167 | 30 | measured |
| 46 | New Orleans | 25.47 | 256,232 | 6 | 2 | 1 | - | 30 | measured |
| 47 | Cork | 15.28 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 48 | Jacksonville | 22.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 49 | Fukuoka | 14.60 | 77,485 | 15 | 9 | 1 | - | 60 | measured |
| 50 | Palma de Mallorca | 13.42 | 84,075 | 5 | 1 | 1 | 8 | 30 | measured |
| 51 | Haarlem | 10.53 | 33,960 | 21 | 1 | 2 | 277 | 20 | measured |
| 52 | Asheville | 20.89 | - | - | - | - | - | 20 | predicted (travel demand) |
| 53 | Nijmegen | 10.36 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 54 | Boston | 19.70 | 385,902 | 11 | 2 | 1 | - | 30 | measured |
| 55 | Long Beach | 20.48 | - | - | - | - | - | 30 | predicted (travel demand) |
| 56 | Kyoto | 13.08 | 142,353 | 18 | 12 | 2 | - | 60 | measured |
| 57 | Little Rock | 20.40 | - | - | - | - | - | 20 | predicted (travel demand) |
| 58 | Glasgow | 18.85 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 59 | Athens | 18.68 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 60 | Sao Paulo | 18.17 | 911 | 1 | - | - | - | 100 | measured |
| 61 | Oakland | 18.81 | - | - | - | - | - | 30 | predicted (travel demand) |
| 62 | Leiden | 9.17 | 33,227 | 20 | 6 | 1 | 129 | 20 | measured |
| 63 | Sardinia | 10.19 | - | 5 | 4 | - | 8 | 60 | measured |
| 64 | Lexington | 18.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 65 | Reno | 18.19 | - | - | - | - | - | 30 | predicted (travel demand) |
| 66 | Coimbra | 9.85 | 34,962 | 4 | - | - | 5 | 20 | measured |
| 67 | Des Moines | 18.11 | - | - | - | - | - | 20 | predicted (travel demand) |
| 68 | Las Vegas | 18.00 | - | 11 | - | 2 | - | 30 | measured |
| 69 | Madrid | 11.04 | 274,553 | 17 | 11 | 2 | - | 60 | measured |
| 70 | Copenhagen | 17.15 | 218,621 | 42 | 34 | 6 | - | 30 | measured |
| 71 | Warsaw | 11.89 | 197,929 | 39 | 5 | 4 | 1407 | 60 | measured |
| 72 | Daytona Beach | 17.66 | - | - | - | - | - | 20 | predicted (travel demand) |
| 73 | Ottawa | 11.72 | - | 21 | - | 3 | 122 | 60 | measured |
| 74 | Geneva | 11.38 | 162,269 | 21 | 5 | 4 | 131 | 20 | measured |
| 75 | San Francisco | 16.64 | 361,111 | 6 | 1 | 1 | - | 30 | measured |
| 76 | Chattanooga | 16.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 77 | Vilnius | 10.87 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 78 | Madeira | 9.68 | - | 10 | 1 | 1 | - | 30 | measured |
| 79 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 80 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 81 | Chicago | 15.62 | 485,769 | 6 | - | - | - | 60 | measured |
| 82 | Reykjavik | 13.42 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 83 | Granada | 9.85 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 84 | Huntsville | 15.35 | - | - | - | - | - | 20 | predicted (travel demand) |
| 85 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 86 | West Palm Beach | 14.98 | - | - | - | - | - | 20 | predicted (travel demand) |
| 87 | Washington DC | 13.59 | 606,731 | 15 | 1 | 3 | - | 30 | measured |
| 88 | Saint Petersburg | 14.83 | - | - | - | - | - | 100 | predicted (travel demand) |
| 89 | St. Louis | 14.80 | - | - | - | - | - | 30 | predicted (travel demand) |
| 90 | Tilburg | 7.30 | - | 20 | - | 3 | 87 | 20 | measured |
| 91 | Seattle | 13.92 | 398,724 | 6 | 1 | - | - | 30 | measured |
| 92 | Tampa | 14.10 | - | - | - | - | - | 30 | predicted (travel demand) |
| 93 | Cincinnati | 13.33 | - | - | - | - | - | 30 | predicted (travel demand) |
| 94 | Lansing | 13.02 | - | - | - | - | - | 20 | predicted (travel demand) |
| 95 | Detroit | 12.53 | - | - | - | - | - | 30 | predicted (travel demand) |
| 96 | Parma | 6.96 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 97 | Groningen | 6.11 | 31,401 | 21 | 1 | 2 | 76 | 20 | measured |
| 98 | Kanazawa | 7.81 | 25,778 | 7 | 2 | 1 | 2 | 30 | measured |
| 99 | Montreal | 11.89 | 315,322 | 13 | 1 | 2 | - | 60 | measured |
| 100 | Eindhoven | 5.94 | - | 21 | - | 4 | 195 | 20 | measured |
| 101 | Hobart | 7.81 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 102 | Denver | 11.66 | - | - | - | - | - | 30 | predicted (travel demand) |
| 103 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 60 | predicted (travel demand) |
| 104 | San Jose | 11.39 | - | - | - | - | - | 60 | predicted (travel demand) |
| 105 | Sacramento | 11.32 | - | - | - | - | - | 30 | predicted (travel demand) |
| 106 | Jersey City | 10.08 | - | - | - | - | - | 30 | predicted (travel demand) |
| 107 | Melbourne | 7.47 | 267,898 | 16 | - | 2 | 403 | 100 | measured |
| 108 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 60 | predicted (travel demand) |
| 109 | Bari | 6.62 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 110 | Osaka | 7.13 | 163,112 | 6 | 1 | - | - | 60 | measured |
| 111 | Dubai | 11.02 | 334,167 | - | - | - | - | 60 | predicted (travel demand) |
| 112 | Milwaukee | 10.63 | - | - | - | - | - | 30 | predicted (travel demand) |
| 113 | Sorrento | 5.26 | 40,049 | 7 | - | 1 | 20 | 10 | measured |
| 114 | Leipzig | 6.96 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 115 | Salt Lake City | 10.31 | - | - | - | - | - | 20 | predicted (travel demand) |
| 116 | Atlanta | 10.29 | - | - | - | - | - | 30 | predicted (travel demand) |
| 117 | Anchorage | 10.25 | - | - | - | - | - | 30 | predicted (travel demand) |
| 118 | Budapest | 9.85 | 283,807 | 12 | 1 | 3 | - | 60 | measured |
| 119 | Ibiza | 6.45 | - | 1 | - | - | 4 | 20 | measured |
| 120 | Raleigh | 10.07 | - | - | - | - | - | 30 | predicted (travel demand) |
| 121 | Pittsburgh | 9.85 | - | 4 | - | 1 | - | 30 | measured |
| 122 | Segovia | 6.28 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 123 | Bali | 9.95 | - | - | - | - | - | 60 | predicted (travel demand) |
| 124 | Leeuwarden | 4.92 | - | 41 | - | 2 | 61 | 20 | measured |
| 125 | Spokane | 7.13 | - | 13 | - | 2 | 18 | 20 | measured |
| 126 | Cleveland | 9.76 | - | - | - | - | - | 30 | predicted (travel demand) |
| 127 | El Paso | 9.70 | - | - | - | - | - | 30 | predicted (travel demand) |
| 128 | Yakushima | 6.11 | - | 2 | - | - | 1 | 10 | measured |
| 129 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 130 | Miami | 9.48 | 278,558 | - | - | - | - | 30 | predicted (travel demand) |
| 131 | Edmonton | 9.38 | - | - | - | - | - | 60 | predicted (travel demand) |
| 132 | Winnipeg | 9.21 | - | - | - | - | - | 30 | predicted (travel demand) |
| 133 | Naples | 4.59 | 198,913 | 24 | 3 | 3 | 46 | 30 | measured |
| 134 | Nashville | 8.93 | - | - | - | - | - | 30 | predicted (travel demand) |
| 135 | Strasbourg | 5.94 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 136 | Amersfoort | 4.42 | - | 18 | 1 | 2 | 181 | 20 | measured |
| 137 | Zurich | 8.49 | 140,788 | 6 | 1 | - | - | 30 | measured |
| 138 | Tampere | 8.78 | - | - | - | - | - | 30 | predicted (travel demand) |
| 139 | Charleston | 8.49 | 155,987 | 2 | 1 | - | - | 20 | measured |
| 140 | Bordeaux | 5.77 | 156,201 | 10 | - | 2 | 211 | 30 | measured |
| 141 | Ann Arbor | 8.55 | - | - | - | - | - | 20 | predicted (travel demand) |
| 142 | Dordrecht | 4.25 | - | 20 | 1 | 2 | 105 | 20 | measured |
| 143 | Crete | 8.49 | - | 4 | 3 | - | - | 30 | measured |
| 144 | Sydney | 8.32 | 305,304 | 7 | 1 | - | - | 100 | measured |
| 145 | Adelaide | 8.14 | 139,166 | - | - | - | - | 60 | predicted (travel demand) |
| 146 | Helmond | 4.08 | - | 20 | - | 2 | 54 | 20 | measured |
| 147 | Nice | 7.98 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 148 | Stockholm | 6.28 | 188,184 | 6 | 4 | - | - | 30 | measured |
| 149 | Seoul | 7.30 | 206,265 | 8 | 5 | 1 | - | 100 | measured |
| 150 | Albuquerque | 7.83 | - | - | - | - | - | 30 | predicted (travel demand) |
| 151 | Hoorn | 3.91 | - | 12 | - | 2 | 52 | 20 | measured |
| 152 | Savannah | 7.81 | 128,162 | 2 | 1 | - | - | 20 | measured |
| 153 | Cyprus | 7.47 | - | 4 | - | - | - | 60 | measured |
| 154 | Menorca | 4.92 | - | 6 | - | - | 2 | 20 | measured |
| 155 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 20 | predicted (travel demand) |
| 156 | Toronto | 7.30 | 411,011 | 6 | - | - | - | 60 | measured |
| 157 | Bergen | 7.30 | 82,940 | - | - | - | - | 30 | predicted (travel demand) |
| 158 | Leuven | 7.30 | 40,645 | 4 | - | - | - | 20 | measured |
| 159 | Hawaii | 6.45 | - | 6 | - | 1 | 6 | 60 | measured |
| 160 | Dubrovnik | 6.79 | 119,586 | 4 | 1 | - | 2 | 10 | measured |
| 161 | Boise | 7.13 | - | 4 | - | 1 | - | 20 | measured |
| 162 | Quebec City | 4.75 | 124,358 | 6 | - | 1 | 494 | 30 | measured |
| 163 | Helsinki | 5.60 | 148,908 | 12 | 2 | 1 | 13 | 30 | measured |
| 164 | Istanbul | 6.11 | 333,027 | 14 | 4 | 1 | - | 100 | measured |
| 165 | Cambridge | 6.96 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 166 | Catania | 4.08 | 58,252 | 4 | 3 | 1 | 5 | 30 | measured |
| 167 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 20 | predicted (travel demand) |
| 168 | Siena | 4.62 | 57,436 | - | - | - | - | 20 | predicted (travel demand) |
| 169 | Potsdam | 4.59 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 170 | Tallinn | 4.59 | 124,888 | 9 | 3 | 2 | 42 | 30 | measured |
| 171 | Guimaraes | 3.57 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 172 | Enschede | 3.40 | - | 15 | 1 | 2 | 82 | 20 | measured |
| 173 | Maastricht | 3.40 | 47,763 | 19 | - | 2 | 135 | 20 | measured |
| 174 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 20 | predicted (travel demand) |
| 175 | Zagreb | 6.42 | 122,890 | - | - | - | - | 30 | predicted (travel demand) |
| 176 | Bogota | 6.39 | 1,623 | - | - | - | - | 100 | predicted (travel demand) |
| 177 | Lyon | 4.25 | 136,951 | 13 | 4 | 1 | 156 | 30 | measured |
| 178 | Sapporo | 4.25 | 88,633 | 6 | - | - | - | 60 | measured |
| 179 | Shanghai | 6.38 | 277,140 | - | - | - | - | 100 | predicted (travel demand) |
| 180 | Beijing | 6.37 | 269,737 | 7 | 1 | - | - | 100 | measured |
| 181 | Verona | 3.74 | 77,646 | 8 | 4 | 1 | 3 | 30 | measured |
| 182 | Funchal | 3.77 | 174,351 | - | - | - | - | 20 | predicted (travel demand) |
| 183 | Caserta | 3.06 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 184 | Bristol | 6.11 | 163,983 | 6 | 2 | - | - | 30 | measured |
| 185 | Girona | 3.57 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 186 | Padua | 3.23 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 187 | Ljubljana | 5.94 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 188 | Perth | 5.94 | 180,478 | 6 | 3 | 1 | - | 60 | measured |
| 189 | Vancouver | 5.94 | 351,552 | 7 | - | - | - | 30 | measured |
| 190 | Oslo | 5.26 | 181,113 | 4 | - | - | - | 30 | measured |
| 191 | Hong Kong | 3.99 | 689,212 | 10 | 4 | 1 | 505 | 100 | measured |
| 192 | Genoa | 3.23 | 145,206 | 13 | 2 | 1 | 10 | 30 | measured |
| 193 | Malta | 5.79 | - | - | - | - | - | 30 | predicted (travel demand) |
| 194 | Minneapolis | 5.77 | - | 4 | - | - | - | 30 | measured |
| 195 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 196 | Luxembourg City | 3.74 | 64,851 | 10 | 5 | 2 | 18 | 20 | measured |
| 197 | Salzburg | 3.74 | 107,243 | 9 | 3 | 2 | 34 | 20 | measured |
| 198 | Avignon | 5.54 | 64,047 | - | - | - | - | 20 | predicted (travel demand) |
| 199 | Galway | 3.65 | 88,162 | - | - | - | - | 20 | predicted (travel demand) |
| 200 | Phuket | 5.46 | 5,487 | - | - | - | - | 30 | predicted (travel demand) |
| 201 | Rovaniemi | 5.38 | - | - | - | - | - | 20 | predicted (travel demand) |
| 202 | Lagos | 3.43 | 34,452 | - | - | - | - | 100 | predicted (travel demand) |
| 203 | Santa Fe | 5.17 | - | - | - | - | - | 20 | predicted (travel demand) |
| 204 | Lund | 5.14 | - | - | - | - | - | 20 | predicted (travel demand) |
| 205 | Perugia | 2.72 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 206 | Kobe | 3.40 | 54,798 | - | - | - | - | 60 | predicted (travel demand) |
| 207 | Liverpool | 5.09 | 248,189 | 2 | 1 | - | - | 30 | measured |
| 208 | Bologna | 2.72 | 146,161 | 12 | 7 | 1 | 9 | 30 | measured |
| 209 | Cordoba | 3.23 | 74,675 | 16 | 2 | 2 | 3 | 30 | measured |
| 210 | Heraklion | 4.96 | 66,359 | - | - | - | - | 20 | predicted (travel demand) |
| 211 | Marseille | 4.96 | 182,033 | - | - | - | - | 30 | predicted (travel demand) |
| 212 | Christchurch | 4.83 | 104,874 | - | - | - | - | 30 | predicted (travel demand) |
| 213 | Bergamo | 2.38 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 214 | Zwolle | 2.38 | - | 16 | - | 2 | 56 | 20 | measured |
| 215 | Bangkok | 4.75 | 222,206 | 5 | 1 | 1 | - | 100 | measured |
| 216 | Okinawa | 3.06 | 24,466 | 6 | - | - | 1 | 30 | measured |
| 217 | Basel | 4.59 | 105,838 | - | - | - | - | 20 | predicted (travel demand) |
| 218 | Como | 2.21 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 219 | Den Bosch | 2.21 | 39,682 | 12 | 2 | 1 | 118 | 20 | measured |
| 220 | Hilversum | 2.21 | - | 6 | 1 | 1 | 122 | 20 | measured |
| 221 | Tasmania | 4.41 | - | - | - | - | - | 30 | predicted (travel demand) |
| 222 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 20 | predicted (travel demand) |
| 223 | San Sebastian | 2.80 | 367 | - | - | - | - | 20 | predicted (travel demand) |
| 224 | Indianapolis | 4.08 | - | 1 | - | - | - | 30 | measured |
| 225 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 30 | predicted (travel demand) |
| 226 | Alkmaar | 2.04 | - | 14 | - | 2 | 79 | 20 | measured |
| 227 | Split | 4.08 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 228 | Turin | 2.04 | 147,456 | 11 | 7 | 2 | 30 | 30 | measured |
| 229 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 230 | Azores | 2.62 | - | - | - | - | - | 20 | predicted (travel demand) |
| 231 | Pisa | 2.55 | 52,174 | 4 | - | - | - | 20 | measured |
| 232 | Ferrara | 2.21 | 27,490 | 5 | 3 | 1 | 7 | 20 | measured |
| 233 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 234 | Niagara Falls | 3.68 | - | - | - | - | - | 20 | predicted (travel demand) |
| 235 | Dresden | 2.55 | 113,624 | 5 | 5 | 1 | - | 30 | measured |
| 236 | Heidelberg | 3.40 | 75,837 | 6 | 1 | 1 | - | 20 | measured |
| 237 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 100 | predicted (travel demand) |
| 238 | Cologne | 3.74 | 191,812 | 5 | - | 1 | - | 60 | measured |
| 239 | San Diego | 3.74 | 214,939 | 4 | 1 | 1 | - | 60 | measured |
| 240 | Matera | 2.21 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 241 | Wellington | 3.60 | 132,267 | - | - | - | - | 20 | predicted (travel demand) |
| 242 | Cardiff | 3.57 | - | 4 | - | 1 | - | 30 | measured |
| 243 | Salamanca | 2.38 | 47,897 | 4 | - | 1 | 1 | 20 | measured |
| 244 | Bilbao | 2.38 | 133,133 | 4 | - | 1 | - | 30 | measured |
| 245 | Nantes | 3.57 | 67,689 | 1 | 1 | - | - | 30 | measured |
| 246 | Kauai | 3.06 | - | 6 | 1 | - | 8 | 20 | measured |
| 247 | Montpellier | 3.47 | 64,238 | - | - | - | - | 30 | predicted (travel demand) |
| 248 | Oxford | 3.40 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 249 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 250 | Cape Town | 3.29 | 199,169 | - | - | - | - | 60 | predicted (travel demand) |
| 251 | Rhodes | 3.42 | 127,205 | - | - | - | - | 20 | predicted (travel demand) |
| 252 | Heerlen | 1.70 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 253 | Tulsa | 3.40 | - | 1 | - | - | - | 30 | measured |
| 254 | San Antonio | 3.32 | - | 4 | 1 | - | - | 60 | published, never ranked (may be uncrawled) |
| 255 | Chania | 3.30 | 47,379 | - | - | - | - | 20 | predicted (travel demand) |
| 256 | Santiago | 3.25 | 111,647 | - | - | - | - | 100 | predicted (travel demand) |
| 257 | York | 3.23 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 258 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 30 | predicted (travel demand) |
| 259 | Hilo | 2.38 | - | 6 | - | 1 | 16 | 10 | measured |
| 260 | Stuttgart | 2.38 | 112,789 | 6 | 1 | - | - | 30 | measured |
| 261 | Fort Lauderdale | 3.06 | - | 4 | - | - | - | 20 | measured |
| 262 | Lucerne | 3.10 | 66,356 | - | - | - | - | 20 | predicted (travel demand) |
| 263 | Malmo | 3.07 | 103,940 | - | - | - | - | 30 | predicted (travel demand) |
| 264 | Lille | 3.06 | 73,435 | - | - | - | - | 20 | predicted (travel demand) |
| 265 | Toulouse | 2.04 | 112,721 | 10 | - | 1 | 34 | 30 | measured |
| 266 | Corsica | 3.00 | - | - | - | - | - | 30 | predicted (travel demand) |
| 267 | Mechelen | 2.93 | 20,707 | - | - | - | - | 20 | predicted (travel demand) |
| 268 | Regensburg | 2.72 | 51,930 | 5 | 1 | 1 | 4 | 20 | measured |
| 269 | Manchester | 2.89 | 316,438 | 5 | - | - | - | 30 | measured |
| 270 | Gdansk | 1.87 | 4,908 | 12 | 4 | 1 | 307 | 30 | measured |
| 271 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 272 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 273 | Delft | 1.36 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 274 | Deventer | 1.36 | - | 12 | - | 1 | 213 | 20 | measured |
| 275 | Taipei | 2.72 | 143,193 | 4 | 1 | - | - | 60 | measured |
| 276 | Trento | 1.36 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 277 | Corfu | 2.71 | 139,334 | - | - | - | - | 20 | predicted (travel demand) |
| 278 | Mexico City | 2.55 | 566,583 | 9 | 2 | - | - | 100 | measured |
| 279 | Ghent | 2.55 | 82,757 | 8 | 1 | 1 | - | 30 | measured |
| 280 | Belgrade | 2.63 | 178,116 | 5 | 5 | - | - | 60 | measured |
| 281 | Syracuse | 1.75 | 102,833 | - | - | - | - | 20 | predicted (travel demand) |
| 282 | Riga | 2.55 | 108,918 | 5 | 2 | - | - | 30 | measured |
| 283 | Cartagena | 2.58 | 65,066 | - | - | - | - | 30 | predicted (travel demand) |
| 284 | Gran Canaria | 1.67 | - | - | - | - | - | 30 | predicted (travel demand) |
| 285 | Bratislava | 1.70 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 286 | Graz | 1.70 | 65,717 | 12 | 7 | 1 | 87 | 30 | measured |
| 287 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 20 | predicted (travel demand) |
| 288 | Bern | 2.51 | 90,627 | - | - | - | - | 20 | predicted (travel demand) |
| 289 | Freiburg | 2.38 | 92,752 | 7 | 2 | 1 | - | 20 | measured |
| 290 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 291 | Faro | 1.62 | 55,645 | - | - | - | - | 20 | predicted (travel demand) |
| 292 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 293 | Assen | 1.19 | - | 10 | - | 2 | 66 | 20 | measured |
| 294 | Roosendaal | 1.19 | - | 8 | - | 1 | 116 | 20 | measured |
| 295 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 296 | Cusco | 2.35 | 87,732 | - | - | - | - | 30 | predicted (travel demand) |
| 297 | Limerick | 1.57 | 90,379 | - | - | - | - | 20 | predicted (travel demand) |
| 298 | Hamburg | 2.21 | 191,221 | 6 | 1 | 1 | - | 60 | measured |
| 299 | Nagoya | 1.53 | 83,437 | 6 | 1 | - | 1 | 60 | measured |
| 300 | Nuremberg | 1.53 | 161,614 | 12 | 1 | 1 | 38 | 30 | measured |
| 301 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 20 | predicted (travel demand) |
| 302 | Hallstatt | 1.87 | 47,271 | 5 | 1 | - | - | 10 | measured |
| 303 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 304 | Belfast | 2.04 | 224,315 | 4 | - | 1 | - | 30 | measured |
| 305 | Frankfurt | 1.36 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 306 | Kansas City | 2.04 | - | 4 | - | 1 | - | 30 | measured |
| 307 | Lausanne | 2.04 | 68,242 | 8 | 1 | 1 | - | 20 | measured |
| 308 | Lucca | 1.02 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 309 | Rotterdam | 1.02 | 104,938 | 12 | - | 2 | 83 | 30 | measured |
| 310 | Thessaloniki | 2.04 | 180,145 | 4 | - | 1 | - | 30 | measured |
| 311 | Trieste | 1.02 | 117,233 | 36 | 1 | 3 | 43 | 20 | measured |
| 312 | Ischia | 1.32 | - | - | - | - | 2 | 20 | predicted (travel demand) |
| 313 | Ronda | 1.19 | 51,510 | 6 | 1 | - | 9 | 10 | measured |
| 314 | Tarragona | 1.19 | 32,396 | 4 | 2 | - | - | 20 | measured |
| 315 | Izmir | 1.88 | 69,826 | - | - | - | - | 60 | predicted (travel demand) |
| 316 | Rio de Janeiro | 1.95 | 279,431 | 6 | - | - | - | 100 | measured |
| 317 | Braga | 1.02 | 34,522 | 4 | 2 | - | 8 | 20 | measured |
| 318 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 319 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 320 | Maui | 1.70 | - | 4 | - | - | 3 | 20 | measured |
| 321 | Hiroshima | 1.19 | 129,791 | 33 | 5 | 2 | - | 60 | measured |
| 322 | Dijon | 1.72 | 43,526 | - | - | - | - | 20 | predicted (travel demand) |
| 323 | Trier | 1.56 | 69,369 | - | - | - | - | 20 | predicted (travel demand) |
| 324 | Breda | 0.85 | 36,579 | 10 | - | 2 | 118 | 20 | measured |
| 325 | Annecy | 1.69 | 56,859 | - | - | - | - | 20 | predicted (travel demand) |
| 326 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 327 | Canterbury | 1.59 | 53,301 | - | - | - | - | 20 | predicted (travel demand) |
| 328 | Mostar | 1.58 | 63,907 | - | - | - | - | 20 | predicted (travel demand) |
| 329 | Setubal | 0.85 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 330 | Brighton | 1.53 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 331 | Zadar | 1.53 | 71,549 | - | - | - | - | 20 | predicted (travel demand) |
| 332 | Buenos Aires | 1.44 | 333,331 | 4 | 2 | - | - | 60 | measured |
| 333 | Modena | 0.85 | 51,698 | 5 | 1 | 1 | 3 | 20 | measured |
| 334 | Aarhus | 1.36 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 335 | Baltimore | 1.36 | - | 4 | - | - | - | 30 | measured |
| 336 | Apeldoorn | 0.68 | - | 10 | - | 2 | 80 | 20 | measured |
| 337 | Kamakura | 0.85 | 33,492 | 6 | - | - | - | 20 | measured |
| 338 | Antalya | 1.31 | 70,688 | - | - | - | - | 60 | predicted (travel demand) |
| 339 | Colmar | 1.28 | 45,517 | - | - | - | - | 20 | predicted (travel demand) |
| 340 | Cesky Krumlov | 0.85 | 28,582 | 6 | 3 | - | 11 | 10 | measured |
| 341 | Wroclaw | 0.85 | 123,894 | 5 | 1 | 1 | 121 | 30 | measured |
| 342 | Bodrum | 1.26 | 33,918 | - | - | - | - | 20 | predicted (travel demand) |
| 343 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 344 | Rothenburg ob der Tauber | 1.02 | 39,879 | 4 | - | 1 | 8 | 10 | measured |
| 345 | Busan | 1.19 | 94,737 | 2 | - | - | - | 60 | measured |
| 346 | Evora | 0.78 | 15,345 | - | - | - | - | 20 | predicted (travel demand) |
| 347 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 348 | La Palma | 0.70 | - | - | - | - | - | 20 | predicted (travel demand) |
| 349 | Auckland | 1.02 | 152,056 | 5 | 2 | - | - | 60 | measured |
| 350 | Canberra | 1.02 | - | 1 | 1 | - | - | 30 | measured |
| 351 | Sofia | 0.68 | 138,710 | 4 | - | - | - | 60 | measured |
| 352 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 60 | predicted (travel demand) |
| 353 | Bruges | 0.85 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 354 | Turku | 0.85 | - | 1 | - | - | - | 20 | measured |
| 355 | Brno | 0.51 | 63,714 | 8 | 5 | 2 | 34 | 30 | measured |
| 356 | Rouen | 0.68 | 72,334 | 12 | - | 1 | 6 | 20 | measured |
| 357 | Venlo | 0.34 | - | 7 | - | 1 | 144 | 20 | measured |
| 358 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 100 | published, never ranked (may be uncrawled) |
| 359 | Assisi | 0.34 | 30,278 | 6 | 1 | 2 | 6 | 10 | measured |
| 360 | Phoenix | 0.55 | - | - | - | - | - | 60 | predicted (travel demand) |
| 361 | Zaragoza | 0.34 | 87,580 | 7 | - | 1 | - | 30 | measured |
| 362 | Gothenburg | 0.51 | 119,991 | 5 | - | 1 | - | 30 | measured |
| 363 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 364 | Toledo | 0.24 | 3,149 | - | - | - | - | 20 | predicted (travel demand) |
| 365 | Bucharest | 0.34 | 136,836 | 4 | - | 1 | - | 60 | measured |
| 366 | Fort Worth | 0.34 | - | 4 | - | - | - | 30 | measured |
| 367 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 368 | George Town | 0.28 | 36,080 | - | - | - | - | 30 | predicted (travel demand) |
| 369 | Poznan | 0.17 | 65,666 | 10 | - | 1 | 397 | 30 | measured |
| 370 | Allentown | 0.24 | - | - | - | - | - | 20 | predicted (travel demand) |
| 371 | Oss | 0.11 | - | 6 | - | - | 48 | 20 | published, never ranked (may be uncrawled) |
| 372 | Bamberg | 0.17 | 28,716 | 5 | 4 | 1 | 10 | 20 | measured |
| 373 | Antwerp | 0.17 | 128,289 | 10 | 4 | 1 | - | 30 | measured |
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

