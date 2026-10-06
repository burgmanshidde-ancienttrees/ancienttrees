#!/usr/bin/env python3
"""Enrich the tree pages Google can see, before adding pages it cannot.

Hidde, 2026-10-06 ("ja"), on Google's guidance after the 09-28 demotion: a
page should carry what no AI can make up, and we did very little with it.
Measured that day on the 943 indexed tree pages (the ones with a photograph):
53% carried a measurement, 43% a season, 19% concrete opening facts, 2% a
reader's photograph, and 12% named an official register. The night runs were
meanwhile opening US cities whose new trees, photo-less, never reach the index.
So this is now the night run's FIRST work, above verifying new trees
(prepare.py prints it first), and it reverses his 2026-10-05 "keep adding
trees" for the order of work, not for whether trees are added at all.

What counts as a gap on an indexed tree (photo, not held):
  register     no official register named (site/src/lib/official-register.ts)
  measurement  no girth_cm and no height_m
  access       the access line has no hours, no "free"/price and no days
  season       no best_time, while data/phenology/ has a file for the species

Usage:
  python3 scripts/enrich.py              # per proven city, gaps on indexed trees
  python3 scripts/enrich.py --next       # the one city to enrich now
  python3 scripts/enrich.py --brief <city>   # paste-ready brief for an agent
  python3 scripts/enrich.py --apply <file>   # merge an agent's answer (out/enrich/<city>.answer.json)
  python3 scripts/enrich.py --done <city>    # a pass that closed nothing: skip it 14 days

The answer file is a JSON list of {"id", optional "add_source" (a URL the
agent opened: the authority's own record, the site's own page), "girth_cm",
"height_m", "measure_source", "access", "best_time"}. Nothing is written
without a source, and the apply step refuses a measurement or an access line
that arrives without one.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CITIES = os.path.join(ROOT, "data", "cities")

RECORD = re.compile(
    r"online\.bunka\.go\.jp/.*detail/|kunishitei\.bunka\.go\.jp/heritage/detail/|kyoju\.biodic\.go\.jp/.*gtsearchdetail"
    r"|crfop\.gdos\.gov\.pl/.*viewpomnikprzyrody|inventaris\.onroerenderfgoed\.be/erfgoedobjecten/|heritagetrees\.nparks\.gov\.sg/ht-"
    r"|comune\.milano\.it/.*/alberi-monumentali/|mediambient\.gencat\.cat/.*arbres-monumentals/|heritage\.go\.kr/heri/cul/culSelectDetail"
    r"|drusop\.nature\.cz/.*pstromy|nycgovparks\.org/.*great-trees"
    r"|barcelona\.cat/.*(trees-of-local-interest|arboles-de-interes-local|arbres-d-interes-local)|geneve\.ch/.*arbres-particuliers/")
REG_SLUGS = [os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, "data", "registers", "*.json"))]
CONCRETE = re.compile(r"\d{1,2}[:.h]\d{2}|\b(free|gratis|daylight|dawn|dusk|always open|open all|24 hours|eur|€|\$|£|¥|ticket|closed)\b", re.I)
PHEN = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, "data", "phenology", "*.json"))}


def has_photo(t):
    p = t.get("photo") or {}
    return bool(p.get("url")) and p.get("status") != "held"


def species_slug(t):
    common = (t.get("species") or "").split("(")[0].strip().lower()
    return re.sub(r"[^a-z0-9]+", "-", common).strip("-")


def gaps(t):
    out = []
    src = t.get("verified_sources") or []
    if not (t.get("official_register") or any(RECORD.search(s) for s in src)
            or any(not s.startswith("http") and any(re.search(rf"(^|[\s/(]){re.escape(sl)}(\.json)?(?=[\s,()]|$)", s) for sl in REG_SLUGS) for s in src)):
        out.append("register")
    if not (t.get("girth_cm") or t.get("height_m")):
        out.append("measurement")
    if not CONCRETE.search(t.get("access") or ""):
        out.append("access")
    if not t.get("best_time") and species_slug(t) in PHEN:
        out.append("season")
    return out


def roster():
    try:
        d = json.load(open(os.path.join(ROOT, "data", "depth-roster-frozen.json")))
        return list(d["cities"].items())
    except (OSError, ValueError, KeyError):
        return []


LEDGER = os.path.join(ROOT, "data", "enrich-done.json")


def ledger():
    try:
        return json.load(open(LEDGER))
    except (OSError, ValueError):
        return {}


def recently_done(slug, days=14):
    import datetime
    d = ledger().get(slug)
    if not d:
        return False
    return (datetime.date.today() - datetime.date.fromisoformat(d)).days < days


def mark_done(slug):
    import datetime
    led = ledger()
    led[slug] = datetime.date.today().isoformat()
    with open(LEDGER, "w") as fh:
        json.dump(dict(sorted(led.items())), fh, indent=1)
        fh.write("\n")


def city_rows():
    rows = []
    for slug, v in roster():
        p = os.path.join(CITIES, slug + ".json")
        if not os.path.exists(p):
            continue
        trees = json.load(open(p, encoding="utf-8")).get("trees", [])
        ix = [t for t in trees if has_photo(t)]
        g = {t["id"]: gaps(t) for t in ix}
        n = sum(len(x) for x in g.values())
        if n:
            rows.append((slug, v.get("impressions", 0), len(ix), n, g))
    return rows


def show(rows, limit=None):
    print("ENRICH: gaps on INDEXED tree pages (photo), proven cities by pre-demotion impressions")
    print("| City | Impressions 09-27 | Indexed trees | Gaps | register | measurement | access | season |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|")
    for slug, imp, ix, n, g in rows[:limit]:
        c = {k: sum(k in x for x in g.values()) for k in ("register", "measurement", "access", "season")}
        print(f"| {slug} | {imp} | {ix} | {n} | {c['register']} | {c['measurement']} | {c['access']} | {c['season']} |")


def brief(slug):
    p = os.path.join(CITIES, slug + ".json")
    d = json.load(open(p, encoding="utf-8"))
    items = []
    for t in d["trees"]:
        if not has_photo(t):
            continue
        g = gaps(t)
        if not g:
            continue
        items.append({"id": t["id"], "name": t["name"], "species": t.get("species"),
                      "address": (t.get("location") or {}).get("address"),
                      "access": t.get("access"), "gaps": g,
                      "sources": t.get("verified_sources") or [],
                      "season_file": f"data/phenology/{species_slug(t)}.json" if "season" in g else None})
    print(f"""ENRICHMENT PASS: {d['city']} ({len(items)} indexed trees with gaps). Use the verify agent.

