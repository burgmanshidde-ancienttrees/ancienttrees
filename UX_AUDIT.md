# UX audit: the website and the iOS app

Written 2026-08-20, on Hidde's brief: look at both products the way somebody who
has just moved here from AllTrails would, with one question in front of all the
others, which is how we get more people to make an account.

Everything below was found by LOOKING. The app was built, installed and driven in
the simulator; the site was walked at 375px in a browser. Nothing here is read
off the source alone, because the three worst things in this list are all
invisible in the source and obvious on a screen.

The verdict in one line: **the app was well built and could not be signed into at
all, and the thing standing in front of the account problem was not the account
flow but the fact that the map did not know where anybody was.**

---

## The one that outranks the account question

| | |
|---|---|
| **What** | `NSLocationWhenInUseUsageDescription` was missing from the app's Info.plist |
| **So** | iOS silently refuses to show the permission dialog when that key is absent. `requestWhenInUseAuthorization()` returned without asking anybody anything, `location.coordinate` stayed nil forever, and the app fell through to its hardcoded fallback |
| **Which means** | Every user of the app, anywhere in the world, opened it on Dam square in Amsterdam |
| **Proof** | The dialog had never once appeared in the simulator. After the fix it appears on first launch, screenshotted |
| **Status** | Fixed |

This ranks above the account work and it is worth saying why rather than just
fixing it. The funnel is: know where you are, see a tree worth walking to, walk
to it, tick it off, and only then does an account mean anything. The first step
was broken, so for anybody outside Amsterdam every step after it was too. No
sign-in screen, however good, converts a person who was shown the wrong city.

---

## iOS app

| # | Finding | Severity | Status |
|---|---|---|---|
| 1 | Location permission never requested, everyone falls back to Amsterdam (above) | Blocker | Fixed |
| 2 | **No account exists.** The You tab's first row was the text "Signed in ... not yet", not tappable. There was no sign-in surface anywhere in the app | Blocker | Fixed |
| 3 | **The paywall's waitlist button had never written a row.** It posted a `note` column that does not exist on the table, so PostgREST rejected every insert with a 400, while the screen said "We will tell you the day it opens" | Blocker | Fixed |
| 4 | That same button set its success state without reading the result, so a failure looked identical to a success | High | Fixed |
| 5 | Three `.sheet` modifiers stacked on one view. SwiftUI honours one, so the others silently never presented | High | Fixed |
| 6 | Map sheet's peek height (160pt) was shorter than the floating tab bar, so the first tree card was always sliced in half | Medium | Fixed |
| 7 | Saved tab content ran under the floating tab bar with no bottom inset | Medium | Fixed |
| 8 | Tree count rendered with the device's locale grouping, so English copy on a Dutch phone read "1.406 trees" | Low | Fixed |
| 9 | The You tab was a settings list whose top half was four zeros and whose account row was a dead label | High | Fixed |
| 10 | **Explore is a table of contents.** "At their best in August" is the best idea in the product and it renders as plain text rows with no photograph anywhere on the screen | High | Fixed |
| 11 | Locked walks show a bare padlock in a plain list with no word of explanation | Medium | Fixed |
| 12 | The map has no recentre-on-me control | Medium | Fixed |
| 13 | "Near you" floats over the map as a bare title with no bar behind it, and "Near Amsterdam" stated a problem with no way to fix it | Medium | Fixed |
| 14 | The website's homepage advertises a collection screen with species stamps that the app does not have | Medium | Open |
| 22 | The location permission was never primed. iOS gives one shot, and a refusal cannot be taken back | High | Fixed |
| 23 | The map has no filters | Low | Open |
| 24 | **The season shelf shows leafless trees.** Now that "At their best in August" renders photographs, the first card is a bare wingnut in a car park. The layout is right and the photograph contradicts the header | Medium | Open, for a photo pass |

### What was built for the account, and why in that order

Hidde ruled two things this morning: Apple sign-in is allowed, and the wall is
soft. Both are in.

| Piece | What it does | Why this shape |
|---|---|---|
| Sign in with Apple | One Face ID tap, no typing, never leaves the app | On a phone, typing an address, switching to Mail and finding the way back is four chances to give up. This is the single biggest lever on iOS and everything else in this table is smaller |
| An emailed six digit code | Type it back into the app | Not a magic link. A link means leaving the app, which is exactly the drop the website already has |
| Union merge on sign-in | Six ticked here plus four on the website equals ten | A collection that eats entries is worse than no collection, so deletes are never inferred from what is missing on one side |
| Keychain, not UserDefaults | Where the tokens live | A list of tree ids in a plist is fine; a credential in a plist lands in an unencrypted backup |
| Refresh on every launch | Keeps the hour-long token alive | The website shipped without this and saves silently stopped reaching accounts for three weeks |
| The prompt, twice at most | First tick, third save. Three times ever, never twice in a week | A tick is a memory, not a bookmark, and it is the moment something becomes worth keeping. A prompt that keeps returning teaches people to dismiss without reading |
| A card on You, a line on Saved | Always there, never interrupts | These will do most of the work. A prompt has to be well timed; these only have to be true |

