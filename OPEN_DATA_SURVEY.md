# Can open data make the ten trees per city faster to find?

Measured 2026-07-21. The question changed halfway through, and so did the answer.

It started as "can open data get us to every city in the world", which assumed publishing hundreds of trees per city. Hidde rejected that the same day: ten per city is what makes the passport work, and scarcity is the mechanism rather than a limitation. See BACKLOG.md. So the surviving question is narrower and more useful: **can open data cut the dull half of a city run, finding candidates and fixing coordinates, so runs spend their time on stories?**

## Spain: the regional registers, scouted 2026-08-04

Spain has no national register; every autonomous community keeps its own, and they differ in quality, licence and whether the file even downloads. Scouted for the cities we publish and the ones we might.

**The fastest way to find them, worth reusing for any country:** the datos.gob.es API returns every regional dataset in one call with licence and download URL attached, `https://datos.gob.es/apidata/catalog/dataset/title/árboles singulares` with the accents URL-encoded. Three registers below surfaced there and in no ordinary web search.

**USABLE, licence verified against the holder's own metadata:**
- **Navarra**, 47 named trees, per-tree coordinates, and a per-tree official PDF fact sheet, which is a second-source generator in itself. Shapefile at `https://idena.navarra.es/descargas/BIODIV_Sym_MonumNat.zip`. The ISO metadata inside the download states CC BY 4.0 and the required wording: "Información geográfica propiedad del Gobierno de Navarra." A companion layer covers 8 trees in the Pamplona river park, a walkable cluster on its own.
- **Aragon**, 45 singular trees and 13 groves region-wide, CC BY 4.0 per `opendata.aragon.es`, which states commercial use explicitly. Served through IDEAragon; the GeoNetwork record was returning a server error, so the direct file URL still needs resolving through their download portal. Note the count: 45 for the whole region means one or two inside Zaragoza.
- **Illes Balears**, 78 trees, CC BY per the holder's CKAN metadata, GeoJSON and CSV both downloadable. **But the export carries a single attribute, the year catalogued: no name, no species, no municipality.** As shipped it is 78 dots. The attributes presumably live on the regional WFS. Not usable until that is resolved.

**THE TRAP, and it is a good one.** Castilla y Leon publishes two datasets on the same portal, same subject, different licences. "Arboles singulares en espacios naturales" is CC BY 4.0 and is the one to use, though every download URL was 404 during the scout and the page itself said the service was temporarily unavailable. "Mapa de Arboles Singulares de Castilla y Leon" carries **IGCYL-NC**, whose terms authorise only non-commercial use, which disqualifies it outright under our rules. Anyone finding the second one first would import a licence we cannot use.

**Needs a human, ranked by what they would unlock:** Comunitat Valenciana has a Catalogo de Arboles Monumentales y Singulares covering Valencia and Alicante, licence unchecked, and is the obvious next scout. Las Palmas de Gran Canaria has a municipal catalogue of 326 specimens, the largest single count found anywhere in this scan and city-scale. Cantabria has 214 catalogued trees browsable per municipality with no open distribution. Asturias runs an ArcGIS Hub, which would give GeoJSON out of the box, but its dataset record came back empty. Murcia, Extremadura and La Rioja all have real catalogues behind PDFs or a Cloudflare challenge.

**Not worth the effort:** Castilla-La Mancha declares about ten singular trees in the whole region, none near a city we would publish.

## Japan: the Environment Ministry giant-tree database (scouted 2026-08-04, VERDICT: usable with one real caveat)

`https://kyoju.biodic.go.jp/`, the 巨樹・巨木林データベース, the national record of every tree in Japan over 300 cm girth at breast height, with measured girth, height, species, and location. It is the closest thing Japan has to Portugal's ICNF, and it is the spine of any cheap layer-two coverage for Japanese cities.

**Licence, with the proving sentence.** The Biodiversity Centre's terms page (`https://www.biodic.go.jp/copyright/terms_of_service.html`) states that its content may be used under 「公共データ利用規約（第1.0版）」（PDL1.0）, the Public Data License 1.0, which permits commercial reuse with attribution and which CLAUDE.md already names as an acceptable register licence. Attribution must give the title, 環境省生物多様性センター, and the URL or download date; any editing or adaptation must be stated separately along with who did it.

