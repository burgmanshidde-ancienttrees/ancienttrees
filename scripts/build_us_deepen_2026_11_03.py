"""Publish the eleven US trees verified and written 2026-11-03 and held for the 25-a-day pace.
    python3 scripts/build_us_deepen_2026_11_03.py            # writes into data/cities
    python3 scripts/build_us_deepen_2026_11_03.py --max N    # only the first N, for the pace
Then preflight.py, commit each city by path, push, and passcheck.py --release each city.
Sources (verify passes and one write pass, 2026-11-03, Hidde: "doe 1 en 2"):
  salt-lake-city  data/research/salt-lake-city-verified.json slc_007..slc_009
  spokane         data/research/spokane-verified.json spk_016..spk_019
  miami           data/research/miami-verified.json mia_009..mia_012
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN = [("salt-lake-city", ["slc_007", "slc_008", "slc_009"]),
        ("spokane", ["spk_016", "spk_017", "spk_018", "spk_019"]),
        ("miami", ["mia_009", "mia_010", "mia_011", "mia_012"])]
# Copy that promised the old counts (preflight's count promises), applied only when every tree of the city lands.
COPY = {"salt-lake-city": [("of the six trees", "of the nine trees"), ("All six are free to visit", "All nine are free to visit"),
                           ("Where to find all six", "Where to find all nine")],
        "spokane": [("14 remarkable trees", "18 remarkable trees"),
                    ("all fourteen stand in public city parks with no entry charge", "all eighteen can be seen free, most of them in public city parks with no entry charge")],
        "miami": []}
def recopy(obj, pairs):
    if isinstance(obj, str):
        for a, b in pairs: obj = obj.replace(a, b)
        return obj
    if isinstance(obj, list): return [recopy(x, pairs) for x in obj]
    if isinstance(obj, dict): return {k: (v if k == "trees" else recopy(v, pairs)) for k, v in obj.items()}
    return obj
left = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 99
for city, ids in PLAN:
    res = {t["id"]: t for t in json.load(open(os.path.join(ROOT, "data", "research", city + "-verified.json")))}
    path = os.path.join(ROOT, "data", "cities", city + ".json")
    doc = json.load(open(path))
    have = {t["id"] for t in doc["trees"]}
    added = []
    for i in ids:
        if left <= 0 or i in have:
            continue
        t = dict(res[i])
        if not t.get("story"):
            print("SKIP", i, "has no story"); continue
        doc["trees"].append(t); added.append(i); left -= 1
    if added and len(added) == len(ids):
        doc = recopy(doc, COPY[city])
    if added:
        json.dump(doc, open(path, "w"), ensure_ascii=False, indent=2); open(path, "a").write("\n")
    print(city, "added", added, "now", len(doc["trees"]))
