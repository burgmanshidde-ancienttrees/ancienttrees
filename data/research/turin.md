# Turin (Torino) research notes

## Piemonte regional register: YES, and it carries an AGE field

Regione Piemonte publishes "Alberi Monumentali del Piemonte: dati del censimento" on the
regional Geoportale (Sistema Conoscenze Ambientali), licence **CC BY 4.0**.

- Metadata record: https://www.geoportale.piemonte.it/geonetwork/geonetwork/api/records/r_piemon:9410f966-96b4-41ee-8f4c-ccdb60167218
- WFS: https://gisserver.territorio.csi.it/geoserver/decsiraogc_geo_alb_monum/wfs (typeName decsiraogc_geo_alb_monum:AlberiMonumentaliLoc)
- WMS: https://gisserver.territorio.csi.it/geoserver/decsiraogc_geo_alb_monum/wms

Fields carried per tree:
  id_n_scheda_albero          register card number, e.g. 010/L219/TO/01
  descr_stato                 status, e.g. "Iscritte in elenco"
  oggetto_di_identif          ALBERO SINGOLO / GRUPPO / FILARE DOPPIO / VIALE ALBERATO
  specie                      binomial with authority
  eta_presunta                PRESUMED AGE, as a band: "< 100" / "100-200" / "> 200" / "Non applicabile"
  circonferenza               girth in cm
  altezza_misurata_metri      measured height in m
  diametro_medio_chioma_metri mean crown diameter in m
  tipo_proprieta              Pubblica / Privata / Sia pubblica che privata
  url_decreto_minist          link to the ministerial decree

This is the first Italian source found with an age field of any kind. It is a band, not a
figure, but it separates ">200" from "100-200", which is exactly the distinction the pages need.
It also carries ownership, which settles hard rule 10 without a site visit, and the
oggetto_di_identif field which flags avenues and groups mechanically.

MASAF's national file for Torino is the SAME survey: identical coordinates and identical girths
for all ten trees in data/research/_candidates_turin.md. So national + regional is ONE source,
not two. The second source has to come from outside the register.

## Second source: the official city route

Turismo Torino e Provincia publishes an urban route "Gli alberi monumentali di Torino - Un filo
verde nel cuore di Torino", 13.9 km, 4 h, on Outdooractive with a GPX download. It names the
trees individually with species, exact place and measured height:
https://www.outdooractive.com/it/route/percorso-urbano/provincia-di-torino/gli-alberi-monumentali-di-torino-un-filo-verde-nel-cuore-di-torino/804381643/

mole24.it (2025-08-13) publishes the full 16-tree table with the DESIGNATION REASON per tree
("molto antico", "particolare architettura vegetale", "pregio paesaggistico", "rarita botanica"),
which the register layer itself does not expose.

## Outcome, 2026-08-05

Shipped to data/research/turin.json: **8 trees, one straight walk, 1.94 km spread**,
about 3 km of actual walking, Porta Nuova station to the Po.

  tor_001  Caucasian Wingnut    Giardino Sambuy        605 cm  27 m  100-200  photo
  tor_002  London Plane         Giardini Cavour        550 cm  34 m  100-200
  tor_003  Ginkgo               Giardini Cavour        370 cm  27 m  100-200  photo
  tor_004  Mediterranean Hackberry  Valentino north    475 cm  23 m  100-200  photo
  tor_005  Pedunculate Oak      Valentino, Rocaille    400 cm  28 m  > 200    approximate pin
  tor_006  London Plane         Valentino, Eridano     600 cm  26 m  > 200
  tor_007  London Plane         Valentino, Borgo       510 cm  36 m  100-200  approximate pin
  tor_008  London Plane         Valentino, Fontana     550 cm  40 m  > 200

Cut deliberately: the 13.9 km official route also takes in Parco della Tesoriera
(3.6 km west), Villa Rey and Corso Novara (2.4 km+ northeast) and the Giardini
Reali (1 km north, the wrong way). Those are in data/leads/turin.json. Taking the
whole route would have been four separate walks pretending to be one.

**The Sambuy connection is the thing that makes this a walk rather than a list.**
Ernesto Balbo Bertone di Sambuy ran Turin's public gardens and later became its
mayor. The garden outside the station carries his name, and he laid out the
Giardini Cavour at stop two between 1872 and 1875, on ground left uneven by the
demolished seventeenth century bastions. So the first three trees are one man's
work, and the Cavour laying-out date is what narrows those two from the register's
100-200 band to about 150 years.

### La Stampa: nothing, and the newspaper step still paid off

No La Stampa survey of Turin's monumental trees was found. What replaced it, and
did the same job, was the local news ecosystem covering the register release:
Quotidiano Piemontese, TorinoToday, Torino Cronaca and Mole24 all publish the
full per-tree table. Mole24's carries the **designation reason** per tree ("molto
antico", "particolare architettura vegetale", "pregio paesaggistico", "rarita
botanica"), which the register layer itself does not expose. Turismo Torino's
Outdooractive route carries the exact place per tree plus the measured height and
a GPX download. Between them that is the independent second source for existence,
species, place and height on all eight.

### Vitality check

A 13 July 2026 storm damaged roughly 50 trees "dalla collina al Valentino". The
Torino Oggi report names no species and no individual tree, only Vanchiglietta
and a generic list of streets. The regional layer, read live on 2026-08-05,
still lists all 14 Torino trees as "Iscritte in elenco" with nothing removed, so
nothing on this walk is recorded as lost. That is a register statement rather
than a sighting, and it is the honest limit of what can be checked from here.

Separately: the Corso Novara plane named by the tourist route is **absent from
the current regional layer**, on a street where the council has an active felling
programme for unstable trees. Blocked rather than published.
