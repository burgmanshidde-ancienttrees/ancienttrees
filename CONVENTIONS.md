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

## Two sign-in buttons stacked, and why they cannot fully agree

**Looked up 2026-09-01:** Apple's Human Interface Guidelines and
https://developers.google.com/identity/branding-guidelines, read rather than
remembered.

**What each provider specifies, and they differ.** Apple's
`SignInWithAppleButton` is Apple's own control: it centres its mark and its
words together as one group and derives its type size from the button's height.
Nothing about that is adjustable. Google's spec puts their mark at the LEADING
edge with 16 points of padding on iOS, at 14 point text, with the mark larger
than the type.

Follow both literally on one sheet and you get what Hidde saw twice: one mark
at the left edge and one near the middle, one large label and one small.

**What Google actually forbids** is altering the mark itself: "You can't change
the size or color of the Google 'G' logo. It must be the standard color
version." They permit a custom button outright, while recommending their SDK.
Apple effectively does not, so ours is the only one of the two that can move.

**So: ours matches theirs.** Mark and label centred as one group, label at the
same size Apple draws, mark sized against Apple's rather than by Google's own
ratio. `Screens/GoogleButton.swift` carries the numbers and the measurements
behind them.

**The residue, so nobody chases it again:** the two marks still sit about 7
points apart, because "Google" is a wider word than "Apple" and both groups are
centred. Both are perfectly symmetrical about the screen's centre; the gap is
arithmetic, not a mistake. Closing it entirely means replacing Apple's own
button with a hand-drawn one, which is the thing the entry above was written
against.

---

## Alignment on a sheet, centred or leading

**Reference: Apple, WWDC25 "Get to know the new design system".** Typography is
"now bolder and left-aligned to improve readability in key moments like alerts
and onboarding". Apple has moved its own onboarding sheets off centre.

Ours followed on 2026-09-01, sign-in sheet first, chosen by Hidde from
photographs of both ("rechts ziet er beter uit"). The rule that came with it
matters more than the alignment: it is a WHOLE-SHEET decision. Mark, headline,
subtitle, small print and links move together or not at all. A single element
switched to make a layout check go quiet is how that sheet ended up with one
flush-left paragraph above its centred twin earlier the same day.

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

## The splash screen, and how long it stays (2026-08-30)

**Looked up:** Apple's Human Interface Guidelines, "Launching", and Android's
"Splash screens" developer guide, both read on the day.

**Apple allows this, and names it.** "If you need a splash screen, consider
displaying it at the beginning of your onboarding flow... If you don't provide
an onboarding experience, you might display your splash screen as soon as
launching completes." What it refuses is a dressed-up LAUNCH SCREEN, which
"isn't part of an onboarding experience or a splash screen, and it isn't an
opportunity for artistic expression". Those are two different objects and
conflating them is what made me tell Hidde four times that his idea was not
possible.

**Neither platform publishes a duration for a branded cover.** Android's
"we recommend not exceeding 1,000 milliseconds" is the cap on its system
splash's ICON ANIMATION, and its own advice for a slower start is a looping
animation rather than a longer wait.

**So the number comes from the sentence on it.** Seven words is roughly 1.7
seconds of reading at an ordinary pace, and that clock starts only once the eye
has found them. Ours ran 1.4 seconds and was gone before it could be read. It
is 2.4 now, with a tap taking it away sooner and no appearance at all when the
app comes back from the background.

---

## A permission somebody refused (2026-08-30)

**Reference: Apple Maps, driven directly rather than read about.** Location was
revoked for com.apple.Maps on a simulator and the app was walked with "Don't
Allow" tapped, which is the only way to be sure what it does. Screenshots in
docs/conventions/. Apple's own map app is the strongest reference we have for
this, because it is the same product shape as ours and it is written by the
people who wrote the permission system.

**What it does, in the order you meet it:**

1. **The map works completely.** Every control, search, the sheet, all of it.
   Nothing is blocked and nothing is greyed out.
2. **It does NOT pretend to know where you are.** It zooms out to a regional
   view instead of centring on a guess. There is no fake blue dot and no
   distance to anything.
