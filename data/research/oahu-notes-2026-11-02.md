# Oahu verify pass, 2026-11-03 (file name keeps the briefed date)

Delivered 11 trees in data/research/oahu-verified.json (hnl_022 to hnl_032), leads appended to data/leads/oahu.json.

Sources that worked (all fetched): Honolulu City Council Bill 66 (2025), https://hnldoc.ehawaii.gov/hnldoc/document-download?id=26197 (12-page PDF with a text layer; it restates the exceptional-tree register with a location description and TMK per tree; ordinance wording gave tree-level descriptions like "Ewa tree across the street from the Diamond Head Tennis Center, makai side of Paki Avenue"); Honolulu Magazine photo gallery Feb 2021 (https://www.honolulumagazine.com/?p=333740; independent description of the Dept of Agriculture kapok, Nuuanu Valley Park mango, Waialua earpod); Outdoor Circle Kapiolani walk PDF; City DPR Wahiawa Botanical Garden self-guided tour PDF; Hawaii Magazine June 2024 (Wahiawa garden entry free).

Method note: pypdf extracts the PDF text (no pdftotext on this Mac); helper out/tmp/pdftxt.py. The bill text has words run together; grep with partial strings.

Hosts: Nominatim rate-limited (429) after about 10 calls in a row; Photon (photon.komoot.io, with lat/lon bias) worked with no limit and gave Natatorium, tennis centre, La Pietra, Wahiawa garden, Waikiki Shell, Nuuanu Valley Park. Not found by either: Kailua Road Triangle Park, archery range. hawaii.edu still unreachable (not retried).

Register caveats applied: banyan girth (circumference in feet) disagrees with the register diameter on most Kapiolani banyans (multi-stem masses), recorded as register figures and flagged in verify_notes. 115 kapok: the "151 inches around" in magazine and Outdoor Circle text is the register DIAMETER; circumference is 12.07 m.

Life checks: no report found of any of the 11 falling or cut. Related cuts: exceptional earpod on Keeaumoku St (Nov 2013, kapok beside it left standing, Hawaii News Now); five insect-damaged banyans on Monsarrat Ave at the bandstand lot (Star-Advertiser ?p=435260, undated, not register trees). Kailua-Kona Moreton Bay fig loss (Oct 2025) is the Big Island, unrelated.

Not done: lifecheck.py (no recency data for Oahu), Lyon Arboretum cluster (see lead), the UH arboretum list, Ala Moana largest banyan.
