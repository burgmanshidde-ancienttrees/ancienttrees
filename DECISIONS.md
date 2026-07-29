# Decisions

One dated entry per decision that shapes the product, newest first: what was decided, by whom, and why. This file exists because the 2026-07-27 assumption audit showed decisions scattered across five documents and chat, which is how observations silently harden into rules. New decisions land here the day they are made; older ones migrate when a document touching them is edited anyway. The standard here is the lightweight ADR (Architecture Decision Record) practice, ours-sized.

- **2026-07-29 — Hidde:** One fixed hero photo (the Kevin Young frame), rotation and photo bank dropped, visible credit removed (Unsplash License permits; attribution stays recorded in source per hard rule 4). New hero candidates only when he brings them.
- **2026-07-29 — Hidde:** QA is a three-layer work form: build-time contract checks (every build), scripts/qa.py as a deploy gate (every push: dead links, banned words, em dashes, File: page urls), and the visual composition walk of every page type at desktop and 375px as a recurring ritual, every two weeks and after any visual system change.
- **2026-07-29 — Hidde:** Consistency must be systemic, not remembered: design tokens in the shared CSS plus DESIGN_SYSTEM.md; a visual change edits the token or component, never one page's instance. Figma explicitly not the vehicle while the product is generated from one file; tokens translate 1:1 to Figma variables when a human designer joins.
- **2026-07-28 — Hidde:** The capacity doctrine: runs chain day and night; a session presence beacon pauses the daytime chain 4 hours; silence means the machine runs.
- **2026-07-28 — Hidde:** Product direction sealed: soul = trees, form = AllTrails rebuilt, walking routes as extra never as base. Five recorded deviations (PRODUCT_IA.md).
- **2026-07-28 — Hidde:** Owner privacy is maximal: no personal name, location or email anywhere public; Organization schema; the SEO cost is accepted and recorded.
- **2026-07-28 — Hidde:** Public copy makes no forever-promises (no "never ads"); ads/tracking remain an internal default only he can change.
- **2026-07-28 — Hidde:** Privacy page approved ("prima dit"); sign-in wired to his Supabase, field-tested by him; delete function is the hard gate before public linking.
- **2026-07-28 — Hidde:** Japan wave recomposed around his own trip (deadline 2026-08-22); rollout is his strategy, scans inform, only he reorders.
- **2026-07-27 — Hidde:** Europe top-10 city trips: walk-weighted ranking, Palermo/Cadiz/Sintra exception to the coverage freeze.
- **2026-07-27 — Hidde:** Cookieless analytics in, ads/ad-tracking out; no spending without approval, no fixed ceiling, condition: start earning.
- **2026-07-27 — Hidde:** Interim identity: Direction A (Gabarito, warmed palette), logo 3A, explicitly temporary until a real designer pass.
- **2026-07-26 — Hidde:** The four verbs (find, walk, collect, season); count follows the trees, ten is a cap; no points, the currency is years.
