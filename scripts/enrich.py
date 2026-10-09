#!/usr/bin/env python3
"""Enrich the tree pages of the proven cities, before adding pages anywhere.

Hidde, 2026-10-06 ("ja"), on Google's guidance after the 09-28 demotion: a
page should carry what no AI can make up, and we did very little with it.
Measured that day on the 943 indexed tree pages (the ones with a photograph):
53% carried a measurement, 43% a season, 19% concrete opening facts, 2% a
reader's photograph, and 12% named an official register. So this is the night
run's FIRST work, above verifying new trees (prepare.py prints it first).

Widened on 2026-10-09 (Hidde: "do this"), because the first version was not
doing the job. It looked only at INDEXED trees (the photographed ones, 5 to 14
per city) while 2,311 of the 2,822 tree pages in the proven cities sat out of
the index with nothing working on them, and it marked a whole city done after
ONE pass whatever it had closed: 52 cities were "done" on 10-06 and 10-07 with
Singapore still at 3 gaps, Lisbon 13, Seville 19, London 48, Munich 40, and the
queue had moved on to Tallinn. Measured 2026-10-09 on the trees live since
09-27: stories changed on 4, a register link gained on 215, a girth on 62, a
height on 70. The content had not changed; only what Google was allowed to see.

So now:
  * EVERY tree in a proven city is in scope, indexed first, then the rest.
  * A finished page RETURNS TO THE INDEX (findable.enriched(), read by
    thin_pages.py): findable on the ground, plus register, measurement and
    concrete access. That is what each pass is working toward.
  * A city leaves the queue only when every gap on every tree is closed or is
    recorded as a dead end for THAT tree and THAT gap. A pass records dead
    ends for the trees it was briefed on and nothing else; dead ends expire
    after DEAD_END_DAYS so a new register or a new source gets its chance.

What counts as a gap:
  pin          not findable: no photo, pin not confirmed, no small site + line
  register     no official register named (site/src/lib/official-register.ts)
  measurement  no girth_cm and no height_m
  access       the access line has no hours, no "free"/price and no days
  season       no best_time, while data/phenology/ has a file for the species

Usage:
  python3 scripts/enrich.py              # per proven city, open gaps, by pre-demotion impressions
  python3 scripts/enrich.py --next       # the one city to enrich now
  python3 scripts/enrich.py --brief <city>   # paste-ready brief for an agent (writes out/enrich/<city>.brief.json)
  python3 scripts/enrich.py --apply <file>   # merge an agent's answer (out/enrich/<city>.answer.json)
  python3 scripts/enrich.py --done <city>    # a pass that closed nothing: dead-end the briefed gaps
  python3 scripts/enrich.py --status         # how many pages the enriched rule returns to the index

The answer file is a JSON list of {"id", optional "add_source" (a URL the
agent opened: the authority's own record, the site's own page), "girth_cm",
"height_m", "measure_source", "access", "best_time", "register_url",
"register_name", "register_id", "location_site" {"name","radius_m","source"},
"pin" {"latitude","longitude","source"}}. Nothing is written without a
source, and the apply step refuses a measurement, an access line, a site or a
pin that arrives without one.
"""
import datetime
import glob
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from findable import findable, has_photo, enriched, SITE_MAX_M  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CITIES = os.path.join(ROOT, "data", "cities")
OUT = os.path.join(ROOT, "out", "enrich")
LEDGER = os.path.join(ROOT, "data", "enrich-done.json")
DEAD_END_DAYS = 90
BRIEF_MAX = 20          # trees per pass: a brief's cost is set by its stopping condition
PIN_MOVE_MAX_M = 300    # the same guard sightings_publish.move_pin applies to a reader's fix

RECORD = re.compile(
    r"online\.bunka\.go\.jp/.*detail/|kunishitei\.bunka\.go\.jp/heritage/detail/|kyoju\.biodic\.go\.jp/.*gtsearchdetail"
    r"|crfop\.gdos\.gov\.pl/.*viewpomnikprzyrody|inventaris\.onroerenderfgoed\.be/erfgoedobjecten/|heritagetrees\.nparks\.gov\.sg/ht-"
    r"|comune\.milano\.it/.*/alberi-monumentali/|mediambient\.gencat\.cat/.*arbres-monumentals/|heritage\.go\.kr/heri/cul/culSelectDetail"
    r"|drusop\.nature\.cz/.*pstromy|nycgovparks\.org/.*great-trees"
    r"|barcelona\.cat/.*(trees-of-local-interest|arboles-de-interes-local|arbres-d-interes-local)|geneve\.ch/.*arbres-particuliers/")