3. **A pill sits at the top of the map, permanently: "Location Services is Off
   >".** In the app's accent colour, with a chevron, always visible while the
   state lasts. Not a banner that dismisses, not a toast, not a modal on
   launch. It is a piece of the map's furniture for as long as the state is
   true.
4. **Tapping it does NOT jump to Settings.** It opens a sheet first:

   > **Maps works best with Location Services turned on.**
   > You'll get turn-by-turn directions, estimated travel times and improved
   > search results when you turn on Location Services for Maps.
   > [ Turn On in Settings ]  [ Keep Location Services Off ]

   Three things in that sheet are worth copying exactly. The title says what
   the app CANNOT DO WELL, not that you refused something. The body lists
   named features rather than naming the permission. And the second button is
   "Keep Location Services Off" rather than "Cancel", so declining a second
   time is a decision somebody makes rather than a dialog they escape.
5. **Every control that needs location leads to the same sheet.** The recentre
   arrow raises it too, verified separately. Not one of them is a dead button
   that silently does nothing, which is the failure this rule mostly exists to
   prevent.

**Apple's written rule agrees and adds the constraint.** Rather than reporting
an error when somebody reaches a feature whose permission is denied, explain
why it cannot be used and provide a link to where they can toggle it on. The
system dialog fires once per permission ever, so after a refusal there is no
second prompt at any price: `UIApplication.openSettingsURLString` opens our own
page in Settings and is the only route back. There is no supported way to
deep-link a single toggle, which is why handing somebody the page beats writing
out a tap-by-tap path.

**Reference: AllTrails, from Hidde's own phone (2026-08-30).** A plain system
alert, not a designed screen: "AllTrails heeft toegang nodig tot je exacte
locatie tijdens het navigeren", one sentence of body saying the same thing, and
[Oke] / [Annuleren]. Two things it confirms and one it gets wrong. It confirms
that a plain alert is enough, no illustration and no custom sheet, and that the
title should name THE FEATURE ("tijdens het navigeren") rather than the
permission. What it does not do is say where the setting is, which is the half
Hidde asked for and the half our own measurement says is necessary.

**MEASURED, and it changes the recommendation: `openSettingsURLString` did NOT
land on our app's page.** Tested 2026-08-30 on iOS 26.5 with the real path,
somebody tapping "Don't Allow" on the system dialog and then our chip. It
opened the ROOT of Settings. The AncientTrees pane exists and is reachable, but
it lives at Settings > Apps > AncientTrees > Location, which is four steps from
where the button drops you, and iOS 26 moved apps under an "Apps" row that is
most of a screen down from the top. Nothing on screen says any of that.

Caveat kept honestly: this was a Debug build on a simulator, and a real App
Store install may land on the pane. But the conclusion is the same either way,
because we cannot tell which one a given phone will do, and the cost of naming
the path when the button happened to work is one line of small type.

**So the sheet names the path.** One line, in the app's own words, under the
buttons: Settings > Apps > Ancient Trees > Location. Not a numbered tutorial
and not an illustration, which is the overbuilt version of this and ages badly
every time Apple moves a screen. One line, so somebody who lands at the top of
Settings knows what they are looking for.

**Degrade before you explain.** Where the task can still be finished another
way, do it that way and say why it changed. A refused camera opens the library;
a refused photo library still shows the picker and asks where the tree stands.
Explaining a dead end is worth less than not having one.

**And a permission REFUSED is not a fact MISSING.** They must never share a
sentence. "Your photograph does not say where it was taken" is true of a
screenshot and false of somebody who refused the library, and the second person
cannot act on the first sentence.

Read and driven 2026-08-30:
- Apple Maps on iOS 26.5, location revoked via `simctl privacy revoke`
- https://developers.apple.com/design/human-interface-guidelines/patterns/accessing-private-data/
- https://useyourloaf.com/blog/open-settings-url/

---

## Measuring what people do in the app (2026-08-30)

**Reference: every benchmark app measures, and all of them do it in two or
three separate layers.** Read off the Exodus Privacy teardowns of the shipping
Android builds, which list the SDKs actually compiled into the binary rather
than what a privacy policy claims. AllTrails was version 26.8.30, current on
the day this was read.

