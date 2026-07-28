# The target information architecture

Written 2026-07-28 from the nine-product benchmark (AllTrails, Komoot, Wikiloc, Geocaching, eBird, Atlas Obscura, Strava, Polarsteps, PictureThis; full teardowns in the session transcript, rulings in COMPETITION.md). Hidde's frame: copy the form, keep the soul. This document is the form we are copying toward. It changes navigation, page anatomy and emphasis; it never moves an existing URL.

## The five laws the benchmark converged on

1. **Search and find is the hero; the SEO directory is the basement.** All nine lead with one action (search near you, sign up); their enormous programmatic directories sit in below-the-fold link blocks, one Explore hub, breadcrumbs and the footer. Fully crawlable, never occupying the living room. Our homepage hero already does this right; the 36-city grid on the homepage is the part that violates it.
2. **The detail page has a fixed anatomy, and the do-buttons live at the top.** Photos + title + rating/stats + the action buttons above the fold; story, waypoints, reviews below; nearby-cards at the end so no session dead-ends. Atlas Obscura puts Been Here and Want to Go above the story; Wikiloc's collect is one click ("I've navigated this trail"); AllTrails opens with an answer-first paragraph; eBird answers "why go this month" on the page itself.
3. **Content is never the paywall.** Two gates, in order: a FREE account captures the keep-verbs (collect, save, lists: Geocaching converts on it, eBird personalizes on it, Atlas Obscura socializes on it), and the PAID tier sells in-the-field convenience (offline, alerts, navigation, GPS export). The upgrade prompt appears contextually next to the gated feature, not as a nav item.
4. **Web reads, app walks.** Every product keeps reading free on web and attaches recording/navigation to the app. For our current phase the posture to copy is Strava's: the homepage sells a WEB account, app badges wait in the footer until there is an app. Polarsteps is the cautionary tale: their web decayed into an SPA that renders "Page not found" under correct SEO titles. Our static pages are a quiet strength; never trade them away.
5. **The nav carries verbs, not content types.** eBird: Submit, Explore, My eBird. AllTrails keeps "Saved" in the logged-out nav as a hook. Our current nav (Cities, Species, Collections) is a content-type list, which is exactly why the site feels like a database with a product hidden in it.

## The target navigation

    [logo] Map | Walks | In season | Explore v          [My trees] [Sign in]

- **Map**: the find-near-me product, the homepage hero grown up.
- **Walks**: the signature walks index (ships when the routes ship; until then the item stays hidden).
- **In season**: exists today at /in-season; promoted to the nav because it is our sharpest "why now".
- **Explore** (dropdown): Cities, Species, Collections, Suggest a tree: the entire acquisition layer in one hub, eBird-style. Nothing deleted, everything demoted.
- **My trees**: the collection, visible logged-out as the AllTrails-style hook; becomes the account dashboard.

URLs do not move. City pages stay at /[city], tree pages at /[city]/[tree]. This is re-emphasis, not migration.

## The homepage, reordered

1. Hero: find trees near you (search + map). Unchanged in spirit, already right.
2. The four verbs as sections (find, walk, collect, season). Exists; tighten.
3. One opinionated shelf: the flagship collection (top-10 trips) plus in-season now. Lists with an opinion are the shareable layer.
4. A COMPACT explore directory: country-grouped city links, plain names, plus species and collections links. The current 36-card grid moves here in a fraction of the height, exactly the AllTrails "Adventure anywhere" block: present for crawlers and the determined, invisible as furniture.

## The tree page, target anatomy (the product page Hidde asked to wireframe)

    photo or painterly illustration
    Tree name                         [age chip] [species chip] [pin-honesty chip]
    [ Collect: I stood here ]  [ Directions ]  [ Walk from here ]
    Answer-first opening line (what it is, why it is worth the walk)
    The story (150-250 words)
    Season block: "at its best in November" + the radar tie-in (eBird's why-go-now)
    Practical: access, transport, coordinates
    Nearby trees (cards, with distances)     <- no dead ends
    Part of: [city page] [collection]

The collect button sits above the story (Atlas Obscura's law). Logged-out it still shows, and tapping it invites the free account, which is the Geocaching conversion engine pointed at our honest version: we never hide coordinates; identity gates only the KEEPING of things.

## The city page, target anatomy

Stays the workhorse it is. Order tightens to: map with the ten pins, then the walk banner ("Walk 7 of these trees, 4.9 km"), then the ten trees with collect buttons on each row, then explore-onward links. The question pages, species pages and collections keep feeding it from below.

## The five deliberate deviations from AllTrails (Hidde asked "wijk ergens af?", 2026-07-28)

Everything else copies wholesale. These five do not: (1) URL structure stays our flat /city/tree, never their deep /trail/country/region path: ours is indexed, short and irreversible territory. (2) No Shop item until there is something to sell (the keepsake, someday). (3) No star ratings ever: their soul is volume-plus-reviews, ours is ten-that-all-deserve-it; our future signal is the binary worth-it tap. (4) No user route planner: our walks are curated. (5) The species layer stays: an axis AllTrails does not have, our PictureThis side.

## Phasing

- **Phase A, now (session work, needs Hidde's eyes):** nav switches to verbs with the Explore dropdown; homepage city grid compresses into the directory block; tree pages move actions above the story and gain the nearby-trees footer. No URL changes, no new features, pure re-emphasis.
- **Phase B, when accounts open publicly:** My trees in the nav, collect buttons as signup hooks everywhere, the localized hook on the homepage ("N remarkable trees around [city], free account to collect them").
- **Phase C, app era:** "Start the walk" handoff per page, paid convenience layer with contextual prompts (offline city packs, season alerts, GPX-to-watch), pricing page only when there is a price, which is Hidde's alone.

The tree-first versus walk-first question stays open (BACKLOG.md, checkpoint mid-September); this IA embodies the working hypothesis by making the tree the hero object and the walk the first-class button beside it, which survives either answer.
