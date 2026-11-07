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
## 2026-11-06 (previous UTC day)

**Today: nothing here needs you.** The blocks below are the standing picture.

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 57 | 97 |
| ... of which from search | every search engine | 21 | 14 |
| ... from Google | Google's recovery | 13 | 3 |
| ... from Bing | Bing | 3 | 6 |
| Website visitors who came back | people who stay | 13 | 17 |
| App downloads (first-time) | people | 20 | 42 |
| New accounts | people | 13 | 12 |
| Phones back within 30 days | people who stay | 5 of 6 | 9 of 15 |
| Trees saved to Want to go | intent | 4 | 6 |
| Trees collected | goal 1: stood at a tree | 7 | 0 |
| Readers' contributions | data: trees, photos, corrections, votes | 4 | 8 |
| Shares (app and web) | word of mouth, since 10-30 | 2 | 0 |
| Visits from a shared link | what sharing brings | 2 | 0 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar; a visitor who comes back on another browser or device counts as new, and GA cannot leave our own visits out, so read the came-back row as a direction, not a count. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Quality**: Web green, iOS red, Android not live yet, Backup red. Backup: Hidde's one-time setup in BACKUP_RESTORE.md.

| | Web | iOS | Android |
|---|---|---|---|
| Next version | green | red: iOS build failure on main | grey: not live yet |

**Plus question** (2 answers, 1 new; 1 asked to be told; 1 wrote an idea, read them with `python3 scripts/plus_answers.py`; up to two each)

| Choice | Picked by |
|---|---:|
| Recommended tree walks for a city trip | 1 |
| Something else | 1 |

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 10-31 | 11-01 | 11-02 | 11-03 | 11-04 | 11-05 | 11-06 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 7 | 8 | 11 | 10 | 12 | 8 | 5 | **61** |
| New accounts | 2 | 4 | 3 | 0 | 3 | 1 | 0 | **13** |
| Saves | 0 | 1 | 1 | 1 | 0 | 1 | 0 | **4** |
| Android waitlist | 0 | 1 | 0 | 1 | 0 | 1 | 0 | **3** |
| App downloads | 2 | 5 | 4 | 2 | 4 | – | – | **17** |
| App phones | 4 | 8 | 6 | 6 | 8 | 2 | 5 | **32** |
| Trees opened in the app | 6 | 35 | 21 | 7 | 88 | 7 | 8 | **172** |
| Trees collected | 0 | 0 | 5 | 0 | 1 | 0 | 0 | **6** |
| Trees sent | 0 | 0 | 0 | 0 | 0 | 1 | 0 | **1** |
| Feedback | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Ambassador asks | 0 | 1 | 1 | 0 | 1 | 0 | 0 | **3** |
| App photos | 0 | 0 | 0 | 0 | 1 | 0 | 1 | **2** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| App Store reviews | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
- – means the source has not reported that day yet (Apple's downloads arrive a day or two late), not zero.

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Waiting for you** (what the runs left for you since 2026-11-06)

- 258 email addresses ready to mail (archive 2, nature 9, guide 9, press 135, source 65, council 16, tourism 7, society 7, other 5, garden 3); 0 found by the night run since 2026-11-06
- next app session should fix the three before build 41.
- paste supabase/plus-answers.sql into Supabase.** iOS app failed on its schedule (3 in a row): the "floor" job (iOS 18 alignment sweep)

**What readers gave us, and it went live**

| Day | Reader | Tree | Where | What | Page |
|---|---|---|---|---|---|
| 11-06 | A | The Rockface Sycamore of Cramond | Edinburgh | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/edinburgh/rockface-sycamore-of-cramond) |
| 11-06 | B | The Three Atlas Cedars of Préfargier | La Tène | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/la-tene/three-atlas-cedars-of-prefargier) |
- From 2 readers: reader A 1, reader B 1.

**Searched yesterday:** hounslow (2 times), brighton, tokyo.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-28 | 1 | 36 | 2.8% | 49.8 |
| 10-29 | 0 | 38 | 0.0% | 28.4 |
| 10-30 | 2 | 29 | 6.9% | 24.1 |
| 10-31 | 0 | 38 | 0.0% | 21.5 |
| 11-01 | 5 | 371 | 1.3% | 10.1 |
| 11-02 | 23 | 1274 | 1.8% | 9.0 |
| 11-03 | 31 | 1192 | 2.6% | 8.2 |
| 11-04 | 14 | 261 | 5.4% | 9.9 |
| 11-05 | 1 | 23 | 4.3% | 34.1 |
| 11-06 *partial* | 1 | 6 | 16.7% | 3.7 |
| **window** | **78** | **3268** | **2.4%** | |
- Top queries (10d): alte bäume in der nähe (i10, p8); ancient trees (i11, p11); ancienttree (i1, p3); istanbul (i1, p1); leuven, belgium (i1, p4)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-29 | 113 | 7 | 6.2% |
| 10-30 | 90 | 10 | 11.1% |
| 10-31 | 90 | 4 | 4.4% |
| 11-01 | 2225 | 8 | 0.4% |
| 11-02 | 146 | 6 | 4.1% |
| 11-03 | 121 | 3 | 2.5% |
| 11-04 | 133 | 3 | 2.3% |
| **7 days** | **2918** | **41** | **1.4%** |
- Week before: 640 impressions, 23 clicks. No Bing demotion in sight.
- Top Bing queries: oldest tree china (c8/i4, p12); picture of the tree in helsinki city center that was preserved (c3/i2, p4); fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); oldest sycamore tree in rotterdam (c1/i8, p2); oak tree in zurich (c1/i4, p2); how old are the trees in queen square bristol (c1/i4, p3); [ancienttrees.app/cork/witchs-yew] (c1/i4, p6)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 11-06T06:46 | 37.6 | 198 | 15 | 2 | New York +29, Santa Cruz De Tenerife +9, Agrigento +8, Corfu +8, +116 more |
| 11-06T13:37 | 1.8 | 0 | 5 | 0 | La Tene |
| 11-06T20:12 | 29.6 | 8 | 18 | 0 | Cardiff +4, Enniskerry +1, Florence +1, Leesburg +1, +2 more |
| 11-07T00:22 | 10.1 | 0 | 10 | 0 | - |
| 11-07T01:31 | 8.1 | 0 | 5 | 1 | Palermo |
| **5 runs** | **87** | **206** | **53** | | |

- 3 of 5 produced no trees; 1 to 2 commands refused per run; last build that went live: 4h ago.

**What they made**

