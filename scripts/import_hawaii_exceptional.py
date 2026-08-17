#!/usr/bin/env python3
"""Import Hawaii's Exceptional Trees register.

    python3 scripts/import_hawaii_exceptional.py

Hawaii protects individual trees by law: Act 105 of 1975 lets each county
designate "exceptional trees", and the designation attaches to the specimen
rather than to the land, which is why this register names single trunks instead
of woodland. The City and County of Honolulu publishes the database, and despite
its title, "Exceptional Trees On Oahu", it carries all four counties: 236 rows
on Oahu, 38 on the Big Island, 29 on Maui, 24 on Kauai and 4 on Molokai.

Licence: CC0 1.0 Universal, Public Domain Dedication. Proven from the dataset's
own metadata endpoint, https://data.honolulu.gov/api/views/84fd-3fzf.json, whose
`license` block reads {"name": "Creative Commons 1.0 Universal (Public Domain
Dedication)", "termsLink": "http://creativecommons.org/publicdomain/zero/1.0/
legalcode"} with `licenseId` CC0_10 and attribution "Department of Parks and
Recreation". Fetched and read directly on 2026-08-17, not taken from a search
summary, which is the rule this project added the same week after WebSearch
invented two measurements.

Why this one matters: every row has coordinates, 217 carry a trunk
circumference, and 301 carry a condition reading. Coordinates AND a vitality
field under CC0 is better than anything else in data/registers/.

THE SEMANTIC FILTER, and hard rule 10 is unusually well served here because the
register answers it itself rather than leaving us to guess:

  military_base       39 rows sit on Schofield Barracks or Wheeler Army
                      Airfield. An active army base is not ground the public may
                      walk onto, so these are publishable: false. This is the
                      clearest hard-rule-10 signal any register has ever handed
                      us, and it would have been invisible from coordinates.
  dead_tree_location  a row recording where a dead tree stood. Never a page.
  ensembles           rows whose own text says grove, row, avenue or cluster
                      fail the collectible-point test unless the ensemble is
                      itself the destination, which is a judgement a verify pass
                      makes, not an import.

What is deliberately NOT filtered, because guessing would be worse than passing
it through: `land_use` is a single-letter code (P 145, I 100, S 58, V 17, and a
few SC, LC, M, L) with no codebook published beside the data, so it is carried
through raw rather than decoded into an access decision. `owner_name` appears on
only 53 rows and includes private individuals, which is a real private-land
signal, so it is carried through for the verify pass to weigh. And
`accessibility` is populated on 27 rows of 339, so it is a hint and not a gate.
"""

import json
import os
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "registers", "hawaii-exceptional-trees.json")
DATA = "https://data.honolulu.gov/resource/84fd-3fzf.json?$limit=2000"
META = "https://data.honolulu.gov/api/views/84fd-3fzf.json"
UA = "AncientTreesResearch/1.0 (https://ancienttrees.app; research contact via repo)"

ISLANDS = {"O": "Oahu", "Oahu": "Oahu", "B": "Hawaii (Big Island)", "M": "Maui",
           "K": "Kauai", "MO": "Molokai", "Moloka`i": "Molokai"}
ENSEMBLE_WORDS = ("grove", "row of", "avenue", "cluster", "hedge", "allee")


def get(url):
    return json.load(urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30))


def unit_check(diameter_in, circumference_ft):
    """Does this row's own circumference agree with its own diameter?

    The median across the dataset proves the unit, but a median cannot catch a
    single bad row, and there is at least one: a kamani recorded at 126 inches of
    diameter and 1.0 foot of circumference, off by a factor of 400. So every row
    is checked against itself and any disagreement is carried into the file
    rather than averaged away. "ok" means the two columns agree within 30 percent,
    loose enough for a buttressed trunk measured at a different height and tight
    enough to catch a typo.
    """
    if not diameter_in or not circumference_ft:
        return None
    import math as _m
    implied_ft = diameter_in * _m.pi / 12.0
    ratio = circumference_ft / implied_ft
    if 0.7 <= ratio <= 1.3:
        return "ok"
    return (f"disagrees: diameter {diameter_in:.0f} in implies {implied_ft:.1f} ft of "
            f"girth, the circumference column says {circumference_ft:.1f} ft "
            f"(ratio {ratio:.2f}). Do not use either without checking.")


def num(v):
    try:
        return float(str(v).replace(",", ""))
    except (TypeError, ValueError):
        return None


