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
| 1 | Amsterdam | 78.58 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 2 | Rome | 78.58 | 358,876 | 30 | 9 | 2 | 32 | 30 | measured |
| 3 | Milan | 45.09 | 212,705 | 22 | 9 | 2 | 25 | 30 | measured |
| 4 | Lisbon | 42.56 | 201,877 | 33 | 10 | 3 | 66 | 30 | measured |
| 5 | Barcelona | 40.45 | 346,477 | 55 | 12 | 8 | 180 | 30 | measured |
| 6 | Tenerife | 50.35 | - | 4 | - | - | - | 20 | measured |
| 7 | Singapore | 40.24 | 967,821 | 18 | 3 | 2 | 165 | 30 | measured |
| 8 | Brisbane | 36.66 | 162,602 | 19 | 1 | 2 | 189 | 30 | measured |
| 9 | Florence | 26.12 | 184,099 | 23 | 7 | 1 | 27 | 30 | measured |
| 10 | Palermo | 24.86 | 124,310 | 21 | 7 | 1 | 37 | 20 | measured |
| 11 | Madrid | 30.55 | 274,553 | 17 | 10 | 2 | - | 20 | measured |
| 12 | Naples | 24.23 | 198,913 | 22 | 3 | 3 | 46 | 20 | measured |
| 13 | Prague | 32.23 | 303,350 | 17 | 13 | 3 | 29 | 30 | measured |
| 14 | Vienna | 31.18 | 283,090 | 30 | 13 | 5 | 376 | 30 | measured |
| 15 | Seville | 30.76 | 170,545 | 43 | 6 | 2 | - | 20 | measured |
| 16 | Paris | 29.07 | 524,268 | 31 | 9 | 4 | 129 | 30 | measured |
| 17 | Copenhagen | 40.87 | 218,621 | 16 | 1 | 2 | - | 30 | measured |
| 18 | Malaga | 28.23 | 117,780 | 10 | 5 | 1 | - | 30 | measured |
| 19 | Madeira | 22.75 | - | 6 | 1 | - | - | 20 | measured |
| 20 | London | 32.87 | 718,291 | 23 | 10 | 1 | - | 30 | measured |
| 21 | Bath | 37.08 | 144,950 | 5 | 1 | 1 | - | 20 | measured |
| 22 | Venice | 18.54 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 23 | Brussels | 22.12 | 176,863 | 30 | 4 | 1 | 436 | 30 | measured |
| 24 | Nijmegen | 13.69 | 42,338 | 20 | 1 | 2 | 159 | 20 | measured |
| 25 | Valencia | 13.48 | 162,209 | 16 | 2 | 2 | 350 | 30 | measured |
| 26 | Palma de Mallorca | 16.01 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 27 | Dublin | 14.75 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 28 | Fukuoka | 15.38 | 77,485 | 13 | 7 | 1 | - | 20 | measured |
| 29 | Sardinia | 12.85 | - | 5 | 2 | - | 8 | 20 | measured |
| 30 | Seoul | 20.65 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 31 | Crete | 19.80 | - | 4 | - | - | - | 20 | measured |
| 32 | Bologna | 10.32 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 33 | Alicante | 9.48 | 77,454 | 14 | 2 | 2 | 44 | 20 | measured |
| 34 | Porto | 9.48 | 120,415 | 27 | 5 | 2 | 40 | 20 | measured |
| 35 | Krakow | 12.01 | 140,824 | 26 | 3 | 3 | 200 | 30 | measured |
| 36 | The Hague | 8.64 | 236,723 | 30 | 1 | 5 | 166 | 20 | measured |
| 37 | Montreal | 16.85 | 315,322 | 7 | - | 1 | - | 30 | measured |
| 38 | Edinburgh | 16.43 | 292,981 | 15 | 4 | 1 | - | 30 | measured |
| 39 | New York | 14.54 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 40 | Toronto | 15.80 | 411,011 | 6 | - | - | - | 30 | measured |
| 41 | Portland | 10.53 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 42 | Groningen | 7.80 | 31,401 | 20 | - | 2 | 72 | 20 | measured |
| 43 | Leiden | 7.80 | 33,227 | 12 | 4 | 1 | 129 | 20 | measured |
| 44 | Geneva | 10.32 | 162,269 | 21 | 4 | 4 | 131 | 20 | measured |
| 45 | Reykjavik | 12.43 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 46 | Tokyo | 7.16 | 394,702 | 10 | 8 | - | 7 | 20 | measured |
| 47 | Dubrovnik | 13.06 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 48 | Las Vegas | 13.69 | - | 11 | - | 2 | - | 30 | measured |
| 49 | Girona | 7.87 | 51,072 | - | - | - | - | 10 | predicted (travel demand) |
| 50 | Cagliari | 6.95 | 51,351 | 8 | 1 | 2 | 15 | 20 | measured |
| 51 | Cambridge | 12.43 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 52 | Padua | 6.53 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 53 | Sintra | 6.11 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 54 | Berlin | 7.80 | 412,181 | 19 | 11 | 1 | 195 | 30 | measured |
| 55 | Bordeaux | 7.80 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 56 | Washington DC | 10.53 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 57 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 58 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 59 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 60 | Trieste | 5.48 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 61 | Guimaraes | 5.69 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 62 | Kyoto | 6.95 | 142,353 | 18 | 8 | 2 | - | 20 | measured |
| 63 | Munich | 7.16 | 224,067 | 45 | 14 | 6 | 80 | 30 | measured |
| 64 | Vilnius | 7.16 | 113,188 | 10 | 1 | 1 | 34 | 30 | measured |
| 65 | Hamburg | 10.27 | 191,221 | - | - | - | - | 10 | predicted (travel demand) |
| 66 | Utrecht | 5.27 | 67,963 | 33 | 4 | 2 | 345 | 20 | measured |
| 67 | Kansas City | 10.51 | - | - | - | - | - | 10 | predicted (travel demand) |
| 68 | Asheville | 10.45 | - | - | - | - | - | 10 | predicted (travel demand) |
| 69 | Oslo | 8.85 | 181,113 | 4 | - | - | - | 20 | measured |
| 70 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 71 | Turin | 4.85 | 147,456 | 10 | 7 | 2 | 30 | 20 | measured |
| 72 | Vancouver | 9.47 | 351,552 | - | - | - | - | 10 | predicted (travel demand) |
| 73 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 74 | Dresden | 6.41 | 113,624 | 4 | - | - | - | 10 | predicted (travel demand) |
| 75 | Bratislava | 6.32 | 132,162 | 6 | - | 1 | 26 | 30 | measured |
| 76 | Boston | 9.06 | 385,902 | 10 | 1 | 1 | - | 30 | measured |
| 77 | Turku | 9.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 78 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 79 | Sorrento | 4.63 | 40,049 | 4 | - | - | 20 | 20 | measured |
| 80 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 81 | Canberra | 9.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 82 | Manchester | 9.06 | 316,438 | - | - | - | - | 10 | predicted (travel demand) |
| 83 | Bristol | 8.85 | 163,983 | 5 | 1 | - | - | 20 | measured |
| 84 | Pisa | 5.85 | 52,174 | - | - | - | - | 10 | predicted (travel demand) |
| 85 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 86 | Cordoba | 5.48 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 87 | Potsdam | 5.69 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 88 | Hiroshima | 5.55 | 129,791 | - | - | - | - | 10 | predicted (travel demand) |
| 89 | Athens | 8.22 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 90 | Taipei | 8.38 | 143,193 | - | - | - | - | 10 | predicted (travel demand) |
| 91 | Salamanca | 5.50 | 47,897 | - | - | - | 1 | 10 | predicted (travel demand) |
| 92 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 93 | San Francisco | 8.08 | 361,111 | - | - | - | - | 10 | predicted (travel demand) |
| 94 | Chicago | 8.22 | 485,769 | 6 | - | - | - | 30 | measured |
| 95 | Lyon | 5.48 | 136,951 | 13 | 3 | 1 | 156 | 20 | measured |
| 96 | Perth | 7.80 | 180,478 | 6 | 1 | 1 | - | 30 | measured |
| 97 | Cork | 5.27 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 98 | Budapest | 7.58 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 99 | Buenos Aires | 7.33 | 333,331 | 4 | - | - | - | 10 | predicted (travel demand) |
| 100 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 101 | Kauai | 7.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 102 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 103 | Cyprus | 7.16 | - | 4 | - | - | - | 20 | measured |
| 104 | Quebec City | 4.85 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 105 | Helsinki | 5.90 | 148,908 | 8 | 1 | - | 9 | 30 | measured |
| 106 | Strasbourg | 4.63 | 154,700 | 10 | 1 | 2 | 66 | 30 | measured |
| 107 | Warsaw | 4.63 | 197,929 | 15 | 3 | 2 | 1430 | 30 | measured |
| 108 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 109 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 110 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 111 | Caserta | 3.37 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 112 | Maastricht | 3.37 | 47,763 | 14 | - | 1 | 137 | 20 | measured |
| 113 | Liverpool | 6.46 | 248,189 | - | - | - | - | 10 | predicted (travel demand) |
| 114 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 115 | Freiburg | 6.18 | 92,752 | - | - | - | - | 10 | predicted (travel demand) |
| 116 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 117 | Glasgow | 6.11 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 118 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 119 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 120 | Rio de Janeiro | 6.36 | 279,431 | - | - | - | - | 10 | predicted (travel demand) |
| 121 | Seattle | 6.11 | 398,724 | 6 | - | - | - | 30 | measured |
| 122 | Haarlem | 3.16 | 33,960 | 21 | - | 2 | 277 | 20 | measured |
| 123 | Tallinn | 4.21 | 124,888 | 4 | 2 | 1 | 42 | 20 | measured |
| 124 | Detroit | 6.26 | - | - | - | - | - | 10 | predicted (travel demand) |
| 125 | Gothenburg | 5.95 | 119,991 | - | - | - | - | 10 | predicted (travel demand) |
| 126 | Lucca | 2.95 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 127 | Nice | 5.90 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 128 | Beijing | 5.73 | 269,737 | - | - | - | - | 10 | predicted (travel demand) |
| 129 | Denver | 5.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 130 | Sydney | 5.69 | 305,304 | 6 | - | - | - | 30 | measured |
| 131 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 132 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 133 | Zurich | 5.48 | 140,788 | 4 | - | - | - | 20 | measured |
| 134 | Sacramento | 5.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 135 | Bruges | 5.60 | 106,902 | - | - | - | - | 10 | predicted (travel demand) |
| 136 | Cadiz | 3.58 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 137 | Philadelphia | 5.34 | 405,294 | - | - | - | - | 10 | predicted (travel demand) |
| 138 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 139 | San Diego | 5.53 | 214,939 | - | - | - | - | 10 | predicted (travel demand) |
| 140 | Riga | 4.90 | 108,918 | - | - | - | - | 10 | predicted (travel demand) |
| 141 | Aarhus | 5.27 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 142 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 143 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 144 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 145 | Toulouse | 3.58 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 146 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 147 | York | 5.27 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 148 | Sapporo | 3.51 | 88,633 | - | - | - | - | 10 | predicted (travel demand) |
| 149 | Cardiff | 5.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 150 | Salt Lake City | 5.16 | - | - | - | - | - | 10 | predicted (travel demand) |
| 151 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 152 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 153 | Setubal | 2.74 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 154 | Auckland | 4.67 | 152,056 | - | - | - | - | 10 | predicted (travel demand) |
| 155 | Istanbul | 4.42 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 156 | Lausanne | 4.90 | 68,242 | - | - | - | - | 10 | predicted (travel demand) |
| 157 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 158 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 159 | Perugia | 2.53 | 42,572 | 10 | - | 2 | 19 | 20 | measured |
| 160 | Nagoya | 3.17 | 83,437 | - | - | - | 1 | 10 | predicted (travel demand) |
| 161 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 162 | Graz | 3.16 | 65,717 | 10 | 3 | 1 | 87 | 20 | measured |
| 163 | Miami | 4.74 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 164 | Verona | 2.74 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 165 | Delft | 2.32 | 31,293 | 4 | - | 1 | 51 | 20 | measured |
| 166 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 167 | Stuttgart | 4.08 | 112,789 | - | - | - | - | 10 | predicted (travel demand) |
| 168 | Menorca | 2.93 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 169 | Nuremberg | 2.95 | 161,614 | 10 | 1 | 1 | 39 | 20 | measured |
| 170 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 171 | Naha | 2.84 | 24,466 | - | - | - | 1 | 10 | predicted (travel demand) |
| 172 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 173 | Arnhem | 2.11 | 31,478 | 9 | 1 | 1 | 196 | 20 | measured |
| 174 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 175 | Belfast | 4.15 | 224,315 | - | - | - | - | 10 | predicted (travel demand) |
| 176 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 177 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 178 | Salzburg | 2.71 | 107,243 | - | - | - | 33 | 10 | predicted (travel demand) |
| 179 | Kanazawa | 2.53 | 25,778 | - | - | - | 2 | 10 | predicted (travel demand) |
| 180 | Catania | 2.32 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 181 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 182 | Nantes | 3.83 | 67,689 | - | - | - | - | 10 | predicted (travel demand) |
| 183 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 184 | Braga | 2.11 | 34,522 | 4 | 1 | - | 8 | 20 | measured |
| 185 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 186 | Los Angeles | 3.60 | 665,559 | 7 | 2 | - | - | 10 | published, never ranked (may be uncrawled) |
| 187 | Bergamo | 1.90 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 188 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 189 | Rotterdam | 1.90 | 104,938 | 9 | - | 2 | 83 | 20 | measured |
| 190 | Hong Kong | 2.53 | 689,212 | 10 | 2 | 1 | 505 | 20 | measured |
| 191 | Oahu | 2.53 | - | 6 | - | - | 133 | 20 | measured |
| 192 | Rothenburg ob der Tauber | 3.08 | 39,879 | - | - | - | 8 | 10 | predicted (travel demand) |
| 193 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 194 | Bari | 2.16 | 86,456 | 4 | - | - | 8 | 10 | published, never ranked (may be uncrawled) |
| 195 | Luxembourg City | 2.39 | 64,851 | - | - | - | - | 10 | predicted (travel demand) |
| 196 | Genoa | 1.90 | 145,206 | 12 | 1 | 1 | 11 | 20 | measured |
| 197 | Brighton | 3.40 | 114,108 | - | - | - | - | 10 | predicted (travel demand) |
| 198 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 199 | Busan | 3.31 | 94,737 | - | - | - | - | 10 | predicted (travel demand) |
| 200 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 201 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 202 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 203 | Mexico City | 3.16 | 566,583 | 9 | 1 | - | - | 30 | measured |
| 204 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 205 | Segovia | 2.17 | 30,968 | - | - | - | 1 | 10 | predicted (travel demand) |
| 206 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 207 | Leipzig | 2.15 | 121,319 | 7 | 7 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 208 | Oxford | 3.16 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 209 | Brno | 2.11 | 63,714 | 7 | 1 | 2 | 30 | 20 | measured |
| 210 | Frankfurt | 2.11 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 211 | Poznan | 2.11 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 212 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 213 | Sao Paulo | 2.96 | 911 | - | - | - | - | 10 | predicted (travel demand) |
| 214 | Savannah | 3.05 | 128,162 | - | - | - | - | 10 | predicted (travel demand) |
| 215 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 216 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 217 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 218 | Cologne | 3.04 | 191,812 | 5 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 219 | Stockholm | 2.32 | 188,184 | 4 | 3 | - | - | 30 | measured |
| 220 | Heidelberg | 2.69 | 75,837 | - | - | - | - | 10 | predicted (travel demand) |
| 221 | Modena | 1.77 | 51,698 | - | - | - | 3 | 10 | predicted (travel demand) |
| 222 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 223 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 224 | New Orleans | 2.95 | 256,232 | 4 | - | 1 | - | 20 | measured |
| 225 | Den Bosch | 1.47 | 39,682 | 11 | 1 | 1 | 119 | 20 | measured |
| 226 | Bilbao | 1.90 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 227 | Ibiza | 1.85 | - | - | - | - | - | 10 | predicted (travel demand) |
| 228 | Kamakura | 1.74 | 33,492 | - | - | - | - | 10 | predicted (travel demand) |
| 229 | Coimbra | 1.44 | 34,962 | - | - | - | 5 | 10 | predicted (travel demand) |
| 230 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 231 | Austin | 2.74 | 226,631 | 5 | - | - | - | 20 | measured |
| 232 | Split | 2.74 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 233 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 234 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 235 | Zaragoza | 1.69 | 87,580 | 7 | - | 1 | - | 20 | measured |
| 236 | Ronda | 1.68 | 51,510 | - | - | - | 1 | 10 | predicted (travel demand) |
| 237 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 238 | Lima | 2.03 | 132,792 | - | - | - | - | 10 | predicted (travel demand) |
| 239 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 240 | Ljubljana | 2.53 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 241 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 242 | Ghent | 2.36 | 82,757 | - | - | - | - | 10 | predicted (travel demand) |
| 243 | Breda | 1.26 | 36,579 | 4 | - | 1 | 119 | 20 | measured |
| 244 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 245 | Trento | 1.26 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 246 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 247 | Maui | 2.33 | - | - | - | - | 3 | 10 | predicted (travel demand) |
| 248 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 249 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 250 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 251 | Tarragona | 1.45 | 32,396 | - | - | - | - | 10 | predicted (travel demand) |
| 252 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 253 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 254 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 255 | Osaka | 1.47 | 163,112 | 4 | 1 | - | - | 30 | measured |
| 256 | Hallstatt | 1.99 | 47,271 | - | - | - | - | 10 | predicted (travel demand) |
| 257 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 258 | Charleston | 2.21 | 155,987 | - | - | - | - | 10 | predicted (travel demand) |
| 259 | Belgrade | 2.21 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 260 | Hobart | 1.47 | 81,734 | 10 | - | 2 | 455 | 20 | measured |
| 261 | Rouen | 2.17 | 72,334 | - | - | - | 1 | 10 | predicted (travel demand) |
| 262 | Sofia | 1.47 | 138,710 | 4 | - | - | - | 30 | measured |
| 263 | Como | 1.05 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 264 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 265 | Leuven | 2.05 | 40,645 | - | - | - | - | 10 | predicted (travel demand) |
| 266 | Pamplona | 1.35 | 128,065 | - | - | - | 1 | 10 | predicted (travel demand) |
| 267 | Cesky Krumlov | 1.36 | 28,582 | - | - | - | 11 | 10 | predicted (travel demand) |
| 268 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 269 | Granada | 1.26 | 86,361 | 10 | 3 | 2 | 4 | 20 | measured |
| 270 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 271 | Melbourne | 1.26 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 272 | Ferrara | 1.05 | 27,490 | 5 | 1 | 1 | 7 | 20 | measured |
| 273 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 274 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 275 | Yakushima | 1.13 | - | - | - | - | 1 | 10 | predicted (travel demand) |
| 276 | Matera | 1.00 | 67,033 | - | - | - | 2 | 10 | predicted (travel demand) |
| 277 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 278 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 279 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 280 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 281 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 282 | Wroclaw | 1.05 | 123,894 | 5 | 1 | 1 | 121 | 20 | measured |
| 283 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 284 | Dallas | 1.47 | - | 8 | - | 1 | - | 30 | measured |
| 285 | Bangkok | 1.37 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 286 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 287 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 288 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 289 | Bucharest | 1.26 | 136,836 | 4 | - | 1 | - | 20 | measured |
| 290 | Houston | 1.26 | - | 4 | - | - | - | 30 | measured |
| 291 | Thessaloniki | 1.26 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 292 | Regensburg | 1.18 | 51,930 | - | - | - | 2 | 10 | predicted (travel demand) |
| 293 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 294 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 295 | Assisi | 0.68 | 30,278 | - | - | - | 6 | 10 | predicted (travel demand) |
| 296 | Bamberg | 0.97 | 28,716 | - | - | - | 10 | 10 | predicted (travel demand) |
| 297 | Parma | 0.63 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 298 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 299 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 300 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 301 | Gdansk | 0.42 | 4,908 | 4 | 2 | - | 228 | 20 | measured |
| 302 | Ottawa | 0.42 | - | 8 | - | 1 | 119 | 20 | measured |
| 303 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 304 | Antwerp | 0.42 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
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

