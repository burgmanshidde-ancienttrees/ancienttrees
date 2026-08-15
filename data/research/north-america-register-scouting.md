# North America register scouting, 2026-08-15

Scouting pass aimed at semi-big US/Canadian cities per Hidde's thesis: Boston
(published, 10 trees, our best-converting American page at 62 impressions)
proves the format works in North America; Charleston, Savannah, New Orleans,
Austin, Seattle, Philadelphia, Vancouver, Montreal and Quebec City are
unpublished with real demand. Method and bar per OPEN_DATA_SURVEY.md: licence
must permit commercial-leaning reuse, quote the proving sentence verbatim,
semantic filter (designated/champion/heritage trees only, never a bulk
street-tree inventory), per-tree coordinates strongly preferred.

Note: `data/registers/portland-heritage-trees.json` already exists (Portland
Heritage Trees, referenced in fetch-blocklist.json under portlandmaps.com), so
a US municipal heritage-tree register import is already a proven pattern here.
Not re-scouted this pass since it is already imported.

---

## 1. American Forests National Champion Trees register

**VERDICT: BLOCKED on licence.** The interactive "search the register" widget
advertised on `americanforests.org/champion-trees/champion-trees-registry/`
no longer functions as a live search (the page is a 2021 snapshot, "Welcome
to the 2021 National Register of Champion Trees!"); the only real distribution
is a static Excel-exported PDF:
`https://d3f9k0n15ckvhe.cloudfront.net/wp-content/uploads/2021/11/2021-National-Register-of-Champion-Trees.pdf`
(700 KB, 6 pages, PDF metadata `Producer: Microsoft Excel 2016`, no embedded
licence or rights statement anywhere in the document).

Confirmed by fetch and by PDF text extraction (pypdf): a genuine flat table,
Record Reference Number / Year Nominated / Nominated By / Scientific name /
Circumference / Height / Crown Spread / Total Points / Year Last Verified /
Last Reported Tree Health / Current Status / Date Crowned / **County / State**.
This IS a semantic-filter pass (every row is a designated National or
Co-Champion, not a bulk inventory), and health/status fields even give a
vitality signal for free ("Excellent/Good/Fair/N/A", "Champion/Co-Champion",
occasional "Deceased"). **But there are no coordinates and no city, only
county and state** ("Travis TX", "King WA", "Philadelphia PA" each appear;
Suffolk/Middlesex/Norfolk MA, Charleston SC, Chatham GA and Orleans LA each
appear zero times, i.e. no in-city Champion for Boston, Charleston, Savannah
or New Orleans specifically in this national list). Even with a licence this
table is county-precision at best, a lead list requiring per-tree
geolocation, same tier as Nara's town-level XLSX.

**The licence question, checked directly, is the real blocker.** No terms-of-
use, terms-and-conditions or legal/licensing page exists on americanforests.org
(`/terms-of-use/`, `/terms-and-conditions/`, `/terms/` all 404; `/legal/`
redirects to an unrelated 2012 blog post about environmental law). The only
rights statement anywhere on the site is the standard WordPress footer on
every page including the registry page itself:

> "Copyright © 2026 American Forests. All Rights Reserved."

No CC licence, no public-domain statement, no explicit reuse permission
anywhere, on the page, in the PDF, or in a dedicated terms page. Per this
project's own standard (an explicit named licence, quoted verbatim, never an
absence of a prohibition) an all-rights-reserved footer with no countervailing
licence statement is a clean disqualification, the same pattern as Kyoto's
誇りの木 register and Ishikawa's cultural-properties database above.
**Do not import.** Usable only as a verification-only lead source the way
monumentaltrees.com is treated under hard rule 1: it can confirm a species/
size claim found elsewhere, never be copied or bulk-imported. If Hidde wants
this unlocked, the path is the same shape as the Woodland Trust: email
American Forests asking for explicit reuse permission (nonprofit, likely to
say yes, but that is his call and his email per hard rule 4).

---

## 2. State champion-tree registers

### Massachusetts: USABLE (public record), IMPORTED

