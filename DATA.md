# DATA — the daily numbers, and what they mean

One entry per day, newest first, written automatically by the data-digest
workflow. Numbers are for the previous UTC day. While volume is tiny the
conclusion says so plainly; noise is never narrated as trend (Hidde's
standing rule, 2026-07-27).

Three event counts changed meaning on 2026-08-20, and the fall in them is the
fix rather than a regression. Until that date `app-cta`, `directions` and
`walks-app` were each counted by two click listeners at once, so one click
inserted two rows. Read any figure for those three from before 2026-08-20 as
roughly double the real number, and do not compare one across that date.
`app-cta` was worse than doubled: it also fired on the two `walks-app` links,
because those point at /app and the listener matched the href. Every other
event on the list is unaffected.

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-10](archive/DATA-2026-10.md)
- [2026-09](archive/DATA-2026-09.md)
- [2026-08](archive/DATA-2026-08.md)
- [2026-07](archive/DATA-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
<!-- archive-index -->
## 2026-10-30 (previous UTC day)

**Today: an account was opened today (50 total).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 97 | 40 |
| ... of which from search | every search engine | 14 | 10 |
| ... from Google | Google's recovery | 3 | 3 |
| ... from Bing | Bing | 6 | 0 |
| Website visitors who came back | people who stay | 17 | 10 |
| App downloads (first-time) | people | 41 | 15 |
| New accounts | people | 13 | 8 |
| Phones back within 30 days | people who stay | 9 of 15 | 7 of 9 |
| Trees saved to Want to go | intent | 6 | 17 |
| Trees collected | goal 1: stood at a tree | 0 | 13 |
| Readers' contributions | data: trees, photos, corrections, votes | 8 | 11 |
| Shares (app and web) | word of mouth, since 10-30 | 0 | 0 |
| Visits from a shared link | what sharing brings | 0 | 0 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar; a visitor who comes back on another browser or device counts as new, and GA cannot leave our own visits out, so read the came-back row as a direction, not a count. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 10-24 | 10-25 | 10-26 | 10-27 | 10-28 | 10-29 | 10-30 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 41 | 11 | 14 | 11 | 7 | 8 | 12 | **104** |
| New accounts | 6 | 3 | 3 | 0 | 0 | 0 | 1 | **13** |
| Saves | 6 | 0 | 0 | 0 | 0 | 0 | 0 | **6** |
| Android waitlist | 15 | 4 | 5 | 1 | 0 | 1 | 0 | **26** |
| App downloads | 23 | 8 | 2 | 1 | 1 | 1 | 0 | **36** |
| App phones | 21 | 9 | 6 | 4 | 6 | 3 | 6 | **46** |
| Trees opened in the app | 104 | 37 | 88 | 4 | 17 | 33 | 6 | **289** |
| Trees collected | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Trees sent | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Feedback | 0 | 0 | 1 | 0 | 0 | 0 | 0 | **1** |
| Ambassador asks | 1 | 0 | 6 | 0 | 0 | 0 | 0 | **7** |
| App photos | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| App Store reviews | 0 | 0 | 0 | 1 | 0 | 0 | 0 | **1** |

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Waiting for you** (what the runs left for you since 2026-10-30)

- 357 email addresses ready to mail (archive 1, nature 8, guide 2, press 237, source 71, council 16, tourism 7, society 7, other 5, garden 3); 9 found by the night run since 2026-10-30
- the source batch of five waits for your word.
- Organizer, Distribute App, App Store Connect, then test it from TestFlight.
- the iOS scheduled run is red on StressWalk and SignedOutWalk (see above).

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| 2026-10-30 | The Town Hall Plane | - | - | open | - |
| 2026-10-30 | A tree in Baarn | - | - | open | - |
| 2026-10-30 | European Beech in Baarn | - | - | open | - |
| 2026-10-30 | A tree in Baarn | - | - | open | - |

4 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**Searched yesterday:** hounslow (3 times), leeuwa, lisboa, nantes.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-21 | 0 | 43 | 0.0% | 39.2 |
| 10-22 | 2 | 45 | 4.4% | 51.8 |
| 10-23 | 0 | 48 | 0.0% | 55.1 |
| 10-24 | 1 | 24 | 4.2% | 43.2 |
| 10-25 | 3 | 55 | 5.5% | 50.2 |
| 10-26 | 3 | 36 | 8.3% | 30.5 |
| 10-27 | 0 | 25 | 0.0% | 28.5 |
| 10-28 | 1 | 36 | 2.8% | 49.8 |
| 10-29 | 0 | 38 | 0.0% | 28.4 |
| 10-30 *partial* | 1 | 25 | 4.0% | 23.0 |
| **window** | **11** | **375** | **2.9%** | |
- Top queries (10d): 200 old tree trace (i1, p54); 43 rue buffon 75005 paris (i1, p73); 600 year old ginkgo tree jeonju (i1, p55); ahuehuete madrid (i1, p95); ancient roman trees (i1, p68)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-23 | 82 | 5 | 6.1% |
| 10-24 | 69 | 4 | 5.8% |
| 10-25 | 83 | 3 | 3.6% |
| 10-26 | 84 | 3 | 3.6% |
| 10-27 | 132 | 3 | 2.3% |
| 10-28 | 113 | 3 | 2.7% |
| 10-29 | - | - | 0.0% |
| **7 days** | **563** | **21** | **3.7%** |
- Week before: 530 impressions, 20 clicks. No Bing demotion in sight.
- Top Bing queries: oldest tree china (c8/i4, p12); fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); oak tree in zurich (c1/i4, p2); how old are the trees in queen square bristol (c1/i4, p3); trees in the plaza dus burgos seville (c1/i3, p5); oldest live oak trees in new orleans (c1/i2, p6); remarkable trees copenhagen (c1/i2, p4)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-30T07:58 | 9.9 | 0 | 5 | 1 | - |
| 10-30T14:53 | 9.8 | 1 | 5 | 1 | Paris +1 |
| 10-30T19:31 | 17.3 | 3 | 10 | 1 | Frankfurt +1, Graz +1, Rio Frio +1 |
| 10-31T01:22 | 15.7 | 0 | 9 | 1 | - |
| **4 runs** | **53** | **4** | **29** | | |

- 2 of 4 produced no trees; 1 to 1 commands refused per run; last build that went live: 11h ago, 4 failed since.

**What they made**

- Night run log: second retry, pace still full
- Night run retry: nothing could ship, spokane wall, log
- Night run log and agent costs, 2026-10-31 01:22 window
- Fort Worth and Canberra: seven stories written, held by the 25-a-day pace
- Build fix: reader account id out of four sighting photo paths, photo sizes measured
- Photographs readers sent, queued for a look; vouched ones live
- Record when each page last changed
- Canberra: five register trees verified for a writer, six leads, one dead
- Canberra verify pass: five register trees (can_004 to can_008) and leads
- Graz de intro back under 100 words
- Night run: costs, log, rio-frio names, health answer, sightings genus refill
- Rio Frio, Texas: the Rio Frio Landmark Oak (txf_004) as a single-tree place, view-only from FM 1120
- Graz: the Stadtpark Caucasian Wingnut (grz_017), from the park's first planting around 1870, with a squill best_time and German overlay; counts to 17
- Frankfurt: the Mark Oak of Offenbach (frk_024), six-stemmed register oak, story and German overlay; counts to 24

**Photographs the night run approved** (1; the last column undoes one)

| Day | Tree | Where | Overrule |
|---|---|---|---|
| 10-30 | The Sycamore Maple of Parc Monceau | Paris | `photo_apply.py hold par_073` |

Machine: 7 chain attempts yesterday, 6 got real work time (~61 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c8/i17); /lisbon (c1/i7); /lisbon/giant-rubber-tree-of-mouraria (c1/i2); /seville (c1/i1); /sequoia-national-park/general-sherman-tree (c0/i16)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'comfort tree niagara' (i2, p75)
    - '200 old tree trace' (i1, p54)
    - 'ancient roman trees' (i1, p68)
    - 'die 10 ältesten bäume der welt' (i1, p1)

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 370 |
| Clicks | 11 |
| Pages that got at least one impression | 225 |
| Impressions on the proven cities | 232 |

- 326 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3092 trees Google may index, 844 kept out for lacking a photo and an exact pin, 7023 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 95 | 1 | 2 | 0.02 | 0 |
| Not yet rich | 62 | 2 | 3 | 0.05 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| sequoia-national-park | 0 | 18 | 0.0% | 73.2 | 0.4% | general sherman tree (i4, p80) |
| munich | 0 | 11 | 0.0% | 6.0 | 5.0% | - |

- Plus 257 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

## 2026-10-29 (previous UTC day)

**Today: an android waitlist signup arrived yesterday (45 total).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 100 | 28 |
| ... of which from search | every search engine | 13 | 8 |
| ... from Google | Google's recovery | 2 | 3 |
| ... from Bing | Bing | 4 | 0 |
| Website visitors who came back | people who stay | 17 | 9 |
| App downloads (first-time) | people | 42 | 14 |
| New accounts | people | 13 | 7 |
| Phones back within 30 days | people who stay | 9 of 15 | 7 of 10 |
| Trees saved to Want to go | intent | 6 | 19 |
| Trees collected | goal 1: stood at a tree | 1 | 12 |
| Readers' contributions | data: trees, photos, corrections, votes | 8 | 11 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar; a visitor who comes back on another browser or device counts as new, and GA cannot leave our own visits out, so read the came-back row as a direction, not a count. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Ambassador requests, open** (3 people, 3 places; each stays here until the badge is granted with `python3 scripts/ambassador.py --grant`)

| Asked | Places | From | Our mail with the questions | Waiting on |
|---|---|---|---|---|
| 2026-10-26 | **Sintra** | /sintra | sent 2026-10-26 | their answer, then your yes |
| 2026-10-24 | **Porto** | the app | sent 2026-10-24 | their answer, then your yes |
| 2026-10-20 | **New York** | /new-york | sent 2026-10-20 | their answer, then your yes |

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 10-23 | 10-24 | 10-25 | 10-26 | 10-27 | 10-28 | 10-29 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 15 | 41 | 11 | 14 | 11 | 7 | 8 | **107** |
| New accounts | 1 | 6 | 3 | 3 | 0 | 0 | 0 | **13** |
| Saves | 0 | 6 | 0 | 0 | 0 | 0 | 0 | **6** |
| Android waitlist | 1 | 15 | 4 | 5 | 1 | 0 | 1 | **27** |
| App downloads | 5 | 23 | 8 | 2 | 1 | 1 | 0 | **40** |
| App phones | 2 | 21 | 10 | 6 | 5 | 6 | 4 | **44** |
| Trees opened in the app | 12 | 104 | 50 | 88 | 7 | 17 | 36 | **314** |
| Trees collected | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Trees sent | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Feedback | 0 | 0 | 0 | 1 | 0 | 0 | 0 | **1** |
| Ambassador asks | 0 | 1 | 0 | 6 | 0 | 0 | 0 | **7** |
| App photos | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| App Store reviews | 0 | 0 | 0 | 0 | 1 | 0 | 0 | **1** |

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Waiting for you** (what the runs left for you since 2026-10-29)

- 323 email addresses ready to mail (archive 0, nature 8, guide 0, press 232, source 50, council 14, society 7, other 5, tourism 4, garden 3); 8 found by the night run since 2026-10-29
- the iOS scheduled run is red on StressWalk and SignedOutWalk (see above).
- a session with Xcode should run StressWalk and look at those two actions.

**Searched yesterday:** amster, brisbane, bru.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-20 | 3 | 39 | 7.7% | 26.3 |
| 10-21 | 0 | 43 | 0.0% | 39.2 |
| 10-22 | 2 | 45 | 4.4% | 51.8 |
| 10-23 | 0 | 48 | 0.0% | 55.1 |
| 10-24 | 1 | 24 | 4.2% | 43.2 |
| 10-25 | 3 | 55 | 5.5% | 50.2 |
| 10-26 | 3 | 36 | 8.3% | 30.5 |
| 10-27 | 0 | 25 | 0.0% | 28.5 |
| 10-28 | 1 | 36 | 2.8% | 49.8 |
| 10-29 *partial* | 0 | 28 | 0.0% | 29.1 |
| **window** | **13** | **379** | **3.4%** | |
- Top queries (10d): # system role you operate as a precision (i1, p6); 200 old tree trace (i1, p54); 43 rue buffon 75005 paris (i1, p73); 600 year old ginkgo tree jeonju (i1, p55); ahuehuete madrid (i1, p95)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-22 | 77 | 2 | 2.6% |
| 10-23 | 82 | 5 | 6.1% |
| 10-24 | 69 | 4 | 5.8% |
| 10-25 | 83 | 3 | 3.6% |
| 10-26 | 84 | 3 | 3.6% |
| 10-27 | 132 | 3 | 2.3% |
| 10-28 | - | - | 0.0% |
| **7 days** | **527** | **20** | **3.8%** |
- Week before: 531 impressions, 26 clicks. No Bing demotion in sight.
- Top Bing queries: oldest tree china (c8/i4, p12); fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); oak tree in zurich (c1/i4, p2); how old are the trees in queen square bristol (c1/i4, p3); trees in the plaza dus burgos seville (c1/i3, p5); berlin tree (c1/i2, p1); oldest tree in belfast (c1/i2, p1)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-29T07:55 | 5.4 | 0 | 6 | 0 | - |
| 10-29T13:02 | 62.9 | 12 | 9 | 2 | Monchique +3, Canberra +2, Porto +2, Coimbra +1, +4 more |
| 10-30T01:22 | 8.2 | 0 | 3 | 0 | - |
| 10-30T01:32 | 2.9 | 0 | 7 | 0 | - |
| **4 runs** | **79** | **12** | **25** | | |

- 3 of 4 produced no trees; 2 to 2 commands refused per run; last build that went live: 4h ago.

**What they made**

- Coimbra released: only 4 unmined candidates, wall for 48h
- Night run continuation 2026-10-30: nothing new to take, Canberra still a wall
- Night run 2026-10-30: Algarve READY leads held, enrichment dead ends recorded, log
- Portugal READY leads: none could ship as written, 13 marked held, blocked or published with a dated reason
- Record when each page last changed
- Record when each page last changed
- Sao Bras de Alportel: the Algarve's Tree of the Year 2023 runner-up holm oak as a lone-tree place; Oliveira Real held on resort access
- Monchique: three classified trees (plane, Norfolk Island pine, Monchique oak) as a lone-tree place, found from Lagos
- Madeira: the Campo da Barca dragon tree; Vale do Pereiro: Portugal's Tree of the Year 2022 cork oak as its own lone-tree place
- Porto: the two remaining Palacete Burmester register trees go live (26 to 28); Setubal pass found only an Azeitao duplicate
- Coimbra: the Botanical Garden strangler fig goes live; Braga verified, nothing new (Tibaes still closed)
- Three written trees go live without a photograph now that the photo gate is off: Canberra x2, San Francisco x1
- Night run: Sintra and Guimaraes verify passes found nothing new, walls set (Portugal registers mined out)
- Fresh-eyes review: 4 finding(s)

Machine: 6 chain attempts yesterday, 2 got real work time (~72 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c10/i21); /lisbon (c1/i7); /lisbon/giant-rubber-tree-of-mouraria (c1/i2); /zaragoza/oldest-tree (c1/i1); /sequoia-national-park/general-sherman-tree (c0/i18)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'comfort tree niagara' (i2, p75)
    - '# system role you operate as a precision' (i1, p6)
    - '200 old tree trace' (i1, p54)
    - 'ancient roman trees' (i1, p68)
    - 'die 10 ältesten bäume der welt' (i1, p1)

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 392 |
| Clicks | 13 |
| Pages that got at least one impression | 229 |
| Impressions on the proven cities | 232 |

- 310 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3078 trees Google may index, 830 kept out for lacking a photo and an exact pin, 6967 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 95 | 1 | 2 | 0.02 | 0 |
| Not yet rich | 62 | 2 | 3 | 0.05 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| sequoia-national-park | 0 | 20 | 0.0% | 72.3 | 0.4% | general sherman tree (i4, p80) |
| munich | 0 | 11 | 0.0% | 6.0 | 5.0% | - |

- Plus 257 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

## 2026-10-28 (previous UTC day)

**Today: nothing here needs you.** The blocks below are the standing picture.

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 103 | 21 |
| ... of which from search | every search engine | 12 | 6 |
| ... from Google | Google's recovery | 3 | 2 |
| ... from Bing | Bing | 2 | 0 |
| Website visitors who came back | people who stay | 17 | 7 |
| App downloads (first-time) | people | 44 | 13 |
| New accounts | people | 15 | 5 |
| Phones back within 30 days | people who stay | 9 of 13 | 7 of 12 |
| Trees saved to Want to go | intent | 19 | 6 |
| Trees collected | goal 1: stood at a tree | 1 | 12 |
| Readers' contributions | data: trees, photos, corrections, votes | 8 | 11 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar; a visitor who comes back on another browser or device counts as new, and GA cannot leave our own visits out, so read the came-back row as a direction, not a count. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Ambassador requests, open** (3 people, 3 places; each stays here until the badge is granted with `python3 scripts/ambassador.py --grant`)

| Asked | Places | From | Our mail with the questions | Waiting on |
|---|---|---|---|---|
| 2026-10-26 | **Sintra** | /sintra | sent 2026-10-26 | their answer, then your yes |
| 2026-10-24 | **Porto** | the app | sent 2026-10-24 | their answer, then your yes |
| 2026-10-20 | **New York** | /new-york | sent 2026-10-20 | their answer, then your yes |

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 10-22 | 10-23 | 10-24 | 10-25 | 10-26 | 10-27 | 10-28 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 11 | 15 | 41 | 11 | 14 | 11 | 7 | **110** |
| New accounts | 2 | 1 | 6 | 3 | 3 | 0 | 0 | **15** |
| Saves | 13 | 0 | 6 | 0 | 0 | 0 | 0 | **19** |
| Android waitlist | 0 | 1 | 15 | 4 | 5 | 1 | 0 | **26** |
| App downloads | 2 | 5 | 23 | 8 | 2 | 1 | 0 | **41** |
| Trees sent | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Feedback | 0 | 0 | 0 | 0 | 1 | 0 | 0 | **1** |
| Ambassador asks | 0 | 0 | 1 | 0 | 6 | 0 | 0 | **7** |
| App photos | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Waiting for you** (what the runs left for you since 2026-10-28)

- 382 email addresses ready to mail (archive 1, nature 6, guide 0, press 270, source 73, council 14, society 6, other 5, tourism 4, garden 3); 2 found by the night run since 2026-10-28
- the association file still keeps /profile in Safari; flip it once a store build carries the handler, or a shared link opens today's app on nothing.

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| 2026-10-22 | The Weeping Cedar of the Vallée-aux-Lo | Chatenay-Malabry | - | publish | ja, ziet er goed uit |

0 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**Searched yesterday:** mil (2 times), perth (2 times), chesterfield, great kanto, li.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-19 | 1 | 48 | 2.1% | 59.2 |
| 10-20 | 3 | 39 | 7.7% | 26.3 |
| 10-21 | 0 | 43 | 0.0% | 39.2 |
| 10-22 | 2 | 45 | 4.4% | 51.8 |
| 10-23 | 0 | 48 | 0.0% | 55.1 |
| 10-24 | 1 | 24 | 4.2% | 43.2 |
| 10-25 | 3 | 55 | 5.5% | 50.2 |
| 10-26 | 3 | 36 | 8.3% | 30.5 |
| 10-27 | 0 | 25 | 0.0% | 28.5 |
| 10-28 *partial* | 1 | 28 | 3.6% | 50.6 |
| **window** | **14** | **391** | **3.6%** | |
- Top queries (10d): # system role you operate as a precision (i1, p6); 200 old tree trace (i1, p54); 2023 euwallacea validus over 20 families (i1, p96); 43 rue buffon 75005 paris (i1, p73); 600 year old ginkgo tree jeonju (i1, p55)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-20 | 91 | 9 | 9.9% |
| 10-21 | 103 | 2 | 1.9% |
| 10-22 | 77 | 2 | 2.6% |
| 10-23 | 82 | 5 | 6.1% |
| 10-24 | 69 | 4 | 5.8% |
| 10-25 | 83 | 3 | 3.6% |
| 10-26 | 84 | 3 | 3.6% |
| **7 days** | **589** | **28** | **4.8%** |
- Week before: 521 impressions, 20 clicks. No Bing demotion in sight.
- Top Bing queries: oldest tree china (c8/i4, p12); fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); oak tree in zurich (c1/i4, p2); how old are the trees in queen square bristol (c1/i4, p3); trees in the plaza dus burgos seville (c1/i3, p5); husalle lindens copenhagen (c1/i2, p3); ancient trees in wiesbaden germany (c1/i2, p6)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-28T07:50 | 11.3 | 0 | 5 | 2 | - |
| 10-28T19:45 | 7.6 | 0 | 4 | 0 | - |
| **2 runs** | **19** | **0** | **9** | | |

- 2 of 2 produced no trees; 2 to 2 commands refused per run; last build that went live: 6h ago.

**What they made**

- Contributor replies and ambassador invitations sent, log updated
- Canberra can_002 and can_003 written, held for a photograph; LOG: pending shelf, nothing shippable
- Record when each page last changed
- Contributor replies and ambassador invitations sent, log updated
- Log: contact sourcing
- Canberra verify pass: 2 register-only trees held for photographs; log
- Fresh-eyes review: 5 finding(s)
- Fresh-eyes review: 2 finding(s)

Machine: 7 chain attempts yesterday, 2 got real work time (~25 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c10/i20); /lisbon (c1/i6); /de/vienna/giant-sequoias-of-potzleinsdorfer-schlosspark (c1/i2); /lisbon/giant-rubber-tree-of-mouraria (c1/i2); /zaragoza/oldest-tree (c1/i1)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'comfort tree niagara' (i2, p75)
    - '# system role you operate as a precision' (i1, p6)
    - '200 old tree trace' (i1, p54)
    - '2023 euwallacea validus over 20 families' (i1, p96)
    - 'ancient roman trees' (i1, p68)

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 400 |
| Clicks | 14 |
| Pages that got at least one impression | 232 |
| Impressions on the proven cities | 238 |

- 260 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3073 trees Google may index, 823 kept out for lacking a photo and an exact pin, 6950 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 95 | 1 | 2 | 0.02 | 0 |
| Not yet rich | 59 | 1 | 2 | 0.03 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| sequoia-national-park | 0 | 23 | 0.0% | 72.7 | 0.4% | general sherman tree (i5, p76) |
| munich | 0 | 11 | 0.0% | 6.0 | 5.0% | - |

- Plus 257 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

## 2026-10-27 (previous UTC day)

