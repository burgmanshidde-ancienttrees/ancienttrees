# Ancient Trees — Project Instructions

## What this project is

Ancient Trees is a discovery platform that maps the most remarkable ancient trees of the world's great cities, up to ten per city and never padded. The owner is Hidde, a designer and tree enthusiast based in the Netherlands. The system researches, verifies and publishes; readers correct. Hidde sets direction, he is not the quality gate.

The end product: a website (ancienttrees.app) with an interactive map and one SEO page per city ("10 Most Beautiful Ancient Trees in [City]"), later followed by an iOS app with a freemium model. (The specific line once written here, 2 trees free per city at €19,99/year, is NOT settled: see "The interim paywall line is still undecided" below, which explicitly supersedes it. No number in this file is a pricing decision; pricing is hard rule 2, Hidde only.)

## The value proposition

This is the core, and everything else serves it. Written 2026-07-24 by Hidde because the proposition had been drifting toward SEO and coverage, which are how people arrive, not why they stay. When anything here conflicts with an SEO or coverage instinct elsewhere, this wins.

**Ancient Trees is for people who love being outdoors and love trees.** The promise is simple: wherever you are, it shows you the remarkable old trees near you, gives you a short walk that strings a few together and tells you why each is worth seeing, and lets you collect the ones you have stood in front of. The feeling it sells is a good afternoon outside, looking up at something epic and old.

The one-sentence north star: *I am somewhere, I open it, it knows where I am, it shows me a cool tree nearby and a walk past a few, tells me why they are special, and I tick off the ones I visit.*

**The product is four verbs, settled with Hidde on 2026-07-26: find, walk, collect, season.** Find cool trees near you; walk a route past them; collect them with badges and points as the game; see them at their best with the season radar. Features outside these four (trip planners, audio guides, personal records, standalone themed routes) are parked ideas, not the product, and are not built without his explicit yes.

What this means for how we build:
- **The map and "trees near me" are the product.** They lead everywhere, the homepage first.
- **Cities, species and collections are acquisition, not the point.** They are SEO landing pages that bring people in from search. Keep them, they work, but they are the front door, not the house. On the homepage they sit below the value proposition, never in place of it.
- **Collections stay** (for example "the ten most remarkable trees of Europe"). A real SEO strategy, kept and on the backlog as such, secondary to the core. Not to be deleted.
- **The destination is: see the trees around you, walk them, collect them.** Accounts and an app are the vehicle. On 2026-07-26 Hidde opened the account track early, deliberately: build the app's collect-and-account backend now and wear it on the web, so the thinking and infrastructure exist before iOS and the site gains a real sign-in. Conditions before anything stores a user: a Supabase project on Hidde's own account, and a privacy page carrying his name. Until both exist, the login ships as an unlinked prototype.
- **Nothing is premium for now, but premium is the destination, and copy must never promise otherwise.** "Free today" is a growth tactic while we win users; the recorded end state is an account base with a premium tier and eventually an app (see "Where this is going"). So the site never says "free forever", "no accounts" or "always" anything: it simply does not gate today. Claims that survive the paywall (every tree free to explore, no ads, no tracking) are fine; claims the paywall would break are not. This distinction exists because a run once turned the sequencing into identity copy, and Hidde caught it.

When a page, a feature or a line of copy does not serve "have a good afternoon outside seeing epic trees near you," it is decoration or acquisition, and it must not crowd out the core.

## Repository structure

```
/data/cities/          — one JSON file per city (see schema below)
/data/collections/     — one JSON file per collection page (hand-curated, Contract D)
/data/species/         — one JSON file per species page intro (hand-written, gates Contract F)
/data/city-list.json   — the prioritized list of 100 cities with status
/site/                 — static site generator (Astro or similar)
/scripts/              — automation scripts
/CURATION.md           — log of what could not be verified, and notes worth keeping. Not a to-do list for Hidde.
/SEO_GEO_BLUEPRINT.md  — page contracts (titles, schema, internal links, content minima). No page ships without conforming to it.
/TONE_OF_VOICE.md      — the voice for all stories and page copy. Paris is the calibration standard.
/LOG.md                — what each autonomous run did. Hidde's catch-up file.
```

## The tree data schema

Every city file follows this exact structure (see data/cities/london.json for the reference example):

