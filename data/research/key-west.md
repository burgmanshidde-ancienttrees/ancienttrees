# Key West research notes, 2026-09-25 (session)

Claimed via passcheck.py --claim key-west --kind verify. City is currently
UNPUBLISHED (rank #80 in city-queue.json, 0 trees, 0 register rows, 0 ready
leads). scout_next.py --target (limit 60) named it next in strict rank order
after Chattanooga (recorded stalled) was resolved.

## What was scouted and rejected

- City of Key West "Heritage Tree Program" (cityofkeywest-fl.gov/634): a
  nomination/application process (Jan 1 - Jun 30 each year), no published
  list of designated trees found. Not usable as supply.
- No Monroe County / Key West ArcGIS "notable tree" or "champion tree"
  layer found via arcgis.com item search.
- Florida's own Champion Tree register lives at ffs.fdacs.gov, which is on
  the hosts-that-hang list in CLAUDE.md (connection refused). Not chased
  further this pass; a Wayback snapshot may work per that entry's own note.

## What was found: Key West Tropical Forest & Botanical Garden

11 acres (historically 55, WPA project from 1936, landscape architect Ralph
Ellis Gunn), 5210 College Road, Stock Island, Key West, FL 33040.
Approx. 24.5737, -81.7493 (garden entrance area; not tree-level precision).
Open daily, paid admission with free entry for locals the first Sunday of
the month (access = paid entry, state it honestly). Operated by the
non-profit Key West Botanical Garden Society. ArbNet Level II accredited
arboretum (arbnet.org/morton-register/key-west-tropical-forest-botanical-garden).

The garden holds/held several trees designated National or Florida Champion
or Challenger by American Forests / the Florida Division of Forestry, per
the garden's own "gallery of champions" page and Wikipedia's article on the
garden. IMPORTANT: Hurricane Irma (Sept 2017) killed or badly damaged
several of them. Current status per the garden's own page (archived
2024-07-21, since the live site returns a bot-challenge to plain fetches
and needs Wayback: http://web.archive.org/web/20240721221529/https://www.keywest.garden/our-gallery-of-champions/):

Native Champions and former Champions:
- Milkbark (West Loop), National Champion -- "Down but seedlings growing
  from roots". DO NOT PUBLISH: the original trunk is down, only root
  suckers survive. Same shape as the never-dead-tree rule.
- Pigeon Plum (Northside pond), National Champion -- "Destroyed". DO NOT
  PUBLISH, dead.
- Saffron Plum (Parking Lot), Challenger -- "OK". Candidate.
- Cinnamon Bark (West Loop) -- "OK". Candidate (champion status unclear,
  check).
- Wild Dilly (West Loop), Former National Champion -- "Partially down but
  still alive". Judgement call: alive per the source's own words, but
  visibly storm-damaged; if published, say so honestly rather than
  presenting it as an intact champion.
- Black Olive (Boardwalk), Challenger -- "Down but growing suckers".
  Same shape as Milkbark: likely DO NOT PUBLISH unless a fresher source
  shows the trunk itself standing again.
- Cuban Lignum Vitae (Boardwalk), State/Florida Champion -- "OK". Strong
  candidate.
- Locustberry / Locust-berry (Western Loop), National Champion (Byrsonima
  lucida) -- "OK". Strong candidate; American Forests search snippet
  independently confirms it as a genuine National Champion with real
  measurements: 57in circumference, 17ft height, 17ft crown spread, 78
  total points, nominated/crowned 2014 (americanforests.org/tree/long-key-
  locustberry-fl/ -- the page itself would not render through WebFetch in
  this pass, served unrelated cached content; try again with a direct
  fetch or the National Register PDF at
  https://d3f9k0n15ckvhe.cloudfront.net/wp-content/uploads/2021/11/2021-National-Register-of-Champion-Trees.pdf).

Historic Legacy Trees (not champions, but named, photographed, dated to
the 1936 planting per ArbNet's page on the garden's history):
- African Tulip Tree (Boardwalk) -- "Broken at about 20 feet but alive and
  growing suckers". Judgement call, same as Wild Dilly: alive but storm-
  damaged, say so if published.
- Arjun Almond / Arjan Almond (Boardwalk), Former Champion -- "OK".
  Candidate.
- Sausage Tree (Parking Lot) -- "OK". Candidate.
- Canary Date Palm (Desbiens Pond) -- "OK". Candidate, but it is a PALM;
  check house style on whether palms count as trees elsewhere on the site
  before using it (species pages/collections may implicitly assume
  dicot/conifer trees).
- Barringtonia (Boardwalk), Florida Champion (Barringtonia asiatica) --
  "OK". Strong candidate.

## What a verify pass still needs to do

1. Get the scientific name right for each candidate (Saffron Plum =
   Sideroxylon celastrinum or Bumelia celastrina; Cinnamon Bark =
   Canella winterana; confirm before writing).
2. Find a genuinely independent SECOND source for species + champion
   status per tree (the garden's own page is source one for all of them).
   Try: americanforests.org's tree pages (site did not render cleanly this
   pass, may need a different fetch approach or the PDF register above),
   the Florida Division of Forestry's champion tree list (ffs.fdacs.gov,
   known to hang -- try Wayback), local press (Key West Citizen, Florida
   Keys News) covering the garden's champions or Irma damage, or
   Wikipedia's own citations on the garden's article.
3. Check for a MORE RECENT status update than the 2024-07-21 Wayback
   snapshot -- fetch the live gallery-of-champions page through Wayback's
   newest capture, or check the garden's newsletter/Facebook for a 2025-26
   update, since "down but growing suckers" could have changed either way
   in two years.
4. No age is published anywhere found so far; leave age_estimate empty
   and flag it (Step 2: missing age is fine).
5. Location precision: the garden is 11 acres with each tree noted only
   by informal area name (Boardwalk, West Loop, Parking Lot, Desbiens
   Pond) -- location_precision should be "approximate" unless a per-tree
   coordinate can be found (e.g. the garden's tree map at
   keywest.garden/garden-tree-map/, not yet checked).
6. This is ONE institution (a botanical garden), so all trees share one
   address; per CLAUDE.md's cluster guidance this reads as a single tight
   cluster (a garden, like Cadiz), which is exactly the case the count
   doctrine wants: pick the ones that clearly pass the bar (verified
   alive, named, distinguishable), leave out the dead/ambiguous ones.
   Floor is 4; there appear to be 5-8 clearly-alive named candidates
   above, comfortably clearing it.
