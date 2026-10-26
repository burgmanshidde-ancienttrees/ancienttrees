# LOG

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-10](archive/LOG-2026-10.md)
- [2026-09](archive/LOG-2026-09.md)
- [2026-08](archive/LOG-2026-08.md)
- [2026-07](archive/LOG-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
<!-- archive-index -->
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
## 2026-10-23 night run, sixteenth attempt: nothing shipped

- No claims standing, inbox empty, READY is 3 photo-less own trees (oxford 2, madrid 1) and `SUPPLY_PAUSED` is True, so no write pass. `enrich.py --next`, `recognise.py --stuck` and `pagegaps.py` all report nothing to do. The 54 "awaiting a writer" trees cannot go live while supply is paused.
- I reran `photo_hunt.py --recheck` against the fifteenth entry's note: 0 new candidates again. Stirling was retried twice today already, still stalled. iOS failure is the same appfit hang, nothing new.
- Do not rerun any of the above until Search Console moves or a reader's tree arrives.
## 2026-10-23 night run, fifteenth attempt (22:50): nothing shipped

- Inbox empty, READY the same 3 photo-less own trees (supply paused). health.py exit 1 is only the iOS app: both failed runs (40013002762, 40017321068) died in appfit's `xcodebuild test` hanging past 30 minutes on the iPhone SE simulator, then the 110-minute cap; the appsweep after it produced 40 screenshots. A runner hang, no assertion failure, and the run before succeeded, so no source fix is possible from this runner. For Hidde: nothing yet; if the next scheduled iOS run hangs too, the SweepFrames step needs a look on the Mac.
- I reran `photo_hunt.py --recheck` against the fourteenth entry's note: 40 trees, 0 new candidates, as predicted. Do not rerun.
- Open lane remains `scout_next.py --target` (RETRY Stirling).
## 2026-10-23 night run, fourteenth attempt: nothing shipped, one finding

- Claims none, inbox empty, READY is the same 3 own trees without photographs (supply paused). `enrich.py --next`: nothing anywhere. `photo_gaps.py --shortlist`: nothing queued, every candidate already judged.
- Correction to the thirteenth entry: `photo_hunt.py --recheck` re-asks the same first 40 trees by design, and the "1025 unchecked" line counts the recheck pool. Plain `photo_hunt.py` says 0 unchecked: the kept set is fully swept. Photo lane is exhausted until new uploads appear; do not rerun it.
- `scout_next.py --target` names RETRY Stirling (#266): the one open lane for the next window.
## 2026-10-23 night run, thirteenth attempt: nothing shipped

- No claims standing; sightings inbox empty. READY leads are 3 (Oxford 2, Madrid 1), all our own trees without a photograph, so `ADD_NEEDS_PHOTO` and the paused own supply keep them waiting.
- `photo_hunt.py --recheck` run twice: both swept the same 40 kept-set trees (ali, ams, arn), 0 new candidates; the sweep does not advance past them. A session with time should look at why the other ~985 unchecked photo-less trees are never reached.

## 2026-10-23 night run, twelfth attempt (19:44 window): nothing published

Rungs 1 and 2 clear (0 reader photos waiting, health.py clean, 0 BLOCKER). Own supply is paused, enrichment says nothing to do, `recognise.py --stuck` and `pagegaps.py` are empty. `photo_hunt.py --recheck` swept 40 kept-set trees: 0 new candidates, so no viewing pass. Scout target Stirling was already retried earlier today (still stalled), so I did not repeat it. Nothing refused in the shell.

## 2026-10-24 every map draws pins the Airbnb way, never counted bubbles (live, web and app)

Hidde, an hour after the city map got bubbles: "je wil ook niet nodeloos bubbels openklikken ... kun je deze interactie bij airbnb onderzoeken". Airbnb and Google Maps never pile a results map into counted bubbles (benchmark in CONVENTIONS.md); shown Lisbon both ways, he chose: "Doe de Airbnb-manier overal ... Web en app." Now on every map (city, /explore, country and state, My trees, the app): every tree drawn, a full pin where none stands within 40 px (lib/map.ts PIN_DISTANCE, TreeMap.swift pinDistance), photograph first, a dot for the rest, a tap always opens the tree, nothing zooms for you. The app's own grid clusterer is gone; MapLibre's symbol collision places the pins there and on the circle-pin maps, the city map does the pass over its DOM pins. The one bubble left is a same-spot stack, from zoom 14 only (STACK_ZOOM, stackZoom). Checked on mocks of the live pages at 375px and desktop (Lisbon 18 pins and 18 dots at the opening zoom; explore 98 pins and 2,731 dots over Europe; Italy; My trees filled and hollow) and in the simulator (Lisbon, the Ajuda stack); the app built twice and its unit tests pass. qa `check_every_map_shows_pins_the_same_way()` refuses a clustered source, the old grid, or the two numbers drifting. DECISIONS.md 2026-10-24, CLAUDE.md one line. Not done: the night's three cluster tests were replaced by three pin-rule tests; a walk through the UI test sweep on CI will say whether the grid tap still lands.

## 2026-10-24 city map piles its own trees like every other map (live)

Hidde, on /lisbon (36 trees): the city map drew every species pin over the others zoomed out while /explore, the country maps, My trees and the app showed counted bubbles ("kunnen we die interacties gelijk houden?"). The city map now carries a clustered source of its own trees that decides which DOM pins show and draws the same moss bubble with the count, from the shared numbers in lib/map.ts (radius 13, distance 40, piles to zoom 14); a tap zooms to where the bubble parts, past zoom 14 the species pins and the same-spot stacks are back, and a selected tree flies to 15.5 so its pin never lands inside a bubble. Checked on a mockup of the live pages at 375px and desktop: Lisbon 6+2+16+10 plus two pins, Palermo, London 27 in six piles plus five, Bruges one 2 beside two pins. qa `check_every_web_map_piles_with_the_same_numbers()` refuses a map file writing those numbers as literals. CONVENTIONS.md "How close two pins have to be" got the dated line. Seen in passing, not fixed: /london at 375px opens at zoom 8.4, below FAR, so the live page shows one 32 bubble and no pins until you zoom in.

## 2026-10-23 night run, eleventh attempt: nothing live, photo lane nearly empty

No claims stood. READY is still 3 (Oxford 2, Madrid 1) and own supply is paused, so no write pass. `photo_fetch.py --roster` had only four images left to look at, and I viewed them: 3 rejected (seedling leaves twice at lux_009, a dark horse chestnut for the plane tri_032), 1 held (tri_003: a good giant sequoia 89 m from the pin where the entry says Ghost Pine, so trunk and species need a check). Approved 0. The sweep of the kept set is close to exhausted; the next lever is checking tri_003 or Hidde lifting the pause.

## 2026-10-23 night run, tenth attempt: nothing published

No claims stood. READY is still 3 (Oxford 2, Madrid 1), none with a photograph, so own-supply rules stop them. `photo_hunt.py --recheck` swept the same first 40 kept-set trees (Alicante, Amsterdam, Arnhem) again: 0 new candidates, so the sweep order needs to advance before it is worth running again. Nothing dispatched.

## 2026-10-23 night run, ninth attempt: nothing published

Resolved a LOG.md rebase conflict with the city-map entry and pushed. No claims stood. READY is 3 (Oxford 2, Madrid 1), none with a photograph, so `ADD_NEEDS_PHOTO` and `SUPPLY_PAUSED` stop a write pass from shipping them. enrich.py reports nothing to do, the Stirling register was retried earlier today, and a verify pass on a staged city would only add leads that cannot go live. Nothing dispatched.

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

