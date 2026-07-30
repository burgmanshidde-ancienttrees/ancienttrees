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


## Japan scouting for the register layer, 2026-07-30 (two research passes, verified by download where stated)

The register layer (two-layer model, DECISIONS.md 2026-07-29) needs sources that are official, licensed for commercial-leaning reuse, and ideally carry coordinates. Japan, as the pilot:

**National level:**
- **国指定文化財等データベース (kunishitei.bunka.go.jp), Agency for Cultural Affairs.** 967 Natural Monuments + 75 Special Natural Monuments (plants, animals AND geology; the individual-tree subset is likely a few hundred, exact count unverified). Browsable with CSV export of search results. Per-record map pages exist; whether the CSV carries lat/long is UNVERIFIED, and designations often cover an area, so imported pins will structurally be `approximate`. Licence: the site defers to MEXT terms, which state conformity with 政府標準利用規約 2.0, CC BY 4.0 compatible, commercial use allowed; IMAGES are explicitly excluded (third-party rights). One duty before shipping: read kunishitei's own /top/policy page in full; its footer boilerplate says "All Rights Reserved" and the umbrella-terms reading must survive that. **Pilot backbone.**
- **環境省 巨樹・巨木林データベース (kyoju.biodic.go.jp).** ~64,500 giant trees (girth >= 3m), GIS downloads exist on biodic's shapedata page. Licence 公共データ利用規約 PDL 1.0 (attribution required, modifications stated, commercial OK), with the explicit carve-out that USER-SUBMITTED content stays with contributors. Decades-old records in places, no accessibility info per entry, so hard rule 10 filtering is manual. **The later volume layer, not the pilot.**
- **国土数値情報 P32 (MLIT, prefectural designations as points).** REJECTED: terms say 非商用 (non-commercial), data is 2014, and Tokyo/Nara/Oita are withheld at those prefectures' own request.

