"""Build data/cities/{palagiano,vico-del-gargano}.json from the second Puglia pass (2026-11-02).

Held for the 25-a-day pace. Run only when the pace allows two more trees, then
python3 scripts/city_names.py and python3 scripts/preflight.py, commit by path.
The first Puglia pass (Lecce, Vernole, Martina Franca) has its own builder; no place overlaps.
--remove deletes the two files again (for a test run).
"""
import json
import os
import sys

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
held = json.load(open(os.path.join(R, "data/research/puglia-2-held-2026-11-02.json")))["places"]
KEYS = ["city", "country", "intro", "meta_description", "question_meta", "question_answer",
        "question_context", "hero_tree_id", "oldest_tree_id", "faq"]

for slug, p in held.items():
    path = os.path.join(R, "data/cities", slug + ".json")
    if "--remove" in sys.argv:
        if os.path.exists(path):
            os.remove(path)
            print("removed", slug)
        continue
    if os.path.exists(path):
        sys.exit(slug + " already exists in data/cities; merge by hand instead")
    trees = json.load(open(os.path.join(R, "data/research", slug + "-verified.json")))
    city = {k: p[k] for k in KEYS}
    city["status"] = "needs_curation"
    city["trees"] = trees
    with open(path, "w") as f:
        json.dump(city, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(slug, len(trees), "trees")
