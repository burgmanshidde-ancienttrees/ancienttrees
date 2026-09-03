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
| 1 | Rome | 184.58 | 358,876 | 30 | 9 | 2 | 32 | 30 | measured |
| 2 | Amsterdam | 115.17 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 3 | Lisbon | 78.32 | 201,877 | 33 | 10 | 3 | 66 | 30 | measured |
| 4 | Barcelona | 70.02 | 346,477 | 56 | 12 | 7 | 180 | 30 | measured |
| 5 | Singapore | 62.65 | 967,821 | 28 | 3 | 3 | 165 | 30 | measured |
| 6 | Milan | 46.68 | 212,705 | 22 | 9 | 2 | 25 | 30 | measured |
| 7 | Seville | 57.43 | 170,545 | 43 | 6 | 2 | - | 20 | measured |
| 8 | Florence | 42.08 | 184,099 | 23 | 8 | 1 | 27 | 30 | measured |
| 9 | Brisbane | 52.82 | 162,602 | 19 | 1 | 2 | 189 | 30 | measured |
| 10 | Vienna | 44.84 | 283,090 | 32 | 13 | 5 | 376 | 30 | measured |
| 11 | London | 56.20 | 718,291 | 23 | 10 | 1 | - | 30 | measured |
| 12 | Tenerife | 43.00 | - | 4 | 1 | - | - | 20 | measured |
| 13 | Naples | 32.55 | 198,913 | 24 | 3 | 3 | 46 | 20 | measured |
| 14 | Prague | 42.69 | 303,350 | 18 | 13 | 3 | 30 | 30 | measured |
| 15 | Malaga | 40.23 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 16 | New York | 52.21 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 17 | Madeira | 33.17 | - | 10 | 1 | 1 | - | 20 | measured |
| 18 | Hilo | 40.54 | - | 6 | - | 1 | 16 | 20 | measured |
| 19 | Paris | 35.63 | 524,268 | 31 | 9 | 4 | 129 | 30 | measured |
| 20 | Portland | 35.01 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 21 | Alicante | 24.26 | 77,454 | 14 | 3 | 2 | 44 | 20 | measured |
| 22 | Sardinia | 26.72 | - | 5 | 2 | - | 8 | 20 | measured |
| 23 | Fukuoka | 29.79 | 77,485 | 15 | 7 | 1 | - | 20 | measured |
| 24 | Palermo | 22.73 | 124,310 | 21 | 7 | 1 | 37 | 20 | measured |
| 25 | Copenhagen | 42.08 | 218,621 | 16 | 1 | 2 | - | 30 | measured |
| 26 | Palma de Mallorca | 25.80 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 27 | Venice | 23.34 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 28 | Dublin | 24.26 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 29 | Leiden | 20.27 | 33,227 | 12 | 4 | 1 | 129 | 20 | measured |
| 30 | Brussels | 26.72 | 176,863 | 30 | 4 | 1 | 436 | 30 | measured |
| 31 | Valencia | 19.66 | 162,209 | 24 | 2 | 2 | 350 | 30 | measured |
| 32 | Nijmegen | 19.04 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 33 | Birmingham | 37.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 34 | Bologna | 19.96 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 35 | Las Vegas | 36.24 | - | 11 | - | 2 | - | 30 | measured |
| 36 | Crete | 34.70 | - | 4 | 2 | - | - | 20 | measured |
| 37 | Seattle | 32.55 | 398,724 | 6 | - | - | - | 30 | measured |
| 38 | Kyoto | 21.19 | 142,353 | 17 | 8 | 2 | - | 20 | measured |
| 39 | Madrid | 20.27 | 274,553 | 17 | 10 | 2 | - | 20 | measured |
| 40 | Toronto | 28.87 | 411,011 | 6 | - | - | - | 30 | measured |
| 41 | Krakow | 18.73 | 140,824 | 34 | 3 | 3 | 198 | 30 | measured |
| 42 | Bath | 27.95 | 144,950 | 5 | 1 | 1 | - | 20 | measured |
| 43 | Chicago | 27.64 | 485,769 | 6 | - | - | - | 30 | measured |
| 44 | Munich | 18.12 | 224,067 | 45 | 14 | 6 | 80 | 30 | measured |
| 45 | Berlin | 17.81 | 412,181 | 19 | 11 | 1 | 195 | 30 | measured |
| 46 | Sintra | 13.21 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 47 | Oahu | 17.20 | - | 11 | 1 | - | 160 | 20 | measured |
| 48 | Utrecht | 12.59 | 67,963 | 33 | 4 | 2 | 345 | 20 | measured |
| 49 | Cagliari | 13.21 | 51,351 | 10 | 1 | 2 | 15 | 20 | measured |
| 50 | Seoul | 22.73 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 51 | Athens | 22.73 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 52 | Boston | 22.11 | 385,902 | 11 | 1 | 1 | - | 30 | measured |
| 53 | Jacksonville | 22.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 54 | Tokyo | 11.98 | 394,702 | 16 | 8 | 1 | 6 | 20 | measured |
| 55 | Edinburgh | 21.81 | 292,981 | 16 | 4 | 1 | - | 30 | measured |
| 56 | The Hague | 10.75 | 236,723 | 29 | 1 | 5 | 166 | 20 | measured |
| 57 | Asheville | 20.89 | - | - | - | - | - | 10 | predicted (travel demand) |
| 58 | Groningen | 10.44 | 31,401 | 20 | - | 2 | 72 | 20 | measured |
| 59 | Boise | 20.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 60 | Long Beach | 20.48 | - | - | - | - | - | 10 | predicted (travel demand) |
| 61 | Little Rock | 20.40 | - | - | - | - | - | 10 | predicted (travel demand) |
| 62 | Perth | 19.35 | 180,478 | 6 | 1 | 1 | - | 30 | measured |
| 63 | New Orleans | 19.66 | 256,232 | 4 | 2 | 1 | - | 20 | measured |
| 64 | Indianapolis | 18.28 | - | - | - | - | - | 10 | predicted (travel demand) |
| 65 | Vilnius | 12.59 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 66 | Oakland | 18.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 67 | Fort Lauderdale | 18.43 | - | - | - | - | - | 10 | predicted (travel demand) |
| 68 | Lexington | 18.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 69 | Reno | 18.19 | - | - | - | - | - | 10 | predicted (travel demand) |
| 70 | Des Moines | 18.11 | - | - | - | - | - | 10 | predicted (travel demand) |
| 71 | Bordeaux | 11.98 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 72 | Melbourne | 11.98 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 73 | Sydney | 17.51 | 305,304 | 6 | - | - | - | 30 | measured |
| 74 | Porto | 8.91 | 120,415 | 27 | 14 | 2 | 40 | 20 | measured |
| 75 | Sorrento | 8.91 | 40,049 | 6 | - | 1 | 20 | 20 | measured |
| 76 | Daytona Beach | 17.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 77 | Reykjavik | 14.74 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 78 | Chattanooga | 16.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 79 | Austin | 16.58 | 226,631 | 5 | - | - | - | 20 | measured |
| 80 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 81 | Eindhoven | 7.99 | - | 7 | - | 1 | 195 | 20 | measured |
| 82 | Cyprus | 15.66 | - | 4 | - | - | - | 20 | measured |
| 83 | Spokane | 15.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 84 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 85 | Pittsburgh | 15.18 | - | - | - | - | - | 10 | predicted (travel demand) |
| 86 | Arnhem | 7.68 | 31,478 | 9 | 1 | 1 | 196 | 20 | measured |
| 87 | Huntsville | 15.35 | - | - | - | - | - | 10 | predicted (travel demand) |
| 88 | Geneva | 10.13 | 162,269 | 21 | 4 | 4 | 131 | 20 | measured |
| 89 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 90 | West Palm Beach | 14.98 | - | - | - | - | - | 10 | predicted (travel demand) |
| 91 | Monterey | 14.58 | - | - | - | - | - | 10 | predicted (travel demand) |
| 92 | Cadiz | 9.52 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 93 | Saint Petersburg | 14.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 94 | St. Louis | 14.80 | - | - | - | - | - | 10 | predicted (travel demand) |
| 95 | Montreal | 14.43 | 315,322 | 7 | - | 1 | - | 30 | measured |
| 96 | Budapest | 13.82 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 97 | Strasbourg | 9.52 | 154,700 | 10 | 1 | 2 | 66 | 30 | measured |
| 98 | Tampa | 14.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 99 | Quebec City | 9.21 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 100 | Cincinnati | 13.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 101 | Lansing | 13.02 | - | - | - | - | - | 10 | predicted (travel demand) |
| 102 | Trieste | 6.45 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 103 | Washington DC | 11.67 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 104 | Detroit | 12.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 105 | Tulsa | 12.03 | - | - | - | - | - | 10 | predicted (travel demand) |
| 106 | Dallas | 11.67 | - | 8 | 1 | 1 | - | 30 | measured |
| 107 | Denver | 11.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 108 | Warsaw | 7.68 | 197,929 | 19 | 3 | 2 | 1446 | 30 | measured |
| 109 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 110 | San Jose | 11.39 | - | - | - | - | - | 10 | predicted (travel demand) |
| 111 | Sacramento | 11.32 | - | - | - | - | - | 10 | predicted (travel demand) |
| 112 | Jersey City | 10.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 113 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 114 | Maastricht | 5.53 | 47,763 | 14 | - | 1 | 137 | 20 | measured |
| 115 | Lyon | 7.37 | 136,951 | 13 | 3 | 1 | 156 | 20 | measured |
| 116 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 117 | Milwaukee | 10.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 118 | Houston | 10.44 | - | 4 | - | - | - | 30 | measured |
| 119 | Glasgow | 9.83 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 120 | Istanbul | 9.06 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 121 | Salt Lake City | 10.31 | - | - | - | - | - | 10 | predicted (travel demand) |
| 122 | Atlanta | 10.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 123 | Anchorage | 10.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 124 | Raleigh | 10.07 | - | - | - | - | - | 10 | predicted (travel demand) |
| 125 | Bristol | 9.83 | 163,983 | 5 | 1 | - | - | 20 | measured |
| 126 | Guimaraes | 5.22 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 127 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 128 | Oslo | 8.60 | 181,113 | 4 | - | - | - | 20 | measured |
| 129 | Cleveland | 9.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 130 | El Paso | 9.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 131 | Potsdam | 6.45 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 132 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 133 | Braga | 5.22 | 34,522 | 4 | 1 | - | 8 | 20 | measured |
| 134 | Miami | 9.48 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 135 | Turku | 9.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 136 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 137 | Helsinki | 7.68 | 148,908 | 8 | 1 | - | 9 | 30 | measured |
| 138 | Nuremberg | 6.14 | 161,614 | 12 | 1 | 1 | 38 | 20 | measured |
| 139 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 140 | Canberra | 9.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 141 | Oxford | 8.91 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 142 | Catania | 5.22 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 143 | Pisa | 5.85 | 52,174 | - | - | - | - | 10 | predicted (travel demand) |
| 144 | Nashville | 8.93 | - | - | - | - | - | 10 | predicted (travel demand) |
| 145 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 146 | Graz | 5.84 | 65,717 | 12 | 3 | 1 | 87 | 20 | measured |
| 147 | Cordoba | 5.53 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 148 | Ann Arbor | 8.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 149 | Mexico City | 7.99 | 566,583 | 9 | 1 | - | - | 30 | measured |
| 150 | Salamanca | 5.50 | 47,897 | - | - | - | 1 | 10 | predicted (travel demand) |
| 151 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 152 | Cork | 5.53 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 153 | Tallinn | 5.53 | 124,888 | 4 | 2 | 1 | 42 | 20 | measured |
| 154 | Pamplona | 5.22 | 128,065 | 6 | - | - | 1 | 20 | measured |
| 155 | Lucca | 3.99 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 156 | Rotterdam | 3.99 | 104,938 | 9 | - | 2 | 83 | 20 | measured |
| 157 | Albuquerque | 7.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 158 | Osaka | 4.91 | 163,112 | 5 | 1 | - | - | 30 | measured |
| 159 | Minneapolis | 7.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 160 | Los Angeles | 7.20 | 665,559 | 8 | 2 | - | - | 10 | published, never ranked (may be uncrawled) |
| 161 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 162 | Turin | 3.69 | 147,456 | 11 | 7 | 2 | 30 | 20 | measured |
| 163 | Venlo | 3.69 | - | 7 | - | 1 | 144 | 20 | measured |
| 164 | Brno | 4.91 | 63,714 | 8 | 2 | 2 | 34 | 20 | measured |
| 165 | Hobart | 4.91 | 81,734 | 10 | - | 2 | 455 | 20 | measured |
| 166 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 167 | Granada | 4.61 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 168 | Baltimore | 7.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 169 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 170 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 171 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 172 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 173 | Dubrovnik | 6.14 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 174 | Bilbao | 4.30 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 175 | Bratislava | 4.30 | 132,162 | 6 | - | 1 | 26 | 30 | measured |
| 176 | Leipzig | 4.30 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 177 | Poznan | 4.30 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 178 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 179 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 180 | Verona | 3.69 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 181 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 182 | Como | 3.07 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 183 | Delft | 3.07 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 184 | Dordrecht | 3.07 | - | 7 | - | 1 | 103 | 20 | measured |
| 185 | Tilburg | 3.07 | - | 7 | - | 1 | 84 | 20 | measured |
| 186 | Sapporo | 3.99 | 88,633 | 6 | - | - | - | 20 | measured |
| 187 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 188 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 189 | Kauai | 4.91 | - | 6 | - | - | 8 | 20 | measured |
| 190 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 191 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 192 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 193 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 194 | Aarhus | 5.22 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 195 | Ljubljana | 5.22 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 196 | Hong Kong | 3.53 | 689,212 | 10 | 2 | 1 | 505 | 20 | measured |
| 197 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 198 | Kansas City | 5.26 | - | 4 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 199 | Cardiff | 5.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 200 | Santa Fe | 5.17 | - | - | - | - | - | 10 | predicted (travel demand) |
| 201 | Bari | 3.07 | 86,456 | 4 | 1 | - | 8 | 30 | measured |
| 202 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 203 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 204 | Lausanne | 4.90 | 68,242 | - | - | - | - | 10 | predicted (travel demand) |
| 205 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 206 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 207 | Alkmaar | 2.46 | - | 7 | - | 1 | 79 | 20 | measured |
| 208 | Amersfoort | 2.46 | - | 8 | 1 | 1 | 181 | 20 | measured |
| 209 | Den Bosch | 2.46 | 39,682 | 11 | 1 | 1 | 119 | 20 | measured |
| 210 | Helmond | 2.46 | - | 7 | - | 1 | 55 | 20 | measured |
| 211 | Leeuwarden | 2.46 | - | 7 | - | 1 | 61 | 20 | measured |
| 212 | Trento | 2.46 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 213 | Kamakura | 3.07 | 33,492 | 6 | - | - | - | 20 | measured |
| 214 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 215 | Girona | 2.76 | 51,072 | 7 | - | - | - | 20 | measured |
| 216 | Genoa | 2.46 | 145,206 | 12 | 1 | 1 | 11 | 20 | measured |
| 217 | Perugia | 2.46 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 218 | Frankfurt | 3.07 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 219 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 220 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 221 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 222 | Apeldoorn | 2.15 | - | 8 | - | 1 | 80 | 20 | measured |
| 223 | Bergamo | 2.15 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 224 | Cambridge | 4.30 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 225 | Caserta | 2.15 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 226 | Heerlen | 2.15 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 227 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 228 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 229 | Riga | 3.99 | 108,918 | 5 | - | - | - | 20 | measured |
| 230 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 231 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 232 | Nantes | 3.83 | 67,689 | - | - | - | - | 10 | predicted (travel demand) |
| 233 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 234 | Zurich | 3.69 | 140,788 | 4 | - | - | - | 20 | measured |
| 235 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 236 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 237 | San Francisco | 3.69 | 361,111 | 6 | - | 1 | - | 30 | measured |
| 238 | Nice | 3.69 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 239 | Toulouse | 2.46 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 240 | Assen | 1.84 | - | 9 | - | 2 | 67 | 20 | measured |
| 241 | Haarlem | 1.84 | 33,960 | 21 | - | 2 | 277 | 20 | measured |
| 242 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 243 | Stockholm | 2.76 | 188,184 | 4 | 3 | - | - | 30 | measured |
| 244 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 245 | Padua | 1.84 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 246 | Vancouver | 3.38 | 351,552 | 4 | - | - | - | 30 | measured |
| 247 | Busan | 3.31 | 94,737 | - | - | - | - | 10 | predicted (travel demand) |
| 248 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 249 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 250 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 251 | Cologne | 3.38 | 191,812 | 5 | - | 1 | - | 30 | measured |
| 252 | San Antonio | 3.32 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 253 | Parma | 1.84 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 254 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 255 | Fort Worth | 3.28 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 256 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 257 | Luxembourg City | 2.15 | 64,851 | 10 | - | 2 | 18 | 20 | measured |
| 258 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 259 | Sao Paulo | 2.96 | 911 | - | - | - | - | 10 | predicted (travel demand) |
| 260 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 261 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 262 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 263 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 264 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 265 | Coimbra | 1.54 | 34,962 | 4 | - | - | 5 | 20 | measured |
| 266 | Menorca | 1.84 | - | 6 | - | - | 2 | 20 | measured |
| 267 | Ibiza | 1.85 | - | - | - | - | - | 10 | predicted (travel demand) |
| 268 | Gdansk | 1.84 | 4,908 | 6 | 4 | - | 288 | 20 | measured |
| 269 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 270 | Salzburg | 1.84 | 107,243 | 5 | - | - | 34 | 20 | measured |
| 271 | Sofia | 1.84 | 138,710 | 4 | - | - | - | 30 | measured |
| 272 | York | 2.76 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 273 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 274 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 275 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 276 | Bangkok | 2.61 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 277 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 278 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 279 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 280 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 281 | Hilversum | 1.23 | - | 6 | - | 1 | 122 | 20 | measured |
| 282 | Savannah | 2.46 | 128,162 | 2 | - | - | - | 20 | measured |
| 283 | Zwolle | 1.23 | - | 7 | - | 1 | 57 | 20 | measured |
| 284 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 285 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 286 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 287 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 288 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 289 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 290 | Cesky Krumlov | 1.54 | 28,582 | 6 | 2 | - | 11 | 20 | measured |
| 291 | Hallstatt | 1.99 | 47,271 | - | - | - | - | 10 | predicted (travel demand) |
| 292 | Wroclaw | 1.54 | 123,894 | 5 | 1 | 1 | 121 | 20 | measured |
| 293 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 294 | Taipei | 2.09 | 143,193 | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 295 | Tarragona | 1.23 | 32,396 | 4 | - | - | - | 20 | measured |
| 296 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 297 | Modena | 1.23 | 51,698 | 5 | - | 1 | 3 | 20 | measured |
| 298 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 299 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 300 | Maui | 1.84 | - | 4 | - | - | 3 | 20 | measured |
| 301 | Philadelphia | 1.84 | 405,294 | 1 | - | - | - | 20 | measured |
| 302 | Belgrade | 1.84 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 303 | Deventer | 0.92 | - | 7 | - | 1 | 213 | 20 | measured |
| 304 | Enschede | 0.92 | - | 7 | 1 | 1 | 82 | 20 | measured |
| 305 | Hoorn | 0.92 | - | 8 | - | 1 | 52 | 20 | measured |
| 306 | Ottawa | 1.23 | - | 8 | - | 1 | 119 | 20 | measured |
| 307 | Split | 1.84 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 308 | Thessaloniki | 1.84 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 309 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 310 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 311 | Buenos Aires | 1.69 | 333,331 | 4 | 1 | - | - | 30 | measured |
| 312 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 313 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 314 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 315 | Matera | 1.00 | 67,033 | 4 | - | - | 2 | 10 | predicted (travel demand) |
| 316 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 317 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 318 | Freiburg | 1.54 | 92,752 | 7 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 319 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 320 | Ronda | 0.92 | 51,510 | 6 | - | - | 9 | 20 | measured |
| 321 | Belfast | 1.54 | 224,315 | 4 | - | 1 | - | 20 | measured |
| 322 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 323 | Assisi | 0.92 | 30,278 | 6 | 1 | 2 | 6 | 20 | measured |
| 324 | Rothenburg ob der Tauber | 1.23 | 39,879 | 4 | - | 1 | 8 | 20 | measured |
| 325 | Segovia | 0.92 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 326 | Nagoya | 0.92 | 83,437 | 6 | - | - | 1 | 20 | measured |
| 327 | Naha | 0.92 | 24,466 | 6 | - | - | 1 | 20 | measured |
| 328 | Hawaii | 1.23 | - | 6 | - | 1 | 6 | 30 | measured |
| 329 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 330 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 331 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 332 | Charleston | 1.23 | 155,987 | 2 | 1 | - | - | 20 | measured |
| 333 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 334 | Antwerp | 1.23 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 335 | Bucharest | 1.23 | 136,836 | 4 | - | 1 | - | 20 | measured |
| 336 | Roosendaal | 0.61 | - | 8 | - | 1 | 116 | 20 | measured |
| 337 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 338 | Stuttgart | 1.02 | 112,789 | 7 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 339 | Setubal | 0.61 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 340 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 341 | Zaragoza | 0.73 | 87,580 | 7 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 342 | Ferrara | 0.61 | 27,490 | 5 | 1 | 1 | 7 | 20 | measured |
| 343 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 344 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 345 | Auckland | 0.92 | 152,056 | 5 | - | - | - | 20 | measured |
| 346 | Dresden | 0.61 | 113,624 | 5 | 1 | 1 | - | 20 | measured |
| 347 | Hiroshima | 0.61 | 129,791 | 8 | 1 | 2 | - | 20 | measured |
| 348 | Liverpool | 0.92 | 248,189 | 2 | - | - | - | 20 | measured |
| 349 | Brighton | 0.85 | 114,108 | 6 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 350 | Heidelberg | 0.67 | 75,837 | 6 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 351 | Ghent | 0.59 | 82,757 | 6 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 352 | Breda | 0.31 | 36,579 | 4 | - | 1 | 119 | 20 | measured |
| 353 | Gothenburg | 0.61 | 119,991 | 5 | - | 1 | - | 20 | measured |
| 354 | Leuven | 0.61 | 40,645 | 4 | - | - | - | 20 | measured |
| 355 | Manchester | 0.61 | 316,438 | 5 | - | - | - | 30 | measured |
| 356 | San Diego | 0.61 | 214,939 | 4 | - | 1 | - | 20 | measured |
| 357 | Lima | 0.51 | 132,792 | 5 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 358 | Rouen | 0.54 | 72,334 | 12 | - | 1 | 6 | 10 | published, never ranked (may be uncrawled) |
| 359 | Phoenix | 0.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 360 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 361 | Yakushima | 0.31 | - | 1 | - | - | 1 | 20 | measured |
| 362 | Kanazawa | 0.31 | 25,778 | 7 | - | 1 | 2 | 20 | measured |
| 363 | Bamberg | 0.31 | 28,716 | 5 | 3 | 1 | 10 | 20 | measured |
| 364 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 365 | Regensburg | 0.31 | 51,930 | 5 | - | 1 | 4 | 20 | measured |
| 366 | Hamburg | 0.31 | 191,221 | 6 | - | 1 | - | 30 | measured |
| 367 | Beijing | 0.31 | 269,737 | 6 | - | - | - | 30 | measured |
| 368 | Bruges | 0.31 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 369 | Rio de Janeiro | 0.31 | 279,431 | 6 | - | - | - | 30 | measured |
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

