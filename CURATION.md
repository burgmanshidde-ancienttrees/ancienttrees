# CURATION — items awaiting Hidde's review

Newest entries on top. When you approve a city, its status moves to `curated` and each tree to `hidde_approved`.

## 2026-07-15 — Paris (test run of the nightly workflow)

- 10 trees researched and written, saved to `data/cities/paris.json`
- 7 flagged, mostly for one reason: the tree is confirmed to stand in a given park by two sources, but the exact spot inside the park still needs confirmation. Wrong pin placement kills trust, so these stay flagged until coordinates are verified on the ground or via the Paris open data tree registry.
- 1 flagged for source depth: the Buttes-Chaumont sequoia has only one detailed source so far
- 2 photos found on Wikimedia Commons with valid open licenses (Robinier Rene-Viviani: CC BY-SA 3.0, Cedar of Jussieu: public domain), both marked found_needs_check for your approval
- 8 photos missing
- Suggested follow-up: the Paris open data portal (opendata.paris.fr) has a per-tree registry with exact coordinates for all 200,000 street and park trees. One improvement-mode run could resolve most flagged locations.

## 2026-07-15 — London (imported from earlier research)

- 10 trees imported into the new schema at `data/cities/london.json`
- 2 flagged: The Fulham Palace Oak (photo verification), Barney the Plane (location not confirmed by two sources)
- 10 photos missing: no open-license photo URLs were carried over from the original research, all need a Wikimedia Commons search
- 8 of 10 trees are missing verified source URLs (the original research named sources like Atlas Obscura and Wikimedia Commons but did not record links). These need backfilling before publication.
- Note: Queen Elizabeth's Oak (lon_005) is dead and recumbent since 1991. Decide whether a dead tree belongs in a top 10.

## 2026-07-15 — Amsterdam (skeleton only, not ready for review)

- 10 tree names carried over from chat research, no data behind them yet
- Status stays `pending` so the nightly workflow picks Amsterdam up for a full research run
- Nothing to curate yet
