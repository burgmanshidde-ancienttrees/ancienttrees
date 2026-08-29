# Conventions we have looked up

Every entry here is one interaction, the product we copied it from, what that
product actually does, and where that was read. It exists for two reasons.

The first is speed. CLAUDE.md has said since 2026-08-01 that a new interaction
gets a convention check before it gets designed, and since 2026-08-20 in the
sharper form Hidde gave it: "altijd conventies volgen geen eigen ideeen." A
lookup you have to repeat is a lookup that gets skipped on a short window, so
the answer gets written down once and read after that. This is DECISIONS.md's
rule applied to interactions: never re-litigate, and now never re-research.

The second is that it makes the rule checkable. A design proposal either cites
an entry here or adds one, and `scripts/conventioncheck.py` refuses a new
screen or component whose header names no reference at all.

What belongs here: an interaction a person performs. What does not: styling,
copy, layout, or anything with pixels in it, which is per surface and is judged
by eyes rather than by precedent.

Format per entry: the interaction, the reference, what it does, the source, the
date it was read. An entry with no source URL is one recorded from our own
corpus, where the reference was named at the time but the lookup was not
written down; treat those as weaker and re-check before leaning on them.

---

## Naming the species of a tree somebody added

**Reference: iNaturalist's identify screen.** A searchable list of taxa, with
computer vision suggestions above it, and the tick is always the person's to
give. Nothing is assigned on their behalf.

**How location is used there, which is the part worth copying exactly.** The
suggestions come from the PHOTOGRAPH. Location is a second model on top of it
(their Geomodel) that FILTERS and labels the visually similar candidates as
"Expected Nearby". So the picture identifies and the place narrows; the place
never identifies on its own.

We measured what happens if it does, on 2026-08-29, because it is the free
version and the temptation is obvious. Over 1,945 published trees, the
commonest species within 500 metres is the right answer 9 percent of the time.
Tighter is worse, because a curated set avoids repeating a species in one park.
So our list is ORDERED by what grows nearby and claims nothing, until there is
a model reading the photograph. See DECISIONS.md 2026-08-29.

**A name not on the list is still typeable**, the ordinary tag-field behaviour,
and offered only when nothing matches what was typed. Offering it beside a
matching row invites a second spelling of a name we already have.

Read 2026-08-29:
- https://help.inaturalist.org/en/support/solutions/articles/151000170368-which-taxa-are-included-in-the-computer-vision-suggestions-
- https://www.inaturalist.org/blog/84677-introducing-the-inaturalist-geomodel

---

## Picking a photo from the camera roll, and where it was taken

**Reference: iNaturalist.** The camera roll is the ordinary route, not the
exception: press and hold the camera button, or tap the plus and choose the
gallery. Date, time and location are read from the photo's own metadata, and
anything missing or misread is filled in or corrected by the person afterwards.

**A photo without a location is never refused.** The observation is created and
kept, and is graded Casual rather than blocked. Only rising to the verified
tier needs photo, date and location all three. The grading is on COMPLETENESS
and not on trust: a pin the person dragged into place counts exactly as much as
one read out of the EXIF.

**Reference: Apple.** The conventional picker is `PHPickerViewController`, not
the older `UIImagePickerController`. To get the photo's location it must be
built with `PHPickerConfiguration(photoLibrary:)`, which returns an
`assetIdentifier`; the location and the creation date then come off the
`PHAsset`. That path needs photo library authorisation.

Read 2026-08-28:
- https://help.inaturalist.org/en/support/solutions/articles/151000197160-how-to-make-an-observation-with-the-inaturalist-iphone-app
- https://www.inaturalist.org/posts/89210-getting-to-research-grade-or-casual-status
- https://www.inaturalist.org/posts/6020-getting-started-make-observations-from-photos
- https://developer.apple.com/forums/thread/660696
- https://help.inaturalist.org/en/support/solutions/articles/151000197162-inaturalist-next-app-permissions

---

## Recording what you found, when the database may or may not know it

