# Indianapolis deepen pass, 2026-11-04

Delivered to data/research/indianapolis-verified.json: ind_002 Temple Oak, ind_003 Nowland Oak (Chinquapin Oak Park), ind_004 Indiana Statehouse Moon Tree. Leads added to data/leads/indianapolis.json.

Naming bodies found: none official for Marion County. Indiana DNR Big Tree Register (champions only, GIS layer 2005 at gisdata.in.gov Big_Tree_Champions_2005, queryable with curl; Marion rows: Downey Hawthorne at IMA, Hornbeam at Crown Hill, Red Oak on Kollman Road, all 2002-2004 and unusable for pins), Springdale Neighborhood Association, Keep Indianapolis Beautiful, NASA Moon Trees.

Dead ends:
- Crown Hill tree map and brochure PDFs (crownhillhf.org, 2019/2021/2022) are image-only; WebFetch returns binary, zlib streams hold no text. Retry needs OCR or a browser. Saved copies: out/tmp/ind_treemap.pdf, out/tmp/ind_brochure.pdf.
- Hosts: www.in.gov/dnr/forestry/8169.htm hung (curl -m 20, exit 28). Cloudflare/403: indianapolisrecorder.com, indyarts.org, onlyinyourstate.com, monumentaltrees.com (WebFetch), playgroundequipment.com, indianaforestalliance.org, geocaching.com worked through WebFetch.
- Nominatim could not give the Temple/Brookside intersection; pin built from street geometry (Temple Ave lon -86.1181; Brookside Pkwy S Dr lat about 39.7858).
- lifecheck.py returned only unrelated iNaturalist plant observations (grass, chicory); not alive evidence for either oak.
- Holliday Park (1,200 labelled arboretum trees), Garfield Park, Military Park, Newfields/Oldfields, Butler, Fort Harrison, Eagle Creek: no individually named old tree found in any source seen.
- Search summaries stated several facts not seen on fetched pages ($8,000 treatment, Indy Arts 450 years, Temple Oak 2007 contest); the first two were left out of the deliverable.

Supply is honestly thin: three delivered, not nine.