| App | Crash | Product analytics | Ad attribution |
|---|---|---|---|
| AllTrails | Crashlytics | Amplitude, Firebase Analytics | AppsFlyer, Branch, Facebook, AdMob |
| Strava | Sentry | Firebase Analytics | Branch, Facebook |
| Polarsteps | Crashlytics | Mixpanel, Firebase Analytics | AppsFlyer |
| Komoot | Crashlytics | Firebase Analytics | Facebook |
| PictureThis | Crashlytics | Firebase Analytics | Adjust |
| iNaturalist | Crashlytics | none | none |

**The three layers are separate decisions and get taken separately.** Crash is
"did it break", and we have it already without a third party (MetricKit,
Kit/Diagnostics.swift). Product analytics is "what did they do", which nobody
here has. Attribution is "which advert sold this subscription", which is
marketing-spend infrastructure and is the layer that drags in the ATT prompt
and the consent question; it is worth nothing to a product that buys no ads.

**iNaturalist is the proof that the middle layer is a choice rather than a
requirement**, and it is the closest thing to us in posture: a naturalist app,
a nonprofit, no advertising, crash reporting only. What it does not have is a
paywall, and a trial that has to convert is precisely the question Amplitude
exists to answer for AllTrails.

**The convention is first-party events, not the SDK.** Amplitude and Mixpanel
are hosted event tables with a dashboard on top; what they receive is a stream
of named events with properties. Our website already sends exactly that shape
to our own `events` table (`track()` in site/src/layouts/Base.astro), so the
app copying that pattern IS the convention, minus a vendor. It also keeps hard
rule 5 shut, needs no ATT prompt (first-party, no advertising identifier, not
shared across companies) and adds nothing to the privacy label that would be
linked to a person.

Read 2026-08-30:
- https://reports.exodus-privacy.eu.org/en/reports/com.alltrails.alltrails/latest/
- https://reports.exodus-privacy.eu.org/en/reports/com.polarsteps/latest/
- https://reports.exodus-privacy.eu.org/en/reports/de.komoot.android/latest/
- https://reports.exodus-privacy.eu.org/en/reports/org.inaturalist.android/latest/
- https://reports.exodus-privacy.eu.org/en/reports/cn.danatech.xingseus/latest/
- https://reports.exodus-privacy.eu.org/en/reports/com.strava/latest/

---

## How a settings page is built, and where deleting an account sits (2026-08-31)

**Looked up because Hidde asked twice on one afternoon**: first whether Delete
account could sit under Sign out on the main list, then how a settings page is
built at all. Described from use rather than from documentation, like the
sign-out entry above, so re-check before leaning on it for anything larger.

**Reference, on a phone: Strava, AllTrails, Komoot, and Apple's own Settings.**
All four are built the same way, top to bottom:

1. An identity card first: picture, name, and a chevron into the account.
2. Grouped sections under small uppercase headers, never one long list.
3. Rows of one shape: leading icon, label, then either a value or a chevron.
4. **Sign out at the BOTTOM of the main list**, on its own, away from everything.
5. The version number last.

**Where deletion sits, and it is unanimous:** inside the Account screen, one
layer in. Strava is Settings, My Account, Delete Account. AllTrails is Settings,
Account, Delete account. Google, reached from Maps, buries it four layers down
under Data and privacy. Instagram puts it under Accounts Centre, Personal
details, Account ownership and control.

Not one of them puts it on the main settings list beside Sign out. What they all
DO is ask more than once: Strava confirms and then mails you, Google makes you
sign in again.

**So the two halves of the same instinct point in opposite directions.** Making
it harder to trigger is exactly right and is what everybody does. Moving it up
next to Sign out would make it easier to trigger, and nobody does that. The
answer that satisfies both is the one already in the app: keep the Account row,
keep deletion inside it, and add the second confirmation.

**Reference, on the web: GitHub, Airbnb, Strava, Google.** Different shape,
same logic. Settings is its own page, sections are cards or a side navigation,
and Account is a section that opens its own page. Destructive actions sit in a
marked area at the bottom of that page; GitHub calls it the Danger Zone in so
many words. **Sign out is not on the settings page at all on the web**: it is in
the user menu at the top right, which is where somebody looks for it.

**What that means for us.** The app already follows this and needs no change
beyond the second confirmation. The website does not: /account is one flat card
with sign out and delete side by side on it, where a mis-click is one pixel
away from the other.


