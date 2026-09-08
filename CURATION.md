

<!-- archive-index -->

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-08](archive/CURATION-2026-08.md)
- [2026-07](archive/CURATION-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.

## 2026-09-08 (continuation, previous attempt stopped after 17 min with 103 min unspent) - Radomsko, Stokaičiai, Pajūris opened; a coordinate copy-error caught before it shipped

Picked up per the standing instruction: two earlier attempts in this window
had claimed `_famous-japan` (write), `_famous-lithuania` (write) and
`_famous-poland` (verify) and left completed-but-uncommitted work on disk.
Merged and released `_famous-japan` first (4 single-tree places:
Aizuwakamatsu, Iida, Kitakata, Oyodo), then `_famous-poland`'s verify
output (1 tree, rad_001).

Dispatched a write pass on the remaining READY leads across cities (2
Lithuania, 1 Poland, 1 Utrecht):

- **Radomsko** (Poland, 1 tree, flagged: 0): The Insurgents' Linden,
  three limes planted 1863 on the grave of three killed insurgents,
  fused into one trunk, 5.33m round, extensive 2021-2022 conservation
  surgery.
- **Stokaičiai** (Lithuania, 1 tree, flagged: 1): The Visbarai Pine,
  single-sourced, no age.
- **Pajūris** (Lithuania, 1 tree, flagged: 1): The Akmenynė Oak,
  single-sourced (a second source confirms existence but not
  measurements), no age.
- **Utrecht's "Peer" lead was a duplicate, not a new tree.** Its
  coordinate (52.08586, 5.12903) was an exact copy of utr_018's own
  coordinate, a transcription bug caught by passcheck.py's duplicate
  detector before anything shipped. The register's real row for that
  entry (LRMB nr 1678119) gives 52.086488, 5.118036, which turned out
  to be the ALREADY-PUBLISHED utr_031 (The Old Pear of the
  Geertebolwerk). Folded its species (tightened to the canonical
  "European Pear (Pyrus communis)") and measurements (girth_cm 182,
  height_m 11) into utr_031 instead of shipping a second page for one
  tree. Fixed the coordinate in the source lead file too.

All three new places carry full page copy (intro, meta, FAQ) per
Contracts B/C. `city_names.py` run for all three; Stokaičiai's own
match resolved to the containing district rather than the village and
was moved to `unresolved_names` rather than shipped as a wrong alias.
`preflight.py` (556 cities, 0 problems), `astro build` (5090 pages) and
`qa.py` (7959 pages) all clean.

**Also fixed, rung 2:** `ios.yml`'s scheduled iOS-18-floor job has
failed since this morning on a false-positive tap-target FAIL
(`Button 'mytrees-who'` 62 by 14) that a 2026-09-06 fix (an identifier
plus `.accessibilityElement(children: .contain)`) only closed on iOS 26,
not iOS 18. Nothing reads that identifier, so removed it and the now-
unneeded `.contain` rather than trading one false positive for another.
Could not build or run a simulator in this sandbox (Linux, no Xcode);
the scheduled job will confirm. Vendored the one photograph the session
brief flagged as not yet on our own domain (utr_015). Recorded
REVIEW.md's 2026-09-08 superlatives.py WARN as answered (already fixed
in `bfaa50f3` by an earlier attempt this window).

**Verified and wrote up Sweden** (rung 0c, `famous_demand.py --next`):
9 candidates, 3 shipped (Ekerö/Ekebyhovseken, Sweden's largest
deciduous tree by volume, two sources' girth figures both stated
honestly rather than picked; Trollskogen/Trolleken, Öland's oldest oak,
no girth or height found so left absent; Sjukhuseken added to
Stockholm as sto_006, honestly framed as a declining hollow veteran
rather than a pristine specimen), 2 confirmed dead and blocked
(Hagstaeken Huddinge, felled Dec 2025; Lojstaeken, dead since 2001), 4
held for a follow-up pass (genuine designated monuments, one source
each so far). Also fixed Stockholm's intro, stale at "the four" since
before this pass. `preflight.py` (558 cities, 0 problems), `astro
build` (5106 pages) and `qa.py` (7976 pages) all clean.

## 2026-09-08 (continuation 5) - Two new Lithuanian places from a stranded write pass: Vytogala and Pagramantis Regional Park

Merged completed-but-uncommitted work from an earlier attempt in this
window: a `_famous-lithuania` write pass (data/research/famouslithuania-verified.json,
5 trees, full stories) that had been assembled into two new city files
but never committed.

- **Vytogala** (1 tree, single-famous-tree exception): the Vytogala
  Independence Oaks, four oaks around a memorial stone on the birthplace
  of Stasys Girenas, who flew the Lituanica across the Atlantic in 1933.
  Three planted in 1928 for the tenth anniversary of Lithuanian
  independence, the fourth a 1989 replacement. Two sources, girth
  recorded for two of the four, no photo.
- **Pagramantis Regional Park** (4 trees): the Gudlaukis oak (6.30m
  round, hollow, ~600 years by local tradition), the Geniai oak (5.6 to
  5.8m, undated, largest healthy oak in the register pair), the
  Tamosaiciai cemetery oak (4.3m, undated) and the Andriejaiciai oak
  (5m, 300+ years by local tradition, old crosses at its foot). All four
  are Lithuanian state-protected natural heritage objects, listed
  February 2016. No photos.

All 5 trees carry age gaps left honest (local-tradition estimates
stated as such, or left empty with a reader question) rather than
invented, per the estimate-vs-invention rule. `preflight.py` (0
problems), `astro build` (5078 pages) and `qa.py` (7903 pages) all
clean. Also fixed a `lastmod.py` bug found earlier this session: the
translated-tree hash was including fields (`how_to_recognise`,
`curation_status`, `submitted_by`) that `TranslatedTreePage.astro`
never reads, so an English-only edit to one of those fields restamped
every language variant's sitemap entry though nothing translated had
changed; re-derived `data/lastmod.json` against the fix.

Released the `_famous-lithuania` claim. ~30 scattered single-oak leads
from the same batch remain unresearched for a future pass. Nothing
flagged for Hidde.

## 2026-09-08 (continuation 4) - _famous-slovakia refilled, one new place, one live page corrected

Two more parallel verify passes, this time on `_famous-slovakia`. Batch A
delivered 4 candidates; batch B delivered 0 (3 confirmed avenues/rows,
now blocked as non-collectible-points, one genuine pear tree that failed
the single-tree-destination test, kept as a lead).

The write pass then found 3 of batch A's 4 were **already published**:
the Bosaca apple and pear (bsa_001, bsa_002) and the Velke Borove pine
(vbo_001) all exist in data/cities already, under names close enough
that the lead file's own duplicate-name matching missed them (the pear's
lead was "Pink pear from Bosaca", the live tree is "The Pink Pear of
Zabudisova"). `passcheck.py --pending` caught it before any duplicate
prose was written; no harm done beyond the verify pass's own tokens.

Only Komjatice's plane tree was genuinely new. Published as komjatice.json
(kom_001): Slovakia's most commonly cited thickest trunk (930cm, though
the story says plainly that Myjava's hollow lime measures wider), Tree
of the Year 2012, European Tree of the Year top-5 in 2013.

**The duplicate-work near-miss paid for itself**: the verify pass fetched
pravda.sk and teraz.sk directly for the Bosaca pear and got "about 200
years" from both, independently confirming a figure the live page had
explicitly left open as unverifiable ("those articles are no longer
reachable"). That also flips which of Bosaca's two trees is older (the
pear at ~200y, not the apple at ~130y), so corrected bsa_002's age fields
and story, and every city-level field on bosaca.json that named the old
answer: intro, meta_description, question_meta/answer/context,
oldest_tree_id, and two FAQ entries. This is rung-3 work (something
published being imprecise), found as a byproduct of rung-4 work.

Preflight and the Astro build both clean after all of it.
<!-- archive-index -->
## 2026-09-08 (continuation 3) - 8 new single-tree French places from the famous-trees batch

Refilled the shelf with two verify passes on `_famous-france`'s remaining
unsourced leads (batch A: 5 candidates, batch B: 4 candidates, run in
parallel), then a write pass on the 8 that verified. All 8 are standalone
rural French trees, none part of a city cluster, each judged against the
single-famous-tree-destination test in its own `verify_notes`.

Published as 8 new city files, one tree each: Magescq (Chene de Nerthe,
mgs_001), Nicorps (If commun de Nicorps, nic_001), Jauze (If de Jauze,
jau_001), Pesselieres (Le Sully de Pesselieres, pes_001), Feternes (Tilleul
de Chateauvieux, fet_001), Bracon (Tilleul de Grange Sauvaget, bra_001),
Reaumont (Tilleul de Reaumont, rea_001), Chatenay-Malabry (Cedre pleureur
de la Vallee-aux-Loups, cma_001). Tilleul de Joux blocked instead (private
chateau grounds, no evidence of routine public access); both verify passes
reached that verdict independently.

Fixed two writer-side issues before merging: a species-name collision
(both yews delivered as "Common Yew", the site's existing convention is
"European Yew") and an over-60-char tree-page title (Bracon's tree name
carried a redundant French-name parenthetical). Ran `city_names.py` for
search aliases afterward and it produced one wrong one: "bracon" ->
"Arbois", the exact proximity-matching failure its own docstring warns
about (Bracon and Arbois are distinct Jura communes 7.4km apart, not the
same place under two names). Removed that entry from both `search_names`
and `wikipedia_titles`; kept the other 4 (chatenay-malabry, feternes,
magescq, reaumont), which look like genuine local-language spellings of
the same place.

Also, separately: a viewing pass on the Commons photo sweep gave 4 more
single-tree pages (previously photo-less) their first photograph -
Allouville-Bellefosse's Chene Chapelle, Aberford's Nellie's Tree, Aguas de
Moura's Whistler Cork Oak (the 2018 European Tree of the Year) and
Albersdorf's Funffingerlinde - plus the Oak of Hersberg in Altrier. 12
mismatched candidates rejected (wrong commune, a trail sign, generic
village/castle shots, Helmond's two candidates 600m+ from the pins).

And rung 1: 3 reader photographs of Baarn's Cantonspark Giant Sequoia held
rather than approved (matched by distance only; the reader's own
"Watercypres" label and the foliage in all three point to the Dawn Redwood
128m away instead), 2 leads turned out to be indoor test shots through a
window, and a striking unidentified multi-stemmed tree by a stream in Nara
kept as a lead for a verify pass.

## 2026-09-08 (continuation 2) - 40 recognition lines across 8 cities, worst-first by impressions

Week still had headroom, so continued past the Sant'Alfio work. New coverage
was thin everywhere checked: `city_queue.py --next`'s OPENABLE cities mostly
carry 1-2 Wikidata leads each, well under a single verify pass's 6-candidate
floor, and Florida's champion-tree register (the only one covering Daytona
Beach, scout_next.py's suggested target) was already fully scouted and
recorded as a dead end for exactly this reason in an earlier Jacksonville
pass. Rather than force a thin pass, moved to rung 7: `recognise.py --stuck`
(270 trees with no photo, no recognition line, and a government-designated
neighbour within 25m).

Wrote and applied 40 lines, worst-first by search impressions: Lisbon (2),
Barcelona (6), Singapore (7), Vienna (6), Leiden (11), Paris (3), Florence
(4), Prague (1). All restatement from each tree's own story and verify
data per BRIEF_WRITING.md's rule (species, girth, height, setting, what
already distinguishes it from its stuck neighbour), nothing new claimed.
Several pairs needed the "which one" answer directly: Leiden's two Siebold
zelkovas (single-trunk vs five-stemmed), Vienna's oak and yew twelve
metres apart at Schönbrunn (deciduous vs evergreen), the two Bobolino
cedars in Florence (cedar of Lebanon vs the horned incense cedar).
`recognise.py --stuck` backlog: 270 to 230.

