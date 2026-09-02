# ARCHITECTURE.md — Astro migration plan

Written 2026-08-08, proposed in session. Records the direction agreed on
(replace `scripts/build_site.py`'s HTML generation with Astro) and how to get
there without breaking anything currently live: 90 cities, 777 trees, indexed
URLs, Search Console history. The npm dependency list this implies still
needs Hidde's explicit yes per hard rule 5 before anything is installed; see
Open decisions.

## The decision, and why

- **Astro, not Next.js or a Vite SPA.** The site is ~95% static content
  (tree/city/species/country/collection pages) with a handful of interactive
  pockets (map, sign-in, search). Astro's island model ships zero JS by
  default and hydrates only the specific widgets that need it, which matches
  that ratio better than a React-everywhere framework. It also keeps output
  mode static (`output: 'static'`), so the GitHub Pages deploy barely changes.
- **Python does not move.** The entire research/verification/curation
  pipeline (`passcheck.py`, the verify/write-stories agents, `photo_hunt.py`,
  the register importers, all of it) keeps writing to `data/*.json` exactly
  as it does today. Astro reads that same data at build time. This migration
  touches the rendering layer only.
- **Supabase is the live backend**, already wired for auth
  (`build_account_page`, `scripts/build_site.py:5487`) and the target for
  UGC (pending submissions visible immediately, verified ones promoted into
  `data/*.json` by the existing Python review loop). Astro islands talk to
  it directly client-side, same pattern the current vanilla-JS login script
  already uses.
- **GitHub Pages stays the host.** No server to run, no new cost, no new
  liability under hard rule 5 beyond the npm toolchain itself.

## What does not change

- `data/` schema, `data/city-list.json`, `data/city-aliases.json`,
  `RENAMED_CITY_SLUGS`/`RENAMED_TREE_SLUGS` — all untouched. Astro is a new
  reader of the same files, not a new schema.
- `scripts/qa.py` and `scripts/smoke_test.py` run against rendered HTML in
  `site/dist/` and know nothing about how it got there. They keep working
  unmodified against Astro's output, and stay the deploy gate. This is the
  single biggest reason the migration is low-risk: the two layers that
  actually catch regressions (dead links, banned words, orphan pages, the
  em-dash rule, the executed-DOM smoke test) don't care which generator ran.
- CLAUDE.md's research workflow, the assembly line, the model tiering, the
  hard rules. None of this is a product or process change.
- URL structure. Every contract's URL pattern (Contract A-H) stays
  byte-identical. This is non-negotiable per hard rule 3 (nothing
  irreversible in public) and SEO_GEO_BLUEPRINT.md's global rule ("a URL
  never changes once published").
- The one localStorage key left, `ancienttrees_session`. It is a public
  contract with every visitor's browser and renaming it signs everybody out.
  `ancienttrees_seen` (collected trees) and `at_saved_v1` (saved trees) were
  the other two and are GONE as of 2026-09-02, on Hidde's instruction that
  nothing be stored on the device: the collection lives in the account, in the
  `visited` and `saves` tables, and the browser holds only the token that says
  whose account it is. Nothing renamed a key, which is the failure
  PRINCIPLES.md #12 is about; the data moved somewhere that survives a cleared
  browser, a second device and Safari's seven-day wipe, which is what that
  principle actually wanted.

## What changes

`scripts/build_site.py`'s HTML-generation half is replaced by an Astro
project. Concretely, everything from `render_page()` down (the f-string
templates, `PAGE_SHELL`, the per-contract `build_*_page()` functions) becomes
`.astro` components and pages. Everything above that (reading `data/cities/*.json`,
computing derived fields, `city-aliases.json` lookups) becomes Astro content
loading, run at build time in JS/TS instead of Python.

## Target shape

**A routing pitfall to build in from the start, not discover late.** Astro's
default `build.format` is `directory`: a page component named `about.astro`
emits `about/index.html`, and GitHub Pages then serves `/about` with a 301 to
`/about/`. Today's site is file-format throughout: `london.html` is the city
page, and `london/index.html` is a hand-written *redirect stub* sending the
trailing-slash form back to the canonical (`build_redirects`,
`build_site.py:5310`). Left on Astro's default, every city and country page
would flip its own canonical to a trailing slash and collide with that stub's
own path. Two settings fix this before a single page is ported:
`build: { format: 'file' }` in `astro.config.mjs`, and Contract C/G routed as
single-segment dynamic files (`src/pages/[city].astro`, not
`[city]/index.astro`) so they emit `london.html` directly. Nested contracts
(tree, question pages) already sit one level under a city folder in both the
current and target layout, so `format: 'file'` alone makes
`src/pages/[city]/[tree].astro` emit `{city}/{tree}.html`, matching today.

```
/data/                    unchanged — Python's output, Astro's input
/scripts/                 unchanged — the research pipeline
/site/                    NEW — the Astro project
  astro.config.mjs        output: 'static', build: { format: 'file' },
                           site: BASE_URL, redirects: {...} (see Redirects)
  src/
    content/
      config.ts           Zod schemas mirroring the tree/city/species/
                           country/collection JSON shapes — this is where
                           Contract field requirements (title length, gate
                           conditions) become typed, checked before a page
                           can even render, not after
    layouts/
      Base.astro           the PAGE_SHELL equivalent: head, schema.org
                           JSON-LD, header, footer, login link
    components/
      TreeMap.astro         MapLibre wrapper, client:visible
      SearchBox.astro       the live-suggestion convention, client:idle
      AccountWidget.astro   the Supabase magic-link flow, client:load
      PhotoCredit.astro, FactBlock.astro, Breadcrumbs.astro, ...
    pages/
      index.astro                          → homepage
      [city]/index.astro                   → Contract C, getStaticPaths from city JSON
      [city]/oldest-tree.astro             → Contract B
      [city]/[tree].astro                  → Contract A
      collections/[slug].astro             → Contract D
      parks/index.astro, parks/[slug].astro → Contract H
      species/index.astro, species/[slug].astro → Contract F
      [country].astro                      → Contract G (root-level, collision-
                                              checked against city slugs same
                                              as today)
      account.astro                        → noindexed while AUTH_ENABLED
      explore.astro, contribute.astro, privacy.astro, about.astro
    lib/
      images.ts             thumb_url()/img_srcset() ported straight across;
                             qa.py's Wikimedia-original and iNaturalist-original
                             checks depend on this helper being used everywhere,
                             same as today
  dist/                    build output — same path GH Pages already deploys
```

### Redirects

Verified against Astro's own docs (not assumed): for `output: 'static'`,
Astro's `redirects` config *does* generate the same kind of thing
`build_redirects()` hand-rolls today — a static HTML page with
`<meta http-equiv="refresh">` plus `<meta name="robots" content="noindex">`
— controlled by `build.redirects` (defaults to `true` in static mode). So
this doesn't need a hand-rolled `redirects.ts`: compute the full redirect map
at config-load time (`astro.config.mjs` is a plain Node module, so it can
read `data/city-aliases.json`, `RENAMED_CITY_SLUGS`, `RENAMED_TREE_SLUGS`,
plus the `/cities/[slug]/`, `/{slug}/` trailing-slash, `/collections/`,
`/species/` legacy paths) and pass it into `defineConfig({ redirects })`
directly. One thing to check in the prototype step, since it affects
parity: whether Astro's generated stub can carry a custom per-page `<title>`
the way `redirect_stub()` does today ("Moved: Ancient Trees in London"); if
not, decide whether that matters (the page is noindexed and redirects
immediately, so it's low-stakes either way) or fall back to hand-rolled
stubs for that one detail.

## Page contract mapping (SEO_GEO_BLUEPRINT.md Layer 2)

| Contract | Current function | Astro route | Notes |
|---|---|---|---|
| A — Tree | `build_tree_page` | `src/pages/[city]/[tree].astro` | `getStaticPaths()` flattens every city's `trees[]`; emits `{city}/{tree}.html` under `format:'file'` |
| B — Question | `build_question_page` | `src/pages/[city]/oldest-tree.astro` | per-city static path, emits `{city}/oldest-tree.html` |
| C — City | `build_city_page` | `src/pages/[city].astro` | single-segment dynamic file, NOT `[city]/index.astro` — emits `{city}.html` directly, so it can't collide with the `{city}/index.html` trailing-slash redirect stub |
| D — Collection | `build_collection_page` | `src/pages/collections/[slug].astro` | reads `data/collections/*.json` as a content collection |
| E — About | (parked, P5) | n/a | stays parked |
| F — Species | `build_species_page` | `src/pages/species/[slug].astro` | publish gate (3+ trees, hand-written intro) enforced in `getStaticPaths` filter, same logic, moved language |
| G — Country | `build_country_page` | `src/pages/[country].astro` | same single-segment-file pattern as Contract C; root-level slug collision check becomes a build-time assertion over all path params |
| H — Park | `build_park_page` | `src/pages/parks/[slug].astro` | 5+ trees AND intro gate, same as F |

Redirects, sitemap, `robots.txt`, RSS-equivalent (none currently) map to
small dedicated scripts/integrations rather than page components.

## Contract validation: where it goes

Today, `render_page()` pushes into a module-level `ERRORS` list
(`build_site.py:2230-2233`) and the build fails if it's non-empty at the end
(`validate_internal_links`, `build_site.py:5363`). Two things replace this:

1. **Shape/gate validation → Zod schemas in `content/config.ts`.** A tree
   entry missing `location.latitude` or a species page under 3 renderable
   trees fails at the content-loading step, before any template runs. This
   is strictly earlier and stricter than today's runtime check.
2. **Cross-page validation (title length, link minima, orphan pages, em
   dashes, banned words, business-rule-phrase leakage) → unchanged, stays in
   `qa.py`.** It already runs post-build against `site/dist/`. Nothing to
   port; point `DIST` at the same path (no change needed, Astro's default
   `outDir` is `dist/` under the project root, so keep the Astro project
   rooted at `site/` and `qa.py`'s existing `site/dist` path is already
   correct).

## Interactive islands (the JS currently inline in `PAGE_SHELL`/`build_*`)

| Feature | Current location | Astro island | Hydration |
|---|---|---|---|
| Tree/city map | inline `<script>` around `maplibregl.Map` (`build_site.py:1207`, `:1570`) | `TreeMap.astro` | `client:visible` — map is below the fold on most pages |
| Magic-link sign-in | `build_account_page` (`build_site.py:5487`) | `AccountWidget.astro` | `client:load` on `/account` only |
| Search-with-suggestions | homepage/explore search | `SearchBox.astro` | `client:idle` |
| Check-in / passport (localStorage) | inline script per tree page | `CheckInButton.astro` | `client:visible` |
| Pending-submission pins (new, UGC) | n/a yet | `PendingPins.astro`, queries Supabase directly | `client:visible`, only on city/explore pages |

The smoke test's assertions (map produces a canvas, check-in button carries
`aria-pressed`, no script source leaks as text) transfer unchanged, since
they test the executed DOM, not the generator.

## Rollout: page-type by page-type, not a big-bang rewrite

Given 90 live cities and indexed URLs, cut over one contract at a time,
verified against the existing site before deleting the Python renderer for
that page type:

1. **Scaffold the Astro project alongside `build_site.py`**, both writing to
   *different* output directories at first (e.g. Astro to
   `site/dist-astro/`). Nothing deploys from it yet. `qa.py` and
   `smoke_test.py` both hardcode `DIST = .../site/dist` (`qa.py:24`); give
   each an optional `--dist` argument (or a `DIST` env override), a small
   additive change, so they can run against `dist-astro` during the parallel
   period without touching their behavior against the real `dist`.
2. **Port the shell + one low-traffic contract first** (Park pages, Contract
   H — fewest pages, gate logic is simple, good template for the others).
   Run `qa.py` and `smoke_test.py` against the Astro output directly to
   prove the harness works unmodified.
3. **Port Tree, City, Question, Species, Collection, Country pages**, each
   diffed page-for-page against the current Python output before being
   trusted (same title, same schema.org graph, same link count, same
   rendered text minus incidental whitespace). At each step, also confirm no
   URL was dropped, renamed or given a new trailing-slash form:
   `diff <(cd site/dist && find . -type f | sort) <(cd site/dist-astro && find . -type f | sort)`
   should come back empty once a contract's pages are fully ported on both
   sides. This is the check that actually protects the indexed URLs, since
   title/schema parity alone wouldn't have caught the directory-format
   pitfall above.
4. **Port redirects last**, since correctness there is only checkable by
   walking every entry in `RENAMED_CITY_SLUGS`/`RENAMED_TREE_SLUGS` and
   confirming the stub still resolves.
5. **Cut every workflow that reads `site/dist` as the real build over**,
   in one commit, once every contract passes `qa.py` + `smoke_test.py`
   against Astro's own output. That's three workflows, not one:
   `deploy.yml` (the artifact that ships), `smoke.yml` (must exercise what
   actually deploys, not a retired renderer) and `review.yml` (the
   fresh-eyes reviewer inspects "the BUILT product in site/dist", which
   must be the real one). `nightly.yml` runs `build_site.py` too, but only
   as the research agent's own self-check that a data edit still builds;
   it produces no artifact and needs no change here. One commit keeps a
   single clear rollback point and avoids a half-cutover where smoke tests
   one generator's output while deploy ships the other's.
6. **Delete the Python rendering code, done 2026-08-09.** `scripts/build_site.py`
   is gone. Its claim above (nothing in the research pipeline calls into it)
   turned out to be wrong for one case, found by grepping every script for
   `import build_site` before deleting rather than trusting the sentence:
   `scripts/route_walks.py` used `load_cities()` and `plan_walks()` (and
   their dependencies) to work out which walks need a real routed distance
   cached in `data/walk-routes.json`, which has nothing to do with page
   rendering and every reason to survive. That code moved verbatim into
   `scripts/walk_planning.py`, a new standalone module with no Astro/render
   dependency; `route_walks.py` now imports from there instead. Nothing else
   had a real import, only comments in `site/src/` citing
   `build_site.py:<line>` as where a piece of TS was ported from, which stay
   as historical provenance (resolvable via git history) rather than being
   rewritten. `nightly.yml`'s research-agent prompt and `allowedTools`
   (needed `Bash(npm:*)`/`Bash(npx:*)`, previously only `Bash(git:*)` and
   `Bash(python3:*)`) were updated in the same commit as the deletion, per
   the warning this step used to carry: its self-check now runs
   `(cd site && npm ci && npx astro build)` instead of the Python script.

Each step shipped independently and was reversible until this one (`deploy.yml`
still pointed at the Python build until step 5's commit); step 6 is the point
past which reverting means restoring a deleted file from git history rather
than flipping a config value back, consistent with hard rule 3 treating deleted
code as recoverable-but-not-costless.

## Open decisions

- **Dependency list.** Hard rule 5 requires sign-off on new dependencies.
  Astro itself plus whatever's needed for MapLibre and Supabase in an island
  is a short, boring list (`astro`, `@astrojs/*` as needed, `maplibre-gl`,
  `@supabase/supabase-js`) but it should be enumerated and approved
  explicitly before `npm install` runs, not implied by "we picked Astro."
- **Where UGC pending-pins render first**: every relevant page (city,
  explore) or a dedicated "recent submissions" view — flagged in the prior
  conversation as still open, unaffected by the rendering-engine choice.
- **Timeline.** Not sized here; this doc is the shape, not the schedule.
  Given the steady-fortnight review cadence already running in CLAUDE.md,
  this is worth sequencing as its own tracked effort rather than folded into
  autonomous research runs, since none of the assembly-line agents
  (`verify`, `write-stories`) touch rendering at all.

## What this buys, concretely

- Type-checked data at build time instead of runtime `ERRORS.append()`.
- Component reuse instead of copy-pasted f-string blocks (97 top-level
  functions in `build_site.py` today, several visibly repeating the same
  fact-block/map/breadcrumb patterns).
- A real place for UGC to hydrate without inventing a second stack.
- Zero change to hosting, cost, or the Python research pipeline.
