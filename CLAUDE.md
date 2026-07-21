# Ancient Trees — Project Instructions

## What this project is

Ancient Trees is a discovery platform that maps the 10 most remarkable ancient trees in the 100 most-visited cities worldwide. The owner is Hidde, a designer and tree enthusiast based in the Netherlands. The system researches, verifies and publishes; readers correct. Hidde sets direction, he is not the quality gate.

The end product: a website (ancienttrees.app) with an interactive map and one SEO page per city ("10 Most Beautiful Ancient Trees in [City]"), later followed by an iOS app with a freemium model (2 trees free per city, €19,99/year for full access).

## Repository structure

```
/data/cities/          — one JSON file per city (see schema below)
/data/collections/     — one JSON file per collection page (hand-curated, Contract D)
/data/species/         — one JSON file per species page intro (hand-written, gates Contract F)
/data/city-list.json   — the prioritized list of 100 cities with status
/site/                 — static site generator (Astro or similar)
/scripts/              — automation scripts
/CURATION.md           — log of what could not be verified, and notes worth keeping. Not a to-do list for Hidde.
/SEO_GEO_BLUEPRINT.md  — page contracts (titles, schema, internal links, content minima). No page ships without conforming to it.
/TONE_OF_VOICE.md      — the voice for all stories and page copy. Paris is the calibration standard.
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
      "story": "150-250 words. Specific, historical, vivid. No filler.",
      "verified_sources": ["url1", "url2"],
      "access": "Free / paid entry / restricted",
      "transport": "Nearest station + walk time",
      "photo": {
        "url": null,
        "license": null,
        "attribution": null,
        "status": "missing | found_needs_check | approved"
      },
      "curation_status": "ai_generated | hidde_approved | flagged",
      "location_precision": "confirmed | approximate"
    }
  ]
}
```

## The research workflow (autonomous run)

Runs hourly around the clock via GitHub Actions. Most attempts hit the Claude usage limit and stop immediately, which is expected and costs almost nothing; the work goes through whenever the window has room.

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
150-250 words per tree (the Paris run of 2026-07-15 sets the standard; anything over 250 words gets shortened). Style rules:
- Direct, specific, slightly vivid. Scott Galloway meets nature writing.
- Lead with the most surprising fact.
- Include what the tree has "witnessed" historically.
- Never use: "hidden gem", "must-see", "breathtaking", "nestled".
- Never use em dashes.

Stories and any page copy must satisfy SEO_GEO_BLUEPRINT.md — in particular P2 (answer first, in the first two sentences where the page is a question/city page) and P3 (unique content, no fill-in-the-city-name templating) — and follow TONE_OF_VOICE.md, including its calibration examples and hard bans.

### Step 4 — Find photos
Search Wikimedia Commons and other openly-licensed sources (CC0, CC-BY, CC-BY-SA only). Record the exact license and attribution. If no good photo exists, set photo status to `missing`. NEVER use photos from monumentaltrees.com, Google Maps, or any source without a clear open license.

### Step 5 — Commit and update state
- Save the city JSON file
- Update city-list.json (status: pending → needs_curation)
- Append to CURATION.md: city name, date, number of trees, number flagged, photos missing
- Commit with message: "Add [city]: 10 trees, X flagged, Y photos missing"
- Rebuild the site so the new city page goes live. The generated pages (city, tree, question, collection) must conform to the Layer 2 contracts in SEO_GEO_BLUEPRINT.md — titles, meta descriptions, schema, and internal link minima. A page that fails that validation does not deploy.

### Improvement mode (when all 100 cities have data)
Cycle through existing cities oldest-first and: hunt for missing photos, strengthen weak stories, re-verify flagged items, check for dead trees in the news.

### Collections (any time coverage allows)
data/collections/BACKLOG.md holds the prioritized queue of collection pages, with per-item triggers for when coverage suffices. At most one new draft at a time, and per Contract D a draft never publishes without Hidde's approval: it ships with status needs_curation and gets logged in CURATION.md.

### Step 0b — Process reader submissions (before picking a new city)

Readers submit trees and whole cities through a public form. Hidde is deliberately not in this loop: submissions come straight to you.

If `SUBMISSIONS_CSV_URL` is set in scripts/build_site.py, fetch it at the start of every run. Each row is one submission. Skip any row whose id already appears in `data/submissions-processed.json`.

For each new submission:
1. Treat it as a research lead, never as fact. A submitter saying a tree is 500 years old is a claim to verify, not a source.
2. Apply the exact same bar as your own research: two independent sources for existence, species and age, and a location you can place precisely. The hard rules still apply in full, especially "never fabricate" and "photos need a verified open licence".
3. If it verifies: write the story in the tone of voice, add it to the right city file, and credit the submitter by the name they gave (`"submitted_by"` on the tree). If the city does not exist yet, create it as a new city file with the submitted trees, and set its status to `needs_curation`.
4. If it does not verify: do not publish it. Record it in CURATION.md under the submission's city with what is missing, so Hidde or a later run can pick it up.
5. Either way, append the row id to `data/submissions-processed.json` so it is never handled twice, and note the outcome in CURATION.md.

A submitted tree that verifies is worth more than a new city researched from scratch, because it proves someone cares about that city. Process submissions first, then continue with the next pending city if the usage window still allows.

## Quality gate: the research standard, not Hidde

Hidde is not the quality gate and will not be at 1,000 trees. Do not write anything that promises human review. The bar is the standard you already apply: two independent sources for existence, species and age, and a location you can place. Readers are the correction layer.

That puts the weight on you, so two rules tighten:
- **Publish what verifies, flag what does not.** A tree you cannot confirm does not go live with confident phrasing. State the range, name the disagreement (P7).
- **Set `location_precision` on every tree**, `"confirmed"` or `"approximate"`. Approximate means you know the park or street but not the spot. The site shows a visible warning next to the directions button for approximate pins, because sending someone to wander a park is a broken promise. Never mark a pin confirmed to make a page look tidier.

`curation_status` and the `status` field on a city stay in the data as internal signal, but they no longer gate publication and no longer show on the site.

## Hidde's curation workflow (optional, when he feels like it)

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
7. NEVER ship a page (tree, question, city, or collection) that doesn't conform to SEO_GEO_BLUEPRINT.md. Changes to that document itself require Hidde's explicit approval and a version bump.
8. Superlative claims ("oldest in Europe", "largest of its kind", "more than X and Y combined") must be checked against what other city pages already claim before publication. When in doubt, soften to "one of the oldest" or drop the claim.
9. Use one canonical common name per species so the species pages (Contract F) group correctly. When a species has multiple valid common names, pick the nationality-neutral one and match what other cities already use (e.g. Quercus robur is "Pedunculate Oak", never "English Oak"; Platanus x acerifolia is "London Plane"). The scientific name in parentheses is the tiebreaker for whether two trees are the same species.

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
