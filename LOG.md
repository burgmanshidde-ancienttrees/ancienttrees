# LOG

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-10](archive/LOG-2026-10.md)
- [2026-09](archive/LOG-2026-09.md)
- [2026-08](archive/LOG-2026-08.md)
- [2026-07](archive/LOG-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
<!-- archive-index -->
## 2026-10-22 night run (01:38 UTC window): Potsdam +3 trees

- **Live:** Potsdam goes from 15 to 18 trees: the pollarded linden of Fahrland, the Babelsberger Strasse oak and the Nattwerder lindens (register-only, no photographs yet, confirmed pins). German overlay and counts updated. Preflight 0 problems. 7-day visits line not printed by prepare.py this run.
- **Wall:** Rothenburg ob der Tauber verified empty (near register trees already live or blocked; Bettwar and Insingen lindens stay leads), walled 48h.
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

## 2026-10-19 night run, second attempt: Frankfurt 17 to 20 trees

- Frankfurt: three new trees live (frk_018 Service Tree of Riedberg, frk_019 Border Oak at Berger Warte, frk_020 Brentanopark Oak), none with a photograph yet (Commons candidates noted in verify_notes for the photo lane). Intro and FAQ counts updated, German overlay translated. Preflight 0 problems; full site build not run here. Six rejects kept in data/leads/frankfurt.json. frankfurt.de returns 403 to every fetch.
- fdl_001, ftw_018, std_001 are not READY to merge: their files carry a not_merged_reason (no honest container), so they stay.
- Claim released. Costs: verify about 120k tokens, write about 60k, translate about 75k.

## 2026-10-19 night run (window from 21:56 UTC): nothing published, no tree added

- Rung 1: one reader photograph of an unmapped tree (European Beech, Freiburg, ed90210d). corroborate.py: no register entry within 100 m, no article within 300 m. The photograph is not on this runner (out/sightings/ empty), so the verdict stays open until a run can look at it.
- Rung 2: the failed deploys were feedshape.py refusing null photo credits; 8a9ad1a24 (empty strings) is the fix and the 21:44 dispatched deploy carries it, still in progress at 22:15.
- Spokane claimed and released: one unmined candidate, under the six-candidate minimum (wall 48h). Munich refused: full (63/60). The writable pile is mostly small Dutch trees; the few other written ones (fdl_001, ftw_018, std_001) were not merged this run.
- Photo recheck on the London plus seven frozen-roster cities (47 trees): one new candidate (ams_028), nothing to judge. Lane is near empty.
- For Hidde: nothing.

## 2026-10-19 night run (earlier, window from 21:39 UTC): nothing published

Rung 1: one app sighting, ed90210d (European Beech, Freiburg, 47.9543 7.8067). No register entry within 100 m, no encyclopaedia article within 300 m. Its photograph is not on this runner (out/sightings/ has no file), so the verdict stays open rather than judged blind. Rung 4: `photo_hunt.py --recheck --city london` found 0 new candidates for the 7 photo-less trees. The writable pile is three finished trees (fdl_001, ftw_018, std_001) and prepare.py asks for a verify refill (1026 leads short only a source); I dispatched no verify agent this run. Not done: no trees added, no commits besides this entry. Also open from the session brief: the Build and deploy site failure (1 in a row) and 31 photographs not yet vendored.
## 2026-10-19 session with Hidde: the headline never grades a first day by Take me there
A session quoted the 10-18 digest's old activation table and called "2 of 14 tapped Take me there on day one" the weakest link. Hidde: people are often scouting for their holidays and are far too far away for that button. The headline already dropped the row this morning; what was missing was a ratchet. `check_the_headline_never_judges_take_me_there()` in qa.py refuses a Take me there, first-day, weakest-link or back-within-a-week line in `headline_section()` and in DATA.md's newest entry from 2026-10-20 on. CLAUDE.md's digest line says why. Nothing in the product changed.

## 2026-10-19 session with Hidde: 40 readers' photographs were wrongly unlinked; restored, and a brake added
The 16:45 UTC knock unlinked every reader photograph on the site (40, seven accounts) as if all seven had deleted their account, twenty minutes after the ids became codes. Almost certainly the runner's codes do not match the files' (a different SUPABASE_SERVICE_KEY), so every account looked gone. Reverted a1e70b7 (links back) and photo_takedown.py now refuses a sweep where every account, or more than two, reads as deleted. Resolved the same evening: `people.py --check` passed on the Mac (9 of 10 codes are live accounts; the tenth is probably a real deletion) and the GitHub secret SUPABASE_SERVICE_KEY was set to the Mac's key at 17:32 UTC. The next knock will show whether the sweep now unlinks only that one.

## 2026-10-20 session: IVN Amersfoort reply sent
On Hidde's "verstuur", the reply to IVN Amersfoort went out in Lenny's thread (batch reply-ivn-amersfoort-2026-10-20): thanks for the expert's list, the Randenbroek oak is live with both ages, the Havik lime's age is updated, and would he be Amersfoort's ambassador. Watch for his answer; an ambassador grant waits for it.

## 2026-10-19 session: three Randenbroek trees live in Amersfoort, from IVN's expert list

**Live on /amersfoort (21 trees, English and Dutch):** ame_019 the oak on the pond bank behind Huize Randenbroek (LRMB 1677723, 5.34 m round, 25 m) carries both ages, about 160 by the register and about 375 by the local expert's 1650, and the page's oldest-tree answer now says the expert's date contests the Hertekop oak's title; ame_020 the pair of planes at the park gate (LRMB 1680326, 4.81 m, 30 m, observed by the register July 2026); ame_021 the two-stemmed yew by the house (LRMB 1680327, 19 m). Pins are the register's, confirmed; estate history (Jacob van Campen, 1626 onwards) from the Rijksmonumentenregister. No photos yet, so Bing only until one lands. The expert is not named anywhere.
**Not shipped, and why:** the copper beech before the house is felled (LRMB "Gekapt", status 5). The weeping ash in the Provenierssteeg is also status 5 in the register (dead or felled, last seen December 2024), though the expert's October 2026 list still gives it; held in data/leads/amersfoort.json until someone confirms it stands. **For Hidde:** the IVN reply in out/tmp/reply-ivn-amersfoort.md now asks whether that ash still stands instead of saying it is going up; it is ready to send.
Found in passing: the LRMB file holds 4,472 status 5 (dead or felled) rows, and `passcheck.py --brief` lists them as candidates. No live tree points at one.

## 2026-10-19 session with Hidde: merging trees moves into the menu, and readers can report a tree that is on the map twice
App: the green "Is this <name>?" box on a tree you added is gone (Hidde: "hell intrusive flow for how rare it is"). Instead the ⋯ menu on your own tree has "Merge with another tree": a list of our nearest trees with search, then "Merge into <name>?" and "Merge trees". It is instant (it only changes your own tree) and lands on our tree with "Trees merged". App and web: "Something's wrong" has a new chip, "It's on the map twice", with "Which other tree is it?" in all eight languages; those reports are reviewed by a run, never merged on the reader's word (rule in CLAUDE.md, Reader input).

## 2026-10-19 session: readers' account ids are codes in every public file

Every reader account id in the repository (photos in 13 city files, leads, judgements' photo paths, the vouched list, the ambassador invitation lists: 210 places) is now `people.ref(uid)`, a keyed code nobody without the service key can turn back. Scripts that need the person (mail, takedown) resolve the code through the account list (scripts/people.py). The account-deletion promise is tested: scripts/test_people.py unlinks a deleted account's photo and lead on a copy and touches nothing when the account list is unreadable; on the real data the takedown check reads 40 reader photos from 9 accounts, none gone. qa refuses a raw id where a code belongs. Ambassadors' own rows keep their id (consented, public through the badge). Still in git history, like everything removed today; no force-push, no private repo (Hidde: too expensive).

## 2026-10-19 session: profile header aligned, round flag fixed, open.ancienttrees.app prepared

**What changed in the product (app, next build):** on My trees the name and counts now sit centred on the photo (the name's 44-point tap frame no longer takes layout space), and the flag after your name fills its circle (the emoji is cropped to its own pixels; it sat off-centre with a white crescent). Polarsteps layout unchanged.
**Open in app, AllTrails' way (CONVENTIONS.md):** a second GitHub Pages site, github.com/burgmanshidde-ancienttrees/ancienttrees-open, serves open.ancienttrees.app: the app-link file for /open, the /open fallback to the App Store, everything else to ancienttrees.app, robots disallow. The app now claims applinks:open.ancienttrees.app (next build). **For Hidde:** one DNS record at TransIP (CNAME open to burgmanshidde-ancienttrees.github.io). Done 2026-10-20: Hidde added the record, GitHub's certificate came after re-setting the domain, HTTPS enforced, and the website's Open in app buttons now point at https://open.ancienttrees.app/open (live, checked on /baarn/cantonspark-dawn-redwood). On an iPhone it opens the app from the next app build on; until then it lands in the App Store as before.

## 2026-10-19 session: Manchester's Variegated Green Ash found by the Friends of Alexandra Park

**Live (next deploy):** mcr_004 has its first photograph and a confirmed pin. A Friends of Alexandra Park volunteer, answering the 2026-10-09 help mail, went looking and mailed a geotagged photo of the trunk ("This may be the tree you're looking for"). Pin moved about 280 m to the GPS fix, photo published uncredited per the mailed-photo ruling (EXIF stripped, 480x640 as mail delivered it), story and access no longer say the spot is unknown. Identification is theirs and hedged; a canopy photo follows by mail and is the check on the cream leaves (verify_notes). Reply sent on Hidde's "send" (outreach_send.py, in his thread, logged in the private outreach-sent.json): thanks, the page is live, and an invitation to be ambassador for Manchester, named on the page or not as he prefers. Grant with `ambassador.py` once he answers.

**Amersfoort (IVN):** IVN Amersfoort forwarded a local tree expert's checked list (80 years and over, planting years). Our 18 trees agree with it. The Havik lime (ame_018) now carries the expert's 1850 beside the register's 1880s band. 12 leads and 8 blocked private-garden trees in data/leads/amersfoort.json, matched to LRMB register numbers. Top: the oak at the Randenbroek pond, 1650 by the expert, 1860-1870 by the register, plus a Randenbroek cluster (copper beech, plane, yew) and the Provenierssteeg weeping ash (expert and register agree on 1840). Not yet written as pages. Reply drafted in out/tmp/reply-ivn-amersfoort.md (asks the expert to be ambassador); best sent once Randenbroek is live.

## 2026-10-19 session: photo push on the roster, and why Take me there looks low

**Live:** 8 roster trees have their first photograph: four Dresden oaks (dre_006 Rieseneiche Sauerbusch, dre_023 Luthereiche Kleinluga, dre_024 Oberpoyritz, dre_026 König-Albert-Eiche), Salzburg szb_013, Brno brq_002 (GPS fix 8 m and the memorial-tree sign; large iNaturalist file), Viroflay vir_001 (Chêne de la Vierge) and Nagoya ngy_001 (Castle kaya). These pages come back into Google's index with the next deploy. Undo any one with `python3 scripts/photo_apply.py hold <id> --reason overrule`.

Held (photo parked, nothing live changed): lux_009, nyc_022, utr_037, yak_002, slm_001 (right tree, file on disk only 200x500: fetch the full-size original), per_005, ali_006, bil_001.

**The negative that matters:** `photo_hunt --recheck` on the top 27 roster cities plus `photo_fetch --roster` gave 236 candidates; 216 rejected (buildings, statues, plaques, birds, archival black-and-white, wrong species). About 940k tokens for 8 photographs, roughly 117k a photo against the 15k target. The Commons and iNaturalist supply for roster trees is close to used up: do not run another full roster viewing pass without a new source. Better lanes: readers' app photographs, and the `slm_001` full-size fetch.

**Take me there on day one** (data/research/take-me-there-diagnosis-2026-10-19.md): nothing is broken; the event and button are unchanged and ungated. The likely cause is that most new phones come from App Store search and browse from far away; 14 phones prove no rate either way. The PostHog key file `~/.ancienttrees-posthog.env` is missing on this Mac, so the per-version split could not run. Proposed: count Take me there only among phones that opened a tree near them (measurement only); for a far tree, Save leads (needs Hidde's yes).

Also: photo-judge must never send a person's name or address in a User-Agent (one batch did once, to Wikimedia, in a failed request).

**The digest is short now** (Hidde's yes, DECISIONS.md 2026-10-19): it opens with his numbers (visits and from search, first-time downloads, accounts, back within 30 days, Want to go, collected, readers' contributions), then readers, decisions, yesterday's site searches, Google and Bing. About 60 lines a day; Monday adds the slow tables; the night run's lists (shift, photo approvals with reversals, depth roster) sit below a line at the bottom. Google Analytics is out. Dry-run here with Supabase and App Store keys; Cloudflare, Google and PostHog rows are first seen in tomorrow's CI entry.

Then: Google Analytics is the digest's one visitor source and Cloudflare left it (Hidde's call; GA counts only cookie-accepters, the headline says so); the Cloudflare beacon script is still on the site. The Monday mail (weekly-mail.yml, weekly_mail.py) is deleted: alarms now reach Hidde only through a session's brief.py and the digest's URGENT line.

Then Cloudflare left the project altogether (Hidde: "lets get rid of cloudflare alltogether and clean up"): the beacon is off every page, the privacy page no longer names it, visitors.py, country_look.py and country-look.yml are deleted, audience.py and seo_diagnose.py keep only their Search Console halves, and no workflow passes the token. `?notrack=1` still opts our own devices out, now handled by the event tracker in Base.astro. For Hidde (optional): the CLOUDFLARE_ANALYTICS_TOKEN secret and the Web Analytics site in the Cloudflare dashboard can be deleted; nothing reads them.

**Breakage, fixed:** every deploy since 16:45 UTC failed preflight on the Palma fig (plm_006). Its reader deleted their account, photo_takedown.py unlinked the photograph, and `reader_found()` stopped seeing a reader's tree. An unlinked contributor photograph now counts as the reader's evidence (DECISIONS.md 2026-09-04: the picture outlives the account).

## 2026-10-19 session: privacy audit ("wat als Follow the Money ons onderzoekt")

Closed: names and the follow graph were readable with the website's public key (now signed-in only, via the profile SQL Hidde ran); one served photo (the owner's own Pekingtuin oak) carried GPS (stripped; 1,221 others clean); readers' exact photo times sat in public repo files (78 removed, scripts stop writing them); personal mail addresses in 17 tracked files (masked; two exclusion lists now hashed); ambassadors' mail quotes (out); the shared_trees view listed all 86 shared sightings to anybody (now one tree by its link through `shared_tree()`, waiting in PENDING.sql). Two new ratchet checks in qa.py keep the repo and the photos clean.

Not closed: everything removed is still in git history, because the repository is public and rewriting history needs a force-push (hard list 3, Hidde's call). Readers' account ids still sit beside tree coordinates in data/leads/_sightings.json and as contributor_user_id on photos; they no longer resolve to a name without an account, and hashing them touches the account-deletion chain (photo_takedown.py), so it is its own job.

FOR HIDDE: paste supabase/PENDING.sql (shared trees) once the deploy of this session is live.

## 2026-10-19 session: the dead-yew reader got "on the site now"

- Submission 466 (the reader who reported the Yew of Campo Santana dead) was set to `changed` with no reply_text, so the 09:31 knock auto-composed and sent "What you sent us is on the site now", linking /lisbon, with the App Store line to an app user. Only that mail went; no real answer.
- Fixed in scripts/contributor_reply.py: the auto template now only fires for an added tree or city; a correction set to `changed` with no reply_text is held ("write one"). The App Store line to app users was already fixed in 4b7d89c65.
- The correction for the reader (drafts/reply-campo-santana-yew.md, mailcheck clean) was approved by Hidde and put on submission 466 as reply_text with replied_at cleared; no knock ran (review yield), so it was sent from the Mac with contributor_reply.py --send at 13:28 UTC, the only mail in the queue; replied_at is set.
- Then, on Hidde's word ("the message about the app is very irrelevant keep that out of all mails to users"): the App Store line is gone from every automated mail (contributor_reply.py thank-you, change confirmation and the line it appended to written replies; ambassador.py heads-up), and mailcheck now refuses the link in any letter, not only reply drafts. This ends the 2026-09-03 standing instruction. "Add it in the app" asks to people writing from the app stay.

## 2026-10-19 session: the iOS app check stops going red on tests it passed

- Nothing changed in the product for readers except one small thing in the app: once somebody allows location, the map now shows their blue dot straight away instead of only after tapping the recentre arrow.
- Why ios.yml kept going red: four of the five reds on 10-18 and 10-19 were tests that passed on their automatic retry. xcodebuild said "TEST SUCCEEDED", but our own step read the failed first try and went red anyway (UndoWalk twice, the map-pin test, the "Failed to get launch progress" error). Now a test that needed its retry shows as a yellow warning naming it, and the run stays green. Red still means a test failed both tries.
- UndoWalk: the tap landed while the collect sheet was still sliding in, so it was lost. The test now waits for the button to hold still, and taps once more only when nothing happened. LocationAskWalk: on the CI phone the app froze behind its opening photo, which fits the map asking the system for the location permission and waiting for the answer on the main thread. It now reads the answer from the system's callback. I could not make the freeze happen on the Mac, so this is the best-evidence fix, not a proven one.
- Merged to main (4ababaed9). Green three times in a row: push run 39238094865 (227 passed, nothing needed a retry), scheduled run 39238782925, and run 39244469187 that I started by hand. In that last one the tests and layout jobs passed; its iOS 18 floor job was cancelled halfway by a newer push to main, so the floor is still unconfirmed for this change. Locally the two tests passed 15 of 15 under CPU load.

## 2026-10-19 night run 09:31: one photograph, roster sweep spent

- Rung 1: the one open sighting (ed90210d, European Beech in Freiburg, unlisted in registers and Wikipedia) has no photograph file on this runner, so no verdict; left open for a session that can view it. Rung 2: health.py's only item is the profiles.public migration, which needs Hidde to paste supabase/PENDING.sql (already in his FOR HIDDE above).
- Photos: London recheck found one usable file; approved lon_033 (Roehampton Lucombe Oak, CC BY-SA 4.0), preflight 0 problems, committed. Roster sweep (photo_fetch --roster) judged 72 images for 40 trees: 0 approved, 71 rejected and recorded. It repeats 10-18's "near exhausted" finding: the roster's Commons supply is spent, do not rerun it until new candidates exist. Visits last 7 days: 2080.
- Not done: the shelf's READY pile is 44 Dutch trees without a photograph or story pull (low value in recovery mode); london enrichment brief (7 gaps) untouched.

## 2026-10-19 session: the Yew of Campo Santana is dead, retired

- A reader's correction (submission 466, 2026-10-18): "Look at the pictures, please. The tree is dead". Their two app photographs, GPS 6 and 20 m from our pin, show bleached bare yew wood propped on an earth mound, no foliage. Hidde saw them.
- Retired lis_014 with retire.py (to data/leads/lisbon.json, blocked, reason recorded); /lisbon/yew-of-campo-santana redirects. Lisbon is 35 trees; the Portuguese title count fixed by hand. Preflight 0 problems. Submission 466 outcome set to `changed` without a reply_text, so contributor_reply.py mailed its "What you sent us is on the site now" template at 09:31 UTC, with an App Store line, to a reader who uses the app. Wrong for a dead tree. With Hidde's yes a follow-up went out by hand (from the domain, logged in the private outreach-sent.json): sorry for the automatic mail, thanks for the yew report and for the two Jardim Constantino photographs (lis_026, lis_027 had been live since 2026-08-12; the reader gave their photographs, not the trees), and an ask to look through the Lisbon list. Fixed: contributor_reply.py no longer adds the App Store line for an account with app sightings, and CLAUDE.md says reply_text goes in before or with `changed`.
- Also: the local digest page now shows readers' own words where DATA.md says "read it in the database" (show_digest.py, check_the_digest_page_shows_readers_words()).

## 2026-10-19 session: a profile anybody can open, when its owner says so

What changed in the product (web and app, merged and pushed; nothing visible yet): a "Private profile" switch in Settings, on for everyone (Polarsteps' default). Turning it off opens one sheet that says what becomes visible (name and picture, Collected and Want to visit, badges); only "Make public" writes. A public profile is your own profile as a visitor sees it: /profile?u=<id> on the web (noindexed), a pushed screen in the app, reached from People and from an ambassador's name on a city page, which becomes a link with a chevron only while that person's profile is public. The server answers through `public_profile()`, never the dates a tree was ticked. Rule in CLAUDE.md (Privacy and accounts), story in DECISIONS.md, reference in CONVENTIONS.md.

Checked: app built and looked at on the SE simulator (public profile, private profile, the switch, the sheet); signed-out Follow added to SignedOutWalk and passing. Web checked by the source checkers only (no local Astro build); the dispatched deploy is the verdict. Not seen: the linked ambassador row in the app, which needs a public profile in the data first.

FOR HIDDE: paste supabase/PENDING.sql into Supabase (SQL editor, Run). Until then the switch stays hidden on both surfaces and every profile link reads "This profile is private".

## 2026-10-19 session: city pages only say "walk" where the app has walks

What changed for readers: the "Walk them with the app / The walking routes..." pitch at the foot of every city page (English and all seven languages) was shown on every city, ungated, since the walks page went (Contract K, 2026-09-02). The gate the blueprint names, `hasWalksPage()` in site/src/lib/city-walks.ts, was imported by nothing; its last callers went with the tree-page redesign of 2026-09-24 (ac1a7910a) and the city page never re-gained it. It is now wired into site/src/pages/[city].astro and TranslatedCityPage.astro. It runs the same planner as the app's /api/walks.json (walkableTrees, planWalks, routed cache, combined walks left out) with the file's floor of five trees. Cities under it get "Collect the trees you stand in front of" plus a new `appPitchCityBodyNoWalks` line in eight languages, with no walk promised. Verified on a dispatched branch build (run 39211492979: build and QA green, deploy refused for the branch as designed): 120 English city pages keep the walk pitch and 609 lose it, nl 11/3, ja 3/16, and every page agrees with the built walks feed. Big cities such as Tokyo (an app walk of 3 trees) and San Francisco (4) are now on the no-walk side, by the floor's rule. The tightest-walks list on /explore and the home page's product pitch were left alone (general product copy, not a promise about one city). The blueprint and DECISIONS.md references to city-walks.ts are accurate again, so nothing for Hidde to edit.

## 2026-10-19 05:21 window: Miami opens, Key West and London added

Visits last 7 days: 1920 (3080 page views). Inbox empty. health.py: same two flags as the earlier window (scheduled iOS run failed again, smoke "skipped" on push); not touched, needs a session. Rung 4: write pass (Opus, ~95k tokens) on the staged Miami file. New: Miami with 4 trees (Simpson Park paradise tree, Vizcaya Garden Mound oaks, redberry stopper, last Cuban royal palm; page copy written), Key West as its own one-tree place (kyw_001, 250 km from Miami, tree page only), and London lon_033 Roehampton Lucombe Oak. All pins approximate, no photographs yet; 3 of 4 Miami trees sit behind Vizcaya's ticket (note only, free trees wanted). us-states.json and city_names updated. Preflight 0 problems. Claim released with --force (kyw_001 lives in key-west.json).

Second item, same window: Miami and Key West deepen. Verify pass (Sonnet, ~190k tokens) found 4 free trees, all single-source and flagged; write pass (Opus, ~107k) shipped mia_006 Castellow Hammock champion false mastic, mia_007 Merrick packing-house fig, mia_008 Collins Park baobabs, kyw_002 Key West Cemetery strangler figs (city foresters asked to remove them, decision postponed; Tree Commission agendas since Feb 2026 not checked), plus nsb_001 Venerable Oak of Novo Selo as its own one-tree place. Held: std_001 Grandpa Kolyo's Oak (private field, no roadside viewing coordinate). Miami now 7 trees, 3 paid; Castellow Hammock is a car trip, may want its own place later. Several Coral Gables nominations kept as leads. Preflight 0 problems.

Third item, same window: Innsbruck opened. Verify (Sonnet, ~78k) from the Land Tirol Naturdenkmal register (CC BY 4.0) joined to the de.wikipedia list: 7 flagged trees; write (Opus, ~95k) shipped inn_001 to inn_006 as a new Austrian city page, approximate pins, no ages (no source gives one), recognition line on each. Held inn_007 (lime below the Bergisel: access of the plot unsettled, only a 2016 photo). Hofgarten and Schloss Ambras not researched (no register points); they need their own pass. Eight leads and six blocked (felled trees) kept in data/leads/innsbruck.json. Preflight 0 problems. Superlatives collision chr_001/dnk_001 pre-exists, not from this pass.

Fourth item: photo hunt and viewing pass (Opus, ~115k) on the new Miami, Innsbruck and Key West trees, 23 candidates viewed as pixels. Approved: inn_003 Schulgasse Oak and inn_006 Traklpark Oak (register number in the filename, geotag under 20 m, CC BY-SA 3.0 AT, Gotglä). Reverse with `photo_apply.py hold <id> <url>` (inn_003 file ND_101_10_Eiche_Schulgasse..., inn_006 file ND_101_11_Stieleiche...). Held kyw_002 (which trunk?). Nothing usable for Miami (no whole-tree frame) or the other Innsbruck trees. Note: photo_fetch.py has no single-tree option and needed Pillow, which this runner lacks (installed under out/tmp/pylib, temporary). For Hidde: the scheduled iOS run still fails (timeout 1h54m on the simulator, push runs pass); not touched.

## 2026-10-19 02:51 window: Las Vegas retry, little on the shelf

Visits last 7 days: 1920 (2970 page views). Inbox empty. health.py: the scheduled iOS run failed again, in the log a simulator "Timed out while requesting launch progress" (infrastructure, push-triggered runs pass); smoke "skipped" is its push trigger, deploy green. Enrich empty. Shelf: READY 43 are mostly Roosendaal street trees earlier passes declined; the written trees in data/research are blocked (ftw_018 access, fdl_001 removed on purpose, no city file for Studena/Novo Selo/Key West). Scouting RETRY Las Vegas (already live with 11 trees, so a deepen): verify pass (Sonnet, ~85k tokens) flagged 2 UNLV champions, lvg_015 Mondell Pine (157 cm girth, 2023 Nevada register plus UNLV) and lvg_016 Holly Oak (small, one source); approximate pins, no photograph, so not written; the rest stay leads with reasons. Claim released with --force, Las Vegas a 48h wall. The scouting note is stale (the city is published).

## 2026-10-19 00:31 window: Delft enrichment

Visits last 7 days: 1951 (3075 page views). Inbox empty. health.py flags the scheduled iOS run (timed out at 1h54m, hand runs pass; needs a session, not touched) and a "skipped" smoke test (push-triggered, build itself green). Rung 4 on the frozen roster: Delft enrichment (Sonnet, ~51k tokens). del_012, del_013 and del_014 now carry register ids with girth and height from the LRMB layer, del_013 a sourced access line (free, sunrise to sunset), del_014 an autumn best_time. Pins stay approximate for all three (register coordinate equals ours, cemetery too big for a site). Preflight 0 problems.

Rung 4, scouting RETRY London (Great Trees of London list): verify pass found 3 flagged trees, photo-judge approved 2 (Royal Oak, Osterley cork oak; Roehampton Lucombe held, ambiguous trunk), write pass shipped lon_032 (Osterley Park Cork Oak, photo 640x480 so soft large; approximate pin) and fixed London's count copy. lon_031 Royal Oak is the live lon_002 (10 m away), so not written. For a session: lon_002's source and pin come from the Woodland Trust Ancient Tree Inventory, which the London gate forbids, and its story cites that inventory; the new Commons photo of the Royal Oak (Richmond_Royal_Oak_(3).jpg, CC BY-SA 4.0, in out/tmp/london-photos.json) could join lon_002's photos. Refused: nothing.

## 2026-10-18 22:16 window: deploy fix and roster photo pass

Visits last 7 days: 2079 (3240 page views). Rung 2: the failed deploy was qa's soft-hero check on Portland's Balch Creek Fir (375px iNaturalist medium file); swapped to the 1024px large file, measured by photo_res.py, preflight 0 problems, pushed (567f5b563). The iOS app failure is the scheduled run only and needs a session (not touched). Rung 4/6: `photo_hunt --recheck` plus `photo_fetch --roster` and a photo-judge pass: 2 approved (ber_059 Berlin oak, wdc_015 Smithsonian elm, large file), 1 held (nyc_022), 70 rejected. The roster photo sweep is close to exhausted; the yield per pass keeps falling. Written trees waiting in data/research (ftw_018 access unstated by its register, kyw_001 Miami below the four-tree floor) were left alone. Miami verify pass (Sonnet, ~105k tokens): 4 flagged trees in data/research/miami-verified.json (Simpson Park paradise tree free; three Vizcaya trees paid), all approximate pins and no photograph, so nothing could be written to a city file (Miami would be 75% paid and preflight needs a photo or confirmed pin). Parked, claim released; path forward is a photograph of the Simpson Park tree and a Miami Beach pass. Refused or odd: `python3 scripts/photo_fetch.py --roster` ran past the 600 s foreground limit and moved to the background on its own.

## 2026-10-18, second restart: merged written trees

- Live: Spokane gets the Grant Park Guardian (horse chestnut, no photo yet, so Bing and readers only). Counts and FAQ updated to 14.
- Not merged: ftw_018 Memorial Bur Oak (register does not say the ground is public, hard rule 10); fdl_001 Figueira das Lágrimas (slug is in REMOVED_TREE_SLUGS, removed on purpose). Key West, Studena and Novo Selo have no city file; left in research.
- READY (43) is mostly Roosendaal street trees; no write pass dispatched.

## 2026-10-18, restart after early stop: Frankfurt enrichment

- No new trees. Claims were empty; READY (43) is mostly Roosendaal leads earlier passes declined, so no write pass.
- Frankfurt enrichment (5 trees): frk_014 and frk_015 got a girth and height from the city's ND object pages (read via Wayback, frankfurt.de is blocklisted) and a firmer access line for frk_014. frk_015's location_site was refused (needs a source URL), so its pin stays approximate. frk_012, frk_013, frk_017: no per-tree record found; 10 gaps recorded as dead ends. Claim released.
- Stuttgart enrichment (3 trees, 7 gaps): stu_008, stu_009, stu_010 gained LUBW register records (Naturdenkmal numbers); stu_010 pin from Wikipedia's coordinate. No measurements found; the city PDF 3-8.pdf may hold them. Claim released.
- Needs a tool: the pass has no PDF reader, so the Palmengarten tree PDF (Senckenberg Yew) stays unread.

## 2026-10-18, 19:58 run: reader sighting verdict, roster photo pass

- 7-day visits: 2010 visits, 2900 page views.
- Rung 1: the one reader photograph of an unmapped tree (Moreton Bay Fig, Jardin de la Mendoubia, Tangier) was looked at: a huge buttressed fig, worth the walk, but no register or encyclopaedia source and Morocco is out of focus. Kept as a lead with a written verdict in data/leads/_sightings.json.
- Photos first (recovery mode): `photo_hunt.py --recheck` found no new candidates, so `photo_fetch.py --roster` plus a photo-judge pass on the queue: 14 photographs approved (Utrecht Dolehof plane, Portland Corbett Oak, Hong Kong Nathan Road banyan, Dallas Post Oak Grove, New York Reservoir plane, Berlin Korean Evodia, Los Angeles El Pino, Tokyo Hongo camphor, Stockholm Bellmanseken, Vilnius Mickiewicz ash, Washington DC Travilah Oak, Naples Villa Comunale gum, Seattle Hiawatha oak and Roanoke elm), 5 held, 38 rejected. Reversal commands are in the pass report (`photo_apply.py hold <id> --reason overrule`).
- The six written-and-ready trees (fdl_001, ftw_018, kyw_001, spk_015, std_001, nsb_001) were not merged: they have neither a photograph nor a confirmed pin, and preflight refuses them. No new trees this window.
- Leipzig enrichment pass (5 trees, 9 gaps): closed nothing. No official per-tree record for the Starkeiche, Wikipedia ND coordinates only repeat our pins, no source states more on access. Recorded as dead ends (`enrich.py --done leipzig`), claim released.
- The image viewer hit a request limit for a long stretch, so the pass ran about 45 minutes.

## 2026-10-18, retry run: READY write pass

- Live: Leipzig +1 (lpz_030, white elm by the B2, German overlay), Delft +3 (del_012 to del_014); counts fixed on both pages (Leipzig 29, Delft 12).
- 22 READY leads handed over, 4 written: 6 already live, 7 access not established, 5 too thin or too small. Claims for leipzig, delft, vienna released. Munich and Salzburg had nothing to write.
- leads.py --ready overcounts: earlier passes declined many of these in wording it does not recognise.
- Next: photo-judge on the Commons candidate for lpz_030 ("Flatterulme Lzg. B2.jpg", CC BY-SA 3.0). Roosendaal (22 READY) untouched.
- Breakage: iOS app workflow shows FAILED (newest run 2026-10-18), not looked at this run.
## 2026-10-19 session: collecting a tree takes it off Want to visit (Hidde's call)

**What changed in the product:** collecting a tree now removes it from Want to visit, in the app (Saved.toggleVisited) and on the website (atPushVisited). Unticking does not bring it back; a heart put on a collected tree afterwards stays. Older hearted-and-collected trees: cleared once on each phone at its next sign-in sync, and 4 rows in 3 accounts deleted from `saves` today (backup in out/tmp/saves-backup-2026-10-19.json, main checkout). Reverses part of the 2026-08-26 ruling; DECISIONS.md has it. Unit tests pass (FailureTests' unheart test reordered to the new rule). The app half ships with the next build.

## 2026-10-18 session: Hidde's app test, four fixes

**What changed in the product:**
- **Pins no longer blink on first open.** When the fresh feed replaced the bundled trees, the map removed every pin layer before the new data was drawn, so for about 0.3 s it was empty (filmed frame by frame). Now the new pins go on top and the old ones are removed only once the new source has its points (MapLayers.apply / retireWhenDrawn). Re-filmed: no gap.
- **A second photo of a tree you added yourself joins that tree** instead of becoming a second tree with its own pin. Within 30 m the "Which one is it?" list offers "Your tree" first; picking it adds the photo (Sightings.addExtra). Test: aSecondPhotoOfYourOwnTreeOffersIt. His account still holds older pairs (Nara 1d61e594/b6706a98, Tokyo a4fa2700/ae06e952), left untouched.
- **The ambassador tag opens its place**, in the app (My trees) and on /account.
- **Early-adopter sheet** says "You are one of the first users of Ancient Trees", no months, app and web.

**Not changed, needs Hidde:** auto-removing a tree from Want to visit once collected (his own ruling 2026-08-26 keeps the two lists independent); "Open in app" on the website goes to the App Store even with the app installed, because iOS ignores a universal link to the domain you are already on.

## 2026-10-18 session: small code tidy (Hidde asked)

**No product change.** 17 one-off scripts (old register importers, two `_tmp_` files, finished batch helpers) moved to archive/scripts/, nothing deleted. Two app views nobody shows any more removed: SentCard (unused since Collected became a grid, 10-09) and ProfileButton (gatecheck entry dropped with it). DATA.md went from 2 MB to 435 KB: `archive_logs.py` now also moves DATA.md entries older than 14 days to archive/DATA-YYYY-MM.md, daily, every line checked present after the move. A stale August copy "BRIEF_RESEARCH 2.md" removed (every line is in archive/BRIEF_RESEARCH-full-2026-10-12.md).
**Left alone on purpose:** site/src/lib/city-walks.ts is imported by nothing, yet SEO_GEO_BLUEPRINT.md names its `hasWalksPage()` as the gate on the word "walk". So either the gate silently stopped running or it lives elsewhere; that is a finding, not a deletion.

## 2026-10-18 session: iOS CI compiles again

**Breakage, fixed:** since the near-a-tree banner commit (8ed90c196) the app did not compile on CI: ContentView's `body` was too big for the runner's type-checker ("unable to type-check this expression in reasonable time"). The first fix (a33538bab, moving the banner and tab-bar inset out) was not enough; measured locally, `body` still took 14.4 s. The second fix (54644b983) splits it into three pieces (tabs, routed, presented) and gets it down to 0.27 s. No change in behaviour; appfit (iOS 18, iPhone 16 Pro Max) gives 0 findings on 39 screens.

**CI now:** push run 39141889872 on main is green (test, look). Dispatched run 39145554047: floor and look green, but test is red from `UndoWalk.testRemoveFromCollectedOffersUndo` failing its first attempt and passing its retry. Run 39137010429 had the same pattern with `testTappingAPinOpensItsTree`, which also did it at 09:53 that morning, before the banner commit. Still open: ios.yml fails on any failure line even when `-retry-tests-on-failure` then passes, so flakes like these keep the scheduled run red.

## 2026-10-18 17:02 window: reader verdict, photo lane, Sequoia

7-day visits: 1,990 visits, 2,790 page views (peak 550 on 10-16).
- **Rung 1:** the Baarn photograph f9336891 (owner account, no note) is a large old willow trunk on a waterside bank. No register or Wikipedia match, no age or girth, so verdict lead with its coordinate; written to judgements and `_sightings.json`.
- **Photos on roster pages:** `photo_hunt.py --recheck` for Vienna, London, Leipzig, Cardiff, then two photo-judge passes: 5 approved in all (vie_049, vie_056, vie_058, lon_029, lpz_023; reversals in the entry below). I approved the Sequoia National Park Sentinel Tree myself (the park's SENTINEL sign is in the frame, geotag 12 m; undo with `photo_verdicts.py` hold on seq_007).
- **Enrichment:** the vienna+london+leipzig+cardiff brief held only season and pin gaps with no evidence on hand, so I recorded it as dead ends (`enrich.py --done`); `enrich.py --next` now says nothing to do.
- **Scouting:** Denver retried, still stalled (no open register of Denver's remarkable trees; Forestry's champion register is not a download).
- **Leipzig (live, 22 to 28 trees):** verify pass (6 trees, 9 new leads) then write pass; lpz_024 to lpz_029 merged with a German overlay, 4 best_time lines, and the Rosental Starkeiche (lpz_026) is now Leipzig's oldest tree on the page (age disputed, 350 vs 600 years, said on the page). All six have no photograph yet; Commons CC BY-SA candidates exist for lpz_024, 025, 027, 028, 029 (lpz_029's file may show the other oak). Photo hunt and a viewing pass are next for them. lpz_019 stays dropped as a duplicate.
- **Stuttgart's three new trees (photo-judge pass):** 6 files, 8 candidate verdicts, every one viewed, both oaks zoomed at full size for species. 3 approved, 0 held, 5 rejected. All three new trees now have a photograph. Approved, with reversal:
  - stu_008 Schillereiche: Schillereiche (Wernhaldenstraße, Stuttgart), 2024-05-05 (CC BY-SA 4.0, Fyrtaarn). Geotag on our pin, title names it, bench beside the trunk as the story says. Thick twisting limbs and pale ridged bark, lobed oak leaves high in the sunlit crown (the oval leaves in front are dogwood shrubs). Undo: `python3 scripts/photo_apply.py hold stu_008 "https://commons.wikimedia.org/wiki/File:Schillereiche_(Wernhaldenstra%C3%9Fe,_Stuttgart),_2024-05-05,_yj.jpg" --reason "reversed"`
  - stu_009 Wernhalde sequoias: Naturdenkmal Stuttgart - 1 Mammutbaum Steinkopfstr. 6 (CC BY-SA 4.0, Laserlicht). The title names the register tree at number 6 (geotag 41 m). Conical crown, red fibrous trunk, houses and roadside rail as described. Undo: `python3 scripts/photo_apply.py hold stu_009 "https://commons.wikimedia.org/wiki/File:Naturdenkmal_Stuttgart_-_1_Mammutbaum_%E2%80%9ESteinkopfstr._6%E2%80%9C.jpg" --reason "reversed"`
  - stu_010 Jahneiche: Jahneiche Stuttgart (CC BY-SA 4.0, Florian Hoffmann). The title names it. Open-grown oak on a lawn by a road and car park, deep furrowed bark, cut-limb scars, spring leaf. Undo: `python3 scripts/photo_apply.py hold stu_010 "https://commons.wikimedia.org/wiki/File:Jahneiche_Stuttgart.jpg" --reason "reversed"`
  - Rejected: the two cross-tree swaps, an archival Wernhalde forestry map, a distant vineyard view, and the Bei der Eiche 16 A oak (a different natural monument 108 m away, shot at dusk).
- **Leipzig's six new trees (photo-judge pass):** 27 candidates, all viewed, 3 approved, 0 held, 24 rejected. Three of the six trees now have a photograph. Approved, with reversal:
  - lpz_024 Flossplatz pagoda tree: Jap. Schnurbaum Lzg. Floßpl. (CC BY-SA 3.0, Geisler Martin). The caption names this tree at the Riemannstrasse corner; fine pinnate leaflets, forked trunk. Undo: `python3 scripts/photo_apply.py hold lpz_024 "https://commons.wikimedia.org/wiki/File:Jap._Schnurbaum_Lzg._Flo%C3%9Fpl.jpg" --reason "reversed"`
  - lpz_025 Kantatenweg oak: Eiche Lzg. Kantatenweg 5 (CC BY-SA 4.0, Martin Geisler). The caption names the oak at Kantatenweg 5, and its crown is wider than the tree is tall, as the record says. Undo: `python3 scripts/photo_apply.py hold lpz_025 "https://commons.wikimedia.org/wiki/File:Eiche_Lzg._Kantatenweg_5.JPG" --reason "reversed"`
  - lpz_027 Plaussig Steinlinde: Plaussig Steinlinde-01 (CC BY-SA 4.0, Radler59). Geotagged at the tree, with the boulder and the Steinlinde sign beside the gnarled trunk, in leaf. Undo: `python3 scripts/photo_apply.py hold lpz_027 "https://commons.wikimedia.org/wiki/File:Plaussig_Steinlinde-01.jpg" --reason "reversed"`
  - Still without a photograph: lpz_026 (the only candidate shows a swamp-cypress-type conifer in the Rosental meadow), lpz_028 (all eight are Viertelsweg house facades), lpz_029 (the only candidate is an oak seedling leaf close-up; neither Torhaus oak was ever in frame, so the question of which trunk never came up). For a session: the 1999 Steinlinde sign reads 15 m and 330 cm, against the cadastre's 11 m and 390 cm on the page.
- **Frankfurt photographs (photo-judge pass):** 43 candidates for 11 trees, 29 viewed as pixels, 5 approved, 0 held, 38 rejected. Frankfurt goes from 1 photograph to 6. Approved, with reversal:
  - frk_008 Paradieseiche: Naturdenkmal Stieleiche in Sachsenhausen, Paradieseiche (CC BY-SA 4.0, Thomas Wilhelmi). The title names the tree; low-forked oak in full leaf. Undo: `python3 scripts/photo_apply.py hold frk_008 "https://commons.wikimedia.org/wiki/File:Naturdenkmal_Stieleiche_in_Sachsenhausen,_Paradieseiche.jpg" --reason "reversed"`
  - frk_010 Sossenheim Peace Oak: Sossenheimer Friedenseiche in Frankfurt (CC BY-SA 4.0, Thomas Wilhelmi). Geotagged 10 m from the pin, massive buttressed trunk, oak leaves. Undo: `python3 scripts/photo_apply.py hold frk_010 "https://commons.wikimedia.org/wiki/File:Sossenheimer_Friedenseiche_in_Frankfurt.jpg" --reason "reversed"`
  - frk_014 Cemetery Lindens: Lindengruppe in Nieder-Erlenbach, Naturdenkmal (CC BY-SA 4.0, Fernando Ferkelkraut). Geotagged 1 m from the pin, two flowering limes over the cemetery gate. This is the June 2020 frame the story already describes as showing two of the register's three. Undo: `python3 scripts/photo_apply.py hold frk_014 "https://commons.wikimedia.org/wiki/File:Lindengruppe_in_Nieder-Erlenbach,_Naturdenkmal.jpg" --reason "reversed"`
  - frk_016 Schaeferkoeppel Chestnut: Kastanie am Schäferköppel 2 (CC BY-SA 4.0, Fernando Ferkelkraut). Geotagged 25 m away, a lone horse chestnut dome at the edge of a field. Undo: `python3 scripts/photo_apply.py hold frk_016 "https://commons.wikimedia.org/wiki/File:Kastanie_am_Sch%C3%A4ferk%C3%B6ppel_2.jpg" --reason "reversed"`
  - frk_017 August Reiss Oak: August-Reiß-Eiche (CC BY-SA 4.0, Lucas Willem Danehl). This is the image on the tree's own Wikidata item (Q119288797), shot looking up the trunk into a tall crown in full leaf. Undo: `python3 scripts/photo_apply.py hold frk_017 "https://commons.wikimedia.org/wiki/File:August-Rei%C3%9F-Eiche.jpg" --reason "reversed"`
  - Still without a photograph: frk_015 (its one real frame is the right tree but a bare winter oak at dusk, light score POOR), frk_012 (only the 1907 black-and-white scan of the move), frk_013 (three bare November frames, the crown cut off or lost among other trees), frk_005 (no Grüneburgpark frame shows the eight-stemmed lime), frk_007 (sign-and-leaf close-ups only), frk_009 (a street).
- **Leipzig photographs:** 3 more approved (lpz_024, 025, 027; reversals in the entry below); lpz_026, 028, 029 still have none (lpz_029 has two oaks 36 m apart, nothing in frame settles it). The Steinlinde sign reads 15 m and 330 cm against our page's 11 m and 390 cm, worth a look.
- **Frankfurt (live, 11 to 17 trees):** verify pass (6 trees: Senckenberg Yew, Ostpark red oak, Nieder-Erlenbach lindens and oak, Schaeferkoeppel chestnut, August Reiss Oak in Offenbach) and write pass, with German overlay; the yew (about 400 years, tradition-based) is now the page's oldest tree. Photo pass approved 5 (frk_008, 010, 014, 016, 017). frk_017's travel time from Frankfurt is not stated as minutes because nobody confirmed one; a session should check. Push failed late in the window (expired token); commits are local and left to the Run health step.
- **Stuttgart (live, 6 to 9 trees):** verify pass (3 of the 9 leads were enough: Schillereiche, Wernhalde sequoias, Jahneiche; the rest of the register has no measurements and stays leads), write pass with German overlay, photo pass approved all three. The Jahneiche (over 300 years, one Wikipedia source) is now the page's oldest tree.
- Not done: I tried merging del_011 and then reverted it, because the entry below records it was held on purpose (register-dead neighbour, removed slug). No new trees this window.

## 2026-10-18 night run (retry): written-but-unmerged trees, rung 4

The rich-or-reader rule is off since 10-18, so the ten trees earlier runs refused were merged again. Live: London Marble Hill Black Walnut (lon_029), Salt Lake City Mount Olivet Linden (slc_006), Leipzig lpz_021, lpz_022, lpz_023, Vienna Prater black poplar (vie_059, approximate pin, last photographs 2014, said on the page). German overlays for Leipzig and Vienna written; city counts fixed. Dropped lpz_019 as a twin of lpz_021 (same ginkgo; its access note was an internal "hold" line). Not merged: del_011 (stands on a register tree marked dead, and its slug is a removed redirect), ftw_018 and spk_015 (story now written, but fort-worth access ground unknown and Grant Park may not be a findable small site), kyw_001 (no Key West city file yet), std_001/nsb_001 and fdl_001 (famous batches with no city file). The 60 READY leads are still not turned into verified files; stale research files left alone. Mount Olivet's address looks odd (1342 W vs the pin) and wants a check.

**Vienna photographs (photo-judge pass, recovery lane):** 80 open candidates for 19 trees judged, 3 approved, 0 held, 77 rejected (Gugerell's general park views, station interiors, plaques, bark close-ups). Each approval was viewed at full size; filename names the Naturdenkmal and the geotag sits within 25 m. Approved, with reversal:
- vie_049 Maurer Schubertpark Lime: Schubertpark_Mauer_Naturdenkmal_03.jpg (CC BY-SA 4.0, Funke). Undo: `python3 scripts/photo_apply.py hold vie_049 "https://commons.wikimedia.org/wiki/File:Schubertpark_Mauer_Naturdenkmal_03.jpg" --reason "reversed"`
- vie_056 Oberlaa Horse Chestnut: Naturdenkmal 808 Hintere Liesingbachstrasse1 Rosskastanie (CC BY-SA 3.0 AT, GuentherZ). Undo: `python3 scripts/photo_apply.py hold vie_056 "https://commons.wikimedia.org/wiki/File:Naturdenkmal_808_2014-05-10_(51)_Wien10_Hintere_Liesingbachstrasse1_Rosskastanie.JPG" --reason "reversed"`
- vie_058 Strassergasse Oak: Naturdenkmal 671 2012-07-31 0003 Strassergasse Stieleiche (CC BY 3.0, GuentherZ). Undo: `python3 scripts/photo_apply.py hold vie_058 "https://commons.wikimedia.org/wiki/File:Naturdenkmal_671_2012-07-31_0003_Wien19_Strassergasse_Stieleiche_GuentherZ.JPG" --reason "reversed"`

Two things for a later session: the newer plaque on vie_055 (Türkisgasse) reads "Schwarzpappel, Populus nigra", which settles the register/cadastre conflict in the cadastre's favour. And Theodor-Körner-Park has a stone reading "Theodor Körner Eiche 1813 1913", so vie_045 may be a 1913 commemorative planting; check that before the page claims an age. photo_light.py could not run here (no PIL).

**Photographs for the five new trees (photo-judge pass, recovery lane):** 18 open candidates for lon_029, lpz_021, lpz_022, lpz_023 and crd_004, all viewed, 2 approved, 0 held, 16 rejected. Approved, with reversal:
- lon_029 Marble Hill Black Walnut: Jim Linwood's Flickr view (CC BY 2.0), named file in the Commons category for this tree; pinnate leaves, near-black ridged bark, the forked trunk with its hollow matches the CC BY-SA "Marble Hill Black Walnut" set. Undo: `python3 scripts/photo_apply.py hold lon_029 "https://commons.wikimedia.org/wiki/File:The_Black_Walnut_Tree_Of_Marble_Hill_Park,_London._(4621674542).jpg" --reason "reversed"`
- lpz_023 Probstheida Village Green Oak: Leipzig Stieleiche Russenstrasse (CC BY-SA 4.0, Reise Reise), Commons category of the natural monument, geotag 30 m from the pin; broad crown wider than tall at April bud-burst. Undo: `python3 scripts/photo_apply.py hold lpz_023 "https://commons.wikimedia.org/wiki/File:Leipzig_Stieleiche_Russenstra%C3%9Fe.jpg" --reason "reversed"`

No photograph yet: lpz_021 (Pixelkaktus's seven files are the sign, bark and leaf close-ups; the one whole-tree view has a blown white sky and a shrub over the trunk), lpz_022 (only candidate is the Schillerlinde 158 m away), crd_004 (a sculpture show garden). For a session: the lpz_021 sign at the tree reads 19 m and 260 cm girth, against the cadastre's 24 m and 357 cm on the page.

## 2026-10-18 night run (13:43 UTC): reader photographs, rung 1

Visits last 7 days: 1980. Rung 1: two app photographs of lis_014 (Yew of Campo Santana, Lisbon) looked at and both rejected: they show a bleached dead trunk laid on a mound beside the pond, not a living yew. Open question for a session: that dead wood stands 5 to 25 m from our pin, so the yew may have died or been cut down. Check the garden (Jardim Braamcamp Freire) before the page keeps claiming a living 14 m yew; not retired, nothing could confirm it from here. Nothing else done in this window beyond that: shelf lanes untouched.

## 2026-10-18 session: near-a-tree banner in a park

**Changed in the app (next build):** the "You are 40 m from ..." banner now works in a park with many trees. Before, it only looked at the single nearest tree, so other trees close by never got a banner, and a new banner could push the previous one off the screen. Now each tree gets its turn, nearest first, one banner at a time, and the next one comes only once you walk on. Standing still in Parc d'Egmont (eleven trees within 50 m) gives one banner, not a new one every nine seconds. The banner now also shows on the tree's own page (Hidde: "deze uitzondering hoeft van mij niet"), and tapping it there opens Collect.

**Checked:** build plus screenshots on the iPhone SE simulator (the park while standing still, the tree page). Not checked: a real walk through the park, and the tap itself (simctl cannot tap). Still no push notifications and nothing in the background, as it was.

## 2026-10-19 session: Hidde's photo review round 2 applied, three photographs live

- **Live with a photograph now:** the Independence Spruce in Helsinki, Takinoya no Hidarimakigaya in Yabu and the Münzgrabenstraße plane in Graz. Each file names the tree, and each tree is unique at its spot.
- **Held, not dropped (13):** Hidde's "Twijfel" picks (the new button, added today for "good photo, not sure it is this tree"), plus good photos with no tie to the trunk. One was the Corstorphine sycamore clone in the Botanic Garden rather than the churchyard tree; others were shore-wide cherry views, one of two crutched mulberries, and a generic Brisbane file.
- **Rejected (12):** recorded in data/photo-queue.json. Seven good picks were for trees that already had a photograph (Seattle, Utrecht, Los Angeles, Berlin), so those were left alone.
- **Yield:** 3 approvals from 35 candidates, against 5 from 212 in round 1. Even with the strict gate, Hidde's time mostly goes to photos we cannot tie to the trunk. The ones that ship are single named trees with the name in the filename.
- Also fixed: a comment in AmbassadorLine.astro, from this morning's profile commit, sat in the markup where preflight reads it as English page text. It is moved into the frontmatter, wording unchanged.

## 2026-10-18 session: Hidde's photo review, round 2

- **His unapplied verdicts are in:** 108 verdicts given on the review page after the 10-01 pass were never applied. Now 59 rejects are recorded in data/photo-queue.json, and his 17 "good photo" picks are held, not approved: none could be tied to the trunk. They named only the place, e.g. a Trsteno file of the plane tree offered for the ginkgo, or had geotags 86 to 561 m off.
- **Round 2 on the page** (https://claude.ai/artifact/T4TtkFaSAmJXdTVJy1unHp): 35 candidates for 25 trees, roster cities first. The gate is new and strict: the filename must name a tree or the species, AND either the geotag is within 60 m of the pin or the filename names the species and the site. Built by out/tmp/review_batch.py; images numbered from 1001 so old verdict ids never collide.
- **Applying round 2 (a session does this):** read `verdicts` with ArtifactData, take only ids whose number is 1001 or higher, rejects to photo_verdicts.py, goods through the identity check (geotag or named file), then preflight, commit, push.

## 2026-10-18 session: Lady Liberty and a Cedar Breaks bristlecone from the US register sieve

**New on the site, both with photographs:** Lady Liberty in Longwood, Florida (bald cypress, about 2,000 years by Seminole County's estimate, 10 m round), and the Spectra Point Bristlecone at Cedar Breaks, Utah (Utah's state champion, 8.26 m round, past 1,500 years; pin confirmed because the photo geotag sits 10 m from the register's GPS). Both are lone-tree places.

**The sieve:** six state registers with coordinates (Florida, Ohio, Utah, Oklahoma, New Jersey, Delaware; 1,800 public rows), Commons geosearch within 100 m of the top 50 per state. 11 of 300 had a tree-named photo nearby; 2 were real and epic. The state register counts as the official source, so verification was quick: about 60k tokens for both, done in-session without agents, against about 100k per tree in Australia. Script: out/tmp/us_sieve.py, output out/us-register/ (not in the repo). Weak hits not pursued: the Ohio champion Atlantic white cedar (named photo, small tree), the Hollywood FL baobab (girth uncorroborated before), the Dover elm.

## 2026-10-18 session: four Australian giants from the big-tree register trial

**New on the site:** the Giant Tingle Tree near Walpole (with photo), the Prison Boab near Wyndham (with photo), the Ada Tree near Powelltown and the Dave Evans Bicentennial Tree at Pemberton. The Gloucester Tree got its first photograph. Walpole, Wyndham and Powelltown are lone-tree places under Hidde's new rule of the same day: a lone tree goes live as a tree page, and its place page stays out of Google until it has four.

**How:** Australia's National Register of Big Trees (923 trees, All Rights Reserved) was used as a finding aid only. A free script searched Commons for the 107 trees scoring 500+ points; 25 had filename hits, about 6 were real candidates. Then one verify pass (127k tokens), one photo pass (153k) and one writing pass (133k): roughly 410k tokens for 4 trees plus a photo, about 100k per tree, well over the 15k target. The sieve is cheap, but most register giants have no usable photo and no second source.

**Kept as leads:** Grandma Tingle (written, but no trunk photo or recognition line), the Wonnerup Giant (approved photo, only the register as source), the Woodford blue gum, and Big Red, Grey Bark, Pleated Lady, Forest Lord, The Tyrant and Hawke (register only). The sieve output is in out/au-register/ (not in the repo).

**Open:** the Pemberton FAQ and the Gloucester story call it "second-tallest fire lookout behind Dave Evans", but Dave Evans was never a fire lookout. Needs a source check. The Gloucester pin sits about 260 m from two photo geotags.

## 2026-10-18 A stranger in Lisbon gave two trees their first photographs
A signed-in reader (not our account) collected the Moreton Bay Fig and the Prickly Paperbark of Jardim Constantino in the app this morning and took three photographs. Neither tree had a photograph. Looked at all three: fig whole with its surface roots and the Prometheus statue behind (lead), the fig from under its crown (added beside it), the paperbark's white peeling bark (lead). Published with sightings_publish.py, mail off; verdicts in data/judgements.json. Both pages now qualify for Google (Lisbon is on the proven roster). Found because Hidde asked about the two collections in the digest: `sightings_inbox.py --status` reads only the local queue, so it said 0 waiting until the inbox itself ran. Also: judgement.py --scan reads the queue, which sightings_publish empties, so scan before publishing.

## 2026-10-18 iOS scheduled run: the layout sweep's three DRIFT findings fixed
Breakage, not product. ios.yml had failed three runs in a row on SweepFrames DRIFT only (all 224 tests green). Two causes, neither a real misalignment. (1) The early-adopter sheet had no named root, so its "Done" (BrandSheet's 24) was measured against the profile page behind it (20); it now carries `early-adopter-sheet` as its root, like the sign-in and paywall sheets. (2) The add-a-tree sentence was centred text whose widest line measured 0.881 of the screen, a hair over the centred-text exemption (0.88), so it read as starting at 26 against the buttons' 20; the 10-16 fix (full-width frame) did not move the measured box. It now takes the headline's 18 at the sides, wraps as two balanced lines and reads as centred. Ratchet untouched. appfit locally: 0 findings on 39 screens (16 Pro Max, iOS 18.6); screenshots looked at.

## 2026-10-18 session with Hidde: new trees without a photograph go live again; the photo fetcher keeps to its cities
- New trees no longer have to be rich to ship (`ADD_NEEDS_RICH = False` in scripts/findable.py). Hidde: "let new trees without a photo go live again (readers and Bing only)". Google cannot see them until they get a photograph (the noindex change below), so the hold bought nothing and kept 60 READY leads and 28 written trees idle through 38 empty night attempts. Every other gate holds (photo-or-pin, told-apart, a named source, the reason floor), so not all 88 will pass. prepare.py and passcheck.py briefs now print the rule from the flag. Undo: set it True.
- `photo_fetch.py` ignored `--city` whenever `--zero` was given and fetched every photo-less city (Dallas, Oss, Rotterdam) instead of the pages Google shows. Named cities now win, `--city a,b` works, and `--roster` fetches the frozen roster most impressions first; prepare.py points the night run at `--roster`.

## 2026-10-18 session with Hidde: the extra "Is it ...?" step on Add a new tree is gone again
Hidde: "deze vraag staat al op het eerste scherm ... deze stap is onnodig". The collect list already names our trees above "Add a new tree", so that button goes straight to a new tree as before. The fold afterwards stays ("Is this <name>?" and "Another of our trees" on a tree of yours); he wants it. CONVENTIONS.md says not to bring the step back.

## 2026-10-18 session with Hidde: no more second copies of our trees in the app
Hidde found a second Town Hall Plane among his own trees in Baarn, made by "Add a new tree" right beside ours. App only, LIVE on main (merged 2026-10-18; ios.yml green on the branch: build, unit and UI tests, layout gate after one SMALL fix on the new button): "Add a new tree" with one of ours within 30 m first asks "Is it <name>?" (yes collects ours with the photo, no adds the new tree as before), and a tree of yours within 30 m of ours shows "Is this <name>?" with "It is this tree", which folds it into ours without deleting anything (`Sightings.fold`). The server already matched at 30 m, so the site never had the duplicate. New unit test `aNewTreeOnTopOfOursIsAskedAbout`. Second step, same day, because our pins are not always right: the box also offers "Another of our trees" (or "Already on our map?" with nothing within 30 m), the collect sheet's nearby, closest and search list inline; a pick further than 400 m also sends a pin correction. For Hidde: next build carries it; open your Baarn copy and tap "It is this tree".

## 2026-10-18 session with Hidde: Google now sees only tree pages with a photograph
The 10-09 exception that let finished tree pages without a photograph back into Google is closed (`RETURN_ENRICHED = False` in scripts/thin_pages.py). 1,128 tree pages (1,810 urls with their translations) get the googlebot-only noindex on the next deploy; readers still see them, Bing keeps them through sitemap-bing.xml, and each returns to Google the day it gets a photograph. Why: the digest's "Is enriching working" table showed those pages earned 0.05 impressions a page after they came back on 10-12/13, and the 10-13 rule (widen only once returned pages earn impressions) was never met. Hidde: "Yes, take the 1,128 photo-less pages out of Google; Bing keeps them." Undo: set it True. Next look: mid-November, impressions per photographed page.

## 2026-10-18 thirty-eighth attempt: nothing shipped
Pulled; no claims; 60 READY leads and 28 written trees still held by the rich-or-reader rule (recovery mode); enrich empty; BACKUP is Denver only (no licence, needs Hidde's ask). Nothing dispatched.

## 2026-10-18 thirty-seventh attempt: nothing shipped
Pulled; no claims; 60 READY leads and 28 written trees still held by the rich-or-reader rule (recovery mode); enrich empty; prepare BACKUP is Denver only (no licence, needs Hidde's permission ask). Nothing dispatched.

## 2026-10-18 thirty-sixth attempt: nothing shipped
Pulled; no claims; 60 READY leads and 28 written trees still held by the rich-or-reader rule (recovery mode); enrich empty; langcheck --next has no city over 10 impressions; Denver still has no licence or coordinates. Nothing dispatched.

## 2026-10-18 08:29 window: one sighting verdict, no trees
Rung 1: sighting c86ff6bf (owner-account tulip tree, Cantonspark, Amersfoort area) judged lead: no register or Wikipedia entry nearby, no size or note, photo not on disk. Rung 2: smoke "skipped" is just the path filter on log-only pushes; the iOS app's scheduled runs fail on appsweep DRIFT findings (collect-intro and collect-away 'Photograph a tree you are standing in fro...' starts at x=26 vs 20; early-adopter-sheet 'early-adopter-done' x=24 vs 20), while the push-triggered run at 15:36 passed. Swift layout work, not doable on this Linux runner: For Hidde/a Mac session. photo_hunt --recheck london: 0 new candidates; photo_fetch --zero ignored --city and pulled filename-only junk (Dallas, Fort Worth, Oss, Rotterdam), none approved. Verified-unpublished trees are still the held ones; no write pass. Visits last 7 days: 1920.

## 2026-10-18 thirty-fifth attempt: nothing shipped
Pulled; no claims; 60 READY leads still held by the rich-or-reader rule (recovery mode), so no write pass; langcheck --next lists no city with impressions. Nothing dispatched.

## 2026-10-18 thirty-fourth attempt: nothing shipped
Pulled; no claims; 60 READY leads and 28 written trees still held by the rich-or-reader rule (recovery mode); enrich empty. Denver scouting note re-read: no licence statement and no coordinates, needs a permission ask to Colorado Tree Coalition (Hidde's call), so it stays stalled. Nothing dispatched.

## 2026-10-18 thirty-third attempt: nothing shipped
No claims; 60 READY leads and 28 written trees still held by the rich-or-reader rule (recovery mode); enrich empty. Detroit retry: Michigan Botanical Club site now answers (200), but its homepage links no Big Tree register page or licence, so it stays stalled, marked retried 2026-10-18. Nothing dispatched.

## 2026-10-18 06:37 window (7-day visits: 1910 visits, 2510 page views): one photograph
Rung 4 photos lane. photo_fetch.py --zero (it ignores --city and fetches every city) gave 35 candidates; I looked at the pixels and approved one: the Ypres Four-Trunked Survivor (sweet chestnut in leaf, Wikidata-linked file, 6 m from pin, CC BY-SA 4.0 Stad Ieper). Reversal: set ypr_005 photo status back to missing. The rest were leaves, hands, indoor or unrelated shots; photo_verdicts.py cannot record rejects for iNat candidates (no matching page), so those come back next sweep. Sequoia's Sentinel Tree has 13 new candidates queued but photo_fetch --zero did not fetch it; not judged. Health still shows Smoke skipped and iOS scheduled failure (needs a Mac session). Enrich empty; 60 READY leads and 28 written trees still held by the rich-or-reader rule.

## 2026-10-18 thirty-second attempt: nothing shipped
Pulled; no claims; 60 READY leads and 28 written trees still held by the rich-or-reader rule (recovery mode); enrich empty; only backup is the Detroit retry (host unreachable earlier). Nothing dispatched.

## 2026-10-18 thirty-first attempt: nothing shipped
Pulled; no claims; 60 READY leads and the 28 written trees still held by the rich-or-reader rule (recovery mode); enrich empty; scout target Detroit retry unchanged. Nothing dispatched.

## 2026-10-18 thirtieth attempt: nothing shipped
No claims; 60 READY leads still held by the rich-or-reader rule (recovery mode), no write pass. Photo recheck on London found no new candidates (queue file touched only). Nothing dispatched.

## 2026-10-18 02:38 window (7-day visits: 1908 visits, 2571 page views): nothing shippable
Inbox empty; health flags only Smoke "skipped" (log-only pushes) and the iOS scheduled-run failure (needs a Mac session); enrich empty; 60 READY leads and 28 written trees still held by the rich-or-reader rule (recovery mode). Nothing dispatched, no claims.

## 2026-10-18 twenty-ninth attempt: nothing shipped
Pulled; no claims; 60 READY leads still held by the rich-or-reader rule (recovery mode), so no write pass. Nothing dispatched.

## 2026-10-18 twenty-eighth attempt: nothing shipped
No claims; 60 READY leads still held by the rich-or-reader rule (recovery mode); langcheck --next has no city over 10 English impressions. Nothing dispatched.

## 2026-10-18 twenty-seventh attempt: nothing shipped
Pulled; no claims; sightings inbox empty; 60 READY leads still held by the rich-or-reader rule (recovery mode), so no write pass. Nothing claimed.

## 2026-10-18 00:00 window (7-day visits: 2093 visits, 2901 page views): nothing shippable
Inbox empty; enrich empty; 60 READY leads and 28 written trees still held by the rich-or-reader rule (recovery mode); scout target is the Detroit retry, host unreachable as in earlier attempts. Nothing dispatched, no claims. Later attempts in this window should not repeat the orientation.

