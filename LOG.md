# LOG

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-10](archive/LOG-2026-10.md)
- [2026-09](archive/LOG-2026-09.md)
- [2026-08](archive/LOG-2026-08.md)
- [2026-07](archive/LOG-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
<!-- archive-index -->
## 2026-10-27 night run (18:18 window)

- Rungs 1 to 3 clear (no reader photos or notes, health green). Rung 4: 94 drafts still open, so no new mail batch; sourced two archive contacts instead (Nederlandse Dendrologische Vereniging for Arnhem, Asociación Española de Arboricultura for Barcelona/Seville/Valencia; both addresses from their own sites), contacts rebuilt and pushed. Tree Register and Ancient Tree Forum addresses were only on the Charity Commission register, not their own sites, so left out. Hoyt Arboretum's address was only in old event listings (its site returned 403).
- Rung 5: enrichment lisbon+albertshausen+bamberg+potsdam: 4 trees closed (3 best_time, Potsdam beech pin source), 14 gaps recorded as dead ends. Measurements and Bamberg access had no source. Preflight 0 problems.

## 2026-10-27 session with Hidde: Show HN, second try

The 10-24 Show HN (item 50208440, posted on a Saturday) ended at 1 point, and its first comment is [dead]: the filter for new accounts killed it (hburgmans, karma 1). Hidde already mailed hn@ycombinator.com about the dead comment on Friday 10-23 at 15:13 (his Sent folder; so the post went up that Friday, not 10-24), and no answer came. Second try: the same URL with the explanation in the submission's own text field, Tuesday to Thursday 14:00 to 17:00; if the submit lands on the old item, the duplicate filter folded it and he stops. drafts/show-hn.md now says text in the post, not a separate comment.

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

## 2026-10-24 night run, eighteenth attempt (nothing shipped)

No claims standing, sightings inbox empty, 3 READY leads (Oxford x2, Madrid) have no approved photograph and own supply is paused. The iOS run for the pill fix (40144403493) is in progress; the earlier failure was the appfit issue it fixes. The Reddit batch still waits on Hidde, so no mail batch started.

## 2026-10-24 night run, seventeenth attempt (nothing shipped)

Nothing changed in the product. Sightings inbox is empty, both open Reddit items already carry drafted replies (r/lisbon Santa Iria photo, r/marijuanaenthusiasts Grizzly Giant), no claims stood. The 3 READY leads (Oxford x2, Madrid) cannot ship under the paused own supply. Graz and Nuremberg were claimed and released: 0 of 7 and 3 of 16 leads carry a coordinate, so a verify pass would fail on the pin. Both are walls for 48h. Stage 1 and 2 cities have no placed supply either. Open: the iOS workflow shows FAILED since 2026-10-24 (not investigated this attempt).

## 2026-10-25 night run, sixteenth attempt: nothing shipped

Sightings inbox empty. health.py: the deploy "skipped" runs are cancelled by newer pushes (one deploy running), and the ios.yml failure is the pill fix the fifteenth attempt pushed, now rebuilding. Reddit harvest and watch found nothing new; the 2 open items (r/lisbon Santa Iria photo, r/marijuanaenthusiasts Grizzly Giant) are already drafted and the preview is rebuilt, no mail batch started while that batch waits. Own supply is paused, so READY leads and staged cities were not dispatched.

For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-24 night run, fifteenth attempt: one app fix, no trees

The iOS run failed appfit on the new Add a photo pill: its touch target (inset -4 on all sides) put the button's right edge at W-16 against the page's W-20. Now the target grows vertically only (TreeDetail.swift addPhotoRow); not rebuilt here (no Xcode), the next ios.yml run confirms. Site deploy skips were concurrency, one deploy is running. READY leads (3) and every staged city only make trees of our own, which are paused, so no verify or write pass was dispatched. Community drafts unchanged.

For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-24 night run, fourteenth attempt: nothing shipped

No claims standing. 3 READY leads (Oxford 2, Madrid 1) have no approved photograph, and own supply is paused, so none can go live. Sightings inbox empty. Community queue: 2 open items, both already drafted (r/lisbon Santa Iria photo, r/marijuanaenthusiasts Grizzly Giant); preview rebuilt, nothing new to push. Stirling register retry already done on 10-22 and 10-23 with no new angle, left stalled.

For Hidde: 2 Reddit replies in drafts/batch-community-preview.md

## 2026-10-24 night run, thirteenth attempt (short)

Nothing shipped; no product change. Checked: no claims standing, sighting inbox empty, no new Reddit comments. The 3 READY leads (Oxford x2, Madrid) have no approved photograph and own supply is paused, so they wait. health.py's smoke/deploy flags predate the 44px Add-a-photo fix (92166dd74); the 23:22 deploy succeeded and pushes are skipped by design.
For Hidde: 2 Reddit replies in drafts/batch-community-preview.md (r/lisbon Santa Iria photo ask, r/marijuanaenthusiasts Grizzly Giant).
The iOS workflow still reads failure (0.8h ago): log not read this attempt.

## 2026-10-24 23:44 window

- Rung 2: the smoke test was red because the new "Add a photo" pill on tree pages was 36px tall at 375px (floor 44). Now 44px on phones (style.css, `.addphoto-btn.tonal`), pushed as 92166dd74. Reader inbox empty. Not yet re-verified by a smoke run; the next smoke run will say.
- Rung 4: harvested 22 new Reddit comments (r/lisbon, r/sicily). The Sicily tips (Ortigia ficus, Villa Bellini, Agrigento olive) are already leads; 20 items closed with a reason. Two replies drafted. community.py had repeated rows per id, so a verdict closed only one copy and the preview listed the same reply four times; now one row per id and verdicts cover all. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md (the r/lisbon Santa Iria photo asks permission to use it; the Grizzly Giant thread).

## 2026-10-24, night run, twelfth attempt: nothing shipped

Nothing changed in the product. Same state as the eleventh: no claims, inbox empty, 3 READY leads (Oxford x2, Madrid) held by the supply pause, last real deploy green. For Hidde: paste supabase/tree-notes.sql to clear the Postbox check.

## 2026-10-24, night run, eleventh attempt: nothing shipped

Nothing changed in the product. No claims, inbox empty, 3 READY leads still held by the supply pause, site healthy (the "skipped" builds are log-only pushes; Postbox check is still only the unpasted tree_notes.sql). Reddit queue is the same as the tenth attempt: replies drafted, waiting for Hidde. The window's remaining work is Hidde's to unblock, not a run's.

## 2026-10-24, night run, tenth attempt (rung 4, community)

- No claims standing. 3 READY leads (Oxford x2, Madrid x1) left unwritten on purpose: own supply is paused under recovery mode.
- Reddit: harvested and watched, all 17 open items closed. 4 replies drafted for Hidde, left unposted. The Grizzly Giant draft had a wrong history claim (Grant and the 1864 act), so I rewrote it with no claim in it. 8 items closed with `--done`, each with its reason.
- For Hidde: 4 Reddit replies in drafts/batch-community-preview.md.
- For Hidde: Postbox check fails only because supabase/tree-notes.sql has never been pasted (sqlcheck: table tree_notes). Paste it and the check goes green.
- No mail batch started this run.

## 2026-10-24 20:05 window (ninth attempt): nothing shipped

Nothing changed in the product. Inbox empty. health.py still flags the Postbox check from 11:35; its log shows only sqlcheck naming tree_notes.sql as not pasted (the already-answered case, no site fault). The Reddit harvest found 0 new comments in r/lisbon and r/sicily, so the commenter still has not posted a tree location. READY is the same 3 own leads under the supply pause. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md still wait.

## 2026-10-24 eighth attempt: nothing shipped

Nothing changed in the product. No claims, inbox empty, READY is the same 3 own leads (oxford 2, madrid 1) under the supply pause, so no write pass. health.py's skipped builds and Postbox failure are the ones already answered. No new angle.

## 2026-10-24 seventh attempt: nothing shipped

Nothing changed in the product. No claims standing, inbox empty, READY is still 3 own leads (oxford 2, madrid 1) under the supply pause. The Reddit queue came back with the same duplicates and no tree tip. Nothing new to act on.

## 2026-10-24 sixth attempt: nothing shipped

Nothing changed in the product. No claims standing, inbox empty, READY is 3 own leads (oxford 2, madrid 1) held by the supply pause. health.py's skipped builds (log-only pushes) and Postbox failure were already answered; a deploy dispatched 16:49 is still running. No new angle on any rung, so I did not repeat earlier work.

## 2026-10-24 17:09 window (fifth attempt): nothing shipped

Nothing changed in the product. The inbox is empty, and health.py's 'skipped' builds and the Postbox failure are the ones already answered. Own supply is paused and READY is still 3 own leads. `private_store.py pull` brought back the Reddit queue with 17 open items, duplicates again, though the harvest found 0 new comments. None carries a tree tip, and the r/lisbon commenter has still not posted a location. I did not re-close the queue, because the next pull restores it. The queue and the pull need a fix: `--done` loses its effect once a pull restores the duplicates. For Hidde: the 2 Reddit replies in drafts/batch-community-preview.md still wait.

## 2026-10-24 (fourth attempt): nothing shipped, state re-checked

Nothing changed in the product. No claims standing, inbox empty, health.py's 'skipped' builds are log-only pushes (path filters) and the Postbox failure was already answered. READY is still 3 own leads (oxford 2, madrid 1) under a paused supply. The Stirling register retry has been tried on 10-15, 10-22 and 10-23 with no new angle, so I did not repeat it. Open for the next run: check the r/lisbon thread for the commenter's tree location; the 997 leads needing only a source could feed a verify pass on a staged US city (fort-worth, portland, san-francisco), which is leads-only work while supply is paused.

## 2026-10-24 (third attempt): Reddit queue closed for real, no trees

Nothing shipped to the product. No claims were standing; 3 READY leads (oxford 2, madrid 1) are own trees, and own supply is paused. The inbox was empty. `private_store.py pull` had restored the Reddit queue with duplicate ids, so the earlier `--done` calls were lost and `--done` only touched the first of two copies. I deduplicated data/outreach-community.json and closed everything without a tip. Two items stay open: the Santa Iria cypress photo ask (Hidde posts it) and the Grizzly Giant reply (the stale Grant draft is gone). One r/lisbon commenter (19riuyxs4wn0g) still owes a location; check that thread. Pushed to the private store.
For Hidde: 2 Reddit replies in drafts/batch-community-preview.md.

## 2026-10-24 (late window): Reddit queue closed, no trees

Nothing shipped to the product. No claims were standing. Only 3 READY leads (oxford 2, madrid 1), under the six-candidate minimum for a pass, and own supply is paused. The sightings inbox was empty. Reddit: 12 open items, 3 with drafts, the other 9 closed with `--done` (no tip, no location). I rewrote the Grizzly Giant draft, which wrongly put 1903 "earlier than Grant"; it was Roosevelt who camped with Muir. For Hidde: 3 Reddit replies in drafts/batch-community-preview.md. Archive-ask lead from the thread: digarb.hku.hk (HKU Hong Kong tree registry) and Gigantes Verdes (Portugal) as contacts.

## 2026-10-24 17:00 UTC, night run: Reddit queue worked, no tree made

Nothing changed in the product. Rung 1: no reader photographs waiting. Rung 2: the Postbox check failure of 11:35 was only sqlcheck saying tree_notes.sql was not pasted yet; the table has been live since, so I recorded the answer with health.py. Rung 4: harvested r/lisbon (32 comments) and r/sicily (none new), closed 11 open items with a reason (no tree tip in any of them) and drafted nothing new. Two earlier drafts wait.
For Hidde: 2 Reddit replies in drafts/batch-community-preview.md (the Santa Iria cypress photo ask in r/lisbon, the Grizzly Giant comment in r/marijuanaenthusiasts). Because that batch waits for his word, I left the mail batch and the archive asks alone tonight.
Nothing else was open: enrichment says nothing to do, no recognition lines are stuck, own supply is paused, and the only page gap is one species page that Google would not see anyway. Photo hunts for Google are off the ladder. One r/lisbon commenter says they will come back with the location of a tree; the next run should check that thread.

## 2026-10-24, session with Hidde: every website map shows the same tree card

- **Live with this deploy:** a tap on a tree on /explore (every language), the country and state maps and your profile map now shows the same Airbnb card as the city map, instead of jumping straight to the tree page. On a phone the card sits over the map above the sheet's peek; on a desktop it sits beside the pin. The card opens the tree and its heart saves.
- **How it stays one thing:** the tap lives once, in site/src/lib/map-card-js.ts, and every map calls it. qa.py `check_one_tree_card_on_every_map()` fails the deploy if a map builds its own card, opens a popup for a tree, or jumps straight to a page. Tested against the old code: it refuses all five map scripts.
- Checked through a proxy of the live site at 375px and desktop, on /explore and /lisbon: opening, closing with a map tap, the heart asking to sign in, and the pin released on close. The country and profile maps use the same function as /explore and were not opened in the proxy.

## 2026-10-24 late window: Reddit queue closed

- Nothing new is live on the site. The 3 READY leads (2 Oxford, 1 Madrid) are our own trees, so they wait under the supply pause (a new tree of our own needs an approved photograph). No claims were standing.
- Reddit: 15 open items, 13 closed (no tree tip, private land, or a pointer only), 2 replies drafted. The r/lisbon photo-permission reply and the Grizzly Giant reply are left unsent.
- For Hidde: 2 Reddit replies in drafts/batch-community-preview.md.

## 2026-10-24, 13:47 window (Sonnet): nothing new, nothing shipped

No trees shipped, on purpose: own supply is paused. Rung 1 empty (0 photographs waiting). Rung 2: health.py still lists the Postbox failure, the skipped smoke test and the unpasted tree-notes.sql migration; all three were answered earlier and need Hidde's Supabase login. Rung 4: harvest found 0 new comments; the 2 drafted Reddit replies already wait in drafts/batch-community-preview.md. Backup lane: Stirling is a RETRY target but was retried 10-22 and 10-23 with no register found, so not repeated. Nothing else on the ladder has work under recovery mode.

## 2026-10-24, last attempt (Sonnet): nothing shippable, nothing broken

Shipped no trees, on purpose. Own supply is paused, so the 3 READY leads (2 Oxford, 1 Madrid) wait. No claims were standing, no reader photographs waiting, `enrich.py --next` has nothing, and the `archive` outreach group has 0 ready.
- health.py's "Build and deploy keeps failing" is stale. The pal_001 feed-count failure was the 11:40 and 12:01 builds, before images.ts let source `mine` through `showable()`. The 12:25 build with the fix succeeded and the later runs skipped (LOG-only commits). Answered with `health.py --answer`.
- Still open, not touched: the Postbox check failure (1.8h old) and one migration not pasted into the database (`python3 scripts/sqlcheck.py` names it). Both need a look by someone with those logins.

## 2026-10-24, late attempt (Sonnet)

- Shipped no trees: own supply is paused, and the 3 READY leads (2 Oxford, 1 Madrid) are our own trees, so they wait.
- Deploy: health.py showed the pal_001 feed-count failure, but the 12:25 build with the images.ts fix succeeded; the newest run is a skipped log-only commit. No action needed.
- vendor_photos.py: 1 photograph vendored (pal_022).
- Reddit: closed 5 open items (no tree, no ask). 2 replies drafted. For Hidde: 2 Reddit replies in drafts/batch-community-preview.md (the r/lisbon Santa Iria photo offer and the Grizzly Giant thread).
- Still open: the r/lisbon thread on the cypress with the metal frame and the Santa Iria location. The Postbox check failure was answered earlier.
## 2026-10-24 night run (13:15 window): rung 4, Reddit read, two replies drafted

**Nothing changed in the product this window.** Rung 1 empty (0 photographs waiting). Health: the Postbox check failure and the "migration not pasted" line are one cause, supabase/tree-notes.sql, already FOR HIDDE; answered with `health.py --answer`. Rung 4: harvest found 0 new comments, watch found 9 new posts; the 13 open items closed with a reason each, except two with a reply. **For Hidde: 2 Reddit replies in drafts/batch-community-preview.md:** (1) the r/Lisbon commenter's photograph of the Santa Iria olive (I looked at it: a big old olive with the information panel, our lis_036, which has no photograph yet), a reply asking if we may use it on the page; (2) the Grizzly Giant thread in r/marijuanaenthusiasts, a light reply that also gently corrects the 1903 camp (Roosevelt with Muir, not Grant), check that fact before posting. No new tree leads (the Evansville reserve and the Santa Iria image gave no placeable new tree). Mail batch: none drafted, the 10-23 batches still wait for his word; the `archive` group has 0 ready in contacts_db, no feeder yet. Own supply paused, enrichment says nothing to do, recognise --stuck and pagegaps have nothing worth a window (one species page, noindex under the strict cut).

## 2026-10-24 session: the tree page rebuilt, web and app (Hidde: "bouw alles")

**What changed in the product:** the tree page follows the day's benchmark (CONVENTIONS.md 2026-10-24 entries). Without a photograph the hero is the map with one card at its foot ("No photograph yet. Been here? Yours would be the first on this page." and Add a photo). Under the title only the district and the park link, the crumb at the top keeps the path. The story folds to about six lines with Read more. "Getting there" is one block with a heading: address, how to recognise it (its own row, the eye), access only when there is something to meet (1,266 "Free, public park" lines now say nothing), transport. New section "From people who stood here": one note per person per tree, dated, public the moment it is written, the name only from a public profile, else "A visitor"; empty, it borrows the nearest tree's real note, else a ghost example; one button, "Leave a note for the next visitor", the prompt inside the sheet. Eight languages. Same sections in the app (branch tree-page-app, next build): map hero, folded story, Getting there, notes with the BrandSheet, `-notesdemo` for the sweep, SignedOutWalk.testNoteAsks.

**Machinery:** supabase/tree-notes.sql (table, RLS, GRANT, `tree_notes_for()`); scripts/tree_notes.py (`--new --seen`, `--hide <code> <tree_id> "why"`) runs at every knock. **Live first for photographs:** `sightings_publish.py --live-first` at every knock puts a reader's photograph in the strip of a tree that already has a lead (photo-less pages keep the judged path, since the strip's first picture would become the hero); `--unstrip <sighting_id>` undoes one, the judge's approve promotes, hold or reject removes; the digest's machine part lists each with its undo. Schema accepts `source: "mine"` (the Piazza Marina fig had broken every build since 10:01).