**The caveat, and it is a real one.** The same page carves out user submissions by name: 「いきものログ」及び「巨樹・巨木林データベース」ウェブサイトの投稿情報... 著作権は投稿者に帰属します. Copyright in posted content belongs to the poster. The database mixes two things: the ministry's own national survey data from 1988 and 2000, which is Centre content under PDL 1.0, and citizen reports submitted through the site since, which are not. The interface does not obviously separate them.

**Working position for runs.** Use it, and use it carefully:
- Treat measurements, species and coordinates as facts, which they are, and which carry no copyright in themselves.
- Never copy submitted prose, observation reports or photographs from the site. Photographs in particular belong to their posters and fall outside PDL 1.0 entirely.
- Attribute as the terms require, and record in the register file which survey or page each record came from.
- Where a record is clearly a recent citizen report rather than survey data, treat it as a lead to verify elsewhere, not as an importable record.

That is enough to build the second layer for Japanese cities at near-zero cost, which was the open question blocking the Japan plan.

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
- **国指定文化財等データベース (kunishitei.bunka.go.jp), Agency for Cultural Affairs.** 967 Natural Monuments + 75 Special Natural Monuments (plants, animals AND geology; the individual-tree subset is likely a few hundred, exact count unverified). Browsable with CSV export of search results. Per-record map pages exist; whether the CSV carries lat/long is still UNVERIFIED, and designations often cover an area, so imported pins will structurally be `approximate`. **Licence, actually read 2026-07-30, and weaker than this entry previously assumed**: `/top/policy` (linked from `/bsys/about`, not the `/bsys/top/policy` path this file previously guessed, which 404s) states text may be freely reused with attribution ("出典を記載の上、自由にご利用ください"), with no reference anywhere on the page to 政府標準利用規約, CC BY, or any named open-licence framework, and the same page's footer carries a blanket "Copyright (c) 1997 Agency for Cultural Affairs, Government of Japan, All Rights Reserved." Images separately require per-work permission (third-party rights). This is genuinely ambiguous rather than a clean pass: "free to use with attribution" reads permissive and states no non-commercial restriction, but it is not the explicit, named licence text hard rule (register layer) asks for, and sits directly under a boilerplate all-rights-reserved notice the way Tokyo's own catalog page did before its CKAN API's explicit `license_id: CC-BY-4.0` field settled that case cleanly. **Do not import from this source on this reading alone.** Before it can be the pilot backbone: (1) find whether the database exposes the same licence commitment in a more explicit, structured place (an API/CKAN-style metadata field the way Tokyo's did, rather than page prose), or (2) treat the ambiguity as disqualifying per "when in doubt, leave it out" and look elsewhere for the national backbone. CSV-export mechanics and coordinate presence are also still unverified; a plain WebFetch only reaches the static search-form shell, not exported results, so confirming either needs a session that can drive the actual search/export interaction, not just read markup.
- **環境省 巨樹・巨木林データベース (kyoju.biodic.go.jp).** ~64,500 giant trees (girth >= 3m), GIS downloads exist on biodic's shapedata page. Licence 公共データ利用規約 PDL 1.0 (attribution required, modifications stated, commercial OK), with the explicit carve-out that USER-SUBMITTED content stays with contributors. Decades-old records in places, no accessibility info per entry, so hard rule 10 filtering is manual. **The later volume layer, not the pilot.**
- **国土数値情報 P32 (MLIT, prefectural designations as points).** REJECTED: terms say 非商用 (non-commercial), data is 2014, and Tokyo/Nara/Oita are withheld at those prefectures' own request.