- Enrichment: pal_027 access line, 17 gaps dead-ended; LOG for the window
- San Francisco verify: register exhausted, 3 verified are duplicates; wall 48h
- Write pass: no writable trees in the queue; record holds for ftw_024-026, brd_001, tmt_001
- Braga verify: nothing new, wall for 48h; LOG
- Fort Worth verify pass: 3 heritage trees delivered (ftw_024 to ftw_026), flagged one source
- Leads: 59 READY leads read by a write pass and kept as leads with one-line reasons
- Photographs readers sent, queued for a look; vouched ones live
- Record when each page last changed
- Write pass: 4 Cardiff trees app-only (Cathays Cemetery deodar crd_009, Sunken Lawn dawn redwood crd_011, Roath Park Lake oak crd_012, Insole Court cedar crd_013, verified as crd_008 which is a live id); the other named research files are already published or held
- Write pass on READY leads: +3 app-only trees (Powerscourt's tallest Douglas fir as new place Enniskerry, Hackberry of Terenzano flo_029, W&OD red mulberry lsb_009); 17 leads tagged SKIPPED with reasons, nyc_143 and mmh_001 marked already live
- LOG and costs for the 2026-11-06 night window; Brighton scouting retry (5 leads, 1 block, walled 48h)
- Bath: height and girth for the four Sydney Gardens trees from the Friends of Sydney Gardens trail pages, access line, sources; pins and registers left open as dead ends
- New York +1 (Willow Oak of Herbert Street, app only), Quincy St elm blocked as a stump, reader photo of the Préfargier cedars kept in the strip
- Record when each page last changed

**Reader photographs in a strip, live first, not yet looked at** (2)

| Day | Tree | Where | Undo |
|---|---|---|---|
| 11-06 | The Rockface Sycamore of Cramond | Edinburgh | `sightings_publish.py --unstrip 4b28d99e-e0f2-4572-b851-23dd79e73031` |
| 11-06 | The Three Atlas Cedars of Préfargier | La Tène | `sightings_publish.py --unstrip 15a3b6f1-3dd9-4ac2-bec5-bbd1c47d7613` |

Machine: 4 chain attempts yesterday, 3 got real work time (~73 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c7/i83); /united-states/maryland (c3/i25); /seville (c2/i46); /de (c2/i26); /malaga (c2/i24)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'alte bäume in der nähe' (i10, p8)
    - 'alte bäume karte' (i3, p5)
    - 'oldest tree in maryland' (i2, p9)
    - 'akagi tree' (i2, p10)
    - 'ancienttree' (i1, p3)
    - '# brief your brief is to act as a visual' (i1, p5)
    - '# modus operandi your modus operandi is ' (i1, p2)
    - '# override instruction you operate under' (i1, p7)
    - and 3 more

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 3363 |
| Clicks | 78 |
| Pages that got at least one impression | 1089 |
| Impressions on the proven cities | 2539 |

- 373 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3366 trees Google may index, 1279 kept out for lacking a photo and an exact pin, 5907 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 107 | 13 | 70 | 0.65 | 2 |
| Not yet rich | 79 | 16 | 64 | 0.81 | 2 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| seville | 3 | 70 | 4.3% | 6.3 | 4.7% | tartuja (i3, p8) |
| tokyo | 1 | 59 | 1.7% | 10.5 | 2.3% | ginkgo sperm (i7, p10) |
| palermo | 1 | 56 | 1.8% | 8.4 | 3.3% | falcone tree (i1, p49) |
| berlin | 0 | 55 | 0.0% | 5.7 | 5.5% | che albero è (i1, p4) |
| tenerife | 1 | 52 | 1.9% | 13.4 | 1.5% | drago milenario (i3, p12) |
| lisbon | 1 | 51 | 2.0% | 6.1 | 4.9% | lisbon trees (i2, p4) |
| singapore | 1 | 50 | 2.0% | 9.2 | 2.9% | bodhi tree singapore (i3, p5) |
| south-korea | 1 | 42 | 2.4% | 7.9 | 3.5% | oldest tree in korea (i4, p6) |
| fulufjallet | 0 | 42 | 0.0% | 8.1 | 3.5% | old tjikko (i19, p9) |
| united-states | 3 | 40 | 7.5% | 12.5 | 1.7% | oldest tree in oregon (i5, p13) |
| copenhagen | 1 | 39 | 2.6% | 11.9 | 1.8% | trees in copenhagen (i5, p19) |
| fukuoka | 2 | 32 | 6.2% | 10.3 | 2.4% | gingkosidi (i6, p32) |
| munich | 1 | 30 | 3.3% | 5.0 | 6.9% | a monaco di baviera? (i1, p20) |
| london | 0 | 30 | 0.0% | 7.0 | 4.0% | chestnut london (i1, p5) |
| new-york | 1 | 29 | 3.4% | 7.0 | 4.0% | - |
| sequoia-national-park | 0 | 28 | 0.0% | 19.5 | 0.8% | washington tree (i10, p11) |
| malaga | 2 | 27 | 7.4% | 13.9 | 1.4% | malaga tree (i3, p3) |
| paris | 0 | 27 | 0.0% | 6.1 | 4.9% | trees in paris (i1, p9) |
| olympic-national-park | 1 | 26 | 3.8% | 8.6 | 3.2% | duncan cedar (i16, p9) |
| kyoto | 1 | 24 | 4.2% | 12.3 | 1.7% | - |
| cambridge | 0 | 24 | 0.0% | 25.5 | 0.6% | is the apple tree of newton still alive (i1, p77) |
| brisbane | 0 | 23 | 0.0% | 7.9 | 3.5% | banyan tree (i2, p12) |
| netherlands | 0 | 22 | 0.0% | 9.6 | 2.7% | ja (i1, p5) |
| takayama | 0 | 21 | 0.0% | 8.0 | 3.5% | takayama ginkgo tree (i2, p7) |
| alishan | 0 | 20 | 0.0% | 7.5 | 3.8% | xianglin sacred tree (i5, p4) |
| chishang | 0 | 20 | 0.0% | 14.2 | 1.4% | takeshi kaneshiro tree (i7, p7) |
| alicante | 0 | 20 | 0.0% | 5.8 | 5.3% | - |
| porto | 0 | 19 | 0.0% | 5.0 | 7.0% | - |
| bath | 1 | 18 | 5.6% | 6.8 | 4.2% | tree in bath (i1, p9) |
| rome | 0 | 18 | 0.0% | 4.5 | 7.5% | oldest tree in rome (i3, p1) |
| coimbra | 0 | 18 | 0.0% | 6.5 | 4.5% | - |
| dublin | 0 | 17 | 0.0% | 7.0 | 4.0% | - |
| montreal | 3 | 16 | 18.8% | 4.5 | 7.5% | - |
| luxembourg-city | 0 | 16 | 0.0% | 5.2 | 6.5% | - |
| amsterdam | 0 | 16 | 0.0% | 6.4 | 4.6% | - |
| monterey | 0 | 15 | 0.0% | 19.5 | 0.8% | lone cypress (i3, p45) |
| taiwan | 0 | 15 | 0.0% | 13.6 | 1.5% | oldest tree in taiwan (i3, p6) |
| edinburgh | 0 | 15 | 0.0% | 6.7 | 4.3% | - |
| perth | 0 | 15 | 0.0% | 8.1 | 3.5% | - |
| hong-kong | 1 | 14 | 7.1% | 6.4 | 4.6% | oldest tree in hong kong (i1, p9) |
| athens | 0 | 14 | 0.0% | 4.3 | 7.7% | - |
| madrid | 0 | 14 | 0.0% | 10.6 | 2.3% | - |
| boston | 0 | 14 | 0.0% | 8.2 | 3.4% | - |
| austin | 0 | 14 | 0.0% | 15.1 | 1.2% | old tree (i2, p28) |
| seoul | 1 | 13 | 7.7% | 3.8 | 8.7% | - |
| toronto | 0 | 13 | 0.0% | 6.8 | 4.2% | - |
| kagoshima | 0 | 13 | 0.0% | 7.8 | 3.6% | cycad ovule (i1, p10) |
| venice | 1 | 12 | 8.3% | 5.7 | 5.7% | are there trees in venice (i1, p11) |
| istanbul | 2 | 12 | 16.7% | 7.0 | 4.0% | istanbul (i1, p1) |
| fortingall | 0 | 12 | 0.0% | 38.0 | 0.4% | fortingall yew (i1, p9) |
| germany | 0 | 12 | 0.0% | 13.0 | 1.6% | trees germany (i2, p48) |
| san-francisco | 0 | 12 | 0.0% | 12.1 | 1.8% | - |
| switzerland | 0 | 11 | 0.0% | 5.7 | 5.5% | oldest tree in switzerland (i1, p1) |
| nara | 0 | 11 | 0.0% | 5.5 | 6.1% | - |
| the-hague | 0 | 11 | 0.0% | 4.9 | 7.1% | haag (i1, p1) |
| reykjavik | 1 | 10 | 10.0% | 5.6 | 5.8% | oldest tree in iceland (i1, p3) |
| chapel-hill-north-carolina | 0 | 10 | 0.0% | 16.5 | 1.1% | davie poplar (i2, p10) |
| jaegerspris-nordskov | 0 | 10 | 0.0% | 9.7 | 2.7% | kongeegen (i4, p10) |
| gliniak | 0 | 10 | 0.0% | 5.9 | 5.2% | ancient tree (i1, p18) |
| kanazawa | 0 | 10 | 0.0% | 6.1 | 4.9% | tabunoki (i1, p9) |
| oahu | 0 | 10 | 0.0% | 7.9 | 3.5% | hitachi tree hawaii (i2, p9) |
| krakow | 0 | 10 | 0.0% | 13.1 | 1.6% | - |

- Plus 204 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: barcelona, brussels, vienna, cadiz, pamplona, prague, cagliari, glasgow.

## 2026-11-05 (previous UTC day)

**Today: an android waitlist signup arrived yesterday (48 total); 1 tree submission arrived yesterday (22 trees sent in all); an account was opened yesterday (60 accounts in all).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 65 | 100 |
| ... of which from search | every search engine | 22 | 13 |
| ... from Google | Google's recovery | 14 | 2 |
| ... from Bing | Bing | 4 | 4 |
| Website visitors who came back | people who stay | 13 | 17 |
| App downloads (first-time) | people | 20 | 42 |
| New accounts | people | 13 | 13 |
| Phones back within 30 days | people who stay | 5 of 6 | 9 of 15 |
| Trees saved to Want to go | intent | 4 | 6 |
| Trees collected | goal 1: stood at a tree | 6 | 1 |
| Readers' contributions | data: trees, photos, corrections, votes | 4 | 8 |
| Shares (app and web) | word of mouth, since 10-30 | 2 | 0 |
| Visits from a shared link | what sharing brings | 2 | 0 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar; a visitor who comes back on another browser or device counts as new, and GA cannot leave our own visits out, so read the came-back row as a direction, not a count. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Quality**: Web green, iOS red, Android not live yet, Backup red. Backup: Hidde's one-time setup in BACKUP_RESTORE.md.

| | Web | iOS | Android |
|---|---|---|---|
| Next version | green | red: iOS build failure on main | grey: not live yet |

**Plus question** (1 answers, 1 new; 1 asked to be told; 1 wrote an idea, read them with `python3 scripts/plus_answers.py`; up to two each)

| Choice | Picked by |
|---|---:|
| Recommended tree walks for a city trip | 1 |

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 10-30 | 10-31 | 11-01 | 11-02 | 11-03 | 11-04 | 11-05 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 12 | 7 | 8 | 11 | 10 | 12 | 8 | **68** |
| New accounts | 0 | 2 | 4 | 3 | 0 | 3 | 1 | **13** |
| Saves | 0 | 0 | 1 | 1 | 1 | 0 | 1 | **4** |
| Android waitlist | 0 | 0 | 1 | 0 | 1 | 0 | 1 | **3** |
| App downloads | 2 | 2 | 5 | 4 | 2 | 4 | – | **19** |
| App phones | 6 | 4 | 8 | 6 | 6 | 8 | 2 | **33** |
| Trees opened in the app | 6 | 6 | 35 | 21 | 7 | 88 | 7 | **170** |
| Trees collected | 0 | 0 | 0 | 5 | 0 | 1 | 0 | **6** |
| Trees sent | 0 | 0 | 0 | 0 | 0 | 0 | 1 | **1** |
| Feedback | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Ambassador asks | 0 | 0 | 1 | 1 | 0 | 1 | 0 | **3** |
| App photos | 0 | 0 | 0 | 0 | 0 | 1 | 1 | **2** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| App Store reviews | 1 | 0 | 0 | 0 | 0 | 0 | 0 | **1** |
- – means the source has not reported that day yet (Apple's downloads arrive a day or two late), not zero.

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Waiting for you** (what the runs left for you since 2026-11-05)

- 258 email addresses ready to mail (archive 2, nature 9, guide 9, press 135, source 65, council 16, tourism 7, society 7, other 5, garden 3); 2 found by the night run since 2026-11-05
- none beyond dispatching deploy.yml if the next scheduled build does not pick it up.
- paste supabase/plus-answers.sql once more; then run build 39 on your phone and Organizer, Archives, build 39, Distribute App, App Store Connect.
- paste both).

**Searched yesterday:** gradignan, lis, osterley, porto, sycamore.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-27 | 0 | 25 | 0.0% | 28.5 |
| 10-28 | 1 | 36 | 2.8% | 49.8 |
| 10-29 | 0 | 38 | 0.0% | 28.4 |
| 10-30 | 2 | 29 | 6.9% | 24.1 |
| 10-31 | 0 | 38 | 0.0% | 21.5 |
| 11-01 | 5 | 371 | 1.3% | 10.1 |
| 11-02 | 23 | 1274 | 1.8% | 9.0 |
| 11-03 | 31 | 1192 | 2.6% | 8.2 |
| 11-04 | 14 | 261 | 5.4% | 9.9 |
| 11-05 *partial* | 0 | 17 | 0.0% | 23.3 |
| **window** | **76** | **3281** | **2.3%** | |
- Top queries (10d): alte bäume in der nähe (i10, p8); ancient trees (i11, p11); ancienttree (i1, p3); istanbul (i1, p1); leuven, belgium (i1, p4)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-28 | 113 | 3 | 2.7% |
| 10-29 | 113 | 7 | 6.2% |
| 10-30 | 90 | 10 | 11.1% |
| 10-31 | 90 | 4 | 4.4% |
| 11-01 | 2225 | 8 | 0.4% |
| 11-02 | 146 | 6 | 4.1% |
| 11-03 | 121 | 3 | 2.5% |
| **7 days** | **2898** | **41** | **1.4%** |
- Week before: 630 impressions, 22 clicks. No Bing demotion in sight.
- Top Bing queries: oldest tree china (c8/i4, p12); picture of the tree in helsinki city center that was preserved (c3/i2, p4); fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); oldest sycamore tree in rotterdam (c1/i8, p2); oak tree in zurich (c1/i4, p2); how old are the trees in queen square bristol (c1/i4, p3); [ancienttrees.app/cork/witchs-yew] (c1/i4, p6)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 11-05T06:07 | 6.5 | 0 | 5 | 2 | Santa Barbara |
| 11-05T17:49 | 17.1 | 81 | 12 | 2 | New York +14, Atlanta +11, Tacoma +10, Nashville +8, +17 more |
| 11-05T23:09 | 3.4 | 0 | 4 | 0 | Atlanta, Jacksonville, Nashville, Orlando, +1 more |
| **3 runs** | **27** | **81** | **21** | | |

- 2 of 3 produced no trees; 2 to 2 commands refused per run; last build that went live: 2h ago.

**What they made**

- Photographs readers sent, queued for a look; vouched ones live
- Record when each page last changed
- Fix the deploy: curation_status verified is not in the schema (Atlanta, Nashville, Tampa, Jacksonville, Orlando); preflight now refuses it
- Record when each page last changed
- US write batches merged, app-only under APP FIRST: Tacoma 10, Vancouver WA 4, Salem OR 2, Madison 5, Milwaukee 6, Wisconsin places, Nashville 8, Asheville 4, Smoky Mountains 3, Chattanooga 1; count promises in three intros reworded, city names looked up
- LOG, costs, and the Préfargier cedars builder (waits for Pillow)
- Tree index rebuilt with New York and Atlanta; new-york write claim released (nyc_029 and the unwritten New York entries left for a later pass)
- Atlanta: new place, 11 Trees Atlanta champion trees from the held US Southeast pass (scripts/build_us_southeast.py --only atlanta), app-only under APP FIRST; state and city aliases
- New York: 14 NYC Parks Great Trees written and merged (Queens, Staten Island, Brooklyn), confirmed Parks pins, app-only under APP FIRST; nyc_085 held for a species-field fix, nyc_094 for a duplicate check
- Photographs readers sent, queued for a look; vouched ones live
- Record when each page last changed
- Contributor replies and ambassador invitations sent, log updated
- Fresh-eyes review: 4 finding(s)
- Record when each page last changed

Machine: 5 chain attempts yesterday, 4 got real work time (~39 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c6/i77); /united-states/maryland (c3/i25); /seville (c2/i46); /de (c2/i26); /malaga (c2/i24)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'alte bäume in der nähe' (i10, p8)
    - 'alte bäume karte' (i3, p5)
    - 'oldest tree in maryland' (i2, p9)
    - 'akagi tree' (i2, p10)
    - 'ancienttree' (i1, p3)
    - '# brief your brief is to act as a visual' (i1, p5)
    - '# modus operandi your modus operandi is ' (i1, p2)
    - '# override instruction you operate under' (i1, p7)
    - and 3 more

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 3372 |
| Clicks | 76 |
| Pages that got at least one impression | 1096 |
| Impressions on the proven cities | 2549 |