REG_SLUGS = [os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, "data", "registers", "*.json"))]
CONCRETE = re.compile(r"\d{1,2}[:.h]\d{2}|\b(free|gratis|daylight|dawn|dusk|always open|open all|24 hours|eur|€|\$|£|¥|ticket|closed)\b", re.I)
PHEN = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, "data", "phenology", "*.json"))}


def species_slug(t):
    common = (t.get("species") or "").split("(")[0].strip().lower()
    return re.sub(r"[^a-z0-9]+", "-", common).strip("-")


def gaps(t):
    """Every open gap on a tree, dead ends included. See open_gaps()."""
    out = []
    if not findable(t):
        out.append("pin")
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


# ---- the ledger: dead ends per tree and gap --------------------------------

def ledger():
    try:
        d = json.load(open(LEDGER))
    except (OSError, ValueError):
        return {"trees": {}}
    if "trees" not in d:
        # The first shape (2026-10-06 to 10-08) was {city: date}, one date per
        # city after one pass. Dropped deliberately: those marks are what let
        # 52 cities leave the queue in two days with their gaps open.
        return {"trees": {}}
    return d


def save_ledger(led):
    led["_note"] = ("Dead ends per tree and gap: a pass briefed on this tree looked for this and found nothing, "
                    "on this date. Expires after %d days. Written by scripts/enrich.py --apply / --done, read by "
                    "--next; a city stays in the queue until every gap is closed or dead-ended." % DEAD_END_DAYS)
    led["trees"] = dict(sorted(led["trees"].items()))
    with open(LEDGER, "w") as fh:
        json.dump(led, fh, indent=1)
        fh.write("\n")


def dead(led, tid, gap, today=None):
    d = (led.get("trees") or {}).get(tid, {}).get(gap)
    if not d:
        return False
    today = today or datetime.date.today()
    return (today - datetime.date.fromisoformat(d)).days < DEAD_END_DAYS


def open_gaps(t, led):
    return [g for g in gaps(t) if not dead(led, t["id"], g)]


# ---- the queue ---------------------------------------------------------------

def roster():
    try:
        d = json.load(open(os.path.join(ROOT, "data", "depth-roster-frozen.json")))
        return list(d["cities"].items())
    except (OSError, ValueError, KeyError):
        return []


def city_trees(slug):
    p = os.path.join(CITIES, slug + ".json")
    if not os.path.exists(p):
        return None, []
    d = json.load(open(p, encoding="utf-8"))
    return d, d.get("trees", [])


def city_rows():
    led = ledger()
    rows = []
    for slug, v in roster():
        d, trees = city_trees(slug)
        if not trees:
            continue
        g = {t["id"]: open_gaps(t, led) for t in trees}
        n = sum(len(x) for x in g.values())
        if n:
            rows.append((slug, v.get("impressions", 0), sum(1 for t in trees if has_photo(t)), len(trees), n, g))
    return rows