---

## When the location question is asked (2026-08-31)

**Settled where it started, after going round the houses in one afternoon.** The
entry of 2026-08-30 has Apple Maps raising its location sheet only from a control
that NEEDS location, with a permanent "Location Services is Off" pill as map
furniture in the meantime. That is what we do.

The detour is worth recording, because the argument against it was good and it
still lost. Told the convention, Hidde first overruled it: "dit gebeurd te weinig
dus ik zou map interactie doen ... gewoon scrollen ofzo." The reasoning is sound
on its face. Apple Maps can afford to wait for that button because it is already
the map you opened on purpose; ours is a discovery app whose promise is the trees
around you, and somebody who never taps the arrow never gets asked.

So it was built: the map first, and a card over the blurred map on the first pan
or pinch. Then he walked it and dropped it: "ik vind eigenlijk dat je het heel
goed hebt opgelost met een no location [chip] op de map en dat je die kan
inklikken, wat mij betreft vergeten we het hele overlay scherm."

**What the detour actually proved, and it is the useful part.** The worry behind
"dit gebeurd te weinig" was that nobody would ever be asked. That worry was
unfounded here, and only checking the code showed it: our chip is not the Apple
one. It appears whenever we have no location AT ALL, including a fresh install
where nothing has ever been asked, and tapping it goes straight to the system
prompt. Apple's appears only after a refusal. So the ask is already in front of
everybody, permanently, on the main map, and an interstitial would have been a
second ask in front of a first one.

**The rule, then:** no screen in front of the system prompt. The map opens, it
says plainly that location is off, and the person taps it when they want it. One
line in TreeMap carries the weight of this: `showsUserLocation` stays false until
somebody has already said yes, because MapLibre asks the system the moment it is
set, and without that guard iOS would get in first, on launch, with no reason
given.

---

## Landing after you have added something (2026-09-01)

**Looked up because Hidde walked the add-a-tree flow and found two things at
once: the loudest button on the page you land on is about going somewhere, and
nothing anywhere says the tree was saved.**

**Reference: iNaturalist.** Sharing an observation puts you on your own Me
page, where the observation you just made is the top row and carries its own
upload state. You are never left wondering whether it took.

**Reference: Google Maps.** Adding a missing place shows a short thank-you at
the moment you submit, the place appears under Your contributions, and the
verdict arrives later by mail. The acknowledgement and the STATUS are two
different things: one is a second long, the other stays true until the review
is over.

**Reference: Apple's HIG, "Feedback".** Status feedback belongs near the item
it describes, so somebody gets it without leaving what they are doing, and an
alert is never used merely to inform: "People don't appreciate an interruption
from an alert that's informative, but not actionable."

**Reference: Material, acknowledgement.** A submitted form is acknowledged by
one line at the bottom of the screen, briefly, with at most one action on it
(Undo). Not a dialog, not a screen.

**So the pattern, in three beats.** (1) You land on the THING you made, or on
the list holding it. (2) It is acknowledged in one line at the moment it
happens, non-modal. (3) Its state is written ON it and stays there while it is
true, because a toast leaves no trace and somebody coming back an hour later
has no way to ask.

**And the fourth, which is where ours went wrong:** the loudest control on that
page belongs to the thing you just made, which means finishing it or leaving.
Directions to a tree you are standing under, and "Add a tree" on the tree you
have this second added, both read as though the save did not take.

Read 2026-09-01:
- https://help.inaturalist.org/en/support/solutions/articles/151000192921-how-to-make-an-observation
- https://support.google.com/maps/answer/6320846
- https://support.google.com/maps/answer/9678350
- https://developer.apple.com/design/human-interface-guidelines/patterns/feedback/
- https://m2.material.io/design/communication/confirmation-acknowledgement.html

---

## Sharing something you made that has no page (2026-09-02)

**Reference: Strava.** Tapping share on your own activity draws a CARD rather
than sending a link: your photograph or your map, the facts on top of it, their
own mark in the corner, handed to the system sheet. Where the activity carries
photographs it asks which to use; where it carries none it uses the map.

