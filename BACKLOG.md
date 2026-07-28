# Backlog

Things worth building, deliberately not being built yet. Each has a **trigger**: the thing that has to be true before starting. Without a trigger an item is just a wish, and wishes accumulate until they crowd out the work that matters.

A run may pick up an item on its own once the trigger has fired, unless the item says it needs Hidde.

---

## The open product question: tree-first or walk-first (Hidde, 2026-07-28)

His framing, verbatim in spirit: AllTrails is clear, you go hiking and need a route; we hang between "you go for a walk with trees on it" and "you visit ten trees". A possible fork: not the ten most epic trees but the ten most walkable, but then we become a walking app, not a tree app. He does not have the answer, wants it parked, wants findings gathered slowly, leans toward staying open.

**Working hypothesis, now owner-endorsed (Hidde, same day, after the benchmark synthesis: "ziel bomen, product namaken AllTrails, wandelroutes als extra maar niet als basis"): wow-first selection, walk-first packaging.** The checkpoint below stays, to confirm with field evidence rather than to reopen from scratch. The tree is the product, the walk is the delivery. Walkability ranks CITIES for trips (his earlier ruling) and shapes routes, but never demotes an epic tree from its city's ten; the unwalkable epic gets the "worth the detour" label instead. The one door not to close while open: never replace "the ten most remarkable" with "the ten most walkable" as the selection rule without evidence.

**The evidence streams that will settle it, each already flowing or scheduled:**
1. **Search demand** (flowing): do people arrive on tree queries or walk queries? The demand scans already lean tree-first (tree queries are a vacuum, walk queries are institutionally owned); DATA.md's query lists keep scoring this daily.
2. **On-page behaviour** (flowing, beacon): per-tree directions clicks versus walk-panel engagement and GPX downloads. Runs can add path-level counts to the digest once volume exists.
3. **The founder field test (scheduled, the decisive one): Hidde's Japan trip, 2026-09-05.** Does he actually walk the chains, or cherry-pick single trees? His felt experience plus his check-in pattern is the richest single data point this project will get this year.
4. **Worth-signal** (future, flywheel): "was the visit worth it" per tree versus completed walks, once the tap exists.
5. **The top-10 trips collection** (soon): if trip pages outperform city pages on engagement, walk-weight rises.

**Checkpoint: mid-September 2026, right after the Japan trip.** A session with Hidde reads streams 1-5 and either settles the question or explicitly extends the open state. Runs: gather, never decide this one.

## A nicer sign-in email (Hidde, 2026-07-28, explicitly not important now)

The magic-link mail is currently Supabase's plain default template from their default sender. Fine for the quiet launch; his words: "voor nu niet belangrijk". When it matters: restyle the template in the brand voice and identity (Supabase dashboard, Authentication > Email Templates: subject plus HTML, a session job with Hidde logged in), and optionally send from an @ancienttrees.app address, which additionally needs SMTP config and remains his infrastructure call.

**Trigger:** before the login ever links publicly (natural moment: the same session that builds the delete function), or earlier if Hidde asks.

## The flywheel: users strengthen the content, designed 2026-07-27 with Hidde

The moat that compounds daily: content can be copied, field signal cannot. Six signal types, his four plus the two the design surfaced: proof-of-life ("the tree still stands", our defence against the staleness that will otherwise rot 328 trees), worth-signal ("was the visit worth it"), corrections and suggestions (both live), **user photos** (the strongest one: the person who just checked in is standing at our biggest content gap with a camera; needs a clean licence grant and credit), and **season ground-truth** ("the ginkgo is turning NOW", which upgrades the radar from forecast to live report).

The carrier is the post-check-in moment, in the app: location-verified, one screen, three taps (worth it? standing well? share a photo?). Verified presence is also the trust model: only people who provably stood there feed the worth-signal.

Scale-honesty, why this works at five visitors a day: classic flywheels need mass, ours does not, because the night runs make every single signal valuable at n=1. One report is a research lead, verified against sources the same night. Phase one (now): signals as leads, machine as the processing plant. Phase two (app plus accounts): volume, thresholds, weights.

The self-improving selection: every tree quietly accrues a field record (visits, worth-votes, condition pings). Ten stays ten, but persistent underperformers go to the bench: a run researches a replacement from the lead lists and swaps, with an honest note. One guard rail that is design law: votes inform, runs decide with context. A quiet cloister tree with few votes is not a bad tree, and mass taste must never vote away calm beauty in favour of instagram trees.

Build order when the time comes: 1. the worth-it tap after web check-in (tiny, starts harvesting early); 2. the user-photo path with licence grant (attacks our weakest number directly); 3. the condition ping; 4. live season pings in the app.

**Trigger:** items 1 to 3 buildable on web whenever Hidde says go; item 4 is the app. **Needs Hidde:** the licence text for user photos carries his project's name.

## Top city trips and signature walks (Hidde's direction, 2026-07-27)

Hidde, in session, partially unparking the themed-route idea below. His words, condensed: an **"Ancient Trees top 10" of the best tree city trips** (his gut list: Palermo, Cadiz, Lisbon), and **properly curated, genuinely attractive walking routes** in a handful of prime cities. The model he sketched matches the flywheel above: every big city set up by AI, strengthened by user signals, in a pleasantly walkable map; on top of that a thin, opinionated curated layer. Lists with an opinion are the acquisition surface.