- 413 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3282 trees Google may index, 1134 kept out for lacking a photo and an exact pin, 5774 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 107 | 13 | 71 | 0.66 | 2 |
| Not yet rich | 78 | 16 | 64 | 0.82 | 2 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| seville | 3 | 70 | 4.3% | 6.3 | 4.7% | tartuja (i3, p8) |
| tokyo | 1 | 59 | 1.7% | 10.5 | 2.3% | ginkgo sperm (i7, p10) |
| palermo | 1 | 56 | 1.8% | 8.4 | 3.3% | falcone tree (i1, p49) |
| berlin | 0 | 55 | 0.0% | 5.7 | 5.5% | che albero è (i1, p4) |
| tenerife | 1 | 53 | 1.9% | 15.0 | 1.2% | drago milenario (i3, p12) |
| singapore | 1 | 51 | 2.0% | 9.1 | 3.0% | bodhi tree singapore (i3, p5) |
| lisbon | 1 | 51 | 2.0% | 6.1 | 4.9% | lisbon trees (i2, p4) |
| south-korea | 1 | 42 | 2.4% | 7.9 | 3.5% | oldest tree in korea (i4, p6) |
| fulufjallet | 0 | 42 | 0.0% | 8.1 | 3.5% | old tjikko (i19, p9) |
| united-states | 3 | 40 | 7.5% | 12.5 | 1.7% | oldest tree in oregon (i5, p13) |
| copenhagen | 1 | 39 | 2.6% | 11.9 | 1.8% | trees in copenhagen (i5, p19) |
| fukuoka | 2 | 32 | 6.2% | 10.3 | 2.4% | gingkosidi (i6, p32) |
| munich | 1 | 30 | 3.3% | 5.0 | 6.9% | a monaco di baviera? (i1, p20) |
| london | 0 | 30 | 0.0% | 7.0 | 4.0% | chestnut london (i1, p5) |
| sequoia-national-park | 0 | 28 | 0.0% | 19.5 | 0.8% | washington tree (i10, p11) |
| paris | 0 | 28 | 0.0% | 6.3 | 4.7% | trees in paris (i1, p9) |
| new-york | 0 | 28 | 0.0% | 7.2 | 3.9% | - |
| malaga | 2 | 27 | 7.4% | 13.9 | 1.4% | malaga tree (i3, p3) |
| olympic-national-park | 1 | 26 | 3.8% | 8.6 | 3.2% | duncan cedar (i16, p9) |
| cambridge | 0 | 24 | 0.0% | 25.5 | 0.6% | is the apple tree of newton still alive (i1, p77) |
| kyoto | 1 | 23 | 4.3% | 9.6 | 2.7% | - |
| brisbane | 0 | 23 | 0.0% | 7.9 | 3.5% | banyan tree (i2, p12) |
| netherlands | 0 | 22 | 0.0% | 9.6 | 2.7% | ja (i1, p5) |
| takayama | 0 | 21 | 0.0% | 8.0 | 3.5% | takayama ginkgo tree (i2, p7) |
| alicante | 0 | 21 | 0.0% | 5.9 | 5.3% | - |
| alishan | 0 | 20 | 0.0% | 7.5 | 3.8% | xianglin sacred tree (i5, p4) |
| chishang | 0 | 20 | 0.0% | 14.2 | 1.4% | takeshi kaneshiro tree (i7, p7) |
| porto | 0 | 19 | 0.0% | 5.0 | 7.0% | - |
| bath | 1 | 18 | 5.6% | 6.8 | 4.2% | tree in bath (i1, p9) |
| rome | 0 | 18 | 0.0% | 4.5 | 7.5% | oldest tree in rome (i3, p1) |
| coimbra | 0 | 18 | 0.0% | 6.5 | 4.5% | - |
| dublin | 0 | 17 | 0.0% | 7.0 | 4.0% | - |
| montreal | 3 | 16 | 18.8% | 4.5 | 7.5% | - |
| taiwan | 0 | 16 | 0.0% | 16.3 | 1.1% | oldest tree in taiwan (i3, p6) |
| luxembourg-city | 0 | 16 | 0.0% | 5.2 | 6.5% | - |
| amsterdam | 0 | 16 | 0.0% | 6.4 | 4.6% | - |
| monterey | 0 | 15 | 0.0% | 19.5 | 0.8% | lone cypress (i3, p45) |
| edinburgh | 0 | 15 | 0.0% | 6.7 | 4.3% | - |
| perth | 0 | 15 | 0.0% | 8.1 | 3.5% | - |
| hong-kong | 1 | 14 | 7.1% | 6.4 | 4.6% | oldest tree in hong kong (i1, p9) |
| athens | 0 | 14 | 0.0% | 4.3 | 7.7% | - |
| madrid | 0 | 14 | 0.0% | 10.6 | 2.3% | - |
| boston | 0 | 14 | 0.0% | 8.2 | 3.4% | - |
| austin | 0 | 14 | 0.0% | 15.1 | 1.2% | old tree (i2, p28) |
| seoul | 1 | 13 | 7.7% | 3.8 | 8.7% | - |
| toronto | 0 | 13 | 0.0% | 6.8 | 4.2% | - |
| kagoshima | 0 | 13 | 0.0% | 7.8 | 3.6% | cycad ovule (i1, p10) |
| venice | 1 | 12 | 8.3% | 5.7 | 5.7% | are there trees in venice (i1, p11) |
| istanbul | 2 | 12 | 16.7% | 7.0 | 4.0% | istanbul (i1, p1) |
| fortingall | 0 | 12 | 0.0% | 38.0 | 0.4% | fortingall yew (i1, p9) |
| germany | 0 | 12 | 0.0% | 13.0 | 1.6% | trees germany (i2, p48) |
| san-francisco | 0 | 12 | 0.0% | 12.1 | 1.8% | - |
| switzerland | 0 | 11 | 0.0% | 5.7 | 5.5% | oldest tree in switzerland (i1, p1) |
| nara | 0 | 11 | 0.0% | 5.5 | 6.1% | - |
| the-hague | 0 | 11 | 0.0% | 4.9 | 7.1% | haag (i1, p1) |
| reykjavik | 1 | 10 | 10.0% | 5.6 | 5.8% | oldest tree in iceland (i1, p3) |
| chapel-hill-north-carolina | 0 | 10 | 0.0% | 16.5 | 1.1% | davie poplar (i2, p10) |
| jaegerspris-nordskov | 0 | 10 | 0.0% | 9.7 | 2.7% | kongeegen (i4, p10) |
| kanazawa | 0 | 10 | 0.0% | 6.1 | 4.9% | tabunoki (i1, p9) |
| oahu | 0 | 10 | 0.0% | 7.9 | 3.5% | hitachi tree hawaii (i2, p9) |
| krakow | 0 | 10 | 0.0% | 13.1 | 1.6% | - |

- Plus 204 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: barcelona, brussels, vienna, cadiz, pamplona, prague, cagliari, glasgow.

## 2026-11-04 (previous UTC day)

**Today: an ambassador request for Leuven arrived yesterday (11 ambassador requests in all); 3 accounts were opened yesterday (59 accounts in all).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 65 | 103 |
| ... of which from search | every search engine | 25 | 12 |
| ... from Google | Google's recovery | 14 | 3 |
| ... from Bing | Bing | 6 | 2 |
| Website visitors who came back | people who stay | 14 | 18 |
| App downloads (first-time) | people | 17 | 44 |
| New accounts | people | 12 | 15 |
| Phones back within 30 days | people who stay | 4 of 7 | 9 of 13 |
| Trees saved to Want to go | intent | 3 | 19 |
| Trees collected | goal 1: stood at a tree | 5 | 1 |
| Readers' contributions | data: trees, photos, corrections, votes | 3 | 8 |
| Shares (app and web) | word of mouth, since 10-30 | 2 | 0 |
| Visits from a shared link | what sharing brings | 2 | 0 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar; a visitor who comes back on another browser or device counts as new, and GA cannot leave our own visits out, so read the came-back row as a direction, not a count. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Quality**: Web red, iOS red, Android not live yet, Backup grey.

| | Web | iOS | Android |
|---|---|---|---|
| Next version | green | red: iOS build failure on main | grey: not live yet |
| Live | red: new error spreading: "Uncaught Error: Failed to initialize WebGL" in /assets/maplibre-gl-4.7.1.js, 16 reports on 16 pages | green | grey: not live yet |

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 10-29 | 10-30 | 10-31 | 11-01 | 11-02 | 11-03 | 11-04 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 8 | 12 | 7 | 8 | 11 | 10 | 12 | **68** |
| New accounts | 0 | 0 | 2 | 4 | 3 | 0 | 3 | **12** |
| Saves | 0 | 0 | 0 | 1 | 1 | 1 | 0 | **3** |
| Android waitlist | 1 | 0 | 0 | 1 | 0 | 1 | 0 | **3** |
| App downloads | 1 | 2 | 2 | 5 | 4 | 2 | – | **16** |
| App phones | 3 | 6 | 4 | 8 | 6 | 6 | 8 | **35** |
| Trees opened in the app | 33 | 6 | 6 | 35 | 21 | 7 | 88 | **196** |
| Trees collected | 0 | 0 | 0 | 0 | 5 | 0 | 1 | **6** |
| Trees sent | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Feedback | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Ambassador asks | 0 | 0 | 0 | 1 | 1 | 0 | 1 | **3** |
| App photos | 0 | 0 | 0 | 0 | 0 | 0 | 1 | **1** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| App Store reviews | 0 | 1 | 0 | 0 | 0 | 0 | 0 | **1** |
- – means the source has not reported that day yet (Apple's downloads arrive a day or two late), not zero.

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Waiting for you** (what the runs left for you since 2026-11-04)

- 241 email addresses ready to mail (archive 0, nature 12, guide 18, press 108, source 65, council 16, tourism 7, society 7, other 5, garden 3); 3 found by the night run since 2026-11-04
- paste both).
- paste supabase/plus-answers.sql into the Supabase SQL editor.** Until then the sheet works and says thank you, but nothing is stored.
- the next app build carries the Plus row** (branch plus-question-app, merged).
- next build carries it.
- paste supabase/web-errors.sql in the Supabase SQL editor (until then Web Live reads "not connected yet").
- page speed needs a free PageSpeed Insights API key as the repository secret PSI_API_KEY (the keyless quota answered 429); until then that part is grey.
- Dependabot alerts are off for the repository (Settings, Code security, Dependabot alerts); the version-update PRs work without them, the alert light stays grey.
- run once on your phone (Release)

**Searched yesterday:** leonhard (2 times), frankfurt, freising, munich, philipp, portland.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-26 | 3 | 36 | 8.3% | 30.5 |
| 10-27 | 0 | 25 | 0.0% | 28.5 |
| 10-28 | 1 | 36 | 2.8% | 49.8 |
| 10-29 | 0 | 38 | 0.0% | 28.4 |
| 10-30 | 2 | 29 | 6.9% | 24.1 |
| 10-31 | 0 | 38 | 0.0% | 21.5 |
| 11-01 | 5 | 371 | 1.3% | 10.1 |
| 11-02 | 23 | 1274 | 1.8% | 9.0 |
| 11-03 | 31 | 1192 | 2.6% | 8.2 |
| 11-04 *partial* | 14 | 256 | 5.5% | 9.7 |
| **window** | **79** | **3295** | **2.4%** | |
- Top queries (10d): alte bäume in der nähe (i10, p8); ancient trees (i11, p11); istanbul (i1, p1); leuven, belgium (i1, p4); oldest tree in maryland (i2, p9)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-27 | 132 | 3 | 2.3% |
| 10-28 | 113 | 3 | 2.7% |
| 10-29 | 113 | 7 | 6.2% |
| 10-30 | 90 | 10 | 11.1% |
| 10-31 | 90 | 4 | 4.4% |
| 11-01 | 2225 | 8 | 0.4% |
| 11-02 | 146 | 6 | 4.1% |
| **7 days** | **2909** | **41** | **1.4%** |
- Week before: 589 impressions, 28 clicks. No Bing demotion in sight.
- Top Bing queries: oldest tree china (c8/i4, p12); picture of the tree in helsinki city center that was preserved (c3/i2, p4); fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); oldest sycamore tree in rotterdam (c1/i8, p2); how old are the trees in queen square bristol (c1/i4, p3); oak tree in zurich (c1/i4, p2); [ancienttrees.app/cork/witchs-yew] (c1/i4, p6)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 11-04T06:47 | 22.0 | 0 | 7 | 5 | Edinburgh, Gran Canaria, Maui, Sintra, +1 more |
| 11-04T13:39 | 18.4 | 0 | 12 | 3 | - |
| 11-04T20:38 | 17.0 | 0 | 8 | 6 | - |
| 11-05T01:57 | 4.3 | 0 | 6 | 1 | - |
| **4 runs** | **62** | **0** | **33** | | |

