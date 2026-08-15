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

