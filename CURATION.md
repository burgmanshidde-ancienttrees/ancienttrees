


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
## 2026-09-23 (late) - Copenhagen: 26 trees, 19 flagged, 26 photos missing

Second write pass on Copenhagen, finishing a claim an earlier attempt in
this window left uncommitted: cop_017 through cop_042. Five are Dyrehave
veteran oaks 11-13km north of the city (day-trip, like the three already
published); the rest sit inside Copenhagen itself, in J.C. Jacobsens Have,
Bispebjerg and Vestre cemeteries, Landbohojskolens Have and street trees.
19 of 26 flagged, mostly single-sourced or an approximate pin; none dead,
none fabricated, all alive and publicly accessible. All 26 still need a
photo. Rewrote the city intro, question_context and two FAQ answers that
had gone stale: the thickest-tree claim now correctly names the London
Plane of Landbohojskolens Have (6.71m, inside the city) rather than a tree
that predates this batch.

## 2026-09-23 - Friedewald and Bad Homburg, from reader submissions

**Friedewald: 1 tree, 0 flagged, 0 photos missing.** The Hammundeseiche,
8.65m girth (2015, breast height) and 8.77m at 1m (2001), 25m tall, crown
20m, estimated 350-440 years by Kuhn & Kuhn (2007) and Frohlich (2000) via
de.wikipedia; second source kuppenrhoen.de for the deserted village, the
1141 first mention, the 1312 abandonment and the walking route. Pin
confirmed: Wikidata Q1573933, de.wikipedia and the submitter's own
coordinate agree within about 10m. Two photographs, both looked at.

NOT USED: kuppenrhoen.de says Mercator's 1592 map marks a notable tree at
this place, which the 350-440 estimate cannot easily be squared with. Left
as two facts rather than joined. An older 1000-year claim is called
unreliable by its own source and is not repeated. The best whole-tree
photograph otherwise available (Hammundeseiche,2.jpg, public domain) scores
POOR on photo_light.py, backlit with a blown sky, and was rejected for the
2009 panoramio shot at 800x600.

**Bad Homburg: 4 trees, 4 flagged, 3 photos missing.** All in the
Schlosspark. Three of the four rest on one source, the baumkunde.de forum
thread carrying Rainer Lippert's 2021 survey of the park, hence the flags.

Two gaps published as gaps rather than guessed:
- The cedar's SPECIES. The city of Bad Homburg's page is titled
  "Libanonzeder" and its own text calls the tree an Atlaszeder; baumkunde
  registers it as Libanon Zeder. The page says disputed and asks.
- The AGE of the oak and the plane. Both are wider than the dated cedar and
  neither has ever been dated. The park's own dates (a garden from 1441,
  baroque from 1680, English landscape from the later 18th century) are not
  attached to any particular trunk by any source, so they are not attached
  here. The page asks.

Also checked and kept apart: the Naturdenkmal "Eiche am Forellenteich" is a
different oak, 4.30m, 2.5km west in Dornholzhausen. In leads.

monumentaltrees.com returned 403 to WebFetch on the Schlosspark page, so the
cross-check of the forum's measurements against a second measurer could not
be done.

## 2026-09-19 (continuation) - The Pamplona poplar/plane growth rate does not exist for one of the two species, checked against the actual Forestry Commission source

The 2026-09-18 Pamplona entry below said a sourced girth-increment rate for
Populus nigra and Platanus x acerifolia "unblocks 24 trees site-wide" and
called it "one sourced growth rate away from being free." Checked properly
against John White's 1998 Forestry Commission paper (FCIN12, "Estimating
the Age of Large and Veteran Trees in Britain"), the actual source behind
`scripts/ages.py`'s own method: this is true for only one of the two species.

