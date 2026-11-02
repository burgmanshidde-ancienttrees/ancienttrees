"""Build the northern Thailand places (verified and written 2026-11-02) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_thailand_north.py            # writes data/cities/<slug>.json
    python3 scripts/build_thailand_north.py --out DIR  # dry build elsewhere
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/<slug>-verified.json (trees with stories) and
data/research/northern-thailand-places.json (place fields). The run from the
Ministry of Culture heritage-tree register (data/registers/thailand-rukkha.json)
yielded one tree: the khajao at Wat Phra That Lampang Luang, a lone tree page
(Lampang stays under four, so its place page stays out of Google). Nan, Phrae,
Mae Hong Son, Lamphun and Chiang Rai found nothing that cleared the bar; their
rows wait in data/leads/.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "data", "cities")

PLACES = ["lampang"]
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise",
               "location_precision", "curation_status", "verify_notes"]


def tree(t):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["photo"] = {"url": None, "license": None, "attribution": None, "status": "missing"}
    o.setdefault("curation_status", "ai_generated")
    return o


def main():
    places = json.load(open(os.path.join(R, "northern-thailand-places.json")))
    os.makedirs(OUT, exist_ok=True)
    for slug in PLACES:
        ts = [tree(t) for t in json.load(open(os.path.join(R, slug + "-verified.json")))
              if t.get("story") and not t.get("hold")]
        if not ts:
            print("nothing to build for", slug)
            continue
        path = os.path.join(OUT, slug + ".json")
        if os.path.exists(path) and OUT.endswith(os.path.join("data", "cities")):
            sys.exit(f"{path} exists; refusing to overwrite")
        p = places[slug]
        d = {k: p[k] for k in PLACE_FIELDS if k in p}
        d.setdefault("country", "Thailand")
        d.setdefault("status", "needs_curation")
        d["trees"] = ts
        json.dump(d, open(path, "w"), ensure_ascii=False, indent=2)
        open(path, "a").write("\n")
        print("wrote", path, len(ts), "tree(s)")


if __name__ == "__main__":
    main()
