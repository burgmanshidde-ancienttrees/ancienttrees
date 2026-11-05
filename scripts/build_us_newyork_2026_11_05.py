"""Publish fourteen New York Great Trees written 2026-11-05 from data/research/new-york-3-verified.json.

    python3 scripts/build_us_newyork_2026_11_05.py            # writes into data/cities/new-york.json
    python3 scripts/build_us_newyork_2026_11_05.py --out DIR  # dry build elsewhere

Every one is an NYC Parks Great Trees entry with a confirmed pin (the Parks Tree Map point) and a
recognition line. Left out on purpose: nyc_085 (species field reads "Swamp White Oak" over the
Latin Quercus x filialis, a Parks mislabel the verify notes flagged; needs a verify fix first),
nyc_094 (14 m from the Camperdown Elm, duplicate check by hand), and the approximate-pin entries
without a story. Then preflight.py, commit by path.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES
IDS = ["nyc_071", "nyc_072", "nyc_074", "nyc_075", "nyc_078", "nyc_082", "nyc_083", "nyc_084",
       "nyc_086", "nyc_087", "nyc_088", "nyc_089", "nyc_090", "nyc_096"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "how_to_recognise",
               "verified_sources", "official_register", "access", "transport", "best_time",
               "photo", "location_precision", "pin_source", "curation_status", "paid_entry"]
PAID = {"nyc_084"}
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}


def main():
    res = {t["id"]: t for t in json.load(open(os.path.join(ROOT, "data", "research", "new-york-3-verified.json")))
           if isinstance(t, dict) and t.get("id")}
    path = os.path.join(CITIES, "new-york.json")
    d = json.load(open(path))
    have = {t["id"] for t in d["trees"]}
    added = []
    for i in IDS:
        if i in have:
            continue
        t = res[i]
        if not t.get("story") or not t.get("how_to_recognise"):
            sys.exit(i + " has no story or recognition line; refusing to build")
        o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
        p = t.get("photo") or {}
        o["photo"] = ({k: v for k, v in p.items() if v is not None} if p.get("status") == "approved" else dict(MISSING))
        o.setdefault("curation_status", "ai_generated")
        if i in PAID:
            o["paid_entry"] = True
        d["trees"].append(o)
        added.append(i)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "new-york.json"), "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("new-york added", len(added), "now", len(d["trees"]))


if __name__ == "__main__":
    main()