**Poplar has no entry at all.** White's Table 1a, the core-development growth
table for 20 named genera (oak, beech, chestnut, plane, lime, sycamore and so
on), does not include Populus in any form. Paragraph 5 says why: "Pioneers
such as poplar, willow and alder frequently have a productive but short
formative period and then go straight into senescence," skipping the
mature-state CAI phase the whole method depends on. Poplar is not a species
missing a rate by oversight, it is a species the method's own author
considers unsuited to it, for the same structural reason yew is (paragraph 5
again), just at the opposite end of the growth-speed scale. Forcing a linear
rate onto it would not be finding a sourced number, it would be inventing a
method the source itself declines to offer.

**Plane does have an entry, and it does not fit ages.py's model either.**
Table 1a gives Plane, "average site, garden, parkland" (the closest match to
a register specimen), as 70 years core age at a 5mm annual ring width. That
is a RADIAL figure: converted to girth (2 x pi x ring width), it is about
3.14 cm/year during the core phase, which is higher than the generic
"fast, open-grown" ceiling (2.5 cm/year) `ages.py` currently uses as its
refusal threshold for plane, confirming the refusal is correctly calibrated.
But White's method is not a constant rate: after the core phase, ring WIDTH
narrows as the tree thickens because ring AREA (not width) stays constant,
so a mature plane's true average girth rate is well under 3.14 cm/year and
falls further with age. Plugging 3.14 into `ages.py`'s existing simple
girth/rate formula would systematically UNDER-estimate old planes' ages,
the same direction of error the script's own retrospective already measured
for its existing rate on big trunks generally.

Doing this properly means implementing White's actual two-phase calculation
(core basal area at the table's rate, then remaining basal area divided by
the mature-state CAI from Table 2), not extending the existing linear model
with a third number. That is real, worthwhile engineering, but it is a
method change to a script whose current 6-in-10 accuracy is measured and
trusted, and it deserves the same validation-against-300-known-ages rigor
`ages.py`'s header describes, which a research pass should not skip to
close out one city's photo/age checklist. Filed here rather than attempted
half-built. The source PDF (Forestry Commission FCIN12, November 1998, Crown
copyright, ISBN 0-85538-383-6) is at
https://www.ancienttreeforum.co.uk/wp-content/uploads/2015/03/John-White-estimating-file-pdf.pdf
should curl fail on it again (it 403s to a plain user agent; WebFetch's
browser path gets through). Table 1a's Plane row, all site categories, for
whoever picks this up: champion tree potential 100/6mm, good/open/sheltered
60/6mm, average/garden/parkland 70/5mm, churchyard 70/5mm; no entry for
poor ground, woodland-boundary pollard or inside-woodland categories.

## 2026-09-19 (night run, continuation) - Finished an earlier attempt's uncommitted work: Senonches and Réno-Valdieu, plus two photos and two ONF-panel ages found while finishing them

Resumed a window that had stopped after 54 minutes with 66 unspent, having
shipped nothing despite the work being done. `data/cities/senonches.json`
(4 trees) and `data/cities/reno-valdieu.json` (4 trees), both flagged
`needs_curation`, both drawn from `data/research/famousfrance-verified.json`
and `data/leads/_famous-france.json`, are now live and verified clean.

**Senonches**: Chêne Fauteuil (5-stem oak, 300-340y, 680cm girth, safety
perimeter for falling deadwood), Les Trois Frères (3-stem oak, ~340y,
550cm), a sweet chestnut at Rond de Condé (undated, flagged), and a ring of
seven 1854-seed giant sequoias plus a cedar at Rond de Monsieur. All free,
all on one official waymarked "venerable trees" loop.

**Réno-Valdieu**, 28-30km away: four oaks in the "série artistique de la
Gautrie" dedicated to Oxford, Aberdeen, the Forestry Commission and a
forestry congress, at Carrefour Degraine, all four sharing one pin
(honest: nothing in any source separates the trunks) and all flagged.

**Photo hunt on the leads file's own candidate list found two tree photos
and, unexpectedly, two ONF interpretive panels.** All six candidates
fetched and viewed against the Cadiz standard. Approved (CC BY-SA, Le
Passant, via Wikimedia Commons): sno_001, sno_002, rvd_001, rvd_002.

