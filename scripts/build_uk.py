"""Build the UK midlands and Scotland pass (verified 2026-11-02/03, written 2026-11-03) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_uk.py            # appends to edinburgh.json and glasgow.json, writes the new places
    python3 scripts/build_uk.py --out DIR  # dry build elsewhere
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/{edinburgh,glasgow-verified-2,wolverhampton,milton-keynes}-verified.json
(trees with stories, photo verdicts made by looking at the pixels), place fields in
data/research/uk-places.json. Edinburgh and Glasgow grow; their intro and meta are replaced
by the rewritten ones in uk-places.json and Edinburgh's free-entry answer loses its count. Wolverhampton, Cannock Chase and Milton Keynes have
two trees each, so their place pages stay out of Google and the trees go live as tree pages.
Birmingham, Aylesbury and West Bromwich found nothing that ships (data/leads/).
Woodland Trust Ancient Tree Inventory not used.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES

# slug: (research file, tree ids taken from it)
SOURCES = {
    "edinburgh": ("edinburgh-verified.json", ["edi_017", "edi_018", "edi_019", "edi_020", "edi_021"]),
    "glasgow": ("glasgow-verified-2.json", ["gla_007", "gla_009", "gla_010", "gla_011"]),
    "wolverhampton": ("wolverhampton-verified.json", ["wol_001", "wol_002"]),
    "cannock-chase": ("wolverhampton-verified.json", ["cnk_001", "cnk_002"]),
    "milton-keynes": ("milton-keynes-verified.json", ["mkn_001", "mkn_002"]),
}
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise",
               "location_precision", "pin_source", "curation_status", "verify_notes", "photo", "paid_entry"]
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}
# live faq sentences that state the old count (the intros are rewritten whole in uk-places.json)
FAQ_FIXES = {
    "edinburgh": [
        ("Thirteen of the sixteen are free", "Most are free"),
        ("both included in a paid admission ticket.",
         "both included in a paid admission ticket, and the yews of Malleny Garden, which charges admission."),
    ],
}
PAID = {"edi_020", "cnk_001", "gla_011"}  # Malleny (NTS), Shugborough (NT), Finlaystone: admission


def tree(t):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["verified_sources"] = [s if isinstance(s, str) else s.get("url") for s in o.get("verified_sources", [])]
    p = o.get("photo") or {}
    if p.get("status") == "approved" and p.get("url") and p.get("license"):
        o["photo"] = {k: v for k, v in p.items() if k in ("url", "license", "attribution", "attribution_url", "status")}
    else:
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
    return o


def main():
    places = json.load(open(os.path.join(R, "uk-places.json")))
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
            ts.append(tree(t))
        if not ts:
            continue
        live = os.path.join(CITIES, slug + ".json")
        path = os.path.join(OUT, slug + ".json")
        p = places.get(slug, {})
        if os.path.exists(live):
            d = json.load(open(live))
            mine = {x["id"] for x in ts}
            trees = [x for x in d["trees"] if x["id"] not in mine] + ts
            for k in ("intro", "meta_description"):
                if p.get(k):
                    d[k] = p[k]
            for f in d.get("faq", []):
                for old, new in FAQ_FIXES.get(slug, []):
                    f["a"] = f["a"].replace(old, new)
        else:
            if not p.get("intro"):
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
