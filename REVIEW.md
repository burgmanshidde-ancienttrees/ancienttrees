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

## 2026-09-12

Reviewed commits since the last review (bae8a196, 2026-09-11) through abfb15e6
(~128 commits, day-and-night): the usual claim/verify/write cycle across many
cities (Warsaw 26->28, Amersfoort 8->14 and Breda 4->10 from the Dutch LRMB
register, Ottawa +5 forming a second Dominion Arboretum cluster with its own
earned park page, Prague +3 Praha 8 oaks, Milan +1, several exhausted-register
releases correctly logged rather than re-hunted), a mobile Safari zoom-on-focus
fix (`.hero-search` font-size, now gated by `smoke_test.py`'s computed-size
check), a run of map-attribution work (OpenFreeMap/OSM credit now reaches
every one of the 5 MapLibre call sites via one `mapScript()` wrapper, collapses
to an "(i)" after 5 seconds per the OSMF 2021 guideline, and moved out of the
global footer into the map itself), the cross-language control-parity check
(907 translated tree pages and 47 city pages were missing the worth-it vote
and share button; `check_every_language_gets_the_same_controls()` in qa.py now
catches this class, `data/lang-gaps.json` honestly lists the two still-open
gaps with reasons), and the multi-photo feature merging to main (`photo` stays
the lead, `photos[]` carries extras, both surfaces get a strip + pager, see
DECISIONS.md 2026-09-12). Both WARNs from the 2026-09-11 review (the empty
"Photo: " credit and the three self-repeating tree titles) are fixed
(ef66e113) and verified gone from the built output. Ran `python3
scripts/preflight.py` (595 cities, 0 problems; standing NOTEs only, none
touching a page changed in this window), `python3 scripts/superlatives.py`
(366 claims, no collisions), `python3 scripts/crosscheck.py` (3057 trees,
feed and app agree field for field) and `python3 scripts/qa.py` (clean, 8584
pages, links resolve, text clean). Read the built multi-photo page
(`kyoto/camphor-of-munakata-shrine.html`): thumbnail strip, paging lightbox
with swipe/arrow-key navigation and a correct "Photograph 1 of 2" / "2 of 2"
count all render as described.

