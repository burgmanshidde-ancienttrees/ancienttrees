# Plus: the thinking as it stands, 2026-08-26

Working note from a session with Hidde, superseding nothing yet: the recorded
paywall line of 2026-08-18 (DECISIONS.md, €19.95/year, four features) stands
until he replaces it. He called that line "een beetje random bedacht" today
and asked for better thinking. This file is that thinking, so the next
conversation continues instead of restarting.

## What is settled in this conversation (his words, today)

- **The app launches free and clean, with NO reference to Plus at all.** His
  reason: "dan krijg je een veel vergevingsgezindere groep." So the paywall
  screen and every Plus-named card go behind a flag in the launch build (code
  stays). The launch moment (Product Hunt, Reddit, Facebook groups) is spent
  on users and data, not on a first euro. Never say "free forever" anywhere;
  the copy rule stands.
- **"Sponsor this project" DOES go live at launch.** The one money ask that
  fits the forgiving register (Wikipedia/OSM, not freemium), aimed at covering
  his cloud costs. State: everything around it was built on 2026-08-25; the
  purchase itself is his (hard rule 2). In the app that means he creates the
  IAP product in App Store Connect (Apple requires IAP for this, minus 15%);
  on the website a support page can use any provider once he opens the
  account (Ko-fi, GitHub Sponsors, Stripe), which only he may do.
- **Log, badges and photo upload are free.** His reason is the right one:
  "dat heb je nodig voor je datalust." Collecting is the flywheel; charging
  contributors strangles it.
- **Walks are held in reserve.** The app can launch without them. Verified
  today: the city page's walk button already says "in the app" and the
  /[city]/walks pages are quiet SEO pages, so holding walks back costs
  nothing. They stay a card to play later (free update moment, or Plus).
- **Season Radar must be TRUE before it can be sold.** Today ~34 species files
  and ~1 in 5 trees with a best_time. If radar becomes a Plus pillar, the
  2026-08-08 "phenology is lowest-priority depth" ruling flips at that moment,
  not before.
- **The 2026-08-18 four-feature package is too weak as a subscription.** His
  own verdict today. Offline is weak in cities (you have 5G in Barcelona; it
  is a mountains feature at AllTrails and becomes ours when parks/forests
  arrive). Radar is half real. Walks are in reserve. Log depth does not exist
  yet. What remains does not carry €19.95/year.

## The four-question test for any future Plus idea

1. Does gating it slow the inflow of data or users? Then free.
2. Does the heavy user want it while the new user does not miss it? Then it
   may be Plus.
3. Does it have recurring value? Otherwise it fits a one-time purchase (the
   Komoot map-pack model), not a subscription.
4. Does a reference product charge for the same thing? If none does, why are
   we the first?

## His line, later the same day: the walks ARE Plus

Hidde, after rejecting the stats-and-recap lane ("nobody gives a fuck",
keep it in Plus but it converts nobody) and staying unsure on the Komoot
model: "alle wandelingen naar plus... een harde streep. Je kan toevoegen en
je kan bomen alleen bekijken, maar de wandelingen zelf, die hou je helemaal
achter." One sentence: **every tree free, the walks are Plus.**

Why it holds up: it leaves everything that feeds the flywheel free (viewing,
adding, collecting); the walks are our own editorial work, not community
contribution, so the line taxes no contributor; the category precedent is
GPSmyCity (place articles free, the self-guided walk paid); and the July
interim-paywall paragraph always had routes on the paid list. It also chains
perfectly with "launch without walks": the later Plus introduction then IS
the walks launch, news instead of a wall, and the no-clawback contract holds
by construction.

The two costs, owed before the introduction: (1) the quality bar, a paid walk
that routes badly is a refund-grade review, so the auto-routed walks must
feel curated before they are sold; (2) the web leak, /[city]/walks currently
serves full routes plus GPX free and must become a teaser when walks go paid,
which is an SEO decision to take deliberately, not a footnote.

Radar alerts and offline can join the package later as "everything for the
afternoon out"; behaviour will tell. The stats/recap lane stays in the
drawer as garnish, not a driver.

## The earlier open choice: feature line or geography line

**Feature line** (the current recorded shape, revised): free = everything
that grows the product; Plus = full offline, radar alerts, the rich log
(year recap, species counts, rare badges). Honest state: every pillar needs
building before it is sellable.

**Geography line** (his idea today: hometown free, world paid). Komoot's
proven model. Why it fits: the pay moment coincides with the spend moment (a
booked trip), collecting and contributing happen at home and home stays free,
the core promise ("trees near you") stays free by definition, and the weak
features (offline, radar, world access) become one coherent travel kit
together. The correction it needs: our acquisition IS travellers finding city
pages on Google, so the first-run experience must never wall the city someone
is standing in. Komoot's mechanic (you choose your one free region, forever)
or "your current location always works, paying is about planning and
collecting beyond home" are the candidate shapes; where that line falls
exactly is the design work.

The tension to resolve consciously: the geography line has the app gating
content that the website must keep serving free (SEO). The leak is
acceptable, the app sells comfort, but it contradicts the letter of the
2026-08-18 "every tree, story and location stays free on web and in the app"
sentence, so choosing it means rewriting that sentence, which is Hidde's
alone.

**Also on the table, parked:** the Polarsteps money model, a printed tree
passport (the trees you actually stood before, with your photos) as a
one-time physical purchase beside any subscription. On-brand for collectors,
zero commercial hate; needs a print partner, which is a new dependency and
his yes.

## What this licenses a run or session to do now

Nothing behind a paywall, nothing priced. The only work this note justifies
today: keep building the candidate pillars as free infrastructure (offline
feeds, phenology coverage when prioritised, log sync end-to-end proof), and
hide the existing paywall screen from the launch build when the release nears.
Pricing, the final line, and the launch call are Hidde's (hard rules 2 and 5).
