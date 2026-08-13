# SEO_GEO_BLUEPRINT.md — Ancient Trees
Version 1.11 — Owner: Hidde. No page ships without conforming to this document. Changes require Hidde's explicit approval and a version bump with changelog entry (bottom of file).

This document has two layers with different lifespans. Layer 1 (Principles) should almost never change. Layer 2 (Page Contracts) changes rarely and only via versioning. Volatile tactics (current keyword targets, AI-citation trends, measurement results) do NOT belong here — they live in CLAUDE.md and CURATION.md.

---

## LAYER 1 — PRINCIPLES (stable for years)

**P1. One page, one search intent.** Every page answers exactly one question or serves one intent. The question page answers "what is the oldest tree in X". The tree page serves "tell me about this specific tree". The city page serves "show me the remarkable trees of X". Never merge intents to save pages.

**P2. Answer first, depth behind the click.** The direct answer appears in the first two sentences of every page, unguarded. This makes us quotable by AI engines and featured snippets. The story, the map, the route, and the neighbouring trees are the reasons to click through. We give away the fact and sell the experience.

**P3. Unique content is the moat.** Minimum 30-50% of every page is content that exists nowhere else on the web and nowhere else on this site. Template-filled pages (only the city name swapped) are prohibited — they trigger Helpful Content demotion and they are indistinguishable from the spam we compete against.

**P4. Machine-readable everything.** Every fact that appears as prose also appears as structured data. If a human can read the tree's age, coordinates, and species, so can a crawler and an AI engine. Schema is not an add-on; it is the second rendering of the page.

**P5. Verifiable entity behind the site, within the owner-privacy rule.** Revised in v1.4: the owner chooses maximum personal privacy (2026-07-28), so the site-level entity is the Organization "Ancient Trees", not a named Person. Every page carries WebSite + Organization schema. The trade-off is known and accepted: an organisation signal is weaker than a named person against the anonymous-programmatic-site suspicion; the named-person option and the About page reopen only on the owner's explicit say-so.

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
- **Site-level schema on every page:** WebSite + Organization (Ancient Trees). Person schema parked per the owner-privacy rule (v1.4).
- **OpenGraph/Twitter:** og:title (may match title tag), og:description, og:image, og:type=article. **og:image is the page's own tree photograph whenever one exists**, at 960px; the site logo is the fallback, never the default. A city page's face is its `hero_tree_id`, or the first tree with a usable photo.
- **Every page that owns an image declares it in schema (v1.11).** The page's main entity carries `image`, largest first: the source original for a crawler, then the 960px variant. This is P4 applied to pictures, and it is the only way Google is told which image represents the page rather than guessing. Metadata may point at a larger file than the page renders; the `<img>` itself still goes through `imgSrcset` and qa.py still fails a full-resolution original in an img tag.
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
| Title (≤60 chars) | The search query, plainly, in `seo_title`: a number, a place and the words people actually type (`6 Ancient Trees Older Than the Cities Around Them`). Falls back to `title` when absent. |
| H1 | The editorial `title`, which may differ from the title tag: the tag answers a query, the H1 sets the tone once the reader is on the page. Every superlative in either still passes hard rule 8. |
| Body | Hand-written intro (100-150 words, Paris-quality) → curated entries, 2-3 sentences each + link to tree page, grouped logically (by region or era) |
| Schema | ItemList + BreadcrumbList |
| Internal links | Every entry links to its tree page; footer links to 3+ city pages |
| Hard rule | Curated from verified tree data under the research standard: every entry script-checked (the tree exists, the claimed property holds), superlatives softened or sourced per the project's superlative rule, voice per TONE_OF_VOICE.md. Publishes without owner approval; readers are the correction layer, as everywhere. |

### Contract H — Park page  `/parks/[slug]` + `/parks` index

