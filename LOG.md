# LOG

What the autonomous runs did, newest first. One entry per run that actually changed something. Hidde reads this to catch up, and says good or bad.

Format, deliberately short:

```
## YYYY-MM-DD HH:MM — what it did in one line
- What changed (files, pages, cities)
- Why, if it was a judgement call
- FOR HIDDE: only when something genuinely needs him. Otherwise leave it out.
```

If an entry has no `FOR HIDDE` line, nothing is waiting on you. That is the normal case.

---

# Open with Hidde

Standing list. Everything else in this file is history; this block is what is actually waiting.

### 1. ~~Make the submission form~~ — DONE 2026-07-21

Form is live and wired in. Every contribution button on the site points at it, and
runs read the published CSV (email column excluded, so no address ever reaches a
run or the public sheet). Form: `SUBMISSION_FORM_URL`, responses:
`SUBMISSIONS_CSV_URL`, both in `scripts/build_site.py`.

Only thing left on Hidde: nothing, until submissions arrive. Then he may want to
mail the people who left an address to say their tree went live. That list lives
in the private column of his own spreadsheet.

### 2. Illustrated icons (needs Hidde's eye, do it together)

Map pins should move to the painterly style he asked for, and to leaf shapes so species actually differ. Six of Lisbon's ten trees still share one broadleaf silhouette. Deliberately not started alone: it is taste work.

### 3. Unanswered question

He said "je kan niet de website gratis maken". Everything so far assumes the opposite: the site stays free forever because it is the entire acquisition engine (blueprint P9), and the app is what people pay for. Worth settling, because it changes a lot.

### 4. Later, not now

Analytics once there is traffic, and cookieless to avoid a consent banner. Search Console reading needs his Google credentials; no data worth reading yet.

---

## 2026-07-21 18:30 — Tokyo researched and live: 6 cities, 60 trees

- No reader submissions yet (checked the CSV, header row only). Site was healthy (build clean, contracts passing), nothing published was wrong, so went straight to the next pending city per the ladder.
- Tokyo: 10 trees researched, written and shipped. Zenpukuji's 750-year-old ginkgo leads as Tokyo's oldest living tree; Sensoji's war-scarred ginkgo, Ueno Toshogu's 600-year camphor, and Meiji Jingu's ginkgo avenue and camphor couple round out the list. Full detail and what's flagged is in CURATION.md.
- The throughline that fell out of the research: Tokyo has burned down repeatedly (1657, 1868, 1923, 1945), and five of the ten surviving trees are ginkgos, a species whose wood resists catching fire. Used that as the city intro instead of a generic "remarkable trees of Tokyo" opener.
- 7 of 10 photos found on Wikimedia Commons (open licenses, awaiting your approval like always). 3 missing, none faked.
- 6 of 10 pins confirmed, 4 approximate (all cases of a tree inside a large garden or spanning an avenue rather than a single small address). No pin claims more precision than it has.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-21 17:00 — The funnel, thought through properly

Hidde asked for this while away. Written to be read cold.

**The funnel today, honestly:**

1. Someone finds the site. Nobody does. No distribution has happened, and the domain is new, so organic search will take months, not weeks.
2. They land on a city or tree page. These are good: story, map, directions, nearby trees.
3. They read.
4. They walk to a tree. Nothing bridges this, and it is where the product lives or dies.
5. They return, or pay. No mechanism, no evidence anyone would.

**The leak nobody is looking at is step 3 to 4.** Everyone is worried about step 1, and step 1 is real, but it is not the part we control. Someone reads about the Heimanseik at 22:00 on a Tuesday, thinks "nice", and never goes. The whole product is a destination read indoors, while the value only happens outdoors, on another day. Nothing currently carries the intent across that gap.

Three things close it, in order of how much they help:
- **A reason to go now.** Seasonality is the strongest and we have none of it: catkins, blossom, autumn colour, the month a given tree is worth the trip. That is knowledge nobody else has, it is cheap to research alongside the trees themselves, and it converts "nice" into "this weekend".
- **A way to keep it.** Saving a tree or a route for later, in LocalStorage, no account. Cheap, and it is the only thing that survives closing the tab.
- **The walk.** Built 2026-07-21. Turns ten scattered facts into one afternoon.

**On measurement, which is what makes the rest answerable.** Cloudflare analytics went live today, so within days we will know whether anyone arrives at all and which pages they land on. That is the first real signal this project has ever had. Note what it cannot see: whether anyone actually walked. Nothing on a website can see that, and pretending otherwise would be the wrong thing to build.

**The uncomfortable conclusion.** Every funnel improvement below step 1 multiplies a number that is currently zero. Distribution is the only step that changes the zero, and it cannot be automated: it needs Hidde to tell actual people this exists, once. Until that happens, more cities is the right work (it builds the SEO base that pays off in months) but it produces no learning at all. Runs should keep going wide, and nobody should mistake that for progress on the question of whether anyone cares.

FOR HIDDE: one post, one link, to any group of people who like trees or like Amsterdam. That is the whole ask, and it is worth more than the next twenty cities.

## 2026-07-21 10:15 — Paris pulled above the quality floor instead of starting city six

- Priority ladder in CLAUDE.md (rung 3, quality floor) beat rung 4 (next pending city, Tokyo): with the honest `location_precision` count from the previous run, Paris and Amsterdam were both below floor, and Paris was worse (8 of 10 approximate, 2 of 10 photos).
- Resolved all 8 approximate Paris pins to confirmed. Five city park/avenue trees matched against the Ville de Paris open tree registry (opendata.paris.fr); the three Jardin des Plantes trees aren't in that dataset at all (the garden belongs to the Museum national d'Histoire Naturelle, not the city) so those came from OpenStreetMap's individually named heritage-tree nodes instead, cross-checked against sourced planting dates.
- Added one photo (Great Plane of Parc Monceau, Public Domain), clearing Paris's photo floor too.
- Paris now has 0 approximate pins and 3 of 10 photos. Full detail in CURATION.md.
- Amsterdam is still below floor (7 of 10 approximate, 2 of 10 photos) and is next in line for the same treatment, ahead of Tokyo.

## 2026-07-21 09:00 — Every pin now says honestly how precise it is

- Set `location_precision` explicitly on all 50 trees. It was set on none of them, despite CLAUDE.md requiring it on every tree.
- The site had been guessing instead: `location_is_approximate()` sniffed free-text notes for ten hardcoded phrases like "exact position". Trees whose notes described a rough pin in any other wording rendered as confident pins with no warning.
- Six trees were lying to visitors that way. Adonis in Villa Borghese is the clearest: its note says the coordinates point at the Valle dei Platani generally, "not Adonis's specific trunk", and the page showed no warning. Same for the Hortus cycad, the Amstelveld wingnuts, the Rijksmuseum wingnut, the Belvedere cedar and Barney.
- Replaced the keyword guessing with the field alone, and made a missing field count as approximate. A warning nobody needed costs a visitor nothing; a missing one costs them a wasted walk.
- Result: 25 of 50 pins are approximate. That is high, and it is the real number. It also says where the improvement runs should go first: Paris (8 of 10) and Amsterdam (7 of 10).

## 2026-07-21 — Working agreement set up

- Added this log, plus a priority ladder and decision boundary in CLAUDE.md, so runs know what to work on and what to leave alone.
- Nothing about the site itself changed.
- FOR HIDDE: the boundary is in CLAUDE.md under "What runs decide alone". If anything in the "ask first" column feels too strict or too loose, move it. That list is the whole steering wheel.
