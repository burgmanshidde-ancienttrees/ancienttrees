# The target information architecture

Written 2026-07-28 from the nine-product benchmark (AllTrails, Komoot, Wikiloc, Geocaching, eBird, Atlas Obscura, Strava, Polarsteps, PictureThis; full teardowns in the session transcript, rulings in COMPETITION.md). Hidde's frame: copy the form, keep the soul. This document is the form we are copying toward. It changes navigation, page anatomy and emphasis; it never moves an existing URL.

## The five laws the benchmark converged on

1. **Search and find is the hero; the SEO directory is the basement.** All nine lead with one action (search near you, sign up); their enormous programmatic directories sit in below-the-fold link blocks, one Explore hub, breadcrumbs and the footer. Fully crawlable, never occupying the living room. Our homepage hero already does this right; the 36-city grid on the homepage is the part that violates it.
2. **The detail page has a fixed anatomy, and the do-buttons live at the top.** Photos + title + rating/stats + the action buttons above the fold; story, waypoints, reviews below; nearby-cards at the end so no session dead-ends. Atlas Obscura puts Been Here and Want to Go above the story; Wikiloc's collect is one click ("I've navigated this trail"); AllTrails opens with an answer-first paragraph; eBird answers "why go this month" on the page itself.
3. **Content is never the paywall.** Two gates, in order: a FREE account captures the keep-verbs (collect, save, lists: Geocaching converts on it, eBird personalizes on it, Atlas Obscura socializes on it), and the PAID tier sells in-the-field convenience (offline, alerts, navigation, GPS export). The upgrade prompt appears contextually next to the gated feature, not as a nav item.
4. **Web reads, app walks.** Every product keeps reading free on web and attaches recording/navigation to the app. For our current phase the posture to copy is Strava's: the homepage sells a WEB account, app badges wait in the footer until there is an app. Polarsteps is the cautionary tale: their web decayed into an SPA that renders "Page not found" under correct SEO titles. Our static pages are a quiet strength; never trade them away.
5. **The nav carries verbs, not content types.** eBird: Submit, Explore, My eBird. AllTrails keeps "Saved" in the logged-out nav as a hook. Our current nav (Cities, Species, Collections) is a content-type list, which is exactly why the site feels like a database with a product hidden in it.

## The target navigation

    [logo] Map | Walks | Explore v          [My trees] [Sign in]

- **Map**: the find-near-me product, the homepage hero grown up.
- **Walks**: an index of cities that have walks, never a page per walk. See the walks ruling below; until walks ship, the item stays hidden.
- **In season**: demoted from the nav on 2026-07-29 (Hidde: "wordt veel te belangrijk gemaakt"). Season is a map layer (gold pins, pulse, popup badge) and a per-tree block, not a destination; /in-season stays live for search but is linked only from season contexts and the footer.
- **Explore** (dropdown): Cities, Countries, Species, Collections, Suggest a tree: the entire acquisition layer in one hub, eBird-style. Nothing deleted, everything demoted. Countries joined on 2026-08-04, after Hidde could not find the country pages that had been live and unlinked since 2026-08-01; /countries is their index and every country page is one hop from the menu.
- **My trees**: the collection, visible logged-out as the AllTrails-style hook; becomes the account dashboard.

URLs do not move. City pages stay at /[city], tree pages at /[city]/[tree]. This is re-emphasis, not migration.

## The homepage, reordered

1. Hero: find trees near you (search over a rotating curated photo, AllTrails-style). Amended 2026-07-28: the map moved to /explore; Hidde's grounds, plus his own addition that a sparse world map advertises incompleteness. The show-don't-tell principle now lives in the /explore page and the verb sections, and the hero photo bank is curated for one mood: warm light, one epic tree, human scale.
2. The four verbs as sections (find, walk, collect, season), with their own visuals. Exists; tighten, never duplicate. On 2026-08-04 a second, thinner three-step band was added above it, so a visitor met the same promise twice within one screen and Hidde called the page a mess. The band was removed and this line is the reason it should never come back: if find/walk/collect needs more prominence, it is this section that moves or grows.
3. One opinionated shelf: the flagship collection (top-10 trips) plus in-season now. Lists with an opinion are the shareable layer.
4. A COMPACT explore directory: country-grouped city links, plain names, plus species and collections links. The current 36-card grid moves here in a fraction of the height, exactly the AllTrails "Adventure anywhere" block: present for crawlers and the determined, invisible as furniture.

## The funnel, written down (2026-08-04, because it was implied everywhere and stated nowhere)

Where a visitor comes in, where they should go, and what counts as arriving.

    search / social  ->  tree page or city page      (85% of entries land deep, not on the homepage)
                          |
                          v
                     the map, near me                (the product: what is around me)
                          |
                          v
                     directions clicked              <- THE conversion. Goal 1 in one event.
                          |
                          v
                     collect / the app               (the keep-verb, gated by an account later)

Three things follow from this shape and are easy to forget:

- **The deep page is the front door.** Most people never see the homepage, so every tree and city page has to work as a first impression on its own: it must say where it is, why it is worth the walk, and what else is nearby. The nearby-cards exist for exactly this reason.
- **The conversion is a directions click, not a signup.** It is the only event on the site that means someone might actually stand in front of a tree, which is goal 1. Everything else is a proxy. This is why the events counter exists and why the weekly scorecard leads with directions-per-visit.
- **The ask comes after the value, never before it.** Contribution asks belong at the bottom of a page or beside the gap they refer to, not stacked under the value proposition at the top. The 2026-08-04 homepage mistake was exactly this ordering error.

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