| Element | Specification |
|---|---|
| Title (≤60 chars) | `Ancient Trees in [Park], [City]: [N] Worth Finding`, or the hand-written `title` when present |
| H1 | `Ancient Trees in [Park]` |
| Body | Hand-written intro (the first sentence becomes the answer-first lede, the rest the prose block) → every mapped tree in the park, oldest first, with thumb, species and its story's opening line |
| Schema | ItemList + BreadcrumbList |
| Internal links | Every tree links to its tree page; links to the park's city, to `/parks`, and to 6 other cities |
| Publish gate | **5+ mapped trees in the park AND a hand-written intro in `data/parks/[slug].json`.** Both, or no page. |
| Hard rule | The gate is higher than the species gate of three deliberately: a park is a place you spend an afternoon, and below five trees a park page is a thin page wearing a park's name while the city page serves the reader better. Parks with 3 or 4 are named on the index in plain text, linked to their city, never given a page. |

The index at `/parks` uses the same browse-card grid as `/cities` and `/species`, and sits in the Explore menu beside Species.

### Contract E — About page  `/about`

Named person, short bio, why this exists, one verifiable external link (LinkedIn or equivalent). Person schema with sameAs. This page exists for entity verification as much as for readers.

### Contract I — Press page  `/press`

| Element | Specification |
|---|---|
| Title (≤60 chars) | `Press and Data: Ancient Trees` |
| H1 | `Press and data` |
| Body | Answer-first lede stating the current headline finding (P2) → dated stories from the data, newest first, each linking its collection page (the AllTrails newsroom pattern: the stories are the page, the kit is the footer) → press kit: one-paragraph boilerplate, downloadable logo and screenshots, the photo-licence rule → what the data is and is not → how to reach us |
| Schema | WebPage + BreadcrumbList |
| Internal links | The collection carrying the headline finding, `/explore`, `/cities`, and the cities named in the angles |
| Hard rule | **Not one number on this page is typed by hand.** Every figure is computed from the published tree data at build time, so the page cannot go stale between a journalist reading it and checking it. A hand-typed number here is the one failure this page cannot survive, because its entire purpose is to be checkable. |
| Hard rule | No personal name and no contact address, per the v1.4 privacy ruling: contact runs through the existing form, exactly as the privacy page does. |
| Hard rule | The caveats ship on the page, not on request: what the count covers, why the map is denser in some countries, and that ages are as sourced with disagreements stated. A press page that omits its own limits is the fastest way to be quoted wrongly and blamed for it. |

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

### Contract G — Country page  `/[country-slug]`

The mid-tier of the pyramid (tree → city → country), added v1.5 on Hidde's instruction after the AllTrails country-page pattern. Targets "ancient trees in [country]" head terms, and gives city pages a linked breadcrumb parent. Semi-automated like Contract F: structure generated, intro hand-written.

| Element | Specification |
|---|---|
| Title (≤60 chars) | `Ancient Trees in [Country]: [N] Cities to Explore` (shorten if over 60) |
| Meta description (≤155) | The country's tree story in one line + strongest city or tree as teaser |
| H1 | `Ancient trees in [Country]` |
| First two sentences | How many cities and trees the site maps there, and the single most remarkable thing among them, quotable standalone (P2) |
| Body | Hand-written country intro (100-150 words, Paris-quality, unique per country, P3) → the country map with the city chooser panel → city photo cards (the design-system card, count + face) → the species that grow there, grouped under the same browse-by-family headings the species index uses (v1.12) → "the oldest tree in [Country]" block linking its tree page → footer links to relevant collections and, where a usable national register exists, an honest one-line register note |
| Schema | CollectionPage + ItemList (cities) + BreadcrumbList |
| Internal links (min) | Every published city in the country; the oldest tree's page; 1+ collection; /cities |
| Breadcrumbs | Home → [Country]. City pages switch their country crumb from plain text to a link the moment the country page exists. |
| Publish gate | A country page ships ONLY when the country has 3+ published cities AND a hand-written intro exists (data/countries/[slug].json). Fewer cities or no intro: no page. A one-city country page is a duplicate of that city page with a flag on it (P3). |
| URL | Root-level country slug (`/netherlands`, `/united-kingdom`). Never a prefix path; collision with city slugs is prevented at build time (build fails on a clash). |

