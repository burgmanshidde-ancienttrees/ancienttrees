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
