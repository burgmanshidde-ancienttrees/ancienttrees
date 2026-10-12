#!/usr/bin/env python3
"""Match published trees to the register rows we already hold, by script.

2026-10-12: the cost meter showed enrichment passes spending 125k to 220k
tokens each, 15k to 40k per enriched tree, and much of it went on a job with
no judgement in it: find the tree's row in a register that sits in
data/registers/ already, copy the register's number into official_register
and its girth or height into the tree. Retrieval is a script; judgement needs
an agent. This is the retrieval half. enrich.py --brief runs it for its city
before it writes a brief, so an agent only gets what still needs judgement.

THE MATCH, per register (heights.py's rule, tightened):
  * a row within 5 m of our pin whose genus does not contradict ours, or
  * a row within 30 m whose genus agrees with ours (the Latin in our
    species' brackets against the register's species text).
  * Two different rows of ONE register in range is a skip, printed with both
    distances, never a guess. That is also how twins metres apart come out
    (BRIEF_RESEARCH.md: they fold into one entry, a person decides which).
    One exception, because it is not ambiguous: the best row sits within 1 m
    (our pin is that row's imported coordinate) and the next is beyond 10 m.
  * Several registers matching one tree is not ambiguity (Piemonte and MASAF
    are one survey): the first in PRIORITY order names the register, and each
    missing measurement comes from the first matching register that has it.
  * A row the register itself marks dead, felled or gone is never matched;
    such a near-miss is printed as a warning, because it may be our tree.
  * Registers whose coordinates are not tree level (Hawaii, Ireland at 100 m)
    are not matched by distance at all.

WHAT IT WRITES, never over an existing value:
  * official_register {name: "<register>, no. <id>", url: <per-tree record
    or null>} only while enrich.py's "register" gap is open on the tree.
  * girth_cm and height_m from the register's own measurement, with the unit
    each register is known to use (the caveats in each file: Portugal and
    Valencia in METRES, Portland and Wisconsin in feet and inches). Never a
    diameter turned into a girth and never a girth the register derived from
    a diameter (Christchurch, Hong Kong, Rouen, Castilla y Leon). Never from
    a group row (an ensemble's figure is not this trunk's). Sanity bounds:
    girth 50 to 3000 cm, height 3 to 120 m.
  * the per-tree record URL into verified_sources, and one verify_notes
    sentence naming register, number, distance and what was copied.

    python3 scripts/register_match.py               # dry run, all cities
    python3 scripts/register_match.py --city lisbon # one city
    python3 scripts/register_match.py --apply       # write
    python3 scripts/register_match.py --list        # print every match and skip
"""
import datetime
import glob
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CITIES = os.path.join(ROOT, "data", "cities")
REGS = os.path.join(ROOT, "data", "registers")

NEAR_M = 5
FAR_M = 30
GIRTH_CM = (50, 3000)
HEIGHT_M = (3, 120)

# Not matched by distance: their coordinates are not tree level.
NOT_TREE_LEVEL = {"hawaii-exceptional-trees", "ireland-heritage-trees", "japan-bunkacho", "tokyo",
                  "flanders-onroerend-erfgoed", "hamburg-naturdenkmale", "spain-aragon-arboledas-singulares",
                  "brisbane-significant-landscape-trees", "massachusetts-dcr-legacy-trees",
                  "quebec-city-arbres-remarquables", "spokane-heritage-trees"}

# Regional before national (BRIEF_RESEARCH.md), a per-tree link before none.
PRIORITY = ["piemonte-alberi-monumentali", "puglia-alberi-monumentali", "sardinia-alberi-monumentali",
            "italy-masaf"]


def num(v):
    try:
        f = float(str(v).replace(",", ".").strip())
        return f if f > 0 else None
    except (TypeError, ValueError):
        return None


UNIT = re.compile(r"([\d]+(?:[.,]\d+)?)\s*(cm|m)\b", re.I)