**Also fixed a real fabrication risk in `leads.py`**: four Nara trees
retired the same day they were published (zero verified sources, see the
prior continuation's brief) were showing up as READY again within the
hour, because their own `why` field IS the retirement note and
`has_source_evidence()` read its mere presence as proof a pass had
looked at the tree. Added a `retired_id` check to `classify()` so a
retired lead short-circuits straight to BLOCKED. Also cleared two stale,
fully-consumed verify-pass leftovers (`famousslovakia-verified.json`,
`famoustaiwan-verified.json`) sitting uncommitted since the prior
continuation.

Build (5023 pages), qa.py (7779 pages) and preflight.py (536 cities, 0
problems) all clean. No FOR HIDDE items.
## 2026-09-08 (continuation) - Sant'Alfio grows from 1 tree to 3: the two chestnut/birch neighbours that had no home

Continuation of an attempt that stopped after 34 minutes with 86 of its
window unspent. No claims standing, `leads.py --ready` empty. Deleted
two stale, already-consumed research files sitting uncommitted from the
prior attempt: `famousslovakia-verified.json` (all 5 trees confirmed
live under bosaca/senica/stary-smokovec/velke-borove) and
`famoustaiwan-verified.json` (an empty array, its one candidate already
shipped as bilu.json weeks ago).

Then `city_queue.py --next` and `scout_next.py --target` for new
coverage; Taormina's own register supply is exhausted (all five in-town
trees blocked on the Excelsior Palace's private grounds, per
`data/leads/taormina.json`). But `data/leads/santalfio-etna.json` held
two more fully-verified trees, from the same 2026-08-30 pass that had
already shipped the Hundred-Horse Chestnut alone under the single-tree
exception, explicitly left for later ("A Sant'Alfio page of its own
once four trees clear the bar on that slope; these three are already
three of them"). Wrote their stories and added them to santalfio.json:

- **sal_002, The Ship's Chestnut** (Castagno della Nave): ~1,800 years
  by one source, a second only confirms "over a thousand"; 500m uphill
  from the Hundred-Horse Chestnut. Stands on private land but at the
  path's edge, described by the source as clearly visible without
  entering the property, the view-only-tree allowance. Flagged for the
  age and the access read.
- **sal_003, The Etna Birch of Magazzeni** (Betula aetnensis): a
  glacial-relict endemic growing at 1010m, well below its usual
  1450-2000m band. No age source exists, so the field stays empty and
  the story asks the reader rather than guess. Girth (205cm) and
  height (12m) corroborated across the national and a regional
  register. Flagged: no source confirms a marked path to this specific
  tree, though it stands in open forest with no gate.

Both carry a `how_to_recognise` line (bark colour/base shape are
restatements of verify_notes, not new claims). Rewrote the city intro
to reflect three trees instead of one, kept within the 60-100 word
Contract C range. Still below the 4-tree floor at 3, which is fine:
the page already shipped under the single-tree exception and growing
it with genuinely verified neighbours is normal work, not padding.

Build (5023 pages), qa.py (7779 pages) and preflight.py (536 cities,
0 problems) all clean. No FOR HIDDE items.
## 2026-09-08 - Finished the standing _famous-slovakia and _famous-taiwan claims; a stranded Poland write also merged

Continuation of an earlier attempt that stopped after 10 min with 110 of
its window unspent. `passcheck.py --claims` showed two standing,
`_famous-taiwan` and `_famous-slovakia`, both verify, with uncommitted
output already on disk. `famoustaiwan-verified.json` was an empty array:
that pass's one candidate, the Bilu Sacred Tree, had already shipped as
bilu.json in an earlier commit, so the claim was pure orientation cost.
Released it. `famousslovakia-verified.json` held 5 fully verified trees
with no story; `passcheck.py --pending` also surfaced a fully-written but
unmerged `famouspoland-verified.json` (3 trees) from an even earlier
session.

**5 new single-tree/small-cluster Slovak places, all under the
2026-08-31 single-tree-destination exception (national Strom roka
contest wins standing in for global fame, per the Amt Neuhaus
precedent):**
- **Bošáca** (new, bsa_001/bsa_002): two national Tree of the Year
  fruit trees 350m apart in the Zabudišová hillside hamlet, an heirloom
  apple (2017 winner, 6th in Europe) and a rare pink-fleshed pear (2015
  winner, 3rd in Europe). Reassigned from the verify pass's `bsc_001`/
  `bsc_002` ids, which collided with live Bucaco (Portugal) trees;
  `passcheck.py --pending` caught it before merge.
- **Veľké Borové** (new, vbo_001): Slovakia's first-ever Tree of the
  Year (2004), a Scots pine estimated 250-350 years old. Flagged: no
  dated sighting since a geocache route to it was archived in 2014, so
  the page says plainly that its current status is unconfirmed rather
  than assume the best.
- **Starý Smokovec** (new, sms_001): the Smokovec Beech, "Tree of
  Lovers," a weeping beech (~80 years) in the centre of the High Tatras'
  main resort town, 2021 Tree of the Year.
- **Senica** (new, sen_001): the White Mulberry of Senica, ~210 years,
  the town's own Tree of the City (2010) and national Tree of the Year
  (2014), 8th of 14 in the 2015 European final.

**Brzoza, Poland (new, brp_001/002/003):** an oak and two limes standing
within 15m of each other in state forest north of Toruń, all made nature
monuments in one 2014 council resolution. Renumbered from the verify
pass's placeholder `xxx_003/004/005` ids. None of the three carries a
documented age; two of three rest on a single source and are flagged.
Ships below the 4-tree floor as a genuine below-floor cluster rather than
one tree, per the exception's "local documentation, not global fame"
standard.

`city_names.py` run for the 4 new Slovak places (Brzoza's own name is a
common Polish toponym and could not be resolved to one Wikipedia article;
left unresolved rather than guessed). Build (5021 pages), qa.py (7777
pages, 0 problems) and preflight.py (536 cities, 0 problems) all clean.
Deleted 3 stale `data/research/*-verified.json` files whose contents were
already fully merged (bilu, brisbane, famouspoland).

## 2026-09-07 (continuation 9) - Finished the _bomenbieb-netherlands and _famous-germany claims

**Maastricht +1 (maa_015), Deventer +1 (dev_010), Tilburg +1 (til_016).**
Three bomenbieb.nl leads (Meerssen tulip tree, Wilp trumpet tree,
Oisterwijk's Marialinde) were fully verified and written but sat
unmerged; `passcheck.py --brief` placed all three inside an existing
city's radius rather than as new places.

**16 new German single-tree places from `_famous-germany`.** hmb_001
(Himmelsberg, a lime trained into a dance floor, on a 2001 postage
stamp) and lnd_001 (Linderhof, spared by Ludwig II for the terrace
gardens) were already fully verified with no story. The remaining 26
leads on that file (all `status: lead`) went to a `verify` pass: 14
shipped as new single-tree places (bargischow, horn-bremen, eichigt,
niedenstein, neuenrade, peesten, frankenthal-sachsen, polchow,
schlettau, wilparting, baldenhain, limmersdorf, neudrossenfeld,
ottendorf-gaedheim), 10 held as real-but-ordinary Dorflinden/
Gerichtslinden, 2 blocked as dead (Kandelaberlinde Dorla, felled 2023;
Winterlinde am Friedhof Eschelbronn, felled 2019, caught from a stray
`tmp_eschelbronn.txt` an earlier attempt had fetched and never
processed). Every one of the file's 53 leads now carries a status;
none are left as a bare `lead`.

## 2026-09-07 (continuation 7) - Leiden 18 to 20: two Hortus trees a prior write pass left unmerged

`leiden-lrmb-written.json` carried 8 written trees; the prior continuation
merged 6 (12 to 18) and left lei_012 (Fern-leaved Beech of the Nut Field)
and lei_013 (Grafted Ash of the Hortus) on disk. Both were fully verified
and written, needed only merging, `paid_entry: true` (missing, caught by
preflight against their Hortus siblings) and count-line fixes (eighteen to
twenty, eight to ten, English and Dutch). Leiden: 18 to 20 trees, both new
ones paid Hortus entries (paid-entry share unchanged at 50%). Deleted both
now-empty research files. Build, qa.py and preflight clean.

## 2026-09-07 (continuation 6) - Leiden 12 to 18: 6 free trees from the Dutch LRMB register

Same window as the Berlin and Milan passes below, after both came back
thin. Checked `city_queue.py --next`'s stage-2 deepening list for a
better-quality register than Berlin's (no age field) or Milan's
(near-centre supply exhausted): Leiden's Dutch LRMB register carries a
planted-decade band directly on every entry and had 399 unmined
candidates within 20km. Dispatched a verify pass, deliberately steered
toward free public trees since Leiden already sat at a high paid-entry
share (8 of 12, 67%).

**6 trees shipped, all free**: two London Planes and a weeping willow
clustered around the Van der Werff statue in Van der Werfpark, a
Caucasian wingnut in the Plantsoen that won a public "X-factor" tree
election in 2009 (160 votes to a copper beech's 83), a 3-tree Persian
Ironwood ensemble in the same park that turns out to be the actual type
planting for the cultivar Parrotia persica 'Het Plantsoen', now sold by
nurseries across Europe, and an elm inside the 11th-century Burcht
mound, one of the country's surviving monumental elms amid the ongoing
Dutch elm disease die-off. 2 blocked (a beech at a private townhouse, a
9-tree maple grove that fails the single-collectible-point test), 4 left
as leads. Wrote all 6 stories directly (single-city batch, judged too
small for a cross-city write pass) and their Dutch overlay translation,
since Leiden ships an nl page and the build refuses a translated city
missing trees the English page holds.

**One pin upgraded**: lei_005 (the Beets Beech of the Burcht) moved from
approximate to confirmed using the LRMB register's own tree-level
coordinate for the same tree, matched by name and place. Fixed five
stale "twelve trees" count promises across both languages (title, meta
description, intro, question page, FAQ) and trimmed both intros back
into Contract C's 60-100 word range after a first draft ran long.
Leiden: 18 trees, paid-entry share down from 67% to 44%. Build, QA,
preflight and superlatives all clean. Claim released.

## 2026-09-07 (continuation 5b) - Milan verify pass repeated: still 0, duplicated continuation 3's own finding

After Berlin's low yield, dispatched a Milan verify pass on the strength
of `city_queue.py --next` showing 25 register candidates and real room
to target (22 of 30). It came back with 0 trees, independently
re-confirming near-centre supply is exhausted: 17 already published, 3
already blocked, 3 already tracked as leads. Only afterwards did a check
of this file surface **continuation 3, earlier the same day, already
found and logged the identical result** ("Milan's near-centre register
supply is genuinely exhausted"). This is exactly the waste
`grep -ri "<place>" CURATION.md archive/` exists to prevent and this pass
skipped that check before dispatching. ~171k tokens for a
re-confirmation, partially offset by one real new attempt (RAMI lookup
on the Villa Litta ambiguity, still unresolved, documented in
`data/leads/milan.json` for whoever tries next with a browser session).
Claim released, logged.

## 2026-09-07 (continuation 5) - Berlin verify pass: 561 register candidates, 1 shipped (ber_020)

Continued a window a still earlier attempt had stopped after 15 minutes
having shipped 0 trees, with 105 of 120 minutes unspent.
`passcheck.py --claims` showed a standing Berlin verify claim (589
Naturdenkmal register candidates within 20km, 561 unmined, plus 284
Wikidata candidates). Dispatched a verify pass to finish it rather than
re-claim or abandon it.

Yield was low and the reason is a genuine register gap, not an unworked
city: `berlin-naturdenkmale.json` carries no age or girth field at all,
and for nearly every unmined candidate the only apparent "second source"
was de.wikipedia's district Naturdenkmal list, which traces to the same
government ordinance as the register itself (confirmed by exact
coordinate matching), so per this project's own established precedent it
does not count as independent. monumentaltrees.com, which resolved most
of Berlin's earlier leads, 403'd throughout with no usable Wayback
snapshots.

**1 tree shipped: ber_020, the Podbielski Oak**, the only tree standing
anywhere on the Olympiastadion's 810x320m grounds, named in 1914 for
Prussian cavalry general Victor von Podbielski. Two independent sources
disagree on its history: de.wikipedia implies continuity from a
~200-year-old original, golocal.de says the 1913 original was felled with
the old Deutsches Stadion and a replacement planted in 1936 (~90 years).
Delivered flagged, both readings stated rather than a winner picked, per
the Dicke Marie precedent already on this city's own page. Species also
carries an unresolved minor conflict (register says Quercus petraea, a
Commons photo filename suggests Quercus robur), noted but not resolved.
Wrote the story myself (1 tree, below the threshold for a write-stories
batch) and its German overlay translation (`data/i18n/de/berlin.json`,
title count 19 to 20 Naturdenkmäler). Berlin now 20 trees, 12 with photos.

7 clusters recorded as new open leads in `data/leads/berlin.json`
(Johannaplatz yews, Wallotstrasse/Königsallee beeches, a 13-tree Tiergarten
exotic cluster, a TU Berlin arboretum, a Dahlem churchyard lime, Grunewald
forest oaks, Heinrich-von-Kleist-Park), none confirmed dead ends, each
missing either an independent source or an access confirmation. Claim
released. Build, QA and preflight all clean.

## 2026-09-07 (continuation 4) - Prague write pass merged (+3); Nara reader sightings closed out (+4), 11 submissions answered

Resumed a window a still earlier attempt had stopped after 57 minutes
having shipped 5 trees elsewhere, with 63 of 120 minutes unspent.
`passcheck.py --claims` showed a standing Prague verify claim with real
output on disk (`data/research/prague-verified.json`, 3 trees fully
verified, no story yet). Dispatched a write-stories pass on those 3
(prg_019 Hungarian Oak of Italska Street, prg_020 Oak of U Malvazinky,
prg_021 Plane of Jezerka Park), merged into `data/cities/prague.json`
(18 to 21), fixed 3 stale count promises in the page copy (eighteen to
twenty-one, sixteen more to twenty more, four planes to six), and one in
`data/countries/czech-republic.json` (49 to 52 trees). Claim released.

**11 unprocessed reader submissions were sitting in Supabase, all from
this morning, all Hidde walking Nara with the app's "add a tree" camera
flow.** A still-earlier continuation (see below) had already fetched and
matched the 8 that carried photographs via `sightings_inbox.py`, filing
them to `data/leads/_sightings.json`, but had dispatched a background
research agent to identify them that never delivered: the session that
started it ended first, the same Nara-loss pattern as 2026-08-03. Nothing
had reached `data/research/`.

Looked at all 8 photographs directly. Two ("I'm not sure which one it
is") turned out to be the same Roben-sugi already published as nra_010,
photographed seconds apart from the shot already approved as its page
photo, not a new tree. The remaining 4 distinct trees (one cedar beside a
small shrine near Nigatsu-do, a leaning cedar by the approach road, a
broad tree by a park pond and pavilion, and a large ginkgo beside a
temple wall in Suimon-cho, the last shot three times) went to a fresh
verify pass with the photos, GPS and visual descriptions as the brief.

**None of the four cleared the two-independent-source bar**: web and
Japanese-language searches (municipal giant-tree lists, temple pages,
OSM/Overpass reverse geocoding) found no named, individually documented
tree at any of the four spots, only the photograph itself as evidence.
Per Step 2 ("if sources conflict or only one source exists, include the
tree but flag it"), published all four rather than leaving them in
research limbo: nra_011 through nra_014, all `curation_status: flagged`,
`location_precision: approximate`, no invented age, girth or name beyond
a descriptive one, species left honestly uncertain on nra_013 and access
phrased as view-only on nra_014 (temple ownership of the wall unclear).
Each story ends by inviting the reader to name the exact spot. A
title-length build break on nra_014's first-draft name (65 chars) was
caught by the build and fixed before merging (renamed to fit under 60).
Nara's meta_description count promise fixed (nine more to thirteen).

Closed the loop on all 11 submissions via the service key: outcome set
on each (`changed` for the 4 new trees and the first of the 3 ginkgo
duplicates, `holds` with a composed reply for the 2 Roben-sugi
duplicates and the other 2 ginkgo duplicates, `open_question` for one
sighting whose photo never uploaded, `holds` for a worth-it vote on
nra_005 and its undo). Custom replies checked clean against
`mailcheck.py` before writing them to the rows; `contributor_reply.py`'s
own scheduled run sends them. All 11 row ids appended to
`data/submissions-processed.json`. `data/leads/_sightings.json` updated
to `published`/`duplicate` with the resulting tree ids so a future pass
does not re-litigate them.

Build (4897 pages), qa.py, preflight.py (0 problems) and superlatives.py
(702 claims, no collisions) all clean. `city_queue.py` rerun to keep
`CITY_QUEUE.md`/`city-list.json` current. Nothing FOR HIDDE.

## 2026-09-07 (continuation 3) - Milan verify pass: 0 new (supply fully mined); Nara reader sightings processed, one photo held, deeper research dispatched

Resumed a window a still earlier, unlogged attempt had stopped after 48
minutes with 5 trees already shipped elsewhere and 72 of 120 minutes
unspent. `passcheck.py --claims` showed two standing claims from that
attempt, both verify passes claimed but never delivered: milan (empty
delivery file) and prague (delivery file present but empty, `[]`).
`leads.py --ready` had only the 1 Voorburg elm already known to be below
the no-pass-under-six floor. Dispatched verify agents on both claimed
cities per their passcheck briefs.

**Milan: 0 new trees, and it is a real answer, not a stall.** All 14
register candidates within reach of the walk were cross-matched against
the live city file, the leads file and the blocked list: every one
already published, already blocked (Villa Belgiojoso's children-only
garden), or the one known single-source lead (a 625cm Montanelli plane).
A fresh attempt to find a second source for that plane via RAMI
(ilregistrodeglialberi.it) traced the record's own AMI code back to a
*different*, already-published Milan plane, so it stays a lead. Milan's
near-centre register supply is genuinely exhausted; logged to
`data/agent-costs.json`, claim released.

**Reader sightings: Hidde walked Nara this morning and used the app's
own "add a tree" flow repeatedly.** `sightings_inbox.py` picked up 1
photo queued against an existing tree (a second photo of nra_010, the
Roben-sugi) and 6 fresh leads with no match in `data/cities`.
Downloaded every photo from the private bucket and looked at the pixels
before deciding anything, per the Cadiz standard:

- The second nra_010 photo shows a much thicker, deeply furrowed,
  steel-propped trunk than a photo of a ~60-year-old 1967 replacement
  tree would suggest, and it cannot be confirmed as the same specimen
  as the currently-approved photo without more evidence. Held rather
  than swapped in (`sightings_publish.py`, verdict recorded).
- Visual triage of the remaining leads found at least 3-4 genuinely
  distinct large trees Hidde photographed nowhere near each other
  (a large cedar by a small shrine ~99m from nra_010, another leaning
  cedar by a gravel road, and what looks like a row of large trees
  along a temple precinct wall near central Nara/Kofuku-ji), plus one
  distant meadow view too far to read. None are register candidates,
  so a normal verify pass cannot place them: dispatched a research
  agent with the photos and my visual notes to identify and verify
  what it can, deliver to
  `data/research/nara-sightings-verified.json`. Result not in yet.

Nothing committed to a city file yet; this entry covers the processing
so far. See the next entry(ies) for what the Prague and Nara passes
returned. Nothing FOR HIDDE.

## 2026-09-07 (continuation 2) - Merged a stranded write pass: Deventer +1, The Hague +1, Kasukabe and Aguas de Moura new (single-famous-tree), plus 2 photo approvals

A prior attempt in this same window had already claimed and finished a
write-stories pass on 5 targets (`the-hague`, `deventer`, `rumskulla`,
`kasukabe`, `aguas-de-moura`), and a photo-judge viewing pass on 18
photo-less cities, but stopped after 24 minutes without committing
either. `passcheck.py --claims` showed the 5 claims still standing
(133 min left); `git status` showed the actual finished output sitting
uncommitted: 2 new single-tree city files, 2 existing cities each +1
tree, and 2 approved photographs already vendored into
`data/cities/*.json`. Verified each city file (word counts, sources,
`location_precision`) before trusting it, ran `preflight.py` (0
problems) and a full `astro build` + `qa.py` (had to rebuild once,
because `vendor_photos.py` had written the two new photo files into
`site/public/photos` mid-build and the first build had already copied
`public/` before they landed; second build picked them up, QA passed
clean at 7488 pages).

- **Deventer +1** (dev_009): The White Willow of Wilp, from the
  Bomenbieb Netherlands register.
- **The Hague +1** (hag_033): The Wych Elm of Park Middenburg, same
  register.
- **Kasukabe, Japan** (new, ksk_001, single-famous-tree exception):
  Ushijima no Fuji, the Great Wisteria of Ushijima, Japan's only
  wisteria at Special National Natural Monument rank, roughly 1,200
  years old. The garden built around it opens only mid-April to
  early May.
- **Aguas de Moura, Portugal** (new, agm_001, single-famous-tree
  exception): the Whistler Cork Oak (Sobreiro Assobiador).
- **Rumskulla, Sweden** (new, rkm_001, single-famous-tree exception):
  Rumskullaeken, the Kvill Oak.
- Photo-judge viewing pass approved 2 of 47 candidates viewed as pixels:
  the Molkenkur linden in Heidelberg (hei_001, CC BY-SA 4.0) and the
  Olive of San Martin de Porres in Lima (lim_002, CC BY-SA 4.0, the
  city's longest-lived tree, previously photo-less).

Released all 5 claims after merging. `city_queue.py` re-run to fold the
two new cities into CITY_QUEUE.md and city-list.json (now 247 entries).
Nothing flagged for Hidde.

## 2026-09-07 (continuation) - Finished 4 stranded write-story passes: Pelham, Itoshiro, Yangpyeong ship; Osaka +1

An earlier attempt this window stopped after 14 minutes having shipped
nothing, with 106 of 120 minutes unspent. Checking claims and READY leads
(both empty of new work) turned up something more valuable sitting
uncommitted on disk from an even earlier, unrelated attempt: four fully
verified AND fully written trees (`data/research/comfort-maple-verified.json`,
`ginkgo-of-yongmunsa-temple-verified.json`, `itoshiro-no-osugi-verified.json`,
`myokokuji-no-sotetsu-verified.json`) that a write-stories pass had already
finished, never merged, never committed.

- **Pelham, Ontario, Canada** (new, pel_001): the Comfort Maple, widely
  reckoned Canada's oldest sugar maple and possibly Ontario's oldest tree
  of any species, with an entire conservation area built around it.
  Photo found and viewed against the Cadiz standard (full tree, autumn
  colour, well exposed, CC BY-SA 2.0, Flickr via Commons) and approved.
- **Itoshiro, Gifu, Japan** (new, ita_001): the Itoshiro Osugi, a
  ~1,800-year cedar and the only Special National Natural Monument tree
  in the prefecture, reached by 420 purpose-built steps. Photo viewed and
  approved (whole tree, daylight, the trailhead sign visibly confirms the
  age/girth figures used in the story).
- **Yangpyeong, South Korea** (new, ymp_001): the Ginkgo of Yongmunsa
  Temple, reckoned Korea's tallest ginkgo, Natural Monument No. 30. Photo
  viewed and approved (full crown in autumn gold, matching the best_time
  label exactly; KOGL Type 1, already precedented via Seoul's photos).
- **Osaka +6th tree** (osa_006): Myokoku-ji's cycad colony ("the Homesick
  Cycad") in neighbouring Sakai, 20-25 minutes by Nankai train from
  Namba, inside the day-trip boundary. Two photo candidates were viewed
  and both rejected (one a black-and-white archival print with a person
  in it, one a satellite/aerial map, neither a photograph of the plant
  itself), so it ships `photo.status: missing`. Updated Osaka's intro
  (which had also drifted stale: it said "three of the four" trees were
  camphors against an actual five, now corrected to "four of the six"),
  one FAQ answer, and the Japanese translation overlay (new osa_006
  entry, intro/FAQ text updated to match, trimmed to the 250-character
  Contract C limit for Japanese).

**famouspoland-verified.json (the Brzoza trio, xxx_003-005) got stories
too, but stays HELD.** Below the 4-tree floor with no evidence of the
wider fame the single-tree exception requires (a municipal legal
designation and a forest-district webpage, not a tourist destination).
Kept as finished research, not thrown away, for whenever a container
opens.

**Continued the standing `_bomenbieb-netherlands` verify claim** (a
`night-run` claim from a "shelf refill, next batch" pass, 146 minutes
left when picked up): the earlier attempt's followup file had only
gotten through 1 of its assigned 18. Before dispatching more research,
cross-checked all 17 remaining against the CURRENT full corpus by actual
coordinates rather than trusting the batch's own stale `nearest_ours`
field, and caught 2 that had already shipped under different names from
this same lead pile the day before (`zwarte els paleis loo` = apd_010,
`kasteellinden nijenrode` = bkl_001, both exact 0m coordinate matches),
now marked `duplicate` with the reason on record so nobody re-researches
them. Dispatched a verify agent on the remaining 15 (Voorburg, Amsterdam,
two in Wilp, Meerssen, Houten, Grubbenvorst, Oisterwijk, Achterberg, De
Steeg, Zutphen, Midlaren, Tull en 't Waal, Slochteren, Putten); result
not yet in as this entry is written.

Build (4878 pages), qa.py and superlatives.py (697 claims, no crown
collisions) all clean. Pushed as `ab570643`.

## 2026-09-07 - Finished the standing _famous-france and _famous-poland verify claims: 5 trees, 3 new single-tree places plus one into Ghisonaccia

Resumed into a window an earlier attempt had stopped 12 minutes in with 108
of 120 minutes unspent. `passcheck.py --claims` showed two standing verify
claims (`_famous-france`, `_famous-poland`, both by night-run) with real
uncommitted output on disk: `data/research/famousfrance-verified.json` (4
trees) and `famouspoland-verified.json` (5 trees), fully verified with
sources and coordinates but no stories, so `leads.py --ready` correctly
showed 0.

Filtered to what should actually become a page before dispatching a
write-stories pass, since two of the nine did not clear the bar: **the
Fontenay Abbey plane tree**, whose own verify_notes recommend against a
standalone page (a garden feature of an already-famous UNESCO abbey,
people travel for the abbey rather than the tree), and **the Brzoza
trio** (an oak and two limes near Torun, legally designated together but
with no evidence of the wider fame the 2026-08-31 single-tree exception
requires, only a municipal resolution and a forest-district webpage).
Both are kept as fully-verified research rather than discarded: Fontenay
back in `famousfrance-verified.json`, the Brzoza three in
`famouspoland-verified.json`, for whenever a container opens (a Marmagne
page with other trees; a Torun page; further evidence of fame).

The other five got stories from a write-stories pass and were assembled
into containers by hand:

- **U Listincu** joined the existing Ghisonaccia page as arb_002. Its own
  story already alluded to it ("the person who had already had
  Ghisonaccia's other old tree, a mastic reckoned at a thousand years,
  officially recognised"), so this closes a reference the page had been
  carrying unfulfilled. Ghisonaccia is now 2 trees; oldest_tree_id moved
  to arb_002 (700-1000 years vs arb_001's 200-250), intro/meta/question
  page/FAQ all rewritten for two trees.
- **Chene de Venon** (vno_001), a new single-tree place near Grenoble: a
  solitary "vegetation lighthouse" oak visible across the whole valley,
  French Arbre remarquable since 2017, ~100 people at its recognition
  ceremony. Genus left unresolved (Quercus sp.), publish-and-ask.
- **The Saman of Habitation Ceron** (lpr_001), a new place, Le Precheur,
  Martinique: the park's headline attraction, survived the 1902 Pelee
  eruption. Used the real commune name rather than the whole island,
  matching the Venon/Rogalin/Sant'Alfio precedent of precise village-level
  containers rather than a broad island page built for one tree. Country
  set to France (Martinique is an overseas department), matching how
  Corsica is treated. Its pin sits 6499km from the nearest other French
  tree, which is real geography (island vs mainland/Corsica), not a data
  error; added `lpr_001` to preflight's `CHECKED_BY_HAND` set alongside
  the existing Pirangi do Norte precedent.
- **Lech's Oak and Rus's Oak** (rog_001, rog_002), a new place, Rogalin,
  Poland: two of a legendary named trio (Lech, Czech, Rus) beside Rogalin
  Palace; Rus is dendrochronologically dated to 800-850 years (Institute
  of Dendrology, Kornik, 2019), the oldest dated oak in Poland, Lech has
  no dated age and the story says so plainly. The dead third oak, Czech,
  appears only as context, never as its own entry, per the never-dead-tree
  rule. Two distinct trees, two entries, not folded into one (unlike
  Breukelen's indistinguishable lime pair), since each has its own
  well-sourced, independent story.

All four leads files updated with `status: published` and the tree id, so
a future dedupe check reads them as done rather than re-litigating them
(confirmed via `preflight.py`'s own "may already be published" NOTE, which
now correctly flags all four against the new entries). Regenerated
city-list.json/CITY_QUEUE.md, full Astro build (7435 pages), qa.py clean,
preflight.py clean (0 problems after the CHECKED_BY_HAND fix),
superlatives.py clean (694 claims, no collisions). Released both claims.

Also checked rung 2 (site broken): the site itself is fully green (smoke,
deploy, digest, review). The iOS app gate is red, on its fourth
consecutive failed fix attempt for `testTappingAPinOpensItsTree` across
several hours of CI time by (presumably) other continuations; did not
duplicate that effort. REVIEW.md's two 2026-09-06 WARNs (business-rule
phrasing in three FAQ answers, a contradiction in Contribute.swift) were
both already fixed by an earlier pass; verified rather than re-fixed.

`passcheck.py --pending` also surfaced 7 other already-verified
single-tree files still needing only a story (Comfort Maple, Yongmunsa
ginkgo, Itoshiro no Osugi, Myokoku-ji sotetsu, Rumskullaeken, Ushijima no
Fuji, Whistler Cork Oak): bought and paid for, worth a write pass next.

## 2026-09-06 (continuation 18) - bomenbieb-netherlands verify claim finished: 5 trees, 4 new single-tree places, 1 into Apeldoorn

Apeldoorn +1 (apd_010, Black Alder of the Sculpture Garden, single-sourced
and flagged, paid entry inside Paleis Het Loo). Four new single-tree
places under the 2026-08-31 exception: Altrier/Luxembourg (alt_001, the
Oak of Hersberg, Luxembourg's thickest tree; age genuinely disputed,
roughly 300 vs roughly 500 years, and the "thousand-year" folk name is
unsupported by any source found; a 2024 visit found the crown declined
to about a third still bearing leaves, alive but worth a recheck),
Breukelen (bkl_001, the Limes of Kasteel Nijenrode, a view-only pair on
a private castle forecourt, pin on the public viewing point per the
Hobart rule, approximate), Laren, Gelderland (lar_001, the Dikke Boom of
Verwolde, the Netherlands' biggest pedunculate oak, root dieback from
adjacent maize-field fertiliser addressed by a 2005 restoration
programme, not a current concern), Amerongen (amg_001, the Adoption Oak,
Bomenstichting-adopted 1987, paid garden ticket separate from the
castle museum).

Two independent verify efforts had worked the same three places
(Altrier, Breukelen, Laren) the same day; the standalone lead files
(`data/leads/altrier.json`, `breukelen.json`, `laren-gelderland.json`)
were more carefully sourced than the claimed research file for those
three, so their figures won where they disagreed (age bands, the
Nijenrode limes' species, and dropping Verwolde's unconfirmed 25m
height). All three lead files marked `published` with tree ids.
0 photos found (verify-only leads, no photo hunt run this pass); all 5
ship with `photo.status: missing`. Build (4856 pages) and preflight
clean. Full detail in LOG.md continuation 18.

## 2026-09-06 (continuation 17) - Caught a near-duplicate before it shipped; Leiden's Golden Chain gets a confirmed pin instead

Continuation 15 had released the `_bomenbieb-netherlands` verify claim
with one tree left uncommitted: lei_019 "The Golden Rain of the Hortus
Entrance", checked only against its nearest published neighbour by
distance (lei_001, the Tulip Tree, 50m away, wrong species) and staged
as a new tree. It was never checked against lei_004 The Golden Chain of
the Hortus: same species (Laburnum anagyroides), same bomenbieb source,
same debunked-1601/1720s-Boerhaave story, 46m from lei_004's own
(approximate) pin. Same tree. Worth naming as a pattern: a verify pass's
"nearest published tree" check is a distance search, not a duplicate
check, and it can clear a candidate against the wrong neighbour while
the real duplicate sits a few trees further down the same city file.

Folded lei_019's more precise coordinate and its Wayback-archived
hortusleiden.nl source into lei_004 instead: upgraded its pin from
approximate to confirmed and added the 1601-garden-inventory detail (the
Hortus's own records place a laburnum here that year, but not where this
one stands) to the story. Marked the lead a duplicate with the full
reasoning in `data/leads/_bomenbieb-netherlands.json`, released the
stale verify claim and removed the now-empty `bomenbiebnetherlands-` and
`famousczech2-verified.json` research files (everything else in both was
already merged in continuation 14). Leiden stays at 12 trees. Build
(4839 pages), qa.py and preflight.py all clean.

## 2026-09-06 (continuation 14) - 11 trees written and merged: 4 into Deventer/Arnhem/Leeuwarden/Den Bosch, 7 new Czech single-tree places

Finished the two verify passes continuation 13 had left running
(`_bomenbieb-netherlands`, `_famous-czech-republic`). Dutch: the
Steenenkamer Maple (Deventer, dev_008), the Robinia of Kasteel Doorwerth
(Arnhem, arn_038, a disputed 1678/1601/1579 planting date, oldest black
locust in NL by local tradition), the White Horse Chestnut of Poptaslot
(Leeuwarden, lee_009), the Annenborch Lime (Den Bosch, dbo_012, new
oldest tree for that city at ~250y). Czech, each its own single-tree
place under rule 1(0c): Frydlant, Cinovec (a 2007 successor to a
lightning-killed original, written honestly as such), Prosec pod
Jestedem, Lazy (half-fallen, both halves protected), Mcely, Jihlava
(disputed age, 132 vs 211 years), Lukavice. 0 flagged as unverifiable
beyond the honest disputes/gaps named above; 0 photos found (verify-only
scope), all 11 ship with `photo.status: missing`. Both leads files marked
published with tree ids; two country-page stale counts fixed (Czech
Republic, Netherlands). Full detail in LOG.md.

## 2026-09-06 (continuation 11) - 8 new Slovak single-tree/small-cluster places published, Arnhem Dutch overlay finished

Hronsek (hrs_001, memorial lindens by a UNESCO wooden church, count
disputed 3/4/6 across sources), Trencianske Stankovce (tst_001, the
two Lipsky lindens, age disputed 250 vs 500 years), Lipany (lip_001,
town-square linden, Tree of the Year 2011), Drnava (drz_001, Tree of
the Year 2020, in the village chronicle since 1670), Dubinne
(dbi_001, likely Slovakia's oldest oak, undatable hollow trunk, Tree
of the Year 2010), Uzovska Panica (uzp_001, service tree, Tree of the
Year 2019), Casta (cst_001, Slovakia's largest sweet chestnut) and
Zilina (zil_001/002/003, a Tree-of-the-Year plane plus two disputed
street trees, Slovakia's 4th-largest city, previously unpublished).
All ship under the 2026-08-31 single-famous-tree exception. 0 flagged
as unverifiable beyond the honest disputes named above, 0 photos
found (verify-only scope); all 10 trees ship with `photo.status:
missing`. Full detail in LOG.md.

Also completed the Dutch translation overlay for Arnhem (37/37 trees
now rendered), started in an earlier continuation today.

Redid the photo-8-cities viewing pass that continuation 10 dispatched
and then lost (session closed before it finished; see LOG.md). 58
candidates fetched and viewed as pixels; 5 approved: The Japanese
Pagoda Tree of Alsterufer (Hamburg), the Grinava Poplar (Bratislava),
the Beech of Bastion Beck and the Prince Jean Chestnut (Luxembourg
City), the Ginkgo of Muinkpark (Ghent). 51 rejected, mostly wrong
subject entirely: three Maastricht Stolpersteine matched on a shared
surname, several Hamburg and Groningen building facades matched on a
street address, two Wilhelmina statues (one in the wrong city
outright), four Ghent register photos of the wrong species. 2 held
for licence/geotag risk. Groningen, Maastricht, Eindhoven and
Brighton keep an honest photo gap; their candidates genuinely did not
clear the bar.

## 2026-09-06 (continuation 8) - Hiroshima +2, Sulechow +1, three new Polish single-tree places; the germany leads-file staleness bug caught again

Hiroshima: hir_016 (Fukuoji Lantern Cedars, hillside temple, three
survivors of five planted in 1391) and hir_017 (Chichisagari Ginkgo,
Nukui Hachiman Shrine, ~1,200-1,600 years per its 1979 designation,
now the city's oldest documented tree). Sulechow: sul_002 Sosna
Rzepicha (Poland's current thickest pine under updated rules, no
published age, 10.5km off-trail from sul_001). Three new single-tree
places under the 2026-08-31 exception: Przybudki (Dab Dunin),
Cieletniki (the Cieletniki Linden), Wisniowa (Dab Jozef). Full detail
in LOG.md. 0 flagged as unverifiable, 0 photos found (none hunted,
per BRIEF_RESEARCH.md's verify-only scope); all 4 new trees ship with
`photo.status: missing`, an honest gap for a later viewing pass or a
reader.

**Worth fixing structurally, seen twice now: a leads file's `status`
field does not get updated when a tree ships if the merge happens in
a different session than the verify pass.** Checking `_famous-germany`
for a possible verify batch this window, its top demand-ranked
candidate (Tassilolinde, Wessobrunn, 306 views/mo) turned out to
already be published as `wes_001`, weeks ago, with the leads file
still reading `"status": "lead"`. This is the identical bug the
2026-09-05 UK pass flagged after nearly re-shipping the Ankerwycke and
Llangernyw Yews (LOG.md that day: "the underlying fix worth doing
later is cross-checking a verify brief against the leads file's own
status field rather than trusting it wasn't touched"). It has not
been fixed since. Skipped Germany entirely this window rather than
risk a duplicate; a future session should either patch every leads
file against `data/cities` by coordinate once, or add that
cross-check to `passcheck.py --brief` itself so it happens on every
brief instead of by memory.

Picked up where an earlier attempt in this window stopped after 74 minutes
with 46 unspent. Rung 1 (submissions, sightings inbox) was clear. Rung 2:
health.py flagged the Data digest workflow as failed; `gh run view
--log-failed` showed a plain git push race (commit succeeded, a concurrent
push to main won, the retry loop in data-digest.yml has no `git pull
--rebase` before its own push) rather than a code defect, and this is
already logged FOR HIDDE (LOG.md, needs `workflows` scope this environment
does not have). `leads.py --ready` had only 1 lead, too thin for a write
batch, so claimed `_famous-united-kingdom` (26 leads, several well-known
yews) for a verify pass instead.

The verify pass returned 3 candidates and 1 correctly blocked (Ormiston
Yew: alive and real, but its own landowner withdrew it from Scotland's
Tree of the Year specifically to reduce visitor footfall on health
grounds, and the Woodland Trust agreed; treated as a hard-rule-10-spirit
case and left blocked). Of the 3, only Borrowdale Yews was genuinely new.
**Ankerwycke Yew turned out to already be published as `ank_001` under
Runnymede** (same coordinates to the metre), caught by
`preflight.py`'s duplicate-pin check before the second copy (written
under a colliding `fuk` id prefix, itself already taken by Fukuoka) was
committed. **Llangernyw Yew was worse: already published as `lgy_001`
under its own page from an earlier run earlier today**, and my Write call
silently overwrote that file with a weaker rewrite (no photo-hunt notes,
missing the 06:09 run's fuller verify_notes) before `git status` showed it
as modified rather than new and the original was restored with `git
checkout HEAD --`. Root cause in both cases: the leads file's own status
field was never updated when those two shipped, so a fresh brief read them
as still-open leads. Fixed `data/leads/_famous-united-kingdom.json` to
mark all three (plus Ormiston) with accurate status and a note, so a
future pass does not repeat either mistake. Worth a real fix later: the
verify-pass brief and famous_map.py's "do we already map this" check
should be cross-referencing the leads file's own status field, not relying
on a run to notice a `git status` surprise.

Borrowdale (Cumbria) shipped as a new single-tree place: the Borrowdale
Yews, Wordsworth's "Fraternal Four", an ensemble of 3 surviving yews (of
an original 4) on National Trust land above Seathwaite, one collectible
point, largest tree dendro-dated to roughly 1,500 years. Flagged (age
dispute, ensemble pin approximate), no photo yet (3 Commons candidates
identified in the leads file, not judged against the Cadiz standard this
pass). id prefix `bwd_001`.

Also wrote the one species-page gap `pagegaps.py` had open, Box Elder (3
trees: Chicago, Eindhoven, Setubal), a small enough job to do directly
rather than dispatch, per the "each intro written from that subject's own
trees" rule.

Build (4658 pages), qa.py (7003 pages), preflight.py (454 cities, 0
problems) and superlatives.py all clean.

## 2026-09-06 (continuation 4) - 5 new German single-tree places; Tilburg +8, Eindhoven +4

Finished four standing claims left by an earlier attempt in this window that
stopped after 11 minutes with 109 unspent (_famous-germany and
_bomenbieb-netherlands verify, plus eindhoven and tilburg verify, plus
amsterdam and lisbon photo).

Aachen: 1 tree (aac_001, The Forster Linde), flagged (age is a carried-forward
1852 estimate), 1 photo approved (CC BY 3.0). New place, single-tree-
destination exception: widely reported as Aachen's oldest tree, own
Wikipedia article, city QR-code trail.

Coppenbrügge: 1 tree (cpb_001, The Peter-Linde), flagged, 1 photo approved
(CC BY-SA 4.0). New place, same exception: grows out of the castle wall,
once trained into a climbable three-storey bower, named for a 1697 visit by
Peter the Great.

Erdmannrode: 1 tree (edm_001, The Gerichtslinde), flagged (girth and age
single-sourced), 1 photo approved (CC BY-SA 4.0, bare winter, no in-leaf
candidate found). New place, same exception: 8.65m girth, once carried a
musicians' platform. Published as edm_001, not erd_001 (that id prefix
already belonged to Nantes).

Galenbeck: 1 tree (gnb_001, The Galenbeck Dance Linden), flagged, 1 photo
approved (CC BY-SA 3.0). New place, same exception: the last surviving
Tanzlinde (dance linden) in Mecklenburg-Vorpommern and, per English
Wikipedia, in all of northern Germany, a real regional superlative.

Schlagsdorf: 1 tree (sgd_001, The Gerichtslinde von Schlagsdorf), flagged
(location approximate, churchyard-level), 0 photos (both Commons candidates
were a grave-marker close-up and an information sign, not the tree). New
place, same exception: documented 1518 ducal court, on the village's own
coat of arms.

Not shipped: Zehdenick's Gerichtslinde (also verified this batch) was left
as a lead. The verify pass's own notes called it a weaker single-tree case
than the five above (no girth, hedged judicial history), and that judgement
was kept rather than overridden on a mechanical "ready" flag.

Tilburg: 8 trees added (til_008-015), now 15. A rare-tree teaching
collection in Zuiderpark (Caucasian wingnut, American yellowwood, pecan,
Transcaucasian birch, golden beech; planted 1950s around the city's old
municipal nursery, evening horticulture/floristry students examined along
the "zweetlaantje"), plus a 3-tree Kloosterpark extension of the existing
Leijpark walk (an oak, a lime and a large-leaved holly on former convent
ground). All flagged (register-only). 0 new photos. 2 candidates blocked:
a beech held "op afspraak" (by appointment) unlike its neighbours, and a
treurbeuk on a school playground with no evidence of genuine public access.

Eindhoven: 4 trees added (ein_008-011), now 11. A new Strijp churchyard
cluster: a copper beech in the Sint Trudo entrance avenue, and in the small
Antonius kerkhof a box elder, a stand of three Nordmann firs, and the oak
at the gate. All flagged (register plus general cemetery-access source
only). 0 new photos (monumentaltrees.com's Trudokerk page, which does carry
girth figures, returned 403).

Also found and fixed while validating: a pre-existing 1.6px CSS
misalignment on every tree page with a credited hero photo (figcaption
padding hardcoded to 1.1rem instead of var(--gutter)), invisible until
Aachen became the alphabetically-first city with one, since the smoke
test's DRIFT check only ever samples that one page. Reproduced on Aarhus's
long-published Wild Service Tree page to confirm it predated this session.
One-line fix, smoke test green after.

Amsterdam and Lisbon's photo claims closed with zero new approvals: 33
Amsterdam candidates and 12 Lisbon candidates were viewed and judged
honestly rather than padded. Worth keeping: the Wilhelminalinde's best
Amsterdam candidate was a good photo of a different Wilhelmina lime at
Nassauplein (caught via the uploader's own Commons categories), and six of
Lisbon's Bela-Sombra candidates turned out to be a tree 7km away in
Restelo (caught via the uploader's own caption). 45 candidates recorded so
nobody re-judges the same dead ends.

## 2026-09-06 (continuation 2) - 3 new single-tree places from the famous-demand list; Beijing +1; a fake tree and a dead tree caught before shipping

Canberra, Australia: 1 tree (can_001, The Lone Pine, Australian War
Memorial), flagged, 0 photos. New place under the single-tree-destination
exception.

Gumeli, Turkey: 1 tree (gum_001, The Gumeli Yew), flagged (disputed age,
1,950-2,000 years vs a popular 4,112 year claim), 0 photos. New place,
genuinely remote (no road, forest hike required).

San Quirico d'Orcia, Italy: 1 tree (sqo_001, The Cypresses of San Quirico
d'Orcia), flagged (no age documented), 0 photos. New place, ensemble
exception (compact, famous for being exactly that, one obvious vantage).

Beijing: 1 tree added (bjs_007, The Guilty Scholar Tree), now 7 trees.
Flagged. Third-generation tree on the historic 1644 site; no lineage
claimed.

Blocked, not shipped: Sprookjesboom (Netherlands) is a wholly artificial
animatronic structure at Efteling, not a living tree. Cedre Gouraud
(Morocco) has been dead since 2003. Arbol de la Noche Triste (Mexico)
resolved as the same site as our own already-published mex_007, whose
story already documents the original as a ruin.

## 2026-09-06 - Brussels bru_031 (Grand Sablon Ailanthus) committed; Higashiomi grows to 3 trees; Tokyo grows to 17

Brussels: 1 tree added (bru_031, The Tree of Heaven of the Grand Sablon),
0 newly flagged beyond the 1 that ships flagged for a single-source-only
reason, 0 new photos (missing, an open-licence hunt found nothing beyond
the register's own page, which is not an image source). English and
French both written.

Higashiomi: 1 tree added (hga_003, The Sennen Bodaiju of Hyakusai-ji),
now 3 trees total, still short of the ordinary 4-tree floor but already
published under no exception check (it shipped in 2026-08 as a
deliberate pair, "not because Higashiomi's research is finished"; a
third genuinely remarkable tree turning up later is normal growth per
CLAUDE.md, not padding). 0 photos on any of its 3 trees. Oldest-tree
claim on the page moved to the new linden; see LOG.md for the reasoning.

Tokyo: 1 tree added (tok_017, The Senbon Ginkgo of Katsushika
Hachimangu), now 17 trees. Flagged (no tree-specific monument
designation, temple-tradition age). 0 photos. Its true place name
(Ichikawa, Chiba) is stated honestly rather than folded into Tokyo
proper, per the day-trip rule.

Continuation of a window an earlier attempt stopped after 12 min with 108
unspent. `passcheck.py --claims` showed two standing: `_famous-poland` and
`_famous-lithuania`, both verify, with uncommitted verify output already on
disk from the earlier attempt: `data/research/famouspoland-batch-verified.json`
held 3 fully judged candidates (fpl_001-003), and `_famous-lithuania.json`
carried bookkeeping fixes (statuses, species) with no new verified trees.
`leads.py --ready` was empty (2691 leads, 0 READY).

**Shipped: Rudy, Poland, a new single-tree place under the 2026-08-31
exception.** Dab Cysters (rud_001), a 500ish-year pedunculate oak in the
former Cistercian abbey's park, girth 7.35m, that survived an arson attack
in October 2022 (confirmed by the Regional Directorate of State Forests in
Katowice; a 2023 tomography assessment found it alive and recovering).
Documented since a 1752 engraving of the abbey. Age kept as a 400-550 year
range since sources disagree (450 vs 500 years, 26m vs 32m height). Photo
approved after viewing the actual pixels (Cadiz standard): a Commons CC BY
4.0 photograph by Marek Mroz, full tree in frame, in leaf, daylight; a
second candidate (bark close-up) rejected on sight. Built the city file by
hand rather than dispatching a write-stories agent, matching the sunk-cost
single-tree pattern used for Amt Neuhaus and Omishima this week. Build
(4612 pages), qa.py (6912 pages, 0 problems), preflight.py (445 cities, 0
problems) and superlatives.py (675 claims, no collisions) all clean.
`city_names.py --city rudy` run (no exonym).

**Held rather than shipped: fpl_002 (Cis Warcislaw) and fpl_003 (Dab
Ksiazecy), both in Szczecin's Park Lesny Zdroje, ~300m apart.** Both fully
verified (girth, register cross-check), but two trees in one park is short
of the 4-tree place floor, and neither is a clear single-tree destination
on its own: the yew is a fine specimen inside a reserve of "several hundred"
yews with no age, and the oak's own identity is unresolved (its geotagged
coordinate sits ~360m from the register's point for a similarly-named
grove, and it may be one tree or one of a dozen-plus). Recorded with full
reasoning as `hold_reason` on both entries in `data/leads/_famous-poland.json`
for a future Szczecin pass to build a real cluster around.

**`_famous-lithuania` closed with nothing new to ship.** The uncommitted
work already on disk was bookkeeping, not new candidates: two duplicate
Priekule leads reconciled to the city's already-published pri_001/pri_002
(status corrected from stale `lead` to `done`), one dead-oak duplicate
confirmed and blocked via its own geotagged photo, and two Silale monuments
(a 13-oak-and-lime freedom memorial, a single 1918 independence oak) held
as leads: both real and sourced, but Silale has only these 2 collectible
points found so far, short of the 4-tree floor, and neither clears the
single-tree-destination bar alone. `silale.lt` added to
`data/fetch-blocklist.json` (Cloudflare-blocked, confirmed twice).

Released both claims. Rung 2 (`health.py`): Data digest still shows
failing; read the log directly (`gh run view 33957091004 --log-failed`),
same benign git-push race documented repeatedly this week (a concurrent
writer won the push, the digest's own commit was lost with the runner).
Nothing new to fix; the next scheduled run picks it up.

## 2026-09-06 - Omishima gains a third camphor (omi_003); Kakumaki held, Okina sugi confirmed dead; hiroshima claim released

Continuation of a window an earlier attempt stopped after 46 min with 74
unspent. `passcheck.py --claims` showed two standing: `hiroshima` (verify)
and `_famous-japan` (verify), both with uncommitted verify output already on
disk. `hiroshima-verified.json` was an empty array for the second attempt
running against the same two register clusters (Hirayama Shrine, Fukujoji
temple); `famousjapan-batch-verified.json` held 3 fully judged candidates
from `famous_demand.py --next`.

**Shipped: omi_003, Ochi-no-Mikoto's Hand-Planted Camphor, joining the
existing Omishima page.** Stands on the sando (approach path) of Oyamazumi
Shrine, distinct from omi_001 (Ikiki no Gomon, the inner-sanctuary camphor)
and omi_002 (the Ito Hirobumi memorial tree). Girth 11.0m, height 15m per
the Chugoku-Shikoku giant-tree survey; the ~2,600-year age is temple-sign
legend tied to a founding figure of the Ochi clan, kept broad and flagged
rather than treated as measured. Rewrote the city intro and one FAQ entry to
cover three trees instead of two; `oldest_tree_id` unchanged (omi_001's
2,000-3,000 year range still leads on real evidence). Tree name shortened
from the verify record's parenthetical form (72 chars) to fit the 60-char
title limit; the full Japanese name stays in the story and sources.

**Held as a lead: Okakumaki, the cube-pruned Buddhist Pine of Ogi Park
(Saga Prefecture).** Alive, well documented, girth 2.7m, but no national or
prefectural Natural Monument designation found and no legend beyond generic
tourism-listing fame; does not clearly clear the single-tree-destination
bar, and its nearest published tree (Fukuoka fuk_015) sits 18.2km away,
unconfirmed under the day-trip boundary. Recorded in
`data/leads/_famous-japan.json` with full reasoning for a future pass.

**Confirmed dead, moved to blocked: Okina sugi (Yakushima).** Collapsed
September 2010, trunk failure from interior rot plus epiphyte load,
confirmed by ja.wikipedia and a 2010 Nikkei report. Was the second-largest
living yakusugi after Jomon Sugi (yak_001). Never ships per the never-dead
rule.

Build (4609 pages), qa.py (6904 pages, 0 problems) and preflight.py (444
cities, 0 new problems) all clean.

**Released the `hiroshima` claim.** Two consecutive verify attempts against
the same two unmined register clusters (Hirayama Shrine, Fukujoji temple)
came back with nothing new; the remaining 77 leads in
`data/leads/hiroshima.json` are raw, untranslated rows from Japan's national
giant-tree survey (age bands, no individual distinction, health noted only
in Japanese) rather than named candidates, which is a slower and thinner dig
than the famous-tree lane. Leaving it released rather than re-claiming
blind; a future pass should hand-pick specific named trees from the register
(as this session did for the two shrine clusters) rather than mining rows in
bulk, or wait for a fresh angle.

**Left the `_famous-japan` claim standing.** `famous_demand.py --next`
still shows 11 remaining Japan candidates (mostly near-zero measured demand,
one at 45 reads/month: Ushikubo-no-Nagi, joining Nishio). Dispatched a
verify pass on those 11 to `data/research/famousjapan-batch2-verified.json`.

## 2026-09-06 - Amt Neuhaus ships (Eiche am Forsthaus Gruener Jaeger); Schillershoehe oak held

Continuation of an earlier attempt that stopped after 10 min with 110 of its
120-minute window unspent. `passcheck.py --claims` showed two standing:
`_famous-germany` and `hiroshima`, both verify, with uncommitted output
already on disk from that earlier attempt. `data/research/famousgermany-
verified.json` held 2 fully verified trees; `hiroshima-verified.json` was an
empty array (that verify pass found nothing new in the 78 remaining
register leads this attempt).

**Shipped: Amt Neuhaus, Germany, a new single-tree place.** fgm_001, the
Eiche am Forsthaus Gruener Jaeger near Stapel village, ships as amn_001: a
hollow, lightning-scarred pedunculate oak, girth 8.91m, dendrologists'
estimate ~450 years despite its local "700-year oak" nickname, storm-damaged
in 2017 and recovering. Two specialist German tree registers
(baumkunde.de, monumentale-eichen.de) plus the Amt Neuhaus municipality's
own tourism page as the access source. Passes the single-famous-tree-
destination exception on its own local documentation and dramatic
storm/hollow-trunk story, not on global fame.

**Held rather than published: fgm_002, Eiche Schillershoehe (Rudolstadt).**
Verified (coordinates, 3 independent Commons photos, official Thuringian
Naturdenkmal register entry) but no age, no girth, species only to genus.
The fame at that site belongs to the Schiller memorial viewpoint it stands
beside, not to the tree itself, so it does not clear "would somebody travel
specifically for THIS tree". Recorded as held with reasoning in
`data/leads/_famous-germany.json` rather than discarded; may be reconsidered
if a future source gives it real individual distinction, or if Rudolstadt
ever becomes a real city page it could join.

Build (4608 pages), qa.py (6903 pages, 0 problems after fixing a "must-see"
banned word the intro/story/access fields all repeated), preflight.py (444
cities, 0 new problems) and `city_queue.py` (regenerated city-queue.json,
CITY_QUEUE.md, LEDGER.html) all clean. Released the `_famous-germany` claim.

Rung 2 (`health.py`): Data digest flagged failing (17h old). Read the log:
the same benign git-push race documented repeatedly this week (local commit
succeeds, a concurrent writer wins the push, commit lost with the runner).
`gh workflow run data-digest.yml` failed with 403, this token still lacks
`workflow_dispatch` scope. Not fixable from here; the 05:15 UTC cron retries
it as normal.

Left the `hiroshima` claim standing rather than releasing it outright: it
still holds real remaining supply (78 unblocked leads in Japan's national
giant-tree register for the city), just none verified this attempt. A
future continuation should either finish a fresh verify batch from that
register or make the call to release it if the remaining leads keep coming
back thin (many carry no age, address-level-only geocoding, or health
fields in Japanese needing translation).

## 2026-09-06 - _famous-lithuania re-check: no new trees, prior work confirmed sound

Claimed `_famous-lithuania` to refill the writable shelf per prepare.py's
warning. Dispatched a verify pass on the 4 candidates prepare.py's own shelf
count implied were still unsourced (Agluona oak, Bagrėnas linden, Degsnė
larch, Didžioji tuja Kintuose). All 4 turned out to be already handled:
Degsnė and Kintai are the two published places from 2026-09-05 below, and
Agluona/Bagrėnas are already correctly held as leads (Agluona is a 2-tree
cluster under the 4-tree floor; Bagrėnas lacks a fame case beyond being a
real protected tree). The pass did strengthen Bagrėnas's sourcing (found a
second independent source, the state protected-areas cadastre, that an
earlier note had missed) without changing its lead status. Released the
claim; nothing merged. Logged in data/agent-costs.json under 2026-09-06.

## 2026-09-05 (continuation) - Degsne and Kintai: Lithuania's first two published places, one dead tree caught before it shipped

Released `_famous-japan`, claimed `_famous-lithuania` next (94 leads, none
touched before this pass). Picked 6 fresh candidates with coordinates:
Bagrėnas linden, Degsnė larch, Latežeris oak, Karpio tuopa (a poplar),
Didžioji tuja Kintuose (a giant thuja), Papušynė pine.

**2 cleared the single-tree-destination bar, both record claims rather
than legends.** The Degsnė Forest Larch is documented by the Lithuanian
State Protected Areas Service's own register as the tallest tree growing
in Lithuania (49 metres), part of a forest stand planted in 1849 that is
itself the country's tallest forest; shipped as `deg_001` in a new place,
`degsne.json`. The Great Thuja of Kintai is a western red cedar with a
50-year measurement series (16m in 1973 to 19.5m in 2021, still growing),
reputed the tallest of its kind in Lithuania and, by local reckoning,
second only to one tree in Switzerland across Europe; shipped as `kin_001`
in `kintai.json`. Its planting date is only guessed from a neighbouring
building's construction (1902-1912), a textbook bridge claim, so age was
kept broad and the guess written as a guess rather than a fact.

**3 held as leads**: Bagrėnas linden (real, protected, but not the
national record lime, which is already published as Braziūkai), Latežeris
oak (ordinary protected oak, storm-damaged) and Papušynė pine (protected
locally only, nowhere near Lithuania's thickest/tallest pine records).

**1 confirmed dead, caught before it could ship**: Karpio tuopa (Paštuva),
which carries an excellent legend (a flogging-whip planted by a
serf-freeing 19th-century landowner that took root), but the verify pass
downloaded and looked at the Commons photos directly and found a bare,
roofed dead stump matching the on-site sign's own account: lightning split
the tree in 2011, the remnant was covered with a protective shelter in
2012. Blocked rather than shipped on legend alone.

**One bad auto-generated alias caught and fixed**: `city_names.py` matched
"Degsne" to the Wikipedia article for Alytus, a real but unrelated
Lithuanian city about 20km away, well inside its 40km sanity radius but
simply the wrong place. That would have shipped Alytus's own name and
translations (Olita, Alīta, Aleits...) as search aliases for our Degsnė
forest page. Reverted the `search_names`/`wikipedia_titles` entries and
recorded it in `unresolved_names` instead, with the reason, so a future
run of `city_names.py` does not silently regenerate the same mismatch.
`kintai`'s own resolution (to the actual Kintai village article) checked
out and was kept.

These are Lithuania's first two published places (no country page yet,
Contract G needs 3+). Preflight, tree_index, build and qa all clean;
committed, pushed, released the claim.

## 2026-09-05 (continuation) - Takeo: a new single-tree place from the _famous-japan claim, 5 duplicates caught

Released `_famous-germany` and claimed `_famous-japan` next (still the
second-biggest unsourced country batch after japan overtook it). Picked 6
candidates: three that sit inside already-published cities (Kenchō-ji no
Byakushin/Kamakura, Neagarinomatsu at Kenrokuen/Kanazawa, Nagoya-jo no
kaya/Nagoya castle) and three standalone leads (Kamo-no-Okusu, Takeo no
Okusu, Nago no Hinpun Gajumaru).

**5 of the 6 turned out to be duplicates of trees already on the site**,
each caught by running `passcheck.py --brief` and a direct coordinate
check before writing anything, exactly the check that caught Göttingen's
duplicate in the previous batch: Kenchō-ji's juniper is kmk_001 (~12m away),
Kenrokuen's pine is kan_004 (~90m), Nagoya Castle's kaya is ngy_001 (~35m),
Kamo's camphor is hmy_001 (higashimiyoshi.json, identical coordinate), and
Nago's banyan is nag_001 (identical coordinate, its own existing place).
The Nago duplicate check did produce one real improvement worth a future
curation pass: independently confirmed the species as banyan (Ficus
microcarpa, national register + ja.wikipedia) against the currently generic
"Fig (Ficus sp.)" on file, and found a dated alive-now event (a car struck
the tree during a typhoon on 2026-08-08, minor damage, resecured, confirmed
still standing).

**Takeo no Okusu had no container and verified cleanly**: a 20-metre-girth,
30-metre camphor on the grounds of Takeo Shrine (Saga Prefecture, founded
735), sacred tree with a stone shrine built inside its own hollow trunk,
traditionally said to be 3,000 years old (shrine tradition, not a
measurement, kept broad and flagged), repeatedly named one of Japan's
largest trees by girth and one of Saga's three biggest. Health has been
declining for years (city restoration 1994-2003, a widened protective
perimeter since a 2022 notice), still standing and viewable per the most
recent evidence. Shipped as a new place, `takeo.json` (tak_001), distinct
from the existing Kawago place (kwg_001, a different camphor 7.5km away in
the same municipality). All 6 leads marked resolved so this batch never
re-runs. Preflight (0 problems, only the expected "never looked up in
other languages" NOTE), city_names, tree_index, build and qa all clean;
committed, pushed, released the claim.

## 2026-09-05 (continuation) - Scheessel: a new single-tree place from the _famous-germany claim, plus 5 leads held or blocked

Shelf refill: `prepare.py` reported "REFILL THE SHELF FIRST" (0 leads ready
to write, 47 files staged for a later verify pass, none awaiting a writer).
Claimed `_famous-germany` (still the biggest unsourced country batch) and
dispatched a verify pass on 6 named candidates, all with coordinates and
Commons photos already attached: Everseiche, Lieveneiche, Gerichtslinde
Göttingen, Gerichtslinde in Alfeld (Leine), Gerichtslinde Scheeßel,
Heinrichslinde.

Two cleared verification: the Gerichtslinde of Göttingen turned out to be a
duplicate of the already-published gtn_001 (same coordinates, same 714cm
girth, same two sources), caught by `passcheck.py --pending` before it was
written up, so no new tree there, just a wasted verify slot. **The
Gerichtslinde of Scheeßel** did clear the single-tree-destination bar (a
documented Femegericht/court site since 1288, a pillory into the 1900s, a
hollow twin-trunk structure, 710cm girth, age genuinely disputed 500-800
years) and became a new place, `scheessel.json`, on the same template as
Effeltrich and Reinborn: one tree, its own intro/FAQ/question page, `sch_001`.

Held below the bar as leads: Everseiche (verified but its crown is reported
"partially dead" as of a July 2025 photo caption) and Lieveneiche (verified
existing but too thin, no age, no girth, no register entry). Corrected:
Gerichtslinde in Alfeld (Leine) is officially "2 Dinglinden" per its own
register, not one tree, kept as a lead with that correction. Blocked:
Heinrichslinde, whose current physical tree is a sapling planted January
2022, the second replacement after the original collapsed in 1894 and its
successor was felled in 2021; no genuinely old tree stands there today.

Ran preflight (0 problems), tree_index, `npm run build`; committed and
pushed. Cost logged to `data/agent-costs.json` under 2026-09-05 (verify
~179k tokens for the 6-candidate batch, write ~101k for the single-tree
batch, the batch-of-one overhead BRIEF_WRITING.md warns about). Released the
`_famous-germany` claim.

## 2026-09-05 (night run) - Baarn submissions 84-86: two Cantonspark register trees found via a reader's GPS

Three `kind: tree` rows, same account, same visit (07:12-07:15 UTC), all GPS-tagged
near Cantonspark's main entrance, minutes after the same reader's two photographs
of brn_001/brn_002 were approved. Matched the three points against the
Landelijk Register Monumentale Bomen (`data/registers/netherlands-lrmb.json`):
row 85 (17m) and row 86 (7m) both sit tight on the register's coordinate for
"Mammoetboom Cantonspark" (nr 1696953, planted 1910-1920, gemeente-owned,
visitable, heading toward 6m girth), which reads as the same specimen already
published as brn_002 at a rough "main entrance" placeholder 140m off. Upgraded
brn_002's pin from approximate to confirmed using the register point and added
the register as a second source; the story's closing note now says the pin is
sharper rather than claiming a fresh girth measurement, since the register gives
no new number.

The same cluster also sits 15-32m from a second register entry, "Tulpenboom
Cantonspark" (nr 1696955, same planting decade, same owner), a tulip tree
genuinely distinct from the brn_003 grove several kilometres away at Kasteel
Groeneveld. That was not in our data at all. Added as brn_007, sourced to the
register plus Cantonspark's own Rijksmonument listing (rijksmonumenten.nl),
story written, no photo.

Row 84 ("Watercypres", 21-32m from both register points) matches neither
entry, and no cypress-genus tree is registered at that spot. `data/leads/baarn.json`
already flags an unresolved, coordinate-less "Bald Cypress 'Fastigiatum'" and
"a second Dawn Redwood" from a 2014 monumentaltrees.com index of the same
pinetum, either of which this could be; not enough to place, so not shipped.
Left as an open question.

Set outcomes via the service key: rows 85/86 `changed` (one combined reply on
row 86 naming both pages, mailcheck clean, sent via contributor_reply.py),
row 84 `open_question` asking for a photo or a rough position relative to the
sequoia. All three appended to `data/submissions-processed.json`. Updated
Baarn's intro/FAQ from "five of the six" to "six of the seven" free trees.
Build (npx astro build), tree_index.py and preflight all clean.

## 2026-09-05 (night run) - Merged famous-uk-batch-a: 3 new single-tree places, Bristol to 6

Finished a verify pass claimed and left mid-window by an earlier attempt this
same run: `data/research/famousuk-batch-a-verified.json`, 4 trees, dispatched to
a write-stories pass and then merged in. The Brimmon Oak (Newtown, Powys), a
pollard oak the A483 Newtown bypass was rerouted 15m to save, runner-up in the
2017 European Tree of the Year; Nellie's Tree (Aberford, West Yorkshire), three
beeches a miner grafted into a living letter N around 1920, UK Tree of the Year
2018; and the Survivor Tree (near Moffat, Dumfries and Galloway), a modest
rowan that was nearly the only tree standing in the Carrifran valley when
700,000 were planted around it, all three ship as new single-tree places under
the 2026-08-31 exception, none reaching the four-tree floor and none needing to.
The Strawberries and Cream Tree, a graft-chimera cherry in Backwell, joins
Bristol as bri_006 (day-trip distance, 9.5km), flagged for its rough 2025
health after a dry spell rather than described as thriving.

All four keep `location_precision: confirmed` and `curation_status: flagged`
from verification; photos left `missing` (candidates found but not yet viewed,
per the Cadiz standard). Released the `famous-uk-batch-a` claim. Removed the 4
published leads (5 rows, Nellie's Tree was a duplicate at two indices) from
`data/leads/_famous-united-kingdom.json`. tree_index.py rebuilt, build and
preflight clean.

## 2026-09-05 - Write pass on bomenbieb-dutch-verified.json: 11 Dutch single-tree places

Eleven verified trees from the bomenbieb.nl Dutch register, each published as its
own single-tree place (no existing city page). Stories written, three best_time
fields set, no verified field changed. All eleven are flagged rather than
confirmed, and each page carries its own dispute in the prose. Both ensemble
candidates resolved as ONE collectible entry, as the verify notes said they
should: the Wodanseiken are a compact signed grove with the Wodanroute built
around them, and the Koningstafel pollards are a named cluster at one viewpoint.
Philemon ships alone; its named partner Baucis blew down in storm Ciaran at the
end of 2023 and is blocked as dead, with bomenbieb's own vitality field still
wrongly listing it alive (a stale-register case worth remembering).

- Wolfheze, 1 tree (The Wodanseiken), single-tree place from the bomenbieb.nl Dutch register
- Velp, 1 tree (Philemon), single-tree place from the bomenbieb.nl Dutch register
- Doornenburg, 1 tree (The Thousand-Year Oak of Doornenburg), single-tree place from the bomenbieb.nl Dutch register
- Den Hout, 1 tree (The Heilige Eik), single-tree place from the bomenbieb.nl Dutch register
- Hilvarenbeek, 1 tree (The Gebodenlinde), single-tree place from the bomenbieb.nl Dutch register
- Stoutenburg, 1 tree (Adam en Eva, a pair mapped as one entry, view-only from the road), single-tree place from the bomenbieb.nl Dutch register
- Fleringen, 1 tree (The Kroezeboom), single-tree place from the bomenbieb.nl Dutch register
- Rhenen, 1 tree (The Pollard Oaks of the Koningstafel), single-tree place from the bomenbieb.nl Dutch register
- Vorden, 1 tree (The Lodewijkslinde), single-tree place from the bomenbieb.nl Dutch register
- Nuenen, 1 tree (The Dorpslinde), single-tree place from the bomenbieb.nl Dutch register
- Sambeek, 1 tree (The Linde van Sambeek), single-tree place from the bomenbieb.nl Dutch register

Superlative discipline (hard rule 8): three of these are locally promoted as the
oldest oak or tree in the Netherlands. Doornenburg attributes the claim to a
municipal sign and says the sampling does not support a thousand years, Den Hout
attributes it to the forester who argues the case and names the majority view
against him, and Fleringen records the claim as not well supported. Sambeek
carries "thickest lime in the Netherlands" and Nuenen "thickest large-leaved
lime", which are different crowns and are stated as such. superlatives.py reports
no collisions.

Photos: all eleven ship with status `missing`. Nothing was hunted in this pass.

## 2026-09-05 (continuation) - Finished the _famousgermany + _famousjapan-b verify claims: 8 trees merged, 6 new single-tree places, 1 held

Two verify passes had already finished under the standing `_famous-japan` and
`_famous-germany` claims and sat staged uncommitted: `famousgermany-2026-09-05-verified.json`
(3 candidates: Tanzlinde Sachsenbrunn, Marienlinde Telgte, Gerichtslinde
Gottingen) and `famousjapan-2026-09-05-b-verified.json` (6: Ushikubo-no-Nagi,
Minamihanazawa/Kitahanazawa no Hananoki, Ryotokuji and Shirahatayama
Ohatsuki Icho, Jissoji no Icho). Dispatched a write-stories pass on all 9,
merged 8 into `data/cities`: 6 new single-tree places (Sachsenbrunn,
Telgte, Gottingen, Higashiomi with 2 trees, Maibara, Mito) and one tree
(Jissoji no Icho) joined the existing Ichinohe page as its second tree.
Ushikubo-no-Nagi held, not published: a second independent pass confirms the
2026-09-04 verdict that it does not clear the single-tree-destination bar
(~45 Wikipedia views/month, no festival or rite found); its full record is
kept on the leads entry rather than discarded. Preflight caught 5 length
violations in the hand-written page copy before build; fixed, build and QA
both clean (6440 pages). Full writeup in LOG.md. Claims released for
`_famous-japan` and `_famous-germany`; `_bomenbieb-netherlands` (64 unresolved
leads across several Dutch cities) left standing for the next run.

## 2026-09-05 (continuation) - Finished the standing _famous-japan claim: 9 trees merged, 5 new single-tree places

Picked up a `_famous-japan` verify claim left standing by an earlier attempt in this window (112 min left on the claim), with three research batches (A/B/C, 9 trees total, batch1 empty) already fully verified and written, staged uncommitted in `data/research/famousjapan-batch{1,A,B,C}-verified.json`. All 9 were already merged into city files by the earlier attempt; this pass verified the merge was clean, fixed two meta_descriptions the build caught over the 155-char limit (Kimotsuki, Maebashi), ran `city_names.py` for the 5 new places (4 of 5 resolved; Hino ambiguous on Wikipedia, left unresolved), and committed. New single-tree places: Himi (Oidani no Otsubaki, Japan's largest known wild camellia), Hino (Kumano no Hidarimakigaya, 1922 discovery site of a left-spiraling kaya mutation), Kimotsuki (Tsukazaki no Kusu, a camphor atop a 4th-century burial mound), Oguni (Shimojo no Oichou, a giant ginkgo mistaken from the road for a wood), Yamanashi City (Okkazuma no Shidarezakura, a weeping cherry alone on a hilltop). Grown: Maebashi (+Kinmokusei of Kezoji), Iwata (+Kitahama no Okayanoki), Hokuto (+Utsukushimori no Oyamatsutsuji), Fujikawaguchiko (+Yamanokami no Fuji). Japan's country page corrected 76->81 places, 196->205 trees. Full build (4373 pages), qa.py (6387 pages), preflight.py (388 cities, 0 problems) and superlatives.py (638 claims, no collisions) all clean. Claim released. The research staging files could not be deleted this session (rm denied by permission mode) and sit untracked; a future run should remove them, their content is fully merged.

## 2026-09-05 (continuation) - Finished the standing _famous-japan claim: 3 trees staged since 01:56 UTC, written and merged

Picked up a `_famous-japan` verify claim left standing by an earlier attempt in this window, with three trees already fully verified and staged uncommitted in `data/research/famousjapan-verified.json`, stories only missing. Wrote all three directly rather than dispatching a fresh write pass: Maebashi (new single-tree place, mae_001, The Great Kaya of Yokomuro, one of Japan's three great kaya trees), Hokuto (hok_002, Shinden no Oitozakura, a paddy-field weeping cherry), Yabu (yab_002, Takinoya no Hidarimakigaya, one of only 4 documented left-spiraling Torreya in Japan, genuinely declining per the city's own record). Full writeup in LOG.md. Species name for Torreya nucifera reconciled to the corpus's existing canonical "Japanese Nutmeg-yew" (hard rule 9), which the build caught. Japan's country page corrected 75->76 places, 193->196 trees. Removed the 3 delivered entries from `data/leads/_famous-japan.json`. Full build (4354 pages), qa.py (6343 pages) and superlatives.py (637 claims, no collisions) all clean. Claim released.

## Submissions batch, 2026-09-04 (ids 64-83): votes and one already-queued tree lead

20 unprocessed rows, all from today. 18 are "worth it" / "vote undone" pairs on
sar_001, ful_001, utr_002 and pad_001 (mostly one account exercising the new
compact vote button, per WorthIt.swift's 2026-09-04 redesign) — bookkeeping,
verified nothing, mailed nothing, per the standing rule for vote-undo rows.
The one real submission, id 70 (kind: tree, Baarn, GPS 52.21398,5.29701,
"standing at the tree"), is the app's own sighting 4d6fb810, already fetched
and recorded by `sightings_inbox.py` earlier today at
`data/leads/_sightings.json` ("A tree I found", no species, 554m from the
nearest published tree) with outcome "lead". Nothing more to verify from a
name-only, species-unknown photograph; it waits like any other lead. All 20
ids appended to `data/submissions-processed.json`.

## Lisbon, 2026-09-04: +2 from getLISBON's own writing

getLISBON (contact@getlisbon.com) replied to batch-006 suggesting two jacarandas
at the Jardim Botanico da Ajuda, and proposed a mutual link. Researched from
their two published articles rather than by asking them questions.

- **lis_034, The First Jacarandas of Lisbon.** Two surviving originals of the
  specimens Felix de Avelar Brotero acclimatised from 1811; he distributed seed
  across the city, which is why Lisbon is a jacaranda city at all. Both sources
  (getLISBON; A Mensagem 2025 and 2026) say the pair are the LAST in Lisbon to
  flower, and neither says where in the garden they stand. Published as ONE
  entry for two trees (the surviving pair is itself the destination), pin at the
  garden, location_precision approximate, and the page asks the reader which two
  they are. Age derived from Brotero's directorship, not from a planting date.
  No photograph: Commons geosearch around the garden returns 50 files, all from
  one generic Flickr batch, none identifiable as these two.
- **lis_035, The Paineira of Rua dos Jeronimos.** Named in their public-interest
  trees article and verified against ICNF processo KNJ1/404: Ceiba crispiflora
  H.B.et K., arvore isolada, classified D.R. n.o 298 II Serie 27/12/2001, girth
  4.2 m, height 24 m, crown 22 m, measured 2015, per-tree coordinate. Named
  "Paineira (Ceiba crispiflora)" under hard rule 9: crispiflora is accepted and
  distinct from pentandra ("Kapok") and speciosa ("Silk Floss Tree"), so
  borrowing either name would group three species under one page.

Not resolved and worth a later pass: their article also lists a Ficus
macrophylla group at Largo Hintze Ribeiro, which ICNF holds as AIP11066601C at
38.71869,-9.15517. That is a different location from our lis_013 (Jardim Franca
Borges) and may be a tree we do not have.

Hosts that refused this pass: www.nationalgeographic.pt and www.publico.pt both
return HTTP 403 to WebFetch. Fast fail, not a hang, so they cost a second
rather than a window; not added to the blocklist for that reason.


**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-08](archive/CURATION-2026-08.md)
- [2026-07](archive/CURATION-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.

<!-- archive-index -->
## 2026-09-04 (continuation) - Finished the standing _famous-japan claim: 3 trees, Fujikawaguchiko and Atami grown to two each, Iwaki opened

Picked up a `_famous-japan` verify claim left standing by an earlier attempt in this window, with three trees already fully verified and staged uncommitted in `data/research/famous-japan-batch{1,2,3}-verified.json`, stories only missing. Wrote all three directly rather than dispatching a fresh write pass:

- **Fujikawaguchiko** (fjk_002, The Ohatsuki Ginkgo of Jotakuji Temple): a leaf-seed variant ginkgo in Minobu (~17km south, day-trip distance, labelled honestly), one of only 7 nationally-designated Ohatsuki Icho in Japan. Toppled by Typhoon Trami on 2018-09-30; the temple left it where it fell and it has resprouted and fruited from the ground every year since. Age (~750 years) is a Nichiren-era legend, stated as such. Fujikawaguchiko's intro/meta/question_answer updated from "maps one tree" to two; hero/oldest stay fjk_001 (Shoji no Osugi, older).
- **Atami** (ata_002, The Byakushin of Joganji Temple): a spiral-trunked Chinese juniper over 800 years old at a temple in Yugawara, one stop by train from Atami (day-trip boundary, labelled honestly). National Natural Monument since 1939. Atami's intro/meta/question_answer updated from "maps one tree" to two; hero/oldest stay ata_001 (the Great Camphor, legendarily older).
- **Iwaki** (iwk_001, Nakakamado no Shidare Momiji): new single-tree place under the 2026-08-31 exception. A two-trunk weeping Japanese maple, National Natural Monument since 1937, that Iwaki's city government tracks and forecasts for autumn colour every year. No confirmed age: ja.wikipedia's 400-500 year figure rests on a bridge claim to the temple's founding date that no source actually makes, so left unstated per the no-basis rule. Real travel to Takahagi's only tree (tkh_001) is 45-70 minutes door to door, well past the day-trip boundary, so it does not join Takahagi as a container.

None have photos yet (honest gap, `status: missing`). `data/countries/japan.json`'s city count corrected 66 to 67; `city_names.py` resolved Iwaki's foreign-language names into `data/city-aliases.json`. Full local build (6155 pages) and `scripts/qa.py`/`preflight.py` clean. Claim released.

## 2026-09-04 (continuation) - Australia famous-tree batch: 1 verified of 12, and a photo viewing pass on the 5+-tree shortlist

Dispatched a verify pass on `famous_demand.py --next`'s Australia batch (12 candidates, unusually weak demand for this lane at 17-82 reads/month, several 19th-century explorer "blazed"/"marked" trees flagged in the brief as high dead-tree risk). The caution paid off: **1 verified, 11 blocked**, the worst yield of any famous-tree batch run so far.

- **Miriam Vale** (bfm_001, The Big Fig): a weeping fig on a public road reserve, roughly 12m round including its buttressing, 30x35m canopy, planted around 1897-1900 per Queensland's heritage register. Long civic history (milk depot until 1977, Anzac Day shelter, informal vet's surgery); last confirmed alive by council-commissioned root work in January 2015. Passed the single-tree-destination test cautiously: no dedicated visitor infrastructure yet, but unfenced, physically enormous, the town's own chosen emblem, and a known waypoint on the coast road to Agnes Water/Seventeen Seventy.
- **Blocked (11):** 3 confirmed dead (Landsborough Tree, burnt stump since 2002 arson; The Robbers Tree, lightning-struck 2021; Moonah Creek Hanging Tree, a 2003 assessment states outright "no longer living"), 6 on private land with no public access (Kidman's Tree of Knowledge, H2 Hinde Tree, both Landsborough's Blazed Trees, Hodgkinson's Marked Tree, Hoop Pines at a still-operating school), 1 not a single collectible point (William Wyndham's remnant orchard, scattered across a suburb), and 1 that cleared every evidence bar but failed the destination test itself (Fig Tree, Gladstone: a fine, well-documented heritage tree but no tourism promotion found, reads as a car-park shade tree rather than a reason to travel). Every blazed/marked explorer tree in the batch turned out dead or landlocked, exactly the risk flagged going in. Full detail recorded back into `data/leads/_famous-australia.json` (1 flipped to published, 11 to blocked with reasons) rather than left only in the research file. Wrote a new species page, `weeping-fig.json` (Ficus benjamina now has 3 mapped trees: Miriam Vale, Brisbane, Lisbon), earned by this addition per `pagegaps.py`. Claim released.

**Photo viewing pass on `photo_gaps.py`'s shortlist**, 12 cities that cleared the 5-tree threshold with no photograph at all: **3 approved** (Kanazawa's Raised-Root Pine, Kauai's Tree Tunnel, Auckland's Coronation Tree), **1 held** (Brighton's Preston Twin, right park but cannot confirm which twin survived a 2019 felling), **8 rejected**, several not even photos of trees at all (a Stolperstein memorial cobblestone offered for Maastricht, an archival portrait of Queen Wilhelmina offered for Eindhoven) or a straightforward species/city mismatch (Groningen's ginkgo candidate was actually Utrecht's; Hilversum's and Ghent's candidates were the wrong species in the right garden). Found and fixed a real bug while applying the approvals: `photo_apply.py`'s `full_image()` only recognised the `upload.wikimedia.org` hostname, but `photo_hunt.py`'s sweep writes candidates under the API's `thumb.wikimedia.org` hostname, so every recent approval through this path was silently shipping a capped 960px thumbnail instead of the site's own original-resolution standard. Fixed to recognise both; 25 already-approved trees are affected and worth a follow-up sweep to re-derive their originals.

Full local build (6130 pages) and `scripts/qa.py`/`preflight.py` clean throughout.

## 2026-09-04 (continuation) - 6 more single-tree places: Brazil batch 1, Bulgaria batch 1 and 2, France batch 1

Finished 4 standing verify claims (`_famous-brazil-batch1`, `_famous-bulgaria-batch1`, `_famous-france-batch1`, `_famous-bulgaria-batch2`) left by an earlier attempt in this window. Three trees (Brazil x2, Bulgaria x1) already had full stories written and new city files staged, uncommitted; wrote the remaining three (France x2, Bulgaria x1) directly from the verify pass's `verify_notes`, all under the 2026-08-31 single-tree-destination exception:

- **Pirangi** (pir_001, Cajueiro de Pirangi): a single cashew whose branches root laterally, spreading one tree across roughly 8,500 sqm; Guinness World Record holder since 1994 for largest cashew tree, ~138 years old, paid entry (R$10).
- **Vassununga** (pat_001, O Patriarca): a jequitiba-rosa in the cerrado of Vassununga State Park, widely called Brazil's oldest tree though the age claims range wildly (600 to 3,000+ years across three uncorroborated sources); free but pre-booked entry.
- **Bansko** (bkp_001, Baikushev's Pine): a Bosnian pine in Pirin National Park, ~1,300 years by repeated tradition (contemporary of Khan Asparuh, no ring count found), 7.8m girth, free.
- **Allouville-Bellefosse** (alv_001, Chêne Chapelle): an oak roughly 800-1,200 years old, hollowed by lightning in the 1600s and holding two working chapels inside since 1696, monument historique since 1932, free.
- **Concoret** (gth_001, Guillotin Oak): an oak on the edge of Forêt de Paimpont (Brocéliande), 500-1,000 years disputed, national "Arbre remarquable" since 2017, fenced since 2019 but visible from a public path, free.
- **Granit** (gnk_001, Granit Oak): Bulgaria's oldest tree by an actual 1982 ring count (~1,680 years), reduced to one living branch after a 1969 storm and falling groundwater, confirmed still greening as of 2024, natural monument since 1967, free.

None have photos yet (honest gap, `status: missing`). Two new country pages written to close the page-gap these opened (`brazil.json`, 3 cities/8 trees; `bulgaria.json`, 3 cities/6 trees), and France's country page counts corrected (7→9 cities, 96→98 trees). Also cleared and re-added the pin-outlier NOTE for `pir_001` in `preflight.py`'s `check_pin_is_in_its_own_country()` by hand (checked against pt/en Wikipedia coordinates; Pirangi is a genuine 2,054km outlier from Rio de Janeiro, our other Brazilian city). Full local build (6121 pages) and `scripts/qa.py` clean (had to `git fetch --unshallow` first; the shallow-clone sitemap-lastmod check otherwise false-positives). All 4 claims released.

## 2026-09-04 (continuation) - 6 single-tree places: UK batch 1, Germany batch 1, Formentera, Ibiza

Finished 2 standing verify claims (`_famous-uk-batch1`, `_famous-germany-batch1`) plus 2 orphaned verified-but-unwritten leads (Formentera, Ibiza) with one write-stories pass, one tree each place, all under the 2026-08-31 single-tree-destination exception:

- **Glastonbury** (gls_001, The Glastonbury Thorn): a hawthorn (Crataegus monogyna 'Biflora') in St John the Baptist's churchyard, ~90 years old (planted 1930s by Abbey head gardener George Chislett), flowered twice a year, supplies the sprig cut every December since 1929 and sent to the monarch. Flagged: coordinates are the church's, not a tree-level pin (`location_precision: approximate`).
- **Runnymede** (ank_001, The Ankerwycke Yew): 2,000-2,500 years (Woodland Trust vs National Trust disagree by 500 years, both carried), 7.98m girth, in the ruined grounds of St Mary's Priory across the Thames from Runnymede meadow. Tradition, not record, ties it to the 1215 Magna Carta sealing and Henry VIII/Anne Boleyn.
- **Tolpuddle** (tol_001, The Tolpuddle Martyrs Tree): sycamore, ~340 years, 6.06m girth, largest sycamore in Dorset, where six farm labourers founded an agricultural union in 1833 before being transported to Australia. Pollarded 2023 to extend its life.
- **Wessobrunn** (wes_001, The Tassilolinde): large-leaved lime, 700-900 years (German Dendrological Society, stem-structure estimate), ~14m girth, third-largest lime girth in Bavaria. Legend ties it to Duke Tassilo III's 753 founding dream, which the tree is too young to have witnessed; told as legend, not fact. Naturdenkmal since 1980, Nationalerbe-Baum since October 2023.
- **Formentera** (fmt_001, Savina de Ses Salines): Phoenician juniper, over 500 years (no upper bound stated by either source), inside Ses Salines Natural Park near Ses Illetes beach. Split out of an earlier Ibiza dispatch (2026-09-03) after the original id turned out to be on the wrong island.
- **Ibiza** (ibz_001, Pi de Can Reiet): Aleppo pine, 100-150 years, 349cm girth, roadside on the Santa Eularia-Sant Joan road, owned by the island council. Leaning crown, actively managed.

None have photos yet (honest gap, `status: missing`); none are in `data/photo-queue.json`. Also fixed 4 country pages' stale `meta_description` tree/city counts (Germany, Japan, Spain, United Kingdom) caught by `preflight.py` after these went live. Full detail in LOG.md.

Finished a standing famous-Japan verify pass an earlier attempt in this window left uncommitted (verified and written, never merged). Three candidates became single-tree places under the 2026-08-31 exception:

- **Kawago** (kwg_001, Kawago no Okusu): a hollow camphor with a 21m base girth, 5th-widest tree in Japan, national monument since 1924, a purpose-built park around it since 1995.
- **Asago** (asg_001, Itoi-no-Okatsura): a decayed katsura stump ringed by roughly 80 root suckers reading as a small grove, national monument since 1951, reached only by a 90-minute walk up a gorge trail.
- **Suzuka** (suz_001, Shiroko Fudan Zakura): type specimen of the Fudanzakura cherry cultivar (nearly year-round flowering, documented double season), one of only 39 cherries ever designated a national natural monument, a named cherry recorded at the same temple courtyard since 757-765 CE though the current wood is ~80 years old after repeated fire and storm damage.

6 further batch candidates blocked (Wilson's Stump and Noin's Rain-Praying Camphor, both dead; the Tado pear habitat, Ono no Shidare-guri and Shikishima's bamboo, all population/habitat designations rather than single collectible trees; a mis-pinned Senbon Icho candidate corrected in place) and 1 held (Ushikubo-no-Nagi, verified but borderline on the single-tree-destination test). Recorded in `data/leads/_famous-japan.json` and a new `data/leads/nagoya.json` (holding the Tado block, 21.7km from Nagoya). `preflight.py` caught word-count violations on 2 of the 3 new pages (Contract B/C), fixed before commit; `city_names.py` run for all three (Kawago has no Wikipedia article to resolve against, a hamlet too small, reported not stored).

**Register scouting (rung 5): 2 real finds, neither licensed yet.** `scout_next.py --target` walked Boise (empty, Idaho's Big Tree Program has no coordinates), then Long Beach and Little Rock, both real: California's `selectree.calpoly.edu/api/bigtrees/getAllBt` (266 champion trees statewide, found in a webapp's JS bundle, no stated licence anywhere on either Cal Poly site) and Arkansas's ArcGIS "Champion Trees layer" (117 points with a Public/Private flag baked into each description, no stated licence, and the state department's own page 403s to automated fetches via Cloudflare). Both recorded `stalled` in `data/register-scouting.json`, pending a licence ask; full detail in `OPEN_DATA_SURVEY.md`. Stopped before New Orleans (#63, next on the list) to avoid turning scouting into a sweep.

## 2026-09-04 (continuation) - Cagliari's Italian overlay (Contract J)

`langcheck.py --next` named Cagliari the highest-impression untranslated Italian page (43 impressions, its English twin, over the ten-day window) with no `it` overlay yet. Hand-written full overlay for all 10 trees plus the city and question page, matching the established Italian style (Rome/Palermo/Naples/Florence/Milan/Bologna/Venice overlays, "alberi monumentali" as the search term). Faithful to the English facts throughout, including the honest gaps (Corongiu's lime keeps its unconfirmed trail-access note, the Tintitaco keeps its two disagreeing age figures). `i18ncheck.py` caught a missing `intro` key and two over-length meta fields (174 and 165 chars against the 155 limit), fixed before commit.

## 2026-09-04 (continuation) - Ibiza register verify pass: 2 verified, both below their floor, and one belongs to Formentera not Ibiza

Dispatched a verify pass on Ibiza's 5 register candidates (balears-arbres-singulars.json). 3 turned out to sit on private land, the register's own `private: true` flag confirmed by independent sources (periodicodeibiza.es); one of them, the Olivera de N'Espanya, a possibly 1,000+-year-old olive and plausibly the largest in Spain, is the single most tempting exclusion of the pass, but its own sources say its exact location is deliberately kept low-profile and it stands on private land. All recorded in `data/leads/ibiza.json` with reasons, alongside the 3 group-designation entries the brief had already excluded.

Of the 2 that verified clean (public land, two independent sources each), only one is actually on Ibiza: **ibz_001, Pi de Can Reiet**, an Aleppo pine on a public road near Santa Eularia, owned by the island council itself. The other, the register's "Savina de Ses Salines" (a Phoenician juniper over 500 years old, likely the oldest sabina in the Balearics), turned out from its own coordinates to stand in Ses Salines Natural Park on **Formentera**, reached from Ibiza only by a 25-35 minute ferry plus a further walk. Folding it into "Ibiza" would have been exactly the out-of-island misattribution CLAUDE.md's day-trip rule forbids (the same shape of error the 2026-09-04 Sakegawa/Tsuruoka case caught). Re-id'd to `fmt_001` and split into its own `data/research/formentera-verified.json`, since Formentera is its own island and municipality and gets the same treatment as Kauai, Menorca and Madeira: a place, not assumed to be part of its larger neighbour.

Both `ibz_001` and `fmt_001` sit below the 4-tree floor alone and stay unpublished, waiting for more candidates (Ibiza's other register rows are exhausted; Formentera has not been scouted at all yet). Claim released.

## 2026-09-04 (continuation, finishing a standing write pass) - 6 single-tree places published from famous-Japan leads; Alicante's 15th tree

Finished a write-stories pass an earlier attempt in this window left uncommitted (verify_notes already merged by an even earlier attempt, stories never written up). Six verified famous-Japan candidates became their own single-tree places under the 2026-08-31 exception, none near a published city:

- **Kawatana** (kwt_001, The Camphor Forest of Kawatana): a single tree reading as a wood, National Natural Monument since 1922, dying back since 2017 and tentatively recovering.
- **Matsumae** (mtm_001, Kechimyaku Zakura): mother tree of the Matsumae-hayazaki cherry cultivar, at Kozenji temple.
- **Numata** (num_001, The Great Mulberry of Usune): Japan's largest wild mulberry, National Natural Monument since 1956, tied to the Gunma silk story.
- **Omishima** (omi_001, Ikiki no Gomon): a camphor at Oyamazumi Shrine hollowed into a walkable passage.
- **Sakegawa** (skg_001, Kosugi no Osugi, "the Totoro Tree"): went internationally viral around 2020 for its ear-shaped twin crowns.
- **Shimizu** (smz_001, The Great Cycad of Ryuge-ji): largest cultivated cycad in Japan, one of the "three great cycads", paid temple entry (fixed a missing `paid_entry` flag preflight caught).

**Alicante 14 -> 15**: ali_015, a Norfolk Island pine on Plaza de Calvo Sotelo, cleared the two-source bar this pass (a second, independent local-history blog post). Spanish overlay extended to cover it (Contract J), and the leads files for both famous-Japan and Alicante updated to remove the now-published entries.

Two question_context bodies (Kawatana, Sakegawa; Omishima) were widened to clear Contract B's 150-200 word floor, which the write pass had left short. Japan and Spain country-page meta_descriptions corrected for the new counts (57->63 cities, 248->249 trees). Build (4194 pages) and `scripts/qa.py` (5987 checked) clean. All three standing claims from the earlier attempts (_famous-japan, alicante, _famous-global) released; the last had no work product on disk to finish.

## 2026-09-03 (continuation, finishing a standing claim) - Brisbane fifth deepen attempt: zero trees, two open leads checked and still genuinely unresolved

Finished the standing `brisbane` verify claim left by an earlier attempt in this window (register candidates already fetched: 558 significant-landscape-tree points within 20km, all unnamed coordinates, matching the previous two zero-yield deepen passes' finding that this register requires per-point identification with no name field). Rather than mine that pile again, checked the two most promising open leads in `data/leads/brisbane.json`:

- **The Hoop Pines of St Paul's Anglican School (Bald Hills)**: well-sourced (Queensland Heritage Register + independent local news), within day-trip range, single collectible point. Still blocked purely on access: fetched the Wikipedia article and the heritage listing again, found only that the pines frame the school's private driveway and have "landmark value on the ridge", which is aesthetic significance, not evidence of a public sightline or open grounds. No new evidence either way; correctly still a lead per the schools rule.
- **The Bunya Tree of Manly West**: single-sourced to the Brisbane Heritage Register. A WebSearch summary appeared to cite mappingbrisbanehistory.com.au as an independent second source describing "two bunya pines... two sentinels", but fetching the actual page via Wayback Machine (direct fetch 403s) found no mention of bunya trees at all in its text; the search engine's synthesis had drawn on the same heritage-register source, not a second one. Still single-sourced, and still 14km/35-43min from the CBD, outside the ~30 minute day-trip guideline. Correctly still a lead.

Zero trees shipped, but a real question closed both ways rather than left stale: neither lead is quietly re-openable by a future pass without genuinely new evidence (a street-level photo of the St Paul's driveway from the road, or a second independent source for the Bunya tree). Claim released.

## 2026-09-03 (continuation run 8, part 2) - Jacksonville register scout: thin, one lead recorded, zero trees

After releasing all six bomenbieb claims, `scout_next.py --target` pointed at Jacksonville (#53, no supply/no verdict). The Florida Champion Tree Register (ffs.fdacs.gov, 577 entries statewide) is real and reachable only via Wayback (live host times out from this sandbox; added to `data/fetch-blocklist.json`). Duval County holds just 8 rows, and the register withholds Latitude/Longitude/Location for private-ownership trees exactly like Missouri's already-scouted Champion Trees service did: confirmed on 2 of 3 checked (Florida Champion American Elm id 32, National Co-Champion Slash Pine id 29, both Private/Withheld). Only one Duval row is public: id 1060, the Tough Bumelia (Sideroxylon tenax) National Champion, with real coordinates and a location string ("Next to HQ Driveway adjacent from the Curatorial Building") that a future pass still needs to identify. Recorded as a single-candidate lead (`data/leads/jacksonville.json`) rather than a register import, since one usable public specimen out of 577 doesn't clear the bar for a register file. Verdict logged in `data/register-scouting.json` as `stalled`, not `blocked` or `empty`, since the register itself is genuine and usable elsewhere in Florida, just thin for this specific city. Jacksonville still needs a from-zero web research pass for its other candidates.

## 2026-09-03 (continuation run 8, following an attempt that shipped 5 trees and stopped after 42 min with 78 unspent) - Finished the standing bomenbieb-netherlands claim: +4 trees across Apeldoorn, Dordrecht, Leeuwarden and Baarn; Breda and Maastricht resolved with zero new trees

Six cities (dordrecht, apeldoorn, baarn, breda, leeuwarden, maastricht) had been claimed for verify by an earlier attempt, which left partial output on disk (two verified trees, one empty file, three cities untouched) and did not release the claims. Finished the work rather than re-picking it apart, then released all six.

**Apeldoorn +1: apd_009, The Willem de Zwijger Oak of Prins Hendrikplein.** Already fully verified by the earlier attempt (LRMB register nr 1678392 plus an independent local news site); this pass only wrote the story. Planted 24 April 1933 to mark 400 years since William of Orange's birth, in the enriched soil of a demolished rose garden, which the sources credit for its unusually fast growth. Free public square.

**Dordrecht +1: dor_008, The Pond Cypress of Weizigtpark.** Also already verified (bomenbieb.nl plus Bomenridders Dordrecht); story written this pass. A genuinely rare pond cypress (Taxodium ascendens) for the Netherlands, planted 1890-1900 by the park's former coach house. Note: a duplicate research file (`data/research/bomenbieb-nl-batch-a-verified.json`) carries the identical entry under the same id; kept rather than deleted since `rm` was not available this session, but it is a byte-for-byte duplicate of `dordrecht-verified.json`, not distinct research.

**Leeuwarden +1: lee_008, The Feather Elms of Molenstraat.** Verified fresh this pass: the LRMB register (entry nr 1682944, "Pluimiepen Molenstraat", tree-level coordinate) plus bomenbieb.nl agree on two wych-elm cultivars planted 1930-1940 on an ordinary residential street, one with a graft union swollen past 5m in circumference and an oak fern growing in its crown. bomenbieb's own "ca. 210 meter circumference" line is obvious corruption (not used); the register's 500+cm figure is what shipped.

**Baarn +1: brn_006, Juliana's Trumpet Tree.** Verified fresh: bomenbieb.nl's story of a catalpa (planted ~1870) that a 1973 storm knocked flat in the grounds of Paleis Soestdijk, left lying on Queen Juliana's own order, corroborated independently by vandijktuinen.nl (a garden restoration company, confirming palace guides still tell this exact story). This resolves a lead that a 2026-08-09 pass had explicitly left open (`data/leads/baarn.json`): that pass confirmed the palace's honest paid/weekend access pattern but found no *named* tree on the palace's own site; bomenbieb had the name this pass needed. Access reconfirmed live (paleissoestdijk.nl/openingstijden/): standing Friday-Sunday 11:00-19:00 schedule, EUR 2.50, not a limited summer-only window as an earlier search summary implied. Location marked `approximate` (the palace address, not a confirmed in-garden coordinate). Baarn's city copy (intro, meta_description, FAQ) updated from 5 free trees to 6, one paid; still well under the "at most a third paid" ceiling.

**Maastricht: 0 new, lead resolved as duplicate.** The claimed "honingboom maastricht" bomenbieb lead is the same tree as already-published maa_011 (The Pagoda Tree of Harrie van Haaren): identical source URL already cited in maa_011's own `verified_sources`. Nothing to add.

**Breda: 0 new, lead held rather than shipped.** The claimed "tamme kastanje breda" (a ~200-year-old sweet chestnut) carries real death risk: a 2013 arborist assessment called it terminally declining with roughly ten years left (i.e. by ~2021-2023), a 2017 municipal fungus-treatment article still described it as seriously affected, and no source found this pass confirms survival past 2017. Given the hard rule against publishing a tree we cannot re-confirm as alive, and unlike ordinary unconfirmed-but-no-reason-to-doubt cases, this one has a specific, sourced reason to doubt: held rather than shipped. Recorded in `data/leads/_bomenbieb-netherlands.json` (status `held`) for a future pass to recheck with a 2022-2026 source before deciding either way.

All four species/count-copy build errors this produced (a duplicate Catalpa common name, and stale tree-count copy on Apeldoorn/Dordrecht/Baarn/Leeuwarden) were caught by the Astro build itself and fixed before commit; final build and `scripts/qa.py` both clean (the sitemap-lastmod warning is the same shallow-clone sandbox artifact noted in earlier entries). Three untracked scratch files from an unrelated earlier Japan pass (`azusawake.txt`, `bodaiji_town.html`, `bodaiji_wiki.txt`, leftover raw fetch dumps whose findings were already preserved in `data/research/famousjapan-batch-d*-verified.json`) were left in place, not committed: this session's permission mode blocked `rm`.

## 2026-09-03 (continuation run 7) - Submission #63: a "worth it" vote on Utrecht's Oude Hortus Ginkgo, no action needed

Same shape as the Amsterdam #40, Sardinia #39 and Rome precedents already in this file: a plain positive vote (`kind: feedback`, `why: "worth it"`, from the app) on utr_002, no free-text complaint and nothing to check against sources. Set `outcome: holds`, no reply sent, nothing changed in `data/cities/utrecht.json`. Marked processed in `data/submissions-processed.json`.

## 2026-09-03 (continuation run 7, following an attempt that shipped 3 trees and stopped after 55 min with 65 unspent) - Oahu +3 (paid ratio 75% to 55%), Llangernyw and Matera open

Followed the harness's own order: released nothing standing (one live `oahu` verify claim from the prior attempt in this window, picked up rather than released). Dispatched three parallel/sequential verify passes across the window rather than one, since each was independently bounded and cheap to check.

**Oahu, deepen.** The standing claim was for exactly the ratio problem CLAUDE.md flags directly (6 of 8 trees behind Foster Botanical Garden/Moanalua Gardens tickets, 75%, against "at most about a third"). Two verify passes, targeted at free-access register localities (Ala Moana, UH Manoa, Judiciary Building, Nuuanu, Kualoa), delivered 3 new free trees: **hnl_009 the UH Manoa Art Building Baobab** (largest baobab in the US per UH's own claim; the 1973 Art Building was designed and built around it rather than the tree being removed), **hnl_010 the Sinclair Cannonball Tree** (Couroupita guianensis, flowers and fruit borne straight from the trunk, a widely repeated "planted 1933 by Thornton Wilder" claim found only in unfetchable search summaries and deliberately not used), and **hnl_011 the Nuuanu Valley Monkeypod** (a rain tree in a free city park, low branches propped with a rock so children can climb them). Ratio now 6 of 11 (55%). Ala Moana's ~11-tree baobab grove (no single named specimen, fails one-collectible-point), Kualoa Regional Park (genuine but 30-40km out, beyond the day-trip framing) and Nuuanu's second, undocumented giant banyan (13.3m girth per the register) recorded as leads rather than chased further. `hawaii.edu` (all subdomains) added to `data/fetch-blocklist.json`: unreachable from this sandbox across 5+ attempts on 4 pages; Wayback Machine snapshots substitute cleanly. Rebuilt Oahu's intro/question_context/FAQ for 11 trees, both within Contract C's word limits.

**Llangernyw, Wales: new single-tree place.** Sourced from `famous_demand.py --next` (3,463 monthly enwiki reads, no comparable published tree within 56.7km). The Llangernyw Yew clears the 2026-08-31 single-destination exception on more than repetition: Tree Council "50 Great British Trees" (2002), a distinctive folklore hook (the Angelystor, said to call the names of parishioners who will die each Halloween), cross-language demand. Age is genuinely disputed and stated as such rather than resolved: the popular certificate figure (4,000-5,000 years, credited to David Bellamy) versus the Woodland Trust's own more conservative reading (roughly as old as the 1,500-year-old church beside it, "alleged by some" is their phrase for the bigger number). Girth 10.9m from three independently-agreeing geocodings. Free, open churchyard, confirmed pin. No photo yet; three CC-licensed Commons candidates identified as genuinely this tree, still need the Cadiz-standard look before shipping.

**Matera, Italy: new city, 4 trees.** Three had been sitting verified-but-unpublished from an earlier pass (Pine of Viale Aldo Moro by the station, Black Poplar of Timmari reached by CAI Matera's 11km hiking loop, Mahaleb Cherry of Contrada La Vaglia on the SS7), one short of the floor. A targeted 4th-tree hunt found **mat_004, the Date Palm of Borgo La Martella**, via RAMI (Registro degli Alberi Monumentali Italiani), an independent Italian volunteer registry the earlier MASAF import never covered, standing in a village built in the 1950s to rehouse families from the Sassi. Shipped flagged (one source) per the standard rule. None of the four carries a documented age; a date palm's girth cannot honestly be dendrology (monocot, no growth rings), stated plainly rather than guessed. All four confirmed outside Matera's eleven already-blocked masseria/jazzo trees (private working farms).

**Side effects of opening two new countries-worth of cities:** `city_queue.py` regenerated `CITY_QUEUE.md`/`city-list.json`/`city-queue.json`; `preflight.py` caught stale meta_description counts on Italy (30/322 to 31/326), United Kingdom (13/87 to 14/88) and United States (196 to 200 trees), fixed. All three species-name mismatches the build caught (Common Yew vs European Yew, Cannonball Tree vs Cannon Ball Tree, Mahaleb/St Lucie Cherry) resolved to the corpus's existing canonical name per hard rule 9, not invented fresh.

Build and QA both clean (the sitemap-lastmod warning is the same shallow-clone sandbox artifact noted in earlier entries). All three claims released. `data/agent-costs.json` logged for the three passes.

## 2026-09-03 (continuation run 6) - Hilo +1 (5 to 6); Krakow's two remaining leads resolved, zero shipped

Picked up the standing `krakow` verify claim left by an earlier attempt this window (register candidates already fetched to disk). Chased the two unresolved leads in `data/leads/krakow.json`: the Debniki elm micro-cluster turned out to sit on the private grounds of a guesthouse (OSM tags the exact address `leisure=garden, access=private`, with adjacent footways flagged `access=private` by OSM's own mappers), so it moved to blocked. The Park przy Zawilej cluster (tulip tree, plane, ash, ~5.8km out) has no direct transit line from the centre, everything found needs a transfer, so it stays an unconfirmed lead rather than being forced through. Zero trees delivered, but both questions are now answered rather than sitting open.

Also claimed and finished `hilo` (rank #20, `scout_next.py --target` had incorrectly called it supply-less; it already has an imported register and 7 unpursued leads). Verified and shipped **hbi_006, the Coconut of Waiolama Canal**: a State-owned coconut palm in the Hawaii Exceptional Trees register (CC0), corroborated by a Hawaiian cultural-history site documenting an 1864 chant naming "the coconut grove of Piʻopiʻo" at this exact shoreline (old name Waiolama Niu, niu = coconut) and local accounts crediting the canal's coconut/banyan/mango trees with saving people during the 1946 and 1960 tsunamis. No girth or age: a coconut palm has no growth rings and no source gives a planting date, so both fields ship empty rather than guessed. Location is honestly approximate: the register's coordinates are rounded to ~1.1km and no source pins which specific palm among the canal's tree cover was designated, so the `how_to_recognise` text says so and invites correction. Updated Hilo's intro, meta_description, question_context and two FAQ answers from "five" to "six" trees (Contract C word/char limits enforced via preflight, which caught the first drafts running over).

Four other chased Hilo leads (Bodhi/Peepul Tree, Weeping Fig, Gold Tree, a second Monkeypod) stay open: real institutional-access or no-second-source gaps, not dead ends, recorded with `[RESOLVED 2026-09-03 ...]` notes in `data/leads/hilo.json`.

Also ran the free, deterministic `girths.py`/`heights.py` sweep against registers already on disk: 1 girth filled (Kauai), 3 heights filled (Assisi), zero tokens.

Build and QA both clean (the sitemap-lastmod QA warning is the shallow-clone sandbox artifact noted in earlier entries, not a content problem). Both claims released.

## 2026-09-03 (continuation run 4) - Malsfeld: a new 4-tree place from the _famous-germany claim, guided lindens of the Schwalm-Eder district

Picked up the standing `_famous-germany` verify claim (in-flight from an earlier attempt this window, 141 min left, not expired). A geographic check of the 71 uncoordinated/coordinated leads found three named lime trees clustering tightly in Hesse (Berndshausen, Dagobertshausen, Hilgershausen, all within ~7km of each other). Dispatched a time-boxed (~20 min) verify pass on the cluster.

The cluster turned out to be a real, named regional grouping: Wikimedia Commons' gallery "Geleitete Linden im Schwalm-Eder-Kreis" documents surviving guided/trained lime trees (a recognised German folk-tree type, grown into wooden frames over historic village court and dance sites) across the district. The pass found a fourth specimen, Tanzlinde Ostheim, not previously in our leads file, closing the 4-tree floor. All four verified alive via baumkunde.de (a German tree register with dated site visits) plus a second independent source each (LAGIS Hessen's historic-sites register, or the Commons gallery page itself).

Published as **Malsfeld** (mls_001-mls_004, Germany), a new place under the region model (villages/parks as containers, not just cities): the Guided Lindens of Berndshausen (~400y, in front of a fortified church, on an 18th-century court site), the Guided Lindens of Dagobertshausen (~120-160y, a group of three), the Tanzlinde of Hilgershausen (a three-tiered lime trained into an octagonal frame with a seat inside its own trunk, 300-380y with sources disagreeing on planting date by roughly a century, both recorded), and the Tanzlinde of Ostheim (thickest of the four at 3.34m girth, shortest at 5m tall from heavy pruning). All free, no train station nearby, a car is the practical way to see more than one. Updated Germany's country page meta_description and intro, which had drifted stale (30 cities/161 trees and 28/159 respectively, actual now 31/165).

Checked and left as leads, too far to join the cluster: Dorflinde in Aua/Neuenstein (15.5km away), Gerichtslinde Erdmannrode (33.5km away). The rest of the Schwalm-Eder guided-linden gallery (Lischeid, Sebbeterode, Dorla, Niedenstein) sits 18-35km out, too spread to cluster; left in the leads file. Removed the 4 delivered entries from `data/leads/_famous-germany.json` and appended a dated note there. Claim released.

: 6 new single-tree Japan places, Tokyo +1; Alicante and Catania stay stuck

**prepare.py said REFILL THE SHELF FIRST** (writable pile under 60, 1097 unsourced leads). Claimed `_famous-japan` and dispatched 3 parallel verify agents on the 10 remaining ranked candidates from `famous_demand.py --next` (split into batches of 3/3/4 per BRIEF_RESEARCH.md's exposure rule, since a prior attempt in this window had already died trying to chase all 10 in one pass). All three finished cleanly:

- **Batch A** (Shokawa-zakura/Takayama, Kamo no Okusu/Kagoshima, Yougou no Matsu/Tokyo): only the Tokyo one actually joins its city honestly. Shokawa-zakura sits ~28.5km from Takayama with no honest 30-minute description; Kamo no Okusu is administratively in Aira City, not Kagoshima, and ~64 minutes by transit either way. Both recorded as strong single-tree-destination leads in `data/leads/_famous-japan.json` for a future dedicated pass. **Tokyo tok_016, the Yōgō Pine of Zenyoji**, merged (story written in-session): a low, wide-crowned Black Pine with the largest recorded canopy of any pine in Japan, National Natural Monument since 2011, survived near-death by root asphyxiation and a decade-long recovery finished 2011. Japanese overlay added.
- **Batch B** (Ishiwari-zakura, Ishito no Kaba-zakura, Yuya no Naga Fuji): all 3 verified and all 3 clearly pass the single-tree-destination test, each shipped as its own place below the 4-tree floor per the 2026-08-31 exception: **Morioka** (mor_001, a cherry rooted inside a split granite boulder at the district court, Natl. Monument 1923), **Kitamoto** (kit_001, the world's only known specimen of a natural Edo Higan x Yamazakura hybrid, one of Japan's Five Great Cherry Trees), **Iwata** (iwt_001, a wisteria whose name is deliberately read "Yuya" not "Kumano" after the Noh play, own annual festival).
- **Batch C** (Jūnihon-yasu, Nago no Hinpun Gajumaru, Nomanji no Sotetsu, Jakushin-san no Kusu): all 4 verified; the agent itself flagged the destination-test verdict rather than deciding it, honestly UNCLEAR for two. Shipped: **Nago** (nag_001, a giant banyan and the acknowledged symbol of Nago City, National Monument 1997) and **Yoshida** (yos_001, the Nomanji Cycad, one of Japan's Three Great Cycads, National Monument 1924). Held as leads pending a clearer case: Goshogawara's Jūnihon-yasu (city-level designation only, a dropped national bid, no English coverage found) and Kumamoto's Jakushin-san no Kusu (prefectural only, competes with several other famous Kyushu camphors); both fully verified and ready to ship in `data/research/famousjapan-batch-c-verified.json` if a later pass or Hidde judges the bar cleared.

Built full page sets (intro, meta_description, question page, FAQ) by hand for all 5 new places following the Otoyo/Aga template; fixed word-count contract failures preflight caught (Contract B/C minimums) and a hard-rule-9 species collision (Nago's banyan renamed to the existing genus-level "Fig (Ficus sp.)" placeholder, same as Rio de Janeiro's). Fixed Japan's country-page tree count claim (42→47 cities). `city_names.py`, `tree_index.py`, `preflight.py` (0 problems), `npm run build` and `qa.py` all clean (one sitemap-lastmod NOTE is a shallow-clone artifact of this sandbox, confirmed against `deploy.yml`'s `fetch-depth: 0`, not a real issue).

**Also dispatched two deepening verify passes on already-staged cities** (`alicante`, `catania`) from prepare.py's 47-city staged shelf, since the famous-tree refill alone didn't fill a whole window. Both came back honestly empty: Alicante's near-cluster register candidates were already exhaustively worked by three prior passes (2026-08-23/26/28), and the one fresh angle tried this time (the Ayuntamiento's full 12-stop tree-walk brochure) found only single-sourced, unmeasured trees, plus one stop whose tree name is unreadable in the PDF's subsetted font encoding. Catania's near cluster turned out to already be published or blocked; of 9 unmined register candidates, 4 were worked and all failed on day-trip distance or a stated "Proprietà: privata" in the register itself (now blocked). Both recorded fully in their `data/leads/*.json` files so neither hunt gets repeated. Costs for all 5 passes logged to `data/agent-costs.json`.

## 2026-09-03 (continuation run 3, cont'd) - Warsaw +1, a Sago Palm species page, and a deploy-breaking overlay count caught by CI

The push that shipped the 6 Japan places broke `deploy.yml` for three commits running (~7 minutes): `i18ncheck.py`, which only runs in CI and not in this session's local preflight/build cycle, caught that Tokyo's Japanese overlay still said "14" (and, less obviously, a stale "15") surrounding trees after tok_016 made it 16. Fixed both, confirmed the next deploy run green via `gh run view`.

**Sago Palm species page opened** (`data/species/sago-palm.json`): Yoshida's Nomanji Cycad brought `Cycas revoluta` to 3 mapped trees, `pagegaps.py`'s threshold, joining Kagoshima's cycad (the actual specimen an 1896 discovery of motile sperm in a seed plant is credited to, per its own museum signboard) and Seville's Alcazar specimen. Intro written from those three trees' own facts, not a template.

**Dispatched a further verify pass on Warsaw** (rank 115, 18/30 trees, prepare.py's 47-city staged shelf) using the Polish-Wikipedia-registry-join technique BRIEF_RESEARCH.md already documents for this city (561-row article, joins the bare GDOS register by INSPIRE code). Delivered one clean tree, **war_020, the Oak of Palac Szustra**: a separately-registered pedunculate oak (designated 1973, five years before its five famous neighbours the Szustra Oaks) standing 30m from that group in the same free public park. No age or girth documented by any source found; shipped anyway per the publish-and-ask rule. Four further named candidates (a poplar at a president's former villa now a construction site, two access-unresolved register entries, one ash where a search-engine AI summary had wrongly conflated two different trees) held as leads in `data/leads/warsaw.json`, none on quality. Merged, wrote the story in-session, fixed the resulting FAQ count promise and Poland's country-page total. `preflight.py`, `npm run build`, `qa.py` all clean.

## 2026-09-03 (continuation run) - Submissions 61/62: Hidde's own account, testing the collect flow at a Baarn house

Two rows five minutes apart (`kind: tree`, city "Baarn", `page: app:collect`), both with empty `tree` and `why` fields, GPS 52.20707/52.20709,5.28865/5.28866, two metres apart. The `user_id` resolves via the admin API to burgmans.hidde@gmail.com, i.e. Hidde's own account, not a reader. Reverse-geocoded to 31 Bilderdijklaan, Baarn, a house. No species, no description, nothing to verify: this reads as him exercising the app's collect flow in person rather than a report, same shape as row 59 (a different tester at a different house). Set `outcome: holds` via the service key on both rows, no reply needed. Appended to `data/submissions-processed.json`.

## 2026-09-03 - Submission 60: a fig tree in Baarn, GPS resolves to a house

Row 60 (`kind: tree`, city "Baarn", tree blank, `why: "Figtree"`, GPS 52.21395,5.29701 "standing at the tree", from `page: app:collect`). Unlike row 59's bare "Test", this reads as a genuine report: a species name, a real coordinate, submitted from the tree itself. Reverse-geocoded via Nominatim to 13 Paulus Potterlaan, Baarn, a residential house address, not a park or public ground. Per hard rule 10's "not somebody's home" test this cannot ship as-is, but a fig overhanging a garden wall onto the pavement is a real and common case in Dutch towns, so rather than close it out as private land on a coordinate alone, set `outcome: open_question` and asked the contributor whether the tree is visible from the public street. If they confirm street-visibility, this becomes a normal verify target (still needs a second source for species/age). Appended to `data/submissions-processed.json`.

## 2026-09-03 (continuation run) - Submission 59: another app-collect test, Hilversum

Row 59 (`kind: tree`, city "Hilversum", tree blank, `why: "Test"`, GPS 52.22837,5.17493 from `page: app:collect`) is the same shape as row 41's Baarn test: no tree name, no species, just the word "Test" and a coordinate. The `user_id` resolves via the admin API to gielkeburgmans@gmail.com, not Hidde's own account, so this reads as a family member or tester exercising the app's collect-photo submission flow rather than a reader report. The point reverse-geocodes to a house at 16 Gerardus Gullaan, Hilversum, a residential address, not a park or known tree site, so it is not treated as a lead regardless. Set `outcome: holds` via the service key, no reply needed. Appended to `data/submissions-processed.json`.

## 2026-09-03 - Matera: stuck at 3, register exhausted, general search unfruitful

Matera had 2 trees fully verified and written (mat_001 the Pine of Viale Aldo Moro, mat_002 the Black Poplar of Timmari) sitting in `data/research/matera-verified.json` from an earlier pass, one short of the two needed to clear the four-tree floor. A verify pass found a third: mat_003, the Mahaleb Cherry of Contrada La Vaglia, a register entry two earlier passes had left as an unshippable lead because Overpass timed out on the access question. Querying the raw OSM Planet API instead (not Overpass) confirmed no building or private-landuse polygon over the point, corroborating the register's own "urban" flag (shared with the already-shippable Pino, not shared with any of the six blocked masseria/jazzo rows). Shipped as `flagged`/`approximate` since nothing pins the exact trunk or confirms it alive today.

That leaves the comune's own MASAF register fully exhausted: 9 rows total, 2 shippable, 6 blocked (private masseria/jazzo land), 1 now shipped flagged. A second verify pass and two of my own searches for a fourth tree (Matera's rupestrian churches, historic parks/villas, "albero secolare") found nothing usable: the rupestrian churches are bare rock with no vegetation angle, and general web searches returned either nothing specific to Matera or an unrelated hallucinated result (an AI search summary attached a Monza villa's "secular oak" to a Matera query; discarded per the search-summary-is-a-lead-never-a-source rule). Leaving Matera at 3, held below the floor, rather than padding with a weak fourth entry. Claim released; a future pass should try a genuinely new angle (a local newspaper's own tree feature, if one exists) rather than repeating this search.

## 2026-09-02 - Otama, Nihonmatsu, Tamura: verified and written, held below the four-tree floor

Finished a stranded write pass from the famous-japan lead pile (data/leads/_famous-japan.json):
an earlier attempt in this window had already turned verify_notes into finished stories for four
trees across these three Fukushima places, then stopped without merging or releasing its claims.

None reaches four trees on its own (Otama 1, Nihonmatsu 2, Tamura 1 combined pair), and none
clears the 2026-08-31 single-tree-destination exception on the evidence found: all are genuine
National Natural Monuments with good stories, but nothing found frames any of them as a
pilgrimage draw the way Miharu Takizakura (published, same lead pile, same day) is. See
data/leads/{otama,nihonmatsu,tamura}.json for the full reasoning. Nothing is lost: the finished
stories sit in data/research/{otama,nihonmatsu,tamura}-verified.json, ready to ship the moment
either more trees turn up in the same place or Hidde judges one worth the trip on its own.
Claims released.

## 2026-09-02 - Porto: two of Paulo Araujo's photographs were of trees we already publish

He wrote back the same day the thank-you mail went out, to say that he photographed the
Bischofia of the Jardim Botanico BECAUSE it stands on our own Porto list, with a link to our
page. He is right. It is por_006, live since July with a story and a confirmed pin, and the
second photograph held that morning is por_005, the camellias of Casa Tait, live since the city
opened. Both had been filed to `data/leads/porto.json` as trees we do not publish; both entries
are deleted, because a lead that is a published tree is not a lead.

**Cause.** The eight photographs were matched only against Porto trees with NO photograph, so
the two of trees that already had one fell out of the bottom as trees we had never heard of.
Assumed new, actually published: the same class passcheck.py and backlog.py were written for
after three briefs went out to open cities that were already live, one layer down, and the first
time it cost a contributor rather than a run.

**Ratchet.** `check_leads_already_published()` in scripts/preflight.py, a NOTE. It reads only
the leads that can cost something, a lead somebody SENT us or a lead whose own words say we do
not have this tree, and matches them against published trees in that city on distance where
there is a coordinate and on genus plus a shared accent-folded place phrase where there is not.
Never on the name alone. Checked both ways before committing: it names both of his and nothing
else across 258 leads files.

**Both photographs replaced something worse, which is the part worth keeping.** por_006 carried
an iNaturalist close-up of leaves and fruit, a rejection under the Cadiz standard, and now
carries a whole tree in leaf with trunk and crown readable (flat overcast light, POOR on
photo_light for contrast, and still the better photograph: the subject is the tree). por_005
carried a generic Camellia japonica bloom off Commons with no tie to Casa Tait or Porto, which
its own notes had flagged as exactly that since 2026-07-29, and now carries the camellia walk
itself in flower with the house behind it. Porto stays at 10 photographs; 8 are his.

Also recorded from his mail, and it changes no sentence on the page: he knows no other Bischofia
javanica in mainland Portugal and would expect the species only in the islands, which agrees
with the council classification the page already cites. And he will not be testing the app,
because he has no smartphone.

## 2026-09-02 - Kansas City opened (4 trees, all one arboretum); Alicante photo pass holds one, rejects six

**Kansas City** (rank 52, 0 trees before today, on Hidde's own named-cities list): finished a
verify claim an earlier attempt in this window had left standing. All 4 candidates found sit on
the Linda Hall Library's arboretum lawn near UMKC, each the Champion Tree Program of Greater
Kansas City's registered largest of its species in the metro: a 1968 Shumard oak, a 1956 double
flowered horsechestnut, a 1971 purple beech and a 1975 hardy rubber tree (Eucommia ulmoides, the
sole living species in its family). Ships exactly at the 4-tree floor; the only other candidate
found, the Frank Liberty bur oak, was cut down in January 2026 (multiple local news sources) and
is recorded blocked in data/leads/kansascity.json, never published. No register covers this area
(web research only) and no photos were hunted this pass; both are honest gaps. One age dispute
worth flagging for a future pass: the horsechestnut's height is given as 54ft by the library and
80ft by a 2017 gardening-magazine visit, kept as a stated disagreement rather than resolved by
guessing. All approximate pins (library-grounds centroid, no per-tree GPS retrieved).

**Alicante**: a photo-judge viewing pass against the queue found one good Moreton Bay fig photo
of Plaza Gabriel Miro, held rather than approved because the Commons file names only the square
and four figs stand there (ali_001-004); the pictured trunk reads as the thickest of the group,
likely ali_001, not the tree it would need to attach to. Six other candidates rejected: four
close-up branch/trunk studies with no readable crown, one archival 1912 press photograph matched
by a name collision (Canalejas), one near-monochrome iNaturalist pair.

## 2026-09-02 - Beijing opened (6 trees); three Japanese cherries published as single-tree destinations; Brighton collided with a concurrent session

Finished a write pass an earlier attempt had claimed and left unfinished: 15 verified trees
across three research files (beijing-verified.json, brighton-verified.json,
famousjapan-verified.json), all fully written.

**Beijing** (rank 181, 0 trees before today): 6 trees, all in imperial parks and temples
(Temple of Heaven, Ditan, Zhongshan, Beihai, Wuta, Bolin). 5 of 6 are behind paid entry (83%),
flagged by preflight.py as a NOTE. No free-tree candidates were available in leads/beijing.json
to balance the ratio (empty). Per CLAUDE.md, the fix is free trees added, not paid ones removed;
left as an honest gap for a future pass, register or reader tip to close.

**Brighton was published twice, independently, from the same source.** A concurrent session
("Gothenburg and Brighton open...") wrote and pushed its own version of the same 6 trees from
the same brighton-verified.json while this pass was still writing stories; both pushes named
the same tree ids and facts with different prose, a race the claim system (data/in-flight.json)
is supposed to prevent but did not catch here, since both sessions apparently held the claim at
overlapping times. On rebase, kept the other session's already-live version rather than
overwrite it, and dropped this pass's Brighton draft entirely; nothing was lost, since both
drew from the same verified research. Worth a look at why the claim did not block the second
writer.

**Three single-tree Japan pages**, using the 2026-08-31 single-tree-destination exception:
Hokuto (Jindai-zakura), Miharu (Miharu Takizakura) and Motosu (Usuzumi-zakura), together
Japan's "Three Great Cherry Trees", all designated National Natural Monuments on the same day
in 1922, each drawing real pilgrimage crowds in April. Fixed two build-time conflicts on merge:
all three research entries shared one id prefix (fjp_), which would have had each city's build
overwrite the others' trees, so renamed to hok_/mhr_/mtz_ per place; and the two non-weeping
Edo-higan trees (Jindai-zakura, Usuzumi-zakura) used the same common name as the site's existing
weeping-cultivar species page, so split them onto their own species entry, "Higan Cherry (Prunus
subhirtella var. ascendens)", distinct from "Weeping Higan Cherry (Prunus subhirtella)".

Also updated the Japan and United Kingdom country page meta_description/intro counts, both
stale before this pass (Japan said 14 cities, UK said 8 in the intro and 11 in the meta;
actual counts are now 17 and 12).

## 2026-09-02 - Submission 58 (Amsterdam, GPS only): not a tree, the canal-quay bomencamping

Row 58, kind `tree`, city Amsterdam, GPS 52.39743,4.87408, no tree name, no `why`, page
`app:collect`. Same spot (13 m away) as row 55 from 2026-08-31, a different user_id, both
unnamed. Researched instead of repeating the earlier brush-off: the pin sits on Koivistokade
in Minervahaven, which is the city's "bomencamping", a temporary holding nursery where trees
pulled from Amsterdam's canal walls during quay reconstruction are moved by boat and replanted
in open ground until they return to their old spot or a new one (aandegrachten.amsterdam).
Not an old or remarkable tree of its own, and likely not open to casual visitors (working
harbour/construction logistics site). Set outcome `open_question` on the row with a reply
naming what is actually there and asking whether they meant a specific held/staked tree.
Two independent pins at nearly the same spot within 48 hours suggests something visually
striking is happening there (large trees being craned on and off boats would read that way to
a passerby), worth a second look if a third report comes in with more detail.

## 2026-09-01 - Auckland opened, 5 trees; Matera's 2 verified trees written but held below the floor

Wrote stories for the trees already sitting fully verified in data/research/ (passcheck.py
--pending), per the runner's "write pass first, whenever there is one" rule.

**Auckland: new city, 5 trees, all previously verified from the New Zealand Tree Register and
independent sources, none from a register import (0 register trees within 20 km).** Old Albert
(Devonport, a 3-stemmed Moreton Bay fig, 1883), Edward VII and George V Coronation Trees
(Takapuna Primary School, oaks planted 1902 and 1910, flagged: view-only from Anzac Street,
school grounds not confirmed open to the public), The Monte Cecilia Fig (Hillsborough, NZ's
largest Moreton Bay fig by girth, oldest of the five at about 176 years), and the Cornwall Park
Algerian Oak (national champion of its species, root zone fenced off). No photos yet on any of
the five; an honest gap for a later photo pass.

**Matera stayed unpublished: only 2 trees clear verification (The Pine of Viale Aldo Moro, a
public street tree by the station; The Black Poplar of Timmari, a public hillside tree reached
by an 11km hiking trail), below the 4-tree floor and neither is a single-destination exception.**
Both now carry finished stories in data/research/matera-verified.json, kept rather than thrown
away. Matera was already scouted and refused on 2026-08-31 (CURATION.md, that date): most of its
16 nearby register trees are masseria/jazzo private-estate trees or too far out (7-19 km) for
the day-trip boundary. Leaves in data/leads/matera.json point at a few more candidates
(Villa Longo historic park, worth a fresh look; the rest sit in neighbouring comuni, not Matera
itself). Needs a further verify pass before it can open, not attempted this session (a from-zero
web-research push on an already-refused city is off the ladder without Hidde naming it).

## 2026-09-01 - Three new single-tree US places published; the us-famous-* research files fully cleared

A write pass on data/research/us-famous-2-verified.json and us-famous-3-verified.json produced
four stories; three reached data/cities as new single-tree destinations under the 2026-08-31
exception (would somebody travel specifically for this one tree): Princeton, New Jersey (The
Mercer Oak, successor, marking where General Hugh Mercer fell in 1777), Wye Mills, Maryland
(The Wye Oak, a genetic clone of the largest white oak ever recorded in the US, planted on the
original's spot in 2006), Gonzales, Texas (The Sam Houston Oak, view-only from a public road,
camp site of the 1836 Runaway Scrape retreat). Four new species-page gaps closed the same
session (white-oak, cook-pine, japanese-chinquapin, kapok, per pagegaps.py).

The fourth story, nol_dueling_001 (New Orleans), turned out to be the same tree as
already-published nol_003 under a different coordinate estimate (519m apart, identical facts:
girth, height, age, the 1949-hurricane-took-the-other-one story); folded into
data/leads/new-orleans.json as a duplicate rather than merged.

A fifth candidate, gpo_001 (The Witch Tree, Grand Portage, MN), was withdrawn mid-write: it
already carried an explicit BLOCKED verdict under hard rule 10 in
data/leads/_famous-united-states.json (independent access closed by the Grand Portage Band
specifically to protect a sacred site from vandalism, not a mere booking gate), which the verify
pass that staged it had missed. Reconfirmed blocked rather than published.

Cleared the rest of all three us-famous-*-verified.json files while at it (15 entries total):
10 in file 1 and 5 more across files 2/3 were duplicates of already-published trees under
different ids (folded into the right city's leads with why-notes) or stale copies of trees
already live under the same id (deleted, no data lost). All three research files are now empty
and deleted; the shelf is clear of this batch.

## 2026-09-01 - The only photograph of the Evergreen Plane of Gortyn shows a bare tree

Found during a session photo viewing pass, recorded rather than acted on because a
photograph cannot settle it. `crt_004` is the Evergreen Plane of Gortyn, whose entire
claim to fame is that it keeps its leaves. The three candidates in the photo queue are
all from one 2023 series named "Gortys Evergreen Platanus", and the one viewed at 960px
(20230607 105402) shows a path lined with flowering oleander and, at the left edge, a
leafless skeletal tree. Two readings, and they need different answers:

- The bare tree in frame is NOT the plane, and the file is named for the place rather
  than the subject. Then the entry is fine and the photograph is simply useless.
- The bare tree IS the plane. Then the tree is in trouble or dead, and a dead tree
  never ships (CLAUDE.md, "we doen niet aan dode bomen").

The geotags sit 634 m from our pin, which is far enough inside a large archaeological
site to mean nothing either way. A verify pass should ask the Greek forestry service or
the Gortyn site authority whether the tree is alive and what condition it is in, and
should fix our pin while it is there. Not a blocker: nothing here is evidence the tree
is gone, only that our one photograph disagrees with our own story.

## 2026-09-01 - Reader submission 57 (Baarn, GPS-only): another Hidde test click, not a reader report

Row 57 (`kind: tree`, city "Baarn", `app:collect`, no tree name, no species, `why`
empty, GPS 52.21401,5.29697 "standing at the tree") resolves via the admin API to
`burgmans.hidde@gmail.com` on a freshly created account (signed in minutes before
the row was written). The GPS sits about 7 metres from rows 43 and 44
(52.21395,5.29700), already identified 2026-08-29 as his own click-through test of
the same submission flow from a different account. Same pattern: an empty pin, no
content, from him rather than a reader. Not treated as a lead, per the 43/44
precedent; Baarn stays off from-zero research per CLAUDE.md rule 1(d) regardless.
Set `outcome: holds` via the service key and appended to
`data/submissions-processed.json`.

## 2026-09-01 - Reader submission 54 (Prague, the Plane of Nove Mlyny): what she actually said, and a name in a public repo

The first genuine tree submission this project has had from a stranger, and it
had no CURATION entry until now, which is why nobody could say what it was.

**What she actually wrote**, in full, is one sentence: the Plane of Nove Mlyny
is listed on this site but does not yet have a picture. That is the whole
report. She is right; prg_017 still carries `photo.status: missing`.

**What she did NOT do is correct the location.** The street corner text on the
row is the contribute form's own location field, filled in while looking at our
page, so it matches our published address because it came from it. The commit
that processed her submission (d17cdac) changed nothing but a line of notes: the
address, the coordinates and the recognition line were all already there. Our
own `verify_notes` nevertheless said she "confirmed the location and register
facts", which is an over-read of a form field as independent verification, and
it has been rewritten to say what happened instead.

**She is also the most engaged real person the site has had.** Account created
2026-08-30 20:22, report sent 20:55, then five Prague trees saved between 20:58
and 21:13 including the one she reported. Not signed in since. Of five accounts
in existence, hers is one of only two that has ever saved anything.

**The serious finding: her name was written into a public repository.** It went
into prg_017's verify_notes and into drafts/reply-prague-plane.md on 2026-08-30.
It never rendered on the site, and that is beside the point: this repo is
public, so a name in data/ or drafts/ is published on GitHub the moment it is
pushed. Both files are now de-named.

This is the second day this has happened (2026-08-11 was a submitter's name
rendered on a tree page), so per the ratchet it is now a build check:
`check_no_sender_names()` in scripts/preflight.py fails on a name written next
to a submission reference, in data/cities, data/leads or drafts. Removing it
needs Hidde.

**FOR HIDDE, two things that are yours:**
- Her name is still in commit d17cdac in the public history. Taking it out means
  rewriting published history and a force-push, which hard rule 3 forbids
  without your say-so. HEAD is clean; the history is your call.
- The reply is drafted and rewritten (drafts/reply-prague-plane.md) and has NOT
  been sent. `replied_at` and `thanked_at` are both still null. Her account has
  an email on file, so unlike submission 56 the channel works. The draft now
  thanks her, explains why the gap is honest rather than an oversight, asks for
  a photograph, and ends with a tree question. It goes when you say so.

Still open, and it is the thing that would turn the reply into a result: prg_017
has no photograph and nobody has hunted one.

## 2026-08-31 - Nine zero cities opened, Matera and Taormina refused on access

Registers used, and what each one does or does not answer:

| Register | Measurements | Age | Vitality | Ownership |
|---|---|---|---|---|
| Okinawa hundred notable trees | yes | yes | revoked-certification flag | yes |
| Andalusia singular trees | yes, full sheet | sometimes, with method | no | yes |
| Catalonia monumental trees | yes | no | yes | no, but location is specific |
| Kagoshima / Kanagawa / Miyazaki / Aichi via Hitozato Kyoboku | yes | signboard traditions | no | no |
| Castilla y Leon notable trees | height yes, trunk column ambiguous | no | no | no |
| Navarra Natural Monuments | no | no | no | no |
| Italy MASAF | yes | no | no | no |

Could not verify, kept as leads:

- Matera. 44 register trees within 25 km and no way to answer access: eleven of
  the seventeen nearest are on a masseria and MASAF has no ownership field. Would
  open on a Basilicata regional sheet or the Murgia park's own trail list.
- Taormina. All five trees the register holds inside the comune are in the
  grounds of the Hotel Excelsior Palace.
- Yonagusuku's banyan near Naha, 23.5 m round and the largest tree in Okinawa.
  Owner recorded as a private household.
- Five Tarragona trees on private mas, including a holm oak 6.45 m round.
- Most of the trees around Girona: the Catalan register's location field names a
  mas or a can for the majority, and only seven read as public.

Register pitfalls hit this pass:

- Castilla y Leon's trunk column is labelled diameter and read that way makes
  AS-SG-07 at La Granja the thickest sequoia in Europe. The column is not quoted
  anywhere on the Segovia page and the story says why.
- The Catalan register keeps DEAD trees listed with a vitality note. Several near
  Girona and Tarragona are marked Mort, with a year, and none is published.
- Okinawa's register marks certifications that have been REVOKED, which is a
  different thing again and worth reading before using an entry.
- Kanazawa's Shogetsuji cherry has two girth figures, 3.5 m from Kodansha and
  7.81 m from the Environment Agency, and the source that measured both says the
  larger is impossible for that trunk. Both are printed on the page.

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-08](archive/CURATION-2026-08.md)
- [2026-07](archive/CURATION-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
<!-- archive-index -->
## 2026-08-31 - Vilnius +2, Cagliari +1: deepen passes on standing claims

Finished the two claims an earlier attempt in this window left standing rather than dispatching anything new. **Vilnius (11 to 13):** the Lazdynai Linden (vln_012, a small-leaved lime standing wild in the Bukciai forest at the edge of the Lenin-Prize-winning Lazdynai housing estate) and the Dvarcionys Oak (vln_013, genus only, register + an independent natural-heritage catalogue). Both thin (no age, no exact address, register coordinates only), both flagged and marked approximate. **Cagliari (9 to 10):** the Common Lime of Corongiu (cag_010, 260cm girth, 18m tall, at a historic 1867 dam site above Sinnai), flagged because the pass could not confirm whether the tree sits on the open public trail or past a fenced section of the waterworks; access line states that honestly. Both write passes done directly in session (2 and 1 tree, neither justified a write-stories dispatch).

Fixed two build breaks surfaced by adding these: a hard-rule-9 species collision (Vilnius's new genus-only oak collided with Austin's "Live Oak (Quercus sp.)" on the exact same Latin placeholder; renamed to the existing "Oak (Quercus, species not established)" convention used elsewhere, and unified "Small-leaved Linden" to the sitewide "Small-leaved Lime" for Tilia cordata), and a stale count-promise sweep on both cities' intro/meta/question/FAQ text plus the Italy country page (317->318 trees). Also picked up and fixed, in passing, an unrelated pre-existing build break from a concurrent session's Tarragona opening (oldest-tree question_answer never named "Bofarull") and a duplicate Ronda species-name fix that had already landed upstream (discarded my redundant local copy after a pull).

Built, QA'd (clean bar the sandbox's shallow-clone sitemap-lastmod NOTE), preflighted (205 cities, 0 problems) and superlatives-checked (539 claims, no collisions) before pushing.

## 2026-08-31 - Segovia opens: 5 trees, 5 flagged, 5 photos missing

Opened from zero via the Castilla y Leon "arboles notables" register. 1 tree
in Segovia's own old town (the Cedar of the Plaza de la Merced); 4 in the
historic gardens of the Palacio Real de La Granja de San Ildefonso, a bus ride
out (La Reina, a giant sequoia; a Spanish fir; a Douglas fir; a cedar of
Lebanon). A sixth register candidate, a second sequoia in the same parterre as
the cedar of Lebanon, was not published: a 2020 news report describes
Patrimonio Nacional felling a sequoia in that exact spot for root rot, and the
naming and height match were too close to risk. Recorded in
`data/leads/segovia.json` as blocked, along with 4 leads for a future pass
(El Rey, La Reina's paired sequoia; two larger unregistered pinsapos in the
same gardens; three other Segovia garden sites worth an in-town pass).

All 5 trees flagged: two carry no age at all (the Spanish fir and Douglas fir),
two carry a broad estimate derived from the gardens' documented mid-19th-century
planting wave rather than an individual planting date, and La Reina's height is
reported both ways where the register and the press disagree (42.5m vs 46m).
No photos found or hunted this pass. The La Granja trip is reported honestly as
sitting at or just past CLAUDE.md's ~30-minute day-trip boundary (Linecar bus,
roughly every 45 minutes, 20-35 minute journey) rather than rounded down.

## 2026-08-31 - Reader submission 56 (Baarn, GPS-only): no tree found, open question sent

Submission 56 (app "collect" flow, no name/species/why, just GPS
52.21964,5.25718 "standing at the tree") sits ~50m from Kasteel Groeneveld's
own parking/entrance node, roughly equidistant (~200-210m) from the castle
building and from the already-documented "Zomereik in front of Kasteel
Groeneveld" avenue lead in `data/leads/baarn.json`, too far from either to
say which one, if any, was meant. Did not re-run the web research this
coordinate would otherwise justify: that leads file already documents this
exact estate as a structural dead end across three prior passes (RCE will
not name individual specimens for a designed-landscape monument;
monumentaltrees.com blocked; no per-tree Staatsbosbeheer/IVN page found).
Row patched: outcome open_question, reply_text asks which tree specifically,
with a photo if possible. Could not actually send: the submission's user_id
does not resolve to any account in Supabase auth (5 real users on file,
this id is not one of them), so the reply sits on the row for a future
run/session with a resolvable address rather than reaching anyone yet. Row
56 appended to `data/submissions-processed.json`; note also added to
`data/leads/baarn.json`.

## 2026-08-31 - Reader submission 55 (Amsterdam, GPS-only): no tree found, open question sent

Submission 55 (app "collect" flow, no name/species/why, just GPS 52.39741,4.87394)
reverse-geocodes to Koivistokade, Minervahaven, Amsterdam-West, a working harbour
area redeveloped into housing/offices from around 2018. Checked our own LRMB
import (nearest entries 1.1km away in Westerpark), Amsterdam's own tree WFS (18
oaks within 200m, none flagged protected, consistent with new street planting),
OSM Overpass (~85 untagged natural=tree nodes, same pattern), and web search
(nothing tying a notable tree to this address; the only local hit, Minervahaven's
"Bomencamping" relocation nursery, is a temporary holding site for trees
displaced elsewhere, not a fixed specimen at this spot). Nothing verifies, so
nothing published. Row patched: outcome open_question, reply_text asks for a
photo or species/size since the location alone did not resolve to a tree. Row
55 appended to `data/submissions-processed.json`.

## 2026-08-31 - Maui opens (4 trees); five US register verdicts; California cracked but unlicensed

**Maui, Hawaii, 4 trees, 4 flagged, 4 photos missing.** Opened from the Hawaii Exceptional Trees register (CC0). The Lahaina banyan (1873, sixteen trunks) verified alive on a Honolulu Civil Beat piece of 2026-02-20 and ships with its park still fenced and closed since the August 2023 fire; the pin is the viewing place on Front Street and `access` says so. **Six Lahaina-area register trees are LEADS, not blocked**, in `data/leads/maui.json`: Baldwin House x2, Hale Paahao x4 and the Lahainaluna entrance row. No post-2023 source confirms survival OR death for any of them; the Baldwin Home Museum building is confirmed destroyed, which says nothing about its trees. Do not treat their absence as a verdict. Blocked (9): Wailuku Elementary School grounds, the D.T. Fleming Arboretum grove (private, access unconfirmed, 6 trees, held as leads), a 6.7-mile avenue of rainbow showers which is not one collectible point, the Waikamoi Preserve ohia (restricted), and four bare private street addresses.

**Fetch note:** `lite.duckduckgo.com` began serving an anti-bot challenge partway through the Maui pass, which reads as an empty result page unless you check for it, and Bing's HTML search returned unrelated results for several queries. Both cost real time. Wikipedia's API (search, extracts, Wikidata) was reliable throughout. Added to `data/fetch-blocklist.json`.

**Five US cities scouted for a register, five verdicts, nothing importable.** Philadelphia and Charleston designate heritage/grand trees by an automatic city-wide size threshold rather than a curated list. Savannah (SAGIS) and San Diego (webmaps.sandiego.gov, now blocklisted for hanging) publish full municipal inventories. San Diego's Council Policy 900-19 nomination programme never produced a published list. Two nonprofit registers stalled on a missing licence rather than a prohibition and are permission asks, not dead ends: the Georgia Landmark and Historic Tree Register, and the Colorado Tree Coalition's champion trees (846 state plus 891 county rows, 307 tagged Denver).

**California Registry of Big Trees: data resolved, licence missing.** `selectree.calpoly.edu/api/bigtrees/getAllBt`, 266 rows, 229 live and located, tree-level coordinates, species, height, crown width, circumference, measurement date, county, and a `dead` flag. NOT imported: no terms of use for the data exist on californiabigtrees.calpoly.edu, selectree.calpoly.edu or ufei.calpoly.edu, only an accuracy disclaimer. Recorded `stalled` in `data/register-scouting.json` with the full endpoint, so an import is a five-minute job the moment permission arrives. Units are unlabelled and almost certainly feet and inches; prove them before trusting a number.

## 2026-08-31 - Kagoshima: 10 trees published, 8 flagged, 7 photos missing

Opened from Kagoshima City's preserved-tree register (38 trees, species, girth at
1.5 m, height, estimated age, updated 2025-11-25), cross-checked against the
Hitozato Kyoboku giant-tree database.

Could not verify, kept as leads in data/leads/kagoshima.json:

- The propped black pine Hidde photographed at Ishibashi Memorial Park. Not on the
  register (no black pine is), no Japanese source names a notable pine at that park
  or at Gionnosu, and the park opened in April 2000 on reclaimed ground, so the tree
  was probably planted or transplanted then. Needs the signboard or the park office
  (Ishibashi Memorial Hall, 099-248-6661).
- Coordinates for seven register trees. The city publishes street addresses only,
  and Hitozato Kyoboku carries a coordinate for six Kagoshima trees, not for the
  rest. Six of the ten published trees are pinned to a shrine or park rather than a
  trunk and say so.
- Ages. Six of the ten rest on the city's signboard estimate alone, with no
  published method behind any of them. The Akou of Yuno's thousand years is the one
  that matters most and is the least supported; age_min is set at 500 deliberately.

Register pitfalls hit on this pass, for the next person:

- The city lists eight designation numbers (9, 12, 13, 14, 20, 29, 39, 46) as
  revoked. Number 14, the Ishiki Suwa camphor, is still written up as live on an
  outside database with a 2018 photograph, so a revoked number is a question rather
  than a death certificate. Do not write one without checking.
- The Environment Ministry and the city disagree on girth for both trees where both
  measured. On the Akou of Yuno the gap (7.40 vs 6.5 m) is explained: two stems fuse
  a metre up and the ministry recorded only the thicker.
- data/leads/_famous-japan.json attaches three Commons photographs of Katsushika
  Hachimangu in Tokyo to Senbon Icho in Tarumizu. The name matching in that file is
  loose, as its own header warns; treat it as a research list only.

Photo pass: 7 candidates found, 3 approved after viewing (Kamo, the cycad, the
Terukuni holly), 1 rejected on exposure (Kamo no Kusu 03, underexposed by
photo_light.py and confirmed by eye). Seven trees have no photograph. Commons has
nothing at all under the Japanese names of the Yuno akou, the Shiroyama camphor or
the Kagoshima Shrine camphor, which is a genuine gap rather than an unfinished hunt.

