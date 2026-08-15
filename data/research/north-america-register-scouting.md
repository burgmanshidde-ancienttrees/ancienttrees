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




### Texas: BLOCKED on licence (explicit non-commercial), data quality is excellent, worth a permission ask

**The Texas Big Tree Registry has genuinely the best-shaped data found this
whole pass**, better than Massachusetts: a live ArcGIS Feature Layer, not a
static file, found by reading the registry web app's own Angular config
(`tfsweb.tamu.edu`'s search app ships its data source URL in plain JS):

`https://tfsgis02.tfs.tamu.edu/arcgis/rest/services/BigTreeRegistry/BigTreeRegistry/MapServer/1`

239 records live now (`?where=1=1&returnCountOnly=true`), each carrying:
species (Latin + common), circumference/height/spread/TreeIndex (the scoring
formula), **StateChampion/NationalChampion/ChampionType flags**, county,
organization/site name, **LatDec/LongDec (WGS84 decimal degrees, per-tree,
already the right coordinate system)**, **PublicOrPrivate flag (202 of 239
= 1/public, 35 = 0/private)**, and **Condition (1-5, a genuine per-tree
vitality-adjacent field, codes not yet decoded from this pass, worth
resolving before import)**. Travis County (Austin) has **8 records** in the
current 239.

**Licence, read at the primary source, and it is a clean no.**
`https://tfsweb.tamu.edu/accessibility-site-policies-and-public-notices/`,
section "Fair use", quoted verbatim:

> "Texas A&M Forest Service invites visitors to use its online content for
> personal, educational, and other non-commercial purposes."

And further down the same section: reuse is conditioned on citing the source
and complying with "all terms or restrictions other than copyright." This is
an explicit, direct non-commercial restriction, not an absence of a
statement (unlike American Forests above) and not a two-tier public-record
argument (unlike Massachusetts): the agency has spoken to exactly this
question and the answer is non-commercial only. Per the standing bar, this
disqualifies outright. **Do not import.**

**Worth a permission ask, separate from the licence finding.** Texas A&M
Forest Service is a state agency with an educational mission close to this
project's own (Hidde-approval-gated per hard rule 4, same shape as the
Woodland Trust and Kyoto asks already on file): the data is precise,
per-tree, coordinate-bearing and already flags public/private and champion
status, which would make Austin (and San Antonio, Houston, Dallas, Fort
Worth, if ever wanted) nearly free to research once granted. Not drafted this
pass since outreach emails are Hidde's to send and this is a scouting pass,
but flagged here as the single best target if he wants to ask.

---

## 3. The Live Oak Society (Louisiana Garden Club Federation)

**VERDICT: BLOCKED, explicit written-permission requirement, exceptionally rich data.**

Real, and exactly as described: a live-oak membership registry running since
1934, minimum-girth entry bar (8 ft circumference at 4.5 ft), each entry
carrying a name, address, county/parish, girth and sponsor. Distributed as
scanned-to-digital PDFs from `lgcfinc.org/live-oak-society.html`, at least two
files found (`5001-currentapril2019.pdf`, 265 pages, registrations 5001
onward; `6001_6500.pdf` not fetched this pass) plus an earlier 1-5000 range
implied by the numbering but not located in the time available.

**The society's own page states the licence outright, and it forecloses the
question before any file needs opening:**

> "The information contained in the Registry of the Live Oak Society is the
> copyrighted property of the Louisiana Garden Club Federation and the owners
> of the Live Oak trees. Anyone else wishing to use the information for any
> purpose whatsoever must get written permission from the Live Oak Society
> through its Chairman."

"For any purpose whatsoever" is about as unambiguous a block as this project
has found. **Do not import, do not bulk-extract.** This is a written-
permission-path case, same shape as the Woodland Trust and the Texas Big Tree
Registry above: draft sits for Hidde to send if he wants it (hard rule 4),
addressed to the Live Oak Society chairman via the LGCF contact page.

