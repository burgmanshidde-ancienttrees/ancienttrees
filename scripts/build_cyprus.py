"""Build the Cyprus run (verified and written 2026-11-02) into data/cities/cyprus.json.

Held for the 25-a-day pace when written. The eleven trees join the live Cyprus
island page (cyp_001 to cyp_004) as cyp_005 to cyp_015: no town reached four
trees on its own, and trees into an existing place beat new places. The place
fields are rewritten for fifteen trees. The session that publishes runs:
    python3 scripts/build_cyprus.py            # updates data/cities/cyprus.json
    python3 scripts/build_cyprus.py --out DIR  # dry build elsewhere
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/cyprus-verified.json (stories and place fields, written
from data/research/cyprus-{larnaca,limassol,troodos,paphos}-verified.json) and
data/research/cyprus-photos.json (four Commons photographs, pixels viewed
2026-11-02). Register: data/registers/cyprus-forests.json.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
SRC = os.path.join(ROOT, "data", "cities", "cyprus.json")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "data", "cities")

PLACE_FIELDS = ["intro", "meta_description", "question_meta", "question_answer",
                "question_context", "faq", "hero_tree_id", "oldest_tree_id"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise",
               "location_precision", "pin_source", "curation_status", "notes"]
# tree id -> key in cyprus-photos.json
PHOTOS = {"cyp_006": "cape_greco_juniper", "cyp_011": "giant_black_pine",
          "cyp_013": "agia_solomoni", "cyp_014": "aphrodite_oak"}
# canonical names where the writing pass chose a less common one
SPECIES = {"Black Pine (Pinus nigra subsp. pallasiana)": "Crimean Pine (Pinus nigra subsp. pallasiana)"}
PHOTO_KEYS = ["url", "license", "attribution", "attribution_url", "status", "width", "height", "taken_month"]


def tree(t, photos):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["species"] = SPECIES.get(o["species"], o["species"])
    p = photos.get(PHOTOS.get(t["id"]))
    if p:
        o["photo"] = {k: p[k] for k in PHOTO_KEYS if p.get(k) is not None}
    else:
        o["photo"] = {"url": None, "license": None, "attribution": None, "status": "missing"}
    o.setdefault("curation_status", "ai_generated")
    return o


def main():
    w = json.load(open(os.path.join(R, "cyprus-verified.json")))
    photos = json.load(open(os.path.join(R, "cyprus-photos.json")))
    d = json.load(open(SRC))
    have = {x["id"] for x in d["trees"]}
    new = [tree(t, photos) for t in w["trees"] if t["id"] not in have]
    if len(new) != len(w["trees"]):
        print("already in cyprus.json:", sorted(have & {t["id"] for t in w["trees"]}))
    for k in PLACE_FIELDS:
        if w["place"].get(k):
            d[k] = w["place"][k]
    trees = d.pop("trees") + new
    d["trees"] = trees
    ids = {x["id"] for x in trees}
    for k in ("hero_tree_id", "oldest_tree_id"):
        assert d.get(k) in ids, (k, d.get(k))
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "cyprus.json")
    with open(path, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("wrote", path, len(new), "new tree(s),", len(trees), "in all,",
          sum(1 for x in new if x["photo"].get("status") == "approved"), "with a photograph")


if __name__ == "__main__":
    main()