```json
{
  "city": "London",
  "country": "United Kingdom",
  "status": "needs_curation | curated | published",
  "trees": [
    {
      "id": "lon_001",
      "name": "The Totteridge Yew",
      "species": "European Yew (Taxus baccata)",
      "age_estimate": "2000 years",
      "age_min": 1000,
      "age_max": 2000,
      "location": {
        "address": "...",
        "latitude": 51.6323,
        "longitude": -0.2002,
        "neighbourhood": "..."
      },
      "story": "150-250 words. Specific, historical, vivid. No filler.",
      "verified_sources": ["url1", "url2"],
      "access": "Free / paid entry / restricted",
      "transport": "Nearest station + walk time",
      "photo": {
        "url": null,
        "license": null,
        "attribution": null,
        "status": "missing | found_needs_check | approved"
      },
      "curation_status": "ai_generated | hidde_approved | flagged",
      "location_precision": "confirmed | approximate"
    }
  ]
}
```

## The research workflow (autonomous run)

Runs hourly around the clock via GitHub Actions. Most attempts hit the Claude usage limit and stop immediately, which is expected and costs almost nothing; the work goes through whenever the window has room.

Each run, do exactly this, in order:

### Step 0 — Read state and pick the work

Read `/data/city-list.json` and the published city files, then take the first item on this ladder that applies. Do one thing per run and do it properly; a half-researched city is worse than none.

