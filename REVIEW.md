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
