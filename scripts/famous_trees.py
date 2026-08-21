#!/usr/bin/env python3
"""Search for famous trees, not for our tree names. Commons has a whole tree of them.

Hidde, 2026-08-13: "what if you just search famous tree amsterdam. and you then
find some, identify which one it is and use it." He is right, and it turns out
Commons has done the work already. `Category:Famous trees by country` holds 82
countries, and under each sits one category PER NAMED TREE: Kroezeboom
Fleringen, Linde van Sambeek, Lindes van de Uithof Utrecht. Every file in one
of those is a photograph of one specific famous tree, which is exactly what a
tree page needs and what our per-tree searching kept failing to find.

The direction is reversed from photo_hunt.py, and that is the point:

    photo_hunt.py   for each of our trees, ask the world for a photo of it
    famous_trees.py ask the world which trees it thinks are famous, then see
                    which of them we already have

Both halves of the answer are useful. A category that matches one of our trees
by coordinate is a photograph we can use. A category that matches nothing is a
famous tree we do not map, with a photo and coordinates attached, which is a
lead worth more than most register rows.

    python3 scripts/famous_trees.py --country "Netherlands"
    python3 scripts/famous_trees.py --all          # every country we publish in
    python3 scripts/famous_trees.py --country Italy --write

Without --write it prints and changes nothing. With --write it adds photo
candidates to data/photo-queue.json for matched trees (a viewing pass still
judges them, as always) and appends unmatched famous trees to
data/leads/_famous-<country>.json.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from geo import km  # noqa: E402
from photo_hunt import licence_ok, _plain  # noqa: E402

API = "https://commons.wikimedia.org/w/api.php"
UA = "AncientTreesBot/1.0 (https://ancienttrees.app; famous tree sweep)"
MATCH_M = 150       # a named tree's photos scatter around it; 150 m is the tree
PAUSE = 0.4


def api(**params):
    params = dict(params, format="json", action="query")
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params),
                                 headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def members(category, kind):
    out, cont = [], {}
    while True:
        d = api(list="categorymembers", cmtitle=category, cmtype=kind,
                cmlimit="200", **cont)
        out += [m["title"] for m in d.get("query", {}).get("categorymembers", [])]
        if "continue" not in d:
            return out
        cont = d["continue"]
        time.sleep(PAUSE)


def files_with_meta(titles):
    """Licence, url, coordinates for up to 50 files at a time."""
    out = []
    for i in range(0, len(titles), 50):
        d = api(titles="|".join(titles[i:i + 50]),
                prop="imageinfo|coordinates", iiprop="url|extmetadata",
                iiurlwidth="800")
        for page in (d.get("query", {}).get("pages", {}) or {}).values():
            for ii in page.get("imageinfo", []):
                meta = ii.get("extmetadata", {})
                lic = (meta.get("LicenseShortName") or {}).get("value", "")
                if not licence_ok(lic):
                    continue
                coord = (page.get("coordinates") or [{}])[0]
                out.append({
                    "title": page.get("title"),
                    "thumb": ii.get("thumburl"),
                    "url": ii.get("descriptionurl"),
                    "licence": lic,
                    "author": _plain((meta.get("Artist") or {}).get("value", "")),
                    "lat": coord.get("lat"),
                    "lng": coord.get("lon"),
                    "source": "commons/famous",
                })
        time.sleep(PAUSE)
    return out


def our_trees():
    import glob
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for t in d.get("trees", []):
            loc = t.get("location") or {}
            if loc.get("latitude") is None:
                continue
            out.append({"id": t["id"], "name": t["name"], "city": d["city"],
                        "country": d.get("country", ""), "file": f,
                        "lat": loc["latitude"], "lng": loc["longitude"],
                        "has_photo": bool((t.get("photo") or {}).get("url"))})
    return out


def sweep_country(country, trees, write=False):
    # Commons files some countries with the article and some without
    # ("Famous trees in the Netherlands", "Famous trees in Italy"), and the
    # wrong one returns an empty category rather than an error, which is how
    # this script reported zero for a country with eighteen named trees.
    subs, loose, cat = [], [], None
    for candidate in (f"Category:Famous trees in {country}",
                      f"Category:Famous trees in the {country}"):
        try:
            s2, f2 = members(candidate, "subcat"), members(candidate, "file")
        except Exception:
            continue
        if s2 or f2:
            subs, loose, cat = s2, f2, candidate
            break
    if cat is None:
        print(f"  {country}: no famous-trees category")
        return [], []
    # "Category:Famous trees in Tuscany" is a container, not a tree. Recurse one
    # level into those and treat what is inside as the named trees; anything
    # deeper is a rabbit hole (Commons nests regions inside regions).
    containers = [x for x in subs if re.search(r"famous .*\bin\b|tree of the year", x, re.I)]
    named = [x for x in subs if x not in containers
             and not re.search(r"memorial|by |in \d", x, re.I)]
    for box in containers:
        try:
            named += [x for x in members(box, "subcat")
                      if not re.search(r"famous .*\bin\b|memorial", x, re.I)]
        except Exception:
            continue
    print(f"  {country}: {len(named)} named trees, {len(loose)} loose files")

    matched, leads = [], []
    for sub in named:
        try:
            titles = members(sub, "file")
        except Exception:
            continue
        if not titles:
            continue
        photos = files_with_meta(titles[:12])
        geo = [p for p in photos if p["lat"] is not None]
        label = sub.replace("Category:", "")
        hit = None
        # Fall back to the name when the photographs carry no coordinates,
        # which is most of them: "Lindes van de Uithof, Utrecht" is our
        # utr_001 and matched nothing until this existed. A shared word of
        # five letters or more, in the same country, is enough to flag; the
        # print says what it matched so a human can see it is right.
        def tokens(x):
            # Generic words for tree in the languages we cover. Without this,
            # "Quercia centorami (Forenza)" matched Milan's Quercia Rossa on
            # the word for oak, which is not evidence of anything.
            generic = {"trees", "tree", "boom", "bomen", "arbre", "arbres",
                       "albero", "alberi", "quercia", "querce", "olmo", "pino",
                       "cedro", "platano", "tiglio", "linde", "lindes", "eiken",
                       "beuk", "plataan", "chene", "chêne", "tilleul", "hetre",
                       "hêtre", "roble", "encina", "arbol", "árbol", "arvore",
                       "árvore", "baum", "baume", "eiche", "linden", "buche",
                       "famous", "monumental", "monumentale", "grande", "grote",
                       "oude", "nieuwe", "vecchio", "viejo",
                       # English species words, for the same reason: "Hundred
                       # Horse Chestnut" (Sicily) matched Rome's horse chestnut
                       # on the word chestnut alone.
                       "chestnut", "beech", "planetree", "plane", "cedar",
                       "linden", "lime", "yew", "olive", "cypress", "poplar",
                       "willow", "walnut", "maple", "sequoia", "redwood",
                       "ginkgo", "mulberry", "elm", "birch", "banyan", "fig",
                       "hundred", "great", "giant", "ancient", "national"}
            return {w for w in re.findall(r"[a-zà-ÿ]{5,}", (x or "").lower())
                    if w not in generic}
        if geo:
            here = (geo[0]["lat"], geo[0]["lng"])
            for t in trees:
                if t["country"] != country:
                    continue
                if km(here, (t["lat"], t["lng"])) * 1000 <= MATCH_M:
                    hit = t
                    break
        by_name = False
        if not hit:
            lab = tokens(sub.replace("Category:", ""))
            for t in trees:
                if t["country"] != country:
                    continue
                # The tree's NAME only. Including the city matched "Anne Frank
                # tree, Amsterdam" to the Heimanseik on the word Amsterdam,
                # and "Rode beuk, De Nieuwe Ooster" to Breda's mulberries on
                # the word Nieuwe. A city name is never the evidence.
                if lab & tokens(t["name"]):
                    hit = t
                    by_name = True
                    break
        if hit:
            # A name match is a suggestion, never evidence. Measured across all
            # 30 countries on 2026-08-13 it produced four matches and all four
            # were wrong: "Washington Oak" to the Washington Monument witness
            # tree, "White Oak, Wernersville PA" to Boston's Peters Hill white
            # oak, Brookline's Olmsted Elm to a tulip tree in DC. So it prints
            # and it never queues; only a coordinate match writes anything.
            matched.append({"tree": hit, "label": label, "photos": photos,
                            "by_name": by_name})
            state = ("has a photo already" if hit["has_photo"]
                     else "NEEDS A PHOTO" if not by_name
                     else "name match only, not queued: check by hand")
            print(f"      {label[:44]:46s} -> {hit['id']} {hit['name'][:28]:30s} {state}")
        else:
            leads.append({"label": label, "photos": photos,
                          "lat": geo[0]["lat"] if geo else None,
                          "lng": geo[0]["lng"] if geo else None})
            where = f"{geo[0]['lat']:.4f},{geo[0]['lng']:.4f}" if geo else "no coordinates"
            print(f"      {label[:44]:46s} -> not on our map ({where})")
    return matched, leads


def main():
    args = sys.argv[1:]
    write = "--write" in args
    trees = our_trees()
    countries = []
    if "--country" in args:
        countries = [args[args.index("--country") + 1]]
    elif "--all" in args:
        countries = sorted({t["country"] for t in trees})
    else:
        print(__doc__.strip().splitlines()[0])
        print("usage: famous_trees.py --country <name> [--write] | --all [--write]")
        return 1

    all_matched, all_leads = [], []
    for c in countries:
        m, l = sweep_country(c, trees, write)
        all_matched += m
        all_leads.append((c, l))

    need = [m for m in all_matched if not m["tree"]["has_photo"] and not m.get("by_name")]
    print(f"\n{len(all_matched)} of our trees matched a famous-tree category, "
          f"{len(need)} of them have no photo yet")
    print(f"{sum(len(l) for _, l in all_leads)} famous trees are not on our map at all")

    if not write:
        print("\n(dry run: pass --write to queue the photos and save the leads)")
        return 0

    qpath = os.path.join(ROOT, "data", "photo-queue.json")
    queue = json.load(open(qpath, encoding="utf-8"))
    added = 0
    for m in need:
        e = queue["trees"].setdefault(m["tree"]["id"], {
            "city": m["tree"]["city"], "name": m["tree"]["name"], "candidates": []})
        seen = {c.get("url") for c in e.get("candidates") or []}
        fresh = [p for p in m["photos"] if p["url"] not in seen]
        e["candidates"] = (e.get("candidates") or []) + fresh
        e["checked"] = time.strftime("%Y-%m-%d")
        added += len(fresh)
    json.dump(queue, open(qpath, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"queued {added} candidates for a viewing pass")

    for country, leads in all_leads:
        if not leads:
            continue
        slug = re.sub(r"[^a-z]+", "-", country.lower()).strip("-")
        path = os.path.join(ROOT, "data", "leads", f"_famous-{slug}.json")
        # MERGE, never overwrite: a bare re-dump here once erased a hand-added
        # entry (Greece's Tsagarada plane, tipped by Hidde 2026-08-14, with a
        # "why" field this sweep knows nothing about) because Commons simply
        # did not return it that day. Old entries survive by name unless this
        # sweep re-found them, in which case the sweep's fresher lat/lng/photos
        # win but any extra hand-written fields (why, status other than
        # "lead") are kept.
        old = {}
        if os.path.exists(path):
            try:
                old = {e["name"]: e for e in json.load(open(path, encoding="utf-8"))
                       .get("leads", []) if e.get("name")}
            except Exception:
                old = {}
        merged = dict(old)
        for l in leads:
            fresh = {"name": l["label"], "lat": l["lat"], "lng": l["lng"],
                      "photos": [p["url"] for p in l["photos"][:3]],
                      "status": "lead"}
            prior = old.get(l["label"], {})
            merged[l["label"]] = {**prior, **fresh}
        json.dump({
            "country": country,
            "note": ("Famous trees Commons has a category for and we do not map. "
                     "Found by scripts/famous_trees.py; each one already has "
                     "photographs and usually coordinates, so the expensive half "
                     "of a research pass is done. Not verified by us, not published."),
            "leads": list(merged.values()),
        }, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(f"wrote {len(merged)} leads to {os.path.relpath(path, ROOT)} "
              f"({len(leads)} from this sweep, {len(merged) - len(leads)} kept from before)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
