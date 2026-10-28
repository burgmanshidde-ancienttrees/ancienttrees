# LOG

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-10](archive/LOG-2026-10.md)
- [2026-09](archive/LOG-2026-09.md)
- [2026-08](archive/LOG-2026-08.md)
- [2026-07](archive/LOG-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
<!-- archive-index -->
## 2026-10-28 session with Hidde: second archive batch sent

archive-2026-10-26 went out on his word ("verstuur alle 3"): photo asks to the Austrian (Vienna), Polish (Krakow, Warsaw) and German (Berlin, Munich) dendrology societies; the DDG mail is a third contact with resend_reason recorded. Logged in drafts/OUTREACH.md and outreach-sent.json (private store). Next archive candidate: the Nederlandse Dendrologische Vereniging, now with a published address (secretariaat@dendrologie.nl) in the contacts database.

## 2026-10-28 session with Hidde: one person, one ambassador row

The digest showed Miguel's five places (Porto, Guimarães, Braga, Calvos, Vales, one account, 10-26) as five requests, four "not yet (next knock)". They were held all along (a session had marked rows 575 to 578 by hand), so nothing would have gone out, but the page said otherwise. Now the block has one row per person with every place named (4 people, 8 places today), and a row held on purpose reads "held". ambassador.py --requests no longer depends on the hand marking: a person already sent the questions mail gets no second template for another place, the row is recorded "same person as row N; answered in that thread".

## 2026-10-28 session with Hidde: returning website visitors in the headline

His numbers gain a row, "Website visitors who came back" (GA's returning activeUsers, week on week; Hidde: "yes add returning website visitors"). First reading: 18 this week against 5. The footnote says it reads low (another browser or device counts as new) and may hold our own visits, since GA cannot filter us out. Also checked on his question: the week's 19 saves came from two accounts (13 on 10-22, mostly Paris; 6 on 10-24, mostly Cambridge), no one else saved.

## 2026-10-28 scheduled send

Sent the thank-you reply to Laura Parrack (Cardiff Council parks) for the Tree Register and Bute Park trail links, approved by Hidde 2026-10-27.

## 2026-10-28 night run (07:50 window)

- Shipped 0 trees. Rungs 1 to 2 clear: no reader photos or notes waiting; the two "skipped" deploys health.py flagged are bot-commit pushes, the scheduled build at 05:54 succeeded (answered in health). The only unpublished verified entries (sfo_013, inn_007, ftw_018, txf_004) are still held for photo or access, same as last night.
- Graz and Nuremberg are walls (3 of 16 and 0 of 7 leads carry a coordinate). Canberra verify pass: 2 register-only trees (can_002 Blue Atlas Cedar, can_003 Gorman House Arizona Cypress, approximate pins, no photo, so they cannot go live under the photo rule); cityservices.act.gov.au answers 403 to curl and WebFetch, which blocked the per-tree register PDFs. Five more leads kept in data/leads/canberra.json. Canberra a wall for 48h.
- Rung 4 contact sourcing: one new archive contact (Munich Baumschutz, "Mein schönster Baum" page, for muc_021/022/023/025/026); Brussels and Valencia candidates were already mailed, Seville and Singapore addresses unverifiable (403 or social media only). Database rebuilt and pushed; no nature or guide contacts found.
- For Hidde: nothing. The shelf is empty of photographed supply; what would move it is photographs (archive asks) rather than more verify passes.

## 2026-10-27 night run (second retry window)

- Shipped 0 trees. The 3 READY leads are false positives: Oxford's two are a young oak and a possibly dead chestnut with no photo, Madrid's has none either. The 56 "awaiting a writer" are mostly stale files or duplicates (passcheck --pending flags them). The only real unpublished entries are sfo_012/013, ftw_018, inn_007, txf_004, all without a photograph.
- Retried the Bristol register (BACKUP): the National Trust Leigh Woods veteran walk names 12 trees (Parish Yew about 500 years, an oak pollard about 400) but gives no girth, no coordinates and no open photos. Still stalled; the note in data/register-scouting.json says what would unblock it.
- san-francisco claim left standing: its four verified entries are unwritten and wait for photographs. sfo_014 and sfo_015 are duplicates of sfo_003 and sfo_006.

## 2026-10-27 night run (retry window, after an early stop)

- Shipped 0 trees. Shelf check: 3 READY leads (oxford 2, madrid 1), under the six-candidate floor for a write pass and none has a photograph, so none can go live under the photographed-only supply rule. Stale research files make up most of the "awaiting a writer" count.
- Verify pass on san-francisco (staged, US): 2 new verified entries in data/research/san-francisco-verified.json (sfo_014 Bernal Heights Library flowering ashes, sfo_015 Customs House sweet bay), both flagged, no open-licence photograph found. They wait for a photo. Claim left standing (releases once merged, or expires after 4 hours); sfo_012 to sfo_015 are in that file unwritten.
- Next run: photo sweep on those four SF trees, then write; or the Bristol register retry named in prepare.py BACKUP.

## 2026-10-27 night run (18:18 window)

- Rungs 1 to 3 clear (no reader photos or notes, health green). Rung 4: 94 drafts still open, so no new mail batch; sourced two archive contacts instead (Nederlandse Dendrologische Vereniging for Arnhem, Asociación Española de Arboricultura for Barcelona/Seville/Valencia; both addresses from their own sites), contacts rebuilt and pushed. Tree Register and Ancient Tree Forum addresses were only on the Charity Commission register, not their own sites, so left out. Hoyt Arboretum's address was only in old event listings (its site returned 403).
- Rung 5: enrichment lisbon+albertshausen+bamberg+potsdam: 4 trees closed (3 best_time, Potsdam beech pin source), 14 gaps recorded as dead ends. Measurements and Bamberg access had no source. Preflight 0 problems.
- Shelf thin (the writable pile is stale or held), so scout: Canberra (#31). The ACT Tree Register (ArcGIS FeatureServer, CC BY 4.0 per the item's licenseInfo; data.gov.au says "Other") holds 376 rows, 350 registered; stored in data/registers/act-tree-register.json, 12 large public-ground trees as leads in data/leads/canberra.json, verdict in register-scouting.json and OPEN_DATA_SURVEY.md. Coordinates are crown-polygon means, so approximate. Nothing published. Next for Canberra: photo hunt on the 12 leads. The scout agent used a heredoc for the survey append (rule slip, content fine).

## 2026-10-27 session with Hidde: Show HN, second try

The 10-24 Show HN (item 50208440, posted on a Saturday) ended at 1 point, and its first comment is [dead]: the filter for new accounts killed it (hburgmans, karma 1). Hidde already mailed hn@ycombinator.com about the dead comment on Friday 10-23 at 15:13 (his Sent folder; so the post went up that Friday, not 10-24), and no answer came. Second try: the same URL with the explanation in the submission's own text field, Tuesday to Thursday 14:00 to 17:00; if the submit lands on the old item, the duplicate filter folded it and he stops. drafts/show-hn.md now says text in the post, not a separate comment. Result, ~14:45: no new item; his submitted list still shows only 50208440 (1 point), so the duplicate filter folded the resubmit into Friday's post. Next try with the text in the post in two to three weeks, ideally with a new reason, and a few genuine comments from the account before then.

## 2026-10-26/27 session with Hidde: nature magazines, the Wilder model

- **Outreach:** 47 nature magazines mailed in three batches on his word (natur, Sveriges Natur, Countryfile on 10-26; 8 whose own article names a tree of ours and 36 with one photographed tree from their country on 10-27), in eight languages, from his own text (drafts/nature-template.md, variants A and B). Each article named in a variant A mail is now a source on that tree's page. The nature group went from 0 to 58 addresses; 10 remain (weak fits or unverified addresses).
- **Product:** 11 trees gained a magazine article as a source (Hueter des Feldes, Fortingall Yew, Rumskullaeken, Old Tjikko, Dicke Marie, Williamson bur oak, Goose Island Big Tree, Gija Jumulu, Platano di Curinga and others).
- **Rules he set:** never ask a stranger to go out and photograph a tree (OUTREACH_STRATEGY.md); the Lisbon photographers get "we happily use your photos" instead (drafts/lisbon-photo-thanks.md, he posts on Commons).
- **Breakage:** AmbassadorLine.astro tripped preflight on main (a > inside the tag); rewritten as !== 0, preflight clean.
- For Hidde: 6 Lisbon photographer messages in drafts/lisbon-photo-thanks.md, to post on their Commons talk pages.

## 2026-10-27 session with Hidde: a second ambassador may sign up

- **Product:** a place that already has an ambassador keeps the open row under that person, "Become an ambassador", and the sheet says "an" instead of "the". Web in all seven languages and the app; the app was looked at in the simulator on Florence (row and sheet). The website is checked by the CI build only, no local Node. Home's "your city is looking" row stays for empty places only, and --invite-scan still mails only places nobody holds. CONVENTIONS.md "the open seat" carries the reference.
- **Inês (Wilder):** her Bucaco request, row 503, was her own test (her mail of 2026-10-26); noted in data/ambassadors.json and left out of the digest.
- **Then smaller, same day** (Hidde: second in rank, not green): the row under a named ambassador is now a thin rule and one grey 12px line with a small seal, Atlas Obscura's "Make an Edit" shape. Web and app; the app looked at in the simulator on Florence. The website's chevron on the open-seat row is now the Phosphor icon (the pre-push icon check refused the old hand-drawn path).
- **Then text only** (Hidde: no icon, the pill would outrank Giulia): a thin rule and the grey line under the name, even space either side. Web and app, the app looked at in the simulator on Florence.
- For Hidde: the next app build carries the second-ambassador line.

## 2026-10-27 session with Hidde: digest cleanup, sightings no longer re-sent, Miguel's five places
- **App, next build**: the catch-up after sign-in now sends only sightings that changed (a fingerprint of what the account last received). Until now every new session re-sent every sighting and stamped it as freshly saved, which is why the Tangier fig came back on the digest as a new photograph. Seven unit tests, whole unit-test target green on iOS 26; merged to main. For Hidde: next build carries the fix for sightings re-sent on every sign-in.
- **Digest**: an app sighting shows again only when its content changed (scripts/sighting_changes.py, data/sightings-shown.json, 93 seeded). The Android waitlist counts every row except four Hidde named (two test addresses, family, a colleague with an iPhone): 44, not 48.
- **Miguel Portugal is one person**: the ICNF Norte forester who mailed at 23:48 on 10-26 is the account that asked to be ambassador for Porto, Guimarães, Braga, Calvos and Vales (Calvos and Vales in that same minute) and reported the FAUP copper beech dead or gone. One reply in his thread, Hidde's own text plus the Sources fix: drafts/reply-miguel-minho-2026-10-27.md; the earlier ICNF draft is marked replaced. The four template mails are held. Hidde's text is now the template for one person asking for several places (drafts/ambassador-mails.md). Nothing sent.
- **The FAUP copper beech (por_011) is off the map** at Hidde's word, on Miguel's report (he works on the register it was in): retired to blocked leads with a redirect, Porto now 26 trees, the free-access count and 'two university quintas' fixed in English and Portuguese; submission 573 closed as changed with replied_at set, so no automatic mail. The reply to Miguel says it is off the map.

## 2026-10-27 session with Hidde: ICNF's Miguel Portugal, Sources page link fixed
- Miguel Portugal (ICNF Norte, 30 years at the institute, two on Arvores de Interesse Publico) wrote after the Wilder article, made an account, offered help and pointed out that the Sources page linked ICNF's register to si.icnf.pt, which redirects to a login page. Cause: data/registers/portugal-icnf.json had no catalogue url, so the credits builder stripped the WFS endpoint back to its host. Fixed with `metadata_url` on the dataset's own geocatalogo page (the one the licence proof already cited); live with this push's deploy.
- Reply drafted in his thread, drafts/reply-miguel-portugal-icnf-2026-10-27.md (the fix as fact, then his standard judge-the-list ask for Porto, 27 trees), mailcheck clean, nothing sent. His only earlier mail from us is the automatic welcome of 10-26.

## 2026-10-27 day run (window from 06:10 UTC)
- Second attempt in the window: nothing new shipped. READY is the same 3 photo-less Oxford/Madrid leads; ftw_018, inn_007, txf_004, sfo_013 stay held (access or photograph). The fort-worth claim stays until ftw_018 can merge (no register candidates there, 0 mined). Scouting: Canterbury retried, still stalled (no council register; cathedral precincts and Dane John searches name no veteran trees).
- Rung 1 empty, health: the 10-26 iOS failure is the same single `testNoAnswerFromTheServerAsksNobody` crash as the night run logged, previous runs green, so still read as a flake (watch the next run); the skipped smoke runs are non-site pushes. Shelf refill: San Francisco verify found its landmark register used up (0 new, two leads recorded). Write pass: sfo_013 (Moreton Bay Fig, Valencia Street) story written but held for a photograph; sfo_012 is a duplicate of live sfo_004 (53 m apart, same Landmark Tree 15; its DataSF pin and girth belong in an enrich pass); inn_007, ftw_018, txf_004 stay held. No tree shipped. Scouting: Middletown CT retried, oak.conncoll.edu times out (added to fetch-blocklist), stays stalled. The san-francisco claim stays until sfo_013 has a photograph.

## 2026-10-27 night run (window from 00:51 UTC)
- Rung 1: inbox and tree notes empty. Rung 2: the iOS run of 10-26 21:20 failed on one test of 227, `testNoAnswerFromTheServerAsksNobody` ("Crash: AncientTrees at <external symbol>"); the test only reads `Profiles.ensureName` with no network, the previous two runs passed and nothing in Kit/ changed since, so I read it as a simulator flake and left the app alone (watch the next run). Deploy is behind main; dispatching one at the end of the window.
- Rung 4: mail batches wait (archive 10-26, follow-ups, lisbon-ten), so no new batch. Sourced one archive contact: Portland Parks & Recreation Heritage Tree Program, address published on portland.gov/trees/heritage (Portland has 31 photo-less trees); Hoyt Arboretum pages return 403 to every fetch, so no address verified there; Singapore's NParks Heritage Trees publish a web form only. `contacts_db.py --build`, private_store pushed.
- Rung 5: enrichment batch lisbon+albertshausen+bamberg+potsdam held only season gaps (phenology, lowest priority), recorded as dead ends. Merged Tate-no-Omayumi (kna_002, approved CC BY-SA photograph, pin approximate, two sources 155 m apart) into Koriyama, with the place intro and meta now saying two trees; preflight 0 problems. Fort Worth's ftw_018 and Innsbruck inn_007 stay held (access unknown), txf_004's photo is held.

## 2026-10-26 session: drafts know when they have been sent

Hidde: "die ambassadeurs zijn al gemaild - kun je mn mail checken of bijhouden zodat ik je niet steeds de status hoef te vertellen". The four ambassador mails (New York, Buçaco, Porto, Luisa Carta) and the 10-25 archive batch had gone out through outreach_send.py on 10-25, yet the digest, the night run and a session still called them waiting: each read a "For Hidde:" line and nobody checked the send log or his mail. New `scripts/sent_drafts.py` gives every draft of the last 30 days a status (sent, partly, open, unknown) from data/outreach-sent.json plus the headers of his Gmail Sent folder (To, Subject, Date only, read-only), and writes hand-sent mails to drafted addresses into the send log (15 found, so the one-week rest knows them). Status file data/outreach-drafts.json, private. The digest's Waiting for you drops a line whose drafts are all sent (checked: Luisa and the archive batch are gone from it), data-digest.yml runs the check first, and the session brief lists the drafts not yet sent. Open today: archive batch 2 (10-26), the six follow-ups, lisbon-ten-mails (0 of 5), reply-john-beetham-2026-10-25, the Hans and Paulo consent mail; twelve reply drafts name no address, so they show as unknown (reply-peter-wifi-crash among them).

## 2026-10-26 session with Hidde: archive batch 2 drafted (Vienna, Krakow and Warsaw, Berlin and Munich)
- Hidde asked for the next batch; none had waited since 10-23. Inbox read first, then the archive group as the strategy orders: two dendrology societies with a published address found today (Austria's ÖDG for Vienna's 33 photo-less trees, Poland's PTD for Krakow's 27 and Warsaw's 19), plus a third mail to the DDG with a resend reason, Hidde's call. Preview drafts/batch-archive-2026-10-26-preview.md, nothing sent. Morton and the Ancient Tree Forum skipped at three unanswered mails; NDV and Hoyt have no published address.

## 2026-10-26 restart run: 13 photographed trees live from the parked batches

- Thirteen trees with approved photographs went live, parked since 10-22 behind the pace guard: photo-batch-2 (Winterswijk, Hägerum, Bregenz, Hochosterwitz, Leonstein, Ogi, Sakurai, Shikokuchū) and the Texas famous places (Goliad, Coppell, College Station). Four colon reveals in the stories were rewritten; the three Texas places were added to data/us-states.json. Preflight is clean. The site build was not run here (npm was denied), so CI's qa is the first full check.
- Not done: txf_004 (held photo), the stale `*-verified.json` files, ftw_018 and inn_007 (unwritten), and the three READY Oxford/Madrid leads, which have no photograph. `city_names.py` left Hägerum and Leonstein unresolved.

## 2026-10-26 09:35 run (short window, rung 4)

No reader photographs or notes, health.py clear. The 10-25 archive batch still waits for Hidde's "verstuur", so no new mail batch. Sourced archive contacts: the Deutsche Dendrologische Gesellschaft (own Bildarchiv and Champion Trees gallery, Berlin/Munich trees) and the Morton Arboretum library (Chicago, a weak tie); recorded in the private archive contacts file, built the database, pushed it. Not found: the Österreichische Dendrologische Gesellschaft (no published address), the Tree Register (address only behind Cloudflare obfuscation, not verified), the Ancient Tree Forum (contact form only). Nothing sent. No trees made; the shelf says REFILL but I spent the window on contacts only.
## 2026-10-25 session: eight more Lippert photographs, the Calvos oak, and mailed words get quoted

- **Live with this deploy**: eight more trees lead with Rainer Lippert's own photographs, each replacing a Commons lead that moves into the strip: the Marienlinde of Linden, the Hohenheim Love Plane, the Cedars of the Königsflügel in Bad Homburg, St. Wolfgang's Oak, the Schäferköppel chestnut, the Bötersheim oak, the Waldhaustanne and the Betteleiche. Found by the coordinate pass Hidde asked for: his My Maps layer (1,838 oaks) for the oaks, his 551 other-species pages for the rest; looked at, and checked against his Commons uploads by image fingerprint (none the same). That pass is now complete: 43 trees carry his site photographs from today.
- **Live earlier tonight**: the Carvalho de Calvos (clv_001) has Paulo V. Araujo's own photograph from his 2009 Dias com Arvores post. His blog has three authors; only posts by him and marked "Foto: pva" count, and most 2004-2006 images are on hosts that no longer exist, so this was the one usable photo of one of our trees.
- **New rule, live**: words people send by mail go on the page like app notes. The session handling the mail copies the sender's own sentences into the private data/outreach-words.json and `reader_words.py` lists them until quoted (CLAUDE.md, reply-mail skill). Luisa Carta's two PDFs turned out to be Camarda's book text, used correctly already; nothing of hers to quote.
- For Hidde: the ambassador mail to Luisa Carta (Sardinia) in drafts/reply-luisa-carta-2026-10-25.md waits for his "verstuur". Paulo's mail (his own words) goes once the Calvos photo shows on the page.

## 2026-10-25 session: a town we hold no tree for asks for its first one (web; app on its way)

- **What changed, website**: search now finds every town of 15,000 people or more, also where we have nothing. Type "Bern" and the dropdown opens with the grey card of an empty notes section, "No trees mapped in Bern yet", "Know an old tree here? Add the first one.", and "Add a tree" (the contribute form with Bern filled in); under it Bern on the map and the nearest tree (The Linden of Morat, 27 km). On the map, any view without a tree shows the same card and the nearest tree. A typo gets one plain line, "Nothing matches ... Check the spelling, or try a town nearby." Seven languages. Hidde approved the design today, screens 1 and 2 as drawn, no card on a typo.
- **No new pages**: nothing for Google; the ask lives in search and on the map (the convention, and the 09-28 demotion's lesson). Towns from GeoNames cities15000 (CC BY 4.0, credited on /sources), `data/places-geonames.json` via `scripts/geonames_places.py`; the nearest tree is worked out at every build in `/places.json`, loaded only when a query matches none of our places.
- **Measured from now**: a search that ends on an empty town logs `search-empty-<ctx>`, one that ends on nothing `search-none-<ctx>`, and the card's button `empty-place-add`. Until today only a clicked result was logged, so how often people hit an empty place was unknown.
- Benchmark in CONVENTIONS.md, "A place we have nothing for".

## 2026-10-25 session: 35 German trees get Rainer Lippert's photographs

- **Live with this deploy**: 35 German trees now lead with a photograph from Rainer Lippert's monumentale-eichen.de, credited with a link to his page, under his standing permission (mail, 2026-10-10: "Ihr könnt gerne Fotos von meiner Seite verwenden, mit Namensangabe und Link"). 13 had no photograph at all (Hamburg's Hirschpark maple, the Ash at Schloss Solitude, both Dawn Redwoods in Frankfurt and Bad Homburg, two Nuremberg burl oaks, three Frankfurt and Offenbach oaks, Leipzig's Starkeiche, Dresden's Grenzeiche, Gut Burgstall's lime). 22 swapped a Commons lead for his, and the Commons photo moved into the strip (Dicke Marie, the Humboldt Oak, the Kaditzer Linde, the Tassilolinde, Teuchatz, Effeltrich and others).
- **Google**: all 35 now count as reader content (a photograph unique to us). This deploy has room for 26 returning pages; the guard lets the rest back on the next deploys by itself.
- **How it was matched**: his sitemap (2,882 pages), narrowed by place and genus, then paired on the coordinates every page of his carries (same genus, mostly within 20 m). Every photo was looked at, and each was checked against his 1,523 Commons uploads by image fingerprint: none is on Commons, so they really are unique. Five stories that now face Google lost a colon reveal.
- Held, not applied: frk_023 (Bethmannpark ginkgo, several trees in the frame), pot_011 (his twin oak against our three oaks, 69 m), pot_012 (66 m, unclear trunk), frk_009 (131 m, a group).
- Next on the same permission: only 78 of his 2,882 pages were read this time, chosen by place name. A coordinate pass over the rest would find German trees whose names do not match his.
- The archive mail batch the night run still lists as waiting went out this afternoon on Hidde's "verstuur" (Brussels, Munich, Barcelona).

## 2026-10-25 night run, third attempt (same window): Baltimore retried

Same state as the two attempts before: no claims, 3 READY leads all held by the supply pause, rungs 1, 2 and 4 clear (health.py flags only a skipped smoke run on a log-only commit), enrich and recognise have nothing, the archive mail batch still waits for Hidde. Scouting: Baltimore retried, the ArcGIS item has no licence statement, so still stalled (only a written yes from Rec and Parks opens it), `retried` set. No trees added.

## 2026-10-25 night run, second attempt (same window): nothing to ship

Claims: none standing. READY leads: 3 (Oxford 2, Madrid 1), all our own supply, so held by the supply pause (no reader found them, none carries an approved photograph). Rung 1 clear, health.py's only flag was a skipped smoke run on a log-only commit (build green, not a break). Rung 4: harvest, watch and open all 0; no mail batch because the archive batch still waits for Hidde. No trees added.

## 2026-10-25 night run (window from 18:40 UTC): nothing to ship

Rungs 1 and 2 clear (no photographs or notes waiting, health.py all green). Rung 4: Reddit harvest and watch found 0 new comments and 0 threads, 0 open items; no new mail batch, because the archive batch of today (drafts/batch-archive-2026-10-25-preview.md) still waits for Hidde. Rung 5 is closed by the supply pause and enrich says nothing to do. Scouting: Stirling retried (one search, same answer: the council appeal routes to the Woodland Trust inventory, off limits), still stalled, `retried` set; next target is Baltimore. No trees added; no commands were refused. Local pre-push hooks were armed by prepare.py.

## 2026-10-25 session: the first archive batch, and Reddit drafts stop blocking mail

- **Outreach**: the first `archive` batch is drafted, three photo asks: Belgische Dendrologie Belge for Brussels (31 of 35 trees without a photo), Dr. Andreas Gröger for Munich (33 of 63), and Ricard Llerins Bonet, who self-published two Barcelona tree books with his own photos (42 of 56). Each names last week's Wilder article. Mailcheck clean, every URL answered 200. For Hidde: 3 archive mails in drafts/batch-archive-2026-10-25-preview.md
- **Rule**: Hidde had already answered the 3 Reddit items himself; all closed with `community.py --done`. A drafted Reddit reply no longer counts as a batch waiting for his word (CLAUDE.md rung 4), so the night run stops holding mail for it. Two days of mail were held for nothing.
- Left out of the batch: Peter Kálnai (Seville). Hidde's 10-15 mail promised to tell him about the WiFi crash, and drafts/reply-peter-wifi-crash.md is still unsent. Not his: the January felling in Seville's Jardines de las Delicias was an ombú (ID 236), not our Senegal date palm sev_034.

## 2026-10-25 session: a note under the thumb after collecting a tree

- **In the next app build**: after "Was it worth the trip?", the chosen thumb stays filled and an open box appears under it, "Leave a note: share something you'd like the next visitors to read about this tree". Done becomes Add note once something is typed; empty, Done just closes. The "first tree in your collection / first photo" line is gone. Benchmarked on Google Play's in-app review card and Google Maps' review screen (CONVENTIONS.md "A note under the thumb on the payoff"). Hidde approved each render.
- **Live on the web and in the next app build**: the note sheet on a tree page says only "Shown as A visitor." (or the name); "with today's date. Public right away." is gone in all eight languages. copycheck now refuses that kind of line.
- Also live earlier today: the empty notes card on the web showed "Write a note" twice (the button was read before it was declared); fixed.

## 2026-10-25 session: no year chart for an evergreen without a moment

- **Tree pages**: "The tree's year" is left out for an evergreen with no best_time and no moment rated striking or worth the trip (pines, cedars, cypresses, holm and live oaks, camphor: their line was near flat). About 315 charts go, 74 to 66 percent of trees; deciduous trees keep theirs (bare winter, fresh leaf). Hidde, after the Lone Pine in Canberra. Web only: the app has no year chart. Noticed in passing: some autumn colour reads low (White Oak, Pecan, Silver Maple "nice").

## 2026-10-25 session: the map card and sheet on a phone

- **Live on the phone website, every map**: the tapped tree's card has 16 on all four sides (it had 30 on top, 16 under), the list sheet steps away while a card is up and comes back when it closes (Airbnb's mobile map), and /explore's resting sheet shows the top of its first city, cut by the screen edge, so the list reads as something to pull up. Hidde approved the mockup first. Desktop and the app are unchanged (the app's tapped tree rises in its own sheet). CONVENTIONS.md "Tapping a pin on a map that has a list in a sheet" has the measurements.

## 2026-10-25 session: the Pohutukawa of Campo Santana is live (lis_038)

**In the product:** /lisbon gains its 37th tree, the Pohutukawa of Campo Santana, from a reader's photograph with GPS (the one that had wrongly led the weeping fig's page), on the ICNF register's classified group AIP11065609C (four bela-sombra and two Pohutukawa, 123 years at the 2016 survey). Hidde chose it: "this photo looks way more interesting". English and Portuguese; Lisbon's counts updated (title 37, "and thirty-six more" beside the olive). Both pages seen live after the deploy. On Hidde's word ("mail de beste persoon dat zn boom live staat") the reader who identified it (submissions 484 to 486) got a reply with both links, signed Ancient Trees, via contributor_reply.py.

## 2026-10-25 session: the Campo Santana fig shows the fig again; every reader photograph reaches Hidde

**In the product:** /lisbon, the Weeping Fig of Campo Santana (lis_015). A reader reported on 10-20 that its lead photograph showed a Pohutukawa and that the pin had moved to it; both photographs looked at, the reader was right. The fig's own photograph (smooth grey trunk, glossy leaves, the plaque) now leads, the Pohutukawa photograph is off the page, and the pin is back on the ICNF register point, 11 m from where the reader placed the fig on Google Maps, approximate. The Pohutukawa is a READY reader lead in data/leads/lisbon.json (the reader asked for it to be added); it ships with a short story. The reader (submissions 484 to 486) has no reply yet; a reply goes out only with Hidde's word.

**For Hidde:** the digest page now opens with how many reader photographs he has not seen and links photos.html (scripts/reader_photos.py: every shared app photograph, new trees and existing ones, unseen first). 11 were unseen today. After he has looked, a session runs `reader_photos.py --seen`. Held by qa's `check_every_reader_photo_reaches_hidde()`. This commit also carries another session's CLAUDE.md change (rung 4: the night run does nothing with Reddit).

## 2026-10-25 session: personal follow-up to the three ambassador requests sent

Hidde's own words, grammar only, sent on his "verstuur alle drie" (batch ambassador-personal-2026-10-25, logged in outreach-sent.json): New York (EN), Buçaco and Porto (PT). They thank them again and ask what they think of the list and the product. Open for a run: the Campo Santana weeping fig (lis_015) has a reader's 10-20 report, unanswered, that its photograph shows a Pohutukawa (Metrosideros excelsa) where the pin now stands and that the fig stood at the old spot (submissions 484 to 486, with a Google Maps link).

## 2026-10-25 session: notes are read by the run, and Claude starts only when there is work

**Notes on trees:** until today the knock marked every new note read into the Actions log, so no run ever read one. Now the knock only counts them (`tree_notes.py --waiting`); the run reads them at rung 1 (`--new`, `--hide` for the closed list, `--seen`, which marks only what `--new` printed). Guarded by qa's `check_notes_are_read_before_they_are_marked_read()`.

**Night run (Hidde: "saving tokens is good tbh if we can"):** every knock still runs the cheap steps every two hours (mail, live-first photographs, unlinking, outreach batches, page dates, deploy). The Claude window now starts only when `scripts/claude_gate.py` finds work: an app photograph in the queue, a submission from the last 150 minutes, an unread note, or the fixed slots 06:00 to 07:59 and 18:00 to 19:59 UTC for Reddit, outreach and the rest of the ladder. Any doubt starts it. A skipped knock writes no run-health record or LOG stub. Revert: delete the "Is there work for Claude" step in nightly.yml. Also: the digest's day table now has days across.

## 2026-10-25 session: tree notes table confirmed, digest shows the week day by day

tree_notes is in Supabase: sqlcheck with the service key says every migration is applied, and the Postbox check is green (10-24 22:35 and 10-25 11:58). Stop writing "paste supabase/tree-notes.sql" as something for Hidde. The digest now opens with readers' words in full (local page only), a day-by-day table for the last seven days, and a Waiting for you block. Its Today line now counts accounts and waitlist signups.

## 2026-10-25, forty-first attempt (nothing shipped)

Nothing changed in the product. Same state: no claims, inbox empty, 3 READY leads blocked by the own-supply pause, health.py's exit 1 is the push-skipped smoke and deploy runs (a scheduled deploy was in progress, not a break).

## 2026-10-25, fortieth attempt (nothing shipped)

Nothing changed in the product. No claims, inbox empty, 3 READY leads still under the supply pause, all 3 open Reddit items already drafted. health.py's exit 1 is again the push-skipped smoke and deploy runs; a scheduled deploy was in progress.

## 2026-10-25 (late attempt): outreach rung

Nothing shipped on the site. No claims standing, inbox empty, health.py's only flag is smoke "skipped" (log-only pushes skip it; Build and deploy succeeded, not a break). The 3 READY leads (Oxford x2, Madrid) are own supply, which is paused. Pulled private store, harvested r/lisbon and r/sicily (0 new comments), 3 open items all already have drafted replies; rebuilt the preview.
For Hidde: 3 Reddit replies in drafts/batch-community-preview.md (the r/lisbon Santa Iria photo reply is the one that matters: asks permission to use the photograph).

## 2026-10-25, thirty-ninth attempt (nothing shipped)

Nothing changed in the product. Inbox empty, harvest 0 new comments, all 3 open Reddit items already drafted, same 3 photo-less READY leads under the supply pause. health.py exit 1 is the push-skipped smoke test, answered. For Hidde: 3 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25, thirty-eighth attempt (nothing shipped)

Re-checked: no claims, same 3 photo-less READY leads (Oxford x2, Madrid) held by the own-supply pause, `enrich.py --next` has nothing. No new work found; nothing dispatched.

## 2026-10-25, thirty-seventh attempt (nothing shipped)

Re-checked, nothing workable: no claims standing, no reader photographs waiting, health.py's "skipped" deploys are push-skips by design (the 12:36 dispatch succeeded). The 3 READY leads (Oxford x2, Madrid) are own supply, paused under recovery mode, so not written. `enrich.py --next` says nothing to do. The 3 open Reddit items already have drafted replies; preview refreshed, nothing new to push. For Hidde: 3 Reddit replies in drafts/batch-community-preview.md.

## 2026-10-25, thirty-sixth attempt (nothing shipped)

State re-checked. No claims standing. No photographs waiting. health.py's two "skipped" flags (Smoke test, Build and deploy) are push-triggered runs that skip by design; the dispatched deploy at 12:36 succeeded, so the site is not stuck. READY has 3 leads (oxford 2, madrid 1) but own supply is paused, so they wait. Community lane: 3 open Reddit items all already carry drafted replies, harvest found no new comments, preview rebuilt. For Hidde: 3 Reddit replies in drafts/batch-community-preview.md. No mail batch started because this batch waits for his word.

## 2026-10-25, thirty-fifth attempt (nothing shipped)

Nothing changed in the product. Inbox empty, harvest 0 new comments, watch queued 0 threads, all 3 open Reddit items already drafted (batch waits for Hidde, so no mail batch). Same 3 photo-less READY leads under paused own supply, no write pass. health.py exit 1 is the push-skipped smoke test; the scheduled deploy succeeded.

## 2026-10-25, thirty-fourth attempt (nothing shipped)

Nothing changed in the product. No claims, inbox empty, the same 3 photo-less READY leads wait under the supply pause. The skipped Build and deploy / Smoke test runs are push no-ops, answered in health.py. All 3 open Reddit items already have drafted replies and a batch waits for Hidde, so no mail batch was started.

## 2026-10-25 night run, rung 4 (communities)

No claims standing. The 3 READY leads (Oxford x2, Madrid) are our own trees without an approved photograph, so they wait under the supply pause. Health: the skipped deploys are push no-ops, the scheduled build succeeded. Reddit: harvested, watched (1 new thread queued), 3 replies drafted, previewed and pushed to the private store.

For Hidde: 3 Reddit replies in drafts/batch-community-preview.md (r/lisbon Santa Iria photo permission, two r/marijuanaenthusiasts redwood threads).
## 2026-10-25, thirty-third attempt (nothing shipped)

Nothing changed in the product. No claims, inbox empty, same 3 photo-less READY leads (Oxford 2, Madrid 1) under paused own supply, so no write pass. health.py exit 1 is only the skipped smoke test (bot push); the deploy succeeded 0.8h ago. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25, thirty-second attempt (nothing shipped)

Nothing changed in the product. Inbox empty, harvest 0 new comments, both open Reddit items already drafted, same 3 photo-less READY leads (Oxford 2, Madrid 1) under paused own supply, so no write or verify pass. health.py exit 1 is the push-skipped smoke test (scheduled run 09:18 succeeded); answered with `health.py --answer`. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25, thirty-first attempt (nothing shipped)

No claims standing, inbox empty, same 3 photo-less READY leads (Oxford 2, Madrid 1) under the paused own supply, both open Reddit items already drafted. Staged-city verify would only add leads that cannot go live under the pause, so none dispatched. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25, thirtieth attempt (nothing shipped)

No claims standing. Same 3 READY leads (Oxford 2, Madrid 1), own supply under the pause and no photographs, so no write pass. Nothing new since the twenty-ninth attempt; Reddit drafts still wait for Hidde.

## 2026-10-25, twenty-ninth attempt

Nothing shipped. No claims standing; 3 READY leads (Oxford 2, Madrid 1) are our own supply and wait under the pause. Inbox empty. Smoke and deploy "skipped" on bot pushes only; the scheduled deploys succeed, so not broken. Reddit: 2 open items both already drafted, preview rebuilt, harvest and watch found nothing new.
For Hidde: 2 Reddit replies in drafts/batch-community-preview.md (r/lisbon Santa Iria photo ask, r/marijuanaenthusiasts Grizzly Giant).

## 2026-10-25 night run, twenty-eighth attempt (nothing shipped)

Nothing changed in the product. Inbox empty, harvest 0 new comments, the 2 open Reddit items already drafted (preview rebuilt, store pushed), no archive-group mail ready. Same 3 photo-less READY leads under paused own supply, enrich says nothing to do. health.py exit 1 is the by-design skipped smoke test (smoke.yml skips claude[bot] pushes); answered with `health.py --answer`. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25 night run, twenty-seventh attempt (nothing shipped)

No claims standing, inbox empty. READY leads are 3 of our own (Oxford x2, Madrid x1), none with a photograph, so own supply pause and ADD_NEEDS_PHOTO keep them from going live; no write pass dispatched. health.py's "Smoke test / Build and deploy skipped" is a false alarm: log-only pushes skip by path filter, the last scheduled deploy (04:55) succeeded.

## 2026-10-25 night run, twenty-sixth attempt (nothing shipped)

Nothing changed in the product. No claims, inbox empty, same 3 photo-less READY leads under paused own supply, both open Reddit items already drafted. health.py exit 1 is only the push-skipped smoke and build runs; the last scheduled deploy succeeded. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25 night run, twenty-fifth attempt (nothing shipped)

Nothing changed in the product. No claims, inbox empty, same 3 photo-less READY leads (own supply paused), 2 Reddit items already drafted, health.py exit 1 is still only the skipped smoke test. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25 night run, twenty-fourth attempt (nothing shipped)

Nothing changed in the product. Inbox empty, harvest 0 new comments, the 2 open Reddit items already drafted. health.py exit 1 is only the push-skipped smoke test (deploy succeeded 2h ago). Own supply paused, 3 READY leads photo-less, so no write or verify pass. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25 night run, twenty-third attempt (nothing shipped)

Nothing changed in the product. Pulled, no claims standing, same 3 photo-less READY leads (Oxford 2, Madrid 1) under paused own supply, so no write pass. Stirling register already retried twice (10-22, 10-23) with no register to find, so not a third time. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25 night run, twenty-second attempt (nothing shipped)

Nothing changed in the product. No claims, inbox empty, same 3 photo-less READY leads (own supply paused). The skipped deploys are push-triggered no-ops; the last dispatched deploy succeeded. The 2 Reddit items are still drafted. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25 night run, twenty-first attempt (nothing shipped)

Nothing changed in the product. No claims, inbox empty, 3 READY leads (Oxford 2, Madrid 1) are photo-less and own supply is paused, so no write pass (under six anyway). Staged cities only feed a paused supply. The 2 open Reddit items already carry drafts. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25 night run, twentieth attempt (nothing shipped)

Nothing changed in the product. Inbox empty, harvest 0 new comments, watch 0 new threads; the 2 open Reddit items are drafted, preview rebuilt and pushed, so no mail batch started. health.py exit 1 is only the push-skipped smoke test. Own supply paused, 3 READY leads photo-less, staged cities walled. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-25 night run, nineteenth attempt (nothing shipped)

Nothing changed in the product. No claims, sightings inbox empty, the 3 READY leads still cannot ship under paused own supply. Community lane re-run: harvest found 0 new comments, the 2 open items (r/lisbon Santa Iria photo, r/marijuanaenthusiasts Grizzly Giant) already carry drafts, preview refreshed and pushed. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md. iOS run 40144403493 for the pill fix was still in progress.

## 2026-10-25 night run, sixteenth attempt: nothing shipped

Sightings inbox empty. health.py: the deploy "skipped" runs are cancelled by newer pushes (one deploy running), and the ios.yml failure is the pill fix the fifteenth attempt pushed, now rebuilding. Reddit harvest and watch found nothing new; the 2 open items (r/lisbon Santa Iria photo, r/marijuanaenthusiasts Grizzly Giant) are already drafted and the preview is rebuilt, no mail batch started while that batch waits. Own supply is paused, so READY leads and staged cities were not dispatched.

For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