def show(rows, limit=None):
    print("ENRICH: open gaps on every tree page of the proven cities, by pre-demotion impressions (dead ends excluded)")
    print("| City | Impressions 09-27 | Indexed | Trees | Gaps | pin | register | measurement | access | season |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for slug, imp, ix, n_trees, n, g in rows[:limit]:
        c = {k: sum(k in x for x in g.values()) for k in ("pin", "register", "measurement", "access", "season")}
        print(f"| {slug} | {imp} | {ix} | {n_trees} | {n} | {c['pin']} | {c['register']} | {c['measurement']} | {c['access']} | {c['season']} |")


def status():
    """How many tree pages the enriched rule returns to the index, and what stands between the rest and it."""
    led = ledger()
    tot = back = photo = 0
    short = {"pin": 0, "register": 0, "measurement": 0, "access": 0}
    for slug, _ in roster():
        _, trees = city_trees(slug)
        for t in trees:
            tot += 1
            if has_photo(t):
                photo += 1
                continue
            g = gaps(t)
            if enriched(t, g):
                back += 1
            for k in short:
                if k in g:
                    short[k] += 1
    print(f"proven cities: {tot} trees, {photo} indexed by photograph, {back} more indexed by being finished (findable + register + measurement + access).")
    print("still short on the rest: " + ", ".join(f"{k} {v}" for k, v in short.items()))


# ---- the brief ---------------------------------------------------------------

def brief(slug):
    d, trees = city_trees(slug)
    if d is None:
        sys.exit(f"no such city: {slug}")
    led = ledger()
    items = []
    # Indexed trees first (their page is already in Google and gets better),
    # then the rest, which RETURN to Google the day they are finished.
    for t in sorted(trees, key=lambda t: (not has_photo(t), not findable(t))):
        g = open_gaps(t, led)
        if not g:
            continue
        loc = t.get("location") or {}
        items.append({"id": t["id"], "name": t["name"], "species": t.get("species"),
                      "address": loc.get("address"),
                      "lat": loc.get("latitude"), "lng": loc.get("longitude"),
                      "location_precision": t.get("location_precision"),
                      "indexed": has_photo(t),
                      "access": t.get("access"), "gaps": g,
                      "sources": t.get("verified_sources") or [],
                      "season_file": f"data/phenology/{species_slug(t)}.json" if "season" in g else None})
        if len(items) >= BRIEF_MAX:
            break
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f"{slug}.brief.json"), "w", encoding="utf-8") as fh:
        json.dump({"city": slug, "date": datetime.date.today().isoformat(),
                   "trees": {i["id"]: i["gaps"] for i in items}}, fh, indent=1)
    print(f"""ENRICHMENT PASS: {d['city']} ({len(items)} trees with open gaps; indexed ones first). Use the verify agent.

Fill what each tree page lacks, from sources you actually open. Never invent: a gap
you cannot close stays a gap, and that is a finished answer (it is recorded as a dead
end for this tree, so say nothing rather than something thin). Time-box: report after
about forty minutes.

WHY: a tree page in this city returns to Google the day it is findable AND carries a
register record, a measurement and concrete access (scripts/findable.py enriched()).
A tree marked "indexed": false is out of Google now and comes back when you finish it.

Per gap:
- pin: the tree is not findable (pin approximate, no photograph). Two honest ways to
  close it, both from evidence you can name: (a) location_site: a SMALL named site
  taken in at one glance (a churchyard, a cemetery gate, a square, a cloister; radius
  at most {SITE_MAX_M} m; never a park, campus or garden you walk through) with the
  source that places the tree there; or (b) pin: a coordinate from the register's own
  record, Wikidata, OpenStreetMap or an aerial check per BRIEF_RESEARCH.md, with its
  source, within {PIN_MOVE_MAX_M} m of our pin. A coordinate you reasoned your way to is not
  evidence. Leave it open otherwise.
- register: find the AUTHORITY'S OWN RECORD for this tree (a government or national
  register page about this one tree: Naturdenkmal entry, monumental-tree sheet,
  heritage-tree page). Return register_url (that page) and register_name (the
  register's own name, e.g. "Arvoredo de Interesse Público (ICNF)"). A register
  homepage, a data endpoint or a news article is not a record. Where the register
  has NO per-tree page but you found this tree's own entry in its data, return
  register_name and register_id (the register's number for this tree) instead.
- measurement: girth_cm and/or height_m from a register, a plaque or the authority's
  page, with measure_source. Girth is circumference at 1.30 m; a base circumference is
  not a girth, leave it out. Never from our own story, never the species' maximum.
- access: one plain line a visitor can act on: free or the price, opening days and
  hours where the site publishes them, from the site's own page (add it as add_source).
  Keep what the current line says that is still true.
- season: read season_file; set best_time {{"months": [...], "label": "...", "kind": "..."}}
  only if the species has a moment marked "striking" or "worth the trip" and this tree
  is the kind that shows it. Otherwise leave it. Scarcity is the point.

Answer: a JSON list written to out/enrich/{slug}.answer.json, one object per tree you
improved: {{"id", "register_url"?, "register_name"?, "register_id"?, "add_source"?, "girth_cm"?,
"height_m"?, "measure_source"?, "access"?, "best_time"?,
"location_site"? {{"name", "radius_m", "source"}}, "pin"? {{"latitude", "longitude", "source"}}}}.
Trees you looked at and could not improve need no entry. Do not edit data/ yourself. No em dashes.

TREES:
{json.dumps(items, ensure_ascii=False, indent=1)}
""")


# ---- apply -------------------------------------------------------------------

def _dist_m(lat1, lng1, lat2, lng2):
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _is_url(u):
    return isinstance(u, str) and u.startswith("http")


