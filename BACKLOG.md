# Backlog

Things worth building, deliberately not being built yet. Each has a **trigger**: the thing that has to be true before starting. Without a trigger an item is just a wish, and wishes accumulate until they crowd out the work that matters.

A run may pick up an item on its own once the trigger has fired, unless the item says it needs Hidde.

---

## Gamification: points, badges, rarity (the app's collecting core)

Hidde's direction, 2026-07-26, replacing photo-led presentation as the emotional engine: the photos of old trees are honestly often ugly, the game is not. Sketch to build on when the app lands:

- **Points per tree, weighted by rarity and age.** A neighbourhood plane is 10 points; a 2000-year yew is 500. The weighting already half-exists in the data (age_min/age_max, flagged uniqueness).
- **Badges for completable sets:** a city complete ("Amsterdam 10/10"), a country complete, themed sets across cities ("the three oldest oaks of the world", "every ginkgo worth a November trip"). Collections thereby become playable content, not just SEO pages.
- **Season multipliers:** checking in during a tree's best_time window is worth more, which points the game at exactly the moment worth going.
- **Seasonal badge variants (Hidde, 2026-07-26):** the badge you earn at a tree takes the colour of the season you stood there, so one tree is four collectibles and a reason to come back in another season. Works for every tree, evergreen or not: the visit has a season even when the peak does not.
- **Prime bonus:** checking in inside a tree's best_time window scores extra. Measured spread says this works year-round, not just spring: Nov 23 trees, Oct 9, May 8, Aug 8 (catkins), Apr 7, Jul 6, even Jan/Feb 3, with only Sep/Dec/Mar thin. Peaks rotate every few weeks, and a real prime lasts roughly ten days (blossom) to a month (autumn colour), which is exactly what makes a prime check-in scarce enough to reward.
- Tasteful, not Pokemon Go (PRINCIPLES.md): no streak punishment, no popups.

**Trigger:** the app project. **Needs Hidde:** the whole feel of it.

## Web check-in moves to the app; web becomes discovery plus sales floor

Hidde's call in principle, 2026-07-26: GPS check-in on a website feels half-app ("dat moet je voor de app maken"). Web keeps find (map, near me), the stories, walk (routes), suggest-a-tree and feedback; collecting becomes the app's reason to exist. Not yet executed: the counterpoint (check-in is our only pre-app collect-demand signal, and the August checkpoint reads it) is with him; awaiting his confirm on framing before code is removed. Until then PRODUCT_TODO item 1 stays superseded and nothing passport-related is built or removed.

## The next coverage wave: home-country density, not more world cities

Decided in discussion with Hidde 2026-07-26. When the depth phase completes and coverage reopens, the next wave is not the remaining world list but the Netherlands, dense: Utrecht, Rotterdam, Den Haag, Haarlem, Groningen, Leiden, Delft, Maastricht, Nijmegen, Breda and onward, so that a Dutch collector has a real collecting field at home.

The reasoning, so it does not have to be re-argued: world cities and collections serve the searcher (acquisition); home-country density serves the resident collector, who is the person that returns, collects for months and eventually pays (retention). Density needs no search volume because collectors arrive via the map, not Google, so small-city pages are for the collector's map, not for ranking. A licence correction from 2026-07-26 tempers the economics: the Bomenstichting register turned out to be CC-BY-NC (see OPEN_DATA_SURVEY.md), so it is a research lead list, never an import source for a commercial product. Confirmed pins come instead from municipal government open data (licences to be read per city) and our own two-source verification. Hidde can verify in person, and the collector logic stands unchanged.

**Trigger:** depth phase done (Amsterdam flawless, lead-group cities at the photo floor with pins resolved), and Hidde reopening coverage (ladder rung 6).

**Needs Hidde:** only the reopen decision. Research is runs' work, and the register licence check must happen before any import (see OPEN_DATA_SURVEY.md).

## More collections from existing data

Hidde's read 2026-07-26: collections may be the best SEO value per page, and they are nearly free now, since a new collection recombines the 328 trees already researched, zero new research. Candidates: oldest oaks of Europe, ginkgos worth a November trip, trees older than the city around them, wisteria and blossom trees for spring. Runs may draft them (status needs_curation); per Contract D nothing publishes without Hidde's approval.

**Trigger:** none for drafting; Hidde's approval per draft for publishing.

## Let runs read the visitor numbers

A run cannot currently see Cloudflare analytics: the numbers need Hidde's login, and reading them would mean putting a Cloudflare API token in the repo or the GitHub environment. That is a new secret that can leak and a new third-party dependency (hard rule 5), and it puts a first crack in the deliberate separation that keeps visitor and personal data on Hidde's side rather than a run's. Worth it later, not now: today the number is almost certainly zero, so a run would add a key and a dependency to read a nought.

Value when it fires: a run sees traffic starting for itself and can flag in LOG.md "real visitors now, time for the next step" instead of Hidde checking the dashboard by hand. That is the missing signal the whole project is waiting on.

**Trigger:** measurable traffic in Cloudflare, and Hidde not wanting to watch it by hand. Recorded 2026-07-21 at his request.

