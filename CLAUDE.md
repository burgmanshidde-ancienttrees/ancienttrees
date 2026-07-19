# Ancient Trees — Project Instructions

## What this project is

Ancient Trees is a discovery platform that maps the 10 most remarkable ancient trees in the 100 most-visited cities worldwide. The owner is Hidde, a designer and tree enthusiast based in the Netherlands. He curates; the system builds.

The end product: a website (ancienttrees.app) with an interactive map and one SEO page per city ("10 Most Beautiful Ancient Trees in [City]"), later followed by an iOS app with a freemium model (2 trees free per city, €19,99/year for full access).

## Repository structure

```
/data/cities/          — one JSON file per city (see schema below)
/data/city-list.json   — the prioritized list of 100 cities with status
/site/                 — static site generator (Astro or similar)
/scripts/              — automation scripts
/CURATION.md           — running list of items awaiting Hidde's review
```

## The tree data schema

Every city file follows this exact structure (see data/cities/london.json for the reference example):

```json
{
  "city": "London",
  "country": "United Kingdom",
  "status": "needs_curation | curated | published",
  "trees": [
    {
      "id": "lon_001",
      "name": "The Totteridge Yew",
      "species": "European Yew (Taxus baccata)",
      "age_estimate": "2000 years",
      "age_min": 1000,
      "age_max": 2000,
      "location": {
        "address": "...",
        "latitude": 51.6323,
        "longitude": -0.2002,
        "neighbourhood": "..."
      },
      "story": "150-220 words. Specific, historical, vivid. No filler.",
      "verified_sources": ["url1", "url2"],
      "access": "Free / paid entry / restricted",
      "transport": "Nearest station + walk time",
      "photo": {
        "url": null,
        "license": null,
        "attribution": null,
        "status": "missing | found_needs_check | approved"
      },
      "curation_status": "ai_generated | hidde_approved | flagged"
    }
  ]
}
```

## The nightly workflow (autonomous run)

Each run, do exactly this, in order:

### Step 0 — Read state
Read `/data/city-list.json`. Find the next city with status `pending`. If all cities are done, switch to improvement mode (see below).

### Step 1 — Research the city's trees (BE THOROUGH)
Search the web extensively for the city's most remarkable trees. Minimum research per city:
- Search "[city] oldest trees", "[city] remarkable trees", "[city] monumental trees", "[city] famous historic trees" — in English AND the local language
- Check municipal/government tree registries (many cities have official "great trees" lists)
- Check monumentaltrees.com for verification of age/location claims (NEVER copy their photos or text — verification only)
- Check Atlas Obscura, local history blogs, park authority websites
- A tree qualifies if it is: genuinely old OR visually spectacular OR historically significant, AND publicly accessible

### Step 2 — Verify each tree
For each candidate tree, cross-reference at least 2 independent sources for:
- Existence and species
- Approximate age
- Exact location (GPS coordinates)
If sources conflict or only one source exists, include the tree but set `curation_status: "flagged"` with a note explaining the uncertainty.

### Step 3 — Write the stories
150-220 words per tree. Style rules:
- Direct, specific, slightly vivid. Scott Galloway meets nature writing.
- Lead with the most surprising fact.
- Include what the tree has "witnessed" historically.
- Never use: "hidden gem", "must-see", "breathtaking", "nestled".
- Never use em dashes.

### Step 4 — Find photos
Search Wikimedia Commons and other openly-licensed sources (CC0, CC-BY, CC-BY-SA only). Record the exact license and attribution. If no good photo exists, set photo status to `missing`. NEVER use photos from monumentaltrees.com, Google Maps, or any source without a clear open license.

### Step 5 — Commit and update state
- Save the city JSON file
- Update city-list.json (status: pending → needs_curation)
- Append to CURATION.md: city name, date, number of trees, number flagged, photos missing
- Commit with message: "Add [city]: 10 trees, X flagged, Y photos missing"
- Rebuild the site so the new city page goes live (marked "awaiting curation" until Hidde approves)

### Improvement mode (when all 100 cities have data)
Cycle through existing cities oldest-first and: hunt for missing photos, strengthen weak stories, re-verify flagged items, check for dead trees in the news.

## Hidde's curation workflow

When Hidde opens a session, FIRST show him the top of CURATION.md: what's new, what's flagged, what needs photos. Prioritize his time on:
1. Cities he knows personally (Amsterdam, Lisbon, London, European cities)
2. Flagged items with uncertainty
3. Photo approvals

When he approves a city, set status to `curated` and each tree to `hidde_approved`.

## Hard rules

1. NEVER use content, photos, or text from monumentaltrees.com beyond fact verification. Their disclaimer prohibits commercial reuse.
2. NEVER fabricate tree facts. If you cannot verify age or location, flag it. A wrong location kills user trust permanently.
3. NEVER use em dashes anywhere.
4. Photos must have verified open licenses with attribution recorded.
5. Costs matter: this project targets max €50/month total. Keep runs efficient. One city per night is enough.
6. The goal is revenue, not a beautiful product nobody buys. If Hidde starts adding features before validation, remind him: "Have we validated that real people will pay for this?"

## Current state (as of handover)

- Amsterdam: researched in chat, needs to be converted to schema (10 trees identified: Olifantsiep, Leidsebosje platanen, Vondelpark Canadapopulier, Wertheimpark vleugelnoot, Hortus cycad, Artis oak, Lomanstraat X-trees, Amstelkade olijfwilg, Amstelveld vleugelnoten, Frederiksplein vleugelnoot)
- London: complete in schema (london.json exists with 10 trees, 6 verified, 2 need location verification)
- Landing page: HTML file exists (light minimal design, Playfair Display, waitlist form)
- Website content doc: exists with copy for homepage, about, blog structure
- City list: 100 cities prioritized in 4 tiers (Tier 1: Amsterdam, Lisbon, London, Paris, Rome, Tokyo, Istanbul, Barcelona, Kyoto, Madrid, New York, Singapore, Vienna, Prague, Bangkok, Berlin, Seville, Porto, Athens, Florence)

## First session goals

1. Set up the repository structure
2. Import the existing London data and Amsterdam research
3. Build the static site skeleton: homepage + city page template + interactive map (MapLibre + OpenStreetMap, no paid services)
4. Set up the GitHub Action for nightly runs
5. Do one test run on Paris to validate the workflow end-to-end
