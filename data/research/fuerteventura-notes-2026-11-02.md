# Fuerteventura verify pass, 2026-11-02

Result: 0 trees verified. Fuerteventura has no official catalogue of singular or monumental trees that any search surfaced (Tenerife and Gran Canaria have Cabildo catalogues; the Cabildo de Fuerteventura site cabildofuer.es only shows tree-giveaway news and a protected-areas map PDF). A 2009 Gobierno de Canarias publication on singular trees of the archipelago was mentioned in a snippet, not fetched or confirmed to cover Fuerteventura.

What worked: iNaturalist API (taxon and text search inside the island bbox) for tree coordinates; Commons API (categories Trees in Fuerteventura and Palm trees in Fuerteventura hold almost nothing relevant).

Dead ends:
- mdc.ulpgc.es PDFs (a dragon-tree text and a palm text): HTTP 403 to curl and WebFetch. Only search snippets seen, which are leads.
- Overpass: kumi.systems returned empty, private.coffee exit 000; OSM tree nodes not checked.
- Search for "oldest tree of Fuerteventura", Betancuria, Vega de Rio Palmas, Pajara, Tarajal de Sancho: nothing naming an individual tree with age or size.

Observations: dragon trees on Fuerteventura are imported plantings (ULPGC snippet); the iNaturalist ones are flagged casual and photographed CC BY-NC, which our photo rules do not accept. Floor of 4 trees for a place page is not reachable; at most lone tree pages if an old palm or fig with a source turns up.

Ideas for a later session with a browser: Cabildo de Fuerteventura Medio Ambiente site, Gobierno de Canarias 2009 singular trees book, IDECanarias layers, Betancuria church square (Santa Maria) for a fig or palm, OSM tree nodes via a working Overpass.
