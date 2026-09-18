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
| 1 | Brussels | 164.63 | 176,863 | 35 | 4 | 2 | 436 | 30 | measured |
| 2 | Pamplona | 96.75 | 128,065 | 14 | - | 1 | 9 | 20 | measured |
| 3 | Lisbon | 71.63 | 201,877 | 36 | 16 | 3 | 67 | 30 | measured |
| 4 | Barcelona | 66.12 | 346,477 | 56 | 14 | 7 | 180 | 30 | measured |
| 5 | Milan | 65.90 | 212,705 | 30 | 12 | 3 | 25 | 30 | measured |
| 6 | Amsterdam | 65.67 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 7 | Oahu | 87.27 | - | 21 | 2 | 3 | 163 | 20 | measured |
| 8 | Arnhem | 51.35 | 31,478 | 39 | 3 | 3 | 204 | 20 | measured |
| 9 | Rome | 50.91 | 358,876 | 31 | 10 | 2 | 32 | 30 | measured |
| 10 | Tenerife | 60.17 | - | 4 | 4 | - | - | 20 | measured |
| 11 | Florence | 44.52 | 184,099 | 27 | 9 | 1 | 27 | 30 | measured |
| 12 | Prague | 58.18 | 303,350 | 30 | 21 | 4 | 31 | 30 | measured |
| 13 | Palermo | 43.20 | 124,310 | 21 | 9 | 1 | 37 | 20 | measured |
| 14 | Singapore | 57.08 | 967,821 | 34 | 6 | 3 | 165 | 30 | measured |
| 15 | Berlin | 56.42 | 412,181 | 33 | 23 | 3 | 195 | 30 | measured |
| 16 | Seville | 48.93 | 170,545 | 43 | 9 | 2 | - | 20 | measured |
| 17 | Tokyo | 40.77 | 394,702 | 22 | 10 | 1 | 5 | 20 | measured |
| 18 | Alicante | 31.29 | 77,454 | 21 | 4 | 2 | 44 | 20 | measured |
| 19 | Brisbane | 39.67 | 162,602 | 20 | 2 | 2 | 186 | 30 | measured |
| 20 | Valencia | 29.75 | 162,209 | 31 | 4 | 2 | 350 | 30 | measured |
| 21 | Vienna | 37.69 | 283,090 | 32 | 18 | 5 | 376 | 30 | measured |
| 22 | Los Angeles | 54.21 | 665,559 | 8 | 2 | - | - | 30 | measured |
| 23 | Paris | 36.36 | 524,268 | 31 | 9 | 4 | 129 | 30 | measured |
| 24 | Portland | 36.14 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 25 | Malaga | 35.70 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 26 | Philadelphia | 44.08 | 405,294 | 1 | - | - | - | 20 | measured |
| 27 | London | 36.80 | 718,291 | 23 | 14 | 1 | - | 30 | measured |
| 28 | New York | 37.91 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 29 | Austin | 40.99 | 226,631 | 5 | 2 | - | - | 20 | measured |
| 30 | Utrecht | 19.83 | 67,963 | 27 | 7 | 2 | 340 | 20 | measured |
| 31 | Porto | 19.17 | 120,415 | 27 | 15 | 2 | 40 | 20 | measured |
| 32 | Krakow | 25.34 | 140,824 | 38 | 8 | 3 | 198 | 30 | measured |
| 33 | Birmingham | 37.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 34 | Dublin | 21.38 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 35 | Dallas | 36.58 | - | 9 | 1 | 1 | - | 30 | measured |
| 36 | Copenhagen | 32.62 | 218,621 | 16 | 2 | 2 | - | 30 | measured |
| 37 | Munich | 22.70 | 224,067 | 45 | 15 | 6 | 80 | 30 | measured |
| 38 | Bath | 33.72 | 144,950 | 5 | 2 | 1 | - | 20 | measured |
| 39 | Leiden | 16.09 | 33,227 | 20 | 6 | 1 | 129 | 20 | measured |
| 40 | The Hague | 15.65 | 236,723 | 31 | 2 | 5 | 167 | 20 | measured |
| 41 | Boston | 29.97 | 385,902 | 11 | 2 | 1 | - | 30 | measured |
| 42 | Kyoto | 19.39 | 142,353 | 18 | 12 | 2 | - | 20 | measured |
| 43 | Houston | 29.09 | - | 6 | - | - | - | 30 | measured |
| 44 | Vilnius | 19.39 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 45 | Sintra | 14.33 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 46 | Cork | 18.95 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 47 | Haarlem | 14.10 | 33,960 | 21 | 1 | 2 | 277 | 20 | measured |
| 48 | Venice | 15.21 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 49 | Nijmegen | 13.66 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 50 | Helmond | 12.78 | - | 20 | - | 2 | 54 | 20 | measured |
| 51 | Fukuoka | 16.53 | 77,485 | 15 | 9 | 1 | - | 20 | measured |
| 52 | Ottawa | 16.97 | - | 21 | - | 3 | 122 | 20 | measured |
| 53 | Cagliari | 13.66 | 51,351 | 14 | 1 | 2 | 15 | 20 | measured |
| 54 | Reykjavik | 20.94 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 55 | Las Vegas | 24.24 | - | 11 | - | 2 | - | 30 | measured |
| 56 | Granada | 14.99 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 57 | Jacksonville | 22.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 58 | Madeira | 13.66 | - | 10 | 1 | 1 | - | 20 | measured |
| 59 | New Orleans | 22.48 | 256,232 | 4 | 2 | 1 | - | 20 | measured |
| 60 | Geneva | 14.77 | 162,269 | 21 | 5 | 4 | 131 | 20 | measured |
| 61 | Cadiz | 13.66 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 62 | Palma de Mallorca | 12.78 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 63 | Asheville | 20.89 | - | - | - | - | - | 10 | predicted (travel demand) |
| 64 | Tilburg | 10.36 | - | 20 | - | 3 | 87 | 20 | measured |
| 65 | Edinburgh | 20.28 | 292,981 | 16 | 5 | 1 | - | 30 | measured |
| 66 | Long Beach | 20.48 | - | - | - | - | - | 10 | predicted (travel demand) |
| 67 | Little Rock | 20.40 | - | - | - | - | - | 10 | predicted (travel demand) |
| 68 | Athens | 19.61 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 69 | Madrid | 12.34 | 274,553 | 17 | 11 | 2 | - | 20 | measured |
| 70 | Monterey | 19.83 | - | 3 | 1 | - | - | 20 | measured |
| 71 | Oakland | 18.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 72 | Lexington | 18.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 73 | Reno | 18.19 | - | - | - | - | - | 10 | predicted (travel demand) |
| 74 | Des Moines | 18.11 | - | - | - | - | - | 10 | predicted (travel demand) |
| 75 | Daytona Beach | 17.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 76 | Parma | 9.70 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 77 | Melbourne | 11.46 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 78 | Dordrecht | 8.37 | - | 20 | 1 | 2 | 105 | 20 | measured |
| 79 | Hoorn | 8.37 | - | 12 | - | 2 | 52 | 20 | measured |
| 80 | Chattanooga | 16.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 81 | San Francisco | 16.31 | 361,111 | 6 | 1 | 1 | - | 30 | measured |
| 82 | Nice | 16.53 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 83 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 84 | Chicago | 15.87 | 485,769 | 6 | - | - | - | 30 | measured |
| 85 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 86 | Sardinia | 8.60 | - | 5 | 4 | - | 8 | 20 | measured |
| 87 | Coimbra | 8.37 | 34,962 | 4 | - | - | 5 | 20 | measured |
| 88 | Huntsville | 15.35 | - | - | - | - | - | 10 | predicted (travel demand) |
| 89 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 90 | West Palm Beach | 14.98 | - | - | - | - | - | 10 | predicted (travel demand) |
| 91 | Saint Petersburg | 14.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 92 | St. Louis | 14.80 | - | - | - | - | - | 10 | predicted (travel demand) |
| 93 | Oslo | 12.78 | 181,113 | 4 | - | - | - | 20 | measured |
| 94 | Seattle | 13.66 | 398,724 | 6 | 1 | - | - | 30 | measured |
| 95 | Tampa | 14.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 96 | Bordeaux | 9.26 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 97 | Enschede | 6.83 | - | 15 | 1 | 2 | 82 | 20 | measured |
| 98 | Strasbourg | 9.04 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 99 | Cincinnati | 13.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 100 | Groningen | 6.61 | 31,401 | 21 | 1 | 2 | 76 | 20 | measured |
| 101 | Lansing | 13.02 | - | - | - | - | - | 10 | predicted (travel demand) |
| 102 | Glasgow | 12.12 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 103 | Eindhoven | 6.39 | - | 21 | - | 4 | 195 | 20 | measured |
| 104 | Warsaw | 8.37 | 197,929 | 39 | 5 | 4 | 1407 | 30 | measured |
| 105 | Detroit | 12.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 106 | Osaka | 7.71 | 163,112 | 6 | 1 | - | - | 30 | measured |
| 107 | Budapest | 11.46 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 108 | Leeuwarden | 5.95 | - | 41 | - | 2 | 61 | 20 | measured |
| 109 | Cyprus | 11.46 | - | 4 | - | - | - | 20 | measured |
| 110 | Denver | 11.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 111 | Caserta | 5.73 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 112 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 113 | San Jose | 11.39 | - | - | - | - | - | 10 | predicted (travel demand) |
| 114 | Sacramento | 11.32 | - | - | - | - | - | 10 | predicted (travel demand) |
| 115 | Jersey City | 10.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 116 | Menorca | 7.27 | - | 6 | - | - | 2 | 20 | measured |
| 117 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 118 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 119 | Yakushima | 6.83 | - | 2 | - | - | 1 | 20 | measured |
| 120 | Milwaukee | 10.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 121 | Perth | 10.36 | 180,478 | 6 | 3 | 1 | - | 30 | measured |
| 122 | Tallinn | 7.05 | 124,888 | 9 | 3 | 2 | 42 | 20 | measured |
| 123 | Salt Lake City | 10.31 | - | - | - | - | - | 10 | predicted (travel demand) |
| 124 | Atlanta | 10.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 125 | Anchorage | 10.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 126 | Raleigh | 10.07 | - | - | - | - | - | 10 | predicted (travel demand) |
| 127 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 128 | Cambridge | 9.92 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 129 | Cleveland | 9.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 130 | Ibiza | 6.17 | - | 1 | - | - | 4 | 20 | measured |
| 131 | El Paso | 9.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 132 | Istanbul | 8.48 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 133 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 134 | Zurich | 9.26 | 140,788 | 6 | 1 | - | - | 20 | measured |
| 135 | Segovia | 5.95 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 136 | Crete | 9.48 | - | 4 | 3 | - | - | 20 | measured |
| 137 | Miami | 9.48 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 138 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 139 | Bari | 5.51 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 140 | Hobart | 6.17 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 141 | Potsdam | 6.17 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 142 | Washington DC | 8.37 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 143 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 144 | Leipzig | 5.95 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 145 | Nashville | 8.93 | - | - | - | - | - | 10 | predicted (travel demand) |
| 146 | Seoul | 8.15 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 147 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 148 | Ann Arbor | 8.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 149 | Amersfoort | 4.19 | - | 18 | 1 | 2 | 181 | 20 | measured |
| 150 | Sydney | 8.15 | 305,304 | 7 | 1 | - | - | 30 | measured |
| 151 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 152 | Montreal | 8.15 | 315,322 | 13 | 1 | 2 | - | 30 | measured |
| 153 | Luxembourg City | 5.29 | 64,851 | 10 | 5 | 2 | 18 | 20 | measured |
| 154 | Maastricht | 3.97 | 47,763 | 19 | - | 2 | 135 | 20 | measured |
| 155 | Padua | 4.19 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 156 | Perugia | 4.19 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 157 | Albuquerque | 7.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 158 | Ljubljana | 7.49 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 159 | Lyon | 5.07 | 136,951 | 13 | 4 | 1 | 156 | 20 | measured |
| 160 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 161 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 162 | Charleston | 7.05 | 155,987 | 2 | 1 | - | - | 20 | measured |
| 163 | Hong Kong | 4.63 | 689,212 | 10 | 4 | 1 | 505 | 20 | measured |
| 164 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 165 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 166 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 167 | Heerlen | 3.31 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 168 | Naples | 3.31 | 198,913 | 24 | 3 | 3 | 46 | 20 | measured |
| 169 | Sorrento | 3.31 | 40,049 | 7 | - | 1 | 20 | 20 | measured |
| 170 | Zwolle | 3.31 | - | 16 | - | 2 | 56 | 20 | measured |
| 171 | Bangkok | 6.61 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 172 | Bristol | 6.61 | 163,983 | 6 | 2 | - | - | 20 | measured |
| 173 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 174 | Genoa | 3.53 | 145,206 | 13 | 2 | 1 | 10 | 20 | measured |
| 175 | Hawaii | 5.73 | - | 6 | - | 1 | 6 | 30 | measured |
| 176 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 177 | Helsinki | 5.07 | 148,908 | 12 | 2 | 1 | 13 | 30 | measured |
| 178 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 179 | Verona | 3.75 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 180 | Sapporo | 4.19 | 88,633 | 6 | - | - | - | 20 | measured |
| 181 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 182 | Cordoba | 3.97 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 183 | Turin | 3.09 | 147,456 | 11 | 7 | 2 | 30 | 20 | measured |
| 184 | Indianapolis | 5.73 | - | 1 | - | - | - | 30 | measured |
| 185 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 186 | Bologna | 3.09 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 187 | Beijing | 5.73 | 269,737 | 7 | 1 | - | - | 30 | measured |
| 188 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 189 | Girona | 3.31 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 190 | Salzburg | 3.75 | 107,243 | 9 | 3 | 2 | 34 | 20 | measured |
| 191 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 192 | Guimaraes | 2.87 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 193 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 194 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 195 | Pisa | 3.53 | 52,174 | 4 | - | - | - | 20 | measured |
| 196 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 197 | San Diego | 5.29 | 214,939 | 4 | 1 | 1 | - | 20 | measured |
| 198 | Savannah | 5.29 | 128,162 | 2 | 1 | - | - | 20 | measured |
| 199 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 200 | Santa Fe | 5.17 | - | - | - | - | - | 10 | predicted (travel demand) |
| 201 | Dubrovnik | 4.85 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 202 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 203 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 204 | Stockholm | 3.97 | 188,184 | 6 | 4 | - | - | 30 | measured |
| 205 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 206 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 207 | Nuremberg | 3.31 | 161,614 | 12 | 1 | 1 | 38 | 20 | measured |
| 208 | Vancouver | 4.85 | 351,552 | 7 | - | - | - | 30 | measured |
| 209 | Como | 2.42 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 210 | Deventer | 2.42 | - | 12 | - | 1 | 213 | 20 | measured |
| 211 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 212 | Kanazawa | 3.09 | 25,778 | 7 | 2 | 1 | 2 | 20 | measured |
| 213 | Dresden | 3.09 | 113,624 | 5 | 5 | 1 | - | 20 | measured |
| 214 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 215 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 216 | Den Bosch | 2.20 | 39,682 | 12 | 2 | 1 | 118 | 20 | measured |
| 217 | Trento | 2.20 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 218 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 219 | Toronto | 4.19 | 411,011 | 6 | - | - | - | 30 | measured |
| 220 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 221 | Split | 4.19 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 222 | Kauai | 3.53 | - | 6 | 1 | - | 8 | 20 | measured |
| 223 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 224 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 225 | Nagoya | 2.64 | 83,437 | 6 | 1 | - | 1 | 20 | measured |
| 226 | Belfast | 3.97 | 224,315 | 4 | - | 1 | - | 20 | measured |
| 227 | Boise | 3.97 | - | 4 | - | 1 | - | 30 | measured |
| 228 | Alkmaar | 1.98 | - | 14 | - | 2 | 79 | 20 | measured |
| 229 | Apeldoorn | 1.98 | - | 10 | - | 2 | 80 | 20 | measured |
| 230 | Delft | 1.98 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 231 | Hilversum | 1.98 | - | 6 | 1 | 1 | 122 | 20 | measured |
| 232 | Quebec City | 2.64 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 233 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 234 | Belgrade | 3.86 | 178,116 | 5 | 5 | - | - | 20 | measured |
| 235 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 236 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 237 | Oxford | 3.75 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 238 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 239 | Taipei | 3.75 | 143,193 | 4 | 1 | - | - | 30 | measured |
| 240 | Catania | 2.20 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 241 | Hamburg | 3.53 | 191,221 | 6 | 1 | 1 | - | 30 | measured |
| 242 | Maui | 3.53 | - | 4 | - | - | 3 | 20 | measured |
| 243 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 244 | Fort Lauderdale | 3.53 | - | 4 | - | - | - | 30 | measured |
| 245 | Minneapolis | 3.53 | - | 4 | - | - | - | 20 | measured |
| 246 | Assen | 1.76 | - | 10 | - | 2 | 66 | 20 | measured |
| 247 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 248 | Ferrara | 1.98 | 27,490 | 5 | 3 | 1 | 7 | 20 | measured |
| 249 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 250 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 251 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 252 | Rio de Janeiro | 3.42 | 279,431 | 6 | - | - | - | 30 | measured |
| 253 | Regensburg | 3.09 | 51,930 | 5 | 1 | 1 | 4 | 20 | measured |
| 254 | Mexico City | 3.20 | 566,583 | 9 | 2 | - | - | 30 | measured |
| 255 | Matera | 1.98 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 256 | San Antonio | 3.32 | - | 4 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 257 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 258 | Fort Worth | 3.28 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 259 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 260 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 261 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 262 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 263 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 264 | Spokane | 2.20 | - | 13 | - | 2 | 18 | 20 | measured |
| 265 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 266 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 267 | Heidelberg | 2.64 | 75,837 | 6 | 1 | 1 | - | 20 | measured |
| 268 | Hilo | 2.20 | - | 6 | - | 1 | 16 | 20 | measured |
| 269 | Cologne | 2.87 | 191,812 | 5 | - | 1 | - | 30 | measured |
| 270 | Liverpool | 2.87 | 248,189 | 2 | 1 | - | - | 20 | measured |
| 271 | Nantes | 2.87 | 67,689 | 1 | 1 | - | - | 20 | measured |
| 272 | Kamakura | 1.76 | 33,492 | 6 | - | - | - | 20 | measured |
| 273 | Braga | 1.54 | 34,522 | 4 | 2 | - | 8 | 20 | measured |
| 274 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 275 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 276 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 277 | Salamanca | 1.76 | 47,897 | 4 | - | 1 | 1 | 20 | measured |
| 278 | Breda | 1.32 | 36,579 | 10 | - | 2 | 118 | 20 | measured |
| 279 | Hiroshima | 1.76 | 129,791 | 17 | 5 | 2 | - | 20 | measured |
| 280 | Lucca | 1.32 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 281 | Rotterdam | 1.32 | 104,938 | 12 | - | 2 | 83 | 20 | measured |
| 282 | Trieste | 1.32 | 117,233 | 20 | 1 | 3 | 44 | 20 | measured |
| 283 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 284 | Stuttgart | 1.98 | 112,789 | 6 | 1 | - | - | 20 | measured |
| 285 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 286 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 287 | Ghent | 2.42 | 82,757 | 8 | 1 | 1 | - | 20 | measured |
| 288 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 289 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 290 | Aarhus | 2.42 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 291 | Riga | 2.42 | 108,918 | 5 | 2 | - | - | 20 | measured |
| 292 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 293 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 294 | York | 2.42 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 295 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 296 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 297 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 298 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 299 | Naha | 1.54 | 24,466 | 6 | - | - | 1 | 20 | measured |
| 300 | Bilbao | 1.54 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 301 | Bratislava | 1.54 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 302 | Brno | 1.54 | 63,714 | 8 | 5 | 2 | 34 | 20 | measured |
| 303 | Toulouse | 1.54 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 304 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 305 | Cardiff | 2.20 | - | 4 | - | 1 | - | 20 | measured |
| 306 | Pittsburgh | 2.20 | - | 4 | - | 1 | - | 20 | measured |
| 307 | Bergamo | 1.10 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 308 | Lausanne | 2.20 | 68,242 | 8 | 1 | 1 | - | 20 | measured |
| 309 | Roosendaal | 1.10 | - | 8 | - | 1 | 116 | 20 | measured |
| 310 | Tulsa | 2.20 | - | 1 | - | - | - | 20 | measured |
| 311 | Venlo | 1.10 | - | 7 | - | 1 | 144 | 20 | measured |
| 312 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 313 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 314 | Hallstatt | 1.76 | 47,271 | 5 | 1 | - | - | 20 | measured |
| 315 | Graz | 1.32 | 65,717 | 12 | 7 | 1 | 87 | 20 | measured |
| 316 | Thessaloniki | 1.98 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 317 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 318 | Buenos Aires | 1.76 | 333,331 | 4 | 2 | - | - | 30 | measured |
| 319 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 320 | Baltimore | 1.76 | - | 4 | - | - | - | 20 | measured |
| 321 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 322 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 323 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 324 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 325 | Zaragoza | 1.10 | 87,580 | 7 | - | 1 | - | 20 | measured |
| 326 | Frankfurt | 1.10 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 327 | Gdansk | 1.10 | 4,908 | 12 | 4 | 1 | 307 | 20 | measured |
| 328 | Sofia | 1.10 | 138,710 | 4 | - | - | - | 30 | measured |
| 329 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 330 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 331 | Freiburg | 1.54 | 92,752 | 7 | 2 | 1 | - | 20 | measured |
| 332 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 333 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 334 | Modena | 0.88 | 51,698 | 5 | 1 | 1 | 3 | 20 | measured |
| 335 | Auckland | 1.32 | 152,056 | 5 | 2 | - | - | 20 | measured |
| 336 | Busan | 1.32 | 94,737 | 2 | - | - | - | 20 | measured |
| 337 | Brighton | 1.32 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 338 | Kansas City | 1.32 | - | 4 | - | 1 | - | 30 | measured |
| 339 | Leuven | 1.32 | 40,645 | 4 | - | - | - | 20 | measured |
| 340 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 341 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 342 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 343 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 344 | Setubal | 0.66 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 345 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 346 | Ronda | 0.66 | 51,510 | 6 | 1 | - | 9 | 20 | measured |
| 347 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 348 | Manchester | 1.10 | 316,438 | 5 | - | - | - | 30 | measured |
| 349 | Assisi | 0.66 | 30,278 | 6 | 1 | 2 | 6 | 20 | measured |
| 350 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 351 | Sao Paulo | 0.99 | 911 | 1 | - | - | - | 20 | measured |
| 352 | Poznan | 0.66 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 353 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 354 | Rothenburg ob der Tauber | 0.66 | 39,879 | 4 | - | 1 | 8 | 20 | measured |
| 355 | Bruges | 0.66 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 356 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 357 | Rouen | 0.54 | 72,334 | 12 | - | 1 | 6 | 10 | published, never ranked (may be uncrawled) |
| 358 | Phoenix | 0.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 359 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 360 | Bucharest | 0.44 | 136,836 | 4 | - | 1 | - | 20 | measured |
| 361 | Canberra | 0.44 | - | 1 | 1 | - | - | 30 | measured |
| 362 | Tarragona | 0.22 | 32,396 | 4 | 2 | - | - | 20 | measured |
| 363 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 364 | Cesky Krumlov | 0.22 | 28,582 | 6 | 3 | - | 11 | 20 | measured |
| 365 | Wroclaw | 0.22 | 123,894 | 5 | 1 | 1 | 121 | 20 | measured |
| 366 | Bamberg | 0.24 | 28,716 | 5 | 4 | 1 | 10 | 10 | published, never ranked (may be uncrawled) |
| 367 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 368 | George Town | 0.28 | 36,080 | - | - | - | - | 10 | predicted (travel demand) |
| 369 | Allentown | 0.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 370 | Antwerp | 0.22 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 371 | Gothenburg | 0.22 | 119,991 | 5 | - | 1 | - | 20 | measured |
| 372 | Oss | 0.11 | - | 6 | - | - | 48 | 10 | published, never ranked (may be uncrawled) |
| 373 | Turku | 0.22 | - | 1 | - | - | - | 30 | measured |
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

