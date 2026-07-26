# Product work for autonomous runs

The queue a run may draw from when every content rung in CLAUDE.md Step 0 is satisfied. Rules of this lane, and they are strict because a CI run cannot see the page it changes:

- Only reversible work. Every item must leave `python3 scripts/build_site.py` passing with all contracts validated.
- Every item carries a **done when** that a blind run can verify with build output, grep, or a script, not with eyes.
- No visual-taste work here: no logo, icon art, layout aesthetics or colour changes. Those need a session with eyes (Hidde's, or a browser-equipped session). No hard-list items, ever: no accounts, payments, dependencies, brand, blueprint or tone-of-voice edits.
- One item per pass, finished and committed before the next. Log in LOG.md. When judgement wobbles, the mandate's three questions decide.

## Queue, in order

### 1. SUPERSEDED, do not build: the shareable my-trees page
Hidde is moving check-in and collecting toward the app (web becomes discovery plus the sales floor). Until that decision is recorded in CLAUDE.md, build nothing passport-related and remove nothing either. Skip to item 2.

### 2. DONE 2026-07-26, built in session: the season radar page
A page at `/in-season` (linked from the Season act on the homepage once it exists): every tree whose `best_time.months` contains the current build month, grouped by city, each with its label phrase and a link. Static is fine: the site rebuilds many times a day, so "this month" stays true. Month with nothing in season shows the nearest upcoming moments instead of an empty page (empty states teach, PRINCIPLES.md).
Shipped as /in-season: current month plus the two coming months, grouped by city, linked from the homepage Season act, contracts green. Runs keep it honest simply by rebuilding the site. Skip to item 3.

### 3. Copy audit against the value proposition and the durable-claims rule
Walk every template string in `scripts/build_site.py` against CLAUDE.md's value proposition and the rule that copy may only promise what the paywall will survive. Remove drifted or filler copy; tighten to the tone of voice.
**Done when:** grep finds no "free forever", "always free", "no accounts" (as a promise), "never pay" anywhere in generated pages; spot-grep of banned tone words ("hidden gem", "must-see", "breathtaking", "nestled", em dashes) stays zero across `site/dist`.

### 4. The collections programme, promoted by Hidde 2026-07-26
Collections are the highest-leverage SEO pages we have (broad queries, zero new research, they recombine the 328 verified trees) and each one is designed as a future badge set: finite, completable, 5 to 12 trees across cities. Search Console already shows us ranking accidentally for "ancient oaks" (position 26) and "old trees" with no page aimed at either.

Draft up to two per pass from this slate, best query-fit first: Ancient oaks of Europe; Trees older than 1000 years; The ginkgos worth a November trip; Europe's most remarkable yews; Trees that outlived their city; The great planes of Europe; Wisteria and blossom worth a spring trip; The oldest tree in every country we map. Ground every entry in existing verified data only. One future slate item, recorded 2026-07-26 when Hidde asked "why not the US": Live Oaks of the American South, unlockable once New Orleans (queued) and ideally Savannah or Charleston are built. The US already consumes our European pages (third country in week-one Search Console without one promoted US city); full US city coverage stays behind Europe because ancient is thin there, its cities are car cities, and its SERPs are the hardest, but the South's live oaks are the honest exception.

Contract D holds: drafts ship as `needs_curation`, announced under FOR HIDDE in LOG.md, nothing linked publicly until Hidde approves. His approval is deliberately cheap: read the draft, say yes or no.
**Done when (per pass):** up to two new collection JSONs validate and build unlinked; the FOR HIDDE line exists; every listed tree exists in the data with the claimed property (age, species) checkable by script.

### 5. Seasonality completion pass
Every qualifying tree across all 33 cities gets an honest `best_time` (species with a real peak only; evergreens get none, per Step 3's rules).
**Done when:** a count script shows every ginkgo, wisteria, wingnut, horse chestnut, magnolia and deciduous-showpiece species carries `best_time`, and no evergreen (yew, holm oak, cypress, cedar, pine, camphor, olive) does.

### 6. Internal linking pass for the collections and species pages
Question pages should link a relevant collection where one exists; species pages should be linked from every tree of that species (already contract-checked) and from city pages where 3+ trees share a species.
**Done when:** link-count contracts still validate and a grep confirms collection links on at least the city pages whose trees appear in a collection.