**Reference: iNaturalist, which does the opposite and shows why.** Its share is
a LINK, because every observation has a public page. Ask which of the two you
are before copying either: a link is better when there is something to link to,
and an invention when there is not.

**Ours has no page.** A tree only you have holds no address on the web, so the
picture is the only honest thing to send. It carries the name, the date, the
species where you have named one, and the wordmark, which is the whole reason
to draw a card rather than to send the bare photograph.

**And the shape: 4:5 at 1080 wide**, which Instagram, WhatsApp and Messages all
show without cropping into it. Strava also draws a 9:16 story sticker; that is a
second size, for the day somebody asks.

Read 2026-09-02:
- https://support.strava.com/hc/en-us/articles/221089587-Sharing-Your-Strava-Activities
- https://forum.inaturalist.org/t/getting-creating-a-link-to-your-observations-so-they-can-be-shared-etc/49896

---

## A page for something a person added, and who may see it (2026-09-02)

**Looked up when Hidde asked the obvious next question about the share card:
"kunnen we niet een pagina maken van de boom die wel deelbaar is?"**

**Reference: Strava.** Every activity has a URL, and every activity carries a
visibility of its own: Everyone, Followers, or Only You, settable per activity
and as a default. Map visibility is a SEPARATE control on top of that, so
somebody can share the ride and hide where it started.

**Reference: iNaturalist.** Every observation has a public page and the default
is open, because the whole product is sharing. What is not open by default is
the LOCATION: observations of at-risk taxa are obscured automatically to a
0.2 degree cell, and only the observer and people they trust see the real
coordinates. The precision of the location is treated as a separate question
from whether the record is public.

**Reference: Google Maps.** A place somebody adds gets its page only after
review. Until then it lives in Your contributions, visible to them alone.

**So the convention is three decisions, not one:** does the record have a page,
who may open it, and how precise is the position on it. Every reference answers
them separately, and the two that publish user records both hold something back
about WHERE.

**What that means here, where the whole product is a map of exact trunks.**
Hard rule 10 already says we never undo a location a source withheld and never
send strangers to somebody's home, and a tree a person photographed may be
either. So a page for one of these carries the same three answers, and the
location one is not a detail: a garden tree is the case, not the exception.

Read 2026-09-02:
- https://support.strava.com/en-us/articles/15401987-Activity-Privacy-Controls
- https://www.inaturalist.org/pages/geoprivacy
- https://support.google.com/maps/answer/6320846

---

## Switching the language of a page

**References: komoot and AllTrails, both read directly on 2026-09-02.** Both are
the standing outdoor references, both are SEO-driven, and both translate real
content rather than only their interface, which makes them the closest thing to
our problem that exists.

**Where the control lives: the FOOTER, last item, in both.** Neither puts it in
the header, and neither uses a flag. komoot's is a plain line reading `English`
at the very bottom, after the legal links. AllTrails' is a native `<select>`
with `aria-label="Select a language"` in the footer's own `languageSelect`
block.

**How the options read: endonyms, the language named in itself.** komoot shows
`English`. AllTrails goes further and adds the country in the same language,
`English (US)`, `English (UK)`, `Dansk (Danmark)`, because it distinguishes
locales rather than languages. Not flags: a flag is a country and several of
these languages have no single country.

**URL shape: locale subdirectory, English on the bare path.** komoot uses
`/de-de/discover`, `/ja-jp/discover`, with `/discover` itself being English.
AllTrails uses `/de/parks/...`, `/es/parques/...`, English again on the bare
path.

**And AllTrails translates the PATH SEGMENT, not just the content:**
`/parks/us/california/yosemite-national-park` becomes `/parken/...` in Dutch,
`/parcs/...` in French, `/parchi/...` in Italian, `/parques/...` in Spanish and
Portuguese. This is worth recording because it is exactly what Contract J
already does with our question pages, `/seville/oldest-tree` against
`/es/seville/arbol-mas-antiguo`. Our URL design matches the reference without
having been checked against it, which is luck rather than judgement, and it is
now checked.

**Both emit `hreflang` for every locale of the page**, including
`x-default`, which we also already do.