def with_unit(v):
    """'212 cm', 'Circa 250 cm', '2,5 m.', '16 m' -> (value, unit). 'Circa' is a register estimate; refused."""
    s = str(v or "")
    if not s or re.search(r"circa|ca\.|ongeveer|approx|~|-", s, re.I):
        return None
    m = UNIT.search(s)
    if not m:
        return None
    return float(m.group(1).replace(",", ".")), m.group(2).lower()


def cm_from_text(v):
    u = with_unit(v)
    if not u:
        return None
    return u[0] * 100 if u[1] == "m" else u[0]


def m_from_text(v):
    u = with_unit(v)
    if not u:
        return None
    return u[0] / 100 if u[1] == "cm" else u[0]


def ft(v):
    n = num(v)
    return n * 0.3048 if n else None


def portland_girth(r):
    # Units are inferred, not labelled: accept the circumference (feet) only
    # where the diameter (inches) agrees with it within a quarter.
    c, dia = num(r.get("circumference_ft")), num(r.get("diameter_in"))
    if not c or not dia or abs(dia * math.pi / 12 - c) > 0.25 * c:
        return None
    return c * 30.48


def portugal_ok(r):
    # The first rows of the ICNF file are shifted one column (last_measured
    # 45, girth 4 on a sixteen-year-old magnolia): trust a measurement only
    # where last_measured reads as a year.
    y = num(r.get("last_measured"))
    return bool(y and 1950 <= y <= 2030)


# slug -> (id field, name, girth_cm(row), height_m(row), per-tree url field)
G = lambda k: (lambda r: num(r.get(k)))                      # noqa: E731
GM = lambda k: (lambda r: (num(r.get(k)) or 0) * 100 or None)  # noqa: E731
H = lambda k: (lambda r: num(r.get(k)))                      # noqa: E731
NONE = lambda r: None                                         # noqa: E731

