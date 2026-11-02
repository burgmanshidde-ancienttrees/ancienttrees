# Bali verify pass, 2026-11-02

No register covers Bali; no naming body found (Bali has no tree register, the Gianyar and Badung offices keep none per local press). Expect few trees. Search in English and Indonesian.

Verified (data/research/bali-verified.json): bli_001 Pura Kehen banyan (approximate), bli_002 Kayu Putih / Bayan Ancient Tree (confirmed via plus code), bli_003 Bunut Bolong (confirmed via plus code). Floor of four NOT reached, so no Bali page yet.

Method notes
- Google plus codes printed on lokasibali.com decode offline (full code needs the 4-char prefix: 6P3Q for Tua, 6P3P for Pekutatan). Cell about 14 m. Script idea: A='23456789CFGHJMPQRVWX', pairs of lat/lng.
- Nominatim finds temples (Pura Kehen) but not trees. Overpass is dead from here. Ubud Monkey Forest and Sangeh are woods; both had fatal tree falls (Ubud Dec 2024, Sangeh 3 Dec 2025), check openings before any work.
- Hosts: djkn.kemenkeu.go.id slow (SSL handshake timeout once, loaded second try); thejakartapost.com loads but heavy; nowbali.co.id Sangeh page timed out once.
- Kayu Putih tree: dimensions conflict (50 m government vs 70-75 m local); trunk diameter about 6 m is consistent.
- Next angle: Ubud cluster trees need the Padangtegal forest management's tree list or geotagged photos; Wikipedia id and Balinese temple registers (PHDI) might name pule and beringin by pura. Search 'pohon pule' and 'kepuh' at pura dalem (death temples keep ancient pule).

## Second pass, 2026-11-02
Verified now 5 (bli_004 Bali Botanic Garden Giant Ficus, confirmed pin; bli_005 Gesing giant banyan, approximate, weak). Floor of four reached: Bali can open, with bli_005 and bli_001 thin and flagged.
- What worked: Nominatim search bounded to Bali (viewbox 114.4,-8.05,115.75,-8.85, bounded=1) for 'giant tree', 'banyan tree' returns OSM natural=tree nodes with names. Found: Giant Ficus Tree (node 4821991026, bli_004), Giant banyan tree Gesing (10958802627), Banyan Tree (4345222406), Old Giant Tree Pelaga (11781902566), Bunut Bolong (nodes 4760876821 at -8.38677,114.87353 and 990920888 at -8.36341,114.91871, the second a different place). Node 4760876821 sits about 25 m from bli_003's plus-code pin: the pin is corroborated; bli_003 can be treated as confirmed with that node as second evidence.
- iNaturalist: the API by bounding box only gives street and garden plants. Useful only as a GPS cross-check for a tree already named (bli_004: 2013 note 'Giant Fig Tree, believed hundreds of years old' plus 2026 'Locally famous specimen' within 15 m of the OSM node, dated 2026-07 to 2026-10). No iNat evidence for temple pule or kepuh.
- Commons geosearch and category listings: 'cirrussearch too busy' on the geosearch twice, categories (Trees in Bali) empty. Wikidata search 'banyan Bali' empty. Nothing from these.
- Indonesian searches for pule, kepuh, beringin tertua: no age-figured tree in a pura dalem; the Akah (Klungkung) cemetery pule fell (balidiscovery, no age); the Puri Kantor Ubud banyan fell (about 300 years, kumparan; already blocked). No Dinas Kehutanan, BKSDA or Kalpataru tree list found for Bali; only hutan adat and sacred-forest research.
- Kepuh Agung (airport) one source of 2016 only: lead. Lanang Wadon in Sangeh: lead.
- Hosts: budayabali.com timed out on WebFetch once; commons search busy; nominatim fine at one request per second.
- Gesing/Munduk banyan: every page repeats 700 years and 85 m; 85 m is not recorded. The Yogitimes, Holidify, Tatinta, Thrillophilia and balitouristic pages are not independent.
