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
| 1 | Brussels | 163.67 | 176,863 | 35 | 4 | 2 | 436 | 30 | measured |
| 2 | Lisbon | 79.00 | 201,877 | 36 | 16 | 3 | 67 | 30 | measured |
| 3 | Pamplona | 93.52 | 128,065 | 14 | - | 1 | 9 | 20 | measured |
| 4 | Barcelona | 71.28 | 346,477 | 56 | 14 | 7 | 180 | 30 | measured |
| 5 | Milan | 70.37 | 212,705 | 30 | 12 | 3 | 25 | 30 | measured |
| 6 | Amsterdam | 67.87 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 7 | Oahu | 81.72 | - | 21 | 2 | 3 | 163 | 20 | measured |
| 8 | Rome | 54.93 | 358,876 | 31 | 10 | 2 | 32 | 30 | measured |
| 9 | Florence | 46.99 | 184,099 | 27 | 9 | 1 | 27 | 30 | measured |
| 10 | Arnhem | 44.04 | 31,478 | 39 | 3 | 3 | 204 | 20 | measured |
| 11 | Tenerife | 57.43 | - | 4 | 2 | - | - | 20 | measured |
| 12 | Singapore | 56.75 | 967,821 | 34 | 6 | 3 | 165 | 30 | measured |
| 13 | Palermo | 39.95 | 124,310 | 21 | 9 | 1 | 37 | 20 | measured |
| 14 | Seville | 51.30 | 170,545 | 43 | 9 | 2 | - | 20 | measured |
| 15 | Berlin | 47.67 | 412,181 | 33 | 23 | 3 | 195 | 30 | measured |
| 16 | Tokyo | 38.59 | 394,702 | 21 | 10 | 1 | 5 | 20 | measured |
| 17 | Brisbane | 44.04 | 162,602 | 20 | 2 | 2 | 186 | 30 | measured |
| 18 | Valencia | 32.01 | 162,209 | 31 | 4 | 2 | 350 | 30 | measured |
| 19 | Los Angeles | 60.84 | 665,559 | 8 | 2 | - | - | 30 | measured |
| 20 | Prague | 41.31 | 303,350 | 30 | 21 | 4 | 31 | 30 | measured |
| 21 | Alicante | 30.19 | 77,454 | 21 | 4 | 2 | 44 | 20 | measured |
| 22 | Vienna | 37.46 | 283,090 | 32 | 18 | 5 | 376 | 30 | measured |
| 23 | Paris | 36.55 | 524,268 | 31 | 9 | 4 | 129 | 30 | measured |
| 24 | Malaga | 36.09 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 25 | Portland | 35.41 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 26 | London | 40.18 | 718,291 | 23 | 14 | 1 | - | 30 | measured |
| 27 | New York | 39.50 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 28 | Philadelphia | 39.95 | 405,294 | 1 | - | - | - | 20 | measured |
| 29 | Austin | 39.50 | 226,631 | 5 | 2 | - | - | 20 | measured |
| 30 | Birmingham | 37.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 31 | Dublin | 21.57 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 32 | Krakow | 24.97 | 140,824 | 38 | 8 | 3 | 198 | 30 | measured |
| 33 | Dallas | 36.77 | - | 9 | 1 | 1 | - | 30 | measured |
| 34 | Copenhagen | 33.14 | 218,621 | 16 | 2 | 2 | - | 30 | measured |
| 35 | Boston | 33.60 | 385,902 | 11 | 2 | 1 | - | 30 | measured |
| 36 | Vilnius | 23.15 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 37 | Utrecht | 17.03 | 67,963 | 27 | 7 | 2 | 340 | 20 | measured |
| 38 | Porto | 16.80 | 120,415 | 27 | 15 | 2 | 40 | 20 | measured |
| 39 | Haarlem | 16.34 | 33,960 | 21 | 1 | 2 | 277 | 20 | measured |
| 40 | The Hague | 16.34 | 236,723 | 31 | 2 | 5 | 167 | 20 | measured |
| 41 | Houston | 31.33 | - | 6 | - | - | - | 30 | measured |
| 42 | Cork | 20.88 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 43 | Munich | 20.43 | 224,067 | 45 | 15 | 6 | 80 | 30 | measured |
| 44 | Madeira | 17.93 | - | 10 | 1 | 1 | - | 20 | measured |
| 45 | Nijmegen | 14.76 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 46 | Kyoto | 18.84 | 142,353 | 18 | 12 | 2 | - | 20 | measured |
| 47 | Bath | 29.06 | 144,950 | 5 | 2 | 1 | - | 20 | measured |
| 48 | Ottawa | 19.07 | - | 21 | - | 3 | 122 | 20 | measured |
| 49 | Geneva | 18.61 | 162,269 | 21 | 5 | 4 | 131 | 20 | measured |
| 50 | Venice | 14.98 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 51 | Helmond | 13.62 | - | 20 | - | 2 | 54 | 20 | measured |
| 52 | Sintra | 13.39 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 53 | Reykjavik | 22.70 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 54 | New Orleans | 25.88 | 256,232 | 4 | 2 | 1 | - | 20 | measured |
| 55 | Granada | 16.34 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 56 | Fukuoka | 16.57 | 77,485 | 15 | 9 | 1 | - | 20 | measured |
| 57 | Palma de Mallorca | 14.53 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 58 | Leiden | 11.80 | 33,227 | 20 | 6 | 1 | 129 | 20 | measured |
| 59 | Las Vegas | 23.15 | - | 11 | - | 2 | - | 30 | measured |
| 60 | Jacksonville | 22.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 61 | Leeuwarden | 10.90 | - | 41 | - | 2 | 61 | 20 | measured |
| 62 | Cagliari | 11.58 | 51,351 | 14 | 1 | 2 | 15 | 20 | measured |
| 63 | Cadiz | 13.62 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 64 | Asheville | 20.89 | - | - | - | - | - | 10 | predicted (travel demand) |
| 65 | Long Beach | 20.48 | - | - | - | - | - | 10 | predicted (travel demand) |
| 66 | Little Rock | 20.40 | - | - | - | - | - | 10 | predicted (travel demand) |
| 67 | Edinburgh | 19.98 | 292,981 | 16 | 5 | 1 | - | 30 | measured |
| 68 | San Francisco | 19.52 | 361,111 | 6 | 1 | 1 | - | 30 | measured |
| 69 | Athens | 19.30 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 70 | Melbourne | 12.71 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 71 | Seattle | 18.16 | 398,724 | 6 | 1 | - | - | 30 | measured |
| 72 | Oakland | 18.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 73 | Sardinia | 10.21 | - | 5 | 4 | - | 8 | 20 | measured |
| 74 | Lexington | 18.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 75 | Reno | 18.19 | - | - | - | - | - | 10 | predicted (travel demand) |
| 76 | Dordrecht | 9.08 | - | 20 | 1 | 2 | 105 | 20 | measured |
| 77 | Des Moines | 18.11 | - | - | - | - | - | 10 | predicted (travel demand) |
| 78 | Nice | 17.93 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 79 | Daytona Beach | 17.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 80 | Madrid | 10.90 | 274,553 | 17 | 11 | 2 | - | 20 | measured |
| 81 | Hoorn | 8.63 | - | 8 | - | 1 | 52 | 20 | measured |
| 82 | Monterey | 17.25 | - | 3 | 1 | - | - | 20 | measured |
| 83 | Chicago | 16.80 | 485,769 | 6 | - | - | - | 30 | measured |
| 84 | Tilburg | 8.40 | - | 20 | - | 3 | 87 | 20 | measured |
| 85 | Coimbra | 9.08 | 34,962 | 4 | - | - | 5 | 20 | measured |
| 86 | Chattanooga | 16.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 87 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 88 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 89 | Oslo | 13.85 | 181,113 | 4 | - | - | - | 20 | measured |
| 90 | Huntsville | 15.35 | - | - | - | - | - | 10 | predicted (travel demand) |
| 91 | Osaka | 9.76 | 163,112 | 6 | 1 | - | - | 30 | measured |
| 92 | Parma | 8.40 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 93 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 94 | West Palm Beach | 14.98 | - | - | - | - | - | 10 | predicted (travel demand) |
| 95 | Saint Petersburg | 14.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 96 | St. Louis | 14.80 | - | - | - | - | - | 10 | predicted (travel demand) |
| 97 | Strasbourg | 9.53 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 98 | Tampa | 14.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 99 | Enschede | 7.04 | - | 15 | 1 | 2 | 82 | 20 | measured |
| 100 | Cyprus | 13.62 | - | 4 | - | - | - | 20 | measured |
| 101 | Cincinnati | 13.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 102 | Bordeaux | 8.85 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 103 | Eindhoven | 6.58 | - | 21 | - | 4 | 195 | 20 | measured |
| 104 | Lansing | 13.02 | - | - | - | - | - | 10 | predicted (travel demand) |
| 105 | Glasgow | 12.03 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 106 | Perth | 12.49 | 180,478 | 6 | 3 | 1 | - | 30 | measured |
| 107 | Caserta | 6.36 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 108 | Detroit | 12.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 109 | Hawaii | 10.90 | - | 6 | - | 1 | 6 | 30 | measured |
| 110 | Budapest | 11.58 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 111 | Cordoba | 7.72 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 112 | Tallinn | 7.95 | 124,888 | 9 | 3 | 2 | 42 | 20 | measured |
| 113 | Groningen | 5.90 | 31,401 | 21 | 1 | 2 | 76 | 20 | measured |
| 114 | Denver | 11.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 115 | Warsaw | 7.72 | 197,929 | 39 | 5 | 4 | 1407 | 30 | measured |
| 116 | Menorca | 7.49 | - | 6 | - | - | 2 | 20 | measured |
| 117 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 118 | San Jose | 11.39 | - | - | - | - | - | 10 | predicted (travel demand) |
| 119 | Sacramento | 11.32 | - | - | - | - | - | 10 | predicted (travel demand) |
| 120 | Jersey City | 10.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 121 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 122 | Istanbul | 9.76 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 123 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 124 | Ibiza | 6.81 | - | 1 | - | - | 4 | 20 | measured |
| 125 | Milwaukee | 10.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 126 | Salt Lake City | 10.31 | - | - | - | - | - | 10 | predicted (travel demand) |
| 127 | Atlanta | 10.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 128 | Anchorage | 10.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 129 | Cambridge | 10.21 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 130 | Raleigh | 10.07 | - | - | - | - | - | 10 | predicted (travel demand) |
| 131 | Crete | 9.99 | - | 4 | 3 | - | - | 20 | measured |
| 132 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 133 | Bari | 5.90 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 134 | Seoul | 9.08 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 135 | Cleveland | 9.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 136 | El Paso | 9.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 137 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 138 | Washington DC | 8.63 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 139 | Miami | 9.48 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 140 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 141 | Sydney | 9.08 | 305,304 | 7 | 1 | - | - | 30 | measured |
| 142 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 143 | Segovia | 5.67 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 144 | Perugia | 4.77 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 145 | Nashville | 8.93 | - | - | - | - | - | 10 | predicted (travel demand) |
| 146 | Hobart | 5.90 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 147 | Leipzig | 5.90 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 148 | Potsdam | 5.90 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 149 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 150 | Amersfoort | 4.31 | - | 18 | 1 | 2 | 181 | 20 | measured |
| 151 | Helsinki | 6.81 | 148,908 | 12 | 2 | 1 | 13 | 30 | measured |
| 152 | Ann Arbor | 8.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 153 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 154 | Luxembourg City | 5.45 | 64,851 | 10 | 5 | 2 | 18 | 20 | measured |
| 155 | Yakushima | 4.99 | - | 1 | - | - | 1 | 20 | measured |
| 156 | Albuquerque | 7.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 157 | Salzburg | 5.22 | 107,243 | 9 | 3 | 2 | 34 | 20 | measured |
| 158 | Zurich | 7.49 | 140,788 | 6 | 1 | - | - | 20 | measured |
| 159 | Bangkok | 7.72 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 160 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 161 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 162 | Padua | 3.86 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 163 | Sorrento | 3.63 | 40,049 | 7 | - | 1 | 20 | 20 | measured |
| 164 | Zwolle | 3.63 | - | 16 | - | 2 | 56 | 20 | measured |
| 165 | Ljubljana | 7.04 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 166 | Lyon | 4.77 | 136,951 | 13 | 4 | 1 | 156 | 20 | measured |
| 167 | Hong Kong | 4.65 | 689,212 | 10 | 4 | 1 | 505 | 20 | measured |
| 168 | Charleston | 6.81 | 155,987 | 2 | 1 | - | - | 20 | measured |
| 169 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 170 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 171 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 172 | Hilo | 4.99 | - | 6 | - | 1 | 16 | 20 | measured |
| 173 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 174 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 175 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 176 | Como | 3.18 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 177 | Heerlen | 3.18 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 178 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 179 | Bristol | 6.13 | 163,983 | 6 | 2 | - | - | 20 | measured |
| 180 | Verona | 3.63 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 181 | Turin | 2.95 | 147,456 | 11 | 7 | 2 | 30 | 20 | measured |
| 182 | Girona | 3.41 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 183 | Beijing | 5.79 | 269,737 | 7 | 1 | - | - | 30 | measured |
| 184 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 185 | Nuremberg | 3.86 | 161,614 | 12 | 1 | 1 | 38 | 20 | measured |
| 186 | Vancouver | 5.68 | 351,552 | 7 | - | - | - | 30 | measured |
| 187 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 188 | Indianapolis | 5.45 | - | 1 | - | - | - | 30 | measured |
| 189 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 190 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 191 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 192 | Montreal | 5.45 | 315,322 | 13 | 1 | 2 | - | 30 | measured |
| 193 | Sapporo | 3.63 | 88,633 | 6 | - | - | - | 20 | measured |
| 194 | Savannah | 5.45 | 128,162 | 2 | 1 | - | - | 20 | measured |
| 195 | Apeldoorn | 2.72 | - | 10 | - | 2 | 80 | 20 | measured |
| 196 | Trento | 2.72 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 197 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 198 | Genoa | 2.95 | 145,206 | 13 | 2 | 1 | 10 | 20 | measured |
| 199 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 200 | Santa Fe | 5.17 | - | - | - | - | - | 10 | predicted (travel demand) |
| 201 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 202 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 203 | Bologna | 2.72 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 204 | Alkmaar | 2.50 | - | 14 | - | 2 | 79 | 20 | measured |
| 205 | San Diego | 4.99 | 214,939 | 4 | 1 | 1 | - | 20 | measured |
| 206 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 207 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 208 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 209 | Belfast | 4.77 | 224,315 | 4 | - | 1 | - | 20 | measured |
| 210 | Graz | 3.18 | 65,717 | 12 | 7 | 1 | 87 | 20 | measured |
| 211 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 212 | Stockholm | 3.63 | 188,184 | 6 | 4 | - | - | 30 | measured |
| 213 | Den Bosch | 2.27 | 39,682 | 12 | 2 | 1 | 118 | 20 | measured |
| 214 | Hilversum | 2.27 | - | 6 | 1 | 1 | 122 | 20 | measured |
| 215 | Maastricht | 2.27 | 47,763 | 19 | - | 2 | 135 | 20 | measured |
| 216 | Naples | 2.27 | 198,913 | 24 | 3 | 3 | 46 | 20 | measured |
| 217 | Pisa | 2.95 | 52,174 | 4 | - | 1 | - | 20 | measured |
| 218 | Split | 4.54 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 219 | Dresden | 2.95 | 113,624 | 5 | 5 | 1 | - | 20 | measured |
| 220 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 221 | Hamburg | 4.09 | 191,221 | 6 | 1 | 1 | - | 30 | measured |
| 222 | Maui | 4.09 | - | 4 | - | - | 3 | 20 | measured |
| 223 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 224 | Taipei | 4.31 | 143,193 | 4 | 1 | - | - | 30 | measured |
| 225 | Belgrade | 4.20 | 178,116 | 5 | 5 | - | - | 20 | measured |
| 226 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 227 | Boise | 4.09 | - | 4 | - | 1 | - | 30 | measured |
| 228 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 229 | Assen | 2.04 | - | 10 | - | 2 | 66 | 20 | measured |
| 230 | Deventer | 2.04 | - | 12 | - | 1 | 213 | 20 | measured |
| 231 | Quebec City | 2.72 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 232 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 233 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 234 | Catania | 2.27 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 235 | Dubrovnik | 3.63 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 236 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 237 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 238 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 239 | Toronto | 3.63 | 411,011 | 6 | - | - | - | 30 | measured |
| 240 | Kauai | 3.18 | - | 6 | 1 | - | 8 | 20 | measured |
| 241 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 242 | Delft | 1.82 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 243 | Kamakura | 2.27 | 33,492 | 6 | - | - | - | 20 | measured |
| 244 | Rio de Janeiro | 3.63 | 279,431 | 6 | - | - | - | 30 | measured |
| 245 | Kanazawa | 2.27 | 25,778 | 7 | 2 | 1 | 2 | 20 | measured |
| 246 | Guimaraes | 1.82 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 247 | Oxford | 3.41 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 248 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 249 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 250 | Matera | 2.04 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 251 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 252 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 253 | Bratislava | 2.27 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 254 | San Antonio | 3.32 | - | 4 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 255 | Braga | 1.82 | 34,522 | 4 | 2 | - | 8 | 20 | measured |
| 256 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 257 | Fort Worth | 3.28 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 258 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 259 | Fort Lauderdale | 3.18 | - | 4 | - | - | - | 30 | measured |
| 260 | Mexico City | 3.06 | 566,583 | 9 | 2 | - | - | 30 | measured |
| 261 | Breda | 1.59 | 36,579 | 10 | - | 2 | 118 | 20 | measured |
| 262 | Rotterdam | 1.59 | 104,938 | 12 | - | 2 | 83 | 20 | measured |
| 263 | Ferrara | 1.82 | 27,490 | 5 | 3 | 1 | 7 | 20 | measured |
| 264 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 265 | Spokane | 2.27 | - | 13 | - | 2 | 18 | 20 | measured |
| 266 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 267 | Nagoya | 2.04 | 83,437 | 6 | 1 | - | 1 | 20 | measured |
| 268 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 269 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 270 | Heidelberg | 2.72 | 75,837 | 6 | 1 | 1 | - | 20 | measured |
| 271 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 272 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 273 | Regensburg | 2.72 | 51,930 | 5 | 1 | 1 | 4 | 20 | measured |
| 274 | Cologne | 2.95 | 191,812 | 5 | - | 1 | - | 30 | measured |
| 275 | Liverpool | 2.95 | 248,189 | 2 | 1 | - | - | 20 | measured |
| 276 | Riga | 2.72 | 108,918 | 5 | 2 | - | - | 20 | measured |
| 277 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 278 | Hiroshima | 1.82 | 129,791 | 17 | 5 | 3 | - | 20 | measured |
| 279 | Toulouse | 1.82 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 280 | Bergamo | 1.36 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 281 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 282 | Lucca | 1.36 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 283 | Thessaloniki | 2.72 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 284 | Trieste | 1.36 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 285 | Venlo | 1.36 | - | 7 | - | 1 | 144 | 20 | measured |
| 286 | York | 2.72 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 287 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 288 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 289 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 290 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 291 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 292 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 293 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 294 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 295 | Naha | 1.59 | 24,466 | 6 | - | - | 1 | 20 | measured |
| 296 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 297 | Brno | 1.59 | 63,714 | 8 | 5 | 2 | 34 | 20 | measured |
| 298 | Ghent | 2.27 | 82,757 | 8 | 1 | 1 | - | 20 | measured |
| 299 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 300 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 301 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 302 | Aarhus | 2.27 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 303 | Pittsburgh | 2.27 | - | 4 | - | 1 | - | 20 | measured |
| 304 | Minneapolis | 2.27 | - | 4 | - | - | - | 20 | measured |
| 305 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 306 | Buenos Aires | 2.04 | 333,331 | 4 | 2 | - | - | 30 | measured |
| 307 | Salamanca | 1.36 | 47,897 | 4 | - | 1 | 1 | 20 | measured |
| 308 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 309 | Lausanne | 2.04 | 68,242 | 8 | 1 | 1 | - | 20 | measured |
| 310 | Nantes | 2.04 | 67,689 | 1 | 1 | - | - | 20 | measured |
| 311 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 312 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 313 | Baltimore | 1.82 | - | 4 | - | - | - | 20 | measured |
| 314 | Cardiff | 1.82 | - | 4 | - | 1 | - | 20 | measured |
| 315 | Bucharest | 1.84 | 136,836 | 4 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 316 | Roosendaal | 0.91 | - | 8 | - | 1 | 116 | 20 | measured |
| 317 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 318 | Tulsa | 1.82 | - | 1 | - | - | - | 20 | measured |
| 319 | Hallstatt | 1.59 | 47,271 | 5 | 1 | - | - | 20 | measured |
| 320 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 321 | Stuttgart | 1.36 | 112,789 | 6 | 1 | - | - | 20 | measured |
| 322 | Zaragoza | 1.14 | 87,580 | 7 | - | 1 | - | 20 | measured |
| 323 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 324 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 325 | Gdansk | 1.14 | 4,908 | 12 | 4 | 1 | 307 | 20 | measured |
| 326 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 327 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 328 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 329 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 330 | Ronda | 0.91 | 51,510 | 6 | 1 | - | 9 | 20 | measured |
| 331 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 332 | Auckland | 1.36 | 152,056 | 5 | 2 | - | - | 20 | measured |
| 333 | Frankfurt | 0.91 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 334 | Kansas City | 1.36 | - | 4 | - | 1 | - | 30 | measured |
| 335 | Leuven | 1.36 | 40,645 | 4 | - | - | - | 20 | measured |
| 336 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 337 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 338 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 339 | Setubal | 0.68 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 340 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 341 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 342 | Freiburg | 1.14 | 92,752 | 7 | 2 | 1 | - | 20 | measured |
| 343 | Brighton | 1.14 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 344 | Manchester | 1.14 | 316,438 | 5 | - | - | - | 30 | measured |
| 345 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 346 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 347 | Bilbao | 0.68 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 348 | Wroclaw | 0.68 | 123,894 | 5 | 1 | 1 | 121 | 20 | measured |
| 349 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 350 | Busan | 0.91 | 94,737 | 2 | - | - | - | 20 | measured |
| 351 | Rothenburg ob der Tauber | 0.68 | 39,879 | 4 | - | 1 | 8 | 20 | measured |
| 352 | Sao Paulo | 0.79 | 911 | 1 | - | - | - | 20 | measured |
| 353 | Tarragona | 0.45 | 32,396 | 4 | 2 | - | - | 20 | measured |
| 354 | Modena | 0.45 | 51,698 | 5 | 1 | 1 | 3 | 20 | measured |
| 355 | Assisi | 0.45 | 30,278 | 6 | 1 | 2 | 6 | 20 | measured |
| 356 | Poznan | 0.45 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 357 | Sofia | 0.45 | 138,710 | 4 | - | - | - | 30 | measured |
| 358 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 359 | Rouen | 0.54 | 72,334 | 12 | - | 1 | 6 | 10 | published, never ranked (may be uncrawled) |
| 360 | Phoenix | 0.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 361 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 362 | Bruges | 0.45 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 363 | Canberra | 0.45 | - | 1 | 1 | - | - | 30 | measured |
| 364 | Turku | 0.45 | - | 1 | - | - | - | 30 | measured |
| 365 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 366 | Cesky Krumlov | 0.23 | 28,582 | 6 | 3 | - | 11 | 20 | measured |
| 367 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 368 | Bamberg | 0.23 | 28,716 | 5 | 4 | 1 | 10 | 20 | measured |
| 369 | George Town | 0.28 | 36,080 | - | - | - | - | 10 | predicted (travel demand) |
| 370 | Allentown | 0.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 371 | Antwerp | 0.23 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 372 | Gothenburg | 0.23 | 119,991 | 5 | - | 1 | - | 20 | measured |
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

