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
| 1 | Rome | 117.06 | 358,876 | 30 | 9 | 2 | 32 | 30 | measured |
| 2 | Amsterdam | 101.77 | 294,030 | 34 | 7 | 3 | 5488 | 30 | measured |
| 3 | Lisbon | 59.66 | 201,877 | 33 | 10 | 3 | 66 | 30 | measured |
| 4 | Barcelona | 46.37 | 346,477 | 56 | 12 | 7 | 180 | 30 | measured |
| 5 | Milan | 40.11 | 212,705 | 22 | 9 | 2 | 25 | 30 | measured |
| 6 | Tenerife | 48.88 | - | 4 | - | - | - | 20 | measured |
| 7 | Brisbane | 46.87 | 162,602 | 19 | 1 | 2 | 189 | 30 | measured |
| 8 | Seville | 45.37 | 170,545 | 43 | 6 | 2 | - | 20 | measured |
| 9 | Singapore | 45.62 | 967,821 | 28 | 3 | 3 | 165 | 30 | measured |
| 10 | Florence | 30.08 | 184,099 | 23 | 8 | 1 | 27 | 30 | measured |
| 11 | Naples | 29.08 | 198,913 | 24 | 3 | 3 | 46 | 20 | measured |
| 12 | Malaga | 38.10 | 117,780 | 9 | 5 | 1 | - | 30 | measured |
| 13 | Vienna | 36.10 | 283,090 | 32 | 13 | 5 | 376 | 30 | measured |
| 14 | Prague | 35.34 | 303,350 | 17 | 13 | 3 | 29 | 30 | measured |
| 15 | London | 41.11 | 718,291 | 23 | 10 | 1 | - | 30 | measured |
| 16 | Copenhagen | 43.87 | 218,621 | 16 | 1 | 2 | - | 30 | measured |
| 17 | Madeira | 26.32 | - | 6 | 1 | - | - | 20 | measured |
| 18 | Paris | 30.33 | 524,268 | 31 | 9 | 4 | 129 | 30 | measured |
| 19 | Palermo | 22.31 | 124,310 | 21 | 7 | 1 | 37 | 20 | measured |
| 20 | Venice | 22.31 | 267,527 | 11 | 6 | 2 | 4 | 30 | measured |
| 21 | Palma de Mallorca | 23.06 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 22 | Madrid | 22.06 | 274,553 | 17 | 10 | 2 | - | 20 | measured |
| 23 | Alicante | 17.80 | 77,454 | 14 | 2 | 2 | 44 | 20 | measured |
| 24 | Brussels | 23.56 | 176,863 | 30 | 4 | 1 | 436 | 30 | measured |
| 25 | Fukuoka | 22.81 | 77,485 | 13 | 7 | 1 | - | 20 | measured |
| 26 | Valencia | 17.55 | 162,209 | 24 | 2 | 2 | 350 | 30 | measured |
| 27 | Bologna | 18.80 | 146,161 | 12 | 7 | 1 | 9 | 20 | measured |
| 28 | Sardinia | 18.80 | - | 5 | 2 | - | 8 | 20 | measured |
| 29 | Bath | 32.84 | 144,950 | 5 | 1 | 1 | - | 20 | measured |
| 30 | Dublin | 18.55 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 31 | Crete | 27.57 | - | 4 | - | - | - | 20 | measured |
| 32 | Nijmegen | 13.29 | 42,338 | 22 | 1 | 3 | 159 | 20 | measured |
| 33 | Seoul | 24.31 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 34 | New York | 21.81 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 35 | Toronto | 23.81 | 411,011 | 6 | - | - | - | 30 | measured |
| 36 | Kyoto | 15.04 | 142,353 | 17 | 8 | 2 | - | 20 | measured |
| 37 | Leiden | 11.53 | 33,227 | 12 | 4 | 1 | 129 | 20 | measured |
| 38 | Krakow | 14.04 | 140,824 | 34 | 3 | 3 | 198 | 30 | measured |
| 39 | Edinburgh | 20.55 | 292,981 | 15 | 4 | 1 | - | 30 | measured |
| 40 | Las Vegas | 19.55 | - | 11 | - | 2 | - | 30 | measured |
| 41 | Portland | 13.03 | 217,222 | 20 | 1 | 2 | 301 | 20 | measured |
| 42 | Sintra | 9.53 | 46,889 | 5 | 3 | - | 6 | 20 | measured |
| 43 | Utrecht | 9.53 | 67,963 | 33 | 4 | 2 | 345 | 20 | measured |
| 44 | Munich | 12.53 | 224,067 | 45 | 14 | 6 | 80 | 30 | measured |
| 45 | Berlin | 11.53 | 412,181 | 19 | 11 | 1 | 195 | 30 | measured |
| 46 | Porto | 8.52 | 120,415 | 27 | 5 | 2 | 40 | 20 | measured |
| 47 | The Hague | 8.27 | 236,723 | 29 | 1 | 5 | 166 | 20 | measured |
| 48 | Bordeaux | 10.78 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 49 | Vilnius | 10.78 | 113,188 | 14 | 1 | 1 | 34 | 30 | measured |
| 50 | Groningen | 8.02 | 31,401 | 20 | - | 2 | 72 | 20 | measured |
| 51 | Cagliari | 8.52 | 51,351 | 10 | 1 | 2 | 15 | 20 | measured |
| 52 | Tokyo | 8.02 | 394,702 | 10 | 8 | - | 7 | 20 | measured |
| 53 | Montreal | 14.79 | 315,322 | 7 | - | 1 | - | 30 | measured |
| 54 | Sydney | 14.04 | 305,304 | 6 | - | - | - | 30 | measured |
| 55 | Reykjavik | 12.28 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 56 | Seattle | 13.29 | 398,724 | 6 | - | - | - | 30 | measured |
| 57 | Cyprus | 13.54 | - | 4 | - | - | - | 20 | measured |
| 58 | Perth | 13.29 | 180,478 | 6 | 1 | 1 | - | 30 | measured |
| 59 | Athens | 13.03 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 60 | Sorrento | 6.52 | 40,049 | 6 | - | 1 | 20 | 20 | measured |
| 61 | Chicago | 12.53 | 485,769 | 6 | - | - | - | 30 | measured |
| 62 | Cadiz | 7.77 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 63 | Geneva | 8.02 | 162,269 | 21 | 4 | 4 | 131 | 20 | measured |
| 64 | Maastricht | 5.77 | 47,763 | 14 | - | 1 | 137 | 20 | measured |
| 65 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 66 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 67 | Guimaraes | 5.77 | 26,203 | 8 | 1 | 1 | 19 | 20 | measured |
| 68 | Arnhem | 5.51 | 31,478 | 9 | 1 | 1 | 196 | 20 | measured |
| 69 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 70 | Trieste | 5.51 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 71 | Melbourne | 7.27 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 72 | Quebec City | 7.27 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 73 | Hamburg | 10.27 | 191,221 | - | - | - | - | 10 | predicted (travel demand) |
| 74 | Kansas City | 10.51 | - | - | - | - | - | 10 | predicted (travel demand) |
| 75 | Asheville | 10.45 | - | - | - | - | - | 10 | predicted (travel demand) |
| 76 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 77 | Budapest | 9.27 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 78 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 79 | Turku | 9.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 80 | Oahu | 6.27 | - | 8 | - | - | 133 | 20 | measured |
| 81 | Strasbourg | 6.27 | 154,700 | 10 | 1 | 2 | 66 | 30 | measured |
| 82 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 83 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 84 | Canberra | 9.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 85 | Manchester | 9.06 | 316,438 | - | - | - | - | 10 | predicted (travel demand) |
| 86 | Pisa | 5.85 | 52,174 | - | - | - | - | 10 | predicted (travel demand) |
| 87 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 88 | Potsdam | 5.77 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 89 | Taipei | 8.38 | 143,193 | - | - | - | - | 10 | predicted (travel demand) |
| 90 | Salamanca | 5.50 | 47,897 | - | - | - | 1 | 10 | predicted (travel demand) |
| 91 | Boston | 8.02 | 385,902 | 10 | 1 | 1 | - | 30 | measured |
| 92 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 93 | Lyon | 5.51 | 136,951 | 13 | 3 | 1 | 156 | 20 | measured |
| 94 | San Francisco | 8.08 | 361,111 | - | - | - | - | 10 | predicted (travel demand) |
| 95 | Delft | 4.01 | 31,293 | 8 | - | 1 | 63 | 20 | measured |
| 96 | New Orleans | 8.02 | 256,232 | 4 | - | 1 | - | 20 | measured |
| 97 | Helsinki | 6.52 | 148,908 | 8 | 1 | - | 9 | 30 | measured |
| 98 | Cordoba | 5.01 | 74,675 | 16 | 2 | 2 | 3 | 20 | measured |
| 99 | Istanbul | 6.64 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 100 | Nuremberg | 5.01 | 161,614 | 11 | 1 | 1 | 39 | 20 | measured |
| 101 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 102 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 103 | Mexico City | 6.89 | 566,583 | 9 | 1 | - | - | 30 | measured |
| 104 | Glasgow | 6.77 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 105 | Oslo | 6.27 | 181,113 | 4 | - | - | - | 20 | measured |
| 106 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 107 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 108 | Braga | 3.76 | 34,522 | 4 | 1 | - | 8 | 20 | measured |
| 109 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 110 | Bristol | 6.52 | 163,983 | 5 | 1 | - | - | 20 | measured |
| 111 | Liverpool | 6.46 | 248,189 | - | - | - | - | 10 | predicted (travel demand) |
| 112 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 113 | Freiburg | 6.18 | 92,752 | - | - | - | - | 10 | predicted (travel demand) |
| 114 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 115 | Cambridge | 6.52 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 116 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 117 | Cork | 4.26 | 101,405 | 13 | 2 | 1 | - | 20 | measured |
| 118 | Graz | 4.26 | 65,717 | 12 | 3 | 1 | 87 | 20 | measured |
| 119 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 120 | Rio de Janeiro | 6.36 | 279,431 | - | - | - | - | 10 | predicted (travel demand) |
| 121 | Washington DC | 5.77 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 122 | Detroit | 6.26 | - | - | - | - | - | 10 | predicted (travel demand) |
| 123 | Aarhus | 6.02 | 52,722 | 7 | 1 | 1 | - | 30 | measured |
| 124 | Rotterdam | 3.01 | 104,938 | 9 | - | 2 | 83 | 20 | measured |
| 125 | Turin | 3.01 | 147,456 | 11 | 7 | 2 | 30 | 20 | measured |
| 126 | Bilbao | 4.01 | 133,133 | 4 | - | 1 | - | 20 | measured |
| 127 | Bratislava | 4.01 | 132,162 | 6 | - | 1 | 26 | 30 | measured |
| 128 | Gothenburg | 5.95 | 119,991 | - | - | - | - | 10 | predicted (travel demand) |
| 129 | Oxford | 5.77 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 130 | Beijing | 5.73 | 269,737 | - | - | - | - | 10 | predicted (travel demand) |
| 131 | Denver | 5.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 132 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 133 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 134 | Sacramento | 5.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 135 | Warsaw | 3.76 | 197,929 | 18 | 3 | 2 | 1445 | 30 | measured |
| 136 | Bruges | 5.60 | 106,902 | - | - | - | - | 10 | predicted (travel demand) |
| 137 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 138 | Catania | 3.26 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 139 | Verona | 3.26 | 77,646 | 8 | 4 | 1 | 3 | 20 | measured |
| 140 | San Diego | 5.53 | 214,939 | - | - | - | - | 10 | predicted (travel demand) |
| 141 | Caserta | 2.76 | 14,783 | 20 | - | 1 | 51 | 20 | measured |
| 142 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 143 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 144 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 145 | Dubrovnik | 5.01 | 119,586 | 4 | 1 | - | 2 | 20 | measured |
| 146 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 147 | Cardiff | 5.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 148 | Salt Lake City | 5.16 | - | - | - | - | - | 10 | predicted (travel demand) |
| 149 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 150 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 151 | Auckland | 4.67 | 152,056 | - | - | - | - | 10 | predicted (travel demand) |
| 152 | Lausanne | 4.90 | 68,242 | - | - | - | - | 10 | predicted (travel demand) |
| 153 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 154 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 155 | Brno | 3.26 | 63,714 | 8 | 2 | 2 | 34 | 20 | measured |
| 156 | Poznan | 3.26 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 157 | Tallinn | 3.26 | 124,888 | 4 | 2 | 1 | 42 | 20 | measured |
| 158 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 159 | Austin | 4.76 | 226,631 | 5 | - | - | - | 20 | measured |
| 160 | Osaka | 3.01 | 163,112 | 4 | 1 | - | - | 30 | measured |
| 161 | York | 4.76 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 162 | Miami | 4.74 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 163 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 164 | Stuttgart | 4.08 | 112,789 | - | - | - | - | 10 | predicted (travel demand) |
| 165 | Lucca | 2.26 | 52,271 | 14 | 3 | 1 | 27 | 20 | measured |
| 166 | Dallas | 4.51 | - | 8 | 1 | 1 | - | 30 | measured |
| 167 | Frankfurt | 3.01 | 150,379 | 6 | 1 | - | - | 30 | measured |
| 168 | Hobart | 3.01 | 81,734 | 10 | - | 2 | 455 | 20 | measured |
| 169 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 170 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 171 | Padua | 2.26 | 54,592 | 12 | 4 | 1 | 12 | 20 | measured |
| 172 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 173 | Belfast | 4.15 | 224,315 | - | - | - | - | 10 | predicted (travel demand) |
| 174 | Hong Kong | 2.76 | 689,212 | 10 | 2 | 1 | 505 | 20 | measured |
| 175 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 176 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 177 | Granada | 2.51 | 86,361 | 9 | 3 | 2 | 4 | 20 | measured |
| 178 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 179 | Nantes | 3.83 | 67,689 | - | - | - | - | 10 | predicted (travel demand) |
| 180 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 181 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 182 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 183 | Los Angeles | 3.60 | 665,559 | 8 | 2 | - | - | 10 | published, never ranked (may be uncrawled) |
| 184 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 185 | Houston | 3.51 | - | 4 | - | - | - | 30 | measured |
| 186 | Brighton | 3.40 | 114,108 | - | - | - | - | 10 | predicted (travel demand) |
| 187 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 188 | Busan | 3.31 | 94,737 | - | - | - | - | 10 | predicted (travel demand) |
| 189 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 190 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 191 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 192 | Toulouse | 2.26 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 193 | Girona | 1.97 | 51,072 | 7 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 194 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 195 | Nice | 3.26 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 196 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 197 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 198 | Sao Paulo | 2.96 | 911 | - | - | - | - | 10 | predicted (travel demand) |
| 199 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 200 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 201 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 202 | Heidelberg | 2.69 | 75,837 | - | - | - | - | 10 | predicted (travel demand) |
| 203 | Como | 1.50 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 204 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 205 | Den Bosch | 1.50 | 39,682 | 11 | 1 | 1 | 119 | 20 | measured |
| 206 | Haarlem | 1.50 | 33,960 | 21 | - | 2 | 277 | 20 | measured |
| 207 | Trento | 1.50 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 208 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 209 | Genoa | 1.50 | 145,206 | 12 | 1 | 1 | 11 | 20 | measured |
| 210 | Ibiza | 1.85 | - | - | - | - | - | 10 | predicted (travel demand) |
| 211 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 212 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 213 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 214 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 215 | Lima | 2.03 | 132,792 | - | - | - | - | 10 | predicted (travel demand) |
| 216 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 217 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 218 | Ghent | 2.36 | 82,757 | - | - | - | - | 10 | predicted (travel demand) |
| 219 | Bari | 1.50 | 86,456 | 4 | - | - | 8 | 30 | measured |
| 220 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 221 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 222 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 223 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 224 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 225 | Dresden | 1.60 | 113,624 | 5 | 1 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 226 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 227 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 228 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 229 | Setubal | 1.25 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 230 | Hallstatt | 1.99 | 47,271 | - | - | - | - | 10 | predicted (travel demand) |
| 231 | Stockholm | 1.75 | 188,184 | 4 | 3 | - | - | 30 | measured |
| 232 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 233 | Split | 2.26 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 234 | Leipzig | 1.50 | 121,319 | 7 | 7 | 1 | - | 30 | measured |
| 235 | Sofia | 1.50 | 138,710 | 4 | - | - | - | 30 | measured |
| 236 | Zurich | 2.01 | 140,788 | 4 | - | - | - | 20 | measured |
| 237 | Hiroshima | 1.39 | 129,791 | 8 | - | 2 | - | 10 | published, never ranked (may be uncrawled) |
| 238 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 239 | Leuven | 2.05 | 40,645 | - | - | - | - | 10 | predicted (travel demand) |
| 240 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 241 | Bangkok | 2.01 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 242 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 243 | Perugia | 1.00 | 42,572 | 12 | - | 2 | 19 | 20 | measured |
| 244 | Wroclaw | 1.25 | 123,894 | 5 | 1 | 1 | 121 | 20 | measured |
| 245 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 246 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 247 | Ljubljana | 1.75 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 248 | Yakushima | 1.13 | - | - | - | - | 1 | 10 | predicted (travel demand) |
| 249 | Matera | 1.00 | 67,033 | - | - | - | 2 | 10 | predicted (travel demand) |
| 250 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 251 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 252 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 253 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 254 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 255 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 256 | Belgrade | 1.50 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 257 | Bergamo | 0.75 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 258 | Thessaloniki | 1.50 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 259 | Parma | 0.75 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 260 | Sapporo | 0.88 | 88,633 | 6 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 261 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 262 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 263 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 264 | Regensburg | 1.18 | 51,930 | - | - | - | 2 | 10 | predicted (travel demand) |
| 265 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 266 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 267 | Nagoya | 0.79 | 83,437 | 6 | - | - | 1 | 10 | published, never ranked (may be uncrawled) |
| 268 | Kauai | 1.00 | - | 6 | - | - | 8 | 20 | measured |
| 269 | Menorca | 0.73 | - | 4 | - | - | 4 | 10 | published, never ranked (may be uncrawled) |
| 270 | Gdansk | 0.75 | 4,908 | 6 | 4 | - | 288 | 20 | measured |
| 271 | Salzburg | 0.75 | 107,243 | 5 | - | - | 34 | 20 | measured |
| 272 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 273 | Naha | 0.71 | 24,466 | 6 | - | - | 1 | 10 | published, never ranked (may be uncrawled) |
| 274 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 275 | Antwerp | 1.00 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 276 | Breda | 0.50 | 36,579 | 4 | - | 1 | 119 | 20 | measured |
| 277 | Bucharest | 1.00 | 136,836 | 4 | - | 1 | - | 20 | measured |
| 278 | Kanazawa | 0.63 | 25,778 | 7 | - | 1 | 2 | 10 | published, never ranked (may be uncrawled) |
| 279 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 280 | Luxembourg City | 0.60 | 64,851 | 10 | - | 2 | 18 | 10 | published, never ranked (may be uncrawled) |
| 281 | Rothenburg ob der Tauber | 0.75 | 39,879 | 4 | - | 1 | 8 | 20 | measured |
| 282 | Ferrara | 0.50 | 27,490 | 5 | 1 | 1 | 7 | 20 | measured |
| 283 | Segovia | 0.54 | 30,968 | 6 | - | 1 | 5 | 10 | published, never ranked (may be uncrawled) |
| 284 | Savannah | 0.76 | 128,162 | 2 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 285 | Zaragoza | 0.50 | 87,580 | 7 | - | 1 | - | 20 | measured |
| 286 | Cologne | 0.75 | 191,812 | 5 | - | 1 | - | 30 | measured |
| 287 | Ottawa | 0.50 | - | 8 | - | 1 | 119 | 20 | measured |
| 288 | Modena | 0.44 | 51,698 | 5 | - | 1 | 3 | 10 | published, never ranked (may be uncrawled) |
| 289 | Ronda | 0.42 | 51,510 | 6 | - | - | 9 | 10 | published, never ranked (may be uncrawled) |
| 290 | Kamakura | 0.44 | 33,492 | 6 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 291 | Buenos Aires | 0.63 | 333,331 | 4 | - | - | - | 30 | measured |
| 292 | Maui | 0.58 | - | 4 | - | - | 3 | 10 | published, never ranked (may be uncrawled) |
| 293 | Rouen | 0.54 | 72,334 | 12 | - | 1 | 6 | 10 | published, never ranked (may be uncrawled) |
| 294 | Tarragona | 0.36 | 32,396 | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 295 | Charleston | 0.55 | 155,987 | 2 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 296 | Pamplona | 0.34 | 128,065 | 6 | - | - | 1 | 10 | published, never ranked (may be uncrawled) |
| 297 | Cesky Krumlov | 0.34 | 28,582 | 6 | 2 | - | 11 | 10 | published, never ranked (may be uncrawled) |
| 298 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 299 | Coimbra | 0.25 | 34,962 | 4 | - | - | 5 | 20 | measured |
| 300 | Assisi | 0.25 | 30,278 | 6 | 1 | 2 | 6 | 20 | measured |
| 301 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 302 | Bamberg | 0.24 | 28,716 | 4 | 3 | 1 | 10 | 10 | published, never ranked (may be uncrawled) |
| 303 | George Town | 0.28 | 36,080 | - | - | - | - | 10 | predicted (travel demand) |
| 304 | Hawaii | 0.25 | - | 6 | - | 1 | 6 | 30 | measured |
| 305 | Philadelphia | 0.25 | 405,294 | 1 | - | - | - | 20 | measured |
| 306 | Riga | 0.25 | 108,918 | 5 | - | - | - | 20 | measured |
| 307 | Vancouver | 0.25 | 351,552 | 4 | - | - | - | 30 | measured |
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