---

### Contract J — Translated city set  `/es/[city]` (v1.10, test scope)

Approved by Hidde in session 2026-08-10 ("wat als we een paar spaanse paginas
maken en testen of het werkt? maar wel een opzet doen die op de lange termijn
werkt"). One city translated end to end as a market test, inside the structure
that scales if it works.

- **URL shape:** language subdirectory. `/es/{city}`, `/es/{city}/{tree-slug}`
  (tree slugs stay identical to English), `/es/{city}/arbol-mas-antiguo` for
  the question page (the searched phrase, not an English path segment).
- **hreflang is reciprocal or it is nothing.** Every translated page and its
  English pair each carry `hreflang` links to both versions plus `x-default`
  pointing at English. The English city page also carries one visible link to
  the Spanish version, which doubles as the qa.py inbound-link guarantee.
- **Translation is an overlay, never a fork.** `data/i18n/{lang}/{slug}.json`
  holds translated text only (names, stories, intro, question set, FAQ,
  access/transport lines, Spanish common species names). Coordinates, photos,
  licences, walks and every future correction live solely in the canonical
  city file. The build fails if the overlay misses a tree the English city
  has, so a city cannot grow past its translation silently.
- **Same bars, same numbers:** intro 60-100 words, stories 150-250, title max
  60, descriptions max 155, no em dashes, answer-first on the question page.
  Hand-written in the target language; mechanically patched text is forbidden
  (the 2026-08-09 accent incident is the reason this sentence exists).
- **Known limits of the test, deliberate:** site chrome (nav, footer), map
  popups and the season block stay English. If the test earns a second
  language or a wider rollout, those become contract items, not silent debt.
- **The test's measure, recorded so the page is judged by it:** Malaga was
  chosen because "árboles históricos de málaga" showed 20 impressions at
  position 74 with our English page. The question is whether `/es/malaga`
  moves on that query within four weeks of indexing.

## MEASUREMENT CONTRACT (what proves this blueprint works)

The hypothesis order, checked in Search Console: (1) question pages show impressions first (months 2-3), (2) tree pages follow on long-tail tree names, (3) city pages gain last as authority compounds. Secondary signal: submissions via the suggestion forms. If question pages show zero movement by month 4, the strategy — not the effort — gets reviewed. This contract exists so that "keep building" never substitutes for "check if it works".

---

## CHANGELOG

- **v1.11 (2026-08-11):** og:image and schema `image`, approved by Hidde in session ("ja verbeter en SEO_GEO_BLUEPRINT"). He spotted it in Search Console Insights: of 95 city pages only /lisbon showed a tree photograph beside its result and every other page showed our generic logo. Two causes, both real. City pages never set og:image from their own photo, so all 95 emitted `og-default.png`; tree pages did set one. And NO page of any type declared `image` in its structured data, so Google was left to guess a thumbnail from the markup. Both fixed: city pages now take their face photo (hero tree, else first tree with a usable photo) as og:image, and city, tree and list entities all carry a schema `image` array. A thumbnail beside a result moves click-through more than any title rewrite, which matters on a site whose measured problem is click-through, and it applies to every page at once rather than city by city.
- **v1.9 (2026-08-08):** Contract I restructured newsroom-first, approved by Hidde in session ("maak maar die perspagina") after he judged the v1.8 page useless ("vrij bizar... wat doet bijvoorbeeld AllTrails op een perspagina") and a convention check of AllTrails' newsroom answered him: their press page is data stories first, kit second. Ours now leads with dated stories from the data, then a press kit (generated boilerplate, downloadable logo SVG, live-site screenshots), then the caveats and the form. The page also left the global footer the same day: it is reachable from the contribute form and from pitches, a destination for journalists rather than site furniture. The no-hand-typed-numbers rule is unchanged.
- **v1.8 (2026-08-08):** Added Contract I (press page `/press`), approved by Hidde in session ("pers pagina is prima"). Built because the site had a press-worthy finding and nowhere to send a journalist: four in ten of the ancient trees we map in European cities are not European species. The contract's distinguishing rule is that no number on the page may be hand-typed, all of them generate from the tree data at build time, since a press page exists to be checked and a stale figure there costs more than no page at all. Carries its own caveats rather than supplying them on request.
- **v1.7 (2026-08-07):** Added Contract H (park page `/parks/[slug]` + `/parks` index), approved by Hidde in session ("so parks do it now"). His reasoning: parks are a browse facet visitors already think in, and the search evidence agrees, since "york museum gardens" is the site's best-performing query at position 4 and "den brandt park" surfaced with 12 impressions and no page. Publish-gated at 5 trees plus a hand-written intro, a higher bar than the species contract's three because a park page with four trees is a thin page wearing a park's name. 9 parks qualify at launch, 3 have intros and pages.
- **v1.6 (2026-08-01):** Contract D splits the title tag from the H1, approved by Hidde in session ("de content beslissing rond collecties klinken goed doe het maar") after he judged the collection titles weak for search. The editorial titles were doing double duty: strong as headings, invisible to search, because nobody types "Trees That Outlived Their City". New optional `seo_title` per collection carries the query-shaped version; `title` stays the H1. All 12 collections got one the same day.
- v1.3 — Contract D loses the owner-approval gate, approved by Hidde ("yes pas aan", 2026-07-27). It was the last place he sat as a mandatory quality gate, contradicting the recorded principle that the system publishes and readers correct. The risks it guarded are covered without him: entries are script-verifiable against the tree data, superlatives fall under the existing softening rule, voice under TONE_OF_VOICE.md. Collections now publish like cities do.
- v1.2 — Removed the curation-status banner from every page type, approved by Hidde. He is not the quality gate and never will be at 1,000 trees, so promising "final human review is still in progress" was a promise nobody was going to keep. The bar is now the research standard already applied (two independent sources) plus readers as the correction layer. Two replacements: every tree page carries a visible "is something here not right?" invitation, and a tree whose pin is only approximate says so next to the directions button, because that costs the visitor a wasted walk. Uncertainty about age stays where it already was, inside the story text as a stated range (P7).
- v1.1 — Added Contract F (species page `/species/[slug]` + `/species` index), approved by Hidde. Semi-automated browse facet: auto-generated entry list, hand-written intro, publish-gated at 3+ trees and an intro. Single-species collections are now folded into this contract to avoid duplicate content.
- v1.0 — Initial blueprint. Consolidates: four-layer architecture, AllTrails-pattern page structure, metadata contracts, schema stacks, freshness rule, entity requirements, measurement hypothesis.

- **v1.12 (2026-08-13):** Contract G gains a species section, on Hidde's instruction in session ("the country page feels not updated - we also need to include that like species and it probably needs conventional clusters too"). Counted from the country's own published trees and grouped under the browse-by-family headings the species index already uses, which now live in `site/src/lib/species.ts` so the two pages cannot drift apart. Species with a Contract F page are linked, the rest are named in plain text; the internal-link minimum is unchanged and this only adds to it.

- **v1.5 (2026-07-31):** Added Contract G (country page `/[country-slug]`), approved by Hidde ("voeg het landencontract toe en neem dit mee in de totale seo strategie"). The AllTrails country-page pattern sized to our honesty rules: publish-gated at 3+ published cities plus a hand-written intro, so no one-city duplicate pages exist. Slots the pyramid's missing middle tier (tree → city → country) and gives every city page a linked breadcrumb parent.
- **v1.4 (2026-07-28):** Owner-privacy rule applied on Hidde's instruction in session: P5 and site-level schema switch from named Person to Organization; About page (Contract E) parked indefinitely. Trade-off recorded in P5 itself.
