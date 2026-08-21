# Spot, the camera, and your own trees

Written 2026-08-21 for Hidde, who asked for one proposal rather than a
half-built feature: "we moeten nadenken over die spot/fotografeer/collect
interactie in het midden van een app, want dat is echt de kern van de app."

## The idea in one sentence

Photographing a tree you are standing in front of is the app's core act, the
way recording a run is Strava's, and it produces one of two things: a tree
added to YOUR map, or a tree suggested for OURS.

## Why a photograph rather than a tap

A tap is free, so it means nothing and can be done from the sofa. A
photograph is evidence AND a souvenir at once, which is the rare case where
the thing that proves you were there is also the thing you want to keep. It
also answers the project's oldest data problem: 1,190 of 1,562 trees have no
photograph, and the people best placed to fix that are standing in front of
them.

## Two layers, and this is Hidde's own distinction

**Ours** is the Remarkable Trees map: verified, sourced, editorially chosen,
the thing the website publishes. Unchanged.

**Yours** is every tree you have photographed, on the same map in your own
colour. It includes trees of ours you have collected AND trees only you have
recorded. Nobody else sees it.

A tree can be in both: you photograph our Beethoven Plane, it joins yours and
stays ours.

## What happens when you press Spot

The GPS decides the order, never the outcome.

1. **Trees of ours within 400 m.** Pick one, photograph it, and it is
   collected. The photograph is yours; you may also offer it to us for that
   tree's page.
2. **Nothing of ours here.** Photograph it and answer two short questions
   (what is it, why is it worth it). It joins YOUR map immediately, and you
   choose whether to suggest it for ours.

Either way you are looking at a camera within one tap of pressing the button.

## Status, for a suggested tree

Hidde asked for this and it is the honest half of asking people for work.
Four states, visible on your own tree: **sent**, **being checked**,
**on the map** (with a link to the published page), **not this time** (with
one line saying why: not publicly reachable, could not verify, already
mapped). A tree that is not taken still stays on YOUR map. Nothing is
wasted.

## What this needs, and the two things only Hidde can approve

**Phase 1, buildable now, needs nothing from him.** Camera capture, the photo
stored ON THE PHONE, your own trees layer on the map, your own list in
Collect, and the suggestion text sent through the submissions channel that
already exists. No new server storage, no new personal data on our side, no
cost. This gives the entire core interaction and the whole feel of the
feature.

**Phase 2 needs his explicit yes, twice over.** Uploading photographs means a
new Supabase bucket and a new table holding a person's photograph with its
coordinates and time, which is personal data (accounts rule) and storage that
costs money (hard rule 5). The numbers: a photo downsized to 1600px is about
300 KB, so the free tier's 1 GB holds roughly 3,000 of them; beyond that it
is 25 dollars a month. Recommendation: keep user photographs PRIVATE at
first. Publishing them means moderating them, and that is a different
project.

## The paywall problem, stated plainly

The recorded line (DECISIONS.md, 2026-08-20) is that ticking is free and the
PROOF is what Plus sells: photograph, seal, badges. If photographing becomes
the only way to collect, that line puts the core act behind the paywall and a
free user can no longer collect at all, which contradicts PRODUCT_IA.md's law
3 and leaves nothing to convert.

So the line has to move. The recommendation: **photographing to collect is
free and unlimited.** Plus keeps season alerts, curated walks, offline, and
gains the things that are genuinely extra: your photograph published on our
tree page, badges, and the yearly summary of where you walked. That is
Hidde's call, not mine.

## What I would build first

Phase 1, in this order: camera in Spot, your own trees on the map in your own
colour, your own list in Collect beside ours, and the status line on a
suggested tree. Then we look at it on his phone and decide about uploading.
