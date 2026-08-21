# LOG

What the autonomous runs did, newest first. One entry per run that actually changed something. Hidde reads this to catch up, and says good or bad.

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-08](archive/LOG-2026-08.md)
- [2026-07](archive/LOG-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
<!-- archive-index -->

## 2026-08-21 - Night run 2026-08-21 20:31 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 0.0 minutes of its 120 minute window (wall clock: cancelled before it could report its own duration), ended clean (cut off at the cap, no result record). Nothing reached data/cities.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-21 - Night run 2026-08-21 18:44 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 0.1 minutes of its 120 minute window (wall clock: cancelled before it could report its own duration), ended clean (cut off at the cap, no result record). Nothing reached data/cities.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-21 (session) - The iOS workflow gets its first green: a crash, two wrong tests, two sturdier ones, and a layout gate that measures what it means to

The "iOS app" workflow had never once been green (`gh run list --status
success` is empty), and the two days since it was added showed only
cancelled runs and one failure with four red UI tests. Diagnosed rather than
patched, reproducing on a local iPhone SE (CI's phone) and a 17 Pro (the
phone the tests were written on). Three different causes were hiding under
one red badge:

**A real crash, from this morning.** Commit 374a838 gave the Spot sheet an
`@Environment(Account.self)` read and the `.spot` sheet case still injected
only Saved and Navigator, so selecting Spot crashed the app on every phone
(SIGTRAP in EnvironmentValues). Two tests caught it locally; CI had not run
that commit yet. The sheet now receives every environment object once, for
every case, so a view gaining a read can never crash the sheet again.

**Two tests that were wrong for a small phone.** On a 667 point SE the
"Our favourite tree cities" shelf sits below the fold of Home's lazy stack,
so it does not exist until scrolled to; `testHomeCarriesTheCollections`
asked for it without scrolling and `testPillSwapsListAndMap` used it as
proof the pill came back. Home's list face is now named `explore-home`
(the map face was already `explore-map`), the pill test judges the face,
and the shelf test scrolls. The screens were right; the tests were not.

**Two tests that were speed-sensitive on the runner.** Panning and
sheet-drag passed on both local phones and failed on the runner. The pan
now drags most of the width up to eight times and stops as soon as the chip
changes (four short drags landed right on the three kilometre threshold on
an SE's four kilometre view). The sheet test now states outright where the
sheet opened ("the search field sits at y=176 on a 667 point screen") and
judges each half on an absolute position, so the next runner failure says
something in words instead of "70.5 is not less than 43.0". And the result
bundle is uploaded as an artifact on every run, failure screenshots
included, which is what it took a local SE reproduction to replace today.

**The workflow's own time.** Most "cancelled" runs were not cancelled by
the next push: the job timeout was 30 minutes and the test step alone
takes 17 (green) to 29 (four failures retried). Timeout is 50 now;
cancel-in-progress stays, because a gate should judge the newest commit.

**The layout gate, which also blocked green: 24 findings on CI, 21 locally,
0 now.** Measured on the SE with appfit before and after, and every screen
looked at on the SE after (appsweep). Real fixes in the app: Spot's
add-path and the city walk rows are 44 point targets; the tree page's
action bar sits at the page's 20 point inset (it was 16); the fact trio is
leading-aligned so a value's width no longer decides where it starts;
LockedRow reports the row rather than its glyph; paywall bullets clear the
cards' text; the contribute kind picker is three ticked rows instead of a
34 point menu button; the primer's lines share one margin. Three changes to
the GATE, each a judgement and each written down in the script: the
navigation bar is exempt (Back, Cancel, Share are Apple's sizes, like the
tab bar already was); a sheet is measured on its own, by ancestry from a
named root, instead of together with the screen behind it (the paywall
was "drifting" from Explore's hero chip); and iOS 26's floating sheet
scales its content by 0.957, so tap sizes inside one are read back to
layout points (a 44 point close button measured 42.1). Plus one
refinement to DRIFT: content centred on the screen's centre line is
compared by its centre, not its left edge (the location primer). Thresholds
in scripts/layout_rules.py are untouched.

**And two things only the runner could teach.** The first CI run with all
of this had every real test green and still went red on two launches
that "did not have a process ID": xcodebuild had cloned the simulator and
was starting the app in two clones at once, 60 to 110 seconds per launch
on the runner. UI tests run one simulator at a time now. That in turn put
the tests and the layout sweep on ONE simulator, and a tree ticked by
`testTickingATreeKeepsIt` greeted the sweep's map as a "Seen" badge, one
finding that had not existed the run before. So the app has a `-reset`
launch argument (Saved.load() empties the collection), every test and
sweep launch carries it, and the sweep's measurements are uploaded with
the result bundle so the next oddity can be read from here.

Verified locally: full suite green on iPhone SE and iPhone 17 Pro, appfit
0 findings. CI: tests 16 passed, 0 failed and the layout gate at 0
findings on runs 32476429195 and 32478930343 (each green on the half the
other was not); run 32481289239 was the first fully green run of this
workflow (16 passed, 0 failed, 0 findings, 23 minutes), and run
32488114317 is green on the merged main, which is what went into main.
One thing to know: in that last run the walk test failed its first
attempt on the runner ("did not advance from 0 of 14") and passed on the
retry, so it is flaky on the iOS 18 simulator even from a clean start.
The retry is what made the run green; the flake is main's test and is
not diagnosed.

**Merged onto the main that moved underneath (bdcd7c8 and after).** Main
had meanwhile made Map tab 0, Explore the feed at tab 1, deleted the pill,
folded Saved into Collect, added walk mode, fixed the same Spot crash its
own way and added `-reset-collection`. So the pill test is gone with the
pill, the shelf test launches `-tab=1`, the sweep's list is main's with my
root identifiers (walk mode measured under `walk-mode`), and
`-reset-collection` is the one wipe argument; my `-reset` never shipped.
The merge's first SE run then failed two more tests, and the screenshot
explained it: the simulator was on its side. The launch tests run once per
UI configuration, landscape included, and on one shared simulator the last
orientation stays. Every test class and the sweep now start in portrait,
and the launch tests launch with the same fixed origin as everything else
so no location dialog is left on the shared simulator either. One more,
read from XCTest's own screen recording of the failure: the sheet test's
second gesture was aimed at the search field's frame a moment after the
first drag, while the sheet was still springing, and landed on the tall
photo card main now puts first, which opened the tree. Every gesture in
that test now starts from a settled frame (two reads 0.4 s apart that
agree), and no assertion message reads a frame that may be gone.

**And the test was right all along: it had found two app bugs on the SE.**
Staged diagnostics (a long press alone, then drags, frames attached) put
the first card's tappable frame at y=369.5 under a search field whose
centre is y=370. A card's photograph is drawn with .fill inside a 190
point box and `.clipped()` clips the drawing only, so every photo card was
tappable 33 points above and below its visible edges: through the lower
half of the search field above it, and into the top of the next card.
TreeCard's content shape is the visible card now and the photograph is
hidden from accessibility. Second: at full height on a 667 point phone the
sheet's top was 53 points down and its search field sat under the floating
chip row, unreachable; full now stops 124 points short of the top. Neither
shows on a 17 Pro, which is the phone the app was being looked at on.
Re-verified on the merge: both phones green, 0 findings.

**And main's new walk test had the last red.** It read "1 of 14 ticked
off" on the runner (it launched without `-reset-collection`, so a tick from
an earlier test was still there), tapped, and then waited for a label
that does NOT CONTAIN "1", which "2 of 14" never satisfies. It launches
clean now and waits for the exact next count. Read from the result bundle
the workflow now keeps, without a local reproduction.

**The runner is on Xcode 16.4, not 26.6.** The workflow's "Which Xcode"
step selects Xcode_26.6 with `|| true` and the macos-15 image does not
have it, so every CI build is against the iOS 18 SDK on an iOS 18
simulator, while this Mac builds with 26.6 on iOS 26. That is why the
runner saw a 40 point pill where this Mac saw 44, and why main's
SpeciesGlyph compiled here and not there. Left as it is for now: it is a
real second compiler, which today caught a real bug, and the fix (a
runner image that has 26.6) is a choice for a session with Hidde.

FOR HIDDE: the three gate changes above loosen what the app's layout check
sees, and your ratchet says removing a check needs you. None is removed,
but nav-bar exemption, sheet isolation and the 0.957 read-back are calls I
made to get an honest green; if you would rather the gate kept counting
Apple's Back button, say so and the line comes out.

## 2026-08-21 (session) - Munich and Vienna each gain one register tree, closing near their targets

7-day visits (visitors.py): 400 visits, 615 page views (14th 34/67, 15th
33/37, 16th 83/95, 17th 44/75, 18th 67/101, 19th 42/71, 20th 74/134, 21st
23/35). Step 0: no reader submissions (Supabase checked, 0 unprocessed of
10), health.py rung 2 clear (0 BLOCKER, 1 WARN, nothing stale). Bari's 3
verified-but-unpublished trees stay below the 4-tree floor; its 4th tree
hunt is genuinely exhausted per three prior passes (CURATION.md
2026-08-20/21), did not re-open it.

Went to `city_queue.py --next` and `data/city-queue.json` for cities
closest to target with real demand: Rome (30 target, 29 trees, 215
impressions/10d) and Munich (30 target, 29 trees, 41 impressions/10d) each
needed exactly one more tree; Vienna (30 target, 27 trees, 115
impressions/10d) needed three. Rome's remaining 4 leads.py-READY leads all
carry documented reasons they don't actually ship (day-trip boundary,
unresolved vitality, not a collectible point per CURATION.md's entry from
earlier today), so left Rome alone rather than re-litigate that. Read
Munich's and Vienna's actual leads files by hand rather than trusting
leads.py's READY count at face value (same lesson as today's earlier
Rome/Florence/Vienna entry).

Munich: 15 READY leads, all legally protected single trees on public
land per the 2021 Naturdenkmalverordnung, all missing only age. Picked the
Nymphenburg Porcelain Manufactory lime for joining the existing muc_007/
011-014 Nymphenburg cluster (about 0.7km away) and for having a real second
source, a 2011 local paper piece naming this specific tree, which the
register alone didn't give it. Shipped as `muc_034`. Munich now 30/30.

Vienna: checked all remaining leads against their own notes rather than
re-researching. Most are genuinely marginal (unconfirmed courtyard access
on a strong Prater ginkgo lead, a third plane in an already-covered park,
two young Kugeltrompetenbaum specimens). One, the Alser Strasse plane,
was explicitly noted "verifies fine" by an earlier pass and just weaker
than what got picked then; confirmed via Vienna's own Baumkataster
(documented 1894 planting date, girth 315cm) and shipped as `vie_028`.
Vienna now 28/30; updated its meta_description off a stale "Twenty-seven".

Both new trees: `curation_status: flagged` (single-source register data,
per Step 2), honest `location_precision`, no invented ages, no photo
judged (this runner's egress blocks Wikimedia image fetches; found one
CC BY-SA candidate for the Munich tree via the API and left it
`found_needs_check` for a session that can view it). Ran preflight.py
(clean), `npm --prefix site ci && npm --prefix site run build` (clean),
qa.py (one pre-existing sitemap lastmod warning from this sandbox's
shallow git clone, unrelated to this change), `route_walks.py` (both
routes walk clean, 2.0km/24-25min), `tree_index.py`, logged to
data/agent-costs.json. Full detail in CURATION.md. Released both claims.

## 2026-08-21 (session, with Hidde) - The contributor reply loop: input is core, gets thanked, answered, never dismissed

Hidde's ruling, designed and built in one session: "this process of user giving input is one of the core features of our platform and must be treated with care." Spec in docs/superpowers/specs/2026-08-21-contributor-reply-design.md, plan beside it. What shipped:

- **Feedback follows the account convention, revised the same day after Hidde asked for the competitor check.** Google Maps, AllTrails, Waze and Apple Maps all gate contribution behind the account, so we do too: every control is visible to everyone, the first act while signed out opens the one sign-in surface, posts carry the user's token so rows arrive with `user_id`, and no one types an email anywhere (the reply script resolves the address from the account at send time). Privacy requests stay ungated. The web form keeps a typed draft across the magic-link round trip, got the double-submit fix (the Toulouse correction of 08-20 arrived as three identical rows), and its name-field hint stopped claiming "so we can write back", which was never true. qa.py now refuses a page with gated controls and no sign-in dialog.
- **Two mail kinds, standing approval given in session**: an automatic thank-you in Hidde's own words within a couple of hours, then the run-composed answer with three outcomes (changed / holds / open question). A "holds" always ends in a question back, never a dismissal; Prague's wrong-location report is the worked example of what we used to file silently. Transport is scripts/contributor_reply.py with the outreach guardrails (dry-run default, do-not-contact beats everything, daily cap, mailcheck gates every answer); wired into data-digest.yml and nightly.yml. Runs compose reply_text per Step 0b's new "Closing the loop" section.
- **The worth-it thumbs are toggle buttons now, on both surfaces**: press selects, press again undoes (a compensating "vote undone" row, netted out everywhere), the other thumb switches, and a down-vote unfolds the why-chips as an optional follow-up (app-store convention; knowingly amends the 2026-08-16 split, whose core survives). The app had no vote control at all; it was born with this design on the tree page.
- **Privacy page states the email facts** and stops saying a submitter's name is kept "for credit". The both-surfaces rule (Hidde, same day) is recorded in CLAUDE.md beside the other design checks.

**FOR HIDDE, two pastes and the loop is live:**
1. Supabase SQL editor: run `supabase/contributor-reply.sql` (adds user_id/outcome/reply columns to submissions; user_id stamps itself from the signed-in sender). Until then signed-in submissions still land, just without the reply columns.
2. GitHub repo settings, Actions secrets: add `OUTREACH_SMTP_HOST`, `OUTREACH_SMTP_PORT`, `OUTREACH_SMTP_USER`, `OUTREACH_SMTP_PASS`, `OUTREACH_FROM`. Until then the CI step prints a dry run and sends nothing.

Both done by Hidde the same morning; a manual digest run then executed the reply step with the real secrets and reported "nothing waiting", so the loop is live. `OUTREACH_FROM` in CI is `Ancient Trees <burgmans.hidde@gmail.com>`, deliberately not the "Hidde, Ancient Trees" of his outreach letters: the machine sends these unread, so they speak as the product (hard rule 4).

**FOR HIDDE, optional, whenever:** recipients can still see the Gmail address behind the sender name, because Gmail only sends from the account that logs in or a verified alias. The clean route is an address on the domain (`hello@ancienttrees.app` as a Workspace mailbox or a registrar forwarding alias), verified in Gmail under "Send mail as", then `OUTREACH_FROM` changes to it. He agreed it is the right move; nothing blocks on it. **Tried 2026-08-21 and parked:** Gmail's "Add another email address" popup returned "Temporary error (405)" twice, once in the wrong account and once in the right one. Next attempt: first make the TransIP forward (hello@ancienttrees.app to his Gmail), then retry in an incognito window (AdBlock Plus off) with SMTP smtp.gmail.com / 587 / burgmans.hidde@gmail.com / the app password. Until then the mails go out as "Ancient Trees" from his Gmail, which works.

## 2026-08-21 - Night run 2026-08-21 06:21 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 20.2 minutes of its 120 minute window, 140 turns, 35 commands refused by the allowlist, ended clean (success). 6 commit(s), none of them a published tree. Claims left behind: seville, caserta, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-21 - Night run 2026-08-21 04:25 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 25.7 minutes of its 120 minute window, 198 turns, 42 commands refused by the allowlist, ended clean (success). 5 commit(s), none of them a published tree. Claims left behind: oahu, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-21 - Night run 2026-08-21 02:52 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 15.3 minutes of its 120 minute window, 143 turns, 43 commands refused by the allowlist, ended clean (success). 4 commit(s), none of them a published tree. Claims left behind: krakow, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-21 (night run) - Milan +2, Brussels +4 from the shelf; Bari's 4th tree still missing; a passcheck bug fixed

`python3 scripts/visitors.py`: 378 visits, 581 page views over 7 days (14th 34, 15th 33, 16th 83, 17th 44, 18th 67, 19th 42, 20th 74, 21st 1 partial). Flat, no city dominating. `prepare.py`: 40 cities staged for verify, Bari's 3 written trees still awaiting a 4th to clear the floor.

**Rung 2 (health):** clear, 0 BLOCKER/WARN.

**Bari's 4th tree, checked and still not found.** The three remaining day-trip register candidates in Molfetta (an isolated eucalyptus, an oak beside a walled private ruin, a carob near a private-house hamlet) all failed hard rule 10 on the evidence available (OSM proximity, on-site reportage). That exhausts Puglia's regional register for Bari; it stays at 3 trees, below the 4-tree floor, until a reader submission or a from-zero sweep turns up a 4th. Full detail in CURATION.md.

**leads.py's READY count checked before trusting it for Rome, Florence and Vienna, and none were genuinely ready** (each carries its own explanation for being skipped that just doesn't match `data/block-reasons.json`'s patterns: day-trip boundary, unresolved vitality, a planted grove, missing second source). Vienna's count also had a real bug: entries already noted "delivered TO ...verified.json" (not "delivered AS") slipped past the DONE regex. Fixed in `scripts/leads.py`.

**Milan (19 to 21) and Brussels (26 to 30) did have genuinely ready material**, once checked by hand: 2 single-sourced MASAF planes in Milan, and the Parc d'Egmont pyramidal holly plus 3 trees a 2019 survey added to that park in Brussels. Dispatched to a write-stories pass, merged, count-promising text fixed, preflight and Astro build clean.

**Lyon verify pass: zero new trees**, but its one live candidate (the Anne Frank chestnut) turned out to already be published as lyo_012, exposing a real passcheck.py bug: the Wikidata section trusted a one-time 2026-08-09 harvest flag with no re-check against what has published since. Fixed to filter by live-coordinate proximity like register candidates already do.

**Also:** `superlatives.py` false-positive fixed (two London Plane pages sharing ordinary species trivia about the hybrid's 17th-century origin were flagged as a crown collision). `photo_hunt.py --recheck` swept 40 more trees for a future viewing session. 5 free `famous_trees.py` country sweeps (Argentina, Taiwan, Brazil, Colombia, Indonesia) for cities on the queue with no register yet.

## 2026-08-20 - Night run 2026-08-20 22:33 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 22.3 minutes of its 120 minute window, 163 turns, 38 commands refused by the allowlist, ended clean (success). 3 commit(s), none of them a published tree. Claims left behind: munich, utrecht, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-20 - Night run 2026-08-20 20:34 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 0.0 minutes of its 120 minute window, 1 turns, ended clean (success). Nothing reached data/cities.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-20 (session) - Toulouse submission checked, four Dutch cities deepened, a species page gap closed

`python3 scripts/visitors.py`: 383 visits, 609 page views over 7 days (13th 17, 14th 34, 15th 33, 16th 83, 17th 44, 18th 67, 19th 42, 20th 63), flat, no single city dominating.

**Reader submission (rung 1):** three duplicate rows (a form double-submit) from a reader named Katy questioned tls_002's Wych Elm identification (hairless leaves, atypical shape) and noted two elms stand a few metres apart at the spot. Re-checked Toulouse's own open-data API directly: it still returns Ulmus glabra at the exact coordinate and is the only tree in the area flagged remarkable by the city, among 14 nearby elms including an unflagged Ulmus laevis 15m away that better matches the reader's description (smoother leaves). Left the species as the register states it, added a verify_notes entry and one story sentence so a future visitor trusts the pin over the nearest elm, logged in CURATION.md. All 3 rows marked processed.

**Species page gap closed:** Lombardy Poplar (3 trees: Amsterdam, Seattle, Portland), hand-written intro grounded in each tree's own facts.

**Four register-backed verify passes off the shelf, all dispatched to the `verify` agent and merged in-session:**
- Lyon 12 to 13 (Square Gabrielle Dupond-Ebrard cedar, joins the Point du Jour cluster; 7 more candidates left as leads, mostly single-source or private-garden)
- Groningen 16 to 19 (Poortershoes plane predating its 1881 building by 35 years, an ANWB linden with a flagged arithmetic error in its own commemorative date, a 1937 royal-wedding lime)
- Utrecht 16 to 18 (the Markiezeneik of Amelisweerd, 2022 Dutch Tree of the Year and the named protest symbol against an A27 widening the Raad van State cancelled in March 2026; the thickest plane in the Zocherpark bastion chain, 629cm)
- Rotterdam, Haarlem and Maastricht dispatched and still running at time of writing.

Fixed a real stale-count bug caught by preflight.py in both Groningen and Utrecht: meta_description, question_meta and one FAQ answer still promised the pre-deepen tree count.

Build, preflight and QA all clean after every merge. Costs logged to data/agent-costs.json.
## 2026-08-21 (session) - The bar moves again, and Begin actually walks with you

Two pieces, both Hidde's call, both live.

**The bar is Map, Explore, Spot, Collect, Profile** (DECISIONS.md, top). His diagnosis of yesterday's build: Saved was a second empty room next to Collect, while the feed we already had is the thing that works. So the pill is gone, the map and the shelves are two tabs (Komoot's split), and want-and-had are two segments inside Collect. Day zero now opens on two full screens instead of two promises.

**Begin is a mode rather than a handoff.** It used to open Apple Maps and our part of the afternoon was over. Now it is a full-screen map with the route drawn, the walk's progress on top, and the next tree as a card: within 120 m the loud button is "I am standing before it", further away it is "Take me there", and ticking always works because GPS is a bonus and never a gate. Progress is `Saved.isVisited` rather than a new store, so a walk survives a kill, syncs to the account and cannot drift from the collection. Web keeps its static walk page; Begin stays app-only, which is the honest answer to the both-surfaces rule.

**Three real bugs the tests caught**, worth knowing because each is a class rather than a one-off: the Spot sheet TRAPPED at launch after another session put its send path behind an account and nobody handed that sheet the account; the map sheet still led with whatever tree was nearest, photograph or not (`Editorial.leadWithAPhotograph` now sits in front of it); and a container `accessibilityIdentifier` on the walk screen stamped itself onto every button inside it, which is the same trap a card once played on its heart button. A `-reset-collection` launch argument makes the day-zero test independent of what other tests ticked.

New launch arguments for the sweep: `-begin=<city>|<walk>`, `-reset-collection`. Both sweep lists know the new screens.

## 2026-08-20 (session, evening) - The app is rebuilt on the five-slot bar, and it stands on white

Hidde's verdict on the first app build ("conceptueel gaat het niet goed", the features "moeten verder worden uitgedacht") became a decided structure (DECISIONS.md, top entry) and this rebuild, executed against docs/superpowers/plans/2026-08-20-app-five-slot-rebuild.md:

