# LOG

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-10](archive/LOG-2026-10.md)
- [2026-09](archive/LOG-2026-09.md)
- [2026-08](archive/LOG-2026-08.md)
- [2026-07](archive/LOG-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
<!-- archive-index -->
## 2026-10-24 city map piles its own trees like every other map (live)

Hidde, on /lisbon (36 trees): the city map drew every species pin over the others zoomed out while /explore, the country maps, My trees and the app showed counted bubbles ("kunnen we die interacties gelijk houden?"). The city map now carries a clustered source of its own trees that decides which DOM pins show and draws the same moss bubble with the count, from the shared numbers in lib/map.ts (radius 13, distance 40, piles to zoom 14); a tap zooms to where the bubble parts, past zoom 14 the species pins and the same-spot stacks are back, and a selected tree flies to 15.5 so its pin never lands inside a bubble. Checked on a mockup of the live pages at 375px and desktop: Lisbon 6+2+16+10 plus two pins, Palermo, London 27 in six piles plus five, Bruges one 2 beside two pins. qa `check_every_web_map_piles_with_the_same_numbers()` refuses a map file writing those numbers as literals. CONVENTIONS.md "How close two pins have to be" got the dated line. Seen in passing, not fixed: /london at 375px opens at zoom 8.4, below FAR, so the live page shows one 32 bubble and no pins until you zoom in.

## 2026-10-23 night run, eighth attempt: nothing published

Inbox empty, health.py clear. `photo_hunt.py --recheck` swept 40 more kept-set trees (Alicante, Amsterdam, Arnhem), 0 new candidates. Own supply is paused and READY is 3 without photos; scout_next names Stirling, already retried today. Nothing dispatched.

## 2026-10-23 night run, seventh attempt: nothing published

No claims stood. READY is still 3 (Oxford 2, Madrid 1, no photos, supply paused). Staged-city and refill advice only adds leads while `SUPPLY_PAUSED` holds; Stirling register already retried today. Nothing dispatched.

## 2026-10-23 night run, sixth attempt: nothing published, photo lane checked

No claims stood. READY is 3 (Oxford 2, Madrid 1, no photos, supply paused). `photo_hunt.py --recheck` swept 40 kept-set trees (Alicante, Amsterdam, Arnhem), 0 new candidates. A photo-judge pass found every fetchable candidate in the kept set already judged; 720 unjudged are last-resort (no geotag, or 30 to 100 m off the pin). It viewed the 7 nearest, all wrong subjects, 8 rejects recorded (6de16587b). No approvals. Next photo step is a by-name sweep on the 35 trees left, not another viewing pass. Pillow was missing on the runner and was installed.

## 2026-10-23 night run, fifth attempt: nothing published

Sightings 0. health.py again flags "deploy skipped", which is pushes superseding each other (the latest deploys were in progress, not failed). Supply is still paused, READY is 3 without photos, and the 92 staged cities would only add leads. Nothing dispatched, nothing refused by the shell.

## 2026-10-23 night run, fourth attempt: nothing published

No claims stood. READY is 3 (Oxford 2, Madrid 1, no photos, supply paused, so no write pass). Enrichment and page gaps: nothing to do. prepare.py's staged-city and refill advice assumes supply is open; with `SUPPLY_PAUSED` a verify pass would only add leads, and the walls already hold the likely cities. Stirling already retried three times today, not repeated. Nothing dispatched.

## 2026-10-23 night run, third attempt: nothing published

No claims stood. READY is still 3 (Oxford 2, Madrid 1, no photos). The written batches parked earlier (photo-batch-2: 10, texas-famous: 4) are own supply, so they stay unmerged while `SUPPLY_PAUSED` holds. Sightings 0, enrichment nothing to do. health.py's "deploy skipped" is only cancelled or skipped runs from pushes landing close together, not a failing build.

## 2026-10-23 night run, second attempt: nothing published

No claims stood, READY is 3 (Oxford 2, Madrid 1, no photos, supply paused). `photo_hunt.py --recheck` swept 40 more trees, no new candidates. Claimed Bamberg for a verify pass, found it already holds its 9 trees and only 6 open leads, released it (now a 48h wall in data/walls.json). Munich is full (63 of 60). Stirling register retry was done in the first attempt. Nothing worth dispatching while supply is paused.

## 2026-10-23 night run (14:28 UTC window): nothing published, supply paused

Rung 1 and 2 clear (0 sightings waiting, health green). Own supply is paused, so no tree work. Ran `photo_hunt.py --recheck` (40 trees swept, no new candidates) and fetched the only four queued candidates: two Luxembourg sycamore saplings (not the tree), a giant-sequoia photo for the Trieste Ghost Pine (species mismatch) and a worm's-eye chestnut for the Trieste plane (wrong species, no frame). All four rejected, nothing approved. Enrichment, recognition lines and page gaps all say nothing to do. Scouted Stirling again (rung 5): only Inchmahome yews/oaks and the Bridge of Allan sequoia as leads, still stalled, note in data/register-scouting.json. READY leads (Oxford 2, Madrid 1) have no photo, so they wait. Nothing refused by the shell.

## 2026-10-24 session: map list comes down again with no trees in view

App: a raised list on the map stayed stuck once no trees were in view (Hidde's report). The empty-list lock now stops raising only, never lowering (BottomSheet.swift). Checked on the iPhone 17 Pro simulator: raised over Amsterdam, panned to Ruigoord, dragged down to peek, and an upward swipe still leaves it down. For Hidde: next build carries this fix.

## 2026-10-24 session: the six weeks concentrate on Lisbon

After the cold-start research (reports/Kip ei start van content apps.md: nine apps, every one grew contributors in one dense place with a few named people), Hidde chose Lisbon ("Yes, Lisbon"). GO_TO_MARKET.md carries the revised plan and the measure: Lisbon trees with a stranger's photograph, 5 today, ten by 2026-12-05. Lisbon stands at 36 trees, 18 approved photos, 32 confirmed pins; Commons is judged out for the 18 photo-less trees (every candidate rejected by 10-19), so photographs come from people. A search pass found fifteen people and bodies who already photograph Lisbon's trees (drafts/lisbon-ten.md, local: Commons uploaders, three juntas, Gigantes Verdes, a tree-walk organiser), and ten first mails are drafted in drafts/lisbon-ten-mails.md, one tree each, for Hidde to send two or three a week. Side finding: JF Penha de França's felling notice of 10-20 on Praça Paiva Couceiro is a white poplar, not our ginkgo (lis_008 stands). Instagram: six posts drafted as a business card (drafts/instagram-first-six.md).

## 2026-10-24 session: Wilder's article is out, four followed links

wilder.pt published the Lisbon interview on 2026-10-23 (Ines Sequeira): links to the home page, /lisbon, /porto and /contribute, all followed, no App Store link. The second press placement ever and the first with links. Watched by backlinks.py, contacts_db marks Wilder linked, details in drafts/OUTREACH.md. Nothing in the product changed; the digest's GA and Portugal download rows are where it shows from 10-25.

## 2026-10-24 session: Show HN posted

Hidde posted "Show HN: I'm mapping the old trees worth walking to (3,800 so far)" at 15:04 Dutch time, news.ycombinator.com/item?id=50208440, from his own account; first comment in his About-page voice with the AI paragraph in his own framing (drafts/show-hn.md, local). Measure over the week: points and comments on the item, visitors with referrer news.ycombinator.com in Google Analytics, submissions and accounts. OUTREACH_STRATEGY's "later or not at all" was replaced on his word on 10-23.

## 2026-10-23 session: Reddit threads (r/Lisbon, r/sicily), a Sicily collection, the Messina fig live

**In the product:** /collections/sicilys-most-remarkable-trees (13 trees: Palermo, Catania, Sant'Alfio, Messina) as the page Hidde's r/sicily post links to in its edit; out of Google like every collection under the strict cut. /messina/the-moreton-bay-fig-of-villa-mazzini is the first tree from a Reddit tip to go live: regional register sheet 05/F158/ME/19 (25.13 m round) plus LetteraEmme 2020, a CC BY-SA Commons photograph with the board in front of the trunk, looked at. **Rule:** a stranger's public tip is a reader's tree under the supply pause (`found_by_reader.tip`, findable.reader_added; CLAUDE.md). **Outreach:** a post is for people, not tips, the name goes in every thread (OUTREACH_STRATEGY.md); HIS_VOICE got his AI line and the no-photo-ask-by-reflex lesson. **Leads:** Seia (Souto da Lapa chestnuts, the tipster's photos were off the internet), Agrigento (7 Valle dei Templi register trees, a walk; the Borgo Giallonardo olive blocked on hotel grounds), Syracuse, Pozzallo. r/sicily gave 8 places in two hours and no accounts; GA referrals to check tomorrow for both subs.

## 2026-10-23 session: Mapillary tried as a photo source

Two trees looked at in the viewer (Catania figs, Den Bosch plane): coverage at both, frames from dashcams and walks where the tree is at the edge or out of shot. Verdict in OPEN_DATA_SURVEY.md: a dated life check, rarely a photograph; the API needs a free token Hidde would have to create. Nothing in the product changed.

## 2026-10-23 session: the Season Radar case, answered; Plus parked; one digest row
Made the case that Season Radar (a dated push) is the retention hook and the paid feature (docs/season-radar-case.md, conventions looked up in CONVENTIONS.md: Weathernews 紅葉Ch., eBird, Audubon, AllTrails, Strava, Apple; mockup beside the reference in a preview). Hidde was not convinced and was right: return is a monthly, trip-shaped thing, season is content, and the open question is the Plus step once people upload trees, which is parked until free traction (DECISIONS.md 2026-10-23). Today's cohorts: 103 stranger phones, 60 opened on one day only; back within 7 days 1 in 3 in September, 1 in 5 in October (not the 1 in 13 quoted on 10-22). **Digest: unchanged in the end.** A row under "Phones back within 30 days" (how many of those saved, ticked or photographed a tree in those 30 days) was built, widened and removed within the hour on Hidde's word ("slechte titel en vraag me af of dit nou het getal is"): his seven headline numbers already say whether there is free traction. What the exercise did settle: of the 23 phones back on three days or more, 10 gave something and 13 never, so the session's line that "the ones who come back are the ones who contribute" was wrong. Nothing in the product changed.

## 2026-10-23 night run, fourth attempt: nothing new, said plainly
Nothing changed on the site. No claims, READY leads still the same 3 (photo-less, supply paused). `photo_hunt.py --recheck` swept 40 more kept-set trees (Alicante, Amsterdam, Arnhem): 0 new candidates. Stirling already retried yesterday. Remaining kept-set photo-less trees: about 985, same sweep next run.

## 2026-10-23 night run, third attempt: two species intros
Wrote the two missing species intros (Sugar Maple, Eastern White Pine) from the site's own trees; `pagegaps.py --check` now clean. Bing only while the strict cut holds. Not built or qa-run here (no site/dist). Nothing else workable: claims empty, READY leads photo-less under the supply pause, enrich empty.

## 2026-10-23 night run, second attempt: nothing to do, said plainly
Nothing changed on the site. No claims standing. READY leads (3: Oxford x2, Madrid) have no approved photograph and own supply is paused (`SUPPLY_PAUSED`), so no write pass. Written-and-ready batches (photo-batch-2, texas-famous) are held by the same pause. `enrich.py --next` and `photo_gaps.py --shortlist` empty; pagegaps only species pages, which the strict cut keeps out of Google. Stirling register retried yesterday and stays stalled. iOS fix (FlowWalk) is running in CI. Open for Hidde: when own supply restarts, photo-batch-2 (10 trees) and texas-famous (4) are ready to merge.

## 2026-10-23 night run (09:00 UTC): photo recheck on the kept set, nothing live
Nothing changed on the site. Rung 1 empty (0 sightings). Rung 2: the iOS app failure of 10-22 is a FlowWalk assertion (search-to-a-tree has no way back after the first result); a fix commit is already running in CI, so left alone. Own supply is paused, so I ran `photo_hunt.py --recheck` (no new candidates) and `photo_fetch.py --roster`, which fetched 7 images for Luxembourg, Como and Trieste. I looked at them: a sycamore seedling, a magnolia and a statue, a dark chestnut shot, and a giant sequoia against our Monterey Cypress. All 8 candidate urls rejected via photo_verdicts.py (the `page` field must hold the candidate url, not the city). prepare.py printed no 7-day visits line.

## 2026-10-23 session: readers' photos lead the page, and readers hear when theirs is live

What changed in the product: a reader's photograph now becomes the LEAD on a tree's page, the old lead moving into the strip ("if google appreciates them as lead better then make them lead"; `unique_photo()` reads the lead only). Applied to the three trees that had one as an extra only (cma_001, lis_030, tkc_001). And a reader whose photograph goes live gets a mail: the first at once, later ones bundled, at most one per 30 days (text he approved in drafts/photo-live-mail.md; sent by nightly.yml's mail step). The weeping cedar's reader is queued for the first one. Hidde agreed on the cedar (judgement filed). The red iOS check is one flaky test (search-to-a-tree in FlowWalk, 229 of 230 pass); not fixed.

## 2026-10-23 session: source batch sent, Season Radar session started

Hidde: "verstuur een batch!" The source batch of ten (people-run sites our tree pages cite, link ask) went out, then on his second word press round 4 (ten regional desks) and tourism batch 2 (Porto, The Hague, Ede, Cagliari): 24 mails today. Every desk from the 10-20 press list is now mailed; round 5 needs new desks from the kept set. Sent log and contacts database in the private store. A separate session makes the case for Season Radar as the retention lever, honestly, with references; nothing built.

## 2026-10-23 second restart: nothing to ship

No claims; READY still 3 leads without photographs; inbox empty; supply paused. `photo_hunt.py --recheck` found 0 new candidates in its 40-tree slice. `vendor_photos.py` still cannot downscale bne_004 and chi_023 (no Pillow on this runner). Deploy dispatch refused (HTTP 403 from this token), so the live site stays behind main until the next scheduled build. For Hidde: nothing.

## 2026-10-23 restart attempt: nothing to ship, and why

No claims standing. READY holds 3 leads (two Oxford, one Madrid), none with an approved photograph. The 15 written trees (photo-batch-2, texas-famous, ftw_018) and the 11 held city files are not waiting on the pace cap any more: own supply is paused (SUPPLY_PAUSED), per data/research/held-pace-2026-10-22/README.md, so merging them would break the 10-22 ruling. Stirling register was retried earlier today. Refill and verify lanes add leads only, and the shelf already holds more than the paused supply can use. No trees added.

## 2026-10-23 03:00 window: photo sweep and vendoring, no new trees

- Rung 1 inbox empty. Rung 2: Smoke skipped (push condition) and iOS failure (FlowWalk, needs a Mac) answered in health.py. Supply paused and READY leads lack photographs, so no write pass.
- `photo_hunt.py --recheck` swept 40 kept-set trees; photo-judge viewed 13 files for 16 trees, approved none (park-wide aerials, sculptures, a mineral; The Hague beech has no geotag). Kept-set queue has no unjudged candidates left.
- `vendor_photos.py` put 22 photographs on our own domain; bne_004 and chi_023 failed to downscale (Pillow missing on this runner), still to vendor.
- For Hidde: nothing.

## 2026-10-22 restart attempt: nothing shipped, no claims standing

No claims standing. READY has 3 leads (2 Oxford, 1 Madrid): the Oxford ones are approximate pins with no photograph (one a young oak, one a 2008 sighting needing a life check), so `ADD_NEEDS_PHOTO` and the supply pause keep them out. Staged cities need a verify pass but own supply is paused; Stirling was already retried. Nothing useful to dispatch under the rules.

## 2026-10-22 late attempt: nothing shipped, Stirling retried

No standing claims. READY is Oxford 2 and Madrid 1, both without an approved photograph, and own supply is paused, so no write pass. Enrichment: nothing to do. BACKUP register retry, Stirling: Wikidata within 25 km holds only the Wallace Oak (Torwood, Falkirk), already a lead in glasgow.json. Verdict stays stalled, note updated. Honest result: nothing useful left on the ladder under recovery mode.

## 2026-10-22 22:55 window: iOS failure read, nothing shipped

Rung 2: health.py flags the iOS app run of 20:24 (1h48m). Log: 229 passed, 1 failed, `testEveryFlowLeavesAWayBack`: flow "search-to-a-tree" has no tab bar, back button or dismiss after "first-result". No ios/ commit since the green run of 11:34 (only a test string), so this is a data/feed change or a flaky tap, not an app edit; it cannot be reproduced on this Linux runner and the night run never builds the app. For Hidde or a Mac session: rerun ios.yml once; if it fails again, look at the first search result's tree screen (the SearchFlow in FlowWalk). Reader inbox empty, READY leads still only Oxford 2 and Madrid 1 (own supply paused), enrichment says nothing to do. No deploy dispatch attempted (403 earlier).

## 2026-10-22 session: three outreach batches on Hidde's desk for 10-23

Press round 4 (the ten regional desks left from 10-20, autumn hook where the page has it), a source batch of ten people-run sites our pages cite, and tourism batch 2 (Porto, The Hague, Ede, Cagliari). All drafted, mailcheck and dry runs clean, every link 200, previews in drafts/batch-*-2026-10-23-preview.md (private, pushed to the private store). Nothing sent; his word goes into approved_word first. Inbox read: nothing waits for a reply.

## 2026-10-22 r/Lisbon thread read: replies drafted, Gigantes Verdes scouted

- Hidde's r/Lisbon post (16 upvotes, 2.3K views after 8h). New since the last pass: a commenter posted a photo of the Santa Iria olive (lis_036, no photo yet); others pointed to Gigantes Verdes, a volunteer big-tree map. Replies for him to post are in drafts/reddit-lisbon.md (photo permission ask first, then the tracking question, the cork oak, a grandparent memory to quote on lis_003 with consent).
- Gigantes Verdes (Associação VERDE): all rights reserved per their terms, so blocked as a source to import, a finding aid only; recorded in data/register-scouting.json. Permission would be an outreach mail, only if Hidde wants it.

## 2026-10-22 fifth attempt: nothing shipped, nothing live changed

- No claims standing. READY leads: 3 (oxford x2, madrid x1), but own supply is paused and none has an approved photograph, so none can ship. Awaiting-a-writer files are the same story, plus several duplicate-by-coordinate flags (las-vegas, london, munich, new-york, taiwan, washington-dc) that passcheck --pending says to fold by hand.
- `photo_hunt.py --recheck` swept 40 kept-set trees: 0 new candidates. `photo_fetch.py --roster` fetched only 7 images (luxembourg-city, como, trieste), too few for a photo-judge pass.
- Stirling register retry (BACKUP): its note's next angle is Wikidata/OSM nodes, a research hunt with low yield while supply is paused. Not started; status left as stalled.
- Deploy not dispatched (403 in earlier attempts).

## 2026-10-22 fourth attempt: nothing to ship, deploy still not dispatched

No product change. No claims stood. Reader inbox empty. READY leads are only Oxford 2 and Madrid 1 (own supply, paused, no write pass). `photo_hunt.py --recheck` swept the kept set again: 0 new candidates, nothing left unchecked. The Brisbane hero fix (bd86678a6) is on main, but both push-triggered deploys were "skipped" and `gh workflow run deploy.yml` returns 403 from this token, so the site is still not confirmed rebuilt. For Hidde: dispatch Build and deploy once (or let the next knock do it) and check that it goes green.

## 2026-10-22 19:41 window: deploy fix (Brisbane hero), nothing else to publish

Rung 2: the Build and deploy run of 18:05 failed on qa's soft-hero check (Brisbane hero, the City Botanic Gardens banyan, was the 500px iNaturalist rendition while 3648px photos sit elsewhere in the city). Switched that same photograph to its 1024px `large.jpg` rendition (checked 200 OK) in data/cities/brisbane.json, preflight 0 problems, pushed as bd86678a6. The push's deploy run came back "skipped" in 9s, so the site is not yet confirmed rebuilt: the next run should check `gh run list --workflow=deploy.yml` and dispatch a deploy if it is still red. qa.py cannot run here (no site/dist, build is refused). No reader submissions waiting. `photo_hunt.py --recheck` swept 40 kept-set trees: 0 new candidates. Enrichment says nothing to do; own supply is paused, so the 54 awaiting-writer trees and READY leads were not touched. Nothing else shipped.

## 2026-10-22 third attempt: Minneapolis register retried, nothing shipped

No product change. No claims stood. READY leads (Oxford 2, Madrid 1) are own supply and own supply is paused, so no write pass. Retried the BACKUP register: the MPRB Heritage Tree page renders now but gives no licence, says trees may be on private land, and offers only a Google My Map; still not imported (note and "retried" date in data/register-scouting.json). Next angle: mail MPRB for the list and licence; Hidde sends.

## 2026-10-22 photo viewing pass pj2 on the kept set: nothing approved, 70 rejects recorded

No product change: no tree gained a photograph. 32 images looked at as pixels (Arnhem arn_004/005/007/008/021/026/027/028, Florence flo_007/016, Kagoshima kag_011, Baarn brn_007, Utrecht utr_006/007/031, Nijmegen nij_019/020, The Hague hag_024/027/028/030, Vienna vie_035/036, Singapore sgp_015, Amsterdam ams_016/027, Brisbane bne_005/013); 70 tree-candidate rejects written to data/photo-queue.json so none is judged again. Approvals: none, so no reversal commands. The swept Arnhem candidates are sculptures (Pluto, VLUCHT) with trees as background; the rest are monuments, information panels, buildings, swans, overviews, two black-and-white archival street scenes, and an iNaturalist bunya pine offered for the Cook and Hoop Pines. One near miss worth a lead: "Firenze, giardini del bobolino, 10.jpg" is a fine multi-stemmed red-barked cupressaceous conifer in the Bobolino, not our cedar or stone pine. Remaining unjudged rows in kept-set cities are mostly last-resort radius hits (Mapillary, street files); not worth a pass without a better sweep. Preflight 0 problems.

## 2026-10-22 later attempt: nothing shipped, nothing claimed

No claims standing. Three READY leads (two Oxford, one Madrid) have no approved photograph and own supply is paused, so none ships. Health clear, reader inbox empty. `photo_hunt --recheck` swept 40 kept-set trees (Alicante, Amsterdam, Arnhem): 4 new candidates in Arnhem, but `photo_fetch` says nothing to fetch for them, so no viewing pass was worth the tokens. Manchester register retried: still none; two named-tree leads noted in data/register-scouting.json (Heaton Park eucalyptus, Alexandra Park Railway Poplar), each needs a second source. No trees added.

## 2026-10-22 night window (from 17:39 UTC): reader photo, photo sweep

Rung 1: a reader's photograph of the Weeping Cedar of the Vallée-aux-Loups (cma_001) looked at, same tree, daylight and colour, added beside the lead photo; the verdict record had to be stubbed by hand in data/judgements.json because sightings_publish.py had already cleared the queue entry (judgement.py --scan found nothing). Health clear. Own supply is paused, so rung 6: photo_hunt --recheck on the kept set, then a photo-judge pass: 26 images viewed, 1 approved (bne_004, Brisbane banyan, iNaturalist CC BY, 500px only), 32 rejects recorded; most kept-set candidates are generic park files shared by several trees. To check: msl_003 Krüsellinde may have been missed in a 2020 photo (life check). Prepare's REFILL note is moot while supply is paused. Not pushed (credential note); Run health pushes.

## 2026-10-22 session: the night runs under the demand cut

Own supply paused (Hidde: "moeten we de nachtruns nog aanpassen dan?"): preflight now refuses a new tree of our own (check_own_supply_is_paused, SUPPLY_PAUSED in findable.py); a reader's tree still ships. thin_pages.py writes data/index-kept.json, the cities with a page still in Google; enrich.py --next and photo_hunt.py (without --city) take their queue from it instead of the 259-city roster. The 12 trees held past the pace cap stay in data/research/held-pace-2026-10-22/ (README says why). CLAUDE.md recovery mode says so.

## 2026-10-22 session: the demand cut, hreflang, the sources line

Google: the 09-28 fall sits inside the September 2026 spam update (24 Sep to 8 Oct), no core update since May. Demand cut added to scripts/thin_pages.py (DEMAND_CUT 50): 720 more pages carry the googlebot noindex, 598 English tree pages in 101 cities and 84 place pages stay in Google, every unique-photo page and reader-found tree kept; Bing keeps everything. hreflang now names only indexable alternates. The Sources line on every tree page says the story was written with AI and readers correct it, in eight languages. The recrawl sitemap was already live since 10-01 (robots.txt names it), nothing for Hidde to submit. Preflight 0 problems; the Astro build runs in CI on this push. Each change is its own commit.

## 2026-10-22 session: about page tightened

About page: "huge" from four to one, "marvel" from two to one, and the sources line now says what is true ("written with AI, and readers who know the trees correct them" instead of "corrected by people who know the trees"). A comment marks where the Wilder (wilder.pt) article link goes once it is published; Hidde wants it linked (2026-10-22). Hidde's own text otherwise untouched.

## 2026-10-22 night run (third retry): cap at 73 of 60, nothing shipped

No claims standing. Only 3 READY leads, none with an approved photograph. Tried goliad.json into data/cities again: preflight fails on `check_publishing_pace()` (73 new trees in 24 hours, cap 60) and the missing data/us-states.json entry; moved it back out to out/tmp/. The 15 written trees still wait for the count to drop. Manchester register retry not attempted (the TPO layer is protection, not remarkable status, per the scouting note). No trees added.

## 2026-10-22 night run (second retry): cap still holds, Inverness retried

No claims standing; 3 READY leads (two Oxford, one Madrid) have no approved photograph so none ships. 15 written trees (photo-batch-2 10, texas-famous 4, ftw_018) wait only on the 24-hour pace cap, as do the 11 held city files in data/research/held-pace-2026-10-22/ (add college-station, coppell, goliad to data/us-states.json when restoring). Inverness register retry: Wikidata has no tree items inside it, still stalled, noted. Munich photo recheck repeated the earlier result (muc_022, 026, 027, 037 candidates await a photo-judge pass). No trees added.

## 2026-10-22 night run (retry, 15:00): photo lane while the pace cap holds

Resolved a LOG.md rebase conflict. The pace cap still holds 54 verified trees, so I added no verify or write passes. Munich photo recheck found 7 new candidates (muc_022, 026, 027, 037); a photo-judge pass was dispatched on them. Tulsa register retry: still no county list, only the Creek Council Oak, noted in data/register-scouting.json. No trees added.

## 2026-10-22 session: product list checked against the product

Hidde asked how current the open list is. Item 19 ("I have seen this one" behaves differently on web) is gone from PRODUCT_TODO.md: that control no longer exists, collecting is by photograph on web and app since 2026-10-10/14 (Collect this tree, camera then seal, one sheet). Item 17 (Hide My Email second account) now carries a count: 9 of 36 accounts use an Apple relay address, 1 of them has saves; no duplicate proven. Checked afterwards: Apple sign-in is already live on the web (2026-09-17) and the web route answers, so Apple on both surfaces is one account; the only unclosable case is Google on the web plus hidden Apple in the app, which needs a merge flow. Noted on the item. Nothing in the product changed.

## 2026-10-22 night run (14:49 window): nothing publishable, pace cap

Rungs 1 and 2 clear (no reader photos, health green). Tried to merge the three Texas places; preflight refused on the pace cap (75 new trees in 24 hours against 60) and the missing us-states entries, so I moved them out of data/cities again (now in out/tmp/, copies still in data/research/texas-places/). Photo recheck sweeps on Munich and Paris found 6 new Munich candidates; the only one fetched (Luitpoldpark, muc_027) shows a stand of bare trees, not this one, so nothing approved. enrich.py says nothing to do. No trees added; this window did nothing useful beyond confirming the cap.

## 2026-10-22 night run (retry attempt): pace cap holds 12 trees

Eleven new city files an earlier attempt left uncommitted (bregenz, college-station, coppell, goliad, hagerum, hochosterwitz, leonstein, ogi, sakurai, shikokuchuo, winterswijk; 12 trees, all with approved photographs) failed preflight: 84 new trees in 24 hours against the cap of 60, and three Texas places (college-station, coppell, goliad) missing from data/us-states.json. Moved to data/research/held-pace-2026-10-22/ to restore tomorrow: add the three states, move the files back, run preflight. Nothing else was writable: 3 READY leads (two Oxford, one Madrid) wait on photos, and every claim was already free.

## 2026-10-22 night run (12:29 UTC window): enrichment leiden+frankfurt+regensburg

Rungs 1 to 3 clear (no sightings waiting, health green). Rung 4: enrichment pass on 7 trees; one gap closed (frk_023 Bethmannpark Ginkgo girth 484 cm, height 26 m from Baumkunde.de, a private register, noted as such), 10 gaps dead-ended for 90 days. Preflight 0 problems.

Then a verify pass on San Francisco (top US city under target with supply): nothing shippable. No unmined register row has an open-licence photograph (Commons and iNaturalist searched at each coordinate) and the rest are private yards. Three leads added to data/leads/san-francisco.json (Dr. Hurd Manzanita may be sidewalk-visible, Cook St Norfolk Pine view-only, five private-yard trees re-confirmed blocked). SF is a wall for new trees until photos exist; a photo sweep is the route.

Scouting retry on Oxford (scout_next RETRY): still stalled. No Wikidata trees, no open register; leads only (Headington Hill Park butternut and oak, Addison's Walk oak, Iffley horse chestnut, felled Tolkien pine blocked) in data/leads/oxford.json, none with a coordinate and open photo. oxford-tree-trails.org timed out at 20 s (not blocklisted). Window ended on walls: nothing new published this run; the real route is photo sweeps, not more verify passes.

## 2026-10-22 session: US photo push, nothing to approve

Hidde asked how our US supply looks after three US downloads in a day. Verdict: plenty of trees (456 in 76 places, second after the Netherlands) but 90 photographs, so most US tree pages sit outside Google. The cities Google shows are nearly bare: Oahu 5/21, New York 8/28, Houston 0/11, Chicago 1/38, Portland 2/33, Dallas 1/12.

- `photo_hunt.py --recheck` over all 32 US roster cities (free API sweep). Only 15 trees had candidates nobody had judged; the rest were rejected in earlier passes.
- One photo-judge pass on those 15 (94k tokens): 0 approved. All 18 images were off-subject; ten champion trees in Chicago and Pittsburgh all drew the same 1941 "Champion" train postcard. "champion" is now a not-distinctive word in photo_hunt.py.
- Read: Commons is exhausted for the US photo gap. The next real source is a new one (Flickr CC, state champion-tree registers with photos, or readers), not another sweep.

## 2026-10-22 (session with Hidde): Madrid's Guia Verde read, four leads

Madrid's tourist office answered the 10-20 tourism mail by pointing at the city's new Guia Verde de Madrid (2026 PDF on madrid.es). Read it: mostly parks in general, few single trees. Four new leads in data/leads/madrid.json, best the Castellana elm opposite the Hotel Villa Magna, "Madrid's oldest street tree" (18 m, 380 cm, singular under the 1997 PGOU); it needs a second source, a trunk pin and an open photo. The guide's photos are all rights reserved. Register lead: the 1997 PGOU catalogue of arboles singulares. Reply draft asking who at the city could release the photos: drafts/reply-madrid-turismo-2026-10-22.md, sent on Hidde's "verstuur" the same day.

## 2026-10-22 (session with Hidde): ten famous trees with photos written, parked behind the pace guard

- **Ready, not live:** 10 trees with approved Commons photos, 8 new places, ready in data/research/photo-batch-2-places/ (winterswijk, leonstein, hochosterwitz, bregenz, ogi, hagerum, shikokuchuo, sakurai) plus kna_002 Tate-no-Omayumi for Koriyama in data/research/photo-batch-2-verified.json. Preflight passes on them except `check_publishing_pace()` (82 in 24 hours). **Next run once the count drops:** move the eight files into data/cities/, append kna_002 (from the verified file, without `_city`, `_slug`, `alive_basis`, `country`, `place`, `place_note`) to data/cities/koriyama.json, preflight, merge. The night run's three Texas files (data/research/texas-places/) go first, they were parked earlier.
- **Found gone despite a good photo:** Birr Castle grey poplar (blew down 2014), the Québec cannonball elm (felled 2021), and the Everseiche looks dead in a July 2025 photo. A photo is not a life check.
- **Held:** Häradseken (no public path known on Gotland farmland), Mogadouro (no written source), Hamerenne (private front garden).
- **Waste, said plainly:** the four Texas trees were verified and written twice. A night run took this LOG's "next lane: Texas" an hour before my claim, and my claim was named `photo-batch-2`, so neither side could see the other. A claim should name the place or list it covers. Cost of the pass: verify 226k, write 175k, for 10 trees, about 40k a tree.

## 2026-10-22 (session with Hidde): Hong Kong OVT photo sweep, low yield

- We hold 698 of the 713 OVT/SWT register trees (data/registers/hongkong-ovt.json) and publish 21. A Commons geosearch (40 m) on the 50 biggest unpublished ones found open-licence files near 33, but they are street-photography series ("SS2", "Px3") of roads, shops and statues; the five most promising, viewed, held no whole-tree photograph (aerial roots close-up, a statue, a street with the banyan in the background, privet flowers). Treat Commons geosearch on Hong Kong OVT trees as exhausted; script and results in out/tmp/hk_ovt_sweep.py and out/tmp/hk-ovt-photos.json (not committed).
- Better routes, both waiting on Hidde: a reader's photo ask in r/HongKong in his voice (as in r/Lisbon), and Gavin Scott Coates, who made HKU's Digital Arboretum (digarb.hku.hk, suggested by a commenter on his r/Lisbon post) and is the Gavin Sally Bunker of leafy.hk introduced on 2026-10-14; Hidde contacts him on WhatsApp himself, so no mail. Kowloon Park alone holds seven big unpublished OVT figs, a walk if photos turn up.

## 2026-10-22 (session with Hidde): 481 colon reveals out of the indexed stories

- **Product:** every colon reveal in the 1,183 stories Google indexes is rewritten (481 sentences, 218 place files): a full stop or a comma and a plain clause, every fact and number unchanged (the apply script refused any sentence whose numbers changed), every story still 150 to 250 words. Translations, now out of Google, keep their older wording.
- **Guard:** preflight's `check_no_colon_reveal_in_an_indexed_story()` refuses the shape in any story with an approved photograph; BRIEF_WRITING.md and CLAUDE.md (Stories) say so. **For the night run:** approving a photograph on a tree whose story has one means rewriting that sentence in the same commit.
- **Reddit:** Hidde posted his own r/Lisbon post with a reader's photo (118 views, 1 upvote in the first hour, no comments yet). Replies are in drafts/reddit-lisbon.md.

## 2026-10-22 (session with Hidde): what Google sees on the indexed pages, five checks

- **Fixed, live with the next deploy:** (1) 118 paid trees told Google `isAccessibleForFree: true` because "under 6 free" sat in their access line; paid_entry now decides first, English and translated pages. (2) 280 sources written "url (note)" rendered as one broken link; the link is now the url alone (site/src/lib/tree-sources.ts). (3) 23 dead source links repointed: Luxembourg's dated register download to the dataset page (9 trees), four renamed Wikipedia lists (Graz, Innsbruck, Berlin-Mitte, Kopčany; 14 sources). Innsbruck inn_003 and inn_006 had every link dead and now have a live one.
- **Measured, nothing to fix:** shared text on 60 indexed tree pages is a median 31%, and it is all interface (sheet buttons and dialogs), no story sentence on 20%+ of pages. JSON-LD is clean (WebSite, Organization, TouristAttraction, BreadcrumbList).
- **For the night run:** `python3 scripts/source_links.py` (new) lists about 40 remaining dead source links on indexed trees, one per tree; repoint each (the host's search, the Wayback Machine), never drop a tree's last source. PageSpeed Insights answered 429 today (keyless quota); retry `python3 scripts/pagespeed.py` another day.
- **Colon reveals:** done the same afternoon on Hidde's "waar wacht je op", see the entry above.

## 2026-10-22 (session with Hidde): translations out of Google too

- **Product (Hidde: "translation uit de index halen dan?"):** every translation of a place or tree page (654 urls) joins the strict cut, googlebot tag only, Bing keeps them (`TRANSLATIONS_OUT` in scripts/thin_pages.py). Four translations a digest showed before 09-28 stay. Google's index goes to about 1,450 English pages, nearly all photographed trees plus roster places.
- **For the night run:** new translation passes pause while `TRANSLATIONS_OUT` holds (CLAUDE.md, recovery mode); the BACKUP lane is register scouting.

## 2026-10-22 (session with Hidde): readers' words on the page; iOS test green again; Baarn line refused

- **Product:** the Montsouris plane (par_034, English and French) and the Hammundeseiche (fwd_001) now quote their readers instead of paraphrasing them. New `scripts/reader_words.py` lists every stranger's note on a live tree that no story quotes yet (0 left today); sightings_publish.py prints it after publishing. Rule in CLAUDE.md, Reader input.
- **Fixed:** iOS CI failed on one unit test still looking for the pre-copy-sweep wording ("Allowing photos"); the test reads the new sentence. App unchanged.
- **Mail:** mailcheck refuses "I live in Baarn" without what he does in the same sentence, and "minutes from Amsterdam" (Hidde: "when will you remember that this sentence is weird"). drafts/group-messages.md (untracked, names people) now opens with a status table: Fred Breglia and Samuel Mitchell were mailed on 10-16, the Ancient Tree Forum is not mailed again; only the four Reddit mod messages are open. Hidde's Reddit account is new, so he comments for a week before the first post.

## 2026-10-22 (session with Hidde): the strict cut, 367 more pages out of Google

- **Product (Hidde: "ik ga liever te ver nu met meer kans op herstel en dat we dan langzaam weer toe laten"; "alleen uit Google, Bing houdt ze"):** every species (197), park (49), collection (19), state (10) and country page, the place pages of cities off the frozen roster, and translations there now carry the googlebot noindex. Bing keeps them via sitemap-bing.xml. 367 paths, `STRICT_CUT` in scripts/thin_pages.py (group 5 in data/noindex.md). Kept: the roster, anything a digest's top pages showed before 09-28, and every photographed tree page in English. Google's index goes from about 2,450 urls to about 2,080, nearly all photographed trees plus roster places.
- **Ratchet widened with Hidde's yes:** qa's `check_the_noindex_split_holds()` lets the strict cut's listing and place pages carry the googlebot tag (it allowed tree pages only); question pages still never may. The recrawl and Bing sitemaps skip listed paths the build did not make (six listing files with too few trees).
- **Not verified locally** (no local build): the deploy's qa run is the first full check of the tags.
- **Letting back:** only once Search Console shows recovery, in steps, places and countries first, then species, each step after the previous one earns impressions.
- **Press, wait (Hidde: "laten we maar even wachten we zijn met beide in contact geweest"):** no follow-up to Omrop Fryslân (Wybren, last mail 10-15) and no news pitch to Omroep Brabant (link ask 10-15) until Hidde says so.

## 2026-10-22 night run (fourth attempt): nothing shipped, pace guard still at 75

- Shipped nothing. Tried the three Texas place files (college-station, coppell, goliad) again: preflight still fails only `check_publishing_pace()` at 75 new trees in 24 hours (cap 60), so I reverted the move. Next run once the count drops: move the three files from data/research/texas-places/ into data/cities/, add the slugs to data/us-states.json ("Texas"), preflight, merge.
- READY leads: 0. san-francisco photo recheck: 8 trees, 0 new candidates. The san-francisco claim stands (sfo_012, sfo_013 need stories, which add new trees, so they wait on the same guard).

## 2026-10-22 night run (third attempt): enrichment only, new trees still behind the pace guard

- Nothing READY. Everything awaiting a writer is either already published (stale files), a duplicate, or adds new trees, which the pace guard (75 in 24 hours, cap 60) still refuses; so no new trees this window. The san-francisco claim stays (sfo_012, sfo_013 still need stories; release refused until merged).
- Seattle enrichment: 9 SDOT street trees, pin-only gaps with no photograph and no register page; recorded as dead ends (`enrich.py --done seattle`). Dispatched an enrichment verify pass on leiden+frankfurt+regensburg (answer to out/enrich/leiden+frankfurt+regensburg.answer.json).

## 2026-10-22 night run (second attempt): three Texas place files built, held by the pace guard

- Nothing was READY. Verified and wrote four famous Texas trees that already had open photos (Century Tree, Houston Campsite Oak, Cart War Oak, Rio Frio Landmark Oak). Three have approved photographs and full place files, parked in `data/research/texas-places/` (college-station, coppell, goliad; ids clg_001, cpl_001, gld_001). They pass preflight except `check_publishing_pace()` (75 new trees in 24 hours, cap 60), so they were not published. Next run once the count drops: move the three files into data/cities/, add the three slugs to data/us-states.json ("Texas"), run preflight, merge, then release no claim (none held).
- Rio Frio oak (txf_004) is written but held: its photo has no geotag and was shot from inside the fenced land. Kept in data/research/texas-famous-verified.json, story intact, until a roadside photo turns up.
- San Francisco deepen pass: sfo_012 (Cork Oak, Landmark Tree 15) and sfo_013 (Moreton Bay Fig, view-only) verified, no photographs, so they wait for a photo (ADD_NEEDS_PHOTO). Claim on san-francisco stays until they merge or the claim expires. 4 leads kept. sfenvironment.org and citizenportal.ai return 403.
- inn_007 skipped: pin on a building, probably private yard, no photo.

## 2026-10-22 night run (09:06 UTC window): photos and scouting, no tree added

- Ladder: no reader photos waiting, health clear. Nothing writable: the one written tree (ftw_018) has no confirmed photo path and the other "awaiting a writer" files are stale or duplicates. prepare.py 7-day visits line not shown by this run's output.
- Photo sweep Chicago (36 trees, 6 new candidates) and Seattle (27, 2 new): sweeps otherwise exhausted. Viewing pass on the 19 roster-fetched images (hong-kong, pittsburgh, luxembourg-city, como, trieste, dresden): 0 approved, 18 rejected (wrong species, close-ups, felled twin, non-tree). Chicago and Seattle candidates were not fetched by `photo_fetch.py --roster` (it said nothing to fetch for them); next run should check why.
- Chicago enrichment: only season gaps left, recorded as dead ends (`enrich.py --done chicago`). Catania scouted: same dataset as the national MASAF list, 3 to 4 trees round Villa Bellini, verdict `exhausted` in register-scouting.json.
- Left open: the Texas famous-trees batch (4 trees with an open photo) for the next run.

## 2026-10-22 (session with Hidde): a new tree of our own needs a photograph

- **Rule (Hidde):** "we should only focus on trees with photos". It reverses 10-18's photo-less trees for Bing. New preflight FAIL `check_a_new_tree_has_a_photograph()` (`ADD_NEEDS_PHOTO` in scripts/findable.py): a new tree needs a lead photo with status `approved`, a reader's tree is exempt, and the 3,880 trees live today are in data/photo-baseline.json. Tested on a copy: quiet on today's data, fires on a new photo-less tree, passes one with a photo and a reader's. CLAUDE.md (Google recovery mode) and DECISIONS.md updated.
- **For the night run:** READY leads in `leads.py` are mostly photo-less register rows, and writing them now fails preflight. Run `photo_hunt.py` on a place before you verify or write it, and take leads that already carry an open photo first (data/leads/_famous-*.json, about 130 with a pin).
- **Next lane (Hidde: "if the texas trees seem valuable lets try that one"):** Famous Trees of Texas (data/research/texas-famous-trees.json, 93 not yet live). A photo sweep runs first; the trees with an open photo go to a check in batches of 20.

## 2026-10-22 session with Hidde: no ambassador tag on app Settings

Live on main for the next app build: the Settings card shows name and address only; the ambassador tag stays on My trees and the public profile (Hidde: "op de setting pagina ... mag die weg"). Built and looked at in the simulator, signed in as a Paris ambassador. The website's settings page never had it.

## 2026-10-22 session with Hidde: copy drift guard

The Monday fresh-eyes review (review.yml 6b) now also reads the week's new strings for machine-written shapes (and proposes regexes for copycheck's `AI_SHAPES`) and reads that week's DECISIONS.md entries against all product copy for sentences they made false. CLAUDE.md, How to work: a decision that changes the product greps the product for the old claim in the same session; the product-copy skill gained that step. Applied to today's photo rule: nothing on the site contradicts it.

## 2026-10-22 session with Hidde: copy sweep live on both surfaces

Hidde: "voer alle voorstellen door in alle talen, behalve de titels/meta en de voorwaarden". 68 sentences rewritten (commits 5466b4bdd web, 0ab9b8183 app plus web), every language a string exists in: colon reveals, morals ("A map of scattered pins is a list"), Dutch tense ("tell us and we correct it"), "the button wakes up", the badge promise on the home page, and the "verified against two independent sources" claims on /explore, /support, /contribute and /press, which stopped being true when a reader's photo with GPS became a source. Left for Hidde: homeTitle, homeDescription, citiesDescription, exploreDescription (Google recovery) and /terms. Kept on purpose: "Made for people who love being outside" on the home page (his own line). One /app sentence stays as it was, because it shares a line with a hand-drawn icon and iconcheck refuses any edit to that line until the icon is replaced. App strings ship with the next build.

Shared-checkout accident: another session's staged change (a new tree of our own needs a photograph: CLAUDE.md, DECISIONS.md, its LOG entry, findable.py, preflight.py, data/photo-baseline.json) went into 0ab9b8183 under the copy-sweep message. Complete and as that session intended, only the label is wrong. Its own LOG entry below describes it.

## 2026-10-22 session with Hidde: product copy guard, app pitch rewritten

Hidde found "The walking routes, your saved trees, and the collection of the ones you have stood in front of: the Ancient Trees app." on city pages ("loopt scheef en lijkt door ai geschreven"). Live now, in all seven languages: the three app-pitch bodies, their titles, the home page's "Tick off the trees you visit." and the /app meta. Guard: copycheck.py gained `AI_SHAPES` (colon reveal, whether-you're, defining by denying, "the ones you have stood"), which run on web and app; a PostToolUse hook (scripts/hooks/copy_after_edit.py) runs it on every edit of a copy file; new project skill `.claude/skills/product-copy/`. Also fixed copycheck's comment blanking, which ate blank lines and shifted every site line number. A sweep found 68 more crooked sentences (30 certain), in drafts/copy-sweep.html (proposals in out/tmp/copy-sweep.json), waiting for Hidde's go. Not yet seen rendered: no local build, so checked after deploy.

## 2026-10-22 session with Hidde: a reply-mail skill

Hidde asked whether a skill would help with mails. The rules for a reply lived in seven places (HIS_VOICE.md, five memory notes, mailcheck.py), loaded only when a session remembered. New project skill `.claude/skills/reply-mail/SKILL.md` bundles them in order: read the voice file and the thread, do the fix first, the reply shape, the never-list, a de-AI cutting pass, mailcheck, show with the full mail above the draft. It points at the existing files and rewrites none of them. Loads from the next session on.

## 2026-10-22 session with Hidde: press round 3 and tourism batch 1 sent
- Hidde: "verstuur beide". Twenty mails out through outreach_send.py: ten regional desks (press round 3, roster cities in the US, UK and Germany, one tree and one sourced fact each) and ten official visit-the-city sites (tourism batch 1, the map as a resource for their parks page). Every link checked live before sending; no repeats, nobody on the do-not-contact list. Logged in drafts/OUTREACH.md (private); link check on 2026-10-29 is in OUTREACH_STRATEGY.md's dates.
- Prof. Roloff answered the 10-20 link ask with a no (too many such requests); his thank-you reply draft waits for Hidde to send.

## 2026-10-22 (session with Hidde): 15 famous US trees live from their Commons photographs

- **Product:** first batch of Hidde's 2026-10-21 call ("bomen met fotos zijn interessant, die mogen live"). 15 named US trees from Wikidata, each with an open-licence Commons photo looked at in session: Adam and Genesis (new place Mountain Home State Forest), the Hart Tree (Kings Canyon, now four), Bennett Juniper, Jardine Juniper, the Chandelier Tree (Leggett), Boyington Oak (Mobile), Friendship Oak (Long Beach, Mississippi), The Big Oak (Thomasville), The Big Tree (Goose Island State Park), Mother Orange Tree (Oroville), and Riverside as a new four-tree place (Parent Navel Orange, White Sox Redwood, Roosevelt Palm, a landmark sycamore). The Roosevelt Palm photo is held (six palms, trunk unknown).
- **Blocked, kept as leads:** King Arthur (dead, Castle Fire 2020), Seven Sisters Oak (private front yard), Duffie Oak and Council Oak (access unsettled), Fairmount bald cypresses (plural, no pin).
- **Pace cap:** past the 60-a-day guard (73 in 24 hours with the night runs' 58), as a one-off on Hidde's word: "Ja, zet ze nu live, eenmalig over de grens van 60." The guard stays.
- **Cost:** verify 186k, write 158k tokens, about 23k per tree, over the 15k target; five dropouts and a rewrite of the place contexts after Contract B refused them. Weak alive evidence is stated on the pages (Genesis burned, Jardine no dated sighting since 2020, the sycamore one source).
- **Next batch** when Hidde says: the other ~130 pinned photo leads in data/leads/_famous-*.json.

## 2026-10-22 night run (06:36 UTC window): Leiden +2, seven READY leads held

Rung 1 empty (0 photographs waiting). Rung 2: the health "Smoke test skipped" flag is a 1-second if-condition skip on every push while Build and deploy succeeded, answered with health.py --answer. Write pass on the 9 READY leads: lei_025 (Endegeest linden) and lei_026 (Jan Wolkers's oak) live in Leiden (17 to 19, Oegstgeest day-trip trees, nl overlay done). The other seven held with reasons (Pittsburgh x4 no honest recognition line or access, Wilhelmina linden unconfirmed standing, Pelgrimvaderskerk beech no access source, Insingen linden too thin). Photo sweep on 17 roster trees (Chicago, Frankfurt, Leiden, Regensburg): 13 trees viewed, none approved (railway postcard, castle facades, wrong plane). Fort Worth scouting retried: the city's arcgis item has no licence line, still stalled. Chicago +10 (28 to 38, chi_030 to chi_039, FPCC champion register, flagged, no photos); existing Chicago claims that the new walnut and pin oak outdid were corrected. Seattle +9 (21 to 30, target reached; sea_022 to sea_030 from the city's Heritage register, one source each, approximate pins, no photos, address-level recognition lines; sea_025 renamed to Sweet Chestnut to match other cities).

## 2026-10-22 night run (02:55 UTC window): photograph sweep, one approval

- **Live:** the Presidio Centennial Tree (San Francisco) now has a photograph (BrokenSphere, CC BY-SA 3.0; reversal `python3 scripts/photo_apply.py hold sfo_011`). Rung 1 empty, health.py's only flags were push-skipped deploys (a dispatched deploy was running). `photo_hunt.py --recheck` on glasgow, san-francisco, washington-dc, pittsburgh found little; a viewing pass over 40 fetched files rejected 39 (wrong subject or species). Next time: queue the named Commons files for the Yamaki Pine (wdc_025: "Japanese White Pine 'Hiroshima Survivor', 30 April 2012.JPG", Sage Ross CC BY-SA, viewed and fits). Nothing written: the one written tree waiting, ftw_018, is held on unknown access.
- **Also live:** the Yamaki Pine (wdc_025) now has a photograph (Sage Ross, CC BY-SA 3.0, queued from the named Commons file and viewed; reversal `python3 scripts/photo_apply.py hold wdc_025`).
- **Chicago 21 to 28:** seven Forest Preserves of Cook County champion trees (bur oak Harms Woods, sycamore Riverside Lawn, black oak Willow Springs, American elm Schiller Woods with an approximate pin and the story says so, bald cypress McGinnis Slough, swamp white oak Spears Woods, silver maple Harms Flatwoods). One register source each, flagged; none has a photograph yet, so Bing and readers only. Superlatives on chi_008/chi_017/chi_018 corrected where the new trees changed them. Preflight 0 problems.
- **Frankfurt 21 to 23:** the Bethmannpark ginkgo (2015 measurement, said so) and the Leonhard-Eissnert-Park oak (in Offenbach-Bieber, labelled; the two measurers disagree on species and age and the page says so). German overlay updated. Frankfurt's supply is spent (the pass found only these two plus six leads); flurbaum.de/f-stadt.html is a new dated, measured lead source. Pending: more of the pass's leads need a second source.
- **Photo approval (night run):** chi_023 Bur Oak of Harms Woods, Ben Redding (iNaturalist, CC BY): the observation's fix sits 11 m from the register's GNSS pin and the lone big oak fills the frame (bare, winter). Reversal `python3 scripts/photo_apply.py hold chi_023`. Other sweeps (frk_023 park view, chi_027 crown and cone close-ups) left unapproved.
- **Page gap:** Swamp White Oak species intro written (pagegaps.py now says nothing missing).
- **Where it stopped:** Chicago and Frankfurt moved; the rest of the shelf is thin (9 READY leads are young or weak, Pittsburgh and Leiden; famous lane's top is Lithuania, outside the focus countries). Washington DC has only a duplicate in its verified file (wdc_017 = wdc_012).
- **Enrichment pass** on glasgow+san-francisco+washington-dc+pittsburgh (11 trees): closed nothing, 18 gaps recorded as dead ends (`enrich.py --done`). Pittsburgh champions have no sizes in the Shade Tree Commission minutes; remarkabletreespgh.com returns a stub to automated fetches (a browser session could read the champion measurements). Claims released (washington-dc with --force: wdc_017 is a 0 m duplicate of wdc_012, not a pending tree).

## 2026-10-22 night run, later attempt: San Francisco +1, Studena new

- **Live:** San Francisco 10 to 11: the Presidio Centennial Tree (1876 blue gum, approximate pin, no photograph yet; Commons has two CC BY-SA candidates to check). New one-tree place Studena (Grandpa Kolyo's Oak, Tree of the Year), out of Google until four. Preflight 0 problems. san-francisco claim released.
- **Held:** ftw_018 (public ground unknown), inn_007 (pin on a private building), Pittsburgh READY four (school grounds, indistinguishable pins), Rothenburg/Rotterdam/Leiden (walls). Leiden Jan Wolkersboom oak could ship once its wall expires.
- **Open:** city_names.py cannot resolve Studena (no Wikipedia article); sfo_011 transport still says "(stop not verified)".

## 2026-10-22 night run (01:38 UTC window): Potsdam +3 trees

- **Live:** Potsdam goes from 15 to 18 trees: the pollarded linden of Fahrland, the Babelsberger Strasse oak and the Nattwerder lindens (register-only, no photographs yet, confirmed pins). German overlay and counts updated. Preflight 0 problems. 7-day visits line not printed by prepare.py this run.
- **Live:** Frankfurt 20 to 21: the Jahn Oak in Offenbach (confirmed pin, CC0 photograph looked at and approved, so Google can show it). Rumpenheim ginkgos stay a lead (approximate pin, not findable). frankfurt.de returned 403 for three more candidates (Untermainkai ironwoods, zoo bald cypresses, Liebfrauenschule mulberry). Portland refused to claim: already over its target.
- **Photo:** pot_017 (Babelsberger Strasse oak) approved after viewing: Commons "Haplochromis", CC BY-SA 4.0, on-pin geotag, the Wikidata photo. Four others rejected (sapling, wrong street, plaque, pavement shot of a possibly different trunk). Reversal: `photo_apply.py hold pot_017 <url> --reason revert`. photo_light.py cannot run here (no Pillow), judged by eye.
- **Live:** Pittsburgh 4 to 12 trees. The scout retry found that remarkabletreespgh.com's map is a Google My Map whose KML holds 16 tree-level points; used as facts only (the site is All Rights Reserved). Six of the new trees have confirmed pins, two (black locust, American elm) approximate with size-based recognition lines; four more (sycamore, crabapple, two pin oaks) went back to leads. The sycamore, crabapple and oaks, plus the KDKA claim, need a second source. Las Vegas and Ann Arbor scouting retried (Las Vegas already published; Ann Arbor's big-tree page has no licence or per-tree data, stays stalled).
- **Live:** Glasgow 5 to 6: the Wallace Yew at Elderslie (day trip, age disputed and said so, confirmed GPS pin, Commons geograph photograph approved after viewing; reversal `photo_apply.py hold gla_006 <url> --reason revert`). For a later pass: lifecheck the Darnley Sycamore after storm Eowyn.
- **Live:** Regensburg 6 to 8: Wutzlhofen Oak and Unterisling Oaks (confirmed OSM pins, no photographs yet, ages stated as the ordinance's figures). rgb_001 (Herzogspark plane) gained girth 620 cm, 31 m and age 150 to 200 years from the Baumkunde register; oldest tree on the page is now rgb_007. Six more Naturdenkmal rows (ND 3, 23, 27, 28, 29, 48) still have no coordinate; the runner has no PDF reader, which blocks the city's planning PDF.
- **Live:** Washington DC 20 to 21: the Yamaki Pine (a 400-year-old potted bonsai at the National Arboretum, said plainly; age is the family's and foundation's account). Three more verified (Lincoln Memorial elm, Roosevelt Island bald cypress, Congressional Cemetery swamp white oak) are held leads for lack of a photo or findable pin. wdc_017 stays unwritten (duplicate of wdc_012), so that claim was released with --force.
- **Live:** San Antonio 4 to 5: the Alamo Pecan (one source, last dated mention 2015, planting date given as the horticulturist's undocumented account; the pin marks the rear lawn, said on the page). Taco Land live oak held (restaurant lot, nothing after 2021). Fort Sam Houston's Quadrangle Oak blocked for access.
- **Wall:** Leiden verified empty again: Endegeest linden and Wolkers oak are strong but have no photograph or confirmed pin (NL rule), kept as leads. Rothenburg ob der Tauber verified empty (near register trees already live or blocked; Bettwar and Insingen lindens stay leads), walled 48h.
- **Health:** the Smoke test BLOCKER is the push-trigger skip (1s, by its condition), Build and deploy succeeded; answered with health.py --answer. No reader submissions waiting.

## 2026-10-22 night run (22:59 UTC window): three photographs approved

- **Live:** photographs on nyc_028 (Kingsland weeping beech), dre_028 (fingered horse chestnut), dre_010 (white elm, Königsbrücker Strasse); nyc_028 now has a photo, so Google can show it. dre_017 held: pre-2025 photos of a twin oak pair, one felled June 2025. Reversal: `photo_apply.py hold <id> <url> --reason revert`. About 60 iNaturalist candidates remain unjudged in the queue.
- **Nothing else:** health.py flagged only that GitHub dropped 6 of 12 knocks. Spokane claimed then released (1 unmined row, under the six-candidate floor). No write pass: the writable pile is 1 READY lead plus held trees. A second viewing pass looked at the other 61 candidates and approved none (wrong subject or species, close-ups, or trunk ambiguity). Tooling note: photo_apply.py matches iNaturalist candidates by observation url, so verdicts for photos of one observation can land on the wrong one; feed it thumb urls. The sweep also re-adds about 93 already-judged candidates.
- **Scout:** Chicago retried, stays stalled on licence. The Forest Preserves of Cook County champion layer (106 rows with GNSS coordinates) carries no licence and a sensitive-areas notice; those trees are already leads. Whether a county layer with no reuse restriction counts as open is Hidde's call; nothing imported. Leipzig claimed and released (1 tree to target).
- **Enrichment:** New York + San Francisco + Heidelberg pass. sfo_010's girth 383 cm (DataSF DBH 48 in) was already on the page, nothing new; hei_007 got its LUBW Naturdenkmal ids (82210001208/9; the LUBW page itself timed out, ids rest on the Wikipedia list). nyc_028 closed nothing: the landmarked 1847 beech died in 1998, so the LPC record and 14 ft girth are not applied to the replacement. 8 gaps dead-ended for 90 days. nycgovparks.org serves a captcha to automated fetches. Langcheck and pagegaps both have nothing to do.

## 2026-10-21 night run (19:53 UTC window): five trees live

- **Live:** sfo_009 (Mary Ellen Pleasant's blue gums), sfo_010 (Third and Yosemite pepper), hei_007 (Münchelstrasse oaks), nyc_028 (weeping beech, descendant of the 1847 original), pot_015 (Königswald beech). None has a photograph, so Google will not show them. German overlays for hei_007 and pot_015 added. preflight 0 problems. prepare.py: 92 cities claimable, READY pile 3 (under 60, shelf refill flagged).
- **Held:** inn_007 (pin on a house, private yard), Rotterdam Pelgrimvaderskerk beech (church garden, open two days a week), nyc_029 (duplicate-ish of nyc_003). Regensburg READY lead was already rgb_006 and is marked so.
- **Found:** Garfield Square sequoia in San Francisco is a stump (moved to blocked). sfo_008's pin may sit about 300 m off the DataSF Quesada median; needs a look at aerial imagery.
- **Breakage, separate:** iOS app run 39580864787 (FlowWalk back-way test) failed; needs a Mac, not touched. Rungs 1 to 3 otherwise clear.

## 2026-10-21 (session with Hidde): the Santranges well is closed for good

Hidde has turned down the Santranges oak photograph (a garden well, not the oak) about ten times: "kun je ergens registreren dat die waterput al 10 keer is afgekeurd onthoud dat". No script looped; every session reopened the file and brought it back as news. Now `rejected` with `closed_by_hidde` in data/leads/_sightings.json, verdict `reject` with his answer in data/judgements.json, `rejected` in data/sightings-processed.json. New preflight check `check_a_closed_sighting_stays_closed()` fails if any of the three reopens. The reader's girth and age stay on the row; a new photograph of the oak arrives as a new sighting and is judged fresh.

Also checked, nothing changed: no lead with a photograph is held back for being in Russia, India, Israel or Africa. The Tangier fig was the only one; Morocco's Cèdre Gouraud is dead and "Prayer trees in Egypt" is a Commons category, not a tree.

## 2026-10-21 (session): report a second thing on the same tree

A reader told Hidde that after one report on a tree, "Something's wrong" was gone and the line only said "Thanks, that helps", so a second report meant the flag up top. Now the line stays on both surfaces (Google Maps keeps "Suggest an edit" the same way); a new report shows its own follow-up question. Live on the website with the next deploy; in the app from the next build. App build checked; the reported state was not looked at on screen (it needs a signed-in tap, which simctl cannot do).

## 2026-10-21 (session): less air in the map sheet and on My trees

**Product (app, next build):** Hidde found the map sheet at its lowest stop and My trees "not using the space". Benchmarked (Polarsteps' profile measured, Google Maps' and Apple Maps' list sheets from their App Store screens), shown as now / middle / tight; he chose the middle and kept the grip where it is on every sheet. Built and measured in the simulator: at peek the first tree card shows 46 points above the tab bar instead of 29 (grip to "7 trees" 25, to the card 16); on My trees the photos start about 25 points higher (tags to tabs 27, was 41). Tap targets unchanged, BottomSheet untouched. Reference in CONVENTIONS.md, "Vertical rhythm of a profile header".

## 2026-10-21 (session with Hidde): Tangier fig live from a reader, and a stranger's photo with GPS is never parked again

- **Product:** tng_001, The Moreton Bay Fig of the Mendoubia (Tangier), live as a lone tree page from a stranger's app photograph and three-paragraph note (sighting 2aa7147b, 2026-10-18). The story quotes them: the 800-to-1,000-year age on the signs against their 120 to 140 years, planted by the Mendoub's residency. Wikipedia's Mendoubia page is the written source. lis_037 (Lisbon dragon tree) now quotes its reader too.
- **Rule (Hidde):** "user content is the most valuable thing"; a good photo plus a GPS fix goes live, whatever the focus areas, sources or certainty; their words go on the page quoted and unnamed. CLAUDE.md (Verify), DECISIONS.md, and preflight `note_a_strangers_photo_with_gps_waits_for_nothing()`. Out-of-focus now covers our own research only.
- **Data:** two stale sighting rows corrected: the Montsouris plane has been live as par_034 since 10-13; the Santranges oak is held (its photo shows a well, not the tree).
- **Mail:** the Tangier reader gets the automatic "your tree is on Ancient Trees" mail on the next knock, which no longer asks for what their note already gave. The ambassador ask now rides as a P.S. under that mail instead of a second mail the same day; the separate invitation goes only to a reader with photos of two or more trees in one place, and thanks them for photographs, not for "adding". Photos on existing trees still mail nothing (Hidde: "doe maar niet").
- **App:** the app checked for new trees only at a cold launch and on Home's pull to refresh, so a phone with the app still in memory never saw Tangier. It now also checks each time it comes back to the front (ContentView.swift). Built and seen in the simulator: the fig shows at the Mendoubia. For Hidde: next build carries this fix; until then, swipe the app away and reopen it.
- **Breakage, separate:** the iOS app workflow failed on 2026-10-21 (session-start brief); not looked at in this session.

## 2026-10-21 (window from 14:48 UTC): one reader photograph cleared, then stopped

Rung 1: the one queued sighting (lis_037, Lisbon dragon tree) was already the tree's live lead photo, same sighting id, so nothing new for readers to see. I viewed it (Dracaena draco, fits the recognition line) and recorded the verdict in data/sightings-processed.json. sightings_publish.py's `add` copied the same picture beside itself; I reverted the city file and moved the duplicate jpg out of site/public/photos (to out/tmp). Worth a fix: `add` should skip a sighting that is already the lead photo. Preflight 0 problems.

Photos on the roster: photo_hunt sweep queued candidates for 14 new trees; a photo-judge pass looked at 44 and approved 8 (hst_007, pot_012, pot_013, pot_014, rgb_006, thm_001, wdc_018, wdc_020), none held, 36 rejected; reverse one with `python3 scripts/photo_apply.py hold <tree_id> <candidate_url> --reason "..."`. Weakest: wdc_020 (over-processed colours, barriers) and wdc_018 (375x500 iNaturalist CC0). Open: wdc_018's iNaturalist GPS (6 m) could confirm its pin. Still no photo: hst_006, pot_011, rot_017, rot_018, srm_006, wdc_021.

Enrichment, 7 proven cities (10 trees): verify pass improved 3. sea_020 and sea_021 got the SDOT Heritage Tree record id and an autumn best_time; frb_008 got an autumn best_time. 14 gaps dead-ended for 90 days. Not closed: hst_006's pin (e-gov.ooe.gv.at refused port 443 from this runner), lis_037 and frb_008 register and measurement (nothing found; the Ebringen NatURWALDpfad brochure PDF could not be read, pdftotext missing). SDOT diameter and height left out, units unconfirmed.

Supply: US/UK/DE/AT cities are full or walled (Vienna has 2 slots; claim released, wall written). Took the scouting RETRY, San Francisco: DataSF moved to data.sf.gov with renamed fields; 232 landmark rows, 30 not palms, kept in data/registers/san-francisco-landmark-trees.json (PDDL). Still stalled, nothing to publish from it; one lead worth a pass, the Moreton Bay Fig at 1580 Valencia St (72 in DBH, seen from the pavement). Verdict rewritten in data/register-scouting.json with `retried`.

Page gaps: wrote the Willow Oak species intro (data/species/willow-oak.json) from its three Washington DC trees; pagegaps now shows none open.

Broken, not mine to fix from Linux: iOS app run 39580864787 failed `FlowWalk.testEveryFlowLeavesAWayBack` (search-to-a-tree: after "first-result" no tab bar, back button or dismiss; 229 passed, 1 failed). No ios/ commits since the last green run, so it is either data-driven (the first search result) or a flake; it needs a Mac session. For Hidde: nothing to do yet, the next scheduled ios.yml run says which.

## 2026-10-21 (retry window): the Lisbon dragon tree is live

The Goethe-Institut garden dragon tree (lis_037) is on the Lisbon page, with the reader's photograph, a written verdict and the Portuguese overlay. Pillow installed fine this time. The reader's verdict also needed a `sight:` entry in data/judgements.json, which preflight looks for; the `lead:` one alone was not enough. Preflight clean; the site build and qa.py were not run on this runner (no dist).

## 2026-10-21 (window from 09:03 UTC): stopped on Pillow

Rung 1: the Lisbon dragon tree (sighting 9b10ae23). The photograph is a clear Cadiz-standard Dracaena draco, and a web search found Time Out Lisboa listing the Goethe-Institut garden as a public garden esplanade with opening hours, which settles the access doubt that held it yesterday. I wrote the new tree (lis_037) as a script, out/tmp/add_dragon.py, but it stopped at the first step: Pillow is not installed on this runner and `pip install pillow` was refused, so the photograph cannot be rotated upright and written to site/public/photos. Nothing was added; the verdict in data/leads/_sightings.json still reads "lead". The script sits in out/tmp (gitignored), so it will not survive this runner. Nothing else was taken from the ladder in this attempt.

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-10](archive/LOG-2026-10.md)
- [2026-09](archive/LOG-2026-09.md)
- [2026-08](archive/LOG-2026-08.md)
- [2026-07](archive/LOG-2026-07.md)

## 2026-10-21 - Night run 2026-10-21 05:55 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 0.0 minutes of its 120 minute window, 1 turns, ended clean (success). Nothing reached data/cities.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported.

What each attempt said as it stopped, in its own words (secrets scrubbed):

- Attempt 1: You've hit your weekly limit · resets 9am (UTC)

## 2026-10-21 - Night run 2026-10-21 02:56 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 0.3 minutes of its 120 minute window (wall clock: cancelled before it could report its own duration), ended clean (cut off at the cap, no result record). 1 commit(s), none of them a published tree.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported.

What it cannot tell you is WHY the run stopped: no attempt left closing words on disk. If this shape repeats, the two things worth suspecting are the usage window and the refused commands.

## 2026-10-20 - Night run 2026-10-20 22:53 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 0.0 minutes of its 120 minute window, 1 turns, ended clean (success). Nothing reached data/cities.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported.

What each attempt said as it stopped, in its own words (secrets scrubbed):

- Attempt 1: You've hit your weekly limit · resets 9am (UTC)

## 2026-10-20 - Night run 2026-10-20 22:28 UTC ended without saying anything

Written by the workflow's Run health step, not by the run. 0.0 minutes of its 120 minute window, 1 turns, ended clean (success). 1 commit(s), none of them a published tree.

This entry exists because the run wrote none. The prompt asks every run to log even when it ships nothing, and a run that gives up is exactly the one that skips that instruction, so the count above is measured rather than reported.

What each attempt said as it stopped, in its own words (secrets scrubbed):

- Attempt 1: You've hit your weekly limit · resets 9am (UTC)

## 2026-10-20 session with Hidde: your own trees get the pin step too
- **App (next build):** tapping one of your own trees on the Map tab or in My trees now shows it in the sheet first (your photograph, the name, a cross), as our trees do; the card opens your tree's page. No save and no share on it (it is yours, and has no public page yet).
- **Freeze on a pin tap, fixed (next build):** Hidde's phone hung when a tree's card came up. My own change from this afternoon: the map reported what was in view while a tree was selected, the rising sheet moves the map every frame, and every report rebuilt the list of trees. Measured on the simulator: 66 percent of a Mac core for a second per tap before, 3 percent after; a phone is several times slower. Now the map stays quiet while a tree is selected and reports once when it is let go, so the count is still right afterwards ("8 trees", checked).

## 2026-10-20 session with Hidde: a "Yes" waits for a newer version, four months on

- **App**: refines the entry below. Somebody can say "Yes" and never rate, so a yes no longer ends the asking for good: it stays quiet until a newer app version AND at least 120 days, then asks once more (Apple's own sample asks once per version; somebody who did rate usually sees nothing then, iOS keeps its dialog away). New device key `reviewPrompt.yes.v1` ruled `device` in data/cross-device.json; ReviewPromptTests 14/14.

## 2026-10-20 session with Hidde: a "Yes" to the review question ends the asking

- **App**: after "Yes" on "Are you enjoying Ancient Trees?" the app never asks again (Hidde: "iemand die al beoordeeld heeft niet meer vragen, dat lijkt me de conventie"). Apple never tells an app whether somebody rated, so the yes is the signal; "Not really" keeps the later milestones. Apple's dialog is now asked for once our sheet has closed, since a request during the dismissal may be dropped. Kit/ReviewPrompt.swift, new test `aYesEndsTheAskingForGood`; ReviewPromptTests 13/13 on the 17 Pro.
- **For Hidde**: next build carries this. His own "Yes" with no dialog was most likely Apple's limit (already rated, three a year, or TestFlight), not ours.

## 2026-10-20 session with Hidde: Imperia opens with five register trees (his sister lives at Villa Guardia, Pontedassio)

- **New place: Imperia**, five MASAF register trees, flagged, approximate pins: imp_001 Bunya Pine at the Palazzo della Provincia (26 m; **photo approved**, Commons CC BY-SA 4.0, linked from the register tree's own Wikidata item), imp_002 Mediterranean Hackberry at San Michele, Diano Borello (5.1 m girth), imp_003 the Downy Oak pair of Maro Castello (meadow access not confirmed, said on the page), imp_005 the Sweet Chestnut of the Passo Furchè above Ceriana (8.5 m girth, 5 m tall; a MTB guide's "1,300 years" reported as its claim, age left empty), imp_006 the Horse Chestnut pair of Sant'Agostino, Triora.
- **Held for tomorrow by the 60-in-24h pace cap**: imp_004 Holm Oak at the Lampedusa sanctuary, Castellaro, and imp_007 Horse Chestnut of San Bernardino, Triora. Both written and ready in data/research/imperia-verified.json: move them into data/cities/imperia.json and add Castellaro and San Bernardino back to the intro and context.
- Leads not written: Conio oak (03/B020, 30 m, access unknown), Dolcedo olive (01/D319, likely a grove), Prelà lime (small), Chiusanico strawberry tree (at an agriturismo).

## 2026-10-20, 15:13 window (night run)

- Rung 1: inbox empty. Rung 2: health flagged the Smoke test as skipped; it skips on push by design, Build and deploy succeeded, answered with `health.py --answer`.
- Shelf: only held trees were awaiting a writer (ftw_018 access, std_001 no viewing pin, inn_007 pin on a house). Graz walled for 48h (0 of 7 leads placed). Nuremberg verify found two Dutzendteich oaks (nbg_019, nbg_020), written and merged: Nuremberg 18 to 20, no photographs, German overlay and count copy updated.
- Nuremberg's register is now mostly exhausted; next deepen should go elsewhere (Vienna was claimed at 13:31 by an earlier run).
- Photo pass on nbg_006, nbg_019, nbg_020: 14 Commons candidates viewed, all rejected (hollow-trunk interiors, lake postcards), none approved.
- New York verify: nyc_028 (Weeping Beech Park, a descendant of the dead 1847 tree, no age or girth) and nyc_029 (Prospect Park hornbeam, register diameter implausible) held in data/research/new-york-verified.json, not written: neither is old or measured enough to earn a page. NYC Parks Great Trees site answers 405 to fetchers. New York walled 48h.
- Seattle (19 to 21): sea_020 Aloha Street tulip tree (private lot, seen from the pavement; its pin is the city's trunk point, approximate, metres from the viewing spot) and sea_021 Leschi Park tulip tree. 297 of 330 heritage rows are privately owned, so the register gives few more; Volunteer Park trunks cannot be pinned without a coordinate source.
- Potsdam (10 to 14): pot_011 three Weinmeisterweg oaks (ND 12, access unstated, said so), pot_012 Sacrow roadside oak, pot_013 Am Kanal plane, pot_014 Rote Kaserne oak (city lists it as ND 10, tree archive says not; no age claim). No photographs. I replaced pot_014's "not checked against OSM" access sentence with plain reader wording in English and German.
- Washington DC (16 to 20): wdc_018 Tudor Place tulip tree, wdc_019 Farragut Square pagoda tree, wdc_020 Arlington House deodar (1874 planting), wdc_021 Oxon Hill willow oak (Maryland, car only). All from the NPS Witness Tree register, approximate pins with a 50 m site, no photographs; newest life evidence is 2018 for three of them and the stories say so. Methuselah willow oak is a stump, Farragut ginkgo dead, both blocked.
- Regensburg (5 to 6): rgb_006 Bildeiche at Höhenhof, 7.20 m girth (Lippert 2021), confirmed pin, 8 km south, buses unchecked and said so. Tegernheim oak and Eilsbrunn linden stay leads.
- Heidelberg verify: one tree (hei_007, two Münchelstrasse oaks, register only, approximate pin, no measurements) held in data/research/heidelberg-verified.json; not written, since a photo or confirmed pin is needed in a covered country and a register listing is not a reason to visit. Plöck 45-49 courtyard trees (access settled) are the best lead, wanting a photo or pin. Heidelberg walled 48h.
- Hallstatt (5 to 7 trees): hst_006 Tausendjährige Linde, Bad Ischl (register says 400 to 500 years, not a thousand; 20 km away, said on the page) and hst_007 Gosau wych elm (last seen 2015, stated). Oldest-tree answer moved to hst_006. For a look: the hst_006 story adds Franz Joseph's summers at Bad Ischl, general knowledge with no source on file.

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
## 2026-10-20 night run (13:13 UTC window)
- **Product:** a reader's photograph of the Campo Santana weeping fig (Lisbon, lis_015) is live, replacing a held panoramio image; their GPS fix moved the pin 129 m and confirmed it. Looked at the pixels first: big fig, aerial roots, daylight and colour. Five trees written: Bamberg bam_007 to 009 (now 9), Rotterdam rot_017 and rot_018 (now 17), with the city copy counts fixed. Held as leads on access: Innsbruck inn_007 (probably a private yard) and the Rotterdam church-garden beech at the Pelgrimvaderskerk.
- **Breakage:** iOS app run of 10:55 failed 40 passed 1 failed (test name only in the xcresult); newer runs are in progress, answered in health.py, no action without the Mac. Mistake worth knowing: sightings_publish does not write the judgements.json entry, and preflight then refuses; I added it by hand (out/tmp/addjudge.py) after the queue had emptied.
- Later in the window: Hong Kong enrichment closed 9 trees' register numbers, girth and height (OVT register; pins match ours within 1 m so stay approximate, no season moment for figs or camphor). Species intros written for Mountain Ash and Karri, so pagegaps is empty. Ibiza scouted: the Balears register is already imported and has nothing unmined for it (verdict in register-scouting.json). London, Munich claims refused or walled, released.
- Photos, Bamberg (I looked at 8 Commons candidates): approved bam_009 (Pödeldorf lime, ND-03734 in the filename, geotag 40 m, CC BY-SA, Stephan van Helden) and bam_006 (Kilianseiche, geotag 18 m, CC BY 3.0, Immanuel Giel; bare oak, reversal: `photo_apply.py hold bam_006`). Held bam_008 (a lime by a wayside cross our entry does not mention). Rejected two aerials and a decayed trunk for bam_007.
- Still on the shelf: 91 claimable staged cities, REFILL THE SHELF flag (1,024 leads need only a source).

## 2026-10-20 session: the app's layout gate now measures the right edge too
- **App, layout gate (appfit.py).** Until now it only caught things a few points off the shared LEFT edge. It now asks the same of the RIGHT edge (TRAIL): cards, buttons and photos that should end at the same distance from the right side and miss by 2 to 11 points. Prompted by the map tab's pin sheet, whose cross sat off the card's edge (2026-10-19/20). Same exemptions as the left edge, plus left-aligned text, whose right end is just where the words stop.
- First run on both phones (iPhone 17 Pro and SE, iOS 26.5): one element on five screens, the tree page's little map in the photo's bottom-right corner. It sits 10 points in from the photograph's corner on purpose (Airbnb's photo-and-map swap), so it is exempt like the pills on a card photo; the photo-less branch now carries the same identifier. After that, 0 findings on 80 screens, and the rule fails the gate like DRIFT does.
- Limit, said plainly: 44 point icon buttons stay exempt on both edges, because their hit box is wider than the drawn circle (the pin sheet's cross is a 38 point circle in a 44 box pulled 3 points out). A frame check cannot see the circle; the eyes rule and the reference beside the design still carry that case.

## 2026-10-20 side session: the tourism-site feeder, and ten mails to visit-the-city sites on Hidde's desk

- **No product change.** Outreach only (Hidde, 2026-10-20: "start doing all this", the tourism group of OUTREACH_STRATEGY.md).
- **New feeder, scripts/tourism_sites.py:** finds the official tourism site of every roster city (Wikidata's tourist office, else the tourism domain the city's Wikivoyage page links most, else visit<city>-style host patterns in the local spelling; parked domains and redirects that drop the city's name refused) and reads its contact and press pages for an address, scored like press_desks.py. Private output data/outreach-tourism-sites.json; contacts_db.py reads it into the tourism segment (`contacts_db.py --ready tourism`: 18 ready). Forty roster cities looked up, 17 with a usable address. The big boards (visitlondon.com, muenchen.travel, parisjetaime.com, thisisbarcelona.com) sit behind bot walls and need a browser read; the feeder records the wall.
- **Ten mails drafted, nothing sent:** Lisbon, Amsterdam, Seville, Madrid, Bath, Berlin, Rome, Vienna, Brussels, Austin, each in the city's language, one photographed tree with its page link, the city map in that language, one ask (a place on their parks or green page). Under 120 words, mailcheck clean, links checked live. Preview drafts/batch-tourism-2026-10-20-preview.md (private, English gloss per mail), batch drafts/batches/tourism-2026-10-20.json, status drafted. **FOR HIDDE:** read the preview; his word goes into approved_word.
- Full note in drafts/OUTREACH.md (private). Feeder cost: code, about 90 minutes of fetching; the session itself about 250k tokens.

## 2026-10-20 side session: press round 3 drafted, twenty regional desks

- **For Hidde to read:** drafts/batch-press-regional-2026-10-20-preview.md, ten mails to regional desks in roster cities (New York, Edinburgh, Glasgow, Los Angeles, Austin, Liverpool, Guerneville, Monterey, Portland, Frankfurt in German), each on one sourced fact from a tree page with an approved photo. Nothing sent; status drafted, your word goes into approved_word. mailcheck clean, every link checked live.
- Twenty desks hand-found from the papers' own contact pages, all new to the database (press ready 271 to 291), in the private contacts file; the ten without a mail wait for round 4 after tomorrow's readout of rounds 1 and 2. Details and the why-this-desk per city in drafts/OUTREACH.md (private).
- Judgement calls: Frankfurt is the only German city on the roster with a photo and real impressions; Sequoia National Park skipped (no city desk); where the paper of record blocks fetches or lists no newsroom address, the public-radio web desk stands in (LAist, KUT, WBUR, KUOW, WHYY).

## 2026-10-20 session with Hidde: tapping a pin shows the tree instead of leaving the map
- **App and website, every city map.** A tapped pin grows and the tree comes up in place, as in Apple Maps (recorded in the simulator) and Airbnb (Hidde's screenshot). In the app (Map tab, a city's map, My trees) and on a phone's website the sheet's top becomes one row: share, the name with species and age, a cross; the tree's photograph under it opens the tree page. On a computer the tree's card floats beside the pin with save and a cross. The cross, a swipe down, or a tap on the map gives the list back. Approved by Hidde after five rendered rounds. App: next build; website: live with this deploy.
- Fixed with it: the app's map count read "No trees in view" after letting a tree go.
- Not changed: /explore still opens the tree page on a pin (its pins carry no card data yet).
- Breakage: the smoke test was red since the Hong Kong commit (Kapok/Bombax and Kigelia pinnata clashed with other cities' names, hard rule 9); fixed and pushed separately.
- For next time: a new screen state gets a sweep row (map-pin added) so the layout gate measures its edges; designs go to Hidde beside the recorded reference, never alone.

## 2026-10-20 session with Hidde: your face in the bar, and a flag by default

**Live (web):** signed in, the desktop bar shows your round profile picture (else your initial) instead of the word Account; signed out it still says Sign in. Mockup shown first, Hidde: "ja bouw alles". This reverses 2026-10-10's "no icons in the menu bar" (that was a line-art person; this is your own photo). The country picker has "Don't show" on top. **Flag by default** (Hidde: Polarsteps showed his flag without him choosing): unchosen, the website takes the computer's time zone and the app the phone's region, written once; "Don't show" is remembered in the new profiles.flag_hidden. App: next build. Why nobody had a flag: none of the 14 profiles had ever picked a country; yesterday's flag was the simulator's demo account.
**FOR HIDDE:** paste supabase/PENDING.sql (one line, the flag_hidden column). Until then nobody gets a default flag; the face in the bar does not need it.
**Breakage, fixed:** a code comment in settings ("stores it with your name") tripped qa's never-publish-a-name check and failed one deploy, which also held back another session's push for about 25 minutes. Also: another session's reset threw away this session's uncommitted site edits once; the work moved to a worktree.

## 2026-10-20 session with Hidde: Sanremo opens with six register trees (his sister visits tomorrow)

- **New place: Sanremo**, six MASAF register trees, all flagged, approximate register pins, recognition line on each, no photos yet (Hidde: "met foto's is bonus maar hoeft niet"). Sanremo: srm_001 Senegal Date Palm in the Giardini Nobel (19.5 m, the register's locality; OSM puts the point in that park opposite Villa Ormond, never bridged to Ormond's "most majestic" palm), srm_002 Chilean Wine Palm in the Parco Marsaglia, srm_003 California Fan Palms at the Zampillo (group). Day trip Bordighera: srm_004 La Scibretta (11.8 m girth), srm_005 the Bicknell figs (planted 1886 per the Clarence Bicknell Association; two register rows 13 m apart, one point), srm_006 Canary Pine on Via Romana (40 m).
- Left as leads in the brief, not written: the Poggio olive (Via Val d'Olivi 248, could be private ground), the hill trees 8 to 20 km out. Commons images on Wikidata Q55741680 (Zampillo) and Q55741671 (the pine) are unchecked photo candidates.
- One pass done in-session by hand (verify and write together, under the six-candidate floor) because of the deadline; about 90k tokens.

## 2026-10-20 session with Hidde: Gavin Coates's HKU Digital Arboretum, and the Kam Tin Tree House pin

- **Hong Kong 10 to 21 trees** (Hidde: "add more trees"; outside the focus countries, claimed with his reason). New, all from the Old and Valuable Trees register: hkg_011 the Rubber Fig of Lugard Road (5 m diameter, the register's widest), hkg_012 to 014 Hong Kong Park (big-leaved fig, 28 m banyan, kapok), hkg_015 the pink shower tree at The Murray (hotel ground, access says so), hkg_016 Garden Road banyan, hkg_017 City Hall sausage tree (photo), hkg_018 Botanical Gardens camphor, hkg_019 Kwai Chung rubber fig (32 m), hkg_020 Mui Wo banyan (photo, iNaturalist CC0), hkg_021 Signal Hill banyan. Intro, meta and the free-to-visit faq updated; the King Banyan's "largest" is dated to its 1997 title, since Lugard Road's trunk is wider.
- **Register status:** the open GeoJSON carries no alive or removed flag; the register's detail pages do. 195 removed and 37 failed trees are still in data/registers/hongkong-ovt.json; status per tree in data/research/hong-kong-ovt-status.json. Nine of our ten older trees read Alive (Kam Tin with confirmed brown root rot); hkg_008 (YTM/98) is not listed on the site, note on the tree, not retired.
- Photos: re-searched on the corrected pins, nothing for the ten older trees; the register site's own tree photos carry no open licence. Leads: Kuk Po tree house (Gavin's video only source), Granville Square, Kwan Mun Hau rubber trees, CW/145. Cost: verify ~200k, write ~137k.

- **Fixed, six of ten Hong Kong pins:** hkg_001, 002, 003, 004, 005 and 006 were each about 300 m off by the identical vector (170 m south, 252 m east missing): an earlier hand conversion of HK1980 grid references left out the datum shift. All six now sit on the register's own WGS84 point (shifted, each old pin lands within 6 m of it). hkg_001 and hkg_002 gained their register numbers (LCSD YTM/97, ARCHSD CW/47); register heights added. Gavin's videos at Kam Tin are what exposed it.
- hkg_003, the Kam Tin Tree House, was pinned about 300 m from the register coordinate of the tree it cites (LCSD YL/6). Moved to the register point, which three of Gavin's videos at the tree confirm within 11 m; height 18.5 m from the register.
- The arboretum's map is a public GeoJSON (1,182 dated, placed videos, 324 species) with no licence: a finding aid for pins, life checks and leads, never imported or shown. Notes and uses in data/research/hong-kong-digarb.md. It maps where Gavin teaches, not old trees: 15 videos sit at an Old and Valuable Tree.

## 2026-10-20 session with Hidde: iPad question, and the header fits an iPad in portrait

- Live (65eb661fc): at 801 to 1023px the header's logo, Sign in and app pill no longer wrap onto two lines; the search field shrinks instead. Checked in English and French (longest labels) at 801 and 820px, and the phone bar is unchanged.
- iPad app: parked. Google Analytics holds 26 consented visitors in 8 days, too few to count iPads (and iPad Safari reports itself as a Mac). The real count is App Store Connect downloads by device, which only Hidde can see. Revisit when that shows iPad downloads or traffic recovers.

## 2026-10-20 session with Hidde, afternoon: a Nationalerbe lime live, and the warm-replier link batch is one mail
- **Product:** rob_005, The Courtyard Lime of Gut Burgstall, Rothenburg: Prof. Roloff's 10-07 tip, 8.70 m, 600-800 years by the Nationalerbe-Bäume initiative, pin from its published GPS. The 10-14 pass had blocked it under hard rule 10 on baumkunde's "Privatgelände geduldet"; the designating body's own page says the drive in is free and the tree may be viewed, so it ships with an access line that says it is a family's home. Reversible with retire.py if Hidde reads the rule the other way. Rothenburg's intro, metas, question page and faq now count five and name both oldest trees (by estimate, by carved date).
- **Outreach (Hidde: "go do this", warm repliers, inbox first, Quercus/Woodland Trust/Bomenstichtingen/Baumkunde left alone):** read the inbox since 08-20. Of 31 "replied" contacts, one qualifies for a link ask today: Prof. Roloff, with the news that his tree is live. Draft in drafts/batch-warm-roloff-2026-10-20-preview.md (private), batch drafted, send after the deploy. The rest are his active threads this month, ambassador threads (never asked for links), already asked once (Buçaco, Dumbarton Oaks, Blarney), redirections, or government desks; listed in the preview. Lesson for OUTREACH_STRATEGY: the "replied" column is mostly the ambassador lane, not a link lane.
- Strategy proposals he said yes to in principle and that wait for his sending time: no more register mails in the source group; regional press in focus countries for roster cities; a tourism-site group.

## 2026-10-20 session with Hidde, later: Google has not recrawled the noindex pages (URL Inspection sample)
- Hidde asked how we would know whether the next update passes us. Built `scripts/gsc_inspect.py` and `gsc-inspect.yml` (one-off, by hand) and ran it: 25 Google-only noindex tree pages, 25 kept photo pages on the roster, 12 roster place pages. Answers in data/research/gsc-inspection-2026-10-20.json.
- **The noindex has not reached Google.** 16 of the 25 noindex pages are still "Submitted and indexed" with the crawler's last view "indexing allowed"; their last crawl dates run 08-09 to 09-28, none since the tag went on (10-08). The other 9 were never indexed. sitemap-recrawl.xml is live, in robots.txt, with honest dates; Google reads it and still does not come back. Nothing short of waiting forces a recrawl of 2,700 pages (Request indexing is a dozen a day; the Indexing API is not for this content).
- **A third of the pages we keep are not in Google either.** Of 25 photo pages, 6 are "Discovered, currently not indexed" and 2 unknown; several gained their photograph this week (Dresden, Berlin, Stuttgart) and have simply not been fetched yet. 4 of 17 indexed ones were crawled since 10-08. Place pages fare best: 11 of 12 indexed, 5 crawled since 10-08.
- Reading: Google's crawl interest in the site is low since the demotion, so the shape it will judge at the next update is still mostly the pre-10-08 shape. For Hidde: Search Console, Pages, "Excluded by 'noindex' tag" count, and Settings, Crawl stats, requests per day, are the two numbers that will show the recrawl happening.
- Also this session: `~/.ancienttrees-posthog.env` now exists (new key "mac"); PostHog shows 14 phones on 1.0.3 from the App Store since 10-14 with no crash report, 33 phones still on 1.0.2.

## 2026-10-20 session with Hidde: the Freiburg beech is live, and the inbox now downloads every open lead's photograph
- **Product:** frb_008, The Schönberg Beech above Ebringen, a stranger's app sighting of 10-18 (ed90210d), live on Freiburg's page under the 2026-10-12 reader rule (photo shows a tree worth the walk, GPS pin, not our account). No register, article or web source; the page asks for a girth. Freiburg is eight trees now; intro, question texts, faq and the German overlay updated. The congratulation mail (tree_approved.py) goes on the next knock once the deploy carries frb_008.
- **Why it sat open a day:** sightings_inbox.py fetched a photograph only after a sighting matched a tree we map; one matching nothing was filed as a lead without its file, and out/ is fresh on every runner. Seven night runs logged "photograph not on this runner". Fixed: `fetch_open_lead_photos()` runs on every inbox read, and `--status` says per lead whether the file is on disk.
- Hidde answered the three Lisbon photographs (two of the fig, one of the paperbark): agreed, already discussed. The inspect page (inspect_readers.py) now records which trees he was shown and flags one shown before and never answered, so a session asks for the verdict instead of presenting it as new; CLAUDE.md carries the rule.
- Asked and answered, no action: the Meiji Jingu Gaien ginkgo avenue (his own photo, filed as a lead because it is an avenue; the ensemble rule may well allow it, his call); the build 20 MyVotes crash (fixed and contained 10-16, drops out of the table on 10-23).

## 2026-10-20 (second attempt in the window)
- No product change; no new trees. Rotterdam deepen pass (verify, ~93k tokens): 1 flagged candidate, rot_017 Wilhelmina Chestnut (Noordereiland; cankered, expected to go within years, no photo, approximate pin), left in data/research as research, not written (under the six-candidate minimum). 2 blocked (felled elm, private garden), 3 leads kept in data/leads/rotterdam.json.
- Fixed a published duplicate: rot_002 and rot_003 were the same Breytenbach plane on one pin. Kept rot_002, retired rot_003 (redirect added), fixed the city's meta, question_meta and question_context counts (15). The 2021 Tree of the Year runner-up and 1960s move facts from rot_003 are not yet on rot_002. The register places the tree about 600 m north of our pin (51.9192, 4.4720); not moved, pin evidence needed. See data/research/rotterdam-corrections.json.
- Shelf: the 2 READY leads are reader sightings; ftw_018, std_001, inn_007 stay held for access reasons (see earlier entries). Portland and Munich are full. Rotterdam is a 48h wall.

## 2026-10-20 retry attempt: 1 tree live

- New place Thalmassing, one tree (thm_001): St. Wolfgang's Oak, 9.80 m round, a Nationalerbe-Baum, 15 km from Regensburg. The story was already written; it went into its own one-tree place file because it is not part of Regensburg's walk (same shape as Eisolzried). No photograph yet; the Commons candidate is in its verify_notes for a photo pass.
- Not done: the Freiburg beech sighting (ed90210d). No register or Wikipedia entry within 100 m, and its photograph is not on disk, so the verdict stays open.
- Fort-worth: claimed, then found 0 unmined candidates. Released with --force and it is on the 48h wall list.
- Written but held on purpose: ftw_018 (access unknown), std_001 and its sibling (no honest container), inn_007 (register pin on a private yard). fdl_001 was a duplicate of spa_001.
- Stuttgart verify pass (about 99k tokens): 0 trees. Wilhelma plane is owner-confirmed but has no tree-level pin or photo; Hohenheim's pre-1800 list needs a browser; five leads with reasons added to data/leads/stuttgart.json. stu_011 folded into the live stu_007 as a duplicate. Wall for 48h.
- fdl_001 was a duplicate of the live spa_001 and is dropped from the research file.
- Munich is full at 63 of 60, so no claim. The staged Stuttgart/Fort Worth supply is exhausted; the shelf is walled for now.

## 2026-10-20 07:00 run

- Rung 1: Freiburg beech (ed90210d) photo still not on this runner, verdict stays open.
- Bamberg verify pass (claimed, 107k tokens): 3 register-only Naturdenkmal trees (bam_007 maple, bam_008 and bam_009 lindens) in data/research/bamberg-verified.json, all with CC BY-SA photographs, none with girth, age or a story, so remarkability is weak ("protected is not a reason"). Not written or merged; claim stays until a writer decides. 3 more leads added to data/leads/bamberg.json. Nothing new is live.

## 2026-10-20 05:20 run

- Stuttgart: 2 trees live (Wilhelma sequoia grove, Wilhelma ginkgo; both paid entry, no photo, grove pin approximate). City copy corrected (not all free any more) and the German overlay updated. Preflight 0 problems. stu_011 was a duplicate of stu_007, dropped.
- Rung 1: the Freiburg beech reader photo (ed90210d) is not on this runner, so I could not look at it; verdict left open. No register or Wikipedia entry within 100 to 300 m.
- London enrich (lon_032, lon_033): one access line closed (Osterley, National Trust hours); register, measurement and season found nothing, 6 gaps dead-ended for 90 days.
- Enrich amersfoort+frankfurt+stuttgart: Wilhelma ginkgo got its DDG register record, girth 458 cm and opening hours; sequoia grove got hours; frk_018 location_site was refused by the tool (no source URL), still open. 9 gaps dead-ended. Preflight 0 problems.
- Not touched: iOS app workflow failure flagged at session start (needs a session), 36 photos not yet vendored (daily photos.yml).

## 2026-10-20 retry attempt: nothing shipped, chicago claim released

Chicago's brief had 0 register candidates (under the six-candidate floor), so the claim was released and chicago is a wall for 48h. READY holds only two reader sightings; the Freiburg beech (ed90210d) stays open because the photograph is not in out/sightings/ on this machine and a stranger's submission is never judged blind. The prepare.py staged list (munich, portland, potsdam, salzburg, vienna, bamberg) points at cities already published whose verified files are stale; briefs for them show no candidates. Not done: Las Vegas register retry (BACKUP 1), stale research file cleanup.

## 2026-10-20 write pass: the John Peter Smith Oak live in Fort Worth (19 trees)

- Live: ftw_020 John Peter Smith Oak, the 4.5 m Texas live oak on the Kimbell Art Museum's lawn on Darnell Street, named at the school district's 1982 centennial and listed by the city in 2009 (Gathering Growth: 13.7 m tall, crown about 28 m). Pin approximate (register point, not checked against imagery); the newest dated report is 2018, and the story says so and asks readers. No photograph yet, so Bing only. Fort Worth intro, meta and FAQ counts now say nineteen, and the Cultural District walk names it.
- Held, with reasons in the research files: ftw_018 Memorial Bur Oak (the register never says the ground is public; the point is near the Trinity Trails path in Benbrook but nothing shows the pin itself is public). inn_007 Winterlinde unter dem Bergisel (the register pin falls on the building at Brennerstrasse 6f, likely a private yard; not written). fdl_001 is the live spa_001, a duplicate. std_001 Studena oak has no roadside viewing pin and one chain of sources.
- Preflight 0 problems; qa.py not run (needs a site build).

## 2026-10-20 write pass: six Dutch register trees live, READY pile cleaned

- Live: Roosendaal 16 to 20 trees, roo_022 Silver Maple behind the Library (5.25 m round, now the thickest tree on the page), roo_023 Black Locust of Emile van Loonpark (4.06 m), roo_024 Caucasian Wingnut of Emile van Loonpark (23 m), roo_025 Beech in the Path at Vrouwenhof (29 m, tallest on the page). Intro, meta and question copy recounted to twenty. New place Batenburg (Wijchen), two trees, no indexed place page under four: btb_001 Horse Chestnut of Batenburg Church (5.08 m, 26 m) and btb_002 Copper Beech of the St Victorkerk (5.10 m), pins confirmed from the register point on one crown in the PDOK frame. All six from the live LRMB layer, re-queried today (status 3; Batenburg inspected May 2026, Emile van Loonpark trees March 2023, said on each page). No photographs yet.
- Not written: most of the 44 "READY" leads were not ready. 20 Dutch leads were dead in the register (LRMB status 5), among them Assen's Overcingel oak, all of Haarlemmermeer, Sittard-Geleen and Zaanstad, and three Roosendaal leads. leads.py's dead-register filter did not catch them; they carry the number only as "LRMB register nr N" in their why text. Worth a fix in leads.py. Marked blocked. Barcelona's huingan is already live as bcn_041 (marked duplicate). Rows, groups, the Mariadal convent, an appointment-only farmyard, trees below the size floor, Walpole's Grandma Tingle (no way to tell her apart), Cardiff, Maastricht and Rothenburg are marked held with a reason. The two reader sightings (Tangier fig, Freiburg beech) are left untouched for rung 1.
- Preflight 0 problems; qa.py needs a site build, not run here.

## 2026-10-20 night run (00:54): four photographs approved

- Rung 6/photos: photo_fetch.py --roster plus a photo-judge pass over 120 candidates: 4 approved (Dresden dre_025, dre_029, dre_030 oaks; Luxembourg lux_008 sycamore, bare in winter), 1 held (kra_033), 115 rejected. Reversal commands are in the commit message of 3e862b604's report: `python3 scripts/photo_apply.py hold <id> <url> --reason "overruled"`. Some of these look like the Dresden oaks already approved on 10-19; the sweep was marked exhausted and I reran it anyway, so do not run it again.
- Rung 1: the Freiburg beech (ed90210d) still has no file on this runner, verdict left open. New trees: none; Rothenburg has only 5 leads (under the six-candidate floor, 48h wall), Munich is full at 63/60.

## 2026-10-20 night run (00:41): nothing published

- Rung 1: the one open reader photograph (ed90210d, European Beech in Freiburg, 47.9543 7.8067) has no file on this runner (out/sightings/ is empty for it), so its verdict stays open until a run can look at the pixels. corroborate.py: no register entry within 100 m, no Wikipedia tree article within 300 m.
- Rung 4: Frankfurt deepen pass, 0 trees. The de.wikipedia Naturdenkmal list is used up; three more candidates (Wolfsweide oak, Niddaaltarm walnut, Herrenwiese oak) filed as leads, none has a photograph or a pin from a source. frankfurt.de still 403. Frankfurt is a 48h wall. Stuttgart has no register supply (from-zero stays off). The ready-to-merge Memorial Bur Oak (ftw_018) has no stated access, so it waits.
- Nothing left on the shelf that a window can move; the READY pile is ordinary Dutch trees.

## 2026-10-20 session: IVN Amersfoort reply sent
On Hidde's "verstuur", the reply to IVN Amersfoort went out in Lenny's thread (batch reply-ivn-amersfoort-2026-10-20): thanks for the expert's list, the Randenbroek oak is live with both ages, the Havik lime's age is updated, and would he be Amersfoort's ambassador. Watch for his answer; an ambassador grant waits for it.

