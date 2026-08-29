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
| 1 | Rome | 82.20 | 358,876 | 30 | 9 | 2 | 32 | 30 | measured |
| 2 | Amsterdam | 79.46 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 3 | Milan | 47.21 | 212,705 | 22 | 9 | 2 | 25 | 30 | measured |
| 4 | Lisbon | 45.32 | 201,877 | 33 | 10 | 3 | 66 | 30 | measured |
| 5 | Barcelona | 38.99 | 346,477 | 56 | 12 | 7 | 180 | 30 | measured |
| 6 | Tenerife | 51.22 | - | 4 | - | - | - | 20 | measured |
| 7 | Singapore | 39.62 | 967,821 | 18 | 3 | 2 | 165 | 30 | measured |
| 8 | Brisbane | 39.41 | 162,602 | 19 | 1 | 2 | 189 | 30 | measured |
| 9 | Florence | 26.35 | 184,099 | 23 | 7 | 1 | 27 | 30 | measured |
| 10 | Seville | 33.72 | 170,545 | 43 | 6 | 2 | - | 20 | measured |
| 11 | Prague | 32.67 | 303,350 | 17 | 13 | 3 | 29 | 30 | measured |
| 12 | Naples | 24.45 | 198,913 | 23 | 3 | 3 | 46 | 20 | measured |
| 13 | Vienna | 32.04 | 283,090 | 30 | 13 | 5 | 376 | 30 | measured |
| 14 | Malaga | 31.19 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 15 | Copenhagen | 43.42 | 218,621 | 16 | 1 | 2 | - | 30 | measured |
| 16 | Palermo | 22.55 | 124,310 | 21 | 7 | 1 | 37 | 20 | measured |
| 17 | Paris | 29.72 | 524,268 | 31 | 9 | 4 | 129 | 30 | measured |
| 18 | Madrid | 26.98 | 274,553 | 17 | 10 | 2 | - | 20 | measured |
| 19 | Madeira | 24.45 | - | 6 | 1 | - | - | 20 | measured |
| 20 | London | 32.25 | 718,291 | 23 | 10 | 1 | - | 30 | measured |
| 21 | Bath | 36.88 | 144,950 | 5 | 1 | 1 | - | 20 | measured |
| 22 | Venice | 18.13 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 23 | Palma de Mallorca | 18.13 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 24 | Brussels | 20.02 | 176,863 | 30 | 4 | 1 | 436 | 30 | measured |
| 25 | Valencia | 14.33 | 162,209 | 15 | 2 | 2 | 350 | 30 | measured |
| 26 | Sardinia | 14.54 | - | 5 | 2 | - | 8 | 20 | measured |
| 27 | Nijmegen | 12.65 | 42,338 | 20 | 1 | 2 | 159 | 20 | measured |
| 28 | Fukuoka | 16.02 | 77,485 | 13 | 7 | 1 | - | 20 | measured |
| 29 | Dublin | 13.70 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 30 | Crete | 22.76 | - | 4 | - | - | - | 20 | measured |
| 31 | Seoul | 20.87 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 32 | Bologna | 10.96 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 33 | Alicante | 10.12 | 77,454 | 14 | 2 | 2 | 44 | 20 | measured |
| 34 | Krakow | 12.44 | 140,824 | 26 | 3 | 3 | 200 | 30 | measured |
| 35 | The Hague | 8.85 | 236,723 | 29 | 1 | 5 | 166 | 20 | measured |
| 36 | Toronto | 17.28 | 411,011 | 6 | - | - | - | 30 | measured |
| 37 | Montreal | 17.49 | 315,322 | 7 | - | 1 | - | 30 | measured |
| 38 | Leiden | 8.64 | 33,227 | 12 | 4 | 1 | 129 | 20 | measured |
| 39 | Edinburgh | 16.86 | 292,981 | 15 | 4 | 1 | - | 30 | measured |
| 40 | New York | 14.96 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 41 | Porto | 8.22 | 120,415 | 27 | 5 | 2 | 40 | 20 | measured |
| 42 | Portland | 10.33 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 43 | Geneva | 10.12 | 162,269 | 21 | 4 | 4 | 131 | 20 | measured |
| 44 | Groningen | 7.59 | 31,401 | 20 | - | 2 | 72 | 20 | measured |
| 45 | Las Vegas | 14.96 | - | 11 | - | 2 | - | 30 | measured |
| 46 | Reykjavik | 12.86 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 47 | Kyoto | 9.27 | 142,353 | 17 | 8 | 2 | - | 20 | measured |
| 48 | Tokyo | 7.38 | 394,702 | 10 | 8 | - | 7 | 20 | measured |
| 49 | Girona | 7.87 | 51,072 | - | - | - | - | 10 | predicted (travel demand) |
| 50 | Cagliari | 6.96 | 51,351 | 9 | 1 | 2 | 15 | 20 | measured |
| 51 | Bordeaux | 8.43 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 52 | Vilnius | 8.22 | 113,188 | 10 | 1 | 1 | 34 | 30 | measured |
| 53 | Berlin | 7.80 | 412,181 | 19 | 11 | 1 | 195 | 30 | measured |
| 54 | Munich | 7.80 | 224,067 | 45 | 14 | 6 | 80 | 30 | measured |
| 55 | Padua | 6.11 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 56 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 57 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 58 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 59 | Sintra | 5.48 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 60 | Trieste | 5.48 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 61 | Hamburg | 10.27 | 191,221 | - | - | - | - | 10 | predicted (travel demand) |
| 62 | Cambridge | 10.54 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 63 | Utrecht | 5.27 | 67,963 | 33 | 4 | 2 | 345 | 20 | measured |
| 64 | Guimaraes | 5.48 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 65 | Kansas City | 10.51 | - | - | - | - | - | 10 | predicted (travel demand) |
| 66 | Asheville | 10.45 | - | - | - | - | - | 10 | predicted (travel demand) |
| 67 | Dubrovnik | 9.70 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 68 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 69 | Oslo | 8.64 | 181,113 | 4 | - | - | - | 20 | measured |
| 70 | Sorrento | 4.85 | 40,049 | 6 | - | 1 | 20 | 20 | measured |
| 71 | Vancouver | 9.47 | 351,552 | - | - | - | - | 10 | predicted (travel demand) |
| 72 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 73 | Bratislava | 6.32 | 132,162 | 6 | - | 1 | 26 | 30 | measured |
| 74 | Turku | 9.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 75 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 76 | Athens | 9.06 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 77 | Perth | 9.06 | 180,478 | 6 | 1 | 1 | - | 30 | measured |
| 78 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 79 | Canberra | 9.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 80 | Manchester | 9.06 | 316,438 | - | - | - | - | 10 | predicted (travel demand) |
| 81 | Pisa | 5.85 | 52,174 | - | - | - | - | 10 | predicted (travel demand) |
| 82 | Boston | 8.64 | 385,902 | 10 | 1 | 1 | - | 30 | measured |
| 83 | Turin | 4.43 | 147,456 | 10 | 7 | 2 | 30 | 20 | measured |
| 84 | Potsdam | 5.90 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 85 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 86 | Chicago | 8.64 | 485,769 | 6 | - | - | - | 30 | measured |
| 87 | Cyprus | 8.43 | - | 4 | - | - | - | 20 | measured |
| 88 | Lyon | 5.69 | 136,951 | 13 | 3 | 1 | 156 | 20 | measured |
| 89 | Hiroshima | 5.55 | 129,791 | - | - | - | - | 10 | predicted (travel demand) |
| 90 | Taipei | 8.38 | 143,193 | - | - | - | - | 10 | predicted (travel demand) |
| 91 | Salamanca | 5.50 | 47,897 | - | - | - | 1 | 10 | predicted (travel demand) |
| 92 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 93 | San Francisco | 8.08 | 361,111 | - | - | - | - | 10 | predicted (travel demand) |
| 94 | Cordoba | 5.27 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 95 | Bristol | 8.01 | 163,983 | 5 | 1 | - | - | 20 | measured |
| 96 | Sydney | 8.01 | 305,304 | 6 | - | - | - | 30 | measured |
| 97 | Washington DC | 7.38 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 98 | Cork | 5.27 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 99 | Quebec City | 5.27 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 100 | Strasbourg | 5.06 | 154,700 | 10 | 1 | 2 | 66 | 30 | measured |
| 101 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 102 | Kauai | 7.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 103 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 104 | Tallinn | 4.85 | 124,888 | 4 | 2 | 1 | 42 | 20 | measured |
| 105 | Budapest | 6.96 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 106 | Seattle | 6.74 | 398,724 | 6 | - | - | - | 30 | measured |
| 107 | Warsaw | 4.64 | 197,929 | 16 | 3 | 2 | 1430 | 30 | measured |
| 108 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 109 | Helsinki | 5.69 | 148,908 | 8 | 1 | - | 9 | 30 | measured |
| 110 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 111 | Cadiz | 4.43 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 112 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 113 | Arnhem | 3.37 | 31,478 | 9 | 1 | 1 | 196 | 20 | measured |
| 114 | Liverpool | 6.46 | 248,189 | - | - | - | - | 10 | predicted (travel demand) |
| 115 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 116 | Freiburg | 6.18 | 92,752 | - | - | - | - | 10 | predicted (travel demand) |
| 117 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 118 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 119 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 120 | Rio de Janeiro | 6.36 | 279,431 | - | - | - | - | 10 | predicted (travel demand) |
| 121 | Caserta | 3.16 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 122 | Lucca | 3.16 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 123 | Maastricht | 3.16 | 47,763 | 14 | - | 1 | 137 | 20 | measured |
| 124 | Detroit | 6.26 | - | - | - | - | - | 10 | predicted (travel demand) |
| 125 | Aarhus | 5.90 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 126 | Nuremberg | 4.00 | 161,614 | 10 | 1 | 1 | 39 | 20 | measured |
| 127 | Gothenburg | 5.95 | 119,991 | - | - | - | - | 10 | predicted (travel demand) |
| 128 | Beijing | 5.73 | 269,737 | - | - | - | - | 10 | predicted (travel demand) |
| 129 | Denver | 5.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 130 | Glasgow | 5.48 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 131 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 132 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 133 | Graz | 3.79 | 65,717 | 10 | 3 | 1 | 87 | 20 | measured |
| 134 | Toulouse | 3.79 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 135 | Sacramento | 5.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 136 | Bruges | 5.60 | 106,902 | - | - | - | - | 10 | predicted (travel demand) |
| 137 | Philadelphia | 5.34 | 405,294 | - | - | - | - | 10 | predicted (travel demand) |
| 138 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 139 | San Diego | 5.53 | 214,939 | - | - | - | - | 10 | predicted (travel demand) |
| 140 | Riga | 4.90 | 108,918 | - | - | - | - | 10 | predicted (travel demand) |
| 141 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 142 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 143 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 144 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 145 | Sapporo | 3.51 | 88,633 | - | - | - | - | 10 | predicted (travel demand) |
| 146 | Cardiff | 5.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 147 | Salt Lake City | 5.16 | - | - | - | - | - | 10 | predicted (travel demand) |
| 148 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 149 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 150 | Haarlem | 2.53 | 33,960 | 21 | - | 2 | 277 | 20 | measured |
| 151 | York | 5.06 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 152 | Auckland | 4.67 | 152,056 | - | - | - | - | 10 | predicted (travel demand) |
| 153 | Zurich | 4.85 | 140,788 | 4 | - | - | - | 20 | measured |
| 154 | Lausanne | 4.90 | 68,242 | - | - | - | - | 10 | predicted (travel demand) |
| 155 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 156 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 157 | Istanbul | 4.32 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 158 | Nagoya | 3.17 | 83,437 | - | - | - | 1 | 10 | predicted (travel demand) |
| 159 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 160 | Miami | 4.74 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 161 | Catania | 2.74 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 162 | Delft | 2.32 | 31,293 | 4 | - | 1 | 51 | 20 | measured |
| 163 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 164 | Stuttgart | 4.08 | 112,789 | - | - | - | - | 10 | predicted (travel demand) |
| 165 | Perugia | 2.32 | 42,572 | 10 | - | 2 | 19 | 20 | measured |
| 166 | Menorca | 2.93 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 167 | Mexico City | 4.22 | 566,583 | 9 | 1 | - | - | 30 | measured |
| 168 | New Orleans | 4.43 | 256,232 | 4 | - | 1 | - | 20 | measured |
| 169 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 170 | Naha | 2.84 | 24,466 | - | - | - | 1 | 10 | predicted (travel demand) |
| 171 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 172 | Verona | 2.53 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 173 | Braga | 2.32 | 34,522 | 4 | 1 | - | 8 | 20 | measured |
| 174 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 175 | Belfast | 4.15 | 224,315 | - | - | - | - | 10 | predicted (travel demand) |
| 176 | Poznan | 2.74 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 177 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 178 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 179 | Nice | 4.00 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 180 | Kanazawa | 2.53 | 25,778 | - | - | - | 2 | 10 | predicted (travel demand) |
| 181 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 182 | Setubal | 2.11 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 183 | Nantes | 3.83 | 67,689 | - | - | - | - | 10 | predicted (travel demand) |
| 184 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 185 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 186 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 187 | Rotterdam | 1.90 | 104,938 | 9 | - | 2 | 83 | 20 | measured |
| 188 | Oahu | 2.53 | - | 8 | - | - | 133 | 20 | measured |
| 189 | Los Angeles | 3.60 | 665,559 | 8 | 2 | - | - | 10 | published, never ranked (may be uncrawled) |
| 190 | Rothenburg ob der Tauber | 3.08 | 39,879 | - | - | - | 8 | 10 | predicted (travel demand) |
| 191 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 192 | Luxembourg City | 2.39 | 64,851 | - | - | - | - | 10 | predicted (travel demand) |
| 193 | Brighton | 3.40 | 114,108 | - | - | - | - | 10 | predicted (travel demand) |
| 194 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 195 | Busan | 3.31 | 94,737 | - | - | - | - | 10 | predicted (travel demand) |
| 196 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 197 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 198 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 199 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 200 | Segovia | 2.17 | 30,968 | - | - | - | 1 | 10 | predicted (travel demand) |
| 201 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 202 | Leipzig | 2.15 | 121,319 | 7 | 7 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 203 | Oxford | 3.16 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 204 | Bilbao | 2.11 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 205 | Brno | 2.11 | 63,714 | 8 | 2 | 2 | 34 | 20 | measured |
| 206 | Frankfurt | 2.11 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 207 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 208 | Sao Paulo | 2.96 | 911 | - | - | - | - | 10 | predicted (travel demand) |
| 209 | Savannah | 3.05 | 128,162 | - | - | - | - | 10 | predicted (travel demand) |
| 210 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 211 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 212 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 213 | Cologne | 3.04 | 191,812 | 5 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 214 | Heidelberg | 2.69 | 75,837 | - | - | - | - | 10 | predicted (travel demand) |
| 215 | Modena | 1.77 | 51,698 | - | - | - | 3 | 10 | predicted (travel demand) |
| 216 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 217 | Hong Kong | 2.00 | 689,212 | 10 | 2 | 1 | 505 | 20 | measured |
| 218 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 219 | Austin | 2.95 | 226,631 | 5 | - | - | - | 20 | measured |
| 220 | Ibiza | 1.85 | - | - | - | - | - | 10 | predicted (travel demand) |
| 221 | Kamakura | 1.74 | 33,492 | - | - | - | - | 10 | predicted (travel demand) |
| 222 | Coimbra | 1.44 | 34,962 | - | - | - | 5 | 10 | predicted (travel demand) |
| 223 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 224 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 225 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 226 | Zaragoza | 1.69 | 87,580 | 7 | - | 1 | - | 20 | measured |
| 227 | Ronda | 1.68 | 51,510 | - | - | - | 1 | 10 | predicted (travel demand) |
| 228 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 229 | Lima | 2.03 | 132,792 | - | - | - | - | 10 | predicted (travel demand) |
| 230 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 231 | Ljubljana | 2.53 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 232 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 233 | Ghent | 2.36 | 82,757 | - | - | - | - | 10 | predicted (travel demand) |
| 234 | Split | 2.53 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 235 | Bergamo | 1.26 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 236 | Como | 1.26 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 237 | Den Bosch | 1.26 | 39,682 | 11 | 1 | 1 | 119 | 20 | measured |
| 238 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 239 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 240 | Maui | 2.33 | - | - | - | - | 3 | 10 | predicted (travel demand) |
| 241 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 242 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 243 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 244 | Dresden | 1.60 | 113,624 | 5 | 1 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 245 | Tarragona | 1.45 | 32,396 | - | - | - | - | 10 | predicted (travel demand) |
| 246 | Genoa | 1.26 | 145,206 | 12 | 1 | 1 | 11 | 20 | measured |
| 247 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 248 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 249 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 250 | Osaka | 1.48 | 163,112 | 4 | 1 | - | - | 30 | measured |
| 251 | Hallstatt | 1.99 | 47,271 | - | - | - | - | 10 | predicted (travel demand) |
| 252 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 253 | Charleston | 2.21 | 155,987 | - | - | - | - | 10 | predicted (travel demand) |
| 254 | Rouen | 2.17 | 72,334 | - | - | - | 1 | 10 | predicted (travel demand) |
| 255 | Dallas | 2.11 | - | 8 | 1 | 1 | - | 30 | measured |
| 256 | Breda | 1.05 | 36,579 | 4 | - | 1 | 119 | 20 | measured |
| 257 | Trento | 1.05 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 258 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 259 | Leuven | 2.05 | 40,645 | - | - | - | - | 10 | predicted (travel demand) |
| 260 | Pamplona | 1.35 | 128,065 | - | - | - | 1 | 10 | predicted (travel demand) |
| 261 | Cesky Krumlov | 1.36 | 28,582 | 6 | - | - | 11 | 10 | predicted (travel demand) |
| 262 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 263 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 264 | Stockholm | 1.48 | 188,184 | 4 | 3 | - | - | 30 | measured |
| 265 | Buenos Aires | 1.83 | 333,331 | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 266 | Melbourne | 1.26 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 267 | Sofia | 1.26 | 138,710 | 4 | - | - | - | 30 | measured |
| 268 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 269 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 270 | Yakushima | 1.13 | - | - | - | - | 1 | 10 | predicted (travel demand) |
| 271 | Matera | 1.00 | 67,033 | - | - | - | 2 | 10 | predicted (travel demand) |
| 272 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 273 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 274 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 275 | Houston | 1.69 | - | 4 | - | - | - | 30 | measured |
| 276 | Granada | 1.05 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 277 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 278 | Bangkok | 1.58 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 279 | Hobart | 1.05 | 81,734 | 10 | - | 2 | 455 | 20 | measured |
| 280 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 281 | Wroclaw | 1.05 | 123,894 | 5 | 1 | 1 | 121 | 20 | measured |
| 282 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 283 | Belgrade | 1.48 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 284 | Ferrara | 0.84 | 27,490 | 5 | 1 | 1 | 7 | 20 | measured |
| 285 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 286 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 287 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 288 | Bucharest | 1.26 | 136,836 | 4 | - | 1 | - | 20 | measured |
| 289 | Thessaloniki | 1.26 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 290 | Regensburg | 1.18 | 51,930 | - | - | - | 2 | 10 | predicted (travel demand) |
| 291 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 292 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 293 | Bamberg | 0.97 | 28,716 | 4 | - | 1 | 10 | 10 | predicted (travel demand) |
| 294 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 295 | Assisi | 0.68 | 30,278 | 6 | - | 2 | 6 | 10 | predicted (travel demand) |
| 296 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 297 | Salzburg | 0.68 | 107,243 | 5 | - | - | 34 | 10 | published, never ranked (may be uncrawled) |
| 298 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 299 | Bari | 0.42 | 86,456 | 4 | - | - | 8 | 30 | measured |
| 300 | Gdansk | 0.42 | 4,908 | 6 | 4 | - | 288 | 20 | measured |
| 301 | Ottawa | 0.42 | - | 8 | - | 1 | 119 | 20 | measured |
| 302 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 303 | Antwerp | 0.42 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 304 | Parma | 0.21 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 305 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 306 | George Town | 0.28 | 36,080 | - | - | - | - | 10 | predicted (travel demand) |
| 307 | Hawaii | 0.21 | - | 6 | - | 1 | 6 | 30 | measured |
| 308 | Queenstown | 0.16 | 36,672 | - | - | - | - | 10 | predicted (travel demand) |
| 309 | Halifax | 0.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 310 | Memphis | 0.04 | - | - | - | - | - | 10 | predicted (travel demand) |

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

