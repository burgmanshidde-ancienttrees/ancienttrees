# Malta notes (verify pass, 2026-11-02)

## The official list and its licence
- Instrument: List of Historical Trees having an Antiquarian Importance Order, S.L. 445.02 (originally Government Notice 269 of 1933). Sites it names, per a search summary of ERA's page (not seen on a fetched page, ERA 403s to curl and WebFetch): Il-Ballut tal-Wardija, Il-Wied tal-Imgiebah (Mellieha), Il-Bidnija (Wardija), Il-Buskett, Il-gonna ta' San Anton.
- Tree Protection Areas under the Trees and Woodlands Protection Regulations 2011 (L.N. 200 of 2011, S.L. 549.64; updated by S.L. 549.123): Wardija oaks TPA005MT, Mellieha oak TPA004MT, Bidnija olives (G.N. 473/11).
- Publisher: ERA (Environment and Resources Authority, era.org.mt), the legal text on legislation.mt (Government of Malta).
- Licence/reuse: no reuse terms seen. legislation.mt/eli/sl/445.02/eng/pdf returned "no legislation found" via WebFetch (a 30 KB page came back via curl but could not be parsed: no pdftotext/pypdf here). The schedule names SITES, not individual trees with coordinates. Legal notice used as a fact source only; no data import possible.
- Hosts: era.org.mt (403 to curl, curl UA and WebFetch, including wp-content PDFs), mdpi.com (403), environmentcms.gov.mt (ECONNREFUSED), eracms.gov.mt (DNS fails), web.archive.org (429 after a few calls). monumentaltrees.com not tried by curl.
- Overpass: overpass-api.de fails TLS, overpass.private.coffee times out; the maps.mail.ru mirror (https://maps.mail.ru/osm/tools/overpass/api/interpreter) WORKS from this Mac with a User-Agent header (urllib POST). OSM natural=tree in Malta is sparse: only the Xemxija carob has a name/age.
- Naming body: none gives individual trees with coordinates. Expect 1 to 3 trees for Malta.

## Verdicts
- Verified (malta-verified.json): mlt_001 Xemxija Old Carob Tree (flagged).
- Leads (data/leads/malta.json): Bidnija (closed to the public per Heritage Malta), Wardija holm oaks (private-property signs), Wied tal-Imgiebah, Buskett, San Anton, Argotti dragon tree, Barrakka (nothing).
- Not a cluster: Attard and Valletta gave no individual tree; the one verified tree is in Xemxija, St Paul's Bay (north), about 30 to 45 minutes by road from Valletta.
- Existing earlier lead: data/leads/_famous-malta.json Xemxija Old Carob (now mlt_001). Commons category Xemxija Old Carob Tree has photos.
- Not tried: Gozo (one search, nothing), Ta' Qali, Ghajn Tuffieha, Wied il-Qlejja.