ADAPT = {
    "amsterdam-bijzondere-bomen": ("register_id", "Bijzondere bomen (Gemeente Amsterdam)", lambda r: cm_from_text(r.get("trunk_girth")), NONE, None),
    "andalucia-rediam": ("id", "Árboles y arboledas singulares de Andalucía (REDIAM, Junta de Andalucía)", NONE, NONE, "sheet_pdf"),
    "auckland-notable-trees": ("schedule_id", "Schedule 10 Notable Trees (Auckland Council)", NONE, NONE, None),
    "balears-arbres-singulars": ("register_id", "Catàleg d'Arbres Singulars (Govern de les Illes Balears)", NONE, NONE, None),
    "barcelona-ail": ("register_id", "Arbres d'interès local (Ajuntament de Barcelona)", lambda r: cm_from_text(r.get("girth")), lambda r: m_from_text(r.get("height_m")), None),
    "bayern-naturdenkmale": ("register_id", "Naturdenkmal (Bayerisches Landesamt für Umwelt)", NONE, NONE, None),
    "berlin-naturdenkmale": ("register_id", "Naturdenkmal (Land Berlin)", NONE, NONE, None),
    "bordeaux-metropole-remarquables": ("gid", "Patrimoine arboré remarquable (Bordeaux Métropole)", G("girth_cm"), H("height_m"), None),
    "brussels-arbres-remarquables": ("register_id", "Inventaire légal des arbres remarquables (heritage.brussels)", G("girth_cm"), NONE, "url"),
    "canada-capital-ncc-remarkable-trees": ("objectid", "Remarkable Trees (National Capital Commission)", NONE, NONE, None),
    "castilla-leon-arboles-notables": ("register_id", "Árboles Notables de Castilla y León (Junta de Castilla y León)", NONE, H("height_m"), None),
    "christchurch-district-plan-trees": ("schedule_ref", "District Plan scheduled trees (Christchurch City Council)", NONE, H("height_m"), None),
    "croatia-spomenici-prirode": (None, None, NONE, NONE, None),
    "czech-aopk-pamatne-stromy": ("kod", "Památné stromy (AOPK ČR, Ústřední seznam ochrany přírody)", G("girth_cm"), NONE, None),
    "estonia-eelis-yksikobjektid": ("register_id", "Kaitstavad looduse üksikobjektid (EELIS, Keskkonnaagentuur)", NONE, NONE, None),
    "finland-helsinki-luonnonmuistomerkit": ("register_id", "Luonnonmuistomerkit (City of Helsinki)", NONE, NONE, None),
    "geneva-sitg-arbres-remarquables": ("no_inventaire", "Inventaire des arbres isolés (SITG, République et canton de Genève)", G("circumference_cm"), H("height_m"), None),
    "graz-naturdenkmale": ("register_id", "Naturdenkmale Graz (Stadt Graz)", NONE, NONE, None),
    "hobart-significant-trees": ("planning_ref_no", "Significant Tree Register (City of Hobart)", NONE, NONE, None),
    "hongkong-ovt": ("ovt_no", "Register of Old and Valuable Trees (Development Bureau, Hong Kong)", NONE, H("height_m"), None),
    "italy-masaf": ("sheet_id", "Elenco degli alberi monumentali d'Italia (MASAF)", G("girth_cm"), H("height_m"), None),
    "lithuania-stvk-gpo": ("register_id", "Saugomų teritorijų valstybės kadastras (STVK)", NONE, NONE, None),
    "luxembourg-anf": ("register_id", "Arbres remarquables (Administration de la nature et des forêts)", NONE, NONE, None),
    "lyon-arbres-remarquables": ("register_id", "Arbres remarquables (Métropole de Lyon)", NONE, NONE, None),
    "melbourne-boroondara-significant-trees": ("group_id", "Significant Tree register (City of Boroondara)", GM("girth_m"), H("height_m"), None),
    "melbourne-yarra-significant-trees": ("ref", "City of Yarra Significant Trees register", NONE, H("height_m"), None),
    "navarra-parflu": ("feature_id", "Árboles singulares del Parque Fluvial de la Comarca de Pamplona (Gobierno de Navarra)", NONE, NONE, None),
    "navarra-sitna": (None, None, NONE, NONE, None),
    "netherlands-lrmb": ("nr", "Landelijk Register Monumentale Bomen (Bomenstichting)", NONE, NONE, None),
    "paris-arbres-remarquables": ("register_id", "Arbres remarquables de Paris (Ville de Paris)", G("girth_cm"), H("height_m"), None),
    "piemonte-alberi-monumentali": ("register_id", "Alberi monumentali del Piemonte (Regione Piemonte)", G("girth_cm"), H("height_m"), None),
    "poland-gdos-pomniki-przyrody": ("kodinspire", "Centralny Rejestr Form Ochrony Przyrody (GDOŚ), pomnik przyrody", NONE, NONE, "source_record_url"),
    "portland-heritage-trees": ("treeid", "City of Portland Heritage Trees (Portland Parks & Recreation)", portland_girth, lambda r: ft(r.get("height_ft")), None),
    "portugal-icnf": ("processo", "Arvoredo de Interesse Público (ICNF)",
                      lambda r: (num(r.get("girth_m")) or 0) * 100 if portugal_ok(r) else None,
                      lambda r: num(r.get("height_m")) if portugal_ok(r) else None, None),
    "puglia-alberi-monumentali": ("register_id", "Alberi monumentali della Puglia (Regione Puglia)", G("girth_cm"), H("height_m"), None),
    "rouen-foret-arbres-remarquables": ("id", "Arbres remarquables en forêt domaniale (Métropole Rouen Normandie, ONF)", NONE, lambda r: m_from_text(r.get("height")), "pdf_url"),
    "salzburg-naturdenkmale": ("register_id", "Naturdenkmal (Land Salzburg)", NONE, NONE, None),
    "sardinia-alberi-monumentali": ("register_id", "Alberi monumentali della Sardegna (Regione Autonoma della Sardegna)", G("girth_cm"), H("height_m"), None),
    "singapore-heritage-trees": ("ht_id", "Heritage Trees Scheme (NParks)", NONE, NONE, "nparks_url"),
    "slovakia-chranene-stromy": ("register_id", "Chránené stromy (Štátna ochrana prírody SR)", NONE, NONE, "detail_url"),
    "spain-aragon-arboles-singulares": ("sitecode", "Árboles Singulares de Aragón (Gobierno de Aragón)", NONE, NONE, None),
    "strasbourg-arbres-remarquables": (None, None, NONE, NONE, None),
    "tenerife-santacruz-arboles-singulares": ("geocodigo", "Árboles singulares (Ayuntamiento de Santa Cruz de Tenerife)", NONE, NONE, None),
    "toulouse-metropole-remarquables": ("id", "Arbres remarquables (Toulouse Métropole)", NONE, NONE, None),
    "valencia-arboles-monumentales": ("register_id", "Catálogo de Árboles Monumentales y Singulares de la Comunitat Valenciana (Generalitat Valenciana)", GM("girth_m"), H("height_m"), None),
    "wien-naturdenkmale": ("register_id", "Naturdenkmal Wien (Stadt Wien)", NONE, NONE, None),
    "wisconsin-dnr-champion-trees": ("objectid", "Wisconsin Champion Trees (Wisconsin DNR)",
                                     lambda r: (num(r.get("circumference_in")) or 0) * 2.54 or None,
                                     lambda r: ft(r.get("height_ft")), None),
}