**Today: an android waitlist signup arrived yesterday (44 total).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 99 | 23 |
| ... of which from search | every search engine | 10 | 7 |
| ... from Google | Google's recovery | 3 | 2 |
| ... from Bing | Bing | 1 | 1 |
| App downloads (first-time) | people | 46 | 11 |
| New accounts | people | 16 | 5 |
| Phones back within 30 days | people who stay | 9 of 12 | 8 of 16 |
| Trees saved to Want to go | intent | 19 | 6 |
| Trees collected | goal 1: stood at a tree | 6 | 7 |
| Readers' contributions | data: trees, photos, corrections, votes | 8 | 11 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Ambassador requests, open** (8; each stays here until the badge is granted with `python3 scripts/ambassador.py --grant`)

| Asked | Place | From | Our mail with the questions | Waiting on |
|---|---|---|---|---|
| 2026-10-26 | **Vales** | /vales | not yet (next knock) | the mail |
| 2026-10-26 | **Calvos** | /calvos | not yet (next knock) | the mail |
| 2026-10-26 | **Braga** | /braga | not yet (next knock) | the mail |
| 2026-10-26 | **Guimaraes** | /guimaraes | not yet (next knock) | the mail |
| 2026-10-26 | **Porto** | /porto | sent 2026-10-27 | their answer, then your yes |
| 2026-10-26 | **Sintra** | /sintra | sent 2026-10-26 | their answer, then your yes |
| 2026-10-24 | **Porto** | the app | sent 2026-10-24 | their answer, then your yes |
| 2026-10-20 | **New York** | /new-york | sent 2026-10-20 | their answer, then your yes |

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 10-21 | 10-22 | 10-23 | 10-24 | 10-25 | 10-26 | 10-27 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 3 | 11 | 15 | 41 | 11 | 14 | 11 | **106** |
| New accounts | 1 | 2 | 1 | 6 | 3 | 3 | 0 | **16** |
| Saves | 0 | 13 | 0 | 6 | 0 | 0 | 0 | **19** |
| Android waitlist | 0 | 0 | 1 | 15 | 4 | 5 | 1 | **26** |
| App downloads | 3 | 2 | 5 | 23 | 8 | 2 | 0 | **43** |
| Trees sent | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Feedback | 0 | 0 | 0 | 0 | 0 | 1 | 0 | **1** |
| Ambassador asks | 0 | 0 | 0 | 1 | 0 | 6 | 0 | **7** |
| App photos | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Waiting for you** (what the runs left for you since 2026-10-27)

- 388 email addresses ready to mail (archive 3, nature 10, guide 0, press 270, source 73, council 14, society 6, other 5, tourism 4, garden 3); 2 found by the night run since 2026-10-27
- the next app build carries the second-ambassador line.
- next build carries the fix for sightings re-sent on every sign-in.

**What readers gave us, and it went live**

| Day | Reader | Tree | Where | What | Page |
|---|---|---|---|---|---|
| 10-26 | A | por_011 (The Copper Beech of FAUP) | Porto | a reader's feedback changed the page | - |
- All from one reader (reader A 1).

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| 2026-10-22 | The Weeping Cedar of the Vallée-aux-Lo | Chatenay-Malabry | - | publish | ja, ziet er goed uit |

0 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**Searched yesterday:** oaks (3 times), lis.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-18 | 2 | 53 | 3.8% | 42.9 |
| 10-19 | 1 | 48 | 2.1% | 59.2 |
| 10-20 | 3 | 39 | 7.7% | 26.3 |
| 10-21 | 0 | 43 | 0.0% | 39.2 |
| 10-22 | 2 | 45 | 4.4% | 51.8 |
| 10-23 | 0 | 48 | 0.0% | 55.1 |
| 10-24 | 1 | 24 | 4.2% | 43.2 |
| 10-25 | 3 | 55 | 5.5% | 50.2 |
| 10-26 | 3 | 36 | 8.3% | 30.5 |
| 10-27 *partial* | 0 | 22 | 0.0% | 25.7 |
| **window** | **15** | **413** | **3.6%** | |
- Top queries (10d): # system role you operate as a precision (i1, p6); 200 old tree trace (i1, p54); 2023 euwallacea validus over 20 families (i1, p96); 43 rue buffon 75005 paris (i1, p73); 600 year old ginkgo tree jeonju (i1, p55)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-19 | 82 | 0 | 0.0% |
| 10-20 | 91 | 9 | 9.9% |
| 10-21 | 103 | 2 | 1.9% |
| 10-22 | 77 | 2 | 2.6% |
| 10-23 | 82 | 5 | 6.1% |
| 10-24 | 69 | 4 | 5.8% |
| 10-25 | 83 | 3 | 3.6% |
| **7 days** | **587** | **25** | **4.3%** |
- Week before: 520 impressions, 23 clicks. No Bing demotion in sight.
- Top Bing queries: oldest tree china (c8/i4, p12); fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); how old are the trees in queen square bristol (c1/i4, p3); oak tree in zurich (c1/i4, p2); trees in the plaza dus burgos seville (c1/i3, p5); oldest live oak trees in new orleans (c1/i2, p6); husalle lindens copenhagen (c1/i2, p3)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-27T18:18 | 16.2 | 0 | 7 | 0 | Bamberg, Lisbon, Potsdam |
| **1 runs** | **16** | **0** | **7** | | |

- 1 of 1 produced no trees; last build that went live: 1h ago.

**What they made**

- Record when each page last changed
- Bristol register retried: Leigh Woods walk is a finding aid only; log
- San Francisco verify pass: 2 flagged entries awaiting photographs; log
- Scout Canberra: ACT Tree Register (CC BY 4.0) imported, 12 leads
- Enrich lisbon/albertshausen/bamberg/potsdam; two archive contacts sourced; log
- Record when each page last changed
- Record when each page last changed
- Fresh-eyes review: 4 finding(s)
- Fresh-eyes review: 2 finding(s)
- Vendor 1 photograph file(s) onto our own domain

Machine: 9 chain attempts yesterday, 3 got real work time (~35 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c11/i24); /lisbon (c1/i4); /de/stuttgart/hohenheim-love-plane (c1/i2); /de/vienna/giant-sequoias-of-potzleinsdorfer-schlosspark (c1/i2); /zaragoza/oldest-tree (c1/i1)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'comfort tree niagara' (i2, p75)
    - '# system role you operate as a precision' (i1, p6)
    - '200 old tree trace' (i1, p54)
    - '2023 euwallacea validus over 20 families' (i1, p96)
    - 'ancient roman trees' (i1, p68)

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 425 |
| Clicks | 15 |
| Pages that got at least one impression | 238 |
| Impressions on the proven cities | 255 |

- 277 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3073 trees Google may index, 823 kept out for lacking a photo and an exact pin, 6950 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 95 | 1 | 2 | 0.02 | 0 |
| Not yet rich | 59 | 1 | 2 | 0.03 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| sequoia-national-park | 0 | 26 | 0.0% | 71.7 | 0.4% | general sherman tree (i6, p75) |
| munich | 0 | 13 | 0.0% | 5.3 | 6.4% | - |

- Plus 257 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

## 2026-10-26 (previous UTC day)

**Today: an android waitlist signup arrived today (48 total); an ambassador request for Braga and an ambassador request for Calvos and an ambassador request for Guimaraes and an ambassador request for Porto and an ambassador request for Sintra and an ambassador request for Vales and a feedback report arrived yesterday (55 total); 3 accounts were opened yesterday (48 total).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 96 | 25 |
| ... of which from search | every search engine | 10 | 7 |
| ... from Google | Google's recovery | 4 | 1 |
| ... from Bing | Bing | 1 | 1 |
| App downloads (first-time) | people | 45 | 15 |
| New accounts | people | 17 | 5 |
| Phones back within 30 days | people who stay | 13 of 18 | 5 of 14 |
| Trees saved to Want to go | intent | 19 | 7 |
| Trees collected | goal 1: stood at a tree | 6 | 7 |
| Readers' contributions | data: trees, photos, corrections, votes | 17 | 5 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Ambassador requests, open** (9; each stays here until the badge is granted with `python3 scripts/ambassador.py --grant`)

| Asked | Place | From | Our mail with the questions | Waiting on |
|---|---|---|---|---|
| 2026-10-26 | **Vales** | /vales | not yet (next knock) | the mail |
| 2026-10-26 | **Calvos** | /calvos | not yet (next knock) | the mail |
| 2026-10-26 | **Braga** | /braga | not yet (next knock) | the mail |
| 2026-10-26 | **Guimaraes** | /guimaraes | not yet (next knock) | the mail |
| 2026-10-26 | **Porto** | /porto | sent 2026-10-27 | their answer, then your yes |
| 2026-10-26 | **Sintra** | /sintra | sent 2026-10-26 | their answer, then your yes |
| 2026-10-24 | **Porto** | the app | sent 2026-10-24 | their answer, then your yes |
| 2026-10-22 | **Bucaco** | /bucaco | sent 2026-10-22 | their answer, then your yes |
| 2026-10-20 | **New York** | /new-york | sent 2026-10-20 | their answer, then your yes |

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 10-20 | 10-21 | 10-22 | 10-23 | 10-24 | 10-25 | 10-26 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 6 | 3 | 11 | 15 | 41 | 11 | 14 | **101** |
| New accounts | 1 | 1 | 2 | 1 | 6 | 3 | 3 | **17** |
| Saves | 0 | 0 | 13 | 0 | 6 | 0 | 0 | **19** |
| Android waitlist | 0 | 0 | 0 | 1 | 15 | 4 | 5 | **25** |
| App downloads | 3 | 3 | 2 | 5 | 23 | 8 | 0 | **44** |
| Trees sent | 1 | 0 | 0 | 0 | 0 | 0 | 0 | **1** |
| Feedback | 6 | 0 | 0 | 0 | 0 | 0 | 1 | **7** |
| Ambassador asks | 1 | 0 | 1 | 0 | 1 | 0 | 6 | **9** |
| App photos | 7 | 5 | 2 | 0 | 0 | 1 | 0 | **15** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Waiting for you** (what the runs left for you since 2026-10-26)

- 431 email addresses ready to mail (archive 2, nature 54, guide 0, press 270, source 73, council 14, society 6, other 5, tourism 4, garden 3); 62 found by the night run since 2026-10-26
- " line and nobody checked the send log or his mail.

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| 2026-10-22 | The Weeping Cedar of the Vallée-aux-Lo | Chatenay-Malabry | - | publish | ja, ziet er goed uit |
| 2026-10-20 | The Weeping Fig of Campo Santana | Lisbon | - | publish | ja, eens |
| 2026-10-20 | Dragon Tree in Lisbon | - | - | publish | ja, eens |
| 2026-10-20 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | ja, eens |
| 2026-10-20 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | ja, eens (zelfde boom, alle vier eens 2026-10-22) |
| 2026-10-20 | The Paperbark of Jardim Constantino | Lisbon | - | publish | ja, eens |
| 2026-10-20 | The Weeping Fig of Campo Santana | Lisbon | - | publish | ja, eens (zelfde boom, alle vier eens 2026-10-22) |
| 2026-10-20 | Dragon Tree in Lisbon | - | - | publish | ja, eens (zelfde boom, alle vier eens 2026-10-22) |

0 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**Searched yesterday:** vila nova (11 times), oeiras (5 times), braganca (2 times), castelo branco (2 times), lisb (2 times), oli (2 times), porto (2 times), portugal (2 times), sintra (2 times), barc, forta, lis, lisboa, lisboa, portugal, palmela, pot, sao p.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-17 | 2 | 62 | 3.2% | 44.6 |
| 10-18 | 2 | 53 | 3.8% | 42.9 |
| 10-19 | 1 | 48 | 2.1% | 59.2 |
| 10-20 | 3 | 39 | 7.7% | 26.3 |
| 10-21 | 0 | 43 | 0.0% | 39.2 |
| 10-22 | 2 | 45 | 4.4% | 51.8 |
| 10-23 | 0 | 48 | 0.0% | 55.1 |
| 10-24 | 1 | 24 | 4.2% | 43.2 |
| 10-25 | 3 | 55 | 5.5% | 50.2 |
| 10-26 *partial* | 3 | 33 | 9.1% | 30.7 |
| **window** | **17** | **450** | **3.8%** | |
- Top queries (10d): # system role you operate as a precision (i1, p6); 200 old tree trace (i1, p54); 2023 euwallacea validus over 20 families (i1, p96); 43 rue buffon 75005 paris (i1, p73); 600 year old ginkgo tree jeonju (i1, p55)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-19 | 82 | 0 | 0.0% |
| 10-20 | 91 | 9 | 9.9% |
| 10-21 | 103 | 2 | 1.9% |
| 10-22 | 77 | 2 | 2.6% |
| 10-23 | 82 | 5 | 6.1% |
| 10-24 | 69 | 4 | 5.8% |
| 10-25 | - | - | 0.0% |
| **7 days** | **504** | **22** | **4.4%** |
- Week before: 520 impressions, 23 clicks. No Bing demotion in sight.
- Top Bing queries: oldest tree china (c8/i4, p12); fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); how old are the trees in queen square bristol (c1/i4, p3); oak tree in zurich (c1/i4, p2); trees in the plaza dus burgos seville (c1/i3, p5); berlin tree (c1/i2, p1); oldest tree in belfast (c1/i2, p1)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-26T09:35 | 5.8 | 12 | 6 | 1 | Shikokuchuo +2, Bregenz +1, College Station +1, Coppell +1, +7 more |
| 10-27T00:51 | 4.9 | 1 | 5 | 0 | Koriyama +1 |
| 10-27T06:10 | 9.0 | 0 | 4 | 0 | - |
| **3 runs** | **20** | **13** | **15** | | |

- 1 of 3 produced no trees; 1 to 1 commands refused per run; last build that went live: 1h ago.

**What they made**

- Log: Canterbury register retried, still stalled; nothing publishable
- Day run: San Francisco register used up, sfo_013 held for a photograph, Middletown retried; log and costs
- San Francisco: story for sfo_013 (held, no photo); sfo_012 marked duplicate of sfo_004
- Record when each page last changed
- Scouting: York retried, still stalled (only Victorian plantings)
- Log: night run 2026-10-27
- Koriyama: Tate-no-Omayumi (giant spindle tree, approved photograph) joins Akatsu no Katsura; intro and meta now say two
- Contributor replies and ambassador invitations sent, log updated
- Weekly analysis
- Fresh-eyes review: 8 finding(s)
- Fresh-eyes review: 5 finding(s)
- Record when each page last changed
- Vendor 12 photograph file(s) onto our own domain
- Three Texas famous trees (Goliad, Coppell, College Station) go live with photographs; log

Machine: 6 chain attempts yesterday, 1 got real work time (~7 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c12/i27); /de (c1/i6); /lisbon (c1/i5); /de/stuttgart/hohenheim-love-plane (c1/i2); /de/vienna/giant-sequoias-of-potzleinsdorfer-schlosspark (c1/i2)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'comfort tree niagara' (i2, p75)
    - '# system role you operate as a precision' (i1, p6)
    - '200 old tree trace' (i1, p54)
    - '2023 euwallacea validus over 20 families' (i1, p96)
    - 'ancient roman trees' (i1, p68)
    - 'canary island dates' (i1, p99)

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 465 |
| Clicks | 17 |
| Pages that got at least one impression | 247 |
| Impressions on the proven cities | 278 |

- 327 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3073 trees Google may index, 824 kept out for lacking a photo and an exact pin, 6952 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 96 | 1 | 2 | 0.02 | 0 |
| Not yet rich | 59 | 1 | 2 | 0.03 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| sequoia-national-park | 0 | 34 | 0.0% | 71.1 | 0.4% | general sherman tree (i6, p75) |
| munich | 0 | 13 | 0.0% | 5.3 | 6.4% | - |

- Plus 257 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

## Weekly analysis 2026-10-26

Thirteenth weekly analysis. Compares 10-19 to 10-25 with 10-12 to 10-18, read
from the 10-25 daily entry. Google's last three days are still filling, so
its row can move. Volumes are small; nothing below is a trend unless it says so.

**Scorecard**

| Week | Impressions | Clicks | CTR | Avg position | Visitors (GA, new) | Directions (web) | App-CTA | App downloads (first-time) | Android waitlist total | Readers' contributions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10-12 to 10-18 | 317 | 12 | 3.8% | 30 to 53 | 25 | 0 (7d) | 14 (7d) | 18 | n/a | 4 |
| 10-19 to 10-25 | 296 (partial) | 10 | 3.4% | 26 to 59 | 85 | not in the entry (8 ever) | not in the entry (117 ever) | 38 | 42 (20 this week) | 11 |

Bing, same weeks: 523 impressions and 23 clicks, then 554 and 24 (4.3% CTR);
index 2,775 to 3,428 pages. Device split and per-visit ratios are not in the
10-25 entry (the audience section failed that day), so no ratio is claimed.
App return: 9 of 13 phones back within 30 days against 6 of 15.

**What moved:**
1. Google is flat at the floor for a fourth week: about 42 impressions a day,
   10 clicks. Position is all over (26 to 59) on single-digit clicks, which is
   noise.
2. Visitors jumped, from one day: 10-24 had 41 people against 3 to 15 on the
   other days, with 23 app downloads and 15 Android waitlist signups that
   day. The same day wilder.pt first linked us (12 visits, 8 people in the
   week, 5th backlink) and Facebook sent 11 visits. Lisbon (45 pageviews, 20
   people), Porto and Sintra lead the pages, so this is Portuguese interest.
3. Bing again out-clicks Google, 24 against 10, and its index keeps growing.
4. Readers gave more: contributions 4 to 11, accounts 3 to 16, trees collected
   1 to 13, saved 7 to 19, 16 app photos. Mostly one weekend spike; small
   numbers.
5. The machine: 6 runs of about 28 minutes in the last day, 0 trees. Night
   runs are mostly re-checking state; the digest says no new outreach
   contacts in two days.

**Suggestions, ranked:**
1. **[run]** Source nature magazines and websites per focus country (the
   Wilder model) into the outreach database. One placed link produced the
   week's only spike (41 visitors, 23 downloads, 15 signups in a day), while
   the digest shows nature 0 ready to mail and no new contacts in two days.
   Start with Portugal-adjacent and Spain/Italy titles; drafts only.
2. **[sessie]** Fix two broken digest blocks seen in the 10-25 entry:
   `audience_section failed (name 'MARKERS' is not defined)` and App Store
   downloads "unreadable (timed out)". Without the first, device splits and
   per-visit ratios cannot be kept on this scorecard.
3. **[run]** Portugal depth: Lisbon, Porto and Sintra drew 71 of 474
   pageviews. Check each has photographs, access lines and a visible way to
   save a tree, so the next link-driven day converts; Porto's ambassador
   request is already open.
4. **[run]** Bing converts, so give its winning pages (oldest tree china
   c8/i4 p12, fig tree in square alicante c2, big trees of quebec city c2,
   queen square bristol, oak tree in zurich) a photograph, register link and
   access line. Still the same call as last week.
5. **[FOR HIDDE]** Android waitlist is 42 total, 20 in this week, against 38
   iOS downloads. Is an Android build still phase 2, or does that demand move
   it? A decision to note, not urgent.

**Watch next week:** whether visitors stay above about 10 a day without a
new link (if not, 10-24 was a one-off), Google days above 100 impressions,
and the Sequoia / Sherman page (31 impressions, position 73.6 again).

## 2026-10-25 (previous UTC day)

**Today: 4 android waitlist signups arrived yesterday (42 total); 3 accounts were opened yesterday (45 total).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 85 | 25 |
| ... of which from search | every search engine | 8 | 6 |
| ... from Google | Google's recovery | 2 | 1 |
| ... from Bing | Bing | 0 | 1 |
| App downloads (first-time) | people | 38 | 18 |
| New accounts | people | 16 | 3 |
| Phones back within 30 days | people who stay | 9 of 13 | 6 of 15 |
| Trees saved to Want to go | intent | 19 | 7 |
| Trees collected | goal 1: stood at a tree | 13 | 1 |
| Readers' contributions | data: trees, photos, corrections, votes | 11 | 4 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Ambassador requests, open** (3; each stays here until the badge is granted with `python3 scripts/ambassador.py --grant`)

| Asked | Place | From | Our mail with the questions | Waiting on |
|---|---|---|---|---|
| 2026-10-24 | **Porto** | the app | sent 2026-10-24 | their answer, then your yes |
| 2026-10-22 | **Bucaco** | /bucaco | sent 2026-10-22 | their answer, then your yes |
| 2026-10-20 | **New York** | /new-york | sent 2026-10-20 | their answer, then your yes |

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 10-19 | 10-20 | 10-21 | 10-22 | 10-23 | 10-24 | 10-25 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 4 | 6 | 3 | 11 | 15 | 41 | 11 | **91** |
| New accounts | 2 | 1 | 1 | 2 | 1 | 6 | 3 | **16** |
| Saves | 0 | 0 | 0 | 13 | 0 | 6 | 0 | **19** |
| Android waitlist | 0 | 0 | 0 | 0 | 1 | 15 | 4 | **20** |
| App downloads | 1 | 3 | 3 | 2 | 5 | 23 | 0 | **37** |
| Trees sent | 1 | 1 | 0 | 0 | 0 | 0 | 0 | **2** |
| Feedback | 0 | 6 | 0 | 0 | 0 | 0 | 0 | **6** |
| Ambassador asks | 0 | 1 | 0 | 1 | 0 | 1 | 0 | **3** |
| App photos | 0 | 7 | 5 | 3 | 0 | 0 | 1 | **16** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Waiting for you** (what the runs left for you since 2026-10-25)

- 375 email addresses ready to mail (archive 0, nature 0, guide 0, press 270, source 73, council 14, society 6, other 5, tourism 4, garden 3); **the night run found no new contacts in two days**
- the ambassador mail to Luisa Carta (Sardinia)
- 3 archive mails in drafts/batch-archive-2026-10-25-preview.md
- the digest page now opens with how many reader photographs he has not seen and links photos.html (scripts/reader_photos.py: every shared app photograph, new trees and existing ones, unseen first).
- 3 Reddit replies in drafts/batch-community-preview.md (the r/lisbon Santa Iria photo reply is the one that matters: asks permission to use the photograph).

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| 2026-10-22 | The Weeping Cedar of the Vallée-aux-Lo | Chatenay-Malabry | - | publish | ja, ziet er goed uit |
| 2026-10-20 | The Weeping Fig of Campo Santana | Lisbon | - | publish | ja, eens |
| 2026-10-20 | Dragon Tree in Lisbon | - | - | publish | ja, eens |
| 2026-10-20 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | ja, eens |
| 2026-10-20 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | ja, eens (zelfde boom, alle vier eens 2026-10-22) |
| 2026-10-20 | The Paperbark of Jardim Constantino | Lisbon | - | publish | ja, eens |
| 2026-10-20 | The Weeping Fig of Campo Santana | Lisbon | - | publish | ja, eens (zelfde boom, alle vier eens 2026-10-22) |
| 2026-10-20 | Dragon Tree in Lisbon | - | - | publish | ja, eens (zelfde boom, alle vier eens 2026-10-22) |
| 2026-10-19 | The Schönberg Beech above Ebringen | Freiburg | - | publish | - |
| 2026-10-19 | European Beech in Freiburg | - | - | publish | - |

