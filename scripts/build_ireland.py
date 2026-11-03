"""Build the Ireland pass (verified and written 2026-11-03) into data/cities.

Hidde, 2026-11-03: "Ja, start Ierland", for readers of Crann, whose Autumn/Winter edition
carries our article. Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_ireland.py            # appends to tullamore.json, writes the new places
    python3 scripts/build_ireland.py --out DIR  # dry build elsewhere
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/{tullamore,birr,emo,inistioge,castlepollard,killarney,gort}-verified.json
(trees with stories, photo verdicts inside each tree) and place fields in
data/research/ireland-places.json. Candidates came from Heritage Trees of Ireland
(data/research/ireland-register-candidates.json); rounds 1 and 2 found that the register's
rows carry no names and the estates publish names without positions, so most rows are leads.
Every place is one to three trees, so its place page stays out of Google and the trees go
live as tree pages. Powerscourt, Kilmacurragh, Mount Usher, Doneraile and Lismore gave nothing
that ships (data/leads/).
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES

SOURCES = ["tullamore", "birr", "emo", "inistioge", "castlepollard", "killarney", "gort"]
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise",
               "photo", "photos", "location_precision", "pin_source", "curation_status",
               "verify_notes", "paid_entry"]
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}
PAID = {"bir_001", "bir_002", "bir_003", "wds_001", "wds_002"}  # Birr Castle Demesne tickets; Woodstock EUR 5 a car


def tree(t):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    if not o.get("how_to_recognise") and t.get("recognise"):
        o["how_to_recognise"] = t["recognise"]
    o["verified_sources"] = [s if isinstance(s, str) else s.get("url") for s in o.get("verified_sources", [])]
    if (o.get("photo") or {}).get("status") != "approved":
        o["photo"] = dict(MISSING)
    o.setdefault("curation_status", "ai_generated")
    if o["id"] in PAID:
        o["paid_entry"] = True
    if len(o["name"]) >= 60:
        sys.exit(f"{o['id']}: name over 60 characters")
    if not o.get("story"):
        sys.exit(f"{o['id']} has no story; refusing to build")
    if "—" in json.dumps(o, ensure_ascii=False):
        sys.exit(f"{o['id']}: em dash")
    return {k: o[k] for k in TREE_FIELDS if k in o}


def main():
    places = json.load(open(os.path.join(R, "ireland-places.json")))
    os.makedirs(OUT, exist_ok=True)
    for slug in SOURCES:
        ts = []
        for t in json.load(open(os.path.join(R, slug + "-verified.json"))):
            if not isinstance(t, dict):
                continue
            if t.get("hold") or not t.get("story"):
                print("HELD", t.get("id"), t.get("hold") or "no story")
                continue
            ts.append(tree(t))
        if not ts:
            continue
        live = os.path.join(CITIES, slug + ".json")
        p = places.get(slug, {})
        if os.path.exists(live):
            d = json.load(open(live))
            mine = {x["id"] for x in ts}
            trees = [x for x in d["trees"] if x["id"] not in mine] + ts
            d.update({k: p[k] for k in PLACE_FIELDS if k in p})
        else:
            if not p:
                sys.exit(f"{slug}: new place without place fields")
            d = {k: p[k] for k in PLACE_FIELDS if k in p}
            trees = ts
        d.setdefault("country", "Ireland")
        d.setdefault("status", "needs_curation")
        tids = {x["id"] for x in trees}
        for k in ("hero_tree_id", "oldest_tree_id"):
            if k in d and d[k] not in tids:
                sys.exit(f"{slug}: {k} {d.get(k)} is not one of its trees")
        rest = {k: v for k, v in d.items() if k not in PLACE_FIELDS + ["trees"]}
        d = {**{k: d[k] for k in PLACE_FIELDS if k in d}, **rest, "trees": trees}
        with open(os.path.join(OUT, slug + ".json"), "w") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("wrote", slug, len(trees), "tree(s),", len(ts), "from this pass")


if __name__ == "__main__":
    main()