SPECIES_KEYS = ("species", "species_latin", "botanical_name", "scientific_name", "genus", "species_pl_latin",
                "species_fr", "species_de", "species_guess_fr", "species_nl", "name", "name_it", "name_pt")


def rows_of(d):
    if isinstance(d, list):
        return d
    for k in ("trees", "entries", "rows", "data", "features"):
        if isinstance(d.get(k), list):
            return d[k]
    return []


def flat(r):
    """A GeoJSON feature becomes a plain row with latitude/longitude."""
    if r.get("type") == "Feature":
        p = dict(r.get("properties") or {})
        g = r.get("geometry") or {}
        if g.get("type") == "Point":
            p["longitude"], p["latitude"] = g["coordinates"][:2]
        return p
    return r


def is_group(r):
    if r.get("group") is True:
        return True
    for k in ("point_count", "quantity", "units", "n_trees", "tree_count", "number_trees", "individuals",
              "specimens_catalogued"):
        n = num(r.get(k))
        if n and n > 1:
            return True
    tipo = r.get("tipo")  # ICNF: an alameda or a conjunto is many trunks under one number
    if tipo and tipo not in ("Árvore isolada", "Exemplar isolado"):
        return True
    if str(r.get("description") or "").startswith("Groupe"):  # Rouen
        return True
    ot = str(r.get("object_type") or r.get("element") or "").upper()
    return bool(ot) and ot not in ("ALBERO SINGOLO", "ÁRBOL", "ARBOL")


def is_dead(slug, r):
    if r.get("death_signal") or r.get("date_disparition") or r.get("check_alive"):
        return True
    if r.get("status_life") not in (None, "VIVANT"):
        return True
    if slug == "netherlands-lrmb" and r.get("status") == 5:
        return True
    if r.get("specimens_remaining") == 0:
        return True
    return False


def latin_genus(species):
    m = re.search(r"\(([A-Z][a-z]+)", species or "")
    return m.group(1).lower() if m else ""


