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
