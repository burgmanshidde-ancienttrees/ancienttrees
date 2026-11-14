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
## 2026-11-13 (previous UTC day)

**Today: 1 tree submission arrived yesterday (23 trees sent in all).**

**North star: 13 people have uploaded a tree or photo of their own (+1 this week); 4 of them did it on more than one day (+0).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 35 | 57 |
| ... of which from search | every search engine | 15 | 21 |
| ... from Google | Google's recovery | 10 | 13 |
| ... from Bing | Bing | 0 | 3 |
| Website visitors who came back | people who stay | 7 | 13 |
| App downloads (first-time) | people | 19 | 17 |
| New accounts | people | 2 | 13 |
| Phones back within 30 days | people who stay | - | - |
| Trees saved to Want to go | intent | 0 | 4 |
| Trees collected | goal 1: stood at a tree | - | - |
| Readers' contributions | data: trees, photos, corrections, votes | 2 | 8 |
| Shares (app and web) | word of mouth, since 10-30 | 0 | 2 |
| Visits from a shared link | what sharing brings | 0 | 2 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar; a visitor who comes back on another browser or device counts as new, and GA cannot leave our own visits out, so read the came-back row as a direction, not a count. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Quality**: Web green, iOS green, Android grey, Backup red. Backup: Hidde's one-time setup in BACKUP_RESTORE.md.