**Prefecture detail (verified by download):**
- **Tokyo: the best source found anywhere so far, now imported (2026-07-30).** 文化財一覧 CSV, licence field literally CC-BY-4.0 (confirmed via the catalog's own `package_show` API, `license_id: CC-BY-4.0`). 248 rows, 35 天然記念物, WITH populated 緯度/経度 columns (all 35). Shift_JIS encoding. **Two access notes for whoever touches this next**: the dataset's own HTML page (catalog.data.metro.tokyo.lg.jp/dataset/...) is behind an AWS WAF bot-challenge and returns empty to a plain fetch; the CKAN API (`/api/3/action/package_show?id=...`) is not, and gave clean JSON including the direct CSV url (`www.opendata.metro.tokyo.lg.jp/suisyoudataset/130001_cultural_property.csv`, note the `www.` and the domain rename from the plain `opendata.metro.tokyo.lg.jp` this file previously recorded, which no longer resolves). **Built `data/registers/tokyo.json`, 28 trees**, filtered from the 35 Natural Monument rows: 3 excluded as non-tree geological designations (a limestone cave, a limestone-outcrop area, a rock dike), 4 more excluded per hard rule 10 because the register's own owner field names a private individual and this dataset doesn't independently confirm public access (left out rather than guessed at, the same "when in doubt, leave it out" discipline layer 1 uses). All 28 kept entries are owned by a religious corporation, a school, a ward/town government or the Metropolitan government itself. Every entry `location_precision: approximate` (register coordinates are institution/address-level, e.g. two trees at the same temple share one lat/long, not individually surveyed). Municipal 保存樹木 CSVs (Mitaka, Suginami, Chofu) also CC BY, not yet imported. Not yet wired into the explore map; that is the next build-order step.
- **Nara: CC BY list, no coordinates.** 県指定文化財一覧 XLSX (pref.nara.lg.jp), 715 properties, 64 天然記念物, town-level addresses only; prefecture deliberately withholds coordinates (same grounds as its P32 opt-out). Treat as a lead list: geocode only what is clearly public and signposted, per hard rule 10. Nara City's own CSV is name-only, near-useless.
- **Kyoto: effectively no itemized open data.** The prefectural cultural-property DB lives inside a GIS with no export and no open licence (all-rights-reserved by default); Kyoto City's portal has zero cultural-property datasets. Kyoto register data = verification-only source, like monumentaltrees.
- **Kyushu/Hokuriku (Ishikawa, Fukuoka, Miyazaki, Kagoshima), scouted 2026-07-30: all four dead ends at the sub-national level, same shape as Kyoto.** Checked both the prefecture and the major city (Kanazawa, Fukuoka, Miyazaki, Kagoshima) in every case, via each area's BODIK ODCS open-data catalog plus its own dedicated cultural-properties site, searching for 天然記念物/巨樹/巨木/名木. None has a downloadable, coordinate-bearing, openly-licensed dataset:
  - **Ishikawa/Kanazawa, closest of the four but still disqualified on licence.** Kanazawa's and the prefecture's open-data catalogs return zero relevant datasets, but a dedicated site exists, いしかわ文化財ナビ (bunkazainavi.pref.ishikawa.lg.jp), a searchable prefectural cultural-properties database with a 天然記念物 filter and an apparent CSV-export button. Its terms page (`/userpolicy2`) has no licence statement beyond "Copyright (c) Ishikawa Prefecture. All Rights Reserved," no CC BY, no 政府標準利用規約, no 二次利用 clause anywhere. All-rights-reserved by default, disqualified; coordinate coverage not even checked, moot given the licence.
  - **Fukuoka: browse-only, no export, no licence page.** fukuoka-bunkazai.jp's natural-monument section is list/map-only (no CSV/Excel/GeoJSON, no visible coordinates), and no terms-of-use page exists anywhere on the site. Both the prefecture's and city's BODIK catalogs return zero results for any tree-register search term.
  - **Miyazaki: plain HTML list, no coordinates, no reuse terms.** The prefectural digital museum's 天然記念物 list gives town-level addresses only, footer says "All right reserved," no licence. BODIK catalogs (prefecture and city, the city's otherwise CC BY 4.0) return zero results for a tree register specifically.
  - **Kagoshima: plain HTML list; the source itself disclaims currency.** The prefectural board of education's list has no CSV or coordinates, "All Rights Reserved," and the page states outright it does not maintain current information about the monuments, pointing back to individual owners/managers. BODIK catalogs return zero results.
  
  Net: none of the four adds an import candidate; the backbone stays exactly the two national sources above. Treat all four as scouted and closed, same as Kyoto, not "not yet scouted."

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

## Licence check round one, 2026-07-26: the Dutch register is non-commercial

First licence actually read, via the Bomenstichting's own IPT page: the Landelijk Register Monumentale Bomen is published under **CC-BY-NC 4.0**, 10,012 records, coordinates included. Non-commercial, and this project's recorded destination is commercial (premium, revenue). So the register can never be the data backbone of the product.

What it still is: a research lead list. Finding a candidate in the register, then verifying existence, species, age and position against two independent sources and writing our own story is our normal bar anyway, and it is not republishing the database. What it is not: a source to import coordinates from at scale.

The general lesson, which reshuffles the register ranking for import purposes: **NGO registers protect, government registers open.** Bomenstichting is NC, the Woodland Trust hides locations and its terms sit unread behind a download flow, the Tree Council of Ireland's terms are unknown. Meanwhile government sources (Italy's MASAF registry, the Flanders heritage inventory, Paris open data) are typically published under open licences that allow commercial reuse. For anything we import rather than merely consult, government sources first, and read every licence before touching the data.

Dense-Netherlands remains viable despite the NC register: Dutch municipalities publish their own tree data as government open data (Amsterdam's gemeente among them), and the register stays a lead list. Checked for the licence only; the municipal licences still need reading per city.
