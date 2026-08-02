# REVIEW — the fresh-eyes findings

Written daily by the Fresh-eyes review workflow (06:10 UTC): a separate,
empty context reads the last day's changes and the built site against the
corpus, and writes findings here, newest first. It never fixes anything.

Severities: **BLOCKER** (the site is wrong or broken; runs treat as rung 2),
**WARN** (drift or risk; rung 3), **NOTE** (worth knowing, no action forced).
"FOR HIDDE" appears only on judgment calls no run may make alone.

An empty day says "Nothing found." A reviewer that never finds anything is
suspect; a reviewer that finds fifteen nitpicks a day is worse.

---

## 2026-08-02 (second pass)

**WARN** — CLAUDE.md's Step 3 (`best_time`) was widened today (commit 63b7b51) to
document a third season family, "bare winter structure," with the explicit
instruction `Use kind: bare silhouette`. But `scripts/build_site.py`'s
`KIND_ICONS` dict (line 927) only defines five kinds: `flowers`, `fruit`,
`autumn colour`, `catkins`, `fresh leaves`. `season_kind()` (line 950) treats
any kind not in that dict as invalid: it appends to the global `ERRORS` list
and `main()` (line 4555) fails the entire build (`sys.exit(1)`, "nothing
deployed") the moment `ERRORS` is non-empty. No tree currently sets
`kind: "bare silhouette"` (checked every `data/cities/*.json`), so the build
is not broken today, but CLAUDE.md now actively instructs the next run to
write exactly that string onto "a hollow, buttressed or wildly limbed
veteran" tree, and the first one that does will silently take the whole site
down at build time with no visible symptom until the deploy fails. This is a
corpus/code mismatch of the kind the 2026-07-29 QA-ratchet rule exists to
prevent ("the fix ships WITH a check"), except here the instruction shipped
without the code it depends on. Fix is small: add a `bare silhouette` entry
to `KIND_ICONS` (and ideally a `KIND_HINTS` derivation entry) before this is
next relied on.

**WARN** — `data/cities/lisbon.json`'s new `lis_011` ("The Fig of the Estrela
Garden", added today in 63b7b51) produces a meta description that cuts off
mid-sentence and loses its own point. The story's opening sentence is "The
city of Lisbon has bolted a small metal plate to this trunk giving the
species, the country it came from and, where the age should be, a single
word: unknown." (162 chars). `meta_from_story()` (build_site.py line 861)
truncates any over-length first sentence at `DESC_MAX` (155) with no ellipsis,
so the live meta description on `site/dist/lisbon/fig-of-the-estrela-garden.html`
reads "...where the age should be, a single word" and stops there, never
naming the word ("unknown") that is the entire hook of the sentence. Verified
live in the rendered HTML. Violates Contract A's meta description spec
("Answer + hook: what it is, why it's remarkable, one click-reason") since
what should be the click-reason is the exact clause that got cut. Not a new
bug in `meta_from_story` itself (pre-existing, generic), but this is the
story that newly collides with it, and it is live on the site right now.
Fix is either a shorter first sentence in the story, or hardening
`meta_from_story` to prefer ellipsis over losing the sentence's payload.

**NOTE** — Two of yesterday's new-city trees carry `curation_status:
"hidde_approved"` despite Hidde never having seen them: `del_001` (Delft,
"The Black Mulberry of Hofje van Pauw", commit 9515549) and `dbo_002` (Den
Bosch, "The Norway Maple of Bastion Oranje", commit f9ebd36), both written
and committed by autonomous runs. CLAUDE.md's curation section is explicit
that `hidde_approved` is what a tree becomes only when "he asks to curate"
and approves it; every other city opened by a run in the same window (Cork,
Osaka, Seoul, Athens) correctly uses `ai_generated` or `flagged` for its
entries. `curation_status` no longer gates or shows on the site (blueprint
v1.2), so this has no visitor-facing effect, but it corrupts the one field
that records who actually vetted a tree, for exactly the two entries the
runs judged strongest. Worth a grep-and-fix (`grep -l '"hidde_approved"'
data/cities/*.json` and check each against LOG.md/CURATION.md for an actual
Hidde session) rather than a rule change.

## 2026-08-02

**BLOCKER** — Every tree page and question page ships self-contradicting
BreadcrumbList schema for the country crumb (`scripts/build_site.py`,
`crumb_items` at line 2190 for tree pages, line 2374 for question pages;
`breadcrumb_schema()` at line 1070). The country entry is always passed with
`url=None`, so `breadcrumb_schema`'s fallback (`item = url or page_url`,
line 1078) sets its `item` to the current page's own canonical URL. Verified
live on `site/dist/amsterdam/amstelkade-olive-willow.html`: the JSON-LD
BreadcrumbList lists position 2 as `{"name": "Netherlands", "item":
"https://ancienttrees.app/amsterdam/amstelkade-olive-willow"}` and position 4
as `{"name": "The Amstelkade Olive Willow", "item":
"https://ancienttrees.app/amsterdam/amstelkade-olive-willow"}` — the same
URL asserted to be two different, differently-named pages. This is not
edge-case: it happens on every tree/question page regardless of whether a
country page exists (same defect confirmed on `cork/witchs-yew.html`,
Ireland has no country page yet). Only the city-page builder (line
2455-2456) actually looks up `country_pages` for a real URL; the tree and
question page builders never picked up that lookup when Contract G shipped
yesterday (commit b71072c, "Country pages ship"). Violates P4 ("every fact
that appears as prose also appears as structured data... schema is not an
add-on, it is the second rendering of the page") and is exactly the
self-contradicting-page failure class the 2026-07-29 QA walk was written to
catch. Visible effect beyond the schema: on tree pages the Netherlands
breadcrumb still renders as plain, unlinked text even now that `/netherlands`
exists, while the city page one level up correctly links it — an
inconsistency between two page types describing the same fact.

**BLOCKER** — `data/countries/netherlands.json`'s `meta_description` says
"Sheltered survivors across **11** mapped cities", and that exact string is
emitted verbatim as the `<meta name="description">`, `og:description`, AND
the `CollectionPage` schema `description` on the live `/netherlands` page
(`scripts/build_site.py` line 2996: `description =
intro_data.get("meta_description", "")`, used as-is). The same page's
answer-first paragraph and its own rendered city list say "**13** cities"
and list 13 rows summing to 66 trees, which is the correct, current count.
Delft and Den Bosch shipped yesterday (commits 951554, f9ebd36), taking the
Netherlands from 11 to 13 published cities, without the hand-written intro
file being updated. Result: the page's search snippet, its social-share
description and its own machine-readable schema all state a stale number
that the page's own H1 paragraph immediately contradicts. Violates P7
("truth outranks polish") and P2 (the answer-first sentence should be
quotable standalone; here two different "quotable" numbers exist on the
same page). Fix is a one-line edit to the `meta_description` field in
`data/countries/netherlands.json`.

No FOR HIDDE on either: both are build bugs a run can fix directly
(re-derive the country breadcrumb URL for tree/question pages the way the
city page already does; edit one string in the Netherlands intro file).