**Prefecture detail (verified by download):**
- **Tokyo: the best source found anywhere so far, now imported (2026-07-30).** 文化財一覧 CSV, licence field literally CC-BY-4.0 (confirmed via the catalog's own `package_show` API, `license_id: CC-BY-4.0`). 248 rows, 35 天然記念物, WITH populated 緯度/経度 columns (all 35). Shift_JIS encoding. **Two access notes for whoever touches this next**: the dataset's own HTML page (catalog.data.metro.tokyo.lg.jp/dataset/...) is behind an AWS WAF bot-challenge and returns empty to a plain fetch; the CKAN API (`/api/3/action/package_show?id=...`) is not, and gave clean JSON including the direct CSV url (`www.opendata.metro.tokyo.lg.jp/suisyoudataset/130001_cultural_property.csv`, note the `www.` and the domain rename from the plain `opendata.metro.tokyo.lg.jp` this file previously recorded, which no longer resolves). **Built `data/registers/tokyo.json`, 28 trees**, filtered from the 35 Natural Monument rows: 3 excluded as non-tree geological designations (a limestone cave, a limestone-outcrop area, a rock dike), 4 more excluded per hard rule 10 because the register's own owner field names a private individual and this dataset doesn't independently confirm public access (left out rather than guessed at, the same "when in doubt, leave it out" discipline layer 1 uses). All 28 kept entries are owned by a religious corporation, a school, a ward/town government or the Metropolitan government itself. Every entry `location_precision: approximate` (register coordinates are institution/address-level, e.g. two trees at the same temple share one lat/long, not individually surveyed). Municipal 保存樹木 CSVs (Mitaka, Suginami, Chofu) also CC BY, not yet imported. **Wired into the explore map the same day**: a second, unclustered GeoJSON source renders as small hollow grey dots (visually quieter than the curated green/gold trees on purpose), each popup stating the required "From the official register, not yet verified by us." label verbatim, no link out (no own page exists). Areas and the designation label were machine-translated to English for the popup (`area_en` added per entry after catching one address-parsing bug: a naive regex first mis-cut 東村山市/Higashimurayama to 東村, fixed before shipping). Confirmed via the built HTML: all 28 register features present in `explore.html`'s embedded GeoJSON, `python3 scripts/qa.py` and `python3 scripts/smoke_test.py` (headless Chrome, asserts the MapLibre canvas actually renders) both green.
- **Nara: CC BY list, no coordinates.** 県指定文化財一覧 XLSX (pref.nara.lg.jp), 715 properties, 64 天然記念物, town-level addresses only; prefecture deliberately withholds coordinates (same grounds as its P32 opt-out). Treat as a lead list: geocode only what is clearly public and signposted, per hard rule 10. Nara City's own CSV is name-only, near-useless.
- **Kyoto: effectively no itemized open data.** The prefectural cultural-property DB lives inside a GIS with no export and no open licence (all-rights-reserved by default); Kyoto City's portal has zero cultural-property datasets. Kyoto register data = verification-only source, like monumentaltrees.
- **Tokyo's municipal 保存樹木/保護指定樹木 CSVs (Mitaka, Suginami), checked by download 2026-07-30: dead ends, a different shape than the national source.** These are a separate, standardized Tokyo-wide template (found via the same CKAN catalog, confirmed CC-BY-4.0), but the template itself doesn't carry what the register layer needs, not a licence or access problem this time. **Mitaka** (`t132047d2024000003`, CSV at `city.mitaka.lg.jp/c_service/111/attached/attach_111873_1.csv`): 90+ individual rows with a per-tree ID and species, but 緯度/経度 (lat/long) and every address field below city-name level are blank for every row checked, no coordinates to import at any precision. **Suginami** (`t131156d2024000003`, CSV at `opendata.metro.tokyo.lg.jp/suginami/131156_suginamiku_hogoshiteijumoku.csv`): worse still, no per-tree ID at all, just a deduplicated list of species names present somewhere in the ward with a designation-status column reading "不明" (unknown) throughout, a species tally rather than individual tree records. Suginami's separate "公園樹木" (park trees) dataset, which sounded more promising since park trees are unambiguously public, turned out to be served through a dynamic wagmap.jp portal endpoint that returns 404 to both a plain fetch and WebFetch, not a static CSV; unresolved rather than confirmed dead, worth a retry with different tooling. **Chofu has no matching dataset in this catalog at all** (a `樹木` search against its organization id, t132080, returns zero results); the 2026-07-30 entry above that flagged it alongside Mitaka/Suginami as "also CC BY, not yet imported" was not itself verified by download and should be treated as superseded by this entry. Net: this specific "municipal 保存樹木 CSV" lead does not extend Tokyo's register beyond the 28 trees already imported; a future pass should not re-fetch these same three files expecting coordinates to appear. If Tokyo's register layer grows further, the more promising untried thread is still the national kunishitei/kyoju.biodic backbone below, not more municipal preservation-tree lists.
- **The "worth a retry" threads left open above, both closed for real 2026-07-30 (same session, later pass).** Queried the Tokyo CKAN catalog's own `package_search` API for every 保護指定樹木 dataset site-wide (not just Mitaka/Suginami/Chofu): it returns 20+ municipalities on the identical standardized template, Setagaya, Chiyoda, Sumida, Toshima, Katsushika, Fuchu, Kunitachi and more, all CC-BY-4.0. Downloaded and checked six of the largest directly (Setagaya 2,895 rows, Toshima 310, Sumida 160, Katsushika 53, Chiyoda 3, plus Mitaka/Suginami already known): every single one has the 緯度/経度 columns present in the header but blank on every row, and the 画像 (image) column empty on every row too, across all six. This generalizes cleanly: the shared template itself structurally omits coordinates and images citywide, not a per-ward gap worth checking ward by ward. **The 公園樹木 (park trees) dataset's separate wagmap.jp portal endpoint was also retried directly this session (both the generic `/suginami/OpenData` listing and the specific `OpenDataDetail?lid=1500&mids=107` resource URL the catalog API itself returns): both 404, confirming the earlier finding rather than reversing it.** Net: this whole family of Tokyo municipal designated-tree CSVs, roughly 20 files, is now confirmed closed; a future register-layer pass should not re-open it, and should go straight to the national kunishitei/kyoju.biodic backbone if it wants to grow Tokyo's register further.
- **Kyushu/Hokuriku (Ishikawa, Fukuoka, Miyazaki, Kagoshima), scouted 2026-07-30: all four dead ends at the sub-national level, same shape as Kyoto.** Checked both the prefecture and the major city (Kanazawa, Fukuoka, Miyazaki, Kagoshima) in every case, via each area's BODIK ODCS open-data catalog plus its own dedicated cultural-properties site, searching for 天然記念物/巨樹/巨木/名木. None has a downloadable, coordinate-bearing, openly-licensed dataset:
  - **Ishikawa/Kanazawa, closest of the four but still disqualified on licence.** Kanazawa's and the prefecture's open-data catalogs return zero relevant datasets, but a dedicated site exists, いしかわ文化財ナビ (bunkazainavi.pref.ishikawa.lg.jp), a searchable prefectural cultural-properties database with a 天然記念物 filter and an apparent CSV-export button. Its terms page (`/userpolicy2`) has no licence statement beyond "Copyright (c) Ishikawa Prefecture. All Rights Reserved," no CC BY, no 政府標準利用規約, no 二次利用 clause anywhere. All-rights-reserved by default, disqualified; coordinate coverage not even checked, moot given the licence.
  - **Fukuoka: browse-only, no export, no licence page.** fukuoka-bunkazai.jp's natural-monument section is list/map-only (no CSV/Excel/GeoJSON, no visible coordinates), and no terms-of-use page exists anywhere on the site. Both the prefecture's and city's BODIK catalogs return zero results for any tree-register search term.
  - **Miyazaki: plain HTML list, no coordinates, no reuse terms.** The prefectural digital museum's 天然記念物 list gives town-level addresses only, footer says "All right reserved," no licence. BODIK catalogs (prefecture and city, the city's otherwise CC BY 4.0) return zero results for a tree register specifically.
  - **Kagoshima: plain HTML list; the source itself disclaims currency.** The prefectural board of education's list has no CSV or coordinates, "All Rights Reserved," and the page states outright it does not maintain current information about the monuments, pointing back to individual owners/managers. BODIK catalogs return zero results.
  
  Net: none of the four adds an import candidate; the backbone stays exactly the two national sources above. Treat all four as scouted and closed, same as Kyoto, not "not yet scouted."


