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

## 2026-10-16 (previous UTC day)

**Today: an android waitlist signup arrived yesterday (22 total).**

**Conclusion: the numbers that matter now** (this week against the week before)

| Number | Why it counts | This week | Week before |
|---|---|---:|---:|
| Stood at a tree (app collections) | goal 1, the north star | 1 | 10 |
| New phones that opened a tree on day one | activation | 12 of 16 (75%) | 4 of 7 (57%) |
| New phones that tapped Take me there on day one | activation | 2 of 16 (12%) | 0 of 7 (0%) |
| Phones back within a week | retention | 3 of 7 (43%) | 7 of 13 (54%) |
| New accounts (strangers) | people collected | 4 | 3 |
| Readers' trees and photographs live | data collected | 2 | 4 |
| Arrivals from search, every engine (8 days) | traction | 110 | - |

1 collection at a tree this week against 10 the week before, a handful: read it as a count, not a trend. The weakest link is tapping Take me there on day one (2 of 16): that step is the work, more traffic only pours more people into it.

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Did the product happen**

| Action | Yesterday | 7 days | Last |
|---|---:|---:|---|
| signin-open | 2 | 12 | yesterday |
| app-cta | 2 | 15 | yesterday |
| signin-oauth | 0 | 0 | 8 days ago |
| signin-done | 0 | 0 | 10 days ago |
| directions | 0 | 0 | 8 days ago |
| search-home | 1 | 4 | yesterday |
| app-open | 1 | 4 | yesterday |
| suggestion-submit | 0 | 0 | 22 days ago |
| home-country | 0 | 3 | 2 days ago |
| home-fav | 0 | 0 | 8 days ago |
| waitlist-submit | 1 | 2 | yesterday |
| signin-link-sent | 0 | 0 | 22 days ago |
| save | 0 | 0 | 15 days ago |
| search-explore | 2 | 2 | yesterday |
| home-dir-tree | 0 | 1 | 2 days ago |
| visit | 0 | 0 | 27 days ago |
| app-page-badge | 0 | 0 | 8 days ago |
| home-species | 0 | 0 | 26 days ago |
| sponsor-open | 0 | 1 | 2 days ago |
| home-dir-species | 0 | 1 | 6 days ago |
| walks-app | 0 | 0 | 24 days ago |
| worthit-report | 0 | 0 | 23 days ago |
| worthit-report detail | 0 | 0 | 23 days ago |
| worthit-worth it | 0 | 0 | 27 days ago |
| worthit-not worth it | 0 | 0 | never |
| **all** | **9** | **45** | |

**Searched yesterday:** brighton (2 times).

| Day | Accounts | Android waitlist | Saves | Trees sent | Feedback | Ambassador asks |
|---|---:|---:|---:|---:|---:|---:|
| 10-10 | 1 | 1 | 0 | 0 | 0 | 0 |
| 10-11 | 1 | 0 | 0 | 0 | 0 | 0 |
| 10-12 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-13 | 1 | 0 | 0 | 0 | 2 | 0 |
| 10-14 | 1 | 0 | 0 | 0 | 0 | 0 |
| 10-15 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-16 | 0 | 1 | 0 | 0 | 0 | 0 |
| 10-17 | 0 | 0 | 0 | 0 | 0 | 0 |
| **7 days** | **4** | **2** | **0** | **0** | **2** | **0** |

| Ambassadors | Yesterday | 7 days | Total |
|---|---:|---:|---:|
| Granted | 0 | 1 | 6 |
| Invitations sent (app contributors) | 0 | 1 | 7 |
| Open-seat requests answered | 0 | 0 | 0 |
- New in 7 days: Kerry Pickett (Brighton) since 2026-10-10.
- Android waitlist: 22 total, newest yesterday
- Submissions: 35 total (19 trees sent, 16 feedback), newest 4 days ago
- Accounts:    28 total, newest 3 days ago