**Reference: Seek (iNaturalist).** You point the camera and it tells you what
you found. It does not ask first whether you think the thing is in its
database. So there is one button and one camera, and the outcome is resolved
afterwards from where the shutter fell. "Add" and "collect" survive as outcomes
we report, never as a choice on the way in.

Recorded from our own corpus, 2026-08-23 (Hidde: "add en collect zijn wel
moeilijk uit te leggen"). No source URL captured at the time.

---

## The camera itself

**Reference: the system camera.** `UIImagePickerController` wraps the control
every phone owner already knows. A hand-built AVCapture viewfinder is exactly
the kind of invention the rule forbids.

Recorded from our own corpus. No source URL captured at the time. Note that the
entry above supersedes this one for the LIBRARY half: the system camera stays
right for taking a photograph now, and PHPicker is the convention for choosing
an existing one.

---

## A sign-in button

**Reference: the provider's own published asset.** Apple and Google both
publish the button, its mark and its wording. Use the asset. Where no official
asset exists, copy the reference product rather than designing one.

Recorded from our own corpus, 2026-08-20, after a "Continue with Google" button
shipped as a plain bordered pill with no mark on it. Caution and invention are
not the same thing, and a sign-in button is the most convention-bound control
that exists.

---

## Feedback and reporting, and who may send it

**Reference: Google Maps.** The options are visible to everyone; acting on one
needs sign-in, and the account is the reply channel.

Recorded from our own corpus, 2026-08-21.

---

## Search

**Reference: standard consumer search.** Live suggestions under the field, and
a tap goes straight there. Not a type-and-submit form, and never a native
`datalist`, which iOS renders as a broken QuickType strip.

Recorded from our own corpus, 2026-08-01, the day the rule itself was set.

---

## A sheet that asks for one thing

**Reference: Airbnb.** The one action fills the sheet, so it sits where a thumb
already is. Everything after it is a list or a form, so those scroll.

Recorded from our own corpus. No source URL captured at the time.

---

## Directions, when the phone has more than one maps app

**Reference: WhatsApp.** Tapping an address asks which maps app to open, and
the answer is remembered; a settings row changes it afterwards. iOS cannot
answer this for an app: the default-navigation-app setting added in iOS 18.4 is
EU-only and governs Siri and Apple's own address taps, so a `maps.apple.com`
link opens Apple Maps whatever the person has chosen system-wide.

Open both destinations as https universal links, never a custom scheme. Google
documents that `https://www.google.com/maps/dir/?api=1&...` launches the Google
Maps app when it is installed and a browser when it is not
(developers.google.com/maps/documentation/urls/get-started), and `maps.apple.com`
does the same for Apple Maps. A custom scheme raises the system's own "no app
installed" alert on a phone that lacks it, which this project shipped four times.

Waze publishes no https link, only `waze://`, so it is not offered.

Recorded 2026-08-28, the day Take me there turned out to open Apple Maps on
every phone because the Google branch under it was unreachable.

---

## What signing out takes with it

**Reference: Strava, AllTrails, Google Maps.** Signing out of an account app
leaves the device showing the signed-out app: the saved lists, the ticks, the
name and the avatar all go, and they come back on the next sign-in because they
live in the account rather than on the phone. Nothing any of them do treats a
sign-out as a request to delete anything from the account.

The one thing that is NOT cleared anywhere is media the person created on that
device and may not have uploaded yet. Photographs are the case where "it is
safely in the account" can be false, and losing one is not recoverable by
signing back in.

Recorded from our own corpus, 2026-08-29 (Hidde: "de favourites en seen moet
ook leeg wanneer niet ingelogd... profielfoto moet weg als je uitlogt net als
alle hartjes op de thumbnails"). No source URL captured; the behaviour is
described from use rather than from documentation, so re-check before leaning
on it for anything larger.

---

## A default-app setting, and whether it offers to ask again

**Reference: WhatsApp, and iOS's own Default Apps screen.** An app that opens
directions and cannot read the system default asks the person once and remembers,
with a settings row to change it afterwards. The row lists THE APPS. iOS's own
Default Apps screen does the same: it names the apps and has no "ask me each
time" entry.

So the settings row here lists Apple Maps and Google Maps and nothing else
(Hidde, 2026-08-29: "directions ask again optie is niet nodig"). It still SHOWS
"Ask each time" while nobody has answered, because that is what is true then.

Extends the entry above on which maps app to open, recorded 2026-08-28.

---

## Loading a photograph over the network, reliably

**Reference: SDWebImage and Kingfisher**, the two libraries almost every iOS app
uses for this, and what they do rather than what they are. Four properties, and
SwiftUI's own `AsyncImage` has none of them: retry on a failed or rate-limited
request, a memory cache of DECODED images so a scroll back costs nothing, a cap
on how many requests run at once, and one request per url however many views ask
for it at the same moment.

Neither library is used here, because a dependency inside the product needs
Hidde's yes (hard rule 5). The four properties are the convention; the eighty
lines in `ios/AncientTrees/AncientTrees/Kit/TreePhoto.swift` are ours.

Recorded 2026-08-29 from what these libraries are known to do, after Hidde
reported "plaatjes laden weer niet" for the second time in three days. No source
URL captured at the time.

---

## How close two pins have to be before they become one

**Reference: MapLibre and Mapbox GL.** Both cluster on a radius given in
PIXELS, and both default to 50. The `supercluster` library underneath them
defaults to 40 at a 512 tile size.

**Reference: MapKit.** It takes no number at all. `MKMarkerAnnotationView`
clusters when two annotation views would OVERLAP, which is the same question
asked in the honest form: not "are these trees near each other" but "would
these pins collide on screen".

So the number belongs to the PIN, not to the ground. Ours are 38 points across,
so the cell is 44: two pins that would touch become one bubble, two that would
not stay two.

**And the honest half of the answer, which no number fixes.** The case that
prompted this was Baarn, where a bubble marked 2 covers two trees standing 34
metres apart. At the zoom he was looking at, 34 metres is about ten points: the
two pins are on top of each other whatever we do, and the bubble is telling the
truth. What a smaller cell buys is the cases where the pins were merely near,
not overlapping.

Read 2026-08-29, after Hidde saw two trees a couple of streets apart in Baarn
drawn as a bubble marked 2:
- https://maplibre.org/maplibre-style-spec/sources/
- https://docs.mapbox.com/style-spec/reference/sources/
- https://github.com/mapbox/supercluster
- https://developer.apple.com/documentation/mapkit/mkannotationview/clusteringidentifier

---

## What a sign-in sheet says

**Reference: Google Maps, AllTrails, Airbnb, Apple.** One short line about what
an account is FOR, and then the buttons. None of them counts what you have, and
none of them describes the syncing.

Both halves matter and we had got both wrong: "Sign in to keep your 7 trees"
prints a fact about this moment into a sentence, and "Sign in and they follow
you to the website and to any phone" is a promise about a mechanism that has to
stay true through every change to it. Hidde, 2026-08-29: "hou het maar wat
oppervlakkiger zodat we niet elke keer als we iets wijzigen die tekst niet meer
klopt."

So the copy says what somebody GETS and never how, and never how much.

Recorded from our own corpus, 2026-08-29. No source URL captured; the wording
of each app is described from use.

## App Store screenshots (2026-08-29)

**Looked up:** AllTrails (id405075943), komoot (id447374873), PictureThis
(id1252497129), read off their own App Store pages rather than remembered.

**What all three do, without exception:** a solid brand-coloured ground rather
than the white of the screenshot; a caption at the TOP, one or two lines, four
to six words, benefit first; and the screen inset below it, cropped at the
bottom rather than shrunk to fit, so it reads as a phone in use.

**Where they differ:** AllTrails draws a black device bezel; komoot and
PictureThis let the screen bleed to the panel's sides. We follow AllTrails,
because our screens are pale and map-heavy and without a bezel the panel and
the screenshot melt into each other.

**The pattern worth more than the styling:** the first panel carries a promise
rather than a screen. AllTrails opens on black with "Discover 500,000+ trails",
komoot with "Explore 7M+ routes". A gallery gets scrolled; the first frame is
the only one everybody sees.

Ours: `scripts/appstore_frames.py`, run after `appstore_shots.py`.
