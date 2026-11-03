"""Build the Hawaii trees (verified and written 2026-11-02/03) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_us_hawaii.py            # appends to oahu, kauai, maui, hilo, hawaii
    python3 scripts/build_us_hawaii.py --out DIR  # dry build elsewhere (live places read from data/cities)
then city_names.py, preflight.py, commit by path, push.

Sources in data/research/: oahu-verified.json (hnl_022..032; 024 and 032 carry "hold"),
kauai-verified.json (kau_007..009), maui-verified.json (mau_005), hilo-verified.json
(hbi_007..009, Banyan Drive), hawaii-verified.json (haw_007..008, Kailua-Kona). Place copy
in us-hawaii-places.json. All five places are live, so their intro, meta and question
fields are replaced and new FAQ items appended. No photographs this pass: every tree
ships on its recognition line with an honest approximate pin.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES

SOURCES = [
    ("oahu-verified.json", "oahu"),
    ("kauai-verified.json", "kauai"),
    ("maui-verified.json", "maui"),
    ("hilo-verified.json", "hilo"),
    ("hawaii-verified.json", "hawaii"),
]
REPLACE = ["intro", "meta_description", "question_meta", "question_answer", "question_context",
           "hero_tree_id", "oldest_tree_id"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "how_to_recognise",
               "verified_sources", "official_register", "access", "transport", "best_time",
               "photo", "location_precision", "pin_source", "curation_status", "verify_notes",
               "paid_entry"]
PAID = {"kau_007"}  # Allerton Garden, guided tour only
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}


def tree(t):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    if not o.get("how_to_recognise") and t.get("recognise"):
        o["how_to_recognise"] = t["recognise"]
    o["verified_sources"] = [s if isinstance(s, str) else s.get("url") for s in o.get("verified_sources", [])]
    if isinstance(o.get("verify_notes"), list):
        o["verify_notes"] = " ".join(o["verify_notes"])
    o["photo"] = dict(MISSING)
    o.setdefault("location_precision", "approximate")
    o.setdefault("curation_status", "flagged")
    if o["id"] in PAID:
        o["paid_entry"] = True
    return o


def write(path, d):
    with open(path, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    places = json.load(open(os.path.join(R, "us-hawaii-places.json")))
    os.makedirs(OUT, exist_ok=True)
    for src, slug in SOURCES:
        ts = []
        for t in json.load(open(os.path.join(R, src))):
            if t.get("hold"):
                continue
            if not t.get("story"):
                sys.exit(f"{t['id']} has no story; refusing to build")
            ts.append(tree(t))
        d = json.load(open(os.path.join(CITIES, slug + ".json")))
        have = {x["id"] for x in d["trees"]}
        new = [x for x in ts if x["id"] not in have]
        if not new:
            print("already in", slug)
            continue
        d["trees"] += new
        p = places.get(slug, {})
        for k in REPLACE:
            if p.get(k):
                d[k] = p[k]
        fix = {f["q"]: f for f in p.get("faq_replace") or []}
        done = set()
        for f in d.get("faq", []):
            if f["q"] in fix:
                done.add(f["q"])
                f["a"] = fix[f["q"]]["a"]
                f["q"] = fix[f["q"]].get("new_q", f["q"])
        missed = set(fix) - done
        if missed:
            sys.exit(f"{slug}: faq_replace names questions the page does not ask: {missed}")
        asked = {f["q"] for f in d.get("faq", [])}
        d.setdefault("faq", []).extend(f for f in p.get("faq_add", []) if f["q"] not in asked)
        ids = {x["id"] for x in d["trees"]}
        for k in ("hero_tree_id", "oldest_tree_id"):
            if d.get(k) and d[k] not in ids:
                sys.exit(f"{slug}: {k} {d[k]} is not one of its trees")
        write(os.path.join(OUT, slug + ".json"), d)
        print("wrote", slug, len(d["trees"]), "tree(s),", len(new), "from this pass")


if __name__ == "__main__":
    main()
