# Product work for autonomous runs

The queue a run may draw from when every content rung in CLAUDE.md Step 0 is satisfied. Rules of this lane, and they are strict because a CI run cannot see the page it changes:

- Only reversible work. Every item must leave `python3 scripts/build_site.py` passing with all contracts validated.
- Every item carries a **done when** that a blind run can verify with build output, grep, or a script, not with eyes.
- No visual-taste work here: no logo, icon art, layout aesthetics or colour changes. Those need a session with eyes (Hidde's, or a browser-equipped session). No hard-list items, ever: no accounts, payments, dependencies, brand, blueprint or tone-of-voice edits.
- One item per pass, finished and committed before the next. Log in LOG.md. When judgement wobbles, the mandate's three questions decide.

## Queue, in order

### 1. The shareable "my trees" page
A page at `/my-trees` that renders the visitor's passport from LocalStorage: which trees, grouped by city, city and total counts, and the existing `#trees=` link both as "back up your collection" and as "share it". Sharing is the one growth loop that needs nobody to post, and the page is the future reason an account is worth having. Empty state must invite ("You have not stood anywhere yet. Find a tree near you.") rather than look broken.
**Done when:** the page builds and validates; grep shows it reads `ancienttrees_seen` and emits the `#trees=` link; every city page's passport box links to it; empty-state copy present in the built HTML.

### 2. Copy audit against the value proposition and the durable-claims rule
Walk every template string in `scripts/build_site.py` against CLAUDE.md's value proposition and the rule that copy may only promise what the paywall will survive. Remove drifted or filler copy; tighten to the tone of voice.
**Done when:** grep finds no "free forever", "always free", "no accounts" (as a promise), "never pay" anywhere in generated pages; spot-grep of banned tone words ("hidden gem", "must-see", "breathtaking", "nestled", em dashes) stays zero across `site/dist`.

### 3. Two new collection drafts from existing data
Per BACKLOG.md: recombine the 328 researched trees into two new collections (candidates: Europe's oldest oaks; ginkgos worth a November trip). Contract D applies: they ship as `needs_curation` drafts and are announced in LOG.md under FOR HIDDE for publish approval.
**Done when:** two new JSON files in `data/collections/` validate and build; LOG.md carries the FOR HIDDE line; nothing links to them publicly until approved.

### 4. Seasonality completion pass
Every qualifying tree across all 33 cities gets an honest `best_time` (species with a real peak only; evergreens get none, per Step 3's rules).
**Done when:** a count script shows every ginkgo, wisteria, wingnut, horse chestnut, magnolia and deciduous-showpiece species carries `best_time`, and no evergreen (yew, holm oak, cypress, cedar, pine, camphor, olive) does.

### 5. Internal linking pass for the collections and species pages
Question pages should link a relevant collection where one exists; species pages should be linked from every tree of that species (already contract-checked) and from city pages where 3+ trees share a species.
**Done when:** link-count contracts still validate and a grep confirms collection links on at least the city pages whose trees appear in a collection.
