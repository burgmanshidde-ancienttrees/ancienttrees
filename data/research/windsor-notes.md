# Windsor verify pass, 2026-11-02 (stopped early: session usage limit hit)

Result: 0 trees verified. Nothing shipped. Leads and one block in data/leads/windsor.json.

## Searched, what yielded
- Wikipedia Windsor Great Park and King Offa's Oak (WebFetch): Offa's Oak is in a private area, so blocked. Conqueror's Oak is mentioned in Cranbourne Park, no figures.
- Official park map and guide PDF (https://www.windsorgreatpark.co.uk/wp-content/uploads/2023/02/Windsor-Great-Park-map-and-guide..pdf, downloaded to out/tmp/wsr/guide.pdf, text extracted with pypdf): open daily dawn to dusk, free, areas marked private on the map must be respected. Savill Garden is a paid garden, no dogs. Tree-level content: none. Gates: Cranbourne Gate SL4 2BY, Forest Gate, Queen Anne's Gate SL4 2BQ, Bishops Gate, Ranger's Gate SL4 2LD. The map's private-area shading is graphic only, so it must be viewed to place any oak.
- Queen's Green Canopy 70 Ancient Trees page: Signing Oak, 900 years, Windsor Great Park, nothing else.
- englandspuzzle.com Windsor oaks: Conqueror's Oak/King's Oak, Victoria Oak (did not survive), Herne's Oak (original lost, replanted early 1900s, per a comment only). Weak source.
- Tree Register 2021 news: nearly 400 TROBI champions at Valley Gardens, Savill Garden and Chapel Wood Arboretum, but no named champion or figures found.

## Not done (ran out of usage)
- Individual champion trees in Valley Gardens/Savill Garden (look at TROBI champion lists, Historic England list entry 1001176, parksandgardens.org).
- Herne's Oak replacement in Home Park (access?), Eton, Windsor Castle environs, Virginia Water.
- Geograph and Commons photos, lifecheck, OSM pins.
- Next angle: Wikipedia "List of superlative trees in the United Kingdom" Windsor rows; Historic England 1000592 and 1001176 for named trees; Geograph search for "Conqueror's Oak" to get a geotag and life evidence.
- Overpass is dead from here; use the OSM API.

## Second session (2026-11-03)
Also searched: Wikipedia superlative-trees list (only Ankerwycke Yew for the area), Historic England list entry 1001176 (403), Windsor Local History Group (no tree content), Geograph (no Conqueror's Oak page; photo 7918227 is the 1937 Coronation Grove plaque), Herne's Oak (Home Park, private). Result stays 0 verified: no tree reached a coordinate plus a second source plus public access. Likely best next move: a session with a browser to open the Windsor Great Park veteran-tree pages and Geograph tag search for Conqueror's and Signing Oak.

## Third pass (2026-11-04), new angle: Tree Register champion list
Result: 1 tree verified (wsr_001 Signing Oak), several leads with coordinates. Windsor stays under four, so no place page yet.
- The Tree Register champion list is public and searchable by site: https://www.treeregister.org/champion-trees-list/?list_search=Windsor+Great+Park&per_page=100 (48 records). Each record page (/tree-directory/tree/<id>) gives girth, year, grid ref, owner and an Access field (Public open access / Private). curl works with a browser user agent. This is the working method: it surfaced 20-odd public oaks of 7 to 9.5 m girth with 10 m grid refs. Convert grid refs with pyproj EPSG:27700 to 4326.
- Tree Register records are copied from Ancient Tree Inventory data (recorder field says so). No Woodland Trust page was fetched or used.
- Signing Oak: owner page windsorgreatpark.co.uk/the-bronze-oak/ (900 years, bronze replica at Savill Garden cafe, 2025), Queen's Green Canopy 70 trees page, Tree Register 189522 (955 cm, SU96397342). Geograph 934772 is a geotagged oak photo 10 m away.
- Public unnamed oaks, the sequoia and the pin oak are leads only (register-only, no photo).
- Dead ends: windsorgreatpark.co.uk and monumentaltrees.com and geograph search pages are Cloudflare-blocked to curl (WebFetch gets some windsorgreatpark pages; the Valley Gardens URL guessed 404); historicengland 1000592 returns 403; parksandgardens has no individual trees; Commons categories have no tree-level categories beyond King Offa's Oak; Windsor churchyard yew search found nothing; OSM nodes near the oak are only Bing-traced anonymous trees.
- Next: a session with a browser to view Geograph 934772, 3546111 and 3054963 and photo-find the sequoia, pin oak and giraffe pollard; a second source for the Valley Gardens specimens (the garden keeper's champion tree notes).