## The licence-led country scan, 2026-07-30 (verified by download and licence text)

The queue-maker for the register layer (CLAUDE.md rung 5). Verdicts below rest on a fetched licence sentence or a fetched dataset, never on a portal's reputation. Countries still unscanned are named at the end rather than assumed.

### Usable now, licence proven

| Source | Trees | Coordinates | Licence, with the proving evidence |
|---|---|---|---|
| **Portugal, ICNF Arvoredo de Interesse Publico** (si.icnf.pt WFS `BDG:arv_class`, GeoJSON in one unauthenticated GET) | 555 designated (460 single trees; 87 ensembles need the collectible-point test) | Per-tree, median 8 decimals, all inside the country box | CC BY 4.0. ICNF's own metadata: "Sem restricoes. A utilizacao ou divulgacao deste conjunto de dados geograficos requer sempre a indicacao expressa da sua proveniencia e autoria: ICNF." dados.gov.pt returns `license: cc-by`; the WFS itself declares Fees "sem restricoes", AccessConstraints "Nenhum". |
| **Czech Republic, AOPK CR pamatne stromy** (gis.nature.cz ArcGIS REST, `outSR=4326` native) | 16,795 individually positioned; 13,149 with species | Per-tree, WGS84 served directly | CC BY 4.0, verbatim: "Tato datova sada poskytovana Agenturou ochrany prirody a krajiny Ceske republiky podleha licenci Creative Commons Uvedte puvod 4.0 Mezinarodni". Attribution "(c) AOPK CR". |
| **Poland, CRFOP / GDOS** (sdi.gdos.gov.pl WFS, daily updates) | 117,474 tree monuments, the largest verified pool anywhere | Yes, EPSG:2180 needs reprojection; precision unstated so `approximate` by default | CC0 per dane.gov.pl metadata; WFS Fees and AccessConstraints both "brak" (none). WEAKER PROOF: the licence-condition fields are empty and GDOS's own site publishes CC BY-SA 4.0 for site content. Pin the data licence down before importing 117k rows. |
| **Brussels** (opendata.bruxelles.be `bruxelles_arbres_remarquables`) | 582, richest per record: Latin name, circumference, crown, rarity, status, official per-tree page | Yes, WGS84 `geo_point_2d` | CC BY 4.0 (`license_url` on the dataset). Two flags: the inventory surveys private gardens and courtyards, so rule-10 filtering is mandatory; and the `firstimage` photo URLs are NOT covered by the dataset licence, so those are not licensed photos. |

