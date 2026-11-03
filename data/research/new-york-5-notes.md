# New York 5 verify pass (2026-11-03)

Delivered 3 (nyc_140 to nyc_142), all flagged: Green-Wood Phoenix Ginkgo (OSM node pin, confirmed), Green-Wood Weeping Beech Tunnel (approximate, 50 m site), Queens Botanical Garden blue atlas cedars (approximate, garden-level pin). Below the 6 asked for: nothing else pinnable and worth the visit was in reach.

Method that worked: Green-Wood publishes a "Celebrated Trees Walk" (20 numbered stops with species blurbs) in its Alive at G-W visitor map PDFs (2023 and 2025 editions, URLs in the verified file). Several stops are mapped in OpenStreetMap as natural=tree nodes with name (Overpass bbox 40.646,-73.998,40.664,-73.976, only 8 of 370 nodes carry tags): Phoenix Ginkgo, Weeping Beech, Northern Red Oak, European Horse Chestnut, Yoshino Cherry. The map's pdf text is extractable with pypdf.

Leads worth a session: Green-Wood tulip tree (largest tree in the cemetery, 110 ft, nearly 6 ft diameter) and the NY State Champion hackberry. Both need the Tree Finder (https://gardens.green-wood.com/portal/apps/experiencebuilder/experience/?id=6ba13c738a2340e5bc4bc987f72cf2ba, reached by 302 from green-wood.com/trees) for coordinates.

Hosts: gardens.green-wood.com hangs to curl (-m 20, twice) and the Browser pane refused it. overpass-api.de answers 406 to a default curl user agent; with a descriptive User-Agent it works but often returns 502 at capacity (retry once). Nominatim has no entry for the Queens Botanical Garden entrance. No Moravian Cemetery tree is named by any source; Snug Harbor not researched (time). No photos hunted, photo_candidate null throughout. Transport left as "check route".