def main():
    rows = get(DATA)
    meta = get(META)
    lic = (meta.get("license") or {}).get("name")

    out = []
    for r in rows:
        lat, lng = num(r.get("latitude")), num(r.get("longitude"))
        text = " ".join(str(r.get(f) or "") for f in
                        ("common_name", "location_description", "description")).lower()
        reasons = []
        if r.get("military_base"):
            reasons.append(f"on an active military base ({r['military_base']}): "
                           "not ground the public may walk onto, hard rule 10")
        if r.get("dead_tree_location"):
            reasons.append("the register records this as a dead tree's location")
        if any(w in text for w in ENSEMBLE_WORDS):
            reasons.append("reads as a grove or row rather than one standable tree: "
                           "the collectible-point test is a verify pass's call")
        if lat is None or lng is None:
            reasons.append("no coordinate")

        # trunk_circumference is published in FEET, while diameter is in INCHES.
        # Nothing in the dataset says so and the two columns sit side by side, so
        # the first version of this import read circumference as inches and made
        # every girth twelve times too small: an Indian banyan came out at 155 cm,
        # a sapling rather than an exceptional tree, which is what gave it away.
        # Proven rather than assumed: across the 160 rows carrying both columns,
        # the median of (diameter x pi) / circumference is exactly 12.00.
        circ_ft = num(r.get("trunk_circumference"))
        out.append({
            "register_id": r.get("object_id") or r.get("old_id") or r.get("number"),
            "name": r.get("hawaiian_name") or None,
            "species_latin": r.get("scientific_name") or None,
            "common_name": r.get("common_name") or None,
            "island": ISLANDS.get(r.get("island"), r.get("island")),
            "latitude": lat, "longitude": lng,
            "girth_cm": round(circ_ft * 30.48, 1) if circ_ft else None,
            "girth_unit_check": unit_check(num(r.get("diameter_in_")), circ_ft),
            "diameter_cm": round(num(r["diameter_in_"]) * 2.54, 1)
                           if num(r.get("diameter_in_")) else None,
            "height_ft": num(r.get("height")),
            "vitality": r.get("tree_condition") or None,
            "assessed": r.get("date_assessed") or None,
            "locality": r.get("location_description") or r.get("location_address") or None,
            "land_use_raw": r.get("land_use") or None,
            "owner_name": r.get("owner_name") or None,
            "accessibility_raw": r.get("accessibility") or None,
            "military_base": r.get("military_base") or None,
            "coord_precision": "grid ~1.1 km, NOT tree level: the source rounds "
                               "latitude and longitude to 2 decimal places",
            "position_source": r.get("location_description") or r.get("location_address")
                               or None,
            "publishable": not reasons,
            "publishable_note": "; ".join(reasons) or None,
        })

    doc = {
        "source": "City and County of Honolulu, Department of Parks and Recreation: "
                  "Exceptional Trees (Act 105 of 1975). Titled 'On Oahu' but covering all "
                  "four Hawaiian counties.",
        "endpoint": DATA,
        "licence": lic,
        "licence_proof": (
            "Fetched live from the dataset's own metadata endpoint "
            f"{META} on 2026-08-17: license.name = {lic!r}, licenseId 'CC0_10', "
            "termsLink http://creativecommons.org/publicdomain/zero/1.0/legalcode, "
            "attribution 'Department of Parks and Recreation'. Read directly rather "
            "than from a search summary."),
        "designation": "Exceptional tree, designated by county ordinance under Hawaii "
                       "Act 105 (1975). The designation attaches to the individual "
                       "specimen, not to the land.",
        "country": "United States",
        "attribution": "City and County of Honolulu, Department of Parks and Recreation",
        "fetched": "2026-08-17",
        "scope": f"{len(out)} designated trees across Oahu, Hawaii (Big Island), Maui, "
                 f"Kauai and Molokai. {sum(1 for t in out if t['publishable'])} pass the "
                 f"semantic filter; {sum(1 for t in out if not t['publishable'])} do not.",
        "caveat": (
            "Three things a run must know. (1) THREE UNITS SIT SIDE BY SIDE AND NOTHING IN "
            "THE DATASET SAYS SO: height in FEET, diameter in INCHES, trunk "
            "circumference in FEET. The first version of this import read "
            "circumference as inches and made every girth twelve times too small; an "
            "Indian banyan came out at 155 cm, which is what gave it away. The unit "
            "is proven, not assumed: across the 160 rows carrying both columns the "
            "median of (diameter x pi) / circumference is exactly 12.00. Every row "
            "also carries `girth_unit_check`, because a median cannot catch one bad "
            "row and there is at least one. "
            "(2) `land_use` is a "
            "single-letter code with no codebook published beside the data, so it is "
            "carried raw and MUST NOT be decoded into an access decision by guessing. "
            "(3) THE COORDINATES ARE NOT TREE LEVEL AND MUST NEVER "
            "CARRY A CONFIRMED PIN. The source rounds latitude and longitude to two "
            "decimal places, about 1.1 km, so 278 of the 339 trees share a point with at "
            "least one other and one point in Honolulu carries 31 trees. That is coarser "
            "than `approximate` is meant to be, which is knowing the park but not the "
            "spot. The real locator is the text: `position_source` carries the register's "
            "own location description, Kalakaua Park, Haili Street, Old Riverside School, "
            "and a pin has to be geocoded from that and then said to be approximate, the "
            "way Hiroshima's shrines were. (4) There is no age field. Girth is on 217 "
            "rows, so an age can be derived where the species has a published growth rate, "
            "and it must say so."),
    }
    doc["trees"] = out
    with open(OUT, "w") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
    print(f"wrote {OUT}: {len(out)} trees, "
          f"{sum(1 for t in out if t['publishable'])} publishable")
    import collections
    print("  by island:", collections.Counter(t["island"] for t in out).most_common())
    print("  filtered out:",
          collections.Counter((t["publishable_note"] or "").split(":")[0]
                              for t in out if not t["publishable"]).most_common())


if __name__ == "__main__":
    main()
