# DATA — the daily numbers, and what they mean

One entry per day, newest first, written automatically by the data-digest
workflow. Numbers are for the previous UTC day. While volume is tiny the
conclusion says so plainly; noise is never narrated as trend (Hidde's
standing rule, 2026-07-27).

## 2026-08-08 (previous UTC day)

Search Console (freshest day Google provides, data lags 2-3 days):
- 2026-08-08: 5 clicks, 187 impressions, avg position 10.3 (day before: c5/i226)
- Days: 07-30:c7/i251  07-31:c2/i230  08-01:c7/i253  08-02:c7/i299  08-03:c2/i260  08-04:c8/i254  08-05:c0/i280  08-06:c7/i215  08-07:c5/i226  08-08:c5/i187
- Top queries (10d): oldest tree in lisbon (i5, p11); "york museum gardens" (i4, p4); 400 year old tree (i1, p18); acient tree (i1, p40); alley pond giant (i1, p28)
- Top pages (10d): /lisbon (c4/i89); / (c3/i24); /kyoto (c3/i48); /amsterdam (c2/i133); /app (c2/i8)
- Content lead: '400 year old tree' has no matching page (i1, p18)
- Seen, not clicked: /rome (c0/i61, 0.0%) for trees in rome (i18, p18); trees of rome (i8, p26); rome trees (i8, p36)
- Seen, not clicked: /malaga (c0/i24, 0.0%) for árboles históricos de málaga (i19, p73); malaga tree (i3, p8); malaga trees (i1, p8)

Web Analytics (beacon, real browsers, cookieless):
- Days (visits/pageviews): 08-01:v10/p60  08-02:v20/p20  08-03:v10/p10  08-04:v10/p20  08-05:v20/p20  08-06:v0/p10  08-07:v30/p30  08-08:v70/p120
- Top paths: / (60); /app (40); /porto (30); /explore (10); /lisbon (10)
- Referrers: (direct) (130); ancienttrees.app (120); www.google.com (40)
- Countries: NL (130); US (40); PT (30); UA (20); DE (20)
- Devices: desktop (160); mobile (130)
- Page load (8d): p50 931ms, p90 5169ms

Links and referrers:
- External referrers (a link somebody clicked): none yet
- Backlink count: not automatable, Search Console's API has no links endpoint. Read it by hand at https://search.google.com/search-console/links?resource_id=sc-domain%3Aancienttrees.app

Site actions (yesterday): none recorded.
Waitlist signups (total): 5.
Registered accounts (total): 3, 1 new yesterday.