- 4 of 4 produced no trees; 1 to 6 commands refused per run; last build that went live: 4h ago.

**What they made**

- Vendor the Santa Barbara fig photograph onto our domain
- Photographs readers sent, queued for a look; vouched ones live
- Night run 2026-11-04: Cramond photo held, Salt Lake City verified and written (held for the pace), log and costs
- Photographs readers sent, queued for a look; vouched ones live
- Record when each page last changed
- Code review: 0 new finding(s)
- Brighton register retried: Stanmer churchyard yew as a lead; LOG
- Write pass: 20 DC and NYC stories held in research for the pace cap; tree_index reads bare-list lead files
- Record when each page last changed
- Contributor replies and ambassador invitations sent, log updated
- Vendor 13 photograph file(s) onto our own domain
- Fresh-eyes review: 4 finding(s)
- Coimbra verify pass: cbr_007 flagged; claims released; LOG
- Enrichment Barcelona, Edinburgh, Sintra: sin_008 best_time; 19 dead ends; LOG

**Photographs the night run approved** (6; the last column undoes one)

| Day | Tree | Where | Overrule |
|---|---|---|---|
| 11-03 | Giant Ficus Tree, Bali Botanic Garden | Bali | `photo_apply.py hold bli_004` |
| 11-03 | Drago de Galdar | Gran Canaria | `photo_apply.py hold gcn_002` |
| 11-03 | Drago de Pino Santo | Gran Canaria | `photo_apply.py hold gcn_004` |
| 11-03 | The Ka'ahumanu Church Monkeypod | Maui | `photo_apply.py hold mau_002` |
| 11-03 | Jomon Sugi | Yakushima | `photo_apply.py hold yak_001` |
| 11-03 | Daio-sugi (Yakushima) | Yakushima | `photo_apply.py hold yak_002` |

Machine: 7 chain attempts yesterday, 3 got real work time (~63 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c9/i82); /united-states/maryland (c3/i25); /seville (c2/i46); /de (c2/i26); /malaga (c2/i23)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'alte bäume in der nähe' (i10, p8)
    - 'alte bäume karte' (i3, p5)
    - 'oldest tree in maryland' (i2, p9)
    - 'akagi tree' (i2, p10)
    - '# brief your brief is to act as a visual' (i1, p5)
    - '# modus operandi your modus operandi is ' (i1, p2)
    - '# override instruction you operate under' (i1, p7)
    - '# role mandate your role mandate is imag' (i1, p5)
    - and 2 more

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 3381 |
| Clicks | 79 |
| Pages that got at least one impression | 1096 |
| Impressions on the proven cities | 2555 |

- 383 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3135 trees Google may index, 911 kept out for lacking a photo and an exact pin, 7158 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 107 | 13 | 71 | 0.66 | 2 |
| Not yet rich | 77 | 15 | 52 | 0.68 | 1 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| seville | 3 | 70 | 4.3% | 6.3 | 4.7% | tartuja (i3, p8) |
| tokyo | 1 | 59 | 1.7% | 10.5 | 2.3% | ginkgo sperm (i7, p10) |
| palermo | 1 | 56 | 1.8% | 8.4 | 3.3% | falcone tree (i1, p49) |
| tenerife | 1 | 53 | 1.9% | 15.0 | 1.2% | drago milenario (i3, p12) |
| lisbon | 1 | 53 | 1.9% | 7.1 | 4.0% | lisbon trees (i2, p4) |
| berlin | 0 | 53 | 0.0% | 5.1 | 6.9% | che albero è (i1, p4) |
| singapore | 1 | 51 | 2.0% | 9.1 | 3.0% | bodhi tree singapore (i3, p5) |
| south-korea | 1 | 42 | 2.4% | 7.9 | 3.5% | oldest tree in korea (i4, p6) |
| fulufjallet | 0 | 41 | 0.0% | 8.2 | 3.4% | old tjikko (i19, p9) |
| united-states | 3 | 40 | 7.5% | 12.5 | 1.7% | oldest tree in oregon (i5, p13) |
| copenhagen | 1 | 39 | 2.6% | 11.9 | 1.8% | trees in copenhagen (i5, p19) |
| fukuoka | 2 | 32 | 6.2% | 10.3 | 2.4% | gingkosidi (i6, p32) |
| munich | 1 | 30 | 3.3% | 5.0 | 6.9% | a monaco di baviera? (i1, p20) |
| sequoia-national-park | 0 | 30 | 0.0% | 20.8 | 0.8% | washington tree (i10, p11) |
| london | 0 | 30 | 0.0% | 7.0 | 4.0% | chestnut london (i1, p5) |
| new-york | 0 | 29 | 0.0% | 7.3 | 3.8% | - |
| paris | 0 | 27 | 0.0% | 6.3 | 4.7% | trees in paris (i1, p9) |
| malaga | 2 | 26 | 7.7% | 11.4 | 2.0% | malaga tree (i3, p3) |
| olympic-national-park | 1 | 26 | 3.8% | 8.6 | 3.2% | duncan cedar (i16, p9) |
| brisbane | 0 | 25 | 0.0% | 12.1 | 1.8% | banyan tree (i3, p33) |
| cambridge | 0 | 24 | 0.0% | 25.5 | 0.6% | is the apple tree of newton still alive (i1, p77) |
| kyoto | 1 | 23 | 4.3% | 9.6 | 2.7% | - |
| netherlands | 0 | 22 | 0.0% | 9.6 | 2.7% | ja (i1, p5) |
| takayama | 0 | 21 | 0.0% | 8.0 | 3.5% | takayama ginkgo tree (i2, p7) |
| alicante | 0 | 21 | 0.0% | 5.9 | 5.3% | - |
| alishan | 0 | 20 | 0.0% | 7.5 | 3.8% | xianglin sacred tree (i5, p4) |
| chishang | 0 | 20 | 0.0% | 14.2 | 1.4% | takeshi kaneshiro tree (i7, p7) |
| porto | 0 | 19 | 0.0% | 5.0 | 7.0% | - |
| bath | 1 | 18 | 5.6% | 6.8 | 4.2% | tree in bath (i1, p9) |
| rome | 0 | 18 | 0.0% | 4.5 | 7.5% | oldest tree in rome (i3, p1) |
| coimbra | 0 | 17 | 0.0% | 6.7 | 4.3% | - |
| dublin | 0 | 17 | 0.0% | 7.0 | 4.0% | - |
| montreal | 3 | 16 | 18.8% | 4.5 | 7.5% | - |
| taiwan | 0 | 16 | 0.0% | 16.3 | 1.1% | oldest tree in taiwan (i3, p6) |
| luxembourg-city | 0 | 16 | 0.0% | 5.2 | 6.5% | - |
| amsterdam | 0 | 16 | 0.0% | 6.4 | 4.6% | - |
| monterey | 0 | 15 | 0.0% | 19.5 | 0.8% | lone cypress (i3, p45) |
| edinburgh | 0 | 15 | 0.0% | 6.7 | 4.3% | - |
| perth | 0 | 15 | 0.0% | 8.1 | 3.5% | - |
| hong-kong | 1 | 14 | 7.1% | 6.4 | 4.6% | oldest tree in hong kong (i1, p9) |
| athens | 0 | 14 | 0.0% | 4.3 | 7.7% | - |
| madrid | 0 | 14 | 0.0% | 10.6 | 2.3% | - |
| boston | 0 | 14 | 0.0% | 8.2 | 3.4% | - |
| austin | 0 | 14 | 0.0% | 15.1 | 1.2% | old tree (i2, p28) |
| seoul | 1 | 13 | 7.7% | 3.8 | 8.7% | - |
| toronto | 0 | 13 | 0.0% | 6.8 | 4.2% | - |
| kagoshima | 0 | 13 | 0.0% | 7.8 | 3.6% | cycad ovule (i1, p10) |
| venice | 1 | 12 | 8.3% | 5.7 | 5.7% | are there trees in venice (i1, p11) |
| istanbul | 2 | 12 | 16.7% | 7.0 | 4.0% | istanbul (i1, p1) |
| fortingall | 0 | 12 | 0.0% | 38.0 | 0.4% | fortingall yew (i1, p9) |
| germany | 0 | 12 | 0.0% | 13.0 | 1.6% | trees germany (i2, p48) |
| san-francisco | 0 | 12 | 0.0% | 12.1 | 1.8% | - |
| switzerland | 0 | 11 | 0.0% | 5.7 | 5.5% | oldest tree in switzerland (i1, p1) |
| nara | 0 | 11 | 0.0% | 5.5 | 6.1% | - |
| the-hague | 0 | 11 | 0.0% | 4.9 | 7.1% | haag (i1, p1) |
| reykjavik | 1 | 10 | 10.0% | 5.6 | 5.8% | oldest tree in iceland (i1, p3) |
| chapel-hill-north-carolina | 0 | 10 | 0.0% | 16.5 | 1.1% | davie poplar (i2, p10) |
| jaegerspris-nordskov | 0 | 10 | 0.0% | 9.7 | 2.7% | kongeegen (i4, p10) |
| kanazawa | 0 | 10 | 0.0% | 6.1 | 4.9% | tabunoki (i1, p9) |
| oahu | 0 | 10 | 0.0% | 7.9 | 3.5% | hitachi tree hawaii (i2, p9) |
| krakow | 0 | 10 | 0.0% | 13.1 | 1.6% | - |

- Plus 204 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: barcelona, brussels, vienna, cadiz, pamplona, prague, cagliari, glasgow.

## 2026-11-03 (previous UTC day)

**Today: an android waitlist signup arrived yesterday (47 total).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 59 | 99 |
| ... of which from search | every search engine | 21 | 10 |
| ... from Google | Google's recovery | 9 | 3 |
| ... from Bing | Bing | 6 | 1 |
| Website visitors who came back | people who stay | 12 | 19 |
| App downloads (first-time) | people | 16 | 46 |
| New accounts | people | 9 | 16 |
| Phones back within 30 days | people who stay | 5 of 9 | 9 of 12 |
| Trees saved to Want to go | intent | 3 | 19 |
| Trees collected | goal 1: stood at a tree | 5 | 6 |
| Readers' contributions | data: trees, photos, corrections, votes | 2 | 8 |
| Shares (app and web) | word of mouth, since 10-30 | 1 | 0 |
| Visits from a shared link | what sharing brings | 2 | 0 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar; a visitor who comes back on another browser or device counts as new, and GA cannot leave our own visits out, so read the came-back row as a direction, not a count. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 10-28 | 10-29 | 10-30 | 10-31 | 11-01 | 11-02 | 11-03 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 7 | 8 | 12 | 7 | 8 | 11 | 10 | **63** |
| New accounts | 0 | 0 | 0 | 2 | 4 | 3 | 0 | **9** |
| Saves | 0 | 0 | 0 | 0 | 1 | 1 | 1 | **3** |
| Android waitlist | 0 | 1 | 0 | 0 | 1 | 0 | 1 | **3** |
| App downloads | 1 | 1 | 2 | 2 | 5 | 4 | 0 | **15** |
| App phones | 6 | 3 | 6 | 4 | 8 | 6 | 6 | **31** |
| Trees opened in the app | 17 | 33 | 6 | 6 | 35 | 21 | 7 | **125** |
| Trees collected | 0 | 0 | 0 | 0 | 0 | 5 | 0 | **5** |
| Trees sent | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Feedback | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Ambassador asks | 0 | 0 | 0 | 0 | 1 | 1 | 0 | **2** |
| App photos | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| App Store reviews | 0 | 0 | 1 | 0 | 0 | 0 | 0 | **1** |

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Waiting for you** (what the runs left for you since 2026-11-03)

- 796 email addresses ready to mail (archive 0, nature 18, guide 23, press 652, source 65, council 16, tourism 7, society 7, other 5, garden 3); 40 found by the night run since 2026-11-03
- before build 37, run once on your phone with Release (Edit Scheme, Run, Release, Debug executable off)
- the next app build carries the ambassador seat on the person's row.
- next build carries the snackbar and own-photo fixes.
- lax_013 El Pino is live with "view only from the street", but data/leads/los-angeles.json blocks the same tree as a private front yard under hard rule 10.
- tav_001 access rests on the 11-02 ruling that the municipal route past the resort reception counts as public; hard rule 10 excludes a reception desk, so confirm.

**What readers gave us, and it went live**

