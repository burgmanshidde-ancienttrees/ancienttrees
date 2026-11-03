# Washington DC verify pass 2 (wdc_026 to wdc_035), 2026-11-02

Method that worked: the DDOT Urban Forestry Division public tree inventory (Open Data DC, CC BY 4.0) is queryable as a per-tree ArcGIS layer with DBH, arborist condition and date, ownership, and a GPS point per tree:
https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Urban_Tree_Canopy/MapServer/23/query (fields CMMN_NM, SCI_NM, DBH, CONDITION, CONDITIODT, OWNERSHIP, VICINITY, FACILITYID, TREE_NOTES, CROWN_AREA, MAX_CROWN_HEIGHT). curl works, no key. Filter used: DBH >= 50 and < 100 (above that is typing error), OWNERSHIP in (UFA, DPR, NPS, DGS), CONDITION not Dead or Poor. Ten trees chosen; 20 m neighbour check done so each is the largest crown at its point.
Useful for future passes in other DC corners (Rock Creek Park and NPS ground are not in it). OWNERSHIP 'Private' rows are never shippable.

Caveats the writer must keep:
- Every entry is ONE SOURCE (the city's own inventory). Age is not documented anywhere; do not derive one.
- girth_cm is computed from DBH (DBH x pi x 2.54), not measured girth.
- Crown height and area are LiDAR fields in the record (units believed feet and square feet); not used as height_m.
- wdc_030 East Capitol Street Elm is rated Fair with dieback since 2019: flagged.
- Pins are the inventory GPS points ('confirmed' because each is a single tree record whose neighbours within 20 m are far smaller); no photo seen on any of them.
- No photo_candidate found for any (Commons geosearch, 60 m, empty for all tested).

Dead ends this pass: see washington-dc-2-rejects.json. Hosts: gardens.si.edu (Cloudflare 500), www.aoc.gov (use web.archive.org/web/2026/ with curl; worked for /blog/biggest-capitol-tree), congressionalcemetery.org arboretum pages (fetch fine, no coordinates), caseytrees.org (fetch fine with a browser user agent), nominatim returned nothing for 'Senior Circle'.
Leads worth a session with a browser or a GPS fix: Rock Creek Park exercise-course Willow Oak (Casey Trees 2023, 250 in), Union Square bur oak (AOC 2026, 64 in DBH), Glastonbury thorn in Senior Circle (National Cathedral), Congressional Cemetery oaks and magnolias.
