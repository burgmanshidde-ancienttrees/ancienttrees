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

## 2026-09-03 (previous UTC day)

**Today: 2 tree submissions and 1 feedback report arrived yesterday (10 total); an account was opened yesterday (8 total).**

**Did the product happen**

| Action | Yesterday | 14 days | Ever | Last |
|---|---:|---:|---:|---|
| app-cta | 1 | 22 | 47 | yesterday |
| directions | 0 | 44 | 44 | 2 days ago |
| search-home | 0 | 28 | 32 | 2 days ago |
| waitlist-submit | 7 | 13 | 18 | yesterday |
| save | 0 | 7 | 12 | 5 days ago |
| search-explore | 2 | 8 | 10 | today |
| walks-app | 0 | 7 | 10 | 2 days ago |
| suggestion-submit | 0 | 1 | 4 | 5 days ago |
| walk-open | 0 | 0 | 4 | 18 days ago |
| smoke-test | 0 | 0 | 2 | 34 days ago |
| home-fav | 1 | 1 | 1 | yesterday |
| sponsor-open | 1 | 1 | 1 | yesterday |
| beacon-fix-verify | 0 | 0 | 1 | 19 days ago |
| beacon-test | 0 | 0 | 1 | 19 days ago |
| worthit-not worth it | 0 | 0 | 1 | 18 days ago |
| signin-link-sent | 0 | 0 | 0 | never |
| walk-start | 0 | 0 | 0 | never |
| worthit-worth it | 0 | 0 | 0 | never |
| **all** | **12** | **132** | **188** | |
- 'Ever' counts every row in the events table, which begins 2026-08-01 when the funnel was repaired. Anything named here with a zero has never fired at all.

**What people typed into our search** (14 days, 30 searches, 18 different terms)

| Typed | Times |
|---|---:|
| mel | 6 |
| melbourne | 4 |
| melb | 3 |
| milano | 3 |
| berli | 1 |
| ei | 1 |
| glasg | 1 |
| leiden | 1 |
| london | 1 |
| melbo | 1 |
| melbou | 1 |
| oslo | 1 |
| perth | 1 |
| prague | 1 |
| sea | 1 |
| sy | 1 |
| vienna | 1 |
| warszawa | 1 |

| Day | Accounts | Android waitlist | Saves | Trees sent | Feedback |
|---|---:|---:|---:|---:|---:|
| 08-21 | 1 | 0 | 0 | 0 | 1 |
| 08-22 | 0 | 0 | 1 | 0 | 0 |
| 08-23 | 0 | 0 | 0 | 0 | 0 |
| 08-24 | 0 | 0 | 0 | 0 | 0 |
| 08-25 | 0 | 1 | 0 | 0 | 0 |
| 08-26 | 0 | 1 | 1 | 0 | 0 |
| 08-27 | 0 | 1 | 0 | 0 | 1 |
| 08-28 | 0 | 1 | 0 | 0 | 0 |
| 08-29 | 0 | 0 | 0 | 0 | 0 |
| 08-30 | 1 | 0 | 5 | 1 | 0 |
| 08-31 | 0 | 2 | 0 | 0 | 0 |
| 09-01 | 1 | 0 | 0 | 0 | 0 |
| 09-02 | 1 | 0 | 0 | 0 | 0 |
| 09-03 | 2 | 0 | 0 | 2 | 1 |
| 09-04 | 0 | 0 | 0 | 0 | 0 |
| **14 days** | **6** | **6** | **7** | **3** | **3** |
- Our own rows are not in this table: 10 trees, 22 feedback, 2 accounts. They are testing, and counting them reads as traction.
- Android waitlist: 16 total, newest 4 days ago
- Submissions: 10 total (3 trees sent, 7 feedback), newest yesterday
- Accounts:    8 total, newest yesterday

**What readers told us** (14 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 08-21 | par_001 (The Robinier of Square Re | not worth it | - | no acct | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | report | could not reach it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | us | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | worth it | - | us | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | vote undone | worth it | us | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | not worth it | - | us | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | us | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | us | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | us | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | not worth it | us | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | us | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | us | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | us | holds |
| 08-24 | Baarn | tree sent in | 4 chars, read it in the database | us | open_question |
| 08-25 | utr_005 (Onder de Linden) | vote undone | not worth it | us | - |
| 08-26 | sar_003 (The Olivastro of Santa Ma | worth it | - | us | - |
| 08-27 | ams_001 | worth it | - | 46c1 | holds |
| 08-27 | Baarn | tree sent in | 4 chars, read it in the database | us | holds |
| 08-28 | - | Super | - | us | - |
| 08-29 | Baarn | tree sent in | 4 chars, read it in the database | us | holds |
| 08-29 | Baarn | tree sent in | - | us | holds |
| 08-30 | rom_002 (Adonis) | worth it | - | us | - |
| 08-30 | rom_002 (Adonis) | vote undone | worth it | us | - |
| 08-30 | rom_002 (Adonis) | not worth it | - | us | - |
| 08-30 | rom_002 (Adonis) | vote undone | not worth it | us | - |
| 08-30 | rom_002 (Adonis) | worth it | - | us | - |
| 08-30 | rom_002 (Adonis) | vote undone | worth it | us | - |
| 08-30 | rom_002 (Adonis) | not worth it | - | us | - |
| 08-30 | rom_002 (Adonis) | vote undone | not worth it | us | - |
| 08-30 | rom_002 (Adonis) | worth it | - | us | - |
| 08-30 | London Plane | tree sent in | 71 chars, read it in the database | 21dc | holds |
| 08-31 | Amsterdam | tree sent in | - | us | open_question |
| 08-31 | Baarn | tree sent in | - | us | open_question |
| 09-01 | Baarn | tree sent in | - | us | holds |
| 09-02 | Amsterdam | tree sent in | - | us | open_question |
| 09-03 | Hilversum | tree sent in | 4 chars, read it in the database | 92b5 | holds |
| 09-03 | Baarn | tree sent in | 7 chars, read it in the database | a9c1 | open_question |
| 09-03 | Baarn | tree sent in | - | us | holds |
| 09-03 | Baarn | tree sent in | - | us | holds |
| 09-03 | utr_002 (The Oude Hortus Ginkgo) | worth it | - | a9c1 | holds |

- 48 of these 54 rows are ours, marked us. The rest is the reader traffic.
- 1 arrived signed out, so they cannot be told apart.
- 5 rows from 4 accounts.

**The funnel, as rates**
- Seen to clicked: 2.3% (329 of 14184) vs 2.4% the fortnight before
- Pages per visit: 1.7 (1780 visits, 2970 pageviews since 2026-08-08)
- Visits that did something: 10.4% (186 actions on 1780 visits)

**What people did in the app**

| What | Yesterday | 14 days | Ever | Last |
|---|---:|---:|---:|---|
| app_open | 7 | 9 | 9 | today |
| tab | 8 | 13 | 13 | today |
| tree_opened | 16 | 27 | 27 | today |
| directions | 0 | 1 | 1 | today |
| tree_saved | 0 | 0 | 0 | never |
| tree_visited | 0 | 0 | 0 | never |
| sighting_recorded | 0 | 0 | 0 | never |
| **all** | **31** | **50** | **50** | |
- Measuring since 2026-08-30, when Measure.swift went in. Unlinked to any account by design: an install id, the app version and the OS, nothing else.
- Ours is not in this table: 20 install(s), 349 events, the testing before the app went live on 2026-09-03. Any install first seen before that stays excluded, so testing on the same phone never reads as a stranger.
- 4 installs have ever sent anything. An install id is made fresh on each install, so this is an upper bound on people, not a count of them.
- Tabs opened (14d): My trees 5; Discover 5; Map 3

**App Store downloads** (Apple's own count, not PostHog)
- no report instances yet (first one can take up to 48h after the request was created)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-25 | 19 | 1108 | 1.7% | 20.1 |
| 08-26 | 24 | 1144 | 2.1% | 18.7 |
| 08-27 | 15 | 1003 | 1.5% | 18.8 |
| 08-28 | 27 | 1014 | 2.7% | 16.3 |
| 08-29 | 32 | 1068 | 3.0% | 17.6 |
| 08-30 | 32 | 1065 | 3.0% | 19.2 |
| 08-31 | 21 | 949 | 2.2% | 16.4 |
| 09-01 | 26 | 921 | 2.8% | 10.5 |
| 09-02 | 29 | 1055 | 2.7% | 11.2 |
| 09-03 *partial* | 26 | 958 | 2.7% | 10.4 |
| **window** | **251** | **10285** | **2.4%** | |
- Top queries (10d): ancient trees (i32, p22); dutch elm amsterdam (i44, p4); ancient tree (i22, p31); cannonball tree singapore (i7, p9); e bordeaux? (i1, p1)
- Top pages (10d): / (c17/i142); /prague (c12/i118); /lisbon (c9/i220); /rome (c7/i592); /seville (c7/i141)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - '"oldest of its species" owl park' (i8, p8)
    - '400 year old tree' (i5, p8)
    - '"quercus short"' (i4, p5)
    - '"400 years old as of 2023" tree' (i2, p8)
    - '"quercus aggressive"' (i2, p6)
    - '"courtyard" "okinawa"' (i1, p9)
    - '"oldest of its species" "park" tree' (i1, p10)
    - '"polish"' (i1, p14)
    - and 3 more

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| rome | 7 | 630 | 1.1% | 9.1 | 3.0% | trees in rome (i52, p10) |
| amsterdam | 8 | 339 | 2.4% | 8.2 | 3.4% | dutch elm amsterdam (i44, p4) |
| lisbon | 11 | 270 | 4.1% | 7.6 | 3.7% | oldest tree in lisbon (i8, p8) |
| barcelona | 6 | 228 | 2.6% | 8.8 | 3.1% | barcelona trees (i5, p7) |
| singapore | 5 | 204 | 2.5% | 10.6 | 2.3% | oldest tree in singapore (i25, p10) |
| seville | 8 | 175 | 4.6% | 7.9 | 3.5% | seville (i2, p4) |
| london | 2 | 175 | 1.1% | 21.2 | 0.8% | old trees near me (i2, p7) |
| brisbane | 6 | 157 | 3.8% | 20.1 | 0.8% | the big macadamia nut (i13, p64) |
| vienna | 5 | 141 | 3.5% | 7.5 | 3.7% | alter (i1, p3) |
| milan | 0 | 140 | 0.0% | 8.7 | 3.2% | "oldest of its species" owl park (i8, p8) |
| prague | 13 | 136 | 9.6% | 7.3 | 3.9% | praga (i1, p1) |
| florence | 3 | 131 | 2.3% | 6.6 | 4.4% | florence trees (i3, p5) |
| copenhagen | 1 | 125 | 0.8% | 11.6 | 1.9% | trees in copenhagen (i16, p17) |
| malaga | 4 | 122 | 3.3% | 12.4 | 1.7% | árboles históricos de málaga (i10, p79) |
| tenerife | 2 | 120 | 1.7% | 9.1 | 3.0% | pino gordo (i8, p24) |
| paris | 2 | 114 | 1.8% | 15.5 | 1.2% | trees paris (i3, p46) |
| crete | 0 | 105 | 0.0% | 11.5 | 2.0% | kavousi olive tree (i2, p10) |
| madeira | 3 | 99 | 3.0% | 9.6 | 2.7% | fanal witch tree (i10, p20) |
| brussels | 1 | 95 | 1.1% | 11.0 | 2.2% | belgium trees (i2, p10) |
| sardinia | 0 | 88 | 0.0% | 8.2 | 3.4% | baltolu sardinia (i22, p8) |
| fukuoka | 2 | 87 | 2.3% | 14.1 | 1.4% | couple camphor trees (i3, p9) |
| naples | 0 | 87 | 0.0% | 9.4 | 2.8% | naples tree (i3, p6) |
| alicante | 0 | 82 | 0.0% | 7.9 | 3.5% | - |
| athens | 2 | 79 | 2.5% | 10.2 | 2.4% | oldest olive tree in athens (i2, p1) |
| bath | 1 | 79 | 1.3% | 7.4 | 3.8% | hanging tree bath (i3, p11) |
| toronto | 2 | 79 | 2.5% | 8.1 | 3.5% | big red oak (i15, p7) |
| new-york | 0 | 75 | 0.0% | 18.9 | 0.9% | - |
| palermo | 1 | 73 | 1.4% | 7.1 | 4.0% | giardini reali palermo (i1, p14) |
| dublin | 2 | 72 | 2.8% | 11.9 | 1.8% | hybrid strawberry tree (i1, p10) |
| kyoto | 1 | 68 | 1.5% | 11.2 | 2.1% | japanese camphor (i2, p70) |
| palma-de-mallorca | 0 | 68 | 0.0% | 7.2 | 3.9% | olivera de cort (i1, p11) |
| venice | 0 | 68 | 0.0% | 5.7 | 5.5% | trees in venice (i3, p8) |
| edinburgh | 4 | 66 | 6.1% | 12.7 | 1.7% | edinburgh tree map (i1, p10) |
| leiden | 0 | 66 | 0.0% | 9.3 | 2.8% | "oldest of its species" ginkgo park (i16, p7) |
| seoul | 0 | 66 | 0.0% | 13.2 | 1.6% | korean trees (i1, p48) |
| hilo | 1 | 65 | 1.5% | 58.7 | 0.4% | loulu palm (i42, p76) |
| istanbul | 3 | 63 | 4.8% | 6.4 | 4.6% | a ten ile ma (i1, p2) |
| berlin | 0 | 62 | 0.0% | 10.4 | 2.4% | berlin trees (i2, p50) |
| perth | 1 | 61 | 1.6% | 12.2 | 1.8% | jarrah tree bark (i2, p50) |
| valencia | 0 | 60 | 0.0% | 7.8 | 3.6% | - |
| bologna | 0 | 58 | 0.0% | 7.3 | 3.8% | - |
| munich | 2 | 57 | 3.5% | 8.4 | 3.3% | the hornbeam centre (i1, p59) |
| portland | 1 | 57 | 1.8% | 13.6 | 1.5% | - |
| nijmegen | 0 | 55 | 0.0% | 7.5 | 3.8% | brakkenstein nijmegen maps (i3, p11) |
| sydney | 0 | 55 | 0.0% | 9.1 | 3.0% | the wishing tree sydney (i7, p10) |
| madrid | 1 | 54 | 1.9% | 13.6 | 1.5% | oldest tree in madrid (i2, p10) |
| krakow | 0 | 52 | 0.0% | 14.0 | 1.4% | kossaka (i4, p15) |
| mexico-city | 2 | 51 | 3.9% | 9.8 | 2.6% | ahuehuete mexico city (i2, p9) |
| reykjavik | 1 | 51 | 2.0% | 17.2 | 1.0% | oldest tree in iceland (i2, p7) |
| cyprus | 2 | 49 | 4.1% | 7.2 | 3.9% | oldest tree in cyprus (i3, p10) |
| budapest | 1 | 48 | 2.1% | 7.1 | 3.9% | - |
| sintra | 1 | 46 | 2.2% | 6.4 | 4.6% | - |
| seattle | 4 | 44 | 9.1% | 6.7 | 4.3% | oldest tree in seattle (i2, p8) |
| greece | 0 | 43 | 0.0% | 37.9 | 0.4% | greek trees (i3, p29) |
| montreal | 3 | 42 | 7.1% | 9.5 | 2.8% | mckenna grave height (i1, p5) |
| utrecht | 0 | 42 | 0.0% | 8.8 | 3.1% | zocher utrecht (i2, p22) |
| chicago | 3 | 41 | 7.3% | 11.1 | 2.1% | - |
| melbourne | 7 | 40 | 17.5% | 8.4 | 3.3% | - |
| las-vegas | 0 | 39 | 0.0% | 13.0 | 1.6% | vegas trees (i8, p30) |
| tokyo | 1 | 38 | 2.6% | 7.4 | 3.8% | - |
| glasgow | 0 | 36 | 0.0% | 9.0 | 3.0% | - |
| cagliari | 2 | 35 | 5.7% | 4.6 | 7.4% | ficus macrophylla cagliari (i2, p6) |
| geneva | 2 | 35 | 5.7% | 6.2 | 4.8% | - |
| strasbourg | 1 | 35 | 2.9% | 7.7 | 3.7% | - |
| new-orleans | 1 | 34 | 2.9% | 23.6 | 0.7% | anseman oak (i3, p9) |
| porto | 3 | 34 | 8.8% | 8.7 | 3.1% | - |
| vilnius | 0 | 34 | 0.0% | 10.5 | 2.3% | amur linden (i1, p60) |
| bordeaux | 3 | 33 | 9.1% | 5.7 | 5.7% | e bordeaux? (i1, p1) |
| boston | 1 | 33 | 3.0% | 8.7 | 3.2% | - |
| the-hague | 1 | 33 | 3.0% | 8.5 | 3.2% | arentsburg (i1, p7) |
| austin | 0 | 33 | 0.0% | 12.1 | 1.8% | antebellum oaks (i1, p54) |
| groningen | 1 | 32 | 3.1% | 9.9 | 2.6% | oak groningen (i1, p7) |
| cadiz | 0 | 30 | 0.0% | 7.0 | 4.0% | cadiz botanical gardens (i1, p2) |
| quebec-city | 2 | 29 | 6.9% | 7.9 | 3.5% | wych elm (i1, p25) |
| dubrovnik | 1 | 28 | 3.6% | 6.1 | 4.9% | - |
| tallinn | 0 | 28 | 0.0% | 5.4 | 6.3% | - |
| oxford | 4 | 27 | 14.8% | 6.6 | 4.4% | - |
| oahu | 1 | 27 | 3.7% | 7.0 | 4.0% | baobab hawaii (i1, p6) |
| eindhoven | 1 | 25 | 4.0% | 14.4 | 1.3% | beukenboom (i1, p3) |
| oslo | 1 | 24 | 4.2% | 8.2 | 3.4% | - |
| warsaw | 1 | 24 | 4.2% | 9.2 | 2.9% | aleja niepodleglosci (i1, p11) |
| nara | 1 | 23 | 4.3% | 5.0 | 6.9% | - |
| arnhem | 0 | 23 | 0.0% | 8.7 | 3.2% | musispark arnhem (i1, p4) |
| helsinki | 0 | 23 | 0.0% | 4.7 | 7.3% | in helsinki (i1, p4) |
| nuremberg | 0 | 23 | 0.0% | 7.0 | 4.0% | kontumaz (i1, p7) |
| sorrento | 0 | 23 | 0.0% | 12.9 | 1.6% | - |
| lyon | 1 | 22 | 4.5% | 5.9 | 5.3% | antoine rivoire (i1, p10) |
| dallas | 0 | 22 | 0.0% | 10.5 | 2.3% | centennial tree (i3, p12) |
| hong-kong | 0 | 22 | 0.0% | 7.2 | 3.9% | 樹齡 (i1, p4) |
| bristol | 0 | 21 | 0.0% | 11.0 | 2.2% | domesday oak (i1, p8) |
| trieste | 0 | 20 | 0.0% | 11.1 | 2.1% | piazza hortis (i3, p10) |
| graz | 1 | 19 | 5.3% | 14.6 | 1.3% | oak (i4, p10) |
| cork | 0 | 18 | 0.0% | 8.8 | 3.1% | oldest tree in ireland (i2, p10) |
| riga | 0 | 18 | 0.0% | 5.3 | 6.4% | brisbane river sewage (i1, p9) |
| pamplona | 2 | 17 | 11.8% | 4.2 | 7.8% | "quercus short" (i4, p5) |
| potsdam | 0 | 17 | 0.0% | 16.6 | 1.1% | glienicker park (i1, p63) |
| ljubljana | 1 | 16 | 6.2% | 8.6 | 3.2% | trees ljubljana (i1, p9) |
| bangkok | 0 | 16 | 0.0% | 10.5 | 2.3% | - |
| brno | 0 | 16 | 0.0% | 4.1 | 7.9% | - |
| houston | 0 | 16 | 0.0% | 40.6 | 0.4% | trees in houston (i2, p62) |
| maastricht | 0 | 16 | 0.0% | 8.1 | 3.5% | tulip maastricht (i1, p20) |
| washington-dc | 0 | 16 | 0.0% | 13.2 | 1.6% | survey lodge (i1, p8) |
| bilbao | 1 | 15 | 6.7% | 6.0 | 5.0% | bilbao tree (i1, p9) |
| braga | 2 | 15 | 13.3% | 6.6 | 4.4% | santa tecla braga (i1, p1) |
| catania | 1 | 15 | 6.7% | 5.3 | 6.5% | - |
| granada | 1 | 15 | 6.7% | 4.9 | 7.1% | - |
| sapporo | 1 | 15 | 6.7% | 10.8 | 2.2% | sapporo tree (i2, p11) |
| aarhus | 0 | 15 | 0.0% | 8.0 | 3.5% | happy pig (i1, p11) |
| cordoba | 0 | 15 | 0.0% | 37.7 | 0.4% | ginkgo location (i1, p63) |
| leipzig | 0 | 15 | 0.0% | 13.5 | 1.5% | beech leaf disease (i1, p19) |
| nice | 0 | 15 | 0.0% | 5.8 | 5.4% | promenade des anglais palm trees (i1, p5) |
| osaka | 0 | 15 | 0.0% | 4.8 | 7.2% | - |
| vancouver | 0 | 15 | 0.0% | 17.5 | 1.0% | ancient trees of vancouver (i3, p29) |
| kamakura | 2 | 14 | 14.3% | 4.9 | 7.1% | kamakura tree (i6, p4) |
| poznan | 1 | 14 | 7.1% | 17.0 | 1.0% | - |
| rotterdam | 1 | 14 | 7.1% | 6.9 | 4.1% | delftseplein (i2, p4) |
| hobart | 0 | 14 | 0.0% | 12.3 | 1.7% | - |
| belgrade | 1 | 13 | 7.7% | 8.1 | 3.5% | - |
| girona | 1 | 13 | 7.7% | 5.4 | 6.2% | - |
| zurich | 1 | 13 | 7.7% | 6.2 | 4.8% | - |
| emmen | 0 | 13 | 0.0% | 6.3 | 4.7% | rensenpark emmen former zoo park (i1, p6) |
| guimaraes | 0 | 13 | 0.0% | 13.2 | 1.6% | pine tree portugal (i4, p18) |
| bratislava | 2 | 12 | 16.7% | 6.8 | 4.2% | - |
| lucca | 0 | 12 | 0.0% | 7.2 | 3.9% | balearic box (i1, p7) |
| venlo | 0 | 12 | 0.0% | 19.4 | 0.8% | sequoia waterloo (i1, p74) |
| cambridge | 3 | 11 | 27.3% | 7.1 | 4.0% | - |
| cologne | 1 | 11 | 9.1% | 7.9 | 3.5% | gibt es das in köln (i1, p4) |
| salzburg | 1 | 11 | 9.1% | 6.3 | 4.7% | - |
| buenos-aires | 0 | 11 | 0.0% | 10.5 | 2.3% | trees in buenos aires (i1, p18) |
| frankfurt | 0 | 11 | 0.0% | 6.8 | 4.2% | what tree is this (i1, p6) |
| trento | 0 | 11 | 0.0% | 5.4 | 6.3% | - |
| verona | 0 | 11 | 0.0% | 7.1 | 4.0% | - |
| como | 1 | 10 | 10.0% | 6.6 | 4.4% | como tree (i1, p7) |
| kauai | 1 | 10 | 10.0% | 5.2 | 6.6% | - |
| australia | 0 | 10 | 0.0% | 18.3 | 0.9% | oldest tree in australia (i2, p50) |
| bari | 0 | 10 | 0.0% | 7.1 | 4.0% | roots quasano (i2, p12) |
| dordrecht | 0 | 10 | 0.0% | 6.9 | 4.1% | - |
| tilburg | 0 | 10 | 0.0% | 9.5 | 2.8% | - |
| toulouse | 0 | 10 | 0.0% | 7.4 | 3.8% | - |
| turin | 0 | 10 | 0.0% | 7.1 | 4.0% | - |

**The language test** (Contract J v1.13: a translated set should pass its English twin's impressions within four weeks of indexing):

| Lang | City | Clicks | Impressions | Position | English twin |
|---|---|---:|---:|---:|---:|
| de | berlin | 0 | 101 | 21.3 | 62 |
| de | vienna | 3 | 89 | 8.5 | 141 |
| es | malaga | 1 | 87 | 13.3 | 122 |
| ja | kyoto | 2 | 67 | 10.2 | 68 |
| pt | lisbon | 3 | 59 | 12.9 | 270 |
| pt | porto | 3 | 59 | 6.2 | 34 |
| es | barcelona | 0 | 53 | 13.6 | 228 |
| ja | tokyo | 1 | 48 | 11.5 | 38 |
| it | palermo | 0 | 44 | 10.5 | 73 |
| it | rome | 2 | 39 | 10.4 | 630 |
| es | cadiz | 2 | 34 | 12.7 | 30 |
| de | zurich | 1 | 29 | 12.7 | 13 |
| nl | amsterdam | 1 | 27 | 4.6 | 339 |
| es | tenerife | 0 | 27 | 24.9 | 120 |
| es | madrid | 0 | 26 | 7.4 | 54 |
| pt | sintra | 1 | 24 | 12.8 | 46 |
| nl | nijmegen | 0 | 18 | 7.8 | 55 |
| ja | osaka | 2 | 17 | 14.8 | 15 |
| fr | geneva | 1 | 16 | 16.2 | 35 |
| fr | nice | 0 | 16 | 15.9 | 15 |
| it | milan | 0 | 15 | 11.1 | 140 |
| fr | paris | 0 | 9 | 7.4 | 114 |
| nl | the-hague | 0 | 5 | 17.8 | 33 |
- Seen, not clicked: /rome (c2/i239, 0.8%) for trees in rome (i52, p10); rome trees (i49, p9); rome tree (i14, p16)
- Seen, not clicked: /species/strawberry-tree (c0/i94, 0.0%) for strawberry tree (i24, p64); arbutus strawberry tree (i10, p61); strawberry trees (i5, p68)
- Seen, not clicked: /species/osage-orange (c0/i55, 0.0%) for osage orange (i12, p79); osage oranges (i3, p81); osage orange tree (i3, p83)
- Seen, not clicked: /hilo/loulu-palm-of-kalakaua-park (c0/i46, 0.0%) for loulu palm (i42, p76); loulu palm tree (i2, p52); loulu tree (i1, p47)
- Seen, not clicked: /species/austrian-pine (c0/i32, 0.0%) for austrian pine (i10, p93); austrian pine tree (i8, p83); austrian pine trees (i7, p75)
- Seen, not clicked: /species/dragon-tree (c0/i32, 0.0%) for dragon tree (i12, p46); dragon trees (i9, p45); dragontree (i6, p64)
- Seen, not clicked: /species/silver-maple (c0/i29, 0.0%) for silver maple tree (i7, p58); silver maple (i6, p60); sliver maple (i2, p60)
- Seen, not clicked: /singapore/oldest-tree (c0/i26, 0.0%) for oldest tree in singapore (i25, p10); changi tree (i1, p4)

**Climbing** (this ten days against the ten before it)

| Page | Impressions | Change | Position | Moved | Clicks |
|---|---:|---:|---:|---:|---:|
| /rome | 592 | +360 | 9.2 | +3.7 | +5 |
| /amsterdam/elm-of-elsenhoeve | 100 | +90 | 6.4 | -2.1 | +0 |
| /lisbon | 220 | +75 | 7.4 | +0.9 | +4 |
| /species/strawberry-tree | 113 | +75 | 64.8 | +2.1 | +0 |
| /seville | 141 | +73 | 8.4 | +2.3 | +4 |
| / | 142 | +67 | 17.6 | -2.6 | +6 |
| /collections/trees-older-than-400-years | 89 | +66 | 19.8 | +6.6 | +0 |
| /collections/tallest-trees | 45 | +43 | 31.5 | +12.0 | +0 |

**Newly ranking** (no impressions at all ten days ago)

| Page | Impressions | Clicks | Position |
|---|---:|---:|---:|
| /species/austrian-pine | 39 | 0 | 81.3 |
| /sydney/wishing-tree | 35 | 0 | 10.9 |
| /ja/kyoto/land-boat-pine | 23 | 0 | 9.8 |
| /seattle/sylvia | 22 | 2 | 6.5 |
| /es/cadiz | 22 | 1 | 16.0 |
| /de/berlin/aeltester-baum | 22 | 0 | 47.0 |

**Slipping**

| Page | Impressions | Change | Position | Moved |
|---|---:|---:|---:|---:|
| /madrid | 32 | -90 | 16.5 | -2.4 |
| /es/malaga/ficus-avenue-of-the-alameda-principal | 17 | -39 | 7.2 | -1.6 |
| /amsterdam/oudemanhuispoort-elm | 18 | -19 | 7.6 | -0.8 |
| /es/malaga | 42 | -13 | 10.5 | -0.6 |

- New queries this window: cannonball tree singapore (i7).

**Who they are**
Audience, 28 days of search (506 clicks, 21552 impressions):
- Countries: usa c90/i4822; gbr c56/i2435; nld c31/i1041; aus c25/i757; prt c24/i603
- Devices: MOBILE c340/i11721; DESKTOP c158/i9637; TABLET c8/i194
- Landing pages: / c30/i240; /prague c25/i349; /lisbon c15/i413; /rome c10/i908; /seville c10/i220

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-27 | 60 | 140 |
| 08-28 | 120 | 170 |
| 08-29 | 60 | 140 |
| 08-30 | 70 | 180 |
| 08-31 | 30 | 90 |
| 09-01 | 80 | 120 |
| 09-02 | 110 | 270 |
| 09-03 | 200 | 250 |
| **window** | **730** | **1360** |
- Top paths: / (110); /explore (60); /account (40); /prague/beethoven-plane (40); /app (30); /australia (30); /melbourne/remnant-river-red-gum-of-edinburgh-gardens (30); /melbourne (30); /nijmegen/wilhelminaboom-of-hertogplein (30); /rome (20); /leeuwarden/marilandica-poplar (20); /porto (20)
- Referrers: ancienttrees.app (630); (direct) (480); www.google.com (250)
- Moved between our own pages: 630 of 1360 pageviews (46%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: US (240); AU (200); NL (190); GB (110); SG (90)
- Devices: mobile (670); desktop (670); tablet (20)
- Page load (8d): p50 602ms, p90 3070ms

Links: external referrers (a link somebody actually clicked): none yet
AI: arrivals from an assistant that cited us: none yet


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 09-03T11:44 | 35.0 | 9 | 11 | 4 | Giessen +4, Aga +1, Biei +1, Effeltrich +1, +2 more |
| 09-03T12:20 | 65.1 | 18 | 21 | 28 | Giessen +4, Aga +1, Biei +1, Effeltrich +1, +11 more |
| 09-03T15:13 | 101.2 | 14 | 26 | 51 | Malsfeld +4, Iwata +1, Kanagi +1, Kitamoto +1, +7 more |
| 09-03T17:22 | 99.7 | 11 | 43 | 52 | Matera +4, Oahu +3, Higashimiyoshi +1, Hilo +1, +4 more |
| 09-03T20:15 | 73.2 | 9 | 13 | 55 | Apeldoorn +1, Atami +1, Baarn +1, Dordrecht +1, +5 more |
| 09-03T23:32 | 47.7 | 6 | 17 | 33 | Port Renfrew +2, Cooper Creek +1, Derby +1, Flinders Ranges +1, +2 more |
| 09-04T00:21 | 58.6 | 13 | 34 | 30 | Port Renfrew +2, Alicante +1, Cooper Creek +1, Derby +1, +9 more |
| 09-04T01:53 | 43.0 | 3 | 11 | 29 | Asago +1, Kawago +1, Suzuka +1 |
| 09-04T06:03 | 95.4 | 14 | 25 | 42 | Allouville Bellefosse +1, Bad Blumau +1, Bansko +1, Concoret +1, +33 more |
| 09-04T07:40 | 40.0 | 9 | 38 | 31 | Allouville Bellefosse +1, Bad Blumau +1, Bansko +1, Bari +1, +29 more |
| **10 runs** | **659** | **106** | **239** | | |

- 4 to 55 commands refused per run; 1 wrote nothing to LOG.md.

**What they made**

- Vendor 3 photographs to our own domain
- Bari +1: The Roverella of Pilapalucci, a bookable-access farm oak
- Fix Catania: two bunya pines were each citing the other's girth
- Resolve _famous-japan verify claim: 2 candidates blocked
- Merge remaining stale verified batches; file Australia's 10 blocked candidates to leads
- Merge stale famous-japan verified batches: 2 already-published trees confirmed, remaining blocked candidates filed to leads
- Add German overlay for Potsdam (Contract J)
- Re-derive 21 photo URLs from capped 960px thumbnails to originals
- Publish Bad Blumau's disputed thousand-year oak
- Mark Krasi published (crt_003), Tilleuls de Sully blocked (not a single tree)
- Mark 6 famous-tree leads published (Pirangi, Vassununga, Bansko, Granit, Allouville-Bellefosse, Concoret)
- Publish Miriam Vale's Big Fig; add weeping-fig species page
- Photo viewing pass: 3 approved, 1 held, 8 rejected across 12 cities
- photo_hunt.py sweep: candidates found for new single-tree destinations and others

Machine: 10 chain attempts yesterday, 10 got real work time (~682 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 26 clicks and 958 impressions on Google's freshest day (day before: c29/i1055). Directional at best; no strategic conclusions from these volumes.

## 2026-09-02 (previous UTC day)

**Today: 2 tree submissions arrived today (9 total); an account was opened today (8 total).**

**Did the product happen**

| Action | Yesterday | 14 days | Ever | Last |
|---|---:|---:|---:|---|
| app-cta | 0 | 23 | 47 | today |
| directions | 11 | 44 | 44 | yesterday |
| search-home | 3 | 29 | 32 | yesterday |
| waitlist-submit | 0 | 14 | 18 | today |
| save | 0 | 10 | 12 | 4 days ago |
| walks-app | 2 | 7 | 10 | yesterday |
| search-explore | 0 | 8 | 9 | today |
| suggestion-submit | 0 | 4 | 4 | 4 days ago |
| walk-open | 0 | 0 | 4 | 17 days ago |
| smoke-test | 0 | 0 | 2 | 33 days ago |
| beacon-fix-verify | 0 | 0 | 1 | 18 days ago |
| beacon-test | 0 | 0 | 1 | 18 days ago |
| sponsor-open | 0 | 1 | 1 | today |
| worthit-not worth it | 0 | 0 | 1 | 17 days ago |
| signin-link-sent | 0 | 0 | 0 | never |
| walk-start | 0 | 0 | 0 | never |
| worthit-worth it | 0 | 0 | 0 | never |
| **all** | **16** | **140** | **186** | |
- 'Ever' counts every row in the events table, which begins 2026-08-01 when the funnel was repaired. Anything named here with a zero has never fired at all.

**What people typed into our search** (14 days, 31 searches, 19 different terms)

| Typed | Times |
|---|---:|
| mel | 6 |
| melbourne | 4 |
| melb | 3 |
| milano | 3 |
| berli | 1 |
| boston | 1 |
| ei | 1 |
| glasg | 1 |
| leiden | 1 |
| london | 1 |
| melbo | 1 |
| melbou | 1 |
| oslo | 1 |
| perth | 1 |
| portland | 1 |
| prague | 1 |
| sea | 1 |
| sy | 1 |
| warszawa | 1 |

| Day | Accounts | Android waitlist | Saves | Trees sent | Feedback |
|---|---:|---:|---:|---:|---:|
| 08-20 | 0 | 1 | 3 | 0 | 1 |
| 08-21 | 1 | 0 | 0 | 0 | 1 |
| 08-22 | 0 | 0 | 1 | 0 | 0 |
| 08-23 | 0 | 0 | 0 | 0 | 0 |
| 08-24 | 0 | 0 | 0 | 0 | 0 |
| 08-25 | 0 | 1 | 0 | 0 | 0 |
| 08-26 | 0 | 1 | 1 | 0 | 0 |
| 08-27 | 0 | 1 | 0 | 0 | 1 |
| 08-28 | 0 | 1 | 0 | 0 | 0 |
| 08-29 | 0 | 0 | 0 | 0 | 0 |
| 08-30 | 1 | 0 | 5 | 1 | 0 |
| 08-31 | 0 | 2 | 0 | 0 | 0 |
| 09-01 | 1 | 0 | 0 | 0 | 0 |
| 09-02 | 1 | 0 | 0 | 0 | 0 |
| 09-03 | 2 | 0 | 0 | 2 | 0 |
| **14 days** | **6** | **7** | **10** | **3** | **3** |
- Our own rows are not in this table: 10 trees, 22 feedback, 2 accounts. They are testing, and counting them reads as traction.
- Android waitlist: 16 total, newest 3 days ago
- Submissions: 9 total (3 trees sent, 6 feedback), newest today
- Accounts:    8 total, newest today

**What readers told us** (14 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-21 | par_001 (The Robinier of Square Re | not worth it | - | no acct | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | report | could not reach it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | us | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | worth it | - | us | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | vote undone | worth it | us | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | not worth it | - | us | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | us | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | us | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | us | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | not worth it | us | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | us | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | us | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | us | holds |
| 08-24 | Baarn | tree sent in | 4 chars, read it in the database | us | open_question |
| 08-25 | utr_005 (Onder de Linden) | vote undone | not worth it | us | - |
| 08-26 | sar_003 (The Olivastro of Santa Ma | worth it | - | us | - |
| 08-27 | ams_001 | worth it | - | 46c1 | holds |
| 08-27 | Baarn | tree sent in | 4 chars, read it in the database | us | holds |
| 08-28 | - | Super | - | us | - |
| 08-29 | Baarn | tree sent in | 4 chars, read it in the database | us | holds |
| 08-29 | Baarn | tree sent in | - | us | holds |
| 08-30 | rom_002 (Adonis) | worth it | - | us | - |
| 08-30 | rom_002 (Adonis) | vote undone | worth it | us | - |
| 08-30 | rom_002 (Adonis) | not worth it | - | us | - |
| 08-30 | rom_002 (Adonis) | vote undone | not worth it | us | - |
| 08-30 | rom_002 (Adonis) | worth it | - | us | - |
| 08-30 | rom_002 (Adonis) | vote undone | worth it | us | - |
| 08-30 | rom_002 (Adonis) | not worth it | - | us | - |
| 08-30 | rom_002 (Adonis) | vote undone | not worth it | us | - |
| 08-30 | rom_002 (Adonis) | worth it | - | us | - |
| 08-30 | London Plane | tree sent in | 71 chars, read it in the database | 21dc | holds |
| 08-31 | Amsterdam | tree sent in | - | us | open_question |
| 08-31 | Baarn | tree sent in | - | us | open_question |
| 09-01 | Baarn | tree sent in | - | us | holds |
| 09-02 | Amsterdam | tree sent in | - | us | open_question |
| 09-03 | Hilversum | tree sent in | 4 chars, read it in the database | 92b5 | holds |
| 09-03 | Baarn | tree sent in | 7 chars, read it in the database | a9c1 | open_question |
| 09-03 | Baarn | tree sent in | - | us | holds |
| 09-03 | Baarn | tree sent in | - | us | holds |

- 48 of these 56 rows are ours, marked us. The rest is the reader traffic.
- 4 arrived signed out, so they cannot be told apart.
- 4 rows from 4 accounts.

**The funnel, as rates**
- Seen to clicked: 2.3% (327 of 14422) vs 2.4% the fortnight before
- Pages per visit: 1.7 (1580 visits, 2720 pageviews since 2026-08-08)
- Visits that did something: 11.6% (184 actions on 1580 visits)

**What people did in the app**

| What | Yesterday | 14 days | Ever | Last |
|---|---:|---:|---:|---|
| app_open | 0 | 4 | 4 | today |
| tab | 0 | 7 | 7 | today |
| tree_opened | 0 | 9 | 9 | today |
| directions | 0 | 0 | 0 | never |
| tree_saved | 0 | 0 | 0 | never |
| tree_visited | 0 | 0 | 0 | never |
| sighting_recorded | 0 | 0 | 0 | never |
| **all** | **0** | **20** | **20** | |
- Measuring since 2026-08-30, when Measure.swift went in. Unlinked to any account by design: an install id, the app version and the OS, nothing else.
- Ours is not in this table: 20 install(s), 298 events, the testing before the app went live on 2026-09-03. Any install first seen before that stays excluded, so testing on the same phone never reads as a stranger.
- 2 installs have ever sent anything. An install id is made fresh on each install, so this is an upper bound on people, not a count of them.
- At one or two installs this is a person or two, not an audience. Read nothing into a single tap.
- Tabs opened (14d): My trees 3; Map 2; Discover 2

**App Store downloads** (Apple's own count, not PostHog)
- no report instances yet (first one can take up to 48h after the request was created)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-24 | 28 | 998 | 2.8% | 15.9 |
| 08-25 | 19 | 1108 | 1.7% | 20.1 |
| 08-26 | 24 | 1144 | 2.1% | 18.7 |
| 08-27 | 15 | 1003 | 1.5% | 18.8 |
| 08-28 | 27 | 1014 | 2.7% | 16.3 |
| 08-29 | 32 | 1068 | 3.0% | 17.6 |
| 08-30 | 32 | 1065 | 3.0% | 19.2 |
| 08-31 | 21 | 949 | 2.2% | 16.4 |
| 09-01 | 26 | 921 | 2.8% | 10.5 |
| 09-02 | 29 | 1028 | 2.8% | 11.3 |
| 09-03 *partial* | 7 | 201 | 3.5% | 9.9 |
| **window** | **260** | **10499** | **2.5%** | |
- Top queries (10d): dutch elm amsterdam (i53, p4); ancient trees (i31, p23); ancient tree (i22, p31); cannonball tree singapore (i6, p9); e bordeaux? (i1, p1)
- Top pages (10d): / (c18/i145); /prague (c13/i122); /seville (c9/i150); /rome (c8/i556); /lisbon (c7/i207)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - '"oldest of its species" owl park' (i8, p9)
    - '400 year old tree' (i5, p8)
    - '"quercus short"' (i4, p5)
    - '"400 years old as of 2023" tree' (i2, p8)
    - '"quercus aggressive"' (i2, p6)
    - '"courtyard" "okinawa"' (i1, p9)
    - '"oldest of its species" "park" tree' (i1, p10)
    - '"polish"' (i1, p14)
    - and 3 more

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| rome | 8 | 601 | 1.3% | 9.3 | 2.8% | trees in rome (i47, p10) |
| amsterdam | 9 | 375 | 2.4% | 8.3 | 3.3% | dutch elm amsterdam (i49, p4) |
| lisbon | 9 | 255 | 3.5% | 7.7 | 3.6% | oldest tree in lisbon (i8, p8) |
| barcelona | 7 | 228 | 3.1% | 8.9 | 3.1% | barcelona trees (i7, p7) |
| singapore | 6 | 204 | 2.9% | 10.6 | 2.3% | oldest tree in singapore (i24, p10) |
| seville | 10 | 187 | 5.3% | 8.1 | 3.4% | seville spain orange trees (i2, p35) |
| london | 3 | 183 | 1.6% | 21.8 | 0.7% | old trees near me (i2, p7) |
| brisbane | 6 | 172 | 3.5% | 19.9 | 0.8% | the big macadamia nut (i14, p64) |
| milan | 0 | 152 | 0.0% | 8.4 | 3.3% | "oldest of its species" owl park (i8, p9) |
| vienna | 4 | 146 | 2.7% | 9.0 | 3.0% | alter (i1, p3) |
| tenerife | 2 | 140 | 1.4% | 9.4 | 2.8% | pino gordo (i10, p22) |
| prague | 14 | 139 | 10.1% | 7.5 | 3.8% | - |
| florence | 3 | 137 | 2.2% | 7.0 | 4.0% | florence trees (i3, p5) |
| copenhagen | 1 | 137 | 0.7% | 11.4 | 2.0% | trees in copenhagen (i19, p17) |
| malaga | 4 | 131 | 3.1% | 13.2 | 1.6% | árboles históricos de málaga (i12, p79) |
| paris | 2 | 116 | 1.7% | 15.9 | 1.1% | trees in paris (i3, p28) |
| crete | 0 | 113 | 0.0% | 11.0 | 2.2% | kavousi olive tree (i2, p10) |
| madeira | 3 | 108 | 2.8% | 9.5 | 2.8% | fanal witch tree (i10, p20) |
| naples | 0 | 106 | 0.0% | 9.0 | 3.0% | naples tree (i3, p6) |
| fukuoka | 3 | 97 | 3.1% | 13.3 | 1.5% | couple camphor trees (i3, p9) |
| toronto | 1 | 94 | 1.1% | 8.2 | 3.4% | big red oak (i18, p7) |
| bath | 2 | 91 | 2.2% | 7.6 | 3.7% | giant plane tree bath (i4, p12) |
| brussels | 1 | 87 | 1.1% | 11.0 | 2.2% | belgium trees (i2, p10) |
| sardinia | 0 | 87 | 0.0% | 8.1 | 3.4% | baltolu sardinia (i21, p8) |
| new-york | 1 | 85 | 1.2% | 17.6 | 1.0% | - |
| palma-de-mallorca | 0 | 84 | 0.0% | 7.2 | 3.9% | placa de cort palma olive tree (i2, p8) |
| dublin | 2 | 79 | 2.5% | 12.4 | 1.7% | hybrid strawberry tree (i1, p10) |
| alicante | 0 | 79 | 0.0% | 7.8 | 3.6% | - |
| venice | 0 | 76 | 0.0% | 5.7 | 5.6% | trees in venice (i3, p8) |
| athens | 1 | 74 | 1.4% | 10.6 | 2.3% | amritara olive trotter (i1, p84) |
| palermo | 0 | 74 | 0.0% | 6.6 | 4.4% | giardini reali palermo (i1, p14) |
| seoul | 0 | 74 | 0.0% | 14.2 | 1.4% | korean trees (i2, p47) |
| edinburgh | 4 | 71 | 5.6% | 12.2 | 1.8% | edinburgh trees (i1, p52) |
| kyoto | 1 | 69 | 1.4% | 10.4 | 2.4% | japanese camphor (i1, p84) |
| hilo | 1 | 66 | 1.5% | 58.6 | 0.4% | loulu palm (i42, p76) |
| madrid | 1 | 66 | 1.5% | 14.4 | 1.3% | oldest tree in madrid (i2, p10) |
| leiden | 0 | 66 | 0.0% | 9.3 | 2.9% | "oldest of its species" ginkgo park (i15, p7) |
| bologna | 0 | 65 | 0.0% | 7.6 | 3.7% | - |
| valencia | 2 | 64 | 3.1% | 8.0 | 3.5% | - |
| perth | 1 | 63 | 1.6% | 12.2 | 1.8% | oldest tree in perth (i3, p6) |
| nijmegen | 0 | 62 | 0.0% | 7.3 | 3.8% | brakkenstein nijmegen maps (i3, p11) |
| krakow | 1 | 61 | 1.6% | 15.1 | 1.2% | kossaka (i4, p15) |
| istanbul | 2 | 59 | 3.4% | 6.8 | 4.2% | a ten ile ma (i1, p2) |
| munich | 2 | 59 | 3.4% | 8.5 | 3.2% | the hornbeam centre (i1, p59) |
| las-vegas | 0 | 59 | 0.0% | 19.5 | 0.8% | vegas trees (i27, p31) |
| berlin | 0 | 58 | 0.0% | 10.6 | 2.3% | berlin trees (i2, p50) |
| portland | 1 | 57 | 1.8% | 13.6 | 1.5% | - |
| sydney | 0 | 57 | 0.0% | 8.8 | 3.1% | the wishing tree sydney (i7, p10) |
| seattle | 5 | 53 | 9.4% | 6.4 | 4.6% | oldest tree in seattle (i2, p8) |
| mexico-city | 2 | 52 | 3.8% | 10.1 | 2.5% | ahuehuete mexico city (i2, p9) |
| cyprus | 2 | 51 | 3.9% | 7.1 | 3.9% | oldest tree in cyprus (i4, p10) |
| reykjavik | 1 | 48 | 2.1% | 17.9 | 1.0% | oldest tree in iceland (i3, p7) |
| montreal | 3 | 47 | 6.4% | 9.2 | 2.9% | mckenna grave height (i1, p5) |
| greece | 0 | 46 | 0.0% | 36.7 | 0.4% | greek trees (i4, p34) |
| chicago | 4 | 45 | 8.9% | 11.5 | 2.0% | wooded grove (i1, p48) |
| budapest | 1 | 45 | 2.2% | 7.0 | 4.0% | - |
| cagliari | 2 | 43 | 4.7% | 4.7 | 7.3% | ficus macrophylla cagliari (i2, p6) |
| sintra | 1 | 43 | 2.3% | 6.0 | 5.0% | - |
| utrecht | 0 | 41 | 0.0% | 9.0 | 3.0% | zocher utrecht (i2, p22) |
| vilnius | 0 | 41 | 0.0% | 9.6 | 2.7% | amur linden (i1, p60) |
| melbourne | 7 | 39 | 17.9% | 8.5 | 3.2% | - |
| bordeaux | 4 | 39 | 10.3% | 5.9 | 5.2% | e bordeaux? (i1, p1) |
| tokyo | 1 | 39 | 2.6% | 7.4 | 3.8% | - |
| boston | 2 | 36 | 5.6% | 10.7 | 2.2% | - |
| the-hague | 1 | 35 | 2.9% | 8.6 | 3.2% | arentsburg (i1, p7) |
| groningen | 1 | 34 | 2.9% | 9.7 | 2.6% | oak groningen (i1, p7) |
| geneva | 2 | 33 | 6.1% | 7.9 | 3.5% | - |
| bristol | 2 | 32 | 6.2% | 10.0 | 2.5% | domesday oak (i1, p8) |
| new-orleans | 1 | 32 | 3.1% | 23.7 | 0.7% | anseman oak (i3, p9) |
| glasgow | 0 | 32 | 0.0% | 9.2 | 2.9% | - |
| strasbourg | 1 | 31 | 3.2% | 8.1 | 3.5% | - |
| cadiz | 0 | 31 | 0.0% | 7.1 | 4.0% | cadiz botanical gardens (i1, p2) |
| quebec-city | 2 | 30 | 6.7% | 8.0 | 3.5% | wych elm (i1, p25) |
| oxford | 4 | 29 | 13.8% | 6.6 | 4.4% | - |
| porto | 2 | 29 | 6.9% | 9.5 | 2.8% | - |
| sorrento | 1 | 29 | 3.4% | 11.3 | 2.1% | - |
| oahu | 1 | 28 | 3.6% | 6.5 | 4.5% | baobab hawaii (i1, p6) |
| oslo | 2 | 28 | 7.1% | 7.8 | 3.6% | "oldest ginkgo tree" park motto (i1, p5) |
| austin | 0 | 27 | 0.0% | 12.4 | 1.7% | antebellum oaks (i1, p54) |
| eindhoven | 1 | 26 | 3.8% | 14.1 | 1.4% | beukenboom (i1, p3) |
| nara | 1 | 26 | 3.8% | 8.7 | 3.2% | - |
| warsaw | 1 | 25 | 4.0% | 10.5 | 2.3% | aleja niepodleglosci (i1, p11) |
| arnhem | 0 | 25 | 0.0% | 8.1 | 3.5% | musispark arnhem (i1, p4) |
| helsinki | 0 | 25 | 0.0% | 5.0 | 7.0% | in helsinki (i1, p4) |
| lyon | 1 | 24 | 4.2% | 6.5 | 4.5% | antoine rivoire (i2, p8) |
| hong-kong | 0 | 23 | 0.0% | 6.9 | 4.1% | 樹齡 (i1, p4) |
| potsdam | 0 | 21 | 0.0% | 16.9 | 1.1% | glienicker park (i1, p63) |
| trieste | 0 | 21 | 0.0% | 10.9 | 2.2% | piazza hortis (i3, p10) |
| dubrovnik | 0 | 20 | 0.0% | 6.2 | 4.8% | - |
| nuremberg | 0 | 20 | 0.0% | 7.0 | 4.0% | kontumazgarten (i1, p11) |
| graz | 1 | 19 | 5.3% | 14.6 | 1.3% | oak (i4, p10) |
| dallas | 0 | 19 | 0.0% | 8.6 | 3.2% | centennial tree (i3, p12) |
| washington-dc | 0 | 19 | 0.0% | 16.9 | 1.0% | state tree of washington dc (i1, p53) |
| cordoba | 0 | 18 | 0.0% | 34.5 | 0.4% | ginkgo location (i1, p63) |
| cork | 0 | 18 | 0.0% | 9.0 | 3.0% | oldest tree in ireland (i3, p12) |
| maastricht | 0 | 18 | 0.0% | 7.9 | 3.5% | tulip maastricht (i1, p20) |
| tallinn | 0 | 18 | 0.0% | 5.5 | 6.0% | - |
| pamplona | 2 | 17 | 11.8% | 4.2 | 7.8% | "quercus short" (i4, p5) |
| braga | 2 | 17 | 11.8% | 9.5 | 2.7% | santa tecla braga (i1, p1) |
| catania | 1 | 17 | 5.9% | 5.5 | 6.1% | - |
| houston | 1 | 17 | 5.9% | 48.6 | 0.4% | trees in houston texas (i3, p67) |
| ljubljana | 1 | 17 | 5.9% | 8.4 | 3.3% | trees ljubljana (i1, p9) |
| aarhus | 0 | 17 | 0.0% | 8.4 | 3.3% | happy pig (i1, p11) |
| bangkok | 0 | 17 | 0.0% | 10.4 | 2.4% | - |
| guimaraes | 0 | 17 | 0.0% | 11.9 | 1.8% | pine tree portugal (i4, p18) |
| brno | 0 | 16 | 0.0% | 3.9 | 8.4% | - |
| hobart | 0 | 16 | 0.0% | 11.8 | 1.9% | - |
| osaka | 0 | 16 | 0.0% | 8.7 | 3.2% | - |
| granada | 1 | 15 | 6.7% | 4.9 | 7.1% | - |
| bratislava | 2 | 14 | 14.3% | 6.4 | 4.6% | - |
| cambridge | 2 | 14 | 14.3% | 10.0 | 2.5% | isaac newton tree cambridge (i1, p51) |
| bilbao | 1 | 14 | 7.1% | 5.8 | 5.4% | bilbao trees (i1, p7) |
| poznan | 1 | 14 | 7.1% | 17.0 | 1.0% | - |
| leipzig | 0 | 14 | 0.0% | 13.8 | 1.4% | beech leaf disease (i1, p19) |
| rotterdam | 1 | 13 | 7.7% | 7.2 | 3.9% | delftseplein (i2, p4) |
| sapporo | 1 | 13 | 7.7% | 10.8 | 2.2% | braga circuit (i1, p16) |
| emmen | 0 | 13 | 0.0% | 6.3 | 4.7% | rensenpark emmen former zoo park (i1, p6) |
| lucca | 0 | 13 | 0.0% | 7.5 | 3.8% | balearic box (i1, p7) |
| riga | 0 | 13 | 0.0% | 5.6 | 5.8% | brisbane river sewage (i1, p9) |
| belgrade | 1 | 12 | 8.3% | 8.0 | 3.5% | - |
| zurich | 1 | 12 | 8.3% | 6.5 | 4.5% | - |
| nice | 0 | 12 | 0.0% | 5.4 | 6.2% | promenade des anglais palm trees (i1, p5) |
| turin | 0 | 12 | 0.0% | 6.3 | 4.7% | - |
| venlo | 0 | 12 | 0.0% | 19.4 | 0.8% | sequoia waterloo (i1, p74) |
| verona | 0 | 12 | 0.0% | 7.3 | 3.8% | - |
| cologne | 1 | 11 | 9.1% | 7.9 | 3.5% | gibt es das in köln (i1, p4) |
| buenos-aires | 0 | 11 | 0.0% | 10.5 | 2.3% | trees in buenos aires (i1, p18) |
| vancouver | 0 | 11 | 0.0% | 13.7 | 1.5% | ancient trees of vancouver (i3, p29) |
| como | 1 | 10 | 10.0% | 6.6 | 4.4% | como tree (i1, p7) |
| delft | 1 | 10 | 10.0% | 15.4 | 1.2% | - |
| kamakura | 1 | 10 | 10.0% | 6.1 | 4.9% | kamakura tree (i4, p6) |
| australia | 0 | 10 | 0.0% | 18.3 | 0.9% | oldest tree in australia (i2, p50) |
| bari | 0 | 10 | 0.0% | 7.1 | 4.0% | roots quasano (i2, p12) |
| dordrecht | 0 | 10 | 0.0% | 7.5 | 3.8% | - |
| frankfurt | 0 | 10 | 0.0% | 6.6 | 4.4% | what tree is this (i1, p6) |
| tilburg | 0 | 10 | 0.0% | 9.9 | 2.5% | leijpark (i1, p11) |

**The language test** (Contract J v1.13: a translated set should pass its English twin's impressions within four weeks of indexing):

| Lang | City | Clicks | Impressions | Position | English twin |
|---|---|---:|---:|---:|---:|
| de | berlin | 0 | 94 | 22.4 | 58 |
| es | malaga | 1 | 89 | 13.3 | 131 |
| de | vienna | 2 | 72 | 9.0 | 146 |
| ja | kyoto | 2 | 69 | 10.4 | 69 |
| pt | lisbon | 3 | 53 | 9.6 | 255 |
| pt | porto | 1 | 50 | 6.4 | 29 |
| ja | tokyo | 1 | 46 | 10.5 | 39 |
| it | rome | 3 | 44 | 9.8 | 601 |
| es | barcelona | 0 | 41 | 15.1 | 228 |
| it | palermo | 0 | 41 | 10.5 | 74 |
| de | zurich | 1 | 26 | 9.3 | 12 |
| nl | amsterdam | 1 | 24 | 4.1 | 375 |
| pt | sintra | 1 | 24 | 12.8 | 43 |
| es | cadiz | 1 | 23 | 15.8 | 31 |
| es | tenerife | 0 | 23 | 25.8 | 140 |
| es | madrid | 0 | 19 | 7.5 | 66 |
| nl | nijmegen | 0 | 18 | 7.9 | 62 |
| ja | osaka | 2 | 16 | 12.6 | 16 |
| it | milan | 0 | 14 | 13.2 | 152 |
| fr | geneva | 1 | 12 | 20.2 | 33 |
| fr | nice | 0 | 11 | 18.5 | 12 |
| fr | paris | 0 | 5 | 6.4 | 116 |
| nl | the-hague | 0 | 3 | 7.7 | 35 |
- Seen, not clicked: /rome (c2/i223, 0.9%) for trees in rome (i47, p10); rome trees (i40, p9); roman trees (i14, p11)
- Seen, not clicked: /species/strawberry-tree (c0/i100, 0.0%) for strawberry tree (i28, p64); arbutus strawberry tree (i10, p61); strawberry trees (i5, p68)
- Seen, not clicked: /species/osage-orange (c0/i56, 0.0%) for osage orange (i11, p84); osage orange tree (i3, p83); osage oranges (i2, p88)
- Seen, not clicked: /hilo/loulu-palm-of-kalakaua-park (c0/i46, 0.0%) for loulu palm (i42, p76); loulu palm tree (i2, p52); loulu tree (i1, p47)
- Seen, not clicked: /species/austrian-pine (c0/i32, 0.0%) for austrian pine (i10, p93); austrian pine tree (i8, p83); austrian pine trees (i7, p75)
- Seen, not clicked: /species/bunya-pine (c0/i29, 0.0%) for bunya pine (i10, p74); bunya tree (i5, p78); bunya pine tree (i2, p74)
- Seen, not clicked: /species/dragon-tree (c0/i29, 0.0%) for dragon tree (i10, p47); dragon trees (i9, p47); dragontree (i5, p68)
- Seen, not clicked: /species/silver-maple (c0/i29, 0.0%) for silver maple tree (i7, p58); silver maple (i6, p60); sliver maple (i2, p60)

**Climbing** (this ten days against the ten before it)

| Page | Impressions | Change | Position | Moved | Clicks |
|---|---:|---:|---:|---:|---:|
| /rome | 556 | +336 | 9.5 | +3.7 | +7 |
| /seville | 150 | +98 | 8.5 | +3.1 | +8 |
| /species/strawberry-tree | 120 | +89 | 64.9 | +2.1 | +0 |
| / | 145 | +77 | 17.7 | - | +8 |
| /collections/trees-older-than-400-years | 89 | +65 | 19.6 | +10.9 | +0 |
| /lisbon | 207 | +61 | 7.5 | +0.9 | +2 |
| /species/osage-orange | 100 | +47 | 80.4 | -0.3 | +0 |
| /hilo/loulu-palm-of-kalakaua-park | 53 | +43 | 71.2 | +28.3 | +0 |

**Newly ranking** (no impressions at all ten days ago)

| Page | Impressions | Clicks | Position |
|---|---:|---:|---:|
| /amsterdam/elm-of-elsenhoeve | 110 | 4 | 6.2 |
| /collections/tallest-trees | 46 | 0 | 32.6 |
| /species/austrian-pine | 39 | 0 | 81.3 |
| /sydney/wishing-tree | 35 | 0 | 10.9 |
| /athens/olive-tree-of-pisistratus | 34 | 0 | 11.4 |
| /de/berlin/kaisereiche | 28 | 0 | 17.8 |

**Slipping**

| Page | Impressions | Change | Position | Moved |
|---|---:|---:|---:|---:|
| /madrid | 42 | -69 | 17.5 | -3.9 |
| /es/malaga/ficus-avenue-of-the-alameda-principal | 19 | -35 | 7.5 | -2.0 |
| /reykjavik | 24 | -9 | 24.5 | -3.0 |
| /amsterdam/oudemanhuispoort-elm | 23 | -8 | 7.4 | -0.7 |

- New queries this window: cannonball tree singapore (i6).

**Who they are**
Audience, 28 days of search (494 clicks, 20983 impressions):
- Countries: usa c89/i4659; gbr c56/i2397; nld c30/i1013; aus c25/i737; can c22/i667
- Devices: MOBILE c332/i11421; DESKTOP c155/i9380; TABLET c7/i182
- Landing pages: / c30/i233; /prague c25/i349; /lisbon c13/i396; /seville c11/i217; /rome c10/i865

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-26 | 80 | 110 |
| 08-27 | 60 | 140 |
| 08-28 | 120 | 170 |
| 08-29 | 60 | 140 |
| 08-30 | 70 | 180 |
| 08-31 | 30 | 90 |
| 09-01 | 80 | 120 |
| 09-02 | 110 | 270 |
| **window** | **610** | **1220** |
- Top paths: / (130); /explore (60); /prague/beethoven-plane (40); /account (40); /melbourne/remnant-river-red-gum-of-edinburgh-gardens (30); /nijmegen/wilhelminaboom-of-hertogplein (30); /melbourne (30); /barcelona (20); /australia (20); /prague (20); /brisbane/hoop-pine (20); /zwolle (20)
- Referrers: ancienttrees.app (610); (direct) (380); www.google.com (230)
- Moved between our own pages: 610 of 1220 pageviews (50%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: US (210); AU (190); NL (170); GB (120); ES (90)
- Devices: mobile (620); desktop (570); tablet (30)
- Page load (8d): p50 641ms, p90 3094ms

Links: external referrers (a link somebody actually clicked): none yet
AI: arrivals from an assistant that cited us: none yet


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 09-02T17:29 | 50.3 | 0 | 40 | 47 | Alicante, Bologna, Mexico City, Sardinia, +2 more |
| 09-02T20:15 | 0.0 | 0 | 0 | 0 | - |
| 09-02T23:35 | 95.1 | 35 | 19 | 45 | Heidelberg +6, Stuttgart +6, Freiburg +4, Taipei +4, +13 more |
| 09-03T01:11 | 73.2 | 51 | 34 | 28 | Freiburg +7, Stuttgart +7, Heidelberg +6, Taipei +4, +25 more |
| 09-03T02:26 | 63.1 | 29 | 22 | 43 | Priekule +5, Kaunas +4, Albersdorf +1, Bad Staffelstein +1, +86 more |
| 09-03T06:30 | 20.6 | 0 | 4 | 38 | - |
| 09-03T06:52 | 33.9 | 1 | 17 | 37 | Robenhausen +1 |
| 09-03T11:44 | 35.0 | 9 | 11 | 4 | Giessen +4, Aga +1, Biei +1, Effeltrich +1, +2 more |
| 09-03T12:20 | 65.1 | 18 | 21 | 28 | Giessen +4, Aga +1, Biei +1, Effeltrich +1, +11 more |
| 09-03T15:13 | 101.2 | 14 | 26 | 51 | Malsfeld +4, Iwata +1, Kanagi +1, Kitamoto +1, +7 more |
| **10 runs** | **538** | **157** | **194** | | |

- 3 of 10 produced no trees; 4 to 51 commands refused per run; 2 wrote nothing to LOG.md.

**What they made**

- Clean up: delete fully-published famousjapan batch verify files
- Fix smoke test: stop requiring the walking-routes pill it no longer has
- Ship Higashimiyoshi and Shingu: two new single-tree Japan places
- Answer 2026-09-03 review WARN: Home.swift hero tagline already fixed
- famous_demand.py: filter leads already published under a different id
- mail-health heartbeat
- Contributor replies sent, log updated
- LOG.md: record the Malsfeld continuation run
- Malsfeld: 4 guided lindens of the Schwalm-Eder district, new German place
- LOG.md: note the Kamo no Okusu duplicate near-miss and the fix
- Shokawa: a new single-tree Japan place, the twin cherries moved to escape a dam
- LOG.md: record this continuation run
- Two new single-tree places in Japan: Kanagi (Jūnihon-yasu) and Ueki (Jakushin-san no Kusu)
- Matera: record the write pass, still held at 3 below the 4-tree floor

Machine: 11 chain attempts yesterday, 10 got real work time (~602 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 7 clicks and 201 impressions on Google's freshest day (day before: c29/i1028). Directional at best; no strategic conclusions from these volumes.

## 2026-09-01 (previous UTC day)

**Today: an account was opened yesterday (5 total).**

**Did the product happen**

| Action | Yesterday | 14 days | Ever | Last |
|---|---:|---:|---:|---|
| app-cta | 1 | 24 | 46 | yesterday |
| directions | 2 | 33 | 33 | yesterday |
| search-home | 0 | 27 | 29 | 2 days ago |
| save | 0 | 10 | 12 | 3 days ago |
| waitlist-submit | 0 | 9 | 11 | 2 days ago |
| walks-app | 1 | 5 | 8 | yesterday |
| search-explore | 1 | 6 | 7 | yesterday |
| suggestion-submit | 0 | 4 | 4 | 3 days ago |
| walk-open | 0 | 0 | 4 | 16 days ago |
| smoke-test | 0 | 0 | 2 | 32 days ago |
| beacon-fix-verify | 0 | 0 | 1 | 17 days ago |
| beacon-test | 0 | 0 | 1 | 17 days ago |
| worthit-not worth it | 0 | 0 | 1 | 16 days ago |
| signin-link-sent | 0 | 0 | 0 | never |
| walk-start | 0 | 0 | 0 | never |
| worthit-worth it | 0 | 0 | 0 | never |
| **all** | **5** | **118** | **159** | |
- 'Ever' counts every row in the events table, which begins 2026-08-01 when the funnel was repaired. Anything named here with a zero has never fired at all.

**What people typed into our search** (14 days, 26 searches, 17 different terms)

| Typed | Times |
|---|---:|
| mel | 6 |
| melb | 3 |
| melbourne | 3 |
| berli | 1 |
| boston | 1 |
| ei | 1 |
| glasg | 1 |
| leiden | 1 |
| london | 1 |
| melbo | 1 |
| melbou | 1 |
| milano | 1 |
| oslo | 1 |
| portland | 1 |
| prague | 1 |
| sea | 1 |
| sy | 1 |

| Day | Accounts | Waitlist | Saves | Trees sent | Feedback |
|---|---:|---:|---:|---:|---:|
| 08-19 | 0 | 1 | 0 | 0 | 0 |
| 08-20 | 0 | 1 | 3 | 0 | 1 |
| 08-21 | 1 | 0 | 0 | 0 | 1 |
| 08-22 | 0 | 0 | 1 | 0 | 0 |
| 08-23 | 0 | 0 | 0 | 0 | 0 |
| 08-24 | 0 | 0 | 0 | 0 | 0 |
| 08-25 | 0 | 1 | 0 | 0 | 0 |
| 08-26 | 0 | 1 | 1 | 0 | 0 |
| 08-27 | 0 | 1 | 0 | 0 | 1 |
| 08-28 | 0 | 1 | 0 | 0 | 0 |
| 08-29 | 0 | 0 | 0 | 0 | 0 |
| 08-30 | 1 | 0 | 5 | 1 | 0 |
| 08-31 | 0 | 2 | 0 | 0 | 0 |
| 09-01 | 1 | 0 | 0 | 0 | 0 |
| 09-02 | 0 | 0 | 0 | 0 | 0 |
| **14 days** | **3** | **8** | **10** | **1** | **3** |
- Our own rows are not in this table: 7 trees, 22 feedback, 2 accounts. They are testing, and counting them reads as traction.
- Waitlist:    16 total, newest 2 days ago
- Submissions: 7 total (1 trees sent, 6 feedback), newest 3 days ago
- Accounts:    5 total, newest yesterday

**What readers told us** (14 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-21 | par_001 (The Robinier of Square Re | not worth it | - | no acct | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | report | could not reach it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | us | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | us | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | worth it | - | us | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | vote undone | worth it | us | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | not worth it | - | us | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | us | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | us | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | us | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | not worth it | us | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | us | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | us | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | us | holds |
| 08-24 | Baarn | tree sent in | 4 chars, read it in the database | us | open_question |
| 08-25 | utr_005 (Onder de Linden) | vote undone | not worth it | us | - |
| 08-26 | sar_003 (The Olivastro of Santa Ma | worth it | - | us | - |
| 08-27 | ams_001 | worth it | - | 46c1 | holds |
| 08-27 | Baarn | tree sent in | 4 chars, read it in the database | us | holds |
| 08-28 | - | Super | - | us | - |
| 08-29 | Baarn | tree sent in | 4 chars, read it in the database | us | holds |
| 08-29 | Baarn | tree sent in | - | us | holds |
| 08-30 | rom_002 (Adonis) | worth it | - | us | - |
| 08-30 | rom_002 (Adonis) | vote undone | worth it | us | - |
| 08-30 | rom_002 (Adonis) | not worth it | - | us | - |
| 08-30 | rom_002 (Adonis) | vote undone | not worth it | us | - |
| 08-30 | rom_002 (Adonis) | worth it | - | us | - |
| 08-30 | rom_002 (Adonis) | vote undone | worth it | us | - |
| 08-30 | rom_002 (Adonis) | not worth it | - | us | - |
| 08-30 | rom_002 (Adonis) | vote undone | not worth it | us | - |
| 08-30 | rom_002 (Adonis) | worth it | - | us | - |
| 08-30 | London Plane | tree sent in | 71 chars, read it in the database | 21dc | holds |
| 08-31 | Amsterdam | tree sent in | - | us | open_question |
| 08-31 | Baarn | tree sent in | - | us | open_question |
| 09-01 | Baarn | tree sent in | - | us | holds |

- 45 of these 51 rows are ours, marked us. The rest is the reader traffic.
- 4 arrived signed out, so they cannot be told apart.
- 2 rows from 2 accounts.

**The funnel, as rates**
- Seen to clicked: 2.2% (303 of 13700) vs 2.4% the fortnight before
- Pages per visit: 1.7 (1470 visits, 2450 pageviews since 2026-08-08)
- Visits that did something: 10.7% (157 actions on 1470 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-23 | 15 | 958 | 1.6% | 16.2 |
| 08-24 | 28 | 998 | 2.8% | 15.9 |
| 08-25 | 19 | 1108 | 1.7% | 20.1 |
| 08-26 | 24 | 1144 | 2.1% | 18.7 |
| 08-27 | 15 | 1003 | 1.5% | 18.8 |
| 08-28 | 27 | 1014 | 2.7% | 16.3 |
| 08-29 | 32 | 1068 | 3.0% | 17.6 |
| 08-30 | 32 | 1065 | 3.0% | 19.2 |
| 08-31 | 21 | 948 | 2.2% | 16.3 |
| 09-01 *partial* | 20 | 623 | 3.2% | 9.5 |
| **window** | **233** | **9929** | **2.3%** | |
- Top queries (10d): dutch elm amsterdam (i61, p4); ancient tree (i16, p29); ancient trees (i25, p24); cannonball tree singapore (i6, p9); e bordeaux? (i1, p1)
- Top pages (10d): / (c15/i140); /prague (c14/i125); /seville (c8/i157); /lisbon (c7/i195); /rome (c6/i454)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - '"oldest of its species" owl park' (i7, p9)
    - '"quercus short"' (i4, p5)
    - '"400 years old as of 2023" tree' (i2, p8)
    - '"quercus aggressive"' (i2, p6)
    - '"courtyard" "okinawa"' (i1, p9)
    - '"oldest of its species" "park" tree' (i1, p10)
    - '10 feet tall trees' (i1, p58)
    - '400 year old tree' (i1, p7)
    - and 4 more

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| rome | 6 | 508 | 1.2% | 9.9 | 2.5% | trees in rome (i37, p11) |
| amsterdam | 9 | 397 | 2.3% | 8.3 | 3.3% | dutch elm amsterdam (i49, p4) |
| lisbon | 9 | 245 | 3.7% | 7.6 | 3.7% | oldest tree in lisbon (i7, p8) |
| singapore | 5 | 195 | 2.6% | 10.9 | 2.2% | oldest tree in singapore (i24, p10) |
| seville | 9 | 193 | 4.7% | 8.3 | 3.4% | a to? (i1, p1) |
| barcelona | 7 | 193 | 3.6% | 9.8 | 2.6% | barcelona trees (i8, p8) |
| london | 3 | 170 | 1.8% | 23.5 | 0.7% | old trees near me (i2, p7) |
| brisbane | 6 | 163 | 3.7% | 18.2 | 0.9% | the big macadamia nut (i10, p63) |
| tenerife | 2 | 162 | 1.2% | 8.6 | 3.2% | drago milenario (i11, p11) |
| copenhagen | 4 | 156 | 2.6% | 10.3 | 2.4% | trees in copenhagen (i22, p17) |
| milan | 0 | 145 | 0.0% | 8.3 | 3.4% | "oldest of its species" owl park (i7, p9) |
| malaga | 2 | 143 | 1.4% | 13.7 | 1.5% | árboles históricos de málaga (i13, p80) |
| vienna | 4 | 141 | 2.8% | 9.8 | 2.6% | alter (i1, p3) |
| prague | 15 | 139 | 10.8% | 7.4 | 3.8% | - |
| florence | 3 | 127 | 2.4% | 7.6 | 3.7% | florence trees (i4, p5) |
| crete | 0 | 119 | 0.0% | 10.5 | 2.3% | kavousi olive tree (i2, p10) |
| paris | 2 | 117 | 1.7% | 17.9 | 1.0% | trees in paris france (i4, p52) |
| bath | 2 | 106 | 1.9% | 7.4 | 3.8% | how old is the tree in abbey green bath (i5, p8) |
| naples | 0 | 105 | 0.0% | 10.2 | 2.4% | naples tree (i3, p6) |
| madeira | 2 | 101 | 2.0% | 9.4 | 2.8% | fanal witch tree (i10, p20) |
| brussels | 1 | 92 | 1.1% | 11.3 | 2.1% | belgium trees (i2, p10) |
| fukuoka | 3 | 92 | 3.3% | 12.0 | 1.8% | couple camphor trees (i3, p9) |
| seoul | 0 | 90 | 0.0% | 14.9 | 1.2% | korean trees (i2, p47) |
| toronto | 1 | 89 | 1.1% | 8.5 | 3.3% | big red oak (i17, p7) |
| palma-de-mallorca | 0 | 88 | 0.0% | 7.1 | 4.0% | placa de cort palma olive tree (i2, p8) |
| edinburgh | 4 | 83 | 4.8% | 12.6 | 1.7% | edinburgh trees (i1, p52) |
| new-york | 1 | 81 | 1.2% | 17.7 | 1.0% | - |
| sardinia | 0 | 81 | 0.0% | 7.7 | 3.6% | baltolu sardinia (i14, p7) |
| bologna | 0 | 78 | 0.0% | 7.3 | 3.8% | - |
| venice | 0 | 77 | 0.0% | 5.7 | 5.6% | trees in venice (i3, p8) |
| alicante | 0 | 75 | 0.0% | 8.0 | 3.5% | how old (i1, p3) |
| madrid | 1 | 74 | 1.4% | 15.2 | 1.2% | oldest tree in madrid (i3, p9) |
| dublin | 3 | 73 | 4.1% | 13.1 | 1.6% | hybrid strawberry tree (i1, p10) |
| palermo | 1 | 72 | 1.4% | 6.5 | 4.5% | giardini reali palermo (i1, p14) |
| kyoto | 1 | 69 | 1.4% | 10.4 | 2.3% | japanese camphor (i1, p84) |
| valencia | 2 | 65 | 3.1% | 8.1 | 3.5% | ficus centenarios de la glorieta (i1, p12) |
| las-vegas | 0 | 64 | 0.0% | 21.7 | 0.7% | vegas trees (i35, p32) |
| hilo | 1 | 60 | 1.7% | 59.9 | 0.4% | loulu palm (i39, p75) |
| athens | 1 | 58 | 1.7% | 12.3 | 1.7% | amritara olive trotter (i1, p84) |
| perth | 1 | 58 | 1.7% | 11.5 | 2.0% | oldest tree in perth (i3, p6) |
| istanbul | 2 | 56 | 3.6% | 6.8 | 4.2% | a ten ile ma (i1, p2) |
| mexico-city | 2 | 56 | 3.6% | 9.6 | 2.7% | ahuehuete mexico city (i2, p9) |
| nijmegen | 0 | 56 | 0.0% | 7.2 | 3.9% | brakkenstein nijmegen maps (i3, p11) |
| sydney | 0 | 56 | 0.0% | 7.3 | 3.8% | the wishing tree sydney (i7, p10) |
| munich | 2 | 55 | 3.6% | 8.5 | 3.2% | the hornbeam centre (i1, p59) |
| krakow | 1 | 54 | 1.9% | 13.8 | 1.4% | kossaka (i2, p10) |
| cyprus | 2 | 52 | 3.8% | 7.1 | 4.0% | oldest tree in cyprus (i4, p10) |
| portland | 1 | 51 | 2.0% | 14.9 | 1.2% | - |
| berlin | 0 | 51 | 0.0% | 11.2 | 2.1% | berlin trees (i2, p50) |
| leiden | 0 | 51 | 0.0% | 11.9 | 1.8% | "oldest of its species" ginkgo park (i12, p8) |
| seattle | 4 | 50 | 8.0% | 6.6 | 4.4% | oldest tree in seattle (i2, p8) |
| reykjavik | 0 | 50 | 0.0% | 19.5 | 0.8% | iceland tree (i2, p61) |
| chicago | 4 | 49 | 8.2% | 10.3 | 2.4% | wooded grove (i1, p48) |
| greece | 0 | 48 | 0.0% | 34.9 | 0.4% | greek trees (i4, p34) |
| montreal | 2 | 47 | 4.3% | 9.1 | 2.9% | mckenna grave height (i1, p5) |
| budapest | 1 | 41 | 2.4% | 6.9 | 4.1% | - |
| bordeaux | 3 | 39 | 7.7% | 6.4 | 4.6% | e bordeaux? (i1, p1) |
| utrecht | 0 | 39 | 0.0% | 9.3 | 2.8% | zocher utrecht (i2, p22) |
| vilnius | 0 | 39 | 0.0% | 7.9 | 3.5% | willow tree in lithuanian (i2, p9) |
| sintra | 1 | 38 | 2.6% | 5.8 | 5.4% | - |
| cagliari | 0 | 37 | 0.0% | 4.7 | 7.3% | ficus macrophylla cagliari (i2, p6) |
| tokyo | 1 | 36 | 2.8% | 7.3 | 3.8% | - |
| groningen | 1 | 34 | 2.9% | 12.9 | 1.6% | oak groningen (i1, p7) |
| geneva | 2 | 33 | 6.1% | 9.1 | 3.0% | - |
| melbourne | 7 | 32 | 21.9% | 8.8 | 3.1% | - |
| new-orleans | 1 | 32 | 3.1% | 23.7 | 0.7% | anseman oak (i3, p9) |
| the-hague | 1 | 32 | 3.1% | 8.2 | 3.4% | arentsburg (i1, p7) |
| cadiz | 0 | 32 | 0.0% | 7.1 | 3.9% | cadiz botanical gardens (i1, p2) |
| bristol | 2 | 31 | 6.5% | 10.3 | 2.4% | domesday oak (i1, p8) |
| boston | 2 | 30 | 6.7% | 14.6 | 1.3% | - |
| porto | 2 | 29 | 6.9% | 9.7 | 2.7% | alameda dos platanos (i2, p6) |
| strasbourg | 2 | 29 | 6.9% | 7.9 | 3.6% | - |
| glasgow | 0 | 29 | 0.0% | 9.1 | 2.9% | - |
| oxford | 3 | 28 | 10.7% | 6.8 | 4.2% | - |
| sorrento | 1 | 28 | 3.6% | 11.5 | 2.0% | - |
| quebec-city | 1 | 26 | 3.8% | 7.7 | 3.7% | wych elm (i1, p25) |
| nara | 1 | 25 | 4.0% | 9.0 | 3.0% | - |
| oahu | 1 | 25 | 4.0% | 6.4 | 4.6% | - |
| oslo | 2 | 25 | 8.0% | 8.4 | 3.3% | "oldest ginkgo tree" park motto (i1, p5) |
| eindhoven | 0 | 24 | 0.0% | 11.6 | 1.9% | beukenboom (i1, p3) |
| helsinki | 0 | 24 | 0.0% | 4.7 | 7.3% | in helsinki (i1, p4) |
| hong-kong | 0 | 23 | 0.0% | 6.7 | 4.3% | 樹齡 (i1, p4) |
| warsaw | 2 | 22 | 9.1% | 7.3 | 3.9% | - |
| arnhem | 0 | 22 | 0.0% | 8.4 | 3.3% | musispark arnhem (i1, p4) |
| trieste | 0 | 22 | 0.0% | 10.3 | 2.4% | piazza hortis (i3, p10) |
| washington-dc | 0 | 22 | 0.0% | 18.8 | 0.9% | survey lodge ranger station (i2, p12) |
| lyon | 1 | 20 | 5.0% | 6.5 | 4.5% | antoine rivoire (i2, p8) |
| cambridge | 1 | 19 | 5.3% | 11.2 | 2.1% | milton tree (i1, p9) |
| graz | 1 | 19 | 5.3% | 14.2 | 1.4% | oak (i3, p9) |
| maastricht | 1 | 19 | 5.3% | 8.0 | 3.5% | tulip maastricht (i1, p20) |
| aarhus | 0 | 19 | 0.0% | 8.2 | 3.4% | happy pig (i1, p11) |
| cordoba | 0 | 19 | 0.0% | 39.9 | 0.4% | ginkgo location (i1, p63) |
| guimaraes | 0 | 19 | 0.0% | 11.7 | 1.9% | pine tree portugal (i5, p18) |
| nuremberg | 0 | 19 | 0.0% | 7.1 | 3.9% | kontumazgarten (i1, p11) |
| potsdam | 0 | 19 | 0.0% | 13.9 | 1.4% | glienicker park (i1, p63) |
| austin | 0 | 18 | 0.0% | 12.6 | 1.7% | antebellum oaks (i1, p54) |
| catania | 1 | 17 | 5.9% | 5.4 | 6.2% | - |
| cork | 1 | 17 | 5.9% | 9.3 | 2.9% | oldest tree in ireland (i3, p12) |
| houston | 1 | 17 | 5.9% | 48.6 | 0.4% | trees in houston texas (i3, p67) |
| dallas | 0 | 17 | 0.0% | 8.6 | 3.2% | centennial tree (i3, p12) |
| braga | 1 | 16 | 6.2% | 7.1 | 3.9% | santa tecla braga (i1, p1) |
| bangkok | 0 | 16 | 0.0% | 10.7 | 2.3% | - |
| dubrovnik | 0 | 16 | 0.0% | 6.6 | 4.4% | - |
| bilbao | 1 | 15 | 6.7% | 5.7 | 5.7% | bilbao trees (i1, p7) |
| delft | 2 | 15 | 13.3% | 18.3 | 0.9% | - |
| bratislava | 2 | 14 | 14.3% | 6.4 | 4.6% | - |
| osaka | 0 | 14 | 0.0% | 9.9 | 2.5% | - |
| tallinn | 0 | 14 | 0.0% | 5.9 | 5.1% | - |
| verona | 0 | 14 | 0.0% | 7.2 | 3.9% | - |
| belgrade | 1 | 13 | 7.7% | 8.0 | 3.5% | - |
| granada | 1 | 13 | 7.7% | 5.4 | 6.2% | - |
| brno | 0 | 13 | 0.0% | 4.6 | 7.4% | - |
| emmen | 0 | 13 | 0.0% | 6.3 | 4.7% | rensenpark emmen former zoo park (i1, p6) |
| lucca | 0 | 13 | 0.0% | 7.5 | 3.8% | balearic box (i1, p7) |
| poznan | 1 | 12 | 8.3% | 10.8 | 2.2% | - |
| australia | 0 | 12 | 0.0% | 18.8 | 0.9% | oldest tree in australia (i2, p50) |
| hobart | 0 | 12 | 0.0% | 14.2 | 1.4% | - |
| rotterdam | 0 | 12 | 0.0% | 8.1 | 3.5% | delftseplein (i2, p4) |
| turin | 0 | 12 | 0.0% | 5.8 | 5.5% | - |
| york | 0 | 12 | 0.0% | 9.5 | 2.8% | - |
| frankfurt | 0 | 11 | 0.0% | 6.3 | 4.7% | what tree is this (i1, p6) |
| venlo | 0 | 11 | 0.0% | 20.5 | 0.8% | sequoia waterloo (i1, p74) |

**The language test** (Contract J v1.13: a translated set should pass its English twin's impressions within four weeks of indexing):

| Lang | City | Clicks | Impressions | Position | English twin |
|---|---|---:|---:|---:|---:|
| es | malaga | 0 | 88 | 13.9 | 143 |
| de | berlin | 0 | 86 | 23.4 | 51 |
| de | vienna | 2 | 59 | 9.1 | 141 |
| ja | kyoto | 2 | 54 | 10.7 | 69 |
| pt | lisbon | 3 | 49 | 9.9 | 245 |
| pt | porto | 1 | 44 | 6.4 | 29 |
| it | rome | 3 | 42 | 10.0 | 508 |
| ja | tokyo | 1 | 42 | 10.5 | 36 |
| it | palermo | 0 | 34 | 8.6 | 72 |
| es | barcelona | 0 | 27 | 15.7 | 193 |
| pt | sintra | 1 | 24 | 12.8 | 38 |
| es | cadiz | 1 | 22 | 16.0 | 32 |
| es | madrid | 0 | 18 | 7.6 | 74 |
| nl | nijmegen | 0 | 18 | 7.9 | 56 |
| es | tenerife | 0 | 16 | 32.9 | 162 |
| nl | amsterdam | 0 | 16 | 3.6 | 397 |
| ja | osaka | 2 | 13 | 13.0 | 14 |
| de | zurich | 1 | 13 | 13.7 | 7 |
| it | milan | 0 | 13 | 13.4 | 145 |
| fr | geneva | 0 | 11 | 21.6 | 33 |
| fr | nice | 0 | 9 | 21.1 | 9 |
| fr | paris | 0 | 1 | 8.0 | 117 |
- Seen, not clicked: /rome (c1/i176, 0.6%) for trees in rome (i37, p11); rome trees (i27, p10); oldest tree in rome (i14, p6)
- Seen, not clicked: /species/strawberry-tree (c0/i93, 0.0%) for strawberry tree (i23, p66); arbutus strawberry tree (i10, p61); strawberry trees (i4, p67)
- Seen, not clicked: /species/osage-orange (c0/i53, 0.0%) for osage orange (i11, p84); where do osage orange trees grow (i2, p96); osage oranges (i2, p88)
- Seen, not clicked: / (c1/i47, 2.1%) for ancient trees (i23, p27); ancient tree (i12, p40); ancient tree map (i3, p17)
- Seen, not clicked: /hilo/loulu-palm-of-kalakaua-park (c0/i43, 0.0%) for loulu palm (i39, p75); loulu palm tree (i2, p52); loulu tree (i1, p47)
- Seen, not clicked: /las-vegas (c0/i35, 0.0%) for vegas trees (i35, p32)
- Seen, not clicked: /species/austrian-pine (c0/i32, 0.0%) for austrian pine (i10, p93); austrian pine tree (i8, p83); austrian pine trees (i7, p75)
- Seen, not clicked: /tenerife/el-drago-milenario (c0/i31, 0.0%) for drago milenario (i11, p11); el drago milenario (i6, p10); oldest tree tenerife (i3, p11)

**Climbing** (this ten days against the ten before it)

| Page | Impressions | Change | Position | Moved | Clicks |
|---|---:|---:|---:|---:|---:|
| /rome | 454 | +254 | 10.3 | +3.9 | +5 |
| /seville | 157 | +131 | 8.6 | +6.6 | +7 |
| /species/strawberry-tree | 114 | +89 | 65.6 | - | +0 |
| / | 140 | +77 | 16.7 | +1.5 | +5 |
| /lisbon | 195 | +63 | 7.4 | +1.5 | +3 |
| /species/osage-orange | 102 | +56 | 81.2 | -1.0 | +0 |
| /malaga | 130 | +53 | 14.6 | -0.5 | +0 |
| /collections/trees-older-than-400-years | 69 | +46 | 21.4 | +6.9 | +0 |

**Newly ranking** (no impressions at all ten days ago)

| Page | Impressions | Clicks | Position |
|---|---:|---:|---:|
| /amsterdam/elm-of-elsenhoeve | 109 | 4 | 6.1 |
| /species/austrian-pine | 39 | 0 | 81.3 |
| /collections/tallest-trees | 35 | 0 | 36.0 |
| /sydney/wishing-tree | 34 | 0 | 8.4 |
| /de/berlin/kaisereiche | 28 | 0 | 17.8 |
| /athens/olive-tree-of-pisistratus | 24 | 0 | 14.9 |

**Slipping**

| Page | Impressions | Change | Position | Moved |
|---|---:|---:|---:|---:|
| /madrid | 54 | -45 | 17.5 | -4.4 |
| /es/malaga | 24 | -31 | 10.7 | -0.7 |
| /es/malaga/ficus-avenue-of-the-alameda-principal | 22 | -29 | 7.5 | -2.1 |
| /singapore/tembusu-of-lawn-e | 20 | -6 | 9.1 | -0.7 |

- New queries this window: cannonball tree singapore (i6).

**Who they are**
Audience, 28 days of search (452 clicks, 19735 impressions):
- Countries: usa c83/i4324; gbr c53/i2305; nld c26/i949; aus c24/i674; esp c20/i1190
- Devices: MOBILE c307/i10768; DESKTOP c139/i8795; TABLET c6/i172
- Landing pages: / c27/i222; /prague c25/i332; /lisbon c12/i367; /seville c10/i200; /rome c8/i740

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-25 | 60 | 70 |
| 08-26 | 80 | 110 |
| 08-27 | 60 | 140 |
| 08-28 | 120 | 170 |
| 08-29 | 60 | 140 |
| 08-30 | 70 | 180 |
| 08-31 | 30 | 90 |
| 09-01 | 80 | 120 |
| **window** | **560** | **1020** |
- Top paths: / (110); /explore (70); /melbourne/remnant-river-red-gum-of-edinburgh-gardens (30); /nijmegen/wilhelminaboom-of-hertogplein (30); /prague (30); /brisbane/hoop-pine (20); /melbourne (20); /barcelona (20); /brussels (20); /sponsor (20); /zwolle (20); /amsterdam/cycad-of-the-hortus (10)
- Referrers: ancienttrees.app (460); (direct) (340); www.google.com (220)
- Moved between our own pages: 460 of 1020 pageviews (45%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: US (190); AU (160); NL (110); GB (100); ES (90)
- Devices: desktop (510); mobile (490); tablet (20)
- Page load (8d): p50 750ms, p90 3094ms

Links: external referrers (a link somebody actually clicked): none yet
AI: arrivals from an assistant that cited us: none yet


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 09-01T08:28 | 15.7 | 0 | 6 | 16 | - |
| 09-01T08:58 | 12.5 | 0 | 5 | 12 | - |
| 09-01T11:56 | 11.7 | 0 | 5 | 11 | - |
| 09-01T14:23 | 0.4 | 0 | 1 | - | - |
| 09-01T18:42 | 0.0 | 0 | 0 | - | - |
| 09-01T18:42 | 0.0 | 0 | 0 | - | - |
| 09-01T18:58 | 53.9 | 3 | 25 | 29 | Gonzales Texas +1, Princeton New Jersey +1, Wye Mills Maryland +1, Athens Georgia, +7 more |
| 09-01T22:10 | 45.7 | 5 | 8 | 11 | Auckland +5 |
| 09-02T01:08 | 50.3 | 2 | 5 | 36 | Bamberg +1, Nuremberg +1 |
| 09-02T02:00 | 14.4 | 0 | 7 | 15 | - |
| 09-02T05:58 | 46.4 | 4 | 13 | 28 | Curinga +1, Fara In Sabina +1, Gutau +1, Ramsau Am Dachstein +1 |
| 09-02T06:45 | 14.3 | 4 | 10 | 10 | Curinga +1, Fara In Sabina +1, Gutau +1, Ramsau Am Dachstein +1 |
| **12 runs** | **265** | **18** | **85** | | |

- 7 of 12 produced no trees; 10 to 36 commands refused per run; 3 wrote nothing to LOG.md.

**What they made**

- Verify famous-japan cherries: 3 ready, Kakunodate blocked as an avenue
- Update mail-health timestamp
- Log: four single-tree destination pages, iOS CI resolved
- Four single-tree destination pages: Gutau, Ramsau am Dachstein, Fara in Sabina, Curinga
- Verify 4 more famous Austria/Italy leads to READY
- Save iOS CI grep-bug fix as a patch for Hidde (can't push workflow files)
- Revert "Fix iOS CI false-positive: grep bug turned a passing test run red"
- Fix iOS CI false-positive: grep bug turned a passing test run red
- Retry SweepFrames on the testmanagerd connection-drop flake
- leads.py: sixth widening of NOT_READY_MARKER, plus a wrong-city case
- Bamberg +1, Nuremberg +1: finish standing verify claims; iOS CI bug found already fixed
- Mail health: routine bookkeeping update
- claim hokuto, miharu, neo-motosu for write passes
- claim _famous-japan for a verify pass (shelf refill)

Machine: 8 chain attempts yesterday, 7 got real work time (~218 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 20 clicks and 623 impressions on Google's freshest day (day before: c21/i948). Directional at best; no strategic conclusions from these volumes.

## 2026-08-31 (previous UTC day)

**Today: a waitlist arrived yesterday (16 total); 2 tree submissions arrived yesterday (35 total); an account was opened yesterday (5 total).**

**Did the product happen**

| Action | Yesterday | 14 days | Ever | Last |
|---|---:|---:|---:|---|
| app-cta | 5 | 43 | 45 | yesterday |
| directions | 7 | 31 | 31 | yesterday |
| search-home | 3 | 28 | 29 | yesterday |
| save | 0 | 12 | 12 | 2 days ago |
| waitlist-submit | 2 | 10 | 11 | yesterday |
| walks-app | 1 | 7 | 7 | yesterday |
| search-explore | 1 | 5 | 6 | yesterday |
| suggestion-submit | 0 | 4 | 4 | 2 days ago |
| walk-open | 0 | 0 | 4 | 15 days ago |
| smoke-test | 0 | 0 | 2 | 31 days ago |
| beacon-fix-verify | 0 | 0 | 1 | 16 days ago |
| beacon-test | 0 | 0 | 1 | 16 days ago |
| worthit-not worth it | 0 | 0 | 1 | 15 days ago |
| signin-link-sent | 0 | 0 | 0 | never |
| walk-start | 0 | 0 | 0 | never |
| worthit-worth it | 0 | 0 | 0 | never |
| **all** | **19** | **140** | **154** | |
- 'Ever' counts every row in the events table, which begins 2026-08-01 when the funnel was repaired. Anything named here with a zero has never fired at all.

**What people typed into our search** (14 days, 27 searches, 18 different terms)

| Typed | Times |
|---|---:|
| mel | 6 |
| melb | 3 |
| melbourne | 3 |
| berli | 1 |
| boston | 1 |
| ei | 1 |
| glasg | 1 |
| leiden | 1 |
| london | 1 |
| melbo | 1 |
| melbou | 1 |
| milano | 1 |
| oslo | 1 |
| portland | 1 |
| prague | 1 |
| sea | 1 |
| sofia | 1 |
| sy | 1 |

| Day | Accounts | Waitlist | Saves | Trees sent | Feedback |
|---|---:|---:|---:|---:|---:|
| 08-18 | 0 | 1 | 2 | 0 | 0 |
| 08-19 | 0 | 1 | 0 | 0 | 0 |
| 08-20 | 0 | 1 | 3 | 0 | 1 |
| 08-21 | 1 | 0 | 0 | 0 | 16 |
| 08-22 | 0 | 0 | 1 | 0 | 0 |
| 08-23 | 0 | 0 | 0 | 0 | 0 |
| 08-24 | 0 | 0 | 0 | 1 | 0 |
| 08-25 | 0 | 1 | 0 | 0 | 0 |
| 08-26 | 0 | 1 | 1 | 0 | 1 |
| 08-27 | 0 | 1 | 0 | 1 | 1 |
| 08-28 | 0 | 1 | 0 | 0 | 1 |
| 08-29 | 0 | 0 | 0 | 2 | 0 |
| 08-30 | 1 | 0 | 5 | 1 | 5 |
| 08-31 | 1 | 2 | 0 | 2 | 0 |
| 09-01 | 0 | 0 | 0 | 0 | 0 |
| **14 days** | **3** | **9** | **12** | **7** | **25** |
- Waitlist:    16 total, newest yesterday
- Submissions: 35 total (7 trees sent, 28 feedback), newest yesterday
- Accounts:    5 total, newest yesterday

**What readers told us** (14 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-21 | par_001 (The Robinier of Square Re | not worth it | - | no acct | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | report | could not reach it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | worth it | - | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | not worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-24 | Baarn | tree sent in | 4 chars, read it in the database | d4e6 | open_question |
| 08-25 | utr_005 (Onder de Linden) | vote undone | not worth it | d4e6 | - |
| 08-26 | sar_003 (The Olivastro of Santa Ma | worth it | - | d4e6 | - |
| 08-27 | ams_001 | worth it | - | 46c1 | holds |
| 08-27 | Baarn | tree sent in | 4 chars, read it in the database | d4e6 | holds |
| 08-28 | - | Super | - | d4e6 | - |
| 08-29 | Baarn | tree sent in | 4 chars, read it in the database | d4e6 | holds |
| 08-29 | Baarn | tree sent in | - | d4e6 | holds |
| 08-30 | rom_002 (Adonis) | worth it | - | d4e6 | - |
| 08-30 | rom_002 (Adonis) | vote undone | worth it | d4e6 | - |
| 08-30 | rom_002 (Adonis) | not worth it | - | d4e6 | - |
| 08-30 | rom_002 (Adonis) | vote undone | not worth it | d4e6 | - |
| 08-30 | rom_002 (Adonis) | worth it | - | d4e6 | - |
| 08-30 | rom_002 (Adonis) | vote undone | worth it | d4e6 | - |
| 08-30 | rom_002 (Adonis) | not worth it | - | d4e6 | - |
| 08-30 | rom_002 (Adonis) | vote undone | not worth it | d4e6 | - |
| 08-30 | rom_002 (Adonis) | worth it | - | d4e6 | - |
| 08-30 | London Plane | tree sent in | 71 chars, read it in the database | 21dc | holds |
| 08-31 | Amsterdam | tree sent in | - | d4e6 | open_question |
| 08-31 | Baarn | tree sent in | - | d4e6 | open_question |

- 44 of these 50 came from one account (d4e6). At this volume that is almost certainly our own testing rather than readers, and it should be read that way until somebody checks the rows.

**The funnel, as rates**
- Seen to clicked: 2.2% (295 of 13377) vs 2.5% the fortnight before
- Pages per visit: 1.7 (1390 visits, 2330 pageviews since 2026-08-08)
- Visits that did something: 10.9% (152 actions on 1390 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-22 | 17 | 1030 | 1.7% | 19.9 |
| 08-23 | 15 | 958 | 1.6% | 16.2 |
| 08-24 | 28 | 998 | 2.8% | 15.9 |
| 08-25 | 19 | 1108 | 1.7% | 20.1 |
| 08-26 | 24 | 1144 | 2.1% | 18.7 |
| 08-27 | 15 | 1003 | 1.5% | 18.8 |
| 08-28 | 27 | 1014 | 2.7% | 16.3 |
| 08-29 | 32 | 1068 | 3.0% | 17.6 |
| 08-30 | 32 | 1063 | 3.0% | 19.2 |
| 08-31 *partial* | 14 | 641 | 2.2% | 16.4 |
| **window** | **223** | **10027** | **2.2%** | |
- Top queries (10d): dutch elm amsterdam (i62, p5); ancient tree (i12, p34); ancient trees (i23, p21); e bordeaux? (i1, p1); italian trees in rome (i4, p10)
- Top pages (10d): / (c16/i137); /prague (c12/i129); /seville (c8/i150); /lisbon (c5/i191); /rome (c5/i413)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - '"oldest of its species" owl park' (i8, p8)
    - 'ahuehuete tree' (i4, p14)
    - '"400 years old as of 2023" tree' (i1, p7)
    - '"oldest of its species" "park" tree' (i1, p10)
    - '10 feet tall trees' (i1, p58)
    - '400 year old tree' (i1, p7)
    - '800 year old tree' (i1, p10)
    - '99 yew trees' (i1, p58)
    - and 3 more

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| rome | 5 | 467 | 1.1% | 10.1 | 2.5% | trees in rome (i28, p12) |
| amsterdam | 11 | 406 | 2.7% | 8.7 | 3.2% | dutch elm amsterdam (i47, p4) |
| lisbon | 7 | 238 | 2.9% | 7.9 | 3.5% | oldest tree in lisbon (i7, p8) |
| tenerife | 2 | 195 | 1.0% | 9.1 | 3.0% | drago milenario (i13, p11) |
| brisbane | 6 | 187 | 3.2% | 16.4 | 1.1% | the big macadamia nut (i11, p65) |
| barcelona | 6 | 185 | 3.2% | 10.1 | 2.5% | barcelona trees (i8, p8) |
| singapore | 4 | 182 | 2.2% | 10.9 | 2.2% | oldest tree in singapore (i19, p10) |
| seville | 9 | 181 | 5.0% | 8.5 | 3.2% | a to? (i1, p1) |
| copenhagen | 5 | 175 | 2.9% | 10.5 | 2.3% | trees in copenhagen (i25, p17) |
| london | 2 | 164 | 1.2% | 24.6 | 0.6% | london trees (i2, p74) |
| milan | 0 | 160 | 0.0% | 9.0 | 3.0% | "oldest of its species" owl park (i8, p8) |
| malaga | 3 | 152 | 2.0% | 13.8 | 1.4% | árboles históricos de málaga (i15, p80) |
| vienna | 3 | 144 | 2.1% | 9.8 | 2.6% | alter (i1, p3) |
| prague | 12 | 141 | 8.5% | 8.3 | 3.4% | - |
| bath | 2 | 131 | 1.5% | 7.6 | 3.7% | giant plane tree bath (i6, p11) |
| paris | 1 | 121 | 0.8% | 20.1 | 0.8% | trees in paris france (i4, p52) |
| florence | 2 | 120 | 1.7% | 8.6 | 3.2% | florence trees (i4, p5) |
| naples | 1 | 116 | 0.9% | 10.3 | 2.4% | naples tree (i4, p6) |
| crete | 0 | 110 | 0.0% | 9.5 | 2.8% | kavousi olive tree (i2, p10) |
| madeira | 2 | 105 | 1.9% | 8.8 | 3.1% | dragon tree madeira (i9, p10) |
| seoul | 0 | 97 | 0.0% | 14.3 | 1.3% | seoul trees (i4, p8) |
| toronto | 1 | 95 | 1.1% | 8.3 | 3.3% | oldest tree in toronto (i14, p9) |
| brussels | 1 | 94 | 1.1% | 11.2 | 2.1% | belgium trees (i2, p10) |
| palma-de-mallorca | 0 | 92 | 0.0% | 7.1 | 4.0% | oldest olive tree in palma (i2, p10) |
| fukuoka | 3 | 91 | 3.3% | 12.1 | 1.8% | couple camphor trees (i3, p9) |
| palermo | 1 | 89 | 1.1% | 7.1 | 3.9% | ficus macrophylla palermo (i1, p11) |
| venice | 0 | 89 | 0.0% | 6.3 | 4.7% | trees in venice (i3, p8) |
| madrid | 1 | 88 | 1.1% | 14.8 | 1.2% | oldest tree in madrid (i3, p9) |
| new-york | 1 | 87 | 1.1% | 17.4 | 1.0% | - |
| edinburgh | 3 | 82 | 3.7% | 16.2 | 1.1% | oldest tree in edinburgh (i2, p10) |
| las-vegas | 0 | 78 | 0.0% | 23.5 | 0.7% | vegas trees (i48, p32) |
| bologna | 0 | 75 | 0.0% | 7.5 | 3.8% | - |
| sardinia | 0 | 75 | 0.0% | 8.0 | 3.5% | baltolu sardinia (i12, p7) |
| dublin | 3 | 74 | 4.1% | 13.1 | 1.6% | hybrid strawberry tree (i1, p10) |
| alicante | 0 | 71 | 0.0% | 7.8 | 3.6% | how old (i1, p3) |
| valencia | 2 | 70 | 2.9% | 8.1 | 3.5% | ficus centenarios de la glorieta (i1, p12) |
| kyoto | 1 | 60 | 1.7% | 11.3 | 2.0% | japanese camphor (i1, p84) |
| montreal | 3 | 59 | 5.1% | 8.5 | 3.3% | mckenna grave height (i1, p5) |
| krakow | 1 | 56 | 1.8% | 13.3 | 1.5% | bednarski park (i1, p9) |
| hilo | 0 | 56 | 0.0% | 60.4 | 0.4% | loulu palm (i37, p78) |
| sydney | 0 | 56 | 0.0% | 7.3 | 3.8% | the wishing tree sydney (i7, p10) |
| mexico-city | 2 | 55 | 3.6% | 10.4 | 2.4% | ahuehuete mexico city (i2, p9) |
| cyprus | 2 | 54 | 3.7% | 7.2 | 3.9% | oldest tree in cyprus (i5, p10) |
| seattle | 4 | 53 | 7.5% | 6.3 | 4.7% | oldest tree in seattle (i2, p8) |
| istanbul | 2 | 53 | 3.8% | 6.6 | 4.4% | a ten ile ma (i1, p2) |
| nijmegen | 0 | 53 | 0.0% | 7.6 | 3.7% | brakkenstein nijmegen maps (i3, p11) |
| perth | 0 | 53 | 0.0% | 11.9 | 1.8% | jarrah tree bark (i2, p50) |
| athens | 1 | 52 | 1.9% | 13.1 | 1.6% | amritara olive trotter (i1, p84) |
| portland | 1 | 52 | 1.9% | 12.3 | 1.7% | - |
| chicago | 4 | 50 | 8.0% | 11.1 | 2.1% | wooded grove (i1, p48) |
| munich | 1 | 50 | 2.0% | 10.0 | 2.5% | the hornbeam centre (i1, p59) |
| reykjavik | 0 | 49 | 0.0% | 20.7 | 0.8% | iceland tree (i2, p61) |
| greece | 1 | 47 | 2.1% | 31.0 | 0.4% | greek trees (i6, p37) |
| berlin | 0 | 46 | 0.0% | 10.9 | 2.2% | berlin trees (i2, p50) |
| leiden | 0 | 46 | 0.0% | 12.8 | 1.6% | "oldest of its species" ginkgo park (i9, p8) |
| bordeaux | 3 | 43 | 7.0% | 7.6 | 3.7% | e bordeaux? (i1, p1) |
| vilnius | 0 | 43 | 0.0% | 8.1 | 3.4% | willow tree in lithuanian (i3, p9) |
| sintra | 2 | 38 | 5.3% | 6.0 | 5.1% | - |
| utrecht | 1 | 38 | 2.6% | 9.1 | 3.0% | zocher utrecht (i2, p22) |
| budapest | 1 | 37 | 2.7% | 6.8 | 4.2% | - |
| porto | 3 | 34 | 8.8% | 9.4 | 2.8% | alameda dos platanos (i4, p7) |
| cagliari | 0 | 34 | 0.0% | 4.3 | 7.7% | età (i1, p2) |
| the-hague | 1 | 33 | 3.0% | 8.6 | 3.2% | arentsburg (i1, p7) |
| geneva | 2 | 32 | 6.2% | 9.1 | 3.0% | - |
| boston | 2 | 32 | 6.2% | 20.2 | 0.8% | boston hill trees (i1, p19) |
| groningen | 1 | 32 | 3.1% | 13.1 | 1.6% | oak groningen (i1, p7) |
| new-orleans | 1 | 32 | 3.1% | 23.7 | 0.7% | anseman oak (i3, p9) |
| tokyo | 1 | 32 | 3.1% | 7.2 | 3.9% | - |
| cadiz | 0 | 31 | 0.0% | 7.0 | 4.0% | cadiz botanical gardens (i1, p2) |
| melbourne | 7 | 29 | 24.1% | 8.8 | 3.1% | - |
| quebec-city | 1 | 29 | 3.4% | 6.7 | 4.3% | - |
| glasgow | 0 | 27 | 0.0% | 9.2 | 2.9% | - |
| bristol | 2 | 26 | 7.7% | 10.5 | 2.3% | domesday oak (i1, p8) |
| sorrento | 1 | 26 | 3.8% | 17.2 | 1.0% | - |
| cambridge | 0 | 26 | 0.0% | 20.2 | 0.8% | newton's apple tree (i2, p47) |
| helsinki | 0 | 26 | 0.0% | 4.8 | 7.2% | in helsinki (i1, p4) |
| oahu | 1 | 25 | 4.0% | 6.4 | 4.6% | - |
| oslo | 2 | 25 | 8.0% | 8.2 | 3.4% | "oldest ginkgo tree" park motto (i1, p5) |
| strasbourg | 2 | 25 | 8.0% | 8.1 | 3.5% | - |
| aarhus | 0 | 24 | 0.0% | 8.0 | 3.5% | happy pig (i2, p10) |
| oxford | 2 | 23 | 8.7% | 8.1 | 3.4% | - |
| maastricht | 1 | 23 | 4.3% | 8.5 | 3.2% | tulip maastricht (i1, p20) |
| nara | 1 | 23 | 4.3% | 9.3 | 2.8% | - |
| washington-dc | 1 | 23 | 4.3% | 22.8 | 0.7% | survey lodge ranger station (i2, p12) |
| eindhoven | 0 | 23 | 0.0% | 11.9 | 1.8% | beukenboom (i1, p3) |
| guimaraes | 0 | 23 | 0.0% | 11.0 | 2.2% | pine tree portugal (i5, p18) |
| potsdam | 0 | 23 | 0.0% | 14.5 | 1.3% | glienicker park (i1, p63) |
| lyon | 1 | 22 | 4.5% | 6.4 | 4.6% | antoine rivoire (i2, p8) |
| arnhem | 0 | 22 | 0.0% | 8.4 | 3.3% | musispark arnhem (i1, p4) |
| hong-kong | 0 | 22 | 0.0% | 7.2 | 3.9% | - |
| trieste | 0 | 22 | 0.0% | 10.3 | 2.4% | piazza hortis (i3, p10) |
| cordoba | 0 | 20 | 0.0% | 32.2 | 0.4% | ginkgo location (i1, p63) |
| dubrovnik | 0 | 20 | 0.0% | 9.9 | 2.5% | - |
| nuremberg | 0 | 20 | 0.0% | 7.0 | 4.0% | kontumazgarten (i1, p11) |
| york | 1 | 19 | 5.3% | 8.5 | 3.3% | - |
| austin | 0 | 19 | 0.0% | 12.4 | 1.7% | antebellum oaks (i1, p54) |
| dallas | 0 | 18 | 0.0% | 8.7 | 3.1% | centennial tree (i3, p12) |
| cork | 1 | 17 | 5.9% | 8.7 | 3.1% | oldest tree in ireland (i4, p12) |
| graz | 1 | 17 | 5.9% | 9.9 | 2.6% | oak (i2, p8) |
| bratislava | 2 | 16 | 12.5% | 6.6 | 4.4% | - |
| bilbao | 1 | 16 | 6.2% | 6.0 | 5.0% | - |
| delft | 2 | 16 | 12.5% | 17.8 | 1.0% | - |
| bangkok | 0 | 16 | 0.0% | 10.7 | 2.3% | - |
| warsaw | 2 | 15 | 13.3% | 7.3 | 3.9% | - |
| braga | 1 | 15 | 6.7% | 7.6 | 3.7% | santa tecla braga (i1, p1) |
| houston | 1 | 14 | 7.1% | 54.9 | 0.4% | trees in houston texas (i3, p67) |
| poznan | 1 | 13 | 7.7% | 9.7 | 2.7% | - |
| australia | 0 | 13 | 0.0% | 18.2 | 0.9% | oldest tree in australia (i2, p50) |
| brno | 0 | 13 | 0.0% | 4.8 | 7.2% | - |
| catania | 0 | 13 | 0.0% | 6.2 | 4.8% | - |
| emmen | 0 | 13 | 0.0% | 6.3 | 4.7% | rensenpark emmen former zoo park (i1, p6) |
| nice | 0 | 13 | 0.0% | 5.8 | 5.3% | promenade des anglais palm trees (i1, p5) |
| tallinn | 0 | 13 | 0.0% | 6.2 | 4.8% | - |
| verona | 0 | 13 | 0.0% | 7.0 | 4.0% | - |
| belgrade | 1 | 12 | 8.3% | 12.2 | 1.8% | - |
| frankfurt | 0 | 12 | 0.0% | 6.0 | 5.0% | what tree is this (i1, p6) |
| hobart | 0 | 12 | 0.0% | 14.2 | 1.4% | - |
| osaka | 0 | 12 | 0.0% | 10.5 | 2.3% | - |
| rotterdam | 0 | 12 | 0.0% | 8.1 | 3.5% | delftseplein (i2, p4) |
| turin | 0 | 12 | 0.0% | 5.3 | 6.3% | - |
| canada | 0 | 11 | 0.0% | 18.4 | 0.9% | oldest tree in canada (i2, p20) |
| caserta | 0 | 11 | 0.0% | 17.6 | 1.0% | - |
| granada | 1 | 10 | 10.0% | 5.2 | 6.6% | - |
| venlo | 0 | 10 | 0.0% | 13.0 | 1.6% | sequoia waterloo (i1, p74) |

**The language test** (Contract J v1.13: a translated set should pass its English twin's impressions within four weeks of indexing):

| Lang | City | Clicks | Impressions | Position | English twin |
|---|---|---:|---:|---:|---:|
| es | malaga | 0 | 105 | 12.9 | 152 |
| de | berlin | 0 | 81 | 21.8 | 46 |
| de | vienna | 2 | 55 | 9.3 | 144 |
| ja | kyoto | 2 | 53 | 10.7 | 60 |
| pt | lisbon | 3 | 46 | 10.0 | 238 |
| it | rome | 3 | 41 | 10.0 | 467 |
| pt | porto | 1 | 40 | 6.5 | 34 |
| ja | tokyo | 0 | 37 | 10.6 | 32 |
| it | palermo | 0 | 34 | 8.6 | 89 |
| es | barcelona | 0 | 25 | 14.4 | 185 |
| es | cadiz | 1 | 22 | 16.0 | 31 |
| pt | sintra | 1 | 22 | 13.6 | 38 |
| es | madrid | 0 | 18 | 7.6 | 88 |
| nl | nijmegen | 0 | 17 | 7.9 | 53 |
| nl | amsterdam | 0 | 15 | 3.2 | 406 |
| es | tenerife | 0 | 14 | 32.2 | 195 |
| ja | osaka | 2 | 13 | 13.0 | 12 |
| it | milan | 0 | 13 | 13.4 | 160 |
| de | zurich | 1 | 12 | 9.3 | 8 |
| fr | geneva | 0 | 11 | 21.6 | 32 |
| fr | nice | 0 | 9 | 21.1 | 13 |

**Cities seen but never clicked** (60+ impressions, zero clicks, with what they are actually shown for):

- tenerife (i70): drago milenario (i13, p11); pino gordo tenerife (i8, p10); pino gordo (i8, p21); el drago milenario (i7, p10)
- Seen, not clicked: /rome (c1/i154, 0.6%) for trees in rome (i28, p12); rome trees (i25, p11); oldest tree in rome (i14, p6)
- Seen, not clicked: /species/strawberry-tree (c0/i89, 0.0%) for strawberry tree (i21, p69); arbutus strawberry tree (i10, p61); strawberry tree plant (i4, p72)
- Seen, not clicked: /species/osage-orange (c0/i70, 0.0%) for osage orange (i12, p85); osage orange tree (i3, p84); osage orange fruit (i3, p85)
- Seen, not clicked: /las-vegas (c0/i48, 0.0%) for vegas trees (i48, p32)
- Seen, not clicked: / (c1/i43, 2.3%) for ancient trees (i22, p24); ancient tree (i10, p46); ancient tree map (i3, p17)
- Seen, not clicked: /tenerife/el-drago-milenario (c0/i42, 0.0%) for drago milenario (i13, p11); el drago milenario (i7, p10); oldest tree tenerife (i4, p12)
- Seen, not clicked: /hilo/loulu-palm-of-kalakaua-park (c0/i41, 0.0%) for loulu palm (i37, p78); loulu palm tree (i2, p52); loulu tree (i1, p47)
- Seen, not clicked: /copenhagen (c0/i33, 0.0%) for trees in copenhagen (i25, p17); copenhagen trees (i7, p15); trees in denmark (i1, p38)

**Climbing** (this ten days against the ten before it)

| Page | Impressions | Change | Position | Moved | Clicks |
|---|---:|---:|---:|---:|---:|
| /rome | 413 | +230 | 10.5 | +4.7 | +4 |
| /seville | 150 | +133 | 8.8 | +10.3 | +7 |
| /species/strawberry-tree | 113 | +96 | 66.5 | -4.2 | +0 |
| /species/osage-orange | 117 | +95 | 82.5 | -6.1 | +0 |
| / | 137 | +80 | 15.8 | +2.1 | +7 |
| /lisbon | 191 | +70 | 7.4 | +2.1 | +1 |
| /copenhagen | 141 | +62 | 11.3 | +1.6 | +2 |
| /malaga | 139 | +60 | 14.6 | -0.5 | +2 |

**Newly ranking** (no impressions at all ten days ago)

| Page | Impressions | Clicks | Position |
|---|---:|---:|---:|
| /amsterdam/elm-of-elsenhoeve | 107 | 4 | 6.2 |
| /species/austrian-pine | 36 | 0 | 80.7 |
| /sydney/wishing-tree | 34 | 0 | 8.4 |
| /de/berlin/kaisereiche | 27 | 0 | 15.7 |
| /collections/tallest-trees | 27 | 0 | 34.9 |
| /perth/oldest-tree | 25 | 0 | 9.2 |

**Slipping**

| Page | Impressions | Change | Position | Moved |
|---|---:|---:|---:|---:|
| /prague | 129 | -26 | 7.9 | -0.5 |
| /madrid | 69 | -15 | 16.2 | -2.9 |
| /es/malaga/ficus-avenue-of-the-alameda-principal | 32 | -9 | 6.9 | -1.6 |
| /singapore/tembusu-of-lawn-e | 20 | -6 | 9.1 | -0.7 |

- New queries this window: italian trees in rome (i4).

**Who they are**
Audience, 28 days of search (433 clicks, 19057 impressions):
- Countries: usa c78/i4184; gbr c48/i2218; nld c28/i917; aus c24/i649; esp c20/i1146
- Devices: MOBILE c297/i10394; DESKTOP c131/i8493; TABLET c5/i170
- Landing pages: / c29/i217; /prague c23/i323; /lisbon c11/i353; /seville c10/i190; /amsterdam c7/i398

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-24 | 10 | 20 |
| 08-25 | 60 | 70 |
| 08-26 | 80 | 110 |
| 08-27 | 60 | 140 |
| 08-28 | 120 | 170 |
| 08-29 | 60 | 140 |
| 08-30 | 70 | 180 |
| 08-31 | 30 | 90 |
| **window** | **490** | **920** |
- Top paths: / (100); /explore (60); /melbourne/remnant-river-red-gum-of-edinburgh-gardens (30); /nijmegen/wilhelminaboom-of-hertogplein (30); /prague (30); /brisbane/hoop-pine (20); /melbourne (20); /brussels (20); /sponsor (20); /paris/robinier-of-square-rene-viviani (10); /australia (10); /brisbane/bodhi-tree (10)
- Referrers: ancienttrees.app (430); (direct) (280); www.google.com (210)
- Moved between our own pages: 430 of 920 pageviews (47%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: AU (160); US (160); ES (90); NL (90); GB (90)
- Devices: desktop (460); mobile (440); tablet (20)
- Page load (8d): p50 735ms, p90 2714ms

Links: external referrers (a link somebody actually clicked): none yet
AI: arrivals from an assistant that cited us: none yet


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 08-31T10:14 | 26.8 | 3 | 9 | 24 | Graz +2, Philadelphia +1 |
| 08-31T18:23 | 101.4 | 61 | 39 | 42 | Girona +7, Kamakura +6, Nagoya +6, Naha +6, +10 more |
| 08-31T23:29 | 71.8 | 4 | 18 | 55 | Warsaw +2, Turin +1, Vilnius +1 |
| 09-01T02:31 | 61.2 | 7 | 12 | 35 | Delft +4, Kagoshima +1, Naples +1, Valencia +1 |
| **4 runs** | **261** | **75** | **78** | | |

- 24 to 55 commands refused per run; 1 wrote nothing to LOG.md.

**What they made**

- photo_hunt.py --recheck: partial sweep progress (free API sweep, no tokens)
- Naples +1: the disputed-species Nolina/Beaucarnea, publish-and-ask per policy
- Delft +4: finish the standing delft verify claim, a Kalverbos/Nieuwe Plantage cluster
- Kagoshima +1, Valencia +1: finish the standing write-pass-batch claim, and fix leads.py --ready's real gap
- Fix iOS 18 floor job: unbooted device race, sign-in DRIFT, RefusedWalk flake
- Cagliari deepen pass: honest zero, two new remote clusters banked as leads
- Photo queue: sweep ~280 more photo-less trees for open-licence candidates
- Vilnius +1, Warsaw +1: finish standing verify claims (actually merged this time)
- Vilnius +1, Warsaw +1: finish standing verify claims
- Keep the Turin and Warsaw verify-pass delivery files as a record
- Turin +1: The Downy Oak of the Colle della Maddalena (tor_011)
- Warsaw +1: The Chestnut of Pulawska and Merliniego (war_018)
- Write 4 species intros the data had earned: Spanish Fir, Katsura, Buddhist Pine, Bishop Wood
- Refill: genus from name for one Vilnius lead

Machine: 4 chain attempts yesterday, 4 got real work time (~278 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 14 clicks and 641 impressions on Google's freshest day (day before: c32/i1063). Directional at best; no strategic conclusions from these volumes.

## Weekly analysis 2026-08-31

Sixth weekly analysis, comparing the 10-day Search Console window ending
2026-08-30 against the one ending 2026-08-23 (both read from the daily
entries directly, so both are apples-to-apples "last 10 days Google will
give us" snapshots one week apart), plus the beacon's own 8-day windows for
the same two boundaries.

**Scorecard**

| Week ending | Impressions | Clicks | CTR | Avg position | Visits (beacon, 8d) | Pageviews (beacon, 8d) | Directions (14d) | App-CTA (14d) | Waitlist total | Submissions total |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-08-23 | 7,666 | 165 | 2.2% | 16.4 | 530 | 840 | n/a (table format didn't exist yet) | n/a | 10 | 20 |
| 2026-08-30 | 9,870 (still settling) | 212 (still settling) | 2.1% | 17.9 | 530 | 950 | 24 | 44 | 15 | 33 |

**What moved:**
1. Impressions rose 7,666 to 9,870 week over week (+29%, and the newest
   day is still backfilling upward the way 08-22 and 08-24 did before it),
   clicks rose 165 to 212 (+28%). CTR held essentially flat, 2.2% to 2.1%.
   Today is GO_TO_MARKET.md's own "review at the end of August 2026"
   checkpoint, and its stated healthy bar is exactly this: impressions and
   clicks growing week over week into the tens.
2. Beacon visits held EXACTLY flat at 530 across both 8-day windows
   (08-16 to 08-23 and 08-23 to 08-30) while pageviews rose 840 to 950
   (+13%, pages/visit 1.58 to 1.79). Search impressions climbing 29% did
   not turn into more visits this window, only into more pages seen per
   visit that did arrive.
3. Milan (0%, 199 impressions) and Madrid (0%, 94 impressions) are still
   stuck at 0% CTR, the third straight weekly analysis naming both. Vienna,
   flagged alongside them on 08-28, recovered to 2.1% CTR (146 to 142
   impressions) on its own; nothing in LOG.md shows the title/meta
   diagnostic that fixed Rome and Malaga was ever actually run against
   Milan or Madrid.
4. Porto's 'alameda dos platanos' content gap, flagged in three straight
   prior windows, is gone from this week's leads list: the 08-26 merge of
   its two duplicate plane-avenue pages (por_026/por_028) took, just slower
   than expected.
5. Reader-submitted trees rose from 0 to 5 this week (waitlist, accounts
   and saves all held exactly flat at 4/1/6 both weeks); feedback fell 19
   to 8, but last week's 19 included the d4e6 test-account voting spike
   already flagged as internal testing, so 8 is closer to the real reader
   rate.

**Suggestions, ranked:**
1. **[FOR HIDDE]** GO_TO_MARKET.md's Phase 0 checkpoint is dated today. By
   its own written bar (impressions and clicks growing week over week into
   the tens), this week clears it cleanly: +29% impressions, +28% clicks,
   both up from a smaller base the week before too. This is the second
   weekly analysis to surface this exact date (the first was 08-28, before
   the checkpoint had technically arrived); worth a conscious decision
   today per the document's own reasoning, rather than the date passing
   unremarked a second time.
2. **[run]** Milan and Madrid have now sat at 0% CTR through three weekly
   analyses running, both with real impressions (94-199) at rankable
   positions (8.5, 16.0). The Rome/Malaga fix (check P2 answer-first
   wording and the title/meta against the actual query) was suggested for
   both on 08-28 and neither shows any sign of having been touched since.
3. **[sessie]** Beacon visits flat at 530 for two consecutive 8-day windows
   despite impressions up 29% is worth a direct look: either it is
   dilution from pages that rank but don't convert (consistent with the
   Milan/Madrid finding above), or something in the beacon pipeline itself
   has plateaued independent of traffic. Worth knowing which before reading
   more into either number.
4. **[run]** Tenerife's city page still converts at 0.9% (228 impressions,
   biggest query 'drago milenario' at position 11) and its own tree page
   /el-drago-milenario, flagged 08-28 as newly-ranking-but-0%-CTR, has not
   moved. It carries the bulk of Tenerife's search volume, so a title/meta
   look there specifically is worth more than one at the city level.

**Watch next week:** whether Milan and Madrid's CTR responds to an actual
title/meta pass this time, whether the 530-visit beacon plateau breaks now
that pageviews have started moving, and what Hidde decides at the
Phase 0 checkpoint.

## 2026-08-30 (previous UTC day)

**Today: a waitlist arrived today (15 total); 1 tree submission and 5 feedback reports arrived yesterday (33 total); an account was opened yesterday (5 total).**

**Did the product happen**

| Action | Yesterday | 14 days | Ever | Last |
|---|---:|---:|---:|---|
| app-cta | 4 | 44 | 44 | today |
| search-home | 14 | 28 | 28 | today |
| directions | 10 | 24 | 24 | yesterday |
| save | 5 | 12 | 12 | yesterday |
| waitlist-submit | 0 | 10 | 10 | today |
| search-explore | 1 | 6 | 6 | today |
| walks-app | 1 | 6 | 6 | yesterday |
| suggestion-submit | 1 | 4 | 4 | yesterday |
| walk-open | 0 | 3 | 4 | 14 days ago |
| smoke-test | 0 | 0 | 2 | 30 days ago |
| beacon-fix-verify | 0 | 0 | 1 | 15 days ago |
| beacon-test | 0 | 0 | 1 | 15 days ago |
| worthit-not worth it | 0 | 1 | 1 | 14 days ago |
| signin-link-sent | 0 | 0 | 0 | never |
| walk-start | 0 | 0 | 0 | never |
| worthit-worth it | 0 | 0 | 0 | never |
| **all** | **36** | **138** | **143** | |
- 'Ever' counts every row in the events table, which begins 2026-08-01 when the funnel was repaired. Anything named here with a zero has never fired at all.

**What people typed into our search** (14 days, 28 searches, 19 different terms)

| Typed | Times |
|---|---:|
| mel | 6 |
| melb | 3 |
| melbourne | 3 |
| berli | 1 |
| boston | 1 |
| copenhagen | 1 |
| ei | 1 |
| glasg | 1 |
| leiden | 1 |
| london | 1 |
| melbo | 1 |
| milano | 1 |
| oslo | 1 |
| portland | 1 |
| prague | 1 |
| sea | 1 |
| sofia | 1 |
| sy | 1 |
| war | 1 |

| Day | Accounts | Waitlist | Saves | Trees sent | Feedback |
|---|---:|---:|---:|---:|---:|
| 08-17 | 0 | 1 | 0 | 0 | 2 |
| 08-18 | 0 | 1 | 2 | 0 | 0 |
| 08-19 | 0 | 1 | 0 | 0 | 0 |
| 08-20 | 0 | 1 | 3 | 0 | 1 |
| 08-21 | 1 | 0 | 0 | 0 | 16 |
| 08-22 | 0 | 0 | 1 | 0 | 0 |
| 08-23 | 0 | 0 | 0 | 0 | 0 |
| 08-24 | 0 | 0 | 0 | 1 | 0 |
| 08-25 | 0 | 1 | 0 | 0 | 0 |
| 08-26 | 0 | 1 | 1 | 0 | 1 |
| 08-27 | 0 | 1 | 0 | 1 | 1 |
| 08-28 | 0 | 1 | 0 | 0 | 1 |
| 08-29 | 0 | 0 | 0 | 2 | 0 |
| 08-30 | 1 | 0 | 5 | 1 | 5 |
| 08-31 | 0 | 1 | 0 | 0 | 0 |
| **14 days** | **2** | **9** | **12** | **5** | **27** |
- Waitlist:    15 total, newest today
- Submissions: 33 total (5 trees sent, 28 feedback), newest yesterday
- Accounts:    5 total, newest yesterday

**What readers told us** (14 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 08-17 | hel_006 (The Meilahti Ancient Pine | not worth it | - | no acct | holds |
| 08-17 | lis_005 (The Tipu of Jardim de São | worth it | - | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-21 | par_001 (The Robinier of Square Re | not worth it | - | no acct | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | report | could not reach it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | worth it | - | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | not worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-24 | Baarn | tree sent in | 4 chars, read it in the database | d4e6 | open_question |
| 08-25 | utr_005 (Onder de Linden) | vote undone | not worth it | d4e6 | - |
| 08-26 | sar_003 (The Olivastro of Santa Ma | worth it | - | d4e6 | - |
| 08-27 | ams_001 | worth it | - | 46c1 | holds |
| 08-27 | Baarn | tree sent in | 4 chars, read it in the database | d4e6 | holds |
| 08-28 | - | Super | - | d4e6 | - |
| 08-29 | Baarn | tree sent in | 4 chars, read it in the database | d4e6 | holds |
| 08-29 | Baarn | tree sent in | - | d4e6 | holds |
| 08-30 | rom_002 (Adonis) | worth it | - | d4e6 | - |
| 08-30 | rom_002 (Adonis) | vote undone | worth it | d4e6 | - |
| 08-30 | rom_002 (Adonis) | not worth it | - | d4e6 | - |
| 08-30 | rom_002 (Adonis) | vote undone | not worth it | d4e6 | - |
| 08-30 | rom_002 (Adonis) | worth it | - | d4e6 | - |
| 08-30 | rom_002 (Adonis) | vote undone | worth it | d4e6 | - |
| 08-30 | rom_002 (Adonis) | not worth it | - | d4e6 | - |
| 08-30 | rom_002 (Adonis) | vote undone | not worth it | d4e6 | - |
| 08-30 | rom_002 (Adonis) | worth it | - | d4e6 | - |
| 08-30 | London Plane | tree sent in | 71 chars, read it in the database | 21dc | holds |

- 42 of these 50 came from one account (d4e6). At this volume that is almost certainly our own testing rather than readers, and it should be read that way until somebody checks the rows.

**The funnel, as rates**
- Seen to clicked: 2.2% (281 of 12913) vs 2.4% the fortnight before
- Pages per visit: 1.6 (1360 visits, 2240 pageviews since 2026-08-08)
- Visits that did something: 10.4% (141 actions on 1360 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-21 | 18 | 913 | 2.0% | 19.9 |
| 08-22 | 17 | 1030 | 1.7% | 19.9 |
| 08-23 | 15 | 958 | 1.6% | 16.2 |
| 08-24 | 28 | 998 | 2.8% | 15.9 |
| 08-25 | 19 | 1108 | 1.7% | 20.1 |
| 08-26 | 24 | 1144 | 2.1% | 18.7 |
| 08-27 | 15 | 1003 | 1.5% | 18.8 |
| 08-28 | 27 | 1014 | 2.7% | 16.3 |
| 08-29 | 32 | 1068 | 3.0% | 17.6 |
| 08-30 *partial* | 17 | 634 | 2.7% | 15.7 |
| **window** | **212** | **9870** | **2.1%** | |
- Top queries (10d): dutch elm amsterdam (i58, p5); ancient tree (i15, p40); ancient trees (i21, p23); e bordeaux? (i1, p1); italian trees in rome (i4, p10)
- Top pages (10d): / (c13/i129); /prague (c13/i139); /seville (c6/i141); /lisbon (c5/i179); /amsterdam/elm-of-elsenhoeve (c4/i90)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - '"oldest of its species" owl park' (i9, p8)
    - 'ahuehuete tree' (i4, p14)
    - '"400 years old as of 2023" tree' (i1, p7)
    - '"oldest of its species" "park" tree' (i1, p10)
    - '10 feet tall trees' (i1, p58)
    - '800 year old tree' (i1, p10)
    - '99 yew trees' (i1, p58)
    - 'a izvan hrvatske' (i1, p4)
    - and 3 more

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| rome | 4 | 431 | 0.9% | 10.0 | 2.5% | trees in rome (i24, p11) |
| amsterdam | 11 | 392 | 2.8% | 9.0 | 3.0% | dutch elm amsterdam (i42, p4) |
| tenerife | 2 | 228 | 0.9% | 9.5 | 2.8% | drago milenario (i18, p11) |
| lisbon | 7 | 225 | 3.1% | 7.6 | 3.7% | oldest tree in lisbon (i7, p8) |
| milan | 0 | 199 | 0.0% | 8.5 | 3.2% | "oldest of its species" ginkgo park (i9, p6) |
| copenhagen | 6 | 188 | 3.2% | 10.8 | 2.2% | trees in copenhagen (i28, p17) |
| brisbane | 6 | 187 | 3.2% | 16.8 | 1.1% | the big macadamia nut (i10, p65) |
| singapore | 4 | 179 | 2.2% | 11.1 | 2.1% | oldest tree in singapore (i18, p10) |
| barcelona | 6 | 176 | 3.4% | 10.0 | 2.5% | barcelona trees (i8, p8) |
| seville | 7 | 173 | 4.0% | 10.1 | 2.5% | a to? (i1, p1) |
| prague | 13 | 154 | 8.4% | 7.6 | 3.7% | - |
| malaga | 3 | 152 | 2.0% | 13.5 | 1.5% | árboles históricos de málaga (i13, p80) |
| bath | 2 | 146 | 1.4% | 7.7 | 3.6% | the giant plane tree bath (i7, p11) |
| london | 2 | 146 | 1.4% | 25.8 | 0.6% | trees in london (i2, p70) |
| vienna | 3 | 142 | 2.1% | 9.8 | 2.6% | alter (i1, p3) |
| paris | 1 | 139 | 0.7% | 19.8 | 0.8% | trees in paris france (i3, p55) |
| florence | 2 | 121 | 1.7% | 9.3 | 2.8% | florence trees (i5, p5) |
| crete | 0 | 118 | 0.0% | 9.4 | 2.8% | 2000 years old olive tree (i2, p13) |
| naples | 1 | 109 | 0.9% | 10.5 | 2.3% | naples tree (i2, p5) |
| madeira | 2 | 105 | 1.9% | 8.6 | 3.2% | dragon tree madeira (i7, p10) |
| seoul | 0 | 100 | 0.0% | 13.7 | 1.5% | seoul trees (i4, p8) |
| palermo | 1 | 95 | 1.1% | 7.1 | 3.9% | oldest tree in palermo (i2, p12) |
| madrid | 0 | 94 | 0.0% | 16.0 | 1.1% | oldest tree in madrid (i3, p9) |
| palma-de-mallorca | 0 | 92 | 0.0% | 7.0 | 4.0% | oldest olive tree in palma (i2, p10) |
| venice | 0 | 90 | 0.0% | 6.2 | 4.8% | trees in venice (i2, p10) |
| fukuoka | 3 | 86 | 3.5% | 11.9 | 1.8% | kanatake (i2, p76) |
| brussels | 1 | 82 | 1.2% | 11.5 | 2.0% | belgian trees (i1, p36) |
| edinburgh | 3 | 81 | 3.7% | 15.7 | 1.1% | oldest tree in edinburgh (i2, p10) |
| toronto | 1 | 79 | 1.3% | 8.3 | 3.4% | oldest tree in toronto (i12, p9) |
| las-vegas | 0 | 78 | 0.0% | 24.0 | 0.6% | vegas trees (i49, p33) |
| valencia | 2 | 77 | 2.6% | 8.7 | 3.1% | ficus centenarios de la glorieta (i2, p11) |
| sardinia | 0 | 76 | 0.0% | 7.7 | 3.7% | baltolu sardinia (i12, p7) |
| dublin | 2 | 73 | 2.7% | 13.4 | 1.5% | oldest tree in ireland (i1, p62) |
| new-york | 2 | 73 | 2.7% | 16.3 | 1.1% | - |
| montreal | 4 | 68 | 5.9% | 8.8 | 3.1% | century trees (i2, p58) |
| bologna | 0 | 65 | 0.0% | 7.6 | 3.7% | - |
| alicante | 0 | 61 | 0.0% | 7.1 | 3.9% | how old (i1, p3) |
| perth | 0 | 56 | 0.0% | 13.4 | 1.5% | jarra tree (i2, p38) |
| kyoto | 1 | 55 | 1.8% | 10.2 | 2.4% | japanese camphor (i1, p84) |
| hilo | 0 | 55 | 0.0% | 61.1 | 0.4% | loulu palm (i33, p82) |
| istanbul | 2 | 54 | 3.7% | 6.8 | 4.2% | a ten ile ma (i1, p2) |
| krakow | 2 | 54 | 3.7% | 9.1 | 3.0% | bednarski park (i1, p12) |
| mexico-city | 2 | 54 | 3.7% | 10.4 | 2.4% | ahuehuete mexico city (i2, p9) |
| portland | 1 | 52 | 1.9% | 10.9 | 2.2% | - |
| nijmegen | 0 | 52 | 0.0% | 6.8 | 4.2% | hertogplein nijmegen maps (i1, p6) |
| cyprus | 2 | 51 | 3.9% | 7.1 | 4.0% | oldest tree in cyprus (i5, p10) |
| sydney | 0 | 51 | 0.0% | 7.3 | 3.8% | the wishing tree sydney (i7, p10) |
| chicago | 4 | 48 | 8.3% | 11.2 | 2.1% | wooded grove (i1, p48) |
| greece | 1 | 48 | 2.1% | 32.9 | 0.4% | greek trees (i6, p37) |
| reykjavik | 0 | 48 | 0.0% | 21.0 | 0.8% | oldest tree in iceland (i3, p7) |
| bordeaux | 3 | 44 | 6.8% | 7.8 | 3.6% | sequoia bordeaux (i2, p9) |
| munich | 1 | 44 | 2.3% | 10.8 | 2.2% | the hornbeam centre (i1, p59) |
| athens | 1 | 43 | 2.3% | 13.8 | 1.4% | oldest olive tree in athens (i1, p1) |
| berlin | 0 | 42 | 0.0% | 9.6 | 2.7% | berlin tree map (i1, p10) |
| seattle | 2 | 41 | 4.9% | 6.4 | 4.6% | oldest tree in seattle (i1, p7) |
| leiden | 0 | 41 | 0.0% | 11.1 | 2.1% | "oldest of its species" ginkgo park (i7, p9) |
| budapest | 1 | 39 | 2.6% | 6.9 | 4.1% | - |
| the-hague | 1 | 39 | 2.6% | 8.5 | 3.2% | old tree (i1, p9) |
| tokyo | 0 | 37 | 0.0% | 6.6 | 4.4% | - |
| utrecht | 1 | 36 | 2.8% | 9.2 | 2.9% | zocher utrecht (i2, p22) |
| boston | 1 | 35 | 2.9% | 19.5 | 0.8% | boston hill trees (i1, p19) |
| porto | 3 | 34 | 8.8% | 8.9 | 3.0% | alameda dos platanos (i5, p7) |
| oslo | 2 | 33 | 6.1% | 10.8 | 2.2% | "oldest ginkgo tree" park motto (i1, p5) |
| sintra | 2 | 33 | 6.1% | 5.7 | 5.6% | - |
| cambridge | 0 | 33 | 0.0% | 27.3 | 0.5% | newton's apple tree (i3, p46) |
| strasbourg | 2 | 32 | 6.2% | 7.9 | 3.6% | - |
| vilnius | 0 | 32 | 0.0% | 7.7 | 3.7% | willow tree in lithuanian (i3, p9) |
| geneva | 2 | 31 | 6.5% | 9.2 | 2.9% | - |
| cagliari | 0 | 31 | 0.0% | 4.8 | 7.2% | età (i1, p2) |
| aarhus | 1 | 30 | 3.3% | 7.9 | 3.6% | happy pig (i2, p10) |
| new-orleans | 1 | 30 | 3.3% | 24.8 | 0.6% | anseman oak (i3, p9) |
| groningen | 1 | 29 | 3.4% | 13.2 | 1.6% | oak groningen (i1, p7) |
| cadiz | 0 | 29 | 0.0% | 7.5 | 3.7% | cadiz botanical gardens (i1, p2) |
| bristol | 2 | 28 | 7.1% | 15.6 | 1.2% | bristol trees (i1, p58) |
| washington-dc | 1 | 28 | 3.6% | 20.2 | 0.8% | survey lodge ranger station (i5, p11) |
| glasgow | 0 | 27 | 0.0% | 9.4 | 2.8% | - |
| guimaraes | 0 | 26 | 0.0% | 10.3 | 2.4% | pine tree portugal (i5, p18) |
| potsdam | 0 | 25 | 0.0% | 14.6 | 1.3% | glienicker park (i1, p63) |
| dubrovnik | 1 | 24 | 4.2% | 8.1 | 3.4% | - |
| helsinki | 0 | 24 | 0.0% | 4.9 | 7.1% | in helsinki (i1, p4) |
| quebec-city | 0 | 24 | 0.0% | 6.7 | 4.3% | - |
| sorrento | 1 | 23 | 4.3% | 18.5 | 0.9% | - |
| york | 1 | 23 | 4.3% | 8.2 | 3.4% | - |
| hong-kong | 0 | 23 | 0.0% | 7.0 | 4.0% | - |
| eindhoven | 0 | 22 | 0.0% | 9.7 | 2.7% | beukenboom (i1, p3) |
| oxford | 3 | 21 | 14.3% | 7.8 | 3.6% | - |
| nara | 1 | 20 | 5.0% | 11.0 | 2.1% | - |
| oahu | 1 | 20 | 5.0% | 6.8 | 4.2% | - |
| arnhem | 0 | 20 | 0.0% | 6.0 | 5.0% | musispark arnhem (i1, p4) |
| cordoba | 0 | 20 | 0.0% | 34.7 | 0.4% | ginkgo location (i1, p63) |
| nuremberg | 0 | 20 | 0.0% | 6.5 | 4.5% | - |
| lyon | 1 | 19 | 5.3% | 12.7 | 1.7% | antoine rivoire (i2, p8) |
| maastricht | 1 | 19 | 5.3% | 7.4 | 3.8% | - |
| melbourne | 3 | 19 | 15.8% | 8.6 | 3.2% | - |
| trieste | 0 | 19 | 0.0% | 9.3 | 2.8% | piazza hortis (i3, p10) |
| cork | 1 | 18 | 5.6% | 8.7 | 3.1% | oldest tree in ireland (i5, p14) |
| dallas | 1 | 18 | 5.6% | 7.7 | 3.7% | centennial tree (i2, p13) |
| austin | 0 | 17 | 0.0% | 12.9 | 1.6% | antebellum oaks (i1, p54) |
| bratislava | 2 | 16 | 12.5% | 6.2 | 4.8% | - |
| bangkok | 0 | 16 | 0.0% | 10.7 | 2.3% | - |
| warsaw | 2 | 15 | 13.3% | 10.5 | 2.3% | - |
| bilbao | 1 | 15 | 6.7% | 5.9 | 5.1% | - |
| braga | 1 | 15 | 6.7% | 7.6 | 3.7% | santa tecla braga (i1, p1) |
| padua | 0 | 15 | 0.0% | 6.8 | 4.2% | - |
| tallinn | 0 | 14 | 0.0% | 6.1 | 4.9% | - |
| turin | 0 | 14 | 0.0% | 4.9 | 7.1% | - |
| graz | 1 | 13 | 7.7% | 5.2 | 6.5% | oak (i1, p7) |
| houston | 1 | 13 | 7.7% | 55.2 | 0.4% | trees in houston texas (i3, p67) |
| australia | 0 | 13 | 0.0% | 18.5 | 0.9% | ancient trees in australia (i2, p18) |
| canada | 0 | 13 | 0.0% | 16.5 | 1.1% | oldest tree in quebec (i3, p9) |
| belgrade | 1 | 12 | 8.3% | 12.2 | 1.8% | - |
| catania | 0 | 12 | 0.0% | 6.2 | 4.8% | - |
| emmen | 0 | 12 | 0.0% | 5.9 | 5.2% | rensenpark emmen former zoo park (i1, p6) |
| nice | 0 | 12 | 0.0% | 5.4 | 6.2% | promenade des anglais palm trees (i1, p5) |
| delft | 2 | 11 | 18.2% | 23.1 | 0.7% | - |
| brno | 0 | 11 | 0.0% | 6.1 | 4.9% | - |
| frankfurt | 0 | 11 | 0.0% | 4.0 | 8.0% | what tree is this (i1, p6) |
| hobart | 0 | 11 | 0.0% | 11.1 | 2.1% | - |
| osaka | 0 | 11 | 0.0% | 11.3 | 2.1% | - |
| caserta | 0 | 10 | 0.0% | 18.5 | 0.9% | parchi caserta (i1, p1) |
| haarlem | 0 | 10 | 0.0% | 10.1 | 2.5% | - |
| ljubljana | 0 | 10 | 0.0% | 10.0 | 2.5% | - |
| rotterdam | 0 | 10 | 0.0% | 5.1 | 6.8% | delftseplein (i2, p4) |
| split | 0 | 10 | 0.0% | 9.7 | 2.7% | mediterranean cypress croatia (i2, p8) |
| venlo | 0 | 10 | 0.0% | 13.0 | 1.6% | sequoia waterloo (i1, p74) |
| verona | 0 | 10 | 0.0% | 6.8 | 4.2% | - |

**The language test** (Contract J v1.13: a translated set should pass its English twin's impressions within four weeks of indexing):

| Lang | City | Clicks | Impressions | Position | English twin |
|---|---|---:|---:|---:|---:|
| es | malaga | 1 | 114 | 12.7 | 152 |
| de | berlin | 0 | 76 | 22.0 | 42 |
| de | vienna | 1 | 49 | 9.6 | 142 |
| ja | kyoto | 1 | 49 | 10.3 | 55 |
| pt | lisbon | 3 | 41 | 10.6 | 225 |
| it | rome | 3 | 37 | 10.0 | 431 |
| pt | porto | 1 | 37 | 6.1 | 34 |
| ja | tokyo | 0 | 35 | 10.6 | 37 |
| it | palermo | 0 | 32 | 8.8 | 95 |
| pt | sintra | 1 | 20 | 13.9 | 33 |
| es | cadiz | 1 | 18 | 15.0 | 29 |
| es | barcelona | 0 | 18 | 15.9 | 176 |
| nl | nijmegen | 0 | 17 | 7.9 | 52 |
| es | madrid | 0 | 15 | 7.5 | 94 |
| it | milan | 0 | 12 | 13.3 | 199 |
| nl | amsterdam | 0 | 12 | 3.8 | 392 |
| es | tenerife | 0 | 11 | 31.4 | 228 |
| fr | geneva | 0 | 11 | 21.6 | 31 |
| ja | osaka | 1 | 10 | 12.1 | 11 |
| de | zurich | 1 | 9 | 9.9 | 9 |
| fr | nice | 0 | 8 | 21.9 | 12 |

**Cities seen but never clicked** (60+ impressions, zero clicks, with what they are actually shown for):

- tenerife (i89): drago milenario (i18, p11); pino gordo tenerife (i9, p10); el drago milenario (i8, p10); pino gordo (i7, p18)
- Seen, not clicked: /rome (c1/i127, 0.8%) for trees in rome (i24, p11); rome trees (i21, p10); famous trees in rome (i10, p7)
- Seen, not clicked: /species/strawberry-tree (c0/i77, 0.0%) for strawberry tree (i22, p68); arbutus strawberry tree (i8, p62); greek strawberry tree (i4, p67)
- Seen, not clicked: /tenerife/el-drago-milenario (c0/i59, 0.0%) for drago milenario (i18, p11); el drago milenario (i8, p10); tenerife oldest tree (i5, p10)
- Seen, not clicked: /species/osage-orange (c0/i57, 0.0%) for osage orange (i8, p85); where to find osage orange trees (i2, p70); where do osage orange trees grow (i2, p96)
- Seen, not clicked: /las-vegas (c0/i49, 0.0%) for vegas trees (i49, p33)
- Seen, not clicked: / (c1/i43, 2.3%) for ancient trees (i20, p26); ancient tree (i12, p48); ancient tree map (i3, p17)
- Seen, not clicked: /hilo/loulu-palm-of-kalakaua-park (c0/i37, 0.0%) for loulu palm (i33, p82); loulu palm tree (i2, p52); loulu tree (i1, p47)
- Seen, not clicked: /copenhagen (c0/i36, 0.0%) for trees in copenhagen (i28, p17); copenhagen trees (i7, p17); trees in denmark (i1, p38)

**Climbing** (this ten days against the ten before it)

| Page | Impressions | Change | Position | Moved | Clicks |
|---|---:|---:|---:|---:|---:|
| /rome | 376 | +195 | 10.5 | +6.8 | +2 |
| /seville | 141 | +125 | 10.1 | +2.1 | +5 |
| /species/osage-orange | 109 | +94 | 82.7 | -13.0 | +0 |
| /copenhagen | 147 | +91 | 11.8 | +1.0 | +2 |
| /species/strawberry-tree | 104 | +91 | 67.0 | -5.5 | +0 |
| /tenerife/el-drago-milenario | 108 | +83 | 10.8 | +0.4 | +0 |
| /milan | 182 | +80 | 8.4 | +3.2 | +0 |
| / | 129 | +69 | 17.1 | -4.0 | +2 |

**Newly ranking** (no impressions at all ten days ago)

| Page | Impressions | Clicks | Position |
|---|---:|---:|---:|
| /amsterdam/elm-of-elsenhoeve | 90 | 4 | 6.2 |
| /las-vegas | 53 | 0 | 31.1 |
| /species/austrian-pine | 32 | 0 | 81.3 |
| /sydney/wishing-tree | 30 | 0 | 8.6 |
| /de/berlin/kaisereiche | 27 | 0 | 15.7 |
| /perth/oldest-tree | 25 | 0 | 9.2 |

**Slipping**

| Page | Impressions | Change | Position | Moved |
|---|---:|---:|---:|---:|
| /cadiz | 16 | -3 | 8.6 | -1.6 |

- New queries this window: italian trees in rome (i4).

**Who they are** (full cut, Mondays)
Audience, 28 days of search (406 clicks, 18247 impressions):
- Countries: usa c71/i3993; gbr c46/i2143; nld c28/i883; aus c19/i599; prt c19/i482
- Devices: MOBILE c279/i9959; DESKTOP c122/i8127; TABLET c5/i161
- Landing pages: / c26/i206; /prague c20/i317; /lisbon c10/i337; /seville c8/i183; /amsterdam c7/i406
- Search language (top 100 named queries, crude match, most clicks are in queries Google withholds): English 59q c6/i223; unclassified 31q c7/i145; Spanish 6q c0/i10; Italian 3q c0/i3; German 1q c0/i1
On the site since 2026-08-08 (1360 visits, 2240 pageviews, 1.6 pages per visit):
- Countries: NL 490; US 400; AU 170; GB 170; DE 160
- Devices: desktop 1260; mobile 960; tablet 20
- Browsers: Chrome 830; ChromeMobile 460; MobileSafari 410; Unknown 150
- Arrived via: (direct) 890; ancienttrees.app 880; www.google.com 460; zscaler-blocked.dpgmedia.n 10
- Opened: / 280; /amsterdam 100; /explore 90; /app 90; /copenhagen 70; /porto 60; /paris 50; /prague 50

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-23 | 70 | 120 |
| 08-24 | 10 | 20 |
| 08-25 | 60 | 70 |
| 08-26 | 80 | 110 |
| 08-27 | 60 | 140 |
| 08-28 | 120 | 170 |
| 08-29 | 60 | 140 |
| 08-30 | 70 | 180 |
| **window** | **530** | **950** |
- Top paths: / (120); /explore (50); /melbourne/remnant-river-red-gum-of-edinburgh-gardens (30); /copenhagen (30); /nijmegen/wilhelminaboom-of-hertogplein (30); /prague (30); /brisbane/hoop-pine (20); /app (20); /melbourne (20); /cities (20); /brussels (20); /sponsor (20)
- Referrers: ancienttrees.app (420); (direct) (320); www.google.com (210)
- Moved between our own pages: 420 of 950 pageviews (44%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: US (170); AU (130); NL (100); ES (80); GB (80)
- Devices: mobile (470); desktop (460); tablet (20)
- Page load (8d): p50 753ms, p90 2894ms

Links: external referrers (a link somebody actually clicked): none yet
AI: arrivals from an assistant that cited us: none yet


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 08-30T09:33 | 7.8 | 0 | 1 | 8 | - |
| 08-30T11:49 | 63.6 | 4 | 16 | 31 | Vancouver +4, Malaga |
| 08-30T14:33 | 98.5 | 13 | 12 | 53 | Krakow +8, Singapore +4, Nuremberg +1, Assisi, +2 more |
| 08-30T16:36 | 49.2 | 5 | 19 | 46 | Riga +5 |
| 08-30T18:55 | 24.3 | 0 | 11 | 19 | - |
| 08-30T19:20 | 20.9 | 8 | 13 | 29 | Coimbra +4, Rothenburg Ob Der Tauber +4 |
| 08-30T22:13 | 14.8 | 0 | 2 | 13 | Prague |
| 08-31T02:11 | 75.5 | 17 | 6 | 42 | Valencia +8, Singapore +6, Nijmegen +2, Luxembourg City +1 |
| **8 runs** | **355** | **47** | **80** | | |

- 3 of 8 produced no trees; 8 to 53 commands refused per run; 2 wrote nothing to LOG.md.

**What they made**

- Singapore +6 trees, a Botanic Gardens cluster from the NParks register
- Valencia +8 trees, plus the species and park pages they earned
- Nijmegen +2, Luxembourg City +1; iOS CI hang traced but not fixed
- Add Norway Spruce species page; fix Luxembourg City id collision; stale-file cleanup
- Coimbra and Rothenburg ob der Tauber published, 0 -> 4 trees each
- Fix iOS CI: two sign-in tests need -show-email now that it is hidden by default
- Verify pass: Coimbra and Rothenburg ob der Tauber, 4 trees each
- LOG.md: this run's progress so far
- leads.py: READY now requires a pass actually looked at the tree
- Refill genus for a Portuguese famous-tree lead; photo_hunt.py --recheck sweep
- Process submissions #45-53: vote-toggle bookkeeping on Rome rom_002, no action needed
- Re-harvest Wikidata candidates for madeira; log the Riga publish and re-dispatched claims
- Publish Riga: 5 verified trees with stories, city goes live
- famous_trees.py sweep for Portugal: 9 candidates queued for viewing pass, 14 new leads recorded

Machine: 8 chain attempts yesterday, 8 got real work time (~306 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 17 clicks and 634 impressions on Google's freshest day (day before: c32/i1068). Directional at best; no strategic conclusions from these volumes.

## 2026-08-29 (previous UTC day)

**Today: 2 tree submissions arrived yesterday (27 total).**

**Did the product happen**

| Action | Yesterday | 14 days | Ever | Last |
|---|---:|---:|---:|---|
| app-cta | 1 | 36 | 36 | yesterday |
| search-home | 5 | 17 | 17 | today |
| directions | 4 | 15 | 15 | today |
| waitlist-submit | 0 | 9 | 9 | 2 days ago |
| save | 0 | 7 | 7 | 4 days ago |
| search-explore | 0 | 5 | 5 | today |
| walks-app | 0 | 5 | 5 | 2 days ago |
| walk-open | 0 | 4 | 4 | 13 days ago |
| suggestion-submit | 0 | 3 | 3 | 10 days ago |
| smoke-test | 0 | 0 | 2 | 29 days ago |
| beacon-fix-verify | 0 | 1 | 1 | 14 days ago |
| beacon-test | 0 | 1 | 1 | 14 days ago |
| worthit-not worth it | 0 | 1 | 1 | 13 days ago |
| signin-link-sent | 0 | 0 | 0 | never |
| walk-start | 0 | 0 | 0 | never |
| worthit-worth it | 0 | 0 | 0 | never |
| **all** | **10** | **104** | **106** | |
- 'Ever' counts every row in the events table, which begins 2026-08-01 when the funnel was repaired. Anything named here with a zero has never fired at all.

**What people typed into our search** (14 days, 18 searches, 15 different terms)

| Typed | Times |
|---|---:|
| mel | 3 |
| melbourne | 2 |
| berli | 1 |
| boston | 1 |
| copenhagen | 1 |
| ei | 1 |
| glasg | 1 |
| leiden | 1 |
| london | 1 |
| milano | 1 |
| oslo | 1 |
| portland | 1 |
| sofia | 1 |
| sy | 1 |
| war | 1 |

| Day | Accounts | Waitlist | Saves | Trees sent | Feedback |
|---|---:|---:|---:|---:|---:|
| 08-16 | 0 | 0 | 0 | 0 | 0 |
| 08-17 | 0 | 1 | 0 | 0 | 2 |
| 08-18 | 0 | 1 | 2 | 0 | 0 |
| 08-19 | 0 | 1 | 0 | 0 | 0 |
| 08-20 | 0 | 1 | 3 | 0 | 1 |
| 08-21 | 1 | 0 | 0 | 0 | 16 |
| 08-22 | 0 | 0 | 1 | 0 | 0 |
| 08-23 | 0 | 0 | 0 | 0 | 0 |
| 08-24 | 0 | 0 | 0 | 1 | 0 |
| 08-25 | 0 | 1 | 0 | 0 | 0 |
| 08-26 | 0 | 1 | 1 | 0 | 1 |
| 08-27 | 0 | 1 | 0 | 1 | 1 |
| 08-28 | 0 | 1 | 0 | 0 | 1 |
| 08-29 | 0 | 0 | 0 | 2 | 0 |
| 08-30 | 0 | 0 | 0 | 0 | 0 |
| **14 days** | **1** | **8** | **7** | **4** | **22** |
- Waitlist:    14 total, newest 2 days ago
- Submissions: 27 total (4 trees sent, 23 feedback), newest yesterday
- Accounts:    4 total, newest 9 days ago

**What readers told us** (14 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 08-17 | hel_006 (The Meilahti Ancient Pine | not worth it | - | no acct | holds |
| 08-17 | lis_005 (The Tipu of Jardim de São | worth it | - | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-21 | par_001 (The Robinier of Square Re | not worth it | - | no acct | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | report | could not reach it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | worth it | - | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | not worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-24 | Baarn | tree sent in | 4 chars, read it in the database | d4e6 | open_question |
| 08-25 | utr_005 (Onder de Linden) | vote undone | not worth it | d4e6 | - |
| 08-26 | sar_003 (The Olivastro of Santa Ma | worth it | - | d4e6 | - |
| 08-27 | ams_001 | worth it | - | 46c1 | holds |
| 08-27 | Baarn | tree sent in | 4 chars, read it in the database | d4e6 | holds |
| 08-28 | - | Super | - | d4e6 | - |
| 08-29 | Baarn | tree sent in | 4 chars, read it in the database | d4e6 | holds |
| 08-29 | Baarn | tree sent in | - | d4e6 | holds |

- 33 of these 40 came from one account (d4e6). At this volume that is almost certainly our own testing rather than readers, and it should be read that way until somebody checks the rows.

**The funnel, as rates**
- Seen to clicked: 2.1% (276 of 12895) vs 2.3% the fortnight before
- Pages per visit: 1.6 (1290 visits, 2060 pageviews since 2026-08-08)
- Visits that did something: 8.1% (104 actions on 1290 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-20 | 17 | 1022 | 1.7% | 21.5 |
| 08-21 | 18 | 913 | 2.0% | 19.9 |
| 08-22 | 17 | 1030 | 1.7% | 19.9 |
| 08-23 | 15 | 958 | 1.6% | 16.2 |
| 08-24 | 28 | 998 | 2.8% | 15.9 |
| 08-25 | 19 | 1108 | 1.7% | 20.1 |
| 08-26 | 24 | 1144 | 2.1% | 18.7 |
| 08-27 | 15 | 1003 | 1.5% | 18.8 |
| 08-28 | 27 | 1014 | 2.7% | 16.3 |
| 08-29 *partial* | 29 | 948 | 3.1% | 17.2 |
| **window** | **209** | **10138** | **2.1%** | |
- Top queries (10d): dutch elm amsterdam (i59, p5); ancient tree (i15, p40); ancient trees (i22, p25); e bordeaux? (i1, p1); italian trees in rome (i3, p11)
- Top pages (10d): /prague (c11/i144); / (c8/i117); /seville (c6/i129); /lisbon (c5/i173); /amsterdam/elm-of-elsenhoeve (c4/i75)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - '"oldest of its species" owl park' (i9, p8)
    - '"400 years old as of 2023" tree' (i1, p7)
    - '"oldest of its species" "park" tree' (i1, p10)
    - '"stands nearly 20 metres" tower medieval' (i1, p8)
    - '10 feet tall trees' (i1, p58)
    - '800 year old tree' (i1, p10)
    - '99 yew trees' (i1, p58)
    - 'a izvan hrvatske' (i1, p4)
    - and 1 more

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| rome | 4 | 419 | 1.0% | 10.6 | 2.3% | trees in rome (i22, p11) |
| amsterdam | 11 | 393 | 2.8% | 10.1 | 2.5% | dutch elm amsterdam (i37, p4) |
| tenerife | 1 | 244 | 0.4% | 10.1 | 2.5% | drago milenario (i21, p11) |
| lisbon | 7 | 220 | 3.2% | 8.1 | 3.4% | oldest tree in lisbon (i6, p9) |
| milan | 0 | 214 | 0.0% | 8.7 | 3.1% | "oldest of its species" ginkgo park (i9, p6) |
| copenhagen | 6 | 211 | 2.8% | 12.4 | 1.7% | trees in copenhagen (i31, p18) |
| brisbane | 5 | 199 | 2.5% | 17.6 | 1.0% | the big macadamia nut (i10, p66) |
| singapore | 5 | 194 | 2.6% | 11.4 | 2.0% | oldest tree in singapore (i22, p10) |
| barcelona | 4 | 182 | 2.2% | 10.1 | 2.5% | barcelona trees (i7, p9) |
| seville | 8 | 165 | 4.8% | 10.0 | 2.5% | seville spain orange trees (i1, p41) |
| bath | 3 | 164 | 1.8% | 8.1 | 3.4% | how old is the tree in abbey green bath (i7, p9) |
| prague | 11 | 162 | 6.8% | 8.0 | 3.5% | - |
| vienna | 2 | 157 | 1.3% | 9.1 | 2.9% | alter (i1, p3) |
| malaga | 3 | 150 | 2.0% | 13.5 | 1.5% | árboles históricos de málaga (i13, p80) |
| london | 1 | 148 | 0.7% | 26.3 | 0.5% | trees in london (i2, p70) |
| paris | 1 | 143 | 0.7% | 20.0 | 0.8% | palm trees in paris (i3, p61) |
| florence | 2 | 131 | 1.5% | 10.0 | 2.5% | florence tree (i6, p9) |
| crete | 0 | 120 | 0.0% | 10.7 | 2.3% | 2000 years old olive tree (i2, p13) |
| madeira | 2 | 118 | 1.7% | 8.4 | 3.3% | dragon tree madeira (i6, p10) |
| naples | 2 | 117 | 1.7% | 12.0 | 1.8% | naples tree (i2, p5) |
| madrid | 0 | 109 | 0.0% | 15.4 | 1.2% | oldest tree in madrid (i3, p9) |
| palermo | 1 | 102 | 1.0% | 7.0 | 4.0% | oldest tree in palermo (i2, p12) |
| seoul | 0 | 96 | 0.0% | 14.1 | 1.4% | seoul trees (i5, p8) |
| montreal | 4 | 93 | 4.3% | 10.7 | 2.2% | century trees (i3, p53) |
| brussels | 2 | 92 | 2.2% | 9.9 | 2.6% | belgian trees (i1, p36) |
| palma-de-mallorca | 0 | 92 | 0.0% | 6.9 | 4.1% | oldest olive tree in palma (i2, p10) |
| edinburgh | 2 | 87 | 2.3% | 15.6 | 1.2% | oldest tree in edinburgh (i2, p10) |
| fukuoka | 3 | 86 | 3.5% | 11.5 | 2.0% | kanatake (i2, p76) |
| toronto | 1 | 86 | 1.2% | 9.9 | 2.6% | big red oak (i12, p7) |
| venice | 0 | 86 | 0.0% | 8.8 | 3.1% | trees in venice (i2, p10) |
| valencia | 2 | 78 | 2.6% | 8.6 | 3.2% | ficus centenarios de la glorieta (i2, p11) |
| las-vegas | 0 | 76 | 0.0% | 24.4 | 0.6% | vegas trees (i49, p33) |
| sardinia | 0 | 76 | 0.0% | 8.1 | 3.4% | baltolu sardinia (i10, p7) |
| new-york | 2 | 70 | 2.9% | 17.8 | 1.0% | - |
| dublin | 2 | 65 | 3.1% | 12.6 | 1.7% | oldest tree in ireland (i1, p62) |
| bologna | 0 | 61 | 0.0% | 7.5 | 3.8% | - |
| krakow | 2 | 56 | 3.6% | 11.4 | 2.0% | bednarski park (i1, p12) |
| istanbul | 2 | 55 | 3.6% | 6.3 | 4.7% | a ten ile ma (i1, p2) |
| portland | 1 | 54 | 1.9% | 10.7 | 2.3% | - |
| reykjavik | 0 | 54 | 0.0% | 19.6 | 0.8% | oldest tree in iceland (i5, p8) |
| alicante | 0 | 53 | 0.0% | 7.0 | 4.0% | ficus alicante (i4, p9) |
| nijmegen | 0 | 53 | 0.0% | 7.1 | 4.0% | hertogplein nijmegen maps (i1, p6) |
| cyprus | 2 | 51 | 3.9% | 8.0 | 3.5% | oldest tree in cyprus (i5, p10) |
| kyoto | 1 | 51 | 2.0% | 8.5 | 3.3% | japanese camphor (i1, p84) |
| hilo | 0 | 51 | 0.0% | 64.4 | 0.4% | loulu palm (i31, p85) |
| perth | 0 | 50 | 0.0% | 14.8 | 1.2% | jarra tree (i2, p38) |
| sydney | 0 | 49 | 0.0% | 7.2 | 3.9% | the wishing tree sydney (i6, p10) |
| chicago | 4 | 48 | 8.3% | 11.4 | 2.0% | wooded grove (i1, p48) |
| greece | 1 | 48 | 2.1% | 32.8 | 0.4% | greek trees (i6, p37) |
| mexico-city | 2 | 48 | 4.2% | 10.7 | 2.3% | viejo del agua (i2, p6) |
| athens | 2 | 46 | 4.3% | 14.5 | 1.3% | oldest olive tree in athens (i1, p1) |
| cambridge | 0 | 44 | 0.0% | 31.6 | 0.4% | newton's apple tree (i5, p46) |
| bordeaux | 2 | 43 | 4.7% | 8.0 | 3.5% | sequoia bordeaux (i2, p9) |
| leiden | 0 | 42 | 0.0% | 11.0 | 2.1% | "oldest of its species" ginkgo park (i7, p9) |
| munich | 1 | 41 | 2.4% | 8.1 | 3.5% | kirchtruderinger straße (i1, p8) |
| boston | 1 | 40 | 2.5% | 24.6 | 0.6% | trees in boston (i2, p54) |
| the-hague | 1 | 40 | 2.5% | 7.0 | 4.0% | old tree (i1, p9) |
| seattle | 2 | 39 | 5.1% | 6.4 | 4.6% | - |
| vilnius | 4 | 39 | 10.3% | 8.3 | 3.4% | willow tree in lithuanian (i3, p9) |
| oslo | 2 | 38 | 5.3% | 13.3 | 1.5% | "oldest ginkgo tree" park motto (i1, p5) |
| tokyo | 0 | 38 | 0.0% | 6.4 | 4.6% | - |
| berlin | 0 | 37 | 0.0% | 13.6 | 1.5% | berlin tree map (i1, p10) |
| geneva | 3 | 36 | 8.3% | 9.2 | 2.9% | - |
| porto | 3 | 36 | 8.3% | 6.3 | 4.7% | alameda dos platanos (i9, p7) |
| bristol | 2 | 34 | 5.9% | 19.3 | 0.9% | bristol trees (i2, p55) |
| budapest | 1 | 34 | 2.9% | 7.1 | 4.0% | - |
| dubrovnik | 1 | 34 | 2.9% | 7.6 | 3.7% | trsteno plane tree (i2, p12) |
| strasbourg | 2 | 34 | 5.9% | 7.5 | 3.8% | - |
| washington-dc | 1 | 34 | 2.9% | 23.2 | 0.7% | survey lodge ranger station (i5, p11) |
| cagliari | 0 | 33 | 0.0% | 4.9 | 7.1% | età (i1, p2) |
| groningen | 1 | 30 | 3.3% | 19.0 | 0.9% | big five groningen (i1, p83) |
| bratislava | 2 | 28 | 7.1% | 9.3 | 2.9% | - |
| aarhus | 1 | 28 | 3.6% | 8.0 | 3.5% | happy pig (i2, p10) |
| new-orleans | 1 | 28 | 3.6% | 26.4 | 0.5% | anseman oak (i3, p9) |
| sintra | 2 | 28 | 7.1% | 6.0 | 5.0% | - |
| cadiz | 0 | 28 | 0.0% | 7.8 | 3.6% | cadiz botanical gardens (i1, p2) |
| trieste | 0 | 28 | 0.0% | 8.6 | 3.2% | piazza hortis (i4, p10) |
| utrecht | 1 | 27 | 3.7% | 8.3 | 3.4% | zocher utrecht (i2, p22) |
| guimaraes | 0 | 27 | 0.0% | 13.2 | 1.6% | pine tree portugal (i5, p18) |
| quebec-city | 0 | 26 | 0.0% | 10.8 | 2.2% | avenue elm (i1, p34) |
| helsinki | 0 | 25 | 0.0% | 6.3 | 4.7% | in helsinki (i1, p4) |
| potsdam | 0 | 25 | 0.0% | 14.4 | 1.3% | jagdschloss glienicke (i1, p12) |
| warsaw | 2 | 24 | 8.3% | 10.7 | 2.3% | poland national tree (i1, p55) |
| sorrento | 1 | 24 | 4.2% | 21.5 | 0.7% | - |
| cordoba | 0 | 24 | 0.0% | 38.9 | 0.4% | gingko garden (i1, p56) |
| glasgow | 0 | 24 | 0.0% | 10.0 | 2.5% | - |
| padua | 0 | 24 | 0.0% | 8.6 | 3.2% | - |
| cork | 1 | 23 | 4.3% | 15.0 | 1.2% | oldest tree in ireland (i5, p14) |
| york | 1 | 23 | 4.3% | 8.2 | 3.4% | - |
| oxford | 3 | 22 | 13.6% | 7.8 | 3.6% | - |
| lyon | 1 | 22 | 4.5% | 15.7 | 1.1% | antoine rivoire (i2, p8) |
| hong-kong | 0 | 22 | 0.0% | 6.6 | 4.4% | - |
| zurich | 1 | 21 | 4.8% | 14.5 | 1.3% | - |
| arnhem | 0 | 20 | 0.0% | 9.0 | 3.0% | musispark arnhem (i1, p4) |
| canada | 0 | 20 | 0.0% | 21.9 | 0.7% | oldest tree in canada (i3, p21) |
| nuremberg | 0 | 20 | 0.0% | 6.2 | 4.8% | - |
| tallinn | 0 | 20 | 0.0% | 8.9 | 3.0% | - |
| maastricht | 1 | 19 | 5.3% | 7.4 | 3.8% | - |
| nara | 1 | 19 | 5.3% | 11.2 | 2.1% | - |
| oahu | 1 | 19 | 5.3% | 6.9 | 4.1% | - |
| nice | 0 | 19 | 0.0% | 6.7 | 4.3% | promenade des anglais palm trees (i1, p5) |
| dallas | 1 | 18 | 5.6% | 7.7 | 3.7% | centennial tree (i2, p13) |
| toulouse | 2 | 17 | 11.8% | 5.7 | 5.6% | - |
| austin | 0 | 17 | 0.0% | 12.9 | 1.6% | antebellum oaks (i1, p54) |
| graz | 1 | 16 | 6.2% | 7.2 | 3.9% | oak (i2, p8) |
| melbourne | 3 | 16 | 18.8% | 9.0 | 3.0% | - |
| eindhoven | 0 | 16 | 0.0% | 10.7 | 2.3% | beukenboom (i1, p3) |
| bangkok | 0 | 15 | 0.0% | 10.4 | 2.4% | - |
| caserta | 0 | 14 | 0.0% | 24.4 | 0.6% | parchi caserta (i1, p1) |
| turin | 0 | 14 | 0.0% | 4.9 | 7.1% | - |
| belgrade | 1 | 13 | 7.7% | 18.8 | 0.9% | - |
| poznan | 1 | 13 | 7.7% | 22.2 | 0.7% | - |
| australia | 0 | 13 | 0.0% | 22.2 | 0.7% | oldest tree in australia (i3, p42) |
| catania | 0 | 13 | 0.0% | 6.8 | 4.2% | - |
| bilbao | 0 | 12 | 0.0% | 7.3 | 3.8% | - |
| emmen | 0 | 12 | 0.0% | 5.9 | 5.2% | rensenpark emmen former zoo park (i1, p6) |
| frankfurt | 0 | 12 | 0.0% | 5.1 | 6.8% | what tree is this (i1, p6) |
| ljubljana | 0 | 12 | 0.0% | 22.5 | 0.7% | - |
| braga | 1 | 11 | 9.1% | 9.6 | 2.7% | santa tecla braga (i1, p1) |
| delft | 2 | 11 | 18.2% | 23.1 | 0.7% | - |
| lucca | 1 | 11 | 9.1% | 6.5 | 4.5% | lucca tree (i1, p10) |
| brno | 0 | 11 | 0.0% | 6.1 | 4.9% | - |
| haarlem | 0 | 11 | 0.0% | 14.5 | 1.3% | noble tree (i1, p59) |
| portugal | 0 | 11 | 0.0% | 62.5 | 0.4% | portugal trees (i2, p71) |
| rotterdam | 0 | 11 | 0.0% | 8.9 | 3.0% | delftseplein (i2, p4) |
| setubal | 0 | 11 | 0.0% | 8.5 | 3.3% | - |
| houston | 1 | 10 | 10.0% | 49.2 | 0.4% | trees in houston texas (i3, p67) |
| split | 0 | 10 | 0.0% | 9.0 | 3.0% | mediterranean cypress croatia (i2, p8) |
| verona | 0 | 10 | 0.0% | 6.8 | 4.2% | - |

**The language test** (Contract J v1.13: a translated set should pass its English twin's impressions within four weeks of indexing):

| Lang | City | Clicks | Impressions | Position | English twin |
|---|---|---:|---:|---:|---:|
| es | malaga | 1 | 131 | 12.3 | 150 |
| de | berlin | 0 | 70 | 20.1 | 37 |
| ja | kyoto | 1 | 45 | 10.2 | 51 |
| pt | lisbon | 3 | 40 | 10.6 | 220 |
| de | vienna | 1 | 38 | 10.0 | 157 |
| it | rome | 3 | 35 | 10.1 | 419 |
| pt | porto | 1 | 33 | 6.2 | 36 |
| ja | tokyo | 0 | 32 | 10.1 | 38 |
| it | palermo | 0 | 27 | 9.1 | 102 |
| pt | sintra | 1 | 19 | 14.3 | 28 |
| es | cadiz | 1 | 18 | 15.0 | 28 |
| es | barcelona | 0 | 18 | 15.9 | 182 |
| nl | nijmegen | 0 | 17 | 7.9 | 53 |
| es | madrid | 0 | 14 | 7.8 | 109 |
| es | tenerife | 0 | 11 | 31.4 | 244 |
| fr | geneva | 0 | 11 | 21.6 | 36 |
| nl | amsterdam | 0 | 10 | 3.2 | 393 |
| it | milan | 0 | 9 | 14.6 | 214 |
| ja | osaka | 1 | 8 | 13.0 | 8 |
| de | zurich | 1 | 7 | 9.9 | 21 |
| fr | nice | 0 | 7 | 24.4 | 19 |

**Cities seen but never clicked** (60+ impressions, zero clicks, with what they are actually shown for):

- tenerife (i98): drago milenario (i21, p11); pino gordo (i9, p20); pino gordo tenerife (i8, p10); el drago milenario (i8, p10)
- Seen, not clicked: /rome (c1/i116, 0.9%) for trees in rome (i22, p11); rome trees (i20, p10); famous trees in rome (i10, p7)
- Seen, not clicked: /species/strawberry-tree (c0/i72, 0.0%) for strawberry tree (i22, p68); arbutus strawberry tree (i7, p63); strawberry trees (i4, p74)
- Seen, not clicked: /tenerife/el-drago-milenario (c0/i67, 0.0%) for drago milenario (i21, p11); el drago milenario (i8, p10); tenerife oldest tree (i5, p10)
- Seen, not clicked: /species/osage-orange (c0/i55, 0.0%) for osage orange (i8, p85); where to find osage orange trees (i2, p70); where do osage orange trees grow (i2, p96)
- Seen, not clicked: /las-vegas (c0/i49, 0.0%) for vegas trees (i49, p33)
- Seen, not clicked: /copenhagen (c0/i43, 0.0%) for trees in copenhagen (i31, p18); copenhagen trees (i10, p20); trees near me (i1, p75)
- Seen, not clicked: / (c1/i40, 2.5%) for ancient trees (i20, p29); ancient tree (i10, p52); ancient tree map (i3, p17)
- Seen, not clicked: /hilo/loulu-palm-of-kalakaua-park (c0/i35, 0.0%) for loulu palm (i31, p85); loulu palm tree (i2, p52); loulu tree (i1, p47)

**Climbing** (this ten days against the ten before it)

| Page | Impressions | Change | Position | Moved | Clicks |
|---|---:|---:|---:|---:|---:|
| /rome | 361 | +186 | 11.2 | +6.3 | +1 |
| /copenhagen | 157 | +118 | 12.6 | -2.0 | +2 |
| /tenerife/el-drago-milenario | 123 | +114 | 10.8 | +1.4 | +0 |
| /seville | 129 | +109 | 10.2 | - | +5 |
| /species/osage-orange | 114 | +109 | 80.7 | -1.3 | +0 |
| /milan | 195 | +104 | 8.6 | +2.3 | +0 |
| /species/strawberry-tree | 101 | +98 | 66.8 | -22.5 | +0 |
| /lisbon | 173 | +74 | 7.6 | +1.9 | +2 |

**Newly ranking** (no impressions at all ten days ago)

| Page | Impressions | Clicks | Position |
|---|---:|---:|---:|
| /amsterdam/elm-of-elsenhoeve | 75 | 4 | 6.1 |
| /species/american-elm | 62 | 0 | 78.4 |
| /las-vegas | 53 | 0 | 31.1 |
| /palma-de-mallorca/solivera-de-cort | 51 | 0 | 6.8 |
| /greece | 48 | 1 | 32.8 |
| /hilo/loulu-palm-of-kalakaua-park | 39 | 0 | 80.5 |

**Slipping**

| Page | Impressions | Change | Position | Moved |
|---|---:|---:|---:|---:|
| /boston | 17 | -24 | 32.0 | -15.2 |
| /oslo | 15 | -16 | 18.0 | -5.7 |
| /washington-dc | 17 | -14 | 24.5 | -7.3 |

- New queries this window: italian trees in rome (i3).

**Who they are**
Audience, 28 days of search (393 clicks, 17792 impressions):
- Countries: usa c69/i3956; gbr c44/i2096; nld c27/i846; prt c20/i460; esp c19/i1077
- Devices: MOBILE c273/i9640; DESKTOP c115/i7995; TABLET c5/i157
- Landing pages: / c20/i194; /prague c18/i315; /lisbon c10/i320; /seville c8/i172; /amsterdam c7/i397

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-22 | 90 | 120 |
| 08-23 | 70 | 120 |
| 08-24 | 10 | 20 |
| 08-25 | 60 | 70 |
| 08-26 | 80 | 110 |
| 08-27 | 60 | 140 |
| 08-28 | 120 | 170 |
| 08-29 | 60 | 140 |
| **window** | **550** | **890** |
- Top paths: / (130); /copenhagen (40); /nijmegen/wilhelminaboom-of-hertogplein (30); /brisbane/hoop-pine (20); /explore (20); /cities (20); /melbourne/remnant-river-red-gum-of-edinburgh-gardens (20); /brussels (20); /amsterdam (20); /sponsor (20); /aarhus (10); /bath/plane-trees-of-the-circus (10)
- Referrers: (direct) (360); ancienttrees.app (340); www.google.com (190)
- Moved between our own pages: 340 of 890 pageviews (38%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: US (150); AU (90); NL (90); GB (80); DE (70)
- Devices: desktop (500); mobile (370); tablet (20)
- Page load (8d): p50 815ms, p90 3094ms

Links: external referrers (a link somebody actually clicked): none yet
AI: arrivals from an assistant that cited us: none yet


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 08-29T10:33 | 44.3 | 11 | 5 | 49 | Salzburg +5, Bucaco +4, Los Angeles +1, Warsaw +1 |
| 08-29T11:40 | 58.1 | 4 | 18 | 55 | Barcelona +1, Cagliari +1, Naples +1, Oahu +1 |
| 08-29T13:53 | 39.6 | 3 | 15 | 31 | Sorrento +2, Oahu +1, Barcelona, Crete, +2 more |
| 08-29T15:54 | 114.7 | 16 | 28 | 40 | Assisi +6, Cesky Krumlov +6, Bamberg +4 |
| 08-29T18:59 | 6.8 | 0 | 2 | 7 | - |
| 08-29T22:06 | 14.6 | 0 | 5 | 14 | - |
| 08-30T02:16 | 12.4 | 0 | 2 | 19 | - |
| 08-30T09:33 | 7.8 | 0 | 1 | 8 | - |
| **8 runs** | **298** | **34** | **76** | | |

- 4 of 8 produced no trees; 7 to 55 commands refused per run; 3 wrote nothing to LOG.md.

**What they made**

- Fix appfit's DRIFT false positive on the keyboard's own frame
- Clean up stale research files for cities merged this session
- Cesky Krumlov opens: 6 trees, and a real check_paid_share() gap fixed
- refill.py: genus guess for one Bamberg lead (oak, from its own name)
- LOG.md: note the git/gh credential outage and how it was worked around
- preflight.py: catch stale country-page counts (the pattern just found 12 times)
- Fix stale city/tree counts on 11 country pages (rung 3, found while opening Bamberg/Assisi)
- photo_hunt.py --recheck sweep (free API, no tokens)
- Species page: Downy Oak, from its own four trees (Assisi, Perugia)
- Assisi opens: 6 trees, and a passcheck.py bug caught before it did damage
- passcheck.py: don't fold a separately-ranked city into a nearby one on distance alone
- Bamberg opens: 4 protected trees, none dated, exactly at the floor
- LOG.md: this window's work so far
- photo_hunt.py --recheck: queue refreshed for a future viewing pass

Machine: 8 chain attempts yesterday, 8 got real work time (~325 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 29 clicks and 948 impressions on Google's freshest day (day before: c27/i1014). Directional at best; no strategic conclusions from these volumes.

## 2026-08-28 (previous UTC day)

**Today: a waitlist arrived yesterday (14 total); 1 feedback report arrived yesterday (25 total).**

**Did the product happen**
- directions:  5 yesterday, last today
- waitlist-submit: 1 yesterday, last yesterday
- walks-app:   1 yesterday, last yesterday
- app-cta:     0 yesterday, last 2 days ago
- beacon-fix-verify: 0 yesterday, last 13 days ago
- beacon-test: 0 yesterday, last 13 days ago
- save:        0 yesterday, last 3 days ago
- search-explore: 0 yesterday, last 8 days ago
- search-home: 0 yesterday, last today
- signin-link-sent: 0 yesterday, last never
- smoke-test:  0 yesterday, last 28 days ago
- suggestion-submit: 0 yesterday, last 9 days ago
- walk-open:   0 yesterday, last 12 days ago
- walk-start:  0 yesterday, last never
- worthit-not worth it: 0 yesterday, last 12 days ago
- worthit-worth it: 0 yesterday, last never

| Day | Accounts | Waitlist | Saves | Trees sent | Feedback |
|---|---:|---:|---:|---:|---:|
| 08-15 | 0 | 0 | 0 | 0 | 1 |
| 08-16 | 0 | 0 | 0 | 0 | 0 |
| 08-17 | 0 | 1 | 0 | 0 | 2 |
| 08-18 | 0 | 1 | 2 | 0 | 0 |
| 08-19 | 0 | 1 | 0 | 0 | 0 |
| 08-20 | 0 | 1 | 3 | 0 | 1 |
| 08-21 | 1 | 0 | 0 | 0 | 16 |
| 08-22 | 0 | 0 | 1 | 0 | 0 |
| 08-23 | 0 | 0 | 0 | 0 | 0 |
| 08-24 | 0 | 0 | 0 | 1 | 0 |
| 08-25 | 0 | 1 | 0 | 0 | 0 |
| 08-26 | 0 | 1 | 1 | 0 | 1 |
| 08-27 | 0 | 1 | 0 | 1 | 1 |
| 08-28 | 0 | 1 | 0 | 0 | 1 |
| 08-29 | 0 | 0 | 0 | 0 | 0 |
| **14 days** | **1** | **8** | **7** | **2** | **23** |
- Waitlist:    14 total, newest yesterday
- Submissions: 25 total (2 trees sent, 23 feedback), newest yesterday
- Accounts:    4 total, newest 8 days ago

**What readers told us** (14 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 08-15 | prg_007 (The Oak of Cisarsky ostro | not worth it | wrong location | no acct | holds |
| 08-17 | hel_006 (The Meilahti Ancient Pine | not worth it | - | no acct | holds |
| 08-17 | lis_005 (The Tipu of Jardim de São | worth it | - | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-21 | par_001 (The Robinier of Square Re | not worth it | - | no acct | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | report | could not reach it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | worth it | - | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | not worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-24 | Baarn | tree sent in | 4 chars, read it in the database | d4e6 | open_question |
| 08-25 | utr_005 (Onder de Linden) | vote undone | not worth it | d4e6 | - |
| 08-26 | sar_003 (The Olivastro of Santa Ma | worth it | - | d4e6 | - |
| 08-27 | ams_001 | worth it | - | 46c1 | holds |
| 08-27 | Baarn | tree sent in | 4 chars, read it in the database | d4e6 | holds |
| 08-28 | - | Super | - | d4e6 | - |

- 31 of these 39 came from one account (d4e6). At this volume that is almost certainly our own testing rather than readers, and it should be read that way until somebody checks the rows.

**The funnel, as rates**
- Seen to clicked: 2.1% (257 of 12279) vs 2.4% the fortnight before
- Pages per visit: 1.6 (1230 visits, 1920 pageviews since 2026-08-08)
- Visits that did something: 7.2% (89 actions on 1230 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-19 | 18 | 806 | 2.2% | 17.0 |
| 08-20 | 17 | 1022 | 1.7% | 21.5 |
| 08-21 | 18 | 913 | 2.0% | 19.9 |
| 08-22 | 17 | 1030 | 1.7% | 19.9 |
| 08-23 | 15 | 958 | 1.6% | 16.2 |
| 08-24 | 28 | 998 | 2.8% | 15.9 |
| 08-25 | 19 | 1108 | 1.7% | 20.1 |
| 08-26 | 24 | 1144 | 2.1% | 18.7 |
| 08-27 | 15 | 1005 | 1.5% | 18.9 |
| 08-28 *partial* | 19 | 699 | 2.7% | 15.2 |
| **window** | **190** | **9683** | **2.0%** | |
- Top queries (10d): dutch elm amsterdam (i52, p5); ancient tree (i13, p41); ancient trees (i20, p27); e bordeaux? (i1, p1); italian trees in rome (i3, p11)
- Top pages (10d): /prague (c8/i137); /seville (c7/i124); / (c6/i101); /lisbon (c6/i165); /amsterdam/elm-of-elsenhoeve (c4/i55)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - '"oldest of its species" owl park' (i10, p9)
    - 'ahuehuete tree' (i6, p13)
    - '"400 years old as of 2023" tree' (i1, p7)
    - '"oldest of its species" "park" tree' (i1, p10)
    - '"stands nearly 20 metres" tower medieval' (i1, p8)
    - '10 feet tall trees' (i1, p58)
    - '800 year old tree' (i1, p10)
    - '99 yew trees' (i1, p58)
    - and 2 more

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| rome | 5 | 390 | 1.3% | 10.6 | 2.3% | trees in rome (i23, p14) |
| amsterdam | 11 | 377 | 2.9% | 10.7 | 2.3% | dutch elm amsterdam (i26, p4) |
| tenerife | 0 | 243 | 0.0% | 10.7 | 2.3% | drago milenario (i24, p10) |
| milan | 0 | 224 | 0.0% | 9.4 | 2.8% | "oldest of its species" ginkgo park (i11, p6) |
| lisbon | 8 | 215 | 3.7% | 8.4 | 3.3% | oldest tree in lisbon (i3, p9) |
| copenhagen | 7 | 206 | 3.4% | 12.3 | 1.7% | trees in copenhagen (i30, p17) |
| singapore | 4 | 188 | 2.1% | 13.1 | 1.6% | oldest tree in singapore (i21, p10) |
| brisbane | 3 | 187 | 1.6% | 16.2 | 1.1% | the big macadamia nut (i10, p67) |
| barcelona | 4 | 185 | 2.2% | 10.4 | 2.4% | barcelona trees (i6, p8) |
| bath | 3 | 175 | 1.7% | 8.2 | 3.4% | how old is the tree in abbey green bath (i7, p9) |
| seville | 9 | 160 | 5.6% | 10.2 | 2.4% | seville spain orange trees (i1, p41) |
| prague | 8 | 155 | 5.2% | 8.0 | 3.5% | - |
| london | 1 | 153 | 0.7% | 26.4 | 0.5% | great trees of london (i2, p54) |
| vienna | 0 | 152 | 0.0% | 9.3 | 2.8% | alter (i1, p3) |
| malaga | 3 | 148 | 2.0% | 12.9 | 1.6% | árboles históricos de málaga (i11, p81) |
| paris | 3 | 141 | 2.1% | 20.5 | 0.8% | palm trees in paris (i3, p61) |
| madrid | 0 | 128 | 0.0% | 15.7 | 1.1% | oldest tree in madrid (i3, p9) |
| florence | 1 | 125 | 0.8% | 10.0 | 2.5% | florence tree (i6, p9) |
| madeira | 1 | 116 | 0.9% | 8.2 | 3.4% | dragon tree madeira (i6, p10) |
| naples | 2 | 116 | 1.7% | 12.2 | 1.8% | naples tree (i2, p5) |
| crete | 0 | 108 | 0.0% | 10.5 | 2.3% | 2000 years old olive tree (i2, p13) |
| palermo | 1 | 107 | 0.9% | 7.2 | 3.9% | oldest tree in palermo (i2, p12) |
| seoul | 0 | 99 | 0.0% | 13.2 | 1.6% | seoul trees (i7, p9) |
| brussels | 4 | 95 | 4.2% | 9.7 | 2.7% | belgian trees (i1, p36) |
| venice | 2 | 86 | 2.3% | 9.6 | 2.7% | trees in venice (i3, p7) |
| palma-de-mallorca | 0 | 86 | 0.0% | 6.9 | 4.1% | oldest olive tree in palma (i2, p10) |
| montreal | 3 | 83 | 3.6% | 10.8 | 2.2% | century trees (i3, p53) |
| toronto | 1 | 82 | 1.2% | 9.9 | 2.5% | big red oak (i13, p7) |
| edinburgh | 2 | 80 | 2.5% | 14.7 | 1.3% | oldest tree in edinburgh (i2, p10) |
| fukuoka | 3 | 76 | 3.9% | 11.2 | 2.1% | largest camphor tree (i1, p59) |
| new-york | 2 | 71 | 2.8% | 18.8 | 0.9% | - |
| las-vegas | 0 | 71 | 0.0% | 25.8 | 0.6% | vegas trees (i49, p33) |
| sardinia | 0 | 69 | 0.0% | 7.3 | 3.8% | baltolu sardinia (i6, p7) |
| valencia | 2 | 68 | 2.9% | 8.6 | 3.2% | ficus centenarios de la glorieta (i2, p11) |
| dublin | 2 | 65 | 3.1% | 13.7 | 1.5% | oldest tree in ireland (i1, p62) |
| reykjavik | 1 | 61 | 1.6% | 19.4 | 0.8% | oldest tree in iceland (i5, p8) |
| nijmegen | 0 | 60 | 0.0% | 7.1 | 3.9% | hertogplein nijmegen maps (i1, p6) |
| krakow | 2 | 59 | 3.4% | 11.3 | 2.0% | kossaka (i1, p10) |
| bologna | 0 | 52 | 0.0% | 6.4 | 4.6% | - |
| cambridge | 0 | 50 | 0.0% | 33.6 | 0.4% | newton's apple tree (i5, p46) |
| portland | 1 | 49 | 2.0% | 8.4 | 3.3% | - |
| geneva | 3 | 48 | 6.2% | 10.6 | 2.3% | sixty tree (i1, p9) |
| alicante | 0 | 48 | 0.0% | 7.0 | 4.0% | ficus alicante (i4, p9) |
| dubrovnik | 1 | 46 | 2.2% | 7.7 | 3.6% | trsteno plane tree (i2, p12) |
| hilo | 0 | 45 | 0.0% | 63.1 | 0.4% | loulu palm (i26, p88) |
| kyoto | 1 | 44 | 2.3% | 6.3 | 4.7% | yoshimine-dera (i1, p1) |
| athens | 3 | 43 | 7.0% | 12.9 | 1.6% | old plane tree (i1, p35) |
| perth | 0 | 43 | 0.0% | 13.9 | 1.4% | jarra tree (i2, p38) |
| the-hague | 1 | 42 | 2.4% | 6.9 | 4.1% | old tree (i1, p9) |
| chicago | 3 | 41 | 7.3% | 9.3 | 2.9% | wooded grove (i1, p48) |
| boston | 1 | 41 | 2.4% | 25.4 | 0.6% | trees in boston (i2, p54) |
| greece | 1 | 41 | 2.4% | 32.2 | 0.4% | greek trees (i5, p36) |
| istanbul | 2 | 41 | 4.9% | 6.3 | 4.7% | a ten ile ma (i1, p2) |
| oslo | 2 | 41 | 4.9% | 12.7 | 1.7% | "oldest ginkgo tree" park motto (i1, p5) |
| leiden | 0 | 41 | 0.0% | 11.2 | 2.1% | "oldest of its species" ginkgo park (i7, p9) |
| bordeaux | 2 | 40 | 5.0% | 8.3 | 3.4% | sequoia bordeaux (i2, p9) |
| cyprus | 1 | 40 | 2.5% | 8.1 | 3.5% | oldest tree in cyprus (i5, p10) |
| mexico-city | 2 | 40 | 5.0% | 9.8 | 2.6% | ahuehuete (i1, p35) |
| porto | 2 | 39 | 5.1% | 6.1 | 4.9% | alameda dos platanos (i9, p7) |
| vilnius | 4 | 39 | 10.3% | 6.9 | 4.1% | willow tree in lithuanian (i3, p9) |
| bristol | 2 | 38 | 5.3% | 19.1 | 0.9% | bristol trees (i2, p55) |
| sydney | 0 | 38 | 0.0% | 7.2 | 3.9% | the wishing tree sydney (i4, p8) |
| berlin | 0 | 37 | 0.0% | 18.5 | 0.9% | berlin tree map (i1, p10) |
| munich | 0 | 37 | 0.0% | 8.1 | 3.5% | kirchtruderinger straße (i1, p8) |
| groningen | 0 | 36 | 0.0% | 25.6 | 0.6% | big five groningen (i2, p84) |
| washington-dc | 1 | 35 | 2.9% | 22.8 | 0.7% | survey lodge ranger station (i5, p11) |
| tokyo | 0 | 35 | 0.0% | 6.2 | 4.8% | - |
| budapest | 1 | 33 | 3.0% | 7.3 | 3.8% | - |
| cagliari | 0 | 33 | 0.0% | 4.2 | 7.8% | età (i1, p2) |
| seattle | 2 | 32 | 6.2% | 6.6 | 4.4% | - |
| bratislava | 2 | 30 | 6.7% | 9.0 | 3.0% | - |
| padua | 0 | 29 | 0.0% | 8.1 | 3.4% | - |
| aarhus | 1 | 28 | 3.6% | 8.0 | 3.5% | happy pig (i2, p10) |
| potsdam | 0 | 28 | 0.0% | 13.3 | 1.5% | jagdschloss glienicke (i1, p12) |
| lyon | 1 | 27 | 3.7% | 13.9 | 1.4% | antoine rivoire (i2, p8) |
| helsinki | 0 | 27 | 0.0% | 6.2 | 4.8% | in helsinki (i1, p4) |
| sintra | 1 | 26 | 3.8% | 6.5 | 4.5% | - |
| glasgow | 0 | 26 | 0.0% | 8.3 | 3.3% | - |
| guimaraes | 0 | 26 | 0.0% | 13.0 | 1.6% | pine tree portugal (i4, p18) |
| trieste | 0 | 26 | 0.0% | 7.2 | 3.9% | piazza hortis (i4, p10) |
| cork | 1 | 25 | 4.0% | 15.0 | 1.2% | oldest tree in ireland (i5, p14) |
| utrecht | 1 | 25 | 4.0% | 11.5 | 2.0% | zocher utrecht (i2, p22) |
| cordoba | 0 | 25 | 0.0% | 39.4 | 0.4% | gingko garden (i1, p56) |
| quebec-city | 0 | 25 | 0.0% | 10.9 | 2.2% | avenue elm (i1, p34) |
| strasbourg | 2 | 24 | 8.3% | 6.5 | 4.5% | - |
| york | 1 | 24 | 4.2% | 8.3 | 3.4% | - |
| sorrento | 1 | 23 | 4.3% | 21.4 | 0.7% | - |
| zurich | 1 | 23 | 4.3% | 13.6 | 1.5% | - |
| tallinn | 0 | 23 | 0.0% | 8.0 | 3.5% | - |
| canada | 1 | 22 | 4.5% | 20.2 | 0.8% | oldest tree in canada (i3, p21) |
| warsaw | 1 | 22 | 4.5% | 14.0 | 1.4% | poland national tree (i1, p55) |
| cadiz | 0 | 21 | 0.0% | 8.0 | 3.5% | - |
| new-orleans | 0 | 21 | 0.0% | 25.2 | 0.6% | anseman oak (i2, p10) |
| turin | 0 | 21 | 0.0% | 5.0 | 6.9% | alberi monumentali (i1, p8) |
| nara | 1 | 19 | 5.3% | 11.2 | 2.1% | - |
| hong-kong | 0 | 19 | 0.0% | 6.5 | 4.5% | - |
| nice | 0 | 19 | 0.0% | 7.0 | 4.0% | promenade des anglais palm trees (i1, p5) |
| nuremberg | 0 | 19 | 0.0% | 6.1 | 4.9% | - |
| toulouse | 3 | 18 | 16.7% | 5.2 | 6.6% | - |
| graz | 1 | 18 | 5.6% | 8.4 | 3.3% | oak (i2, p8) |
| arnhem | 0 | 16 | 0.0% | 10.0 | 2.5% | musispark arnhem (i1, p4) |
| lucca | 1 | 15 | 6.7% | 6.9 | 4.1% | lucca tree (i1, p10) |
| maastricht | 1 | 15 | 6.7% | 8.1 | 3.5% | trees (i1, p8) |
| oxford | 2 | 15 | 13.3% | 7.8 | 3.6% | - |
| bangkok | 0 | 15 | 0.0% | 10.7 | 2.3% | - |
| caserta | 0 | 15 | 0.0% | 22.9 | 0.7% | parchi caserta (i1, p1) |
| eindhoven | 0 | 15 | 0.0% | 6.6 | 4.4% | beukenboom (i1, p3) |
| austin | 0 | 14 | 0.0% | 14.1 | 1.4% | antebellum oaks (i1, p54) |
| belgrade | 0 | 14 | 0.0% | 17.1 | 1.0% | - |
| poznan | 1 | 13 | 7.7% | 21.8 | 0.7% | - |
| catania | 0 | 13 | 0.0% | 6.9 | 4.1% | - |
| ljubljana | 1 | 12 | 8.3% | 17.9 | 1.0% | - |
| australia | 0 | 12 | 0.0% | 22.5 | 0.7% | oldest tree in australia (i3, p42) |
| haarlem | 0 | 12 | 0.0% | 22.9 | 0.7% | noble tree (i2, p58) |
| oahu | 0 | 12 | 0.0% | 7.0 | 4.0% | - |
| split | 0 | 12 | 0.0% | 8.6 | 3.2% | mediterranean cypress croatia (i2, p8) |
| verona | 0 | 12 | 0.0% | 6.3 | 4.7% | - |
| braga | 1 | 11 | 9.1% | 9.6 | 2.7% | santa tecla braga (i1, p1) |
| delft | 2 | 11 | 18.2% | 23.3 | 0.7% | - |
| emmen | 0 | 11 | 0.0% | 6.0 | 5.0% | rensenpark emmen former zoo park (i1, p6) |
| perugia | 0 | 11 | 0.0% | 6.5 | 4.5% | che albero é (i1, p2) |
| portugal | 0 | 11 | 0.0% | 62.5 | 0.4% | portugal trees (i2, p71) |
| dallas | 1 | 10 | 10.0% | 7.6 | 3.7% | centennial tree (i1, p18) |
| bilbao | 0 | 10 | 0.0% | 7.0 | 4.0% | - |
| brno | 0 | 10 | 0.0% | 6.6 | 4.4% | - |
| frankfurt | 0 | 10 | 0.0% | 5.0 | 7.0% | what tree is this (i1, p6) |
| setubal | 0 | 10 | 0.0% | 8.4 | 3.3% | - |

**The language test** (Contract J v1.13: a translated set should pass its English twin's impressions within four weeks of indexing):

| Lang | City | Clicks | Impressions | Position | English twin |
|---|---|---:|---:|---:|---:|
| es | malaga | 1 | 143 | 12.4 | 148 |
| de | berlin | 0 | 52 | 15.2 | 37 |
| ja | kyoto | 1 | 36 | 9.9 | 44 |
| de | vienna | 1 | 31 | 6.7 | 152 |
| it | rome | 3 | 29 | 8.8 | 390 |
| pt | lisbon | 2 | 29 | 8.6 | 215 |
| pt | porto | 0 | 28 | 5.7 | 39 |
| ja | tokyo | 0 | 27 | 10.8 | 35 |
| it | palermo | 0 | 24 | 9.5 | 107 |
| pt | sintra | 1 | 18 | 14.9 | 26 |
| es | cadiz | 1 | 14 | 15.4 | 21 |
| nl | nijmegen | 0 | 14 | 8.0 | 60 |
| es | barcelona | 0 | 13 | 11.9 | 185 |
| es | madrid | 0 | 10 | 7.8 | 128 |
| es | tenerife | 0 | 9 | 31.0 | 243 |
| fr | geneva | 0 | 9 | 25.2 | 48 |
| nl | amsterdam | 0 | 9 | 3.1 | 377 |
| it | milan | 0 | 7 | 15.1 | 224 |
| fr | nice | 0 | 6 | 27.5 | 19 |
| de | zurich | 1 | 4 | 11.8 | 23 |
| ja | osaka | 0 | 4 | 17.0 | 7 |

**Cities seen but never clicked** (60+ impressions, zero clicks, with what they are actually shown for):

- tenerife (i102): drago milenario (i24, p10); pino gordo (i11, p22); pino gordo tenerife (i8, p10); el drago milenario (i8, p10)
- Seen, not clicked: /rome (c1/i108, 0.9%) for trees in rome (i23, p14); rome trees (i18, p12); famous trees in rome (i9, p8)
- Seen, not clicked: /tenerife/el-drago-milenario (c0/i73, 0.0%) for drago milenario (i24, p10); el drago milenario (i8, p10); tenerife oldest tree (i5, p10)
- Seen, not clicked: /species/strawberry-tree (c0/i58, 0.0%) for strawberry tree (i19, p69); arbutus strawberry tree (i4, p68); strawberry trees (i3, p75)
- Seen, not clicked: /species/osage-orange (c0/i57, 0.0%) for osage orange (i6, p85); osage orange tree (i4, p84); osage orange trees (i3, p83)
- Seen, not clicked: /las-vegas (c0/i49, 0.0%) for vegas trees (i49, p33)
- Seen, not clicked: /copenhagen (c0/i42, 0.0%) for trees in copenhagen (i30, p17); copenhagen trees (i10, p20); trees near me (i1, p75)
- Seen, not clicked: / (c1/i35, 2.9%) for ancient trees (i18, p31); ancient tree (i8, p58); old tree near me (i2, p4)
- Seen, not clicked: /species/american-elm (c0/i33, 0.0%) for american elm (i13, p84); elm american (i3, p85); where do elm trees grow (i2, p78)

**Climbing** (this ten days against the ten before it)

| Page | Impressions | Change | Position | Moved | Clicks |
|---|---:|---:|---:|---:|---:|
| /rome | 324 | +160 | 11.4 | +6.4 | +1 |
| /milan | 201 | +132 | 8.9 | +0.9 | +0 |
| /copenhagen | 151 | +122 | 12.4 | - | +2 |
| /seville | 124 | +108 | 10.2 | -2.9 | +7 |
| /lisbon | 165 | +75 | 7.9 | +1.6 | +4 |
| /madrid | 114 | +75 | 16.7 | -7.9 | +0 |
| /malaga | 134 | +55 | 13.7 | +6.3 | +2 |
| /bath/plane-tree-of-abbey-green | 147 | +51 | 8.9 | -0.4 | +1 |

**Newly ranking** (no impressions at all ten days ago)

| Page | Impressions | Clicks | Position |
|---|---:|---:|---:|
| /tenerife/el-drago-milenario | 132 | 0 | 10.9 |
| /species/osage-orange | 106 | 0 | 80.4 |
| /species/strawberry-tree | 83 | 0 | 67.8 |
| /species/american-elm | 62 | 0 | 78.4 |
| /amsterdam/elm-of-elsenhoeve | 55 | 4 | 5.8 |
| /madeira/witch-tree-of-fanal | 53 | 0 | 9.4 |

**Slipping**

| Page | Impressions | Change | Position | Moved |
|---|---:|---:|---:|---:|
| /boston | 15 | -26 | 35.1 | -18.2 |
| /lyon | 16 | -19 | 18.9 | -3.6 |
| /sintra | 18 | -12 | 6.5 | -0.9 |
| /washington-dc | 18 | -12 | 23.6 | -6.2 |

- New queries this window: italian trees in rome (i3).

**Who they are**
Audience, 28 days of search (363 clicks, 16784 impressions):
- Countries: usa c64/i3743; gbr c42/i2019; nld c27/i795; esp c19/i1014; deu c18/i567
- Devices: MOBILE c249/i9009; DESKTOP c109/i7623; TABLET c5/i152
- Landing pages: / c18/i174; /prague c16/i297; /lisbon c10/i310; /seville c8/i165; /amsterdam c6/i387

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-21 | 40 | 80 |
| 08-22 | 90 | 120 |
| 08-23 | 70 | 120 |
| 08-24 | 10 | 20 |
| 08-25 | 60 | 70 |
| 08-26 | 80 | 110 |
| 08-27 | 60 | 140 |
| 08-28 | 120 | 170 |
| **window** | **530** | **830** |
- Top paths: / (120); /copenhagen (40); /nijmegen/wilhelminaboom-of-hertogplein (30); /explore (30); /brussels (20); /brisbane/hoop-pine (20); /melbourne/remnant-river-red-gum-of-edinburgh-gardens (20); /cities (20); /athens/holm-oak-of-the-national-garden (20); /sponsor (20); /amsterdam (20); /madrid (10)
- Referrers: (direct) (350); ancienttrees.app (300); www.google.com (180)
- Moved between our own pages: 300 of 830 pageviews (36%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: US (110); NL (110); AU (80); GB (70); DE (70)
- Devices: desktop (420); mobile (390); tablet (20)
- Page load (8d): p50 889ms, p90 3611ms

Links: external referrers (a link somebody actually clicked): none yet
AI: arrivals from an assistant that cited us: none yet


**What the night shift did**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 08-28T19:45 | 28.1 | 0 | 8 | 24 | - |
| 08-29T02:35 | 27.9 | 8 | 7 | 18 | Buenos Aires +4, Dresden +4 |
| **2 runs** | **56** | **8** | **15** | | |

- 1 of 2 produced no trees; 18 to 24 commands refused per run; 1 wrote nothing to LOG.md.

**What they made**

- Finish Brisbane's standing verify claim (0 trees, 3 candidates recorded); release Girona rather than dispatch a thin pass; two photo sweeps
- Add Buenos Aires and Dresden: 4 trees each, finishing a stalled write pass
- Buenos Aires verify pass: 4 trees delivered to research, release claim
- Dresden verify pass: 4 trees delivered to research, release claim
- Photo queue: free API sweep, --recheck
- Fix stale UI test assertion after CollectIntro title copy change
- Fresh-eyes review: 2 finding(s)

Machine: 10 chain attempts yesterday, 6 got real work time (~226 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 19 clicks and 699 impressions on Google's freshest day (day before: c15/i1005). Directional at best; no strategic conclusions from these volumes.

## 2026-08-27 (previous UTC day)

**Today: a waitlist arrived today (14 total); 1 tree submission and 1 feedback report arrived yesterday (24 total).**

**Did the product happen**
- app-cta:     2 yesterday, last yesterday
- search-home: 1 yesterday, last yesterday
- waitlist-submit: 1 yesterday, last today
- walks-app:   1 yesterday, last today
- beacon-fix-verify: 0 yesterday, last 12 days ago
- beacon-test: 0 yesterday, last 12 days ago
- directions:  0 yesterday, last today
- save:        0 yesterday, last 2 days ago
- search-explore: 0 yesterday, last 7 days ago
- signin-link-sent: 0 yesterday, last never
- smoke-test:  0 yesterday, last 27 days ago
- suggestion-submit: 0 yesterday, last 8 days ago
- walk-open:   0 yesterday, last 11 days ago
- walk-start:  0 yesterday, last never
- worthit-not worth it: 0 yesterday, last 11 days ago
- worthit-worth it: 0 yesterday, last never

| Day | Accounts | Waitlist | Saves | Trees sent | Feedback |
|---|---:|---:|---:|---:|---:|
| 08-14 | 0 | 1 | 0 | 0 | 0 |
| 08-15 | 0 | 0 | 0 | 0 | 1 |
| 08-16 | 0 | 0 | 0 | 0 | 0 |
| 08-17 | 0 | 1 | 0 | 0 | 2 |
| 08-18 | 0 | 1 | 2 | 0 | 0 |
| 08-19 | 0 | 1 | 0 | 0 | 0 |
| 08-20 | 0 | 1 | 3 | 0 | 1 |
| 08-21 | 1 | 0 | 0 | 0 | 16 |
| 08-22 | 0 | 0 | 1 | 0 | 0 |
| 08-23 | 0 | 0 | 0 | 0 | 0 |
| 08-24 | 0 | 0 | 0 | 1 | 0 |
| 08-25 | 0 | 1 | 0 | 0 | 0 |
| 08-26 | 0 | 1 | 1 | 0 | 1 |
| 08-27 | 0 | 1 | 0 | 1 | 1 |
| 08-28 | 0 | 1 | 0 | 0 | 0 |
| **14 days** | **1** | **9** | **7** | **2** | **22** |
- Waitlist:    14 total, newest today
- Submissions: 24 total (2 trees sent, 22 feedback), newest yesterday
- Accounts:    4 total, newest 7 days ago

**What readers told us** (14 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 08-15 | prg_007 (The Oak of Cisarsky ostro | not worth it | wrong location | no acct | holds |
| 08-17 | hel_006 (The Meilahti Ancient Pine | not worth it | - | no acct | holds |
| 08-17 | lis_005 (The Tipu of Jardim de São | worth it | - | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-21 | par_001 (The Robinier of Square Re | not worth it | - | no acct | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | report | could not reach it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | worth it | - | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | not worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-24 | Baarn | tree sent in | 4 chars, read it in the database | d4e6 | open_question |
| 08-25 | utr_005 (Onder de Linden) | vote undone | not worth it | d4e6 | - |
| 08-26 | sar_003 (The Olivastro of Santa Ma | worth it | - | d4e6 | - |
| 08-27 | ams_001 | worth it | - | 46c1 | holds |
| 08-27 | Baarn | tree sent in | 4 chars, read it in the database | d4e6 | holds |

- 30 of these 38 came from one account (d4e6). At this volume that is almost certainly our own testing rather than readers, and it should be read that way until somebody checks the rows.

**The funnel, as rates**
- Seen to clicked: 2.1% (248 of 11852) vs 2.3% the fortnight before
- Pages per visit: 1.6 (1110 visits, 1750 pageviews since 2026-08-08)
- Visits that did something: 7.5% (83 actions on 1110 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-18 | 19 | 609 | 3.1% | 15.0 |
| 08-19 | 18 | 806 | 2.2% | 17.0 |
| 08-20 | 17 | 1022 | 1.7% | 21.5 |
| 08-21 | 18 | 913 | 2.0% | 19.9 |
| 08-22 | 17 | 1030 | 1.7% | 19.9 |
| 08-23 | 15 | 958 | 1.6% | 16.2 |
| 08-24 | 28 | 998 | 2.8% | 15.9 |
| 08-25 | 19 | 1108 | 1.7% | 20.1 |
| 08-26 | 24 | 1144 | 2.1% | 18.7 |
| 08-27 *partial* | 10 | 754 | 1.3% | 16.5 |
| **window** | **185** | **9342** | **2.0%** | |
- Top queries (10d): dutch elm amsterdam (i49, p5); italian trees in rome (i2, p12); oldest tree in dc (i2, p33); "400 years old as of 2023" tree (i1, p7); "oldest ginkgo tree" park motto (i1, p5)
- Top pages (10d): /prague (c9/i135); /seville (c6/i107); / (c5/i83); /lisbon (c5/i152); /brussels (c4/i76)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - '"oldest of its species" owl park' (i9, p9)
    - 'ahuehuete tree' (i6, p13)
    - 'oldest tree in dc' (i2, p33)
    - '"400 years old as of 2023" tree' (i1, p7)
    - '"oldest of its species" "park" tree' (i1, p10)
    - '"stands nearly 20 metres" tower medieval' (i1, p8)
    - '800 year old tree' (i1, p10)
    - '99 yew trees' (i1, p58)
    - and 4 more

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| amsterdam | 12 | 373 | 3.2% | 10.6 | 2.3% | dutch elm amsterdam (i22, p4) |
| rome | 4 | 373 | 1.1% | 10.9 | 2.2% | rome trees (i15, p11) |
| tenerife | 0 | 239 | 0.0% | 10.6 | 2.3% | drago milenario (i24, p10) |
| milan | 0 | 214 | 0.0% | 9.6 | 2.7% | "oldest of its species" ginkgo park (i12, p6) |
| lisbon | 7 | 202 | 3.5% | 8.6 | 3.2% | oldest tree in lisbon (i3, p9) |
| copenhagen | 6 | 194 | 3.1% | 11.9 | 1.8% | trees in copenhagen (i28, p17) |
| barcelona | 4 | 192 | 2.1% | 10.1 | 2.5% | barbary thuja (i5, p8) |
| singapore | 4 | 191 | 2.1% | 13.2 | 1.6% | oldest tree in singapore (i21, p10) |
| bath | 2 | 176 | 1.1% | 8.5 | 3.3% | giant plane tree bath (i7, p11) |
| brisbane | 3 | 174 | 1.7% | 16.2 | 1.1% | the big macadamia nut (i9, p68) |
| london | 1 | 156 | 0.6% | 25.6 | 0.6% | london trees (i3, p77) |
| prague | 10 | 153 | 6.5% | 8.0 | 3.5% | - |
| vienna | 0 | 148 | 0.0% | 9.9 | 2.5% | alter (i1, p3) |
| seville | 8 | 146 | 5.5% | 10.6 | 2.3% | seville spain orange trees (i1, p41) |
| madrid | 0 | 145 | 0.0% | 15.4 | 1.2% | oldest tree in madrid (i3, p9) |
| paris | 3 | 138 | 2.2% | 22.1 | 0.7% | palm trees in paris (i3, p61) |
| malaga | 3 | 134 | 2.2% | 13.7 | 1.5% | árboles históricos de málaga (i11, p81) |
| florence | 1 | 124 | 0.8% | 10.5 | 2.3% | florence tree (i6, p9) |
| palermo | 2 | 118 | 1.7% | 8.1 | 3.5% | oldest tree in palermo (i2, p12) |
| naples | 2 | 115 | 1.7% | 11.3 | 2.0% | a tree in naples (i1, p15) |
| madeira | 0 | 108 | 0.0% | 8.3 | 3.3% | dragon tree madeira (i6, p10) |
| brussels | 4 | 105 | 3.8% | 10.5 | 2.3% | belgian trees (i1, p36) |
| seoul | 0 | 98 | 0.0% | 14.3 | 1.3% | seoul tree (i7, p8) |
| crete | 0 | 94 | 0.0% | 10.5 | 2.3% | 2000 years old olive tree (i2, p13) |
| venice | 2 | 88 | 2.3% | 9.7 | 2.6% | trees in venice (i3, p7) |
| montreal | 2 | 80 | 2.5% | 10.9 | 2.2% | century trees (i3, p53) |
| edinburgh | 1 | 78 | 1.3% | 16.0 | 1.1% | oldest tree in edinburgh (i2, p10) |
| palma-de-mallorca | 0 | 76 | 0.0% | 6.7 | 4.3% | oldest olive tree in palma (i2, p10) |
| toronto | 0 | 75 | 0.0% | 10.3 | 2.4% | big red oak (i11, p7) |
| fukuoka | 3 | 73 | 4.1% | 9.4 | 2.8% | kanatake (i1, p76) |
| dublin | 2 | 70 | 2.9% | 13.4 | 1.5% | oldest tree in ireland (i1, p62) |
| new-york | 2 | 69 | 2.9% | 18.9 | 0.9% | - |
| las-vegas | 0 | 65 | 0.0% | 27.6 | 0.5% | vegas trees (i49, p33) |
| nijmegen | 0 | 65 | 0.0% | 7.0 | 4.0% | hertogplein nijmegen maps (i1, p6) |
| valencia | 2 | 64 | 3.1% | 8.6 | 3.2% | ficus centenarios de la glorieta (i2, p11) |
| dubrovnik | 3 | 62 | 4.8% | 7.3 | 3.8% | trsteno plane tree (i2, p12) |
| sardinia | 0 | 61 | 0.0% | 7.7 | 3.6% | baltolu sardinia (i5, p7) |
| reykjavik | 1 | 59 | 1.7% | 20.1 | 0.8% | oldest tree in iceland (i5, p8) |
| cambridge | 0 | 59 | 0.0% | 33.1 | 0.4% | newton's apple tree (i6, p46) |
| krakow | 2 | 57 | 3.5% | 11.2 | 2.1% | plac kossaka krakow (i1, p10) |
| portland | 1 | 50 | 2.0% | 8.5 | 3.3% | - |
| washington-dc | 2 | 50 | 4.0% | 20.0 | 0.8% | survey lodge ranger station (i7, p11) |
| geneva | 3 | 49 | 6.1% | 10.6 | 2.3% | sixty tree (i1, p9) |
| bologna | 0 | 49 | 0.0% | 6.3 | 4.7% | - |
| porto | 2 | 45 | 4.4% | 5.6 | 5.7% | alameda dos platanos (i11, p7) |
| alicante | 1 | 45 | 2.2% | 6.8 | 4.2% | ficus alicante (i4, p9) |
| boston | 1 | 43 | 2.3% | 28.3 | 0.5% | trees in boston (i2, p54) |
| bristol | 2 | 42 | 4.8% | 21.3 | 0.7% | bristol trees (i4, p55) |
| istanbul | 2 | 42 | 4.8% | 6.5 | 4.5% | a ten ile ma (i1, p2) |
| oslo | 1 | 42 | 2.4% | 13.6 | 1.5% | "oldest ginkgo tree" park motto (i1, p5) |
| the-hague | 3 | 41 | 7.3% | 6.7 | 4.3% | old tree (i1, p9) |
| athens | 3 | 39 | 7.7% | 14.1 | 1.4% | old plane tree (i1, p35) |
| chicago | 3 | 39 | 7.7% | 9.3 | 2.8% | wooded grove (i1, p48) |
| hilo | 0 | 39 | 0.0% | 62.3 | 0.4% | loulu palm (i21, p93) |
| bordeaux | 1 | 37 | 2.7% | 8.7 | 3.1% | sequoia bordeaux (i2, p9) |
| berlin | 0 | 37 | 0.0% | 18.6 | 0.9% | berlin tree map (i1, p10) |
| groningen | 0 | 37 | 0.0% | 27.3 | 0.5% | big five groningen (i3, p84) |
| leiden | 0 | 37 | 0.0% | 11.7 | 1.9% | "oldest of its species" ginkgo park (i6, p10) |
| perth | 0 | 37 | 0.0% | 12.9 | 1.6% | oldest tree in perth (i1, p10) |
| budapest | 1 | 36 | 2.8% | 7.7 | 3.7% | - |
| vilnius | 4 | 34 | 11.8% | 7.1 | 4.0% | willow tree in lithuanian (i3, p9) |
| cyprus | 0 | 34 | 0.0% | 8.1 | 3.4% | oldest tree in cyprus (i5, p10) |
| munich | 0 | 34 | 0.0% | 7.9 | 3.5% | - |
| tokyo | 0 | 34 | 0.0% | 6.0 | 5.1% | - |
| greece | 1 | 33 | 3.0% | 31.4 | 0.4% | greek trees (i5, p36) |
| kyoto | 1 | 33 | 3.0% | 6.9 | 4.1% | - |
| cagliari | 0 | 33 | 0.0% | 4.2 | 7.8% | età (i1, p2) |
| padua | 0 | 31 | 0.0% | 7.9 | 3.5% | - |
| bratislava | 2 | 30 | 6.7% | 9.0 | 3.0% | - |
| mexico-city | 0 | 30 | 0.0% | 11.2 | 2.1% | ahuehuete (i1, p35) |
| sintra | 2 | 29 | 6.9% | 6.7 | 4.3% | - |
| seattle | 1 | 29 | 3.4% | 5.7 | 5.6% | - |
| glasgow | 0 | 29 | 0.0% | 8.0 | 3.5% | - |
| helsinki | 0 | 28 | 0.0% | 6.4 | 4.6% | - |
| nice | 0 | 28 | 0.0% | 8.9 | 3.1% | promenade des anglais palm trees (i1, p5) |
| guimaraes | 0 | 27 | 0.0% | 12.6 | 1.7% | pine tree portugal (i4, p18) |
| potsdam | 0 | 27 | 0.0% | 11.4 | 2.0% | jagdschloss glienicke (i1, p12) |
| sydney | 0 | 27 | 0.0% | 7.5 | 3.8% | the wishing tree sydney (i3, p9) |
| lyon | 1 | 26 | 3.8% | 16.5 | 1.1% | antoine rivoire (i2, p8) |
| zurich | 2 | 26 | 7.7% | 13.1 | 1.6% | - |
| cordoba | 0 | 26 | 0.0% | 38.2 | 0.4% | gingko garden (i1, p56) |
| trieste | 0 | 26 | 0.0% | 6.6 | 4.4% | piazza hortis (i3, p9) |
| aarhus | 1 | 25 | 4.0% | 8.0 | 3.5% | happy pig (i2, p10) |
| cork | 1 | 25 | 4.0% | 14.9 | 1.2% | oldest tree in ireland (i4, p15) |
| utrecht | 1 | 25 | 4.0% | 13.3 | 1.5% | ja leuk (i1, p9) |
| york | 1 | 25 | 4.0% | 8.2 | 3.4% | - |
| hong-kong | 0 | 24 | 0.0% | 8.5 | 3.2% | - |
| quebec-city | 0 | 23 | 0.0% | 11.5 | 2.0% | avenue elm (i1, p34) |
| turin | 0 | 23 | 0.0% | 5.3 | 6.3% | alberi monumentali (i1, p8) |
| canada | 1 | 22 | 4.5% | 20.2 | 0.8% | oldest tree in canada (i3, p21) |
| sorrento | 1 | 22 | 4.5% | 21.9 | 0.7% | - |
| strasbourg | 1 | 22 | 4.5% | 6.7 | 4.3% | - |
| warsaw | 1 | 22 | 4.5% | 14.0 | 1.4% | poland national tree (i1, p55) |
| belgrade | 0 | 21 | 0.0% | 15.7 | 1.1% | - |
| tallinn | 0 | 20 | 0.0% | 7.8 | 3.6% | - |
| toulouse | 3 | 17 | 17.6% | 5.4 | 6.2% | - |
| cadiz | 0 | 17 | 0.0% | 8.0 | 3.5% | - |
| maastricht | 1 | 16 | 6.2% | 8.4 | 3.3% | trees (i1, p8) |
| caserta | 0 | 16 | 0.0% | 21.6 | 0.7% | parchi caserta (i1, p1) |
| graz | 1 | 15 | 6.7% | 9.3 | 2.8% | panoramagasse (i1, p5) |
| nara | 1 | 15 | 6.7% | 12.6 | 1.7% | - |
| oxford | 2 | 15 | 13.3% | 7.8 | 3.6% | - |
| haarlem | 0 | 15 | 0.0% | 22.9 | 0.7% | noble tree (i3, p57) |
| lucca | 1 | 14 | 7.1% | 7.1 | 4.0% | lucca tree (i1, p10) |
| new-orleans | 0 | 14 | 0.0% | 23.0 | 0.7% | mcdonogh oak (i2, p10) |
| nuremberg | 0 | 14 | 0.0% | 6.2 | 4.8% | - |
| setubal | 1 | 13 | 7.7% | 7.6 | 3.7% | - |
| austin | 0 | 13 | 0.0% | 11.0 | 2.1% | - |
| bangkok | 0 | 13 | 0.0% | 11.3 | 2.0% | - |
| split | 0 | 13 | 0.0% | 8.4 | 3.3% | mediterranean cypress croatia (i2, p8) |
| verona | 0 | 13 | 0.0% | 7.4 | 3.8% | - |
| ljubljana | 1 | 12 | 8.3% | 17.9 | 1.0% | - |
| oahu | 0 | 12 | 0.0% | 7.0 | 4.0% | - |
| perugia | 0 | 12 | 0.0% | 6.5 | 4.5% | che albero é (i1, p2) |
| delft | 2 | 11 | 18.2% | 23.3 | 0.7% | - |
| bucaco | 0 | 11 | 0.0% | 11.8 | 1.9% | cedro do bussaco (i2, p2) |
| catania | 0 | 11 | 0.0% | 7.2 | 3.9% | - |
| emmen | 0 | 11 | 0.0% | 6.0 | 5.0% | rensenpark emmen former zoo park (i1, p6) |
| portugal | 0 | 11 | 0.0% | 62.5 | 0.4% | portugal trees (i2, p71) |
| stockholm | 0 | 11 | 0.0% | 8.2 | 3.4% | - |
| braga | 1 | 10 | 10.0% | 9.5 | 2.8% | santa tecla braga (i1, p1) |
| arnhem | 0 | 10 | 0.0% | 11.8 | 1.9% | - |
| australia | 0 | 10 | 0.0% | 18.9 | 0.9% | ancient trees in australia (i2, p18) |
| brno | 0 | 10 | 0.0% | 6.6 | 4.4% | - |
| frankfurt | 0 | 10 | 0.0% | 5.0 | 7.0% | what tree is this (i1, p6) |
| poznan | 0 | 10 | 0.0% | 26.2 | 0.6% | - |

**The language test** (Contract J v1.13: a translated set should pass its English twin's impressions within four weeks of indexing):

| Lang | City | Clicks | Impressions | Position | English twin |
|---|---|---:|---:|---:|---:|
| es | malaga | 1 | 152 | 12.1 | 134 |
| de | berlin | 0 | 43 | 15.5 | 37 |
| it | rome | 2 | 25 | 9.5 | 373 |
| pt | porto | 0 | 25 | 5.7 | 45 |
| de | vienna | 1 | 23 | 7.0 | 148 |
| ja | kyoto | 1 | 23 | 11.3 | 33 |
| pt | lisbon | 1 | 20 | 9.9 | 202 |
| it | palermo | 0 | 18 | 9.8 | 118 |
| ja | tokyo | 0 | 18 | 8.9 | 34 |
| es | barcelona | 0 | 13 | 11.9 | 192 |
| nl | nijmegen | 0 | 13 | 7.8 | 65 |
| pt | sintra | 1 | 12 | 19.2 | 29 |
| es | cadiz | 1 | 11 | 12.7 | 17 |
| es | madrid | 0 | 9 | 7.8 | 145 |
| it | milan | 0 | 7 | 15.1 | 214 |
| nl | amsterdam | 0 | 7 | 2.7 | 373 |
| fr | nice | 0 | 5 | 32.8 | 28 |
| de | zurich | 1 | 4 | 11.8 | 26 |
| es | tenerife | 0 | 3 | 19.3 | 239 |
| fr | geneva | 0 | 3 | 32.7 | 49 |
| ja | osaka | 0 | 2 | 4.0 | 7 |

**Cities seen but never clicked** (60+ impressions, zero clicks, with what they are actually shown for):

- tenerife (i100): drago milenario (i24, p10); pino gordo (i10, p23); pino gordo tenerife (i8, p10); el drago milenario (i8, p10)
- Seen, not clicked: /rome (c1/i91, 1.1%) for rome trees (i15, p11); trees in rome (i13, p18); trees in rome italy (i8, p17)
- Seen, not clicked: /tenerife/el-drago-milenario (c0/i73, 0.0%) for drago milenario (i24, p10); el drago milenario (i8, p10); tenerife oldest tree (i5, p10)
- Seen, not clicked: /species/osage-orange (c0/i51, 0.0%) for osage orange (i6, p85); osage orange tree (i4, p84); osage orange trees (i3, p83)
- Seen, not clicked: /las-vegas (c0/i49, 0.0%) for vegas trees (i49, p33)
- Seen, not clicked: /species/strawberry-tree (c0/i47, 0.0%) for strawberry tree (i17, p68); strawberry tree flowers (i3, p60); arbutus strawberry tree (i3, p68)
- Seen, not clicked: /copenhagen (c0/i37, 0.0%) for trees in copenhagen (i28, p17); copenhagen trees (i8, p20); trees near me (i1, p75)
- Seen, not clicked: /bath/plane-tree-of-abbey-green (c0/i33, 0.0%) for the giant plane tree bath (i7, p11); how old is the tree in abbey green bath (i7, p9); giant plane tree bath (i7, p11)
- Seen, not clicked: /species/american-elm (c0/i33, 0.0%) for american elm (i13, p84); elm american (i3, p85); where do elm trees grow (i2, p78)

**Climbing** (this ten days against the ten before it)

| Page | Impressions | Change | Position | Moved | Clicks |
|---|---:|---:|---:|---:|---:|
| /rome | 305 | +156 | 11.8 | +6.5 | +0 |
| /milan | 192 | +139 | 9.1 | +0.7 | +0 |
| /copenhagen | 139 | +116 | 11.9 | -0.5 | +1 |
| /madrid | 126 | +99 | 15.9 | -7.2 | +0 |
| /seville | 107 | +88 | 10.1 | -3.1 | +6 |
| /bath/plane-tree-of-abbey-green | 153 | +71 | 9.0 | -0.9 | +1 |
| /barcelona | 150 | +70 | 9.2 | -1.1 | +3 |
| /lisbon | 152 | +59 | 8.2 | +1.4 | +2 |

**Newly ranking** (no impressions at all ten days ago)

| Page | Impressions | Clicks | Position |
|---|---:|---:|---:|
| /tenerife/el-drago-milenario | 132 | 0 | 10.9 |
| /species/osage-orange | 97 | 0 | 79.7 |
| /species/strawberry-tree | 68 | 0 | 67.3 |
| /species/american-elm | 61 | 0 | 78.3 |
| /las-vegas | 53 | 0 | 31.1 |
| /madeira/witch-tree-of-fanal | 52 | 0 | 9.3 |

**Slipping**

| Page | Impressions | Change | Position | Moved |
|---|---:|---:|---:|---:|
| /geneva | 16 | -39 | 12.8 | -2.8 |
| /lyon | 16 | -20 | 22.4 | -8.5 |
| /boston | 18 | -19 | 36.0 | -20.9 |
| /sintra | 21 | -7 | 6.8 | -1.6 |

- New queries this window: dutch elm amsterdam (i49).

**Who they are**
Audience, 28 days of search (341 clicks, 16064 impressions):
- Countries: usa c62/i3581; gbr c36/i1941; nld c27/i761; deu c18/i545; esp c17/i977
- Devices: MOBILE c233/i8646; DESKTOP c104/i7269; TABLET c4/i149
- Landing pages: / c17/i155; /prague c16/i295; /lisbon c9/i304; /seville c7/i150; /amsterdam c6/i384

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-20 | 110 | 180 |
| 08-21 | 40 | 80 |
| 08-22 | 90 | 120 |
| 08-23 | 70 | 120 |
| 08-24 | 10 | 20 |
| 08-25 | 60 | 70 |
| 08-26 | 80 | 110 |
| 08-27 | 60 | 140 |
| **window** | **520** | **840** |
- Top paths: / (90); /amsterdam (70); /copenhagen (40); /explore (40); /nijmegen/wilhelminaboom-of-hertogplein (30); /brussels (20); /paris (20); /toulouse/hackberry-of-place-saint-georges (20); /cities (20); /athens/holm-oak-of-the-national-garden (20); /sponsor (20); /brisbane/hoop-pine (10)
- Referrers: (direct) (370); ancienttrees.app (320); www.google.com (150)
- Moved between our own pages: 320 of 840 pageviews (38%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: NL (170); US (140); DE (70); GB (60); AU (50)
- Devices: desktop (480); mobile (340); tablet (20)
- Page load (8d): p50 815ms, p90 3611ms

Links: external referrers (a link somebody actually clicked): none yet
AI: arrivals from an assistant that cited us: none yet


**What the night shift did**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 08-28T02:06 | 19.8 | 0 | 11 | 20 | - |
| 08-28T05:28 | 12.6 | 0 | 5 | 18 | - |
| 08-28T08:56 | 0.1 | 0 | 0 | - | - |
| 08-28T08:59 | 0.1 | 0 | 0 | - | - |
| **4 runs** | **33** | **0** | **16** | | |

- 4 of 4 produced no trees; 18 to 20 commands refused per run; 4 wrote nothing to LOG.md.

**What they made**

- Weekly analysis
- Remove stale verified-writer files whose trees already shipped
- Sintra deepen pass: register reconfirmed exhausted, Grande Maior nickname resolved as sin_003 duplicate
- Photo API sweep: 40 photo-less trees checked, several new candidates queued
- Fix EXIF orientation on Porto ginkgo photo, unblocking deploy
- LOG.md: Wroclaw +1, Munich +1, git push still blocked
- Munich +1: a red oak held only for missing an age
- Wroclaw +1 (Witness Plane); Zaragoza, Brno, Trento confirmed clean
- LOG.md: Warsaw +2, three register cities scouted, git push blocked
- Warsaw +2 (Botanical Garden pairs); Rome checked, three register scouts recorded

Machine: 2 chain attempts yesterday, 2 got real work time (~158 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 10 clicks and 754 impressions on Google's freshest day (day before: c24/i1144). Directional at best; no strategic conclusions from these volumes.

## Weekly analysis 2026-08-28

Fifth weekly analysis. The scheduled 08-24 run failed silently (health.py's
rung 2 caught it this morning) so this covers the two weeks since the last
one, comparing 2026-08-21 to 2026-08-27 against 2026-08-14 to 2026-08-20,
using the latest-settled Search Console figure for each date.

**Scorecard**

| Week ending | Impressions | Clicks | CTR | Visits (beacon) | Pageviews (beacon) | Directions/visit | App-CTA | Waitlist total | Submissions total |
|---|---|---|---|---|---|---|---|---|---|
| 2026-08-16 | 3,457 | 81 | 2.3% | 410 | 560 | 0.0% (0 of 410) | 0 (0 of 410) | 6 real | 1 real |
| 2026-08-20 | 4,941 | 115 | 2.3% | 410 | 640 | n/a (pre-fix, not comparable) | n/a (pre-fix, not comparable) | 10 | 6 |
| 2026-08-27 | 6,810 (still settling) | 129 (still settling) | 1.9% | 410 | 660 | 1.2% (5 of 410) | 10 (2.4% of 410) | 13 | 24 (18 landed in one day) |

**What moved:**
1. Impressions rose 4,941 to 6,810 week over week (+38%, and the newest day
   is still backfilling upward the way 08-24 did, from 730 to 998 three days
   later). Clicks rose less, 115 to 129 (+12%, also understated for the same
   reason), so CTR fell 2.3% to 1.9% and average daily position worsened
   from about 15.6 to about 18.1. More pages are being seen; fewer of them
   convert.
2. Malaga's chronic 0%-CTR problem, flagged in three straight prior weekly
   analyses (08-08, 08-10, 08-17), looks resolved: 2.3% CTR this window on
   133 impressions, the same shape as Rome's earlier fix. The same problem
   has now grown on three other cities: Milan (0%, 211 impressions, position
   9.6, unmoved since at least 08-20), Vienna (0%, 146 impressions, down
   from 3.5% CTR two weeks ago at the same position 10.0) and Madrid (0%,
   145 impressions, up from 78 two weeks ago, still 0%).
3. Beacon visits held flat at 410 both this week and last; pageviews barely
   moved (640 to 660). Search impressions growing 38% did not turn into
   more visits this window.
4. First fully clean week for the click-tracking fix from 08-20 (directions,
   app-cta and walks-app were all double-counted before that date, so the
   prior week's figures are not comparable): 5 directions clicks and 10
   app-cta clicks across 410 visits, 1.2% and 2.4% of visits respectively.
5. The submissions total jumped from 6 to 24, but 18 of those rows arrived
   in one day (08-21) from a single account (d4e6) voting worth-it/not-worth-it
   repeatedly on a handful of trees, already flagged in the daily entry as
   almost certainly internal testing rather than reader activity.

**Suggestions, ranked:**
1. **[run]** Apply the diagnostic that fixed Rome and appears to have fixed
   Malaga (check P2 answer-first wording and the title/meta against the
   actual query) to Milan, Vienna and Madrid. All three now show the same
   shape: real impressions (145-211) at reasonable positions (9.6-15.4) and
   a flat 0% CTR, and Vienna's is a regression from 3.5% two weeks ago
   rather than a page that was never converting.
2. **[run]** Tenerife's /el-drago-milenario is newly ranking (position
   10.5, 237 impressions this window, was 0 two windows ago) but converting
   at 0%, the same early shape Rome and Malaga had before they were fixed.
   Worth a look now rather than after it has sat at 0% for three weekly
   analyses like the others did.
3. **[FOR HIDDE]** GO_TO_MARKET.md's Phase 0 checkpoint, "review at the end
   of August 2026," lands this week. Its own healthy bar (impressions and
   clicks growing week over week into the tens) reads as met at current
   volumes (roughly 1,000 impressions and 18 clicks a day). What it does
   not show growing is beacon visits, flat at 410 two weeks running. Worth
   a conscious decision per that document rather than letting the date pass
   unremarked, since the document says the choice should be made with
   numbers on the table rather than by drift.
4. **[run]** 'alameda dos platanos' (Porto's plane avenue) has now shown up
   as an unserved content lead in three straight windows (8 impressions on
   08-20, 15 on 08-24, 11 on 08-27) despite LOG.md recording a 08-26 merge
   of Porto's duplicate plane-avenue pages that was meant to fix exactly
   this. Worth confirming the merged page's title actually carries this
   phrase; the query has not moved since the merge.
5. **[sessie]** Check whether the worsening average position (15.6 to 18.1)
   is dilution from new pages ranking, which DATA.md's own note says is
   normal, or genuine slippage on established pages: Boston (-19
   impressions, position down 20.9) and Geneva (-39 impressions, position
   down 2.8) both appear in this window's "Slipping" table, and Boston's
   drop is large enough that it is worth a direct look rather than
   assuming dilution.

**Watch next week:** whether Milan, Vienna and Madrid's CTR responds to any
title/meta fix, whether beacon visits break out of the 410-visits-a-week
plateau they have held for two windows running, and whether 08-27's
partial figures settle upward the way 08-24's did.

## 2026-08-26 (previous UTC day)

**Today: a waitlist arrived today (13 total); 1 tree submission and 2 feedback reports arrived today (24 total).**

**Did the product happen**
- directions:  3 yesterday, last yesterday
- app-cta:     1 yesterday, last today
- save:        1 yesterday, last yesterday
- waitlist-submit: 1 yesterday, last today
- beacon-fix-verify: 0 yesterday, last 11 days ago
- beacon-test: 0 yesterday, last 11 days ago
- search-explore: 0 yesterday, last 6 days ago
- search-home: 0 yesterday, last today
- signin-link-sent: 0 yesterday, last never
- smoke-test:  0 yesterday, last 26 days ago
- suggestion-submit: 0 yesterday, last 7 days ago
- walk-open:   0 yesterday, last 10 days ago
- walk-start:  0 yesterday, last never
- walks-app:   0 yesterday, last today
- worthit-not worth it: 0 yesterday, last 10 days ago
- worthit-worth it: 0 yesterday, last never

| Day | Accounts | Waitlist | Saves | Trees sent | Feedback |
|---|---:|---:|---:|---:|---:|
| 08-13 | 0 | 0 | 0 | 0 | 0 |
| 08-14 | 0 | 1 | 0 | 0 | 0 |
| 08-15 | 0 | 0 | 0 | 0 | 1 |
| 08-16 | 0 | 0 | 0 | 0 | 0 |
| 08-17 | 0 | 1 | 0 | 0 | 2 |
| 08-18 | 0 | 1 | 2 | 0 | 0 |
| 08-19 | 0 | 1 | 0 | 0 | 0 |
| 08-20 | 0 | 1 | 3 | 0 | 1 |
| 08-21 | 1 | 0 | 0 | 0 | 16 |
| 08-22 | 0 | 0 | 1 | 0 | 0 |
| 08-23 | 0 | 0 | 0 | 0 | 0 |
| 08-24 | 0 | 0 | 0 | 1 | 0 |
| 08-25 | 0 | 1 | 0 | 0 | 0 |
| 08-26 | 0 | 1 | 1 | 0 | 1 |
| 08-27 | 0 | 1 | 0 | 1 | 1 |
| **14 days** | **1** | **8** | **7** | **2** | **22** |
- Waitlist:    13 total, newest today
- Submissions: 24 total (2 trees sent, 22 feedback), newest today
- Accounts:    4 total, newest 6 days ago

**What readers told us** (14 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 08-15 | prg_007 (The Oak of Cisarsky ostro | not worth it | wrong location | no acct | holds |
| 08-17 | hel_006 (The Meilahti Ancient Pine | not worth it | - | no acct | holds |
| 08-17 | lis_005 (The Tipu of Jardim de São | worth it | - | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-21 | par_001 (The Robinier of Square Re | not worth it | - | no acct | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | report | could not reach it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | worth it | - | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | not worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-24 | Baarn | tree sent in | 4 chars, read it in the database | d4e6 | open_question |
| 08-25 | utr_005 (Onder de Linden) | vote undone | not worth it | d4e6 | - |
| 08-26 | sar_003 (The Olivastro of Santa Ma | worth it | - | d4e6 | - |
| 08-27 | ams_001 | worth it | - | 46c1 | - |
| 08-27 | Baarn | tree sent in | 4 chars, read it in the database | d4e6 | - |

- 30 of these 38 came from one account (d4e6). At this volume that is almost certainly our own testing rather than readers, and it should be read that way until somebody checks the rows.

**The funnel, as rates**
- Seen to clicked: 2.1% (243 of 11526) vs 2.2% the fortnight before
- Pages per visit: 1.5 (1050 visits, 1610 pageviews since 2026-08-08)
- Visits that did something: 7.6% (80 actions on 1050 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-17 | 15 | 606 | 2.5% | 14.4 |
| 08-18 | 19 | 609 | 3.1% | 15.0 |
| 08-19 | 18 | 806 | 2.2% | 17.0 |
| 08-20 | 17 | 1022 | 1.7% | 21.5 |
| 08-21 | 18 | 913 | 2.0% | 19.9 |
| 08-22 | 17 | 1030 | 1.7% | 19.9 |
| 08-23 | 15 | 958 | 1.6% | 16.2 |
| 08-24 | 28 | 998 | 2.8% | 15.9 |
| 08-25 | 19 | 1108 | 1.7% | 20.1 |
| 08-26 | 20 | 1105 | 1.8% | 18.8 |
| 08-27 *partial* | 0 | 21 | 0.0% | 9.8 |
| **window** | **186** | **9176** | **2.0%** | |
- Top queries (10d): dutch elm amsterdam (i45, p5); italian trees in rome (i2, p12); oldest tree in dc (i2, p33); "400 years old as of 2023" tree (i1, p7); "oldest ginkgo tree" park motto (i1, p5)
- Top pages (10d): /prague (c11/i134); / (c6/i78); /lisbon (c6/i152); /seville (c6/i97); /amsterdam (c4/i158)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - '"oldest of its species" owl park' (i7, p9)
    - 'ahuehuete tree' (i6, p13)
    - 'oldest tree in dc' (i2, p33)
    - '"400 years old as of 2023" tree' (i1, p7)
    - '"stands nearly 20 metres" tower medieval' (i1, p8)
    - '800 year old tree' (i1, p10)
    - '99 yew trees' (i1, p58)
    - 'a ten ile ma' (i1, p2)
    - and 3 more

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| amsterdam | 12 | 368 | 3.3% | 10.7 | 2.2% | dutch elm amsterdam (i21, p6) |
| rome | 5 | 353 | 1.4% | 11.0 | 2.2% | trees in rome (i14, p17) |
| tenerife | 0 | 226 | 0.0% | 10.7 | 2.2% | drago milenario (i24, p10) |
| barcelona | 4 | 215 | 1.9% | 10.5 | 2.3% | barbary thuja (i5, p8) |
| milan | 0 | 209 | 0.0% | 9.7 | 2.6% | "oldest of its species" ginkgo park (i12, p6) |
| lisbon | 9 | 204 | 4.4% | 8.7 | 3.1% | oldest tree in lisbon (i3, p9) |
| copenhagen | 6 | 198 | 3.0% | 11.4 | 2.0% | trees in copenhagen (i29, p17) |
| singapore | 4 | 189 | 2.1% | 14.3 | 1.3% | oldest tree in singapore (i21, p10) |
| bath | 2 | 185 | 1.1% | 8.4 | 3.3% | the giant plane tree bath (i9, p11) |
| london | 1 | 163 | 0.6% | 24.3 | 0.6% | london trees (i3, p77) |
| brisbane | 0 | 163 | 0.0% | 16.4 | 1.1% | mahogany (i9, p24) |
| prague | 12 | 151 | 7.9% | 8.1 | 3.4% | - |
| vienna | 0 | 147 | 0.0% | 9.9 | 2.6% | - |
| madrid | 0 | 144 | 0.0% | 15.4 | 1.2% | oldest tree in madrid (i4, p11) |
| seville | 8 | 138 | 5.8% | 11.0 | 2.1% | seville spain orange trees (i1, p41) |
| paris | 3 | 138 | 2.2% | 22.0 | 0.7% | palm trees in paris (i3, p61) |
| florence | 0 | 136 | 0.0% | 11.1 | 2.1% | florence tree (i6, p9) |
| palermo | 2 | 133 | 1.5% | 7.9 | 3.6% | oldest tree in palermo (i2, p12) |
| malaga | 3 | 130 | 2.3% | 13.2 | 1.6% | árboles históricos de málaga (i9, p81) |
| naples | 2 | 119 | 1.7% | 11.2 | 2.1% | a tree in naples (i1, p15) |
| brussels | 4 | 108 | 3.7% | 13.3 | 1.5% | belgian trees (i1, p36) |
| madeira | 0 | 98 | 0.0% | 8.3 | 3.3% | witch tree fanal (i6, p11) |
| seoul | 0 | 98 | 0.0% | 14.3 | 1.3% | seoul tree (i7, p8) |
| venice | 2 | 91 | 2.2% | 9.7 | 2.6% | trees in venice (i3, p7) |
| crete | 0 | 84 | 0.0% | 10.7 | 2.2% | 2000 years old olive tree (i2, p13) |
| montreal | 2 | 79 | 2.5% | 10.9 | 2.2% | century trees (i3, p53) |
| dublin | 2 | 78 | 2.6% | 14.8 | 1.2% | buchanan tree (i1, p10) |
| new-york | 2 | 74 | 2.7% | 17.9 | 1.0% | ancient elm (i1, p54) |
| edinburgh | 1 | 74 | 1.4% | 17.0 | 1.0% | john muir grove edinburgh (i2, p8) |
| cambridge | 0 | 74 | 0.0% | 35.0 | 0.4% | newton's apple tree (i6, p46) |
| palma-de-mallorca | 0 | 72 | 0.0% | 6.7 | 4.3% | oldest olive tree in palma (i2, p10) |
| fukuoka | 3 | 69 | 4.3% | 9.6 | 2.7% | kanatake (i1, p76) |
| dubrovnik | 4 | 67 | 6.0% | 7.5 | 3.8% | trsteno plane tree (i3, p12) |
| valencia | 2 | 66 | 3.0% | 9.2 | 2.9% | ficus centenarios de la glorieta (i3, p10) |
| toronto | 0 | 66 | 0.0% | 10.6 | 2.3% | big red oak (i8, p7) |
| nijmegen | 0 | 65 | 0.0% | 6.9 | 4.1% | hertogplein nijmegen maps (i1, p6) |
| las-vegas | 0 | 63 | 0.0% | 28.1 | 0.5% | vegas trees (i49, p33) |
| reykjavik | 1 | 58 | 1.7% | 19.5 | 0.8% | oldest tree in iceland (i5, p8) |
| washington-dc | 3 | 58 | 5.2% | 20.7 | 0.8% | survey lodge ranger station (i7, p11) |
| sardinia | 0 | 54 | 0.0% | 7.7 | 3.6% | baltolu sardinia (i4, p7) |
| krakow | 2 | 53 | 3.8% | 11.5 | 2.0% | plac kossaka krakow (i1, p10) |
| boston | 1 | 52 | 1.9% | 27.2 | 0.5% | trees in boston (i2, p54) |
| geneva | 3 | 51 | 5.9% | 11.5 | 2.0% | sixty tree (i1, p9) |
| alicante | 1 | 47 | 2.1% | 7.1 | 3.9% | ficus alicante (i5, p9) |
| porto | 1 | 47 | 2.1% | 6.0 | 5.0% | alameda dos platanos (i12, p8) |
| bristol | 2 | 45 | 4.4% | 22.0 | 0.7% | bristol trees (i4, p55) |
| oslo | 1 | 45 | 2.2% | 13.8 | 1.4% | "oldest ginkgo tree" park motto (i1, p5) |
| the-hague | 3 | 43 | 7.0% | 7.1 | 4.0% | old tree (i1, p9) |
| portland | 0 | 43 | 0.0% | 9.0 | 3.0% | - |
| berlin | 0 | 41 | 0.0% | 17.0 | 1.0% | berlin tree map (i1, p10) |
| bologna | 0 | 41 | 0.0% | 6.5 | 4.5% | - |
| istanbul | 1 | 40 | 2.5% | 6.4 | 4.6% | a ten ile ma (i1, p2) |
| leiden | 1 | 38 | 2.6% | 11.5 | 2.0% | "oldest of its species" ginkgo park (i6, p10) |
| chicago | 3 | 37 | 8.1% | 9.5 | 2.8% | wooded grove (i1, p48) |
| athens | 4 | 36 | 11.1% | 15.2 | 1.2% | old plane tree (i1, p35) |
| budapest | 1 | 35 | 2.9% | 7.3 | 3.9% | - |
| bordeaux | 1 | 34 | 2.9% | 8.9 | 3.0% | sequoia bordeaux (i2, p9) |
| cyprus | 0 | 34 | 0.0% | 8.1 | 3.4% | oldest tree in cyprus (i5, p10) |
| padua | 0 | 34 | 0.0% | 7.8 | 3.6% | - |
| perth | 0 | 34 | 0.0% | 13.2 | 1.6% | oldest tree in perth (i1, p10) |
| vilnius | 4 | 33 | 12.1% | 7.2 | 3.9% | willow tree in lithuanian (i3, p9) |
| hilo | 0 | 33 | 0.0% | 60.9 | 0.4% | loulu palm (i16, p100) |
| tokyo | 0 | 33 | 0.0% | 6.0 | 5.0% | - |
| groningen | 0 | 32 | 0.0% | 32.7 | 0.4% | big five groningen (i4, p84) |
| sintra | 2 | 31 | 6.5% | 6.5 | 4.5% | - |
| kyoto | 1 | 31 | 3.2% | 6.6 | 4.4% | - |
| cagliari | 0 | 31 | 0.0% | 4.4 | 7.6% | età (i1, p2) |
| greece | 1 | 30 | 3.3% | 32.3 | 0.4% | greek trees (i4, p44) |
| nice | 0 | 30 | 0.0% | 9.7 | 2.6% | promenade des anglais palm trees (i1, p5) |
| bratislava | 2 | 29 | 6.9% | 9.0 | 3.0% | - |
| mexico-city | 0 | 29 | 0.0% | 11.4 | 2.0% | ahuehuete (i1, p35) |
| munich | 0 | 29 | 0.0% | 8.2 | 3.4% | - |
| cork | 2 | 28 | 7.1% | 14.1 | 1.4% | oldest tree in ireland (i4, p15) |
| seattle | 1 | 27 | 3.7% | 5.6 | 5.8% | - |
| cordoba | 0 | 27 | 0.0% | 37.6 | 0.4% | gingko garden (i1, p56) |
| glasgow | 0 | 27 | 0.0% | 11.1 | 2.1% | - |
| potsdam | 0 | 27 | 0.0% | 11.4 | 2.0% | jagdschloss glienicke (i1, p12) |
| trieste | 0 | 27 | 0.0% | 6.7 | 4.3% | piazza hortis (i3, p9) |
| zurich | 1 | 26 | 3.8% | 13.4 | 1.5% | - |
| guimaraes | 0 | 26 | 0.0% | 12.3 | 1.7% | pine tree portugal (i3, p18) |
| utrecht | 1 | 25 | 4.0% | 12.8 | 1.6% | ja leuk (i1, p9) |
| york | 1 | 25 | 4.0% | 8.2 | 3.4% | - |
| hong-kong | 0 | 25 | 0.0% | 9.3 | 2.8% | - |
| quebec-city | 0 | 25 | 0.0% | 11.1 | 2.1% | what about quebec (i1, p7) |
| aarhus | 1 | 24 | 4.2% | 7.8 | 3.6% | happy pig (i1, p10) |
| helsinki | 1 | 24 | 4.2% | 7.3 | 3.8% | helsinki tree (i1, p8) |
| belgrade | 0 | 24 | 0.0% | 14.6 | 1.3% | - |
| sydney | 0 | 24 | 0.0% | 7.5 | 3.8% | the wishing tree sydney (i3, p9) |
| cadiz | 0 | 23 | 0.0% | 7.8 | 3.6% | - |
| genoa | 0 | 23 | 0.0% | 6.3 | 4.7% | - |
| lyon | 0 | 23 | 0.0% | 18.1 | 0.9% | antoine rivoire (i2, p8) |
| turin | 0 | 23 | 0.0% | 5.3 | 6.3% | alberi monumentali (i1, p8) |
| canada | 1 | 22 | 4.5% | 20.2 | 0.8% | oldest tree in canada (i3, p21) |
| warsaw | 1 | 22 | 4.5% | 14.1 | 1.4% | poland national tree (i1, p55) |
| bangkok | 0 | 22 | 0.0% | 9.3 | 2.8% | - |
| sorrento | 1 | 21 | 4.8% | 19.8 | 0.8% | - |
| strasbourg | 1 | 21 | 4.8% | 6.4 | 4.6% | - |
| tallinn | 0 | 19 | 0.0% | 8.1 | 3.5% | - |
| toulouse | 3 | 18 | 16.7% | 5.5 | 6.0% | - |
| maastricht | 1 | 17 | 5.9% | 8.1 | 3.4% | trees (i1, p8) |
| haarlem | 0 | 17 | 0.0% | 24.1 | 0.6% | noble tree (i4, p58) |
| split | 0 | 17 | 0.0% | 9.2 | 2.9% | mediterranean cypress croatia (i2, p8) |
| lucca | 1 | 16 | 6.2% | 7.1 | 4.0% | lucca tree (i1, p10) |
| oxford | 2 | 16 | 12.5% | 7.3 | 3.8% | - |
| caserta | 0 | 16 | 0.0% | 21.0 | 0.8% | parchi caserta (i1, p1) |
| stockholm | 0 | 16 | 0.0% | 7.9 | 3.6% | - |
| ljubljana | 1 | 15 | 6.7% | 15.5 | 1.2% | - |
| setubal | 1 | 14 | 7.1% | 7.4 | 3.8% | - |
| portugal | 0 | 14 | 0.0% | 58.4 | 0.4% | portugal trees (i2, p71) |
| bucaco | 0 | 13 | 0.0% | 12.7 | 1.7% | cedro do bussaco (i2, p2) |
| nara | 0 | 13 | 0.0% | 13.8 | 1.4% | - |
| osaka | 0 | 13 | 0.0% | 10.2 | 2.4% | - |
| poznan | 0 | 13 | 0.0% | 25.4 | 0.6% | - |
| new-orleans | 0 | 12 | 0.0% | 12.7 | 1.7% | mcdonogh oak (i2, p10) |
| nuremberg | 0 | 12 | 0.0% | 5.6 | 5.8% | - |
| braga | 1 | 11 | 9.1% | 9.4 | 2.8% | santa tecla braga (i1, p1) |
| delft | 2 | 11 | 18.2% | 23.3 | 0.7% | - |
| bergamo | 0 | 11 | 0.0% | 6.8 | 4.2% | parco caprotti (i3, p9) |
| graz | 0 | 11 | 0.0% | 10.2 | 2.4% | panoramagasse (i1, p5) |
| oahu | 0 | 11 | 0.0% | 7.0 | 4.0% | - |
| verona | 0 | 11 | 0.0% | 7.4 | 3.8% | - |
| antwerp | 0 | 10 | 0.0% | 21.4 | 0.7% | parks near me (i1, p1) |
| perugia | 0 | 10 | 0.0% | 6.4 | 4.6% | che albero é (i1, p2) |

**The language test** (Contract J v1.13: a translated set should pass its English twin's impressions within four weeks of indexing):

| Lang | City | Clicks | Impressions | Position | English twin |
|---|---|---:|---:|---:|---:|
| es | malaga | 1 | 156 | 12.4 | 130 |
| de | berlin | 0 | 33 | 14.9 | 41 |
| ja | kyoto | 1 | 20 | 11.5 | 31 |
| it | rome | 2 | 19 | 9.6 | 353 |
| it | palermo | 0 | 15 | 10.1 | 133 |
| ja | tokyo | 0 | 15 | 10.3 | 33 |
| de | vienna | 1 | 14 | 6.0 | 147 |
| pt | porto | 0 | 14 | 5.5 | 47 |
| pt | lisbon | 1 | 13 | 8.0 | 204 |
| nl | nijmegen | 0 | 12 | 7.5 | 65 |
| es | barcelona | 0 | 11 | 13.0 | 215 |
| pt | sintra | 1 | 10 | 22.5 | 31 |
| es | cadiz | 1 | 8 | 13.2 | 23 |
| es | madrid | 0 | 5 | 6.6 | 144 |
| it | milan | 0 | 5 | 19.0 | 209 |
| fr | nice | 0 | 4 | 39.8 | 30 |
| nl | amsterdam | 0 | 4 | 4.0 | 368 |
| es | tenerife | 0 | 3 | 19.3 | 226 |
| fr | geneva | 0 | 3 | 32.7 | 51 |
| ja | osaka | 0 | 2 | 4.0 | 13 |
| de | zurich | 0 | 1 | 11.0 | 26 |
- Seen, not clicked: /rome (c1/i80, 1.2%) for trees in rome (i14, p17); rome trees (i11, p11); trees in rome italy (i8, p17)
- Seen, not clicked: /tenerife/el-drago-milenario (c0/i73, 0.0%) for drago milenario (i24, p10); el drago milenario (i8, p10); tenerife oldest tree (i5, p10)
- Seen, not clicked: /las-vegas (c0/i49, 0.0%) for vegas trees (i49, p33)

**Climbing** (this ten days against the ten before it)

| Page | Impressions | Change | Position | Moved | Clicks |
|---|---:|---:|---:|---:|---:|
| /rome | 283 | +140 | 12.0 | +7.3 | +2 |
| /milan | 185 | +140 | 9.3 | +0.4 | +0 |
| /copenhagen | 141 | +131 | 11.0 | +2.2 | +1 |
| /barcelona | 166 | +111 | 9.0 | -1.2 | +3 |
| /madrid | 126 | +110 | 15.9 | -7.0 | +0 |
| /bath/plane-tree-of-abbey-green | 162 | +99 | 8.9 | -0.8 | +1 |
| /seville | 97 | +77 | 10.7 | -4.3 | +5 |
| /london | 102 | +73 | 30.9 | +18.0 | +0 |

**Newly ranking** (no impressions at all ten days ago)

| Page | Impressions | Clicks | Position |
|---|---:|---:|---:|
| /tenerife/el-drago-milenario | 132 | 0 | 10.9 |
| /species/osage-orange | 81 | 0 | 79.2 |
| /species/strawberry-tree | 60 | 0 | 68.1 |
| /species/american-elm | 56 | 0 | 77.8 |
| /las-vegas | 53 | 0 | 31.1 |
| /amsterdam/last-elm-of-stationsplein | 49 | 2 | 6.4 |

**Slipping**

| Page | Impressions | Change | Position | Moved |
|---|---:|---:|---:|---:|
| /geneva | 21 | -29 | 13.6 | -4.3 |
| /lyon | 15 | -24 | 23.7 | -9.2 |
| /boston | 20 | -14 | 36.4 | -22.6 |
| /cambridge | 15 | -14 | 39.9 | -21.1 |

- New queries this window: dutch elm amsterdam (i45).

**Who they are**
Audience, 28 days of search (334 clicks, 15543 impressions):
- Countries: usa c62/i3469; gbr c36/i1906; nld c26/i731; esp c19/i931; deu c18/i522
- Devices: MOBILE c226/i8354; DESKTOP c106/i7048; TABLET c2/i141
- Landing pages: / c16/i148; /prague c16/i285; /lisbon c11/i303; /seville c8/i145; /amsterdam c7/i390

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-19 | 40 | 80 |
| 08-20 | 110 | 180 |
| 08-21 | 40 | 80 |
| 08-22 | 90 | 120 |
| 08-23 | 70 | 120 |
| 08-24 | 10 | 20 |
| 08-25 | 60 | 70 |
| 08-26 | 80 | 110 |
| **window** | **500** | **780** |
- Top paths: /amsterdam (80); / (80); /copenhagen (40); /explore (40); /athens/holm-oak-of-the-national-garden (20); /toulouse/hackberry-of-place-saint-georges (20); /app (20); /cities (20); /brussels (20); /paris (20); /paris/turkish-hazel-of-square-du-temple (10); /contribute (10)
- Referrers: (direct) (360); ancienttrees.app (280); www.google.com (140)
- Moved between our own pages: 280 of 780 pageviews (36%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: NL (160); US (120); DE (70); GB (70); FR (60)
- Devices: desktop (450); mobile (320); tablet (10)
- Page load (8d): p50 764ms, p90 2714ms

Links: external referrers (a link somebody actually clicked): none yet
AI: arrivals from an assistant that cited us: none yet


**What the night shift did**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 08-26T19:53 | 20.9 | 5 | 9 | 23 | Las Vegas +3, Alicante +2 |
| 08-26T23:10 | 28.3 | 2 | 10 | 37 | Alicante +1, Rome +1 |
| 08-27T05:12 | 77.1 | 10 | 18 | 38 | Cologne +5, Guimaraes +2, Nijmegen +2, Toronto +1 |
| **3 runs** | **126** | **17** | **37** | | |

- 23 to 38 commands refused per run; 2 wrote nothing to LOG.md.

**What they made**

- Fresh-eyes review: 2 finding(s)
- Refresh city queue ledger; log 5 photo-queue verdicts from the viewing pass
- data/agent-costs.json: log this session's five passes
- LOG.md: guimaraes, photo pass, and a stuck push credential
- Guimaraes 6 to 8: two register trees on Monte da Penha, found by fixing a merge mistake
- LOG.md: session summary, nijmegen/toronto/cologne
- Open Cologne with 5 natural monuments, from the Naturdenkmal register
- Toronto 5 to 6: Zhelevo, the red oak the city bought a house to save
- register-scouting.json: record Palma de Mallorca's verdict
- Nijmegen 18 to 20: two Brakkenstein veterans, register ages reconciled
- photo_hunt --recheck: sweep 40 more photo-less trees, 607 queued with candidates
- Caserta leads: 23 leads verified and marked resolved, 1 held on access
- Rome +1: the Eucalyptus of Forte Ardeatino
- Process submission #39: a worth-it vote on Sardinia's Olivastro, no action

Machine: 8 chain attempts yesterday, 3 got real work time (~79 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 0 clicks and 21 impressions on Google's freshest day (day before: c20/i1105). Directional at best; no strategic conclusions from these volumes.

## 2026-08-25 (previous UTC day)

**Today: a waitlist arrived yesterday (11 total).**

**Did the product happen**
- app-cta:     2 yesterday, last yesterday
- waitlist-submit: 1 yesterday, last yesterday
- beacon-fix-verify: 0 yesterday, last 10 days ago
- beacon-test: 0 yesterday, last 10 days ago
- directions:  0 yesterday, last 5 days ago
- save:        0 yesterday, last 4 days ago
- search-explore: 0 yesterday, last 5 days ago
- search-home: 0 yesterday, last 3 days ago
- signin-link-sent: 0 yesterday, last never
- smoke-test:  0 yesterday, last 25 days ago
- suggestion-submit: 0 yesterday, last 6 days ago
- walk-open:   0 yesterday, last 9 days ago
- walk-start:  0 yesterday, last never
- walks-app:   0 yesterday, last 8 days ago
- worthit-not worth it: 0 yesterday, last 9 days ago
- worthit-worth it: 0 yesterday, last never

| Day | Accounts | Waitlist | Saves | Trees sent | Feedback |
|---|---:|---:|---:|---:|---:|
| 08-12 | 0 | 0 | 0 | 0 | 0 |
| 08-13 | 0 | 0 | 0 | 0 | 0 |
| 08-14 | 0 | 1 | 0 | 0 | 0 |
| 08-15 | 0 | 0 | 0 | 0 | 1 |
| 08-16 | 0 | 0 | 0 | 0 | 0 |
| 08-17 | 0 | 1 | 0 | 0 | 2 |
| 08-18 | 0 | 1 | 2 | 0 | 0 |
| 08-19 | 0 | 1 | 0 | 0 | 0 |
| 08-20 | 0 | 1 | 3 | 0 | 1 |
| 08-21 | 1 | 0 | 0 | 0 | 16 |
| 08-22 | 0 | 0 | 1 | 0 | 0 |
| 08-23 | 0 | 0 | 0 | 0 | 0 |
| 08-24 | 0 | 0 | 0 | 1 | 0 |
| 08-25 | 0 | 1 | 0 | 0 | 0 |
| 08-26 | 0 | 0 | 0 | 0 | 0 |
| **14 days** | **1** | **6** | **6** | **1** | **20** |
- Waitlist:    11 total, newest yesterday
- Submissions: 21 total (1 trees sent, 20 feedback), newest 2 days ago
- Accounts:    4 total, newest 5 days ago

**What readers told us** (14 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 08-15 | prg_007 (The Oak of Cisarsky ostro | not worth it | wrong location | no acct | holds |
| 08-17 | hel_006 (The Meilahti Ancient Pine | not worth it | - | no acct | holds |
| 08-17 | lis_005 (The Tipu of Jardim de São | worth it | - | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-21 | par_001 (The Robinier of Square Re | not worth it | - | no acct | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | report | could not reach it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | worth it | - | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | not worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-24 | Baarn | tree sent in | 4 chars, read it in the database | d4e6 | - |
| 08-25 | utr_005 (Onder de Linden) | vote undone | not worth it | d4e6 | - |

- 28 of these 35 came from one account (d4e6). At this volume that is almost certainly our own testing rather than readers, and it should be read that way until somebody checks the rows.

**The funnel, as rates**
- Seen to clicked: 2.2% (227 of 10497) vs 2.3% the fortnight before
- Pages per visit: 1.5 (970 visits, 1500 pageviews since 2026-08-08)
- Visits that did something: 7.1% (69 actions on 970 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-16 | 15 | 736 | 2.0% | 13.5 |
| 08-17 | 15 | 606 | 2.5% | 14.4 |
| 08-18 | 19 | 609 | 3.1% | 15.0 |
| 08-19 | 18 | 806 | 2.2% | 17.0 |
| 08-20 | 17 | 1022 | 1.7% | 21.5 |
| 08-21 | 18 | 913 | 2.0% | 19.9 |
| 08-22 | 17 | 1030 | 1.7% | 19.9 |
| 08-23 | 15 | 958 | 1.6% | 16.2 |
| 08-24 | 28 | 998 | 2.8% | 15.9 |
| 08-25 *partial* | 14 | 764 | 1.8% | 18.3 |
| **window** | **176** | **8442** | **2.1%** | |
- Top queries (10d): dutch elm amsterdam (i40, p5); oldest tree in dc (i2, p33); "oldest ginkgo tree" park motto (i1, p5); "oldest of its species" ginkgo park (i15, p7); "oldest of its species" owl park (i6, p9)
- Top pages (10d): /prague (c11/i145); / (c6/i62); /athens/holm-oak-of-the-national-garden (c5/i8); /seville (c5/i82); /amsterdam (c4/i154)
- Content lead: 'alameda dos platanos' has no matching page (i13, p8)

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| amsterdam | 11 | 347 | 3.2% | 10.9 | 2.2% | dutch elm amsterdam (i21, p6) |
| rome | 4 | 295 | 1.4% | 10.9 | 2.2% | trees in rome (i10, p20) |
| barcelona | 5 | 214 | 2.3% | 10.2 | 2.4% | barcelona tree (i4, p6) |
| tenerife | 0 | 209 | 0.0% | 10.8 | 2.2% | drago milenario (i24, p10) |
| bath | 3 | 202 | 1.5% | 8.1 | 3.5% | the giant plane tree bath (i10, p11) |
| lisbon | 7 | 193 | 3.6% | 10.3 | 2.4% | oldest tree in lisbon (i4, p9) |
| copenhagen | 6 | 193 | 3.1% | 11.8 | 1.9% | trees in copenhagen (i24, p17) |
| milan | 0 | 191 | 0.0% | 10.2 | 2.4% | "oldest of its species" ginkgo park (i12, p6) |
| singapore | 4 | 169 | 2.4% | 13.5 | 1.5% | oldest tree in singapore (i18, p10) |
| prague | 12 | 166 | 7.2% | 7.2 | 3.9% | four trees prague (i2, p21) |
| london | 1 | 156 | 0.6% | 21.2 | 0.8% | london trees (i3, p77) |
| vienna | 0 | 148 | 0.0% | 10.0 | 2.5% | - |
| palermo | 2 | 147 | 1.4% | 8.2 | 3.4% | oldest tree in palermo (i4, p10) |
| brisbane | 0 | 145 | 0.0% | 15.5 | 1.2% | mahogany (i9, p24) |
| madrid | 0 | 143 | 0.0% | 14.2 | 1.4% | oldest tree in madrid (i2, p11) |
| florence | 0 | 130 | 0.0% | 11.9 | 1.8% | florence tree (i6, p9) |
| paris | 4 | 127 | 3.1% | 22.1 | 0.7% | palm trees in paris (i3, p61) |
| seville | 6 | 124 | 4.8% | 10.2 | 2.4% | - |
| malaga | 2 | 116 | 1.7% | 12.7 | 1.7% | árboles históricos de málaga (i7, p80) |
| naples | 2 | 107 | 1.9% | 11.8 | 1.9% | a tree in naples (i1, p15) |
| brussels | 3 | 101 | 3.0% | 13.6 | 1.5% | belgium national tree (i1, p47) |
| seoul | 0 | 95 | 0.0% | 14.4 | 1.3% | seoul tree (i7, p8) |
| venice | 3 | 82 | 3.7% | 10.2 | 2.4% | trees in venice (i1, p1) |
| cambridge | 0 | 82 | 0.0% | 35.8 | 0.4% | newton's apple tree (i6, p46) |
| montreal | 2 | 75 | 2.7% | 11.1 | 2.1% | century trees (i3, p53) |
| crete | 0 | 75 | 0.0% | 10.4 | 2.4% | 2000 years old olive tree (i2, p13) |
| madeira | 0 | 75 | 0.0% | 8.1 | 3.5% | fanal witch tree (i4, p13) |
| dublin | 3 | 74 | 4.1% | 15.9 | 1.1% | buchanan tree (i1, p10) |
| palma-de-mallorca | 0 | 69 | 0.0% | 7.4 | 3.8% | oldest olive tree in palma (i2, p10) |
| dubrovnik | 4 | 68 | 5.9% | 7.4 | 3.8% | trsteno plane tree (i3, p12) |
| new-york | 3 | 68 | 4.4% | 15.0 | 1.2% | ancient elm (i1, p54) |
| edinburgh | 1 | 68 | 1.5% | 19.0 | 0.9% | john muir grove edinburgh (i2, p8) |
| washington-dc | 3 | 67 | 4.5% | 18.9 | 0.9% | survey lodge ranger station (i7, p10) |
| valencia | 2 | 66 | 3.0% | 9.2 | 2.9% | ficus centenarios de la glorieta (i3, p10) |
| reykjavik | 1 | 62 | 1.6% | 16.5 | 1.1% | oldest tree in iceland (i5, p8) |
| boston | 1 | 58 | 1.7% | 27.0 | 0.5% | trees in boston (i2, p54) |
| fukuoka | 2 | 56 | 3.6% | 9.9 | 2.5% | kanatake (i1, p76) |
| geneva | 1 | 55 | 1.8% | 11.4 | 2.0% | sixty tree (i1, p9) |
| las-vegas | 0 | 55 | 0.0% | 30.7 | 0.4% | vegas trees (i48, p33) |
| porto | 1 | 53 | 1.9% | 5.8 | 5.4% | alameda dos platanos (i13, p8) |
| alicante | 1 | 52 | 1.9% | 6.5 | 4.5% | ficus alicante (i5, p9) |
| toronto | 0 | 52 | 0.0% | 10.8 | 2.2% | big red oak (i7, p7) |
| krakow | 2 | 51 | 3.9% | 11.8 | 1.9% | plac kossaka krakow (i1, p10) |
| oslo | 1 | 51 | 2.0% | 12.5 | 1.7% | "oldest ginkgo tree" park motto (i1, p5) |
| budapest | 1 | 49 | 2.0% | 7.5 | 3.8% | in budapest? (i1, p4) |
| bristol | 3 | 48 | 6.2% | 20.1 | 0.8% | bristol trees (i4, p55) |
| sardinia | 0 | 46 | 0.0% | 7.7 | 3.7% | baltolu sardinia (i4, p7) |
| portland | 0 | 42 | 0.0% | 6.9 | 4.1% | - |
| the-hague | 2 | 41 | 4.9% | 7.4 | 3.8% | old tree (i1, p9) |
| berlin | 0 | 41 | 0.0% | 15.0 | 1.2% | berlin tree map (i1, p10) |
| nijmegen | 0 | 41 | 0.0% | 7.1 | 3.9% | oldest tree in the netherlands (i1, p5) |
| padua | 0 | 40 | 0.0% | 7.7 | 3.7% | - |
| athens | 5 | 39 | 12.8% | 14.6 | 1.3% | old plane tree (i1, p35) |
| istanbul | 1 | 38 | 2.6% | 6.6 | 4.4% | a ten ile ma (i1, p2) |
| helsinki | 1 | 37 | 2.7% | 8.6 | 3.2% | helsinki tree (i1, p8) |
| bologna | 0 | 37 | 0.0% | 6.3 | 4.7% | - |
| sintra | 2 | 34 | 5.9% | 6.6 | 4.4% | - |
| bordeaux | 1 | 33 | 3.0% | 8.9 | 3.0% | sequoia bordeaux (i2, p9) |
| zurich | 1 | 33 | 3.0% | 13.4 | 1.5% | zurich (i1, p2) |
| vilnius | 4 | 31 | 12.9% | 7.3 | 3.9% | willow tree in lithuanian (i3, p9) |
| guimaraes | 0 | 31 | 0.0% | 11.2 | 2.1% | pine tree portugal (i3, p18) |
| cagliari | 0 | 30 | 0.0% | 5.0 | 7.0% | ficus cagliari (i1, p8) |
| nice | 0 | 30 | 0.0% | 9.9 | 2.5% | promenade des anglais palm trees (i1, p5) |
| cork | 3 | 29 | 10.3% | 15.5 | 1.2% | oldest tree in ireland (i3, p16) |
| groningen | 0 | 29 | 0.0% | 36.2 | 0.4% | big five groningen (i4, p84) |
| hong-kong | 0 | 29 | 0.0% | 13.2 | 1.6% | trees in hong kong (i1, p60) |
| glasgow | 1 | 28 | 3.6% | 12.9 | 1.6% | - |
| turin | 1 | 28 | 3.6% | 5.0 | 7.0% | alberi monumentali (i1, p8) |
| lyon | 0 | 28 | 0.0% | 16.3 | 1.1% | antoine rivoire (i2, p8) |
| tokyo | 0 | 27 | 0.0% | 5.7 | 5.6% | - |
| chicago | 2 | 26 | 7.7% | 10.3 | 2.4% | wooded grove (i1, p48) |
| bratislava | 1 | 26 | 3.8% | 9.2 | 2.9% | - |
| leiden | 1 | 26 | 3.8% | 13.1 | 1.6% | "oldest of its species" ginkgo park (i2, p10) |
| warsaw | 1 | 26 | 3.8% | 15.2 | 1.2% | oldest tree in poland (i1, p53) |
| potsdam | 0 | 26 | 0.0% | 11.7 | 1.9% | jagdschloss glienicke (i1, p12) |
| york | 1 | 25 | 4.0% | 8.2 | 3.4% | - |
| belgrade | 0 | 25 | 0.0% | 14.4 | 1.3% | - |
| cordoba | 0 | 25 | 0.0% | 31.2 | 0.4% | gingko garden (i1, p56) |
| cyprus | 0 | 25 | 0.0% | 8.9 | 3.0% | oldest tree in cyprus (i4, p10) |
| aarhus | 1 | 24 | 4.2% | 7.8 | 3.6% | happy pig (i1, p10) |
| greece | 1 | 24 | 4.2% | 31.3 | 0.4% | greek trees (i4, p44) |
| hilo | 0 | 24 | 0.0% | 63.7 | 0.4% | loulu palm (i13, p100) |
| ljubljana | 1 | 23 | 4.3% | 11.3 | 2.0% | - |
| seattle | 1 | 23 | 4.3% | 5.7 | 5.6% | - |
| utrecht | 1 | 23 | 4.3% | 12.3 | 1.7% | ja leuk (i1, p9) |
| trieste | 0 | 23 | 0.0% | 6.4 | 4.6% | piazza hortis (i2, p10) |
| kyoto | 1 | 22 | 4.5% | 6.4 | 4.6% | - |
| bangkok | 0 | 22 | 0.0% | 12.6 | 1.7% | - |
| genoa | 0 | 22 | 0.0% | 6.7 | 4.3% | - |
| cadiz | 0 | 21 | 0.0% | 7.9 | 3.5% | - |
| canada | 1 | 20 | 5.0% | 18.1 | 1.0% | oldest tree in canada (i3, p21) |
| maastricht | 1 | 20 | 5.0% | 8.3 | 3.3% | trees (i1, p8) |
| haarlem | 0 | 20 | 0.0% | 26.7 | 0.5% | noble tree (i6, p58) |
| mexico-city | 0 | 20 | 0.0% | 8.4 | 3.3% | ahuehuete (i1, p35) |
| perth | 0 | 20 | 0.0% | 17.8 | 1.0% | oldest tree in perth (i1, p10) |
| stockholm | 0 | 20 | 0.0% | 7.7 | 3.6% | - |
| munich | 0 | 19 | 0.0% | 9.1 | 2.9% | - |
| lucca | 1 | 18 | 5.6% | 9.8 | 2.6% | lucca tree (i1, p10) |
| granada | 0 | 18 | 0.0% | 24.3 | 0.6% | granada orange trees (i1, p64) |
| osaka | 0 | 18 | 0.0% | 10.4 | 2.3% | - |
| quebec-city | 0 | 18 | 0.0% | 12.3 | 1.7% | what about quebec (i1, p7) |
| strasbourg | 1 | 17 | 5.9% | 7.0 | 4.0% | - |
| caserta | 0 | 17 | 0.0% | 20.2 | 0.8% | parchi caserta (i1, p1) |
| split | 0 | 17 | 0.0% | 9.2 | 2.9% | mediterranean cypress croatia (i2, p8) |
| setubal | 1 | 16 | 6.2% | 6.9 | 4.1% | - |
| oxford | 2 | 15 | 13.3% | 7.5 | 3.8% | - |
| sofia | 1 | 15 | 6.7% | 14.1 | 1.4% | - |
| sorrento | 1 | 15 | 6.7% | 20.5 | 0.8% | - |
| portugal | 0 | 15 | 0.0% | 59.5 | 0.4% | portugal trees (i2, p71) |
| tallinn | 0 | 15 | 0.0% | 8.4 | 3.3% | - |
| toulouse | 3 | 14 | 21.4% | 4.5 | 7.5% | - |
| arnhem | 0 | 13 | 0.0% | 12.5 | 1.7% | - |
| bucaco | 0 | 13 | 0.0% | 12.7 | 1.7% | cedro do bussaco (i2, p2) |
| poznan | 0 | 13 | 0.0% | 25.2 | 0.6% | - |
| antwerp | 0 | 12 | 0.0% | 18.8 | 0.9% | parks near me (i1, p1) |
| breda | 0 | 12 | 0.0% | 33.9 | 0.4% | - |
| nara | 0 | 12 | 0.0% | 13.5 | 1.5% | - |
| delft | 2 | 11 | 18.2% | 14.5 | 1.3% | - |
| bergamo | 0 | 11 | 0.0% | 6.8 | 4.2% | parco caprotti (i3, p9) |
| perugia | 0 | 11 | 0.0% | 6.7 | 4.3% | che albero é (i1, p2) |
| verona | 0 | 11 | 0.0% | 7.5 | 3.7% | - |
| catania | 0 | 10 | 0.0% | 7.0 | 4.0% | - |
| graz | 0 | 10 | 0.0% | 10.5 | 2.3% | panoramagasse (i1, p5) |
| hobart | 0 | 10 | 0.0% | 6.5 | 4.5% | - |
- Seen, not clicked: /tenerife/el-drago-milenario (c0/i70, 0.0%) for drago milenario (i24, p10); el drago milenario (i8, p10); tenerife oldest tree (i5, p10)
- Seen, not clicked: /rome (c0/i55, 0.0%) for trees in rome (i10, p20); rome trees (i8, p12); trees in rome italy (i7, p18)
- Seen, not clicked: /las-vegas (c0/i48, 0.0%) for vegas trees (i48, p33)

**Climbing** (this ten days against the ten before it)

| Page | Impressions | Change | Position | Moved | Clicks |
|---|---:|---:|---:|---:|---:|
| /milan | 170 | +132 | 9.7 | +1.0 | +0 |
| /bath/plane-tree-of-abbey-green | 169 | +130 | 8.6 | +0.5 | +1 |
| /madrid | 126 | +123 | 14.5 | -2.2 | +0 |
| /barcelona | 157 | +108 | 8.7 | -0.6 | +3 |
| /rome | 229 | +89 | 12.1 | +7.7 | +1 |
| /lisbon | 144 | +75 | 8.5 | +1.5 | +2 |
| /london | 94 | +68 | 26.4 | +27.9 | +0 |
| /seville | 82 | +63 | 9.7 | -3.4 | +4 |

**Newly ranking** (no impressions at all ten days ago)

| Page | Impressions | Clicks | Position |
|---|---:|---:|---:|
| /copenhagen | 135 | 1 | 11.4 |
| /tenerife/el-drago-milenario | 125 | 0 | 10.9 |
| /species/osage-orange | 66 | 0 | 78.8 |
| /las-vegas | 51 | 0 | 31.8 |
| /amsterdam/last-elm-of-stationsplein | 49 | 2 | 6.4 |
| /species/strawberry-tree | 43 | 0 | 66.3 |

**Slipping**

| Page | Impressions | Change | Position | Moved |
|---|---:|---:|---:|---:|
| /granada | 16 | -29 | 27.0 | -18.2 |
| /nice | 19 | -20 | 12.3 | -0.5 |
| /geneva | 26 | -19 | 12.4 | -2.9 |
| /lyon | 19 | -18 | 20.7 | -5.1 |

- New queries this window: dutch elm amsterdam (i40), "oldest of its species" owl park (i6).

**Who they are**
Audience, 28 days of search (318 clicks, 14320 impressions):
- Countries: usa c59/i3171; gbr c36/i1816; nld c26/i672; deu c17/i481; esp c15/i850
- Devices: MOBILE c218/i7760; DESKTOP c99/i6427; TABLET c1/i133
- Landing pages: / c16/i132; /prague c16/i281; /lisbon c10/i284; /amsterdam c7/i403; /seville c7/i128

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-18 | 40 | 60 |
| 08-19 | 40 | 80 |
| 08-20 | 110 | 180 |
| 08-21 | 40 | 80 |
| 08-22 | 90 | 120 |
| 08-23 | 70 | 120 |
| 08-24 | 10 | 20 |
| 08-25 | 60 | 70 |
| **window** | **460** | **730** |
- Top paths: /amsterdam (90); / (80); /explore (50); /copenhagen (40); /parks/national-botanic-gardens-dublin (20); /paris (20); /toulouse/hackberry-of-place-saint-georges (20); /athens/holm-oak-of-the-national-garden (20); /app (20); /cities (20); /aarhus (10); /contribute (10)
- Referrers: (direct) (310); ancienttrees.app (270); www.google.com (150)
- Moved between our own pages: 270 of 730 pageviews (37%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: NL (160); US (120); GB (80); DE (60); AU (40)
- Devices: desktop (370); mobile (360)
- Page load (8d): p50 687ms, p90 3611ms

Links: external referrers (a link somebody actually clicked): none yet
AI: arrivals from an assistant that cited us: none yet


**What the night shift did**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 08-25T18:46 | 0.0 | 0 | 0 | 0 | - |
| 08-25T20:34 | 0.0 | 0 | 0 | 0 | - |
| 08-25T22:32 | 0.0 | 0 | 0 | 0 | - |
| 08-26T00:28 | 0.0 | 0 | 0 | 0 | - |
| 08-26T02:54 | 0.0 | 0 | 0 | 0 | - |
| 08-26T04:27 | 0.0 | 0 | 0 | 0 | - |
| **6 runs** | **0** | **0** | **0** | | |

- 6 of 6 produced no trees; 6 wrote nothing to LOG.md.

Machine: 9 chain attempts yesterday, 0 got real work time (~0 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 14 clicks and 764 impressions on Google's freshest day (day before: c28/i998). Directional at best; no strategic conclusions from these volumes.

## 2026-08-24 (previous UTC day)

**Today: 1 tree submission arrived yesterday (21 total).**

**Did the product happen**
- app-cta:     0 yesterday, last 2 days ago
- beacon-fix-verify: 0 yesterday, last 9 days ago
- beacon-test: 0 yesterday, last 9 days ago
- directions:  0 yesterday, last 4 days ago
- save:        0 yesterday, last 3 days ago
- search-explore: 0 yesterday, last 4 days ago
- search-home: 0 yesterday, last 2 days ago
- signin-link-sent: 0 yesterday, last never
- smoke-test:  0 yesterday, last 24 days ago
- suggestion-submit: 0 yesterday, last 5 days ago
- waitlist-submit: 0 yesterday, last 5 days ago
- walk-open:   0 yesterday, last 8 days ago
- walk-start:  0 yesterday, last never
- walks-app:   0 yesterday, last 7 days ago
- worthit-not worth it: 0 yesterday, last 8 days ago
- worthit-worth it: 0 yesterday, last never

| Day | Accounts | Waitlist | Saves | Trees sent | Feedback |
|---|---:|---:|---:|---:|---:|
| 08-11 | 0 | 0 | 0 | 0 | 0 |
| 08-12 | 0 | 0 | 0 | 0 | 0 |
| 08-13 | 0 | 0 | 0 | 0 | 0 |
| 08-14 | 0 | 1 | 0 | 0 | 0 |
| 08-15 | 0 | 0 | 0 | 0 | 1 |
| 08-16 | 0 | 0 | 0 | 0 | 0 |
| 08-17 | 0 | 1 | 0 | 0 | 2 |
| 08-18 | 0 | 1 | 2 | 0 | 0 |
| 08-19 | 0 | 1 | 0 | 0 | 0 |
| 08-20 | 0 | 1 | 3 | 0 | 1 |
| 08-21 | 1 | 0 | 0 | 0 | 16 |
| 08-22 | 0 | 0 | 1 | 0 | 0 |
| 08-23 | 0 | 0 | 0 | 0 | 0 |
| 08-24 | 0 | 0 | 0 | 1 | 0 |
| 08-25 | 0 | 0 | 0 | 0 | 0 |
| **14 days** | **1** | **5** | **6** | **1** | **20** |
- Waitlist:    10 total, newest 5 days ago
- Submissions: 21 total (1 trees sent, 20 feedback), newest yesterday
- Accounts:    4 total, newest 4 days ago

**What readers told us** (14 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 08-15 | prg_007 (The Oak of Cisarsky ostro | not worth it | wrong location | no acct | holds |
| 08-17 | hel_006 (The Meilahti Ancient Pine | not worth it | - | no acct | holds |
| 08-17 | lis_005 (The Tipu of Jardim de São | worth it | - | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-21 | par_001 (The Robinier of Square Re | not worth it | - | no acct | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | report | could not reach it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | worth it | - | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | not worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-24 | Baarn | tree sent in | 4 chars, read it in the database | d4e6 | - |

- 27 of these 34 came from one account (d4e6). At this volume that is almost certainly our own testing rather than readers, and it should be read that way until somebody checks the rows.

**The funnel, as rates**
- Seen to clicked: 2.2% (219 of 9879) vs 2.4% the fortnight before
- Pages per visit: 1.6 (910 visits, 1430 pageviews since 2026-08-08)
- Visits that did something: 7.3% (66 actions on 910 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-15 | 18 | 645 | 2.8% | 13.8 |
| 08-16 | 15 | 736 | 2.0% | 13.5 |
| 08-17 | 15 | 606 | 2.5% | 14.4 |
| 08-18 | 19 | 609 | 3.1% | 15.0 |
| 08-19 | 18 | 806 | 2.2% | 17.0 |
| 08-20 | 17 | 1022 | 1.7% | 21.5 |
| 08-21 | 18 | 913 | 2.0% | 19.9 |
| 08-22 | 17 | 1030 | 1.7% | 19.9 |
| 08-23 | 15 | 957 | 1.6% | 16.2 |
| 08-24 | 26 | 730 | 3.6% | 14.1 |
| **window** | **178** | **8054** | **2.2%** | |
- Top queries (10d): dutch elm amsterdam (i32, p6); oldest tree in central park (i3, p10); oldest tree in dc (i2, p33); "oldest ginkgo tree" park motto (i1, p5); "oldest of its species" ginkgo park (i15, p7)
- Top pages (10d): /prague (c9/i149); / (c6/i55); /amsterdam (c5/i150); /athens/holm-oak-of-the-national-garden (c5/i8); /lisbon (c5/i142)
- Content lead: 'alameda dos platanos' has no matching page (i15, p8)

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| amsterdam | 11 | 317 | 3.5% | 11.1 | 2.1% | dutch elm amsterdam (i20, p6) |
| rome | 4 | 294 | 1.4% | 10.7 | 2.2% | trees in rome (i13, p18) |
| bath | 3 | 220 | 1.4% | 7.9 | 3.5% | the giant plane tree bath (i11, p11) |
| barcelona | 5 | 210 | 2.4% | 10.3 | 2.4% | barcelona tree (i5, p6) |
| lisbon | 7 | 192 | 3.6% | 9.5 | 2.8% | oldest tree in lisbon (i5, p9) |
| tenerife | 0 | 179 | 0.0% | 10.9 | 2.2% | drago milenario (i18, p10) |
| copenhagen | 6 | 177 | 3.4% | 12.1 | 1.8% | trees in copenhagen (i21, p17) |
| milan | 0 | 177 | 0.0% | 10.5 | 2.3% | "oldest of its species" ginkgo park (i12, p6) |
| singapore | 2 | 172 | 1.2% | 14.2 | 1.4% | oldest tree in singapore (i16, p10) |
| prague | 10 | 171 | 5.8% | 7.1 | 4.0% | four trees prague (i2, p21) |
| london | 1 | 153 | 0.7% | 21.2 | 0.8% | london trees (i3, p77) |
| palermo | 3 | 151 | 2.0% | 8.4 | 3.3% | oldest tree in palermo (i4, p10) |
| vienna | 1 | 148 | 0.7% | 10.6 | 2.3% | - |
| florence | 0 | 138 | 0.0% | 11.7 | 1.9% | florence tree (i6, p9) |
| madrid | 0 | 135 | 0.0% | 13.5 | 1.5% | oldest tree in madrid (i4, p13) |
| paris | 6 | 131 | 4.6% | 20.8 | 0.8% | palm trees in paris (i3, p61) |
| brisbane | 0 | 128 | 0.0% | 15.9 | 1.1% | mahogany (i9, p24) |
| seville | 4 | 110 | 3.6% | 10.9 | 2.2% | - |
| naples | 2 | 102 | 2.0% | 10.6 | 2.3% | a tree in naples (i1, p15) |
| cambridge | 0 | 99 | 0.0% | 32.3 | 0.4% | newton's apple tree (i6, p46) |
| malaga | 2 | 98 | 2.0% | 12.0 | 1.8% | árboles históricos de málaga (i5, p80) |
| brussels | 3 | 97 | 3.1% | 14.0 | 1.4% | belgium national tree (i1, p47) |
| seoul | 0 | 91 | 0.0% | 14.3 | 1.3% | seoul tree (i7, p8) |
| geneva | 1 | 85 | 1.2% | 11.2 | 2.1% | sixty tree (i1, p9) |
| venice | 3 | 83 | 3.6% | 10.1 | 2.5% | trees in venice (i1, p1) |
| dublin | 5 | 74 | 6.8% | 14.5 | 1.3% | buchanan tree (i1, p10) |
| dubrovnik | 4 | 72 | 5.6% | 7.4 | 3.8% | trsteno plane tree (i4, p12) |
| montreal | 2 | 72 | 2.8% | 11.0 | 2.1% | century trees (i3, p53) |
| washington-dc | 3 | 70 | 4.3% | 18.7 | 0.9% | survey lodge ranger station (i8, p11) |
| boston | 1 | 69 | 1.4% | 24.0 | 0.6% | trees in boston (i2, p54) |
| edinburgh | 0 | 69 | 0.0% | 18.8 | 0.9% | john muir grove edinburgh (i2, p8) |
| madeira | 0 | 69 | 0.0% | 8.0 | 3.5% | fanal witch tree (i4, p13) |
| new-york | 4 | 67 | 6.0% | 16.0 | 1.1% | ancient elm (i1, p54) |
| valencia | 2 | 67 | 3.0% | 9.2 | 2.9% | ficus centenarios de la glorieta (i3, p10) |
| porto | 1 | 66 | 1.5% | 5.7 | 5.6% | alameda dos platanos (i15, p8) |
| palma-de-mallorca | 0 | 59 | 0.0% | 7.5 | 3.7% | oldest olive tree in palma (i2, p10) |
| budapest | 1 | 58 | 1.7% | 8.3 | 3.3% | in budapest? (i1, p4) |
| reykjavik | 1 | 58 | 1.7% | 14.7 | 1.3% | oldest tree in iceland (i4, p8) |
| crete | 0 | 58 | 0.0% | 9.5 | 2.8% | 2000 years old olive tree (i2, p13) |
| bristol | 3 | 52 | 5.8% | 21.0 | 0.8% | bristol trees (i6, p55) |
| istanbul | 2 | 52 | 3.8% | 8.5 | 3.2% | - |
| alicante | 1 | 50 | 2.0% | 6.5 | 4.5% | ficus alicante (i5, p9) |
| oslo | 1 | 50 | 2.0% | 13.5 | 1.5% | "oldest ginkgo tree" park motto (i1, p5) |
| toronto | 0 | 48 | 0.0% | 11.0 | 2.1% | big red oak (i6, p6) |
| krakow | 2 | 47 | 4.3% | 11.8 | 1.9% | - |
| padua | 1 | 46 | 2.2% | 7.6 | 3.7% | - |
| bologna | 0 | 43 | 0.0% | 6.7 | 4.3% | trees hours (i1, p11) |
| the-hague | 2 | 42 | 4.8% | 6.7 | 4.3% | old tree (i1, p9) |
| fukuoka | 1 | 42 | 2.4% | 7.7 | 3.6% | - |
| sintra | 2 | 41 | 4.9% | 6.4 | 4.6% | - |
| berlin | 0 | 40 | 0.0% | 15.2 | 1.2% | - |
| las-vegas | 0 | 40 | 0.0% | 31.2 | 0.4% | vegas trees (i37, p33) |
| portland | 0 | 40 | 0.0% | 8.4 | 3.3% | - |
| sardinia | 0 | 39 | 0.0% | 7.9 | 3.5% | baltolu sardinia (i3, p7) |
| athens | 5 | 38 | 13.2% | 14.8 | 1.2% | old plane tree (i1, p35) |
| helsinki | 1 | 38 | 2.6% | 8.5 | 3.2% | helsinki tree (i1, p8) |
| zurich | 1 | 35 | 2.9% | 12.9 | 1.6% | zurich (i1, p2) |
| nice | 0 | 34 | 0.0% | 12.4 | 1.7% | - |
| nijmegen | 0 | 32 | 0.0% | 7.2 | 3.9% | oldest tree in the netherlands (i1, p5) |
| cork | 4 | 31 | 12.9% | 14.8 | 1.2% | oldest tree in ireland (i2, p17) |
| glasgow | 2 | 31 | 6.5% | 15.2 | 1.2% | - |
| hong-kong | 0 | 31 | 0.0% | 12.4 | 1.7% | trees in hong kong (i1, p60) |
| bordeaux | 1 | 30 | 3.3% | 9.4 | 2.8% | sequoia bordeaux (i2, p9) |
| turin | 1 | 28 | 3.6% | 5.2 | 6.6% | alberi monumentali (i1, p8) |
| tokyo | 0 | 28 | 0.0% | 5.7 | 5.6% | - |
| groningen | 1 | 27 | 3.7% | 38.4 | 0.4% | big five groningen (i4, p84) |
| bangkok | 0 | 27 | 0.0% | 10.7 | 2.3% | - |
| warsaw | 1 | 26 | 3.8% | 15.5 | 1.2% | oldest tree in poland (i1, p53) |
| lyon | 0 | 26 | 0.0% | 16.4 | 1.1% | agriates lyon (i1, p64) |
| vilnius | 4 | 25 | 16.0% | 8.1 | 3.5% | willow tree in lithuanian (i3, p9) |
| leiden | 2 | 25 | 8.0% | 16.9 | 1.0% | "oldest of its species" ginkgo park (i2, p10) |
| utrecht | 1 | 25 | 4.0% | 11.7 | 1.9% | ja leuk (i1, p9) |
| cagliari | 0 | 25 | 0.0% | 4.9 | 7.1% | ficus cagliari (i1, p8) |
| genoa | 0 | 25 | 0.0% | 6.5 | 4.5% | - |
| granada | 0 | 25 | 0.0% | 19.8 | 0.8% | granada orange trees (i1, p64) |
| guimaraes | 0 | 25 | 0.0% | 11.3 | 2.0% | pine tree portugal (i2, p18) |
| chicago | 2 | 24 | 8.3% | 10.4 | 2.4% | wooded grove (i1, p48) |
| potsdam | 0 | 24 | 0.0% | 10.2 | 2.4% | jagdschloss glienicke (i1, p12) |
| trieste | 0 | 24 | 0.0% | 10.0 | 2.5% | piazza hortis (i1, p10) |
| aarhus | 1 | 23 | 4.3% | 7.8 | 3.6% | happy pig (i1, p10) |
| belgrade | 0 | 23 | 0.0% | 14.5 | 1.3% | - |
| york | 1 | 22 | 4.5% | 6.5 | 4.5% | - |
| bratislava | 0 | 22 | 0.0% | 9.8 | 2.6% | - |
| cordoba | 0 | 22 | 0.0% | 26.3 | 0.5% | gingko garden (i1, p56) |
| haarlem | 0 | 22 | 0.0% | 30.8 | 0.4% | noble tree (i7, p58) |
| stockholm | 0 | 22 | 0.0% | 7.7 | 3.6% | - |
| ljubljana | 1 | 21 | 4.8% | 11.8 | 1.9% | - |
| strasbourg | 1 | 21 | 4.8% | 7.1 | 3.9% | - |
| cadiz | 0 | 21 | 0.0% | 8.2 | 3.4% | - |
| maastricht | 1 | 20 | 5.0% | 8.6 | 3.2% | trees (i1, p8) |
| osaka | 0 | 20 | 0.0% | 10.0 | 2.5% | - |
| canada | 1 | 19 | 5.3% | 18.5 | 0.9% | oldest tree in canada (i3, p21) |
| caserta | 0 | 19 | 0.0% | 25.3 | 0.6% | parchi caserta (i1, p1) |
| hilo | 0 | 19 | 0.0% | 59.1 | 0.4% | loulu palm (i10, p100) |
| mexico-city | 0 | 19 | 0.0% | 8.7 | 3.1% | ahuehuete (i1, p35) |
| split | 0 | 19 | 0.0% | 8.5 | 3.3% | mediterranean cypress croatia (i2, p8) |
| greece | 1 | 18 | 5.6% | 26.6 | 0.5% | greek trees (i3, p42) |
| kyoto | 1 | 18 | 5.6% | 6.0 | 5.0% | - |
| cyprus | 0 | 18 | 0.0% | 9.7 | 2.7% | oldest tree in cyprus (i2, p9) |
| munich | 0 | 18 | 0.0% | 9.4 | 2.8% | - |
| portugal | 0 | 18 | 0.0% | 61.4 | 0.4% | portugal trees (i2, p71) |
| lucca | 1 | 17 | 5.9% | 9.8 | 2.6% | lucca tree (i1, p10) |
| oxford | 2 | 17 | 11.8% | 7.2 | 3.9% | - |
| setubal | 1 | 17 | 5.9% | 7.1 | 3.9% | - |
| sofia | 1 | 17 | 5.9% | 13.1 | 1.6% | - |
| bergamo | 0 | 17 | 0.0% | 7.3 | 3.9% | parco caprotti (i7, p9) |
| toulouse | 3 | 16 | 18.8% | 10.2 | 2.4% | french plane tree (i1, p44) |
| seattle | 0 | 16 | 0.0% | 6.1 | 4.9% | - |
| antwerp | 0 | 15 | 0.0% | 16.5 | 1.1% | parks near me (i1, p1) |
| perth | 0 | 15 | 0.0% | 20.7 | 0.8% | oldest tree in perth (i1, p10) |
| quebec-city | 0 | 15 | 0.0% | 13.0 | 1.6% | what about quebec (i1, p7) |
| sorrento | 1 | 14 | 7.1% | 21.1 | 0.8% | - |
| arnhem | 0 | 14 | 0.0% | 12.5 | 1.7% | - |
| perugia | 0 | 14 | 0.0% | 5.9 | 5.1% | che albero é (i1, p2) |
| bucaco | 0 | 13 | 0.0% | 12.7 | 1.7% | cedro do bussaco (i2, p2) |
| breda | 0 | 12 | 0.0% | 33.7 | 0.4% | - |
| den-bosch | 0 | 12 | 0.0% | 8.1 | 3.5% | - |
| nara | 0 | 12 | 0.0% | 20.2 | 0.8% | - |
| poznan | 0 | 12 | 0.0% | 26.2 | 0.6% | - |
| rotterdam | 0 | 12 | 0.0% | 15.8 | 1.1% | old tree (i1, p6) |
| tallinn | 0 | 11 | 0.0% | 10.2 | 2.4% | - |
| verona | 0 | 11 | 0.0% | 7.5 | 3.7% | - |
| delft | 1 | 10 | 10.0% | 15.7 | 1.1% | - |
| como | 0 | 10 | 0.0% | 22.5 | 0.7% | lake como tree (i2, p58) |
| graz | 0 | 10 | 0.0% | 10.5 | 2.3% | panoramagasse (i1, p5) |
- Seen, not clicked: /tenerife/el-drago-milenario (c0/i56, 0.0%) for drago milenario (i18, p10); oldest tree in tenerife (i5, p16); tenerife oldest tree (i4, p10)
- Seen, not clicked: /rome (c0/i51, 0.0%) for trees in rome (i13, p18); rome trees (i8, p13); trees in rome italy (i6, p20)
- Seen, not clicked: /las-vegas (c0/i37, 0.0%) for vegas trees (i37, p33)

**Climbing** (this ten days against the ten before it)

| Page | Impressions | Change | Position | Moved | Clicks |
|---|---:|---:|---:|---:|---:|
| /bath/plane-tree-of-abbey-green | 174 | +160 | 8.6 | +1.0 | +1 |
| /milan | 156 | +111 | 10.0 | +0.2 | +0 |
| /barcelona | 147 | +97 | 8.8 | -0.5 | +2 |
| /rome | 217 | +88 | 12.1 | +9.5 | +1 |
| /lisbon | 142 | +75 | 8.3 | +1.8 | +3 |
| /london | 90 | +65 | 27.5 | +24.5 | +0 |
| /florence | 123 | +57 | 10.8 | -2.2 | +0 |
| /venice | 71 | +56 | 10.6 | -1.6 | +3 |

**Newly ranking** (no impressions at all ten days ago)

| Page | Impressions | Clicks | Position |
|---|---:|---:|---:|
| /madrid | 121 | 0 | 13.6 |
| /copenhagen | 119 | 1 | 11.7 |
| /tenerife/el-drago-milenario | 99 | 0 | 11.4 |
| /species/osage-orange | 58 | 0 | 79.4 |
| /amsterdam/last-elm-of-stationsplein | 43 | 2 | 6.7 |
| /las-vegas | 39 | 0 | 31.8 |

**Slipping**

| Page | Impressions | Change | Position | Moved |
|---|---:|---:|---:|---:|
| /lyon | 21 | -18 | 19.4 | -4.1 |
| /granada | 24 | -15 | 20.5 | -11.7 |
| /nice | 24 | -14 | 15.0 | -5.7 |
| /new-york | 21 | -3 | 31.1 | -8.5 |

- New queries this window: dutch elm amsterdam (i32).

**Who they are**
Audience, 28 days of search (307 clicks, 13484 impressions):
- Countries: usa c56/i2985; gbr c33/i1731; nld c24/i620; deu c18/i450; esp c14/i781
- Devices: MOBILE c212/i7314; DESKTOP c94/i6043; TABLET c1/i127
- Landing pages: / c16/i121; /prague c14/i276; /lisbon c11/i284; /amsterdam c7/i380; /athens/holm-oak-of-the-national-garden c6/i14

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-17 | 30 | 90 |
| 08-18 | 40 | 60 |
| 08-19 | 40 | 80 |
| 08-20 | 110 | 180 |
| 08-21 | 40 | 80 |
| 08-22 | 90 | 120 |
| 08-23 | 70 | 120 |
| 08-24 | 10 | 20 |
| **window** | **430** | **750** |
- Top paths: /amsterdam (90); / (90); /copenhagen (60); /explore (40); /athens/holm-oak-of-the-national-garden (20); /cities (20); /toulouse/hackberry-of-place-saint-georges (20); /app (20); /paris (20); /sydney/bidwill-kauri-pine (10); /rome/oldest-tree (10); /aarhus (10)
- Referrers: ancienttrees.app (320); (direct) (290); www.google.com (140)
- Moved between our own pages: 320 of 750 pageviews (43%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: NL (160); US (130); GB (90); DK (60); DE (60)
- Devices: mobile (390); desktop (360)
- Page load (8d): p50 687ms, p90 3611ms

Links: external referrers (a link somebody actually clicked): none yet
AI: arrivals from an assistant that cited us: none yet


**What the night shift did**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 08-24T18:49 | 0.0 | 0 | 0 | 0 | - |
| 08-24T20:36 | 0.0 | 0 | 0 | 0 | - |
| 08-24T22:32 | 0.0 | 0 | 0 | 0 | - |
| 08-25T00:27 | 0.0 | 0 | 0 | 0 | - |
| 08-25T02:48 | 0.0 | 0 | 0 | 0 | - |
| 08-25T04:25 | 0.0 | 0 | 0 | 0 | - |
| **6 runs** | **0** | **0** | **0** | | |

- 6 of 6 produced no trees; 6 wrote nothing to LOG.md.

Machine: 9 chain attempts yesterday, 2 got real work time (~44 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 26 clicks and 730 impressions on Google's freshest day (day before: c15/i957). Directional at best; no strategic conclusions from these volumes.

## 2026-08-23 (previous UTC day)

**Today: nothing here needs you.** The blocks below are the standing picture.

**Did the product happen**
- search-home: 2 yesterday, last yesterday
- app-cta:     1 yesterday, last yesterday
- beacon-fix-verify: 0 yesterday, last 8 days ago
- beacon-test: 0 yesterday, last 8 days ago
- directions:  0 yesterday, last 3 days ago
- save:        0 yesterday, last 2 days ago
- search-explore: 0 yesterday, last 3 days ago
- signin-link-sent: 0 yesterday, last never
- smoke-test:  0 yesterday, last 23 days ago
- suggestion-submit: 0 yesterday, last 4 days ago
- waitlist-submit: 0 yesterday, last 4 days ago
- walk-open:   0 yesterday, last 7 days ago
- walk-start:  0 yesterday, last never
- walks-app:   0 yesterday, last 6 days ago
- worthit-not worth it: 0 yesterday, last 7 days ago
- worthit-worth it: 0 yesterday, last never

| Day | Accounts | Waitlist | Saves | Trees sent | Feedback |
|---|---:|---:|---:|---:|---:|
| 08-10 | 0 | 0 | 0 | 0 | 0 |
| 08-11 | 0 | 0 | 0 | 0 | 0 |
| 08-12 | 0 | 0 | 0 | 0 | 0 |
| 08-13 | 0 | 0 | 0 | 0 | 0 |
| 08-14 | 0 | 1 | 0 | 0 | 0 |
| 08-15 | 0 | 0 | 0 | 0 | 1 |
| 08-16 | 0 | 0 | 0 | 0 | 0 |
| 08-17 | 0 | 1 | 0 | 0 | 2 |
| 08-18 | 0 | 1 | 2 | 0 | 0 |
| 08-19 | 0 | 1 | 0 | 0 | 0 |
| 08-20 | 0 | 1 | 3 | 0 | 1 |
| 08-21 | 1 | 0 | 0 | 0 | 16 |
| 08-22 | 0 | 0 | 1 | 0 | 0 |
| 08-23 | 0 | 0 | 0 | 0 | 0 |
| 08-24 | 0 | 0 | 0 | 0 | 0 |
| **14 days** | **1** | **5** | **6** | **0** | **20** |
- Waitlist:    10 total, newest 4 days ago
- Submissions: 20 total (0 trees sent, 20 feedback), newest 3 days ago
- Accounts:    4 total, newest 3 days ago

**What readers told us** (14 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 08-15 | prg_007 (The Oak of Cisarsky ostro | not worth it | wrong location | no acct | holds |
| 08-17 | hel_006 (The Meilahti Ancient Pine | not worth it | - | no acct | holds |
| 08-17 | lis_005 (The Tipu of Jardim de São | worth it | - | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | holds |
| 08-21 | par_001 (The Robinier of Square Re | not worth it | - | no acct | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | report | could not reach it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | worth it | - | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | not worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |

- 26 of these 33 came from one account (d4e6). At this volume that is almost certainly our own testing rather than readers, and it should be read that way until somebody checks the rows.

**The funnel, as rates**
- Seen to clicked: 2.2% (207 of 9362) vs 2.5% the fortnight before
- Pages per visit: 1.6 (900 visits, 1410 pageviews since 2026-08-08)
- Visits that did something: 7.3% (66 actions on 900 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-14 | 15 | 523 | 2.9% | 13.9 |
| 08-15 | 18 | 645 | 2.8% | 13.8 |
| 08-16 | 15 | 736 | 2.0% | 13.5 |
| 08-17 | 15 | 606 | 2.5% | 14.4 |
| 08-18 | 19 | 609 | 3.1% | 15.0 |
| 08-19 | 18 | 806 | 2.2% | 17.0 |
| 08-20 | 17 | 1022 | 1.7% | 21.5 |
| 08-21 | 18 | 913 | 2.0% | 19.9 |
| 08-22 | 17 | 1030 | 1.7% | 19.9 |
| 08-23 | 13 | 776 | 1.7% | 15.1 |
| **window** | **165** | **7666** | **2.2%** | |
- Top queries (10d): dutch elm amsterdam (i22, p6); oldest tree in central park (i4, p10); oldest tree in dc (i2, p33); "oldest of its species" ginkgo park (i13, p7); "oldest of its species" owl park (i5, p8)
- Top pages (10d): / (c10/i62); /prague (c8/i144); /amsterdam (c5/i144); /athens/holm-oak-of-the-national-garden (c5/i8); /dubrovnik (c4/i61)
- Content lead: 'alameda dos platanos' has no matching page (i15, p8)

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| rome | 3 | 282 | 1.1% | 11.2 | 2.1% | trees in rome (i11, p15) |
| amsterdam | 8 | 274 | 2.9% | 12.0 | 1.8% | dutch elm amsterdam (i17, p6) |
| bath | 2 | 223 | 0.9% | 8.0 | 3.5% | the giant plane tree bath (i10, p11) |
| barcelona | 5 | 207 | 2.4% | 10.3 | 2.4% | barcelona tree (i5, p6) |
| lisbon | 6 | 185 | 3.2% | 9.6 | 2.7% | oldest tree in lisbon (i5, p9) |
| palermo | 3 | 168 | 1.8% | 9.2 | 2.9% | oldest tree in palermo (i4, p10) |
| copenhagen | 6 | 167 | 3.6% | 12.2 | 1.8% | trees in copenhagen (i18, p17) |
| prague | 9 | 166 | 5.4% | 7.4 | 3.8% | four trees prague (i2, p21) |
| singapore | 2 | 162 | 1.2% | 15.2 | 1.2% | oldest tree in singapore (i20, p10) |
| milan | 0 | 161 | 0.0% | 10.8 | 2.2% | "oldest of its species" ginkgo park (i11, p6) |
| tenerife | 0 | 160 | 0.0% | 11.1 | 2.1% | drago milenario (i16, p10) |
| vienna | 3 | 138 | 2.2% | 9.4 | 2.8% | - |
| london | 0 | 137 | 0.0% | 21.7 | 0.7% | london trees (i3, p77) |
| paris | 6 | 134 | 4.5% | 22.0 | 0.7% | palm trees in paris (i3, p61) |
| florence | 0 | 130 | 0.0% | 11.1 | 2.1% | florence tree (i8, p8) |
| madrid | 0 | 126 | 0.0% | 13.0 | 1.6% | oldest tree in madrid (i4, p13) |
| cambridge | 0 | 113 | 0.0% | 34.0 | 0.4% | newton's apple tree (i7, p45) |
| brisbane | 0 | 112 | 0.0% | 15.2 | 1.2% | mahogany (i7, p23) |
| malaga | 2 | 97 | 2.1% | 11.2 | 2.1% | árboles históricos de málaga (i4, p79) |
| brussels | 3 | 93 | 3.2% | 13.9 | 1.4% | belgium national tree (i1, p47) |
| seville | 2 | 89 | 2.2% | 11.5 | 2.0% | - |
| geneva | 1 | 88 | 1.1% | 11.1 | 2.1% | sixty tree (i1, p9) |
| naples | 2 | 87 | 2.3% | 11.4 | 2.0% | a tree in naples (i1, p15) |
| seoul | 0 | 86 | 0.0% | 16.2 | 1.1% | seoul tree (i7, p8) |
| new-york | 3 | 85 | 3.5% | 16.8 | 1.1% | ancient elm (i1, p54) |
| dubrovnik | 4 | 81 | 4.9% | 7.3 | 3.8% | trsteno plane tree (i5, p12) |
| washington-dc | 4 | 79 | 5.1% | 17.1 | 1.0% | survey lodge ranger station (i10, p11) |
| venice | 3 | 77 | 3.9% | 10.5 | 2.3% | trees in venice (i1, p1) |
| porto | 1 | 73 | 1.4% | 5.9 | 5.2% | alameda dos platanos (i15, p8) |
| boston | 0 | 72 | 0.0% | 24.1 | 0.6% | trees in boston (i2, p54) |
| valencia | 1 | 70 | 1.4% | 8.8 | 3.1% | ficus centenarios de la glorieta (i3, p10) |
| dublin | 5 | 69 | 7.2% | 13.6 | 1.5% | buchanan tree (i1, p10) |
| budapest | 1 | 68 | 1.5% | 9.3 | 2.9% | in budapest? (i1, p4) |
| reykjavik | 1 | 65 | 1.5% | 14.0 | 1.4% | oldest tree in iceland (i5, p8) |
| edinburgh | 0 | 65 | 0.0% | 18.9 | 0.9% | john muir grove edinburgh (i2, p8) |
| montreal | 2 | 61 | 3.3% | 11.8 | 1.9% | century trees (i3, p53) |
| istanbul | 2 | 56 | 3.6% | 9.1 | 3.0% | archeologisch museum van istanbul (i1, p1) |
| madeira | 0 | 55 | 0.0% | 7.9 | 3.5% | witch tree fanal (i4, p10) |
| oslo | 0 | 50 | 0.0% | 13.7 | 1.5% | dronningparken (i1, p8) |
| portland | 0 | 48 | 0.0% | 11.7 | 1.9% | trees in portland or (i1, p55) |
| alicante | 1 | 46 | 2.2% | 6.7 | 4.3% | ficus alicante (i5, p9) |
| crete | 0 | 46 | 0.0% | 10.6 | 2.3% | 2000 years old olive tree (i1, p14) |
| the-hague | 2 | 45 | 4.4% | 6.6 | 4.4% | old tree (i1, p9) |
| bristol | 1 | 45 | 2.2% | 23.3 | 0.7% | bristol trees (i6, p55) |
| padua | 1 | 44 | 2.3% | 7.6 | 3.7% | - |
| berlin | 0 | 44 | 0.0% | 16.2 | 1.1% | - |
| krakow | 2 | 41 | 4.9% | 9.3 | 2.9% | - |
| athens | 5 | 40 | 12.5% | 15.3 | 1.2% | old plane tree (i2, p37) |
| zurich | 2 | 40 | 5.0% | 12.2 | 1.8% | zurich (i1, p2) |
| cork | 4 | 39 | 10.3% | 13.5 | 1.5% | oldest tree in ireland (i2, p17) |
| sintra | 2 | 39 | 5.1% | 6.4 | 4.6% | - |
| nice | 0 | 39 | 0.0% | 11.6 | 2.0% | - |
| helsinki | 1 | 37 | 2.7% | 8.7 | 3.2% | helsinki tree (i1, p8) |
| palma-de-mallorca | 0 | 37 | 0.0% | 7.8 | 3.6% | mallorca trees (i1, p11) |
| bologna | 0 | 35 | 0.0% | 6.7 | 4.3% | trees hours (i1, p11) |
| glasgow | 2 | 33 | 6.1% | 14.7 | 1.3% | - |
| fukuoka | 0 | 33 | 0.0% | 8.2 | 3.4% | - |
| hong-kong | 0 | 33 | 0.0% | 12.2 | 1.8% | trees in hong kong (i1, p60) |
| bordeaux | 0 | 32 | 0.0% | 9.3 | 2.9% | sequoia bordeaux (i2, p9) |
| sardinia | 0 | 32 | 0.0% | 8.5 | 3.3% | olivastro santa maria navarrese (i1, p8) |
| lyon | 0 | 31 | 0.0% | 14.8 | 1.2% | agriates lyon (i1, p64) |
| toronto | 0 | 31 | 0.0% | 12.3 | 1.7% | big red oak (i3, p6) |
| bangkok | 0 | 29 | 0.0% | 10.2 | 2.4% | - |
| nijmegen | 0 | 28 | 0.0% | 7.8 | 3.6% | oldest tree in the netherlands (i1, p5) |
| tokyo | 0 | 28 | 0.0% | 5.8 | 5.4% | - |
| leiden | 3 | 27 | 11.1% | 13.0 | 1.6% | "oldest of its species" ginkgo park (i1, p9) |
| groningen | 1 | 27 | 3.7% | 37.6 | 0.4% | big five groningen (i4, p84) |
| granada | 0 | 27 | 0.0% | 19.0 | 0.9% | granada orange trees (i1, p64) |
| haarlem | 0 | 27 | 0.0% | 32.7 | 0.4% | noble tree (i8, p57) |
| turin | 1 | 26 | 3.8% | 4.8 | 7.2% | alberi monumentali (i1, p8) |
| utrecht | 1 | 25 | 4.0% | 14.9 | 1.2% | ja leuk (i1, p9) |
| genoa | 0 | 25 | 0.0% | 6.4 | 4.6% | - |
| strasbourg | 1 | 24 | 4.2% | 6.8 | 4.2% | - |
| warsaw | 1 | 24 | 4.2% | 15.0 | 1.2% | oldest tree in poland (i1, p53) |
| belgrade | 0 | 24 | 0.0% | 14.1 | 1.4% | - |
| osaka | 0 | 24 | 0.0% | 7.0 | 4.0% | meoto kusu (i1, p7) |
| guimaraes | 0 | 23 | 0.0% | 11.8 | 1.9% | pine tree portugal (i2, p18) |
| las-vegas | 0 | 23 | 0.0% | 33.1 | 0.4% | vegas trees (i22, p34) |
| ljubljana | 1 | 22 | 4.5% | 11.5 | 2.0% | - |
| trieste | 0 | 22 | 0.0% | 10.5 | 2.3% | piazza hortis (i1, p10) |
| maastricht | 1 | 21 | 4.8% | 8.2 | 3.4% | trees (i1, p8) |
| cadiz | 0 | 21 | 0.0% | 8.1 | 3.5% | - |
| potsdam | 0 | 21 | 0.0% | 10.9 | 2.2% | jagdschloss glienicke (i1, p12) |
| stockholm | 0 | 21 | 0.0% | 7.6 | 3.7% | - |
| aarhus | 1 | 20 | 5.0% | 7.7 | 3.6% | happy pig (i1, p10) |
| chicago | 1 | 20 | 5.0% | 9.4 | 2.8% | oldest tree in chicago (i1, p17) |
| oxford | 2 | 20 | 10.0% | 7.0 | 4.0% | - |
| setubal | 1 | 20 | 5.0% | 7.1 | 4.0% | - |
| york | 1 | 20 | 5.0% | 6.4 | 4.6% | - |
| bratislava | 0 | 20 | 0.0% | 10.4 | 2.3% | - |
| cordoba | 0 | 20 | 0.0% | 28.8 | 0.4% | gingko garden (i1, p56) |
| vilnius | 4 | 19 | 21.1% | 8.6 | 3.2% | willow tree in lithuanian (i2, p8) |
| kyoto | 1 | 19 | 5.3% | 9.4 | 2.8% | - |
| lucca | 1 | 19 | 5.3% | 9.6 | 2.7% | lucca tree (i1, p10) |
| cagliari | 0 | 19 | 0.0% | 5.0 | 7.0% | ficus cagliari (i1, p8) |
| caserta | 0 | 19 | 0.0% | 25.3 | 0.6% | parchi caserta (i1, p1) |
| portugal | 0 | 19 | 0.0% | 58.5 | 0.4% | portugal trees (i2, p71) |
| toulouse | 3 | 18 | 16.7% | 9.3 | 2.9% | french plane tree (i1, p44) |
| antwerp | 0 | 18 | 0.0% | 18.7 | 0.9% | klaverbladdreef (i1, p83) |
| split | 0 | 18 | 0.0% | 8.2 | 3.4% | mediterranean cypress croatia (i1, p7) |
| bergamo | 0 | 17 | 0.0% | 7.4 | 3.8% | parco caprotti (i8, p9) |
| canada | 1 | 16 | 6.2% | 18.6 | 0.9% | oldest tree in canada (i2, p20) |
| sofia | 1 | 16 | 6.2% | 13.6 | 1.5% | - |
| cyprus | 0 | 16 | 0.0% | 9.6 | 2.7% | oldest tree in cyprus (i1, p8) |
| hilo | 0 | 16 | 0.0% | 63.1 | 0.4% | loulu palm (i9, p100) |
| munich | 0 | 16 | 0.0% | 9.5 | 2.8% | - |
| greece | 1 | 15 | 6.7% | 24.8 | 0.6% | greek trees (i3, p42) |
| perugia | 0 | 15 | 0.0% | 5.6 | 5.8% | che albero é (i1, p2) |
| bucaco | 0 | 14 | 0.0% | 11.9 | 1.8% | cedro do bussaco (i2, p2) |
| perth | 0 | 14 | 0.0% | 21.6 | 0.7% | oldest tree in perth (i1, p10) |
| quebec-city | 0 | 14 | 0.0% | 13.1 | 1.6% | what about quebec (i1, p7) |
| rotterdam | 0 | 14 | 0.0% | 14.1 | 1.4% | old tree (i1, p6) |
| breda | 0 | 13 | 0.0% | 31.7 | 0.4% | - |
| arnhem | 0 | 12 | 0.0% | 14.4 | 1.3% | - |
| hobart | 0 | 12 | 0.0% | 18.8 | 0.9% | oldest trees in tasmania (i1, p61) |
| poznan | 0 | 12 | 0.0% | 26.2 | 0.6% | - |
| como | 0 | 11 | 0.0% | 20.9 | 0.8% | lake como tree (i2, p58) |
| den-bosch | 0 | 11 | 0.0% | 9.1 | 3.0% | - |
| seattle | 0 | 11 | 0.0% | 6.4 | 4.6% | - |
| tallinn | 0 | 11 | 0.0% | 10.2 | 2.4% | - |
| delft | 1 | 10 | 10.0% | 5.6 | 5.8% | - |
| graz | 0 | 10 | 0.0% | 10.5 | 2.3% | panoramagasse (i1, p5) |
| mexico-city | 0 | 10 | 0.0% | 8.3 | 3.3% | - |
| trento | 0 | 10 | 0.0% | 7.0 | 4.0% | - |
| zaragoza | 0 | 10 | 0.0% | 10.5 | 2.3% | - |
- Seen, not clicked: /tenerife/el-drago-milenario (c0/i53, 0.0%) for drago milenario (i16, p10); oldest tree in tenerife (i5, p16); tenerife oldest tree (i4, p10)
- Seen, not clicked: /rome (c0/i49, 0.0%) for trees in rome (i11, p15); rome trees (i8, p13); trees in rome italy (i6, p20)
- Seen, not clicked: /cambridge/newtons-apple-tree (c0/i41, 0.0%) for newton's apple tree (i7, p45); newton apple tree (i4, p45); isaac newton apple tree (i4, p47)

**Climbing** (this ten days against the ten before it)

| Page | Impressions | Change | Position | Moved | Clicks |
|---|---:|---:|---:|---:|---:|
| /bath/plane-tree-of-abbey-green | 177 | +176 | 8.7 | +3.3 | +1 |
| /milan | 144 | +92 | 10.2 | -0.3 | +0 |
| /barcelona | 135 | +84 | 9.0 | -0.7 | +0 |
| /rome | 208 | +65 | 12.8 | +8.6 | +0 |
| /lisbon | 135 | +59 | 8.5 | +2.0 | +2 |
| /prague | 144 | +55 | 7.6 | +1.6 | +4 |
| /florence | 115 | +55 | 10.0 | -1.2 | +0 |
| /london | 77 | +54 | 29.7 | +20.6 | +0 |

**Newly ranking** (no impressions at all ten days ago)

| Page | Impressions | Clicks | Position |
|---|---:|---:|---:|
| /madrid | 110 | 0 | 13.1 |
| /copenhagen | 107 | 1 | 12.0 |
| /tenerife/el-drago-milenario | 90 | 0 | 11.4 |
| /es/malaga | 55 | 0 | 9.9 |
| /es/malaga/ficus-avenue-of-the-alameda-principal | 54 | 1 | 5.5 |
| /species/osage-orange | 52 | 0 | 79.8 |

**Slipping**

| Page | Impressions | Change | Position | Moved |
|---|---:|---:|---:|---:|
| /antwerp | 16 | -14 | 19.9 | -11.8 |
| /granada | 26 | -14 | 19.6 | -10.1 |
| /nice | 25 | -13 | 14.9 | -5.7 |
| /palermo | 143 | -9 | 9.5 | -0.8 |

- New queries this window: dutch elm amsterdam (i22), "oldest of its species" owl park (i5), oldest tree in central park (i4).

**Who they are** (full cut, Mondays)
Audience, 28 days of search (287 clicks, 12778 impressions):
- Countries: usa c49/i2841; gbr c25/i1604; nld c24/i590; deu c17/i433; esp c14/i744
- Devices: MOBILE c199/i6951; DESKTOP c88/i5711; TABLET c0/i116
- Landing pages: / c15/i115; /prague c13/i266; /lisbon c11/i284; /amsterdam c7/i381; /athens/holm-oak-of-the-national-garden c6/i14
- Search language (top 100 named queries, crude match, most clicks are in queries Google withholds): English 65q c3/i195; unclassified 28q c2/i90; Spanish 4q c0/i9; Italian 2q c0/i2; French 1q c0/i2
On the site since 2026-08-08 (900 visits, 1410 pageviews, 1.6 pages per visit):
- Countries: NL 420; US 240; DE 140; PT 90; GB 90
- Devices: desktop 840; mobile 570
- Browsers: Chrome 550; MobileSafari 270; ChromeMobile 230; Unknown 130
- Arrived via: (direct) 630; ancienttrees.app 510; www.google.com 260; zscaler-blocked.dpgmedia.n 10
- Opened: / 180; /amsterdam 100; /app 80; /copenhagen 70; /porto 50; /paris 50; /explore 50; /barcelona 30

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-16 | 110 | 110 |
| 08-17 | 30 | 90 |
| 08-18 | 40 | 60 |
| 08-19 | 40 | 80 |
| 08-20 | 110 | 180 |
| 08-21 | 40 | 80 |
| 08-22 | 90 | 120 |
| 08-23 | 70 | 120 |
| **window** | **530** | **840** |
- Top paths: / (110); /amsterdam (90); /copenhagen (60); /paris (50); /explore (40); /app (30); /athens/holm-oak-of-the-national-garden (20); /toulouse/hackberry-of-place-saint-georges (20); /cities (20); /contribute (10); /singapore/mandela-tree-of-orchid-plaza (10); /london/totteridge-yew (10)
- Referrers: (direct) (360); ancienttrees.app (310); www.google.com (170)
- Moved between our own pages: 310 of 840 pageviews (37%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: NL (190); US (150); GB (90); DE (70); DK (60)
- Devices: desktop (430); mobile (410)
- Page load (8d): p50 691ms, p90 3828ms

Links: external referrers (a link somebody actually clicked): none yet
AI: arrivals from an assistant that cited us: none yet


**What the night shift did**

| Started | Minutes | Turns | Trees | Commits | Refused |
|---|---:|---:|---:|---:|---:|
| 08-23T18:36 | 63.6 | 441 | 17 | 28 | 30 |
| 08-23T20:29 | 9.2 | 67 | 0 | 2 | 13 |
| 08-23T22:28 | 19.4 | 131 | 0 | 5 | 4 |
| 08-24T00:28 | 11.6 | 96 | 6 | 5 | 14 |
| 08-24T02:52 | 31.5 | 174 | 10 | 12 | 32 |
| 08-24T04:32 | 0.0 | 1 | 0 | 0 | 0 |
| **6 runs** | **135** | | **33** | **52** | |

- 3 of 6 produced no trees; 4 to 32 commands refused per run; 5 wrote nothing to LOG.md.

Machine: 9 chain attempts yesterday, 9 got real work time (~333 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 13 clicks and 776 impressions on Google's freshest day (day before: c17/i1030). Directional at best; no strategic conclusions from these volumes.

## 2026-08-22 (previous UTC day)

**Today: nothing here needs you.** The blocks below are the standing picture.

**Did the product happen**
- app-cta:     4 yesterday, last yesterday
- save:        1 yesterday, last yesterday
- beacon-fix-verify: 0 yesterday, last 7 days ago
- beacon-test: 0 yesterday, last 7 days ago
- directions:  0 yesterday, last 2 days ago
- search-explore: 0 yesterday, last 2 days ago
- search-home: 0 yesterday, last 3 days ago
- signin-link-sent: 0 yesterday, last never
- smoke-test:  0 yesterday, last 22 days ago
- suggestion-submit: 0 yesterday, last 3 days ago
- waitlist-submit: 0 yesterday, last 3 days ago
- walk-open:   0 yesterday, last 6 days ago
- walk-start:  0 yesterday, last never
- walks-app:   0 yesterday, last 5 days ago
- worthit-not worth it: 0 yesterday, last 6 days ago
- worthit-worth it: 0 yesterday, last never

| Day | Accounts | Waitlist | Saves | Trees sent | Feedback |
|---|---:|---:|---:|---:|---:|
| 08-09 | 0 | 0 | 0 | 0 | 0 |
| 08-10 | 0 | 0 | 0 | 0 | 0 |
| 08-11 | 0 | 0 | 0 | 0 | 0 |
| 08-12 | 0 | 0 | 0 | 0 | 0 |
| 08-13 | 0 | 0 | 0 | 0 | 0 |
| 08-14 | 0 | 1 | 0 | 0 | 0 |
| 08-15 | 0 | 0 | 0 | 0 | 1 |
| 08-16 | 0 | 0 | 0 | 0 | 0 |
| 08-17 | 0 | 1 | 0 | 0 | 2 |
| 08-18 | 0 | 1 | 2 | 0 | 0 |
| 08-19 | 0 | 1 | 0 | 0 | 0 |
| 08-20 | 0 | 1 | 3 | 0 | 1 |
| 08-21 | 1 | 0 | 0 | 0 | 16 |
| 08-22 | 0 | 0 | 1 | 0 | 0 |
| 08-23 | 0 | 0 | 0 | 0 | 0 |
| **14 days** | **1** | **5** | **6** | **0** | **20** |
- Waitlist:    10 total, newest 3 days ago
- Submissions: 20 total (0 trees sent, 20 feedback), newest 2 days ago
- Accounts:    4 total, newest 2 days ago

**What readers told us** (14 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 08-15 | prg_007 (The Oak of Cisarsky ostro | not worth it | wrong location | no acct | - |
| 08-17 | hel_006 (The Meilahti Ancient Pine | not worth it | - | no acct | - |
| 08-17 | lis_005 (The Tipu of Jardim de São | worth it | - | no acct | - |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | - |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | - |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | - |
| 08-21 | par_001 (The Robinier of Square Re | not worth it | - | no acct | - |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | report | could not reach it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | worth it | - | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | not worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |

- 26 of these 33 came from one account (d4e6). At this volume that is almost certainly our own testing rather than readers, and it should be read that way until somebody checks the rows.

**The funnel, as rates**
- Seen to clicked: 2.3% (195 of 8630) vs 2.2% the fortnight before
- Pages per visit: 1.6 (830 visits, 1290 pageviews since 2026-08-08)
- Visits that did something: 7.6% (63 actions on 830 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-13 | 9 | 446 | 2.0% | 17.5 |
| 08-14 | 15 | 523 | 2.9% | 13.9 |
| 08-15 | 18 | 645 | 2.8% | 13.8 |
| 08-16 | 15 | 736 | 2.0% | 13.5 |
| 08-17 | 15 | 606 | 2.5% | 14.4 |
| 08-18 | 19 | 609 | 3.1% | 15.0 |
| 08-19 | 18 | 806 | 2.2% | 17.0 |
| 08-20 | 17 | 1022 | 1.7% | 21.5 |
| 08-21 | 18 | 913 | 2.0% | 19.9 |
| 08-22 | 12 | 769 | 1.6% | 18.5 |
| **window** | **156** | **7075** | **2.2%** | |
- Top queries (10d): dutch elm amsterdam (i15, p6); juttepeer (i2, p3); oldest tree in central park (i4, p10); oldest tree in dc (i3, p26); "oldest of its species" ginkgo park (i12, p7)
- Top pages (10d): / (c10/i58); /prague (c7/i141); /amsterdam (c5/i127); /athens/holm-oak-of-the-national-garden (c5/i8); /dubrovnik (c4/i65)
- Content lead: 'alameda dos platanos' has no matching page (i13, p8)

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| rome | 3 | 249 | 1.2% | 11.0 | 2.2% | trees in rome (i10, p17) |
| amsterdam | 7 | 223 | 3.1% | 13.3 | 1.5% | dutch elm amsterdam (i11, p6) |
| bath | 2 | 206 | 1.0% | 8.2 | 3.4% | the giant plane tree bath (i10, p11) |
| barcelona | 4 | 200 | 2.0% | 9.8 | 2.6% | barcelona tree (i5, p6) |
| palermo | 2 | 175 | 1.1% | 9.4 | 2.8% | oldest tree in palermo (i4, p10) |
| lisbon | 6 | 170 | 3.5% | 10.1 | 2.5% | oldest tree in lisbon (i6, p9) |
| prague | 8 | 163 | 4.9% | 7.8 | 3.6% | four trees prague (i2, p21) |
| singapore | 2 | 156 | 1.3% | 15.0 | 1.2% | oldest tree in singapore (i19, p10) |
| milan | 0 | 149 | 0.0% | 10.7 | 2.2% | "oldest of its species" ginkgo park (i10, p6) |
| copenhagen | 2 | 136 | 1.5% | 13.2 | 1.6% | trees in copenhagen (i15, p16) |
| vienna | 3 | 135 | 2.2% | 8.8 | 3.1% | - |
| paris | 6 | 134 | 4.5% | 21.7 | 0.7% | paris trees (i2, p62) |
| london | 0 | 130 | 0.0% | 23.2 | 0.7% | london trees (i2, p76) |
| florence | 0 | 128 | 0.0% | 11.2 | 2.1% | florence tree (i7, p8) |
| madrid | 0 | 113 | 0.0% | 13.2 | 1.6% | oldest tree in madrid (i3, p15) |
| tenerife | 0 | 111 | 0.0% | 11.8 | 1.9% | drago milenario (i13, p10) |
| cambridge | 0 | 110 | 0.0% | 35.1 | 0.4% | newton's apple tree (i7, p45) |
| brussels | 3 | 96 | 3.1% | 16.4 | 1.1% | turners oak (i3, p31) |
| new-york | 3 | 91 | 3.3% | 17.5 | 1.0% | ancient elm (i1, p54) |
| geneva | 1 | 87 | 1.1% | 10.7 | 2.3% | sixty tree (i1, p9) |
| dubrovnik | 4 | 85 | 4.7% | 7.3 | 3.9% | trsteno plane tree (i5, p12) |
| malaga | 2 | 82 | 2.4% | 11.1 | 2.1% | árboles históricos de málaga (i4, p76) |
| washington-dc | 3 | 81 | 3.7% | 16.9 | 1.1% | survey lodge ranger station (i9, p10) |
| boston | 0 | 81 | 0.0% | 21.5 | 0.7% | trees in boston (i2, p54) |
| brisbane | 0 | 80 | 0.0% | 16.5 | 1.1% | the big macadamia nut (i3, p75) |
| dublin | 5 | 77 | 6.5% | 14.5 | 1.3% | buchanan tree (i1, p10) |
| naples | 2 | 75 | 2.7% | 9.6 | 2.7% | a tree in naples (i1, p15) |
| seoul | 0 | 74 | 0.0% | 16.7 | 1.1% | seoul tree (i7, p8) |
| venice | 3 | 71 | 4.2% | 10.8 | 2.2% | trees in venice (i1, p1) |
| budapest | 1 | 71 | 1.4% | 9.1 | 2.9% | in budapest? (i1, p4) |
| valencia | 1 | 70 | 1.4% | 8.6 | 3.2% | ficus valencia (i2, p12) |
| porto | 1 | 69 | 1.4% | 5.8 | 5.4% | alameda dos platanos (i13, p8) |
| istanbul | 2 | 67 | 3.0% | 11.9 | 1.9% | archeologisch museum van istanbul (i1, p1) |
| edinburgh | 1 | 65 | 1.5% | 21.9 | 0.7% | edinburgh tree map (i1, p52) |
| reykjavik | 1 | 62 | 1.6% | 13.9 | 1.4% | oldest tree in iceland (i5, p8) |
| seville | 2 | 61 | 3.3% | 13.2 | 1.6% | - |
| the-hague | 5 | 51 | 9.8% | 6.2 | 4.8% | juttepeer (i2, p3) |
| krakow | 2 | 50 | 4.0% | 9.0 | 3.0% | - |
| montreal | 1 | 50 | 2.0% | 13.0 | 1.6% | century trees (i3, p53) |
| oslo | 1 | 50 | 2.0% | 13.3 | 1.5% | dronningparken (i1, p8) |
| bristol | 1 | 48 | 2.1% | 23.0 | 0.7% | bristol trees (i7, p53) |
| madeira | 0 | 48 | 0.0% | 7.5 | 3.7% | witch tree fanal (i4, p10) |
| padua | 1 | 44 | 2.3% | 7.2 | 3.9% | - |
| zurich | 2 | 44 | 4.5% | 11.6 | 1.9% | zurich (i1, p2) |
| berlin | 0 | 43 | 0.0% | 18.9 | 0.9% | - |
| nice | 0 | 43 | 0.0% | 13.8 | 1.4% | - |
| portland | 0 | 43 | 0.0% | 12.3 | 1.7% | trees in portland or (i1, p55) |
| alicante | 1 | 42 | 2.4% | 6.4 | 4.6% | ficus alicante (i5, p9) |
| sintra | 1 | 39 | 2.6% | 6.5 | 4.5% | - |
| helsinki | 1 | 38 | 2.6% | 8.6 | 3.2% | helsinki tree (i1, p8) |
| athens | 5 | 37 | 13.5% | 14.6 | 1.3% | old plane tree (i2, p37) |
| cork | 3 | 37 | 8.1% | 13.9 | 1.4% | oldest tree in ireland (i2, p17) |
| lyon | 0 | 37 | 0.0% | 15.9 | 1.1% | agriates lyon (i1, p64) |
| glasgow | 2 | 35 | 5.7% | 14.9 | 1.2% | - |
| crete | 0 | 34 | 0.0% | 12.1 | 1.8% | oldest olive tree crete (i1, p21) |
| hong-kong | 0 | 34 | 0.0% | 13.7 | 1.5% | trees in hong kong (i1, p60) |
| bangkok | 0 | 31 | 0.0% | 9.9 | 2.5% | bangkok trees (i1, p9) |
| nijmegen | 0 | 31 | 0.0% | 11.0 | 2.1% | oldest tree in the netherlands (i1, p5) |
| haarlem | 0 | 30 | 0.0% | 35.3 | 0.4% | noble tree (i9, p57) |
| granada | 0 | 29 | 0.0% | 18.2 | 0.9% | granada orange trees (i1, p64) |
| leiden | 3 | 28 | 10.7% | 12.9 | 1.6% | "oldest of its species" ginkgo park (i1, p9) |
| groningen | 1 | 28 | 3.6% | 37.3 | 0.4% | big five groningen (i4, p84) |
| palma-de-mallorca | 0 | 28 | 0.0% | 8.2 | 3.4% | mallorca trees (i1, p11) |
| tokyo | 0 | 28 | 0.0% | 9.6 | 2.7% | - |
| turin | 1 | 27 | 3.7% | 5.2 | 6.6% | alberi monumentali (i1, p8) |
| fukuoka | 0 | 27 | 0.0% | 7.6 | 3.7% | - |
| bordeaux | 0 | 26 | 0.0% | 9.3 | 2.9% | caucasian elm (i1, p9) |
| utrecht | 1 | 25 | 4.0% | 18.2 | 0.9% | ja leuk (i1, p9) |
| bologna | 0 | 25 | 0.0% | 6.8 | 4.2% | trees hours (i1, p11) |
| oxford | 2 | 24 | 8.3% | 6.9 | 4.1% | - |
| cadiz | 0 | 24 | 0.0% | 7.4 | 3.8% | how old (i1, p1) |
| genoa | 0 | 24 | 0.0% | 6.3 | 4.7% | - |
| osaka | 0 | 24 | 0.0% | 6.7 | 4.3% | meoto kusu (i1, p7) |
| toronto | 0 | 24 | 0.0% | 12.4 | 1.7% | big red oak (i3, p6) |
| sardinia | 0 | 23 | 0.0% | 9.1 | 3.0% | olivastri millenari di luras / s'ozzastr (i1, p11) |
| warsaw | 0 | 23 | 0.0% | 15.7 | 1.1% | oldest tree in poland (i1, p53) |
| ljubljana | 1 | 22 | 4.5% | 11.5 | 2.0% | - |
| strasbourg | 0 | 22 | 0.0% | 6.9 | 4.1% | - |
| trieste | 0 | 22 | 0.0% | 10.7 | 2.3% | piazza hortis (i1, p10) |
| belgrade | 0 | 21 | 0.0% | 12.9 | 1.6% | - |
| stockholm | 0 | 21 | 0.0% | 7.6 | 3.7% | - |
| antwerp | 1 | 20 | 5.0% | 18.0 | 1.0% | klaverbladdreef (i1, p83) |
| lucca | 1 | 20 | 5.0% | 9.6 | 2.7% | lucca tree (i2, p10) |
| setubal | 1 | 20 | 5.0% | 7.1 | 4.0% | - |
| bratislava | 0 | 20 | 0.0% | 10.4 | 2.3% | - |
| guimaraes | 0 | 20 | 0.0% | 12.3 | 1.7% | pine tree portugal (i1, p17) |
| potsdam | 0 | 20 | 0.0% | 11.0 | 2.1% | jagdschloss glienicke (i1, p12) |
| caserta | 0 | 19 | 0.0% | 25.5 | 0.6% | parchi caserta (i1, p1) |
| kyoto | 0 | 19 | 0.0% | 13.7 | 1.5% | kyoto tree (i1, p5) |
| maastricht | 0 | 19 | 0.0% | 8.2 | 3.4% | trees (i1, p8) |
| portugal | 0 | 19 | 0.0% | 57.5 | 0.4% | portugal trees (i2, p71) |
| munich | 1 | 18 | 5.6% | 6.2 | 4.8% | - |
| cagliari | 0 | 18 | 0.0% | 5.2 | 6.6% | ficus cagliari (i1, p8) |
| split | 0 | 18 | 0.0% | 7.4 | 3.8% | mediterranean cypress croatia (i1, p7) |
| toulouse | 3 | 17 | 17.6% | 9.5 | 2.8% | french plane tree (i1, p44) |
| cordoba | 0 | 17 | 0.0% | 25.4 | 0.6% | gingko garden (i1, p56) |
| rotterdam | 0 | 17 | 0.0% | 12.3 | 1.7% | old tree (i1, p6) |
| sofia | 1 | 16 | 6.2% | 13.6 | 1.5% | - |
| york | 1 | 16 | 6.2% | 6.4 | 4.6% | - |
| bergamo | 0 | 16 | 0.0% | 7.4 | 3.8% | parco caprotti (i7, p9) |
| vilnius | 4 | 15 | 26.7% | 8.9 | 3.0% | - |
| chicago | 1 | 15 | 6.7% | 12.7 | 1.7% | oldest tree in chicago (i1, p17) |
| cyprus | 0 | 15 | 0.0% | 10.0 | 2.5% | oldest tree in cyprus (i1, p8) |
| breda | 0 | 14 | 0.0% | 30.5 | 0.4% | ulvenhoutselaan (i1, p13) |
| perugia | 0 | 14 | 0.0% | 5.9 | 5.3% | - |
| aarhus | 1 | 13 | 7.7% | 6.9 | 4.1% | happy pig (i1, p10) |
| canada | 1 | 13 | 7.7% | 20.0 | 0.8% | ancient tree (i1, p27) |
| thessaloniki | 1 | 13 | 7.7% | 15.5 | 1.2% | - |
| bucaco | 0 | 13 | 0.0% | 6.7 | 4.3% | cedro do bussaco (i2, p2) |
| greece | 1 | 12 | 8.3% | 29.5 | 0.4% | greek trees (i3, p42) |
| arnhem | 0 | 12 | 0.0% | 14.4 | 1.3% | - |
| den-bosch | 0 | 12 | 0.0% | 8.8 | 3.1% | - |
| hobart | 0 | 12 | 0.0% | 18.8 | 0.9% | oldest trees in tasmania (i1, p61) |
| como | 0 | 11 | 0.0% | 20.9 | 0.8% | lake como tree (i2, p58) |
| hilo | 0 | 11 | 0.0% | 72.0 | 0.4% | loulu palm (i7, p99) |
| poznan | 0 | 11 | 0.0% | 28.5 | 0.5% | - |
| tallinn | 0 | 11 | 0.0% | 10.2 | 2.4% | - |
| bucharest | 0 | 10 | 0.0% | 13.8 | 1.4% | - |
| las-vegas | 0 | 10 | 0.0% | 36.0 | 0.4% | vegas trees (i10, p36) |
| trento | 0 | 10 | 0.0% | 7.0 | 4.0% | - |
| zaragoza | 0 | 10 | 0.0% | 10.5 | 2.3% | - |
- Seen, not clicked: /cambridge/newtons-apple-tree (c0/i41, 0.0%) for newton's apple tree (i7, p45); newton apple tree (i4, p45); isaac newton apple tree (i4, p47)
- Seen, not clicked: /rome (c0/i37, 0.0%) for trees in rome (i10, p17); rome trees (i5, p15); roman trees (i3, p22)
- Seen, not clicked: /tenerife/el-drago-milenario (c0/i37, 0.0%) for drago milenario (i13, p10); tenerife oldest tree (i3, p10); oldest tree in tenerife (i3, p19)

**Climbing** (this ten days against the ten before it)

| Page | Impressions | Change | Position | Moved | Clicks |
|---|---:|---:|---:|---:|---:|
| /barcelona | 128 | +83 | 8.1 | -0.2 | -1 |
| /milan | 132 | +77 | 10.0 | - | +0 |
| /paris | 93 | +63 | 24.1 | +3.2 | +4 |
| /prague | 141 | +62 | 8.2 | +0.5 | +3 |
| /florence | 113 | +59 | 10.2 | -1.4 | +0 |
| /dubrovnik | 65 | +54 | 5.8 | +0.4 | +3 |
| /species/ginkgo | 59 | +52 | 46.0 | +4.1 | +0 |
| /london | 76 | +51 | 31.5 | +17.2 | +0 |

**Newly ranking** (no impressions at all ten days ago)

| Page | Impressions | Clicks | Position |
|---|---:|---:|---:|
| /bath/plane-tree-of-abbey-green | 164 | 1 | 8.9 |
| /madrid | 97 | 0 | 13.3 |
| /copenhagen | 88 | 0 | 12.2 |
| /tenerife/el-drago-milenario | 62 | 0 | 11.9 |
| /es/malaga | 55 | 0 | 9.9 |
| /es/malaga/ficus-avenue-of-the-alameda-principal | 49 | 1 | 5.4 |

**Slipping**

| Page | Impressions | Change | Position | Moved |
|---|---:|---:|---:|---:|
| /istanbul | 22 | -30 | 16.0 | -6.5 |
| /amsterdam | 127 | -22 | 13.3 | -0.7 |
| /explore | 15 | -20 | 11.3 | -3.7 |
| /nice | 28 | -14 | 18.0 | -12.3 |

- New queries this window: dutch elm amsterdam (i15), oldest tree in central park (i4), oldest tree in dc (i3).

**Who they are**
Audience, 28 days of search (270 clicks, 11938 impressions):
- Countries: usa c47/i2664; gbr c23/i1483; nld c22/i560; deu c15/i400; esp c14/i688
- Devices: MOBILE c187/i6439; DESKTOP c83/i5391; TABLET c0/i108
- Landing pages: / c15/i108; /lisbon c12/i272; /prague c12/i251; /amsterdam c7/i372; /athens/holm-oak-of-the-national-garden c6/i14

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-15 | 30 | 50 |
| 08-16 | 110 | 110 |
| 08-17 | 30 | 90 |
| 08-18 | 40 | 60 |
| 08-19 | 40 | 80 |
| 08-20 | 110 | 180 |
| 08-21 | 40 | 80 |
| 08-22 | 90 | 120 |
| **window** | **490** | **770** |
- Top paths: / (100); /amsterdam (80); /paris (50); /explore (30); /copenhagen (30); /athens/holm-oak-of-the-national-garden (20); /app (20); /toulouse/hackberry-of-place-saint-georges (20); /contribute (10); /london/totteridge-yew (10); /aarhus (10); /rome/oldest-tree (10)
- Referrers: (direct) (310); ancienttrees.app (280); www.google.com (180)
- Moved between our own pages: 280 of 770 pageviews (36%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: NL (180); US (150); GB (90); DK (60); AU (40)
- Devices: desktop (400); mobile (370)
- Page load (8d): p50 664ms, p90 3197ms

Links: external referrers (a link somebody actually clicked): none yet
AI: arrivals from an assistant that cited us: none yet


**What the night shift did**

| Started | Minutes | Turns | Trees | Commits | Refused |
|---|---:|---:|---:|---:|---:|
| 08-22T18:37 | 24.1 | 226 | 0 | 6 | 29 |
| 08-22T20:29 | 13.1 | 107 | 0 | 4 | 18 |
| 08-22T22:27 | 23.3 | 209 | 5 | 10 | 30 |
| 08-23T00:28 | 34.4 | 317 | 12 | 13 | 21 |
| 08-23T02:52 | 69.1 | 470 | 70 | 15 | 25 |
| 08-23T04:24 | 21.1 | 197 | 22 | 12 | 11 |
| **6 runs** | **185** | | **109** | **60** | |

- 2 of 6 produced no trees; 11 to 30 commands refused per run; 5 wrote nothing to LOG.md.

Machine: 14 chain attempts yesterday, 10 got real work time (~266 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 12 clicks and 769 impressions on Google's freshest day (day before: c18/i913). Directional at best; no strategic conclusions from these volumes.

## 2026-08-21 (previous UTC day)

**Today: 16 feedback reports arrived yesterday (20 total); an account was opened yesterday (4 total).**

**Did the product happen**
- directions:  2 yesterday, last yesterday
- search-explore: 2 yesterday, last yesterday
- app-cta:     0 yesterday, last 2 days ago
- beacon-fix-verify: 0 yesterday, last 6 days ago
- beacon-test: 0 yesterday, last 6 days ago
- save:        0 yesterday, last today
- search-home: 0 yesterday, last 2 days ago
- signin-link-sent: 0 yesterday, last never
- smoke-test:  0 yesterday, last 21 days ago
- suggestion-submit: 0 yesterday, last 2 days ago
- waitlist-submit: 0 yesterday, last 2 days ago
- walk-open:   0 yesterday, last 5 days ago
- walk-start:  0 yesterday, last never
- walks-app:   0 yesterday, last 4 days ago
- worthit-not worth it: 0 yesterday, last 5 days ago
- worthit-worth it: 0 yesterday, last never

| Day | Accounts | Waitlist | Saves | Trees sent | Feedback |
|---|---:|---:|---:|---:|---:|
| 08-08 | 1 | 1 | 0 | 0 | 0 |
| 08-09 | 0 | 0 | 0 | 0 | 0 |
| 08-10 | 0 | 0 | 0 | 0 | 0 |
| 08-11 | 0 | 0 | 0 | 0 | 0 |
| 08-12 | 0 | 0 | 0 | 0 | 0 |
| 08-13 | 0 | 0 | 0 | 0 | 0 |
| 08-14 | 0 | 1 | 0 | 0 | 0 |
| 08-15 | 0 | 0 | 0 | 0 | 1 |
| 08-16 | 0 | 0 | 0 | 0 | 0 |
| 08-17 | 0 | 1 | 0 | 0 | 2 |
| 08-18 | 0 | 1 | 2 | 0 | 0 |
| 08-19 | 0 | 1 | 0 | 0 | 0 |
| 08-20 | 0 | 1 | 3 | 0 | 1 |
| 08-21 | 1 | 0 | 0 | 0 | 16 |
| 08-22 | 0 | 0 | 1 | 0 | 0 |
| **14 days** | **2** | **6** | **6** | **0** | **20** |
- Waitlist:    10 total, newest 2 days ago
- Submissions: 20 total (0 trees sent, 20 feedback), newest yesterday
- Accounts:    4 total, newest yesterday

**What readers told us** (14 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 08-15 | prg_007 (The Oak of Cisarsky ostro | not worth it | wrong location | no acct | - |
| 08-17 | hel_006 (The Meilahti Ancient Pine | not worth it | - | no acct | - |
| 08-17 | lis_005 (The Tipu of Jardim de São | worth it | - | no acct | - |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | - |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | - |
| 08-20 | Elm | correction sent in | 374 chars, read it in the database | no acct | - |
| 08-21 | par_001 (The Robinier of Square Re | not worth it | - | no acct | - |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | report | could not reach it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | not worth it | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | not worth it | - | d4e6 | holds |
| 08-21 | rom_001 (The Ginkgo of Villa Sciar | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | worth it | - | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | vote undone | worth it | d4e6 | holds |
| 08-21 | ams_004 (The Wertheimpark Wingnut) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | not worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | worth it | - | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | vote undone | worth it | d4e6 | holds |
| 08-21 | utr_005 (Onder de Linden) | not worth it | - | d4e6 | holds |

- 26 of these 33 came from one account (d4e6). At this volume that is almost certainly our own testing rather than readers, and it should be read that way until somebody checks the rows.

**The funnel, as rates**
- Seen to clicked: 2.4% (190 of 7899) vs 2.2% the fortnight before
- Pages per visit: 1.6 (740 visits, 1170 pageviews since 2026-08-08)
- Visits that did something: 8.0% (59 actions on 740 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-12 | 9 | 441 | 2.0% | 19.1 |
| 08-13 | 9 | 446 | 2.0% | 17.5 |
| 08-14 | 15 | 523 | 2.9% | 13.9 |
| 08-15 | 18 | 645 | 2.8% | 13.8 |
| 08-16 | 15 | 736 | 2.0% | 13.5 |
| 08-17 | 15 | 606 | 2.5% | 14.4 |
| 08-18 | 19 | 609 | 3.1% | 15.0 |
| 08-19 | 18 | 806 | 2.2% | 17.0 |
| 08-20 | 17 | 1022 | 1.7% | 21.5 |
| 08-21 | 18 | 757 | 2.4% | 20.2 |
| **window** | **153** | **6591** | **2.3%** | |
- Top queries (10d): dutch elm amsterdam (i12, p6); juttepeer (i2, p3); oldest tree in central park (i4, p10); oldest tree in dc (i2, p10); "oldest of its species" ginkgo park (i8, p7)

**Every page that got a click** (10 days)

| Page | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| / | 9 | 55 | 16.4% | 18.5 |
| /prague | 7 | 138 | 5.1% | 7.4 |
| /athens/holm-oak-of-the-national-garden | 5 | 8 | 62.5% | 3.9 |
| /amsterdam | 4 | 130 | 3.1% | 13.4 |
| /lisbon | 4 | 115 | 3.5% | 9.3 |
| /paris | 4 | 87 | 4.6% | 25.4 |
| /dubrovnik | 4 | 65 | 6.2% | 5.8 |
| /brussels | 3 | 72 | 4.2% | 16.2 |
| /venice | 3 | 50 | 6.0% | 11.7 |
| /dublin | 3 | 47 | 6.4% | 18.0 |
| /the-hague | 3 | 26 | 11.5% | 6.7 |
| /new-york/sassafras-of-green-wood | 3 | 6 | 50.0% | 2.8 |
| /palermo | 2 | 158 | 1.3% | 9.2 |
| /groningen | 2 | 21 | 9.5% | 34.9 |
| /leiden | 2 | 21 | 9.5% | 7.4 |
| /dublin/queen-victorias-sequoia | 2 | 17 | 11.8% | 5.2 |
| /kyoto | 2 | 15 | 13.3% | 16.5 |
| /toulouse | 2 | 5 | 40.0% | 2.4 |
| /vilnius/oldest-tree | 2 | 5 | 40.0% | 15.6 |
| /paris/great-plane-of-parc-monceau | 2 | 2 | 100.0% | 5.0 |
| /rome | 1 | 176 | 0.6% | 15.1 |
| /bath/plane-tree-of-abbey-green | 1 | 141 | 0.7% | 8.9 |
| /vienna | 1 | 101 | 1.0% | 9.3 |
| /malaga | 1 | 67 | 1.5% | 13.0 |
| /budapest | 1 | 42 | 2.4% | 9.2 |
| /es/malaga/ficus-avenue-of-the-alameda-principal | 1 | 41 | 2.4% | 5.3 |
| /washington-dc | 1 | 34 | 2.9% | 16.4 |
| /sintra | 1 | 33 | 3.0% | 6.1 |
| /zurich | 1 | 29 | 3.4% | 8.3 |
| /glasgow | 1 | 27 | 3.7% | 18.0 |
| /reykjavik | 1 | 27 | 3.7% | 21.3 |
| /species/european-yew | 1 | 25 | 4.0% | 39.0 |
| /antwerp | 1 | 24 | 4.2% | 16.2 |
| /collections/the-oldest-tree-in-every-country-we-map | 1 | 21 | 4.8% | 33.2 |
| /singapore/bodhi-tree-of-pearls-hill | 1 | 21 | 4.8% | 9.8 |
| /munich | 1 | 18 | 5.6% | 6.3 |
| /krakow | 1 | 17 | 5.9% | 6.5 |
| /species/oriental-plane | 1 | 17 | 5.9% | 43.5 |
| /amsterdam/last-elm-of-stationsplein | 1 | 16 | 6.2% | 6.9 |
| /seville | 1 | 16 | 6.2% | 16.9 |
| /tokyo | 1 | 15 | 6.7% | 28.9 |
| /species/wych-elm | 1 | 14 | 7.1% | 75.6 |
| /alicante/ficus-of-parque-de-canalejas | 1 | 13 | 7.7% | 7.6 |
| /collections/trees-planted-by-kings | 1 | 13 | 7.7% | 17.4 |
| /cork/oldest-tree | 1 | 13 | 7.7% | 14.8 |
| /istanbul/oldest-plane-of-bahcekoy | 1 | 13 | 7.7% | 9.9 |
| /sofia/oldest-tree | 1 | 12 | 8.3% | 11.8 |
| /barcelona/wild-olive-of-park-guell | 1 | 11 | 9.1% | 5.8 |
| /parks/national-botanic-gardens-dublin | 1 | 11 | 9.1% | 12.5 |
| /canada | 1 | 10 | 10.0% | 23.5 |
| /collections | 1 | 10 | 10.0% | 26.3 |
| /edinburgh/john-muir-grove | 1 | 10 | 10.0% | 8.6 |
| /istanbul/gulhane-nettle-tree | 1 | 10 | 10.0% | 6.6 |
| /oxford/iffley-yew | 1 | 10 | 10.0% | 7.3 |
| /cork | 1 | 9 | 11.1% | 21.0 |
| /lucca | 1 | 9 | 11.1% | 7.9 |
| /oxford/oldest-tree | 1 | 8 | 12.5% | 5.6 |
| /krakow/oldest-tree | 1 | 7 | 14.3% | 6.1 |
| /parks/central-park-new-york | 1 | 7 | 14.3% | 17.7 |
| /rome/oldest-tree | 1 | 7 | 14.3% | 3.0 |
| /sintra/pohutukawa-of-monserrate | 1 | 7 | 14.3% | 8.7 |
| /washington-dc/oldest-tree | 1 | 7 | 14.3% | 37.9 |
| /cordoba/orange-courtyard-of-the-mezquita | 1 | 6 | 16.7% | 33.5 |
| /cork/great-western-red-cedar-of-blarney | 1 | 6 | 16.7% | 8.0 |
| /countries | 1 | 6 | 16.7% | 6.3 |
| /oslo/oldest-tree | 1 | 6 | 16.7% | 11.8 |
| /zurich/alfred-eschers-giant-sequoia | 1 | 6 | 16.7% | 6.2 |
| /barcelona/oldest-tree | 1 | 5 | 20.0% | 2.8 |
| /bristol/sweet-chestnut-of-ashton-park | 1 | 5 | 20.0% | 11.8 |
| /chicago/oldest-tree | 1 | 5 | 20.0% | 6.0 |
| /lisbon/oldest-tree | 1 | 5 | 20.0% | 7.0 |
| /rome/magnolia-of-via-corsini | 1 | 5 | 20.0% | 3.6 |
| /the-hague/juttepeer-of-heilige-geesthofje | 1 | 5 | 20.0% | 5.0 |
| /barcelona/london-plane-of-the-ciutadella | 1 | 4 | 25.0% | 5.2 |
| /helsinki/meilahti-ancient-pine | 1 | 4 | 25.0% | 6.0 |
| /ljubljana/marmontova-lipa | 1 | 4 | 25.0% | 23.2 |
| /parks/singapore-botanic-gardens-singapore | 1 | 4 | 25.0% | 10.0 |
| /singapore/mandela-tree-of-orchid-plaza | 1 | 4 | 25.0% | 3.0 |
| /thessaloniki/oldest-tree | 1 | 4 | 25.0% | 33.2 |
| /bath/coast-redwood-of-the-great-dell | 1 | 3 | 33.3% | 6.0 |
| /glasgow/holmwoods-giant-redwoods | 1 | 3 | 33.3% | 3.7 |
| /lisbon/ajuda-dragon-tree | 1 | 3 | 33.3% | 2.7 |
| /montreal/last-elm-of-mont-royal | 1 | 3 | 33.3% | 4.7 |
| /naples/eucalyptus-of-the-villa-comunale | 1 | 3 | 33.3% | 4.7 |
| /setubal/peruvian-pepper-of-the-jardim-de-palhais | 1 | 3 | 33.3% | 6.3 |
| /seville/magnolia-of-the-real-alcazar | 1 | 3 | 33.3% | 5.0 |
| /the-hague/oldest-tree | 1 | 3 | 33.3% | 3.3 |
| /washington-dc/willow-oak-circle | 1 | 3 | 33.3% | 9.7 |
| /aarhus/wild-service-tree-of-moesgard | 1 | 2 | 50.0% | 6.0 |
| /barcelona/himalayan-cedar-of-the-labyrinth | 1 | 2 | 50.0% | 8.0 |
| /barcelona/pica-pica-tree-of-the-teatre-grec | 1 | 2 | 50.0% | 6.5 |
| /copenhagen/skovfogedegen | 1 | 2 | 50.0% | 5.5 |
| /dallas | 1 | 2 | 50.0% | 2.5 |
| /geneva/grange-cedar | 1 | 2 | 50.0% | 2.0 |
| /leiden/beets-beech-of-the-burcht | 1 | 2 | 50.0% | 10.0 |
| /paris/old-hazel-of-square-maurice-gardette | 1 | 2 | 50.0% | 2.5 |
| /prague/ash-of-strahov-garden | 1 | 2 | 50.0% | 8.0 |
| /turin/oak-behind-the-castello-del-valentino | 1 | 2 | 50.0% | 2.5 |
| /valencia/ficus-of-the-alameditas-de-serranos | 1 | 2 | 50.0% | 2.0 |
| /vienna/field-elm-of-burggasse | 1 | 2 | 50.0% | 4.0 |
| /vienna/sisi-platane-of-volksgarten | 1 | 2 | 50.0% | 1.0 |
| /copenhagen/weeping-beech-of-assistens | 1 | 1 | 100.0% | 1.0 |
| /dublin/deans-tree | 1 | 1 | 100.0% | 2.0 |
| /es/malaga/native-oak-of-malaga-park | 1 | 1 | 100.0% | 1.0 |
| /padua/oriental-plane-of-the-orto-botanico | 1 | 1 | 100.0% | 4.0 |
| /toulouse/hackberry-of-place-saint-georges | 1 | 1 | 100.0% | 7.0 |
| /vilnius/oldest-oak-of-vilnius | 1 | 1 | 100.0% | 4.0 |
| /vilnius/sapiegos-park-linden | 1 | 1 | 100.0% | 2.0 |

**And the same clicks by page type**

| Type | Pages seen | Clicks | Impressions | CTR |
|---|---:|---:|---:|---:|
| city page | 131 | 63 | 3310 | 1.9% |
| tree page | 712 | 60 | 2371 | 2.5% |
| question page | 100 | 14 | 469 | 3.0% |
| home | 1 | 9 | 55 | 16.4% |
| collections | 10 | 3 | 112 | 2.7% |
| parks | 19 | 3 | 68 | 4.4% |
| species | 84 | 3 | 604 | 0.5% |
| countries | 1 | 1 | 6 | 16.7% |
| product | 3 | 0 | 18 | 0.0% |
| cities | 1 | 0 | 2 | 0.0% |
- Top pages (10d): / (c9/i55); /prague (c7/i138); /athens/holm-oak-of-the-national-garden (c5/i8); /amsterdam (c4/i130); /dubrovnik (c4/i65)
- Content lead: 'alameda dos platanos' has no matching page (i11, p8)

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| rome | 3 | 246 | 1.2% | 12.8 | 1.6% | trees in rome (i14, p18) |
| amsterdam | 5 | 203 | 2.5% | 13.9 | 1.4% | dutch elm amsterdam (i9, p6) |
| barcelona | 5 | 200 | 2.5% | 9.4 | 2.8% | barcelona tree (i5, p6) |
| bath | 2 | 178 | 1.1% | 8.3 | 3.4% | the giant plane tree bath (i8, p11) |
| palermo | 2 | 173 | 1.2% | 9.5 | 2.8% | palermo tree (i4, p10) |
| lisbon | 6 | 164 | 3.7% | 10.2 | 2.4% | oldest tree in lisbon (i6, p9) |
| prague | 8 | 160 | 5.0% | 7.2 | 3.9% | four trees prague (i2, p21) |
| singapore | 2 | 140 | 1.4% | 15.8 | 1.1% | oldest tree in singapore (i25, p10) |
| london | 0 | 137 | 0.0% | 23.1 | 0.7% | london trees (i2, p76) |
| es | 2 | 132 | 1.5% | 12.4 | 1.7% | árboles históricos de málaga (i14, p15) |
| milan | 0 | 131 | 0.0% | 10.8 | 2.2% | "oldest of its species" ginkgo park (i8, p7) |
| vienna | 3 | 126 | 2.4% | 9.1 | 3.0% | - |
| paris | 7 | 125 | 5.6% | 21.9 | 0.7% | paris trees (i2, p62) |
| florence | 0 | 121 | 0.0% | 11.0 | 2.2% | florence tree (i6, p7) |
| copenhagen | 2 | 115 | 1.7% | 13.8 | 1.4% | trees in copenhagen (i11, p15) |
| cambridge | 0 | 114 | 0.0% | 35.0 | 0.4% | newton's apple tree (i6, p49) |
| madrid | 0 | 98 | 0.0% | 12.5 | 1.7% | oldest tree in madrid (i3, p15) |
| brussels | 3 | 95 | 3.2% | 19.7 | 0.8% | belgian tree (i5, p58) |
| boston | 0 | 94 | 0.0% | 21.0 | 0.8% | shaw memorial elms (i2, p10) |
| new-york | 3 | 93 | 3.2% | 16.4 | 1.1% | ancient elm (i1, p54) |
| dubrovnik | 4 | 86 | 4.7% | 6.5 | 4.5% | trsteno plane tree (i5, p12) |
| geneva | 1 | 85 | 1.2% | 11.3 | 2.0% | sixty tree (i1, p9) |
| tenerife | 0 | 82 | 0.0% | 11.5 | 2.0% | drago milenario (i11, p10) |
| malaga | 1 | 80 | 1.2% | 12.6 | 1.7% | árboles históricos de málaga (i5, p75) |
| washington-dc | 3 | 79 | 3.8% | 16.9 | 1.0% | survey lodge ranger station (i9, p10) |
| seoul | 0 | 79 | 0.0% | 17.4 | 1.0% | seoul tree (i7, p8) |
| dublin | 6 | 75 | 8.0% | 14.5 | 1.3% | buchanan tree (i1, p10) |
| istanbul | 2 | 71 | 2.8% | 11.5 | 2.0% | archeologisch museum van istanbul (i1, p1) |
| budapest | 1 | 69 | 1.4% | 9.3 | 2.8% | in budapest? (i1, p4) |
| naples | 1 | 67 | 1.5% | 10.9 | 2.2% | a tree in naples (i1, p15) |
| valencia | 1 | 67 | 1.5% | 8.8 | 3.1% | ficus centenarios de la glorieta (i3, p10) |
| venice | 3 | 62 | 4.8% | 10.8 | 2.2% | trees in venice (i1, p1) |
| edinburgh | 1 | 61 | 1.6% | 18.7 | 0.9% | edinburgh tree map (i1, p52) |
| porto | 0 | 61 | 0.0% | 5.9 | 5.2% | alameda dos platanos (i11, p8) |
| reykjavik | 1 | 60 | 1.7% | 13.1 | 1.6% | oldest tree in iceland (i5, p8) |
| brisbane | 0 | 55 | 0.0% | 17.8 | 1.0% | the big macadamia nut (i2, p76) |
| bristol | 1 | 52 | 1.9% | 21.8 | 0.7% | bristol trees (i9, p54) |
| oslo | 1 | 51 | 2.0% | 13.3 | 1.5% | dronningparken (i1, p8) |
| seville | 2 | 50 | 4.0% | 13.5 | 1.5% | - |
| the-hague | 5 | 49 | 10.2% | 6.2 | 4.8% | juttepeer (i2, p3) |
| krakow | 2 | 46 | 4.3% | 9.1 | 2.9% | - |
| padua | 1 | 45 | 2.2% | 7.4 | 3.8% | - |
| zurich | 2 | 44 | 4.5% | 10.5 | 2.3% | zurich (i1, p2) |
| nice | 0 | 44 | 0.0% | 13.7 | 1.5% | - |
| sintra | 2 | 43 | 4.7% | 6.7 | 4.3% | - |
| berlin | 0 | 41 | 0.0% | 20.5 | 0.8% | - |
| athens | 5 | 40 | 12.5% | 16.2 | 1.1% | old plane tree (i2, p37) |
| glasgow | 2 | 39 | 5.1% | 16.6 | 1.1% | oldest tree in glasgow (i1, p11) |
| montreal | 1 | 39 | 2.6% | 12.6 | 1.7% | century trees (i1, p45) |
| lyon | 0 | 38 | 0.0% | 18.3 | 0.9% | agriates lyon (i1, p64) |
| tokyo | 1 | 37 | 2.7% | 17.5 | 1.0% | - |
| alicante | 1 | 36 | 2.8% | 6.5 | 4.5% | ficus alicante (i5, p9) |
| portland | 0 | 36 | 0.0% | 13.0 | 1.6% | trees in portland or (i1, p55) |
| helsinki | 1 | 35 | 2.9% | 8.8 | 3.1% | helsinki tree (i1, p8) |
| hong-kong | 0 | 35 | 0.0% | 13.5 | 1.5% | trees in hong kong (i1, p60) |
| madeira | 0 | 35 | 0.0% | 7.6 | 3.7% | fanal witch tree (i3, p14) |
| cork | 3 | 34 | 8.8% | 16.1 | 1.1% | trees cork (i2, p71) |
| bangkok | 0 | 33 | 0.0% | 9.9 | 2.5% | bangkok trees (i1, p9) |
| belgrade | 0 | 33 | 0.0% | 15.4 | 1.2% | - |
| granada | 0 | 33 | 0.0% | 16.8 | 1.1% | granada orange trees (i1, p64) |
| nijmegen | 0 | 30 | 0.0% | 11.2 | 2.1% | oldest tree in the netherlands (i1, p5) |
| groningen | 2 | 29 | 6.9% | 36.2 | 0.4% | big five groningen (i4, p84) |
| leiden | 3 | 29 | 10.3% | 12.4 | 1.7% | old zelkova tree (i1, p66) |
| munich | 1 | 28 | 3.6% | 6.4 | 4.6% | - |
| turin | 1 | 28 | 3.6% | 5.1 | 6.9% | alberi monumentali (i1, p8) |
| haarlem | 0 | 28 | 0.0% | 37.6 | 0.4% | noble tree (i10, p57) |
| bologna | 0 | 27 | 0.0% | 6.9 | 4.1% | trees hours (i1, p11) |
| kyoto | 2 | 26 | 7.7% | 12.5 | 1.7% | kyoto tree (i2, p7) |
| oxford | 2 | 26 | 7.7% | 6.8 | 4.2% | - |
| antwerp | 1 | 25 | 4.0% | 16.0 | 1.1% | klaverbladdreef (i1, p83) |
| crete | 0 | 25 | 0.0% | 14.2 | 1.4% | oldest olive tree crete (i1, p21) |
| cadiz | 0 | 24 | 0.0% | 7.5 | 3.7% | how old (i1, p1) |
| genoa | 0 | 24 | 0.0% | 6.3 | 4.7% | - |
| osaka | 0 | 24 | 0.0% | 6.7 | 4.3% | meoto kusu (i1, p7) |
| utrecht | 0 | 24 | 0.0% | 18.6 | 0.9% | ja leuk (i1, p9) |
| warsaw | 0 | 24 | 0.0% | 15.2 | 1.2% | oldest tree in poland (i1, p53) |
| ljubljana | 1 | 22 | 4.5% | 11.5 | 2.0% | - |
| trieste | 0 | 22 | 0.0% | 10.8 | 2.2% | piazza hortis (i1, p10) |
| fukuoka | 0 | 21 | 0.0% | 8.2 | 3.4% | - |
| palma-de-mallorca | 0 | 21 | 0.0% | 8.4 | 3.3% | mallorca trees (i1, p11) |
| stockholm | 0 | 21 | 0.0% | 7.6 | 3.7% | - |
| lucca | 1 | 20 | 5.0% | 9.8 | 2.6% | lucca tree (i3, p10) |
| setubal | 1 | 20 | 5.0% | 7.7 | 3.6% | - |
| strasbourg | 0 | 20 | 0.0% | 6.7 | 4.3% | - |
| guimaraes | 0 | 19 | 0.0% | 12.3 | 1.7% | pine tree portugal (i1, p17) |
| rotterdam | 0 | 19 | 0.0% | 11.7 | 1.9% | old tree (i1, p6) |
| bordeaux | 0 | 18 | 0.0% | 7.8 | 3.6% | caucasian elm (i1, p9) |
| bratislava | 0 | 18 | 0.0% | 10.7 | 2.2% | - |
| portugal | 0 | 18 | 0.0% | 57.5 | 0.4% | portugal trees (i2, p71) |
| split | 0 | 18 | 0.0% | 6.9 | 4.1% | mediterranean cypress croatia (i1, p7) |
| toulouse | 3 | 17 | 17.6% | 9.5 | 2.8% | french plane tree (i1, p44) |
| caserta | 0 | 17 | 0.0% | 20.1 | 0.8% | parchi caserta (i1, p1) |
| maastricht | 0 | 17 | 0.0% | 10.4 | 2.4% | trees (i1, p8) |
| sardinia | 0 | 17 | 0.0% | 8.9 | 3.0% | olivastri millenari di luras / s'ozzastr (i1, p11) |
| cordoba | 1 | 16 | 6.2% | 29.4 | 0.4% | gingko garden (i1, p56) |
| sofia | 1 | 16 | 6.2% | 13.6 | 1.5% | - |
| bergamo | 0 | 16 | 0.0% | 7.4 | 3.8% | parco caprotti (i7, p9) |
| breda | 0 | 15 | 0.0% | 29.1 | 0.4% | ulvenhoutselaan (i1, p13) |
| cagliari | 0 | 15 | 0.0% | 5.5 | 6.1% | - |
| potsdam | 0 | 14 | 0.0% | 10.1 | 2.5% | jagdschloss glienicke (i1, p12) |
| thessaloniki | 1 | 13 | 7.7% | 15.5 | 1.2% | - |
| den-bosch | 0 | 13 | 0.0% | 8.5 | 3.2% | - |
| perugia | 0 | 13 | 0.0% | 5.5 | 5.9% | - |
| chicago | 1 | 12 | 8.3% | 9.8 | 2.6% | oldest tree in chicago (i1, p17) |
| arnhem | 0 | 12 | 0.0% | 14.4 | 1.3% | - |
| bucaco | 0 | 12 | 0.0% | 7.8 | 3.6% | cedro do bussaco (i2, p2) |
| hobart | 0 | 12 | 0.0% | 18.8 | 0.9% | oldest trees in tasmania (i1, p61) |
| toronto | 0 | 12 | 0.0% | 18.2 | 0.9% | big red oak (i3, p6) |
| tallinn | 0 | 11 | 0.0% | 10.2 | 2.4% | - |
| zaragoza | 0 | 11 | 0.0% | 11.1 | 2.1% | - |
| vilnius | 4 | 10 | 40.0% | 9.4 | 2.8% | - |
| canada | 1 | 10 | 10.0% | 23.5 | 0.7% | ancient tree (i1, p27) |
| bucharest | 0 | 10 | 0.0% | 13.8 | 1.4% | - |
| como | 0 | 10 | 0.0% | 22.1 | 0.7% | lake como tree (i2, p58) |
| poznan | 0 | 10 | 0.0% | 31.0 | 0.4% | - |
- Seen, not clicked: /cambridge/newtons-apple-tree (c0/i45, 0.0%) for newton's apple tree (i6, p49); newton apple tree (i4, p45); isaac newton apple tree (i4, p47)
- Seen, not clicked: /rome (c0/i39, 0.0%) for trees in rome (i14, p18); rome trees (i4, p16); roman trees (i3, p22)
- Seen, not clicked: /singapore/oldest-tree (c0/i28, 0.0%) for oldest tree in singapore (i25, p10); singapore national tree (i2, p3); angsana meaning (i1, p3)

**Climbing** (this ten days against the ten before it)

| Page | Impressions | Change | Position | Moved | Clicks |
|---|---:|---:|---:|---:|---:|
| /barcelona | 127 | +90 | 8.2 | +0.3 | -1 |
| /milan | 118 | +69 | 10.6 | -0.4 | +0 |
| /prague | 138 | +67 | 7.4 | +3.2 | +2 |
| /dubrovnik | 65 | +58 | 5.8 | +0.7 | +3 |
| /paris | 87 | +57 | 25.4 | - | +4 |
| /florence | 107 | +57 | 10.5 | -1.5 | +0 |
| /seoul | 59 | +53 | 16.9 | -9.2 | +0 |
| /geneva | 61 | +52 | 11.1 | -3.0 | +0 |

**Newly ranking** (no impressions at all ten days ago)

| Page | Impressions | Clicks | Position |
|---|---:|---:|---:|
| /bath/plane-tree-of-abbey-green | 141 | 1 | 8.9 |
| /madrid | 83 | 0 | 12.6 |
| /copenhagen | 72 | 0 | 12.6 |
| /es/malaga | 53 | 0 | 10.0 |
| /tenerife/el-drago-milenario | 48 | 0 | 10.4 |
| /es/malaga/ficus-avenue-of-the-alameda-principal | 41 | 1 | 5.3 |

**Slipping**

| Page | Impressions | Change | Position | Moved |
|---|---:|---:|---:|---:|
| /kyoto | 15 | -35 | 16.5 | -6.8 |
| /naples | 53 | -26 | 11.6 | -2.2 |
| /explore | 15 | -22 | 15.4 | -8.6 |
| /istanbul | 26 | -22 | 14.5 | -4.5 |

- New queries this window: dutch elm amsterdam (i12), oldest tree in central park (i4).

**Who they are**
Audience, 28 days of search (258 clicks, 11130 impressions):
- Countries: usa c47/i2492; nld c21/i534; gbr c20/i1421; deu c14/i378; esp c13/i637
- Devices: MOBILE c178/i5992; DESKTOP c80/i5038; TABLET c0/i100
- Landing pages: / c14/i101; /lisbon c12/i266; /prague c12/i239; /amsterdam c6/i368; /athens/holm-oak-of-the-national-garden c6/i14

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-14 | 50 | 70 |
| 08-15 | 30 | 50 |
| 08-16 | 110 | 110 |
| 08-17 | 30 | 90 |
| 08-18 | 40 | 60 |
| 08-19 | 40 | 80 |
| 08-20 | 110 | 180 |
| 08-21 | 40 | 80 |
| **window** | **450** | **720** |
- Top paths: / (90); /amsterdam (70); /paris (40); /explore (30); /copenhagen (20); /barcelona (20); /athens/holm-oak-of-the-national-garden (20); /app (20); /toulouse/hackberry-of-place-saint-georges (20); /singapore/mandela-tree-of-orchid-plaza (10); /london/totteridge-yew (10); /rome/oldest-tree (10)
- Referrers: (direct) (280); ancienttrees.app (270); www.google.com (170)
- Moved between our own pages: 270 of 720 pageviews (38%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: NL (220); US (160); GB (80); IE (30); PT (30)
- Devices: mobile (360); desktop (360)
- Page load (8d): p50 605ms, p90 3197ms

Links: external referrers (a link somebody actually clicked): none yet
AI: arrivals from an assistant that cited us: none yet


**What the night shift did**

| Started | Minutes | Turns | Trees | Commits | Refused |
|---|---:|---:|---:|---:|---:|
| 08-21T18:44 | 0.1 | 0 | 0 | 0 | - |
| 08-21T20:31 | 0.0 | 0 | 0 | 0 | - |
| 08-21T22:30 | 0.1 | 0 | 0 | 0 | - |
| 08-22T00:26 | 0.1 | 0 | 0 | 0 | - |
| 08-22T02:44 | 0.1 | 0 | 0 | 0 | - |
| 08-22T04:19 | 0.1 | 0 | 0 | 0 | - |
| 08-22T05:33 | 16.0 | 148 | 0 | 7 | 42 |
| 08-22T05:50 | 16.5 | 148 | 0 | 14 | 36 |
| **8 runs** | **33** | | **0** | **21** | |

- 8 of 8 produced no trees; 36 to 42 commands refused per run; 7 wrote nothing to LOG.md.

Machine: 9 chain attempts yesterday, 6 got real work time (~132 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 18 clicks and 757 impressions on Google's freshest day (day before: c17/i1022). Directional at best; no strategic conclusions from these volumes.

## 2026-08-20 (previous UTC day)

**Today: a waitlist arrived yesterday (10 total); a submission arrived yesterday (6 total).**

**Did the product happen**
- save:        3 yesterday, last yesterday
- suggestion-submit: 3 yesterday, last yesterday
- app-cta:     1 yesterday, last yesterday
- search-explore: 1 yesterday, last today
- search-home: 1 yesterday, last yesterday
- waitlist-submit: 1 yesterday, last yesterday
- beacon-fix-verify: 0 yesterday, last 5 days ago
- beacon-test: 0 yesterday, last 5 days ago
- directions:  0 yesterday, last never
- signin-link-sent: 0 yesterday, last never
- smoke-test:  0 yesterday, last 20 days ago
- walk-open:   0 yesterday, last 4 days ago
- walk-start:  0 yesterday, last never
- walks-app:   0 yesterday, last 3 days ago
- worthit-not worth it: 0 yesterday, last 4 days ago
- worthit-worth it: 0 yesterday, last never

| Day | Accounts | Waitlist | Submissions |
|---|---:|---:|---:|
| 08-07 | 0 | 1 | 0 |
| 08-08 | 1 | 1 | 0 |
| 08-09 | 0 | 0 | 0 |
| 08-10 | 0 | 0 | 0 |
| 08-11 | 0 | 0 | 0 |
| 08-12 | 0 | 0 | 0 |
| 08-13 | 0 | 0 | 0 |
| 08-14 | 0 | 1 | 0 |
| 08-15 | 0 | 0 | 1 |
| 08-16 | 0 | 0 | 0 |
| 08-17 | 0 | 1 | 2 |
| 08-18 | 0 | 1 | 0 |
| 08-19 | 0 | 1 | 0 |
| 08-20 | 0 | 1 | 3 |
| 08-21 | 0 | 0 | 0 |
| **14 days** | **1** | **7** | **6** |
- Waitlist:    10 total, newest yesterday
- Submissions: 6 total, newest yesterday
- Accounts:    3 total, newest 13 days ago

**The funnel, as rates**
- Seen to clicked: 2.4% (159 of 6740) vs 2.1% the fortnight before
- Pages per visit: 1.6 (700 visits, 1090 pageviews since 2026-08-08)
- Visits that did something: 8.0% (56 actions on 700 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-11 | 8 | 415 | 1.9% | 12.9 |
| 08-12 | 9 | 441 | 2.0% | 19.1 |
| 08-13 | 9 | 446 | 2.0% | 17.5 |
| 08-14 | 13 | 517 | 2.5% | 14.2 |
| 08-15 | 15 | 630 | 2.4% | 14.4 |
| 08-16 | 14 | 723 | 1.9% | 13.9 |
| 08-17 | 15 | 600 | 2.5% | 14.7 |
| 08-18 | 19 | 609 | 3.1% | 15.0 |
| 08-19 | 18 | 806 | 2.2% | 17.0 |
| 08-20 | 5 | 434 | 1.2% | 19.5 |
| **window** | **125** | **5621** | **2.2%** | |
- Top queries (10d): dutch elm amsterdam (i8, p6); juttepeer (i2, p3); oldest tree in central park (i4, p10); oldest tree in dc (i2, p10); "oldest of its species" ginkgo park (i7, p7)
- Top pages (10d): / (c6/i49); /amsterdam (c4/i131); /athens/holm-oak-of-the-national-garden (c4/i7); /dubrovnik (c4/i58); /prague (c4/i122)
- Content lead: 'alameda dos platanos' has no matching page (i8, p8)

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| rome | 2 | 215 | 0.9% | 13.8 | 1.4% | trees in rome (i13, p19) |
| barcelona | 4 | 185 | 2.2% | 9.5 | 2.8% | barcelona tree (i4, p6) |
| amsterdam | 5 | 183 | 2.7% | 12.5 | 1.7% | dutch elm amsterdam (i6, p5) |
| palermo | 3 | 181 | 1.7% | 9.8 | 2.6% | palermo tree (i5, p10) |
| bath | 1 | 145 | 0.7% | 8.8 | 3.1% | the giant plane tree bath (i5, p10) |
| lisbon | 4 | 141 | 2.8% | 11.0 | 2.1% | oldest tree in lisbon (i6, p9) |
| prague | 5 | 134 | 3.7% | 8.1 | 3.4% | four trees prague (i2, p21) |
| london | 0 | 124 | 0.0% | 21.5 | 0.7% | london trees (i2, p76) |
| singapore | 1 | 119 | 0.8% | 15.8 | 1.1% | oldest tree in singapore (i28, p10) |
| cambridge | 0 | 117 | 0.0% | 33.0 | 0.4% | newton's apple tree (i5, p50) |
| vienna | 4 | 115 | 3.5% | 10.0 | 2.5% | trees in austria (i1, p54) |
| es | 0 | 107 | 0.0% | 13.0 | 1.6% | árboles históricos de málaga (i12, p16) |
| paris | 6 | 102 | 5.9% | 21.6 | 0.7% | paris trees (i2, p62) |
| boston | 0 | 101 | 0.0% | 18.3 | 0.9% | shaw memorial elms (i2, p10) |
| florence | 0 | 95 | 0.0% | 10.8 | 2.2% | florence tree (i2, p6) |
| milan | 0 | 92 | 0.0% | 11.8 | 1.9% | "oldest of its species" ginkgo park (i7, p7) |
| new-york | 2 | 90 | 2.2% | 17.0 | 1.0% | ancient elm (i1, p54) |
| geneva | 1 | 85 | 1.2% | 11.5 | 2.0% | sixty tree (i1, p9) |
| brussels | 2 | 83 | 2.4% | 20.9 | 0.8% | belgian tree (i5, p58) |
| dubrovnik | 4 | 80 | 5.0% | 6.8 | 4.2% | trsteno plane tree (i4, p12) |
| madrid | 0 | 78 | 0.0% | 11.8 | 1.9% | oldest tree in madrid (i3, p15) |
| malaga | 1 | 77 | 1.3% | 14.9 | 1.2% | árboles históricos de málaga (i7, p75) |
| washington-dc | 3 | 77 | 3.9% | 15.1 | 1.2% | survey lodge ranger station (i9, p11) |
| dublin | 6 | 75 | 8.0% | 14.6 | 1.3% | buchanan tree (i1, p10) |
| seoul | 0 | 74 | 0.0% | 18.1 | 1.0% | seoul tree (i7, p8) |
| copenhagen | 1 | 73 | 1.4% | 11.3 | 2.1% | trees in copenhagen (i7, p12) |
| budapest | 1 | 69 | 1.4% | 9.4 | 2.8% | in budapest? (i1, p4) |
| naples | 0 | 69 | 0.0% | 8.1 | 3.4% | a tree in naples (i3, p9) |
| istanbul | 1 | 65 | 1.5% | 12.4 | 1.7% | archeologisch museum van istanbul (i1, p1) |
| valencia | 1 | 61 | 1.6% | 8.0 | 3.5% | ficus centenarios de la glorieta (i2, p10) |
| reykjavik | 1 | 56 | 1.8% | 13.5 | 1.5% | oldest tree in iceland (i2, p8) |
| venice | 3 | 55 | 5.5% | 8.9 | 3.1% | trees in venice (i1, p1) |
| bristol | 1 | 55 | 1.8% | 21.3 | 0.7% | bristol trees (i8, p53) |
| porto | 0 | 55 | 0.0% | 6.3 | 4.7% | alameda dos platanos (i8, p8) |
| edinburgh | 1 | 49 | 2.0% | 20.8 | 0.8% | edinburgh tree map (i1, p52) |
| nice | 0 | 45 | 0.0% | 13.7 | 1.5% | - |
| sintra | 2 | 44 | 4.5% | 6.6 | 4.4% | - |
| oslo | 1 | 43 | 2.3% | 9.7 | 2.7% | dronningparken (i1, p8) |
| the-hague | 5 | 42 | 11.9% | 5.5 | 6.1% | juttepeer (i2, p3) |
| munich | 2 | 41 | 4.9% | 8.1 | 3.4% | - |
| seville | 1 | 39 | 2.6% | 11.0 | 2.1% | - |
| berlin | 0 | 39 | 0.0% | 19.2 | 0.9% | east berlin germany plants (i1, p77) |
| granada | 0 | 39 | 0.0% | 15.6 | 1.1% | granada orange trees (i1, p64) |
| hong-kong | 0 | 39 | 0.0% | 13.0 | 1.6% | kam tin tree house (i3, p11) |
| padua | 1 | 38 | 2.6% | 6.7 | 4.3% | - |
| lyon | 0 | 38 | 0.0% | 13.4 | 1.5% | near lyon (i1, p10) |
| bangkok | 1 | 37 | 2.7% | 9.7 | 2.6% | bangkok trees (i1, p9) |
| zurich | 2 | 36 | 5.6% | 9.1 | 2.9% | zurich (i1, p2) |
| glasgow | 1 | 35 | 2.9% | 19.2 | 0.9% | oldest tree in glasgow (i1, p11) |
| athens | 4 | 34 | 11.8% | 14.6 | 1.3% | old plane tree (i1, p39) |
| belgrade | 0 | 34 | 0.0% | 12.4 | 1.7% | - |
| krakow | 1 | 33 | 3.0% | 6.7 | 4.3% | - |
| portland | 0 | 33 | 0.0% | 13.6 | 1.5% | trees in portland or (i1, p55) |
| helsinki | 1 | 32 | 3.1% | 8.1 | 3.5% | helsinki tree (i1, p8) |
| cork | 3 | 31 | 9.7% | 16.2 | 1.1% | trees cork (i2, p71) |
| tokyo | 1 | 31 | 3.2% | 21.7 | 0.7% | - |
| tenerife | 0 | 31 | 0.0% | 12.2 | 1.8% | pino gordo (i4, p30) |
| leiden | 3 | 29 | 10.3% | 10.4 | 2.4% | - |
| groningen | 2 | 27 | 7.4% | 33.6 | 0.4% | big five groningen (i4, p84) |
| alicante | 1 | 27 | 3.7% | 6.9 | 4.1% | ficus alicante (i4, p10) |
| antwerp | 1 | 27 | 3.7% | 15.4 | 1.2% | klaverbladdreef (i1, p83) |
| bologna | 0 | 27 | 0.0% | 6.7 | 4.3% | trees hours (i1, p11) |
| cadiz | 0 | 26 | 0.0% | 6.8 | 4.2% | ficus cadiz (i1, p10) |
| haarlem | 0 | 26 | 0.0% | 41.9 | 0.4% | noble tree (i11, p57) |
| nijmegen | 0 | 26 | 0.0% | 11.6 | 1.9% | oldest tree in the netherlands (i1, p5) |
| turin | 1 | 25 | 4.0% | 5.4 | 6.2% | alberi monumentali (i1, p8) |
| utrecht | 0 | 25 | 0.0% | 18.0 | 1.0% | ginkgo utrecht (i2, p8) |
| kyoto | 2 | 24 | 8.3% | 12.5 | 1.7% | kyoto tree (i4, p6) |
| genoa | 0 | 23 | 0.0% | 6.6 | 4.4% | - |
| osaka | 0 | 23 | 0.0% | 6.6 | 4.4% | meoto kusu (i1, p7) |
| oxford | 0 | 23 | 0.0% | 7.8 | 3.6% | - |
| brisbane | 0 | 21 | 0.0% | 13.7 | 1.5% | banyan tree brisbane (i1, p11) |
| lucca | 0 | 21 | 0.0% | 10.4 | 2.4% | lucca tree (i4, p10) |
| stockholm | 0 | 21 | 0.0% | 8.0 | 3.5% | - |
| warsaw | 0 | 21 | 0.0% | 14.8 | 1.2% | oldest tree in poland (i1, p53) |
| split | 0 | 20 | 0.0% | 8.6 | 3.2% | - |
| rotterdam | 0 | 19 | 0.0% | 9.7 | 2.7% | old tree (i1, p6) |
| maastricht | 0 | 17 | 0.0% | 10.6 | 2.3% | trees (i1, p8) |
| toulouse | 3 | 16 | 18.8% | 10.4 | 2.4% | french plane tree (i1, p44) |
| ljubljana | 1 | 16 | 6.2% | 4.8 | 7.2% | - |
| setubal | 1 | 16 | 6.2% | 7.6 | 3.7% | - |
| bordeaux | 0 | 16 | 0.0% | 8.0 | 3.5% | caucasian elm (i1, p9) |
| trieste | 0 | 16 | 0.0% | 12.2 | 1.8% | piazza hortis (i1, p10) |
| cordoba | 1 | 15 | 6.7% | 16.8 | 1.1% | jacaranda cordoba (i1, p12) |
| caserta | 0 | 15 | 0.0% | 21.4 | 0.7% | douglas fir teaching garden (i1, p81) |
| palma-de-mallorca | 0 | 15 | 0.0% | 9.3 | 2.8% | mallorca trees (i1, p11) |
| sofia | 1 | 14 | 7.1% | 4.7 | 7.3% | - |
| thessaloniki | 1 | 13 | 7.7% | 15.7 | 1.1% | - |
| breda | 0 | 13 | 0.0% | 19.3 | 0.9% | ulvenhoutselaan (i1, p13) |
| guimaraes | 0 | 13 | 0.0% | 8.2 | 3.4% | - |
| zaragoza | 0 | 13 | 0.0% | 6.2 | 4.8% | - |
| chicago | 1 | 12 | 8.3% | 10.0 | 2.5% | oldest tree in chicago (i1, p7) |
| bergamo | 0 | 12 | 0.0% | 6.9 | 4.1% | parco caprotti (i6, p10) |
| bucaco | 0 | 12 | 0.0% | 7.8 | 3.6% | cedro do bussaco (i2, p2) |
| den-bosch | 0 | 12 | 0.0% | 6.8 | 4.2% | - |
| portugal | 0 | 12 | 0.0% | 52.8 | 0.4% | portuguese trees (i1, p54) |
| strasbourg | 0 | 12 | 0.0% | 7.5 | 3.8% | - |
| cagliari | 0 | 11 | 0.0% | 5.6 | 5.7% | - |
| madeira | 0 | 11 | 0.0% | 8.6 | 3.2% | fanal witch tree (i2, p14) |
| perugia | 0 | 11 | 0.0% | 6.0 | 5.0% | - |
| arnhem | 0 | 10 | 0.0% | 10.3 | 2.4% | - |
| como | 0 | 10 | 0.0% | 22.3 | 0.7% | lake como tree (i2, p58) |
| hobart | 0 | 10 | 0.0% | 20.8 | 0.8% | oldest trees in tasmania (i1, p61) |
| potsdam | 0 | 10 | 0.0% | 5.6 | 5.8% | jagdschloss glienicke (i1, p12) |
- Seen, not clicked: /cambridge/newtons-apple-tree (c0/i43, 0.0%) for newton's apple tree (i5, p50); oldest apple tree (i4, p33); isaac newton apple tree (i4, p47)
- Seen, not clicked: /rome (c0/i37, 0.0%) for trees in rome (i13, p19); rome trees (i4, p16); roman trees (i4, p26)
- Seen, not clicked: /singapore/oldest-tree (c0/i31, 0.0%) for oldest tree in singapore (i28, p10); singapore national tree (i2, p3); angsana meaning (i1, p3)

**Climbing** (this ten days against the ten before it)

| Page | Impressions | Change | Position | Moved | Clicks |
|---|---:|---:|---:|---:|---:|
| /barcelona | 111 | +74 | 7.9 | +0.5 | -1 |
| /prague | 122 | +62 | 8.3 | +3.0 | +0 |
| /dubrovnik | 58 | +55 | 6.2 | +1.1 | +4 |
| /geneva | 61 | +53 | 11.3 | -2.4 | +0 |
| /cambridge/newtons-apple-tree | 53 | +51 | 45.3 | +3.7 | +0 |
| /seoul | 53 | +48 | 17.8 | -10.2 | +0 |
| /palermo | 168 | +39 | 9.7 | -0.8 | +3 |
| /budapest | 40 | +39 | 9.7 | -2.7 | +1 |

**Newly ranking** (no impressions at all ten days ago)

| Page | Impressions | Clicks | Position |
|---|---:|---:|---:|
| /bath/plane-tree-of-abbey-green | 110 | 0 | 9.6 |
| /madrid | 62 | 0 | 11.7 |
| /es/malaga | 45 | 0 | 9.8 |
| /copenhagen | 43 | 0 | 10.7 |
| /species/olive | 32 | 0 | 53.0 |
| /es/malaga/ficus-avenue-of-the-alameda-principal | 32 | 0 | 6.0 |

**Slipping**

| Page | Impressions | Change | Position | Moved |
|---|---:|---:|---:|---:|
| /kyoto | 16 | -36 | 15.2 | -4.9 |
| /istanbul | 25 | -25 | 15.2 | -4.7 |
| /tokyo | 15 | -20 | 32.0 | -13.2 |
| /nice | 33 | -9 | 16.6 | -10.1 |

- New queries this window: dutch elm amsterdam (i8), oldest tree in central park (i4).

**Who they are**
Audience, 28 days of search (224 clicks, 9851 impressions):
- Countries: usa c40/i2213; nld c19/i494; gbr c16/i1275; deu c14/i346; fra c11/i226
- Devices: MOBILE c154/i5388; DESKTOP c70/i4377; TABLET c0/i86
- Landing pages: / c11/i95; /lisbon c10/i244; /prague c8/i208; /amsterdam c7/i364; /vienna c6/i181

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-13 | 10 | 60 |
| 08-14 | 50 | 70 |
| 08-15 | 30 | 50 |
| 08-16 | 110 | 110 |
| 08-17 | 30 | 90 |
| 08-18 | 40 | 60 |
| 08-19 | 40 | 80 |
| 08-20 | 110 | 180 |
| **window** | **420** | **700** |
- Top paths: / (100); /amsterdam (70); /paris (40); /toulouse/hackberry-of-place-saint-georges (20); /app (20)
- Referrers: ancienttrees.app (280); (direct) (260); www.google.com (160)
- Countries: NL (220); US (140); GB (80); PT (40); DK (30)
- Devices: desktop (400); mobile (300)
- Page load (8d): p50 599ms, p90 2171ms

Links: external referrers (a link somebody actually clicked): none yet
AI: arrivals from an assistant that cited us: none yet


**What the night shift did**

| Started | Minutes | Turns | Trees | Commits | Refused |
|---|---:|---:|---:|---:|---:|
| 08-20T18:48 | 23.8 | 219 | 6 | 19 | 30 |
| 08-20T20:34 | 0.0 | 1 | 0 | 0 | 0 |
| 08-20T22:33 | 22.3 | 163 | 0 | 3 | 38 |
| 08-21T00:29 | 28.1 | 228 | 6 | 16 | 18 |
| 08-21T02:52 | 15.3 | 143 | 0 | 4 | 43 |
| 08-21T04:25 | 25.7 | 198 | 0 | 5 | 42 |
| **6 runs** | **115** | | **12** | **47** | |

- 4 of 6 produced no trees; 18 to 43 commands refused per run; 4 wrote nothing to LOG.md.

Machine: 9 chain attempts yesterday, 8 got real work time (~217 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 5 clicks and 434 impressions on Google's freshest day (day before: c18/i806). Directional at best; no strategic conclusions from these volumes.

## 2026-08-19 (previous UTC day)

**Today: a waitlist arrived yesterday (9 total).**

**Did the product happen**
- app-cta:     2 yesterday, last yesterday
- waitlist-submit: 2 yesterday, last yesterday
- search-home: 1 yesterday, last yesterday
- beacon-fix-verify: 0 yesterday, last 4 days ago
- beacon-test: 0 yesterday, last 4 days ago
- directions:  0 yesterday, last never
- save:        0 yesterday, last 2 days ago
- search-explore: 0 yesterday, last 3 days ago
- signin-link-sent: 0 yesterday, last never
- smoke-test:  0 yesterday, last 19 days ago
- walk-open:   0 yesterday, last 3 days ago
- walk-start:  0 yesterday, last never
- walks-app:   0 yesterday, last 2 days ago
- worthit-not worth it: 0 yesterday, last 3 days ago
- worthit-worth it: 0 yesterday, last never

| Day | Accounts | Waitlist | Submissions |
|---|---:|---:|---:|
| 08-06 | 0 | 0 | 0 |
| 08-07 | 0 | 1 | 0 |
| 08-08 | 1 | 1 | 0 |
| 08-09 | 0 | 0 | 0 |
| 08-10 | 0 | 0 | 0 |
| 08-11 | 0 | 0 | 0 |
| 08-12 | 0 | 0 | 0 |
| 08-13 | 0 | 0 | 0 |
| 08-14 | 0 | 1 | 0 |
| 08-15 | 0 | 0 | 1 |
| 08-16 | 0 | 0 | 0 |
| 08-17 | 0 | 1 | 2 |
| 08-18 | 0 | 1 | 0 |
| 08-19 | 0 | 1 | 0 |
| 08-20 | 0 | 0 | 0 |
| **14 days** | **1** | **6** | **3** |
- Waitlist:    9 total, newest yesterday
- Submissions: 3 total, newest 3 days ago
- Accounts:    3 total, newest 12 days ago

**The funnel, as rates**
- Seen to clicked: 2.5% (151 of 6163) vs 2.1% the fortnight before
- Pages per visit: 1.5 (590 visits, 910 pageviews since 2026-08-08)
- Visits that did something: 7.5% (44 actions on 590 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-10 | 16 | 394 | 4.1% | 13.5 |
| 08-11 | 8 | 415 | 1.9% | 12.9 |
| 08-12 | 9 | 441 | 2.0% | 19.1 |
| 08-13 | 9 | 445 | 2.0% | 17.6 |
| 08-14 | 13 | 517 | 2.5% | 14.2 |
| 08-15 | 15 | 630 | 2.4% | 14.4 |
| 08-16 | 14 | 723 | 1.9% | 13.9 |
| 08-17 | 15 | 600 | 2.5% | 14.7 |
| 08-18 | 19 | 609 | 3.1% | 15.0 |
| 08-19 | 8 | 449 | 1.8% | 16.3 |
| **window** | **126** | **5223** | **2.4%** | |
- Top queries (10d): dutch elm amsterdam (i4, p6); juttepeer (i2, p3); oldest tree in central park (i4, p10); oldest tree in dc (i2, p10); "oldest of its species" ginkgo park (i6, p6)
- Top pages (10d): / (c8/i56); /prague (c7/i125); /dubrovnik (c4/i51); /vienna (c4/i86); /amsterdam (c3/i127)
- Content lead: 'alameda dos platanos' has no matching page (i6, p8)

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| rome | 1 | 214 | 0.5% | 15.0 | 1.2% | trees in rome (i13, p19) |
| palermo | 3 | 184 | 1.6% | 10.1 | 2.5% | palermo tree (i5, p10) |
| barcelona | 4 | 167 | 2.4% | 9.5 | 2.7% | high tree barcelona (i4, p10) |
| amsterdam | 4 | 154 | 2.6% | 11.9 | 1.8% | amsterdam tree (i4, p10) |
| lisbon | 3 | 137 | 2.2% | 10.7 | 2.2% | oldest tree in lisbon (i6, p9) |
| prague | 8 | 136 | 5.9% | 7.6 | 3.7% | four trees prague (i2, p21) |
| bath | 1 | 132 | 0.8% | 8.8 | 3.1% | the giant plane tree bath (i5, p10) |
| london | 0 | 131 | 0.0% | 22.1 | 0.7% | oldest tree in london (i4, p52) |
| vienna | 7 | 119 | 5.9% | 10.1 | 2.5% | trees in austria (i1, p54) |
| cambridge | 0 | 115 | 0.0% | 31.5 | 0.4% | isaac newton apple tree (i5, p45) |
| paris | 5 | 108 | 4.6% | 21.4 | 0.7% | paris trees (i2, p62) |
| boston | 0 | 102 | 0.0% | 17.4 | 1.0% | shaw memorial elms (i2, p10) |
| singapore | 1 | 98 | 1.0% | 15.7 | 1.1% | oldest tree in singapore (i26, p10) |
| florence | 0 | 92 | 0.0% | 11.0 | 2.1% | florence tree (i2, p6) |
| new-york | 3 | 91 | 3.3% | 16.4 | 1.1% | ancient elm (i1, p54) |
| washington-dc | 3 | 82 | 3.7% | 15.9 | 1.1% | survey lodge ranger station (i9, p11) |
| malaga | 1 | 81 | 1.2% | 16.1 | 1.1% | árboles históricos de málaga (i9, p74) |
| geneva | 0 | 79 | 0.0% | 11.9 | 1.8% | - |
| milan | 0 | 79 | 0.0% | 11.7 | 1.9% | "oldest of its species" ginkgo park (i4, p6) |
| budapest | 1 | 76 | 1.3% | 9.4 | 2.8% | in budapest? (i1, p4) |
| es | 0 | 76 | 0.0% | 14.3 | 1.3% | árboles históricos de málaga (i10, p16) |
| dublin | 6 | 75 | 8.0% | 15.6 | 1.2% | buchanan tree (i1, p10) |
| brussels | 1 | 75 | 1.3% | 23.2 | 0.7% | belgian tree (i5, p58) |
| istanbul | 1 | 71 | 1.4% | 13.3 | 1.5% | archeologisch museum van istanbul (i1, p1) |
| madrid | 0 | 70 | 0.0% | 10.1 | 2.5% | oldest tree in madrid (i3, p15) |
| dubrovnik | 4 | 69 | 5.8% | 6.9 | 4.1% | trsteno plane tree (i3, p13) |
| seoul | 0 | 69 | 0.0% | 18.9 | 0.9% | seoul tree (i6, p8) |
| naples | 0 | 65 | 0.0% | 8.5 | 3.2% | a tree in naples (i3, p9) |
| valencia | 1 | 60 | 1.7% | 8.7 | 3.2% | ficus centenarios de la glorieta (i2, p10) |
| bristol | 1 | 58 | 1.7% | 17.3 | 1.0% | bristol trees (i7, p53) |
| copenhagen | 0 | 55 | 0.0% | 11.1 | 2.1% | trees in copenhagen (i4, p12) |
| porto | 2 | 53 | 3.8% | 6.5 | 4.5% | alameda dos platanos (i6, p8) |
| edinburgh | 1 | 52 | 1.9% | 20.1 | 0.8% | old tree near me (i1, p68) |
| venice | 2 | 50 | 4.0% | 6.7 | 4.3% | trees in venice (i1, p1) |
| reykjavik | 1 | 49 | 2.0% | 14.7 | 1.3% | oldest tree in iceland (i2, p8) |
| the-hague | 5 | 48 | 10.4% | 5.7 | 5.6% | juttepeer (i2, p3) |
| sintra | 3 | 46 | 6.5% | 6.6 | 4.4% | - |
| hong-kong | 1 | 46 | 2.2% | 11.9 | 1.8% | kam tin tree house (i6, p11) |
| oslo | 1 | 46 | 2.2% | 10.2 | 2.4% | oak tree near me (i1, p3) |
| nice | 0 | 43 | 0.0% | 13.7 | 1.5% | - |
| granada | 0 | 42 | 0.0% | 15.1 | 1.2% | granada orange trees (i1, p64) |
| seville | 1 | 41 | 2.4% | 9.3 | 2.8% | - |
| lyon | 0 | 41 | 0.0% | 13.7 | 1.5% | near lyon (i1, p10) |
| munich | 2 | 40 | 5.0% | 8.3 | 3.3% | - |
| zurich | 2 | 36 | 5.6% | 9.3 | 2.8% | zurich (i1, p2) |
| bangkok | 1 | 35 | 2.9% | 10.1 | 2.5% | bangkok trees (i1, p9) |
| glasgow | 1 | 35 | 2.9% | 18.8 | 0.9% | oldest tree in glasgow (i1, p11) |
| tokyo | 1 | 35 | 2.9% | 23.2 | 0.7% | - |
| belgrade | 0 | 35 | 0.0% | 12.3 | 1.7% | - |
| berlin | 0 | 34 | 0.0% | 15.9 | 1.1% | east berlin germany plants (i1, p77) |
| krakow | 1 | 32 | 3.1% | 6.8 | 4.2% | - |
| bologna | 0 | 32 | 0.0% | 6.8 | 4.2% | trees hours (i1, p11) |
| athens | 3 | 31 | 9.7% | 15.8 | 1.1% | old plane tree (i1, p39) |
| antwerp | 1 | 31 | 3.2% | 15.3 | 1.2% | klaverbladdreef (i1, p83) |
| helsinki | 1 | 31 | 3.2% | 8.2 | 3.4% | helsinki tree (i1, p8) |
| padua | 1 | 31 | 3.2% | 6.6 | 4.4% | - |
| leiden | 3 | 30 | 10.0% | 11.9 | 1.8% | "oldest of its species" ginkgo park (i2, p6) |
| cork | 3 | 30 | 10.0% | 16.3 | 1.1% | trees cork (i2, p71) |
| portland | 0 | 30 | 0.0% | 14.4 | 1.3% | trees in portland or (i1, p55) |
| kyoto | 2 | 27 | 7.4% | 11.7 | 1.9% | kyoto tree (i5, p7) |
| utrecht | 0 | 26 | 0.0% | 15.2 | 1.2% | ginkgo utrecht (i2, p8) |
| groningen | 2 | 25 | 8.0% | 28.2 | 0.5% | big five groningen (i3, p85) |
| osaka | 0 | 25 | 0.0% | 6.9 | 4.1% | meoto kusu (i1, p7) |
| cadiz | 0 | 24 | 0.0% | 6.7 | 4.3% | ficus cadiz (i1, p10) |
| haarlem | 0 | 24 | 0.0% | 42.6 | 0.4% | noble tree (i10, p57) |
| oxford | 0 | 24 | 0.0% | 7.5 | 3.7% | - |
| split | 0 | 24 | 0.0% | 8.8 | 3.1% | - |
| genoa | 0 | 23 | 0.0% | 6.6 | 4.4% | - |
| alicante | 1 | 20 | 5.0% | 7.2 | 3.9% | ja (i1, p2) |
| maastricht | 1 | 20 | 5.0% | 10.1 | 2.5% | trees (i1, p8) |
| rotterdam | 0 | 20 | 0.0% | 10.2 | 2.4% | old tree (i1, p6) |
| turin | 1 | 19 | 5.3% | 5.6 | 5.8% | alberi monumentali (i1, p8) |
| lucca | 0 | 19 | 0.0% | 10.4 | 2.4% | lucca tree (i3, p10) |
| nijmegen | 0 | 19 | 0.0% | 13.1 | 1.6% | oldest tree in the netherlands (i1, p5) |
| stockholm | 0 | 19 | 0.0% | 8.1 | 3.5% | - |
| ljubljana | 1 | 17 | 5.9% | 4.9 | 7.1% | trees ljubljana (i1, p7) |
| setubal | 1 | 17 | 5.9% | 7.4 | 3.8% | - |
| warsaw | 0 | 17 | 0.0% | 14.1 | 1.4% | oldest tree in poland (i1, p53) |
| cordoba | 1 | 14 | 7.1% | 14.1 | 1.4% | jacaranda cordoba (i1, p12) |
| bordeaux | 0 | 14 | 0.0% | 8.3 | 3.4% | caucasian elm (i1, p9) |
| breda | 0 | 14 | 0.0% | 18.1 | 0.9% | ulvenhoutselaan (i1, p13) |
| caserta | 0 | 14 | 0.0% | 16.2 | 1.1% | douglas fir teaching garden (i1, p81) |
| guimaraes | 0 | 14 | 0.0% | 7.8 | 3.6% | - |
| palma-de-mallorca | 0 | 14 | 0.0% | 9.8 | 2.6% | mallorca trees (i1, p11) |
| zaragoza | 0 | 14 | 0.0% | 6.6 | 4.4% | - |
| trieste | 1 | 13 | 7.7% | 12.2 | 1.8% | pino fantasma (i1, p5) |
| chicago | 1 | 12 | 8.3% | 10.0 | 2.5% | oldest tree in chicago (i1, p7) |
| sofia | 1 | 12 | 8.3% | 5.3 | 6.3% | - |
| bergamo | 0 | 12 | 0.0% | 6.9 | 4.1% | parco caprotti (i6, p10) |
| den-bosch | 0 | 12 | 0.0% | 6.8 | 4.2% | - |
| strasbourg | 0 | 12 | 0.0% | 7.5 | 3.8% | - |
| portugal | 0 | 11 | 0.0% | 51.7 | 0.4% | portuguese trees (i2, p66) |
| thessaloniki | 1 | 10 | 10.0% | 6.8 | 4.2% | - |
| arnhem | 0 | 10 | 0.0% | 10.3 | 2.4% | - |
| brisbane | 0 | 10 | 0.0% | 9.9 | 2.5% | buddha tree (i1, p57) |
| como | 0 | 10 | 0.0% | 22.3 | 0.7% | lake como tree (i2, p58) |
| hobart | 0 | 10 | 0.0% | 20.8 | 0.8% | oldest trees in tasmania (i1, p61) |
- Seen, not clicked: /rome (c0/i46, 0.0%) for trees in rome (i13, p19); rome tree (i5, p58); roman trees (i5, p32)
- Seen, not clicked: /cambridge/newtons-apple-tree (c0/i38, 0.0%) for isaac newton apple tree (i5, p45); apple tree of newton (i4, p47); oldest apple tree (i3, p35)
- Seen, not clicked: /singapore/oldest-tree (c0/i29, 0.0%) for oldest tree in singapore (i26, p10); singapore national tree (i2, p3); angsana meaning (i1, p3)

**Climbing** (this ten days against the ten before it)

| Page | Impressions | Change | Position | Moved | Clicks |
|---|---:|---:|---:|---:|---:|
| /prague | 125 | +65 | 7.7 | +3.6 | +3 |
| /barcelona | 95 | +58 | 8.4 | - | -1 |
| /geneva | 61 | +53 | 11.4 | -2.6 | +0 |
| /dubrovnik | 51 | +48 | 6.2 | +1.1 | +4 |
| /cambridge/newtons-apple-tree | 46 | +44 | 45.8 | +3.2 | +0 |
| /seoul | 47 | +42 | 19.2 | -11.6 | +0 |
| /palermo | 169 | +40 | 10.1 | -1.2 | +3 |
| /budapest | 41 | +40 | 9.6 | -2.6 | +1 |

**Newly ranking** (no impressions at all ten days ago)

| Page | Impressions | Clicks | Position |
|---|---:|---:|---:|
| /bath/plane-tree-of-abbey-green | 98 | 0 | 9.7 |
| /madrid | 49 | 0 | 9.8 |
| /copenhagen | 34 | 0 | 11.4 |
| /es/malaga | 31 | 0 | 10.3 |
| /species/moreton-bay-fig | 25 | 0 | 38.3 |
| /porto/alameda-dos-platanos-of-jardim-da-cordoaria | 25 | 0 | 6.0 |

**Slipping**

| Page | Impressions | Change | Position | Moved |
|---|---:|---:|---:|---:|
| /kyoto | 20 | -32 | 13.4 | -3.1 |
| /istanbul | 30 | -20 | 15.6 | -5.0 |
| /tokyo | 16 | -19 | 33.1 | -14.2 |
| /nice | 29 | -13 | 17.3 | -10.8 |

- New queries this window: oldest tree in central park (i4), dutch elm amsterdam (i4).

**Who they are**
Audience, 28 days of search (210 clicks, 9162 impressions):
- Countries: usa c36/i2085; nld c18/i472; gbr c16/i1207; deu c14/i338; esp c10/i489
- Devices: MOBILE c146/i5034; DESKTOP c64/i4049; TABLET c0/i79
- Landing pages: / c11/i98; /lisbon c9/i241; /prague c8/i200; /amsterdam c6/i355; /vienna c6/i168

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-12 | 10 | 30 |
| 08-13 | 10 | 60 |
| 08-14 | 50 | 70 |
| 08-15 | 30 | 50 |
| 08-16 | 110 | 110 |
| 08-17 | 30 | 90 |
| 08-18 | 40 | 60 |
| 08-19 | 40 | 80 |
| **window** | **320** | **550** |
- Top paths: / (100); /paris (30); /barcelona (20); /app (20); /copenhagen (20)
- Referrers: ancienttrees.app (230); (direct) (200); www.google.com (120)
- Countries: NL (160); US (90); GB (50); PT (40); DK (30)
- Devices: desktop (300); mobile (250)
- Page load (8d): p50 574ms, p90 2171ms

Links: external referrers (a link somebody actually clicked): none yet
AI: arrivals from an assistant that cited us: none yet


**What the night shift did**

| Started | Minutes | Turns | Trees | Commits | Refused |
|---|---:|---:|---:|---:|---:|
| 08-19T18:41 | 66.1 | 251 | 10 | 9 | 33 |
| 08-19T20:34 | 87.3 | 296 | 24 | 10 | 45 |
| 08-19T22:29 | 5.4 | 47 | 0 | 2 | 7 |
| 08-20T00:27 | 6.9 | 65 | 0 | 1 | 8 |
| 08-20T02:46 | 16.4 | 118 | 0 | 6 | 15 |
| 08-20T04:23 | 26.7 | 204 | 5 | 13 | 15 |
| **6 runs** | **209** | | **39** | **41** | |

- 3 of 6 produced no trees; 7 to 45 commands refused per run; 3 wrote nothing to LOG.md.

Machine: 6 chain attempts yesterday, 3 got real work time (~160 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 8 clicks and 449 impressions on Google's freshest day (day before: c19/i609). Directional at best; no strategic conclusions from these volumes.

## 2026-08-18 (previous UTC day)

**Today: a waitlist arrived today (9 total).**

**Did the product happen**
- app-cta:     20 yesterday, last today
- walks-app:   3 yesterday, last yesterday
- save:        2 yesterday, last yesterday
- search-home: 1 yesterday, last today
- waitlist-submit: 1 yesterday, last today
- beacon-fix-verify: 0 yesterday, last 3 days ago
- beacon-test: 0 yesterday, last 3 days ago
- directions:  0 yesterday, last never
- search-explore: 0 yesterday, last 2 days ago
- signin-link-sent: 0 yesterday, last never
- smoke-test:  0 yesterday, last 18 days ago
- walk-open:   0 yesterday, last 2 days ago
- walk-start:  0 yesterday, last never
- worthit-not worth it: 0 yesterday, last 2 days ago
- worthit-worth it: 0 yesterday, last never

| Day | Accounts | Waitlist | Submissions |
|---|---:|---:|---:|
| 08-05 | 0 | 0 | 0 |
| 08-06 | 0 | 0 | 0 |
| 08-07 | 0 | 1 | 0 |
| 08-08 | 1 | 1 | 0 |
| 08-09 | 0 | 0 | 0 |
| 08-10 | 0 | 0 | 0 |
| 08-11 | 0 | 0 | 0 |
| 08-12 | 0 | 0 | 0 |
| 08-13 | 0 | 0 | 0 |
| 08-14 | 0 | 1 | 0 |
| 08-15 | 0 | 0 | 1 |
| 08-16 | 0 | 0 | 0 |
| 08-17 | 0 | 1 | 2 |
| 08-18 | 0 | 1 | 0 |
| 08-19 | 0 | 1 | 0 |
| **14 days** | **1** | **6** | **3** |
- Waitlist:    9 total, newest today
- Submissions: 3 total, newest 2 days ago
- Accounts:    3 total, newest 11 days ago

**The funnel, as rates**
- Seen to clicked: 2.3% (137 of 5834) vs 1.9% the fortnight before
- Pages per visit: 1.5 (550 visits, 830 pageviews since 2026-08-08)
- Visits that did something: 8.0% (44 actions on 550 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-09 | 6 | 305 | 2.0% | 11.8 |
| 08-10 | 16 | 394 | 4.1% | 13.5 |
| 08-11 | 8 | 415 | 1.9% | 12.9 |
| 08-12 | 9 | 441 | 2.0% | 19.1 |
| 08-13 | 9 | 445 | 2.0% | 17.6 |
| 08-14 | 13 | 517 | 2.5% | 14.2 |
| 08-15 | 15 | 630 | 2.4% | 14.4 |
| 08-16 | 14 | 723 | 1.9% | 13.9 |
| 08-17 | 15 | 600 | 2.5% | 14.7 |
| 08-18 | 13 | 449 | 2.9% | 13.3 |
| **window** | **118** | **4919** | **2.4%** | |
- Top queries (10d): juttepeer (i2, p3); oldest tree in central park (i4, p10); "oldest of its species" ginkgo park (i4, p6); 1800 trees (i1, p19); a tree in naples (i3, p9)
- Top pages (10d): / (c7/i51); /prague (c7/i114); /vienna (c4/i81); /amsterdam (c3/i131); /dublin (c3/i50)
- Content lead: 'alameda dos platanos' has no matching page (i6, p8)

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| rome | 2 | 215 | 0.9% | 14.5 | 1.3% | trees in rome (i12, p21) |
| palermo | 3 | 188 | 1.6% | 10.0 | 2.5% | palermo tree (i7, p10) |
| barcelona | 4 | 160 | 2.5% | 9.2 | 2.9% | high tree barcelona (i4, p10) |
| amsterdam | 3 | 156 | 1.9% | 12.2 | 1.8% | amsterdam tree (i6, p13) |
| prague | 7 | 124 | 5.6% | 8.0 | 3.5% | four trees prague (i2, p21) |
| london | 0 | 124 | 0.0% | 21.1 | 0.8% | oldest tree in london (i3, p54) |
| bath | 1 | 121 | 0.8% | 8.7 | 3.2% | the giant plane tree bath (i5, p10) |
| vienna | 7 | 120 | 5.8% | 9.5 | 2.7% | sulzwiese (i2, p6) |
| lisbon | 2 | 120 | 1.7% | 11.0 | 2.1% | oldest tree in lisbon (i6, p9) |
| cambridge | 0 | 105 | 0.0% | 31.3 | 0.4% | apple tree of newton (i4, p47) |
| paris | 5 | 104 | 4.8% | 21.4 | 0.7% | paris trees (i2, p62) |
| boston | 0 | 100 | 0.0% | 16.6 | 1.1% | shaw memorial elms (i2, p10) |
| florence | 0 | 92 | 0.0% | 10.3 | 2.4% | florence trees (i3, p16) |
| dublin | 6 | 90 | 6.7% | 14.8 | 1.2% | buchanan tree (i1, p10) |
| new-york | 3 | 90 | 3.3% | 16.1 | 1.1% | ancient elm (i1, p54) |
| malaga | 1 | 84 | 1.2% | 19.0 | 0.9% | árboles históricos de málaga (i12, p74) |
| istanbul | 1 | 81 | 1.2% | 12.5 | 1.7% | archeologisch museum van istanbul (i1, p1) |
| singapore | 1 | 80 | 1.2% | 15.5 | 1.2% | oldest tree in singapore (i23, p11) |
| washington-dc | 2 | 76 | 2.6% | 15.8 | 1.1% | survey lodge ranger station (i8, p11) |
| budapest | 1 | 74 | 1.4% | 9.4 | 2.8% | in budapest? (i1, p4) |
| geneva | 0 | 74 | 0.0% | 11.1 | 2.1% | - |
| brussels | 0 | 73 | 0.0% | 22.6 | 0.7% | belgian tree (i5, p58) |
| naples | 0 | 73 | 0.0% | 8.6 | 3.2% | a tree in naples (i3, p9) |
| milan | 0 | 68 | 0.0% | 10.1 | 2.5% | "oldest of its species" ginkgo park (i2, p6) |
| valencia | 1 | 65 | 1.5% | 8.5 | 3.3% | ficus centenarios de la glorieta (i2, p10) |
| es | 0 | 61 | 0.0% | 13.6 | 1.5% | árboles históricos de málaga (i7, p18) |
| nice | 1 | 60 | 1.7% | 11.3 | 2.0% | - |
| madrid | 0 | 59 | 0.0% | 9.6 | 2.7% | oldest tree in madrid (i3, p15) |
| porto | 2 | 56 | 3.6% | 6.8 | 4.2% | alameda dos platanos (i6, p8) |
| dubrovnik | 3 | 55 | 5.5% | 7.0 | 4.0% | trsteno plane tree (i3, p13) |
| seoul | 0 | 55 | 0.0% | 20.5 | 0.8% | common trees in korea (i1, p52) |
| bristol | 1 | 53 | 1.9% | 17.2 | 1.0% | bristol trees (i7, p53) |
| edinburgh | 1 | 50 | 2.0% | 20.3 | 0.8% | old tree near me (i1, p68) |
| sintra | 3 | 49 | 6.1% | 6.6 | 4.4% | how old is it? (i1, p3) |
| hong-kong | 1 | 47 | 2.1% | 11.9 | 1.9% | kam tin tree house (i6, p11) |
| venice | 1 | 47 | 2.1% | 7.1 | 4.0% | are there palm trees in venice italy (i2, p10) |
| copenhagen | 0 | 47 | 0.0% | 11.0 | 2.1% | trees in copenhagen (i3, p11) |
| the-hague | 5 | 46 | 10.9% | 5.8 | 5.3% | juttepeer (i2, p3) |
| granada | 0 | 46 | 0.0% | 12.4 | 1.7% | granada orange trees (i1, p64) |
| oslo | 1 | 44 | 2.3% | 10.5 | 2.3% | oak tree near me (i1, p3) |
| munich | 2 | 40 | 5.0% | 8.9 | 3.0% | - |
| reykjavik | 0 | 38 | 0.0% | 13.2 | 1.6% | oldest tree in iceland (i2, p8) |
| tokyo | 1 | 37 | 2.7% | 22.5 | 0.7% | - |
| seville | 0 | 37 | 0.0% | 8.5 | 3.2% | - |
| antwerp | 1 | 36 | 2.8% | 16.6 | 1.1% | klaverbladdreef (i1, p83) |
| zurich | 2 | 36 | 5.6% | 9.4 | 2.8% | zurich (i1, p2) |
| lyon | 0 | 36 | 0.0% | 15.0 | 1.2% | near lyon (i1, p10) |
| bologna | 0 | 34 | 0.0% | 6.8 | 4.2% | trees hours (i1, p11) |
| kyoto | 3 | 33 | 9.1% | 12.3 | 1.7% | kyoto tree (i6, p8) |
| bangkok | 1 | 33 | 3.0% | 10.4 | 2.4% | bangkok trees (i1, p9) |
| berlin | 0 | 33 | 0.0% | 16.0 | 1.1% | east berlin germany plants (i1, p77) |
| cadiz | 1 | 32 | 3.1% | 6.9 | 4.1% | ficus cadiz (i1, p10) |
| leiden | 3 | 31 | 9.7% | 11.7 | 1.9% | "oldest of its species" ginkgo park (i2, p6) |
| glasgow | 1 | 30 | 3.3% | 20.8 | 0.8% | oldest tree in glasgow (i1, p11) |
| helsinki | 1 | 30 | 3.3% | 8.3 | 3.4% | helsinki tree (i1, p8) |
| krakow | 1 | 28 | 3.6% | 6.8 | 4.2% | - |
| padua | 1 | 28 | 3.6% | 6.8 | 4.2% | - |
| belgrade | 0 | 28 | 0.0% | 14.3 | 1.3% | - |
| athens | 2 | 26 | 7.7% | 15.6 | 1.2% | old plane tree (i1, p39) |
| cork | 3 | 26 | 11.5% | 17.4 | 1.0% | trees cork (i2, p71) |
| osaka | 0 | 25 | 0.0% | 6.9 | 4.1% | meoto kusu (i1, p7) |
| oxford | 0 | 25 | 0.0% | 7.6 | 3.7% | - |
| genoa | 0 | 23 | 0.0% | 6.6 | 4.4% | - |
| portland | 0 | 23 | 0.0% | 17.1 | 1.0% | trees in portland or (i1, p55) |
| haarlem | 0 | 22 | 0.0% | 41.1 | 0.4% | noble tree (i9, p57) |
| utrecht | 0 | 22 | 0.0% | 14.2 | 1.4% | ginkgo utrecht (i2, p8) |
| split | 0 | 21 | 0.0% | 9.2 | 2.9% | - |
| rotterdam | 0 | 20 | 0.0% | 10.2 | 2.4% | old tree (i1, p6) |
| groningen | 2 | 19 | 10.5% | 20.6 | 0.8% | trees (i3, p10) |
| maastricht | 1 | 19 | 5.3% | 10.2 | 2.4% | - |
| turin | 1 | 19 | 5.3% | 5.0 | 7.0% | - |
| stockholm | 0 | 19 | 0.0% | 8.1 | 3.5% | - |
| setubal | 1 | 18 | 5.6% | 7.4 | 3.8% | francisco soveral (i1, p8) |
| nijmegen | 0 | 18 | 0.0% | 13.3 | 1.5% | oldest tree in the netherlands (i1, p5) |
| alicante | 0 | 17 | 0.0% | 6.9 | 4.1% | ja (i1, p2) |
| ljubljana | 0 | 16 | 0.0% | 4.7 | 7.3% | trees ljubljana (i1, p7) |
| warsaw | 0 | 16 | 0.0% | 11.1 | 2.1% | oldest tree in poland (i1, p53) |
| lucca | 0 | 15 | 0.0% | 11.3 | 2.1% | lucca tree (i3, p10) |
| breda | 0 | 14 | 0.0% | 18.1 | 0.9% | ulvenhoutselaan (i1, p13) |
| guimaraes | 0 | 14 | 0.0% | 7.8 | 3.6% | - |
| palma-de-mallorca | 0 | 14 | 0.0% | 9.8 | 2.6% | mallorca trees (i1, p11) |
| cordoba | 1 | 13 | 7.7% | 14.8 | 1.2% | jacaranda cordoba (i1, p12) |
| caserta | 0 | 13 | 0.0% | 17.1 | 1.0% | douglas fir teaching garden (i1, p81) |
| chicago | 1 | 12 | 8.3% | 10.0 | 2.5% | oldest tree in chicago (i1, p7) |
| sofia | 1 | 12 | 8.3% | 5.3 | 6.3% | - |
| trieste | 1 | 12 | 8.3% | 12.9 | 1.6% | pino fantasma (i1, p5) |
| bordeaux | 0 | 12 | 0.0% | 8.2 | 3.4% | caucasian elm (i1, p9) |
| den-bosch | 0 | 12 | 0.0% | 6.8 | 4.2% | - |
| strasbourg | 0 | 12 | 0.0% | 7.5 | 3.8% | - |
| bergamo | 0 | 11 | 0.0% | 7.4 | 3.8% | parco caprotti (i6, p10) |
| portugal | 0 | 11 | 0.0% | 51.7 | 0.4% | portuguese trees (i2, p66) |
| zaragoza | 0 | 11 | 0.0% | 6.9 | 4.1% | - |
| verona | 1 | 10 | 10.0% | 7.7 | 3.6% | - |
| arnhem | 0 | 10 | 0.0% | 10.3 | 2.4% | - |
| como | 0 | 10 | 0.0% | 22.3 | 0.7% | lake como tree (i2, p58) |
- Seen, not clicked: /rome (c0/i41, 0.0%) for trees in rome (i12, p21); rome tree (i5, p58); roman trees (i5, p32)
- Seen, not clicked: /cambridge/newtons-apple-tree (c0/i33, 0.0%) for apple tree of newton (i4, p47); newton's apple tree (i3, p53); isaac newton apple tree (i3, p46)
- Seen, not clicked: /singapore/oldest-tree (c0/i25, 0.0%) for oldest tree in singapore (i23, p11); singapore national tree (i2, p3)

**Who they are**
Audience, 28 days of search (196 clicks, 8591 impressions):
- Countries: usa c34/i1970; nld c18/i450; gbr c15/i1101; deu c14/i321; esp c10/i452
- Devices: MOBILE c136/i4761; DESKTOP c60/i3753; TABLET c0/i77
- Landing pages: / c10/i93; /lisbon c9/i231; /prague c8/i187; /amsterdam c6/i357; /vienna c6/i158

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-11 | 40 | 50 |
| 08-12 | 10 | 30 |
| 08-13 | 10 | 60 |
| 08-14 | 50 | 70 |
| 08-15 | 30 | 50 |
| 08-16 | 110 | 110 |
| 08-17 | 30 | 90 |
| 08-18 | 40 | 60 |
| **window** | **320** | **520** |
- Top paths: / (110); /barcelona (30); /copenhagen (30); /paris (30); /london/totteridge-yew (10)
- Referrers: (direct) (210); ancienttrees.app (200); www.google.com (110)
- Countries: NL (160); US (90); PT (40); GB (40); IE (40)
- Devices: desktop (270); mobile (250)
- Page load (8d): p50 599ms, p90 2972ms

Links: external referrers (a link somebody actually clicked): none yet
AI: arrivals from an assistant that cited us: none yet


**What the night shift did**

| Started | Minutes | Turns | Trees | Commits | Refused |
|---|---:|---:|---:|---:|---:|
| 08-18T20:16 | 0.0 | 1 | 0 | 0 | 0 |
| 08-18T23:16 | 0.0 | 1 | 0 | 0 | 0 |
| 08-19T02:49 | 0.0 | 1 | 0 | 0 | 0 |
| 08-19T05:20 | 0.0 | 1 | 0 | 0 | 0 |
| **4 runs** | **0** | | **0** | **0** | |

- 4 of 4 produced no trees; 4 wrote nothing to LOG.md.

Machine: 6 chain attempts yesterday, 2 got real work time (~44 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 13 clicks and 449 impressions on Google's freshest day (day before: c15/i600). Directional at best; no strategic conclusions from these volumes.

## 2026-08-17 (previous UTC day)

**Today: a waitlist arrived yesterday (7 total); a submission arrived yesterday (3 total).**

**Did the product happen**
- walk-open:   3 yesterday, last yesterday
- app-cta:     2 yesterday, last yesterday
- search-explore: 1 yesterday, last yesterday
- search-home: 1 yesterday, last yesterday
- waitlist-submit: 1 yesterday, last yesterday
- worthit-not worth it: 1 yesterday, last yesterday
- beacon-fix-verify: 0 yesterday, last 2 days ago
- beacon-test: 0 yesterday, last 2 days ago
- directions:  0 yesterday, last never
- save:        0 yesterday, last never
- signin-link-sent: 0 yesterday, last never
- smoke-test:  0 yesterday, last 17 days ago
- walk-start:  0 yesterday, last never
- worthit-worth it: 0 yesterday, last never

| Day | Accounts | Waitlist | Submissions |
|---|---:|---:|---:|
| 08-04 | 0 | 1 | 0 |
| 08-05 | 0 | 0 | 0 |
| 08-06 | 0 | 0 | 0 |
| 08-07 | 0 | 1 | 0 |
| 08-08 | 1 | 1 | 0 |
| 08-09 | 0 | 0 | 0 |
| 08-10 | 0 | 0 | 0 |
| 08-11 | 0 | 0 | 0 |
| 08-12 | 0 | 0 | 0 |
| 08-13 | 0 | 0 | 0 |
| 08-14 | 0 | 1 | 0 |
| 08-15 | 0 | 0 | 1 |
| 08-16 | 0 | 0 | 0 |
| 08-17 | 0 | 1 | 2 |
| 08-18 | 0 | 0 | 0 |
| **14 days** | **1** | **5** | **3** |
- Waitlist:    7 total, newest yesterday
- Submissions: 3 total, newest yesterday
- Accounts:    3 total, newest 10 days ago

**The funnel, as rates**
- Seen to clicked: 2.4% (130 of 5517) vs 2.2% the fortnight before
- Pages per visit: 1.5 (510 visits, 770 pageviews since 2026-08-08)
- Visits that did something: 2.4% (12 actions on 510 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-08 | 7 | 194 | 3.6% | 10.0 |
| 08-09 | 6 | 305 | 2.0% | 11.8 |
| 08-10 | 16 | 394 | 4.1% | 13.5 |
| 08-11 | 8 | 415 | 1.9% | 12.9 |
| 08-12 | 9 | 441 | 2.0% | 19.1 |
| 08-13 | 9 | 445 | 2.0% | 17.6 |
| 08-14 | 13 | 517 | 2.5% | 14.2 |
| 08-15 | 15 | 630 | 2.4% | 14.4 |
| 08-16 | 14 | 723 | 1.9% | 13.9 |
| 08-17 | 13 | 478 | 2.7% | 13.6 |
| **window** | **110** | **4542** | **2.4%** | |
- Top queries (10d): juttepeer (i2, p3); oldest tree in central park (i4, p10); "oldest of its species" ginkgo park (i2, p6); 1800 trees (i1, p19); a tree in naples (i3, p9)
- Top pages (10d): / (c7/i51); /prague (c5/i114); /kyoto (c4/i27); /vienna (c4/i73); /dublin (c3/i48)
- Content lead: 'oldest tree in central park' has no matching page (i4, p10)

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| rome | 3 | 199 | 1.5% | 15.2 | 1.2% | trees in rome (i14, p22) |
| palermo | 2 | 177 | 1.1% | 9.8 | 2.6% | palermo tree (i6, p10) |
| amsterdam | 2 | 146 | 1.4% | 12.4 | 1.7% | amsterdam tree (i6, p13) |
| barcelona | 4 | 140 | 2.9% | 8.3 | 3.3% | high tree barcelona (i4, p10) |
| prague | 6 | 131 | 4.6% | 7.9 | 3.5% | four trees prague (i2, p21) |
| lisbon | 1 | 115 | 0.9% | 11.2 | 2.1% | oldest tree in lisbon (i7, p9) |
| vienna | 8 | 114 | 7.0% | 9.5 | 2.7% | sulzwiese (i2, p6) |
| london | 0 | 113 | 0.0% | 21.0 | 0.8% | oldest tree in london (i3, p54) |
| bath | 1 | 105 | 1.0% | 8.6 | 3.2% | the giant plane tree bath (i5, p10) |
| cambridge | 0 | 96 | 0.0% | 30.4 | 0.4% | apple tree of newton (i4, p47) |
| paris | 5 | 94 | 5.3% | 21.0 | 0.8% | paris trees (i2, p62) |
| boston | 0 | 92 | 0.0% | 15.5 | 1.2% | boston trees (i1, p54) |
| florence | 0 | 91 | 0.0% | 9.9 | 2.5% | florence trees (i5, p11) |
| malaga | 0 | 89 | 0.0% | 19.9 | 0.8% | árboles históricos de málaga (i14, p74) |
| new-york | 3 | 88 | 3.4% | 16.5 | 1.1% | ancient elm (i1, p54) |
| dublin | 6 | 85 | 7.1% | 14.2 | 1.4% | buchanan tree (i1, p10) |
| istanbul | 1 | 77 | 1.3% | 12.7 | 1.7% | archeologisch museum van istanbul (i1, p1) |
| naples | 0 | 77 | 0.0% | 7.9 | 3.6% | a tree in naples (i3, p9) |
| brussels | 1 | 73 | 1.4% | 21.8 | 0.7% | belgian tree (i5, p58) |
| singapore | 1 | 70 | 1.4% | 14.9 | 1.2% | oldest tree in singapore (i20, p11) |
| budapest | 1 | 69 | 1.4% | 9.4 | 2.8% | in budapest? (i1, p4) |
| geneva | 0 | 69 | 0.0% | 11.0 | 2.1% | - |
| washington-dc | 2 | 64 | 3.1% | 14.0 | 1.4% | survey lodge ranger station (i7, p11) |
| valencia | 1 | 61 | 1.6% | 8.5 | 3.3% | ficus centenarios de la glorieta (i2, p10) |
| milan | 0 | 58 | 0.0% | 9.9 | 2.5% | - |
| porto | 2 | 54 | 3.7% | 7.3 | 3.9% | alameda dos platanos (i4, p8) |
| nice | 1 | 53 | 1.9% | 10.2 | 2.4% | - |
| edinburgh | 1 | 51 | 2.0% | 17.5 | 1.0% | old tree near me (i1, p68) |
| bristol | 1 | 49 | 2.0% | 16.2 | 1.1% | bristol trees (i5, p53) |
| madrid | 0 | 48 | 0.0% | 7.9 | 3.6% | oldest tree in madrid (i3, p15) |
| granada | 0 | 47 | 0.0% | 12.1 | 1.8% | granada orange trees (i1, p64) |
| dubrovnik | 2 | 45 | 4.4% | 6.9 | 4.1% | trsteno plane tree (i3, p13) |
| seoul | 0 | 45 | 0.0% | 18.7 | 0.9% | common trees in korea (i1, p52) |
| munich | 3 | 44 | 6.8% | 8.9 | 3.0% | - |
| the-hague | 3 | 42 | 7.1% | 5.9 | 5.2% | juttepeer (i2, p3) |
| es | 0 | 42 | 0.0% | 12.4 | 1.7% | árboles históricos de málaga (i4, p16) |
| copenhagen | 0 | 41 | 0.0% | 10.8 | 2.2% | trees in copenhagen (i2, p29) |
| sintra | 2 | 40 | 5.0% | 6.7 | 4.3% | how old is it? (i1, p3) |
| antwerp | 1 | 39 | 2.6% | 15.0 | 1.2% | den brandt park (i2, p70) |
| hong-kong | 1 | 39 | 2.6% | 11.4 | 2.0% | kam tin tree house (i6, p11) |
| oslo | 1 | 39 | 2.6% | 10.3 | 2.4% | oak tree near me (i1, p3) |
| venice | 1 | 39 | 2.6% | 7.6 | 3.7% | are there palm trees in venice italy (i2, p10) |
| bologna | 0 | 39 | 0.0% | 7.0 | 4.0% | trees hours (i1, p11) |
| reykjavik | 0 | 38 | 0.0% | 13.2 | 1.6% | oldest tree in iceland (i2, p8) |
| seville | 0 | 37 | 0.0% | 7.6 | 3.7% | - |
| lyon | 0 | 36 | 0.0% | 13.5 | 1.5% | near lyon (i1, p10) |
| kyoto | 5 | 35 | 14.3% | 11.7 | 1.9% | kyoto tree (i6, p8) |
| tokyo | 1 | 35 | 2.9% | 23.5 | 0.7% | - |
| berlin | 0 | 33 | 0.0% | 16.2 | 1.1% | east berlin germany plants (i1, p77) |
| athens | 2 | 32 | 6.2% | 15.4 | 1.2% | athens trees (i3, p9) |
| bangkok | 1 | 32 | 3.1% | 10.5 | 2.3% | bangkok trees (i1, p9) |
| zurich | 1 | 32 | 3.1% | 9.4 | 2.8% | zurich (i1, p2) |
| cadiz | 1 | 29 | 3.4% | 6.9 | 4.1% | ficus cadiz (i1, p10) |
| leiden | 3 | 28 | 10.7% | 12.0 | 1.8% | "oldest of its species" ginkgo park (i2, p6) |
| helsinki | 1 | 28 | 3.6% | 8.4 | 3.3% | helsinki tree (i1, p8) |
| krakow | 1 | 27 | 3.7% | 7.0 | 4.0% | - |
| padua | 1 | 27 | 3.7% | 6.9 | 4.1% | - |
| cork | 3 | 25 | 12.0% | 17.7 | 1.0% | trees cork (i2, p71) |
| glasgow | 1 | 25 | 4.0% | 23.8 | 0.6% | oldest tree in glasgow (i1, p11) |
| osaka | 0 | 25 | 0.0% | 6.9 | 4.1% | meoto kusu (i1, p7) |
| oxford | 0 | 25 | 0.0% | 7.6 | 3.7% | - |
| belgrade | 0 | 22 | 0.0% | 14.1 | 1.4% | - |
| portland | 0 | 22 | 0.0% | 17.4 | 1.0% | trees in portland or (i1, p55) |
| utrecht | 0 | 22 | 0.0% | 14.2 | 1.4% | ginkgo utrecht (i2, p8) |
| rotterdam | 0 | 19 | 0.0% | 10.4 | 2.4% | - |
| turin | 1 | 18 | 5.6% | 4.8 | 7.2% | - |
| haarlem | 0 | 18 | 0.0% | 46.1 | 0.4% | noble tree (i8, p57) |
| split | 0 | 18 | 0.0% | 8.3 | 3.4% | - |
| alicante | 0 | 17 | 0.0% | 6.9 | 4.1% | ja (i1, p2) |
| genoa | 0 | 17 | 0.0% | 6.8 | 4.2% | - |
| ljubljana | 0 | 16 | 0.0% | 4.7 | 7.3% | trees ljubljana (i1, p7) |
| warsaw | 0 | 16 | 0.0% | 11.1 | 2.1% | oldest tree in poland (i1, p53) |
| groningen | 2 | 15 | 13.3% | 24.3 | 0.6% | trees (i2, p8) |
| maastricht | 1 | 15 | 6.7% | 11.1 | 2.1% | - |
| setubal | 0 | 15 | 0.0% | 7.9 | 3.5% | francisco soveral (i1, p8) |
| palma-de-mallorca | 0 | 14 | 0.0% | 9.8 | 2.6% | mallorca trees (i1, p11) |
| breda | 0 | 13 | 0.0% | 15.5 | 1.2% | ulvenhoutselaan (i1, p13) |
| lucca | 0 | 13 | 0.0% | 11.7 | 1.9% | lucca tree (i3, p10) |
| nijmegen | 0 | 13 | 0.0% | 16.2 | 1.1% | oldest tree in the netherlands (i1, p5) |
| guimaraes | 0 | 12 | 0.0% | 8.1 | 3.5% | - |
| chicago | 1 | 11 | 9.1% | 10.4 | 2.4% | oldest tree in chicago (i1, p7) |
| cordoba | 1 | 11 | 9.1% | 16.4 | 1.1% | jacaranda cordoba (i1, p12) |
| bordeaux | 0 | 11 | 0.0% | 8.0 | 3.5% | caucasian elm (i1, p9) |
| caserta | 0 | 11 | 0.0% | 19.6 | 0.8% | douglas fir teaching garden (i1, p81) |
| den-bosch | 0 | 11 | 0.0% | 7.4 | 3.8% | - |
| portugal | 0 | 11 | 0.0% | 51.7 | 0.4% | portuguese trees (i2, p66) |
| sofia | 0 | 11 | 0.0% | 5.6 | 5.7% | - |
| stockholm | 0 | 11 | 0.0% | 7.8 | 3.6% | - |
| zaragoza | 0 | 11 | 0.0% | 6.9 | 4.1% | - |
| arnhem | 0 | 10 | 0.0% | 10.3 | 2.4% | - |
| como | 0 | 10 | 0.0% | 22.3 | 0.7% | lake como tree (i2, p58) |
| strasbourg | 0 | 10 | 0.0% | 7.0 | 4.0% | - |
- Seen, not clicked: /rome (c0/i42, 0.0%) for trees in rome (i14, p22); rome tree (i5, p58); roman trees (i4, p27)
- Seen, not clicked: /cambridge/newtons-apple-tree (c0/i31, 0.0%) for apple tree of newton (i4, p47); isaac newton apple tree (i3, p46); cambridge newton tree (i3, p54)
- Seen, not clicked: /singapore/oldest-tree (c0/i21, 0.0%) for oldest tree in singapore (i20, p11); singapore national tree (i1, p3)

**Who they are**
Audience, 28 days of search (182 clicks, 8025 impressions):
- Countries: usa c32/i1830; nld c16/i417; gbr c14/i1026; deu c13/i302; esp c10/i415
- Devices: MOBILE c124/i4467; DESKTOP c58/i3487; TABLET c0/i71
- Landing pages: / c11/i94; /lisbon c8/i224; /prague c6/i181; /vienna c6/i147; /amsterdam c5/i339

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-10 | 150 | 170 |
| 08-11 | 40 | 50 |
| 08-12 | 10 | 30 |
| 08-13 | 10 | 60 |
| 08-14 | 50 | 70 |
| 08-15 | 30 | 50 |
| 08-16 | 110 | 110 |
| 08-17 | 30 | 90 |
| **window** | **430** | **630** |
- Top paths: / (90); /barcelona (30); /copenhagen (30); /paris (30); /app (20)
- Referrers: (direct) (280); ancienttrees.app (200); www.google.com (140); zscaler-blocked.dpgmedia.net (10)
- Countries: NL (200); US (120); DE (70); PT (50); IE (40)
- Devices: desktop (400); mobile (230)
- Page load (8d): p50 622ms, p90 3470ms

Links: external referrers (a link somebody actually clicked): zscaler-blocked.dpgmedia.net (10)
AI: arrivals from an assistant that cited us: none yet

Machine: 6 chain attempts yesterday, 6 got real work time (~163 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 13 clicks and 478 impressions on Google's freshest day (day before: c14/i723). Directional at best; no strategic conclusions from these volumes.

## Weekly analysis 2026-08-17

Fourth weekly analysis, covering 2026-08-10 to 2026-08-16 against the prior
week (2026-08-03 to 2026-08-09), using the latest-settled Search Console
figure for each date.

**Scorecard**

| Week ending | Impressions | Clicks | CTR | Visits (beacon) | Pageviews (beacon) | Directions/visit | App-CTA | Waitlist total | Submissions total |
|---|---|---|---|---|---|---|---|---|---|
| 2026-07-31 | 1,150 | 31 | 2.7% | 70 | 170 | n/a (not captured) | n/a (not captured) | 0 real (2 test rows) | 0 real (1 test row) |
| 2026-08-07 | 1,762 | 36 | 2.0% | 100 | 170 | n/a (not captured) | n/a (not captured) | 4 real | 0 real (1 test row) |
| 2026-08-09 | 1,734 | 35 | 2.0% | 150 | 230 | n/a (not captured) | n/a (not captured) | 5 real | 0 real |
| 2026-08-16 | 3,457 | 81 | 2.3% | 410 | 560 | 0.0% (0 of 410) | 0 (0 of 410) | 6 real | 1 real |

**What moved:**
1. Impressions nearly doubled (1,734 to 3,457, settled) and clicks more than
   doubled (35 to 81), lifting CTR 2.0% to 2.3%: the strongest weekly jump
   since tracking began, concentrated in the last three days (08-14 to 08-16
   ran 517-630 impressions/day against 394-445 earlier in the week).
2. Beacon visits rose 173% (150 to 410) and pageviews 143% (230 to 560), not
   a boundary artifact: the 08-10 spike (150v/170pv) now sits fully inside
   this week's window, but 08-14 through 08-16 (50, 30, 110 visits) show the
   volume held up after it rather than reverting.
3. Rome's chronic 0%-CTR problem, flagged in both prior weekly analyses
   (08-08, 08-10), looks resolved: a steady 2 clicks/day (1.1% CTR) all
   week instead of zero. Malaga, the same-shape problem raised the same two
   weeks, has not moved: 0% CTR every single day again this week on 95-100
   daily impressions at position ~20.
4. Directions-click and app-cta are now real tracked numbers for the first
   time (previously "not captured" every week since 08-02's analysis first
   asked for this) and both read a firm zero across all 410 visits. One
   walk-open event fired on 08-16, the first real product action of any
   kind recorded since tracking began.
5. Waitlist and accounts stayed near-flat (waitlist 5 to 6, accounts steady
   at 3, no new signups since 08-08); submissions total reads 1 real, down
   from "2" mid-week after one of two 08-14 feedback reports turned out to
   be a self-marked test row.

**Suggestions, ranked:**
1. **[run]** Diagnose `/cambridge/newtons-apple-tree`'s 0% CTR. It has shown
   up in "seen, not clicked" three days running (08-14 to 08-16) on real
   impressions (21-25/day) at decent positions (p36-56) for "newton's apple
   tree", "oldest apple tree" and "apple tree of newton". Check P2
   (answer-first) and whether the title/meta wording matches these queries,
   the same class of fix that appears to have worked for Rome.
2. **[run]** Do for Malaga what happened for Rome, raised a third time now
   (08-08, 08-10, this week). The English `/malaga` page has taken 0 clicks
   on 95-100 impressions/day at position ~20-21 every day this week, exactly
   Rome's old shape, while Rome moved to 2 clicks/day. Check title/meta and
   P2 wording specifically; the earlier `/es/malaga` Spanish page targets a
   different query and does not fix this one.
3. **[run]** Write an answer for "oldest tree in Central Park." It has shown
   2-4 impressions at position ~10 for three straight days (08-14 to 08-16)
   with no matching content, while New York's page overall already converts
   at 3.6% CTR, well above the site average, suggesting this specific angle
   closes cheaply.
4. **[FOR HIDDE]** Directions-click and app-cta are measurable for the first
   time and both read zero across 410 real visits this week; the one
   walk-open event on 08-16 is the first real product action ever recorded.
   This is the first honest look at whether visitors use find/walk/collect
   beyond reading a story, and this week's answer is barely, and not the
   CTA. Worth having before the next product-priority call; no run action
   attached.
5. **[sessie]** Stop counting self-marked test rows in the submissions
   total. DATA.md read "2 total" through 08-14/08-15 then dropped to "1
   total" by 08-16 with no removal logged; the 08-14 pair were both
   feedback-type reports and one was explicitly suffixed "[TEST ROW]" in
   Supabase. If that is the read, filter it in the digest so the total
   does not wobble and confuse next week's comparison.

**Watch next week:** whether the 08-14 to 08-16 impressions jump holds or
reverts, whether Newton's apple tree or Malaga's CTR responds to any fix,
and whether a second walk-open or any directions/app-cta event ever fires.

## 2026-08-16 (previous UTC day)

**Today: nothing here needs you.** The blocks below are the standing picture.

**Did the product happen**
- beacon-fix-verify: 1 yesterday, last yesterday
- beacon-test: 1 yesterday, last yesterday
- walk-open:   1 yesterday, last yesterday
- app-cta:     0 yesterday, last never
- directions:  0 yesterday, last never
- save:        0 yesterday, last never
- signin-link-sent: 0 yesterday, last never
- smoke-test:  0 yesterday, last 16 days ago
- waitlist-submit: 0 yesterday, last never
- walk-start:  0 yesterday, last never
- worthit-not worth it: 0 yesterday, last never
- worthit-worth it: 0 yesterday, last never

| Day | Accounts | Waitlist | Submissions |
|---|---:|---:|---:|
| 08-03 | 0 | 0 | 0 |
| 08-04 | 0 | 1 | 0 |
| 08-05 | 0 | 0 | 0 |
| 08-06 | 0 | 0 | 0 |
| 08-07 | 0 | 1 | 0 |
| 08-08 | 1 | 1 | 0 |
| 08-09 | 0 | 0 | 0 |
| 08-10 | 0 | 0 | 0 |
| 08-11 | 0 | 0 | 0 |
| 08-12 | 0 | 0 | 0 |
| 08-13 | 0 | 0 | 0 |
| 08-14 | 0 | 1 | 0 |
| 08-15 | 0 | 0 | 1 |
| 08-16 | 0 | 0 | 0 |
| 08-17 | 0 | 0 | 0 |
| **14 days** | **1** | **4** | **1** |
- Waitlist:    6 total, newest 3 days ago
- Submissions: 1 total, newest 2 days ago
- Accounts:    3 total, newest 9 days ago

**The funnel, as rates**
- Seen to clicked: 2.2% (116 of 5191) vs 2.1% the fortnight before
- Pages per visit: 1.4 (480 visits, 680 pageviews since 2026-08-08)
- Visits that did something: 0.6% (3 actions on 480 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-07 | 5 | 226 | 2.2% | 9.7 |
| 08-08 | 7 | 194 | 3.6% | 10.0 |
| 08-09 | 6 | 305 | 2.0% | 11.8 |
| 08-10 | 16 | 394 | 4.1% | 13.5 |
| 08-11 | 8 | 415 | 1.9% | 12.9 |
| 08-12 | 9 | 441 | 2.0% | 19.1 |
| 08-13 | 9 | 445 | 2.0% | 17.6 |
| 08-14 | 13 | 517 | 2.5% | 14.2 |
| 08-15 | 15 | 630 | 2.4% | 14.4 |
| 08-16 | 11 | 615 | 1.8% | 12.4 |
| **window** | **99** | **4182** | **2.4%** | |
- Top queries (10d): juttepeer (i2, p3); oldest tree in central park (i4, p10); oldest tree in lisbon (i5, p9); "oldest of its species" ginkgo park (i2, p6); 1800 trees (i1, p19)
- Top pages (10d): / (c5/i48); /kyoto (c4/i29); /prague (c4/i111); /vienna (c4/i74); /dublin (c3/i39)
- Content lead: 'oldest tree in central park' has no matching page (i4, p10)

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal at that position |
|---|---:|---:|---:|---:|---:|
| rome | 2 | 187 | 1.1% | 15.9 | 1.1% |
| palermo | 2 | 171 | 1.2% | 9.9 | 2.6% |
| amsterdam | 1 | 140 | 0.7% | 12.3 | 1.7% |
| prague | 5 | 129 | 3.9% | 7.8 | 3.6% |
| vienna | 8 | 116 | 6.9% | 9.5 | 2.8% |
| barcelona | 3 | 112 | 2.7% | 7.6 | 3.7% |
| lisbon | 1 | 110 | 0.9% | 11.8 | 1.9% |
| london | 0 | 98 | 0.0% | 21.9 | 0.7% |
| malaga | 0 | 95 | 0.0% | 20.2 | 0.8% |
| paris | 5 | 87 | 5.7% | 19.2 | 0.9% |
| bath | 1 | 87 | 1.1% | 8.5 | 3.2% |
| new-york | 3 | 83 | 3.6% | 16.4 | 1.1% |
| boston | 0 | 82 | 0.0% | 14.5 | 1.3% |
| florence | 0 | 82 | 0.0% | 9.3 | 2.9% |
| dublin | 6 | 81 | 7.4% | 12.5 | 1.7% |
| istanbul | 1 | 81 | 1.2% | 12.4 | 1.7% |
| naples | 0 | 80 | 0.0% | 8.2 | 3.4% |
| cambridge | 0 | 78 | 0.0% | 28.7 | 0.5% |
| brussels | 1 | 67 | 1.5% | 18.6 | 0.9% |
| budapest | 0 | 64 | 0.0% | 9.6 | 2.7% |
| geneva | 0 | 62 | 0.0% | 11.2 | 2.1% |
| valencia | 1 | 60 | 1.7% | 7.8 | 3.6% |
| washington-dc | 1 | 59 | 1.7% | 14.6 | 1.3% |
| nice | 2 | 58 | 3.4% | 9.6 | 2.7% |
| singapore | 1 | 56 | 1.8% | 13.8 | 1.4% |
| porto | 2 | 54 | 3.7% | 7.3 | 3.9% |
| edinburgh | 1 | 51 | 2.0% | 14.3 | 1.3% |
| munich | 3 | 49 | 6.1% | 9.2 | 2.9% |
| milan | 0 | 47 | 0.0% | 8.7 | 3.1% |
| bristol | 1 | 46 | 2.2% | 15.2 | 1.2% |
| granada | 0 | 46 | 0.0% | 9.8 | 2.6% |
| dubrovnik | 1 | 42 | 2.4% | 6.8 | 4.2% |
| sintra | 4 | 41 | 9.8% | 6.3 | 4.7% |
| bologna | 0 | 41 | 0.0% | 7.0 | 4.0% |
| lyon | 0 | 40 | 0.0% | 13.1 | 1.6% |
| tokyo | 1 | 39 | 2.6% | 22.1 | 0.7% |
| antwerp | 1 | 38 | 2.6% | 15.7 | 1.1% |
| seoul | 0 | 38 | 0.0% | 19.3 | 0.9% |
| kyoto | 5 | 37 | 13.5% | 11.4 | 2.0% |
| oslo | 1 | 37 | 2.7% | 10.4 | 2.4% |
| the-hague | 3 | 37 | 8.1% | 5.8 | 5.5% |
| seville | 0 | 36 | 0.0% | 7.3 | 3.9% |
| athens | 0 | 35 | 0.0% | 16.2 | 1.1% |
| madrid | 0 | 34 | 0.0% | 7.6 | 3.7% |
| berlin | 1 | 33 | 3.0% | 16.7 | 1.1% |
| hong-kong | 1 | 33 | 3.0% | 8.5 | 3.2% |
| cadiz | 1 | 32 | 3.1% | 6.9 | 4.1% |
| venice | 1 | 32 | 3.1% | 7.9 | 3.5% |
| reykjavik | 0 | 32 | 0.0% | 14.4 | 1.3% |
| es | 0 | 31 | 0.0% | 11.1 | 2.1% |
| zurich | 1 | 30 | 3.3% | 8.2 | 3.4% |
| krakow | 1 | 27 | 3.7% | 7.0 | 4.0% |
| copenhagen | 0 | 26 | 0.0% | 9.8 | 2.6% |
| padua | 1 | 25 | 4.0% | 6.9 | 4.1% |
| helsinki | 0 | 25 | 0.0% | 8.6 | 3.2% |
| leiden | 2 | 24 | 8.3% | 13.0 | 1.6% |
| oxford | 0 | 23 | 0.0% | 7.7 | 3.7% |
| bangkok | 1 | 22 | 4.5% | 12.4 | 1.7% |
| glasgow | 1 | 22 | 4.5% | 22.0 | 0.7% |
| cork | 2 | 21 | 9.5% | 19.7 | 0.8% |
| belgrade | 0 | 21 | 0.0% | 14.3 | 1.3% |
| osaka | 0 | 20 | 0.0% | 7.4 | 3.8% |
| utrecht | 0 | 20 | 0.0% | 15.2 | 1.2% |
| portland | 0 | 19 | 0.0% | 18.7 | 0.9% |
| turin | 1 | 18 | 5.6% | 4.8 | 7.2% |
| rotterdam | 0 | 18 | 0.0% | 8.0 | 3.5% |
| haarlem | 0 | 17 | 0.0% | 45.4 | 0.4% |
| split | 0 | 17 | 0.0% | 8.6 | 3.2% |
| maastricht | 1 | 15 | 6.7% | 11.1 | 2.1% |
| warsaw | 0 | 15 | 0.0% | 11.3 | 2.0% |
| york | 0 | 14 | 0.0% | 11.2 | 2.1% |
| groningen | 2 | 13 | 15.4% | 21.2 | 0.8% |
| ljubljana | 0 | 13 | 0.0% | 4.4 | 7.6% |
| setubal | 0 | 13 | 0.0% | 8.5 | 3.2% |
| guimaraes | 0 | 12 | 0.0% | 8.1 | 3.5% |
| nijmegen | 0 | 12 | 0.0% | 17.2 | 1.0% |
| chicago | 1 | 11 | 9.1% | 10.4 | 2.4% |
| alicante | 0 | 11 | 0.0% | 6.1 | 4.9% |
| lucca | 0 | 11 | 0.0% | 12.5 | 1.7% |
| cordoba | 1 | 10 | 10.0% | 15.6 | 1.2% |
| verona | 1 | 10 | 10.0% | 7.0 | 4.0% |
| bordeaux | 0 | 10 | 0.0% | 7.8 | 3.6% |
| breda | 0 | 10 | 0.0% | 15.9 | 1.1% |
| den-bosch | 0 | 10 | 0.0% | 7.9 | 3.5% |
| zaragoza | 0 | 10 | 0.0% | 6.6 | 4.4% |
- Seen, not clicked: /cambridge/newtons-apple-tree (c0/i25, 0.0%) for apple tree of newton (i4, p47); oldest apple tree (i2, p36); newtons apple tree (i2, p50)

**Who they are** (full cut, Mondays)
Audience, 28 days of search (166 clicks, 7440 impressions):
- Countries: usa c29/i1682; gbr c14/i958; nld c14/i393; deu c12/i289; esp c10/i378
- Devices: MOBILE c112/i4144; DESKTOP c54/i3230; TABLET c0/i66
- Landing pages: / c9/i91; /lisbon c8/i209; /vienna c6/i141; /kyoto c5/i100; /porto c5/i37
- Search language (top 100 named queries, crude match, most clicks are in queries Google withholds): English 60q c2/i145; unclassified 34q c1/i67; Spanish 3q c0/i6; French 1q c0/i2; Italian 1q c0/i1; Dutch 1q c0/i1
On the site since 2026-08-08 (480 visits, 680 pageviews, 1.4 pages per visit):
- Countries: NL 260; US 110; DE 80; PT 60; IE 50
- Devices: desktop 500; mobile 180
- Browsers: Chrome 350; ChromeMobile 90; MobileSafari 70; Edge 50
- Arrived via: (direct) 340; ancienttrees.app 200; www.google.com 130; zscaler-blocked.dpgmedia.n 10
- Opened: / 90; /app 60; /porto 50; /paris 30; /barcelona 30; /boston 20; /prague 20; /naples 10

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-09 | 10 | 20 |
| 08-10 | 150 | 170 |
| 08-11 | 40 | 50 |
| 08-12 | 10 | 30 |
| 08-13 | 10 | 60 |
| 08-14 | 50 | 70 |
| 08-15 | 30 | 50 |
| 08-16 | 110 | 110 |
| **window** | **410** | **560** |
- Top paths: / (90); /barcelona (30); /app (30); /paris (30); /prague (20)
- Referrers: (direct) (270); ancienttrees.app (150); www.google.com (130); zscaler-blocked.dpgmedia.net (10)
- Countries: NL (210); US (100); DE (70); IE (40); PT (30)
- Devices: desktop (400); mobile (160)
- Page load (8d): p50 622ms, p90 3953ms

Links: external referrers (a link somebody actually clicked): zscaler-blocked.dpgmedia.net (10)
AI: arrivals from an assistant that cited us: none yet

Machine: 9 chain attempts yesterday, 9 got real work time (~153 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 11 clicks and 615 impressions on Google's freshest day (day before: c15/i630). Directional at best; no strategic conclusions from these volumes.

## 2026-08-15 (previous UTC day)

**Today: a submission arrived yesterday (1 total).**

**Did the product happen**
- app-cta:     0 yesterday, last never
- beacon-fix-verify: 0 yesterday, last today
- beacon-test: 0 yesterday, last today
- directions:  0 yesterday, last never
- save:        0 yesterday, last never
- signin-link-sent: 0 yesterday, last never
- smoke-test:  0 yesterday, last 15 days ago
- waitlist-submit: 0 yesterday, last never
- walk-open:   0 yesterday, last today
- walk-start:  0 yesterday, last never
- worthit-not worth it: 0 yesterday, last never
- worthit-worth it: 0 yesterday, last never

| Day | Accounts | Waitlist | Submissions |
|---|---:|---:|---:|
| 08-02 | 0 | 0 | 0 |
| 08-03 | 0 | 0 | 0 |
| 08-04 | 0 | 1 | 0 |
| 08-05 | 0 | 0 | 0 |
| 08-06 | 0 | 0 | 0 |
| 08-07 | 0 | 1 | 0 |
| 08-08 | 1 | 1 | 0 |
| 08-09 | 0 | 0 | 0 |
| 08-10 | 0 | 0 | 0 |
| 08-11 | 0 | 0 | 0 |
| 08-12 | 0 | 0 | 0 |
| 08-13 | 0 | 0 | 0 |
| 08-14 | 0 | 1 | 0 |
| 08-15 | 0 | 0 | 1 |
| 08-16 | 0 | 0 | 0 |
| **14 days** | **1** | **4** | **1** |
- Waitlist:    6 total, newest 2 days ago
- Submissions: 1 total, newest yesterday
- Accounts:    3 total, newest 8 days ago

**The funnel, as rates**
- Seen to clicked: 2.3% (111 of 4805) vs 2.2% the fortnight before
- Pages per visit: 1.5 (370 visits, 570 pageviews since 2026-08-08)
- Visits that did something: 0.8% (3 actions on 370 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-06 | 7 | 215 | 3.3% | 13.4 |
| 08-07 | 5 | 226 | 2.2% | 9.7 |
| 08-08 | 7 | 194 | 3.6% | 10.0 |
| 08-09 | 6 | 305 | 2.0% | 11.8 |
| 08-10 | 16 | 394 | 4.1% | 13.5 |
| 08-11 | 8 | 415 | 1.9% | 12.9 |
| 08-12 | 9 | 441 | 2.0% | 19.1 |
| 08-13 | 9 | 445 | 2.0% | 17.6 |
| 08-14 | 13 | 517 | 2.5% | 14.2 |
| 08-15 | 14 | 560 | 2.5% | 14.4 |
| **window** | **94** | **3712** | **2.5%** | |
- Top queries (10d): juttepeer (i2, p3); oldest tree in central park (i3, p10); oldest tree in lisbon (i4, p10); "oldest of its species" ginkgo park (i2, p6); 1800 trees (i1, p19)
- Top pages (10d): / (c5/i48); /kyoto (c4/i32); /prague (c4/i101); /vienna (c4/i66); /munich (c3/i47)
- Content lead: 'oldest tree in central park' has no matching page (i3, p10)

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal at that position |
|---|---:|---:|---:|---:|---:|
| rome | 2 | 186 | 1.1% | 16.3 | 1.1% |
| palermo | 4 | 161 | 2.5% | 9.7 | 2.7% |
| amsterdam | 2 | 138 | 1.4% | 12.3 | 1.7% |
| prague | 6 | 120 | 5.0% | 8.3 | 3.4% |
| vienna | 8 | 102 | 7.8% | 9.3 | 2.9% |
| malaga | 0 | 100 | 0.0% | 21.1 | 0.8% |
| barcelona | 3 | 99 | 3.0% | 8.2 | 3.4% |
| lisbon | 1 | 95 | 1.1% | 9.3 | 2.8% |
| london | 0 | 95 | 0.0% | 21.8 | 0.7% |
| paris | 3 | 84 | 3.6% | 18.1 | 1.0% |
| naples | 0 | 81 | 0.0% | 8.4 | 3.3% |
| new-york | 2 | 80 | 2.5% | 16.8 | 1.1% |
| dublin | 4 | 75 | 5.3% | 12.8 | 1.6% |
| boston | 0 | 75 | 0.0% | 15.0 | 1.2% |
| cambridge | 0 | 72 | 0.0% | 28.0 | 0.5% |
| florence | 0 | 71 | 0.0% | 8.6 | 3.2% |
| istanbul | 0 | 71 | 0.0% | 13.0 | 1.6% |
| nice | 2 | 63 | 3.2% | 9.4 | 2.8% |
| brussels | 1 | 57 | 1.8% | 19.4 | 0.8% |
| valencia | 1 | 57 | 1.8% | 7.9 | 3.6% |
| bath | 0 | 55 | 0.0% | 8.5 | 3.3% |
| geneva | 0 | 55 | 0.0% | 11.7 | 1.9% |
| munich | 3 | 54 | 5.6% | 9.5 | 2.8% |
| edinburgh | 1 | 52 | 1.9% | 14.1 | 1.4% |
| porto | 3 | 51 | 5.9% | 7.2 | 3.9% |
| washington-dc | 1 | 50 | 2.0% | 15.7 | 1.1% |
| budapest | 0 | 49 | 0.0% | 10.4 | 2.4% |
| singapore | 1 | 46 | 2.2% | 14.3 | 1.3% |
| granada | 0 | 45 | 0.0% | 9.2 | 2.9% |
| milan | 0 | 44 | 0.0% | 8.8 | 3.1% |
| kyoto | 5 | 43 | 11.6% | 14.3 | 1.3% |
| bologna | 0 | 43 | 0.0% | 8.5 | 3.3% |
| sintra | 4 | 41 | 9.8% | 6.1 | 4.9% |
| tokyo | 1 | 41 | 2.4% | 23.2 | 0.7% |
| antwerp | 1 | 40 | 2.5% | 18.5 | 0.9% |
| seville | 1 | 40 | 2.5% | 7.8 | 3.6% |
| bristol | 0 | 39 | 0.0% | 16.4 | 1.1% |
| dubrovnik | 1 | 38 | 2.6% | 6.8 | 4.2% |
| lyon | 1 | 38 | 2.6% | 14.5 | 1.3% |
| berlin | 1 | 36 | 2.8% | 17.2 | 1.0% |
| cadiz | 1 | 36 | 2.8% | 6.9 | 4.1% |
| athens | 0 | 34 | 0.0% | 18.8 | 0.9% |
| seoul | 0 | 33 | 0.0% | 20.0 | 0.8% |
| the-hague | 3 | 32 | 9.4% | 5.8 | 5.4% |
| hong-kong | 1 | 30 | 3.3% | 8.7 | 3.2% |
| venice | 0 | 30 | 0.0% | 8.3 | 3.3% |
| oslo | 1 | 27 | 3.7% | 10.3 | 2.4% |
| krakow | 1 | 23 | 4.3% | 6.9 | 4.1% |
| reykjavik | 0 | 22 | 0.0% | 15.1 | 1.2% |
| oxford | 0 | 21 | 0.0% | 7.4 | 3.8% |
| leiden | 2 | 20 | 10.0% | 14.1 | 1.4% |
| zurich | 1 | 20 | 5.0% | 8.9 | 3.0% |
| madrid | 0 | 20 | 0.0% | 7.0 | 4.0% |
| belgrade | 0 | 19 | 0.0% | 14.9 | 1.2% |
| glasgow | 0 | 18 | 0.0% | 22.3 | 0.7% |
| padua | 1 | 17 | 5.9% | 7.1 | 3.9% |
| split | 0 | 17 | 0.0% | 8.6 | 3.2% |
| utrecht | 0 | 17 | 0.0% | 16.8 | 1.1% |
| bangkok | 1 | 16 | 6.2% | 5.2 | 6.5% |
| york | 0 | 15 | 0.0% | 11.3 | 2.1% |
| cork | 1 | 14 | 7.1% | 20.9 | 0.8% |
| copenhagen | 0 | 14 | 0.0% | 7.8 | 3.6% |
| es | 0 | 14 | 0.0% | 7.8 | 3.6% |
| portland | 0 | 14 | 0.0% | 23.2 | 0.7% |
| rotterdam | 0 | 14 | 0.0% | 6.8 | 4.2% |
| turin | 0 | 14 | 0.0% | 5.1 | 6.9% |
| haarlem | 0 | 13 | 0.0% | 43.1 | 0.4% |
| groningen | 2 | 12 | 16.7% | 16.1 | 1.1% |
| maastricht | 1 | 12 | 8.3% | 11.5 | 2.0% |
| verona | 1 | 12 | 8.3% | 6.2 | 4.8% |
| setubal | 0 | 12 | 0.0% | 8.9 | 3.0% |
| chicago | 1 | 10 | 10.0% | 11.3 | 2.0% |
| nijmegen | 0 | 10 | 0.0% | 19.4 | 0.8% |
| zaragoza | 0 | 10 | 0.0% | 6.6 | 4.4% |
- Seen, not clicked: /rome (c0/i35, 0.0%) for trees in rome (i12, p25); rome tree (i5, p58); roman trees (i3, p32)
- Seen, not clicked: /cambridge/newtons-apple-tree (c0/i22, 0.0%) for apple tree of newton (i3, p46); oldest apple tree (i2, p36); newton's apple tree (i2, p56)

**Who they are**
Audience, 28 days of search (154 clicks, 6755 impressions):
- Countries: usa c25/i1511; nld c14/i357; deu c12/i262; gbr c12/i859; esp c10/i336
- Devices: MOBILE c101/i3769; DESKTOP c53/i2922; TABLET c0/i64
- Landing pages: / c9/i89; /lisbon c8/i193; /vienna c6/i130; /kyoto c5/i100; /porto c5/i37

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-08 | 70 | 120 |
| 08-09 | 10 | 20 |
| 08-10 | 150 | 170 |
| 08-11 | 40 | 50 |
| 08-12 | 10 | 30 |
| 08-13 | 10 | 60 |
| 08-14 | 50 | 70 |
| 08-15 | 30 | 50 |
| **window** | **370** | **570** |
- Top paths: / (70); /porto (50); /app (50); /barcelona (30); /prague (20)
- Referrers: (direct) (270); ancienttrees.app (200); www.google.com (90); zscaler-blocked.dpgmedia.net (10)
- Countries: NL (230); US (90); DE (70); PT (60); IE (30)
- Devices: desktop (410); mobile (160)
- Page load (8d): p50 577ms, p90 5169ms

Links: external referrers (a link somebody actually clicked): zscaler-blocked.dpgmedia.net (10)
AI: arrivals from an assistant that cited us: none yet

Machine: 9 chain attempts yesterday, 9 got real work time (~163 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 14 clicks and 560 impressions on Google's freshest day (day before: c13/i517). Directional at best; no strategic conclusions from these volumes.

## 2026-08-14 (previous UTC day)

**Today: a waitlist arrived yesterday (6 total); a submission arrived yesterday (2 total).**

**Did the product happen**
- app-cta:     0 yesterday, last never
- directions:  0 yesterday, last never
- save:        0 yesterday, last never
- signin-link-sent: 0 yesterday, last never
- smoke-test:  0 yesterday, last 14 days ago
- waitlist-submit: 0 yesterday, last never
- walk-open:   0 yesterday, last never
- walk-start:  0 yesterday, last never
- worthit-worth it: 0 yesterday, last never

| Day | Accounts | Waitlist | Submissions |
|---|---:|---:|---:|
| 08-01 | 0 | 0 | 0 |
| 08-02 | 0 | 0 | 0 |
| 08-03 | 0 | 0 | 0 |
| 08-04 | 0 | 1 | 0 |
| 08-05 | 0 | 0 | 0 |
| 08-06 | 0 | 0 | 0 |
| 08-07 | 0 | 1 | 0 |
| 08-08 | 1 | 1 | 0 |
| 08-09 | 0 | 0 | 0 |
| 08-10 | 0 | 0 | 0 |
| 08-11 | 0 | 0 | 0 |
| 08-12 | 0 | 0 | 0 |
| 08-13 | 0 | 0 | 0 |
| 08-14 | 0 | 1 | 2 |
| 08-15 | 0 | 0 | 0 |
| **14 days** | **1** | **4** | **2** |
- Waitlist:    6 total, newest yesterday
- Submissions: 2 total, newest yesterday
- Accounts:    3 total, newest 7 days ago

**The funnel, as rates**
- Seen to clicked: 2.3% (99 of 4379) vs 2.2% the fortnight before
- Pages per visit: 1.7 (268 visits, 445 pageviews since 2026-08-08)
- Visits that did something: 0.0% (0 actions on 268 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-05 | 0 | 280 | 0.0% | 14.1 |
| 08-06 | 7 | 215 | 3.3% | 13.4 |
| 08-07 | 5 | 226 | 2.2% | 9.7 |
| 08-08 | 7 | 194 | 3.6% | 10.0 |
| 08-09 | 6 | 305 | 2.0% | 11.8 |
| 08-10 | 16 | 394 | 4.1% | 13.5 |
| 08-11 | 8 | 415 | 1.9% | 12.9 |
| 08-12 | 9 | 441 | 2.0% | 19.1 |
| 08-13 | 5 | 445 | 1.1% | 17.6 |
| 08-14 | 12 | 398 | 3.0% | 14.9 |
| **window** | **75** | **3313** | **2.3%** | |
- Top queries (10d): oldest tree in lisbon (i4, p10); "oldest of its species" ginkgo park (i2, p6); 1800 trees (i1, p19); a tree in naples (i3, p9); american elm central park (i1, p37)
- Top pages (10d): / (c4/i38); /kyoto (c4/i37); /prague (c4/i92); /vienna (c4/i68); /munich (c3/i55)
- Content lead: 'belgian tree' has no matching page (i6, p58)

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions |
|---|---:|---:|
| palermo | 3 | 153 |
| amsterdam | 1 | 138 |
| rome | 2 | 122 |
| prague | 6 | 103 |
| barcelona | 2 | 93 |
| vienna | 7 | 75 |
| boston | 0 | 62 |
| lisbon | 1 | 60 |
| brussels | 1 | 57 |
| munich | 3 | 55 |
| cambridge | 0 | 54 |
| dublin | 2 | 51 |
| cadiz | 1 | 41 |
| antwerp | 1 | 40 |
| bologna | 0 | 39 |
| kyoto | 5 | 38 |
| athens | 0 | 38 |
| nice | 2 | 37 |
| budapest | 0 | 37 |
| berlin | 1 | 35 |
| lyon | 1 | 35 |
| bristol | 0 | 33 |
| tokyo | 1 | 24 |
| porto | 3 | 23 |
| sintra | 4 | 23 |
| dubrovnik | 1 | 20 |
| seville | 1 | 17 |
| belgrade | 0 | 17 |
| bangkok | 1 | 14 |
| zurich | 1 | 14 |
| bath | 0 | 14 |
| leiden | 1 | 13 |
| washington-dc | 1 | 10 |
- Seen, not clicked: /rome (c0/i36, 0.0%) for trees in rome (i12, p25); rome tree (i5, p58); roman trees (i3, p48)
- Seen, not clicked: /cambridge/newtons-apple-tree (c0/i21, 0.0%) for oldest apple tree (i2, p36); newton's apple tree (i2, p56); isaac newton's tree (i2, p47)
- Seen, not clicked: /malaga (c0/i21, 0.0%) for árboles históricos de málaga (i20, p74); malaga tree (i1, p4)

**Who they are**
Audience, 28 days of search (135 clicks, 6076 impressions):
- Countries: usa c23/i1332; gbr c11/i754; deu c10/i244; nld c10/i321; esp c9/i307
- Devices: MOBILE c91/i3337; DESKTOP c44/i2683; TABLET c0/i56
- Landing pages: / c8/i76; /lisbon c8/i186; /vienna c6/i122; /kyoto c5/i100; /porto c5/i36

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-07 | 30 | 30 |
| 08-08 | 70 | 120 |
| 08-09 | 10 | 20 |
| 08-10 | 150 | 170 |
| 08-11 | 40 | 50 |
| 08-12 | 10 | 30 |
| 08-13 | 10 | 60 |
| 08-14 | 50 | 70 |
| **window** | **370** | **550** |
- Top paths: / (60); /app (50); /porto (50); /barcelona (30); /prague (20)
- Referrers: (direct) (260); ancienttrees.app (180); www.google.com (100); zscaler-blocked.dpgmedia.net (10)
- Countries: NL (210); US (100); DE (80); PT (60); CH (20)
- Devices: desktop (420); mobile (130)
- Page load (8d): p50 578ms, p90 5169ms

Links: external referrers (a link somebody actually clicked): zscaler-blocked.dpgmedia.net (10)

Machine: 7 chain attempts yesterday, 6 got real work time (~139 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 12 clicks and 398 impressions on Google's freshest day (day before: c5/i445). Directional at best; no strategic conclusions from these volumes.

## 2026-08-13 (previous UTC day)

**Today: a submission arrived today (2 total).**

**Did the product happen**
- app-cta:     0 yesterday, last never
- collect:     0 yesterday, last never
- directions:  0 yesterday, last never
- share:       0 yesterday, last never
- smoke-test:  0 yesterday, last 13 days ago
- walk-start:  0 yesterday, last never

| Day | Accounts | Waitlist | Submissions |
|---|---:|---:|---:|
| 07-31 | 0 | 2 | 0 |
| 08-01 | 0 | 0 | 0 |
| 08-02 | 0 | 0 | 0 |
| 08-03 | 0 | 0 | 0 |
| 08-04 | 0 | 1 | 0 |
| 08-05 | 0 | 0 | 0 |
| 08-06 | 0 | 0 | 0 |
| 08-07 | 0 | 1 | 0 |
| 08-08 | 1 | 1 | 0 |
| 08-09 | 0 | 0 | 0 |
| 08-10 | 0 | 0 | 0 |
| 08-11 | 0 | 0 | 0 |
| 08-12 | 0 | 0 | 0 |
| 08-13 | 0 | 0 | 0 |
| 08-14 | 0 | 0 | 2 |
| **14 days** | **1** | **5** | **2** |
- Waitlist:    5 total, newest 6 days ago
- Submissions: 2 total, newest today
- Accounts:    3 total, newest 6 days ago

**The funnel, as rates**
- Seen to clicked: 2.1% (89 of 4160) vs 2.1% the fortnight before
- Pages per visit: 1.6 (234 visits, 378 pageviews since 2026-08-08)
- Visits that did something: 0.0% (0 actions on 234 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-04 | 8 | 254 | 3.1% | 11.1 |
| 08-05 | 0 | 280 | 0.0% | 14.1 |
| 08-06 | 7 | 215 | 3.3% | 13.4 |
| 08-07 | 5 | 226 | 2.2% | 9.7 |
| 08-08 | 7 | 194 | 3.6% | 10.0 |
| 08-09 | 6 | 305 | 2.0% | 11.8 |
| 08-10 | 16 | 394 | 4.1% | 13.5 |
| 08-11 | 8 | 415 | 1.9% | 12.9 |
| 08-12 | 9 | 441 | 2.0% | 19.1 |
| 08-13 | 5 | 394 | 1.3% | 16.0 |
| **window** | **71** | **3118** | **2.3%** | |
- Top queries (10d): oldest tree in lisbon (i4, p10); "oldest of its species" ginkgo park (i2, p6); 1800 trees (i1, p19); 400 year old tree (i1, p18); a tree in naples (i3, p9)
- Top pages (10d): / (c4/i33); /app (c4/i14); /kyoto (c4/i40); /prague (c4/i83); /munich (c3/i59)
- Content lead: 'belgian tree' has no matching page (i6, p58)

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions |
|---|---:|---:|
| palermo | 3 | 158 |
| amsterdam | 2 | 156 |
| rome | 2 | 124 |
| prague | 6 | 94 |
| barcelona | 1 | 92 |
| vienna | 5 | 73 |
| lisbon | 3 | 67 |
| munich | 3 | 59 |
| brussels | 1 | 55 |
| boston | 0 | 54 |
| dublin | 2 | 53 |
| bologna | 0 | 43 |
| kyoto | 5 | 42 |
| cadiz | 1 | 42 |
| nice | 2 | 42 |
| athens | 0 | 41 |
| antwerp | 1 | 39 |
| berlin | 1 | 36 |
| cambridge | 0 | 36 |
| lyon | 1 | 33 |
| bristol | 0 | 28 |
| porto | 4 | 26 |
| budapest | 0 | 26 |
| sintra | 4 | 23 |
| seville | 1 | 23 |
| tokyo | 1 | 23 |
| belgrade | 0 | 16 |
| dubrovnik | 1 | 14 |
| bangkok | 1 | 12 |
- Seen, not clicked: /rome (c0/i37, 0.0%) for trees in rome (i14, p23); rome tree (i5, p58); roman trees (i3, p48)
- Seen, not clicked: /malaga (c0/i21, 0.0%) for árboles históricos de málaga (i20, p74); malaga tree (i1, p4)

**Who they are**
Audience, 28 days of search (123 clicks, 5627 impressions):
- Countries: usa c20/i1227; gbr c11/i689; deu c10/i228; nld c9/i301; prt c8/i150
- Devices: MOBILE c84/i3087; DESKTOP c39/i2487; TABLET c0/i53
- Landing pages: /lisbon c8/i184; / c6/i65; /kyoto c5/i96; /porto c5/i36; /prague c5/i130

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-06 | 0 | 10 |
| 08-07 | 30 | 30 |
| 08-08 | 70 | 120 |
| 08-09 | 10 | 20 |
| 08-10 | 150 | 170 |
| 08-11 | 40 | 50 |
| 08-12 | 10 | 30 |
| 08-13 | 10 | 60 |
| **window** | **320** | **490** |
- Top paths: /app (50); /porto (50); / (40); /boston (20); /prague (20)
- Referrers: (direct) (220); ancienttrees.app (170); www.google.com (90); zscaler-blocked.dpgmedia.net (10)
- Countries: NL (160); DE (80); US (80); PT (60); CH (20)
- Devices: desktop (380); mobile (110)
- Page load (8d): p50 752ms, p90 7177ms

Links: external referrers (a link somebody actually clicked): zscaler-blocked.dpgmedia.net (10)

Machine: 10 chain attempts yesterday, 10 got real work time (~153 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 5 clicks and 394 impressions on Google's freshest day (day before: c9/i441). Directional at best; no strategic conclusions from these volumes.

## 2026-08-12 (previous UTC day)

**Today: nothing here needs you.** The blocks below are the standing picture.

**Did the product happen**
- app-cta:     0 yesterday, last never
- collect:     0 yesterday, last never
- directions:  0 yesterday, last never
- share:       0 yesterday, last never
- smoke-test:  0 yesterday, last 12 days ago
- walk-start:  0 yesterday, last never

| Day | Accounts | Waitlist | Submissions |
|---|---:|---:|---:|
| 07-30 | 0 | 0 | 0 |
| 07-31 | 0 | 2 | 0 |
| 08-01 | 0 | 0 | 0 |
| 08-02 | 0 | 0 | 0 |
| 08-03 | 0 | 0 | 0 |
| 08-04 | 0 | 1 | 0 |
| 08-05 | 0 | 0 | 0 |
| 08-06 | 0 | 0 | 0 |
| 08-07 | 0 | 1 | 0 |
| 08-08 | 1 | 1 | 0 |
| 08-09 | 0 | 0 | 0 |
| 08-10 | 0 | 0 | 0 |
| 08-11 | 0 | 0 | 0 |
| 08-12 | 0 | 0 | 0 |
| 08-13 | 0 | 0 | 0 |
| **14 days** | **1** | **5** | **0** |
- Waitlist:    5 total, newest 5 days ago
- Submissions: 0 total, newest never
- Accounts:    3 total, newest 5 days ago

**The funnel, as rates**
- Seen to clicked: 2.2% (91 of 4078) vs 2.3% the fortnight before
- Pages per visit: 1.5 (217 visits, 325 pageviews since 2026-08-08)
- Visits that did something: 0.0% (0 actions on 217 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-03 | 2 | 260 | 0.8% | 12.7 |
| 08-04 | 8 | 254 | 3.1% | 11.1 |
| 08-05 | 0 | 280 | 0.0% | 14.1 |
| 08-06 | 7 | 215 | 3.3% | 13.4 |
| 08-07 | 5 | 226 | 2.2% | 9.7 |
| 08-08 | 7 | 194 | 3.6% | 10.0 |
| 08-09 | 6 | 305 | 2.0% | 11.8 |
| 08-10 | 16 | 394 | 4.1% | 13.5 |
| 08-11 | 8 | 415 | 1.9% | 12.9 |
| 08-12 | 9 | 434 | 2.1% | 19.2 |
| 08-13 | 0 | 68 | 0.0% | 9.1 |
| **window** | **68** | **3045** | **2.2%** | |
- Top queries (10d): oldest tree in lisbon (i3, p10); "oldest of its species" ginkgo park (i2, p6); 1800 trees (i1, p19); 400 year old tree (i1, p18); a tree in naples (i3, p9)
- Top pages (10d): / (c4/i31); /app (c4/i14); /kyoto (c4/i41); /prague (c4/i78); /porto (c3/i24)
- Content lead: 'belgian tree' has no matching page (i6, p58)

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions |
|---|---:|---:|
| amsterdam | 2 | 177 |
| palermo | 3 | 175 |
| rome | 2 | 140 |
| barcelona | 2 | 94 |
| prague | 6 | 91 |
| lisbon | 3 | 70 |
| vienna | 5 | 68 |
| munich | 2 | 59 |
| dublin | 1 | 57 |
| bologna | 0 | 55 |
| brussels | 1 | 51 |
| cadiz | 1 | 47 |
| antwerp | 0 | 45 |
| athens | 0 | 45 |
| boston | 0 | 44 |
| kyoto | 5 | 43 |
| nice | 3 | 40 |
| berlin | 1 | 34 |
| cambridge | 0 | 32 |
| lyon | 1 | 31 |
| seville | 1 | 27 |
| porto | 4 | 26 |
| bristol | 0 | 25 |
| tokyo | 1 | 24 |
| budapest | 0 | 22 |
| sintra | 4 | 20 |
| belgrade | 0 | 16 |
| dubrovnik | 1 | 11 |
- Seen, not clicked: /rome (c0/i49, 0.0%) for trees in rome (i16, p24); rome tree (i8, p56); trees of rome italy (i3, p48)
- Seen, not clicked: /malaga (c0/i21, 0.0%) for árboles históricos de málaga (i20, p74); malaga tree (i1, p4)

**Who they are**
Audience, 28 days of search (118 clicks, 5294 impressions):
- Countries: usa c20/i1148; gbr c11/i648; deu c10/i218; nld c8/i275; prt c8/i141
- Devices: MOBILE c81/i2894; DESKTOP c37/i2350; TABLET c0/i50
- Landing pages: /lisbon c8/i176; / c6/i61; /kyoto c5/i95; /porto c5/i36; /prague c5/i119

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-05 | 20 | 20 |
| 08-06 | 0 | 10 |
| 08-07 | 30 | 30 |
| 08-08 | 70 | 120 |
| 08-09 | 10 | 20 |
| 08-10 | 150 | 170 |
| 08-11 | 40 | 50 |
| 08-12 | 10 | 30 |
| **window** | **330** | **450** |
- Top paths: /app (50); /porto (50); / (30); /boston (20); /prague (20)
- Referrers: (direct) (240); ancienttrees.app (120); www.google.com (80); zscaler-blocked.dpgmedia.net (10)
- Countries: NL (130); US (90); DE (80); PT (50); IE (20)
- Devices: desktop (350); mobile (100)
- Page load (8d): p50 1019ms, p90 7177ms

Links: external referrers (a link somebody actually clicked): zscaler-blocked.dpgmedia.net (10)

Machine: 7 chain attempts yesterday, 7 got real work time (~92 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 0 clicks and 68 impressions on Google's freshest day (day before: c9/i434). Directional at best; no strategic conclusions from these volumes.

## 2026-08-11 (previous UTC day)

**Today: nothing here needs you.** The blocks below are the standing picture.

**Did the product happen**
- app-cta:     0 yesterday, last never
- collect:     0 yesterday, last never
- directions:  0 yesterday, last never
- share:       0 yesterday, last never
- smoke-test:  0 yesterday, last 11 days ago
- walk-start:  0 yesterday, last never

| Day | Accounts | Waitlist | Submissions |
|---|---:|---:|---:|
| 07-29 | 0 | 0 | 0 |
| 07-30 | 0 | 0 | 0 |
| 07-31 | 0 | 2 | 0 |
| 08-01 | 0 | 0 | 0 |
| 08-02 | 0 | 0 | 0 |
| 08-03 | 0 | 0 | 0 |
| 08-04 | 0 | 1 | 0 |
| 08-05 | 0 | 0 | 0 |
| 08-06 | 0 | 0 | 0 |
| 08-07 | 0 | 1 | 0 |
| 08-08 | 1 | 1 | 0 |
| 08-09 | 0 | 0 | 0 |
| 08-10 | 0 | 0 | 0 |
| 08-11 | 0 | 0 | 0 |
| 08-12 | 0 | 0 | 0 |
| **14 days** | **1** | **5** | **0** |
- Waitlist:    5 total, newest 4 days ago
- Submissions: 0 total, newest never
- Accounts:    3 total, newest 4 days ago

**The funnel, as rates**
- Seen to clicked: 2.4% (91 of 3776) vs 2.2% the fortnight before
- Pages per visit: 1.5 (196 visits, 289 pageviews since 2026-08-08)
- Visits that did something: 0.0% (0 actions on 196 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-02 | 7 | 299 | 2.3% | 15.5 |
| 08-03 | 2 | 260 | 0.8% | 12.7 |
| 08-04 | 8 | 254 | 3.1% | 11.1 |
| 08-05 | 0 | 280 | 0.0% | 14.1 |
| 08-06 | 7 | 215 | 3.3% | 13.4 |
| 08-07 | 5 | 226 | 2.2% | 9.7 |
| 08-08 | 7 | 194 | 3.6% | 10.0 |
| 08-09 | 6 | 305 | 2.0% | 11.8 |
| 08-10 | 16 | 394 | 4.1% | 13.5 |
| 08-11 | 8 | 369 | 2.2% | 11.6 |
| **window** | **66** | **2796** | **2.4%** | |
- Top queries (10d): oldest tree in lisbon (i3, p10); "oldest of its species" ginkgo park (i2, p6); 1800 trees (i1, p19); 400 year old tree (i1, p18); a tree in naples (i3, p9)
- Top pages (10d): / (c4/i30); /app (c4/i14); /prague (c4/i64); /kyoto (c3/i46); /porto (c3/i25)
- Content lead: '1800 trees' has no matching page (i1, p19)
- Seen, not clicked: /rome (c0/i57, 0.0%) for trees in rome (i14, p27); rome tree (i9, p54); trees of rome (i5, p20)
- Seen, not clicked: /malaga (c0/i20, 0.0%) for árboles históricos de málaga (i19, p74); malaga tree (i1, p4)

**Who they are**
Audience, 28 days of search (109 clicks, 4745 impressions):
- Countries: usa c18/i1016; deu c10/i197; gbr c10/i587; nld c8/i246; prt c7/i129
- Devices: MOBILE c74/i2638; DESKTOP c35/i2064; TABLET c0/i43
- Landing pages: /lisbon c8/i165; / c6/i57; /porto c5/i36; /prague c5/i99; /vienna c5/i102

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-04 | 10 | 20 |
| 08-05 | 20 | 20 |
| 08-06 | 0 | 10 |
| 08-07 | 30 | 30 |
| 08-08 | 70 | 120 |
| 08-09 | 10 | 20 |
| 08-10 | 150 | 170 |
| 08-11 | 40 | 50 |
| **window** | **330** | **440** |
- Top paths: /app (50); /porto (50); / (30); /boston (20); /prague (20)
- Referrers: (direct) (230); ancienttrees.app (110); www.google.com (90); zscaler-blocked.dpgmedia.net (10)
- Countries: NL (140); US (90); DE (70); PT (50); CH (20)
- Devices: desktop (330); mobile (110)
- Page load (8d): p50 885ms, p90 7177ms

Links: external referrers (a link somebody actually clicked): zscaler-blocked.dpgmedia.net (10)

Machine: 7 chain attempts yesterday, 4 got real work time (~40 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 8 clicks and 369 impressions on Google's freshest day (day before: c16/i394). Directional at best; no strategic conclusions from these volumes.

## 2026-08-10 (previous UTC day)

**Today: nothing here needs you.** The blocks below are the standing picture.

**Did the product happen**
- app-cta:     0 yesterday, last never
- collect:     0 yesterday, last never
- directions:  0 yesterday, last never
- share:       0 yesterday, last never
- smoke-test:  0 yesterday, last 10 days ago
- walk-start:  0 yesterday, last never

| Day | Accounts | Waitlist | Submissions |
|---|---:|---:|---:|
| 07-28 | 2 | 0 | 0 |
| 07-29 | 0 | 0 | 0 |
| 07-30 | 0 | 0 | 0 |
| 07-31 | 0 | 2 | 0 |
| 08-01 | 0 | 0 | 0 |
| 08-02 | 0 | 0 | 0 |
| 08-03 | 0 | 0 | 0 |
| 08-04 | 0 | 1 | 0 |
| 08-05 | 0 | 0 | 0 |
| 08-06 | 0 | 0 | 0 |
| 08-07 | 0 | 1 | 0 |
| 08-08 | 1 | 1 | 0 |
| 08-09 | 0 | 0 | 0 |
| 08-10 | 0 | 0 | 0 |
| 08-11 | 0 | 0 | 0 |
| **14 days** | **3** | **5** | **0** |
- Waitlist:    5 total, newest 3 days ago
- Submissions: 0 total, newest never
- Accounts:    3 total, newest 3 days ago

**The funnel, as rates**
- Seen to clicked: 2.4% (86 of 3526) vs 1.9% the fortnight before
- Pages per visit: 1.5 (155 visits, 227 pageviews since 2026-08-08)
- Visits that did something: 0.0% (0 actions on 155 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 08-01 | 7 | 253 | 2.8% | 15.1 |
| 08-02 | 7 | 299 | 2.3% | 15.5 |
| 08-03 | 2 | 260 | 0.8% | 12.7 |
| 08-04 | 8 | 254 | 3.1% | 11.1 |
| 08-05 | 0 | 280 | 0.0% | 14.1 |
| 08-06 | 7 | 215 | 3.3% | 13.4 |
| 08-07 | 5 | 226 | 2.2% | 9.7 |
| 08-08 | 7 | 194 | 3.6% | 10.0 |
| 08-09 | 6 | 305 | 2.0% | 11.8 |
| 08-10 | 14 | 315 | 4.4% | 12.5 |
| **window** | **63** | **2601** | **2.4%** | |
- Top queries (10d): oldest tree in lisbon (i3, p10); "oldest of its species" ginkgo park (i2, p6); 1800 trees (i1, p19); 400 year old tree (i1, p18); amsterdam tree (i3, p17)
- Top pages (10d): / (c4/i28); /prague (c4/i56); /app (c3/i13); /kyoto (c3/i46); /porto (c3/i26)
- Content lead: '1800 trees' has no matching page (i1, p19)
- Seen, not clicked: /rome (c0/i52, 0.0%) for trees in rome (i14, p27); rome tree (i6, p50); trees of rome (i5, p20)
- Seen, not clicked: /malaga (c0/i24, 0.0%) for árboles históricos de málaga (i20, p74); malaga tree (i2, p6); malaga trees (i1, p8)

**Who they are**
Audience, 28 days of search (99 clicks, 4298 impressions):
- Countries: usa c17/i927; deu c9/i187; gbr c9/i522; nld c8/i205; prt c7/i123
- Devices: MOBILE c69/i2386; DESKTOP c30/i1869; TABLET c0/i43
- Landing pages: /lisbon c8/i157; / c6/i55; /porto c5/i36; /prague c4/i86; /vienna c4/i88

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-03 | 10 | 10 |
| 08-04 | 10 | 20 |
| 08-05 | 20 | 20 |
| 08-06 | 0 | 10 |
| 08-07 | 30 | 30 |
| 08-08 | 70 | 120 |
| 08-09 | 10 | 20 |
| 08-10 | 150 | 170 |
| **window** | **300** | **400** |
- Top paths: /app (50); /porto (50); / (30); /explore (20); /prague (20)
- Referrers: (direct) (200); ancienttrees.app (100); www.google.com (90); zscaler-blocked.dpgmedia.net (10)
- Countries: NL (120); US (80); DE (70); PT (40); CH (20)
- Devices: desktop (310); mobile (90)
- Page load (8d): p50 658ms, p90 8737ms

Links: external referrers (a link somebody actually clicked): zscaler-blocked.dpgmedia.net (10)

Machine: 10 chain attempts yesterday, 8 got real work time (~171 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 14 clicks and 315 impressions on Google's freshest day (day before: c6/i305). Directional at best; no strategic conclusions from these volumes.

## Weekly analysis 2026-08-10

Third weekly analysis, covering 2026-08-03 to 2026-08-09 against the prior
week (2026-07-27 to 2026-08-02), using the latest-settled Search Console
figure for each date (GSC revises up for 2-3 days after the "freshest day"
reading, so same-day numbers understate).

**Scorecard**

| Week ending | Impressions | Clicks | CTR | Visits (beacon) | Pageviews (beacon) | Directions/visit | App-CTA | Waitlist total | Submissions total |
|---|---|---|---|---|---|---|---|---|---|
| 2026-07-31 | 1,150 | 31 | 2.7% | 70 | 170 | n/a (not captured) | n/a (not captured) | 0 real (2 test rows) | 0 real (1 test row) |
| 2026-08-07 | 1,762 | 36 | 2.0% | 100 | 170 | n/a (not captured) | n/a (not captured) | 4 real | 0 real (1 test row) |
| 2026-08-09 | 1,680 | 35 | 2.1% | 150 | 230 | n/a (not captured) | n/a (not captured) | 5 real | 0 real |

**What moved:**
1. Impressions held flat week over week (1,682 to 1,680, settled 7-day
   totals) but clicks slipped again (45 to 35), pulling CTR from 2.7% to
   2.1%: this is the second straight week CTR has fallen while impressions
   stayed level or grew, the opposite of what ranking gains should produce.
2. Beacon visits rose 67% (90 to 150), almost entirely on one day
   (08-08: 70 visits/120 pageviews, the week's biggest by far), while
   total pageviews stayed flat (230 to 230): pages-per-visit nearly halved,
   2.6 to 1.5, so more people arrived and each looked at less.
3. Waitlist grew 2 to 5 (+3 real signups this week) and 3 real accounts
   now exist (first tracked in the 08-09 digest, all recent); both are
   small but repeated, non-test growth, which is the demand condition
   GO_TO_MARKET.md's Phase 1 trigger names.
4. /rome and /malaga's 0.0% CTR pattern (flagged in last week's analysis)
   continued all week on real volume (Rome c0/i50-77/day, Malaga
   c0/i21-25/day), until Wednesday, when Malaga got a direct fix: a
   dedicated Spanish-language page (/es/malaga) targeting the exact query
   it was failing on. Rome's equivalent diagnostic, suggested last week,
   is still not logged as done.
5. Distribution became the site's explicit strategic lens this week
   (CLAUDE.md's "Reason from distribution first," added 2026-08-09):
   twelve outreach emails went out to Portuguese organisations, the
   project's first ever, alongside real SEO-basics fixes (a proper
   favicon, og:site_name, og:image on non-tree pages, deferred MapLibre
   loading) diagnosed from Search Console's own crawl-coverage data.

**Suggestions, ranked:**
1. **[run]** Do for Rome what was just done for Malaga. Rome has taken
   0 clicks on 50-77 daily impressions for "trees in rome" (~pos 17-20)
   every day this week, the same shape Malaga had before Wednesday's
   /es/malaga fix. Last week's analysis already suggested checking P2
   (answer-first) and title/meta wording against the query; nothing in
   LOG.md this week shows that check happened. Rome is the site's
   deepest page (24 trees) earning zero conversion, the largest
   un-actioned signal on the site two weeks running.
2. **[sessie]** Wire directions-click and app-cta events into the daily
   digest. Third consecutive weekly analysis raising this (08-02, 08-08,
   now): both columns have read "n/a" or "none recorded" every single day
   since tracking began. GO_TO_MARKET.md's Phase 1 test is explicitly
   "does anyone click the walking route or the check-in" and that
   question currently cannot be answered from any data this project
   collects.
3. **[run]** Diagnose the 08-08 traffic spike (70 visits/120 pageviews,
   the week's outlier by 2-7x) rather than let it pass as noise: check
   Cloudflare's referrer/landing-page breakdown for that specific day
   against what shipped that day (the SEO fixes, or something else).
   Pages-per-visit nearly halved this week; knowing whether the spike
   was one-time or a new baseline changes how that number should read.
4. **[run]** Track "árboles históricos de málaga" position weekly from
   here, since blueprint v1.10 Contract J ties /es/malaga's fate to it
   directly: move within four weeks of indexing and the experiment opens
   more Spanish pages, stay flat and it does not. This week's baseline,
   pre-launch: position 70+, 0 clicks on the English /malaga page.
5. **[FOR HIDDE]** Waitlist and accounts both show small real growth
   again this week (waitlist 2 to 5, accounts 0 to 3), arriving four days
   before your 2026-08-14 steady-fortnight review. Worth having in hand
   going in; no action needed from a run.

**Watch next week:** whether the favicon/og-tag/MapLibre fixes and the
Malaga ES launch move CTR or position at all, and whether the twelve
Portuguese outreach emails produce a single reply, referring domain, or
photo, the first real test of whether the new distribution lens converts
to anything measurable.

## 2026-08-09 (previous UTC day)

**Today: nothing here needs you.** The blocks below are the standing picture.

**Did the product happen**
- app-cta:     0 yesterday, last never
- collect:     0 yesterday, last never
- directions:  0 yesterday, last never
- share:       0 yesterday, last never
- smoke-test:  0 yesterday, last 9 days ago
- walk-start:  0 yesterday, last never

| Day | Accounts | Waitlist | Submissions |
|---|---:|---:|---:|
| 07-27 | 0 | 0 | 0 |
| 07-28 | 2 | 0 | 0 |
| 07-29 | 0 | 0 | 0 |
| 07-30 | 0 | 0 | 0 |
| 07-31 | 0 | 2 | 0 |
| 08-01 | 0 | 0 | 0 |
| 08-02 | 0 | 0 | 0 |
| 08-03 | 0 | 0 | 0 |
| 08-04 | 0 | 1 | 0 |
| 08-05 | 0 | 0 | 0 |
| 08-06 | 0 | 0 | 0 |
| 08-07 | 0 | 1 | 0 |
| 08-08 | 1 | 1 | 0 |
| 08-09 | 0 | 0 | 0 |
| 08-10 | 0 | 0 | 0 |
| **14 days** | **3** | **5** | **0** |
- Waitlist:    5 total, newest 2 days ago
- Submissions: 0 total, newest never
- Accounts:    3 total, newest 2 days ago

**The funnel, as rates**
- Seen to clicked: 2.4% (80 of 3362) vs 1.7% the fortnight before
- Pages per visit: 1.4 (72 visits, 104 pageviews since 2026-08-08)
- Visits that did something: 0.0% (0 actions on 72 visits)

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 07-31 | 2 | 230 | 0.9% | 16.9 |
| 08-01 | 7 | 253 | 2.8% | 15.1 |
| 08-02 | 7 | 299 | 2.3% | 15.5 |
| 08-03 | 2 | 260 | 0.8% | 12.7 |
| 08-04 | 8 | 254 | 3.1% | 11.1 |
| 08-05 | 0 | 280 | 0.0% | 14.1 |
| 08-06 | 7 | 215 | 3.3% | 13.4 |
| 08-07 | 5 | 226 | 2.2% | 9.7 |
| 08-08 | 7 | 194 | 3.6% | 10.0 |
| 08-09 | 6 | 251 | 2.4% | 11.0 |
| **window** | **51** | **2462** | **2.1%** | |
- Top queries (10d): oldest tree in lisbon (i3, p10); "york museum gardens" (i4, p4); 1800 trees (i1, p19); 400 year old tree (i1, p18); alley pond giant (i1, p28)
- Top pages (10d): / (c3/i23); /kyoto (c3/i46); /app (c2/i9); /berlin/swamp-cypress-of-charlottenburg (c2/i3); /lisbon (c2/i76)
- Content lead: '1800 trees' has no matching page (i1, p19)
- Seen, not clicked: /rome (c0/i50, 0.0%) for trees in rome (i16, p19); trees of rome (i8, p26); rome tree (i4, p50)
- Seen, not clicked: /malaga (c0/i25, 0.0%) for árboles históricos de málaga (i20, p74); malaga tree (i3, p6); malaga trees (i1, p8)

**Who they are** (full cut, Mondays)
Audience, 28 days of search (85 clicks, 3929 impressions):
- Countries: usa c14/i832; gbr c9/i471; nld c8/i179; deu c6/i175; bel c5/i104
- Devices: MOBILE c61/i2212; DESKTOP c24/i1678; TABLET c0/i39
- Landing pages: /lisbon c8/i153; / c4/i47; /porto c4/i33; /amsterdam c3/i238; /kyoto c3/i79
- Search language (top 100 named queries, crude match, most clicks are in queries Google withholds): English 57q c1/i118; unclassified 38q c0/i76; Spanish 2q c0/i4; French 1q c0/i2; Italian 1q c0/i1; Dutch 1q c0/i1
On the site since 2026-08-08 (72 visits, 104 pageviews, 1.4 pages per visit):
- Countries: NL 29; PT 27; US 13; IE 11; DE 5
- Devices: desktop 75; mobile 29
- Browsers: Chrome 61; ChromeMobile 21; MobileSafari 8; Unknown 6
- Arrived via: (direct) 55; ancienttrees.app 32; www.google.com 15; zscaler-blocked.dpgmedia.n 2
- Opened: /porto 15; /app 12; / 10; /naples 5; /amsterdam 4; /porto/tulip-tree-of-casa- 2; /lisbon 2; /porto/magnolia-of-casa-ta 2

Web Analytics (beacon, real browsers, cookieless):
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews |
|---|---:|---:|
| 08-02 | 20 | 20 |
| 08-03 | 10 | 10 |
| 08-04 | 10 | 20 |
| 08-05 | 20 | 20 |
| 08-06 | 0 | 10 |
| 08-07 | 30 | 30 |
| 08-08 | 70 | 120 |
| 08-09 | 10 | 20 |
| **window** | **170** | **250** |
- Top paths: / (40); /app (40); /porto (30); /lisbon (10); /species/oriental-plane (10)
- Referrers: (direct) (130); ancienttrees.app (80); www.google.com (40)
- Countries: NL (80); US (50); PT (30); UA (20); DE (20)
- Devices: desktop (180); mobile (70)
- Page load (8d): p50 1019ms, p90 5169ms

Links: external referrers (a link somebody actually clicked): none yet

Machine: 6 chain attempts yesterday, 5 got real work time (~221 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 6 clicks and 251 impressions on Google's freshest day (day before: c7/i194). Directional at best; no strategic conclusions from these volumes.

## 2026-08-08 (previous UTC day)

**Today: a waitlist arrived yesterday (5 total); an account was opened yesterday (3 total).**

**Did the product happen**
- app-cta:     0 yesterday, last never
- collect:     0 yesterday, last never
- directions:  0 yesterday, last never
- share:       0 yesterday, last never
- smoke-test:  0 yesterday, last 8 days ago
- walk-start:  0 yesterday, last never
- Waitlist:    5 total, newest yesterday
- Submissions: 1 total, newest 9 days ago
- Accounts:    3 total, newest yesterday

**The funnel, as rates**
- Seen to clicked: 2.2% (74 of 3311) vs 0.9% the fortnight before
- Pages per visit: 1.6 (44 visits, 72 pageviews since 2026-08-08)
- Visits that did something: 0.0% (0 actions on 44 visits)

**Where demand is going to waste**

Search Console (freshest day Google provides, data lags 2-3 days):
- 2026-08-09: 1 clicks, 5 impressions, avg position 6.6 (day before: c5/i192)
- Days: 07-30:c7/i251  07-31:c2/i230  08-01:c7/i253  08-02:c7/i299  08-03:c2/i260  08-04:c8/i254  08-05:c0/i280  08-06:c7/i215  08-07:c5/i226  08-08:c5/i192  08-09:c1/i5
- Top queries (10d): oldest tree in lisbon (i5, p11); "york museum gardens" (i4, p4); 400 year old tree (i1, p18); acient tree (i1, p40); alley pond giant (i1, p28)
- Top pages (10d): /lisbon (c4/i89); / (c3/i25); /kyoto (c3/i48); /amsterdam (c2/i133); /app (c2/i9)
- Content lead: '400 year old tree' has no matching page (i1, p18)
- Seen, not clicked: /rome (c0/i61, 0.0%) for trees in rome (i18, p18); trees of rome (i8, p26); rome trees (i8, p36)
- Seen, not clicked: /malaga (c0/i24, 0.0%) for árboles históricos de málaga (i19, p73); malaga tree (i3, p8); malaga trees (i1, p8)

**Who they are**
Audience, 28 days of search (78 clicks, 3681 impressions):
- Countries: usa c14/i790; gbr c7/i437; nld c7/i162; bel c5/i95; can c5/i92
- Devices: MOBILE c56/i2050; DESKTOP c22/i1597; TABLET c0/i34
- Landing pages: /lisbon c8/i150; / c4/i47; /porto c4/i29; /amsterdam c3/i227; /kyoto c3/i76

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

Machine: 9 chain attempts yesterday, 9 got real work time (~152 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 1 clicks and 5 impressions on Google's freshest day (day before: c5/i192). Directional at best; no strategic conclusions from these volumes.

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
