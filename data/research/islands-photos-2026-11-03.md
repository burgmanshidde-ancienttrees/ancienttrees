# Island photo pass, 2026-11-03

Goal: one approved, openly licensed photograph per island so the Discover shelf "Tree islands" can show it: menorca, maui, hawaii, okinawa, yakushima, gran-canaria, cyprus, bali.

Machinery: `photo_hunt.py --city <8 islands> --recheck --limit 60`, then `photo_last_resort.py` where empty, `photo_fetch.py` to disk, pixels viewed, `photo_verdicts.py` to apply.

Before: no approved photo on any of the 38 trees. Held: mau_001 (iNat 2011, pre-fire), yak_002 (Commons fog shot, unnamed cedar). Earlier rejects in data/photo-queue.json (Cyprus chapel shots, Kalopa iNat details, Lahaina panoramas, Jomon Sugi trunk close-ups).

Openverse timed out on every tree during the sweep; Commons, Wikidata and iNaturalist answered.

## Findings

The sweep found new candidates for only five trees (bli_004, gcn_001, gcn_003, gcn_004, and nothing new elsewhere). `photo_last_resort.py --radius 150` added two church shots for cyp_001 and nothing else. So the Commons categories named after the trees were listed straight into the queue (out/tmp/commons_cat_queue.py, source "category", photo_hunt's licence rules), looked at on contact sheets, and applied with `photo_verdicts.py`.

### Approved (7)
- yakushima / yak_001 Jomon Sugi: File:Jomon Sugi Panorama.jpg, CC BY-SA 3.0, Chris 73 (Commons category Jomon sugi). Whole tree in leaf, sun, blue sky. Attribution fixed by hand: the Artist field is empty, the credit comes from the Attribution field.
- yakushima / yak_002 Daio-sugi: File:Dai-O-Sugi.jpg, CC BY-SA 3.0, Chris 73 (category Daio sugi). This replaces the held fog shot "Forest in Yakushima 15".
- gran-canaria / gcn_002 Drago de Galdar: File:Drago de Gáldar.jpg, CC BY-SA 4.0, Josefa Molina (category Drago de Gáldar). Whole tree in its red courtyard.
- gran-canaria / gcn_004 Drago de Pino Santo: iNat obs 185621502, CC BY, Vicente Lopes. Geotag 28 m from the pin; the dragon tree on its basalt ledge.
- bali / bli_004 Giant Ficus, Bali Botanic Garden: iNat obs 320400659, CC BY, Lyu yi-chi. Geotag 13 m; shows the many fused trunks the story describes; a small walker for scale.
- maui / mau_002 Ka'ahumanu Church Monkeypod: File:Ka'ahumanu Church Behind Tree.jpg, CC BY-SA 4.0, Rodrigues808. Geotag at the church; low monkeypod limbs with the church behind. Note: our approximate pin (20.89694,-156.50028) sits about 1.2 km north of the church (photo geotag 20.88596,-156.50446); the address is the church. Worth a pin pass.

### Held
- gcn_003 Teror araucaria: iNat 252263419 (CC0), geotag 6 m, but the photo shows one trunk where our recognition line says two parallel trunks forking low. It may be the plaza's other araucaria.
- gcn_001 Pino de Casandra: File:Pino de Casandra - Presa de las Niñas ... 01.jpg (CC BY-SA 4.0, Rvr) is named, but the pine is a small figure on a far ridge.
- mau_001 Lahaina banyan: three more iNat shots (2019, 2020 and 2022), all from before the 2023 fire, so held for the same reason as the 2011 one. No post-fire open photograph found.

### Rejected (kept in the queue)
- gcn_001 iNat: a young pine at the pin (not the old tree), a cone close-up, a bark close-up, and one POOR.
- gcn_003: a branch close-up, and one POOR.
- bli_004: leaves in a hand, a different single-stemmed fig 25 to 40 m off, fig fruit, and a WEAK detail.
- bli_001 Pura Kehen: 47 category files, all temple scenes or carvings. The banyan with the kulkul is never the subject; two 1998 scans show only hanging roots.
- mau_002: 17 other church and grounds files, where the tree is not the subject.
- men_005: the Llatzeret island seen across the water, and harbour views. No tree.
- cyp_001: the Kalopanayiotis church porch and a vault detail.

### Still no photo
- menorca: nothing on Commons, iNat or Wikidata within reach of any of the six pins. The Illa del Llatzeret category holds no tree.
- okinawa: nothing for any of the six. No Commons category found for the Shuri akagi.
- hawaii (Big Island, Kalopa): nothing new. All six share one pin, so no geotag can tell the trunks apart. Candidates need a Kalopa trail photo with a name on it.
- cyprus: nothing usable. Earlier rejects stand (Hidde judged the Theoskepasti chapel shots poor; the Xyliatos olive was shot at dusk).
- bali/bli_002, bli_003, bli_005: no source answered.

Next angle, if any: the archive lane (OUTREACH_STRATEGY.md group `archive`) for Menorca (whoever photographed the Balearic register's singular trees) and Okinawa (the prefecture's notable-tree list); not checked in this pass. Commons will not close these.