**WARN APP — a single-tree place's own page shows "1 trees" in its header,
`ios/AncientTrees/AncientTrees/Screens/Home.swift:720` (`CityView`,
`ShelfHeader(title: "\(trees.count) trees")`).** Confirmed live in
`city.png` (Aachen, 1 tree: header reads "1 trees") from this rotation's
screenshots. The adjacent screenshot of the same city's map sheet,
`city-map.png`, gets it right: "1 tree in Aachen"
(`PlaceMapPage.swift:85`, which does branch on `trees.count == 1`). This is
the same bug class flagged in the 2026-09-10 review in a different file
(`MapSearch.swift`'s "1 trees" for Liskiava/Alishan under Places), which
means it is a recurring pattern rather than a one-off: at least one other
unconditional `"\(count) trees"` construction exists nearby with no
singular branch (`Home.swift:538`, a homepage shelf, not confirmed on
screen this rotation). PRINCIPLES.md #9 is the rule this trips: text a loop
generates is "guilty until read aloud", and a single-tree place (the site
has several) is exactly where a stranger reading cold notices the
grammar first.

**NOTE — CONVENTIONS.md's new 2026-09-12 entry ("Adding a photograph of a
place, and saying you were there") correctly flags an open product question
rather than resolving it, and is doing its job: `CollectSheet.claim()` still
ticks a tree as visited in the same call that attaches an identification
photograph, which the entry itself says Google Maps and iNaturalist keep
separate and marks "Undecided by Hidde as of this date."** Not acted on: it
is explicitly parked for him, and forcing a resolution here would be a
judgment call above this reviewer's mandate. Recorded so it does not read as
missed on a later pass.

No Monday corpus-rot audit today (Saturday UTC).

## 2026-09-11

Reviewed commits since the last review (519318c2, itself the newest at review
time) back through bf9467f8 (~137 commits, day-and-night assembly-line work
plus a substantial session block from Hidde directly): the usual claim/verify/
write cycle across many thin cities (Lausanne to 8, Salamanca and Minneapolis
to 4, Spokane to 6, Cardiff and Fort Lauderdale opened at the floor, Zwolle
deepened from the Dutch register), four stranded verify passes shipped under
the 2026-08-31 single-famous-tree exception (Indianapolis, Sao Paulo, Busan,
Monterey), a new girth data point (database, app UI, /contribute, feed) built
in session with Hidde across nine commits, a website/app parity pass
(`scripts/paritycheck.py`, now in the pre-push hook) that moved the "Worth the
visit?" vote beside the tree name on both surfaces and removed the app's dead
heading the check itself found, the reader-photograph pipeline reaching the
site (Kyoto's kyo_019, from Hidde's own submitted photograph; a rejected
Demizu-guchi candidate correctly held rather than shipped), and an outreach
photograph (Lisbon's Sao Bento tipu, from getLISBON, correctly recorded as a
gift rather than an open licence). Ran `python3 scripts/qa.py` (clean per the
last logged run) and spot-checked `preflight.py`'s and `superlatives.py`'s
last recorded clean runs in the commit trail rather than re-running them.

**WARN — a reader-submitted photograph under the "no name printed" rule
renders a broken, empty credit line: `<figcaption>Photo: </figcaption>`.**
Confirmed live on 5 pages built from current data: `kyoto/twisted-muku-of-
omiya-gate-kyoto-gyoen.html`, `kyoto/camphor-of-munakata-shrine.html`,
`kyoto/ginkgo-of-inui-gate-kyoto-gyoen.html`, `baarn/cantonspark-dawn-
redwood.html`, `baarn/cantonspark-giant-sequoia.html`. Root cause in
`site/src/lib/images.ts`: `isAGift()` matches any licence string starting
with "provided by", including "Provided by a reader through the Ancient
Trees app, all rights reserved" (the exact string CLAUDE.md's 2026-09-04
ruling and the app's own code use for reader photos, which deliberately
carry `attribution: null` so no name prints). `creditRequired()` therefore
returns true, but `creditText(null, license)` returns null since there is no
name to print, and `PhotoFigure.astro` falls back to `t.photoCredit("")`
instead of skipping the figcaption entirely, printing "Photo: " with nothing
after the colon. This is exactly the builder-speak-adjacent, "site presents
itself as finished" failure TONE_OF_VOICE.md's opening rule exists to catch:
a visitor sees a caption that looks broken rather than no caption at all.
Fix belongs in `PhotoFigure.astro` (treat a null `creditText()` result as no
credit, matching `isAGift()`'s own reader-photo case) or in `isAGift()`
(reader-app photos are a distinct, no-credit case, not a gift with a
withheld name). Not visual-taste and not app-only: it is template logic
shared by both surfaces, though today it only manifests on the web build.

**WARN — three published tree pages carry a self-repeating title: "The X: X
in [City]".** `manchester/amur-cork-tree.html` ("The Amur Cork Tree: Amur
Cork Tree in Manchester"), `manchester/adams-laburnum.html` ("Adam's
Laburnum: Adam's Laburnum in Manchester"), `munich/fern-leaved-beech.html`
("The Fern-leaved Beech: Fern-leaved Beech in Munich"). Cause: Contract A's
title candidates in `[city]/[tree].astro` fall back to `` `${tree.name}:
${speciesCommon(tree)} in ${cityName}` `` once `ageToken()` returns null
(correctly null here: Munich's beech is explicitly "undated" and age_min/
age_max are bounds rather than a stated figure, per that function's own
2026-08 fix), and none of the fallback candidates checks whether the tree's
own name already IS the species name. All three trees are named directly
after their species with no further epithet, so the fallback produces a
duplicated, robotic-looking title instead of dropping to `` `${tree.name} in
${cityName}` ``. This is PRINCIPLES.md #9's canonical failure ("a phrase
repeats because a loop wrote it... guilty until read aloud") and a narrow
but real Contract A violation (SEO_GEO_BLUEPRINT.md): the title is what
Google and a human both read first. Scanned every built tree page for the
pattern; exactly these three match site-wide.

**NOTE — the Sao Bento tipu's gift photograph (Lisbon, getLISBON) is the
kind of one-off permission exception DECISIONS.md 2026-08-11 said would each
need "its own explicit yes from him, not a standing policy," recorded in
DECISIONS.md.** The commit is authored by Hidde in session and the
reasoning is sound and well documented in the commit message and the photo's
own `note` field, so nothing here suggests it happened without him. It is
simply not logged in DECISIONS.md the way the Porto precedent it explicitly
follows was. Twenty-three gift/permission photos now exist across five
sources (Porto, Bucaco, Florence, Lisbon, and reader-app submissions), which
reads as an established pattern rather than a one-off exception; worth a
session deciding whether DECISIONS.md's framing should be updated to match,
or left as historical record. Not acted on, no action forced.

Read the app screenshots (`species-pick.png`, `species.png`, `tree-
nophoto.png`, `tree.png`, `walk-begin.png`, `walk.png`, a fresh rotation):
all clean against the corpus. The new girth row reads correctly beside Age
and Species on `tree.png` (Dab Fabrykant); the species picker, the no-photo
species page, the tree detail with photo, and the two walk screens (route
map, walk detail with Begin/distance) all match their surface's own
conventions with no contradiction, no dead control and no overclaimed count.

No Monday corpus-rot audit today (Friday UTC).

## 2026-09-10

Reviewed commits since the last review (0d4e001b, 2026-09-09) through
10097533 (~340 commits): dominated by the assembly line's ordinary work
across many small claims (Leeuwarden deepened 9->41 across five stranded
verify claims, Eindhoven +5, Tilburg completed to its 20-tree target,
Valencia +6, Milan +1, plus recognition-line batches across well over 150
cities), five photo-hunt rounds against the last-resort ("plant-word filter
off") seam (round five's own log: 95 candidates, 0 approvals, correctly
read as "the well is dry" rather than re-run), two real corrections
(Utrecht's Geertebolwerk Pear pin fixed 750m, Seattle's Sylvia correctly
kept alive against a misleading plaque, `verify_notes` recorded so it is
not relitigated), and the day's one substantial feature: continuous,
self-closing copy testing on city titles (`scripts/copytest.py`,
blueprint bumped to v1.16 then v1.17 for Hidde's "Approval do this without
me!"). Checked that feature specifically since it is new and touches every
demand page's title tag: read `site/src/lib/copy-test.ts` and the
`[city].astro` wiring, then the built output for all three seeded cities
(`lisbon.html` age_first: "Oldest 457 Years, 35 to See"; `rome.html` and
`barcelona.html` control: "N to See, Oldest Age Years"). The head phrase
"Ancient Trees in [City]" is identical in both arms as the contract
requires, the H1 stays plain ("Ancient Trees in Lisbon"), and both
rendered titles sit under the 60-character limit. Working as specified.

Ran `python3 scripts/qa.py` (8199 pages, clean), `python3 scripts/health.py`
(rung 2 clear: iOS app back to success, the failure the 2026-09-08/09
reviews carried is resolved), `python3 scripts/preflight.py` (565 cities, 0
problems; the standing NOTEs, paid-entry ratios, stale country
meta-descriptions, four one-space-indented city files, the why_go/age
backlog, are all pre-existing and none touch a page changed in this
window) and `python3 scripts/superlatives.py` (352 claims, no collisions).
Spot-checked `miharu.json`/`motosu.json`'s unusually large diffs in the
recognition-line commit: pure re-indentation (1-space to 2-space) plus one
added `how_to_recognise` line each, not a content change.

Read the six rotated app screenshots
(profile-signed-in.png, profile.png, refused.png, search.png,
signin-email.png, signin.png), a fresh rotation this time (not the
2026-09-07/09 repeat).

**WARN APP — a single-tree place shows "1 trees" in the map search
results, in `ios/AncientTrees/AncientTrees/Screens/MapSearch.swift`.**
`search.png` (query "lis") shows "Liskiava / Lithuania - 1 trees" and
"Alishan / Taiwan - 1 trees" under Places, while the Species row two lines
below it correctly reads "1 tree" for the same count. Confirmed in source:
lines 210 and 217 build the places subtitle as `"\(c.count) trees"`
unconditionally, while the file's own `pluralized(_:)`-style helper three
lines away, at line 307 (`"\(n) \(n == 1 ? "tree" : "trees")"`), already
does this correctly and is used elsewhere in the same screen. TONE_OF_VOICE
and PRODUCT_COPY.md hold this site to being precise and unpretentious about
its own data; a grammatically wrong count on every single-tree place (34
of 190 published places sit at the four-tree floor or below per CLAUDE.md,
so single-tree places are not rare) reads as sloppy rather than deliberate.
Not visual-taste, a one-line fix once picked up: route both sites through
the existing helper. Tagged APP per instructions; a night run may not
touch app UI-adjacent Swift under CLAUDE.md's visual-taste rule, so this
waits for a session.

No Monday corpus-rot audit today (Thursday UTC).

## 2026-09-09

Reviewed commits since the last review (fad01a7f, 2026-09-08 ~06:10 UTC)
through e73d9788 (~125 commits): a night-and-morning assembly-line stretch
across many small claims (Oahu +7 across a verify+write pair, Cagliari +3,
Sorrento +1, Warsaw +7, Maastricht +3, Dordrecht +3, Utrecht +3), a batch of
recognition lines (Barcelona 42, Vienna 26, London 16, Arnhem 10), two new
species pages (White Poplar, Japanese Maple, both 3+ trees with hand-written
intros per Contract F), a large photo-vendoring commit (dc1ce46d, 78
backlogged approvals copied to site/public/photos), a fix to
`superlatives.py`'s `re.I` scope-matching bug flagged as WARN in yesterday's
review (bfaa50f3, confirmed: 347 claims, no collisions today), a new
build-time check that a BY/BY-SA photo names its photographer (4737c21c,
caught and fixed two live credits reading only "via Wikimedia Commons"), and
two real corrections worth calling out on their own: Utrecht's pin for the
Geertebolwerk Pear was 750m wrong and has been fixed to its register
coordinate (96911214), and seven of Utrecht's 34 trees turned out to be
recorded as felled by the register's own inspection layer and were retired
correctly, with leads kept, `REMOVED_TREE_SLUGS` updated, page copy (meta
description, question_meta, FAQ) corrected to the new count, and the count
re-corrected again three commits later when three more trees were added
(ebad8429, 72959c1b; verified the live page's paid/free FAQ arithmetic,
"three of the 30 ... the other 27", is internally consistent). Ran
`python3 scripts/qa.py` (8070 pages, clean), `python3 scripts/health.py`
(rung 2: **iOS app** failing on its newest scheduled run, already the
session-start brief's own top item, not a new finding) and
`python3 scripts/preflight.py` (564 cities, 0 problems; only pre-existing
NOTEs, none touching a page changed in this window). Spot-checked Oahu's,
Cagliari's, and Sorrento's new trees' `verified_sources` (real, reachable
citations, not monumentaltrees.com), a sample of the new recognition lines
against BRIEF_WRITING.md's shape (all restatement, traceable to the tree's
own girth/height/story, no invented detail), and the built HTML for
Utrecht, Cagliari (Italian), Oahu, Warsaw and Maastricht: every title,
meta description and question_meta on the changed pages matches its city's
current tree count.

Read the six rotated app screenshots (own-tree.png, paywall.png,
people.png, photo-viewer.png, place-pin.png, profile-edit.png): all clean
against the corpus, and all previously traced and accepted by the
2026-09-07 review (DemoPeople.swift's demo people, the "Plus is not open
yet... we are building it" line, which is the sanctioned coming-soon
exception TONE_OF_VOICE.md carves out of the builder-speak ban, not a
violation of it).

**NOTE — the app-screenshot rotation this review reads from is not
actually rotating, and the cause is the same broken CI job rung 2 already
names.** review.yml downloads screenshots from the newest GREEN ios.yml
run (`.github/workflows/review.yml` line 96 on); today's set came from an
`appsweep-ios18-*` artifact (the scheduled iOS-18-floor job), and its six
picked screens are the exact same six, in the same order, that the
2026-09-07 review already read and cleared. Since push-triggered ios.yml
runs have been failing (session-start brief: "iOS app keeps failing ON ITS
SCHEDULE"), the newest green run this workflow can find is stale, so the
"every screen seen inside four nights" guarantee this file's own
instructions describe is not holding: two reviews two days apart saw
identically the same six screens rather than a fresh rotation. Nothing on
the pages themselves is wrong; this is a coverage gap in the review
process, not a product finding, and it self-heals the moment ios.yml goes
green again. Worth knowing rather than acting on, since acting on it means
fixing the iOS app, which is already rung-2 work.

No Monday corpus-rot audit today (Wednesday UTC).

## 2026-09-08

Reviewed commits since the last review (~230 commits in 24h): dominated by
`cd4e1f69`, a single pass writing `how_to_recognise` lines for the last 206
published trees that carried none of the three things that settle which
trunk is meant (recognition line, photograph, confirmed pin), plus the new
`check_a_tree_can_be_told_apart()` gate in scripts/preflight.py that now
fails the build on a recurrence. Also in the window: two new Lithuanian
places (Vytogala, Pagramantis Regional Park), a `_famous-japan` verify
pass, a `_famous-lithuania` verify pass (5 ready, 3 dead trees correctly
blocked rather than published), a large walk-routes regeneration, and
batch-011 outreach (nine mails, Hidde's own "doe die laatste 9 maar",
status `approved_by_hidde`, so hard rule 4 is not in play here). Ran
`python3 scripts/qa.py` (7903 pages, clean), `python3 scripts/health.py`
(rung 2: **Build and deploy** and **iOS app** both failing on their newest
runs, already surfaced by the session-start brief and outside what this
review duplicates), `python3 scripts/preflight.py` (549 cities, 0 FAILs)
and `python3 scripts/superlatives.py` (720 claims, see WARN below).
Spot-checked the new `how_to_recognise` lines against BRIEF_WRITING.md
(fixed "You can recognise it by X. It stands Y" shape, all under 240
chars, restatement only, numbers traced back to each tree's own
`girth_cm`/`height_m`/story, no banned words or em dashes), read
`vytogala.json` and `pagramantis-regional-park.json` in full (honest
hedged ages throughout, "nobody has cored it, tell us" pattern used
correctly, the Regional Park container correctly framed as reached "by
car or bicycle" rather than dressed up as walkable), and read the six
rotated app screenshots (`contribute.png`, `directions.png`,
`explore.png`, `feedback.png`, `map-full.png`, `map.png`).

**WARN — `scripts/superlatives.py`'s scope regex is compiled with
`re.I`, which silently defeats its own "capitalised place name" check
and produced two false-positive collisions today.** The pattern's scope
group is `[A-Z][\w'-]*`, meant to require a proper noun so that e.g. "in
the city of Fukuoka" is read as scope "Fukuoka". Because the whole
`CLAIM` regex is compiled `re.IGNORECASE`, `[A-Z]` matches lowercase
letters too, so the scope match stops at the next capped-length word
instead of reaching the actual city name: "the largest tree in the city
of Fukuoka" and "the largest tree in the city of Stockholm" (fuk_008,
`data/cities/fukuoka.json`; sto_004, `data/cities/stockholm.json`,
touched today in `f5deab19`) both truncate to scope "the city of" and
register as the same claim about two different cities. The same bug
paired "the first decade of the twentieth century" in `haarlem.json`
(`66e4f759`, today) and `leiden.json`, a date phrase with no ranking
content at all, misread as a "first ... of ..." claim. Both trees in
both pairs are correct as written; nothing needs to change in the data.
The risk is the tool crying wolf into a future run's hands: CLAUDE.md's
own account of hard rule 8 says a writer "no longer has to hold the
whole corpus in their head" because this script does the checking, so a
false collision is exactly the kind of finding that gets "fixed" by
quietly rewriting a true sentence to make the phantom contradiction go
away. Fix is narrow: require the scope group to stay case-sensitive
regardless of the rest of the pattern's flags (e.g. an inline
`(?-i:...)` around just that group, or split scope-matching into its
own non-`I` regex) rather than something for a run to patch by hand
without checking the fix against the two known-good pairs above.

**WARN APP — `map-full.png`'s second tree card renders a floating cloud
icon and a "Map" pill button where the photo and title should be,
obscuring the tree's name.** In the Map tab's bottom sheet list ("24
trees you can see"), the first card (Rijksmuseum Wingnut) is a normal
photo card; the second card beneath it is solid dark green with a white
cloud glyph and a rounded "Map" button centred over it, and the tree's
name is visible only as a sliver of cut-off text ("Wych ElIm") right at
the bottom screen edge, half hidden behind the button. Nothing on
screen explains what tapping "Map" here would do, and it reads as
either a broken/unloaded state for a photo-less tree (the app's
placeholder for "no photo" apparently differs from the website's
labelled silhouette-plus-caption treatment) or a stray render of the
tab bar's own "Map" control caught mid-transition; either way a person
scrolling this list would stop on it as visibly wrong, which is
PRINCIPLES.md's own bar ("does a screen contradict itself, show a
control with no obvious purpose"). Tagged APP: this is visual-taste
work a night run may not touch (CLAUDE.md), for a session with Xcode to
reproduce via `appsweep.py` and look at directly.

Nothing else found at BLOCKER or WARN. `contribute.png`, `explore.png`,
`feedback.png`, `directions.png` and `map.png` are clean against the
corpus (the "24 trees you can see" / "536 places" copy and the
feedback screen's "Nobody else sees who sent this... Sending needs a
free account" line are consistent with the account-gated-feedback and
never-publish-a-name rules, not a contradiction: the account identifies
a sender to us for a reply, "nobody else" is about other readers).

No Monday corpus-rot audit today (Tuesday UTC).

## 2026-09-07

Reviewed commits since the last review (d52051f2, 2026-09-06 ~09:42 UTC)
through 746c5f43 (~150 commits): mostly an iOS session driven by Hidde
testing the collect flow live in Nara (the "I am not sure which" picker
state, an honest age-string fix, an approximate-pin never auto-ticks a
tree, a "first tree"/"first in this city" milestone line, "yours
immediately, ours is a separate question" copy, a register-corroboration
script for reader-added trees) plus the usual assembly-line research
(Prague +3, Nara +4 from reader photos, single-tree famous-tree places
opened in France, Poland, Japan and Corsica, Dutch bomenbieb verify
batches, photo vendoring, three iOS map-test flakiness fixes). Ran
`python3 scripts/qa.py` (7495 pages, clean), `python3 scripts/health.py`
(rung 2 clear, no BLOCKER), `python3 scripts/preflight.py` (504 cities,
0 problems) and `python3 scripts/superlatives.py` (702 claims, no
collisions). Confirmed both 2026-09-06 WARNs are genuinely fixed rather
than just claimed: Canberra/Gumeli/San Quirico d'Orcia's FAQ answers now
name the actual fame case instead of the four-tree-floor threshold (and
the two new phrases were added to `qa.py`'s `BUSINESS_RULE_PHRASES`,
confirmed no page in the built site matches the old rule-explaining
pattern), and Contribute.swift's line now reads "Nobody else sees who
sent this." Spot-checked the new single-tree/low-tree-count places
(`ghisonaccia`, `le-precheur`, `venon`, `rogalin`, `sulechow`) for the
same rule-explaining anti-pattern and for the four-tree-floor exception:
clean, and the 2-tree places (Rogalin's two named oaks, Sulechow's two
pines, Ghisonaccia's two trees) match an existing, established site
pattern (19 other 2-tree places already published, including Charleston
and Savannah, the cases DECISIONS.md 2026-08-31 names directly), not new
drift. Read the six rotated app screenshots
(`own-tree.png`, `paywall.png`, `people.png`, `photo-viewer.png`,
`place-pin.png`, `profile-edit.png`): all clean against the corpus.
`people.png`'s "Find people" list (Marieke/Tom/Sofia) and `paywall.png`'s
"We are building it" line were both already traced and accepted by
earlier reviews (2026-08-27, `Kit/DemoPeople.swift` demo data; Hidde's
own copy, kept deliberately). `own-tree.png`'s "Added to your trees...
once it's verified, we will add it to our map" (TreeDetail.swift) does
not contradict today's CollectSheet.swift copy change ("yours
immediately, ours is a separate question") despite living in a different
file; both say the same thing in the same order.

Nothing found at BLOCKER or WARN for the last 24 hours' changes. This
was an unusually careful session: four separate bugs Hidde found live
in the field each got a real fix plus a benchmarked convention entry in
CONVENTIONS.md (Merlin, geocaching FTF/DNF, Strava, AllTrails/Google
Maps/Komoot compass words) rather than an invented pattern.

**Monday corpus audit** (CLAUDE.md, PRINCIPLES.md, PRODUCT_IA.md,
BACKLOG.md, GO_TO_MARKET.md, DECISIONS.md).

**NOTE — CLAUDE.md's "The paywall line, SET by Hidde 2026-08-18" section
lists a four-feature Plus bundle that a later standing decision
explicitly replaced.** CLAUDE.md still reads: "four features behind it:
Season Radar alerts, curated tree walks, **a personal tree log with
badges and photo upload**, and full offline access." DECISIONS.md
2026-08-26 ("the launch is free, the walks and the season are Plus, and
the free scope freezes at launch") opens by saying it "REPLACES the
four-feature Plus line of 2026-08-18" and rules explicitly: "Log, badges,
photo upload and collecting stay free forever-in-practice because they
ARE the flywheel." CLAUDE.md was never updated to match, so a run reading
only CLAUDE.md (which nightly.yml points at, per its own "this paragraph
is the only place either of them lives" convention elsewhere in the same
file) would build photo-upload or badges as paid features, the opposite
of the standing ruling. Suggest: rewrite the paywall section to say
walks and the whole season story are Plus, log/badges/photo-upload/
collecting are free, per the 2026-08-26 entry, or add an explicit
superseded-by pointer the way other sections in this file do.

**NOTE — the same CLAUDE.md section's account snapshot describes a
sync mechanism that no longer exists.** "Where the account track
actually stands (2026-08-14...)" lists as live: "cloud sync of saved
trees as a union." DECISIONS.md 2026-08-30 reverses exactly this
("saving needs an account... two stores merged as a union is where the
drift lives, and it produced a real fault"), and 2026-09-02 goes
further ("Nothing is stored on the device any more... Gone with it: ...
the saved cache (`at_saved_v1`)"). The union mechanism CLAUDE.md
describes as current was killed by two later rulings. Suggest: drop the
"as a union" clause or point it at the 2026-08-30/09-02 DECISIONS.md
entries.

**NOTE — BACKLOG.md carries two parked items whose triggers already
fired weeks ago and whose open questions are already answered.** "Web
check-in moves to the app; web becomes discovery plus sales floor" says
"Not yet executed... awaiting his confirm on framing before code is
removed. Until then... nothing passport-related is built or removed" —
but DECISIONS.md 2026-08-25/29/30 and 2026-09-02 already gated
saving/collecting behind an account and then removed the local passport
entirely ("nothing is stored on the device any more"), which is exactly
the confirm-and-remove this item was waiting on. Likewise "Accounts, and
a paywall on top" gives its trigger as "evidence that people want this"
and needs Hidde — both accounts (2026-08-14) and the paywall line
(2026-08-18, revised 2026-08-26) are long since decided and recorded in
DECISIONS.md. Both backlog entries read as open questions to a reader
today; they are resolved history. Suggest moving/removing both, per
BACKLOG.md's own stated purpose ("things worth building, deliberately
not being built yet... without a trigger an item is just a wish").

## 2026-09-06

Reviewed commits since the last review (c7d4847e, 2026-09-05 ~11:00 UTC)
through d52051f2 (~230 commits): the usual assembly-line volume (single-tree
"famous-tree" destinations opened across Germany, France, Finland, Denmark,
Slovakia, Lithuania, Turkey, Australia, Italy, Switzerland, the UK and
Poland; Tilburg and Eindhoven deepened from the Dutch register; Borrowdale
opened while catching two pre-existing duplicate leads; several photos
vendored to our own domain). Ran `python3 scripts/qa.py` (7050 pages,
clean), `python3 scripts/health.py` (rung 2 clear, no BLOCKER),
`python3 scripts/preflight.py` (459 cities, 0 problems) and
`python3 scripts/superlatives.py` (681 claims, no collisions). Confirmed
both 2026-09-05 WARNs are fixed: Scheessel's story now spells the town
consistently (0 hits for "Scheeßel" in the built HTML, was 3), and the
Gerichtslinde-of-Scheessel fame flag was a note rather than a call to
retire. Spot-checked the substantial new pages (`/aachen`, `/schlagsdorf`,
`/gumeli`, `/borrowdale`, `/canberra`, `/tilburg`, `/eindhoven`) plus five
random others (`/`, `/explore`, `/species`, and two tree pages); read six
rotated app screenshots (`collection.png`, `contribute.png`,
`directions.png`, `explore.png`, `feedback.png`, `map-full.png`).

**WARN — three new single-tree-destination pages explain our own publish
threshold to the reader, the exact disease TONE_OF_VOICE.md was written to
stop.** `data/cities/canberra.json`, `gumeli.json` and
`san-quirico-d-orcia.json` each carry an FAQ answer built from the same
sentence: "This site publishes a place below the usual four tree floor only
when a single tree ... is itself the destination people travel for."
Confirmed live in the built HTML's FAQPage schema on all three
(`site/dist/canberra.html`, `gumeli.html`, `san-quirico-d-orcia.html`).
TONE_OF_VOICE.md's "Never explain our own rules to the reader" (v1.4,
2026-08-08) names this exact shape ("the publish gate as copy... that is
our logic back to the end user, they don't care about our specific rules")
and was written after the same mistake shipped on the parks index.
`scripts/qa.py`'s `BUSINESS_RULE_PHRASES` list already guards against it
but only matches the park-page wording ("earns a page", "publish gate",
etc.); this new phrasing, built for the 2026-08-31 single-tree-destination
exception, isn't in the list, so it shipped past the existing check on
three pages in one day. Not a BLOCKER because nothing is factually wrong,
but it is the same drift the check was built to prevent, now recurring in
a page type that didn't exist when the check was written. Fix is cheap:
reword the three FAQ answers to say what IS here (the fame case) rather
than the threshold behind it, and add the new phrase (or "below the usual
four tree floor") to `BUSINESS_RULE_PHRASES` so the next single-tree
place can't repeat it.

**WARN, APP — the feedback screen contradicts itself in the space of two
sentences.** `ios/AncientTrees/AncientTrees/Screens/Contribute.swift`:
line 89 tells the reader, directly above the text box, "Nobody sees who
sent this, and we do not ask for your name." Line 118, in the footer under
the Send button on the same screen, reads "Sending needs a free account,
so we can thank you, ask a question if we need to, and tell you what your
tip changed." A visitor reading top to bottom meets an anonymity promise
followed by a requirement to sign in to an account so the team can address
them personally, which is not anonymous by any ordinary reading of the
word. The code comment above line 89 shows the distinction that was meant
("not 'we never publish your name'... nobody sees who sent THIS", i.e. no
other USER sees it, not that we don't know), but that nuance lives in a
comment, not on the screen, and a stranger holding the phone has no way to
read it that generously. This is a corpus violation on its own terms:
PRODUCT_COPY.md exists so the twenty words somebody reads while holding
the app say what they get without leaving a contradiction for the reader
to resolve themselves. A session (not a night run, per the app
visual-taste rule) should reword one of the two lines, most likely
narrowing the first to "Nobody else sees who sent this" so it stops
promising something the second sentence takes back.

Everything else read clean: no em dashes or banned words on the sampled
pages (the one "majestic" hit in `explore.html`'s embedded map data is
the tree's own registered name, "The Majestic Beech of Roumare", traced to
the register's own file name `h_majestueux.pdf`, not house-style prose),
no superlative collisions, photo licences and visible CC BY attribution
render correctly on the new Aachen page, and the other four rotated app
screenshots (`collection.png`, `directions.png`, `explore.png`,
`map-full.png`) show nothing that contradicts itself or leaves an
unexplained control; the floating "Map" pill in `map-full.png` is the
documented back-to-map button for a fully-expanded sheet
(`MapTab.swift`), not a stray control.

---

## 2026-09-05

Reviewed commits since the last review (61cc80c6, 2026-09-04 ~11:00 UTC)
through c7d4847e (~227 commits): almost entirely assembly-line work
(single-tree "famous-tree" places published across Japan, Germany, the UK,
Poland, Slovakia, Lithuania; Arnhem/Park Sonsbeek deepened; two
self-ranking season collections built by Hidde in session; reader photos
and a reader-GPS register match merged into Baarn). Ran `python3
scripts/qa.py` (6617 pages, clean) and `python3 scripts/health.py`
(green except the already-tracked Data digest failure, which health.py's
own rung-2 line already surfaces to runs). Spot-checked the new pages
(`/takeo`, `/scheessel`, `/newtown`, `/aberford`, `/moffat`, the merged
`/bristol` and `/baarn`) and the two new collections
(`/collections/autumn-colour-trees`, `/collections/autumn-harvest-trees`),
plus the homepage and four other pages at random.

**WARN — Scheessel's own page spells the town two different ways.** The
Gerichtslinde tree's `story` field (data/cities/scheessel.json) uses
"Scheeßel" (with eszett) twice: "Scheeßel's Femegericht met..." and
"Scheeßel is a small town...". Every other field on the same city
(`intro`, `question_context`, both FAQ entries, the title, and the rest of
the same story) spells it "Scheessel". Confirmed in the built HTML: both
`site/dist/scheessel.html` and
`site/dist/scheessel/gerichtslinde-of-scheessel.html` render "Scheeßel"
three times against "Scheessel" 29-36 times. This is not the English-exonym
rule (there is no exonym here, both are the local spelling); it is one
writer typing the town's name two different ways within a single document.
A reader would notice two spellings of the same place in one story, which
TONE_OF_VOICE.md's "written for a human first" standard and P3's
uniqueness-and-care bar both argue against. Cheap fix: pick one spelling
(city-aliases.json and every other field already say "Scheessel").

**WARN — the Gerichtslinde of Scheessel is the one single-tree place
published today that does not obviously clear the "would somebody travel
specifically for THIS ONE TREE" bar (DECISIONS.md 2026-08-31).** The other
four single-tree places shipped in the same 24 hours each carry an
independent credential that makes the fame case for itself: Newtown's
Brimmon Oak (runner-up, European Tree of the Year 2017, national road-
rerouting campaign), Aberford's Nellie's Tree (UK Tree of the Year 2018,
in Flora Britannica), Moffat's Survivor Tree (Scotland's Tree of the Year
2020, symbol of the Carrifran restoration), Takeo's Great Camphor (named
one of Japan's largest trees by girth, a shrine built inside it). Scheessel's
Gerichtslinde has two registers agreeing it is large (about 7m girth) and
disagreeing on its age by three centuries, and a genuinely interesting
history (a court sat under it from 1288), but no award, campaign, or
superlative distinguishes it from the many other "Gerichtslinde" trees
recorded across Germany, and its own story is honest that the age is
unsettled. This is a judgment call a run is entitled to make (CLAUDE.md:
"a judgement call about whether a tree is good enough never blocks
publication"), so this is not a call to retire it, only a flag that this
one entry's fame case reads noticeably thinner than its four siblings
published the same day, worth a second look by whichever run or session
next touches Scheessel.

**NOTE, APP — the collection tab's own heading disagrees with the tab bar
it sits under.** `collection-tab.png` (rotated app screenshot, signed-out
state): the bottom tab bar item reads "My trees" (also the label used on
the map's own filter chip in `collect-intro.png`/`collect-away.png"), but
the sheet's own heading directly above the stats reads "Your trees". Minor,
and possibly deliberate voice (label short, heading conversational), but it
is exactly the "title disagrees with the tab it sits under" pattern this
review is asked to watch for, so naming it rather than silently editorialising.

Everything else read clean: no em dashes or banned words in the sampled
pages (`grep -c "—"` zero across all five new city pages), no superlative
collisions, no builder-speak toward the visitor, the new register-upgraded
Baarn pin and its `notes` field correctly document the provenance chain
(reader GPS to register coordinate), the two new season collections both
carry a hand-written 100-150-word intro and a real `generated` filter
rather than a bare template, and the four other randomly sampled pages
(`/bristol`, homepage, `/collections/autumn-colour-trees`,
`/collections/autumn-harvest-trees`) all render with correct counts and
titles.

---

## 2026-09-04

Reviewed commits since the last review (f66c7324, 2026-09-03 11:19 UTC)
through 61cc80c6 (~240 commits, mostly routine assembly-line work: dozens of
single-tree "famous-tree" places opened across Japan/Australia/Germany/
Poland/UK/Brazil/Bulgaria/France, register scouting, photo sweeps, outreach
batches). Sampled the substantial, non-routine ones: the App Store review
prompt build (`b54a1542`/`a08eafd8`/`47c131db`/`63ed91f3`, self-reviewed
in-session and correctly following Apple's SKStoreReviewController guidance,
recorded in `CONVENTIONS.md`), the on-device camera GPS-fabrication fix
(`c4598e78`), the walks/Season Radar ad removal from the site and app
(`f8b4539b`, `117f185f`, `7031e30a`), the App Store announcement on the
website (`a98fe78a`, `a5694be0`), the Bari booking-access publish
(`95251f0d`), the personal-email removal from outbound mail
(`e4a788c2`), the breadcrumb-schema fix (`d06293b0`), the tree-card
boundary restyle (`ec65076b`), the My trees/Favourites per-tree state fix
(`bc6eeaf0`), the `/t` share-page redesign (`9a5dc878`), and the sitemap
lastmod-by-content-hash rewrite (`1d061928`). Ran `python3 scripts/qa.py`
(6145 pages, clean) and `python3 scripts/health.py` (all green, no
BLOCKER, REVIEW.md's 2026-09-03 WARN already answered and verified fixed:
`Home.swift`'s hero tagline is back on `Brand.gold`). Spot-checked the
built site: `/app`, `/`, `/bari` (new bar_005 tree renders correctly, title
and FAQ updated from four to five trees, "Are Bari's trees free to see?"
correctly split into free/paid), `/prague` (new Elm of Zatory, count
correct at 18), `/t`, and `/account` (Seen badge and per-tree heart state
both render).

**WARN, APP — the exact bug just fixed on-device has no regression test,
despite a UI test suite built specifically for this state.**
`ios/AncientTrees/AncientTreesUITests/RefusedWalk.swift` exists, by its own
header comment, because "this app is ABOUT where you are standing, so it is
the state most likely to make it look broken," and CLAUDE.md calls a
fabricated location the product's "one unforgivable error." `c4598e78`
(today) fixed exactly that failure mode: `CollectSheet.resolve()` was
recording a confident `.device` GPS fix even when location was off,
silently falling back to the last remembered fix or Dam square, found only
because Hidde happened to test it on his own phone. `RefusedWalk`'s one
test that opens the collect sheet with location refused,
`testCollectSaysWhatItCannotDoRatherThanShowingNothing`, never taps the
camera button; it only asserts the sheet isn't blank. No test anywhere
exercises `resolve()` taking its new `.place` branch. The fix itself reads
correct (routes to the same honest pin-drag stage a location-less
photograph already uses), but a later refactor of `CollectSheet`'s photo
flow could reintroduce the exact fabrication CLAUDE.md hard rule 10 forbids
and nothing in CI would notice. A session (not a night run, since this is
app test-authoring) should add a case to `RefusedWalk` that launches
`-collect` with location refused, taps the camera affordance, and asserts
the flow lands on the pin-drag/`.place` stage rather than silently
recording a `.device` fix.

Everything else read clean: no em dashes or banned words, no
builder-speak toward the visitor, no superlative collisions in the sampled
pages, the Android-app copy change and the App Store announcement are
Hidde's own explicit wording rather than a run's invention, and the six
rotated app screenshots (`species-pick.png`, `species.png`,
`tree-nophoto.png`, `tree.png`, `walk-begin.png`, `walk.png`) show nothing
that contradicts itself, overpromises, or leaves an unexplained control.

---

## 2026-09-03

Reviewed commits since the last review (3f36e214, 2026-09-02 11:19 UTC)
through f66c7324: the dark-mode pass across the app (`351b26c8`), the map's
first-fix aim bug (`66df3ffc`), account-deletion photo takedown
(`8adf1248`), Wikimedia's real width buckets (`717da28e`), the dark map
style (`26242382`), the web account page rebuilt to the app's shape
(`b67a5f53`), the translated-chrome fix (`70caa23f`, `3ebe658b`), the
unlisted tree-share page (`16c1bcac`), and the routine digest/re-rank and
assembly-line commits (Ghent, Leuven, Bruges, Ypres, Stuttgart, Freiburg,
Taipei, and the famous-tree lane). Ran `python3 scripts/qa.py` (5613 pages,
clean) and `python3 scripts/health.py` (all green, no BLOCKER) against the
current build. Spot-checked `/es/seville` for the chrome-translation fix
(nav, breadcrumb and footer all read in Spanish now, confirmed in the built
HTML) and `/t` for the new unlisted share page (honest "this link leads
nowhere" state, noindex, no location exposed, matching hard rule 10).

**WARN, APP — `Home.swift`'s hero tagline swapped to a colour calibrated for
the wrong background, in the same commit that fixed the real version of this
bug.** `ios/AncientTrees/AncientTrees/Screens/Home.swift:274`, "wherever you
are." changed from `Brand.gold` to `Brand.goldInk` in `351b26c8`. `goldInk`
exists specifically to fix gold-as-text on a *white* surface (measured
2.30:1 there, per the commit message and `darkcheck.py`'s `PAIRS` list,
which only checks solid-colour pairs like `goldInk`/`surface`). But this
text does not sit on a white surface: it sits on a rotating photograph under
a `.black.opacity(0.62)` gradient (`Home.swift:267-269`), exactly the
composition `HeroCover.swift:52` uses for the identical line and correctly
left on plain `Brand.gold` in this same commit (that file isn't even in the
diff). `goldInk`'s light-mode value is `0x8F6210`, a dark brownish gold
picked to read on white; over a darkened photo in light mode (the app's
default appearance) it is duller and lower-contrast than the `Brand.gold`
it replaced, the opposite of what the commit was trying to achieve
everywhere else. On today's sample photo (`explore.png` in the rotated
screenshots, a bright sunlit canopy) it still reads, but the photo rotates
(`Heroes.image`) and a darker or more uniform frame would make it worse.
This is a plausible regression, not certain breakage, and not something a
mechanical check can catch (`darkcheck.py` only measures the fixed palette,
never a photo overlay), which is exactly the kind of thing this layer
exists to catch. A session should compare `Home.swift`'s hero band against
`HeroCover.swift`'s and decide which one is right, since right now the
identical line of copy is styled two different ways for no stated reason.

Everything else read clean: no em dashes or banned words in the sampled
pages, no builder-speak toward the visitor, no superlative collisions, the
account page's two lanes match the app's own state language as the commit
claims, and the photo-takedown guard (`check_contributor_photos_are_traceable`)
is correctly wired both directions before any contributor photo has shipped.

---

## 2026-09-02

Reviewed the last 24 hours (~140 commits): heavy assembly-line work (Rio de
Janeiro, San Diego, Belfast and Liverpool opened; Auckland, Lima, Regensburg
opened; Hamburg, San Francisco, Manchester, Fort Worth, San Antonio opened;
twenty famous American trees and several famous-Japan/Austria/Italy leads
published; Madeira, Kagoshima and others deepened), Palma de Mallorca's
Spanish translation, the account/deletion and app share-card work
(`438e7752`, `2be34589`), and the daily digest/re-rank. Ran
`python3 scripts/qa.py` directly against the current `site/dist` build.

**BLOCKER — the site currently fails its own deploy gate: `scripts/qa.py`
reports 2 problems, both a false-positive on legitimate content, introduced
today by the Palma de Mallorca Spanish translation (`b9de0302`).**
`check_no_name_promise()` (scripts/qa.py:817-842) greps built pages for the
literal string `"con su nombre"` as a proxy for "we promise to publish your
name", the pattern that shipped on Spanish tree pages on 2026-08-16. But
`data/i18n/es/palma-de-mallorca.json`'s story for S'Olivera de Cort contains
the sentence "El ayuntamiento le prometió a Batle una placa **con su
nombre**" ("the city promised Batle a plaque with his name"), a documented
historical fact about a 1989 civic gift (sourced to Ultima Hora), not a
promise to the reader. Spanish `su` is both third-person ("his/her/their")
and formal-second-person ("your"), and the check cannot tell them apart, so
it fires on `site/dist/es/palma-de-mallorca.html` and
`site/dist/es/palma-de-mallorca/solivera-de-cort.html` alike. This is
exactly the class of error CLAUDE.md's ratchet exists to prevent (a check
that fires twice becomes a build gate) turned on itself: the check is sound
in intent but the keyword is not specific enough for Spanish grammar, and it
is currently failing a build that should ship (SessionStart's "Build and
deploy site FAILED" matches this). Fix direction for a session, not decided
here: narrow the pattern to second-person contexts (e.g. require "tu"/"su"
immediately after a promise verb aimed at "you", or exclude known
third-person referents), or check the English source sentence's grammatical
person before translation rather than grepping the Spanish output blind.

**APP, NOTE.** `collect-away.png` and `collect-intro.png` (both rotated into
today's six) render as the same screen pixel-for-pixel as far as a read can
tell: the Amsterdam map behind a "Build your tree collection" /
"Every tree you photograph joins your collection" sheet with "Take a photo"
and "Choose from your photos". Their names imply two different entry
states (arriving away from any known tree vs. a first-use intro), and if the
underlying launch arguments are meant to produce different content, one of
them is not doing so. Low confidence since this cannot be fixed by a night
run either way (CLAUDE.md: runs do no visual-taste work) and may simply be
two arguments that correctly fall back to one honest shared state; worth a
session glance rather than a rung.

Everything else read clean. Spot-checked the built pages for Liverpool (a
new 2-tree place under the 2026-08-31 single-destination-tree exception,
correctly flagged and sourced, "Trees nearby" renders correctly on both tree
pages), Rio de Janeiro, San Diego, Belfast, Kagoshima and Palma's English
and Spanish sets: no em dashes, no banned words, no superlative collisions
in the sampled pages, hreflang reciprocal on the Spanish set, and the
walks-pill/walks-page contradiction flagged BLOCKER on 2026-08-31 stays
fixed (Liverpool has no walks page and correctly falls back to the app
pill). Verified Kuala Lumpur's non-publication (`2f077b3a`) is handled
honestly: two single-sourced trees, neither passing the destination-tree
test, a fabricated "300-year-old mahogany" claim identified and explicitly
not used, all recorded in `data/leads/kuala-lumpur.json` rather than
shipped.

Read all six rotated app screenshots (`city-map.png`, `city.png`,
`collect-away.png`, `collect-intro.png`, `collect-place.png`,
`collection-tab.png`). Aside from the NOTE above, nothing contradicts
itself, overpromises, or shows a control with no stated purpose; the
signed-out Collection tab's "0 Trees / 0 Species / 0 Countries" reads as an
honest empty state per PRINCIPLES.md #3.

---

## 2026-09-01

Reviewed the last 24 hours (~140 commits): heavy assembly-line work (Naha,
Pamplona, Ronda, Nagoya, Kamakura, Segovia, Sapporo, Tarragona, Girona,
Kanazawa, Miyazaki, Hiroshima and Kagoshima opened from zero; Delft, Naples,
Valencia, Turin, Warsaw, Vilnius deepened), the sender-name privacy fix
(`f91e11bb`, de-naming a submitter from `data/cities/prague.json` and
`drafts/`, plus a new `check_no_sender_names()` ratchet in preflight.py), two
outreach replies sent with Hidde's approval (Sydney's register-licensing
refusal recorded in OPEN_DATA_SURVEY.md so it is not rescouted; the Florence
Himalayan cedar photo, sent directly by the garden with a verbatim credit
line, going live), the web account page rebuild (`bac7be40`, a name field so
web-created accounts become findable in the app, deletion moved to a marked
area at the page foot), and the App Review reply package for Apple's
Guideline 2.1 rejection (`d6f01f21`). Ran `python3 scripts/qa.py` (4080
pages, clean), `python3 scripts/superlatives.py` (540 claims, no collisions)
and `python3 scripts/preflight.py` (207 cities, 0 problems besides the
already-tracked paid-entry NOTEs, Kamakura newly on that list at 67% and not
re-litigated here).

Verified both of yesterday's findings are fixed in the current build. The
walks-pill BLOCKER: sampled `site/dist/kagoshima.html`, the map pill now
links to `/kagoshima/walks` (the real walks page) rather than `/app`
(`b299c341`). The empty "Trees nearby" WARN: `site/dist/santalfio/
hundred-horse-chestnut.html` no longer renders the heading over nothing, and
`site/dist/philadelphia/bartrams-ginkgo.html` no longer has the "all 1
remarkable ancient trees" singular/plural slip (`ad73db9d`).

Spot-checked five new city pages (Naha, Pamplona, Kagoshima, Segovia, Naples)
in the built HTML: titles, descriptions and the two-format title logic in
`[city].astro` (the "Oldest N Years" hook only above 200 years, falling back
to "Remarkable Trees Worth Visiting" otherwise) all read correctly, no em
dashes or banned words. Naples's new disputed-species entry (nap_024, the
Elephant's Foot) correctly asks the reader which of two register names is
right rather than guessing, per the publish-and-ask rule, and the city's
tree-count copy (23/24) is internally consistent across intro, FAQ and
question_meta. The Prague fix itself reads honestly: `verify_notes` now says
plainly that the submitter's own filled-in location field was not
independent confirmation, rather than over-crediting a form default as
verification.

**APP.** Read all six rotated screenshots (`people.png`, `place-pin.png`,
`profile-edit.png`, `profile-signed-in.png`, `profile.png`, `refused.png`).
`profile-signed-in.png` and `profile.png` carry "You can add a tree by
taking a photograph of it and filling in what you know", which is the
corrected PRODUCT_COPY.md pattern (reader as subject, joined with "by") in
active use rather than the rejected builder-speak version, and both empty
counters ("0 collected · 0 saved") read as honest zero states rather than as
broken ones. `profile.png` correctly shows the "Add a tree" entry point
while signed out, consistent with the Google Maps convention already ruled
on repeatedly (visible to everyone, acting needs sign-in): tapping it is
what should gate, not seeing it. `place-pin.png` (the pin-correction flow)
states up front that sending needs a free account and why ("so we can tell
you what your correction changed"), which is the honest, non-wall version of
the same rule. `refused.png` (location permission refused) matches the
2026-08-31 ruling recorded in CONVENTIONS.md: no interstitial in front of
the system prompt, a plain statement of what is off and why it helps.
Nothing across the six contradicts itself, overpromises, or shows a control
with no stated purpose.

Nothing found at BLOCKER or WARN level. One thing noted and deliberately not
raised as a finding: Florence's new cedar photo and the pre-existing Bucaco
photos are licensed as "Provided by [institution], all rights reserved"
rather than an open licence (CC0/CC-BY/CC-BY-SA), which is narrower than
CLAUDE.md Step 4's literal wording ("openly-licensed sources... CC0, CC-BY,
CC-BY-SA only"). This is an established pattern, not new today, and it is a
direct, verbatim-credited grant from the copyright holder rather than a
weaker claim, so it reads as more defensible than an open licence, not less.
Flagging only as context in case a future corpus pass wants to reconcile the
written rule with the practice; it is not a reader-facing problem.

---

## 2026-08-31

Reviewed the last 24 hours (134 commits, back through `323b35f4`): heavy
night-run assembly-line work (Riga opens, Girona/Madeira/Cagliari/Barcelona/
Singapore/Krakow/Nuremberg verify+write passes, a US register-scouting sweep
that found no importable register for five cities), the day's product ruling
("a place may publish below four trees when one tree is itself the
destination", `cbb2662f`) applied to Charleston, Savannah, Philadelphia,
Sant'Alfio and Maui, an account-page rebuild (`bac7be40`, name field + settings
shape), an app permission/location rework (LocationPrimer deleted, delete-account
row restored), and iOS CI now walking every installed runtime (`3d5c5e84`). Ran
`python3 scripts/qa.py` (3912 pages, clean), `python3 scripts/superlatives.py`
(525 claims, no collisions) and `python3 scripts/preflight.py` (195 cities, 0
problems besides already-tracked paid-entry NOTEs, Oahu improved from 86% to
75% today and is not re-litigated here). Confirmed yesterday's i18n BLOCKER
(stale tree counts and a wrong-oldest-tree claim on the-hague/malaga/kyoto
translation overlays) is fixed in the current build: all three now show the
corrected counts (29/9/17) and the-hague's Dutch FAQ now carries the same
appointment-only caveat as its English twin.

**BLOCKER — the map's "Walking routes, in the app" pill is false on every one
of the 93 city pages that has its own walks page, because the same page links
to that walks page two paragraphs later.** `site/src/pages/[city].astro`
(rendered e.g. in `site/dist/kagoshima.html`): the map toolbar carries a pill
reading "Walking routes" / "in the app", `data-ev="walks-app"`, exactly per
PRODUCT_IA.md's 2026-08-18 ruling ("the web city page no longer offers
walks... one small pill on the map... linking to /app"). Lower on the SAME
page, the panel footer says "Walk them. The trees of Kagoshima fall into
routes you can do on foot in an afternoon:" and links to `/kagoshima/walks`,
which is a fully built page (Contract K, SEO_GEO_BLUEPRINT.md v1.14,
2026-08-24) naming two real named walks with tree counts, distances and
minutes on foot. Checked programmatically: of 195 published places, 93 have
their own `/[city]/walks` page, and all 93 render the app-only pill on the
same page that links to it. This is not a hypothetical reader confusion, it
is the literal sequence a visitor meets: told routes need the app, then
handed a page of routes on the web. TONE_OF_VOICE.md: "Never claim more than
is true." This is the same self-contradicting-page failure class the
2026-07-29 QA walk was written to catch, on a surface no build check reads
(`qa.py` passed clean; nothing checks pill copy against the presence of the
page it would contradict). Root cause for a session to judge, not decided
here: Contract K (2026-08-24) reintroduced walks on the web six days after
the 2026-08-18 ruling took them off it, and nobody reconciled the pill's
wording with the page it now sits beside.

**WARN — the newest page type (a place publishing below four trees because
one tree is the destination, ruled today in `cbb2662f`) breaks Contract A's
"Trees nearby" block on both trees that use it.** `site/dist/santalfio/
hundred-horse-chestnut.html` and `site/dist/philadelphia/bartrams-ginkgo.html`
both render `<h2>Trees nearby</h2><div class="near-cards"></div>`, an empty
div under a heading that promises something, because each place has exactly
one tree and nothing else to put there. Charleston, Savannah and Maui (2, 2
and 4 trees respectively, published from the same ruling today) all populate
this block correctly, so the break is specific to the single-tree case the
ruling introduced. PRINCIPLES.md #3: "Empty states teach... every zero state
is an instruction, not a dead end"; this one teaches nothing, it is a gap.
The page recovers below it with a CTA to the city and question pages, so
nothing is broken end to end, but the heading-over-nothing is visible on the
built page and will recur on every future single-tree place until the
template accounts for the case (hide the heading, or drop straight to the
CTA line). The same CTA line also reads "all 1 remarkable ancient trees in
Philadelphia", a singular/plural templating slip worth a look in the same
pass.

**NOTE, Monday corpus check — PRODUCT_IA.md's walks section is stale against
a later blueprint decision, and is the direct cause of the BLOCKER above.**
The "Walks are an APP feature" section (dated 2026-08-18) states as settled
fact that "the web city page no longer offers walks" and that walks live
only behind the app pill. SEO_GEO_BLUEPRINT.md's Contract K (v1.14,
2026-08-24, six days later) added a full `/[city]/walks` page back onto the
web, with its own publish gate and content rules, and PRODUCT_IA.md was never
updated to note the supersession or reconcile the pill copy with it. Suggest:
add a line to PRODUCT_IA.md's walks section pointing at Contract K the way
the document already does for its other superseded rulings, and settle
whether the pill should say "more, in the app" or similar once the wording
is decided.

**WARN, APP — the map's expanded-sheet frame shows a floating "Map" pill
rendered on top of a tree card in the nearby-trees carousel, not above it.**
`map-full.png` (iPhone SE): "The Rijksmuseum Wingnut" card is followed by a
second card whose photo area is replaced by a white cloud-shaped glyph and a
dark "Map" pill sitting centred over it, with only a sliver of the tree's own
name ("...ch Elm") visible beneath the tab bar at the very bottom edge. Read
cold, this is a control with no stated purpose sitting inside a scrolling
list of tree cards rather than fixed over the map itself (the AllTrails-style
floating list/map toggle PRODUCT_IA.md describes), and it obscures the one
thing the card exists to show, the tree. Not a mechanical CLIPPED/SMALL/DRIFT
fault appfit.py would catch, since nothing is off-screen or misspaced by a
few points; it is a stacking/placement question for a session with Xcode
to look at directly, per CLAUDE.md's rule that runs do no visual-taste work
on the app.

Nothing else found at BLOCKER level in the web or app diffs. The account
page rebuild (`bac7be40`) reads consistent with the both-surfaces rule and
PRINCIPLES.md #10 (no personal data beyond what is already stored, no name
shown anywhere but the account's own settings row); its own commit message
flags it as not visually verified, and the built `site/dist/account.html`
does contain all the ids its script references, so nothing is structurally
missing.

## 2026-08-30

Reviewed the last 24 hours (back through `95369942`, ~137 commits): the
hard-rule-10 access sweep (`da226ec1`, five trees pulled for needing
somebody's permission, plus the `check_access_permission()` ratchet in
`570eab4f`), the account-write gate closing (`e3191efe`, "adding a tree needs
an account, at the write and not only at the buttons"), a pin-precision
upgrade pass (`0596b369`, 112 pins), a dead-code sweep (`c40e673f`), Batch 007
outreach mail (Hidde-approved, `f66491a2`), and heavy night-run assembly-line
work (Vancouver/Cagliari/Barcelona/Naples/Perugia verify claims, register
girth/height backfill on 413 trees). Ran `python3 scripts/qa.py` (3723 pages,
clean), `python3 scripts/superlatives.py` (497 claims, no collisions) and
`python3 scripts/preflight.py` (180 cities, 0 problems besides the paid-entry
NOTEs already tracked from prior days, not re-litigated here). Spot-checked
the Hague's rebuilt oldest-tree question page and Malaga's post-removal city
page directly in the built HTML: both correctly answer from their own reduced
tree lists in English. Sampled `/species/downy-oak`, `/parks`, `/press`
clean of banned words and em dashes.

**BLOCKER — yesterday's hard-rule-10 removal (`da226ec1`) updated the
canonical city files but not their translation overlays, so three published
pages still promote a tree that was pulled specifically for failing hard
rule 10, or a stale count, or both.** Hard rule 10 and its new ratchet
(`570eab4f`) are unambiguous: a tree needing somebody's permission does not
ship. The English pages for The Hague, Malaga and Kyoto were fixed correctly
(29, 9 and 17 trees respectively, with The Hague's English question page
explicitly explaining that its true oldest tree, the 1638 Juttepeer, is not
on the list "because it needs a booked tour"). Their translation overlays in
`data/i18n/` were never touched:

- `data/i18n/nl/the-hague.json` still lists 30 trees (`title`: "de 30
  mooiste") against the canonical 29, and its FAQ answer to "Wat is de oudste
  boom van Den Haag?" (built into `site/dist/nl/the-hague.html`) states flatly
  that the oldest tree is "De juttepeer van het Heilige Geesthofje... waarschijnlijk
  de oudste perenboom van Nederland", with no caveat in that answer that it
  needs an appointment. This directly contradicts its own English twin one
  click away, which names the Koekamp Oak as oldest and explains why the
  pear is not counted.
- `data/i18n/es/malaga.json` still lists 10 trees against the canonical 9;
  the built `site/dist/es/malaga.html` title tag reads "10 ejemplares
  singulares" and its FAQ says "Seis de los diez árboles de esta lista llevan
  una de esas placas", both stale by one. A second FAQ answer still describes
  "el aguacate del colegio de Churriana" (mlg_010, the removed appointment-only
  school tree) as one of "los árboles singulares de Málaga", as if it were
  still part of the collection rather than pulled from it.
- `data/i18n/ja/kyoto.json` still lists 18 trees against the canonical 17;
  the built `site/dist/ja/kyoto.html` title tag reads "京都の巨木と名木18選"
  (18 selections).

This is the same failure class CLAUDE.md's own ratchet already names ("copy
promising a tree count the city does not have"), reaching a surface the
existing checks do not cover: `check_country_counts()` in preflight.py
guards country pages, `check_tree_count_claims()` in qa.py guards only the
one sitewide "N trees worth the walk" line, and neither reads a per-city
page's own title or FAQ, hand-written per language under Contract J. The
Hague's case is the more serious of the three: it is not just a stale
number, it is a live page telling a Dutch-speaking visitor the wrong tree is
the city's oldest and omitting the access warning its own English page
carries.

**WARN, APP — a tree with no photograph, viewed by someone who has not
collected it, shows two identical-purpose "add a photo" buttons at once.**
`tree-nophoto.png` (Caucasian Wingnut and Weeping Silver Lime, Maastricht):
a camera icon sits in the top-left corner of the placeholder image AND a
second camera icon sits in the bottom action bar, both wired to the same
`navigator.collectNearby = true` action
(`ios/AncientTrees/AncientTrees/Screens/TreeDetail.swift:971-990` and
`:1070-1082`). The code's own comment on the overlay button says it exists
"ONLY WHERE THERE IS NO PHOTOGRAPH" and was added specifically to stop a
"second camera two centimetres from the one in the bar" on trees that DO
have a photo, but the bar's camera renders unconditionally whenever the tree
is not the visitor's own (`if mine == nil`), so the exact duplication the
comment says was fixed for the has-photo case still happens for the
no-photo case, which is the more common one (1,077 of 1,435 trees per the
same file's own comment). A person looking at this screen sees two controls
with no visible difference in purpose.

Nothing else found at BLOCKER level. Not a Monday, so no scheduled
corpus-rot audit this entry.

## 2026-08-29

## 2026-08-29

Reviewed the last 24 hours (back through `90b07ce3`): night-run assembly-line
work (Bucaco +4/LA +1/Warsaw +1 writes, Salzburg opened at 5, a genus-name
lexicon widening READY leads, a photo-vendoring pass, Gdansk 4-to-6, walking
routes regenerated) plus this morning's verify claims (Naples' Magnolia of
Capodimonte shipped flagged with two conflicting register sizes, Cagliari's
Blue Eucalyptus of Sinnai, a Barcelona Pedralbes claim that duplicated three
already-published trees and was correctly untangled into leads/blocked before
anything shipped twice, and Oahu's Banyans of Thomas Square). Ran
`python3 scripts/qa.py` (3690 pages, clean), `python3 scripts/superlatives.py`
(497 claims, no collisions), `python3 scripts/preflight.py` (clean besides the
two items below) and `python3 scripts/health.py` (rung 2 is a dropped-cron
knock count, not a broken build; not re-litigated here). Spot-checked
oahu/naples/cagliari/barcelona's new tree pages plus five random other pages
(alkmaar, enschede, padua, zurich, and yesterday's Oahu WARN pages) for em
dashes, banned words and count consistency: all clean, and every stated tree
count in the built HTML (Oahu "7", Naples "twenty-three", Cagliari "nine")
matches its own trees array.

**WARN — Oahu's paid-entry ratio is still 86%, and the commit message
overstates what today's addition did.** Yesterday's WARN here said Oahu was a
"garden page, not a city page" at 100% paid (6/6) and asked for a free,
walkable tree. Today's `1c067fcb` added one, the Banyans of Thomas Square
(free, Honolulu's oldest public park), and its own commit message says this
brings "the ratio to 86%" without saying what that number means against the
rule: CLAUDE.md's 2026-08-23 ruling sets the ceiling at "at most about a
third," reached after Hidde said "ik heb liever 34 goede bereikbare dan 39."
`scripts/preflight.py` still reports it: `Oahu: 6 of 7 trees are behind paid
entry (86%)`. One free tree is real progress and the right kind of fix
(CLAUDE.md: "the answer to a bad ratio is FREE TREES ADDED"), but the page is
still, by the corpus's own words, the shape it explicitly forbids. Rung-3 work
for a research pass: at least one or two more free Oahu trees outside Foster
Garden and Moanalua before this city reads as solved.

**WARN — the `paid_entry` boolean that drives the tree page's "Ticket
needed" banner is unreliably set, and one of today's own touched trees is a
live example.** `site/src/pages/[city]/[tree].astro:203` renders `{tree.
paid_entry && <p class="ticket-note">Ticket needed...}` directly under the
breadcrumbs, deliberately placed there per Hidde's 2026-08-24 ruling "because
it changes whether somebody sets off at all." Checked every city file for
trees whose `access` text unambiguously says paid entry (excluding two
false-positive phrasings where only a museum inside a free park charges,
Aarhus's Moesgard trees and NYC's nyc_010) against the `paid_entry` field:
8 trees across 5 cities have paid access text but no `paid_entry: true`, so
their pages render no ticket banner at all. Confirmed directly in the built
site: `oahu/hitachi-tree.html` (hnl_006, $10 Moanalua Gardens admission,
added yesterday in `a3b7da0b`, untouched by today's Oahu commit) has zero
occurrences of `ticket-note`, while `oahu/foster-garden-baobab.html` (same
city, `paid_entry` correctly set) has one. The other seven: `bcn_002`,
`bcn_003`, `bcn_016` (Park Guell, "no free zone" since 2020), `crt_001`
(Crete, Olive Tree Museum of Vouves), `sev_042` (Seville, Monasterio de la
Cartuja/CAAC), `war_012`, `war_013` (Warsaw Botanical Garden). This is a data
hygiene gap rather than a new bug (`preflight.py`'s own `check_paid_share()`
reads the `access` string, not the boolean, which is why it never caught
this), but it means the site is currently promising free entry by omission on
eight pages where a visitor will in fact be asked to pay. Rung-3 work: set
`paid_entry: true` on the eight trees named above; a build check comparing
the two fields would catch a ninth.

**NOTE — yesterday's open app question is resolved.** The 2026-08-28 entry
here could not confirm whether `signin.png`'s stale data-promise sentence was
a captured-before-the-fix artifact or a live bug. Today's `signin.png`
(same screen, fresh sweep) reads "We store your email address and what you
collect: the trees you save, the ones you photograph, and where they stand.
No advertising, and you can delete the lot from this app," which matches
`SignIn.swift:262` exactly. The fix (`8060afd2`) is live.

**APP screenshots (rotation, iPhone SE): place-pin, primer, profile-edit,
profile, search, signin.** All six looked at, none flagged beyond the note
above. `place-pin.png` (the pin-correction flow, "Where is it really?") and
its account-gated submission match the 2026-08-21 feedback ruling. `primer.
png`'s tree count ("We map 1,941 remarkable old trees") trails the live data
count (1,950) by 9, which is normal feed lag from today's four new trees plus
Salzburg's five from yesterday, not a bug worth a build check. `profile-edit.
png`, `profile.png` (Settings, with "Add a tree" copy matching the
reader-as-subject fix) and `search.png` are unremarkable and correct.

Nothing else found at BLOCKER level. Not a Monday, so no scheduled corpus-rot
audit this entry.

## 2026-08-28

Reviewed the last 24 hours of git history (back through `00547c5e`, roughly
140 commits): heavy unattended night-run churn (Groningen, Maastricht,
Utrecht, Oss, Krakow, Warsaw, Leipzig opened/deepened, Sardinia register
import, a Canada famous-trees sweep, a genus-name refill taking READY leads
54 to 366) plus a full Friday session (the `[city]`-means-a-place blueprint
change to v1.15, the first two Commons famous-trees imports for Seattle and
Oahu, a walking-routes rebuild, six data-promise corrections across app and
web, the sponsor page rewritten in Hidde's own words, and a "Build 2" TestFlight
archive). Ran `python3 scripts/qa.py` (3643 pages, clean), `python3
scripts/superlatives.py` (485 claims, no collisions), `python3
scripts/preflight.py` (174 cities, 0 problems) and `python3
scripts/copycheck.py` (clean, no absolute-claim tics). `python3
scripts/health.py` shows rung 2 is not clear: the iOS app's newest scheduled
run failed 1.4h ago; already surfaced there, not re-litigated here.

Spot-checked the `[city]`-means-a-place change (v1.15) against Contract A: the
three stated guardrails (four-tree floor, a name a person would say out loud,
only real cities on `/cities`) are the only new rules, and nothing in the
diff loosens the never-cuttable list. Verified the Oahu tree-page walks-link
fix (`fc88da35`) directly in the built site: `/rome/adonis.html` correctly
says "See the 2 walks past Rome's other trees", and `/oahu/hitachi-tree.html`
(a city with no walks page) says nothing about a walk at all, which is the
intended behaviour, not a silent gap. Sampled 3 further pages at random
(`/es/malaga/arbol-mas-antiguo`, `/species/silky-oak`, `/portugal`): clean
titles, no banned words, no em dashes.

**WARN — Oahu is a garden page, not a city page, and today's addition made it
more so rather than less.** `data/cities/oahu.json`: all 6 trees now carry
`paid_entry: true` (`preflight.py` flags it as a NOTE: "Oahu: 6 of 6 trees are
behind paid entry (100%)"), 5 in Foster Botanical Garden and, as of today's
`a3b7da0b`, 1 in Moanalua Gardens (the Hitachi Tree, $10 entry). CLAUDE.md's
2026-08-23 ruling on exactly this shape is explicit: "at most about a third
of a city may sit behind a ticket," reached after Hidde objected to Amsterdam
being one-third ticketed ("ik heb liever 34 goede bereikbare dan 39"), and
names the failure mode by description: "what is not allowed is a city page
that turns out to be a garden page, which is what happens when a run opens a
city by taking the easiest eight trees out of one ticketed collection." Oahu
is that page at 100%, not a third. The rule's own fix is written down too
("the answer to a bad ratio is FREE TREES ADDED rather than good ones
removed"), which today's commit had the chance to do (it was adding a tree
from a country-wide famous-trees sweep, not limited to Oahu's two gardens)
and instead added a second ticketed one. Not a BLOCKER because `preflight.py`
deliberately treats this as a NOTE rather than a build failure, by design,
for cases where the trees themselves are the legitimate best available; this
is flagged because the ratio moved the wrong way on the same day a free
alternative (Sylvia, added to Seattle in the same commit) was sitting right
there in the same sweep unused for Oahu. Rung-3 work for a research pass:
find a free, walkable Oahu tree outside the two gardens before adding a
seventh.

**APP screenshots (rotation, iPhone SE): profile-edit, profile, search,
signin, species, sponsor.** All six looked at. `profile.png`,
`profile-edit.png` and `sponsor.png` (Settings, profile editor, and the
"Sponsor this project" sheet reachable from it) read clean against
PRODUCT_COPY.md and TONE_OF_VOICE.md: "You can add a tree by taking a
photograph of it and filling in what you know" matches the reader-as-subject
fix from `9860c876`/CLAUDE.md's own worked example. `search.png` (a
place-search result for "lis") and `species.png` (the Aleppo Pine species
sheet, five cities named, none contradicting the site's own pages) are both
unremarkable and correct. `signin.png`'s account-benefit dialog is the
Geocaching-style "that tree is yours, sign in to keep it" pattern and matches
the convention.

**NOTE, APP — the sign-in dialog's data-promise sentence in the screenshot
does not match what ships in the source today, and it is the exact sentence
today's own fix targeted.** `signin.png` reads "We store your email address
and the trees you collect. Nothing else, no advertising, and you can delete
the lot from this app." `ios/AncientTrees/AncientTrees/Screens/SignIn.swift:262`
currently reads "We store your email address and what you collect: the trees
you save, the ones you photograph, and where they stand. No advertising, and
you can delete the lot from this app.", changed today in `8060afd2` ("Every
old promise about somebody's data...") specifically because "Nothing else"
was named there as one of six stale absolutes, "against eight declared data
types." `copycheck.py` is clean against the current source, so the fix is
real; what cannot be confirmed from here is whether the screenshot in
`/tmp/appshots` was captured before that commit landed (in which case this is
a stale artifact, not a live bug) or from a build the fix has not reached.
Given the commit exists specifically to kill this sentence, a session should
re-run `appsweep.py` and confirm the live build shows the corrected text
before trusting this screen fixed.

Nothing else found at BLOCKER or WARN. Not a Monday, so no scheduled
corpus-rot audit this entry.

---

## 2026-08-27 (second pass, evening)

Reviewed since the last review commit (`9d2fba34`, 2026-08-27 12:32 UTC): 41
commits, spanning a long afternoon/evening app session (My trees restructure,
sign-in-linked social features with report/block, account deletion proven
end-to-end, worth-it vote counts, a gold "my tree" ring on the map, a live
feed/app contract so a website deploy cannot silently break every installed
phone, and a self-inflicted two-hour deploy outage found and fixed by the new
alarm) plus two night-run city passes (Bari opened at its 4-tree floor,
Barcelona 46 to 52 off its own leads shelf) and a Kyoto species/title
correction. Ran `python3 scripts/qa.py` (3574 pages, clean), `python3
scripts/superlatives.py` (480 claims, no collisions), `python3
scripts/preflight.py` (173 cities, 0 problems, same two pre-existing paid-share
NOTEs as before) and `python3 scripts/health.py` (rung 2 clear; Smoke test,
Build and deploy and iOS app all show "cancelled" but health.py already reads
that correctly as push-cancels-predecessor rather than breakage, per today's
own `6f9fe2f7`/`975e59ed` fix, and its scheduled iOS run is green).

Spot-checked the two data changes directly: Barcelona's renamed Erythrina
caffra ("Coast Coral Tree") does not collide with the existing Erythrina
corallodendron entry (grepped both; different ids, superlatives.py agrees),
and Kyoto's kyo_016 rename ("Sudajii of Omiya Gate" replacing the
self-contradicting "Chinkapin oak (Sudajii)") is live on the built site with
its old URL redirecting via the new `RENAMED_TREE_SLUGS` entry. Sampled 5
other pages at random (Alkmaar, Cambridge, Geneva, Lucca, Poland): clean
titles, no banned words, no em dashes.

**APP screenshots (rotation, iPhone SE): map-full, map, paywall, people,
place-pin, primer.** All six looked at. `people.png`'s "Find people" list
(Marieke/Tom/Sofia) traces to `Kit/DemoPeople.swift`, added today,
launch-argument-gated and documented in its own header as unable to reach a
real build's screen; not a finding. The floating "Map" pill mid-screen in
`map-full.png` traces to `MapTab.swift`'s documented back-to-map button
(shown only at full sheet height, per Hidde's own 2026-08-25 correction); not
a finding. `primer.png`'s "We map 1,858 remarkable old trees" is the app's
bundled fallback catalogue, 10 trees behind the live 1,868, which is exactly
today's Barcelona (+6) and Bari (+4) additions, i.e. an expected bundle-vs-live
lag rather than a wrong count.

**WARN, APP, FOR HIDDE — the paywall screen narrates our own construction
progress to the reader, which TONE_OF_VOICE.md names and bans almost verbatim.**
`ios/AncientTrees/AncientTrees/Screens/Paywall.swift:85`: "Plus is not open
yet. **We are building it**, and this is the list." TONE_OF_VOICE.md's
"No builder-speak toward the visitor" section states the rule plainly: "Copy
states what something DOES, never its state of construction," and lists
"still being built" by name among the banned phrases, exactly what "we are
building it" says with different words. The rest of the screen already fits
the document's own carve-out for this case ("an honest, styled 'coming soon'
... the app page's waitlist is the model"): "Plus is not open yet" plus "Tell
me when this opens" is that pattern done right. The one clause that steps
outside it is "we are building it," whose subject is our own progress rather
than the visitor. This is Hidde's own copy (commit `1706026c`, 2026-08-25,
"it just says it will come soon"), so this is not reported as an error, only
said out loud per the corpus's own rule for handling his decisions ("the
contradiction must be said out loud so changing course is a decision, never a
drift"): keep it if that is the intended exception, or drop the clause and
let "not open yet" carry the sentence alone.

Nothing else found at BLOCKER or WARN. Not a Monday, so no scheduled
corpus-rot audit this entry.

---

## 2026-08-27

Reviewed the last 24 hours of git history (back through `8910fc07`, spanning
Wednesday afternoon into Thursday, roughly 100 commits): a long iOS session
(tab bar redesign, profiles/follow/block/report, account deletion proven
end-to-end, the sponsor sheet, the flow-walk QA layer, TestFlight prep) plus
the usual night-run research passes (Cologne opened from zero, Nijmegen,
Toronto, Guimaraes, Alicante, Palma verify passes, a Las Vegas self-correction
restoring three wrongly-pulled trees) and a Wikidata-layer rework of the city
queue. Ran `python3 scripts/qa.py` (3531 pages, clean), `python3
scripts/superlatives.py` (480 claims, no collisions), and `python3
scripts/health.py` (rung 2 shows the 2026-08-23 BLOCKER already answered;
The Hague's intro now correctly reads 30 trees, confirmed against the built
page and the underlying data file).

**APP — could not run the screenshot pass this cycle: `/tmp/appshots-list.txt`
is empty and `/tmp/appshots-note.txt` says "no screenshots under
/tmp/appshots."** Given the size of tonight's app session (a full nav/tab
redesign, new profile and moderation screens, a new sponsor sheet), this is
the cycle where a visual pass would matter most. Flagging rather than
guessing from diffs.

**WARN, APP — a second, undocumented meaning for gold on the map, the exact
kind of change DECISIONS.md asks to have recorded when it happens.**
`ios/.../Screens/TreeMap.swift` (commit `51d6b061`, today) draws a gold ring
around the pin for any tree a person added via their own photograph, with the
commit's own reasoning: "Gold is allowed here and nowhere else outside Plus:
this is the one thing on the map that is yours rather than ours." But
DECISIONS.md's 2026-08-25 entry states the rule this touches in plain words:
"a ticket is not a Plus feature, so the ticket mark on a pin left gold for
blue. **Gold means paid-by-us everywhere else in the app**," and that entry
exists specifically because "it moves a colour rule" and the project's own
practice is to record such moves. Adding a tree by photograph is explicitly
FREE (2026-08-20: "ticking is FREE; the PROOF is what is sold" refers to the
photo/GPS-seal bundle as Plus, but collecting itself, including a
self-submitted tree per 2026-08-24's "he comes to us whether they offer it or
not," is not gated). So a reader who has internalised gold-means-Plus from
the ticket badge may reasonably read their own free contribution's gold ring
as a paid-tier marker, which is the reverse of the intended message ("yours,
not ours"). This may well be exactly what Hidde wants (his own message
proposed "met een gouden randje ofzo," tentative wording), but it is a colour
rule that changed without a DECISIONS.md line the way the 2026-08-25 one got
one, and the next session touching pin colours has no single place to learn
both exceptions exist. FOR HIDDE: whether gold should mean two different
things on the same map, or whether the "my trees" ring should use a different
colour now that blue already carries "not one of our own tiers."

Nothing else found at BLOCKER or WARN on the web side. Spot-checked the
sponsor page, support page, privacy and terms (all touched today) against
TONE_OF_VOICE.md and the builder-speak/never-explain-our-rules rules: clean,
no banned words, no leaked personal data (the 2026-08-22 Gmail-address WARN
in CURATION.md is also gone, confirmed by grep). Spot-checked Rome's new
Eucalyptus of Forte Ardeatino entry (added by tonight's verify pass): the
tree correctly ships with `photo.status: missing` and no photo anywhere in
its schema, og:image falls back to the default, and an earlier read of a
ginkgo filename near it in the raw city-page HTML turned out to belong to an
unrelated `ItemList` entry, not this tree; false alarm, recorded so it is not
re-chased. Not a Monday, so no scheduled corpus-rot audit this entry.

---

## 2026-08-23

Reviewed since the last review commit (`a9d6f4c`, 2026-08-22 07:00 UTC): 198
commits, roughly 24 hours of unattended register/write-pass churn (The Hague
21 to 30, Brisbane 10 to 14, Seville 20 to 37, Cork 5 to 13, four new Dutch
cities from staged LRMB write passes, Amsterdam/Zaanstad/Haarlemmermeer,
Haarlem/Hilversum/Hoorn, Oahu published) plus a large app-design session and
the seven-language Contract J rollout going live in the blueprint. Ran
`python3 scripts/qa.py` (3202 pages, clean), `python3 scripts/superlatives.py`
(483 claims, no collisions) and `python3 scripts/preflight.py` (171 cities,
0 problems, two pre-existing NOTEs on Hawaii/Oahu about shared coordinates).

**BLOCKER — The Hague's city page contradicts its own tree count: the intro
says "Twenty-one trees in all" while the page has 30.** `data/cities/the-hague.json:5`,
live on `site/dist/the-hague.html`. Commit `6aa4e2a9` took the city from 21
to 30 trees and correctly updated `meta_description` ("30 verified trees"),
`question_meta` ("All 30 mapped"), and the FAQ, but the intro's closing
sentence, the last line a visitor reads before the tree list, was left at
the old count. This is exactly the error class CLAUDE.md names as a build
check already earned by two prior incidents ("copy promising a tree count
the city does not have") and P7 ("truth outranks polish") condemns as a
self-contradicting page. It slipped past the guard that exists for it,
`site/src/lib/count-promises.ts`: the checker's seven phrasing patterns
(`N more`, `all N trees`, `N verified locations`, etc.) do not cover "N
trees in all", so the Astro build did not throw. Checked the rest of the
corpus for the same phrasing (`grep` across all 171 city files' intro/meta/
question fields for "<number> trees in all/in total/mapped"): The Hague is
the only real hit, so this looks like an isolated miss rather than a
pattern, but the checker itself now has a known gap worth widening the next
time count-promises.ts is touched.

Nothing else found at BLOCKER or WARN. Spot-checked five other pages picked
at random (Rome, Poznan, Cadiz, Oslo, Zaragoza): no banned words, titles and
counts read consistent. Not a Monday, so no scheduled corpus-rot audit this
entry.

---

## 2026-08-22

Reviewed since the last review commit (`316d086`, 2026-08-21 07:10 UTC): 133
commits, spanning a night of research (Nijmegen 8 to 11 trees, its oldest
tree now the Kabouterboom at Beek), a large session on the contributor-reply
loop and account-gated feedback (web + iOS), several homepage shelf
additions (countries, species, parks, oldest-trees, all from Hidde's own
session), three self-inflicted night-run outage fixes, and the usual
digest/queue/photo-sweep churn. Ran `python3 scripts/qa.py` (2370 pages,
clean), `python3 scripts/superlatives.py` (432 claims, no collisions) and
`python3 scripts/health.py` (rung 2 clear, no BLOCKER, REVIEW.md's
2026-08-21 WARN already answered by `537a9ec`, see below).

**WARN — Hidde's personal Gmail address is committed in plain text in
`CURATION.md:16`, the only place in the repo it appears.** Commit
`8a81a3a` ("Process submissions 11-36...") resolved a Supabase `user_id` to
an email via `/auth/v1/admin/users` to work out whose test clicks a batch of
26 feedback rows were, and wrote the resolved address straight into the
entry: "all from one `user_id` that resolves to burgmans.hidde@gmail.com."
PRINCIPLES.md #10 is explicit and does not carve out an exception for
internal files: "no personal name, no personal location..., no personal
email, no photo, no social links, **anywhere public**: site copy, schema,
privacy page, commit identities, **artifacts**." A committed markdown file
is an artifact under that rule's own list, and this repo's remote is
`github.com/burgmanshidde-ancienttrees/ancienttrees`, a name that already
identifies the owner, which makes leaking the address alongside it a real
rather than theoretical exposure. The identification itself (working out
that the burst was Hidde's own QA rather than a reader) was good, careful
work and the right call not to treat it as feedback; only the verbatim
address in a committed file is the problem. FOR HIDDE: whether the address
should be scrubbed from git history is his call (rewriting history is the
kind of irreversible-in-public action hard rule 3 and the mandate's
question-3 test both flag); a run should not do this unprompted. Any run can
safely fix the forward-looking half now: redact the address in CURATION.md
to "his own account" or similar, the way `f36b0c9`'s note already does it
right ("the address is his own").

**NOTE — the built homepage no longer matches the order PRODUCT_IA.md
documents, and nothing supersedes that section.** "The homepage, reordered"
still reads: (1) hero, (2) the four verbs as sections, (3) *one* opinionated
shelf, (4) the compact explore directory. The built `site/dist/index.html`
now runs hero -> "Our favourite tree cities" shelf -> the four verbs
(`home-acts`) -> Countries shelf -> Species shelf -> Parks shelf -> "The
oldest trees we map" shelf -> the directory: a curated shelf ahead of the
verbs, and four shelves after them rather than one. This looks like
deliberate, reviewed work rather than drift: the commits (`b303b5e`,
`7b0034e`, `0530ba8`, `901e547`, `238e27a`, `34bfc5e`) are Hidde's own
session, one of them opens with him spotting a repeated photo across
shelves and fixing it on the spot, which is exactly the pixel-level
composition check PRINCIPLES.md #11 asks for. So this reads as a real
direction change that the document simply was not updated to record, not a
build defect. Worth a line in PRODUCT_IA.md's homepage section the next time
that file is touched, so a future run does not read the stale five-year
version as current.

Nothing else found at BLOCKER or WARN. Not a Monday, so no scheduled
corpus-rot audit this entry; the NOTE above surfaced during the general read
rather than a sweep.

---

## 2026-08-21

Reviewed since the last review commit (`16adc7d`, 2026-08-20 07:08 UTC): 161
commits, roughly 24 hours spanning a full session on the iOS app (thin
outline tab icons, a Spot-sheet close control, the tab bar hidden on pushed
pages, a new `scripts/appcopy.py` guard that caught a licence-explaining
hero line) alongside the usual night-run and session data work (a Dutch LRMB
register run closing 8 cities/36 trees including The Hague to 21 and
Brussels to 26, a Milan+Brussels leads-file write pass taking Brussels to
30, two register scouts recorded empty/blocked for Reykjavik and Kansas
City, and the daily digest gaining a saves/trees-sent/feedback split per
Hidde's same-day ask). Ran `python3 scripts/qa.py` (2364 pages, clean),
`python3 scripts/superlatives.py` (430 claims, no collisions) and `python3
scripts/health.py` (rung 2 clear, no BLOCKER) against the built site.

Spot-checked the highest-risk items against the built output rather than
commit messages: Brussels' and The Hague's hand-geocoded/hand-mined
additions (bru_024-030, hag_018-021) all carry honest `location_precision`
(`approximate` wherever the register gave a shared or inferred point,
`confirmed` only where the register's own coordinate is used directly) and
notes stating the inference method, which is exactly what hard rule 2 and
the location-honesty rule ask for; the built Brussels page's title, FAQ and
oldest-tree question page all say "30"/"thirty" with no leftover "26" or
"twenty-six" anywhere, so the count-promising-copy fix mentioned in the
commit message actually shipped. The homepage hero button churn
(`25a5b03` then `78b8141` reverting it back to a text link, both Hidde's own
session) nets to the built homepage still showing the plain text link, so
there is nothing live to flag. No price string, "trial" or "Season Radar"
anywhere in `site/dist/app.html`, so CLAUDE.md's "do not put the price on
the website until he says it goes live" still holds.

**WARN — the night-run continuation fix shipped 2026-08-20 has not been
shown to fix the thing it was built for, and the three cron knocks since
are evidence it might not be working.** The 2026-08-20 session diagnosed a
real problem (runs ending cleanly at 5-25 minutes of a 120-minute window,
shipping nothing, leaving claims that cascade into the next run) and built
a continuation step, closing with "None of this is proven yet. The next
cron knock is the test." `data/run-health.json`'s last three entries, all
after that fix (2026-08-21T02:52, 04:25, 06:21 UTC), all show `attempts: 2`
(so the continuation step is firing), all end at 15-26 minutes with 0 trees
and 4-6 commits, and each leaves a fresh claim (krakow, then oahu, then
seville+caserta) for LOG.md's own auto-generated "ended without saying
anything" entry to report. Their denial rates (43/143, 42/198, 35/140 =
0.21-0.30 per turn) are 2-3x the two most recent successful single-attempt
runs (18/228 = 0.08, 30/219 = 0.14 on 08-20T00:29 and 08-20T18:48), which
is worth naming because the same 2026-08-20 session had just concluded from
the pre-fix dataset that denials were "not the cause: near identical per
turn, a constant tax". That conclusion was drawn before this data existed
and the new numbers do not obviously agree with it. Nobody has looked back
at these three runs since they landed; LOG.md's auto-entries for them are
the generic "written by the workflow's Run health step" boilerplate with no
comparison to the fix. This is not proof the fix failed, a run's own
transcript is hidden by design, but it is three data points in the
direction the fix was supposed to prevent, and the file that promised to
check ("the next cron knock is the test") has not been reopened since.

**NOTE — CLAUDE.md's capacity-doctrine paragraph still says night cron
knocks are "each capped at 60 minutes," which has been wrong since
2026-08-17/19.** `.github/workflows/nightly.yml` sets `timeout-minutes: 120`
(comment: "GitHub allows six hours per job; we take 120 minutes"), and
DECISIONS.md's 2026-08-19 entry and every `run-health.json` record this
window agree on 120. CLAUDE.md's line was last touched 2026-08-12, before
the 2026-08-17 change (c61b64c per LOG.md), and reads: "The only trigger is
nightly.yml's nine cron knocks a day, each capped at 60 minutes, which is
what DATA.md's utilization meter has been counting all along." A run
skimming that paragraph for how much time a knock actually has would get
the wrong number by half. Small, mechanical fix: change "60" to "120" and
update the utilization-meter framing to match, or drop the specific number
and point at nightly.yml as the source of truth the way the sibling
`data/in-flight.json` note now does after the same lesson (see next note).

**NOTE — `data/in-flight.json`'s own `expire_hours_by_holder.night-run`
(1.5) and its `expire_hours_note` still describe the exact bug the
2026-08-20 session said it fixed.** That session's log entry: "a night-run
claim expired after 90 minutes on the strength of a docstring saying the
job is killed at 60, while the cap has been 120 since c61b64c... The expiry
is now read from the workflow instead of remembered." `scripts/passcheck.py`
does now override `by_holder["night-run"]` at runtime via
`night_run_expiry_hours()`, which greps `timeout-minutes` straight out of
nightly.yml, so this is cosmetic rather than a live bug: nothing actually
expires a claim at 90 minutes any more. But the JSON file a human or a run
would read directly still says 1.5 hours and still explains it with "the
job is killed at 60 minutes," which is the same stale-docstring shape the
fix was written to eliminate. Worth a one-line edit to say the number is
derived from nightly.yml and not to be trusted as written, the way the
script's own docstring already does.

Nothing else found at BLOCKER or WARN. Not a Monday, so no corpus-rot audit
this entry beyond the two NOTEs above, which surfaced during the general
read rather than a scheduled sweep.

---

## 2026-08-20

Reviewed since the last review commit (`9700788`, 2026-08-19 12:02 UTC): 99
commits to `d778755`, an unusually large window spanning a full session on
the iOS app (accounts, Sign in with Apple, the freemium paywall screen, a Map
tab rebuild) alongside the usual night-run and session data work (Los
Angeles, Seattle, Dallas, Mexico City, Ottawa, Bilbao, Hawaii/Big Island,
Copenhagen and Tallinn photo/tree additions, Vienna, Palermo, Geneva, Lyon,
and a run of Dutch cities: Arnhem, Utrecht, Groningen, Haarlem, Maastricht,
Rotterdam). Ran `python3 scripts/qa.py` (2287 pages, clean), `python3
scripts/superlatives.py` (419 claims, no collisions) and `python3
scripts/health.py` (rung 2 clear, no BLOCKER) against the built site.

Spot-checked the highest-risk-looking items by reading the actual diffs and
built output rather than trusting commit messages: the iOS paywall screen
(`Entitlement.swift`, `Paywall.swift`) shows Hidde's own 2026-08-18 price and
never processes a purchase, only a waitlist join, so hard rule 2 (no taking
payments) is not touched; Las Vegas' removal of three published trees
(state-champion status but 51-102cm trunks) was Hidde's own editorial call in
session, with redirects added in `redirect-map.ts` for all three retired
slugs, so hard rule 3 is not touched; "Walks draw their line" turned out to
be `ios/.../Screens/TreeMap.swift`, the app's own walk view, not a
reappearance of walk routes on the web city page (PRODUCT_IA.md's
2026-08-18 ruling that walks left the web is intact, verified against the
built city pages: no route capsule anywhere in `site/dist`). The new Ottawa,
Mexico City and Bilbao tree stories read clean against TONE_OF_VOICE.md and
the bridge-claim rule: uncertainty is stated plainly ("nobody wrote down...
if you know its age, tell us") rather than bridged into a false precision,
sources are named per claim, and the new photographs (Skovfogedegen, Kelch's
Linden, the Eschersheimer Linde, Mexico City's ahuehuete) all carry a
verified CC BY-SA licence and attribution that renders on the built tree
page. The sign-in dialog trim (`SignInModal.astro`) uses `textContent`, not
`innerHTML`, to insert the saved tree's name, so no injection risk from a
tree name string.

Nothing found at BLOCKER or WARN. Not a Monday, so no corpus-rot audit this
entry.
## 2026-08-19

Reviewed since the last review commit (`8ca5ccd`, 2026-08-18 07:07 UTC): 75
commits to `328879f`, roughly a day and a half spanning the tail of a
research/product session (Dutch national register import, Amsterdam/The
Hague/Leiden batches, the paywall copy, saved-trees-to-account, walking
routes leaving the web) and a morning largely spent on the iOS app and on
CITY_QUEUE.md's targets and ordering (three corrections in one morning,
recorded in DECISIONS.md 2026-08-19). Ran `python3 scripts/qa.py` (2113
pages, clean) and `python3 scripts/superlatives.py` (395 claims, no
collisions) against the built site.

**WARN — `scripts/city_queue.py --next`'s STAGE 1 header claims Hidde
authorized from-zero web research for 181 cities; he named 17.** The command
is the one `nightly.yml` tells every run to use for city order
(`.github/workflows/nightly.yml:232`). Its printed header reads: "STAGE 1,
OPEN THE UNOPENED: every ranked city with no trees yet, to 10, as fast as
they go... A register is NOT required here; he named these cities, which is
what rule 1(d) asks for before from-zero research" (`scripts/city_queue.py`
lines 414-417, mirroring the code comment at lines 390-403). The list under
that header is `s1 = [c for c in doc["cities"] if c.get("rank") and not
c.get("trees", 0)]`, i.e. every ranked city with zero trees, currently 181 of
them, printed to 40. CITY_QUEUE.md itself gets this right: Hidde named a
specific 17 ("Seattle, Dallas, Houston, Cologne, Perth, Sydney, Las Vegas,
Frankfurt, Bilbao, Dubai, Kansas City, Mexico City, Vancouver, Manchester,
Taipei, Buenos Aires and Hawaii") and the file scopes "from-zero web research
is ON" to "these". The script generalised that named list into "every city
with no trees" and kept the sentence saying he named them. Running the
command today, the STAGE 1 list includes Bari, Girona, Chiang Mai, Jerusalem,
Asheville, Hamburg, Bali, Santorini, Edmonton, Turku, Winnipeg, Canberra,
Tampere, Pisa, Leipzig, Taipei, Salamanca, Hiroshima, Adelaide, San
Francisco, Luang Prabang, Oahu and Buenos Aires alongside the 17 he actually
named, all under the same "he named these cities" line.

This is exactly the failure mode CLAUDE.md's rule 1(d) exists to prevent
("From-zero web research on a city is off unless Hidde asks for that city by
name: Baarn cost 556k tokens across three passes for zero trees"), and the
tool's own most prominent output now reads as blanket permission for it. The
script does partially self-correct 30 lines later, under "WHAT YOU CAN
ACTUALLY MOVE": "Everything else on the lists above needs from-zero web
research, which is OFF unless Hidde names the city" — so a run that reads the
whole output would find the correct rule, but the STAGE 1 header and the
narrower footer directly contradict each other in one command's output, and
a run skimming for "what's next" meets the wrong one first. No run has acted
on the wider list yet: the only city work claimed or shipped this window
(Sydney, Las Vegas, Frankfurt, Perth) is inside Hidde's actual 17. Fix is
mechanical: either print only the named 17 under the "he named these" claim,
or drop that claim from the general unopened-list header and let the
"WHAT YOU CAN ACTUALLY MOVE" section carry the rule 1(d) boundary alone.

**Nothing else found at BLOCKER or WARN.** Spot-checked and clean: the
Dutch national register import (`data/registers/netherlands-lrmb.json`,
16,094 trees) carries the licence correction and Hidde's written permission
recorded in OPEN_DATA_SURVEY.md before any tree shipped; the Amsterdam,
Leiden and The Hague batches drawn from it (ams_021-029, leiden and
the-hague growth) carry `verified_sources` naming both the register entry
and the Amsterdam booklet, honest `access` lines, and no em dashes or bridge
claims; `location_precision: "approximate"` on The Hague's four register-only
trees (hag_001/002/003/005) renders the "pin approximate" chip on their tree
pages, confirmed on `koekamp-oak.html`. The paywall copy recorded in
DECISIONS.md 2026-08-18 is not live on the site (no "19.95" or price string
found anywhere in `site/dist`, per CLAUDE.md's "do not put the price on the
website until he says it goes live"). The walks-leave-the-web change
(`810c4af`) is consistent end to end: no route capsule or walk picker in the
built city pages, one "Walking routes, in the app" pill wired to `/app` with
`data-ev="walks-app"`, and `/api/walks.json` serves the same data to a future
app client rather than nothing, matching the same-day "gooi de info niet weg"
instruction. `data/city-queue.json` targets are clean, all 10/20/30, no
leftover 50s from the ladder that was killed mid-session. The nightly
cron change (`f81c294`) is exactly nine knocks (3 + 6) matching DECISIONS.md
2026-08-19's "every two hours from 18:00 to 10:00 UTC" and its six-knock
restore line is left in a comment. `Jerusalem` appearing in the unopened-city
list is not itself a violation of the 2026-08-16 "out of focus" ruling: that
ruling's own text says the queue still ranks those cities and only
`scout_next.py`'s register-scouting `--target` is gated on it; nothing reads
`out_of_focus` from `city_queue.py`. The 2026-08-18 WARN (Naples nap_018-020
missing pin provenance, Caserta cas_013/014 pin drift from the cited
register point) is unchanged this window, so it is not restated here; it
remains open rung-3 work. No new BLOCKER; REVIEW.md's WARN log otherwise
matches `health.py`'s read of it.

---

## 2026-08-18

Reviewed since the last review commit (`04097cc`, 2026-08-17 07:18 UTC): 120
commits, roughly 24 hours of night-run and session work. New: Singapore (18
trees, first cluster in the Botanic Gardens), five island city pages
(Hilo/Big Island, Tenerife, Madeira, Sardinia, Crete, Cyprus), an Islands
section on /explore (added to the nav, then correctly pulled back out of the
nav while the section itself stayed, per commits 8225a77/0b88552). Grown:
Krakow (10 to 16), Brussels (20 to 23), Caserta (10 to 14), Naples (to its
target of 20), Palermo (to 14), Vilnius (to 10), Bratislava (5 to 10 across
two passes), Graz (8 to 10), Alicante and Lyon (both closed to 10). Warsaw's
Sowinski's Linden retired (delisted dead since 2012, redirect added). New
species pages: Turner's Oak, Scots Pine. Two pages rewritten to answer the
query people actually typed (Central Park's oldest-tree question, Newton's
Apple Tree). A caught-before-shipping incident worth noting as a pass, not a
finding: a Cyprus verify pass caught WebSearch's own AI summary inventing two
measurements for an olive tree; the fabrication was discarded and never
reached `data/cities/`, and the lesson is now written into BRIEF_RESEARCH.md.
Also fixed this window: a photo-credit bug that would have published a
photographer's email address (caught before merge; verified no email string
survives anywhere in `data/cities/`). Ran `python3 scripts/qa.py` (2083
pages, clean), `python3 scripts/superlatives.py` (386 claims, no collisions)
and `python3 scripts/health.py` (rung 2 clear) against the built site.

**WARN — Three trees published in this window carry `location_precision:
"confirmed"` without the provenance documentation every sibling entry in the
same city files uses for that claim, and in two cases the published
coordinate does not match the register point cited as the source.**

`data/cities/naples.json` nap_018, nap_019 and nap_020 (published in
64f9961, "Naples reaches its target of 20") are the only three of Naples' 20
trees with no `notes` field at all. Every other entry, including the other
`confirmed` ones, states in `notes` why: typically "MASAF and Campania agree
... position to sub-metre" with both sources' coordinates quoted (nap_013,
nap_014, nap_015, nap_016). These three have no equivalent sentence anywhere
in the file, on disk, or in CURATION.md; the story text discusses girth and
height agreement between the two registers but never their coordinates.

`data/cities/caserta.json` cas_012, cas_013 and cas_014 (the Piazza
Vanvitelli trio, published in 7320e3b) show the same gap, and for two of the
three it is checkable against the cited source rather than just undocumented.
The register file the trees themselves cite, `data/registers/italy-masaf.json`
(sheet_ids 07/08/09, B963/CE/15), gives its own coordinates for all three:
07 matches the published cas_012 pin exactly (0 m). But 08 (the casuarina)
sits at 41.075528,14.332417 against the published cas_013 pin of
41.075272,14.332242, **32 metres away**, and 09 (the yew) sits at
41.07535,14.332183 against the published cas_014 pin of 41.075377,14.332408,
**19 metres away**. The pre-publish leads file (`data/leads/caserta.json`,
diff in 7320e3b) carried the MASAF coordinates unchanged right up to the
point of shipping, so the published pins were moved sometime during this
pass, not carried over from a source. Nothing in the tree's `notes`, `story`,
`CURATION.md` or any `data/research/` file says why, or names the evidence
that justified the move (an aerial check, a site description, anything
matching the project's own `PIN_NEW_EVIDENCE` pattern in
`scripts/preflight.py`). It may well be a genuine improvement, cas_014's
address even hints at one ("in the flower bed on the Via Alois side"), but as
written there is no way to tell a deliberate correction from a transcription
drift, on the one field the project has repeatedly ruled is the only one
that really matters (CLAUDE.md, "the one field that carries the product").

Why this is a WARN and not a BLOCKER: nothing here proves either pin is
actually wrong, both squares are compact (well under the distances involved),
and `scripts/preflight.py`'s `check_pin_upgrades()` doesn't catch this shape
of case because these are new trees, not upgrades of an existing recorded
pin. This is process drift against the project's own convention, not a
demonstrated broken pin. Worth a rung-3 look: either recover why cas_013 and
cas_014 moved from their cited source and write it down, or pull them back to
the register point; and add the missing `notes` sentence to nap_018-020
explaining what actually grounds "confirmed" for each.

**Nothing else found at BLOCKER or WARN.** Spot-checked and clean: the
Hawaii/Hilo import (the 12x girth unit-conversion bug and the 1.1km-grid
coordinate problem, both named in their own commit messages, are genuinely
fixed; all 5 Hilo trees are honestly `approximate`, none upgraded to
`confirmed` on grid-level coordinates); the five new island cities
(Tenerife, Madeira, Sardinia, Crete, Cyprus) for hard-rule-10 access
(no private land, honest access lines, disputed ages left as ranges rather
than sharpened); the Islands nav/page pairing (no dead link: the section
lives on /explore, reachable via the existing "Map" nav item, and is not
itself in the dropdown); the photo-credit fix (verified no email-shaped
string survives in any `data/cities/*.json` photo credit field); the
WebSearch-fabrication catch on Cyprus (the invented figures never reached a
published tree); Bali's narrow, explicitly-quoted exception to the
2026-08-15 rich-tourists rule (a place-level exception the country-level
rule itself anticipates, not a quiet reopening of a paused country); and the
day-by-day search and signup tables in DATA.md, which remain in the ruled
format. No em dashes, banned words, or bridge claims found in the reviewed
pages. REVIEW.md's 2026-08-17 BLOCKER (Milan's Archdevil hackberry) is
recorded answered in `data/review-answers.json` and `health.py` confirms it
current; spot-checked mil_019 directly and the courtyard/park distinction
now matches the comune's own source rather than an invented bridge claim.

---

## 2026-08-17

Reviewed since the last review commit (`f72c8d5`, 2026-08-16 07:02 UTC): 131
commits, roughly a day and a half of night-run and session work. New cities:
Graz (8, then 10), Bratislava (5), Toronto (4), Montreal (7), Vilnius (7),
Tallinn (4). Grown: Milan (17 to 19), Krakow (6 to 10), Lyon (9 to 10),
Alicante (9 to 10), Warsaw (dead tree retired, 5 to 7). Opened: Canada
country page, Field Maple species page. Product/infra: the funnel-tracking
beacon bug fixed (every event had read zero since launch), MapLibre and
Gabarito self-hosted off Google/unpkg, the vote/problem-report control
split apart, the night-run schedule changed from 9x60 to 6x90 minutes, two
run-health measurement bugs fixed. Yesterday's BLOCKER (Potsdam/Berlin
duplicate trees) was fixed same-day with a preventive cross-city-distance
check added to preflight.py, confirmed still passing. Ran `python3
scripts/qa.py` (1990 pages, clean) and `python3 scripts/superlatives.py`
(371 claims, no collisions) against the built site.

**BLOCKER — Milan's Archdevil hackberry (mil_019) is published on the private grounds of an inhabited residence, against hard rule 10's absolute "not somebody's home" test.** `data/cities/milan.json` mil_019, live at
`/milan/archdevil-of-villa-marietti-radice-fossati`, stands in the interior
courtyard of Villa Marietti Radice Fossati, a building the story itself
says the Comune di Milano "lent to a small community of Jesuit fathers, who
still live there today." The page's own `access` field reads: "Free to
enter through the villa's gate, but it is a lived-in community, not a
public park; the city's own guidance is to enter with the discretion due to
an inhabited place rather than to treat the gate as a tourist entrance."
The Milan FAQ repeats it: "the villa courtyard housing the Archdevil
hackberry, ... asks for quiet discretion rather than a fee since it is a
lived-in community."

Hard rule 10 draws three tests for the access half, and the story passes
two (no gate to ask past, and the access line is honest) but fails the
third outright: "Is it not somebody's home? Front gardens, courtyards of
dwellings, private houses and their grounds stay out, whatever the register
says and however fine the tree. This one does not bend, because the person
we would be sending strangers to never asked for any of it." An arcaded
inner courtyard of a villa where a religious community currently lives is a
courtyard of a dwelling in exactly the sense that sentence means, and the
entry's own copy concedes it by asking readers for "discretion" before
walking in on people's home. That the comune itself lists the tree on its
monumental-trees page does not settle the question; hard rule 10 is
explicit that ground type and a register's inclusion do not override the
home test.

The entry's own `notes` field shows this was a judgement call rather than
an oversight: an earlier pass held the tree back "only for standing alone,"
and this pass published it anyway citing the count doctrine (distance from
other trees is not grounds for exclusion), without weighing the private-
residence question at all. The fix is a run's to make: either retire the
entry (folding it to a lead, per the pattern already used for Potsdam and
Zaragoza) or, if there is real evidence visitors are routinely admitted to
this specific courtyard regardless of who lives there, restate the access
line to say so plainly rather than asking for "discretion" — the same
distinction hard rule 10 draws for the Hobart Government House oak
(view-only, publishable) versus a private garden (not).

**NOTE (Monday corpus audit) — CLAUDE.md's own description of how runs fire is stale again, the same way the paragraph it sits in was written to correct.** "How they actually fire" (the paragraph starting "corrected
2026-08-12") says: "The only trigger is nightly.yml's nine cron knocks a
day, each capped at 60 minutes." `.github/workflows/nightly.yml` now runs
six knocks a day capped at 90 minutes each (changed 2026-08-16, commit
`4e86faa`, "Six knocks of 90 minutes instead of nine of 60"; the new
schedule is also recorded in `data/run-health.json`'s `schedule_changes`
block). The paragraph's own text is about a previous instance of exactly
this failure mode: a claim about the schedule going stale while the
schedule moved on. Worth a one-line update the next time this paragraph is
touched; not gating anything, since `scripts/run_health.py` now reads the
real timeout from the workflow file directly rather than trusting this
prose.

**Nothing else found at BLOCKER or WARN.** Spot-checked and clean:
Graz's holdback of a kindergarten Paulownia and a youth-care-home tree
pair under the school-grounds rule (documented in the city's own
`question_context`); Bratislava's private-plot-boundary oak (brt_004,
correctly worded to view from the public stairway rather than stepping
onto the neighbouring private plot); the Toronto Echo Valley "shared
coordinate" trap (five register entries on one identical lat/lng, caught
and not promoted to separate pins); Montreal's cemetery trees (all
`approximate`, sourced from the city's own montroyal.montreal.ca pages,
correctly flagged single-sourced rather than treated as two-source
verified, and correctly NOT scraped as a register import given the site's
all-rights-reserved notice); Warsaw's Sowinski's Linden retirement (dead
since 1986, delisted 2012, redirect added so the old URL still resolves,
exactly the Potsdam/Zaragoza pattern); several derived-age entries (Geneva's
cedar, Krakow's columnar oak, Poznan's plane) that state their growth-rate
basis, keep the range broad and flag rather than sharpen a vague figure,
per the 2026-08-16 estimate-vs-invention rule. No em dashes, banned words,
fabricated ages, or bridge claims found in the reviewed pages. The
self-hosting changes (MapLibre, Gabarito) and the sendBeacon fix were
checked against their stated behaviour (identical bytes vendored, licences
recorded, build still constructs maps) rather than taken on the commit
message's word.

---

## 2026-08-16

Reviewed since the last review commit (`e33ef1f`, 2026-08-15 06:59 UTC): 101
commits, a full day of night-run and session work. New cities: Quebec City
(6), Poznan (6), Brno (7), Wroclaw (4), Melbourne (8, then 12), Aarhus (7),
Brisbane (8), Sorrento (4). Deepened: Potsdam (4, then 6), Bergamo (8),
Cordoba (10 to 15). Register imports for Canada, Massachusetts, Poland,
Czechia, Switzerland. Product/infra: night-run self-observability
(`run_health.py`), the travel-demand rescore and 19-city pause, a
southern-hemisphere phenology fix, a Wikipedia coordinate-lookup fix, a
focus-ring CSS fix. Ran `python3 scripts/qa.py` (1896 pages, clean) and
`python3 scripts/superlatives.py` (355 claims, no collisions) against the
built site.

**BLOCKER — Potsdam republishes two of Berlin's already-live Pfaueninsel
trees as separate entries, under different names and ids.** `data/cities/
potsdam.json` pot_005 ("The Door Oak of Pfaueninsel", 52.430667,13.122139)
and pot_006 ("The Schlosswiese Oak of Pfaueninsel", 52.431453,13.120752) sit
6-12 metres from Berlin's already-published `data/cities/berlin.json`
ber_012 ("The Tuereiche (Door Oak) of Pfaueninsel", 52.430565,13.122087) and
ber_011 ("The Great Oak of Pfaueninsel", 52.4315,13.1207). Both pairs cite
the same source (baumkunde.de/baumregister/6402 for the door-oak pair;
baumkunde.de/baumregister/2135 plus the same Berlin Naturdenkmal PDF for the
other), describe the same door cut into the same trunk, the same ~250-year
age and the same meadow below the Schloss. This is one physical tree, live
twice, under two ids, two names, two cities, two "verified_sources" lists
and (per the FAQ) two different girths/measurement dates cited independently.
A confirmed global coordinate sweep of every published city (60m radius,
cross-city only) found no other instance; this is contained to these two
pairs, not a systemic pattern.

Why it matters, named against the corpus rather than taste: it breaks the
collect mechanic PRINCIPLES.md #2 calls the retention moat (a visitor can
"collect" the same trunk twice under two ids and two names, and the two
pages disagree about which city it is in), and it is the same class of
mistake CLAUDE.md's 2026-08-05 ruling was written to stop ("match places by
distance, never by name") happening one layer up, to a live tree rather than
a research candidate. It is also self-inflicted and foreseeable: CURATION.md
2026-08-15 ("Potsdam's staged register candidates are all in Berlin, not
Potsdam") already flagged this exact Glienicke/Pfaueninsel supply as
Berlin's, not Potsdam's, and left it unshipped for exactly this reason; a
later pass shipped the Pfaueninsel pair anyway, honestly labeling them as
standing in Berlin (the FAQ says so, and that half is good practice) but
without checking them against Berlin's own already-published tree list
first. Potsdam's other four trees (pot_001-004, at Jagdschloss/Schlossgarten
Glienicke and Volkspark Klein-Glienicke) do not duplicate anything in
Berlin's file and are not implicated.

The fix is a run's to make (retire one side of each duplicate, most likely
pot_005/pot_006, since Berlin published first and Potsdam's own FAQ already
concedes these are "not actually in Potsdam"; reassign or drop the ids per
hard rule 3 on published URLs). What is missing from the toolchain, and
where a rule that fails on two different days should become a check
(CLAUDE.md's own ratchet): `scripts/superlatives.py` catches two pages
claiming the same crown; nothing catches two pages claiming the same trunk.
A cross-city proximity check (same shape as the sweep above, maybe 50m) run
in `qa.py` or as its own script would have caught this at build time.

**Nothing else found at BLOCKER or WARN.** Spot-checked and clean: Sorrento
(day-trip framing to Piano di Sorrento is honest in every location field,
matches the Cork/Fota and now-established pattern), Brisbane and the new
Australia country page (no superlative collision between Melbourne's and
Brisbane's oldest-tree estimates, checked deliberately per the commit
message and confirmed), Bergamo's unconfirmable horse-chestnut entry
(bgm_008, correctly shipped per the 2026-08-06 "a tree that cannot be
re-confirmed does not hold a city back" ruling, with the uncertainty stated
plainly and a reader asked to check), Quebec City's unattributed
"250-year-old red oak" newspaper claim (correctly left unresolved rather
than bridged onto a specific tree, per the 2026-08-13 bridge-claim rule),
and the Brno hospital-grounds tree (brq_005, satisfies all three of hard
rule 10's loosened access tests with an honest access line). All spot-
checked new trees carry 2+ sources, an honest `location_precision`, and no
fabricated ages or sizes. No em dashes, banned words or builder-speak found
in the reviewed pages.

---

## 2026-08-15

Reviewed since the last review commit (`609804b`, 2026-08-14 09:49 UTC): 80
commits, roughly a day of night-run and session work. New cities: Ferrara
(5 trees), Parma (5), Palma de Mallorca (5), Alicante (9). Cities reaching
their target: Padua (10), Trieste (10), Bucaco (10), Trento (9), Guimaraes,
Perugia (10), Cagliari (7), Braga (4). Product/UX: the search field's
zero-query state (recent/near-you/start-here), the desktop walk control
redocked as a white map-control card, an es-city sign-in modal parity fix,
Worth-the-Visit and accounts-related follow-through, and the corpus catch-up
for accounts opening (`172a1ca`) that closes both WARNs from the 2026-08-14
review. Ran `python3 scripts/qa.py` (1789 pages, clean) and
`python3 scripts/superlatives.py` (336 claims, no collisions) against the
built site.

**Nothing found at BLOCKER or WARN.** Specifically checked and clean:

- The two 2026-08-14 WARNs are properly closed, not just silenced:
  `account.astro` now correctly distinguishes saved trees (sync via account)
  from the collection/passport (still device-only, app to come), matching
  `/saved`'s copy; CLAUDE.md hard rule 1 and DECISIONS.md carry the accounts
  ruling; and `check_auth_corpus_agreement()` in `scripts/qa.py` now fails
  the build if `AUTH_ENABLED` and the rule text disagree again, which is the
  build-check ratchet this project's own learning loop calls for on a third
  recurrence.
- All four new cities: every tree carries `location_precision: confirmed`,
  2+ sources, and an honest, specific `access` line (no gates glossed over,
  paid entry stated, opening hours given). Stories are 200-225 words, no em
  dashes, no banned words, no invented ages or sizes; register figures are
  cited as the register's own measurement where a source disagrees (e.g.
  Ferrara's plane: "the register measures it; nobody has dated it.").
  Multi-trunk/ensemble entries (Braga's Three Oaks, Trees of the Embrace)
  are registered as single conjunto entries in the source register, which is
  the collectible-point test passing rather than being waived.
- Zaragoza's prison laurel (`e47bea6`) and Bergamo's hospital garden
  (`8aef04e`) are the hard rules working as designed: the best story in
  Zaragoza's register got killed on the dead-tree rule rather than shipped
  for its narrative, and Bergamo's blocked lead was re-evaluated against the
  *current* (2026-08-13-loosened) hard rule 10 standard rather than left
  citing the superseded "when in doubt, leave it out" text.
- The es-city sign-in modal gap (`b72bca9`, misleadingly titled "no
  `<main>`") was a real parity bug (the dialog markup was missing from the
  Spanish city template) and is fixed and verified present on both language
  variants in `site/dist`.

**NOTE** — Cities' split-panel layout (`[city].astro`, both `/en` and `/es`)
renders no `<main>` landmark at all; `Base.astro`'s shared shell only wraps
`<slot />` with no semantic container, by explicit design ("the split-panel
map layout has no room for the standard footer"). This predates the
reviewed window and both language variants are consistent with each other,
so it is not a regression, just worth a line: an accessibility pass would
find this if one is ever scheduled.

---

## 2026-08-14

Reviewed since the last review commit (`9e8f6f8`, 2026-08-13 09:53 UTC): a
large batch (~120 commits, roughly a day of night-run plus session work)
covering Catania opening, Como/Toulouse/Strasbourg reaching target, the
AllTrails-shaped action capsule and sign-in funnel, Worth the Visit voting,
species/country/park page gaps closing, and accounts opening. Spot-checked
the built site (`site/dist`): catania/como/toulouse/strasbourg pages, the
tree-page capsule and sign-in dialog, account.html, saved.html, index.html,
plus a site-wide sweep for em dashes, banned words and builder-speak (all
clean). Tree data for the four changed/new cities (27 trees) all carry
honest `location_precision: confirmed` and flagged, sourced hedges in the
prose (e.g. Catania's two bunya pines openly disagree with each other's
register height figures). No public vote counts render for Worth the Visit,
matching the 2026-08-14 DECISIONS.md ruling.

**WARN, FOR HIDDE** — Accounts opened in production today (`ca303c5`,
"Accounts open: the saves table SQL, cloud sync for hearts, and the one
sign-in surface", authored as a real Hidde ruling in session, "just build
it - we're continuing with this product") but CLAUDE.md's own text was not
updated in the same commit, unlike every other hard-list exception this
project has made carefully before (compare `b432ac6`, hard rule 10, which
updated CLAUDE.md and DECISIONS.md together same commit). Two places are now
stale: hard rule 1 still reads "No accounts, logins, or storage of personal
data... the one item Hidde waved off and it stayed closed anyway... A
waitlist form that posts to Hidde is fine. A user table is not" — but
`supabase/saves.sql` (added today) is exactly a user table, and sign-in is
now linked from the nav of every page. And "Where this is going" still says
the account page "stays an unlinked, noindexed prototype (AUTH_ENABLED
False) until account deletion works end-to-end: that is the gate Hidde set"
— but `/account` is now linked from the header nav on every page and the
tree-page capsule's first save opens the sign-in dialog, ahead of Hidde's
own admission in `LOG.md` that the delete loop is still unproven ("FOR
HIDDE, the last two minutes: paste supabase/saves.sql... delete your test
account afterwards to prove the whole loop"). DECISIONS.md carries no
primary entry recording the ruling itself, only two tangential 2026-08-14
entries about the AllTrails funnel that mention accounts opening in passing.
This is a real, considered exception, not a run overstepping (same shape as
the 2026-08-10 outreach-mail finding and the 2026-08-12 Porto-photo
finding, both flagged WARN/FOR HIDDE here), but it is now the third time
this exact shape has recurred: a genuine hard-list exception shipped without
CLAUDE.md's rule text or a DECISIONS.md entry updated in the same commit.
Per this project's own ratchet ("a lesson that appears on two different days
becomes a build check"), this has appeared three times and still has no
mechanism, only three individual notes.

**WARN** — `site/src/pages/account.astro:57`, the signed-in state's own
copy ("Your collected trees are saved on this device. The app brings them
to all your devices.") is now factually wrong and self-contradicting within
the site: as of the same-day `ca303c5`, saved trees for a signed-in user
sync to Supabase and follow the account across devices with no app
involved, which is the entire point of today's build ("hearts sync to the
cloud as a union whenever a session exists... /saved merges device and
account"). `site/src/pages/saved.astro:53` was correctly updated the same
day ("Signed in: these follow your account to any device."), so the two
pages now tell a signed-in visitor opposite things about the one fact that
matters most on an account page: what happens to their data. `account.astro`
was not touched by `ca303c5` at all. A visitor who signs in specifically to
stop losing their collection (the passport-loss problem PRINCIPLES.md #12
and CLAUDE.md's "Where this is going" describe) is told on the account page
itself that this still requires an app that does not exist.

---

## 2026-08-13

Reviewed the last 24 hours: Portland goes live (10 heritage trees), Hobart
goes live (7 significant trees), Singapore grows from 7 to 10, the
`preflight.py` id-prefix collision check, and the `registercheck.py`
survival-story fix. No BLOCKER, no WARN.

**NOTE** — The Portland launch (`8860db9`) is the standing example of a
near-miss caught cleanly. A write pass generated ten trees numbered
`por_001`-`por_010`, which is Porto's live prefix; merging would have
silently overwritten ten indexed Porto trees (hard rule 3). The pass refused
to merge its own output, and the same commit adds `check_id_prefixes()` to
`scripts/preflight.py`, verified against a staged collision. Checked the
live data: `ptl_*` (Portland) and `por_*` (Porto) are now distinct, both
cities intact in `data/cities/`.

**NOTE** — Spot-checked all three new/grown cities (Hobart, Portland,
Singapore) against the hard rules and the honesty rules in CLAUDE.md Step
0/2/4, plus a random sample of five older pages (Athens, Cadiz, Florence,
Krakow, Nijmegen). Clean throughout: no em dashes or banned words anywhere
in `site/dist` (checked site-wide), all titles/meta descriptions within
contract limits, every tree's `access` field respects private land (Portland
excludes the ~40% of register trees on private yards outright; `ptl_004`
explicitly tells the visitor to stay at the street corner rather than cross
onto school grounds), all photo licences on the three Singapore approved
photos carry CC BY/BY-SA plus attribution, and every missing-photo tree
renders the honest "Nobody has published a photograph of this tree under a
licence we can use" line rather than a substitute image. Two entries are
worth naming as good examples of the honesty rules actually working: the
Tiong Bahru banyan (`sgp_009`, 22.8m girth reached in "under sixty years")
is written as speed rather than age with "ancient" kept out of the copy, and
Portland's Balch Creek Fir (74.1m) claims only "nothing else in Portland
comes close" on its own page, no site-wide or regional superlative, which
checked out: it is the tallest tree actually published on the site (the
80m figure elsewhere on the site is a citation of California's General
Sherman for comparison, not one of our own trees).

**NOTE** — Singapore's rewritten intro (`e233f37`) was checked against the
tree list for accuracy rather than taken on faith: it claims five trees
cluster on Fort Canning, and the data confirms exactly five (`sgp_002`,
`sgp_003`, `sgp_004`, `sgp_005`, `sgp_010`) share that neighbourhood; the
"reachable only by boat" line matches `sgp_007` at Chek Jawa on Pulau Ubin.

---

## 2026-08-12

No review ran on 2026-08-11, so this pass covers roughly 44 hours of commits
(since 2026-08-10's second pass) rather than the usual 24: the mail-outreach
thread, the Paulo/Porto submission, the walks fixes, and this morning's
CLAUDE.md and DATA.md changes.

**WARN, FOR HIDDE** — Porto's ginkgo tree page (`/porto/ginkgo-of-the-jardim-das-virtudes`,
data in `data/cities/porto.json`, por_008, live since `7a79497`) ships a photo
whose licence field reads "Used with the photographer's written permission,
by email 2026-08-11", sourced from a third-party blog (`photos1.blogger.com`,
hotlinked directly in `<img src>`, `og:image` and the page's schema `image`).
This is not an open licence. CLAUDE.md's Step 4 is explicit and unqualified:
"Search Wikimedia Commons and other openly-licensed sources (CC0, CC-BY,
CC-BY-SA only)... NEVER use photos from monumentaltrees.com, Google Maps, or
any source without a clear open license," and hard rule 4 says "Photos must
have verified open licenses with attribution recorded" with no permission
carve-out anywhere in the corpus. `drafts/reply-paulo.md` shows this was a
real, considered call Hidde made in session ("Hidde cut it: his yes is
enough," after the run had correctly flagged the blog as unlicensed), not a
run overstepping, so this reads as the same shape as the 2026-08-10 outreach
finding: a genuine exception he made that the corpus text does not yet
reflect. Hard rule 4 sits on the closed "hard list" whose header says these
five items "stay closed no matter how well they score," so a future run
reading only CLAUDE.md would reasonably conclude this photo should never have
shipped, and would have no way to know a one-off permission grant is
different from a standing policy change (is this one photo, or does
"permission" now join the accepted licence list generally?). Flagging FOR
HIDDE rather than as a defect: either record this as a scoped exception (one
photo, one permission, not a new licence category) in DECISIONS.md, or amend
CLAUDE.md if permission-based photos are meant to be usable more broadly.

**NOTE** — On the good side, the same commit correctly enforces the adjacent,
harder-won rule: `1107a1e` ("Never publish a submitter's name") removed
`submitted_by` rendering from `[tree].astro`, the CSS credit block and the
promise-of-credit copy on `/contribute` and the no-photo caption, and swept
Paulo's name out of `porto.json`'s own `notes` field in favour of "the sender
is recorded off-site and is NOT named here." Verified: no occurrence of
"Paulo" or "Araújo" anywhere in `site/dist` (checked the whole built tree,
including `search-index.json` and both sitemaps). The photo credit correctly
points at the publication ("Dias com Arvores") rather than a person, per the
2026-08-11 ruling.

**NOTE** — Walk-name collapsing (`30c816c`) works as intended on the one live
example: Porto's two walks, one running through the area labelled "Massarelos"
and the other through "Lordelo do Ouro e Massarelos," render as "Massarelos
east" / "Massarelos west" rather than as awkward near-duplicates. The area
labels themselves (used for tree metadata, not walk names) correctly keep the
full parish name.

**NOTE** — DATA.md's digest (`bcaf696`) is already table-formatted throughout
(funnel rates, Search Console, audience, Web Analytics all render as
Markdown tables with at most two sentences of prose per block), consistent
with the same-morning CLAUDE.md instruction (`7e9af63`) to report digests in
tables rather than prose.

**NOTE** — Spot-checked five further built pages (`berlin.html`,
`collections.html`, `fukuoka.html`, `italy.html`, `munich.html`) plus a
site-wide grep for em dashes and TONE_OF_VOICE.md's banned words across all
of `site/dist`: clean. No builder-speak or rule-explaining-to-the-reader
phrasing found on the sample.

---

## 2026-08-10 (second pass, ~10:45 UTC, covering commits since this morning's review at 08:30 UTC)

This morning's BLOCKER (`ageToken()`) and WARN (nightly permissions) are both
fixed, verified in the rebuilt `site/dist` and in the corrected workflow file;
see the confirmations under each below rather than restating them as new
findings.

**WARN, FOR HIDDE** — The outreach mail system now live-sends real email under
Hidde's name at meaningful volume (batch 003, 12 mails, and batch 004, 28
mails, both today, both `data/outreach-sent.json`-logged with status
`approved_by_hidde`), and it contradicts CLAUDE.md hard rule 4 as written:
"Never speak as Hidde, never contact anyone as him. No emails... under his
name." Batch 004's own bodies open "Mein Name ist Hidde" and are dispatched by
`scripts/outreach_send.py` over SMTP once a batch's status is flipped to
`approved_by_hidde`, i.e. the session performs the send action itself, not
Hidde in his own mail client. `drafts/OUTREACH.md`'s own "De verzendmachine is
blijvend" section documents this as a deliberate 2026-08-08/09 design (a
per-batch approval word from Hidde, machine-bound credentials, a daily cap)
and the send commits are authored under the `Hidde` git identity, so this
reads like a real, considered exception he made in session rather than a run
overstepping. But the hard list is explicit that these five items "stay
closed no matter how well they score" and changing one is his call, said out
loud — and CLAUDE.md's own hard rule 4 text has not been amended, and
DECISIONS.md carries no entry recording this exception, so a run reading only
the canonical corpus (as instructed in Step 0) would reasonably conclude this
entire subsystem is forbidden. This is exactly the "test every incoming
thought against the recorded picture... the contradiction must be said out
loud" case CLAUDE.md itself describes. Flagging FOR HIDDE rather than as a
defect: either amend hard rule 4 in CLAUDE.md to state the mandate-pattern
exception (his call, hard rule 7-adjacent territory since it's editing
CLAUDE.md itself isn't gated the same way, but the hard list item is), or add
the decision to DECISIONS.md so the corpus stops contradicting the live
system. Structural note, not a mitigation of the above but relevant to blast
radius: `.github/workflows/nightly.yml` has no reference to `OUTREACH_SMTP_*`
or `outreach_send.py`, and the credentials live only in a file on Hidde's own
machine, so unattended night runs cannot trigger a send today.

**NOTE** — Confirms this morning's BLOCKER is fixed: `9e06275` rewrote
`ageToken()` to prefer a number inside the tree's own `age_min`/`age_max`
range, verified live in the rebuilt `site/dist` — `boston.html`'s title now
reads "Oldest 214 Years" (was "1772"), `boston/shaw-memorial-elms.html` reads
"214 Year Old" (was "1772"), and `rome/hackberries-of-the-aranciera.html`
reads "300 Year Old" (was "1600"), all three now inside their tree's own
data range. Also confirms this morning's WARN is fixed: `8b6fa3f` restored an
enumerated `allowedTools` list in `nightly.yml` in place of the same-day
"allow Bash, deny six things" inversion, with a stated (and correct) argument
that neither list was ever a sandbox given `Bash(python3:*)`.

**NOTE** — Swept the four new country pages (`italy.json`, `poland.json`,
`france.json`, on top of the UK one from a prior session) against their
source city data: Italy's Goethe/Padua palm claim, Poland's Henryk Oak and
Warsaw's Dąb Mieszko I details, and France's 1601 Robinier all check out
against `data/cities/*.json` verbatim, no fabrication. Confirmed reachable
from `/countries` and linked in the built site (the class of bug that left
country pages live-but-unlinked for three days on 2026-08-04), and `qa.py`
passed per the commit's own claim.

**NOTE** — Spot-checked a further sample of built pages (`lisbon.html`,
`edinburgh.html`, `dublin.html`, `kyoto.html`, `es/malaga.html`, two species
pages, one collection page) plus a site-wide grep for em dashes and the
TONE_OF_VOICE.md hard-banned words across all of `site/dist`: clean.

---

## 2026-08-10 (first pass, 08:30 UTC)

**BLOCKER** — `ageToken()` (`site/src/lib/tree-copy.ts:16-20`) extracts the
FIRST number in a tree's `age_estimate` string, and for any tree whose
sentence leads with a calendar year before stating the actual age, that
year ships live as the tree's age. Verified on the built site in three
independent places, since today's city-title change (e630a27) newly reuses
this same function for a fourth: `site/dist/boston.html`'s `<title>` reads
"Ancient Trees in Boston: 10 to See, Oldest 1772 Years"; the question page
`site/dist/boston/oldest-tree.html`'s `<title>` reads "What Is the Oldest
Tree in Boston? (1772 Years Old)"; the tree page
`site/dist/boston/shaw-memorial-elms.html`'s `<title>` reads "The Shaw
Memorial Elms: 1772 Year Old English Elm in Boston". The tree's own data
(`data/cities/boston.json`, bos_001) gives `age_min: 214, age_max: 254`
from the string "planted between 1772 and 1812, so roughly 214 to 254
years old"; the regex grabbed the planting year instead of the age. This
is not a one-off: swept every city file for the same shape (a leading
number in `age_estimate` outside the tree's own `age_min`/`age_max`
range) and it hits **75 trees across at least 30 cities**, confirmed live
on a second sample, `site/dist/rome/hackberries-of-the-aranciera.html`'s
title reads "1600 Year Old Tree in Rome" for a tree whose own data says
300-400 years and whose story explicitly states "no dendrological
confirmation", and a third,
`site/dist/naples/camphor-of-the-royal-orchard.html` reads "19 Year Old
Tree in Naples" for a tree estimated at 190-225 years (the string said
"19th century"). Direction is not consistent: some come out absurdly old
(1600, 1772, 1810, 2010), others absurdly young (7, 16, 18, 19, 20). This
is a straightforward hard-rule-2 violation ("NEVER fabricate tree facts")
at scale, live in the exact field (the title tag) most likely to be seen
and indexed, and it directly undermines today's own city-title change,
whose entire point was to put a true, specific age in front of a searcher.
Full list of affected `(city, tree_id)` pairs available by re-running the
sweep; fix is in `ageToken()` itself (prefer `age_min`/`age_max` over
parsing prose, falling back to the regex only when neither is set) rather
than editing 75 data files.

**WARN** — The nightly workflow's tool allowlist was inverted today
(commits 010598c, 1aa2f81) from an enumerated allowlist to `Bash` (all of
it) plus a five-entry `disallowedTools` denylist
(`Bash(rm:*),Bash(sudo:*),Bash(gh repo:*),Bash(gh secret:*),Bash(gh
auth:*),Bash(gh api -X DELETE:*)`). The commit's own stated rationale is
sound (the old allowlist blocked the workflow's own build step and the
prior list's security value was already undermined by `Bash(git:*)`
permitting a force-push), but the replacement denylist is a prefix match
on literal command names and does not catch the equivalent destructive
actions available through the same shell it now grants in full: `find .
-delete`, `git clean -fdx`, `git reset --hard`, `python3 -c
"import os,shutil; ..."`, or piping to `rm` via `xargs` all bypass every
one of the five denied prefixes. This is an unattended, scheduled job
that also holds `WebFetch`/`WebSearch` and therefore ingests untrusted
web content into the same context that now has near-unrestricted `Bash`,
which is exactly the shape where a prompt-injected page could turn "read
this source" into a destructive command the denylist does not name. Not
a page defect and nothing has gone wrong yet, but it is a same-day,
unreviewed widening of what an unattended process can do against hard
rule 3 ("nothing irreversible in public"), and worth Hidde's eyes rather
than assuming the five-line denylist does what its commit message claims.

**NOTE** (Malaga /es/ test, Contract J, ef110f6) — Checked thoroughly and
found clean: reciprocal hreflang on both `/malaga` and `/es/malaga` plus
`x-default`, visible "en español" link on the English page, `html
lang="es"`, canonical self-referencing, intro at 91 words (inside the
60-100 contract band), all ten stories 181-229 words (inside 150-250), no
em dashes anywhere in the eleven rendered Spanish pages, and the English
Malaga page's own title correctly picked up today's age-hook format
without the ageToken bug above (400 is both the true age and the first
number in "unos 400 años", so this city happens not to trigger it).

**Monday corpus audit** (CLAUDE.md, PRINCIPLES.md, PRODUCT_IA.md,
BACKLOG.md, GO_TO_MARKET.md, DECISIONS.md), suggestions only:

- **NOTE** — `TONE_OF_VOICE.md:2` still reads "Version 1.0 (draft, awaiting
  Hidde's approval)" while the file's own changelog records three
  subsequent approved edits, the latest "v1.3 (2026-08-04)... approved by
  Hidde in session." The header contradicts the document beneath it.
  Suggest bumping the header to "Version 1.3" and dropping "draft,
  awaiting approval."
- **NOTE** — `BACKLOG.md`'s "Country pages, Contract G: proposed
  2026-07-31, WAITS ON HIDDE'S YES" entry (line 33) is fully executed and
  stale: Contract G was approved and added to SEO_GEO_BLUEPRINT.md that
  same day (v1.5, confirmed in the blueprint's own changelog and in
  DECISIONS.md), and CLAUDE.md already describes the renderer as "live
  since 2026-08-01." No run can still act on this entry as written.
  Suggest deleting it or moving the approval to DECISIONS.md.
- **NOTE** — `BACKLOG.md`'s "Let runs read the visitor numbers" entry
  (line 186) says "A run cannot currently see Cloudflare analytics... that
  is a new secret and a new third-party dependency," with the trigger
  "measurable traffic in Cloudflare." This has already been built:
  `scripts/daily_digest.py` reads `CLOUDFLARE_ANALYTICS_TOKEN` via the
  GraphQL API today, and DATA.md's daily entry already prints the beacon
  numbers this item describes as not yet possible. Suggest removing the
  entry or marking it done with a pointer to daily_digest.py.
- **NOTE** — `CLAUDE.md`'s country-page paragraph (Step 0 rung 4) says
  "Waiting with three or more cities right now: United Kingdom, Italy,
  Spain, Poland, France, Portugal, Japan." Spain, Portugal and Japan are
  no longer waiting: all three have live country pages
  (`data/countries/{spain,portugal,japan}.json`, confirmed built at
  `site/dist/{spain,portugal,japan}.html`). The sentence is a stale
  snapshot from before those shipped, and also predates
  `data/countries/united-states.json`, which now exists too. Suggest
  refreshing the waiting list or generating it at digest time so it
  cannot go stale again.

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
