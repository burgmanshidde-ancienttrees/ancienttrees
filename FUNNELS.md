# FUNNELS — the three journeys, and how to audit them

Written 2026-08-14 at Hidde's request ("how can i best instruct you to assess
those funnels"). **The instruction is one line: "run the funnel audit."** A
session or run that gets it reads this file, pulls the latest numbers from
DATA.md (never re-derives them), fills the three tables, and names ONE fix per
funnel: the biggest measured drop-off with a proposed change, its convention
reference, and what event will prove it worked. Suggestions without a measured
drop-off behind them are decoration; so are redesigns of steps that already
convert.

Hidde's framing, verbatim intent: step 1 make people interested in the content
and explore; step 2 see the functionalities that require login and use them;
step 3 see the benefits of the app and go there, because **the app is where
the money will be**.

## Funnel 1 — Arrive → explore (content does its job)

| Step | Meter |
|---|---|
| Shown in Google | impressions (Search Console, DATA.md) |
| Clicked | clicks / CTR |
| Read more than one page | pages per visit (Cloudflare) |
| Opened a walk | `walk-open`, `walk-start` events |
| Asked for directions | `directions` event |

Directions is this funnel's floor: goal 1 of the whole project is a person in
front of a tree, and `directions` is the closest measurable proxy.

## Funnel 2 — Explore → identified (the login features)

| Step | Meter |
|---|---|
| Saved a tree | `save` event |
| Voted worth-it | `worthit-*` events |
| Opened the sign-in surface | first-save dialog (no own event; infer from next row) |
| Asked for a magic link | `signin-link-sent` |
| Became an account | accounts count (digest) |

Deliberate divergence, recorded in DECISIONS.md 2026-08-14: the save works
WITHOUT login (AllTrails gates it). So this funnel's conversion is soft by
design until the deletion proof lands; judge it accordingly.

## Funnel 3 — Anywhere → the app (the money)

| Step | Meter |
|---|---|
| Tapped any Get-the-app | `app-cta` (nav, tree bar, pitch blocks, sign-in dialog — all tagged `data-ev`) |
| Reached /app | Cloudflare top paths |
| Joined the waitlist | `waitlist-submit` + waitlist count (digest) |

Until the app exists, the waitlist IS the revenue funnel. Every `app-cta`
source carries the same event on purpose: the first question is whether anyone
taps at all, not which button they tapped.

## Rules for the audit

- Numbers from DATA.md only; the digest now counts every event above daily.
- Tiny volumes stay tiny: below ~50 visits/day, report direction, never
  percentages with decimals, and say so (the standing noise rule).
- One fix per funnel per audit, with its convention reference (AllTrails,
  Google Maps, Airbnb, PictureThis) and its proving event. Ship it, then the
  next audit judges it.
- Adding a funnel step to the site is an attribute, not a script: put
  `data-ev="event-name"` on the element (Base.astro's delegated tracker
  reports it) and add the name to the digest's list in daily_digest.py.
