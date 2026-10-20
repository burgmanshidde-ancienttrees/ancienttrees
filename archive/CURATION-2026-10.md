# CURATION archive, 2026-10

Entries moved out of CURATION.md by scripts/archive_logs.py to keep the living
file small enough to read cheaply. Nothing here is edited or summarised: it is
the original text, newest first. CURATION.md links back to this file.

## 2026-10-16 Berlin ber_062 (the Beech south of the Kleiner Stern) may be FELLED: check today (rung 3)

The 2026-10-16 photo viewing pass found Commons photographs of the same Naturdenkmal dated 2025-02-14 and 2025-12-09 that show logs and a topped stump where the beech stood. Not retired on a photograph alone: confirm against the Berlin Naturdenkmal register (data/registers/) or a Bezirksamt notice, then `python3 scripts/retire.py berlin ber_062 --reason "..."` if it is gone. Every candidate photo for it was rejected; the full verdicts are in out/tmp/photo-verdicts-2026-10-16.json (not committed).

Also from that pass, held rather than approved: vie_037 (the Commons file for Naturdenkmal 842 shows a purple copper beech while our record says European Beech; either the species line is wrong or the photo is a neighbour), ber_059 (crops show palmate leaves, not clearly the oak), pal_012 (one of several silk floss trees on the avenue), vie_041 (plane not confirmable at that resolution).

## 2026-10-14 Rambynas rmb_001 (Witch's Spruce) is reported DEAD: RETIRED later the same window (place removed on the Oss pattern, /rambynas redirects to Silale; see LOG). The paragraph below is the state before that.

15min.lt (mid-2026) and Diena ("Raganu egle mire?") report that the spruce was killed by bark beetle in 2024, specialists found it completely dried out, the crown was cut back and it stays as a standing dead tree. Rambynas has no other tree, so `retire.py rambynas rmb_001` leaves a zero-tree city page with copy about the spruce, and there is no precedent or tooling for retiring a whole place (redirect to the Lithuania page, rewrite or remove the city file). I reverted the retirement rather than risk a red build I cannot run here. A session should retire the tree and the place together. stvk.lt id S0310505040003.

**Older entries live in the archive**, moved by `scripts/archive_logs.py`, nothing deleted:

- [2026-10](archive/CURATION-2026-10.md)
- [2026-09](archive/CURATION-2026-09.md)
- [2026-08](archive/CURATION-2026-08.md)
- [2026-07](archive/CURATION-2026-07.md)

So absence from this file is not evidence something was never tried: `grep -ri "<place>" archive/` before concluding a hunt is new. Re-running an exhausted hunt is this project's most repeated waste.

## 2026-10-09 Berlin ber_031: possibly felled

The Swiss Stone Pine of the TU Schaugärten (register 6-77/B-3): de.wikipedia's Naturdenkmal list for Steglitz-Zehlendorf says "Stand November 2024 gefällt". One source only, a search found no second; check the Berlin Senate register or TU Berlin before retiring the entry (rung 3).

## 2026-10-09 Seville: a reader's pin correction on sev_018, held as a question

A new account (10-08) moved the pin of The Judas Tree of the Real Alcázar 643 m, from inside the Alcázar (Jardín Inglés, our pin approximate) to Calle Gandesa in San Bartolomé, outside the walls. No photograph, no GPS fix, and the point contradicts the tree's own name and address, so the pin is untouched. Submission 375: outcome open_question, reply sent asking whether he is sure and which tree he saw; the Seville ambassador seat was offered in the same mail (Hidde). If he answers with a location inside the gardens or a photograph, the 2026-09-08 rule applies: a reader's fix beats our approximate pin.

