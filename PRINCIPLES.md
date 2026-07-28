# Product principles

What we have learned from comparable products (AllTrails, Polarsteps, Strava, Atlas Obscura, PictureThis) and from established web practice, written down so every run and session applies the same thinking. Applied, not generic: each line says what it means for Ancient Trees.

## Lessons from the comparable products

1. **The core loop is a habit loop: trigger, action, reward, investment.** Our action is the check-in; the reward is a tree turning green and a story worth the walk; the investment is the collection that accumulates. The investment phase is the retention moat: the more someone has collected, the harder it is to leave. Surface progress everywhere, make each check-in feel like it adds up.

2. **The collection is the moat, so protect it.** A growing passport is switching cost. Keep it survivable (portable link, eventually accounts), never lose it, always show the running total across cities. This is why the passport is not a gimmick but the retention engine.

3. **Never reset progress punitively.** If completion or streaks are ever added, welcome people back rather than zeroing them, the way Calm and Apple Fitness do. A tree collection is naturally forgiving; keep it that way.

4. **First value must be frictionless: the aha moment fast, with the fewest clicks.** For us the aha is a genuinely remarkable tree the visitor did not know stood near them, or their first check-in. No signup wall stands in front of it; that is our deliberate bet, and the opposite (Polarsteps asks for an account first) is simply a different strategy, not a flaw (Hidde, 2026-07-28). Guard this: never put a gate before the first wow.

5. **Sharing is the growth-loop HYPOTHESIS, untested (labelled 2026-07-28).** Distribution is our weakest point and the owner will not post under his name; the hope is that users share their own collection, making a shareable "my trees" page word of mouth and an inbound link. Nobody has shared anything yet, so build the passport to be shareable, but do not stack further work on this loop as if it were proven; the flywheel's worth-signal will test it.

6. **Seasonality is the re-engagement trigger.** "At its best right now" and, later, "trees at their best near you this week" are the internal triggers that bring people back, the way AllTrails uses recaps. The season feature is not decoration; it is the reason to return.

7. **Privacy is a feature worth saying out loud, but say the right one.** Corrected 2026-07-27 after actually reading Polarsteps' privacy policy: Polarsteps runs cookies AND Mixpanel analytics; its real promise is no ads, no ad-tracking, no data sale. For us that is the internal default (hard rule 5), NOT a public forever-promise: Hidde ruled 2026-07-28 that public copy stays boring-standard and keeps every future option his. He chose cookieless visit counting the day before. The earlier version of this principle ("no trackers, cookieless, say it on the homepage") was an assumption copied from a teardown without verification, exactly the failure mode to watch for: never harden a competitor observation into our own promise without reading the source.

8. **Money without a content paywall: two proven routes.** Utility behind a soft paywall (AllTrails: offline, routes) and a keepsake of the collection (Polarsteps: the physical book). Both let the content stay free and indexable. Neither forces us to become a subscription business early. See COMPETITION.md.

9. **Breadth is honest trust.** AllTrails' city and park directory builds credibility by its size and doubles as SEO. Our city grid does the same. Lean into "cities mapped, more to go" instead of social proof we cannot fake.

## General web practice we hold to

1. **Show, do not tell.** We can, because the product is the value. Use the real map, a real tree, the real season chart in the hero, not claims. SaaS sells a promise; we show the thing.

2. **One primary action per screen.** The homepage hero has one: find trees near me. Everything else is secondary.

3. **Empty states teach.** A 0 of 10 passport should invite the first check-in, not look broken. Every zero state is an instruction, not a dead end.

4. **Mobile-first, and performance is UX, and it is a CHECK, not a mood (sharpened 2026-07-28 after Hidde caught a desktop-only nav ship).** Our visitor is outdoors on a phone, maybe on 3G in a park. Static HTML, light pages, images that load. A slow page in a park is a lost walk. The rule with teeth: NO visual or template change ships without being looked at, in the same pass, at phone width (375px). Desktop-only shipping is the same failure mode as machine-logic copy: it passes every contract and fails the actual person, and it must be caught by us, never by Hidde.

5. **Programmatic SEO quality rules, because search is our only channel.** Every page must exist for a real reason and carry unique, substantive content, never fill-in-the-city-name templating (blueprint P3). Internal links by relevance, not everywhere. Quality over quantity: a few excellent pages beat many thin ones, which is the same logic as ten curated trees per city and the lead-group focus. Publish a little, measure, then scale, the canary-batch pattern, which is exactly the reference-city approach in GO_TO_MARKET.md.

6. **Progressive disclosure.** Lead with the one thing that matters, reveal depth on demand. A tree page opens with the story and the walk, not a wall of fields.

7. **Convention over invention for solved UX (Hidde, 2026-07-26).** Login, onboarding, forms, sharing, settings, empty states: these are solved problems with conventions users already know from the big apps. Research the leading pattern first, then build exactly that in our skin. The novelty budget is spent on the content, the game and the voice, never on plumbing UX: a surprising sign-in flow is a bug, not a feature.

8. **Trust through honesty is the moat.** Every honest label (an approximate pin that says so, "not finished yet") is a deposit in the one account competitors cannot copy. Never trade it for polish or growth.

9. **Written for a human first; the machine reads over their shoulder (Hidde, 2026-07-28).** The canonical failure: a city page footer listing all 33 cities as "Ancient trees in Lisbon · Ancient trees in London · Ancient trees in...": loop-generated anchor text, written for Google, absurd to any human reading it. Hidde found it, not us, and that is the part that must not repeat. The test, applied to EVERY generated block before it ships: read it as a stranger encountering it cold. If a phrase repeats because a loop wrote it, if a label exists for a crawler rather than the reader, if the wording only makes sense knowing the template behind it, rewrite. The pattern that resolves the tension: the SEO phrase lives ONCE in the heading or context sentence, and the repeated elements underneath read like language (bare city names, bare tree names). Search engines read context; humans read lists. Any block generated in a loop is guilty until read aloud.

10. **The owner stays as private as the law allows, until he says otherwise (Hidde, 2026-07-28).** No personal name, no personal location ("run from the Netherlands" level detail included), no personal email, no photo, no social links, anywhere public: site copy, schema, privacy page, commit identities, artifacts. Contact runs through brand addresses (info@ancienttrees.app). Where a rule or best practice wants a named person (GDPR controller, SEO entity trust), we take the honest cost of the anonymous option and record it rather than leaking identity. Only Hidde reopens this, explicitly.

## How to use this

When building or judging anything user-facing, check it against these. If a change strengthens the habit loop, the aha moment, shareability, honesty or findability, it serves the goals. If it adds friction before first value, fakes trust, or chases breadth that dilutes quality, it does not.