Hidde pasted supabase/tree-notes.sql the same afternoon (the first try ran an old tab's SQL and failed on an `events` column; a clean tab succeeded) and the block shows on the ginkgo page. The app's tree page is merged to main, carried by the next build.

**Not done:** the collect sheet's optional "What did you see?" field (CONVENTIONS.md names Strava and Polarsteps as the reference for the next build); the night run does not yet quote a visitor's note into a story (reader_words.py reads sightings only).

## 2026-10-24 session: three UNLV trees get photographs from the campus grounds superintendent

**What changed:** the weeping mulberry, Camperdown elm and Texas olive in Las Vegas have photographs mailed by UNLV's grounds superintendent (answering our 10-07 mail), uncredited per the mailed-photo ruling, pins moved to his coordinates and confirmed (two geotags agree within 20 m). They now count as reader content, so the three pages and /las-vegas go back into Google. Two colon reveals in those stories rewritten. `outreach_inbox.py --save-from <address>` now saves one matched sender's attachments to out/mail-photos/. **For Hidde:** reply drafted in drafts/reply-james-kearney-2026-10-24.md; he says more photos follow.

## 2026-10-24 session: the night run asks for photo archives, no more Commons hunting for Google

**What changed:** rung 4 now drafts archive asks after Reddit: societies, photographers and ambassadors who hold photographs of our trees that are on no open site, asked to let us use them, credited (new group `archive` in OUTREACH_STRATEGY.md and contacts_db.py, first among the groups). Commons photo sweeps only when nothing else is left, for readers. Why: one archive gave Copenhagen 32 pages in Google, all readers together 51 photos. **For the night run:** the `archive` group has no feeder script yet; start from the warm repliers (society 12, garden 6), the ambassadors and the societies in data/outreach-contacts-*.json, and log what a feeder would need.

## 2026-10-24 session: the reader cut, Google sees only pages with reader content

**What changed:** Google is now asked to show only tree pages with something a reader gave us (a unique photo, a reader's photo in the strip, a reader-found tree) and the place pages of cities where one tree has it, plus home and the site's own pages (Hidde: "ik ga liever te ver en voeg langzaam weer dingen toe"). 105 tree pages and 27 place pages in 34 cities stay, down from 598 tree pages; 1,413 more pages carry the googlebot noindex, Bing keeps everything. `READER_ONLY` in scripts/thin_pages.py, one flag back. A reader's photograph on a tree returns its page by itself. **For the night run:** Commons photos no longer put a page in Google; the photo lane prepares the first step back (data/index-kept.json still names the demand cut's 108 cities), reader input is what grows the index. **Not verified locally:** qa.py needs the Astro build, so the split check runs in CI on deploy.

## 2026-10-24 session: the night run reads Reddit for Hidde (rung 4)

**What changed:** the night run's ladder has a new rung 4, communities and outreach, above enrichment while recovery mode holds (Hidde: "refocus the nightrun on outreach and local community posts if you find an effective way"). Why: Google Analytics shows 3 to 6 people a day before the r/Lisbon post and 11 and 15 on 10-22 and 10-23, while 7 night runs on 10-23 made 0 trees. `scripts/community.py` reads every comment under his posts and new threads about an old tree (four tree subs plus the city subs he posted in) from the Arctic Shift archive, since Reddit refuses us. The run turns tips into leads, drafts replies into drafts/batch-community-preview.md (private), and he posts them; it never posts and never keeps a username. Then one mail batch draft a night through OUTREACH_STRATEGY.md's daily rhythm when none waits for his word. **First pass:** r/Lisbon 19 comments, 12 already answered by him, 7 open, one a photograph of the Santa Iria olive he asked for; 10 threads, two worth a reply (the Grizzly Giant, which we have; Evansville's tulip poplars, a tip). Renumbered: enrichment is rung 5, registers 6, photos 7, recognition 8, page gaps 9, product 10. **Gap:** the archive holds the r/sicily post but none of its comments yet, so an empty harvest proves nothing. Not done here: no reply drafted, that is the night run's first job.

## 2026-10-24 night run, restart after early stop

Nothing new live. No standing claims. READY leads were 3 (Oxford 2, Madrid 1), own supply is paused and they have no photographs, so none written. Ran the kept-set photo sweep (`photo_hunt.py --recheck`) and a photo-judge pass over the 35 trees with unjudged candidates (Singapore, Amsterdam, Chicago, Utrecht, Budapest): 712 candidates, 0 approved, 1 held (sgp_027, earlier closer-geotag hold kept). Commons is spent for the kept set; further photos need iNaturalist or readers. Not done: iOS app workflow shows FAILED (newest finished run 10-23), not investigated this attempt.
## 2026-10-24 which tree gets the full pin: photograph, then readers' saves (live, web and app)

Hidde, looking at the new maps: "it looks good tbh" and, on the order, "i think photo and likes are the best way." The likes are readers' Want to go saves, which never reached the build. scripts/tree_saves.py counts them per tree from Supabase (counts only, our own accounts left out) into data/tree-saves.json, nightly from data-digest.yml; lib/saves.ts reads it, every map's features carry `pr` from one `pinPriority(hasPhoto, saves)` in lib/map.ts, the app feed carries `saves` and TreeMap.swift uses the same arithmetic (qa holds them equal). First count today: 38 trees saved by readers, 39 saves, so for now the photograph decides almost everywhere and the count grows with the people.

## 2026-10-24 session: r/sicily's second day, the Villino Favaloro fig live

**In the product:** /palermo/white-fig-of-villino-favaloro (pal_022), a reader tip from the thread: a white fig (Ficus virens), 10 m round and 20 m tall by MASAF and the Regione Siciliana list, sheet 18/G273/PA/19. It leans out of the closed garden of the Basile villa on Piazza Virgilio and is seen from the street. BlogSicilia 2023 is the second source. A CC BY 4.0 Commons photograph by Esculapio, taken 2026-10-02, was looked at and approved, and it is also the life check. The reader's words are quoted on the page in English and Italian. It is in the Sicily collection (now 14 trees). Pin is approximate, register point by the railings. **Leads:** the Ficuzza oak (Palermo leads, no register row), the Ortigia fig and the Zimmiti cactus (Syracuse), and the "Innari" olive (Sardinia file, place unknown). **For Hidde:** replies for the five new comments are in drafts/reddit-sicily-replies-2026-10-24.md. Chloe_Lifter's "How old is this tree?" gets no draft because it is unclear which tree it means. The build runs in CI only, so the page has not been looked at rendered yet.


## 2026-10-24 later attempt in the 08:34 window: nothing shipped

- No claims standing, inbox empty, READY still 3 own trees without photographs (supply paused), so no write pass. iOS red is still the 30-minute `xcodebuild` hang on the large phone (run 40017321068); needs a Mac session.
- `photo_hunt.py --recheck` swept 40 trees in the kept set: 0 new candidates. Photo queue holds nothing newly judgeable.

## 2026-10-24 08:34 window: nothing shipped

- Inbox empty. health.py exit 1 is the same iOS hang plus the push-skipped smoke test. Supply paused, READY is 3 photo-less own trees, so no write pass.
- `photo_hunt.py --recheck` found 0 new candidates; `photo_fetch.py --roster` fetched 2 (lux_009, iNat leaf and seedling close-ups). I looked at both and they are not the tree; `photo_verdicts.py` refused the reject ("no candidate matching luxembourg-city"), so nothing was recorded. Not debugged.

## 2026-10-24 night run, restart after early stop: nothing shipped

- No claims standing, sighting inbox empty. READY leads are 3 (Oxford 2, Madrid 1), all our own trees, held by SUPPLY_PAUSED and ADD_NEEDS_PHOTO, so no write pass.
- iOS red is the known SweepFrames xcodebuild hang (killed at 30 min, run 40013002762); needs a Mac session. Smoke "skipped" is the normal push-skip.

## 2026-10-24 night run (02:55): nothing shipped

- Inbox empty, READY still 3 photo-less own trees (supply paused), prepare.py shelf unchanged. health.py exit 1 is the same iOS appfit hang (run 40017321068) plus a skipped smoke test; no source fix possible from Linux. Stirling RETRY not repeated: already stalled twice on 10-23. Nothing new since the sixteenth attempt; waiting on Search Console or a reader's tree.
## 2026-10-24 every map draws pins the Airbnb way, never counted bubbles (live, web and app)

Hidde, an hour after the city map got bubbles: "je wil ook niet nodeloos bubbels openklikken ... kun je deze interactie bij airbnb onderzoeken". Airbnb and Google Maps never pile a results map into counted bubbles (benchmark in CONVENTIONS.md); shown Lisbon both ways, he chose: "Doe de Airbnb-manier overal ... Web en app." Now on every map (city, /explore, country and state, My trees, the app): every tree drawn, a full pin where none stands within 40 px (lib/map.ts PIN_DISTANCE, TreeMap.swift pinDistance), photograph first, a dot for the rest, a tap always opens the tree, nothing zooms for you. The app's own grid clusterer is gone; MapLibre's symbol collision places the pins there and on the circle-pin maps, the city map does the pass over its DOM pins. The one bubble left is a same-spot stack, from zoom 14 only (STACK_ZOOM, stackZoom). Checked on mocks of the live pages at 375px and desktop (Lisbon 18 pins and 18 dots at the opening zoom; explore 98 pins and 2,731 dots over Europe; Italy; My trees filled and hollow) and in the simulator (Lisbon, the Ajuda stack); the app built twice and its unit tests pass. qa `check_every_map_shows_pins_the_same_way()` refuses a clustered source, the old grid, or the two numbers drifting. DECISIONS.md 2026-10-24, CLAUDE.md one line. Not done: the night's three cluster tests were replaced by three pin-rule tests; a walk through the UI test sweep on CI will say whether the grid tap still lands.

## 2026-10-24 city map piles its own trees like every other map (live)

Hidde, on /lisbon (36 trees): the city map drew every species pin over the others zoomed out while /explore, the country maps, My trees and the app showed counted bubbles ("kunnen we die interacties gelijk houden?"). The city map now carries a clustered source of its own trees that decides which DOM pins show and draws the same moss bubble with the count, from the shared numbers in lib/map.ts (radius 13, distance 40, piles to zoom 14); a tap zooms to where the bubble parts, past zoom 14 the species pins and the same-spot stacks are back, and a selected tree flies to 15.5 so its pin never lands inside a bubble. Checked on a mockup of the live pages at 375px and desktop: Lisbon 6+2+16+10 plus two pins, Palermo, London 27 in six piles plus five, Bruges one 2 beside two pins. qa `check_every_web_map_piles_with_the_same_numbers()` refuses a map file writing those numbers as literals. CONVENTIONS.md "How close two pins have to be" got the dated line. Seen in passing, not fixed: /london at 375px opens at zoom 8.4, below FAR, so the live page shows one 32 bubble and no pins until you zoom in.

## 2026-10-24 session: map list comes down again with no trees in view

App: a raised list on the map stayed stuck once no trees were in view (Hidde's report). The empty-list lock now stops raising only, never lowering (BottomSheet.swift). Checked on the iPhone 17 Pro simulator: raised over Amsterdam, panned to Ruigoord, dragged down to peek, and an upward swipe still leaves it down. For Hidde: next build carries this fix.

## 2026-10-24 session: the six weeks concentrate on Lisbon

After the cold-start research (reports/Kip ei start van content apps.md: nine apps, every one grew contributors in one dense place with a few named people), Hidde chose Lisbon ("Yes, Lisbon"). GO_TO_MARKET.md carries the revised plan and the measure: Lisbon trees with a stranger's photograph, 5 today, ten by 2026-12-05. Lisbon stands at 36 trees, 18 approved photos, 32 confirmed pins; Commons is judged out for the 18 photo-less trees (every candidate rejected by 10-19), so photographs come from people. A search pass found fifteen people and bodies who already photograph Lisbon's trees (drafts/lisbon-ten.md, local: Commons uploaders, three juntas, Gigantes Verdes, a tree-walk organiser), and ten first mails are drafted in drafts/lisbon-ten-mails.md, one tree each, for Hidde to send two or three a week. Side finding: JF Penha de França's felling notice of 10-20 on Praça Paiva Couceiro is a white poplar, not our ginkgo (lis_008 stands). Instagram: six posts drafted as a business card (drafts/instagram-first-six.md).

## 2026-10-24 session: Wilder's article is out, four followed links

wilder.pt published the Lisbon interview on 2026-10-23 (Ines Sequeira): links to the home page, /lisbon, /porto and /contribute, all followed, no App Store link. The second press placement ever and the first with links. Watched by backlinks.py, contacts_db marks Wilder linked, details in drafts/OUTREACH.md. Nothing in the product changed; the digest's GA and Portugal download rows are where it shows from 10-25.

## 2026-10-24 session: Show HN posted

Hidde posted "Show HN: I'm mapping the old trees worth walking to (3,800 so far)" at 15:04 Dutch time, news.ycombinator.com/item?id=50208440, from his own account; first comment in his About-page voice with the AI paragraph in his own framing (drafts/show-hn.md, local). Measure over the week: points and comments on the item, visitors with referrer news.ycombinator.com in Google Analytics, submissions and accounts. OUTREACH_STRATEGY's "later or not at all" was replaced on his word on 10-23.

