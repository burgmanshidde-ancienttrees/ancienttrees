"""Build the US Pacific Northwest pass (verified and written 2026-11-03) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_us_northwest.py            # writes data/cities/<slug>.json
    python3 scripts/build_us_northwest.py --out DIR  # dry build elsewhere
    python3 scripts/build_us_northwest.py --remove   # deletes the three files again (test runs)
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/{tacoma,vancouver-washington,salem-oregon}-verified.json (trees with
stories) and data/research/us-northwest-places.json (place fields). Facts come from the City of
Tacoma and City of Vancouver Heritage Tree registers and the Oregon Heritage Tree programme,
cited per entry. Pins are approximate; every tree carries a recognition line instead.
Salem is two trees: tree pages, place page noindexed under four.
Portland (33/30) and Seattle (30/30) were full, so passcheck refused new trees there.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "data", "cities")

PLACES = ["tacoma", "vancouver-washington", "salem-oregon"]
STATES = {"tacoma": "Washington", "vancouver-washington": "Washington", "salem-oregon": "Oregon"}
STATES_FILE = os.path.join(ROOT, "data", "us-states.json")  # Contract L: the build fails on a US place missing here
PLACE_FIELDS = ["city", "country", "kind", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise",
               "location_precision", "curation_status", "verify_notes", "paid_entry"]


def tree(t):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["photo"] = {"url": None, "license": None, "attribution": None, "status": "missing"}
    o.setdefault("curation_status", "ai_generated")
    return o


def set_states(add):
    if not OUT.endswith(os.path.join("data", "cities")):
        return
    s = json.load(open(STATES_FILE))
    for slug, state in STATES.items():
        if add:
            s["places"][slug] = state
        else:
            s["places"].pop(slug, None)
    with open(STATES_FILE, "w") as f:
        json.dump(s, f, ensure_ascii=False, indent=1)  # the file's own format, no trailing newline


def main():
    if "--remove" in sys.argv:
        for slug in PLACES:
            path = os.path.join(OUT, slug + ".json")
            if os.path.exists(path):
                os.remove(path)
                print("removed", path)
        set_states(False)
        return
    places = json.load(open(os.path.join(R, "us-northwest-places.json")))
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
        d.setdefault("country", "United States")
        d.setdefault("status", "needs_curation")
        d["trees"] = ts
        d = {k: d[k] for k in PLACE_FIELDS + ["trees"] if k in d}
        with open(path, "w") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("wrote", path, len(ts), "tree(s)")
    set_states(True)


if __name__ == "__main__":
    main()
