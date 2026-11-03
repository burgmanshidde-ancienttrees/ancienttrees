"""Build the Tenerife trees (verified and written 2026-11-02/03) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_tenerife.py            # writes data/cities/santa-cruz-de-tenerife.json, appends to tenerife.json
    python3 scripts/build_tenerife.py --out DIR  # dry build elsewhere
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/santa-cruz-de-tenerife-verified.json (sct_*, a walk in the capital,
from the Santa Cruz municipal register, CC BY), data/research/tenerife-verified.json
(tfe_005 onward, from the Cabildo's catalogue, CC0) and data/research/tenerife-places.json
(place fields for both). Santa Cruz is its own place: nine trees inside about two kilometres,
some 30 km from the island page's other stops. The island page keeps its trees and grows.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES

PLACE_FIELDS = ["city", "country", "status", "kind", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "paid_entry", "best_time", "how_to_recognise",
               "photo", "location_precision", "pin_source", "curation_status", "verify_notes"]
PHOTO_FIELDS = ["url", "license", "attribution", "attribution_url", "status"]


def tree(t):
    t = dict(t)
    if t.get("recognise") and not t.get("how_to_recognise"):
        t["how_to_recognise"] = t["recognise"]
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    p = t.get("photo") or {}
    if p.get("status") == "approved" and p.get("url"):
        o["photo"] = {k: p[k] for k in PHOTO_FIELDS if p.get(k)}
    else:
        o["photo"] = {"url": None, "license": None, "attribution": None, "status": "missing"}
    if isinstance(o.get("verify_notes"), (list, dict)):
        o["verify_notes"] = json.dumps(o["verify_notes"], ensure_ascii=False)
    o.setdefault("curation_status", "ai_generated")
    return o


def load(name):
    d = json.load(open(os.path.join(R, name)))
    ts = d["trees"] if isinstance(d, dict) else d
    out = []
    for t in ts:
        if t.get("hold"):
            print("HELD", t["id"], t["hold"])
            continue
        if not t.get("story"):
            print("NO STORY, skipped", t["id"])
            continue
        out.append(tree(t))
    return out


def write(path, d):
    json.dump(d, open(path, "w"), ensure_ascii=False, indent=2)
    open(path, "a").write("\n")


def main():
    places = json.load(open(os.path.join(R, "tenerife-places.json")))
    os.makedirs(OUT, exist_ok=True)

    # Santa Cruz de Tenerife: a new place
    sct = load("santa-cruz-de-tenerife-verified.json")
    path = os.path.join(OUT, "santa-cruz-de-tenerife.json")
    if os.path.exists(path) and os.path.abspath(OUT) == os.path.abspath(CITIES):
        sys.exit(f"{path} exists; refusing to overwrite")
    p = dict(places["santa-cruz-de-tenerife"])
    p.setdefault("city", "Santa Cruz de Tenerife")
    p.setdefault("country", "Spain")
    p["status"] = "needs_curation"
    if p.get("kind") == "city":
        del p["kind"]  # only islands carry a kind
    d = {k: p[k] for k in PLACE_FIELDS if k in p}
    d["trees"] = sct
    write(path, d)
    print("wrote", path, len(sct), "tree(s)")

    # Tenerife: append and rewrite the place text
    tfe = load("tenerife-verified.json")
    d = json.load(open(os.path.join(CITIES, "tenerife.json")))
    have = {x["id"] for x in d["trees"]}
    new = [x for x in tfe if x["id"] not in have]
    d["trees"] += new
    for k, v in places["tenerife"].items():
        if k in PLACE_FIELDS and k not in ("city", "country", "status", "kind"):
            d[k] = v
    path = os.path.join(OUT, "tenerife.json")
    write(path, d)
    print("wrote", path, "+%d tree(s), %d in all" % (len(new), len(d["trees"])))

    # The Spanish overlay must cover every tree, or the whole build is refused
    es = json.load(open(os.path.join(R, "tenerife-es.json")))
    src = os.path.join(ROOT, "data", "i18n", "es", "tenerife.json")
    o = json.load(open(src))
    o.update(es["place"])
    for tid, tr in es["trees"].items():
        o["trees"].setdefault(tid, tr)
    if os.path.abspath(OUT) == os.path.abspath(CITIES):
        path = src
    else:
        path = os.path.join(OUT, "es-tenerife.json")
    write(path, o)
    print("wrote", path, len(o["trees"]), "tree(s) in Spanish")


if __name__ == "__main__":
    main()
