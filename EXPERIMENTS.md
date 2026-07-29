# Experiments

Every validation experiment gets an entry BEFORE it runs: hypothesis, metric, review date. Results get written next to it, whatever they say. This file exists so observations become evidence instead of assumptions (the disease the 2026-07-27 audit named), and so no experiment runs forgotten forever.

## 1. The Plus door (live 2026-07-28, demoted same evening, CLOSED 2026-07-29 by Hidde before any data)

Hidde's call: "plus komt nog te vroeg, laten we eerst de app-behoefte testen." The nav button existed for a few hours; the page (now a full benefits landing) stays reachable via the footer. Click data from the nav period and the footer period are not comparable; treat footer-era clicks as the baseline.

- **Hypothesis:** visitors who love the site will click a "Plus" nav item, signalling willingness to pay for convenience (offline packs, season alerts, route guidance).
- **Metric:** cookieless path counts for /plus (weekly, in DATA.md's beacon section) plus any waitlist emails via the form.
- **Honesty guard:** the page states plainly that Plus does not exist yet and shows no price (hard rule 2).
- **CLOSED 2026-07-29, Hidde: "you can delete everything around plus for now."** The footer link is gone and /plus now redirects to /app (the url had been public for a day, so it resolves rather than 404s). No data was collected; nothing was learned; the app door (below) is the one running experiment. If Plus returns it gets a fresh entry.
- **Review:** 2026-09-15, post-Japan checkpoint. Noise caveat: at current volume, weeks of zero clicks prove nothing; a cluster of clicks means something.

## 2. The app door, the PRIMARY experiment (live since 2026-07-28)

- **Hypothesis:** "Get the app" is the most-wanted missing piece; clicks measure app-demand before a line of app code exists.
- **Metric:** path counts for /app, same cadence and caveats as above.
- **Page upgraded to a full benefits landing (AllTrails-style, four verb-cards, coming soon) the same evening**; click data before/after the upgrade not comparable, which matters little since the before-window was hours.
- **Review:** 2026-09-15.
