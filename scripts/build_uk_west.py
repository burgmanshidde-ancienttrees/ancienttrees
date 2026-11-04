"""Build the West of England pass (verified and written 2026-11-04) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_uk_west.py               # writes data/cities/<slug>.json
    python3 scripts/build_uk_west.py --only bath   # one place (repeatable: --only bath --only wells)
    python3 scripts/build_uk_west.py --max 12      # at most N new trees in all, places in file order
    python3 scripts/build_uk_west.py --out DIR     # dry build elsewhere
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/<slug>-verified.json (trees with stories), or the file a place
names in "source" (the Somerset and Dorset yews share one file, each yew carrying
place.slug), and data/research/uk-west-places-a.json and -b.json (place fields, one
per writing pass). A live place (Bath,
Bristol, Glastonbury) gets its new trees appended and, when the places file gives them,
a grown intro and meta; a new place is created whole. A tree marked "hold" or without a
story stays out. Woodland Trust inventory never used.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "data", "cities")
ONLY = [sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--only"]
MAX = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else None

PLACE_FIELDS = ["city", "country", "kind", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
GROWS = ["intro", "meta_description", "question_meta", "question_answer", "question_context",
         "hero_tree_id", "oldest_tree_id", "faq"]
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


def trees_for(slug, p):
    src = os.path.join(R, p.get("source") or slug + "-verified.json")
    if not os.path.exists(src):
        return None
    out = []
    for t in json.load(open(src)):
        if t.get("place") and t["place"].get("slug") != slug:
            continue
        if t.get("hold") or not t.get("story"):
            print("HELD", t.get("id"), t.get("hold") or "no story")
            continue
        out.append(tree(t))
    return out


def main():
    places = {}
    for name in ("uk-west-places-a.json", "uk-west-places-b.json"):
        places.update(json.load(open(os.path.join(R, name))))
    os.makedirs(OUT, exist_ok=True)
    left = MAX
    for slug, p in places.items():
        if slug.startswith("_") or (ONLY and slug not in ONLY):
            continue
        ts = trees_for(slug, p)
        if ts is None:
            print("SKIP", slug, "no verified file")
            continue
        live = os.path.join(ROOT, "data", "cities", slug + ".json")
        if os.path.exists(live):
            d = json.load(open(live))
            have = {t["id"] for t in d["trees"]}
            new = [t for t in ts if t["id"] not in have]
        else:
            d, new = None, ts
        if left is not None:
            new = new[:max(left, 0)]
            left -= len(new)
        if not new:
            print("SKIP", slug, "nothing new")
            continue
        if d is not None:
            d["trees"].extend(new)
            for k in GROWS:
                if p.get(k):
                    d[k] = p[k]
            print("grew", slug, "+%d" % len(new), "->", len(d["trees"]))
        else:
            d = {k: p[k] for k in PLACE_FIELDS if k in p}
            d.setdefault("country", "United Kingdom")
            d.setdefault("status", "needs_curation")
            d["trees"] = new
            d = {k: d[k] for k in PLACE_FIELDS + ["trees"] if k in d}
            print("new", slug, len(new), "tree(s)")
        with open(os.path.join(OUT, slug + ".json"), "w") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")


if __name__ == "__main__":
    main()
