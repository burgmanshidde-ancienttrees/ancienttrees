"""Build the central Italy MASAF pass (verified and written 2026-11-02) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_italy_central.py            # appends to live cities, writes new places
    python3 scripts/build_italy_central.py --out DIR  # dry build elsewhere
    python3 scripts/build_italy_central.py --only spoleto,rome   # a subset, when the pace allows only some
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/<file> per place below (trees with stories, from the MASAF national
register, data/registers/italy-masaf.json, CC BY 4.0) and data/research/italy-central-places.json
(place fields: for a live city they replace its intro, meta and FAQ, rewritten to cover the
new trees; for a new place they are the whole place), plus data/research/italy-central-it-overlay.json
(Italian for the new trees and changed place copy of Florence, Lucca and Rome, merged into
data/i18n/it/). A tree with "hold" never ships; a photo that is not "approved" ships as missing.
Spoleto's Marignoli plane (spo_003) is view-only, pinned on Vicolo del Quartiere.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES
ONLY = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None

SOURCES = {
    "spoleto": "spoleto-verified.json",
    "vallombrosa": "vallombrosa-verified.json",
    "rome": "rome-masaf-verified.json",
    "lucca": "lucca-masaf-verified.json",
    "perugia": "perugia-masaf-verified.json",
    "florence": "florence-masaf-verified.json",
}
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise",
               "location_precision", "pin_source", "curation_status", "verify_notes", "photo",
               "paid_entry"]
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}


def tree(t):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["verified_sources"] = [s if isinstance(s, str) else s.get("url") for s in o.get("verified_sources", [])]
    p = o.get("photo") or {}
    # a held or unjudged photo never ships; the tree goes out photo-less
    o["photo"] = {k: v for k, v in p.items() if v is not None} if p.get("status") == "approved" else dict(MISSING)
    o.setdefault("curation_status", "ai_generated")
    if isinstance(o.get("girth_cm"), float) and o["girth_cm"].is_integer():
        o["girth_cm"] = int(o["girth_cm"])
    return o


def load(src):
    path = os.path.join(R, src)
    if not os.path.exists(path):
        return []
    d = json.load(open(path))
    return d["trees"] if isinstance(d, dict) else d


def main():
    places = json.load(open(os.path.join(R, "italy-central-places.json")))
    os.makedirs(OUT, exist_ok=True)
    for slug, src in SOURCES.items():
        if ONLY and slug not in ONLY:
            continue
        ts = [tree(t) for t in load(src) if not t.get("hold")]
        if not ts:
            print("skip", slug, "(nothing to ship)")
            continue
        for t in ts:
            if not t.get("story"):
                sys.exit(f"{t['id']} has no story; refusing to build")
        live = os.path.join(CITIES, slug + ".json")
        path = os.path.join(OUT, slug + ".json")
        p = places.get(slug, {})
        if os.path.exists(live):
            d = json.load(open(live))
            have = {x["id"] for x in d["trees"]}
            clash = [x["id"] for x in ts if x["id"] in have]
            if clash:
                sys.exit(f"{slug}: ids already live {clash}; refusing to build twice")
            trees = d["trees"] + ts
            d.update({k: p[k] for k in PLACE_FIELDS if k in p})
        else:
            if not p:
                sys.exit(f"{slug}: new place without place fields")
            d = {k: p[k] for k in PLACE_FIELDS if k in p}
            trees = ts
        d.setdefault("country", "Italy")
        d.setdefault("status", "needs_curation")
        ids = {x["id"] for x in trees}
        for k in ("hero_tree_id", "oldest_tree_id"):
            if k in d and d[k] not in ids:
                sys.exit(f"{slug}: {k} {d.get(k)} is not one of its trees")
        rest = {k: v for k, v in d.items() if k not in PLACE_FIELDS + ["trees"]}
        d = {**{k: d[k] for k in PLACE_FIELDS if k in d}, **rest, "trees": trees}
        json.dump(d, open(path, "w"), ensure_ascii=False, indent=2)
        open(path, "a").write("\n")
        print("wrote", path, len(trees), "tree(s),", len(ts), "from this pass")
        overlay(slug, ts)


def overlay(slug, ts):
    # Florence, Lucca and Rome have Italian overlays; preflight refuses the whole deploy when one misses a tree.
    it_path = os.path.join(ROOT, "data", "i18n", "it", slug + ".json")
    if not os.path.exists(it_path):
        return
    it = json.load(open(it_path))
    new = json.load(open(os.path.join(R, "italy-central-it-overlay.json"))).get(slug, {})
    missing = [t["id"] for t in ts if t["id"] not in new.get("trees", {}) and t["id"] not in it["trees"]]
    if missing:
        sys.exit(f"italy-central-it-overlay.json lacks {missing}: translate them before building")
    for t in ts:
        it["trees"].setdefault(t["id"], new["trees"][t["id"]])
    for k, v in new.get("place", {}).items():
        if v:
            it[k] = v
    out = it_path if OUT == CITIES else os.path.join(OUT, "it-" + slug + ".json")
    json.dump(it, open(out, "w"), ensure_ascii=False, indent=1)
    open(out, "a").write("\n")
    print("wrote", out)


if __name__ == "__main__":
    main()
