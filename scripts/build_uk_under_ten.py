"""Build the UK under-ten pass (verified 2026-11-04, written 2026-11-09) into data/cities.

Hidde's bar of 2026-11-04: every ranked UK city at ten trees. This pass adds two elms and a
yew to Brighton (bhm_007 to bhm_009), the Eastham Yew to Liverpool, the Bute Park Tulip
Tree to Cardiff, and starts Windsor with the Signing Oak. Four more Cardiff trees from the same
verify pass went live with the night run of 2026-11-06. York, Stratford-upon-Avon and a further
Windsor angle found nothing that ships (data/leads/, data/research/*-notes*).

New trees are app-only under APP FIRST (findable.py), so the live place text of Brighton,
Liverpool and Cardiff stays as it is: those web pages keep showing the trees they show.

    python3 scripts/build_uk_under_ten.py            # appends to the city files, writes Windsor
    python3 scripts/build_uk_under_ten.py --out DIR  # dry build elsewhere
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/brighton-verified-2.json (a night run emptied brighton-verified.json on
2026-11-06), liverpool-, cardiff- and windsor-verified.json, Windsor's place fields in
data/research/uk-under-ten-places.json, photo verdicts in data/research/uk-under-ten-photos.json
(only `approved` ever ships). Woodland Trust Ancient Tree Inventory not used.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES

# slug: (research file, tree ids taken from it)
SOURCES = {
    "brighton": ("brighton-verified-2.json", ["bhm_007", "bhm_008", "bhm_009"]),
    "liverpool": ("liverpool-verified.json", ["lvp_004"]),
    "cardiff": ("cardiff-verified.json", ["crd_010"]),
    "windsor": ("windsor-verified.json", ["wsr_001"]),
}
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise",
               "location_precision", "pin_source", "curation_status", "verify_notes", "photo", "paid_entry"]
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}


def tree(t, photos):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["verified_sources"] = [s if isinstance(s, str) else s.get("url") for s in o.get("verified_sources", [])]
    p = photos.get(o["id"])
    o["photo"] = {**p, "status": "approved"} if p else dict(MISSING)
    o["photo"].pop("why", None)
    o.setdefault("curation_status", "ai_generated")
    if len(o["name"]) >= 60:
        sys.exit(f"{o['id']}: name over 60 characters")
    if not o.get("story"):
        sys.exit(f"{o['id']} has no story; refusing to build")
    if not (o["photo"].get("url") or o.get("location_precision") == "confirmed" or o.get("how_to_recognise")):
        sys.exit(f"{o['id']}: no photo, confirmed pin or recognition line")
    if "—" in json.dumps(o, ensure_ascii=False):
        sys.exit(f"{o['id']}: em dash")
    return o


def main():
    places = json.load(open(os.path.join(R, "uk-under-ten-places.json")))
    photos = json.load(open(os.path.join(R, "uk-under-ten-photos.json")))["approved"]
    os.makedirs(OUT, exist_ok=True)
    for slug, (src, ids) in SOURCES.items():
        rows = {t["id"]: t for t in json.load(open(os.path.join(R, src))) if isinstance(t, dict)}
        for i in ids:
            if i not in rows:
                sys.exit(f"{slug}: {i} not in {src}")
        ts = [tree(rows[i], photos) for i in ids]
        live = os.path.join(CITIES, slug + ".json")
        path = os.path.join(OUT, slug + ".json")
        if os.path.exists(live):
            d = json.load(open(live))
            mine = {x["id"] for x in ts}
            d["trees"] = [x for x in d["trees"] if x["id"] not in mine] + ts
        else:
            p = places.get(slug)
            if not p:
                sys.exit(f"{slug}: new place without place fields")
            d = {**{k: p[k] for k in PLACE_FIELDS if k in p}, "trees": ts}
        with open(path, "w") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("wrote", path, len(d["trees"]), "tree(s),", len(ts), "from this pass")


if __name__ == "__main__":
    main()
