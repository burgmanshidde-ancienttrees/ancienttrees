"""Publish the three READY leads written on 2026-11-06 from
data/research/leads-write-2026-11-06-verified.json:
enk_001 (Enniskerry, new place), flo_029 (Florence), lsb_009 (Leesburg).

    python3 scripts/build_leads_write_2026_11_06.py [--check]

--check prints word counts and bans only. Writes into data/cities/<slug>.json
(creating enniskerry.json), then mark the leads with mark_leads_2026_11_06.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TREE_FIELDS = ["id", "name", "species", "masaf_code", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "how_to_recognise",
               "verified_sources", "official_register", "access", "transport", "best_time",
               "photo", "location_precision", "pin_source", "curation_status", "verify_notes"]
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}
BANNED = ["hidden gem", "must-see", "breathtaking", "nestled", "majestic", "stunning", "iconic",
          "a testament to", "—", "–", "!"]

NEW_PLACES = {
    "enniskerry": {
        "city": "Enniskerry",
        "country": "Ireland",
        "status": "needs_curation",
        "intro": "Powerscourt, beside Enniskerry in County Wicklow, says its River Walk holds the tallest tree in Ireland, a Douglas fir of 61.5 metres, officially recognised as the tallest on record in 2013. The estate's conifers came largely from a tree-planting programme of 1870. The gardens are ticketed.",
        "meta_description": "Powerscourt's River Walk Douglas fir at Enniskerry, Co. Wicklow: 61.5 metres, recognised in 2013 as the tallest tree in Ireland on record.",
        "question_meta": "Enniskerry's tallest tree is the Douglas fir on Powerscourt's River Walk, 61.5 metres by the estate's figure.",
        "question_answer": "The tallest tree at Enniskerry is a Douglas Fir (Pseudotsuga menziesii) on the River Walk of the Powerscourt Estate, 61.5 metres or 202 feet by the estate's figure. In 2013 it was reported as officially recognised as the tallest tree in Ireland since records began.",
        "hero_tree_id": "enk_001",
        "oldest_tree_id": "enk_001",
        "faq": [
            {"q": "How tall is the Powerscourt Douglas fir?",
             "a": "The estate gives 61.5 metres, or 202 feet, the figure reported in 2013 when it was recognised as the tallest tree in Ireland on record."},
            {"q": "Is it free to visit?",
             "a": "No. Powerscourt's gardens are ticketed, and the estate does not say whether the River Walk sits inside the garden ticket, so ask at the entrance."}
        ],
        "trees": []
    }
}


def words(s):
    return len(re.findall(r"\b[\w'.,-]+\b", s))


def check(t):
    errs = []
    n = len(t["story"].split())
    if not 150 <= n <= 250:
        errs.append(f"story {n} words")
    blob = json.dumps(t, ensure_ascii=False)
    for b in BANNED:
        if b.lower() in blob.lower():
            errs.append("banned " + repr(b))
    if len(t["how_to_recognise"]) >= 240:
        errs.append(f"recognise {len(t['how_to_recognise'])} chars")
    if ":" in t["story"]:
        errs.append("colon in story")
    return n, errs


def main():
    src = json.load(open(os.path.join(ROOT, "data", "research", "leads-write-2026-11-06-verified.json")))
    bad = False
    for t in src:
        n, errs = check(t)
        print(t["id"], n, "words", len(t["how_to_recognise"]), "chars", errs or "ok")
        bad = bad or bool(errs)
    if bad or "--check" in sys.argv:
        sys.exit(1 if bad else 0)
    for t in src:
        slug = t["city_slug"]
        path = os.path.join(ROOT, "data", "cities", slug + ".json")
        if os.path.exists(path):
            d = json.load(open(path))
        else:
            d = json.loads(json.dumps(NEW_PLACES[slug]))
        if t["id"] in {x["id"] for x in d["trees"]}:
            print(t["id"], "already live, skipped")
            continue
        o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
        o["photo"] = dict(MISSING)
        d["trees"].append(o)
        with open(path, "w") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(slug, "added", t["id"], "now", len(d["trees"]))


if __name__ == "__main__":
    main()