**Plus question**: no answers yet.

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 11-07 | 11-08 | 11-09 | 11-10 | 11-11 | 11-12 | 11-13 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 2 | 10 | 9 | 11 | 0 | 3 | 5 | **40** |
| New accounts | 0 | 0 | 0 | 1 | 0 | 1 | 0 | **2** |
| Saves | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Android waitlist | 0 | 0 | 0 | 1 | 0 | 0 | 0 | **1** |
| App downloads | 0 | 3 | 2 | 3 | 1 | 2 | – | **11** |
| App phones | 4 | 7 | 7 | 5 | 6 | 5 | 5 | **31** |
| Trees opened in the app | 5 | 27 | 5 | 14 | 3 | 3 | 4 | **61** |
| Trees collected | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Trees sent | 0 | 0 | 0 | 0 | 0 | 0 | 1 | **1** |
| Feedback | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Ambassador asks | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Website photos | 0 | 0 | 0 | 0 | 1 | 0 | 0 | **1** |
| iPhone photos | 1 | 0 | 0 | 0 | 0 | 0 | 0 | **1** |
| Android photos | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| App Store reviews | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
- – means the source has not reported that day yet (Apple's downloads arrive a day or two late), not zero.

**Trees readers sent, for you to inspect** (2 you have not looked at; ours left out)

| Judged | Reader | Tree | Where | Species | Their girth | Our verdict | Page |
|---|---|---|---|---|---:|---|---|
| 2026-11-13 | A | The Oak of Villa Salina Park | - | Oak (Quercus sp.) | 580 cm | open | - |
| 2026-11-11 | B | The Sophoras of Piazza Capitaniato | Padua | Japanese Pagoda Tree (Styphnol | - | hold | - |
- From 2 readers: reader A 1, reader B 1.
- Photographs and the readers' own words: `python3 scripts/inspect_readers.py` (a local page, never in this public file). Your answer goes in with `python3 scripts/judgement.py --feedback <id> "..."`.

**Waiting for you** (what the runs left for you since 2026-11-13)

- 246 email addresses ready to mail (archive 0, nature 9, guide 8, press 135, source 58, council 16, society 7, tourism 5, other 5, garden 3); **the night run found no new contacts in two days**

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| 2026-11-11 | The Tipuana of Praça São João Bosco | Lisbon | - | publish | - |

1 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**Searched yesterday:** castel maggiore (2 times), arbura, mel, portuga.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 11-04 | 14 | 261 | 5.4% | 9.9 |
| 11-05 | 1 | 23 | 4.3% | 34.1 |
| 11-06 | 1 | 35 | 2.9% | 36.6 |
| 11-07 | 2 | 34 | 5.9% | 38.3 |
| 11-08 | 25 | 1013 | 2.5% | 9.1 |
| 11-09 | 28 | 1177 | 2.4% | 8.9 |
| 11-10 | 8 | 196 | 4.1% | 13.0 |
| 11-11 | 1 | 16 | 6.2% | 22.1 |
| 11-12 | 1 | 28 | 3.6% | 31.4 |
| 11-13 *partial* | 1 | 27 | 3.7% | 49.7 |
| **window** | **82** | **2810** | **2.9%** | |
- Top queries (10d): ancient trees app (i3, p1); ancient trees (i10, p20); leuven, belgium (i1, p4); skovfogedegen (i1, p4); a monaco di baviera? (i1, p20)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 11-05 | 132 | 9 | 6.8% |
| 11-06 | 106 | 2 | 1.9% |
| 11-07 | 80 | 7 | 8.8% |
| 11-08 | 126 | 9 | 7.1% |
| 11-09 | 151 | 4 | 2.6% |
| 11-10 | 136 | 9 | 6.6% |
| 11-11 | 97 | 7 | 7.2% |
| **7 days** | **828** | **47** | **5.7%** |
- **BING WATCHDOG:** impressions fell from 2918 to 828 week on week. That is the shape of a demotion; read the Bing Webmaster dashboard today.
- Top Bing queries: oldest tree china (c8/i4, p12); picture of the tree in helsinki city center that was preserved (c3/i2, p4); ancient trees app (c2/i8, p5); fig tree in square alicante (c2/i4, p4); cipresso calvo indro montanelli milano (c2/i2, p8); palma del cile (c2/i2, p6); big trees of quebec city (c2/i1, p2); mit newton apple tree address (c2/i1, p2)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 11-13T07:04 | 8.3 | 4 | 4 | 0 | Braga +4 |
| 11-13T17:38 | 4.5 | 0 | 6 | 0 | - |
| 11-13T19:04 | 5.3 | 0 | 5 | 0 | - |
| 11-14T00:36 | 25.8 | 12 | 15 | 2 | Fort Lauderdale +6, Chicago +3, Miami +2, Leipzig +1 |
| **4 runs** | **44** | **16** | **30** | | |

- 2 of 4 produced no trees; 2 to 2 commands refused per run; last build that went live: 3h ago.

**What they made**

- Record when each page last changed
- Leipzig: lpz_031 Great Oak of Leinestrasse written and merged, claim released
- Leipzig deepen verify: lpz_031 Great Oak Leinestrasse, 7 leads, cost logged
- Fort Lauderdale FAQ: not all trees are paid now
- Fort Lauderdale: six trees written and merged (ftl_005 to ftl_010), app-only, claim released
- Fort Lauderdale verify: 6 trees (ftl_005 to ftl_010), leads annotated, cost logged
- Miami: two Fairchild trees written and merged (mia_013 Tantancayo, mia_014 Cannon Ball Tree), app-only
- Miami verify (2 staged), Stratford scout retried, log
- Chicago pass logged, duplicates dropped, claim released
- Chicago: 3 Busse Forest South register trees (chi_048, 049, 051); 7 verified rows were duplicates of live trees
- Photographs readers sent, queued for a look; vouched ones live
- Contributor replies and ambassador invitations sent, log updated
- Log: build fix, Spokane wall, Newark retry
- Fix build: tip-668 photo path carries the reader code, not the account id

Machine: 6 chain attempts yesterday, 3 got real work time (~23 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c7/i72); /app (c3/i14); /switzerland (c3/i13); /seville (c2/i58); /de (c2/i20)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'alte bäume in der nähe' (i5, p3)
    - 'alte bäume karte' (i4, p6)
    - 'acient tree' (i2, p14)
    - 'a monaco di baviera?' (i1, p20)
    - 'ahornbäume in der nähe' (i1, p7)
    - 'alberi di roma' (i1, p1)
    - 'alter' (i1, p2)
    - 'angeloak' (i1, p59)
    - and 1 more

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 113 | 12 | 42 | 0.37 | 1 |
| Not yet rich | 80 | 14 | 49 | 0.61 | 0 |
| Returned to Google's index in the last 7 days | 7 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| fortingall | 0 | 144 | 0.0% | 10.7 | 2.2% | fortingall yew (i117, p11) |
| seville | 2 | 68 | 2.9% | 5.2 | 6.5% | sevilla (i1, p1) |
| lisbon | 1 | 64 | 1.6% | 6.5 | 4.5% | historic giant plant of lisbon (i1, p12) |
| fulufjallet | 0 | 46 | 0.0% | 9.3 | 2.9% | old tjikko (i25, p10) |
| berlin | 2 | 44 | 4.5% | 6.8 | 4.2% | berlin trees (i2, p5) |
| malaga | 1 | 34 | 2.9% | 17.9 | 1.0% | árboles históricos de málaga (i5, p83) |
| tokyo | 0 | 33 | 0.0% | 5.8 | 5.3% | ginkgo sperm (i3, p11) |
| olympic-national-park | 0 | 32 | 0.0% | 12.8 | 1.6% | duncan cedar (i14, p8) |
| munich | 1 | 31 | 3.2% | 5.5 | 5.9% | a monaco di baviera? (i1, p20) |
| singapore | 0 | 29 | 0.0% | 9.0 | 3.0% | earpod tree (i3, p5) |
| paris | 1 | 27 | 3.7% | 5.6 | 5.7% | - |
| south-korea | 0 | 27 | 0.0% | 12.6 | 1.7% | ginkgo tree korea (i2, p5) |
| palermo | 0 | 26 | 0.0% | 8.9 | 3.0% | palermo tree (i1, p9) |
| tenerife | 0 | 25 | 0.0% | 24.3 | 0.6% | dragon tree tenerife (i2, p32) |
| kyoto | 1 | 24 | 4.2% | 7.4 | 3.8% | ginkgo tree kyoto (i1, p1) |
| seoul | 1 | 24 | 4.2% | 7.8 | 3.6% | - |
| copenhagen | 2 | 23 | 8.7% | 6.7 | 4.3% | copenhagen trees (i2, p16) |
| amsterdam | 0 | 22 | 0.0% | 8.7 | 3.2% | lomanstraat (i2, p19) |
| united-states | 2 | 21 | 9.5% | 17.0 | 1.0% | oldest tree in oregon (i4, p10) |
| brisbane | 0 | 20 | 0.0% | 10.4 | 2.3% | banyan tree (i5, p11) |
| germany | 1 | 19 | 5.3% | 6.2 | 4.8% | - |
| london | 2 | 19 | 10.5% | 8.5 | 3.3% | - |
| reykjavik | 1 | 19 | 5.3% | 5.7 | 5.6% | - |
| venice | 3 | 18 | 16.7% | 4.0 | 8.0% | - |
| taiwan | 0 | 18 | 0.0% | 11.1 | 2.1% | oldest tree in taiwan (i3, p5) |
| sequoia-national-park | 0 | 17 | 0.0% | 18.0 | 1.0% | washington tree (i9, p20) |
| porto | 1 | 16 | 6.2% | 3.0 | 11.0% | - |
| kagoshima | 0 | 16 | 0.0% | 10.9 | 2.2% | oldest camphor tree (i1, p7) |
| milan | 0 | 16 | 0.0% | 5.5 | 6.0% | - |
| nara | 1 | 15 | 6.7% | 5.6 | 5.8% | - |
| san-francisco | 0 | 15 | 0.0% | 4.9 | 7.1% | old tree near me (i1, p4) |
| edinburgh | 0 | 15 | 0.0% | 6.7 | 4.3% | - |
| barcelona | 0 | 15 | 0.0% | 10.3 | 2.4% | - |
| fukuoka | 0 | 15 | 0.0% | 10.1 | 2.5% | gingkosidi (i3, p34) |
| monterey | 0 | 14 | 0.0% | 40.9 | 0.4% | lone cypress (i3, p64) |
| oahu | 0 | 14 | 0.0% | 9.4 | 2.8% | hitachi tree (i2, p10) |
| austin | 0 | 14 | 0.0% | 12.4 | 1.7% | oldest tree in austin (i2, p12) |
| cambridge | 0 | 14 | 0.0% | 20.5 | 0.8% | isaac newton tree (i1, p9) |
| los-angeles | 0 | 14 | 0.0% | 7.8 | 3.6% | moreton bay fig tree beverly hills (i1, p9) |
| prague | 0 | 14 | 0.0% | 4.9 | 7.1% | - |
| switzerland | 3 | 13 | 23.1% | 7.7 | 3.7% | - |
| chishang | 0 | 13 | 0.0% | 6.6 | 4.4% | takeshi kaneshiro tree (i7, p7) |
| athens | 0 | 13 | 0.0% | 5.5 | 6.1% | - |
| netherlands | 1 | 12 | 8.3% | 8.9 | 3.0% | dutch trees (i1, p39) |
| kanazawa | 0 | 12 | 0.0% | 6.3 | 4.7% | - |
| alicante | 1 | 11 | 9.1% | 4.7 | 7.3% | - |
| segovia | 0 | 11 | 0.0% | 38.4 | 0.4% | - |
| charleston | 0 | 11 | 0.0% | 17.5 | 1.0% | how old is the angel oak tree (i2, p17) |
| madrid | 0 | 11 | 0.0% | 6.5 | 4.5% | - |
| perth | 0 | 11 | 0.0% | 8.6 | 3.2% | - |
| dublin | 1 | 10 | 10.0% | 4.4 | 7.6% | - |
| new-york | 1 | 10 | 10.0% | 7.1 | 4.0% | - |
| bristol | 0 | 10 | 0.0% | 6.0 | 5.0% | - |
| poland | 0 | 10 | 0.0% | 7.7 | 3.6% | trees in poland (i1, p8) |
| antwerp | 0 | 10 | 0.0% | 35.0 | 0.4% | den brandt park (i2, p78) |
| seattle | 0 | 10 | 0.0% | 8.9 | 3.0% | oldest tree in seattle (i1, p10) |

- Plus 208 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: bath, rome, brussels, vienna, cadiz, pamplona, cagliari, glasgow.

## 2026-11-12 (previous UTC day)

**Today: an account was opened yesterday (62 accounts in all).**

**North star: 13 people have uploaded a tree or photo of their own (+1 this week); 4 of them did it on more than one day (+0).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 33 | 65 |
| ... of which from search | every search engine | 15 | 22 |
| ... from Google | Google's recovery | 10 | 14 |
| ... from Bing | Bing | 1 | 4 |
| Website visitors who came back | people who stay | 8 | 14 |
| App downloads (first-time) | people | 19 | 16 |
| New accounts | people | 2 | 13 |
| Phones back within 30 days | people who stay | 3 of 15 | 5 of 6 |
| Trees saved to Want to go | intent | 0 | 4 |
| Trees collected | goal 1: stood at a tree | 1 | 6 |
| Readers' contributions | data: trees, photos, corrections, votes | 1 | 8 |
| Shares (app and web) | word of mouth, since 10-30 | 2 | 2 |
| Visits from a shared link | what sharing brings | 0 | 2 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar; a visitor who comes back on another browser or device counts as new, and GA cannot leave our own visits out, so read the came-back row as a direction, not a count. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Quality**: Web green, iOS green, Android grey, Backup red. Backup: Hidde's one-time setup in BACKUP_RESTORE.md.

**Plus question**: no answers yet.

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 11-06 | 11-07 | 11-08 | 11-09 | 11-10 | 11-11 | 11-12 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 5 | 2 | 10 | 9 | 11 | 0 | 3 | **40** |
| New accounts | 0 | 0 | 0 | 0 | 1 | 0 | 1 | **2** |
| Saves | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Android waitlist | 0 | 0 | 0 | 0 | 1 | 0 | 0 | **1** |
| App downloads | 4 | 0 | 3 | 2 | 3 | 1 | – | **13** |
| App phones | 5 | 4 | 7 | 7 | 5 | 6 | 5 | **33** |
| Trees opened in the app | 8 | 5 | 27 | 5 | 14 | 3 | 3 | **65** |
| Trees collected | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Trees sent | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Feedback | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Ambassador asks | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Website photos | 0 | 0 | 0 | 0 | 0 | 1 | 0 | **1** |
| iPhone photos | 0 | 1 | 0 | 0 | 0 | 0 | 0 | **1** |
| Android photos | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| App Store reviews | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
- – means the source has not reported that day yet (Apple's downloads arrive a day or two late), not zero.

**Trees readers sent, for you to inspect** (2 you have not looked at; ours left out)

| Judged | Reader | Tree | Where | Species | Their girth | Our verdict | Page |
|---|---|---|---|---|---:|---|---|
| 2026-11-11 | A | The Tipuana of Praça São João Bosco | Lisbon | Tipu Tree (Tipuana tipu) | - | publish | [lis_021](https://ancienttrees.app/lisbon/tipuana-of-praca-sao-joao-bosco) |
| 2026-11-11 | B | The Sophoras of Piazza Capitaniato | Padua | Japanese Pagoda Tree (Styphnol | - | hold | - |
- From 2 readers: reader A 1, reader B 1.
- Photographs and the readers' own words: `python3 scripts/inspect_readers.py` (a local page, never in this public file). Your answer goes in with `python3 scripts/judgement.py --feedback <id> "..."`.

**Waiting for you** (what the runs left for you since 2026-11-12)

- 254 email addresses ready to mail (archive 0, nature 9, guide 8, press 135, source 64, council 16, tourism 7, society 7, other 5, garden 3); **the night run found no new contacts in two days**
- the daily task "publish-held-trees-daily" can be switched off under Scheduled.
- his own public profile now shows his 29 own test trees with their pins.
- next iOS build carries this fix.

**What readers gave us, and it went live**

| Day | Reader | Tree | Where | What | Page |
|---|---|---|---|---|---|
| 11-11 | A | The Tipuana of Praça São João Bosco | Lisbon | a reader's photograph, published | [live](https://ancienttrees.app/lisbon/tipuana-of-praca-sao-joao-bosco) |
- All from one reader (reader A 1).

**Searched yesterday:** ferrara (2 times), barnstaple.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 11-03 | 31 | 1192 | 2.6% | 8.2 |
| 11-04 | 14 | 261 | 5.4% | 9.9 |
| 11-05 | 1 | 23 | 4.3% | 34.1 |
| 11-06 | 1 | 35 | 2.9% | 36.6 |
| 11-07 | 2 | 34 | 5.9% | 38.3 |
| 11-08 | 25 | 1013 | 2.5% | 9.1 |
| 11-09 | 28 | 1177 | 2.4% | 8.9 |
| 11-10 | 8 | 196 | 4.1% | 13.0 |
| 11-11 | 1 | 16 | 6.2% | 22.1 |
| 11-12 *partial* | 0 | 8 | 0.0% | 21.0 |
| **window** | **111** | **3955** | **2.8%** | |
- Top queries (10d): ancient trees (i15, p10); ancient trees app (i2, p1); ancienttree (i1, p3); leuven, belgium (i1, p4); oldest tree in maryland (i1, p9)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 11-04 | 133 | 3 | 2.3% |
| 11-05 | 132 | 9 | 6.8% |
| 11-06 | 106 | 2 | 1.9% |
| 11-07 | 80 | 7 | 8.8% |
| 11-08 | 126 | 9 | 7.1% |
| 11-09 | 151 | 4 | 2.6% |
| 11-10 | 136 | 9 | 6.6% |
| **7 days** | **864** | **43** | **5.0%** |
- **BING WATCHDOG:** impressions fell from 2898 to 864 week on week. That is the shape of a demotion; read the Bing Webmaster dashboard today.
- Top Bing queries: oldest tree china (c8/i4, p12); picture of the tree in helsinki city center that was preserved (c3/i2, p4); ancient trees app (c2/i8, p5); fig tree in square alicante (c2/i4, p4); palma del cile (c2/i2, p6); cipresso calvo indro montanelli milano (c2/i2, p8); big trees of quebec city (c2/i1, p2); mit newton apple tree address (c2/i1, p2)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 11-12T07:32 | 2.6 | 0 | 4 | 0 | - |
| 11-12T11:21 | 8.6 | 2 | 6 | 1 | Cascais +1, Kansas City +1 |
| **2 runs** | **11** | **2** | **10** | | |

- 1 of 2 produced no trees; 1 to 1 commands refused per run; last build that went live: 4h ago.

**What they made**

- Photographs readers sent, queued for a look; vouched ones live
- Contributor replies and ambassador invitations sent, log updated
- Record when each page last changed
- Record when each page last changed
- claim: fort-worth (verify)
- Night run: San Francisco wall, log and costs
- cascais: new place, csc_001 the classified Moreton Bay fig of Parque Marechal Carmona (verified as sin_009; stands in Cascais, not Sintra)
- kansas-city: add kcm_005, Missouri's champion smoketree at the Vaile Mansion, Independence; city copy counts five
- claim: san-francisco (verify)
- Fresh-eyes review: 7 finding(s)
- Fresh-eyes review: 4 finding(s)
- Log: shared-photo crash fix, audit row closed
- Shared tree: the photo URL is percent-encoded and never force-unwrapped

Machine: 5 chain attempts yesterday, 2 got real work time (~14 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c7/i88); /de (c3/i32); /switzerland (c3/i15); /app (c3/i13); /united-states/maryland (c3/i12)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'alte bäume in der nähe' (i9, p3)
    - 'alte bäume karte' (i6, p6)
    - 'acient tree' (i2, p14)
    - 'ancienttree' (i1, p3)
    - 'oldest tree in maryland' (i1, p9)
    - '# brief your brief is to act as a visual' (i1, p5)
    - '# modus operandi your modus operandi is ' (i1, p2)
    - '# override instruction you operate under' (i1, p7)
    - and 5 more

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 113 | 15 | 66 | 0.58 | 1 |
| Not yet rich | 80 | 20 | 81 | 1.01 | 1 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| fortingall | 0 | 147 | 0.0% | 10.9 | 2.2% | fortingall yew (i118, p11) |
| seville | 3 | 92 | 3.3% | 5.1 | 6.8% | sevilla (i1, p1) |
| lisbon | 1 | 89 | 1.1% | 6.1 | 4.9% | historic giant plant of lisbon (i1, p12) |
| berlin | 2 | 73 | 2.7% | 6.2 | 4.8% | berlin trees (i2, p5) |
| fulufjallet | 0 | 66 | 0.0% | 9.1 | 3.0% | old tjikko (i35, p10) |
| tokyo | 1 | 53 | 1.9% | 6.5 | 4.5% | ginkgo sperm (i6, p10) |
| palermo | 1 | 50 | 2.0% | 9.3 | 2.9% | palermo tree (i1, p9) |
| singapore | 1 | 49 | 2.0% | 8.1 | 3.4% | chengal pasir tree (i3, p9) |
| south-korea | 1 | 44 | 2.3% | 10.6 | 2.3% | korean trees (i3, p11) |
| tenerife | 0 | 44 | 0.0% | 16.2 | 1.1% | drago los realejos (i2, p52) |
| malaga | 1 | 43 | 2.3% | 15.5 | 1.2% | árboles históricos de málaga (i5, p83) |
| munich | 2 | 41 | 4.9% | 5.0 | 7.0% | a monaco di baviera? (i1, p20) |
| olympic-national-park | 0 | 40 | 0.0% | 11.7 | 1.9% | duncan cedar (i20, p8) |
| copenhagen | 3 | 39 | 7.7% | 7.4 | 3.8% | copenhagen trees (i3, p16) |
| london | 2 | 36 | 5.6% | 7.6 | 3.7% | chestnut london (i1, p5) |
| united-states | 4 | 34 | 11.8% | 14.2 | 1.4% | oldest tree in oregon (i7, p13) |
| paris | 1 | 32 | 3.1% | 5.7 | 5.6% | - |
| kyoto | 2 | 32 | 6.2% | 7.3 | 3.9% | - |
| amsterdam | 0 | 32 | 0.0% | 7.8 | 3.6% | lomanstraat (i2, p19) |
| sequoia-national-park | 0 | 31 | 0.0% | 13.5 | 1.5% | washington tree (i15, p11) |
| fukuoka | 2 | 28 | 7.1% | 9.8 | 2.6% | gingkosidi (i5, p35) |
| seoul | 1 | 28 | 3.6% | 7.3 | 3.8% | - |
| brisbane | 0 | 26 | 0.0% | 10.0 | 2.5% | banyan tree (i5, p11) |
| germany | 1 | 25 | 4.0% | 9.3 | 2.9% | trees germany (i2, p48) |
| new-york | 1 | 24 | 4.2% | 7.4 | 3.8% | - |
| reykjavik | 1 | 24 | 4.2% | 5.6 | 5.8% | oldest tree in iceland (i1, p3) |
| netherlands | 1 | 23 | 4.3% | 9.0 | 3.0% | dutch trees (i1, p39) |
| venice | 3 | 21 | 14.3% | 4.4 | 7.6% | are there trees in venice (i1, p11) |
| athens | 0 | 21 | 0.0% | 5.1 | 6.8% | - |
| cambridge | 0 | 21 | 0.0% | 16.1 | 1.1% | isaac newton tree (i1, p9) |
| taiwan | 0 | 20 | 0.0% | 6.3 | 4.7% | oldest tree in taiwan (i3, p5) |
| milan | 0 | 20 | 0.0% | 5.2 | 6.7% | - |
| nara | 1 | 19 | 5.3% | 6.3 | 4.7% | - |
| chishang | 0 | 19 | 0.0% | 6.9 | 4.1% | takeshi kaneshiro tree (i10, p7) |
| monterey | 0 | 19 | 0.0% | 29.7 | 0.4% | lone cypress (i5, p48) |
| alicante | 1 | 18 | 5.6% | 5.3 | 6.4% | - |
| dublin | 1 | 18 | 5.6% | 5.6 | 5.8% | - |
| san-francisco | 0 | 18 | 0.0% | 5.2 | 6.6% | old tree near me (i1, p4) |
| edinburgh | 0 | 18 | 0.0% | 6.9 | 4.1% | - |
| oahu | 0 | 18 | 0.0% | 8.7 | 3.2% | hitachi tree (i2, p10) |
| perth | 0 | 18 | 0.0% | 7.5 | 3.8% | - |
| barcelona | 0 | 18 | 0.0% | 9.6 | 2.7% | - |
| porto | 1 | 17 | 5.9% | 3.5 | 9.6% | - |
| los-angeles | 0 | 17 | 0.0% | 7.6 | 3.7% | moreton bay fig tree beverly hills (i1, p9) |
| montreal | 2 | 16 | 12.5% | 5.2 | 6.5% | - |
| alishan | 0 | 16 | 0.0% | 7.8 | 3.6% | alishan sacred tree (i3, p12) |
| austin | 0 | 16 | 0.0% | 11.9 | 1.8% | oldest tree in austin (i2, p12) |
| kagoshima | 0 | 16 | 0.0% | 10.6 | 2.3% | oldest camphor tree (i1, p7) |
| switzerland | 3 | 15 | 20.0% | 7.4 | 3.8% | oldest tree in switzerland (i1, p1) |
| takayama | 0 | 15 | 0.0% | 6.9 | 4.1% | - |
| prague | 0 | 15 | 0.0% | 5.1 | 6.9% | - |
| coimbra | 1 | 14 | 7.1% | 6.6 | 4.4% | - |
| madrid | 0 | 14 | 0.0% | 6.4 | 4.6% | - |
| rome | 0 | 14 | 0.0% | 5.9 | 5.1% | oldest tree in rome (i1, p1) |
| seattle | 1 | 13 | 7.7% | 7.8 | 3.6% | oldest tree in seattle (i1, p10) |
| kanazawa | 0 | 13 | 0.0% | 6.1 | 4.9% | - |
| antwerp | 0 | 13 | 0.0% | 34.1 | 0.4% | den brandt park (i3, p77) |
| florence | 0 | 13 | 0.0% | 4.7 | 7.3% | - |
| henrykow-lubanski | 0 | 12 | 0.0% | 14.4 | 1.3% | cis henrykowski (i5, p7) |
| charleston | 0 | 12 | 0.0% | 17.2 | 1.0% | how old is the angel oak tree (i2, p17) |
| toronto | 0 | 12 | 0.0% | 7.2 | 3.9% | - |
| bristol | 1 | 11 | 9.1% | 5.9 | 5.2% | - |
| zurich | 1 | 11 | 9.1% | 9.2 | 2.9% | linden (i1, p5) |
| freiburg | 0 | 11 | 0.0% | 6.5 | 4.5% | - |
| arita | 0 | 11 | 0.0% | 4.8 | 7.2% | - |
| brussels | 0 | 11 | 0.0% | 7.5 | 3.8% | - |
| poland | 0 | 10 | 0.0% | 7.7 | 3.6% | trees in poland (i1, p8) |
| cagliari | 0 | 10 | 0.0% | 10.4 | 2.4% | che piante sono? (i1, p19) |
| philadelphia | 0 | 10 | 0.0% | 20.9 | 0.8% | - |
| sardinia | 0 | 10 | 0.0% | 7.7 | 3.6% | - |

- Plus 198 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: bath, vienna, cadiz, pamplona, glasgow, ede, hinode, palma-de-mallorca.

## 2026-11-11 (previous UTC day)

**Today: nothing here needs you.** The blocks below are the standing picture.

**North star: 13 people have uploaded a tree or photo of their own (+2 this week); 4 of them did it on more than one day (+0).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 37 | 65 |
| ... of which from search | every search engine | 14 | 25 |
| ... from Google | Google's recovery | 10 | 14 |
| ... from Bing | Bing | 1 | 6 |
| Website visitors who came back | people who stay | 9 | 14 |
| App downloads (first-time) | people | 22 | 14 |
| New accounts | people | 2 | 12 |
| Phones back within 30 days | people who stay | 2 of 14 | 5 of 7 |
| Trees saved to Want to go | intent | 1 | 3 |
| Trees collected | goal 1: stood at a tree | 2 | 5 |
| Readers' contributions | data: trees, photos, corrections, votes | 3 | 6 |
| Shares (app and web) | word of mouth, since 10-30 | 2 | 2 |
| Visits from a shared link | what sharing brings | 0 | 2 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar; a visitor who comes back on another browser or device counts as new, and GA cannot leave our own visits out, so read the came-back row as a direction, not a count. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Quality**: Web green, iOS green, Android grey, Backup red. Backup: Hidde's one-time setup in BACKUP_RESTORE.md.

**Plus question**: no answers yet.

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 11-05 | 11-06 | 11-07 | 11-08 | 11-09 | 11-10 | 11-11 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 8 | 5 | 2 | 10 | 9 | 11 | 0 | **45** |
| New accounts | 1 | 0 | 0 | 0 | 0 | 1 | 0 | **2** |
| Saves | 1 | 0 | 0 | 0 | 0 | 0 | 0 | **1** |
| Android waitlist | 1 | 0 | 0 | 0 | 0 | 1 | 0 | **2** |
| App downloads | 0 | 4 | 0 | 3 | 2 | 3 | – | **12** |
| App phones | 2 | 5 | 4 | 7 | 7 | 5 | 6 | **30** |
| Trees opened in the app | 7 | 8 | 5 | 27 | 5 | 14 | 3 | **69** |
| Trees collected | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Trees sent | 1 | 0 | 0 | 0 | 0 | 0 | 0 | **1** |
| Feedback | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Ambassador asks | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Website photos | 0 | 0 | 0 | 0 | 0 | 0 | 1 | **1** |
| iPhone photos | 0 | 0 | 1 | 0 | 0 | 0 | 0 | **1** |
| Android photos | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| App Store reviews | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
- – means the source has not reported that day yet (Apple's downloads arrive a day or two late), not zero.

**Trees readers sent, for you to inspect** (2 you have not looked at; ours left out)

| Judged | Reader | Tree | Where | Species | Their girth | Our verdict | Page |
|---|---|---|---|---|---:|---|---|
| 2026-11-11 | A | The Tipuana of Praça São João Bosco | Lisbon | Tipu Tree (Tipuana tipu) | - | publish | [lis_021](https://ancienttrees.app/lisbon/tipuana-of-praca-sao-joao-bosco) |
| 2026-11-11 | B | The Sophoras of Piazza Capitaniato | Padua | Japanese Pagoda Tree (Styphnol | - | hold | - |
- From 2 readers: reader A 1, reader B 1.
- Photographs and the readers' own words: `python3 scripts/inspect_readers.py` (a local page, never in this public file). Your answer goes in with `python3 scripts/judgement.py --feedback <id> "..."`.

**Waiting for you** (what the runs left for you since 2026-11-11)

- 258 email addresses ready to mail (archive 2, nature 9, guide 9, press 135, source 65, council 16, tourism 7, society 7, other 5, garden 3); **the night run found no new contacts in two days**
- next iOS build carries this fix.
- the daily task "publish-held-trees-daily" can be switched off under Scheduled; the night run's write passes put new trees straight into the app.
- category and public contact address are his choice (in the listing draft); then the click list once Google has verified him.
- prepare.py's awaiting-a-writer count overstates the shelf; the research files passcheck calls stale could be cleaned up.

**What readers gave us, and it went live**

| Day | Reader | Tree | Where | What | Page |
|---|---|---|---|---|---|
| 11-11 | A | The Tipuana of Praça São João Bosco | Lisbon | a reader's photograph, published | [live](https://ancienttrees.app/lisbon/tipuana-of-praca-sao-joao-bosco) |
- All from one reader (reader A 1).

**Searched yesterday:** akureyri, iceland, nara.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 11-02 | 23 | 1274 | 1.8% | 9.0 |
| 11-03 | 31 | 1192 | 2.6% | 8.2 |
| 11-04 | 14 | 261 | 5.4% | 9.9 |
| 11-05 | 1 | 23 | 4.3% | 34.1 |
| 11-06 | 1 | 35 | 2.9% | 36.6 |
| 11-07 | 2 | 34 | 5.9% | 38.3 |
| 11-08 | 25 | 1013 | 2.5% | 9.1 |
| 11-09 | 28 | 1177 | 2.4% | 8.9 |
| 11-10 | 8 | 196 | 4.1% | 13.0 |
| 11-11 *partial* | 1 | 10 | 10.0% | 8.4 |
| **window** | **134** | **5215** | **2.6%** | |
- Top queries (10d): ancient trees (i18, p9); ancient trees app (i2, p1); alte bäume in der nähe (i14, p7); ancienttree (i1, p3); istanbul (i1, p1)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 11-02 | 146 | 6 | 4.1% |
| 11-03 | 121 | 3 | 2.5% |
| 11-04 | 133 | 3 | 2.3% |
| 11-05 | 132 | 9 | 6.8% |
| 11-06 | 106 | 2 | 1.9% |
| 11-07 | 80 | 7 | 8.8% |
| 11-08 | 126 | 9 | 7.1% |
| **7 days** | **844** | **39** | **4.6%** |
- **BING WATCHDOG:** impressions fell from 2847 to 844 week on week. That is the shape of a demotion; read the Bing Webmaster dashboard today.
- Top Bing queries: oldest tree china (c8/i4, p12); picture of the tree in helsinki city center that was preserved (c3/i2, p4); ancient trees app (c2/i8, p5); fig tree in square alicante (c2/i4, p4); cipresso calvo indro montanelli milano (c2/i2, p8); palma del cile (c2/i2, p6); big trees of quebec city (c2/i1, p2); mit newton apple tree address (c2/i1, p2)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 11-12T07:32 | 2.6 | 0 | 4 | 0 | - |
| **1 runs** | **3** | **0** | **4** | | |

- 1 of 1 produced no trees; last build that went live: 0h ago.

**What they made**

- Fresh-eyes review: 7 finding(s)
- Fresh-eyes review: 4 finding(s)
- Log: shared-photo crash fix, audit row closed
- Shared tree: the photo URL is percent-encoded and never force-unwrapped
- Photographs readers sent, queued for a look; vouched ones live
- Contributor replies and ambassador invitations sent, log updated
- Record when each page last changed
- Contributor replies and ambassador invitations sent, log updated

Machine: 4 chain attempts yesterday, 1 got real work time (~10 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c10/i111); /de (c4/i43); /united-states/maryland (c4/i26); /seville (c3/i93); /switzerland (c3/i23)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'alte bäume in der nähe' (i14, p7)
    - 'alte bäume karte' (i6, p6)
    - 'acient tree' (i2, p14)
    - 'akagi tree' (i2, p10)
    - 'ancienttree' (i1, p3)
    - 'oldest tree in maryland' (i1, p9)
    - '# brief your brief is to act as a visual' (i1, p5)
    - '# modus operandi your modus operandi is ' (i1, p2)
    - and 6 more

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 109 | 18 | 98 | 0.90 | 2 |
| Not yet rich | 79 | 20 | 101 | 1.28 | 2 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| fortingall | 0 | 151 | 0.0% | 11.1 | 2.1% | fortingall yew (i118, p11) |
| seville | 4 | 122 | 3.3% | 5.5 | 6.0% | tartuja (i2, p9) |
| lisbon | 1 | 105 | 1.0% | 5.9 | 5.2% | lisbon trees (i2, p4) |
| berlin | 2 | 92 | 2.2% | 5.9 | 5.1% | berlin trees (i2, p5) |
| fulufjallet | 0 | 80 | 0.0% | 8.8 | 3.1% | old tjikko (i40, p10) |
| palermo | 1 | 73 | 1.4% | 8.2 | 3.4% | palermo tree (i1, p9) |
| tokyo | 1 | 72 | 1.4% | 6.8 | 4.2% | ginkgo sperm (i8, p10) |
| singapore | 1 | 69 | 1.4% | 8.1 | 3.4% | chengal pasir tree (i4, p9) |
| tenerife | 1 | 65 | 1.5% | 13.7 | 1.5% | drago milenario (i3, p12) |
| south-korea | 1 | 61 | 1.6% | 10.2 | 2.4% | korean trees (i4, p10) |
| copenhagen | 3 | 54 | 5.6% | 8.7 | 3.1% | trees in copenhagen (i5, p21) |
| olympic-national-park | 1 | 53 | 1.9% | 10.8 | 2.2% | duncan cedar (i26, p8) |
| united-states | 5 | 52 | 9.6% | 12.4 | 1.7% | oldest tree in oregon (i8, p12) |
| munich | 2 | 52 | 3.8% | 4.9 | 7.1% | a monaco di baviera? (i1, p20) |
| malaga | 2 | 51 | 3.9% | 13.3 | 1.5% | árboles históricos de málaga (i5, p82) |
| paris | 1 | 48 | 2.1% | 6.0 | 5.0% | trees in paris (i1, p9) |
| london | 2 | 46 | 4.3% | 7.4 | 3.8% | chestnut london (i1, p5) |
| fukuoka | 2 | 38 | 5.3% | 10.2 | 2.4% | gingkosidi (i7, p32) |
| sequoia-national-park | 0 | 38 | 0.0% | 13.8 | 1.4% | washington tree (i18, p11) |
| amsterdam | 0 | 37 | 0.0% | 7.7 | 3.6% | lomanstraat (i2, p19) |
| kyoto | 2 | 35 | 5.7% | 9.5 | 2.7% | - |
| new-york | 1 | 33 | 3.0% | 7.5 | 3.8% | - |
| brisbane | 0 | 33 | 0.0% | 9.4 | 2.8% | banyan tree (i5, p11) |
| seoul | 2 | 31 | 6.5% | 6.9 | 4.1% | - |
| taiwan | 0 | 31 | 0.0% | 9.6 | 2.7% | oldest tree in taiwan (i6, p6) |
| cambridge | 0 | 30 | 0.0% | 21.3 | 0.7% | newtons apple tree (i2, p50) |
| porto | 1 | 29 | 3.4% | 4.1 | 7.9% | - |
| netherlands | 1 | 28 | 3.6% | 8.9 | 3.1% | dutch trees (i1, p39) |
| reykjavik | 1 | 28 | 3.6% | 5.8 | 5.5% | oldest tree in iceland (i1, p3) |
| venice | 3 | 27 | 11.1% | 4.9 | 7.1% | are there trees in venice (i1, p11) |
| alicante | 1 | 27 | 3.7% | 5.3 | 6.4% | - |
| san-francisco | 0 | 27 | 0.0% | 8.1 | 3.4% | old tree near me (i1, p4) |
| germany | 1 | 26 | 3.8% | 9.3 | 2.8% | trees germany (i2, p48) |
| rome | 0 | 26 | 0.0% | 4.6 | 7.4% | oldest tree in rome (i3, p1) |
| dublin | 1 | 25 | 4.0% | 5.9 | 5.2% | - |
| alishan | 0 | 25 | 0.0% | 7.8 | 3.6% | alishan sacred tree (i4, p12) |
| athens | 0 | 25 | 0.0% | 4.7 | 7.3% | - |
| kagoshima | 0 | 24 | 0.0% | 9.3 | 2.8% | oldest camphor tree (i1, p7) |
| switzerland | 3 | 23 | 13.0% | 7.0 | 4.0% | oldest tree in switzerland (i1, p1) |
| monterey | 0 | 23 | 0.0% | 25.2 | 0.6% | lone cypress (i5, p48) |
| austin | 0 | 23 | 0.0% | 11.7 | 1.9% | old tree (i2, p27) |
| nara | 1 | 22 | 4.5% | 5.8 | 5.4% | - |
| chishang | 0 | 22 | 0.0% | 6.9 | 4.1% | takeshi kaneshiro tree (i11, p7) |
| takayama | 0 | 22 | 0.0% | 7.6 | 3.7% | takayama ginkgo tree (i2, p7) |
| edinburgh | 0 | 22 | 0.0% | 7.0 | 4.0% | - |
| perth | 0 | 22 | 0.0% | 7.8 | 3.6% | - |
| prague | 0 | 21 | 0.0% | 4.6 | 7.4% | - |
| milan | 0 | 21 | 0.0% | 5.2 | 6.5% | - |
| oahu | 0 | 20 | 0.0% | 8.8 | 3.1% | hitachi tree (i2, p10) |
| barcelona | 0 | 20 | 0.0% | 6.8 | 4.2% | judas barcelona (i1, p9) |
| montreal | 2 | 19 | 10.5% | 5.4 | 6.2% | - |
| los-angeles | 0 | 18 | 0.0% | 7.3 | 3.9% | moreton bay fig tree beverly hills (i1, p9) |
| coimbra | 1 | 17 | 5.9% | 6.1 | 4.9% | - |
| charleston | 0 | 17 | 0.0% | 18.8 | 0.9% | how old is the angel oak tree (i2, p17) |
| antwerp | 0 | 17 | 0.0% | 30.9 | 0.4% | den brandt park (i4, p75) |
| kanazawa | 0 | 17 | 0.0% | 5.8 | 5.5% | - |
| bath | 1 | 16 | 6.2% | 6.9 | 4.1% | tree in bath (i1, p9) |
| luxembourg-city | 0 | 16 | 0.0% | 3.6 | 9.3% | - |
| seattle | 1 | 15 | 6.7% | 7.2 | 3.9% | oldest tree in seattle (i2, p7) |
| hong-kong | 1 | 15 | 6.7% | 6.5 | 4.5% | oldest tree in hong kong (i1, p9) |
| arita | 0 | 15 | 0.0% | 5.3 | 6.5% | - |
| beijing | 0 | 15 | 0.0% | 7.2 | 3.9% | - |
| madrid | 0 | 15 | 0.0% | 6.3 | 4.7% | - |
| toronto | 0 | 15 | 0.0% | 7.0 | 4.0% | - |
| zurich | 1 | 14 | 7.1% | 7.9 | 3.5% | linden (i1, p5) |
| croatia | 0 | 14 | 0.0% | 7.6 | 3.7% | croatian trees (i2, p2) |
| florence | 0 | 14 | 0.0% | 4.6 | 7.4% | - |
| bristol | 1 | 13 | 7.7% | 5.7 | 5.6% | - |
| mexico-city | 0 | 13 | 0.0% | 5.5 | 5.9% | ahuehuete mexico city (i1, p11) |
| philadelphia | 0 | 13 | 0.0% | 19.1 | 0.9% | - |
| krakow | 0 | 13 | 0.0% | 6.3 | 4.7% | - |
| chapel-hill-north-carolina | 0 | 12 | 0.0% | 14.1 | 1.4% | davie poplar (i2, p10) |
| freiburg | 0 | 12 | 0.0% | 6.1 | 4.9% | - |
| henrykow-lubanski | 0 | 12 | 0.0% | 14.4 | 1.3% | cis henrykowski (i5, p7) |
| melbourne | 0 | 12 | 0.0% | 8.7 | 3.2% | - |
| boston | 0 | 12 | 0.0% | 7.9 | 3.5% | - |
| naples | 0 | 12 | 0.0% | 5.5 | 6.0% | eucalyptus village (i1, p16) |
| sardinia | 0 | 12 | 0.0% | 6.7 | 4.3% | - |
| brussels | 0 | 12 | 0.0% | 7.4 | 3.8% | - |
| the-hague | 0 | 12 | 0.0% | 4.8 | 7.2% | haag (i1, p1) |
| osaka | 1 | 11 | 9.1% | 4.0 | 8.0% | - |
| new-orleans | 1 | 11 | 9.1% | 7.2 | 3.9% | - |
| hamburg | 0 | 11 | 0.0% | 7.1 | 4.0% | - |
| cagliari | 0 | 11 | 0.0% | 9.5 | 2.7% | che piante sono? (i1, p19) |
| gliniak | 0 | 11 | 0.0% | 6.1 | 4.9% | ancient tree (i1, p18) |
| madeira | 0 | 11 | 0.0% | 27.7 | 0.5% | dragon tree madeira (i1, p9) |
| stuttgart | 0 | 11 | 0.0% | 5.0 | 7.0% | - |
| valencia | 0 | 11 | 0.0% | 3.4 | 9.9% | - |
| bologna | 1 | 10 | 10.0% | 5.5 | 6.0% | - |
| istanbul | 1 | 10 | 10.0% | 5.4 | 6.2% | istanbul (i1, p1) |
| poland | 0 | 10 | 0.0% | 7.7 | 3.6% | trees in poland (i1, p8) |
| naha | 0 | 10 | 0.0% | 7.3 | 3.9% | akagi tree (i2, p10) |
| geneva | 0 | 10 | 0.0% | 8.0 | 3.5% | - |
| leeuwarden | 0 | 10 | 0.0% | 4.9 | 7.1% | - |

- Plus 177 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: vienna, cadiz, pamplona, glasgow, ede, hinode, palma-de-mallorca, arnhem.

## 2026-11-10 (previous UTC day)

**Today: an android waitlist signup arrived yesterday (49 total); an account was opened yesterday (62 accounts in all).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 49 | 59 |
| ... of which from search | every search engine | 20 | 21 |
| ... from Google | Google's recovery | 15 | 9 |
| ... from Bing | Bing | 2 | 6 |
| Website visitors who came back | people who stay | 11 | 13 |
| App downloads (first-time) | people | 24 | 17 |
| New accounts | people | 6 | 9 |
| Phones back within 30 days | people who stay | 3 of 12 | 5 of 9 |
| Trees saved to Want to go | intent | 1 | 3 |
| Trees collected | goal 1: stood at a tree | 2 | 5 |
| Readers' contributions | data: trees, photos, corrections, votes | 2 | 2 |
| Shares (app and web) | word of mouth, since 10-30 | 2 | 1 |
| Visits from a shared link | what sharing brings | 0 | 2 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar; a visitor who comes back on another browser or device counts as new, and GA cannot leave our own visits out, so read the came-back row as a direction, not a count. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Quality**: Web red, iOS orange, Android grey, Backup red. Backup: Hidde's one-time setup in BACKUP_RESTORE.md.

| | Web | iOS | Android |
|---|---|---|---|
| Next version | orange: fresh-eyes review 2 days old (due every 1) | orange: fresh-eyes review 2 days old (due every 1) | grey: no checks wired yet |
| Live | red: new error spreading: "Uncaught ReferenceError: maplibregl is not defined" in inline, 3 reports on 3 pages | green | grey: no checks wired yet |

**Plus question**: no answers yet.

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 11-04 | 11-05 | 11-06 | 11-07 | 11-08 | 11-09 | 11-10 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 12 | 8 | 5 | 2 | 10 | 9 | 11 | **57** |
| New accounts | 3 | 1 | 0 | 0 | 1 | 0 | 1 | **6** |
| Saves | 0 | 1 | 0 | 0 | 0 | 0 | 0 | **1** |
| Android waitlist | 0 | 1 | 0 | 0 | 0 | 0 | 1 | **2** |
| App downloads | 4 | 0 | 4 | 0 | 3 | 2 | – | **13** |
| App phones | 8 | 2 | 5 | 4 | 7 | 7 | 5 | **33** |
| Trees opened in the app | 88 | 7 | 8 | 5 | 27 | 5 | 14 | **154** |
| Trees collected | 1 | 0 | 0 | 0 | 0 | 0 | 0 | **1** |
| Trees sent | 0 | 1 | 0 | 0 | 0 | 0 | 0 | **1** |
| Feedback | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Ambassador asks | 1 | 0 | 0 | 0 | 0 | 0 | 0 | **1** |
| App photos | 1 | 0 | 0 | 1 | 0 | 0 | 0 | **2** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| App Store reviews | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
- – means the source has not reported that day yet (Apple's downloads arrive a day or two late), not zero.

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Waiting for you** (what the runs left for you since 2026-11-10)

- 258 email addresses ready to mail (archive 2, nature 9, guide 9, press 135, source 65, council 16, tourism 7, society 7, other 5, garden 3); **the night run found no new contacts in two days**
- prepare.py's awaiting-a-writer count overstates the shelf; the research files passcheck calls stale could be cleaned up.
- build 42 is not archived or uploaded; `scripts/release.py` when you want it in TestFlight, then judge the sheet on your phone.
- `authorize?provider=apple&redirect_to=ancienttrees://auth-callback` answers 302 to appleid.apple.com (Services ID app.ancienttrees.web), and ancienttrees://auth-callback is already on the redirect allow-list (the iPhone'
- in the emulator, the first things to try are signing in with Google and with email, a heart, and Collect (the emulator's camera works; its location can be set in the emulator's extended controls).
- compliance, 6 points wait for your word (data/compliance.json): the 33 accounts made public on 10-29, public by default at sign-up, your full name or KvK on the privacy page, PostHog without consent, mailed photos live b

**Searched yesterday:** lisbon, national park, zu.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 11-01 | 5 | 371 | 1.3% | 10.1 |
| 11-02 | 23 | 1274 | 1.8% | 9.0 |
| 11-03 | 31 | 1192 | 2.6% | 8.2 |
| 11-04 | 14 | 261 | 5.4% | 9.9 |
| 11-05 | 1 | 23 | 4.3% | 34.1 |
| 11-06 | 1 | 35 | 2.9% | 36.6 |
| 11-07 | 2 | 34 | 5.9% | 38.3 |
| 11-08 | 25 | 1013 | 2.5% | 9.1 |
| 11-09 | 28 | 1177 | 2.4% | 8.9 |
| 11-10 *partial* | 8 | 189 | 4.2% | 11.9 |
| **window** | **138** | **5569** | **2.5%** | |
- Top queries (10d): ancient trees (i19, p8); ancient trees app (i2, p1); alte bäume in der nähe (i15, p7); ancienttree (i1, p3); istanbul (i1, p1)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 11-02 | 146 | 6 | 4.1% |
| 11-03 | 121 | 3 | 2.5% |
| 11-04 | 133 | 3 | 2.3% |
| 11-05 | 132 | 9 | 6.8% |
| 11-06 | 106 | 2 | 1.9% |
| 11-07 | 80 | 7 | 8.8% |
| 11-08 | 126 | 9 | 7.1% |
| **7 days** | **844** | **39** | **4.6%** |
- **BING WATCHDOG:** impressions fell from 2847 to 844 week on week. That is the shape of a demotion; read the Bing Webmaster dashboard today.
- Top Bing queries: oldest tree china (c8/i4, p12); picture of the tree in helsinki city center that was preserved (c3/i2, p4); ancient trees app (c2/i8, p5); fig tree in square alicante (c2/i4, p4); palma del cile (c2/i2, p6); cipresso calvo indro montanelli milano (c2/i2, p8); big trees of quebec city (c2/i1, p2); mit newton apple tree address (c2/i1, p2)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 11-10T07:37 | 4.3 | 0 | 4 | 0 | - |
| 11-10T12:04 | 9.5 | 5 | 12 | 0 | Fort Worth +2, Indianapolis +1, Tucson +1, Vienna +1 |
| 11-10T18:37 | 8.4 | 2 | 7 | 0 | Vienna +2 |
| 11-11T01:40 | 8.5 | 1 | 9 | 0 | New York +1 |
| **4 runs** | **31** | **8** | **32** | | |

- 1 of 4 produced no trees; last build that went live: 5h ago.

**What they made**

- Windsor register retry: still stalled, next angle noted
- Leads: Vienna Messe oak hold names the right passes
- Leads: hold the seven READY leads a second write pass declined, with reasons
- LOG and agent costs: night run 2026-11-11, claims released
- New York: the Japanese pagoda tree beside the Camperdown elm (nyc_144)
- Photographs readers sent, queued for a look; vouched ones live
- Record when each page last changed
- Log: second attempt, Vienna written, Sintra verified
- Sintra verify pass: sin_009 Moreton Bay Fig, Parque Marechal Carmona (Cascais), flagged
- Vienna: write and merge vie_060 (Prater Meadow Oak, ND 867) and vie_061 (Heustadelwasser Lime, ND 868), app-only; rest of the write shelf still held; LOG
- Night run: Coimbra verify found no new trees, Phoenix scouting retried, log
- Record when each page last changed
- Leads: genus filled from names; release fort-worth claim
- Indianapolis: write and merge ind_005, the Anne Frank chestnut at the Children's Museum

Machine: 8 chain attempts yesterday, 3 got real work time (~26 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c11/i126); /de (c4/i45); /united-states/maryland (c4/i31); /seville (c3/i96); /app (c3/i27)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'alte bäume in der nähe' (i15, p7)
    - 'alte bäume karte' (i6, p6)
    - 'oldest tree in maryland' (i2, p9)
    - 'acient tree' (i2, p14)
    - 'akagi tree' (i2, p10)
    - 'ancienttree' (i1, p3)
    - '# brief your brief is to act as a visual' (i1, p5)
    - '# modus operandi your modus operandi is ' (i1, p2)
    - and 7 more

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 108 | 18 | 103 | 0.95 | 2 |
| Not yet rich | 79 | 22 | 109 | 1.38 | 2 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| fortingall | 0 | 153 | 0.0% | 11.3 | 2.0% | fortingall yew (i118, p11) |
| seville | 4 | 126 | 3.2% | 5.8 | 5.4% | tartuja (i3, p8) |
| lisbon | 1 | 107 | 0.9% | 5.8 | 5.4% | lisbon trees (i2, p4) |
| berlin | 2 | 94 | 2.1% | 5.9 | 5.2% | berlin trees (i2, p5) |
| tokyo | 1 | 86 | 1.2% | 6.8 | 4.2% | ginkgo sperm (i9, p10) |
| fulufjallet | 0 | 83 | 0.0% | 8.7 | 3.1% | old tjikko (i41, p10) |
| palermo | 1 | 79 | 1.3% | 8.1 | 3.5% | palermo tree (i1, p9) |
| singapore | 1 | 79 | 1.3% | 9.1 | 3.0% | chengal pasir tree (i4, p9) |
| tenerife | 1 | 69 | 1.4% | 13.3 | 1.5% | drago milenario (i3, p12) |
| south-korea | 1 | 65 | 1.5% | 8.7 | 3.2% | korean trees (i4, p10) |
| united-states | 5 | 59 | 8.5% | 12.6 | 1.7% | oldest tree in oregon (i9, p12) |
| olympic-national-park | 1 | 57 | 1.8% | 11.0 | 2.1% | duncan cedar (i29, p8) |
| copenhagen | 3 | 57 | 5.3% | 9.1 | 3.0% | trees in copenhagen (i6, p20) |
| malaga | 2 | 53 | 3.8% | 12.9 | 1.6% | árboles históricos de málaga (i5, p82) |
| munich | 2 | 52 | 3.8% | 4.9 | 7.1% | a monaco di baviera? (i1, p20) |
| paris | 1 | 51 | 2.0% | 6.0 | 5.0% | trees in paris (i1, p9) |
| london | 2 | 46 | 4.3% | 7.4 | 3.8% | chestnut london (i1, p5) |
| fukuoka | 2 | 41 | 4.9% | 9.7 | 2.7% | gingkosidi (i7, p32) |
| kyoto | 2 | 41 | 4.9% | 9.2 | 2.9% | - |
| sequoia-national-park | 0 | 41 | 0.0% | 14.3 | 1.3% | washington tree (i18, p11) |
| amsterdam | 0 | 37 | 0.0% | 7.7 | 3.6% | lomanstraat (i2, p19) |
| new-york | 1 | 36 | 2.8% | 7.4 | 3.8% | - |
| seoul | 2 | 35 | 5.7% | 6.6 | 4.4% | - |
| brisbane | 0 | 35 | 0.0% | 8.1 | 3.5% | banyan tree (i5, p11) |
| cambridge | 0 | 33 | 0.0% | 22.5 | 0.7% | newtons apple tree (i2, p50) |
| taiwan | 0 | 32 | 0.0% | 9.7 | 2.7% | oldest tree in taiwan (i6, p6) |
| netherlands | 1 | 31 | 3.2% | 8.8 | 3.1% | dutch trees (i1, p39) |
| alishan | 0 | 29 | 0.0% | 7.3 | 3.8% | xianglin sacred tree (i6, p4) |
| chishang | 0 | 29 | 0.0% | 7.0 | 4.0% | takeshi kaneshiro tree (i13, p7) |
| venice | 3 | 28 | 10.7% | 4.7 | 7.3% | are there trees in venice (i1, p11) |
| porto | 1 | 28 | 3.6% | 4.2 | 7.8% | - |
| reykjavik | 1 | 28 | 3.6% | 5.8 | 5.5% | oldest tree in iceland (i1, p3) |
| austin | 0 | 28 | 0.0% | 13.8 | 1.4% | old tree (i3, p27) |
| germany | 1 | 27 | 3.7% | 9.2 | 2.9% | trees germany (i2, p48) |
| alicante | 1 | 27 | 3.7% | 5.3 | 6.4% | - |
| monterey | 0 | 27 | 0.0% | 25.4 | 0.6% | lone cypress (i6, p54) |
| san-francisco | 0 | 27 | 0.0% | 8.1 | 3.4% | old tree near me (i1, p4) |
| athens | 0 | 27 | 0.0% | 4.9 | 7.1% | - |
| rome | 0 | 27 | 0.0% | 4.9 | 7.1% | oldest tree in rome (i3, p1) |
| dublin | 1 | 25 | 4.0% | 5.9 | 5.2% | - |
| switzerland | 3 | 24 | 12.5% | 6.8 | 4.2% | oldest tree in switzerland (i1, p1) |
| oahu | 0 | 24 | 0.0% | 8.8 | 3.1% | hitachi tree hawaii (i3, p10) |
| takayama | 0 | 24 | 0.0% | 7.4 | 3.8% | takayama ginkgo tree (i2, p7) |
| kagoshima | 0 | 24 | 0.0% | 9.6 | 2.7% | cycad ovule (i1, p10) |
| nara | 1 | 23 | 4.3% | 5.6 | 5.8% | - |
| edinburgh | 0 | 23 | 0.0% | 7.1 | 3.9% | - |
| kanazawa | 0 | 22 | 0.0% | 6.2 | 4.8% | tabunoki (i1, p9) |
| perth | 0 | 22 | 0.0% | 7.8 | 3.6% | - |
| prague | 0 | 22 | 0.0% | 4.7 | 7.3% | - |
| montreal | 2 | 21 | 9.5% | 5.7 | 5.7% | - |
| milan | 0 | 21 | 0.0% | 5.2 | 6.5% | - |
| coimbra | 1 | 20 | 5.0% | 6.0 | 5.0% | - |
| madrid | 0 | 20 | 0.0% | 8.8 | 3.1% | - |
| barcelona | 0 | 20 | 0.0% | 6.8 | 4.2% | judas barcelona (i1, p9) |
| los-angeles | 0 | 19 | 0.0% | 7.2 | 3.9% | moreton bay fig tree beverly hills (i1, p9) |
| bath | 1 | 18 | 5.6% | 6.8 | 4.2% | tree in bath (i1, p9) |
| antwerp | 0 | 18 | 0.0% | 29.3 | 0.4% | den brandt park (i4, p75) |
| hong-kong | 1 | 17 | 5.9% | 6.5 | 4.5% | oldest tree in hong kong (i1, p9) |
| charleston | 0 | 17 | 0.0% | 18.8 | 0.9% | how old is the angel oak tree (i2, p17) |
| arita | 0 | 16 | 0.0% | 5.5 | 6.0% | - |
| beijing | 0 | 16 | 0.0% | 7.6 | 3.7% | - |
| luxembourg-city | 0 | 16 | 0.0% | 3.6 | 9.3% | - |
| florence | 0 | 16 | 0.0% | 4.2 | 7.8% | - |
| seattle | 1 | 15 | 6.7% | 6.9 | 4.1% | oldest tree in seattle (i2, p7) |
| toronto | 0 | 15 | 0.0% | 7.0 | 4.0% | - |
| istanbul | 2 | 14 | 14.3% | 6.8 | 4.2% | istanbul (i1, p1) |
| bristol | 1 | 14 | 7.1% | 5.7 | 5.6% | - |
| zurich | 1 | 14 | 7.1% | 7.9 | 3.5% | linden (i1, p5) |
| croatia | 0 | 14 | 0.0% | 7.6 | 3.7% | croatian trees (i2, p2) |
| mexico-city | 0 | 14 | 0.0% | 10.6 | 2.3% | ahuehuete mexico city (i1, p11) |
| boston | 0 | 14 | 0.0% | 8.2 | 3.4% | - |
| krakow | 0 | 14 | 0.0% | 6.5 | 4.5% | - |
| chapel-hill-north-carolina | 0 | 13 | 0.0% | 13.8 | 1.4% | davie poplar (i2, p10) |
| melbourne | 0 | 13 | 0.0% | 8.8 | 3.1% | - |
| philadelphia | 0 | 13 | 0.0% | 19.1 | 0.9% | - |
| freiburg | 0 | 12 | 0.0% | 6.1 | 4.9% | - |
| naha | 0 | 12 | 0.0% | 7.1 | 4.0% | akagi tree (i2, p10) |
| naples | 0 | 12 | 0.0% | 5.5 | 6.0% | eucalyptus village (i1, p16) |
| sardinia | 0 | 12 | 0.0% | 6.7 | 4.3% | - |
| brussels | 0 | 12 | 0.0% | 7.4 | 3.8% | - |
| the-hague | 0 | 12 | 0.0% | 4.8 | 7.2% | haag (i1, p1) |
| osaka | 1 | 11 | 9.1% | 4.0 | 8.0% | - |
| new-orleans | 1 | 11 | 9.1% | 7.2 | 3.9% | - |
| bologna | 1 | 11 | 9.1% | 5.5 | 6.1% | - |
| henrykow-lubanski | 0 | 11 | 0.0% | 15.2 | 1.2% | cis henrykowski (i4, p8) |
| hamburg | 0 | 11 | 0.0% | 7.1 | 4.0% | - |
| cagliari | 0 | 11 | 0.0% | 9.5 | 2.7% | che piante sono? (i1, p19) |
| gliniak | 0 | 11 | 0.0% | 6.1 | 4.9% | ancient tree (i1, p18) |
| madeira | 0 | 11 | 0.0% | 27.7 | 0.5% | dragon tree madeira (i1, p9) |
| higashi-hiroshima | 0 | 11 | 0.0% | 19.1 | 0.9% | meoto sugi (i5, p6) |
| stuttgart | 0 | 11 | 0.0% | 5.0 | 7.0% | - |
| valencia | 0 | 11 | 0.0% | 3.4 | 9.9% | - |
| poland | 0 | 10 | 0.0% | 7.7 | 3.6% | trees in poland (i1, p8) |
| budapest | 0 | 10 | 0.0% | 6.6 | 4.4% | - |
| jaegerspris-nordskov | 0 | 10 | 0.0% | 9.7 | 2.7% | kongeegen (i4, p10) |
| cadiz | 0 | 10 | 0.0% | 7.9 | 3.5% | - |
| geneva | 0 | 10 | 0.0% | 8.0 | 3.5% | - |
| leeuwarden | 0 | 10 | 0.0% | 4.9 | 7.1% | - |

- Plus 173 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: vienna, pamplona, glasgow, ede, hinode, palma-de-mallorca, arnhem, houston.

## 2026-11-09 (previous UTC day)

**Today: an android waitlist signup arrived today (49 total).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 52 | 58 |
| ... of which from search | every search engine | 22 | 18 |
| ... from Google | Google's recovery | 17 | 5 |
| ... from Bing | Bing | 2 | 6 |
| Website visitors who came back | people who stay | 10 | 14 |
| App downloads (first-time) | people | 24 | 38 |
| New accounts | people | 5 | 9 |
| Phones back within 30 days | people who stay | 4 of 10 | 4 of 8 |
| Trees saved to Want to go | intent | 2 | 2 |
| Trees collected | goal 1: stood at a tree | 7 | 0 |
| Readers' contributions | data: trees, photos, corrections, votes | 2 | 2 |
| Shares (app and web) | word of mouth, since 10-30 | 2 | 1 |
| Visits from a shared link | what sharing brings | 0 | 2 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar; a visitor who comes back on another browser or device counts as new, and GA cannot leave our own visits out, so read the came-back row as a direction, not a count. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Quality**: Web green, iOS green, Android grey, Backup red. Backup: Hidde's one-time setup in BACKUP_RESTORE.md.

**Plus question**: no answers yet.

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 11-03 | 11-04 | 11-05 | 11-06 | 11-07 | 11-08 | 11-09 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 10 | 12 | 8 | 5 | 2 | 10 | 9 | **56** |
| New accounts | 0 | 3 | 1 | 0 | 0 | 1 | 0 | **5** |
| Saves | 1 | 0 | 1 | 0 | 0 | 0 | 0 | **2** |
| Android waitlist | 1 | 0 | 1 | 0 | 0 | 0 | 0 | **2** |
| App downloads | 2 | 4 | 0 | 4 | 0 | 3 | – | **13** |
| App phones | 6 | 8 | 2 | 5 | 4 | 7 | 7 | **34** |
| Trees opened in the app | 7 | 88 | 7 | 8 | 5 | 27 | 5 | **147** |
| Trees collected | 0 | 1 | 0 | 0 | 0 | 0 | 0 | **1** |
| Trees sent | 0 | 0 | 1 | 0 | 0 | 0 | 0 | **1** |
| Feedback | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Ambassador asks | 0 | 1 | 0 | 0 | 0 | 0 | 0 | **1** |
| App photos | 0 | 1 | 0 | 0 | 1 | 0 | 0 | **2** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| App Store reviews | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
- – means the source has not reported that day yet (Apple's downloads arrive a day or two late), not zero.

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Waiting for you** (what the runs left for you since 2026-11-09)

- 258 email addresses ready to mail (archive 2, nature 9, guide 9, press 135, source 65, council 16, tourism 7, society 7, other 5, garden 3); **the night run found no new contacts in two days**

**Searched yesterday:** beng, bristol, china, forting, ginkgo, ginkgo amsterdam, hungry, london, london plane, new, porto.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-31 | 0 | 38 | 0.0% | 21.5 |
| 11-01 | 5 | 371 | 1.3% | 10.1 |
| 11-02 | 23 | 1274 | 1.8% | 9.0 |
| 11-03 | 31 | 1192 | 2.6% | 8.2 |
| 11-04 | 14 | 261 | 5.4% | 9.9 |
| 11-05 | 1 | 23 | 4.3% | 34.1 |
| 11-06 | 1 | 35 | 2.9% | 36.6 |
| 11-07 | 2 | 34 | 5.9% | 38.3 |
| 11-08 | 25 | 1013 | 2.5% | 9.1 |
| 11-09 *partial* | 24 | 979 | 2.5% | 8.5 |
| **window** | **126** | **5220** | **2.4%** | |
- Top queries (10d): ancient trees (i17, p8); ancient trees app (i2, p1); alte bäume in der nähe (i15, p7); ancienttree (i1, p3); istanbul (i1, p1)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 11-01 | 2225 | 8 | 0.4% |
| 11-02 | 146 | 6 | 4.1% |
| 11-03 | 121 | 3 | 2.5% |
| 11-04 | 133 | 3 | 2.3% |
| 11-05 | 132 | 9 | 6.8% |
| 11-06 | 106 | 2 | 1.9% |
| 11-07 | 80 | 7 | 8.8% |
| **7 days** | **2943** | **38** | **1.3%** |
- Week before: 705 impressions, 33 clicks. No Bing demotion in sight.
- Top Bing queries: oldest tree china (c8/i4, p12); picture of the tree in helsinki city center that was preserved (c3/i2, p4); ancient trees app (c2/i8, p5); fig tree in square alicante (c2/i4, p4); cipresso calvo indro montanelli milano (c2/i2, p8); palma del cile (c2/i2, p6); big trees of quebec city (c2/i1, p2); mit newton apple tree address (c2/i1, p2)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.

Machine: 5 chain attempts yesterday, 2 got real work time (~18 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c10/i125); /de (c4/i41); /united-states/maryland (c4/i31); /seville (c3/i92); /app (c3/i27)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'alte bäume in der nähe' (i15, p7)
    - 'alte bäume karte' (i6, p6)
    - 'oldest tree in maryland' (i2, p9)
    - 'acient tree' (i2, p14)
    - 'akagi tree' (i2, p10)
    - 'ancienttree' (i1, p3)
    - '# brief your brief is to act as a visual' (i1, p5)
    - '# modus operandi your modus operandi is ' (i1, p2)
    - and 7 more

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 108 | 18 | 102 | 0.94 | 2 |
| Not yet rich | 79 | 22 | 106 | 1.34 | 2 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| fortingall | 0 | 149 | 0.0% | 11.3 | 2.0% | fortingall yew (i114, p11) |
| seville | 4 | 120 | 3.3% | 5.9 | 5.2% | tartuja (i3, p8) |
| lisbon | 1 | 98 | 1.0% | 6.0 | 5.0% | lisbon trees (i2, p4) |
| berlin | 2 | 89 | 2.2% | 5.9 | 5.2% | berlin trees (i1, p6) |
| tokyo | 1 | 82 | 1.2% | 6.9 | 4.1% | ginkgo sperm (i9, p10) |
| fulufjallet | 0 | 75 | 0.0% | 8.5 | 3.2% | old tjikko (i35, p10) |
| palermo | 1 | 72 | 1.4% | 7.5 | 3.7% | palermo tree (i1, p9) |
| singapore | 1 | 71 | 1.4% | 8.4 | 3.3% | chengal pasir tree (i4, p9) |
| tenerife | 1 | 69 | 1.4% | 13.3 | 1.5% | drago milenario (i3, p12) |
| south-korea | 1 | 61 | 1.6% | 8.8 | 3.1% | korean trees (i4, p10) |
| united-states | 5 | 57 | 8.8% | 12.9 | 1.6% | oldest tree in oregon (i9, p12) |
| copenhagen | 3 | 52 | 5.8% | 8.7 | 3.1% | trees in copenhagen (i5, p22) |
| malaga | 2 | 50 | 4.0% | 13.2 | 1.6% | árboles históricos de málaga (i5, p82) |
| munich | 1 | 50 | 2.0% | 4.9 | 7.1% | a monaco di baviera? (i1, p20) |
| olympic-national-park | 1 | 48 | 2.1% | 11.2 | 2.1% | duncan cedar (i29, p8) |
| paris | 0 | 48 | 0.0% | 5.9 | 5.2% | trees in paris (i1, p9) |
| london | 2 | 46 | 4.3% | 7.2 | 3.9% | chestnut london (i1, p5) |
| sequoia-national-park | 0 | 39 | 0.0% | 14.8 | 1.2% | washington tree (i17, p11) |
| kyoto | 2 | 38 | 5.3% | 9.3 | 2.9% | - |
| fukuoka | 2 | 37 | 5.4% | 10.1 | 2.5% | gingkosidi (i7, p32) |
| new-york | 1 | 36 | 2.8% | 7.4 | 3.8% | - |
| amsterdam | 0 | 35 | 0.0% | 7.9 | 3.6% | lomanstraat (i2, p19) |
| cambridge | 0 | 32 | 0.0% | 22.9 | 0.7% | newtons apple tree (i2, p50) |
| brisbane | 0 | 32 | 0.0% | 7.5 | 3.8% | banyan tree (i4, p11) |
| netherlands | 1 | 31 | 3.2% | 8.8 | 3.1% | dutch trees (i1, p39) |
| seoul | 2 | 31 | 6.5% | 6.9 | 4.1% | - |
| reykjavik | 1 | 28 | 3.6% | 5.8 | 5.5% | oldest tree in iceland (i1, p3) |
| austin | 0 | 28 | 0.0% | 13.8 | 1.4% | old tree (i3, p27) |
| venice | 3 | 27 | 11.1% | 4.5 | 7.5% | are there trees in venice (i1, p11) |
| porto | 1 | 27 | 3.7% | 4.3 | 7.7% | - |
| alicante | 1 | 27 | 3.7% | 5.3 | 6.4% | - |
| chishang | 0 | 27 | 0.0% | 7.0 | 4.0% | takeshi kaneshiro tree (i11, p7) |
| dublin | 1 | 26 | 3.8% | 6.0 | 5.0% | - |
| monterey | 0 | 26 | 0.0% | 26.4 | 0.5% | lone cypress (i5, p48) |
| rome | 0 | 26 | 0.0% | 4.7 | 7.3% | oldest tree in rome (i3, p1) |
| taiwan | 0 | 25 | 0.0% | 10.7 | 2.2% | oldest tree in taiwan (i3, p6) |
| takayama | 0 | 24 | 0.0% | 7.4 | 3.8% | takayama ginkgo tree (i2, p7) |
| athens | 0 | 24 | 0.0% | 4.9 | 7.1% | - |
| switzerland | 2 | 23 | 8.7% | 7.0 | 4.0% | oldest tree in switzerland (i1, p1) |
| germany | 1 | 23 | 4.3% | 9.7 | 2.7% | trees germany (i2, p48) |
| nara | 1 | 23 | 4.3% | 5.6 | 5.8% | - |
| alishan | 0 | 23 | 0.0% | 7.5 | 3.8% | xianglin sacred tree (i5, p4) |
| san-francisco | 0 | 23 | 0.0% | 8.8 | 3.1% | old tree near me (i1, p4) |
| edinburgh | 0 | 23 | 0.0% | 7.2 | 3.9% | - |
| kagoshima | 0 | 22 | 0.0% | 9.5 | 2.8% | cycad ovule (i1, p10) |
| prague | 0 | 22 | 0.0% | 4.7 | 7.3% | - |
| coimbra | 1 | 21 | 4.8% | 6.1 | 4.9% | - |
| montreal | 2 | 21 | 9.5% | 5.7 | 5.7% | - |
| madrid | 0 | 21 | 0.0% | 9.3 | 2.9% | - |
| oahu | 0 | 19 | 0.0% | 8.8 | 3.1% | hitachi tree hawaii (i3, p10) |
| los-angeles | 0 | 19 | 0.0% | 7.2 | 3.9% | moreton bay fig tree beverly hills (i1, p9) |
| bath | 1 | 18 | 5.6% | 6.8 | 4.2% | tree in bath (i1, p9) |
| hong-kong | 1 | 18 | 5.6% | 6.7 | 4.3% | oldest tree in hong kong (i1, p9) |
| kanazawa | 0 | 18 | 0.0% | 6.2 | 4.8% | tabunoki (i1, p9) |
| seattle | 1 | 16 | 6.2% | 7.0 | 4.0% | oldest tree in seattle (i2, p7) |
| charleston | 0 | 16 | 0.0% | 18.9 | 0.9% | how old is the angel oak tree (i2, p17) |
| perth | 0 | 16 | 0.0% | 8.1 | 3.5% | - |
| luxembourg-city | 0 | 15 | 0.0% | 3.3 | 10.0% | - |
| antwerp | 0 | 15 | 0.0% | 25.1 | 0.6% | den brandt park (i3, p75) |
| toronto | 0 | 15 | 0.0% | 7.0 | 4.0% | - |
| croatia | 0 | 14 | 0.0% | 7.6 | 3.7% | croatian trees (i2, p2) |
| boston | 0 | 14 | 0.0% | 8.2 | 3.4% | - |
| krakow | 0 | 14 | 0.0% | 6.5 | 4.5% | - |
| barcelona | 0 | 14 | 0.0% | 6.8 | 4.2% | judas barcelona (i1, p9) |
| istanbul | 2 | 13 | 15.4% | 6.9 | 4.1% | istanbul (i1, p1) |
| bristol | 1 | 13 | 7.7% | 5.8 | 5.5% | - |
| beijing | 0 | 13 | 0.0% | 8.0 | 3.5% | - |
| philadelphia | 0 | 13 | 0.0% | 19.1 | 0.9% | - |
| florence | 0 | 13 | 0.0% | 4.5 | 7.5% | - |
| zurich | 1 | 12 | 8.3% | 8.1 | 3.5% | - |
| chapel-hill-north-carolina | 0 | 12 | 0.0% | 10.4 | 2.4% | davie poplar (i2, p10) |
| arita | 0 | 12 | 0.0% | 4.7 | 7.3% | - |
| hamburg | 0 | 12 | 0.0% | 10.9 | 2.2% | - |
| mexico-city | 0 | 12 | 0.0% | 12.0 | 1.8% | ahuehuete mexico city (i1, p11) |
| brussels | 0 | 12 | 0.0% | 7.4 | 3.8% | - |
| the-hague | 0 | 12 | 0.0% | 4.8 | 7.2% | haag (i1, p1) |
| bologna | 1 | 11 | 9.1% | 5.5 | 6.1% | - |
| freiburg | 0 | 11 | 0.0% | 6.3 | 4.7% | - |
| cagliari | 0 | 11 | 0.0% | 9.5 | 2.7% | che piante sono? (i1, p19) |
| gliniak | 0 | 11 | 0.0% | 6.1 | 4.9% | ancient tree (i1, p18) |
| naha | 0 | 11 | 0.0% | 6.9 | 4.1% | akagi tree (i2, p10) |
| stuttgart | 0 | 11 | 0.0% | 5.0 | 7.0% | - |
| valencia | 0 | 11 | 0.0% | 3.4 | 9.9% | - |
| milan | 0 | 11 | 0.0% | 4.7 | 7.3% | - |
| new-orleans | 1 | 10 | 10.0% | 7.3 | 3.9% | - |
| melbourne | 0 | 10 | 0.0% | 10.4 | 2.4% | - |
| budapest | 0 | 10 | 0.0% | 6.6 | 4.4% | - |
| jaegerspris-nordskov | 0 | 10 | 0.0% | 9.7 | 2.7% | kongeegen (i4, p10) |
| madeira | 0 | 10 | 0.0% | 29.5 | 0.4% | dragon tree madeira (i1, p9) |
| naples | 0 | 10 | 0.0% | 5.9 | 5.2% | eucalyptus village (i1, p16) |
| cadiz | 0 | 10 | 0.0% | 7.9 | 3.5% | - |
| higashi-hiroshima | 0 | 10 | 0.0% | 15.4 | 1.2% | meoto sugi (i5, p6) |
| amersfoort | 0 | 10 | 0.0% | 4.5 | 7.5% | - |

- Plus 176 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: vienna, pamplona, glasgow, ede, hinode, palma-de-mallorca, arnhem, houston.

## Weekly analysis 2026-11-09

Fifteenth weekly analysis. Compares 11-02 to 11-08 with 10-26 to 11-01, read from
the 11-08 daily entry (its 7-day tables). Google's 11-08 row is partial. Volumes are
small; nothing below is a trend unless it says so.

**Scorecard**

| Week | Impressions | Clicks | CTR | Avg position | Visitors (GA, new) | From Google | App downloads (first-time) | New accounts | Trees collected | Readers' contributions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10-26 to 11-01 | 573 | 11 | 1.9% | 21 to 50, 10.1 on 11-01 | 62 | 3 | 17 | 9 | 0 | 8 |
| 11-02 to 11-08 | 3,616 (11-08 partial) | 93 | 2.6% | 8 to 10 on 4 days, 34 to 38 on 3 | 54 | 16 | 14 | 8 | 7 | 3 |

Google by day: 1,274 and 1,192 impressions on 11-02 and 11-03, 261 on 11-04, then 23,
35 and 34 on 11-05 to 11-07, then 797 (partial) on 11-08. Bing, 7 days to 11-05: 2,937
impressions and 43 clicks against 676 and 28; 2,225 of the impressions fall on 11-01
alone (0.4% CTR). Device split and per-visit ratios are not in the entry, so none is
claimed. Android waitlist: 2 this week. Website actions ever: 800, directions 7.

**Outreach yield** (data/mail-yield.json, mailbox read; weeks keyed by the Monday of our first mail; the week of 10-26 is the one old enough to read, the week of 11-02 is not)

| Group | Mailed, week of 10-26 | Answered of those | Mailed, total | Answered, total | Rate | Linked |
|---|---:|---:|---:|---:|---:|---:|
| archive | 11 | 1 | 25 | 1 | 4% | 0 |
| nature | 63 | 3 (2 automatic only) | 81 | 6 | 7% | 1 |
| guide | 12 | 0 | 36 | 1 | 3% | 1 |
| source | 21 | 2 | 59 | 4 | 7% | 0 |
| press | 38 | 1 | 121 | 7 | 6% | 0 |
| tourism | 0 | 0 | 18 | 3 | 17% | 0 |
| garden | 0 | 0 | 97 | 11 | 11% | 0 |
| society | 2 | 1 | 148 | 25 | 17% | 1 |
| council | 1 | 0 | 58 | 9 | 16% | 0 |
| other | 10 | 5 | 160 | 50 | 31% | 2 |

The week of 11-02 added archive 10, nature 16, guide 19, press 23, council 3 and other 19
mailed, with 7 answers so far (nature 2, other 4, council 1), too young to judge. Five
links in all across every group.

**What moved:**
1. Google was up on 11-02 and 11-03 (about 1,200 impressions a day at position 8 to 9,
   23 and 31 clicks), then fell to 23 to 35 a day for three days at position 34 to 38,
   then 797 (partial) on 11-08. The week's total is 6 times the week before, but it is
   two days and a partial one; the swing between days is the finding, not the total.
2. Visitors from Google 16 against 3, while all new visitors are flat (54 against 62)
   and Bing's share fell (2 against 7). Daily visitors still sit at 2 to 12.
3. App: 14 first-time downloads against 17 (of the last 21 on record, 11 came from App
   Store search, 6 from a web referrer, 4 from an app referrer; US 7, GB 5, NL 4). Trees
   opened 163 on 32 phones, trees collected 7 against 0.
4. Readers gave 3 contributions against 8 (one tree, two app photos); two ambassador
   requests (Pamplona, Leuven). No tree waits for inspection.
5. Quality: Web orange (a new TypeError "undefined is not a function ... addEvent" in an
   inline script) and Backup red (Hidde's one-time setup, BACKUP_RESTORE.md). The night
   run found no new outreach contacts in two days; 258 addresses are ready.

**Suggestions, ranked:**
1. **[run]** Fix the new web TypeError (`mq.addEvent`, 2 new error types in the quality
   line). It is rung-2 work and it reaches every visitor the Google days bring (16 this week).
2. **[run]** Read data/tagged-still-shown.json against the Google days and say which
   pages carry 11-02, 11-03 and 11-08 (800 to 1,200 impressions) and which the 23 to 35
   days, so the digest can say whether the same pages drop out and return. No page-set
   change on this evidence: it is two days up and three down.
3. **[run]** Spend the sourcing window on nature and guide contacts, not press. Ready
   pool: press 135, source 65 against nature 9 and guide 9, and no new contacts in two
   days. Guide has 1 answer in 36 mailed (3%), so source guide only for cities with
   photographed trees, and wait for the 19 guide mails of week 11-02 to answer first.
4. **[FOR HIDDE]** The week of 10-26 sent 63 nature mails and got 3 answers (2 of them
   automatic). Before the next nature batch goes, decide whether it keeps the same short
   mail; wilder.pt (10-24) is the only referral spike on file.
5. **[sessie]** App Store search is 11 of the last 21 downloads, the largest source and
   independent of the web demotion. Look once at the listing (name, subtitle, keywords)
   against the search terms Apple reports, before build 41.

**Watch next week:** whether Google days return to 1,000+ impressions at position
under 10 and hold for three in a row (read beside the tagged-still-shown list), and
whether the week-of-11-02 outreach batch (nature 16, guide 19, press 23) brings answers
beyond automatic ones.

## 2026-11-08 (previous UTC day)

**Today: an account was opened yesterday (61 accounts in all).**

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 54 | 62 |
| ... of which from search | every search engine | 21 | 17 |
| ... from Google | Google's recovery | 16 | 3 |
| ... from Bing | Bing | 2 | 7 |
| Website visitors who came back | people who stay | 10 | 12 |
| App downloads (first-time) | people | - | - |
| New accounts | people | 8 | 9 |
| Phones back within 30 days | people who stay | 4 of 8 | 8 of 13 |
| Trees saved to Want to go | intent | 3 | 1 |
| Trees collected | goal 1: stood at a tree | 7 | 0 |
| Readers' contributions | data: trees, photos, corrections, votes | 3 | 8 |
| Shares (app and web) | word of mouth, since 10-30 | 2 | 1 |
| Visits from a shared link | what sharing brings | 0 | 2 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar; a visitor who comes back on another browser or device counts as new, and GA cannot leave our own visits out, so read the came-back row as a direction, not a count. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Quality**: Web orange, iOS orange, Android not live yet, Backup red. Backup: Hidde's one-time setup in BACKUP_RESTORE.md.

| | Web | iOS | Android |
|---|---|---|---|
| Live | orange: 2 new error type(s), first "TypeError: undefined is not a function (near '...mq.addEvent" in inline | green | grey: not live yet |
| Open bugs | green | orange: 2 open, 2 found by people | grey: not live yet |

**Plus question** (3 answers, 1 new; 1 asked to be told; 1 wrote an idea, read them with `python3 scripts/plus_answers.py`; up to two each)

| Choice | Picked by |
|---|---:|
| Recommended tree walks for a city trip | 1 |
| Something else | 1 |
| A richer log of every tree you've collected | 1 |
| Download offline maps | 1 |

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 11-02 | 11-03 | 11-04 | 11-05 | 11-06 | 11-07 | 11-08 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 11 | 10 | 12 | 8 | 5 | 2 | 10 | **58** |
| New accounts | 3 | 0 | 3 | 1 | 0 | 0 | 1 | **8** |
| Saves | 1 | 1 | 0 | 1 | 0 | 0 | 0 | **3** |
| Android waitlist | 0 | 1 | 0 | 1 | 0 | 0 | 0 | **2** |
| App downloads | 4 | 2 | 4 | 0 | 4 | – | – | **14** |
| App phones | 6 | 6 | 8 | 2 | 5 | 4 | 7 | **32** |
| Trees opened in the app | 21 | 7 | 88 | 7 | 8 | 5 | 27 | **163** |
| Trees collected | 5 | 0 | 1 | 0 | 0 | 0 | 0 | **6** |
| Trees sent | 0 | 0 | 0 | 1 | 0 | 0 | 0 | **1** |
| Feedback | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Ambassador asks | 1 | 0 | 1 | 0 | 0 | 0 | 0 | **2** |
| App photos | 0 | 0 | 1 | 0 | 0 | 1 | 0 | **2** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| App Store reviews | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
- – means the source has not reported that day yet (Apple's downloads arrive a day or two late), not zero.

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Waiting for you** (what the runs left for you since 2026-11-08)

- 258 email addresses ready to mail (archive 2, nature 9, guide 9, press 135, source 65, council 16, tourism 7, society 7, other 5, garden 3); **the night run found no new contacts in two days**
- both still need a session on the Mac.
- seg_003 (Andromeda parterre sequoia, AS-SG-09)
- Organizer, the top 1.0.4 (41), Distribute App; TestFlight round; submit with phased release.
- the next Mac session builds, runs AmbassadorAskWalk and merges before build 41.
- iOS scheduled runs keep failing; look at the xcresult artifact of run 42412097686.
- the daily task "publish-held-trees-daily" can be switched off under Scheduled; new trees now reach the app straight from the night run's write passes.

**Searched yesterday:** brno, prague, tokyo.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-30 | 2 | 29 | 6.9% | 24.1 |
| 10-31 | 0 | 38 | 0.0% | 21.5 |
| 11-01 | 5 | 371 | 1.3% | 10.1 |
| 11-02 | 23 | 1274 | 1.8% | 9.0 |
| 11-03 | 31 | 1192 | 2.6% | 8.2 |
| 11-04 | 14 | 261 | 5.4% | 9.9 |
| 11-05 | 1 | 23 | 4.3% | 34.1 |
| 11-06 | 1 | 35 | 2.9% | 36.6 |
| 11-07 | 2 | 34 | 5.9% | 38.3 |
| 11-08 *partial* | 21 | 797 | 2.6% | 8.9 |
| **window** | **100** | **4054** | **2.5%** | |
- Top queries (10d): alte bäume in der nähe (i13, p7); ancient trees (i13, p9); ancienttree (i1, p3); istanbul (i1, p1); leuven, belgium (i1, p4)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-30 | 90 | 10 | 11.1% |
| 10-31 | 90 | 4 | 4.4% |
| 11-01 | 2225 | 8 | 0.4% |
| 11-02 | 146 | 6 | 4.1% |
| 11-03 | 121 | 3 | 2.5% |
| 11-04 | 133 | 3 | 2.3% |
| 11-05 | 132 | 9 | 6.8% |
| **7 days** | **2937** | **43** | **1.5%** |
- Week before: 676 impressions, 28 clicks. No Bing demotion in sight.
- Top Bing queries: oldest tree china (c8/i4, p12); picture of the tree in helsinki city center that was preserved (c3/i2, p4); ancient trees app (c2/i8, p5); fig tree in square alicante (c2/i4, p4); palma del cile (c2/i2, p6); cipresso calvo indro montanelli milano (c2/i2, p8); big trees of quebec city (c2/i1, p2); mit newton apple tree address (c2/i1, p2)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

**Monday: the slow tables.** They rarely change a day's decision, so they come once a week.

**Website actions, ever** (the events table begins 2026-08-01, when the funnel was repaired; a zero has never fired at all)

| Action | Ever |
|---|---:|
| app-cta | 189 |
| signin-open | 164 |
| search-home | 107 |
| home-fav | 64 |
| waitlist-submit | 33 |
| signin-oauth | 31 |
| signin-done | 30 |
| search-bar | 29 |
| app-open | 26 |
| home-country | 21 |
| search-explore | 16 |
| home-dir-city | 14 |
| ambassador-request | 11 |
| search-bar-m | 9 |
| signin-link-sent | 8 |
| directions | 7 |
| home-dir-collection | 4 |
| search-empty-bar | 4 |
| home-dir-species | 3 |
| home-dir-tree | 3 |
| home-species | 3 |
| save | 3 |
| plus-open | 2 |
| search-empty-home | 2 |
| share_arrived | 2 |
| share_tapped | 2 |
| signout | 2 |
| sponsor-open | 2 |
| app-page-badge | 1 |
| home-oldest | 1 |
| search-empty-explore | 1 |
| search-none-bar | 1 |
| search-none-bar-m | 1 |
| search-none-explore | 1 |
| search-none-home | 1 |
| tree-photo-sent | 1 |
| worthit-report | 1 |
| worthit-not worth it | 0 |
| worthit-worth it | 0 |
| **all** | **800** |

**App events, ever** (measured since 2026-08-30)

| What | Ever |
|---|---:|
| app_open | 587 |
| tab | 519 |
| tree_opened | 2158 |
| directions | 77 |
| tree_saved | 48 |
| tree_visited | 41 |
| sighting_recorded | 97 |
| sync_skipped | 0 |
| sync_failed | 0 |
| location | 84 |
| share_tapped | 1 |
| **all** | **3612** |

**What readers told us** (7 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 11-02 | Pamplona | ambassador request | - | 2512 | - |
| 11-04 | Leuven | ambassador request | - | 0c58 | - |
| 11-05 | 15A3B6F1-3DD9-4AC2-BEC5-BBD1C47D76 | tree sent in | 128 chars, read it in the database | 6ec2 | - |

- 3 rows from 3 accounts.

**App Store downloads** (Apple's own count, not PostHog)

| Day | Downloads |
|---|---:|
| 2026-10-31 | 2 |
| 2026-11-01 | 5 |
| 2026-11-02 | 4 |
| 2026-11-03 | 2 |
| 2026-11-04 | 4 |
| 2026-11-06 | 4 |
| **6 days** | **21** |
- First-time downloads only, which is what App Store Connect's Trends screen counts; redownloads and updates are not in this table.

**Where the downloads came from** (7 days, Apple's attribution)

| Came from | Via | Downloads |
|---|---|---:|
| App Store search | - | 11 |
| Web referrer | - | 6 |
| App referrer | - | 4 |
| **window** | | **21** |
- Countries: US (7); GB (5); NL (4); PT (2); BR (1); CA (1)
- Apple's own source split, first-time downloads only. "Web referrer" with our own domain is the site's app page; "App Store search" is somebody who typed into the store. "Unavailable" is Apple's word for a source it could not attribute.

**Bing's index** (pages crawled and in index, Bing Webmaster Tools)

| Day | Pages crawled | Pages in index |
|---|---:|---:|
| 10-30 | 221 | 3740 |
| 10-31 | 307 | 3868 |
| 11-01 | 423 | 3958 |
| 11-02 | 300 | 3958 |
| 11-03 | 380 | 4092 |
- In index the week before: 3678.

**Who they are** (full cut, Mondays)
Audience, 28 days of search (126 clicks, 4818 impressions):
- Countries: usa c20/i928; prt c14/i111; esp c13/i426; deu c10/i314; ita c10/i211
- Devices: MOBILE c78/i2633; DESKTOP c45/i2125; TABLET c3/i60
- Landing pages: / c22/i142; /de c4/i39; /seville c4/i69; /united-states/maryland c3/i27; /app c2/i36
- Search language (top 100 named queries, crude match, most clicks are in queries Google withholds): English 47q c3/i99; unclassified 43q c4/i51; German 4q c1/i30; Spanish 3q c0/i24; Italian 2q c0/i2; French 1q c0/i1

**Google Analytics** (last 7 days, visitors who accepted cookies)

| Day | People | New | Returning | Visits | Pageviews | Engaged visits |
|---|---:|---:|---:|---:|---:|---:|
| 11-02 | 11 | 10 | 1 | 13 | 28 | 11 |
| 11-03 | 10 | 10 | 0 | 11 | 19 | 6 |
| 11-04 | 12 | 12 | 0 | 15 | 41 | 9 |
| 11-05 | 8 | 7 | 1 | 10 | 35 | 6 |
| 11-06 | 5 | 3 | 2 | 7 | 8 | 4 |
| 11-07 | 2 | 2 | 0 | 2 | 6 | 2 |
| 11-08 | 10 | 10 | 0 | 14 | 28 | 8 |
| **window** | | **54** | | **72** | **165** | **46** |
- People per day are not summed: one person on two days is one person, and GA counts them once per day.
- Coming back (28 days): 39 returning against 226 new, 15% of the people GA saw.

| Page | Pageviews | People |
|---|---:|---:|
| / | 8 | 6 |
| /seattle | 8 | 2 |
| /ede | 4 | 3 |
| /es/pamplona | 4 | 1 |
| /fr/paris/plane-of-square-des-batignolles | 4 | 1 |
| /porto | 4 | 2 |
| /amsterdam | 3 | 2 |
| /brisbane/banyan-tree-of-city-botanic-gardens | 3 | 1 |
| /fr/explore | 3 | 1 |
| /leuven | 3 | 1 |

| Came from | Visits | People |
|---|---:|---:|
| (direct) / (none) | 34 | 26 |
| google / organic | 20 | 17 |
| accounts.google.com / referral | 2 | 2 |
| bing / organic | 2 | 2 |
| ch.search.yahoo.com / referral | 2 | 1 |
| ecosia.org / organic | 2 | 2 |
| fr.search.yahoo.com / referral | 2 | 1 |
| m.facebook.com / referral | 2 | 1 |
- GA sees only visitors who pressed Accept on the cookie bar; read it as a sample.

Backlinks (watched pages):
| Site | Links to | rel | First seen |
|---|---|---|---|
| getlisbon.com | /lisbon | followed | 2026-09-08 |
| getlisbon.com | /pt/lisbon | followed | 2026-09-08 |
| www.baumkunde.de | /copenhagen | followed | 2026-09-26 |
| www.baumkunde.de | /rogalin/russ-oak | followed | 2026-09-26 |
| wilder.pt | / | followed | 2026-10-24 |
5 linking page(s), 5 followed. Checked by fetching the page: a link with rel="noreferrer" never appears in the referrer table, so these two lines measure different things and neither replaces the other. Unknown links stay a manual read of Search Console's Links report. This run read 8 of 12 fetched (4 unreachable), out of 28 watched pages.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 11-08T16:29 | 20.6 | 8 | 10 | 2 | Porto +3, Salt Lake City +2, Guimaraes +1, Oahu +1, +1 more |
| 11-08T18:55 | 4.3 | 0 | 3 | 0 | - |
| 11-09T01:22 | 6.3 | 0 | 6 | 3 | - |
| **3 runs** | **31** | **8** | **19** | | |

- 2 of 3 produced no trees; 2 to 3 commands refused per run; last build that went live: 5h ago.

**What they made**

- Vienna verify pass: 2 Prater trees, 4 leads; log the window
- Web errors: old Safari matchMedia listener and browsers without dialog.showModal no longer throw
- Photographs readers sent, queued for a look; vouched ones live
- Brighton scouting retry: nothing new, stays stalled
- Guimaraes verify pass: 0 trees, wall for 48h; log the window
- Record when each page last changed
- Write pass: por_032 to por_034, the three protected trees of Quinta de Villar d'Allen (Porto)
- Write pass: gui_009 Briteiros stone pine, hnl_024 Waikiki Aquarium banyan, Penacova wisteria (pcv_001)
- Segovia scouted: register already imported, one lead, seg_003 life question logged
- Salt Lake City: slc_019 and slc_020, the city reaches its target of 20
- Record when each page last changed
- Fresh-eyes review: 4 finding(s)
- Fresh-eyes review: 2 finding(s)

Machine: 7 chain attempts yesterday, 4 got real work time (~42 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c8/i101); /seville (c3/i65); /de (c3/i32); /united-states/maryland (c3/i25); /malaga (c2/i31)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'alte bäume in der nähe' (i13, p7)
    - 'alte bäume karte' (i4, p6)
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
| Impressions | 4159 |
| Clicks | 100 |
| Pages that got at least one impression | 1188 |
| Impressions on the proven cities | 3082 |

- 413 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3391 trees Google may index, 1307 kept out for lacking a photo and an exact pin, 5907 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 107 | 14 | 81 | 0.76 | 2 |
| Not yet rich | 79 | 19 | 79 | 1.00 | 2 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| seville | 4 | 92 | 4.3% | 5.9 | 5.1% | tartuja (i3, p8) |
| fortingall | 0 | 91 | 0.0% | 12.2 | 1.8% | fortingall yew (i63, p11) |
| berlin | 1 | 73 | 1.4% | 5.8 | 5.3% | berlin trees (i1, p6) |
| tokyo | 1 | 64 | 1.6% | 7.4 | 3.8% | ginkgo sperm (i8, p10) |
| palermo | 1 | 61 | 1.6% | 7.6 | 3.7% | - |
| lisbon | 1 | 60 | 1.7% | 5.7 | 5.6% | lisbon trees (i2, p4) |
| tenerife | 1 | 59 | 1.7% | 12.3 | 1.7% | drago milenario (i3, p12) |
| singapore | 1 | 57 | 1.8% | 8.7 | 3.1% | bodhi tree singapore (i3, p5) |
| fulufjallet | 0 | 53 | 0.0% | 8.2 | 3.4% | old tjikko (i25, p9) |
| south-korea | 1 | 50 | 2.0% | 8.9 | 3.0% | korean trees (i4, p10) |
| united-states | 4 | 43 | 9.3% | 13.7 | 1.5% | oldest tree in oregon (i6, p12) |
| copenhagen | 2 | 42 | 4.8% | 9.6 | 2.7% | trees in copenhagen (i5, p19) |
| london | 2 | 37 | 5.4% | 7.4 | 3.8% | chestnut london (i1, p5) |
| malaga | 2 | 35 | 5.7% | 15.0 | 1.2% | árboles históricos de málaga (i4, p84) |
| munich | 1 | 35 | 2.9% | 5.1 | 6.8% | a monaco di baviera? (i1, p20) |
| olympic-national-park | 1 | 34 | 2.9% | 12.5 | 1.7% | duncan cedar (i21, p9) |
| fukuoka | 2 | 34 | 5.9% | 10.0 | 2.5% | gingkosidi (i6, p32) |
| paris | 0 | 34 | 0.0% | 6.1 | 4.9% | trees in paris (i1, p9) |
| new-york | 1 | 33 | 3.0% | 7.4 | 3.8% | - |
| sequoia-national-park | 0 | 32 | 0.0% | 16.0 | 1.1% | washington tree (i13, p11) |
| netherlands | 1 | 31 | 3.2% | 8.8 | 3.1% | dutch trees (i1, p39) |
| kyoto | 1 | 29 | 3.4% | 11.1 | 2.1% | - |
| cambridge | 0 | 28 | 0.0% | 25.0 | 0.6% | newtons apple tree (i2, p50) |
| chishang | 0 | 26 | 0.0% | 12.4 | 1.7% | takeshi kaneshiro tree (i9, p7) |
| amsterdam | 0 | 25 | 0.0% | 6.9 | 4.1% | lomanstraat amsterdam trees (i1, p9) |
| brisbane | 0 | 24 | 0.0% | 7.8 | 3.6% | banyan tree (i3, p11) |
| porto | 0 | 23 | 0.0% | 4.7 | 7.3% | - |
| coimbra | 1 | 21 | 4.8% | 6.1 | 4.9% | - |
| monterey | 0 | 21 | 0.0% | 29.2 | 0.4% | lone cypress (i4, p51) |
| takayama | 0 | 21 | 0.0% | 8.0 | 3.5% | takayama ginkgo tree (i2, p7) |
| rome | 0 | 21 | 0.0% | 4.2 | 7.8% | oldest tree in rome (i3, p1) |
| alicante | 0 | 21 | 0.0% | 5.6 | 5.8% | - |
| alishan | 0 | 20 | 0.0% | 7.5 | 3.8% | xianglin sacred tree (i5, p4) |
| austin | 0 | 20 | 0.0% | 15.3 | 1.2% | old tree (i3, p27) |
| venice | 2 | 19 | 10.5% | 5.1 | 6.9% | are there trees in venice (i1, p11) |
| reykjavik | 1 | 19 | 5.3% | 5.5 | 5.9% | oldest tree in iceland (i1, p3) |
| germany | 1 | 18 | 5.6% | 10.1 | 2.5% | trees germany (i2, p48) |
| seoul | 1 | 18 | 5.6% | 7.0 | 4.0% | - |
| bath | 1 | 18 | 5.6% | 6.8 | 4.2% | tree in bath (i1, p9) |
| athens | 0 | 18 | 0.0% | 4.5 | 7.5% | - |
| edinburgh | 0 | 18 | 0.0% | 7.1 | 4.0% | - |
| madrid | 0 | 18 | 0.0% | 9.2 | 2.9% | - |
| dublin | 0 | 18 | 0.0% | 6.7 | 4.3% | - |
| switzerland | 1 | 17 | 5.9% | 8.2 | 3.4% | oldest tree in switzerland (i1, p1) |
| nara | 1 | 17 | 5.9% | 5.3 | 6.4% | - |
| san-francisco | 0 | 17 | 0.0% | 9.8 | 2.6% | old tree near me (i1, p4) |
| montreal | 3 | 16 | 18.8% | 4.5 | 7.5% | - |
| hong-kong | 1 | 15 | 6.7% | 6.7 | 4.3% | oldest tree in hong kong (i1, p9) |
| taiwan | 0 | 15 | 0.0% | 13.6 | 1.5% | oldest tree in taiwan (i3, p6) |
| luxembourg-city | 0 | 15 | 0.0% | 3.3 | 10.0% | - |
| oahu | 0 | 15 | 0.0% | 8.7 | 3.2% | hitachi tree hawaii (i3, p10) |
| kagoshima | 0 | 15 | 0.0% | 8.1 | 3.4% | cycad ovule (i1, p10) |
| prague | 0 | 15 | 0.0% | 5.3 | 6.5% | - |
| boston | 0 | 14 | 0.0% | 8.2 | 3.4% | - |
| kanazawa | 0 | 14 | 0.0% | 6.6 | 4.4% | tabunoki (i1, p9) |
| perth | 0 | 14 | 0.0% | 7.9 | 3.6% | - |
| toronto | 0 | 14 | 0.0% | 6.9 | 4.1% | - |
| istanbul | 2 | 12 | 16.7% | 7.0 | 4.0% | istanbul (i1, p1) |
| los-angeles | 0 | 12 | 0.0% | 5.8 | 5.3% | moreton bay fig tree beverly hills (i1, p9) |
| antwerp | 0 | 12 | 0.0% | 16.8 | 1.1% | den brandt park (i2, p72) |
| florence | 0 | 12 | 0.0% | 4.2 | 7.8% | - |
| seattle | 1 | 11 | 9.1% | 7.3 | 3.9% | oldest tree in seattle (i1, p4) |
| bristol | 1 | 11 | 9.1% | 5.6 | 5.7% | - |
| zurich | 1 | 11 | 9.1% | 8.5 | 3.3% | - |
| chapel-hill-north-carolina | 0 | 11 | 0.0% | 10.4 | 2.4% | davie poplar (i2, p10) |
| croatia | 0 | 11 | 0.0% | 7.5 | 3.8% | croatian trees (i2, p2) |
| charleston | 0 | 11 | 0.0% | 22.6 | 0.7% | how old is the angel oak tree (i2, p17) |
| philadelphia | 0 | 11 | 0.0% | 21.3 | 0.7% | - |
| the-hague | 0 | 11 | 0.0% | 4.9 | 7.1% | haag (i1, p1) |
| bologna | 1 | 10 | 10.0% | 5.1 | 6.8% | - |
| arita | 0 | 10 | 0.0% | 4.4 | 7.6% | - |
| beijing | 0 | 10 | 0.0% | 6.9 | 4.1% | - |
| budapest | 0 | 10 | 0.0% | 6.6 | 4.4% | - |
| jaegerspris-nordskov | 0 | 10 | 0.0% | 9.7 | 2.7% | kongeegen (i4, p10) |
| gliniak | 0 | 10 | 0.0% | 5.9 | 5.2% | ancient tree (i1, p18) |
| barcelona | 0 | 10 | 0.0% | 5.9 | 5.2% | judas barcelona (i1, p9) |
| milan | 0 | 10 | 0.0% | 4.9 | 7.1% | - |

- Plus 192 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: brussels, vienna, cadiz, pamplona, cagliari, glasgow, ede, hinode.

## 2026-11-07 (previous UTC day)

**Today: nothing here needs you.** The blocks below are the standing picture.

**The numbers that matter** (this week against the week before; strangers only)

| Number | Why | This week | Week before |
|---|---|---:|---:|
| New website visitors | people | 52 | 64 |
| ... of which from search | every search engine | 22 | 13 |
| ... from Google | Google's recovery | 13 | 3 |
| ... from Bing | Bing | 3 | 6 |
| Website visitors who came back | people who stay | 12 | 13 |
| App downloads (first-time) | people | 23 | 41 |
| New accounts | people | 11 | 8 |
| Phones back within 30 days | people who stay | 4 of 6 | 9 of 13 |
| Trees saved to Want to go | intent | 4 | 0 |
| Trees collected | goal 1: stood at a tree | 7 | 0 |
| Readers' contributions | data: trees, photos, corrections, votes | 4 | 7 |
| Shares (app and web) | word of mouth, since 10-30 | 2 | 0 |
| Visits from a shared link | what sharing brings | 2 | 0 |

Website visitors are Google Analytics' count, so only people who accepted the cookie bar; a visitor who comes back on another browser or device counts as new, and GA cannot leave our own visits out, so read the came-back row as a direction, not a count. The 30-day row is the phones that arrived five weeks ago, so it moves slowly.

**Quality**: Web orange, iOS red, Android not live yet, Backup red. Backup: Hidde's one-time setup in BACKUP_RESTORE.md.

| | Web | iOS | Android |
|---|---|---|---|
| Next version | green | red: iOS build failure on main | grey: not live yet |
| Live | orange: 1 new error type(s), first "ResizeObserver loop completed with undelivered notifications" in inline | green | grey: not live yet |

**Plus question** (2 answers, 0 new; 1 asked to be told; 1 wrote an idea, read them with `python3 scripts/plus_answers.py`; up to two each)

| Choice | Picked by |
|---|---:|
| Recommended tree walks for a city trip | 1 |
| Something else | 1 |

**Day by day, the last seven days** (strangers only; visitors are Google Analytics', so only people who accepted the cookie bar)

| | 11-01 | 11-02 | 11-03 | 11-04 | 11-05 | 11-06 | 11-07 | **7 days** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Visitors | 8 | 11 | 10 | 12 | 8 | 5 | 2 | **56** |
| New accounts | 4 | 3 | 0 | 3 | 1 | 0 | 0 | **11** |
| Saves | 1 | 1 | 1 | 0 | 1 | 0 | 0 | **4** |
| Android waitlist | 1 | 0 | 1 | 0 | 1 | 0 | 0 | **3** |
| App downloads | 5 | 4 | 2 | 4 | 0 | 4 | – | **19** |
| App phones | 8 | 6 | 6 | 8 | 2 | 5 | 4 | **31** |
| Trees opened in the app | 35 | 21 | 7 | 88 | 7 | 8 | 5 | **171** |
| Trees collected | 0 | 5 | 0 | 1 | 0 | 0 | 0 | **6** |
| Trees sent | 0 | 0 | 0 | 0 | 1 | 0 | 0 | **1** |
| Feedback | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| Ambassador asks | 1 | 1 | 0 | 1 | 0 | 0 | 0 | **3** |
| App photos | 0 | 0 | 0 | 1 | 0 | 0 | 1 | **2** |
| Tree notes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| App Store reviews | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
- – means the source has not reported that day yet (Apple's downloads arrive a day or two late), not zero.

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Waiting for you** (what the runs left for you since 2026-11-07)

- 258 email addresses ready to mail (archive 2, nature 9, guide 9, press 135, source 65, council 16, tourism 7, society 7, other 5, garden 3); **the night run found no new contacts in two days**
- iOS scheduled runs keep failing; look at the xcresult artifact of run 42412097686.
- the daily task "publish-held-trees-daily" can be switched off under Scheduled; new trees now reach the app straight from the night run's write passes.
- next app session should fix the three before build 41.

**What readers gave us, and it went live**

| Day | Reader | Tree | Where | What | Page |
|---|---|---|---|---|---|
| 11-06 | A | The Rockface Sycamore of Cramond | Edinburgh | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/edinburgh/rockface-sycamore-of-cramond) |
| 11-06 | B | The Three Atlas Cedars of Préfargier | La Tène | a reader's photograph, published beside the one it had | [live](https://ancienttrees.app/la-tene/three-atlas-cedars-of-prefargier) |
- From 2 readers: reader A 1, reader B 1.

**Searched yesterday:** munchen, traubeneiche.

**Search**

Google, the last 10 days it will give us (2-3 days behind; the newest row is still filling, so it reads better than it is):

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-29 | 0 | 38 | 0.0% | 28.4 |
| 10-30 | 2 | 29 | 6.9% | 24.1 |
| 10-31 | 0 | 38 | 0.0% | 21.5 |
| 11-01 | 5 | 371 | 1.3% | 10.1 |
| 11-02 | 23 | 1274 | 1.8% | 9.0 |
| 11-03 | 31 | 1192 | 2.6% | 8.2 |
| 11-04 | 14 | 261 | 5.4% | 9.9 |
| 11-05 | 1 | 23 | 4.3% | 34.1 |
| 11-06 | 1 | 35 | 2.9% | 36.6 |
| 11-07 *partial* | 2 | 30 | 6.7% | 36.8 |
| **window** | **79** | **3291** | **2.4%** | |
- Top queries (10d): alte bäume in der nähe (i10, p8); ancient trees (i12, p16); ancienttree (i1, p3); istanbul (i1, p1); leuven, belgium (i1, p4)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-30 | 90 | 10 | 11.1% |
| 10-31 | 90 | 4 | 4.4% |
| 11-01 | 2225 | 8 | 0.4% |
| 11-02 | 146 | 6 | 4.1% |
| 11-03 | 121 | 3 | 2.5% |
| 11-04 | 133 | 3 | 2.3% |
| 11-05 | 132 | 9 | 6.8% |
| **7 days** | **2937** | **43** | **1.5%** |
- Week before: 676 impressions, 28 clicks. No Bing demotion in sight.
- Top Bing queries: oldest tree china (c8/i4, p12); picture of the tree in helsinki city center that was preserved (c3/i2, p4); ancient trees app (c2/i8, p5); fig tree in square alicante (c2/i4, p4); palma del cile (c2/i2, p6); cipresso calvo indro montanelli milano (c2/i2, p8); big trees of quebec city (c2/i1, p2); mit newton apple tree address (c2/i1, p2)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers. Bing's data lags about two days.

---

**For the night run, not for you.** You can stop reading here.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 11-07T06:01 | 17.5 | 21 | 10 | 2 | La Palma +4, Ayutthaya +2, Horta +2, Bar +1, +33 more |
| 11-07T13:20 | 22.8 | 14 | 18 | 1 | Salt Lake City +4, Chicago +3, Tucson +3, Fort Worth +2, +2 more |
| 11-07T18:07 | 5.0 | 0 | 3 | 2 | - |
| 11-08T00:56 | 4.3 | 0 | 6 | 1 | - |
| 11-08T01:03 | 3.2 | 0 | 6 | 1 | - |
| **5 runs** | **53** | **35** | **43** | | |

- 3 of 5 produced no trees; 1 to 2 commands refused per run; last build that went live: 4h ago.

**What they made**

- Sintra verify pass: wall, claim released; LOG: iOS FlowWalk failure noted
- Sintra verify pass: nothing new, wall for 48h; LOG, cost
- Photographs readers sent, queued for a look; vouched ones live
- Record when each page last changed
- Salt Lake City verify: 2 University of Utah trees verified, not written; LOG
- Record when each page last changed
- Coimbra verify: nothing new, claim released, wall; LOG
- London: lon_031 is lon_002 The Royal Oak (10 m), folded into blocked leads, not written
- Chicago: three ranked trees of Bunker Hill Woods, the third sugar maple, second bitternut hickory and champion red maple
- Salt Lake City: four more state champions, the Murray arboretum halfelm, pear and alder and the South Jordan willow
- Cost line for the 2026-11-07 write pass
- New York: the Davis hybrid oak of Stuyvesant Place, Staten Island
- Chattanooga: the Grace Episcopal water and willow oaks
- Tucson: three University of Arizona heritage trees (pistache, rock fig, Sinaloan albizia)

**Reader photographs in a strip, live first, not yet looked at** (1)

| Day | Tree | Where | Undo |
|---|---|---|---|
| 11-06 | The Rockface Sycamore of Cramond | Edinburgh | `sightings_publish.py --unstrip 4b28d99e-e0f2-4572-b851-23dd79e73031` |

Machine: 8 chain attempts yesterday, 5 got real work time (~73 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Search work lists**

- Top pages (10d): / (c7/i87); /de (c3/i27); /united-states/maryland (c3/i24); /seville (c2/i46); /malaga (c2/i24)
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
| Impressions | 3391 |
| Clicks | 79 |
| Pages that got at least one impression | 1088 |
| Impressions on the proven cities | 2558 |

- 423 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 3391 trees Google may index, 1299 kept out for lacking a photo and an exact pin, 5907 pages on the noindex list.

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
| tokyo | 1 | 57 | 1.8% | 7.5 | 3.7% | ginkgo sperm (i7, p10) |
| palermo | 1 | 55 | 1.8% | 7.7 | 3.7% | - |
| berlin | 0 | 55 | 0.0% | 5.7 | 5.5% | che albero è (i1, p4) |
| tenerife | 1 | 52 | 1.9% | 13.6 | 1.5% | drago milenario (i3, p12) |
| singapore | 1 | 50 | 2.0% | 9.2 | 2.9% | bodhi tree singapore (i3, p5) |
| lisbon | 1 | 49 | 2.0% | 5.8 | 5.4% | lisbon trees (i2, p4) |
| south-korea | 1 | 42 | 2.4% | 7.9 | 3.5% | oldest tree in korea (i4, p6) |
| fulufjallet | 0 | 42 | 0.0% | 8.1 | 3.5% | old tjikko (i19, p9) |
| united-states | 3 | 39 | 7.7% | 10.2 | 2.4% | oldest tree in oregon (i5, p13) |
| copenhagen | 1 | 39 | 2.6% | 11.9 | 1.8% | trees in copenhagen (i5, p19) |
| fukuoka | 2 | 32 | 6.2% | 10.3 | 2.4% | gingkosidi (i6, p32) |
| munich | 1 | 30 | 3.3% | 5.0 | 6.9% | a monaco di baviera? (i1, p20) |
| london | 0 | 30 | 0.0% | 7.0 | 4.0% | chestnut london (i1, p5) |
| olympic-national-park | 1 | 28 | 3.6% | 13.6 | 1.5% | duncan cedar (i16, p9) |
| sequoia-national-park | 0 | 28 | 0.0% | 19.5 | 0.8% | washington tree (i10, p11) |
| malaga | 2 | 27 | 7.4% | 13.9 | 1.4% | malaga tree (i3, p3) |
| new-york | 1 | 27 | 3.7% | 7.2 | 3.9% | - |
| paris | 0 | 27 | 0.0% | 6.1 | 4.9% | trees in paris (i1, p9) |
| kyoto | 1 | 24 | 4.2% | 12.3 | 1.7% | - |
| cambridge | 0 | 24 | 0.0% | 26.9 | 0.5% | newtons apple tree (i2, p50) |
| brisbane | 0 | 23 | 0.0% | 7.9 | 3.5% | banyan tree (i2, p12) |
| netherlands | 0 | 22 | 0.0% | 9.6 | 2.7% | ja (i1, p5) |
| takayama | 0 | 21 | 0.0% | 8.0 | 3.5% | takayama ginkgo tree (i2, p7) |
| alishan | 0 | 20 | 0.0% | 7.5 | 3.8% | xianglin sacred tree (i5, p4) |
| chishang | 0 | 20 | 0.0% | 14.2 | 1.4% | takeshi kaneshiro tree (i7, p7) |
| alicante | 0 | 20 | 0.0% | 5.8 | 5.3% | - |
| monterey | 0 | 19 | 0.0% | 31.6 | 0.4% | lone cypress (i4, p51) |
| porto | 0 | 19 | 0.0% | 5.0 | 7.0% | - |
| rome | 0 | 19 | 0.0% | 4.5 | 7.5% | oldest tree in rome (i3, p1) |
| bath | 1 | 18 | 5.6% | 6.8 | 4.2% | tree in bath (i1, p9) |
| coimbra | 0 | 18 | 0.0% | 6.5 | 4.5% | - |
| dublin | 0 | 17 | 0.0% | 7.0 | 4.0% | - |
| montreal | 3 | 16 | 18.8% | 4.5 | 7.5% | - |
| amsterdam | 0 | 16 | 0.0% | 6.4 | 4.6% | - |
| hong-kong | 1 | 15 | 6.7% | 6.7 | 4.3% | oldest tree in hong kong (i1, p9) |
| taiwan | 0 | 15 | 0.0% | 13.6 | 1.5% | oldest tree in taiwan (i3, p6) |
| luxembourg-city | 0 | 15 | 0.0% | 3.3 | 10.0% | - |
| edinburgh | 0 | 15 | 0.0% | 6.7 | 4.3% | - |
| perth | 0 | 15 | 0.0% | 8.1 | 3.5% | - |
| seoul | 1 | 14 | 7.1% | 7.4 | 3.8% | - |
| athens | 0 | 14 | 0.0% | 4.3 | 7.7% | - |
| madrid | 0 | 14 | 0.0% | 10.6 | 2.3% | - |
| boston | 0 | 14 | 0.0% | 8.2 | 3.4% | - |
| austin | 0 | 14 | 0.0% | 15.1 | 1.2% | old tree (i2, p28) |
| toronto | 0 | 13 | 0.0% | 6.8 | 4.2% | - |
| kagoshima | 0 | 13 | 0.0% | 7.8 | 3.6% | cycad ovule (i1, p10) |
| venice | 1 | 12 | 8.3% | 5.7 | 5.7% | are there trees in venice (i1, p11) |
| istanbul | 2 | 12 | 16.7% | 7.0 | 4.0% | istanbul (i1, p1) |
| germany | 0 | 12 | 0.0% | 13.0 | 1.6% | trees germany (i2, p48) |
| switzerland | 0 | 12 | 0.0% | 10.0 | 2.5% | oldest tree in switzerland (i1, p1) |
| san-francisco | 0 | 12 | 0.0% | 12.1 | 1.8% | - |
| nara | 0 | 11 | 0.0% | 5.5 | 6.1% | - |
| the-hague | 0 | 11 | 0.0% | 4.9 | 7.1% | haag (i1, p1) |
| reykjavik | 1 | 10 | 10.0% | 5.6 | 5.8% | oldest tree in iceland (i1, p3) |
| jaegerspris-nordskov | 0 | 10 | 0.0% | 9.7 | 2.7% | kongeegen (i4, p10) |
| gliniak | 0 | 10 | 0.0% | 5.9 | 5.2% | ancient tree (i1, p18) |
| kanazawa | 0 | 10 | 0.0% | 6.1 | 4.9% | tabunoki (i1, p9) |
| oahu | 0 | 10 | 0.0% | 7.9 | 3.5% | hitachi tree hawaii (i2, p9) |
| krakow | 0 | 10 | 0.0% | 13.1 | 1.6% | - |

- Plus 204 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: barcelona, brussels, vienna, cadiz, pamplona, prague, cagliari, glasgow.

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

