"""Build the southern England pass (verified and written 2026-11-03) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_uk_south.py            # writes data/cities/<slug>.json
    python3 scripts/build_uk_south.py --out DIR  # dry build elsewhere (new places only)
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/<slug>-verified.json (trees with stories) and
data/research/uk-south-places.json (place fields). A live place (Oxford, Cambridge)
gets its new trees appended and, when the places file gives them, a grown intro and
meta_description; a new place is created whole and refuses to overwrite.
A tree marked "hold" or without a story stays out. Woodland Trust inventory never used.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "data", "cities")

PLACE_FIELDS = ["city", "country", "kind", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
GROWS = ["intro", "meta_description", "question_answer", "question_context", "oldest_tree_id"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise",
               "photo", "photos", "location_precision", "curation_status", "verify_notes", "paid_entry"]
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}


def tree(t):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    if not t.get("how_to_recognise") and t.get("recognise"):
        o["how_to_recognise"] = t["recognise"]
    ph = o.get("photo") or {}
    if ph.get("status") != "approved":
        o["photo"] = dict(MISSING)
    o.setdefault("curation_status", "ai_generated")
    return {k: o[k] for k in TREE_FIELDS if k in o}


def main():
    places = json.load(open(os.path.join(R, "uk-south-places.json")))
    os.makedirs(OUT, exist_ok=True)
    for slug, p in places.items():
        if slug.startswith("_"):
            continue
        src = os.path.join(R, slug + "-verified.json")
        if not os.path.exists(src):
            print("SKIP", slug, "no verified file")
            continue
        ts = []
        for t in json.load(open(src)):
            if t.get("hold") or not t.get("story"):
                print("HELD", t.get("id"), t.get("hold") or "no story")
                continue
            ts.append(tree(t))
        if not ts:
            print("SKIP", slug, "nothing written")
            continue
        path = os.path.join(OUT, slug + ".json")
        live = os.path.join(ROOT, "data", "cities", slug + ".json")
        if os.path.exists(live):
            d = json.load(open(live))
            have = {t["id"] for t in d["trees"]}
            new = [t for t in ts if t["id"] not in have]
            d["trees"].extend(new)
            for k in GROWS:
                if p.get(k):
                    d[k] = p[k]
            print("grew", slug, "+%d" % len(new), "->", len(d["trees"]))
        else:
            d = {k: p[k] for k in PLACE_FIELDS if k in p}
            d.setdefault("country", "United Kingdom")
            d.setdefault("status", "needs_curation")
            d["trees"] = ts
            d = {k: d[k] for k in PLACE_FIELDS + ["trees"] if k in d}
            print("new", slug, len(ts), "tree(s)")
        with open(path, "w") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")


if __name__ == "__main__":
    main()
