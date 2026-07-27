# Product work for autonomous runs

The queue a run may draw from when every content rung in CLAUDE.md Step 0 is satisfied. Rules of this lane, and they are strict because a CI run cannot see the page it changes:

- Only reversible work. Every item must leave `python3 scripts/build_site.py` passing with all contracts validated.
- Every item carries a **done when** that a blind run can verify with build output, grep, or a script, not with eyes.
- No visual-taste work here: no logo, icon art, layout aesthetics or colour changes. Those need a session with eyes (Hidde's, or a browser-equipped session). No hard-list items, ever: no accounts, payments, dependencies, brand, blueprint or tone-of-voice edits.
- One item per pass, finished and committed before the next. Log in LOG.md. When judgement wobbles, the mandate's three questions decide.

## Queue, in order

### 1. The account track, opened by Hidde 2026-07-26 (supersedes the earlier supersession)
Collect returns to the web as the app's rehearsal: login UX (magic link, Slack-style states) is being built in-session behind an AUTH_ENABLED flag, unlinked and noindexed until Hidde's Supabase project and privacy page exist. Runs: do not wire any backend, do not link the page, do not touch the flag. The game design (points, badges, sets) is being settled with Hidde in conversation.

### 2. DONE 2026-07-26, built in session: the season radar page
A page at `/in-season` (linked from the Season act on the homepage once it exists): every tree whose `best_time.months` contains the current build month, grouped by city, each with its label phrase and a link. Static is fine: the site rebuilds many times a day, so "this month" stays true. Month with nothing in season shows the nearest upcoming moments instead of an empty page (empty states teach, PRINCIPLES.md).
Shipped as /in-season: current month plus the two coming months, grouped by city, linked from the homepage Season act, contracts green. Runs keep it honest simply by rebuilding the site. Skip to item 3.

### 3. Copy audit against the value proposition and the durable-claims rule
Walk every template string in `scripts/build_site.py` against CLAUDE.md's value proposition and the rule that copy may only promise what the paywall will survive. Remove drifted or filler copy; tighten to the tone of voice.
**Done when:** grep finds no "free forever", "always free", "no accounts" (as a promise), "never pay" anywhere in generated pages; spot-grep of banned tone words ("hidden gem", "must-see", "breathtaking", "nestled", em dashes) stays zero across `site/dist`.

### 4. The collections programme, promoted by Hidde 2026-07-26
Collections are the highest-leverage SEO pages we have (broad queries, zero new research, they recombine the 328 verified trees) and each one is designed as a future badge set: finite, completable, 5 to 12 trees across cities. Search Console already shows us ranking accidentally for "ancient oaks" (position 26) and "old trees" with no page aimed at either.

Draft up to two per pass from this slate, best query-fit first: Ancient oaks of Europe; Trees older than 1000 years; The ginkgos worth a November trip; Europe's most remarkable yews; Trees that outlived their city; The great planes of Europe; Wisteria and blossom worth a spring trip; The oldest tree in every country we map. Ground every entry in existing verified data only. One future slate item, recorded 2026-07-26 when Hidde asked "why not the US": Live Oaks of the American South, unlockable once New Orleans (queued) and ideally Savannah or Charleston are built. The US already consumes our European pages (third country in week-one Search Console without one promoted US city); full US city coverage stays behind Europe because ancient is thin there, its cities are car cities, and its SERPs are the hardest, but the South's live oaks are the honest exception.

Since blueprint v1.3 (2026-07-27) collections publish without owner approval, under the research standard: every entry script-checked against the tree data, superlatives per hard rule 8, voice per TONE_OF_VOICE.md. Announce each new collection in LOG.md like any other work.
**Done when (per pass):** up to two new collection JSONs validate, build and are linked; a check script confirms every listed tree exists with the claimed property (age, species); the LOG.md entry exists.

### 5. Seasonality completion pass
Every qualifying tree across all 33 cities gets an honest `best_time` (species with a real peak only; evergreens get none, per Step 3's rules).
**Done when:** a count script shows every ginkgo, wisteria, wingnut, horse chestnut, magnolia and deciduous-showpiece species carries `best_time`, and no evergreen (yew, holm oak, cypress, cedar, pine, camphor, olive) does.

### 6. DONE 2026-07-27, built across two passes: internal linking for collections and species pages
Question pages should link a relevant collection where one exists; species pages should be linked from every tree of that species (already contract-checked) and from city pages where 3+ trees share a species.
Species linking shipped first (5 cities). The collection-linking half turned up a real bug on the way: both the question page and the city page were picking the same first collection unconditionally regardless of whether the city actually had a tree in it, with hardcoded copy ("the yew, the oaks", "Several of these trees") that was false for most cities. Fixed both to filter by actual membership and state the real count. Verified on built output: 23 question pages and every city with a collection tree now link a genuinely relevant one, the rest fall back to a generic `/collections` link. Nothing left in this item.
