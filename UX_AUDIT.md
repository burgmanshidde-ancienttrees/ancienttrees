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
