# What Hidde found on his own telephone

The first TestFlight build, 28 August 2026. Written as he reports them, in his
words, so nothing is lost while he keeps walking through the app. Triage and
findings go underneath each one; a line moves to LOG.md when it is fixed.

## 1. My trees does not centre on the trees

"als je op mytrees pagina komt dan is de map en de boom niet in het midden
uitgelijnt"

Reproduced in the simulator: with two collected trees the pins sit high in the
uncovered strip of map, with an empty band beneath them before the sheet.
makeUIView aimed the camera while the view still had no height and therefore no
content inset, so the opening shot centred the collection in the whole map
rather than in the strip somebody can see. Fixed by aiming once more the moment
the inset is real. HONEST CAVEAT: the simulator looked identical before and
after, so the ordering bug was real and whether it is HIS bug is for him to say
on the next build.

## 2. His own tree's pin is bigger than every other pin

"het icoon van mijn boom met de foto is groter dan de rest"

FIXED. It was 44 points against 38 for every other pin, with a ring outside its
hole and a shadow under it. Now 38, like the rest.

## 3. The map shows a fraction of the trees it says it has

"hij lijkt niet goed alle bomen te laden waarom tootn die zo weining"

The worst of the three. At a Europe-wide zoom his screenshot shows clusters of
11, 5 and 12 with nothing at all over London, Paris, Berlin or Munich, while
the sheet above them reads "1.356 trees you can see". The count and the map
disagreed by two orders of magnitude.

FIXED, and it was the worst of the four. setTrees clustered at
`mapRef?.zoomLevel ?? 12`, which is street level, so when the catalogue arrived
before the map had attached, every tree in the world was grouped into cells
sized for a street while he was looking at a continent. Nearly every pin landed
on another and was suppressed. Any region change recomputes at the real zoom,
which is why dragging the map healed it, and why it could only ever be reported
as "it was weird for a second".

## 4. The country thumbnails are poor

"ik vind de thumnbnail foto van italie nederland portugal neit mooi", plus Ireland

One cause for all eight, and a country inherits its biggest city's face, which
is why he could name four countries and four cities in a row. The ranking ended
on "widest wins", which is worse than random here: a wide shot of a place beats
a portrait of a tree every time, so Rome wore a staircase and a fountain and
Dublin wore a park overview.

FIXED as far as a machine can: anything wider than two to one is set aside, and
the last tiebreaker is a stable id rather than width. Said plainly, this removes
a bias rather than adding taste. A machine cannot tell a good photograph of a
tree from a good photograph of a park; pinning a face already works and is how
the cities that matter should get theirs.
