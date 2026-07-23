# LOG

What the autonomous runs did, newest first. One entry per run that actually changed something. Hidde reads this to catch up, and says good or bad.

Format, deliberately short:

```
## YYYY-MM-DD HH:MM — what it did in one line
- What changed (files, pages, cities)
- Why, if it was a judgement call
- FOR HIDDE: only when something genuinely needs him. Otherwise leave it out.
```

If an entry has no `FOR HIDDE` line, nothing is waiting on you. That is the normal case.

---

# Open with Hidde

Standing list. Everything else in this file is history; this block is what is actually waiting.

### 1. ~~Make the submission form~~ — DONE 2026-07-21

Form is live and wired in. Every contribution button on the site points at it, and
runs read the published CSV (email column excluded, so no address ever reaches a
run or the public sheet). Form: `SUBMISSION_FORM_URL`, responses:
`SUBMISSIONS_CSV_URL`, both in `scripts/build_site.py`.

Only thing left on Hidde: nothing, until submissions arrive. Then he may want to
mail the people who left an address to say their tree went live. That list lives
in the private column of his own spreadsheet.

### 2. Illustrated icons (needs Hidde's eye, do it together)

Map pins should move to the painterly style he asked for, and to leaf shapes so species actually differ. Six of Lisbon's ten trees still share one broadleaf silhouette. Deliberately not started alone: it is taste work.

### 3. Unanswered question

He said "je kan niet de website gratis maken". Everything so far assumes the opposite: the site stays free forever because it is the entire acquisition engine (blueprint P9), and the app is what people pay for. Worth settling, because it changes a lot.

### 4. Later, not now

Analytics once there is traffic, and cookieless to avoid a consent banner. Search Console reading needs his Google credentials; no data worth reading yet.

---

## 2026-07-23 — Dublin photo pass: 1/10 to 3/10

- First "rest of the lead group" city (Ireland) after UK and Netherlands. Found solid CC BY-SA matches for the St Anne's Park cypress sculpture and the Holm Oak Avenue, both pinned precisely by their Commons captions and categories.
- Found a third candidate, a plane tree at Trinity College, but couldn't confirm it's the New Square pair specifically rather than the separate Provost's Plane elsewhere on campus, so left it as found_needs_check instead of guessing.
- No photo anywhere open for the sequoia at the President's residence, the private-garden yew (expected, it's barely open to the public), Addison's Walk, the Provost's Plane itself, the Farmleigh sycamore, or the Corkagh oak avenue.
- Dublin at 3/10, below the floor, honestly. Moving to Brussels next, then Antwerp, to finish the lead group.

## 2026-07-23 — Amsterdam photo pass: 4/10 to 5/10 (plus one needing a visual check)

- Second focus-region city (Netherlands, after Edinburgh). Found a strong CC0 match for the Olifantsiep, whose Commons caption names its exact street corner. Found a public-domain candidate for the Lomanstraat tree tunnel too, but couldn't confirm from its description that the canopy effect is actually in frame, so left it as `found_needs_check` instead of approving it blind.
- No photo exists anywhere open for the Heimanseik (Artis keeps its own photography copyrighted), the Vondelpark poplar, the Hortus cycad, or the Amstelkade olive willow. For the cycad specifically, deliberately did not reach for a generic photo of the species from elsewhere, since this project already had to correct exactly that mistake once (a Kirstenbosch photo used for what should have been the Amsterdam specimen). Recorded all 4 as missing rather than stretched.
- Amsterdam at 5/10, below the floor, honestly.
- Moving to the rest of the lead group next (Dublin, Brussels, Antwerp), then the marquee European cities.

## 2026-07-23 — Edinburgh photo pass: 1/10 to 4/10, plus a live location fix

