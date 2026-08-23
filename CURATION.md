

<!-- archive-index -->

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-08](archive/CURATION-2026-08.md)
- [2026-07](archive/CURATION-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.
<!-- archive-index -->

## 2026-08-23 - Finished an abandoned write claim: Warsaw +2, Berlin +1, Turin held

A prior attempt this same window claimed berlin, warsaw and turin for a write pass at 08:19, then never touched them, doing unrelated work instead and leaving the claim standing. `leads.py --ready` showed 3 candidates each in all three, but most turned out thinner than the READY label suggests (that check only confirms name+species+position, not sourcing or access), so this pass verified each individually rather than writing all 9.

**Warsaw (+2, 7 to 9):** The Szustra Oaks (war_009, five oaks registered as one 1978 designation) and the SGGW Oak (war_010, declared 1974, standing on the site of the university's original 1923-1956 Mokotow campus before it moved to Ursynow). Both single-sourced from the register, both flagged, second sources used only for setting/access (the park's own page and zabytek.pl for the Szuster estate; SGGW's own history page for the campus). A third Warsaw lead, the Karol Oak, stayed a lead: far from the existing cluster and never researched past the register.

**Berlin (+1, 18 to 19):** The Copper Beech of the Fraenkel Garden (ber_019), Naturdenkmal ND 5-56/B in the public Landhausgarten Dr. Max Fraenkel at Kladow (reopened to the public 2016). Register point sat 270m from the garden's own mapped grounds, so the pin uses the garden's centroid instead, marked approximate. Added the missing German translation entry (data/i18n/de/berlin.json), since the DE build fails hard on any untranslated tree. A second Berlin lead, an oak at Fuerstenbrunner Weg 30, turned out to sit in the Villenkolonie Westend, a private villa district (OSM classes the point a residential house); blocked on hard rule 10, no evidence the plot is public ground. A third, a weeping-beech-and-common-beech pair sharing one averaged coordinate that is actually ~400m from each in reality, stays a lead: publishing one pin for two trees 400m apart would fake precision.

**Turin (0, still 10):** Both candidates researched turned out not shippable. The Plane of Parco di Villa Rey is on the grounds of ASI's (Automotoclub Storico Italiano) national headquarters, open only for scheduled FAI/Open House events or by appointment, not walk-in public; blocked on hard rule 10's first test. The wide plane east of the Po (reg_id 006/L219/TO/01, 640cm girth, oddly short at 14m, likely pollarded) still has no name and no second source; a reverse geocode of its coordinate returned "Villa Rey" as the nearest OSM feature but the point sits 1.8km from Villa Rey's own registered tree, so that is probably just sparse tagging on the Sassi hillside rather than evidence of the actual site. Left as a lead with the geocode note for whoever picks it up with better local knowledge.

Released all three claims. Build and qa.py both pass (qa's one remaining failure, sitemap lastmod, is the pre-existing shallow-checkout environment issue, unrelated). preflight.py and superlatives.py both clean.

FOR HIDDE: nothing blocks. The 8 unclaimed minutes this window's first attempt left on the table went into finishing what it started rather than opening anything new.

## 2026-08-23 - Seville deepened 20 to 37 from its own municipal catalogue

`leads.py --ready` showed 26 candidates sitting in `data/leads/seville.json`, all from the city's own 2022 Inventario de Arboles Singulares (the same municipal catalogue four already-published Seville trees, sev_017 to sev_020, already draw on), each carrying real dendrometry and vitality fields rather than a bare species-and-location line. Seville clears the demand bar this rung requires (50 ten-day impressions), so deepening an already-at-target city (20/20) was in scope. Wrote 17 of the 26: 5 thicken the Parque de María Luisa cluster (an araucaria, two planes, a stone pine, a bald cypress), 4 more join the Real Alcázar cluster (a windmill palm, a bougainvillea trained as a small tree, a European fan palm, a cycad correctly described as not actually a palm), and 8 stand alone across the city (a cemetery cypress, a 42 m eucalyptus with two named pests, a Triana fig, a mulberry by an Expo-park farmstead, a Senegal date palm, a university-campus Canary pine, a 32 m tipu tree, and Parasenegalia visco, a South American species almost never planted in Europe). Held back the remaining 9: 7 rated only "Regular" condition and one (a lagunaria) the leads file's own note says needs a second source before it ships, both left for a future pass; the last (a ficus at a private nursing home's garden) was dropped outright, since Hermanitas de los Pobres' grounds fail hard rule 10's access test. Species naming needed one fix mid-build: Chamaerops humilis had to match Padua's existing "European Fan Palm / Saint Peter's Palm" rather than a shorter name I'd written, per hard rule 9. Fixed the city's question_meta and one FAQ answer, both of which still counted the old 20. All 17 single-sourced from the catalogue, flagged, no photos.

FOR HIDDE: nothing blocks.

## 2026-08-23 - Four Dutch cities open at once: Heerlen, Oss, Roosendaal, Sittard-Geleen

A write pass on `python3 scripts/leads.py --ready` found four fully-verified, story-less LRMB register files sitting staged (`data/research/{heerlen,oss,roosendaal,sittard-geleen}-verified.json`), 30 candidate trees between them, all above the 4-tree floor. Wrote stories for all four and published them as new cities, 28 trees total.

**Heerlen (8):** two oaks on the wooded Terworm/Eyckholt estate grounds, a neighbourhood oak from the 1920s mining-colony era, a lime banded to the 1600s with no other history recorded, the plane everyone in town calls the Oak of Terworm (probably planted in 1749 for an heir's birth), a tulip tree in a former miners' park, a castle-drive ginkgo, a town-hall catalpa. hee_003's species had to move from "Oak (Quercus sp.)" to "Oak (Quercus, species not established)" mid-build: hard rule 9 caught it colliding with Austin's unrelated "Live Oak (Quercus sp.)" entries under the same Latin string.

**Oss (6):** two village limes and a named-by-year (1928) sycamore in Macharen, a churchyard beech in Haren, a horse chestnut in Oss itself, and Megen's "Lulboom", a 1937 royal wedding lime the register itself records twice as adjoining entries; folded into one story rather than two, since a visitor sees one planting.

**Roosendaal (7):** a rare Oriental plane and a horse chestnut sharing De Kring square, a catalpa and a London plane framing one building on Burgerhoutsestraat, a beech behind a restaurant, a fast-growing poplar on a car park, a second chestnut by the Van Loonpark pond. Its own park lime, the register's original fifth candidate there, was declared dead in 1998 per the register's own site_history and never shipped, per the never-dead-trees rule.

**Sittard-Geleen (7):** three Geleen trees tracing the district's mining-era growth (a station red oak, a street sycamore, and an oak the register's own surveyor is rooting for against a housing development on the neighbouring plot), plus a poet's-garden copper beech and ash, and a Stadspark pin oak and tulip tree.

All 28 single-sourced LRMB, all flagged, no photos. Build and qa.py both pass.

FOR HIDDE: nothing blocks.

## 2026-08-23 - Cork 5 to 13, on a newly-scouted national register

`scripts/scout_next.py --target` pointed at Cork for register scouting (published, but no register supply on file and no scouting verdict, because the register itself had never been logged in `data/register-scouting.json` despite already being live). Found `data/registers/ireland-heritage-trees.json` (Heritage Trees of Ireland, National Biodiversity Data Centre, CC-BY 4.0, 724 trees island-wide) was already imported and in use on 2026-08-08/09 for Dublin, with a working Irish Grid to lat/long converter at `scripts/irish_grid.py`; a first pass here nearly re-imported and overwrote it as a fresh find before the "M" in `git status` (not "??") caught it. Re-used the existing conversion instead. Cork's page already draws on Blarney and Fota, so those two sites' public status was established; checked the register's Blarney/Fota entries against the 5 already-published trees, skipped two near-certain duplicates within 60m (a yew and a Western Red Cedar, same species, same site as cor_001/cor_002, confirmed by converting their coordinates), and shipped six new Fota trees (a camphor tree, a spiral-needled Japanese cedar cultivar, a Canary Island date palm, a New Zealand tanekaha, a holm oak, a coast redwood) plus two new Blarney trees (a Cappadocian maple, a beech), all with real converted coordinates. All single-sourced from the register, flagged. Fixed the city's meta_description and question_meta, which still said "five" and "four more". Logged the missing scouting verdict. Two more register clusters (Doneraille Park, The Gearagh nature reserve) turned up but sit 35-40 minutes from Cork city, past the day-trip boundary, so they wait in `data/leads/cork.json`. The register covers all of Ireland and has runway left for Galway, Limerick, Killarney, Kilkenny and Belfast, checked against each city's existing coverage first.

FOR HIDDE: nothing blocks.

## 2026-08-23 - Haarlemmermeer opens with 8, register exhausted

Finished the verify pass CURATION.md's previous entry had dispatched but left unrun: the 6 unmined Hoofddorp/Vijfhuizen/Badhoevedorp candidates from the LRMB register (`data/leads/haarlemmermeer-register.json`). Checked each against hard rule 10: a wingnut on the Markt (kept alive on the municipality's own condition when the shopping centre around it was built), a lime planted for Queen Wilhelmina's 1923 jubilee, a London plane in front of a notary's office (Hoofddorp's oldest registered tree, 1880s), and a weeping beech whose own 2024 register inspection says it "feels very unhappy" squeezed onto a ring-road corner all cleared the access test and shipped. A sixth, a maple on the Nieuwemeerdijk in Badhoevedorp, ships as view-only per the Hobart precedent: private front garden, but the register's own text says it is clearly visible from the road; its story also flags that the register contradicts itself on the planting date (1895 in the descriptive note, 1910-1920 in the structured field). A seventh, a beech at a private garden corner in Hoofddorp, stayed blocked for lack of any visibility evidence (`data/leads/haarlemmermeer.json`). Also set names on the three previously-written Nieuw-Vennep trees, which a prior write pass had left null. City now ships at 8 trees, all single-sourced LRMB, all flagged; no photos. Register supply for this gemeente is exhausted; a ninth tree would need a reader tip or a from-zero web sweep neither of which is warranted right now.

FOR HIDDE: nothing blocks.

## 2026-08-23 - Assen opens with 9, all LRMB register, all flagged

Finished a write pass a prior attempt this window had claimed and left half done (one story written, eight to go, in `data/research/assen-verified.json`). All nine trees come from the Landelijk Register Monumentale Bomen, single-sourced throughout, so every entry ships `curation_status: flagged`. Three share the private Overcingel estate (a horse chestnut in the register's top ereklasse, a hollowed oak with a 27m-to-14m veteran crown reduction, a bald cypress reduced to regrowth after its main trunk broke), two share a hidden pocket garden behind Nieuw Echten reached via a footpath between two front doors on Alteveerstraat (a weeping beech, a copper beech), and the remaining four stand in a deer park, the former Vredeveld estate (now Valkenstijn park), a private front garden visible from Beilerstraat (registered as the heaviest oak in Assen), and the former grounds of the Port Natal psychiatric hospital (now the Wilhelmina Ziekenhuis). No photos (`status: missing` throughout); no `best_time` on the weeping beech, the broken cypress or the two ageing/declining oaks (ass_002, ass_003), since none has a peak worth the badge this year. Build and qa.py both pass; qa's one failure (sitemap lastmod, shallow git checkout) is a pre-existing environment issue unrelated to this city. `data/city-queue.json`'s Assen stub flipped to published/9 trees.

FOR HIDDE: nothing blocks.

## 2026-08-23 (night) - Amsterdam 31 to 39, Zaanstad opens with 4, Haarlemmermeer held at 3

A write pass staged 15 register-sourced trees (a prior verify pass's shelf, all LRMB, all single-source flagged) across three Dutch cities; this session merged the output. Amsterdam gained 8 trees, all in Amstelveen (Broersepark, the Amsterdamse Bos, several street plantings), taking it from 31 to 39; its stale "31"/"21 free" copy and Dutch translation overlay (nl/amsterdam.json) both updated to match, since the build enforces full per-tree translation coverage on any city with an nl file. Zaanstad opened as a new city with 4 trees spread across Zaandam, Westzaan and Assendelft (a cemetery copper beech with a self-contradicting age in its own register entry, a plane that outlived the industrial Zaan waterfront, two declining horse chestnuts), full Contract C copy written from scratch. Haarlemmermeer's 3 written Nieuw-Vennep trees stay held in data/research/, one short of the 4-tree floor (2 of its original 5 register candidates were correctly blocked earlier on access grounds); a follow-up verify pass is dispatched on 6 unmined Hoofddorp candidates (a market-square wingnut, two planes, a weeping beech, two private-garden beeches needing an access check) to open a second cluster and clear the floor.

Also fixed a real bug found along the way: `scripts/city_queue.py`'s regeneration step (not `--next`, which was fine) crashed with a `KeyError: 'basis'` on the two 2026-08-22 stub queue entries for Zaanstad and Haarlemmermeer, which lack the field every properly-scored entry has. Two lines used `c["basis"]` instead of the `.get()` pattern the rest of the function already uses; fixed, queue regenerates clean now that Zaanstad is a live city.

Zero photo hunting or judging this run (night-runner egress rule); all 12 published trees carry an honest `missing` photo status.

FOR HIDDE: nothing blocks.

## 2026-08-22 (night) - Oahu published, 5 trees, all in one garden

A verify pass claimed earlier in the window found 5 trees, all inside Foster
Botanical Garden in downtown Honolulu (a baobab, a Bodhi tree grown from a
Bodh Gaya cutting, a kapok older than the garden itself, a cannonball tree
and a quipo), all within a five minute walk of each other. A write pass
turned them into stories and the city went live at /oahu with 5 of a target
10. No photos yet (all `status: missing`). One tree (hnl_003, the Hillebrand
Kapok) is flagged for an unresolved girth disagreement between two sources,
kept honest in the prose rather than resolved by picking one. hnl_004 (the
Cannonball Tree) has no recorded planting date; the story asks the reader
for it rather than hedging around the gap. Roughly 51 more register-listed
Exceptional Trees sit within 20km, still unmined by any pass (`passcheck.py
--brief Oahu`), so this city has plenty of cheap runway toward its target
of 10 for a future verify pass.

## 2026-08-22 (night) - A tree named after the wrong genus, and it needs the redirect work first

**kyo_016 is called "Chinkapin oak (Sudajii) of Omiya Gate" and is not an
oak.** Its own `species` field says Japanese Chinquapin, *Castanopsis
sieboldii*. Chinkapin oak is *Quercus muehlenbergii*, a North American oak,
and Castanopsis is not a Quercus at all. The name and the species field on the
same entry contradict each other, and the name is what a reader sees as the
page title. Sudajii is correct and is the Japanese name for the Castanopsis.

**Not fixed, and the reason is the same one blocking the umlaut URLs.** A tree
slug is derived from its name, so correcting this moves a published, indexed
URL, and the redirect machinery covers city slugs only. This now belongs with
the 17 tree URLs missing a letter (the German ß and Icelandic eth entries
recorded earlier today): one small feature, tree-slug redirects, unblocks all
eighteen fixes at once. Doing any of them without it trades a factual error
for a dead link, which is the worse of the two.

**Fixed in place, since neither touches a URL:**

- `kyo_013` sent visitors to "Keihan Marutamachi Station", which does not
  exist. The Keihan station is Jingu-Marutamachi; plain Marutamachi is the
  Karasuma subway stop roughly a kilometre west, on the far side of Kyoto
  Gyoen. A directions field pointing at the wrong station is the one class of
  error this project says it cannot afford, so this one did not wait.
- `kyo_015` said Kyoto Gyoen has been public ground "since the court left for
  Tokyo in 1877" while `kyo_012` dates the court's departure to 1869 and the
  clearing of the plots to 1877. The two events are separate now.

**Reported by the Kyoto pass and NOT acted on, because each needs a source in
hand rather than a judgement:**

- `kyo_001` "Hanayama's former minister Ieatsu" is very likely Kazan'in Ieatsu,
  a court noble, with 花山院 read as a place rather than as his surname.
- `kyo_009` "fuseki-dai sugi" mis-romanises fukujo-daisugi, and "Goshomigoyo"
  matches no term the pass could identify.
- `kyo_015` names "the Kyoto nurseryman Sano Toujiro" while `kyo_005` names
  "Sano Toemon XV" of the same sakuramori family. If those are one family, two
  of our pages are quietly telling one story about two people.
- `kyo_018` says another tree is "about a kilometre and a half north"; our own
  pins put it 945 metres away. Both pins are approximate, so this may be the
  pins rather than the prose.

## 2026-08-22 (evening) - The Vienna duplicate was invisible, and 17 URLs are missing a letter

**The vie_024 / vie_028 duplicate is resolved, and it turned out to cost
nothing.** Both entries carried the identical name "The Plane of Alser
Strasse", and `treeSlugsForCity` derives a slug from the NAME, so the two
collided on one URL and only one of them ever rendered. Checked against the
live site: `/vienna/plane-of-alser-strae` serves vie_028's story, and vie_024
has never had a page at all. So retiring vie_024 moved no published URL and
hard rule 3 never applied; the staging note from this morning was written
before anyone looked at what the slug function actually does. Removed from the
city file and from the German overlay. Vienna is 30 trees.

**Finding it exposed a bigger one. `slugify` silently drops any character
NFKD cannot decompose, and German ß is one of them.** The function normalises
to NFKD, strips combining marks, then strips everything non-ASCII. Scandinavian
å and ö survive that, because NFKD splits them into a letter plus a mark. ß has
no decomposition, so it is simply deleted, and "Strasse" becomes "strae".

17 live tree URLs are affected: Munich 11, Reykjavik 3, Vienna 2, Copenhagen 1.

    munich/norway-maple-of-herrnstrae     should be  ...herrnstrasse
    vienna/cemetery-plane-of-singerstrae  should be  ...singerstrasse
    reykjavik/whitebeam-of-vikurgarur     should be  ...vikurgardur   (eth)
    reykjavik/spruce-of-elliaarholmi      should be  ...ellidaarholmi (eth)

The fix is four lines, a transliteration table applied before normalising:
ss for ß, o for ø, ae for æ, oe for œ, l for ł, d for ð and đ, th for þ. Polish
ł has no live victims yet and will the moment a Wrocław street name reaches a
tree.

**Not applied here, deliberately, and this time hard rule 3 really does
apply**: unlike the duplicate, these URLs exist, are in the sitemap and are
what Google has indexed. Changing them needs redirects, and the redirect
machinery that exists (`RENAMED_CITY_SLUGS` in site/src/lib/redirect-map.ts)
covers CITY slugs, not tree slugs. So this is a small feature plus a data
migration, not a four-line patch, and it deserves its own session rather than
the tail of a long one.

Worth doing though: "leinthalerstrae" is not a word in any language, nobody
searches it, and it reads as a broken page to a German speaker, which is the
audience the German pages were just built for.

## 2026-08-22 (later) - Reader-facing fields were carrying notes we wrote to ourselves

The Palermo translation pass found it, and it is the most embarrassing thing
in today's batch because it was live and visible: the `access` and
`transport` fields render straight to visitors, and in 21 cities they were
carrying instructions to the writer and internal tree ids.

The worst examples, all live before this:

- `pal_010` access: "Confirm current opening hours and whether the fig's part
  of the grounds needs a booked visit before publishing a specific time."
- `pal_016` access: "State the caveat plainly and tell readers to check
  current hours before visiting rather than quoting an unverified schedule."
- `gnv_002`, `gnv_003`, `gnv_004` access: "Not confirmed this pass." /
  "Not established this pass."
- `com_006` access: "Same schedule as the Villa del Grumello cedar (com_005)".
  A reader has no idea what com_005 is.

63 fields across 18 cities were cleaned mechanically: internal ids stripped,
"this pass" removed, spacing repaired. Toulouse (11), Padua (10) and Nuremberg
(9) were the worst. Nothing factual changed; every hedge survives, it just
stopped narrating our own process, which CLAUDE.md's ratchet already lists as
one of the seven things that became build checks.

**And that is the finding: the build check did not catch this.** qa.py checks
rendered text for builder-speak, and these fields went through it. Worth a
look at whether it only checks story prose and not the short fields.

**A second checker gap, same session.** `scripts/superlatives.py` reports
"468 superlative claims, no two trees claiming the same crown" while
`mad_005` says the cypress is "both the oldest and the tallest tree" in the
Royal Botanic Garden and `mad_006` said the elm "wins on height" there and
called it "the garden's tallest resident". The checker matches phrasing, so a
paraphrase walks straight past it. Fixed the content (the cypress states 32
metres flatly, the elm only "over 30" with the measurements admitted to
disagree, so the elm's claim yielded), but the check still cannot see the
class.

That makes two contradictions in one day that a translation pass found and an
automated check missed, after the Paris girth pair. The pattern is that our
checks match strings and the errors are semantic. Worth deciding whether the
fresh-eyes reviewer should be pointed at superlatives specifically.

**Still open from earlier today:** vie_024 and vie_028 remain one tree under
two ids, staged because retiring an entry moves a published URL.

## 2026-08-22 - Six translation passes found four errors in our own English

Six overlays landed in one batch (Italian Rome, Dutch Amsterdam, German
Vienna, Portuguese Lisbon, French Paris, Japanese Tokyo). The translations are
the smaller half of what they produced. Rendering a story into another
language turns out to be a fresh-eyes review of the English, because a
translator cannot skim: every clause has to be understood before it can be
carried across, and the ones that do not survive that are the ones that were
never quite true.

**Fixed the same session, all live before this:**

- `tokyo` intro said the oldest tree "predates the Kamakura shogunate". Our own
  figure for tok_001 is 750 years, so about 1276, and the shogunate began in
  1185. The tree cannot predate it. Now "dates from the Kamakura period",
  which our own number supports.
- `tok_005` called Tokyo Tower "a 1930s landmark". It opened in 1958. The
  sentence has been rebuilt around the real date.
- `par_005` said the Monceau plane has "a waistline of seven metres" while
  `par_014` said "the thickest plane in Paris, in Parc Monceau, measures eight
  metres around", about the same tree. Both were wrong AND they contradicted
  each other on the site. par_005's own notes carry the Ville de Paris
  register figure, 645 cm. Both now say that.
- `par_009` said a tree planted in 1840 "was a 30 year old tree" in the 1860s.

**Not fixed, needs a check I cannot do offline:**

- `tok_009` credited the Meiji Jingu Gaien avenue to "Origeshi Yoshinobu",
  which is not a plausible romanisation. The Japanese pass reads it as
  Orishimo Yoshinobu (折下吉延) with high confidence, and that is very likely
  right, but I could not verify it from our own sources and hard rule 2 does
  not bend for a likely-right name. The garbled name is REMOVED rather than
  replaced, so the sentence now says "the landscape architect who laid it
  out". Restore the name once somebody confirms it; the Japanese overlay
  carries 折下吉延 already.

**BLOCKER-class, staged for the next session because it changes public URLs:**

- `vie_024` and `vie_028` are the same tree. Identical coordinates to the
  metre, the same Naturdenkmal register_id 3257866, the same Baumkataster
  baum_id 126884, the same 1894 planting and the same 315 cm girth, both named
  "The Plane of Alser Strasse". A visitor can collect one trunk twice, which
  is the exact fault the Potsdam and Berlin Pfaueninsel oaks were retired for
  on 2026-08-16. It was NOT retired on the spot because removing an entry
  moves a published URL, and hard rule 3 puts that above speed; it needs the
  slug and redirect handled deliberately rather than at the end of a long
  session.

**Two contradictions the passes flagged that are real and still open:**

- `amsterdam`: the intro calls the 35 m elm the city's tallest tree while
  ams_003 gives a poplar 38.5 m and leaves "is anything taller" open. Both
  renderings are faithful to the English, so the Dutch page now carries the
  same tension.
- `vienna` vie_006 asserts the 1783 reading in two sentences after presenting
  1783 versus 1876 as an open dispute. The German attaches those sentences to
  the older reading explicitly, which is better than the English does it.

**And a schema gap worth naming before it is discovered as a bug:**
`how_to_recognise` and `best_time` have no slot in the overlay format, so those
reader-facing lines render in ENGLISH on a translated page. Five Paris trees
carry a recognition line, and par_032's is load-bearing ("The square has two
enormous planes. This is the one the register pins..."). The French pass
folded three best_time moments into its prose as a workaround, which is a
reasonable stopgap and not a fix.

## 2026-08-22 (session, continued) - Vienna 28 to 31: Rathauspark's third plane, past its 30 target

Three trees, all confirmed-public: vie_029 completes Rathauspark's three-plane 1973 protection set (an earlier pass held it back as "padding"; it is the third of a designation that already exists as a trio, not a fourth plane added for its own sake). vie_030 (Black Pine, Ebner-Eschenbach-Park) and vie_031 (Sessile Oak, Prater/Belvedereallee) both needed checking against several genuinely private neighbours in the same register clusters (Wahring courtyard trees, Meiereistrasse sculptor's-studio planes) before shipping; those stayed blocked with sourced reasons in data/leads/vienna.json. Fixed two stale count promises preflight caught (meta_description "Twenty-eight", question_meta "twenty-six more"). Walk now 10.6 km (up from 10.1, still multiple clusters across a large city, each cluster itself tight). Vienna is now 1 over its 30 target, which CLAUDE.md treats as normal, not padding, since nothing was added to hit a number.

## 2026-08-22 (session, continued) - Haarlem 9 to 13: the Statenbolwerk stretch of De Bolwerken, one storm-felled beech found and blocked

## 2026-08-22 (session, continued) - Haarlem 9 to 13: the Statenbolwerk stretch of De Bolwerken, one storm-felled beech found and blocked

A verify pass tightened Haarlem's existing Kenaupark cluster rather than widening the walk: four new trees (haa_010 to haa_013) all sit 220-375 m from the nearest existing tree, in the Statenbolwerk section of De Bolwerken, the older (1828) Zocher-designed green ring the Kenaupark cluster (1865) sits inside. A ginkgo added to the lawn in the 1910s, an oak pair marking a path entrance (species left honestly undetermined, robur or petraea, since the register does not say), a four-beech ensemble, and a Caucasian wingnut in a private villa garden shipped as view-only per hard rule 10 (visible from the public footpath, register itself marks it visitable/visible, access line says plainly what a visitor does and does not get).

The pass also caught a real thing worth recording: a separate, single copper beech 200 m away at Statenbolwerk 2 was blown down by storm Eunice in February 2022 (two independent Dutch sources), and is now correctly BLOCKED in data/leads/haarlem.json rather than sitting there to be rediscovered and nearly shipped by a future pass. A second, similarly-old green beech nearby was left as a lead rather than verified, on the writer's own judgement that confusion risk with the fallen tree could not be ruled out this pass.

Updated two stale count promises preflight.py caught (question_meta "the full nine", an FAQ answer claiming "all nine stand" free and open): now 13, and the FAQ answer now says honestly that 12 of 13 are open access, the wingnut being the one view-only exception. Walk still spans 3.3 km, unchanged: the new trees tightened the cluster rather than widening it. Build, qa.py, superlatives.py and preflight.py all clean.

## 2026-08-22 (session) - Florence 22 to 23: one Boboli Gardens cypress, oldest-tree pin kept on the documented yew

A verify pass steered away from Florence's already-exhausted cheap leads (Bobolino stone pine etc., checked twice on 2026-08-21 and still single-sourced) and toward fresh, unmined MASAF register candidates instead. It found one: flo_023, The Cypress of the Boboli Gardens, Mediterranean Cypress, 357 cm girth, verified via matching MASAF/RAMI register codes 9 m apart. RAMI's own register states an age of "roughly 375 years, calculated from a registered birth year" but the underlying documentary basis was not found independently, so `curation_status: flagged` and the story hedges the figure as an estimate rather than a fact.

That estimate (age_max 400) technically exceeds flo_001's documented 306-year yew, which would have silently flipped the /florence/oldest-tree page's answer to a hedged register guess instead of a precisely documented 1720 planting. Set `oldest_tree_id: "flo_001"` explicitly (same mechanism Amsterdam's cycad uses) rather than let the raw age_max win: flo_001's whole point, already made in the page's own question_context, is that its age is not a guess. Build, qa.py and superlatives.py all clean (qa's one sitemap complaint is the sandbox's shallow git clone, unrelated).

Also this session: redacted Hidde's personal Gmail address from LOG.md (same PRINCIPLES.md #10 issue REVIEW.md flagged in CURATION.md and a run had already fixed there), wrote the Norway Maple species page intro (the one page gap pagegaps.py found), ran a free photo API sweep (40 more trees checked), and dispatched Haarlem and Vienna verify passes (register deepening, both still running/pending write at time of writing).

## 2026-08-22 (session) - The nine most-visited tree pages, checked; Newton's pin was 180 metres wrong

Hidde asked whether the pages people actually see carry errors. A verify pass
took the nine tree pages with the most Search Console traffic and checked five
things each: alive, pin, bridge claims, species and age, access. Four real
problems, all fixed the same hour.

**Newton's Apple Tree, Cambridge, is the serious one.** 113 impressions in ten
days, zero clicks, and a pin marked `confirmed` that sat at 52.20689, 0.115113,
an exact six-decimal match for Nominatim's centroid of Trinity College as a
whole. The tree stands outside the Great Gate, about 180 metres east. Two
independent checks agree: the geotag of our own approved photograph of this
tree (Geograph 5599349) and the CB2 1TQ postcode centroid from our own address
line. Moved to the photograph's coordinate. This is exactly the failure the
project says it cannot afford, it survived on a well-read page, and no check we
own would have caught it, because a plausible coordinate inside the right city
looks like every other coordinate.

**Amsterdam's Last Elm of Stationsplein carried an unflagged conflict.** Our
age band (about 120 years) comes from the national register's 1900-1910
planting band; De Correspondent quotes the city's own head tree consultant
giving 1889, backed by a 1906 archive photograph. Fifteen years apart, both
real. Recorded in verify_notes, published age left with the register, neither
picked as winner, per the two-source rule.

**Two smaller ones.** Green-Wood's own great-trees page has 404ed since we
cited it, so the citation now points at the Internet Archive snapshot rather
than nothing; and Singapore's Bodhi tree story said Captain Pearl planted the
hill with nutmeg, where NParks and Wikipedia both say pepper.

**What did NOT need fixing, which is worth as much:** Bath's plane, Malaga's
ficus avenue, the Athens holm oak, Dublin's sequoia and the Parc Monceau plane
all held up, pins included; the Paris one matched the city's own tree registry
to the metre.

Two upgrades left on the table, both cheap and both real: Green-Wood indexes
the sassafras as Section 54, between Forest and Locust Avenues, which would
turn an approximate pin into a confirmed one, and Dublin's sequoia still has no
tree-level coordinate.

## 2026-08-22 (session) - Munich 30 to 44: finished a write pass an earlier attempt in this window claimed and left unwritten

A prior attempt in this same usage window claimed Munich for a write pass (14 register-only leads verified and staged in `data/research/munich-verified.json`) and then stopped after 10 minutes without dispatching the pass. This session picked the claim up, dispatched `write-stories` on the 14 trees (muc_035-048), merged the result into `data/cities/munich.json`, and released the claim.

All 14 come from Munich's 2021 Naturdenkmalverordnung, single-source, no age and no girth on any of them; each ships flagged with an honest invitation for a reader to supply a date or a measurement. Caught and fixed one species-naming slip before merging: the writer delivered muc_035 as "Sycamore Maple (Acer pseudoplatanus)" against the corpus canonical "Sycamore (Acer pseudoplatanus)" (10 existing trees use the canonical form); renamed before merge so hard rule 9 and the build's one-species-one-name check don't trip. `best_time` set on 3 of 14 (muc_037 red oak, muc_040 beech, muc_042 maple), kept scarce since Munich already carries 17 best_times across its other 30 trees.

Build and `qa.py` both clean except one pre-existing false positive: `qa.py`'s sitemap lastmod check fails locally because this sandbox's git checkout is shallow (4 commits only), which flattens every page's last-source-commit date to today; this is a checkout-depth artifact, not a data problem, and doesn't reproduce on the real CI checkout.

Munich: 30 to 44 trees, still one published city, still needs a photo push (14/44 have one). Deleted `data/research/munich-verified.json` (fully merged).

## 2026-08-22 (session) - Nijmegen 11 to 12, one tree, and the rest recorded as leads/blocked

Finished the verify claim the previous attempt in this window left standing
(scout_next --target still said BUILD Nijmegen: 159 unjudged register trees,
nothing to scout). Picked 4 single-tree candidates from the LRMB register
around the centre, all confirmed via the register's own `n_trees` field to
be individual specimens rather than rows: several nearby cemetery entries
(n_trees 4, 12, 14, 28) were excluded before dispatch for exactly that
reason, they are avenue/row plantings, not collectible points.

**Shipped: nij_012, The Wilhelminaboom of Hertogplein** (Lime, species not
otherwise identified). A lime planted 1 September 1898 for Wilhelmina's
coronation, ringed by a wrought-iron fence whose crowns were removed by the
Germans and restored in 1948. Sources genuinely conflict on whether the
tree standing today is the 1898 original: Dutch Wikipedia says the old lime
"has made way for another"; a 2025 local-history blog describes today's
tree without mentioning any replacement; the register's own planted_band
(1880s) predates the 1898 date the narrative sources give. Delivered all
three facts rather than picking a winner, `age_estimate` left blank, marked
`flagged`. This is the bridge-claim trap almost in reverse: rather than
join the facts into a tidy story, the story says plainly that nobody has
reconciled them.

**2 leads, 1 blocked**, all in `data/leads/nijmegen.json`. The blocked one
(a beech on "Beukenlaan", Landgoed Brakkestein) would have been the oldest
candidate in the batch, planted_band 1700-1750, but the register's own
place name and the park's Rijksmonument description confirm it sits on a
beech-lined avenue with no individual recognition, the avenue exclusion
BRIEF_RESEARCH.md names explicitly.

`rijksmonumenten.nl` added to the fetch blocklist: hangs on individual
monument pages, both WebFetch and curl with a browser UA.

**Second pass, same session: Nijmegen 12 to 13.** Two more clusters: the
Brakkenstein manor house (extends the existing Sterrenbos cluster, ~900m
away) and Park Leeuwenstein, a west-side park on the site of a demolished
19th-century villa. The manor-house pair (a chestnut and a beech, both
1830-1840) went to leads, no second source names either individually.

**Shipped: nij_013, The Beverboom of Park Leeuwenstein** (Magnolia sp.,
exact species unconfirmed). Register-dated to the 1880s, roughly 140
years. Its neighbour, the park's giant sequoia, was caught DEAD (fell in
the storm of 18 January 2018, two independent sources) and blocked before
it could ship, exactly the vitality check the register itself cannot do.
Species stays an open question on the page: "beverboom" is old Dutch for
Magnolia, but whether this specimen is Magnolia virginiana or the
Magnolia acuminata a 2023 local survey lists for the same park was not
settled this pass.

**Third pass, same session: Nijmegen 13 to 14.** Two new stops, both
previously unrepresented: Hees (a church square about 3km west of the
centre) and Lent (Nijmegen-Noord, across the Waal, annexed by the city
in 1998).

**Shipped: nij_014, The Pastorie Chestnut of Lent** (Horse Chestnut,
Aesculus hippocastanum). A genuine tree-level match: the national heritage
register's own listing for the parish complex names "an old chestnut tree"
on the specific square the LRMB register also pins by coordinate, not an
inferential join. Not flagged.

Hees's church-square beech and plane (Schependomlaan/Korte Bredestraat)
went to leads: the square itself is confirmed by local history, but no
source names either individual tree, and monumentaltrees.com's own page
for this exact spot 403'd on every fetch attempt. Two more hangs added to
the blocklist: reliwiki.nl and Nijmegen's own municipal tree WFS endpoint.

**Photo viewing pass, same session: Nijmegen's first photograph.** Ran
`photo_hunt.py --city nijmegen` (free, API-only) to seed candidates, then a
session viewing pass judged 42 candidates across the city's 8 photo-less
trees against the Cadiz standard. 1 approved: **nij_009, the Kabouterboom**,
identity settled by hard data rather than by name (the Commons file's own
GPS sits 25m from our pin, and its caption states an 850cm girth, exactly
matching our `girth_cm`). 41 rejected, 0 held. Seven trees (nij_001,
nij_002, nij_003, nij_004, nij_008, nij_012, nij_014) are now documented
Commons dead ends: the nationally-famous names (Julianaboom, Wilhelminaboom,
Sterrenbos) kept returning other towns' same-named trees, and should not be
re-swept without a genuinely new source.

One thing worth a future verify pass rather than a photo pass: two 2020s
photographs of Hertogplein show the square rebuilt with young trees and no
crowned iron fence visible, which is the recognition feature nij_012's story
leans on. Checked it: the fence itself, "sierhek Wilhelminaboom", is its own
listed national monument (monumentenregister.cultureelerfgoed.nl/monumenten/516445),
and the crown-replacement ceremony is a standing yearly tradition on 24
July per the Wonen in Nijmegen blog, so it is not something that gets
quietly removed. Reads as the two photographs simply not framing it,
resolved, no correction made.

Released the Brisbane claim the earlier attempt left standing (558 unnamed
"significant landscape trees" candidates, no names to work from yet, not
today's priority per scout_next). Salzburg's claim belongs to a separate,
still-live night run and was left alone.

## 2026-08-22 (night run) - Submissions 11-36: Hidde's own QA of the rebuilt worthit widget, not reader input

26 new rows in `submissions`, all `kind: feedback`, all from one `user_id`
that resolves to his own account (checked via
`/auth/v1/admin/users`). The pattern makes it unambiguous: rapid vote/undo
cycles on three trees (Rome's rom_001 Ginkgo of Villa Sciarra, Amsterdam's
ams_004 Wertheimpark Wingnut, Utrecht's utr_005 Onder de Linden), several
pairs under 20ms apart, which no human thumb produces. Timestamps land the
same day the WorthIt widget was revised (worthit-js.ts's own 2026-08-21
comment), so this reads as his own click-through test of the toggle/undo/
chip behaviour right after shipping it, not field feedback.

One row (id 14) is a genuine chip click, "report: could not reach it" on
rom_001. Checked against our own data anyway: `access` already says "Free,
open access, Villa Sciarra public park", a well documented public park, so
nothing here suggests the pin or access line is actually wrong. Read together
with the rest of the sequence, this is almost certainly a test click rather
than a real "I stood at a locked gate" report. Not treated as a correction;
no page changed. If a second, distinct report on rom_001 arrives later, per
the standing rule it reopens the question rather than being waved off by this
entry.

All 26 ids appended to `data/submissions-processed.json`. `outcome: holds` was
also set on all 26 rows via the service key by a concurrent run's identical
check; no `reply_text` set on any of them (nothing to answer; the generic
thank-you, if it fires, is harmless since the address is his own).

## 2026-08-21 (session) - Bucaco: the Fundacao's nine plaques, read and merged

The files arrived within the hour: nine PDFs of the Trilho das Arvores Notaveis
plaques (2019, texts validated with the University of Aveiro) and three
photographs. The nine plaques match our nine remaining Bucaco trees exactly,
one each.

**What they gave us.** A measured girth for all nine, which is the field this
project is shortest of (13 trees carried one before today): 240 cm on
Wellington's Olive up to 865 cm on King Regnans. Heights for four. Two facts
worth a story edit later: the cork oak "appears to have never been corked", and
the plaque calls King Regnans the tallest tree in the forest at about 73 m.
Sources and verify_notes on all nine now cite the plaque by number.

**One correction avoided, and it is the lesson.** The Portuguese layer of the
PDFs mangles digits through its embedded font: the cypresses' planting year
extracts as "1_44". Read as 1844 it would have demolished a correct page,
because our story says the plaque dates the Cedro de Sao Jose to between 1628
and 1650. The ENGLISH layer of the same plaque is clean: "planted around 1644".
So the plaque confirms our page rather than contradicting it. Recorded at the
top of data/research/bucaco-plaques.md for the next run.

**One conflict recorded rather than resolved.** Plaque 07 dates the First Fall
cypress to around 1644 (about 380 years), while the state measurement from 2016
that our page cites reads about three centuries. Two official sources seventy
years apart; the published age still follows the dated state measurement and
the verify_note carries the plaque's figure. The girth settles the identity at
least: the plaque's 5.26 m against the 5.25 m already in our story.

**Three photographs are live** on Wellington's Olive, the Bunya Pine and the
Santa Teresa redwood, all three of which had none. Rotated, resized to 1600 px
and recompressed from 3 MB originals, hosted by us like the Baarn oak. Credited
to the Fundacao Mata do Bucaco, with the provenance in the photo note: they are
NOT under an open licence, they were sent to us by the body that manages the
forest. Hidde's call, 2026-08-21: "we mogen de foto's gebruiken, anders
versturen ze die niet." The written confirmation is still asked for in
drafts/reply-bucaco.md, which now also tells them what we did with the files.

## 2026-08-21 (session) - Bucaco: the Fundacao's biologist answers, and the Santo Elias redwoods come off

The Fundacao Mata do Bucaco replied to our outreach and had its own biologist
check the app. Three things came back.

**Every tree we list there is classified of public interest**, and each carries
an information plaque whose text was validated by the University of Aveiro and
the Fundacao. They sent the plaque PDFs and photographs by WeTransfer. That is
a second, authoritative source for the whole Bucaco page, better than anything
a research pass can assemble remotely, and it is the first time a forest's own
managers have handed us their field data.

**They asked for the Santo Elias redwoods to be removed** (bsc_005, "The
Redwoods of Santo Elias"): it is not possible to travel to them, which is why
the notable-trees trail does not sign them. Done the same day. Our page said
"free on foot" and marked the pin confirmed, so we were promising a walk that
cannot be made, which is the one error this site does not leave standing. The
entry moved to data/leads/bucaco.json as blocked with the reason, the old URL
redirects to the city page (REMOVED_TREE_SLUGS), and the intro and FAQ now say
nine trees rather than ten. The walk re-routes itself, since walk-routes.json
is keyed on the ordered tree ids.

**What is owed:** the plaque texts and photographs may not be published until
the Fundacao says so in writing, with a credit line they choose. Draft reply
asking exactly that is in drafts/reply-bucaco.md (mailcheck clean); it also
asks which tree on their trail visitors look for that we do not have yet.
FOR HIDDE: the WeTransfer link expires after seven days, so forward the files
or the link when you can.

## 2026-08-21 - Submission #10: "not worth it" vote on Paris par_001 (the Robinier of Square Rene-Viviani), no action

A reader used the worth-it control to mark the Robinier not worth the visit,
with no reason chip and no name/email on the row. Re-read the tree entry: it
is genuinely the oldest tree in Paris (1601), two independent sources, free
public square, `location_precision: confirmed`. The likely cause is the
physical experience rather than a factual error: the story already says
plainly that concrete props hold up its heaviest limbs, ivy hides much of
the trunk, and the on-site plaque undersells it. That is an honest account
of an underwhelming-looking tree with a genuinely remarkable history, not a
location or vitality problem, so nothing on the page needed to change.
Marked processed in `data/submissions-processed.json` (id 10). No email on
the row, so no reply owed.

## 2026-08-21 (session) - Florence's two cheapest leads (Bobolino pine, Simone Weil cypress) checked, confirmed still single-sourced

Both are held back only for want of a second source per data/leads/florence.json
(the pine stands 25m from live flo_007, the cypress 90m from the same cluster,
so either would be a genuinely zero-cost addition if a second source existed).
Fetched the comune di Firenze's own press release on its 29 monumental trees
directly (ambiente.comune.fi.it and comune.firenze.it) rather than trusting
the search summary, which initially and wrongly implied the comune page names
the pine (it does not; only "Cedro dell'incenso" appears on the Bobolino park
page itself). The press release does confirm the pine and Cedar of Lebanon at
Bobolino by name, but also states plainly that the municipal census IS the
data submitted to the Region and merged into the national MASAF Geoportale:
"la Regione Toscana ha gia completato l'inserimento dei dati sul Geoportale
ministeriale". So the comune announcement and the MASAF register are the same
designation act reported twice, one source, exactly as the leads file already
warned. intoscana.it's article repeats the same municipal announcement,
likewise not independent. No RAMI per-tree page or municipal park inventory
entry found for either tree. Left both as leads; the earlier pass's judgement
was correct. Also checked the Giardino dell'Iris strawberry tree (corbezzolo):
confirmed independently that the garden opens only 2-20 May each year, free,
which settles its access caveat if it ever ships, but found no dedicated
second source for the tree itself either. No changes made; recorded so a
future Florence pass does not re-run these same three searches.

## 2026-08-21 (session) - Munich 29 to 30, Vienna 27 to 28: one register lead each, closing the earlier "not worth a fresh pass" finding

Follows up on the same day's "Rome, Florence and Vienna's leads.py READY
counts checked, not written from" entry below, which correctly declined a
whole write pass on Vienna's remaining 8 leads but flagged one of them,
the Alser Strasse plane, as "verifies fine" on its own terms, just weaker
than the six shipped in an earlier pass. That is a legitimate single-tree
addition rather than a pass worth dispatching for its own sake, so it went
in directly: `vie_028`, London Plane, girth 315cm, Vienna's Baumkataster
gives a documented 1894 planting date (about 130 years), single register
source plus the city's own tree inventory, `curation_status: flagged`,
`location_precision: confirmed`, no photo. Took Vienna from 27 to 28
against a target of 30; the remaining leads (a Prater ginkgo with
unconfirmed courtyard access, a third Rathauspark plane, two young
Kugeltrompetenbaum specimens) stay leads for the reasons already on record.

Munich was one tree short of its target (29 of 30) with 15 READY leads,
all legally protected single trees on public land per the city's 2021
Naturdenkmalverordnung, most failing only on age (the ordinance carries no
age or girth column). Picked the Nymphenburg lime at Nordliches
Schlossrondell 8 for clustering: it sits about 0.7km from the existing
muc_007/011-014 Nymphenburg walk. Confirmed by a second source (Wochenanzeiger
Muenchen, 12 Oct 2011, naming this specific tree among eleven declared that
year), which the register-only leads file did not carry. Ships as `muc_034`,
`curation_status: flagged` (no age), `location_precision: approximate`. A
Commons photo (CC BY-SA 4.0, self-published 2020, filename matches this
tree and its Naturdenkmal designation by name) was found via the API and
set to `found_needs_check`; not viewed here, this runner's egress blocks
upload.wikimedia.org.

Both cities' route still walks clean (Munich 2.0km/24min, Vienna
2.0km/25min per `route_walks.py`). Vienna's meta_description updated from
"Twenty-seven" to "Twenty-eight". Full detail in LOG.md.

## 2026-08-21 (night run) - Milan 19 to 21, Brussels 26 to 30: leads.py READY trees, all flagged, no photos

Both were single-source-only register trees that a past pass had correctly
found and correctly left in leads.json as thin rather than blocked; per
CLAUDE.md's ruling that a judgement call about thinness never blocks
publication, both got written up. Milan: two MASAF-register London planes
(Viale Montesanto, 38m; Piazzale Libia, 35m), each single-sourced,
`curation_status: flagged`, no age (the Italian register carries no age
field). Brussels: the Parc d'Egmont pyramidal holly (140cm girth, second
largest of its cultivar in the region) plus the three trees a July 2019
survey added to that park's register entry (a pagoda tree, a weeping ash,
a thornless honey locust), the latter three sharing one approximate
coordinate since the register itself recorded a group point rather than
one per trunk. All 6 flagged, all photo-less. Both cities' count-promising
copy (intro/meta/faq/question block) updated. Full detail in LOG.md.

## 2026-08-21 (night run) - Rome, Florence and Vienna's leads.py READY counts checked, not written from

`prepare.py`'s shelf summary and `city_queue.py --next` both pointed at Rome
(4 ready), Florence (1 ready) and Vienna (10 ready, later 8 after the fix
below) as cheap write-only passes: below target, register-rich, leads.py
says READY. Read the actual lead entries behind all three before claiming
tokens for a write pass, and none were genuinely ready:

- **Rome's 4** each carry a `[SKIPPED 2026-08-14 by the write pass]` note
  explaining a real reason none matches `data/block-reasons.json`'s patterns:
  beyond the 30-minute day-trip boundary, an unresolved post-fire vitality
  check, or a planted grove with no individual specimen (not a collectible
  point). Correctly excluded before; still correctly excluded now.
- **Florence's 1** is an unverified RAMI-only list (3 species) needing its
  own second source per its own text, i.e. exactly the "not verified yet"
  case the two-source bar exists for, not a done story waiting to be typed.
- **Vienna's list** was mostly a bug: entries already noted "verified and
  delivered to data/research/vienna-verified.json as vie_026" (no literal
  "delivered AS" match) were slipping past `leads.py`'s DONE regex and
  showing as fresh candidates. Fixed in `scripts/leads.py` (widened DONE to
  catch "delivered to" as well), dropping Vienna's count from 10 to 8. The
  remaining 8 are real leads a past pass deliberately left out for legitimate,
  non-blocking reasons (a third plane in a park that already has two, access
  still unconfirmed on a Prater ginkgo, a weaker specimen off the main walk),
  none of which is a fresh six-candidate pass worth dispatching on its own.

None of this changes the shelf's headline numbers being genuinely useful for
*some* cities (see the Milan/Brussels write pass below, dispatched instead):
the lesson is that `leads.py`'s READY count is a start, not a verdict, and a
run should read the `why`/`why_not_published`/`why_not_yet` text before
claiming a city on the strength of the number alone.

## 2026-08-21 (night run) - Bari's 4th tree checked and still not found

Bari has 3 fully verified, written trees (`data/research/bari-verified.json`)
sitting one short of the 4-tree floor: an ombu and a "mangiafumo" (ponytail
palm) in Piazza Umberto I gardens, and the Pine of Carrassi. The in-city
register supply is exhausted (2026-08-20) and the two closest day-trip
candidates (La Grave carobs, Sovereto pine) were already blocked. This pass
checked the last three unchecked day-trip candidates from Puglia's regional
register, all in Molfetta (24-29km, well inside the 30-minute rail day-trip
boundary at 21-25 minutes each way): the Torre di Pettine eucalyptus, the
Navarino roverella and the Macchia Clemente carob. All three moved to
blocked in `data/leads/bari.json`: the eucalyptus sits 300m+ from any
mapped road (Overpass check), the roverella adjoins a privately walled,
ruined masseria with no source placing the tree relative to the wall, and
the carob sits in a private-house contrada with no source confirming it is
the same tree as the unrelated, definitely-public carrubo secolare in
Molfetta's Parco Lama Martina (joining those two would be the bridge-claim
error). That exhausts the regional register's day-trip supply for Bari.
Bari stays unpublished, 3 trees, until a reader submission, a from-zero
web sweep, or Hidde widening the day-trip boundary produces a 4th. Claim
released. Logged in data/agent-costs.json as a zero-yield verify pass.

## 2026-08-20 (autonomous run) - Toulouse submission: elm ID correction checked, not changed

Reader submission (3 duplicate rows, same content, a form double-submit)
questioned tls_002's species: hairless leaves, shape said to be atypical
for Wych Elm (Ulmus glabra), plus a note that two elms stand a few metres
apart at the spot and another nearby. Re-queried Toulouse's own open-data
API directly for id 15138: it still returns Ulmus glabra at essentially
our exact coordinate and remains the sole tree in the area flagged
remarquable=Ville de Toulouse. Found 14 elms within 150m, including one
Ulmus laevis (id 15143) about 15m away, unflagged. Laevis has notably
smoother leaves than glabra, so the reader most likely looked at that
neighbouring tree rather than tls_002. Left the species as the register
states it (our only source, government-trusted per the register-layer
rule), added a verify_notes entry recording the correction and the check,
and added one sentence to the story noting the cluster of elms so a
future visitor trusts the pin over the first elm they see. Stayed
`flagged` (unchanged; a second independent source still does not exist).
All 3 rows marked processed.

## 2026-08-20 (session) - Arnhem: deepened 4 to 9 from the freshly-staged Netherlands register

Bari checked first per the shelf's own writing queue: register genuinely
exhausted (only 4 designated monumental trees exist in the whole city, one
already correctly blocked on university-grounds access, one on a school
courtyard with no evidence of public access), stays at 3 verified trees
below the 4-tree floor, from-zero research off (not one of Hidde's 17 named
cities). Checked Rome/Florence/Milan/Vienna's leads.py-flagged READY trees
by hand next: all turned out stale (one was a duplicate register id for an
already-published Bari tree; Vienna's "Alser Straße" plane turned out to be
an exact-coordinate duplicate of the already-published vie_024) or carrying
real unresolved caveats their own notes already named (single MASAF-only
source with a failed second-source hunt, an unresolved size discrepancy
across three sources for a Milan plane in a piazza with several planes).
None of that shipped.

`prepare.py`'s staging shelf held a genuinely fresh one instead: Arnhem's
190 freshly-staged Dutch LRMB (Landelijk Register Monumentale Bomen)
candidates, never touched by a prior pass. A tight cluster around
Velperplein/Musispark, 0.21 to 0.32km from each other, all `visitable: ja`,
`owner_category: gemeente`. Ran every candidate's `history` text against the
register's own `dead_entries_regex` before shipping anything: caught and
excluded a copper beech in the same cluster whose own history field says it
was felled in 2000 after fungal damage. Shipped 5: a Scarlet Oak, a Weeping
Japanese Pagoda Tree (registered for rarity, not age), a second Oriental
Plane, a Black Walnut with a documented fungal decline-and-apparent-recovery
history, and a Sessile Oak, all `curation_status: flagged` (single
register source per tree) and `location_precision: confirmed`. Corroborated
the shared 1880 Leonard Springer park-design context, common to four of the
five, via nl.wikipedia and an Arnhem municipal heritage document; the
Pagoda Tree has no such context (registered for species rarity, "dendrologisch",
not the 1880 planting) and says so plainly in its own story. The build's walk
planner independently grouped 6 of Arnhem's 9 trees (5 new plus the existing
poplar) into one 0.6km, 8 minute walk, unprompted, confirming the cluster
reads as a real afternoon rather than a scattered list. Intro/meta/FAQ counts
updated 4 to 9. Preflight, superlatives and the full site build all clean;
qa.py's one flagged item is the pre-existing sitemap-lastmod warning from
this sandbox's shallow git checkout (documented in prior entries, not a
real defect). Photos: none hunted, per this runner's no-photo-judging rule;
an honest gap for all 9.

## 2026-08-20 (session, continued) - Utrecht: deepened 5 to 9 from the same fresh Netherlands register

Same shelf, next Dutch city by rank (50 vs Arnhem's 170). 316 freshly-staged
LRMB candidates, concentrated around the Zocherpark/singel ring that circles
Utrecht's historic centre. Caught two things worth recording so a later pass
does not repeat the check from scratch: a DUIC news article describes a
specific, named, 184-year-old elm in "Zocherplantsoen" now terminally
infected with Dutch elm disease and being preserved as a dead standing snag
rather than felled; two Hollandse iep (elm) register candidates sat in the
same Hieronymusplantsoen cluster this pass was drawing from, and neither
could be positively ruled out as that tree, so both were dropped rather than
risk publishing a documented terminal case as a normal collectible. Separately,
a "Hollandse linde" register point 80m from the already-published utr_005
(Onder de Linden) turned out to be the same canal-side double row that entry
already covers at approximate precision, not a new distinct tree; dropped as
a near-duplicate rather than shipped as a second entry for the same feature.

Shipped 4: a Copper Beech and a 4-tree Oriental Plane grove, both dated by
the municipality to an 1835 planting under J.D. Zocher's remaking of
Utrecht's old defensive ring into parkland (the beech's own register carries
a genuine, unresolved internal contradiction between that 1835 municipal
date and an 1880s Bomenstichting registration date; stated as a disagreement
in the story rather than resolved by picking one), a second Oriental Plane at
Janskerkhof churchyard square, and a London Plane at Lucasbolwerk, corroborated
against the independently documented 1941 construction date of the
Stadsschouwburg theatre it now fronts. All four `curation_status: flagged`
(single register source per tree beyond the general park-history
corroboration), `location_precision: confirmed`. The build's walk planner
grouped 8 of Utrecht's 9 trees (all but the outlying Uithof Linden) into one
1.6km, 21 minute walk. Intro/meta/FAQ counts updated 5 to 9; the intro
needed trimming back into Contract C's 60-100 word band after the update,
caught by `preflight.py`. Build/preflight/superlatives/qa all clean (same
pre-existing sitemap-lastmod warning as the Arnhem pass, this sandbox's
shallow checkout). Photos: none hunted, per this runner's no-photo-judging
rule.

## 2026-08-20 (session, continued) - Groningen: deepened 5 to 10 from the same fresh Netherlands register

Third Dutch city off the same shelf, next by rank after Utrecht. A central
cluster around Martinikerkhof, Akerkhof, Prinsentuin and Guyotplein, all
within 0.7km of each other. Shipped 5: an oak at Martinikerkhof (shipped with
an honest note that the municipality's own 2021 survey rates its condition
moderate to poor and declining, since a struggling tree is still a living one
and not a reason to withhold it), a horse chestnut in the walled 1626
Prinsentuin garden (free entry confirmed independently, not just from the
register), a horse chestnut at Akerkhof (corroborated against the
municipality's own account of a recent square redevelopment that explicitly
preserved this tree while removing three others, which also confirms recent
vitality), a sycamore at Guyotplein, and a Siberian Balsam Poplar (Populus x
berolinensis, a documented 1865 Berlin hybrid) at the Engelenpoortje alley,
which was itself closed to the public from 2012 to 2020 and is open again
now. All `curation_status: flagged`, `location_precision: confirmed`, all
clean against the register's `dead_entries_regex`. Build's walk planner
grouped 6 of Groningen's 10 trees into one 2.5km, 33 minute central walk.
Preflight clean on the first pass. Build/superlatives/qa all clean (same
pre-existing sitemap-lastmod warning as the other two Dutch passes today,
this sandbox's shallow checkout). Photos: none hunted, per this runner's
no-photo-judging rule.

## 2026-08-20 (session, continued) - Haarlem: deepened 4 to 9, closing a gap the city's own page already pointed at

Fourth Dutch city off the same shelf. Haarlem's existing haa_004 story
already namechecked "monumental planes, a cypress grove, oaks, a walnut and
a stand of chestnuts" as Kenaupark neighbours nobody had actually added; this
pass added three of them from the freshly-staged register: a 6-tree bald
cypress grove and a 3-tree plane grove (both within 80m of haa_004, both
historically tied to the same 1865 Zocher park design already in the city's
intro), and a common lime from the same park's later planting phase. Two
more came from a small cluster of former monastery gardens 0.5km away: a
weeping beech in Prinsenhof (monastery ground since before 1477, the city's
herb garden since 1721) and an oak in the neighbouring Wijngaardtuin
(a 16th-century monastery vineyard, redesigned late 19th century probably by
L.P. Zocher, same family). Skipped two nearby chestnut candidates with
status 5 and "onbekend" history out of caution rather than confirmed cause.
All `curation_status: flagged`, `location_precision: confirmed`, all clean
against `dead_entries_regex`. Walk planner grouped 6 of Haarlem's 9 trees
into one 1.2km, 16 minute walk. Preflight clean on the first pass.
Build/superlatives/qa all clean (same pre-existing sitemap-lastmod warning
as the other three Dutch passes today). Photos: none hunted, per this
runner's no-photo-judging rule.

## 2026-08-20 (session, continued) - Maastricht: deepened 5 to 10 from the same fresh Netherlands register

Fifth Dutch city off the same shelf. Two central lindens 85m apart at the
squares ringing the Basilica of Saint Servaas (a 1909 birth-tree for Princess
Juliana at Keizer Karelplein, whose own commemorative ironwork skips her name
entirely and repeats "no bicycles" six times instead; a second linden at
Vrijthof, the former churchyard-turned-main-square), plus three grove
entries from Monseigneur Nolenspark's 1886 westward expansion, designed by
Lievin Rosseels (son of the Leuven landscape architect who designed the
park's earlier stretch): black walnuts, weeping silver limes along the
Haet ende Nijt moat, and a pair of tulip trees. Dropped a sixth candidate, a
Nolenspark plane group, after finding it sits 240m from the already-published
maa_005 ("Tallest Plane Tree in the Netherlands", itself at approximate
precision on the same street): different register point, same species, same
street, judged too easy to confuse with the existing entry to be worth
shipping. All `curation_status: flagged`, `location_precision: confirmed`,
clean against `dead_entries_regex`. Walk planner grouped 7 of Maastricht's
10 trees into one 1.6km, 21 minute walk. Preflight clean on first pass.
Build/superlatives/qa all clean (same pre-existing sitemap-lastmod warning
as the other four Dutch passes today). Photos: none hunted, per this
runner's no-photo-judging rule.

## 2026-08-20 (session, continued) - Rotterdam: deepened 5 to 9, one bridge claim caught and dropped

Sixth Dutch city off the same shelf. Two exceptional finds: the Lijnbaan
plane, a second May-1940-bombing survivor (planted 1851 in a hospital
garden; only the tree and the hospital's entrance gate survived the
bombing; the 1960s Lijnbaan extension literally bent the street to spare
it; nominated for the 2019 national Tree of the Year), and the
Eendrachtsplein memorial yew (1947, initiated by Rotterdam Philharmonic
violinist Willem Ganter after the war). The register's own history text for
the yew claims it stands where Zadkine's famous "De Verwoeste Stad" statue
was unveiled in 1953; independent search consistently places that statue at
Plein 1940/Leuvehaven, not Eendrachtsplein, so the connection reads like the
register conflating two different memorials. Dropped the Zadkine claim
entirely and wrote the story from only what corroborates, rather than
publish an uncertain bridge claim on a page whose whole intro is about
buildings that didn't survive being confused with objects that did.
Separately dropped a "Bruine beuk Koningin Emmaplein" candidate 54m from the
already-published rot_005: same species, and the register's own text
describes a single monumental copper beech on that square, so almost
certainly the same tree rather than a second one. Also shipped a 4-tree
mixed plane group at Delftseplein station forecourt (1860, 3 London plane
plus 1 Oriental plane) and a plainer Westersingel plane. All
`curation_status: flagged`, `location_precision: confirmed`, clean against
`dead_entries_regex`. Walk planner formed two walks (6 and 3 trees). Preflight
caught a stale "plus four more" count promise in `question_meta`, fixed to
eight. Build/superlatives/qa all clean (same pre-existing sitemap-lastmod
warning as the rest of today's Dutch passes). Photos: none hunted, per this
runner's no-photo-judging rule.

## 2026-08-20 (session, continued) - Nijmegen: deepened 5 to 8, two traps caught, deliberately smaller batch

Seventh and final Dutch city off today's shelf, lower yield on purpose. A
"Julianaboom" register candidate at Julianapark turned out to be the exact
same tree as the already-published nij_004. A "Wilhelmina linde" at
Hertogplein looked like a strong companion piece (a coronation tree for
Queen Wilhelmina, 1898) until independent search
(woneninnijmegen.blog/2025/04/04/wilhelminaboom) turned up that the original
tree was replaced with another at an unrecorded date, and the register's own
planted_band (1880-1890) predates the 1898 coronation it supposedly
commemorates anyway; dropped entirely rather than publish an age or a
commemorative claim for what is very likely not the original specimen. Also
skipped a Hunnerpark elm (status 5, "onbekend" history, no positive
confirmation found anywhere) and several cemetery register entries whose
`n_trees` counts (28, 14, 12) mark them as avenue or hedge plantings rather
than single collectible points. Shipped 3: a hornbeam and a black locust
both a few metres from the already-published nij_005 giant sequoia in
Krayenhoffpark, and a sweet chestnut at the Rijksmonument-listed
Begraafplaats Daalseweg (Catholic cemetery consecrated 1885, also the burial
site of 300 victims of the February 1944 bombing of Nijmegen). All
`curation_status: flagged`, `location_precision: confirmed`, clean against
`dead_entries_regex`. Preflight clean on first pass. Build/superlatives/qa
all clean (same pre-existing sitemap-lastmod warning as the rest of today's
Dutch passes). Photos: none hunted, per this runner's no-photo-judging rule.

## 2026-08-20 (session, continued) - The Hague: deepened 16 to 21, mined the raw register by hand

Rank 24 in CITY_QUEUE.md, much higher priority than the seven cities worked
earlier today, but its own pre-staged shelf file
(data/research/the-hague-lrmb-ready.json) turned out already fully consumed:
every id in it already exists in data/cities/the-hague.json except one
correctly-held-back "potentieel" beech. So this pass mined
data/registers/netherlands-lrmb.json directly, replicating prepare.py's own
filter (visitable=ja, not particulier, not within 60m of a published tree)
by hand within 3km of the centre. Confirmed via independent search that the
Paleistuin, the garden behind the King's working palace at Noordeinde, is
genuinely free and open to the public sunrise to sunset (closed only for
occasional state visits) before shipping its bald cypress. Skipped the Lange
Voorhout linden avenue outright, 325 trees in one register entry, a mass
planting rather than a collectible point by any reading of the rule.
Shipped 5: the Paleistuin cypress, a 7-tree horse chestnut row along the
Vijverberg beside the Hofvijver (the pond beside the Binnenhof), a 2-tree
plane pair at the Grote Kerk (planted on the church's own former graveyard),
and a plane group plus a Hungarian oak group in Huijgenspark. All
`curation_status: flagged`, `location_precision: confirmed`, clean against
`dead_entries_regex`. Walk planner folded all 5 into three existing or
reshaped walks. Preflight caught a meta_description 3 characters over
Contract C's limit, fixed. Build/superlatives/qa all clean (same
pre-existing sitemap-lastmod warning as every other pass today). Photos:
none hunted, per this runner's no-photo-judging rule.

**Today's Dutch register total, all from the same national LRMB import: 8
cities, 36 trees (Arnhem 4→9, Utrecht 5→9, Groningen 5→10, Haarlem 4→9,
Maastricht 5→10, Rotterdam 5→9, Nijmegen 5→8, The Hague 16→21).**

## 2026-08-20 (session, continued) - Brussels: deepened 23 to 26, geocoded the register by hand

Rank 20, higher priority than any Dutch city worked today, 436 register
entries within reach. Brussels' own official inventory
(data/registers/brussels-arbres-remarquables.json, CC BY 4.0) carries no
address text, only coordinates and a heritage.brussels URL per tree; that
site returned only navigation menus to a curl fetch (the known
403-to-WebFetch workaround gets a 200, but the page itself is JS-rendered).
Used OpenStreetMap Nominatim reverse geocoding instead (a read-only public
API, gear for us under hard rule 5's carve-out, no product impact) to place
a dense cluster of legally-inscribed trees at the Jardin du Mont des Arts,
confirmed by web search as a genuine public garden (1910 World's Fair
origin, rebuilt 1957-58 as a suspended garden over an underground car
park). Shipped 3 (a pedunculate oak, an ailanthus, a Caucasian wingnut),
all `location_precision: approximate` since the specific garden is inferred
from geocoding rather than stated by the register, matching the existing
bru_023 single-source pattern exactly: `curation_status: flagged`, a
`notes` field spelling out both the single-source and inferred-location
caveats, age left undocumented since the register gives girth and legal
status but no planting date. Brussels 23 to 26. Preflight clean.
Build/superlatives/qa all clean (same pre-existing sitemap-lastmod warning
as every other pass today). Photos: none hunted, per this runner's
no-photo-judging rule.

## 2026-08-19 - Caserta: deepened to target (14 to 20), 6 new trees from its own leads file

Six trees written from already-verified MASAF/Campania register leads that
had only been held back by the pre-2026-08-02 count cap: Bottle Tree
(Kurrajong), Chir Pine, Turkey Oak, Southern Magnolia (free, Piazza Carlo di
Borbone), Osage Orange and Mediterranean Hackberry (all `location_precision:
approximate`, `curation_status: flagged`, matching the rest of the city).
Deliberately excluded from this pass: several other READY-labelled leads in
the same file whose own `why_not_published` notes flag real unresolved
problems (implausible measurements, a disputed species identity between two
registers, a girth field that reads "sdraiata" instead of a number) rather
than a stale count objection; those stay in data/leads/caserta.json for a
pass that can actually resolve them. City intro/meta/FAQ counts updated
(11 paid/3 free to 16 paid/4 free). Photos: 0 new candidates on the API
sweep, an honest gap.

## 2026-08-19 - Bilbao: opened, 4 trees (at the floor), all flagged, 4 photos missing, 7 leads and 3 blocked recorded

New city, from-zero web research (no usable Basque/Bizkaia register).
All 4 `location_precision: approximate` (park-level, no tree individually
pinned) and `curation_status: flagged`. Three of four carry only a vague
"over a century" age with no measurement; the Dona Casilda horse chestnut's
two sources use near-identical wording, flagged in the story as likely
sharing one original line rather than confirming independently. Not one
walkable cluster: four neighbourhoods, 1.5-3km apart, page says so. 7 leads
in data/leads/bilbao.json (ombu, ginkgo and dragon tree present in Dona
Casilda but unpinned; a second sequoia at an institutional garden with
unclear access; the Plaza Ametzola tree named by a DEIA feature but no
species/size found; the unusable Bizkaia singular-tree catalogue). 3 blocked
as confirmed dead (Arbol Gordo de Arbieto, Tilo del Arenal, El Abuelo of
Arriquibar, all per a DEIA feature). Photos: 0 of 4, API sweep queued
candidates for 2.

## 2026-08-19 - Ottawa: opened, 8 trees, all flagged (single-sourced tree-specific facts), 8 photos missing

New city, Confederation Square / Confederation Park / Major's Hill Park
cluster from the NCC's "A Living Legacy" register. All 8 `curation_status:
flagged` and `location_precision: confirmed` (tree-level register
coordinates, not grid-rounded). Caught and did not publish a bridge claim
(the National War Memorial's 1939 unveiling date almost inherited onto the
adjacent linden). Three trees share one circa-1900 age estimate from a single
document; the question page states the tie rather than picking a winner.
Photos: 0 of 8, API sweep queued candidates for 3, none judged.

## 2026-08-19 - Hawaii (the Big Island): opened, 6 trees, 0 flagged as unusable, 6 photos missing

New city, Kalopa Native Forest State Park cluster on the Hamakua coast (a
koa, a hame, two kopiko 'ula, two ohi'a lehua), all `location_precision:
approximate` (the register rounds coordinates to about 1km and all six share
one grid cell). 3 of 6 carry `curation_status: flagged` for the register's own
implausible height figures, excluded from the record rather than published;
girths are trustworthy and used instead. No tree has a documented age; the
page says so plainly and asks readers rather than guessing. One Kona
candidate (a Moreton Bay Fig gifted 1882, "Excellent" vitality in the
register) was blocked as dead, cut to a stump October 2025. Two more Kona
banyans went to leads, real candidates (one plausibly a surviving 1882 royal
banyan cutting) that need a dedicated identification pass. Photos: 0 of 6,
API sweep queued 1 candidate each for 5 of 6, none judged (this session's
egress cannot reach upload.wikimedia.org).

## 2026-08-19 - Dallas: 8 stories written (write pass)

All 8 written. The two Dealey Plaza oaks (dal_001, dal_002) carry the 22 November 1963 shooting plainly and at different lengths: dal_001 leads on the shots passing through its canopy, dal_002 leads on being the largest of the three trees the Texas Historic Tree Coalition measured and gives the disputed knoll two sentences, no more. Both ensembles say in the prose that they are groups: dal_007 names the fountain as the place to stand and separates the largest trunk (about 11 ft round) from the grove average (30 in diameter), and dal_008 leads on Moore Park's 1938 founding as one of five parks for the city's Black residents and its 1940 Juneteenth renaming, then states the age conflict as a 125 to 190 year span across three sources rather than picking one. dal_003 (county champion post oak) has no age in any source and asks the reader for one; dal_006 has no girth and asks for that. best_time set on 1 of 8 (dal_008, pecans down in October and November); the live oaks and the winter-bare bur oaks get none.

## 2026-08-19 - Los Angeles: 7 stories written (write pass)

All 7 written (lax_001 and lax_007 were pulled at the merge and are absent from the file; nothing was written for them). Five of the seven are Moreton Bay figs and each is led by a different fact rather than by the species: the Miramar's 1889 planting by Georgina Jones in a mansion garden the hotel later grew around, the church fig's status as Historic-Cultural Monument No. 19 with the church built around it in 1962, the Plaza figs as a single ensemble entry opening on the fourth tree's collapse during a lantern festival on 2 March 2019, the Beverly Hills fig opening on the Burton Green planting being local tradition with no paperwork, and the Auto Club fig on Chapman's 1894 planting outside his own house. lax_005 (oldest palm) is built on its three relocations, 1850s, 1889 and 5 September 1914. lax_006 states the fungal treatment and the request to stay out from under the branches, and says the 200-year age is the Arboretum's own estimate. No best_time on any: all seven are evergreen or aseasonal. Four trees have no published girth and three of them ask the reader for it. NOTE for the merging session: lax_005 carries "Desert Fan Palm (Washingtonia filifera)" against the live "California Fan Palm (Washingtonia filifera)" on three existing trees, which fails hard rule 9 at build; left unchanged because a write pass changes no verified field, and the story names only the Latin binomial so it reads correctly under either.

## 2026-08-19 - Seattle: 5 stories written (write pass)

All 5 written. Every pin in this city is approximate and no story implies otherwise: sea_001 says outright that no source publishes where the Big Tree stands inside the 120 acres of old growth and that finding it is part of the walk, and it also warns readers off the much younger fir the park's own printed walk starts with. sea_002 leads on the fact that the only published figures for the Volunteer Park sequoia belong to the species and not to the tree, records no age, refuses to date it from the 1904-1912 Olmsted landscaping, and asks Capitol Hill for a planting record or a tape measure. sea_003 (Kubota grand fir) states that its 200-year age rests on one document. sea_004 (bigcone Douglas fir) says the state champion title traces back to one 2003 survey through both of its sources. sea_005 uses the university tree tour's own dating of the trunk to the 1909 Alaska-Yukon-Pacific Exposition and explicitly claims no size record, since two other Seattle Lombardy poplars are claimed as record holders and sit in leads. best_time set on 1 of 5 (sea_005, yellow in late October and November); the four conifers get none.

## 2026-08-19 - Mexico City: 10 stories written (write pass)

All 10 written, no best_time on any of them: seven are ahuehuetes, one is an evergreen laurel fig and two are shamel ashes, and no source in the pass records a seasonal moment worth a badge. The page's own story is that the trees come from SEDEMA's 2025 Arboles Patrimoniales register rather than from fame, so the two famous losses appear only as context in the prose (El Sargento in mex_001, the Popotla Noche Triste tree in mex_007) and neither is presented as somewhere to walk. mex_001 carries its legendary 1521 planting as legend and its 2018 partial collapse plainly; mex_003 states both published ages (35 years and 100-115) without choosing; mex_004 opens by separating Eugenio from the felled Eugenito; mex_005 uses its documented 21 September 1921 planting. Five trees (mex_004, 006, 007, 008, 010) have no age at all and each asks the reader for one in a single sentence. mex_008 also asks readers whether the register's two trunk readings are one forked tree or two. Only mex_009 and mex_010 are written as a pair (700 m apart in Coyoacan's Barrio Santa Catarina); the rest are borough stops and no story implies otherwise.

## 2026-08-19 - Perth: 6 stories written (write pass)

All 6 written. Gija Jumulu's story states in its first line that the boab did not grow in Kings Park (dug up in the Kimberley in 2008, trucked 3,200 km, replanted 20 July 2008), so no reader can discover the relocation elsewhere and feel misled; per_005 (Old Jarrah, Armadale) carries both its honest caveats in the prose, the approximate cross-street pin and the unconfirmed fencing, so it promises a sighting and not a walk to the trunk. Two trees have no published girth (per_004 Proclamation Tree, per_005 Old Jarrah) and both ask the reader for it. best_time set on 2 of 6: the boab's leafless winter trunk (bare silhouette, Jun-Aug) and the Fraser Avenue red flowering gum's scarlet summer (Jan-Feb). The four figs and the ringbarked jarrah get none.

## 2026-08-19 - Sydney: 6 stories written (write pass)

All 6 written. Two are living replacements and say so in their opening lines rather than trading on the original's fame: syd_002 (Quad Jacaranda) opens with "about nine years old", a 2017 clone of the 1928 tree that fell in October 2016, and syd_006 (Wishing Tree) is the 1930s replacement for the c.1816 pine removed in 1945, led by its own plaque admitting it will never match its predecessor. syd_004 (Vailele fig) rests on Hunter's Hill Council's register alone and the story keeps that visible, including that the c.1900 date is one council's reading of two photographs. No girth exists for any of the 6; syd_001, syd_004 and syd_005 ask the reader for one. best_time set on 1 of 6 (jacaranda flowers, late Oct-Nov); the rest are evergreen. NOTE for the merging session: two species names collide with names already published, and hard rule 9 fails the build on this. syd_001 has "Queensland Kauri Pine (Agathis robusta)" against the live "Queensland Kauri (Agathis robusta)", and syd_002 has "Jacaranda (Jacaranda mimosifolia)" against the live "Blue Jacaranda (Jacaranda mimosifolia)". Left unchanged here because a write pass changes no verified field; the stories use plain language and read correctly under either name.

## 2026-08-19 - Frankfurt: 6 stories written (write pass)

All 6 verified Naturdenkmal trees written and ready to merge; thin spots: frk_005 (eight-stemmed linden, Grüneburgpark) has no age and no established Tilia species, both stated in the prose as open questions for readers; frk_006's "second thickest tree in Frankfurt" claim came from a search summary only and was left out of the story. best_time set on 4 of 6 (lime blossom, dawn redwood and weeping beech autumn colour, copper beech spring flush).

## 2026-08-19 - Las Vegas: 11 stories written (write pass)

All 11 written; the whole page is thin by design and says so: no age is derivable for any of the 11 (each story states it and asks the reader), every pin is approximate at building or park level, lvg_007 and lvg_008 could not be geocoded to a building at all, and the 3 Winchester Park trees share one park-level pin with no confirmation newer than 2016 plus the July 2025 valley windstorm as an open alive-now question, all three carrying that caveat in the prose. best_time set on 1 of 11 (desert willow flowers); everything else is evergreen or has no sourced timing.

## 2026-08-18 - Caserta: 10 to 14 trees, a new free second walk

Third city this session off `leads.py --ready`'s cheap-end shelf, and the only one worth doing carefully: Caserta's 32 READY-flagged leads turned out mostly NOT safe to ship on sight, unlike Krakow and Brussels. Sampled the whole list before touching anything: many carry real, unresolved problems the classifier's keyword matching cannot see (two registers disagreeing on species, coordinates 200-400m apart between MASAF and the Campania regional card, girth figures that are averages across a pair rather than measurements of either tree, trees below any reasonable size bar). None of those are the invalid "count/taste" reasons CLAUDE.md's ruling overturns; they are genuine unresolved-evidence problems, so they stay leads.

Shipped the two candidates with a clean data trail. The Third Plane of the English Garden (cas_011) was held back only for being a third plane on the page, register-clean otherwise (MASAF and Campania agree exactly on 560cm girth), so ships per the same repetition-is-not-a-reason ruling used on Krakow and Brussels. The Piazza Vanvitelli trio (cas_012-014, a monkey puzzle, a casuarina and a yew, all within 50m in Caserta's own town square) was recorded single-sourced in the leads file; found and confirmed the missing second source this pass (Campania regional register cards scheda_48/49/50, fetched directly rather than trusted from a search summary), which matched MASAF's girth figures for all three exactly. This is a genuinely valuable addition: Caserta's other 11 trees all sit inside the Reggia's paid English Garden, and these three are free, in the town centre, and form their own short walk (0.1km, all three trees essentially adjacent).

Caught a hard-rule-9 species-name collision at build time: Casuarina equisetifolia was already published in Cordoba as "Horsetail Casuarina", not "Casuarina"; fixed before the second build. Updated intro, meta_description and two FAQ answers to describe two clusters instead of one (the old copy said "all in one place, and it is not the town", now false). Build and `qa.py` green (1784 pages, 2082 checked), `superlatives.py` clean (386 claims). Ran `tree_index.py`. Claimed and released `caserta`.

## 2026-08-18 - Brussels: 20 to 23 trees, more of the READY leads shelf

Same rule 1(a) pass as Krakow above, second city. `leads.py --ready` listed 6 Brussels candidates; picked the 3 with the strongest basis and left the rest (a shrub-scale holly, a group with an unclear per-tree girth, and a maple whose register health rating flags "middling defects" needing a check first) as leads rather than force a full sweep. The second Turner's Oak of Parc d'Egmont (register 649) was held back only because "two Turner's oaks four hundred metres apart would read as one entry told twice"; the already-published bru_011 already names it directly ("A second, taller Turner's oak grows a few minutes away on the same lawns"), so this was always known-good, just unwritten. Caught Wood Wide Web's atlas page conflating this tree's measurements with bru_011's own (already flagged in bru_011's own notes); used only the register-sourced figures, not the page's mixed prose. The White Mulberries pair was held back only for duplicating bru_009's species, also an invalid reason; dropped an unverified claim from the leads file about a Belgian silk industry rather than repeat it unchecked (no independent source found this pass). The Turkish Hazel of the Grand Sablon ships single-sourced and flagged, per Step 2's explicit allowance for one source.

Recomputed the walk: the new trees fall inside the existing Egmont cluster's radius (900m), producing one 13-tree, 1.0km walk that also absorbs the Grand Sablon hazel (the two locations are about 400m apart in reality). Left it as one walk rather than forcing a split: CLAUDE.md's "four to eight trees" guidance describes typical shape, not a hard cap, and `walk_planning.py` itself clusters by distance, not tree count. Fixed two count-promise breaks preflight caught (question_meta and one FAQ answer still said "twenty" after the count moved to 23). Build and `qa.py` green (1780 pages, 2078 checked), `superlatives.py` clean. Ran `tree_index.py`. Claimed and released `brussels`.

## 2026-08-18 - Krakow: 10 to 16 trees, writing off the READY leads shelf

Followed the course's rule 1(a) (cheapest supply: write what is already verified) via `scripts/leads.py --ready`, which listed 4 Krakow leads as publishable. Checked each against current doctrine rather than trusting the old verdicts: all four had been held back in an earlier pass for reasons CLAUDE.md's 2026-08-10 ruling now forbids (cut for count, ninth-in-line, a taste judgement about an invasive species being "just a curiosity"). None of those are valid reasons to hold a tree back, so all four ship.

Also found, while reading the leads file directly: two more Krakow leads (Sikorskiego Square Oak, Tarlowska Lime) were misclassified as DONE by `leads.py`'s own resolved-marker regex, a false positive on "shipped as kra_009" / "shipped as kra_007" appearing in a *comparison* sentence about a different, already-published tree, not a self-resolution marker. Confirmed by coordinate check that neither is actually published. Not fixing the regex this pass (fails safe, only hides candidates rather than double-publishing), but noting it here since it is worth a check in `leads.py` if it recurs elsewhere: the DONE marker should not fire on "shipped as <id>" when <id> belongs to a different tree's story, not this entry's own resolution.

Verified all six new trees against a second independent source before writing: the GDOS/CRFOP national register (already licensed, same source as kra_005-010) cross-checked against Polish Wikipedia's reproduction of Krakow's own registry list, which also supplied exact street addresses (ul. Studencka 25, Plac Kossaka 4, ul. Batorego 12 and 14, Plac Sikorskiego, ul. Tarlowska, ul. Swietego Jana 30) that the leads file itself didn't carry. Ages derived by scaling girth against an already-published same-species same-register Krakow tree only where one existed (Studencka Plane against kra_005, Kossaka Ash against kra_006, Tarlowska Lime against kra_007); left empty for the standard-form oak, the ginkgo and the tree of heaven, since no safe same-cultivar/same-species growth factor was available (kra_009 is a columnar cultivar, not a valid proxy for a standard oak) and Ailanthus's growth rate is documented in `data/species/tree-of-heaven.json` as too fast and site-dependent to date off girth at all.

Shipped the Batorego oak and ginkgo (ul. Batorego 14 and 12, ~20m apart) as one entry rather than two, since only one coordinate point was available for the pair; marked `location_precision: approximate` for that reason, `confirmed` for the other five (register GPS points, same source and precision as the already-published trees on this page).

Recomputed the walk directly rather than trusting old copy: two new short walks, 7 trees/1.8km (Stare Miasto south, absorbing the Planty-ring trees plus the three new ones) and 5 trees/1.4km (Stare Miasto north), plus the existing 3-tree botanical garden cluster and the standalone Henryk Oak. Rewrote intro, meta_description and the "one walk" FAQ answer to match; oldest-tree answer (Henryk Oak) unchanged, still correct after checking every new age against it. Build and `qa.py` green (1777 pages, 2075 checked). `preflight.py` clean (133 cities). Ran `tree_index.py` (45,874 trees tracked, 1340 highlighted, up from 1334). Released the `krakow` claim.

## 2026-08-17 - Lisbon: a "worth it" vote on lis_005, no action needed

Submission #6 (Supabase `submissions`, kind `feedback`) was a reader's "worth it" vote (thumbs up, no report chip) on lis_005, the Tipu of Jardim de São Bento, Lisbon. Unlike the Helsinki and Prague feedback rows, this carries no complaint to check against sources, just a positive signal, stored per the vote design (DECISIONS.md 2026-08-14) and shown nowhere until volume makes a count honest. Nothing to verify, nothing changed in `data/cities/lisbon.json`. Marked processed in `data/submissions-processed.json`.

## 2026-08-17 - The photo hunt for the 35 photo-less cities is measured out, and the finding is that the pictures do not exist

Hidde asked for at least one photograph per city. A viewing pass worked the ranked shortlist and the result is worth recording rather than repeating: **of eight candidates judged across two sessions, two shipped.** Brisbane's Bodhi Tree and Alicante's Ficus del Passeig de Canalejas are live; one more is `held`.

**What the six rejections were, because the pattern is the point and only one of them was about picture quality.**

| city | candidate | why it failed |
|---|---|---|
| Copenhagen | the Pacifier Tree, CC0, well exposed | **the wrong tree**, in Ostre Anlaeg, three kilometres from ours in Frederiksberg Have; Denmark has several |
| Cagliari | "Albero secolare, vista frontale" | trunk not visible, and the sweep had attached the same file to two different trees |
| Catania | the botanical garden's dragon tree | the subject is the garden's entrance; the tree is a dark rim along the top |
| Perugia | "Giardini del Frontone.JPG" | statues, event chairs and a dog, trees as scenery |
| Toulouse | the Terre-Cabade hackberry | POOR on `photo_light.py`: flat, almost colourless |
| Montreal, Groningen | iNaturalist observations, right species, geotagged | **a hand holding a single leaf.** iNaturalist is an identification platform and its photographs are identification photographs |

**The conclusion, and it is a dead end worth writing down rather than re-running.** For these cities Commons and iNaturalist do not hold a photograph OF the individual tree. The filename can be made to score better and it changes nothing, because the picture a tree page needs was never taken. Poznan's "Krzysztof the Oak" matches a photograph of a politician named Krzysztof; Rotterdam's "Wilhelmina Linden" matches an archival portrait of the queen. Those are not tuning problems.

**What remains, in order of cost.** (1) `data/leads/_famous-*.json`: **929 famous trees we do not map, 926 arriving with a photograph already attached.** Adding a tree that brings its own picture is cheaper than hunting a picture for a tree nobody photographed, and it adds a tree people have heard of. Two of Denmark's sit 12 and 13 km from central Copenhagen, inside the day-trip boundary. (2) Reader submissions, which is the standing flywheel. (3) Partner and permission sources.

`scripts/photo_gaps.py` now carries every filter these rejections earned: archival dates, non-tree words, a required plant word in the TITLE rather than in the Commons categories (which include "Trees in X" almost regardless of subject), and iNaturalist demoted from a bonus to a penalty.

## 2026-08-17 - Helsinki: a "not worth it" vote on hel_006, checked and left as is

Submission #5 (Supabase `submissions`, kind `feedback`) was a reader's "not worth it" vote on hel_006, the Meilahti Ancient Pine, no free-text reason and no specific complaint (unlike Prague's earlier "wrong location" chip). Re-checked both cited sources (kirkkojakaupunki.fi, hel.fi) and both still resolve and still support the story as written: a real, ring-dated ~340-year-old pine beside a Bronze Age burial cairn. Nothing factually wrong to fix. The page's own known weaknesses (no photo, `location_precision: approximate`, `curation_status: flagged`) likely explain a "not worth the trip" reaction better than any error would, and are already tracked as an honest gap rather than something this vote newly discovered. Single low-volume signal, not narrated as a trend per the digest rule. Marked processed in `data/submissions-processed.json`, nothing changed in `data/cities/helsinki.json`.

## 2026-08-17 - Graz closes to 10: the Eggenberg lead from this morning's pass pays off

Second Graz verify pass, closing the gap from 8 to 10 using the Eggenberg Schlosspark lead the first pass had already scouted and left in `data/leads/graz.json`. Of ten designated trees at one address inside the UNESCO World Heritage palace park (5 planes, 4 Weymouth pines, 1 copper beech), only two carried individual documentation strong enough to ship: a Weymouth pine with a real 2016 field measurement (girth 370cm) and a copper beech corroborated by a GPS-tagged 2014 Commons photo matching the register point exactly. The other eight share an address and a 1979 protection date but no individuating record, correctly left as one avenue rather than eight near-identical entries, per the collectible-point rule. Both new trees are paid entry (the park charges), the first exception to Graz's otherwise free page, stated honestly in `access` and in the FAQ.

Updated intro, meta_description, question_context and all four FAQ answers for the ten-tree count and the two-cluster structure. Build clean (1704 pages), qa.py clean apart from the pre-existing sitemap warning, superlatives.py clean. Cost: 128,178 tokens verify for 2 trees. Claim released.

## 2026-08-17 - Warsaw's Sowinski's Linden retired: officially delisted as dead since 2012, published anyway on an unchecked listicle

A verify pass dispatched to close Warsaw's gap of 5 (register: Poland's national GDOS list carries almost no metadata, 3259 points near Warsaw, solved with the same Polish-Wikipedia join technique that worked for Krakow on 2026-08-16) surfaced something more important than new supply: the Wikipedia reproduction of Warsaw's own official register states, for the monument named "Lipa Sowinskiego" at Wola/ul. Wolska (the fortification embankment), that it was **blown down by wind in 1986, searched for and not found in a 2004 field survey, and formally delisted in 2012**. That location matches already-published war_003 (Sowinski's Linden, Park Sowinskiego, the Reduta Wolska embankment) closely enough to be the same monument.

**Checked directly rather than left for a later pass, per the standing rule that a tree reported dead gets verified and removed the same day.** Re-fetched both of war_003's own cited sources. warszawawpigulce.pl (a general "oldest trees of Warsaw" listicle) does describe a living ~190-year-old linden by this name, present tense, no mention of any 1986 windfall, exactly what got published. The second cited source, the Polish Wikipedia "Reduta nr 56" article, does not mention the linden at all, so the story's implicit two-source backing was really one source plus an unrelated historical-context article. Against that, the GDOS/Wikipedia register entry is a dated, specific, government record including a documented 2004 field search that failed to relocate the tree. On balance of evidence, war_003 was published from an outdated or simply wrong source, never checked against the official register.

**Retired.** Removed from `data/cities/warsaw.json` (was 5 trees, now 4 remaining plus 3 new = 7). Old URL kept resolving per hard rule 3: added to `REMOVED_TREE_SLUGS` in `site/src/lib/redirect-map.ts` (`warsaw/sowinskis-linden`), redirects to the city page. No replacement tree took its id or its story; the 3 new Warsaw trees below are independent finds, not substitutes.

**The same pass delivered 3 new trees, cleanly sourced.** The Royal Oaks of Lazienki (war_006, two pedunculate oaks in the king's Romantic Garden, register + the palace museum's own "oldest trees" page, girth 450cm each, roughly 200 years). King Jan's Linden (war_007, Wilanow palace park, register + the palace's own monument-tree inventory confirming it alive among 27 of 28 living; the Sobieski-planting legend is named but not bridged into an age for this specific tree). Niemcewicz's Walnut (war_008, Krasinski Palace on the SGGW campus, register + a dedicated Wikipedia article on the palace itself citing Warsaw city hall's register, corroborated by a 2023-dated Commons photo; grounds only reopened to the public in 2025 after nine years of campaigning). All three flagged, all `location_precision: confirmed`, ages left honestly undocumented where no source gave one.

Leads recorded for a future pass: the Szustra Oaks (5-oak cluster, access to the palace-side alley unresolved), the SGGW Oak (register-only, no second source found), the Karol Oak (too far, would start a new cluster), and a Wawer-district 5-tree micro-cluster 7-9km out. One blocked (Cis Starynkiewicza, a working water-filtration station's grounds, ticketed-tour-only access). Build clean (1702 pages, redirect stub count 285 to 286), qa.py clean apart from the pre-existing sitemap warning, superlatives.py clean (371 claims). Cost: 166,992 tokens verify for 3 trees plus the dead-tree find. Claim released.

## 2026-08-17 - Como stays at 9/10, genuinely thin, and the resurfacing bug behind it gets fixed

Como was staged (gap 1) and looked cheap (76 register candidates within 20km), but a verify pass found all 7 unmined-looking candidates near the existing walk were exact-coordinate matches to entries already blocked or held by the 2026-08-15 pass (Villa Saporiti's plane/magnolia/arbutus trio, Villa Erba's plane avenue, Istituto Ugo Foscolo's cedar), correctly not re-researched. 0 new trees; Como's remaining gap is genuinely an access question (Museo Giovio's courtyard still closed for renovation, Via Baserga still leaning private on a 2026 aerial-imagery check), not a supply shortage.

**The resurfacing itself was a real, now-fixed bug, and Como's own leads file had already logged it once before without a fix landing.** `scripts/passcheck.py`'s `mined_points()` only read `lat`/`lng` and `location.latitude/longitude`; three of Como's blocked entries used `coordinates_lat_lng` and `coordinates_lat_lng_sample` instead (one entry covering three physically distinct trees at Villa Saporiti as a list of pairs), invisible to the dedupe. A repo-wide check found 17 more entries across 6 other cities using a third shape, a flat `coordinates: [lat, lng]` pair, including this run's own freshly written Bratislava leads. Fixed (commit 2c1256e): `_extract_coords()` now reads every shape in the corpus, one point or several. A second bug surfaced fixing the first: the same-tree genus safety check took the first word of a species string, which breaks the moment a blocked entry names several species in one combined field (Villa Saporiti's "American Sycamore (Platanus occidentalis), Southern Magnolia..." extracted to genus "american", matching nothing); `_genus()` now returns every genus named in parentheses and the check is set intersection. Verified end to end: Como's brief now correctly shows the Villa Saporiti trio as BLOCKED rather than fresh.

Cost: 90,259 tokens for 0 trees, logged honestly with `brief_wrong: true` since the resurfacing was the root cause. Claim released.

## 2026-08-17 - Alicante closes to 10: a fig at the railway station forecourt, checked against an active construction zone next door

Alicante was staged with a gap of exactly 1 (9/10). Verify pass found the one candidate an earlier pass had flagged promising but unresolved: three Ficus macrophylla registered beside Alicante's main railway station facade. Shipped the largest (register_id 3096, 6.9m girth, 28m tall) as ali_010, cross-checked against three independent sources (the city's own monumental-fig information-panel programme, independent press, and a 2026 redevelopment report) confirming a public station-forecourt location. One real risk caught and resolved rather than ignored: the immediately adjacent Plaza de la Estrella is, per an April 2026 news report, a fenced construction site for the Parque Central project; the register's coordinates for this tree sit on the station forecourt itself, about 28m from that fenced lot, so it shipped with the caveat stated honestly in `access` rather than hidden. Two companion figs from the same trio (7m and 58m away) held as leads to avoid fragmenting one small grove into near-identical entries, matching the existing 300/302 Parque de Canalejas precedent.

Updated intro, meta_description (still said "Nine" after an earlier tree was added, caught and fixed), question_context and the "can I see them all" FAQ answer for the tenth tree and its position relative to the existing three clusters (city centre, Benalua, and now the station forecourt, close enough to Benalua's pair to fold into the same southern outing). Preflight caught the question_context running 20 words over Contract B's ceiling, trimmed. Build clean (1700 pages), qa.py clean apart from the pre-existing sitemap warning, superlatives.py clean. Cost: 116,808 tokens verify for 1 tree. Claim released.

## 2026-08-17 - Graz opens, the first Austrian city, and a real tooling bug fixed along the way

Staged as a new city (rank #82, gap 10, register 87 unmined candidates), but the generated brief centred on Ancona, Italy (43.70,13.90) rather than Graz, Austria (47.07,15.44). Traced the bug before dispatching anything: `scripts/passcheck.py`'s `centre_from_any_name()` did a naive folded-substring search of register place names, and "graz" is a substring of the unrelated Italian place name "Grazie" (as in Madonna delle Grazie), no word boundary. Fixed by preferring the verified `data/city-coords.json` table over the register-substring heuristic (commit 4a2d439); the register search stays as a fallback for places not yet in that table, which is the case it was built for (Melbourne's suburb-filed entries). Re-briefed, correctly centred, 90 candidates from `graz-naturdenkmale.json`.

Verify pass delivered 8 trees, cross-matched against Wikipedia's independently maintained "Liste der Naturdenkmaler in Graz" for each register entry: a maple on the Schlossberg hill, three trees (one oak, two planes) in the Volksgarten park, a field maple in the Augarten with a documented 1956 citation giving it a 70-year age floor, a plane on Schillerplatz corroborated by a dated 2014 Commons photo, and two oaks on Panoramagasse protected the same day in 1979 with real 2015 field-measured girths (2.80m and 4.90m, nearly double).

**Caught a second real error before shipping, this one in the delivered data itself: grz_005's coordinates were a copy-paste of grz_002's (1.9m apart), not the register's actual point for that entry.** Checked the raw register file directly (register_id 38: 47.062255,15.437708, about 1km from the wrong coordinate used) and independently re-fetched Wikipedia's own geocode for the same Naturdenkmal entry (47.062233,15.437672, agreeing within 5m of the TRUE register point), confirming the underlying two-source verification was sound and only the transcription was wrong. Fixed before merging. Also caught at build time: two hard-rule-9 species-name collisions (London Plane's common name against London's existing "London Plane, Baobab Group" entry, and the Latin binomial Platanus x hispanica against the site's established Platanus x acerifolia), both standardised to match.

2 candidates blocked outright (a kindergarten, a state youth-care home, both hard rule 10). 5 leads recorded, the strongest a 9-tree cluster in the Eggenberg Schlosspark (UNESCO World Heritage palace grounds, paid entry, ~3.5km from centre, independently corroborated by monumentaltrees.com) for a follow-up pass. Build clean (1698 pages), qa.py clean apart from the pre-existing shallow-clone sitemap warning, superlatives.py clean (371 claims). Cost: 188,894 tokens verify + 0 session tokens write for 8 trees. Claim released.

## 2026-08-17 - Bratislava opens, the first Slovak city, 5 trees on a 1.7km walk

Staged as a new city with 31 register candidates within 20km, 19 of them inside 1.5km of each other, from Slovakia's state register of protected trees (CC BY 4.0, licence already verified in data/registers/slovakia-chranene-stromy.json). Claimed, dispatched a verify pass. It delivered 5 verified trees, clearing the 4-tree floor: a Japanese pagoda tree on the Danube embankment (register plus an independent Slovak protected-trees resource, age derived from the register's 80-years-at-1996 figure), an ash on Rudnayovo Square in front of St. Martin's Cathedral (register plus a 2026 news roundup, no age found by either source, left honest), an Empress Tree in a volunteer-rebuilt neighbourhood park (genuine age conflict between two sources, 60 vs 150 years, both stated rather than one picked), an Adriatic oak at the edge of the Šulekova public stairway (base sits at a private-plot boundary per the register's own text, access worded honestly: view from the steps), and a small North American paper birch on an ordinary street. All five chain into a walk spanning 1.69km end to end, well within the 2km rule of thumb.

Caught along the way: one register entry (a wild service tree at Devín, S 495) is confirmed dead by a 2020 hiking.sk article the register itself has not caught up with, exactly the register-lag problem CLAUDE.md warns about; recorded blocked rather than shipped. Several more candidates sit in private gardens ("v záhrade") or a hospital's gated grounds and are held as leads with dated notes, not researched further.

Wrote all 5 stories directly in session (a 5-tree new city was not worth spinning up a separate write-stories batch) plus intro, meta description, question page and FAQ. Build caught one real error before it shipped: the Empress Tree entry was drafted as "Princess Tree (Paulownia tomentosa)", a second common name for a species Milan already publishes as "Empress Tree", tripping hard rule 9's one-canonical-name check at build time. Fixed to match Milan's existing name. Preflight, build (1688 pages), qa.py (clean apart from the pre-existing shallow-clone sitemap warning) and superlatives.py (371 claims, no collisions) all clean. Cost: 148,605 tokens verify + 0 session tokens for the write (not metered) across 5 trees. Claim released.

## 2026-08-17 - Lyon closes to 10: a rare street oak in Villeurbanne, register plus an independent 2025 corroboration

Lyon was staged for verify with a gap of exactly 1 (9/10 live) and 425 register candidates within 20km, the cheapest possible move on the queue. Claimed, dispatched a verify pass. It found lyo_011, a pedunculate oak (Quercus robur) at the corner of Rue Viret and Rue Francis de Pressense in Villeurbanne (Gratte-Ciel/Les Poulettes), 1.4km from the existing Tete d'Or cluster. Two independent sources: the Metropole de Lyon's own PLU-H remarkable-tree register (register_id 4183, calling the species genuinely rare for Villeurbanne street planting) and a 2025-08-26 Mediacites investigative piece that independently names this exact tree at this exact corner while mapping the same database, serving as the alive-now evidence 8 years after the register's 2017 survey. No age or girth documented by either source; `age_estimate` left as "not documented" rather than invented, per Step 2. Story written directly in session since it was a single tree, not worth spinning up a full write-stories batch. `location_precision: confirmed`, photo missing (no photo hunting in a verify pass).

Two leads recorded (single-source only, both close to existing trees so worth a second look if corroboration turns up): a hickory/Carya at Jardin des Chartreux (register's own species field is corrupted, "Juglans ovoida" is not a valid taxon) and a red oak at Square Gustave-Auguste Ferrie. Three Cedars of Lebanon blocked outright, all sitting in named private gardens per the register's own condition text (hard rule 10).

Fixed Lyon's FAQ ("All nine stand..." to "All ten are free to see..."), caught by `scripts/preflight.py`. Build clean (1681 pages), `qa.py` clean apart from the pre-existing shallow-clone sitemap-lastmod warning, `superlatives.py` clean (371 claims). Cost: 143,775 tokens for 1 tree, logged to `data/agent-costs.json`. Claim released.

## 2026-08-16 - Guimaraes verify pass: both flagged camellia leads still fail hard rule 10

Dispatched a verify pass (109k tokens) to close Guimaraes's gap of 4 (6 live, target 10), claimed via passcheck.py first. All 23 "unmined" ICNF register candidates within 20km matched, by coordinate, to trees already published or to the Casa da Penha arboretum already blocked by an earlier pass as a non-collectible inventory (not re-litigated, per "never re-litigate a decision"). That left the two leads an earlier pass had flagged "genuinely remarkable": the Camellias of Casa de Margaride (rare 18th/19th-century cultivars, Portuguese Tree of the Year 2024) and the Camellia of Casa da Covilha (the register's single oldest dated tree in the whole Guimaraes set, 300 years).

Both re-checked in depth and both still fail hard rule 10's first access test (can they get in without asking anyone's permission). Margaride: em.guimaraes.pt's own directory carries no access information at all, and the one open-day writeup found (maisguimaraes.pt, the A Muralha association) describes a single dated event with registration by email, not a standing offering. Covilha: still privately owned by the Tavora family, guided visits only, no standing public hours in any municipal, press or architecture-history source searched. Neither is visible from public ground either, so the Hobart view-only pattern does not apply. Both stay leads, `data/leads/guimaraes.json` updated in place with dated notes rather than shipped or blocked outright, since access could genuinely change.

Two findings worth keeping even though nothing shipped: Casa da Covilha's age is genuinely disputed (the ICNF register says 300 years at 2018, the classification decree text quoted by labpaisagem.pt says "over 100 years"), worth stating as a range if this ever ships; and passoverde.pt's page for this tree carries coordinates identical (to 5 decimal places) to this file's own Moreira de Conegos stone pine entry, 8km away, i.e. mislocated and not to be trusted as a source. Zero trees delivered this pass; `data/research/guimaraes-verified.json` is an empty array, kept as the record that the pass ran. Claim released.

## 2026-08-16 - Potsdam's two Pfaueninsel oaks retired as duplicates of Berlin's

Rung 2 (site is broken): REVIEW.md's 2026-08-16 fresh-eyes review flagged a BLOCKER, confirmed by re-checking both files directly. Potsdam's pot_005 ("The Door Oak of Pfaueninsel") and pot_006 ("The Schlosswiese Oak of Pfaueninsel") are the same two physical trees as Berlin's already-published ber_012 ("The Tuereiche (Door Oak) of Pfaueninsel") and ber_011 ("The Great Oak of Pfaueninsel"): same Berlin Naturdenkmal register ids (6-101/B and 6-102/B), coordinates 10-15 metres apart, the same underlying sources. Potsdam's own FAQ already conceded these two "stand on a separate island further out" and are "not actually in Potsdam". Berlin's entries are the fuller, earlier-sourced pair (register-confirmed 2026-08-07, richer notes) and survive; Potsdam's were retired.

Removed pot_005/pot_006 from `data/cities/potsdam.json` (now 4 trees, exactly the floor), rewrote the intro, meta description, question_context and FAQ off the six-tree count (they had said "six" and described the Pfaueninsel detour throughout), and folded both into `data/leads/potsdam.json`'s `blocked` list so a future pass does not re-research them into Potsdam. Added a cross-city redirect (`CROSS_CITY_MERGED_TREE_SLUGS` in `site/src/lib/redirect-map.ts`) so `/potsdam/door-oak-of-pfaueninsel` and `/potsdam/schlosswiese-oak-of-pfaueninsel` now resolve to the Berlin pages, per hard rule 3 (never retire a public URL outright).

Toolchain fix per the review's own suggestion: `scripts/superlatives.py` already catches two pages claiming the same crown; nothing caught two pages claiming the same trunk. Added `check_cross_city_duplicates()` to `scripts/preflight.py`, a 60-metre cross-city coordinate sweep over every published tree (same shape as the existing `check_id_prefixes()`). Ran it against the full corpus: no other collisions found, confirming the review's own global sweep. `python3 scripts/preflight.py`, `python3 scripts/qa.py` (1 unrelated pre-existing failure, sitemap lastmod, caused by this checkout's shallow git history, not this change) and `python3 scripts/superlatives.py` all pass; `npm --prefix site run build` succeeds.

## 2026-08-16 - Brisbane opens with 8 trees, all from an earlier night run's verify pass

A verify pass left `data/research/brisbane-verified.json` behind (8 trees, National Trust of Australia's Significant Tree Database plus State Library of Queensland corroboration), claimed by an earlier night run whose write claim had expired unreleased. Wrote all 8 (write pass, 88k tokens) and merged as Brisbane's opening page: 7 inside the City Botanic Gardens, planted under Walter Hill's 1855-onward curatorship, plus the Eagle Street Fig Trees a kilometre north on a CBD traffic island (planted 1889, on Queensland's state heritage register). Oldest and hero tree: the Macadamia Nut Tree, grown from 1858 trials and independently described as the first macadamia ever brought into cultivation. Walk spans 2.1km, 28 minutes per the build's own route planner.

Three of the eight (Old Government House Fig, Crows Ash, Bodhi Tree) are single-sourced to the National Trust database alone and ship flagged, said plainly in the prose. The write pass caught and corrected a factual error in one of the two independent sources: the State Library of Queensland's account of Prince Albert's Cook Pine calls him "the later King Edward VII", which is wrong (that was his elder brother); the story states his correct identity instead of repeating the source's mistake. Added Brisbane to `data/city-list.json` by hand (same as Alicante and Melbourne before it): new cities never add themselves there.

Register supply for Brisbane is far from exhausted (186 register trees per `data/city-queue.json`, target 10, 8 shipped); the remaining 2-to-target and any further deepening is ordinary future work, not recorded as leads here since nothing was individually rejected this pass.

## 2026-08-16 - Sorrento opens at the 4-tree floor, all of it a day trip to Piano di Sorrento

Register-backed (Italy's national MASAF register, pre-staged) verify+write pass, 205k tokens for 4 trees. All four stand in Piano di Sorrento, the comune next door to Sorrento proper, reached by one Circumvesuviana stop plus a 10-15 minute walk: the sanctioned day-trip pattern (same as Blarney/Fota for Cork), applied here to the whole page rather than one entry, because nothing verified inside Sorrento's own boundary this pass. Every location field, every story and the FAQ say plainly these are not in Sorrento itself. Two share Villa Fondi De Sangro (a former prince's villa, garden laid out 1875, now a free public park and archaeological museum): a holm oak and a stone pine the WWF named in 2014 among the last old pines on that stretch of coast, saving it from a hard pruning. The other two are a kilometre and a half away: a cypress that has stood since the municipal cemetery opened in 1876, and a plane tree the register itself uses as a wayfinding landmark on the road up to it.

**Held back:** four trees (plane, kauri pine, ginkgo, camphor) in the grounds of the Grand Hotel Parco dei Principi, whose own site states the garden is open to guests and restaurant patrons only, not general walk-in visitors, failing hard rule 10's first test. Left as blocked leads rather than access-unresolved, since the hotel's own words settle it. Also left as leads: two more register cypresses in the same cemetery (single-sourced only), a "homogeneous olive group" register entry that reads as an ensemble rather than a single tree, and three trees at "Antico Parco del Principe" near Colli di San Pietro whose Regione Campania card calls it "una tenuta" (an estate) next to a castle, smelling private but not confirmed closed either way.

At exactly 4 trees the page sits right at the floor CLAUDE.md sets ("four verified trees or no page"); no padding attempted, and the two Villa Fondi trees plus the two cemetery-area trees split into clusters roughly 1.6km apart, each under the site's 3-tree/900m walk-clustering minimum, so the page ships with individual tree directions but no single combined walk. Fixed a hard-rule-9 species collision the build caught (Cupressus sempervirens: "Italian Cypress" here vs "Mediterranean Cypress" already standard elsewhere).

## 2026-08-16 - Cordoba deepens by 5, and two leads turned out to already be live under different ids

Followed rule (a) of "the course after the fortnight": `leads.py --ready` showed 7 usable Cordoba leads sitting inside or near the existing 2.3km walk. Verify pass (95k tokens) brought 7 to research/cordoba-verified.json; write pass (70k tokens) delivered 5. Shipped as cdb_011/013/014/016/017: the Chinaberry of the Puerta de Almodovar, the Ginkgo of the Jardines de la Agricultura (best_time set, autumn colour), the three Casuarinas of Plaza de Jeronimo Paez (ensemble, single-sourced, said so), the River Red Gum of Parque Celia Mendez (single-sourced, 3km outside the existing walk, said so), and the Ash of Santa Marina (declining, approximate pin, age argued not documented). Cordoba is now 15 trees.

**The write pass caught a duplicate-collision the verify pass missed, same class as the 2026-08-13 Munich bug.** Two of the seven verified leads, the Himalayan Cedar of Plaza del Cardenal Toledo and the Cypress at the Alcazar Entrance, turned out to be the exact same physical trees as already-published cdb_010 and cdb_008: identical coordinates, identical catalogue measurements, same single source, just reached via an old 2026-08-03 leads file that predates the two live entries. Left unwritten and deleted from the research file rather than merged as duplicates. The Alcazar cypress's genuine open question, whether the catalogue's measured specimen is a standalone tree outside the ticket gate or one of many in the paid Paseo de los Reyes avenue, is a correction to the LIVE cdb_008 (whose story already asserts "outside the ticket gate" on one source), not a writing job on a new entry; left for a future pass rather than resolved here.

**Held back, not shipped:** the Canary Palm of the Doctor Emilio Luque Square, on an unresolved vitality question (red palm weevil, the register's own named threat to the city's Canary palms) plus a possible species mismatch (one independent description calls the square's palms Trachycarpus, the catalogue says Phoenix canariensis). Left as a lead. Also left as leads: Stone Pine of Santa Maria de Trassierra, Photinia at the Palacio de la Merced, Siberian Elm of the Alcazar, none touched this pass.

## 2026-08-16 - Prague's prg_007 flagged "wrong location": re-verified, coordinates match the source to within 5 metres

Supabase `submissions` held one new `kind: feedback` row (id 4, created 2026-08-15 19:00 UTC) reporting prg_007 (The Oak of Cisarsky ostrov, Prague) as "wrong location". Treated as a lead, not a fact, per the submission-handling rule.

Re-fetched both cited sources. Czech Wikipedia (sourced from Wikidata) gives 50°6'40.66"N 14°24'49.54"E, which converts to 50.111295, 14.413761; our stored pin is 50.1113, 14.4138, a difference of a few metres, well inside GPS precision. Nominatim reverse-geocodes our exact coordinate to a service road named "Cisarsky ostrov" in Bubeneč, Praha 7, i.e. on land, on the embankment path, not in the canal or river. Prazskestromy.cz's own register entry (#45) describes the tree as standing on the island's south bank along the road beside the navigation canal, under 200m from the bridge to Kralovska obora (Stromovka) — matching our story and address text exactly, no bridge-claim join involved. Also checked: the island is genuinely publicly reachable, three bridges plus a 2020 footbridge from Troja, contradicting no part of our `access`/`transport` fields.

No error found. Left the tree unchanged (location_precision stays `confirmed`). Likely explanation is either a stale in-session test of the report feature or a visitor who could not find the crossing rather than an actual pin error; nothing here rules that out, so a second report on the same tree should re-open this rather than being waved off. Marked id 4 processed in `data/submissions-processed.json`.

## 2026-08-15 - Five cities published: Brno, Poznan, Wroclaw, Quebec City, Potsdam

Merged in one session from verified files. All 26 trees flagged, all 26 photos missing, which is the normal state for a new register-backed city and is a photo-pass job, not a research gap.

| city | trees | flagged | photos missing | note |
|---|---:|---:|---:|---|
| Brno | 6 | 4 | 6 | girth figures disagree across measurement years on five trees; the pages print the range and say the years rather than picking one |
| Poznan | 6 | 6 | 6 | the GDOS register carries no age or girth column at all, so four of the six ship with a planting decade only, said outright on the page |
| Wroclaw | 4 | 4 | 4 | wro_003 and wro_004 have no published age in any source found; stated in the FAQ rather than smoothed over |
| Quebec City | 6 | 6 | 6 | first Canadian page; the register publishes DIAMETER, not girth, and every circumference on the page is a stated conversion |
| Potsdam | 4 | 4 | 4 | the trees stand on the Berlin bank of the Glienicke bridge; the intro, all four stories and a dedicated FAQ say so |

**Two unknowns kept open rather than closed by inference.** Quebec City: La Presse reports the park's oldest tree as a red oak of 250+ years on Rue De Laune and names no trunk, while five red oaks are registered there. The claim is attached to the largest, qbc_001, and the page says plainly that this is an inference from size and not a named match; qbc_002, fifteen metres away, ships with no age rather than borrowing the number. Poznan: the Bazar hotel on Plac Wolnosci is where Paderewski spoke on 26 December 1918, but the planting date straddles that year, so the story says nobody has recorded whether these trees were standing for it.

## 2026-08-15 - Potsdam's staged register candidates are all in Berlin, not Potsdam

`data/research/potsdam-register-candidates.json` (7 entries, stocked by `prepare.py`) all sit at Jagdschloss Glienicke, Schlossgarten Glienicke or Volkspark Klein-Glienicke, district Steglitz-Zehlendorf, postcode 141xx: administratively Berlin, not Potsdam, however close to the border (Glienicke Brucke, the actual city line, sits metres away). Not shipped anywhere this pass: attributing them to Potsdam would misstate which city a visitor is in, and Berlin (already published, 18/30 trees) is a Google-confirmed stage-2 city, so deepening it is paused while stage-1 cities like Potsdam still have real supply elsewhere. Left for whoever revisits Potsdam or Berlin next: worth checking whether `prepare.py`'s candidate-staging picks trees by raw distance to a city's centre point without checking which municipality/postcode they actually fall in, since that would explain the mismatch and might affect other border cities too.

## 2026-08-15 - Zaragoza's prison laurel: the strongest history in the register, and it is dead

Checked as a candidate to close Zaragoza's gap (a READY-flagged lead per `leads.py`, which does not read the `why` field). The Bay Laurel of the old Carcel de Torrero grew inside the prison compound, between the infirmary, a module and the north wall, visible above the walls from the street; prisoners tended it and it became, by more than one account, a symbol of the world outside for people who could not leave. It is the strongest single story the Zaragoza register holds, ahead of anything currently published.

It died. The prison was demolished afterward and the plot redeveloped; the site is now a small square the neighbourhood renamed Plaza del Laurel in the tree's memory, currently in poor repair (a 2020s rat-infestation complaint is the most recent thing written about the square). Blocked in `data/leads/zaragoza.json` per the dead-tree rule, which does not bend for a good story. Recorded here because it is worth knowing rather than re-finding: a future pass on Zaragoza should not spend time on this one again.

Also touched, not resolved: the Field Elms of Camino de Enmedio, La Cartuja, where a 2005 source flagged one of two registered elms as endangered by nearby concreting. A current hiking-trail description still lists an elm and a mulberry along that exact lane, which is real corroboration that something survives, but not which of the two register entries it is. Left as a lead rather than guessed at.

## 2026-08-14 - Two feedback submissions on Baarn's brn_005: already fixed, both look like test rows

Supabase `submissions` held two new `kind: feedback` rows (ids 2 and 3, both created 06:52-06:53 UTC today), both reporting brn_005 (The American Oak of the Pekingtuin, Baarn) as "wrong location". Row 3 is explicitly suffixed "[TEST ROW, session 2026-08-14, safe to ignore]"; row 2 is byte-identical content submitted 23 seconds earlier without the marker, almost certainly the same in-session test of the new vote/report feature (LOG.md's same-day entry: "the full interaction chain was tested live including a real Supabase insert (201, marked TEST ROW)"). Checked the live data anyway rather than assume: brn_005's location was already fixed on 2026-08-13 (see that date's entry below), pin moved to the correct oak at 52.209694,5.292861, on-site checked, story now explicitly distinguishes it from the ringed tree 60m away. Nothing to fix. Marked both ids processed in `data/submissions-processed.json` alongside the original id 1.

## 2026-08-13 - Baarn's Pekingtuin oak: the ring belongs to a different tree, and the pin was on the wrong one

Ground truth from Hidde, who walked into the Pekingtuin on 2026-08-11 and photographed what is actually there. Two true facts had been welded into one false claim, which is the error this file exists for.

- **What was right.** Dutch Wikipedia's line stands and his photograph agrees with it: an Amerikaanse eik planted around 1850, 5.52 metres round, in a free municipal park five minutes from Baarn station. The 2021 poetry ring is real, and so is the poem by Ewoud M. Rosenthal.
- **What was wrong, and it is the location.** Our story said the ring marks off THIS oak's root plate, and the pin (52.20956, 5.29203) sat at the ring. The ring stands around a smaller tree with dark purple foliage, and the oak stands about 60 metres east at 52.209694, 5.292861. No source ever connected the two; the connection was our own inference from a news article about the ring plus a Wikipedia sentence about the oak. A reader following the old pin would have arrived at a modest tree in a steel circle and concluded we had never been there.
- **How it got a confirmed pin.** `data/research/baarn-pins.json` (the pin pass) states plainly that the ring could NOT be located in aerial imagery at that resolution and left the pin approximate. A later pass upgraded it to confirmed citing PDOK aerial imagery in which "the ~6m 2021 protective ring is individually visible around the standing tree". That is a claim built on exactly the evidence a previous pass had recorded as unavailable, and it is the mechanism worth remembering: our own earlier finding was in the file and nothing made anyone read it.

Fixed: pin moved to the oak and now genuinely confirmed, story rewritten to describe the oak and to place the ring honestly on its own tree, `how_to_recognise` added because the two trees are the one pair in this park anybody could confuse, and the entry now carries the project's first owner-supplied photograph (site/public/photos/, credited to Ancient Trees rather than to a person, per PRINCIPLES #10).

## 2026-08-13 - Porto's ginkgo photo: the grant is in writing, and the OTHER post's photos are not his

Paulo Araújo answered in writing that we may use the ginkgo photograph, with one caveat that had to be checked rather than assumed: only that photo on the page is his, the other text and its photographs are not. He has written about this tree twice, so the caveat lands exactly on us.

- **Live and covered.** `photos1.blogger.com/img/291/1346/480/Ginkgo-amarela.jpg` (por_018) is the lead image of the post "Alerta amarelo", 5 December 2005, published by Paulo Araújo, and the only photo credit on that page is "Fotos: © Paulo V. Araújo". Fetched and read directly. His yes covers this photo, which is the one already on the page.
- **Never usable, do not re-hunt.** The other post about the same tree, "Golden time - Ginkgo" (December 2004), credits its photographs "Fotos: manueladlramos-0412". Those belong to a third person who has granted nothing. A future photo pass looking for a better ginkgo image will find them first, because they are the prettier set; they stay off the site regardless.

DECISIONS.md's 2026-08-11 entry stands unchanged: one photo, one permission, not a new licence category, and every other photo on the site still needs a verified open licence.

## 2026-08-13 - Munich: fixed four trees published twice under different ids

Found while looking for cheap-end write work (`scripts/leads.py --ready`): Munich's
2026-08-12 Naturdenkmal writing pass re-wrote four Schlosspark Nymphenburg register
entries (Copper Beech, Large-leaved Lime, Fern-leaved Beech, Weeping Beech) that were
already live as muc_011-014, giving each of the four physical trees a second id
(muc_015-018), a second page, thinner data (no address, no age, no best_time) and a
duplicate story. Confirmed by exact coordinate match, not guesswork. Removed the four
newer duplicates from `data/cities/munich.json`, kept the better-documented originals,
added redirect stubs (`site/src/lib/redirect-map.ts` REMOVED_TREE_SLUGS) so the four
now-gone URLs resolve to `/munich` rather than 404, and merged the photo candidates
`data/photo-queue.json` had already found for two of the duplicates onto the surviving
ids (muc_015->muc_011, muc_016->muc_012, muc_017->muc_013), since those candidates are
genuinely of the same trees.

Root cause: the four source leads in `data/leads/munich.json` were never marked
resolved after the first write, so `leads.py`'s READY count still offered them as
unwritten. Marked all four `[RESOLVED 2026-08-13, delivered as muc_0XX]`. Also found,
by the same coordinate check, four more Munich leads that duplicate already-published
trees under different names (White Ash/Maximiliansplatz -> muc_019, Beech/
Flaucheranlagen -> muc_021, two Englischer Garten limes -> muc_020/muc_022) with no
live duplicate page this time, just a dormant landmine for the next write pass; marked
those resolved too. Checked every other published city for the same coordinate-collision
pattern: none found, everything else that shares a rounded coordinate is genuinely
distinct neighbouring trees (species differ).

Munich now 22 to 18 trees. Build and `qa.py` green (1325 pages; the sitemap
`lastmod` warning is the shallow git checkout in this environment, not a content
problem). Ran `tree_index.py` (1045 highlighted, down from 1049, correctly).

## 2026-08-12 - Den Bosch: 4 to 11 trees, two new clusters, the oldest-tree answer changes

Finished the writing pass that a prior session left open (dbo_005 to dbo_011, verified facts already in data/research/den-bosch-verified.json, only stories missing). Two new clusters: Sint Janskerkhof/Casinotuin (5 trees, dbo_005-009, within 300m of the already-published Bastion Oranje maple) and Pettelaarse Schans (2 trees, dbo_010/011, a former fort mound across town, below the 3-tree walk floor so they stand as honest standalone entries rather than a chip). The write pass caught and I fixed three things before shipping: two `how_to_recognise` fields carried internal process labels ("FLAGGED FOR AMBIGUITY:") that would have rendered verbatim to visitors under "Which one is it?", two `transport` fields read as an instruction to us ("checking a local bus... may cut this shorter") rather than to a visitor, and two new trees used `Platanus x hispanica` where the site's other 79 London Planes use `Platanus x acerifolia`, which would have failed the build's hard-rule-9 one-scientific-name-per-common-name check.

The oldest-tree answer changes: dbo_005, the Plane of Sint Janskerkhof (roughly 170 years, register-only, flagged), beats the previous answer, the Bastion Oranje Norway maple (roughly 120 years) by margin even at each range's overlap. Updated intro, meta_description, question_answer/meta/context and the FAQ's first two entries to match; all three age/count fields (four trees, three verified entries, the maple as oldest) were previously baked into hand-written city-page copy exactly like the Netherlands-country-page bug REVIEW.md flagged as a BLOCKER on 2026-08-02, so this was corrected before it could repeat that class of error live.

Computed the walk directly: one cluster of 9 trees (all published trees except the two Pettelaarse Schans ones), 2.9km, 39 minutes. Ran `tree_index.py` (19,401 trees tracked). Build and `qa.py` both green (1205 pages). Released the `den-bosch` claim in data/in-flight.json.

## 2026-08-12 - Kyoto: the two HELD Gyoen trees ship, 16 to 18 trees

`data/leads/kyoto.json` held two written-and-ready stories (kyo_015 the carriage-turning cherry, kyo_017 the Shimodachiuri camphor) HELD since 2026-08-11/12 on an identical placeholder coordinate, both copied from the already-published Demizu-guchi hackberry's own point rather than surveyed. Resolved via Nominatim/OSM: Seisho-mon gate (kyo_015's actual reference point, confirmed "southwest of Seisho-mon" by an independent web source) at 35.0258332/135.7610189, Shimodachiuri-gomon (kyo_017's own story already names it directly, and OSM has the gate tagged as a building) at 35.0195774/135.7595584, 0.71km apart. Both ship `location_precision: approximate` (gate-area estimates, the same honest convention kyo_011 already uses, not a GPS fix on the trunk). Corrected kyo_017's species to the site's canonical "Camphor Tree (Cinnamomum camphora)" and shortened kyo_015's name (the "Kurumagaeshi-zakura (the carriage-turning cherry), Kyoto Gyoen" form tripped the 60-char title limit at build time).

Also fixed a real live gap found along the way: kyo_016 and kyo_018 (shipped 2026-08-11) had no `access`/`transport` fields at all, rendering as blank rows on their pages. Added both.

Recomputed the walk rather than trusting the old copy: Kyoto Gyoen now forms two walks (5 trees/1.0km, 4 trees/1.2km), 9 trees total in or beside the park, up from "five within 1.1km, one walk". Rewrote intro/meta_description/question_meta/two FAQ answers for the new 18-tree, 13-free-of-18 totals.

Deliberately left alone: kyo_017's real coordinate sits ~25m from the already-published kyo_011's own pin despite both stories placing the trees a short walk apart; kyo_011 may itself be imprecise but that's a separate live tree, not touched on today's evidence alone, recorded in leads/kyoto.json's new `shipped` section for a future pass. Build and `qa.py` green together with Den Bosch, 1420 pages. Ran `tree_index.py` (19,401 trees, 941 highlighted).

## 2026-08-12 - Rome and Bologna: a dead landmark blocked, a genuine new tree shipped

Rome's passcheck brief printed a Wikidata discovery candidate, "Quercia del Tasso" on the Janiculum, CC0 image attached, not already in our data. Checked before touching anything: it is dead, a dried husk held up by a retaining wall (struck by lightning 1843, arson-damaged 2011). Blocked in `data/leads/rome.json` so it is never re-surfaced as a live candidate. Rome's three other non-flagged MASAF register entries near the Celimontana cluster turned out to be the same three trees already correctly blocked as access-restricted (the closed San Sisto nursery). Rome's register is genuinely picked clean right now, confirmed rather than assumed.

Bologna's register held one genuine, cheap addition: a grey walnut (Juglans cinerea, "Noce Cenerino"), the only one of its species on Italy's entire national monumental-trees register, sitting about 230m from the already-published bol_007 ginkgo, both inside the university's Orto Botanico on Via Irnerio. Two independent press sources (a Bologna news site and a tourism guide, both citing the garden's own curator and a university professor running a 2025 five-year conservation project) corroborate species, height and that it is alive now, under active care for age-related decline rather than dead. Girth disagrees between sources (register 420cm, press 471cm) and both figures are recorded rather than one picked as a winner. Shipped as bol_011. This crosses the 3-tree minimum for a second Bologna walk that didn't exist before: bol_001 (Montagnola), bol_007, bol_011, 1.1km, 15 minutes. Bologna: 10 to 11 trees, one walk to two. A second register entry (Cedro dell'Atlante, Villa delle Rose, 545cm girth) was left as a lead in a new `data/leads/bologna.json`, genuine but too far from any existing cluster to join a walk. Build and `qa.py` green (1421 pages). Ran `photo_hunt.py --recheck` and `tree_index.py` on both cities.

## 2026-08-10 - Berlin's Charlottenburg/Lietzensee cluster: documented, and why it isn't a walk yet

ber_016 (Lietzensee Plane), ber_017 (Lietzensee Wingnut) and ber_018 (Karpfenteich Elm, Schlosspark Charlottenburg) were verified and merged into data/cities/berlin.json by a night run whose LOG.md entry was never finished (a permission-list bug broke builds right around then; see LOG.md 2026-08-10). Logging the gap now since the data was already live. `plan_walks()` confirms these four Charlottenburg-area trees (with the already-published ber_004 Swamp Cypress) do not form a computed walk: Lietzensee's pair sits 170m apart, the palace-park pair sits 66m apart, but the two pairs are 1.9km apart, just past the 900m walk-clustering radius, so each pair alone is one tree short of the 3-tree floor. Two register-only leads in the same palace garden (Echte Mispel and Kirschpflaume, both "Eigenart, landeskundliche Gründe" designations, no age, no second source found across three separate checks now) were judged too marginal to ship just to force a third tree into the cluster. Stays an honest gap: Berlin has two real destinations in the same corner of the city, Lietzensee and Schlosspark Charlottenburg, about a 25 minute walk apart, but no single page walk connects them yet.


## 2026-08-19 — Caserta and Naples pins (answering the 2026-08-18 WARN)

The fresh-eyes review flagged six trees published as `confirmed` without a
recorded basis. Checked all six against the MASAF register they cite:

- Naples nap_018, nap_019, nap_020 are grounded: 17m, 1m and 2m from their
  own register sheets (08, 18 and 03 of F839/NA/15), and for the cedar the
  next entry in the same garden is a different species 41m away, so the
  identification is unambiguous. The pins stand; each now carries a `notes`
  sentence saying so, which is what was actually missing.
- Caserta cas_013 (casuarina) and cas_014 (yew) were 32m and 19m from their
  cited register points, and each sat nearer the OTHER's point than its own,
  which reads as a swap rather than as imprecision. No basis for the move was
  recorded anywhere. Both are back on the coordinate their own source gives.
  The yew's address also claimed "the flower bed on the Via Alois side"; Via
  Alois runs east of the square (14.3338) and the register puts the yew on
  the west side (14.3322), so that description was dropped from the address
  and the story rather than left contradicting the pin.
  Open to correction: nobody has stood in that square for us. A reader who
  has can settle which trunk is which in one message.
- cas_012 (araucaria) sits exactly on its register point and needed nothing.

## Eindhoven, 2026-08-22

Opened from the Dutch LRMB register (Bomenstichting, attribution-only licence).
7 trees, 6 flagged, 7 photos missing.

What could not be settled:
- **Age of De Gevlekte Zuiderling.** The Wereldboom foundation says planted
  around 1760, the national register gives a band of 1820-1830. Both are on the
  page; nobody has cored it.
- **Is it still alive?** It was set on fire on 28 July 2022 and arborists put its
  survival at 30 percent, with the answer not visible until spring 2024. The
  register's 2024 edition still carries it and NOS reported thirty shoots grafted
  into a living scaffold. Published with the question asked on the page.
- **The Glorieuxpark beech.** The thickest beech in North Brabant stood in this
  park and was felled after its crown collapsed in September 2013. That was a
  green beech; ours is a copper beech and the register recorded it eleven years
  later, so they are almost certainly different trees. Stated plainly on the page
  with an invitation to correct us.
- **Photos: none.** Not hunted this pass. Wikimedia has a Groendomein Wasven
  category worth a viewing pass.

Dropped from the shortlist: the Hungarian oak by the PSV stadium (Quercus
frainetto, register nr 1697320). Real and visitable, but the register's history
for it is generic species prose copied from ecotree.green and no second source
turned up, so there was nothing to write. It stays in
data/leads/eindhoven-register.json.

## Apeldoorn and Tilburg, 2026-08-22

Both opened from the Dutch LRMB register. Apeldoorn 8 trees, Tilburg 7, all
flagged, no photos hunted.

**Tilburg: a felled tree found in the register before it shipped.** The register
carries a Dutch lime on the Heuvel with a planting band of 1600-1700. That tree
was cut down in 1994 at roughly five hundred years old, after heavy public
protest, and three descendants were planted on the rebuilt square on 26 March
2009. It is blocked in data/leads/tilburg-register.json and must never be
published. The register's own felled-entry regex could not catch it, because
that regex reads the `history` field and this entry has none.

That produced a rule, now in scripts/nl_candidates.py as `needs_alive_check()`:
a candidate 200 years or older whose register history is empty or "onbekend"
gets one web check before publishing. 58 percent of the 1,017 candidates across
the 25 cities have no history at all, but only 24 of those are 200+ years old,
so the check is affordable. `python3 scripts/nl_candidates.py <city> --risky`
lists them and the ordinary brief marks them "<< CHECK ALIVE".

Not settled:
- **Apeldoorn.** Five of the eight stand inside Paleis Het Loo, which is a paid
  site: palace and formal gardens on a museum ticket, the surrounding Paleispark
  on a two euro day ticket. Stated per tree in `access`. Four of them are on the
  alive-check list and were published on the register alone, on the reasoning
  that a palace garden is intensively managed and a loss there would be recorded;
  that reasoning is weaker than a check and is recorded here as such.
- **The Woldhuis lime, Apeldoorn.** Banded 1600-1700 with no reasoning at all,
  so it may be the oldest tree in the city or may not. The page asks readers for
  a girth measurement at 1.30 metres, which is the number that would settle it.
- **Photos: none for either city.** Not hunted this pass.

### The in-flight.json merge driver, 2026-08-22

data/in-flight.json conflicted on three separate rebases in one session, because
a session and a night run were each claiming places at the same time. That is
the normal case for a coordination file and not a disagreement, so it now has a
git merge driver (scripts/merge_inflight.py) that unions the claims instead.

One caveat worth knowing: the driver is wired in .gitattributes, which is
committed, but git requires the driver itself to be registered in local config,
which is not. On a fresh checkout run:

    git config merge.inflight.name "union the in-flight claims"
    git config merge.inflight.driver "python3 scripts/merge_inflight.py %O %A %B"

Without that, git falls back to an ordinary conflict, which is exactly the old
behaviour rather than a breakage.

## Amersfoort, Enschede and Leeuwarden, 2026-08-22

Three more from the Dutch LRMB register, 7 trees each, all flagged, no photos.

**Two trees deliberately left out, both on the school rule.** Amersfoort's plane
on the Sint Jorisschool schoolyard (Schimmelpenninckkade) and Enschede's oak at
the Kottenpark Lyceum are both real, both old and both recorded as visitable.
They stay leads, because a page telling adult strangers to walk onto school
grounds is not something this site should publish, and no source says either
site is genuinely open.

**A register history that is wrong, caught before it was copied.** The entry for
Amersfoort's copper beech at the St Franciscus Xavierius church says the church
is "also known as De Krijtberg" and "plays an important role in Utrecht". The
Krijtberg is in Amsterdam. The rest of the entry (church built 1881-83, so the
beech predates it) is consistent with the tree's own band and is what the page
uses. This is the register's fourth known error class, alongside wrong units,
corrupt fields, double-counted twins and stale felled entries: **borrowed prose
about the wrong building.**

**Leeuwarden's oldest tree is dying and the register says so.** The copper beech
at the Westerkerk had its rooting ground compacted in the 1990s, never recovered,
and the register states it will in time have to be felled. It is alive now, so it
is published, with that fact in the story and an argument for going sooner. If it
comes down, the page needs updating rather than quietly leaving it up.

Not settled:
- **Photos: none for any of the three.** Leeuwarden's Prinsentuin and Enschede's
  Ledeboerpark are both likely to have Commons coverage and are worth a sweep.
- **Enschede's Het Bouwhuis trees** have no street address in the register at all,
  only coordinates, so both pins are marked approximate.

## Dordrecht, Zwolle and Ede, 2026-08-22

Three more from the Dutch LRMB register, 7 trees each, all flagged, no photos.

**Two real measurements captured, which is rare in this register.** Zwolle's
plane on the Potgietersingel carries a measured height of 33.6 m and a girth of
719 cm, both now in the data as `height_m` and `girth_cm` so they feed the
generated thickest and tallest rankings. Dordrecht's black locust in Park
Merwestein carries something better than a band: municipal research in September
2020 dated it at 300 to 325 years, which agrees with the register's own
1700-1750 band and is the firmest age on any Dutch page here.

**Ede's oldest entry is a coppice stool, not a trunk**, and the page says so
rather than presenting the band as the age of what you see. The register's
1750-1800 describes when the stool was established; the stems standing on it are
decades old. Worth remembering the next time a very old band turns up on sandy
Veluwe ground, because coppice is the normal explanation there.

Not settled:
- **Dordrecht's Sorghvliet plane** stands on Landgoed Dordwijk, private ground
  south of the city. The register records it as visitable and the access line
  tells readers to check before setting out rather than promising them a walk in.
- **Ede's Pampel oak** is inside Nationaal Park De Hoge Veluwe, which charges
  admission. Stated in `access`.
- **Photos: none for any of the three.**

### A second gap in the felled-tree detection, 2026-08-22

Alkmaar's thickest beech, nearly seven metres round in the Alkmaarderhout and
originally three shoots planted together, was lost in the Poly storm of summer
2023; about four metres of trunk still stands. The register says so in plain
Dutch and its own regex missed it, because the word used is "gesneuveld" and the
regex only knows geveld, gekapt, gerooid, omgewaaid, omgezaagd and verwijderd.
It was caught one sentence before it would have shipped as the oldest tree in
Alkmaar.

EXTRA_FELLED in scripts/nl_candidates.py now covers gesneuveld, omgevallen and
the phrasings that describe a surviving stump ("staat de stam nog", "stamrest",
"alleen de stam"). Rescanning the whole register with it found 30 further dead
entries the original regex missed, in Utrecht, Haarlem, Hilversum, Maastricht,
Zutphen and elsewhere. None of them is on any published page: that was checked
by coordinate against every Dutch city file, not by eye.

Two dead trees found in one day, both in the top handful of candidates for their
city, is the argument for never treating this register as clean.

## Venlo, Deventer and Alkmaar, 2026-08-22

Three more from the Dutch register, 7 trees each, all flagged, no photos.

**A prefix collision caught by the build, not by me.** Venlo was generated with
the id prefix `ven_`, which belongs to Venice, and two cities sharing a prefix
overwrite each other's trees. Venlo is now `vnl_`, and `prefix()` in
scripts/nl_to_research.py reads the published cities and picks a free one
instead of taking the first three letters and hoping.

**Deventer has the best-argued age on the site.** For the poplar called De Reus
van De Worp the register dates from a photograph: a 1917 image of the Lange Laan
in the Ossenwaarde shows the tree small and distant, clearly young, which rules
out the older datings its girth would suggest. The Worpplantsoen itself is dated
to a documented 1822 replanting made after the occupying French destroyed the
old stock, with an earlier 1816 planting redone around 1820 to 1822 because
drifting ice on the IJssel damaged it.

**Alkmaar's oldest tree changed while the page was being written.** See the note
above on the Poly storm.

Not settled:
- **The Steyl sequoia cluster.** The connection this page draws between the
  missionary orders and three giant sequoias within a kilometre is inference
  from the addresses, not something the register states. Said so on the page.
- **Venlo's Vrijbroekweg chestnut** carries an age claim the register attributes
  to an unnamed elderly passer-by, including a fire in 1870. Passed on as
  hearsay rather than laundered into a fact; the page tells readers what scar to
  look for if they want to check it.
- **Photos: none for any of the three.**

## The remaining eleven, staged rather than written, 2026-08-22

Hidde: "prima zet ze maar klaar". 93 candidates are staged as READY leads and as
write-pass input, by scripts/nl_stage.py, which generates both files from one
selection so they cannot drift apart.

**Two were folded into existing cities instead of getting pages.** Voorburg is
3.6 km from The Hague's centre and Amstelveen 7.4 km from Amsterdam's, both
inside the day-trip boundary, so their trees are staged as hag_023 onward and
ams_033 onward. Each entry carries the instruction that the real place goes in
the location fields and the true travel time in transport, and that the tree is
never presented as standing in the bigger city. This avoids two thin suburban
pages and adds seventeen trees to pages that already get impressions.

**One school tree blocked automatically**, in Sittard-Geleen, using the wording
data/block-reasons.json matches. nl_stage.py does this rather than leaving it to
a writer to remember, because CLAUDE.md's school rule is about not sending adult
strangers where children are and no register field can settle it.

**A passcheck bug, found by staging Assen.** `--brief Assen` answered "ALREADY
PUBLISHED as Apeldoorn". The register fallback in centre_from_registers() used
bare substring containment, and "assen" is inside "kassen", the greenhouses of
Paleis Het Loo, so two Apeldoorn entries centred the brief 55 km from Assen. The
function's docstring already described this failure shape (graz inside Grazie)
and the containment had been left in anyway. It is now word-bounded, and all
eleven places are in data/city-coords.json so the verified table answers first.
Regression checked against Graz, Melbourne, Naples, Apeldoorn and the cities
opened today.

**Stale research files removed** for eindhoven, apeldoorn and tilburg, published
earlier the same day. `passcheck --pending` would have offered them to a write
pass as unwritten work, which is the exact failure BRIEF_WRITING.md documents.
Two pre-existing items remain and are not from this run: bari-verified.json has
3 stories written and ready to merge, and nijmegen-verified.json is stale.

## The species cards were choosing their own faces, 2026-08-23

Hidde, on the Horse Chestnut card: he would not use that photo as a thumbnail.
It was a close-up of a trunk with red survey paint ringing an old wound, which
at card size reads as crude graffiti and which fails the Cadiz standard outright
whatever it is used for: the tree is not the subject and the crown is not
readable. That photo (vie_003, the Prater Hauptallee) is now `held`.

**The cause is the second appearance of a lesson, so it is now a check.** On
2026-08-21 he said the London Plane and Ginkgo cards were showing the wrong
pictures, and `face_tree_id` was added to the species schema so a person could
pin one. It was wired into the homepage shelves BY HAND and nowhere else, so
/species went on taking the first photograph it happened to find, in whatever
order the collection returned. That is the same failure CLAUDE.md already
records for hearts and the sign-in dialog: parity wired by hand does not survive
the page count.

- `speciesFace()` in site/src/lib/images.ts is now the one helper, the missing
  twin of `cityFace()`. Pin wins, then enough pixels, then landscape, then
  widest.
- `check_species_face_is_chosen()` in scripts/qa.py is the twelfth ratchet
  check: any page drawing species cards must go through it or read
  `face_tree_id`. Verified against the pre-fix file, which it refuses.
- Horse Chestnut is pinned to hag_004, The Hague's Postzegelboom: whole tree,
  autumn colour, people for scale, centred so it survives the crop.

**How bad is the rest? Unknown, and that is the honest answer.** 79 species show
a photo and 76 of them are still guessed. Three were sampled and two failed:
this one, and European Beech, whose face is a woodland footpath with no tree in
it (edi_009, which is a fine picture for its own entry, "The Tall Trees of the
Hermitage of Braid", and useless as a species face). That distinction matters: a
photo can be right for its tree page and wrong as a card, so the fix is pinning,
not deleting.

`python3 scripts/species_faces.py` lists every face for a viewing pass, the same
shortlist pattern photo_gaps.py uses, and flags pins that do nothing. One is
dangling already: Pin Oak points at apd_008, published this morning with no
photograph.

## Our own map style, and the app parity question, 2026-08-23

Hidde asked which map Polarsteps uses and whether we can have it. They run
Mapbox, on both web (GL JS) and mobile (Maps SDK), and their CEO's stated reason
is "design control". The answer for us is that we do not need their supplier for
that: a style is a JSON file over vector tiles, MapLibre reads the same format
Mapbox GL JS does, and OpenFreeMap already serves us the tiles. Mapbox is free to
50,000 web loads and 25,000 mobile MAUs a month and then costs real money at
exactly the point where we would be succeeding, and it is a service a reader's
browser talks to, so it is a hard rule 5 decision. Not needed, not taken.

**What shipped: our own style.** scripts/build_map_style.py generates
site/public/assets/map-style.json from positron. Same tiles, glyphs, sprite and
attribution, so it is a restyle rather than a dependency. The case for it is
measurable: positron spends 20 layers on roads and 1 on parks, and side by side
at the Vondelpark it renders the park in the same grey as the buildings around
it. For a site about trees standing in parks the basemap was hiding the content.
Verified rendered at desktop and 375px before and after.

**Also closed a real gap.** Every layer asserted that a map canvas EXISTS and
none asked whether anything was painted into it, so a broken style or a dark tile
host would have shown every visitor an empty rectangle with green pins floating
on it while the whole pipeline stayed green. check_basemap() in smoke_test.py
fails on our own style being missing, unparseable, layerless, glyphless or
unattributed, and only WARNS when the tile host is down, because a check that
turns the deploy red for somebody else's outage is one people learn to ignore.

**The app cannot follow, and that is a decision he has to make.** The iOS app is
MKMapView. MapKit exposes no control over land, water, park or road colour, so
the web style cannot be ported to it. What was available was taken:
`MKStandardMapConfiguration(emphasisStyle: .muted)` desaturates roads and labels,
which is the same instruction in the only language MapKit speaks, alongside the
POI filter that was already there. Real parity means moving the app to MapLibre
Native so both surfaces render the same style file, which is a new dependency in
the product (hard rule 5, his yes) and rework of the clustering that TreeMap.swift
chose MKMapView for in the first place. Recorded here rather than decided.

### Correction: offline was NOT "essentially ready", 2026-08-23

DECISIONS.md's 2026-08-18 record of the paywall says of the four promises that
"Offline is the one that is essentially ready, because the feeds carry
everything but the pictures". That is true of the DATA and false of the MAP, and
the promise sold is "Download interactive maps and routes to explore with
confidence, even deep in the woods or abroad."

Checked today: there are zero lines of tile-caching code in the app, no
MKTileOverlay and no offline packs, and MapKit offers no API for any of it.
Apple's tiles cannot be pre-downloaded and their terms do not permit caching
them. Meanwhile `Feature.offlineDownload` already exists in Entitlement.swift
with the ask "Keep this city in your pocket", and Profile.swift already sells
"the whole map offline".

So offline maps are not a MapKit feature we have not got round to. They are the
one promise that the current renderer makes impossible, which turns MapLibre
Native from a styling preference into the only route to a feature already
written into the paywall copy and already surfaced in the app's own UI.

Checked at the same time, because it would have been the blocker: OpenFreeMap
place no limit on requests, allow commercial use, ask only for attribution, and
publish weekly planet extracts in MBTiles. Nothing in the way.

## The app's map on MapLibre: what works, and the one thing that does not, 2026-08-23

The port is on the branch `maplibre-map-wip`, not on main, and this is the
record so the next attempt starts from what was learned rather than repeating
it.

**Working, verified on the simulator and photographed:** the app renders the
website's own `map-style.json`, so both surfaces finally look like one product.
All 1,406 trees draw with their own species silhouettes in our palette. Camera,
route line, recentre control and tap-to-select behave.

**Not working: clustering.** With `MLNShapeSourceOptionClustered` set, the source
yields exactly ONE feature whatever is done to it, so a city shows a single pin.
Turn clustering off and every pin appears, which is how it was isolated. Four
hypotheses were tested and all four were wrong:

| tried | result |
|---|---|
| a UIColor in feature attributes (invalid GeoJSON) | fixed anyway, no change |
| `style.image(forName:)` as an existence check | fixed anyway, no change |
| handing the source `MLNShapeCollectionFeature` rather than real GeoJSON | rewritten, no change |
| clustering options as Swift Int/Bool rather than NSNumber | no change |

Predicates were tried both ways, `cluster == YES` and `point_count > 0`, and
neither matches, which fits a source that never produces cluster features at all.

**One real fix worth keeping regardless:** MapLibre's zoom is defined against
512-point tiles and the first version used the 256 figure from the web slippy
convention, so every camera opened one level too close and a four kilometre view
showed two. That looked exactly like broken clustering for an hour and was
arithmetic.

Clustering is why MKMapView was chosen in the first place, so main stays on
MapKit rather than shipping a map that hides trees.

**And a hazard that cost real time:** two sessions were editing this one checkout
at once. Halfway through, `SpotSheet.swift` was staged as deleted and
`SpotIntro.swift` removed from the working tree by the other session, which broke
every build here until the work moved into a `git worktree` at HEAD. That is the
fix for next time: build app changes in a worktree, not in the shared checkout.
