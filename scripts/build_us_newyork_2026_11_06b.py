"""Publish nyc_143 (Willow Oak of Herbert Street) from data/research/new-york-verified.json.

    python3 scripts/build_us_newyork_2026_11_06b.py

Writes into data/cities/new-york.json. Then preflight.py, commit by path.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "how_to_recognise",
               "verified_sources", "official_register", "access", "transport", "best_time",
               "photo", "location_precision", "pin_source", "curation_status", "paid_entry"]
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}
IDS = ["nyc_143"]


def main():
    path = os.path.join(ROOT, "data", "cities", "new-york.json")
    d = json.load(open(path))
    have = {t["id"] for t in d["trees"]}
    res = {t["id"]: t for t in json.load(open(os.path.join(ROOT, "data", "research", "new-york-verified.json")))
           if isinstance(t, dict) and t.get("id")}
    added = []
    for i in IDS:
        if i in have:
            continue
        t = res[i]
        if not t.get("story") or not t.get("how_to_recognise"):
            sys.exit(i + " has no story or recognition line")
        o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
        o["photo"] = dict(MISSING)
        o["curation_status"] = "ai_generated"
        d["trees"].append(o)
        added.append(i)
    with open(path, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("new-york added", len(added), "now", len(d["trees"]))


if __name__ == "__main__":
    main()
