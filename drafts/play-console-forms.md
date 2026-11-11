# Play Console forms, 2026-11-11

The answers for Policy > App content in the Play Console, derived from the
privacy page (site/src/pages/privacy.astro), data/privacy-map.json and what the
Android code actually sends, read on 2026-11-11:

- Supabase (android/.../account/Supa.kt and the files beside it): the account
  (email, the name Google gives), profile and avatar, saves, visited, sightings
  with their photograph and the place it was taken, tree notes, submissions,
  reports, blocks, follows, recent searches, Plus answers and waitlist.
- PostHog (account/Measure.kt): event name, app version, Android major version,
  build, a random install id, signed in yes/no and while signed in the account
  id. No email, no name, no coordinates, no advertising id. Silent on emulators.
- Location: used on the phone to show what is near; sent only as the place of
  a sighting the person records themselves.
- No crash reporter on Android (the iPhone's MetricKit has no Android twin yet),
  no ads SDK, no advertising id, no Firebase.

If any of this changes (a crash reporter, a new table), this file and the Data
safety form change with it, as the privacy page does (privacycheck.py).

## App access

Choose: **All or some functionality is restricted.** Instructions for the reviewer:

```
Browsing the map, tree pages and Discover needs no account. Saving a tree, collecting one with a photograph and the profile need an account: tap Sign in and continue with any Google account, or enter an email address and open the sign-in link sent to it.
```

No password to hand over: the app has no password sign-in. (The CI test
account, apptest@, signs in by a service key, which a reviewer cannot use.)

## Ads

**No, my app does not contain ads.**

## Content rating (IARC questionnaire)

- Email for the rating certificate: yours (the same as the developer account).
- Category: **All Other App Types** (not a game, not social or communication
  first, not reference/news as Play defines it).
- Violence: No. Fear: No. Sexuality: No. Gambling: No. Language: No.
  Controlled substances: No. Crude humour: No.
- Does the app allow users to interact or exchange content? **Yes.** Notes on
  trees, photographs and profile names are public, and people can follow each
  other. (Reporting and blocking exist: privacy page, "Reporting somebody".)
- Does the app share the user's current physical location with other users?
  **No.** A sighting's photograph goes on the tree's page without its location
  data; the tree's own pin is ours, not the person's position.
- Does the app allow users to purchase digital goods? **No.**
- Is the app a web browser or search engine? **No.**
- Expected result: PEGI 3 / Everyone, with the interactive element
  "Users Interact".

## Target audience and content

- Target age groups: **16 to 17** and **18 and over**. Not younger: the privacy
  page says Ancient Trees is for people aged 16 and over (UAVG art. 5).
- Could the app unintentionally appeal to children? **No.**
- Store presence: no "Designed for Families", no teacher approval.

## Data safety

Overview answers:

- Does your app collect or share any of the required user data types? **Yes.**
- Is all of the user data collected by your app encrypted in transit? **Yes**
  (HTTPS to Supabase and PostHog).
- Which of the following methods of account creation does your app support?
  **Username and other authentication**, plus **OAuth** (Google).
- Delete account URL: **https://ancienttrees.app/account** (the account page
  has the delete option, privacy page "Deleting"). Partial deletion without
  deleting the account: **Yes**, by a privacy request at
  https://ancienttrees.app/contribute?kind=privacy.
- Shared with third parties: **No** for every type below. Play counts a
  service provider that processes data for us (Supabase, PostHog) as not
  sharing, and a photograph a person publishes on a tree's page themselves is
  user-initiated, which Play also exempts.

Data types, each **collected, not shared**:

| Play data type | Why it is collected | Optional? | Where in the code |
|---|---|---|---|
| Location > Precise location | App functionality (the place of a sighting) | Optional | sightings |
| Personal info > Name | App functionality, Account management | Optional (from Google, or a tree name) | profiles |
| Personal info > Email address | Account management, App functionality | Optional (only with an account) | Supabase auth |
| Personal info > User IDs | Account management, Analytics | Optional | Supa.kt, Measure.kt |
| Photos and videos > Photos | App functionality | Optional | sightings, avatars |
| App activity > App interactions | Analytics, App functionality | Required while the app runs on a phone | Measure.kt; saves, visited, follows |
| App activity > In-app search history | App functionality | Optional (only with an account) | recent_searches |
| App activity > Other user-generated content | App functionality | Optional | tree_notes, submissions, reports, plus_answers |
| Device or other IDs | Analytics (the random install id) | Required | Measure.kt |

Not collected: financial info, health, messages, contacts, calendar, audio,
files and docs, web browsing, app info and performance (no crash logs on
Android yet), approximate location (the precise place of a sighting is the only
location sent).

Processed ephemerally: **No** for each (they are stored).

## Advertising ID

**No**, the app does not use an advertising ID. The merged manifest carries no
AD_ID permission (checked on the release build, see the LOG entry).

## Government apps, financial features, health, news, COVID-19

No, none of them.

## Closed test: 12 testers, 14 days

Google requires a new personal developer account to run a closed test with at
least 12 testers who stay opted in for 14 days in a row before production
access can be requested. The steps:

1. Testing > Closed testing > Create track (or use the default "Closed testing
   - Alpha").
2. Testers tab: **Email lists**, create a list (for example "Ancient Trees
   testers") and paste the addresses, one per line. They must be the Google
   account addresses the testers use on their Android phone.
3. Create a release on that track with the .aab from out/play/, roll it out.
4. The Testers tab then shows the **opt-in link** ("Join on the web"). Each
   tester opens it while signed in with that Google account, taps Become a
   tester, then installs from the Play Store link on the same page.
5. Count from the day the twelfth tester opted in; keep all twelve opted in
   for 14 days. Leaving the test or uninstalling early can reset the count, so
   ask for a few more than twelve (fifteen is safe).
6. After 14 days: Dashboard > Apply for production, answering Google's
   questions about the test (how testers were found, what feedback changed).
   Keep a note of what testers said during the two weeks for that form.

Who could be asked (groups only: the names and addresses stay in the private
store, never in this public file, and nobody has been contacted):

- Ambassadors with an Android phone (`python3 scripts/ambassador.py --requests`
  and data/ambassadors.json name who they are; their addresses come through
  `private_store.py pull`).
- Readers who replied by mail and said yes to staying in touch
  (data/outreach-sent.json, his inbox), and readers whose added tree went live.
- Friends and family with Android phones; Google allows it, and it is the
  fastest way to twelve.
- The one-week rest holds (mailer.py): a tester ask to somebody mailed in the
  last seven days waits.

A mail asking someone to test is a new kind of mail: Hidde writes or approves
its words before any goes (hard list 4, drafts only).
