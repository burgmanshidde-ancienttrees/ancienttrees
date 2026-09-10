# Experiments

Every validation experiment gets an entry BEFORE it runs: hypothesis, metric, review date. Results get written next to it, whatever they say. This file exists so observations become evidence instead of assumptions (the disease the 2026-07-27 audit named), and so no experiment runs forgotten forever.

## 3. Copy testing, continuous (live 2026-09-10)

Registered before it runs, which is this file's own rule and the reason it
exists. Hidde's instruction was two sentences: "let's test", then "i'd like to
do continuous testing of copy tbh and make it part of the learning cycle". The
second is the important one, so this entry describes a STANDING LANE rather
than one experiment: a test ends, a winner is promoted, the next one starts,
and the daily digest reports where the running one stands.

- **Hypothesis (test 1, `city-title-age-first`):** on a city page title the age
  is the hook and the count is inventory, so `Oldest 235 Years, 23 to See`
  earns more clicks than `23 to See, Oldest 235 Years`.
- **Arms:** 28 pages each, matched pairs on pre-period impressions. Assignment
  frozen in `data/copy-tests.json` on the start date and never recomputed.
- **Metric:** index, meaning CTR against the CTR that position normally earns,
  read as difference in differences against each city's own pre-period so that
  city-level differences and Google-wide movements both cancel.
- **Review:** 2026-11-05, eight weeks. Not before, and this is the whole
  discipline of the thing: a page takes about two clicks per ten days, so a
  lead at three weeks is noise wearing a result's clothes. `copytest.py` prints
  TOO EARLY until day 42.
- **What it can see:** an effect of roughly 25 to 35 percent. Smaller than that
  is invisible at our volume and no amount of staring at the table changes it.
- **What it cannot see:** Google rewrites title links a share of the time, so
  this measures the title we set and not always the title shown. That dilutes a
  real effect rather than inventing a false one, so a null result is weaker
  evidence than a positive one.
- **Honesty guard:** the head phrase `Ancient Trees in [City]` is identical in
  both arms, so a win cannot be a ranking change wearing a copy result's
  clothes. Both arms remain true sentences about the page; TONE_OF_VOICE.md's
  bans and "never promise the visitor something that is not there" are not
  suspended for a test.
- **Guard against the silent failure:** `check_copy_test_renders()` in
  scripts/qa.py fails the deploy if the challenger wording is not actually
  reaching its pages. The first wiring of this test looked up a variable that
  did not exist, built cleanly, and put every page in the control. Eight weeks
  would have passed before anybody noticed, and the report would have read
  exactly like a failed hypothesis.

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
