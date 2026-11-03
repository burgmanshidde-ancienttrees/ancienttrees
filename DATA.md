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
   live. Ambassador requests keep arriving (Pamplona, New Orleans; 56 total).
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

