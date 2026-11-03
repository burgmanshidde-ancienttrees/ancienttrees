# DC suburbs pass, 2026-11-02

Delivered 2 flagged trees (wdc_040, wdc_041), 16 rejects and leads in dc-suburbs-rejects.json.

- The Prince George's County champion layer (ArcGIS Prince_Georges_County_Native_Champion_Trees_/FeatureServer/0, 49 rows) has only species, address, other-location text, coordinates and a state-champion flag. No girth, height or year. The 2019 PG Tree Book PDF (pgparks.com) returns an HTML 404 shell to curl and WebFetch. So no PG row could be sized or given a second source; a register row alone is not a reason to walk.
- UMD arboretum's champion page lists 15 trees, none a post oak; campus champions are ornamentals.
- Montgomery Forestry Board register pages (mcmdforestryboard.org, Wix) render without data to WebFetch and to the browser pane's page text.
- Strongest find: Alexandria Bicentennial Willow Oak with a city-published GPS and a Nov 2024 measurement, but about 45 to 50 minutes away, so a lead (full record in rejects).
- Arlington County specimen nominations PDF (arlington.granicus.com clip_id 437 meta_id 42607) is useful: county-owned park trees with sizes, none with coordinates.
- Overpass not used; OSM API bbox queries return no natural=tree nodes at Fort C.F. Smith Park.
- New hosts: none hang. pgparks.com PDF path serves an HTML 404 page.