| Day | Reader | Tree | Where | What | Page |
|---|---|---|---|---|---|
| 11-02 | A | The Twisted Beech of Square des Arenes de Lutece | Paris | a reader's photograph, published | [live](https://ancienttrees.app/paris/twisted-beech-of-square-des-arenes-de-lutece) |
| 11-02 | A | The Cedar of Jussieu | Paris | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/paris/cedar-of-jussieu) |
| 11-02 | A | The Horse Chestnut of Square Rene-Le Gall | Paris | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/paris/horse-chestnut-of-square-rene-le-gall) |
| 11-02 | A | The Buffon Plane | Paris | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/paris/buffon-plane) |
- All from one reader (reader A 4).

**Searched yesterday:** agrigento, leeuwar, vienna, wi.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-25 | 3 | 55 | 5.5% | 50.2 |
| 10-26 | 3 | 36 | 8.3% | 30.5 |
| 10-27 | 0 | 25 | 0.0% | 28.5 |
| 10-28 | 1 | 36 | 2.8% | 49.8 |
| 10-29 | 0 | 38 | 0.0% | 28.4 |
| 10-30 | 2 | 29 | 6.9% | 24.1 |
| 10-31 | 0 | 38 | 0.0% | 21.5 |
| 11-01 | 5 | 371 | 1.3% | 10.1 |
| 11-02 | 23 | 1274 | 1.8% | 9.0 |
| 11-03 *partial* | 17 | 754 | 2.3% | 8.4 |
| **window** | **54** | **2656** | **2.0%** | |
- Top queries (10d): alte bäume in der nähe (i10, p8); ancient trees (i8, p14); istanbul (i1, p1); tintitaco (i2, p2); # brief your brief is to act as a visual (i1, p5)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-26 | 84 | 3 | 3.6% |
| 10-27 | 132 | 3 | 2.3% |
| 10-28 | 113 | 3 | 2.7% |
| 10-29 | 113 | 7 | 6.2% |
| 10-30 | 90 | 10 | 11.1% |
| 10-31 | 90 | 4 | 4.4% |
| 11-01 | 2225 | 8 | 0.4% |
| **7 days** | **2847** | **38** | **1.3%** |
- Week before: 587 impressions, 25 clicks. No Bing demotion in sight.
- Top Bing queries: oldest tree china (c8/i4, p12); picture of the tree in helsinki city center that was preserved (c3/i2, p4); fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); oldest sycamore tree in rotterdam (c1/i8, p2); how old are the trees in queen square bristol (c1/i4, p3); oak tree in zurich (c1/i4, p2); [ancienttrees.app/cork/witchs-yew] (c1/i4, p6)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 11-03T06:12 | 13.0 | 0 | 8 | 2 | Pamplona |
| **1 runs** | **13** | **0** | **8** | | |

- 1 of 1 produced no trees; 2 to 2 commands refused per run; last build that went live: 4h ago.

**What they made**

- Photographs readers sent, queued for a look; vouched ones live
- Contributor replies and ambassador invitations sent, log updated
- Record when each page last changed
- Record when each page last changed
- Vendor 1 photograph file(s) onto our own domain
- Weekly analysis
- Fresh-eyes review: 5 finding(s)
- Fresh-eyes review: 3 finding(s)
- Record when each page last changed
- Belfast register retried: still nothing to import, Belvoir Oak already live
- Log: Pamplona enrichment and open reader leads
- Pamplona enrichment: cedar of Arantzadi height; 29 gaps recorded as dead ends
- Write pass 2026-11-03: Capuchos plane story (sin_006), Gran Canaria and Sintra place copy, a builder for twelve held trees; nothing in data/cities yet, the 24-hour pace stands at 34

**Photographs the night run approved** (7; the last column undoes one)

| Day | Tree | Where | Overrule |
|---|---|---|---|
| 11-03 | Giant Ficus Tree, Bali Botanic Garden | Bali | `photo_apply.py hold bli_004` |
| 11-02 | The Cork Oak of Villa Siotto Pintor | Bergamo | `photo_apply.py hold bgm_009` |
| 11-03 | Drago de Galdar | Gran Canaria | `photo_apply.py hold gcn_002` |
| 11-03 | Drago de Pino Santo | Gran Canaria | `photo_apply.py hold gcn_004` |
| 11-03 | The Ka'ahumanu Church Monkeypod | Maui | `photo_apply.py hold mau_002` |
| 11-03 | Jomon Sugi | Yakushima | `photo_apply.py hold yak_001` |
| 11-03 | Daio-sugi (Yakushima) | Yakushima | `photo_apply.py hold yak_002` |

Machine: 6 chain attempts yesterday, 4 got real work time (~26 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c9/i63); /seville (c2/i37); /de (c2/i24); /fr/lyon/pedunculate-oak-of-rue-viret (c2/i8); /tenerife/el-drago-milenario (c1/i46)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'alte bäume in der nähe' (i10, p8)
    - 'alte bäume karte' (i2, p6)
    - '# brief your brief is to act as a visual' (i1, p5)
    - '# modus operandi your modus operandi is ' (i1, p2)
    - '# role mandate your role mandate is imag' (i1, p5)
    - '200 old tree trace' (i1, p54)
    - 'alte bäume' (i1, p27)
    - 'arbol mas antiguo de españa' (i1, p92)

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 2718 |
| Clicks | 54 |
| Pages that got at least one impression | 973 |
| Impressions on the proven cities | 2043 |

- 373 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3122 trees Google may index, 899 kept out for lacking a photo and an exact pin, 7133 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 106 | 10 | 21 | 0.20 | 1 |
| Not yet rich | 75 | 14 | 23 | 0.31 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| seville | 3 | 57 | 5.3% | 6.4 | 4.6% | tartuja (i3, p8) |
| tenerife | 1 | 49 | 2.0% | 15.9 | 1.1% | drago milenario (i3, p12) |
| palermo | 1 | 49 | 2.0% | 7.0 | 4.0% | falcone tree (i1, p49) |
| berlin | 0 | 44 | 0.0% | 5.0 | 6.9% | che albero è (i1, p4) |
| singapore | 0 | 44 | 0.0% | 11.8 | 1.9% | chengal pasir tree (i3, p8) |
| tokyo | 0 | 43 | 0.0% | 11.3 | 2.0% | ginkgo sperm (i4, p9) |
| lisbon | 2 | 41 | 4.9% | 7.7 | 3.6% | hoe oud (i1, p2) |
| fulufjallet | 0 | 34 | 0.0% | 7.8 | 3.6% | old tjikko (i14, p9) |
| sequoia-national-park | 0 | 32 | 0.0% | 30.3 | 0.4% | washington tree (i8, p11) |
| copenhagen | 1 | 31 | 3.2% | 11.9 | 1.8% | trees in copenhagen (i4, p18) |
| united-states | 1 | 28 | 3.6% | 13.4 | 1.5% | oldest tree in oregon (i2, p8) |
| south-korea | 0 | 26 | 0.0% | 8.1 | 3.4% | trees in korea (i3, p10) |
| olympic-national-park | 1 | 25 | 4.0% | 11.8 | 1.9% | duncan cedar (i14, p12) |
| fukuoka | 1 | 24 | 4.2% | 10.3 | 2.4% | gingkosidi (i4, p31) |
| paris | 0 | 23 | 0.0% | 6.8 | 4.2% | trees in paris (i1, p9) |
| london | 0 | 22 | 0.0% | 6.8 | 4.2% | - |
| munich | 1 | 21 | 4.8% | 4.5 | 7.5% | - |
| new-york | 0 | 21 | 0.0% | 10.4 | 2.4% | - |
| cambridge | 0 | 20 | 0.0% | 25.5 | 0.6% | is the apple tree of newton still alive (i1, p77) |
| alishan | 0 | 19 | 0.0% | 7.5 | 3.7% | xianglin sacred tree (i5, p4) |
| malaga | 1 | 18 | 5.6% | 13.6 | 1.5% | malaga tree (i2, p2) |
| rome | 0 | 17 | 0.0% | 4.7 | 7.3% | oldest tree in rome (i3, p1) |
| alicante | 0 | 16 | 0.0% | 5.6 | 5.8% | - |
| bath | 0 | 16 | 0.0% | 6.8 | 4.2% | tree in bath (i1, p9) |
| monterey | 0 | 15 | 0.0% | 23.9 | 0.6% | lone cypress (i4, p53) |
| netherlands | 0 | 15 | 0.0% | 10.1 | 2.5% | ja (i1, p5) |
| luxembourg-city | 0 | 15 | 0.0% | 5.4 | 6.2% | - |
| brisbane | 0 | 15 | 0.0% | 15.6 | 1.2% | banyan tree (i1, p74) |
| coimbra | 0 | 15 | 0.0% | 5.6 | 5.8% | - |
| dublin | 0 | 15 | 0.0% | 7.0 | 4.0% | - |
| chishang | 0 | 14 | 0.0% | 17.1 | 1.0% | takeshi kaneshiro tree (i3, p7) |
| taiwan | 0 | 14 | 0.0% | 17.7 | 1.0% | oldest tree in taiwan (i3, p6) |
| takayama | 0 | 14 | 0.0% | 8.9 | 3.1% | takayama ginkgo tree (i2, p7) |
| austin | 0 | 14 | 0.0% | 15.1 | 1.2% | old tree (i2, p28) |
| kyoto | 0 | 14 | 0.0% | 12.1 | 1.8% | - |
| porto | 0 | 13 | 0.0% | 5.0 | 7.0% | - |
| montreal | 3 | 12 | 25.0% | 5.1 | 6.8% | - |
| fortingall | 0 | 12 | 0.0% | 38.9 | 0.4% | fortingall yew (i1, p9) |
| madrid | 0 | 12 | 0.0% | 11.7 | 1.9% | - |
| boston | 0 | 12 | 0.0% | 8.0 | 3.5% | - |
| amsterdam | 0 | 12 | 0.0% | 6.5 | 4.5% | - |
| istanbul | 2 | 11 | 18.2% | 7.6 | 3.7% | istanbul (i1, p1) |
| switzerland | 0 | 11 | 0.0% | 5.7 | 5.5% | oldest tree in switzerland (i1, p1) |
| hong-kong | 1 | 10 | 10.0% | 6.2 | 4.8% | - |
| venice | 0 | 10 | 0.0% | 6.0 | 5.0% | are there trees in venice (i1, p11) |
| jaegerspris-nordskov | 0 | 10 | 0.0% | 9.7 | 2.7% | kongeegen (i4, p10) |
| kanazawa | 0 | 10 | 0.0% | 6.1 | 4.9% | tabunoki (i1, p9) |
| edinburgh | 0 | 10 | 0.0% | 7.3 | 3.9% | - |
| kagoshima | 0 | 10 | 0.0% | 7.4 | 3.8% | cycad ovule (i1, p10) |

- Plus 215 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: barcelona, oahu, brussels, vienna, athens, cadiz, pamplona, prague.

## Weekly analysis 2026-11-03

Fourteenth weekly analysis. Compares 10-26 to 11-01 with 10-19 to 10-25, read
from the 11-02 and 11-01 daily entries. Google's newest days are partial, so
11-02 is shown apart. Volumes are small; nothing below is a trend unless it says so.

**Scorecard**

| Week | Impressions | Clicks | CTR | Avg position | Visitors (GA, new) | Directions (web) | App-CTA | App downloads (first-time) | Android waitlist total | Readers' contributions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10-19 to 10-25 | 296 (partial) | 10 | 3.4% | 26 to 59 | 85 | not in the entries | not in the entries | 38 | 42 | 11 |
| 10-26 to 11-01 | 573 | 11 | 1.9% | 21 to 50, then 12.3 on 11-01 | 62 | not in the entries | not in the entries | 17 | 46 (11-01) | 8 |
| 11-02 alone (partial) | 854 | 14 | 1.6% | 9.1 | 11 (day) | - | - | 0 | n/a | 2 |

Bing, 7 days ending 10-31: 705 impressions and 33 clicks (4.7%), against 554 and 24.
Bing index 3,428 to 3,740 pages. App return: 4 of 8 phones back within 30 days
against 13 of 18 (small bases). Device split and per-visit ratios cannot be kept:
`audience_section` still fails ("name 'MARKERS' is not defined", 11-01 entry), so
no ratio is claimed.

**Outreach yield** (data/mail-yield.json, mailbox read; weeks keyed by the Monday of our first mail, so the week of 10-26 is too young to judge)

