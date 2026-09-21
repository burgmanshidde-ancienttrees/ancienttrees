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
| 1 | Brussels | 119.63 | 176,863 | 35 | 4 | 2 | 436 | 30 | measured |
| 2 | Pamplona | 97.07 | 128,065 | 14 | - | 1 | 9 | 20 | measured |
| 3 | Oahu | 94.04 | - | 21 | 2 | 3 | 163 | 20 | measured |
| 4 | Lisbon | 61.43 | 201,877 | 36 | 16 | 3 | 67 | 30 | measured |
| 5 | Amsterdam | 54.98 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 6 | Barcelona | 54.03 | 346,477 | 56 | 14 | 7 | 180 | 30 | measured |
| 7 | Arnhem | 44.36 | 31,478 | 39 | 3 | 3 | 204 | 20 | measured |
| 8 | Palermo | 43.60 | 124,310 | 21 | 9 | 1 | 37 | 20 | measured |
| 9 | Rome | 43.23 | 358,876 | 31 | 10 | 2 | 32 | 30 | measured |
| 10 | Milan | 43.04 | 212,705 | 30 | 14 | 3 | 25 | 30 | measured |
| 11 | Singapore | 56.12 | 967,821 | 34 | 6 | 3 | 165 | 30 | measured |
| 12 | Tenerife | 54.60 | - | 4 | 4 | - | - | 20 | measured |
| 13 | Tokyo | 43.42 | 394,702 | 22 | 10 | 1 | 5 | 20 | measured |
| 14 | Berlin | 51.57 | 412,181 | 33 | 23 | 3 | 195 | 30 | measured |
| 15 | Alicante | 33.56 | 77,454 | 21 | 4 | 2 | 44 | 20 | measured |
| 16 | Seville | 42.66 | 170,545 | 43 | 9 | 2 | - | 20 | measured |
| 17 | Prague | 42.85 | 303,350 | 30 | 21 | 4 | 31 | 30 | measured |
| 18 | Florence | 29.58 | 184,099 | 27 | 9 | 1 | 27 | 30 | measured |
| 19 | Portland | 36.78 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 20 | Vienna | 35.45 | 283,090 | 32 | 18 | 5 | 376 | 30 | measured |
| 21 | New York | 43.60 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 22 | Valencia | 24.27 | 162,209 | 31 | 4 | 2 | 350 | 30 | measured |
| 23 | Brisbane | 32.23 | 162,602 | 20 | 2 | 2 | 186 | 30 | measured |
| 24 | Paris | 31.85 | 524,268 | 31 | 9 | 4 | 129 | 30 | measured |
| 25 | Bath | 47.21 | 144,950 | 5 | 2 | 1 | - | 20 | measured |
| 26 | Austin | 45.88 | 226,631 | 5 | 2 | - | - | 20 | measured |
| 27 | Malaga | 30.33 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 28 | Los Angeles | 43.23 | 665,559 | 8 | 2 | - | - | 30 | measured |
| 29 | Porto | 21.23 | 120,415 | 27 | 15 | 2 | 40 | 20 | measured |
| 30 | Philadelphia | 39.81 | 405,294 | 1 | - | - | - | 20 | measured |
| 31 | Munich | 27.11 | 224,067 | 45 | 15 | 6 | 80 | 30 | measured |
| 32 | London | 32.80 | 718,291 | 23 | 14 | 1 | - | 30 | measured |
| 33 | Dublin | 22.18 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 34 | Utrecht | 18.77 | 67,963 | 27 | 7 | 2 | 340 | 20 | measured |
| 35 | Birmingham | 37.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 36 | Krakow | 23.51 | 140,824 | 38 | 8 | 3 | 198 | 30 | measured |
| 37 | Dallas | 32.99 | - | 9 | 1 | 1 | - | 30 | measured |
| 38 | The Hague | 15.36 | 236,723 | 31 | 2 | 5 | 167 | 20 | measured |
| 39 | Sintra | 15.17 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 40 | Cagliari | 15.93 | 51,351 | 14 | 1 | 2 | 15 | 20 | measured |
| 41 | Boston | 26.92 | 385,902 | 11 | 2 | 1 | - | 30 | measured |
| 42 | Monterey | 27.68 | - | 3 | 1 | - | - | 20 | measured |
| 43 | New Orleans | 27.68 | 256,232 | 4 | 2 | 1 | - | 20 | measured |
| 44 | Venice | 15.17 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 45 | Copenhagen | 24.46 | 218,621 | 16 | 2 | 2 | - | 30 | measured |
| 46 | Cork | 17.25 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 47 | Houston | 25.40 | - | 6 | - | - | - | 30 | measured |
| 48 | Edinburgh | 24.65 | 292,981 | 16 | 5 | 1 | - | 30 | measured |
| 49 | Leiden | 12.51 | 33,227 | 20 | 6 | 1 | 129 | 20 | measured |
| 50 | Cadiz | 15.93 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 51 | Kyoto | 15.93 | 142,353 | 18 | 12 | 2 | - | 20 | measured |
| 52 | Haarlem | 12.32 | 33,960 | 21 | 1 | 2 | 277 | 20 | measured |
| 53 | Las Vegas | 23.51 | - | 11 | - | 2 | - | 30 | measured |
| 54 | Fukuoka | 15.17 | 77,485 | 15 | 9 | 1 | - | 20 | measured |
| 55 | Glasgow | 21.80 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 56 | Jacksonville | 22.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 57 | Palma de Mallorca | 12.89 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 58 | Asheville | 20.89 | - | - | - | - | - | 10 | predicted (travel demand) |
| 59 | Nijmegen | 10.43 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 60 | Long Beach | 20.48 | - | - | - | - | - | 10 | predicted (travel demand) |
| 61 | Ottawa | 13.65 | - | 21 | - | 3 | 122 | 20 | measured |
| 62 | Vilnius | 13.65 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 63 | Little Rock | 20.40 | - | - | - | - | - | 10 | predicted (travel demand) |
| 64 | Reykjavik | 17.44 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 65 | Geneva | 13.08 | 162,269 | 21 | 5 | 4 | 131 | 20 | measured |
| 66 | Coimbra | 10.43 | 34,962 | 4 | - | - | 5 | 20 | measured |
| 67 | Athens | 18.77 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 68 | Oakland | 18.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 69 | Lexington | 18.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 70 | Chicago | 18.20 | 485,769 | 6 | - | - | - | 30 | measured |
| 71 | Reno | 18.19 | - | - | - | - | - | 10 | predicted (travel demand) |
| 72 | Des Moines | 18.11 | - | - | - | - | - | 10 | predicted (travel demand) |
| 73 | Madrid | 11.00 | 274,553 | 17 | 11 | 2 | - | 20 | measured |
| 74 | Daytona Beach | 17.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 75 | San Francisco | 17.06 | 361,111 | 6 | 1 | 1 | - | 30 | measured |
| 76 | Tilburg | 8.53 | - | 20 | - | 3 | 87 | 20 | measured |
| 77 | Madeira | 10.24 | - | 10 | 1 | 1 | - | 20 | measured |
| 78 | Sardinia | 9.29 | - | 5 | 4 | - | 8 | 20 | measured |
| 79 | Chattanooga | 16.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 80 | Helmond | 8.15 | - | 20 | - | 2 | 54 | 20 | measured |
| 81 | Santa Cruz | 16.06 | - | - | - | - | - | 10 | predicted (travel demand) |
| 82 | Parma | 8.91 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 83 | Washington DC | 14.41 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 84 | Key West | 15.81 | - | - | - | - | - | 10 | predicted (travel demand) |
| 85 | Seattle | 14.79 | 398,724 | 6 | 1 | - | - | 30 | measured |
| 86 | Huntsville | 15.35 | - | - | - | - | - | 10 | predicted (travel demand) |
| 87 | Saratoga Springs | 15.05 | - | - | - | - | - | 10 | predicted (travel demand) |
| 88 | Granada | 9.48 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 89 | West Palm Beach | 14.98 | - | - | - | - | - | 10 | predicted (travel demand) |
| 90 | Saint Petersburg | 14.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 91 | St. Louis | 14.80 | - | - | - | - | - | 10 | predicted (travel demand) |
| 92 | Melbourne | 9.67 | 267,898 | 16 | - | 2 | 403 | 30 | measured |
| 93 | Warsaw | 9.48 | 197,929 | 39 | 5 | 4 | 1407 | 30 | measured |
| 94 | Osaka | 9.10 | 163,112 | 6 | 1 | - | - | 30 | measured |
| 95 | Tampa | 14.10 | - | - | - | - | - | 10 | predicted (travel demand) |
| 96 | Eindhoven | 7.01 | - | 21 | - | 4 | 195 | 20 | measured |
| 97 | Cincinnati | 13.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 98 | Lansing | 13.02 | - | - | - | - | - | 10 | predicted (travel demand) |
| 99 | Detroit | 12.53 | - | - | - | - | - | 10 | predicted (travel demand) |
| 100 | Denver | 11.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 101 | Bari | 6.83 | 86,456 | 5 | 1 | - | 8 | 30 | measured |
| 102 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 103 | San Jose | 11.39 | - | - | - | - | - | 10 | predicted (travel demand) |
| 104 | Groningen | 5.69 | 31,401 | 21 | 1 | 2 | 76 | 20 | measured |
| 105 | Bordeaux | 7.58 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 106 | Strasbourg | 7.58 | 154,700 | 10 | 2 | 2 | 66 | 30 | measured |
| 107 | Sacramento | 11.32 | - | - | - | - | - | 10 | predicted (travel demand) |
| 108 | Jersey City | 10.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 109 | Crete | 11.19 | - | 4 | 3 | - | - | 20 | measured |
| 110 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 111 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 112 | Dordrecht | 5.50 | - | 20 | 1 | 2 | 105 | 20 | measured |
| 113 | Zurich | 10.24 | 140,788 | 6 | 1 | - | - | 20 | measured |
| 114 | Milwaukee | 10.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 115 | Amersfoort | 5.31 | - | 18 | 1 | 2 | 181 | 20 | measured |
| 116 | Cambridge | 10.62 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 117 | Hoorn | 5.31 | - | 12 | - | 2 | 52 | 20 | measured |
| 118 | Ibiza | 6.64 | - | 1 | - | - | 4 | 20 | measured |
| 119 | Yakushima | 6.64 | - | 2 | - | - | 1 | 20 | measured |
| 120 | Salt Lake City | 10.31 | - | - | - | - | - | 10 | predicted (travel demand) |
| 121 | Atlanta | 10.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 122 | Anchorage | 10.25 | - | - | - | - | - | 10 | predicted (travel demand) |
| 123 | Budapest | 9.86 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 124 | Hobart | 6.83 | 81,734 | 11 | 1 | 2 | 455 | 20 | measured |
| 125 | Leipzig | 6.83 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 126 | Caserta | 5.12 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 127 | Oslo | 8.91 | 181,113 | 4 | - | - | - | 20 | measured |
| 128 | Raleigh | 10.07 | - | - | - | - | - | 10 | predicted (travel demand) |
| 129 | Segovia | 6.26 | 30,968 | 6 | - | 1 | 5 | 20 | measured |
| 130 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 131 | Naples | 4.93 | 198,913 | 24 | 3 | 3 | 46 | 20 | measured |
| 132 | Cleveland | 9.76 | - | - | - | - | - | 10 | predicted (travel demand) |
| 133 | El Paso | 9.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 134 | Montreal | 9.67 | 315,322 | 13 | 1 | 2 | - | 30 | measured |
| 135 | Nice | 9.67 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 136 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 137 | Enschede | 4.74 | - | 15 | 1 | 2 | 82 | 20 | measured |
| 138 | Miami | 9.48 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 139 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 140 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 141 | Sorrento | 4.55 | 40,049 | 7 | - | 1 | 20 | 20 | measured |
| 142 | Nashville | 8.93 | - | - | - | - | - | 10 | predicted (travel demand) |
| 143 | Cyprus | 8.72 | - | 4 | - | - | - | 20 | measured |
| 144 | Tallinn | 5.88 | 124,888 | 9 | 3 | 2 | 42 | 20 | measured |
| 145 | Seoul | 8.15 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 146 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 147 | Sydney | 8.53 | 305,304 | 7 | 1 | - | - | 30 | measured |
| 148 | Istanbul | 7.58 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 149 | Ann Arbor | 8.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 150 | Kanazawa | 5.50 | 25,778 | 7 | 2 | 1 | 2 | 20 | measured |
| 151 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 152 | Leuven | 8.15 | 40,645 | 4 | - | - | - | 20 | measured |
| 153 | Luxembourg City | 5.31 | 64,851 | 10 | 5 | 2 | 18 | 20 | measured |
| 154 | Lyon | 5.31 | 136,951 | 13 | 4 | 1 | 156 | 20 | measured |
| 155 | Stockholm | 6.26 | 188,184 | 6 | 4 | - | - | 30 | measured |
| 156 | Albuquerque | 7.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 157 | Pittsburgh | 7.58 | - | 4 | - | 1 | - | 20 | measured |
| 158 | Potsdam | 5.12 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 159 | Leeuwarden | 3.79 | - | 41 | - | 2 | 61 | 20 | measured |
| 160 | Savannah | 7.58 | 128,162 | 2 | 1 | - | - | 20 | measured |
| 161 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 162 | Padua | 3.98 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 163 | Spokane | 5.31 | - | 13 | - | 2 | 18 | 20 | measured |
| 164 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 165 | Menorca | 4.74 | - | 6 | - | - | 2 | 20 | measured |
| 166 | Hong Kong | 4.83 | 689,212 | 10 | 4 | 1 | 505 | 20 | measured |
| 167 | Genoa | 3.98 | 145,206 | 13 | 2 | 1 | 10 | 20 | measured |
| 168 | Maastricht | 3.60 | 47,763 | 19 | - | 2 | 135 | 20 | measured |
| 169 | Helsinki | 5.69 | 148,908 | 12 | 2 | 1 | 13 | 30 | measured |
| 170 | Ljubljana | 7.01 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 171 | Perth | 7.01 | 180,478 | 6 | 3 | 1 | - | 30 | measured |
| 172 | Catania | 4.17 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 173 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 174 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 175 | Sapporo | 4.55 | 88,633 | 6 | - | - | - | 20 | measured |
| 176 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 177 | Bristol | 6.64 | 163,983 | 6 | 2 | - | - | 20 | measured |
| 178 | Guimaraes | 3.41 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 179 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 180 | Beijing | 6.54 | 269,737 | 7 | 1 | - | - | 30 | measured |
| 181 | Girona | 3.79 | 51,072 | 7 | 3 | - | - | 20 | measured |
| 182 | Dubrovnik | 6.07 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 183 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 184 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 185 | Hawaii | 5.69 | - | 6 | - | 1 | 6 | 30 | measured |
| 186 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 187 | Charleston | 6.07 | 155,987 | 2 | 1 | - | - | 20 | measured |
| 188 | Vancouver | 6.07 | 351,552 | 7 | - | - | - | 30 | measured |
| 189 | Minneapolis | 6.07 | - | 4 | - | - | - | 20 | measured |
| 190 | Turin | 3.03 | 147,456 | 11 | 7 | 2 | 30 | 20 | measured |
| 191 | Perugia | 3.22 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 192 | Quebec City | 3.98 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 193 | Salzburg | 3.98 | 107,243 | 9 | 3 | 2 | 34 | 20 | measured |
| 194 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 195 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 196 | Bangkok | 5.69 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 197 | Boise | 5.69 | - | 4 | - | 1 | - | 30 | measured |
| 198 | Den Bosch | 2.84 | 39,682 | 12 | 2 | 1 | 118 | 20 | measured |
| 199 | Bologna | 3.03 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 200 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 201 | Pisa | 3.60 | 52,174 | 4 | - | - | - | 20 | measured |
| 202 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 203 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 204 | Verona | 3.22 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 205 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 206 | San Diego | 5.31 | 214,939 | 4 | 1 | 1 | - | 20 | measured |
| 207 | Zwolle | 2.65 | - | 16 | - | 2 | 56 | 20 | measured |
| 208 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 209 | Santa Fe | 5.17 | - | - | - | - | - | 10 | predicted (travel demand) |
| 210 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 211 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 212 | Indianapolis | 4.93 | - | 1 | - | - | - | 30 | measured |
| 213 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 214 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 215 | Como | 2.46 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 216 | Naha | 3.22 | 24,466 | 6 | - | - | 1 | 20 | measured |
| 217 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 218 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 219 | Alkmaar | 2.28 | - | 14 | - | 2 | 79 | 20 | measured |
| 220 | Split | 4.55 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 221 | Dresden | 3.03 | 113,624 | 5 | 5 | 1 | - | 20 | measured |
| 222 | Nuremberg | 3.03 | 161,614 | 12 | 1 | 1 | 38 | 20 | measured |
| 223 | Cordoba | 2.84 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 224 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 225 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 226 | Salamanca | 2.84 | 47,897 | 4 | - | 1 | 1 | 20 | measured |
| 227 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 228 | Hilversum | 2.09 | - | 6 | 1 | 1 | 122 | 20 | measured |
| 229 | Liverpool | 4.17 | 248,189 | 2 | 1 | - | - | 20 | measured |
| 230 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 231 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 232 | Kauai | 3.41 | - | 6 | 1 | - | 8 | 20 | measured |
| 233 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 234 | Fort Lauderdale | 3.79 | - | 4 | - | - | - | 30 | measured |
| 235 | Oxford | 3.79 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 236 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 237 | Matera | 2.28 | 67,033 | 4 | - | - | 2 | 20 | measured |
| 238 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 239 | Bergamo | 1.90 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 240 | Heerlen | 1.90 | - | 8 | 1 | 2 | 53 | 20 | measured |
| 241 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 242 | Toronto | 3.60 | 411,011 | 6 | - | - | - | 30 | measured |
| 243 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 244 | Heidelberg | 3.22 | 75,837 | 6 | 1 | 1 | - | 20 | measured |
| 245 | Nantes | 3.60 | 67,689 | 1 | 1 | - | - | 20 | measured |
| 246 | York | 3.60 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 247 | Hilo | 2.65 | - | 6 | - | 1 | 16 | 20 | measured |
| 248 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 249 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 250 | Bratislava | 2.28 | 132,162 | 7 | 1 | 1 | 26 | 30 | measured |
| 251 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 252 | Delft | 1.71 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 253 | Deventer | 1.71 | - | 12 | - | 1 | 213 | 20 | measured |
| 254 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 255 | Cologne | 3.41 | 191,812 | 5 | - | 1 | - | 30 | measured |
| 256 | Tulsa | 3.41 | - | 1 | - | - | - | 20 | measured |
| 257 | San Antonio | 3.32 | - | 4 | 1 | - | - | 10 | published, never ranked (may be uncrawled) |
| 258 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 259 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 260 | Belgrade | 3.22 | 178,116 | 5 | 5 | - | - | 20 | measured |
| 261 | Taipei | 3.22 | 143,193 | 4 | 1 | - | - | 30 | measured |
| 262 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 263 | Toulouse | 2.09 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 264 | Braga | 1.71 | 34,522 | 4 | 2 | - | 8 | 20 | measured |
| 265 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 266 | Cardiff | 3.03 | - | 4 | - | 1 | - | 20 | measured |
| 267 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 268 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 269 | Trento | 1.52 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 270 | Stuttgart | 2.28 | 112,789 | 6 | 1 | - | - | 20 | measured |
| 271 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 272 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 273 | Ferrara | 1.71 | 27,490 | 5 | 3 | 1 | 7 | 20 | measured |
| 274 | Regensburg | 2.65 | 51,930 | 5 | 1 | 1 | 4 | 20 | measured |
| 275 | Lausanne | 2.84 | 68,242 | 8 | 1 | 1 | - | 20 | measured |
| 276 | Mexico City | 2.65 | 566,583 | 9 | 2 | - | - | 30 | measured |
| 277 | Hallstatt | 2.46 | 47,271 | 5 | 1 | - | - | 20 | measured |
| 278 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 279 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 280 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 281 | Apeldoorn | 1.33 | - | 10 | - | 2 | 80 | 20 | measured |
| 282 | Rotterdam | 1.33 | 104,938 | 12 | - | 2 | 83 | 20 | measured |
| 283 | Trieste | 1.33 | 117,233 | 20 | 1 | 3 | 44 | 20 | measured |
| 284 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 285 | Hamburg | 2.46 | 191,221 | 6 | 1 | 1 | - | 30 | measured |
| 286 | Nagoya | 1.71 | 83,437 | 6 | 1 | - | 1 | 20 | measured |
| 287 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 288 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 289 | Ghent | 2.46 | 82,757 | 8 | 1 | 1 | - | 20 | measured |
| 290 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 291 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 292 | Belfast | 2.46 | 224,315 | 4 | - | 1 | - | 20 | measured |
| 293 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 294 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 295 | Maui | 2.28 | - | 4 | - | - | 3 | 20 | measured |
| 296 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 297 | Freiburg | 2.28 | 92,752 | 7 | 2 | 1 | - | 20 | measured |
| 298 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 299 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 300 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 301 | Riga | 2.28 | 108,918 | 5 | 2 | - | - | 20 | measured |
| 302 | Assen | 1.14 | - | 10 | - | 2 | 66 | 20 | measured |
| 303 | Gdansk | 1.52 | 4,908 | 12 | 4 | 1 | 307 | 20 | measured |
| 304 | Graz | 1.52 | 65,717 | 12 | 7 | 1 | 87 | 20 | measured |
| 305 | Manchester | 2.28 | 316,438 | 5 | - | - | - | 30 | measured |
| 306 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 307 | Rio de Janeiro | 2.18 | 279,431 | 6 | - | - | - | 30 | measured |
| 308 | Thessaloniki | 2.09 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 309 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 310 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 311 | Bilbao | 1.33 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 312 | Frankfurt | 1.33 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 313 | Sao Paulo | 1.90 | 911 | 1 | - | - | - | 20 | measured |
| 314 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 315 | Baltimore | 1.90 | - | 4 | - | - | - | 20 | measured |
| 316 | Kansas City | 1.90 | - | 4 | - | 1 | - | 30 | measured |
| 317 | Lucca | 0.95 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 318 | Roosendaal | 0.95 | - | 8 | - | 1 | 116 | 20 | measured |
| 319 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 320 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 321 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 322 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 323 | Hiroshima | 1.14 | 129,791 | 33 | 5 | 2 | - | 20 | measured |
| 324 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 325 | Buenos Aires | 1.61 | 333,331 | 4 | 2 | - | - | 30 | measured |
| 326 | Middletown | 1.64 | - | - | - | - | - | 10 | predicted (travel demand) |
| 327 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 328 | Modena | 0.95 | 51,698 | 5 | 1 | 1 | 3 | 20 | measured |
| 329 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 330 | Aarhus | 1.52 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 331 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 332 | Breda | 0.76 | 36,579 | 10 | - | 2 | 118 | 20 | measured |
| 333 | Brno | 0.95 | 63,714 | 8 | 5 | 2 | 34 | 20 | measured |
| 334 | Sofia | 0.95 | 138,710 | 4 | - | - | - | 30 | measured |
| 335 | Setubal | 0.76 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 336 | Brighton | 1.33 | 114,108 | 6 | 1 | 1 | - | 20 | measured |
| 337 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 338 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 339 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 340 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 341 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 342 | Auckland | 1.14 | 152,056 | 5 | 2 | - | - | 20 | measured |
| 343 | Busan | 1.14 | 94,737 | 2 | - | - | - | 20 | measured |
| 344 | Rothenburg ob der Tauber | 0.95 | 39,879 | 4 | - | 1 | 8 | 20 | measured |
| 345 | Wroclaw | 0.76 | 123,894 | 5 | 1 | 1 | 121 | 20 | measured |
| 346 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 347 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 348 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 349 | Tarragona | 0.57 | 32,396 | 4 | 2 | - | - | 20 | measured |
| 350 | Canberra | 0.95 | - | 1 | 1 | - | - | 30 | measured |
| 351 | Venlo | 0.38 | - | 7 | - | 1 | 144 | 20 | measured |
| 352 | Ronda | 0.38 | 51,510 | 6 | 1 | - | 9 | 20 | measured |
| 353 | Rouen | 0.57 | 72,334 | 12 | - | 1 | 6 | 20 | measured |
| 354 | Assisi | 0.38 | 30,278 | 6 | 1 | 2 | 6 | 20 | measured |
| 355 | Kamakura | 0.38 | 33,492 | 6 | - | - | - | 20 | measured |
| 356 | Lima | 0.51 | 132,792 | 5 | 1 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 357 | Zaragoza | 0.38 | 87,580 | 7 | - | 1 | - | 20 | measured |
| 358 | Bruges | 0.57 | 106,902 | 4 | - | 1 | - | 20 | measured |
| 359 | Phoenix | 0.55 | - | - | - | - | - | 10 | predicted (travel demand) |
| 360 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 361 | Bucharest | 0.38 | 136,836 | 4 | - | 1 | - | 20 | measured |
| 362 | Fort Worth | 0.38 | - | 4 | - | - | - | 20 | measured |
| 363 | Gothenburg | 0.38 | 119,991 | 5 | - | 1 | - | 20 | measured |
| 364 | Turku | 0.38 | - | 1 | - | - | - | 30 | measured |
| 365 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 366 | Cesky Krumlov | 0.19 | 28,582 | 6 | 3 | - | 11 | 20 | measured |
| 367 | Newark | 0.29 | - | - | - | - | - | 10 | predicted (travel demand) |
| 368 | Poznan | 0.19 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 369 | George Town | 0.28 | 36,080 | - | - | - | - | 10 | predicted (travel demand) |
| 370 | Allentown | 0.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 371 | Bamberg | 0.19 | 28,716 | 5 | 4 | 1 | 10 | 20 | measured |
| 372 | Oss | 0.11 | - | 6 | - | - | 48 | 10 | published, never ranked (may be uncrawled) |
| 373 | Antwerp | 0.19 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
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