The copy rule throughout is AllTrails' paywall rule moved to a sign-in: **name
what the person was doing, never the plan.** So the sheet says "That one is
yours" over "The Last Elm of Stationsplein is ticked off", and never "Create an
account".

---

## Website

| # | Finding | Severity | Status |
|---|---|---|---|
| 15 | The sign-in dialog offered three calls to action, and the middle one, "More options", linked to /account, which carries the same single email form and nothing else | High | Fixed |
| 16 | The dialog never named the tree that had just been saved, although a save is the only reason it opens | Medium | Fixed |
| 17 | On /account at 375px the email field shrank next to its long button until the placeholder read "you@exampl", on the page whose entire job is getting an address typed into it | High | Fixed |
| 18 | The only web route in is a magic link, so on a phone signing in means leaving the browser for Mail | High | Open, needs a template line |
| 19 | **"Explore trees near you" is an underlined text link.** The core action of the whole product, and it is the weakest affordance on the homepage, sitting under a search field that is styled as the primary | High | Fixed |
| 20 | The tree page's action bar carries three peers, with Save coloured and "Take me there" plain. AllTrails colours exactly one, and it is always the go-there verb | Medium | Open, wants data first |
| 21 | `public.visited` does not exist in the database. visited.sql was written on 2026-08-18 and never run, so the tick log has no cloud half on either platform | High | Needs Hidde |

On 19, now done: it is a filled pill with a pin on it reading "Trees near you",
which is also shorter and says the thing rather than describing the page it
opens. The search field is untouched and now reads as the second option, which
is what it is: the product's own north star sentence is "I open it, it knows
where I am, it shows me a cool tree nearby", and search is the fallback for when
that is not what you want.

On 20, and this is the reason it is not done: colouring Save is arguably right
for the account goal, and colouring "Take me there" is right for goal 1 and for
the `directions` button that has never fired. That is a real trade and it should
be settled by what the bar is actually earning, not by taste. The click data
lives in a place a session can read and I did not have it open. It is a fifteen
minute decision once the numbers are on the table.

---

## The convention walk, 2026-08-20 (later)

Hidde, having run the app on his own phone: "kun je uberhaupt de app doorlopen
en kijken of er interactie conventie worden overgeslagen". A grep found most of
it and needed no opinion: `sensoryFeedback` 0, `ShareLink` 0,
`accessibilityLabel` 0, `refreshable` 0, `searchable` 0,
`scrollDismissesKeyboard` 0.

| # | Convention | Severity | Status |
|---|---|---|---|
| 25 | **The app could never update its own data.** Sync.swift was written and nothing called it; CatalogueStore only read the bundled copy. A tree added by a night run could not reach a phone without App Store review | Blocker | Fixed |
| 26 | The list did not follow the map. Pan to Paris and it still described where you were standing | High | Fixed |
| 27 | Explore listed 30 of 119 places, and 89 cities were unreachable from that screen | High | Fixed |
| 28 | No haptic feedback anywhere, including on the tick, which is the product's own verb | High | Fixed |
| 29 | No way to share a tree, on a project whose recorded binding constraint is distribution | High | Fixed |
| 30 | Every icon-only button read to VoiceOver as "button" | High | Fixed |
| 31 | Dragging the sheet up scrolled the list instead of raising the sheet | High | Fixed |
| 32 | Tapping the active tab did nothing. Four trees deep, the only way out was four taps on Back | Medium | Fixed |
| 33 | No pull to refresh, no search on Saved, no way to remove a saved tree except the heart | Medium | Fixed |
| 34 | The keyboard sat over the search results | Medium | Fixed |
| 35 | The card's photograph sat at a fixed 190pt and names clipped at two lines under large Dynamic Type | Low | Fixed |

Two things about how these were verified, because it is the interesting part.

**The catalogue refresh was proved rather than asserted.** A fresh install showed
1,406 trees in 38 countries; after a refresh and a full restart it showed 1,526
in 39. That also proves the downloaded copy persists and is preferred on launch.

**Two of them cannot be seen in a screenshot at all**, because they only happen
after a finger drags something, so they became UI tests instead: one pans the map
and asserts the chip stops saying "Near you", one opens a tree and taps the
active tab and asserts it lands back on the map. The suite is five tests and the
other three cover the way back from a tree, ticking, and the sign-in sheet
presenting.

