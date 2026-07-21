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

## The two-tier data model

Split the map into a cheap data tier (every tree we can place from open data, hundreds per city) and a story tier (the ten or so per city that get research, verification, a written story and a photo). This is what lets the ten-per-city limit rise without the story workload rising with it, and it is the only route to world coverage that arithmetic supports.

**Trigger:** finish `OPEN_DATA_SURVEY.md` first. Five cities were measured and five timed out, and the national registers have not been checked at all. Then decide the schema, because schema changes get expensive once fifty cities are in.

## Seasonality: when is this tree at its best

Bloom, autumn colour, the month a tree is worth the trip. Nobody else publishes this, it comes almost free alongside research already being done, and it is the strongest known fix for the gap between reading about a tree indoors and actually going.

**Trigger:** none needed beyond a run having room. Good candidate for improvement mode.

## Telling submitters what happened to their tree

Someone submits a tree and then hears nothing, because nobody may write to them as Hidde (hard list 4). Three weeks later it looks like it fell into a hole, and that is the person we can least afford to lose. A public page showing what happened to submissions, with credit where a name was given, would close the loop and prove the "by tree lovers, for tree lovers" claim rather than asserting it.

**Trigger:** the first real submission arriving.

## Illustrated map pins

Painterly per-species icons instead of the current shared silhouettes. Six of Lisbon's ten trees still share one broadleaf shape.

**Needs Hidde:** yes, it is taste work and he asked to do it together.
