# Andalucia REDIAM verify pass, 2026-11-02

Source: sheets in data/research/andalucia-rediam-sheets.json. Delivery files: grazalema-, alpujarras-, granada-, cordoba-rediam-verified.json. Rejects: data/leads/andalucia-rediam.json.

Method per tree: sheet text, iNaturalist GPS observations within 150 m (api.inaturalist.org), Commons geosearch (rate-limited, 429 on retry), one or two searches, fetch of a page only for a figure.

Results
- Confirmed pin: only the Chaparro de las Animas (rediam_745), by two iNaturalist cork-oak observations (2025-02-20 accuracy 4 m, 2026-06-18 accuracy 15 m), photos viewed. Both observations are not openly licensed (all rights reserved; CC BY-NC), so no photo lead.
- Everything else is register-only with approximate pins and no photograph: Spain is covered, so each lacks the photo-or-confirmed-pin gate. Delivered flagged so register data and facts are kept.
- Only sourced age: the Carob of Loma de los Escalones (350 to 400 years, the register's own estimate, basis not stated).
- Hosts that failed: blog.fuertehoteles.com (403), universolorca.com (certificate mismatch / OpenCms 404), commons.wikimedia.org geosearch (429 after first calls), en.andalucia.org pages return only navigation.
- Hispanopedia (a Wikipedia mirror) says the Ocuri wild olive is over 700 years old; unsourced, not used as age.
- No pypdf in the system Python, so sheet text was limited to the 2,500 characters already parsed (the Algarrobo and Chaparro sheets cut off at the end of Entorno).
- Distances to villages in transport lines are estimates from coordinates and say so.
- Not examined for lack of time: rediam_154, 156, 153 (Alpujarras, private or Polopos).

## Cazorla and Aracena pass (2026-11-02)
- Sheets 1025, 1042, 1047, 1082, 1180, 1037, 1240, 1228 return 404 on the Junta server and have no parsed text; Jaen/Huelva text decodes with +28 on control characters (digits intact).
- Cazorla delivered: czl_001 Felix pine (1035), czl_002 Pino de las Cruces (1025, Junta leaflet ends at tree, Commons photos 2013-2019), czl_003 la Misa (1018), czl_004 Fuente del Oso I (1046, folds 1047), czl_005 Cornicabra Salto de los Organos (1014, folds 1015). Others left as leads for lack of any path evidence.
- Aracena delivered: arc_001 quejigo Pena de Arias Montano. Most Huelva sheets are private or lack path evidence.
- Commons API 429s after a few queries; wait a minute.

## Verify pass 2026-11-02 (Ronda, Grazalema, Alpujarras, Malaga)

- Ronda: rnx_001 to rnx_004 in ronda-rediam-verified.json (Alcazaba pinsapo, Pinsapo Moreno, Pinsapo del Candelabro, Quejigo de La Plazoleta with the Mostajo folded in). Access caveat: the Junta trail leaflets (about 2010) list a park-office authorisation for the Quejigales and Saucillo trails; 2022 to 2026 guides mention none. Moreno and Candelabro have a dated second source (ESDiario 3 Nov 2023).
- Grazalema: grz_004 (Taramal pinsapo, in the permit-controlled Pinsapar zone, free authorisation via El Bosque visitor centre) and grz_005 (Zurraque holm oak, register only). Cornicabra de Los Nunez blocked (private farmland).
- Alpujarras: Tres Hermanas, Tia Manuela, Jeromos blocked (private, no public path evidenced); Haza del Lino blocked (fenced estate). Nothing added to alpujarras-rediam-verified.json.
- Malaga: mlx_001 Ombu of Jotron (flagged, register plus Komoot for the cortijo ruins). Pino de Jotron has no sheet: lead.
- Hosts: overpass-api.de refuses connections from the shell; wikiloc and loc.wiki 403; urbanismo.malaga.eu PDF unreadable by WebFetch. Shell has no outbound network, only WebFetch/WebSearch.