### Blocked, and why (each is fixable, none by guessing)

- **Wallonia, AHREM** (20,245 tree points, the richest schema found: genus, species, cultivar, circumference, height, survey year, decree date). Licence is fine and explicit: "Licence CC-BY 4.0 : L'utilisateur peut utiliser et modifier les donnees... a condition de citer les sources", access "Non restreint". BLOCKED on hard rule 10: the Walloon criterion deliberately includes private trees merely *visible from public space*, the `DOMAINE` field splits 13,007 / 6,985 / 253 across three codes nobody has decoded, and the data model itself admits some points are placed RANDOMLY inside an address perimeter ("Positionnes aleatoirement dans le perimetre defini en adresse"). Read AHREM.pdf's field dictionary first.
- **Catalonia** (302 monumental trees plus a separate 4,176 monumental olives, per-trunk coordinates). BLOCKED on licence: the ISO metadata says only `otherRestrictions`, and the WFS declares no Fees or AccessConstraints at all, so there is no self-declared permission. Do not import until the sentence is found.
- **Spain, four real registers with live download endpoints but no licence sentence yet**: Illes Balears (GeoJSON + CSV, the most import-ready), Comunitat Valenciana (statutory catalogue under Ley 4/2006, SHP + WMS), Castilla y Leon (SHP), Navarra (SHP, but the identifier says polygon so it may be perimeters not trunks). Each needs one page fetched and quoted.
- **Spain dead ends**: Comunidad de Madrid has no machine-readable singular-tree dataset at all (the catalogue is a PDF under Decreto 18/1992); Madrid city publishes only a full bulk inventory, which the semantic filter forbids; Euskadi's singular trees exist legally (Decreto 265/1995) but survive only inside a 1:25,000 protected-areas polygon set whose metadata says `otherRestrictions` and whose download is a 404.
- **Flanders** (4,398 rows, licence fine): NOT RECOMMENDED. Wrong shape and wrong places: only 1,768 are standing trees (the rest hedges, coppice, even farm buildings), geometry is parcel MultiPolygons with no coordinates in the CSV, and coverage is deliberately rural (Voeren 648 versus Antwerp 8, Leuven 16).

