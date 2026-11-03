"""Build the Boston-area trees (verified and written 2026-11-03) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_us_boston.py            # appends 27 to boston (13 -> 40), writes salem-massachusetts (3) and lexington-massachusetts (1)
    python3 scripts/build_us_boston.py --out DIR  # dry build elsewhere (live places read from data/cities)
then city_names.py, preflight.py, commit by path, push. 31 trees: more than one day's pace,
so a publisher may pass --only boston first.

Sources in data/research/: boston-mtauburn-verified.json (bos_014..023: Mount Auburn Cemetery,
pins from the cemetery's own plant inventory, all approximate; bos_023 the York St plane in
Cambridge), boston-arboretum-verified.json (bos_030..038, confirmed pins from the Arnold
Arboretum's accession GIS), boston-common-verified.json (bos_046..053: Public Garden and
Common pinned from the City of Boston's BPRD park tree inventory, PDDL; Franklin Square;
Dilboy Field, Somerville), salem-concord-verified.json (sma_001..003 Salem, lxg_001 Lexington,
view-only from the pavement; Concord yielded none). Register rows: Massachusetts DCR Legacy
Trees (data/registers/massachusetts-dcr-legacy-trees.json, geocoded in
boston-dcr-geocoded.json). Place copy in us-boston-places.json. No photographs yet.
Salem (3) and Lexington (1) stay out of Google until four.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None

SOURCES = [
    ("boston-mtauburn-verified.json", "boston"),
    ("boston-arboretum-verified.json", "boston"),
    ("boston-common-verified.json", "boston"),
    ("salem-concord-verified.json", None),  # each tree names its place
]
PLACE_OF = {"Salem": "salem-massachusetts", "Lexington": "lexington-massachusetts"}
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
REPLACE = ["intro", "meta_description", "question_meta", "question_answer", "question_context",
           "hero_tree_id", "oldest_tree_id"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "how_to_recognise",
               "verified_sources", "official_register", "access", "transport", "best_time",
               "photo", "location_precision", "pin_source", "curation_status", "verify_notes",
               "paid_entry"]
PAID = set()
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
    if o["id"] in PAID:
        o["paid_entry"] = True
    return o


def write(path, d):
    with open(path, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    places = json.load(open(os.path.join(R, "us-boston-places.json")))
    by_place = {}
    for src, slug in SOURCES:
        for t in json.load(open(os.path.join(R, src))):
            if t.get("hold"):
                continue
            place = slug or PLACE_OF[t.get("place")]
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
            for k in REPLACE:
                if p.get(k):
                    d[k] = p[k]
            for f in d.get("faq", []):
                if f["q"] in p.get("faq_replace", {}):
                    f["a"] = p["faq_replace"][f["q"]]
            asked = {f["q"] for f in d.get("faq", [])}
            d.setdefault("faq", []).extend(f for f in p.get("faq_add", []) if f["q"] not in asked)
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
            d["places"].update({s: "Massachusetts" for s in added})
            with open(sp, "w") as f:
                json.dump(d, f, ensure_ascii=False, indent=1)
                f.write("\n")
            print("us-states.json: added", ", ".join(added))

if __name__ == "__main__":
    main()
