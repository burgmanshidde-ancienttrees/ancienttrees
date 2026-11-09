# St. Louis verify pass, 2026-11-04

Result: 6 trees delivered to data/research/st-louis-verified.json (stl_001 to stl_006), leads and blocked in data/leads/st-louis.json. The pass stopped on supply: no named old tree could be placed beyond park level elsewhere.

Naming bodies found
- Missouri Department of Conservation champion list. Public ArcGIS layer (no licence recorded, facts only): https://gisblue.mdc.mo.gov/arcgis/rest/services/Land_Cover/Champion_Trees_List/MapServer/0 ; query with where=COUNTY LIKE 'St. Louis%', outSR=4326 gives girth (in), height (ft), spread, points, public location, public access, point geometry. Coordinates are fuzzed to site level (the Bellefontaine elm sits ~500 m from the marker).
- Tower Grove Park's own GPS interactive map (https://www.towergroveparkmap.org): a Drupal page that embeds mapPinGeoJSON with coordinates for every stop, including a 10-stop Tree Walk (category 13) on the east side: American beech, hophornbeam, Austrian pine, bald cypress, chestnut oak, English oak, osage-orange, rock elm, tuliptree, white fir. Per-tree pages at /<slug>. Owner of the ground, so one source is enough in the US.
- Missouri Botanical Garden trees page (owner of the ground): oldest tree (bald cypress c. 1874 from a coring project), Scotch elm c. 1913, stout ginkgo (possibly Shaw 1861), Osage-oranges from the 1860s.
- HMdb marker 62186 (Great St. Louis Tree Hunt #9, American elm, Bellefontaine): reachable only via web.archive.org; gives the marker lat/lon 38.68742,-90.22607 and the 2010 MDC measurements.

Hosts
- missouribotanicalgarden.org: WebFetch fails TLS ("unable to verify the first certificate"); curl -sk works. hmdb.org: 403 to WebFetch, archive copy works via curl, content has non-UTF8 bytes (decode with errors=ignore). Overpass not tried. Wikidata SPARQL works (curl with UA) but returned zero tree items within 25 km.
- stltoday hidden-gems page: needs the trailing slash http:// URL.

Judgement notes
- Ticketed share: two MBG trees (basswood, bald cypress) of six is a third.
- The Bellefontaine champion shingle oak (removed 2022) and the Tower Grove "Keebler Elf" catalpa (removed June 2022) are dead; do not publish. Stale articles still describe both as standing.
- Bellefontaine elm is a FORMER champion (lost the title in May 2017 to a Johnson County tree) and has no recent observation; flagged on the aliveness. The latest source describing it as standing is stlmag, updated Feb 2025.
- Tower Grove Osage-oranges: the park map pin is a CIRCLE planted as a carriage turnaround; the "oldest trees" grouping is near the Music Stand and its location is not on the map (stlmag puts it near the Piper Palm House, 1.1 km from the pin). Do not merge the two.
- MBG basswood figures conflict (MDC 158 in / 87 ft vs the Garden page 149 in / 103 ft).
- St. Louis is not a place of ancient trees (coal-smoke era, 1904 fair clearing, DED). Honest supply is big champions and Shaw's 1860s to 1880s plantings. Writers should not invent age.
- Not examined: Compton Hill, Lafayette Park, Carondelet Park, Grant's Farm, Jefferson Barracks, Shaw Nature Reserve (Gray Summit, 60 km), Calvary Cemetery (nothing sourced), WashU Arbor Walk tree by tree (trees.wustl.edu).
- The brief said deliver to stlouis-verified.json; the caller's instruction (st-louis-verified.json) was followed.
