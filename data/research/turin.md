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