**What we do that they do not, and it is defensible.** Our language link is
inline on the page itself ("Esta página también está disponible"), written in
the target language, rather than a site-wide control in the footer. That serves
a reader who landed on the English page from Google and would prefer their own,
which is our actual traffic pattern. The two are not exclusive and the footer
control is the one we lack.

**The gap this lookup was done for.** A translated page of ours sits inside an
English frame: on `/es/seville` the navigation still reads Map, Cities,
Countries, Species, Parks, Collections, and the buttons still say "Suggest a
tree", "Sponsor this project" and "Get the app". Both references translate
their chrome into every locale they serve. Ours is roughly twenty strings.

Sources, read 2026-09-02: `komoot.com/discover` (footer, and its 14 `hreflang`
alternates) and `alltrails.com/parks/us/california/yosemite-national-park`
(footer `Footer_languageSelect`, and its 12 `hreflang` alternates). Airbnb was
not usable as a reference here: its page is behind a consent wall and its globe
control covers language, currency and region together, which is a different
problem from ours.

---

## Opening a photograph at full size (2026-09-03)

**Reference: Wikipedia's Media Viewer**, and it is the closest reference we have
because it has our exact content problem: photographs under a licence that
obliges a credit. Clicking a thumbnail opens a LIGHT BOX over the page, not a new
page. The image is shown at a screen-sized version, with the caption, the author,
the source and the licence along the bottom. Clicking the image INSIDE the viewer
is what goes to the original at full resolution. Escape closes it, an X sits top
right, arrow keys move between the images of a page.

That is the two-step Hidde described before either of us had looked it up: a
standard size on the page, the whole photograph one click further. It is worth
naming because the tempting shortcut is to link the thumbnail straight at the
original file, and that hands somebody a 6 MB image with no credit attached to it.

**Reference: Apple Photos, and every iOS viewer copying it.** The gestures are
not ours to invent and people arrive already trained: pinch to zoom and pan,
double tap to zoom in and out at once, drag DOWN to dismiss, single tap to hide
the chrome and leave only the picture. A viewer missing swipe-down is the one
people complain about, because it is the gesture the hand reaches for first.

**The size half, which is the part that actually bit us.** The convention is one
picture at several widths and the surface picking, `srcset` on the web and the
right url per view in the app. What it means in practice is that there has to be
something BETWEEN the card size and the raw original. We had 500px and then a
3008px, 6.6 MB file and nothing in between, so every card was a 500px image
stretched over a 1170px phone screen, and every hero was either capped or
enormous.

**Wikimedia's live thumbnail widths, re-probed 2026-09-03 on two different files:
250, 330, 500, 960, 1280, 1920.** 320, 400, 640, 800, 1000, 1024, 1600, 2000 and
2560 all return 400. The list written down here on 2026-07-31 stopped at 960 and
was incomplete, which had capped every Wikimedia hero in the app and on the web
at 960px since. This is the third time a probed verdict about Wikimedia has
outlived the fact; re-probe before trusting one.

Read 2026-09-03:
- https://www.mediawiki.org/wiki/Help:Extension:Media_Viewer
- https://en.wikipedia.org/wiki/Wikipedia:Media_Viewer
- https://www.lightgalleryjs.com/ (escape to close, arrows to move: the same two on every web lightbox library)

---

## A profile page, and where settings sit (2026-09-02)

**Reference: Polarsteps' own profile, and our app's My trees screen.** Hidde
put the two side by side and asked for the same shape on the web. What both do,
in this order: the avatar and name, a small follow line, a row of counts, one
primary action, then the person's lists as tabs. Settings are NOT on the page.
They sit behind a gear in the top corner and open a screen of their own.

Polarsteps: avatar, name, `51 Landen / 21 Volgers / 24 Volgend`, a red "Voeg een
reis toe" button, then Reizen / Statistieken as tabs. Read from
polarsteps.com/HiddeBurgmans, 2026-09-02.