| Group | Mailed, week of 10-19 | Answered of those | Mailed, total | Answered, total | Rate | Linked |
|---|---:|---:|---:|---:|---:|---:|
| archive | 0 | 0 | 15 | 1 | 7% | 0 |
| nature | 0 | 0 | 65 | 3 | 5% | 1 |
| guide | 0 | 0 | 17 | 1 | 6% | 1 |
| source | 24 | 1 | 59 | 3 | 5% | 0 |
| press | 27 | 1 | 98 | 6 | 6% | 0 |
| tourism | 17 | 3 | 18 | 3 | 17% | 0 |
| garden | 0 | 0 | 97 | 11 | 11% | 0 |
| society | 0 | 0 | 148 | 25 | 17% | 1 |
| council | 0 | 0 | 55 | 8 | 15% | 0 |
| other | 17 | 7 | 143 | 46 | 32% | 2 |

Nature had 63 of its 65 mailed in the week of 10-26: 2 answers so far, both
automatic, so its rate is not yet a rate. Six links in total across all groups.

**What moved:**
1. Google stepped up on its last two days: 371 impressions on 11-01 and 854 (partial)
   on 11-02, against 24 to 55 a day for the weeks before, with position 10.1 and 9.1
   instead of 20 to 50. Clicks 5 and 14. Two days, partial rows, the first time since the
   09-28 demotion; not yet a recovery. Top pages in the window are still `/` and
   Portugal, Seville, Maryland pages at 15 to 50 impressions.
2. Everything the 10-24 Portuguese link day inflated fell back: visitors 96 to 58,
   downloads 45 to 14, saves 19 to 2, collected 7 to 0, contributions 16 to 2. Daily
   visitors sit at 7 to 12, the same floor as before the spike.
3. Bing still out-clicks Google over the full week, 33 against 11, and sent 6 to 7
   new visitors a week against 0 before.
4. Readers: one person (reader A) photographed five Paris trees on 11-02, four went
   live. Ambassador requests keep arriving (Pamplona, New Orleans). The "56 total"
   this line carried was every submission of every kind, not requests; the count
   lives in `ambassador.py --requests` only (Hidde, 2026-11-03).
5. Outreach: 364 addresses are ready and unsent (press 234, source 67, nature 9,
   guide 5, archive 9). The yield table says press and source answer at 5 to 6%,
   society, council and tourism at 15 to 17%.

**Suggestions, ranked:**
1. **[run]** Once 11-01 to 11-03 fill in, pull the query and page split of the Google
   step-up (which pages carry the 854 impressions, how many are `site:` or operator
   searches, which are real queries) and say in the next digest whether it holds for
   three days. Everything else on Google waits on this one answer.
2. **[FOR HIDDE]** Send the nature (9), guide (5) and archive (9) drafts first, the
   order you set on 10-31. They are 23 of 364 ready addresses, while press (234) has
   the lowest answer rate of the large groups (6% of 98). Nature produced the only
   referral spike (wilder.pt, 10-24), and its 63 recent mails are too young to judge.
3. **[run]** Pages at positions 5 to 7 with no clicks: berlin (21 impressions, 5.0),
   alicante (10, 5.4), paris (15, 6.3), luxembourg-city (13, 6.1), bath (13, 6.7), where
   the normal CTR is 4.7 to 6.9%. About 5 clicks expected from 72 impressions, 0 got.
   Counts are small, so check title, meta and lead photograph on each for a mismatch
   with the query, not a rewrite of the set.
4. **[run]** Serve queries that name a page we have or a gap: "alte bäume in der nähe"
   (4 impressions, position 8: does the German home title carry "in der Nähe"?),
   "drago milenario" (Tenerife page, position 13, 24 impressions: photograph and
   register link), "general sherman tree" (Sequoia, position 64 to 77 for a fifth week:
   check the page answers it in the first line).
5. **[sessie]** Fix `audience_section` (MARKERS undefined), failing in the Monday
   entry two weeks running, so this scorecard has no device split or per-visit ratios.

**Watch next week:** whether Google stays above about 300 impressions a day at position
under 15 without the partial-day inflation, and whether the 10-26 outreach batch (63
nature, 38 press, 21 source) produces answers or links beyond the 2 automatic ones.

## 2026-11-02 (previous UTC day)

**Today: an ambassador request for Pamplona arrived yesterday (56 total); 3 accounts were opened yesterday (56 total).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 58 | 96 |
| ... of which from search | every search engine | 18 | 10 |
| ... from Google | Google's recovery | 5 | 4 |
| ... from Bing | Bing | 6 | 1 |
| Website visitors who came back | people who stay | 13 | 17 |
| App downloads (first-time) | people | 14 | 45 |
| New accounts | people | 9 | 17 |
| Phones back within 30 days | people who stay | 4 of 8 | 13 of 18 |
| Trees saved to Want to go | intent | 2 | 19 |
| Trees collected | goal 1: stood at a tree | 0 | 7 |
| Readers' contributions | data: trees, photos, corrections, votes | 2 | 16 |
| Shares (app and web) | word of mouth, since 10-30 | 1 | 0 |
| Visits from a shared link | what sharing brings | 2 | 0 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar; a visitor who comes back on another browser or device counts as new, and GA cannot leave our own visits out, so read the came-back row as a direction, not a count. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 10-27 | 10-28 | 10-29 | 10-30 | 10-31 | 11-01 | 11-02 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 11 | 7 | 8 | 12 | 7 | 8 | 11 | **64** |
| New accounts | 0 | 0 | 0 | 0 | 2 | 4 | 3 | **9** |
| Saves | 0 | 0 | 0 | 0 | 0 | 1 | 1 | **2** |
| Android waitlist | 1 | 0 | 1 | 0 | 0 | 1 | 0 | **3** |
| App downloads | 1 | 1 | 1 | 2 | 2 | 5 | 0 | **12** |
| App phones | 4 | 6 | 3 | 6 | 4 | 8 | 6 | **29** |
| Trees opened in the app | 4 | 17 | 33 | 6 | 6 | 35 | 21 | **122** |
| Trees collected | 0 | 0 | 0 | 0 | 0 | 0 | 5 | **5** |
| Trees sent | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Feedback | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Ambassador asks | 0 | 0 | 0 | 0 | 0 | 1 | 1 | **2** |
| App photos | 0 | 0 | 0 | 0 | 0 | 0 | 5 | **5** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| App Store reviews | 1 | 0 | 0 | 1 | 0 | 0 | 0 | **2** |

**Trees readers sent, for you to inspect** (5 you have not looked at; ours left out)

