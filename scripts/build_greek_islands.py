"""Build the Greek islands (verified and written 2026-11-02) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_greek_islands.py            # writes data/cities/<slug>.json
    python3 scripts/build_greek_islands.py --out DIR  # dry build elsewhere
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/{corfu,kefalonia,paros}-verified.json (trees with stories) and
data/research/greek-islands-places.json (place fields). Most facts come from the Greek
Tree Registry of the Friends of Hellenic National Parks (data/research/greek-tree-registry-filoiparkon.json),
cited per entry; it is not an open licence, so no text or photographs of theirs.
Kefalonia and Paros are one tree each: tree pages, place page noindexed under four.
Rhodes and Kos gave no new tree this run (data/leads/rhodes.json, data/leads/kos.json).
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "data", "cities")

PLACES = ["corfu", "kefalonia", "paros"]
PLACE_FIELDS = ["city", "country", "kind", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise",
               "location_precision", "curation_status", "verify_notes", "paid_entry"]
PAID = {"pao_001"}  # Butterflies Nature Reserve, ticketed June to September


def tree(t):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["photo"] = {"url": None, "license": None, "attribution": None, "status": "missing"}
    o.setdefault("curation_status", "ai_generated")
    if o["id"] in PAID:
        o["paid_entry"] = True
    return o


def main():
    places = json.load(open(os.path.join(R, "greek-islands-places.json")))
    os.makedirs(OUT, exist_ok=True)
    for slug in PLACES:
        ts = []
        for t in json.load(open(os.path.join(R, slug + "-verified.json"))):
            if t.get("hold") or t.get("fold_into"):
                print("HELD", t["id"], t.get("hold") or "folded into " + t["fold_into"])
                continue
            if not t.get("story"):
                sys.exit(f"{t['id']} has no story")
            ts.append(tree(t))
        path = os.path.join(OUT, slug + ".json")
        if os.path.exists(path) and OUT.endswith(os.path.join("data", "cities")):
            sys.exit(f"{path} exists; refusing to overwrite")
        p = places[slug]
        d = {k: p[k] for k in PLACE_FIELDS if k in p}
        d.setdefault("country", "Greece")
        d.setdefault("status", "needs_curation")
        d["trees"] = ts
        d = {k: d[k] for k in PLACE_FIELDS + ["trees"] if k in d}
        with open(path, "w") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("wrote", path, len(ts), "tree(s)")


if __name__ == "__main__":
    main()
