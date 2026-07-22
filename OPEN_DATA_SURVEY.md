# Can open data make the ten trees per city faster to find?

Measured 2026-07-21. The question changed halfway through, and so did the answer.

It started as "can open data get us to every city in the world", which assumed publishing hundreds of trees per city. Hidde rejected that the same day: ten per city is what makes the passport work, and scarcity is the mechanism rather than a limitation. See BACKLOG.md. So the surviving question is narrower and more useful: **can open data cut the dull half of a city run, finding candidates and fixing coordinates, so runs spend their time on stories?**

## Round one: OpenStreetMap, and why it misled

Trees tagged `natural=tree` + `denotation=natural_monument`, counted per city with bounding box queries against the public Overpass API.

| City | Trees | City | Trees |
|---|---|---|---|
| Warsaw | 224 | Barcelona | 30 |
| Paris | 207 | Madrid | 27 |
| Berlin | 90 | London | 19 |
| Vienna | 82 | Rome | 15 |
| | | Tokyo | 10 |
| | | Amsterdam | 4 |

Prague and New York timed out repeatedly; the public endpoint is heavily loaded and those two need retrying.

Note the wider `denotation` tag is useless alone: Berlin carries 35,848 of them, because it also covers ordinary street trees tagged `avenue` or `urban`.

The first conclusion drawn from this table was that OSM works in Central Europe and fails elsewhere. **That conclusion was wrong**, and the error is worth recording because it is easy to repeat: this table measures mapping culture, not tree data availability. Amsterdam does not have four monumental trees, and London does not have nineteen.

## Round two: the national registers, which is where the data actually is

| Source | Size | Format | Notes |
|---|---|---|---|
| UK, Woodland Trust Ancient Tree Inventory | 233,200+ records | Download, free of charge | Citizen science, run with TROBI. Licence terms sit behind the portal's download flow and were not readable without accepting them. |
| Italy, MASAF official registry | 4,944 trees | Shapefile and Excel, by region | Government registry, updated by decree, latest October 2025. |
| Paris, opendata.paris.fr | Hundreds | Open data portal | Already used by the Paris run. |
| Netherlands, Bomenstichting register | Unknown | Unchecked | Thousands are believed to be listed. Amsterdam's OSM count of 4 is clearly not the real number. |

**London went from worst in the OSM table to best available anywhere.** 19 tagged in OSM, over 233,000 records in the national inventory. That single comparison is the finding: judging a country's data by its OSM count is close to meaningless.

## What this means for the work

Use open data as **research input, never as published content**. A run opens a city with a candidate list and coordinates already placed by people who stood in front of the tree, and spends its time on what the site is actually for: verifying, writing, finding photographs. Nothing changes about what ships. Still ten, still fully researched, still two independent sources.

Expect this to cut the finding and coordinate work substantially and to improve pin precision, since register coordinates are usually surveyed rather than estimated. Expect it to do nothing for the writing, which is the real cost and should not be sped up.

Work registers out per country rather than per city. Doing Italy once serves Rome, Florence, Milan and Naples.

## Two things to settle before building on this

**Licences are unresolved.** The UK terms could not be read without going through the download flow, and the Dutch register has not been looked at. Italy is a government registry and Italian public sector data is normally openly licensed, but that was not verified either. None of this is legal advice, and nothing should be imported on the strength of a machine's reading.

**Some trees are deliberately kept off public maps, and this one matters.** The Woodland Trust excludes trees "deliberately hidden from public view" from its public map. That is not bureaucracy: ancient trees are damaged by visitor pressure, soil compaction around roots, climbing and vandalism, and some stand on private land whose owners never agreed to visitors.

This project publishes exact coordinates and actively sends people to stand at the trunk. That is the whole point, and it is also a way to hurt a tree or trespass on someone's land. It falls squarely under question 3 of the mandate, the one that overrides the others: can this hurt anyone other than Hidde.

Nothing here is currently checked for it. Before importing any register, and arguably before the next city ships, decide: do not publish a tree whose source withholds its location, prefer trees that are already publicly signposted, and drop any tree where publishing the pin would plausibly harm it or its owner. Coverage is not worth a damaged tree.

## Next

1. Retry Prague and New York.
2. Read the UK licence terms properly, and find out what the Dutch register offers and under what conditions.
3. Decide the tree-protection rule above. That one does not need to wait for anything.

## Which countries to invest in, weighed 2026-07-21

Researched at Hidde's request: national tree databases plus photo availability and other factors, ranked for the strategy (English site, travelers plus enthusiasts as the audience).

National register quality, on evidence:

| Country | National register | Size and access |
|---|---|---|
| UK | Woodland Trust Ancient Tree Inventory | 233,000, downloadable, one source. Best in the world. |
| Netherlands | Landelijk Register Monumentale Bomen (Bomenstichting) | ~15,000, open data in CSV/GeoJSON with coordinates. Best accessibility after the UK. |
| Ireland | Tree Register of Ireland + Heritage Trees of Ireland | 11,000+, GPS-recorded. |
| Italy | MASAF official registry | 4,944, shapefile and Excel, by region. |
| Belgium | Flanders heritage inventory + Brussels remarkable trees | Regional, with coordinates. |
| France | none national; Paris and Ile-de-France open data | Fragmented, rich where it matters. |
| Germany | none national; per Bundesland, some cities | Fragmented. |
| Spain | none national; regional (Castilla y Leon, Aragon) via datos.gob.es | Fragmented. |

Correction to the earlier OSM-based read: the Netherlands is data-rich, not thin. The OSM count of 4 was mapping culture, not the register, which holds ~15,000.

Photos: not a national property, closer to a per-tree lottery driven by how touristed and Wikimedia-active a place is. Weighted low, because the fix is wider sources (iNaturalist, Flickr, Openverse) and submissions, not country choice.

Other factors that matter: whether a register gives exact coordinates or blurs them (hard rule 10, and it now breaks check-in if vague); seasonality strength (northern and temperate beat Mediterranean for the season chart); existing competition (the UK already has the Woodland Trust map, so we compete on curation); and licence, which is unchecked per country and must be before any import.

Ranked top 10 to invest in:

1. UK, 2. Netherlands, 3. Ireland, 4. Belgium, 5. France, 6. Italy, 7. Germany, 8. Austria, 9. Spain, 10. Japan.

The shape matters more than the order. Three groups:
- Lead group (1-4, UK/Netherlands/Ireland/Belgium): where data, verifiability and reachability meet. All near Hidde, real registers, reachable in person. Invest here.
- Traveler group (5,6,9, France/Italy/Spain): weaker or fragmented data, but they pull the English-speaking traveler who converts. Take the marquee cities, not the whole country.
- Quality group (7,8,10, Germany/Austria/Japan): where the season feature shines and tree culture is richest. Japan is 10th on strategy but would be top three on quality alone, and that tension is a real choice, not something to explain away.

The USA stays out: English is a plus, but its cities are young so "ancient" is thin, and there is no national register.

Not yet done, and gating any import: per-country licence checks, starting with the two leaders, the UK and the Netherlands.
