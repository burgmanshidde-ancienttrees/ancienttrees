"""Build the northern England and Wales pass (verified 2026-11-03, written 2026-11-03) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_uk_north.py            # appends to liverpool.json and cardiff.json, writes the new places
    python3 scripts/build_uk_north.py --out DIR  # dry build elsewhere
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/{liverpool,cardiff,sheffield,ripon,wales-yews,keswick,newcastle}-verified.json
(trees with stories), place fields in data/research/uk-north-places.json, and photo verdicts in
data/research/uk-north-photos.json (looked at 2026-11-03; only `approved` ever ships).
Liverpool gains the Speke Hall yews and Cardiff three Bute Park champions; their intro and
meta grow with them. Every other place is one or two trees, so its place page stays out of
Google and the trees go live as tree pages. Leeds, York, Manchester, Chester and Durham passes
found nothing that ships (data/leads/). Woodland Trust Ancient Tree Inventory not used.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES

# slug: (research file, tree ids taken from it)
SOURCES = {
    "liverpool": ("liverpool-verified.json", ["lvp_003"]),
    "cardiff": ("cardiff-verified.json", ["crd_005", "crd_006", "crd_007"]),
    "sheffield": ("sheffield-verified.json", ["shf_001", "shf_002"]),
    "ripon": ("ripon-verified.json", ["rip_002"]),
    "defynnog": ("wales-yews-verified.json", ["dfy_001"]),
    "discoed": ("wales-yews-verified.json", ["dsc_001"]),
    "pennant-melangell": ("wales-yews-verified.json", ["pml_001"]),
    "llanerfyl": ("wales-yews-verified.json", ["lef_001"]),
    "gresford": ("wales-yews-verified.json", ["gfd_001"]),
    "nevern": ("wales-yews-verified.json", ["nvn_001"]),
    "martindale": ("keswick-verified.json", ["mtd_001"]),
    "lorton": ("keswick-verified.json", ["ltn_001"]),
    "beltingham": ("newcastle-verified.json", ["blt_001"]),
}
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise",
               "location_precision", "pin_source", "curation_status", "verify_notes", "photo", "paid_entry"]
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}
PAID = {"lvp_003"}  # Speke Hall: National Trust admission (the Studley Royal deer park is open to walkers)


def tree(t, photos):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["verified_sources"] = [s if isinstance(s, str) else s.get("url") for s in o.get("verified_sources", [])]
    p = photos.get(o["id"])
    o["photo"] = {**p, "status": "approved"} if p else dict(MISSING)
    o["photo"].pop("why", None)
    o.setdefault("curation_status", "ai_generated")
    if o["id"] in PAID:
        o["paid_entry"] = True
    if len(o["name"]) >= 60:
        sys.exit(f"{o['id']}: name over 60 characters")
    if not o.get("story"):
        sys.exit(f"{o['id']} has no story; refusing to build")
    if "—" in json.dumps(o, ensure_ascii=False):
        sys.exit(f"{o['id']}: em dash")
    return o


def main():
    places = json.load(open(os.path.join(R, "uk-north-places.json")))
    photos = json.load(open(os.path.join(R, "uk-north-photos.json")))["approved"]
    os.makedirs(OUT, exist_ok=True)
    for slug, (src, ids) in SOURCES.items():
        rows = {t["id"]: t for t in json.load(open(os.path.join(R, src))) if isinstance(t, dict)}
        ts = []
        for i in ids:
            t = rows.get(i)
            if t is None:
                sys.exit(f"{slug}: {i} not in {src}")
            if t.get("hold"):
                print("HELD", i, t["hold"])
                continue
            ts.append(tree(t, photos))
        if not ts:
            continue
        live = os.path.join(CITIES, slug + ".json")
        path = os.path.join(OUT, slug + ".json")
        p = places.get(slug, {})
        if os.path.exists(live):
            d = json.load(open(live))
            # a rerun replaces this pass's own trees, so a fixed story always lands
            mine = {x["id"] for x in ts}
            trees = [x for x in d["trees"] if x["id"] not in mine] + ts
            d.update({k: p[k] for k in PLACE_FIELDS if k in p})
        else:
            if not p:
                sys.exit(f"{slug}: new place without place fields")
            d = {k: p[k] for k in PLACE_FIELDS if k in p}
            trees = ts
        d.setdefault("country", "United Kingdom")
        d.setdefault("status", "needs_curation")
        tids = {x["id"] for x in trees}
        for k in ("hero_tree_id", "oldest_tree_id"):
            if k in d and d[k] not in tids:
                sys.exit(f"{slug}: {k} {d.get(k)} is not one of its trees")
        rest = {k: v for k, v in d.items() if k not in PLACE_FIELDS + ["trees"]}
        d = {**{k: d[k] for k in PLACE_FIELDS if k in d}, **rest, "trees": trees}
        with open(path, "w") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("wrote", path, len(trees), "tree(s),", len(ts), "from this pass")


if __name__ == "__main__":
    main()