The two panel photos, at Réno-Valdieu, were not usable as tree photos but
were usable as sources: each gives a real forestry-survey figure for one
named oak, 360 years in 2006 (about 380 today), a girth (383cm Forestry
Commission, 343cm Oxford) and a height (43m both). Both trees had been
carrying only the série-wide "200 to 350, sources disagree"; they now
carry their own derived age, girth and height, sourced to the panel photo.

**The same two panels, worded identically, name the fourth oak "le Xème
Congrès Forestier Mondial."** ONF manages the forest and wrote the signs,
which settles a numbering dispute the story had left open against a hiking
site calling it the eleventh. Renamed rvd_004 to "Chêne du Xe Congrès
Forestier" and said so plainly in the story, disagreement included.
rvd_003 (Aberdeen) has no panel and stays at 200-350, flagged.

Updated reno-valdieu.json's intro, meta_description, question fields and
FAQ for the two now-individually-dated trees, then trimmed seven fields
(`preflight.py` catches length caps; the edits pushed intro, both meta
fields, and three `how_to_recognise` lines over SEO_GEO_BLUEPRINT's
limits). `preflight.py`: 0 problems. Local `npx astro build`: clean.
Released both standing claims (senonches, reno-valdieu).

## 2026-09-18 (session 11, continuation) - Three translation batches: German, French, Japanese, 15 cities

