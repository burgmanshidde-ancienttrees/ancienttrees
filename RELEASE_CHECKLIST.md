# Going live: what has to be true before the App Store

Written 2026-08-27 on Hidde's ask ("denk na over wat je allemaal zou testen voor
je live gaat, echt echt live, en test dat allemaal"), after a sheet that opened
too low reached his telephone through a green gate. The gate was not lying: it
measures geometry, and nothing in it asked whether a person can reach the thing
on the screen. That gap is the reason this file exists.

Three columns of work, and only one of them is mine.

## 1. What a machine can check, and now does

| Check | What it catches | State |
|---|---|---|
| `appsweep.py` both phones | a screen nobody has looked at | runs |
| `appfit.py` CLIPPED | anything off the edge | runs |
| `appfit.py` SMALL | a control under Apple's 44 points | runs |
| `appfit.py` DRIFT | margins out of step | runs |
| `appfit.py` BURIED | **a control under the floating bar** | added 2026-08-27 |
| 16 UI tests | the flows that can run without a person | runs in CI |
| `copycheck.py` | forbidden phrasing, forever-promises, hardcoded counts | runs |
| `appsweep --check-lists` | a screen the layout gate cannot see | runs |
| `appdata.py` | the bundled catalogue drifting behind the site | run before every release |
| the recentre test | a map with no way back to your own location | added 2026-08-29 |

BURIED is the new one and it is the lesson: every other rule asks a question
about geometry, and a screen can pass all of them and still be unusable.

## 2. What only a person can check, and I cannot

These need a real account, a real camera, a real network and a real phone. None
of them can be automated here, and none of them may be skipped.

**Signed in, end to end**
- [ ] Magic-link sign-in arrives and works
- [ ] Save a tree, see it on My trees, see it on the website signed in as the same person
- [ ] Photograph a tree, see it in My trees
- [x] Set a display name and a picture, see them on My trees (Hidde, 2026-08-30)
- [ ] Follow somebody, watch both counts move
- [ ] Send a tree and a piece of feedback, find both rows in Supabase
- [x] **Delete the account and confirm everything is gone** (2026-08-27, proven; see below): saves, visits, profile, avatar file, follows in both directions. This is the promise the whole account track was opened on, and Apple requires a working deletion path. **This one is now a command rather than a checklist item**: `SUPABASE_SERVICE_KEY=... python3 scripts/account_delete_test.py` makes a throwaway account, gives it one of everything, signs in as it, calls `delete_user()` the way the button does, and prints what is left. It needs the service key, which is Hidde's to hand over or to run himself.

**When things go wrong**
- [ ] No network at all: no crash, no blank screen that reads as broken
- [ ] Location denied, and then granted
- [ ] Camera denied
- [ ] A brand new install with nothing collected
- [ ] The largest accessibility text size
- [ ] Dark mode
- [ ] A real device, not the simulator, on cellular data

## 3. What Apple will ask for, and what we owe them

