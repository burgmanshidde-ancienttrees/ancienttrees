# Backlog

Things worth building, deliberately not being built yet. Each has a **trigger**: the thing that has to be true before starting. Without a trigger an item is just a wish, and wishes accumulate until they crowd out the work that matters.

A run may pick up an item on its own once the trigger has fired, unless the item says it needs Hidde.

---

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

## Illustrated map pins

Painterly per-species icons instead of the current shared silhouettes. Six of Lisbon's ten trees still share one broadleaf shape.

**Needs Hidde:** yes, it is taste work and he asked to do it together.