### The finding worth copying into every future scan

Catalonia's register ships a vitality field, `DIAGNOSI`, populated on all 302 records: 191 alive, 53 in advanced decline, 58 outright dead (37% dead or dying). A naive import would have put 58 confirmed-dead trees on a map whose promise is standing in front of something alive. **Every register scan from now on looks for a vitality or last-surveyed field before anything else**, and where none exists that alone is a reason to treat the source as a lead list rather than an import.

### Still unscanned (not "no data", just not looked at)

Italy (the ~4,944-tree MASAF national list, the biggest known European prize), Germany (per-Bundesland Naturdenkmal registers), France, and the whole English-speaking group including the UK's 233,000-record Ancient Tree Inventory whose licence remains the single highest-value unanswered question. Also unread: Spain's default reuse regime (RD 1495/2011 art. 8), which would settle four Spanish registers at once.

**2026-08-02: RD 1495/2011 art. 8 checked and it does NOT settle the four Spanish registers.** Its own title says "para el ámbito del sector público estatal" (national/state administration only); Illes Balears, Comunitat Valenciana, Castilla y León and Navarra are all autonomous-community (regional) governments with their own separate reuse regimes, not bound by this decree. Worth one line so a future session doesn't reread it expecting the same shortcut. A search-snippet check of Castilla y León's own open-data portal found a plausible CC BY 4.0 statement on its "Términos de uso de los conjuntos de datos" page, but this project's own standard is reading the primary source directly, not inferring from a snippet (the same rule Japan's register work follows), and `datosabiertos.jcyl.es` failed TLS certificate verification on every fetch attempt this session ("unable to verify the first certificate"), so nothing from it is recorded as proven. Try again from a session whose network handles that certificate, or verify via `datos.gob.es`'s own metadata for the specific singular-trees dataset instead of the portal's own pages.

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

## Imported 2026-08-05: Italy and Andalusia, both CC BY 4.0

**Italy, MASAF national register.** 21 regional .xls files from
https://www.masaf.gov.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/11260, one
identical schema, 5,008 rows, of which 4,522 single trees and 485 marked
"Insieme omogeneo di ..." (a homogeneous set: an avenue or a stand, not a
collectible point). 1,653 of the singles carry the register's own CONTESTO
URBANO flag, which filters city trees for free. Coordinates are sexagesimal
text with a comma decimal; converted on import and cross-checked against
Sicily's decimal GeoJSON republication, where 156 of 159 agree to the metre and
the three that do not are re-surveys between the 2021 and 2025 versions.
Licence proof: the Sicilian republication of the same data carries
`license_id: cc-by` in its portal metadata (dati.regione.sicilia.it, dataset
alberi-monumentali-di-sicilia). The photo gallery on masaf.gov.it is explicitly
NOT under that licence. Data yes, images never.

