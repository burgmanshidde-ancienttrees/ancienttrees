# Discover, redesigned (2026-10-10)

Approved by Hidde on 2026-10-10 ("im happy build it in the app") from board D3 of the Discover canvas (https://claude.ai/artifact/313WKZqbMxFFqHZw8HqVm2), with the Want to visit board beside it. The benchmark behind it is CONVENTIONS.md "The browse / Discover screen, benchmarked (2026-10-06)".

## The page, top to bottom (app, Screens/Home.swift)

1. **Discover** title and search bar, pinned as before (his 2026-08-26 sticky search).
2. **Season hero (H1).** The nearest photographed tree whose best_time includes this month, on the viewer's half of the world. "Autumn is here" (the word flips for the south), "N trees at their best this month · M within 20 km of you", and the white tag "At its best now". Taps through to that tree. No such tree: the stock hero.
3. **Want to visit, with trees.** Your saved trees, nearest first, three tiles; See all opens My trees on the Want to visit lane (Navigator.openWantToVisit).
4. **At their best now.** Six photographed trees at their best, nearest first, as tiles.
5. **Our favourite tree cities.** The app's place card, 172 by 120.
6. **Ambassador row** for the city you stand in, only when its seat is open. Kept away from Add a tree on purpose.
7. **Tree countries.** The same place card.
8. **Want to visit, empty.** Three blank tiles with a bookmark, one line, "Find trees near you" (opens the map). Lower on the page so a first visit meets trees first.
9. **Tree islands.** Tiles, the island as the tag.
10. **By species.** Photo pills, wrapping (S3).
11. **The records.** Oldest, thickest, tallest: three tiles opening the full list.
12. **Lists with an opinion.** Six hand-made collections, in-season first, each face used once.
13. **Walks near you**, once walks ship (Launch.walks).
14. **The map is still growing**, with Add a tree.
15. **More trees near you.** Every photographed tree not already on the page, nearest first, three across, loading as you scroll.

## Rules

- **One tile:** CollectedTile, 3:4, three across, edge to edge, 2 points apart, as My trees.
- **One tag:** TagPill, white with moss letters. A tree within 30 km shows "City · 1.4 km", further away the city alone.
- **See all ›** on every heading that has a destination; no subtitles under headings.
- **A row with nothing for where you are is skipped**, never drawn empty. Want to visit's empty state is the one deliberate exception.
- Photographed trees only in tiles; trees without a photograph stay on the map and their city pages.

## Not in this change

- **The website homepage.** Hidde asked for the app ("build it in the app"); the web board on the canvas is out of date and is redrawn from D3 before it is built. A deliberate one-surface change, recorded here.
- **Gardens and parks row.** The app has no park page, so the row has nowhere to go yet.
- **Feed fields.** Nothing new travels except TreeCollection.face, which browse.json already sent.

## Known limit

The season hero shows a tree's lead photograph, and many were taken in winter (Copenhagen's dendron.dk set is mostly bare), so "Autumn is here" can sit over a leafless crown. Nothing in the data says when a photograph was taken; a reader's in-season photograph would fix it per tree.
