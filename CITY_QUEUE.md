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
| 1 | Amsterdam | 76.58 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 2 | Rome | 73.46 | 358,876 | 30 | 9 | 2 | 32 | 30 | measured |
| 3 | Barcelona | 44.74 | 346,477 | 46 | 12 | 6 | 183 | 30 | measured |
| 4 | Milan | 43.49 | 212,705 | 22 | 9 | 2 | 25 | 30 | measured |
| 5 | Lisbon | 42.45 | 201,877 | 33 | 10 | 3 | 66 | 30 | measured |
| 6 | Tenerife | 47.03 | - | 4 | - | - | - | 20 | measured |
| 7 | Singapore | 39.33 | 967,821 | 18 | 3 | 2 | 165 | 30 | measured |
| 8 | Florence | 28.30 | 184,099 | 23 | 7 | 1 | 27 | 30 | measured |
| 9 | Palermo | 27.68 | 124,310 | 21 | 7 | 1 | 37 | 20 | measured |
| 10 | Brisbane | 33.92 | 162,602 | 15 | 1 | 1 | 186 | 30 | measured |
| 11 | Naples | 24.76 | 198,913 | 20 | 3 | 3 | 46 | 20 | measured |
| 12 | Madrid | 29.97 | 274,553 | 17 | 10 | 2 | - | 20 | measured |
| 13 | Prague | 31.42 | 303,350 | 17 | 13 | 3 | 29 | 30 | measured |
| 14 | Vienna | 30.59 | 283,090 | 30 | 13 | 5 | 376 | 30 | measured |
| 15 | Copenhagen | 41.20 | 218,621 | 16 | 1 | 2 | - | 30 | measured |
| 16 | Seville | 28.72 | 170,545 | 43 | 6 | 2 | - | 20 | measured |
| 17 | Paris | 28.72 | 524,268 | 30 | 9 | 4 | 129 | 30 | measured |
| 18 | Malaga | 27.05 | 117,780 | 10 | 5 | 1 | - | 30 | measured |
| 19 | London | 33.92 | 718,291 | 23 | 10 | 1 | - | 30 | measured |
| 20 | Bath | 38.50 | 144,950 | 5 | 1 | 1 | - | 20 | measured |
| 21 | Madeira | 20.39 | - | 6 | 1 | - | - | 20 | measured |
| 22 | Venice | 18.94 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 23 | Brussels | 22.47 | 176,863 | 30 | 4 | 1 | 436 | 30 | measured |
| 24 | Dublin | 16.23 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 25 | Valencia | 13.73 | 162,209 | 16 | 2 | 2 | 350 | 30 | measured |
| 26 | Nijmegen | 13.53 | 42,338 | 20 | 1 | 2 | 159 | 20 | measured |
| 27 | Palma de Mallorca | 14.98 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 28 | Fukuoka | 14.36 | 77,485 | 13 | 7 | 1 | - | 20 | measured |
| 29 | Seoul | 20.39 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 30 | Alicante | 9.78 | 77,454 | 14 | 2 | 2 | 44 | 20 | measured |
| 31 | Porto | 9.78 | 120,415 | 27 | 5 | 2 | 40 | 20 | measured |
| 32 | Sardinia | 11.24 | - | 5 | 2 | - | 4 | 20 | measured |
| 33 | The Hague | 8.95 | 236,723 | 30 | 1 | 5 | 166 | 20 | measured |
| 34 | New York | 15.40 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 35 | Crete | 17.48 | - | 4 | - | - | - | 20 | measured |
| 36 | Krakow | 11.03 | 140,824 | 21 | 3 | 2 | 198 | 30 | measured |
| 37 | Montreal | 16.44 | 315,322 | 7 | - | 1 | - | 30 | measured |
| 38 | Geneva | 10.61 | 162,269 | 21 | 4 | 4 | 131 | 20 | measured |
| 39 | Bologna | 8.53 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 40 | Leiden | 7.91 | 33,227 | 12 | 4 | 1 | 129 | 20 | measured |
| 41 | Edinburgh | 15.40 | 292,981 | 15 | 4 | 1 | - | 30 | measured |
| 42 | Cambridge | 15.40 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 43 | Bari | 8.65 | 86,456 | - | - | - | 8 | 10 | predicted (travel demand) |
| 44 | Dubrovnik | 13.94 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 45 | Reykjavik | 12.07 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 46 | Toronto | 13.73 | 411,011 | 6 | - | - | - | 30 | measured |
| 47 | Girona | 7.87 | 51,072 | - | - | - | - | 10 | predicted (travel demand) |
| 48 | Portland | 8.95 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 49 | Tokyo | 6.87 | 394,702 | 10 | 8 | - | 7 | 20 | measured |
| 50 | Groningen | 6.66 | 31,401 | 19 | - | 2 | 72 | 20 | measured |
| 51 | Padua | 7.08 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 52 | Washington DC | 12.07 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 53 | Las Vegas | 13.11 | - | 11 | - | 2 | - | 30 | measured |
| 54 | Leipzig | 8.60 | 121,319 | - | - | - | - | 10 | predicted (travel demand) |
| 55 | Sintra | 6.45 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 56 | Berlin | 8.53 | 412,181 | 19 | 11 | 1 | 195 | 30 | measured |
| 57 | Cagliari | 6.45 | 51,351 | 7 | 1 | 2 | 9 | 20 | measured |
| 58 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 59 | Boston | 10.82 | 385,902 | 10 | 1 | 1 | - | 30 | measured |
| 60 | Trieste | 5.62 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 61 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 62 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 63 | Hamburg | 10.27 | 191,221 | - | - | - | - | 10 | predicted (travel demand) |
| 64 | Oslo | 9.36 | 181,113 | 4 | - | - | - | 20 | measured |
| 65 | Bordeaux | 7.08 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 66 | Kansas City | 10.51 | - | - | - | - | - | 10 | predicted (travel demand) |
| 67 | Asheville | 10.45 | - | - | - | - | - | 10 | predicted (travel demand) |
| 68 | Utrecht | 5.20 | 67,963 | 22 | 4 | 2 | 345 | 20 | measured |
| 69 | Guimaraes | 5.41 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 70 | Vilnius | 6.87 | 113,188 | 10 | 1 | 1 | 34 | 30 | measured |
| 71 | Kyoto | 6.45 | 142,353 | 18 | 8 | 2 | - | 20 | measured |
| 72 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 73 | Vancouver | 9.47 | 351,552 | - | - | - | - | 10 | predicted (travel demand) |
| 74 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 75 | Dresden | 6.41 | 113,624 | - | - | - | - | 10 | predicted (travel demand) |
| 76 | Turin | 4.79 | 147,456 | 10 | 7 | 2 | 30 | 20 | measured |
| 77 | Bristol | 9.36 | 163,983 | 5 | 1 | - | - | 20 | measured |
| 78 | Turku | 9.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 79 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 80 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 81 | Canberra | 9.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 82 | Manchester | 9.06 | 316,438 | - | - | - | - | 10 | predicted (travel demand) |
| 83 | Bratislava | 6.03 | 132,162 | 6 | - | 1 | 26 | 30 | measured |
| 84 | Munich | 6.03 | 224,067 | 44 | 14 | 6 | 80 | 30 | measured |
| 85 | Genoa | 4.79 | 145,206 | 12 | 1 | 1 | 11 | 20 | measured |
| 86 | Pisa | 5.85 | 52,174 | - | - | - | - | 10 | predicted (travel demand) |
| 87 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 88 | Cordoba | 5.62 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 89 | Cork | 5.83 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 90 | Sorrento | 4.37 | 40,049 | 4 | - | - | 20 | 20 | measured |
| 91 | Hiroshima | 5.55 | 129,791 | - | - | - | - | 10 | predicted (travel demand) |
| 92 | Potsdam | 5.62 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 93 | Taipei | 8.38 | 143,193 | - | - | - | - | 10 | predicted (travel demand) |
| 94 | Salamanca | 5.50 | 47,897 | - | - | - | 1 | 10 | predicted (travel demand) |
| 95 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 96 | San Francisco | 8.08 | 361,111 | - | - | - | - | 10 | predicted (travel demand) |
| 97 | Buenos Aires | 7.33 | 333,331 | - | - | - | - | 10 | predicted (travel demand) |
| 98 | Quebec City | 5.20 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 99 | Chicago | 7.70 | 485,769 | 6 | - | - | - | 30 | measured |
| 100 | Athens | 7.49 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 101 | Budapest | 7.28 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 102 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 103 | Cadiz | 4.79 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 104 | Kauai | 7.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 105 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 106 | Cyprus | 7.08 | - | 4 | - | - | - | 20 | measured |
| 107 | Perth | 7.08 | 180,478 | 6 | 1 | 1 | - | 30 | measured |
| 108 | Lyon | 4.79 | 136,951 | 13 | 3 | 1 | 156 | 20 | measured |
| 109 | Haarlem | 3.54 | 33,960 | 21 | - | 2 | 277 | 20 | measured |
| 110 | Maastricht | 3.54 | 47,763 | 10 | - | 1 | 136 | 20 | measured |
| 111 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 112 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 113 | Warsaw | 4.58 | 197,929 | 10 | 3 | 1 | 1427 | 30 | measured |
| 114 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 115 | Caserta | 3.33 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 116 | Lucca | 3.33 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 117 | Liverpool | 6.46 | 248,189 | - | - | - | - | 10 | predicted (travel demand) |
| 118 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 119 | Freiburg | 6.18 | 92,752 | - | - | - | - | 10 | predicted (travel demand) |
| 120 | Strasbourg | 4.37 | 154,700 | 10 | 1 | 2 | 66 | 30 | measured |
| 121 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 122 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 123 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 124 | Rio de Janeiro | 6.36 | 279,431 | - | - | - | - | 10 | predicted (travel demand) |
| 125 | Detroit | 6.26 | - | - | - | - | - | 10 | predicted (travel demand) |
| 126 | Nice | 6.24 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 127 | Helsinki | 4.99 | 148,908 | 8 | 1 | - | 9 | 30 | measured |
| 128 | Glasgow | 5.62 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 129 | Gothenburg | 5.95 | 119,991 | - | - | - | - | 10 | predicted (travel demand) |
| 130 | Tallinn | 3.95 | 124,888 | 4 | 2 | 1 | 42 | 20 | measured |
| 131 | Beijing | 5.73 | 269,737 | - | - | - | - | 10 | predicted (travel demand) |
| 132 | Seattle | 5.62 | 398,724 | 5 | - | - | - | 30 | measured |
| 133 | Denver | 5.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 134 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 135 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 136 | Sacramento | 5.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 137 | Zurich | 5.41 | 140,788 | 4 | - | - | - | 20 | measured |
| 138 | Toulouse | 3.75 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 139 | Bruges | 5.60 | 106,902 | - | - | - | - | 10 | predicted (travel demand) |
| 140 | Philadelphia | 5.34 | 405,294 | - | - | - | - | 10 | predicted (travel demand) |
| 141 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 142 | San Diego | 5.53 | 214,939 | - | - | - | - | 10 | predicted (travel demand) |
| 143 | Riga | 4.90 | 108,918 | - | - | - | - | 10 | predicted (travel demand) |
| 144 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 145 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 146 | Setubal | 2.91 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 147 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 148 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 149 | Sapporo | 3.51 | 88,633 | - | - | - | - | 10 | predicted (travel demand) |
| 150 | York | 5.20 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 151 | Aarhus | 4.99 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 152 | Cardiff | 5.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 153 | Salt Lake City | 5.16 | - | - | - | - | - | 10 | predicted (travel demand) |
| 154 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 155 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 156 | Sydney | 4.99 | 305,304 | 6 | - | - | - | 30 | measured |
| 157 | Auckland | 4.67 | 152,056 | - | - | - | - | 10 | predicted (travel demand) |
| 158 | Lausanne | 4.90 | 68,242 | - | - | - | - | 10 | predicted (travel demand) |
| 159 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 160 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 161 | Nagoya | 3.17 | 83,437 | - | - | - | 1 | 10 | predicted (travel demand) |
| 162 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 163 | Istanbul | 4.16 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 164 | Miami | 4.74 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 165 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 166 | Bergamo | 2.29 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 167 | Delft | 2.29 | 31,293 | 4 | - | 1 | 51 | 20 | measured |
| 168 | Stuttgart | 4.08 | 112,789 | - | - | - | - | 10 | predicted (travel demand) |
| 169 | Menorca | 2.93 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 170 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 171 | Stockholm | 3.33 | 188,184 | 4 | 3 | - | - | 30 | measured |
| 172 | Naha | 2.84 | 24,466 | - | - | - | 1 | 10 | predicted (travel demand) |
| 173 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 174 | Osaka | 2.71 | 163,112 | 4 | 1 | - | - | 30 | measured |
| 175 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 176 | Braga | 2.29 | 34,522 | 4 | 1 | - | 8 | 20 | measured |
| 177 | Belfast | 4.15 | 224,315 | - | - | - | - | 10 | predicted (travel demand) |
| 178 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 179 | Perugia | 2.08 | 42,572 | 10 | - | 2 | 19 | 20 | measured |
| 180 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 181 | Poznan | 2.71 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 182 | Salzburg | 2.71 | 107,243 | - | - | - | 33 | 10 | predicted (travel demand) |
| 183 | Kanazawa | 2.53 | 25,778 | - | - | - | 2 | 10 | predicted (travel demand) |
| 184 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 185 | Nantes | 3.83 | 67,689 | - | - | - | - | 10 | predicted (travel demand) |
| 186 | Hong Kong | 2.60 | 689,212 | 10 | 2 | 1 | 505 | 20 | measured |
| 187 | Verona | 2.29 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 188 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 189 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 190 | Los Angeles | 3.60 | 665,559 | 7 | 2 | - | - | 10 | published, never ranked (may be uncrawled) |
| 191 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 192 | Nuremberg | 2.50 | 161,614 | 10 | 1 | 1 | 39 | 20 | measured |
| 193 | Breda | 1.87 | 36,579 | 4 | - | 1 | 119 | 20 | measured |
| 194 | Rothenburg ob der Tauber | 3.08 | 39,879 | - | - | - | 8 | 10 | predicted (travel demand) |
| 195 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 196 | Luxembourg City | 2.39 | 64,851 | - | - | - | - | 10 | predicted (travel demand) |
| 197 | Split | 3.54 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 198 | Brighton | 3.40 | 114,108 | - | - | - | - | 10 | predicted (travel demand) |
| 199 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 200 | Busan | 3.31 | 94,737 | - | - | - | - | 10 | predicted (travel demand) |
| 201 | Graz | 2.29 | 65,717 | 10 | 3 | 1 | 87 | 20 | measured |
| 202 | Oahu | 2.29 | - | 5 | - | - | 133 | 20 | measured |
| 203 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 204 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 205 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 206 | Oxford | 3.33 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 207 | Den Bosch | 1.66 | 39,682 | 11 | 1 | 1 | 119 | 20 | measured |
| 208 | Rotterdam | 1.66 | 104,938 | 9 | - | 2 | 83 | 20 | measured |
| 209 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 210 | Segovia | 2.17 | 30,968 | - | - | - | 1 | 10 | predicted (travel demand) |
| 211 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 212 | Mexico City | 3.02 | 566,583 | 9 | 1 | - | - | 30 | measured |
| 213 | Catania | 1.87 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 214 | Ljubljana | 3.12 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 215 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 216 | Sao Paulo | 2.96 | 911 | - | - | - | - | 10 | predicted (travel demand) |
| 217 | Savannah | 3.05 | 128,162 | - | - | - | - | 10 | predicted (travel demand) |
| 218 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 219 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 220 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 221 | Cologne | 3.04 | 191,812 | 5 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 222 | Heidelberg | 2.69 | 75,837 | - | - | - | - | 10 | predicted (travel demand) |
| 223 | Modena | 1.77 | 51,698 | - | - | - | 3 | 10 | predicted (travel demand) |
| 224 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 225 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 226 | Granada | 1.87 | 86,361 | 10 | 3 | 2 | 4 | 20 | measured |
| 227 | Zaragoza | 1.87 | 87,580 | 7 | - | 1 | - | 20 | measured |
| 228 | Arnhem | 1.46 | 31,478 | 9 | 1 | 1 | 196 | 20 | measured |
| 229 | Como | 1.46 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 230 | Brno | 1.87 | 63,714 | 7 | 1 | 2 | 30 | 20 | measured |
| 231 | Frankfurt | 1.87 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 232 | Ibiza | 1.85 | - | - | - | - | - | 10 | predicted (travel demand) |
| 233 | Kamakura | 1.74 | 33,492 | - | - | - | - | 10 | predicted (travel demand) |
| 234 | Coimbra | 1.44 | 34,962 | - | - | - | 5 | 10 | predicted (travel demand) |
| 235 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 236 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 237 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 238 | Ronda | 1.68 | 51,510 | - | - | - | 1 | 10 | predicted (travel demand) |
| 239 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 240 | Lima | 2.03 | 132,792 | - | - | - | - | 10 | predicted (travel demand) |
| 241 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 242 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 243 | Ghent | 2.36 | 82,757 | - | - | - | - | 10 | predicted (travel demand) |
| 244 | Ferrara | 1.46 | 27,490 | 5 | 1 | 1 | 7 | 20 | measured |
| 245 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 246 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 247 | Belgrade | 2.50 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 248 | New Orleans | 2.50 | 256,232 | 4 | - | 1 | - | 20 | measured |
| 249 | Bilbao | 1.66 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 250 | Sofia | 1.66 | 138,710 | 4 | - | - | - | 30 | measured |
| 251 | Maui | 2.33 | - | - | - | - | 3 | 10 | predicted (travel demand) |
| 252 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 253 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 254 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 255 | Tarragona | 1.45 | 32,396 | - | - | - | - | 10 | predicted (travel demand) |
| 256 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 257 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 258 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 259 | Hallstatt | 1.99 | 47,271 | - | - | - | - | 10 | predicted (travel demand) |
| 260 | Bangkok | 2.29 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 261 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 262 | Charleston | 2.21 | 155,987 | - | - | - | - | 10 | predicted (travel demand) |
| 263 | Rouen | 2.17 | 72,334 | - | - | - | 1 | 10 | predicted (travel demand) |
| 264 | Hobart | 1.46 | 81,734 | 10 | - | 2 | 455 | 20 | measured |
| 265 | Melbourne | 1.46 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 266 | Antwerp | 2.08 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 267 | Trento | 1.04 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 268 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 269 | Leuven | 2.05 | 40,645 | - | - | - | - | 10 | predicted (travel demand) |
| 270 | Pamplona | 1.35 | 128,065 | - | - | - | 1 | 10 | predicted (travel demand) |
| 271 | Cesky Krumlov | 1.36 | 28,582 | - | - | - | 11 | 10 | predicted (travel demand) |
| 272 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 273 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 274 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 275 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 276 | Yakushima | 1.13 | - | - | - | - | 1 | 10 | predicted (travel demand) |
| 277 | Matera | 1.00 | 67,033 | - | - | - | 2 | 10 | predicted (travel demand) |
| 278 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 279 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 280 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 281 | Austin | 1.66 | 226,631 | 5 | - | - | - | 20 | measured |
| 282 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 283 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 284 | Wroclaw | 1.04 | 123,894 | 4 | 1 | 1 | 122 | 20 | measured |
| 285 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 286 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 287 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 288 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 289 | Dallas | 1.25 | - | 8 | - | 1 | - | 30 | measured |
| 290 | Houston | 1.25 | - | 4 | - | - | - | 30 | measured |
| 291 | Regensburg | 1.18 | 51,930 | - | - | - | 2 | 10 | predicted (travel demand) |
| 292 | Thessaloniki | 1.25 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 293 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 294 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 295 | Assisi | 0.68 | 30,278 | - | - | - | 6 | 10 | predicted (travel demand) |
| 296 | Bamberg | 0.97 | 28,716 | - | - | - | 10 | 10 | predicted (travel demand) |
| 297 | Parma | 0.62 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 298 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 299 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 300 | Bucharest | 1.04 | 136,836 | 4 | - | 1 | - | 20 | measured |
| 301 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 302 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 303 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 304 | Gdansk | 0.21 | 4,908 | 4 | 2 | - | 228 | 20 | measured |
| 305 | Ottawa | 0.21 | - | 8 | - | 1 | 119 | 20 | measured |
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

