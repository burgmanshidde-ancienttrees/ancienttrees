# Show HN draft, plus the comment answers

First written 2026-08-08, approved in principle by Hidde ("klinkt prima"); his HN account exists since 2026-08-09. Rewritten 2026-10-23 on his "lets do 3 then" after the Reddit practice: the numbers, the stack and the AI line were out of date (the site has accounts, a cookie bar and an app now, so "no accounts, no cookies" is false). Only he posts it, from his own account (hard rule 4; HN expects the maker in the comments).

**What Show HN is, in one paragraph.** Hacker News (news.ycombinator.com) is the discussion site of the tech world; a "Show HN" is its standing format for "I built this, have a look". A post that lands brings thousands of curious, critical visitors in a day, and the mentions that follow are the kind of authority our rankings lack. Free, one post, roughly one good shot, so it is written with care. Post on a Tuesday, Wednesday or Thursday between 14:00 and 17:00 Dutch time (US morning). Submit the URL with the title AND the first-comment text in the text field of the submit form, so the explanation sits on the post itself (2026-10-27: on the first try the separate comment from a new account went [dead] at once, so readers saw a bare link; the mail to the Hacker News moderators of 10-23 got no answer). Stay near the comments for a few hours; "fair point" and fix beats arguing. Never ask anyone to upvote (HN bans for it).

## The post

**Title** (under 80 characters; the plain one first):

Show HN: A map of old trees worth walking to

Show HN: I'm mapping the old trees worth walking to (3,800 so far)

**URL:** https://ancienttrees.app

**First comment** (his voice; put one sentence of your own in before it goes):

This actually started in Lisbon. Travelling for work, I always had some time to kill, and strolling through the parks I was fascinated by the old jacarandas and fig trees (not that I knew the species then). They seemed ages old, planted by someone no longer living, for us to marvel at. Later I accidentally parked in front of a huge old ficus in Palermo and was blown away. I'm not a tree expert, but I am a big fan, and I wanted an easier way to find trees like these wherever I was.

So this is a map of old trees worth a detour. For each one: where exactly it stands, how old it is and how sure anyone is about that, what its story is, and whether you can actually get to it. About 3,800 trees in 230 cities so far. The oldest is a chestnut on Etna that a 2022 study put at roughly 2,200 years; I still haven't seen it. Every tree is free to look at, no signup. You only need an account to save trees or tick off the ones you've visited.

To be honest about how it was made: AI helped me set this up. The trees come from official registers of protected trees, tree societies and local papers, and AI wrote the first version of each story from those sources, which every page says. The whole idea is that it doesn't stay that way. People who know the trees correct them and add the ones I'm missing, and that has started to happen. AI was the starting point, not the product.

Each tree has a story that only locals know, and that's the part I can't do alone. Which tree near you is missing?

(Hidde, 2026-10-24: the AI paragraph in his own framing, "AI was just there as a starting point"; the stack and the photo share cut, "nobody cares"; the account line made honest, saving needs an account. If asked about the stack: "Astro static site, Supabase, a SwiftUI iOS app", once.)

## Prepared answers for the questions that will come

**"AI-generated content?"** Straight, it is the only thing that works there: the stories are written with AI from named sources and labelled on every page; the trees, pins, measurements and photos come from registers and people, not generated; readers correct them and a correction is applied the same day. "The fastest way to check is to look up a tree you already know." (They will.)

**"Is the data open?"** The repo is public (github.com/burgmanshidde-ancienttrees/ancienttrees, the trees are JSON under data/cities) but there is no licence on it yet. Say that plainly; promise nothing. Whether to license the merged dataset openly is Hidde's call.

**"Doesn't publishing exact locations endanger the trees?"** The honest strength: where a register withholds a location, we never publish that tree, even when the spot could be worked out from elsewhere. What we map is trees that cities themselves signpost and registers publish.

**"How do you make money?"** Not yet. The idea is a paid tier later for app extras (offline, navigation); every tree stays free to explore. Never "free forever", never "no ads ever".

**"How sure are the ages?"** As sure as the source: the page gives the basis, and "approximately" means approximately. Where two sources disagree the page says both (the Messina fig's two girths are a good example).

**"Why no Android?"** One person, iOS first. There is a notify-me list on the site.

**"Where's the oldest?"** Point at a real page: the Hundred-Horse Chestnut on Etna (ancienttrees.app/santalfio), the 2,850-year olive near Lisbon.

**"City X is missing / my city's list is wrong."** Thank them, ask where it stands, add it as a lead the same day. Every tip is a tree to finish, same as Reddit.

## Pre-flight (the session runs this before he posts)

1. Refresh the numbers in the comment against the live data (trees, cities, photo share move daily).
2. Production check: homepage, map, two flagship cities, one tree page, the Sicily collection, all loading clean; latest deploy green.
3. Test "Suggest a tree" end to end once, because submissions are the win the post asks for.
4. Google Analytics is in place, so the spike measures; note the date in LOG.md.

## After it runs

Record in LOG.md and OUTREACH.md: date, points, comments, visitors (GA, referrer news.ycombinator.com), submissions and accounts in the following week. A good thread becomes the "as seen on" line for press pitches.
