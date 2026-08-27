# The App Store listing, written out so it can be pasted

Written 2026-08-27. Every field App Store Connect asks for, filled in, with the
character limits already counted. Nothing here needs deciding, only checking:
it is Hidde's name on the listing and his account that submits it.

Two rules held throughout. **Nothing promises what the build cannot do**: Plus
is hidden at launch, so walks, season alerts, offline and badges are not sold
here, and there is no "free forever" anywhere, because where the paid line
falls is his decision and copy must not make it for him. And the reader is the
subject, per PRODUCT_COPY.md.

## The fields

| Field | Value | Limit |
|---|---|---|
| App Name | `Ancient Trees` | 13 of 30 |
| Subtitle | `Find remarkable old trees` | 25 of 30 |
| Promotional Text | see below | 122 of 170 |
| Keywords | see below | 96 of 100 |
| Support URL | `https://ancienttrees.app/support` | |
| Marketing URL | `https://ancienttrees.app` | |
| Privacy Policy URL | `https://ancienttrees.app/privacy` | |
| Primary Category | Travel | |
| Secondary Category | Education | |
| Copyright | `2026 Ancient Trees` | |

**Promotional text** (changeable any time without a new build, which makes it
the right place for anything seasonal):

```
Every tree on the map is checked against two independent sources, and every one of them is free to find, read and walk to.
```

**Keywords** (comma separated, no spaces, they are matched as well as the name
and subtitle, so nothing here repeats those two):

```
trees,tree,nature,walk,walking,hiking,map,park,forest,outdoors,botany,oak,history,heritage,green
```

## Description

```
Ancient Trees maps the remarkable old trees of the world's cities, and shows you the ones near you.

Open it anywhere and the map fills with the trees around you: a yew that was old when the church beside it was built, a plane whose trunk takes four people to reach around, an oak that has stood through everything that happened on the street it shades. Each one has a page telling you what it is, roughly how old, and why it is worth the walk.

WHAT YOU GET

Trees near you, on a map you can search by place, by species or by name.

A story for every tree, written to be read rather than skimmed, and honest about what nobody knows: where an age has never been measured, the page says so and asks you.

Directions to the trunk. Where a location is rough rather than exact, the page tells you before you set off, because sending you to the wrong spot is the one mistake worth avoiding.

Your own collection. Photograph a tree while you stand in front of it and it joins your trees, ours and your own alike. Your photographs stay on your phone.

A season calendar per species, so you know whether a tree is at its best in April or in November.

WHERE THE TREES COME FROM

Every tree is verified against at least two independent sources before it goes on the map, and where the sources disagree the page says which and why. Official registers of protected and monumental trees are read directly. Photographs carry their own open licence and credit.

Nothing here is a wholesale import of a municipal tree inventory. A tree earns its place by being worth crossing town for.

WHEN WE ARE WRONG

We will be, and readers are how it gets fixed. Every page has a way to report a wrong pin, a fallen tree or a mistaken species, and corrections are made the same day.

An account is one email address. Sign in and your collection follows you to a new phone; delete the account and everything goes with it.
```

## What's New (version 1.0)

```
The first version. Remarkable old trees on a map, a story for each one, directions to the trunk, and a place to keep the ones you have stood in front of.
```

## Age rating

Answer every question with the lowest option. The two that need thought:

- **User-Generated Content**: YES, infrequent or mild. People can choose a display name and a picture other people see. There is reporting, blocking, a published contact address and terms that say what is not allowed.
- **Unrestricted Web Access**: NO. The app opens external links only for map directions and our own pages, never a browser you can type into.

Everything else (violence, language, gambling, medical, alcohol, horror,
contests) is None. The expected rating is 4+.

## App Review notes

Paste this in the Review Notes box. It answers the two questions this app
predictably raises, and gives them a way in that does not need a real email:

```
Ancient Trees is a map of verified remarkable old trees, free to use. There is no paid content and no in-app purchase in this version.

SIGNING IN is by email link, Apple or Google. Nothing in the app requires an account except keeping a collection and sending a correction; the map, every tree and every story work signed out.

USER CONTENT: people may set a display name and a profile picture that others can see when searching for somebody to follow. Reporting and blocking are on the three dots beside any person in Find People (My trees, the person icon beside your name). Blocked people can be lifted again under Settings, Blocked people. Reports reach us directly and we act on them. Our terms state there is no tolerance for offensive or impersonating profiles: https://ancienttrees.app/terms

PHOTOGRAPHS people take of trees stay on their own device and are not uploaded or shown to anybody else.

LOCATION is used only to centre the map on the trees nearest you and is never sent anywhere.

ACCOUNT DELETION is under Settings and removes the email address, the collection, the display name, the picture and every follow.
```

## Screenshots

Required: 6.9 inch iPhone (1320 x 2868), which Apple reuses for every smaller
size. `python3 scripts/appstore_shots.py` produces them from the simulator at
exactly that size, unframed and without captions, which is what a first
submission needs. Captions and a designed frame are a marketing decision and
his.
