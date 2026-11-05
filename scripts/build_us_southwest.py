"""Build the US Southwest and Mountain West trees (verified and written 2026-11-04) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_us_southwest.py              # writes every place below (all new)
    python3 scripts/build_us_southwest.py --out DIR    # dry build elsewhere
    python3 scripts/build_us_southwest.py --only tucson
then city_names.py, preflight.py, commit by path, push.

Sources in data/research/: tucson-verified.json (tus_; University of Arizona campus arboretum,
pins from its GIS, plus Phina's Tree downtown), boulder-verified.json (bld_; the City of
Boulder's notable-tree story map), santa-fe-verified.json (sfn_), prescott-verified.json (pct_;
prs is Perusic's), phoenix-verified.json (sct_001 Scottsdale, glz_001 Glendale; Phoenix proper
yielded none), albuquerque-verified.json (abq_), denver-verified.json (dnv_),
flagstaff-verified.json (flg_), sedona-verified.json (sdn_, Slide Rock State Park, paid).
Tubac and Tumacacori yielded none. Place copy in us-southwest-places.json. No photographs yet.
Only Tucson and Boulder reach four; the rest are lone tree pages, their place pages stay out of
Google until they reach four.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None

SOURCES = [
    ("tucson-verified.json", "tucson"),
    ("boulder-verified.json", "boulder"),
    ("santa-fe-verified.json", "santa-fe"),
    ("prescott-verified.json", "prescott"),
    ("phoenix-verified.json", None),  # each tree names its place
    ("albuquerque-verified.json", "albuquerque"),
    ("denver-verified.json", "denver"),
    ("flagstaff-verified.json", "flagstaff"),
    ("sedona-verified.json", "sedona"),
]
STATE = {"tucson": "Arizona", "prescott": "Arizona", "scottsdale": "Arizona",
         "glendale-arizona": "Arizona", "flagstaff": "Arizona", "sedona": "Arizona",
         "santa-fe": "New Mexico", "albuquerque": "New Mexico",
         "boulder": "Colorado", "denver": "Colorado"}
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "how_to_recognise",
               "verified_sources", "official_register", "access", "transport", "best_time",
               "photo", "location_precision", "pin_source", "curation_status", "verify_notes",
               "paid_entry"]
PAID = {"sdn_001"}  # Slide Rock State Park fee
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}


def tree(t):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    if not o.get("how_to_recognise") and t.get("recognise"):
        o["how_to_recognise"] = t["recognise"]
    o["verified_sources"] = [s if isinstance(s, str) else s.get("url") for s in o.get("verified_sources", [])]
    p = t.get("photo") or {}
    o["photo"] = ({k: p[k] for k in ("url", "license", "attribution", "attribution_url", "status") if p.get(k)}
                  if p.get("status") == "approved" else dict(MISSING))
    o.setdefault("curation_status", "ai_generated")
    if o["id"] in PAID or t.get("paid_entry") is True:
        o["paid_entry"] = True
    return o


def write(path, d):
    with open(path, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    places = json.load(open(os.path.join(R, "us-southwest-places.json")))
    by_place = {}
    for src, slug in SOURCES:
        for t in json.load(open(os.path.join(R, src))):
            if t.get("hold"):
                continue
            place = slug or t["place"]
            if ONLY and place != ONLY:
                continue
            if not t.get("story"):
                sys.exit(f"{t['id']} has no story; refusing to build")
            by_place.setdefault(place, []).append(tree(t))
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