Stays the workhorse it is. Order tightens to: map with the pins, then the walks (see the ruling below), then the trees with collect buttons on each row, then explore-onward links. The question pages, species pages and collections keep feeding it from below.

## Walks are an APP feature. Ruled by Hidde, 2026-08-18, superseding the section below

His words: "je mag van mij de walking routes achter een kleinere knop zetten op de kaart, dat is een diepere filter dan, die ik niet beschikbaar wil maken op web, maar die je naar de landingspagina van de app brengt omdat ze daar beschikbaar zijn, zodat er meer ruimte is voor de kaart en de bomen."

So the web city page no longer offers walks. Where the green route capsule, the walk picker and the drawn route line used to sit, there is one small pill on the map reading "Walking routes, in the app", linking to /app. The map and the trees get the space back.

Two reasons this is a continuation rather than a reversal, and one cost worth naming.

It is line 10 of this document finally applied: **web reads, app walks.** Routes are navigation, navigation is what an app is for, and giving the web a half version of it was always the odd part. And it turns the deepest filter on the page into the one honest reason to want the app, which is the only app hook the site has ever had that is a feature rather than a promise.

The cost: walking is one of the four verbs, and the web now delivers three of them. The pill has to carry that weight, so it says where the routes are instead of implying they are here. Worth watching in the funnel; `data-ev="walks-app"` is the event.

**Nothing is deleted.** Hidde, same day: "de functie hebben we later dus wel nog nodig voor app dus gooi de info niet weg." `site/src/lib/walks.ts`, `data/walk-routes.json`, `scripts/route_walks.py` and `scripts/walk_planning.py` all stay, with a note at the top of walks.ts saying why, so no future tidy-up reads them as dead code.

## The superseded ruling: walks live INSIDE the city page. Hidde, 2026-08-06

Kept because its two constraints still bind whenever walks come back, on any surface: no walk URLs, and no walk may hide a tree from a crawler.


His words, and they are a standing no rather than a preference: "I'm not asking for extra pages. I never want extra pages for extra walks." A walk is **a feature within the city page, never a page of its own.**

What he does want, in his own framing: a city like Rome has its overview page and its trees, and from that one page you can pick one of perhaps three suggested walks and focus on it. So a city with many trees offers several walks, the visitor chooses one, and the page narrows to it. The trees are the permanent thing; a walk is a way of reading them.

Three consequences that settle questions this project kept reopening:

- **No walk contract in SEO_GEO_BLUEPRINT.md, and no walk URLs.** The blueprint work that a routes feature seemed to require does not exist, because there is no new page type. This is the cheap path, not the compromise: it needs Hidde's approval for nothing (hard rule 7 is about new page types) and it creates no indexed URLs to regret (hard rule 3).
- **Selecting a walk must not cost the page its SEO.** The city page is the indexed asset and every tree has to stay in the served HTML. So a walk selector filters or highlights what is already on the page; it never replaces the tree list with a fetched subset, and it never hides trees from a crawler.
- **The clustering is already done and is not a research job.** Measured 2026-08-06 across the published set: Porto is a single walk of all 17 trees across 1.6 km, Barcelona is two clean walks (10 across 0.8 km, then 8), Rome is 7 across 1.0 km plus a second of 4, Padua is 8 across 0.6 km. `scripts/cluster_register.py` and the same single-link method produce these from coordinates alone, so what a walk needs is a name, an order and a distance, not a research pass.

The tree-first versus walk-first question in BACKLOG.md is unaffected: this ruling says where a walk lives, not whether the tree or the walk is the hero.

## The five deliberate deviations from AllTrails (Hidde asked "wijk ergens af?", 2026-07-28)

Everything else copies wholesale. These five do not: (1) URL structure stays our flat /city/tree, never their deep /trail/country/region path: ours is indexed, short and irreversible territory. (2) No Shop item until there is something to sell (the keepsake, someday). (3) No star ratings ever: their soul is volume-plus-reviews, ours is ten-that-all-deserve-it; our future signal is the binary worth-it tap. (4) No user route planner: our walks are curated. (5) The species layer stays: an axis AllTrails does not have, our PictureThis side.

## Phasing

- **Phase A, now (session work, needs Hidde's eyes):** nav switches to verbs with the Explore dropdown; homepage city grid compresses into the directory block; tree pages move actions above the story and gain the nearby-trees footer. No URL changes, no new features, pure re-emphasis.
- **Phase B, when accounts open publicly:** My trees in the nav, collect buttons as signup hooks everywhere, the localized hook on the homepage ("N remarkable trees around [city], free account to collect them").
- **Phase C, app era:** "Start the walk" handoff per page, paid convenience layer with contextual prompts (offline city packs, season alerts, GPX-to-watch), pricing page only when there is a price, which is Hidde's alone.

The tree-first versus walk-first question stays open (BACKLOG.md, checkpoint mid-September); this IA embodies the working hypothesis by making the tree the hero object and the walk the first-class button beside it, which survives either answer.