0 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**Searched yesterday:** lisb (2 times), galicia, lis, lisbon, tera, van.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-16 | 3 | 73 | 4.1% | 53.0 |
| 10-17 | 2 | 62 | 3.2% | 44.6 |
| 10-18 | 2 | 53 | 3.8% | 42.9 |
| 10-19 | 1 | 48 | 2.1% | 59.2 |
| 10-20 | 3 | 39 | 7.7% | 26.3 |
| 10-21 | 0 | 43 | 0.0% | 39.2 |
| 10-22 | 2 | 45 | 4.4% | 51.8 |
| 10-23 | 0 | 48 | 0.0% | 55.1 |
| 10-24 | 1 | 24 | 4.2% | 43.2 |
| 10-25 *partial* | 3 | 49 | 6.1% | 47.8 |
| **window** | **17** | **484** | **3.5%** | |
- Top queries (10d): # system role you operate as a precision (i1, p6); 2023 euwallacea validus over 20 families (i1, p96); 43 rue buffon 75005 paris (i1, p73); 600 year old ginkgo tree jeonju (i1, p55); ancient roman trees (i1, p68)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-18 | 50 | 2 | 4.0% |
| 10-19 | 82 | 0 | 0.0% |
| 10-20 | 91 | 9 | 9.9% |
| 10-21 | 103 | 2 | 1.9% |
| 10-22 | 77 | 2 | 2.6% |
| 10-23 | 82 | 5 | 6.1% |
| 10-24 | 69 | 4 | 5.8% |
| **7 days** | **554** | **24** | **4.3%** |
- Week before: 523 impressions, 23 clicks. No Bing demotion in sight.
- Top Bing queries: oldest tree china (c8/i4, p12); fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); how old are the trees in queen square bristol (c1/i4, p3); oak tree in zurich (c1/i4, p2); trees in the plaza dus burgos seville (c1/i3, p5); berlin tree (c1/i2, p1); oldest tree in belfast (c1/i2, p1)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

**Monday: the slow tables.** They rarely change a day's decision, so they come once a week.

**Website actions, ever** (the events table begins 2026-08-01, when the funnel was repaired; a zero has never fired at all)

| Action | Ever |
|---|---:|
| signin-open | 418 |
| app-cta | 117 |
| search-home | 70 |
| home-fav | 52 |
| waitlist-submit | 22 |
| app-open | 21 |
| signin-oauth | 19 |
| home-country | 18 |
| signin-done | 13 |
| home-dir-city | 9 |
| search-bar | 9 |
| directions | 8 |
| search-bar-m | 6 |
| search-explore | 4 |
| home-dir-species | 2 |
| ambassador-request | 2 |
| app-page-badge | 2 |
| home-dir-collection | 2 |
| home-dir-tree | 2 |
| save | 2 |
| home-species | 1 |
| sponsor-open | 1 |
| signin-link-sent | 0 |
| worthit-not worth it | 0 |
| worthit-worth it | 0 |
| **all** | **800** |

**App events, ever** (measured since 2026-08-30)

| What | Ever |
|---|---:|
| app_open | 494 |
| tab | 463 |
| tree_opened | 1817 |
| directions | 58 |
| tree_saved | 46 |
| tree_visited | 35 |
| sighting_recorded | 90 |
| sync_skipped | 0 |
| sync_failed | 0 |
| location | 50 |
| **all** | **3053** |

