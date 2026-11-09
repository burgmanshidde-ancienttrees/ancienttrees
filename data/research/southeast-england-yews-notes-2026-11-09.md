# South-east England yews, verify pass 2026-11-09

Method: AYG find-a-yew table filtered by county (works with `county=Surrey|Sussex+West|Sussex+East|Hampshire|Berkshire`, `/find-a-yew/page/N/` for further pages, 20 rows a page; rows carry the map coordinate in the "View on map" link). Per-tree page /yew_tree_database/<slug>/ and the site-file PDF (wp-content/uploads/<year>/<month>/<Name>-2019|2025.pdf; PyPDF2 reads them, system python3 not -I) hold the dated girth history. 402 rows in the five counties; the 7 m+ churchyard rows are about 70.

Delivered 10 (data/research/southeast-england-yews-verified.json): Crowhurst (Surrey), Tandridge, Wilmington (East Sussex), Corhampton, Stedham, Dunsfold, Charlwood, Coldwaltham, Tangmere, Itchen Abbas. All AYG survey (Hills 1997 to 2004, Norton later), none from the Ancient Tree Hunt. Six are flagged for a last dated sighting of 2011 to 2013 only.

Not delivered, with reason:
- Aldworth (Berkshire): AYG class 7m+ is historic; the single surviving propped fragment is 353 cm at ground (2008) after a 1976 storm. Not a 6 m trunk now.
- Breamore (Hampshire): many stems regrown inside an old bole, AYG says no girth should be taken seriously; 1082 cm at 60 cm. Lead, multi-stem, a good Saxon-church visit.
- Buxted (East Sussex): shattered, multi-fragment (795 cm at ground); lead.
- Wilmington is twin-trunk and is flagged as one tree because of the common base.
- Ankerwycke (Berkshire/Runnymede) already live.
- Not yet worked, 7 m+ churchyard leads in the AYG table with coordinates: Surrey Peper-Harow, Horley (Lost marker), Hambledon; West Sussex Ardingly, Mid Lavant, Slaugham, Stopham; East Sussex Ninfield, Etchingham, Herstmonceux, Rotherfield, Chailey, Crowhurst (Sussex); Hampshire Bedhampton, Boarhunt, Durley, Fareham, Farringdon, Greatham, Hawkley, Lockerley, Long Sutton, Priors Dean, South Hayling, Highclere; Berkshire Langley Marish, White Waltham. 5 to 7 m rows (Albury, Alfold, Ashtead, Capel, Tillington, Funtington, Walberton and others) not opened. Tillington is 503 cm, under the 6 m cut.

Photos: Geograph file names via Commons search; none viewed or downloaded. Wikimedia API rate-limited (429) after the first metadata call, so licence and author are only confirmed for Geograph 7296752 (N Chadwick, CC BY-SA 2.0, 2021-09-22).
Hosts: ancient-yew.org fine (wp-content PDFs); treeregister.org record pages need a trailing slash (301 otherwise).
Windsor: only Tree Register 125681 (pin oak, a named TROBI measurer, 2021) is not ATI-recorded; the six oaks and the sequoia name the Ancient Tree Inventory as recorder and stay leads.
