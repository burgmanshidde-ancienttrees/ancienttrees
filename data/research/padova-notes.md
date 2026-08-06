# Padova — salvaged notes from the interrupted verification pass

Recovered 2026-08-06 from the transcript of a `verify` pass that was cut off
mid-run when its session was archived. The pass had made 25 fetches and written
nothing to disk, so none of this was in the repository. Treat everything below
as raw material for a verification pass, not as verified: each claim still needs
its second source and a check that the tree is alive.

## The finding that outlives Padova: RAMI carries ages, MASAF does not

`ilregistrodeglialberi.it` (RAMI, the volunteer Registro degli Alberi
Monumentali Italiani) publishes a per-comune index and a per-tree page. The
per-tree pages carry what the national MASAF file structurally lacks:

- an **age** (calculated from a recorded birth year)
- **health status** (Buono / Sufficiente)
- **accessibility** ("accessible" / "not accessible to the public")
- its own **coordinates**, and field notes explaining why the tree was designated

Index URL pattern: `ilregistrodeglialberi.it/italia/<region>/<province>/<comune>`
Tree URL pattern: `ilregistrodeglialberi.it/<id>-<slug>-<comune>-<prov>-<region>`

This extends the recorded rule "the regional register before the national one".
For Italy there is now a third layer worth trying first: MASAF is the index,
the region fills age and vitality where it publishes at all, and RAMI fills both
for comuni the volunteers have covered. It answered the accessibility question
outright on two Padova trees, which is a hard-rule-10 question.

Caveat before this becomes doctrine: RAMI is volunteer-compiled, so it is one
source and not an official register. It does not satisfy the two-source bar on
its own the way a government register does.

## Padova per RAMI: 32 trees listed, ages where MASAF has none

| Tree | Species | Age per RAMI | Level |
|---|---|---|---|
| Palma di Goethe | Chamaerops humilis | 441 years | National |
| Platano orientale dell'Orto Botanico | Platanus orientalis | 346 years | National |
| Ginkgo dell'Orto botanico n. 1 | Ginkgo biloba | 276 years | Regional |
| Magnolia dell'Orto Botanico | Magnolia grandiflora | 240 years | National |
| Magnolia del Santo | Magnolia grandiflora | 216 years | National |
| Cedro dell'Himalaya | Cedrus deodara | 198 years | Regional |
| Criptomeria dell'Orto Botanico | Cryptomeria japonica | 176 years | Regional |
| Sofora del Giappone (Corte Capitaniato) | Styphnolobium japonicum | 165 years | National |
| Platano del Parco Treves n. 1 | Platanus hispanica | 156 years | Regional |
| Cedro di via Michelangelo | Cedrus sp. | ~105 years | Local |

Also listed without an age: Faggio a foglia di felce, Acero americano, Platano
di Palazzo Papafava, Platano di piazzetta Nievo, Tasso di Prato della Valle,
Platano di Prato della Valle, Corniolo, Ginko di Prato della Valle, Pioppo
bianco, Platano del Parco Treves n. 2, Bagolaro sdraiato del Parco Treves.

## The two clusters

**Orto Botanico, UNESCO since 1997, founded 1545.** The world's oldest academic
botanical garden still on its original site, and five of the registered trees
stand inside it. Paid entry, which is honest to state rather than a
disqualification. Address Via Orto Botanico 15, between Prato della Valle and
the Basilica. Specimens: Goethe's palm (planted 1585, in the Ortus Sphearicus
greenhouse, genome sequenced by Unipd in 2025), the magnolia of 1786 probably
the first Magnolia grandiflora brought to Italy, the ginkgo of 1750 (male, with
a female branch grafted on in the mid-19th century so it fruits, which is a
genuinely good story), a Platanus orientalis of ~346 years, a cryptomeria and a
Himalayan cedar.

**Parco Treves de' Bonfili.** Designed by Giuseppe Jappelli 1829-35, the first
designed park in Padova, on the sixteenth-century Venetian walls near the
Basilica. Four registered trees within about 60 metres of each other: two
London planes (the larger 6.37 m girth, 48 m tall, ~156 years, health
"sufficiente"), a yew near the old Via Gallucci entrance, and the "bagolaro
sdraiato" (Celtis occidentalis, brought down by a storm in the 1950s and still
growing horizontally, which is a collectible point if it is genuinely alive).

The two clusters plus the Magnolia del Santo at the Basilica sit within roughly
900 metres of each other. This is a real walk, not a list.

## Cautions the pass surfaced

- **Prato della Valle's planes are dead.** A Padova news report is headlined
  that the last plane tree of Prato della Valle has died; the square's hundred
  planes were removed between the 1980s and now. MASAF still lists "Platano di
  Prato della Valle". Any plane at that address is a dead-tree suspect and
  needs a dated check before it goes anywhere near a page.
- **The Sofora del Giappone at Ponte di Brenta is marked "not accessible to the
  public" by RAMI.** Hard rule 10: leave it out. It is not the same tree as the
  Sofora at Corte Capitaniato / Via Galileo Galilei, which is the one in the
  brief's candidate list.
- **The Magnolia del Santo is in a cloister of the Basilica** (Chiostro della
  Magnolia), planted 1810 per one source. Access needs checking: the museum
  complex changed its visiting arrangements and now sells a combined ticket.
- **Two magnolias, three sources, three dates.** 1786 (Orto Botanico, "first in
  Italy"), 1810 and "216 years" (the Santo). Do not let them merge into one
  tree.
- **The Cipresso del Canova at the Chiesa degli Eremitani** has a book written
  about it and no clear public access statement. Worth one check, no more.
- `www.comune.padova.it` returned an empty body to WebFetch on the
  `/luogo/giardino-del-ginkgo` page. Not a hang, so not blocklist material, but
  do not spend a second attempt on it.