Strava, AllTrails and Airbnb are the same shape, and it is the shape our own
`Collect.swift` already had. What the website had instead was a sign-in card
first, then account admin, a name editor and a delete panel stacked around the
trees, which is the fault Hidde found in the app on 2026-08-21 ("my first button
I see is to sign out or delete accounts") surviving a fortnight longer here.

**The counts are the app's counts, not new ones**: trees you have stood in
front of plus the ones you added, the species among them, the countries. Taken
from Collect.swift so two surfaces cannot answer the same question differently.

**What differs per surface, and only this**: adding a tree is a camera sheet on
the phone and the contribute form on the web, because a laptop has no camera in
a park. The behaviour matches, the design does not have to (CLAUDE.md's
both-surfaces rule).

---

## A feature that lives in the app only (2026-09-02)

**Reference: our own AppModal, which already followed AllTrails.** When the
website carries a control for something only the app does, the control opens
the one app overlay. It does not navigate to a teaser page, and it does not
sometimes do one and sometimes the other: a control that behaves two ways is
two controls.

This settled the walks. They are the Plus product, so a web page showing the
route undercuts what is sold and a web page teasing it half-delivers. Hidde:
"stuur ze maar gewoon naar de app. Dan kunnen we zien hoe vaak het wordt geklikt
en gaan we dan maar snel die walks in de app maken." The tap count is the point:
it is what times the work in the app.

**The honesty half, which is ours rather than borrowed**: a page may only
mention the feature where it genuinely exists. `hasWalksPage()` gates whether
the word "walk" appears at all, so we never advertise a route the app does not
have. Enforced by `check_walks_go_to_the_app()` in scripts/qa.py.

---

## Dark mode, and what a map app darkens (2026-09-03)

Looked up the day the app shipped, because two of the first people to open it
were in dark mode and it was not nice. Half the app's surface had never been
photographed once: a simulator boots light and nothing had ever told it
otherwise, so every screenshot the sweep had taken in two weeks was daylight.

**Reference: Google Maps, Apple Maps, and OpenFreeMap's own dark style.** All
three darken the MAP, not only the chrome around it. Google publish their night
style array as a worked example, and two of its rules are structural rather than
decorative:

- **Water is DARKER than the land**, so it recedes at night: their land is
  `#242f3e` and their water `#17263c`. Ours had never been asked the question,
  because in daylight water is lighter than land and the instinct is to keep
  that relation.
- **Every label's halo is the background colour**, so a place name reads as a
  gap cut around the letters rather than as an outline drawn on top of the map.

OpenFreeMap serve a dark style over the same OpenMapTiles source and on the same
layer ids we use, which is what makes ours a colour mapping rather than a rebuild.

**Reference: Material's dark theme, for what a filled control does.** A dark
theme takes its accent from the LIGHT end of the ramp, tone 200 rather than the
daylight 500, and the label on it is DARK. Google's own dark products press in
`#8AB4F8` with near-black text, not in their daylight blue with white. This is
the rule we had half of: our moss did lighten in the dark and the label stayed
white, which measured 2.85:1 and looked like a highlighter.

**Reference: Apple's HIG, for depth.** In the dark the system uses two sets of
backgrounds, base and elevated, and a thing in front is LIGHTER than the thing
behind it. Nothing is separated by a shadow, because a shadow is invisible on a
dark ground. So the order in this app is map, then screen, then card, then sheet,
each a step up.

**What we got wrong and would get wrong again: a translucent material samples
what is behind it.** The bottom sheet, the floating "Map" pill and the round
buttons on the tree page are all `.regularMaterial`. On a cream map they render
light grey and white, which reads as a foreign panel dropped on a dark app. None
of those three was a bug in the chrome. Fixing the map fixed all of them, and
the general form is worth keeping: on a screen where something floats over
content, judge the floating thing against the content it will actually sample.

**What does NOT change in the dark: photographs.** Apple treat a photograph as
content and leave it alone, and AllTrails, Airbnb and Google all run full-bleed
pictures at full strength on a dark ground. Material's advice to cut luminance
applies to decorative imagery, which for us is the green tile a tree with no
photograph wears; that one is dimmed, the photographs are not.

Read 2026-09-03:
- https://developers.google.com/maps/documentation/javascript/examples/style-array
- https://tiles.openfreemap.org/styles/dark
- https://developer.apple.com/design/human-interface-guidelines/dark-mode

## Sending a mobile visitor to the app (2026-09-03)

Hidde, on the AllTrails sheet that had just interrupted him on his own phone:
"zijn we al zover dat we net als bij alltrails een overlay willen doen op de
mobiele website om mensen naar de app te sturen", and then the question that
decided it: "of gaan we daar seo mee killen?"

**Measured rather than remembered.** Each site below was fetched on 2026-09-03
with an iPhone Safari user agent and read for what it actually ships.

| Site | Apple's `apple-itunes-app` meta | Its own banner |
|---|---|---|
| komoot | yes, with `app-argument` | yes, an `AppBanner` component |
| iNaturalist | yes on the homepage, **none on a deep taxon page** | yes |
| Strava | no | yes, its own `SmartBanner` |
| Marktplaats | no | yes, its own `SmartBanner` |
| AllTrails | no | yes, the full-screen sheet |
| Reddit, Pinterest | no | yes, their own overlays |
| TripAdvisor | `app-id=-1`, which is the tag deliberately switched off | |
| Wikipedia | no | nothing at all |

**Four things that table says.**

1. **There are two schools and almost nobody abstains.** Apple's native meta
   tag, or a banner of their own. Only Wikipedia ships neither, and Wikipedia
   depends on search more completely than anybody else on the list.
2. **The nearest neighbour does both.** komoot is our shape exactly: outdoors,
   routes, a large SEO surface, European. It ships Apple's tag AND a component
   of its own, which is the answer to "which one" being "both, in that order".
3. **`app-argument` is the piece worth copying.** komoot hands the app the URL
   the person is standing on, so opening the app lands on that route. Without
   it the app opens on its own home screen and the reader has to find their way
   back to what they were reading.
4. **iNaturalist puts the banner on the homepage and not on the content page.**
   That is the cautious reading of the same worry Hidde had, and it is worth
   knowing somebody made that call deliberately.

**What we do, and why it is not the sheet from his screenshot.** Google names
an interstitial that covers the content on arrival from search as an intrusive
interstitial, and names a banner using a reasonable amount of screen space as
the exception, with Apple's smart app banner as its own example. AllTrails can
carry the cost because a large share of their traffic types "alltrails" into
the box. Ours is long-tail search with no referring domain a human made, so the
one channel we have is the one the sheet puts at risk. We take Apple's banner.

**What Apple's banner cannot do, which is the whole of the remaining gap.**
Safari draws it; Chrome on iOS and every in-app browser (Instagram, the Google
app) do not, and the screenshot Hidde sent was one of those. So a banner of our
own still has a job, and its shape is settled by the same reasoning: a bar at
the top of the page that pushes the content down rather than covering it, one
dismissal that sticks, iOS only, and never a dimmed backdrop.

**The badge is Apple's own artwork**, localised per language from Apple's badge
service, one file per language in `site/public/assets/appstore/`. A store
button is the most convention-bound control there is and drawing our own pill
with the words typed into it is the exact failure of 2026-08-20.

---

## Asking for an App Store review

**Reference: Apple's own SKStoreReviewController guidance**, not a specific
third-party app. Use the native `.requestReview` SwiftUI environment action
only; never a custom "are you enjoying this?" screen in front of it, which
App Store Review Guideline 5.6.1 forbids as satisfaction gating. Never wire
it to a "Rate us" button. Ask at the end of a sequence the person has just
completed successfully, never on launch and never mid-task.

**Where we ask: ticking a tree**, `CollectSheet.claim`, the moment already
described in that file's own comment as "the payoff... the app's job at
that exact second is to tell them what it is." AllTrails-style outdoor
apps ask after completing a whole trail; our closest equivalent is
finishing a curated Walk, but that feature is still lightly used, so the
ask is tied to the tick itself, which works for everyone. See
`Kit/ReviewPrompt.swift` and DECISIONS.md-shaped reasoning in
`docs/superpowers/specs/2026-09-03-review-prompt-design.md`.

**Milestones, our own choice (Apple sets no specific numbers):** the 3rd,
10th and 25th tree ticked, each asked once, at least 7 days apart, 3 asks
in the phone's lifetime. The 3 echoes `Nudge.swift`'s own "third save...
starts to look like a collection" reasoning, reused here as the same
restraint pattern applied to a different ask.

Read 2026-09-03:
- https://developer.apple.com/documentation/storekit/requesting-app-store-reviews
- https://www.avanderlee.com/swift/skstorereviewcontroller-app-ratings/
