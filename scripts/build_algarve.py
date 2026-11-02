"""Build the Algarve trees (verified and written 2026-11-02) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_algarve.py            # writes data/cities/tavira.json, adds mnq_004 to monchique.json
    python3 scripts/build_algarve.py --out DIR  # dry build elsewhere (monchique read from data/cities)
then city_names.py, preflight.py, commit by path, push.

Source: data/research/algarve-verified.json (trees with stories, place copy).
Tavira is new with one tree (no place page until four). Monchique goes from three
trees to four, so its intro, meta, question fields and FAQ answer are replaced
with the four-tree versions.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "research", "algarve-verified.json")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES

PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "how_to_recognise",
               "verified_sources", "official_register", "access", "transport", "best_time",
               "photo", "location_precision", "pin_source", "curation_status"]
REPLACE = ["intro", "meta_description", "question_meta", "question_answer", "question_context"]


def tree(t):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o.setdefault("photo", {"url": None, "license": None, "attribution": None, "status": "missing"})
    o.setdefault("curation_status", "ai_generated")
    return o


def write(path, d):
    with open(path, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    src = json.load(open(SRC))
    places = src["places"]
    by_place = {}
    for t in src["trees"]:
        by_place.setdefault(t["place"], []).append(tree(t))
    os.makedirs(OUT, exist_ok=True)
    for slug, ts in by_place.items():
        path = os.path.join(OUT, slug + ".json")
        live = os.path.join(CITIES, slug + ".json")
        p = places[slug]
        if os.path.exists(live):
            d = json.load(open(live))
            have = {x["id"] for x in d["trees"]}
            new = [x for x in ts if x["id"] not in have]
            if not new:
                print("already in", live)
                continue
            d["trees"] += new
            for k in REPLACE:
                if k in p:
                    d[k] = p[k]
            for f in d.get("faq", []):
                if f["q"] in p.get("faq_replace", {}):
                    f["a"] = p["faq_replace"][f["q"]]
        else:
            d = {k: p[k] for k in PLACE_FIELDS if k in p}
            d.setdefault("country", "Portugal")
            d.setdefault("status", "needs_curation")
            d["trees"] = ts
        write(path, d)
        print("wrote", path, len(d["trees"]), "tree(s)")


if __name__ == "__main__":
    main()