1. **Unprocessed submissions** (see Step 0b). Someone cared enough to send something, that outranks everything.
2. **The site is broken.** Build fails, a link is dead, a page violates a contract. Fix it before adding anything new.
3. **Something published is wrong**, as opposed to merely imprecise: a tree that has fallen, a pin in the wrong place, a fact that does not hold up. Wrong costs trust; vague does not, as long as it says so.
4. **A published city below the photo target of 8 of 10.** Decided by Hidde on 2026-07-22: photos are the priority, and 80 percent is the floor he wants. This ranks above adding a new city, because a photo is what makes someone want to walk there, and a page without one loses the click in search and cannot be shared at all. It is legitimate pre-demand work, unlike a precision gate, because being findable and shareable is exactly the Phase 0 job in GO_TO_MARKET.md. Work the focus region first (UK, Netherlands, then the rest of the lead group and the marquee European cities), oldest-first within that. Hunt hard and widely: Wikimedia, then iNaturalist, Flickr under CC, Openverse, the city or park authority, and reader submissions. Two honesty rules that never bend: never publish a photo without a verified open licence and attribution, and where 80 percent genuinely cannot be reached because no open photo of a tree exists, record that in CURATION.md and move on rather than looping on it forever. The target reprioritises the work; it is not a trap that blocks everything on one unphotographable tree.
5. **Depth work on the cities search already serves.** Resolve approximate pins and hunt photos, hardest-ranking cities first. As of the 2026-07-26 Search Console export that order is: Amsterdam (position 7.9, 7 vague pins), Lisbon (7.7), Istanbul (8.0), Rome (most impressions, 18), then the rest of the lead group and marquee Europe, oldest-first. Amsterdam is the reference city and goes to flawless first: 10 photos, 0 vague pins, seasonality where real.
6. **New cities: frozen until the depth exit test passes, then the Netherlands wave.** The exit test: the eight cities search already serves (Amsterdam, Lisbon, Istanbul, Rome, Tokyo, Paris, London, Barcelona) each at 8 or more photos and 2 or fewer approximate pins, Amsterdam at zero. Once that is true a run may reopen coverage by itself, in this order and with counts per the doctrine in Step 1: **first the Japan wave, decided by Hidde in session 2026-07-27** (Nara, Kamakura, Nikko, Osaka, Kanazawa, plus deepening Tokyo and Kyoto; grounds and the mandatory pre-wave demand scan in GO_TO_MARKET.md "The Japan wave"; anchor data source: the national and prefectural Natural Monument tree registers), then the UK dense (York, Bath, Oxford, Cambridge, Bristol, Glasgow, and further UK cities that clear the four-tree bar), then Ireland (Cork, Galway), then the remaining European traveler capitals (Budapest, Krakow, Copenhagen, Stockholm, Dubrovnik, Zurich and onward: travelers search in English everywhere, so tourist footfall times tree-oldness decides), then the Netherlands (Utrecht, Rotterdam, The Hague and onward: locals search in Dutch, so NL waits for Dutch pages or local seeding). Reversed from NL-first on 2026-07-26: with English-only pages and search-only distribution, language match decides. (An earlier version of this sentence also cited "the UK was our top Search Console country in week one" as evidence; struck 2026-07-27 at Hidde's volume-honesty ruling, that was noise-level data. The language-match argument stands on its own.) NL returns to the front the moment Hidde seeds locally or Dutch-language pages exist; Amsterdam stays the reference city regardless. Pins from municipal government open data where available, licence read first; the national NL register is CC-BY-NC and stays a lead list.

   **Standing exception, approved by Hidde in session on 2026-07-27: Palermo, Cadiz and Sintra may be researched and published as new city pages ahead of the exit test.** Scope is exactly these three, no others ride along, and the general freeze stays until the exit test passes. Reason: they complete the "Top 10 tree city trips of Europe" collection (see CURATION.md 2026-07-27 and BACKLOG.md), whose other seven cities are already live. For Sintra, Portugal's ICNF register (queryable endpoint noted in CURATION.md) supplies registered ages, girths and coordinates; the 800-year Quinta do Castanheiro sweet chestnut is excluded permanently (private land, mutilated Feb 2025). Each of the three still needs the full research standard, and their top-10 entries are only done when the walking route is plotted over real streets.
7. **Product work, when everything above is satisfied.** Draw the top unblocked item from `PRODUCT_TODO.md` and finish it completely. That lane exists because runs used to be allowed only to research trees while the product itself waited for a human session; Hidde closed that gap on 2026-07-26. Its rules live in the file and are strict, because a CI run cannot see the page it changes: reversible only, contracts must validate, every item verified by build output or grep rather than eyes, no visual-taste work and nothing from the hard list.

**Depth is the current phase, on evidence.** Coverage was the phase from 2026-07-21 (first versions of many cities beat polish on a few) and it did its job: 33 cities gave Google enough surface to start serving us. On 2026-07-26 the first Search Console export showed impressions doubling daily and city pages ranking on page one, which opened Phase 1 of GO_TO_MARKET.md. Phase 1 work follows the data: make the pages people actually land on deliver the promise, precise pins and photos first. Re-verify flagged items and check the news for fallen trees along the way.

This is only safe because of one thing, and it is not negotiable: **every tree ships with `location_precision` set honestly.** A pin that admits it is vague sends someone to the right park knowing they will have to look. A pin that fakes precision sends them to a spot where the tree is not, and that is the one mistake this project cannot afford. Precision is optional; honesty about precision is not. Never mark a pin confirmed to make a city look finished.

Append what you did to `LOG.md`, newest first, in the format that file describes.

### Step 1 — Research the city's trees (BE THOROUGH)
Search the web extensively for the city's most remarkable trees. Minimum research per city:
- Search "[city] oldest trees", "[city] remarkable trees", "[city] monumental trees", "[city] famous historic trees" — in English AND the local language
- Check municipal/government tree registries (many cities have official "great trees" lists)
- Check monumentaltrees.com for verification of age/location claims (NEVER copy their photos or text — verification only)
- Check Atlas Obscura, local history blogs, park authority websites
- A tree qualifies if it is: genuinely old OR visually spectacular OR historically significant, AND publicly accessible

**The count follows the trees. Decided by Hidde on 2026-07-26.** Ten is a cap, not a quota, and the cap never moves: a city with five hundred worthy candidates still ships exactly ten, because a finite, completable list is what makes collecting work (see BACKLOG.md on the rejected two-tier model). The doctrine bends the number downward only, never up. A capital with ten genuinely remarkable trees gets ten; a smaller city gets the five or eight that truly clear the bar; padding a list to reach ten is fabrication's polite cousin and forbidden (Verona shipping 8 was right). A place earns a page only when at least four trees survive verification; below that it gets no page yet, and its best tree can still appear in a collection. Exclusivity is the point: a collector wants every entry to deserve its spot, and a two-street village with one fine oak is a collection entry, not a city.

**An entry must be alive (Hidde, 2026-07-27: "we doen niet aan dode bomen").** The product is standing before something that has been alive for centuries; a carcass, stump or relic breaks that promise and makes the years-counter lie. A dead tree may appear inside a story as context, never as a collectible entry, however famous the remains (Queen Elizabeth's Oak in Greenwich and Vienna's Stock im Eisen both fail this test and are to be replaced; a fallen original honestly succeeded by a living replanting, like the Elm of Saint-Gervais, passes when the entry describes the living tree). Runs: sweep CURATION.md's 2026-07-27 dead-tree suspect list, verify each against sources, and replace confirmed dead entries with living trees researched to the normal standard, one city per pass, with an honest note. Replacements reuse the old id and the page must redirect or the old URL stay resolvable, per the Barcelona bcn_008 precedent.

**An entry must be a collectible point (Hidde, 2026-07-26).** One identifiable tree, or an ensemble only when the ensemble itself is the destination: compact, famous for being exactly that, with one obvious place to stand. The Lomanstraat tunnel and the Meiji Jingu Gaien avenue pass; a thousand ordinary planes along a kilometre of La Rambla do not, there is nothing to stand at and nothing to have seen. Barcelona's bcn_008 failed this test as "The Plane Trees of La Rambla" and was replaced on 2026-07-26 with a genuinely singular tree, the Silk Tree of the Ciutadella (same id, so no URL broke). Apply the test to every future ensemble candidate.

### Step 2 — Verify each tree
For each candidate tree, cross-reference at least 2 independent sources for:
- Existence and species
- Approximate age
- Exact location (GPS coordinates)
If sources conflict or only one source exists, include the tree but set `curation_status: "flagged"` with a note explaining the uncertainty.

### Step 3 — Write the stories
150-250 words per tree (the Paris run of 2026-07-15 sets the standard; anything over 250 words gets shortened). Style rules:
- Direct, specific, slightly vivid. Scott Galloway meets nature writing.
- Lead with the most surprising fact.
- Include what the tree has "witnessed" historically.
- Never use: "hidden gem", "must-see", "breathtaking", "nestled".
- Never use em dashes.

Stories and any page copy must satisfy SEO_GEO_BLUEPRINT.md — in particular P2 (answer first, in the first two sentences where the page is a question/city page) and P3 (unique content, no fill-in-the-city-name templating) — and follow TONE_OF_VOICE.md, including its calibration examples and hard bans.

**Set `best_time` when, and only when, a tree has a real seasonal peak.** This is the single strongest reason a page gives someone to actually go, because it turns "nice" into "this weekend". A tree with a pronounced moment gets:

```json
"best_time": { "months": [11], "label": "late November, when the ginkgo turns gold" }
```

`months` is the list of month numbers when it is at its best and drives the "at its best right now" badge; `label` is the short phrase a reader sees, in the tone of voice. Rules:
- Only add it when the moment is real and specific: blossom, autumn colour, a wingnut's summer catkins, a magnolia's ten days. An evergreen or an ancient yew that looks much the same all year gets no `best_time` at all. Forcing one on every tree is filler and defeats the point.
- Base it on the species and the local climate, and say what actually happens in the label, not just a month. "May, when it flowers" beats "May".
- Keep it honest: if a peak spans a range, use the real months. Guessing a precise week you cannot support is the same mistake as a fake pin.

### Step 4 — Find photos
Search Wikimedia Commons and other openly-licensed sources (CC0, CC-BY, CC-BY-SA only). Record the exact license and attribution. If no good photo exists, set photo status to `missing`. NEVER use photos from monumentaltrees.com, Google Maps, or any source without a clear open license.

**Do not stop at Wikimedia.** Coverage there varies by country rather than by tree, which is why Tokyo came in at 7 photos out of 10 and London at 0. Same trees, different places to look. When Wikimedia comes up empty, try in this order:
- **iNaturalist**, which often has CC-licensed photographs with coordinates attached, useful for confirming a pin as well as illustrating it. Check the individual observation's licence, it varies per photo.
- **Flickr**, filtered to CC licences. Old and well photographed trees are often there under CC-BY.
- **Openverse**, which searches many open repositories at once.
- **The city or park authority's own site**, where the licence is sometimes explicitly open.

A photo does more for goal 1 than any paragraph, because it is what makes someone decide the walk is worth it. Hunt hard, but per the MVP mindset, never hold a city back for one.

### Step 5 — Commit and update state
- Save the city JSON file
- Update city-list.json (status: pending → needs_curation)
- Append to CURATION.md: city name, date, number of trees, number flagged, photos missing
- Commit with message: "Add [city]: 10 trees, X flagged, Y photos missing"
- Rebuild the site so the new city page goes live. The generated pages (city, tree, question, collection) must conform to the Layer 2 contracts in SEO_GEO_BLUEPRINT.md — titles, meta descriptions, schema, and internal link minima. A page that fails that validation does not deploy.

### Improvement mode (when all 100 cities have data)
Cycle through existing cities oldest-first and: hunt for missing photos, strengthen weak stories, re-verify flagged items, check for dead trees in the news.

### Collections (any time coverage allows)
Collections publish under the same regime as everything else since blueprint v1.3 (2026-07-27): the research standard, script-checked entries, superlatives per hard rule 8, readers as the correction layer. No owner approval; new collections are announced in LOG.md like any other work.

### Step 0b — Process reader submissions (before picking a new city)

Readers submit trees and whole cities through a public form. Hidde is deliberately not in this loop: submissions come straight to you.

If `SUBMISSIONS_CSV_URL` is set in scripts/build_site.py, fetch it at the start of every run. Each row is one submission. Skip any row whose id already appears in `data/submissions-processed.json`.

For each new submission:
1. Treat it as a research lead, never as fact. A submitter saying a tree is 500 years old is a claim to verify, not a source.
2. Apply the exact same bar as your own research: two independent sources for existence, species and age, and a location you can place precisely. The hard rules still apply in full, especially "never fabricate" and "photos need a verified open licence".
3. If it verifies: write the story in the tone of voice, add it to the right city file, and credit the submitter by the name they gave (`"submitted_by"` on the tree). If the city does not exist yet, create it as a new city file with the submitted trees, and set its status to `needs_curation`.
4. If it does not verify: do not publish it. Record it in CURATION.md under the submission's city with what is missing, so Hidde or a later run can pick it up.
5. Either way, append the row id to `data/submissions-processed.json` so it is never handled twice, and note the outcome in CURATION.md.

A submitted tree that verifies is worth more than a new city researched from scratch, because it proves someone cares about that city. Process submissions first, then continue with the next pending city if the usage window still allows.

## The mandate

This section exists so a run can decide for itself. Hidde is not watching, does not want to be the thing that starts the work, and will read `LOG.md` when he feels like it. Everything below is what he would say if you could ask him.

### What this is for

Two goals, deliberately ranked.

**1. Get someone to walk to a specific tree and enjoy standing in front of it.** Not "raise awareness of trees", not traffic. A named person, on a named street, looking up at a named tree that turned out to be worth the walk. Every feature, page and sentence is judged on whether it makes that more likely.

**2. Earn money.** Hidde does not need to get rich off this, but it should pay for itself and then some. (The "few thousand euro a month" figure that used to stand here was called loose talk by Hidde himself on 2026-07-26, GO_TO_MARKET.md "the revenue arithmetic: parked"; treat the amount as undecided, the direction as real.)

When the two conflict, goal 1 wins, because goal 2 does not exist without it. Nobody subscribes to a map that sent them to the wrong place.

Note what that does and does not imply. It does not mean polish before coverage: a map of five cities cannot get anyone outside who does not live in those five. It means never lying about what you have. A rough pin that admits it is rough still gets someone to the right park, and they can enjoy the hunt. A rough pin dressed up as exact gets them to a spot where the tree is not, and they do not come back. Build wide, label honestly.

**The bar under both: the experience has to be good.** MonumentalTrees has more trees than this project ever will, and it does not matter, because using it is miserable. That is the entire opening. So a page that is accurate but ugly, slow, confusing or joyless has not met the standard, even though every fact checks out.

Read that as a floor, not as a reason to stop and polish. The existing page template already clears it: a story worth reading, a map, a working directions button, nearby trees, an honest note when the pin is rough. Pouring a new city into that template gives you a good experience by default, so coverage and quality are not in conflict here. They only conflict when someone proposes rebuilding the template, and the answer to that is in the section above.

### Ship rough, ship wide, fix later

This project is unproven. Nobody has walked to a tree because of it, and nobody has paid for anything. Until that changes, the job is to put a lot of usable material in front of people quickly and find out whether any of it lands. Polish is what you do to something people already use.

**The default is the roughest version that is honest and useful.** Before any piece of work, ask: what is the smallest version that gets one person to a tree, or tells us whether anyone cares? Do that, ship it, move on.

Two lists, and the difference between them is the whole idea.

**Always cuttable, without discussion:**
- Precision. An approximate pin that says so is a finished first version.
- Photo coverage. Hunt hard for photos, they do more for goal 1 than any paragraph, but never hold a city back for them.
- Completeness. Eight good trees ship. The ninth can come later.
- Consistency and polish across pages, matching styles, tidy edge cases.
- A third and fourth source once two independent ones already agree.

**Never cuttable, at any speed:**
- Never fabricate. An invented fact is not a rough version of a real one.
- Never fake precision. Vague is fine when it says it is vague. See the honesty rule in Step 0.
- Never publish a photo without a verified open licence and attribution.
- Never promise the visitor something that is not there.
- Never publish a tree whose location its source deliberately withholds, or one on private land that is not open to visitors (hard rule 10). Speed is never bought from a tree's safety or someone's front garden.

Speed is bought from the first list only. Anything bought from the second is not a fast MVP, it is a broken product with a good excuse.

**The trap to watch for, because it has already happened here.** On 2026-07-21 a run built a quality floor that blocked new cities until existing ones were polished, at five cities, with no users. It was well argued and completely wrong: it optimised for a standard nobody was measuring yet, and it would have cost three months of coverage. The shape to recognise is a mechanism that enforces polish before there is demand for it. If you catch yourself designing a gate, a threshold or a floor, ask what evidence says anyone is waiting on the other side of it. Usually the honest answer is nobody, and the gate should not exist.

Prefer work that produces a signal over work that improves something nobody has used. Hard rule 6 asks whether real people will pay; this section is how that question gets answered, by shipping enough for the question to be answerable at all.

None of this is permanent. It flips when there is evidence: real visitors, submissions arriving, someone paying. Then polish stops being premature and starts being the job.

### Walk the user's timeline before you build

Cheap, and it is not a gate: it costs a minute of thinking and blocks nothing. Before building anything a person keeps, returns to, or accumulates, say out loud what happens at each of these, and fix whatever the answer embarrasses you with:

- **The first minute.** This is the only part that gets tested by default, and it is almost never where the problem is.
- **Day seven, and day thirty.** Is it still there? Does it still make sense? Has it quietly grown wrong?
- **The second device.** They read on a laptop and walk with a phone. Does the thing follow them?
- **The gap.** They come back after three weeks away. What do they find, and is it what they left?
- **The moment it fails.** Not whether it can fail, but what the person loses when it does, and whether they saw it coming.

**The worked example, so the shape is recognisable.** On 2026-07-21 a run shipped the tree passport, verified it thoroughly, and shipped a feature that would have silently deleted people's collections: browser storage on iOS Safari is wiped after seven days without a visit, which is exactly the three week trip the feature exists for. Everything tested passed. The tests were about whether it worked, over thirty seconds, when the entire value of collecting is measured in months. Hidde spotted it immediately, and he was right that it was obvious.

The lesson is not "know more about Safari". It is that knowing something does not help if nothing prompts you to ask. A feature whose value accrues over time has to be reasoned about over time, or the one property that matters is the one property never checked.

### Deciding on something nobody wrote a rule for

Most of what comes up is not in any list. Ask three questions, in order:

1. **Does it serve goal 1 or goal 2?** If neither, do not do it, however satisfying it looks. Activity is not progress.
2. **Can Hidde undo it?** Anything reversible is yours to decide. Ship it, write it in `LOG.md`, let him object afterwards. Being wrong in `LOG.md` is cheap.
3. **Can it hurt anyone other than Hidde?** Readers, submitters, people whose photos or data are involved. If yes, stop, whatever question 1 and 2 said. This is the only one that overrides the rest.

Then act. **When questions 1 and 2 pass and 3 is clear, do it, and do not ask.** Waiting for permission is the failure mode this project is built to avoid. Write down what you did and why, especially when the call was close.

Design, layout, features, page structure, copy, iconography and content all pass this test routinely. Hidde has said explicitly that until the product is proven he would rather you moved than checked. Take him at his word.

### The hard list

Five things stay closed no matter how well they score above, each for a reason that does not expire. If something is genuinely adjacent to one of these but not actually it, that is question 2 territory: go ahead and log it.

1. **No accounts, logins, or storage of personal data.** The moment real people's email addresses or profiles are involved, a mistake stops being Hidde's problem and becomes theirs, plus a GDPR liability in his name. Note this is the one item Hidde waved off and it stayed closed anyway: the loose phase is exactly when the foundation that data later flows into gets built, so it is the most expensive time to get wrong. A waitlist form that posts to Hidde is fine. A user table is not.
2. **No taking payments or setting prices.** Payment processors, subscriptions, plan tiers and the paywall line are Hidde's, because they involve his money, his tax position and a contract with a customer. Build features that could later be paid, price none of them.
3. **Nothing irreversible in public.** Retiring a URL Google has indexed, deleting data, force-pushing, giving up a domain. Reversible mistakes are how this project learns; unreversible ones are how it loses work permanently.
4. **Never speak as Hidde, never contact anyone as him.** No emails, no replies to submitters in his voice, no posts under his name. Write the draft, leave it for him.
5. **No new dependencies or third-party services** without Hidde's yes. Each one is a cost, a privacy question and something that can break the site while nobody is looking. The stack is deliberately boring: Python, static HTML, MapLibre, OpenFreeMap. On measurement, ruled by Hidde 2026-07-27 after learning Polarsteps itself runs cookies and Mixpanel: **cookieless analytics is allowed and wanted** (Cloudflare Web Analytics beacon: no cookies, no personal data, no consent banner needed). What stays banned, and this is the promise worth keeping: ads, ad-tracking, and selling or sharing visitor data, ever. Cookie-based product analytics becomes normal when the iOS app arrives, with proper consent, the Polarsteps model. Note the site itself never carried a "no tracking" claim in its copy (verified 2026-07-27), so no published promise is broken by any of this.

Also unchanged: **SEO_GEO_BLUEPRINT.md and TONE_OF_VOICE.md need Hidde's yes to edit** (hard rule 7), and so does **the brand**: name, domain, logo, core positioning.

### Where this is going: a paywall, and therefore accounts

Recorded 2026-07-21 at Hidde's request, so no future run has to rediscover it or argue him out of it.

**He intends to charge for this eventually.** Not donations alone, an actual paid tier. Nothing below is a reason to talk him out of that; it is the destination.

**And he is right that the passport cannot stay in LocalStorage forever.** Someone who has ticked off forty trees across three countries will not accept losing them, and they will lose them: browser storage goes when someone clears their data, does not exist in private browsing, never syncs between a phone and a laptop, and Safari on iOS deletes it outright after seven days without a visit. That last one breaks the exact case this feature exists for, a trip where you collect over weeks.

Those two facts are one fact. **A paywall requires accounts**, because an entitlement someone paid for cannot live in storage the browser is free to delete. So the hard list item on accounts is not permanent, and pretending otherwise would be dishonest about where this is heading.

What it does mean is that accounts are a project, not an afternoon. When it happens it brings a server, a database, someone's email address, a privacy policy, a data breach you can now have, subject access requests, and a bill. It also cannot be built without Hidde: it is his liability, his provider account and his name on the privacy policy.

So the sequence, and the reasoning behind it:

1. **Now: keep the passport local, and make losing it hard.** Let people export or back up what they have collected without an account. Cheap, no personal data, and it removes the worst failure before anyone has been burned by it.
2. **When there is evidence anyone wants this:** real visitors, submissions arriving, people actually ticking trees off. Then accounts and payment become the obvious next build rather than a bet.
3. **Never before then**, because an account system built for nobody is the most expensive way to learn there was nobody.

A run may not open this on its own. Building toward it is fine and welcome: keeping the passport data portable, keeping tree ids stable, avoiding anything that would make a later migration painful. Building the accounts themselves needs Hidde.

### The interim paywall line is still undecided

Hidde's instinct is that web and app should draw the line in roughly the same place: a lot free, with the genuinely good features behind a subscription. That points at content free everywhere (every tree, story and location, on both platforms, which is also what keeps the site indexable and serves goal 1) and payment attached to the features that get people out and bring them back: routes past several trees, a log of which ones you have visited, offline maps, a nudge when a tree near you is at its best.

It is not settled, and the `2 trees free per city` model written elsewhere in this file contradicts it. Do not resolve this alone and do not build anything that forces the choice. Per hard rule 6, the question is not which model is nicer but whether anyone will pay at all, and there is no evidence yet either way. Work that pays off under every model, better trees, precise pins, photos, faster pages, is always the safer bet.

### What Hidde reads when he has been away

`LOG.md` is the only channel. Assume he has not looked in a week and opens it cold. Lead with what changed about the product, keep what broke separate and obvious, and only use `FOR HIDDE` when something genuinely cannot move without him. A run that quietly did nothing useful should say so plainly rather than dress up the attempt.

## Quality gate: the research standard, not Hidde

Hidde is not the quality gate and will not be at 1,000 trees. Do not write anything that promises human review. The bar is the standard you already apply: two independent sources for existence, species and age, and a location you can place. Readers are the correction layer.

That puts the weight on you, so two rules tighten:
- **Publish what verifies, flag what does not.** A tree you cannot confirm does not go live with confident phrasing. State the range, name the disagreement (P7).
- **Set `location_precision` on every tree**, `"confirmed"` or `"approximate"`. Approximate means you know the park or street but not the spot. The site shows a visible warning next to the directions button for approximate pins, because sending someone to wander a park is a broken promise. Never mark a pin confirmed to make a page look tidier.

`curation_status` and the `status` field on a city stay in the data as internal signal, but they no longer gate publication and no longer show on the site.

## Hidde's curation workflow (optional, when he feels like it)

When Hidde opens a session, FIRST show him the top of CURATION.md: what's new, what's flagged, what needs photos. Prioritize his time on:
1. Cities he knows personally (Amsterdam, Lisbon, London, European cities)
2. Flagged items with uncertainty
3. Photo approvals

When he approves a city, set status to `curated` and each tree to `hidde_approved`.

## Hard rules

1. NEVER use content, photos, or text from monumentaltrees.com beyond fact verification. Their disclaimer prohibits commercial reuse.
2. NEVER fabricate tree facts. If you cannot verify age or location, flag it. A wrong location kills user trust permanently.
3. NEVER use em dashes anywhere.
4. Photos must have verified open licenses with attribution recorded.
5. Money, ruled by Hidde 2026-07-27, replacing the earlier €50/month ceiling: **no spending without his explicit approval, ever.** Beyond that there is no fixed monthly ceiling, on the one condition he stated himself: the project has to start earning. Keep runs efficient anyway; waste needs no budget to be wrong.
6. The goal is revenue, not a beautiful product nobody buys. If Hidde starts adding features before validation, remind him: "Have we validated that real people will pay for this?"
7. NEVER ship a page (tree, question, city, or collection) that doesn't conform to SEO_GEO_BLUEPRINT.md. Changes to that document itself require Hidde's explicit approval and a version bump.
8. Superlative claims ("oldest in Europe", "largest of its kind", "more than X and Y combined") must be checked against what other city pages already claim before publication. When in doubt, soften to "one of the oldest" or drop the claim.
9. Use one canonical common name per species so the species pages (Contract F) group correctly. When a species has multiple valid common names, pick the nationality-neutral one and match what other cities already use (e.g. Quercus robur is "Pedunculate Oak", never "English Oak"; Platanus x acerifolia is "London Plane"). The scientific name in parentheses is the tiebreaker for whether two trees are the same species.
10. **Publish public trees only, and never a location its source deliberately withholds.** Decided by Hidde on 2026-07-21. Some registers hide or blur the position of particular trees, and the Woodland Trust does this openly, because visitors damage ancient trees: soil compaction over the root plate, climbing, carving, and simple footfall. Others stand on private land whose owner never invited anyone. This site publishes exact coordinates and actively sends people to the trunk, which makes it capable of causing that harm rather than merely reporting it.

    So: if a source obscures a tree's location, treat that as a decision by people who know the tree and do not undo it, even where the position can be worked out from somewhere else. Do not publish a tree on private land unless it is genuinely open to visitors, and say what the access actually is. Prefer trees a city already signposts, because that is a public authority saying visitors are welcome. When in doubt, leave it out: there are far more qualifying public trees than this project will ever use, so this rule costs coverage that does not matter and prevents harm that cannot be undone.

    This is a question 3 rule in the sense of the mandate: it outranks goal 1, goal 2 and every argument about speed.

## Current state (as of handover)

- Amsterdam: researched in chat, needs to be converted to schema (10 trees identified: Olifantsiep, Leidsebosje platanen, Vondelpark Canadapopulier, Wertheimpark vleugelnoot, Hortus cycad, Artis oak, Lomanstraat X-trees, Amstelkade olijfwilg, Amstelveld vleugelnoten, Frederiksplein vleugelnoot)
- London: complete in schema (london.json exists with 10 trees, 6 verified, 2 need location verification)
- Landing page: HTML file exists (light minimal design, Playfair Display, waitlist form)
- Website content doc: exists with copy for homepage, about, blog structure
- City list: 100 cities prioritized in 4 tiers (Tier 1: Amsterdam, Lisbon, London, Paris, Rome, Tokyo, Istanbul, Barcelona, Kyoto, Madrid, New York, Singapore, Vienna, Prague, Bangkok, Berlin, Seville, Porto, Athens, Florence)

## First session goals

1. Set up the repository structure
2. Import the existing London data and Amsterdam research
3. Build the static site skeleton: homepage + city page template + interactive map (MapLibre + OpenStreetMap, no paid services)
4. Set up the GitHub Action for nightly runs
5. Do one test run on Paris to validate the workflow end-to-end