Two build shapes, both his to green-light per piece:

1. **The flagship list: "The 10 best tree city trips"** as a collection-style page (Contract D machinery, research standard, editorial framing per hard rule 8: "our ten favourites", never unverifiable superlatives). Requires verifying anchor trees in cities not yet covered (Palermo's Piazza Marina ficus, Cadiz's Parque Genovés giants). Candidate pool beyond his three: Seville, Rome, Istanbul, Tokyo, Edinburgh, London, Amsterdam.
2. **One signature walk per prime city**: 60 to 90 minutes, 4 to 6 trees, named, with a real start, end and story arc. Explicitly NOT two-hour marathons; Hidde flagged those as too long. Builds on the existing per-city GPX.

**Trigger:** fired 2026-07-27, same session: Hidde said "run deze maar alvast, ik ben heel benieuwd naar deze lijsten". Research and drafting of the top-10 city trips list is a go; signature walks follow once the list settles which cities are prime.

Addendum, same session: Hidde also wants the user-generated counterpart, **a public list ranked by "deze boom was de trip waard" votes**. That is exactly the worth-signal (flywheel item 1 above), surfaced as a leaderboard. Honesty rule: this list only appears once real vote volume exists; never render a ranking on a handful of votes as if it were consensus, and never fake counts. Until then the worth-tap quietly collects.

## Parked ideas, brainstormed but not validated (2026-07-26)

From the functionality brainstorm, Hidde approved four verbs as the product (find, walk, collect, season; see CLAUDE.md). The rest of the list is parked here so it neither disappears nor sneaks into a build: themed cross-city route pages, personal records ("the oldest tree you ever stood at"), audio stories at the trunk, the multi-day trip planner. "Die andere weet ik niet," and unknown means not built.

**Trigger:** Hidde explicitly asking for one of them. Nothing else.

## Gamification: points, badges, rarity (the app's collecting core)

Hidde's direction, 2026-07-26, replacing photo-led presentation as the emotional engine: the photos of old trees are honestly often ugly, the game is not. Sketch to build on when the app lands:

- **The currency question, settled by research 2026-07-26: real stats beat points, and our points become YEARS.** The evidence: naked points are the weakest mechanic and can undermine intrinsic motivation in an already-passionate audience (SDT: extrinsic rewards crowding out intrinsic joy), while quantified-self stats are exactly what mastery-oriented hobbyists value most. Every product our audience already loves proves it: Strava runs on personal stats and records, not points; Polarsteps counts countries and percent-of-world; eBird runs birding, the closest cousin of tree collecting, on life lists and counts. None of them award a single point.
  So Ancient Trees keeps no abstract currency. The score is a real quantity: **years**. Stand before the 750-year Zenpukuji ginkgo and your collection grows by 750 years; the headline stat reads "you have stood before 4,850 years of living history." Unfakeable, self-explanatory, automatically rarity-weighted (a millennium tree is a massive day), and it speaks the brand's own word: ancient.
  The engagement hierarchy, in order: 1. the collection itself (the finite sets, x of 10 per city, the Pokedex pull); 2. real stats (trees, cities, species, years, your oldest); 3. badges as milestones (the pyramid below); 4. no points anywhere; 5. no leaderboards, since competition research shows it shifts joy toward validation-seeking, the opposite of a good afternoon outside.
- **Badges as a difficulty pyramid, revised 2026-07-26 after gamification research.** The field's completion-rate targets: common badges for nearly everyone, uncommon for 25 to 50 percent, rare for under 10, and summit badges for under 5 percent, earned over months. Hidde spotted this independently: "wie ziet nou alle eiken van de wereld" is exactly right, and the answer is that summit badges are SUPPOSED to be near-unreachable, celebrated hard, never early filler.
  - Common, day one: "First tree" (the first check-in; endowed-progress effect, give the head start immediately).
  - Uncommon, a good weekend: "City complete", named per city ("Amsterdam complete", 4 to 10 trees); "First prime" (a check-in inside a tree's best_time window).
  - Rare, under 10 percent: "Millennium" (stood at a 1000-plus-year tree); "Four seasons" (Hidde's ring completed on one tree, a full year of returning); "Country collector" (three cities complete in one country).
  - Summit, under 5 percent, shown with rarity percentages and celebrated loudest: a cross-city collection completed ("Every ancient oak of Europe"). Expedition badges, deliberately near-mythical.
  - Field warnings adopted: no badge inflation (nothing for logging in or streaks), badges recognise meaningful moments rather than repetition, rarity indicators visible, and the biggest celebrations reserved for the rarest moments. Our audience is intrinsically motivated already, so badges recognise the love, they never replace it.
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

Hidde's read 2026-07-26: collections may be the best SEO value per page, and they are nearly free, since a new collection recombines already-researched trees. First two (ancient oaks, November ginkgos) live since 2026-07-27. Since blueprint v1.3 they publish without owner approval, under the research standard with script-checked entries.

**Trigger:** none; the slate lives in PRODUCT_TODO.md.

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
