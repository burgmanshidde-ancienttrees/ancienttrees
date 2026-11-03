"""Build the Andalucia REDIAM trees (verified and written 2026-11-02) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_andalucia.py            # appends to live cities, writes new places
    python3 scripts/build_andalucia.py --out DIR  # dry build elsewhere
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/<slug>-rediam-verified.json (trees with stories, from the
REDIAM register, data/registers/andalucia-rediam.json) and
data/research/andalucia-places.json (place fields for new places; for a live
city, the fields given there replace the live ones so intro and meta grow with
the trees). A tree carrying "hold" is skipped and printed.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES

# place slug -> (research file, id prefix for a new place; None = live city keeps its own)
PLACES = {
    "grazalema": ("grazalema-rediam-verified.json", "gzm"),
    "alpujarras": ("alpujarras-rediam-verified.json", "apj"),
    "aracena": ("aracena-rediam-verified.json", "arc"),
    "cazorla": ("cazorla-rediam-verified.json", "czl"),
    "granada": ("granada-rediam-verified.json", None),
    "cordoba": ("cordoba-rediam-verified.json", None),
    "ronda": ("ronda-rediam-verified.json", None),
    "malaga": ("malaga-rediam-verified.json", None),
}
PLACE_FIELDS = ["city", "country", "face_tree_id", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise", "photo",
               "location_precision", "pin_source", "curation_status", "verify_notes"]
PHOTO_FIELDS = ["url", "license", "attribution", "attribution_url", "status", "width", "height", "taken_month"]
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}


def tree(t, new_id):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["id"] = new_id
    o["verified_sources"] = [s.split(" ")[0] for s in o.get("verified_sources", []) if s.startswith("http")]
    if isinstance(o.get("photo"), dict) and o["photo"].get("status") == "approved":
        o["photo"] = {k: v for k, v in o["photo"].items() if k in PHOTO_FIELDS}
    else:
        o["photo"] = dict(MISSING)
    o.setdefault("curation_status", "ai_generated")
    return o


def next_ids(existing, prefix, n):
    nums = [int(m.group(1)) for m in (re.match(prefix + r"_(\d+)$", i) for i in existing) if m]
    start = max(nums, default=0) + 1
    return [f"{prefix}_{i:03d}" for i in range(start, start + n)]


def main():
    places = json.load(open(os.path.join(R, "andalucia-places.json")))
    os.makedirs(OUT, exist_ok=True)
    for slug, (fname, prefix) in PLACES.items():
        src = os.path.join(R, fname)
        if not os.path.exists(src):
            continue
        raw = json.load(open(src))
        raw = raw["trees"] if isinstance(raw, dict) else raw
        ready = []
        for t in raw:
            if t.get("hold") or not t.get("story"):
                print("HELD", slug, t.get("id"), t.get("hold") or "no story")
                continue
            ready.append(t)
        if not ready:
            continue
        live = os.path.join(CITIES, slug + ".json")
        p = places.get(slug, {})
        if os.path.exists(live) and prefix is None:
            d = json.load(open(live))
            have = {x["id"] for x in d["trees"]}
            pre = d["trees"][0]["id"].split("_")[0]
            ids = next_ids(have, pre, len(ready))
            idmap = {t["id"]: i for t, i in zip(ready, ids)}
            d["trees"] += [tree(t, idmap[t["id"]]) for t in ready]
            for k in PLACE_FIELDS:
                if k in p:
                    d[k] = idmap.get(p[k], p[k]) if k.endswith("_tree_id") else p[k]
        else:
            if os.path.exists(live):
                sys.exit(f"{live} exists; refusing to overwrite")
            ids = next_ids(set(), prefix, len(ready))
            idmap = {t["id"]: i for t, i in zip(ready, ids)}
            d = {k: p[k] for k in PLACE_FIELDS if k in p}
            d.setdefault("country", "Spain")
            d["status"] = "needs_curation"
            for k in ("hero_tree_id", "oldest_tree_id", "face_tree_id"):
                if d.get(k):
                    d[k] = idmap.get(d[k], d[k])
            d["trees"] = [tree(t, idmap[t["id"]]) for t in ready]
            d = {k: d[k] for k in PLACE_FIELDS + ["trees"] if k in d}
        path = os.path.join(OUT, slug + ".json")
        with open(path, "w") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("wrote", path, len(ready), "tree(s) added")

    # The Spanish overlays of live cities must cover every tree, or the whole build is refused
    es = json.load(open(os.path.join(R, "andalucia-es.json")))
    for slug in sorted(set(es.get("places", {})) | set(es.get("trees", {}))):
        src = os.path.join(ROOT, "data", "i18n", "es", slug + ".json")
        if not os.path.exists(src):
            continue
        o = json.load(open(src))
        o.update(es.get("places", {}).get(slug, {}))
        for tid, tr in es.get("trees", {}).get(slug, {}).items():
            o["trees"].setdefault(tid, tr)
        if os.path.abspath(OUT) == os.path.abspath(CITIES):
            path = src
        else:
            path = os.path.join(OUT, "es-" + slug + ".json")
        with open(path, "w") as f:
            json.dump(o, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print("wrote", path, len(o["trees"]), "tree(s) in Spanish")


if __name__ == "__main__":
    main()
