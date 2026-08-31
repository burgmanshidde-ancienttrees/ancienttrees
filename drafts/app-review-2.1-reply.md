# Reply to App Review, Guideline 2.1 (Information Needed)

Submission ID 4c352acc-6f59-4502-bbea-7f349ebf2c35, Ancient Trees 1.0, rejected
2026-08-30. Apple asked for seven things. Six of them are text and are written
out below, ready to paste. The seventh, the screen recording, is yours to make
because it has to come off a physical iPhone.

Nothing here needs a new build. This is a metadata reply: make the recording,
paste the text, send the message from the App Review page. Per Apple's own
mail, an app does not have to be resubmitted for this.

---

## What only you can do

1. **Record the screen on your own iPhone**, latest iOS, following the shot
   list below. Apple rejects recordings made on a simulator.
2. **Fill in the device list** in point 2 of the reply. I know what the
   automated sweep covers, I do not know which physical phones you have held
   this build on.
3. **Upload the recording and send the message.** Both are yours: the account
   is in your name and I do not write as you.

---

## The screen recording, shot by shot

Apple named four things that must appear if the app has them. Ancient Trees has
three of the four and no purchase flow at all, so the recording is short. Aim
for three to four minutes, unhurried, no narration needed.

1. **Launch from the home screen.** Show the icon being tapped, so the recording
   begins where they asked it to begin.
2. **The location prompt.** Let it appear and tap Allow. This is one of the
   sensitive-data prompts they asked to see.
3. **The map doing its job.** Let it settle on the trees near you, pan once,
   tap a pin, and let the tree page open.
4. **A tree page, scrolled top to bottom.** The story, the age, the honesty note
   about the pin if that tree has one.
5. **Take me there.** Tap it and let the maps app open, then come back.
6. **Adding a tree of your own.** Tap the camera, let the camera or photo
   library prompt appear, allow it, take or pick a picture, and let it land in
   My trees. That covers the other two sensitive-data prompts and shows
   user-generated content being created.
7. **Sign in.** Use Sign in with Apple, all the way through to being signed in.
8. **Reporting and blocking.** Go to Find People, open the three dots beside a
   person, show the report reasons, send one, then block and show that they are
   hidden. Apple checks these two by tapping and this is the single most likely
   cause of a second rejection if it is not on the tape.
9. **Account deletion.** Settings, Delete account, confirm, and show that you
   land back signed out. Then sign in again if you want the recording to end
   somewhere tidy.

There is no purchase or subscription flow to record. Plus, walks, season alerts
and the sponsor row are all behind launch flags and are not in the shipped
build, which is why point 5 of the reply says so plainly.

---

## The reply, ready to paste

Paste this into the message on the App Review page, and into the App Review
Information Notes field as well, which is what Apple asked for at the end of
their mail. Replace the one bracketed line in point 2.