def load(genera):
    out = []
    for f in sorted(glob.glob(os.path.join(REGS, "*.json"))):
        slug = os.path.basename(f)[:-5]
        if slug in NOT_TREE_LEVEL or slug not in ADAPT or not ADAPT[slug][0]:
            continue
        idk, name, gfn, hfn, urlk = ADAPT[slug]
        try:
            d = json.load(open(f, encoding="utf-8"))
        except ValueError:
            continue
        rows = [flat(r) for r in rows_of(d) if isinstance(r, dict)]
        # A url column counts as a per-tree record only when it differs per row.
        if urlk:
            urls = [r.get(urlk) for r in rows if r.get(urlk)]
            if not urls or len(set(urls)) < 0.9 * len(urls):
                urlk = None
        for r in rows:
            la, ln = num(r.get("latitude")), r.get("longitude")
            try:
                ln = float(ln)
            except (TypeError, ValueError):
                continue
            if not la or r.get(idk) in (None, ""):
                continue
            words = " ".join(str(r.get(k) or "") for k in SPECIES_KEYS)
            g = next((w.lower() for w in re.findall(r"[A-Z][a-z]+", words) if w.lower() in genera), "")
            rid = str(r[idk])
            if rid.endswith(".0"):
                rid = rid[:-2]
            out.append({"slug": slug, "id": rid, "name": name, "lat": la, "lng": ln, "genus": g,
                        "girth": None if is_group(r) else gfn(r), "height": None if is_group(r) else hfn(r),
                        "url": r.get(urlk) if urlk else None, "dead": is_dead(slug, r), "group": is_group(r)})
    return out


def metres(a, b, c, d):
    return math.hypot((a - c) * 111320.0, (b - d) * 111320.0 * math.cos(math.radians(a)))


def grid(rows):
    g = {}
    for r in rows:
        g.setdefault((round(r["lat"], 3), round(r["lng"], 3)), []).append(r)
    return g


def near(g, la, ln):
    k0, k1 = round(la, 3), round(ln, 3)
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            yield from g.get((round(k0 + i / 1000, 3), round(k1 + j / 1000, 3)), [])


def match_tree(t, g):
    """-> (matches [(row, d)] in priority order, skips [str], dead_warnings [str])."""
    loc = t.get("location") or {}
    la, ln = loc.get("latitude"), loc.get("longitude")
    if not la or not ln:
        return [], [], []
    tg = latin_genus(t.get("species"))
    per = {}
    dead = []
    for r in near(g, la, ln):
        d = metres(la, ln, r["lat"], r["lng"])
        if d > FAR_M:
            continue
        agree = bool(tg and r["genus"] and tg == r["genus"])
        conflict = bool(tg and r["genus"] and tg != r["genus"])
        if not ((d <= NEAR_M and not conflict) or agree):
            continue
        if r["dead"]:
            dead.append(f"{r['slug']} no. {r['id']} ({d:.0f} m) is marked dead or gone in the register")
            continue
        per.setdefault(r["slug"], []).append((r, d))
    matches, skips = [], []
    for slug, cands in per.items():
        cands.sort(key=lambda x: x[1])
        ids = {}
        for r, d in cands:
            ids.setdefault(r["id"], (r, d))
        cands = list(ids.values())
        if len(cands) == 1 or (cands[0][1] <= 1 and cands[1][1] > 10):
            matches.append(cands[0])
        else:
            skips.append(f"{slug}: " + ", ".join(f"no. {r['id']} at {d:.0f} m" for r, d in cands[:4]))
    rank = {s: i for i, s in enumerate(PRIORITY)}
    matches.sort(key=lambda x: (x[0]["url"] is None, rank.get(x[0]["slug"], len(PRIORITY)), x[1]))
    return matches, skips, dead


def plan(t, matches, register_gap):
    """What a match would write on this tree: dict of field -> (value, row, d)."""
    out = {}
    if matches and register_gap and not t.get("official_register"):
        r, d = matches[0]
        out["official_register"] = ({"name": f"{r['name']}, no. {r['id']}", "url": r["url"]}, r, d)
    for field, key, lo_hi, nd in (("girth_cm", "girth", GIRTH_CM, 0), ("height_m", "height", HEIGHT_M, 1)):
        if t.get(field):
            continue
        for r, d in matches:
            v = r[key]
            if v and lo_hi[0] <= v <= lo_hi[1]:
                v = round(v, nd)
                out[field] = (int(v) if nd == 0 else v, r, d)
                break
    return out


