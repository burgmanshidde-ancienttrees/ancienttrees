


**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-08](archive/CURATION-2026-08.md)
- [2026-07](archive/CURATION-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-09](archive/CURATION-2026-09.md)
- [2026-08](archive/CURATION-2026-08.md)
- [2026-07](archive/CURATION-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
<!-- archive-index -->
## 2026-09-18 (photo viewing pass) - Milan's plane approved; Arnhem's photo queue is now an honest, documented dead end

20 shortlist rows judged, 49 candidate verdicts written, 1 approved.

**mil_002, Platano di Indro: approved.** The file had been rejected the day
before on its EXIF geotag (328 m away, in a garden with several large
planes). That geotag is rounded to one decimal and is not the tree. The file
is the P18 image of Wikidata Q55741802, a *pianta monumentale* whose own
coordinate sits 14 m from our confirmed pin, with the next registered plane
260 m off. Viewed: a veteran plane, fluted trunk filling the frame, opening
into the five-limb vase our recognition line describes. Bare (March), a
tiebreaker with no leafy alternative on offer.

**Arnhem is exhausted for these ten trees and the reason is worth recording
rather than rediscovering.** Its queue is dominated by one prolific local
photographer's FUNGUS series: oyster mushrooms and beefsteak brackets
photographed on chestnuts and beeches along Zijpendaalseweg and in Park
Angerenstein. The filenames name a host tree species and a street, so they
score well on a filename match and are photographs of mushrooms. Beside them
sit house facades, a wall poem, stained glass, a 1954 relief, an 1850s
print, 1961 Rijksdienst building surveys, a 1900 photochrome, and a
gatekeeper sculpture in Zaltbommel that matched on the tree's name "De
Poortwachters". Ten Arnhem trees were offered and none had a photograph of
itself anywhere in the queue. Nobody has photographed these trunks; the
medicine is a reader or a new source, not another sweep.

**Singapore sgp_020, sgp_023 and sgp_024: all three were offered frames of
the same tree, and it is a fourth tree we already publish.** Every remaining
candidate came from one 2024-02-10 shoot in Commons' "Tembusu tree at Lawn
E" category, i.e. sgp_001, offered as a Teak, a Temak and a Snake Tree.

**Prague and Berlin were on the list by mistake and the mistake is fixed.**
prg_013, prg_022, prg_023, prg_025, ber_028, ber_032 and arn_001 all had
approved photographs already; the shortlist filters cities, not trees, so
they were served their own shoot's second frames as "what to view next".
Because `photo_apply.py`'s approve overwrites `tree["photo"]`, that list
could have replaced a judged lead photograph with an unjudged sibling.
`photo_gaps.py` now skips a tree that carries a photograph, and skips a
duplicate candidate row whose url was judged on another row of the same
tree. The shortlist went from 4 cities to 16.

**`photo_light.py` is unavailable in this sandbox** (no Pillow, install not
permitted), so exposure was judged by eye. Worth having on the image for any
borderline-light candidate.

## 2026-09-18 (session 11) - Finished an earlier attempt's uncommitted work: two single-tree place pages, two more register giants for Higashi-Hiroshima

Resumed an earlier attempt in this window that had stopped after 23
minutes with 97 minutes of budget left, having shipped nothing to a
commit despite the work being done. All of it verified clean and is now
live.

**Two new single-famous-tree place pages from `data/leads/_famous-spain.json`, published under the 2026-08-31 exception (would somebody travel specifically for THIS ONE TREE).** `data/cities/guernica.json` (grk_001, Gernikako Arbola): the standing oak is young, planted 2015, fifth in a documented dynasty; the page says so plainly and the destination is the ground itself, where Basque self-government was sworn for centuries and where the third tree survived the 1937 bombing a few dozen metres away. `data/cities/valentin-tineo.json` (cbv_001, Carbayon de Valentin): documented in writing before 1492, generally held to be the oldest oak in Asturias, a 10-metre girth flagged in the prose as likely measured at the swollen base rather than chest height. Both flagged (single-sourced age ranges), both `location_precision: confirmed`, both no photo. Marked resolved in `_famous-spain.json` with pointers to the published ids so a future famous-tree pass does not re-surface them.

**Two more register giants added to the already-published `higashi-hiroshima.json`, taking it from 17 to 19 trees**: hgh_018 (the Ginkgo of Genko-ji, Kurose-cho, 3.16m girth) and hgh_019 (the Black Pine of Tokuzen-ji, Toyosaka-cho, 3.30m girth), both registry-only (Ministry of Environment giant-tree survey, 2000) with no second source naming the specific tree, both flagged for that reason, both `location_precision: approximate` since the register's own coordinate resolves to the temple site rather than the trunk. Updated the city's count promises (intro, meta_description, question_context) from seventeen to nineteen; `check_count_promises` and the rest of preflight/qa stayed clean. Released the standing `higashi-hiroshima` claim.

Local `npx astro build` (12,035 pages), `preflight.py` (0 problems) and `qa.py` (15,963 pages) all ran clean before committing.

## 2026-09-18 Pamplona is our best-placed page and our thinnest

Search Console's newest ten days put /pamplona at average position 3.6 on 412
impressions, the best placement any city page has, and it took 5 clicks
(index 0.13, the worst on the site). The page explains why: 14 trees, ONE of
which carries an age, not one photograph, and seven black poplars among them,
two of which are "The Poplar of Villava (south)" and "(north)". That is a
register dump wearing a city page's title, and the demand for it already
exists, which is the rare and expensive half.

Six of the poplars carry a girth (471, 393, 377, 314, 314, 314 cm) and no age.
scripts/ages.py refuses all six because Populus nigra is outside its published
rate table, so the ages are one sourced growth rate away from being free.

The work, in order, whenever a window can take it:
1. Fold the Villava twins, and check Erripagana and Zabaldika for the same
   (the Setubal twin rule: a register counts two trunks, a visitor sees one).
2. A sourced girth-increment rate for Populus nigra and Platanus x acerifolia
   into scripts/ages.py, which unblocks 24 trees site-wide, six of them here.
3. Photographs: 0 of 14, and the city clears both the five-tree floor and the
   demand rule, so it belongs at the top of photo_gaps.py --shortlist.

The meta description was rewritten today: it led with "Fourteen trees near
Pamplona" and ended on "eight riverside poplars along the Arga", which sells
the weakest thing on the page in the one line a searcher reads. It now leads
with the palace sequoia and the oak Navarra calls millenary.

## 2026-09-18 (continuation 2) - Finished the standing `_famous-japan` write claim: 4 trees join existing cities, 3 new single-tree places, 4 more duplicates found and folded into leads

An earlier attempt this window stopped after 11 minutes having shipped
nothing, with a `_famous-japan` verify claim already standing from a prior
run. Picked that claim up rather than starting fresh research: 4 verified
batch files (`_famous-japan-batch-{a,b,c,d}-verified.json`, 17 candidates
total) were sitting on disk with no story pass ever dispatched.

**Before dispatching a write pass, a distance sweep against the full
published set (not just each candidate's likely container city) found 7
more duplicates than the original verify pass caught**, all on approximate
pins 12m to 22.7km from a match, which is why they slipped past a
50m-only check: The Great Ginkgo of Jonichiji = `him_002` (Himi), The Great
Camphor of Kozaki = `kzk_001` (Kozaki), The Great Zelkova Pair of Negoya
Shrine = `hok_004` (Hokuto), Nento-Hiramatsu = `ihy_001` (Iheya),
Sentsuzan no Ichii = `ntt_001` (Nichinan, Tottori), The Umbrella Cedar of
Horaiji = `hrj_001` "Kasa sugi" (Horaiji, same Japanese word for umbrella
cedar), Nezu no ki of Horaiji = `hrj_002` (same name, same city), and The
Great Cherry Tree of Isshingyo = `msa_001` Isshingyo-no-Ozakura (Minamiaso,
same story down to the 2004 typhoon damage and the spring 2026 closure).
All 8 folded into `data/leads/_famous-japan.json` as duplicates. 2 more
real, sourced trees (Mineyama Jinya Enoki, Sawatari no Kaya no Ki) were
held as leads rather than published alone: both carry only local/town-level
recognition with no festival, pilgrimage or record-holder claim, so neither
clearly clears the single-tree-destination bar.

That left 7 genuinely new trees for a write pass (dispatched to
write-stories, ~46k tokens, 0 wasted): **Daio-sugi** joined Yakushima as
`yak_002` (the island's second-largest yakusugi, on the Jomon Sugi trail),
**The Camphor Tree of Hongo Yumicho** joined Tokyo as `tok_022` (Bunkyo
Ward's largest tree, on an ordinary street), **The Weeping Cherry of
Kega-kuyoto** joined Iida as `iid_002` (2.85km from the existing Yasutomi
Cherry), and **Shidare Katsura of Ryugen-ji** joined Morioka as `mor_002`
(12km out, a National Natural Monument regrown from an 1824 stump). Three
became new single-tree places under the 2026-08-31 exception: **Gifu**
(`gif_001`, Chujohime Seigan Zakura, the only known specimen of a rare
double-flowered cherry cultivar, seeds once flown to the ISS), **Ibigawa**
(`ibg_001`, Ibi Nido-zakura, a two-stage-flowering cherry regrown twice
after an 1833 storm and a 1934 death), and **Chikubushima** (`chk_001`,
The Mochi Tree of Hogon-ji, planted 1602 beside a National Treasure gate
moved from Hideyoshi's Osaka Castle, reached only by scheduled ferry).

Updated the 4 grown cities' intro/meta/FAQ/question fields to stop
promising one tree where there are now two (Iida, Morioka) and fixed 2
species-name drift issues preflight caught (a verify pass's "Japanese Cedar
/ Yakusugi" and "Weeping Cherry" needed folding into this site's one
canonical name per species, "Japanese Cedar" and "Cherry"). Two new ja
overlays (tokyo, yakushima) needed the new trees translated to keep the
build green; dispatched to a translate pass.

Logged the write-stories cost to `data/agent-costs.json`. Ran
`scripts/city_names.py` for the 3 new places, `scripts/city_queue.py` to
regenerate `data/city-list.json`, and `scripts/preflight.py` /
`scripts/superlatives.py` clean beyond the translation gap.
## 2026-09-18 - Slovakia's 9 cold famous-tree leads verified; 3 held famouspoland trees given a container decision

Claimed and verified `_famous-slovakia`'s 9 leads that had never been looked
at (the rest of that file's 63 leads already carried a `note_verify` from an
earlier pass). 3 verified: **kos_001, The White Poplar of the City Park**
(Kosice, register-protected 1991, girth conflicts between sk.wikipedia and a
2021 teraz.sk piece on a wood-decay fungus found on the trunk, still alive
and monitored), **sly_001, The Lime of Saľa** (register + sk.wikipedia agree
it exists, no age or girth in any fetched source, access uncertain: the
register locality reads "courtyard of a former nursery/creche"), and
**rdv_001, The Lindens of Radava** (a 9-tree ensemble in a village cemetery,
one collectible point, but only one genuinely fetched source and the
reported figures unconfirmed). None clears the four-tree floor or the
single-famous-tree destination test alone, so all three landed as leads
(`data/leads/kosice.json`, `sala.json`, `radava.json`) rather than pages.
Fixed an id collision in the delivery file: the agent's `sal_001`/`rad_001`
already belonged to live Santalfio/Radomsko trees; reassigned to
`sly_001`/`rdv_001` before anything touched data/cities.

2 of the 9 turned out already published (Stary Smokovec's beech as
`sms_001`, Senica's mulberry as `sen_001`) and 4 rejected: Oksovske duby's
protected status was discontinued in 2020, Biela samota is a 24-tree avenue
(not one collectible point), and Dolny Kubin's two civic-planting limes
(34 and 17 years old) don't clear the genuinely-old/spectacular/significant
bar. All recorded in `_famous-slovakia.json`.

Separately, weighed the 3 famouspoland-batch4 trees a 2026-09-17 pass had
fully written but left "for a session to weigh": the Madej and Pietrek
Oaks (Lubiechow Dolny, two village oaks 100m apart, local nicknames only)
and the Jeremi Oak (Bydgoszcz, a real civic tree-of-the-year win with
932 votes and a Napoleon legend, but unconfirmed and not a national
superlative). None clears the destination test alone and none reaches four
trees, so all three are held as leads (`data/leads/lubiechow-dolny.json`,
`bydgoszcz.json`, the latter seeding a future Bydgoszcz page) with their
full prose preserved rather than discarded. Same judgement as the
Fontenay/Mielnik precedent (2026-09-05/17).

Also dispatched a verify pass on `higashi-hiroshima` (32 register leads
split out of Hiroshima prefecture's giant-tree database on 2026-09-07,
never mined): 17 verified across shrine/temple clusters (Fukujo-ji,
Uneyama Shrine, Hongu Hachiman Shrine, Fukutomi-cho, plus two standalone
finds), now in a write pass alongside the 3 Slovakia trees. To be continued
once stories land and a city page is assembled.

Ran `famous_demand.py --resolve` and `fame.py --apply` (free, deterministic)
and `photo_hunt.py --recheck` (free API sweep, new candidates for several
Alkmaar trees among others). Build (11895 pages), preflight and qa clean
throughout.

## 2026-09-18 (continuation 1) - Higashi-Hiroshima published (17 trees), a photo shortlist judged, city_names.py's search fallback fixed

Continuing from the entry above: the `higashi-hiroshima` verify pass came
back with 17 of 32 leads confirmed (facility clusters at Fukujo-ji,
Uneyama Shrine, Hongu Hachiman Shrine, a Fukutomi pair, plus the standalone
Renko-ji ginkgo and Renkyo-ji hiba). A write pass turned those 17 plus the
3 Slovak trees from the previous entry into 20 stories in one context.

**Published as a new city, `data/cities/higashi-hiroshima.json`, 17 trees.**
Hero and oldest: the Great Ginkgo of Renko-ji, roughly 400 years, 5.2 to 5.3
metres round, two minutes from Akitsu Station on the JR Kure Line, the only
one of the seventeen reachable without a car. The intro and question page
say plainly that this is not one walk: a temple trio above Saijo (Fukujo-ji,
three registered giants sharing one precinct), a nine-tree afternoon around
Toyosaka (Renkyo-ji, Uneyama Shrine's five-tree grove, Hongu Hachiman's
three), a Fukutomi pair of shrines 3.5km apart, and the standalone coastal
ginkgo 25km further south. Uneyama's five trees and Hongu Hachiman's three
sit on oaza-level (sub-district) pins rather than site-level, honestly
marked approximate: no coordinate exists anywhere in the source, the
register's own coordinate_trap note already flagged this. Preflight caught
three real issues before they shipped: two hard rule 9 species-name
collisions (this batch's plain "Hinoki Cypress" and "Hiba" against Boston's
stray "Hinoki Cypress bonsai" and Kanagi's "Hiba", fixed by normalising
Boston's mistaken qualifier and dropping my own "/ Asunaro" addition) and a
meta_description that miscounted the tree total by two.

**A demand-ranked photo shortlist (`photo_gaps.py --shortlist`) judged: 40
candidates across Milan, Barcelona, Tenerife, Singapore, Berlin and Arnhem,
2 approved, 38 rejected.** Both approvals are Tenerife (`tfe_003` Pino de
las Dos Pernadas, `tfe_004` El Gran Ficus). The reject pile is worth a
general note: 13 were filename false positives with no tree as the subject
at all (Arnhem's `arn_018` candidates are photographs of an oyster-mushroom
infestation on a chestnut due to be felled; three Barcelona candidates are
the Palau Castanyer building, matched on "Castanyer" being a surname rather
than the Catalan word for chestnut; Milan's `mil_008` is the cathedral
spire, matched on "Madonnina" street name), and a further several were the
WRONG SPECIES at the right address (three Berlin candidates for a Swiss
stone pine were actually the garden's separate Thuja plicata Naturdenkmal,
two Singapore candidates for one dipterocarp were a different one).

**Found and fixed a real bug in `scripts/city_names.py` while chasing why
Higashi-Hiroshima's language aliases came out wrong.** The resolver's
direct-title lookup 404's on "Higashi-Hiroshima" (English Wikipedia's own
title drops the hyphen, "Higashihiroshima"), so it fell to the fuzzy
search fallback, which has NO title-similarity check at all, only a
distance check, and it accepted the nearest article within 40km: plain
"Hiroshima", 25km away and a different, far more famous city, writing
Hiroshima's own language aliases into Higashi-Hiroshima's entry. Fixed by
trying a dehyphenated, correctly-cased title as a direct candidate before
the fallback is ever reached (`city[0] + city[1:].replace("-", "").lower()`),
which only adds a new resolution path and cannot change any city that
already resolves correctly through the existing ones. Verified both ways:
resolves to "Higashihiroshima" now, and reverting the fix reproduces the
"Hiroshima" mismatch exactly.

**That fallback bug is not limited to this one city, and the rest is left
for a dedicated pass rather than patched blind.** A quick audit of all 573
already-resolved `wikipedia_titles` for slug/title overlap found at least
two more confirmed wrong matches from the same loose fallback:
`minamialps` -> "Akaishi Mountains" (a mountain range, not the city; the
real article is "Minami-Alps, Yamanashi", disambiguated by prefecture
rather than country, a different fix than the hyphen one) and `velp` ->
"Arnhem Centraal railway station" (Velp's own Wikipedia title is a
disambiguation page, since two Dutch villages share the name, so it fell
through to search and landed on a railway station instead of either
village). Checked and cleared as legitimate on the same pass: `kotel` ->
"Osecna" is a genuine village-to-parent-municipality match (our Kotel has
no article of its own; Osecna is its containing municipality), which is
the same acceptable pattern as `bracon` -> "Arbois" or `collm` ->
"Wermsdorf" elsewhere in the file. The distinction between a legitimate
parent-municipality fallback and a wrong unrelated match needs per-case
judgement, which is why this is recorded rather than mass-corrected.

Also folded the 3 Slovak trees' finished stories back into their lead
files (`kosice.json`, `sala.json`, `radava.json`) alongside the shorter
`why` summaries already there, so the prose is not lost if a container
opens later. `data/agent-costs.json` carries both the write pass (20
trees, 158,686 tokens) and the photo pass (40 judged, 195,572 tokens).

Build, preflight and qa clean throughout; released the `higashi-hiroshima`
claim.

## 2026-09-17 (continuation 15) - Alkmaar's photo hunt is an exhausted, documented gap

`photo_hunt.py --recheck` restocked candidates for Alkmaar (14 trees, zero
photos, well clear of the 5-tree floor for the standing one-photo-per-city
aim): 8 new candidates across alk_009, alk_010 and alk_012. Fetched and
viewed all 8 against the Cadiz standard. None qualify: two are archival
black-and-white building-facade photos misfiled under the street address,
three are wide winter canal/park views with no single tree as the subject,
two are frozen-canal scenery with a tree only as a framing element, one is
a building with no tree visible at all. All 8 recorded as `reject` via
`photo_verdicts.py`. Alkmaar stays photo-less; do not re-run this hunt
without a genuinely new source (a reader submission, or Wikimedia gaining
new uploads for these specific addresses).

## 2026-09-17 (continuation 14) - Finished two stranded verify passes: Mishima folded into Atami, Zarzecze published standalone, Mielnik held

Two verify claims (`_famous-japan`, `_famous-poland`) sat finished but
unwritten from an earlier attempt: `data/research/famousjapan-verified.json`
(1 tree) and `famouspoland-verified.json` (2 trees). Too thin a batch for a
dispatched write pass, so wrote all three directly in-session per the Ottawa
precedent (2026-09-XX).

**mis_001, the Kinmokusei of Mishima Taisha** (National Natural Monument
1934, a documented annual festival, blooms twice each September): folded
into `data/cities/atami.json` as **ata_003**, honestly labelled with
Mishima's own address and transport, one JR stop from Atami and well inside
the day-trip boundary, matching the ata_002/Yugawara precedent already on
that page. Atami 2 -> 3 trees; fixed the now-stale "two trees" language in
its intro, meta_description and question_answer.

**zrz_001, the Zarzecze Plane Tree** (5.6m round, Dzieduszycki Palace park,
Podkarpackie, Poland; documented family folklore, entered Poland's 2017
national Tree of the Year contest): published as a new single-tree place,
`data/cities/zarzecze.json`, under the 2026-08-31 single-famous-tree
exception. No nearby published Polish city exists to fold it into. This was
a close call, recorded here per the mandate: the tree's own size, its
specific attributed folklore (harvest feasts, a horse burial, women taught
under its crown) and its national contest entry were judged sufficient to
clear "would somebody travel specifically for this one tree", but it is a
weaker signal than, say, Sliven's coin-and-award tree. Revisit if this reads
as wrong.

**mln_001, Sosna Mielnicka (Parasolka)** (a Podlasie roadside pine, register-
designated 1996, re-examined by a dendrologist in 2023): held, not
published. Its own verify_notes call it "not obviously a destination on its
own merit", no festival, record-claim or notable figure attaches to it, and
no nearby published city exists to fold it into. Kept fully verified in
`data/research/famouspoland-verified.json` for a future pass (a Podlasie
cluster, or a stronger fame signal). Recorded in both `_famous-poland.json`
leads and here rather than silently dropped, per the scarcity ruling of
2026-09-08: shipping it just because the research was already paid for
would be exactly the completeness the doctrine warns against.

Released a stale `trieste` verify claim from the same earlier attempt
(a partial fetch of Il Piccolo's 48-monumental-trees survey sat in
`tmp_verify/`, no output produced): folded the extracted article text into
`data/research/trieste.md` for whoever picks it up next (two named
candidates worth checking, a hackberry in Piazza Hortis and a plane on
Viale al Cacciatore, Trieste currently at 10/20 trees), rather than losing
the fetch.

Build (5900+ pages), qa.py and preflight.py clean throughout. Both claims
released.

## 2026-09-17 (continuation 13) - Eindhoven verify pass merged, a species-page gap the Alkmaar fix earned

The Eindhoven verify pass dispatched in continuation 12 came back with 5
trees, all in a new **Villapark** cluster (~250m span, a protected 1907
garden suburb Philips built for its executives), distinct from the 16
already-published trees. Three double-sourced against the city's own
separate street-tree management inventory (a horse chestnut, a Caucasian
wingnut, a pin oak, agreeing within 2-5 metres each); two single-sourced
and flagged honestly (a catalpa on Julianastraat with no house number in
the register, a second horse chestnut at Palingstraat). Wrote all five
stories and recognition lines directly rather than dispatching a
write-stories pass for five trees, taking care to distinguish the two
Prinsenhof trees and the two horse chestnuts from each other by name and
location, since the district plants several of the same species close
together. Merged (**Eindhoven 16 -> 21**), updated the count promises
(intro, meta description, question meta, the "free to visit" FAQ), and
folded the new cluster into the existing "Philips trees" framing since
Villapark literally is one. Six more candidates went to
`data/leads/eindhoven.json` as leads or blocked (an avenue, a 17-tree
grove, four trees the register itself marks not visible/visitable).
Released the claim.

Also wrote a species page continuation 12's fix earned: renaming
Alkmaar's alk_009 from "Silver Lime" to the canonical "Weeping Silver
Lime" (hard rule 9) pushed that cultivar to exactly 3 trees sitewide
(Alkmaar, Ghent, Maastricht), which is pagegaps.py's threshold for a
Contract F species page. Wrote `data/species/weeping-silver-lime.json`
from those three trees' own facts (P3): each planted by a park designer
specifically for the wind-shimmer effect, a detail all three stories
already carried independently. Build and preflight clean throughout.

## 2026-09-17 (continuation 12) - Alkmaar write claim finished, Eindhoven verify dispatched

Resumed a window an earlier attempt stopped in with two claims standing
(alkmaar write, eindhoven verify), per the "finish it or release it" rule.
Alkmaar's `data/research/alkmaar-verified.json` already had 5 of 7 trees
written (from continuation 11's dispatch); wrote the last two stories
(alk_013 Copper Beech of the Hertenkamp, alk_014 Horse Chestnut behind
Koekenbier, both single-source and flagged) directly rather than
redispatching an agent for two trees, merged all seven into the city file
(**Alkmaar 7 -> 14**), fixed one species-name drift (Weeping Silver Lime
was recorded as "Silver Lime" here, "Weeping Silver Lime" everywhere else,
hard rule 9), and updated the count promises. Build and preflight clean.
Released the claim.

Eindhoven's claim had no work behind it at all (claimed, never started).
`scripts/leads.py --ready` showed 0 READY trees sitewide, so there was no
cheaper write-pass work to do first. Dispatched a verify pass on Eindhoven's
register pool (751 candidates within 20 km, 684 unmined) rather than release
the claim unfinished a second time, steered toward forming one new tight
walkable cluster since the existing 16 trees already span 6.5 km. Result not
yet known as this entry is written; the next continuation should check
data/research/eindhoven-verified.json and data/in-flight.json before
claiming anything.

## 2026-09-17 (continuation 11) - Enschede/Helmond write pass merged, Alkmaar verify dispatched

Followed the run prompt's "write pass first, whenever there is one to do" rule.
`prepare.py` showed 3 fully verified trees sitting unmerged (ens_014, ens_015
in `data/research/enschede-verified.json`; hlm_019 in
`data/research/helmond-verified.json`, all left by continuation 10). Claimed
both cities for write, dispatched a write-stories pass, and merged the result:
**Enschede 13 -> 15 trees, Helmond 18 -> 19 trees.** Fixed one species-name
drift at merge time (the writer delivered "Common Hornbeam", the site already
uses "Hornbeam (Carpinus betulus)" everywhere else) and updated both cities'
count promises (meta_description, question_meta, question_context, and
Helmond's "are they free to visit" FAQ, which listed every access group by
name and needed the new Croylaan oak added to it, since it is council land
beside a public road rather than inside the private castle grounds it
approaches).

With the shelf otherwise thin (48 cities staged for verify but none with an
unmerged write ready), dispatched a fresh verify pass on **Alkmaar** (7/20
trees, 361 unmined Dutch LRMB register candidates, real demand at 12
impressions/10d) rather than touching Enschede or Helmond again in parallel,
to avoid two agents writing the same delivery file at once. Brief steered it
toward forming a new tight walkable cluster rather than adding scattered
singletons to a city that already spans 10.9 km.

## 2026-09-17 (continuation 10) - Tallinn register pool confirmed exhausted a second time, claim released

Resumed a window an earlier attempt stopped in with 4 claims standing
(helmond, enschede, tallinn, eindhoven, all verify). Enschede and Helmond
each already had a `-verified.json` file with a story-ready tree
(ens_014, ens_015, hlm_019) sitting unmerged; dispatched a write-stories
pass on those rather than re-verifying.

Read Tallinn's brief before dispatching a verify pass on it, per the
"finish it or release it" rule. The remaining 52 unmined register
candidates are almost entirely ornamental cultivars already carrying a
`lead:` verdict from the 2026-09-12/13 passes (copper beeches, globe
maples, pyramid oaks, weeping cultivars, none with an age or story), one
dead tree, and 3 already-BLOCKED entries. The Wikidata sweep's 6
candidates are the same already-blocked black poplar plus outliers
10-20km out. Nothing here clears the bar. Released the claim rather than
burn a 40-minute pass re-confirming what the 2026-09-12/13 passes already
found; `city_queue.py --next` should move past Tallinn now that this is
on record twice.

## 2026-09-17 (continuation 9) - Houston and Vancouver: write pass on 5 bought-and-paid-for trees, city grows to 6 and 7

A prior attempt this window stopped with two write claims still standing on
data/in-flight.json (Vancouver, Houston) whose verify work had already landed
(064ae72a). Released the stale claims, deleted the now-merged enschede-verified.json
research file (its only entry, ens_013, was already published), then re-claimed
both for a write pass.

**5 fully verified register trees written and merged**: hou_005 (The Rienzi
Yaupon, a yaupon holly grown to tree height in the Museum of Fine Arts' Rienzi
garden, state champion class) and hou_006 (The Russ Pitman Mexican White Oak,
Bellaire) from the Texas Big Tree Registry; van_005 (The Dunbar Street Beech),
van_006 (The West 20th Avenue Sweet Chestnut) and van_007 (The Blenheim Street
Oak) from Vancouver's Heritage Register cross-checked against the city's
separate street-tree inventory. None has a documented age; all five say so
plainly and ask the reader. Houston grows from 4 to 6 trees, Vancouver from 4
to 7.

Normalised 3 species-field collisions the write pass correctly left alone
(verified fields): "Spanish Chestnut" -> "Sweet Chestnut" (Castanea sativa,
matching 23 other published trees), "Mexican White Oak / Monterrey Oak" ->
"Mexican White Oak" (matching 2 others), and van_007's multi-clause dispute
field shortened to the existing convention "Oak (Quercus sp.)" (the dispute
itself stays fully told in the story and how_to_recognise).

Fixed the count-promise copy both cities' new trees broke (Houston's intro/
meta_description/question_meta said "four"/"three more", Vancouver's said
"Full list of 4"/"the four"/"All four"), rebuilt clean, qa.py and preflight.py
both pass (0 problems).

**Also fixed in passing: Houston was missing from data/city-list.json
entirely**, since the city was first opened (0339be59), despite its page
being live and built. This is why feed.xml.ts's `updateFirstSeen()` (which
iterates city-list.json's `cities` array) had never stamped hou_001-004 into
data/first-seen.json either, though the pages themselves built fine via a
different, direct-directory-scan path. Added the missing entry (status
published, trees 6) and corrected Vancouver's stale `trees: 4`. Also bumped
united-states.json's meta_description tree count (249 -> 251) since the two
new Houston trees pushed it stale immediately.

Both claims released. Cost logged to data/agent-costs.json (write, 5 trees,
133k tokens).

## 2026-09-17 (continuation 8) - Ischia settled to a leads verdict, Marthalen Oak photographed, two register-backed verify passes dispatched (Vancouver, Houston)

**Ischia given the same leads-file treatment as Ravenna**: 3 MASAF candidates
2.3-17km apart, below both the six-candidate verify floor and the four-tree
page floor. Written to `data/leads/ischia.json`; `city_queue.py --next` no
longer recommends it.

**The Marthalen Oak (Zurich's mar_001) now has a photograph**, the one
candidate `photo_gaps.py --shortlist` printed today. Six of eight queued
candidates carry a geotag matching our pin within metres, all CC BY 3.0 from
the same photographer (Kurt Spalinger-Røes) via a 2015 Panoramio upload.
Approved the full-height shot (panoramio (2), 2332x4992) as the lead: the oak
is unmistakably taller than the surrounding beeches, in leaf, good daylight.
Added the trunk-plaque close-up (panoramio (1)) as a second photo per the
2026-09-12 `photos` field: it independently confirms the exact figures our
story already cites from the Ortsmuseum (34m tall, 5.60m round, ~360 years),
which is about as strong a corroboration as a photograph can give. Added
`height_m: 34` from the same plaque.

**Two register-backed verify passes dispatched** on cities from Hidde's 2026-08-19
named-cities list (from-zero web research explicitly on, growing toward the
10-tree target): Vancouver (15 remaining unmined leads from the City of
Vancouver Heritage Register, an Open Government Licence source already used
for its 4 published trees) and Houston (10 unmined Texas Big Tree Registry
leads, non-commercial licence so lead-only, needs an independent second
source per tree). Both claimed in data/in-flight.json; results pending.

## 2026-09-17 (continuation 7) - Ravenna settled to a leads-file verdict, a photo-queue cleanup pass, one new photo (Montreal)

**Ravenna given a written leads-file verdict**, closing a gap the 2026-09-17
continuation-5 fix (`settled_verdict()` in city_queue.py) didn't yet cover:
Ravenna had been checked and passed over as too thin five separate times
(2026-09-11, 09-12, 09-13, 09-16, this pass) but never got a `data/leads/`
file of its own, so it kept resurfacing on `city_queue.py --next`'s OPENABLE
list. Wrote `data/leads/ravenna.json` with the verdict (4 MASAF register
candidates, one near the centre and three 17-19km out, none forming a
walkable cluster, below the six-candidate floor); re-ran `city_queue.py`
(no flags) to regenerate data/city-queue.json/CITY_QUEUE.md/city-list.json/
LEDGER.html, and Ravenna now prints under SETTLED rather than OPENABLE.

Also checked Ischia (register=2, 3 unmined candidates 2.3-17km apart, same
thin-and-spread shape, not written to a leads file this pass since only one
brief was read) and Ottawa/Caserta/Tilburg (all already fully judged-negative
photo queues from earlier passes, not fresh gaps).

**Photo queue cleanup: a viewing pass on the biggest zero-photo cities'
queued candidates**, per the 2026-09-01 ruling that a night run may take a
viewing pass. `leads.py --ready` was empty (0 READY) at session start, so
this filled the window instead of a write pass. Fetched and judged every
unjudged candidate for Leeuwarden (41 trees, 0 photos, the single biggest
gap), Haarlem, Maastricht, Eindhoven, Zwolle, Spokane, Rotterdam, Hobart and
Rouen: 39 rejected, 2 held (Haarlem's Kenaupark lime: two candidates show
the right park but at least two similar bare limes stand near the same
lawn, and our own how_to_recognise line singles this one out as "the
youngest," which no photograph can confirm without a nameplate), 1 approved
(Montreal's mtl_013, the McGill Katsura: an iNaturalist courtyard photo
whose own coordinate sits about 13m from our pin, species independently
confirmed by the same observation's leaf close-up).

The pattern worth recording for the next pass: nearly every queued
candidate for these cities was a false positive from name/address matching
rather than an actual photo of the tree, in three repeatable shapes. Dutch
municipal heritage-building surveys (Commons titles like "Zwolle GM
<street address>" or "<Street> N, Zwolle") photograph the FACADE at a
monument's address, not the street tree beside it; all 12 of Zwolle's
candidates and 2 of Haarlem's were this. Archival black-and-white material
(a 1910 postcard, RCE facade surveys, a glass-plate lane scan, funeral and
ceremony photos) came up repeatedly and is banned outright regardless of
subject. And keyword collisions produced outright wrong subjects: a
different, famous Californian redwood matched on "redwood," a Bonnie-and-
Clyde mugshot matched on "Champion," a gravestone matched on the
deceased's own park-adjacent name.

Rebuilt (`npx astro build`, needed a fresh `npm install`, no node_modules
this session) and ran `scripts/qa.py`: 8887 pages, clean. `preflight.py`:
0 problems.

Released a standing claim rather than starting fresh: an earlier attempt in
this same window had already run a verify pass and left its finding on disk
(`data/research/enschede-verified.json`), uncommitted. One candidate: ens_013,
"The Sweet Birch of the Oosterbegraafplaats" (Betula lenta), the fourth
register-designated tree on the Oosterbegraafplaats cemetery alongside
ens_008/009/010 (Hungarian Oak, Sweet Gum, Oriental Spruce). Netherlands
LRMB register nr 1692854 is the primary source (dendrological grounds, no
age or planting history recorded); monumentaltrees.com independently lists
the same specimen and was used only to corroborate species, girth (234cm)
and height (~18m), never as the sole source, per hard rule 1. No age is
documented anywhere, so `age_estimate` stays empty rather than guessed, same
as ens_010's spruce.

Wrote the story myself (one tree, below the six-candidate write-pass
batching floor) and merged it into data/cities/enschede.json. Fixed the
city's meta_description and question_meta, both of which still said twelve
trees. Ran a full `npx astro build` and `scripts/qa.py` against the built
output (both needed a fresh `npm install`, site/ had no node_modules this
session): 5745 pages built, QA clean. preflight.py and superlatives.py also
pass clean (one unrelated pre-existing FAIL on preflight was the enschede
count itself, now fixed; everything else it prints is pre-existing NOTEs
elsewhere in the corpus). Photo still missing (13 of 13 for this city).

Also confirmed rather than re-investigated: the two rung-2 alerts from
session start are both already-known non-issues. Weekly analysis's failure
on 2026-09-14 matches the documented usage-limit-death fingerprint exactly
(1 turn, 0 cost, <1s) and `scripts/health.py` says so outright; the iOS
app's newest failure (2026-09-16) is the same already-documented flaky tap
race in `FlowWalk.swift` (`testEveryFlowLeavesAWayBack` failing to find
"person-more"), already recorded as FOR HIDDE (needs a workflow-scoped push
token this bot's token does not have) as recently as 2026-09-16. Neither
needed new work.

## 2026-09-17 (continuation) - Florence 26 -> 27; city_queue.py stops re-recommending settled dead ends

Picked up two claims an earlier attempt in this window left standing. Vilnius's
verify work (register confirmed exhausted) was already done and logged in the
entry below; released the claim, nothing further to do.

**Florence 26 -> 27**, flo_027, "The Hackberries of Piazza Vasari" (Mediterranean
Hackberry, three MASAF register twins folded into one entry per the register-
twins rule, girth 407cm). Resolves a stale "Three Hackberries of the Cascine"
lead: the name was wrong (Piazza Giorgio Vasari in Campo di Marte, not the
actual Cascine park 4-5km away), and settles an "alive now" question that had
stalled two earlier passes: RFI announced felling 21 trees in this garden in
November 2025 for a railway-bridge rebuild, but La Nazione states plainly the
historic/monumental trees were excluded, and RAMI's own page shows the pinned
tree measured healthy on 14 Oct 2025, weeks before the felling. Four sources.
Also checked and closed: the Isolotto poplar candidate turned out to already
be published (flo_026, same MASAF sheet id, missed by the dispatched pass's
own search); two more candidates confirmed comune Fiesole, not Florence
(matching two already-flagged Wikidata wrong_city leads). Story written and
merged by the session (one tree, below the six-candidate write-pass batching
floor); Italian overlay (data/i18n/it/florence.json) updated in the same
commit, including the stale "26 giganti" count in its title/meta_description.

**city_queue.py --next was re-recommending cities an earlier pass had already
settled as dead ends**, discovered while picking a new-coverage target: Dubai
and Taormina each carry a written verdict in their own `data/leads/*.json`
file (no publishable supply; every register tree on private hotel grounds),
but neither note was ever read by the queue script, so both kept printing as
openable. This exact rediscovery is logged across at least seven sessions
since 2026-09-08 (Taormina alone: 09-08, 09-11, 09-12, 09-13 x3, 09-16).
Added `settled_verdict()` to scripts/city_queue.py: it matches a leads file by
slug and checks its `note` for verdict phrasing already in use ("VERDICT:",
"kept so nobody re-run", "do not re-run/re-research this"); settled cities
move to a new SETTLED section instead of OPENABLE/NAMED BY HIDDE/movable.
While checking the remaining OPENABLE list, found the same failure one layer
deeper: Trier's supply (9 register rows, 4 Wikidata candidates) is entirely
cross-border Luxembourg trees (Rosport-Mompach, Mertert, Manternach,
Echternach, Berdorf, Flaxweiler communes, 10.7-21km out), matched by raw
distance with no jurisdiction check, the same mistake already recorded for
Florence/Fiesole. Wrote a settled verdict for Trier too. The remaining
OPENABLE cities (Adelaide, Zagreb, Lagos, Ravenna, Niagara Falls, Wellington,
Mechelen, Gran Canaria, Kilkenny, Ischia, Izmir, Stirling, Canterbury, Evora,
Stratford-upon-Avon, La Palma) all sit at 0-2 register rows plus 1-8 Wikidata
leads, well below the six-candidate floor; not dispatched.

Confirmed the iOS app's newest CI failure (`testEveryFlowLeavesAWayBack`,
floor job, 2026-09-16) is the same documented flaky tap race already recorded
in FlowWalk.swift's own comments and `drafts/ios-floor-retry.patch` (FOR
HIDDE: the fix needs a `workflow`-scoped push token this bot does not have,
reconfirmed 2026-09-16). Not re-attempted.

`python3 scripts/qa.py`, `preflight.py` and `superlatives.py` all pass clean.

## 2026-09-17 - Milan 29 -> 30, target reached; Vilnius register confirmed exhausted

Two parallel verify passes on the depth-allowed roster (DATA.md 2026-09-15: alicante and krakow were already at/above target despite showing in the queue's "staged for verify" list, so picked the two below instead, both below target with real register supply).

**Milan** delivered one tree, mil_030, Il Bagolaro di Villa Ghirlanda: a Celtis australis, 445cm girth, 34m tall, in the public park of Villa Ghirlanda Silva at Cinisello Balsamo (about 8km north of central Milan), where 19th-century garden theorist Ercole Silva first tried out the English-garden style he then wrote a book about. Two sources (MASAF register plus a directly-fetched 2023 local news piece on the comune's own sensory-map project). This closes Milan at its CITY_QUEUE.md target of 30; the near-centre register (10 rows within 2.3km) is fully exhausted, all duplicates or already-blocked. Story written and merged by the session (not a write-stories pass, since one tree does not clear the six-candidate batching floor); intro/meta_description/question_meta count references updated (29 -> 30), Italian overlay (data/i18n/it/milan.json) translated and updated in the same commit so the build's overlay-completeness gate did not go red. Build and qa.py both pass.

**Vilnius** delivered zero new trees: the register (40 candidates within 20km) was already fully mined by three prior passes (08-16, 08-17, 08-31). This pass closed two open judgement calls instead: a maple circle in the P.Vileišis palace courtyard moved lead->blocked (the courtyard's own Lithuanian Wikipedia page says it's locked, inaccessible), and the Presidential park oaks moved lead->blocked (public park, but every visitor is searched by security at entry, hard rule 10's own "guard who checks: no" case). Two stale/duplicate leads closed. Vilnius stays at 14 trees; nothing left to mine there without a fresh register or a Hidde-named from-zero pass.

Also processed 2 reader submissions (#111, #112) and logged both passes to data/agent-costs.json.

## 2026-09-17 - Submissions #111, #112 (Taketa): two more GPS-only pins at Oka Castle, same submitter as #110

Same reader (user_id a8ca51da-...) who sent #110 from the Oguni/Taketa border
yesterday, now two pins a day later, 290m apart, both landing inside the Oka
Castle ruins (Oka-jo) national historic site in Taketa, Oita: 32.96713,131.40504
and 32.96912,131.40796. Both kind `tree`, app Collect flow, no name, no
species, no girth, no `why`, and no matching row in the `sightings` table for
either tree id, so no photo ever arrived despite the app's copy promising one
travels with the add.

Checked data/registers/japan-bunkacho.json: nothing within 25km of either
point. Web search confirms the coordinates are Oka Castle itself; its
documented trees are planted cherry and maple for seasonal colour (one of
Japan's 100 best cherry-viewing spots), not a named ancient specimen, and no
giant tree at the site turned up in English or Japanese search. An Overpass
check for natural=tree within 400m of both points timed out (server
overloaded, consistent with the standing blocklist note) and was not retried.

Does not clear the bar: no second source, no species, no name, no photo,
nothing to verify beyond two coordinates. Filed as leads
(data/leads/taketa.json) rather than published. Both submissions rows set to
outcome `open_question` with a reply asking for a photo or the species;
rows 111 and 112 marked processed.

Reader submission (kind `tree`, app's Collect flow, no name/species/girth given).
The pin (33.04561, 131.29971) was tagged "Oguni" by the app, but that is just
the nearest city in our own database (25.6km from ogn_001): reverse geocoding
(Nominatim) places the actual point in Taketa, Oita, a prefecture over from
Oguni-machi, Kumamoto. Went looking for a documented tree there anyway, in
case it was a known giant cedar mismapped by the app: found and checked the
national register's Amida Sugi (阿弥陀杉, Kurofuchi, Oguni-machi, designated
1934, ~1600yr claimed, 38m, girth 10.65m per bunkacho + a second source), but
that tree sits demonstrably elsewhere (its own listed address is nowhere near
this pin) and the Japan giant-tree/bunkacho register has nothing within 19km
of the submitted point. Overpass has no named tree node there either, only
generic woodland polygons. No photo was sent with this one.

Does not clear the bar: no second source, no species, no name, nothing to
verify beyond the coordinate. Filed as a lead rather than published (kept in
mind for a future Taketa pass if more evidence ever turns up), outcome set to
`open_question` on the submissions row, reply asks for a photo or the species.
Row 110 marked processed.

## 2026-09-13 (continuation 34) - New place: Portalegre (Portugal), the Plane Tree of Rossio, single-famous-tree exception

Same window, continuing down `famous_demand.py --gap`'s list past the Belgrade
tree. "Plane tree of rossio" (Portugal, 75 views/mo, 2 langs, pin yes) turned
out to be **Plátano do Rossio**, in Portalegre, Alentejo, not Lisbon's Rossio
as the name first suggested (the lead's own coordinate, 39.296/-7.430, is
40km southeast of Lisbon and matched Portalegre's own Rossio square via
Nominatim). No published tree within 100km, so its own place.

An exceptionally well-documented single tree: planted 1838 by the town's own
physician-botanist José Maria Grande, Portugal's first tree ever classified
a Monument of Public Interest (1938), winner of the national Árvore
Portuguesa do Ano contest for 2021 and 4th in the European final. Two
independent sources (Portuguese Wikipedia, the Portalegre municipal
council's own visitor page) plus three corroborating 2020-2021 press pieces
(Público, LusoJornal, Gazeta Rural) on the award.

Flagged rather than silently resolved: Wikipedia gives 5.26m girth/27m
canopy from older records, the municipality and the press all converge on
7m/37m from the 2020-2021 measurements; used the more recent, more widely
corroborated figures and said so in `verify_notes`. Also flagged: the
classification year moves by one across sources (1938 vs 1939), used the
earlier without resolving by guessing. Photo (João Martins, CC BY-SA 4.0)
is a strong Cadiz-standard shot, in leaf, showing the tree's distinctive
20 support props clearly. Full build (5656 pages) and `qa.py` (8788 pages)
both clean.

## 2026-09-13 (continuation 33) - Belgrade 4 -> 5: the Vračar tavern-keeper's plane

Same window, continuing down `famous_demand.py --gap`'s list after La Pochota.
Next candidate with real supply, "Platan na Vračaru" (Serbia, 114 views/mo,
already pinned), had no coordinate in the lead file for the linked entry
"Platan na Vračaru" itself but the lead's sibling record ("Platan na
Vračaru") named an exact address (Makenzijeva 73, Belgrade), which put it
0.98km from the existing bel_001 (Cvetni Trg oak), inside Belgrade's already-
published 7.3km walk. Deepened Belgrade rather than opening a new place.

Verified: the town's own green-space manager, Zelenilo-Beograd (~170 years,
3.90m girth, 27m tall), and Serbian Wikipedia, which cites the 2002 Belgrade
City Assembly protection order (Official Gazette 5/2002) but gives slightly
different figures (~150 years, 3.67m girth). Recorded the discrepancy in
`verify_notes` rather than picking one silently; used the official manager's
numbers as primary. Geocoded the address via Nominatim, which returned the
"Trandafilović" restaurant by name at the tree's own site, matching every
source's description of the tree standing in that restaurant's garden.
`location_precision: confirmed`.

Photo (Ljiljana Sundać, CC BY-SA 4.0, Wikimedia Commons) is a bare winter
shot, the only kind available for this tree on Commons: still meets the
Cadiz standard on composition, exposure and framing, just not the in-leaf
tiebreaker. Fixed intro (was 117 words, Contract C caps at 100) and the FAQ's
stale "all four" after adding the fifth tree. Full build (5653 pages) and
`qa.py` (8780 pages) both clean.

## 2026-09-13 (continuation 32) - New place: Chiapa de Corzo (Mexico), La Pochota, single-famous-tree exception

With `city_queue.py --next`'s OPENABLE list exhausted (see the previous two
entries), moved to the famous-tree track: `famous_demand.py --gap` (trees
read about in other languages and unwritten in English, the thin-competition
end of the list). Top of the list by demand with an actual pin was **La
Pochota**, a giant kapok (Ceiba pentandra) in the main plaza of Chiapa de
Corzo, Chiapas, 386km from our nearest published tree (Santa María del Tule),
too far to join any city.

Verified against Spanish Wikipedia, a July 2026 Sol del Soconusco news piece
on the 33rd anniversary of its 1993 protection declaration, and INAH (Mexico's
national heritage institute): the town was founded beside this tree in 1528,
a 1945 arson fire destroyed roughly a third of the crown (one scorched limb
survived and is still growing), and Chiapas declared it the state's first
Historic and Notable Tree in 1993, a status shared nationally with only two
others (the Árbol del Tule and Mexico City's Árbol de la Noche Triste).

Two things flagged honestly rather than repeated as fact: age is "at least
500 years" per the state's own 2026 notice, not the "thousand-year tree" of
local folklore, since nobody has cored it (`age_min: 500, age_max: 600`).
And several Mexican press pieces describe it as "over 60 metres tall", which
no survey supports and which the tree's own silhouette against the plaza's
two-storey arcades in its own lead photograph contradicts, so no `height_m`
is recorded at all. Photo (Wolfgang Sauber, CC BY-SA 3.0, Wikimedia Commons)
meets the Cadiz standard: fills the frame, in leaf, well exposed, trunk and
crown both readable. `city-aliases.json` gets a `no_other_names` entry (no
English exonym). Preflight caught a real hard-rule-9 violation on first pass
("Kapok / Ceiba" as a second common name beside existing "Kapok" trees in
Lima/Oahu), fixed to "Kapok" alone. Full build (5652 pages) and `qa.py`
(8779 pages) both clean before committing.

## 2026-09-13 (continuation 30) - New place: Gornja Stubica (Croatia), the Gupčeva lipa, single-famous-tree exception

With the Tallinn claim finished and released, `city_queue.py --next`'s
OPENABLE-today list was checked for anything not already documented as thin
today: Adelaide and Zagreb (#154/#173, one Wikidata candidate each) were the
highest-ranked untouched options. Zagreb's one candidate, an oak nicknamed
"Dedek" in Maksimir park, was already recorded blocked in
`data/leads/zagreb.json`: it fell in a storm on 2026-05-16, confirmed by two
Croatian news sources, and its clone saplings have not been replanted at the
site. That same leads file had already flagged the real find and left a note
for later: a second, unrelated Zagreb-area register row ("Lipa na
Medvednici") turned out to be a false positive, a mountain peak not a tree,
but the pass that caught it in August had also surfaced a genuine one nearby:
**Gupčeva lipa**, a linden in Gornja Stubica, in the Zagorje hills, tied by
Croatian tradition to Matija Gubec gathering his followers there before the
1573 Peasant Revolt, one of the defining events of Croatian history. That
pass had explicitly left it for "a future pass to evaluate as its own place."

Verified it properly this pass. Two independent sources (Krapinsko-zagorska
County's own nature-protection page and Croatian Wikipedia) agree on a 2021
survey (4.90m girth, 9m height, no exact age) and the historical tradition;
neither is in Croatia's own 12-entry national monument register. An OSM node
tagged "Gupčeva lipa" matches the Wikidata coordinate within metres, so
`location_precision: confirmed`. Age set honestly as a floor rather than a
figure: "at least 450 years" (the 1573 anchor), flagged, no invented
precision on top. Checked the execution detail in the story (Gubec crowned
with red-hot iron, quartered, February 1573) against English Wikipedia and
ExecutedToday.com before using it; both agree.

Published as its own place, **Gornja Stubica**, one tree (`gst_001`), under
the single-famous-tree exception of 2026-08-31 (would somebody travel
specifically for this one tree, given a national historical association):
Zagreb itself gets nothing added, since its only candidate is dead. Ran
`city_names.py` (no English exonym, correctly). `preflight.py` (0 problems),
`superlatives.py` (no crown conflicts), full build (5649 pages) and `qa.py`
(8771 pages, links resolve, page reachable via the generated Croatia country
page) all passed before committing.

## 2026-09-13 (continuation 29) - Finished the standing Tallinn verify claim: 8 -> 9 trees, the Skoone Bastion Lindens

Followed the resume checklist: `passcheck.py --claims` showed Tallinn standing
(verify, by night-run, 137 min left), an earlier attempt in this window had
already fetched eight pages to disk (Eesti Loodus 2002, KesKus 2006, a
Postimees 2022 piece, Tallinn's own register pages, a Harku municipality page,
two Cloudflare-blocked dead ends) but delivered nothing and committed nothing.
`leads.py --ready` was empty, so the claim was the whole job.

Read what was already fetched rather than re-fetching. Eesti Loodus's 2002
survey of Estonian city lindens, already the source for the published Kelch's
Linden (tln_001), also names old western lindens surviving at Rannamägi park
on the former Skoone bastion, first recorded on Tallinn's 1728 town plan as a
row of 19-20 trees following the bastion's cavalier edge. KesKus (2006, Heldur
Sander) gives the full history and cites a real 1999 University of Tartu
dendrochronology study (Alar Läänelaid): the two thickest of four cored
lindens measured 129cm and 111cm in diameter and were ring-dated to roughly
390 and 300 years, implying planting near 1609 and 1699. The 1609 figure
predates the bastion's own 1683 construction start, a discrepancy neither
source resolves and which the new tree's story states plainly rather than
explaining away. Postimees (2022) independently confirms the row is alive and
vigorous, not a historical footnote: it reports the trees' roots pushing apart
a 300-year-old stone passage buried in the bastion beneath them. Two
independent published sources, no register entry within 500m of the site (the
EELIS register has nothing here). Shipped as **tln_009, The Skoone Bastion
Lindens**, an ensemble entry (a compact, singular row with one obvious place
to stand) rather than pretending to isolate one trunk, since no source
distinguishes the dated trees from their neighbours; `location_precision:
approximate`, pinned to the park (OSM: Rannamägi, confirmed via Nominatim).

Updated the city's intro, meta_description, question_meta, question_context
and three FAQ answers for the new count and to fold the new tree into the
"can I see them in one walk" and "are they free" answers (yes; it sits within
the same Old Town cluster as Kelch's Linden and the Huecki Lindens). Kept the
"generally called the oldest tree in Tallinn" hedge on Kelch's Linden
unchanged and never claimed the new tree as a citywide superlative, since its
age is a single dendro study applied to an ensemble rather than one named,
locatable trunk; `superlatives.py` confirms no two pages claim the same
crown. `preflight.py` (1 FAIL fixed: a stale meta_description tree count),
full site build (5646 pages, clean) and `qa.py` (8763 pages, links resolve,
text clean) all passed before committing.

Also recorded two findings from the same fetch batch that are NOT Tallinn:
Harku vald's own website (a neighbouring municipality, not researched this
pass) confirms its Rabakivi tamm has died completely (blocked, never
re-research) and its Pilladu tamm is alive and protected (a lead for a future
Harku page or day-trip addition). Both filed in `data/leads/tallinn.json`.

Released the Tallinn claim. Checked `health.py`: `ios.yml`'s newest finished
run is still the failing 2026-09-13 one already noted by the prior
continuation (a UI test timing flake, no `ios/` code changed since the last
green run); nothing new to add. No sightings, no new submissions.

## 2026-09-13 (continuation 28) - Finished an inherited _famous-belgium claim: 6 new single-tree places, 2 Ghent additions, 1 held, 1 duplicate caught

Picked up a verify pass (`_famous-belgium`, claimed by an earlier attempt
this window, 134 min still on its clock) that had produced 10 verified
trees in `data/research/famousbelgium-verified.json` but never been
written up or merged. Ran a write-stories pass on it, then judged the
single-famous-tree destination test (CLAUDE.md 2026-08-31) on each
result rather than merging all ten.

**Published as new standalone places** (each below the 4-tree floor
under the exception, since none clusters with a published city or with
each other): Bonnerue (`bnr_001`, Li Béni Hesse, one of Belgium's
largest beeches, damaged, undated), Xhoris (`xho_001`, Tilleul des
Lognards, a nail tree protected since 1965 on the GR571 trail), Macon
(`mom_001`, Tilleul de Macon, its own French Wikipedia article, shaped
into three tiers on twelve posts, protected since 1942), Waremme
(`wrm_001`, Arbre de la Liberté, planted 22 September 1797), Jalhay
(`gos_001`, Les Sept Frères de Gospinal, Belgium's largest multi-trunk
oak, near the Hautes Fagnes) and 's-Gravenvoeren (`gvo_001`, Nagelboom,
a nail tree and former European Tree of the Year finalist).

**Merged into Ghent** rather than given their own pages, both within
the day-trip boundary: `gnt_007` (Dorpslinde van Massemen, Belgium's
Tree of the Year 2016, dendro-dated 378-440 years, ~13.6km from Ghent
centre, De Lijn bus) and `gnt_008` (the Solitaire Plane of Prudens Van
Duyseplein, 1.4km from centre). Ghent now has 8 trees.

**Held back**: the Remarkable Lime of Chantemelle (`cha_001`), verified
and written but carrying nothing beyond a bare Wallonia heritage
reference number, no age, no girth, no story. Fails the destination
test on its own evidence ("that is most of the file"); returned to
`data/leads/_famous-belgium.json` as blocked with the verified record's
git location noted for a later pass if a distinguishing fact surfaces.

**Caught a duplicate**: the Peace Oak of Wondelgem (`wdg_001`) is the
same tree as the already-published `gnt_006`, 75m off pin, same
planting year, same heritage object. Not merged; its one new fact (a
2026 Stad Gent renovation news item) was folded into `gnt_006` as a
third source instead.

**Two mechanical fixes along the way**: an id collision (`mac_001`
already belongs to Macugnaga, Italy; reassigned to `mom_001`) and four
species fields corrected to the site's one canonical common name (hard
rule 9): Large-leaved Lime, Horse Chestnut, London Plane, all previously
written with a non-canonical qualifier.

No photos on any of the 8 new/merged trees; an honest gap, left for a
photo pass. `_famous-belgium.json` still holds 14 further leads for a
future verify pass.

## 2026-09-13 (continuation 27) - Venice/Venlo/Verona photo hunts: dead ends documented; Vienna's Rathauspark trio completed

Venice's ven_011 (Palm of San Servolo), Venlo's vnl_001 and vnl_007, and
Verona's ver_006 (Yew and Laurel Wood of Giardino Giusti) all keep their
honest photo gaps. Candidates from the free `photo_hunt.py --recheck`
sweep: ven_011's one candidate is a good daylight photo but the San
Servolo building facade owns the centre band, not the palm, and the
crown shape reads as the wrong Phoenix species besides. vnl_001 and
vnl_007's four candidates are all archival B&W or a 1944 aerial
reconnaissance frame with no individual tree visible. ver_006's three
candidates are all general Giardino Giusti views (the cypress avenue,
the fountain parterre) rather than the yew and laurel wood the story
names; none show a resolvable yew trunk or crown. All 7 recorded
`judged`/rejected in `data/photo-queue.json` so a future sweep does not
re-serve them.

Vienna's Rathauspark now has photos of all three of its individually
protected planes (Naturdenkmal 564/566/567, designated together in
1973): vie_026 (ND 567) and vie_029 (ND 566) approved this pass, joining
vie_006 (ND 564, already published). The two were previously
indistinguishable in our own data past a register_id; a photographer's
geotags (GuentherZ, two photos taken the same day, 2010-08-25) settled
which pin is which within a metre-scale margin, and the resolution is
now recorded in both trees' `verify_notes`. vie_027 (Plane of
Hugelgasse) also got a photo, named for its own register address.
vie_018, vie_019, vie_020, vie_021 and vie_022 keep honest gaps: 14 of
their 21 rejected candidates were Schonbrunn palace geosearch noise
750-800m from the actual pins (Commons' geosearch returns anything near
a popular landmark, not photos of a specific tree), one was the wrong
Natural Monument entirely (ND 179, the Japanese pagoda tree our own
story already records as destroyed by war), and two right-tree
candidates (Burggasse's elm) failed on `photo_light.py`'s exposure score
under an overcast sky.

Also: `note_a_reader_photograph_is_not_a_reason()` in preflight.py was
firing a WARN on kyo_017/kyo_019 for lacking age+measurement despite
both carrying their own city/park government source; refined the check
to treat a verified source as a reason too, same as an age or a
measurement, rather than flip it to a build-breaking FAIL on two
legitimately-sourced trees. And 21 pages (long place names: national
parks, German/Slovak compounds, American "City, State") were falling
through to a bare "Ancient Trees in X" title with no count or age hook;
added a compact fallback that rescues 20 of the 21 (Chapel Hill, North
Carolina genuinely does not fit). Full detail in LOG.md.

## 2026-09-13 (continuation 3) - 3 submissions processed: 1 pin correction applied, 2 empty test rows

Submission 104 (kind: correction, Baarn, brn_001 the Cantonspark Dawn
Redwood): the reader moved the pin 175 m from the published position, which
our pin already carried as `approximate`. Checked the arithmetic (haversine
on the two coordinate pairs confirms ~176 m) and checked it against three
"Watercypres"-labelled sightings held on 2026-09-08 as ambiguous between
brn_001, brn_002 and an unmapped specimen (`data/leads/_sightings.json`,
ff725d9a and siblings): the corrected position sits ~34 m from that earlier
photo, well inside the same cluster. Per the 2026-09-08 rule (a reader's GPS
fix beats a pin we already call approximate), moved brn_001 to
52.20753,5.298514 and rewrote the address, the honest note and the
recognise line, which still said "main entrance" under the old pin. Kept
`location_precision: approximate` rather than promoting to confirmed: the
corrected spot sits only ~51 m from brn_002 (the giant sequoia) in the old
pinetum, and the underlying species-identity ambiguity from 09-08 was never
resolved, only narrowed. Outcome `changed` recorded on the row.

Submissions 102 and 103 (kind: tree, both Fukuoka, both from the same GPS
point, no name, no why, no species): 103's paired sighting (d0e24fa3) was
already looked at and logged as a feature test (feet on a bed, no tree,
commit 8c23a6bf); 102 has no sighting row in Supabase at all, so no photo
ever backed it. Both outcomes recorded `holds`; nothing to publish or chase.

All three rows are the `a8ca51da` account, which `data/our-accounts.json`
already identifies as Hidde's own (sha1 matches "Hidde's own account"), so
`contributor_reply.py`'s `ours.is_ours` filter means the reply_text set on
each row will never actually mail him.

## 2026-09-13 (continuation 2) - Breda's bre_010 photo hunt: dead end, documented

`photo_gaps.py --shortlist` printed one candidate for The Plane of
Valkenberg's Edge (bre_010, no photo). Looked at the pixels of all three
candidates in its queue entry: "Gevallen blad van een boom in het gras.jpg"
is a single fallen leaf on grass, no tree in frame at all (and categorised
as maple, while bre_010 is a London Plane); the other two ("Lake-Valkenberg-
Breda.jpg", "Stadspark-Valkenberg-Breda.jpg") are wide park/canal views
already rejected once for the neighbouring bre_003 on 2026-08-13 for the
same reason, no single tree identifiable as the subject. All three recorded
`judged`/rejected in `data/photo-queue.json` so a future sweep does not
re-serve them. Photo-less gap stays honest and open; the other 260
photo-less published cities have not cleared the five-tree threshold that
makes them eligible for this rung.

Also checked Taormina, Ravenna, Trier and Niagara Falls against
`city_queue.py --next`'s "openable today" list for new coverage: all four
are documented dead ends or too thin to open. Taormina's five register
trees are all blocked on access (same hotel grounds, already recorded
2026-08-31/2026-09-08). Ravenna and Niagara Falls have only one in-town
register/wikidata candidate each, the rest 15+ km away. Trier's nine
"nearby" register rows are all Luxembourg entries 10-20 km distant, not
Trier supply. None cleared the four-tree floor's worth of real, walkable
candidates. `scout_next.py --target` confirms nothing left to scout this
window either (BUILD, not SCOUT, and nothing left at the top to build from).

## 2026-09-13 (continuation) - Tokyo 17 -> 21, kyo_017 gets its first photo

Finished a standing verify claim on Tokyo: 4 trees added (tok_018 The Great
Zelkova of Nerima Hakusan Shrine, tok_019 The Great Ginkgo of Oji Shrine,
tok_020 The Kaya of Zenyo-ji, tok_021 The Child-Rearing Ginkgo of Zoshigaya
Kishimojin), all flagged (age estimates are tradition, and two carry an
honest unresolved girth discrepancy between sources rather than a picked
winner), 0 photos. 3 register/Wikidata candidates turned out to be
duplicates of trees already published; 2 blocked (an avenue with no single
surviving specimen worth the walk, a school with no evidence of public
access); 6 left as unresearched leads in `data/leads/tokyo.json`. Japanese
overlay (`data/i18n/ja/tokyo.json`) translated and grown to match.

Separately, a reader photograph (Hidde's own account, filed like any other
per the 2026-09-08 rule) closed kyo_017's photo gap after a viewing pass:
two duplicate frames and one mismatched photo of a different tree entirely
(taken 19 seconds earlier on the same walk, at the same app-recorded
coordinate, which is the known CollectSheet own-pin gap rather than
evidence either way) were sorted from the one that actually matches the
recognise line's gate and wall.

Two new Fukuoka submissions (Hidde's own account) came in mid-session: one
photographed a tree 818m from anything we publish, filed as a lead; the
other has no synced photo yet and was left for a later run to pick up.

## 2026-09-13 - Milan 24 -> 25: the fourth Villa Litta plane, written

Write pass on the single verified tree in `data/research/milan-verified.json`,
**mil_025 La Pianta di Manzoni** (London Plane, Parco di Villa Litta Modignani,
Affori). 1 tree added, 1 flagged, 1 photo missing. `location_precision:
confirmed`, on MASAF's sheet-14 point and a long-standing OSM node agreeing to
within 8 m.

The whole writing job here was keeping one bridge claim out of the prose, in a
city that has already been served a BLOCKER for exactly that failure. The tree's
local name is Manzoni's; Villa Litta was Count Trivulzio's salon in the
nineteenth century and local histories name Alessandro Manzoni among its
visitors. **No source joins those two facts**, so the story does not either. It
states the name, states the salon, says in plain words that nobody has recorded
why the tree carries the name, and asks the reader who knows. That is the
publish-and-ask pattern rather than a hedge.

Two other honesty points carried from `verify_notes` into the prose rather than
left in the data:

- **Girth 410 cm is not register data.** MASAF's sheet 14 has no girth field
  filled at all (`girth_cm` is null in our own import). The 4.1 m comes from a
  2020 OSM edit whose note cites a plaque near the tree, so the story attributes
  it to a plaque copied down by a passer-by rather than to a survey. The height,
  28 m, is the register's own and is presented as such.
- **No age, and none derived.** Nothing publishes one, and this register carries
  no age field for any entry it holds, which the story says rather than
  apologising for. No derivation from the park's own 1700s planting era, which
  would have been the bridge claim its sibling mil_015 deliberately avoided.

No `best_time`: a single plane with no documented peak, and the park's fused
Siamese pair (mil_015) already holds the bare-silhouette badge in this city.

Count promises fixed on both language sides, all of them already stale before
this tree: the English intro still said twenty-three at 24 trees, the meta
description and free-to-visit FAQ twenty-four, `question_meta` twenty-three
more; the Italian overlay's title, meta description, intro, `question_meta` and
FAQ all still said 23. Italian translation for mil_025 written the same day,
because preflight refuses a short overlay outright rather than degrading one
page.

Still open in `data/leads/milan.json`: **MASAF sheet 15** (257 m from mil_015, no
girth, no name, no OSM node at its coordinate) stays a lead, and the verify pass
added a new one, the Parco Nord Milano *Patriarchi del Parco* trail map, which
names 30 specimens and gives no coordinate, girth or age for any of them.

## 2026-09-13 - Alicante 19 -> 21: two press-corroborated pairs written up

Write pass on the two verified trees the Alicante verify pass left in
`data/research/alicante-verified.json`. Both are groups rather than single
trunks, both rest on the same 2013 Diario Información survey of the city's
biggest and oldest trees, and both carry `curation_status: flagged`.

- **ali_020 The Centenary Elms of Panteón de Quijano** (Field Elm), the same
  small fenced garden as the already-published ali_017 araucaria, which is why
  `passcheck --pending` flagged it as a possible duplicate at 0 m. Checked by
  hand: different species, different trees, one park-level coordinate, so it
  ships as its own entry on `location_precision: approximate`, matching
  ali_017. Honest gaps stated on the page rather than filled: nobody has
  published how many elms stand here, no girth, no height, no register entry
  of their own, and the page asks the reader for the count. Age is the
  source's own language, nineteenth century and centenary, and is NOT derived
  from the garden's own 1855-1857 build date, which is the bridge claim the
  verify notes flagged. Last explicit confirmation of life is the 2013
  article's account of the 1990 trunk-rot surgery, hence flagged.
- **ali_021 The Silky Oaks of Passeig de Canalejas** (Grevillea robusta), two
  Generalitat register entries (3070 and 3071) about 11 m apart, folded into
  one entry on the twin rule, `confirmed` pin at the midpoint. The register's
  two girths disagree by more than triple (1.05 m against 3.75 m) for a pair
  the newspaper treats as matched; heights agree (19 m and 18 m). The story
  says both figures and leaves the discrepancy unexplained rather than picking
  a winner. No age derived from girth: the species grows fast, so the century
  is the newspaper's word and nothing more. The paseo's 1886 design date is in
  the prose as a fact about the promenade, explicitly not as a planting date.

Neither tree gets a `best_time`: the field elm phenology file peaks at `nice`,
and no species file exists for Grevillea robusta. Both photos `missing`, both
free and open, both carry a `how_to_recognise` line. Spanish overlay written
for both the same day (a short overlay refuses the whole build). Count
promises fixed in the city intro, meta_description, question_context and the
Spanish title. Build clean, `qa.py` clean (8,697 pages), `preflight.py` 598
cities and 0 problems.

## 2026-09-13 - Gdansk 6 -> 12: the Park Oliwski dendrological cluster written up

Write pass on the six verified trees the Gdansk verify pass left in
`data/research/gdansk-verified.json`. All six stand in Park Oliwski im. Adama
Mickiewicza in Oliwa, within a few hundred metres of each other, which turns a
page of four scattered singletons into an actual afternoon's walk. All six are
free, public park, `location_precision: confirmed`, and all six carry
`curation_status: flagged` from the verify pass.

- **gda_007 The Maples of Hugo Conwentz** (Field Maple): register twins folded
  into one entry, 245/180 cm. Designated 26 Feb 2026, the newest natural
  monument on the whole Gdansk list. The verify notes flagged the Conwentz
  biography as needing an independent check before use, so the story attributes
  it ("widely credited with") rather than asserting it, and says outright that
  the register does not explain why these trees carry his name.
- **gda_008 The Ginkgo of Park Oliwski**, 201 cm. No age anywhere; left empty
  and turned into a question on the page rather than a girth-derived guess.
- **gda_009 The Cucumber Magnolia of Park Oliwski**, 271 cm. No age; no growth
  rate published for Magnolia acuminata at this latitude to derive one from,
  stated plainly.
- **gda_010 The Three-Trunked Katsura of Park Oliwski**, stems 168/189/158 cm.
  No age, but the species ceiling is real and is in the story: Cercidiphyllum
  japonicum reached Western collections only after 1865.
- **gda_011 The Giant Thuja of Park Oliwski**, 219 cm, the headline tree of a
  four-tree register group (two yews and a Nootka cypress beside it). No age.
- **gda_012 The Ivy Elm of Park Oliwski**, 420 cm, by the pond, protected 1988
  under a register name that describes the flowering ivy on it. Age 150-250
  years, girth-derived, kept broad and said to be girth-derived.

**Photos: 6 of 6 missing.** The verify notes cite a named Commons file for four
of them (833. ginko biloba gdansk.jpg, 837. magnolia gdansk oliwa.jpg, 838.
grujecznik gdansk oliwa.jpg, 836 skupienie oliwa.jpg, Wiaz z kwitnacym
bluszczem.JPG), so this is a live photo lane rather than a dead end: it needs a
viewing pass, not a new hunt. Not attempted here, photo hunting is not a write
pass's job.

**best_time set on 3 of 6, left empty on 3.** Ginkgo (Oct/Nov gold), katsura
(October, the fallen leaves smell of burnt sugar) and the ivy elm (late Sept
into Oct, when the ivy flowers and pulls in wasps and late bees). The thuja is
evergreen and gets none; the maples and the magnolia have no moment strong
enough to spend the badge on.

**Two species common names harmonised** to what other city files already use:
"Katsura Tree" -> "Katsura (Cercidiphyllum japonicum)" and "Western Redcedar" ->
"Western Red Cedar (Thuja plicata)". The Latin names, which are the verified
fact, are untouched; the build fails on one species under two common names.

**Count promises fixed** across the page: intro, meta_description,
question_meta and the "Are these trees free to visit?" FAQ all still said six.
The first intro rewrite overran Contract C's 60-100 word cap at 158 words and
preflight caught it; cut back to 97.

**The Lawson Cypress lead in `data/leads/gdansk.json` was NOT written.** Its own
note says "not verified this pass", and a write pass verifies nothing. It is a
good candidate in the same walkable cluster, 212 cm, register 830, and it needs
a verify pass rather than a writer. Left in the leads file untouched.

## 2026-09-13 - Berlin 21 -> 23: a wingnut resolved, and the Queen's own oak found beside it

Dispatched a register-backed verify pass on Berlin (target 30, real
unmined supply: 546 Naturdenkmale rows + 648 Wikidata candidates), flagged
by a prior continuation today as the best-supplied unexhausted deepen
target on the whole queue. Focused on the Tiergarten Englischer Garten
cluster, ~13 Naturdenkmal entries within 400m of the already-published
ber_010 (Giant Sequoia), because it was already proven walkable.

**ber_022, The Englischer Garten Wingnut** (Caucasian Wingnut): the register
(1-39/B) plus an independent 2022 blog.inberlin.de article that names and
locates the same tree "near the teahouse", within ~4m of the OSM-mapped
Teehaus. No age documented anywhere, flagged and stated plainly rather than
guessed.

**ber_023, The Queen's Oak of the Englischer Garten** (Northern Red Oak,
not a register tree): two independent Tagesspiegel articles agree Queen
Elizabeth II personally planted it on 27 May 1965 during her first visit to
West Berlin, sapling reportedly from Windsor Castle stock. No exact
coordinate in either source, so `location_precision: approximate`, pin
centred on the Teehaus.

The rest of the cluster (Metasequoia, Libanon-Eiche, Silber-Linde,
Flatter-Ulme, Japanischer Kuchenbaum x2, Stiel-Eiche, Robinia) stayed
single-sourced: the register, Wikidata and de.wikipedia's district list all
trace to the same 2021 government ordinance (confirmed by fetching the
ordinance itself), which carries no age or girth field. Caught and
discarded a WebSearch-summary fabrication in the process: a claimed
"circumference 1825" for the Libanon-Eiche was actually a Flurstueck
(land parcel) number repeated identically across five unrelated trees, not
a measurement.

Wrote both stories (write-stories pass, small batch), added the German
i18n overlay entries for both (title count 21 -> 23; `de/berlin` had been
the only translated overlay for this city and would otherwise have
refused the whole build per Contract J). `preflight.py`, `i18ncheck.py`
and a full `npx astro build` all clean. Cost: ~95k verify + ~40k write,
2 trees, logged in `data/agent-costs.json`.

## 2026-09-13 - Sintra: sixth consecutive verify pass confirms exhaustion, 0 trees

Dispatched a verify pass on Sintra (target 20, was at 5, real ICNF register
supply looked promising at first glance: 30 unmined of 49 candidates within
20km). Every candidate within the walkable radius turned out to be either
already published or already `blocked` in `data/leads/sintra.json` by one of
the five prior passes. Checked genuinely new angles this time rather than
re-running the register sweep: serradesintra.net's grandes-arvores page (its
one named entry, "Feteira da Rainha," is a place, not a tree), Monserrate's
other official recanto pages (generic, no individual specimens), the Feteira
da Rainha recanto itself (a "tuia-gigante" likely already published as
sin_001, plus an uncorroborated travel-article claim of "two enormous
sequoias" left as an open lead, no measurement or pin), Convento dos
Capuchos (a WebSearch AI-summary invented specific ash/plane trees there;
neither the official page nor English Wikipedia mentions them, caught and
discarded per the search-summary-is-a-lead-never-a-source rule), and Jardim
da Preta (a legend about a viewpoint, not a tree). Appended a dated note to
`data/leads/sintra.json` so a seventh pass does not re-walk this ground.

**Honest conclusion: Sintra's five published trees are likely near its
ceiling at the current evidence bar**, short of the target of 20, unless a
future pass gets working access to monumentaltrees.com's Monserrate page or
a source individually names and measures a Sintra sequoia, ash or box
specimen. Cost: ~78k tokens, 0 trees, logged in data/agent-costs.json.

## 2026-09-12 (continuation 19) - Zwolle 14 -> 16, two flagged trees finished from a stranded verify pass

Found `data/research/zwolle-verified.json` uncommitted at session start: 2 fully
verified trees (zwo_015 the Plume Elm of Potgietersingel, zwo_016 Huis de
Paddestoel's Swamp Cypress), produced by an earlier attempt in this window that
stopped without writing them up. Both single-register-sourced, both flagged.
zwo_015's species is genuinely unsettled between the register's own two passes
(Ulmus x hollandica vs Ulmus sp.); page asks the reader. zwo_016's address in
the register (Herenweg 33) does not match its own coordinate (near Herenweg
131-133); the verify pass's reverse-geocoding and a 1991 archive photo caption
resolve this as almost certainly a register typo rather than two trees, cross-
checked against the municipality's own 2015 list which carries only one
Taxodium on the whole street. Wrote both stories and recognition lines
directly rather than dispatching a write-stories agent for 2 trees. Also
released a stale "Berlin verify" claim from the same earlier attempt, which
produced no output (Berlin's recognition lines, committed separately, were
unrelated finished work, already applied).

## 2026-09-12 (continuation 12) - Breda bre_010 photo candidate rejected after looking at it

`photo_gaps.py --shortlist`'s only candidate this pass was "File:Gevallen
blad van een boom in het gras.jpg" for bre_010 (The Plane of Valkenberg's
Edge). Fetched and viewed the actual pixels: it is a close-up of a single
fallen leaf lying on grass, not a photograph of the tree at all (the
Commons description confirms it, "fallen leaf of a tree on the grass").
Fails the Cadiz standard outright. Left bre_010's photo status as
`missing`; do not re-surface this filename for this tree.
## 2026-09-12 - Baarn, +1 tree (town hall plane), and 17 more sitting in the register

Added brn_008 from a newspaper clipping Hidde photographed. Baarn 7 -> 8
trees, 0 flagged, 1 photo missing (no open-licensed image exists; the press
photograph is credited Gemeente Baarn).

What could NOT be verified this session: the other five trees nominated for
a TreeTag in Baarn. The Baarnsche Courant names the count (six, five of them
put forward by werkgroep Baarn Natuurlijk Groen) and not the trees.
baarn.nl, baarnschecourant.nl, mooibaarn.nl and boomkronen.eu are all
refused by this session's egress proxy (403 on CONNECT), so the municipal
list at www.baarn.nl/ontdek-de-bijzondere-bomen-van-baarn was confirmed to
exist via search and never read. This is a network limit of the session, not
an exhausted hunt: a run with open egress should read it before treating
this as closed.

Worth keeping: 44 LRMB rows carry municipality Baarn, we map 11 of them, and
17 of the rest are visitable=ja with a non-private owner, so they clear hard
rule 10 from the register's own fields. Oldest first they are the Moseik and
the Valse acacia (both 1750-1800), the Bruine beuk in the garden of the
Apostolisch Genootschap (1810-1820), the Beuk in the Paleistuin (1850-1860),
then a run of 1860-1870 trees including the Tulpenboom and the Gewone plataan
at Paleis Soestdijk, the Rabobank horse chestnut and the Zilveresdoorn on the
Tromplaan. Twelve more are privately owned and stay out; one is visitable
only by appointment. Nobody needs to research Baarn from zero again.

## 2026-09-12 (continuation 11) - Finished an earlier attempt's Amersfoort/Breda claims; week budget nearly spent

Inherited two standing register-verify claims (breda, amersfoort) whose
work was already complete but uncommitted: Amersfoort 8 -> 14 trees,
Breda 4 -> 10 trees, both from the Landelijk Register Monumentale Bomen
(2024 edition), each new tree flagged (single register source). Ran
preflight, superlatives and a full astro build (clean, 5514 pages, exit
0) before committing, then released both claims. Also found and
committed a park page for Ottawa's Dominion Arboretum that an earlier
commit (5e92ac33) had written but never staged.

Checked `leads.py --ready`: only 3 candidates, and all 3 turn out to be
false positives on inspection (Genoa's was explicitly declined for
padding risk, Prague's is still blocked on unconfirmed access, Lagos's
is a negative-research-result record, not a tree). Nothing to dispatch
a write pass on.

Checked `city_queue.py --next` for a new city to open: Taormina and
Ravenna, the two highest-ranked options with register supply, are both
already documented dead ends (2026-09-11 entry above). Everything else
openable today (Adelaide, Zagreb, Lagos, Niagara Falls, Wellington,
Mechelen, Gran Canaria, Kilkenny, Izmir, Stirling, Canterbury, Evora,
Stratford-upon-Avon, La Palma) has only 1-2 Wikidata leads each, below
the six-candidate floor for a single-city pass; a batched pass across
several of them is the shape that would work but was not started this
attempt.

Stopped here rather than start one: `run_health.py --week` read
4855/5000 minutes with roughly 145 left, shared with Hidde's own usage.
Starting a new multi-city research pass risked either eating most of
what remains of the week's shared budget or dying mid-way on the usage
limit, which is a worse outcome than a short, clean attempt that shipped
14 finished trees across two cities.

## 2026-09-12 (continuation 10) - Ottawa 14 -> 19; Helmond register pass found only duplicates

Ottawa: 5 new trees from the NCC "A Living Legacy" register, all in the
Dominion Arboretum, verified with two sources each (register plus Friends
of the Central Experimental Farm's CelebriTrees tour or an independent
species page) and public access confirmed rather than assumed. Full detail
in LOG.md.

Helmond: a register-backed verify pass on 5 unmined LRMB candidates within
the existing walk found all 5 are exact-coordinate duplicates of already-
published trees (hlm_011/012/013/015/018) under new register-adjacent ids.
Not published. Recorded in data/leads/helmond.json (status: duplicate, with
the register id of the live twin each one matches) so a future pass does
not re-mine these same rows expecting new trees. This is a passcheck gap
worth naming: its "unmined" candidate list did not flag these five as
near-duplicates the way it correctly flags others "within 80m of a live
tree", and nobody has yet worked out why those five specifically slipped
through.

## 2026-09-11 (continuation 8) - Prague 27 -> 30: three Praha 8 oaks from the AOPK register

Finished a standing verify claim on Prague left by the previous attempt in
this window (claimed, never researched). Mined the unmined AOPK register
rows 5-7km northeast of the centre: prg_028 The Oak Behind the Ranger's
Lodge, Cimicky haj (Bohnice, girth 381cm, deliberately the living half of a
once-paired oak whose bigger, more famous neighbour is confirmed dead per
Czech Wikipedia's own extinct-oaks category), prg_029 The Oak of Pod
Labutkou Street (Liben, girth 314cm, an ordinary street oak with an
unusually intact ground-level crown), prg_030 The Oak of Kobylisy
(Sidliste Dablice, girth 436cm, the largest tree in a housing-estate park
on the site of a former military range). All three register+cs.wikipedia
sourced, flagged rather than confirmed on two fully independent sources,
all free and unrestricted. One new lead added: Cedr atlasky Na Balkane
(Atlas cedar, Prague's only protected one), inside a tennis club whose
public-facing offer does not settle whether the tree itself is reachable
without booking a court.

The write pass had transliterated every Czech place name to plain ASCII
(Cimicky haj, Pod Labutkou, Strelnicna, Liben, Dablice); restored proper
diacritics before merging, checked directly against the register's own
name_cz field (Cimicky haj, Pod Labutkou, Strelnicna, Libe, Dablice) rather
than from memory. Also fixed two stale tree-count mentions in the city's
own copy (meta_description and question_meta both still said 27).

**A qa.py failure fixed along the way, unrelated to Prague**: two orphaned
Lisbon photo files (lis_005's `-500`/`-1000` sized copies, saved under a
slug with an extra "the-" that matched neither the tree's own photo.url nor
photo-manifest.json). Confirmed no reference anywhere in data, scripts or
site/src, deleted them, qa.py clean again.

**A photo viewing pass on Tilburg's one fetchable candidate** (biggest gap
on `photo_gaps.py --shortlist`) rejected on sight: the matched file was a
fallen Ginkgo leaf in the grass, not til_018's Flowering Ash. Recorded via
photo_verdicts.py.

**REVIEW.md's two open WARNs from today's fresh-eyes review turned out
already fixed**, just not rebuilt: the broken empty `<figcaption>Photo:
</figcaption>` on reader-app photos with no attribution, and the three
self-repeating tree-page titles ("The X: X in City"). Read the current
source for both (PhotoFigure.astro/images.ts, and `[city]/[tree].astro`'s
`nameEchoesSpecies` guard) and confirmed the fixes are in place and the
built site is clean; nothing further to do.

**Taormina and Ravenna checked and passed over for new coverage.**
Taormina's register is a documented dead end (all in-town candidates
blocked on hotel-grounds access, confirmed again by re-reading its own
leads file rather than re-researching). Ravenna's four register candidates
are 17-19km apart with no walkable cluster and only one close to the
centre, below the six-candidate minimum for a pass. Claimed Rome instead
(30 trees, the single highest-impression depth-allowed city per the latest
digest) for a verify pass on its own unmined near-centre register
candidates; see the next entry for the result.

## 2026-09-11 (continuation) - Milan 23 -> 24 trees; Alicante's register confirmed exhausted; Finch Arboretum park page

Dispatched two parallel verify passes (isolated worktrees) on Alicante and
Milan, both deepen targets with real Search Console demand and register
supply that `passcheck.py --brief` reported as substantially unmined.

**Both briefs turned out to be stale.** Alicante's "43 unmined" candidates
all cross-matched by coordinate to leads already resolved by five prior
passes (published, held, or blocked); the register there is genuinely
exhausted, confirmed independently a third time. Milan's "52 unmined"
candidates likewise all resolved to duplicates, already-blocked entries
(the children-only Villa Belgiojoso garden), or one already-published
tree, except for one genuinely open pair. `passcheck.py`'s "unmined" count
does not currently discount leads a prior pass has already resolved by
coordinate; both agents caught this themselves rather than trusting the
brief, cross-checked the full register against `data/leads/` before
reporting, and left sharper notes behind so a future brief-reader does not
repeat the check. Worth a fix in `passcheck.py --brief` itself: whoever
next touches it should have it subtract resolved leads from the "unmined"
count before printing it, so the number means what it says.

**Milan, 23 -> 24 trees.** mil_024, "I Platani di Villa Litta Modignani":
two more MASAF-registered planes in the same park as the already-published
Siamese pair (mil_015) and La Pianta di Affori (mil_009), folded into one
entry per the register-twins rule (12m apart). Single-sourced and flagged;
the register puts the larger at 43m, which the story flags honestly as
possibly the tallest tree on the page rather than asserting it, since a
differently-dated citation of the same underlying MASAF dataset (an
it.wikipedia rescrape) gives smaller, disagreeing figures for the same
park and neither is silently preferred. Wrote the story and its Italian
overlay translation in-session (Milan ships in Italian; the build refuses
an incomplete overlay). Fixed two Contract C overruns preflight caught
(question_meta length, a stale "twenty-three" count in the FAQ paid-entry
answer). Build, qa.py, i18ncheck.py and preflight.py all clean.

**Alicante, unchanged at 16.** No new trees; the one open lead (a possible
third fig near the Castillo de Santa Barbara elevator entrance, referenced
in a single 2026-08-04 news event) had its coordinates sharpened via
Overpass but still fails the two-source bar. Left as a lead for a future
pass with photo-comparison tooling.

**New park page**, earned by this session's earlier Spokane write pass
pushing Finch Arboretum's tree count to 6: `data/parks/john-a-finch-
arboretum-spokane.json` (Contract H). `pagegaps.py` clean afterward.

Both agent cost lines logged in `data/agent-costs.json`. Both claims
released.

## 2026-09-11 (continuation) - Spokane deepened to 13; four other claimed READY leads declined after reading them

`leads.py --ready` listed 8 trees across five cities (spokane 4, hallstatt 1,
lagos-pt 1, genoa 1, prague 1) as needing only a story. Claimed all five, then
read every underlying lead in `data/leads/` before writing anything, since the
tool's own docstring warns it is a proxy (any pass leaving prose counts as
"source evidence", not a guarantee the tree should ship). Four of the five
turned out not to be ready on inspection; writing them as-is would have shipped
either a non-tree, a padding risk the previous pass had already flagged, or a
hard-rule-10 access question three prior attempts had failed to settle.

**Spokane, 9 -> 13 trees**, the only city whose leads genuinely needed only
prose. All four are Spokane Heritage Tree Register entries, single-sourced and
flagged per Step 2's rule that one source ships rather than holds a tree back:
spk_011 The Towering Norwegian (Norway spruce, ~123ft, register's own second-
tallest-in-the-city claim), spk_012 Powerful Pine (Mexican pinyon, one of the
state's largest, an odd transplant for the Inland Northwest), spk_013 Chief
Garry Park Champion (sycamore, a state size candidate, its own story
distinguishing it from a different variegated sycamore maple HistoryLink names
in Browne's Addition so the two are never merged), spk_014 The Littleleaf
Linden (Moore-Turner Heritage Gardens cluster, ~110 years, species left
genuinely open on the page because the register's own record contradicts
itself, title says littleleaf, description says American). Fixed a species-
naming collision before merging (spk_013 had drafted as "Sycamore Maple",
hard rule 9 wants the one name ~20 other cities already use, "Sycamore") and
two Contract C overruns (intro, meta_description) plus one how_to_recognise
overrun (spk_014) that preflight caught. Build, qa.py, superlatives.py and
preflight.py all clean. Claim released.

**Hallstatt, declined.** The one READY lead, a copper beech (Blutbuche) near
the Gosau forestry office, is 9km from Hallstatt centre in a different village,
with no age or girth, and the pass that found it explicitly deferred all three
Gosau candidates (this beech plus a wych elm and a school linden, all within
100m of each other) for "a future pass that covers Gosau" as its own cluster.
It only surfaced as READY because its "not pursued this pass" phrasing sits
mid-sentence rather than at the start, which is what `leads.py`'s
NOT_READY_MARKER regex actually matches (worth a look for whoever next touches
that script; not fixed here). Shipping one third of a deferred three-tree
cluster alone, under the wrong city, would pre-empt that future pass for no
gain. Left as a lead.

**Lagos (PT), declined.** The single "READY" entry is not a tree: it is the
previous pass's own negative-result note ("No further register or named
candidates found in Lagos town itself"), with `species: "n/a"`. It cleared
`leads.py`'s readiness check only because the note itself counts as source
evidence and nothing checks that `species` is a real species. Nothing to
write; the note already records where a future pass should look next
(the named parish churches, Ponta da Piedade, a direct approach to Camara
Municipal de Lagos).

**Genoa, declined.** The one READY lead is a second Cinnamomum glanduliferum
at Villa Durazzo Pallavicini, and the lead's own text already argues against
shipping it: the park already holds one Cinnamomum-family tree (gnv_009) and
a second one of the same genus stands nearby (gnv_004), so a third this close
together "risks reading as padding rather than a distinct entry unless it's
visibly a different, separately worthwhile specimen." No new evidence this
pass that it is. Left as a lead pending a reason to treat it as distinct.

**Prague, declined.** The one READY lead, an oak at the Dejvice sports ground
(Dub na sportovisti v Dejvicich), has been checked for public access three
times across three separate passes (2026-09-10 x2, plus the Czech Wikipedia
read) and every attempt came back the same way: it stands at a fence between
a kindergarten and a sports ground, no source establishes a public path
reaches that specific edge, and hard rule 10 says leave it out on a guess.
Its own `why` field documents this in full and ends "Leave as a lead until a
street-level photo or map shows a public way actually touching that NE
fence." Shipping it now would have overridden that finding on no new
evidence. Left as a lead; needs a street-level photo, not another search.

Claims released for all five cities. Logged spokane's pass in
`data/agent-costs.json`.

## 2026-09-11 (continuation) - Baltimore and Boise open at 4 trees each

Committing verify+write work an earlier attempt in this window had already staged
but not merged (city files sat untracked, claims still held). Checked both files
against the research standard before shipping rather than trusting the claim:
both clear the four-tree floor, every tree has honest sourcing (two of Baltimore's
four and one of Boise's four are single-sourced and flagged accordingly, per
Step 2's rule that a single source ships rather than holds a tree back), and
location_precision is set honestly (confirmed where a source gives a trunk-level
fix, approximate everywhere else).

**Baltimore, 4 trees.** The Ruxton Liberty Tree (bal_001), a 350-380 year old
white oak on private land, viewable from the public road at Dunlora Road and
Bellona Avenue, its owners paying for 5,000 gallons of weekly watering to keep it
alive; the Frederick Douglass Elm (bal_002) near Camden Yards, an undated English
elm carrying an unproven but honestly-labelled local tradition that Douglass
planted it as an enslaved child; and two Cylburn Arboretum champions, a cockspur
hawthorn (bal_003, single-sourced, flagged) and a paperbark maple (bal_004,
two sources). Both arboretum trees carry only park-level coordinates
(location_precision: approximate) since neither this pass nor the Maryland Big
Tree Program's JS-rendered database gave an exact spot; a future pass with a
JS-capable fetch could tighten both. Photos missing on all four, an honest gap.

**Boise, 4 trees.** Three Idaho state/city champions from the University of
Idaho's Big Tree Program register (largest bur oak, largest Kentucky coffeetree,
both in Julia Davis Park; largest giant sequoia, moved a quarter mile by flatbed
in 2017 so St. Luke's Hospital could expand without felling it) plus a horse
chestnut sapling grafted from the Amsterdam tree Anne Frank watched from the
annex window, one of only eleven such grafts in the US, now older than the storm-
felled 2010 parent. None of the three champions carry a documented age (Idaho's
register measures size, not years, stated honestly on the page rather than
guessed). Photos missing on all four.

Also ran, since both cities had never been resolved in other languages:
`scripts/city_names.py` (found local-name variants for both, no action needed
beyond the alias file update), `scripts/city_queue.py` (re-ranked, rebuilt
CITY_QUEUE.md and LEDGER.html), `scripts/tree_index.py` (67,610 trees indexed),
`scripts/superlatives.py` (364 claims, no collisions), full Astro build and
`scripts/qa.py` (8550 pages, clean). Both claims released. Note: city-list.json's
rebuild only updates rows already present in the file and does not add new ones,
so Baltimore and Boise do not yet appear there; harmless since nothing but
brief.py reads city/status from it and CITY_QUEUE.md (the actual order) carries
both correctly, but worth a look if a future session is touching that script.

## 2026-09-11 (continuation) - Tallinn deepened to 6: the Tammesalu Oak, Tallinn's thickest tree

Verify pass on Tallinn (5 trees, rank 109, real demand: 36 impressions in the
10-day window) found the Kadriorg register candidates were mostly already-leaded
ornamental cultivars on residential streets, but a dendrologist's press ranking
(Postimees 2017, corroborated by Loodusajakiri 2024 and Kadriorg Park's own site)
named Tallinn's single thickest tree: an oak in the old Tammesalu grove, already
substantial when Peter the Great bought the land in 1714, predating both Kadriorg
Palace and the park built around it. Two measurements eight years apart (637cm
2016, 648cm 2024) give a consistent, well-sourced girth-based age estimate of
300-400 years. Shipped as tln_006, `location_precision: approximate` (no source
gives a trunk-level GPS fix, only "the grove's northeastern part, by Kirdetiik
pond"). Wrote the story in-session and updated the city's intro, meta description,
question page and FAQ, all of which hard-coded "five trees" and needed the count
bumped to six; preflight caught the resulting word-count overruns (intro, story,
question_context) and a stale "three more" in question_meta, all fixed before
commit. Three more single-sourced leads (2 candidate oldest-tree oaks, 1
cemetery-park oak) banked in `data/leads/tallinn.json` for a future pass. Build,
qa.py and preflight.py all clean. Claim released, logged in
`data/agent-costs.json`.

## 2026-09-11 (continuation) - Sorrento deepen pass: register confirmed exhausted, 0 trees

Dispatched a verify pass on Sorrento (7 trees live, rank 111, real demand: 27
impressions/2 clicks in the 10-day window) since the MASAF register still showed
"31 unmined" candidates in passcheck's brief. Cross-referencing every candidate by
coordinate and MASAF sheet_id (rather than by name, the method that let these keep
resurfacing as "unmined") found every close-in row is either already published or
already blocked under a different name in `data/leads/sorrento.json` (the Antico
Parco del Principe trio, the Grand Hotel Parco dei Principi grounds, the Via Carlo
Amalfi cedar, the Villa Thuja eucalyptus), and every distant row belongs to a
different comune (Vico Equense, Castellammare di Stabia, Agerola, Pompei, Ravello).
Independently confirms the 2026-09-09 deepen pass's identical finding: this
register is exhausted at Sorrento's radius. The one open lead, a pine on Via
Bagnulo with a disputed August 2026 collapse report, stays unresolved after a
second independent check (a Positanonews AI search summary fabricated a sentence
not in the actual article; the real 2020 piece raises the risk prior without
settling which tree fell). Two new wrong-container leads recorded for a future
Vico Equense page. Claim released, no trees added. Logged in `data/agent-costs.json`.

## 2026-09-11 (continuation) - Two unprocessed submissions (100, 101): a third GPS-only Kyoto lead, a plain worth-it vote

Submission #100 (kind `tree`, `page: app:collect`, same account as 98/99): another
bare GPS pin near Kyoto Gyoen with no name, species or photo, 914m from the nearest
published tree (kyo_016/kyo_019, Omiya Gate). Same shape as the two already recorded
2026-09-10, so recorded the same way: added as a thin lead to `data/leads/kyoto.json`,
`outcome: open_question` set on the row, and this time a `reply_text` was actually
composed (the account is answerable and the prior two were left without one), asking
for a name, species or photo. Submission #101 (kind `feedback`, `why: "worth it"`) on
Tamba's tmb_001: a plain positive vote, no free-text complaint, nothing to check
against sources. Set `outcome: holds`, no reply needed, matching the standing pattern
(Utrecht #63, Amsterdam #40, Sardinia #39, Rome). Both ids added to
`data/submissions-processed.json`.

## 2026-09-11 (continuation) - Lausanne, Minneapolis, Salamanca, Spokane opened; Monterey deepened to 3

Merged the results of a verify pass an earlier attempt this window left
uncommitted: Lausanne 8 trees flagged (7 approximate pins, 1 confirmed;
several with disputed ages between the city's own register and its tourist
office, printed as disagreements rather than resolved), Salamanca 4 (1 with
no age at all, stated plainly), Minneapolis 4 (mostly city-park champions
with thin single-newspaper sourcing, flagged), Spokane 6 (3 old-growth
Douglas firs resting on one 2019 newspaper feature, flagged; 3 more from the
city's own Heritage Tree Registry cross-checked against a 2012 HistoryLink
survey). Wrote the 5 stories the verify pass had left undone via a
write-stories agent, then wrote each city's page-level content (intro,
meta_description, the oldest-tree question page, FAQ) from the same verified
facts and merged all four into `data/cities/`.

Also added mty_002 (Old Veteran of Point Lobos) and mty_003 (Moon Tree of
Friendly Plaza) to the already-published Monterey, previously trimmed to
just the Lone Cypress by a prior continuation the same day pending "a 4th
tree or an independent fame case." Treated this as ordinary city growth
(Monterey already has a page) rather than a new below-floor decision;
flagged in LOG.md as a judgement call in case Hidde reads the close call
differently.

Released the Boise and Baltimore claims: both still sit at 2 verified trees
with nothing that clearly clears the "would someone travel for this one
tree" bar (Boise's moved sequoia and Baltimore's Liberty Tree are good local
stories, not obviously destination-tier), so both stay banked in their
research files rather than shipping padded or under a stretched exception.
Lagos-PT (1 tree, unconfirmed public access) stays banked too.

## 2026-09-11 (continuation 4) - 4 stranded verify passes shipped under the single-famous-tree exception: Indianapolis, Sao Paulo, Busan, Monterey

Continuing the same window's earlier finding (6 cities banked below the 4-tree
floor with finished stories, logged in the prior LOG.md entry). Re-checked
`passcheck.py --pending` and found 4 more sitting in the same state that the
prior continuation had not resolved: Indianapolis (1), Sao Paulo (1), Busan
(2) and Monterey (3), all fully verified and written, none merged because
none reaches four.

Rather than leave these banked again, applied the 2026-08-31 single-famous-tree
exception (DECISIONS.md) to each on its own merits, following the precedent of
Kasukabe/Aguas de Moura/Rumskulla (single trees) and Zilina (a 3-tree page
shipped whole under the same exception):

- **Indianapolis** (ind_001, the Kile Oak): largest bur oak in the metro,
  protected by one family's promise since 1928, an international visitor
  guestbook kept since then. Ships alone.
- **Sao Paulo** (spa_001, Figueira das Lagrimas): reportedly the oldest
  documented tree in a city of 12 million, heritage-listed since 1989, real
  historical weight (soldiers and students said goodbye here). Ships alone.
- **Busan** (bsn_001/002): both independently designated South Korean Natural
  Monuments (No. 168 and No. 270), not a hero-plus-filler page; each one
  clears the fame bar on its own. Fixed a hard-rule-9 collision on the way in
  (bsn_002's species said "Black Pine / Japanese Black Pine", two names for
  Pinus thunbergii; corrected to the one already used for Hiroshima and
  Kagoshima's designated pines).
- **Monterey**: trimmed from 3 candidates to just mty_001, the Lone Cypress,
  a registered trademark and (by any account) the most photographed tree on
  the California coast, comfortably the clearest single-tree case of the
  four. Held mty_002 (Old Veteran of Point Lobos) and mty_003 (Moon Tree) back
  in `data/research/monterey-verified.json`, already written, for a future
  pass to add once the city has a 4th tree or its own independent fame case.

This is a judgement call, flagged as such because it is a close one: the
exception's worked examples (Angel Oak, Castagno dei Cento Cavalli, Bartram's
Ginkgo) are solitary trees, and Busan bends that to two independently-famous
trees at two different sites in the same city rather than one ensemble. The
Zilina precedent (a hero plus two companions) suggests this is within the
exception's intended range rather than outside it, but it is Hidde's to
overrule if he reads it differently.

Left Baltimore (2), Boise (2), Lausanne (3), Minneapolis (3), Salamanca (3),
Spokane (3) and Lagos-PT (1) banked as before: none of their hero trees read
as clearly "would somebody travel specifically for this" (Boise's moved
sequoia and Baltimore's Liberty Tree are good local stories but not
obviously destination-tier), and Lagos-PT's cork oak additionally has
unconfirmed public access, which would need resolving before it could ship
under any rule. A future pass should either find each of these a tree to
close the floor, or make an explicit fame case the way this entry did.

Regenerated `data/tree-index.json`, ran `preflight.py` (0 problems after
fixing the Busan species name and a stale Zwolle tree-count/meta_description
left over from the Zwolle merge in the next entry), `superlatives.py` (no
collisions), full `astro build` and `qa.py`.