- [x] **Moderation, built 2026-08-27** (Hidde: "sociale deel gaat mee", then "maak gewoon die melden optie"). Guideline 1.2 asks for four things and the app now has all four: an ellipsis on every person opening **report** (four reasons, one tap) and **block**; an Unblock on a blocked person wherever you search for them, so a block is never permanent (the separate Blocked people screen was removed on Hidde's ask the same day: "dat heb ik nog nooit als optie gezien in een app"); `info@ancienttrees.app` published on the privacy page and in Settings; and the terms line on the sign-in sheet. Blocks are server-side so they survive a reinstall, and a trigger breaks the follow both ways. Schema: `supabase/reports.sql`.
- [x] **Crash reporting, built 2026-08-27** (Hidde: "crash reporting zullen we daar eens mee beginnen dan"). MetricKit, so no SDK, no third party and no bill: crashes and hangs arrive once a day on the next launch, from real devices only, carrying nothing that says whose phone it was. Schema: `supabase/diagnostics.sql`. It cannot be tested here at all, only on a device through TestFlight.
- [x] **The privacy manifest matches the app again** (`PrivacyInfo.xcprivacy`, rewritten 2026-08-27). It had not moved since accounts were an email address and nothing else.

### The App Store Connect answers, to be typed in once

App Privacy in App Store Connect is a separate form from the manifest above and
nobody can fill it in but Hidde. These are the answers, and they are the same
facts the manifest states, so the two cannot drift:

| Data type | Collected | Linked to them | Used for tracking | Purpose |
|---|---|---|---|---|
| Email address | Yes | Yes | No | App Functionality |
| Name (the display name they choose) | Yes | Yes | No | App Functionality |
| Photos (the profile picture only) | Yes | Yes | No | App Functionality |
| User ID | Yes | Yes | No | App Functionality |
| Other User Content (saves, visits, follows, submissions, reports) | Yes | Yes | No | App Functionality |
| Crash Data | Yes | **No** | No | App Functionality |
| Performance Data | Yes | **No** | No | App Functionality |
| Precise Location | Yes | Yes | No | App Functionality |

**The last two rows of this table were wrong until 2026-08-28 and are the
reason to distrust a table that nobody re-reads.** They said location is never
sent and that photographs of trees stay on the phone, which stopped being true
on 08-27 when SightingSync landed: the photograph goes to the sightings bucket
and the row carries user_id, lat and lng. The same stale sentence was sitting in
`PrivacyInfo.xcprivacy` and in `Sightings.swift`, in three places at once, and
this is a form Hidde types answers FROM. He corrected App Store Connect on
08-28; all four now agree.

What the two live rows actually cover. **Photos** is both the profile picture
and a photograph of a tree you recorded, and neither is shown to anybody else:
the sightings bucket is private and no policy anywhere lets one account read
another's. **Precise Location** is the coordinate saved WITH a tree you record,
not a stream: one per tree, at the moment you record it, and only once you have
signed in. The map's own reading of where you are, which opens it on the trees
near you, is still never sent and is still not declared.

Two answers that are easy to get wrong and both matter: **Tracking is No
everywhere**, because nothing here is shared with a data broker or joined to
another company's data, and **Crash and Performance data are NOT linked**,
because those rows carry no account id by design.

### The SQL Hidde has to run, in this order

Each is idempotent and each is his, the same as `saves.sql` was:

1. `supabase/reports.sql` - reporting and blocking. Until it runs, blocking works on the phone only and reports fail quietly.
2. `supabase/diagnostics.sql` - where crashes land.
3. `supabase/avatars-policy.sql` - lets somebody delete and replace their own profile picture. Without it the Storage API refuses the app's delete, and a deleted account's picture stays public at its old address. Found by running the deletion test, 2026-08-27.
4. `supabase/delete-user.sql` - **replaces** the existing `delete_user()`. The first version of it tried to delete the avatar from SQL, which Supabase refuses, so the whole function rolled back and NOTHING was deleted. The app deletes the picture through the Storage API instead, in the moment before this is called.

**All four are run, and the deletion test passes on every row (2026-08-27).** A throwaway account was made, given a save, a visit, a profile, an avatar image, a follow, a block and a report, signed in as itself, and deleted the way the button does. What is left: nothing. Saves, visits, profile, follows, blocks, reports, the avatar file and the account row are all gone. Re-run it with `SUPABASE_SERVICE_KEY=... python3 scripts/account_delete_test.py` after any change to what an account owns; a new table without a cascade would show up here as the only row that stays.

### Still open

- [x] Support URL, marketing URL, privacy policy URL - `/support` was written 2026-08-27 and is linked from the footer; privacy and terms already existed.
- [x] Screenshots at the required sizes - `python3 scripts/appstore_shots.py` writes five at 1320x2868 into `out/appstore/` and refuses to finish if any is the wrong size.
- [x] Age rating - the answers are in APP_STORE_LISTING.md; the two that need thought are User-Generated Content (yes, mild) and Unrestricted Web Access (no).
- [x] Nothing in the build that promises what it cannot do - a UI test asserts no screen in the app says "Plus", and it was proven to fail when Plus is on.
- [x] The app icon - it carried an alpha channel, which refuses the upload outright. Flattened, and `scripts/icon_check.py` runs on every push.
- [x] Export compliance - `ITSAppUsesNonExemptEncryption` is declared NO, so no upload asks again.
- [x] **1.0 asks for no money anywhere, decided 2026-08-29.** The sponsor row in
  Settings is behind `Launch.sponsor` and hidden, beside Plus and the walks.
  Hidde: "haal er maar uit tenzij we naar de website mogen verwijzen om het daar
  te doen." We may not, in the form worth having: 3.1.1 anti-steering does not
  let an app send somebody out to pay or to tip, the clean exception is a
  registered nonprofit, and the US injunction and the DMA routes both need an
  entitlement a first submission should not carry. Nothing is deleted:
  SponsorSheet, Tips and Tips.storekit stay in the build and `-sponsor` still
  opens the sheet, so the sweep and the layout gate keep seeing it.
- [x] **The DSA trader question, answered by the same decision.** Accepting the
  Paid Applications agreement asks whether you are a trader, and a trader's
  address, phone and email are published on the App Store product page and
  verified by Apple. With no in-app purchase in 1.0, non-trader is the honest
  answer and no address is published. Changing it later starts a new
  verification, so it is a decision rather than a checkbox: taking money in the
  EU means trader, and the address has to be chosen before that day, not on it.
  The website keeps /sponsor and its Ko-fi page, where none of this applies and
  nobody takes a cut, and that is also where we can find out whether anybody
  ever pays.
- [ ] **The App Store Connect record itself**, which only Hidde can create: the listing text, the screenshots and the privacy form are all written out in APP_STORE_LISTING.md, including the TestFlight fields.
- [x] **WAS A BLOCKER, server side fixed the same evening: Sign in with Apple is switched on.** Hidde enabled the provider with the bundle id under Client IDs at once. Confirmed from outside on the route the app actually uses, `/auth/v1/token?grant_type=id_token`, which now answers "Unable to detect issuer in ID token for Apple provider" (a token error, so the provider is accepted) where a disabled provider answers "provider is not enabled". The web route still answers 400 and that is correct and permanent: it needs the OAuth secret we deliberately left empty, and the website has no Apple button. **Proven on a device the same evening** (Hidde: "het werkt"), so the whole path is exercised, not just the server's half. The original finding follows.

- [ ] ~~BLOCKER~~ (resolved above). Found
  2026-08-30 on Hidde's own device: the app reports "Apple sign-in is not
  switched on yet", which is our own honest message for a provider that refuses.
  Our side is correct and was checked, so this is one dashboard setting:
  `codesign -d --entitlements` on the uploaded archive shows
  `com.apple.developer.applesignin`, and Supabase answers 400 on
  `/auth/v1/authorize?provider=apple` while Google answers 302.

  **It is a rejection under guideline 4.8, not merely a broken door.** An app
  offering third-party sign-in (Google works, confirmed the same evening) must
  offer an equivalent privacy-preserving option, and Sign in with Apple is it.
  Shipping the button in a state where it fails is worse than not offering
  Google at all. It also matters more since 2026-08-30 than it would have that
  morning, because the typed email route left the app the same day, so Apple and
  Google are the only two doors.

  The fix is Authentication > Providers > Apple, enabled, with the bundle id
  `app.ancienttrees.AncientTrees` under Client IDs, which is what the app's
  native id-token route uses. A Services ID and .p8 are for the web flow, and
  the website has no Apple button.

  **Test it on a TestFlight or archive build, never on a Debug run.**
  CODE_SIGN_ENTITLEMENTS sits on the Release configuration only, so a Debug
  build from Xcode carries no Apple sign-in entitlement and cannot work however
  well Supabase is configured.

- [x] **Google sign-in on a real phone** (Hidde, 2026-08-30: "google werkt"), so
  `ancienttrees://auth-callback` is on Supabase's redirect list after all.

- [ ] **Google sign-in on a real phone.** `ancienttrees://auth-callback` has to be
  in Supabase's redirect allow-list or Supabase quietly redirects to the website
  instead, which looks like a button that does nothing. Apple's and the magic
  link are unaffected. It cannot be seen in the simulator or in CI.
- [ ] **Everything in part 2 above**, which needs a real phone and cannot be done here.

### Getting a build into TestFlight, which nothing here does for you

Written 2026-08-28, when Hidde looked for the app in TestFlight and found
nothing. Nothing was wrong: **no build has ever been uploaded.** `ios.yml`
builds, tests and photographs the app and it does not archive or distribute,
which is deliberate (uploading needs his signing identity) and easy to mistake
for a pipeline that ships. Signing is automatic on team `5EWWC3M8L2`, bundle
`app.ancienttrees.AncientTrees`.

In Xcode, and it is five steps:

1. Pick **Any iOS Device (arm64)** as the destination. Archive is greyed out while a simulator is selected, which is the step people get stuck on.
2. **Product > Archive.**
3. In the Organizer that opens: **Distribute App > TestFlight Internal Only**, then Upload. (App Store Connect > Upload does the same and also allows external testers later.)
4. Wait. Processing takes five to twenty minutes and the build shows as unavailable until it finishes.
5. In App Store Connect, **TestFlight > Internal Testing**, add yourself to the group with the Apple ID your TestFlight app is signed in with. A build nobody is a tester of never appears on a phone, and this is the second place people get stuck.

**Every later upload needs a HIGHER build number** than the one before it, or
App Store Connect refuses it. That is `CURRENT_PROJECT_VERSION` in the project
file; `MARKETING_VERSION` is the 1.0 a person sees and only changes when you
want it to.

## The two open product calls, which are his

- Whether following shows a follower anything. Today it counts and nothing else.
- ~~Whether the camera stays behind a sign-in wall for a signed-out person.~~
  **Answered 2026-08-30: it stays.** Hidde: "een boom moet onder een account
  vallen dus ja", said while ruling that saving must not work signed out either.
  Nothing had to be built: every real route into the collect sheet already goes
  through `openCollect()`, which requires an account. The launch-argument routes
  stay open on purpose so the sweep can photograph those screens on a simulator
  that has never signed in.