**Boston is exactly the mid-competition/real-demand city the thesis names,
and this register substantially deepens it.** DCR (the Bureau of Forest Fire
Control and Forestry) publishes two downloadable spreadsheets from
`https://www.mass.gov/guides/massachusetts-legacy-tree-program`:

- `Champion Trees 2026`, https://www.mass.gov/doc/champion-trees/download,
  139 rows, the single largest known specimen of each species statewide,
  field-verified in person by a trained DCR forester (the page's own
  description of the nomination process), feeding the National Champion Tree
  Program register.
- `Legacy Trees 2026`, https://www.mass.gov/doc/massachusetts-legacy-tree-list-0/download,
  476 rows, a broader ranked list per species (state's 1st, 2nd, 3rd... largest
  of a species), a superset of the Champion list.

Both are genuine xlsx files (not PDFs despite the URL slug), columns:
Scientific Name, Common Name, **Location (if Publicly Available)**, City,
County, Date Measured, Circumference, Height, Average Crown Spread, Champion
Points, Notes, (Rank on the Legacy list). This is a real semantic designation,
not a bulk inventory: every row is a field-verified largest-of-species record.

**Licence, read in full, genuinely two-tier like Castilla y Leon's IGCYL-NC
rather than a clean CC tag.** `https://www.mass.gov/massgov-terms-of-use`,
section "Public records and copyright", quoted verbatim:

> "All of the material posted on the Commonwealth's websites and available to
> the public without use of an authenticating and authorizing mechanism (such
> as a 'PIN' or password) is public record. Most of the public record posted
> on Commonwealth websites can be copied and used for any purpose."

The same page separately restricts "most of the content on Mass.gov" (its
own words: design, layout, prose) to fair use. Read plainly, the page draws
exactly the line this project's bar draws: **factual government records
(what this spreadsheet is: species, address, county, field measurements
compiled by state foresters under an official program) versus copyrightable
editorial content (design, layout, articles)**. This falls on the public-record
side, which matches the "US federal/state public domain" category the brief
names as acceptable. Recorded honestly as a two-tier reading rather than a
clean licence name, exactly the discipline the Castilla y Leon entry above
sets: the name is not a CC tag, but the terms as read permit commercial-
leaning reuse of the data.

**No coordinates.** `Location (if Publicly Available)` is free text, an
address or landmark name ("28 Moreland St", "Mount Auburn Cemetery"), null
for some rows (private-land trees the sheet itself declines to locate
publicly, which is itself a hard-rule-10 signal worth honouring). This is a
lead list needing geocoding, same tier as Nara's town-level Japanese list,
not a coordinates-in-hand import.

**No vitality field.** Only `Date Measured`, some from the 2010s. Alive-now
is a per-tree check, as with every register scanned so far.

**Imported to `data/registers/massachusetts-dcr-legacy-trees.json`** (139
champion + 476 legacy rows, full licence block, both lists kept since Legacy
is the superset but Champion marks the clean state-record subset).

**Which cities this unlocks, counted directly:**
- Boston (city proper): only 2 rows (a green ash on Moreland St, a
  witch-hazel in the South End). Thin on its own, consistent with Boston's
  existing published page already having taken the obvious Boston-proper
  candidates.
- **Greater Boston (Boston + Cambridge + Somerville + Watertown + Brookline +
  Newton + Quincy + Chelsea + Medford + Malden + Milton + Arlington): 83
  rows.** The standout cluster: **Mount Auburn Cemetery**, straddling
  Watertown/Cambridge about 4 km from downtown Boston, accounts for roughly
  25 of those 83 across a wide species range (European beech, Dawn redwood,
  Cedar of Lebanon, Katsura, Japanese maple, Kentucky coffeetree, Norway
  spruce and more) all inside one walkable, already-touristed cemetery-
  arboretum. This is precisely CLAUDE.md's "cheapest cluster" pattern (dense
  x data-rich, state already field-verified species/size/location): a strong
  candidate for deepening Boston's page or, if it clears the day-trip/cluster
  bar on its own, its own city entry.
- No relevant rows found in this dataset for cities outside Massachusetts, by
  definition (state register).



