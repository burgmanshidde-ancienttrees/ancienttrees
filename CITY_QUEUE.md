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
| 1 | Rome | 43.38 | 358,876 | 29 | 9 | 2 | 32 | 30 | measured |
| 2 | Palermo | 37.30 | 124,310 | 18 | 7 | 2 | 41 | 20 | measured |
| 3 | Barcelona | 33.85 | 346,477 | 46 | 12 | 7 | 183 | 30 | measured |
| 4 | Amsterdam | 31.22 | 294,030 | 31 | 7 | 2 | 5488 | 30 | measured |
| 5 | Lisbon | 27.77 | 201,877 | 33 | 10 | 3 | 66 | 30 | measured |
| 6 | Prague | 27.57 | 303,350 | 17 | 13 | 3 | 29 | 30 | measured |
| 7 | Florence | 18.65 | 184,099 | 22 | 7 | 3 | 27 | 30 | measured |
| 8 | Vienna | 24.12 | 283,090 | 27 | 13 | 5 | 378 | 30 | measured |
| 9 | Paris | 21.89 | 524,268 | 30 | 9 | 4 | 129 | 30 | measured |
| 10 | Milan | 16.01 | 212,705 | 19 | 9 | 2 | 25 | 30 | measured |
| 11 | Singapore | 19.87 | 967,821 | 18 | 3 | 2 | 165 | 30 | measured |
| 12 | Bath | 26.76 | 144,950 | 5 | 1 | 1 | - | 20 | measured |
| 13 | London | 26.56 | 718,291 | 23 | 10 | 1 | - | 30 | measured |
| 14 | Dublin | 15.20 | 240,850 | 17 | 4 | 2 | 12 | 30 | measured |
| 15 | Naples | 13.18 | 198,913 | 20 | 3 | 3 | 46 | 20 | measured |
| 16 | Malaga | 16.42 | 117,780 | 10 | 5 | 2 | - | 30 | measured |
| 17 | Valencia | 12.16 | 162,209 | 16 | 2 | 2 | 350 | 30 | measured |
| 18 | Geneva | 16.01 | 162,269 | 18 | 4 | 4 | 130 | 20 | measured |
| 19 | Cambridge | 23.31 | 97,974 | 5 | 2 | 1 | - | 20 | measured |
| 20 | Brussels | 15.20 | 176,863 | 23 | 4 | 1 | 436 | 30 | measured |
| 21 | Porto | 10.74 | 120,415 | 27 | 5 | 2 | 40 | 20 | measured |
| 22 | Madrid | 14.19 | 274,553 | 17 | 10 | 2 | - | 20 | measured |
| 23 | Boston | 20.68 | 385,902 | 10 | 1 | 1 | - | 30 | measured |
| 24 | The Hague | 9.73 | 236,723 | 16 | 1 | 3 | 166 | 20 | measured |
| 25 | New York | 18.45 | 1,124,326 | 20 | 5 | 2 | - | 30 | measured |
| 26 | Seville | 8.31 | 170,545 | 20 | 6 | 2 | - | 20 | measured |
| 27 | Washington DC | 16.62 | 606,731 | 14 | 1 | 2 | - | 20 | measured |
| 28 | Venice | 10.14 | 267,527 | 11 | 6 | 1 | 4 | 30 | measured |
| 29 | Budapest | 15.41 | 283,807 | 12 | 1 | 3 | - | 30 | measured |
| 30 | Sintra | 9.32 | 46,889 | 5 | 3 | 1 | 6 | 20 | measured |
| 31 | Dubrovnik | 13.99 | 119,586 | 4 | 1 | 1 | 2 | 20 | measured |
| 32 | Bari | 8.65 | 86,456 | - | - | - | 8 | 10 | predicted (travel demand) |
| 33 | Seoul | 13.99 | 206,265 | 8 | 5 | 1 | - | 30 | measured |
| 34 | Hawaii | 12.39 | - | 6 | - | 1 | 6 | 10 | predicted (travel demand) |
| 35 | Granada | 8.51 | 86,361 | 10 | 3 | 2 | 4 | 20 | measured |
| 36 | Lyon | 8.31 | 136,951 | 12 | 3 | 1 | 156 | 20 | measured |
| 37 | Houston | 12.22 | - | - | - | - | - | 10 | predicted (travel demand) |
| 38 | Cologne | 12.17 | 191,812 | - | - | - | - | 10 | predicted (travel demand) |
| 39 | Leiden | 6.08 | 33,227 | 14 | 4 | 1 | 129 | 20 | measured |
| 40 | Munich | 8.11 | 224,067 | 29 | 13 | 6 | 76 | 30 | measured |
| 41 | Girona | 7.87 | 51,072 | - | - | - | - | 10 | predicted (travel demand) |
| 42 | Bristol | 11.76 | 163,983 | 5 | 1 | - | - | 20 | measured |
| 43 | Tokyo | 7.09 | 394,702 | 10 | 8 | - | 7 | 20 | measured |
| 44 | Bilbao | 7.72 | 133,133 | 4 | - | 1 | - | 10 | predicted (travel demand) |
| 45 | Ottawa | 7.62 | - | 8 | - | 1 | 119 | 10 | predicted (travel demand) |
| 46 | Chiang Mai | 11.42 | 66,541 | - | - | - | - | 10 | predicted (travel demand) |
| 47 | Jerusalem | 11.17 | 314,788 | - | - | - | - | 10 | predicted (travel demand) |
| 48 | Copenhagen | 11.15 | 218,621 | 16 | - | 2 | - | 30 | measured |
| 49 | Bologna | 6.49 | 146,161 | 12 | 7 | 2 | 9 | 20 | measured |
| 50 | Dubai | 11.02 | 334,167 | - | - | - | - | 10 | predicted (travel demand) |
| 51 | Padua | 6.28 | 54,592 | 10 | 4 | 1 | 12 | 20 | measured |
| 52 | Edinburgh | 10.54 | 292,981 | 15 | 4 | 1 | - | 30 | measured |
| 53 | Utrecht | 5.27 | 67,963 | 5 | 4 | 1 | 342 | 20 | measured |
| 54 | Kansas City | 10.51 | - | - | - | - | - | 10 | predicted (travel demand) |
| 55 | Asheville | 10.45 | - | - | - | - | - | 10 | predicted (travel demand) |
| 56 | Berlin | 6.89 | 412,181 | 18 | 11 | 1 | 195 | 30 | measured |
| 57 | Hamburg | 10.27 | 191,221 | - | - | - | - | 10 | predicted (travel demand) |
| 58 | Groningen | 5.07 | 31,401 | 5 | - | 1 | 75 | 20 | measured |
| 59 | Bali | 9.95 | - | - | - | - | - | 10 | predicted (travel demand) |
| 60 | Reykjavik | 9.93 | 166,789 | 4 | - | 1 | - | 20 | measured |
| 61 | Haarlem | 4.87 | 33,960 | 4 | - | - | 284 | 20 | measured |
| 62 | Krakow | 6.49 | 140,824 | 16 | 3 | 3 | 198 | 30 | measured |
| 63 | Santorini | 9.63 | - | - | - | - | - | 10 | predicted (travel demand) |
| 64 | Vancouver | 9.47 | 351,552 | - | - | - | - | 10 | predicted (travel demand) |
| 65 | Edmonton | 9.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 66 | Oslo | 9.32 | 181,113 | 4 | - | - | - | 20 | measured |
| 67 | Turku | 9.24 | - | - | - | - | - | 10 | predicted (travel demand) |
| 68 | Winnipeg | 9.21 | - | - | - | - | - | 10 | predicted (travel demand) |
| 69 | Canberra | 9.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 70 | Cork | 6.08 | 101,405 | 5 | 2 | - | - | 20 | measured |
| 71 | Portland | 6.08 | 217,222 | 10 | 1 | 1 | 282 | 20 | measured |
| 72 | Manchester | 9.06 | 316,438 | - | - | - | - | 10 | predicted (travel demand) |
| 73 | Tampere | 8.78 | - | - | - | - | - | 10 | predicted (travel demand) |
| 74 | Pisa | 5.85 | 52,174 | - | - | - | - | 10 | predicted (travel demand) |
| 75 | Nice | 8.72 | 136,877 | 10 | 6 | 2 | - | 30 | measured |
| 76 | Leipzig | 8.60 | 121,319 | - | - | - | - | 10 | predicted (travel demand) |
| 77 | Genoa | 4.66 | 145,206 | 10 | 1 | 1 | 11 | 20 | measured |
| 78 | Taipei | 8.38 | 143,193 | - | - | - | - | 10 | predicted (travel demand) |
| 79 | Salamanca | 5.50 | 47,897 | - | - | - | 1 | 10 | predicted (travel demand) |
| 80 | Hiroshima | 5.55 | 129,791 | - | - | - | - | 10 | predicted (travel demand) |
| 81 | Kyoto | 5.47 | 142,353 | 18 | 8 | 2 | - | 20 | measured |
| 82 | Adelaide | 8.14 | 139,166 | - | - | - | - | 10 | predicted (travel demand) |
| 83 | Alicante | 4.05 | 77,454 | 10 | 2 | 1 | 44 | 20 | measured |
| 84 | Maastricht | 4.05 | 47,763 | 5 | - | - | 140 | 20 | measured |
| 85 | Rotterdam | 4.05 | 104,938 | 5 | - | 1 | 83 | 20 | measured |
| 86 | San Francisco | 8.08 | 361,111 | - | - | - | - | 10 | predicted (travel demand) |
| 87 | Lucca | 3.85 | 52,271 | 10 | 3 | 1 | 27 | 20 | measured |
| 88 | Nijmegen | 3.85 | 42,338 | 5 | - | 1 | 159 | 20 | measured |
| 89 | Turin | 3.85 | 147,456 | 10 | 7 | 2 | 30 | 20 | measured |
| 90 | Osaka | 5.07 | 163,112 | 4 | 1 | - | - | 30 | measured |
| 91 | Luang Prabang | 7.49 | 24,534 | - | - | - | - | 10 | predicted (travel demand) |
| 92 | Oahu | 5.23 | - | - | - | - | 21 | 10 | predicted (travel demand) |
| 93 | Buenos Aires | 7.33 | 333,331 | - | - | - | - | 10 | predicted (travel demand) |
| 94 | Kauai | 7.33 | - | - | - | - | - | 10 | predicted (travel demand) |
| 95 | Bergen | 7.30 | 82,940 | - | - | - | - | 10 | predicted (travel demand) |
| 96 | Cadiz | 4.87 | 79,226 | 5 | 4 | 1 | - | 20 | measured |
| 97 | Zurich | 7.30 | 140,788 | 4 | - | - | - | 20 | measured |
| 98 | Istanbul | 7.20 | 333,027 | 14 | 4 | 1 | - | 30 | measured |
| 99 | Glasgow | 7.10 | 253,705 | 4 | 2 | - | - | 30 | measured |
| 100 | Hong Kong | 4.66 | 689,212 | 10 | 2 | 1 | 505 | 20 | measured |
| 101 | Gyeongju | 6.94 | 30,260 | - | - | - | - | 10 | predicted (travel demand) |
| 102 | Siena | 4.62 | 57,436 | - | - | - | - | 10 | predicted (travel demand) |
| 103 | Santiago de Compostela | 4.52 | 93,477 | - | - | - | - | 10 | predicted (travel demand) |
| 104 | Liverpool | 6.46 | 248,189 | - | - | - | - | 10 | predicted (travel demand) |
| 105 | Zagreb | 6.42 | 122,890 | - | - | - | - | 10 | predicted (travel demand) |
| 106 | Dresden | 6.41 | 113,624 | - | - | - | - | 10 | predicted (travel demand) |
| 107 | Bogota | 6.39 | 1,623 | - | - | - | - | 10 | predicted (travel demand) |
| 108 | Shanghai | 6.38 | 277,140 | - | - | - | - | 10 | predicted (travel demand) |
| 109 | Rio de Janeiro | 6.36 | 279,431 | - | - | - | - | 10 | predicted (travel demand) |
| 110 | Antwerp | 6.28 | 128,289 | 10 | 4 | 1 | - | 20 | measured |
| 111 | Athens | 6.28 | 235,429 | 12 | 6 | 2 | - | 30 | measured |
| 112 | Helsinki | 6.28 | 148,908 | 8 | 1 | - | - | 30 | measured |
| 113 | Detroit | 6.26 | - | - | - | - | - | 10 | predicted (travel demand) |
| 114 | Freiburg | 6.18 | 92,752 | - | - | - | - | 10 | predicted (travel demand) |
| 115 | Setubal | 3.45 | 22,582 | 10 | 1 | 2 | 13 | 20 | measured |
| 116 | Gothenburg | 5.95 | 119,991 | - | - | - | - | 10 | predicted (travel demand) |
| 117 | Denver | 5.83 | - | - | - | - | - | 10 | predicted (travel demand) |
| 118 | Malta | 5.79 | - | - | - | - | - | 10 | predicted (travel demand) |
| 119 | Beijing | 5.73 | 269,737 | - | - | - | - | 10 | predicted (travel demand) |
| 120 | Alice Springs | 5.71 | - | - | - | - | - | 10 | predicted (travel demand) |
| 121 | Breda | 2.84 | 36,579 | 4 | - | 1 | 119 | 20 | measured |
| 122 | Caserta | 2.84 | 14,783 | 20 | - | 2 | 51 | 20 | measured |
| 123 | Funchal | 3.77 | 174,351 | - | - | - | - | 10 | predicted (travel demand) |
| 124 | Sacramento | 5.66 | - | - | - | - | - | 10 | predicted (travel demand) |
| 125 | Bruges | 5.60 | 106,902 | - | - | - | - | 10 | predicted (travel demand) |
| 126 | Vilnius | 3.70 | 113,188 | 10 | 1 | 1 | 34 | 10 | published, never ranked (may be uncrawled) |
| 127 | Avignon | 5.54 | 64,047 | - | - | - | - | 10 | predicted (travel demand) |
| 128 | San Diego | 5.53 | 214,939 | - | - | - | - | 10 | predicted (travel demand) |
| 129 | Galway | 3.65 | 88,162 | - | - | - | - | 10 | predicted (travel demand) |
| 130 | Phuket | 5.46 | 5,487 | - | - | - | - | 10 | predicted (travel demand) |
| 131 | Rovaniemi | 5.38 | - | - | - | - | - | 10 | predicted (travel demand) |
| 132 | Guimaraes | 2.84 | 26,203 | 6 | 1 | 1 | 19 | 20 | measured |
| 133 | Philadelphia | 5.34 | 405,294 | - | - | - | - | 10 | predicted (travel demand) |
| 134 | Aarhus | 5.23 | 52,722 | 7 | 1 | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 135 | Trieste | 2.64 | 117,233 | 10 | 1 | 2 | 43 | 20 | measured |
| 136 | Sapporo | 3.51 | 88,633 | - | - | - | - | 10 | predicted (travel demand) |
| 137 | Warsaw | 3.45 | 197,929 | 7 | 3 | - | 1416 | 30 | measured |
| 138 | Salt Lake City | 5.16 | - | - | - | - | - | 10 | predicted (travel demand) |
| 139 | Lagos | 3.43 | 34,452 | - | - | - | - | 10 | predicted (travel demand) |
| 140 | Lund | 5.14 | - | - | - | - | - | 10 | predicted (travel demand) |
| 141 | Las Vegas | 4.82 | - | 8 | - | 2 | - | 10 | published, never ranked (may be uncrawled) |
| 142 | Kobe | 3.40 | 54,798 | - | - | - | - | 10 | predicted (travel demand) |
| 143 | Cardiff | 5.08 | - | - | - | - | - | 10 | predicted (travel demand) |
| 144 | Heraklion | 4.96 | 66,359 | - | - | - | - | 10 | predicted (travel demand) |
| 145 | Marseille | 4.96 | 182,033 | - | - | - | - | 10 | predicted (travel demand) |
| 146 | Sydney | 4.92 | 305,304 | 6 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 147 | Lausanne | 4.90 | 68,242 | - | - | - | - | 10 | predicted (travel demand) |
| 148 | Riga | 4.90 | 108,918 | - | - | - | - | 10 | predicted (travel demand) |
| 149 | Oxford | 4.87 | 111,583 | 5 | 1 | 1 | - | 20 | measured |
| 150 | Split | 4.87 | 132,399 | 4 | - | 1 | - | 20 | measured |
| 151 | Den Bosch | 2.43 | 39,682 | 11 | 1 | 1 | 119 | 20 | measured |
| 152 | Christchurch | 4.83 | 104,874 | - | - | - | - | 10 | predicted (travel demand) |
| 153 | Nagoya | 3.17 | 83,437 | - | - | - | 1 | 10 | predicted (travel demand) |
| 154 | Miami | 4.74 | 278,558 | - | - | - | - | 10 | predicted (travel demand) |
| 155 | Palma de Mallorca | 2.84 | 84,075 | 5 | 1 | 1 | 8 | 20 | measured |
| 156 | Auckland | 4.67 | 152,056 | - | - | - | - | 10 | predicted (travel demand) |
| 157 | Zaragoza | 2.84 | 87,580 | 7 | - | 1 | - | 20 | measured |
| 158 | Basel | 4.59 | 105,838 | - | - | - | - | 10 | predicted (travel demand) |
| 159 | Cordoba | 2.84 | 74,675 | 15 | 2 | 2 | 3 | 20 | measured |
| 160 | Frankfurt | 4.51 | 150,379 | 6 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 161 | Menorca | 2.93 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 162 | Bergamo | 2.43 | 52,933 | 8 | 1 | 1 | 17 | 20 | measured |
| 163 | New Orleans | 4.43 | 256,232 | - | - | - | - | 10 | predicted (travel demand) |
| 164 | Tasmania | 4.41 | - | - | - | - | - | 10 | predicted (travel demand) |
| 165 | Naha | 2.84 | 24,466 | - | - | - | 1 | 10 | predicted (travel demand) |
| 166 | Bordeaux | 2.84 | 156,201 | 10 | - | 2 | 211 | 20 | measured |
| 167 | Ravenna | 2.77 | 86,471 | - | - | - | 1 | 10 | predicted (travel demand) |
| 168 | San Sebastian | 2.80 | 367 | - | - | - | - | 10 | predicted (travel demand) |
| 169 | Belfast | 4.15 | 224,315 | - | - | - | - | 10 | predicted (travel demand) |
| 170 | Perth | 4.10 | 180,478 | 6 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 171 | Tel Aviv | 4.09 | 177,885 | - | - | - | - | 10 | predicted (travel demand) |
| 172 | Stuttgart | 4.08 | 112,789 | - | - | - | - | 10 | predicted (travel demand) |
| 173 | Arnhem | 2.03 | 31,478 | 4 | 1 | - | 206 | 20 | measured |
| 174 | Interlaken | 4.06 | 24,936 | - | - | - | - | 10 | predicted (travel demand) |
| 175 | Salzburg | 2.71 | 107,243 | - | - | - | 33 | 10 | predicted (travel demand) |
| 176 | Como | 2.03 | 82,645 | 9 | 2 | 1 | 23 | 20 | measured |
| 177 | Azores | 2.62 | - | - | - | - | - | 10 | predicted (travel demand) |
| 178 | Kanazawa | 2.53 | 25,778 | - | - | - | 2 | 10 | predicted (travel demand) |
| 179 | Stockholm | 3.85 | 188,184 | 4 | 3 | - | - | 30 | measured |
| 180 | Nantes | 3.83 | 67,689 | - | - | - | - | 10 | predicted (travel demand) |
| 181 | Kuala Lumpur | 3.80 | 191,800 | - | - | - | - | 10 | predicted (travel demand) |
| 182 | Taormina | 2.35 | 33,169 | - | - | - | 5 | 10 | predicted (travel demand) |
| 183 | Niagara Falls | 3.68 | - | - | - | - | - | 10 | predicted (travel demand) |
| 184 | Los Angeles | 3.60 | 665,559 | 7 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 185 | Austin | 3.65 | 226,631 | - | - | - | - | 10 | predicted (travel demand) |
| 186 | Strasbourg | 2.43 | 154,700 | 10 | 1 | 2 | 66 | 30 | measured |
| 187 | Perugia | 1.82 | 42,572 | 10 | - | 2 | 19 | 20 | measured |
| 188 | Wellington | 3.60 | 132,267 | - | - | - | - | 10 | predicted (travel demand) |
| 189 | Rothenburg ob der Tauber | 3.08 | 39,879 | - | - | - | 8 | 10 | predicted (travel demand) |
| 190 | Bangkok | 3.55 | 222,206 | 5 | 1 | 1 | - | 30 | measured |
| 191 | Belgrade | 3.55 | 178,116 | 4 | 4 | - | - | 20 | measured |
| 192 | Montpellier | 3.47 | 64,238 | - | - | - | - | 10 | predicted (travel demand) |
| 193 | Ljubljana | 3.45 | 125,046 | 4 | - | 1 | - | 30 | measured |
| 194 | Kotor | 3.43 | 48,982 | - | - | - | - | 10 | predicted (travel demand) |
| 195 | Rhodes | 3.42 | 127,205 | - | - | - | - | 10 | predicted (travel demand) |
| 196 | Brighton | 3.40 | 114,108 | - | - | - | - | 10 | predicted (travel demand) |
| 197 | Busan | 3.31 | 94,737 | - | - | - | - | 10 | predicted (travel demand) |
| 198 | Chania | 3.30 | 47,379 | - | - | - | - | 10 | predicted (travel demand) |
| 199 | Segovia | 2.17 | 30,968 | - | - | - | 1 | 10 | predicted (travel demand) |
| 200 | Cape Town | 3.29 | 199,169 | - | - | - | - | 10 | predicted (travel demand) |
| 201 | Santiago | 3.25 | 111,647 | - | - | - | - | 10 | predicted (travel demand) |
| 202 | Sarajevo | 3.15 | 205,074 | - | - | - | - | 10 | predicted (travel demand) |
| 203 | Trento | 1.62 | 56,455 | 10 | 1 | 1 | 20 | 20 | measured |
| 204 | Seattle | 3.11 | 398,724 | 5 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 205 | Lucerne | 3.10 | 66,356 | - | - | - | - | 10 | predicted (travel demand) |
| 206 | Dallas | 3.07 | - | 8 | - | 1 | - | 10 | published, never ranked (may be uncrawled) |
| 207 | Malmo | 3.07 | 103,940 | - | - | - | - | 10 | predicted (travel demand) |
| 208 | Lille | 3.06 | 73,435 | - | - | - | - | 10 | predicted (travel demand) |
| 209 | Savannah | 3.05 | 128,162 | - | - | - | - | 10 | predicted (travel demand) |
| 210 | Brisbane | 2.03 | 162,602 | 10 | 1 | 1 | 186 | 30 | measured |
| 211 | Hobart | 2.03 | 81,734 | 10 | - | 2 | 455 | 20 | measured |
| 212 | Corsica | 3.00 | - | - | - | - | - | 10 | predicted (travel demand) |
| 213 | Sao Paulo | 2.96 | 911 | - | - | - | - | 10 | predicted (travel demand) |
| 214 | Mechelen | 2.93 | 20,707 | - | - | - | - | 10 | predicted (travel demand) |
| 215 | Nuremberg | 1.94 | 161,614 | 10 | 1 | 1 | 39 | 10 | published, never ranked (may be uncrawled) |
| 216 | Ibiza | 1.85 | - | - | - | - | - | 10 | predicted (travel demand) |
| 217 | Inverness | 2.76 | 92,195 | - | - | - | - | 10 | predicted (travel demand) |
| 218 | Modena | 1.77 | 51,698 | - | - | - | 3 | 10 | predicted (travel demand) |
| 219 | Bled | 2.72 | 13,126 | - | - | - | - | 10 | predicted (travel demand) |
| 220 | Cagliari | 1.62 | 51,351 | 7 | 1 | 2 | 9 | 20 | measured |
| 221 | Corfu | 2.71 | 139,334 | - | - | - | - | 10 | predicted (travel demand) |
| 222 | Heidelberg | 2.69 | 75,837 | - | - | - | - | 10 | predicted (travel demand) |
| 223 | Syracuse | 1.75 | 102,833 | - | - | - | - | 10 | predicted (travel demand) |
| 224 | Kamakura | 1.74 | 33,492 | - | - | - | - | 10 | predicted (travel demand) |
| 225 | Cartagena | 2.58 | 65,066 | - | - | - | - | 10 | predicted (travel demand) |
| 226 | Ronda | 1.68 | 51,510 | - | - | - | 1 | 10 | predicted (travel demand) |
| 227 | Innsbruck | 2.52 | 58,742 | - | - | - | - | 10 | predicted (travel demand) |
| 228 | Bern | 2.51 | 90,627 | - | - | - | - | 10 | predicted (travel demand) |
| 229 | Gran Canaria | 1.67 | - | - | - | - | - | 10 | predicted (travel demand) |
| 230 | Mexico City | 2.49 | 566,583 | 9 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 231 | Maui | 2.33 | - | - | - | - | 3 | 10 | predicted (travel demand) |
| 232 | Valletta | 2.45 | 84,342 | - | - | - | - | 10 | predicted (travel demand) |
| 233 | Chicago | 2.43 | 485,769 | 6 | - | - | - | 30 | measured |
| 234 | Faro | 1.62 | 55,645 | - | - | - | - | 10 | predicted (travel demand) |
| 235 | Sofia | 2.43 | 138,710 | 4 | - | - | - | 30 | measured |
| 236 | Capri | 1.60 | - | - | - | - | - | 10 | predicted (travel demand) |
| 237 | Luxembourg City | 2.39 | 64,851 | - | - | - | - | 10 | predicted (travel demand) |
| 238 | Brno | 1.58 | 63,714 | 7 | 1 | 2 | 30 | 10 | published, never ranked (may be uncrawled) |
| 239 | Ghent | 2.36 | 82,757 | - | - | - | - | 10 | predicted (travel demand) |
| 240 | Cusco | 2.35 | 87,732 | - | - | - | - | 10 | predicted (travel demand) |
| 241 | Limerick | 1.57 | 90,379 | - | - | - | - | 10 | predicted (travel demand) |
| 242 | Kilkenny | 1.55 | 34,550 | - | - | - | - | 10 | predicted (travel demand) |
| 243 | Coimbra | 1.44 | 34,962 | - | - | - | 5 | 10 | predicted (travel demand) |
| 244 | Aix-en-Provence | 2.26 | 64,524 | - | - | - | - | 10 | predicted (travel demand) |
| 245 | Verona | 1.42 | 77,646 | 8 | 4 | 2 | 3 | 20 | measured |
| 246 | Charleston | 2.21 | 155,987 | - | - | - | - | 10 | predicted (travel demand) |
| 247 | Rouen | 2.17 | 72,334 | - | - | - | 1 | 10 | predicted (travel demand) |
| 248 | Tarragona | 1.45 | 32,396 | - | - | - | - | 10 | predicted (travel demand) |
| 249 | Gdansk | 1.42 | 4,908 | 4 | 2 | - | 228 | 20 | measured |
| 250 | Potsdam | 1.42 | 51,727 | 4 | - | 1 | 26 | 20 | measured |
| 251 | Toulouse | 1.42 | 112,721 | 10 | - | 1 | 34 | 20 | measured |
| 252 | La Gomera | 1.37 | - | - | - | - | - | 10 | predicted (travel demand) |
| 253 | Leuven | 2.05 | 40,645 | - | - | - | - | 10 | predicted (travel demand) |
| 254 | Pamplona | 1.35 | 128,065 | - | - | - | 1 | 10 | predicted (travel demand) |
| 255 | Ischia | 1.32 | - | - | - | - | 2 | 10 | predicted (travel demand) |
| 256 | Lima | 2.03 | 132,792 | - | - | - | - | 10 | predicted (travel demand) |
| 257 | Thessaloniki | 2.03 | 180,145 | 4 | - | 1 | - | 20 | measured |
| 258 | Delft | 1.01 | 31,293 | 4 | - | 1 | 51 | 20 | measured |
| 259 | Ferrara | 1.22 | 27,490 | 5 | 1 | 1 | 7 | 20 | measured |
| 260 | Hallstatt | 1.99 | 47,271 | - | - | - | - | 10 | predicted (travel demand) |
| 261 | Izmir | 1.88 | 69,826 | - | - | - | - | 10 | predicted (travel demand) |
| 262 | Bucharest | 1.82 | 136,836 | 4 | - | 1 | - | 20 | measured |
| 263 | York | 1.82 | 118,066 | 6 | 2 | 1 | - | 20 | measured |
| 264 | Killarney | 1.20 | 28,763 | - | - | - | - | 10 | predicted (travel demand) |
| 265 | Stirling | 1.78 | 43,558 | - | - | - | - | 10 | predicted (travel demand) |
| 266 | Dijon | 1.72 | 43,526 | - | - | - | - | 10 | predicted (travel demand) |
| 267 | Yakushima | 1.13 | - | - | - | - | 1 | 10 | predicted (travel demand) |
| 268 | Annecy | 1.69 | 56,859 | - | - | - | - | 10 | predicted (travel demand) |
| 269 | Cesky Krumlov | 1.36 | 28,582 | - | - | - | 11 | 10 | predicted (travel demand) |
| 270 | Canterbury | 1.59 | 53,301 | - | - | - | - | 10 | predicted (travel demand) |
| 271 | Mostar | 1.58 | 63,907 | - | - | - | - | 10 | predicted (travel demand) |
| 272 | Trier | 1.56 | 69,369 | - | - | - | - | 10 | predicted (travel demand) |
| 273 | Matera | 1.00 | 67,033 | - | - | - | 2 | 10 | predicted (travel demand) |
| 274 | Sardinia | 0.97 | - | 5 | - | - | 4 | 10 | published, never ranked (may be uncrawled) |
| 275 | Zadar | 1.53 | 71,549 | - | - | - | - | 10 | predicted (travel demand) |
| 276 | Poznan | 1.01 | 65,666 | 10 | - | 1 | 397 | 20 | measured |
| 277 | Parma | 0.81 | 40,425 | 5 | - | 1 | 7 | 20 | measured |
| 278 | Antalya | 1.31 | 70,688 | - | - | - | - | 10 | predicted (travel demand) |
| 279 | Catania | 0.81 | 58,252 | 4 | 3 | 1 | 5 | 20 | measured |
| 280 | Colmar | 1.28 | 45,517 | - | - | - | - | 10 | predicted (travel demand) |
| 281 | Bodrum | 1.26 | 33,918 | - | - | - | - | 10 | predicted (travel demand) |
| 282 | Nafplio | 1.24 | 31,193 | - | - | - | - | 10 | predicted (travel demand) |
| 283 | Regensburg | 1.18 | 51,930 | - | - | - | 2 | 10 | predicted (travel demand) |
| 284 | Quebec City | 0.81 | 124,358 | 6 | - | 1 | 494 | 20 | measured |
| 285 | Tenerife | 0.81 | - | 4 | - | - | - | 20 | measured |
| 286 | Cyprus | 1.18 | - | 4 | - | - | - | 10 | published, never ranked (may be uncrawled) |
| 287 | Evora | 0.78 | 15,345 | - | - | - | - | 10 | predicted (travel demand) |
| 288 | Bamberg | 0.97 | 28,716 | - | - | - | 10 | 10 | predicted (travel demand) |
| 289 | Assisi | 0.68 | 30,278 | - | - | - | 6 | 10 | predicted (travel demand) |
| 290 | Stratford-upon-Avon | 1.10 | 68,555 | - | - | - | - | 10 | predicted (travel demand) |
| 291 | La Palma | 0.70 | - | - | - | - | - | 10 | predicted (travel demand) |
| 292 | Crete | 1.01 | - | 4 | - | - | - | 20 | measured |
| 293 | Fukuoka | 0.61 | 77,485 | 11 | 7 | 1 | 1 | 20 | measured |
| 294 | Oaxaca | 0.95 | 72,955 | - | - | - | - | 10 | predicted (travel demand) |
| 295 | Braga | 0.41 | 34,522 | 4 | 1 | - | 8 | 20 | measured |
| 296 | Bratislava | 0.41 | 132,162 | 6 | - | 1 | 26 | 30 | measured |
| 297 | Melbourne | 0.41 | 267,898 | 12 | - | 2 | 397 | 30 | measured |
| 298 | Windsor | 0.50 | 30,452 | - | - | - | - | 10 | predicted (travel demand) |
| 299 | Sorrento | 0.20 | 40,049 | 4 | - | - | 20 | 20 | measured |
| 300 | Toledo | 0.24 | 3,149 | - | - | - | - | 10 | predicted (travel demand) |
| 301 | Graz | 0.20 | 65,717 | 10 | - | 1 | 87 | 20 | measured |
| 302 | Madeira | 0.20 | - | 6 | - | - | - | 20 | measured |
| 303 | Tallinn | 0.20 | 124,888 | 4 | 1 | 1 | 42 | 20 | measured |
| 304 | Wroclaw | 0.20 | 123,894 | 4 | 1 | 1 | 122 | 20 | measured |
| 305 | George Town | 0.28 | 36,080 | - | - | - | - | 10 | predicted (travel demand) |
| 306 | Toronto | 0.20 | 411,011 | 4 | - | - | - | 30 | measured |
| 307 | Montreal | 0.20 | 315,322 | 7 | - | 1 | - | 30 | measured |
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