`langcheck.py --next` named the top untranslated city per proven language
area (de, es, fr, ja all past their English twin per city). Batched the
three with more than one candidate worth a pass: `transbrief.py --brief de
regensburg cologne baldenhain` (3 cities, 11 trees), `--brief fr bordeaux
lyon venon lausanne nantes` (5 cities, 33 trees), `--brief ja takeo uda
nagano yabu nagoya miyazaki otoyo` (7 cities, 24 trees). Dispatched all
three as translate passes in parallel (Opus, per the agent's own model
pin), applied each answer with `transbrief.py --apply`, fixed two overlong
meta fields the German pass produced (baldenhain's meta_description,
regensburg's question_meta, both over the 155-char cap), and confirmed
`i18ncheck.py` clean at 82 overlays (was 67 going in).

**The French pass caught a real bug in the English source while
translating it**: `data/cities/lyon.json`'s `question_meta` said "eleven
more" trees where Lyon holds 13 (1 named + 11 = 12, not 13), stale since
some earlier growth pass added a tree without updating this line. Fixed
the English to "twelve more" in the same session so both languages agree;
the French overlay already had the correct count because the translator
wrote what was true rather than what the English said.

Verified with a full local `astro build` (12,103 pages) and `qa.py`
(16,031 pages, clean) before committing. Nothing else was found broken;
one lesson recorded for future translation batches: pick by measured
impressions per city per CLAUDE.md's rung 0b correction, not by fame, and
`langcheck.py --next` already does that.

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

## 2026-09-18 (later) Pamplona's Villava trio had the wrong distances, and the shortlist could never have named this city

Two corrections to the entry below, both from measuring rather than reading.

**The distances between the three Villava poplars were wrong in seven places**,
across two access fields, two recognition lines and two stories. Measured from
our own coordinates: pam_011 to pam_012 is **60 m** (we said 240), pam_011 to
pam_013 is **181 m** (we said 400), pam_012 to pam_013 is 240 m (we said 400).
The cardinal directions were right and only the figures were wrong, which is
how it survived: pam_012 is the southernmost, pam_011 the middle, pam_013 the
north end. All seven now carry the measured figure.

This is worse than an ordinary slip because of which trees it was on. pam_012's
own recognition line opens "You can recognise it by position and little else",
and then gave the position as four times the real distance. A visitor pacing
240 metres north for the broken-limbed poplar walks past it at 60 and ends up
at the third tree. Position is the only thing separating these trunks, by our
own admission, so on these three it is not a detail, it is the entry.

**Item 1 of the list below (fold the Villava twins) should not be done on this
evidence.** 60 m apart is not the Setubal case: those were separately
registered trunks metres apart, distinguishable only by girth. pam_011 is
distinguishable in its own right (three main limbs, one dead and bare, bark
coming away) and pam_013 is a Lombardy poplar, a narrow column rather than a
spreading crown. Only pam_012 is undistinguishable, and the shared 314 cm
girth is not evidence of duplication either: three separate trees in this
register carry exactly 314, which reads as a banded figure rather than a
coincidence. Leaving all three, with the real distances, is the honest answer;
folding one would delete a live page to make a thin one look tidier, which is
the Leiden lesson pointing the wrong way.

**Item 3 could not have happened as written.** It says Pamplona "belongs at
the top of photo_gaps.py --shortlist", and the shortlist can only ever print a
city that already has a candidate on file. Pamplona's queue is swept to sweep
5 twice over, on 09-09 and 09-16, and 13 of its 14 trees came back with no
candidate at all, so it appeared on no list anywhere and nothing routed it to
the medicine this file already names. `photo_gaps.py --shortlist` now ends with
a STARVED block: demand cities where every queued candidate is judged or none
was ever found, worst waste first, with the right command per city (the last
resort for a swept-and-empty city, the ordinary sweep for trees never queued,
because sending one to the other burns a window on a question already
answered). It names twelve cities holding 337 unphotographed trees between
them, Pamplona at the top on 448 impressions, and not one of them has ever
been through photo_last_resort.py.

Not run here: this sandbox's network policy refuses commons.wikimedia.org
outright (403 on CONNECT), so the last-resort sweep is a night run's job. The
CI runner reaches Wikimedia fine, measured 2026-09-01.

**A third thing, found by reading the rendered page rather than the data: 242
live pages print an internal tree id to the reader.** Pamplona had seven of
them, in access and transport lines like "the same path segment as pam_012
(about 60m south)" and "about 1.4km beyond the Villava trio (pam_011/012/013)".
All seven are gone here, replaced by what the reader can actually use ("the
southernmost of the three", "the Lombardy poplar at the north end", "the
pollarded poplar at Rochapea").

The other 235 are across many cities (Warsaw, Alicante, Den Bosch, Brisbane,
Deventer, Leeuwarden, Arnhem, Quebec City, Lausanne, Trieste and more; the list
is reproducible by stripping script, style and head, then tags, from every file
under site/dist and matching `[a-z]{3,4}_0\d\d` in what is left). It happens
wherever a pass cross-referenced one tree from another's access or transport
field, which is a sensible thing to write and the wrong place to leave a
database key.

**Deliberately NOT made a build check tonight.** A FAIL would refuse every
deploy until all 235 are rewritten, which is self-inflicted breakage and the
"gate that enforces polish" trap this corpus already names once. The rewrites
are not mechanical either: each id has to become a phrase a visitor can follow,
which is a judgement per sentence. It is worth a batch pass of its own, and the
check belongs in the same change that empties the backlog.

**And trying it found a worse bug than the one it was sent to fix.**
`photo_last_resort.py` swallowed the network error, returned an empty list, and
then stamped `last_resort` with today's date on all fourteen Pamplona trees.
Every one printed "0 new". So a run that reached Commons not once had written
into the queue that the last resort was tried here and found nothing, which is
the exact verdict that would keep the site's most wasted city out of every
future hunt. It also means any `last_resort` stamp written from a sandbox since
this tool existed may be worth nothing, though the 181 stamps on file are all
from cities a night run swept (Utrecht 28, Caserta 20, Deventer 12) and none of
the twelve starved cities carries one.

Fixed rather than worked around: `near_files()` returns None when Commons
cannot be reached and [] when it answers and holds nothing, an unreachable tree
is printed as `unreachable` and gets no stamp at all, and a run where nothing
could be checked exits 1 saying so. The stamps this session wrote were
reverted. `--shortlist`'s STARVED block now also reports a city whose trees are
already through the last resort, so nobody spends a window asking twice.

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