Machine: 9 chain attempts yesterday, 9 got real work time (~152 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 5 clicks and 187 impressions on Google's freshest day (day before: c5/i226). Directional at best; no strategic conclusions from these volumes.

## Weekly analysis 2026-08-08

Second weekly analysis, covering 2026-08-01 to 2026-08-07 against the prior
week (2026-07-25 to 2026-07-31).

**Scorecard**

| Week ending | Impressions | Clicks | CTR | Visits (beacon) | Pageviews (beacon) | Directions/visit | App-CTA | Waitlist total | Submissions total |
|---|---|---|---|---|---|---|---|---|---|
| 2026-07-31 | 1,150 | 31 | 2.7% | 70 | 170 | n/a (not captured) | n/a (not captured) | 0 real (2 test rows) | 0 real (1 test row) |
| 2026-08-07 | 1,762 | 36 | 2.0% | 100 | 170 | n/a (not captured) | n/a (not captured) | 4 real (LOG.md 08-06 confirms, not the test rows) | 0 real (1 test row, unchanged) |

**What moved:**
1. Impressions climbed 53% week over week (1,150 to 1,762) and clicks rose
   modestly (31 to 36), but CTR fell from 2.7% to 2.0%: more searchers are
   seeing the site without a matching gain in who clicks through.
2. Beacon visits rose 43% (70 to 100) while pageviews stayed flat at 170,
   so pages-per-visit dropped from 2.4 to 1.7: more arrivals, each looking
   at less before leaving.
3. The waitlist grew from 2 to 4 real signups this week, the first
   genuine week-over-week increase since tracking began (LOG.md 08-06
   confirms these are real Supabase rows, not the housekeeping test
   entries); submissions stayed at 0 real all week.
4. /rome and /malaga repeat every single day this week as the site's
   biggest seen-not-clicked pages: /rome draws 18-24 impressions/day at
   position ~17-20 for "trees in rome", /malaga 16-25 impressions/day at
   position 70+ for "árboles históricos de málaga", both at 0.0% CTR
   throughout the week.
5. Machine chain attempts collapsed to 1-4/day this week from 24-28/day
   the week before, consistent with Hidde's deliberate 07-31 trim to four
   one-hour runs/day (LOG.md), though three days (08-03/04/05) ran only a
   single attempt, below even that trimmed target.

**Suggestions, ranked:**
1. **[run]** Fix the content-lead detector's false-positive class. 'den
   brandt park' was flagged as "no matching page" two days running
   (i12/p70 each), but Antwerp's data/cities/antwerp.json already carries
   "The Park Trees of Den Brandt". This is the same failure mode as the
   already-documented 'ancient tree map' false positive against /explore
   (CLAUDE.md, "Search evidence is a run's to act on"). Per the project's
   own ratchet rule, a lesson that recurs becomes a build check: widen
   the matcher to check tree/page names, not just city/country/species,
   so real content gaps stop being buried under repeat false alarms.
2. **[sessie]** Wire directions-click and app-cta events into the daily
   digest / DATA.md. This is the same suggestion from the 08-02 weekly
   analysis, still unactioned: "Site actions" has read "none recorded"
   every day but one (a smoke-test row) all week, so the scorecard's
   Directions/visit and App-CTA columns stay permanently n/a and the
   funnel this analysis exists to track cannot be read.
3. **[FOR HIDDE]** The waitlist now holds real growth (2 to 4 this week,
   confirmed non-test by LOG.md 08-06), which already satisfies the
   demand condition your 2026-08-14 steady-fortnight review was waiting
   on ("whether a single waitlist signup or reader submission exists").
   Worth knowing going into that date; no action needed from a run.
4. **[run]** /rome and /malaga carry real, repeated impression volume at
   0.0% CTR every day this week (Rome ranks ~17-20 for "trees in rome"
   and related queries with no click ever landing; Malaga's Spanish
   query sits at position 70+). Rome's photo gap is already a documented
   dead end (LOG.md 08-06), so check instead whether these two pages
   satisfy P2 (answer in the first two sentences) and whether their
   titles/meta match the query wording, since these are the largest
   un-converted signals the site currently produces.

**Watch next week:** whether CTR recovers as impressions keep climbing
(or keeps falling, which would say ranking gains aren't converting), and
whether the waitlist's real growth continues toward the first genuine
reader submission.

## 2026-08-07 (previous UTC day)

Search Console (freshest day Google provides, data lags 2-3 days):
- 2026-08-07: 5 clicks, 201 impressions, avg position 9.8 (day before: c7/i215)
- Days: 07-29:c9/i247  07-30:c7/i251  07-31:c2/i230  08-01:c7/i253  08-02:c7/i299  08-03:c2/i260  08-04:c8/i254  08-05:c0/i280  08-06:c7/i215  08-07:c5/i201
- Top queries (10d): oldest tree in lisbon (i4, p12); "york museum gardens" (i4, p4); 400 year old tree (i1, p18); acient tree (i1, p40); alley pond giant (i1, p28)
- Top pages (10d): /lisbon (c5/i90); / (c3/i24); /porto (c3/i22); /amsterdam (c2/i152); /app (c2/i6)
- Content lead: 'den brandt park' has no matching page (i12, p70)
- Seen, not clicked: /rome (c0/i63, 0.0%) for trees in rome (i18, p20); trees of rome (i8, p26); rome trees (i8, p36)
- Seen, not clicked: /malaga (c0/i25, 0.0%) for árboles históricos de málaga (i20, p73); malaga tree (i3, p8); malaga trees (i1, p8)

Web Analytics (beacon, real browsers, cookieless):
- Days (visits/pageviews): 07-31:v0/p60  08-01:v10/p60  08-02:v20/p20  08-03:v10/p10  08-04:v10/p20  08-05:v20/p20  08-06:v0/p10  08-07:v30/p30
- Top paths: / (70); /cadiz (20); /collections/europes-best-tree-city-trips (10); /species/oriental-plane (10); /kyoto (10)
- Referrers: ancienttrees.app (130); (direct) (60); www.google.com (40)
- Countries: NL (140); US (30); UA (20); ES (10); DE (10)
- Devices: desktop (120); mobile (110)
- Page load (8d): p50 519000ms, p90 3411000ms

Links and referrers:
- External referrers (a link somebody clicked): none yet
- Backlink count: not automatable, Search Console's API has no links endpoint. Read it by hand at https://search.google.com/search-console/links?resource_id=sc-domain%3Aancienttrees.app

Site actions (yesterday): none recorded.
Waitlist signups (total): 4.

Machine: 4 chain attempts yesterday, 4 got real work time (~149 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 5 clicks and 201 impressions on Google's freshest day (day before: c7/i215). Directional at best; no strategic conclusions from these volumes.

## 2026-08-06 (previous UTC day)

Search Console (freshest day Google provides, data lags 2-3 days):
- 2026-08-06: 5 clicks, 195 impressions, avg position 13.1 (day before: c0/i280)
- Days: 07-28:c5/i197  07-29:c9/i247  07-30:c7/i251  07-31:c2/i230  08-01:c7/i253  08-02:c7/i299  08-03:c2/i260  08-04:c8/i254  08-05:c0/i280  08-06:c5/i195
- Top queries (10d): "york museum gardens" (i4, p4); 400 year old tree (i1, p18); acient tree (i1, p40); albero roma (i1, p47); alley pond giant (i1, p28)
- Top pages (10d): /lisbon (c5/i92); / (c3/i25); /porto (c3/i16); /app (c2/i6); /berlin/swamp-cypress-of-charlottenburg (c2/i3)
- Content lead: 'den brandt park' has no matching page (i12, p70)
- Seen, not clicked: /rome (c0/i69, 0.0%) for trees in rome (i20, p19); rome trees (i9, p36); trees of rome (i8, p26)
- Seen, not clicked: /malaga (c0/i23, 0.0%) for árboles históricos de málaga (i18, p73); malaga tree (i3, p8); malaga trees (i1, p8)

Web Analytics (beacon, real browsers, cookieless):
- Days (visits/pageviews): 07-30:v10/p10  07-31:v0/p60  08-01:v10/p60  08-02:v20/p20  08-03:v10/p10  08-04:v10/p20  08-05:v20/p20  08-06:v0/p10
- Top paths: / (70); /cadiz (20); /species/oriental-plane (10); /collections/europes-best-tree-city-trips (10); /lisbon (10)
- Referrers: ancienttrees.app (130); (direct) (60); www.google.com (20)
- Countries: NL (140); UA (30); ES (10); PL (10); GB (10)
- Devices: desktop (110); mobile (100)
- Page load (8d): p50 519000ms, p90 3411000ms

Site actions (yesterday): none recorded.
Waitlist signups (total): 4.

Machine: 2 chain attempts yesterday, 2 got real work time (~93 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 5 clicks and 195 impressions on Google's freshest day (day before: c0/i280). Directional at best; no strategic conclusions from these volumes.

## 2026-08-05 (previous UTC day)

Search Console (freshest day Google provides, data lags 2-3 days):
- 2026-08-05: 0 clicks, 261 impressions, avg position 14.4 (day before: c8/i254)
- Days: 07-27:c8/i205  07-28:c5/i197  07-29:c9/i247  07-30:c7/i251  07-31:c2/i230  08-01:c7/i253  08-02:c7/i299  08-03:c2/i260  08-04:c8/i254  08-05:c0/i261
- Top queries (10d): "york museum gardens" (i4, p4); 400 year old tree (i1, p18); acient tree (i1, p40); albero roma (i1, p47); alley pond giant (i1, p28)
- Top pages (10d): /lisbon (c6/i96); / (c3/i28); /porto (c3/i18); /app (c2/i6); /berlin/swamp-cypress-of-charlottenburg (c2/i2)
- Content lead: 'belgian tree' has no matching page (i4, p73)
- Seen, not clicked: /rome (c0/i77, 0.0%) for trees in rome (i24, p17); rome trees (i9, p36); trees of rome (i8, p26)
- Seen, not clicked: /malaga (c0/i21, 0.0%) for árboles históricos de málaga (i16, p73); malaga tree (i3, p8); malaga trees (i1, p8)

Web Analytics (beacon, real browsers, cookieless):
- Days (visits/pageviews): 07-29:v10/p10  07-30:v10/p10  07-31:v0/p60  08-01:v10/p60  08-02:v20/p20  08-03:v10/p10  08-04:v10/p20  08-05:v20/p20
- Top paths: / (70); /cadiz (20); /kyoto (10); /collections/europes-best-tree-city-trips (10); /species/oriental-plane (10)
- Referrers: ancienttrees.app (120); (direct) (60); www.google.com (30)
- Countries: NL (140); UA (30); US (20); PL (10); ES (10)
- Devices: desktop (110); mobile (100)
- Page load (8d): p50 463199ms, p90 3411000ms

Site actions (yesterday): none recorded.
Waitlist signups (total): 3.

Machine: 1 chain attempts yesterday, 1 got real work time (~10 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 0 clicks and 261 impressions on Google's freshest day (day before: c8/i254). Directional at best; no strategic conclusions from these volumes.

## 2026-08-04 (previous UTC day)

Search Console (freshest day Google provides, data lags 2-3 days):
- 2026-08-04: 8 clicks, 249 impressions, avg position 11.2 (day before: c2/i260)
- Days: 07-26:c1/i197  07-27:c8/i205  07-28:c5/i197  07-29:c9/i247  07-30:c7/i251  07-31:c2/i230  08-01:c7/i253  08-02:c7/i299  08-03:c2/i260  08-04:c8/i249
- Top queries (10d): "york museum gardens" (i4, p4); 400 year old tree (i1, p18); acient tree (i1, p40); albero roma (i1, p47); alley pond giant (i1, p28)
- Top pages (10d): /lisbon (c7/i103); / (c3/i27); /porto (c3/i15); /app (c2/i6); /berlin/swamp-cypress-of-charlottenburg (c2/i3)
- Content lead: 'ancient tree map' has no matching page (i7, p15)

Web Analytics (beacon, real browsers, cookieless):
- Days (visits/pageviews): 07-28:v20/p50  07-29:v10/p10  07-30:v10/p10  07-31:v0/p60  08-01:v10/p60  08-02:v20/p20  08-03:v10/p10  08-04:v10/p20
- Top paths: / (110); /cadiz (20); /kyoto (10); /the-hague (10); /collections/europes-best-tree-city-trips (10)
- Referrers: ancienttrees.app (150); (direct) (60); www.google.com (30)
- Countries: NL (180); UA (30); US (10); AU (10); ES (10)
- Devices: mobile (120); desktop (120)
- Page load (8d): p50 399000ms, p90 3411000ms

Site actions (yesterday): none recorded.
Waitlist signups (total): 3.

Machine: 1 chain attempts yesterday, 1 got real work time (~10 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 8 clicks and 249 impressions on Google's freshest day (day before: c2/i260). Directional at best; no strategic conclusions from these volumes.

## 2026-08-03 (previous UTC day)

Search Console (freshest day Google provides, data lags 2-3 days):
- 2026-08-03: 2 clicks, 249 impressions, avg position 12.4 (day before: c7/i299)
- Days: 07-25:c0/i117  07-26:c1/i197  07-27:c8/i205  07-28:c5/i197  07-29:c9/i247  07-30:c7/i251  07-31:c2/i230  08-01:c7/i253  08-02:c7/i299  08-03:c2/i249
- Top queries (10d): "york museum gardens" (i4, p4); acient tree (i1, p40); albero roma (i1, p47); alley pond giant (i1, p28); amsterdam plane trees (i1, p11)
- Top pages (10d): /lisbon (c6/i104); /berlin/swamp-cypress-of-charlottenburg (c2/i4); /bologna (c2/i27); /brussels/oldest-tree (c2/i4); /cadiz/oldest-tree (c2/i16)
- Content lead: 'ancient tree map' has no matching page (i7, p15)

Web Analytics (beacon, real browsers, cookieless):
- Days (visits/pageviews): 07-27:v20/p20  07-28:v20/p50  07-29:v10/p10  07-30:v10/p10  07-31:v0/p60  08-01:v10/p60  08-02:v20/p20  08-03:v10/p10
- Top paths: / (100); /lisbon (20); /cadiz (20); /kyoto (10); /collections/europes-best-tree-city-trips (10)
- Referrers: ancienttrees.app (140); (direct) (60); www.google.com (40)
- Countries: NL (160); UA (30); US (20); ES (10); BE (10)
- Devices: desktop (140); mobile (100)
- Page load (8d): p50 399000ms, p90 3411000ms

Site actions (yesterday): none recorded.
Waitlist signups (total): 2.

Machine: 1 chain attempts yesterday, 1 got real work time (~43 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 2 clicks and 249 impressions on Google's freshest day (day before: c7/i299). Directional at best; no strategic conclusions from these volumes.

## 2026-08-02 (previous UTC day)

Search Console (freshest day Google provides, data lags 2-3 days):
- 2026-08-03: 0 clicks, 13 impressions, avg position 6.6 (day before: c7/i297)
- Days: 07-24:c2/i106  07-25:c0/i117  07-26:c1/i197  07-27:c8/i205  07-28:c5/i197  07-29:c9/i247  07-30:c7/i251  07-31:c2/i230  08-01:c7/i253  08-02:c7/i297  08-03:c0/i13
- Top queries (10d): "york museum gardens" (i4, p4); acient tree (i1, p40); albero roma (i1, p47); alley pond giant (i1, p28); amsterdam plane trees (i1, p11)
- Top pages (10d): /lisbon (c6/i96); /amsterdam (c2/i123); /berlin/swamp-cypress-of-charlottenburg (c2/i4); /bologna (c2/i24); /brussels/oldest-tree (c2/i4)
- Content lead: 'ancient tree map' has no matching page (i6, p17)

Web Analytics (beacon, real browsers, cookieless):
- Days (visits/pageviews): 07-26:v10/p20  07-27:v20/p20  07-28:v20/p50  07-29:v10/p10  07-30:v10/p10  07-31:v0/p60  08-01:v10/p60  08-02:v20/p20
- Top paths: / (100); /cadiz (20); /lisbon (20); /collections/europes-best-tree-city-trips (10); /rotterdam (10)
- Referrers: ancienttrees.app (150); (direct) (60); www.google.com (40)
- Countries: NL (180); UA (20); US (20); ES (10); BE (10)
- Devices: desktop (150); mobile (100)
- Page load (8d): p50 383899ms, p90 2424799ms

Site actions (yesterday): none recorded.
Waitlist signups (total): 2.

Machine: 2 chain attempts yesterday, 2 got real work time (~80 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.
WATCHDOG: scheduled workflows silent past their slot: fresh-eyes review (last ran 26h ago). Kick with `gh workflow run <file>` and treat a repeat as rung 2.

**Conclusion:** Search is the only channel with real data and it is still small: 0 clicks and 13 impressions on Google's freshest day (day before: c7/i297). Directional at best; no strategic conclusions from these volumes.

## 2026-08-01 (previous UTC day)

Search Console: GSC_* secrets not configured; section skipped.

Web Analytics (beacon, real browsers, cookieless):
- Days (visits/pageviews): 07-25:v10/p10  07-26:v10/p20  07-27:v20/p20  07-28:v20/p50  07-29:v10/p10  07-30:v10/p10  07-31:v0/p60  08-01:v10/p60
- Top paths: / (100); /cadiz (20); /lisbon (20); /rotterdam (10); /collections/europes-best-tree-city-trips (10)
- Referrers: ancienttrees.app (150); (direct) (50); www.google.com (40)
- Countries: NL (190); US (20); UA (10); AU (10); BE (10)
- Devices: desktop (150); mobile (90)
- Page load (8d): p50 360700ms, p90 1019000ms

Site actions (yesterday): smoke-test 2
Waitlist signups (total): 2.

Machine: 4 chain attempts yesterday, 4 got real work time (~204 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Volume is still noise-level (0 unique visitors yesterday, 0 over the window): direction is not readable and no strategic conclusion should be drawn from these numbers yet.

## Weekly analysis 2026-08-02

First weekly analysis; only six daily entries exist (07-26 to 07-31), so
this sets the scorecard's first row rather than showing a trend.

**Scorecard**

| Week ending | Impressions | Clicks | CTR | Visits (beacon) | Pageviews (beacon) | Directions/visit | App-CTA | Waitlist total | Submissions total |
|---|---|---|---|---|---|---|---|---|---|
| 2026-07-31 | 1,150 | 31 | 2.7% | 70 | 170 | n/a (not captured) | n/a (not captured) | 0 real (2 test rows) | 0 real (1 test row) |

**What moved:**
1. Impressions climbed from noise (i38-i117 in the days before 07-26) to a
   197-249/day plateau by week's end, but clicks stayed single-digit and
   flat (0-9/day) the whole week: the site is getting crawled and indexed,
   not yet ranking well enough to convert (avg position 11.8-16.1, all
   page two or worse).
2. Beacon visits are the one number with a real, repeated up-move: 93
   visits in the window ending 07-30, 122 in the window ending 08-01, per
   three separate sessions' own `visitors.py` checks in LOG.md. Small, but
   the first trend that isn't noise.
3. Lisbon is the only page with meaningful clicks (6/10d) of anything on
   the site; Amsterdam, Rome, Vienna and Porto trail with 2/10d each.
   These five are exactly what Hidde's 08-01 dispatch already targets for
   a quality round.
4. Cloudflare's own top-line block ("Page views: 0, Unique visitors: 0")
   has read zero every single day for six days straight while the beacon
   reports real traffic on the same days: that block looks broken, not
   quiet.
5. Zero real waitlist or submission rows this week, only the one test row
   each already flagged in CURATION.md as pipeline tests. Demand signal
   is still exactly zero; Phase 1's trigger in GO_TO_MARKET.md has not
   fired.

**Suggestions, ranked:**
1. **[run]** Finish Hidde's 08-01 quality round on Lisbon, Amsterdam,
   Rome, Vienna, Porto (photos to 8/10, vague pins to confirmed, the
   ICNF corrections). These five pages carry 100% of this week's clicks
   (c6/i79, c2/i108, c2/i165, c2/i37, c2/i8), so any ranking or CTR gain
   there compounds directly instead of spreading thin across 78 cities.
2. **[run]** Diagnose the Cloudflare Web Analytics block: 0 page views
   and 0 unique visitors every day for six straight days while the
   separate beacon shows 10-60 page views the same days. Either the
   Cloudflare zone/binding is misconfigured or this metric is dead;
   either fix it or drop the section, a guaranteed-zero line every day
   is not a data point.
3. **[run]** Check whether "quercus aggressive" -site:reddit.com -s is a
   real query or a digest parsing artifact (the filter text reads like
   it leaked into the query string). It repeats at avg position 2 with
   real impressions, which is either a ranking worth understanding or a
   broken query extraction that is currently polluting "top queries"
   every day.
4. **[sessie]** Add directions-click, app-cta, waitlist and submission
   counts to the daily digest output. LOG.md confirms the events table
   went live 2026-07-31, but DATA.md carries none of it, so this
   scorecard cannot yet report the funnel ratios (directions-per-visit,
   waitlist/submissions growth) the analysis is meant to track. Without
   this the gap repeats every week.

**Watch next week:** whether clicks start converting from the roughly
1,150 impressions/week the site now draws (avg position moving below 10
on any of the five SEO cities), and whether any real (non-test) waitlist
or submission row appears now that the Supabase pipe is live.

## 2026-07-31 (previous UTC day)

Cloudflare, ancienttrees.app:
- Page views: 0 (day before: 0, 0)
- Unique visitors: 0 (day before: 0, 0)
- Requests total: 0
- Page views, last days: no data
- Top countries by requests: none recorded

Search Console (freshest day Google provides, data lags 2-3 days):
- 2026-07-31: 1 clicks, 55 impressions, avg position 16.1 (day before: c7/i249)
- Days: 07-22:c0/i38  07-23:c1/i103  07-24:c2/i106  07-25:c0/i117  07-26:c1/i197  07-27:c8/i205  07-28:c5/i197  07-29:c9/i247  07-30:c7/i249  07-31:c1/i55
- Top queries (10d): "quercus aggressive" -site:reddit.com -s (i6, p2); "york museum gardens" -site:reddit.com - (i3, p5); acient tree (i1, p40); albero roma (i1, p47); alley pond giant (i1, p28)
- Top pages (10d): /lisbon (c6/i79); /amsterdam (c2/i108); /porto (c2/i8); /rome (c2/i165); /vienna (c2/i37)

Web Analytics (beacon, real browsers, cookieless):
- Days (visits/pageviews): 07-24:v0/p20  07-25:v10/p10  07-26:v10/p20  07-27:v20/p20  07-28:v20/p50  07-29:v10/p10  07-30:v10/p10  07-31:v0/p60
- Top paths: / (70); /lisbon (20); /cadiz (20); /rotterdam (10); /verona/plane-tree-of-piazza-indipendenza (10)

Machine: 8 chain attempts yesterday, 8 got real work time (~444 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 1 clicks and 55 impressions on Google's freshest day (day before: c7/i249). Directional at best; no strategic conclusions from these volumes.

## 2026-07-30 (previous UTC day)

Cloudflare, ancienttrees.app:
- Page views: 0 (day before: 0, 0)
- Unique visitors: 0 (day before: 0, 0)
- Requests total: 0
- Page views, last days: no data
- Top countries by requests: none recorded

Search Console (freshest day Google provides, data lags 2-3 days):
- 2026-07-30: 7 clicks, 222 impressions, avg position 13.1 (day before: c9/i247)
- Days: 07-21:c1/i5  07-22:c0/i38  07-23:c1/i103  07-24:c2/i106  07-25:c0/i117  07-26:c1/i197  07-27:c8/i205  07-28:c5/i197  07-29:c9/i247  07-30:c7/i222
- Top queries (10d): "quercus aggressive" -site:reddit.com -s (i7, p2); acient tree (i1, p40); albero roma (i1, p47); amsterdam plane trees (i1, p11); amsterdam trees (i1, p36)
- Top pages (10d): /lisbon (c6/i76); /amsterdam (c2/i108); /porto (c2/i8); /rome (c2/i157); /vienna (c2/i36)

Web Analytics (beacon, real browsers, cookieless):
- Days (visits/pageviews): 07-23:v10/p10  07-24:v0/p20  07-25:v10/p10  07-26:v10/p20  07-27:v20/p20  07-28:v20/p50  07-29:v10/p10  07-30:v10/p10
- Top paths: / (70); /lisbon (20); /antwerp (10); /amsterdam (10); /verona/plane-tree-of-piazza-indipendenza (10)

Machine: 28 chain attempts yesterday, 28 got real work time (~717 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 7 clicks and 222 impressions on Google's freshest day (day before: c9/i247). Directional at best; no strategic conclusions from these volumes.

## 2026-07-29 (previous UTC day)

Cloudflare, ancienttrees.app:
- Page views: 0 (day before: 0, 0)
- Unique visitors: 0 (day before: 0, 0)
- Requests total: 0
- Page views, last days: no data
- Top countries by requests: none recorded

Search Console (freshest day Google provides, data lags 2-3 days):
- 2026-07-29: 8 clicks, 234 impressions, avg position 15.0 (day before: c5/i197)
- Days: 07-20:c0/i1  07-21:c1/i5  07-22:c0/i38  07-23:c1/i103  07-24:c2/i106  07-25:c0/i117  07-26:c1/i197  07-27:c8/i205  07-28:c5/i197  07-29:c8/i234
- Top queries (10d): "quercus aggressive" -site:reddit.com -s (i7, p2); albero roma (i1, p47); amsterdam plane trees (i1, p11); amsterdam trees (i1, p36); ancient greece trees (i1, p82)
- Top pages (10d): /lisbon (c4/i61); /porto (c2/i7); /rome (c2/i131); /vienna (c2/i31); / (c1/i22)

Web Analytics (beacon, real browsers, cookieless):
- Days (visits/pageviews): 07-22:v0/p10  07-23:v10/p10  07-24:v0/p20  07-25:v10/p10  07-26:v10/p20  07-27:v20/p20  07-28:v20/p50  07-29:v10/p10
- Top paths: / (70); /amsterdam (20); /lisbon (10); /antwerp (10); /verona/plane-tree-of-piazza-indipendenza (10)

Machine: 25 chain attempts yesterday, 25 got real work time (~940 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 8 clicks and 234 impressions on Google's freshest day (day before: c5/i197). Directional at best; no strategic conclusions from these volumes.

## 2026-07-28 (previous UTC day)

Cloudflare, ancienttrees.app:
- Page views: 0 (day before: 0, 0)
- Unique visitors: 0 (day before: 0, 0)
- Requests total: 0
- Page views, last days: no data
- Top countries by requests: none recorded

Search Console (freshest day Google provides, data lags 2-3 days):
- 2026-07-28: 5 clicks, 193 impressions, avg position 12.5 (day before: c8/i205)
- Days: 07-20:c0/i1  07-21:c1/i5  07-22:c0/i38  07-23:c1/i103  07-24:c2/i106  07-25:c0/i117  07-26:c1/i197  07-27:c8/i205  07-28:c5/i193
- Top queries (10d): "quercus aggressive" -site:reddit.com -s (i7, p2); albero roma (i1, p47); amsterdam plane trees (i1, p11); amsterdam trees (i1, p36); ancient greece trees (i1, p82)
- Top pages (10d): /lisbon (c3/i54); /vienna (c2/i21); / (c1/i20); /amsterdam (c1/i63); /athens (c1/i25)

Web Analytics (beacon, real browsers, cookieless):
- Days (visits/pageviews): 07-21:v0/p10  07-22:v0/p10  07-23:v10/p10  07-24:v0/p20  07-25:v10/p10  07-26:v10/p20  07-27:v20/p20  07-28:v20/p50
- Top paths: / (70); /amsterdam (20); /lisbon (10); /antwerp (10); /tokyo/oldest-tree (10)

Machine: 24 chain attempts yesterday, 23 got real work time (~958 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 5 clicks and 193 impressions on Google's freshest day (day before: c8/i205). Directional at best; no strategic conclusions from these volumes.

## 2026-07-27 (previous UTC day)

Cloudflare, ancienttrees.app:
- Page views: 0 (day before: 0, 0)
- Unique visitors: 0 (day before: 0, 0)
- Requests total: 0
- Page views, last days: no data
- Top countries by requests: none recorded

Search Console (freshest day Google provides, data lags 2-3 days):
- 2026-07-27: 5 clicks, 128 impressions, avg position 11.8 (day before: c1/i197)
- Days: 07-20:c0/i1  07-21:c1/i5  07-22:c0/i38  07-23:c1/i103  07-24:c2/i106  07-25:c0/i117  07-26:c1/i197  07-27:c5/i128
- Top queries (10d): "quercus aggressive" -site:reddit.com -s (i7, p2); amsterdam plane trees (i1, p11); amsterdam trees (i1, p36); ancient greece trees (i1, p82); ancient oaks (i2, p23)
- Top pages (10d): / (c1/i15); /amsterdam (c1/i54); /athens/olive-tree-of-pisistratus (c1/i3); /brussels/chene-josephine (c1/i3); /brussels/giant-sequoia-of-parc-de-woluwe (c1/i2)

Web Analytics (beacon, real browsers, cookieless):
- Days (visits/pageviews): 07-21:v0/p10  07-22:v0/p10  07-23:v10/p10  07-24:v0/p20  07-25:v10/p10  07-26:v10/p20  07-27:v20/p20
- Top paths: / (30); /amsterdam (20); /lisbon (10); /tokyo/oldest-tree (10); /antwerp (10)

**Conclusion:** Volume is still noise-level (0 unique visitors yesterday, 0 over the window): direction is not readable and no strategic conclusion should be drawn from these numbers yet.

## 2026-07-26 (previous UTC day)

Cloudflare, ancienttrees.app:
- Page views: 0 (day before: 0, 0)
- Unique visitors: 0 (day before: 0, 0)
- Requests total: 0
- Page views, last days: no data
- Top countries by requests: none recorded

Search Console (freshest day Google provides, data lags 2-3 days):
- 2026-07-27: 1 clicks, 25 impressions, avg position 16.1 (day before: c1/i197)
- Days: 07-20:c0/i1  07-21:c1/i5  07-22:c0/i38  07-23:c1/i103  07-24:c2/i106  07-25:c0/i117  07-26:c1/i197  07-27:c1/i25
- Top queries (10d): "quercus aggressive" -site:reddit.com -s (i7, p2); amsterdam plane trees (i1, p11); amsterdam trees (i1, p36); ancient greece trees (i1, p82); ancient oaks (i1, p26)
- Top pages (10d): / (c1/i13); /amsterdam (c1/i48); /athens/olive-tree-of-pisistratus (c1/i2); /lisbon (c1/i35); /paris/second-robinier (c1/i2)

**Conclusion:** Volume is still noise-level (0 unique visitors yesterday, 0 over the window): direction is not readable and no strategic conclusion should be drawn from these numbers yet.