def run(city=None, write=False, verbose=False, quiet=False):
    from enrich import gaps  # noqa: E402  (enrich imports nothing from here at module level)
    genera = set()
    files = sorted(glob.glob(os.path.join(CITIES, "*.json")))
    docs = {}
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        docs[f] = d
        for t in d.get("trees", []):
            g = latin_genus(t.get("species"))
            if g:
                genera.add(g)
    g = grid(load(genera))
    today = datetime.date.today().isoformat()
    tot = {"trees": 0, "enriched": 0, "register": 0, "girth_cm": 0, "height_m": 0, "ambiguous": 0, "dead": 0}
    skipped, deadlist, lines = [], [], []
    tot["skips_by_id"] = {}
    for f, d in docs.items():
        slug = os.path.basename(f)[:-5]
        if city and slug != city:
            continue
        touched = False
        for t in d.get("trees", []):
            tot["trees"] += 1
            matches, skips, dead = match_tree(t, g)
            if dead and not matches:
                tot["dead"] += 1
                deadlist.append(f"{slug}/{t['id']} {t['name']}: " + "; ".join(dead))
            if skips and not matches:
                tot["ambiguous"] += 1
                skipped.append(f"{slug}/{t['id']} {t['name']}: " + " | ".join(skips))
                tot["skips_by_id"][t["id"]] = skips
            if not matches:
                continue
            p = plan(t, matches, "register" in gaps(t))
            if not p:
                continue
            tot["enriched"] += 1
            for k in p:
                tot["register" if k == "official_register" else k] += 1
            r0, d0 = matches[0]
            lines.append(f"{slug}/{t['id']} {t['name']}: " + ", ".join(
                f"{k}={v['name'] if k == 'official_register' else v} ({r['slug']} {d:.0f} m)" for k, (v, r, d) in p.items())
                + (f"   [also skipped: {' | '.join(skips)}]" if skips else ""))
            if not write:
                continue
            for k, (v, r, dist) in p.items():
                t[k] = v
            src = t.setdefault("verified_sources", [])
            notes = []
            for rr, dd in {id(r): (r, dist) for k, (v, r, dist) in p.items()}.values():
                what = [k.replace("official_register", "register number").replace("_cm", "").replace("_m", "")
                        for k, (v, r, _d) in p.items() if r is rr]
                cite = f"{rr['slug']}.json, no. {rr['id']}"
                if rr["url"] and rr["url"] not in src:
                    src.append(rr["url"])
                elif not any(rr["slug"] in str(s) for s in src):
                    src.append(cite)
                notes.append(f"{' and '.join(what).capitalize()} from {rr['name']} no. {rr['id']} "
                             f"(data/registers/{rr['slug']}.json), matched on our pin at {dd:.0f} m "
                             f"(register_match.py, {today}).")
            existing = t.get("verify_notes") or ""
            add = " ".join(n for n in notes if n not in existing)
            if add:
                t["verify_notes"] = (existing + " " if existing else "") + add
            touched = True
        if touched:
            with open(f, "w", encoding="utf-8") as fh:
                json.dump(d, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
    if verbose:
        for x in lines:
            print("MATCH " + x)
    if quiet:
        return tot
    for x in skipped:
        print("AMBIGUOUS " + x)
    for x in deadlist:
        print("REGISTER SAYS GONE " + x)
    print(f"{'wrote' if write else 'would write'}: {tot['enriched']} of {tot['trees']} trees enriched "
          f"(register number {tot['register']}, girth {tot['girth_cm']}, height {tot['height_m']}); "
          f"{tot['ambiguous']} skipped as ambiguous, {tot['dead']} near a row the register marks gone.")
    return tot


def main():
    a = sys.argv[1:]
    city = a[a.index("--city") + 1] if "--city" in a else None
    run(city=city, write="--apply" in a, verbose="--list" in a)


if __name__ == "__main__":
    main()
