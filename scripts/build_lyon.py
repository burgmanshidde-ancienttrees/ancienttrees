"""Grow Lyon with the trees verified and written on 2026-11-02 (Hidde: Lyon run).

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_lyon.py            # appends lyo_015.. to data/cities/lyon.json, updates the place text
    python3 scripts/build_lyon.py --out DIR  # dry build elsewhere
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/lyon-verified.json (lyo_015 to lyo_025: ten measured giants from the
Metropole's surveyed street-tree inventory plus the Villevert cedars, PLU-H rows 4150/4151,
all confirmed pins), data/research/lyon-verified-2.json (lyo_026 to lyo_035: PLU-H register
trees on public ground, approximate pins, findable by their recognition line) and
data/research/lyon-place.json (intro, meta, question fields, faq, hero and oldest).
None has a photograph yet, so each carries the googlebot noindex until a reader adds to it.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
SRC = os.path.join(ROOT, "data", "cities", "lyon.json")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "data", "cities")

PLACE_FIELDS = ["intro", "meta_description", "question_meta", "question_answer", "question_context",
                "faq", "hero_tree_id", "oldest_tree_id"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise",
               "location_precision", "pin_source", "curation_status", "verify_notes"]
PLACE_ORDER = ["city", "country", "status", "intro", "meta_description", "question_answer",
               "question_meta", "question_context", "hero_tree_id", "oldest_tree_id", "faq", "trees"]


def tree(t):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["verified_sources"] = [s for s in o.get("verified_sources", []) if isinstance(s, str) and s.startswith("http")]
    o["photo"] = {"url": None, "license": None, "attribution": None, "status": "missing"}
    o.setdefault("curation_status", "flagged")
    return o


def main():
    new = json.load(open(os.path.join(R, "lyon-verified.json")))
    new += json.load(open(os.path.join(R, "lyon-verified-2.json")))
    place = json.load(open(os.path.join(R, "lyon-place.json")))
    d = json.load(open(SRC))
    have = {t["id"] for t in d["trees"]}
    names = {t["name"] for t in d["trees"]}
    added = []
    for t in new:
        if t.get("hold"):
            print("HELD", t["id"], t["hold"])
            continue
        if t["id"] in have or t["name"] in names:
            print("SKIP already live", t["id"], t["name"])
            continue
        if not t.get("story"):
            sys.exit(f"{t['id']} has no story; the writing pass is not finished")
        added.append(tree(t))
    # Lyon has a French overlay; preflight refuses the whole deploy when it misses a tree.
    fr_path = os.path.join(ROOT, "data", "i18n", "fr", "lyon.json")
    fr = json.load(open(fr_path))
    fr_new = json.load(open(os.path.join(R, "lyon-fr-overlay.json")))
    missing = [t["id"] for t in added if t["id"] not in fr_new["trees"] and t["id"] not in fr["trees"]]
    if missing:
        sys.exit(f"lyon-fr-overlay.json lacks {missing}: translate them before building")
    for t in added:
        fr["trees"].setdefault(t["id"], fr_new["trees"][t["id"]])
    for k, v in fr_new["place"].items():
        if v:
            fr[k] = v
    d["trees"] += added
    for k in PLACE_FIELDS:
        if place.get(k):
            d[k] = place[k]
    ids = {t["id"] for t in d["trees"]}
    for k in ("hero_tree_id", "oldest_tree_id"):
        if d.get(k) and d[k] not in ids:
            sys.exit(f"{k} {d[k]} is not a Lyon tree")
    d = {k: d[k] for k in PLACE_ORDER if k in d} | {k: v for k, v in d.items() if k not in PLACE_ORDER}
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "lyon.json")
    with open(path, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")
    fr_out = fr_path if "--out" not in sys.argv else os.path.join(OUT, "fr-lyon.json")
    with open(fr_out, "w") as f:
        json.dump(fr, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote", fr_out)
    print("wrote", path, len(added), "new tree(s),", len(d["trees"]), "in all")


if __name__ == "__main__":
    main()
