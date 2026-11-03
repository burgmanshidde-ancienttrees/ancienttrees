"""Build the southern Italy MASAF pass (verified and written 2026-11-02) into data/cities.

Held for the 25-a-day pace when written. The session that publishes runs:
    python3 scripts/build_italy_south.py            # appends to live places, writes new ones
    python3 scripts/build_italy_south.py --out DIR  # dry build elsewhere
then city_names.py, preflight.py, commit by path, push.

Sources: data/research/<slug>-verified.json per place (stories written, photos judged)
and data/research/italy-south-places-*.json (place fields, rewritten to cover the new trees
for the live places). A live place keeps its trees and gains the new ones; its intro, meta
and faq are replaced by the grown versions. A tree with "hold" set never ships.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "data", "research")
CITIES = os.path.join(ROOT, "data", "cities")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else CITIES

SOURCES = {
    # Sicily
    "palermo": "palermo-verified.json",
    "agrigento": "agrigento-verified.json",
    "palazzolo-acreide": "palazzolo-acreide-verified.json",
    "noto": "noto-verified.json",
    "ragusa": "ragusa-verified.json",
    # Campania
    "naples": "naples-verified.json",
    "caserta": "caserta-verified.json",
    "benevento": "benevento-verified.json",
    "portici": "portici-verified.json",
    "castellammare-di-stabia": "castellammare-di-stabia-verified.json",
    "monte-faito": "monte-faito-verified.json",
    # Calabria
    "sila": "sila-verified.json",
    "san-pietro-in-amantea": "san-pietro-in-amantea-verified.json",
    "serra-san-bruno": "serra-san-bruno-verified.json",
}
PLACE_FILES = ["italy-south-places-sicily.json", "italy-south-places-campania-1.json",
               "italy-south-places-campania-2-calabria.json"]
PLACE_FIELDS = ["city", "country", "status", "intro", "meta_description", "question_meta",
                "question_answer", "question_context", "hero_tree_id", "face_tree_id",
                "oldest_tree_id", "faq"]
TREE_FIELDS = ["id", "name", "species", "age_estimate", "age_min", "age_max", "age_basis",
               "girth_cm", "height_m", "location", "location_site", "story", "verified_sources",
               "official_register", "access", "transport", "best_time", "how_to_recognise",
               "location_precision", "curation_status", "verify_notes", "photo", "paid_entry"]
PAID = {  # ids behind a ticket
    "agr_001", "agr_002", "agr_003", "agr_004", "agr_005", "agr_007",  # Valle dei Templi, Kolymbethra
    "rgs_001", "pal_027", "nap_028", "nap_029", "sil_001", "csm_001", "csm_002",
    "ptc_001", "ptc_002", "ptc_003", "ptc_004", "ptc_005",
}
# live stories a new tree makes false: pal_024 is a second registered plane in Palermo
STORY_FIX = {
    "pal_019": [("Italy has exactly one nationally registered monumental plane tree in Sicily, and it stands",
                 "Palermo has two London planes on Italy's national register of monumental trees, and this one stands"),
                ("What makes this one worth the ticket price is rarer: on a whole island covered in ornamental gardens built by the same wealthy families who imported half the trees on this list, nobody registered a second one.",
                 "It is the bigger of the city's two registered planes; the other stands by the road outside the Ucciardone prison, north of the port.")],
}
ACCESS_FIX = {
    "pal_019": [("same grounds and ticket as the already-published Fig of Villa Tasca, ; sources disagree on exact hours, confirm before publishing a specific time",
                 "same grounds and ticket as the Fig of Villa Tasca; sources disagree on the hours, so check before you go")],
}
MISSING = {"url": None, "license": None, "attribution": None, "status": "missing"}


def tree(t):
    o = {k: t[k] for k in TREE_FIELDS if t.get(k) not in (None, "", [])}
    o["verified_sources"] = [s if isinstance(s, str) else s.get("url") for s in o.get("verified_sources", [])]
    p = o.get("photo") or {}
    # a held photo never ships; the tree goes out photo-less
    o["photo"] = {k: v for k, v in p.items() if v is not None} if p.get("status") == "approved" else dict(MISSING)
    o.setdefault("curation_status", "ai_generated")
    if o["id"] in PAID:
        o["paid_entry"] = True
    return o


def main():
    places = {}
    for f in PLACE_FILES:
        places.update(json.load(open(os.path.join(R, f))))
    os.makedirs(OUT, exist_ok=True)
    for slug, src in SOURCES.items():
        ts = [tree(t) for t in json.load(open(os.path.join(R, src))) if not t.get("hold")]
        for t in ts:
            if not t.get("story"):
                sys.exit(f"{t['id']} has no story; refusing to build")
        live = os.path.join(CITIES, slug + ".json")
        path = os.path.join(OUT, slug + ".json")
        p = places[slug]
        if os.path.exists(live):
            d = json.load(open(live))
            have = {x["id"] for x in d["trees"]}
            for x in d["trees"]:
                for field, fixes in (("story", STORY_FIX), ("access", ACCESS_FIX)):
                    for old, new in fixes.get(x["id"], []):
                        if old in x.get(field, ""):
                            x[field] = x[field].replace(old, new)
            trees = d["trees"] + [x for x in ts if x["id"] not in have]
            d.update({k: p[k] for k in PLACE_FIELDS if k in p})
        else:
            d = {k: p[k] for k in PLACE_FIELDS if k in p}
            trees = ts
        d.setdefault("country", "Italy")
        d.setdefault("status", "needs_curation")
        ids = {x["id"] for x in trees}
        for k in ("hero_tree_id", "face_tree_id", "oldest_tree_id"):
            if k in d and d[k] not in ids:
                sys.exit(f"{slug}: {k} {d.get(k)} is not one of its trees")
        rest = {k: v for k, v in d.items() if k not in PLACE_FIELDS + ["trees"]}
        d = {**{k: d[k] for k in PLACE_FIELDS if k in d}, **rest, "trees": trees}
        json.dump(d, open(path, "w"), ensure_ascii=False, indent=2)
        open(path, "a").write("\n")
        print("wrote", path, len(trees), "tree(s),", len(ts), "from this pass")
        if slug in IT_OVERLAY:
            it_overlay(slug, IT_OVERLAY[slug], [x["id"] for x in ts])


# Naples and Palermo have Italian overlays; preflight refuses the whole deploy when one misses a tree.
IT_OVERLAY = json.load(open(os.path.join(R, "italy-south-it-overlay.json"))) \
    if os.path.exists(os.path.join(R, "italy-south-it-overlay.json")) else {}


def it_overlay(slug, new, ids):
    path = os.path.join(ROOT, "data", "i18n", "it", slug + ".json")
    ov = json.load(open(path))
    missing = [i for i in ids if i not in new["trees"] and i not in ov["trees"]]
    if missing:
        sys.exit(f"italy-south-it-overlay.json lacks {missing}: translate them before building")
    for i, t in new["trees"].items():  # new trees, plus pal_019's corrected story
        ov["trees"].setdefault(i, {}).update(t)
    for k, v in new["place"].items():
        if v:
            ov[k] = v
    out = path if OUT == CITIES else os.path.join(OUT, "it-" + slug + ".json")
    json.dump(ov, open(out, "w"), ensure_ascii=False, indent=1)
    open(out, "a").write("\n")
    print("wrote", out)


if __name__ == "__main__":
    main()
