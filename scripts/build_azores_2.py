"""Build the second Azores pass (verified and written 2026-11-02) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_azores_2.py            # appends azo_004..azo_007 to azores.json, writes angra-do-heroismo.json
    python3 scripts/build_azores_2.py --out DIR  # dry build elsewhere
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/azores-sm-verified.json (São Miguel, joins the live `azores` place,
which already covers Ponta Delgada and Furnas), data/research/angra-do-heroismo-verified.json
(Terceira, its own place: 150 km from São Miguel, so one walk cannot hold both) and
data/research/azores-2-places.json (place fields for both, rewritten to cover the new trees).
Angra has two trees, so its place page stays out of Google until it reaches four;
the trees go live as tree pages.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES

SOURCES = {
    "azores": "azores-sm-verified.json",
    "angra-do-heroismo": "angra-do-heroismo-verified.json",
}
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise",
               "location_precision", "curation_status", "verify_notes", "photo", "paid_entry"]
PAID = {"azo_006"}  # Mata-Jardim José do Canto, ticketed garden
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}


def tree(t):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["verified_sources"] = [s if isinstance(s, str) else s.get("url") for s in o.get("verified_sources", [])]
    p = o.get("photo") or {}
    # a held photo never ships; the tree goes out photo-less
    o["photo"] = {k: v for k, v in p.items() if v is not None} if p.get("status") == "approved" else dict(MISSING)
    o.setdefault("curation_status", "ai_generated")
    if o["id"] in PAID:
        o["paid_entry"] = True
    return o


def main():
    places = json.load(open(os.path.join(R, "azores-2-places.json")))
    os.makedirs(OUT, exist_ok=True)
    for slug, src in SOURCES.items():
        ts = [tree(t) for t in json.load(open(os.path.join(R, src))) if not t.get("hold")]
        for t in ts:
            if not t.get("story"):
                sys.exit(f"{t['id']} has no story; refusing to build")
        live = os.path.join(CITIES, slug + ".json")
        path = os.path.join(OUT, slug + ".json")
        p = places[slug]
        if os.path.exists(live):
            d = json.load(open(live))
            have = {x["id"] for x in d["trees"]}
            trees = d["trees"] + [x for x in ts if x["id"] not in have]
            d.update({k: p[k] for k in PLACE_FIELDS if k in p})
        else:
            d = {k: p[k] for k in PLACE_FIELDS if k in p}
            trees = ts
        d.setdefault("country", "Portugal")
        d.setdefault("status", "needs_curation")
        ids = {x["id"] for x in trees}
        for k in ("hero_tree_id", "oldest_tree_id"):
            if d.get(k) not in ids:
                sys.exit(f"{slug}: {k} {d.get(k)} is not one of its trees")
        d["trees"] = trees
        rest = {k: v for k, v in d.items() if k not in PLACE_FIELDS + ["trees"]}
        d = {**{k: d[k] for k in PLACE_FIELDS if k in d}, **rest, "trees": trees}
        json.dump(d, open(path, "w"), ensure_ascii=False, indent=2)
        open(path, "a").write("\n")
        print("wrote", path, len(trees), "tree(s),", len(ts), "from this pass")


if __name__ == "__main__":
    main()