**Why it is worth the ask.** A quick grep of just the one 265-page file
confirms real density in exactly the cities this pass targets: "New Orleans"
appears 139 times, "Charleston" 34 times, "Savannah" 5 times, and the roster
is not Louisiana-only, it already reaches North Carolina addresses (Carteret
County) within the sampled range, confirming it tracks live oaks across the
whole South rather than one state. This single society roster, if permission
arrived, would likely be the single richest unlock for New Orleans and a real
one for Charleston.

---

## 4. Canada


### BC Big Tree Registry (Vancouver): UNRESOLVED, bot-blocked, not disqualified

`bigtrees.forestry.ubc.ca` is real and matches the brief's description: ~600
trees, UBC Faculty of Forestry, a Champions list, a Top 30, and a stated
downloadable Excel with "nominators, verifiers, site and access notes." Could
not be verified this pass: **every path on the domain, including
`/terms-of-use/` and `/bc-bigtree-registry/champion/`, returns UBC's bot-
defense captcha challenge page to a plain fetch** (HTTP 200, but the body is
the captcha itself, not the content). Solving a captcha is off-limits by this
project's own rules regardless. Logged to `data/fetch-blocklist.json`
(`bigtrees.forestry.ubc.ca`, 2026-08-15). **Not disqualified, just unread**:
a session using the Browser pane (a real browser, not curl/WebFetch) should
be able to clear the challenge and read the terms-of-use and the Excel
download properly. Worth a short follow-up, not a from-zero rescan.

### Ontario Heritage Tree Program (Toronto): DEAD END, no exportable data at all

Checked both partner sites, `forestscanada.ca/en/program/heritage-tree`
(the program's current home; Forests Ontario rebranded to Forests Canada) and
`oufc.org/index.php/heritage-tree-program/` (Ontario Urban Forest Council,
co-runs it). Neither publishes a database, map, CSV or any structured export.
Both are nomination-and-plaque programs: individual trees get a blog post and
a certificate, not a register entry. This confirms and extends the earlier
finding that Toronto's own open-data portal carries no city-level tree
designation. **Verdict: no dataset exists to licence-check.** A future pass
would have to compile Heritage Tree recipients from the blog posts
individually, which is from-zero research, not an import.

### Quebec's provincial "arbres remarquables" programme: not scouted as such, but Quebec City's OWN municipal register found instead, and it is excellent

**USABLE, CC BY 4.0, IMPORTED.** Ville de Québec's own open-data portal
publishes `Arbres potentiellement remarquables`
(`https://www.donneesquebec.ca/recherche/dataset/vque_82`), found via the
Données Québec / Government of Canada open-data mirror rather than a
provincial "arbres remarquables" programme, which the search suggests is
Montreal/Mount-Royal specific rather than a real province-wide register (not
independently verified this pass, time-boxed out).

**685 trees, full per-tree point coordinates (WGS84, no geocoding needed,
the best coordinate precision of anything found this whole pass), updated
weekly** (dataset metadata: last modified 2026-08-09). CKAN API confirms
licence directly: `license_id: "cc-by"`, `license_title: "Attribution (CC-BY
4.0)"`, matching the page's own "Licence Attribution (CC-BY 4.0)". Fields:
Latin + French common name, tree type (Feuillu/Conifère), diameter at breast
height, multi-trunk flag, planting date (populated for some rows, a real age
source), and **TYPE_PROP, a direct ownership flag** ("Privés" vs "Public"
and subcategories).

**The hard-rule-10 filter matters more here than anywhere else scanned this
pass**: 594 of 685 rows are privately owned (`Privés`), only **76 are
Public** (60 plain public plus small Public:* subcategories like
"Entretenu Par La Ville"). Only that 76-row subset should ever be considered
for publication; the rest stays in the file as data, never as candidates,
same discipline Brussels' register already established. 76 public,
coordinate-precise, city-designated candidate trees is comfortably above the
four-tree floor for Quebec City, one of the pass's named targets.

**No vitality field**, alive-now stays per-tree, as everywhere else.

Imported to `data/registers/quebec-city-arbres-remarquables.json` (all 685
features kept, TYPE_PROP preserved so a future pass filters correctly rather
than re-deriving the split).