- Started the photo floor work from Hidde's 2026-07-22 decision (80% target, focus region UK/Netherlands first). Edinburgh was the weakest UK city, only London's already at 10/10.
- Hunted Commons/Geograph, iNaturalist, Flickr CC, Openverse and RBGE's own site for all 8 photo-less trees. Found and verified 3: the Sweet Chestnut, the Wentworth Elms of Holyroodhouse, and the Hermitage of Braid beech path (upgraded from a prior found_needs_check once re-verified against its Commons category and description).
- While verifying the Sweet Chestnut's photo, found the published entry had the wrong location: RBGE's own page for this tree says Pond Lawn, the data said Rock Garden. Fixed, since a wrong location is exactly the mistake this project can't afford.
- The other 6 (Cammo Ash, Cedar of Lebanon, Lauriston Castle monkey puzzles, St Cuthbert's Camperdown elm, the Cramond rockface sycamore, Corstorphine sycamore) have no open-licensed photo anywhere after a real search. Recorded in CURATION.md and left as missing rather than forced. Edinburgh sits at 4/10, below the floor, honestly.
- Moving to Amsterdam next for the same pass (Netherlands, focus region), then the rest of the lead group.

## 2026-07-22 15:35 — Antwerp: 15th city live, 10 trees researched

- Straight coverage after Brussels: no submissions, site healthy, nothing published wrong. Antwerp is a thinner data city than Brussels: no dedicated tree register, just Flanders' general heritage inventory, so most ages here are honest ranges (champion girths, protection dates) rather than planting records. Said so directly in the intro rather than dressing it up.
- Dropped one promising-looking candidate after checking it properly: the fig tree in the Rubenshuis garden has a genuine 1638 letter linking Rubens to fig trees in his own garden, but the tree standing there today is part of an explicit 2023 museum reconstruction, potted rather than planted, not a survivor. Including it would have implied a continuity that isn't real, so it's out.
- Also caught and fixed a location mixup mid-search: an early "540cm Canadian poplar" result was actually in Geraardsbergen, 40km away, not Antwerp. Found a genuinely Antwerp-located poplar of similar size at Eric Sasselaan instead.
- One young tree included on purpose: a Grote Markt linden planted in 1994 for the 50th anniversary of Antwerp's liberation, labelled "Youngest tree" so nobody mistakes precise 1994 dating for an old specimen.
- 0 of 10 photos found despite real searches; recorded honestly. Site rebuilt, all contracts validated, pushed.

## 2026-07-22 13:50 — Brussels: 14th city live, 10 trees researched

- Straight coverage after Edinburgh: no submissions, site healthy, nothing published wrong. Brussels turned out unusually well documented: the region has run its own official scientific inventory of remarkable trees since 2002, so most ages and girths here come from that register rather than estimation.
- Best story of the run: Parc du Cinquantenaire was built in 1880 for Belgium's 50th anniversary, and rather than planting saplings, city gardeners transplanted already mature trees in from an old cemetery and the Sonian Forest, so parts of the park looked centuries old on opening day. Used as the city's unifying thread.
- One correction worth flagging for whoever reads this next: a source claimed trees over 250 years old at the Boitsfort hippodrome, but that can't apply to the entry's own Douglas fir, since the species only reached Europe in 1827. Capped the age range instead of repeating an impossible number, the same discipline as catching a bad photo match.
- 0 of 10 photos found despite a real search; Brussels' trees are thoroughly documented in text but thinly photographed under open licenses. All 10 flagged missing honestly rather than guessed. The official inventory's own site likely has photos worth checking for licensing in a future pass.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-22 11:40 — Edinburgh: 13th city live, 10 trees researched

- Checked the ladder first: no reader submissions (CSV still just a header row), site builds clean, nothing published is wrong. Every one of the 12 live cities had already had a real photo-hunting pass earlier today (see the long run of entries below), each with genuine near-misses recorded, so doing it all again immediately would have been looping rather than progress. That put this run on coverage: the next pending city, Edinburgh.
- 10 trees, unifying thread is that Edinburgh's exposed hilltops rarely let a tree survive centuries in the open, so almost everything here owes its age to a wall someone built for other reasons: a castle courtyard, a botanic garden fence, a private estate, a churchyard, a royal palace garden.
- Judgement call worth flagging: dropped a strong candidate, the Robert Louis Stevenson yew at Colinton Manse (possibly the city's actual oldest tree, documented since 1638), because it stands in private grounds with no scheduled public access at all, only a glimpse over the churchyard wall. Different situation from Dublin's Old Glebe yew, which genuinely opens some weeks a year. Full reasoning in CURATION.md.
- 2 of 10 photos found and personally license-checked against their Commons file pages (Craigmillar Castle's yews, approved outright; the Hermitage of Braid's beech woodland, found_needs_check). 8 missing after real searches. One photo candidate for the Corstorphine sycamore was caught and rejected: its caption placed it at a different tree entirely (a conservation specimen at the Botanics, not the churchyard one).
- Site rebuilt, all contracts validated, pushed.

## 2026-07-22 09:45 — Kyoto: photo floor pass, 1/10 to 3/10

- Lead group and marquee-European cities are as far as prior runs could take them today, so moved to the next tier: Istanbul, Kyoto and New York. Kyoto (1/10) was oldest-published of the three and untouched this run, so went first.
- Found 2: the Weeping Cherry of Gion in Maruyama Park (CC BY 2.0, a Flickr-sourced Commons file with coordinates about 50m from the pin) and the Emperor's Camphor of Imakumano (CC BY-SA 4.0, a Commons file titled with the tree's own alternate name, "Shoryu Benzaiten," coordinates also about 50m from the pin). Both flagged `found_needs_check` since this is a text workflow without image vision.
- Kyoto now at 3/10. 7 remain missing after real searches, several with dedicated Commons categories that still turned up nothing tree-specific (Munakata Shrine's camphor, Nishi Honganji's famous inverted ginkgo, Sanbo-in's Taiko cherry). Left open rather than looped on.
- Site rebuilt, all contracts validated, pushed. Next: Istanbul or New York.

## 2026-07-22 09:15 — Tokyo photo pass: no new finds, honestly recorded

- Marquee-European sweep is closed out for this run, so checked the city closest to the floor overall: Tokyo at 7/10, needing just one more. Nothing cleared the bar this pass; one near-miss (a memorial-stone photo at Koishikawa Botanical Garden) checked and rejected since it documents the marker, not confirmed to show the tree itself.
- Recorded in CURATION.md so a future run knows this was tried. This closes a long run of photo-floor work: Amsterdam, Dublin, Lisbon, Paris, Rome, Barcelona and Madrid all got a genuine pass this session, plus this Tokyo check.

## 2026-07-22 08:55 — Madrid: photo floor pass, 1/10 to 2/10

- Last marquee-European city below floor after Barcelona. Found 1: the Bald Cypresses of the Crystal Palace Pond, CC BY-SA 4.0, the same photo already used on that tree's own Spanish Wikipedia article.
- Madrid now at 2/10. This closes the marquee-Europe sweep for this run: Lisbon, Paris, Rome, Barcelona and Madrid all got a genuine photo pass this session. None hit 8/10 outright, all moved forward, all gaps recorded honestly rather than papered over.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-22 08:25 — Barcelona: photo floor pass, 1/10 to 2/10

- Next oldest marquee-European city below floor after Rome, and the thinnest coverage in the queue at 1/10. Found 1: an aerial public-domain view of La Rambla's plane tree canopy, a good fit since that entry is already pinned as a 256-tree ensemble rather than a single specimen.
- Two near-misses rejected: a Carrer de la Encarnació street photo at the wrong building number with no tree visible, and Plaça de Prim's Commons files, none confirmed to show the ombú itself.
- Barcelona now at 2/10, smallest gain of the run so far. 8 stay missing after genuine attempts.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-22 07:55 — Rome: photo floor pass, 4/10 to 6/10

- Next oldest marquee-European city below floor after Paris. Found 2: the Quercia del Tasso (CC BY 2.0, also independently confirms the tree is a propped remnant, matching the existing honest framing) and the Cedar of the Garibaldi Mausoleum (CC BY-SA 4.0, GPS within 30m of the existing pin).
- One near-miss rejected: a Villa Doria Pamphilj cedar photo that looked right for the Cedar of the Belvedere but sits about 1.2km from that tree's pin in a large park with multiple documented cedars, likely a different specimen.
- Rome now at 6/10. 4 stay missing after genuine attempts, left open rather than looped on.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-22 07:20 — Paris: photo floor pass, 3/10 to 6/10

- Next oldest marquee-European city below the floor after Lisbon. Best hit rate of any photo pass this run: 3 of 7 missing trees found (the Buffon Plane, the Elm of Saint-Gervais, the Caucasian Elm of Avenue Foch), all clean matches with independently confirming detail in the file descriptions themselves.
- Paris now at 6/10, closest yet to the 8/10 floor. 4 stay missing after real attempts (the Second Robinier, the Sequoia of Buttes-Chaumont, the Parc Montsouris plane, the Sophora by the lake), left open rather than looped on.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-22 06:45 — Lisbon: photo floor pass, 3/10 to 5/10

- Lead group (London, Amsterdam, Dublin) is as far along as this run could get it; moved to marquee European cities next, oldest-first. Lisbon (3/10) was next.
- Found 2: the Praça Paiva Couceiro ginkgo (CC0) and the Jardim da Luz coral trees (CC BY-SA 4.0). One near-miss rejected: a silk floss tree photo that looked right by species and name but its coordinates put it 2.5km from the actual tree, a different specimen in a different neighbourhood.
- Lisbon now at 5/10, still short of the 8/10 floor. 5 trees remain `missing` after genuine attempts, left open for a future pass rather than looped on further.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-22 06:05 — Dublin photo pass: no new finds, honestly recorded

- Same rung as the Amsterdam pass just before it, continuing oldest-first down the focus region: Dublin (1/10) after Amsterdam (now 3/10). Searched Commons, iNaturalist and Flickr for all 9 missing trees.
- Nothing cleared the bar. Two near-misses checked and rejected: a general New Square photo that doesn't clearly show the champion plane trees themselves, and Aras an Uachtarain's well-documented Obama tree-planting photos, which are a different, newer tree from the one this city page needs.
- No file changes from the tree data itself; recorded in CURATION.md so a future run does not re-spend the same searches without knowing they were tried. Moving to the next focus-region city.

## 2026-07-22 05:40 — Amsterdam: photo floor pass, 2/10 to 3/10

- Hidde's new rung 4 (CLAUDE.md, decided 2026-07-22 while this run was already going): published cities below an 8-of-10 photo floor now outrank starting a new city, focus region first, oldest-first. Within the lead group, London is already at 10/10 and Dublin (just published this run, see below) was still ahead of me in the queue, so Amsterdam went first as the oldest lead-group city still below target.
- Found 1 of the 7 missing: a 1973 Nationaal Archief photo of the Amstelveld, CC0, correctly showing that square's trees but not a current-day image, so flagged rather than presented as-is. Amsterdam now at 3/10.
- The other 6 stayed `missing` after genuine searches, including two near-misses caught and rejected: a Hortus Botanicus cycad photo that doesn't identify which of the garden's several cycads it shows, and a same-species photo from Kirstenbosch, South Africa, that would have misrepresented a different continent's plant as the Amsterdam specimen.
- Did not reach the 8/10 floor this pass. Recorded in CURATION.md per the rule's own escape valve (record and move on rather than loop forever) and left open for a future pass. Continuing down the focus region: Dublin is next, since it also now sits below the same floor.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-22 04:20 — Dublin: 10 trees researched, twelfth city live

- Next pending city on the ladder, no reader submissions waiting and no city sitting at zero photos, so straight to coverage. Dublin joins the site with 10 trees in `data/cities/dublin.json`.
- The thread connecting all ten: Dublin's remarkable trees are civic and institutional rather than royal-forest survivors. A plane tree slowly eating a park bench at King's Inns, a giant sequoia Queen Victoria planted at the President's residence in 1861, two Georgian squares at Trinity, a dead cypress carved into a wildlife sculpture instead of felled, and three former private estates (Farmleigh, St Anne's, the Botanic Gardens) now open to everyone.
- 4 flagged, all for genuine reasons stated in the data: a disputed 500-700 year age range and unverified Swift legend for the oldest tree (a yew that only opens to the public a few weeks a year under a heritage tax scheme, disclosed honestly rather than glossed over); a chronology that doesn't add up for the Botanic Gardens' yew avenue; two Trinity College sources that disagree with each other on one plane tree's age; and a "220 years" claim for Farmleigh's oldest sycamore that traces to one repeated source rather than two independent ones.
- One near-miss worth recording: nearly used a walnut tree at a Tallaght priory (St Maelruain's Tree) as the oldest-tree candidate, but dropped it after research showed the site has no established public access, only a blogger's account of being personally let in by a groundskeeper. Not "genuinely open to visitors" under hard rule 10, so left out entirely rather than flagged.
- 1 photo found (the Hungry Tree, CC BY-SA 2.0 via Geograph), 9 missing after a real search across Commons, iNaturalist and Flickr for each named tree; nothing held the city back. The Hungry Tree is also the one pin marked `confirmed`, from a precise Wikipedia coordinate; the other nine are honestly `approximate`.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-22 03:10 — Istanbul: 0 photos to 2

- Same rung as the London pass just before it: a published city with zero photographs. Istanbul was the other one at zero. No reader submissions, site healthy.
- Only found 2 of 10 this time, and that is a coverage fact about Istanbul rather than a shortcut taken: Wikimedia Commons simply has far less documentation of Istanbul's monument trees than of London's. Searched Commons in English and Turkish, plus iNaturalist, Flickr and Openverse, before accepting that.
- Got: the Hüseyin Avni Dede Plane (its photo's own GPS lands about 50m from the existing pin, a nice bonus confirmation) and the Karacaahmet cypresses (a general shot of the cemetery's cypress canopy, honestly not tied to one of the nine specific protected trunks, matching that entry's existing caveat).
- The other 8 stay `missing`, per the mandate: photo coverage is always cuttable, so this moves on rather than digging further for a fifth or sixth find. Good candidates for a future improvement-mode pass.
- Site rebuilt, all contracts validated, pushed. Both zero-photo cities are cleared; Singapore is next.

## 2026-07-22 02:15 — London: 0 photos to 10

- No reader submissions (CSV checked: header row only, no data rows). Site build was healthy. That put rung 4 on top of the ladder: a published city with zero photographs, which outranks starting the next pending city (Singapore). London and Istanbul were both at zero; London went first as the older of the two.
- All 10 London trees now have a Wikimedia Commons photo with a checked licence (CC0, CC BY or CC BY-SA) and attribution, status `found_needs_check` pending your eye. Every file page and licence tag was independently verified, not taken on trust.
- Found a real fact error while at it: the Fulham Palace Oak was recorded as a Pedunculate Oak. It is a Holm Oak, per the Palace's own site plus an independent source, and quite possibly the oldest holm oak in the country. Fixed the species, age range and story, added two sources.
- Barney the Plane's pin got more precise (exact EXIF coordinates from a geotagged photo captioned with its name) but stays `location_precision: approximate` on purpose, since only one source names this specific tree so far.
- Site rebuilt, all contracts validated, pushed. Istanbul is next for the same zero-photo pass, then Singapore.

## 2026-07-22 01:00 — New York researched and live: 11 cities, 110 trees

- No reader submissions (CSV checked: header row only). Site healthy, nothing published was wrong, so went to the next rung: the next pending city, New York.
- 10 trees researched, written and shipped, deliberately two per borough. The throughline: NYC runs its own government Great Trees registry (since 1985, expanded 2024), and every tree here carries that official designation. Full detail and what's flagged in CURATION.md.
- One tree dropped after research, not before: Flushing's famous Weeping Beech, NYC's first living landmark, died in 1998 and got a public funeral. Would have been a great story on a dead tree; replaced with a living one from the same historic nursery grounds instead, same rule that's kept dead trees off other cities' lists as if they were alive.
- 2 of 10 photos found: the Camperdown Elm and the Queens Giant, both CC BY-SA on Wikimedia Commons. The Queens Giant photo's own GPS metadata gave an unusually precise, confirmed coordinate for the tree itself, one of the few trees on this whole site with a truly surveyed pin rather than an estimate.
- 8 of 10 pins approximate otherwise, honestly: most sources only gave building or park-level coordinates, not a surveyed point for the specific trunk.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-21 23:45 — Madrid researched and live: 10 cities, 100 trees

- No reader submissions (CSV checked: header row only). Site healthy, nothing published was wrong, so went to the next rung: the next pending city, Madrid.
- 10 trees researched, written and shipped. The throughline: almost every remarkable tree here is a foreign import planted by royal gardeners testing what could survive Madrid's climate, a Mexican cypress, a Himalayan cedar, an Atlas cedar, a Caucasus elm. Full detail and what's flagged in CURATION.md.
- Two research near-misses caught before they shipped, both location errors: a "1,000-year yew" and a "41-metre sequoia" that first looked like Madrid candidates turned out to be in Rascafria and El Escorial/Aranjuez, separate towns in the wider region, not Madrid city. A supposed Casa de Campo oak, "Encina del Mesto," turned out on checking coordinates to be a same-named tree in a different municipality entirely. All three swapped out or dropped rather than shipped on a name match.
- 1 of 10 photos found: the Ahuehuete, Madrid's presumed oldest tree, public domain via a university archive upload, confirmed to be the right tree by its file description.
- All 10 pins approximate this round, honestly: most sources gave building or park-level coordinates rather than a surveyed point for the tree itself, and no source closed that gap. Nothing here claims precision it doesn't have.
- One age dispute worth a look if you know Madrid: the Ahuehuete's popular 1633 planting date (390 years) versus city arborists' own ~200 year estimate. Presented as a range rather than picked.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-21 22:30 — Kyoto researched and live: 9 cities, 90 trees

- No reader submissions (CSV checked: header row only). Site healthy, nothing published was wrong, so went to the next rung: the next pending city, Kyoto.
- 10 trees researched, written and shipped. The throughline: unlike most cities so far, none of Kyoto's ten are wild trees that happened to survive in a park. All ten are cultivated specimens shaped by centuries of temple and shrine care, including a shogun's bonsai trained into a boat shape and a pine bent flat and named for a dragon in 1857. Full detail and what's flagged in CURATION.md.
- Caught a real near-miss before it shipped: Shimogamo Shrine's most famous sacred tree, revered as the oldest in its forest, turned out to have fallen down on 2026-06-16, a month before this run. Would have been an easy thing to miss and publish as living.
- 1 of 10 photos found: the ~600-year-old Land Boat Pine at Kinkaku-ji, CC BY-SA on Wikimedia Commons, confirmed by GPS metadata to be the right tree.
- 6 of 10 pins approximate, honestly: several temple trees only have building-level coordinates confirmed, not a surveyed point for the tree itself inside the grounds. One tree, a 1,200-year cedar in a remote forest northwest of the city, turned out to have real restricted access (prior arrangement with the city and a guide required); included anyway with that stated plainly in the access field rather than smoothed over.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-21 21:15 — Barcelona researched and live: 8 cities, 80 trees

- No reader submissions (CSV checked: header row only). Site was healthy, nothing published was wrong, so went to the next rung: the next pending city, Barcelona.
- 10 trees researched, written and shipped. The throughline: Barcelona keeps two tree registries, a broad municipal catalogue and a much stricter Catalan government "monumental" list held by only four trees citywide, all four sharing one ravine in the historic botanical garden, declared together in April 2025. Used that as the city intro.
- Two of the ten grew up inside Park Guell before Gaudi built it: one still roots beneath the viaduct's stone columns, the other is a 1907 regrowth shoot from a much bigger carob that died back, ringed by its own dead wood. Full detail and what's flagged in CURATION.md.
- 1 of 10 photos found: a public-domain 1904 photo of the viaduct carob, confirmed as the right tree. Caught a near-miss on tree #1's photo, a similarly named Wikimedia file turned out to be a different holm oak entirely on checking the file page directly; not used.
- 5 of 10 pins approximate, honestly: two botanical-garden trees and one Laberint d'Horta tree have only the park's entrance coordinates, not a surveyed point inside the fenced ravine; the Encarnacio oak has no surveyed lat/long in any source; the Rambla plane trees are pinned as the ensemble they are, not one tree standing in for 256.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-21 20:00 — Istanbul researched and live: 7 cities, 70 trees

- No reader submissions yet (checked the CSV, header row only). Site was healthy (build clean, contracts passing), nothing published was wrong, so went straight to the next pending city per the ladder: Istanbul.
- 10 trees researched, written and shipped. Istanbul's oldest tree, a 1,300-1,400 year old plane, turned up in an unlikely place: a university forestry research forest in Bahçeköy, not a palace or a mosque. Two more protected monumental trees share that same forest.
- The throughline that fell out of the research: Istanbul's grandest, most photographed old trees mostly did not make it. The plane said to have witnessed the 1453 conquest inside Topkapı Palace died by 1928; Dolmabahçe's palace planes were felled for canker disease in 2022. What survived instead is unglamorous: a working forest, a bazaar entrance where a poet has sat under the same tree since 1964, a cemetery, a storm-toppled plane in Çengelköy that city crews nursed back to life after 2017. Used that as the city intro.
- One judgement call worth flagging: several sources described a Çengelköy plane as "780 years old" with a 1993 death under a falling branch. I could not confirm that claim and this storm-survivor tree are the same specimen, so I dropped the unverifiable parts and told the story I could actually source: uprooted by a 2017 storm, replanted and still recovering. Better story, and true.
- 4 of 10 flagged for disputed ages or thin sourcing (two of the Bahçeköy forest trees, the Karacaahmet cemetery cypresses, the Florya mastic tree). Full detail in CURATION.md.
- 0 of 10 photos found this round. Searched Wikimedia Commons for every tree; nothing came back as a confident match to the specific named tree, so all ten are `missing` rather than guessed. Worth another pass, especially Küçük Çamlıca, Büyükada and Beyazıt, which are touristy enough that photos likely exist somewhere.
- 8 of 10 pins approximate (forest, park, cemetery or meadow locations with no street-level source for the exact tree), 2 confirmed. No pin claims more precision than it has.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-21 18:30 — Tokyo researched and live: 6 cities, 60 trees

- No reader submissions yet (checked the CSV, header row only). Site was healthy (build clean, contracts passing), nothing published was wrong, so went straight to the next pending city per the ladder.
- Tokyo: 10 trees researched, written and shipped. Zenpukuji's 750-year-old ginkgo leads as Tokyo's oldest living tree; Sensoji's war-scarred ginkgo, Ueno Toshogu's 600-year camphor, and Meiji Jingu's ginkgo avenue and camphor couple round out the list. Full detail and what's flagged is in CURATION.md.
- The throughline that fell out of the research: Tokyo has burned down repeatedly (1657, 1868, 1923, 1945), and five of the ten surviving trees are ginkgos, a species whose wood resists catching fire. Used that as the city intro instead of a generic "remarkable trees of Tokyo" opener.
- 7 of 10 photos found on Wikimedia Commons (open licenses, awaiting your approval like always). 3 missing, none faked.
- 6 of 10 pins confirmed, 4 approximate (all cases of a tree inside a large garden or spanning an avenue rather than a single small address). No pin claims more precision than it has.
- Site rebuilt, all contracts validated, pushed.

## 2026-07-21 17:00 — The funnel, thought through properly

Hidde asked for this while away. Written to be read cold.

**The funnel today, honestly:**

1. Someone finds the site. Nobody does. No distribution has happened, and the domain is new, so organic search will take months, not weeks.
2. They land on a city or tree page. These are good: story, map, directions, nearby trees.
3. They read.
4. They walk to a tree. Nothing bridges this, and it is where the product lives or dies.
5. They return, or pay. No mechanism, no evidence anyone would.

**The leak nobody is looking at is step 3 to 4.** Everyone is worried about step 1, and step 1 is real, but it is not the part we control. Someone reads about the Heimanseik at 22:00 on a Tuesday, thinks "nice", and never goes. The whole product is a destination read indoors, while the value only happens outdoors, on another day. Nothing currently carries the intent across that gap.

Three things close it, in order of how much they help:
- **A reason to go now.** Seasonality is the strongest and we have none of it: catkins, blossom, autumn colour, the month a given tree is worth the trip. That is knowledge nobody else has, it is cheap to research alongside the trees themselves, and it converts "nice" into "this weekend".
- **A way to keep it.** Saving a tree or a route for later, in LocalStorage, no account. Cheap, and it is the only thing that survives closing the tab.
- **The walk.** Built 2026-07-21. Turns ten scattered facts into one afternoon.

**On measurement, which is what makes the rest answerable.** Cloudflare analytics went live today, so within days we will know whether anyone arrives at all and which pages they land on. That is the first real signal this project has ever had. Note what it cannot see: whether anyone actually walked. Nothing on a website can see that, and pretending otherwise would be the wrong thing to build.

**The uncomfortable conclusion.** Every funnel improvement below step 1 multiplies a number that is currently zero. Distribution is the only step that changes the zero, and it cannot be automated: it needs Hidde to tell actual people this exists, once. Until that happens, more cities is the right work (it builds the SEO base that pays off in months) but it produces no learning at all. Runs should keep going wide, and nobody should mistake that for progress on the question of whether anyone cares.

FOR HIDDE: one post, one link, to any group of people who like trees or like Amsterdam. That is the whole ask, and it is worth more than the next twenty cities.

## 2026-07-21 10:15 — Paris pulled above the quality floor instead of starting city six

- Priority ladder in CLAUDE.md (rung 3, quality floor) beat rung 4 (next pending city, Tokyo): with the honest `location_precision` count from the previous run, Paris and Amsterdam were both below floor, and Paris was worse (8 of 10 approximate, 2 of 10 photos).
- Resolved all 8 approximate Paris pins to confirmed. Five city park/avenue trees matched against the Ville de Paris open tree registry (opendata.paris.fr); the three Jardin des Plantes trees aren't in that dataset at all (the garden belongs to the Museum national d'Histoire Naturelle, not the city) so those came from OpenStreetMap's individually named heritage-tree nodes instead, cross-checked against sourced planting dates.
- Added one photo (Great Plane of Parc Monceau, Public Domain), clearing Paris's photo floor too.
- Paris now has 0 approximate pins and 3 of 10 photos. Full detail in CURATION.md.
- Amsterdam is still below floor (7 of 10 approximate, 2 of 10 photos) and is next in line for the same treatment, ahead of Tokyo.

## 2026-07-21 09:00 — Every pin now says honestly how precise it is

- Set `location_precision` explicitly on all 50 trees. It was set on none of them, despite CLAUDE.md requiring it on every tree.
- The site had been guessing instead: `location_is_approximate()` sniffed free-text notes for ten hardcoded phrases like "exact position". Trees whose notes described a rough pin in any other wording rendered as confident pins with no warning.
- Six trees were lying to visitors that way. Adonis in Villa Borghese is the clearest: its note says the coordinates point at the Valle dei Platani generally, "not Adonis's specific trunk", and the page showed no warning. Same for the Hortus cycad, the Amstelveld wingnuts, the Rijksmuseum wingnut, the Belvedere cedar and Barney.
- Replaced the keyword guessing with the field alone, and made a missing field count as approximate. A warning nobody needed costs a visitor nothing; a missing one costs them a wasted walk.
- Result: 25 of 50 pins are approximate. That is high, and it is the real number. It also says where the improvement runs should go first: Paris (8 of 10) and Amsterdam (7 of 10).

## 2026-07-21 — Working agreement set up

- Added this log, plus a priority ladder and decision boundary in CLAUDE.md, so runs know what to work on and what to leave alone.
- Nothing about the site itself changed.
- FOR HIDDE: the boundary is in CLAUDE.md under "What runs decide alone". If anything in the "ask first" column feels too strict or too loose, move it. That list is the whole steering wheel.