**One change was tried and reverted the same hour:** `displayPriority` away from
`.required`, to let MapKit cull colliding pin labels. It made no visible
difference in Paris and it lets MapKit hide a PIN rather than only a label, which
on this map is the worse bug.

---

## What needs Hidde, and it is four dashboard actions

None of these are code. Three of them gate work that is already written and
sitting there.

| # | Where | What | Gates |
|---|---|---|---|
| A | Supabase, Authentication, Email templates, Magic Link | Add `{{ .Token }}` to the template so the mail carries a six digit code as well as a link | The app's email sign-in, AND finding 18 on the website, which is roughly an hour's work the moment this line exists |
| B | Supabase, Authentication, Providers, Apple | Enable it and add `app.ancienttrees.AncientTrees` to the allowed client IDs | Sign in with Apple, the biggest single lever in this whole audit. A probe today got past the provider check into token parsing, so this may already be half done. Worth confirming |
| C | Supabase, SQL editor | Paste and run `supabase/visited.sql` | The cloud half of the tick log, on the website as well as the app. Until then a tick survives as a save, so nothing is lost, but the date is not kept |
| D | Xcode, next time you build to your own phone | Accept the prompt to enable Sign in with Apple on the App ID | Device builds only. The simulator is unaffected |

Everything else in this audit either shipped today or is written down above as an
open item with its reasoning attached.

---

## What was deliberately not touched

- **The mobile header.** Everything sits behind one hamburger, which reads as
  poor account discovery, and it is Hidde's own ruling of 2026-08-19 ("gooi dan
  alles onder het hamburger menu"). Recorded, not overruled.
- **The price and anything that takes money.** Hard rule 2.
- **The tree action bar's colour hierarchy**, for the reason in 20 above.
- **The email code on the website (18).** It is written on the app side and the
  same one hour on the web, but shipping it before the template carries a token
  would put a code field in front of an email with no code in it. It waits on A.
- **Badges and stamps (14).** A day's work for the reward of a collection almost
  nobody has yet. It is on the list because the homepage already promises it,
  not because it is next.

Onboarding was on this list when the audit was written and is now done: the
location primer is finding 22 above.

---

# 2026-08-25: Hidde's own walk of the app

He installed it, added trees in Baarn on 08-24 and 08-25, and reported roughly
thirty things in one message. Every item is below with what it actually is,
because half of them are the same bug wearing different clothes and two of them
are not mine to build. Nothing here is guessed at: where a cause is named it was
read in the source, and where it was not, the row says so.

The four questions he asked, answered first because they are cheap.

**Why does the map open on Amsterdam when I am in Baarn.** `ContentView.swift:127`
falls through to Dam square (52.3731, 4.8922) whenever `location.coordinate` is
nil. The Info.plist key that was missing on 2026-08-20 is present now, so the
dialog does appear, but the fallback still fires in two real cases: the
permission was refused once and never asked again, and the cold start where the
first GPS fix has not landed by the time the map draws. Neither is fixed by
asking again. The fix is to remember the last coordinate we had and open there,
and to stop naming Amsterdam when we do not know.

**Can we estimate a tree's age from a photograph.** No, and not nearly. Age comes
from girth and a published growth rate for the species, which is how every
register in the world dates a tree, and a photograph does not carry girth: a
trunk fills the frame at two metres or at six depending on where somebody stood.
What a photograph does give is species, health and whether the crown is a
veteran's, which narrows nothing to a number. So the app should ask for the one
measurement a person standing at the tree can actually take, which is the girth,
either with a tape or by counting arm spans, and CLAUDE.md's estimate rule then
applies unchanged: derived, stated basis, century-wide band.

**Why do the trees I added not show up, and why do I only see one.** Because
adding a tree writes a row to Supabase's `submissions` table and nothing more.
The app's map reads `Data/trees.json`, which is built from `data/cities/*.json`
and only carries published trees, so a submitted tree is invisible until a run
verifies it and it ships in a build. The one he sees is `brn_005`, published on
2026-08-12 and already ours. That is the correct behaviour and the wrong
experience: a person who just added a tree should see their own pin, marked as
theirs and pending, and the copy he objected to is the same wound.

**What the approval process looks like.** Step 0b of CLAUDE.md: a run reads the
table, treats every claim as a lead, verifies existence, species and location
against two independent sources, writes the story and ships it, or records why
not. It is not a human queue and there is no delay dial to turn: it happens on
the next run that reaches rung 1, which outranks all new coverage.

## A. Broken, and mine to fix

