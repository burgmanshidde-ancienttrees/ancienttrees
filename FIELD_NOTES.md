# What Hidde found on his own telephone

The first TestFlight build, 28 August 2026. Written as he reports them, in his
words, so nothing is lost while he keeps walking through the app. Triage and
findings go underneath each one; a line moves to LOG.md when it is fixed.

## 1. My trees does not centre on the trees

"als je op mytrees pagina komt dan is de map en de boom niet in het midden
uitgelijnt"

Reproduced in the simulator: with two collected trees the pins sit high in the
uncovered strip of map, with an empty band beneath them before the sheet.
TreeMap sets a bottom content inset from the sheet's height and clamps it at 55
percent of the map view, so at My trees' resting height the camera is aiming
into a viewport that is not the one being looked at. OPEN.

## 2. His own tree's pin is bigger than every other pin

"het icoon van mijn boom met de foto is groter dan de rest"

A sighting's pin carries the photograph and draws larger than the species pins
and the cluster bubbles beside it. OPEN.

## 3. The map shows a fraction of the trees it says it has

"hij lijkt niet goed alle bomen te laden waarom tootn die zo weining"

The worst of the three. At a Europe-wide zoom his screenshot shows clusters of
11, 5 and 12 with nothing at all over London, Paris, Berlin or Munich, while
the sheet above them reads "1.356 trees you can see". The count and the map
disagree by two orders of magnitude. OPEN.

## 4. The country thumbnails are poor

"ik vind de thumnbnail foto van italie nederland portugal neit mooi"

Which photograph fronts a country is decided by the website and travels in the
feed, so this is a data question rather than an app one. OPEN.