def record_dead_ends(slug, led, today):
    """Every gap still open on a briefed tree becomes a dead end dated today."""
    bf = os.path.join(OUT, f"{slug}.brief.json")
    try:
        briefed = json.load(open(bf)).get("trees") or {}
    except (OSError, ValueError):
        print(f"no brief on disk for {slug} (out/enrich/{slug}.brief.json): nothing dead-ended. Run --brief first next time.")
        return 0
    _, trees = city_trees(slug)
    by = {t["id"]: t for t in trees}
    n = 0
    for tid, asked in briefed.items():
        t = by.get(tid)
        if not t:
            continue
        still = set(gaps(t)) & set(asked)
        for g in still:
            led["trees"].setdefault(tid, {})[g] = today
            n += 1
    return n


def apply(path):
    ans = json.load(open(path, encoding="utf-8"))
    by = {a["id"]: a for a in ans}
    changed = 0
    notes = []
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
                if _is_url(u) and u not in src:
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
            site = a.get("location_site") or {}
            if site:
                try:
                    r = float(site.get("radius_m"))
                except (TypeError, ValueError):
                    r = 0
                if (site.get("name") or "").strip() and 0 < r <= SITE_MAX_M and _is_url(site.get("source")):
                    t["location_site"] = {"name": site["name"].strip(), "radius_m": r}
                    if site["source"] not in src:
                        src.append(site["source"])
                else:
                    notes.append(f"{t['id']}: location_site refused (needs a name, radius 1-{SITE_MAX_M} m and a source URL)")
            pin = a.get("pin") or {}
            if pin:
                loc = t.setdefault("location", {})
                try:
                    lat, lng = float(pin["latitude"]), float(pin["longitude"])
                    dist = _dist_m(float(loc["latitude"]), float(loc["longitude"]), lat, lng)
                except (KeyError, TypeError, ValueError):
                    dist = None
                if dist is None or not _is_url(pin.get("source")):
                    notes.append(f"{t['id']}: pin refused (needs latitude, longitude and a source URL)")
                elif t.get("location_precision") == "confirmed":
                    notes.append(f"{t['id']}: pin already confirmed; not moved ({dist:.0f} m away). A confirmed pin needs a source-led correction, not an enrichment pass.")
                elif dist > PIN_MOVE_MAX_M:
                    notes.append(f"{t['id']}: pin NOT moved, the source's coordinate is {dist:.0f} m from ours (limit {PIN_MOVE_MAX_M}). Somebody has to look at this one.")
                else:
                    loc["latitude"], loc["longitude"] = lat, lng
                    t["location_precision"] = "confirmed"
                    t["pin_source"] = {"kind": "enrich", "url": pin["source"], "date": datetime.date.today().isoformat(),
                                       "moved_m": round(dist)}
                    if pin["source"] not in src:
                        src.append(pin["source"])
            hit = True
            changed += 1
        if hit:
            with open(f, "w", encoding="utf-8") as fh:
                json.dump(d, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
    slug = os.path.basename(path).split(".")[0]
    led = ledger()
    today = datetime.date.today().isoformat()
    n_dead = record_dead_ends(slug, led, today) if os.path.exists(os.path.join(CITIES, slug + ".json")) else 0
    save_ledger(led)
    for n in notes:
        print("NOTE " + n)
    print(f"applied to {changed} tree(s); {n_dead} gap(s) on the briefed trees recorded as dead ends for {DEAD_END_DAYS} days. "
          f"{slug} stays in the queue while it has open gaps. Now run: python3 scripts/preflight.py")


def done(slug):
    led = ledger()
    n = record_dead_ends(slug, led, datetime.date.today().isoformat())
    save_ledger(led)
    print(f"{n} gap(s) on the briefed trees of {slug} recorded as dead ends for {DEAD_END_DAYS} days; the rest of the city stays in the queue.")


def main():
    a = sys.argv[1:]
    if "--brief" in a:
        return brief(a[a.index("--brief") + 1])
    if "--apply" in a:
        return apply(a[a.index("--apply") + 1])
    if "--done" in a:
        return done(a[a.index("--done") + 1])
    if "--status" in a:
        return status()
    rows = city_rows()
    if "--next" in a:
        # No pass under six gaps (CLAUDE.md, the assembly line): a pass has a fixed cost.
        rows = [r for r in rows if r[4] >= 6]
        if rows:
            slug, imp, ix, n_trees, n, g = rows[0]
            print(f"enrich next: {slug} ({n} open gaps on {n_trees} trees, {ix} indexed). python3 scripts/enrich.py --brief {slug}")
        else:
            print("enrich: nothing to do on the proven cities")
        return
    show(rows)


if __name__ == "__main__":
    main()
