# Baarn enrich pass, 2026-10-13

Source: LRMB public ArcGIS layer (LRMB_v2024_openbaar, layer 1), queried by nr and by a LAT/LON bounding box over Baarn (the esri distance/units query returned 400, so a where clause on LAT/LON was used).

Returned (own records, numeric stamomtrek and hoogte fields, units cm and m):
- brn_002 nr 1696953: girth 565 cm, height 28 m.
- brn_007 nr 1696955: girth 330 cm, height 20 m. Status field = 4 (Afgekeurd): the register holds the record but did not accept it as monumental. Worth noting on the page, not a reason to retire.
- brn_008 nr 1677447: girth 452 cm, height 25 m (text: ruim 4,5 meter). The record says the plane was probably planted 1890-1900, not 1830-1840.
- brn_006 nr 1691787: registered as Catalpa speciosa (we say bignonioides; species conflict to note). Fallen in a storm (record text says April 1973, boom_opm says 1970), lies as a multi-stem tree; girth 230 / height 18 given in the record but for a fallen tree, so not returned as a measurement. Register coordinate 52.194427, 5.278598 is 6 m from our pin; it does not upgrade precision (tree lying, palace garden paid).

Open (no honest answer found):
- brn_001 dawn redwood: no LRMB record within the Cantonspark box. No OSM tree node.
- brn_003 tulip tree grove Groeneveld: only LRMB record near is nr 1686360 (Beuk, not tulip tree) about 50 m away; nr 1686359 (red oak) and 1677536 (oaks). No tulip tree record, so no register match.
- brn_004 copper beech: no 'Atropunicea' record near Groeneveld (nr 1686360 is a green Beuk, 420 cm, not a match). Overpass found no natural=tree nodes within 300 m of the pin, none with Fagus within 500 m. Pin gap stays open.
- brn_006 pin: no better evidence than the register coordinate above.
- Season: giant-sequoia has no intensity data; London plane is unseen/nice only. Nothing set.

Cantonspark OSM nodes within 200 m of the main entrance are only Aesculus flava, Robinia and Quercus ilex, none ours.
Neighbouring registered trees (not ours, for later): Groene beuk Cantonspark nr 1696954 (440 cm, 26 m), Amerikaanse eik Pekingtuin nr 1677543 (590 cm, 25 m).
