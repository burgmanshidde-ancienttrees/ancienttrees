"""Build the Croatian coast places (verified and written 2026-11-02) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_croatia_coast.py            # writes data/cities/<slug>.json, adds Solin to split.json
    python3 scripts/build_croatia_coast.py --out DIR  # dry build elsewhere
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/croatia-{istria-kvarner,central-dalmatia,south-dalmatia}-verified.json
(trees with stories) and data/research/croatia-coast-places.json (place fields).
Kaštela waits: its olive (cdl_001) carries hold "access unproven" and the place text
is written around it; the oak (cdl_002) goes with it once the olive is settled.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "data", "cities")

# research id -> (place slug, published id)
IDS = {
    "pul_001": ("pula", "pul_001"),
    "pul_002": ("pula", "pul_002"),
    "rab_001": ("rab", "rab_001"),
    "lun_001": ("lun", "lun_001"),
    "cdl_003": ("split", "spl_005"),
    "cdl_004": ("zadar", "zdr_001"),
    "cdl_005": ("brac", "brh_001"),
    "hrv_001": ("hvar", "hvr_001"),
    "hrv_002": ("cara", "car_001"),
    "hrv_003": ("orebic", "orb_001"),
}
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise",
               "location_precision", "curation_status", "verify_notes"]


def load_trees():
    out = {}
    for n in ["croatia-istria-kvarner", "croatia-central-dalmatia", "croatia-south-dalmatia"]:
        d = json.load(open(os.path.join(R, n + "-verified.json")))
        for t in (d["trees"] if isinstance(d, dict) else d):
            out[t["id"]] = t
    return out


def tree(t, new_id):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["id"] = new_id
    reg = o.get("official_register")
    if isinstance(reg, dict) and reg.get("url") and " (" in reg["url"]:
        url, rest = reg["url"].split(" (", 1)
        reg = dict(reg, url=url)
        reg["name"] = reg["name"] + " (" + rest
        o["official_register"] = reg
    o["photo"] = {"url": None, "license": None, "attribution": None, "status": "missing"}
    o.setdefault("curation_status", "ai_generated")
    return o


def main():
    trees = load_trees()
    places = json.load(open(os.path.join(R, "croatia-coast-places.json")))
    idmap = {k: v[1] for k, v in IDS.items()}
    by_place = {}
    for rid, (slug, new_id) in IDS.items():
        t = trees[rid]
        if t.get("hold"):
            print("HELD", rid, t["hold"])
            continue
        by_place.setdefault(slug, []).append(tree(t, new_id))
    os.makedirs(OUT, exist_ok=True)
    for slug, ts in by_place.items():
        path = os.path.join(OUT, slug + ".json")
        if slug == "split":
            src = os.path.join(ROOT, "data", "cities", "split.json")
            d = json.load(open(src))
            have = {x["id"] for x in d["trees"]}
            d["trees"] += [x for x in ts if x["id"] not in have]
            for f in d.get("faq", []):
                f["a"] = f["a"].replace(
                    "Yes, three of the four stand on a public promenade or in a public garden with no charge.",
                    "Yes, three of the city's trees stand on a public promenade or in a public garden with no charge, and the bald cypress in Solin is free to see along the Jadro river.")
        else:
            if os.path.exists(path) and OUT.endswith(os.path.join("data", "cities")):
                sys.exit(f"{path} exists; refusing to overwrite")
            p = places[slug]
            d = {k: p[k] for k in PLACE_FIELDS if k in p}
            d.setdefault("country", "Croatia")
            d.setdefault("status", "needs_curation")
            for k in ("hero_tree_id", "oldest_tree_id"):
                if d.get(k) in idmap:
                    d[k] = idmap[d[k]]
            d["trees"] = ts
            d = {k: d[k] for k in PLACE_FIELDS + ["trees"] if k in d}
        json.dump(d, open(path, "w"), ensure_ascii=False, indent=2)
        open(path, "a").write("\n")
        print("wrote", path, len(ts), "tree(s)")


if __name__ == "__main__":
    main()
