# Welsh yews and Snowdonia: pass notes (2026-11-03)

Method: Ancient Yew Group database pages (facts only: girth, grid ref, notes) plus a second source each (Wikipedia, Wondermondo, the church's own site, National Park page). Girths are 1998-99 visits, trees have grown since. Grid refs converted with pyproj (EPSG:27700), site-level so `approximate` with `location_site`. Age claims are recorded per source, no crown asserted. Dead end: Bodnant's champion coast redwood fell in Storm Arwen. Snowdonia yews are modest (under 4 m girth). Search summaries used as pointers only; figures above were seen on fetched pages except where noted in verify_notes.

## Second round (2026-11-03): seven churchyards
Method: AYG site PDFs read with PyMuPDF (fitz; pypdf not installed), AYG tree pages, Wikipedia, CPAT Radnorshire church surveys (now at heneb.org.uk/archive/cpat/...; cpat.org.uk redirects), Church in Wales Church Heritage Record, Commons/Geograph geotags via the Commons API (needs a User-Agent). Grid refs converted with pyproj, EPSG:27700, matched Geograph geotags within 25 m.
Verified: sfl_001 Strata Florida, lnm_001 Llanfihangel-nant-Melan, bwn_001 Bettws Newydd, ovr_001 Overton, mmh_001 Mamhilad, llf_001 Llanfaredd. Rejected: Corwen (AYG: one very young yew).
Rhyme (Wikipedia): third line is "Overton yew trees, St Winefride's wells": the wonder is the yews plural, not one tree.
AYG PDF URLs: /wp-content/uploads/2022/11/<Name>-2025.pdf works for Strata Florida, Llanfihangel-Nant-Melan, Mamhilad, Bettws-Newydd-2025c; the Mamhilad-2020a and Bettws-2025 variants 404 (return an HTML page, same size). Overton and Llanfaredd are in /userfiles/file/ (2019).
Not reached: other Welsh churchyard yews (Llangar near Corwen 417 cm is modest; Llanafan Fawr and Llanfeugan not looked at). Mamhilad has no independent source for the tree's age beyond a cycling-trust page and a Geograph caption.
