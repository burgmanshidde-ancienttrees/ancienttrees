"""Publish 29 New York trees written 2026-11-06 from data/research/new-york-{2,3,4}-verified.json.

    python3 scripts/build_us_newyork_2026_11_06.py            # writes into data/cities/new-york.json
    python3 scripts/build_us_newyork_2026_11_06.py --out DIR  # dry build elsewhere

Left out on purpose: nyc_085 (species field reads Swamp White Oak over the Latin Quercus x filialis,
a Parks mislabel) and nyc_094 (14 m from the Camperdown Elm). Species names aligned to the live
canonical ones. Then preflight.py, commit by path.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES
FILES = {
    "new-york-2-verified.json": ["nyc_037", "nyc_038", "nyc_039", "nyc_040"],
    "new-york-3-verified.json": ["nyc_091", "nyc_092", "nyc_093", "nyc_097", "nyc_098"],
    "new-york-4-verified.json": ["nyc_110", "nyc_111", "nyc_112", "nyc_113", "nyc_114", "nyc_115",
                                 "nyc_116", "nyc_117", "nyc_118", "nyc_119", "nyc_120", "nyc_125",
                                 "nyc_126", "nyc_128", "nyc_129", "nyc_131", "nyc_132", "nyc_134",
                                 "nyc_135", "nyc_136"],
}
SPECIES = {
    "nyc_116": "Small-leaved Lime (Tilia cordata)",
    "nyc_111": "Weeping Beech (Fagus sylvatica 'Pendula')",
    "nyc_136": "Weeping Beech (Fagus sylvatica 'Pendula')",
    "nyc_128": "Wild Cherry (Prunus avium)",
    "nyc_112": "Fern-leaved Beech (Fagus sylvatica 'Laciniata')",
    "nyc_097": "Persian Ironwood (Parrotia persica)",
}
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "how_to_recognise",
               "verified_sources", "official_register", "access", "transport", "best_time",
               "photo", "location_precision", "pin_source", "curation_status", "paid_entry"]
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}


def main():
    path = os.path.join(CITIES, "new-york.json")
    d = json.load(open(path))
    have = {t["id"] for t in d["trees"]}
    added = []
    for fn, ids in FILES.items():
        res = {t["id"]: t for t in json.load(open(os.path.join(ROOT, "data", "research", fn)))
               if isinstance(t, dict) and t.get("id")}
        for i in ids:
            if i in have:
                continue
            t = res[i]
            if not t.get("story") or not t.get("how_to_recognise"):
                sys.exit(i + " has no story or recognition line; refusing to build")
            o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
            if i in SPECIES:
                o["species"] = SPECIES[i]
            p = t.get("photo") or {}
            o["photo"] = ({k: v for k, v in p.items() if v is not None} if p.get("status") == "approved" else dict(MISSING))
            o.setdefault("curation_status", "ai_generated")
            d["trees"].append(o)
            added.append(i)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "new-york.json"), "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("new-york added", len(added), "now", len(d["trees"]))


if __name__ == "__main__":
    main()