| Judged | Reader | Tree | Where | Species | Their girth | Our verdict | Page |
|---|---|---|---|---|---:|---|---|
| 2026-11-02 | A | The Twisted Beech of Square des Arenes de Lu | Paris | Twisted Beech (Fagus sylvatica | - | lead | [par_016](https://ancienttrees.app/paris/twisted-beech-of-square-des-arenes-de-lutece) |
| 2026-11-02 | A | The Cedar of Jussieu | Paris | Cedar of Lebanon (Cedrus liban | - | lead | [par_002](https://ancienttrees.app/paris/cedar-of-jussieu) |
| 2026-11-02 | A | The Horse Chestnut of Square Rene-Le Gall | Paris | Horse Chestnut (Aesculus hippo | - | lead | [par_031](https://ancienttrees.app/paris/horse-chestnut-of-square-rene-le-gall) |
| 2026-11-02 | A | The Buffon Plane | Paris | Oriental Plane (Platanus orien | - | lead | [par_004](https://ancienttrees.app/paris/buffon-plane) |
| 2026-11-02 | A | The Turkey Oak of Square Rene-Le Gall | Paris | Turkey Oak (Quercus cerris) | - | hold | - |
- All from one reader (reader A 5).
- Photographs and the readers' own words: `python3 scripts/inspect_readers.py` (a local page, never in this public file). Your answer goes in with `python3 scripts/judgement.py --feedback <id> "..."`.

**Waiting for you** (what the runs left for you since 2026-11-02)

- 364 email addresses ready to mail (archive 9, nature 9, guide 5, press 234, source 67, council 17, tourism 7, society 7, other 6, garden 3); 7 found by the night run since 2026-11-02

**What readers gave us, and it went live**

| Day | Reader | Tree | Where | What | Page |
|---|---|---|---|---|---|
| 11-02 | A | The Twisted Beech of Square des Arenes de Lutece | Paris | a reader's photograph, published | [live](https://ancienttrees.app/paris/twisted-beech-of-square-des-arenes-de-lutece) |
| 11-02 | A | The Cedar of Jussieu | Paris | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/paris/cedar-of-jussieu) |
| 11-02 | A | The Horse Chestnut of Square Rene-Le Gall | Paris | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/paris/horse-chestnut-of-square-rene-le-gall) |
| 11-02 | A | The Buffon Plane | Paris | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/paris/buffon-plane) |
- All from one reader (reader A 4).

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| 2026-11-02 | The Twisted Beech of Square des Arenes | Paris | - | lead | - |
| 2026-11-02 | The Cedar of Jussieu | Paris | - | lead | - |
| 2026-11-02 | The Horse Chestnut of Square Rene-Le G | Paris | - | lead | - |
| 2026-11-02 | The Buffon Plane | Paris | - | lead | - |
| 2026-11-02 | The Turkey Oak of Square Rene-Le Gall | Paris | - | hold | - |
| 2026-10-30 | The Town Hall Plane | - | - | open | - |
| 2026-10-30 | A tree in Baarn | - | - | open | - |
| 2026-10-30 | European Beech in Baarn | - | - | open | - |
| 2026-10-30 | A tree in Baarn | - | - | open | - |

4 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**Searched yesterday:** bologna, lisboa, rome.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-24 | 1 | 24 | 4.2% | 43.2 |
| 10-25 | 3 | 55 | 5.5% | 50.2 |
| 10-26 | 3 | 36 | 8.3% | 30.5 |
| 10-27 | 0 | 25 | 0.0% | 28.5 |
| 10-28 | 1 | 36 | 2.8% | 49.8 |
| 10-29 | 0 | 38 | 0.0% | 28.4 |
| 10-30 | 2 | 29 | 6.9% | 24.1 |
| 10-31 | 0 | 38 | 0.0% | 21.5 |
| 11-01 | 5 | 371 | 1.3% | 10.1 |
| 11-02 *partial* | 14 | 854 | 1.6% | 9.1 |
| **window** | **29** | **1506** | **1.9%** | |
- Top queries (10d): istanbul (i1, p1); tintitaco (i2, p2); # role mandate your role mandate is imag (i1, p5); 200 old tree trace (i1, p54); 600 year old ginkgo tree jeonju (i1, p55)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-25 | 83 | 3 | 3.6% |
| 10-26 | 84 | 3 | 3.6% |
| 10-27 | 132 | 3 | 2.3% |
| 10-28 | 113 | 3 | 2.7% |
| 10-29 | 113 | 7 | 6.2% |
| 10-30 | 90 | 10 | 11.1% |
| 10-31 | 90 | 4 | 4.4% |
| **7 days** | **705** | **33** | **4.7%** |
- Week before: 554 impressions, 24 clicks. No Bing demotion in sight.
- Top Bing queries: oldest tree china (c8/i4, p12); picture of the tree in helsinki city center that was preserved (c3/i2, p4); fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); oldest sycamore tree in rotterdam (c1/i8, p2); how old are the trees in queen square bristol (c1/i4, p3); oak tree in zurich (c1/i4, p2); [ancienttrees.app/cork/witchs-yew] (c1/i4, p6)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 11-02T06:32 | 15.2 | 1 | 8 | 2 | Bergamo +1 |
| 11-02T19:56 | 0.0 | 0 | 2 | 0 | - |
| 11-03T01:58 | 3.7 | 0 | 2 | 1 | - |
| **3 runs** | **19** | **1** | **12** | | |

- 2 of 3 produced no trees; 1 to 2 commands refused per run; 1 wrote nothing to LOG.md; last build that went live: 3h ago.

**What they made**

- Sintra verify pass: one flagged tree and two leads; log entry
- Photographs readers sent, queued for a look; vouched ones live
- Record when each page last changed
- Contributor replies and ambassador invitations sent, log updated
- Vendor 2 photograph file(s) onto our own domain
- Fresh-eyes review: 5 finding(s)
- Fresh-eyes review: 3 finding(s)
- Record when each page last changed
- Night run: Porto walled, Bergamo register scouted (stalled), LOG
- Night run second attempt: Bergamo Gorlago cork oak, LOG
- Bergamo +1: the cork oak of Villa Siotto Pintor (Gorlago), photo approved; five READY leads held
- Night run 06:32: enrich NY/Dublin/Montreal closed nothing, LOG

**Photographs the night run approved** (1; the last column undoes one)

| Day | Tree | Where | Overrule |
|---|---|---|---|
| 11-02 | The Cork Oak of Villa Siotto Pintor | Bergamo | `photo_apply.py hold bgm_009` |

Machine: 4 chain attempts yesterday, 2 got real work time (~31 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c9/i50); /tenerife/el-drago-milenario (c1/i23); /lisbon (c1/i20); /seville (c1/i17); /united-states/maryland (c1/i15)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'alte bäume in der nähe' (i4, p8)
    - '# role mandate your role mandate is imag' (i1, p5)
    - '200 old tree trace' (i1, p54)
    - 'biggest spruce tree in the world' (i1, p31)
    - 'bild zu 1' (i1, p2)
    - 'bilder' (i1, p1)

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 1523 |
| Clicks | 29 |
| Pages that got at least one impression | 684 |
| Impressions on the proven cities | 1111 |

- 383 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3110 trees Google may index, 884 kept out for lacking a photo and an exact pin, 7108 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 97 | 7 | 11 | 0.11 | 0 |
| Not yet rich | 70 | 7 | 8 | 0.11 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| lisbon | 2 | 26 | 7.7% | 9.2 | 2.9% | hoe oud (i1, p2) |
| seville | 1 | 25 | 4.0% | 7.9 | 3.6% | tartuja (i2, p9) |
| tokyo | 0 | 25 | 0.0% | 14.2 | 1.4% | ginkgo sperm (i2, p10) |
| tenerife | 1 | 24 | 4.2% | 17.5 | 1.0% | drago milenario (i1, p13) |
| singapore | 0 | 24 | 0.0% | 16.3 | 1.1% | trees online singapore (i2, p44) |
| palermo | 0 | 22 | 0.0% | 8.6 | 3.2% | falcone tree (i1, p49) |
| berlin | 0 | 21 | 0.0% | 5.0 | 6.9% | - |
| united-states | 1 | 19 | 5.3% | 16.6 | 1.1% | maryland's state tree (i1, p100) |
| sequoia-national-park | 0 | 18 | 0.0% | 45.4 | 0.4% | general sherman tree (i4, p64) |
| south-korea | 0 | 15 | 0.0% | 10.5 | 2.3% | 600 year old ginkgo tree jeonju (i1, p55) |
| paris | 0 | 15 | 0.0% | 6.3 | 4.7% | - |
| fulufjallet | 0 | 13 | 0.0% | 7.7 | 3.7% | old tjikko (i3, p8) |
| luxembourg-city | 0 | 13 | 0.0% | 6.1 | 4.9% | - |
| bath | 0 | 13 | 0.0% | 6.7 | 4.3% | - |
| copenhagen | 0 | 13 | 0.0% | 16.4 | 1.1% | trees in copenhagen (i2, p16) |
| new-york | 0 | 13 | 0.0% | 12.0 | 1.8% | - |
| olympic-national-park | 1 | 12 | 8.3% | 16.4 | 1.1% | duncan cedar (i8, p13) |
| chishang | 0 | 11 | 0.0% | 19.6 | 0.8% | takeshi kaneshiro tree (i2, p6) |
| cambridge | 0 | 11 | 0.0% | 32.8 | 0.4% | is the apple tree of newton still alive (i1, p77) |
| jaegerspris-nordskov | 0 | 10 | 0.0% | 9.7 | 2.7% | kongeegen (i4, p10) |
| madrid | 0 | 10 | 0.0% | 12.3 | 1.7% | - |
| alicante | 0 | 10 | 0.0% | 5.4 | 6.2% | - |
| fukuoka | 0 | 10 | 0.0% | 9.0 | 3.0% | gingkosidi (i2, p26) |

- Plus 238 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: amsterdam, barcelona, rome, oahu, munich, edinburgh, brussels, dublin.

## 2026-11-01 (previous UTC day)

**Today: an android waitlist signup arrived yesterday (46 total); an ambassador request for New Orleans arrived yesterday (55 total); 4 accounts were opened yesterday (53 total).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 62 | 85 |
| ... of which from search | every search engine | 17 | 8 |
| ... from Google | Google's recovery | 3 | 2 |
| ... from Bing | Bing | 7 | 0 |
| Website visitors who came back | people who stay | 12 | 17 |
| App downloads (first-time) | people | 17 | 38 |
| New accounts | people | 9 | 16 |
| Phones back within 30 days | people who stay | 8 of 13 | 9 of 13 |
| Trees saved to Want to go | intent | 1 | 19 |
| Trees collected | goal 1: stood at a tree | 0 | 13 |
| Readers' contributions | data: trees, photos, corrections, votes | 8 | 10 |
| Shares (app and web) | word of mouth, since 10-30 | 1 | 0 |
| Visits from a shared link | what sharing brings | 2 | 0 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar; a visitor who comes back on another browser or device counts as new, and GA cannot leave our own visits out, so read the came-back row as a direction, not a count. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Ambassador requests, open** (1 person, 1 place; each stays here until our mail with the questions has gone, or the badge is granted with `python3 scripts/ambassador.py --grant`)

| Asked | Places | From | Our mail with the questions | Waiting on |
|---|---|---|---|---|
| 2026-11-01 | **New Orleans** | /new-orleans | not yet (next knock) | the mail |

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 10-26 | 10-27 | 10-28 | 10-29 | 10-30 | 10-31 | 11-01 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 14 | 11 | 7 | 8 | 12 | 7 | 8 | **67** |
| New accounts | 3 | 0 | 0 | 0 | 0 | 2 | 4 | **9** |
| Saves | 0 | 0 | 0 | 0 | 0 | 0 | 1 | **1** |
| Android waitlist | 5 | 1 | 0 | 1 | 0 | 0 | 1 | **8** |
| App downloads | 2 | 1 | 1 | 1 | 2 | 2 | 0 | **9** |
| App phones | 6 | 4 | 6 | 3 | 6 | 4 | 8 | **27** |
| Trees opened in the app | 88 | 4 | 17 | 33 | 6 | 6 | 35 | **189** |
| Trees collected | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Trees sent | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Feedback | 1 | 0 | 0 | 0 | 0 | 0 | 0 | **1** |
| Ambassador asks | 6 | 0 | 0 | 0 | 0 | 0 | 1 | **7** |
| App photos | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| App Store reviews | 0 | 1 | 0 | 0 | 1 | 0 | 0 | **2** |

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Waiting for you** (what the runs left for you since 2026-11-01)

- 364 email addresses ready to mail (archive 9, nature 9, guide 5, press 234, source 67, council 17, tourism 7, society 7, other 6, garden 3); 7 found by the night run since 2026-11-01

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| 2026-10-30 | The Town Hall Plane | - | - | open | - |
| 2026-10-30 | A tree in Baarn | - | - | open | - |
| 2026-10-30 | European Beech in Baarn | - | - | open | - |
| 2026-10-30 | A tree in Baarn | - | - | open | - |

4 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**Searched yesterday:** amorebieta, creswell, or, dallas.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-23 | 0 | 48 | 0.0% | 55.1 |
| 10-24 | 1 | 24 | 4.2% | 43.2 |
| 10-25 | 3 | 55 | 5.5% | 50.2 |
| 10-26 | 3 | 36 | 8.3% | 30.5 |
| 10-27 | 0 | 25 | 0.0% | 28.5 |
| 10-28 | 1 | 36 | 2.8% | 49.8 |
| 10-29 | 0 | 38 | 0.0% | 28.4 |
| 10-30 | 2 | 29 | 6.9% | 24.1 |
| 10-31 | 0 | 38 | 0.0% | 21.5 |
| 11-01 *partial* | 2 | 125 | 1.6% | 12.3 |
| **window** | **12** | **454** | **2.6%** | |
- Top queries (10d): 200 old tree trace (i1, p54); 600 year old ginkgo tree jeonju (i1, p55); ahuehuete madrid (i1, p95); ancient tree (i1, p76); ancient trees (i3, p81)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-25 | 83 | 3 | 3.6% |
| 10-26 | 84 | 3 | 3.6% |
| 10-27 | 132 | 3 | 2.3% |
| 10-28 | 113 | 3 | 2.7% |
| 10-29 | 113 | 7 | 6.2% |
| 10-30 | 90 | 10 | 11.1% |
| 10-31 | 90 | 4 | 4.4% |
| **7 days** | **705** | **33** | **4.7%** |
- Week before: 554 impressions, 24 clicks. No Bing demotion in sight.
- Top Bing queries: oldest tree china (c8/i4, p12); picture of the tree in helsinki city center that was preserved (c3/i2, p4); fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); oldest sycamore tree in rotterdam (c1/i8, p2); how old are the trees in queen square bristol (c1/i4, p3); oak tree in zurich (c1/i4, p2); [ancienttrees.app/cork/witchs-yew] (c1/i4, p6)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

**Monday: the slow tables.** They rarely change a day's decision, so they come once a week.

**Website actions, ever** (the events table begins 2026-08-01, when the funnel was repaired; a zero has never fired at all)

| Action | Ever |
|---|---:|
| signin-open | 217 |
| app-cta | 168 |
| search-home | 108 |
| home-fav | 61 |
| waitlist-submit | 31 |
| signin-done | 28 |
| signin-oauth | 28 |
| app-open | 23 |
| home-country | 22 |
| search-bar | 16 |
| search-explore | 16 |
| home-dir-city | 12 |
| ambassador-request | 9 |
| directions | 8 |
| search-bar-m | 8 |
| signin-link-sent | 8 |
| save | 4 |
| search-empty-bar | 4 |
| home-dir-collection | 3 |
| home-dir-tree | 3 |
| home-species | 3 |
| share_arrived | 2 |
| app-page-badge | 2 |
| home-dir-species | 2 |
| search-empty-home | 2 |
| signout | 2 |
| sponsor-open | 2 |
| search-none-explore | 1 |
| share_tapped | 1 |
| tree-photo-sent | 1 |
| search-empty-explore | 1 |
| search-none-bar | 1 |
| search-none-bar-m | 1 |
| search-none-home | 1 |
| worthit-report | 1 |
| worthit-not worth it | 0 |
| worthit-worth it | 0 |
| **all** | **800** |

**App events, ever** (measured since 2026-08-30)

| What | Ever |
|---|---:|
| app_open | 538 |
| tab | 476 |
| tree_opened | 1993 |
| directions | 68 |
| tree_saved | 46 |
| tree_visited | 35 |
| sighting_recorded | 90 |
| sync_skipped | 0 |
| sync_failed | 0 |
| location | 65 |
| **all** | **3311** |

**What readers told us** (7 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 10-26 | Sintra | ambassador request | - | d1d9 | - |
| 10-26 | por_011 (The Copper Beech of FAUP) | report | dead or gone | 6cff | changed |
| 10-26 | Porto | ambassador request | - | 6cff | - |
| 10-26 | Guimaraes | ambassador request | - | 6cff | - |
| 10-26 | Braga | ambassador request | - | 6cff | - |
| 10-26 | Calvos | ambassador request | - | 6cff | - |
| 10-26 | Vales | ambassador request | - | 6cff | - |
| 11-01 | New Orleans | ambassador request | - | c9cb | - |

- 6 of the other 8 came from one account (6cff), which is one person rather than a pattern.

**App Store downloads** (Apple's own count, not PostHog)

| Day | Downloads |
|---|---:|
| 2026-10-24 | 23 |
| 2026-10-25 | 8 |
| 2026-10-26 | 2 |
| 2026-10-27 | 1 |
| 2026-10-28 | 1 |
| 2026-10-29 | 1 |
| 2026-10-30 | 2 |
| 2026-10-31 | 2 |
| **8 days** | **40** |
- First-time downloads only, which is what App Store Connect's Trends screen counts; redownloads and updates are not in this table.

**Where the downloads came from** (7 days, Apple's attribution)

| Came from | Via | Downloads |
|---|---|---:|
| App Store search | - | 18 |
| App referrer | - | 12 |
| Web referrer | - | 10 |
| **window** | | **40** |
- Countries: PT (24); GB (5); US (3); BR (2); CA (1); CH (1)
- Apple's own source split, first-time downloads only. "Web referrer" with our own domain is the site's app page; "App Store search" is somebody who typed into the store. "Unavailable" is Apple's word for a source it could not attribute.

**Bing's index** (pages crawled and in index, Bing Webmaster Tools)

| Day | Pages crawled | Pages in index |
|---|---:|---:|
| 10-25 | 235 | 3470 |
| 10-28 | 343 | 3629 |
| 10-29 | 474 | 3678 |
| 10-30 | 221 | 3740 |
- In index the week before: 3428.

audience_section: failed today (name 'MARKERS' is not defined).

**Google Analytics** (last 7 days, visitors who accepted cookies)

| Day | People | New | Returning | Visits | Pageviews | Engaged visits |
|---|---:|---:|---:|---:|---:|---:|
| 10-26 | 14 | 14 | 0 | 19 | 138 | 14 |
| 10-27 | 11 | 9 | 2 | 15 | 79 | 10 |
| 10-28 | 7 | 6 | 1 | 10 | 36 | 9 |
| 10-29 | 8 | 7 | 1 | 9 | 22 | 8 |
| 10-30 | 12 | 11 | 1 | 14 | 37 | 9 |
| 10-31 | 7 | 7 | 0 | 8 | 20 | 4 |
| 11-01 | 8 | 8 | 0 | 12 | 26 | 8 |
| **window** | | **62** | | **87** | **358** | **62** |
- People per day are not summed: one person on two days is one person, and GA counts them once per day.
- Coming back (28 days): 31 returning against 172 new, 15% of the people GA saw.

| Page | Pageviews | People |
|---|---:|---:|
| / | 55 | 23 |
| /about | 19 | 2 |
| /lisbon | 18 | 11 |
| /support | 13 | 2 |
| /sources | 12 | 2 |
| /porto | 10 | 3 |
| /portugal | 10 | 5 |
| /account/settings | 9 | 1 |
| /countries | 7 | 6 |
| /calvos | 6 | 2 |

| Came from | Visits | People |
|---|---:|---:|
| (direct) / (none) | 42 | 34 |
| google / organic | 8 | 3 |
| bing / organic | 7 | 7 |
| wilder.pt / referral | 7 | 6 |
| accounts.google.com / referral | 6 | 2 |
| ecosia.org / organic | 6 | 5 |
| (not set) / (not set) | 3 | 3 |
| chatgpt.com / ai-assistant | 2 | 2 |
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
| 11-01T19:49 | 6.6 | 0 | 4 | 0 | - |
| 11-01T21:36 | 6.3 | 1 | 6 | 0 | Porto +1 |
| 11-02T01:11 | 11.9 | 0 | 6 | 0 | - |
| **3 runs** | **25** | **1** | **16** | | |

- 2 of 3 produced no trees; last build that went live: 5h ago.

**What they made**

- Night run 01:11: Madeira retry stalled, Porto enrich closed, SF wall, LOG
- San Francisco deepen pass 2026-11-02: nothing new, register exhausted
- Write pass: none merged (faro, frankfurt, innsbruck, new-york, san-francisco, cardiff held)
- Photographs readers sent, queued for a look; vouched ones live
- Record when each page last changed
- Porto pt overlay: por_031 under 250 words
- Porto pt overlay: por_031 story back under 250 words
- Porto: 5 leads beyond the day-trip boundary, pass costs logged
- Porto: write and merge por_031, the cork oak of the Capela de Santo Antonio (Maia)
- Cardiff scouting retry: Bute Park champion table, 3 flagged trees staged, 3 leads
- Coimbra verify pass: no new tree, Santa Comba pine kept as a lead, wall for 48h
- Record when each page last changed
- Record when each page last changed
- Vendor 1 photograph file(s) onto our own domain

Machine: 7 chain attempts yesterday, 3 got real work time (~40 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c7/i18); /lisbon (c1/i7); /seville (c1/i4); /lisbon/giant-rubber-tree-of-mouraria (c1/i2); /montreal/mcgill-katsura (c1/i1)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'comfort tree niagara' (i2, p75)
    - '200 old tree trace' (i1, p54)
    - 'bilder' (i1, p1)
    - 'comfort tree' (i1, p13)
    - 'die 10 ältesten bäume der welt' (i1, p1)
    - 'drachenbaum auf teneriffa' (i1, p96)
    - 'drago milenario tree' (i1, p42)

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 432 |
| Clicks | 12 |
| Pages that got at least one impression | 269 |
| Impressions on the proven cities | 278 |

- 373 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3097 trees Google may index, 863 kept out for lacking a photo and an exact pin, 7053 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 96 | 0 | 0 | 0.00 | 0 |
| Not yet rich | 67 | 4 | 6 | 0.09 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| sequoia-national-park | 0 | 14 | 0.0% | 67.9 | 0.4% | general sherman tree (i3, p77) |

- Plus 258 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

## 2026-10-31 (previous UTC day)

**Today: an account was opened today (52 total).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 64 | 77 |
| ... of which from search | every search engine | 13 | 9 |
| ... from Google | Google's recovery | 3 | 2 |
| ... from Bing | Bing | 6 | 0 |
| Website visitors who came back | people who stay | 13 | 14 |
| App downloads (first-time) | people | 38 | 18 |
| New accounts | people | 9 | 13 |
| Phones back within 30 days | people who stay | 9 of 13 | 8 of 12 |
| Trees saved to Want to go | intent | 0 | 23 |
| Trees collected | goal 1: stood at a tree | 0 | 13 |
| Readers' contributions | data: trees, photos, corrections, votes | 7 | 12 |
| Shares (app and web) | word of mouth, since 10-30 | 0 | 0 |
| Visits from a shared link | what sharing brings | 0 | 0 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar; a visitor who comes back on another browser or device counts as new, and GA cannot leave our own visits out, so read the came-back row as a direction, not a count. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 10-25 | 10-26 | 10-27 | 10-28 | 10-29 | 10-30 | 10-31 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 11 | 14 | 11 | 7 | 8 | 12 | 7 | **70** |
| New accounts | 3 | 3 | 0 | 0 | 0 | 1 | 2 | **9** |
| Saves | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Android waitlist | 4 | 5 | 1 | 0 | 1 | 0 | 0 | **11** |
| App downloads | 8 | 2 | 1 | 1 | 1 | 2 | 0 | **15** |
| App phones | 9 | 6 | 4 | 6 | 3 | 6 | 4 | **32** |
| Trees opened in the app | 37 | 88 | 4 | 17 | 33 | 6 | 6 | **191** |
| Trees collected | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Trees sent | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Feedback | 0 | 1 | 0 | 0 | 0 | 0 | 0 | **1** |
| Ambassador asks | 0 | 6 | 0 | 0 | 0 | 0 | 0 | **6** |
| App photos | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| App Store reviews | 0 | 0 | 1 | 0 | 0 | 1 | 0 | **2** |

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Waiting for you** (what the runs left for you since 2026-10-31)

- 399 email addresses ready to mail (archive 9, nature 20, guide 14, press 249, source 67, council 17, tourism 7, society 7, other 6, garden 3); 44 found by the night run since 2026-10-31
- the next app build carries the empty-seat line.
- the four Baarn photos need a look with the key.
- next build carries the fix once deploy.yml runs (a laptop push or the schedule).

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| 2026-10-30 | The Town Hall Plane | - | - | open | - |
| 2026-10-30 | A tree in Baarn | - | - | open | - |
| 2026-10-30 | European Beech in Baarn | - | - | open | - |
| 2026-10-30 | A tree in Baarn | - | - | open | - |

4 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**Searched yesterday:** donegal, funchal, gravesend, lisbo, oak, valenciennes.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-22 | 2 | 45 | 4.4% | 51.8 |
| 10-23 | 0 | 48 | 0.0% | 55.1 |
| 10-24 | 1 | 24 | 4.2% | 43.2 |
| 10-25 | 3 | 55 | 5.5% | 50.2 |
| 10-26 | 3 | 36 | 8.3% | 30.5 |
| 10-27 | 0 | 25 | 0.0% | 28.5 |
| 10-28 | 1 | 36 | 2.8% | 49.8 |
| 10-29 | 0 | 38 | 0.0% | 28.4 |
| 10-30 | 2 | 29 | 6.9% | 24.1 |
| 10-31 *partial* | 0 | 28 | 0.0% | 21.3 |
| **window** | **12** | **364** | **3.3%** | |
- Top queries (10d): 200 old tree trace (i1, p54); 600 year old ginkgo tree jeonju (i1, p55); ahuehuete madrid (i1, p95); ancient roman trees (i1, p68); ancient tree (i1, p76)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-23 | 82 | 5 | 6.1% |
| 10-24 | 69 | 4 | 5.8% |
| 10-25 | 83 | 3 | 3.6% |
| 10-26 | 84 | 3 | 3.6% |
| 10-27 | 132 | 3 | 2.3% |
| 10-28 | 113 | 3 | 2.7% |
| 10-29 | 113 | 7 | 6.2% |
| **7 days** | **676** | **28** | **4.1%** |
- Week before: 530 impressions, 20 clicks. No Bing demotion in sight.
- Top Bing queries: oldest tree china (c8/i4, p12); picture of the tree in helsinki city center that was preserved (c3/i2, p4); fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); oldest sycamore tree in rotterdam (c1/i8, p2); how old are the trees in queen square bristol (c1/i4, p3); oak tree in zurich (c1/i4, p2); [ancienttrees.app/cork/witchs-yew] (c1/i4, p6)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-31T06:03 | 4.3 | 0 | 5 | 2 | Paris, Rio Frio |
| 10-31T07:53 | 3.3 | 0 | 5 | 0 | - |
| 10-31T19:24 | 33.0 | 14 | 12 | 1 | Canberra +5, Frankfurt +4, Fort Worth +3, Madrid +1, +1 more |
| 11-01T01:29 | 21.0 | 3 | 10 | 1 | Dublin +2, New York +1, Paris |
| **4 runs** | **62** | **17** | **32** | | |

- 2 of 4 produced no trees; 1 to 2 commands refused per run; last build that went live: 2h ago.

**What they made**

- Record when each page last changed
- Porto verify: Cavadinha cork oak staged, 2 leads; claim kept until merged
- Write pass: nyc_030 Douglaston weeping beech and dub_019 Marlay cedar live; 5 verified and 6 READY leads held with reasons
- New York verify: two flagged trees staged, 87 leads annotated
- Scout Faro and Savannah again: verdicts recorded, log extended
- Scout Coimbra and Lagos again: both empty, verdicts recorded
- Enrich: Ranelagh wingnut best_time; 11 gaps recorded as dead ends
- Dublin +1: the Marlay Park Yew (dub_018); five verified trees held with reasons
- Photographs readers sent, queued for a look; vouched ones live
- Record when each page last changed
- Dublin verify: two Marlay Park trees staged, held for a photo
- Frankfurt +4 Naturdenkmal trees with German overlay; London claim released
- Braga and Setubal verify passes: nothing new, walls; leads kept
- Funchal scouting retried: still stalled, IFCN sheets already mined

**Photographs the night run approved** (1; the last column undoes one)

| Day | Tree | Where | Overrule |
|---|---|---|---|
| 10-30 | The Sycamore Maple of Parc Monceau | Paris | `photo_apply.py hold par_073` |

Machine: 8 chain attempts yesterday, 5 got real work time (~84 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c8/i19); /lisbon (c1/i7); /lisbon/giant-rubber-tree-of-mouraria (c1/i2); /montreal/mcgill-katsura (c1/i1); /seville (c1/i1)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'comfort tree niagara' (i2, p75)
    - '200 old tree trace' (i1, p54)
    - 'ancient roman trees' (i1, p68)
    - 'die 10 ältesten bäume der welt' (i1, p1)
    - 'drachenbaum auf teneriffa' (i1, p96)
    - 'drago milenario tree' (i1, p42)

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 342 |
| Clicks | 12 |
| Pages that got at least one impression | 206 |
| Impressions on the proven cities | 214 |

- 354 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3093 trees Google may index, 860 kept out for lacking a photo and an exact pin, 7047 pages on the noindex list.

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
| sequoia-national-park | 0 | 14 | 0.0% | 73.7 | 0.4% | general sherman tree (i4, p80) |

- Plus 258 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

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

