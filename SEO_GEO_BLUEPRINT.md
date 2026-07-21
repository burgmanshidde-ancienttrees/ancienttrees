# SEO_GEO_BLUEPRINT.md — Ancient Trees
Version 1.2 — Owner: Hidde. No page ships without conforming to this document. Changes require Hidde's explicit approval and a version bump with changelog entry (bottom of file).

This document has two layers with different lifespans. Layer 1 (Principles) should almost never change. Layer 2 (Page Contracts) changes rarely and only via versioning. Volatile tactics (current keyword targets, AI-citation trends, measurement results) do NOT belong here — they live in CLAUDE.md and CURATION.md.

---

## LAYER 1 — PRINCIPLES (stable for years)

**P1. One page, one search intent.** Every page answers exactly one question or serves one intent. The question page answers "what is the oldest tree in X". The tree page serves "tell me about this specific tree". The city page serves "show me the remarkable trees of X". Never merge intents to save pages.

**P2. Answer first, depth behind the click.** The direct answer appears in the first two sentences of every page, unguarded. This makes us quotable by AI engines and featured snippets. The story, the map, the route, and the neighbouring trees are the reasons to click through. We give away the fact and sell the experience.

**P3. Unique content is the moat.** Minimum 30-50% of every page is content that exists nowhere else on the web and nowhere else on this site. Template-filled pages (only the city name swapped) are prohibited — they trigger Helpful Content demotion and they are indistinguishable from the spam we compete against.

**P4. Machine-readable everything.** Every fact that appears as prose also appears as structured data. If a human can read the tree's age, coordinates, and species, so can a crawler and an AI engine. Schema is not an add-on; it is the second rendering of the page.

**P5. Verifiable entity behind the site.** The site is publishe by a named, real person (Hidde) with a verifiable footprint. Every page carries site-level Person/WebSite schema. Anonymous programmatic sites are held in trust-limbo; named ones are not.

**P6. Freshness is systematic, not incidental.** Every page receives a genuine content update (new fact, updated status, refreshed date) at least once per quarter via the nightly improvement cycle. Recency is a measurable citation factor; we build it into the machine rather than hoping for it.

**P7. Truth outranks polish.** A flagged uncertainty ("estimates range from 1,000 to 2,000 years") is stronger content than a confident error. Factual errors are the only thing that can permanently kill this site's authority with both Google and the tree community. When sources conflict: state the range, cite the disagreement.

**P8. Internal links are the site's circulatory system.** No orphan pages, no dead ends. Every page links up (to its city), sideways (to peers), and down (to details) per the minima in Layer 2. Link text is descriptive ("the 2,000-year-old Totteridge Yew"), never "click here".

**P9. Free content is the acquisition engine, forever.** The content layers (city, tree, question, collection pages) stay free and indexable permanently. Paid is convenience (app, offline, navigation). No paywall ever blocks a crawler or a first-time reader from the content itself.

---

## LAYER 2 — PAGE CONTRACTS (versioned, enforced by templates)

### Global rules (all page types)

- **URLs:** lowercase, hyphens, no trailing slash, no dates. Patterns are permanent — a URL never changes once published (redirects only for genuine corrections).
- **Canonical:** every page self-canonical unless explicitly deduplicating.
- **Breadcrumbs:** visible on page AND as BreadcrumbList schema. Path: Home > [Country] > [City] > [Tree].
- **Site-level schema on every page:** WebSite + Person (Hidde, with sameAs link to a verifiable profile).
- **OpenGraph/Twitter:** og:title (may match title tag), og:description, og:image (tree photo when available; generated map-card of the location until then), og:type=article.
- **Build-time validation:** title length, description length, schema validity, and link minima are checked at build. A page that fails validation does not deploy.
- **Language:** English. Local-language tree names appear in the body and may appear in the title where the tree is famous under that name.

### Contract A — Tree page  `/[city]/[tree-slug]`

| Element | Specification |
|---|---|
| Title (≤60 chars) | `[Tree Name]: [Age] Year Old [Species] in [City]` |
| Meta description (≤155) | Answer + hook: what it is, why it's remarkable, one click-reason |
| H1 | Tree name (local name in parentheses if famous) |
| Above the fold | Fact block, scannable, no prose: Species (common + scientific) · Age estimate · Location + neighbourhood · Access (free/paid) · Nearest station + walk time |
| Body order | Story (150-250 words, unique) → Map (single pin) → "Trees nearby" (2-3 same-city trees) → FAQ if applicable → interaction elements (correction / photo / worth-the-detour) |
| Schema | TouristAttraction (name, description, geo lat/long, isAccessibleForFree) + BreadcrumbList |
| Internal links (min) | 4 outgoing: city page, 2-3 nearby trees, city question page |

### Contract B — Question page  `/[city]/oldest-tree`