**What readers told us** (7 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 10-13 | sev_009 (The Fig of the Glorieta d | worth it | - | c922 | - |
| 10-13 | - | Location not working on iOS, permi | - | c922 | open_question |

- 2 rows from 1 accounts.

**The funnel, as rates**
- Seen to clicked: 3.2% (8 of 251) vs 4.3% the week before
- Pages per visit: 1.3 (7390 visits, 9310 pageviews since 2026-09-19)
- Visits that did something: 10.9% (809 actions on 7390 visits)

**What people did in the app**

| What | Yesterday | 7 days | Last |
|---|---:|---:|---|
| app_open | 31 | 99 | yesterday |
| tab | 28 | 47 | yesterday |
| tree_opened | 62 | 143 | yesterday |
| directions | 0 | 1 | 3 days ago |
| tree_saved | 1 | 4 | yesterday |
| tree_visited | 0 | 1 | 6 days ago |
| sighting_recorded | 0 | 1 | 6 days ago |
| sync_skipped | 0 | 0 | never |
| sync_failed | 0 | 0 | never |
| location | 2 | 4 | yesterday |
| **all** | **124** | **300** | |
- Measuring since 2026-08-30, when Measure.swift went in. Unlinked to any account by design: an install id, the app version and the OS, nothing else.
- 90 installs have ever sent anything. An install id is made fresh on each install, so this is an upper bound on people, not a count of them.
- Yesterday came from 4 installs, and the busiest made 83 of 4 events (2075%). One install making most of a day is what our own reinstall looks like: add its id to excluded_installs in data/app-measure.json if it is ours.
- Tabs opened (7d): My trees 18; Discover 18; Map 11
- Active phones: 4 in the last day, 19 in the last 7 days, 61 in the last 30 days.
- Coming back: 27 of those 61 phones opened the app on more than one day (44%).
- Trees opened by the most phones (7d): The Fig of the Glorieta de Goya (Seville) 3; The Ombú of La Cartuja (Seville) 2; The Grapefruit of the Cartuja Monastery (Seville) 1; The Cardón of the Expo (Seville) 1; The Mulberry of the Alamillo Cortijo (Seville) 1
- Where the phones are (30d): United States 14; United Kingdom 7; Portugal 6; The Netherlands 6; Italy 4; Spain 4
- Trees recorded (7d): a tree we map 1
  A sighting reaches our database only through an account. Signed out it stays on the phone, so this count can run ahead of the trees and photographs we actually receive.

**Trees collected in the app** (7 days, a person standing at the tree)

| Day | Tree | Where | Install | Build | Signed in |
|---|---|---|---|---|---|
| 10-11 | The Lagunària de la Llotja | Palma de Mallorca | A98A | ? | ? |

**The app as a builder reads it** (this week against the week before; the weakest row is the work)

| Link | This week | Week before |
|---|---|---|
| New phones | 16 | 7 |
| First day: opened a tree | 12 of 16 (75%) | 4 of 7 (57%) |
| First day: opened a tree near them | 0 of 1 (0%) | - |
| First day: allowed location | 2 of 2 (100%) | - |
| First day: Take me there | 2 of 16 (12%) | 0 of 7 (0%) |
| First day: collected a tree | 1 of 16 (6%) | 1 of 7 (14%) |
| Back within a week | 3 of 7 (43%) | 7 of 13 (54%) |
| Trees collected (all phones) | 1 | 10 |
- Near and location count only phones on a version that sends them (from 2026-10-10); a dash means none yet.
- Back within a week looks at the phones that arrived a week earlier, so each has had its seven days.

**App Store downloads** (Apple's own count, not PostHog)

| Day | Downloads |
|---|---:|
| 2026-10-08 | 4 |
| 2026-10-09 | 4 |
| 2026-10-10 | 5 |
| 2026-10-12 | 1 |
| 2026-10-13 | 2 |
| 2026-10-15 | 1 |
| **6 days** | **17** |
- First-time downloads only, which is what App Store Connect's Trends screen counts; redownloads and updates are not in this table.

**Where the downloads came from** (7 days, Apple's attribution)

| Came from | Via | Downloads |
|---|---|---:|
| App Store search | - | 8 |
| Web referrer | - | 5 |
| App referrer | - | 3 |
| App Store browse | - | 1 |
| **window** | | **17** |
- Countries: US (6); GB (4); NL (2); BE (1); ES (1); IE (1)
- Apple's own source split, first-time downloads only. "Web referrer" with our own domain is the site's app page; "App Store search" is somebody who typed into the store. "Unavailable" is Apple's word for a source it could not attribute.

**App crashes** (last 7 days, store builds; MetricKit, a sample)

| Crashes | Kind | Build | Where | Phones | Last | Fix |
|---:|---|---|---|---:|---|---|
| 37 | crash | 1.0.2 (20) | Swift runtime failure: Index out of range < static MyVotes.treeId(_:) (WorthIt.swift:84) < MyVotes.load(account:) (WorthIt.swift:103) | 1 | 2026-10-16 | fixed in build 35, released; contained server-side |
- Builds not from the App Store (Xcode or review): 9 report(s) on build 25.

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-07 | 0 | 47 | 0.0% | 34.7 |
| 10-08 | 5 | 35 | 14.3% | 21.8 |
| 10-09 | 3 | 37 | 8.1% | 49.5 |
| 10-10 | 0 | 35 | 0.0% | 29.8 |
| 10-11 | 1 | 32 | 3.1% | 31.7 |
| 10-12 | 1 | 26 | 3.8% | 30.3 |
| 10-13 | 1 | 34 | 2.9% | 38.7 |
| 10-14 | 1 | 39 | 2.6% | 36.9 |
| 10-15 | 2 | 40 | 5.0% | 37.0 |
| 10-16 *partial* | 2 | 45 | 4.4% | 46.1 |
| **window** | **16** | **370** | **4.3%** | |
- Top queries (10d): pokaz na mapie (i1, p1); amsterdam trees (i1, p81); ancient douglas fir tree (i1, p48); ancient tree (i1, p89); ancient trees (i1, p82)
- Top pages (10d): / (c4/i14); /brussels/oldest-tree (c2/i3); /leiden/beets-beech-of-the-burcht (c2/i2); /app (c1/i4); /de/berlin/englischer-garten-wingnut (c1/i2)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'big sherman tree' (i2, p69)
    - 'pokaz na mapie' (i1, p1)
    - 'bunya tree' (i1, p97)
    - 'chapina garden' (i1, p13)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-09 | 47 | 2 | 4.3% |
| 10-10 | 57 | 1 | 1.8% |
| 10-11 | 53 | 2 | 3.8% |
| 10-12 | 81 | 3 | 3.7% |
| 10-13 | 90 | 2 | 2.2% |
| 10-14 | 94 | 3 | 3.2% |
| 10-15 | 78 | 8 | 10.3% |
| **7 days** | **500** | **21** | **4.2%** |
- Week before: 480 impressions, 19 clicks. No Bing demotion in sight.
- Top Bing queries: fig tree in square alicante (c2/i4, p4); big trees of quebec city (c2/i1, p2); oak tree in zurich (c1/i4, p2); how old are the trees in queen square bristol (c1/i4, p3); trees in the plaza dus burgos seville (c1/i3, p5); berlin tree (c1/i2, p1); oldest tree in belfast (c1/i2, p1); french trees found in paris (c1/i2, p6)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers; their arrivals are columns in the Cloudflare table. Bing's data lags about two days.

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 410 |
| Clicks | 16 |
| Pages that got at least one impression | 256 |
| Impressions on the proven cities | 278 |

- 303 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 2951 trees Google may index, 748 kept out for lacking a photo and an exact pin, 2766 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 1715 | 43 | 91 | 0.05 | 5 |
| Not yet rich | 509 | 29 | 44 | 0.09 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| sequoia-national-park | 0 | 32 | 0.0% | 73.5 | 0.4% | general sherman tree california (i5, p74) |
| brussels | 2 | 10 | 20.0% | 12.9 | 1.6% | klint white mulberry (i2, p52) |

- Plus 257 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| before 2026-09-23 | The Twisted Muku of Omiya Gate, Kyoto  | Kyoto | - | publish | - |
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
| 2026-10-05 | London Plane in Paris | Paris | 88% girth | publish | publish (2026-10-13, session: 'follow your suggestion') |

1 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.
- Seen, not clicked: /sequoia-national-park/general-sherman-tree (c0/i31, 0.0%) for general sherman tree california (i5, p74); sequoia national park general sherman (i3, p64); sherman tree (i2, p80)

**Who they are**
Audience, 28 days of search (523 clicks, 20275 impressions):
- Countries: usa c71/i4213; esp c51/i1709; nld c47/i1096; deu c46/i1210; gbr c41/i1560
- Devices: MOBILE c383/i12547; DESKTOP c136/i7473; TABLET c4/i255
- Landing pages: / c23/i209; /leuven c7/i45; /prague c7/i132; /seville c6/i93; /bath/plane-trees-of-the-circus c5/i96

Web Analytics (beacon, cookieless), people only.
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews | From Google | From Bing | From DuckDuckGo | From Yahoo | From Ecosia |
|---|---:|---:|---:|---:|---:|---:|---:|
| 10-09 | 60 | 150 | 0 | 10 | 10 | 10 | 0 |
| 10-10 | 40 | 140 | 10 | 0 | 0 | 0 | 0 |
| 10-11 | 30 | 90 | 0 | 0 | 10 | 0 | 0 |
| 10-12 | 20 | 90 | 0 | 0 | 0 | 10 | 0 |
| 10-13 | 20 | 90 | 0 | 0 | 0 | 0 | 0 |
| 10-14 | 10 | 70 | 0 | 0 | 0 | 0 | 0 |
| 10-15 | 40 | 170 | 10 | 10 | 0 | 0 | 0 |
| 10-16 | 50 | 140 | 10 | 0 | 20 | 0 | 0 |
| **window** | **270** | **940** | **30** | **20** | **40** | **20** | **0** |
- Top paths: /explore (50); /lisbon (40); /de/cologne/moltke-lime-of-the-kahnweiher (20); / (20); /contribute (20); /perth (20); /brighton/preston-twin (10); /luxembourg-city/copper-beech-of-parc-pescatore (10); /lisbon/paineira-of-rua-dos-jeronimos (10); /london/greenwich-park-shagbark-hickory (10); /london/sweet-chestnut-of-greenwich-park (10); /amersfoort/copper-beech-of-the-old-library (10)
- Referrers: (direct) (150); ancienttrees.app (670); duckduckgo.com (40); www.google.com (30); bing.com (10); de.search.yahoo.com (10); localhost (10); uk.search.yahoo.com (10); www.bing.com (10)
- Moved between our own pages: 670 of 940 pageviews (71%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: NL (120); DE (110); PT (110); US (100); SG (90)
- Devices: mobile (520); desktop (410); tablet (10)
- Page load (8d): p50 1568ms, p90 5271ms

Links: external referrers (a link somebody actually clicked): localhost (10)
AI: arrivals from an assistant that cited us: none yet


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-16T05:01 | 2.9 | 0 | 2 | 0 | - |
| 10-16T08:41 | 18.6 | 0 | 8 | 1 | London |
| 10-16T14:17 | 33.7 | 0 | 7 | 1 | Berlin |
| 10-16T14:52 | 8.2 | 0 | 11 | 1 | Berlin |
| 10-16T18:12 | 4.8 | 0 | 5 | 1 | - |
| 10-16T19:13 | 7.5 | 0 | 3 | 0 | - |
| 10-16T21:25 | 3.5 | 0 | 4 | 0 | - |
| 10-16T22:25 | 4.9 | 0 | 4 | 0 | - |
| 10-17T01:35 | 8.0 | 0 | 4 | 0 | - |
| 10-17T02:36 | 3.0 | 0 | 4 | 0 | - |
| **10 runs** | **95** | **0** | **52** | | |

- 10 of 10 produced no trees; 1 to 1 commands refused per run; last build that went live: 0h ago.

**What they made**

- Log: fifth attempt, nothing shippable
- Log: fourth attempt, nothing shippable
- Log: later attempt, nothing shippable
- Log: 02:37 window, iOS sweep drift diagnosed, nothing shippable
- Log: third attempt, nothing shippable
- Log: later attempt, nothing shippable
- Log: 01:35 window, photo sweep, nothing shippable
- Photographs readers sent, queued for a look; vouched ones live
- Photo sweep: 40 trees asked of Commons, candidates queued
- Log: twenty-first attempt, nothing shippable
- Log: twentieth attempt, nothing shippable
- Log: nineteenth attempt, nothing shippable
- Log: eighteenth attempt, nothing shippable
- Log: seventeenth attempt, Cincinnati scouting retried, nothing shippable

**Photographs the night run approved** (41; the last column undoes one)

| Day | Tree | Where | Overrule |
|---|---|---|---|
| 10-15 | The Patriarch Tree | Ancient Bristlecone Pine Forest | `photo_apply.py hold abp_001` |
| 10-15 | The Dawn Redwood by the Kelvin Statue | Belfast | `photo_apply.py hold bfs_003` |
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
| 10-15 | The Queen's Park Champion Wych Elm | Brighton | `photo_apply.py hold bhm_005` |
| 10-15 | 1000jährige Eibe Gutau | Gutau | `photo_apply.py hold gut_001` |
| 10-15 | The Obertraun Dorfeibe | Hallstatt | `photo_apply.py hold hst_002` |
| 10-15 | The Bad Goisern Parish Church Yew | Hallstatt | `photo_apply.py hold hst_004` |
| 10-15 | Robert E. Lee Tree | Kings Canyon National Park | `photo_apply.py hold kcy_002` |
| 10-16 | The Battersea Park Hybrid Strawberry Tree | London | `photo_apply.py hold lon_025` |
| 10-16 | The Carshalton Plane | London | `photo_apply.py hold lon_028` |
| 10-16 | The Gunnersbury Park Black Mulberry | London | `photo_apply.py hold lon_030` |
| 10-15 | The Alzina d'en Pere | Mallorca | `photo_apply.py hold mlc_005` |
| 10-15 | The Moon Tree of Friendly Plaza | Monterey | `photo_apply.py hold mty_003` |
| 10-16 | The Magnolia of Hattie Carthan | New York | `photo_apply.py hold nyc_021` |
| 10-15 | The Ankerwycke Yew | Runnymede | `photo_apply.py hold ank_001` |
| 10-15 | The Katsura Fudo of Koganeyu | Sapporo | `photo_apply.py hold spr_002` |
| 10-16 | The Silver Poplars of Freiligrathpark | Vienna | `photo_apply.py hold vie_044` |

Machine: 9 chain attempts yesterday, 9 got real work time (~127 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

## 2026-10-15 (previous UTC day)

**Today: nothing here needs you.** The blocks below are the standing picture.

**Conclusion: the numbers that matter now** (this week against the week before)

| Number | Why it counts | This week | Week before |
|---|---|---:|---:|
| Stood at a tree (app collections) | goal 1, the north star | 1 | 10 |
| New phones that opened a tree on day one | activation | 12 of 17 (71%) | 4 of 6 (67%) |
| New phones that tapped Take me there on day one | activation | 2 of 17 (12%) | 1 of 6 (17%) |
| Phones back within a week | retention | 3 of 6 (50%) | 8 of 13 (62%) |
| New accounts (strangers) | people collected | 4 | 3 |
| Readers' trees and photographs live | data collected | 3 | 11 |
| Arrivals from search, every engine (8 days) | traction | 90 | - |

1 collection at a tree this week against 10 the week before, a handful: read it as a count, not a trend. The weakest link is tapping Take me there on day one (2 of 17): that step is the work, more traffic only pours more people into it.

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**Did the product happen**

| Action | Yesterday | 7 days | Last |
|---|---:|---:|---|
| signin-open | 1 | 27 | yesterday |
| app-cta | 3 | 17 | today |
| signin-oauth | 0 | 1 | 7 days ago |
| signin-done | 0 | 0 | 9 days ago |
| directions | 0 | 1 | 7 days ago |
| search-home | 0 | 4 | 2 days ago |
| app-open | 1 | 5 | yesterday |
| suggestion-submit | 0 | 0 | 21 days ago |
| home-country | 1 | 4 | yesterday |
| home-fav | 0 | 1 | 7 days ago |
| signin-link-sent | 0 | 0 | 21 days ago |
| save | 0 | 0 | 14 days ago |
| waitlist-submit | 0 | 1 | 6 days ago |
| home-dir-tree | 1 | 1 | yesterday |
| visit | 0 | 0 | 26 days ago |
| sponsor-open | 1 | 1 | yesterday |
| app-page-badge | 0 | 1 | 7 days ago |
| home-species | 0 | 0 | 25 days ago |
| search-explore | 0 | 0 | 14 days ago |
| home-dir-species | 0 | 1 | 5 days ago |
| walks-app | 0 | 0 | 23 days ago |
| worthit-report | 0 | 0 | 22 days ago |
| worthit-report detail | 0 | 0 | 22 days ago |
| worthit-worth it | 0 | 0 | 26 days ago |
| worthit-not worth it | 0 | 0 | never |
| **all** | **8** | **65** | |

**Searched yesterday:** nothing.

| Day | Accounts | Android waitlist | Saves | Trees sent | Feedback | Ambassador asks |
|---|---:|---:|---:|---:|---:|---:|
| 10-09 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-10 | 1 | 1 | 0 | 0 | 0 | 0 |
| 10-11 | 1 | 0 | 0 | 0 | 0 | 0 |
| 10-12 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-13 | 1 | 0 | 0 | 0 | 2 | 0 |
| 10-14 | 1 | 0 | 0 | 0 | 0 | 0 |
| 10-15 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-16 | 0 | 0 | 0 | 0 | 0 | 0 |
| **7 days** | **4** | **1** | **0** | **0** | **2** | **0** |

| Ambassadors | Yesterday | 7 days | Total |
|---|---:|---:|---:|
| Granted | 0 | 1 | 6 |
| Invitations sent (app contributors) | 0 | 2 | 7 |
| Open-seat requests answered | 0 | 0 | 0 |
- New in 7 days: Kerry Pickett (Brighton) since 2026-10-10.
- Android waitlist: 21 total, newest 6 days ago
- Submissions: 35 total (19 trees sent, 16 feedback), newest 3 days ago
- Accounts:    28 total, newest 2 days ago

**What readers told us** (7 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 10-13 | sev_009 (The Fig of the Glorieta d | worth it | - | c922 | - |
| 10-13 | - | Location not working on iOS, permi | - | c922 | open_question |

- 2 rows from 1 accounts.

**The funnel, as rates**
- Seen to clicked: 3.6% (8 of 223) vs 4.5% the week before
- Pages per visit: 1.3 (6950 visits, 8780 pageviews since 2026-09-18)
- Visits that did something: 11.7% (810 actions on 6950 visits)

**What people did in the app**

| What | Yesterday | 7 days | Last |
|---|---:|---:|---|
| app_open | 26 | 77 | today |
| tab | 4 | 20 | yesterday |
| tree_opened | 38 | 91 | yesterday |
| directions | 0 | 3 | 2 days ago |
| tree_saved | 2 | 3 | yesterday |
| tree_visited | 0 | 1 | 5 days ago |
| sighting_recorded | 0 | 1 | 5 days ago |
| sync_skipped | 0 | 0 | never |
| sync_failed | 0 | 0 | never |
| location | 1 | 2 | yesterday |
| **all** | **71** | **198** | |
- Measuring since 2026-08-30, when Measure.swift went in. Unlinked to any account by design: an install id, the app version and the OS, nothing else.
- 87 installs have ever sent anything. An install id is made fresh on each install, so this is an upper bound on people, not a count of them.
- Yesterday came from 5 installs, and the busiest made 61 of 5 events (1220%). One install making most of a day is what our own reinstall looks like: add its id to excluded_installs in data/app-measure.json if it is ours.
- Tabs opened (7d): My trees 8; Discover 8; Map 4
- Active phones: 5 in the last day, 22 in the last 7 days, 58 in the last 30 days.
- Coming back: 27 of those 58 phones opened the app on more than one day (47%).
- Trees opened by the most phones (7d): The Fig of the Glorieta de Goya (Seville) 2; The Ombú of La Cartuja (Seville) 1; The Cardón of the Expo (Seville) 1; The Grapefruit of the Cartuja Monastery (Seville) 1; The Mulberry of the Alamillo Cortijo (Seville) 1
- Where the phones are (30d): United States 14; United Kingdom 7; Portugal 5; The Netherlands 5; Italy 4; Spain 4
- Trees recorded (7d): a tree we map 1
  A sighting reaches our database only through an account. Signed out it stays on the phone, so this count can run ahead of the trees and photographs we actually receive.

**Trees collected in the app** (7 days, a person standing at the tree)

| Day | Tree | Where | Install | Build | Signed in |
|---|---|---|---|---|---|
| 10-11 | The Lagunària de la Llotja | Palma de Mallorca | A98A | ? | ? |

**The app as a builder reads it** (this week against the week before; the weakest row is the work)

| Link | This week | Week before |
|---|---|---|
| New phones | 17 | 6 |
| First day: opened a tree | 12 of 17 (71%) | 4 of 6 (67%) |
| First day: opened a tree near them | 0 of 1 (0%) | - |
| First day: allowed location | 1 of 1 (100%) | - |
| First day: Take me there | 2 of 17 (12%) | 1 of 6 (17%) |
| First day: collected a tree | 2 of 17 (12%) | 1 of 6 (17%) |
| Back within a week | 3 of 6 (50%) | 8 of 13 (62%) |
| Trees collected (all phones) | 1 | 10 |
- Near and location count only phones on a version that sends them (from 2026-10-10); a dash means none yet.
- Back within a week looks at the phones that arrived a week earlier, so each has had its seven days.

**App Store downloads** (Apple's own count, not PostHog)

| Day | Downloads |
|---|---:|
| 2026-10-08 | 4 |
| 2026-10-09 | 4 |
| 2026-10-10 | 5 |
| 2026-10-12 | 1 |
| 2026-10-13 | 2 |
| **5 days** | **16** |
- First-time downloads only, which is what App Store Connect's Trends screen counts; redownloads and updates are not in this table.

**Where the downloads came from** (7 days, Apple's attribution)

| Came from | Via | Downloads |
|---|---|---:|
| App Store search | - | 7 |
| Web referrer | - | 5 |
| App referrer | - | 3 |
| App Store browse | - | 1 |
| **window** | | **16** |
- Countries: US (6); GB (4); BE (1); ES (1); IE (1); NL (1)
- Apple's own source split, first-time downloads only. "Web referrer" with our own domain is the site's app page; "App Store search" is somebody who typed into the store. "Unavailable" is Apple's word for a source it could not attribute.

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-06 | 1 | 45 | 2.2% | 34.5 |
| 10-07 | 0 | 47 | 0.0% | 34.7 |
| 10-08 | 5 | 35 | 14.3% | 21.8 |
| 10-09 | 3 | 37 | 8.1% | 49.5 |
| 10-10 | 0 | 35 | 0.0% | 29.8 |
| 10-11 | 1 | 32 | 3.1% | 31.7 |
| 10-12 | 1 | 26 | 3.8% | 30.3 |
| 10-13 | 1 | 34 | 2.9% | 38.7 |
| 10-14 | 1 | 39 | 2.6% | 36.9 |
| 10-15 *partial* | 1 | 20 | 5.0% | 38.6 |
| **window** | **14** | **350** | **4.0%** | |
- Top queries (10d): pokaz na mapie (i1, p1); alte bäume (i2, p28); ancient douglas fir tree (i1, p48); ancient tree (i1, p89); ancient trees (i1, p82)
- Top pages (10d): / (c5/i17); /brussels/oldest-tree (c2/i3); /app (c1/i5); /de/berlin/englischer-garten-wingnut (c1/i2); /cagliari/ficus-of-piazza-matteotti (c1/i1)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'alte bäume' (i2, p28)
    - 'big sherman tree' (i2, p69)
    - 'pokaz na mapie' (i1, p1)
    - 'araucaria norfolk' (i1, p88)
    - 'avenue de laune' (i1, p24)
    - 'bunya tree' (i1, p97)
    - 'chapina garden' (i1, p13)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-08 | 168 | 4 | 2.4% |
| 10-09 | 47 | 2 | 4.3% |
| 10-10 | 57 | 1 | 1.8% |
| 10-11 | 53 | 2 | 3.8% |
| 10-12 | 81 | 3 | 3.7% |
| 10-13 | 90 | 2 | 2.2% |
| 10-14 | 94 | 3 | 3.2% |
| **7 days** | **590** | **17** | **2.9%** |
- Week before: 312 impressions, 15 clicks. No Bing demotion in sight.
- Top Bing queries: trees in the plaza dus burgos seville (c1/i3, p5); remarkable trees copenhagen (c1/i2, p4); ancient trees in wiesbaden germany (c1/i2, p6); oldest live oak trees in new orleans (c1/i2, p6); french trees found in paris (c1/i2, p6); berlin tree (c1/i2, p1); oldest tree in belfast (c1/i2, p1); husalle lindens copenhagen (c1/i2, p3)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers; their arrivals are columns in the Cloudflare table. Bing's data lags about two days.

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 420 |
| Clicks | 14 |
| Pages that got at least one impression | 249 |
| Impressions on the proven cities | 299 |

- 267 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 2948 trees Google may index, 751 kept out for lacking a photo and an exact pin, 2802 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 1715 | 47 | 111 | 0.06 | 3 |
| Not yet rich | 490 | 28 | 39 | 0.08 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| prague | 0 | 49 | 0.0% | 5.6 | 5.9% | - |
| sequoia-national-park | 0 | 30 | 0.0% | 73.6 | 0.4% | general sherman tree california (i5, p74) |
| brussels | 2 | 10 | 20.0% | 12.9 | 1.6% | klint white mulberry (i2, p52) |

- Plus 256 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| before 2026-09-23 | The Twisted Muku of Omiya Gate, Kyoto  | Kyoto | - | publish | - |
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
| 2026-10-05 | London Plane in Paris | Paris | 88% girth | publish | publish (2026-10-13, session: 'follow your suggestion') |

1 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.
- Seen, not clicked: /sequoia-national-park/general-sherman-tree (c0/i28, 0.0%) for general sherman tree california (i5, p74); sequoia national park general sherman (i3, p64); sherman tree (i2, p80)

**Who they are**
Audience, 28 days of search (554 clicks, 22130 impressions):
- Countries: usa c75/i4661; esp c52/i1842; nld c47/i1170; deu c46/i1299; gbr c46/i1729
- Devices: MOBILE c402/i13773; DESKTOP c147/i8086; TABLET c5/i271
- Landing pages: / c24/i225; /leuven c7/i47; /prague c7/i139; /bath/plane-trees-of-the-circus c6/i112; /seville c6/i103

Web Analytics (beacon, cookieless), people only.
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews | From Google | From Bing | From DuckDuckGo | From Yahoo | From Ecosia |
|---|---:|---:|---:|---:|---:|---:|---:|
| 10-08 | 10 | 90 | 0 | 0 | 0 | 10 | 0 |
| 10-09 | 60 | 150 | 0 | 10 | 10 | 10 | 0 |
| 10-10 | 40 | 140 | 10 | 0 | 0 | 0 | 0 |
| 10-11 | 30 | 90 | 0 | 0 | 10 | 0 | 0 |
| 10-12 | 20 | 90 | 0 | 0 | 0 | 10 | 0 |
| 10-13 | 20 | 90 | 0 | 0 | 0 | 0 | 0 |
| 10-14 | 10 | 70 | 0 | 0 | 0 | 0 | 0 |
| 10-15 | 40 | 170 | 10 | 10 | 0 | 0 | 0 |
| **window** | **230** | **890** | **20** | **20** | **20** | **30** | **0** |
- Top paths: /explore (40); /leuven (30); /de/cologne/moltke-lime-of-the-kahnweiher (20); /contribute (20); /perth (20); / (20); /lisbon (20); /luxembourg-city/copper-beech-of-parc-pescatore (10); /glastonbury/glastonbury-thorn (10); /london/greenwich-park-shagbark-hickory (10); /london/sweet-chestnut-of-greenwich-park (10); /seville/orange-trees-of-the-patio-de-los-naranjos (10)
- Referrers: (direct) (130); ancienttrees.app (660); www.google.com (20); duckduckgo.com (20); bing.com (10); de.search.yahoo.com (10); localhost (10); uk.search.yahoo.com (10); search.yahoo.com (10); www.bing.com (10)
- Moved between our own pages: 660 of 890 pageviews (74%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: NL (120); US (120); DE (110); FR (80); PT (70)
- Devices: mobile (480); desktop (400); tablet (10)
- Page load (8d): p50 1599ms, p90 6164ms

Links: external referrers (a link somebody actually clicked): localhost (10)
AI: arrivals from an assistant that cited us: none yet


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-15T08:45 | 5.4 | 0 | 5 | 0 | - |
| 10-15T14:37 | 7.2 | 0 | 5 | 0 | - |
| 10-15T19:03 | 5.3 | 0 | 6 | 0 | - |
| 10-15T19:38 | 4.9 | 0 | 4 | 1 | - |
| 10-15T22:08 | 12.4 | 0 | 11 | 0 | - |
| 10-15T22:51 | 4.5 | 0 | 4 | 0 | - |
| 10-16T02:45 | 5.8 | 0 | 7 | 0 | - |
| 10-16T05:01 | 2.9 | 0 | 2 | 0 | - |
| **8 runs** | **48** | **0** | **44** | | |

- 8 of 8 produced no trees; 1 to 1 commands refused per run; last build that went live: 2h ago.

**What they made**

- Scout San Juan (stalled: no register); log
- Scout Buffalo (stalled: no heritage register); log
- Scout Allentown (stalled: no city register); log
- Scout Regensburg and Newark (stalled: no coordinates / no register); log
- Scout Windsor (stalled: no open tree-level register)
- Scout Phoenix (stalled: PDF-only list, no coordinates); release Nuremberg; log
- Scout note: Upper Austria Naturdenkmal dataset id
- Scout Hallstatt (stalled: no coordinates; Upper Austria dataset untried); log
- Photographs readers sent, queued for a look; vouched ones live
- Scout Belfast and Brighton (stalled: no register); log
- Scout Stratford-upon-Avon (stalled: TPO points only); log
- Scout Oxford (stalled: TPO points only); log
- Scout Bristol and Cardiff (stalled: no notable-tree register); log
- Scout Canterbury (stalled: TPO points only, no licence for ATI); log

**Photographs the night run approved** (64; the last column undoes one)

| Day | Tree | Where | Overrule |
|---|---|---|---|
| 10-15 | The Patriarch Tree | Ancient Bristlecone Pine Forest | `photo_apply.py hold abp_001` |
| 10-15 | The Dawn Redwood by the Kelvin Statue | Belfast | `photo_apply.py hold bfs_003` |
| 10-15 | The Queen's Park Champion Wych Elm | Brighton | `photo_apply.py hold bhm_005` |
| 10-14 | The Plane Tree of St Anne's | Brno | `photo_apply.py hold brq_005` |
| 10-14 | The Great Chestnut of Časta | Časta | `photo_apply.py hold cst_001` |
| 10-14 | The Albert Edward Oak | Christchurch | `photo_apply.py hold chc_002` |
| 10-14 | The Plane Tree of Piazza Camerlata | Como | `photo_apply.py hold com_008` |
| 10-14 | Square Kauri | Coromandel Forest Park | `photo_apply.py hold sqk_001` |
| 10-14 | The Ohatsuki Ginkgo of Yagisawa | Fujikawaguchiko | `photo_apply.py hold fjk_003` |
| 10-14 | The Plane of the University Garden | Geneva | `photo_apply.py hold gen_015` |
| 10-14 | The Annaplatz Oak | Graz | `photo_apply.py hold grz_012` |
| 10-14 | Gernikako Arbola, the Tree of Gernika | Guernica | `photo_apply.py hold grk_001` |
| 10-15 | 1000jährige Eibe Gutau | Gutau | `photo_apply.py hold gut_001` |
| 10-15 | The Obertraun Dorfeibe | Hallstatt | `photo_apply.py hold hst_002` |
| 10-15 | The Bad Goisern Parish Church Yew | Hallstatt | `photo_apply.py hold hst_004` |
| 10-14 | Clawé Fawe (the nail tree of Foyr) | Jalhay | `photo_apply.py hold gos_002` |
| 10-14 | Gastilonys Oak | Kaunas | `photo_apply.py hold kun_010` |
| 10-15 | Robert E. Lee Tree | Kings Canyon National Park | `photo_apply.py hold kcy_002` |
| 10-14 | Kozaki no Okusu | Kozaki | `photo_apply.py hold kzk_001` |
| 10-14 | The Kozy Plane Tree (Platan Klonolistny) | Kozy | `photo_apply.py hold koz_001` |
| 10-14 | The Beliny-Prazmowskiego Dawn Redwood | Krakow | `photo_apply.py hold kra_035` |
| 10-14 | Carrasca Milenaria de Lecina | Lecina | `photo_apply.py hold lec_001` |
| 10-15 | The Alzina d'en Pere | Mallorca | `photo_apply.py hold mlc_005` |
| 10-14 | The Tanzlinde of Hilgershausen | Malsfeld | `photo_apply.py hold mls_003` |
| 10-14 | The Junipers of Kochozenji | Minami-Alps | `photo_apply.py hold mna_001` |
| 10-15 | The Moon Tree of Friendly Plaza | Monterey | `photo_apply.py hold mty_003` |
| 10-14 | The Podocarpus of Piazza Cavour | Naples | `photo_apply.py hold nap_019` |
| 10-14 | Moko | Otari-Wilton's Bush | `photo_apply.py hold mko_001` |
| 10-14 | McKinney Kauri | Parry Kauri Park | `photo_apply.py hold pky_001` |
| 10-14 | Simpson Kauri | Parry Kauri Park | `photo_apply.py hold pky_002` |
| 10-14 | The Thousand-Year Oak of Sacrow | Potsdam | `photo_apply.py hold pot_005` |
| 10-14 | The Columnar Oaks of Bassinplatz | Potsdam | `photo_apply.py hold pot_006` |
| 10-14 | The Oak of the Schiffbauergasse | Potsdam | `photo_apply.py hold pot_008` |
| 10-14 | The Sessile Oak of Paetowstrasse | Potsdam | `photo_apply.py hold pot_010` |
| 10-15 | The Ankerwycke Yew | Runnymede | `photo_apply.py hold ank_001` |
| 10-14 | The Meadow Oak of Buchholzhofstraße | Salzburg | `photo_apply.py hold szb_012` |
| 10-15 | The Katsura Fudo of Koganeyu | Sapporo | `photo_apply.py hold spr_002` |
| 10-14 | Valkasken | Stockholm | `photo_apply.py hold sto_005` |
| 10-14 | The Visbarai Pine | Stokaičiai | `photo_apply.py hold stk_001` |
| 10-14 | The Hutteneiche | Stuttgart | `photo_apply.py hold stu_002` |
| 10-14 | The Hohenheim Love Plane | Stuttgart | `photo_apply.py hold stu_007` |
| 10-14 | The Planes of the Grote Kerk | The Hague | `photo_apply.py hold hag_020` |
| 10-14 | Kozoji no Kotsubugaya | Toba | `photo_apply.py hold tob_001` |
| 10-14 | Wakidani no Tochinoki | Toga | `photo_apply.py hold tga_001` |
| 10-14 | The Elm of Piazza Dante | Trento | `photo_apply.py hold tre_004` |
| 10-14 | Trolleken (the Troll Oak of Trollskogen) | Trollskogen | `photo_apply.py hold trs_001` |
| 10-14 | The Plane of the Fontana dei Dodici Mesi | Turin | `photo_apply.py hold tor_008` |
| 10-14 | The Grandfather Plane of Parco della Tesoriera | Turin | `photo_apply.py hold tor_009` |
| 10-14 | The Caucasian Elm of the Giardini Reali | Turin | `photo_apply.py hold tor_010` |
| 10-14 | Kalm's Oak | Turku | `photo_apply.py hold tku_001` |
| 10-14 | Ushio no Katsura | Unnan | `photo_apply.py hold unn_001` |
| 10-14 | Vainiai Poplar | Vainiai | `photo_apply.py hold vni_001` |
| 10-14 | Nevėžio Dvilypis Oak | Vainiai | `photo_apply.py hold vni_003` |
| 10-14 | The Vytogala Independence Oaks | Vytogala | `photo_apply.py hold vyt_001` |
| 10-14 | Dąb Józef | Wiśniowa | `photo_apply.py hold wis_001` |
| 10-14 | The Witness Plane (Swiadek) | Wroclaw | `photo_apply.py hold wro_005` |
| 10-14 | Yashiro-no-Okeyaki | Yabu | `photo_apply.py hold yab_003` |
| 10-14 | Kuchioya no O-Abemaki | Yabu | `photo_apply.py hold yab_004` |
| 10-14 | Okkazuma no Shidarezakura (the Weeping Cherry of Okkazuma) | Yamanashi City | `photo_apply.py hold ynh_001` |
| 10-14 | Nomanji no Sotetsu | Yoshida | `photo_apply.py hold yos_001` |
| 10-14 | The Plane Tree of Budatín Park | Žilina | `photo_apply.py hold zil_001` |
| 10-14 | The Maple of Sokolovská Street | Žilina | `photo_apply.py hold zil_003` |
| 10-14 | The Waldhaustanne (Zwieslerwaldhaus Silver Fir) | Zwieslerwaldhaus | `photo_apply.py hold zwi_001` |
| 10-14 | Dąb Franciszek (the Franciszek Oak) | Żywiec | `photo_apply.py hold zyw_001` |

Machine: 8 chain attempts yesterday, 8 got real work time (~114 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

## 2026-10-14 (previous UTC day)

**Today: an account was opened yesterday (28 total).**

**Conclusion: the numbers that matter now** (this week against the week before)

| Number | Why it counts | This week | Week before |
|---|---|---:|---:|
| Stood at a tree (app collections) | goal 1, the north star | 4 | 11 |
| New phones that opened a tree on day one | activation | 10 of 16 (62%) | 5 of 6 (83%) |
| New phones that tapped Take me there on day one | activation | 1 of 16 (6%) | 1 of 6 (17%) |
| Phones back within a week | retention | 4 of 6 (67%) | 8 of 15 (53%) |
| New accounts (strangers) | people collected | 5 | 5 |
| Readers' trees and photographs live | data collected | 3 | 14 |
| Arrivals from search, every engine (8 days) | traction | 100 | - |

4 collections at a tree this week against 11 the week before, a handful: read it as a count, not a trend. The weakest link is tapping Take me there on day one (1 of 16): that step is the work, more traffic only pours more people into it.

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**What readers gave us, and it went live**

| Day | Tree | Where | What | Page |
|---|---|---|---|---|
| 10-13 | The Great Lawn Plane of Parc Montsouris | Paris | a reader's photograph, published | [live](https://ancienttrees.app/paris/great-lawn-plane-of-parc-montsouris) |

**Did the product happen**

| Action | Yesterday | 7 days | Last |
|---|---:|---:|---|
| signin-open | 3 | 31 | yesterday |
| app-cta | 0 | 17 | today |
| signin-oauth | 0 | 1 | 6 days ago |
| signin-done | 0 | 0 | 8 days ago |
| directions | 0 | 1 | 6 days ago |
| search-home | 1 | 5 | yesterday |
| app-open | 0 | 7 | 5 days ago |
| suggestion-submit | 0 | 0 | 20 days ago |
| home-country | 0 | 3 | 3 days ago |
| home-fav | 0 | 2 | 6 days ago |
| signin-link-sent | 0 | 0 | 20 days ago |
| save | 0 | 0 | 13 days ago |
| waitlist-submit | 0 | 1 | 5 days ago |
| home-dir-tree | 0 | 0 | 22 days ago |
| visit | 0 | 0 | 25 days ago |
| app-page-badge | 0 | 1 | 6 days ago |
| home-species | 0 | 0 | 24 days ago |
| search-explore | 0 | 0 | 13 days ago |
| walks-app | 0 | 0 | 22 days ago |
| home-dir-species | 0 | 1 | 4 days ago |
| sponsor-open | 0 | 0 | 25 days ago |
| worthit-report | 0 | 0 | 21 days ago |
| worthit-report detail | 0 | 0 | 21 days ago |
| worthit-worth it | 0 | 0 | 25 days ago |
| worthit-not worth it | 0 | 0 | never |
| **all** | **4** | **70** | |

**Searched yesterday:** zurich.

| Day | Accounts | Android waitlist | Saves | Trees sent | Feedback | Ambassador asks |
|---|---:|---:|---:|---:|---:|---:|
| 10-08 | 1 | 0 | 0 | 0 | 1 | 0 |
| 10-09 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-10 | 1 | 1 | 0 | 0 | 0 | 0 |
| 10-11 | 1 | 0 | 0 | 0 | 0 | 0 |
| 10-12 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-13 | 1 | 0 | 0 | 0 | 2 | 0 |
| 10-14 | 1 | 0 | 0 | 0 | 0 | 0 |
| 10-15 | 0 | 0 | 0 | 0 | 0 | 0 |
| **7 days** | **5** | **1** | **0** | **0** | **3** | **0** |

| Ambassadors | Yesterday | 7 days | Total |
|---|---:|---:|---:|
| Granted | 0 | 1 | 6 |
| Invitations sent (app contributors) | 0 | 2 | 7 |
| Open-seat requests answered | 0 | 0 | 0 |
- New in 7 days: Kerry Pickett (Brighton) since 2026-10-10.
- Android waitlist: 21 total, newest 5 days ago
- Submissions: 35 total (19 trees sent, 16 feedback), newest 2 days ago
- Accounts:    28 total, newest yesterday

**What readers told us** (7 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 10-08 | The Judas Tree of the Real Alcázar | correction sent in | 92 chars, read it in the database | eed7 | open_question |
| 10-13 | sev_009 (The Fig of the Glorieta d | worth it | - | c922 | - |
| 10-13 | - | Location not working on iOS, permi | - | c922 | open_question |

- 3 rows from 2 accounts.

**The funnel, as rates**
- Seen to clicked: 5.6% (11 of 195) vs 3.9% the week before
- Pages per visit: 1.3 (6580 visits, 8340 pageviews since 2026-09-17)
- Visits that did something: 12.4% (819 actions on 6580 visits)

**What people did in the app**

| What | Yesterday | 7 days | Last |
|---|---:|---:|---|
| app_open | 17 | 67 | today |
| tab | 6 | 24 | today |
| tree_opened | 7 | 84 | today |
| directions | 1 | 5 | yesterday |
| tree_saved | 0 | 1 | 2 days ago |
| tree_visited | 0 | 4 | 4 days ago |
| sighting_recorded | 0 | 1 | 4 days ago |
| sync_skipped | 0 | 0 | never |
| sync_failed | 0 | 0 | never |
| location | 1 | 1 | yesterday |
| **all** | **32** | **187** | |
- Measuring since 2026-08-30, when Measure.swift went in. Unlinked to any account by design: an install id, the app version and the OS, nothing else.
- 85 installs have ever sent anything. An install id is made fresh on each install, so this is an upper bound on people, not a count of them.
- Yesterday came from 3 installs, and the busiest made 22 of 3 events (733%). One install making most of a day is what our own reinstall looks like: add its id to excluded_installs in data/app-measure.json if it is ours.
- Tabs opened (7d): Discover 10; My trees 8; Map 6
- Active phones: 3 in the last day, 24 in the last 7 days, 56 in the last 30 days.
- Coming back: 26 of those 56 phones opened the app on more than one day (46%).
- Trees opened by the most phones (7d): The Fig of the Glorieta de Goya (Seville) 2; The Great White Oak of Logan (Logan Oak) (Logan, Ohio) 2; The Ombú of La Cartuja (Seville) 1; The Mulberry of the Alamillo Cortijo (Seville) 1; The Magnolia of the Cathedral (Seville) 1
- Where the phones are (30d): United States 13; United Kingdom 7; Portugal 5; Spain 4; Italy 4; The Netherlands 4
- Trees recorded (7d): a tree we map 1
  A sighting reaches our database only through an account. Signed out it stays on the phone, so this count can run ahead of the trees and photographs we actually receive.

**Trees collected in the app** (7 days, a person standing at the tree)

| Day | Tree | Where | Install | Build | Signed in |
|---|---|---|---|---|---|
| 10-11 | The Lagunària de la Llotja | Palma de Mallorca | A98A | ? | ? |
| 10-08 | The Stone Pine of the Jardines de Cristina | Seville | 92A2 | ? | ? |
| 10-08 | The Stone Pine of the Jardines de Cristina | Seville | 92A2 | ? | ? |
| 10-08 | The Stone Pine of the Jardines de Cristina | Seville | 92A2 | ? | ? |

**The app as a builder reads it** (this week against the week before; the weakest row is the work)

| Link | This week | Week before |
|---|---|---|
| New phones | 16 | 6 |
| First day: opened a tree | 10 of 16 (62%) | 5 of 6 (83%) |
| First day: opened a tree near them | - | - |
| First day: allowed location | - | - |
| First day: Take me there | 1 of 16 (6%) | 1 of 6 (17%) |
| First day: collected a tree | 2 of 16 (12%) | 2 of 6 (33%) |
| Back within a week | 4 of 6 (67%) | 8 of 15 (53%) |
| Trees collected (all phones) | 4 | 11 |
- Near and location count only phones on a version that sends them (from 2026-10-10); a dash means none yet.
- Back within a week looks at the phones that arrived a week earlier, so each has had its seven days.

**App Store downloads** (Apple's own count, not PostHog)

| Day | Downloads |
|---|---:|
| 2026-10-08 | 4 |
| 2026-10-09 | 4 |
| 2026-10-10 | 5 |
| 2026-10-12 | 1 |
| 2026-10-13 | 2 |
| **5 days** | **16** |
- First-time downloads only, which is what App Store Connect's Trends screen counts; redownloads and updates are not in this table.

**Where the downloads came from** (7 days, Apple's attribution)

| Came from | Via | Downloads |
|---|---|---:|
| App Store search | - | 7 |
| Web referrer | - | 5 |
| App referrer | - | 3 |
| App Store browse | - | 1 |
| **window** | | **16** |
- Countries: US (6); GB (4); BE (1); ES (1); IE (1); NL (1)
- Apple's own source split, first-time downloads only. "Web referrer" with our own domain is the site's app page; "App Store search" is somebody who typed into the store. "Unavailable" is Apple's word for a source it could not attribute.

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-05 | 4 | 47 | 8.5% | 39.0 |
| 10-06 | 1 | 45 | 2.2% | 34.5 |
| 10-07 | 0 | 47 | 0.0% | 34.7 |
| 10-08 | 5 | 35 | 14.3% | 21.8 |
| 10-09 | 3 | 37 | 8.1% | 49.5 |
| 10-10 | 0 | 35 | 0.0% | 29.8 |
| 10-11 | 1 | 32 | 3.1% | 31.7 |
| 10-12 | 1 | 26 | 3.8% | 30.3 |
| 10-13 | 1 | 25 | 4.0% | 34.1 |
| 10-14 *partial* | 0 | 5 | 0.0% | 14.8 |
| **window** | **16** | **334** | **4.8%** | |
- Top queries (10d): pokaz na mapie (i1, p1); alte bäume (i3, p27); ancient douglas fir tree (i1, p48); ancient tree (i1, p89); angelystor (i1, p1)
- Top pages (10d): / (c6/i15); /brussels/oldest-tree (c2/i3); /de/berlin/englischer-garten-wingnut (c1/i2); /it/rome/mexican-blue-palm-of-villa-sciarra (c1/i2); /cagliari/ficus-of-piazza-matteotti (c1/i1)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'alte bäume' (i3, p27)
    - 'big sherman tree' (i2, p69)
    - 'pokaz na mapie' (i1, p1)
    - 'angelystor' (i1, p1)
    - 'araucaria norfolk' (i1, p88)
    - 'avenue de laune' (i1, p24)
    - 'bunya tree' (i1, p97)
    - 'chapina garden' (i1, p13)
    - and 1 more
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| 10-06 | 65 | 2 | 3.1% |
| 10-07 | 81 | 2 | 2.5% |
| 10-08 | 168 | 4 | 2.4% |
| 10-09 | 47 | 2 | 4.3% |
| 10-10 | 57 | 1 | 1.8% |
| 10-11 | 53 | 2 | 3.8% |
| 10-12 | 81 | 3 | 3.7% |
| **7 days** | **552** | **16** | **2.9%** |
- Week before: 166 impressions, 11 clicks. No Bing demotion in sight.
- Top Bing queries: trees in the plaza dus burgos seville (c1/i3, p5); french trees found in paris (c1/i2, p6); berlin tree (c1/i2, p1); oldest tree in belfast (c1/i2, p1); remarkable trees copenhagen (c1/i2, p4); oldest live oak trees in new orleans (c1/i2, p6); ancient trees in wiesbaden germany (c1/i2, p6); husalle lindens copenhagen (c1/i2, p3)
- Bing alone, from Bing Webmaster Tools. DuckDuckGo and Yahoo draw on the same index and publish no numbers; their arrivals are columns in the Cloudflare table. Bing's data lags about two days.

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 417 |
| Clicks | 16 |
| Pages that got at least one impression | 221 |
| Impressions on the proven cities | 322 |

- 213 impressions from site: and operator searches left out (ours, not readers; every Google table below is without them).

What we did (context, proves nothing by itself): 2947 trees Google may index, 751 kept out for lacking a photo and an exact pin, 2802 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 1714 | 42 | 129 | 0.08 | 3 |
| Not yet rich | 490 | 26 | 37 | 0.08 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| prague | 0 | 87 | 0.0% | 5.6 | 5.9% | - |
| sequoia-national-park | 0 | 26 | 0.0% | 73.9 | 0.4% | general sherman tree california (i5, p74) |
| brussels | 2 | 10 | 20.0% | 12.9 | 1.6% | klint white mulberry (i2, p52) |

- Plus 256 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| before 2026-09-23 | The Twisted Muku of Omiya Gate, Kyoto  | Kyoto | - | publish | - |
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
| 2026-10-05 | London Plane in Paris | Paris | 88% girth | publish | publish (2026-10-13, session: 'follow your suggestion') |
| 2026-10-04 | Ginkgo in Tokyo | - | - | lead | - |

0 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.
- Seen, not clicked: /sequoia-national-park/general-sherman-tree (c0/i25, 0.0%) for general sherman tree california (i5, p74); sequoia national park general sherman (i3, p64); sequoia tree general sherman (i2, p71)

**Who they are**
Audience, 28 days of search (589 clicks, 24263 impressions):
- Countries: usa c81/i5499; esp c55/i2004; nld c51/i1250; gbr c49/i1879; deu c47/i1362
- Devices: MOBILE c428/i14832; DESKTOP c155/i9135; TABLET c6/i296
- Landing pages: / c23/i227; /prague c8/i190; /bath/plane-trees-of-the-circus c7/i123; /leuven c7/i47; /malaga c6/i146

Web Analytics (beacon, cookieless), people only.
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews | From Google | From Bing | From DuckDuckGo | From Yahoo | From Ecosia |
|---|---:|---:|---:|---:|---:|---:|---:|
| 10-07 | 70 | 150 | 0 | 0 | 10 | 20 | 0 |
| 10-08 | 10 | 90 | 0 | 0 | 0 | 10 | 0 |
| 10-09 | 60 | 150 | 0 | 10 | 10 | 10 | 0 |
| 10-10 | 40 | 140 | 10 | 0 | 0 | 0 | 0 |
| 10-11 | 30 | 90 | 0 | 0 | 10 | 0 | 0 |
| 10-12 | 20 | 90 | 0 | 0 | 0 | 10 | 0 |
| 10-13 | 20 | 90 | 0 | 0 | 0 | 0 | 0 |
| 10-14 | 10 | 70 | 0 | 0 | 0 | 0 | 0 |
| **window** | **260** | **870** | **10** | **10** | **30** | **50** | **0** |
- Top paths: /leuven (30); /explore (30); / (30); /contribute (30); /perth (20); /logan-ohio (20); /rothenburg-ob-der-tauber/vorbachtal-spruces (20); /de/cologne/moltke-lime-of-the-kahnweiher (20); /palma-de-mallorca/solivera-de-cort (10); /cambridge/newtons-apple-tree (10); /portalegre/plane-tree-of-rossio (10); /es/palma-de-mallorca/ficus-de-la-misericordia (10)
- Referrers: (direct) (150); ancienttrees.app (610); duckduckgo.com (30); search.yahoo.com (30); bing.com (10); www.google.com (10); de.search.yahoo.com (10); localhost (10); uk.search.yahoo.com (10)
- Moved between our own pages: 610 of 870 pageviews (70%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: US (190); DE (140); NL (90); FR (80); PT (70)
- Devices: mobile (530); desktop (340)
- Page load (8d): p50 1866ms, p90 6806ms

Links: external referrers (a link somebody actually clicked): localhost (10)
AI: arrivals from an assistant that cited us: none yet


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-14T14:50 | 86.1 | 0 | 21 | 1 | Aachen, Aga, Albersdorf, Amt Neuhaus, +93 more |
| 10-14T19:17 | 87.5 | 1 | 21 | 11 | Roosendaal +2, Como, Gliniak, Granit, +61 more |
| 10-14T20:46 | 40.0 | -1 | 24 | 0 | Alicante, Como, Coromandel Forest Park, Fujikawaguchiko, +52 more |
| 10-14T22:25 | 63.4 | 19 | 11 | 3 | Chicago +5, Oss +5, Roosendaal +3, Seattle +3, +3 more |
| 10-14T23:30 | 9.5 | 10 | 14 | 0 | Chicago +5, Seattle +3, London +2, Potsdam, +1 more |
| 10-15T02:48 | 59.8 | 3 | 15 | 2 | Roosendaal +3, Ancient Bristlecone Pine Forest, Belfast, Brighton, +10 more |
| 10-15T05:15 | 3.6 | 0 | 5 | 0 | - |
| **7 runs** | **350** | **32** | **111** | | |

- 2 of 7 produced no trees; 1 to 11 commands refused per run; last build that went live: 0h ago.

**What they made**

- Record when each page last changed
- Roosendaal: roo_019 to roo_021 register trees, copy recounted to 16, LOG
- LOG and cost: fourth photo pass, queue drained
- Photo viewing pass 4: 16 candidates judged, 0 approved, 1 held (rot_015), 15 rejected
- LOG and cost: third photo pass, 5 approved
- Photo viewing pass 3: 52 candidates judged, 5 approved (bfs_003, gut_001, kcy_002, mty_003, ank_001), 2 held (ind_001, mau_001)
- LOG and cost: second photo pass, 4 approved
- Photo viewing pass 2: 48 candidates judged, 4 approved (abp_001, bhm_005, hst_002, hst_004), 2 held
- LOG and cost: photo viewing pass, 2 approved
- Photo viewing pass: 52 candidates judged, 2 approved (spr_002, mlc_005)
- Graz verify: nothing rich, leads filed, claim released; LOG
- Photographs readers sent, queued for a look; vouched ones live
- Record when each page last changed
- Miami verify: Key West leads filed, claim released; LOG

**Photographs the night run approved** (68; the last column undoes one)

| Day | Tree | Where | Overrule |
|---|---|---|---|
| 10-15 | The Patriarch Tree | Ancient Bristlecone Pine Forest | `photo_apply.py hold abp_001` |
| 10-15 | The Dawn Redwood by the Kelvin Statue | Belfast | `photo_apply.py hold bfs_003` |
| 10-15 | The Queen's Park Champion Wych Elm | Brighton | `photo_apply.py hold bhm_005` |
| 10-14 | The Plane Tree of St Anne's | Brno | `photo_apply.py hold brq_005` |
| 10-14 | The Great Chestnut of Časta | Časta | `photo_apply.py hold cst_001` |
| 10-14 | The Albert Edward Oak | Christchurch | `photo_apply.py hold chc_002` |
| 10-14 | The Plane Tree of Piazza Camerlata | Como | `photo_apply.py hold com_008` |
| 10-14 | Square Kauri | Coromandel Forest Park | `photo_apply.py hold sqk_001` |
| 10-14 | The Ohatsuki Ginkgo of Yagisawa | Fujikawaguchiko | `photo_apply.py hold fjk_003` |
| 10-14 | The Plane of the University Garden | Geneva | `photo_apply.py hold gen_015` |
| 10-13 | Dorpslinde van Massemen | Ghent | `photo_apply.py hold gnt_007` |
| 10-14 | The Annaplatz Oak | Graz | `photo_apply.py hold grz_012` |
| 10-14 | Gernikako Arbola, the Tree of Gernika | Guernica | `photo_apply.py hold grk_001` |
| 10-15 | 1000jährige Eibe Gutau | Gutau | `photo_apply.py hold gut_001` |
| 10-15 | The Obertraun Dorfeibe | Hallstatt | `photo_apply.py hold hst_002` |
| 10-15 | The Bad Goisern Parish Church Yew | Hallstatt | `photo_apply.py hold hst_004` |
| 10-14 | Clawé Fawe (the nail tree of Foyr) | Jalhay | `photo_apply.py hold gos_002` |
| 10-13 | The Chinquapins of Dogata | Kanazawa | `photo_apply.py hold kan_001` |
| 10-14 | Gastilonys Oak | Kaunas | `photo_apply.py hold kun_010` |
| 10-15 | Robert E. Lee Tree | Kings Canyon National Park | `photo_apply.py hold kcy_002` |
| 10-14 | Kozaki no Okusu | Kozaki | `photo_apply.py hold kzk_001` |
| 10-14 | The Kozy Plane Tree (Platan Klonolistny) | Kozy | `photo_apply.py hold koz_001` |
| 10-14 | The Beliny-Prazmowskiego Dawn Redwood | Krakow | `photo_apply.py hold kra_035` |
| 10-14 | Carrasca Milenaria de Lecina | Lecina | `photo_apply.py hold lec_001` |
| 10-15 | The Alzina d'en Pere | Mallorca | `photo_apply.py hold mlc_005` |
| 10-14 | The Tanzlinde of Hilgershausen | Malsfeld | `photo_apply.py hold mls_003` |
| 10-14 | The Junipers of Kochozenji | Minami-Alps | `photo_apply.py hold mna_001` |
| 10-15 | The Moon Tree of Friendly Plaza | Monterey | `photo_apply.py hold mty_003` |
| 10-14 | The Podocarpus of Piazza Cavour | Naples | `photo_apply.py hold nap_019` |
| 10-14 | Moko | Otari-Wilton's Bush | `photo_apply.py hold mko_001` |
| 10-14 | McKinney Kauri | Parry Kauri Park | `photo_apply.py hold pky_001` |
| 10-14 | Simpson Kauri | Parry Kauri Park | `photo_apply.py hold pky_002` |
| 10-14 | The Thousand-Year Oak of Sacrow | Potsdam | `photo_apply.py hold pot_005` |
| 10-14 | The Columnar Oaks of Bassinplatz | Potsdam | `photo_apply.py hold pot_006` |
| 10-14 | The Oak of the Schiffbauergasse | Potsdam | `photo_apply.py hold pot_008` |
| 10-14 | The Sessile Oak of Paetowstrasse | Potsdam | `photo_apply.py hold pot_010` |
| 10-15 | The Ankerwycke Yew | Runnymede | `photo_apply.py hold ank_001` |
| 10-14 | The Meadow Oak of Buchholzhofstraße | Salzburg | `photo_apply.py hold szb_012` |
| 10-15 | The Katsura Fudo of Koganeyu | Sapporo | `photo_apply.py hold spr_002` |
| 10-14 | Valkasken | Stockholm | `photo_apply.py hold sto_005` |
| 10-14 | The Visbarai Pine | Stokaičiai | `photo_apply.py hold stk_001` |
| 10-14 | The Hutteneiche | Stuttgart | `photo_apply.py hold stu_002` |
| 10-14 | The Hohenheim Love Plane | Stuttgart | `photo_apply.py hold stu_007` |
| 10-14 | The Planes of the Grote Kerk | The Hague | `photo_apply.py hold hag_020` |
| 10-14 | Kozoji no Kotsubugaya | Toba | `photo_apply.py hold tob_001` |
| 10-14 | Wakidani no Tochinoki | Toga | `photo_apply.py hold tga_001` |
| 10-14 | The Elm of Piazza Dante | Trento | `photo_apply.py hold tre_004` |
| 10-14 | Trolleken (the Troll Oak of Trollskogen) | Trollskogen | `photo_apply.py hold trs_001` |
| 10-14 | The Plane of the Fontana dei Dodici Mesi | Turin | `photo_apply.py hold tor_008` |
| 10-14 | The Grandfather Plane of Parco della Tesoriera | Turin | `photo_apply.py hold tor_009` |
| 10-14 | The Caucasian Elm of the Giardini Reali | Turin | `photo_apply.py hold tor_010` |
| 10-14 | Kalm's Oak | Turku | `photo_apply.py hold tku_001` |
| 10-14 | Ushio no Katsura | Unnan | `photo_apply.py hold unn_001` |
| 10-14 | Vainiai Poplar | Vainiai | `photo_apply.py hold vni_001` |
| 10-14 | Nevėžio Dvilypis Oak | Vainiai | `photo_apply.py hold vni_003` |
| 10-13 | The Antakalnis Swiss Pine | Vilnius | `photo_apply.py hold vln_014` |
| 10-14 | The Vytogala Independence Oaks | Vytogala | `photo_apply.py hold vyt_001` |
| 10-14 | Dąb Józef | Wiśniowa | `photo_apply.py hold wis_001` |
| 10-14 | The Witness Plane (Swiadek) | Wroclaw | `photo_apply.py hold wro_005` |
| 10-14 | Yashiro-no-Okeyaki | Yabu | `photo_apply.py hold yab_003` |
| 10-14 | Kuchioya no O-Abemaki | Yabu | `photo_apply.py hold yab_004` |
| 10-14 | Okkazuma no Shidarezakura (the Weeping Cherry of Okkazuma) | Yamanashi City | `photo_apply.py hold ynh_001` |
| 10-14 | Nomanji no Sotetsu | Yoshida | `photo_apply.py hold yos_001` |
| 10-14 | The Plane Tree of Budatín Park | Žilina | `photo_apply.py hold zil_001` |
| 10-14 | The Maple of Sokolovská Street | Žilina | `photo_apply.py hold zil_003` |
| 10-13 | The Linden of Linn | Zurich | `photo_apply.py hold boz_001` |
| 10-14 | The Waldhaustanne (Zwieslerwaldhaus Silver Fir) | Zwieslerwaldhaus | `photo_apply.py hold zwi_001` |
| 10-14 | Dąb Franciszek (the Franciszek Oak) | Żywiec | `photo_apply.py hold zyw_001` |

Machine: 8 chain attempts yesterday, 8 got real work time (~487 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

## 2026-10-13 (previous UTC day)

**Today: 2 feedback reports arrived yesterday (35 total); an account was opened yesterday (27 total).**

**Trees readers sent, for you to inspect:** none waiting. Every tree a stranger sent has your answer.

**What readers gave us, and it went live**

| Day | Tree | Where | What | Page |
|---|---|---|---|---|
| 10-13 | The Great Lawn Plane of Parc Montsouris | Paris | a reader's photograph, published | [live](https://ancienttrees.app/paris/great-lawn-plane-of-parc-montsouris) |
| 10-12 | The Fig of La Llotja | Palma de Mallorca | a reader's photograph, published | [live](https://ancienttrees.app/palma-de-mallorca/fig-of-la-llotja) |

**Did the product happen**

| Action | Yesterday | 7 days | Ever | Last |
|---|---:|---:|---:|---|
| signin-open | 2 | 61 | 501 | yesterday |
| app-cta | 2 | 18 | 61 | yesterday |
| signin-oauth | 0 | 4 | 41 | 5 days ago |
| signin-done | 0 | 1 | 39 | 7 days ago |
| directions | 0 | 1 | 37 | 5 days ago |
| search-home | 0 | 4 | 31 | 2 days ago |
| app-open | 0 | 8 | 19 | 4 days ago |
| suggestion-submit | 0 | 0 | 17 | 19 days ago |
| home-country | 0 | 3 | 10 | 2 days ago |
| home-fav | 0 | 3 | 8 | 5 days ago |
| signin-link-sent | 0 | 0 | 6 | 19 days ago |
| save | 0 | 0 | 5 | 12 days ago |
| waitlist-submit | 0 | 1 | 5 | 4 days ago |
| home-dir-tree | 0 | 0 | 3 | 21 days ago |
| search-explore | 0 | 0 | 3 | 12 days ago |
| visit | 0 | 0 | 3 | 24 days ago |
| app-page-badge | 0 | 1 | 2 | 5 days ago |
| home-species | 0 | 0 | 2 | 23 days ago |
| walks-app | 0 | 0 | 2 | 21 days ago |
| home-dir-species | 0 | 1 | 1 | 3 days ago |
| sponsor-open | 0 | 0 | 1 | 24 days ago |
| worthit-report | 0 | 0 | 1 | 20 days ago |
| worthit-report detail | 0 | 0 | 1 | 20 days ago |
| worthit-worth it | 0 | 0 | 1 | 24 days ago |
| worthit-not worth it | 0 | 0 | 0 | never |
| **all** | **4** | **106** | **800** | |
- 'Ever' counts every row in the events table, which begins 2026-08-01 when the funnel was repaired. Anything named here with a zero has never fired at all.

**Searched yesterday:** nothing.

| Day | Accounts | Android waitlist | Saves | Trees sent | Feedback | Ambassador asks |
|---|---:|---:|---:|---:|---:|---:|
| 10-07 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-08 | 1 | 0 | 0 | 0 | 1 | 0 |
| 10-09 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-10 | 1 | 1 | 0 | 0 | 0 | 0 |
| 10-11 | 1 | 0 | 0 | 0 | 0 | 0 |
| 10-12 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-13 | 1 | 0 | 0 | 0 | 2 | 0 |
| 10-14 | 0 | 0 | 0 | 0 | 0 | 0 |
| **7 days** | **4** | **1** | **0** | **0** | **3** | **0** |

| Ambassadors | Yesterday | 7 days | Total |
|---|---:|---:|---:|
| Granted | 0 | 1 | 6 |
| Invitations sent (app contributors) | 0 | 2 | 7 |
| Open-seat requests answered | 0 | 0 | 0 |
- New in 7 days: Kerry Pickett (Brighton) since 2026-10-10.
- Android waitlist: 21 total, newest 4 days ago
- Submissions: 35 total (19 trees sent, 16 feedback), newest yesterday
- Accounts:    27 total, newest yesterday

**What readers told us** (7 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 10-08 | The Judas Tree of the Real Alcázar | correction sent in | 92 chars, read it in the database | eed7 | open_question |
| 10-13 | sev_009 (The Fig of the Glorieta d | worth it | - | c922 | - |
| 10-13 | - | Location not working on iOS, permi | - | c922 | open_question |

- 3 rows from 2 accounts.

**The funnel, as rates**
- Seen to clicked: 5.3% (11 of 209) vs 3.0% the week before
- Pages per visit: 1.3 (6540 visits, 8260 pageviews since 2026-09-16)
- Visits that did something: 12.5% (816 actions on 6540 visits)

**What people did in the app**

| What | Yesterday | 7 days | Ever | Last |
|---|---:|---:|---:|---|
| app_open | 11 | 45 | 306 | yesterday |
| tab | 1 | 19 | 315 | yesterday |
| tree_opened | 15 | 74 | 1251 | yesterday |
| directions | 0 | 4 | 45 | 5 days ago |
| tree_saved | 1 | 1 | 20 | yesterday |
| tree_visited | 0 | 4 | 27 | 3 days ago |
| sighting_recorded | 0 | 1 | 73 | 3 days ago |
| sync_skipped | 0 | 0 | 0 | never |
| sync_failed | 0 | 0 | 0 | never |
| **all** | **28** | **148** | **2037** | |
- Measuring since 2026-08-30, when Measure.swift went in. Unlinked to any account by design: an install id, the app version and the OS, nothing else.
- 83 installs have ever sent anything. An install id is made fresh on each install, so this is an upper bound on people, not a count of them.
- Yesterday came from 2 installs, and the busiest made 27 of 2 events (1350%). One install making most of a day is what our own reinstall looks like: add its id to excluded_installs in data/app-measure.json if it is ours.
- Tabs opened (7d): Discover 11; My trees 5; Map 3
- Active phones: 2 in the last day, 24 in the last 7 days, 57 in the last 30 days.
- Coming back: 24 of those 57 phones opened the app on more than one day (42%).
- Trees opened by the most phones (7d): The Great White Oak of Logan (Logan Oak) (Logan, Ohio) 2; The Arenbergpark Plane (Leuven) 2; The Magnolia of the Cathedral (Seville) 1; The Fig of the Glorieta de Goya (Seville) 1; The Totteridge Yew (London) 1
- Where the phones are (30d): United States 13; United Kingdom 7; Portugal 5; Italy 4; The Netherlands 4; Spain 3
- Trees recorded (7d): a tree we map 1
  A sighting reaches our database only through an account. Signed out it stays on the phone, so this count can run ahead of the trees and photographs we actually receive.

**Trees collected in the app** (7 days, a person standing at the tree)

| Day | Tree | Where | Install | Build | Signed in |
|---|---|---|---|---|---|
| 10-11 | The Lagunària de la Llotja | Palma de Mallorca | A98A | ? | ? |
| 10-08 | The Stone Pine of the Jardines de Cristina | Seville | 92A2 | ? | ? |
| 10-08 | The Stone Pine of the Jardines de Cristina | Seville | 92A2 | ? | ? |
| 10-08 | The Stone Pine of the Jardines de Cristina | Seville | 92A2 | ? | ? |

**The app as a builder reads it** (this week against the week before; the weakest row is the work)

| Link | This week | Week before |
|---|---|---|
| New phones | 16 | 6 |
| First day: opened a tree | 10 of 16 (62%) | 5 of 6 (83%) |
| First day: opened a tree near them | - | - |
| First day: allowed location | - | - |
| First day: Take me there | 1 of 16 (6%) | 1 of 6 (17%) |
| First day: collected a tree | 2 of 16 (12%) | 2 of 6 (33%) |
| Back within a week | 4 of 6 (67%) | 8 of 15 (53%) |
| Trees collected (all phones) | 4 | 11 |
- Near and location count only phones on a version that sends them (from 2026-10-10); a dash means none yet.
- Back within a week looks at the phones that arrived a week earlier, so each has had its seven days.

**App Store downloads** (Apple's own count, not PostHog)

| Day | Downloads |
|---|---:|
| 2026-10-05 | 1 |
| 2026-10-08 | 4 |
| 2026-10-09 | 4 |
| 2026-10-10 | 5 |
| 2026-10-12 | 1 |
| **5 days** | **15** |
- First-time downloads only, which is what App Store Connect's Trends screen counts; redownloads and updates are not in this table.

**Where the downloads came from** (7 days, Apple's attribution)

| Came from | Via | Downloads |
|---|---|---:|
| App Store search | - | 8 |
| Web referrer | - | 5 |
| App referrer | - | 2 |
| **window** | | **15** |
- Countries: US (6); GB (5); BE (1); ES (1); IE (1); SK (1)
- Apple's own source split, first-time downloads only. "Web referrer" with our own domain is the site's app page; "App Store search" is somebody who typed into the store. "Unavailable" is Apple's word for a source it could not attribute.

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-04 | 1 | 50 | 2.0% | 28.8 |
| 10-05 | 4 | 47 | 8.5% | 39.0 |
| 10-06 | 1 | 45 | 2.2% | 34.5 |
| 10-07 | 0 | 47 | 0.0% | 34.7 |
| 10-08 | 5 | 35 | 14.3% | 21.8 |
| 10-09 | 3 | 37 | 8.1% | 49.5 |
| 10-10 | 0 | 35 | 0.0% | 29.8 |
| 10-11 | 1 | 32 | 3.1% | 31.7 |
| 10-12 | 1 | 20 | 5.0% | 25.9 |
| 10-13 *partial* | 1 | 3 | 33.3% | 8.3 |
| **window** | **17** | **351** | **4.8%** | |
- Top queries (10d): pokaz na mapie (i1, p1); alte bäume (i3, p27); ancient douglas fir tree (i1, p48); ancient tree (i1, p65); angelystor (i1, p1)
- Top pages (10d): / (c6/i14); /brussels/oldest-tree (c3/i4); /cagliari/ficus-of-piazza-matteotti (c1/i1); /de/berlin/englischer-garten-wingnut (c1/i2); /es/seville/cypress-of-san-fernando-cemetery (c1/i1)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'alte bäume' (i3, p27)
    - 'big sherman tree' (i2, p69)
    - 'pokaz na mapie' (i1, p1)
    - 'angelystor' (i1, p1)
    - 'araucaria norfolk' (i1, p88)
    - 'arbol de las pagodas' (i1, p33)
    - 'avenue de laune' (i1, p24)
    - 'bunya tree' (i1, p97)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR | Pages crawled | Pages in index |
|---|---:|---:|---:|---:|---:|
| 10-05 | 79 | 5 | 6.3% | 207 | 2106 |
| 10-06 | 65 | 2 | 3.1% | 192 | 2157 |
| 10-07 | 81 | 2 | 2.5% | 78 | 2244 |
| 10-08 | 168 | 4 | 2.4% | 164 | 2293 |
| 10-09 | 47 | 2 | 4.3% | - | - |
| 10-10 | 57 | 1 | 1.8% | - | - |
| 10-11 | 53 | 2 | 3.8% | - | - |
| **7 days** | **550** | **18** | **3.3%** | **641** | **2293** |
- Week before: 87 impressions, 6 clicks; in index then: 2106. No Bing demotion in sight.
- Top Bing queries: trees in the plaza dus burgos seville (c1/i3, p5); berlin tree (c1/i2, p1); oldest tree in belfast (c1/i2, p1); oldest live oak trees in new orleans (c1/i2, p6); remarkable trees copenhagen (c1/i2, p4); husalle lindens copenhagen (c1/i2, p3); ancient trees in wiesbaden germany (c1/i2, p6); french trees found in paris (c1/i2, p6)
- Bing alone, from Bing Webmaster Tools; the in-index column is the last day's count. DuckDuckGo and Yahoo draw on the same index and are not in these numbers. Bing's data lags about two days.

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 643 |
| Clicks | 17 |
| Pages that got at least one impression | 230 |
| Impressions on the proven cities | 550 |

What we did (context, proves nothing by itself): 2916 trees Google may index, 757 kept out for lacking a photo and an exact pin, 2851 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 1622 | 40 | 264 | 0.16 | 3 |
| Not yet rich | 511 | 24 | 42 | 0.08 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| prague | 0 | 294 | 0.0% | 5.6 | 5.7% | prague (i17, p1) |
| sequoia-national-park | 0 | 24 | 0.0% | 73.4 | 0.4% | general sherman tree california (i5, p74) |
| brussels | 3 | 12 | 25.0% | 10.9 | 2.2% | klint white mulberry (i2, p52) |

- Plus 256 cities on the frozen 09-27 roster (data/depth-roster-frozen.json), biggest: singapore, lisbon, amsterdam, barcelona, seville, bath, tenerife, berlin.

**Copy test**

```
Copy test: city-title-age-first (day 34 of 56, review 2026-11-05)
The age is the hook and the count is inventory, so naming the oldest tree before the number earns more clicks.

  control      n1    before 1.38  now 0.00  change -1.38

  TOO EARLY. At about 2 clicks per page per ten days this needs the full window; a lead now is noise wearing a result's clothes.
```

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| before 2026-09-23 | The Twisted Muku of Omiya Gate, Kyoto  | Kyoto | - | publish | - |
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
| 2026-10-05 | London Plane in Paris | Paris | 88% girth | publish | publish (2026-10-13, session: 'follow your suggestion') |
| 2026-10-04 | Ginkgo in Tokyo | - | - | lead | - |

0 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**The language test** (Contract J v1.13: a translated set should pass its English twin's impressions within four weeks of indexing):

| Lang | City | Clicks | Impressions | Position | English twin |
|---|---|---:|---:|---:|---:|
| es | barcelona | 0 | 7 | 41.1 | 3 |
| de | vienna | 0 | 6 | 31.2 | 1 |
| es | tenerife | 0 | 6 | 55.7 | 6 |
| de | graz | 0 | 5 | 45.4 | 0 |
| ja | fukuoka | 0 | 5 | 26.8 | 0 |
| es | seville | 1 | 4 | 15.2 | 5 |
| it | rome | 1 | 4 | 32.5 | 1 |
| de | hamburg | 0 | 4 | 24.5 | 0 |
| pt | rio-de-janeiro | 0 | 4 | 9.8 | 0 |
| de | berlin | 1 | 3 | 26.3 | 2 |
| es | madrid | 0 | 3 | 45.0 | 1 |
| nl | amsterdam | 0 | 3 | 51.3 | 0 |
| nl | arnhem | 0 | 3 | 83.3 | 0 |
| de | munich | 0 | 2 | 11.0 | 6 |
| es | cadiz | 0 | 2 | 66.0 | 0 |
| es | palma-de-mallorca | 0 | 2 | 75.5 | 1 |
| fr | lyon | 0 | 2 | 44.0 | 2 |
| de | regensburg | 0 | 1 | 52.0 | 0 |
| es | malaga | 0 | 1 | 25.0 | 0 |
| fr | nantes | 0 | 1 | 27.0 | 0 |
| fr | nice | 0 | 1 | 6.0 | 0 |
| ja | kagoshima | 0 | 1 | 83.0 | 1 |
| ja | kyoto | 0 | 1 | 1.0 | 2 |
| ja | tokyo | 0 | 1 | 5.0 | 2 |
| nl | the-hague | 0 | 1 | 1.0 | 1 |

**Cities seen but never clicked** (60+ impressions, zero clicks, with what they are actually shown for):

- prague (i159): prague (i17, p9); prague (i17, p8); prague (i17, p7); prague (i17, p5)
- Seen, not clicked: /sequoia-national-park/general-sherman-tree (c0/i23, 0.0%) for general sherman tree california (i5, p74); sequoia tree general sherman (i2, p71); sequoia national park general sherman (i2, p61)

**Who they are**
Audience, 28 days of search (631 clicks, 26759 impressions):
- Countries: usa c90/i6493; nld c60/i1421; esp c59/i2169; gbr c51/i2043; deu c48/i1428
- Devices: MOBILE c456/i16034; DESKTOP c167/i10404; TABLET c8/i321
- Landing pages: / c23/i245; /prague c8/i262; /bath/plane-trees-of-the-circus c7/i132; /leuven c7/i48; /malaga c7/i163

Web Analytics (beacon, cookieless), people only.
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews | From Google |
|---|---:|---:|---:|
| 10-06 | 90 | 160 | 0 |
| 10-07 | 70 | 150 | 0 |
| 10-08 | 10 | 90 | 0 |
| 10-09 | 60 | 150 | 0 |
| 10-10 | 40 | 140 | 10 |
| 10-11 | 30 | 90 | 0 |
| 10-12 | 20 | 90 | 0 |
| 10-13 | 20 | 90 | 0 |
| **window** | **340** | **960** | **10** |
- Top paths: / (60); /explore (30); /leuven (30); /perth (20); /melbourne/hoop-pine-of-yarra-boulevard (20); /logan-ohio (20); /rothenburg-ob-der-tauber/vorbachtal-spruces (20); /app (20); /de/cologne/moltke-lime-of-the-kahnweiher (20); /contribute (20); /portalegre/plane-tree-of-rossio (10); /cambridge/newtons-apple-tree (10)
- Referrers: (direct) (180); ancienttrees.app (620); www.facebook.com (50); duckduckgo.com (40); search.yahoo.com (30); bing.com (10); www.google.com (10); de.search.yahoo.com (10); uk.search.yahoo.com (10)
- Moved between our own pages: 620 of 960 pageviews (65%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: US (240); DE (110); NL (80); GB (80); FR (70)
- Devices: mobile (610); desktop (350)
- Page load (8d): p50 1980ms, p90 7260ms

Links: external referrers (a link somebody actually clicked): www.facebook.com (50); search.yahoo.com (30); de.search.yahoo.com (10); uk.search.yahoo.com (10)
AI: arrivals from an assistant that cited us: none yet

Backlinks (watched pages):
| Site | Links to | rel | First seen |
|---|---|---|---|
| getlisbon.com | /lisbon | followed | 2026-09-08 |
| getlisbon.com | /pt/lisbon | followed | 2026-09-08 |
| www.baumkunde.de | /copenhagen | followed | 2026-09-26 |
| www.baumkunde.de | /rogalin/russ-oak | followed | 2026-09-26 |
4 linking page(s), 4 followed. Checked by fetching the page: a link with rel="noreferrer" never appears in the referrer table, so these two lines measure different things and neither replaces the other. Unknown links stay a manual read of Search Console's Links report. This run read 12 of 12 fetched (0 unreachable), out of 27 watched pages.

**Google Analytics** (last 7 days, visitors who accepted cookies)

| Day | People | New | Returning | Visits | Pageviews | Engaged visits |
|---|---:|---:|---:|---:|---:|---:|
| 10-12 | 3 | 3 | 0 | 4 | 7 | 3 |
| 10-13 | 8 | 8 | 0 | 10 | 38 | 6 |
| **window** | | **11** | | **14** | **45** | **9** |
- People per day are not summed: one person on two days is one person, and GA counts them once per day.
- Coming back (28 days): 1 returning against 11 new, 8% of the people GA saw.

| Page | Pageviews | People |
|---|---:|---:|
| / | 5 | 4 |
| /privacy | 5 | 3 |
| /terms | 3 | 1 |
| /de/cologne | 2 | 1 |
| /de/cologne/moltke-lime-of-the-kahnweiher | 2 | 1 |
| /helmond | 2 | 2 |
| /about | 1 | 1 |
| /cologne | 1 | 1 |
| /contribute | 1 | 1 |
| /freiburg | 1 | 1 |

| Came from | Visits | People |
|---|---:|---:|
| (direct) / (none) | 13 | 10 |
| (not set) / (not set) | 1 | 1 |
| ecosia.org / organic | 1 | 1 |
- GA sees only visitors who pressed Accept on the cookie bar; read it as a sample. Cloudflare's table stays the count.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-13T08:50 | 13.3 | 0 | 7 | 0 | - |
| 10-13T15:53 | 68.8 | -1 | 30 | 3 | Antwerp, Belgrade, Bilu, Craigends, +37 more |
| 10-13T17:18 | 85.8 | 0 | 17 | 0 | Amsterdam, Barcelona, Gdansk, Kamakura, +7 more |
| 10-13T21:10 | 18.8 | 0 | 14 | 0 | Alicante, Amersfoort, Arnhem, Boston, +31 more |
| 10-13T22:12 | 72.3 | 0 | 68 | 9 | Auckland, Baarn, Bad Homburg, Baltimore, +24 more |
| 10-14T00:24 | 6.8 | 0 | 6 | 0 | Malsfeld, Munsterland |
| 10-14T03:09 | 93.3 | -1 | 49 | 0 | Aberford, Aizuwakamatsu, Alishan, Ancient Bristlecone Pine Forest, +79 more |
| **7 runs** | **359** | **-2** | **191** | | |

- 5 of 7 produced no trees; 3 to 9 commands refused per run; last build that went live: 0h ago.

**What they made**

- Higashimiyoshi, Hilvarenbeek, Himi, Hochneukirchen, Hronsek, Ichinohe enrich pass; cost and LOG
- Gumeli, Hampton, Heede, Henrykow, Herchies, Higashiagatsuma enrich pass; cost and LOG
- Fish Lake, Flinders Ranges, Frydlant, Garmen, Gifu, Groton enrich pass; cost and LOG
- Daruvar, Dunkeld, Eraul, Erdmannrode, Farnham, Ferrara enrich pass; cost and LOG
- Cinovec, Colindres, Collm, Cooper Creek, Coppenbrugge, Curinga enrich pass; Dig Tree fee corrected; cost and LOG
- Capeni, Ceska Lipa, Chatenay-Malabry, Cheile Cibinului, Chiapa de Corzo, Chirk enrich pass; cost and LOG
- Bioul, Bojnice, Borculo, Bulat-Pestivien, Cabeza del Buey, Cajvana enrich pass; Cajvana pin corrected; cost and LOG
- Aizuwakamatsu, Argoules, Athens, Azeitao, Bad Blumau, Bataszek enrich pass; cost and LOG
- Waremme, Weywertz, Wrexham, Wye Mills, Zehdenick, Aberford enrich pass; Aberford access corrected; cost and LOG
- Rudy, Sankt Vith, Shokawa, Solingen, Uda, Velke Borove enrich pass; cost and LOG
- Neuenrade, Oberndorf, Princeton, Ramsau, Raudone, Rimov enrich pass; cost and LOG
- Lukavice, Macon, Malacky, Maria Aurora, Martinsville, Melykut enrich pass; Lukavice oak species corrected; cost and LOG
- Kozy, Le Guerno, Lebec, Longlou, Lozorno, Luis Correia enrich pass; Lebec and Longlou access corrected; cost and LOG
- Guaiba, Guernica, Haarlemmermeer, Iida, Innimond, Jericoacoara enrich pass; sycamore species fix; cost and LOG

**Photographs the night run approved** (30; the last column undoes one)

| Day | Tree | Where | Overrule |
|---|---|---|---|
| 10-12 | Le Chêne des Ramolleux | Crécy-en-Ponthieu | `photo_apply.py hold crc_001` |
| 10-12 | The Turenne Lime | Fontaine | `photo_apply.py hold fte_001` |
| 10-13 | Dorpslinde van Massemen | Ghent | `photo_apply.py hold gnt_007` |
| 10-12 | Gupčeva lipa | Gornja Stubica | `photo_apply.py hold gst_001` |
| 10-12 | Jonichiji no Icho | Himi | `photo_apply.py hold him_002` |
| 10-12 | Horner Linde | Horn-Lehe | `photo_apply.py hold hrn_001` |
| 10-12 | Nento Hiramatsu | Iheya | `photo_apply.py hold ihy_001` |
| 10-13 | The Chinquapins of Dogata | Kanazawa | `photo_apply.py hold kan_001` |
| 10-12 | The Kneeling Tree (Klekace Drzewo) | Krasnystaw | `photo_apply.py hold krs_001` |
| 10-12 | King Cypress | Nyingchi | `photo_apply.py hold nyi_001` |
| 10-12 | Gaurė Oak | Pagramantis Regional Park | `photo_apply.py hold pgm_005` |
| 10-12 | Mikalojaus Daukša Oak, Betygala | Plauginiai Forest | `photo_apply.py hold pgn_002` |
| 10-12 | The Oak of the Virgin at Rannée | Rannée | `photo_apply.py hold ran_001` |
| 10-12 | Ilguva Oak | Raudonė | `photo_apply.py hold rdn_003` |
| 10-12 | The Oak of Erentrudishof | Salzburg | `photo_apply.py hold szb_002` |
| 10-12 | The Courtyard Oak of Aigner Straße | Salzburg | `photo_apply.py hold szb_011` |
| 10-12 | Aizen Katsura | Ueda | `photo_apply.py hold bsh_001` |
| 10-12 | The Service Tree of Uzovská Panica | Uzovská Panica | `photo_apply.py hold uzp_001` |
| 10-12 | The Pine of Veľké Borové | Veľké Borové | `photo_apply.py hold vbo_001` |
| 10-12 | The Opatovice Pine | Velke Opatovice | `photo_apply.py hold vop_001` |
| 10-12 | Chene de Venon | Venon | `photo_apply.py hold vno_001` |
| 10-13 | The Antakalnis Swiss Pine | Vilnius | `photo_apply.py hold vln_014` |
| 10-12 | The Lodewijkslinde of Vorden | Vorden | `photo_apply.py hold vrd_001` |
| 10-12 | The Tassilolinde | Wessobrunn | `photo_apply.py hold wes_001` |
| 10-12 | The Wodanseiken | Wolfheze | `photo_apply.py hold wlf_001` |
| 10-12 | Tilleul des Lognards | Xhoris | `photo_apply.py hold xho_001` |
| 10-12 | Tarumi-no-Ozakura | Yabu | `photo_apply.py hold yab_001` |
| 10-12 | Pagryniai Oak | Žalgiriai | `photo_apply.py hold zal_002` |
| 10-12 | The Gerichtslinde of Zehdenick | Zehdenick | `photo_apply.py hold zeh_001` |
| 10-13 | The Linden of Linn | Zurich | `photo_apply.py hold boz_001` |

Machine: 8 chain attempts yesterday, 8 got real work time (~316 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 1 clicks and 3 impressions on Google's freshest day (day before: c1/i20). Directional at best; no strategic conclusions from these volumes.

## 2026-10-12 (previous UTC day)

**Today: nothing here needs you.** The blocks below are the standing picture.

**What readers gave us, and what the night run approved, and it went live**

| Day | Tree | Where | What |
|---|---|---|---|
| 10-12 | The Town Hall Plane | Baarn | a reader's photograph, published |
| 10-12 | The Town Hall Plane | Baarn | a reader's photograph, published beside the one it had |
| 10-12 | The Fig of La Llotja | Palma de Mallorca | a reader's photograph, published |
| 10-12 | Mikalojaus Daukša Oak, Betygala | Plauginiai Forest | the night run approved a photograph (overrule: `photo_apply.py hold pgn_002 "https://upload.wikimedia.org/wikipedia/commons/4/4f/2-Betygalos_%C4%85%C5%BEuolas.JPG"`) |
| 10-12 | Le Chêne des Ramolleux | Crécy-en-Ponthieu | the night run approved a photograph (overrule: `photo_apply.py hold crc_001 "https://upload.wikimedia.org/wikipedia/commons/f/f3/Ch%C3%AAne_des_Ramolleux_for%C3%AAt_de_Cr%C3%A9cy.JPG"`) |
| 10-12 | Ilguva Oak | Raudonė | the night run approved a photograph (overrule: `photo_apply.py hold rdn_003 "https://upload.wikimedia.org/wikipedia/commons/d/dc/Ilguva%2C_%C4%85%C5%BEuolas.JPG"`) |
| 10-12 | Jonichiji no Icho | Himi | the night run approved a photograph (overrule: `photo_apply.py hold him_002 "https://upload.wikimedia.org/wikipedia/commons/e/ef/Ginkgo_at_Jyonichiji_temple.JPG"`) |
| 10-12 | The Lodewijkslinde of Vorden | Vorden | the night run approved a photograph (overrule: `photo_apply.py hold vrd_001 "https://upload.wikimedia.org/wikipedia/commons/5/5c/Lodewijkslinde_bij_Kasteel_Vorden.jpg"`) |
| 10-12 | Tilleul des Lognards | Xhoris | the night run approved a photograph (overrule: `photo_apply.py hold xho_001 "https://upload.wikimedia.org/wikipedia/commons/6/63/Xhoris-tilleul_des_Lognards_%281%29.jpg"`) |
| 10-12 | The Oak of the Virgin at Rannée | Rannée | the night run approved a photograph (overrule: `photo_apply.py hold ran_001 "https://upload.wikimedia.org/wikipedia/commons/f/f3/Rann%C3%A9e_%2835%29_Ch%C3%AAne_%C3%A0_la_Vierge.jpg"`) |
| 10-12 | King Cypress | Nyingchi | the night run approved a photograph (overrule: `photo_apply.py hold nyi_001 "https://upload.wikimedia.org/wikipedia/commons/8/86/Cupressus_gigantea_Bajie.jpg"`) |
| 10-12 | Pagryniai Oak | Žalgiriai | the night run approved a photograph (overrule: `photo_apply.py hold zal_002 "https://upload.wikimedia.org/wikipedia/commons/3/3c/Pagryni%C5%B3_%C4%85%C5%BEuolas_1.JPG"`) |
| 10-12 | Aizen Katsura | Ueda | the night run approved a photograph (overrule: `photo_apply.py hold bsh_001 "https://upload.wikimedia.org/wikipedia/commons/d/d6/Aizenkatsura_Tree.jpg"`) |
| 10-12 | Horner Linde | Horn-Lehe | the night run approved a photograph (overrule: `photo_apply.py hold hrn_001 "https://upload.wikimedia.org/wikipedia/commons/4/4a/Horner_Kirche_-_Linde_jh.jpg"`) |
| 10-13 | Dorpslinde van Massemen | Ghent | the night run approved a photograph (overrule: `photo_apply.py hold gnt_007 "https://upload.wikimedia.org/wikipedia/commons/a/a1/2017_The_Village_Lime_Tree_of_Massemen_BE.jpg"`) |
| 10-12 | The Pine of Veľké Borové | Veľké Borové | the night run approved a photograph (overrule: `photo_apply.py hold vbo_001 "https://upload.wikimedia.org/wikipedia/commons/c/c5/Strom_roka_borovica_velke_borove_01.jpg"`) |
| 10-12 | The Kneeling Tree (Klekace Drzewo) | Krasnystaw | the night run approved a photograph (overrule: `photo_apply.py hold krs_001 "https://upload.wikimedia.org/wikipedia/commons/0/0f/2019_Kneeling_tree_PL.jpg"`) |
| 10-12 | The Gerichtslinde of Zehdenick | Zehdenick | the night run approved a photograph (overrule: `photo_apply.py hold zeh_001 "https://upload.wikimedia.org/wikipedia/commons/7/78/Gerichtslinde_Zehdenick.JPG"`) |
| 10-12 | Gaurė Oak | Pagramantis Regional Park | the night run approved a photograph (overrule: `photo_apply.py hold pgm_005 "https://upload.wikimedia.org/wikipedia/commons/2/25/Gaur%C4%97s_%C4%85%C5%BEuolas_2021.JPG"`) |
| 10-12 | The Service Tree of Uzovská Panica | Uzovská Panica | the night run approved a photograph (overrule: `photo_apply.py hold uzp_001 "https://upload.wikimedia.org/wikipedia/commons/5/57/2020_Sorb_Tree_near_Uzovsk%C3%A1_Panica_SK.jpg"`) |
| 10-12 | The Turenne Lime | Fontaine | the night run approved a photograph (overrule: `photo_apply.py hold fte_001 "https://upload.wikimedia.org/wikipedia/commons/5/56/Tilleul_Turenne_%C3%A0_Fontaine_2008_1.jpg"`) |
| 10-12 | Tarumi-no-Ozakura | Yabu | the night run approved a photograph (overrule: `photo_apply.py hold yab_001 "https://upload.wikimedia.org/wikipedia/commons/b/bb/A_big_cherry_tree_at_Tarumi_village_-_panoramio.jpg"`) |
| 10-12 | Nento Hiramatsu | Iheya | the night run approved a photograph (overrule: `photo_apply.py hold ihy_001 "https://upload.wikimedia.org/wikipedia/commons/a/a4/Nento-Hiramatsu_Pine_Tree_202603_03.jpg"`) |
| 10-12 | Chene de Venon | Venon | the night run approved a photograph (overrule: `photo_apply.py hold vno_001 "https://upload.wikimedia.org/wikipedia/commons/6/67/Le_majestueux_ch%C3%AAne_de_Venon.jpg"`) |
| 10-12 | The Opatovice Pine | Velke Opatovice | the night run approved a photograph (overrule: `photo_apply.py hold vop_001 "https://upload.wikimedia.org/wikipedia/commons/a/ae/Opatovick%C3%A1_borovice.JPG"`) |
| 10-12 | The Oak of Erentrudishof | Salzburg | the night run approved a photograph (overrule: `photo_apply.py hold szb_002 "https://upload.wikimedia.org/wikipedia/commons/9/94/00019_Eiche_am_Erentrudishof%2C_Stift_Nonnberg.jpg"`) |
| 10-12 | The Courtyard Oak of Aigner Straße | Salzburg | the night run approved a photograph (overrule: `photo_apply.py hold szb_011 "https://upload.wikimedia.org/wikipedia/commons/6/6e/Eiche_an_der_Aigner_Strasse_9_%281%29.JPG"`) |
| 10-12 | The Tassilolinde | Wessobrunn | the night run approved a photograph (overrule: `photo_apply.py hold wes_001 "https://upload.wikimedia.org/wikipedia/commons/a/ab/Tassilolinde_Wessobrunn_1.jpg"`) |
| 10-12 | Gupčeva lipa | Gornja Stubica | the night run approved a photograph (overrule: `photo_apply.py hold gst_001 "https://upload.wikimedia.org/wikipedia/commons/b/b8/2019_Gubec_linden_HR.jpg"`) |
| 10-12 | The Wodanseiken | Wolfheze | the night run approved a photograph (overrule: `photo_apply.py hold wlf_001 "https://upload.wikimedia.org/wikipedia/commons/2/24/20191007_WolfhezeWodanseiken_02.jpg"`) |

**Did the product happen**

| Action | Yesterday | 14 days | Ever | Last |
|---|---:|---:|---:|---|
| signin-open | 1 | 155 | 499 | yesterday |
| app-cta | 5 | 21 | 60 | yesterday |
| signin-oauth | 0 | 4 | 41 | 4 days ago |
| directions | 0 | 4 | 39 | 4 days ago |
| signin-done | 0 | 1 | 39 | 6 days ago |
| search-home | 1 | 20 | 31 | yesterday |
| app-open | 0 | 9 | 19 | 3 days ago |
| suggestion-submit | 0 | 0 | 17 | 18 days ago |
| home-country | 1 | 7 | 10 | yesterday |
| home-fav | 0 | 5 | 9 | 4 days ago |
| signin-link-sent | 0 | 0 | 6 | 18 days ago |
| save | 0 | 1 | 5 | 11 days ago |
| waitlist-submit | 0 | 1 | 5 | 3 days ago |
| home-dir-tree | 0 | 0 | 3 | 20 days ago |
| search-explore | 0 | 1 | 3 | 11 days ago |
| visit | 0 | 0 | 3 | 23 days ago |
| app-page-badge | 0 | 2 | 2 | 4 days ago |
| home-species | 0 | 0 | 2 | 22 days ago |
| walks-app | 0 | 0 | 2 | 20 days ago |
| home-dir-species | 0 | 1 | 1 | 2 days ago |
| sponsor-open | 0 | 0 | 1 | 23 days ago |
| worthit-report | 0 | 0 | 1 | 19 days ago |
| worthit-report detail | 0 | 0 | 1 | 19 days ago |
| worthit-worth it | 0 | 0 | 1 | 23 days ago |
| worthit-not worth it | 0 | 0 | 0 | never |
| **all** | **8** | **232** | **800** | |
- 'Ever' counts every row in the events table, which begins 2026-08-01 when the funnel was repaired. Anything named here with a zero has never fired at all.

**What people typed into our search** (14 days, 17 searches, 14 different terms)

| Typed | Times |
|---|---:|
| lisboa | 3 |
| bruss | 2 |
| brussel | 1 |
| cop | 1 |
| granada | 1 |
| guimaraes | 1 |
| lis | 1 |
| lisb | 1 |
| manc | 1 |
| mu | 1 |
| oslo | 1 |
| phila | 1 |
| portland | 1 |
| tokyo | 1 |

| Day | Accounts | Android waitlist | Saves | Trees sent | Feedback | Ambassador asks |
|---|---:|---:|---:|---:|---:|---:|
| 09-29 | 0 | 0 | 0 | 0 | 0 | 0 |
| 09-30 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-01 | 3 | 0 | 0 | 0 | 3 | 0 |
| 10-02 | 0 | 0 | 1 | 0 | 0 | 0 |
| 10-03 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-04 | 0 | 0 | 0 | 1 | 0 | 0 |
| 10-05 | 2 | 0 | 0 | 1 | 0 | 0 |
| 10-06 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-07 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-08 | 1 | 0 | 0 | 0 | 1 | 0 |
| 10-09 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-10 | 1 | 1 | 0 | 0 | 0 | 0 |
| 10-11 | 1 | 0 | 0 | 0 | 0 | 0 |
| 10-12 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-13 | 0 | 0 | 0 | 0 | 0 | 0 |
| **14 days** | **8** | **1** | **1** | **2** | **4** | **0** |
- Our own rows are not in this table: 60 trees, 58 feedback, 3 accounts. They are testing, and counting them reads as traction.

| Ambassadors | Yesterday | 14 days | Total |
|---|---:|---:|---:|
| Granted | 0 | 6 | 6 |
| Invitations sent (app contributors) | 1 | 7 | 7 |
| Open-seat requests answered | 0 | 0 | 0 |
- New in 14 days: Hans Erik Lund (Copenhagen) since 2026-10-02, Giulia Torta (Florence) since 2026-10-03, Hugo Veríssimo (Lisbon) since 2026-10-05, Aleš Rudl (Prague) since 2026-10-05, Daniel Daggfeldt (Stockholm) since 2026-10-05, Kerry Pickett (Brighton) since 2026-10-10.
- Android waitlist: 21 total, newest 3 days ago
- Submissions: 33 total (19 trees sent, 14 feedback), newest 5 days ago
- Accounts:    26 total, newest 2 days ago

**What readers told us** (14 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 09-29 | 8BFEB681-540D-4B78-8DF5-06A95191AD | tree sent in | - | us | - |
| 09-29 | B9A2D2DF-77BA-4240-8C90-63CA0A83B1 | tree sent in | - | us | - |
| 09-29 | A54BCE9E-B822-4E4D-A14D-2097523C4D | tree sent in | 62 chars, read it in the database | us | - |
| 09-29 | 0EE5B139-7042-4BCB-A109-4E8B8D0511 | tree sent in | 62 chars, read it in the database | us | - |
| 10-01 | 74066D89-9958-4D93-BFDC-1C78ED97EE | tree sent in | - | us | - |
| 10-01 | E36A052C-3A48-4EED-BA48-5AB48574FA | tree sent in | - | us | - |
| 10-01 | lis_030 (The Dragon Tree of Quinta | worth it | - | 08aa | holds |
| 10-01 | par_031 (The Horse Chestnut of Squ | worth it | - | cfe8 | holds |
| 10-01 | par_033 (The Turkey Oak of Square  | worth it | - | cfe8 | holds |
| 10-02 | par_031 (The Horse Chestnut of Squ | worth it | - | us | - |
| 10-02 | lis_030 (The Dragon Tree of Quinta | worth it | - | us | - |
| 10-02 | 59E829E3-784F-4302-A98E-2C40D1BE88 | tree sent in | - | us | - |
| 10-04 | 6151F7E2-9211-4C2B-8CE8-E1BF17DAA3 | tree sent in | - | us | - |
| 10-04 | 8F4E7266-CC24-46B3-9A6D-5E8A94BBA1 | tree sent in | - | cfe8 | open_question |
| 10-05 | Reykjavik | ambassador request | - | us | - |
| 10-05 | rey_001 (The Whitebeam of Víkurgar | worth it | - | us | - |
| 10-05 | Barcelona | ambassador request | - | us | - |
| 10-05 | D9C08351-03D1-4B51-A6EC-972F08D308 | tree sent in | 648 chars, read it in the database | cfe8 | - |
| 10-06 | Tokyo | ambassador request | - | us | - |
| 10-06 | 7C8BEC8F-B77B-415C-B4EC-A1589130C4 | tree sent in | - | us | - |
| 10-06 | A4FA2700-1D89-4BF7-8F6E-0EAFA60DC4 | tree sent in | - | us | - |
| 10-06 | AE06E952-7DE0-46AB-AADA-AF2BE3D5C8 | tree sent in | - | us | - |
| 10-06 | D0D4EE1D-A0C3-4C4F-966F-EE01F7ECB5 | tree sent in | - | us | - |
| 10-06 | 038AB20E-98E0-4335-B154-08263B4949 | tree sent in | - | us | - |
| 10-06 | Verona | ambassador request | - | us | - |
| 10-07 | Rome | ambassador request | - | us | - |
| 10-08 | The Judas Tree of the Real Alcázar | correction sent in | 92 chars, read it in the database | eed7 | open_question |
| 10-09 | Amsterdam | ambassador request | - | us | - |
| 10-09 | Paris | ambassador request | - | us | - |
| 10-09 | Berlin | ambassador request | - | us | - |
| 10-10 | Baarn | ambassador request | - | us | - |
| 10-11 | - | Test | - | us | - |
| 10-11 | brn_008 (The Town Hall Plane) | worth it | - | us | - |
| 10-11 | brn_008 (The Town Hall Plane) | worth it | - | us | - |
| 10-12 | 452E8EFB-4537-4FC4-BE23-ABFCE3F959 | tree sent in | - | us | - |
| 10-12 | 0F8D03E1-CE4A-4BC6-8ACC-719C43E443 | correction sent in | 102 chars, read it in the database | us | - |
| 10-12 | Berlin | ambassador request | - | us | - |

- 31 of these 37 rows are ours, marked us. The rest is the reader traffic.
- 4 of the other 6 came from one account (cfe8), which is one person rather than a pattern.

**The funnel, as rates**
- Seen to clicked: 4.2% (27 of 643) vs 2.3% the fortnight before
- Pages per visit: 1.3 (6400 visits, 8100 pageviews since 2026-09-15)
- Visits that did something: 12.8% (818 actions on 6400 visits)

**What people did in the app**

| What | Yesterday | 14 days | Ever | Last |
|---|---:|---:|---:|---|
| app_open | 5 | 80 | 295 | yesterday |
| tab | 4 | 48 | 314 | yesterday |
| tree_opened | 9 | 277 | 1236 | yesterday |
| directions | 0 | 7 | 45 | 4 days ago |
| tree_saved | 0 | 3 | 19 | 12 days ago |
| tree_visited | 0 | 13 | 27 | 2 days ago |
| sighting_recorded | 0 | 21 | 73 | 2 days ago |
| sync_skipped | 0 | 0 | 0 | never |
| sync_failed | 0 | 0 | 0 | never |
| **all** | **18** | **449** | **2009** | |
- Measuring since 2026-08-30, when Measure.swift went in. Unlinked to any account by design: an install id, the app version and the OS, nothing else.
- Ours is not in this table: 22 install(s), 961 events, the testing before the app went live on 2026-09-03 and every install built by Xcode since (the app says how it was built with each event). An App Store copy on our own phone is the one kind this cannot see.
- 82 installs have ever sent anything. An install id is made fresh on each install, so this is an upper bound on people, not a count of them.
- Yesterday came from 3 installs, and the busiest made 12 of 3 events (400%). One install making most of a day is what our own reinstall looks like: add its id to excluded_installs in data/app-measure.json if it is ours.
- Tabs opened (14d): Discover 22; My trees 16; Map 10
- Active phones: 2 in the last day, 23 in the last 7 days, 60 in the last 30 days.
- Coming back: 25 of those 60 phones opened the app on more than one day (42%).
- Trees opened by the most phones (14d): The Dragon Tree of Quinta Conde dos Arcos (Lisbon) 2; The Cedro de Runa (Runa) 2; The Great White Oak of Logan (Logan Oak) (Logan, Ohio) 2; The Olive Trees of Santo Amaro (Lisbon) 2; The Arenbergpark Plane (Leuven) 2
- Where the phones are (30d): United States 13; United Kingdom 9; The Netherlands 5; Portugal 5; Italy 4; Switzerland 3
- Trees recorded (14d): a tree we map 18; a tree we do not 3
  A sighting reaches our database only through an account. Signed out it stays on the phone, so this count can run ahead of the trees and photographs we actually receive.

**Trees collected in the app** (14 days, a person standing at the tree)

| Day | Tree | Where | Install | Build | Signed in |
|---|---|---|---|---|---|
| 10-11 | The Lagunària de la Llotja | Palma de Mallorca | A98A | ? | ? |
| 10-08 | The Stone Pine of the Jardines de Cristina | Seville | 92A2 | ? | ? |
| 10-08 | The Stone Pine of the Jardines de Cristina | Seville | 92A2 | ? | ? |
| 10-08 | The Stone Pine of the Jardines de Cristina | Seville | 92A2 | ? | ? |
| 10-05 | The Finer Holm Oak of Edinburgh Gardens | Melbourne | 2D66 | ? | ? |
| 10-05 | The Southern Mahogany of Edinburgh Gardens | Melbourne | 2D66 | ? | ? |
| 10-03 | The Larch of Hólavallagarður | Reykjavik | 5781 | ? | ? |
| 10-03 | The City Hall Maple | Reykjavik | 5781 | ? | ? |
| 10-03 | The Whitebeam of Víkurgarður | Reykjavik | 5781 | ? | ? |
| 10-01 | The Turkey Oak of Square Rene-Le Gall | Paris | 0E84 | ? | ? |
| 10-01 | The Turkey Oak of Square Rene-Le Gall | Paris | 0E84 | ? | ? |
| 10-01 | The Horse Chestnut of Square Rene-Le Gall | Paris | 0E84 | ? | ? |
| 10-01 | The Dragon Tree of Quinta Conde dos Arcos | Lisbon | B792 | ? | ? |

**The app as a builder reads it** (this week against the week before; the weakest row is the work)

| Link | This week | Week before |
|---|---|---|
| New phones | 15 | 7 |
| First day: opened a tree | 9 of 15 (60%) | 6 of 7 (86%) |
| First day: opened a tree near them | - | - |
| First day: allowed location | - | - |
| First day: Take me there | 1 of 15 (7%) | 2 of 7 (29%) |
| First day: collected a tree | 2 of 15 (13%) | 3 of 7 (43%) |
| Back within a week | 4 of 7 (57%) | 8 of 13 (62%) |
| Trees collected (all phones) | 4 | 12 |
- Near and location count only phones on a version that sends them (from 2026-10-10); a dash means none yet.
- Back within a week looks at the phones that arrived a week earlier, so each has had its seven days.

**App Store downloads** (Apple's own count, not PostHog)

| Day | Downloads |
|---|---:|
| 2026-09-27 | 2 |
| 2026-09-30 | 1 |
| 2026-10-01 | 2 |
| 2026-10-02 | 1 |
| 2026-10-03 | 1 |
| 2026-10-05 | 1 |
| 2026-10-08 | 4 |
| 2026-10-09 | 4 |
| 2026-10-10 | 5 |
| **9 days** | **21** |
- First-time downloads only, which is what App Store Connect's Trends screen counts; redownloads and updates are not in this table.

**Where the downloads came from** (14 days, Apple's attribution)

| Came from | Via | Downloads |
|---|---|---:|
| App Store search | - | 10 |
| Web referrer | - | 6 |
| App referrer | - | 4 |
| App Store browse | - | 1 |
| **window** | | **21** |
- Countries: US (7); GB (5); BE (1); ES (1); FR (1); IE (1)
- Apple's own source split, first-time downloads only. "Web referrer" with our own domain is the site's app page; "App Store search" is somebody who typed into the store. "Unavailable" is Apple's word for a source it could not attribute.

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-03 | 2 | 72 | 2.8% | 32.0 |
| 10-04 | 1 | 50 | 2.0% | 28.8 |
| 10-05 | 4 | 47 | 8.5% | 39.0 |
| 10-06 | 1 | 45 | 2.2% | 34.5 |
| 10-07 | 0 | 47 | 0.0% | 34.7 |
| 10-08 | 5 | 35 | 14.3% | 21.8 |
| 10-09 | 3 | 37 | 8.1% | 49.5 |
| 10-10 | 0 | 35 | 0.0% | 29.8 |
| 10-11 | 1 | 32 | 3.1% | 31.7 |
| 10-12 *partial* | 1 | 18 | 5.6% | 24.3 |
| **window** | **18** | **418** | **4.3%** | |
- Top queries (10d): pokaz na mapie (i1, p1); alte bäume (i3, p27); ancient douglas fir tree (i1, p48); ancient tree (i1, p65); angelystor (i1, p1)
- Top pages (10d): / (c6/i16); /brussels/oldest-tree (c3/i4); /brisbane/white-rabbit-tree-of-newstead-park (c1/i1); /cagliari/ficus-of-piazza-matteotti (c1/i1); /de/berlin/englischer-garten-wingnut (c1/i2)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'alte bäume' (i3, p27)
    - 'big sherman tree' (i2, p69)
    - 'pokaz na mapie' (i1, p1)
    - 'angelystor' (i1, p1)
    - 'araucaria norfolk' (i1, p88)
    - 'arbol de las pagodas' (i1, p33)
    - 'arbol mas antiguo de españa' (i1, p99)
    - 'avenue de laune' (i1, p24)
    - and 2 more
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR | Pages crawled | Pages in index |
|---|---:|---:|---:|---:|---:|
| 10-05 | 79 | 5 | 6.3% | 207 | 2106 |
| 10-06 | 65 | 2 | 3.1% | 192 | 2157 |
| 10-07 | 81 | 2 | 2.5% | 78 | 2244 |
| 10-08 | 168 | 4 | 2.4% | - | - |
| 10-09 | 47 | 2 | 4.3% | - | - |
| 10-10 | 57 | 1 | 1.8% | - | - |
| 10-11 | 53 | 2 | 3.8% | - | - |
| **7 days** | **550** | **18** | **3.3%** | **477** | **2244** |
- Week before: 87 impressions, 6 clicks; in index then: 2106. No Bing demotion in sight.
- Top Bing queries: trees in the plaza dus burgos seville (c1/i3, p5); ancient trees in wiesbaden germany (c1/i2, p6); berlin tree (c1/i2, p1); oldest tree in belfast (c1/i2, p1); oldest live oak trees in new orleans (c1/i2, p6); remarkable trees copenhagen (c1/i2, p4); french trees found in paris (c1/i2, p6); husalle lindens copenhagen (c1/i2, p3)
- Bing alone, from Bing Webmaster Tools; the in-index column is the last day's count. DuckDuckGo and Yahoo draw on the same index and are not in these numbers. Bing's data lags about two days.

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 729 |
| Clicks | 18 |
| Pages that got at least one impression | 250 |
| Impressions on the proven cities | 625 |

What we did (context, proves nothing by itself): 2891 trees Google may index, 779 kept out for lacking a photo and an exact pin, 4638 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 471 | 23 | 215 | 0.46 | 3 |
| Not yet rich | 526 | 26 | 51 | 0.10 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| prague | 0 | 314 | 0.0% | 5.6 | 5.7% | prague (i17, p1) |
| sequoia-national-park | 0 | 24 | 0.0% | 73.4 | 0.4% | general sherman tree california (i5, p74) |
| brussels | 3 | 12 | 25.0% | 10.9 | 2.2% | klint white mulberry (i2, p52) |
| olympic-national-park | 0 | 12 | 0.0% | 11.6 | 1.9% | duncan cedar (i11, p6) |
| singapore | 4 | 359 | - | - | - | frozen 09-27 roster |
| lisbon | 5 | 316 | - | - | - | frozen 09-27 roster |
| amsterdam | 7 | 284 | - | - | - | frozen 09-27 roster |
| barcelona | 3 | 284 | - | - | - | frozen 09-27 roster |
| seville | 7 | 259 | - | - | - | frozen 09-27 roster |
| bath | 9 | 255 | - | - | - | frozen 09-27 roster |
| tenerife | 3 | 241 | - | - | - | frozen 09-27 roster |
| berlin | 5 | 224 | - | - | - | frozen 09-27 roster |
| rome | 3 | 221 | - | - | - | frozen 09-27 roster |
| palermo | 2 | 216 | - | - | - | frozen 09-27 roster |
| oahu | 1 | 213 | - | - | - | frozen 09-27 roster |
| tokyo | 5 | 209 | - | - | - | frozen 09-27 roster |
| munich | 8 | 206 | - | - | - | frozen 09-27 roster |
| new-york | 3 | 188 | - | - | - | frozen 09-27 roster |
| edinburgh | 8 | 173 | - | - | - | frozen 09-27 roster |
| dublin | 6 | 168 | - | - | - | frozen 09-27 roster |
| brisbane | 6 | 163 | - | - | - | frozen 09-27 roster |
| paris | 2 | 163 | - | - | - | frozen 09-27 roster |
| malaga | 7 | 161 | - | - | - | frozen 09-27 roster |
| vienna | 4 | 161 | - | - | - | frozen 09-27 roster |
| south-korea | 0 | 152 | - | - | - | frozen 09-27 roster |
| london | 3 | 147 | - | - | - | frozen 09-27 roster |
| alicante | 1 | 146 | - | - | - | frozen 09-27 roster |
| athens | 4 | 130 | - | - | - | frozen 09-27 roster |
| cadiz | 5 | 125 | - | - | - | frozen 09-27 roster |
| pamplona | 1 | 125 | - | - | - | frozen 09-27 roster |
| porto | 1 | 124 | - | - | - | frozen 09-27 roster |
| cagliari | 3 | 116 | - | - | - | frozen 09-27 roster |
| glasgow | 2 | 110 | - | - | - | frozen 09-27 roster |
| ede | 0 | 100 | - | - | - | frozen 09-27 roster |
| hinode | 0 | 98 | - | - | - | frozen 09-27 roster |
| palma-de-mallorca | 2 | 95 | - | - | - | frozen 09-27 roster |
| los-angeles | 1 | 94 | - | - | - | frozen 09-27 roster |
| madrid | 0 | 93 | - | - | - | frozen 09-27 roster |
| arnhem | 1 | 92 | - | - | - | frozen 09-27 roster |
| milan | 1 | 92 | - | - | - | frozen 09-27 roster |
| krakow | 3 | 91 | - | - | - | frozen 09-27 roster |
| austin | 0 | 91 | - | - | - | frozen 09-27 roster |
| montreal | 9 | 90 | - | - | - | frozen 09-27 roster |
| houston | 4 | 90 | - | - | - | frozen 09-27 roster |
| sintra | 0 | 87 | - | - | - | frozen 09-27 roster |
| florence | 0 | 86 | - | - | - | frozen 09-27 roster |
| the-hague | 1 | 84 | - | - | - | frozen 09-27 roster |
| amerongen | 0 | 84 | - | - | - | frozen 09-27 roster |
| new-orleans | 1 | 83 | - | - | - | frozen 09-27 roster |
| switzerland | 0 | 83 | - | - | - | frozen 09-27 roster |
| reykjavik | 0 | 80 | - | - | - | frozen 09-27 roster |
| liverpool | 1 | 78 | - | - | - | frozen 09-27 roster |
| valencia | 3 | 77 | - | - | - | frozen 09-27 roster |
| guerneville | 0 | 76 | - | - | - | frozen 09-27 roster |
| copenhagen | 5 | 75 | - | - | - | frozen 09-27 roster |
| chicago | 2 | 72 | - | - | - | frozen 09-27 roster |
| nara | 2 | 72 | - | - | - | frozen 09-27 roster |
| warsaw | 1 | 72 | - | - | - | frozen 09-27 roster |
| istanbul | 4 | 70 | - | - | - | frozen 09-27 roster |
| rogalin | 1 | 70 | - | - | - | frozen 09-27 roster |
| cyprus | 2 | 69 | - | - | - | frozen 09-27 roster |
| nijmegen | 0 | 69 | - | - | - | frozen 09-27 roster |
| cork | 3 | 68 | - | - | - | frozen 09-27 roster |
| dallas | 1 | 68 | - | - | - | frozen 09-27 roster |
| venice | 1 | 68 | - | - | - | frozen 09-27 roster |
| hobart | 3 | 66 | - | - | - | frozen 09-27 roster |
| takeo | 0 | 65 | - | - | - | frozen 09-27 roster |
| fukuoka | 2 | 64 | - | - | - | frozen 09-27 roster |
| monterey | 2 | 64 | - | - | - | frozen 09-27 roster |
| netherlands | 2 | 63 | - | - | - | frozen 09-27 roster |
| ottawa | 2 | 63 | - | - | - | frozen 09-27 roster |
| portland | 2 | 63 | - | - | - | frozen 09-27 roster |
| sydney | 0 | 63 | - | - | - | frozen 09-27 roster |
| kanazawa | 2 | 60 | - | - | - | frozen 09-27 roster |
| sardinia | 0 | 60 | - | - | - | frozen 09-27 roster |
| greece | 2 | 58 | - | - | - | frozen 09-27 roster |
| vilnius | 0 | 57 | - | - | - | frozen 09-27 roster |
| coimbra | 1 | 56 | - | - | - | frozen 09-27 roster |
| borrowdale | 0 | 56 | - | - | - | frozen 09-27 roster |
| fulufjallet | 2 | 55 | - | - | - | frozen 09-27 roster |
| beijing | 1 | 55 | - | - | - | frozen 09-27 roster |
| madeira | 1 | 55 | - | - | - | frozen 09-27 roster |
| boston | 0 | 55 | - | - | - | frozen 09-27 roster |
| san-francisco | 0 | 55 | - | - | - | frozen 09-27 roster |
| seoul | 1 | 54 | - | - | - | frozen 09-27 roster |
| utrecht | 3 | 54 | - | - | - | frozen 09-27 roster |
| osaka | 1 | 53 | - | - | - | frozen 09-27 roster |
| crete | 4 | 52 | - | - | - | frozen 09-27 roster |
| hong-kong | 1 | 52 | - | - | - | frozen 09-27 roster |
| budapest | 1 | 51 | - | - | - | frozen 09-27 roster |
| kyoto | 1 | 51 | - | - | - | frozen 09-27 roster |
| leipzig | 1 | 51 | - | - | - | frozen 09-27 roster |
| granada | 2 | 50 | - | - | - | frozen 09-27 roster |
| logan-ohio | 1 | 50 | - | - | - | frozen 09-27 roster |
| seattle | 1 | 49 | - | - | - | frozen 09-27 roster |
| geneva | 3 | 48 | - | - | - | frozen 09-27 roster |
| ibiza | 2 | 47 | - | - | - | frozen 09-27 roster |
| melbourne | 3 | 47 | - | - | - | frozen 09-27 roster |
| toronto | 0 | 47 | - | - | - | frozen 09-27 roster |
| leuven | 7 | 46 | - | - | - | frozen 09-27 roster |
| haarlem | 1 | 46 | - | - | - | frozen 09-27 roster |
| stockholm | 2 | 45 | - | - | - | frozen 09-27 roster |
| zurich | 5 | 45 | - | - | - | frozen 09-27 roster |
| leeuwarden | 0 | 45 | - | - | - | frozen 09-27 roster |
| cambridge | 1 | 44 | - | - | - | frozen 09-27 roster |
| germany | 1 | 44 | - | - | - | frozen 09-27 roster |
| dubrovnik | 0 | 44 | - | - | - | frozen 09-27 roster |
| sweden | 0 | 44 | - | - | - | frozen 09-27 roster |
| naples | 1 | 43 | - | - | - | frozen 09-27 roster |
| washington-dc | 0 | 43 | - | - | - | frozen 09-27 roster |
| nice | 1 | 42 | - | - | - | frozen 09-27 roster |
| palo-alto | 0 | 42 | - | - | - | frozen 09-27 roster |
| strasbourg | 1 | 41 | - | - | - | frozen 09-27 roster |
| las-vegas | 0 | 41 | - | - | - | frozen 09-27 roster |
| amersfoort | 2 | 40 | - | - | - | frozen 09-27 roster |
| runnymede | 0 | 40 | - | - | - | frozen 09-27 roster |
| vancouver | 1 | 39 | - | - | - | frozen 09-27 roster |
| philadelphia | 0 | 38 | - | - | - | frozen 09-27 roster |
| kagoshima | 1 | 37 | - | - | - | frozen 09-27 roster |
| perth | 0 | 37 | - | - | - | frozen 09-27 roster |
| verona | 5 | 36 | - | - | - | frozen 09-27 roster |
| eindhoven | 3 | 36 | - | - | - | frozen 09-27 roster |
| mexico-city | 1 | 36 | - | - | - | frozen 09-27 roster |
| segovia | 1 | 36 | - | - | - | frozen 09-27 roster |
| sorrento | 0 | 35 | - | - | - | frozen 09-27 roster |
| tallinn | 3 | 34 | - | - | - | frozen 09-27 roster |
| helsinki | 1 | 34 | - | - | - | frozen 09-27 roster |
| oslo | 1 | 34 | - | - | - | frozen 09-27 roster |
| bristol | 0 | 33 | - | - | - | frozen 09-27 roster |
| glastonbury | 0 | 33 | - | - | - | frozen 09-27 roster |
| quebec-city | 1 | 32 | - | - | - | frozen 09-27 roster |
| girona | 0 | 32 | - | - | - | frozen 09-27 roster |
| bari | 1 | 31 | - | - | - | frozen 09-27 roster |
| leiden | 2 | 31 | - | - | - | frozen 09-27 roster |
| tricase | 1 | 31 | - | - | - | frozen 09-27 roster |
| bucaco | 0 | 31 | - | - | - | frozen 09-27 roster |
| craigends | 0 | 31 | - | - | - | frozen 09-27 roster |
| pittsburgh | 0 | 31 | - | - | - | frozen 09-27 roster |
| boise | 4 | 30 | - | - | - | frozen 09-27 roster |
| luxembourg-city | 0 | 30 | - | - | - | frozen 09-27 roster |
| spokane | 1 | 29 | - | - | - | frozen 09-27 roster |
| manchester | 1 | 28 | - | - | - | frozen 09-27 roster |
| taipei | 1 | 28 | - | - | - | frozen 09-27 roster |
| maastricht | 0 | 28 | - | - | - | frozen 09-27 roster |
| sapporo | 0 | 28 | - | - | - | frozen 09-27 roster |
| bangkok | 2 | 26 | - | - | - | frozen 09-27 roster |
| parma | 0 | 26 | - | - | - | frozen 09-27 roster |
| cologne | 0 | 25 | - | - | - | frozen 09-27 roster |
| laren-gelderland | 0 | 25 | - | - | - | frozen 09-27 roster |
| ljubljana | 0 | 25 | - | - | - | frozen 09-27 roster |
| groningen | 1 | 24 | - | - | - | frozen 09-27 roster |
| slovakia | 1 | 24 | - | - | - | frozen 09-27 roster |
| dordrecht | 2 | 23 | - | - | - | frozen 09-27 roster |
| lyon | 1 | 23 | - | - | - | frozen 09-27 roster |
| charleston | 0 | 23 | - | - | - | frozen 09-27 roster |
| frankfurt | 0 | 23 | - | - | - | frozen 09-27 roster |
| jaegerspris-nordskov | 0 | 23 | - | - | - | frozen 09-27 roster |
| naha | 0 | 23 | - | - | - | frozen 09-27 roster |
| schenklengsfeld | 2 | 22 | - | - | - | frozen 09-27 roster |
| cordoba | 2 | 22 | - | - | - | frozen 09-27 roster |
| otoyo | 1 | 22 | - | - | - | frozen 09-27 roster |
| bilu | 0 | 22 | - | - | - | frozen 09-27 roster |
| cardiff | 0 | 22 | - | - | - | frozen 09-27 roster |
| enschede | 0 | 22 | - | - | - | frozen 09-27 roster |
| higashi-hiroshima | 0 | 22 | - | - | - | frozen 09-27 roster |
| limmersdorf | 0 | 22 | - | - | - | frozen 09-27 roster |
| minneapolis | 0 | 22 | - | - | - | frozen 09-27 roster |
| savannah | 0 | 22 | - | - | - | frozen 09-27 roster |
| yabu | 0 | 22 | - | - | - | frozen 09-27 roster |
| bologna | 1 | 21 | - | - | - | frozen 09-27 roster |
| guimaraes | 3 | 21 | - | - | - | frozen 09-27 roster |
| caserta | 0 | 21 | - | - | - | frozen 09-27 roster |
| heidelberg | 0 | 21 | - | - | - | frozen 09-27 roster |
| tilburg | 0 | 21 | - | - | - | frozen 09-27 roster |
| zwolle | 0 | 21 | - | - | - | frozen 09-27 roster |
| catania | 1 | 20 | - | - | - | frozen 09-27 roster |
| belgrade | 0 | 20 | - | - | - | frozen 09-27 roster |
| chadds-ford | 0 | 20 | - | - | - | frozen 09-27 roster |
| menorca | 0 | 20 | - | - | - | frozen 09-27 roster |
| miyazaki | 0 | 20 | - | - | - | frozen 09-27 roster |
| sources | 1 | 19 | - | - | - | frozen 09-27 roster |
| bordeaux | 0 | 19 | - | - | - | frozen 09-27 roster |
| hawaii | 0 | 19 | - | - | - | frozen 09-27 roster |
| yakushima | 0 | 19 | - | - | - | frozen 09-27 roster |
| wessobrunn | 2 | 18 | - | - | - | frozen 09-27 roster |
| genoa | 2 | 18 | - | - | - | frozen 09-27 roster |
| nuremberg | 1 | 18 | - | - | - | frozen 09-27 roster |
| gojaus-miskas | 0 | 18 | - | - | - | frozen 09-27 roster |
| llangernyw | 0 | 18 | - | - | - | frozen 09-27 roster |
| oxford | 0 | 18 | - | - | - | frozen 09-27 roster |
| taiwan | 0 | 18 | - | - | - | frozen 09-27 roster |
| toulouse | 2 | 17 | - | - | - | frozen 09-27 roster |
| aarhus | 1 | 17 | - | - | - | frozen 09-27 roster |
| freiburg | 1 | 17 | - | - | - | frozen 09-27 roster |
| padua | 1 | 17 | - | - | - | frozen 09-27 roster |
| bergamo | 0 | 17 | - | - | - | frozen 09-27 roster |
| salzburg | 0 | 17 | - | - | - | frozen 09-27 roster |
| ghent | 1 | 16 | - | - | - | frozen 09-27 roster |
| hallstatt | 1 | 16 | - | - | - | frozen 09-27 roster |
| perouges | 1 | 16 | - | - | - | frozen 09-27 roster |
| biei | 0 | 16 | - | - | - | frozen 09-27 roster |
| macugnaga | 0 | 16 | - | - | - | frozen 09-27 roster |
| salamanca | 0 | 16 | - | - | - | frozen 09-27 roster |
| york | 0 | 16 | - | - | - | frozen 09-27 roster |
| nagoya | 1 | 15 | - | - | - | frozen 09-27 roster |
| timber-creek | 0 | 15 | - | - | - | frozen 09-27 roster |
| tolpuddle | 0 | 15 | - | - | - | frozen 09-27 roster |
| gornja-stubica | 1 | 14 | - | - | - | frozen 09-27 roster |
| stuttgart | 2 | 14 | - | - | - | frozen 09-27 roster |
| bratislava | 0 | 14 | - | - | - | frozen 09-27 roster |
| heinkenszand | 0 | 14 | - | - | - | frozen 09-27 roster |
| helmond | 0 | 14 | - | - | - | frozen 09-27 roster |
| oss | 0 | 14 | - | - | - | frozen 09-27 roster |
| otama | 0 | 14 | - | - | - | frozen 09-27 roster |
| rio-de-janeiro | 0 | 14 | - | - | - | frozen 09-27 roster |
| sulechow | 0 | 14 | - | - | - | frozen 09-27 roster |
| gdansk | 2 | 13 | - | - | - | frozen 09-27 roster |
| alkmaar | 0 | 13 | - | - | - | frozen 09-27 roster |
| den-bosch | 0 | 13 | - | - | - | frozen 09-27 roster |
| derby | 0 | 13 | - | - | - | frozen 09-27 roster |
| graz | 0 | 13 | - | - | - | frozen 09-27 roster |
| hoorn | 0 | 13 | - | - | - | frozen 09-27 roster |
| lausanne | 0 | 13 | - | - | - | frozen 09-27 roster |
| lucca | 0 | 13 | - | - | - | frozen 09-27 roster |
| nantes | 0 | 13 | - | - | - | frozen 09-27 roster |
| simsbury | 0 | 13 | - | - | - | frozen 09-27 roster |
| bilbao | 2 | 12 | - | - | - | frozen 09-27 roster |
| ronda | 1 | 12 | - | - | - | frozen 09-27 roster |
| belfast | 0 | 12 | - | - | - | frozen 09-27 roster |
| buenos-aires | 0 | 12 | - | - | - | frozen 09-27 roster |
| como | 0 | 12 | - | - | - | frozen 09-27 roster |
| deventer | 0 | 12 | - | - | - | frozen 09-27 roster |
| ekero | 0 | 12 | - | - | - | frozen 09-27 roster |
| hamburg | 0 | 12 | - | - | - | frozen 09-27 roster |
| tarragona | 1 | 11 | - | - | - | frozen 09-27 roster |
| trieste | 1 | 11 | - | - | - | frozen 09-27 roster |
| apeldoorn | 0 | 11 | - | - | - | frozen 09-27 roster |
| brno | 0 | 11 | - | - | - | frozen 09-27 roster |
| bruges | 0 | 11 | - | - | - | frozen 09-27 roster |
| canada | 0 | 11 | - | - | - | frozen 09-27 roster |
| delft | 0 | 11 | - | - | - | frozen 09-27 roster |
| dresden | 0 | 11 | - | - | - | frozen 09-27 roster |
| gottingen | 0 | 11 | - | - | - | frozen 09-27 roster |
| perugia | 0 | 11 | - | - | - | frozen 09-27 roster |
| riga | 0 | 11 | - | - | - | frozen 09-27 roster |
| senonches | 0 | 11 | - | - | - | frozen 09-27 roster |
| venon | 0 | 11 | - | - | - | frozen 09-27 roster |
| kauai | 1 | 10 | - | - | - | frozen 09-27 roster |
| regensburg | 1 | 10 | - | - | - | frozen 09-27 roster |
| tulsa | 1 | 10 | - | - | - | frozen 09-27 roster |
| assen | 0 | 10 | - | - | - | frozen 09-27 roster |
| cremines | 0 | 10 | - | - | - | frozen 09-27 roster |
| emmen | 0 | 10 | - | - | - | frozen 09-27 roster |
| matera | 0 | 10 | - | - | - | frozen 09-27 roster |
| nagano | 0 | 10 | - | - | - | frozen 09-27 roster |
| oklahoma-city | 0 | 10 | - | - | - | frozen 09-27 roster |
| ueda | 0 | 10 | - | - | - | frozen 09-27 roster |
| venlo | 0 | 10 | - | - | - | frozen 09-27 roster |
| viroflay | 0 | 10 | - | - | - | frozen 09-27 roster |

**Copy test**

```
Copy test: city-title-age-first (day 33 of 56, review 2026-11-05)
The age is the hook and the count is inventory, so naming the oldest tree before the number earns more clicks.

  control      n1    before 1.38  now 0.00  change -1.38

  TOO EARLY. At about 2 clicks per page per ten days this needs the full window; a lead now is noise wearing a result's clothes.
```

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| before 2026-09-23 | The Twisted Muku of Omiya Gate, Kyoto  | Kyoto | - | publish | - |
| 2026-10-12 | The Town Hall Plane | Baarn | - | publish | - |
| 2026-10-12 | The Town Hall Plane | Baarn | - | publish | - |
| 2026-10-12 | The Town Hall Plane | Baarn | - | hold | - |
| 2026-10-12 | The Lagunària de la Llotja | Palma de Mallorca | - | publish | - |
| 2026-10-06 | A tree in Tokyo | - | - | lead | - |
| 2026-10-06 | A tree in Tokyo | - | - | lead | - |
| 2026-10-06 | Ginkgo in Tokyo | - | - | lead | - |
| 2026-10-06 | A tree in Tokyo | - | - | lead | - |
| 2026-10-06 | A tree in Tokyo | - | - | lead | - |
| 2026-10-05 | The Southern Mahogany of Edinburgh Gar | Melbourne | - | publish | - |
| 2026-10-05 | The Finer Holm Oak of Edinburgh Garden | Melbourne | - | hold | - |
| 2026-10-05 | London Plane in Paris | - | 88% girth | lead | - |
| 2026-10-04 | Ginkgo in Tokyo | - | - | lead | - |
| 2026-10-04 | Pedunculate Oak | - | 112% girth | lead | - |

0 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**The language test** (Contract J v1.13: a translated set should pass its English twin's impressions within four weeks of indexing):

| Lang | City | Clicks | Impressions | Position | English twin |
|---|---|---:|---:|---:|---:|
| es | tenerife | 0 | 14 | 44.9 | 7 |
| es | barcelona | 0 | 12 | 31.6 | 3 |
| de | vienna | 0 | 8 | 28.4 | 1 |
| ja | fukuoka | 0 | 8 | 25.0 | 0 |
| de | graz | 0 | 6 | 45.2 | 0 |
| it | rome | 1 | 5 | 26.2 | 1 |
| es | madrid | 0 | 5 | 52.4 | 1 |
| fr | lyon | 0 | 5 | 64.4 | 2 |
| de | hamburg | 0 | 4 | 24.5 | 0 |
| es | cadiz | 0 | 4 | 55.2 | 0 |
| pt | rio-de-janeiro | 0 | 4 | 9.8 | 0 |
| de | berlin | 1 | 3 | 26.3 | 2 |
| es | seville | 1 | 3 | 16.7 | 5 |
| fr | paris | 0 | 3 | 17.0 | 4 |
| nl | amsterdam | 0 | 3 | 51.3 | 2 |
| nl | arnhem | 0 | 3 | 83.3 | 0 |
| de | munich | 0 | 2 | 11.0 | 6 |
| es | palma-de-mallorca | 0 | 2 | 75.5 | 1 |
| ja | kyoto | 0 | 2 | 1.0 | 2 |
| de | regensburg | 0 | 1 | 52.0 | 0 |
| de | zurich | 0 | 1 | 12.0 | 0 |
| es | alicante | 0 | 1 | 86.0 | 3 |
| es | malaga | 0 | 1 | 25.0 | 0 |
| fr | bordeaux | 0 | 1 | 28.0 | 0 |
| fr | nantes | 0 | 1 | 27.0 | 0 |
| fr | nice | 0 | 1 | 6.0 | 0 |
| it | palermo | 0 | 1 | 10.0 | 0 |
| ja | kagoshima | 0 | 1 | 83.0 | 1 |
| ja | kanazawa | 0 | 1 | 89.0 | 2 |
| ja | tokyo | 0 | 1 | 5.0 | 2 |
| nl | the-hague | 0 | 1 | 1.0 | 1 |

**Cities seen but never clicked** (60+ impressions, zero clicks, with what they are actually shown for):

- prague (i159): prague (i17, p9); prague (i17, p8); prague (i17, p7); prague (i17, p5)
- Seen, not clicked: /sequoia-national-park/general-sherman-tree (c0/i23, 0.0%) for general sherman tree california (i5, p74); sequoia tree general sherman (i2, p71); sequoia national park general sherman (i2, p61)

**Who they are**
Audience, 28 days of search (679 clicks, 28778 impressions):
- Countries: usa c96/i7075; esp c62/i2300; nld c61/i1511; gbr c57/i2218; deu c49/i1515
- Devices: MOBILE c489/i17143; DESKTOP c182/i11297; TABLET c8/i338
- Landing pages: / c23/i262; /prague c11/i293; /bath/plane-trees-of-the-circus c7/i141; /de/vienna/chestnut-avenue-of-the-hauptallee c7/i207; /leuven c7/i48

Web Analytics (beacon, cookieless), people only.
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews | From Google |
|---|---:|---:|---:|
| 10-05 | 30 | 80 | 10 |
| 10-06 | 90 | 160 | 0 |
| 10-07 | 70 | 150 | 0 |
| 10-08 | 10 | 90 | 0 |
| 10-09 | 60 | 150 | 0 |
| 10-10 | 40 | 140 | 10 |
| 10-11 | 30 | 90 | 0 |
| 10-12 | 20 | 90 | 0 |
| **window** | **350** | **950** | **20** |
- Top paths: / (60); /explore (30); /leuven (30); /perth (20); /verona (20); /seville (20); /melbourne/hoop-pine-of-yarra-boulevard (20); /app (20); /rothenburg-ob-der-tauber/vorbachtal-spruces (20); /reykjavik/larch-of-holavallagardur (10); /washington-dc/washington-monument-witness-mulberry (10); /portalegre/plane-tree-of-rossio (10)
- Referrers: (direct) (170); ancienttrees.app (600); www.facebook.com (50); duckduckgo.com (40); search.yahoo.com (30); bing.com (10); www.google.com (10); de.search.yahoo.com (10); uk.search.yahoo.com (10); www.bing.com (10); com.google.android.gm (10)
- Moved between our own pages: 600 of 950 pageviews (63%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: US (230); BE (90); NL (80); GB (80); PT (70)
- Devices: mobile (660); desktop (290)
- Page load (8d): p50 2164ms, p90 7523ms

Links: external referrers (a link somebody actually clicked): www.facebook.com (50); search.yahoo.com (30); de.search.yahoo.com (10); uk.search.yahoo.com (10)
AI: arrivals from an assistant that cited us: none yet

Backlinks (watched pages):
| Site | Links to | rel | First seen |
|---|---|---|---|
| getlisbon.com | /lisbon | followed | 2026-09-08 |
| getlisbon.com | /pt/lisbon | followed | 2026-09-08 |
| www.baumkunde.de | /copenhagen | followed | 2026-09-26 |
| www.baumkunde.de | /rogalin/russ-oak | followed | 2026-09-26 |
4 linking page(s), 4 followed. Checked by fetching the page: a link with rel="noreferrer" never appears in the referrer table, so these two lines measure different things and neither replaces the other. Unknown links stay a manual read of Search Console's Links report. This run read 12 of 12 fetched (0 unreachable), out of 27 watched pages.

**Google Analytics** (last 7 days, visitors who accepted cookies)

| Day | People | New | Returning | Visits | Pageviews | Engaged visits |
|---|---:|---:|---:|---:|---:|---:|
| 10-12 | 3 | 3 | 0 | 4 | 7 | 3 |
| **window** | | **3** | | **4** | **7** | **3** |
- People per day are not summed: one person on two days is one person, and GA counts them once per day.
- Coming back (28 days): 0 returning against 3 new, 0% of the people GA saw.

| Page | Pageviews | People |
|---|---:|---:|
| / | 2 | 1 |
| /lisbon | 1 | 1 |
| /privacy | 1 | 1 |
| /singapore | 1 | 1 |
| /singapore/bodhi-tree-of-pearls-hill | 1 | 1 |
| /singapore/jamuju-of-lawn-h | 1 | 1 |

| Came from | Visits | People |
|---|---:|---:|
| (direct) / (none) | 4 | 3 |
- GA sees only visitors who pressed Accept on the cookie bar; read it as a sample. Cloudflare's table stays the count.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-12T08:26 | 0.0 | 0 | 0 | 0 | - |
| 10-12T12:56 | 29.9 | -9 | 21 | 4 | Palma De Mallorca +1, Baarn, Dresden, Kauai, +8 more |
| 10-12T18:55 | 87.8 | 0 | 20 | 0 | Amersfoort, Ancient Bristlecone Pine Forest, Crecy En Ponthieu, Dengfeng, +30 more |
| 10-12T20:25 | 66.8 | 2 | 20 | 3 | Vienna +2, Amersfoort, Ancient Bristlecone Pine Forest, Bucaco, +11 more |
| 10-13T01:15 | 21.3 | 2 | 5 | 0 | Roosendaal +2, Alicante, Ghent, Hong Kong |
| 10-13T01:46 | 4.0 | 0 | 5 | 0 | Roosendaal |
| **6 runs** | **210** | **-5** | **71** | | |

- 3 of 6 produced no trees; 3 to 4 commands refused per run; 1 wrote nothing to LOG.md; last build that went live: 3h ago.

**What they made**

- Frankfurt verify pass: two leads, wall; release claim; LOG and costs
- Roosendaal: London Plane carries the one scientific name (fixes red build, hard rule 9)
- Record when each page last changed
- Miami, Oss, Batenburg verify passes: leads filed, Oss staged at three; LOG and costs
- Roosendaal: two register-backed trees (London Plane of De Kring, Baumann's Horse Chestnut); roo_001 recognition fixed; LOG and costs
- Ghent Massemen lime photograph approved; Nuremberg verify wall; photo pass rejects recorded; LOG and costs
- Photographs readers sent, queued for a look; vouched ones live
- Record when each page last changed
- Guimarães Portuguese translation; English process leaks and wrong building fixed; LOG and costs
- Buçaco Portuguese translation; English contradictions and process narration fixed; LOG and costs
- Emmen Dutch translation; English FAQ and context wording fixed; LOG and costs
- Vienna second verify pass: cadastre unreachable, 5 leads filed, wall; LOG and costs
- Vienna: two Grinzing Naturdenkmal trees (vie_057, vie_058) with German overlay; claim released; LOG and costs
- Dutch translations for Ghent and Den Bosch; English claims the translator doubted removed; LOG and costs

Machine: 5 chain attempts yesterday, 3 got real work time (~241 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 1 clicks and 18 impressions on Google's freshest day (day before: c1/i32). Directional at best; no strategic conclusions from these volumes.

## Weekly analysis 2026-10-12

Eleventh weekly analysis. Compares 10-05 to 10-11 with 09-28 to 10-04, read
from the daily entries. 10-11 is partial in Search Console. The prior row is
the figure written last week, so Google's later backfill can move it a little.

**Scorecard**

| Week | Impressions | Clicks | CTR | Avg position | Visits (beacon) | Directions (14d) | App-CTA (14d) | App downloads (first-time) | Waitlist total | Submissions total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 09-28 to 10-04 | 400 | 14 | 3.5% | 18 to 39 | 220 (8d) | 34 | 22 | 13 | 20 | 32 |
| 10-05 to 10-11 | 277 | 14 | 5.1% | 22 to 50 | 330 (7d) | 5 | 19 | 14 (3 days absent from the table) | 21 | 33 |

Device split (beacon, 7d): mobile 600 pageviews, desktop 270. Search clicks over
28 days: mobile 523 of 727.

**What moved:**
1. Google is still at the floor and slowly lower: 277 impressions in 7 days
   (about 40 a day, from about 57), 14 clicks, position 22 to 50. No
   recovery signal. The CTR rise is 14 clicks; it means nothing.
2. Bing now shows us more than Google does: 537 impressions and 18 clicks
   for 10-04 to 10-10, against 47 and 4 the week before, with the index at
   2,157 pages and no demotion. Its 18 clicks are more than Google's 14.
3. The one page with real exposure converts nothing. Prague holds 325 of
   the 462 impressions in the 10-day window at position 5.6 with 0 clicks;
   seolearn puts the loss at about 19 clicks per 10 days. Its pages
   (/prague/walks plus tree pages) climbed 18 to 33 impressions each.
4. Site visits 330 (7 days), 62% of pageviews moved between our own pages,
   and Google sent 20 visits. Directions fell from 34 to 5 on the 14-day
   count, the clearest product fall, but it follows the visit drop and the
   counts are small.
5. The app is steady: 14 first-time downloads (10 of the last 21 from App
   Store search), 13 new phones, 2 collected a tree on day one (15%, 33% the
   week before), back-within-a-week 56%. 5 accounts opened, 1 Android
   waitlist signup, 1 reader tree sent. The machine produced nothing in the
   last 24 hours (4 knocks, 0 minutes, 0 trees); the week meter reads 791
   minutes.

**Suggestions, ranked:**
1. **[run]** Fix the Prague title and meta for the query "prague" (i15 at
   positions 1 to 9, 0 clicks, about 19 clicks lost per 10 days). It is the
   only page where position is good and clicks are zero, so it looks like a
   snippet problem, not a content problem. First check whether those
   impressions are rank trackers rather than readers; if so, drop Prague
   from the depth list.
2. **[run]** Treat Bing as a real channel: pull its queries and pages for
   10-04 to 10-10 (queries such as "remarkable trees copenhagen" and "oldest
   tree in belfast" already click at positions 1 to 6) and give those pages
   the photograph, register link and access line first. Bing pages are
   earning clicks now when Google pages are not.
3. **[run]** Keep the sighting queue as rung 1 every knock. Only tree pages
   with a photograph are indexed, and reader photographs are the one steady
   source of new ones (a tree collected in the app in Palma on 10-11, Seville
   on 10-08).
4. **[sessie]** Find out why the machine did nothing on 4 knocks in a row
   (usage window closed, or the knock failing). Enrichment is the only work
   recovery mode allows and idle time is the largest unused lever.
5. **[FOR HIDDE]** The recovery-mode question stands and has gained a week:
   still about 40 impressions a day after 14 days. The Search Console Manual
   actions and Page indexing checks from last week are not answered in the
   data, and they decide between waiting and a reconsideration request.

**Watch next week:** Google daily impressions above 100, whether the Prague
CTR moves off 0%, Bing staying above Google, and whether the machine produces
trees again.

## 2026-10-11 (previous UTC day)

**Today: an account was opened yesterday (26 total); the machine produced nothing across all 4 knocks in the last 24h (0.0 real minutes total, 0 trees), not a quiet night.**

**Did the product happen**

| Action | Yesterday | 14 days | Ever | Last |
|---|---:|---:|---:|---|
| signin-open | 0 | 156 | 499 | today |
| app-cta | 0 | 19 | 56 | today |
| directions | 0 | 5 | 44 | 3 days ago |
| signin-oauth | 0 | 4 | 41 | 3 days ago |
| signin-done | 0 | 1 | 39 | 5 days ago |
| search-home | 1 | 21 | 30 | yesterday |
| app-open | 0 | 9 | 19 | 2 days ago |
| suggestion-submit | 0 | 0 | 17 | 17 days ago |
| home-country | 0 | 6 | 9 | 2 days ago |
| home-fav | 0 | 5 | 9 | 3 days ago |
| signin-link-sent | 0 | 0 | 6 | 17 days ago |
| save | 0 | 1 | 5 | 10 days ago |
| waitlist-submit | 0 | 1 | 5 | 2 days ago |
| home-dir-tree | 0 | 0 | 3 | 19 days ago |
| search-explore | 0 | 1 | 3 | 10 days ago |
| visit | 0 | 0 | 3 | 22 days ago |
| walks-app | 0 | 0 | 3 | 19 days ago |
| app-page-badge | 0 | 2 | 2 | 3 days ago |
| home-species | 0 | 0 | 2 | 21 days ago |
| home-dir-species | 1 | 1 | 1 | yesterday |
| sponsor-open | 0 | 0 | 1 | 22 days ago |
| worthit-report | 0 | 0 | 1 | 18 days ago |
| worthit-report detail | 0 | 0 | 1 | 18 days ago |
| worthit-worth it | 0 | 0 | 1 | 22 days ago |
| worthit-not worth it | 0 | 0 | 0 | never |
| **all** | **2** | **232** | **800** | |
- 'Ever' counts every row in the events table, which begins 2026-08-01 when the funnel was repaired. Anything named here with a zero has never fired at all.

**What people typed into our search** (14 days, 18 searches, 15 different terms)

| Typed | Times |
|---|---:|
| lisboa | 3 |
| bruss | 2 |
| brussel | 1 |
| cop | 1 |
| granada | 1 |
| guimaraes | 1 |
| lis | 1 |
| lisb | 1 |
| lisbon | 1 |
| mu | 1 |
| munich | 1 |
| oslo | 1 |
| phila | 1 |
| portland | 1 |
| tokyo | 1 |

| Day | Accounts | Android waitlist | Saves | Trees sent | Feedback | Ambassador asks |
|---|---:|---:|---:|---:|---:|---:|
| 09-28 | 0 | 0 | 0 | 0 | 0 | 0 |
| 09-29 | 0 | 0 | 0 | 0 | 0 | 0 |
| 09-30 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-01 | 3 | 0 | 0 | 0 | 3 | 0 |
| 10-02 | 0 | 0 | 1 | 0 | 0 | 0 |
| 10-03 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-04 | 0 | 0 | 0 | 1 | 0 | 0 |
| 10-05 | 2 | 0 | 0 | 1 | 0 | 0 |
| 10-06 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-07 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-08 | 1 | 0 | 0 | 0 | 1 | 0 |
| 10-09 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-10 | 1 | 1 | 0 | 0 | 0 | 0 |
| 10-11 | 1 | 0 | 0 | 0 | 0 | 0 |
| 10-12 | 0 | 0 | 0 | 0 | 0 | 0 |
| **14 days** | **8** | **1** | **1** | **2** | **4** | **0** |
- Our own rows are not in this table: 59 trees, 56 feedback, 3 accounts. They are testing, and counting them reads as traction.

| Ambassadors | Yesterday | 14 days | Total |
|---|---:|---:|---:|
| Granted | 0 | 6 | 6 |
| Invitations sent (app contributors) | 0 | 6 | 6 |
| Open-seat requests answered | 0 | 0 | 0 |
- New in 14 days: Copenhagen since 2026-10-02, Giulia Torta (Florence) since 2026-10-03, Hugo Veríssimo (Lisbon) since 2026-10-05, Aleš Rudl (Prague) since 2026-10-05, Daniel Daggfeldt (Stockholm) since 2026-10-05, Kerry Pickett (Brighton) since 2026-10-10.
- Android waitlist: 21 total, newest 2 days ago
- Submissions: 33 total (19 trees sent, 14 feedback), newest 4 days ago
- Accounts:    26 total, newest yesterday

**What readers told us** (14 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 09-28 | 50BAB485-DCC6-479F-A4FA-F45756D855 | tree sent in | - | us | - |
| 09-28 | 70E18AB5-CC32-492E-B2A4-A816E85458 | tree sent in | - | us | - |
| 09-29 | 8BFEB681-540D-4B78-8DF5-06A95191AD | tree sent in | - | us | - |
| 09-29 | B9A2D2DF-77BA-4240-8C90-63CA0A83B1 | tree sent in | - | us | - |
| 09-29 | A54BCE9E-B822-4E4D-A14D-2097523C4D | tree sent in | 62 chars, read it in the database | us | - |
| 09-29 | 0EE5B139-7042-4BCB-A109-4E8B8D0511 | tree sent in | 62 chars, read it in the database | us | - |
| 10-01 | 74066D89-9958-4D93-BFDC-1C78ED97EE | tree sent in | - | us | - |
| 10-01 | E36A052C-3A48-4EED-BA48-5AB48574FA | tree sent in | - | us | - |
| 10-01 | lis_030 (The Dragon Tree of Quinta | worth it | - | 08aa | holds |
| 10-01 | par_031 (The Horse Chestnut of Squ | worth it | - | cfe8 | holds |
| 10-01 | par_033 (The Turkey Oak of Square  | worth it | - | cfe8 | holds |
| 10-02 | par_031 (The Horse Chestnut of Squ | worth it | - | us | - |
| 10-02 | lis_030 (The Dragon Tree of Quinta | worth it | - | us | - |
| 10-02 | 59E829E3-784F-4302-A98E-2C40D1BE88 | tree sent in | - | us | - |
| 10-04 | 6151F7E2-9211-4C2B-8CE8-E1BF17DAA3 | tree sent in | - | us | - |
| 10-04 | 8F4E7266-CC24-46B3-9A6D-5E8A94BBA1 | tree sent in | - | cfe8 | open_question |
| 10-05 | Reykjavik | ambassador request | - | us | - |
| 10-05 | rey_001 (The Whitebeam of Víkurgar | worth it | - | us | - |
| 10-05 | Barcelona | ambassador request | - | us | - |
| 10-05 | D9C08351-03D1-4B51-A6EC-972F08D308 | tree sent in | 648 chars, read it in the database | cfe8 | - |
| 10-06 | Tokyo | ambassador request | - | us | - |
| 10-06 | 7C8BEC8F-B77B-415C-B4EC-A1589130C4 | tree sent in | - | us | - |
| 10-06 | A4FA2700-1D89-4BF7-8F6E-0EAFA60DC4 | tree sent in | - | us | - |
| 10-06 | AE06E952-7DE0-46AB-AADA-AF2BE3D5C8 | tree sent in | - | us | - |
| 10-06 | D0D4EE1D-A0C3-4C4F-966F-EE01F7ECB5 | tree sent in | - | us | - |
| 10-06 | 038AB20E-98E0-4335-B154-08263B4949 | tree sent in | - | us | - |
| 10-06 | Verona | ambassador request | - | us | - |
| 10-07 | Rome | ambassador request | - | us | - |
| 10-08 | The Judas Tree of the Real Alcázar | correction sent in | 92 chars, read it in the database | eed7 | open_question |
| 10-09 | Amsterdam | ambassador request | - | us | - |
| 10-09 | Paris | ambassador request | - | us | - |
| 10-09 | Berlin | ambassador request | - | us | - |
| 10-10 | Baarn | ambassador request | - | us | - |
| 10-11 | - | Test | - | us | - |
| 10-11 | brn_008 (The Town Hall Plane) | worth it | - | us | - |
| 10-11 | brn_008 (The Town Hall Plane) | worth it | - | us | - |

- 30 of these 36 rows are ours, marked us. The rest is the reader traffic.
- 4 of the other 6 came from one account (cfe8), which is one person rather than a pattern.

**The funnel, as rates**
- Seen to clicked: 4.1% (28 of 677) vs 2.3% the fortnight before
- Pages per visit: 1.3 (6370 visits, 8010 pageviews since 2026-09-14)
- Visits that did something: 12.8% (818 actions on 6370 visits)

**What people did in the app**

| What | Yesterday | 14 days | Ever | Last |
|---|---:|---:|---:|---|
| app_open | 3 | 78 | 291 | today |
| tab | 0 | 47 | 312 | today |
| tree_opened | 6 | 271 | 1228 | today |
| directions | 0 | 7 | 45 | 3 days ago |
| tree_saved | 0 | 3 | 19 | 11 days ago |
| tree_visited | 1 | 13 | 27 | yesterday |
| sighting_recorded | 1 | 22 | 73 | yesterday |
| sync_skipped | 0 | 0 | 0 | never |
| sync_failed | 0 | 0 | 0 | never |
| **all** | **11** | **441** | **1995** | |
- Measuring since 2026-08-30, when Measure.swift went in. Unlinked to any account by design: an install id, the app version and the OS, nothing else.
- Ours is not in this table: 22 install(s), 854 events, the testing before the app went live on 2026-09-03 and every install built by Xcode since (the app says how it was built with each event). An App Store copy on our own phone is the one kind this cannot see.
- 81 installs have ever sent anything. An install id is made fresh on each install, so this is an upper bound on people, not a count of them.
- Yesterday came from 2 installs, and the busiest made 10 of 2 events (500%). One install making most of a day is what our own reinstall looks like: add its id to excluded_installs in data/app-measure.json if it is ours.
- Tabs opened (14d): Discover 20; My trees 17; Map 10
- Active phones: 2 in the last day, 22 in the last 7 days, 60 in the last 30 days.
- Coming back: 24 of those 60 phones opened the app on more than one day (40%).
- Trees opened by the most phones (14d): The Dragon Tree of Quinta Conde dos Arcos (Lisbon) 2; The Cedro de Runa (Runa) 2; The Olive Trees of Santo Amaro (Lisbon) 2; The Arenbergpark Plane (Leuven) 2; The Great White Oak of Logan (Logan Oak) (Logan, Ohio) 2
- Where the phones are (30d): United States 14; United Kingdom 8; The Netherlands 5; Portugal 5; Italy 4; Switzerland 3
- Trees recorded (14d): a tree we map 18; a tree we do not 4
  A sighting reaches our database only through an account. Signed out it stays on the phone, so this count can run ahead of the trees and photographs we actually receive.

**Trees collected in the app** (14 days, a person standing at the tree)

| Day | Tree | Where | Install | Build | Signed in |
|---|---|---|---|---|---|
| 10-11 | The Lagunària de la Llotja | Palma de Mallorca | A98A | ? | ? |
| 10-08 | The Stone Pine of the Jardines de Cristina | Seville | 92A2 | ? | ? |
| 10-08 | The Stone Pine of the Jardines de Cristina | Seville | 92A2 | ? | ? |
| 10-08 | The Stone Pine of the Jardines de Cristina | Seville | 92A2 | ? | ? |
| 10-05 | The Finer Holm Oak of Edinburgh Gardens | Melbourne | 2D66 | ? | ? |
| 10-05 | The Southern Mahogany of Edinburgh Gardens | Melbourne | 2D66 | ? | ? |
| 10-03 | The Larch of Hólavallagarður | Reykjavik | 5781 | ? | ? |
| 10-03 | The City Hall Maple | Reykjavik | 5781 | ? | ? |
| 10-03 | The Whitebeam of Víkurgarður | Reykjavik | 5781 | ? | ? |
| 10-01 | The Turkey Oak of Square Rene-Le Gall | Paris | 0E84 | ? | ? |
| 10-01 | The Turkey Oak of Square Rene-Le Gall | Paris | 0E84 | ? | ? |
| 10-01 | The Horse Chestnut of Square Rene-Le Gall | Paris | 0E84 | ? | ? |
| 10-01 | The Dragon Tree of Quinta Conde dos Arcos | Lisbon | B792 | ? | ? |

**The app as a builder reads it** (this week against the week before; the weakest row is the work)

| Link | This week | Week before |
|---|---|---|
| New phones | 13 | 9 |
| First day: opened a tree | 8 of 13 (62%) | 7 of 9 (78%) |
| First day: opened a tree near them | - | - |
| First day: allowed location | - | - |
| First day: Take me there | 1 of 13 (8%) | 3 of 9 (33%) |
| First day: collected a tree | 2 of 13 (15%) | 3 of 9 (33%) |
| Back within a week | 5 of 9 (56%) | 8 of 12 (67%) |
| Trees collected (all phones) | 4 | 13 |
- Near and location count only phones on a version that sends them (from 2026-10-10); a dash means none yet.
- Back within a week looks at the phones that arrived a week earlier, so each has had its seven days.

**App Store downloads** (Apple's own count, not PostHog)

| Day | Downloads |
|---|---:|
| 2026-09-27 | 2 |
| 2026-09-30 | 1 |
| 2026-10-01 | 2 |
| 2026-10-02 | 1 |
| 2026-10-03 | 1 |
| 2026-10-05 | 1 |
| 2026-10-08 | 4 |
| 2026-10-09 | 4 |
| 2026-10-10 | 5 |
| **9 days** | **21** |
- First-time downloads only, which is what App Store Connect's Trends screen counts; redownloads and updates are not in this table.

**Where the downloads came from** (14 days, Apple's attribution)

| Came from | Via | Downloads |
|---|---|---:|
| App Store search | - | 10 |
| Web referrer | - | 6 |
| App referrer | - | 4 |
| App Store browse | - | 1 |
| **window** | | **21** |
- Countries: US (7); GB (5); BE (1); ES (1); FR (1); IE (1)
- Apple's own source split, first-time downloads only. "Web referrer" with our own domain is the site's app page; "App Store search" is somebody who typed into the store. "Unavailable" is Apple's word for a source it could not attribute.

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-02 | 2 | 63 | 3.2% | 39.1 |
| 10-03 | 2 | 72 | 2.8% | 32.0 |
| 10-04 | 1 | 50 | 2.0% | 28.8 |
| 10-05 | 4 | 47 | 8.5% | 39.0 |
| 10-06 | 1 | 45 | 2.2% | 34.5 |
| 10-07 | 0 | 47 | 0.0% | 34.7 |
| 10-08 | 5 | 35 | 14.3% | 21.8 |
| 10-09 | 3 | 37 | 8.1% | 49.5 |
| 10-10 | 0 | 35 | 0.0% | 29.8 |
| 10-11 *partial* | 1 | 31 | 3.2% | 32.4 |
| **window** | **19** | **462** | **4.1%** | |
- Top queries (10d): pokaz na mapie (i1, p1); alte bäume (i4, p27); ancient douglas fir tree (i1, p48); ancient tree (i1, p65); angelystor (i1, p1)
- Top pages (10d): / (c5/i13); /brussels/oldest-tree (c3/i4); /assisi (c1/i1); /brisbane/white-rabbit-tree-of-newstead-park (c1/i1); /cagliari/ficus-of-piazza-matteotti (c1/i1)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'alte bäume' (i4, p27)
    - 'big sherman tree' (i2, p69)
    - 'pokaz na mapie' (i1, p1)
    - 'angelystor' (i1, p1)
    - 'araucaria norfolk' (i1, p88)
    - 'arbol de las pagodas' (i1, p33)
    - 'arbol mas antiguo de españa' (i1, p99)
    - 'avenue de laune' (i1, p24)
    - and 2 more
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR | Pages crawled | Pages in index |
|---|---:|---:|---:|---:|---:|
| 10-04 | 40 | 2 | 5.0% | 88 | 2106 |
| 10-05 | 79 | 5 | 6.3% | 207 | 2106 |
| 10-06 | 65 | 2 | 3.1% | 192 | 2157 |
| 10-07 | 81 | 2 | 2.5% | - | - |
| 10-08 | 168 | 4 | 2.4% | - | - |
| 10-09 | 47 | 2 | 4.3% | - | - |
| 10-10 | 57 | 1 | 1.8% | - | - |
| **7 days** | **537** | **18** | **3.4%** | **487** | **2157** |
- Week before: 47 impressions, 4 clicks; in index then: 2041. No Bing demotion in sight.
- Top Bing queries: trees in the plaza dus burgos seville (c1/i3, p5); remarkable trees copenhagen (c1/i2, p4); french trees found in paris (c1/i2, p6); berlin tree (c1/i2, p1); oldest tree in belfast (c1/i2, p1); husalle lindens copenhagen (c1/i2, p3); ancient trees in wiesbaden germany (c1/i2, p6); oldest live oak trees in new orleans (c1/i2, p6)
- Bing alone, from Bing Webmaster Tools; the in-index column is the last day's count. DuckDuckGo and Yahoo draw on the same index and are not in these numbers. Bing's data lags about two days.

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 780 |
| Clicks | 19 |
| Pages that got at least one impression | 271 |
| Impressions on the proven cities | 670 |

What we did (context, proves nothing by itself): 2892 trees Google may index, 796 kept out for lacking a photo and an exact pin, 4638 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 431 | 23 | 218 | 0.51 | 3 |
| Not yet rich | 561 | 28 | 57 | 0.10 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| prague | 0 | 325 | 0.0% | 5.6 | 5.8% | prague (i15, p1) |
| sequoia-national-park | 0 | 22 | 0.0% | 74.3 | 0.4% | general sherman tree california (i5, p74) |
| olympic-national-park | 0 | 14 | 0.0% | 16.6 | 1.1% | duncan cedar (i11, p6) |
| brussels | 3 | 13 | 23.1% | 10.8 | 2.2% | klint white mulberry (i2, p52) |
| cambridge | 0 | 10 | 0.0% | 53.8 | 0.4% | newton's apple tree (i4, p42) |
| singapore | 4 | 359 | - | - | - | frozen 09-27 roster |
| lisbon | 5 | 316 | - | - | - | frozen 09-27 roster |
| amsterdam | 7 | 284 | - | - | - | frozen 09-27 roster |
| barcelona | 3 | 284 | - | - | - | frozen 09-27 roster |
| seville | 7 | 259 | - | - | - | frozen 09-27 roster |
| bath | 9 | 255 | - | - | - | frozen 09-27 roster |
| tenerife | 3 | 241 | - | - | - | frozen 09-27 roster |
| berlin | 5 | 224 | - | - | - | frozen 09-27 roster |
| rome | 3 | 221 | - | - | - | frozen 09-27 roster |
| palermo | 2 | 216 | - | - | - | frozen 09-27 roster |
| oahu | 1 | 213 | - | - | - | frozen 09-27 roster |
| tokyo | 5 | 209 | - | - | - | frozen 09-27 roster |
| munich | 8 | 206 | - | - | - | frozen 09-27 roster |
| new-york | 3 | 188 | - | - | - | frozen 09-27 roster |
| edinburgh | 8 | 173 | - | - | - | frozen 09-27 roster |
| dublin | 6 | 168 | - | - | - | frozen 09-27 roster |
| brisbane | 6 | 163 | - | - | - | frozen 09-27 roster |
| paris | 2 | 163 | - | - | - | frozen 09-27 roster |
| malaga | 7 | 161 | - | - | - | frozen 09-27 roster |
| vienna | 4 | 161 | - | - | - | frozen 09-27 roster |
| south-korea | 0 | 152 | - | - | - | frozen 09-27 roster |
| london | 3 | 147 | - | - | - | frozen 09-27 roster |
| alicante | 1 | 146 | - | - | - | frozen 09-27 roster |
| athens | 4 | 130 | - | - | - | frozen 09-27 roster |
| cadiz | 5 | 125 | - | - | - | frozen 09-27 roster |
| pamplona | 1 | 125 | - | - | - | frozen 09-27 roster |
| porto | 1 | 124 | - | - | - | frozen 09-27 roster |
| cagliari | 3 | 116 | - | - | - | frozen 09-27 roster |
| glasgow | 2 | 110 | - | - | - | frozen 09-27 roster |
| ede | 0 | 100 | - | - | - | frozen 09-27 roster |
| hinode | 0 | 98 | - | - | - | frozen 09-27 roster |
| palma-de-mallorca | 2 | 95 | - | - | - | frozen 09-27 roster |
| los-angeles | 1 | 94 | - | - | - | frozen 09-27 roster |
| madrid | 0 | 93 | - | - | - | frozen 09-27 roster |
| arnhem | 1 | 92 | - | - | - | frozen 09-27 roster |
| milan | 1 | 92 | - | - | - | frozen 09-27 roster |
| krakow | 3 | 91 | - | - | - | frozen 09-27 roster |
| austin | 0 | 91 | - | - | - | frozen 09-27 roster |
| montreal | 9 | 90 | - | - | - | frozen 09-27 roster |
| houston | 4 | 90 | - | - | - | frozen 09-27 roster |
| sintra | 0 | 87 | - | - | - | frozen 09-27 roster |
| florence | 0 | 86 | - | - | - | frozen 09-27 roster |
| the-hague | 1 | 84 | - | - | - | frozen 09-27 roster |
| amerongen | 0 | 84 | - | - | - | frozen 09-27 roster |
| new-orleans | 1 | 83 | - | - | - | frozen 09-27 roster |
| switzerland | 0 | 83 | - | - | - | frozen 09-27 roster |
| reykjavik | 0 | 80 | - | - | - | frozen 09-27 roster |
| liverpool | 1 | 78 | - | - | - | frozen 09-27 roster |
| valencia | 3 | 77 | - | - | - | frozen 09-27 roster |
| guerneville | 0 | 76 | - | - | - | frozen 09-27 roster |
| copenhagen | 5 | 75 | - | - | - | frozen 09-27 roster |
| chicago | 2 | 72 | - | - | - | frozen 09-27 roster |
| nara | 2 | 72 | - | - | - | frozen 09-27 roster |
| warsaw | 1 | 72 | - | - | - | frozen 09-27 roster |
| istanbul | 4 | 70 | - | - | - | frozen 09-27 roster |
| rogalin | 1 | 70 | - | - | - | frozen 09-27 roster |
| cyprus | 2 | 69 | - | - | - | frozen 09-27 roster |
| nijmegen | 0 | 69 | - | - | - | frozen 09-27 roster |
| cork | 3 | 68 | - | - | - | frozen 09-27 roster |
| dallas | 1 | 68 | - | - | - | frozen 09-27 roster |
| venice | 1 | 68 | - | - | - | frozen 09-27 roster |
| hobart | 3 | 66 | - | - | - | frozen 09-27 roster |
| takeo | 0 | 65 | - | - | - | frozen 09-27 roster |
| fukuoka | 2 | 64 | - | - | - | frozen 09-27 roster |
| monterey | 2 | 64 | - | - | - | frozen 09-27 roster |
| netherlands | 2 | 63 | - | - | - | frozen 09-27 roster |
| ottawa | 2 | 63 | - | - | - | frozen 09-27 roster |
| portland | 2 | 63 | - | - | - | frozen 09-27 roster |
| sydney | 0 | 63 | - | - | - | frozen 09-27 roster |
| kanazawa | 2 | 60 | - | - | - | frozen 09-27 roster |
| sardinia | 0 | 60 | - | - | - | frozen 09-27 roster |
| greece | 2 | 58 | - | - | - | frozen 09-27 roster |
| vilnius | 0 | 57 | - | - | - | frozen 09-27 roster |
| coimbra | 1 | 56 | - | - | - | frozen 09-27 roster |
| borrowdale | 0 | 56 | - | - | - | frozen 09-27 roster |
| fulufjallet | 2 | 55 | - | - | - | frozen 09-27 roster |
| beijing | 1 | 55 | - | - | - | frozen 09-27 roster |
| madeira | 1 | 55 | - | - | - | frozen 09-27 roster |
| boston | 0 | 55 | - | - | - | frozen 09-27 roster |
| san-francisco | 0 | 55 | - | - | - | frozen 09-27 roster |
| seoul | 1 | 54 | - | - | - | frozen 09-27 roster |
| utrecht | 3 | 54 | - | - | - | frozen 09-27 roster |
| osaka | 1 | 53 | - | - | - | frozen 09-27 roster |
| crete | 4 | 52 | - | - | - | frozen 09-27 roster |
| hong-kong | 1 | 52 | - | - | - | frozen 09-27 roster |
| budapest | 1 | 51 | - | - | - | frozen 09-27 roster |
| kyoto | 1 | 51 | - | - | - | frozen 09-27 roster |
| leipzig | 1 | 51 | - | - | - | frozen 09-27 roster |
| granada | 2 | 50 | - | - | - | frozen 09-27 roster |
| logan-ohio | 1 | 50 | - | - | - | frozen 09-27 roster |
| seattle | 1 | 49 | - | - | - | frozen 09-27 roster |
| geneva | 3 | 48 | - | - | - | frozen 09-27 roster |
| ibiza | 2 | 47 | - | - | - | frozen 09-27 roster |
| melbourne | 3 | 47 | - | - | - | frozen 09-27 roster |
| toronto | 0 | 47 | - | - | - | frozen 09-27 roster |
| leuven | 7 | 46 | - | - | - | frozen 09-27 roster |
| haarlem | 1 | 46 | - | - | - | frozen 09-27 roster |
| stockholm | 2 | 45 | - | - | - | frozen 09-27 roster |
| zurich | 5 | 45 | - | - | - | frozen 09-27 roster |
| leeuwarden | 0 | 45 | - | - | - | frozen 09-27 roster |
| germany | 1 | 44 | - | - | - | frozen 09-27 roster |
| dubrovnik | 0 | 44 | - | - | - | frozen 09-27 roster |
| sweden | 0 | 44 | - | - | - | frozen 09-27 roster |
| naples | 1 | 43 | - | - | - | frozen 09-27 roster |
| washington-dc | 0 | 43 | - | - | - | frozen 09-27 roster |
| nice | 1 | 42 | - | - | - | frozen 09-27 roster |
| palo-alto | 0 | 42 | - | - | - | frozen 09-27 roster |
| strasbourg | 1 | 41 | - | - | - | frozen 09-27 roster |
| las-vegas | 0 | 41 | - | - | - | frozen 09-27 roster |
| amersfoort | 2 | 40 | - | - | - | frozen 09-27 roster |
| runnymede | 0 | 40 | - | - | - | frozen 09-27 roster |
| vancouver | 1 | 39 | - | - | - | frozen 09-27 roster |
| philadelphia | 0 | 38 | - | - | - | frozen 09-27 roster |
| kagoshima | 1 | 37 | - | - | - | frozen 09-27 roster |
| perth | 0 | 37 | - | - | - | frozen 09-27 roster |
| verona | 5 | 36 | - | - | - | frozen 09-27 roster |
| eindhoven | 3 | 36 | - | - | - | frozen 09-27 roster |
| mexico-city | 1 | 36 | - | - | - | frozen 09-27 roster |
| segovia | 1 | 36 | - | - | - | frozen 09-27 roster |
| sorrento | 0 | 35 | - | - | - | frozen 09-27 roster |
| tallinn | 3 | 34 | - | - | - | frozen 09-27 roster |
| helsinki | 1 | 34 | - | - | - | frozen 09-27 roster |
| oslo | 1 | 34 | - | - | - | frozen 09-27 roster |
| bristol | 0 | 33 | - | - | - | frozen 09-27 roster |
| glastonbury | 0 | 33 | - | - | - | frozen 09-27 roster |
| quebec-city | 1 | 32 | - | - | - | frozen 09-27 roster |
| girona | 0 | 32 | - | - | - | frozen 09-27 roster |
| bari | 1 | 31 | - | - | - | frozen 09-27 roster |
| leiden | 2 | 31 | - | - | - | frozen 09-27 roster |
| tricase | 1 | 31 | - | - | - | frozen 09-27 roster |
| bucaco | 0 | 31 | - | - | - | frozen 09-27 roster |
| craigends | 0 | 31 | - | - | - | frozen 09-27 roster |
| pittsburgh | 0 | 31 | - | - | - | frozen 09-27 roster |
| boise | 4 | 30 | - | - | - | frozen 09-27 roster |
| luxembourg-city | 0 | 30 | - | - | - | frozen 09-27 roster |
| spokane | 1 | 29 | - | - | - | frozen 09-27 roster |
| manchester | 1 | 28 | - | - | - | frozen 09-27 roster |
| taipei | 1 | 28 | - | - | - | frozen 09-27 roster |
| maastricht | 0 | 28 | - | - | - | frozen 09-27 roster |
| sapporo | 0 | 28 | - | - | - | frozen 09-27 roster |
| bangkok | 2 | 26 | - | - | - | frozen 09-27 roster |
| parma | 0 | 26 | - | - | - | frozen 09-27 roster |
| cologne | 0 | 25 | - | - | - | frozen 09-27 roster |
| laren-gelderland | 0 | 25 | - | - | - | frozen 09-27 roster |
| ljubljana | 0 | 25 | - | - | - | frozen 09-27 roster |
| groningen | 1 | 24 | - | - | - | frozen 09-27 roster |
| slovakia | 1 | 24 | - | - | - | frozen 09-27 roster |
| dordrecht | 2 | 23 | - | - | - | frozen 09-27 roster |
| lyon | 1 | 23 | - | - | - | frozen 09-27 roster |
| charleston | 0 | 23 | - | - | - | frozen 09-27 roster |
| frankfurt | 0 | 23 | - | - | - | frozen 09-27 roster |
| jaegerspris-nordskov | 0 | 23 | - | - | - | frozen 09-27 roster |
| naha | 0 | 23 | - | - | - | frozen 09-27 roster |
| schenklengsfeld | 2 | 22 | - | - | - | frozen 09-27 roster |
| cordoba | 2 | 22 | - | - | - | frozen 09-27 roster |
| otoyo | 1 | 22 | - | - | - | frozen 09-27 roster |
| bilu | 0 | 22 | - | - | - | frozen 09-27 roster |
| cardiff | 0 | 22 | - | - | - | frozen 09-27 roster |
| enschede | 0 | 22 | - | - | - | frozen 09-27 roster |
| higashi-hiroshima | 0 | 22 | - | - | - | frozen 09-27 roster |
| limmersdorf | 0 | 22 | - | - | - | frozen 09-27 roster |
| minneapolis | 0 | 22 | - | - | - | frozen 09-27 roster |
| savannah | 0 | 22 | - | - | - | frozen 09-27 roster |
| yabu | 0 | 22 | - | - | - | frozen 09-27 roster |
| bologna | 1 | 21 | - | - | - | frozen 09-27 roster |
| guimaraes | 3 | 21 | - | - | - | frozen 09-27 roster |
| caserta | 0 | 21 | - | - | - | frozen 09-27 roster |
| heidelberg | 0 | 21 | - | - | - | frozen 09-27 roster |
| tilburg | 0 | 21 | - | - | - | frozen 09-27 roster |
| zwolle | 0 | 21 | - | - | - | frozen 09-27 roster |
| catania | 1 | 20 | - | - | - | frozen 09-27 roster |
| belgrade | 0 | 20 | - | - | - | frozen 09-27 roster |
| chadds-ford | 0 | 20 | - | - | - | frozen 09-27 roster |
| menorca | 0 | 20 | - | - | - | frozen 09-27 roster |
| miyazaki | 0 | 20 | - | - | - | frozen 09-27 roster |
| sources | 1 | 19 | - | - | - | frozen 09-27 roster |
| bordeaux | 0 | 19 | - | - | - | frozen 09-27 roster |
| hawaii | 0 | 19 | - | - | - | frozen 09-27 roster |
| yakushima | 0 | 19 | - | - | - | frozen 09-27 roster |
| wessobrunn | 2 | 18 | - | - | - | frozen 09-27 roster |
| genoa | 2 | 18 | - | - | - | frozen 09-27 roster |
| nuremberg | 1 | 18 | - | - | - | frozen 09-27 roster |
| gojaus-miskas | 0 | 18 | - | - | - | frozen 09-27 roster |
| llangernyw | 0 | 18 | - | - | - | frozen 09-27 roster |
| oxford | 0 | 18 | - | - | - | frozen 09-27 roster |
| taiwan | 0 | 18 | - | - | - | frozen 09-27 roster |
| toulouse | 2 | 17 | - | - | - | frozen 09-27 roster |
| aarhus | 1 | 17 | - | - | - | frozen 09-27 roster |
| freiburg | 1 | 17 | - | - | - | frozen 09-27 roster |
| padua | 1 | 17 | - | - | - | frozen 09-27 roster |
| bergamo | 0 | 17 | - | - | - | frozen 09-27 roster |
| salzburg | 0 | 17 | - | - | - | frozen 09-27 roster |
| ghent | 1 | 16 | - | - | - | frozen 09-27 roster |
| hallstatt | 1 | 16 | - | - | - | frozen 09-27 roster |
| perouges | 1 | 16 | - | - | - | frozen 09-27 roster |
| biei | 0 | 16 | - | - | - | frozen 09-27 roster |
| macugnaga | 0 | 16 | - | - | - | frozen 09-27 roster |
| salamanca | 0 | 16 | - | - | - | frozen 09-27 roster |
| york | 0 | 16 | - | - | - | frozen 09-27 roster |
| nagoya | 1 | 15 | - | - | - | frozen 09-27 roster |
| timber-creek | 0 | 15 | - | - | - | frozen 09-27 roster |
| tolpuddle | 0 | 15 | - | - | - | frozen 09-27 roster |
| gornja-stubica | 1 | 14 | - | - | - | frozen 09-27 roster |
| stuttgart | 2 | 14 | - | - | - | frozen 09-27 roster |
| bratislava | 0 | 14 | - | - | - | frozen 09-27 roster |
| heinkenszand | 0 | 14 | - | - | - | frozen 09-27 roster |
| helmond | 0 | 14 | - | - | - | frozen 09-27 roster |
| oss | 0 | 14 | - | - | - | frozen 09-27 roster |
| otama | 0 | 14 | - | - | - | frozen 09-27 roster |
| rio-de-janeiro | 0 | 14 | - | - | - | frozen 09-27 roster |
| sulechow | 0 | 14 | - | - | - | frozen 09-27 roster |
| gdansk | 2 | 13 | - | - | - | frozen 09-27 roster |
| alkmaar | 0 | 13 | - | - | - | frozen 09-27 roster |
| den-bosch | 0 | 13 | - | - | - | frozen 09-27 roster |
| derby | 0 | 13 | - | - | - | frozen 09-27 roster |
| graz | 0 | 13 | - | - | - | frozen 09-27 roster |
| hoorn | 0 | 13 | - | - | - | frozen 09-27 roster |
| lausanne | 0 | 13 | - | - | - | frozen 09-27 roster |
| lucca | 0 | 13 | - | - | - | frozen 09-27 roster |
| nantes | 0 | 13 | - | - | - | frozen 09-27 roster |
| simsbury | 0 | 13 | - | - | - | frozen 09-27 roster |
| bilbao | 2 | 12 | - | - | - | frozen 09-27 roster |
| ronda | 1 | 12 | - | - | - | frozen 09-27 roster |
| belfast | 0 | 12 | - | - | - | frozen 09-27 roster |
| buenos-aires | 0 | 12 | - | - | - | frozen 09-27 roster |
| como | 0 | 12 | - | - | - | frozen 09-27 roster |
| deventer | 0 | 12 | - | - | - | frozen 09-27 roster |
| ekero | 0 | 12 | - | - | - | frozen 09-27 roster |
| hamburg | 0 | 12 | - | - | - | frozen 09-27 roster |
| tarragona | 1 | 11 | - | - | - | frozen 09-27 roster |
| trieste | 1 | 11 | - | - | - | frozen 09-27 roster |
| apeldoorn | 0 | 11 | - | - | - | frozen 09-27 roster |
| brno | 0 | 11 | - | - | - | frozen 09-27 roster |
| bruges | 0 | 11 | - | - | - | frozen 09-27 roster |
| canada | 0 | 11 | - | - | - | frozen 09-27 roster |
| delft | 0 | 11 | - | - | - | frozen 09-27 roster |
| dresden | 0 | 11 | - | - | - | frozen 09-27 roster |
| gottingen | 0 | 11 | - | - | - | frozen 09-27 roster |
| perugia | 0 | 11 | - | - | - | frozen 09-27 roster |
| riga | 0 | 11 | - | - | - | frozen 09-27 roster |
| senonches | 0 | 11 | - | - | - | frozen 09-27 roster |
| venon | 0 | 11 | - | - | - | frozen 09-27 roster |
| kauai | 1 | 10 | - | - | - | frozen 09-27 roster |
| regensburg | 1 | 10 | - | - | - | frozen 09-27 roster |
| tulsa | 1 | 10 | - | - | - | frozen 09-27 roster |
| assen | 0 | 10 | - | - | - | frozen 09-27 roster |
| cremines | 0 | 10 | - | - | - | frozen 09-27 roster |
| emmen | 0 | 10 | - | - | - | frozen 09-27 roster |
| matera | 0 | 10 | - | - | - | frozen 09-27 roster |
| nagano | 0 | 10 | - | - | - | frozen 09-27 roster |
| oklahoma-city | 0 | 10 | - | - | - | frozen 09-27 roster |
| ueda | 0 | 10 | - | - | - | frozen 09-27 roster |
| venlo | 0 | 10 | - | - | - | frozen 09-27 roster |
| viroflay | 0 | 10 | - | - | - | frozen 09-27 roster |

**What converts, and what does not** (scripts/seolearn.py)

```
SEO learning pass: 1 pages over 40 impressions, 1 of them clean
Index 1.00 means a page converts exactly as its position normally does.

SHARE OF TREES CARRYING A PHOTOGRAPH
   40% and over           n1   i325   c0    ctr  0.0%  index 0.00

SHARE WITH A CONFIRMED PIN
   40% and over           n1   i325   c0    ctr  0.0%  index 0.00

SHARE WITH A RECOGNITION LINE
   40% and over           n1   i325   c0    ctr  0.0%  index 0.00

SHARE WITH A RECORDED AGE
   40% and over           n1   i325   c0    ctr  0.0%  index 0.00

SHARE WITH A SEASONAL PEAK
   40% and over           n1   i325   c0    ctr  0.0%  index 0.00

TREES ON THE PAGE
   over 25                n1   i325   c0    ctr  0.0%  index 0.00

AVERAGE STORY LENGTH
   170 and over           n1   i325   c0    ctr  0.0%  index 0.00

EARNED AND WASTED, worst first (real queries, converting under half)
These have the demand already. Fixing one is worth more than a new page.
   prague           i325   c0   p5.6   index 0.00  loses ~19 clicks/10d  -
```

**Copy test**

```
Copy test: city-title-age-first (day 32 of 56, review 2026-11-05)
The age is the hook and the count is inventory, so naming the oldest tree before the number earns more clicks.

  control      n1    before 1.38  now 0.00  change -1.38

  TOO EARLY. At about 2 clicks per page per ten days this needs the full window; a lead now is noise wearing a result's clothes.
```

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| before 2026-09-23 | The Twisted Muku of Omiya Gate, Kyoto  | Kyoto | - | publish | - |
| 2026-10-12 | The Lagunària de la Llotja | Palma de Mallorca | - | open | - |
| 2026-10-06 | A tree in Tokyo | - | - | open | - |
| 2026-10-06 | A tree in Tokyo | - | - | open | - |
| 2026-10-06 | Ginkgo in Tokyo | - | - | open | - |
| 2026-10-06 | A tree in Tokyo | - | - | open | - |
| 2026-10-06 | A tree in Tokyo | - | - | open | - |
| 2026-10-05 | The Southern Mahogany of Edinburgh Gar | Melbourne | - | publish | - |
| 2026-10-05 | The Finer Holm Oak of Edinburgh Garden | Melbourne | - | hold | - |
| 2026-10-05 | London Plane in Paris | - | 88% girth | open | - |
| 2026-10-04 | Ginkgo in Tokyo | - | - | lead | - |
| 2026-10-04 | Pedunculate Oak | - | 112% girth | lead | - |
| 2026-10-03 | The Whitebeam of Víkurgarður | Reykjavik | - | publish | - |
| 2026-10-03 | The Larch of Hólavallagarður | Reykjavik | - | publish | - |
| 2026-10-03 | The City Hall Maple | Reykjavik | - | publish | zet de andere foto's van onze Reykjavik gebruiker ook maar online, ik vertrouw hem meer dan jou; ook zijn semi slechte foto's zijn beter dan geen |

7 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**The language test** (Contract J v1.13: a translated set should pass its English twin's impressions within four weeks of indexing):

| Lang | City | Clicks | Impressions | Position | English twin |
|---|---|---:|---:|---:|---:|
| es | tenerife | 0 | 17 | 44.6 | 8 |
| es | barcelona | 0 | 13 | 31.0 | 3 |
| ja | fukuoka | 0 | 10 | 28.0 | 1 |
| de | vienna | 0 | 9 | 25.6 | 1 |
| de | graz | 0 | 7 | 45.1 | 0 |
| fr | lyon | 0 | 7 | 68.9 | 1 |
| es | madrid | 0 | 6 | 53.8 | 1 |
| it | rome | 1 | 5 | 26.2 | 1 |
| de | hamburg | 0 | 5 | 25.0 | 0 |
| es | cadiz | 0 | 5 | 45.6 | 0 |
| pt | rio-de-janeiro | 0 | 5 | 10.2 | 0 |
| fr | paris | 0 | 4 | 19.8 | 4 |
| nl | amsterdam | 0 | 3 | 51.3 | 2 |
| nl | arnhem | 0 | 3 | 83.3 | 1 |
| de | berlin | 1 | 2 | 1.0 | 2 |
| es | seville | 1 | 2 | 19.0 | 5 |
| de | munich | 0 | 2 | 11.0 | 7 |
| de | zurich | 0 | 2 | 19.5 | 0 |
| es | malaga | 0 | 2 | 18.5 | 0 |
| es | palma-de-mallorca | 0 | 2 | 75.5 | 1 |
| it | palermo | 0 | 2 | 41.5 | 0 |
| it | sardinia | 0 | 2 | 46.0 | 0 |
| ja | kyoto | 0 | 2 | 1.0 | 2 |
| pt | lisbon | 1 | 1 | 2.0 | 2 |
| de | regensburg | 0 | 1 | 52.0 | 0 |
| es | alicante | 0 | 1 | 86.0 | 3 |
| fr | bordeaux | 0 | 1 | 28.0 | 0 |
| fr | nantes | 0 | 1 | 27.0 | 0 |
| it | cagliari | 0 | 1 | 62.0 | 1 |
| ja | kagoshima | 0 | 1 | 83.0 | 1 |
| ja | kanazawa | 0 | 1 | 89.0 | 2 |
| ja | tokyo | 0 | 1 | 5.0 | 2 |
| pt | porto | 0 | 1 | 6.0 | 5 |

**Cities seen but never clicked** (60+ impressions, zero clicks, with what they are actually shown for):

- prague (i141): prague (i15, p9); prague (i15, p8); prague (i15, p7); prague (i15, p5)
- Seen, not clicked: /sequoia-national-park/general-sherman-tree (c0/i21, 0.0%) for general sherman tree california (i5, p74); sequoia tree general sherman (i2, p71); big sherman tree (i2, p69)

**Climbing** (this ten days against the ten before it)

| Page | Impressions | Change | Position | Moved | Clicks |
|---|---:|---:|---:|---:|---:|
| /prague/oak-of-cisarsky-ostrov | 34 | +33 | 3.7 | -1.7 | +0 |
| /prague/oak-of-dienzenhofer-gardens | 34 | +33 | 4.9 | -0.9 | +0 |
| /prague/ash-of-strahov-garden | 34 | +29 | 7.7 | -1.7 | +0 |
| /prague/twin-beech-of-hvezda | 34 | +29 | 8.6 | -2.2 | +0 |
| /prague/walks | 34 | +28 | 3.4 | -0.9 | +0 |
| /prague/oak-of-u-malvazinky | 34 | +20 | 6.3 | +0.2 | +0 |
| /prague/oldest-tree | 34 | +18 | 4.0 | -0.4 | -2 |
| /prague/field-maple-of-the-seminary-garden | 18 | +9 | 9.3 | -2.6 | +0 |

**Slipping**

| Page | Impressions | Change | Position | Moved |
|---|---:|---:|---:|---:|
| /sequoia-national-park/general-sherman-tree | 21 | -10 | 74.5 | -25.8 |

- New queries this window: alte bäume (i4).

**Who they are** (full cut, Mondays)
Audience, 28 days of search (727 clicks, 30963 impressions):
- Countries: usa c106/i7651; nld c67/i1612; esp c63/i2433; gbr c62/i2375; deu c50/i1589
- Devices: MOBILE c523/i18270; DESKTOP c194/i12331; TABLET c10/i362
- Landing pages: / c23/i273; /prague c11/i298; /bath/plane-trees-of-the-circus c8/i143; /de/vienna/chestnut-avenue-of-the-hauptallee c7/i217; /leuven c7/i48
- Search language (top 100 named queries, crude match, most clicks are in queries Google withholds): English 56q c15/i432; unclassified 39q c21/i195; Italian 4q c0/i5; Dutch 1q c1/i4
On the site since 2026-09-14 (6370 visits, 8010 pageviews, 1.3 pages per visit):
- Countries: US 1320; SG 1040; DE 570; BR 420; GB 320
- Devices: desktop 5610; mobile 2370; tablet 30
- Browsers: Chrome 3040; Firefox 1310; ChromeMobile 1160; Edge 1010
- Arrived via: (direct) 5210; ancienttrees.app 1640; www.google.com 800; duckduckgo.com 90; www.facebook.com 60
- Opened: /open 860; /contribute 230; / 230; /explore 70; /countries 70; /barcelona 60; /amsterdam 60; /florence 60

Web Analytics (beacon, cookieless), people only.
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews | From Google |
|---|---:|---:|---:|
| 10-04 | 0 | 10 | 0 |
| 10-05 | 30 | 80 | 10 |
| 10-06 | 90 | 160 | 0 |
| 10-07 | 70 | 150 | 0 |
| 10-08 | 10 | 90 | 0 |
| 10-09 | 60 | 150 | 0 |
| 10-10 | 40 | 140 | 10 |
| 10-11 | 30 | 90 | 0 |
| **window** | **330** | **870** | **20** |
- Top paths: / (60); /verona (20); /rothenburg-ob-der-tauber/vorbachtal-spruces (20); /perth (20); /melbourne/hoop-pine-of-yarra-boulevard (20); /app (20); /seville (20); /explore (20); /leuven (20); /washington-dc/washington-monument-witness-mulberry (10); /portalegre/plane-tree-of-rossio (10); /reykjavik/larch-of-holavallagardur (10)
- Referrers: (direct) (160); ancienttrees.app (540); www.facebook.com (50); duckduckgo.com (40); search.yahoo.com (30); bing.com (10); www.google.com (10); de.search.yahoo.com (10); www.bing.com (10); com.google.android.gm (10)
- Moved between our own pages: 540 of 870 pageviews (62%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: US (200); BE (80); NL (70); PT (70); FR (70)
- Devices: mobile (600); desktop (270)
- Page load (8d): p50 2261ms, p90 8692ms

Links: external referrers (a link somebody actually clicked): www.facebook.com (50); search.yahoo.com (30); de.search.yahoo.com (10)
AI: arrivals from an assistant that cited us: none yet

Backlinks (watched pages):
| Site | Links to | rel | First seen |
|---|---|---|---|
| getlisbon.com | /lisbon | followed | 2026-09-08 |
| getlisbon.com | /pt/lisbon | followed | 2026-09-08 |
| www.baumkunde.de | /copenhagen | followed | 2026-09-26 |
| www.baumkunde.de | /rogalin/russ-oak | followed | 2026-09-26 |
4 linking page(s), 4 followed. Checked by fetching the page: a link with rel="noreferrer" never appears in the referrer table, so these two lines measure different things and neither replaces the other. Unknown links stay a manual read of Search Console's Links report. This run read 12 of 12 fetched (0 unreachable), out of 27 watched pages.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-11T16:06 | 0.0 | 0 | 1 | 0 | - |
| 10-11T21:22 | 0.0 | 0 | 0 | 0 | - |
| 10-12T00:54 | 0.0 | 0 | 1 | 0 | - |
| 10-12T08:26 | 0.0 | 0 | 0 | 0 | - |
| **4 runs** | **0** | **0** | **2** | | |

- 4 of 4 produced no trees; 4 wrote nothing to LOG.md; last build that went live: 1h ago.

**What they made**

- Photographs readers sent, queued for a look; vouched ones live
- Photographs readers sent, queued for a look; vouched ones live

Machine: 5 chain attempts yesterday, 1 got real work time (~91 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 1 clicks and 31 impressions on Google's freshest day (day before: c0/i35). Directional at best; no strategic conclusions from these volumes.

## 2026-10-10 (previous UTC day)

**Today: an android waitlist signup arrived yesterday (21 total); an account was opened yesterday (25 total).**

**What readers gave us, and what the night run approved, and it went live**

| Day | Tree | Where | What |
|---|---|---|---|
| 10-09 | The City Hall Maple | Reykjavik | a reader's photograph, published |

**Did the product happen**

| Action | Yesterday | 14 days | Ever | Last |
|---|---:|---:|---:|---|
| signin-open | 3 | 167 | 498 | yesterday |
| app-cta | 3 | 19 | 57 | yesterday |
| directions | 0 | 6 | 46 | 2 days ago |
| signin-oauth | 0 | 6 | 41 | 2 days ago |
| signin-done | 0 | 2 | 39 | 4 days ago |
| search-home | 0 | 20 | 29 | 2 days ago |
| app-open | 2 | 14 | 19 | yesterday |
| suggestion-submit | 0 | 0 | 17 | 16 days ago |
| home-country | 1 | 6 | 9 | yesterday |
| home-fav | 0 | 5 | 9 | 2 days ago |
| signin-link-sent | 0 | 0 | 6 | 16 days ago |
| waitlist-submit | 1 | 1 | 5 | yesterday |
| save | 0 | 1 | 5 | 9 days ago |
| home-dir-tree | 0 | 0 | 3 | 18 days ago |
| search-explore | 0 | 1 | 3 | 9 days ago |
| visit | 0 | 0 | 3 | 21 days ago |
| walks-app | 0 | 0 | 3 | 18 days ago |
| app-page-badge | 0 | 2 | 2 | 2 days ago |
| home-species | 0 | 0 | 2 | 20 days ago |
| sponsor-open | 0 | 0 | 1 | 21 days ago |
| worthit-report | 0 | 0 | 1 | 17 days ago |
| worthit-report detail | 0 | 0 | 1 | 17 days ago |
| worthit-worth it | 0 | 0 | 1 | 21 days ago |
| worthit-not worth it | 0 | 0 | 0 | never |
| **all** | **10** | **250** | **800** | |
- 'Ever' counts every row in the events table, which begins 2026-08-01 when the funnel was repaired. Anything named here with a zero has never fired at all.

**What people typed into our search** (14 days, 18 searches, 15 different terms)

| Typed | Times |
|---|---:|
| lisboa | 3 |
| bruss | 2 |
| brussel | 1 |
| cop | 1 |
| granada | 1 |
| guimaraes | 1 |
| lis | 1 |
| lisb | 1 |
| lisbon | 1 |
| mu | 1 |
| munich | 1 |
| oslo | 1 |
| phila | 1 |
| portland | 1 |
| tokyo | 1 |

| Day | Accounts | Android waitlist | Saves | Trees sent | Feedback | Ambassador asks |
|---|---:|---:|---:|---:|---:|---:|
| 09-27 | 0 | 0 | 0 | 0 | 0 | 0 |
| 09-28 | 0 | 0 | 0 | 0 | 0 | 0 |
| 09-29 | 0 | 0 | 0 | 0 | 0 | 0 |
| 09-30 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-01 | 3 | 0 | 0 | 0 | 3 | 0 |
| 10-02 | 0 | 0 | 1 | 0 | 0 | 0 |
| 10-03 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-04 | 0 | 0 | 0 | 1 | 0 | 0 |
| 10-05 | 2 | 0 | 0 | 1 | 0 | 0 |
| 10-06 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-07 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-08 | 1 | 0 | 0 | 0 | 1 | 0 |
| 10-09 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10-10 | 1 | 1 | 0 | 0 | 0 | 0 |
| 10-11 | 0 | 0 | 0 | 0 | 0 | 0 |
| **14 days** | **7** | **1** | **1** | **2** | **4** | **0** |
- Our own rows are not in this table: 59 trees, 56 feedback, 3 accounts. They are testing, and counting them reads as traction.

| Ambassadors | Yesterday | 14 days | Total |
|---|---:|---:|---:|
| Granted | 1 | 6 | 6 |
| Invitations sent (app contributors) | 0 | 6 | 6 |
| Open-seat requests answered | 0 | 0 | 0 |
- New in 14 days: Copenhagen since 2026-10-02, Giulia Torta (Florence) since 2026-10-03, Hugo Veríssimo (Lisbon) since 2026-10-05, Aleš Rudl (Prague) since 2026-10-05, Daniel Daggfeldt (Stockholm) since 2026-10-05, Kerry Pickett (Brighton) since 2026-10-10.
- Android waitlist: 21 total, newest yesterday
- Submissions: 33 total (19 trees sent, 14 feedback), newest 3 days ago
- Accounts:    25 total, newest yesterday

**What readers told us** (14 days, structure only; the words stay in the database)

| Day | Tree | What | Note | From | Outcome |
|---|---|---|---|---|---|
| 09-28 | 50BAB485-DCC6-479F-A4FA-F45756D855 | tree sent in | - | us | - |
| 09-28 | 70E18AB5-CC32-492E-B2A4-A816E85458 | tree sent in | - | us | - |
| 09-29 | 8BFEB681-540D-4B78-8DF5-06A95191AD | tree sent in | - | us | - |
| 09-29 | B9A2D2DF-77BA-4240-8C90-63CA0A83B1 | tree sent in | - | us | - |
| 09-29 | A54BCE9E-B822-4E4D-A14D-2097523C4D | tree sent in | 62 chars, read it in the database | us | - |
| 09-29 | 0EE5B139-7042-4BCB-A109-4E8B8D0511 | tree sent in | 62 chars, read it in the database | us | - |
| 10-01 | 74066D89-9958-4D93-BFDC-1C78ED97EE | tree sent in | - | us | - |
| 10-01 | E36A052C-3A48-4EED-BA48-5AB48574FA | tree sent in | - | us | - |
| 10-01 | lis_030 (The Dragon Tree of Quinta | worth it | - | 08aa | holds |
| 10-01 | par_031 (The Horse Chestnut of Squ | worth it | - | cfe8 | holds |
| 10-01 | par_033 (The Turkey Oak of Square  | worth it | - | cfe8 | holds |
| 10-02 | par_031 (The Horse Chestnut of Squ | worth it | - | us | - |
| 10-02 | lis_030 (The Dragon Tree of Quinta | worth it | - | us | - |
| 10-02 | 59E829E3-784F-4302-A98E-2C40D1BE88 | tree sent in | - | us | - |
| 10-04 | 6151F7E2-9211-4C2B-8CE8-E1BF17DAA3 | tree sent in | - | us | - |
| 10-04 | 8F4E7266-CC24-46B3-9A6D-5E8A94BBA1 | tree sent in | - | cfe8 | open_question |
| 10-05 | Reykjavik | ambassador request | - | us | - |
| 10-05 | rey_001 (The Whitebeam of Víkurgar | worth it | - | us | - |
| 10-05 | Barcelona | ambassador request | - | us | - |
| 10-05 | D9C08351-03D1-4B51-A6EC-972F08D308 | tree sent in | 648 chars, read it in the database | cfe8 | - |
| 10-06 | Tokyo | ambassador request | - | us | - |
| 10-06 | 7C8BEC8F-B77B-415C-B4EC-A1589130C4 | tree sent in | - | us | - |
| 10-06 | A4FA2700-1D89-4BF7-8F6E-0EAFA60DC4 | tree sent in | - | us | - |
| 10-06 | AE06E952-7DE0-46AB-AADA-AF2BE3D5C8 | tree sent in | - | us | - |
| 10-06 | D0D4EE1D-A0C3-4C4F-966F-EE01F7ECB5 | tree sent in | - | us | - |
| 10-06 | 038AB20E-98E0-4335-B154-08263B4949 | tree sent in | - | us | - |
| 10-06 | Verona | ambassador request | - | us | - |
| 10-07 | Rome | ambassador request | - | us | - |
| 10-08 | The Judas Tree of the Real Alcázar | correction sent in | 92 chars, read it in the database | eed7 | open_question |
| 10-09 | Amsterdam | ambassador request | - | us | - |
| 10-09 | Paris | ambassador request | - | us | - |
| 10-09 | Berlin | ambassador request | - | us | - |
| 10-10 | Baarn | ambassador request | - | us | - |
| 10-11 | - | Test | - | us | - |
| 10-11 | brn_008 (The Town Hall Plane) | worth it | - | us | - |
| 10-11 | brn_008 (The Town Hall Plane) | worth it | - | us | - |

- 30 of these 36 rows are ours, marked us. The rest is the reader traffic.
- 4 of the other 6 came from one account (cfe8), which is one person rather than a pattern.

**The funnel, as rates**
- Seen to clicked: 3.1% (76 of 2460) vs 2.3% the fortnight before
- Pages per visit: 1.3 (6320 visits, 7940 pageviews since 2026-09-13)
- Visits that did something: 13.0% (821 actions on 6320 visits)

**What people did in the app**

| What | Yesterday | 14 days | Ever | Last |
|---|---:|---:|---:|---|
| app_open | 8 | 98 | 288 | today |
| tab | 4 | 109 | 310 | yesterday |
| tree_opened | 11 | 349 | 1226 | today |
| directions | 0 | 9 | 45 | 2 days ago |
| tree_saved | 0 | 3 | 19 | 10 days ago |
| tree_visited | 0 | 12 | 26 | 3 days ago |
| sighting_recorded | 0 | 23 | 72 | 6 days ago |
| sync_skipped | 0 | 0 | 0 | never |
| sync_failed | 0 | 0 | 0 | never |
| **all** | **23** | **603** | **1986** | |
- Measuring since 2026-08-30, when Measure.swift went in. Unlinked to any account by design: an install id, the app version and the OS, nothing else.
- Ours is not in this table: 22 install(s), 828 events, the testing before the app went live on 2026-09-03 and every install built by Xcode since (the app says how it was built with each event). An App Store copy on our own phone is the one kind this cannot see.
- 79 installs have ever sent anything. An install id is made fresh on each install, so this is an upper bound on people, not a count of them.
- Yesterday came from 6 installs, and the busiest made 9 of 6 events (150%). One install making most of a day is what our own reinstall looks like: add its id to excluded_installs in data/app-measure.json if it is ours.
- Tabs opened (14d): Discover 45; My trees 36; Map 28
- Active phones: 4 in the last day, 23 in the last 7 days, 59 in the last 30 days.
- Coming back: 27 of those 59 phones opened the app on more than one day (46%).
- Trees opened by the most phones (14d): The Yew of Campo Santana (Lisbon) 2; The Dragon Tree of Quinta Conde dos Arcos (Lisbon) 2; The Ginkgo of Kushida Shrine (Fukuoka) 2; The Married Ginkgos of Kushida (Fukuoka) 2; The Arenbergpark Plane (Leuven) 2
- Where the phones are (30d): United States 13; United Kingdom 10; The Netherlands 5; Italy 4; Portugal 4; Switzerland 3
- Trees recorded (14d): a tree we map 17; a tree we do not 6
  A sighting reaches our database only through an account. Signed out it stays on the phone, so this count can run ahead of the trees and photographs we actually receive.

**Trees collected in the app** (14 days, a person standing at the tree)

| Day | Tree | Where | Install | Build | Signed in |
|---|---|---|---|---|---|
| 10-08 | The Stone Pine of the Jardines de Cristina | Seville | 92A2 | ? | ? |
| 10-08 | The Stone Pine of the Jardines de Cristina | Seville | 92A2 | ? | ? |
| 10-08 | The Stone Pine of the Jardines de Cristina | Seville | 92A2 | ? | ? |
| 10-05 | The Finer Holm Oak of Edinburgh Gardens | Melbourne | 2D66 | ? | ? |
| 10-05 | The Southern Mahogany of Edinburgh Gardens | Melbourne | 2D66 | ? | ? |
| 10-03 | The Larch of Hólavallagarður | Reykjavik | 5781 | ? | ? |
| 10-03 | The City Hall Maple | Reykjavik | 5781 | ? | ? |
| 10-03 | The Whitebeam of Víkurgarður | Reykjavik | 5781 | ? | ? |
| 10-01 | The Turkey Oak of Square Rene-Le Gall | Paris | 0E84 | ? | ? |
| 10-01 | The Turkey Oak of Square Rene-Le Gall | Paris | 0E84 | ? | ? |
| 10-01 | The Horse Chestnut of Square Rene-Le Gall | Paris | 0E84 | ? | ? |
| 10-01 | The Dragon Tree of Quinta Conde dos Arcos | Lisbon | B792 | ? | ? |

**The app as a builder reads it** (this week against the week before; the weakest row is the work)

| Link | This week | Week before |
|---|---|---|
| New phones | 11 | 8 |
| First day: opened a tree | 7 of 11 (64%) | 6 of 8 (75%) |
| First day: opened a tree near them | - | - |
| First day: allowed location | - | - |
| First day: Take me there | 1 of 11 (9%) | 3 of 8 (38%) |
| First day: collected a tree | 1 of 11 (9%) | 3 of 8 (38%) |
| Back within a week | 4 of 8 (50%) | 10 of 16 (62%) |
| Trees collected (all phones) | 7 | 11 |
- Near and location count only phones on a version that sends them (from 2026-10-10); a dash means none yet.
- Back within a week looks at the phones that arrived a week earlier, so each has had its seven days.

**App Store downloads** (Apple's own count, not PostHog)

| Day | Downloads |
|---|---:|
| 2026-09-25 | 6 |
| 2026-09-27 | 2 |
| 2026-09-30 | 1 |
| 2026-10-01 | 2 |
| 2026-10-02 | 1 |
| 2026-10-03 | 1 |
| 2026-10-05 | 1 |
| 2026-10-08 | 4 |
| 2026-10-09 | 4 |
| **9 days** | **22** |
- First-time downloads only, which is what App Store Connect's Trends screen counts; redownloads and updates are not in this table.

**Where the downloads came from** (14 days, Apple's attribution)

| Came from | Via | Downloads |
|---|---|---:|
| Web referrer | - | 8 |
| App Store search | - | 7 |
| App referrer | - | 5 |
| App Store browse | - | 2 |
| **window** | | **22** |
- Countries: US (6); GB (5); IT (2); BE (1); ES (1); FR (1)
- Apple's own source split, first-time downloads only. "Web referrer" with our own domain is the site's app page; "App Store search" is somebody who typed into the store. "Unavailable" is Apple's word for a source it could not attribute.

**Where demand is going to waste**

Search Console, the last 10 days Google will give us (its data lags 2-3 days, so the newest row is never yesterday). The newest row is also still FILLING: Google backfills for days and backfills impressions harder than clicks, so it reads as an unusually good day and is not one (08-22 arrived as 12/769 and settled at 17/1030). Position is an average across every query, so it dips whenever we start ranking for something new:

| Day | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| 10-01 | 1 | 53 | 1.9% | 31.7 |
| 10-02 | 2 | 63 | 3.2% | 39.1 |
| 10-03 | 2 | 72 | 2.8% | 32.0 |
| 10-04 | 1 | 50 | 2.0% | 28.8 |
| 10-05 | 4 | 47 | 8.5% | 39.0 |
| 10-06 | 1 | 45 | 2.2% | 34.5 |
| 10-07 | 0 | 47 | 0.0% | 34.7 |
| 10-08 *partial* | 5 | 35 | 14.3% | 21.8 |
| **window** | **16** | **412** | **3.9%** | |
- Top queries (10d): pokaz na mapie (i1, p1); alte bäume (i4, p27); ancient douglas fir tree (i1, p48); ancient tree (i2, p70); angelystor (i1, p1)
- Top pages (10d): / (c4/i11); /brussels/oldest-tree (c3/i4); /amsterdam/oudemanhuispoort-elm (c1/i1); /assisi (c1/i1); /brisbane/white-rabbit-tree-of-newstead-park (c1/i1)
- Content leads, biggest first. A lead is a query no page TITLE covers, so some are ranking problems on a page we have rather than a page to write ('vegas trees' against /las-vegas). Check before building:
    - 'alte bäume' (i4, p27)
    - 'pokaz na mapie' (i1, p1)
    - 'angelystor' (i1, p1)
    - 'araucaria norfolk' (i1, p88)
    - 'arbol de las pagodas' (i1, p33)
    - 'arbol mas antiguo de españa' (i1, p99)
    - 'avenue de laune' (i1, p24)
    - 'bungeana' (i1, p66)
**What Bing shows and sends** (last 7 days with data, Bing Webmaster Tools)

| Day | Impressions | Clicks | CTR | Pages crawled | Pages in index |
|---|---:|---:|---:|---:|---:|
| 10-03 | 47 | 4 | 8.5% | 86 | 2041 |
| 10-04 | 40 | 2 | 5.0% | 88 | 2106 |
| 10-05 | 79 | 5 | 6.3% | 207 | 2106 |
| 10-06 | 65 | 2 | 3.1% | - | - |
| 10-07 | 81 | 2 | 2.5% | - | - |
| 10-08 | 168 | 4 | 2.4% | - | - |
| 10-09 | 47 | 2 | 4.3% | - | - |
| **7 days** | **527** | **21** | **4.0%** | **381** | **2106** |
- Week before: 0 impressions, 0 clicks; in index then: 1908. No Bing demotion in sight.
- Top Bing queries: trees in the plaza dus burgos seville (c1/i3, p5); ancient trees in wiesbaden germany (c1/i2, p6); oldest live oak trees in new orleans (c1/i2, p6); husalle lindens copenhagen (c1/i2, p3); french trees found in paris (c1/i2, p6); remarkable trees copenhagen (c1/i2, p4); berlin tree (c1/i2, p1); oldest tree in belfast (c1/i2, p1)
- Bing alone, from Bing Webmaster Tools; the in-index column is the last day's count. DuckDuckGo and Yahoo draw on the same index and are not in these numbers. Bing's data lags about two days.

**Google, from the new floor** (2026-10-01: ~50 impressions a day, 0 clicks; before 09-28: ~2,000 a day)

What Google does, last 10 days:

| Measure | Now |
|---|---:|
| Impressions | 709 |
| Clicks | 16 |
| Pages that got at least one impression | 245 |
| Impressions on the proven cities | 615 |

What we did (context, proves nothing by itself): 2892 trees Google may index, 796 kept out for lacking a photo and an exact pin, 4638 pages on the noindex list.

**Is enriching working** (indexed tree pages, last 10 days of Google; rich = register record, a measurement and concrete access)

| Indexed tree pages | Pages | With an impression | Impressions | Per page | Clicks |
|---|---:|---:|---:|---:|---:|
| Rich | 431 | 21 | 186 | 0.43 | 2 |
| Not yet rich | 561 | 22 | 48 | 0.09 | 0 |
| Returned to Google's index in the last 7 days | 0 | 0 | 0 | 0.00 | 0 |

- Google lags 2 to 3 days, so a page returned this week has had a few days at most. Compare the per-page numbers across weeks, not the totals across rows.

**Depth is allowed on these cities** (10+ impressions in the window; photos, pins and best_time go here and nowhere else):

| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |
|---|---:|---:|---:|---:|---:|---|
| prague | 0 | 307 | 0.0% | 5.5 | 6.0% | prague (i9, p1) |
| olympic-national-park | 0 | 17 | 0.0% | 15.1 | 1.2% | duncan cedar (i14, p6) |
| brussels | 3 | 13 | 23.1% | 10.8 | 2.2% | klint white mulberry (i2, p52) |
| singapore | 4 | 359 | - | - | - | frozen 09-27 roster |
| lisbon | 5 | 316 | - | - | - | frozen 09-27 roster |
| amsterdam | 7 | 284 | - | - | - | frozen 09-27 roster |
| barcelona | 3 | 284 | - | - | - | frozen 09-27 roster |
| seville | 7 | 259 | - | - | - | frozen 09-27 roster |
| bath | 9 | 255 | - | - | - | frozen 09-27 roster |
| tenerife | 3 | 241 | - | - | - | frozen 09-27 roster |
| berlin | 5 | 224 | - | - | - | frozen 09-27 roster |
| rome | 3 | 221 | - | - | - | frozen 09-27 roster |
| palermo | 2 | 216 | - | - | - | frozen 09-27 roster |
| oahu | 1 | 213 | - | - | - | frozen 09-27 roster |
| tokyo | 5 | 209 | - | - | - | frozen 09-27 roster |
| munich | 8 | 206 | - | - | - | frozen 09-27 roster |
| new-york | 3 | 188 | - | - | - | frozen 09-27 roster |
| edinburgh | 8 | 173 | - | - | - | frozen 09-27 roster |
| dublin | 6 | 168 | - | - | - | frozen 09-27 roster |
| brisbane | 6 | 163 | - | - | - | frozen 09-27 roster |
| paris | 2 | 163 | - | - | - | frozen 09-27 roster |
| malaga | 7 | 161 | - | - | - | frozen 09-27 roster |
| vienna | 4 | 161 | - | - | - | frozen 09-27 roster |
| south-korea | 0 | 152 | - | - | - | frozen 09-27 roster |
| london | 3 | 147 | - | - | - | frozen 09-27 roster |
| alicante | 1 | 146 | - | - | - | frozen 09-27 roster |
| athens | 4 | 130 | - | - | - | frozen 09-27 roster |
| cadiz | 5 | 125 | - | - | - | frozen 09-27 roster |
| pamplona | 1 | 125 | - | - | - | frozen 09-27 roster |
| porto | 1 | 124 | - | - | - | frozen 09-27 roster |
| cagliari | 3 | 116 | - | - | - | frozen 09-27 roster |
| glasgow | 2 | 110 | - | - | - | frozen 09-27 roster |
| ede | 0 | 100 | - | - | - | frozen 09-27 roster |
| hinode | 0 | 98 | - | - | - | frozen 09-27 roster |
| palma-de-mallorca | 2 | 95 | - | - | - | frozen 09-27 roster |
| los-angeles | 1 | 94 | - | - | - | frozen 09-27 roster |
| madrid | 0 | 93 | - | - | - | frozen 09-27 roster |
| arnhem | 1 | 92 | - | - | - | frozen 09-27 roster |
| milan | 1 | 92 | - | - | - | frozen 09-27 roster |
| krakow | 3 | 91 | - | - | - | frozen 09-27 roster |
| austin | 0 | 91 | - | - | - | frozen 09-27 roster |
| montreal | 9 | 90 | - | - | - | frozen 09-27 roster |
| houston | 4 | 90 | - | - | - | frozen 09-27 roster |
| sintra | 0 | 87 | - | - | - | frozen 09-27 roster |
| florence | 0 | 86 | - | - | - | frozen 09-27 roster |
| the-hague | 1 | 84 | - | - | - | frozen 09-27 roster |
| amerongen | 0 | 84 | - | - | - | frozen 09-27 roster |
| new-orleans | 1 | 83 | - | - | - | frozen 09-27 roster |
| switzerland | 0 | 83 | - | - | - | frozen 09-27 roster |
| reykjavik | 0 | 80 | - | - | - | frozen 09-27 roster |
| liverpool | 1 | 78 | - | - | - | frozen 09-27 roster |
| valencia | 3 | 77 | - | - | - | frozen 09-27 roster |
| guerneville | 0 | 76 | - | - | - | frozen 09-27 roster |
| copenhagen | 5 | 75 | - | - | - | frozen 09-27 roster |
| chicago | 2 | 72 | - | - | - | frozen 09-27 roster |
| nara | 2 | 72 | - | - | - | frozen 09-27 roster |
| warsaw | 1 | 72 | - | - | - | frozen 09-27 roster |
| istanbul | 4 | 70 | - | - | - | frozen 09-27 roster |
| rogalin | 1 | 70 | - | - | - | frozen 09-27 roster |
| cyprus | 2 | 69 | - | - | - | frozen 09-27 roster |
| nijmegen | 0 | 69 | - | - | - | frozen 09-27 roster |
| cork | 3 | 68 | - | - | - | frozen 09-27 roster |
| dallas | 1 | 68 | - | - | - | frozen 09-27 roster |
| venice | 1 | 68 | - | - | - | frozen 09-27 roster |
| hobart | 3 | 66 | - | - | - | frozen 09-27 roster |
| takeo | 0 | 65 | - | - | - | frozen 09-27 roster |
| fukuoka | 2 | 64 | - | - | - | frozen 09-27 roster |
| monterey | 2 | 64 | - | - | - | frozen 09-27 roster |
| netherlands | 2 | 63 | - | - | - | frozen 09-27 roster |
| ottawa | 2 | 63 | - | - | - | frozen 09-27 roster |
| portland | 2 | 63 | - | - | - | frozen 09-27 roster |
| sydney | 0 | 63 | - | - | - | frozen 09-27 roster |
| kanazawa | 2 | 60 | - | - | - | frozen 09-27 roster |
| sardinia | 0 | 60 | - | - | - | frozen 09-27 roster |
| greece | 2 | 58 | - | - | - | frozen 09-27 roster |
| vilnius | 0 | 57 | - | - | - | frozen 09-27 roster |
| coimbra | 1 | 56 | - | - | - | frozen 09-27 roster |
| borrowdale | 0 | 56 | - | - | - | frozen 09-27 roster |
| fulufjallet | 2 | 55 | - | - | - | frozen 09-27 roster |
| beijing | 1 | 55 | - | - | - | frozen 09-27 roster |
| madeira | 1 | 55 | - | - | - | frozen 09-27 roster |
| boston | 0 | 55 | - | - | - | frozen 09-27 roster |
| san-francisco | 0 | 55 | - | - | - | frozen 09-27 roster |
| seoul | 1 | 54 | - | - | - | frozen 09-27 roster |
| utrecht | 3 | 54 | - | - | - | frozen 09-27 roster |
| osaka | 1 | 53 | - | - | - | frozen 09-27 roster |
| crete | 4 | 52 | - | - | - | frozen 09-27 roster |
| hong-kong | 1 | 52 | - | - | - | frozen 09-27 roster |
| budapest | 1 | 51 | - | - | - | frozen 09-27 roster |
| kyoto | 1 | 51 | - | - | - | frozen 09-27 roster |
| leipzig | 1 | 51 | - | - | - | frozen 09-27 roster |
| granada | 2 | 50 | - | - | - | frozen 09-27 roster |
| logan-ohio | 1 | 50 | - | - | - | frozen 09-27 roster |
| seattle | 1 | 49 | - | - | - | frozen 09-27 roster |
| geneva | 3 | 48 | - | - | - | frozen 09-27 roster |
| ibiza | 2 | 47 | - | - | - | frozen 09-27 roster |
| melbourne | 3 | 47 | - | - | - | frozen 09-27 roster |
| toronto | 0 | 47 | - | - | - | frozen 09-27 roster |
| leuven | 7 | 46 | - | - | - | frozen 09-27 roster |
| haarlem | 1 | 46 | - | - | - | frozen 09-27 roster |
| stockholm | 2 | 45 | - | - | - | frozen 09-27 roster |
| zurich | 5 | 45 | - | - | - | frozen 09-27 roster |
| leeuwarden | 0 | 45 | - | - | - | frozen 09-27 roster |
| cambridge | 1 | 44 | - | - | - | frozen 09-27 roster |
| germany | 1 | 44 | - | - | - | frozen 09-27 roster |
| dubrovnik | 0 | 44 | - | - | - | frozen 09-27 roster |
| sweden | 0 | 44 | - | - | - | frozen 09-27 roster |
| naples | 1 | 43 | - | - | - | frozen 09-27 roster |
| washington-dc | 0 | 43 | - | - | - | frozen 09-27 roster |
| nice | 1 | 42 | - | - | - | frozen 09-27 roster |
| palo-alto | 0 | 42 | - | - | - | frozen 09-27 roster |
| strasbourg | 1 | 41 | - | - | - | frozen 09-27 roster |
| las-vegas | 0 | 41 | - | - | - | frozen 09-27 roster |
| amersfoort | 2 | 40 | - | - | - | frozen 09-27 roster |
| runnymede | 0 | 40 | - | - | - | frozen 09-27 roster |
| vancouver | 1 | 39 | - | - | - | frozen 09-27 roster |
| philadelphia | 0 | 38 | - | - | - | frozen 09-27 roster |
| kagoshima | 1 | 37 | - | - | - | frozen 09-27 roster |
| perth | 0 | 37 | - | - | - | frozen 09-27 roster |
| verona | 5 | 36 | - | - | - | frozen 09-27 roster |
| eindhoven | 3 | 36 | - | - | - | frozen 09-27 roster |
| mexico-city | 1 | 36 | - | - | - | frozen 09-27 roster |
| segovia | 1 | 36 | - | - | - | frozen 09-27 roster |
| sequoia-national-park | 0 | 35 | - | - | - | frozen 09-27 roster |
| sorrento | 0 | 35 | - | - | - | frozen 09-27 roster |
| tallinn | 3 | 34 | - | - | - | frozen 09-27 roster |
| helsinki | 1 | 34 | - | - | - | frozen 09-27 roster |
| oslo | 1 | 34 | - | - | - | frozen 09-27 roster |
| bristol | 0 | 33 | - | - | - | frozen 09-27 roster |
| glastonbury | 0 | 33 | - | - | - | frozen 09-27 roster |
| quebec-city | 1 | 32 | - | - | - | frozen 09-27 roster |
| girona | 0 | 32 | - | - | - | frozen 09-27 roster |
| bari | 1 | 31 | - | - | - | frozen 09-27 roster |
| leiden | 2 | 31 | - | - | - | frozen 09-27 roster |
| tricase | 1 | 31 | - | - | - | frozen 09-27 roster |
| bucaco | 0 | 31 | - | - | - | frozen 09-27 roster |
| craigends | 0 | 31 | - | - | - | frozen 09-27 roster |
| pittsburgh | 0 | 31 | - | - | - | frozen 09-27 roster |
| boise | 4 | 30 | - | - | - | frozen 09-27 roster |
| luxembourg-city | 0 | 30 | - | - | - | frozen 09-27 roster |
| spokane | 1 | 29 | - | - | - | frozen 09-27 roster |
| manchester | 1 | 28 | - | - | - | frozen 09-27 roster |
| taipei | 1 | 28 | - | - | - | frozen 09-27 roster |
| maastricht | 0 | 28 | - | - | - | frozen 09-27 roster |
| sapporo | 0 | 28 | - | - | - | frozen 09-27 roster |
| bangkok | 2 | 26 | - | - | - | frozen 09-27 roster |
| parma | 0 | 26 | - | - | - | frozen 09-27 roster |
| cologne | 0 | 25 | - | - | - | frozen 09-27 roster |
| laren-gelderland | 0 | 25 | - | - | - | frozen 09-27 roster |
| ljubljana | 0 | 25 | - | - | - | frozen 09-27 roster |
| groningen | 1 | 24 | - | - | - | frozen 09-27 roster |
| slovakia | 1 | 24 | - | - | - | frozen 09-27 roster |
| dordrecht | 2 | 23 | - | - | - | frozen 09-27 roster |
| lyon | 1 | 23 | - | - | - | frozen 09-27 roster |
| charleston | 0 | 23 | - | - | - | frozen 09-27 roster |
| frankfurt | 0 | 23 | - | - | - | frozen 09-27 roster |
| jaegerspris-nordskov | 0 | 23 | - | - | - | frozen 09-27 roster |
| naha | 0 | 23 | - | - | - | frozen 09-27 roster |
| schenklengsfeld | 2 | 22 | - | - | - | frozen 09-27 roster |
| cordoba | 2 | 22 | - | - | - | frozen 09-27 roster |
| otoyo | 1 | 22 | - | - | - | frozen 09-27 roster |
| bilu | 0 | 22 | - | - | - | frozen 09-27 roster |
| cardiff | 0 | 22 | - | - | - | frozen 09-27 roster |
| enschede | 0 | 22 | - | - | - | frozen 09-27 roster |
| higashi-hiroshima | 0 | 22 | - | - | - | frozen 09-27 roster |
| limmersdorf | 0 | 22 | - | - | - | frozen 09-27 roster |
| minneapolis | 0 | 22 | - | - | - | frozen 09-27 roster |
| savannah | 0 | 22 | - | - | - | frozen 09-27 roster |
| yabu | 0 | 22 | - | - | - | frozen 09-27 roster |
| bologna | 1 | 21 | - | - | - | frozen 09-27 roster |
| guimaraes | 3 | 21 | - | - | - | frozen 09-27 roster |
| caserta | 0 | 21 | - | - | - | frozen 09-27 roster |
| heidelberg | 0 | 21 | - | - | - | frozen 09-27 roster |
| tilburg | 0 | 21 | - | - | - | frozen 09-27 roster |
| zwolle | 0 | 21 | - | - | - | frozen 09-27 roster |
| catania | 1 | 20 | - | - | - | frozen 09-27 roster |
| belgrade | 0 | 20 | - | - | - | frozen 09-27 roster |
| chadds-ford | 0 | 20 | - | - | - | frozen 09-27 roster |
| menorca | 0 | 20 | - | - | - | frozen 09-27 roster |
| miyazaki | 0 | 20 | - | - | - | frozen 09-27 roster |
| sources | 1 | 19 | - | - | - | frozen 09-27 roster |
| bordeaux | 0 | 19 | - | - | - | frozen 09-27 roster |
| hawaii | 0 | 19 | - | - | - | frozen 09-27 roster |
| yakushima | 0 | 19 | - | - | - | frozen 09-27 roster |
| wessobrunn | 2 | 18 | - | - | - | frozen 09-27 roster |
| genoa | 2 | 18 | - | - | - | frozen 09-27 roster |
| nuremberg | 1 | 18 | - | - | - | frozen 09-27 roster |
| gojaus-miskas | 0 | 18 | - | - | - | frozen 09-27 roster |
| llangernyw | 0 | 18 | - | - | - | frozen 09-27 roster |
| oxford | 0 | 18 | - | - | - | frozen 09-27 roster |
| taiwan | 0 | 18 | - | - | - | frozen 09-27 roster |
| toulouse | 2 | 17 | - | - | - | frozen 09-27 roster |
| aarhus | 1 | 17 | - | - | - | frozen 09-27 roster |
| freiburg | 1 | 17 | - | - | - | frozen 09-27 roster |
| padua | 1 | 17 | - | - | - | frozen 09-27 roster |
| bergamo | 0 | 17 | - | - | - | frozen 09-27 roster |
| salzburg | 0 | 17 | - | - | - | frozen 09-27 roster |
| ghent | 1 | 16 | - | - | - | frozen 09-27 roster |
| hallstatt | 1 | 16 | - | - | - | frozen 09-27 roster |
| perouges | 1 | 16 | - | - | - | frozen 09-27 roster |
| biei | 0 | 16 | - | - | - | frozen 09-27 roster |
| macugnaga | 0 | 16 | - | - | - | frozen 09-27 roster |
| salamanca | 0 | 16 | - | - | - | frozen 09-27 roster |
| york | 0 | 16 | - | - | - | frozen 09-27 roster |
| nagoya | 1 | 15 | - | - | - | frozen 09-27 roster |
| timber-creek | 0 | 15 | - | - | - | frozen 09-27 roster |
| tolpuddle | 0 | 15 | - | - | - | frozen 09-27 roster |
| gornja-stubica | 1 | 14 | - | - | - | frozen 09-27 roster |
| stuttgart | 2 | 14 | - | - | - | frozen 09-27 roster |
| bratislava | 0 | 14 | - | - | - | frozen 09-27 roster |
| heinkenszand | 0 | 14 | - | - | - | frozen 09-27 roster |
| helmond | 0 | 14 | - | - | - | frozen 09-27 roster |
| oss | 0 | 14 | - | - | - | frozen 09-27 roster |
| otama | 0 | 14 | - | - | - | frozen 09-27 roster |
| rio-de-janeiro | 0 | 14 | - | - | - | frozen 09-27 roster |
| sulechow | 0 | 14 | - | - | - | frozen 09-27 roster |
| gdansk | 2 | 13 | - | - | - | frozen 09-27 roster |
| alkmaar | 0 | 13 | - | - | - | frozen 09-27 roster |
| den-bosch | 0 | 13 | - | - | - | frozen 09-27 roster |
| derby | 0 | 13 | - | - | - | frozen 09-27 roster |
| graz | 0 | 13 | - | - | - | frozen 09-27 roster |
| hoorn | 0 | 13 | - | - | - | frozen 09-27 roster |
| lausanne | 0 | 13 | - | - | - | frozen 09-27 roster |
| lucca | 0 | 13 | - | - | - | frozen 09-27 roster |
| nantes | 0 | 13 | - | - | - | frozen 09-27 roster |
| simsbury | 0 | 13 | - | - | - | frozen 09-27 roster |
| bilbao | 2 | 12 | - | - | - | frozen 09-27 roster |
| ronda | 1 | 12 | - | - | - | frozen 09-27 roster |
| belfast | 0 | 12 | - | - | - | frozen 09-27 roster |
| buenos-aires | 0 | 12 | - | - | - | frozen 09-27 roster |
| como | 0 | 12 | - | - | - | frozen 09-27 roster |
| deventer | 0 | 12 | - | - | - | frozen 09-27 roster |
| ekero | 0 | 12 | - | - | - | frozen 09-27 roster |
| hamburg | 0 | 12 | - | - | - | frozen 09-27 roster |
| tarragona | 1 | 11 | - | - | - | frozen 09-27 roster |
| trieste | 1 | 11 | - | - | - | frozen 09-27 roster |
| apeldoorn | 0 | 11 | - | - | - | frozen 09-27 roster |
| brno | 0 | 11 | - | - | - | frozen 09-27 roster |
| bruges | 0 | 11 | - | - | - | frozen 09-27 roster |
| canada | 0 | 11 | - | - | - | frozen 09-27 roster |
| delft | 0 | 11 | - | - | - | frozen 09-27 roster |
| dresden | 0 | 11 | - | - | - | frozen 09-27 roster |
| gottingen | 0 | 11 | - | - | - | frozen 09-27 roster |
| perugia | 0 | 11 | - | - | - | frozen 09-27 roster |
| riga | 0 | 11 | - | - | - | frozen 09-27 roster |
| senonches | 0 | 11 | - | - | - | frozen 09-27 roster |
| venon | 0 | 11 | - | - | - | frozen 09-27 roster |
| kauai | 1 | 10 | - | - | - | frozen 09-27 roster |
| regensburg | 1 | 10 | - | - | - | frozen 09-27 roster |
| tulsa | 1 | 10 | - | - | - | frozen 09-27 roster |
| assen | 0 | 10 | - | - | - | frozen 09-27 roster |
| cremines | 0 | 10 | - | - | - | frozen 09-27 roster |
| emmen | 0 | 10 | - | - | - | frozen 09-27 roster |
| matera | 0 | 10 | - | - | - | frozen 09-27 roster |
| nagano | 0 | 10 | - | - | - | frozen 09-27 roster |
| oklahoma-city | 0 | 10 | - | - | - | frozen 09-27 roster |
| ueda | 0 | 10 | - | - | - | frozen 09-27 roster |
| venlo | 0 | 10 | - | - | - | frozen 09-27 roster |
| viroflay | 0 | 10 | - | - | - | frozen 09-27 roster |

**What converts, and what does not** (scripts/seolearn.py)

```
SEO learning pass: 1 pages over 40 impressions, 1 of them clean
Index 1.00 means a page converts exactly as its position normally does.

SHARE OF TREES CARRYING A PHOTOGRAPH
   40% and over           n1   i307   c0    ctr  0.0%  index 0.00

SHARE WITH A CONFIRMED PIN
   40% and over           n1   i307   c0    ctr  0.0%  index 0.00

SHARE WITH A RECOGNITION LINE
   40% and over           n1   i307   c0    ctr  0.0%  index 0.00

SHARE WITH A RECORDED AGE
   40% and over           n1   i307   c0    ctr  0.0%  index 0.00

SHARE WITH A SEASONAL PEAK
   40% and over           n1   i307   c0    ctr  0.0%  index 0.00

TREES ON THE PAGE
   over 25                n1   i307   c0    ctr  0.0%  index 0.00

AVERAGE STORY LENGTH
   170 and over           n1   i307   c0    ctr  0.0%  index 0.00

EARNED AND WASTED, worst first (real queries, converting under half)
These have the demand already. Fixing one is worth more than a new page.
   prague           i307   c0   p5.5   index 0.00  loses ~18 clicks/10d  -
```

**How the grouping pages are doing** (10 days, 10+ impressions). Index 1.00 means the page converts exactly as its position normally does; a query in quotation marks is Google's exact-phrase operator, so read those impressions as nobody:

*species pages*

| Page | Clicks | Impressions | CTR | Position | Index | Biggest query |
|---|---:|---:|---:|---:|---:|---|
| douglas-fir | 0 | 10 | 0.0% | 17.0 | 0.00 | douglas firs (i10, p17) |

**Copy test**

```
Copy test: city-title-age-first (day 31 of 56, review 2026-11-05)
The age is the hook and the count is inventory, so naming the oldest tree before the number earns more clicks.

  control      n1    before 1.38  now 0.00  change -1.38

  TOO EARLY. At about 2 clicks per page per ten days this needs the full window; a lead now is noise wearing a result's clothes.
```

**What was sent in, and what we decided**

| seen | what | where | size for its species | ours | Hidde |
|---|---|---|---|---|---|
| before 2026-09-23 | The Twisted Muku of Omiya Gate, Kyoto  | Kyoto | - | publish | - |
| 2026-10-06 | A tree in Tokyo | - | - | open | - |
| 2026-10-06 | A tree in Tokyo | - | - | open | - |
| 2026-10-06 | Ginkgo in Tokyo | - | - | open | - |
| 2026-10-06 | A tree in Tokyo | - | - | open | - |
| 2026-10-06 | A tree in Tokyo | - | - | open | - |
| 2026-10-05 | The Southern Mahogany of Edinburgh Gar | Melbourne | - | publish | - |
| 2026-10-05 | The Finer Holm Oak of Edinburgh Garden | Melbourne | - | hold | - |
| 2026-10-05 | London Plane in Paris | - | 88% girth | open | - |
| 2026-10-04 | Ginkgo in Tokyo | - | - | lead | - |
| 2026-10-04 | Pedunculate Oak | - | 112% girth | lead | - |
| 2026-10-03 | The Whitebeam of Víkurgarður | Reykjavik | - | publish | - |
| 2026-10-03 | The Larch of Hólavallagarður | Reykjavik | - | publish | - |
| 2026-10-03 | The City Hall Maple | Reykjavik | - | publish | zet de andere foto's van onze Reykjavik gebruiker ook maar online, ik vertrouw hem meer dan jou; ook zijn semi slechte foto's zijn beter dan geen |
| 2026-10-02 | The Camphor of Oimatsu Tenjin Shrine | Fukuoka | - | publish | itoshima ik was er het was mooi en de foto ook dus keur hem goed |

6 waiting for a verdict. Disagree with one and the rule changes: `python3 scripts/judgement.py --feedback <id> "..."`, and `--learn` prints every verdict he has overruled.

**The language test** (Contract J v1.13: a translated set should pass its English twin's impressions within four weeks of indexing):

| Lang | City | Clicks | Impressions | Position | English twin |
|---|---|---:|---:|---:|---:|
| es | tenerife | 0 | 17 | 44.5 | 8 |
| ja | fukuoka | 0 | 10 | 28.0 | 1 |
| es | barcelona | 0 | 9 | 26.2 | 2 |
| de | graz | 0 | 7 | 45.1 | 0 |
| de | vienna | 0 | 7 | 32.3 | 0 |
| es | madrid | 0 | 6 | 53.8 | 0 |
| fr | lyon | 0 | 6 | 67.0 | 1 |
| it | rome | 1 | 5 | 26.2 | 1 |
| de | hamburg | 0 | 5 | 25.0 | 0 |
| es | cadiz | 0 | 5 | 45.6 | 0 |
| fr | paris | 0 | 5 | 17.0 | 2 |
| ja | kyoto | 0 | 4 | 1.0 | 1 |
| nl | amsterdam | 0 | 4 | 55.2 | 3 |
| de | zurich | 0 | 3 | 40.7 | 0 |
| pt | rio-de-janeiro | 0 | 3 | 10.0 | 0 |
| es | seville | 1 | 2 | 19.0 | 4 |
| pt | lisbon | 1 | 2 | 2.5 | 1 |
| de | munich | 0 | 2 | 11.0 | 2 |
| es | malaga | 0 | 2 | 18.5 | 0 |
| es | palma-de-mallorca | 0 | 2 | 75.5 | 0 |
| fr | bordeaux | 0 | 2 | 27.0 | 0 |
| it | palermo | 0 | 2 | 41.5 | 0 |
| it | sardinia | 0 | 2 | 46.0 | 0 |
| ja | kagoshima | 0 | 2 | 90.0 | 1 |
| de | regensburg | 0 | 1 | 52.0 | 0 |
| es | alicante | 0 | 1 | 86.0 | 3 |
| fr | nantes | 0 | 1 | 27.0 | 0 |
| it | cagliari | 0 | 1 | 62.0 | 0 |
| it | milan | 0 | 1 | 43.0 | 0 |
| ja | kanazawa | 0 | 1 | 89.0 | 2 |
| ja | osaka | 0 | 1 | 2.0 | 0 |
| ja | tokyo | 0 | 1 | 5.0 | 2 |
| nl | arnhem | 0 | 1 | 74.0 | 2 |
| pt | porto | 0 | 1 | 6.0 | 3 |

**Cities seen but never clicked** (60+ impressions, zero clicks, with what they are actually shown for):

- prague (i87): prague (i9, p9); prague (i9, p7); prague (i9, p6); prague (i9, p5)

**Climbing** (this ten days against the ten before it)

| Page | Impressions | Change | Position | Moved | Clicks |
|---|---:|---:|---:|---:|---:|
| /prague/twin-beech-of-hvezda | 32 | +31 | 8.1 | -1.1 | +0 |
| /prague/walks | 32 | +30 | 2.8 | -0.8 | +0 |
| /prague/ash-of-strahov-garden | 30 | +27 | 7.4 | -1.1 | +0 |
| /prague/oak-of-cisarsky-ostrov | 28 | +27 | 3.8 | -1.8 | +0 |
| /prague/oak-of-u-malvazinky | 32 | +22 | 5.9 | +1.5 | +0 |
| /prague/oldest-tree | 32 | +20 | 3.6 | +0.4 | -2 |
| /prague/field-maple-of-the-seminary-garden | 22 | +17 | 9.1 | -3.9 | +0 |
| /olympic-national-park/duncan-cedar | 16 | +14 | 11.6 | -3.1 | +0 |

**Newly ranking** (no impressions at all ten days ago)

| Page | Impressions | Clicks | Position |
|---|---:|---:|---:|
| /prague/oak-of-dienzenhofer-gardens | 29 | 0 | 5.3 |

- New queries this window: alte bäume (i4).

**Who they are**
Audience, 28 days of search (770 clicks, 32918 impressions):
- Countries: usa c112/i8377; nld c71/i1718; esp c66/i2590; gbr c66/i2486; deu c52/i1671
- Devices: MOBILE c555/i19353; DESKTOP c205/i13178; TABLET c10/i387
- Landing pages: / c23/i283; /prague c11/i308; /bath/plane-trees-of-the-circus c8/i151; /malaga c8/i211; /de/vienna/chestnut-avenue-of-the-hauptallee c7/i223

Web Analytics (beacon, cookieless), people only.
Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.

| Day | Visits | Pageviews | From Google |
|---|---:|---:|---:|
| 10-03 | 10 | 20 | 0 |
| 10-04 | 0 | 10 | 0 |
| 10-05 | 30 | 80 | 10 |
| 10-06 | 90 | 160 | 0 |
| 10-07 | 70 | 150 | 0 |
| 10-08 | 10 | 90 | 0 |
| 10-09 | 60 | 150 | 0 |
| 10-10 | 40 | 140 | 10 |
| **window** | **310** | **800** | **20** |
- Top paths: / (50); /explore (20); /rothenburg-ob-der-tauber/vorbachtal-spruces (20); /app (20); /seville (20); /verona (20); /leuven (20); /perth (20); /melbourne/hoop-pine-of-yarra-boulevard (20); /washington-dc/washington-monument-witness-mulberry (10); /es/palma-de-mallorca/ficus-de-la-misericordia (10); /lue/chene-de-cantaure (10)
- Referrers: (direct) (150); ancienttrees.app (490); www.facebook.com (50); duckduckgo.com (30); search.yahoo.com (30); bing.com (10); www.google.com (10); de.search.yahoo.com (10); www.bing.com (10); com.google.android.gm (10)
- Moved between our own pages: 490 of 800 pageviews (61%); the rest arrived from search or straight in. Cookieless means no session, so which page led to which cannot be measured.
- Countries: US (190); FR (70); BE (70); DE (60); GB (60)
- Devices: mobile (540); desktop (260)
- Page load (8d): p50 2456ms, p90 8692ms

Links: external referrers (a link somebody actually clicked): www.facebook.com (50); search.yahoo.com (30); de.search.yahoo.com (10)
AI: arrivals from an assistant that cited us: none yet

Backlinks (watched pages):
| Site | Links to | rel | First seen |
|---|---|---|---|
| getlisbon.com | /lisbon | followed | 2026-09-08 |
| getlisbon.com | /pt/lisbon | followed | 2026-09-08 |
| www.baumkunde.de | /copenhagen | followed | 2026-09-26 |
| www.baumkunde.de | /rogalin/russ-oak | followed | 2026-09-26 |
4 linking page(s), 4 followed. Checked by fetching the page: a link with rel="noreferrer" never appears in the referrer table, so these two lines measure different things and neither replaces the other. Unknown links stay a manual read of Search Console's Links report. This run read 12 of 12 fetched (0 unreachable), out of 27 watched pages.


**What the machine did, the last 24 hours**

| Started | Minutes | Trees | Commits | Refused | Cities |
|---|---:|---:|---:|---:|---|
| 10-10T14:45 | 22.3 | 0 | 14 | 22 | Copenhagen, Florence, Houston, New Orleans, +4 more |
| 10-10T16:48 | 34.2 | 0 | 36 | 69 | Amt Neuhaus, Bad Staffelstein, Chicago, Copenhagen, +23 more |
| 10-10T18:55 | 62.2 | -2 | 31 | 38 | Alkmaar, Amerongen, Amersfoort, Apeldoorn, +65 more |
| 10-10T21:01 | 93.6 | -6 | 56 | 86 | Boise, Bologna, Bristol, Bucaco, +44 more |
| 10-11T00:38 | 89.5 | -9 | 90 | 177 | Aarhus, Belfast, Bergamo, Bordeaux, +34 more |
| 10-11T08:09 | 0.0 | 0 | 1 | 0 | - |
| **6 runs** | **302** | **-17** | **228** | | |

- 3 of 6 produced no trees; 22 to 177 commands refused per run; 1 wrote nothing to LOG.md; last build that went live: 3h ago.

**What they made**

- Record when each page last changed
- Bruges enrichment: register records, girth and height for 4 trees; log
- Brno enrichment dead ends; log
- Apeldoorn: retire two register-dead Het Loo beeches; window summary in LOG
- Trieste enrichment, second pass: 15 more MASAF ids, museum hours; log
- Trieste enrichment: MASAF records for 19 trees; agent costs for the window; log
- Hamburg enrichment: measurements, Planten un Blomen hours, a colour season; log
- Deventer enrichment: LRMB records and measurements for 4 trees; log
- Como enrichment: MASAF records for 9 trees, Grumello hours; log
- Buenos Aires enrichment: city Arbopedia records and heights for 4 trees; log
- Belfast enrichment: Woodvale Park hours; log
- Ronda enrichment: REDIAM fichas, girth and height for 6 trees; log
- Bilbao enrichment: dead end recorded; log
- Lucca enrichment: MASAF records and measurements for 13 trees, Orto Botanico access; log

Machine: 6 chain attempts yesterday, 6 got real work time (~248 min total). Dead-in-seconds attempts cost nothing; few get-throughs means the usage window was full or closed.

**Conclusion:** Search is the only channel with real data and it is still small: 5 clicks and 35 impressions on Google's freshest day (day before: c0/i47). Directional at best; no strategic conclusions from these volumes.

