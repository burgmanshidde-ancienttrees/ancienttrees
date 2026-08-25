#!/usr/bin/env python3
"""The numbers the corpus keeps getting wrong, printed instead of written down.

Hidde, 2026-08-25, on whether the corpus needs cleaning: "kijk jij helemaal niet
naar de corpus dan?"

It does need cleaning, and less than it looks. CLAUDE.md is about 27,000 words
and most of its numbers are honestly dated in place ("measured 2026-08-03 across
all 81 published cities"), which is history and reads as history. The rot is the
handful of counts written in the PRESENT tense, because those go stale silently
and a night run acts on them:

  "45 of 127 published cities have no photograph at all"   -> 71 of 171
  "92 of 1223 published trees carry no age"                -> 206 of 1842
  "the prioritized list of 100 cities"                     -> 179 entries

Fixing those three by hand fixes them until the next city ships. So the corpus
now points at this command instead of carrying the number, which is the same
move as every other ratchet here: replace a thing that has to be remembered with
a thing that runs.

    python3 scripts/stats.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def counts():
    out = {"cities": 0, "cities_without_a_photo": 0, "trees": 0, "photos": 0,
           "no_age": 0, "girth": 0, "height": 0, "approximate_pins": 0}
    d = os.path.join(ROOT, "data", "cities")
    for name in sorted(os.listdir(d)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(d, name), encoding="utf-8") as fh:
            city = json.load(fh)
        # A tree counts once it has a story: that is what makes a page.
        trees = [t for t in city.get("trees", []) if t.get("story")]
        if not trees:
            continue
        out["cities"] += 1
        shot = sum(1 for t in trees
                   if (t.get("photo") or {}).get("status") == "approved")
        if shot == 0:
            out["cities_without_a_photo"] += 1
        out["trees"] += len(trees)
        out["photos"] += shot
        for t in trees:
            if not (t.get("age_estimate") or t.get("age_min") or t.get("age_max")):
                out["no_age"] += 1
            if t.get("girth_cm"):
                out["girth"] += 1
            if t.get("height_m"):
                out["height"] += 1
            if t.get("location_precision") != "confirmed":
                out["approximate_pins"] += 1
    return out


def main():
    c = counts()
    print("%d published cities, %d trees" % (c["cities"], c["trees"]))
    print("%d trees carry a photograph; %d cities carry none at all"
          % (c["photos"], c["cities_without_a_photo"]))
    print("%d trees have no age, %d carry a girth, %d carry a height"
          % (c["no_age"], c["girth"], c["height"]))
    print("%d pins are only approximate" % c["approximate_pins"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