| # | What he saw | What it is |
|---|---|---|
| A1 | Map list: one tap on a walk does nothing, the second opens the tree underneath | Hit testing. Two tappable layers in one row, the walk row's gesture losing to the card below it |
| A2 | Walking routes appear and disappear while scrolling the list in Den Haag | The walks section is being rebuilt from the visible map region rather than from the city, so scrolling the sheet moves the region and empties it |
| A3 | Cannot click "Want to see" in Collected | Reported twice, in two sessions. Whatever the cause, it is the second time it has been said |
| A4 | Cannot click "A tree I found", have to press hard | Hit area, and a card that redraws under the finger |
| A5 | Photos break out of the rounded corners, top left and top right | Missing clip on the image inside the card. Same bug on the collection screen and on Explore. His note stands: this is one I should catch myself, and it is now a check |
| A6 | Tapping a walk's "Take me there" gives a straight line | We hand the coordinate to the system without a walking route. The app should draw the real route |
| A7 | "0 ticked off. You walk the whole thing, 0 trees, they're all in your collection" | Two contradicting strings on one card, and the second is only true when the count is the count. Arithmetic, not copy |
| A8 | Tapping a species pin does not centre the map on it | The camera moves to the pin's coordinate without accounting for the sheet covering the lower half of the screen |
| A9 | Signed out and could still heart a tree | Saving is not gated. It must ask for sign-in, and say why |
| A10 | Un-hearting removes a collected tree instantly | Needs a confirmation, because the target sits under a thumb |

## B. Copy and flow

| # | What he saw | What happens |
|---|---|---|
| B1 | "This tree is yours. We have it too." | Replaced with his sentence: "You've added this tree. We're taking a look at it, and once it's verified, we will add it to our map." |
| B2 | "Report a problem" leads to a screen for adding a tree we are missing | The three submission kinds share one screen and it opens on the wrong one |
| B3 | Filter reads "See walking routes" and "Hide walking routes" | "Walking routes", one label, both states |
| B4 | The lock icon next to the label | Removed. The label carries it |
| B5 | Collected filter chip grows a cross the others do not have | Removed |
| B6 | Species list from Explore shows everything | Nine, photos first, then "Show more". Collected ones on top, and no "anything else" bucket in the middle |
| B7 | "Every three photographs join your collection" is a statement, not a door | Becomes a button into the photo flow |
| B8 | Profile credits map data to OpenStreetMap | See D3. This one I am not simply deleting |
| B9 | "I'm in front of it" offered without a photograph | It should go into the photo flow instead |

## C. Layout and colour

| # | What he saw | What happens |
|---|---|---|
| C1 | Horizontal spacing between walks on city screens is too wide, same on Explore | Tightened, measured against the 375pt width appfit already checks |
| C2 | The list sheet sits too high since the walks row arrived, cutting the tree off | Lowered so a card reads whole at rest |
| C3 | The ticket badge shares the Plus colour, so they read as one thing | Tickets go to a blue of their own. Plus keeps the accent |

## D. His to decide, or not mine to build

| # | Item | Why it stops here |
|---|---|---|
| D1 | Sponsor this project, 20 euro a year, in-app purchase | Hard rule 2. Payments, prices and anything that takes money are his alone. I can build the button, the copy and the screen it sits on, and I will not wire a purchase |
| D2 | MVP with Plus turned off: no "See what's included", a coming-soon line under Settings, walks behind an email capture | This is his instruction and I will build it. Flagging it only because it changes what the app promises, and the paywall line he set on 2026-08-18 is the thing being deferred |
| D3 | Remove the OpenStreetMap credit from Profile | Pushing back. The basemap is OpenFreeMap serving OpenStreetMap data, and the ODbL requires the credit. It can move somewhere quieter, inside a Legal row rather than on the Profile face. It cannot simply go |
| D4 | Offline maps listed under Plus alongside Season Alerts | Agreed, and it is copy only until offline exists |

## E. The website, and Search Console

| # | Item | State |
|---|---|---|
| E1 | The Get the App overlay converts worse than the old landing page. Revert the menu link to the page | His call and a reversible one. The overlay stays reachable from the city map CTA, the nav goes straight to /app |
| E2 | Seven 404s of the form `/berlin/app`, `/brisbane/app` | No such page and nothing in the source links there. Cheapest honest fix is to make them resolve to /app rather than 404 |
| E3 | `/auth/v1/token` and `/rest/v1/saves` crawled on our own host | Both are Supabase paths that only appear as absolute URLs in the current source, so this is either an older build or Googlebot resolving a fetch it saw. Worth twenty minutes, not more |
| E4 | `/feed.xml` and `/antwerp` crawled and not indexed | Normal at our size. Antwerp is a thin page, not a broken one |
| E5 | `/saved` and `/account` noindex, `www` redirecting, `/contribute?...` canonicalised | All three are working as intended and need nothing |
