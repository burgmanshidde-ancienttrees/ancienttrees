# Naples deepening pass, 2026-08-05: the Orto Botanico second walk

Naples publishes 12 trees (data/cities/naples.json, nap_001..nap_012), 8 of them at Capodimonte. This pass adds a SECOND WALK: the Real Orto Botanico di Napoli, Via Foria 223.

## The access question, and why it is now a yes

An earlier pass parked the Orto Botanico because it believed entry was "free but by booking during
limited weekday hours", and judged that a booking-only garden breaks a walk. **That belief is
wrong as of 2026-08-05.** The garden's own visiting page states:

- "Lunedì, mercoledì e venerdì dalle ore 9:00 alle ore 14:00, martedì e giovedì dalle ore 9:00
  alle ore 16:00"
- "Ingresso gratuito"
- No reservation is required for ordinary individual visits. Booking applies only to guided tours
  (visite guidate). Last entry 30 minutes before closing.

So: free, walk-in, weekdays only, closed Saturday and Sunday. That is a real restriction and every
entry states it plainly in `access`. It is not a barrier that breaks the walk; it is an opening-hours
fact of the same kind as the State Archive cloister already on this page (nap_007).

Source: https://www.ortobotaniconapoli.it/it/visitare/giorni-e-orari-di-apertura.html

## The cluster

Nine trees are separately entered in the registers inside about 150 metres. Seven are individual
specimens; two are "insieme omogeneo" group entries (a Phoenix canariensis avenue, a Platanus
orientalis row) which fail the collectible-point test and go to leads/blocked.

Source pair for every one of them, per the project's register rule:
- MASAF national register (data/registers/italy-masaf.json, comune Napoli, sheets NN/F839/NA/15)
- Campania regional register cards, agricoltura.regione.campania.it/foreste/monum/scheda_NNN.html
  (schede 160-168), last updated 27 December 2019.

Both registers were scraped independently this pass. Coordinates agree to within a few metres on
every specimen, which is unusual for this region and worth noting: elsewhere in Campania the two
registers disagree by up to 400 m. Girths agree exactly on six of seven.

| MASAF | Scheda | Species | Girth MASAF / Campania | Height | Coord agreement |
|---|---|---|---|---|---|
| 34 | 165 | Ceiba speciosa / Chorisia insignis | 880 / 800 cm | 25 m | exact |
| 32 | 163 | Nolina longifolia / Nolina recurvata | 560 / 560 cm | 4 m | 1 m |
| 35 | 166 | Quercus crenata / Quercus hispanica | 440 / 440 cm | 18 m | exact |
| 37 | 168 | Eucalyptus globulus | 440 / 440 cm | 30 m | 1 m |
| 36 | 167 | Ginkgo biloba | 300 / 300 cm | 16 m | exact |
| 31 | 162 | Jubaea chilensis | 250 / 250 cm | 4 m | 1 m |
| 33 | 164 | Brahea roezlii | 190 / 190 cm | 4 m | 1 m |

Age: Campania gives ">100 anni" for all nine and MASAF gives no age field at all (it has none for
any tree in Italy). So every age here is published as "more than 100 years, undated precisely",
which is exactly what the evidence supports and nothing more. The garden was founded in 1807 and
planted from 1809, which caps the plausible age at about 215 years; that ceiling is stated, not
used as a date.

## Two register conflicts, handled rather than hidden

1. **The Ceiba's girth.** MASAF 880 cm, Campania 800 cm. Both are plausible readings of the same
   fused multi-stem base at slightly different heights, which the approved photograph shows clearly.
   Published with both figures named. It is the largest registered tree in Naples on either number.
2. **The Nolina's species.** MASAF says *Nolina longifolia*, Campania says *Nolina recurvata*
   (the plant now usually placed in *Beaucarnea*). These are genuinely different plants and the
   registers cannot both be right. Genus-only publication was drafted and then rejected, since no
   entry in the corpus names a species at genus level and hard rule 9 keys the species pages on the
   binomial. The tree is held as a lead instead. See the Outcome section below.

