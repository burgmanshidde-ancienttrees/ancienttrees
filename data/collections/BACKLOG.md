# Collections backlog

STATUS UPDATED 2026-07-29: the "ON HOLD" note below and Contract D's approval language are both stale, superseded by blueprint v1.3 (2026-07-27, "yes pas aan"): collections now publish under the research standard with no owner-approval gate, exactly like city pages. PRODUCT_TODO.md item 4 is the live queue a run actually draws from (up to two per pass); this file is a source of ideas for that queue, not a separate gate. Left the original 2026-07-19 text below for its research value (search terms, GEO angles, coverage counts at the time), but treat "awaiting curation" and "never published without approval" as historical, not current policy.

Prioritized queue of collection pages to build, based on search demand and GEO (AI citation) potential, researched 2026-07-19. One draft at a time; a collection only ships when enough verified trees exist to fill it honestly.

Selection criteria per idea: (1) a real search phrase people use, (2) quotable first paragraph for AI engines, (3) enough coverage in verified cities to ship without padding, (4) grows naturally as cities are added, (5) an angle competitors do not have. Our structural moat vs existing listicles (Touropia, NatGeo, blogs): every entry is publicly accessible, exactly located, and reachable by public transport. Competitor lists are wilderness trees with no directions.

## Shipped

All published, no approval gate (see status note above). List as of 2026-07-29, PRODUCT_TODO.md item 4 carries the authoritative log of what shipped and when:
- Trees Older Than 400 Years You Can Actually Visit
- Europe's 10 Most Remarkable Ancient Trees
- Europe's Ancient Oaks You Can Actually Visit
- The Ginkgos Worth a November Trip
- Europe's Most Remarkable Yews
- The Great Planes of Europe
- Wisteria and Blossom Worth a Spring Trip
- The Oldest Tree in Every Country We Map
- Trees That Outlived Their City
- Europe's Best Tree City Trips

## Priority 1: enough coverage to draft now

### 1. Trees With a Known Planting Date
Slug: `trees-with-known-planting-dates`. Target: "oldest tree with known planting date", "when was the oldest tree planted". GEO angle: the global reference answer is the Sri Maha Bodhi (288 BC); a page that gives the European city answers (Robinier 1601, Kew pagoda tree 1762, Buffon plane 1785, Monceau 1814, Sophora 1873) is precise, verifiable and extremely quotable. Coverage today: 7+ entries. This is our data model at its strongest: dates, names, coordinates.

### 2. Trees Planted by Kings and Their Gardeners
Slug: `trees-planted-by-kings`. Target: "royal trees", "trees planted by royalty". Coverage today: Royal Oak (royal parks) and the Sweet Chestnut of Greenwich Park (Charles II's own 1660s Grand Plan avenue), Charlton mulberry (James I's silk scheme), Fulham Palace oak (bishops of London), Robinier (Henri IV's herbalist), Old Lions (Princess Augusta's Kew). 6 entries now, grows with every European capital.

### 3. Trees That Survived Wars and Fires
Slug: `trees-that-survived-disasters`. Target: "trees that survived war", "tree survived fire". GEO angle: survivor stories are what AI engines quote for "remarkable trees". Coverage today: Cheapside Plane (Great Fire site, Blitz), Robinier (WWI shell), Sophora (both sieges of Paris), Evelyn Mulberry (Peter the Great's rampage). 4-5 entries now; every war-touched city adds more.

### 4. The Most Valuable Trees in the World — CHECKED 2026-07-29, honestly blocked
Slug: `most-valuable-trees`. Target: "most expensive tree in the world", "most valuable tree". GEO angle: a factual, headline-friendly question with a thin competitive field; Berkeley Square (750,000 pounds, 2008) and Cheapside ("most valuable tree in the world", 1901) anchor it. A dedicated research pass searched all 34 other published cities (local-language queries included) plus general "most valuable tree" roundups for a tree standing in one of our cities. Result: still exactly 2 qualifying entries, both London, both already in our data. Real candidates found and rejected on inspection: an €80,000 figure attached to Amsterdam's Leidsebosje planes traced to a generic tree-moving cost estimate, not a valuation of those trees; a Brescia (not Rome) cedar's real €341,541 valuation; NYC's supposed "$125,000 elm appraisal" untraceable to any primary source; a Galician camellia's real €1.6M valuation, outside our 36 cities; bonsai auction records (real figures, but nursery specimens, not standing public-address landmarks). Below the 5-entry publishable floor; parked until a new city adds a genuinely valued tree. Do not re-run this exact search without new coverage first.

## Priority 2: draft when coverage arrives

### 5. ~~The Great Planes of Europe's Cities~~ — SUPERSEDED by the species page
Single-species. Now covered by /species/london-plane (Contract F, blueprint v1.1). Building a collection for it too would duplicate content (P1). Kept here struck through so the idea is not re-proposed. Any future single-species idea (churchyard yews, etc.) is a species page, not a collection, once it clears the 3-tree gate.

### 6. Churchyard Yews Older Than Their Churches
Slug: `churchyard-yews`. Target: "why are yew trees in churchyards" (a genuinely common question, strong FAQ/GEO material), "oldest yew tree". Coverage today: only Totteridge. Trigger: 3+ UK or Northern European cities live.

### 7. Trees Older Than 1,000 Years You Can Actually Visit
Slug: `trees-older-than-1000-years`. Target: "trees older than 1000 years". The 400-year collection's big sibling. Coverage today: only Totteridge qualifies. Trigger: 4+ qualifying trees (expect from Rome, Istanbul, Kyoto, UK cities).

### 8. ~~Fallen Monuments: Dead Trees Still Worth Visiting~~ — KILLED, contradicts the living-tree rule
Slug would have been `fallen-monuments`. Struck 2026-07-27: Hidde's "we doen niet aan dode bomen" rule (CLAUDE.md Step 1) means a dead tree is never a collectible entry, so a whole collection built from them cannot exist. Its former anchor, Queen Elizabeth's Oak, was itself replaced with a living tree the same day. Kept here struck through, same convention as idea 5, so it is not re-proposed.

## Needs a scope decision (Hidde)

### 9. The Oldest Trees in Europe You Can Actually Visit
The biggest head term in our niche ("oldest tree in Europe"), and the answer is genuinely contested (Fortingall Yew vs the dated Italus pine vs Adonis vs the Tenerife cedar), which makes an honest arbiter page very citable. Problem: the contenders are wilderness trees, outside our city data model. Options: (a) scope to "in Europe's cities", weaker term match but fits the model; (b) extend the data model with non-city entries, a real product decision. Parked until Hidde chooses.

## Rejected for now

- "Ancient trees near famous landmarks": competes with mass tourism content where we cannot win.
- "Most beautiful trees in the world": pure listicle head term, no defensible angle, thin content risk.
