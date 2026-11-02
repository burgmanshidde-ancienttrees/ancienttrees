"""Build the southern Thailand places (verified and written 2026-11-02) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_thailand_south.py            # writes data/cities/<slug>.json
    python3 scripts/build_thailand_south.py --out DIR  # dry build elsewhere
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/thailand-{gulf,andaman}-verified.json (trees with stories) and
data/research/thailand-south-places.json (place fields). Register: data/registers/thailand-rukkha.json.
Both are lone trees: tree pages, no place page in Google until a place reaches four.
Leads for the rest of the south: data/leads/thailand-south.json and thailand-south-gulf.json.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "data", "cities")

# research id -> (place slug, published id)
IDS = {
    "kpn_001": ("ko-pha-ngan", "kpn_001"),
    "trg_001": ("kantang", "ktg_001"),
}
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise",
               "photo", "photos", "location_precision", "curation_status", "verify_notes"]


def load_trees():
    out = {}
    for n in ["thailand-gulf", "thailand-andaman"]:
        d = json.load(open(os.path.join(R, n + "-verified.json")))
        for t in (d["trees"] if isinstance(d, dict) else d):
            out[t["id"]] = t
    return out


def tree(t, new_id):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["id"] = new_id
    o.setdefault("photo", {"url": None, "license": None, "attribution": None, "status": "missing"})
    o.setdefault("curation_status", "ai_generated")
    return o


def main():
    trees = load_trees()
    places = json.load(open(os.path.join(R, "thailand-south-places.json")))
    idmap = {k: v[1] for k, v in IDS.items()}
    by_place = {}
    for rid, (slug, new_id) in IDS.items():
        t = trees[rid]
        if t.get("hold"):
            print("HELD", rid, t["hold"])
            continue
        by_place.setdefault(slug, []).append(tree(t, new_id))
    os.makedirs(OUT, exist_ok=True)
    for slug, ts in by_place.items():
        path = os.path.join(OUT, slug + ".json")
        if os.path.exists(path) and OUT.endswith(os.path.join("data", "cities")):
            sys.exit(f"{path} exists; refusing to overwrite")
        p = places[slug]
        d = {k: p[k] for k in PLACE_FIELDS if k in p}
        d.setdefault("country", "Thailand")
        d.setdefault("status", "needs_curation")
        for k in ("hero_tree_id", "oldest_tree_id"):
            if d.get(k) in idmap:
                d[k] = idmap[d[k]]
        d["trees"] = ts
        d = {k: d[k] for k in PLACE_FIELDS + ["trees"] if k in d}
        json.dump(d, open(path, "w"), ensure_ascii=False, indent=2)
        open(path, "a").write("\n")
        print("wrote", path, len(ts), "tree(s)")


if __name__ == "__main__":
    main()