| Element | Specification |
|---|---|
| Title (≤60 chars) | `What Is the Oldest Tree in [City]? ([Tree Name], [Age] Years)` |
| Meta description (≤155) | The literal answer + invitation to the full list |
| H1 | The question, verbatim |
| First two sentences | The complete answer: name, age, exact location. Quotable standalone. |
| Body | 150-200 words unique context → map → explicit click-path: "See all 10 remarkable trees in [City]" + walking route from nearest station |
| Schema | FAQPage (the title question + 2-3 related) + BreadcrumbList |
| Internal links (min) | 3: the tree page, the city page, one thematic collection |
| Hard rule | First paragraph written per city. Never a fill-in template. |

### Contract C — City page  `/[city]`

| Element | Specification |
|---|---|
| Title (≤60 chars) | `Ancient Trees in [City]: 10 Remarkable Trees Worth Visiting` |
| Meta description (≤155) | City hook + the strongest single tree as teaser |
| H1 | Ancient Trees in [City] |
| Intro | 60-100 words, unique per city: why THIS city's trees matter |
| Body | The 10 trees, each: rank, name, species/age/neighbourhood line, story, access + transport, link to tree page → FAQ block (3-4 real questions incl. "What is the oldest tree in [City]?") → "Know a tree that belongs on this list?" + suggestion link |
| Schema | ItemList (the 10 trees) + FAQPage + BreadcrumbList |
| Internal links (min) | 12: all 10 tree pages, question page, 1+ collection page |
| Ordering rule | List order is editorial. Votes are curation signal, never ranking. |

### Contract D — Collection page  `/collections/[slug]`

| Element | Specification |
|---|---|
| Title (≤60 chars) | The promise, plainly: `Trees Older Than 1,000 Years You Can Actually Visit` |
| H1 | Matches title |
| Body | Hand-written intro (100-150 words, Paris-quality) → curated entries, 2-3 sentences each + link to tree page, grouped logically (by region or era) |
| Schema | ItemList + BreadcrumbList |
| Internal links | Every entry links to its tree page; footer links to 3+ city pages |
| Hard rule | Hand-curated, never auto-generated. These are editorial products. |

### Contract E — About page  `/about`

Named person, short bio, why this exists, one verifiable external link (LinkedIn or equivalent). Person schema with sameAs. This page exists for entity verification as much as for readers.

### Contract F — Species page  `/species/[slug]`

The one browse facet: "show me every [species] on the site". Semi-automated. The entry list is generated from tree data; the intro is hand-written, which is what keeps the page off the thin-content pile.

| Element | Specification |
|---|---|
| Title (≤60 chars) | `[Common Name]: Ancient [Common Name]s You Can Visit` (shorten if over 60) |
| Meta description (≤155) | What the species is + the strongest single specimen as teaser |
| H1 | The common name |
| First two sentences | What the species is and how many the site has mapped, quotable standalone |
| Body | Hand-written intro (100-150 words, Paris-quality, unique per species) → the trees of that species, grouped by city, each with age/neighbourhood + link to its tree page → footer links to city pages |
| Schema | ItemList + BreadcrumbList |
| Internal links (min) | Every listed tree links to its tree page; the /species index; footer links to 2+ city pages |
| Publish gate | A species page ships ONLY when it has 3+ renderable trees on the site AND a hand-written intro exists for it. Fewer trees or no intro: no page (P3). Never a bare templated list. |
| Index | `/species` lists every published species page. One species is never split across two collections and a species page; a single-species collection is prohibited (use the species page). |

---

## MEASUREMENT CONTRACT (what proves this blueprint works)

The hypothesis order, checked in Search Console: (1) question pages show impressions first (months 2-3), (2) tree pages follow on long-tail tree names, (3) city pages gain last as authority compounds. Secondary signal: submissions via the suggestion forms. If question pages show zero movement by month 4, the strategy — not the effort — gets reviewed. This contract exists so that "keep building" never substitutes for "check if it works".

---

## CHANGELOG
- v1.2 — Removed the curation-status banner from every page type, approved by Hidde. He is not the quality gate and never will be at 1,000 trees, so promising "final human review is still in progress" was a promise nobody was going to keep. The bar is now the research standard already applied (two independent sources) plus readers as the correction layer. Two replacements: every tree page carries a visible "is something here not right?" invitation, and a tree whose pin is only approximate says so next to the directions button, because that costs the visitor a wasted walk. Uncertainty about age stays where it already was, inside the story text as a stated range (P7).
- v1.1 — Added Contract F (species page `/species/[slug]` + `/species` index), approved by Hidde. Semi-automated browse facet: auto-generated entry list, hand-written intro, publish-gated at 3+ trees and an intro. Single-species collections are now folded into this contract to avoid duplicate content.
- v1.0 — Initial blueprint. Consolidates: four-layer architecture, AllTrails-pattern page structure, metadata contracts, schema stacks, freshness rule, entity requirements, measurement hypothesis.
