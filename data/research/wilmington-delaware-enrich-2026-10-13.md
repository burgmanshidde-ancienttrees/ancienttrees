# Wilmington, Delaware enrich pass, 2026-10-13

Layer queried once (207 features, outSR 4326): https://enterprise.firstmap.delaware.gov/arcgis/rest/services/Biota/DE_Big_Tree_Champs/FeatureServer/0
Each of the 8 trees matched a record at 0 m, same species. Fields: ID (register number), OBJECTID, CIRCUMFERENCE_INCHES, HEIGHT_FEET, AVE_CROWN_SPREAD_FEET, SPEC_RANK.
Conversion: inches x 2.54 = girth_cm, feet x 0.3048 = height_m. The layer does not state the measuring height; Big Tree Champion programmes conventionally measure circumference at 4.5 ft, so treated as girth at breast height.

| tree | register ID | OBJECTID | circ in | height ft | crown ft |
|---|---|---|---|---|---|
| wil_001 | 166 | 1047 | 215 | 174 | 121 |
| wil_002 | 171 | 1048 | 244 | 167 | 104 |
| wil_003 | 243 | 1088 | 232 | 130 | 127 |
| wil_004 | 402 | 1123 | 182 | 96 | 82 |
| wil_006 | 130 | 1026 | 91 | 82 | 44 |
| wil_007 | 370 | 1152 | 102 | 84 | 43 |
| wil_008 | 393 | 1021 | 166 | 140 | 102 |
| wil_009 | 193 | 1063 | 219 | 110 | 72 |

No per-tree page exists, so register_name and register_id returned, no register_url. DATE_OF_RANK is a 2024 to 2026 epoch, so records are recent measurements.
Access: winterthur.org/visit/admission/ ($29 adult, $27 senior/student, 10 am to 5 pm Tue to Sun) and hagley.org/hours-tickets ($22 adult, 10 am to 5 pm, last admission 4 pm, closed Wednesdays). Hagley page carries a stray January 1 to 3 note, left out.
Season: wil_003 and wil_006 have phenology files, not checked for a striking moment, left open.