Fill what each tree page lacks, from sources you actually open. Never invent: a gap
you cannot close stays a gap, and that is a finished answer. Time-box: report
after about forty minutes.

Per gap:
- register: find the AUTHORITY'S OWN RECORD for this tree (a government or national
  register page about this one tree: Naturdenkmal entry, monumental-tree sheet,
  heritage-tree page). Return register_url (that page) and register_name (the
  register's own name, e.g. "Arvoredo de Interesse Público (ICNF)"). A register
  homepage, a data endpoint or a news article is not a record. Where the register
  has NO per-tree page but you found this tree's own entry in its data, return
  register_name and register_id (the register's number for this tree) instead.
  Girth is circumference at 1.30 m; a base circumference is not a girth, leave it out.
- measurement: girth_cm and/or height_m from a register, a plaque or the authority's
  page, with measure_source. Never from our own story, never the species' maximum.
- access: one plain line a visitor can act on: free or the price, opening days and
  hours where the site publishes them, from the site's own page (add it as add_source).
  Keep what the current line says that is still true.
- season: read season_file; set best_time {{"months": [...], "label": "...", "kind": "..."}}
  only if the species has a moment marked "striking" or "worth the trip" and this tree
  is the kind that shows it. Otherwise leave it. Scarcity is the point.

Answer: a JSON list written to out/enrich/{slug}.answer.json, one object per tree you
improved: {{"id", "register_url"?, "register_name"?, "register_id"?, "add_source"?, "girth_cm"?, "height_m"?, "measure_source"?, "access"?, "best_time"?}}.
Do not edit data/ yourself. No em dashes.

TREES:
{json.dumps(items, ensure_ascii=False, indent=1)}
""")


def apply(path):
    ans = json.load(open(path, encoding="utf-8"))
    by = {a["id"]: a for a in ans}
    changed = 0
    for f in glob.glob(os.path.join(CITIES, "*.json")):
        d = json.load(open(f, encoding="utf-8"))
        hit = False
        for t in d["trees"]:
            a = by.get(t["id"])
            if not a:
                continue
            src = t.setdefault("verified_sources", [])
            for k in ("add_source", "measure_source"):
                u = a.get(k)
                if u and u.startswith("http") and u not in src:
                    src.append(u)
            url = str(a.get("register_url") or "")
            if a.get("register_name") and (url.startswith("http") or a.get("register_id")):
                name = a["register_name"] + (f", no. {a['register_id']}" if a.get("register_id") else "")
                t["official_register"] = {"name": name, "url": url if url.startswith("http") else None}
                if url.startswith("http") and url not in src:
                    src.append(url)
            ok_measure = bool(a.get("measure_source"))
            for k in ("girth_cm", "height_m"):
                if a.get(k) and ok_measure and not t.get(k):
                    t[k] = a[k]
            if a.get("access") and a.get("add_source"):
                t["access"] = a["access"].replace("—", ",")
            if a.get("best_time") and not t.get("best_time"):
                t["best_time"] = a["best_time"]
            hit = True
            changed += 1
        if hit:
            with open(f, "w", encoding="utf-8") as fh:
                json.dump(d, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
    slug = os.path.basename(path).split(".")[0]
    if os.path.exists(os.path.join(CITIES, slug + ".json")):
        mark_done(slug)
    print(f"applied to {changed} tree(s); {slug} marked enriched for 14 days. Now run: python3 scripts/preflight.py")


def main():
    a = sys.argv[1:]
    if "--brief" in a:
        return brief(a[a.index("--brief") + 1])
    if "--apply" in a:
        return apply(a[a.index("--apply") + 1])
    rows = city_rows()
    if "--done" in a:
        mark_done(a[a.index("--done") + 1])
        return print("marked")
    if "--next" in a:
        # No pass under six gaps (CLAUDE.md, the assembly line): a pass has a fixed cost.
        rows = [r for r in rows if not recently_done(r[0]) and r[3] >= 6]
        if rows:
            slug, imp, ix, n, g = rows[0]
            print(f"enrich next: {slug} ({n} gaps on {ix} indexed trees). python3 scripts/enrich.py --brief {slug}")
        else:
            print("enrich: nothing to do on the proven cities")
        return
    show(rows)


if __name__ == "__main__":
    main()
