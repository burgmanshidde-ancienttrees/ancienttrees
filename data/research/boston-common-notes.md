# Boston Common / Public Garden pass, 2026-11-03

Key find: City of Boston "BPRD Trees" inventory (data.boston.gov/dataset/bprd-trees, PDDL licence, regenerated 2026-11-03) holds tree-level points with DBH for the Common (584), Public Garden (430) and Commonwealth Avenue Mall (503). Matching DCR Legacy Tree circumference (DBH x pi) to inventory DBH by species gave real tree coordinates (pagoda tree, Franklin Sq white oak). Reusable for other Boston parks (Back Bay Fens 1,425, Olmsted Park 590, etc.) and for any DCR row in a city park.
CSV is public domain; inventory carries no height or age and no vitality field. Download: bprd_trees.csv.

Delivered 8 (bos_046 to bos_053), rejected 13 (see boston-common-rejects.json).
Walk: pagoda tree 56140, ginkgo 56146, bur oak 56147 within 40 m (Public Garden west side); rock elm and Bagheera beech 40-120 m east; Common elm 400 m east.

Other big Public Garden trees not delivered (inventory only, DBH in): red oak 56171 (53.9), Kentucky coffeetree 56196 (48), English elms 56268 (51), horsechestnut 56138 (47), purple beech 56148 (50.7), white willows 56177/56180 (52). Franklin Sq American elm 59078 (55 in, 42.3387718,-71.0732117). Common English elms near the Parkman Bandstand: 57538 (64 in, 42.3555717,-71.0668640) and 900093014 (59 in).
Fetch problems: overpass-api.de returned non-JSON (rate limit), no other hangs. Nominatim cannot place Bucknam St / Butterfly Park.
