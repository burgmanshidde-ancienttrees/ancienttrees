"""Build the inland US Southeast trees (verified and written 2026-11-04) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_us_southeast.py              # atlanta 11, nashville 8, asheville 4, great-smoky-mountains 3, chattanooga 1
    python3 scripts/build_us_southeast.py --only atlanta
    python3 scripts/build_us_southeast.py --out DIR    # dry build elsewhere (live places read from data/cities)
then city_names.py, preflight.py, commit by path, push. 27 trees: more than one day's pace,
so a publisher may pass --only first.

Sources in data/research/: atlanta-verified.json (Trees Atlanta champion program points as
finding aid, all pins approximate), nashville-verified.json (nsh_001..005 confirmed pins from the
Vanderbilt arboretum database; nsh_006..008 Tennessee Urban Forestry Council registry),
asheville-verified.json (three of four inside paid Biltmore, over the one-third ticket share;
free trees wanted), great-smoky-mountains-verified.json (trail giants, approximate trail pins),
chattanooga-verified.json (cht_001 only; cht_002 held). Place copy in us-southeast-places-a.json
and us-southeast-places-b.json. No photographs yet. Smokies (3) and Chattanooga (1) stay out of
Google until four.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None

SOURCES = [
    ("atlanta-verified.json", "atlanta"),
    ("nashville-verified.json", "nashville"),
    ("asheville-verified.json", "asheville"),
    ("great-smoky-mountains-verified.json", "great-smoky-mountains"),
    ("chattanooga-verified.json", "chattanooga"),
]
PLACE_FILES = ["us-southeast-places-a.json", "us-southeast-places-b.json"]
STATE = {"atlanta": "Georgia", "nashville": "Tennessee", "chattanooga": "Tennessee",
         "asheville": "North Carolina", "great-smoky-mountains": "Tennessee"}
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
REPLACE = ["intro", "meta_description", "question_meta", "question_answer", "question_context",
           "hero_tree_id", "oldest_tree_id"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "how_to_recognise",
               "verified_sources", "official_register", "access", "transport", "best_time",
               "photo", "location_precision", "pin_source", "curation_status", "verify_notes",
               "paid_entry"]
PAID = {"avl_002", "avl_003", "avl_004", "nsh_008", "atl_009"}
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}


def tree(t):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    if not o.get("how_to_recognise") and t.get("recognise"):
        o["how_to_recognise"] = t["recognise"]
    loc = dict(o.get("location", {}))
    if "neighborhood" in loc and "neighbourhood" not in loc:
        loc["neighbourhood"] = loc.pop("neighborhood")
    o["location"] = loc
    o["verified_sources"] = [s if isinstance(s, str) else s.get("url") for s in o.get("verified_sources", [])]
    p = t.get("photo") or {}
    o["photo"] = ({k: p[k] for k in ("url", "license", "attribution", "attribution_url", "status") if p.get(k)}
                  if p.get("status") == "approved" else dict(MISSING))
    o.setdefault("curation_status", "ai_generated")
    if o["id"] in PAID:
        o["paid_entry"] = True
    return o


def write(path, d):
    with open(path, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    places = {}
    for pf in PLACE_FILES:
        places.update(json.load(open(os.path.join(R, pf))))
    by_place = {}
    for src, slug in SOURCES:
        if ONLY and slug != ONLY:
            continue
        for t in json.load(open(os.path.join(R, src))):
            if t.get("hold"):
                continue
            if not t.get("story"):
                sys.exit(f"{t['id']} has no story; refusing to build")
            by_place.setdefault(slug, []).append(tree(t))
    os.makedirs(OUT, exist_ok=True)
    for slug, ts in by_place.items():
        p = places[slug]
        live = os.path.join(CITIES, slug + ".json")
        if os.path.exists(live):
            d = json.load(open(live))
            have = {x["id"] for x in d["trees"]}
            new = [x for x in ts if x["id"] not in have]
            if not new:
                print("already in", live)
                continue
            d["trees"] += new
            for k in REPLACE:
                if p.get(k):
                    d[k] = p[k]
            asked = {f["q"] for f in d.get("faq", [])}
            d.setdefault("faq", []).extend(f for f in p.get("faq", []) if f["q"] not in asked)
        else:
            d = {k: p[k] for k in PLACE_FIELDS if k in p}
            d.setdefault("country", "United States")
            d.setdefault("status", "needs_curation")
            d["trees"] = ts
        ids = {x["id"] for x in d["trees"]}
        for k in ("hero_tree_id", "oldest_tree_id"):
            if d.get(k) and d[k] not in ids:
                sys.exit(f"{slug}: {k} {d[k]} is not one of its trees")
        write(os.path.join(OUT, slug + ".json"), d)
        print("wrote", slug, len(d["trees"]), "tree(s),", len(ts), "from this pass")
    if OUT == CITIES:  # Contract L: every US place names its state
        sp = os.path.join(ROOT, "data", "us-states.json")
        d = json.load(open(sp))
        added = [s for s in by_place if s not in d["places"]]
        if added:
            d["places"].update({s: STATE[s] for s in added})
            with open(sp, "w") as f:
                json.dump(d, f, ensure_ascii=False, indent=1)
                f.write("\n")
            print("us-states.json: added", ", ".join(added))

if __name__ == "__main__":
    main()
