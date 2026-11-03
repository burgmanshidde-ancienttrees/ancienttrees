"""Build the London pass (verified and written 2026-11-03) into data/cities/london.json.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_uk_london.py            # appends to data/cities/london.json
    python3 scripts/build_uk_london.py --out DIR  # dry build elsewhere
    python3 scripts/build_uk_london.py --max 25   # only the first 25 new trees (the pace)
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/london-verified.json (every London tree ever written; only
ids not yet live are taken) and data/research/london-place.json (the grown intro,
meta_description, faq). A tree marked "hold" or without a story stays out.
Woodland Trust inventory never used.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
LIVE = os.path.join(ROOT, "data", "cities", "london.json")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "data", "cities")
MAX = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else None

GROWS = ["intro", "meta_description", "question_answer", "question_meta", "question_context", "faq"]
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
    d = json.load(open(LIVE))
    have = {t["id"] for t in d["trees"]}
    new = []
    for t in json.load(open(os.path.join(R, "london-verified.json"))):
        if t.get("id") in have:
            continue
        if t.get("hold") or not t.get("story"):
            print("HELD", t.get("id"), t.get("hold") or "no story")
            continue
        new.append(tree(t))
    if MAX is not None:
        new = new[:MAX]
    if not new:
        print("nothing new to add")
        return
    d["trees"].extend(new)
    place = os.path.join(R, "london-place.json")
    if os.path.exists(place):
        p = json.load(open(place))
        for k in GROWS:
            if p.get(k):
                d[k] = p[k]
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "london.json"), "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("grew london +%d -> %d" % (len(new), len(d["trees"])))


if __name__ == "__main__":
    main()