```
Thank you for the review. The requested information follows, and a screen recording made on a physical iPhone running the latest iOS is attached to this message.

1. SCREEN RECORDING
Attached. It begins with the app being launched from the home screen and shows the typical flow: the location prompt, the map of nearby trees, a tree page, walking directions, photographing a tree into a personal collection with the camera and photo library prompts, signing in with Apple, reporting and blocking a person, and deleting the account. There is no purchase or subscription flow in this version, so none appears.

2. DEVICES AND OPERATING SYSTEMS TESTED
[FILL IN: for example, iPhone 15 Pro on iOS 18.6 and iPhone SE (3rd generation) on iOS 18.6]
The app is iPhone only, portrait only, and requires iOS 18.0 or later. Every screen is also built and measured automatically on two simulated screen sizes, the 4.7 inch iPhone SE and a 6.9 inch iPhone, on every change, to catch clipped or undersized elements.

3. WHAT THE APP DOES, AND FOR WHOM
Ancient Trees is a map of remarkable old trees in the world's cities. It shows you the ones near you, tells you what each one is, roughly how old it is and why it is worth walking to, and gives you directions to the trunk. You can photograph the trees you have stood in front of and keep them as your own collection.

The problem it solves: these trees are almost entirely undocumented in any form a person can use outdoors. Official registers exist in many countries but are published as spreadsheets and map viewers meant for civil servants, and the enthusiast websites that do cover them are not usable on a phone in a park. Somebody standing in a city has no way to find out that the yew across the road is nine hundred years old.

The audience is people who like being outdoors and like trees: walkers, gardeners, families looking for an afternoon out, and visitors who want something in a city beyond the usual sights. It is a general audience app with no age-restricted content.

4. SETTING UP AND ACCESSING THE MAIN FEATURES
No login is needed for the core of the app. The map, every tree, every story and the walking directions all work fully signed out. Simply open the app and allow location, or search for a city by name if you would rather not.

No demo account is needed either, because the app signs in with Apple or with Google, so you can use your own Apple ID. An account is required only for two things: keeping a collection of trees across devices, and sending us a correction about a tree.

The main features and where to find them:
- Nearby trees: the map on the first tab, which opens on your location.
- Any city: the search field on the map, by place, species or tree name.
- A tree: tap any pin, then Take me there for walking directions.
- Your own collection: the camera button, which photographs a tree and files it under My trees.
- Finding and following people: the person icon beside your name in My trees.
- Reporting and blocking: the three dots beside any person in that list.
- Account deletion: Settings, then Delete account.

5. EXTERNAL SERVICES USED
- Supabase, for account sign-in, the database behind collections, follows, reports and blocks, and private storage of the photographs a person takes.
- Sign in with Apple, and Google Sign-In through ASWebAuthenticationSession. No third-party sign-in SDK is embedded; the system sheet is used, so the app never sees a password.
- PostHog, on their EU cloud, for anonymous product analytics. One event per action, carrying an app version, a major OS version and a random identifier generated on the device. No email address, no account identifier, no coordinates and no advertising identifier are sent, and no profile is built. The app contains no advertising SDK, does not use the advertising identifier, and does not track users, so no App Tracking Transparency prompt is presented.
- OpenFreeMap, for map tiles, drawn with MapLibre. Attribution is shown on every map.
- ancienttrees.app, our own website, which serves the tree content the app displays as JSON files.
- Wikimedia Commons, iNaturalist and Flickr, which host some of the openly licensed photographs the app displays. The licence and the photographer are recorded for every one, and the credit is displayed as a caption under the photograph wherever the licence obliges one.
- Apple Maps and Google Maps, opened externally for walking directions. Neither is embedded.
- MetricKit, Apple's own framework, for crash and hang reports. No third-party crash SDK is used.

No artificial intelligence service is called by the app at runtime, and the app generates no content on the device. All tree content is researched, sourced and published ahead of time on our website, from official government tree registers and other cited sources, and each entry is checked against at least two independent sources before it appears.

6. REGIONAL DIFFERENCES
There are none. The app ships one English interface and the same content everywhere, and every feature behaves identically in every region. The map covers cities across Europe, North America, Asia and Australia, and which trees you see depends only on where you are looking, never on where your account is registered. Nothing is region-locked, and there is no regional pricing because there is nothing to buy.

7. REGULATED INDUSTRY AND THIRD-PARTY MATERIAL
The app operates in no regulated industry. It gives no medical, financial, legal or safety advice, sells nothing and handles no payments.

On third-party material, all of it is used under licences that permit the use, and every licence that obliges a credit is credited in the app:
- Photographs are only ever used under a verified open licence, meaning CC0, CC BY or CC BY-SA, or the Unsplash licence. The licence and the photographer are recorded for each one, and where the licence requires attribution, as CC BY and CC BY-SA do, the credit appears as a caption under the photograph. No photograph is used from any source without an explicit open licence.
- Tree data comes from official government and municipal registers of protected or monumental trees, published as open data under licences permitting reuse, together with our own research from cited public sources. Where a register asks for attribution we give it.
- Map tiles come from OpenFreeMap, built on OpenStreetMap data, credited on every map as their terms require.
- Photographs taken by the people using the app remain theirs and are stored privately in their own account. They are shown to nobody else.

ADDITIONAL NOTES ON THE TWO POINTS THIS APP PREDICTABLY RAISES

User-generated content: people may set a display name and a profile picture visible to others who search for somebody to follow, and may photograph trees. Reporting and blocking are on the three dots beside any person in Find People. A blocked person is hidden everywhere except in your own search for them, where they appear last with an Unblock button, so a block can always be lifted. Reports reach us and we act on them. Our terms state that there is no tolerance for offensive or impersonating content: https://ancienttrees.app/terms . We can be reached at info@ancienttrees.app, which is published in the app and on our privacy page.

Purchases: there are none in this version. The app contains no in-app purchase, no subscription and no request for money of any kind, and nothing in the app or the listing offers or promises paid content.

Location is used only to centre the map on the trees nearest you. A position is transmitted only when somebody records a tree of their own, saved with that record.

Account deletion is in Settings and removes the email address, the collection, the photographs, the display name, the profile picture, every follow and the account itself.
```

---

## Two things to check before you send

**The recording must show report and block being tapped.** Of everything on the
list this is the one Apple verifies by hand on a social app, and a recording
that skips it invites a 1.2 rejection to follow the 2.1 one.

**Check that the listing promises nothing the build hides.** Plus, walks, season
alerts and the sponsor row are all off in 1.0, and point 5 of this reply tells
Apple in writing that there is nothing to buy. If any screenshot or description
line in App Store Connect still mentions walks, season alerts or offline, it now
contradicts the reply, and a contradiction between the notes and the listing is
its own rejection. The listing text in APP_STORE_LISTING.md is clean on this
point; what I cannot see is what is actually saved in App Store Connect.
