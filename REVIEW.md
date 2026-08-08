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

## 2026-08-08

**BLOCKER** — Vienna's page still says "sixteen" trees, in both visible
prose and machine-readable schema, three trees after today's verify pass
grew it to nineteen (commit e3014de). `data/cities/vienna.json:5`, the
`intro` field: "The sixteen below range from a plane tree Mozart is said to
have walked past... All sixteen are free to see." Line 17, the FAQ answer
to "Are Vienna's ancient trees free to visit?": "All sixteen trees on this
list are free to see." Both render live in `site/dist/vienna.html`: the
intro paragraph under the H1, the visible FAQ `<dd>`, AND the page's own
`FAQPage` JSON-LD (`"acceptedAnswer"` text says "All sixteen trees on this
list are free to see" while the page lists 19 `TouristAttraction` entries
above it). Whoever grew this city updated `meta_description` ("Nineteen
remarkable trees") and `question_meta` ("eighteen more remarkable trees")
correctly but missed `intro` and the FAQ, so the page contradicts its own
schema, not just its own prose. Same defect class as the 2026-08-06
Zaragoza BLOCKER (P2/P7: a page's central numeric claim must match what the
page actually shows), and the ratchet condition applies: this is the
second time in three days a tree-count field has gone stale on publish
(see next finding). Fix is two string edits in `data/cities/vienna.json`.

**BLOCKER** — Paris's meta description and question-page subtitle still
promise "15 more" trees, eight trees after today's pass grew Paris from 16
to 24 (should read "23 more"). `data/cities/paris.json:6`
(`meta_description`: "Meet the 1601 Robinier... and 15 more within a metro
ride.") and line 8 (`question_meta`: "...Its story, exact location, and 15
more remarkable trees nearby."). Both render live: `site/dist/paris.html`'s
`<meta name="description">` (the exact text Google would show in a search
snippet) and `site/dist/paris/oldest-tree.html`'s subtitle. This is not the
first time this exact field has gone stale: LOG.md's 2026-08-07 entry
records a run explicitly catching and fixing this same phrase when Paris
grew 13 to 16 ("both of which said 'a dozen more' trees... now say '15
more'"). It has now gone stale a second time on the very next growth pass,
which is the ratchet condition CLAUDE.md itself defines ("a lesson that
appears on two different days stops being a note and becomes a build
check"). No check in `scripts/qa.py` or `scripts/build_site.py` compares
these copy fields' stated count against `len(trees)`; grep confirms no
such validation exists. Recommend: either a qa.py check that greps
`meta_description`/`question_meta` for a bare number and compares it to
`len(trees) - 1`, or drop the exact count from these fields entirely and
say "more remarkable trees" without a number, which is honest at any city
size and cannot go stale.

**WARN** — Five of the eight Paris trees published today ship a fact-chip
that is a caveat sentence, not a scannable label, repeating a defect
class fixed yesterday on three different Paris trees (par_013-015,
REVIEW.md 2026-08-07, fixed in commit 3d97f07 today). Contract A
(SEO_GEO_BLUEPRINT.md:49) requires the above-the-fold fact block to be
"scannable, no prose." Verified live: `/paris/plane-of-square-dajaccio`'s
age chip reads "likely over a century, since the square was laid out in
the 1860s-1880s"; `/paris/turkish-hazel-of-square-du-temple` reads "not
documented; comparable Corylus colurna elsewhere in Paris date to the
1860s-1880s"; `/paris/chinaberry-of-square-boucicaut` reads "not
documented; the square (created 1870) is known for many century-old
specimens"; two more (`twin-planes-of-avenue-winston-churchill`,
`magnolia-of-square-dajaccio`) are shorter but still full clauses rather
than labels. Today's fix (3d97f07) shortened the three existing offenders
to a plain "not documented" but did not touch `BRIEF_WRITING.md`, which
still has no instruction limiting `age_estimate` to a short phrase, so the
same write-stories pass produced the same defect on new trees the same
day. Per the ratchet: this has now recurred, so a data-only fix will not
hold. Recommend either a `BRIEF_WRITING.md` rule ("age_estimate is a chip
label, not a sentence; put caveats in the story") or a qa.py length/clause
check on `age_estimate` (e.g. flag any value containing a semicolon or
exceeding ~40 characters).

Everything else checked came back clean: both 2026-08-07 BLOCKERs (park
BreadcrumbList, Zaragoza self-contradiction) are confirmed fixed and live;
`qa.py` passes clean (1215 pages); no em dashes or banned words in a
sample spanning today's new tree pages (Paris par_019-026, Vienna
vie_017-019), the homepage, and five unrelated pages picked at random
(Bath, Sofia redirect stub, Guimaraes, Milan, Porto, Athens, Cadiz, Rome,
the olive species page, Venice); species common names stay canonical
site-wide (no scientific name maps to two different common names); no
superlative collisions found among today's "oldest in France" claims
(Paris's cedar of Lebanon and Caucasian wingnut are each the only tree of
their species claiming a France-wide superlative, and both explicitly
attribute the claim to sources rather than asserting it outright, which is
the hard-rule-8 soften-or-attribute pattern working as intended); the new
Ireland Heritage Trees register import (781c1af) stays honest about its
custom coordinate-conversion accuracy and ships `publish_dots: false`, so
it is not user-facing yet.

---

## 2026-08-07

**BLOCKER** — Every Contract H park page ships without BreadcrumbList
schema, contradicting the contract that shipped it yesterday. Contract H
(SEO_GEO_BLUEPRINT.md v1.7, added 2026-08-06) specifies "Schema | ItemList +
BreadcrumbList" and the built pages render a visible breadcrumb nav
(`Home > Parks > [park name]`), but `build_park_page()`
(`scripts/build_site.py:3722`) only appends an `ItemList` to the graph:
`graph = site_graph() + [{"@type": "ItemList", ...}]`, with no call to
`breadcrumb_schema()`. Every other page builder in the file calls it
(question, city, species, country, tree, collection, in-season: 11 call
sites at lines 3081/3181/3351/3499/3616/3806/3993/4039/4089/4143/5238).
Verified live on all 9 published park pages: `site/dist/parks/giardini-
montanelli-milan.html` and `site/dist/parks/york-museum-gardens.html` both
show `WebSite`, `Organization`, `ItemList`, `ListItem` in their `@graph` and
no `BreadcrumbList`. Violates hard rule 7 ("NEVER ship a page that doesn't
conform to SEO_GEO_BLUEPRINT.md") and P4 (every fact visible in prose must
also be structured data) for a page type that has existed for about 18
hours across 9 live URLs. Fix is one line in `build_park_page()`: append
`breadcrumb_schema(crumb_items, canonical)` to `graph`, matching every
other page type.

**BLOCKER** — `/zaragoza/oldest-tree.html` still contradicts itself after
yesterday's fix, on the exact page that fix's own commit message named as
the worst case. `age_token()` now correctly reads "150" out of zar_001's
own `age_estimate` string ("Centennial, no exact figure recorded, probably
around 150 years"), so the `<title>` reads "(150 Years Old)". But the
city's hand-written `question_answer` (data/cities/zaragoza.json), rendered
as the page's answer-first opening paragraph, still opens "Nobody has
established it," then explains the best a source offers is "roughly 150 to
180 years" for unnamed candidates and that the one tree with any public age
claim (zar_001, the page's own mechanically-picked "oldest") only carries
the word "centennial." A visitor reads a title asserting a specific age and,
one paragraph later, the page's own text saying nobody knows it. Same
defect class as yesterday's fixed BLOCKER (P2/P7: the quoted title must be
true, and a flagged uncertainty must not be overwritten by manufactured
precision), different mechanism: `age_token()` is now faithful to the
individual tree's own field, but nothing checks that number against what
the hand-written `question_answer` actually asserts about the page's
central claim. Swept all 91 city files for the same shape (mechanically-
picked oldest tree has a numeric age, but `question_answer` opens with
"nobody"/"no one"/"not established"/"unknown"); Zaragoza is the only match,
so this is narrow, not systemic. `data/cities/zaragoza.json` was not
touched in the reviewed window, so this is a pre-existing gap that survived
the fix rather than a new regression. Fix is data-side: either give
zar_001 an honest range (`age_min`/`age_max` only, no bare `age_estimate`
number) so `age_token()` has nothing false to quote, or rewrite
`question_answer` to state the 150-180 range as the answer instead of
opening with a flat denial the title then contradicts.

**WARN** — The three new Paris trees added today (par_013-015, commit
b7704b0) render an entire explanatory sentence as their above-the-fold age
chip instead of a scannable fact. Contract A requires the fact block to be
"scannable, no prose." All three trees carry a discursive `age_estimate`
string written as a caveat sentence rather than a short label, and the
template (`{esc(t.get('age_estimate',''))}`, same pattern used for the
`tree-label` chip elsewhere) prints it verbatim. Verified live:
`/paris/caucasian-elm-of-square-samuel-paty.html`'s chip row reads "not
documented for this individual; the species itself was introduced to Paris
in 1782, which is context about the species, not this tree's planting
date" as one unbroken chip; `/paris/oriental-planes-of-square-michel-
foucault.html` and `/paris/plane-of-quai-saint-bernard.html` do the same at
shorter length ("not documented; register gives girth only (470cm and
415cm for the two trees)", "not documented for this individual specimen;
the register gives girth (380cm) only"). The content itself is honest and
exactly the kind of caveat P7 wants, it just belongs in the story prose
(where similar context already appears for these same three trees), not
crammed into the one-line fact chip meant to be read in half a second.
Not a BLOCKER: nothing false ships, it just reads as a wall of text where
every other tree page on the site shows a short phrase. Three pages only
(this run's own new trees), so likely fixable by shortening these three
`age_estimate` fields rather than a template change.

---

## 2026-08-06

**BLOCKER** — Page `<title>` tags show a false age whenever a tree's
`age_estimate` is phrased with a qualifier ("roughly", "about", "around",
"over", "nearly", "approximately", "traditionally", "~") instead of a bare
number. `age_token()` (`scripts/build_site.py:895`) extracts a number with
`re.match(r"([\d,]+\+?)", age_estimate)`, which only matches at the START of
the string; when it fails, the function silently falls back to `age_min`
instead of the number the story/answer actually states, and that wrong
number lands straight in the `<title>`, the one thing search engines quote.
Verified live, today's own new cities first: `/zaragoza/oldest-tree.html`
titles itself "(100 Years Old)" while the answer directly beneath it opens
"Nobody has established it" (data/cities/zaragoza.json's own hackberry has
no recorded age; the "100" is a stray `age_min` used only for a *range*
inference) — the exact page whose commit message today says it "says out
loud what it cannot confirm" instead states a false precision in its own
title. `/padova/oldest-tree.html` titles "(400 Years Old)" while its answer
says the Goethe Palm is "roughly 440 years old" (data/cities/padova.json
pad_001). Same defect, pre-existing and site-wide, confirmed on pages
untouched today: `/fukuoka/ayasugi-of-kashii-shrine.html` (a Contract A tree
page, not just the question page) titles "1700 Year Old Tree" while its own
visible fact block two lines down says "traditionally about 1,800 years";
`/nara/oldest-tree.html` "(800 Years Old)" vs. its own answer "over a
thousand years old"; `/seoul/oldest-tree.html` "(700 Years Old)" vs. "nearly
880 years old"; `/malaga/oldest-tree.html` "(350 Years Old)" vs. "around 400
years old"; `/groningen/oldest-tree.html` "(330 Years Old)" vs. "roughly 340
years old". A sweep of all 91 city files found the same numeric mismatch on
43 cities' mechanically-selected oldest tree, and the identical helper
builds every individual tree page's own title (Contract A), so the true
page count is larger than 43 and unmeasured. Violates P2 (the quotable
answer must be true) and P7 (truth outranks polish) on the exact string
Google and AI engines read first. Fix is in the helper, not per-city: parse
the number that actually follows the qualifier word rather than falling
back to `age_min` un-flagged.

**BLOCKER** — `/genoa/oldest-tree.html` names a tree its own hand-written
answer never calls oldest. The mechanically-chosen "oldest" (highest
`age_max`, since `genoa.json` sets no `oldest_tree_id`) is `gnv_003`, The
Holm Oak of San Pantaleo, and the title reads "(200 Years Old)". But the
answer-first paragraph directly beneath it says the *only* tree in Genoa
"with an age anybody actually recorded" is a different tree entirely, the
European hop-hornbeam at Villa Serra (`gnv_007`, 160-170 years, sourced from
Liguria's regional register) — San Pantaleo appears in that same paragraph
only for an unrelated claim, "the thickest trunk in the old town." The
build's own guard against this exact failure (`build_site.py:2818`,
comment: "an answer naming a different tree ships a self-contradicting
page") passed only because the word "holm" from "holm oak at San Pantaleo"
happens to occur in that unrelated sentence, not because the answer names it
as the city's oldest. A visitor reads a title asserting a dated answer and,
one paragraph later, a hand-written explanation that undercuts that exact
tree's claim to it. Violates P2/P7 the same way as the finding above, by a
different mechanism (the guard's substring check isn't scoped to the actual
superlative claim). Fix is data-side: set `oldest_tree_id` to `gnv_007` in
data/cities/genoa.json, or rewrite `question_answer` to actually name and
support San Pantaleo.

**WARN** — Genoa's Villa Serra di Comago cluster is 4 of the city's 10 trees
(40% of the page) and sits, by the page's own FAQ, "roughly thirty-five to
fifty minutes" from the centre by public transport, in a separate comune
(data/cities/genoa.json, FAQ "Can you walk between Genoa's remarkable
trees?"). CLAUDE.md's day-trip boundary is "a tree within roughly 30 minutes
by public transport of the city centre belongs on the city page" (Cork's
Blarney example is ~30 min by the same rule). The page is honest about the
distance and the separate comune, which clears the rule's actual test
("never quietly presenting an out-of-town tree as standing in the city"),
so this is not a fabrication or a broken promise. But 35-50 minutes for
nearly half the page's trees is a real stretch past "roughly 30," on a
larger share of one page's content than any precedent the rule cites. FOR
HIDDE only if the 30-minute figure should be tightened into a hard number or
explicitly widened for up-the-valley clusters like this one; not a blocker,
since the page passes the rule as actually written.

---

## 2026-08-05

**BLOCKER** — `/collections/wisteria-and-blossom-worth-a-spring-trip` now
self-contradicts in its own `<head>`. Today's commit 08e4e01 ("Collections
retitled on measured demand") changed this collection's `seo_title` (the
`<title>` tag per Contract D) to "Where to See Japan's Oldest Wisteria and
Blossom Trees". The collection's actual 11 entries: 1 in Tokyo, the other 10
in Seville, Milan, Granada, Vienna, Antwerp (x2), Lyon, Brussels and New
York (`data/collections/wisteria-and-blossom-worth-a-spring-trip.json`).
Verified live: `site/dist/collections/wisteria-and-blossom-worth-a-spring-trip.html`
carries `<title>Where to See Japan's Oldest Wisteria and Blossom Trees</title>`
directly above `<meta name="description" content="Eleven trees across nine
cities at their spring peak, from Seville's February orange blossom to a
Tokyo wisteria...">`, so the page tells Google and any reader two different
things about its own scope one line apart. Violates P2 (the answer must be
quotable and true) and P7 (truth outranks polish); also the kind of
unverified geographic superlative hard rule 8 exists to catch. A reader who
clicks through from "Japan's" expecting a Japan list lands on a page that is
90% Europe and New York.

**BLOCKER** — Same commit, same bug, second collection:
`/collections/europes-most-remarkable-yews`'s `seo_title` became "The Oldest
Yew Trees of Britain and Ireland", but 4 of its 8 entries are in Naples,
Florence, Verona (Italy) and Madrid (Spain), not Britain or Ireland
(`data/collections/europes-most-remarkable-yews.json`). Verified live:
`site/dist/collections/europes-most-remarkable-yews.html` has
`<title>The Oldest Yew Trees of Britain and Ireland</title>` immediately
above `<meta name="description" content="Eight ancient yews across seven
European cities, from a London yew ... to a three-trunked Madrid
specimen...">`, the same title-vs-description contradiction as above, in the
same commit. Worth checking the other 5 collections this commit touched
before trusting the pattern is contained: those 5 (`europes-most-
remarkable-trees`, `ginkgos-worth-a-november-trip`, `the-great-planes-of-
europe`, `the-oldest-tree-in-every-country-we-map`, `trees-that-outlived-
their-city`) were checked against their actual entry cities and their new
seo_titles do match scope, so the error looks like it was made per-title
rather than systemically, but two live self-contradicting pages from one
commit is enough to call the commit's QA (which caught neither, since
qa.py has no check for title-vs-content scope match) rung 2.

**WARN** — The exact copy claim that today's other work declared false and
removed is still live in two other places. Commit b416ace added TONE_OF_VOICE.md's
"Product copy is soberer than the stories" section, naming "Every tree here
was found, verified and placed by hand" as untrue ("these pages are
researched from sources, and several carry ranges precisely because nobody
has measured them"); commit a935f16 then removed that exact sentence from
the homepage and footer. But `scripts/build_site.py` still prints "each one
verified and placed" verbatim on the `/cities` index (line 3413, "81
cities, 575 trees, each one verified and placed") and on all four country
pages (line 3310; verified live on `site/dist/cities.html`,
`site/dist/japan.html`, `site/dist/spain.html`, `site/dist/portugal.html`
and `site/dist/netherlands.html`). Both lines predate today (2026-07-31 and
2026-08-01) but they make the identical claim in the identical week the
site started treating that claim as false enough to rewrite elsewhere.
"Placed" is also literally imprecise for roughly half the map: the
session-start count is 269 of 575 trees at `location_precision:
"approximate"`, not a confirmed placement. Not a new bug, but today's own
reasoning (TONE_OF_VOICE.md's new rule, applied same-day to the homepage)
argues these two lines should not survive next to it.

**NOTE** — `.github/workflows/nightly.yml` (commit db6f60f) now tells every
autonomous night run to cap new-city photo hunting at "at most 3 photos per
city for now", justified by measured token cost. CLAUDE.md's own Step 4 and
Step 0 rung 6 still describe hunting photos "hard" toward an "8-of-10 photo
target" with no such cap, and a run reads CLAUDE.md as the standing
instruction set. Not necessarily wrong (Hidde's own reasoning is in the
commit message), but the two documents that drive research runs now say
different things about the same number, and only the workflow file
mentions the change. Worth folding into CLAUDE.md's Step 4 or Step 0 rung 6
if the 3-photo cap is meant to stick, so a run reading CLAUDE.md alone does
not over-hunt against the new instruction.

**NOTE** — This file has no entry between 2026-08-02 and today: three days
(08-03, 08-04, 08-05) where either nothing ran the Fresh-eyes review
workflow or it ran and found nothing worth a dated heading (the latter
would still need a "Nothing found." line per this file's own convention,
so more likely it simply did not run). `review.yml` already carries `id-
token: write`, so it is not the permissions bug prior sessions hit. Worth a
`gh run list --workflow=review.yml` check by a session that has `gh`
access, since this run's did not.

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
