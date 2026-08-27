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

BURIED is the new one and it is the lesson: every other rule asks a question
about geometry, and a screen can pass all of them and still be unusable.

## 2. What only a person can check, and I cannot

These need a real account, a real camera, a real network and a real phone. None
of them can be automated here, and none of them may be skipped.

**Signed in, end to end**
- [ ] Magic-link sign-in arrives and works
- [ ] Save a tree, see it on My trees, see it on the website signed in as the same person
- [ ] Photograph a tree, see it in My trees
- [ ] Set a display name and a picture, see them on My trees
- [ ] Follow somebody, watch both counts move
- [ ] Send a tree and a piece of feedback, find both rows in Supabase
- [ ] **Delete the account and confirm everything is gone**: saves, visits, profile, avatar file, follows in both directions. This is the promise the whole account track was opened on, and Apple requires a working deletion path. **This one is now a command rather than a checklist item**: `SUPABASE_SERVICE_KEY=... python3 scripts/account_delete_test.py` makes a throwaway account, gives it one of everything, signs in as it, calls `delete_user()` the way the button does, and prints what is left. It needs the service key, which is Hidde's to hand over or to run himself.

**When things go wrong**
- [ ] No network at all: no crash, no blank screen that reads as broken
- [ ] Location denied, and then granted
- [ ] Camera denied
- [ ] A brand new install with nothing collected
- [ ] The largest accessibility text size
- [ ] Dark mode
- [ ] A real device, not the simulator, on cellular data

## 3. What Apple will ask for, and what we owe them

- [x] **Moderation, built 2026-08-27** (Hidde: "sociale deel gaat mee", then "maak gewoon die melden optie"). Guideline 1.2 asks for four things and the app now has all four: an ellipsis on every person opening **report** (four reasons, one tap) and **block**; a **Blocked people** list in Settings with an Unblock beside each name; `info@ancienttrees.app` published on the privacy page and in Settings; and the terms line on the sign-in sheet. Blocks are server-side so they survive a reinstall, and a trigger breaks the follow both ways. Schema: `supabase/reports.sql`.
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
| Precise or Coarse Location | **No** | | | read on the phone, never sent |
| Photos of trees | **No** | | | they stay in the app's own storage |

Two answers that are easy to get wrong and both matter: **Tracking is No
everywhere**, because nothing here is shared with a data broker or joined to
another company's data, and **Crash and Performance data are NOT linked**,
because those rows carry no account id by design.

### The SQL Hidde has to run, in this order

Each is idempotent and each is his, the same as `saves.sql` was:

1. `supabase/reports.sql` - reporting and blocking. Until it runs, blocking works on the phone only and reports fail quietly.
2. `supabase/diagnostics.sql` - where crashes land.
3. `supabase/delete-user.sql` - **replaces** the existing `delete_user()`. It adds one thing the old one could not do: deleting the avatar image out of the bucket. Storage does not cascade off `auth.users`, so today a deleted account's picture stays public at its old address.

### Still open

- [ ] Support URL, marketing URL, privacy policy URL
- [ ] Screenshots at the required sizes
- [ ] Age rating
- [ ] Nothing in the build that promises what it cannot do (Plus is hidden, sponsoring is hidden until the IAP exists)

## The two open product calls, which are his

- Whether following shows a follower anything. Today it counts and nothing else.
- Whether the camera stays behind a sign-in wall for a signed-out person.