## What was left out of the walk, and why

- **Brahea roezlii (MASAF 33, scheda 164)**, 190 cm and 4 m. Real and registered, but it is the
  smallest of the seven, it is a third palm in a walk that already has two, and it adds nothing the
  Jubaea does not already say better. Lead, not blocked.
- **The Phoenix canariensis avenue (MASAF 29, scheda 160)** and **the Platanus orientalis row
  (MASAF 30, scheda 161)**. Group entries, no single trunk to stand at. Blocked as
  non-collectible points, the La Rambla precedent.

## Photo position

Handled by a separate hunt writing to data/research/naples-photos.json. Commons was already
documented as a dead end for Capodimonte; the Orto Botanico is a different site and was never
searched before this pass.

## Outcome, 2026-08-05

**Five trees ship** (data/research/naples-extra.json), ids nap_013 to nap_017, all in the Real Orto
Botanico, all inside about 150 metres, all doubly sourced by MASAF plus the matching Campania scheda:

| id | Tree | Girth | best_time |
|---|---|---|---|
| nap_013 | Silk Floss Tree (Ceiba speciosa) | 880 / 800 cm | flowers, Oct-Nov |
| nap_014 | Ginkgo (Ginkgo biloba) | 300 cm | autumn colour, Nov |
| nap_015 | Crenate Oak (Quercus crenata) | 440 cm | none |
| nap_016 | Tasmanian Blue Gum (Eucalyptus globulus) | 440 cm | none |
| nap_017 | Chilean Wine Palm (Jubaea chilensis) | 250 cm | none |

Five rather than six or seven, deliberately. The Nolina (560 cm, the second widest trunk in the
garden) was written and then pulled, because the two registers name it as two different species and
nothing else online breaks the tie. Existence, size and position all verify; the binomial does not,
and hard rule 9 keys the species pages on the binomial. It sits in data/leads/napoli.json with the
exact question a future pass needs to answer: read the label on site.

**Naples's first two seasonal peaks.** All twelve published Naples trees are evergreen and carry no
best_time at all, so the "at its best right now" chip has never once lit up for this city. The Ceiba
in October and November and the Ginkgo in late November are the first, and both are sourced rather
than assumed: the Ceiba's Mediterranean flowering window is documented for the species and the fallen
pink petals are visible in the approved photograph, and the garden's own visiting page names "the
golden leaves of the Ginkgo biloba" as its reason to come in winter.

**Photo: one approved, for nap_013.** iNaturalist observation 320623421, CC BY 4.0, Mary Lata, GPS
7 metres from the register point with 6 m stated accuracy. Viewed at full size before approving.
A licence subtlety worth reusing: the observation record is CC BY-NC while the individual photo is
CC BY, and the photo licence is the one that governs. The photo also corrected the story, which had
described the textbook spined bottle trunk rather than this specimen's fused multi-stem base.

Dead ends now documented in data/research/naples-photos.json, so nobody repeats them: the Capodimonte
camphor and Montezuma cypress have no open-licence photograph in any searchable pool (iNaturalist's
only Capodimonte camphor is CC BY-NC and there is no Taxodium there at all), and Wikimedia Commons'
Orto Botanico geosearch is 123 files that all share the entrance coordinate and show labels, lawns
and greenhouse benches rather than trees.

**Live copy must change when these merge.** scripts/build_site.py check_count_promises FAILS the
build at 17 trees on three sentences in data/cities/naples.json. Tested replacements that bring it
back to zero errors are in data/research/naples-extra-copy.json: intro, meta_description,
question_meta and FAQ answers 1 and 3. FAQ 3 is not just a number fix, it now states the botanical
garden's weekday-only hours, which a reader planning a Saturday needs.
