# What AllTrails does, and which of it we take

Written 2026-08-19 from three screen recordings and three screenshots Hidde made
of the AllTrails iOS app and website. The convention rule says look at how the
best consumer products do an interaction before inventing one; this is that
lookup, done once and written down so the app build does not re-derive it.

Source material: 42 frames at `scratchpad/at1..at3`, extracted with
`scripts/gear/frames.swift`. A recording carries what a screenshot cannot, which
is what happens BETWEEN two states.

---

## The shape of the whole app

Four tabs, and they are verbs rather than nouns: **Verkennen, Opgeslagen,
Navigeer, Activiteit**. Ours are find, walk, collect, season. Three of the four
map almost exactly, which is worth noticing before we invent our own navigation:
explore is find, navigate is walk, activity is collect. Nothing in AllTrails
corresponds to season, which is our one genuinely different idea.

A floating green **Kaart** pill sits above the tab bar on every list screen and
toggles list to map. One control, always in the same place, and it means the
user never has to decide which of two pages to be on. We currently ship the map
and the list as separate destinations.

## 1. The list, and what a card carries

Search field, then a horizontal row of filter chips (Alle, Moeilijkheid, Lengte,
Hoogte), then a result count with a sort control ("347 routes", "Meest
relevant"). Each card is a photo carousel with dots, a heart, a download button,
and a **small map inset in the corner of the photo** showing the route's shape.

That inset is the cheapest good idea in the whole app. It answers "what shape is
this walk" without opening anything, and it costs one static image. Our tree
cards show a photo and no geography at all.

The meta line under the title is four facts and no prose: rating, difficulty,
length, time. Ours would be species, age, girth, walk time.

## 2. The route detail, on a map

Tapping a route does NOT open a page. It drops a sheet over the map with the
route already drawn:

- title with a `›` meaning there is more
- a stat row of four icons: distance, ascent, descent, time
- an **elevation profile chart**
- two buttons: `Downloaden` (secondary) and **`Begin`** (primary, green, arrow)

The whole decision happens in one screen, on top of the thing being decided
about. The primary action is one word and it is a verb.

**This is the answer to our own worst number.** `directions` has never fired
once on our site. We ask people to read a story and then find a button; AllTrails
puts Begin under a picture of the route with the elevation under it.

## 3. The web page, and the app interstitial

The website route page is a hero photo carousel with the same map inset, a title,
a rating and difficulty line, then a **four-stat row with labels underneath**
(Lengte, Hoogteverschil, Geschatte tijd, Ronde). Primary button is `Delen`,
secondary is `Kaart`.

Then the interstitial: "AllTrails werkt beter in de app", 4,9 stars and 1M+
reviews, an App Store editor's-choice badge, and one dark button, `Ga verder in
de app`. Sign-in with Google sits below it as the alternative, not the ask.

Note what they lead with: social proof, not features. And they interrupt on a
CONTENT page, once the visitor is already interested.

## 4. Activity, which is our collect verb

Tabs Jij / Community / Volgend. Two summary cards at the top: a stats card
(activities, distance) and **Parkstempels**, park stamps drawn as little
illustrated badges, one per national park. Below that, a searchable log of
activities, each a map thumbnail of the recorded track with a title and date.

The stamps are illustrated, not iconographic: Arches, Yosemite, Joshua Tree each
get a small painted scene. That is the same instinct as our painterly tree art,
and it is the model for our badges. A collection screen needs something worth
looking at, not a grid of ticks.

## 5. The paywall, and the one box to copy outright

€29,99 a year, seven days free. Hidde's own line, set 2026-08-18, is €19,95, so
we undercut them by a third.

The headline is a gift rather than a trial: **"De eerste week krijg je van ons."**
Then a box titled "Zo werkt je proefperiode" with three dated steps and icons:

- **Vandaag:** ontgrendel alle eigenschappen
- **Dag 5:** ontvang een herinnering
- **Dag 7:** er wordt € 29,99 in rekening gebracht

That box is the single most copyable element in the app. It answers the only real
objection to a free trial, which is the fear of a silent charge, and it does it by
promising a reminder two days before. Feature rows below use small screenshots
rather than icons, and the CTA is `Probeer Plus gratis` with `Annuleren wanneer
je wilt` under it.

## 6. Two things a second pass through the frames found

**The action bar is sticky and horizontally scrollable.** On the full route page
the bottom carries `Begin` (green), `Downloaden`, `Opslaan`, and it stays there
while the page scrolls. Begin is always first and always the only coloured one.
So the primary verb is never something you scroll to find, on any screen, in any
state. That is a stronger version of the point above: it is not that Begin sits
under the elevation chart, it is that Begin is pinned to the bottom of the phone
everywhere the route exists.

**The progress screen does not hide its empty state.** Maand / Jaar / Alle
segmented control, a bar chart by month, then a grid of stat tiles: Afstand 0.2,
Hoogteverschil 8, Voltooid 1, Bewogen tijd 0. One bar on the whole chart and they
show it anyway, at full size, with the months labelled underneath.

That is worth copying and it is not obvious. Our collect screen will be empty for
every single user on the day it launches, and the instinct will be to hide the
chart until it has data. AllTrails shows the scaffolding first: the shape of what
you are about to fill in is itself the invitation. An empty grid of tree stamps
with the outlines drawn does more work than a message saying you have not
collected anything yet.

---

## What we take

1. **Begin as a one-word primary action, pinned to the bottom of the phone**
   wherever a walk exists, not a link inside a story. This is the fix for
   `directions` never having fired.
2. **The map inset on every card**, so a walk's shape is visible before opening.
3. **The floating map toggle**, one control, so list and map stop being two
   destinations.
4. **The four-stat row with labelled units**, both on web and in the app.
5. **Illustrated stamps for the collection**, not a grid of ticks, and drawn as
   empty outlines from day one rather than hidden until there is data.
6. **The trial timeline box**, close to verbatim, when the paywall ships.

## What we do not take

- **The elevation profile.** Our walks are flat city walks and a flat line says
  nothing, which is the same reason our season chart draws visibility rather
  than leaf cover.
- **Difficulty ratings.** Nothing here is difficult and pretending otherwise is
  the kind of borrowed convention that makes a product read as a clone.
- **Community and Volgend.** A social graph is a product we are not building
  and cannot moderate.
- **The interstitial, for now.** It is right for a product with 1M reviews to
  lean on; we have nine waitlist signups and the same modal would read as
  desperate. Revisit when there is proof to show.

## The open question the recordings do not answer

AllTrails knows what a user did because the phone recorded the track. We are
asking people to tick a tree they stood in front of, which is a deliberate act
rather than a passive one. Nothing in these recordings shows how to make that
tick feel earned rather than like homework, and that is the design problem our
collect verb actually has.