**Andalusia, REDIAM.** Eight province KML files (arb_sing_<province>.kml) from
portalrediam.cica.es, 749 individual trees, decimal WGS84, and 435 of them link
to an official per-tree PDF sheet, which is the cheapest verification path in
Spain. The companion groves layer (arbda_sing_*) is deliberately not imported.
Licence proof, from the dataset's own GeoNetwork record
(uuid c5d37ec9-a857-42b2-a8d2-2e0d4b947a4e, "Inventario de arboles y arboledas
singulares de Andalucia"): "Creative Commons Attribution 4.0 International
Public License (CC BY 4.0)". The Junta mixes CC BY, CC BY-NC and CC BY 3.0
across its portal, so this proof covers this dataset and nothing else from that
source.

Neither register is on the explore map yet: load_registers() in build_site.py
still only understands the Japanese `trees` + `prefecture` shape, so both files
are read by tree_index.py and cluster_register.py and ignored by the map. That
is a wiring job, not a licence question.

### Campania's regional cards: the second source MASAF cannot give you (found 2026-08-05)

MASAF has no age field at all, which is the single biggest gap in the Italian
register. Campania publishes a per-tree card at
`agricoltura.regione.campania.it/foreste/monum/scheda_NNN.html` carrying an age
estimate, its own coordinates and a short description. The Caserta pass scraped
schede 180-299 and matched 40 of them to register entries, which supplied the
second source for nearly every tree in one go. The same pattern is worth
checking region by region: **MASAF gives you the tree, the regional register
gives you the age and the story.**

Two warnings from the same pass. The two registers disagree on coordinates for
the same tree by up to 400 metres, and MASAF hands one identical coordinate to
four different Caserta trees, so nothing there could honestly be marked
`confirmed`. And where MASAF prints a girth for a multi-stemmed tree, the
regional card sometimes reveals it as *insieme dei fusti*, every stem added
together: publishing the MASAF number alone would have invented a 6.5 m trunk
for the Reggia's sweet osmanthus.

### PDFs are readable after all, and the recipe (2026-08-05)

A scouting pass concluded that "tooling, not searching, is now the bottleneck":
Seville's 390-page municipal catalogue would not open, pypdf choked on its xref,
and the machine has no pdftotext, mutool, qpdf or ghostscript. Two of those three
statements were wrong.

`pdfminer` IS installed alongside pypdf and reads these documents fine. What
actually failed was the download: the Seville file is 36 MB and the fetch came
back with 19 MB and an HTTP 200, so every parser then died on a truncated xref
rather than on a hard PDF. The recipe that works:

    curl -sL -m 300 -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
      --retry 2 "$URL" -o out.pdf
    python3 -c "from pdfminer.high_level import extract_text; print(extract_text('out.pdf'))"

Check the tail before parsing: a complete PDF ends in %%EOF. A file that does not
is a short download, not a broken document, and the fix is a longer timeout
rather than a different library.

**Seville, Inventario de Arboles Singulares de la Ciudad de Sevilla (2022),
confirmed readable.** Its per-tree template carries species, common name, family,
catalogue number and date, **titularidad (ownership, which answers hard rule 10
row by row)**, Arbomap id, emplazamiento, barrio, distrito, **WGS84 coordinates**,
full dendrometry (perimeter at 1.30 m and at base, height, height to first branch,
crown diameters N-S and E-O, lean and its direction) and both physiological and
phytosanitary condition. That last pair is the closest thing to a vitality field
found in any register so far. It is a municipal document distinct from, and denser
than, the Andalusian REDIAM catalogue already imported.

### Friuli Venezia Giulia, scouted 2026-08-05 while researching Trieste

`decreti.regione.fvg.it/Storage/2025_71/ALLEGATO1%20AL%20DPREG%20071-2025.PDF`,
"Elenco regionale degli alberi monumentali 2025" (DPReg 071/2025), all four
provinces. Over the national MASAF file it adds LOCALITA, a real place name
rather than a coordinate, which is what turns a point into a walk; CRITERI DI
MONUMENTALITA, the legal reason for the designation; and NUMERO ELEMENTI, which
separates single trees from stands. It has no age field and no vitality field,
the same gap as MASAF, and no removed-trees sheet the way Lazio has. A 2020
edition exists and diffing it against 2025 is the closest thing to a vitality
signal here. The open-data mirror at dati.friuliveneziagiulia.it refuses
anonymous reads, so the decree PDF is the usable channel.

Running total on Italian regional registers: Campania publishes per-tree cards
with ages, Lazio publishes criteria, notes and a removed-trees sheet, Friuli
publishes criteria and place names but no age. **No Italian source at any level
carries an age**, which is why the newspaper step now sits above the register in
the search order.

### Piemonte breaks that rule, scouted and imported 2026-08-05 while researching Turin

The sentence above is no longer true, and Piemonte is the exception that proves
where to look. Regione Piemonte publishes **Alberi Monumentali del Piemonte: dati
del censimento** on the regional Geoportale, inside the Sistema Conoscenze
Ambientali catalogue, as a live WFS and WMS rather than as a file drop.

**Licence, CC BY 4.0.** The proving sentence is on the metadata record for
`r_piemon:9410f966-96b4-41ee-8f4c-ccdb60167218`: the dataset is released under
Creative Commons Attribution 4.0
(https://creativecommons.org/licenses/by/4.0/deed.it), with access limitation per
INSPIRE Directive art. 13(1)(a). Attribution required, commercial reuse not
restricted. Imported in full to `data/registers/piemonte-alberi-monumentali.json`,
391 trees, on 2026-08-05.

WFS: `https://gisserver.territorio.csi.it/geoserver/decsiraogc_geo_alb_monum/wfs`
(typeName `decsiraogc_geo_alb_monum:AlberiMonumentaliLoc`, add
`outputFormat=application/json&srsName=EPSG:4326` and it answers plain GeoJSON).

Two fields make this the best Italian register found so far:

- **`eta_presunta`, a presumed age**, as a band rather than a figure: `< 100`,
  `100-200`, `> 200`, `Non applicabile`. Populated on 344 of 391. A band is not a
  date, but it separates a 200-year tree from a 120-year one, which is the
  distinction a page actually needs and which MASAF cannot make at all.
- **`descr_stato`, a removal status held inline**, which is Italy's usual missing
  vitality field: 378 listed, 11 removed for natural death, 2 removed by felling.
  Lazio publishes the same information as a separate sheet; Piemonte keeps it in
  the same layer, so a live query is self-cleaning.

Also carried: `oggetto_di_identif`, which mechanically separates ALBERO SINGOLO
from GRUPPO, VIALE ALBERATO, FILARE SINGOLO and FILARE DOPPIO, so avenues and
stands filter out without reading names; `tipo_proprieta` (Pubblica / Privata /
Sia pubblica che privata), which settles hard rule 10 without a site visit;
girth, measured height, mean crown diameter, and a link to the ministerial decree.

Two cautions. **MASAF's national file for Torino repeats these coordinates and
girths exactly**, so national and regional are one survey and not two independent
sources; the second source still has to come from outside the register. And the
register id encodes the comune (L219 is Torino), so trees the local press counts
as a city's are sometimes filed under a neighbour: Turin's count reads 14, 15 or
16 depending on who is counting, and the difference is a downy oak on the Colle
della Maddalena filed under an adjoining municipality.

So the corrected rule for Italy: **the age question is regional, not national, and
it is worth one WFS call before assuming a newspaper is the only route to a date.**

### Liguria has an age field, which no Italian national source does (2026-08-06)

Found by the Genoa verification pass. `agriligurianet.it` carries Liguria's own
monumental-tree register, CC BY, distinct from the national MASAF file, and it
records an age. It dated the Villa Serra hop-hornbeam to 160-170 years, the only
sourced age in a batch of ten where every other figure is a girth-based estimate.

Running total on Italian regional registers, and the pattern is now clear enough
to plan around: **the age question is regional, never national.** Campania
publishes per-tree cards with ages. Piemonte publishes presumed age bands on 344
of 391 trees plus removal status inline. Liguria publishes an age. Lazio
publishes designation criteria and a separate sheet of removed trees. Friuli
publishes criteria and place names but no age. Lombardia publishes nothing per
tree, and its cities publish per-tree municipal pages instead. So the first
question for any Italian city is not "what does MASAF say" but "what does this
region publish", and MASAF is the index rather than the source.

Not yet imported. Worth a proper scout: it would give age to Genoa, Savona,
Imperia and La Spezia at once.
