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
| 1 | Rome | 116.87 | 358,876 | 30 | 9 | 2 | 32 | 30 | measured |
| 2 | Amsterdam | 101.60 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 3 | Lisbon | 59.56 | 201,877 | 33 | 10 | 3 | 66 | 30 | measured |
| 4 | Barcelona | 46.30 | 346,477 | 56 | 12 | 7 | 180 | 30 | measured |
| 5 | Milan | 40.04 | 212,705 | 22 | 9 | 2 | 25 | 30 | measured |
| 6 | Tenerife | 48.80 | - | 4 | - | - | - | 20 | measured |
| 7 | Brisbane | 46.80 | 162,602 | 19 | 1 | 2 | 189 | 30 | measured |
| 8 | Seville | 45.30 | 170,545 | 43 | 6 | 2 | - | 20 | measured |
| 9 | Singapore | 45.55 | 967,821 | 28 | 3 | 3 | 165 | 30 | measured |
| 10 | Florence | 30.03 | 184,099 | 23 | 8 | 1 | 27 | 30 | measured |
| 11 | Naples | 29.03 | 198,913 | 24 | 3 | 3 | 46 | 20 | measured |
| 12 | Malaga | 38.04 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 13 | Vienna | 36.04 | 283,090 | 32 | 13 | 5 | 376 | 30 | measured |
| 14 | Prague | 35.29 | 303,350 | 17 | 13 | 3 | 29 | 30 | measured |
| 15 | New York | 43.54 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 16 | London | 41.04 | 718,291 | 23 | 10 | 1 | - | 30 | measured |
| 17 | Copenhagen | 43.80 | 218,621 | 16 | 1 | 2 | - | 30 | measured |
| 18 | Madeira | 26.28 | - | 6 | 1 | - | - | 20 | measured |
| 19 | Paris | 30.28 | 524,268 | 31 | 9 | 4 | 129 | 30 | measured |
| 20 | Palermo | 22.27 | 124,310 | 21 | 7 | 1 | 37 | 20 | measured |
| 21 | Venice | 22.27 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 22 | Portland | 26.03 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 23 | Las Vegas | 39.04 | - | 11 | - | 2 | - | 30 | measured |
| 24 | Palma de Mallorca | 23.02 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 25 | Birmingham | 37.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 26 | Hilo | 28.03 | - | 5 | - | 1 | 16 | 20 | measured |
| 27 | Madrid | 22.02 | 274,553 | 17 | 10 | 2 | - | 20 | measured |
| 28 | Alicante | 17.77 | 77,454 | 14 | 2 | 2 | 44 | 20 | measured |
| 29 | Brussels | 23.52 | 176,863 | 30 | 4 | 1 | 436 | 30 | measured |
| 30 | Fukuoka | 22.77 | 77,485 | 13 | 7 | 1 | - | 20 | measured |
| 31 | Valencia | 17.52 | 162,209 | 24 | 2 | 2 | 350 | 30 | measured |
| 32 | Bologna | 18.77 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 33 | Sardinia | 18.77 | - | 5 | 2 | - | 8 | 20 | measured |
| 34 | Bath | 32.78 | 144,950 | 5 | 1 | 1 | - | 20 | measured |
| 35 | Dublin | 18.52 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 36 | Seattle | 26.53 | 398,724 | 6 | - | - | - | 30 | measured |
| 37 | Crete | 27.53 | - | 4 | - | - | - | 20 | measured |
| 38 | Nijmegen | 13.26 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 39 | Seoul | 24.28 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 40 | Chicago | 25.03 | 485,769 | 6 | - | - | - | 30 | measured |
| 41 | Toronto | 23.77 | 411,011 | 6 | - | - | - | 30 | measured |
| 42 | Kyoto | 15.02 | 142,353 | 17 | 8 | 2 | - | 20 | measured |
| 43 | Leiden | 11.51 | 33,227 | 12 | 4 | 1 | 129 | 20 | measured |
| 44 | Jacksonville | 22.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 45 | Kansas City | 21.02 | - | - | - | - | - | 10 | predicted (travel demand) |
| 46 | Krakow | 14.01 | 140,824 | 34 | 3 | 3 | 198 | 30 | measured |
| 47 | Edinburgh | 20.52 | 292,981 | 15 | 4 | 1 | - | 30 | measured |
| 48 | Asheville | 20.89 | - | - | - | - | - | 10 | predicted (travel demand) |
| 49 | Boise | 20.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 50 | Long Beach | 20.48 | - | - | - | - | - | 10 | predicted (travel demand) |
| 51 | Little Rock | 20.40 | - | - | - | - | - | 10 | predicted (travel demand) |
| 52 | Sintra | 9.51 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 53 | Utrecht | 9.51 | 67,963 | 33 | 4 | 2 | 345 | 20 | measured |
| 54 | Indianapolis | 18.28 | - | - | - | - | - | 10 | predicted (travel demand) |
| 55 | Oakland | 18.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 56 | Fort Lauderdale | 18.43 | - | - | - | - | - | 10 | predicted (travel demand) |
| 57 | Munich | 12.51 | 224,067 | 45 | 14 | 6 | 80 | 30 | measured |
| 58 | Oahu | 12.51 | - | 8 | - | - | 133 | 20 | measured |
| 59 | Lexington | 18.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 60 | Reno | 18.19 | - | - | - | - | - | 10 | predicted (travel demand) |
| 61 | Des Moines | 18.11 | - | - | - | - | - | 10 | predicted (travel demand) |
| 62 | Daytona Beach | 17.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 63 | Berlin | 11.51 | 412,181 | 19 | 11 | 1 | 195 | 30 | measured |
| 64 | Porto | 8.51 | 120,415 | 27 | 5 | 2 | 40 | 20 | measured |
| 65 | Chattanooga | 16.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 66 | Boston | 16.02 | 385,902 | 10 | 1 | 1 | - | 30 | measured |
| 67 | The Hague | 8.26 | 236,723 | 29 | 1 | 5 | 166 | 20 | measured |
| 68 | San Francisco | 16.17 | 361,111 | - | - | - | - | 10 | predicted (travel demand) |
| 69 | Bordeaux | 10.76 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 70 | Vilnius | 10.76 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 71 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 72 | Groningen | 8.01 | 31,401 | 20 | - | 2 | 72 | 20 | measured |
| 73 | New Orleans | 16.02 | 256,232 | 4 | - | 1 | - | 20 | measured |
| 74 | Spokane | 15.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 75 | Cagliari | 8.51 | 51,351 | 10 | 1 | 2 | 15 | 20 | measured |
| 76 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 77 | Tokyo | 8.01 | 394,702 | 10 | 8 | - | 7 | 20 | measured |
| 78 | Pittsburgh | 15.18 | - | - | - | - | - | 10 | predicted (travel demand) |
| 79 | Huntsville | 15.35 | - | - | - | - | - | 10 | predicted (travel demand) |
| 80 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 81 | West Palm Beach | 14.98 | - | - | - | - | - | 10 | predicted (travel demand) |
| 82 | Monterey | 14.58 | - | - | - | - | - | 10 | predicted (travel demand) |
| 83 | Saint Petersburg | 14.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 84 | St. Louis | 14.80 | - | - | - | - | - | 10 | predicted (travel demand) |
| 85 | Montreal | 14.77 | 315,322 | 7 | - | 1 | - | 30 | measured |
| 86 | Sydney | 14.01 | 305,304 | 6 | - | - | - | 30 | measured |
| 87 | Reykjavik | 12.26 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 88 | Tampa | 14.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 89 | Cyprus | 13.51 | - | 4 | - | - | - | 20 | measured |
| 90 | Perth | 13.26 | 180,478 | 6 | 1 | 1 | - | 30 | measured |
| 91 | Cincinnati | 13.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 92 | San Antonio | 13.28 | - | - | - | - | - | 10 | predicted (travel demand) |
| 93 | Athens | 13.01 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 94 | Fort Worth | 13.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 95 | Lansing | 13.02 | - | - | - | - | - | 10 | predicted (travel demand) |
| 96 | Sorrento | 6.51 | 40,049 | 6 | - | 1 | 20 | 20 | measured |
| 97 | Washington DC | 11.51 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 98 | Detroit | 12.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 99 | Tulsa | 12.03 | - | - | - | - | - | 10 | predicted (travel demand) |
| 100 | Cadiz | 7.76 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 101 | Geneva | 8.01 | 162,269 | 21 | 4 | 4 | 131 | 20 | measured |
| 102 | Denver | 11.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 103 | Maastricht | 5.76 | 47,763 | 14 | - | 1 | 137 | 20 | measured |
| 104 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 105 | San Jose | 11.39 | - | - | - | - | - | 10 | predicted (travel demand) |
| 106 | Sacramento | 11.32 | - | - | - | - | - | 10 | predicted (travel demand) |
| 107 | Jersey City | 10.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 108 | Austin | 9.51 | 226,631 | 5 | - | - | - | 20 | measured |
| 109 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 110 | Guimaraes | 5.76 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 111 | San Diego | 11.06 | 214,939 | - | - | - | - | 10 | predicted (travel demand) |
| 112 | Arnhem | 5.51 | 31,478 | 9 | 1 | 1 | 196 | 20 | measured |
| 113 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 114 | Trieste | 5.51 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 115 | Melbourne | 7.26 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 116 | Quebec City | 7.26 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 117 | Hamburg | 10.27 | 191,221 | - | - | - | - | 10 | predicted (travel demand) |
| 118 | Dallas | 9.01 | - | 8 | 1 | 1 | - | 30 | measured |
| 119 | Milwaukee | 10.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 120 | Salt Lake City | 10.31 | - | - | - | - | - | 10 | predicted (travel demand) |
| 121 | Atlanta | 10.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 122 | Anchorage | 10.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 123 | Raleigh | 10.07 | - | - | - | - | - | 10 | predicted (travel demand) |
| 124 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 125 | Cleveland | 9.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 126 | El Paso | 9.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 127 | Budapest | 9.26 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 128 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 129 | Miami | 9.48 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 130 | Turku | 9.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 131 | Strasbourg | 6.26 | 154,700 | 10 | 1 | 2 | 66 | 30 | measured |
| 132 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 133 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 134 | Canberra | 9.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 135 | Manchester | 9.06 | 316,438 | - | - | - | - | 10 | predicted (travel demand) |
| 136 | Pisa | 5.85 | 52,174 | - | - | - | - | 10 | predicted (travel demand) |
| 137 | Nashville | 8.93 | - | - | - | - | - | 10 | predicted (travel demand) |
| 138 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 139 | Potsdam | 5.76 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 140 | Ann Arbor | 8.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 141 | Taipei | 8.38 | 143,193 | - | - | - | - | 10 | predicted (travel demand) |
| 142 | Salamanca | 5.50 | 47,897 | - | - | - | 1 | 10 | predicted (travel demand) |
| 143 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 144 | Lyon | 5.51 | 136,951 | 13 | 3 | 1 | 156 | 20 | measured |
| 145 | Delft | 4.00 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 146 | Helsinki | 6.51 | 148,908 | 8 | 1 | - | 9 | 30 | measured |
| 147 | Houston | 7.01 | - | 4 | - | - | - | 30 | measured |
| 148 | Albuquerque | 7.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 149 | Cordoba | 5.01 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 150 | Minneapolis | 7.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 151 | Istanbul | 6.63 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 152 | Nuremberg | 5.01 | 161,614 | 11 | 1 | 1 | 39 | 20 | measured |
| 153 | Los Angeles | 7.20 | 665,559 | 8 | 2 | - | - | 10 | published, never ranked (may be uncrawled) |
| 154 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 155 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 156 | Mexico City | 6.88 | 566,583 | 9 | 1 | - | - | 30 | measured |
| 157 | Baltimore | 7.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 158 | Glasgow | 6.76 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 159 | Oslo | 6.26 | 181,113 | 4 | - | - | - | 20 | measured |
| 160 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 161 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 162 | Braga | 3.75 | 34,522 | 4 | 1 | - | 8 | 20 | measured |
| 163 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 164 | Bristol | 6.51 | 163,983 | 5 | 1 | - | - | 20 | measured |
| 165 | Liverpool | 6.46 | 248,189 | - | - | - | - | 10 | predicted (travel demand) |
| 166 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 167 | Freiburg | 6.18 | 92,752 | - | - | - | - | 10 | predicted (travel demand) |
| 168 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 169 | Cambridge | 6.51 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 170 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 171 | Cork | 4.25 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 172 | Graz | 4.25 | 65,717 | 12 | 3 | 1 | 87 | 20 | measured |
| 173 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 174 | Rio de Janeiro | 6.36 | 279,431 | - | - | - | - | 10 | predicted (travel demand) |
| 175 | Aarhus | 6.01 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 176 | Bilbao | 4.00 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 177 | Bratislava | 4.00 | 132,162 | 6 | - | 1 | 26 | 30 | measured |
| 178 | Rotterdam | 3.00 | 104,938 | 9 | - | 2 | 83 | 20 | measured |
| 179 | Turin | 3.00 | 147,456 | 11 | 7 | 2 | 30 | 20 | measured |
| 180 | Gothenburg | 5.95 | 119,991 | - | - | - | - | 10 | predicted (travel demand) |
| 181 | Oxford | 5.76 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 182 | Beijing | 5.73 | 269,737 | - | - | - | - | 10 | predicted (travel demand) |
| 183 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 184 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 185 | Warsaw | 3.75 | 197,929 | 18 | 3 | 2 | 1445 | 30 | measured |
| 186 | Bruges | 5.60 | 106,902 | - | - | - | - | 10 | predicted (travel demand) |
| 187 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 188 | Catania | 3.25 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 189 | Verona | 3.25 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 190 | Caserta | 2.75 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 191 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 192 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 193 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 194 | Dubrovnik | 5.01 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 195 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 196 | Cardiff | 5.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 197 | Santa Fe | 5.17 | - | - | - | - | - | 10 | predicted (travel demand) |
| 198 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 199 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 200 | Auckland | 4.67 | 152,056 | - | - | - | - | 10 | predicted (travel demand) |
| 201 | Lausanne | 4.90 | 68,242 | - | - | - | - | 10 | predicted (travel demand) |
| 202 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 203 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 204 | Brno | 3.25 | 63,714 | 8 | 2 | 2 | 34 | 20 | measured |
| 205 | Poznan | 3.25 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 206 | Tallinn | 3.25 | 124,888 | 4 | 2 | 1 | 42 | 20 | measured |
| 207 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 208 | York | 4.75 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 209 | Osaka | 3.00 | 163,112 | 4 | 1 | - | - | 30 | measured |
| 210 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 211 | Stuttgart | 4.08 | 112,789 | - | - | - | - | 10 | predicted (travel demand) |
| 212 | Frankfurt | 3.00 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 213 | Hobart | 3.00 | 81,734 | 10 | - | 2 | 455 | 20 | measured |
| 214 | Lucca | 2.25 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 215 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 216 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 217 | Padua | 2.25 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 218 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 219 | Belfast | 4.15 | 224,315 | - | - | - | - | 10 | predicted (travel demand) |
| 220 | Hong Kong | 2.75 | 689,212 | 10 | 2 | 1 | 505 | 20 | measured |
| 221 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 222 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 223 | Eindhoven | 1.99 | - | 7 | - | 1 | 195 | 10 | published, never ranked (may be uncrawled) |
| 224 | Granada | 2.50 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 225 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 226 | Nantes | 3.83 | 67,689 | - | - | - | - | 10 | predicted (travel demand) |
| 227 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 228 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 229 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 230 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 231 | Brighton | 3.40 | 114,108 | - | - | - | - | 10 | predicted (travel demand) |
| 232 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 233 | Busan | 3.31 | 94,737 | - | - | - | - | 10 | predicted (travel demand) |
| 234 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 235 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 236 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 237 | Toulouse | 2.25 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 238 | Girona | 1.97 | 51,072 | 7 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 239 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 240 | Nice | 3.25 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 241 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 242 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 243 | Sao Paulo | 2.96 | 911 | - | - | - | - | 10 | predicted (travel demand) |
| 244 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 245 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 246 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 247 | Heidelberg | 2.69 | 75,837 | - | - | - | - | 10 | predicted (travel demand) |
| 248 | Como | 1.50 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 249 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 250 | Den Bosch | 1.50 | 39,682 | 11 | 1 | 1 | 119 | 20 | measured |
| 251 | Haarlem | 1.50 | 33,960 | 21 | - | 2 | 277 | 20 | measured |
| 252 | Trento | 1.50 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 253 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 254 | Genoa | 1.50 | 145,206 | 12 | 1 | 1 | 11 | 20 | measured |
| 255 | Ibiza | 1.85 | - | - | - | - | - | 10 | predicted (travel demand) |
| 256 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 257 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 258 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 259 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 260 | Lima | 2.03 | 132,792 | - | - | - | - | 10 | predicted (travel demand) |
| 261 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 262 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 263 | Ghent | 2.36 | 82,757 | - | - | - | - | 10 | predicted (travel demand) |
| 264 | Bari | 1.50 | 86,456 | 4 | - | - | 8 | 30 | measured |
| 265 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 266 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 267 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 268 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 269 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 270 | Dresden | 1.60 | 113,624 | 5 | 1 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 271 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 272 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 273 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 274 | Setubal | 1.25 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 275 | Kauai | 2.00 | - | 6 | - | - | 8 | 20 | measured |
| 276 | Hallstatt | 1.99 | 47,271 | - | - | - | - | 10 | predicted (travel demand) |
| 277 | Stockholm | 1.75 | 188,184 | 4 | 3 | - | - | 30 | measured |
| 278 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 279 | Leipzig | 1.50 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 280 | Sofia | 1.50 | 138,710 | 4 | - | - | - | 30 | measured |
| 281 | Split | 2.25 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 282 | Hiroshima | 1.39 | 129,791 | 8 | - | 2 | - | 10 | published, never ranked (may be uncrawled) |
| 283 | Zurich | 2.00 | 140,788 | 4 | - | - | - | 20 | measured |
| 284 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 285 | Tilburg | 1.03 | - | 7 | - | 1 | 84 | 10 | published, never ranked (may be uncrawled) |
| 286 | Leuven | 2.05 | 40,645 | - | - | - | - | 10 | predicted (travel demand) |
| 287 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 288 | Alkmaar | 1.01 | - | 7 | - | 1 | 79 | 10 | published, never ranked (may be uncrawled) |
| 289 | Bangkok | 2.00 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 290 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 291 | Perugia | 1.00 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 292 | Wroclaw | 1.25 | 123,894 | 5 | 1 | 1 | 121 | 20 | measured |
| 293 | Hilversum | 0.93 | - | 6 | - | 1 | 122 | 10 | published, never ranked (may be uncrawled) |
| 294 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 295 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 296 | Ljubljana | 1.75 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 297 | Yakushima | 1.13 | - | - | - | - | 1 | 10 | predicted (travel demand) |
| 298 | Matera | 1.00 | 67,033 | - | - | - | 2 | 10 | predicted (travel demand) |
| 299 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 300 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 301 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 302 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 303 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 304 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 305 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 306 | Savannah | 1.52 | 128,162 | 2 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 307 | Belgrade | 1.50 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 308 | Bergamo | 0.75 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 309 | Thessaloniki | 1.50 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 310 | Dordrecht | 0.71 | - | 7 | - | 1 | 103 | 10 | published, never ranked (may be uncrawled) |
| 311 | Parma | 0.75 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 312 | Amersfoort | 0.67 | - | 8 | 1 | 1 | 181 | 10 | published, never ranked (may be uncrawled) |
| 313 | Sapporo | 0.88 | 88,633 | 6 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 314 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 315 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 316 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 317 | Regensburg | 1.18 | 51,930 | - | - | - | 2 | 10 | predicted (travel demand) |
| 318 | Maui | 1.17 | - | 4 | - | - | 3 | 10 | published, never ranked (may be uncrawled) |
| 319 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 320 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 321 | Nagoya | 0.79 | 83,437 | 6 | - | - | 1 | 10 | published, never ranked (may be uncrawled) |
| 322 | Menorca | 0.73 | - | 4 | - | - | 4 | 10 | published, never ranked (may be uncrawled) |
| 323 | Charleston | 1.10 | 155,987 | 2 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 324 | Gdansk | 0.75 | 4,908 | 6 | 4 | - | 288 | 20 | measured |
| 325 | Salzburg | 0.75 | 107,243 | 5 | - | - | 34 | 20 | measured |
| 326 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 327 | Naha | 0.71 | 24,466 | 6 | - | - | 1 | 10 | published, never ranked (may be uncrawled) |
| 328 | Apeldoorn | 0.53 | - | 8 | - | 1 | 80 | 10 | published, never ranked (may be uncrawled) |
| 329 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 330 | Antwerp | 1.00 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 331 | Breda | 0.50 | 36,579 | 4 | - | 1 | 119 | 20 | measured |
| 332 | Bucharest | 1.00 | 136,836 | 4 | - | 1 | - | 20 | measured |
| 333 | Kanazawa | 0.63 | 25,778 | 7 | - | 1 | 2 | 10 | published, never ranked (may be uncrawled) |
| 334 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 335 | Venlo | 0.48 | - | 7 | - | 1 | 144 | 10 | published, never ranked (may be uncrawled) |
| 336 | Luxembourg City | 0.60 | 64,851 | 10 | - | 2 | 18 | 10 | published, never ranked (may be uncrawled) |
| 337 | Rothenburg ob der Tauber | 0.75 | 39,879 | 4 | - | 1 | 8 | 20 | measured |
| 338 | Ferrara | 0.50 | 27,490 | 5 | 1 | 1 | 7 | 20 | measured |
| 339 | Segovia | 0.54 | 30,968 | 6 | - | 1 | 5 | 10 | published, never ranked (may be uncrawled) |
| 340 | Enschede | 0.38 | - | 7 | - | 1 | 82 | 10 | published, never ranked (may be uncrawled) |
| 341 | Zaragoza | 0.50 | 87,580 | 7 | - | 1 | - | 20 | measured |
| 342 | Cologne | 0.75 | 191,812 | 5 | - | 1 | - | 30 | measured |
| 343 | Ottawa | 0.50 | - | 8 | - | 1 | 119 | 20 | measured |
| 344 | Modena | 0.44 | 51,698 | 5 | - | 1 | 3 | 10 | published, never ranked (may be uncrawled) |
| 345 | Ronda | 0.42 | 51,510 | 6 | - | - | 9 | 10 | published, never ranked (may be uncrawled) |
| 346 | Assen | 0.35 | - | 9 | - | 2 | 67 | 10 | published, never ranked (may be uncrawled) |
| 347 | Heerlen | 0.35 | - | 8 | - | 2 | 53 | 10 | published, never ranked (may be uncrawled) |
| 348 | Kamakura | 0.44 | 33,492 | 6 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 349 | Zwolle | 0.35 | - | 7 | - | 1 | 57 | 10 | published, never ranked (may be uncrawled) |
| 350 | Buenos Aires | 0.63 | 333,331 | 4 | - | - | - | 30 | measured |
| 351 | Deventer | 0.31 | - | 7 | - | 1 | 213 | 10 | published, never ranked (may be uncrawled) |
| 352 | Hoorn | 0.30 | - | 8 | - | 1 | 52 | 10 | published, never ranked (may be uncrawled) |
| 353 | Leeuwarden | 0.30 | - | 7 | - | 1 | 61 | 10 | published, never ranked (may be uncrawled) |
| 354 | Rouen | 0.54 | 72,334 | 12 | - | 1 | 6 | 10 | published, never ranked (may be uncrawled) |
| 355 | Tarragona | 0.36 | 32,396 | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 356 | Helmond | 0.29 | - | 7 | - | 1 | 55 | 10 | published, never ranked (may be uncrawled) |
| 357 | Hawaii | 0.50 | - | 6 | - | 1 | 6 | 30 | measured |
| 358 | Phoenix | 0.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 359 | Pamplona | 0.34 | 128,065 | 6 | - | - | 1 | 10 | published, never ranked (may be uncrawled) |
| 360 | Philadelphia | 0.50 | 405,294 | 1 | - | - | - | 20 | measured |
| 361 | Roosendaal | 0.26 | - | 8 | - | 1 | 116 | 10 | published, never ranked (may be uncrawled) |
| 362 | Cesky Krumlov | 0.34 | 28,582 | 6 | 2 | - | 11 | 10 | published, never ranked (may be uncrawled) |
| 363 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 364 | Coimbra | 0.25 | 34,962 | 4 | - | - | 5 | 20 | measured |
| 365 | Assisi | 0.25 | 30,278 | 6 | 1 | 2 | 6 | 20 | measured |
| 366 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 367 | Bamberg | 0.24 | 28,716 | 4 | 3 | 1 | 10 | 10 | published, never ranked (may be uncrawled) |
| 368 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 369 | George Town | 0.28 | 36,080 | - | - | - | - | 10 | predicted (travel demand) |
| 370 | Riga | 0.25 | 108,918 | 5 | - | - | - | 20 | measured |
| 371 | Vancouver | 0.25 | 351,552 | 4 | - | - | - | 30 | measured |
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