**What readers told us** (7 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 10-19 | ED90210D-8ED3-4C85-8AF7-F75F6F34FF | tree sent in | - | 4d30 | - |
| 10-20 | New York | ambassador request | - | e5bb | - |
| 10-20 | lis_027 (The Moreton Bay Fig of Ja | worth it | - | f58e | - |
| 10-20 | lis_026 (The Paperbark of Jardim C | worth it | - | f58e | - |
| 10-20 | lis_015 (The Weeping Fig of Campo  | report | wrong location | f58e | changed |
| 10-20 | lis_015 (The Weeping Fig of Campo  | report detail | 49 chars | f58e | changed |
| 10-20 | The Weeping Fig of Campo Santana | correction sent in | 169 chars, read it in the database | f58e | changed |
| 10-20 | 9B10AE23-BBA4-4AF8-A9AE-95B93ABA92 | tree sent in | 154 chars, read it in the database | f58e | - |
| 10-20 | lis_015 (The Weeping Fig of Campo  | worth it | - | f58e | - |
| 10-22 | Bucaco | ambassador request | - | 061d | - |
| 10-24 | Porto | ambassador request | - | 77c1 | - |

- 7 of the other 11 came from one account (f58e), which is one person rather than a pattern.

**App Store downloads**
- Unreadable (The read operation timed out)

**Bing's index** (pages crawled and in index, Bing Webmaster Tools)

| Day | Pages crawled | Pages in index |
|---|---:|---:|
| 10-18 | 233 | 2775 |
| 10-19 | 204 | 2863 |
| 10-20 | 366 | 2946 |
| 10-21 | 280 | 3055 |
| 10-22 | 458 | 3242 |
| 10-23 | 304 | 3242 |
| 10-24 | 348 | 3428 |
- In index the week before: 2775.

audience_section: failed today (name 'MARKERS' is not defined).

**Google Analytics** (last 7 days, visitors who accepted cookies)

| Day | People | New | Returning | Visits | Pageviews | Engaged visits |
|---|---:|---:|---:|---:|---:|---:|
| 10-19 | 4 | 3 | 1 | 5 | 23 | 4 |
| 10-20 | 6 | 6 | 0 | 6 | 9 | 6 |
| 10-21 | 3 | 2 | 1 | 5 | 18 | 3 |
| 10-22 | 11 | 10 | 1 | 15 | 84 | 12 |
| 10-23 | 15 | 14 | 1 | 23 | 58 | 13 |
| 10-24 | 41 | 40 | 1 | 53 | 220 | 34 |
| 10-25 | 11 | 10 | 1 | 20 | 62 | 14 |
| **window** | | **85** | | **127** | **474** | **86** |
- People per day are not summed: one person on two days is one person, and GA counts them once per day.
- Coming back (28 days): 19 returning against 110 new, 15% of the people GA saw.

| Page | Pageviews | People |
|---|---:|---:|
| / | 81 | 44 |
| /lisbon | 45 | 20 |
| /explore | 20 | 8 |
| /porto | 15 | 7 |
| /contribute | 12 | 6 |
| /about | 11 | 6 |
| /portugal | 11 | 5 |
| /sintra | 11 | 2 |
| /cities | 9 | 6 |
| /countries | 8 | 2 |

| Came from | Visits | People |
|---|---:|---:|
| (direct) / (none) | 82 | 55 |
| wilder.pt / referral | 12 | 8 |
| google / organic | 9 | 2 |
| facebook.com / referral | 7 | 7 |
| m.facebook.com / referral | 4 | 4 |
| duckduckgo / organic | 3 | 2 |
| ecosia.org / organic | 3 | 3 |
| (not set) / (not set) | 2 | 2 |
- GA sees only visitors who pressed Accept on the cookie bar; read it as a sample.

Backlinks (watched pages):
| Site | Links to | rel | First seen |
|---|---|---|---|
| getlisbon.com | /lisbon | followed | 2026-09-08 |
| getlisbon.com | /pt/lisbon | followed | 2026-09-08 |
| www.baumkunde.de | /copenhagen | followed | 2026-09-26 |
| www.baumkunde.de | /rogalin/russ-oak | followed | 2026-09-26 |
| wilder.pt | / | followed | 2026-10-24 |
5 linking page(s), 5 followed. Checked by fetching the page: a link with rel="noreferrer" never appears in the referrer table, so these two lines measure different things and neither replaces the other. Unknown links stay a manual read of Search Console's Links report. This run read 12 of 12 fetched (0 unreachable), out of 28 watched pages.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-25T06:54 | 3.2 | 0 | 4 | 0 | - |
| 10-25T08:53 | 3.9 | 0 | 4 | 0 | - |
| 10-25T12:30 | 4.5 | 0 | 4 | 0 | - |
| 10-25T14:03 | 4.8 | 0 | 4 | 0 | - |
| 10-25T16:50 | 4.4 | 0 | 4 | 0 | - |
| 10-25T18:40 | 7.0 | 0 | 4 | 0 | - |
| **6 runs** | **28** | **0** | **24** | | |

- 6 of 6 produced no trees; last build that went live: 1h ago.

**What they made**

- Record when each page last changed
- Night run, third attempt: Baltimore scouting retried, still stalled, logged
- Night run, second attempt: nothing to ship, logged
- Night run: quiet window, Stirling scouting retried, logged
- Night run: forty-first attempt, state re-checked, log
- Night run: fortieth attempt, state re-checked, log
- Night run: outreach rung, 3 Reddit replies previewed, log
- Night run: thirty-ninth attempt, state re-checked, log
- Night run: thirty-eighth attempt, state re-checked, log
- Night run: thirty-seventh attempt, state re-checked, log
- Night run: thirty-sixth attempt, state re-checked, log
- Night run: thirty-fifth attempt, state re-checked, log
- Night run: thirty-fourth attempt, state re-checked, log
- Night run: community lane, three Reddit replies drafted, log

Machine: 9 chain attempts yesterday, 7 got real work time (~40 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c9/i22); /leiden/beets-beech-of-the-burcht (c2/i2); /de (c1/i6); /lisbon (c1/i3); /de/stuttgart/hohenheim-love-plane (c1/i2)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'comfort tree niagara' (i2, p75)
    - '# system role you operate as a precision' (i1, p6)
    - '2023 euwallacea validus over 20 families' (i1, p96)
    - 'ancient roman trees' (i1, p68)
    - 'big macadamia' (i1, p100)
    - 'canary island dates' (i1, p99)

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 520 |
| Clicks | 17 |
| Pages that got at least one impression | 269 |
| Impressions on the proven cities | 316 |

- 314 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3059 trees Google may index, 824 kept out for lacking a photo and an exact pin, 6925 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 95 | 1 | 2 | 0.02 | 0 |
| Not yet rich | 59 | 1 | 2 | 0.03 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| sequoia-national-park | 0 | 31 | 0.0% | 73.6 | 0.4% | general sherman tree (i3, p72) |
| munich | 0 | 13 | 0.0% | 5.3 | 6.4% | - |
| tenerife | 0 | 10 | 0.0% | 53.4 | 0.4% | drachenbaum auf teneriffa (i1, p96) |

- Plus 256 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, berlin, rome.

## 2026-10-24 (previous UTC day)

**Today: 4 android waitlist signups arrived today (42 total); an ambassador request for Porto arrived yesterday (48 total); 2 accounts were opened today (44 total).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 77 | 23 |
| ... of which from search | every search engine | 9 | 5 |
| ... from Google | Google's recovery | 2 | 1 |
| ... from Bing | Bing | 0 | 1 |
| App downloads (first-time) | people | 38 | 18 |
| New accounts | people | 13 | 4 |
| Phones back within 30 days | people who stay | 8 of 12 | 6 of 15 |
| Trees saved to Want to go | intent | 23 | 3 |
| Trees collected | goal 1: stood at a tree | 13 | 1 |
| Readers' contributions | data: trees, photos, corrections, votes | 13 | 2 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| Day | Visitors | New accounts | Saves | Android waitlist | App downloads | Trees sent | Feedback | Ambassador asks | App photos | Tree notes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10-18 | 2 | 0 | 4 | 0 | 1 | 0 | 2 | 0 | 4 | 0 |
| 10-19 | 4 | 2 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 10-20 | 6 | 1 | 0 | 0 | 3 | 1 | 6 | 1 | 8 | 0 |
| 10-21 | 3 | 1 | 0 | 0 | 3 | 0 | 0 | 0 | 5 | 0 |
| 10-22 | 11 | 2 | 13 | 0 | 2 | 0 | 0 | 1 | 3 | 0 |
| 10-23 | 15 | 1 | 0 | 1 | 5 | 0 | 0 | 0 | 0 | 0 |
| 10-24 | 41 | 6 | 6 | 15 | 23 | 0 | 0 | 1 | 0 | 0 |
| **7 days** | **82** | **13** | **23** | **16** | **38** | **2** | **8** | **3** | **20** | **0** |

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Waiting for you** (what the runs left for you since 2026-10-24)

- 3 Reddit replies in drafts/batch-community-preview.md (the r/lisbon Santa Iria photo reply is the one that matters: asks permission to use the photograph).
- paste supabase/tree-notes.sql to clear the Postbox check.
- Postbox check fails only because supabase/tree-notes.sql has never been pasted (sqlcheck: table tree_notes).
- reply drafted in drafts/reply-james-kearney-2026-10-24.md; he says more photos follow.
- replies for the five new comments are in drafts/reddit-sicily-replies-2026-10-24.md.
- next build carries this fix.

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| 2026-10-22 | The Weeping Cedar of the Vallée-aux-Lo | Chatenay-Malabry | - | publish | ja, ziet er goed uit |
| 2026-10-20 | The Weeping Fig of Campo Santana | Lisbon | - | publish | ja, eens |
| 2026-10-20 | Dragon Tree in Lisbon | - | - | publish | ja, eens |
| 2026-10-20 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | ja, eens |
| 2026-10-20 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | ja, eens (zelfde boom, alle vier eens 2026-10-22) |
| 2026-10-20 | The Paperbark of Jardim Constantino | Lisbon | - | publish | ja, eens |
| 2026-10-20 | The Weeping Fig of Campo Santana | Lisbon | - | publish | ja, eens (zelfde boom, alle vier eens 2026-10-22) |
| 2026-10-20 | Dragon Tree in Lisbon | - | - | publish | ja, eens (zelfde boom, alle vier eens 2026-10-22) |
| 2026-10-19 | The Schönberg Beech above Ebringen | Freiburg | - | publish | - |
| 2026-10-19 | European Beech in Freiburg | - | - | publish | - |
| 2026-10-18 | The Tulip Tree of Cantonspark | - | - | lead | - |
| 2026-10-18 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | Al besproken, akkoord |
| 2026-10-18 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | Al besproken, akkoord |
| 2026-10-18 | The Paperbark of Jardim Constantino | Lisbon | - | publish | Al besproken, akkoord |
| 2026-10-18 | A tree in Baarn | - | - | lead | - |

0 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**Searched yesterday:** lis (7 times), porto (5 times), lisboa (2 times), lisbon (2 times), coimbra, hung, made, madrid, moffat, new, olive, por, portugal, sintr, slo, valen, valencia.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-15 | 2 | 40 | 5.0% | 37.0 |
| 10-16 | 3 | 73 | 4.1% | 53.0 |
| 10-17 | 2 | 62 | 3.2% | 44.6 |
| 10-18 | 2 | 53 | 3.8% | 42.9 |
| 10-19 | 1 | 48 | 2.1% | 59.2 |
| 10-20 | 3 | 39 | 7.7% | 26.3 |
| 10-21 | 0 | 43 | 0.0% | 39.2 |
| 10-22 | 2 | 45 | 4.4% | 51.8 |
| 10-23 | 0 | 48 | 0.0% | 55.1 |
| 10-24 | 1 | 24 | 4.2% | 43.2 |
| 10-25 *partial* | 1 | 15 | 6.7% | 46.6 |
| **window** | **17** | **490** | **3.5%** | |
- Top queries (10d): # system role you operate as a precision (i1, p6); 2023 euwallacea validus over 20 families (i1, p96); 43 rue buffon 75005 paris (i1, p73); amsterdam trees (i1, p81); ancient roman trees (i1, p68)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-18 | 50 | 2 | 4.0% |
| 10-19 | 82 | 0 | 0.0% |
| 10-20 | 91 | 9 | 9.9% |
| 10-21 | 103 | 2 | 1.9% |
| 10-22 | 77 | 2 | 2.6% |
| 10-23 | 82 | 5 | 6.1% |
| 10-24 | - | - | 0.0% |
| **7 days** | **485** | **20** | **4.1%** |
- Week before: 523 impressions, 23 clicks. No Bing demotion in sight.
- Top Bing queries: oldest tree china (c8/i4, p12); fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); how old are the trees in queen square bristol (c1/i4, p3); oak tree in zurich (c1/i4, p2); trees in the plaza dus burgos seville (c1/i3, p5); french trees found in paris (c1/i2, p6); ancient trees in wiesbaden germany (c1/i2, p6)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-24T17:09 | 3.6 | 0 | 4 | 0 | - |
| 10-24T20:04 | 5.1 | 0 | 4 | 0 | - |
| 10-24T23:44 | 5.7 | 0 | 7 | 0 | - |
| 10-24T23:56 | 4.0 | 0 | 4 | 0 | - |
| 10-25T03:04 | 3.8 | 0 | 4 | 0 | - |
| 10-25T06:54 | 3.2 | 0 | 4 | 0 | - |
| 10-25T08:53 | 3.9 | 0 | 4 | 0 | - |
| 10-25T12:30 | 4.5 | 0 | 4 | 0 | - |
| 10-25T14:03 | 4.8 | 0 | 4 | 0 | - |
| 10-25T16:50 | 4.4 | 0 | 4 | 0 | - |
| **10 runs** | **43** | **0** | **43** | | |

- 10 of 10 produced no trees; last build that went live: 1h ago.

**What they made**

- Night run: forty-first attempt, state re-checked, log
- Night run: fortieth attempt, state re-checked, log
- Night run: outreach rung, 3 Reddit replies previewed, log
- Night run: thirty-ninth attempt, state re-checked, log
- Night run: thirty-eighth attempt, state re-checked, log
- Night run: thirty-seventh attempt, state re-checked, log
- Night run: thirty-sixth attempt, state re-checked, log
- Night run: thirty-fifth attempt, state re-checked, log
- Night run: thirty-fourth attempt, state re-checked, log
- Night run: community lane, three Reddit replies drafted, log
- Night run: thirty-third attempt, state re-checked, log
- Night run: thirty-second attempt, state re-checked, log
- Fresh-eyes review: 4 finding(s)
- Fresh-eyes review: 1 finding(s)

Machine: 9 chain attempts yesterday, 9 got real work time (~83 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c8/i23); /leiden/beets-beech-of-the-burcht (c2/i2); /app (c1/i11); /de (c1/i6); /de/stuttgart/hohenheim-love-plane (c1/i2)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'comfort tree niagara' (i2, p75)
    - '# system role you operate as a precision' (i1, p6)
    - '2023 euwallacea validus over 20 families' (i1, p96)
    - 'ancient roman trees' (i1, p68)
    - 'big macadamia' (i1, p100)
    - 'canary island dates' (i1, p99)

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 550 |
| Clicks | 17 |
| Pages that got at least one impression | 280 |
| Impressions on the proven cities | 333 |

- 350 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3057 trees Google may index, 825 kept out for lacking a photo and an exact pin, 6977 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 68 | 2 | 3 | 0.04 | 0 |
| Not yet rich | 41 | 0 | 0 | 0.00 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| sequoia-national-park | 0 | 32 | 0.0% | 73.0 | 0.4% | general sherman tree (i3, p72) |
| munich | 0 | 13 | 0.0% | 5.3 | 6.4% | - |
| brisbane | 0 | 10 | 0.0% | 79.8 | 0.4% | the big macadamia nut (i7, p93) |

- Plus 256 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

## 2026-10-23 (previous UTC day)

**Today: an android waitlist signup arrived yesterday (23 total); an account was opened yesterday (36 total).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 40 | 20 |
| ... of which from search | every search engine | 10 | 3 |
| ... from Google | Google's recovery | 3 | 0 |
| ... from Bing | Bing | 0 | 1 |
| App downloads (first-time) | people | 15 | 17 |
| New accounts | people | 8 | 4 |
| Phones back within 30 days | people who stay | 7 of 9 | 6 of 16 |
| Trees saved to Want to go | intent | 17 | 3 |
| Trees collected | goal 1: stood at a tree | 13 | 1 |
| Readers' contributions | data: trees, photos, corrections, votes | 12 | 2 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**What readers gave us, and it went live**

| Day | Reader | Tree | Where | What | Page |
|---|---|---|---|---|---|
| 10-22 | A | The Weeping Cedar of the Vallée-aux-Loups (Cèdre pleureur) | Chatenay-Malabry | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/chatenay-malabry/weeping-cedar-of-the-vallee-aux-loups-cedre-pleureur) |
- All from one reader (reader A 1).

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| 2026-10-22 | The Weeping Cedar of the Vallée-aux-Lo | Chatenay-Malabry | - | publish | ja, ziet er goed uit |
| 2026-10-20 | The Weeping Fig of Campo Santana | Lisbon | - | publish | ja, eens |
| 2026-10-20 | Dragon Tree in Lisbon | - | - | publish | ja, eens |
| 2026-10-20 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | ja, eens |
| 2026-10-20 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | ja, eens (zelfde boom, alle vier eens 2026-10-22) |
| 2026-10-20 | The Paperbark of Jardim Constantino | Lisbon | - | publish | ja, eens |
| 2026-10-20 | The Weeping Fig of Campo Santana | Lisbon | - | publish | ja, eens (zelfde boom, alle vier eens 2026-10-22) |
| 2026-10-20 | Dragon Tree in Lisbon | - | - | publish | ja, eens (zelfde boom, alle vier eens 2026-10-22) |
| 2026-10-19 | The Schönberg Beech above Ebringen | Freiburg | - | publish | - |
| 2026-10-19 | European Beech in Freiburg | - | - | publish | - |
| 2026-10-18 | The Tulip Tree of Cantonspark | - | - | lead | - |
| 2026-10-18 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | Al besproken, akkoord |
| 2026-10-18 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | Al besproken, akkoord |
| 2026-10-18 | The Paperbark of Jardim Constantino | Lisbon | - | publish | Al besproken, akkoord |
| 2026-10-18 | A tree in Baarn | - | - | lead | - |

0 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**Searched yesterday:** porto (2 times), amsterda, lisboa, ragusa, seattle.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-14 | 1 | 39 | 2.6% | 36.9 |
| 10-15 | 2 | 40 | 5.0% | 37.0 |
| 10-16 | 3 | 73 | 4.1% | 53.0 |
| 10-17 | 2 | 62 | 3.2% | 44.6 |
| 10-18 | 2 | 53 | 3.8% | 42.9 |
| 10-19 | 1 | 48 | 2.1% | 59.2 |
| 10-20 | 3 | 39 | 7.7% | 26.3 |
| 10-21 | 0 | 43 | 0.0% | 39.2 |
| 10-22 | 2 | 45 | 4.4% | 51.8 |
| 10-23 *partial* | 0 | 41 | 0.0% | 57.6 |
| **window** | **16** | **483** | **3.3%** | |
- Top queries (10d): # system role you operate as a precision (i1, p6); 2023 euwallacea validus over 20 families (i1, p96); 43 rue buffon 75005 paris (i1, p73); amsterdam trees (i1, p81); ancient trees (i1, p84)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-15 | 78 | 8 | 10.3% |
| 10-16 | 70 | 2 | 2.9% |
| 10-17 | 57 | 3 | 5.3% |
| 10-18 | 50 | 2 | 4.0% |
| 10-19 | 82 | 0 | 0.0% |
| 10-20 | - | - | 0.0% |
| 10-21 | - | - | 0.0% |
| **7 days** | **337** | **15** | **4.5%** |
- Week before: 590 impressions, 17 clicks. No Bing demotion in sight.
- Top Bing queries: fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); oak tree in zurich (c1/i4, p2); how old are the trees in queen square bristol (c1/i4, p3); trees in the plaza dus burgos seville (c1/i3, p5); husalle lindens copenhagen (c1/i2, p3); french trees found in paris (c1/i2, p6); remarkable trees copenhagen (c1/i2, p4)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-23T09:01 | 8.8 | 0 | 9 | 0 | - |
| 10-23T14:28 | 7.6 | 0 | 8 | 0 | - |
| 10-23T14:37 | 9.7 | 0 | 9 | 0 | - |
| 10-23T18:45 | 8.6 | 0 | 8 | 1 | - |
| 10-23T19:44 | 10.5 | 0 | 3 | 0 | - |
| 10-23T22:50 | 7.7 | 0 | 2 | 0 | - |
| 10-24T02:55 | 5.5 | 0 | 3 | 0 | - |
| **7 runs** | **58** | **0** | **42** | | |

- 7 of 7 produced no trees; 1 to 1 commands refused per run; last build that went live: 1h ago.

**What they made**

- Night run 10-24 restart: nothing publishable, log
- Night run 10-24: nothing publishable, log
- Photographs readers sent, queued for a look; vouched ones live
- Night run 10-23 sixteenth attempt: nothing publishable, log
- Night run 10-23 fifteenth attempt: nothing publishable, iOS CI hang noted, log
- Night run 10-23 fourteenth attempt: photo lane exhausted, log
- Night run 10-23 thirteenth attempt: nothing publishable, log
- Night run 10-23 twelfth attempt: nothing publishable, log
- Night run 10-23 eleventh attempt: four photo candidates judged, none approved, log
- Night run 10-23 tenth attempt: nothing publishable, log
- Night run 10-23 ninth attempt: nothing publishable while supply is paused, log
- Night run 10-23 eighth attempt: inbox empty, photo sweep found nothing, log
- Night run 10-23 seventh attempt: nothing publishable while supply is paused, log
- Night run 10-23 sixth attempt: photo lane checked, nothing to approve, log

**Photographs the night run approved** (6; the last column undoes one)

| Day | Tree | Where | Overrule |
|---|---|---|---|
| 10-22 | The Banyan Tree of City Botanic Gardens | Brisbane | `photo_apply.py hold bne_004` |
| 10-22 | The Bur Oak of Harms Woods | Chicago | `photo_apply.py hold chi_023` |
| 10-22 | The Jahn Oak of Offenbach | Frankfurt | `photo_apply.py hold frk_021` |
| 10-22 | The Oak of Babelsberger Strasse | Potsdam | `photo_apply.py hold pot_017` |
| 10-22 | The Centennial Tree of the Presidio | San Francisco | `photo_apply.py hold sfo_011` |
| 10-22 | The Yamaki Pine | Washington DC | `photo_apply.py hold wdc_025` |

Machine: 7 chain attempts yesterday, 7 got real work time (~78 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c7/i22); /leiden/beets-beech-of-the-burcht (c2/i2); /app (c1/i11); /de (c1/i6); /seville (c1/i4)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - '# system role you operate as a precision' (i1, p6)
    - '2023 euwallacea validus over 20 families' (i1, p96)
    - 'big macadamia' (i1, p100)
    - 'canary island dates' (i1, p99)
    - 'chapina garden' (i1, p13)

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 548 |
| Clicks | 16 |
| Pages that got at least one impression | 285 |
| Impressions on the proven cities | 337 |

- 327 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3053 trees Google may index, 828 kept out for lacking a photo and an exact pin, 6417 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 331 | 17 | 29 | 0.09 | 2 |
| Not yet rich | 270 | 8 | 24 | 0.09 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| sequoia-national-park | 0 | 34 | 0.0% | 72.5 | 0.4% | general sherman tree (i3, p72) |
| munich | 0 | 14 | 0.0% | 5.1 | 6.9% | - |
| brisbane | 0 | 10 | 0.0% | 79.8 | 0.4% | the big macadamia nut (i7, p93) |

- Plus 256 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

## 2026-10-22 (previous UTC day)

**Today: 1 feedback report arrived yesterday (47 total); an account was opened yesterday (35 total).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 28 | 18 |
| ... of which from search | every search engine | 8 | 3 |
| ... from Google | Google's recovery | 3 | 0 |
| ... from Bing | Bing | 0 | 1 |
| App downloads (first-time) | people | 14 | 16 |
| New accounts | people | 7 | 4 |
| Phones back within 30 days | people who stay | 7 of 10 | 6 of 17 |
| Trees saved to Want to go | intent | 19 | 1 |
| Trees collected | goal 1: stood at a tree | 12 | 4 |
| Readers' contributions | data: trees, photos, corrections, votes | 12 | 2 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Trees readers sent, for you to inspect** (1 you have not looked at; ours left out)

| Judged | Reader | Tree | Where | Species | Their girth | Our verdict | Page |
|---|---|---|---|---|---:|---|---|
| 2026-10-22 | A | The Weeping Cedar of the Vallée-aux-Loups | Chatenay-Malabry | - | - | publish | [cma_001](https://ancienttrees.app/chatenay-malabry/weeping-cedar-of-the-vallee-aux-loups-cedre-pleureur) |
- All from one reader (reader A 1).
- Photographs and the readers' own words: `python3 scripts/inspect_readers.py` (a local page, never in this public file). Your answer goes in with `python3 scripts/judgement.py --feedback <id> "..."`.

**What readers gave us, and it went live**

| Day | Reader | Tree | Where | What | Page |
|---|---|---|---|---|---|
| 10-21 | B | The Moreton Bay Fig of the Mendoubia | Tangier | a reader's photograph, published | [live](https://ancienttrees.app/tangier/moreton-bay-fig-of-the-mendoubia) |
| 10-21 | C | The Dragon Tree of the Goethe-Institut Garden | Lisbon | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/lisbon/dragon-tree-of-the-goethe-institut-garden) |
| 10-22 | A | The Weeping Cedar of the Vallée-aux-Loups (Cèdre pleureur) | Chatenay-Malabry | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/chatenay-malabry/weeping-cedar-of-the-vallee-aux-loups-cedre-pleureur) |
- From 3 readers: reader A 1, reader B 1, reader C 1.

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| 2026-10-22 | The Weeping Cedar of the Vallée-aux-Lo | Chatenay-Malabry | - | publish | - |
| 2026-10-20 | The Weeping Fig of Campo Santana | Lisbon | - | publish | ja, eens |
| 2026-10-20 | Dragon Tree in Lisbon | - | - | publish | ja, eens |
| 2026-10-20 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | ja, eens |
| 2026-10-20 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | ja, eens (zelfde boom, alle vier eens 2026-10-22) |
| 2026-10-20 | The Paperbark of Jardim Constantino | Lisbon | - | publish | ja, eens |
| 2026-10-20 | The Weeping Fig of Campo Santana | Lisbon | - | publish | ja, eens (zelfde boom, alle vier eens 2026-10-22) |
| 2026-10-20 | Dragon Tree in Lisbon | - | - | publish | ja, eens (zelfde boom, alle vier eens 2026-10-22) |
| 2026-10-19 | The Schönberg Beech above Ebringen | Freiburg | - | publish | - |
| 2026-10-19 | European Beech in Freiburg | - | - | publish | - |
| 2026-10-18 | The Tulip Tree of Cantonspark | - | - | lead | - |
| 2026-10-18 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | Al besproken, akkoord |
| 2026-10-18 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | Al besproken, akkoord |
| 2026-10-18 | The Paperbark of Jardim Constantino | Lisbon | - | publish | Al besproken, akkoord |
| 2026-10-18 | A tree in Baarn | - | - | lead | - |

0 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**Searched yesterday:** barcelona, leeu, n, por, portugal, prah.

**App crashes** (last 7 days, store builds; MetricKit, a sample)

| Crashes | Kind | Build | Where | Phones | Last | Fix |
|---:|---|---|---|---:|---|---|
| 4 | crash | 1.0.2 (20) | Swift runtime failure: Index out of range < static MyVotes.treeId(_:) (WorthIt.swift:84) < MyVotes.load(account:) (WorthIt.swift:103) | 1 | 2026-10-16 | fixed in build 35, released; contained server-side |

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-13 | 1 | 34 | 2.9% | 38.7 |
| 10-14 | 1 | 39 | 2.6% | 36.9 |
| 10-15 | 2 | 40 | 5.0% | 37.0 |
| 10-16 | 3 | 73 | 4.1% | 53.0 |
| 10-17 | 2 | 62 | 3.2% | 44.6 |
| 10-18 | 2 | 53 | 3.8% | 42.9 |
| 10-19 | 1 | 48 | 2.1% | 59.2 |
| 10-20 | 3 | 39 | 7.7% | 26.3 |
| 10-21 | 0 | 43 | 0.0% | 39.2 |
| 10-22 *partial* | 2 | 32 | 6.2% | 45.0 |
| **window** | **17** | **463** | **3.7%** | |
- Top queries (10d): # system role you operate as a precision (i1, p6); 2023 euwallacea validus over 20 families (i1, p96); 43 rue buffon 75005 paris (i1, p73); amsterdam trees (i1, p81); ancient tree (i1, p89)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-15 | 78 | 8 | 10.3% |
| 10-16 | 70 | 2 | 2.9% |
| 10-17 | 57 | 3 | 5.3% |
| 10-18 | 50 | 2 | 4.0% |
| 10-19 | 82 | 0 | 0.0% |
| 10-20 | - | - | 0.0% |
| 10-21 | - | - | 0.0% |
| **7 days** | **337** | **15** | **4.5%** |
- Week before: 590 impressions, 17 clicks. No Bing demotion in sight.
- Top Bing queries: fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); how old are the trees in queen square bristol (c1/i4, p3); oak tree in zurich (c1/i4, p2); trees in the plaza dus burgos seville (c1/i3, p5); french trees found in paris (c1/i2, p6); husalle lindens copenhagen (c1/i2, p3); remarkable trees copenhagen (c1/i2, p4)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-22T09:06 | 22.1 | 0 | 9 | 1 | - |
| 10-22T12:28 | 15.1 | 0 | 8 | 5 | Berlin, Frankfurt, Graz, Innsbruck, +1 more |
| 10-22T14:49 | 10.9 | 0 | 7 | 3 | - |
| 10-22T17:39 | 25.1 | 0 | 9 | 0 | Brisbane, Chatenay Malabry |
| 10-22T19:41 | 11.9 | 0 | 6 | 0 | Brisbane |
| 10-22T22:55 | 3.6 | 0 | 4 | 0 | - |
| 10-23T02:58 | 12.3 | 0 | 5 | 0 | - |
| **7 runs** | **101** | **0** | **48** | | |

- 7 of 7 produced no trees; 1 to 5 commands refused per run; last build that went live: 2h ago.

**What they made**

- Vendor 22 photographs onto our domain; photo sweep log
- Photo judge: kept-set queue viewed, 36 rejects recorded, nothing approved
- Photographs readers sent, queued for a look; vouched ones live
- Record when each page last changed
- Brisbane hero banyan: use the 1024px iNaturalist rendition so the hero is no longer soft (deploy was failing on it)
- Record when each page last changed
- Contributor replies and ambassador invitations sent, log updated
- Minneapolis register retried (no licence, still not imported); LOG for the third attempt
- Photo viewing pass pj2 on the kept set: 34 images viewed, none meets the Cadiz standard, 70 candidate rejects recorded (Arnhem sculptures, Florence Bobolino overviews, Arentsburg panels, Brisbane bunya)
- LOG and costs for the night window: reader cedar photo, kept-set photo pass
- Photo viewing pass pj1 on the kept set: Brisbane banyan (bne_004) approved, iNat geotag 15 m from pin with its Ficus benghalensis plaque; 32 candidates rejected and recorded
- A reader's photograph of the Weeping Cedar of the Vallée-aux-Loups added beside the lead photo (cma_001)
- Photographs readers sent, queued for a look; vouched ones live
- Record when each page last changed

**Photographs the night run approved** (17; the last column undoes one)

| Day | Tree | Where | Overrule |
|---|---|---|---|
| 10-22 | The Banyan Tree of City Botanic Gardens | Brisbane | `photo_apply.py hold bne_004` |
| 10-22 | The Bur Oak of Harms Woods | Chicago | `photo_apply.py hold chi_023` |
| 10-21 | The Fluttering Elm of Konigsbrucker Strasse | Dresden | `photo_apply.py hold dre_010` |
| 10-21 | The Fingered Horse Chestnut of Volkspark Räcknitz | Dresden | `photo_apply.py hold dre_028` |
| 10-22 | The Jahn Oak of Offenbach | Frankfurt | `photo_apply.py hold frk_021` |
| 10-21 | Bergulme (Wych Elm) at the forestry office, Gosau | Hallstatt | `photo_apply.py hold hst_007` |
| 10-21 | The Weeping Beech of Weeping Beech Park | New York | `photo_apply.py hold nyc_028` |
| 10-21 | The Roadside Oak of Sacrow | Potsdam | `photo_apply.py hold pot_012` |
| 10-21 | The Plane of Am Kanal | Potsdam | `photo_apply.py hold pot_013` |
| 10-21 | The Oak of the Rote Kaserne | Potsdam | `photo_apply.py hold pot_014` |
| 10-22 | The Oak of Babelsberger Strasse | Potsdam | `photo_apply.py hold pot_017` |
| 10-21 | The Bildeiche at Höhenhof | Regensburg | `photo_apply.py hold rgb_006` |
| 10-22 | The Centennial Tree of the Presidio | San Francisco | `photo_apply.py hold sfo_011` |
| 10-21 | St. Wolfgang's Oak (Wolfgangseiche) | Thalmassing | `photo_apply.py hold thm_001` |
| 10-21 | The Tudor Place Tulip Poplar | Washington DC | `photo_apply.py hold wdc_018` |
| 10-21 | The Arlington House Deodar Cedar | Washington DC | `photo_apply.py hold wdc_020` |
| 10-22 | The Yamaki Pine | Washington DC | `photo_apply.py hold wdc_025` |

Machine: 9 chain attempts yesterday, 9 got real work time (~254 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c7/i24); /leiden/beets-beech-of-the-burcht (c2/i2); /app (c1/i11); /de (c1/i7); /seville (c1/i4)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - '# system role you operate as a precision' (i1, p6)
    - '2023 euwallacea validus over 20 families' (i1, p96)
    - 'big macadamia' (i1, p100)
    - 'canary island dates' (i1, p99)
    - 'chapina garden' (i1, p13)

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 523 |
| Clicks | 17 |
| Pages that got at least one impression | 273 |
| Impressions on the proven cities | 324 |

- 361 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3052 trees Google may index, 828 kept out for lacking a photo and an exact pin, 6414 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 331 | 17 | 24 | 0.07 | 2 |
| Not yet rich | 268 | 7 | 21 | 0.08 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| sequoia-national-park | 0 | 34 | 0.0% | 72.3 | 0.4% | general sherman tree (i3, p72) |
| munich | 0 | 14 | 0.0% | 5.1 | 6.9% | - |
| brisbane | 0 | 11 | 0.0% | 80.1 | 0.4% | the big macadamia nut (i8, p92) |

- Plus 256 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

## 2026-10-21 (previous UTC day)

**Today: an account was opened yesterday (33 total).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 21 | 15 |
| ... of which from search | Google's recovery | 6 | 2 |
| App downloads (first-time) | people | 13 | 15 |
| New accounts | people | 5 | 5 |
| Phones back within 30 days | people who stay | 7 of 12 | 6 of 17 |
| Trees saved to Want to go | intent | 6 | 1 |
| Trees collected | goal 1: stood at a tree | 12 | 4 |
| Readers' contributions | data: trees, photos, corrections, votes | 11 | 3 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Trees readers sent, for you to inspect** (4 you have not looked at; ours left out)

| Judged | Tree | Where | Species | Their girth | Our verdict | Page |
|---|---|---|---|---:|---|---|
| 2026-10-20 | The Weeping Fig of Campo Santana (2 photos) | Lisbon | Weeping Fig (Ficus benjamina) | - | publish | [lis_015](https://ancienttrees.app/lisbon/weeping-fig-of-campo-santana) |
| 2026-10-20 | Dragon Tree in Lisbon (2 photos) | lisbon | Dragon Tree | - | publish | [lis_037](https://ancienttrees.app/lisbon/dragon-tree-of-the-goethe-institut-garden) |
| 2026-10-20 | The Moreton Bay Fig of Jardim Constantino (2 photos) | Lisbon | Moreton Bay Fig (Ficus macroph | - | publish | [lis_027](https://ancienttrees.app/lisbon/moreton-bay-fig-of-jardim-constantino) |
| 2026-10-20 | The Paperbark of Jardim Constantino | Lisbon | Prickly Paperbark (Melaleuca s | - | publish | [lis_026](https://ancienttrees.app/lisbon/paperbark-of-jardim-constantino) |
- Photographs and the readers' own words: `python3 scripts/inspect_readers.py` (a local page, never in this public file). Your answer goes in with `python3 scripts/judgement.py --feedback <id> "..."`.

**What readers gave us, and it went live**

| Day | Tree | Where | What | Page |
|---|---|---|---|---|
| 10-21 | The Moreton Bay Fig of the Mendoubia | Tangier | a reader's photograph, published | [live](https://ancienttrees.app/tangier/moreton-bay-fig-of-the-mendoubia) |
| 10-20 | The Schönberg Beech above Ebringen | Freiburg | a reader's photograph, published | [live](https://ancienttrees.app/freiburg/schonberg-beech-above-ebringen) |
| 10-20 | The Weeping Fig of Campo Santana | Lisbon | a reader's photograph, published | [live](https://ancienttrees.app/lisbon/weeping-fig-of-campo-santana) |
| 10-20 | The Moreton Bay Fig of Jardim Constantino | Lisbon | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/lisbon/moreton-bay-fig-of-jardim-constantino) |
| 10-20 | The Moreton Bay Fig of Jardim Constantino | Lisbon | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/lisbon/moreton-bay-fig-of-jardim-constantino) |
| 10-20 | The Paperbark of Jardim Constantino | Lisbon | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/lisbon/paperbark-of-jardim-constantino) |
| 10-20 | The Weeping Fig of Campo Santana | Lisbon | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/lisbon/weeping-fig-of-campo-santana) |
| 10-21 | The Dragon Tree of the Goethe-Institut Garden | Lisbon | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/lisbon/dragon-tree-of-the-goethe-institut-garden) |

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| 2026-10-20 | The Weeping Fig of Campo Santana | Lisbon | - | publish | - |
| 2026-10-20 | Dragon Tree in Lisbon | - | - | publish | - |
| 2026-10-20 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | - |
| 2026-10-20 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | - |
| 2026-10-20 | The Paperbark of Jardim Constantino | Lisbon | - | publish | - |
| 2026-10-20 | The Weeping Fig of Campo Santana | Lisbon | - | publish | - |
| 2026-10-20 | Dragon Tree in Lisbon | - | - | publish | - |
| 2026-10-19 | The Schönberg Beech above Ebringen | Freiburg | - | publish | - |
| 2026-10-19 | European Beech in Freiburg | - | - | publish | - |
| 2026-10-18 | The Tulip Tree of Cantonspark | - | - | lead | - |
| 2026-10-18 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | Al besproken, akkoord |
| 2026-10-18 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | Al besproken, akkoord |
| 2026-10-18 | The Paperbark of Jardim Constantino | Lisbon | - | publish | Al besproken, akkoord |
| 2026-10-18 | A tree in Baarn | - | - | lead | - |
| 2026-10-18 | Moreton Bay Fig | - | - | lead | please put the moreton bay fig live forget about our focus areas - user content is the most valuable thing. if we have a good photo and gps then never hold back and just publish, especially if they give so much information; people can always tell us its wrong. our goal should be pages google loves instead of 100% sure |

0 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**Searched yesterday:** quercus (2 times).

**App crashes** (last 7 days, store builds; MetricKit, a sample)

| Crashes | Kind | Build | Where | Phones | Last | Fix |
|---:|---|---|---|---:|---|---|
| 15 | crash | 1.0.2 (20) | Swift runtime failure: Index out of range < static MyVotes.treeId(_:) (WorthIt.swift:84) < MyVotes.load(account:) (WorthIt.swift:103) | 1 | 2026-10-16 | fixed in build 35, released; contained server-side |

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-12 | 1 | 26 | 3.8% | 30.3 |
| 10-13 | 1 | 34 | 2.9% | 38.7 |
| 10-14 | 1 | 39 | 2.6% | 36.9 |
| 10-15 | 2 | 40 | 5.0% | 37.0 |
| 10-16 | 3 | 73 | 4.1% | 53.0 |
| 10-17 | 2 | 62 | 3.2% | 44.6 |
| 10-18 | 2 | 53 | 3.8% | 42.9 |
| 10-19 | 1 | 48 | 2.1% | 59.2 |
| 10-20 | 3 | 39 | 7.7% | 26.3 |
| 10-21 *partial* | 0 | 30 | 0.0% | 38.5 |
| **window** | **16** | **444** | **3.6%** | |
- Top queries (10d): # system role you operate as a precision (i1, p6); 2023 euwallacea validus over 20 families (i1, p96); 43 rue buffon 75005 paris (i1, p73); amsterdam trees (i1, p81); ancient tree (i1, p89)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-14 | 94 | 3 | 3.2% |
| 10-15 | 78 | 8 | 10.3% |
| 10-16 | 70 | 2 | 2.9% |
| 10-17 | 57 | 3 | 5.3% |
| 10-18 | 50 | 2 | 4.0% |
| 10-19 | 82 | 0 | 0.0% |
| 10-20 | - | - | 0.0% |
| **7 days** | **431** | **18** | **4.2%** |
- Week before: 577 impressions, 16 clicks. No Bing demotion in sight.
- Top Bing queries: fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); oak tree in zurich (c1/i4, p2); how old are the trees in queen square bristol (c1/i4, p3); trees in the plaza dus burgos seville (c1/i3, p5); ancient trees in wiesbaden germany (c1/i2, p6); berlin tree (c1/i2, p1); oldest tree in belfast (c1/i2, p1)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-21T14:48 | 18.9 | 0 | 12 | 2 | Freiburg, Hallstatt, Potsdam, Regensburg, +3 more |
| 10-21T19:53 | 14.5 | 5 | 9 | 0 | San Francisco +2, Heidelberg +1, New York +1, Potsdam +1 |
| 10-21T22:59 | 24.4 | 2 | 10 | 1 | Imperia +2, Dresden, Heidelberg, New York |
| 10-22T01:38 | 72.7 | 19 | 17 | 3 | Pittsburgh +8, Potsdam +3, Regensburg +2, Frankfurt +1, +5 more |
| 10-22T02:55 | 33.1 | 9 | 16 | 0 | Chicago +7, Frankfurt +2, San Francisco, Washington Dc |
| **5 runs** | **164** | **35** | **64** | | |

- 1 of 5 produced no trees; 1 to 3 commands refused per run; last build that went live: 2h ago.

**What they made**

- Rothenburg: hold the Insingen cemetery linden lead, too thin for a story
- Rotterdam: hold the Pelgrimvaderskerk beech lead, access still unknown
- Pittsburgh: hold four READY leads that have no honest recognition line or access
- Leiden 17 to 19: the Endegeest linden and Jan Wolkers's oak in Oegstgeest
- Record when each page last changed
- Chicago: approve a photograph of the Harms Woods bur oak (iNaturalist, CC BY)
- Species intro: Swamp White Oak (Quercus bicolor), from gby_001, ott_017, chi_028
- Frankfurt: log pass costs and leads, release claim
- Frankfurt: write and merge frk_022 (Leonhard-Eissnert-Park oak, Offenbach-Bieber) and frk_023 (Bethmannpark ginkgo), counts to 23, de overlay
- Chicago: fix silver maple comparison in chi_008, log pass costs, release claim
- Chicago: write and merge chi_023 to chi_029, seven Cook County register champions
- Enrich pass on glasgow, san-francisco, washington-dc, pittsburgh: nothing closed, gaps dead-ended; claims released
- Washington DC: approve a photograph of the Yamaki Pine (Sage Ross, CC BY-SA 3.0)
- LOG and cost: photograph sweep, Presidio Centennial Tree approved

**Photographs the night run approved** (23; the last column undoes one)

| Day | Tree | Where | Overrule |
|---|---|---|---|
| 10-20 | The Kilianseiche of Schesslitz | Bamberg | `photo_apply.py hold bam_006` |
| 10-20 | The Linden between Pödeldorf and Naisa | Bamberg | `photo_apply.py hold bam_009` |
| 10-22 | The Bur Oak of Harms Woods | Chicago | `photo_apply.py hold chi_023` |
| 10-21 | The Fluttering Elm of Konigsbrucker Strasse | Dresden | `photo_apply.py hold dre_010` |
| 10-20 | The Albert Oak of Kauscha | Dresden | `photo_apply.py hold dre_025` |
| 10-21 | The Fingered Horse Chestnut of Volkspark Räcknitz | Dresden | `photo_apply.py hold dre_028` |
| 10-20 | The Oak of the Brauteich | Dresden | `photo_apply.py hold dre_029` |
| 10-20 | The Plague Oak of Pesterwitz | Dresden | `photo_apply.py hold dre_030` |
| 10-22 | The Jahn Oak of Offenbach | Frankfurt | `photo_apply.py hold frk_021` |
| 10-21 | Bergulme (Wych Elm) at the forestry office, Gosau | Hallstatt | `photo_apply.py hold hst_007` |
| 10-20 | The Bunya Pine of the Palazzo della Provincia | Imperia | `photo_apply.py hold imp_001` |
| 10-20 | The Sycamore of Hollerich | Luxembourg City | `photo_apply.py hold lux_008` |
| 10-21 | The Weeping Beech of Weeping Beech Park | New York | `photo_apply.py hold nyc_028` |
| 10-21 | The Roadside Oak of Sacrow | Potsdam | `photo_apply.py hold pot_012` |
| 10-21 | The Plane of Am Kanal | Potsdam | `photo_apply.py hold pot_013` |
| 10-21 | The Oak of the Rote Kaserne | Potsdam | `photo_apply.py hold pot_014` |
| 10-22 | The Oak of Babelsberger Strasse | Potsdam | `photo_apply.py hold pot_017` |
| 10-21 | The Bildeiche at Höhenhof | Regensburg | `photo_apply.py hold rgb_006` |
| 10-22 | The Centennial Tree of the Presidio | San Francisco | `photo_apply.py hold sfo_011` |
| 10-21 | St. Wolfgang's Oak (Wolfgangseiche) | Thalmassing | `photo_apply.py hold thm_001` |
| 10-21 | The Tudor Place Tulip Poplar | Washington DC | `photo_apply.py hold wdc_018` |
| 10-21 | The Arlington House Deodar Cedar | Washington DC | `photo_apply.py hold wdc_020` |
| 10-22 | The Yamaki Pine | Washington DC | `photo_apply.py hold wdc_025` |

Machine: 6 chain attempts yesterday, 4 got real work time (~72 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c6/i25); /leiden/beets-beech-of-the-burcht (c2/i2); /app (c1/i12); /de (c1/i7); /seville (c1/i4)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - '# system role you operate as a precision' (i1, p6)
    - '2023 euwallacea validus over 20 families' (i1, p96)
    - 'big macadamia' (i1, p100)
    - 'canary island dates' (i1, p99)
    - 'chapina garden' (i1, p13)

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 507 |
| Clicks | 16 |
| Pages that got at least one impression | 268 |
| Impressions on the proven cities | 306 |

- 358 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3028 trees Google may index, 818 kept out for lacking a photo and an exact pin, 4657 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 642 | 30 | 72 | 0.11 | 2 |
| Not yet rich | 542 | 19 | 38 | 0.07 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| sequoia-national-park | 0 | 35 | 0.0% | 71.3 | 0.4% | sherman tree (i3, p70) |
| munich | 0 | 13 | 0.0% | 4.6 | 7.4% | - |
| brisbane | 0 | 11 | 0.0% | 75.7 | 0.4% | the big macadamia nut (i7, p91) |

- Plus 256 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

## 2026-10-20 (previous UTC day)

**Today: 1 tree submission and 7 feedback reports arrived yesterday (46 total); an account was opened yesterday (32 total).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 23 | 11 |
| ... of which from search | Google's recovery | 7 | 1 |
| App downloads (first-time) | people | 11 | 14 |
| New accounts | people | 5 | 4 |
| Phones back within 30 days | people who stay | 8 of 16 | 5 of 16 |
| Trees saved to Want to go | intent | 6 | 1 |
| Trees collected | goal 1: stood at a tree | 8 | 4 |
| Readers' contributions | data: trees, photos, corrections, votes | 11 | 3 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Trees readers sent, for you to inspect** (7 you have not looked at; ours left out)

| Judged | Tree | Where | Species | Their girth | Our verdict | Page |
|---|---|---|---|---:|---|---|
| 2026-10-20 | The Weeping Fig of Campo Santana (2 photos) | Lisbon | Weeping Fig (Ficus benjamina) | - | publish | [lis_015](https://ancienttrees.app/lisbon/weeping-fig-of-campo-santana) |
| 2026-10-20 | Dragon Tree in Lisbon (2 photos) | lisbon | Dragon Tree | - | publish | [lis_037](https://ancienttrees.app/lisbon/dragon-tree-of-the-goethe-institut-garden) |
| 2026-10-20 | The Moreton Bay Fig of Jardim Constantino (2 photos) | Lisbon | Moreton Bay Fig (Ficus macroph | - | publish | [lis_027](https://ancienttrees.app/lisbon/moreton-bay-fig-of-jardim-constantino) |
| 2026-10-20 | The Paperbark of Jardim Constantino | Lisbon | Prickly Paperbark (Melaleuca s | - | publish | [lis_026](https://ancienttrees.app/lisbon/paperbark-of-jardim-constantino) |
| 2026-10-19 | The Schönberg Beech above Ebringen | Freiburg | European Beech | - | publish | [frb_008](https://ancienttrees.app/freiburg/schonberg-beech-above-ebringen) |
| 2026-10-19 | European Beech in Freiburg | freiburg | European Beech | - | publish | [frb_008](https://ancienttrees.app/freiburg/schonberg-beech-above-ebringen) |
| 2026-10-18 | Moreton Bay Fig | - | Moreton Bay Fig | - | lead | - |
- Photographs and the readers' own words: `python3 scripts/inspect_readers.py` (a local page, never in this public file). Your answer goes in with `python3 scripts/judgement.py --feedback <id> "..."`.

**What readers gave us, and it went live**

| Day | Tree | Where | What | Page |
|---|---|---|---|---|
| 10-20 | The Schönberg Beech above Ebringen | Freiburg | a reader's photograph, published | [live](https://ancienttrees.app/freiburg/schonberg-beech-above-ebringen) |
| 10-20 | The Weeping Fig of Campo Santana | Lisbon | a reader's photograph, published | [live](https://ancienttrees.app/lisbon/weeping-fig-of-campo-santana) |
| 10-20 | The Moreton Bay Fig of Jardim Constantino | Lisbon | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/lisbon/moreton-bay-fig-of-jardim-constantino) |
| 10-20 | The Moreton Bay Fig of Jardim Constantino | Lisbon | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/lisbon/moreton-bay-fig-of-jardim-constantino) |
| 10-20 | The Paperbark of Jardim Constantino | Lisbon | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/lisbon/paperbark-of-jardim-constantino) |
| 10-20 | The Weeping Fig of Campo Santana | Lisbon | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/lisbon/weeping-fig-of-campo-santana) |

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| 2026-10-20 | The Weeping Fig of Campo Santana | Lisbon | - | publish | - |
| 2026-10-20 | Dragon Tree in Lisbon | - | - | publish | - |
| 2026-10-20 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | - |
| 2026-10-20 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | - |
| 2026-10-20 | The Paperbark of Jardim Constantino | Lisbon | - | publish | - |
| 2026-10-20 | The Weeping Fig of Campo Santana | Lisbon | - | publish | - |
| 2026-10-20 | Dragon Tree in Lisbon | - | - | publish | - |
| 2026-10-19 | The Schönberg Beech above Ebringen | Freiburg | - | publish | - |
| 2026-10-19 | European Beech in Freiburg | - | - | publish | - |
| 2026-10-18 | The Tulip Tree of Cantonspark | - | - | lead | - |
| 2026-10-18 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | Al besproken, akkoord |
| 2026-10-18 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | Al besproken, akkoord |
| 2026-10-18 | The Paperbark of Jardim Constantino | Lisbon | - | publish | Al besproken, akkoord |
| 2026-10-18 | A tree in Baarn | - | - | lead | - |
| 2026-10-18 | Moreton Bay Fig | - | - | lead | - |

0 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**Searched yesterday:** prah.

**App crashes** (last 7 days, store builds; MetricKit, a sample)

| Crashes | Kind | Build | Where | Phones | Last | Fix |
|---:|---|---|---|---:|---|---|
| 30 | crash | 1.0.2 (20) | Swift runtime failure: Index out of range < static MyVotes.treeId(_:) (WorthIt.swift:84) < MyVotes.load(account:) (WorthIt.swift:103) | 1 | 2026-10-16 | fixed in build 35, released; contained server-side |

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-11 | 1 | 32 | 3.1% | 31.7 |
| 10-12 | 1 | 26 | 3.8% | 30.3 |
| 10-13 | 1 | 34 | 2.9% | 38.7 |
| 10-14 | 1 | 39 | 2.6% | 36.9 |
| 10-15 | 2 | 40 | 5.0% | 37.0 |
| 10-16 | 3 | 73 | 4.1% | 53.0 |
| 10-17 | 2 | 62 | 3.2% | 44.6 |
| 10-18 | 2 | 53 | 3.8% | 42.9 |
| 10-19 | 1 | 48 | 2.1% | 59.2 |
| 10-20 *partial* | 3 | 33 | 9.1% | 26.8 |
| **window** | **17** | **440** | **3.9%** | |
- Top queries (10d): # system role you operate as a precision (i1, p6); 2023 euwallacea validus over 20 families (i1, p96); amsterdam trees (i1, p81); ancient tree (i1, p89); ancient trees (i1, p82)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-13 | 90 | 2 | 2.2% |
| 10-14 | 94 | 3 | 3.2% |
| 10-15 | 78 | 8 | 10.3% |
| 10-16 | 70 | 2 | 2.9% |
| 10-17 | 57 | 3 | 5.3% |
| 10-18 | 50 | 2 | 4.0% |
| 10-19 | - | - | 0.0% |
| **7 days** | **439** | **20** | **4.6%** |
- Week before: 552 impressions, 16 clicks. No Bing demotion in sight.
- Top Bing queries: fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); how old are the trees in queen square bristol (c1/i4, p3); oak tree in zurich (c1/i4, p2); trees in the plaza dus burgos seville (c1/i3, p5); oldest live oak trees in new orleans (c1/i2, p6); berlin tree (c1/i2, p1); oldest tree in belfast (c1/i2, p1)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-20T13:13 | 19.1 | 5 | 11 | 0 | Bamberg +3, Rotterdam +2, Hong Kong, Lisbon |
| 10-20T15:13 | 67.8 | 15 | 26 | 0 | Potsdam +4, Washington Dc +4, Hallstatt +2, Nuremberg +2, +2 more |
| 10-20T22:28 | 0.0 | 0 | 1 | 0 | - |
| 10-20T22:53 | 0.0 | 0 | 0 | 0 | - |
| 10-21T02:56 | 0.3 | 0 | 1 | - | - |
| 10-21T05:55 | 0.0 | 0 | 0 | 0 | - |
| **6 runs** | **87** | **20** | **39** | | |

- 4 of 6 produced no trees; 4 wrote nothing to LOG.md; last build that went live: 3h ago.

**What they made**

- Nuremberg: claimed and released, 3 of 16 leads placed, wall for 48h
- Lisbon: the Goethe-Institut dragon tree, from a reader's photograph, with verdict and pt overlay
- Photographs readers sent, queued for a look; vouched ones live
- Record when each page last changed
- Four reader photographs of Lisbon trees live beside the existing ones; Lisbon dragon tree kept as a lead
- Photographs readers sent, queued for a look; vouched ones live
- Record when each page last changed
- New York verify pass: two held trees, wall; LOG and costs
- LOG and costs: Seattle two tulip trees
- Seattle: two tulip trees
- Potsdam: reader wording for the Rote Kaserne access line; LOG and costs
- Potsdam: four Naturdenkmal trees
- LOG and costs: Washington DC four trees
- Washington DC: four NPS witness trees

**Photographs the night run approved** (23; the last column undoes one)

| Day | Tree | Where | Overrule |
|---|---|---|---|
| 10-20 | The Kilianseiche of Schesslitz | Bamberg | `photo_apply.py hold bam_006` |
| 10-20 | The Linden between Pödeldorf and Naisa | Bamberg | `photo_apply.py hold bam_009` |
| 10-19 | The Old Town Gate Oak | Brno | `photo_apply.py hold brq_002` |
| 10-19 | The Rieseneiche of the Sauerbusch | Dresden | `photo_apply.py hold dre_006` |
| 10-19 | The Luther Oak of Kleinluga | Dresden | `photo_apply.py hold dre_023` |
| 10-19 | The Village Square Oak of Oberpoyritz | Dresden | `photo_apply.py hold dre_024` |
| 10-20 | The Albert Oak of Kauscha | Dresden | `photo_apply.py hold dre_025` |
| 10-19 | The Albert Oak of Wasaplatz | Dresden | `photo_apply.py hold dre_026` |
| 10-20 | The Oak of the Brauteich | Dresden | `photo_apply.py hold dre_029` |
| 10-20 | The Plague Oak of Pesterwitz | Dresden | `photo_apply.py hold dre_030` |
| 10-19 | The Border Oak at Berger Warte | Frankfurt | `photo_apply.py hold frk_019` |
| 10-19 | The Münzgrabenstrasse Oriental Plane | Graz | `photo_apply.py hold grz_016` |
| 10-19 | The Independence Spruce | Helsinki | `photo_apply.py hold hel_010` |
| 10-20 | The Bunya Pine of the Palazzo della Provincia | Imperia | `photo_apply.py hold imp_001` |
| 10-19 | The Schulgasse Oak in Hötting | Innsbruck | `photo_apply.py hold inn_003` |
| 10-19 | The Traklpark Oak | Innsbruck | `photo_apply.py hold inn_006` |
| 10-19 | The Osterley Park Cork Oak | London | `photo_apply.py hold lon_032` |
| 10-19 | The Roehampton Lucombe Oak | London | `photo_apply.py hold lon_033` |
| 10-20 | The Sycamore of Hollerich | Luxembourg City | `photo_apply.py hold lux_008` |
| 10-19 | The Kaya of Nagoya Castle | Nagoya | `photo_apply.py hold ngy_001` |
| 10-19 | The Oak of Sebastian-Kneipp-Straße | Salzburg | `photo_apply.py hold szb_013` |
| 10-19 | Chêne de la Vierge à Viroflay | Viroflay | `photo_apply.py hold vir_001` |
| 10-19 | Takinoya no Hidarimakigaya | Yabu | `photo_apply.py hold yab_002` |

Machine: 9 chain attempts yesterday, 7 got real work time (~260 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c7/i22); /leiden/beets-beech-of-the-burcht (c2/i2); /app (c1/i8); /de (c1/i7); /seville (c1/i4)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - '# system role you operate as a precision' (i1, p6)
    - '2023 euwallacea validus over 20 families' (i1, p96)
    - 'big macadamia' (i1, p100)
    - 'canary island dates' (i1, p99)
    - 'chapina garden' (i1, p13)

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 480 |
| Clicks | 17 |
| Pages that got at least one impression | 267 |
| Impressions on the proven cities | 304 |

- 366 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3001 trees Google may index, 807 kept out for lacking a photo and an exact pin, 4631 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 630 | 28 | 67 | 0.11 | 2 |
| Not yet rich | 536 | 23 | 41 | 0.08 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| sequoia-national-park | 0 | 32 | 0.0% | 71.6 | 0.4% | sherman tree (i4, p73) |
| brisbane | 0 | 10 | 0.0% | 73.6 | 0.4% | the big macadamia nut (i6, p90) |

- Plus 257 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

## 2026-10-19 (previous UTC day)

**Today: 1 tree submission arrived yesterday (38 total); an account was opened yesterday (31 total).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 22 | 3 |
| ... of which from search | Google's recovery | 6 | 0 |
| App downloads (first-time) | people | 15 | 10 |
| New accounts | people | 5 | 3 |
| Phones back within 30 days | people who stay | 5 of 14 | 6 of 16 |
| Trees saved to Want to go | intent | 7 | 0 |
| Trees collected | goal 1: stood at a tree | 7 | 5 |
| Readers' contributions | data: trees, photos, corrections, votes | 5 | 1 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Trees readers sent, for you to inspect** (2 you have not looked at; ours left out)

| Judged | Tree | Where | Species | Their girth | Our verdict | Page |
|---|---|---|---|---:|---|---|
| 2026-10-18 | The Moreton Bay Fig of Jardim Constantino (2 photos) | Lisbon | Moreton Bay Fig (Ficus macroph | - | publish | [lis_027](https://ancienttrees.app/lisbon/moreton-bay-fig-of-jardim-constantino) |
| 2026-10-18 | The Paperbark of Jardim Constantino | Lisbon | Prickly Paperbark (Melaleuca s | - | publish | [lis_026](https://ancienttrees.app/lisbon/paperbark-of-jardim-constantino) |
- Photographs and the readers' own words: `python3 scripts/inspect_readers.py` (a local page, never in this public file). Your answer goes in with `python3 scripts/judgement.py --feedback <id> "..."`.

**What readers gave us, and it went live**

| Day | Tree | Where | What | Page |
|---|---|---|---|---|
| 10-18 | The Moreton Bay Fig of Jardim Constantino | Lisbon | a reader's photograph, published | [live](https://ancienttrees.app/lisbon/moreton-bay-fig-of-jardim-constantino) |
| 10-18 | The Moreton Bay Fig of Jardim Constantino | Lisbon | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/lisbon/moreton-bay-fig-of-jardim-constantino) |
| 10-18 | The Paperbark of Jardim Constantino | Lisbon | a reader's photograph, published | [live](https://ancienttrees.app/lisbon/paperbark-of-jardim-constantino) |
| 10-18 | The Yew of Campo Santana | Lisbon | a reader's correction changed the page | - |

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| 2026-10-19 | European Beech in Freiburg | - | - | open | - |
| 2026-10-18 | The Tulip Tree of Cantonspark | - | - | lead | - |
| 2026-10-18 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | - |
| 2026-10-18 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | - |
| 2026-10-18 | The Paperbark of Jardim Constantino | Lisbon | - | publish | - |
| 2026-10-18 | A tree in Baarn | - | - | lead | - |
| 2026-10-18 | Moreton Bay Fig | - | - | open | - |
| 2026-10-15 | The Meiji Jingu Gaien Ginkgo Avenue | - | - | lead | - |
| 2026-10-13 | The Great Lawn Plane of Parc Montsouri | Paris | 88% girth | publish | publish (2026-10-13, session: 'follow your suggestion') |

2 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**Searched yesterday:** braga, portugal.

**App crashes** (last 7 days, store builds; MetricKit, a sample)

| Crashes | Kind | Build | Where | Phones | Last | Fix |
|---:|---|---|---|---:|---|---|
| 37 | crash | 1.0.2 (20) | Swift runtime failure: Index out of range < static MyVotes.treeId(_:) (WorthIt.swift:84) < MyVotes.load(account:) (WorthIt.swift:103) | 1 | 2026-10-16 | fixed in build 35, released; contained server-side |
- Builds not from the App Store (Xcode or review): 1 report(s) on build 25.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-10 | 0 | 35 | 0.0% | 29.8 |
| 10-11 | 1 | 32 | 3.1% | 31.7 |
| 10-12 | 1 | 26 | 3.8% | 30.3 |
| 10-13 | 1 | 34 | 2.9% | 38.7 |
| 10-14 | 1 | 39 | 2.6% | 36.9 |
| 10-15 | 2 | 40 | 5.0% | 37.0 |
| 10-16 | 3 | 73 | 4.1% | 53.0 |
| 10-17 | 2 | 62 | 3.2% | 44.6 |
| 10-18 | 2 | 53 | 3.8% | 42.9 |
| 10-19 *partial* | 1 | 29 | 3.4% | 60.2 |
| **window** | **14** | **423** | **3.3%** | |
- Top queries (10d): amsterdam trees (i1, p81); ancient tree (i1, p89); ancient trees (i1, p82); araucaria norfolk island pine (i1, p86); arboles de cadiz (i5, p72)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-12 | 81 | 3 | 3.7% |
| 10-13 | 90 | 2 | 2.2% |
| 10-14 | 94 | 3 | 3.2% |
| 10-15 | 78 | 8 | 10.3% |
| 10-16 | 70 | 2 | 2.9% |
| 10-17 | 57 | 3 | 5.3% |
| 10-18 | 50 | 2 | 4.0% |
| **7 days** | **520** | **23** | **4.4%** |
- Week before: 550 impressions, 18 clicks. No Bing demotion in sight.
- Top Bing queries: fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); oak tree in zurich (c1/i4, p2); how old are the trees in queen square bristol (c1/i4, p3); trees in the plaza dus burgos seville (c1/i3, p5); ancient trees in wiesbaden germany (c1/i2, p6); berlin tree (c1/i2, p1); oldest tree in belfast (c1/i2, p1)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-19T09:31 | 17.5 | 0 | 5 | 0 | London |
| 10-19T21:39 | 3.5 | 0 | 4 | 1 | - |
| 10-19T21:56 | 25.4 | 3 | 6 | 0 | Frankfurt +3 |
| 10-20T00:41 | 3.8 | 0 | 5 | 1 | - |
| 10-20T00:54 | 43.2 | 7 | 9 | 1 | Roosendaal +4, Batenburg +2, Fort Worth +1, Dresden, +2 more |
| 10-20T05:20 | 18.1 | 2 | 8 | 1 | Stuttgart +2, London |
| 10-20T07:01 | 22.4 | 0 | 10 | 2 | Thalmassing +1, Rotterdam |
| **7 runs** | **134** | **12** | **47** | | |

- 4 of 7 produced no trees; 1 to 2 commands refused per run; last build that went live: 2h ago.

**What they made**

- photo_hunt recheck vienna/london/new-york/seattle: 0 new candidates
- Rotterdam deepen pass: retire duplicate rot_003, 1 flagged candidate, 3 leads; release
- Stuttgart verify pass: 0 new trees, 5 leads, stu_011 folded as duplicate; release
- Drop fdl_001 from research: already live as spa_001
- Thalmassing: St. Wolfgang's Oak as a one-tree place; release fort-worth (wall)
- Bamberg verify pass: 3 register-only trees staged, leads, costs, log
- Record when each page last changed
- Vendor 31 photographs onto our own domain
- Enrich Stuttgart ginkgo (register, girth, hours) and Wilhelma access; dead-end 9 gaps
- London enrich: Osterley cork oak access line; 6 gaps dead-ended
- Stuttgart: Wilhelma sequoia grove and ginkgo live (13 trees), German overlay, costs, log
- Record when each page last changed
- Write pass: John Peter Smith Oak live in Fort Worth (19 trees); ftw_018, inn_007 held with reasons
- Verify pass fort-worth: John Peter Smith Oak (ftw_020); Fursman Bur Oak blocked (removed 2018)

**Photographs the night run approved** (54; the last column undoes one)

| Day | Tree | Where | Overrule |
|---|---|---|---|
| 10-18 | The Velvet-leaf Euodia of Fischerinsel | Berlin | `photo_apply.py hold ber_047` |
| 10-18 | The Oak between the Neuer See and the Landwehr Canal | Berlin | `photo_apply.py hold ber_059` |
| 10-19 | The Old Town Gate Oak | Brno | `photo_apply.py hold brq_002` |
| 10-18 | The Post Oak Grove of Pioneer Park Cemetery | Dallas | `photo_apply.py hold dal_012` |
| 10-19 | The Rieseneiche of the Sauerbusch | Dresden | `photo_apply.py hold dre_006` |
| 10-19 | The Luther Oak of Kleinluga | Dresden | `photo_apply.py hold dre_023` |
| 10-19 | The Village Square Oak of Oberpoyritz | Dresden | `photo_apply.py hold dre_024` |
| 10-20 | The Albert Oak of Kauscha | Dresden | `photo_apply.py hold dre_025` |
| 10-19 | The Albert Oak of Wasaplatz | Dresden | `photo_apply.py hold dre_026` |
| 10-20 | The Oak of the Brauteich | Dresden | `photo_apply.py hold dre_029` |
| 10-20 | The Plague Oak of Pesterwitz | Dresden | `photo_apply.py hold dre_030` |
| 10-18 | The Paradieseiche of Sachsenhausen | Frankfurt | `photo_apply.py hold frk_008` |
| 10-18 | The Peace Oak of Sossenheim | Frankfurt | `photo_apply.py hold frk_010` |
| 10-18 | The Cemetery Lindens of Nieder-Erlenbach | Frankfurt | `photo_apply.py hold frk_014` |
| 10-18 | The Chestnut at the Schaeferkoeppel | Frankfurt | `photo_apply.py hold frk_016` |
| 10-18 | The August Reiss Oak of Offenbach | Frankfurt | `photo_apply.py hold frk_017` |
| 10-19 | The Border Oak at Berger Warte | Frankfurt | `photo_apply.py hold frk_019` |
| 10-19 | The Münzgrabenstrasse Oriental Plane | Graz | `photo_apply.py hold grz_016` |
| 10-19 | The Independence Spruce | Helsinki | `photo_apply.py hold hel_010` |
| 10-18 | The Banyan of Nathan Road | Hong Kong | `photo_apply.py hold hkg_010` |
| 10-19 | The Schulgasse Oak in Hötting | Innsbruck | `photo_apply.py hold inn_003` |
| 10-19 | The Traklpark Oak | Innsbruck | `photo_apply.py hold inn_006` |
| 10-18 | The Oak of Probstheida Village Green | Leipzig | `photo_apply.py hold lpz_023` |
| 10-18 | The Japanese Pagoda Tree of Flossplatz | Leipzig | `photo_apply.py hold lpz_024` |
| 10-18 | The Oak of Kantatenweg | Leipzig | `photo_apply.py hold lpz_025` |
| 10-18 | The Steinlinde of Plausig | Leipzig | `photo_apply.py hold lpz_027` |
| 10-18 | The Marble Hill Black Walnut | London | `photo_apply.py hold lon_029` |
| 10-19 | The Osterley Park Cork Oak | London | `photo_apply.py hold lon_032` |
| 10-19 | The Roehampton Lucombe Oak | London | `photo_apply.py hold lon_033` |
| 10-18 | El Pino (The Pine Tree) | Los Angeles | `photo_apply.py hold lax_013` |
| 10-20 | The Sycamore of Hollerich | Luxembourg City | `photo_apply.py hold lux_008` |
| 10-19 | The Kaya of Nagoya Castle | Nagoya | `photo_apply.py hold ngy_001` |
| 10-18 | The Eucalyptus of the Villa Comunale | Naples | `photo_apply.py hold nap_020` |
| 10-18 | The London Plane of the Reservoir | New York | `photo_apply.py hold nyc_019` |
| 10-18 | The Corbett Oak | Portland | `photo_apply.py hold ptl_021` |
| 10-19 | The Oak of Sebastian-Kneipp-Straße | Salzburg | `photo_apply.py hold szb_013` |
| 10-18 | The Hiawatha Playfield Red Oak | Seattle | `photo_apply.py hold sea_009` |
| 10-18 | The Roanoke Park European White Elm | Seattle | `photo_apply.py hold sea_017` |
| 10-18 | Sentinel Tree | Sequoia National Park | `photo_apply.py hold seq_007` |
| 10-18 | Bellmanseken | Stockholm | `photo_apply.py hold sto_007` |
| 10-18 | The Schillereiche | Stuttgart | `photo_apply.py hold stu_008` |
| 10-18 | The Wernhalde Giant Sequoias | Stuttgart | `photo_apply.py hold stu_009` |
| 10-18 | The Jahneiche | Stuttgart | `photo_apply.py hold stu_010` |
| 10-18 | The Camphor Tree of Hongo Yumicho | Tokyo | `photo_apply.py hold tok_022` |
| 10-18 | The Oriental Plane of the Abraham Dolehof | Utrecht | `photo_apply.py hold utr_035` |
| 10-18 | The Maurer Schubertpark Lime | Vienna | `photo_apply.py hold vie_049` |
| 10-18 | The Oberlaa Horse Chestnut | Vienna | `photo_apply.py hold vie_056` |
| 10-18 | The Strassergasse Oak | Vienna | `photo_apply.py hold vie_058` |
| 10-18 | The Ash of Mickiewicz's Courtyard | Vilnius | `photo_apply.py hold vln_004` |
| 10-19 | Chêne de la Vierge à Viroflay | Viroflay | `photo_apply.py hold vir_001` |
| 10-18 | The Smithsonian Witness Elm | Washington DC | `photo_apply.py hold wdc_015` |
| 10-18 | Travilah Oak | Washington DC | `photo_apply.py hold wdc_016` |
| 10-19 | Takinoya no Hidarimakigaya | Yabu | `photo_apply.py hold yab_002` |
| 10-18 | The Four-Trunked Survivor | Ypres | `photo_apply.py hold ypr_005` |

Machine: 7 chain attempts yesterday, 7 got real work time (~173 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c5/i21); /leiden/beets-beech-of-the-burcht (c2/i2); /app (c1/i9); /de (c1/i7); /seville (c1/i5)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'big sherman tree' (i2, p69)
    - 'duncan memorial cedar tree' (i2, p50)
    - 'big macadamia' (i1, p100)
    - 'canary island dates' (i1, p99)
    - 'chapina garden' (i1, p13)

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 465 |
| Clicks | 14 |
| Pages that got at least one impression | 253 |
| Impressions on the proven cities | 288 |

- 343 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 2984 trees Google may index, 779 kept out for lacking a photo and an exact pin, 4583 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 625 | 27 | 69 | 0.11 | 2 |
| Not yet rich | 533 | 23 | 42 | 0.08 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| sequoia-national-park | 0 | 36 | 0.0% | 72.0 | 0.4% | sherman tree (i4, p73) |
| brisbane | 0 | 10 | 0.0% | 68.5 | 0.4% | the big macadamia nut (i5, p89) |

- Plus 257 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

## Weekly analysis 2026-10-19

Twelfth weekly analysis. Compares 10-12 to 10-18 with 10-05 to 10-11, read from
the 10-18 daily entry. 10-18 is partial in Search Console and Google backfills,
so this week's row can still move a little. Volumes are small throughout;
nothing below is a trend unless it says so.

**Scorecard**

| Week | Impressions | Clicks | CTR | Avg position | Visits (beacon) | Directions (web) | App-CTA | App downloads (first-time) | Waitlist total | Submissions total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10-05 to 10-11 | 277 | 14 | 5.1% | 22 to 50 | 330 | 5 (14d) | 19 (14d) | 14 | 21 | 33 |
| 10-12 to 10-18 | 317 | 12 | 3.8% | 30 to 53 | not in the entry | 0 (7d) | 14 (7d) | 14 (6 days) | 22 | 37 |

Bing, same weeks: 537 impressions and 18 clicks, then 523 and 23 (4.4% CTR).
App ratios (new phones this week against last): opened a tree day one 86%
against 58%, tapped Take me there 14% against 8%, back within a week 17%
against 56% (2 of 12 against 5 of 9). Device split is not in the 10-18 entry.

**What moved:**
1. Google is flat at the floor for a third week: 317 impressions (about 45 a
   day), 12 clicks, position 30 to 53. The 10-16 and 10-17 days (73, 62) are
   one blip, not recovery.
2. Bing is steady and ahead on clicks: 23 against Google's 12, index up to
   2,775 pages (2,447 the week before). It converts at 4.4%.
3. The app held its size (14 new phones against 12, 14 downloads, 8 from App
   Store search). Day-one opening of a tree rose; the 17% return rate is two
   phones of twelve, so it is noise either way. Web Take me there: 0 clicks
   in 7 days.
4. Readers gave more: submissions 33 to 37 (4 feedback), 3 accounts, 1
   Android signup, and two Lisbon trees (Jardim Constantino fig and
   paperbark) went live from one app contributor who stood at 3 trees.
5. The machine was busy: 273 minutes, 44 trees, 29 first photographs in the
   last 24 hours; week meter 1,383 minutes against 791 last week.

**Suggestions, ranked:**
1. **[run]** Sequoia National Park is the only city above the depth threshold
   (38 impressions, position 73) and "big sherman tree" is a content lead
   (i2, p69). Check whether a Sherman page exists and what its title says
   against the query; fix the title or add the photograph first. Traces to
   the Depth table and the content-leads list.
2. **[run]** Keep feeding Bing: queries already click at positions 1 to 5
   (fig tree in square alicante c2, big trees of quebec city c2, queen square
   bristol, oak tree in zurich). Give those pages a photograph, register
   link and access line, since Bing is where the clicks are.
3. **[sessie]** The tree-opened row says 89 events yesterday from 7 installs,
   one install making 486% of the average. Check whether that install is
   ours and add it to excluded_installs in data/app-measure.json before the
   day-one activation ratios are read as real.
4. **[sessie]** Take me there is the weakest app step (2 of 14, 14%), and web
   directions are at 0. Walk the tree screen on a phone and see where the
   button sits and what it says; only 14 phones, so decide by looking, not
   by waiting for more data.
5. **[FOR HIDDE]** No new decision. Recovery has now run three weeks with
   Manual actions clear, so the open choice is only how long to wait before
   widening RETURN again; suggest a checkpoint date rather than a number.

**Watch next week:** Google daily impressions above 100 for two days in a row,
whether the Sherman or Sequoia pages move off position 70, and the app
return rate on a larger base than 12 phones.

## 2026-10-18 (previous UTC day)

**Today: 2 feedback reports arrived yesterday (37 total).**

**Conclusion: the numbers that matter now** (this week against the week before)

| Number | Why it counts | This week | Week before |
|---|---|---:|---:|
| Stood at a tree (app collections) | goal 1, the north star | 6 | 5 |
| New phones that opened a tree on day one | activation | 12 of 14 (86%) | 7 of 12 (58%) |
| New phones that tapped Take me there on day one | activation | 2 of 14 (14%) | 1 of 12 (8%) |
| Phones back within a week | retention | 2 of 12 (17%) | 5 of 9 (56%) |
| New accounts (strangers) | people collected | 3 | 5 |
| Readers' trees and photographs live | data collected | 5 | 2 |
| Arrivals from search, every engine (8 days) | traction | - | - |

6 collections at a tree this week against 5 the week before, a handful: read it as a count, not a trend. The weakest link is tapping Take me there on day one (2 of 14): that step is the work, more traffic only pours more people into it.

**Trees readers sent, for you to inspect** (2 you have not looked at; ours left out)

| Judged | Tree | Where | Species | Their girth | Our verdict | Page |
|---|---|---|---|---:|---|---|
| 2026-10-18 | The Moreton Bay Fig of Jardim Constantino (2 photos) | Lisbon | Moreton Bay Fig (Ficus macroph | - | publish | [lis_027](https://ancienttrees.app/lisbon/moreton-bay-fig-of-jardim-constantino) |
| 2026-10-18 | The Paperbark of Jardim Constantino | Lisbon | Prickly Paperbark (Melaleuca s | - | publish | [lis_026](https://ancienttrees.app/lisbon/paperbark-of-jardim-constantino) |
- Photographs and the readers' own words: `python3 scripts/inspect_readers.py` (a local page, never in this public file). Your answer goes in with `python3 scripts/judgement.py --feedback <id> "..."`.

**What readers gave us, and it went live**

| Day | Tree | Where | What | Page |
|---|---|---|---|---|
| 10-18 | The Moreton Bay Fig of Jardim Constantino | Lisbon | a reader's photograph, published | [live](https://ancienttrees.app/lisbon/moreton-bay-fig-of-jardim-constantino) |
| 10-18 | The Moreton Bay Fig of Jardim Constantino | Lisbon | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/lisbon/moreton-bay-fig-of-jardim-constantino) |
| 10-18 | The Paperbark of Jardim Constantino | Lisbon | a reader's photograph, published | [live](https://ancienttrees.app/lisbon/paperbark-of-jardim-constantino) |

**Photographs added to trees already live, last 24 hours** (29)

| Tree | Where | What | By | Page |
|---|---|---|---|---|
| The Velvet-leaf Euodia of Fischerinsel | Berlin | first photograph | night run | [live](https://ancienttrees.app/berlin/velvet-leaf-euodia-of-fischerinsel) |
| The Oak between the Neuer See and the Landwehr Canal | Berlin | first photograph | night run | [live](https://ancienttrees.app/berlin/oak-between-the-neuer-see-and-the-landwehr-canal) |
| The Post Oak Grove of Pioneer Park Cemetery | Dallas | first photograph | night run | [live](https://ancienttrees.app/dallas/post-oak-grove-of-pioneer-park-cemetery) |
| The Paradieseiche of Sachsenhausen | Frankfurt | first photograph | night run | [live](https://ancienttrees.app/frankfurt/paradieseiche-of-sachsenhausen) |
| The Peace Oak of Sossenheim | Frankfurt | first photograph | night run | [live](https://ancienttrees.app/frankfurt/peace-oak-of-sossenheim) |
| The Münzgrabenstrasse Oriental Plane | Graz | first photograph | night run | [live](https://ancienttrees.app/graz/munzgrabenstrasse-oriental-plane) |
| The Independence Spruce | Helsinki | first photograph | night run | [live](https://ancienttrees.app/helsinki/independence-spruce) |
| The Banyan of Nathan Road | Hong Kong | first photograph | night run | [live](https://ancienttrees.app/hong-kong/banyan-of-nathan-road) |
| The Paperbark of Jardim Constantino | Lisbon | first photograph | a reader | [live](https://ancienttrees.app/lisbon/paperbark-of-jardim-constantino) |
| The Moreton Bay Fig of Jardim Constantino | Lisbon | first photograph, 1 more photograph | a reader | [live](https://ancienttrees.app/lisbon/moreton-bay-fig-of-jardim-constantino) |
| El Pino (The Pine Tree) | Los Angeles | first photograph | night run | [live](https://ancienttrees.app/los-angeles/el-pino-the-pine-tree) |
| The Eucalyptus of the Villa Comunale | Naples | first photograph | night run | [live](https://ancienttrees.app/naples/eucalyptus-of-the-villa-comunale) |
| The London Plane of the Reservoir | New York | first photograph | night run | [live](https://ancienttrees.app/new-york/london-plane-of-the-reservoir) |
| The Gloucester Tree | Pemberton | first photograph | session or your review | [live](https://ancienttrees.app/pemberton/gloucester-tree) |
| The Balch Creek Fir | Portland | new lead photograph | session or your review | [live](https://ancienttrees.app/portland/balch-creek-fir) |
| The Corbett Oak | Portland | first photograph | night run | [live](https://ancienttrees.app/portland/corbett-oak) |
| The Hiawatha Playfield Red Oak | Seattle | first photograph | night run | [live](https://ancienttrees.app/seattle/hiawatha-playfield-red-oak) |
| The Roanoke Park European White Elm | Seattle | first photograph | night run | [live](https://ancienttrees.app/seattle/roanoke-park-european-white-elm) |
| Sentinel Tree | Sequoia National Park | first photograph | night run | [live](https://ancienttrees.app/sequoia-national-park/sentinel-tree) |
| Bellmanseken | Stockholm | first photograph | night run | [live](https://ancienttrees.app/stockholm/bellmanseken) |
| The Camphor Tree of Hongo Yumicho | Tokyo | first photograph | night run | [live](https://ancienttrees.app/tokyo/camphor-tree-of-hongo-yumicho) |
| The Oriental Plane of the Abraham Dolehof | Utrecht | first photograph | night run | [live](https://ancienttrees.app/utrecht/oriental-plane-of-the-abraham-dolehof) |
| The Maurer Schubertpark Lime | Vienna | first photograph | night run | [live](https://ancienttrees.app/vienna/maurer-schubertpark-lime) |
| The Oberlaa Horse Chestnut | Vienna | first photograph | night run | [live](https://ancienttrees.app/vienna/oberlaa-horse-chestnut) |
| The Strassergasse Oak | Vienna | first photograph | night run | [live](https://ancienttrees.app/vienna/strassergasse-oak) |
| The Ash of Mickiewicz's Courtyard | Vilnius | first photograph | night run | [live](https://ancienttrees.app/vilnius/ash-of-mickiewiczs-courtyard) |
| The Smithsonian Witness Elm | Washington DC | first photograph | night run | [live](https://ancienttrees.app/washington-dc/smithsonian-witness-elm) |
| Travilah Oak | Washington DC | first photograph | night run | [live](https://ancienttrees.app/washington-dc/travilah-oak) |
| Takinoya no Hidarimakigaya | Yabu | first photograph | night run | [live](https://ancienttrees.app/yabu/takinoya-no-hidarimakigaya) |

**Did the product happen**

| Action | Yesterday | 7 days | Last |
|---|---:|---:|---|
| signin-open | 0 | 9 | 3 days ago |
| app-cta | 0 | 14 | 2 days ago |
| signin-oauth | 0 | 0 | 10 days ago |
| signin-done | 0 | 0 | 12 days ago |
| directions | 0 | 0 | 10 days ago |
| search-home | 1 | 5 | yesterday |
| app-open | 0 | 2 | 3 days ago |
| suggestion-submit | 0 | 0 | 24 days ago |
| home-country | 0 | 2 | 4 days ago |
| home-fav | 0 | 0 | 10 days ago |
| signin-link-sent | 0 | 0 | 24 days ago |
| save | 0 | 0 | 17 days ago |
| waitlist-submit | 0 | 1 | 3 days ago |
| home-dir-tree | 0 | 1 | 4 days ago |
| search-explore | 0 | 2 | 3 days ago |
| visit | 0 | 0 | 29 days ago |
| search-bar | 2 | 2 | yesterday |
| app-page-badge | 0 | 0 | 10 days ago |
| home-species | 0 | 0 | 28 days ago |
| search-bar-m | 0 | 2 | 2 days ago |
| sponsor-open | 0 | 1 | 4 days ago |
| home-dir-city | 0 | 1 | 2 days ago |
| home-dir-species | 0 | 0 | 8 days ago |
| walks-app | 0 | 0 | 26 days ago |
| worthit-report | 0 | 0 | 25 days ago |
| worthit-report detail | 0 | 0 | 25 days ago |
| worthit-worth it | 0 | 0 | 29 days ago |
| worthit-not worth it | 0 | 0 | never |
| **all** | **3** | **42** | |

**Searched yesterday:** london plane (2 times), nepal.

| Day | Accounts | Android waitlist | Saves | Trees sent | Feedback | Ambassador asks |
|---|---:|---:|---:|---:|---:|---:|
| 10-12 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-13 | 1 | 0 | 0 | 0 | 2 | 0 |
| 10-14 | 1 | 0 | 0 | 0 | 0 | 0 |
| 10-15 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-16 | 0 | 1 | 0 | 0 | 0 | 0 |
| 10-17 | 1 | 0 | 0 | 0 | 0 | 0 |
| 10-18 | 0 | 0 | 0 | 0 | 2 | 0 |
| 10-19 | 0 | 0 | 0 | 0 | 0 | 0 |
| **7 days** | **3** | **1** | **0** | **0** | **4** | **0** |

| Ambassadors | Yesterday | 7 days | Total |
|---|---:|---:|---:|
| Granted | 1 | 1 | 7 |
| Invitations sent (app contributors) | 0 | 1 | 7 |
| Open-seat requests answered | 0 | 0 | 0 |
- New in 7 days: Hidde (Baarn) since 2026-10-18.
- Android waitlist: 22 total, newest 3 days ago
- Submissions: 37 total (19 trees sent, 18 feedback), newest yesterday
- Accounts:    29 total, newest 2 days ago

**What readers told us** (7 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 10-13 | sev_009 (The Fig of the Glorieta d | worth it | - | c922 | - |
| 10-13 | - | Location not working on iOS, permi | - | c922 | open_question |
| 10-18 | The Yew of Campo Santana | correction sent in | 49 chars, read it in the database | 08aa | - |
| 10-18 | lis_014 (The Yew of Campo Santana) | worth it | - | 08aa | - |
| 10-18 | lis_014 (The Yew of Campo Santana) | vote undone | worth it | 08aa | - |

- 3 of the other 5 came from one account (08aa), which is one person rather than a pattern.

**The funnel, as rates**
- Seen to clicked: 3.8% (12 of 317) vs 4.9% the week before
- Pages per visit: 1.3 (7430 visits, 9670 pageviews since 2026-09-21)
- Visits that did something: 9.9% (735 actions on 7430 visits)

**What people did in the app**

| What | Yesterday | 7 days | Last |
|---|---:|---:|---|
| app_open | 19 | 124 | today |
| tab | 15 | 82 | yesterday |
| tree_opened | 89 | 237 | yesterday |
| directions | 1 | 3 | yesterday |
| tree_saved | 0 | 8 | 2 days ago |
| tree_visited | 3 | 3 | yesterday |
| sighting_recorded | 8 | 8 | yesterday |
| sync_skipped | 0 | 0 | never |
| sync_failed | 0 | 0 | never |
| location | 2 | 9 | yesterday |
| **all** | **137** | **474** | |
- Measuring since 2026-08-30, when Measure.swift went in. Unlinked to any account by design: an install id, the app version and the OS, nothing else.
- 94 installs have ever sent anything. An install id is made fresh on each install, so this is an upper bound on people, not a count of them.
- Yesterday came from 7 installs, and the busiest made 34 of 7 events (486%). One install making most of a day is what our own reinstall looks like: add its id to excluded_installs in data/app-measure.json if it is ours.
- Tabs opened (7d): Discover 32; My trees 30; Map 20
- Active phones: 7 in the last day, 20 in the last 7 days, 66 in the last 30 days.
- Coming back: 29 of those 66 phones opened the app on more than one day (44%).
- Trees opened by the most phones (7d): The Fig of the Glorieta de Goya (Seville) 3; The Ombú of La Cartuja (Seville) 2; The Yew of Campo Santana (Lisbon) 2; The Paperbark of Jardim Constantino (Lisbon) 2; The Moreton Bay Fig of Jardim Constantino (Lisbon) 2
- Where the phones are (30d): United States 16; The Netherlands 8; United Kingdom 7; Portugal 6; Spain 4; Italy 4
- Trees recorded (7d): a tree we map 5; a tree we do not 3
  A sighting reaches our database only through an account. Signed out it stays on the phone, so this count can run ahead of the trees and photographs we actually receive.

**Trees collected in the app** (7 days, a person standing at the tree)

| Day | Tree | Where | Install | Build | Signed in |
|---|---|---|---|---|---|
| 10-18 | The Yew of Campo Santana | Lisbon | B792 | ? | ? |
| 10-18 | The Moreton Bay Fig of Jardim Constantino | Lisbon | B792 | ? | ? |
| 10-18 | The Paperbark of Jardim Constantino | Lisbon | B792 | ? | ? |

**The app as a builder reads it** (this week against the week before; the weakest row is the work)

| Link | This week | Week before |
|---|---|---|
| New phones | 14 | 12 |
| First day: opened a tree | 12 of 14 (86%) | 7 of 12 (58%) |
| First day: opened a tree near them | 2 of 4 (50%) | - |
| First day: allowed location | 5 of 5 (100%) | - |
| First day: Take me there | 2 of 14 (14%) | 1 of 12 (8%) |
| First day: collected a tree | 1 of 14 (7%) | 1 of 12 (8%) |
| Back within a week | 2 of 12 (17%) | 5 of 9 (56%) |
| Trees collected (all phones) | 6 | 5 |
- Near and location count only phones on a version that sends them (from 2026-10-10); a dash means none yet.
- Back within a week looks at the phones that arrived a week earlier, so each has had its seven days.

**App Store downloads** (Apple's own count, not PostHog)

| Day | Downloads |
|---|---:|
| 2026-10-10 | 5 |
| 2026-10-12 | 1 |
| 2026-10-13 | 2 |
| 2026-10-15 | 1 |
| 2026-10-16 | 2 |
| 2026-10-17 | 3 |
| **6 days** | **14** |
- First-time downloads only, which is what App Store Connect's Trends screen counts; redownloads and updates are not in this table.

**Where the downloads came from** (7 days, Apple's attribution)

| Came from | Via | Downloads |
|---|---|---:|
| App Store search | - | 8 |
| Web referrer | - | 3 |
| App referrer | - | 2 |
| App Store browse | - | 1 |
| **window** | | **14** |
- Countries: US (6); NL (2); DE (1); DK (1); GB (1); IE (1)
- Apple's own source split, first-time downloads only. "Web referrer" with our own domain is the site's app page; "App Store search" is somebody who typed into the store. "Unavailable" is Apple's word for a source it could not attribute.

**App crashes** (last 7 days, store builds; MetricKit, a sample)

| Crashes | Kind | Build | Where | Phones | Last | Fix |
|---:|---|---|---|---:|---|---|
| 37 | crash | 1.0.2 (20) | Swift runtime failure: Index out of range < static MyVotes.treeId(_:) (WorthIt.swift:84) < MyVotes.load(account:) (WorthIt.swift:103) | 1 | 2026-10-16 | fixed in build 35, released; contained server-side |
- Builds not from the App Store (Xcode or review): 2 report(s) on build 25.

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-09 | 3 | 37 | 8.1% | 49.5 |
| 10-10 | 0 | 35 | 0.0% | 29.8 |
| 10-11 | 1 | 32 | 3.1% | 31.7 |
| 10-12 | 1 | 26 | 3.8% | 30.3 |
| 10-13 | 1 | 34 | 2.9% | 38.7 |
| 10-14 | 1 | 39 | 2.6% | 36.9 |
| 10-15 | 2 | 40 | 5.0% | 37.0 |
| 10-16 | 3 | 73 | 4.1% | 53.0 |
| 10-17 | 2 | 62 | 3.2% | 44.6 |
| 10-18 *partial* | 2 | 43 | 4.7% | 41.6 |
| **window** | **16** | **421** | **3.8%** | |
- Top queries (10d): amsterdam trees (i1, p81); ancient tree (i1, p89); ancient trees (i1, p82); araucaria norfolk island pine (i1, p86); arboles de cadiz (i5, p72)
- Top pages (10d): / (c5/i21); /leiden/beets-beech-of-the-burcht (c2/i2); /app (c1/i9); /seville (c1/i5); /de (c1/i3)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'big sherman tree' (i2, p69)
    - 'big macadamia' (i1, p100)
    - 'bunya tree' (i1, p97)
    - 'canary island dates' (i1, p99)
    - 'chapina garden' (i1, p13)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-11 | 53 | 2 | 3.8% |
| 10-12 | 81 | 3 | 3.7% |
| 10-13 | 90 | 2 | 2.2% |
| 10-14 | 94 | 3 | 3.2% |
| 10-15 | 78 | 8 | 10.3% |
| 10-16 | 70 | 2 | 2.9% |
| 10-17 | 57 | 3 | 5.3% |
| **7 days** | **523** | **23** | **4.4%** |
- Week before: 537 impressions, 18 clicks. No Bing demotion in sight.
- Top Bing queries: fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); how old are the trees in queen square bristol (c1/i4, p3); oak tree in zurich (c1/i4, p2); trees in the plaza dus burgos seville (c1/i3, p5); remarkable trees copenhagen (c1/i2, p4); berlin tree (c1/i2, p1); oldest tree in belfast (c1/i2, p1)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers; their arrivals are columns in the Cloudflare table. Bing's data lags about two days.

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 463 |
| Clicks | 16 |
| Pages that got at least one impression | 247 |
| Impressions on the proven cities | 290 |

- 342 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 2973 trees Google may index, 776 kept out for lacking a photo and an exact pin, 4585 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 615 | 27 | 72 | 0.12 | 3 |
| Not yet rich | 528 | 23 | 43 | 0.08 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| sequoia-national-park | 0 | 38 | 0.0% | 73.1 | 0.4% | general sherman tree california (i4, p74) |

- Plus 258 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| before 2026-09-23 | The Twisted Muku of Omiya Gate, Kyoto  | Kyoto | - | publish | - |
| 2026-10-18 | The Tulip Tree of Cantonspark | - | - | lead | - |
| 2026-10-18 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | - |
| 2026-10-18 | The Moreton Bay Fig of Jardim Constant | Lisbon | - | publish | - |
| 2026-10-18 | The Paperbark of Jardim Constantino | Lisbon | - | publish | - |
| 2026-10-18 | A tree in Baarn | - | - | lead | - |
| 2026-10-18 | Moreton Bay Fig | - | - | open | - |
| 2026-10-15 | The Meiji Jingu Gaien Ginkgo Avenue | - | - | lead | - |
| 2026-10-13 | The Great Lawn Plane of Parc Montsouri | Paris | 88% girth | publish | publish (2026-10-13, session: 'follow your suggestion') |
| 2026-10-12 | The Town Hall Plane | Baarn | - | publish | - |
| 2026-10-12 | The Town Hall Plane | Baarn | - | publish | - |
| 2026-10-12 | The Town Hall Plane | Baarn | - | hold | - |
| 2026-10-12 | The Lagunària de la Llotja | Palma de Mallorca | - | publish | publish: Hidde's own call on 2026-10-12 ('if users have good input - just use it') |
| 2026-10-06 | A tree in Tokyo | - | - | lead | - |
| 2026-10-06 | A tree in Tokyo | - | - | lead | - |

1 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.
- Seen, not clicked: /sequoia-national-park/general-sherman-tree (c0/i32, 0.0%) for general sherman tree california (i4, p74); sherman tree (i3, p78); sequoia national park general sherman (i3, p64)

**Who they are** (full cut, Mondays)
Audience, 28 days of search (417 clicks, 16212 impressions):
- Countries: usa c62/i3446; deu c40/i989; esp c39/i1341; nld c35/i864; gbr c33/i1140
- Devices: MOBILE c294/i9577; DESKTOP c120/i6433; TABLET c3/i202
- Landing pages: / c23/i174; /prague c6/i127; /seville c6/i77; /de/graz c5/i44; /de/vienna/chestnut-avenue-of-the-hauptallee c5/i128
- Search language (top 100 named queries, crude match, most clicks are in queries Google withholds): English 33q c7/i173; unclassified 43q c13/i143; Spanish 14q c0/i25; German 3q c0/i24; French 4q c0/i5; Italian 2q c0/i2; Portuguese 1q c0/i2
On the site since 2026-09-21 (7430 visits, 9670 pageviews, 1.3 pages per visit):
- Countries: SG 2410; US 1250; DE 480; BR 470; NL 400
- Devices: desktop 7510; mobile 2130; tablet 30
- Browsers: Chrome 4730; Firefox 1330; Edge 1030; ChromeMobile 930
- Arrived via: (direct) 6630; ancienttrees.app 2240; www.google.com 450; duckduckgo.com 110; www.facebook.com 50
- Opened: /open 890; /contribute 250; / 210; /explore 120; /florence 80; /lisbon 80; /countries 70; /cities 60

fetch_rum: failed today (rum graphql: [{"message": "unable to execute query, please try again later", "path": ["vie).


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-18T08:29 | 5.1 | 0 | 7 | 0 | - |
| 10-18T13:43 | 10.1 | 6 | 8 | 0 | Leipzig +3, London +1, Salt Lake City +1, Vienna +1 |
| 10-18T17:02 | 112.1 | 19 | 36 | 2 | Leipzig +7, Frankfurt +6, Delft +3, Stuttgart +3, +13 more |
| 10-18T19:57 | 67.1 | 1 | 11 | 1 | Spokane +1, Austin, Berlin, Dallas, +14 more |
| 10-18T22:16 | 22.7 | 0 | 6 | 0 | Berlin, New York, Portland, Washington Dc |
| 10-19T00:31 | 14.5 | 1 | 5 | 1 | London +1, Delft |
| 10-19T02:51 | 5.5 | 0 | 4 | 0 | - |
| 10-19T05:21 | 35.8 | 17 | 15 | 6 | Miami +7, Innsbruck +6, Key West +2, London +1, +1 more |
| **8 runs** | **273** | **44** | **92** | | |

- 3 of 8 produced no trees; 1 to 6 commands refused per run; last build that went live: 0h ago.

**What they made**

- Photo pass: two Innsbruck oaks approved, costs and log
- Photo viewing pass: Innsbruck oaks inn_003 and inn_006 approved, kyw_002 held, 20 candidates rejected
- Innsbruck opens with six trees, claim released, costs and log
- Innsbruck write pass: six register trees as a new place, inn_007 held
- Innsbruck verify pass: seven register trees (flagged), leads and blocked recorded
- Miami, Key West, Novo Selo: five more trees live, claim released, costs and log
- Miami, Key West and Novo Selo write pass: five trees, page copy updated
- Miami and Key West verify pass: four trees verified (flagged), leads and blocked recorded
- Miami, Key West and London: six trees live, claim released, costs and log
- Miami and London write pass: four Miami trees, Key West mamey, Roehampton Lucombe Oak
- Las Vegas verify pass: two UNLV champions flagged, not written; claim released, log and costs
- Record when each page last changed
- Scouting: London and Edinburgh retried 2026-10-19, still stalled
- London: add the Osterley Park Cork Oak with photograph, count copy follows

**Photographs the night run approved** (40; the last column undoes one)

| Day | Tree | Where | Overrule |
|---|---|---|---|
| 10-18 | The Velvet-leaf Euodia of Fischerinsel | Berlin | `photo_apply.py hold ber_047` |
| 10-18 | The Oak between the Neuer See and the Landwehr Canal | Berlin | `photo_apply.py hold ber_059` |
| 10-18 | The Post Oak Grove of Pioneer Park Cemetery | Dallas | `photo_apply.py hold dal_012` |
| 10-18 | The Paradieseiche of Sachsenhausen | Frankfurt | `photo_apply.py hold frk_008` |
| 10-18 | The Peace Oak of Sossenheim | Frankfurt | `photo_apply.py hold frk_010` |
| 10-18 | The Cemetery Lindens of Nieder-Erlenbach | Frankfurt | `photo_apply.py hold frk_014` |
| 10-18 | The Chestnut at the Schaeferkoeppel | Frankfurt | `photo_apply.py hold frk_016` |
| 10-18 | The August Reiss Oak of Offenbach | Frankfurt | `photo_apply.py hold frk_017` |
| 10-19 | The Münzgrabenstrasse Oriental Plane | Graz | `photo_apply.py hold grz_016` |
| 10-19 | The Independence Spruce | Helsinki | `photo_apply.py hold hel_010` |
| 10-18 | The Banyan of Nathan Road | Hong Kong | `photo_apply.py hold hkg_010` |
| 10-19 | The Schulgasse Oak in Hötting | Innsbruck | `photo_apply.py hold inn_003` |
| 10-19 | The Traklpark Oak | Innsbruck | `photo_apply.py hold inn_006` |
| 10-18 | The Oak of Probstheida Village Green | Leipzig | `photo_apply.py hold lpz_023` |
| 10-18 | The Japanese Pagoda Tree of Flossplatz | Leipzig | `photo_apply.py hold lpz_024` |
| 10-18 | The Oak of Kantatenweg | Leipzig | `photo_apply.py hold lpz_025` |
| 10-18 | The Steinlinde of Plausig | Leipzig | `photo_apply.py hold lpz_027` |
| 10-18 | The Marble Hill Black Walnut | London | `photo_apply.py hold lon_029` |
| 10-19 | The Osterley Park Cork Oak | London | `photo_apply.py hold lon_032` |
| 10-18 | El Pino (The Pine Tree) | Los Angeles | `photo_apply.py hold lax_013` |
| 10-18 | The Eucalyptus of the Villa Comunale | Naples | `photo_apply.py hold nap_020` |
| 10-18 | The London Plane of the Reservoir | New York | `photo_apply.py hold nyc_019` |
| 10-18 | The Corbett Oak | Portland | `photo_apply.py hold ptl_021` |
| 10-18 | The Hiawatha Playfield Red Oak | Seattle | `photo_apply.py hold sea_009` |
| 10-18 | The Roanoke Park European White Elm | Seattle | `photo_apply.py hold sea_017` |
| 10-18 | Sentinel Tree | Sequoia National Park | `photo_apply.py hold seq_007` |
| 10-18 | Bellmanseken | Stockholm | `photo_apply.py hold sto_007` |
| 10-18 | The Schillereiche | Stuttgart | `photo_apply.py hold stu_008` |
| 10-18 | The Wernhalde Giant Sequoias | Stuttgart | `photo_apply.py hold stu_009` |
| 10-18 | The Jahneiche | Stuttgart | `photo_apply.py hold stu_010` |
| 10-18 | The Camphor Tree of Hongo Yumicho | Tokyo | `photo_apply.py hold tok_022` |
| 10-18 | The Oriental Plane of the Abraham Dolehof | Utrecht | `photo_apply.py hold utr_035` |
| 10-18 | The Maurer Schubertpark Lime | Vienna | `photo_apply.py hold vie_049` |
| 10-18 | The Oberlaa Horse Chestnut | Vienna | `photo_apply.py hold vie_056` |
| 10-18 | The Strassergasse Oak | Vienna | `photo_apply.py hold vie_058` |
| 10-18 | The Ash of Mickiewicz's Courtyard | Vilnius | `photo_apply.py hold vln_004` |
| 10-18 | The Smithsonian Witness Elm | Washington DC | `photo_apply.py hold wdc_015` |
| 10-18 | Travilah Oak | Washington DC | `photo_apply.py hold wdc_016` |
| 10-19 | Takinoya no Hidarimakigaya | Yabu | `photo_apply.py hold yab_002` |
| 10-18 | The Four-Trunked Survivor | Ypres | `photo_apply.py hold ypr_005` |

Machine: 7 chain attempts yesterday, 7 got real work time (~237 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Monday: the slow tables.** They rarely change a day's decision, so they come once a week.

**Website actions, ever** (the events table begins 2026-08-01, when the funnel was repaired; a zero has never fired at all)

| Action | Ever |
|---|---:|
| signin-open | 505 |
| app-cta | 51 |
| signin-oauth | 40 |
| signin-done | 38 |
| directions | 36 |
| search-home | 31 |
| app-open | 21 |
| suggestion-submit | 17 |
| home-country | 11 |
| home-fav | 7 |
| signin-link-sent | 6 |
| save | 5 |
| waitlist-submit | 5 |
| home-dir-tree | 4 |
| search-explore | 4 |
| visit | 3 |
| search-bar | 2 |
| app-page-badge | 2 |
| home-species | 2 |
| search-bar-m | 2 |
| sponsor-open | 2 |
| home-dir-city | 1 |
| home-dir-species | 1 |
| walks-app | 1 |
| worthit-report | 1 |
| worthit-report detail | 1 |
| worthit-worth it | 1 |
| worthit-not worth it | 0 |
| **all** | **800** |

**App events, ever** (measured since 2026-08-30)

| What | Ever |
|---|---:|
| app_open | 415 |
| tab | 394 |
| tree_opened | 1465 |
| directions | 48 |
| tree_saved | 27 |
| tree_visited | 30 |
| sighting_recorded | 81 |
| sync_skipped | 0 |
| sync_failed | 0 |
| location | 9 |
| **all** | **2469** |

**Bing's index** (pages crawled and in index, Bing Webmaster Tools)

| Day | Pages crawled | Pages in index |
|---|---:|---:|
| 10-11 | 155 | 2600 |
| 10-12 | 173 | 2447 |
| 10-13 | 210 | 2447 |
| 10-14 | 426 | 2600 |
| 10-15 | 361 | 2668 |
| 10-16 | 358 | 2668 |
| 10-17 | 249 | 2775 |
- In index the week before: 2447.

**The language test** (Contract J v1.13: a translated set should pass its English twin's impressions within four weeks of indexing):

| Lang | City | Clicks | Impressions | Position | English twin |
|---|---|---:|---:|---:|---:|
| es | tenerife | 0 | 9 | 78.0 | 2 |
| de | vienna | 0 | 7 | 8.1 | 2 |
| es | cadiz | 0 | 6 | 71.2 | 1 |
| de | berlin | 1 | 5 | 32.2 | 2 |
| de | graz | 0 | 5 | 47.0 | 1 |
| es | barcelona | 0 | 5 | 47.4 | 2 |
| pt | rio-de-janeiro | 0 | 4 | 9.8 | 0 |
| nl | amsterdam | 0 | 3 | 43.3 | 4 |
| de | stuttgart | 1 | 2 | 9.0 | 1 |
| de | leiden | 0 | 2 | 7.0 | 8 |
| es | seville | 0 | 2 | 11.5 | 6 |
| fr | paris | 0 | 2 | 8.0 | 4 |
| it | leiden | 0 | 2 | 4.0 | 8 |
| nl | arnhem | 0 | 2 | 88.0 | 1 |
| pt | leiden | 0 | 2 | 6.0 | 8 |
| de | munich | 0 | 2 | 9.5 | 9 |
| ja | yakushima | 0 | 2 | 97.5 | 4 |
| nl | the-hague | 0 | 2 | 40.5 | 0 |
| de | cologne | 0 | 1 | 7.0 | 0 |
| de | nuremberg | 0 | 1 | 8.0 | 0 |
| de | zurich | 0 | 1 | 10.0 | 0 |
| es | pamplona | 0 | 1 | 54.0 | 0 |
| fr | geneva | 0 | 1 | 1.0 | 3 |
| fr | lyon | 0 | 1 | 80.0 | 1 |
| fr | nice | 0 | 1 | 6.0 | 0 |
| it | cagliari | 0 | 1 | 70.0 | 2 |
| it | naples | 0 | 1 | 12.0 | 0 |
| it | palermo | 0 | 1 | 92.0 | 2 |
| ja | osaka | 0 | 1 | 7.0 | 2 |
| nl | nijmegen | 0 | 1 | 58.0 | 0 |
| pt | lisbon | 0 | 1 | 4.0 | 4 |

**Google Analytics** (last 7 days, visitors who accepted cookies)

| Day | People | New | Returning | Visits | Pageviews | Engaged visits |
|---|---:|---:|---:|---:|---:|---:|
| 10-12 | 3 | 3 | 0 | 4 | 7 | 3 |
| 10-13 | 8 | 8 | 0 | 10 | 38 | 6 |
| 10-14 | 4 | 4 | 0 | 4 | 8 | 3 |
| 10-15 | 4 | 3 | 1 | 4 | 13 | 3 |
| 10-16 | 2 | 2 | 0 | 2 | 3 | 2 |
| 10-17 | 3 | 3 | 0 | 6 | 30 | 3 |
| **window** | | **23** | | **30** | **99** | **20** |
- People per day are not summed: one person on two days is one person, and GA counts them once per day.
- Coming back (28 days): 4 returning against 23 new, 15% of the people GA saw.

| Page | Pageviews | People |
|---|---:|---:|
| / | 5 | 4 |
| /privacy | 5 | 3 |
| /estry | 4 | 1 |
| /cardiff/bute-park-sweet-chestnut | 3 | 1 |
| /terms | 3 | 1 |
| /about | 2 | 1 |
| /amsterdam/rijksmuseum-wingnut | 2 | 1 |
| /cologne | 2 | 2 |
| /cologne/hohenlind-oak | 2 | 1 |
| /de | 2 | 1 |

| Came from | Visits | People |
|---|---:|---:|
| (direct) / (none) | 22 | 16 |
| ecosia.org / organic | 2 | 2 |
| google / organic | 2 | 1 |
| bing / organic | 1 | 1 |
| dias-com-arvores.blogspot.com / referral | 1 | 1 |
| duckduckgo / organic | 1 | 1 |
| teams.public.onecdn.static.microsoft / referral | 1 | 1 |
- GA sees only visitors who pressed Accept on the cookie bar; read it as a sample. Cloudflare's table stays the count.

## 2026-10-17 (previous UTC day)

**Today: an account was opened yesterday (29 total).**

**Conclusion: the numbers that matter now** (this week against the week before)

| Number | Why it counts | This week | Week before |
|---|---|---:|---:|
| Stood at a tree (app collections) | goal 1, the north star | 5 | 7 |
| New phones that opened a tree on day one | activation | 11 of 14 (79%) | 7 of 11 (64%) |
| New phones that tapped Take me there on day one | activation | 1 of 14 (7%) | 1 of 11 (9%) |
| Phones back within a week | retention | 3 of 11 (27%) | 4 of 8 (50%) |
| New accounts (strangers) | people collected | 4 | 4 |
| Readers' trees and photographs live | data collected | 2 | 2 |
| Arrivals from search, every engine (8 days) | traction | 90 | - |

5 collections at a tree this week against 7 the week before, a handful: read it as a count, not a trend. The weakest link is tapping Take me there on day one (1 of 14): that step is the work, more traffic only pours more people into it.

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Did the product happen**

| Action | Yesterday | 7 days | Last |
|---|---:|---:|---|
| signin-open | 0 | 9 | 2 days ago |
| app-cta | 2 | 14 | yesterday |
| signin-oauth | 0 | 0 | 9 days ago |
| signin-done | 0 | 0 | 11 days ago |
| directions | 0 | 0 | 9 days ago |
| search-home | 1 | 5 | yesterday |
| app-open | 0 | 2 | 2 days ago |
| suggestion-submit | 0 | 0 | 23 days ago |
| home-country | 0 | 2 | 3 days ago |
| home-fav | 0 | 0 | 9 days ago |
| signin-link-sent | 0 | 0 | 23 days ago |
| save | 0 | 0 | 16 days ago |
| waitlist-submit | 0 | 1 | 2 days ago |
| home-dir-tree | 0 | 1 | 3 days ago |
| search-explore | 0 | 2 | 2 days ago |
| visit | 0 | 0 | 28 days ago |
| search-bar-m | 2 | 2 | yesterday |
| app-page-badge | 0 | 0 | 9 days ago |
| home-species | 0 | 0 | 27 days ago |
| search-bar | 0 | 2 | today |
| sponsor-open | 0 | 1 | 3 days ago |
| home-dir-city | 1 | 1 | yesterday |
| home-dir-species | 0 | 1 | 7 days ago |
| walks-app | 0 | 0 | 25 days ago |
| worthit-report | 0 | 0 | 24 days ago |
| worthit-report detail | 0 | 0 | 24 days ago |
| worthit-worth it | 0 | 0 | 28 days ago |
| worthit-not worth it | 0 | 0 | never |
| **all** | **6** | **43** | |

**Searched yesterday:** amsterdam, brighton.

| Day | Accounts | Android waitlist | Saves | Trees sent | Feedback | Ambassador asks |
|---|---:|---:|---:|---:|---:|---:|
| 10-11 | 1 | 0 | 0 | 0 | 0 | 0 |
| 10-12 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-13 | 1 | 0 | 0 | 0 | 2 | 0 |
| 10-14 | 1 | 0 | 0 | 0 | 0 | 0 |
| 10-15 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-16 | 0 | 1 | 0 | 0 | 0 | 0 |
| 10-17 | 1 | 0 | 0 | 0 | 0 | 0 |
| 10-18 | 0 | 0 | 0 | 0 | 0 | 0 |
| **7 days** | **4** | **1** | **0** | **0** | **2** | **0** |

| Ambassadors | Yesterday | 7 days | Total |
|---|---:|---:|---:|
| Granted | 1 | 1 | 7 |
| Invitations sent (app contributors) | 0 | 1 | 7 |
| Open-seat requests answered | 0 | 0 | 0 |
- New in 7 days: Baarn since 2026-10-18.
- Android waitlist: 22 total, newest 2 days ago
- Submissions: 35 total (19 trees sent, 16 feedback), newest 5 days ago
- Accounts:    29 total, newest yesterday

**What readers told us** (7 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 10-13 | sev_009 (The Fig of the Glorieta d | worth it | - | c922 | - |
| 10-13 | - | Location not working on iOS, permi | - | c922 | open_question |

- 2 rows from 1 accounts.

**The funnel, as rates**
- Seen to clicked: 3.7% (11 of 298) vs 4.6% the week before
- Pages per visit: 1.3 (7380 visits, 9270 pageviews since 2026-09-20)
- Visits that did something: 11.0% (809 actions on 7380 visits)

**What people did in the app**

| What | Yesterday | 7 days | Last |
|---|---:|---:|---|
| app_open | 15 | 112 | today |
| tab | 26 | 74 | today |
| tree_opened | 18 | 185 | today |
| directions | 1 | 3 | today |
| tree_saved | 4 | 8 | yesterday |
| tree_visited | 0 | 3 | today |
| sighting_recorded | 0 | 6 | today |
| sync_skipped | 0 | 0 | never |
| sync_failed | 0 | 0 | never |
| location | 3 | 7 | yesterday |
| **all** | **67** | **398** | |
- Measuring since 2026-08-30, when Measure.swift went in. Unlinked to any account by design: an install id, the app version and the OS, nothing else.
- 92 installs have ever sent anything. An install id is made fresh on each install, so this is an upper bound on people, not a count of them.
- Yesterday came from 6 installs, and the busiest made 38 of 6 events (633%). One install making most of a day is what our own reinstall looks like: add its id to excluded_installs in data/app-measure.json if it is ours.
- Tabs opened (7d): Discover 31; My trees 26; Map 17
- Active phones: 7 in the last day, 20 in the last 7 days, 64 in the last 30 days.
- Coming back: 28 of those 64 phones opened the app on more than one day (44%).
- Trees opened by the most phones (7d): The Fig of the Glorieta de Goya (Seville) 3; The Ombú of La Cartuja (Seville) 2; The Paperbark of Jardim Constantino (Lisbon) 2; The Moreton Bay Fig of Jardim Constantino (Lisbon) 2; The Grapefruit of the Cartuja Monastery (Seville) 1
- Where the phones are (30d): United States 15; United Kingdom 7; The Netherlands 7; Portugal 6; Spain 4; Italy 4
- Trees recorded (7d): a tree we map 4; a tree we do not 2
  A sighting reaches our database only through an account. Signed out it stays on the phone, so this count can run ahead of the trees and photographs we actually receive.

**Trees collected in the app** (7 days, a person standing at the tree)

| Day | Tree | Where | Install | Build | Signed in |
|---|---|---|---|---|---|
| 10-18 | The Moreton Bay Fig of Jardim Constantino | Lisbon | B792 | ? | ? |
| 10-18 | The Paperbark of Jardim Constantino | Lisbon | B792 | ? | ? |
| 10-11 | The Lagunària de la Llotja | Palma de Mallorca | A98A | ? | ? |

**The app as a builder reads it** (this week against the week before; the weakest row is the work)

| Link | This week | Week before |
|---|---|---|
| New phones | 14 | 11 |
| First day: opened a tree | 11 of 14 (79%) | 7 of 11 (64%) |
| First day: opened a tree near them | 1 of 2 (50%) | - |
| First day: allowed location | 3 of 3 (100%) | - |
| First day: Take me there | 1 of 14 (7%) | 1 of 11 (9%) |
| First day: collected a tree | 1 of 14 (7%) | 1 of 11 (9%) |
| Back within a week | 3 of 11 (27%) | 4 of 8 (50%) |
| Trees collected (all phones) | 5 | 7 |
- Near and location count only phones on a version that sends them (from 2026-10-10); a dash means none yet.
- Back within a week looks at the phones that arrived a week earlier, so each has had its seven days.

**App Store downloads** (Apple's own count, not PostHog)

| Day | Downloads |
|---|---:|
| 2026-10-09 | 4 |
| 2026-10-10 | 5 |
| 2026-10-12 | 1 |
| 2026-10-13 | 2 |
| 2026-10-15 | 1 |
| 2026-10-16 | 2 |
| **6 days** | **15** |
- First-time downloads only, which is what App Store Connect's Trends screen counts; redownloads and updates are not in this table.

**Where the downloads came from** (7 days, Apple's attribution)

| Came from | Via | Downloads |
|---|---|---:|
| App Store search | - | 8 |
| Web referrer | - | 4 |
| App referrer | - | 2 |
| App Store browse | - | 1 |
| **window** | | **15** |
- Countries: US (6); GB (2); NL (2); BE (1); DK (1); IE (1)
- Apple's own source split, first-time downloads only. "Web referrer" with our own domain is the site's app page; "App Store search" is somebody who typed into the store. "Unavailable" is Apple's word for a source it could not attribute.

**App crashes** (last 7 days, store builds; MetricKit, a sample)

| Crashes | Kind | Build | Where | Phones | Last | Fix |
|---:|---|---|---|---:|---|---|
| 37 | crash | 1.0.2 (20) | Swift runtime failure: Index out of range < static MyVotes.treeId(_:) (WorthIt.swift:84) < MyVotes.load(account:) (WorthIt.swift:103) | 1 | 2026-10-16 | fixed in build 35, released; contained server-side |
- Builds not from the App Store (Xcode or review): 6 report(s) on build 25.

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-08 | 5 | 35 | 14.3% | 21.8 |
| 10-09 | 3 | 37 | 8.1% | 49.5 |
| 10-10 | 0 | 35 | 0.0% | 29.8 |
| 10-11 | 1 | 32 | 3.1% | 31.7 |
| 10-12 | 1 | 26 | 3.8% | 30.3 |
| 10-13 | 1 | 34 | 2.9% | 38.7 |
| 10-14 | 1 | 39 | 2.6% | 36.9 |
| 10-15 | 2 | 40 | 5.0% | 37.0 |
| 10-16 | 3 | 73 | 4.1% | 53.0 |
| 10-17 *partial* | 2 | 54 | 3.7% | 40.0 |
| **window** | **19** | **405** | **4.7%** | |
- Top queries (10d): pokaz na mapie (i1, p1); amsterdam trees (i1, p81); ancient tree (i1, p89); ancient trees (i1, p82); arboles de cadiz (i4, p72)
- Top pages (10d): / (c5/i17); /brussels/oldest-tree (c2/i3); /leiden/beets-beech-of-the-burcht (c2/i2); /app (c1/i6); /seville (c1/i5)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'big sherman tree' (i2, p69)
    - 'pokaz na mapie' (i1, p1)
    - 'big macadamia' (i1, p100)
    - 'bunya tree' (i1, p97)
    - 'canary island dates' (i1, p99)
    - 'chapina garden' (i1, p13)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-10 | 57 | 1 | 1.8% |
| 10-11 | 53 | 2 | 3.8% |
| 10-12 | 81 | 3 | 3.7% |
| 10-13 | 90 | 2 | 2.2% |
| 10-14 | 94 | 3 | 3.2% |
| 10-15 | 78 | 8 | 10.3% |
| 10-16 | 70 | 2 | 2.9% |
| **7 days** | **523** | **21** | **4.0%** |
- Week before: 527 impressions, 21 clicks. No Bing demotion in sight.
- Top Bing queries: fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); how old are the trees in queen square bristol (c1/i4, p3); oak tree in zurich (c1/i4, p2); trees in the plaza dus burgos seville (c1/i3, p5); ancient trees in wiesbaden germany (c1/i2, p6); husalle lindens copenhagen (c1/i2, p3); oldest live oak trees in new orleans (c1/i2, p6)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers; their arrivals are columns in the Cloudflare table. Bing's data lags about two days.

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 448 |
| Clicks | 19 |
| Pages that got at least one impression | 248 |
| Impressions on the proven cities | 295 |

- 342 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 2951 trees Google may index, 748 kept out for lacking a photo and an exact pin, 4571 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 589 | 27 | 70 | 0.12 | 4 |
| Not yet rich | 510 | 28 | 52 | 0.10 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| sequoia-national-park | 0 | 39 | 0.0% | 73.0 | 0.4% | general sherman tree california (i4, p74) |
| brussels | 2 | 10 | 20.0% | 12.9 | 1.6% | klint white mulberry (i2, p52) |

- Plus 257 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| before 2026-09-23 | The Twisted Muku of Omiya Gate, Kyoto  | Kyoto | - | publish | - |
| 2026-10-18 | The Tulip Tree of Cantonspark | - | - | open | - |
| 2026-10-15 | The Meiji Jingu Gaien Ginkgo Avenue | - | - | open | - |
| 2026-10-13 | The Great Lawn Plane of Parc Montsouri | Paris | 88% girth | publish | publish (2026-10-13, session: 'follow your suggestion') |
| 2026-10-12 | The Town Hall Plane | Baarn | - | publish | - |
| 2026-10-12 | The Town Hall Plane | Baarn | - | publish | - |
| 2026-10-12 | The Town Hall Plane | Baarn | - | hold | - |
| 2026-10-12 | The Lagunària de la Llotja | Palma de Mallorca | - | publish | publish: Hidde's own call on 2026-10-12 ('if users have good input - just use it') |
| 2026-10-06 | A tree in Tokyo | - | - | lead | - |
| 2026-10-06 | A tree in Tokyo | - | - | lead | - |
| 2026-10-06 | Ginkgo in Tokyo | - | - | lead | - |
| 2026-10-06 | A tree in Tokyo | - | - | lead | - |
| 2026-10-06 | A tree in Tokyo | - | - | lead | - |
| 2026-10-05 | The Southern Mahogany of Edinburgh Gar | Melbourne | - | publish | - |
| 2026-10-05 | The Finer Holm Oak of Edinburgh Garden | Melbourne | - | hold | hold: a bare deciduous tree, not our evergreen holm oak (discussed 2026-10-13) |

2 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.
- Seen, not clicked: /sequoia-national-park/general-sherman-tree (c0/i34, 0.0%) for general sherman tree california (i4, p74); sherman tree (i3, p78); sequoia national park general sherman (i3, p64)

**Who they are**
Audience, 28 days of search (472 clicks, 18296 impressions):
- Countries: usa c67/i3816; esp c48/i1529; deu c44/i1104; gbr c39/i1373; nld c39/i992
- Devices: MOBILE c337/i11073; DESKTOP c131/i6993; TABLET c4/i230
- Landing pages: / c23/i190; /prague c7/i131; /seville c7/i82; /de/graz c5/i44; /de/vienna/chestnut-avenue-of-the-hauptallee c5/i147

Web Analytics (beacon, cookieless), people only.
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews | From Google | From Bing | From DuckDuckGo | From Yahoo | From Ecosia |
|---|---:|---:|---:|---:|---:|---:|---:|
| 10-10 | 40 | 140 | 10 | 0 | 0 | 0 | 0 |
| 10-11 | 30 | 90 | 0 | 0 | 10 | 0 | 0 |
| 10-12 | 20 | 90 | 0 | 0 | 0 | 10 | 0 |
| 10-13 | 20 | 90 | 0 | 0 | 0 | 0 | 0 |
| 10-14 | 10 | 70 | 0 | 0 | 0 | 0 | 0 |
| 10-15 | 40 | 170 | 10 | 10 | 0 | 0 | 0 |
| 10-16 | 50 | 140 | 10 | 0 | 20 | 0 | 0 |
| 10-17 | 20 | 30 | 10 | 0 | 0 | 0 | 0 |
| **window** | **230** | **820** | **40** | **10** | **30** | **10** | **0** |
- Top paths: /explore (50); /lisbon (40); /contribute (20); /de/cologne/moltke-lime-of-the-kahnweiher (20); /cambridge/newtons-apple-tree (10); /amersfoort/copper-beech-of-the-old-library (10); /london/greenwich-park-shagbark-hickory (10); /glastonbury/glastonbury-thorn (10); /copenhagen/oldest-tree (10); /paris/robinier-of-square-rene-viviani (10); /london/sweet-chestnut-of-greenwich-park (10); /lisbon/paineira-of-rua-dos-jeronimos (10)
- Referrers: (direct) (130); ancienttrees.app (590); www.google.com (40); duckduckgo.com (30); localhost (10); uk.search.yahoo.com (10); www.bing.com (10)
- Moved between our own pages: 590 of 820 pageviews (72%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: DE (110); NL (100); US (90); SG (90); PT (90)
- Devices: mobile (480); desktop (330); tablet (10)
- Page load (8d): p50 1568ms, p90 4942ms

Links: external referrers (a link somebody actually clicked): localhost (10)
AI: arrivals from an assistant that cited us: none yet


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-17T10:59 | 5.1 | 0 | 4 | 0 | - |
| 10-17T13:25 | 2.6 | 0 | 4 | 0 | - |
| 10-17T16:48 | 6.2 | 0 | 3 | 0 | - |
| 10-17T19:32 | 2.3 | 0 | 4 | 0 | - |
| 10-17T19:58 | 5.6 | 0 | 3 | 0 | - |
| 10-17T21:59 | 1.9 | 0 | 4 | 0 | - |
| 10-17T23:54 | 1.3 | 0 | 4 | 0 | - |
| 10-18T02:38 | 2.3 | 0 | 5 | 0 | - |
| 10-18T06:37 | 5.9 | 0 | 5 | 0 | Ypres |
| 10-18T08:29 | 5.1 | 0 | 7 | 0 | - |
| **10 runs** | **38** | **0** | **43** | | |

- 10 of 10 produced no trees; last build that went live: 1h ago.

**What they made**

- Vendor 1 photograph file(s) onto our own domain
- Log: thirty-eighth attempt, nothing shippable
- Log: thirty-seventh attempt, nothing shippable
- Log: thirty-sixth attempt, nothing shippable
- Log: 08:29 window, one sighting verdict
- Sighting c86ff6bf (Cantonspark tulip tree): verdict lead
- Photographs readers sent, queued for a look; vouched ones live
- Record when each page last changed
- Log: thirty-fifth attempt, nothing shippable
- Log: thirty-fourth attempt, nothing shippable
- Detroit register retry: still stalled; log
- Log: 06:37 window, one photograph approved
- Ypres: photograph approved for the Four-Trunked Survivor
- Log: thirty-second attempt, nothing shippable

**Photographs the night run approved** (31; the last column undoes one)

| Day | Tree | Where | Overrule |
|---|---|---|---|
| 10-16 | The Lebanon Oak of the Tiergarten | Berlin | `photo_apply.py hold ber_034` |
| 10-16 | The Silver Lime by the Bismarck Monument | Berlin | `photo_apply.py hold ber_035` |
| 10-16 | The White Elm east of the English Garden | Berlin | `photo_apply.py hold ber_036` |
| 10-16 | The Oak east of the English Garden | Berlin | `photo_apply.py hold ber_037` |
| 10-16 | The Katsura of Altonaer Strasse | Berlin | `photo_apply.py hold ber_038` |
| 10-16 | The Katsura south of the Fauler See | Berlin | `photo_apply.py hold ber_039` |
| 10-16 | The Zehlendorf Peace Oak | Berlin | `photo_apply.py hold ber_040` |
| 10-16 | The Asia Minor Fontanesia of the Kleiner Tiergarten | Berlin | `photo_apply.py hold ber_042` |
| 10-16 | The Tulip Tree of Luiseninsel | Berlin | `photo_apply.py hold ber_043` |
| 10-16 | The Dawn Redwood of the Rehberge | Berlin | `photo_apply.py hold ber_044` |
| 10-16 | The Bosnian Maple of Gendarmenmarkt | Berlin | `photo_apply.py hold ber_045` |
| 10-16 | The Kentucky Coffeetree of Maerkischer Platz | Berlin | `photo_apply.py hold ber_046` |
| 10-16 | The Ginkgo of the Humboldt University Courtyard | Berlin | `photo_apply.py hold ber_048` |
| 10-16 | The Plane Tree of Bebelplatz | Berlin | `photo_apply.py hold ber_050` |
| 10-16 | The Bald Cypress of Buergerpark Pankow | Berlin | `photo_apply.py hold ber_052` |
| 10-16 | The Copper Beeches of the Natural History Museum Forecourt | Berlin | `photo_apply.py hold ber_054` |
| 10-16 | The Sessile Oak by the Carillon | Berlin | `photo_apply.py hold ber_055` |
| 10-16 | The Black Locust of the Victory Column Island | Berlin | `photo_apply.py hold ber_056` |
| 10-16 | The Plane Tree east of the Neuer See | Berlin | `photo_apply.py hold ber_057` |
| 10-16 | The Plane Tree of Lichtensteinallee | Berlin | `photo_apply.py hold ber_058` |
| 10-16 | The Oak of Katharina-Heinroth-Ufer | Berlin | `photo_apply.py hold ber_060` |
| 10-16 | The Oak of Bellevueallee | Berlin | `photo_apply.py hold ber_061` |
| 10-16 | The Beech south of the Kleiner Stern | Berlin | `photo_apply.py hold ber_062` |
| 10-16 | The Fluttering Elm near the Grosse Sternallee Bridge | Berlin | `photo_apply.py hold ber_063` |
| 10-16 | The 500-Year Oak of Berlin Zoo | Berlin | `photo_apply.py hold ber_041` |
| 10-16 | The Battersea Park Hybrid Strawberry Tree | London | `photo_apply.py hold lon_025` |
| 10-16 | The Carshalton Plane | London | `photo_apply.py hold lon_028` |
| 10-16 | The Gunnersbury Park Black Mulberry | London | `photo_apply.py hold lon_030` |
| 10-16 | The Magnolia of Hattie Carthan | New York | `photo_apply.py hold nyc_021` |
| 10-16 | The Silver Poplars of Freiligrathpark | Vienna | `photo_apply.py hold vie_044` |
| 10-18 | The Four-Trunked Survivor | Ypres | `photo_apply.py hold ypr_005` |

Machine: 11 chain attempts yesterday, 11 got real work time (~58 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

