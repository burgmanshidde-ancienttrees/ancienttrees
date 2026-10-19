# Take me there on day one: diagnosis (2026-10-19)

Diagnosis only. No code changed, nothing committed.

## What I could not do

The PostHog query could not run. `~/.ancienttrees-posthog.env` does not exist on this Mac, so `scripts/posthog.py` stops at "No PostHog key". That means no split by app version, no permission-prompt or sheet events between steps, and no per-phone paths. Everything below comes from the digest's own numbers (DATA.md), the digest query in `scripts/daily_digest.py` (line 3006 on), and the Swift and Astro source. To finish step 1, Hidde adds a Query: Read key to that file (PostHog EU, Settings, Personal API keys), then `python3 scripts/posthog.py --sql ...` can split by `app_version`.

## Funnel (new phones, first 24 hours, from DATA.md 2026-10-18)

| Step | This week | Week before |
|---|---|---|
| New phones | 14 | 12 |
| Opened a tree | 12 (86%) | 7 (58%) |
| Opened a tree near them (only phones on a version that sends `near`) | 2 of 4 | none yet |
| Answered the location prompt as allowed | 5 of 5 | none yet |
| Tapped Take me there (`directions` event) | 2 (14%) | 1 (8%) |
| Collected a tree | 1 (7%) | 1 (8%) |
| Back within a week | 2 of 12 (17%) | 5 of 9 (56%) |

The same row in earlier digests: Take me there was 36% and 38% for arrivals up to about 10-01 (DATA.md 10-09 to 10-11 entries, week-before column), then 8 to 17% for every cohort since. Downloads in the last 6 days were 14, 8 of them from App Store search, 6 in the US.

## The event is fine

- `Measure.event("directions")` fires once, inside `Directions.walk` (ios/AncientTrees/AncientTrees/Kit/Directions.swift:97), for all three call sites: the tree page bar, the map page toolbar and walk mode. It is unchanged in name and place across builds 20 to 35. The digest counts `event = 'directions'` per phone in the first 24 hours (daily_digest.py:3019). A renamed or missing event is ruled out for the app.
- It counts the tap, before the "which maps app" question is answered. A person who taps and then dismisses the question still counts.

## The button is not hidden, and the layout did not cause the drop

- App: Take me there is in the pinned bottom bar of the tree page (TreeDetail.swift:2293), so it is never below the fold on an SE. It has no sign-in or permission gate. With a location fix it reads "Take me there · 4.2 km", without one just "Take me there".
- It was the loud button in build 20 (1.0.2, the build nearly all of these phones have) and is again beyond 200 m in build 34 and 35. Only within 200 m does Collect take the big slot and Take me there become a circle (changed 10-09 and 10-10, commits 427896915 and 30faa76d6). The 10-09 swap shipped in 1.0.3 (build 34 or 35, in App Store review as of 10-16), so it cannot explain a drop that starts with arrivals around 10-02.
- Web: on a phone the loud button is "Open in the app" and Take me there is an unlabelled 52 point circle (TreeDetail.astro:352 to 354). Intended, but it means web visitors rarely tap it and the web `directions` event is not in this app funnel.

## Likely causes, ranked

1. **The new phones are mostly not near a tree, so there is nothing to walk to (strongest, circumstantial).** Of the phones on a version that reports distance, only 4 had a known distance and 2 were within 25 km. Downloads come from App Store search across the US, NL, DE, DK, GB and IE, and 12 of 14 phones open a tree, which looks like browsing. Someone browsing from a sofa does not tap directions. Take me there is a metric of being near a tree, and we divide by everybody.
2. **The audience changed in early October.** The old 36% cohort came from the first weeks of the listing. The 1.0.3 keywords and store-search arrivals (8 of 14) bring people who searched "old trees" out of curiosity. Retention fell from 56% to 17% in the same weeks, which fits a looser audience better than it fits a broken button. Evidence is thin: no per-source funnel exists.
3. **Dropout at the maps handoff (unproven).** On first tap the app asks Apple Maps or Google Maps before opening anything (DirectionsAsk). The `directions` event fires before that question, so this does not lower the count, but a dismissed question would lose the walk. Not measurable today.
4. **Small numbers.** See below.

## What 14 phones can and cannot show

Can: the event is wired the same way; the button is visible and ungated; the decline is not from a UI change in the build these phones run. Cannot: any rate. One phone moves a week by 7 points (1 of 14 is 7%, 2 of 14 is 14%), and the earlier 36% was 4 of 11. 2 of 14 against 1 of 12 is noise; the gap to 4 of 11 is suggestive, not proven. The 17% return rate is 2 of 12. The `near` and `location` events exist only from 10-10, so there are 4 and 5 phones behind them. Treat all of this as a prompt to measure, not as a finding.

## Fixes, both reversible

1. **Measure the thing, then judge it (data only, smallest).** Add the `near` value (and the distance bucket already computed for the button label) to the `directions` event, and change the digest row to "Take me there, of phones that opened a tree near them". Reverse by removing the property. Convention copied: CONVENTIONS.md "Measuring what people do in the app (2026-08-30)", the PostHog practice of AllTrails, Strava and komoot. It makes the weakest-link row stop punishing us for people who were never near a tree. The app half ships with the next build.
2. **For a phone far from every tree, lead with saving, not walking (app and web, one component each).** When `kmAway` is over about 25 km, the label already carries the distance ("Take me there · 800 km"), and the heart ("Want to visit") should be the lead action, with Take me there staying as the circle. Reverse by deleting the distance branch. Convention copied: Google Maps and AllTrails put Save beside Directions on a place far from you and show the distance on Directions. No CONVENTIONS.md heading covers a far-away place or a primary-action swap on distance, only "Directions, when the phone has more than one maps app" (WhatsApp) and "Landing after you have added something". This needs a one-paragraph look-up entry before anyone builds it, and it is a taste call, so Hidde's yes first.

Not recommended: moving the button, renaming the event, or re-ordering the bar. Nothing in the evidence points at them.
