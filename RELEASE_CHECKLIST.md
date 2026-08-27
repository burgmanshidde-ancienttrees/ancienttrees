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
- [ ] **Delete the account and confirm everything is gone**: saves, visits, profile, avatar file, follows in both directions. This is the promise the whole account track was opened on, and Apple requires a working deletion path.

**When things go wrong**
- [ ] No network at all: no crash, no blank screen that reads as broken
- [ ] Location denied, and then granted
- [ ] Camera denied
- [ ] A brand new install with nothing collected
- [ ] The largest accessibility text size
- [ ] Dark mode
- [ ] A real device, not the simulator, on cellular data

## 3. What Apple will ask for, and what we owe them

- [ ] **Privacy labels that match what we now store.** This changed on 2026-08-26: a display name, a profile photograph and a follow graph are new personal data. The privacy page was updated the same day; App Store Connect has not been.
- [ ] **Moderation for user photographs.** People can upload images to a public bucket. Review asks how that is moderated, and today the answer is nothing. This is the single most likely rejection.
- [ ] Support URL, marketing URL, privacy policy URL
- [ ] Screenshots at the required sizes
- [ ] Age rating
- [ ] Nothing in the build that promises what it cannot do (Plus is hidden, sponsoring is hidden until the IAP exists)

## The two open product calls, which are his

- Whether following shows a follower anything. Today it counts and nothing else.
- Whether the camera stays behind a sign-in wall for a signed-out person.
