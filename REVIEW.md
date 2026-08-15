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
