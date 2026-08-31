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
| 1 | Rome | 105.97 | 358,876 | 30 | 9 | 2 | 32 | 30 | measured |
| 2 | Amsterdam | 96.38 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 3 | Lisbon | 55.32 | 201,877 | 33 | 10 | 3 | 66 | 30 | measured |
| 4 | Milan | 48.93 | 212,705 | 22 | 9 | 2 | 25 | 30 | measured |
| 5 | Barcelona | 43.27 | 346,477 | 56 | 12 | 7 | 180 | 30 | measured |
| 6 | Tenerife | 56.06 | - | 4 | - | - | - | 20 | measured |
| 7 | Brisbane | 45.98 | 162,602 | 19 | 1 | 2 | 189 | 30 | measured |
| 8 | Singapore | 44.01 | 967,821 | 28 | 3 | 3 | 165 | 30 | measured |
| 9 | Seville | 42.54 | 170,545 | 43 | 6 | 2 | - | 20 | measured |
| 10 | Florence | 29.75 | 184,099 | 23 | 7 | 1 | 27 | 30 | measured |
| 11 | Prague | 37.87 | 303,350 | 17 | 13 | 3 | 29 | 30 | measured |
| 12 | Malaga | 37.37 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 13 | Naples | 26.80 | 198,913 | 23 | 3 | 3 | 46 | 20 | measured |
| 14 | Vienna | 34.91 | 283,090 | 30 | 13 | 5 | 376 | 30 | measured |
| 15 | Paris | 34.18 | 524,268 | 31 | 9 | 4 | 129 | 30 | measured |
| 16 | Copenhagen | 46.23 | 218,621 | 16 | 1 | 2 | - | 30 | measured |
| 17 | Palermo | 23.36 | 124,310 | 21 | 7 | 1 | 37 | 20 | measured |
| 18 | Madeira | 25.82 | - | 6 | 1 | - | - | 20 | measured |
| 19 | London | 35.90 | 718,291 | 23 | 10 | 1 | - | 30 | measured |
| 20 | Venice | 22.13 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 21 | Valencia | 18.93 | 162,209 | 23 | 2 | 2 | 350 | 30 | measured |
| 22 | Palma de Mallorca | 22.62 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 23 | Madrid | 23.11 | 274,553 | 17 | 10 | 2 | - | 20 | measured |
| 24 | Bath | 35.90 | 144,950 | 5 | 1 | 1 | - | 20 | measured |
| 25 | Sardinia | 18.69 | - | 5 | 2 | - | 8 | 20 | measured |
| 26 | Fukuoka | 21.15 | 77,485 | 13 | 7 | 1 | - | 20 | measured |
| 27 | Dublin | 17.95 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 28 | Brussels | 20.16 | 176,863 | 30 | 4 | 1 | 436 | 30 | measured |
| 29 | Alicante | 15.00 | 77,454 | 14 | 2 | 2 | 44 | 20 | measured |
| 30 | Bologna | 15.98 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 31 | Crete | 29.01 | - | 4 | - | - | - | 20 | measured |
| 32 | Seoul | 24.59 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 33 | Nijmegen | 12.79 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 34 | Kyoto | 13.52 | 142,353 | 17 | 8 | 2 | - | 20 | measured |
| 35 | New York | 17.95 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 36 | Edinburgh | 19.92 | 292,981 | 15 | 4 | 1 | - | 30 | measured |
| 37 | Leiden | 10.08 | 33,227 | 12 | 4 | 1 | 129 | 20 | measured |
| 38 | Krakow | 13.28 | 140,824 | 34 | 3 | 3 | 198 | 30 | measured |
| 39 | Toronto | 19.42 | 411,011 | 6 | - | - | - | 30 | measured |
| 40 | Las Vegas | 19.18 | - | 11 | - | 2 | - | 30 | measured |
| 41 | Portland | 12.79 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 42 | The Hague | 9.59 | 236,723 | 29 | 1 | 5 | 166 | 20 | measured |
| 43 | Utrecht | 8.85 | 67,963 | 33 | 4 | 2 | 345 | 20 | measured |
| 44 | Tokyo | 9.10 | 394,702 | 10 | 8 | - | 7 | 20 | measured |
| 45 | Montreal | 16.72 | 315,322 | 7 | - | 1 | - | 30 | measured |
| 46 | Porto | 8.36 | 120,415 | 27 | 5 | 2 | 40 | 20 | measured |
| 47 | Bordeaux | 10.82 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 48 | Munich | 10.82 | 224,067 | 45 | 14 | 6 | 80 | 30 | measured |
| 49 | Sintra | 8.11 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 50 | Berlin | 10.33 | 412,181 | 19 | 11 | 1 | 195 | 30 | measured |
| 51 | Cagliari | 7.62 | 51,351 | 9 | 1 | 2 | 15 | 20 | measured |
| 52 | Groningen | 7.13 | 31,401 | 20 | - | 2 | 72 | 20 | measured |
| 53 | Perth | 13.77 | 180,478 | 6 | 1 | 1 | - | 30 | measured |
| 54 | Reykjavik | 11.80 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 55 | Girona | 7.87 | 51,072 | - | - | - | - | 10 | predicted (travel demand) |
| 56 | Cyprus | 12.54 | - | 4 | - | - | - | 20 | measured |
| 57 | Sydney | 12.54 | 305,304 | 6 | - | - | - | 30 | measured |
| 58 | Guimaraes | 6.39 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 59 | Chicago | 11.80 | 485,769 | 6 | - | - | - | 30 | measured |
| 60 | Strasbourg | 7.87 | 154,700 | 10 | 1 | 2 | 66 | 30 | measured |
| 61 | Vilnius | 7.87 | 113,188 | 10 | 1 | 1 | 34 | 30 | measured |
| 62 | Geneva | 7.62 | 162,269 | 21 | 4 | 4 | 131 | 20 | measured |
| 63 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 64 | Sorrento | 5.66 | 40,049 | 6 | - | 1 | 20 | 20 | measured |
| 65 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 66 | Cadiz | 7.13 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 67 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 68 | Athens | 10.57 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 69 | Hamburg | 10.27 | 191,221 | - | - | - | - | 10 | predicted (travel demand) |
| 70 | Kansas City | 10.51 | - | - | - | - | - | 10 | predicted (travel demand) |
| 71 | Seattle | 10.08 | 398,724 | 6 | - | - | - | 30 | measured |
| 72 | Asheville | 10.45 | - | - | - | - | - | 10 | predicted (travel demand) |
| 73 | Budapest | 9.59 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 74 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 75 | Arnhem | 4.92 | 31,478 | 9 | 1 | 1 | 196 | 20 | measured |
| 76 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 77 | Turku | 9.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 78 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 79 | Maastricht | 4.67 | 47,763 | 14 | - | 1 | 137 | 20 | measured |
| 80 | Trieste | 4.67 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 81 | Oslo | 8.11 | 181,113 | 4 | - | - | - | 20 | measured |
| 82 | Potsdam | 6.15 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 83 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 84 | Canberra | 9.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 85 | Manchester | 9.06 | 316,438 | - | - | - | - | 10 | predicted (travel demand) |
| 86 | Pisa | 5.85 | 52,174 | - | - | - | - | 10 | predicted (travel demand) |
| 87 | Boston | 8.61 | 385,902 | 10 | 1 | 1 | - | 30 | measured |
| 88 | Quebec City | 5.90 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 89 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 90 | Hiroshima | 5.55 | 129,791 | - | - | - | - | 10 | predicted (travel demand) |
| 91 | Taipei | 8.38 | 143,193 | - | - | - | - | 10 | predicted (travel demand) |
| 92 | Salamanca | 5.50 | 47,897 | - | - | - | 1 | 10 | predicted (travel demand) |
| 93 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 94 | San Francisco | 8.08 | 361,111 | - | - | - | - | 10 | predicted (travel demand) |
| 95 | Cambridge | 8.11 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 96 | Cordoba | 4.92 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 97 | Istanbul | 6.64 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 98 | Washington DC | 6.88 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 99 | Aarhus | 7.38 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 100 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 101 | New Orleans | 7.38 | 256,232 | 4 | - | 1 | - | 20 | measured |
| 102 | Nuremberg | 4.92 | 161,614 | 11 | 1 | 1 | 39 | 20 | measured |
| 103 | Oahu | 4.92 | - | 8 | - | - | 133 | 20 | measured |
| 104 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 105 | Helsinki | 5.90 | 148,908 | 8 | 1 | - | 9 | 30 | measured |
| 106 | Glasgow | 6.64 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 107 | Mexico City | 6.64 | 566,583 | 9 | 1 | - | - | 30 | measured |
| 108 | Bristol | 6.88 | 163,983 | 5 | 1 | - | - | 20 | measured |
| 109 | Lyon | 4.67 | 136,951 | 13 | 3 | 1 | 156 | 20 | measured |
| 110 | Melbourne | 4.67 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 111 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 112 | Padua | 3.69 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 113 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 114 | Turin | 3.44 | 147,456 | 10 | 7 | 2 | 30 | 20 | measured |
| 115 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 116 | Braga | 3.69 | 34,522 | 4 | 1 | - | 8 | 20 | measured |
| 117 | Cork | 4.43 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 118 | Liverpool | 6.46 | 248,189 | - | - | - | - | 10 | predicted (travel demand) |
| 119 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 120 | Freiburg | 6.18 | 92,752 | - | - | - | - | 10 | predicted (travel demand) |
| 121 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 122 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 123 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 124 | Rio de Janeiro | 6.36 | 279,431 | - | - | - | - | 10 | predicted (travel demand) |
| 125 | Detroit | 6.26 | - | - | - | - | - | 10 | predicted (travel demand) |
| 126 | Dubrovnik | 5.90 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 127 | Gothenburg | 5.95 | 119,991 | - | - | - | - | 10 | predicted (travel demand) |
| 128 | Bratislava | 3.93 | 132,162 | 6 | - | 1 | 26 | 30 | measured |
| 129 | Beijing | 5.73 | 269,737 | - | - | - | - | 10 | predicted (travel demand) |
| 130 | Denver | 5.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 131 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 132 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 133 | Sacramento | 5.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 134 | York | 5.66 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 135 | Bruges | 5.60 | 106,902 | - | - | - | - | 10 | predicted (travel demand) |
| 136 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 137 | Bilbao | 3.69 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 138 | Warsaw | 3.69 | 197,929 | 16 | 3 | 2 | 1430 | 30 | measured |
| 139 | San Diego | 5.53 | 214,939 | - | - | - | - | 10 | predicted (travel demand) |
| 140 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 141 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 142 | Delft | 2.70 | 31,293 | 4 | - | 1 | 51 | 20 | measured |
| 143 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 144 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 145 | Oxford | 5.16 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 146 | Sapporo | 3.51 | 88,633 | - | - | - | - | 10 | predicted (travel demand) |
| 147 | Cardiff | 5.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 148 | Salt Lake City | 5.16 | - | - | - | - | - | 10 | predicted (travel demand) |
| 149 | Tallinn | 3.44 | 124,888 | 4 | 2 | 1 | 42 | 20 | measured |
| 150 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 151 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 152 | Auckland | 4.67 | 152,056 | - | - | - | - | 10 | predicted (travel demand) |
| 153 | Catania | 2.95 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 154 | Lausanne | 4.90 | 68,242 | - | - | - | - | 10 | predicted (travel demand) |
| 155 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 156 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 157 | Caserta | 2.46 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 158 | Haarlem | 2.46 | 33,960 | 21 | - | 2 | 277 | 20 | measured |
| 159 | Rotterdam | 2.46 | 104,938 | 9 | - | 2 | 83 | 20 | measured |
| 160 | Nagoya | 3.17 | 83,437 | - | - | - | 1 | 10 | predicted (travel demand) |
| 161 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 162 | Graz | 3.20 | 65,717 | 12 | 3 | 1 | 87 | 20 | measured |
| 163 | Miami | 4.74 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 164 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 165 | Stuttgart | 4.08 | 112,789 | - | - | - | - | 10 | predicted (travel demand) |
| 166 | Dallas | 4.43 | - | 8 | 1 | 1 | - | 30 | measured |
| 167 | Lucca | 2.21 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 168 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 169 | Naha | 2.84 | 24,466 | - | - | - | 1 | 10 | predicted (travel demand) |
| 170 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 171 | Osaka | 2.70 | 163,112 | 4 | 1 | - | - | 30 | measured |
| 172 | Hong Kong | 2.83 | 689,212 | 10 | 2 | 1 | 505 | 20 | measured |
| 173 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 174 | Austin | 4.18 | 226,631 | 5 | - | - | - | 20 | measured |
| 175 | Verona | 2.46 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 176 | Belfast | 4.15 | 224,315 | - | - | - | - | 10 | predicted (travel demand) |
| 177 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 178 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 179 | Brno | 2.70 | 63,714 | 8 | 2 | 2 | 34 | 20 | measured |
| 180 | Frankfurt | 2.70 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 181 | Hobart | 2.70 | 81,734 | 10 | - | 2 | 455 | 20 | measured |
| 182 | Kanazawa | 2.53 | 25,778 | - | - | - | 2 | 10 | predicted (travel demand) |
| 183 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 184 | Nantes | 3.83 | 67,689 | - | - | - | - | 10 | predicted (travel demand) |
| 185 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 186 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 187 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 188 | Los Angeles | 3.60 | 665,559 | 8 | 2 | - | - | 10 | published, never ranked (may be uncrawled) |
| 189 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 190 | Brighton | 3.40 | 114,108 | - | - | - | - | 10 | predicted (travel demand) |
| 191 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 192 | Busan | 3.31 | 94,737 | - | - | - | - | 10 | predicted (travel demand) |
| 193 | Como | 1.72 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 194 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 195 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 196 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 197 | Poznan | 2.21 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 198 | Toulouse | 2.21 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 199 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 200 | Segovia | 2.17 | 30,968 | - | - | - | 1 | 10 | predicted (travel demand) |
| 201 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 202 | Genoa | 1.72 | 145,206 | 12 | 1 | 1 | 11 | 20 | measured |
| 203 | Houston | 3.20 | - | 4 | - | - | - | 30 | measured |
| 204 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 205 | Sao Paulo | 2.96 | 911 | - | - | - | - | 10 | predicted (travel demand) |
| 206 | Granada | 1.97 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 207 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 208 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 209 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 210 | Heidelberg | 2.69 | 75,837 | - | - | - | - | 10 | predicted (travel demand) |
| 211 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 212 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 213 | Bergamo | 1.48 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 214 | Trento | 1.48 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 215 | Nice | 2.95 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 216 | Ibiza | 1.85 | - | - | - | - | - | 10 | predicted (travel demand) |
| 217 | Kamakura | 1.74 | 33,492 | - | - | - | - | 10 | predicted (travel demand) |
| 218 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 219 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 220 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 221 | Ronda | 1.68 | 51,510 | - | - | - | 1 | 10 | predicted (travel demand) |
| 222 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 223 | Lima | 2.03 | 132,792 | - | - | - | - | 10 | predicted (travel demand) |
| 224 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 225 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 226 | Ghent | 2.36 | 82,757 | - | - | - | - | 10 | predicted (travel demand) |
| 227 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 228 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 229 | Ljubljana | 2.46 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 230 | Den Bosch | 1.23 | 39,682 | 11 | 1 | 1 | 119 | 20 | measured |
| 231 | Split | 2.46 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 232 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 233 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 234 | Vancouver | 2.37 | 351,552 | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 235 | Perugia | 1.23 | 42,572 | 10 | - | 2 | 19 | 20 | measured |
| 236 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 237 | Dresden | 1.60 | 113,624 | 5 | 1 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 238 | Tarragona | 1.45 | 32,396 | - | - | - | - | 10 | predicted (travel demand) |
| 239 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 240 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 241 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 242 | Hallstatt | 1.99 | 47,271 | - | - | - | - | 10 | predicted (travel demand) |
| 243 | Zurich | 2.21 | 140,788 | 4 | - | - | - | 20 | measured |
| 244 | Setubal | 1.23 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 245 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 246 | Kauai | 1.83 | - | 6 | - | - | 8 | 10 | published, never ranked (may be uncrawled) |
| 247 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 248 | Leuven | 2.05 | 40,645 | - | - | - | - | 10 | predicted (travel demand) |
| 249 | Pamplona | 1.35 | 128,065 | - | - | - | 1 | 10 | predicted (travel demand) |
| 250 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 251 | Bangkok | 1.97 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 252 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 253 | Stockholm | 1.48 | 188,184 | 4 | 3 | - | - | 30 | measured |
| 254 | Wroclaw | 1.23 | 123,894 | 5 | 1 | 1 | 121 | 20 | measured |
| 255 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 256 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 257 | Yakushima | 1.13 | - | - | - | - | 1 | 10 | predicted (travel demand) |
| 258 | Matera | 1.00 | 67,033 | - | - | - | 2 | 10 | predicted (travel demand) |
| 259 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 260 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 261 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 262 | Bari | 0.98 | 86,456 | 4 | - | - | 8 | 30 | measured |
| 263 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 264 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 265 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 266 | Belgrade | 1.48 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 267 | Thessaloniki | 1.48 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 268 | Philadelphia | 1.34 | 405,294 | 1 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 269 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 270 | Ferrara | 0.74 | 27,490 | 5 | 1 | 1 | 7 | 20 | measured |
| 271 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 272 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 273 | Regensburg | 1.18 | 51,930 | - | - | - | 2 | 10 | predicted (travel demand) |
| 274 | Riga | 1.23 | 108,918 | 5 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 275 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 276 | Bucharest | 1.23 | 136,836 | 4 | - | 1 | - | 20 | measured |
| 277 | Menorca | 0.73 | - | 4 | - | - | 4 | 10 | published, never ranked (may be uncrawled) |
| 278 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 279 | Zaragoza | 0.74 | 87,580 | 7 | - | 1 | - | 20 | measured |
| 280 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 281 | Sofia | 0.74 | 138,710 | 4 | - | - | - | 30 | measured |
| 282 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 283 | Breda | 0.49 | 36,579 | 4 | - | 1 | 119 | 20 | measured |
| 284 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 285 | Rothenburg ob der Tauber | 0.77 | 39,879 | 4 | - | 1 | 8 | 10 | published, never ranked (may be uncrawled) |
| 286 | Luxembourg City | 0.60 | 64,851 | 10 | - | 2 | 18 | 10 | published, never ranked (may be uncrawled) |
| 287 | Savannah | 0.76 | 128,162 | 2 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 288 | Antwerp | 0.74 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 289 | Gdansk | 0.49 | 4,908 | 6 | 4 | - | 288 | 20 | measured |
| 290 | Leipzig | 0.49 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 291 | Modena | 0.44 | 51,698 | 5 | - | 1 | 3 | 10 | published, never ranked (may be uncrawled) |
| 292 | Ottawa | 0.49 | - | 8 | - | 1 | 119 | 20 | measured |
| 293 | Salzburg | 0.49 | 107,243 | 5 | - | - | 34 | 20 | measured |
| 294 | Coimbra | 0.36 | 34,962 | 4 | - | - | 5 | 10 | published, never ranked (may be uncrawled) |
| 295 | Rouen | 0.54 | 72,334 | 12 | - | 1 | 6 | 10 | published, never ranked (may be uncrawled) |
| 296 | Maui | 0.58 | - | 4 | - | - | 3 | 10 | published, never ranked (may be uncrawled) |
| 297 | Charleston | 0.55 | 155,987 | 2 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 298 | Cesky Krumlov | 0.34 | 28,582 | 6 | 2 | - | 11 | 10 | published, never ranked (may be uncrawled) |
| 299 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 300 | Parma | 0.25 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 301 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 302 | Bamberg | 0.24 | 28,716 | 4 | 3 | 1 | 10 | 10 | published, never ranked (may be uncrawled) |
| 303 | Assisi | 0.17 | 30,278 | 6 | 1 | 2 | 6 | 10 | published, never ranked (may be uncrawled) |
| 304 | George Town | 0.28 | 36,080 | - | - | - | - | 10 | predicted (travel demand) |
| 305 | Hawaii | 0.25 | - | 6 | - | 1 | 6 | 30 | measured |
| 306 | Cologne | 0.25 | 191,812 | 5 | - | 1 | - | 30 | measured |
| 307 | Queenstown | 0.16 | 36,672 | - | - | - | - | 10 | predicted (travel demand) |
| 308 | Buenos Aires | 0.12 | 333,331 | 4 | - | - | - | 30 | measured |
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

