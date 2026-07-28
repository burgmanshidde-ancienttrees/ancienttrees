# Competitive analysis

Researched 2026-07-21. The question: what can we learn functionally, and who could actually hurt us.

## The landscape

Five categories touch the product. Figures are from public sources, 2025.

| Player | What they are | Scale / model | Overlaps us on |
|---|---|---|---|
| MonumentalTrees | tree database | completeness, no curation | content (trees) |
| Woodland Trust / national registers | conservation databases | deliberately hide locations | SEO, not product |
| PictureThis | plant ID app | 1M+ reviews, $29.99/yr subscription | seasonality, plant data, price |
| AllTrails | hiking app | 70M registered, 2.1M paid, $73M revenue | routes, offline, business model |
| Atlas Obscura | curated curious places | profitable, "Been There" tracking | curation and collecting |
| Seek / iNaturalist | nature collecting | gamified, "real-life Pokemon Go" | the collection mechanic |

**The MonumentalTrees statement, as Hidde put it 2026-07-28, replacing the untested "using it is miserable":** no iOS app and a very dated UX, which is where we can beat them; and zero curation, which cuts both ways: it makes them the complete reference (a real strength) and overwhelming for a visitor who just wants a good afternoon (our opening). Their completeness plus our curation is the honest framing, not their inferiority.

**Nobody occupies our exact spot.** Each has one axis. PictureThis has plant data but no destination. AllTrails has routes but the tree is a waypoint, never the goal. Atlas Obscura has curation and collecting but across all curious places, trees are a fraction. Seek gamifies identification, not a curated walk. The intersection (curated + story + destination + collectible, for trees) is genuinely empty.

## What we can learn, functionally

- **AllTrails validates the paywall line at scale.** Discovery and content free; offline maps and navigation paid, at ~$36/yr, 2.1M paying. People pay for outdoor utility, not for content. This is exactly Hidde's instinct: routes and offline behind the line, trees free.
- **Atlas Obscura shows two things.** Their "Been There" tracking is our passport, working, at a profitable company. And their revenue is not subscriptions but tourism boards (DMOs), experiences and books. That is a path to money without a paywall or accounts, which fits our hard rules better than a subscription. A tourism board paying to feature its city's trees breaks no rule.
- **PictureThis validates the price** ($29.99/yr for plant content) but is heavily criticised for an aggressive paywall. That is where our "sympathetic project, by tree lovers" framing becomes a weapon: we can be what they are not.
- **Seek shows the collection mechanic gets people outside**, confirming the passport as activation, but over-gamification reads as shallow. Keep it tasteful, not Pokemon Go.

## Threats, ranked by who could cheaply take our space

1. **PictureThis, scariest on paper.** Tens of millions of users, already has plant data and the seasonal feature (we copied theirs), already monetised at our price point. If they added "remarkable trees near you, collect them," they would out-distribute us overnight. What saves us: their DNA is "identify the plant in front of you," not "walk to a landmark." A pivot is possible but off-strategy for them.
2. **Atlas Obscura, closest conceptually.** Has curation, collecting, distribution and a working revenue model. A "remarkable trees" vertical would be theirs. What saves us: trees are a fraction of their scope; they will not go deep.
3. **Google Maps, the sleeper.** Low probability, catastrophic impact. If Google ever surfaced "notable trees" as a category, default distribution wins instantly. Too niche for them to bother, but terminal if it happened.
4. **AllTrails, least likely.** For them the trail is the product, not the tree. A tree walk is adjacent but not their frame.

## The real threat, and why it validates the goal

The biggest threat is not a company. It is that we have no distribution and a well-resourced neighbour could out-distribute us overnight if they cared. The only defence is depth, quality and voice they will not bother to match.

That is exactly why Hidde's own goal is right. If this were a 90-million-user market, PictureThis or Google would come and we would lose. The niche has to be too small to wake the giant. Ten thousand enthusiasts is not just modest, it is defensible. That is the strategic reason under the instinct.

## Implications

- The route/offline paywall is validated (AllTrails). Keep building toward it, price it never (hard rule 2).
- DMO/tourism-board sponsorship is a real revenue path that needs no accounts and no paywall. Worth remembering when the traffic question is answered. On the backlog with the sponsorship item.
- Our moat is curation, story, beauty and honesty, not coverage. Every competitive move should deepen that, not chase breadth that invites a giant.

## Homepage, UX and funnel teardown: AllTrails and Polarsteps

Researched 2026-07-24 at Hidde's request, to learn how the closest comparable products present themselves. Both turned out to validate the find/walk/collect homepage direction and, more importantly, to point at a revenue path that fits our constraints.

### AllTrails homepage (web-first, our closest structural model)

- Hero is search-first, not signup-first: headline "Find your next adventure" over a search bar. The primary action is to search nearby, exactly the "Find trees near me" hero we mocked up.
- Three capability sections in sequence: activity recording, offline maps, custom routes. The three-act structure is the proven pattern; ours (find, walk, collect) is the same shape.
- A large "Adventure anywhere" directory of 100+ cities and 80+ parks. It builds trust through breadth and doubles as SEO. Our city grid is the same move; lean into it.
- Soft paywall: content is free, no hard block. AllTrails+ sells utility (offline maps, print maps, route tools). This validates the route/offline paywall instinct a third time.

### Polarsteps homepage (app-first, but the model is the lesson)

- Core loop is Plan, Track, Relive. Almost identical to find, walk, collect. Reinforces the structure.
- Revenue, and this is the finding: the biggest earner is not the subscription, it is a physical Travel Book, a printed keepsake of the trip you collected, at 36 to 150 euro. A light Plus subscription (nicer maps, stats) and affiliate booking sit alongside. Privacy-first, no ads, no data sale, grown from its own revenue.
- Named testimonials and a 4.8 from 370K ratings carry the page. We have none of that and must not fake it.

### What transfers, and what does not

Adopt:
- The search-first hero: "Find trees near me" as the primary action, web-first like AllTrails, not an app download like Polarsteps (we have no app).
- The three-act structure, find, walk, collect, now double-validated.
- The directory as honest trust and SEO: "12 cities mapped, 88 to go" instead of fake social proof.
- Privacy-first as a stated selling point: no accounts, no ads, no trackers. It differentiates us from PictureThis and matches our honesty positioning. Polarsteps proves it is a feature worth saying out loud.
- The soft paywall on utility, never on content: the AllTrails model, which we already favour.

Reject:
- Fake or borrowed social proof. No 20M users, no 4.8 from hundreds of thousands. Honesty is the whole brand.
- The app-download CTA. We are web-first by strategy.

### The strategic finding: the passport is our "relive," and it can be sold

Polarsteps monetises the reliving, not the tracking: it sells a beautiful artifact of the collection you built. Our "collect" (the passport) is exactly that same reliving stage. Someone who has ticked off forty trees across five countries has built something they might pay to keep: a printed map or small book of their tree year, a "tree passport" as an object.

Why this matters: it is a revenue path that needs no paywall on content, no subscription to administer, and it fits the sympathetic brand. It still eventually needs accounts, to persist a collection worth printing, which is the destination already recorded in CLAUDE.md. But it reframes why accounts exist: not to gate the trees, but to enable a keepsake people actually want. It sits alongside the DMO-sponsorship path from the earlier analysis as the two revenue routes that do not require becoming a subscription business.
