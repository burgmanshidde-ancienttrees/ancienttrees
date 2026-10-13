# Salt Lake City enrichment pass, 2026-10-13

Layer: https://services.arcgis.com/ZzrwjTRez6FJiOq4/arcgis/rest/services/Big_Trees/FeatureServer/0 (274 records, queried with outSR=4326).

All five trees matched a record at 0.0 m (layer Lat/Long equal our pins), species agreeing.

| tree | OBJECTID | measured | circumference in | height ft | girth_cm | height_m |
|---|---|---|---|---|---|---|
| slc_001 London Planetree | 80 | 2025-08 | 199 | 100 | 505 | 30.5 |
| slc_002 Hackberry | 150 | 2018-10 | 147 | 60 | 373 | 18.3 |
| slc_003 Ohio Buckeye | 146 | 2018-10 | 84 | 63 | 213 | 19.2 |
| slc_004 Wych Elm | 244 | 2019-08 | 163 | 84 | 414 | 25.6 |
| slc_005 Cedar of Lebanon | 25 | 2019-08 | 109 | 66 | 277 | 20.1 |

Notes:
- Units are inches (circumference) and feet (height), converted by 2.54 and 0.3048. The layer carries a total-points field (circumference + height + spread/4), the American Forests champion formula, which confirms the units.
- The layer has no description or measuring-height field. Champion-tree scoring normally uses circumference at 4.5 ft (1.37 m); that is an assumption, not stated by the layer.
- The layer has no owner or copyright text in its metadata. register_name is descriptive: Utah Big Tree Register as kept by Salt Lake City Urban Forestry. Not confirmed from an item page.
- Per-record owner field: Salt Lake City (slc_001 to 003), The Church of Jesus Christ of Latter-day Saints (slc_004, 005). PUBLIC_ACCESS is Y/Yes for all five. State champion status 1 on all; HERITAGE_TREE Yes only for slc_001 to 003.
- slc_002 and slc_003 are 22 m apart, each with its own record.
- No register_url (no per-tree page found); register_id given instead.
- Season, pin and access left alone as instructed.
