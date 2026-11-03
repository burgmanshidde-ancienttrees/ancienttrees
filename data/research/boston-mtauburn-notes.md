# Boston, Mount Auburn pass notes (2026-11-03)

Coordinate source: Mount Auburn's own plant inventory GIS behind Flora Mount Auburn (https://flora.mountauburn.org/), a public ArcGIS REST service, no login. Layers "Trees" (FloraReferenceLayers/MapServer/17) and "Trees of Significance" (/16): per-tree lat/lon, species, DBH, height, condition, last check and measure dates, section and avenue pair. About 870 trees with DBH of 30 in or more were pulled to out/tmp/ma_trees.json (scratch). The inventory licence is not stated; only facts (position, species, size, dates) were used, no text. A permission ask to Mount Auburn's plant collections team (their address is on flora.mountauburn.org) would settle it.

DCR rows say only "Mount Auburn Cemetery". Champions were paired to inventory trees by species plus size: inventory DBH (diameter, inches) times pi matches the DCR circumference within 1 to 7 percent for katsura, Nikko fir, cedar of Lebanon, Himalayan pine, dawn redwood, zelkova, spruce. The pairing is inference, flagged in verify_notes.

All pins are `approximate`: the cemetery's mapped point, not confirmed on a crown.
Inventory "1831" is the received-year field with provenance W (wild): older than the cemetery, not a planting year.
Cambridge: London plane across from 40 York St (register only). Harvard Yard not done.
overpass-api.de returned no file (not retried).