**Needs Hidde:** yes. It is his Cloudflare account and his call whether a run should hold a key to it.

## A keepsake of the collection, the Polarsteps move

From the homepage research (COMPETITION.md, 2026-07-24). Polarsteps earns most of its money not from a subscription but from a physical Travel Book, a printed keepsake of the trip you collected. Our passport is the same reliving stage: someone who has ticked off dozens of trees across countries has built something they might pay to keep, a printed map or small book of their tree year.

Why it fits: revenue without a paywall on content and without becoming a subscription business, aligned with the sympathetic brand. It sits alongside DMO sponsorship as a route that does not force us into the account-and-paywall model early.

**Trigger:** evidence that people actually build collections worth keeping, meaning the passport is being used across sessions and cities. Needs accounts to persist a collection worth printing, so it inherits the accounts trigger.

**Needs Hidde:** yes. Money, a print supplier, and accounts, all his.

## Sponsorship link

Deferred 2026-07-21 by Hidde: not important until there are visitors.

Somewhere for people who like the project to chip in. Ko-fi is the fastest to set up, GitHub Sponsors fits the "built in the open" framing better, Patreon is overkill for now. Donations rather than a paywall, so the content stays free and nobody holds a card number or a subscriber list.

**Already built:** `SUPPORT_URL` in `scripts/build_site.py`. Paste a URL in and the button appears on the homepage. Nothing else is needed in code.

**Trigger:** real visitors arriving, visible in Cloudflare analytics. Earning nothing from zero traffic tells us nothing and the button is just clutter.

**Needs Hidde:** yes. It is his money and his account (hard list 2). He creates the page, hands over the public URL, a run wires it in.

## Accounts, and a paywall on top

**Trigger:** evidence that people want this. Visitors returning, trees actually being ticked off, submissions arriving. See "Where this is going" in CLAUDE.md for the full reasoning, including why the passport cannot stay in LocalStorage forever.

**Needs Hidde:** yes, unavoidably. Server, database, personal data, privacy policy, his liability.

## The two-tier data model: rejected 2026-07-21, and why

A run proposed splitting the map into a cheap data tier (hundreds of trees per city from open data) and a story tier (the curated ten). Hidde rejected it the same day, and he was right, so this is recorded rather than deleted: the reasoning will come back around and should not have to be re-argued.

**Ten per city is not a limitation, it is the mechanism.** The passport only works against a finite set. Ten of ten in Tokyo is an achievement; four of two hundred and forty-seven is a rounding error, and nobody collects a rounding error. Adding a data tier would have quietly destroyed the feature that makes people come back, in exchange for a coverage number nobody was asking for.

It also protects the quality Hidde likes: at ten per city every tree gets two sources, a story and a photo. At two hundred, none of them do. MonumentalTrees already has everything and it is miserable to use. **The curation is the product**, and scarcity is what makes it one.

Do not reopen this on coverage arithmetic alone. Reopen it only if there is evidence that people want breadth more than a completable set.

## Open data as a research accelerator, not as content

The useful half of the rejected idea. OSM and the national registers become an input to research rather than something published: a pre-sorted candidate list with coordinates already placed by mappers who stood there. Cuts the two dullest steps of a city run (finding candidates, fixing coordinates) and improves pin precision at the same time. Nothing changes about what ships: still ten, still fully researched.

Second accelerator on the same theme: work a country's register out once and let every city in that country benefit, instead of rediscovering it per city.

Neither speeds up the part that actually takes the time, which is writing ten researched stories, and that part should not be sped up: it is what the site is for.

**Trigger:** finish `OPEN_DATA_SURVEY.md` first. Five cities measured, five timed out, national registers unchecked.

## Seasonality: when is this tree at its best

Bloom, autumn colour, the month a tree is worth the trip. Nobody else publishes this, it comes almost free alongside research already being done, and it is the strongest known fix for the gap between reading about a tree indoors and actually going.

**Trigger:** none needed beyond a run having room. Good candidate for improvement mode.

## Telling submitters what happened to their tree

Someone submits a tree and then hears nothing, because nobody may write to them as Hidde (hard list 4). Three weeks later it looks like it fell into a hole, and that is the person we can least afford to lose. A public page showing what happened to submissions, with credit where a name was given, would close the loop and prove the "by tree lovers, for tree lovers" claim rather than asserting it.

**Trigger:** the first real submission arriving.

## Logo and favicon: parked 2026-07-26 after a rejected first round

Three flat vector directions (tree rings, oak roundel, ginkgo leaf) were proposed and Hidde rejected all three: "ik vind de stijlen niks." The likely root cause is on record and should steer the next attempt: his stated art direction is painterly and illustrated, Polarsteps-like, not flat graphic marks. A next round starts from illustration, not geometry, and only when he asks for it.

## Illustrated map pins

Painterly per-species icons instead of the current shared silhouettes. Six of Lisbon's ten trees still share one broadleaf shape.

**Needs Hidde:** yes, it is taste work and he asked to do it together.
