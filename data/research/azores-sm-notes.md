# São Miguel verify pass, 2026-11-02

Delivered: data/research/azores-sm-verified.json (azo_004 to azo_007). Leads appended to data/leads/azores.json.

Method: register rows (azores-aip.json, CC BY 4.0) checked against OSM API node/bbox (Overpass is dead from here; api.openstreetmap.org/api/0.6/map works), iNaturalist API, Wikidata, Commons API (rate-limits quickly, sleep between calls), lifecheck.py.

Hosts: curl worked on acorianooriental.pt, dn.pt, matajosedocanto.com, siaram.azores.gov.pt, trails.visitazores.com, blogspot. turismo.azores.gov.pt serves a Cloudflare challenge. Wikimedia API 429s after about 10 fast calls.

Findings
- Pohutukawa (SMG_IIM_36): OSM node 11 m from register; iNat 2026; alive. Register says Metrosiderus tomentosa, other sources excelsa.
- Furnas Norfolk pine (SMG_IIP_66): two press sources, 50 m tall; 1.90 m diameter (= about 6 m girth, OSM mislabels it as circumference).
- Sequoia (SMG_IIM_34): stands in the ticketed Mata-Jardim Jose do Canto, inferred from Commons category photos; no measurement; OSM node equals Wikidata coordinate (maybe copied).
- Jardim Antonio Borges Norfolk pine: OSM node plus SIARAM text only.
- Dragon trees Agua de Alto: not dead (iNat 2026-05-01 one alive, SIARAM report says three survive), but in hotel grounds; lead.
- Register level vs press: pohutukawa is Interesse Municipal in the register, press says public interest.
- Not reached: Jardim Jose do Canto (Ponta Delgada) Ficus; Rua Coronel Silva Leal dragon tree (lead entries unchanged).