- **The bar**: Explore, Saved, Spot (a centre BUTTON presenting a sheet, the Strava/Untappd pattern), Collect, Profile. Home and the map became two faces of Explore behind AllTrails' floating pill; the separate Map tab is gone.
- **Nothing opens empty**, his explicit requirement for the middle three: Saved's day zero is suggestions with live hearts (Editorial.suggestions, photo-first, nearest-first, unit-tested), Collect's day zero is a mission naming one real tree with one green action, and Spot always shows both outcomes (tick what we map within 400 m; add what we miss, through the site's own submissions channel, kind "tree", GPS riding along).
- **Two of his corrections landed where they act**: the ground is WHITE and the muted surfaces neutral (Style.swift records his words; no app stands on cream) and the bar wears conventional glyphs (magnifier, heart, plus-circle, rosette, person) instead of invented ones.
- **The findings list he confirmed is worked through**: no literal tab-label headings, the tree page's name renders once, the tab bar hides on pushed pages, one search prompt everywhere, and `scripts/appcopy.py` now greps the app's string literals for em dashes, banned words, builder-speak and forever-promises the way qa.py guards the site (it caught the "licence we can use" hero line; that copy is now "No photograph of this tree yet.").
- **Coordination**: two other sessions were live in this checkout tonight; work was split by file over cross-session messages, their hit-target and image-width fixes landed separately (abc7937, 0e90238), no collisions.

Not built, deliberately: walk Begin-mode (next plan), photo capture in Spot (needs Hidde's storage yes), walk/place hearts in Saved (schema change). Launch args for screenshots: -map, -spot, tabs renumbered 0/1/3/4.

## 2026-08-20 (session) - The two DRIFT findings left on /cities are the check misreading itself, not the page

Diagnosed, deliberately not fixed, because another run is mid-calibration on this check and I cannot run headless Chrome in this worktree to prove a fix.

The smoke test has been red since b9b7777 added DRIFT. 4ad2262 fixed most of it and was right to: `.cindex-grid` now carries `margin-left: -0.45rem` so a card's TEXT lands on the same line as the country heading above it. Look at /cities and it is correct.

The two findings that survive are the check measuring the wrong edge. `.cindex-grid` paints nothing, no background and no border, so by the rule 4ad2262 itself wrote down it should contribute its TEXT edge. It contributes its BOX edge instead: `rowish()` in scripts/smoke_test.py treats any multi-column grid as a stopping point, so the walk never reaches the cards and `contentLeft()` returns the container's own left, which the negative margin has pulled 7.2px out. That 7.2 is the 0.45rem, which is why both findings report exactly it.

The narrow fix is to let a non-painting rowish container hand back the leftmost text edge of its children rather than its own content edge; the walk already takes the minimum, so recursing would give the first card's text edge, which is the number the headings agree with. Whoever holds this check should make that call, not me.

Until then `health.py` rung 2 reads red on a site that is not broken, so a run should check this entry before spending a window on it.

## 2026-08-20 (session) - Three funnel events were counted twice; the old numbers are inflated

`app-cta`, `directions` and `walks-app` each had two click listeners claiming them, so one click inserted two rows in the events table. Every figure for those three in DATA.md before today is roughly double the truth, and `app-cta` was worse than doubled because it also fired on the two links tagged `walks-app`, which point at /app. **When the counts drop tomorrow, that is the fix, not a regression.** DATA.md now says so at the top, in the preamble the digest rewrites each day, so the warning cannot be pushed off the page by newer entries.

What changed: the href-matching listener in Base.astro now tracks only `directions`, which is the one event with no attribute to hang off; everything else is counted once by the single attribute listener, which is the documented mechanism (FUNNELS.md, 2026-08-14). The `at.track` calls duplicating it in AppModal and the tree actions are gone. The footer's "The app" link was counted only through the branch that was removed, so it now carries the attribute and keeps counting.

Per the ratchet, this ships with a check: `check_one_owner_per_event()` in scripts/qa.py fails the build if an event name is both an attribute and a hardcoded `at.track()` call. Verified by reintroducing the bug and watching it fail. It cannot catch a listener matching on something other than the event name, which is exactly the href branch, so that branch is now deliberately down to one event.

Not verified in a browser: no Node in this worktree, so the source-level qa checks were run by hand (all clean) and the build itself is CI's.

## 2026-08-20 - Night run 2026-08-20 10:16 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 19.3 minutes of its 120 minute window, 133 turns, 31 commands refused by the allowlist, ended clean (success). 3 commit(s), none of them a published tree. Claims left behind: vienna, munich, utrecht, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-20 (session) - Geneva, Utrecht and Groningen deepen; a real stale-count bug fixed across 8 cities; two register scouts closed

New session. `python3 scripts/visitors.py`: 351 visits, 536 page views over the last 7 days. Step 0: `health.py` rung 2 clear. Supabase submissions checked (6 rows, all already processed). Nothing published found wrong beyond what's fixed below.

**Bari stays at 3, closed out rather than re-opened.** The prior commit named the La Grave carob grove (Polignano a Mare) and the Terlizzi/Sovereto pine as the remaining day-trip candidates for a 4th tree. Checked both: the carob grove reads as private agricultural land with no source confirming public visibility from the nearby road, and the Sovereto pine can't be confirmed alive given two independent 2025 local reports of fallen century-old trees in that exact area. Recorded both as blocked in `data/leads/bari.json` with a pointer at Molfetta's unchecked candidates for whoever picks this up next.

**Two page gaps closed:** wrote hand intros for Hornbeam and Hungarian Oak species pages (`pagegaps.py` now reports zero missing).

**Three register-backed deepen passes, dispatched to the `verify` agent and merged in-session with hand-written stories:** Geneva 18 to 21 (three SITG-register cedars), Utrecht 9 to 16 (Wilhelminapark and the Servaasbolwerk/Zonnenburg/Lepelenburg bastion-park chain), Groningen 10 to 16 (Oude Hortus and Nieuwe Kerkhof/Noorderplantsoen). One Groningen candidate caught a search-summary fabrication trap (a "oldest ginkgo in the Netherlands" claim that actually belongs to Utrecht's ginkgo, not Groningen's) and was dropped rather than shipped. Fixed 3 hard-rule-9 species naming collisions the build caught along the way.

**Found and fixed a real gap in the stale-tree-count check** (`count-promises.ts`, mirrored in `preflight.py`): it never covered the "N verified locations" meta_description closer or a bare "all N."/"full N." FAQ ending, only patterns followed by a noun like "trees". Widened both, narrowly (anchored on "Yes," for the "all N" case so Frankfurt's genuine "station for all four [of six]" subset reference doesn't false-positive). Running the widened check surfaced 8 real, live stale counts, not just today's own growth: Athens, Bratislava, Dublin, Haarlem and Maastricht were carrying stale question_meta or FAQ text from earlier growth that nothing had caught until now. Fixed all 8; Bratislava's FAQ had never mentioned its 6th tree at all (a separate Bratislava Forest Park specimen 3km from the other five).

**Two register scouting targets closed** (`scout_next.py --target`): South Korea (Seoul #33) has a promising CHA heritage-spatial API but the licence badge couldn't be read by this sandbox's WebFetch, stalled for a session with real browser rendering. Houston (#36, one of Hidde's 17 named cities) has a real, working Texas Big Tree Registry API but it's non-commercial licensed, so verification-lead-only like Nevada's; the Harris County yield itself is thin (18 rows, one real live oak) and caught a register data fault (4 rows tagged Harris County actually sit in the Texas Panhandle, 800km off).

**Two more register-backed verify passes dispatched and still running at time of writing:** Krakow (16 to a 30 target, Poland's national pomniki przyrody register) and Rotterdam (9 to a 20 target, the same Dutch LRMB register that fed today's other three Dutch cities). Will merge and report next entry.

Build clean throughout (last full build 1993 pages), qa.py clean (one pre-existing sitemap-lastmod warning from this sandbox's shallow checkout), superlatives.py clean bar one benign shared species-history phrase on two different London planes.

FOR HIDDE: nothing blocks. Noticed you're live in a concurrent session on the iOS app while this was running (pulled and rebased around your pushes cleanly, no conflicts).

## 2026-08-20 (session) - Portland doubles to twenty, and a build check that was crying wolf

Hidde noticed the US is now our largest audience and asked which American
cities are worth doing. Our own Search Console agrees with him and more
strongly than he put it: usa 36 clicks on 2,085 impressions, against gbr 16 on
1,207 and nld 18 on 472. So the question was measured rather than guessed, and
three of the four routes turned out closed. Those verdicts are in
data/register-scouting.json; the short version is that there is no index
shortcut for US cities and the route is per city.

**The answer was not a new city. It was Portland**, which had 389 unmined
heritage trees sitting in a register imported a week ago, licence already
cleared, private-yard filter already applied on import, and 30 measured
impressions. The cheapest ten trees available anywhere on the site.

Chosen as a cluster rather than by size. Seven of the ten sit inside 600 metres
in Irvington and now make a second loop of about 1.5 km: nine Caucasian
wingnuts along two blocks of NE Knott Street, a pair of London planes and a 35
metre elm on NE 18th, a horse chestnut, a pair of catalpas and a sycamore. The
other three stand alone and earn it: the Mount Tabor sequoia at 42 metres
beside the reservoir, a seven metre beech closing the end of a Parkrose street
where the tarmac ran out, and a Lombardy poplar of 9.75 metres, which is close
to absurd for a species usually rotten at fifty.

Units were checked rather than trusted, since the service labels none: 122
inches of diameter times pi gives exactly the 32 feet recorded, so the register
is internally consistent.

**Two checks fired, one rightly and one wrongly, and both are worth reading.**

The build refused `Smoothleaf Elm` for Ulmus minor because Paris already
publishes it as Field Elm. That is hard rule 9 working exactly as designed: I
had carried the register's wording straight through.

The smoke test then failed on /explore, and that one was crying wolf. Measured
in a real browser at 375px rather than guessed: MapLibre's canvas is 400 wide
inside a .map container of 375 carrying overflow:hidden, so it is clipped, the
page scrollWidth is exactly 375 and nothing is off the screen. `inScroller()`
only looked for overflow-x auto or scroll and did not count hidden or clip as
containment. Ten more trees changed how fast the map settles, which is all it
took to expose a latent false positive. Fixed, and the fix does not weaken the
check: an ancestor that clips really does clip, and if it is itself too wide
the loop catches it on its own turn.

**Still on the list from that conversation:** the pins on Boston, New York and
Washington DC, which are our three most-served US pages and carry 9 of 10, 12
of 20 and 12 of 14 approximate pins between them. And New Orleans, where the
Live Oak Society has 249 registered live oaks in City Park alone.

## 2026-08-20 (session) - Austin and Houston open, nine trees, from two Texas registers

Both live, build and smoke test green, pages checked in the browser.

**Austin, five trees**, and the source that made it possible was a register
nobody here had found: Famous Trees of Texas, 103 trees with a written history
each, sitting behind an ArcGIS dashboard the Forest Service does not advertise.
Six of Austin's ten sit within 2.3 km of the centre, so the page has a real
walk rather than a list.

| tree | why |
|---|---|
| Treaty Oak | poisoned in 1989 with enough Velpar to kill a hundred trees; two thirds died, the rest set acorns again in 1997 |
| Auction Oaks | 217 lots sold beneath them in 1839, paying for the buildings of a new capital, then decades as a parking lot with asphalt to the trunk |
| Battle Oaks | on the university's original forty acres, argued out of the Biology building's ground plan in 1923 by a professor of Classics |
| Old Baldy | a Franciscan wrote about it in 1716; Texas Parks and Wildlife calls it the oldest bald cypress on public land in the state |
| Seiders Oaks | Gideon White died fighting from behind one of these trunks in 1842 |

**Houston, four trees, and the page says out loud that they are drives.** The
two registry trees nearest downtown both stand on private land and the registry
withholds their positions, so central Houston has nothing of this order on
ground the public can reach. Saying that is better than faking a walk. What it
does have: a live oak on a church lawn in Spring Branch with a 40 metre crown
on a 625 cm trunk; the pecan at Sugar Land with a footpath named after it; the
Kissing Tree at Klein, last trace of the 1848 Strack settlement, which a Circle
K forecourt nearly took until Klein Oaks High School students wrote letters;
and the state champion winged elm on the Spring Creek Greenway.

**Dallas gained nothing published, on purpose.** It already carries the post oak
at Glover Cemetery, and the one remaining close candidate reverse-geocodes to a
house number on Roberts Avenue with a park and a cemetery both 250 metres off.
Choosing the nearer park would be the exact bridge claim that put Baarn's pin
sixty metres wrong. It stays a lead with the reasoning written down.

**Two register faults found and recorded.** The Big Tree Registry publishes
INCHES, which this morning's pass read as centimetres and used to write Texas
off as thin. And its `PublicOrPrivate` flag, called undocumented, decodes
cleanly from the data: flag 1 is national parks, forests and TxDOT, flag 0 is
ranches and hunting clubs. Nineteen leads moved to blocked on that alone.
Famous Trees of Texas has a third fault worth carrying: 17 of its 103 trees are
dead or removed, and the only place that says so is the prose of each entry.
Austin's own Washington Elm, Memorial Pecan and Governor Hogg pecans are all in
it and all gone, which the city page now tells the reader.

## 2026-08-20 (session) - Texas was written off this morning over a unit error, and it holds three cities

A scouting pass earlier today found the Texas Big Tree Registry's backend,
looped all 352 species by hand to answer one question about Houston, kept the
18 Harris County rows, threw the rest away and concluded the yield was thin
because most trees measured "70-150cm". They are 70 to 150 INCHES.

The raw data settles it without needing a source. The standout live oak carries
`Spread: 131`, and 131 feet is a forty metre crown on a live oak while 131
metres is impossible. So that tree is 6.25 metres round rather than 2.46, and a
whole county was misjudged by a factor of 2.54. It is the ICNF trap pointing the
other way, the second time a unit has done this to us, and the conversion now
lives in code instead of in a reading.

**`scripts/texas_big_trees.py`** sweeps the state once (660 trees, kept) and
reads it per city with the distance filter and the inch conversion built in, so
nobody loops 352 species by hand again. `CountyName` still cannot be trusted:
rows tagged Harris carry Panhandle coordinates 800 km away.

**Then a second correction, and this one cut the supply rather than raising it.**
`PublicOrPrivate` was recorded as an undocumented flag. The data documents it:
flag 1 is Big Bend and Guadalupe Mountains National Parks, Sam Houston National
Forest, state natural areas and TxDOT; flag 0 is Big Tree Ranch, X-Arrow Ranch
and Little Sandy Hunting & Fishing Club. The registry also sets `Display: 0` on
almost all of the latter, so it withholds those locations from its own public
map and their coordinates only reached us because the backend returns what the
front end hides. Hard rule 10 is absolute about not undoing that, so 19 of the
33 leads moved straight to blocked rather than waiting for an access check
somebody might pass later.

**What is banked, on public ground, with the owner named on every entry:**

| city | rank | ready to verify | the owners |
|---|---|---|---|
| Austin | 182 | 4, exactly the floor | City of Austin PARD (the 4.29 m bastard oak, 700 m from the centre), UT Austin, Sunset Valley, Pflugerville |
| Houston | 36 | 4 | John Knox Presbyterian Church holds the 6.25 m live oak, then Harris County Precinct 4, City of Sugar Land, and an HOA still to check |
| Dallas | 204 | 8 to deepen with | already live at 8; Grapevine and Coppell are really Fort Worth's |

A churchyard and a university campus are both explicit yeses under hard rule 10,
so Houston and Austin can each reach four on public ground.

**What is left is a verify pass and nothing more:** a second independent source
per tree, a check that it is alive, and an honest access line. The coordinates
come from the registry and are probably sound. Claims are released, so a night
run can take this straight off the shelf.

## 2026-08-20 (session) - The night runs were handing back an hour and three quarters, and now they do not

The runs were not being killed. That was the whole finding, and it took
reading `gh run view --log` to see it: every run that shipped no trees ended
with `is_error: false`, `subtype: success`, after 47 to 122 turns, having
committed a claim and stopped. No usage limit, no error, no timeout. The
window is two hours (`timeout-minutes: 120`) and the short ones were using
five minutes of it.

Measured over the 34 runs since 15 August:

| | runs | duur | beurten | bomen | weigeringen per beurt |
|---|---|---|---|---|---|
| kort (<12 min) | 18 | 3,4 min | 32 | 2,0 | 0,06 |
| lang (>=12 min) | 14 | 27,1 min | 162 | 4,6 | 0,08 |

The denials were where this started and they are not the cause: near
identical per turn, a constant tax rather than a doctor's note. What does
correlate almost perfectly is claims left standing. Every zero-tree run left
some; every run that shipped well left none. And they cascade: the 04:28 run
left `bari, taormina, catania`, and the 05:55 run inherited all three, added
`aarhus` and `sorrento`, and died too.

**What was built.** A probe after the agent step judges whether the window is
worth another go, and one continuation step finishes it. Never a loop, since
the step exists once, so the worst case is two attempts inside a window that
was already paid for. A run that died on the usage limit does not qualify,
because a second attempt would die in seconds for the same reason. Replayed
over those 34 runs it fires 8 times and skips all 7 of the one-turn deaths.

The prompt has said "do not stop after one item" since 13 August, and this
file's own workflow carried a note from 15 August about four runs in a row
doing exactly this. Said twice, ignored twice, which is where this project
stops writing and starts building.

**Three smaller things found on the way.**

- `git pull --rebase` refused to run on three of the last twelve runs,
  because the agent left unstaged files behind. It survived only because the
  remote had not moved; the moment it has, the push is rejected and the
  run-health record and the claim release vanish silently. `--autostash`.
- The meter would have reported only the second half of a two-attempt window,
  understating it by exactly what the continuation recovers. It now adds the
  halves and records `attempts`.
- `passcheck` could not list open claims at all, so the continuation prompt
  referenced a flag that did not exist. `--claims` is real now. And a
  night-run claim expired after 90 minutes on the strength of a docstring
  saying the job is killed at 60, while the cap has been 120 since c61b64c,
  so a city could be freed out from under a run still working on it. The
  expiry is now read from the workflow instead of remembered, which is the
  third file to learn that particular lesson.

Also: `passcheck --claim` now refuses a fourth open claim. One run claimed
eight cities in twelve minutes and published nothing; another claimed
fourteen on 13 August. The instruction to claim only what the window can
finish had been written twice and ignored twice.

None of this is proven yet. The next cron knock is the test, and if a
continuation fires it will show up as `attempts: 2` in `data/run-health.json`.

## 2026-08-20 (session) - 9 Dutch/Belgian cities deepened, 39 trees, from a fresh national register import

`visitors.py`: 349 visits, 534 page views over the last 7 days (13-20 Aug),
climbing from 17 to a mid-week peak of 83 (16th) and settling around 40-70
since. `prepare.py`'s shelf held 40 cities staged for verify and 3 verified-
but-unwritten Bari trees; Step 0 found no submissions (all 6 processed rows
already resolved), health clear (rung 2), nothing published wrong.

Checked Bari (top of the staged shelf) first: genuinely register-exhausted,
only 4 monumental trees exist in the whole city and two are already
correctly blocked on access, leaving 3 stuck one short of the 4-tree floor
with from-zero research off. Checked the READY leads.py output for Rome,
Florence, Milan and Vienna by hand next, since those rank far higher than
anything eventually worked: all turned out stale or already-caveated by
earlier passes (a duplicate register id, a duplicate of an already-published
tree, unresolved single-source and size-discrepancy flags already recorded
in their own notes). None of that shipped.

Pivoted to the Netherlands' national LRMB register
(`data/registers/netherlands-lrmb.json`, imported 2026-08-18, licensed CC-BY
with Hidde's own written permission), working down `city_queue.py`'s rank
order among Dutch cities: **Arnhem 4→9, Utrecht 5→9, Groningen 5→10, Haarlem
4→9, Maastricht 5→10, Rotterdam 5→9, Nijmegen 5→8**, then **The Hague 16→21**
(rank 24, its own pre-staged shelf already fully consumed, so this one
required mining the raw register by hand), then **Brussels 23→26** (rank 20,
Belgium's own official register, no address text at all, general locations
worked out via OpenStreetMap reverse geocoding and shipped honestly at
`approximate` precision). 39 trees total, all `curation_status: flagged`
(single official-register source per tree, as the rules allow), checked
individually against the Dutch register's own `dead_entries_regex` for
felled/removed language in the free-text history field.

**Four real traps caught and NOT shipped, worth naming because each would
have been a quiet factual error**: a Bari register "candidate" that was a
duplicate id for an already-published tree; a Vienna plane at the exact
coordinates of an already-published tree (leads.py had not flagged it
DONE); a Rotterdam memorial yew whose register text claims a connection to
Zadkine's famous "De Verwoeste Stad" statue, which independent search
places at a different square entirely, so the claim was dropped rather than
repeated; and a Nijmegen "Wilhelmina linde" whose independently-documented
history says the original coronation tree was replaced at an unrecorded
date, with the register's own planting band predating the coronation it
supposedly marks. Also skipped a felled-in-2000 Arnhem beech (caught by the
regex), a diseased-and-dying Utrecht elm a news article couldn't be ruled
out from, and several cemetery/avenue register entries whose `n_trees`
counts (12 to 325) marked them as mass plantings rather than collectible
points.

Every city's walk planner formed at least one new or reshaped multi-tree
walk from today's additions (Arnhem: 6 trees, 0.6km; Utrecht: 8 trees,
1.6km; Groningen: 6 trees, 2.5km; Haarlem: 6 trees, 1.2km; Maastricht: 7
trees, 1.6km; Rotterdam: two walks, 6+3 trees; The Hague: three walks;
Brussels: folded into the existing central walk) — the cluster-first
doctrine holding up city after city rather than needing to be argued for
each time. Ran `preflight.py`, `superlatives.py` (420 claims, no
collisions), `tree_index.py` and a full `npm --prefix site run build` after
every single city (9 builds total), plus `qa.py` each time (one
pre-existing sitemap-lastmod warning throughout, this sandbox's shallow git
checkout, not a real defect). Preflight caught and fixed two stale count
promises along the way (Rotterdam's `question_meta`, The Hague's
`meta_description` over its character limit) before either could have
shipped. Logged every pass to `data/agent-costs.json`. Photos: none
hunted, per this runner's no-photo-judging rule; all new trees carry an
honest `missing` photo gap.

Committed and pushed after every city (9 commits, each with its own claim/
release round trip via `passcheck.py`); one push landed between two
unrelated concurrent commits (a homepage styling change, a fresh-eyes
review run) and needed a clean rebase, no conflicts.

## 2026-08-20 (session) - A photo viewing pass: 13 photographs approved, 115 candidates rejected, 8 cities off the zero-photo list

Hidde asked to have another go at photographs for the cities with none. `health.py` rung 2 clear first (smoke, deploy, digest, fresh-eyes all green, no BLOCKER), so this was rung 6 work.

**Approved 13. `photo_gaps.py` counts 45 of 144 published cities with no photograph, down from 53 when this started**, so eight cities came off that list: Graz (3: the Schlossberg field maple and the Volksgarten oak, both with their Naturdenkmal sign in frame, plus the Eggenberg copper beech), Sardinia (2: both olivastri, Luras and Santa Maria Navarrese), Copenhagen (Skovfogedegen), Perth (the Royal Perth Hospital fig), Los Angeles (2: the LAHCM 19 fig and the oldest palm), Madeira (the Neves dragon tree grove) Mexico City (the Parque Espana ahuehuete) and Frankfurt (the Eschersheimer Linde). The thirteenth is Tallinn's Kelch's linden, a photo-less tree in a city that already had one picture.

**Rejected 115 and recorded every reason**, which is the half of this work that pays next time: an unrecorded reject is an image the following pass pays to judge again.

What the rejects actually were, because the pattern is worth knowing before the next pass:

| Failure | Examples |
|---|---|
| Not a photograph of a tree at all | three portraits of men called Zakrzewski for Poznan's maple, two Canadian prime ministers for the Mackenzie King pear, a Raphael for Perugia, a c.1650 map and an ESA satellite image for Maastricht, a 1941 railway photograph for two Chicago champions |
| Right species, wrong individual | Copenhagen's pacifier tree came back from Aarhus AND from Ostre Anlaeg, neither being the Frederiksberg hornbeam; a Julianaboom in Beekbergen; a Kampen stadspark for Maastricht |
| One file offered for several trees | two Assistens cemetery avenue shots offered for all seven Copenhagen trees in that cemetery; one iNat observation for both Ottawa Vitifolia lindens and again for both Kalopa kopiko |
| Detail, not portrait | the whole iNaturalist lane here is macro botany: hands holding flowers and leaves, no tree in the frame |
| Composition or light | Sydney's quad jacaranda (sandstone takes four fifths of the frame, and the tree in it is a thin young replacement), several POOR photo_light scores |

**Two things learned that are worth carrying forward.** First, a tree's own `verified_sources` sometimes already names the Commons file, and that is the strongest identity evidence available: Graz's copper beech was solved that way, by a file GPS-tagged at the register coordinate, after the sweep's own top candidate turned out to be a different copper beech in the Schlosspark. Only 4 photo-less trees currently carry such a reference, but it is a free check. Second, `photo_fetch.py`'s geotag and distance filtering is doing real work: everything that survived to an approval sat within 24m of our pin, and everything at 400m-plus was noise.

**One judgement call recorded as such:** Mexico City's ahuehuete is a trunk-dominant frame rather than a wide portrait, approved because the 1921 centenary plaque at its foot settles that it is this tree and not another ahuehuete in a city full of them. Identified and honest beat wide and unproven.

**The ranking function is not a filter, and today proved it in both directions.** `names_match()` in photo_gaps.py documents "0 means do not look", and photo_fetch.py fetches those candidates anyway. The obvious improvement is to make it a gate. Measured before writing it: **three of today's thirteen approvals score exactly 0 there.** Skovfogedegen, Kelch-Linde and L'olivastro di Luras all name their tree in the filename, and none of them contains a word the function recognises as a plant, because Danish, Estonian and Italian do not spell one the way the list does. 1,625 of 1,906 unjudged candidates score 0, so a gate would have thrown away a quarter of the day's results with the noise. That is the 58-trees-written-off lesson pointing the other way, and the docstring now says so with the counter-examples in it, because the idea is tempting enough that somebody will have it again.

What the same check did find is a real bug of the exact kind CLAUDE.md already names. The plant-word test is a SUBSTRING test, and the word set folded in `GENERIC` wholesale, which includes **"of"**. So the gate passed on almost any English title: "Statue of Queen Wilhelmina.jpg" scored 21 against Rotterdam's Wilhelmina Linden and was duly fetched and looked at, along with 76 other candidates riding on a connective. Removed the two connectives; 64 more candidates now correctly sort last. Resisted the follow-up temptation to widen the plant list with more languages, having measured it: adding the Polish "dab" rescues five photographs of roundabouts, because "roun**dab**out" contains it. The comment now carries that measurement so the next person does not have to rediscover it.

**Also fixed a real defect found on the way.** `photo_apply.py` wrote city files at indent 1 with no trailing newline, which is not what data/cities holds, so approving a single photograph reformatted the entire file: Graz arrived as a 724-line diff for a four-line change, and a real edit hidden inside that much churn is a review nobody can do. It writes indent 2 with a trailing newline now, matching `photo_check.py` and `season_backfill.py`.

FOR HIDDE: nothing blocks. The remaining 45 empty cities are mostly genuinely empty on Commons rather than unlooked-at: Caserta (20 trees), Melbourne, Hobart, Las Vegas, Dallas and Zaragoza returned no open-licence candidate at all across two sweeps. The cheaper next move for those is `famous_trees.py`, which finds trees we do not map that arrive with a photograph already attached, rather than hunting a photograph for a tree nobody has photographed.

## 2026-08-20 (session, later) - Everything from the audit that did not need Hidde

He said to do all of it that I could, so this is the audit's open list minus the four things that are his and the two that need a decision or data. Five shipped.

**The homepage has a button.** "Explore trees near you" was an underlined text link under a big white search field, which made the weakest affordance on the page the core action of the whole product. It is a filled pill with a pin on it reading "Trees near you". The search field is untouched and now reads as the second option, which is what it is.

**The location permission is primed before iOS asks.** Yesterday's fix made the system dialog appear at all; the expensive mistake left was being refused by somebody who would have said yes if they had known what it was for, and iOS gives exactly one shot at that question. There is a screen in front of it now that says what you get rather than what we need, with a "Not now" that leaves the shot unspent. This sits upstream of every save and therefore of every account.

**Explore leads with photographs.** "At their best in August" is the best idea in the product and it was rendering as rows of plain text. It is a shelf of cards now, the same card the map sheet uses.

**A locked walk says "Plus" instead of showing a bare padlock**, and the footer now says the honest half that was missing: Plus is not open yet. A lock with no price behind it reads as a thing you could buy today.

**The map's title became a control.** "Near Amsterdam" floated over the map as bare text, stating a problem with no way to fix it. It is a chip now, and when we do not know where you are it is the button that finds out, or the way into Settings if the answer was already no. Apple's own recentre button sits top right; once you had panned away there had been no way back to yourself at all.

**One risk taken and then checked rather than assumed.** Hiding the map's navigation bar so that chip could float meant the pushed tree page might lose its back button, which would trap somebody on a tree: a far worse bug than the cosmetic one being fixed, and not something a screenshot can see. `AncientTreesUITests` now taps a card, asserts there is a way back and taps it. Three UI tests, all passing: the way back, ticking a tree, and the sign-in sheet presenting.

**One new finding, made visible by fixing another.** Now that the season shelf shows photographs, the first card under "At their best in August" is a leafless wingnut in a car park. The layout is right and the picture contradicts the header. That is a photo pass, not a layout job, and it is finding 24 in UX_AUDIT.md.

**Still yours, unchanged from this morning:** the four dashboard actions. Three of them gate work that is written and sitting there, and one of them, the `{{ .Token }}` line, now also gates about an hour of website work rather than just the app.

## 2026-08-20 (session, evening) - The iOS app, rebuilt: accounts, a design of its own, and the four tabs

A long session with Hidde at the keyboard most of it, on his phone for the second half. **The app is the thing that changed today; the website only got small fixes.** If you are reading this cold, `UX_AUDIT.md` has every finding and `DECISIONS.md` has the three rulings he made.

**FOR HIDDE, what is left on your side.** Only two things, and one is money.

1. **`{{ .Token }}` in Supabase's Magic Link email template.** I cannot measure this one. Without it the six digit code in the app does nothing; Google still works.
2. **The Apple Developer Program, 99 euro a year.** Sign in with Apple cannot work on a free Apple ID at all, and TestFlight needs it. Your call, and you need it before the App Store anyway.

**What Hidde already did, measured rather than assumed:** the Google provider is on in Supabase and the authorize endpoint hands out a real client id, `ancienttrees://auth-callback` is in the redirect allow-list, `public.visited` now exists, and the Google Cloud consent screen is External and In production. Do not send him to redo any of that.

**What shipped in the app.** Sign-in exists at all, with three ways in: Apple, Google (through a system sheet, no SDK, so no new dependency in the product) and an emailed six digit code. The collection syncs to the same Supabase the website uses, so one person is one person across both. The app can now UPDATE ITSELF: Sync.swift had been written on 08-19 and called by nothing, so a tree the night runs added could not reach a phone without App Store review. It asks /api/version.json on launch and on pull to refresh. Verified end to end: a fresh install showed 1,406 trees and after a refresh and a restart, 1,526.

The app also stopped looking like the Settings app: cream ground, Gabarito from the website bundled under its OFL licence, cards where the photograph does the work. Tabs are **Home, Map, Collect, Profile**, with Home first on Hidde's ruling, overruling my argument for the map. Season became a gold pulse on the pins rather than a tab, walks became a filter on the map with the nearest one free.

**Do not re-hunt these, they are answered.** The white screen on his phone was **Xcode**: the app sat PAUSED in the debugger with four attach activities queued, half of them mine from `devicectl`. It was never an app bug. Navigation being "dead app-wide" was also wrong: my test had `.accessibilityIdentifier` inside TreeCard, where the heart button inherited it, so the test tapped the heart. And `displayPriority` on the map pins was tried away from `.required` and reverted; it hides pins, not labels.

**Three real bugs Hidde found by using it, and all three were invisible in a screenshot.** The sheet's drag threshold at 4 points ate taps on tree cards. Every card rendering a real MKMapSnapshotter froze Home on a phone. And Home rebuilt four groupings over 1,535 trees on every frame while scrolling. The simulator showed none of them: it has a Mac's network and a Mac's processor.

**The gap that produced all of that, and the next thing worth building:** the app has no CI. The website cannot deploy with a red test; the app has nothing between a push and his phone, which is why he found every one of these and I found none. Nine tests exist and run locally. Putting them on a macOS runner is roughly half an hour and it would have caught the tap bug outright. It will never catch stutter, which is the argument for TestFlight rather than against CI.

**And the honest headline on where the app stands against AllTrails:** the shape now matches, the material does not. 366 of 1,535 trees have a photograph. Every one of their cards is a photo; a quarter of ours are. That is not a design problem and no layout fixes it.

## 2026-08-20 (session) - A UX audit of both products, and the app can now be signed into

Hidde asked for the iOS app to be improved for one thing, getting as many people as possible to make an account, through the eyes of somebody who had just moved here from AllTrails, and then for a UX audit of the site and the app with it. Both are done. The full audit with every finding ranked is **`UX_AUDIT.md`**; this is the short version.

**FOR HIDDE: four things in your Supabase and Xcode dashboards, and three of them gate work that is already written and sitting there.** They are listed with exact locations at the bottom of UX_AUDIT.md. In one line each: add `{{ .Token }}` to the Magic Link email template (gates the app's email sign-in), enable the Apple provider with `app.ancienttrees.AncientTrees` as a client ID (gates Sign in with Apple, the single biggest lever in the whole audit), paste `supabase/visited.sql` into the SQL editor (the table has never been created, so the tick log has no cloud half on either platform), and accept Xcode's prompt about Sign in with Apple next time you build to your own phone.

**You answered two questions this morning and both are now in DECISIONS.md:** Apple sign-in is allowed, and the account wall is soft, meaning saving and ticking work with no account and the ask arrives when there is something to lose.

**The biggest finding is not about accounts at all.** `NSLocationWhenInUseUsageDescription` was missing from the app's Info.plist. iOS refuses to show the location dialog when that key is absent, so it was never shown to anybody, and the app fell through to its hardcoded fallback: **every user of the app, anywhere in the world, opened it on Dam square in Amsterdam.** The dialog appears now, confirmed by running it. This ranks above the account work because no sign-in screen converts a person who was shown the wrong city.

**Two more that were live and broken.** The paywall's "Tell me when this opens" posted a `note` column that does not exist on the waitlist table, so every press was rejected with a 400 while the screen said we would write to them, and the code set its success state without reading the result. It now posts columns that exist, carries the email address it needs to keep that promise, and says so when it fails. And three `.sheet` modifiers were stacked on one view, of which SwiftUI honours one.

**What the account work actually is:** Sign in with Apple and an emailed six digit code (never a magic link, so the app is never left), against the same Supabase project the website has used since July, so somebody who signed in on ancienttrees.app opens the app already holding their collection. Sign-in merges the two sides as a union rather than letting either overwrite the other. Tokens live in the Keychain. The You tab, which used to be a settings list led by the dead text "Signed in ... not yet", now leads with the account. Prompts fire at the first tick and the third save, three times ever at most.

**On the website:** the sign-in dialog offered three calls to action, and the middle one, "More options", linked to /account, which carries the same single email form and nothing else. It is gone, the app is a plain link rather than a competing primary, and the subtitle now names the tree that was just saved. On /account at 375px the email field had shrunk next to its long button until the placeholder read "you@exampl". Both are live and both CI jobs are green.

**Left open on purpose, with reasons in the audit:** the homepage's "Explore trees near you" is an underlined text link when it is the core action of the entire product, the Explore tab in the app is a table of contents with no photograph on it, and the tree page's action bar colours Save rather than "Take me there", which is a real trade between your two goals and should be settled by what the bar is earning rather than by taste.

## 2026-08-20 (session, continued) - Palermo deepens to 21: a verify pass on the Villa Tasca cluster, and a real answer-page bug caught by the build

Answered REVIEW.md's 2026-08-18 WARN too (Naples pin-provenance notes and Caserta's Piazza Vanvitelli pins): both already fixed in a prior session, just never logged.

Then rung 4. `city_queue.py --next`'s "WHAT YOU CAN ACTUALLY MOVE" list put Rome (rank 1) on top, but checking its raw leads file by hand (not trusting `leads.py`'s READY count, per BRIEF_WRITING.md's own warning) showed all 4 candidates had already been explicitly rejected by a 2026-08-14 pass (day-trip boundary, unconfirmed vitality, collectible-point failures) with the status field just never updated. Vienna's 10 "ready" leads turned out to be register-only German entries each held back with real, still-unresolved objections (padding, a live public controversy, unconfirmed access). Rather than keep auditing city after city by hand, moved to Palermo (rank 2, register-rich, small gap to target): claimed it, dispatched a `verify` pass on its Villa Tasca cluster.

**Verified and merged 3 trees, 18 to 21 (past the 20-tree target, judged worth it since all three sit within 200m of the already-published fig):** the London Plane of Villa Tasca (pal_019, Sicily's only nationally registered monumental plane), the Cook Pine (pal_020) and the Norfolk Island Pine (pal_021), each with a source beyond the MASAF register. The pass also caught and discarded a WebSearch AI-summary fabrication (a false "tallest tree in the city" claim not actually in the page it cited) before it could reach data.

**The build caught a real bug on merge, not a pre-existing one: the new plane's age estimate (180-220 years, from a foundation's unexplained figure) exceeded the existing highest-age_max tree, so the site's auto-derived "oldest tree" would have silently swapped from the well-documented 1845-planted fig (pal_003) to the plane's weaker estimate.** Set `oldest_tree_id: "pal_003"` to keep the stronger-evidenced answer. Worth remembering: any new tree with a wide age band can flip a city's oldest-tree page without anyone deciding it should, and the build will refuse to ship the contradiction rather than pick a side, which is what happened here (`palermo/oldest-tree: question_answer never mentions...`). Fixed two stale count promises (`question_meta`, `meta_description`) `preflight.py` caught. Rejected candidates recorded in `data/leads/palermo.json` with reasons (species-ID ambiguity, an undifferentiated avenue, a garden closed pending restoration).

Also ran the free half of the photo/scouting work this runner can actually do: `photo_hunt.py --recheck` (general sweep plus a targeted run on Caserta/Copenhagen/Budapest/Melbourne, the biggest photo-less cities; Copenhagen picked up real candidates, Caserta's register-only trees stayed a dead end), and `famous_trees.py --write` on every published-city country still missing a `_famous-<country>.json` file (Canada, Mexico, Cyprus, Estonia; Singapore/Romania/Iceland have no Commons category at all). Estonia's sweep matched tln_001 Kelch's Linden, which needed a photo, and queued 5 candidates for a viewing pass.

Build, `qa.py` and `superlatives.py` all clean throughout (one pre-existing sitemap-lastmod QA warning from this sandbox's shallow checkout, not real: `deploy.yml` uses `fetch-depth: 0`). Pushed into a race with a concurrent data-digest run (`c1cd5e4`, queue re-rank) and a product commit (photo-ask copy); `git pull --rebase` resolved it cleanly with no manual conflict, rebuilt and reran preflight/QA after to be sure, all still clean. Logged both Palermo passes to `data/agent-costs.json`, released the claim.

FOR HIDDE: nothing blocks. Bari's 3 verified trees (Pine of Carrassi plus the two already-written ombu/mangiafumo) sit in `data/research/bari-verified.json`, ready to ship the moment a 4th Bari tree turns up (register exhausted, both remaining candidates fail hard rule 10); worth remembering next time Bari's name comes up.

## 2026-08-20 (session) - Cleared the writing shelf: Lyon to 12, Bari's 3 verified trees stay held below the 4-tree floor

`python3 scripts/visitors.py`: 330 visits, 511 page views over the last 7 days (13th 17, 14th 34, 15th 33, 16th 83, 17th 44, 18th 67, 19th 42, 20th 10 so far). `prepare.py` said the shelf was already stocked: 40 cities staged for verify, 5 trees awaiting a writer (bari 3, lyon 2). Followed the prompt's own instruction to finish what's staged before starting anything fresh.

Step 0: `health.py` rung 2 clear (smoke, deploy, digest, fresh-eyes all green, no BLOCKER). REVIEW.md's one open WARN (2026-08-19, `city_queue.py --next`'s STAGE 1 header over-claiming Hidde's authorization for from-zero research) turned out already fixed in the code (the `*`-marks-the-named-17 fix is live at lines 424-438); answered it in the ledger rather than re-doing the work. Supabase submissions: all 6 rows already processed and previously resolved (checked CURATION.md for each; nothing left to do). Nothing published found wrong.

Wrote the 3 missing stories on the shelf (bar_003 The Pine of Carrassi, lyo_012 The Anne Frank Chestnut, lyo_013 The Plane Tree of Place Antoine-Rivoire) directly in-session rather than dispatching a writing pass for such a small batch. **Lyon merged: 10 to 12 trees**, both new entries sit within 1.3-2.4km of Lyon's existing clusters (checked by distance, not by name), fixed a stale "all ten" FAQ line and a "eight more" `question_meta` promise that `preflight.py` caught. Ran `tree_index.py`, `npm --prefix site ci && npm --prefix site run build` (1936 pages, clean), `qa.py` (1 pre-existing sitemap-lastmod warning from this sandbox's shallow git checkout, not a real defect: `deploy.yml` uses `fetch-depth: 0`), `superlatives.py` (415 claims, no collisions).

**Bari's 3 verified trees (bar_001, bar_002, bar_003) stay unmerged.** Puglia's register for Bari is exhausted: only 4 monumental trees are designated in the whole city, and the other one is blocked (a Villa Sbisa pine, university grounds with no public access) alongside a second already-blocked school-courtyard leccio. That leaves exactly 3 usable, one short of the 4-tree floor, and finding a 4th means from-zero web research, which rule 1(d) keeps off for Bari (not one of Hidde's 17 named cities). Left the 3 fully written and ready in `data/research/bari-verified.json` for whenever a register import, reader submission or a name from Hidde unlocks a 4th tree.

Logged both to `data/agent-costs.json` under 2026-08-20. Committed and pushed.

## 2026-08-20 - Night run 2026-08-20 02:46 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 16.4 minutes of its 120 minute window, 118 turns, 15 commands refused by the allowlist, ended clean (success). 6 commit(s), none of them a published tree. Claims left behind: bari, lyon, krakow, warsaw, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-20 - Night run 2026-08-20 00:27 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 6.9 minutes of its 120 minute window, 65 turns, 8 commands refused by the allowlist, ended clean (success). 1 commit(s), none of them a published tree. Claims left behind: houston, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-19 - Night run 2026-08-19 22:29 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 5.4 minutes of its 120 minute window, 47 turns, 7 commands refused by the allowlist, ended clean (success). 2 commit(s), none of them a published tree. Claims left behind: houston, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-19 (session, continued) - Caserta deepened to its 20-tree target from its own READY leads

After Bilbao, switched to rule 1(a) of "the course after the fortnight":
writing up already-verified stock is cheaper than opening anything else, and
`leads.py` showed 30 READY leads for Caserta alone, already published at
14/20. Read all 30 by hand rather than trusting the READY label blindly,
because several carried real unresolved caveats in their own
`why_not_published` field (a Cephalotaxus fortunei with an implausible
25m/450cm figure "may be a mis-measurement", a Zelkova whose two registers
disagree on SPECIES not just detail, an Osage orange whose girth field
literally reads "sdraiata" instead of a number). leads.py's fail-open design
would happily hand those over as READY; picking through them by hand and
choosing only the 6 marked "Count only", meaning the sole reason they were
held back originally was the pre-2026-08-02 ten-tree cap doctrine that
CLAUDE.md has since killed, kept this pass honest without costing a
verification cycle.

**The six**: Bottle Tree (Kurrajong), Chir Pine, Turkey Oak, Southern
Magnolia, Osage Orange and Mediterranean Hackberry, all cross-sourced
against Italy's national MASAF register and Campania's own regional detail
card, both already cited in the leads file. Wrote all six in one pass,
merged as cas_015 through cas_020. Caserta is now 20 of 20, its target hit
exactly with real trees rather than padding.

**Two build failures caught at merge**, both hard rule 9 (one species, one
common name): the write pass correctly left `species` untouched, but its
values (`Kurrajong`, plain `Hackberry`) collided with the corpus's existing
canonical forms for the same Latin binomial (`Bottle Tree` already used in
Barcelona, `Mediterranean Hackberry` already used in Ferrara and others).
Fixed both, and renamed/lightly reworded the Kurrajong entry's title and
opening sentence so the page's species chip and its prose agree.

**Fixed the city's own count promises**, since a sixth of its trees just
appeared: intro, meta_description and two FAQ answers said eleven paid /
three free; now sixteen paid (all in the English Garden) and four free (the
existing three in Piazza Vanvitelli plus a new magnolia standing right at
the palace gate on Piazza Carlo di Borbone, a different square). Also caught
and fixed a count-promise false trigger at preflight ("the sixteen stand"
read as a claim about all twenty trees; rephrased to "sixteen of the twenty
trees here stand").

`npm --prefix site run build` clean (1934 pages), `preflight.py` clean (144
cities), `superlatives.py` clean (414 claims, no collisions). Same
shallow-checkout `qa.py` sitemap-lastmod note as the other entries tonight.
Ran the free `photo_hunt.py --recheck` sweep (0 new candidates, an honest
gap this register just doesn't help with). `tree_index.py` refreshed;
`leads.py --city caserta` confirmed all 6 auto-detected as DONE by
coordinate match, no manual leads-file edit needed.

| Pass | Trees | Cost |
|---|---:|---:|
| Caserta write (from existing leads) | 6 | 47k |

## GIT PUSH BLOCKED, roughly 21:34 to past 22:00 UTC: this entry and the
Bilbao/Caserta commits are sitting locally, not yet on origin. The GitHub
installation token embedded in this sandbox's remote URL expired mid-session
and did not refresh on repeated retries (roughly a dozen attempts over 20+
minutes). This is an infrastructure issue, not a data or process one: every
build/QA/preflight check above passed clean on the actual commits. FOR
HIDDE: if this entry is missing from the live LOG.md when you read it,
check whether the Hawaii/Ottawa commits (which did push successfully early
in this session) are the last ones you see, and know that Bilbao and this
Caserta expansion exist, verified and ready, waiting on a push.

## 2026-08-19 (session, continued) - Bilbao opened, 4 trees, honestly thin and scattered

Continued down the ladder after Ottawa. Checked `data/leads/*.json` for cheap
already-verified stock (Caserta alone had 30 READY leads, per rule 1(a) of
"the course after the fortnight") but weighed that against Hidde's more
recent 2026-08-19 ruling in CITY_QUEUE.md that opening unopened cities beats
deepening published ones ("a new city taken to 10 is a page that can start
ranking; a thirtieth tree in Rome is marginal"); Caserta at 14/20 read as
closer to that marginal case than to a genuine gap, so left those leads
staged for a session that picks up rule 1(a) explicitly, and continued
opening instead.

Picked **Bilbao**, one of the 17 cities Hidde named by name (from-zero web
research explicitly authorised there). Confirmed first that no usable
register exists: `passcheck.py --brief` found nothing within 20km, and
OPEN_DATA_SURVEY.md separately records the Basque Country's own singular-tree
decree as a dead end (legal catalogue, download 404). Claimed Bilbao,
dispatched a from-zero research+verify pass following CLAUDE's "name the
places first" technique (parks, university grounds, sacred ground, then local
press, then a generic sweep).

**Result is honestly thin on sourcing, though it walks better than first
reported.** 4 trees, right at the floor, cost 180k tokens (45k/tree, well
above the 27-55k range other from-zero cities ran today) and the pass
stopped there deliberately rather than grinding for a cheaper fifth, per the
80/20 rule. The verify pass's own eyeballed distances ("1.5 to 3km apart,
not one walkable cluster") did not survive a coordinate check afterward:
three of the four, Deusto, the Misericordia garden and Dona Casilda, sit
within 0.93km of each other, and the fourth (the Albia planes downtown) is
1.08 to 1.38km from that group, all well inside the project's own 2km
clustering threshold. Corrected the page copy (intro, meta_description, the
"one walk" FAQ) to describe one walk of roughly 25-30 minutes rather than
four unconnected stops; the lesson for a future brief is to compute
distances rather than estimate them by eye once coordinates exist. Three of
the four
carry only a vague "centenario" (over a century) age claim with no
measurement; one (the Dona Casilda horse chestnut) was flagged by the verify
pass itself for near-identical wording across its two sources, a real risk
they share one original tourist-board line rather than confirming
independently, and the story says so outright rather than presenting it as
double-sourced. Two of the four (the Albia planes, the Misericordia garden)
ship as ensemble entries, the garden or square itself being the destination
rather than one named tree, which the collectible-point rule allows for a
compact, famous, one-place-to-stand site.

Fixed a build failure at merge: the write pass correctly left `species`
fields untouched, but two candidate values collided with the corpus's
existing canonical names (`Platanus x hispanica` vs the corpus's
`Platanus x acerifolia` for London Plane, and a multi-species "mixed: ..."
string in the ensemble entry that broke hard rule 9's parser entirely).
Fixed both to the existing canonical forms; picked the Canary Island date
palm, the one specimen the story itself calls out ("a tall palm dominates
the middle"), as the ensemble's representative species tag.

`npm --prefix site run build` clean (1928 pages), `preflight.py` clean (144
cities), `superlatives.py` clean (414 claims, no collisions). Same
shallow-checkout `qa.py` sitemap-lastmod note as the two entries below,
environmental to this sandbox. Ran the free `photo_hunt.py --recheck` sweep
(candidates for 2 of 4), nothing judged. `tree_index.py` refreshed.

| Pass | Trees | Cost |
|---|---:|---:|
| Bilbao verify | 4 | 180k |
| Bilbao write | 4 | 52k |

Released the Bilbao claim. Bilbao is now 4 of its 10-tree target, at the
floor; growing it further needs either a reader tip or a session willing to
spend well above the usual from-zero rate. Continuing down the ladder.

## 2026-08-19 (session, continued) - Ottawa opened, 8 trees, one bridge-claim trap caught

Continued down the ladder after Hawaii. `city_queue.py --next` still showed
Bari on top (deprioritized, see above) and most of Hidde's 17 named cities
already opened by earlier sessions today. Picked **Ottawa** (rank 49, not one
of the 17 but carrying 119 scouted register candidates already sitting in
`data/research/ottawa-register-candidates.json`), which fits "open it from a
register" under the 2026-08-19 ruling even though it wasn't named outright.

The register (Canada's National Capital Commission, "A Living Legacy:
Remarkable Trees of Canada's Capital", Open Government Licence Canada v2.0,
already cleared in OPEN_DATA_SURVEY.md) is the richest one scouted so far:
real per-tree descriptive prose, not just a data table. Grouped its 114
entries by distance and found 8 within half a kilometre of Parliament Hill,
across Confederation Square, Confederation Park and Major's Hill Park, a
genuinely tight downtown cluster. Claimed Ottawa, dispatched a hand-built
verify brief against the register plus independent sources for each tree.

**The pass caught a real bridge-claim trap.** The register's own description
of "The Response" linden mentions, in the very next sentence, that the
National War Memorial beside it ("The Response" is the memorial's formal
name) was unveiled in 1939 by King George VI. Nothing says the tree itself
was planted then; the pass confirmed independently that "The Response" names
the memorial, not the tree, and shipped the tree's age as undocumented rather
than inheriting the monument's date. Three other trees (a linden pair and a
horse chestnut) carry a genuine circa-1900 estimate tied to William Saunders'
Central Experimental Farm nursery, independently corroborated as a real
mechanism, carried forward with the register's own "likely"/"circa" hedging
intact rather than sharpened. A Serbian spruce trio ships as one entry (three
trunks, one place to stand) per the ensemble rule.

Fixed three species names at merge to match the corpus's existing canonical
common names (Small-leaved Lime, Large-leaved Lime, Horse Chestnut) that the
write pass correctly flagged rather than silently using non-canonical ones.
Since three trees tie on the same age estimate, set `oldest_tree_id`
explicitly to one of them and had the question page state the tie honestly
rather than picking a false winner.

`npm --prefix site run build` clean (1922 pages), `preflight.py` clean (143
cities), `superlatives.py` clean (414 claims, no collisions). Same
shallow-checkout `qa.py` sitemap-lastmod note as the Hawaii entry below,
environmental to this sandbox, not this change. Ran the free
`photo_hunt.py --recheck` sweep (candidates found for 3 of 8), nothing
judged. `tree_index.py` refreshed.

| Pass | Trees | Cost |
|---|---:|---:|
| Ottawa verify | 8 | 100k |
| Ottawa write | 8 | 46k |

Released the Ottawa claim. Ottawa is now 8 of its 10-tree target. Continuing
down the ladder.

## 2026-08-19 (session) - Hawaii (the Big Island) opened at Kalopa State Park, 6 trees

Visits (7-day): 336 visits, 524 views, trending up (67 on 08-18, 37 so far on
08-19). Ran `health.py` (rung 2 clear, 0 BLOCKER), checked Supabase directly
(SUPABASE_URL isn't a real env var, hardcoded in site/src/lib/site-config.ts;
fetched all 6 rows, 0 unprocessed). `prepare.py`'s shelf had 40 cities staged
for verify and Bari's 2 verified-but-unwritten trees still held below the
floor, per the standing Hidde ruling not to open Bari; left both alone rather
than re-litigate.

Rung 4: `city_queue.py --next` puts Bari first but Hidde's 2026-08-19 ruling
in CITY_QUEUE.md says open the unopened big-name cities first. Of the 17 he
named, most (Dallas, Mexico City, Seattle, LA, Frankfurt, Las Vegas and
others) were already opened earlier today by other sessions. Picked **Hawaii**
(rank 39, the Big Island, deliberately kept separate from Hilo which already
covers the town): city-queue.json's own note flagged 30+ unpublished
register trees at Kona, Volcano and the Hamakua coast, and a prior session's
scouting sat unused in `data/research/hawaii-bigisland-candidates.json`.

Grouped the 38 register candidates by coordinate rather than trusting
`passcheck.py --brief` (its radius search centres on the wrong point for this
entry and returned zero matches). Six trees shared one exact coordinate:
Kalopa Native Forest State Park on the Hamakua coast, a 0.7-mile loop through
one of the last old-growth native forest stands on the island. Claimed
Hawaii, dispatched a hand-built verify brief (passcheck's own brief was
unusable here) against the register plus DLNR's own trail page.

**The pass earned its cost.** It caught a dead tree before publication: the
one Kona candidate outside the Kalopa cluster, a Moreton Bay Fig gifted by
Queen Kapiolani in 1882, was cut to a stump in October 2025 after internal rot
failed a branch (Big Island Now, fetched directly), despite the register's own
"Excellent" vitality rating. And it caught three implausible register
heights (a "184 ft" koa, "170 ft" hame, "84 ft" kopiko 'ula, all 2-3x their
species' documented ceilings) and excluded them rather than publishing them;
the girths on the same three specimens are trustworthy and became the leading
facts instead (a hame normally 4-10m tall carrying a 2.16m trunk, a kopiko
'ula normally slender at 3.26m round). None of the six carry a recorded age;
said so plainly per the standing rule rather than guessing.

Wrote all six stories in one batch, built the city file by hand (schema
matched against hilo.json and las-vegas.json for the no-age oldest_tree_id
pattern: named the largest-girth tree, the Larger Ohi'a Lehua, as both hero
and "oldest" while the question page explains honestly that girth is not
age). `preflight.py` caught an over-length intro and question_meta on first
pass, trimmed both to fit Contract C. Ran the free `photo_hunt.py --recheck`
sweep (1 candidate found for 5 of 6 trees, nothing judged, this runner can't
reach upload.wikimedia.org). Ran `tree_index.py` (62,141 trees tracked).

`npm --prefix site ci && npm --prefix site run build` clean (1912 pages),
`preflight.py` clean (142 cities), `superlatives.py` clean (413 claims, no
collisions). `qa.py` reports one failure (sitemap lastmod all identical) that
traces to this sandbox's shallow git checkout (`git rev-parse
--is-shallow-repository` is true here, depth 1), not to this change; flagging
rather than chasing a fix for an environment issue outside this session's
control.

| Pass | Trees | Cost |
|---|---:|---:|
| Hawaii verify | 6 | 95k |
| Hawaii write | 6 | 70k |

Released the Hawaii claim. Hawaii is now 6 of its 10-tree target; the Kona
leads (a likely royal-banyan-cutting Indian Banyan and an unidentified
Chinese Banyan) sit in data/leads/hawaii.json for a future pass that has time
to pin them individually. Continuing down the ladder.

## 2026-08-19 (night run, continued) - Five species pages, and a thin Vienna pass

Closed rung 7 first: `pagegaps.py` had 5 species with 3-4 trees each and no
intro (Southern Live Oak, Pecan, Dutch Elm, Lime, Blue Jacaranda). Wrote all
five, each from that species' own mapped trees per P3, no template filler:
Las Vegas's desert-grown live oak and the two Dealey Plaza oaks that framed
the JFK shots; Bordeaux and Seville's improbably tall park pecans; Amsterdam,
The Hague and Portland's Dutch elm disease survivors; a coronation lime, a
storm-broken one and Frankfurt's eight-trunk bundle planting; three
jacarandas including Sydney's 2017 clone of the Quadrangle original.
`pagegaps.py` now reports 0 missing everywhere.

Then Vienna (rank 8, 25/30 trees, 375 register candidates on the shelf):
claimed, dispatched a verify pass against the city's own Naturdenkmale
register. Yield was thin, 2 of roughly 10 checked candidates, because most
nearby unverified entries turned out to be private courtyards or villa
gardens once checked against German Wikipedia's district Naturdenkmaler
lists (a technique worth reusing). Both delivered: a second Rathauspark
plane (the register dates it 1873, which is the park's founding year on
every entry there, not a per-tree record, so the story keeps the age broad
rather than bridging it), and a Hügelgasse plane whose register address
explicitly reads "vor Nr. 7" (in front of, not inside), the one clean
public-access signal found among several courtyard entries nearby. Wrote
both, merged, fixed the meta_description/question_meta tree counts
preflight caught (still said 25), fixed a species-binomial mismatch the
writer flagged (Platanus x hybrida vs the corpus's x acerifolia). Vienna is
now 27 of 30.

`npm --prefix site run build` clean (1900 pages), `qa.py` clean (2214
pages), `superlatives.py` clean (412 claims, no collisions).

| Pass | Trees | Cost |
|---|---:|---:|
| Species intros x5 | n/a (page work) | included in session, not agent-dispatched |
| Vienna verify | 2 | 202k |
| Vienna write | 2 | 82k |

Vienna's yield-to-cost ratio is worth flagging for whoever picks it up next:
most of what's left near its existing clusters is private land, so another
pass there should expect a similarly thin return unless it opens a new
cluster further out.

Then Palermo (rank 2, 14/20 trees, 43 register candidates, all from Italy's
national monumental-tree registry). Claimed, verified 4: a Giardino Inglese
fig, a Giardini Reali fig that has grown around and partly engulfed a stone
pine over the decades ("l'abbraccio"), a pecan with a Monstera vine coiled
up its trunk in the Orto Botanico, and a flame tree 85m from the
already-published Dragon Tree at the same nursery address. One correctly
avoided: a register entry with an extraordinary 36-metre "girth" turned out
to be the same coordinates as the already-published pal_001 at Piazza
Marina, crown spread rather than trunk, not a new tree. One correctly
blocked: a fig inside a private palace courtyard, visitable only on
owner-guided tours, held under hard rule 10. The write pass caught and cut
a draft sentence that would have bridged the embracing fig's ~135-year
estimate to the Norman kings, and correctly gave the largest-fig-in-Palermo
superlative to the already-live pal_001 rather than claiming it twice.
Fixed the meta_description/question_meta tree counts (still said 14) at
merge. Palermo is now 18 of 20.

`npm --prefix site run build` clean (1904 pages), `qa.py` clean (2218
pages), `superlatives.py` clean (412 claims, no collisions).

| Pass | Trees | Cost |
|---|---:|---:|
| Palermo verify | 4 | 95k |
| Palermo write | 4 | 91k |

Released the Palermo claim. Stopping here for this run; the site builds
clean end to end and every rung down to page gaps has been checked today.

## 2026-08-19 (night run) - Geneva deepened to 18, Bari's two written stories held off the shelf

Visits (7-day): 334 visits, 521 views; 2026-08-19 alone 35/57. Ran health.py
(rung 2 clear, 0 BLOCKER), checked REVIEW.md's newest WARN (city_queue.py's
STAGE 1 header) and the prior 2026-08-18 WARN (Naples/Caserta pin
provenance): both already fixed by earlier commits today (33f6e21 and the
city_queue.py star-marker fix), nothing left to do at rung 2 or 3. Reader
submissions: all 6 in Supabase already in data/submissions-processed.json,
nothing new.

Rung 4: `prepare.py`'s shelf had Geneva's register file (122 SITG candidates)
staged and Bari's two verified-but-unwritten trees (bar_001, bar_002)
waiting on a writer. Claimed Geneva, dispatched a verify pass against the
canton's own remarkable-tree register (it carries a vitality field, one of
the few that do): **4 new trees, gen_015 to gen_018**, filtering out 14
near-duplicates of already-published trees and catching a placeholder-date
trap (the register buckets unknown plantings under 1912-01-01 or
1962-01-01, which would have read as a real year). One likely-private
diplomatic-estate cluster (Rothschild's former Terre de Pregny) went to
blocked rather than shipped. Geneva is now 18 of its 20-tree target.

Wrote stories for both Geneva's 4 and Bari's 2 in one batch (BRIEF_WRITING.md
rules; the writer caught two species-name mismatches, Geneva's plane and
hackberry entries used non-canonical common names, fixed at merge before
build). Merged and published Geneva's 4. **Held Bari's 2 back**: below the
four-tree floor on their own, and LOG.md's own second-round entry today
records Hidde saying explicitly he meant big-name cities when picking the
next unopened city, not Bari ("ik zat meer aan sydney enzo te denken niet
bari"), and killing an earlier Bari pass for exactly that reason. Continuing
to open Bari today would have repeated a correction from earlier the same
session. The two written stories stay in data/research/bari-verified.json,
nothing thrown away, ready the day either the floor is cleared or Hidde
names Bari himself.

`npm --prefix site ci && npm --prefix site run build` clean (1893 pages),
`preflight.py` clean (141 cities), `qa.py` clean (2207 pages), `superlatives.py`
clean (411 claims, no collisions).

| Pass | Trees | Cost |
|---|---:|---:|
| Geneva verify | 4 | 172k |
| Bari+Geneva write | 4 merged (+2 held) | 110k |

Released the Geneva claim. Continuing down the ladder.

## 2026-08-19 (session, second round) - Four more off the top, and a correction to how I picked them

Hidde asked for the next four cities still at zero. I took them by queue rank
and got it wrong: rank here is demand times how cheap a city is for us, so
Bari and Hawaii came out on top because we already hold their registers, not
because anyone searches for them. He said so plainly ("ik zat meer aan sydney
enzo te denken niet bari", then "is dat echt de grootste prio stad nu?").
Both passes were killed two minutes in, about 27k tokens, and Mexico City took
the slot. The lesson is worth keeping: our own score answers "what is cheapest
per tree", and he was asking "what is biggest", and those are different
questions the ranking quietly merges.

**Four cities live, 29 trees.** Los Angeles 7, Dallas 8, Mexico City 9,
Seattle 5. The site is at 141 cities.

| City | Trees | Cost/tree | What carried it |
|---|---:|---:|---|
| Dallas | 8 | 27k | The Texas Big Tree Registry's ArcGIS layer, found through the app's JS bundle after the documented host hung, plus txhtc.org's named historic trees |
| Mexico City | 9 | 32k | SEDEMA's 2025 Arboles Patrimoniales declaration, a register nobody here had scouted, with tree-level GPS and measured trunks |
| Los Angeles | 7 | 40k | No register exists (LAMC 46.00 protects species, not trees); figs dated from the buildings put up beside them |
| Seattle | 5 | 55k | No register either; the Heritage Tree programme names trees and publishes no data, so every entry came from park and university documents |

**The measured pattern across both rounds, eight cities.** A city where some
authority once published a list of individual trees costs 25k to 32k per
published tree. A city where none exists costs 40k to 76k and yields fewer
trees. That is the whole spread, and it does not track city size at all. The
first question before opening a city is not how big it is; it is whether
anybody there ever wrote a list.

**Three entries were pulled at the merge, and two of them are the same rule.**
El Pino in East Los Angeles, the bunya pine from Blood In Blood Out, stands in
the front yard of a private house; the verify pass had it as view-only, which
covers an institution's wall and not somebody's home. Eugenio in Mexico City
sits inside a residential lot by SEDEMA's own location field. Both are
recorded in full in their leads files so the call can be reversed in a minute
if Hidde disagrees. The third, the Chavez Ravine Arboretum, is a hundred
species over a hillside rather than one place to stand, and what belongs there
is its Queensland kauri, held as a lead until somebody pins that trunk.

**What the passes caught before it could ship**, which is the part of this
work that never shows on the site: a state champion black willow in Dallas cut
down by accident in 2015, three Comanche marker trees dead since 1998, a giant
sequoia at Green Lake removed in December 2025, LA's Encino Oak fallen in
1998, and both of Mexico City's famous ahuehuetes, El Sargento dried out in
1969 and the Noche Triste tree that the city's own venue page calls a ruin.
Two of those were the trees I sent the pass to find.

**A register to promote, and it needs ten minutes rather than a run.** SEDEMA's
Arboles Patrimoniales KML carries all twelve declared trees with coordinates,
species and girth, and its licence sentence has not been read at the source,
which is the gate before it can go into data/registers/. Recorded in
data/register-scouting.json with the one data fault it carries: the height
column has lost its decimal point, so 22 metres reads as 2200.

## 2026-08-19 (session) - Four unopened cities off the top of the queue, and three of them opened

Hidde asked for a run on the prioritised cities that have no register and no
trees. The queue already had that as its stage 1, so the ask and the list
agreed: Sydney (#22), Las Vegas (#24), Frankfurt (#25) and Perth (#29), all
four on the seventeen he named on 2026-08-19, which is what rule 1(d) needs.
Four verify passes in parallel, then two write passes.

**Four cities live, 29 trees.** Frankfurt 6, Las Vegas 11, Perth 6, Sydney 6.
Sydney needed a second pass to clear the four-tree floor and only just made
it; the other three cleared it first time.

| City | Trees | What carried it |
|---|---:|---|
| Frankfurt | 6 | de.wikipedia's Naturdenkmal list joined to the city's own Amtsblatt gazette, because frankfurt.de is Cloudflare-blocked (now on the fetch blocklist) |
| Las Vegas | 11 | The 2015 Nevada Big Tree Register, cross-checked against UNLV's own November 2025 piece naming the same champions, which is also the alive-now evidence |
| Perth | 6 | The National Trust WA register plus Wikidata; Kings Park and the CBD figs |
| Sydney | 6 | Two passes. The City's 2,504-entry register turned out to be mostly avenue plantings and does not cover the Botanic Garden or the Domain |

**What the passes refused, which is the part worth reading.** A well
documented fig in Fremantle that stands in a private front garden. Two
Wikidata entries whose own names say the tree was removed. A kauri at
Elizabeth Bay House that is probably on an apartment block's grounds. A
Hunters Hill fig that traces to a private house. Fremantle's King's Square
fig ensemble, where the register still lists six trees and the council's own
page says two were replaced in 2018, so it stays a lead until somebody counts
them on the ground.

**Las Vegas is honest rather than impressive, deliberately.** Girths from 51
to 234 centimetres, no age on any of them, every pin approximate at building
or park level. The question page says so outright: nobody has published an
age, the register measures size and not years, the city dates from 1905, and
the biggest trunk is not the same thing as the oldest tree. It asks the reader
for UNLV's planting records.

**Two of Sydney's six are replacements, and they lead with it.** The
Quadrangle jacaranda is a 2017 clone of the 1928 tree that died in 2016, and
its story opens by saying it is about nine years old. The Wishing Tree is a
1930s replacement whose own plaque admits it will never match its predecessor.

**Answered the pin WARN from the 2026-08-18 review before starting.** Naples'
three undocumented "confirmed" pins turned out to be grounded at 17, 1 and 2
metres from their register sheets and now say so. Caserta's casuarina and yew
were 32 and 19 metres from their cited points and each sat nearer the other's
point than its own, which reads as a swap; both are back on the coordinate
their own source gives, and the yew's unsourced "Via Alois side" description
went with them, since Via Alois runs east and the register puts it west.

**And today's review WARN, fixed the same hour.** `city_queue.py --next`
printed "he named these cities" over all 181 unopened cities. Seventeen were
named. The named ones now carry a star and the header says from-zero research
is off everywhere else.

FOR HIDDE, one thing, no action needed today: every city page ends with "see
all N remarkable ancient trees in [City]", and on Las Vegas that sits under
our own sentence saying nothing there is ancient. It is template copy on all
137 cities and "ancient trees" is the brand, so I have not touched it.

## 2026-08-20 (session) - Alignment is measured now, and both platforms read one rulebook

Hidde saw it on /explore: the panel's heading sat at 28 and the city list under it at 17.6, and he asked the question that mattered more than the fix. "Kunnen we zorgen dat jij de alignment altijd van de website in de gaten houdt?"

**The check.** The smoke test now measures DRIFT on seven pages at 375 and 1280. A COLUMN is anything whose visible children are stacked; each child's GUTTER is the leftmost place it puts ink; two gutters in one column that sit more than 0.6 and at most 11 points apart are a fault. Bigger gaps are deliberate insets and are left alone. What it took to stop it crying wolf, since a naive version flags every page: something that paints a visible box contributes its box edge and everything else its text edge, inline runs are skipped because a <strong> mid-paragraph has no gutter, centred text is skipped because its left edge is a function of its length, and a row hands back its leftmost item rather than its own padding box.

**What it found, all real, all fixed:** /explore's panel (one --panel-x token now feeds the head, the list, the intro and the prose, at both widths); every tree card on every page, where a 3px transparent border-left held the slot for the selected-pin bar and pushed the text 3px right of the heading above it (it is an inset shadow now, which takes no space); /netherlands' ranked rows carrying 0.2rem nobody else had; /cities' whole card grid sitting 7px right of its own country headings.

**Then the second half of his ask: "zorg dat de CI voor app en web dezelfde kwaliteit nastreven".** They did not. The app could measure a four-point drift and threw the numbers away, because SweepFrames printed them and ios.yml's grep discarded them; the website had no idea what a drift was. Now `scripts/layout_rules.py` holds the three thresholds and both sides import it, appfit.py and appsweep.py and SweepFrames.swift are committed (they were untracked, which is the same as not existing), and ios.yml runs appfit.py over the full xcodebuild log so CLIPPED, DRIFT and SMALL fail the app build the way a red smoke test says the site is broken.

**One deliberate difference, said out loud rather than hidden.** SMALL is gated on the app and only PRINTED on the web: the site has 22 controls under 44x44 at 375px, the save heart at 67x26 on every card among them. Fixing those is a design pass, not something to spring on a deploy.

**FOR HIDDE:** nothing is blocked on you. One thing the check cannot see, because it only compares inside a column: a phone has three different gutters on it (bar 16, map panel 17.6, content pages 24). Worth one decision from you some time, and then it is a one-line change.

## 2026-08-20 (session) - The phone header: one control, and the stale CSS that was un-centring it

Hidde on the mobile nav: the hamburger was not centred and the bar looked odd, so put everything under it.

**The centring was not a design slip, it was a duplicate.** The `@media (max-width: 800px)` block describing the mobile header existed THREE times in style.css. The first styled the summary as a 32px circle with the icon flex-centred; the two later copies re-declared it as a padded inline box with `display: inline` on the icon, and being later they won. An inline SVG sits on the text baseline, so it hung high and left inside the circle. The duplicates are deleted, the header is described in one place, and the icon now measures dead centre (dx 0, dy 0 in a 40px button, measured at 375px).

**And the bar is now the mark plus one button.** Map, the account avatar and the "Get the app" pill carry `.only-desktop` and reappear inside the panel: Map first under Browse, a Yours group with saved trees and account, then Suggest a tree, then the CTA as a full-width green button. Desktop is untouched. Two side effects worth naming: this reverses the earlier rule that Map stays a persistent bar item at every width (it is first in the panel instead, which is what that rule was protecting), and the wordmark comes back below 480px, because the bar now wants ~220px of a 375px screen instead of 412px. Recorded in DECISIONS.md.

Verified with eyes at 375px, 768px and 1280px against the real stylesheet: nothing runs off the right edge, the panel is 351px wide on a phone and caps at 352px anchored right on a tablet, and it scrolls rather than running off a short screen.

## 2026-08-19 (session) - The night shift had been dead for 27 hours, and the queue got its new shape

**Start with the thing that was actually broken, because it explains the quiet.** Between 08-18 05:19 and this morning, **eight consecutive night runs failed**, each after 30 to 40 seconds, one turn, no commits. That is the usage-limit signature this file already describes ("attempts that hit the usage limit die in seconds and cost nothing"), and it means the machine did nothing at all for 27 hours while `run-health.json` recorded eight tidy "success" rows. Hidde confirmed the weekly limit had run out and has since reset. Worth saying plainly where it went: 08-16 and 08-17 spent 2.3M and 3.0M tokens, most of it on the five island pages, which was the work he asked for and was also what ate the week.

**The daily digest was throwing away its own entry.** It wrote DATA.md, committed, and then died on `git pull --rebase` with "you have unstaged changes", so the commit was discarded and 08-17 simply had no row. The cause: `city_queue.py` rewrites `LEDGER.html`, which was not in the digest's `git add` list. Fixed twice over, because the list will go stale again: LEDGER.html is named now, and the pull runs with `rebase.autoStash=true` so the next unnamed file cannot kill a run the same way.

**A correction to my own diagnosis, which is the useful part of the day.** Yesterday I read Palermo and Bath (CTR near 1% at average position 9) as a snippet problem. It is not. The digest's depth table shows an IMPRESSION-WEIGHTED AVERAGE across a city's pages, and comparing an average against the CTR curve is only honest when the underlying positions are tight. Crossed against the per-query data, Palermo's biggest query sits at **position 10**, Bath's at **10**, Florence's at **11**, while Vienna, which earns 7%, sits at **6**. Four places over the fold is the entire story, and no title rewrite reaches it. Paris makes the point from the other side: 5.3% CTR while its biggest query ranks 62, so its clicks come from somewhere the average hides. The depth table now prints each city's biggest query and that query's own position, and the pairs pull went from 200 rows to 1,000, because the low-click cities the column exists to diagnose were the ones falling off the end.

**The digest now reports what the night shift ACHIEVED**, not just whether it ran (Hidde: "kun je dat standaard in de daily digest vertellen"). Utilisation answered whether the windows were used; he had to ask what came out of them. New table, every day, straight from `run-health.json`: minutes, turns, trees, commits and refused commands per run.

**And that last column is now readable for the first time.** The denials meter, dead for two days after the SDK renamed its field, was repaired on 08-17 and immediately showed **10 to 27 refused Bash commands per run**. The 05:20 run took 27 refusals in fifteen minutes and produced nothing. That is the best lead we have on why short runs stop early, and the next thing worth seeing is WHICH commands.

**Hidde's three rulings on the queue are in DECISIONS.md** and only summarised here: targets are 10 / 20 / 30 with the 50 tier deleted, opening the unopened cities now outranks deepening, and the cron runs nine times a day this week while he is on the app. The LEDGER.html artifact was regenerated and republished on its existing URL, and now carries a block explaining the rule it renders, which it never did.

**FOR HIDDE:** nothing is blocked on you. The night runs pick up the new order from 18:00 UTC. The two standing asks are unchanged: ten Request Indexing submissions in Search Console, and the Sydney licence email in `drafts/permission-us-registers.md`, which is now more valuable than it was because Sydney sits at rank 22 on tonight's open-these-first list.

## 2026-08-19 - Night run 2026-08-19 08:24 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 0.0 minutes of its 120 minute window, 1 turns, ended clean (success). Nothing reached data/cities.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-19 - Night run 2026-08-19 05:20 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 0.0 minutes of its 120 minute window, 1 turns, ended clean (success). Nothing reached data/cities.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-19 - Night run 2026-08-19 02:49 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 0.0 minutes of its 120 minute window, 1 turns, ended clean (success). Nothing reached data/cities.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-18 - Night run 2026-08-18 23:16 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 0.0 minutes of its 120 minute window, 1 turns, ended clean (success). Nothing reached data/cities.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-18 - Night run 2026-08-18 20:16 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 0.0 minutes of its 120 minute window, 1 turns, ended clean (success). Nothing reached data/cities.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-18 (session) - The menu, investigated properly this time

Hidde: "ik vind t menu nog steeds niet kloppen, onderzoek het en maak het beter." Opened at 375px and on desktop and found three faults rather than guessing at one.

**The map had left the phone navigation entirely.** Fixing the bar overflow earlier took two cuts where one would do: dropping the wordmark saved 115px and fixed it on its own, and hiding the Map link as well removed the product's core from the bar with nothing in the menu to fall back to. On a phone there was no way to reach the map from the navigation at all. That is the one that mattered and it was mine, from an hour before.

**The panel read as a takeover, not a dropdown.** Nearly full width at 375px, 46px between rows, a filled circle behind every icon. Rows are the ordinary 36px now, the icons lost their chips, and the panel is capped at 15rem so the map stays visible behind it. Measured after: 192px wide, 36px rows, on both widths.

**"Suggest a tree" sat under the BROWSE heading**, as though suggesting a tree were a category to browse. It sits below a rule now.

On the reference, stated plainly because two of tonight's faults came from inventing instead of looking: AllTrails is behind a slider bot-check I will not solve, and Komoot's own drawer would not open for me, so the row sizing is ordinary dropdown practice rather than a copy of theirs. Their HEADER shape (mark, one pill, one menu button) is what the bar already follows, and that part I did see.

## 2026-08-18 (session, late night) - The paywall is set, and the app prep it obliges

Hidde set the paywall line and left ("doe het gewoon ik ga weg"). Everything below is live and verified.

**FOR HIDDE, one thing needs your hands.** `supabase/visited.sql` needs one paste into the Supabase SQL editor, exactly like saves.sql. Until it runs, the personal tree log stays as local as it is today: every request 404s, is caught, nothing breaks. After it runs, ticking off a tree survives a new phone.

**The paywall line is recorded, in DECISIONS.md 2026-08-18 with your copy verbatim.** €19.95 a year, 7-day trial, four features behind it. CLAUDE.md's "still undecided" section now points there. Your instruction with it was "we moeten dit verhaal waar gaan maken", so the rest of this entry is the distance between the promise and the product, closed where it could be closed tonight.

| Promise | Was | Now |
|---|---|---|
| Curated tree walks | data existed, reachable by nothing | `/api/walks.json`, 175 walks, 78 with a real routed shape |
| Season Radar | fired for 383 of 1,377 trees | 546, and honestly silent on the rest |
| Personal tree log | localStorage only, one browser | syncs to the account as a union, like saves |
| Full offline access | feeds carry everything but photographs | unchanged; the app caches pictures itself |

**Season Radar, and what it refuses to do.** 163 trees gained a peak from phenology we had already written. A species moment rated `nice` or `unseen` earns nothing, so 343 trees stayed silent on purpose: if every deciduous tree claimed a peak the badge would be lit all year and stop being a reason to go anywhere. The months carry the same latitude shift the site applies at render, since a stored best_time is read literally. The remaining 484 are species with no phenology file at all, led by Mediterranean Hackberry, Coast Redwood and Atlas Cedar. That is writing, and it is ordinary night-run work.

**Also tonight, from your phone screenshots:** the nav bar overflowed by 37px so "Get the app" ran off the screen, the account control was a bare icon beside a stray caret, and two menus could stand open at once. All three fixed, and the mobile bar now follows Komoot's shape (mark, one menu button, one avatar, one pill) because AllTrails sits behind a bot check I will not solve. A photo on Sofia's Oak of Pencho Slaveykov had been a dead Commons link showing a broken frame; found by the new `scripts/photo_check.py` and retired.

**And the check that answers your question about QA.** None of the four layers could see whether a page FITS a phone. The smoke test now loads six representative pages in a 375px iframe and fails the deploy if anything runs past the right edge. It caught the homepage card shelf on its first run, which turned out to be a legitimate side-scroller, so it learned to look for a scrolling ancestor first. Recorded as QA layer 3b; removing it needs you.

## 2026-08-18 (session, night) - Responsive breakage, and the check that should have existed

Hidde walked the site on his own phone and found what a screenshot makes obvious and no gate had noticed. His question was the useful part: "we hebben toch een qa proces? hoe kunnen we dit voorkomen in de toekomst, loop je jezelf wel na?"

**The honest answer is no, not for this.** The four QA layers check structure, check that elements EXIST, read diffs, and use real eyes every two weeks. None of them measures whether a page FITS a phone. And CLAUDE.md's own per-change eyes rule says to look at a changed element rendered at 375px before calling it done; for the account menu I verified with querySelectorAll instead, which is exactly the grep-verified deploy that rule was written against.

**What was broken.** The bar wanted 412px in a 375px screen, so "Get the app" ran off the edge; the wordmark is 115 of those pixels and is the piece every app drops on a phone. The account control was a bare line-art person beside a stray caret, shipped an hour earlier without anyone looking at it; it is now a circular avatar button with no caret, which is what AllTrails, Strava and Google Maps all use. And two `<details>` menus knew nothing about each other, so opening Account over Explore stacked two panels; menus now close their siblings, and a click outside or Escape closes them all.

**The check, which is the part that lasts.** The smoke test now loads six representative pages in a 375px iframe and fails the deploy if anything runs past the right edge. Chrome's --dump-dom returns markup rather than values, so the measuring happens in a harness page that writes its findings into its own DOM. Its first run caught the homepage card shelf, which is an overflow-x:auto row and is supposed to overflow, so the check learned to walk up for a scrolling ancestor first. Recorded in CLAUDE.md as QA layer 3b.

**Also fixed:** the content schema was silently stripping the photo dimensions photo_check.py had just written, so the app feed shipped 353 nulls while the data files held every one.

## 2026-08-18 (session, late) - The app data feed, and three things Hidde caught on his own account

**/api/version.json and /api/trees.json.** How a new tree reaches an app without a new build: the app ships with a snapshot, asks the 85-byte version file on launch, and pulls the 798 KB (gzipped) dataset only when the content hash differs. Data is not code, so App Store review is not involved. Live and verified: both files agree on version `16e011987b841e89`, 1,377 trees, 133 cities, and every tree carries `precision`, access, transport and its photo's licence, so an app cannot show a rough pin as exact or a picture without its credit. Useful whether or not the app happens.

**The 0 trees / 0 cities on /account** read the check-in log, which is app-only on a phone since 2026-08-14, so they sat at zero above a list full of saved trees. They count the saved trees now, owned by the same script that draws the list so they cannot disagree with it.

**Yours moved from Explore to Account**, which is where Strava, AllTrails and Google Maps keep it. Account became a small dropdown, wearing an avatar on a phone so the bar stays on one line.

**The whole tree card is clickable**, using the stretched-link pattern. It lit up on hover on every page and then only its two links did anything.

**A correction worth recording, because it changed advice I had already given.** I argued against building premium features partly on "2.4% of visits do anything". That window runs from 08-08, and until 08-16 every product event was being dropped (`sendBeacon` cannot preflight, commit f240bc2). The number measured our own broken instrument, not behaviour. Since the fix events flow, and a save now reaches the events table, verified by clicking one. Check what the meter is doing before quoting it.

## 2026-08-18 (session, evening) - Four bugs Hidde found by using it, and the walk overlay

**The sheet froze when you zoomed out.** Far enough out, a city page swaps its list for a "Cities in view" chooser, and that code hid every child of .panel except itself. Since this morning's sheet those children are the grab handle and the body, so it hid the one thing you can drag. The chooser now lives inside .sheet-body.

**The photograph became a poster.** The card is drawn for a 480px panel; on a full-width page it stretched to the column. Capped at the panel's own width, everywhere.

**Saved trees moved under /account.** They were a top-level menu item beside Account, which is not how Strava, AllTrails or Google Maps do it. The list lives in lib/saved-list-js.ts, /saved redirects and stays alive.

**Sign-ins were silently expiring after an hour, and this was the serious one.** Supabase gives an access token good for 60 minutes and a refresh token good for far longer; we stored both and used only the first. So an hour after signing in, saves stopped reaching the account and nothing said so. Locally the heart still worked, which is why it looks fine until you open a second device. signin-js now refreshes on load and re-runs the sync.

**The walking-routes pill opens an overlay instead of leaving the city.** Three lines of what the app does, one waitlist field (source `walks-modal`, so it is tellable apart from /app), the full page one tap away, and a cross that puts you back where you were. It reuses SignInModal's dialog rather than inventing a second modal shape.

**The lesson underneath three of these**, and it is now in the convention memory: two were caused by not following our own component, and one by a rule that predated the sheet. Hidde's words: "onthou altijd om niet zelf te gaan experimenteren."

## 2026-08-18 (session) - /explore becomes the same page as a city page, and saved trees keep their photograph

**One layout for every map page.** /explore had its own `.explore-app` / `.explore-split` / `.ex-panel` and a 38vh drawer on a phone, while the city page got a Google Maps sheet the same morning. It now uses the same skeleton and the same SHEET_JS: peek, half, full, tap the map to collapse. The prose moved into the sheet, as the city page's FAQ already was, so nothing sits below a one-screen layout where a phone cannot reach it. Verified at 375px: peek shows the title and the search field, half shows "Cities in view" and then the prose.

Recorded where it acts rather than in a note, per the ratchet: PRODUCT_IA.md carries the ruling, and `check_sheet_integrity()` in qa.py now keys on the LAYOUT rather than a page name, so any future page carrying `.split` must ship the sheet or fail the deploy.

**A saved tree keeps its photograph.** Hidde: "het is wel leuk als de saved trees of het tree component altijd de foto gebruikt als die er is." The component always did; /saved could not, because a save stored only a name and a url. The heart now carries the photograph and the meta line too. Saves made before today have neither and render with empty slots rather than a placeholder.

Found while wiring that: **the save handler stored `location.pathname` as the tree's url**, which on a city list is the CITY page. So every tree saved from a list has been linking back to the city instead of to itself, since hearts went on cards on 2026-08-14. Fixed; older saves keep whatever url they were stored with.

**The stylesheet is fingerprinted, and that was a real bug rather than a precaution.** style.css sat in public/ at a fixed path, so its URL never changed however much the file did, and a returning visitor got fresh HTML with a cached stylesheet. It happened in this session's own check: /explore's map rendered as an empty grey rectangle because the new markup met the old positioning rules. It cures itself when the cache expires and recurs on every layout change, which is the worst shape a bug can have.

`site/src/lib/asset-hash.ts` computes a content hash once per build and the link carries it as `?v=`. Verified live: every page type carries `?v=b99cb9d2bd`, that URL serves the 84 KB stylesheet, and the hash equals the sha1 of the shipped file, so it moves exactly when the bytes move. The font beside it is left alone; its bytes never change.

## 2026-08-18 (session) - One tree card, walks off the web, and cities findable in their own language

Four asks from Hidde in one session, all live. The map fix that started it has its own entry below.

**Walking routes leave the web.** "die ik niet beschikbaar wil maken op web, maar die je naar de landingspagina van de app brengt, zodat er meer ruimte is voor de kaart en de bomen." The green route capsule, the walk picker and the drawn route line are gone from both city pages; one small pill on the map reads "Walking routes, in the app" and links to /app (`data-ev="walks-app"`). This is PRODUCT_IA.md line 10 applied, web reads and app walks, and it makes the deepest filter on the page the one app hook that is a feature rather than a promise. The cost, worth watching: walking is one of the four verbs and the web now delivers three. Nothing was deleted, on his instruction ("de functie hebben we later dus wel nog nodig voor app dus gooi de info niet weg"): walks.ts, data/walk-routes.json and both scripts stay, each with a note saying why, and the walk CSS is marked parked.

**One tree card, everywhere.** "kunnen we niet een centraal component maken zodat we bomen overal op dezelfde manier weergeven." There were two: the city page's .tree-card and a smaller .entry with a 96px thumb on the park, species, collection and country pages, so every improvement to one missed the other. `components/TreeCard.astro` is now the only one, used by both city pages, parks, species, collections and countries. What varies is how much TEXT it carries, and that is not taste: the story is unique 150-250 words whose canonical home is the city page, so repeating it on four URLs is what P3 forbids. City pages get the full story, everyone else the first sentence or a collection's own note. Language is a prop, so the Spanish page is the same component rather than a copy that drifts. /saved stops being a list of links and shows the same card, emitted from JS because it renders from localStorage; it cannot fill species, age or the photograph, so those slots stay empty rather than invented.

**Cities findable in their own language.** "het is wel handig als steden als den haag ook te vinden zijn in hun eigen taal." Den Haag, Firenze, Wien, München, Napoli, Praha, Lisboa, Warschau and Kopenhagen all now find the right page. `scripts/city_names.py` generates them from Wikipedia's langlinks: 131 of 133 cities, 1169 names. A city is confirmed by coordinates and never by name, because Wikipedia's "Cordoba" is a disambiguation page. Standard practice from here, as he asked: nightly.yml regenerates for any city opened that run and queries only cities it has never seen, and preflight prints a NOTE naming any city never looked up.

**The city intro stops being truncated.** It sat in the fixed sheet header at four clamped lines. It now lives in the scrolling body, shown whole, and scrolls away leaving the title.

**Two new ratchet checks in qa.py**, tenth and eleventh: a page carrying the bottom-sheet CSS must carry its markup and script, and no page may ship the retired .entry tree markup.

**FOR HIDDE.** Cloudflare emailed that ancienttrees.app was removed after four weeks without a nameserver change. Checked: nothing is broken and nothing needs doing. The domain never ran through Cloudflare, DNS is at TransIP pointing straight at GitHub Pages, and the site is served by GitHub. The only thing we use is the cookieless Web Analytics beacon, which is a separate product that works on sites Cloudflare does not proxy; it is still loading and still posting, and this morning's digest still read 510 visits. Re-adding the domain would put Cloudflare in front of GitHub Pages, which is a real change to the serving path and needs a reason, not an email.

## 2026-08-18 (session) - The phone city page had no map, and could not be scrolled

Hidde: "gister is er een ux verbetering op de stadspagina gemaakt maar vastgelopen nu is de kaart niet meer zichtbaar."

**What was live, on every city page in both languages, since 2026-08-17 21:02.** The Google Maps bottom sheet landed as CSS only. `style.css` made `.panel` a fixed, full-height sheet at z-index 20 whose position is driven by a transform, and made `.stage` (the map) an absolute layer at z-index 1 underneath it. The markup that gives the sheet a grab handle and an inner scroller was never added, and `sheet-js.ts` was written and imported by nobody. So the transform was never set: the sheet sat at translateY(0) covering the map completely, and the `overflow: hidden` that belongs on `.sheet-body` sat on the panel itself, which meant the tree list could not be scrolled either. A phone visitor saw one tree card and no way to reach the other thirty. Desktop was untouched throughout, which is why nothing caught it: the build passed, the smoke test passed, the deploy went green.

**What now ships, which is the rest of that work rather than a revert.** The four movements Hidde asked for again today, in his words "veel meer zoals google maps is waar de kaart groot wordt als je daarmee interacteert en andersom met de lijst" and "als je op een boom specifiek klikt dat dan de informatie van die boom alleen opent onderin":

1. The page opens as a map, with the sheet at a peek: the city name, the tree count, a drag handle.
2. Dragging or tapping the header moves it through half and full; the map shrinks, the list grows.
3. Tapping a pin or a card opens THAT tree alone, with its story, Save and directions, and a back link to the list. Nothing is removed from the DOM, only hidden with a class, so a crawler still sees the whole city.
4. Touching the map drops the sheet back to the peek. The zoom controls and the walk capsule are exempt, so using them does not collapse the list.

Two things fixed while wiring it up. The walk capsule was pinned to the bottom under a z-20 sheet, so it was invisible; it now floats just above the peek and fades out once the sheet covers the map. And a tapped pin used to fly to the centre of the map ELEMENT, which is behind the sheet: the map now recentres on the part of it you can still see.

**The ratchet.** `check_sheet_integrity()` in `scripts/qa.py`, the tenth. If the stylesheet carries the sheet layout, every built city page must also carry the id, the grab handle, the inner scroller and the script. It is the same shape as the hearts-need-the-dialog check: parts that must never separate. Proven against yesterday's exact output, which it catches.

Verified at 375px and at 1280px in a browser, against the live page with the change injected, because there is no local Node and no local build: peek, half, full, one-tree detail, back, and touch-to-collapse each looked at rather than inferred. What the browser could not exercise is a real finger drag and the flyTo offset, which needs the deployed map script; both are worth a look on a phone once this deploys.
## 2026-08-18 - Night run 2026-08-18 11:15 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 0.0 minutes of its 120 minute window, 1 turns, ended clean (success). Nothing reached data/cities.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-18 - Night run 2026-08-18 08:24 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 0.0 minutes of its 120 minute window, 1 turns, ended clean (success). Nothing reached data/cities.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-18 - Night run 2026-08-18 05:20 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 15.3 minutes of its 120 minute window, 116 turns, 27 commands refused by the allowlist, ended clean (success). 6 commit(s), none of them a published tree. Claims left behind: seville, zaragoza, Las Vegas, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-18 (session) - Krakow: 10 to 16 trees, off the READY leads shelf

`visitors.py`: 275 visits, 427 page views over the last 7 days (2026-08-11 to 2026-08-18), trending down toward the end (83 on 08-16, 44 on 08-17, 2 so far on 08-18). `prepare.py`: 32 cities staged for verify, 0 trees awaiting a writer. Step 0: no unprocessed Supabase submissions (SUPABASE_SERVICE_KEY present, 6 rows total, all already processed). `health.py` rung 2 clear (smoke, build/deploy, digest, fresh-eyes, weekly all green/recent; REVIEW.md's one BLOCKER already answered on 2026-08-17, Milan's Archdevil). Nothing published found wrong.

Followed the course's rule 1(a) (cheapest supply: write what is already verified). `scripts/leads.py --ready` listed 4 Krakow leads as publishable; reading the actual leads file found 2 more that the script's own DONE-marker regex was misfiring on (a false positive on "shipped as kra_009" appearing inside a *comparison* sentence about a different tree, not a self-resolution marker; confirmed by coordinate check that neither was actually live). All 6 had been held back in an earlier pass for reasons CLAUDE.md's 2026-08-10 ruling now explicitly forbids: cut for count, ninth-in-line, and a taste call that an invasive species "reads as a curiosity". None of those block publication any more.

Verified each against a second independent source before writing (Polish Wikipedia's reproduction of Krakow's own registry list, cross-checked against the GDOS/CRFOP national register already used for kra_005-010), which also supplied exact street addresses the leads file itself lacked. Ages derived only where a same-species same-register Krakow tree already existed to scale against (Studencka Plane off kra_005, Kossaka Ash off kra_006, Tarlowska Lime off kra_007); left empty for the standard-form oak, the ginkgo and the tree of heaven, since no safe proxy existed (kra_009 is a columnar cultivar, not comparable to a standard oak) and Ailanthus's growth rate is already documented in `data/species/tree-of-heaven.json` as too fast and site-dependent to date honestly off girth. Shipped the Batorego oak and ginkgo (20m apart) as one entry since only one coordinate point was verified for the pair, marked `approximate`; the other five are `confirmed`, same register precision as the trees already on the page.

Recomputed the walk rather than trusting old copy: two short walks now, 7 trees/1.8km and 5 trees/1.4km, plus the existing 3-tree botanical garden cluster and the standalone Henryk Oak. Rewrote intro, meta_description and the "one walk" FAQ answer to match (had to trim the first draft from 110 to 87 words, Contract C caught it at build time). Build and `qa.py` green (1777 pages, 2075 checked), `preflight.py` clean, `superlatives.py` clean (384 claims, no collisions). Ran `tree_index.py` (45,874 tracked, 1340 highlighted, up from 1334). Logged the pass in `data/agent-costs.json` (session work, tokens untracked by the harness for main-session edits). Claimed and released `krakow` in `data/in-flight.json`. Committed and pushed (20c1e9a).

Left three temp scripts untracked in `scripts/` (`_tmp_*.py`) because `rm` was denied by this session's permission settings; they are not staged or committed, harmless if left, safe for a future run to delete.

FOR HIDDE: nothing blocks. The leads.py DONE-marker false positive (noted above and in CURATION.md) is a minor data-quality finding, not fixed this pass since it fails safe; worth a look if it recurs.

## 2026-08-18 (session) - Brussels: 20 to 23 trees, second READY-leads city this session

Continued the same rule 1(a) pass into a second city. `leads.py --ready` listed 6 Brussels leads; shipped the 3 with the strongest basis (second Turner's Oak of Parc d'Egmont, White Mulberries pair at the Passage de Milan gate, Turkish Hazel of the Grand Sablon single-sourced and flagged) and left 3 genuinely weaker ones as leads (a shrub-scale holly, a group entry with an ambiguous per-tree girth, a maple whose register health rating flags "middling defects" and needs checking before it ships). The second Turner's Oak was already named directly in the published bru_011's own story ("A second, taller Turner's oak grows a few minutes away"), so this was known-good and simply unwritten; caught and avoided repeating a measurement conflation on Wood Wide Web's atlas page that bru_011's own notes had already flagged.

Walk recomputed rather than assumed: the new trees fall inside the existing Egmont cluster and also pull in the Grand Sablon hazel (about 400m away in reality), producing one 13-tree, 1.0km walk. Left it as one walk rather than forcing a split into smaller groups: `walk_planning.py` clusters by distance (900m radius), not tree count, and CLAUDE.md's "four to eight trees" language reads as typical shape rather than a hard cap. `preflight.py` caught two stale count promises (question_meta and one FAQ answer still said "twenty" after the count moved to 23); fixed both. Build and `qa.py` green (1780 pages, 2078 checked), `superlatives.py` clean (no crown collisions). Ran `tree_index.py`. Logged the pass. Claimed and released `brussels`. Committed and pushed (22e001f).

## 2026-08-18 (session) - Caserta: 10 to 14 trees, a new free second walk

Third and last city this session off the READY leads shelf. Unlike Krakow and Brussels, most of Caserta's 32 READY leads turned out NOT safe to ship on sight: sampling the list found real, unresolved data problems (registers disagreeing on species or on coordinates by 200-400m, girths that are averages across a pair rather than either tree's own measurement, trees under any reasonable size bar), which are genuine evidence gaps rather than the invalid count/taste reasons CLAUDE.md's ruling overturns. Shipped only the two clean candidates: a third English Garden plane (held back only for repetition), and a genuinely new find, three trees in Piazza Vanvitelli, Caserta's own town square, that the leads file had marked single-sourced. Found and fetched the missing second source directly (Campania's regional register cards, scheda_48/49/50), which matched the national MASAF register's girths for all three exactly, so they ship two-sourced rather than flagged-and-thin. This gives Caserta a genuinely new thing: a free second walk, since all 11 of its other trees sit inside the Reggia's paid English Garden.

Caught a real hard-rule-9 collision at build time (Casuarina equisetifolia already published in Cordoba as "Horsetail Casuarina", not "Casuarina") and fixed it before the second build. Updated intro, meta_description and two FAQ answers, since the old copy flatly said Caserta's trees were "all in one place, and it is not the town", now false. Build and `qa.py` green (1784 pages, 2082 checked), `superlatives.py` clean. Ran `tree_index.py`. Logged the pass. Claimed and released `caserta`. Committed and pushed (7320e3b).

Nine temp scripts now sit untracked in `scripts/` (`_tmp_*.py`, across all three cities this session). `rm` continues to be denied by this session's permission settings; harmless to leave, safe for a future run or session to delete.

Ran `pagegaps.py` (rung 7, required every run): Brussels' new second Turner's Oak crossed the species page's 3-tree publish gate alongside the existing Amsterdam and first Brussels entries. Wrote `data/species/turners-oak.json` from those three trees' own facts (the disputed 1865/1895 Amsterdam planting year, the two Egmont oaks a few minutes apart). Build and `qa.py` green (1785 pages, 2083 checked). `pagegaps.py` now clean (0 species/country/park gaps). Committed and pushed (936c17f).

Session total: 3 cities deepened (Krakow 10 to 16, Brussels 20 to 23, Caserta 10 to 14), 13 trees published, one new species page, one brand new free walk (Caserta), two walks recomputed and rewritten (Krakow, Brussels), zero new web-research cities opened, all off the already-verified READY leads shelf per the course's rule 1(a). No BLOCKER, no broken build, nothing left mid-flight.

FOR HIDDE: nothing blocks.

## 2026-08-17 - Night run 2026-08-17 23:16 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 12.4 minutes of its 120 minute window, 79 turns, 17 commands refused by the allowlist, ended clean (success). 7 commit(s), none of them a published tree. Claims left behind: yakushima, krakow, rome, perugia, berlin, paris, kyoto, ottawa, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-17 - Night run 2026-08-17 20:19 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 10.7 minutes of its 120 minute window, 98 turns, 15 commands refused by the allowlist, ended clean (success). 4 commit(s), none of them a published tree. Claims left behind: bari, yakushima, ottawa, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-17 - Night run 2026-08-17 11:17 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 19.1 minutes of its 120 minute window, 108 turns, 10 commands refused by the allowlist, ended clean (success). 6 commit(s), none of them a published tree. Claims left behind: salzburg, gdansk, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-17 (session) - Vilnius to 10, and four instruments repaired on the way

Hidde: keep running night runs and improving the system on them. Three cycles so far.

**The denials meter is alive, and it was the missing instrument.** The multi-key search shipped yesterday found it on the first run: the field is `permission_denials`, a LIST, not the `permission_denials_count` the code had been reading since the SDK renamed it. The 08:32 run recorded 6 refusals and produced nothing in 7.8 minutes, which is exactly the pattern we could not see before. Because it is a list it can carry the tool NAMES, so those are now recorded too, names only and never arguments (this repo is public and reader submissions pass through these runs).

**`health.py` was crying wolf.** A deploy still running reports `conclusion: ""`, which the check compared only against `None` and therefore read as a failure: "Smoke test is  (its newest run, 0h ago). The site may be broken." A night run would have stopped to investigate a healthy site. It now reads the newest FINISHED run, which is what the question actually asks.

**Two tools for one job, resolved.** A night run wrote `photo_shortlist.py` the same morning this session wrote `photo_gaps.py`. Their ranking was better than mine (a photograph hanging off the tree's own Wikidata item scores 60, because somebody who knew which tree they meant attached it), so it was folded in and their file deleted.

**Vilnius is live at 10.** The verify pass earned its keep on defence rather than supply: the Wikipedia-registry join confirmed or killed 8 of 10 candidates and caught two delisted-dead trees and a pair locked inside a company courtyard, none of which the register itself flags. Three shipped. The Sapiegos Park linden is the one to read: a storm took its top off on 18 July 2023, an arborist found it rotten through, 28 metres became 11 or 12, and the story LEADS on the break rather than selling a giant that is not there. It ships because sources agree it survived and it was entered into Tree of the Year 2023 after the damage, and the page says plainly that our newest report is two years old and asks the visitor which way it has gone since.

**The photo aim got its answer, and the answer is that the pictures do not exist.** Hidde asked for one photograph per city, then ranked it below five trees. Eight candidates judged across two sessions, two shipped. Only one rejection was about picture quality: the others were the wrong tree (Copenhagen's pacifier tree stands three kilometres from ours), the wrong subject (Perugia's file is statues, event chairs and a dog), or the wrong kind of photograph entirely (iNaturalist is an identification platform, so its images are a hand holding a leaf). Recorded in CURATION.md as a dead end rather than left to be re-run.

**And the reverse route is now proved rather than recommended.** Klopstocks Eg sits 13 km outside Copenhagen with three Commons photographs, and the first one opened is textbook: an ancient oak filling the frame, trunk and crown readable, a bench for scale, CC BY-SA 4.0. So `photo_gaps.py --famous` now pairs each photo-less city with a famous tree that arrives with its own picture. Melbourne's Separation Tree at 2.8 km heads the list and is exactly the one to check first, since it is famous for a proclamation in 1850 and there is a ringbarking story attached to it.

**One rule moved out of the briefs and into the rulebook.** The Wikipedia-registry join has paid off three days running and had to be re-explained each time. It is in BRIEF_RESEARCH.md now, with the reason that matters most: a register records what is designated and never says a tree has fallen down, while the Wikipedia reproductions carry the removals in their footnotes. Every dead tree caught this week was caught there.

## 2026-08-17 - Night run 2026-08-17 08:32 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 7.8 minutes of its 120 minute window, 63 turns, 6 commands refused by the allowlist, ended clean (success). 2 commit(s), none of them a published tree. Claims left behind: naples, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-17 (session) - Every live city was asked for one photograph; ten found one, and the filter that was hiding the rest got fixed

Hidde asked for at least one photograph on every live city. 45 of the 127 published cities had none. Ten now do: **Ferrara, Braga, Brno, Palma de Mallorca, Tallinn, Wroclaw, Nuremberg, Cagliari, Catania and Vilnius**, each verified open licence with attribution recorded, each looked at as pixels before it shipped. Catania got two, its bunya pines being visibly different trees 21 and 29 metres from their own pins.

**The honest headline is that the yield was low and the reason is worth more than the ten.** Around 300 candidates were viewed across 45 cities and nearly all were rejected. They were not near misses: a 1941 postcard of a locomotive matched "Champion", an oil painting of the Oslo palace, a portrait of the physicist Konstanty Zakrzewski matched on a surname, a doorway letterbox matched on a street address, one cemetery photograph served for three different Copenhagen trees, and every Hobart candidate was photographed in Brisbane, 1,789 km away. The queue was never a queue of tree photographs; it was a queue of filename coincidences.

**The find that pays for the day: our own filter was throwing the answers away.** The sweep only keeps a geosearch hit whose title names a plant, and it checked that against OUR species field, which is English. So "Naturdenkmal Linde in der Grünanlage Hallerwiese Nürnberg", CC0, standing 9 metres from our Nuremberg pin, was discarded because we file that tree as "Lime (Tilia sp.)" and the German for lime is Linde. That is a whole class of miss and it falls hardest on exactly the cities where nobody writes in English, which is most of the queue. `GENERIC_TREE_WORDS` now carries the local species names and the Naturdenkmal/pomnik/monumentale designations, and `SWEEP_VERSION` went to 5, which re-asks every negative ever recorded. The re-sweep ran the same day over all 38 remaining cities and paid for itself three times: Catania's bunya arrived on "Pino del Queensland monumentale", Cagliari's ficus and Vilnius's university lime on files no pass had ever been shown.

Only tokens of five characters or more went in, and that limit is load-bearing: `mentions()` anchors just the END of a token, so "den" is inside "garden", "es" ends every plural and "pin" is inside "Chopin". Tested before shipping, on the titles that would have flooded the queue.

**New gear, all of it the cheap half of the work.** `photo_fetch.py` downloads a city's shortlist once, serialised at one request per three seconds (Wikimedia 429s above that), scores exposure on the way past and leaves a manifest, so several viewing passes can run at once without fighting the rate limit or each other. `photo_apply.py` and `photo_verdicts.py` record approve/hold/reject into the city file and the queue in one serialised sweep, because parallel judges would otherwise clobber the queue and the next pass would pay to judge the same images again; 210 rejections are now recorded and can never be re-judged. `photo_last_resort.py` asks for every geotagged photograph within 120 m with the plant-word filter off, for cities the ordinary sweep leaves empty; it found Nuremberg's lime.

**Two things it got wrong and had to fix.** Its category-name search read "Curtain Square" as the Curtain Theatre and returned a map of Shakespearean London for a Melbourne plane tree; that half is now off by default, and 2,256 stored candidates carrying no coordinates were pruned, halving the queue file. And a last-resort candidate is now required to have a geotag, because proximity is the only evidence such a file carries.

**What is left, stated plainly: 35 cities still have no photograph, and 13 of them are now finished rather than merely unfinished.** Budapest, Caserta, Hobart, Melbourne, Montreal, Parma, Potsdam, Quebec City, Reykjavik, Split, Thessaloniki, Toronto and Zaragoza have had every open-licence candidate any source offers looked at and rejected; there is nothing left in the queue for them. The answer there is readers, partners or a genuinely new source, never another sweep. Four photographs are `held` rather than approved, all on identity rather than quality: Aarhus, Bangkok and Catania's dragon tree because no geotag settles which tree it is.

**What the rejections keep turning out to be is a name collision, and that is the next thing to fix.** A tree named after a person matches photographs OF that person: Poznan's Paczoski plane returned the botanist's studio portrait and his gravestone, its Krzysztof oak returned two unrelated men called Krzysztof, Rotterdam's Wilhelmina linden returned the queen twice, and Wroclaw's Dzierzon oak returned the beekeeper. Seven wasted viewings in one day, all detectable from the Commons categories, which say "Beekeepers from Poland" and "Valued images of politicians" in plain words.

**Two credit bugs were caught on the way, both of which would have published something we should not.** Commons' Artist field is free text: Catania's bunya carried the photographer's private email address and a licensing request, and iNaturalist hands back "(c) Name, some rights reserved (CC BY)" as if it were a name. Both were about to render as the visible credit on a public page. `clean_author()` now takes the first line, strips any address or url, and drops the boilerplate; three attributions already live were rewritten. A licence obliges us to name the photographer, and it obliges us to nothing else about them.

FOR HIDDE: nothing is blocked on you. Worth knowing that a second Claude session was working this same request in the same checkout at the same time and wrote `scripts/photo_gaps.py` for it; that tool is good and was adopted rather than duplicated, but two sessions on one task is the collision the in-flight claim exists to prevent.

## 2026-08-17 (session) - Walked the night-run ladder by hand to see where it fights a run, and it fought back four times

Hidde asked for a night run performed and watched. So the Step 0 ladder was executed in order, with notes on every point of friction. It never got past rung 2, which is the correct outcome and also the interesting one.

**Rung 2 held a real BLOCKER, and obeying it would have been wrong.** The fresh-eyes reviewer flagged Milan's Archdevil hackberry as published on the private grounds of an inhabited residence, against hard rule 10's absolute "not somebody's home" test. It was right to raise it. But the premise was a sentence WE wrote: the story said the villa's inner courtyard is "square, arcaded on three sides, and the hackberry stands at the centre of it", which no source says. A bridge claim, and as always the join decided the location. The Comune di Milano owns the villa and its own page says "e' possibile varcare il cancello per visitare il parco", the gate may be passed to visit the park, with the discretion due to an inhabited place. That is the landowner admitting visitors. The buildings are the home; the park is not. So the tree stays, with the permission quoted instead of paraphrased, and two location errors got fixed on the way: the address was Via Villapizzone 9 against the comune's piazza Villapizzone 3, and the pin sat 83 metres from the comune's own marker while claiming confirmed.

**That is now doctrine: a BLOCKER is answered, not obeyed.** The reviewer can only see what we published, so a finding built on our own invention inherits it. Written into rung 2.

**And a night run could not have done any of it.** comune.milano.it 403s every plain fetcher and is on the fetch blocklist for it. Only a browser session reaches it. So this BLOCKER would have sat at the top of the ladder blocking every knock, or a run would have cleared it by retiring a perfectly good tree. Rung 2 now says: a finding that turns on a blocklisted host is a session's job, and never clear one you could not verify.

**Three improvements shipped from the walk itself.**

`scripts/health.py`: rung 2 in one command, exit 0 or 1. It replaces four `gh run list` calls and three staleness thresholds held in the head, which is a check expensive enough to skip on a short window, on the one rung every run executes. It taught itself something in its first five minutes: the first version counted every line containing "BLOCKER", including the file's own legend and a sentence about yesterday's blocker being fixed, and reported three where there was one. It matches the reviewer's heading form now, verified against three days of review history.

`data/review-answered.json`: REVIEW.md is append-only and the next review is a day out, so six knocks would re-serve the same finding five times after it was fixed. `health.py --answer <date> "<note>"` closes it.

`passcheck.py` claim identity: **the lock could not tell two local sessions apart.** Every session claimed as the bare string "session", so `--brief <place> --as session` satisfied the holder check whichever session had actually claimed the place. It only ever guarded session against night run. That is the Padova collision it was built for, 89,000 tokens for nine stories written twice, with the local case uncovered. Sessions name themselves from CLAUDE_CODE_SESSION_ID now, and `--as` defaults to whoever we are.

**FOR HIDDE: there are three other Claude sessions live in this repository right now, all writing to the same working tree.** One has been running 22 hours. That is how the claim defect above got noticed: another session's half-finished photo-queue and Warsaw leads were sitting unstaged in my tree while I worked, and a careless `git add -A` would have committed somebody else's work in progress under my message. I left them alone and pushed only my own files. Nothing is broken and no work was lost, but this is a way of working, not a bug, so whether to keep running several sessions against one checkout is your call rather than mine. If you do keep it, the honest fix is a worktree per session; if you would rather not, one session at a time removes the whole class.

## 2026-08-17 - Night run 2026-08-17 05:26 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. No measurements available, ended clean (unknown). 19 tree(s) reached data/cities across 5 city file(s), and the run still wrote no log entry of its own. Claims left behind: vilnius, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-17 - Night run 2026-08-17 02:52 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 21.9 minutes of its 60 minute window, 193 turns, ended clean (success). 1 tree(s) reached data/cities across 1 city file(s), and the run still wrote no log entry of its own.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-16 - Night run 2026-08-16 23:14 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 6.6 minutes of its 60 minute window, 61 turns, ended clean (success). 4 commit(s), none of them a published tree.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-16 - Night run 2026-08-16 20:15 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 5.0 minutes of its 60 minute window, 65 turns, ended clean (success). 1 commit(s), none of them a published tree. Claims left behind: bratislava, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-16 (session) - A night run done by hand: the queue's cheapest work turned out to be six pages for one spot

Hidde asked for a night run performed live rather than described. Step 0's ladder, rung by rung.

**Rungs 1 to 3 clean.** No unprocessed submissions. Smoke green, digest 6.5h old, review 10h old, weekly-analysis 6.3 days (under the 8-day redispatch threshold, noted not actioned). REVIEW.md's newest entry carried a BLOCKER, Potsdam republishing two of Berlin's Pfaueninsel oaks under different names, and it was already fixed by the 07:29 run. Checked the fix rather than trusting it: both retired tree URLs still return 200 through `RENAMED_CITY_SLUGS` entries, so hard rule 3 held.

**Rung 4 is where it got interesting, and it produced a check rather than a city.** The actionable list pointed at Toronto: rank 14, four trees live, thirteen READY leads. Two things were wrong with that. **Six of the thirteen sat on the same coordinate**, spread 0 metres, one heritage designation (HT-2016-121) covering a group at one address and split into six rows on import. Writing them would have produced six near-identical pages for one place to stand. That is the second time in one session that READY did not mean verified, so by the standing ratchet it is now a check: `leads.py` folds entries within 15 metres into one candidate and reports them as STACKED. Site-wide it caught four groups, twelve leads, in Toronto, Brussels and Genoa.

**And Toronto's remaining leads do not form a walk.** Its four live trees already span 20 km and the leads scatter 4 to 40 km out; only two sit near each other (1.4 km apart, but 5 km from the nearest live tree). Toronto is finished at four for now under the 80/20 rule. With stage 1 holding nothing else cheap, stage 2 opened, and Barcelona, Munich and Seville all turned out to be **above target and finished**, leaving Rome and Milan with room for three trees between them. Too thin to dispatch.

**So the run went to the verify shelf and picked Krakow**, rank 62, four trees live, 811 register entries within 20 km of which 805 had never been judged.

**Krakow is now live at 10.** The verify pass found the key that made it cheap: Poland's GDOS register carries no age, no girth and no names, but Polish Wikipedia reproduces the municipal register list with address, girth and designation year, and its INSPIRE codes join straight to the register we already hold. That join gave real measurements for 115 of 155 candidates. It also caught two storm-felled monuments in the same table's own notes, a red beech at the Archaeological Museum (Feb 2022) and a horse chestnut on ul. Podzamcze (July 2021), both of which would otherwise have been strong candidates.

The six form a genuine loop on Planty, 250 to 500 metres apart, 1,194 metres end to end. The existing four do not join it and the page says so.

**One correction made in session, and it is the transferable part.** Four of the six ages are DERIVED from girth by a growth-factor conversion, twice using a proxy species. The verifier's notes were exemplary about this ("Age is DERIVED, not sourced... do not narrow further"), but the `age_estimate` field said "roughly 200 years", and that field renders as a standalone chip on the tree page where a reader reads it as a record somebody kept. Rewritten to "estimated 150 to 270 years, from its girth", matching the existing "roughly a century, unconfirmed" pattern. The two trees with no reliable growth factor, the ginkgo and the Turkish hazel, ship with no age at all and ask the reader, which is the right answer rather than a gap.

**Cost:** 55k verify plus 62k write for 6 trees, about 19.5k per tree including the page rewrite from 4 to 10.

**What this says about the tooling shipped earlier today.** The new "what you can actually move" list worked, and it is too credulous: it counts supply without asking whether that supply forms a walk or is even separate trees. Toronto read as rank 14 with 13 leads and the honest answer was zero.

## 2026-08-16 (session) - Geneva 6 to 14, Paris 25 to 30, and the brief generator learns to read

**Six cities and 35 trees today.** After four new cities, the last two were deepen passes chosen on demand rather than on rank: Geneva (55 impressions, 6 trees against a target of 20) and Paris (84 impressions, the highest of any page still under its target). Deepening a page people already find compounds; deepening one nobody finds was the measured waste of an earlier week.

**Before either could run, `passcheck.py --brief` had to be fixed, and this is the most valuable thing in the entry.** Geneva's brief printed 204 lines of "(unnamed)" with no species, no girth and no age, because the extractor knew only the field names `species`, `girth_cm` and `age_register`, and Geneva's register uses `species_latin`, `circumference_cm` and `planted`. That is the worst possible failure for this particular tool: the entire argument for a register-led pass is that those fields arrive free, so a brief that cannot print them turns the cheapest kind of pass into the most expensive one, silently, with nothing looking broken. It now reads species from eight spellings, age from eight, and girth from whatever unit the register published, converting diameter and dbh with pi. **Vitality is new to the brief and is the most useful of the four**, because it is the register answering "is it alive" without a single fetch.

**The date trap, found by probing before briefing, then held in both directions by the pass.** Geneva's `planted` field looks like a planting record and mostly is not: 22 entries carry exactly 1912-01-01, 5 carry 1962-01-01, the file already documented 1812-01-01 as a placeholder, and only 71 of 205 carry any date while 84 are flagged estimates. The rule handed to the pass was that any 01-01 date is an era rather than a planting, and a real month is likelier genuine because a placeholder does not pick a season. It then used 1966-04-01 and refused 1850-01-01, deriving that cedar's age instead by calibrating its 743 cm against our own Naville Cedar at a documented 722 cm and 206 years. Same species, same lake, better than any generic table, and the story says so outright. That is today's age ruling working without anyone restating it.

**Geneva's eight.** The Venerable Oak of the Botanical Garden leads: 710 cm, dated 1719 by a City of Geneva museum-trail article whose inventory number matches the register's digit for digit, growing 186 years before the garden moved in around it, with a quiet perimeter drawn around its roots. The Naville Cedar is the one with a person in it, planted in the summer of 1820 by the mayor of Eaux-Vives to mark his son's birth. And gen_014 keeps no age at all, because its planting field is empty and no growth figure for stone pines this far north held up: the page asks the reader instead.

**Paris's five open the 9th, 13th and 18th**, three of them 150 metres apart in Square Louise Michel below Sacre-Coeur. A refusal worth keeping: the Square Jean XXIII candidates stay leads, because that square has been shut since September 2023 for the Notre-Dame works, does not reopen before mid-2027, and an investigative piece documents another tree in it already felled during them.

**The writing pass read both live city files before writing over them and caught three things I would not have.** The service tree is not Geneva's youngest (the official chestnut already claims that at about 11 years), the Port-Noir cedar is not its largest (gen_003 is 762 cm), and par_032 arrived named "Common Plane" against 119 live London Plane entries.

**And the deploy failed once, on me.** Told about that species collision, I renamed par_032 to "London Plane (Platanus x hispanica)" to preserve the register's own binomial, without checking that the build's check runs BOTH ways. One edit made two clashes: it split "London Plane" across two scientific names against 120 live trees on acerifolia, and gave hispanica a second common name beside London's Baobab Group entry. Hard rule 9 names the pairing outright and the corpus was right. Fixed, redeployed, both pages verified live.

**Girth now sits on 33 published trees, from 13 this morning.** That is the point of the instruction added today, and it came almost entirely from registers that were already imported and simply not being read.

**FOR HIDDE:** nothing waits on you.

## 2026-08-16 - Night run 2026-08-16 11:11 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 16.7 minutes of its 60 minute window, 122 turns, ended clean (success). 11 commit(s), none of them a published tree. Claims left behind: krakow, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-16 (session) - Canada opens: Toronto and Montreal, 11 trees, and a city register nobody had found

**Four cities and 22 trees today.** Hidde asked for the next two in line after Vilnius and Tallinn, which after the night run's queue fix are Toronto at #17 and Montreal at #19.

**Montreal is the find, and it is not the trees.** The overnight ArcGIS sweep gave Montreal seven hits; I probed all seven before briefing anything, and five are false. The big 322-tree "arbres remarquables" layer is entirely in Otterburn Park, 27 km away, with no point inside 25 km of the city. Three more are full street-tree inventories the semantic filter excludes. What survived was six species names on a cemetery slope, and chasing those six led to **montroyal.montreal.ca, where the Ville de Montreal publishes a per-tree dendrological page with species, diameter at chest height and at the base, an age reading and a paragraph of history, for dozens of designated specimens across the mountain and both cemeteries.** That is a city register in webpage form, several pages deep, and essentially unmined. The Jardin botanique, Ile Sainte-Helene, Parc La Fontaine and a long tail of individually documented specimens are still sitting on it, and a follow-up pass there is confirm-and-pin work rather than research.

Six of the seven Montreal trees rest on that source alone and are flagged accordingly, which is the rule rather than an exception to it. **Every Montreal pin is approximate on purpose**: the source places a tree in a cemetery section or along a trail, never on a spot, so the findable detail went into the prose instead. Plot ND 7002-9030 for the McKenna maple, the chemin de la Foret gate for the yew, the Smith House margin for the elm, a stand of fifty-year-old spruce for the oak. That is what a vague pin looks like when it is doing its job rather than apologising.

**Toronto clears the floor and is honestly not a walk.** Four trees over twenty kilometres: Kew Gardens in the Beaches, Coronation Park on the waterfront, Long Branch, Islington. The page says so in its first line and the map shows four separate dots with no walking route, because there is not one. Compare Vilnius the same morning, six trees inside a kilometre. Both are real pages; only one is an afternoon.

**The girth instruction is already paying.** Six of seven Montreal trees and the Kew Gardens oak arrived with a girth, converted from published diameters. The whole database held 13 this morning. Every age on these two cities that is not documentary is read off one of those measurements and says so in the prose.

**Three catches worth keeping, none of them mine.** The Toronto pass found that five Echo Valley register entries share one identical coordinate, a site pin dressed as five tree pins, and marked its tree approximate rather than trusting it. The Montreal pass found a designated cemetery red ash dead, felled in 2025 to the emerald ash borer, because the city's own page for it now redirects to an address ending in disparu. And the writing pass caught two of its own inputs: the King's Oak arrived as "English Oak" and would have failed hard rule 9 against 64 live Pedunculate Oak entries, and a Kew Gardens claim about predating colonization does not survive the arithmetic, since 220 years from 2026 lands in 1806.

**One process failure, mine.** I hand-wrote three of today's four research briefs instead of generating them with `passcheck.py --brief`. The Toronto brief told the pass it was from-zero web research with no register behind it, which was false: 25 Ontario Heritage Tree Program candidates were already sitting in data/leads/toronto.json from an earlier scout. The pass found them anyway and it cost nothing this time, but it is exactly the false premise the generated brief exists to make impossible. Logged as `brief_wrong`.

**Cost for the day: roughly 1.1M tokens for 22 published trees**, about 50k each against a 15k target. The split is consistent across all four cities and worth reading rather than averaging: writing runs 10k per tree and is under target, verification runs 30 to 40k and is not. Every one of these four cities has a register with no age field, and a register that cannot answer "how old" turns a verification pass back into research. Registers that carry a measurement (Piemonte, Amsterdam, Otterburn Park) are a different economy, which is the argument for the girth work rather than for doing fewer cities.

**FOR HIDDE:** nothing waits on you here.

## 2026-08-16 (session) - Vilnius and Tallinn open, and an estimated age stops being a forbidden one

**Two cities live, 11 trees, both opened off a register rather than from zero.** Hidde asked which city I would want to make, and the answer came from the queue rather than from taste: Toronto and Montreal sit at #1 and #2 with no register behind them, which is the 556k-tokens-for-nothing route that Baarn measured. Vilnius sits at #3 WITH one, 37 designated trees inside 12 km and 20 of them within 1.3 km of the Old Town. Tallinn came along as the pair because a previous session had already scouted its 37 candidates and left the file untracked, which is the one thing the standing keep-everything rule forbids.

**Vilnius arrives as one walk, which is the whole point of the clustering doctrine.** Six of seven inside a kilometre, four of them in Bernardinai Garden. The garden's own oddity carries the page: a willow with nine trunks, a lime with four, an ash whose two official sources disagree over three or four. Both counts are on its page with the reader asked to settle it, which is cheaper and better than desk research. Five of the seven have no age at all, because Lithuania's register has no age field and nobody has dated them.

**Tallinn opens at the floor and the four earn it**: Kelch's linden at Niguliste, hollow and down to two branches at around 370 years, with a chronicler said to be buried under it; the ginkgo that beat a Soviet parade grandstand so publicly that Estonian has a phrase for a building plan stopped by a tree; a red oak in a manor park whose house burned in 1995; and two limes planted in 1883 for two hundred years of one family at Lai 29, living in what their own source calls a stone desert. The 33 rejects are the real finding and are on disk as leads: Estonia protects the horticulturally interesting, so its register is full of copper beeches and globe maples that are nobody's idea of a walk. Nobody needs to discover that twice.

**Hidde's ruling of the day, and it is now in three files rather than in a note: "leeftijd is geen blocker - we kunnen een estimation doen", then "en onthou dit voor alle toekomstige runs".** The line it draws is that an estimate is DERIVED and says what from, girth plus a growth rate or a documented planting date for the specimen; a number that merely feels right is still fabrication under hard rule 2. Estimates stay broad, because a century-wide band is the honest output of that arithmetic, and the park's own planting date is named as the bridge claim it usually is.

It went into CLAUDE.md, BRIEF_RESEARCH.md and BRIEF_WRITING.md, and the second of those is the one that matters: **a verify pass never opens CLAUDE.md by design, so a rule living only there would never reach the pass that actually decides this.** That is the "record it where it acts" ratchet applied to a corpus edit rather than to a script.

**The gap under the ruling is measured, not asserted: 92 of 1223 published trees carry no age, and 13 carry a girth.** Nothing can be derived from nothing, so girth is the missing input, and every pass now records `girth_cm` whenever a source gives it even when the tree already has an age. At a few hundred of them the estimating becomes a script that runs over all the undated trees at once instead of a judgement made one tree at a time. That is the next cheap unlock and it is not built yet.

**Cost, measured rather than self-reported.** Vilnius verify 133k for 7 trees, Tallinn verify 175k for 4, the shared write pass 116k for 11. Both verify agents under-reported themselves by more than half (55k against 133k, 145k against 175k), so the harness figure went into `data/agent-costs.json` instead. That matters for the meter: at roughly 39k per published tree this batch sits well above the 15k target, and the reason is visible in the split. Writing was cheap at 10.6k per tree, exactly as the batching predicts. Verification was not, because a register with no age, girth or species field turns "confirm this" back into research.

**Looking at the new pages with eyes, rather than at their build log, found three sitewide bugs that had nothing to do with Vilnius.** The worst: the SPANISH tree template ended its photo invitation with "y aparecerá en esta página con tu nombre", live on every photo-less Spanish tree page, promising exactly what was ruled out absolutely on 2026-08-11 on any channel. Our own /contribute page says in English that we never publish a name, so the site was contradicting itself and offering something we must not deliver. A promise is worse than the act, because it invites somebody to send a name expecting it to appear. That class has now failed twice, which is the ratchet's threshold, so it ships with `check_no_name_promise()` in qa.py, greping the BUILT pages rather than the templates. Photo credits are deliberately not caught: a CC BY licence obliges that name and the photographer chose it knowingly.

The other two were cosmetic and equally invisible in a diff. The age chip used `??`, which passes an empty string straight through, so any tree whose `age_estimate` is `""` rendered a grey pill with nothing in it; five of seven Vilnius trees have no age, which is how it surfaced after sitting there for who knows how long. And both templates had lost the space before "Send us yours", so 881 photo-less tree pages read "we can use.Send us yours". All three fixed, deployed and confirmed on the live site, the first by curl and the last two by looking at the rendered page at 375px.

**FOR HIDDE:** nothing waits on you. One judgement call worth your eye: vln_002, the Daukantas memorial oak, is about 47 years old and I kept it, because the city protects it, it sits on the walk, and its reason is historical rather than botanical. Its story opens on the memorial and never implies age it does not have. Say the word if you would rather it went to leads, it is a one-line change.

**Correction to the entry below, and it changes what that entry means.** It reported "63 of 121 published cities took zero impressions". That number came from `impressions_10d` in data/city-queue.json, and that field was not measuring what everything downstream believed. The digest pulled Search Console's page dimension with `rowLimit: 200`; that API sorts by clicks descending; the whole site takes about 90 clicks in a ten-day window, so roughly 40 pages have any clicks and the other 160 rows went to zero-click pages in an order Google does not promise. **Every page past the cut was written into the queue as zero.** So the honest reading of that 63 is "did not appear in the top-200 readback", not "was never shown to anyone".

**It had been contradicting itself in its own output.** The 2026-08-16 digest printed `/cambridge/newtons-apple-tree` at 22 impressions in its seen-not-clicked line, which reads the `pairs` pull, and wrote `cambridge = 0` into the queue in the same run. Nobody caught it because nothing about a zero looks broken. Same class as yesterday's sendBeacon bug, one day apart: an instrument reading zero, and a zero you cannot tell from the real thing. Raised to 5,000 rows, which covers all 1,626 URLs against the API's 25,000 ceiling.

**This was steering real work, not just a report.** `promote()` scores a city from that number, `rescore.py` ranks on it, and CLAUDE.md's depth rule reads it to decide where photos and pins are allowed at all. A city cut off by the row limit looked identical to a city nobody searches for.

**What survives the correction, and it is the part that matters:** the constraint is still indexation. That conclusion rests on the 346 URLs at "Discovered - currently not indexed", which comes from Search Console's own coverage report and is not truncated by any of this. London at 28 days live with 24 URLs and not one of them in the top 200 is still strong evidence, just not proof of a literal zero.

**AI findability, asked the same session, and the answer is mostly that we cannot see it.** Nothing blocks the assistants: robots.txt allows all, and GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot and bingbot were each given a live fetch of /london and each got 200. But the site is served straight from GitHub Pages with no proxy in front, so there are **no access logs at all** and a crawl by any of them leaves no trace we can read; Cloudflare Web Analytics is a JavaScript beacon and bots do not run JavaScript. The only measurable signal is a human clicking a citation, and the referrer pull was `limit: 5`, so with direct, ourselves, google and the DPG proxy holding those slots the first arrival from ChatGPT would have been invisible. Now 25, with the assistants on their own named line. Across all of DATA.md the count is zero, and it now stays a line that says so rather than an absence.

**What was NOT built, deliberately.** IndexNow would automate submission to Bing and Yandex and would end the manual clicking on that half, but Bing is the index behind ChatGPT and Copilot and we currently have no idea whether it holds us at all. Building a submitter before knowing whether the thing it feeds is empty is the wrong order. Bing Webmaster Tools answers it in five minutes and is Hidde's to create.

**FOR HIDDE:** `data/index-requests.json` records the ten URLs you submitted by hand today with what each was earning at the time, and the twenty comparable cities left alone as a control. `python3 scripts/indexcheck.py` reads it against the queue and prints a verdict; it says "too early" until roughly 2026-08-23. That is the answer to whether it was worth doing, and it exists so nobody has to reconstruct it from memory.

## 2026-08-16 (session) - The SEO audit says the titles are fine and half the site has never been crawled

**Asked to find what to improve about SEO, and the first finding contradicts the premise we started from.** The theory on the table was that pages ranking on page one and taking no clicks are a title-and-snippet problem. Scored against normal-CTR-for-position, using the digest's own table, the site takes **63 clicks on 1,625 impressions where its positions predict 38**. We are 25 clicks a fortnight ABOVE par, not below. Five pages sit under par at all (Bath, Bologna, Barcelona, Budapest, Boston) and rewriting every one of them recovers 6.4 clicks per ten days, on samples of 43 to 95 impressions where that is inside the noise band. Sixteen of the 34 pages that earn impressions average position 15 to 31, and no title fixes page two. So the titles were deliberately left alone, which is the opposite of what this session set out to do.

**What the numbers actually say, and it is much larger.** Of 121 published cities, **63 took zero impressions in the ten-day window, holding 523 trees, 43 percent of everything we have ever published.** Thirty of those have been live 14 days or longer, which is past the point where being new explains it. London is the worst case and it is not close: 23 trees, 28 days live, the highest travel demand of any city on the queue, and it has never been shown to one person. That is the 346 "Discovered - currently not indexed" pages from yesterday's entry, measured from our own side rather than read off Search Console.

**Technical SEO was audited and is clean, so nobody should spend a window re-checking it.** Canonicals correct on every page type; hreflang reciprocal and correct on the Spanish Malaga set; schema rich (ItemList, TouristAttraction, FAQPage, BreadcrumbList); sitemap flat with real source-based lastmod; every sampled zero-impression city returns 200 and is linked from /cities; titles 49 to 54 characters and descriptions 134 to 154, all unique; question pages 386 to 435 words with distinct question-shaped titles, so they are not cannibalising the city pages. The problem is authority and crawl budget, and neither is a page-level fix.

**What was actually built, being the one item on the list a session can do alone: three third-party hosts are off the critical path.** The beacon reports p90 page load of 5.2 seconds while our own server answers in 140 milliseconds with 49KB transferred, so the gap was never the server. Gabarito was a render-blocking `<link>` to fonts.googleapis.com which answers with CSS pointing at a file on fonts.gstatic.com, so two fresh DNS lookups and two TLS handshakes stood in front of first paint on a site where 72 percent of search clicks arrive on a phone. Both woff2 subsets are now vendored with Google's unicode-range split intact, so a reader in Bath fetches 34KB and never touches the 12KB latin-ext. MapLibre left unpkg.com the same way: identical v4.7.1 bytes from our own origin, which also ends a third party receiving the IP of every visitor to every page with a map while the privacy page says we run no third-party tracking.

**Verified on the live site, not from the build log.** Smoke test green, deploy green, then Vienna at desktop and 375px: `document.fonts.check('700 24px Gabarito')` true and the h1 computing to Gabarito, map canvas constructed, all four assets 200 with correct content types, and unpkg, fonts.googleapis.com and fonts.gstatic.com all gone from the rendered HTML.

**One honest limit on that check, recorded because it looks alarming and is not ours.** The preview browser paints no basemap tiles: MapLibre initialises, sprites and glyphs load, pins and attribution render, and zero vector data tiles are requested. Loading unpkg's identical copy into the same page reproduces it exactly, so it is the sandbox blocking the blob-URL worker that fetches tiles, not the vendoring. It does mean the basemap itself was confirmed by equivalence rather than by eye, and a real browser should be glanced at next time somebody has one open.

**FOR HIDDE:** the Request Indexing submissions, still the highest-value ten minutes only you can do, now with the list computed rather than guessed. Thirty cities are 14-plus days live with zero impressions; ranked by demand times trees, the ten to paste are london, venice, istanbul, florence, milan, copenhagen, madrid, naples, malaga, seoul.

## 2026-08-16 (session) - 40 outreach mails to the people who answer, in his own words

**Batch 005 is out: 40 mails to tree societies, city tree groups and blogs across eight countries.** The recipients are the finding rather than the work. Reading the first 57 mails back: 8 replies, which is a 14 percent reply rate and high for cold mail, but every useful one came from a named person who cares about trees personally (Paulo Araujo, Wolfgang Schuermann, Jon Pattee, Piet van Dijck). The 40 that went to gardens, palaces, parks departments and ministries produced near silence, and a municipality does not link out anyway. So this batch contains no institution that manages ground.

**The mail is his, not mine.** He wrote it in Dutch in session after rejecting two versions of mine, and it is shorter than anything I would have written: what the site is, one link, one personal question, out. My half was the rendering into Dutch, Portuguese, Spanish, Catalan, Italian and English, the counts read live from the city files, and knowing which claims are safe to make. Third time this division has produced the right mail in one pass, exactly as HIS_VOICE.md says.

**Two of his corrections became mechanisms rather than notes.** Remarkable is "opmerkelijk" in Dutch and never "ongelofelijk", now a check in `scripts/mailcheck.py` so no future draft can carry it. And the photograph ask is gone from first contact ("laat maar die fotos kunnen we altijd in een tweede mail vragen"): a stranger's first mail asks one thing.

**What the batch says that is true and specific:** each recipient's own city with today's tree count, their own page, and for ICNF one sentence about an error in their own register (three Setubal olives carrying 2009 in the age column), which is the only thing in this batch we give rather than ask. The "this tree of yours" claim survives only for Fondazione Villa Ghigi, who actually manage their park.

**Still zero.** No referring domain above DR 10 that a human made, five days after the first 57. The one external referrer on record remains DPG Media's corporate proxy, which is journalists reading the press mail. Reply lag on this lane is weeks; the Utrecht placement that batch 001 produced lands in the first half of 2027.

**And the day's real finding, which came out of asking whether to post on Reddit.** Every funnel event has been silently dropped since launch. `at.track()` sent them with `navigator.sendBeacon` carrying a Blob of type `application/json`, which is not a CORS-simple request, so the browser must preflight it and sendBeacon cannot; the request dies and sendBeacon still returns true, so nothing could observe the failure. Measured on the live site by resource timing: the same insert by fetch returns 201, the beacon returns status 0. Proof it was never user behaviour: on 08-14 a real waitlist signup landed in the waitlist table, written by fetch, while its `waitlist-submit` event fired one line earlier by the beacon never arrived. Same click, one worked, one did not.

So `directions`, `walk-open`, `walk-start`, `save` and `app-cta` did not read zero because nobody clicks. They read zero because nothing was written down, and every conclusion drawn from those zeros over the past weeks was drawn from a broken instrument. Fixed in f240bc2 (always fetch with `keepalive: true`), deployed, and verified on the live Amsterdam page rather than from the build log: no `navigator.sendBeacon(` call remains and a real `at.track` returns 201. Two rows named `beacon-test` and `beacon-fix-verify` in the events table are mine, from this diagnosis.

**What it changes about posting.** Hidde asked whether Reddit and Facebook are worth doing now, since neither gives a backlink, and answered his own question: we already have a small supply of users to test with. He is right, and the reason is stronger than he put it. The site takes ~270 visits a week, which is enough to measure a product with; what was missing was never audience, it was a working meter. Posting into a funnel that records nothing would have burned the one first impression a community gives you and taught us exactly what we knew. Drafts for both channels are ready in `drafts/social-posts.md` and wait for the first few days of real numbers.

**FOR HIDDE:** nothing waits on you from this. 66 of the 106 verified addresses are still unmailed and are almost all gardens, parks and municipalities, deliberately skipped. The next lane worth its window is press desks for the six cities that actually earn impressions (Palermo, Amsterdam, Rome, Prague, Barcelona, Vienna), which needs a named journalist per outlet rather than a list. Reddit is parked until tomorrow on your word.

## 2026-08-16 (session) - Brisbane and Poznan close to target; 64 trees get a real best_time; Brno and Wroclaw verify passes in flight

7-day visits (`visitors.py`): 262 total, 28/83/41/21/17/34/33/5 across 08-09 to 08-16, softest day of the week today so far. `prepare.py` showed 23 cities already staged for verify and one stale empty `guimaraes-verified.json`.

Step 0: submissions clear (checked directly against Supabase since `SUPABASE_URL` wasn't in env, used the hardcoded URL from `daily_digest.py`; all 4 rows already in `data/submissions-processed.json`). Rung 2 (site health) already clean per this morning's earlier session entry (smoke test, data digest, fresh-eyes review and weekly analysis all recent and green); did not re-check, trusted that entry. `pagegaps.py`: nothing owed.

**Tried the cheap end (rule 1a) first and found it mostly unavailable right now.** `leads.py --ready` reports 186 READY leads, but hand-checking a sample across Poznan, Zaragoza, Brno, Wroclaw, Aarhus, Rome and Sorrento found nearly every one still carries a real open question in its own `why` text ("not verified this pass for time", "access unconfirmed", "held back only because...") that the classifier's readiness check (name+species+position only) doesn't read. This is the exact bug the 2026-08-13 and 2026-08-16 LOG entries already flagged and partially patched (`HELD_MARKER`); that fix only catches one specific phrasing convention, not the much more common "not verified this pass" hedge (154 hits in the corpus). Did not attempt a general fix this session (tried a regex sweep, it only caught 12 of the sampled false-positives, judged too unreliable to trust blindly); left as a note rather than a further build check.

**So moved to rule 1b, register-backed verify, on two of the cheapest gaps.** `city_queue.py --next`: Brisbane (8 live, gap 2, 188 register candidates) and Poznan (6 live, gap 4, 2004 register candidates) were the smallest gaps with real supply. Claimed each, dispatched the `verify` agent. Brisbane's register turned out to be bare coordinates with no species (useless alone); the agent used the same National Trust of Australia source as the existing 8 and delivered 2 clean trees (Mahogany of Commerce, Tamarind Tree), both inside the existing 1.1km cluster. Poznan's GDOS register entries also came back bare (CRFOP detail pages 403 to automated fetches, an Incapsula bot-check), but the agent finished 4 stale leads an earlier pass had found and named but not verified: two Cytadela Park oaks named for opposing 1945 battle commanders, a strikingly thick Park Wilsona plane (484cm at ~100yr, flagged rather than resolved), and Krzysztof, a Wilda district oak on a fenced-but-public municipal playground dated 250-300 years, **which becomes Poznan's new oldest and hero tree**, about a century older than the previous record holder.

Merged both in session: wrote 6 stories (2 Brisbane, 4 Poznan) matching each city's existing voice, updated intro/meta/FAQ/oldest_tree_id off the new counts, trimmed two fields that came in over their SEO_GEO_BLUEPRINT.md word caps. Brisbane's walk computes as one route, all 10, 2.2km/29min. Poznan's walk builder still only groups its biggest cluster (6 of 10, 1.6km/21min, same pattern as Rome's multi-cluster page already in production), so its FAQ says plainly that the other four are separate stops. `preflight.py`, `superlatives.py` clean on both; `qa.py`'s one failure is this sandbox's pre-existing shallow-clone sitemap-lastmod warning (3-commit checkout), not a new issue.

**Free work alongside:** ran `photo_hunt.py --recheck` (queue now 840 trees swept, 441 with at least one open-licence candidate, up from before this session; still needs a session that can reach Wikimedia to judge). Cross-referenced every tree in DATA.md's 19 depth-allowed cities against `data/phenology/`, which already records species-level "striking"/"worth the trip" seasonal moments with written labels; found 64 already-published trees with no `best_time` set despite their species file recording a real peak. Filled all 64 in directly from the phenology data, no research, no invented facts (a first pass round-tripped the JSON through Python's serializer and silently normalised every coordinate's trailing zeros across whole files as a side effect; reverted and redid it as a targeted text insertion instead, so the real diff is four lines per tree, nothing else touched).

**Then claimed Brno (gap 3) and Wroclaw (gap 6) for further verify passes**, both with real register supply (30 and 347 candidates) and 2-4 stale leads each an earlier pass had found but not finished; dispatched, running at the time of this entry. Will merge in a follow-up entry.

`tree_index.py` run after each merge (41681 trees tracked in the database). `data/agent-costs.json` logged for all passes this session, including the two zero-token session merges and the best_time pass (tokens not metered by the harness for in-session work, recorded as 0 rather than leaving the day silent per the convention).

FOR HIDDE: nothing blocks. Worth knowing: `leads.py`'s READY classifier is still unreliable enough that hand-checking each candidate's `why` field is currently cheaper than trusting the count; a real fix needs something closer to reading intent than pattern-matching a handful of phrases.

## 2026-08-16 (session) - Fixed the fresh-eyes BLOCKER: Potsdam's two Pfaueninsel oaks were Berlin's, live twice

7-day visits (`visitors.py`): 28/83/41/21/17/34/33/5 across 08-09 to 08-16, 262 visits, 422 page views.

Step 0 rung 2 (site is broken): REVIEW.md's 2026-08-16 review flagged a BLOCKER before any new-coverage work started, so that came first. Confirmed it directly against both city files: Potsdam's pot_005/pot_006 (the two Pfaueninsel oaks) are the same physical trees as Berlin's already-published ber_012/ber_011, same register ids, coordinates 10-15m apart, same sources; Potsdam's own FAQ already admitted these two were "not actually in Potsdam". Retired pot_005/pot_006, rewrote Potsdam's copy off the six-tree count (now 4, exactly the never-cuttable floor), folded both into `data/leads/potsdam.json`'s blocked list, and added a cross-city redirect so the old URLs resolve to Berlin's pages instead of 404ing (hard rule 3). Also added `check_cross_city_duplicates()` to `scripts/preflight.py`, the toolchain gap the review named: a 60m cross-city coordinate sweep, same shape as the existing id-prefix check, so a same-trunk collision fails preflight next time rather than needing a human review to catch it. Ran it against the whole corpus: no other collisions. Full detail in CURATION.md's 2026-08-16 entry.

Checked and reader submissions (rung 1) were clear: all 4 rows in the Supabase `submissions` table are already in `data/submissions-processed.json`. Checks clean: Smoke test (green, 2026-08-16 07:02), Data digest (green, 05:44), Weekly analysis (green 08-10, within the 8-day window), Fresh-eyes review (green, 06:56, same run that filed the BLOCKER above).

`npm --prefix site ci && npm --prefix site run build` succeeds (1623 pages). `python3 scripts/qa.py`: 1 unrelated failure, every sitemap URL sharing one lastmod, caused by this checkout only holding one git commit (shallow history in this sandbox), not by this change; `python3 scripts/preflight.py` and `python3 scripts/superlatives.py` both pass clean. Ran the free `scripts/photo_hunt.py` API sweep twice (80 photo-less trees checked, many new candidates queued for a viewing pass elsewhere, since this runner's egress proxy blocks the image hosts), also `python3 scripts/pagegaps.py` (nothing owed: 0 missing species/country/park pages).

**Then moved to new coverage.** `python3 scripts/city_queue.py --next`: Guimaraes (6 live, target 10, gap 4) had both a `ready` count and register supply. Claimed it, dispatched a verify pass on the full generated brief. Result: zero new trees. All 23 unmined register candidates matched, by coordinate, to trees already published or to the already-blocked Casa da Penha arboretum inventory; the two leads an earlier pass had flagged "genuinely remarkable" (Casa de Margaride's rare camellia cultivars, Casa da Covilha's 300-year camellia) were re-checked in depth and both still fail hard rule 10's access test, guided-tour-only with no standing public hours found anywhere. This is exactly the failure shape the 2026-08-13 LOG entry warned about ("the leads.py READY count needs a health warning": Guimaraes was one of the cities named as misclassified that day), now confirmed a second time. Both stay leads with dated notes; claim released. Full detail in CURATION.md.

**Fixed the root cause, not just Guimaraes.** Checked whether Braga's two Tibaes READY leads were the same shape before dispatching anything: both read `status: "lead"` but their own `why` text says "HELD ON ACCESS, not on evidence" (the Tibaes monastery cerca is closed for works, no end date). This is exactly the bug the 2026-08-13 LOG entry named ("leads.py's READY count over-counts... not urgent, flagging so a future pass does not burn a window on the same discovery") and exactly what just cost Guimaraes 109k tokens. Fixed `scripts/leads.py`'s `classify()`: a new `HELD_MARKER` regex reads the lead's own `why` text for the "HELD ... on access/evidence/the day-trip boundary/transport" convention this project's passes already write, routing those to BLOCKED even when the `status` field was never updated to match. Deliberately narrow and checked against the whole corpus before writing it: catches 5 real cases (Braga's two, Como's Museo Giovio plane, Guimaraes' two transport-blocked pines) with zero false positives on the two traps found while building it (Barcelona's "Held on count and age, not access", a reason CLAUDE.md's own never_blocking list forbids; Toulouse's "held in spring, announced on...", unrelated prose about open-day scheduling). `python3 scripts/leads.py --city guimaraes` and `--city braga` now both correctly show 0 READY instead of 2 each.

Net for the session: one BLOCKER fixed and pushed, one honest zero-yield verify pass logged rather than hidden, and the tool that caused the wasted pass fixed so the next city doesn't repeat it. `python3 scripts/tree_index.py` not needed again (no city file changed since the last run).

## 2026-08-16 - Night run 2026-08-16 05:55 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 5.4 minutes of its 60 minute window, 46 turns, ended clean (success). 2 commit(s), none of them a published tree. Claims left behind: bari, taormina, catania, aarhus, sorrento, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-16 - Night run 2026-08-16 03:27 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. No measurements available, ended clean (unknown). 17 tree(s) reached data/cities across 3 city file(s), and the run still wrote no log entry of its own. Claims left behind: warsaw, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-16 - Night run 2026-08-16 02:14 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 3.8 minutes of its 60 minute window, 35 turns, ended clean (success). 2 commit(s), none of them a published tree. Claims left behind: brisbane, sorrento, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-15 - Night run 2026-08-15 22:49 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 12.0 minutes of its 60 minute window, 60 turns, ended clean (success). 2 commit(s), none of them a published tree. Claims left behind: bucaco, cordoba, which block the top of the queue until they expire.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported. What it cannot tell you is WHY the run stopped: the transcript is hidden on purpose, the repo being public. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-08-15 (session) - 7-day visits: 295, up from a slow week. Aarhus opens; Brisbane's 558-tree register goes to verify

7-day visitor line from `visitors.py`: 44/28/83/41/21/17/34/27 across 08-08 to 08-15, 295 visits total, 475 page views.

**Aarhus is live with 7 trees**, off the Dansk Traeregister, the research a prior session left verified but unwritten (`data/research/aarhus-verified.json`, claimed and released this session). Five cluster in and around Moesgard Museum's park: Denmark's very likely largest wild service tree (filed twice in the register, same coordinates, folded into one entry), a 40.5m silver fir over a family cemetery, a hornbeam, a black locust with a dying crown on an artificial mound, and a beech nicknamed the Happy Pig about 1.3km north in Skade Skov. The other two stand apart: the Women's Oak of Viby, planted in 1916 by the local women's suffrage society to mark Danish women's first vote (with a register date-arithmetic error caught and corrected, anchoring on the 1916 planting year rather than the register's own contradictory "110 years as of 2008" note), and a roadside oak on Elmehojvej protected by Danish law since 1965, undated but the best oldest-tree candidate on the page. Cost: 187k verify (an earlier session) + 62k write (this session) for 7 trees, ~35.6k/tree, over the 15k target because it's a small city (7 trees) carrying a research pass's fixed cost.

Along the way, closed a hard-rule-9 conflict the write pass flagged: Copenhagen's "Common Hornbeam" and Aarhus's new "Hornbeam" are now one canonical name (the shorter, neutral form). Deleted two stale `melbourne-*-verified.json` research files left over from this morning's Melbourne merge (already published, `passcheck --pending` flagged them as stale).

**Closed the one page gap `pagegaps.py` found:** a Sessile Oak species page (4 trees: 3 on Pfaueninsel in Berlin/Potsdam, 1 in Groningen), written directly from those trees' own facts rather than a pass, 0 tokens.

**Dispatched, still running at session end:** a verify pass on Brisbane's 558-tree significant/landscape-trees register (rank 15, high-income tourist city per this morning's rescoring), claimed and pushed. Will report and merge next session if it doesn't finish first.

Both `sitemap.xml`'s single-lastmod QA warning is a known shallow-clone artifact of this sandbox (`git rev-list --count HEAD` returns 3), not a content problem; not something to fix here.

## 2026-08-15 (session) - Melbourne opens Australia, the focus narrows to high-income destinations, and Hobart's calendar was six months wrong

**Melbourne is live with 8 trees**, the first Australian mainland city. One strong walk of six through Fitzroy North, Clifton Hill and Carlton North (Edinburgh Gardens, Darling Gardens, Curtain Square), plus two trees in Yarra Bend Park that are honestly a separate outing six or seven kilometres away, and the page says so rather than implying one route. Cost 9.8k tokens per published tree, under the 15k target, because the register did the finding.

**The verify pass earned its keep by refusing half the data.** Boroondara's `girth_m` column is bimodal: 107 values are real metres, 194 are centimetres wearing a metre label, and there is a clean gap between 8 and 68 with nothing in it. It used none of the 314 entries rather than guess, which was right. The rule and the warning now live in the register file itself as a `data_quality` block, so those trees are usable by the next pass instead of quietly poisonous. Same class of error as the ICNF import that once turned a 2.84 metre trunk into 2.84 centimetres.

**A real bug it found on the way, live on Hobart since it shipped.** `phenologyFor()` guarded the tropics with `Math.abs(lat)` and then computed the month shift from the RAW latitude, so every southern-hemisphere tree was read as a warm northern one: Melbourne at -37.8 drew a calendar six months out, bare in July when a Melbourne elm is in full leaf. Fixed: southern trees shift the whole calendar half a year, then take the same warm-or-cold nudge. Verified in the browser on the live Hobart page rather than from the build log, at desktop and 375px: the curve now troughs through June to August and peaks at both ends of the year, which is the southern winter, and it was the exact inverse before. Northern cities are untouched. Only Hobart and Melbourne are affected; everything between 25S and the equator prints no calendar at all, by design.

**The focus narrowed, on two instructions minutes apart:** "Let's keep India out of the top 250 for now" and "I want to focus on cities for rich tourists". Implemented on the World Bank income classification rather than a hand-picked list: high income full weight, upper-middle half, low and lower-middle paused. 19 unpublished cities left the list, biggest first Ho Chi Minh City, Marrakech, Delhi, Ubud and Siem Reap. Paused is not deleted, no published city is ever unranked this way, and lifting it is deleting a line from one table. The cost is real and is written down rather than hidden: several of those are places the product would serve well.

**A fix worth knowing about, because it nearly cost a window.** `passcheck --brief melbourne` said "no coordinates known" for a city with 202 register trees inside 12 km, which would have sent the pass into from-zero web research. Cause: it locates a city by matching register locality fields, and Melbourne's registers file everything under suburbs, so the word Melbourne appears in none of 546 rows. It now falls back to our own coordinate table. The brief went from 0 candidates to 546. Same class as the Genoa/Genova miss, except that one was a name and this one is a hierarchy.

## 2026-08-15 (session) - The queue was ranking on fame, and the registers were quietly writing the roadmap

Hidde, on being shown the city list: "I don't think Wikipedia impression gives a good representation of English tourist can't we make our top 250 smarter?" He was right, and the question turned out to be answerable rather than arguable, because the queue already carries `impressions_10d` per city from the Search Console readback. That is 55 published, indexed cities where we know what our pages actually earn, which makes any proposed proxy testable.

**Measured, Spearman against our own impressions:** English Wikipedia pageviews +0.23 (what the queue used), English Wikivoyage pageviews **+0.33**, English share of pageviews +0.11.

**Three changes, all committed.**

1. **Demand is travel intent now.** `scripts/travel_demand.py` resolves each city to its Wikivoyage article through Wikidata sitelinks and writes a `travel` column; `scripts/rescore.py` recomputes score, basis and rank from it. Someone reading a Wikivoyage article is packing a bag; someone reading Wikipedia is settling an argument.
2. **CITY_QUEUE.md's founding rule is withdrawn.** It was built on "the more famous a city is, the worse we do there", drawn from ten cities in a digest. On all 111 published cities it does not survive: impressions per 100k travel views run 206 / 224 / 184 across demand thirds, and clicks run 12 / 23 / 33, which points the other way outright. Predicted yield is flat now. We stopped penalising fame and deliberately did not start rewarding it, because the click counts are small and half the site is unindexed.
3. **His anglophone hypothesis was tested and failed**, and is written down as failed so nobody proposes it again. Published anglophone cities earn 1.33 impressions per tree against 1.43 everywhere else, a wash, and our six best pages are all in countries that read about themselves in their own language.

**The finding underneath, which matters more than the proxy.** We hold 37,543 register trees, but 27,000 of them sit in Poland, Germany, Italy, Czechia and Spain. That is why the machine kept opening Poznan, Brno and Potsdam: it was eating whatever was free, and **supply availability had quietly become strategy**. Nothing in the corpus was catching it.

**Acted on it the same session.** A scouting pass on the two highest-demand countries with zero coverage imported **Melbourne 546** (Yarra and Boroondara), **Brisbane 558** and **Ottawa 166** (NCC), all CC BY or Open Government Licence, at roughly 0.05k tokens per tree against 27k for research from zero. It also closed the question honestly: Toronto, Montreal and Vancouver publish full street-tree inventories but no designated register, so **Canada is thin beyond Ottawa and Quebec City**, while Australia is the real unlock. Brisbane (rank 17) and Melbourne (rank 28) are now the only cities that are both high-ranked and cheap, and they are where the next passes should go.

**Also merged this session:** the five cities the night runs and write passes had left half-landed. Brno 6, Potsdam 4, Poznan 6, Wroclaw 4, Quebec City 6, the last of them the first Canadian page. All five live and verified, claims released, costs logged. Quebec City's page states in the open that attaching La Presse's "oldest tree in the park" claim to our largest registered red oak is an inference from size and not a named match, which is the bridge-claim rule catching itself.

**FOR HIDDE, unchanged from yesterday and still the highest-value thing only you can do:** the ten Request Indexing submissions in Search Console. 346 pages sit "Discovered - currently not indexed", and that is now distorting the queue itself, not just the traffic: London, Edinburgh, Portland, Hobart and Quebec City are scored at 0.25 for never having been crawled rather than for failing. Second: **Sydney's Register of Significant Trees, 2,504 trees, is blocked purely on licence** and a draft ask is now waiting in `drafts/permission-us-registers.md` alongside the three American ones.

## 2026-08-15 (continued) - Four night runs quit after nine minutes and nobody could see it, so the workflow now measures itself

Hidde asked how the night runs had gone. The answer took an hour of reading `gh run view --log` by hand, and that is the finding rather than the anecdote.

**What the runs did.** Seven cron knocks between 20:56 and 07:20 UTC. Three produced cities (Cagliari, Braga, Perugia, then Trento, Guimaraes, Nara, then the 02:07 run which used its full 60 minute cap for 22 trees across Alicante, Palma, Trento, Bucaco, Trieste, Padua, Parma and Ferrara plus three page-gap intros). The other four ran 8 to 11 minutes of a 60 minute window, ended with `is_error: false` and `subtype: success`, published nothing, and wrote not one line here. They stopped themselves; nothing cut them off. One of them claimed Cordoba, Milan, Lucca, Genoa, Naples and Vienna for a write pass, wrote nothing, and left the top of the queue locked until noon.

**Why it took an hour to find out.** From the repository those four runs are indistinguishable from runs that never fired. The prompt has told every run since 2026-08-13 to append to LOG.md above all when it shipped nothing, and a run that gives up is precisely the run that skips that instruction. That is the second day this exact failure has been recorded (the 2026-08-13 Como run: 54 turns, one claim commit, silence), so by the standing ratchet it stops being a rule and becomes a check.

**Built.** `nightly.yml` gains a `Run health` step that runs after the agent whatever happened, reads the SDK's own result record, and commits `data/run-health.json`: minutes, turns, commands the allowlist refused, trees that reached `data/cities`, and claims left behind. When the run wrote no LOG.md entry, `scripts/run_health.py` writes a stub one in its place. Verified against the real 05:53 run by replaying its numbers over its actual commit range: it produces "10.6 minutes of its 60 minute window, 49 turns, 10 commands refused by the allowlist, ended clean, 1 commit, none of them a published tree, claims left behind: bari, cagliari, catania, cordoba, milan, lucca, genoa, naples, vienna."

**The number nobody knew.** Every run has commands refused by the allowlist, between 4 and 25 of them, the good runs included. At 10 refusals on 49 turns that is a fifth of a window spent hitting a wall, and which commands they are is unknowable from here. The transcript stays hidden deliberately (public repo, reader submissions pass through these runs), so the count is the way in; three nights of records should say whether widening the allowlist is worth doing and where.

**Claims expire per holder now.** A night-run claim dies after 90 minutes instead of four hours, and the number is derived rather than chosen: `timeout-minutes: 60` kills the job, so a night-run claim older than 90 minutes cannot belong to a live pass. Sessions keep their four hours, because a session legitimately pauses. Under the old rule this morning's dead claims blocked six cities until noon; under this one they would have cleared by 09:30. Tested both directions.

**Not done on purpose.** The cron schedule is untouched. Nine knocks a day may well be the wrong shape, but changing it before knowing why four of them quit after nine minutes is guessing with his usage window.

## 2026-08-15 (continued) - Bergamo reaches 8, and Como stays exhausted at 9

New session. `python3 scripts/visitors.py`: 271 visits, 448 page views over the last 7 days (83 on 2026-08-10 remains the best day, this week trending down). `python3 scripts/prepare.py`: 16 cities staged for verify, 0 awaiting a writer (the pipe was already cleared by earlier sessions today). Step 0: `SUPABASE_SERVICE_KEY` is present in this session but `SUPABASE_URL` is not, so submissions stayed unreadable, treated as absent per the rule. REVIEW.md's 2026-08-15 entry held nothing at BLOCKER or WARN. Smoke test green, data digest and fresh-eyes review both within the last few hours, weekly analysis within 8 days: nothing to dispatch. `passcheck.py --pending` empty, so rule (a) of "the course after the fortnight" had nothing to do; moved to rule (b), register-backed verify on gap-1/small-gap cities from `city_queue.py --next`.

**Sintra** (rank 7, gap 5): claimed, briefed, found nothing new. Every near-in register candidate is either already blocked (the private Quinta do Castanheiro chestnut, the Colares plane avenue) or 9km+ away, too far to join the existing 3.1km cluster. This matches the 2026-08-14 finding exactly; released the claim without shipping, no re-litigation needed since nothing had changed.

**Como** (rank 47, gap 1): claimed, dispatched a verify agent against 7 register candidates the brief called "never checked." All 7 turned out to be the same physical trees as entries already blocked/held (Villa Saporiti, Istituto Ugo Foscolo, Villa Erba, Museo Giovio), just reached via different MASAF sheet numbers than previously cited, because the blocked/held leads stored sheet ids but no coordinates so a coordinate dedupe couldn't recognise them. Fixed that gap: added coordinates to all four leads entries and corrected a sheet-number typo on the Villa Saporiti plane (was mis-cited as the Museo Giovio tree's own sheet). Como stays at 9/10, genuinely exhausted rather than under-searched; released the claim.

**Bergamo** (rank 107, 7/10): claimed, dispatched a verify agent on the one open lead, the Horse Chestnut of Viale delle Rimembranze in Torre Boldone, held back since 2026-08-14 on an unconfirmed post-2021 health check (agronomist flagged decline in 2017, the comune illegally pollarded it in 2018, a limb failed in 2021, nothing published since). No newer sighting turned up, but Lombardy's regional monumental-tree register, updated October 2025, still lists it standing at its pre-damage girth: a comune has to report a felling for delisting, and none has. Per the project's standing rule that unconfirmed-but-not-known-dead never holds a tree back, shipped as **bgm_008**, flagged, with the full history stated plainly in the story and an open invitation for a reader to confirm it's still there. Wrote the story myself (single tree, not worth a dedicated write-stories dispatch) rather than smoothing over the damage. Updated the city's intro, meta_description, question_meta/context and one FAQ answer for 8 trees instead of 7 and a fourth out-of-town stop; `preflight.py` caught an overlength question_context (222 words against Contract B's 200), trimmed to 196.

Build clean (1574 pages). `scripts/qa.py`: one pre-existing sitemap-lastmod warning from this sandbox's shallow git checkout (confirmed against several other sessions hitting the identical artifact today), unrelated to this change. `scripts/superlatives.py` clean, 344 claims. `scripts/tree_index.py` and `scripts/city_queue.py` both run. Ran `scripts/photo_hunt.py --recheck` (free API sweep, per runner rules): 40 trees swept, several new candidates queued for a session's viewing pass, none judged here. Logged all three verify passes to `data/agent-costs.json`. Released the `bergamo` claim, committed and pushed the city file, the leads fix, the cost log and the queue refresh as separate steps.

**Potsdam** (4/10, gap 6): a third verify pass, dispatched in parallel with Bergamo, found two new trees on Pfaueninsel, a former royal pleasure island a further ferry ride past the existing Glienicke cluster: the Door Oak (a sessile oak with a folly-door cut into its trunk, alive-confirmed May 2025) and the Schlosswiese Oak (a five-stemmed veteran a hundred metres away, three sources agreeing within metres). Both ship flagged, honest about the longer trip (a bus change plus a small paid ferry, roughly 35-45 minutes each way against the existing cluster's 12-minute tram), the same day-trip pattern already used for Blarney/Fota (Cork) and Coole Park (Galway). Shipped as pot_005/006, closing Potsdam to 6/10; two more single-source Pfaueninsel candidates (a split-leaved rarity oak, a plane by the island inn) stay leads.

**A genuine coordination bug surfaced and is worth recording plainly.** This verify agent ran in the same working directory as this session rather than an isolated worktree (none of today's three verify dispatches used `isolation: "worktree"`). While it was still writing its delivery file, this session polled the file directly (via `ls`/`cat` instead of waiting for the actual completion notification), read a partial delivery, and started editing `data/cities/potsdam.json` on that premise. The agent, mid-pass, found its own delivery file briefly missing from disk and `data/cities/potsdam.json` (a file it was explicitly told never to touch) modified with content it never wrote; it correctly flagged this as anomalous and reverted the city file via `git checkout`, which destroyed this session's in-progress edits. No data was lost permanently: the agent's actual JSON delivery survived and was merged properly once its real completion notification arrived, but it cost a redo. Lesson for future sessions: either wait for the actual task-notification before touching a dispatched agent's target files, or use `isolation: "worktree"` for any verify/write agent whose delivery file you might need to peek at mid-run.

Build clean (1576 pages). `scripts/qa.py`: same pre-existing shallow-clone sitemap-lastmod warning, unrelated. `scripts/superlatives.py` clean (344 claims). `scripts/tree_index.py` and `scripts/city_queue.py` both run; `data/city-list.json`'s Potsdam row and `data/first-seen.json` updated automatically by those scripts. Logged all three verify passes (como, bergamo, potsdam) to `data/agent-costs.json`. Released the `potsdam` claim, committed and pushed.

**Brno** (6/10, gap 4): rather than dispatch a fourth agent, resolved one of its three open leads directly in-session with four targeted web searches. The lead ("Platan profesora Chudoby") had been held on suspected mistaken identity, two web sources describing what looked like different trees at slightly different girths on the same street corner. Direct checks (turistika.cz, botany.cz, and Masaryk University's own 2022 renaming-ceremony writeup) converged on one tree, not two: same corner of Veveří and Pekárenská, same 2003 declaration year, corroborated by the university's own account of renaming it in 2021/2022 for its first professor of English philology, who wrote about the same tree in a 1930 newspaper column. The 383cm/475cm girth disagreement between sources is real and unresolved, so the story states both rather than picking one. Shipped as **brq_007**, about 600m from the existing Moravské náměstí cluster, well inside the walk. Left the two harder leads alone (a plane on an active construction site, Mendel's Ginkgo behind a currently-closed, booking-only museum) rather than forcing them.

Session total so far: 3 verify passes dispatched (Como: 0 new, dedup fix; Bergamo: +1 tree; Potsdam: +2 trees) plus one direct session verify (Brno: +1 tree), 1 exhausted-hunt city (Sintra, correctly left alone), 4 trees added across 3 cities, one coordination lesson recorded. Continuing to the next rung.

## 2026-08-15 (continued) - Quebec City opens with 6, the first Canadian city on the site

Write pass on `data/research/quebec-city-verified.json`, six verified trees, and the first country added since the European and Japanese runs. They are one walk of about 2.5km: Grande Allee runs straight into Parc des Champs-de-Bataille, so three street trees and three park trees string together, all free, all on public pavement or inside a National Historic Site open dawn to dusk.

**The pattern this sets for Canada, and it is a measurement pattern.** The Ville de Quebec's open register (`Arbres potentiellement remarquables`, CC BY 4.0) publishes DIAMETRE at DHP, diameter at breast height, not girth. Every circumference on this page is therefore a conversion and says so, in the story, in the FAQ and in the question context: 132cm across becomes roughly 4.15m round, 154cm becomes 4.84m. Nothing is presented as a measured girth. Any Canadian city working from a municipal inventory should expect the same field and do the same. All six diameters were physically plausible, so none had to be dropped. The other half of the pattern: 87% of that register is private land, and every tree here comes from the public subset, which is why the access lines are confident rather than hedged.

Oldest-tree answer: **qbc_001**, the larger of two red oaks on Rue De Laune, and the answer is deliberately not clean. La Presse reported the park's oldest tree as a red oak of more than 250 years on that street and named no individual trunk; five red oaks are registered along the stretch; qbc_001 is the largest by a clear margin (132cm against 89 to 110). So the page attaches the claim to the biggest and says outright that this is an inference on size and not a named match. That is the bridge-claim rule applied where it would have been easiest to break: joining "oldest tree in the park" to "largest tree in the register" would have produced a clean sentence neither source supports. Its neighbour qbc_002, fifteen metres away, ships with no age rather than borrowing the number. No other tree on the page carries an age at all.

Also honest on the page: two of the six are Ulmus glabra, a European elm on a North American street, recorded that way by the municipal foresters while the city's heritage page for Grande Allee names only the American elm, so the stories say the species identification is the foresters' and not the heritage record's. And qbc_004 is described as standing among Grande Allee's American elms rather than as one of the originals from the late-1880s planting, because nothing links this stem to that planting. One `best_time`, qbc_001 in October. `pagegaps.py` reports no country gap, so no Canada intro is owed yet.

All photos `missing`, no photo hunting. `preflight.py` clean at 117 cities, `superlatives.py` clean at 344 claims, `tree_index.py` and `city_queue.py` re-run. `data/city-list.json` count updated in place, `data/leads/quebec-city.json` given the standard header and noted with what shipped, `quebec-city-verified.json` deleted.

## 2026-08-15 (continued) - Wroclaw opens with 4, the four named oaks of Wielka Wyspa

Write pass on `data/research/wroclaw-verified.json`, four verified trees, which is the floor exactly. All four shipped: nothing in the verification notes made any of them unshippable, all four stand on public ground with no gate, and the two with damaged trunks are alive and in leaf, which is the only vitality question that matters.

They are one walk. Every oak sits on Wielka Wyspa, the island between the Oder and its canal, within about 1.5km of the others, and three of them were designated pomniki przyrody in a single sitting on 16 February 1953 (decisions 2/53, 3/53, 5/53); the fourth followed in April 1976. The strongest fact on the page belongs to wro_001: in 1865 Breslau's mayor Artur Hobrecht bought the riverbank plot on the city's behalf specifically so the oak would not be felled, and it carried his name until 1945, when the Polish city renamed it for the beekeeper Jan Dzierzon.

Oldest-tree answer: **wro_002, the Dziadek (Grandpa) Oak**, reported at 440 to 460 years, measured at 652.5cm in 2019 against 629cm in 2015, and now held up by elastic bindings and steel clamps. It is the only tree here with a reported age that beats the others, so the answer names it on that basis and then says plainly where the number comes from. Two of the four (Piotr Wlast, Jan Stanko) have no published age in any source, which the FAQ states outright rather than hiding: Poland's GDOS register has no age or girth column anywhere in it, so every measurement on this page comes from a dedicated recent survey of Wielka Wyspa's monument trees, not from the state. Those two ship with girth, height and a designation year and no number for their years.

A near-coincidence worth watching if anyone edits these pages: wro_001 measures 652cm and wro_002 652.5cm, half a centimetre apart. The stories note the coincidence and neither claims to be the thickest, because on those figures nobody should. One `best_time` on the page, wro_002 in midwinter as a bare silhouette, which is the case that field was written for: a braced veteran whose whole frame is only legible without leaves. The other three are empty on purpose.

All photos `missing`, no photo hunting. `preflight.py`, `superlatives.py`, `tree_index.py` and `city_queue.py` all run and clean for Wroclaw. `data/city-list.json` count updated in place, `data/leads/wroclaw.json` noted with what shipped, `wroclaw-verified.json` deleted.

## 2026-08-15 (continued) - Potsdam opens with 4, and the page admits they are in Berlin

Write pass on `data/research/potsdam-verified.json`, four verified trees (pot_001 to pot_004), all protected as Naturdenkmale by the Land of Berlin. This is the city an earlier entry today parked as not shippable, because all the candidates sit administratively in Berlin-Wannsee rather than in Potsdam. The verify pass came back with the honest version of that problem rather than the forced one, and it ships: the trees stand across the Glienicke bridge, twelve minutes by tram 93 from Potsdam Hauptbahnhof and most of an hour from central Berlin, and the intro, the story copy and a dedicated FAQ entry ("Are these trees actually in Potsdam?") all say outright that they are on the Berlin bank. Nothing on the page implies otherwise.

Berlin's natural-monument register is a legal instrument, not a survey: it gives a number, a species, a cadastral parcel and a location sentence, and records no age, no girth and no condition. So three of the four ship with no age and no girth at all, and the stories say that plainly instead of reaching for numbers. The fourth, the Jagerhof oak, has a real second source in the Ostdeutsches Baumarchiv (566cm taped in 2023, photo 2011) and an age that follows that archive's own reasoning back from the Jagerhof's pre-1830 construction, so it carries "roughly 300 years" with the reasoning shown.

One trap defused permanently: a search summary had claimed a 130cm circumference for pot_003, which is the Flur parcel number in the gazette, not a measurement. It is not in the file, and pot_003's `notes` records why so no later pass reintroduces it.

Leads: pot_001, pot_002 and pot_003 open with the Bridge of Spies 200 metres away, a tea-party mosaic floor by the Lions Fountain marking where visitors sat under the Konigslinde, and the flat fact that Berlin protects an oak nobody has ever measured. Oldest-tree answer: pot_004, with the page stating that no register here carries ages and that the other three have no published age anywhere. Two `best_time` entries, both real: lime blossom in late June and July for the Konigslinde, and the bare winter frame of the veteran oak. `how_to_recognise` on the two limes only, which are the pair a visitor could confuse. Photos all `missing`, no hunting this pass.

`scripts/preflight.py` caught one over-long `how_to_recognise` (247 chars against the 240 limit), fixed, then clean. `scripts/superlatives.py`, `scripts/tree_index.py` and `scripts/city_queue.py` all clean. Updated the existing Potsdam row in `data/city-list.json` to 4 trees, recorded the four as delivered in `data/leads/potsdam.json`, deleted the verified file. The three planes in the walled garden behind the hunting lodge stay a lead: nobody could confirm that garden is open to casual visitors.

## 2026-08-15 (continued) - Brno opens with 6, one walk of 1.1 km through the ring of parks

Write pass on `data/research/brno-verified.json`, six verified trees (brq_001 to brq_006), each carrying the AOPK CR national memorial-tree register plus an independent Czech source. They form one continuous walk: Brno demolished its city walls between 1809 and 1859 and laid a ring of parks along the line, and five of the six stand in or beside that ring, the sixth on hospital ground in Stare Brno. Furthest pair 1.1 km apart, none more than twenty minutes on foot from the main station.

What the stories lead with, since the register gives no ages anywhere and several trunks are measured in different decades: the Moravske namesti oak was valued at over 600,000 Kcs when the city protected it in 1985; the oak 130 metres south has a legal protection zone of 13.4 metres radius round its trunk; the Rooseveltova horse chestnut nearly lost its roots to an underground garage plan the architecture press covered as a story about one tree; the plane below Petrov stands on a terrace that is closed in winter, so the page says so; the plane at St Anne's is the thickest at 5.65 to 5.75 metres and stands on a working teaching hospital campus, stated plainly in both the access line and the story; the Benesova plane outlasted the 1948-49 Fuchs bus station on its corner and has no published age at all, so the field stays empty.

Every girth disagreement is written as a range with the reason (410cm in 2004, 423cm in 2010 and 480cm in the register for brq_002, and so on), never silently resolved. Two trees keep their flags in the prose: brq_002's freshest photograph dates from May 2015 and the story asks the reader to report back, brq_001's register record was refreshed in 2024 but no dated post-2020 sighting turned up. `how_to_recognise` written for the three trees where confusion is real (the two oaks 130 m apart, the hospital campus), left off the rest. One `best_time`, the horse chestnut's May flowering. One species normalised: brq_005 came in as Platanus x hispanica, written as London Plane (Platanus x acerifolia) to match the site's 107 other entries for the same hybrid, per hard rule 9.

Oldest-tree answer: brq_002, on Brno's heritage encyclopedia giving it "170+ years", with the page saying outright that the Czech register has no age field, that every age here is an estimate rather than a measurement, and that one tree has no published age at all. `scripts/preflight.py`, `scripts/superlatives.py`, `scripts/tree_index.py` all clean. Photos all `missing`, no hunting this pass. Updated the existing Brno row in `data/city-list.json` to 6 trees, marked the six delivered in `data/leads/brno.json`, deleted the verified file.

## 2026-08-15 (continued) - Poznan opens with 6, written from the city's own designation records

Write pass on `data/research/poznan-verified.json`, six verified trees, all of them Polish natural monuments (pomniki przyrody) protected by council vote and then entered in the national GDOS register. Four are London planes standing together on Plac Wolnosci, designated on 16 May 2023 at the Stare Miasto district council's request and each given the name of a botanist or plant sociologist who worked in the city; the other two are from the April 2024 batch, a plane of about 190 years and 411cm in the Zamek's Rose Courtyard and a 271cm silver maple on Skwer Zielone Ogrodki.

The honest constraint on this page is age: Poland's national register has no age or girth column at all, so every figure here comes from the city's own announcement, and the four square planes have nothing beyond a planting "at the start of the twentieth century". That is stated on the city page, in the oldest-tree answer and inside the stories rather than smoothed over, which is also why the oldest-tree answer names the Zamek plane on the city's published figure rather than ranking six trees on nothing. All six keep `curation_status: flagged` from the verification pass.

Two writing calls worth recording. The four planes on the square are near-identical neighbours of one species, so all four carry a `how_to_recognise` line placing them relative to each other (thirty metres apart to the east, the close pair six metres apart on the south side), which is exactly the case that field exists for. And the Bazar hotel on the same square is where Paderewski spoke on 26 December 1918, the evening the Greater Poland Uprising started: the story says plainly that nobody has recorded whether these trees were already standing for it, because the planting date straddles the year. Joining those two facts would have been a bridge claim.

No `best_time` on any of the six: London Plane's phenology file records nothing above "nice", and there is no species file for Silver Maple, so an empty field is the correct answer. All photos `missing`, no photo hunting this pass. `scripts/preflight.py` caught one real problem, an intro reading "all four are London planes" on a six-tree city, which is the count-promise check doing its job; rewritten and clean. `superlatives.py` clean, `tree_index.py` and `city_queue.py` re-run, `data/city-list.json` count updated in place, `data/leads/poznan.json` noted with what shipped, `poznan-verified.json` deleted.

## 2026-08-15 (continued) - Page gaps: two species intros, one park intro, and a bug in the detector itself

Same session, tenth item. `python3 scripts/pagegaps.py` (part of every run per CLAUDE.md's rung 7) found 2 species gaps, Norfolk Island Hibiscus and Mastic Tree, both cleared to the 3-tree threshold by trees shipped earlier today (Palma's Lagunaria and lentisco, joining existing Setubal/Barcelona/Istanbul specimens), and 1 park gap, Padua's Orto Botanico at 5 trees (pad_001-004 plus today's pad_010). Wrote all three intros from the trees' own data rather than a template, per P3: the hibiscus page uses the itchy-bomb-tree nickname and the three actual cities; the mastic page leads with the shrub-to-tree contrast and Istanbul's 500-year outlier; the park page leads with Padua's 1545 founding and UNESCO 1997 listing.

Caught a real bug while verifying the park page built: it silently did not appear in `site/dist/parks/` on the first build. `site/src/lib/parks.ts`'s `parkKey()` derives a park name from a tree's neighbourhood field first, address second; the intro file's own `park` value has to match that output exactly (the code comment says so). I'd written "Orto Botanico di Padova"; the actual derived key from the trees' neighbourhood fields is "Orto Botanico". Fixed the intro file, and separately found that `scripts/pagegaps.py`'s own detector uses a DIFFERENT algorithm (address only, no neighbourhood fallback), so once the intro file was fixed to match the real page, the detector started reporting a false gap for a page that had just been correctly published. Fixed `pagegaps.py` to mirror `parkKey()` exactly (neighbourhood first, same regex cleanup) rather than leave a second, wrong implementation of the same matching logic in the codebase.

Build clean throughout, `scripts/qa.py` clean (1789 pages at the point of this change). `scripts/superlatives.py` clean. `scripts/tree_index.py` run. Logged to `data/agent-costs.json`.

## 2026-08-15 (continued) - Ferrara opens with 5

Same session, ninth target. Checked **Potsdam** (rank 159, register 12) next in the staged shelf first and found a data problem rather than a tree: all 7 candidates in `data/research/potsdam-register-candidates.json` sit at Jagdschloss/Schlosspark Glienicke, administratively Berlin (district Steglitz-Zehlendorf, postcode 141xx), not Potsdam, however close to the actual city line at Glienicker Brucke. Not shippable as Potsdam without misstating the city, and Berlin itself is a Google-confirmed stage-2 city (18/30) where deepening is paused while stage-1 cities still have real supply. Recorded in CURATION.md rather than forced either direction, with a note that `prepare.py`'s candidate staging may be picking trees by raw distance to a city centre point without checking which municipality they actually fall in, worth checking on other border cities.

Moved to **Ferrara** (rank 189, target 10, register 7, also staged), a UNESCO World Heritage Renaissance city. All 7 candidates sit within 1km of each other across Palazzo dei Diamanti, Parco Massari and the Biblioteca Ariostea. Shipped 5 individual trees; MuseoFerrara, the city's own civic museum, turned out to have dedicated pages for most of the individual specimens (age estimates, history, 2013 Law 10 monumental-list detail), so this pass leaned on real second-source research rather than register-only sourcing, matching Parma and Trieste earlier today rather than the thinner Alicante/Cagliari/Seville pattern from previous sessions. Left 2 candidates as leads (a Cedrus libani trio and a yew, both registered as "Insieme omogeneo" groups).

Notable trees: a gray poplar over 150 years old in the Palazzo dei Diamanti garden, its diamond-fissured bark echoing the palace's own famous facade; a bagolaro and a ginkgo among Parco Massari's original 2013 monumental-list trees; a second ginkgo at the Biblioteca Ariostea first documented in 1890 as a survivor of the university's old botanical garden, drawing annual local press coverage for its autumn colour; and the thickest trunk on the page, an undated street plane on Viale Po.

Build clean (1533 pages): the three central-cluster trees form one 0.6km/8-minute walk, checked from the build output; the two outlying trees are correctly left as singletons. `scripts/qa.py` clean (1786 pages). `scripts/preflight.py` caught an underlength question_context (133 words) on the first pass, expanded to fit Contract B. `scripts/superlatives.py` clean. `scripts/tree_index.py` run. Added Ferrara to `data/city-list.json` by hand. Refreshed `data/city-queue.json`/`CITY_QUEUE.md`. Logged to `data/agent-costs.json`, wrote `data/leads/ferrara.json`, released the `ferrara` claim.

## 2026-08-15 (continued) - Parma opens with 5, Emilia-Romagna's tallest tree

Same session, eighth target, and a new city rather than another gap-fill: **Parma** (rank 149, target 10, register 7), already staged in `prepare.py`'s shelf. All 7 register candidates sit within 1km of each other around Parco Ducale, Palazzo Ducale and Piazzale della Pace, one contiguous public area. Shipped 5 individual entries; 2 more (both plane trees) are registered as "Insieme omogeneo" (homogeneous group) sheets and left as leads, the same ensemble exclusion applied everywhere else today, though one of them may be splittable: a comune.parma.it press release describes municipal tree-climber maintenance, root aeration and tomography on what reads as one specific champion plane at that exact corner, protected individually since the 1950s, which does not obviously square with a "group" register classification.

What shipped: a 47-metre London plane that local press names the tallest tree in Emilia-Romagna; a cedar of Lebanon on Piazzale della Pace, the piazza's one conifer among a remnant of a 65-plane avenue, under documented maintenance since the 1950s; a field elm that survived the Dutch elm disease epidemic that killed most of its kind in the 1930s-40s (independently corroborated by a local press piece describing the same tree by the Palazzetto Sanvitale, matching measurements); a horse chestnut; and an oak. The park's own history carries real drama worth telling straight: founded 1561 by Duke Ottavio Farnese, then every mature tree in it cut down and burned for firewood by occupying troops in 1745 during the War of the Austrian Succession, replanted from 1749 under Duke Filippo di Borbone and the architect Petitot, with further planes added around 1830 under Duchess Maria Luigia (Napoleon's second wife, ruling Parma as her own duchy).

Build clean (1526 pages): the walk-planner merged all 5 trees, including the piazzale a few hundred metres outside the park proper, into one 1.5km/20-minute walk, checked from the build output rather than assumed. `scripts/qa.py` clean (1777 pages), `scripts/preflight.py` and `scripts/superlatives.py` both clean. `scripts/tree_index.py` run. Added Parma to `data/city-list.json` by hand (same gap as Alicante and Palma before it: `city_queue.py` only updates existing rows). Refreshed `data/city-queue.json`/`CITY_QUEUE.md`. Logged to `data/agent-costs.json`, wrote `data/leads/parma.json` for the two held group-registered planes, released the `parma` claim.

## 2026-08-15 (continued) - Padua reaches its 10-tree target

Same session, seventh target. **Padua** (rank 276, 9/10, register 12) already had its leads file (`data/leads/padova.json`, local-name slug, matched via `city-aliases.json`'s reverse lookup) naming the cheapest possible next tree: a Himalayan cedar in the Orto Botanico, the same cluster as 4 already-published trees, held back only because Italy's RAMI register rates its current health "Pessima" (poor). Checked the Orto Botanico's own website and social account, both of which still describe and locate the tree today (Italy's first Cedrus deodara, planted 1828, standing between the Montagnola and the Fontana delle Quattro Stagioni) with no suggestion it is gone. Shipped as pad_010, poor-health rating stated plainly in the story rather than smoothed over, closing Padua to target.

The Astro build's own species-name check caught a hard-rule-9 miss before anything shipped: wrote "Deodar Cedar", the corpus standard elsewhere (Barcelona and others) is "Himalayan Cedar". Fixed in the same pass. Updated the city's intro and one FAQ answer to count five Orto Botanico trees instead of four. Build clean (1519 pages), `scripts/qa.py` clean (1768 pages), `scripts/preflight.py` and `scripts/superlatives.py` both clean. `scripts/tree_index.py` run. Refreshed `data/city-queue.json`/`CITY_QUEUE.md`. Logged to `data/agent-costs.json`, marked the lead RESOLVED, released the `padua` claim.

## 2026-08-15 (continued) - Trieste reaches its 10-tree target, a third cluster in Citta Vecchia

Same session, sixth target (after a Zaragoza pass that shipped nothing, see below). Bergamo's only real remaining lead needed a fresh health check with no clean way to get one this session (a horse chestnut illegally pollarded in 2018, storm-damaged in 2021, nothing since), and its other candidates are all private villa grounds or non-collectible avenues, so it stayed untouched beyond one small fix (see below). Moved to **Trieste** (rank 233, 8/10, register 43), where an earlier pass had left a lead explicitly marked "STRONGEST NEXT ADDITION": a Piazza Hortis hackberry with two sources already in hand (Il Piccolo's 2025 coverage of the city fencing it, over 180 years old, and a 2024 EU TreeTag campaign placement), held back only because it sits 1.7km from the existing Giardino Pubblico cluster and would have stretched that walk past 2km.

Rather than force it into an existing walk, opened a third cluster: the hackberry plus a Siberian elm 700m away in the Piazzale Rosmini garden (also TreeTagged in 2024, a public garden the city's own parks department lists), both in Citta Vecchia. Shipped as tri_009/010, closing Trieste to 10/10. The two are close enough to walk between but, at only two trees, fall under `WALK_MIN_TREES` and do not form their own mapped route; the FAQ answer says exactly that rather than implying one. Updated the city's intro, meta_description and the walk-count FAQ answer for three clusters instead of two; `scripts/preflight.py` caught both an overlength intro and an overlength meta_description on the first pass, trimmed both.

Also this session: fixed a stale Bergamo lead (a hospital-garden plane) that cited the superseded "when in doubt, leave it out" line hard rule 10 dropped on 2026-08-13; re-evaluated it against the current three-test standard and it stays blocked on its own merits (tight visiting hours, no evidence of open access), but the reasoning now says why rather than quoting dead text.

Build clean (1518 pages), `scripts/qa.py` clean (1766 pages), `scripts/superlatives.py` clean. `scripts/tree_index.py` run. Refreshed `data/city-queue.json`/`CITY_QUEUE.md`. Logged to `data/agent-costs.json`, marked both leads RESOLVED, released the `trieste` claim.

## 2026-08-15 (continued) - Bucaco reaches its 10-tree target

Same session, fourth target, and the cheapest of the day: `leads.py --city bucaco --ready` showed 11 already-verified candidates for a 1-tree gap. Picked the cleanest of them, the Redwood of the Fonte de Santa Teresa (5.58m girth, 45m tall, about 150 years old at the 2016 ICNF measurement, on the Trilho da Agua past the forest's historic fountains), over a second candidate (a redwood registered as part of an "Alameda" row standing 10 metres from the already-published King Regnans) whose collectible-point status a previous pass had flagged as genuinely unresolved rather than merely convenient to skip.

The chosen lead's own `why` field said only "cut on the count and because a page with three separate redwood entries stops being a walk and becomes a list", which is exactly the kind of judgement call CLAUDE.md's Step 2 says can never hold a tree back. Checked the claim in that same field that it was "bigger in the trunk" than the already-published Santo Elias pair and it is not (5.58m against 5.64/5.67m per bsc_005's own notes), so the story does not repeat that line; corrected it in the leads file for whoever reads it next.

Updated the city's intro, meta_description and one FAQ answer for the new count of ten. Build clean (1516 pages): the full ten-tree walk still computes as one route, 1.9km, 25 minutes, checked from the build output. `scripts/qa.py` clean (1764 pages), `scripts/preflight.py` and `scripts/superlatives.py` both clean. `scripts/tree_index.py` run (Portugal now 95 highlighted). Refreshed `data/city-queue.json`/`CITY_QUEUE.md`. Logged to `data/agent-costs.json`, marked the lead RESOLVED, released the `bucaco` claim.

## 2026-08-15 (continued) - Trento reaches its 10-tree target

Same session, third target. Checked `city_queue.py --next` again after Palma: Como and Alicante both sit at gap 1 with their only remaining leads access-blocked (rechecked Como's Tibaes-closure and Via Baserga doubts fresh rather than trusting the cache; nothing has changed, both stay held), so moved to **Trento** (rank 97, 9/10, ready 4 per the tool, all four already known misclassified per yesterday's own review notes, real remaining villas). Rather than re-litigate the three held villas, followed the same review's own pointer: "the wild cherry at Passo del Cimirlo... has never been researched."

Found it fast because a register existed and nobody had read it: `dati.trentino.it`'s "Alberi monumentali del comune di Trento 2024" dataset, a CSV export (linked from the resource page, no direct download link on the page itself, had to follow through to find the Google Sheets export URL) with an exact scheda for every one of the city's 18 monumental trees, including this one: 06/L378/TN/22, girth 359cm, height 26.5m, altitude 790m, ownership pubblico, managed by the province's own forestry agency (AFTS). That settles access outright, public forest, no doubt at all, unlike the three villas. Shipped as tre_010 with Wikipedia's Passo del Cimirlo article for the pass's history (WWI fortifications, road access from Povo) and Trentino Trasporti's line 5 for the bus leg; the last stretch is an uphill walk on an unpaved provincial road, roughly 45-60 minutes, honestly described as such rather than glossed over.

Updated the city's meta_description, question_context and one FAQ answer for the new count and outing; `scripts/preflight.py` caught an overlength question_context (225 words) on the first pass, trimmed to within Contract B's 200. Build clean (1515 pages), `scripts/qa.py` clean (1763 pages), `scripts/superlatives.py` clean. `scripts/tree_index.py` run. Refreshed `data/city-queue.json`/`CITY_QUEUE.md`. Logged to `data/agent-costs.json`, noted the promotion in `data/leads/trento.json`'s own review trail, released the `trento` claim.

## 2026-08-15 (continued) - Palma de Mallorca opens with 5

Same session, second target. `python3 scripts/city_queue.py --next` after refreshing the source (see below) put Alicante at gap 1 with its remaining candidate held on an access doubt (see previous entry) and Cagliari's register fully accounted for (7 published, 2 blocked private, nothing left). Moved to **Palma de Mallorca** (rank 62, new city, gap 10, register 8, already staged in `prepare.py`'s shelf): the Balearic government's CC BY catalogue of singular trees gave 8 named, individually catalogued candidates within 4.4km, well clear of the six-candidate floor.

Shipped 5, blocked 3. S'Olivera de Cort (plm_001): a 500-600 year old olive lifted whole from a Pollenca estate and replanted in front of Palma's Ajuntament in 1989, donated after the owner refused to sell it and gave it away instead when he learned its destination; Ultima Hora's 2019 piece on the decades-late commemorative plaque is the second source. The Ficus de la Misericordia (plm_002) and the Ficus del Cementeri (plm_004), two 150-200 year old Moreton Bay figs local sources rank among the largest in the Balearics, one in a free public cultural centre's garden, one in the municipal cemetery (open daily, no ticket). The Lagunaria de la Llotja (plm_003), a Norfolk Island hibiscus nicknamed pica-pica for its itch-inducing seed pods, on the seafront promenade in front of the Gothic Llotja. The Mata de Bellver (plm_005), an ordinary lentisco shrub that grew four trunks and tree size over a century, in the free forest park around Castell de Bellver (the castle interior itself is ticketed, the park is not).

Blocked: the Ginjoler del Convent de la Concepcio (dead, per the register's own "mort l'arbre monumental" note), and two private-land olives/myrtle, one 4.4km out past this pass's cluster radius regardless. All three recorded in the new `data/leads/palma-de-mallorca.json`. The three old-town trees (Cort, Llotja, Misericordia) form a real walk, checked from the build output: 1.4km, 19 minutes. The cemetery fig and the Bellver lentisco stand outside that route as separate stops, honestly described that way in the FAQ rather than implying a route the site does not draw (both are 1.6-2.7km from the old-town cluster).

Added Palma de Mallorca to `data/city-list.json` by hand (confirmed again: `city_queue.py`'s regeneration only updates existing rows, a new city has to be added once). `scripts/preflight.py` caught an overlength intro (107 words against Contract C's 60-100) on the first pass, trimmed to 97. Build clean (1514 pages), `scripts/qa.py` clean (1762 pages), `scripts/superlatives.py` clean. `scripts/tree_index.py` run (Spain now 155 highlighted). Refreshed `data/city-queue.json`/`CITY_QUEUE.md` again after this pass. Logged to `data/agent-costs.json`. Released the `palma-de-mallorca` claim.

## 2026-08-15 - Alicante reaches 9, a second cluster opens in Benalúa

New session. `python3 scripts/visitors.py`: 268 visits, 445 page views over the last 7 days (83 on 2026-08-10 remains the best day; the week is trending down, 34 on 2026-08-14). `python3 scripts/prepare.py`: 14 cities staged for verify, nothing awaiting a writer. Step 0: Supabase submissions unreadable this session (env var expansion blocked, same sandbox limit noted 2026-08-14), treated as absent rather than skipped. REVIEW.md's newest entry (2026-08-14) held two WARN, no BLOCKER; both were already fixed by the time this session read them (account.astro's copy already matches saved.astro, and CLAUDE.md's accounts section already reflects the 2026-08-14 ruling), so nothing to do there. Smoke test, weekly analysis and data digest all recent, none needed dispatching.

Found a stale claim on `caserta` (verify, by night-run, committed 2026-08-14T22:55) with no work behind it beyond the claim itself and no matching LOG entry; Caserta has been at its 10-tree target since 2026-08-13 anyway, so released it as dead rather than continue it.

Followed rule (b) of "the course after the fortnight" (register-backed verify) on **Alicante** (rank 52, gap 3 at session start): its leads file already flagged two register entries as promising-but-unresolved, `register_id 964` (Ficus de Benalúa, access uncertain: on a health centre's grounds) and `945` (Ficus microcarpa at Plaza Navarro Rodrigo, address unconfirmed). Resolved both. The city government's own news article on the Benalúa fig (age over 150 years, trunk 23.7m by the city's measurement against 14.69m in the Generalitat's register, planted before 1860, saved twice from removal) confirmed it stands in a small open garden beside the health centre's entrance, not inside the gated facility; a second municipal article on the city's ficus information-panel programme independently names Plaza Navarro Rodrigo as one of six sites, confirming the second fig sits in a public square with a fountain, playground and kiosk. Nominatim/Overpass reverse-geocoding corroborated both locations (an OSM contributor has independently mapped the Benalúa fig by name).

Shipped both as ali_008/009, opening a second, smaller cluster 1.2km south of the existing seven-tree centre cluster; the Benalúa fig, over 150 years old, becomes the city's new oldest and thickest tree (oldest_tree_id updated), so the question page, FAQ and intro all needed rewriting rather than just appending. Checked a third candidate seriously before dropping it: a group of large figs (register_id 3096-3099) near Avenida de Salamanca corroborated by the same plaques article, but categorised "Proteccion Generica" rather than "Arbol Monumental" in the register, whose own caveat says that category includes private trees indistinguishable from public ones without a per-tree check. Reverse-geocoding showed parks and gardens nearby but not conclusively at the tree points, so left it as a lead with the new evidence written in rather than force a third tree past that doubt (hard rule 10). Three olives and the rest of the Alicante leads file are untouched.

Two Benalúa trees are only 150m apart, below `WALK_MIN_TREES` (3) in `scripts/walk_planning.py`, so the build does not draw a route for them; the FAQ answer was written to match what the page actually does rather than imply a route exists. Build (`npm --prefix site ci` && `npm --prefix site run build`) clean, 1507 pages; `scripts/preflight.py` caught an overlength `question_context` (229 words against Contract B's 150-200) on the first pass, trimmed to 195. `scripts/qa.py` clean (1753 pages). `scripts/superlatives.py` clean, no colliding crowns. `scripts/tree_index.py` run (27,737 trees tracked). Logged to `data/agent-costs.json` (tokens not separately metered for this session pass). Released the `alicante` claim.

## 2026-08-14 (continued) - Guimaraes goes to 6, and the ensemble becomes one oak

Same write pass, second city. Briefed to ship up to 5 of the 5 remaining leads, shipping 2, because the collectible-point test and the day-trip boundary each took one out and access took a third.

gui_005 is The Oak of Santa Marinha da Costa, split out of the register's six-species conjunto rather than published as "the old trees of". The single point is the carvalho-alvarinho at the baroque circular granite tank in the monastery's walled garden, which is the one tree the property's own botanical guide singles out and the one place with an obvious spot to stand. Its age is deliberately empty and the story says why: the register's 290 years, measured 2006, covers a group that includes a eucalyptus, a tree that did not reach Portugal until the nineteenth century, so the figure cannot be this trunk's. The access hold from the earlier pass is lifted on the pousada's own gardens page, which describes the 9 hectare park as open to hospedes e visitantes. No hours are published, so the access line says exactly that. gui_006 is The Stone Pine of Silvares, 26 metres tall with a crown 26.4 metres across, standing in the middle of a roundabout on the old ER 206, city bus 082 from town, no gate and no ticket.

Three held, each on a specific finding rather than on "unresearched". Casa da Ribeira is typed "Bosque" in the ICNF record, eight species and not one measurement, which fails the collectible-point test the way Casa da Penha does. The Megide pine at Moreira de Conegos has a crown 30.5 metres across on a 24 metre tree and is held only because nothing says whose ground it stands on. And the Citania de Briteiros pine, the best of the three and fully researched now, is held on transport: Guimaraes' own tourism site gives 15 km and publishes no public transport route, and the nearest public option anywhere is Braga bus 83 to Lageosa plus a 2 km walk. On that same evidence it belongs to Braga, which is live with 4 trees and room, and everything a pass needs to write it is in data/leads/guimaraes.json.

## 2026-08-14 (continued) - Trento goes to 9, one lead promoted and the sequoia question finally sharpened

Second write pass on Trento, briefed to ship 2 and shipping 1, because access is the decider here and only one of the five remaining leads clears it honestly. What went live is tre_009, the Beech of Malga Brigolina on Monte Bondone: 465 centimetres round on the national register, standing alone in an alpine pasture at around 940 metres, which is the last place a beech is supposed to be. Fagus sylvatica in a wood grows straight and clean and shades out everything under it; left in the open this one went low and broad instead. Its hold was never access (open pasture, nobody's home) but the missing route, and the route exists: bus B202 from Trento towards Monte Bondone stops at Candriai, and the waymarked Giro della Selva path leaves the village near the football pitch and reaches the malga in about fifteen minutes. Pin left approximate, it is the register coordinate about 330 metres from the malga building, and the story says so. No age, because Italy's register has no age column and nobody has published one, so the page asks the reader instead.

The four held leads are now held on findings rather than on a shrug, which is the useful part. The Villa O'Santissima sequoia at Villazzano was researched properly: Cooperativa SAD, the current owner, divides the grounds into three since the Comune bought a portion in 1982, and the sequoia sits in the "parco esterno" between the villa and the church of San Rocco. That is explicitly NOT the part restricted to residents, and also explicitly not the public Giardino storico Garbari, whose own published centre is 160 metres away and whose 13,700 square metres do not stretch that far. The villa is a residence for elderly people, so it stays held until a source says the outer park is walk-in or that the tree can be seen from via Ferrandi or the San Rocco church grounds, which would make it a view-only entry. Villa De Lorenzi, Villa Lubich and the Maderno pair returned nothing at all on access and are street-level questions, not search questions. Also noted in the leads file: the wild cherry at Passo del Cimirlo is on the city's own list of 18 monumental trees, is in none of our files, and has never been researched. That is probably Trento's cheapest tenth tree.

## 2026-08-14 (continued) - Braga opens with 4, because a fresh access check closed the monastery

Same write pass, second city. Braga was briefed as 6 and ships 4, and the reason is a link, not a judgement call. The verify pass had flagged the Mosteiro de Tibaes cerca as worth one fresh look before writing, since it is the only paid, gated site on the page and an older cached result had it closed for works. That look found a live site-wide notice on mosteirodetibaes.gov.pt: due to works in progress the cerca is closed, and the notice names the lago among the closed spaces. The twin Himalayan cedars (brg_004) and the 47-metre maritime pine (brg_005), which Publico's headline calls the tallest pine in Portugal, both stand beside that lake. So both are held in data/leads/braga.json, verified and ready to ship the day it reopens, with the closure notice quoted. Worth remembering: the ticketing page still sells the EUR 1.50 cerca ticket while the cerca is shut, so a ticket page is not evidence of access.

What shipped: the Biscainhos tulip tree, about 285 years old, a 2026 finalist for Portugal's Tree of the Year and the page's oldest by a wide margin; the Santa Tecla cork oak, which the parish spent six years getting protected and celebrated with the local school's fourth years on World Forest Day 2012; the three oaks sharing that square, which the register itself classifies as one grouped listing and measures once; and the oak and plane at the Bom Jesus funicular that both carry "arvore do Abraco" in their own official entries. Why they carry it is not established anywhere we could find, so the page says exactly that and asks the reader, per the publish-and-ask rule. The tulip tree's lost twin gets its own line rather than being confused with the 1997 replacement standing near it.

## 2026-08-14 (continued) - Cagliari opens with 7, and two of the fattest fig trunks on the site

Write pass over two verified files. Cagliari first, +7. The headline is girth: the Moreton Bay fig on Piazza Matteotti, straight outside the central railway station, measures 12 metres round on the national register, and the fig on the Via Roma waterfront 9.8. Both are Australian, both are on public squares, and the second one is locally known as the fig that came through the 1943 bombing. The Giardini Pubblici, Sardinia's oldest public park, adds a twinned pair of figs that the register files as one homogeneous group rather than measuring separately, a honey locust and a jacaranda, and the Tintitaco stands in the Parco della Rimembranza. Six of the seven sit inside a kilometre and a half; the Pirri cemetery cypress is four kilometres out and is the oldest tree on the page, already standing when the burial ground was consecrated in 1913.

Two things kept honest rather than tidied. The station fig has a precautionary fence under its crown since November 2025, which a visitor will meet, so the access line and the story both explain it and say what the January 2025 University of Sassari assessment actually found: no risk of structural collapse, tree healthy, under continuous management since 2019. And the Tintitaco, Prosopis torquata, has no English common name and two girth figures that look contradictory and are not, 3.0 metres on the national sheet against 5.7 measured at ground level because the trunk divides at about 1.3 metres. Its age splits the same way, 166 against 200, and the story gives both. Only one best_time on the page, the jacaranda in May; the evergreens get none. Photos missing on all seven, no hunting in this pass. cag_003's species was aligned to the corpus name Blue Jacaranda under hard rule 9.

## 2026-08-14 (continued) - Alicante opens with seven Moreton Bay figs, four of them on one square

Write pass on the verified Alicante file. +7, every one of them Ficus macrophylla, sourced on the Generalitat Valenciana's catalogue of monumental trees with local press as the second source. Four stand on Plaza Gabriel Miro, catalogued individually as Ficus Gabriel Miro I to IV, and that numbering is not a size order: II is the thickest at 10.65 metres round and is the one todoalicante calls the largest ficus in Spain's catalogue, on a canopy of 40.5 metres. Three more stand in and along Parque de Canalejas, among them the register's own named Ficus del Passeig de Canalejas at 11.59 metres, the heaviest trunk on the page.

All seven ship flagged, and nearly always for the same reason: the Valencian catalogue measures trees and does not date them, so six of the seven carry no individual age at all. The oldest-tree page says so in those words instead of inventing a ranking. It names ali_001 as the only tree here anyone has put a number to, about 120 years, and describes the rival 170 figure as circulating with no measurement and no particular tree behind it.

Two gaps stated rather than papered over. Photos are missing on all seven, photo hunting was not part of this pass. And the four plaza figs stand metres apart, so each carries a how_to_recognise line built on girth, height and where it stands, which is also true of the two near-identical Canalejas figs twenty metres apart. The square's five old elms are absent: local press reports one of them broke and came down at the San Fernando corner in September 2025, and the register alone cannot say which of the five coordinates is the dead one, so they wait in data/leads/alicante.json until something can tell them apart. That fall, and the citywide review of monumental trees it triggered, is in ali_001's story as recent history of the square.

Measured span is 449 metres corner to corner, roughly ten minutes on flat pavement, so the page says 450 rather than the 300 the brief carried. preflight, superlatives and tree_index all clean. Worth knowing for the next new city: city_queue.py only updates rows that already exist in data/city-list.json, so a new city never adds itself there. Alicante's row was added by hand; Catania, published this morning, is still missing from that file.

## 2026-08-14 (continued) - Como stays at 9, and the brief that said otherwise was wrong

Same write pass, fourth city, nothing shipped. The brief called Como's two remaining leads ready and they are not: both are held on access, which is the one thing a writing pass cannot write its way past.

The Museo Giovio plane stands in a museum courtyard still closed for renovation, with only a partial reopening targeted for the second half of 2026, and that was rechecked by this morning's verify pass, so it was not searched again. The Via Baserga plane is registered by MASAF against a house number, Via Baserga 39, with a second registered tree at the same address, which is the shape of a garden rather than a street verge. A search and the province's own tree page say nothing about it either way. Brussels blocks entries on that evidence, and the doubt here is about somebody's home, so it waits for one look at street-level imagery rather than a guess. Both findings are written into data/leads/como.json so the next pass starts from them.

Worth naming, because it cost a chunk of this pass: "READY" from `scripts/leads.py` means a lead has a name, a species and a position and no matching block reason. It is deliberately fail-open and it is not the same as verified. Four of the five Rome trees in the same brief failed for the same reason.

## 2026-08-14 (continued) - Brussels reaches 20, and Parc d'Egmont is now a ten-tree walk

Same write pass, third city. +4, all in Parc d'Egmont, all from the region's CC BY register: the London plane, the horse chestnut, the oriental plane and a Kentucky coffeetree. Every one of the four had been held back in the leads file on a judgement call rather than a rule (thin story, species already covered, a bigger sibling in another park, too young to bother with), which is exactly what CLAUDE.md says must never stop a tree going live. Ten of Brussels' twenty trees now stand in one hectare and a half, which is the densest walk on the site.

The coffeetree is published as what it is: seventy three centimetres round, fourth largest of its kind in the region, which measures how rare the species is in Brussels rather than how big this tree is, and the story says that in those words. Worth knowing for the next Brussels pass: sites.heritage.brussels returned a MySQL error to every fetch today, browser user agent included, so nothing new could be read from the per-tree pages and the open export carried the whole load.

## 2026-08-14 (continued) - Seville reaches 20, three of them inside the Alcázar

Same write pass, second city. +4 from the municipal catalogue of singular trees: the Alcázar's magnolia (4.70 metres round, and the survey names the decay fungus on it by name), a Judas tree that has reached sixteen metres and flowers out of its own bark in March, the bitter orange the catalogue calls El Naranjo de Pedro el Cruel, and the plane growing against the Macarena wall. All four are single-sourced on the 2022 catalogue and ship flagged, quoting the city's own condition wording rather than paraphrasing it.

Two things worth Hidde's eye. The orange tree is the publish-and-ask rule in practice: two metres round at the base, thirty six centimetres at chest height, three metres tall, carrying a fourteenth century king's name that no source explains, so the page says exactly that and asks the reader. And two of the Alcázar pins are deliberately approximate, because the catalogue's coordinates disagree with its own location text (one sits 80 metres from the pin we already publish for the same garden). That is the known coordinate fault in this catalogue, and it is now written at the top of the leads file for whoever ships the next Alcázar tree.

## 2026-08-14 (continued) - Rome takes four register trees, and four of the five briefed ones could not ship

Write pass over four cities' READY leads. Rome first, +4 (now 29 of a 30 target): the chir pine of Villa Fiorelli, the black poplar of Via Conca d'Oro, the hackberry of the Mura Latine and the Mexican blue palm of Villa Sciarra. All four are register-only, all four ship flagged and say so in the prose, which is what CLAUDE.md Step 2 actually prescribes for a single source. Two of them tighten existing walks: the palm makes Villa Sciarra a four-tree stop, the poplar sits a kilometre from the Viale Jonio plane.

The brief named five trees and four of them could not be written. The Risaro poplar is 14 km south, past the day-trip boundary, and burned in 2025 with nobody having looked since. The Ostia Antica holm oak fails the same boundary at 25 km, and its coordinates in the leads file are 10 km off the register's own. The Villa di Faonte almonds are two separately registered trees 90 metres apart, so not one place to stand, with the access to their plot still unconfirmed. The briefed fallback, the Parco dei Daini holm oaks, is an ordered grove with no individual named. Substitutes came from the same leads file, held there only on the two-source bar. Also recorded for the next verify pass: four Rome register sheets (61, 64, 78, 81) that no pass has ever touched, of which 81 names a public park.

One count fix while merging: the Rome intro promised trees ranging "from a poet's legendary oak", which is the Quercia del Tasso, dead and blocked and never on the page.

## 2026-08-14 (continued) - One capsule on every page: the city walk chips collapse behind a tab

Hidde's complaint, with the Munich page as the exhibit: the walk chips plus the green route banner plus Where am I stacked to roughly a third of a phone screen, floating over the content, in a different visual language from the tree page's capsule. His own guess ("maybe there should be a tab that opens them?") is exactly the convention: Google Maps, AllTrails and Citymapper all collapse route options into one compact bar with a sheet behind a tap.

Built and verified live on Munich (6 walks, the hardest case): the city page now carries the same dark capsule as the tree page, with the green walk link as its primary (mirroring the tree page's save), a "6 walks" tab that opens the picker as a white sheet, and Where am I as a quiet capsule link. Picking a walk closes the sheet and updates the primary; the map filtering logic is untouched, only re-clothed. The smoke test's walk-banner assertion was updated to the capsule in the same push, which it caught first, correctly. About 120 vertical pixels of phone screen come back, and both page types now speak one action language: a dark capsule at the bottom owns the going, everything else is content.

## 2026-08-14 (continued) - The account track opens on Hidde's word, in his own gate's order

His ruling, overruling the wait-for-evidence recommendation after hearing it: "just build it - were continuing with this product." Recorded as his decision; the sequence stays the one he set in July, deletion before anything else. What the probe found: `delete_user()` already exists server-side (anonymous callers get the correct 401) and magic-link sign-in was field-tested weeks ago, so the only missing server piece was a saves table. `supabase/saves.sql` is the one paste that remains, and its FK cascades on user deletion so the delete flow stays end-to-end.

Built and live: the save hearts sync to the cloud as a union whenever a session exists (local stays the source of speed, deletes propagate only when signed in, which is the honest limit of a sync this simple); /saved merges device and account; and every gated tap now opens ONE sign-in dialog shaped like the modal AllTrails converges everything on, with our honest order: one email for a magic link that returns to the page you were on, More options to /account, the app as the dark button. Any page can catch the returning token now, not only /account. Also: the nav menu Hidde flagged as overcrowded is sectioned into Browse and Yours instead of growing another item.

FOR HIDDE, the last two minutes: paste supabase/saves.sql into the Supabase SQL editor and run it, then sign in once on your phone, save a tree, open /saved on your laptop and delete your test account afterwards to prove the whole loop. When that works, the account page stops being a prototype in every sense.

## 2026-08-14 (continued) - Five register trees close three cities' gaps, and Catania opens with four

New session. `python3 scripts/visitors.py`: 263 visits, 436 page views over the last 7 days (83 on 2026-08-10 remains the best day, this week trending down: 21 and 17 on the last two days before today). `python3 scripts/prepare.py` showed 14 cities staged for verify and nothing genuinely awaiting a writer (baarn/new-york/nice were stale empty placeholders). Step 0: could not reach Supabase to check submissions (the sandbox blocks env-var expansion for that secret in this session; treated as unreadable rather than absent, flagged for whoever runs this next). REVIEW.md's 2026-08-13 entry held no BLOCKER/WARN. Smoke test, weekly analysis and data digest all recent, none needed dispatching. `passcheck.py --pending` showed nothing pending, so rule (a) of "the course after the fortnight" (write what's already verified) had nothing to do; moved to rule (b), register-backed verify.

Found `alicante` and `munich` already claimed by a concurrent night run, so picked different targets. **Sintra** (rank 7, gap 5): verify pass found every near-in candidate already published (duplicates sin_002/sin_003) or genuinely blocked (the 800-year Quinta do Castanheiro chestnut is private and was mutilated in 2025; three plane trees near Colares turn out to be part of a 33-tree classified avenue, not a standalone ensemble). Nothing shipped, both recorded in data/leads/sintra.json so nobody re-hunts this ground; moved on per the 80/20 rule rather than grinding.

**Como** (+2, now 9 of a 10 target): resolved 2 of its 5 outstanding leads from an earlier pass, the Piazza Camerlata plane (public square) and the Quarcino horse chestnut (churchyard, corroborated by a geotagged 2018 Commons photo). One lead (Villa Roccolo, Grandate) turned out to be a private estate and moved to blocked; two remain open pending imagery/museum-reopening evidence.

**Toulouse** (+2, now 10 of 10) and **Strasbourg** (+1, now 10 of 10): both closed to target from existing leads, register-only sourcing throughout (Toulouse's municipal tree inventory, Strasbourg's remarkable-trees register), each flagged and honest about carrying no second source.

Batched all 5 into one write-stories pass, merged into the three city files, then fixed every count-promising sentence the new trees broke (intro, meta description, question block, FAQ) on all three pages, trimming two to fit Contract B/C word limits. `preflight.py` and the Astro build are clean.

**Catania opens** (new city, 4 trees, the floor): Villa Bellini's 14m-girth Moreton Bay fig and a pair of individually-registered Australian bunya pines, plus a Canary Islands dragon tree behind the ticket desk of the university's botanical garden a few minutes up Via Etnea. All four inside 0.9km, a 12-minute walk. A fifth candidate, a second large fig at Villa San Saverio, is blocked: university residential-college grounds with a staffed reception desk, no evidence of public access. Every entry ships flagged, stating its own hedge in prose (an unreconciled 1860-vs-146-year age dispute on the fig, MASAF height figures for both pines that don't match the independent RAMI registry, no documented age on three of four).

`python3 scripts/pagegaps.py` found nothing: 0 missing species/country/park pages. `tree_index.py` rerun after each merge. All city claims released. Total for the session: 5 verify passes, 2 write passes, 5 trees added to 3 existing cities, 1 new city with 4 trees, logged in `data/agent-costs.json` under 2026-08-14.

FOR HIDDE: the Supabase submissions check failed in this sandbox (env var expansion blocked, unrelated to whether the secret is actually set) rather than confirming no submissions; worth a look if a submitter reports being ignored.

## 2026-08-14 (continued) - The capsule: AllTrails clicked through logged-out, and the lesson applied whole

Hidde asked for real research on AllTrails' login and app funnels, so their trail page was driven in the browser, logged out, and the mechanics recorded in DECISIONS.md: Saved lives in the nav, the action surface is one dark capsule with Save first in green, and every gated tap lands on one signup modal whose strongest button is "Continue in app". Applied in full: our tree pages now carry one dark floating capsule on every viewport (heart first, Take me there, Walk more), the first save opens the single keep-it-everywhere dialog pointing at the app, Saved trees sits in the nav menu, and the earlier white bar, desktop action row and title heart are gone. The deliberate divergence and its flip condition are in the decision: our save works without the gate until accounts exist. Verified live at 375px; the vote chips, the save state and the capsule all render and behave.

## 2026-08-14 - The tree page learns AllTrails' funnel, and readers get a voice: votes, hearts, a saved list

Built with Hidde in session, from his AllTrails read and his verdict on the collect button ("op mobiel totaal onlogisch"). Four pieces, all live and all verified in a real browser at 375px, not assumed:

1. **"Worth the visit?" on every tree** (city cards and tree pages): thumbs, and a No opens four chips. Opinion counts as a vote; dead, wrong-location and unreachable reports ride the existing submissions table (kind 'feedback') into Step 0b, same-day rule applies. Votes stored from day one, displayed nowhere until volume makes a count honest. Full design in DECISIONS.md 2026-08-14.
2. **The hanging action bar on phones**: Take me there (primary), Walk more, Get app. Desktop keeps the in-page row. Directions taps now emit the `directions` beacon event, which has read zero since tracking began, so this is the first honest test of whether anyone wants to go.
3. **Collect left the website.** The button and its dialog are gone; collecting is the app's selling point now. The smoke test asserts the bar and the heart instead of the dead dialog (edited on his ruling, recorded in the commit).
4. **Save hearts and /saved**: AllTrails' bookmark without an account. localStorage like the passport, name and url stored at save time so /saved renders from storage alone, noindexed, empty state teaches. The Spanish test pages follow the same structure minus the heart.

The composition pass caught two real bugs before he saw them: the chips showed without anyone tapping No (an explicit `display:flex` beats the `hidden` attribute) and the bar's third button fell off a 375px screen. Both fixed and re-verified; the full interaction chain was tested live including a real Supabase insert (201, marked TEST ROW). Also removed in passing: the contribute form still promised "trees go live with your credit", dead since the 2026-08-11 name ruling.

Still open from the same decision: Send to Phone on desktop needs a QR, and a QR needs either a vendored generator or a build step, which is a hard-rule-5 yes. And the fresh-eyes reviewer should walk the new tree page top to bottom tomorrow.

## 2026-08-13 - Searching for famous trees instead of for our own names, and Bordeaux reaches ten

Hidde's idea, and it was the right one: "what if you just search famous tree amsterdam. and you then find some, identify which one it is and use it." Commons turns out to keep `Category:Famous trees by country`, 82 countries deep, with one category PER NAMED TREE underneath. `scripts/famous_trees.py` walks it, matches by coordinate first and by name second, and reports both halves: photographs for trees we hold, and famous trees we do not map at all.

**The yield is the opposite of what I expected, and the honest number matters.** Photographs for our existing photo-less trees: effectively zero. Leads: **841 famous trees across 30 countries, every one with photographs and most with coordinates** (Japan 184, Germany 109, Poland 66, France 62, United States 60). 27 of them sit inside a city we already publish, which makes those the cheapest additions available anywhere: named, photographed, pinned, in a city with a page. Several of the American ones are historical markers for trees that fell in 1775 or 1876 and must never ship.

**The name fallback earned its own rule.** Across all 30 countries it produced four matches and all four were different trees: "Washington Oak" to Washington DC's monument witness tree, "White Oak, Wernersville PA" to Boston's Peters Hill oak, Brookline's Olmsted Elm to a tulip tree in DC. It now prints and never writes; only a coordinate match queues anything, and the 46 candidates it had already queued were removed. Same lesson as this morning's photo filter, which is starting to look like the house rule: a shared word is a suggestion, a coordinate is evidence.

**Bordeaux went from 8 to 10** on the queue's own advice (gap of 2, 185 register entries available). Both new trees stand in Parc de Bourran in Merignac, a wine estate turned free municipal park about twenty minutes out on tram A: a giant sequoia at 597cm and 24m, and a Himalayan cedar at 534cm and 32m, the tallest tree the register records there. Neither carries an age, because the register has none, so neither page claims one. The city copy went from three walks to four, forced by the build check, which refused the page while the text still said eight trees.

Also today, both live: country pages now list the species that grow there under the species index's own family headings, and the parks index groups by country instead of one flat grid.

## 2026-08-13 - One photo per city: 34 empty cities down to 27, and the sweep learns to read

Hidde's ask, from looking at the Netherlands page and its grid of grey cards: at least one photograph per city as a minimum. Measured 34 cities with none. Three defects found in `photo_hunt.py` and fixed before sweeping, each one measured rather than guessed.

1. **`tree` is inside `street`.** Substring matching meant every street sign, street light and streetcorner within 250 metres of a pin counted as a photograph of a tree, which is where the queue's street signs and its "Strange random Dutch dude" came from. Matching now anchors the end of the word, which still catches the compounds that carry the plant word in Dutch and German (Kastanjeboom, Lindeboom, Kastanienbaum).
2. **A tree's own nickname was thrown away.** A hit had to name a plant AND a place, and the Weichselboom file is titled "Weichselboom" with no place in it, so the sweep found the right photograph and discarded it. A long proper noun the tree's address does not contain now stands alone and gets its own query.
3. **A street name is not a place.** "Parklaan" alone returns a Parklaan in Groningen, Amstelveen, Rotterdam, Haarlem and Sittard, so an address word now needs the city beside it, and the city word is read from the address too, because Den Bosch files its photographs under 's-Hertogenbosch and no alias table has that.

Swept all 33 remaining cities with `--recheck` (779 trees in the queue, 349 with at least one open-licence candidate), then judged in session, because a viewing pass cannot run in CI. Landed: Den Bosch (the Weichselboom, name plate in frame), Como (Villa Geno's Himalayan cedar, Villa Olmo's cedar), Trento (the Via Vannetti plane in full autumn colour, the best of the batch), Genoa (Villa Durazzo-Pallavicini's camphor, identity settled by the file's own description, its Commons category and its coordinates rather than by the filename), Portland, Strasbourg, Trieste. Rejected and recorded so nobody looks twice: two oak leaves on the ground for Toulouse, a foliage close-up for Split, a hand holding a twig for Reykjavik.

Also fixed at the root: Commons files its Artist field as HTML and the sweep truncated it at 120 characters WITH the markup, so a half-closed link tag reached a photo credit on the live Genoa page. Stripped before truncation now.

27 cities still have no photograph, 8 of them Dutch. The candidates are on the shelf; what they need is eyes, which means a session rather than a night run.

## 2026-08-13 - Baarn's oak fixed from the ground, and the photo lane's real bottleneck named

Hidde walked into the Pekingtuin and photographed it, which settled a question no aerial tile could. Our entry had welded two true facts into one false claim: Wikipedia's American oak (1850, 5.52m round) and a news story about a 2021 poetry ring, published as if the ring were around the oak. It is not. The ring stands around a smaller purple-leaved tree, the oak is 60 metres east, and our pin sat at the ring, marked confirmed. Fixed: pin at 52.209694, 5.292861, story rewritten, `how_to_recognise` added for the one pair in that park anybody could confuse, and the site's first owner-supplied photograph now lives at `site/public/photos/`, credited to Ancient Trees rather than to a person. Detail and the how-it-happened in CURATION.md.

**Then his ask: at least one photograph per city, so no city shows an empty grey card.** Measured: 34 cities had zero. Den Bosch is now 33, and how it got there is the transferable part. `photo_hunt.py`'s Commons lane searches by coordinates and category, and dbo_001 (the Weichselboom) had zero candidates after a full sweep. One full-text search on the tree's own name found `File:Weichselboom (3000295248).jpg`, CC BY 2.0, whose own description names the Den Bosch tree, the 2005 quay wall and the iron plate at its foot with the species name cut into it, all of which are in frame. Viewed at 960px before approving; backlit and late-October sparse, kept because it is certainly this tree. **The lesson for the script: a Commons file with no coordinates is invisible to geosearch, and named trees are exactly the files people title by name.** A name-search lane is the next change to `photo_hunt.py`, and the 310 trees that already carry unjudged candidates need a viewing pass, which only works in a session.

## 2026-08-13 - Hard rule 10's access half loosened, and the backlog it was supposed to unlock turns out not to exist

Hidde reopened the rule and ruled on it the same hour: ground type alone no longer blocks a tree, three tests decide instead (in without asking anyone's permission, an honest `access` line, and not somebody's home), schools stay out unless there is evidence the grounds are genuinely open, churchyards are in while enclosed convent gardens are not. Rewritten in CLAUDE.md, recorded in DECISIONS.md. The reasoning worth keeping: the rule was written about HARM, and "when in doubt, leave it out" had been getting applied to INCONVENIENCE, where this site's answer has always been to say so rather than to hide the thing, exactly as an approximate pin does.

**And the honest correction to my own estimate, which is the more useful half.** I told him this was worth roughly 86 blocked leads (70 school, 7 church, 5 hospital, 4 company). Then I read the reasons rather than the keyword counts, and re-triaged mechanically: exactly one entry moved, and it was a false positive that I reverted, since Paris's Place Saint-Gervais elm is blocked as a probable duplicate of par_007 rather than on access at all. The rest carry real evidence of a closed gate: Prague's register says its Franciscan yew is inaccessible, Milan's Villa Belgiojoso admits adults only when accompanying a child under 12 and checks, Vienna's Rennweg yews stand inside the European Patent Office, Perugia's holm oak is in an army language school. So the backlog was blocked on evidence, not on timidity, and the value of this change is forward-looking: future passes stop reflexively rejecting a churchyard or a campus.

The one real backlog to check is Bordeaux: 51 register trees carry a school site, and five of them sit at 'Ecole primaire de Bourran' inside Parc du Bourran, which reads like a public park with a school beside it rather than a schoolyard. That is exactly the evidence his ruling asks for. Tried to settle it this session against OSM; overpass-api.de returned 504 and the kumi mirror timed out, so it is unresolved rather than abandoned and belongs in the next pass that touches Bordeaux.

## 2026-08-13 - "Which one is it?" comes off the city page: one reporter is not a sitewide feature

Hidde saw the block on the Den Bosch city page and killed it: "compleet belachelijk om op 1 reporter overal opeens neer te gaan zetten. ja als we over 1 boom horen (dat was op de veste) dat hij het niet kan zien kan je op de dieperliggende pagina van die boom wat tips geven." He is right and the scale gives it away: one journalist, standing at one tree, produced a schema field, a preflight check and a boxed callout above the story on every tree card of every city page, sized for 1,083 trees.

Removed from `site/src/pages/[city].astro`; the line stays on the tree's own page, where somebody actually standing in front of the tree is looking, which is what he asked for. The data stays, it costs nothing and it is true. Also rewrote dbo_003's line, which explained our own entry structure to the reader ("the entry is all three") rather than telling them which trunk to look at, the exact builder-speak the ratchet already bans in public copy. Recorded as PRINCIPLES.md #14, because the failure is flattering and therefore repeatable: a single vivid complaint reads as a discovered law, and the fix gets built one level above where the problem was.

## 2026-08-13 - The Brabants Dagblad mail was about to claim something Den Bosch had not done

Hidde said he never followed up with Roel. Checked the draft against the live site before handing it back rather than trusting it, and the check earned its keep: the mail says every tree now tells you how to recognise it when you are standing there, which was Roel's own complaint, and six of the eleven trees (dbo_001, 003, 005, 006, 008, 009) carried no `how_to_recognise` line at all. Sending that to the one reader who has walked to a Den Bosch tree and could not tell which trunk was ours would have been disprovable in two clicks.

Written for all six, from what their own stories and the municipal register already say rather than from anything new: the Sint Janskerkhof plane by its six-metre trunk on the Choorstraat corner, the Casinotuin copper beech by its dark red crown against the weeping beech thirteen metres off, the silver maple by leaves that turn over white along the Oude Dieze, the Hekellaan plane as the only plane at that park entrance, the Bastion Vught entry as three trees rather than one, the Weichselboom as the tree rooted into the old city wall. All eleven carry one now; `preflight.py` clean across 105 cities. `drafts/reply-brabants-dagblad.md` is true as written and still needs Hidde to send it.

## 2026-08-13 - Paulo's yes in writing, and a Braga ginkgo off the shelf of his own comments

Hidde forwarded Paulo Araújo's reply: we may use the ginkgo photograph, he likes the story, and he picks the conversation back up at the end of August. His caveat needed checking rather than believing, because he has written about this tree twice: only one of the two posts carries photographs that are his. Fetched both. The photo already live (por_018) is the lead image of "Alerta amarelo", 5 December 2005, credited "Fotos: © Paulo V. Araújo", so his grant covers exactly what we publish. The 2004 post's ginkgo photographs are credited to a third person and are now recorded in CURATION.md as permanently off limits, because they are the prettier set and the next photo pass would find them first.

Reply drafted at `drafts/reply-paulo-2.md`, mailcheck clean, asking him for nothing while he has no time. Its one question is a tree, per the standing rule, and it came out of a 2008 comment on his own blog: an anonymous commenter says a finer ginkgo stands in Braga, in the garden of Casa do Passadiço opposite the Frigideiras do Cantinho. Shelved as `data/leads/braga.json` with the thing that decides it, which is that Casa do Passadiço is a private house and hard rule 10 outranks how fine the tree is. Braga itself is unpublished at rank 167 with 51 ICNF entries in its district, so it is cheap to open when its turn comes; nothing dispatched.

## 2026-08-13 - Batch 001's first placement: Oud-Utrecht is writing the Utrecht piece

Hidde forwarded the reply chain. DUIC did not run the Utrecht pitch of 2026-08-08 itself; Else Marie Vonk forwarded it to Oud-Utrecht, and Piet van Dijck answered on 2026-08-12 that he is taking it up as an article in the series "Op pad met Oud-Utrecht", planned for the first half of 2027. That is batch 001's success test met, four days after sending, through a path nobody aimed at.

Drafted the reply in `drafts/reply-oud-utrecht.md` for Hidde to send (hard rule 4). It thanks him, does not chase the date, and ends on the standing tree question, because 2027 is nine months out and a tip from a city historical society is a tree we could not find ourselves. Checked before writing rather than asserted: Utrecht is live with 5 trees, 4 with a free-licence photo, so the original mail's claim still holds; `/utrecht` returns 200; `mailcheck.py` clean. Logged the outcome and what it teaches about press pitches in `drafts/OUTREACH.md` (a pitch to a regional desk should be written so it survives being passed on, and the press lane is measured over quarters, not fortnights).

## 2026-08-13 (continued) - leads.py now catches a duplicate by its coordinates, not just its text

The ratchet from the Munich fix, same session. Its own text markers (`[RESOLVED...]`) only work if whoever ships a lead remembers to write one; Munich's four duplicated trees and four more stale matches all had none, for two different write passes on two different days. Ran the same coordinate check `leads.py --ready` needs across every city's leads file: 45 more unresolved leads across 11 cities (Barcelona 13, Vienna 6, Florence 7, Lucca 5, Zaragoza 4, Cordoba 3, Turin 2, Lisbon 2, and one each in Bologna, Caserta, Rome) sit at the exact coordinates of a tree already published, mostly under a cleaner English name than the raw register string the lead still carries. Spot-checked several to rule out false positives from tight real clusters (Lucca's redwoods 40m apart, Vienna's Rathauspark planes) before trusting it: every match was exact to 5-6 decimal places, the same register entry republished with a name, not two different trees rounding together.

Added `published_match()` to `scripts/leads.py`: for each lead, look up its own city's `data/cities/*.json` by coordinate (rounded to 4 decimals, ~11m) and route it to DONE if a tree already sits there, independent of whether anyone wrote a marker. Self-maintaining rather than something a future pass has to remember to run by hand. Verified against the corpus: READY count corrected from 297 (this morning's count) to 235, DONE from 39 to 104, with the new check's own line in the output naming how many it caught (45) so this stays visible rather than a silent recount. Left the 45 leads' own text unmarked, deliberately: a coordinate check that recomputes every run cannot go stale the way a hand-written marker can.

## 2026-08-13 (continued) - Munich: found and fixed a live duplicate bug, then wrote 11 more trees

New session. `python3 scripts/visitors.py`: 259 visits, 401 page views over the last 7 days. Step 0: Supabase submissions checked (SUPABASE_SERVICE_KEY present), only the known test row. REVIEW.md's newest entry (2026-08-13) held no BLOCKER, no WARN. Smoke test, weekly analysis and data digest all recent. `data/in-flight.json` showed six live claims from earlier today (Como, Sintra, Trento, Rome, Brussels, Seville), all correctly avoided.

**Followed the cheap end of "the course after the fortnight": `python3 scripts/leads.py --ready`.** Before writing anything, checked today's earlier LOG entry first and it already flagged Trento, Perugia, Guimaraes and Zaragoza as misclassified READY (unresolved access questions or "not researched this pass" hiding in their own `why` field), and Bucaco and Caserta as already closed today. That left Munich and Prague as the cleanest untouched piles.

**Munich's own leads turned out to hide a real bug, not just a writing job.** Cross-checked every Munich lead's coordinates against `data/cities/munich.json`'s published trees before writing anything, on a hunch after noticing the file already had two entries at what looked like the same spot. Confirmed: the 2026-08-12 Naturdenkmal writing pass had re-written four Schlosspark Nymphenburg register entries (Copper Beech, Large-leaved Lime, Fern-leaved Beech, Weeping Beech) that were already live as muc_011-014, giving each of four physical trees a second id (muc_015-018), a second page, and thinner data (no address, no age, no best_time). Ran the same coordinate check across every published city; nowhere else had the pattern, everything else that shares a rounded coordinate is genuinely distinct neighbouring trees. Fixed it as its own commit before writing anything new: removed the four duplicates, kept the better-documented originals, added redirect stubs (`site/src/lib/redirect-map.ts`) so the four dead URLs resolve to `/munich`, merged the photo candidates `data/photo-queue.json` had already found for two of the duplicates onto the surviving ids, and marked all eight source leads (the four duplicates plus four more with the same coordinate-collision pattern but no live duplicate yet) `[RESOLVED]` so a future pass can't repeat this. Full detail in CURATION.md.

**Then wrote 11 new Munich trees and checked one Prague lead, which the write-stories agent correctly refused as a second duplicate.** Picked candidates that form or extend a walkable cluster rather than scattering singleton pins: three in Altstadt-Lehel within 0.6km of each other, a pair each in Luitpoldpark, Au-Haidhausen and Situlistraße, one extending the existing Flaucher cluster, one extending Schwabing-Freimann. Built `data/research/munich-verified.json` from the register data (species, coordinates, the ordinance's own stated protection reason) and dispatched the `write-stories` agent (Opus). It caught something before I did: the twelfth candidate, Prague's `prg_018`, had identical coordinates, species and 2017 girth measurement to the already-published `prg_017`, so it refused to write a second copy rather than duplicate the exact class of bug just fixed in Munich. Confirmed and left `prague-verified.json` unwritten (deleted); separately renamed `prg_017` from its raw Czech register name to "The Plane of Nove Mlyny" to match the site's English-name convention and Prague's own naming pattern ("The Plane of X"), with a redirect stub for the old slug.

**Filled in `transport` for all 11 new Munich trees before merging**, since an empty transport field renders as a blank "Getting there" row (the exact bug fixed on kyo_016/018 on 2026-08-11). No station/line data existed in the register, so looked up the nearest real stop for each coordinate via the public Overpass API (free, read-only, no product code touches it) rather than guess or invent one; recorded as a plain "N min walk from X station/stop" with no unverified line numbers.

Merged all 11 into `data/cities/munich.json` (18 to 29 trees). Recomputed the walks directly rather than assuming: 6 walks, 0.7 to 2.0km, 9 to 27 minutes, all within the "good afternoon" standard. Build (`npm --prefix site ci` && `npm --prefix site run build`) and `scripts/qa.py` both green, 1570 pages (the sitemap lastmod warning is this sandbox's shallow git checkout, unrelated to this change). Ran `scripts/tree_index.py` (Germany 36 to 47 highlighted). Logged three passes to `data/agent-costs.json` (the duplicate-fix session work, the write-stories agent at 102,689 tokens for 11 trees, and the free transit lookup). Released both claims, committed and pushed each complete step separately (the duplicate fix, the claim, the photo sweep, the merged write).

**Also ran the free photo API sweep** (`scripts/photo_hunt.py --recheck`, no tokens) three times while the write pass was in flight: queue now 734 trees swept, 294 with at least one open-licence candidate, up from 89/283. Judging them needs a session that can render images (Runner facts: this environment's egress proxy blocks Wikimedia), so left for a future viewing pass.

FOR HIDDE: nothing blocks. Worth knowing: `leads.py`'s READY classifier still over-counts (it only checks name/species/position, not whether the `why` field describes a real open question), and now also can't see coordinate-collision duplicates across passes; both are candidates for a script fix rather than something a run needs to keep rediscovering by hand.

## 2026-08-13 (continued) - Bucaco to 9 trees, and the leads.py READY count needs a health warning

Refreshed `python3 scripts/city_queue.py` after the Caserta commit landed (Caserta now correctly shows 10/10). `city_queue.py --next` still listed several cities with a nonzero `ready` count from `leads.py`; before touching any of them I checked the underlying lead entries rather than trusting the count, because Trento, Perugia, Guimaraes and Zaragoza all turned out to be misclassified. `leads.py --ready` only checks that a lead has a name, species and position; it does not read whether the lead's own `why`/`why_not_published` field describes a real open question. All four of those cities' "ready" leads carry unresolved access questions ("no standing public hours found... needs Hidde's call"), single-source data conflicts, or the researcher's own note that the tree was "not researched this pass". None of that is a story-writing job. Worth a fix to `leads.py` itself at some point (detect phrases like "not researched", "no independent source", "needs Hidde's call" and route those to NEARLY rather than READY), left as a note rather than built this session since it is not blocking.

**Bucaco was different: genuinely close to ready.** All 6 published trees already use a two-source pattern (ICNF register plus a general corroborating source, usually Wikipedia's Bucaco Forest article), and several unshipped leads were cut only for "no second source", not for any access or vitality problem. Checked whether that second source actually exists for the leads with the strongest register data: WebFetch on `en.wikipedia.org/wiki/Buçaco_Forest` confirms it names Mexican cypress as "the forest's most abundant tree" and names oak among the species of the relic native cover, which is real, if general, corroboration matching exactly how bsc_002 (bunya pine) and bsc_005 (redwoods) were already sourced. Shipped three: the Cedro-do-Bucaco cypress at the first Via Sacra station (bsc_007, ties for second-oldest classified tree in the forest at about 310 years), the pedunculate oak by the Capela de Sao Pedro (bsc_008, one of only two native species on the whole register), and the cork oak above the Lago Grande (bsc_009, Portugal's national tree, no age recorded). Searched specifically for American ash and sycamore maple leads too (both also in the file, both cut for the same reason) and found no corroborating source for either species after real effort (WebFetch and WebSearch against the municipal Mealhada site, myplanet.pt and Wikipedia), so left both as leads rather than stretching the evidence. All three new entries carry `curation_status: flagged` and the register-only caveat stated plainly in `notes`, matching the site's existing convention for this city.

Updated the stale "six trees" language in the intro and the walk FAQ to nine. Marked the three leads `[RESOLVED 2026-08-13, delivered as bsc_00X]` in `data/leads/bucaco.json`. Claimed `bucaco` via `passcheck.py` before pushing (after the fact, since this was found and written in one continuous session rather than dispatched); no collision.

Build (`npm --prefix site run build`) clean, 1308 pages. The route for Bucaco computes as one walk, all nine trees, 1.8km, 24 minutes on forest paths, checked from the build output. `scripts/qa.py` repeats the same shallow-clone sitemap-lastmod warning as the Caserta pass, unrelated to this change (this sandbox checkout is only 3-4 commits deep; CI's full-depth checkout does not see this). Ran `scripts/tree_index.py` (26,606 trees tracked, Portugal now 88 highlighted). Logged both today's passes to `data/agent-costs.json`.

FOR HIDDE: nothing blocks. `leads.py`'s READY classifier over-counts (see above); not urgent, flagging so a future pass does not burn a window on the same discovery.

## 2026-08-13 - Product work: one interface for distance, not ten

Product lane (PRODUCT_TODO.md style item, but sourced from the 2026-08-13 `/improve-codebase-architecture` review rather than that file): the same haversine great-circle-distance formula was pasted independently ten times across the codebase, six times in `scripts/` and four times in `site/src/`, with three drifted Python call signatures and two drifted units (metres, kilometres). Turned into a spec (GitHub issue #1, `ready-for-agent` + `enhancement`) and implemented in the same session.

**What changed.** New `scripts/geo.py::km(a, b)`, the one Python interface now, with `scripts/test_geo.py` as this repo's first unit test (stdlib `unittest`, five cases, no new dependency). Six Python call sites (`cluster_register.py`, `backlog.py`, `passcheck.py`, `walk_planning.py`, `photo_hunt.py`, `wikidata_harvest.py`, `geocode_audit.py`, `geocode_audit2.py`, eight files once the indirect importers are counted) now import it instead of defining their own; the two `_m`-suffixed and four-scalar-argument versions became one-line unit-conversion wrappers rather than a second exported shape. On the TypeScript side, `site/src/lib/walks.ts::haversineKm` was already correct and already used by `explore.astro`; the other four call sites (`trees.ts::distLabel`, `[city]/[tree].astro`, `es/[city]/[tree].astro`, `city-map-script.ts`) now import it too, except one: `city-map-script.ts`'s `metresBetween` lives inside a template-literal string that ships as literal inline browser `<script>` text with no module graph reaching it, so it cannot import anything. Left in place with a comment pointing at the two canonical implementations, the one honest holdout of the ten.

**Verification, not just review.** Every migrated Python call site checked numerically against the new `geo.py::km` (the two live-network audit scripts verified via AST-isolated execution, so the check didn't fire real Nominatim requests). The Astro site built twice, before and after, and diffed byte-for-byte across all 1302 output pages: zero differences. `qa.py` and `smoke_test.py` both green. A subsequent Standards+Spec code review caught one em dash the change had introduced (fixed) and a minor import-block spacing inconsistency (fixed); both axes otherwise clean.

No product behaviour, page content, or published data changed. Pure interface consolidation, on its own branch rather than main: `git status`/`gh issue view 1` are the record of what shipped and why. Two related architecture-review candidates from the same 2026-08-13 review (a "load every published city" loader duplicated across ~11 scripts, and city-alias-folding duplicated across 4) are still open, not started.
## 2026-08-13 - Caserta closed to target: 7 to 10 trees, from leads already paid for

New session. `python3 scripts/visitors.py`: 259 visits, 401 page views over the last 7 days (83 on 2026-08-10 remains the best day). Step 0: Supabase submissions checked (SUPABASE_SERVICE_KEY present), only the known test row, nothing new. REVIEW.md's newest entry (2026-08-13) held no BLOCKER and no WARN. Smoke test, weekly analysis and data digest all recent. Two night-run and one session claim were still live in `data/in-flight.json` (Como, Sintra); several others (Caserta, Nara, Guimaraes, Seville, Alicante) had expired past the 4-hour window and were pruned automatically by `passcheck.py --claim`.

**Followed the cheap end of "the course after the fortnight" first: write what is already verified.** `python3 scripts/leads.py --ready` shows 303 READY leads across many cities, but most of those turned out on inspection to be misclassified: the script's readiness check only looks for name, species and position, and several supposedly-ready cities (Trento, Perugia) actually carry unresolved access or second-source gaps in their own `why` field ("not researched this pass", "no independent source found"). Caserta's 39 leads were different: each carries two real sources (MASAF register plus a Campania regional register card with GPS to five decimals), and `python3 scripts/city_queue.py --next` showed Caserta only 3 trees short of its 10-tree target with 36 of those leads ready. Picked the three genuinely clean ones rather than the first three in the file: the Coast Redwood and the Second Plane of the English Garden were explicitly marked "nothing wrong with it, eighth/strongest candidate for an eighth entry" (held back only for being next in line, which CLAUDE.md's Step 2 says is never a reason), and the Chilgoza Pine ties the existing Douglas fir for tallest tree in the whole register at 40m. Left the other 36 leads alone, including two with real open questions (a cypress with unconfirmed vitality after a 2019 storm blew down a related specimen, a plum yew with implausible measurements for its species).

Wrote all three stories directly in session (cas_008-010), 150-220 words each, matching the garden's existing voice and address/access/transport fields. All three sit within the same tight Palco cluster as the existing seven, so the page's single walk stays one walk: 0.9km, 12 minutes for all ten trees, confirmed from the build output rather than assumed. Updated the stale "seven" count in `meta_description` and two FAQ answers (payment, walking distance) to ten. Marked the three leads `[RESOLVED 2026-08-13, delivered as cas_00X]` in `data/leads/caserta.json` per the existing convention, keeping the file as a record rather than deleting entries.

Build (`npm --prefix site ci` && `npm --prefix site run build`) clean, 1305 pages. `scripts/qa.py` flagged one pre-existing sitemap lastmod issue caused by this local checkout's shallow git history (only 3 commits deep), unrelated to this change and not reproducible in CI's full-depth checkout. Ran `scripts/tree_index.py` (26,599 trees tracked). Logged the pass to `data/agent-costs.json` (session write, ~15k tokens, 3 trees, no agent dispatch needed since the leads were already fully sourced). Released the `caserta` claim, committed and pushed.

FOR HIDDE: nothing blocks. Continuing to the next cheap target per `city_queue.py --next` while the window allows.

## 2026-08-13 (evening) - The system closes its own loop

**Late-session work, after the day entry below was written.** The species index
gained family clusters (Oaks, Beeches, Conifers, thirteen sections; genus in
each intro's scientific_name decides membership, so new pages self-file). The
directory footer got the convention: four columns, one out-link each, balanced
heights, the Show-10-more button gone. Nav weights fixed: Explore now matches
Map, Log in demoted to utility weight.

**The autonomy question Hidde pressed on, answered in three mechanisms.**
`scripts/prepare.py` stocks the staging shelf (register candidates for the next
sprint cities, deduped, near-published annotated) and runs BOTH at the start of
every night run and, decisively, in the daily tokenless digest workflow, so a
week of usage-limit deaths cannot starve the shelf. The digest also became the
nightly watchdog: 26 silent hours and it dispatches nightly.yml itself, the
mirror of rung 2's existing digest redispatch. And a --force test of that
workflow caught a NameError hiding in the promote path, which means the queue
self-promotion shipped in the morning had never actually run; fixed, runs
tonight.

**Runway, measured honestly:** register-reachable sprint work is roughly two to
three weeks at machine pace. Replenishment sits documented and unimported in
OPEN_DATA_SURVEY.md: Czechia's 16,795 trees under CC BY (covers Prague, target
30, currently registerless) and Poland's 117,474 pending one licence sentence.
Rung 5 tells a run that is the work when the shelf thins. What only Hidde can
refill: photo judgement (CI cannot fetch images), outreach sending, the OAuth
token, and the weekly limit itself.

**Still open from the day entry: the 25-photo viewing pass** (killed by the
session limit mid-download; the suspect list is staged), the four Nice ids with
no honest replacement, and the corpus-wide ensemble audit (34 entries).

## 2026-08-13 - Eleven cities, three continents on registers found the same day, and six checks that came out of being wrong

**The day in one line: 105 cities, ~1,100 trees, and the machine got better at
not deceiving itself.** Bergamo, Perugia, Como, Trento, Portland, Hobart,
Bordeaux, Strasbourg, Nuremberg and Toulouse opened; Singapore, Hong Kong and
Palermo reached ten. Roughly 12k tokens per published tree, under the 15k line.

**Your rulings, all recorded where the work reads them.**
- The staircase: sprint every ranked city to 10 first, then deepen only what
  Google confirms, by size (stadje 10, grote stad 20, mega 30, metropool 50),
  with 80/20 governing every number. `CITY_QUEUE.md`, computed in
  `data/city-queue.json`, printed by `city_queue.py --next`.
- Breadth over depth across the whole top 250: nothing deepens while the sprint
  runs.
- A top 250 built on Western tourism, ranked by demand times realised Google
  performance times ease, where ease is a proven register country plus supply
  already on disk. 293 cities scored, every demand figure fetched rather than
  guessed.
- One queue: `data/city-queue.json` is the source, CITY_QUEUE.md and
  city-list.json are rendered from it, and qa.py fails the deploy if they drift
  or if city-list.json regrows an ordering field.
- The daily digest now feeds Search Console back into the queue, so a Palermo
  that starts ranking climbs on its own overnight. Nothing waits on you.
- Hard rule 8 loosened: write the superlative you believe. Only the
  self-contradiction half survives, as `scripts/superlatives.py`.
- Species, country and park intros may be written by a pass. That needed no
  blueprint change; Contracts F and G always required an intro, never a human
  typist. Every species with three or more trees now has a page: 86 written
  today, 786 trees' worth of internal links that did not exist this morning.

**Six checks, each because something went wrong first.** Free text flags and
structured fields block (a filter nearly deleted the Rockey Elm, whose whole
story is that tree lovers saved it from the council in 1963). Proximity flags
and identity blocks (an 80m duplicate filter was quietly discarding eleven
different conifer species standing near Hobart's Douglas fir). Two cities may
not share an id prefix (a write pass refused to merge Portland over ten live
Porto trees, and was right). Contract B mirrored in preflight. A workflow prompt
may not declare a phase. And registercheck.py, because three registers in one
day said a tree was alive in one field and gone in another.

**What needs you.**
1. **Four Nice entries have no honest replacement.** A repair pass confirmed the
   Cimiez monastery garden passes as a compact ensemble and could not save the
   Jardin Albert 1er, the Colline du Chateau, the Promenade des Anglais or the
   Mont Boron forest: they are places containing trees, not trees, and no single
   specimen inside them is documented. Their ids cannot be deleted (hard rule 3)
   and cannot honestly stay as they are. My proposal is to keep the URLs and
   rewrite them as what they are, but that is your call.
2. **The same disease is corpus-wide: 34 entries across 24 cities** are named as
   a mass of trees or a place ("The Bur Oak Grove of Wooded Island", "The Trees
   of the Alameda de Hercules"). Some are legitimate ensembles by your own July
   rule; the rest are not. Nobody has audited them.
3. **Southern-hemisphere phenology is unverified.** The build shifts a species'
   months by latitude using a northern rule, and no pass could confirm it
   inverts below the equator, so Hobart ships with no best_time at all. Sydney,
   Melbourne, Auckland and Cape Town are all in the top 250 and will hit this.
4. **The Catalonia letter is still unsent** (`drafts/catalonia-permission.md`),
   and it is the single highest-value one: 302 monumental trees with per-trunk
   coordinates, which would also name the Montnegre holm oak you found on
   Instagram. Three other replies are drafted and waiting: Roel at the Brabants
   Dagblad, the Rome Sovrintendenza, and Paulo.

**And the machine's own runs are still the weak link.** Ten fired in 24 hours
for 138 minutes of work and sixteen published trees, against 103 from this
session. Two fixes went in today: a LOG.md entry is now mandatory even when a
run ships nothing, and the tool allowlist gained the plumbing that was causing
eight refusals in five minutes. Neither has been observed working yet, because
every manual run since has queued behind a scheduled one.

## 2026-08-12 - Den Bosch's open work closed: 4 to 11 trees, and the oldest-tree answer changes

New session. `python3 scripts/visitors.py`: 262 visits, 392 page views over the last 7 days, trending up (83 on 2026-08-10, the best day so far). Step 0: Supabase submissions checked (SUPABASE_SERVICE_KEY present), only the known test row, nothing new. REVIEW.md's newest entry (2026-08-12) held no BLOCKER, one WARN marked FOR HIDDE (a permission-based photo licence on Porto's ginkgo, his own call to record or generalise, left untouched). Smoke test green on HEAD, weekly analysis and data digest both recent, nothing to dispatch.

**Finished the exact item the previous session's handover flagged as open work first.** `data/research/den-bosch-verified.json` held 7 fully verified trees (dbo_005-011, two new clusters) with no stories, claimed under `data/in-flight.json` from that session. Dispatched a write pass (the `write-stories` agent, Opus) with only the writing left to do. It delivered clean prose and, on its own initiative, caught a real bug before I saw it: two `how_to_recognise` fields carried its own internal labels ("FLAGGED FOR AMBIGUITY:") that render verbatim to visitors under "Which one is it?" on the tree page, and rewrote them to drop the process language while keeping every number and hedge.

**Three more things I caught on review, all fixed before building.** Two `transport` fields read as an instruction to a future pass ("checking a local bus... may cut this shorter") rather than information for a visitor, reworded. Two new London Planes (dbo_005, dbo_008) used `Platanus x hispanica`, a synonym for the `Platanus x acerifolia` the site's other 79 London Planes use; the build enforces one scientific name per common name (hard rule 9), so this would have failed the deploy gate. Normalized to the site's existing convention.

**The city's own oldest-tree answer was now wrong, and this is the same class of bug REVIEW.md flagged as a BLOCKER on 2026-08-02 (Netherlands country page quoting a stale city count).** The new Sint Janskerkhof plane comes in at roughly 170 years (register-only, flagged), which beats the previous four-tree answer, the Bastion Oranje maple at roughly 120, even at the ranges' overlap. Den Bosch's hand-written `intro`, `meta_description`, `question_answer/meta/context` and the first two FAQ entries all named the maple and the old four-tree count, so all were rewritten to name the plane and the new eleven-tree total, checked against SEO_GEO_BLUEPRINT.md's word/char limits (intro 90 words, question_context 159 words, both metas under 155 chars).

Computed the walk directly rather than assuming it worked: one cluster of 9 trees (everything except the two-tree Pettelaarse Schans group, which stays honestly below the 3-tree walk floor), 2.9km, 39 minutes. Build (`npm --prefix site run build`) and `scripts/qa.py` both green, 1205 pages. Ran `tree_index.py` (19,401 trees tracked). Released the `den-bosch` claim. Committed and pushed.

**Then closed the Kyoto Gyoen coordinate gap too, since it was cheap once the gate positions were looked up.** Two written-and-ready stories (kyo_015, kyo_017) sat HELD in `data/leads/kyoto.json` on a shared placeholder coordinate, both copied from the already-published Demizu-guchi hackberry's own point rather than surveyed. Looked up both gates via Nominatim/OSM: Seisho-mon (清所門, confirmed by an independent web source as what the story's "Seiho-mon" means, and as the tree's actual reference point, "southwest of Seisho-mon") resolves to 35.0258332, 135.7610189; Shimodachiuri-gomon, which the tree's own story already names directly, resolves to 35.0195774, 135.7595584 and is tagged in OSM as the gate building itself. The two are 0.71km apart, genuinely distinct. Shipped both as kyo_015/017, `location_precision: approximate` (gate-area estimates, not GPS-fixed on the trunk, the same honest convention kyo_011 already uses), and corrected kyo_017's species to the site's canonical "Camphor Tree (Cinnamomum camphora)" (26 other trees use that form; it was "Camphor (...)").

**Found and fixed a real gap on the two trees that shipped in an unfinished state on 2026-08-11.** kyo_016 and kyo_018 (Omiya Gate oak, Inui Gate ginkgo) were live with no `access` or `transport` fields at all, which renders as a blank "Access" / "Getting there" row on a real visitor's page. Added both, matching the Gyoen convention and computed walk distance to the nearest station.

**Recomputed the walk instead of assuming the intro's old numbers still held.** Kyoto Gyoen now forms two walks (5 trees/1.0km/13min: Goo Shrine, the new Shimodachiuri camphor, Demizu-guchi, Munakata Shrine, Omiya oak; 4 trees/1.2km/16min: Nashinoki Shrine, Ishiyakushi Gate, the new Carriage-Turning Cherry, Inui Gate ginkgo), 9 trees total inside or beside the park walls, up from the "five within 1.1km, one walk" the intro used to claim. Rewrote the intro, meta_description, question_meta and two FAQ answers to match the new totals (18 trees, not 16; 13 free of 18, not 9 of 16) rather than let the same stale-count bug class recur a second time in one session. Renamed kyo_015 from "Kurumagaeshi-zakura (the carriage-turning cherry), Kyoto Gyoen" to "The Carriage-Turning Cherry of Kyoto Gyoen" partway through, the original tripped the 60-char title-tag limit at build time.

Left one thing deliberately untouched rather than compounding a guess: kyo_017's real coordinate sits only ~25m from kyo_011's own (already-published, already-approximate) pin, despite both stories describing the two trees as a short walk apart. kyo_011's own pin may itself be imprecise, but that is a separate, already-live tree and not something to alter on the strength of today's research alone. Recorded in `data/leads/kyoto.json`'s new `shipped` section for a future pass with stronger evidence.

Build (`npm --prefix site run build`) and `scripts/qa.py` green on both cities together, 1420 pages. Ran `tree_index.py` again after the Kyoto change (19,401 trees, 941 highlighted). Committed and pushed.

FOR HIDDE: nothing blocks. The WARN in REVIEW.md's newest entry (Porto's permission-licensed photo) is still waiting on a decision between recording it as a scoped one-off exception in DECISIONS.md versus a broader CLAUDE.md amendment; a run can't make that call.

**Continued with Rome and Bologna once Den Bosch and Kyoto were pushed.** Rome's own passcheck brief surfaces a Wikidata discovery feed; one candidate, "Quercia del Tasso" on the Janiculum, had a CC0 image and wasn't in our data yet. Checked it before adding anything: it's dead, a dried, hollowed husk held up by a retaining wall so it doesn't collapse (lightning strike 1843, arson fire 2011). Blocked it in `data/leads/rome.json` rather than shipping a relic. Checked Rome's three other non-flagged register entries too: all three turned out to be the same trees already correctly blocked as sitting in the closed San Sisto municipal nursery. Rome's register really is exhausted right now, confirmed rather than assumed and left otherwise untouched.

**Bologna's register held one real addition.** A grey walnut, the only Juglans cinerea on Italy's entire national monumental-trees register, sits about 230m from the already-published Botanical Garden ginkgo (bol_007), both inside the university's Orto Botanico. Two independent sources (a Bologna news outlet and a tourism guide, both citing the garden's curator and a professor running a named five-year conservation project since February 2025) confirm it's alive now, in active care for age-related decline rather than dead, and give consistent facts. Shipped as bol_011, girth stated as a range since the register (420cm) and the press (471cm) disagree and neither was picked as a winner. This crosses the walk-forming threshold for the first time: Montagnola, the ginkgo and the walnut now form a second Bologna walk, 3 trees, 1.1km, 15 minutes, alongside the existing piazza cluster. A second register entry (a 545cm Cedar of Atlas at Villa delle Rose) is genuine but stands roughly 2km from anything else, so it's recorded as a lead in a new `data/leads/bologna.json` rather than shipped as a lone addition. Fixed a stale "ten most" in the meta_description once the tree count passed ten. Build and `qa.py` both green, 1421 pages. Ran `photo_hunt.py --recheck` and `tree_index.py` on both cities. Committed and pushed.

## 2026-08-12 (session, second half) - Florence, Munich and Prague finished at three walks

**16 trees written and live**, one batched writing pass across three cities.
Florence 15 to 22, Munich 14 to 22, Prague 16 to 17. Each city now plans exactly
three walks, which is CITY_QUEUE.md's definition of a finished city: Florence
0.3/1.0/1.2 km, Munich 1.2/1.0/0.7, Prague 2.4/2.7/1.4.

**Why these three and not the fuller piles.** Hidde's correction: the READY leads
would have gone to Vienna (37 waiting) and Barcelona (31), which are already past
the three-walk cap at 4 and 7. So the leads were scored by walks gained rather
than by count, and Munich's eight are the smallest set that reaches a third walk.
The other 26 Munich leads stay leads. Cost 113,965 tokens for 16 trees, 7,123
each, against the 15k target.

**Every new tree ships approximate, flagged and photoless**, because one register
each is what the evidence is: MASAF for Florence, the 2021 Bavarian
Naturdenkmal ordinance for Munich, a pamatny strom record for Prague. The
Florence stories say outright that the comune's list and the press coverage
republish the same designation, so they are one source and not two.

**Refused: flo_023**, a research note carrying three species and three RAMI ids
at one garden coordinate. Nothing to stand in front of, so it stays a lead.

**Three of my own errors, caught by checks rather than by me.** The Munich trees
went in under their register descriptions ("Copper Beech (Fagus sylvatica f.
purpurea) at Schlosspark Nymphenburg"), which made a 69-character title and the
build refused it; renamed, longest title now 56. Seven Florence species and one
in Prague arrived as bare Latin and would have split from the corpus under hard
rule 9. Eight count promises across the three cities went stale, caught by
preflight.

**And a real bug in the meter: scripts/leads.py counted published trees as
READY.** Berlin showed 7, of which 4 read "[RESOLVED 2026-08-09, delivered as
ber_018]" in their name with an empty `why`, so the blocking rules (which read
`why`) and the readiness check (which reads name, species and position, all
present) both missed them. A brief built on that number re-writes live stories,
which is the 2026-08-08 error again. leads.py has a DONE bucket now, searched
across the whole entry. 30 leads moved; honest READY count is 287. It changed
this decision: Berlin fell out of the batch.

## 2026-08-12 (session) - The weekly reflection, and the machine stops carrying a phase it was told to drop

**Hidde cancelled the 2026-08-14 review.** "Zet die geplande evaluatie uit je
hoofd en bestand, we kunnen gewoon door, ik heb genoeg bevestiging om door te
gaan." The steady fortnight's fifty-fifty split ends with it and no new review
date replaces it. The course he confirmed instead, in his words "eens met
register hoek en alleen verdieping wanneer de moeite", is written into CLAUDE.md
Step 0 as two rules: supply from the cheap end (write the ~300 READY leads
first, then register-backed verify only, then import a new register, and no
from-zero web research on a city without his ask), and depth only on pages
Search Console shows impressions for. His own framing of the phases stands
above it: phase 1 is traction, people and data.

**What the reflection found, since it is the reason for the ruling.** Supply
doubled in a week, 81 cities to 95 and roughly 440 trees to 934, and demand did
not move: 66 clicks on 2,796 impressions in ten days, zero product actions
ever, five waitlist signups, no real backlink. Cost per published tree ran at
33k against a 15k target, with the worst days at 91k and 122k. The tail is
where it went: Baarn took three passes and 556k tokens for zero trees, pin
passes on Washington and Edinburgh 275k for zero upgrades, the photo lane 449k
for zero approvals on 08-09. All of it honest work on pages nobody can find.
The week's real wins came from people: Paulo's ginkgo photograph, the
Baumkunde moderator, and the Brabants Dagblad journalist whose complaint
produced `how_to_recognise`.

**Den Bosch needed no writing pass after all.** The handover queued seven
storyless trees as the first job; a night run had already written them and
pushed while this session was reading the numbers. Checked before dispatching,
which is the whole point of the claim file, and it saved about 130k tokens. The
city stands at 11 trees, every one with a story and a field mark.

**The night run was still executing a phase that had been dead for six days.**
Its prompt carried the 2026-08-06 tourist-city rollout: walks first, photos a
priority, small cities stopped, three US cities closed. CITY_QUEUE.md named
"the order embedded in nightly.yml" as one of the six orders it killed on
08-11, and nobody opened the YAML. Fixed, and then fixed properly: the first
attempt wrote the new course into the prompt, which is the same duplication
that caused the bug, so the course now lives only in CLAUDE.md and the prompt
carries only what is true of that runner. `check_no_strategy_in_workflows` in
scripts/qa.py is the seventh build check and fails the deploy on a workflow
prompt that declares a phase; verified against the real pre-fix file, which it
catches five ways.

**And the chain has been lying since 2026-07-31.** Self-chaining was switched
off that day for eating the week in two, but the disabling left the presence
beacon check and a 10-to-30-minute sleep running before an `exit 0` that sat one
line above the dispatch it suppressed. So every night run ended by sleeping for
nothing, the beacon it consulted could not affect anything, and CLAUDE.md's
capacity doctrine has said "runs chain themselves around the clock" for twelve
days while nine cron knocks were the only trigger. The step is four honest lines
now and the doctrine says what actually fires. FOR HIDDE, and it is the one item
here that needs him: turning the chain back on is your usage window, not a run's
call. Say the word and it goes back to the version from before c034207.

## 2026-08-12 - Portugal's register lands 21 trees, and a journalist finds the hole the pins never covered

**OPEN WORK, first thing for the next session.** Den Bosch's seven new trees
(dbo_005 to dbo_011) are verified and sitting in
`data/research/den-bosch-verified.json` with NO STORIES: the write pass was
stopped mid-flight. Everything else about them is done, including their
`how_to_recognise` lines, so this is one writing pass and nothing more. The
city file is claimed in `data/in-flight.json`; release it when they land.

**And a mail is owed.** A journalist at the Brabants Dagblad mailed Hidde on
2026-08-12. He was interested and put off by two things: how early-stage and
unvalidated the data looked, and that he walked to one of our Den Bosch trees
and could not tell which trunk was ours, because several similar ones stand
there. Hidde asked for a follow-up in the shape of "I looked deeper, here is
what it is based on, I had it searched further, here is what came out, what do
you think", and told me to wait until the work was actually live. Six of the
seven pieces are live; the seven stories are the last. Read
drafts/HIS_VOICE.md before drafting and run scripts/mailcheck.py on it.

**What his second objection produced, and it is the most useful feedback this
project has had.** `location_precision` answers WHERE and cannot answer WHICH,
and a pin exact to the metre is useless among five similar trunks. Every tree
can now carry `how_to_recognise`: one plain sentence naming what you look at
when you are standing there. It renders above the story and on the city card.
Den Bosch's four live trees have theirs; the Bastion Oranje maple now says it
is the thicker of the two at 427cm against the other's 317cm, with the
neighbour's register id so he can check it himself. "It stands alone, nothing
near it" is a good value and often the true one.

**Portugal, the batch the previous handover queued.** Lisbon 21 to 33, Porto 18
to 27, all from the ICNF register, which already held species, age, girth,
height and a surveyed coordinate, so the passes only had to confirm alive and
publicly reachable. Nine blocked on access: a guesthouse, a school, a private
office complex, an institutional garden, and two Passeio Alegre plantings that
fail the collectible-point test the way La Rambla did. The trap the handover
warned about was navigated rather than tripped: Porto has two tulipeiro
entries, only one is the school yard, and the other ships.

**Den Bosch's supply, worth knowing for any Dutch city.** The municipality
publishes 1,907 protected trees through an ArcGIS endpoint carrying species,
girth, age, height AND two fields registers almost never have: `EIGENAAR`
(owner, so hard rule 10 is answered by the data) and `VITALITEIT`. Filtered to
municipal ground, alive, girth over 250cm and not already published, it leaves
209 candidates, in `data/research/den-bosch-register-candidates.json`.

**Two lessons, both mine, both about trusting the wrong thing.**

A handover note is not the file. LOG.md said two batches were "ready to write,
no research needed", and I dispatched on that sentence. The Kyoto file's own
`verify_notes` deferred all five trees, one of them sits 10 km outside the park
it was said to be in, and that one is a duplicate of a tree we already publish,
17 m away, whose register glyphs are an OCR slip for the name our own story
uses. The writing pass caught it. Two of the five shipped, two are held on a
shared coordinate, one is blocked for good.

A delegating agent's child may still be running. A Den Bosch pass reported that
it had dispatched a subagent and stopped; I called it wasted and re-dispatched.
Both then delivered, roughly 340k tokens for overlapping work. The second was
better and is what shipped, but the waste was mine.

## 2026-08-11 - HANDOVER: what is queued for the next session

Written at the end of a long working session with Hidde, for whoever opens the
next one. He is out of tokens for today and asked that everything be left ready.
Read this before Step 0's ladder; the items below already sit on their proper
rungs.

**0. If Wolfgang Schürmann sends his ten Münster trees, that is the day's work.**
Baumkunde.de's register moderator was asked on 2026-08-11 for ten trees in his
own city, with the offer that we build the page from them and credit him. If
that list arrives it outranks everything below: a named list from a register
moderator is the cheapest new city this project has ever had, and Münster is
currently in no city file and not even in the 149-entry queue. Germany would go
from two cities to three. The floor is unchanged, four verified trees, and each
one still needs its own check, so the page carries what holds up rather than
all ten automatically. Credit him with `submitted_by` per Step 0b.

**1. Reader tips and replies (rung 1, outranks everything).**
Four replies are drafted and waiting for HIM to send; a run never sends them.
`drafts/reply-rock-creek.md` (his own wording, the calibration for all future
replies), `drafts/reply-baumkunde.md`, `drafts/reply-gruen-berlin.md`,
`drafts/woodland-trust-reply.md`.

Jon Pattee of Rock Creek Conservancy answered our tree question with "several
lovely ones in the park in front of the White House", which is Lafayette Square
in President's Park, and we publish nothing there. Recorded in
`data/leads/washington-dc.json` with what it needs and one trap (the Jackson
Magnolia stood on White House grounds and was removed in 2025, so it fails the
living-tree rule). It is NPS ground, so federal photographs are public domain,
which is the standing answer to Washington's photo gap: 13 of 14 DC trees have
none.

**2. Portugal, the biggest cheap win (rung 4, CITY_QUEUE.md).**
The ICNF register holds 555 trees under CC BY 4.0 and 478 are unused, 44 of
them in Lisboa and 21 in Porto, which are ranks 1 and 2 on the queue and the
two best-converting pages on the site. Candidates are already generated in
`data/research/portugal-register-candidates.json`, fully populated from the
register, so a pass does no discovery. Roughly 360k tokens for about 30 trees
at yesterday's measured rate. What the register cannot do and the pass must:
confirm each tree is alive and publicly reachable. Porto's 300-year tulip tree
on Rua Joao de Deus stands in a school yard and must not ship.

**3. Two batches ready to write, no research needed.**
`data/research/kyoto-gyoen-ready.json` (5 trees, kyo_015 to kyo_019) and the
remaining 13 ready Barcelona leads, both already unblocked by the 2026-08-10
ruling that only the hard rules and an unstatable location stop a tree. Run
`python3 scripts/leads.py` for the full picture: 299 leads are publishable now
and need only a story.

**4. The walk rule is NOT settled, and do not apply the obvious version.**
Hidde ruled: cap kilometres, no cap on tree count, minimum four trees. I
measured what that does before shipping it and it makes things worse. Setting
WALK_BUDGET_KM to 2.5 and WALK_MIN_TREES to 4 leaves Barcelona's 14-tree 3.5 km
chip standing, leaves Porto's 18 at 4.0 km and Lisbon's 11 at 4.5 km, and takes
Rome from 2 walks to 4, because the long options come from COMBINED_MAX_KM
(the "Both walks" chip) rather than from the budget, and a smaller budget
splits clusters into MORE walks. **The real knob is the combined chip.** Take
that to Hidde before changing any constant.

Done today and live: Barcelona to 46 trees, Porto to 18 with the first
reader-submitted tree (the Rainha das Virtudes), Boston's first photograph,
Kyoto's Gyoen cluster, CITY_QUEUE.md as the single city list, blueprint v1.11
(og:image and schema image on every page), the walk-name fix (Montjuic west and
east instead of Walk 2 and Walk 3), pin dimming that actually dims, and
`scripts/mailcheck.py`, which must be run on every draft mail before saving.

FOR HIDDE: four replies wait on you. Nothing else needs you.

## 2026-08-11 - Corpus pruning: two dead planning docs deleted, two stale BACKLOG.md entries removed

Session, at Hidde's request ("we have a huge number of MD files, let's prune and compact"). Not a research run; a corpus cleanup, all approved in session before touching anything.

**Deleted, both fully superseded and zero references found repo-wide:** `ancient_trees_businessplan.md` (2026-07-19, pre-pivot: wrong pricing model already recorded as removed in CLAUDE.md, wrong tech stack, "Rork" native-app plan that never happened) and `PRIORITIES.md` (a disposable 2026-08-05 snapshot generated by `scripts/priorities.py`, named its own city order, explicitly superseded today by `CITY_QUEUE.md`'s "if another document names a city order, it is stale and this one wins"). Also `ancient_trees_website_content.docx`, same era, same call. Note `CITY_QUEUE.md` itself, and the matching edits to CLAUDE.md Step 0 rung 4 and `nightly.yml`'s prompt, were already done by an earlier session today before this one started; this entry only covers what was still outstanding.

**BACKLOG.md:** removed two entries confirmed done by REVIEW.md's 2026-08-10 corpus audit. "Country pages, Contract G... WAITS ON HIDDE'S YES" — shipped, Contract G is live in SEO_GEO_BLUEPRINT.md v1.5. "Let runs read the visitor numbers" — shipped, `scripts/visitors.py` and `daily_digest.py` already read Cloudflare analytics.

**DISTRIBUTION.md and GO_TO_MARKET.md:** left in place (their reasoning and post-draft templates still have future value) but marked. DISTRIBUTION.md's hardcoded numbers (five cities, twelve of fifty trees) are 2026-07-21 snapshot and now badly wrong; added a one-line warning rather than rewriting Hidde's draft copy. GO_TO_MARKET.md's Japan-wave section is superseded by the 2026-07-30 ruling (DECISIONS.md); added a pointer so it reads as history, not live direction.

**TONE_OF_VOICE.md** (hard rule 7, asked first): header said "Version 1.0 (draft, awaiting Hidde's approval)" while the changelog and two inline notes already recorded three approved edits since then. Bumped to v1.4 and backfilled the two changelog entries that existed in the document but never made it into the changelog.

FOR HIDDE: nothing blocks. Two remaining growers with no archive mechanism, not touched this pass: DATA.md and REVIEW.md are both unbounded like LOG.md/CURATION.md used to be, but adding them to `archive_logs.py`'s FILES tuple needs a look at `daily_digest.py`'s read/write pattern first, flagged rather than done blind.

## 2026-08-10 - A full photo-candidate sweep while the chain worked Rome

New session. `python3 scripts/visitors.py`: 198 visits, 270 page views over the last 7 days, trending up (44 on both 2026-08-08 and 2026-08-10 so far, the two best days). Step 0: Supabase submissions checked directly (the CLAUDE.md placeholder URL isn't a real env var; the real endpoint is hardcoded in `scripts/daily_digest.py`), only the known test row (id 1), nothing new. Smoke test, Weekly analysis and Data digest workflows all green and recent. REVIEW.md's newest entry (second pass, ~10:45 UTC) confirmed this morning's BLOCKER (`ageToken()`) and WARN (nightly permissions) both already fixed on disk; its one open item is a WARN marked FOR HIDDE about the outreach mailer's live-sending contradicting hard rule 4 as currently written, a judgment call for him, not a run's to resolve.

**The tourist-rollout ladder (item 1/2 of the dispatch note) was already fully worked by prior sessions today**: every phase-1 city has a walk at or above the 6-8 aim except Berlin and New York, both confirmed hard floors after direct register checks, and London stays gated. `data/in-flight.json` held a live `verify` claim on Rome (by `night-run`, 08:26 UTC, well inside its 4-hour window), and a scheduled "City research" GitHub Actions run started independently at 10:47 UTC and was still active hours later, almost certainly the same Rome pass reporting back. Left Rome alone rather than risk the exact collision the claim file exists to prevent.

**So this session's contribution is item 3, the free half of photo work a run can actually do here.** Ran `scripts/photo_hunt.py --recheck` with no city filter across all 589 photo-less trees site-wide (the prior full sweep was from 2026-08-09, before Berlin's Lietzensee trio, New York's Reservoir cluster and today's other growth existed). Zero AI tokens, pure Commons API retrieval. Result: 247 of 589 now carry at least one open-licence candidate, up from 233. Real gains for trees that had nothing before, including all of London's Square Mile cluster (10-14 fresh candidates each: `lon_011` through `lon_023`), New York's four Reservoir-cluster trees, and Berlin's `ber_016-018`. None of it judged, since this runner's egress proxy still can't reach `upload.wikimedia.org`; that stays a session's job. Committed and pushed (31061e7), smoke test green on the new commit.

FOR HIDDE: nothing new blocks. Same two open items as this morning: the outreach-mailer/hard-rule-4 contradiction REVIEW.md flagged, and Rome's dispatched verify pass, which may still be running when you read this.

## 2026-08-10 - Rollout walks confirmed complete, a free photo sweep, and four country pages opened

New session. `python3 scripts/visitors.py`: 158 visits, 228 page views over the last 7 days, trending up (44 on 2026-08-08, still the best day). Step 0: Supabase submissions checked (SUPABASE_SERVICE_KEY present), only the known test row, nothing new to process. REVIEW.md's newest entry (2026-08-10) held one BLOCKER (`ageToken()` picking a planting year instead of an age for 75 trees/30 cities, e.g. Boston's Shaw elms reading "1772 Year Old") and one WARN (the night run's over-wide Bash permissions); both were already fixed on disk in the prior commit (8b6fa3f), confirmed by reading the code and by a clean working tree. Smoke test, Weekly analysis, Data digest and Fresh-eyes review workflows all green and recent via `gh run list`.

**Checked the dispatch note's four-item priority list against current state and found items 1-2 already done.** Computed `plan_walks()` directly for all ten rollout cities (Barcelona, Rome, Paris, Berlin, Amsterdam, New York, Lisbon, Vienna, Edinburgh, Dublin): every one already has a lead walk at or above the 6-8 aim except Berlin and New York (5 each, both confirmed hard floors in yesterday's sessions after direct register checks) and London (5, gated, untouched). Nothing to grow.

**Rome stayed untouched on purpose.** `data/in-flight.json` held a `verify` claim on Rome from 08:26 UTC, 16-26 minutes old when checked, well inside its 4-hour window; today's first LOG entry shows a background pass was dispatched for it and never reported back before this session started (the Nara pattern: a background agent dies with the session that launched it). Rather than risk the exact collision the claim mechanism exists to prevent, left it for whichever run holds it or picks it up after expiry.

**Photo sweep (item 3): ran `photo_hunt.py --recheck` across all ten rollout cities plus New York (caught a real bug: the city's JSON field is "New York", not "new-york", so my first pass silently swept zero NYC trees; re-ran with the correct name).** Free API sweep, no AI tokens. Found genuine new candidates for 20+ trees that had none before, including all four of New York's newest Reservoir-cluster trees (nyc_017-020) and every new Berlin/Dublin/Edinburgh/Lisbon/Vienna tree from yesterday's growth. Confirmed via a full-site `photo_hunt.py` sweep with no city filter that every photo-less tree site-wide has now been checked at least once (0 unchecked). Ran `tree_index.py` (19,347 trees tracked, unchanged). Committed and pushed (ce901e5).

**Item 4 (season data) skipped deliberately**, per the standing instruction not to sink a research window into it; nothing was being newly written that would have set a `best_time` for free.

**PRODUCT_TODO.md's queue was checked and found exhausted**: item 1 (accounts) explicitly off-limits to runs, item 2c session-reserved, items 2/2b/5/6 DONE, item 3's copy audit superseded by `qa.py`'s standing gate, item 4's collections slate fully shipped or honestly blocked pending new cities. Register-layer scouting (OPEN_DATA_SURVEY.md) is similarly mature: every register mentioned as "usable, licence proven" already has a matching file in `data/registers/`.

**Found and closed a real gap instead: four countries had crossed Contract G's 3-published-city threshold with no hand-written intro, so no country page.** Italy (14 cities, 159 trees), the United Kingdom (8, 68), Poland (3, 13) and France (3, 44). REVIEW.md's own 2026-08-08 NOTE had flagged CLAUDE.md's "waiting" list as stale on exactly this point. Wrote all four intros by hand, grounded in this site's own already-verified tree stories (Padua's 1545 botanical garden and its Goethe-essayed palm for Italy, London's Totteridge Yew and churchyard survival for the UK, Krakow's Henryk Oak named for its human protector plus Warsaw's Dab Mieszko I for Poland, the 1601-planted Robinier of Square Rene-Viviani for France), 100-150 words, no invented facts, no em dashes. Built and verified in the rendered output: all four pages construct with the right city count/meta description/H1, the country-breadcrumb upgrade fires correctly (London's crumb now links `/united-kingdom` instead of rendering as plain text), `qa.py` passes clean. Committed and pushed (be54481).

FOR HIDDE: nothing blocks. Rome's dispatched verify pass from this morning never reported back before this session started; if nobody's actively working it by the time you read this, it's a free pickup for the next run. The four new country pages are live and unlinked from nothing else that needed changing (the breadcrumb upgrade already existed and just needed the intro files to fire).

## 2026-08-10 - Housekeeping: logging Berlin's Charlottenburg/Lietzensee trees that a broken night run left unrecorded, plus Rome's Celimontana cluster dispatched

`python3 scripts/visitors.py`: 157 visits, 227 page views over the last 7 days, best day 2026-08-08 at 44. Step 0: Supabase submissions checked, only the known test row (id 1), nothing new. Smoke test and Build/deploy both green on HEAD. Fresh-eyes review's last scheduled run (2026-08-09 08:23 UTC) failed in 35 seconds (a checkout-stage infra hiccup, not a code problem); tried to redispatch it via `gh workflow run` but this token lacks `workflow` dispatch permission (HTTP 403), so it waits for tomorrow's schedule. REVIEW.md's newest entry (2026-08-08) holds no live BLOCKER, both flagged issues confirmed already fixed in a prior session.

**Found and closed a gap: ber_016-018 (The Lietzensee Plane, The Lietzensee Wingnut, The Karpfenteich Elm) were live in data/cities/berlin.json, verified and sourced, but no LOG.md or CURATION.md entry ever recorded them.** The trail: a night run claimed Berlin's Charlottenburg/Lietzensee cluster yesterday and its verified findings landed in data/research/berlin-verified.json, but the entry documenting it was written "still running" and never followed up, right around when the Astro migration's permission-list bug (see Hidde's own fix, commit "Invert the night run's permission list...") made every subsequent run unable to build or commit. The data itself was already merged and live; only the paper trail was missing. Confirmed: schema valid, sources check out (Berlin's Naturdenkmal register cross-checked against monumentaltrees.com GPS pins, 3-9m apart, for both Lietzensee trees; the elm is flagged since no source gives it an age). Berlin: 15 to 18 trees. Honest gap, checked with `plan_walks()`: these four trees (ber_004 the Swamp Cypress, ber_016, ber_017, ber_018) do NOT form a computed walk. Lietzensee's pair (ber_016/017, 170m apart) and Charlottenburg palace park's pair (ber_004/018, ~66m apart) sit 1.9km apart, just past the walk-clustering radius on both ends, so each pair alone is one tree short of the 3-tree floor. Two weak register-only leads sit within reach (a Medlar and a Cherry Plum in the same palace garden, both "Eigenart, landeskundliche Gründe" designations, no age, no second source after two prior passes each) but were judged not to clear the remarkability bar on a third look rather than padded in to force a walk. Left as an honest gap in data/leads/berlin.json rather than shipped.

Ran `scripts/photo_hunt.py --recheck --city berlin`: filled the queue with candidates for all 7 Berlin trees still missing a photo, including the three new ones. Not judged (this runner's egress proxy can't reach upload.wikimedia.org; that's Hidde's-session work). Ran `scripts/tree_index.py` to refresh the database (19,347 trees now tracked, 893 highlighted).

**Dispatched a verify pass on Rome**, claimed via passcheck (data/in-flight.json), targeting a genuinely promising register-confirmed lead: four unpublished MASAF entries (a second Cedar of Lebanon, a silk floss tree, a Quercus hybrid, a pomegranate) all within 150-450m of the already-published Villa Celimontana cedar and pine (rom_008/009), plus a second hackberry near the Parco degli Scipioni hackberry (rom_024). This is real growth for an existing cluster rather than a scattered single, matching the current dispatch note's priority. Result not yet known; will merge, write stories, build and commit once it reports back.

## 2026-08-10 - El experimento español: Malaga compleet onder /es/, in de opzet die schaalt

Hidde's besluit, boven mijn eerdere bezwaar dat hij expliciet terzijde schoof ("staar je niet zo blind op die wachtrij"): een paar Spaanse pagina's als markttest, gebouwd zodat het blijft werken als er meer talen komen. De wachtrij-zorg is genoteerd en losgelaten; de positieverbetering van 17 naar 10 in negen dagen steunt zijn lezing dat die zichzelf oplost.

De test is Malaga, volledig: stadspagina, vraagpagina op /es/malaga/arbol-mas-antiguo (de frase die een Spaanstalige echt zoekt, geen Engels padsegment), en tien boompagina's. Malaga omdat het de enige stad is met gemeten Spaanse vraag: "arboles historicos de malaga", 20 vertoningen op positie 74, nul kliks op onze Engelse pagina. Dat is ook de meetlat, vastgelegd in blueprint v1.10 (Contract J, door Hidde in sessie goedgekeurd): beweegt /es/malaga binnen vier weken na indexering op die zoekopdracht, dan werkt het en openen we meer; zo niet, dan weten we dat ook.

De opzet, want die was de helft van zijn vraag. Taalsubmap plus wederzijdse hreflang met x-default naar het Engels, de industriestandaard die naar meer talen schaalt zonder verbouwing. De vertaling is een OVERLAY (data/i18n/es/malaga.json) met alleen tekst: elke coordinaat, foto, licentie en wandeling blijft in het ene canonieke stadsbestand, dus een pin die in het Engels wordt gecorrigeerd is overal gecorrigeerd. De build weigert als de Engelse stad groeit voorbij zijn vertaling, zodat een overlay nooit stil veroudert. Het Spaans is met de hand geschreven op dezelfde maten als het Engels (intro 91 woorden, verhalen 181 tot 229, geen em dashes); het accent-incident van gisteren is de reden dat machinaal patchen in het contract verboden staat.

Eerlijk benoemd als bewuste grens van de test: de site-chrome (navigatie, footer), de kaartpopups en het seizoensblok blijven Engels. Verdient de test een tweede taal, dan worden die contractwerk in plaats van stille schuld.

Live geverifieerd op desktop en 375px: kaart bouwt, pins staan, wandelbalk in het Spaans, hreflang in beide richtingen identiek, /es/malaga in de sitemap (12 URL's), taalwissel zichtbaar op beide kanten. Build en smoke in een keer groen.

