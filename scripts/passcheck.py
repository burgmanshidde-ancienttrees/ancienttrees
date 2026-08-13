#!/usr/bin/env python3
"""Everything you must know about a place BEFORE writing a research brief.

Three passes have now been sent out to "open" a city that was already live
(Napoli, Firenze, Munich), each time because a queue entry said new and nobody
checked. Munich alone cost 127,000 tokens to discover the page had existed for
eleven days. The rule to check first has been written down twice and failed
twice, so this is the mechanism instead: one command, run before any brief.

    python3 scripts/passcheck.py Munich
    python3 scripts/passcheck.py Torino          works in the local language too
    python3 scripts/passcheck.py 45.07 7.68      or by coordinate
    python3 scripts/passcheck.py --brief Valencia

--brief prints a complete, paste-ready verification brief: status, ids,
delivery format, the actual register candidates near the place (not a count, a
list), what an earlier pass already found or rejected, and the hosts that hang.
A brief written by this script cannot leave on a false premise, because it is
generated from the same data the premise would have to contradict.

    python3 scripts/passcheck.py --claim Galway --kind verify   before dispatching
    python3 scripts/passcheck.py --release Galway               when merged

--claim records the pass in data/in-flight.json BEFORE it is dispatched, and
--brief refuses a claimed place. This is the other half of the same disease:
passcheck knew what was published, nothing knew what was in flight, and on
2026-08-06 a session and a night run wrote the same nine Padova stories twenty
minutes apart. Claims expire after 4 hours by themselves, so a dead session
cannot block a city. Commit and push the claim, or the night runs cannot see
it: the push is part of the claim.
"""
import datetime
import glob
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import km  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAME_CITY_KM = 20.0
NEAR_PUBLISHED_KM = 0.08  # a register entry this close to a live tree is probably that tree
LEAD_MATCH_KM = 0.025     # ...and this close to a recorded lead is probably that lead

# Local name to our slug, for the cases a name lookup alone would miss. Distance
# is the real test; this only helps the first guess.
def _load_aliases():
    """Local spelling -> the English name this site publishes under.

    Lives in data/city-aliases.json so the build check and this generator read
    one table instead of two that drift: the build refuses to ship a city under
    a local name, and this file needs the same pairs read backwards to find
    register candidates. The inline fallback keeps passcheck working if the data
    file is missing."""
    try:
        p = os.path.join(ROOT, "data", "city-aliases.json")
        with open(p) as fh:
            return json.load(fh)["aliases"]
    except Exception:
        return {"napoli": "naples", "firenze": "florence", "roma": "rome",
                "milano": "milan", "torino": "turin", "genova": "genoa",
                "venezia": "venice", "padova": "padua", "lisboa": "lisbon"}


ALIAS = _load_aliases()

NAME_FIELDS = ("name", "name_en", "name_pt", "name_it", "name_ja", "name_nl",
               "name_eu", "common_fr", "designation")
PLACE_FIELDS = ("comune", "concelho", "city", "municipality", "place", "locality",
                "lugar", "freguesia", "address", "area", "area_en", "district",
                "neighbourhood", "province", "prefecture", "distrito", "region",
                "arrondissement")


def fold(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def cities():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        d = json.load(open(f))
        trees = d.get("trees") or []
        if not trees:
            continue
        pts = [(t["location"]["latitude"], t["location"]["longitude"]) for t in trees]
        out.append({
            "city": d["city"], "slug": os.path.basename(f)[:-5], "n": len(trees),
            "photos": sum(1 for t in trees if (t.get("photo") or {}).get("url")),
            "approx": sum(1 for t in trees if t.get("location_precision") == "approximate"),
            "spread": max((km(a, b) for a in pts for b in pts), default=0.0),
            "ids": sorted(t["id"] for t in trees),
            "points": pts,
            "lat": sum(p[0] for p in pts) / len(pts),
            "lng": sum(p[1] for p in pts) / len(pts),
        })
    return out


def register_entries():
    """Yield every register entry, normalized: lat, lng, name, species, girth_m,
    age, place, file. Handles both flat entries and GeoJSON features."""
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "registers", "*.json"))):
        d = json.load(open(path))
        if not isinstance(d, dict):
            continue
        fname = os.path.basename(path)
        for t in (d.get("entries") or []) + (d.get("trees") or []):
            if t.get("group"):
                continue
            if "properties" in t and "geometry" in t:
                t = t.get("properties") or {}
            la, lo = t.get("latitude"), t.get("longitude")
            if la is None or lo is None:
                continue
            girth = t.get("girth_m")
            if girth is None and t.get("girth_cm"):
                try:
                    girth = float(t["girth_cm"]) / 100.0
                except (TypeError, ValueError):
                    girth = None
            yield {
                "lat": float(la), "lng": float(lo),
                "name": next((t[f] for f in NAME_FIELDS if t.get(f)), None),
                "species": t.get("species"),
                "girth_m": girth,
                "age": t.get("age_register") or t.get("age_band"),
                "place": ", ".join(str(t[f]) for f in PLACE_FIELDS[:6] if t.get(f)),
                "file": fname,
            }


def candidates_near(lat, lng, radius=SAME_CITY_KM):
    out = []
    for e in register_entries():
        d = km((lat, lng), (e["lat"], e["lng"]))
        if d <= radius:
            e["dist"] = d
            out.append(e)
    return sorted(out, key=lambda e: e["dist"])


_MINED = None


def mined_points():
    """Every tree an earlier pass already judged, with its coordinate and verdict.

    passcheck deduped register candidates against PUBLISHED trees only, so a tree
    a previous pass had already rejected came back in the next brief looking
    fresh. That is not theoretical: the Rome pass of 2026-08-10 spent its whole
    window rediscovering, by hand, that all 38 of its "candidates within 20 km"
    were already leads or blocked entries, and shipped nothing. The join was left
    to the agent to do by NAME, which the project's own rule forbids everywhere
    else, because registers and our own files spell the same tree differently.

    Matching is by coordinate, like the published check, so no spelling can fool
    it. Entries without a coordinate (roughly a third) cannot be matched this way
    and stay listed in the leads section below, unchanged.
    """
    global _MINED
    if _MINED is not None:
        return _MINED
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "leads", "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        for kind in ("leads", "blocked"):
            for e in (d.get(kind) or []):
                if not isinstance(e, dict):
                    continue
                loc = e.get("location") if isinstance(e.get("location"), dict) else e
                lat = loc.get("latitude", loc.get("lat"))
                lng = loc.get("longitude", loc.get("lng"))
                if lat is None or lng is None:
                    continue
                why = (e.get("why_not_published") or e.get("reason")
                       or e.get("why") or e.get("status") or "")
                out.append({"lat": float(lat), "lng": float(lng), "kind": kind,
                            "name": e.get("name", "?"), "why": why,
                            "species": e.get("species", ""),
                            "file": os.path.basename(f)})
    _MINED = out
    return out


def _genus(species):
    """First word of a botanical name, lowercased. The cheapest species guard
    there is, and enough: Cedrus is not Brahea."""
    if not species:
        return ""
    s = re.sub(r"[^A-Za-z ]", " ", str(species)).strip().lower().split()
    return s[0] if s else ""


def already_judged(lat, lng, species=None):
    """The lead or blocked entry at this spot, or None. Nearest wins.

    Two guards against a false match, which is the dangerous direction here: a
    wrong hit HIDES a real candidate, while a miss only costs the pass a second
    look. First, the radius is far tighter than the published-tree check (25 m
    against 80 m), because a lead and a register row describing the same tree
    usually come from the same survey and agree closely, while distinct trees in
    a dense park sit tens of metres apart. Second, when both sides name a
    species and the genus differs, it is not the same tree whatever the distance
    says. Both were written after a Himalayan Cedar matched a Mexican Blue Palm
    80 m away in Villa Sciarra.
    """
    g = _genus(species)
    hits = []
    for m in mined_points():
        d = km((lat, lng), (m["lat"], m["lng"]))
        if d > LEAD_MATCH_KM:
            continue
        mg = _genus(m.get("species"))
        if g and mg and g != mg:
            continue
        hits.append((d, m))
    return min(hits, key=lambda h: h[0])[1] if hits else None


def centre_from_registers(key):
    """A new city has no coordinates of ours yet. Infer a centre by matching the
    place name against the registers' own locality fields."""
    hits = [e for e in register_entries() if key and key in fold(e["place"])]
    if not hits:
        return None
    lats = sorted(e["lat"] for e in hits)
    lngs = sorted(e["lng"] for e in hits)
    return (lats[len(lats) // 2], lngs[len(lngs) // 2])


def centre_from_any_name(arg):
    """Locate a place in the registers by trying every name it might be filed
    under. The alias map exists to turn a local name into our English slug, and
    applying it here does the opposite of what is needed: registers file Genoa
    as "Genova", so translating the working name into English threw the match
    away and the brief said "no coordinates known" for a city with sixteen
    register entries. Try the raw name, the alias, and the alias read backwards.
    """
    key = fold(arg)
    reverse = {fold(v): k for k, v in ALIAS.items()}
    for candidate in (key, fold(ALIAS.get(key, "")), fold(reverse.get(key, ""))):
        if not candidate:
            continue
        centre = centre_from_registers(candidate)
        if centre:
            return centre
    return None


def _research_trees(loaded):
    """A *-verified.json is an array, but one pass delivered {"trees": [...]}
    and the pending check crashed instead of reading it. Tolerate both."""
    if isinstance(loaded, dict):
        return loaded.get("trees") or []
    return loaded if isinstance(loaded, list) else []


def pending_research():
    """Research files holding trees that are NOT yet published.

    Exists because "needs a story" is not the same question as "is not
    published", and briefing on the first one sent a write pass after seven
    trees on 2026-08-08 when only three were real: nyc_011-013 and ams_011 had
    been merged into their city files that morning, and the research files were
    stale leftovers nobody had deleted. The pass caught it and refused to write
    duplicates, which is the only reason good live prose was not overwritten.

    The published city file is the truth. A research entry whose id already
    lives in data/cities is finished work, whatever the research file says.

    UNLESS the id is a collision rather than a match, which is the case this
    check got badly wrong on 2026-08-10. A batch was prepared with ids starting
    at bcn_011 from a stale assumption that Barcelona held ten trees; it held
    33, so all eighteen ids belonged to different live trees. Matching on id
    alone, this function reported the whole file as published and told the pass
    to delete it. Thirteen unwritten trees would have gone, and merging as
    briefed would have overwritten eighteen indexed URLs.

    So an id match is only believed when the coordinates agree. Same tree, same
    place; a research entry sitting hundreds of metres from the live tree whose
    id it claims is a collision, and it is reported loudly rather than silently
    counted as done. This is the same rule the register and lead matching
    already follow: position cannot be fooled by a label."""
    live, live_pt = set(), {}
    for f in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
        for t in json.load(open(f)).get("trees", []):
            live.add(t["id"])
            loc = t.get("location") or {}
            if loc.get("latitude") is not None:
                live_pt[t["id"]] = (loc["latitude"], loc["longitude"])

    def same_tree(t):
        """Is this research entry really the live tree that holds its id?"""
        pt = live_pt.get(t["id"])
        loc = t.get("location") or {}
        if not pt or loc.get("latitude") is None:
            return True          # cannot tell; trust the id, as before
        return km(pt, (loc["latitude"], loc["longitude"])) <= 0.15

    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "research", "*-verified.json"))):
        try:
            rows = _research_trees(json.load(open(f)))
        except Exception:
            continue
        unpublished, stale, collisions = [], 0, []
        for t in rows:
            if not t.get("id"):
                continue
            if t["id"] not in live:
                unpublished.append(t)
            elif same_tree(t):
                stale += 1
            else:
                collisions.append(t)
        if unpublished or stale or collisions:
            out.append((os.path.relpath(f, ROOT), unpublished, stale, collisions))
    return out


def print_pending():
    rows = pending_research()
    if not rows:
        print("\nNothing pending: every verified tree is published.")
        return
    print("\nVERIFIED BUT NOT YET PUBLISHED (brief a write pass on these, and only these):")
    for path, unpublished, stale, collisions in rows:
        if unpublished:
            need = sum(1 for t in unpublished if not t.get("story"))
            print(f"  {path}: {len(unpublished)} unpublished "
                  f"({need} still need a story, {len(unpublished) - need} written and ready to merge)")
            for t in unpublished[:6]:
                print(f"      {t['id']} {str(t.get('name'))[:46]}")
        if collisions:
            print(f"  !! {path}: {len(collisions)} entries claim an id that belongs to a "
                  f"DIFFERENT live tree.")
            print(f"     These are NOT published and this file is NOT stale. Merging as-is "
                  f"would overwrite live, indexed trees (hard rule 3).")
            print(f"     Reassign them to free ids before writing or merging:")
            for t in collisions[:8]:
                print(f"      {t['id']} {str(t.get('name'))[:46]}")
        if stale:
            print(f"  {path}: {stale} entries ALREADY PUBLISHED, this file is stale; "
                  f"delete it once the rest is merged")


def resolve(arg, live):
    """Returns (match_or_None, coord_or_None). Distance is the real test."""
    coord = None
    parts = arg.replace(",", " ").split()
    if len(parts) == 2:
        try:
            coord = (float(parts[0]), float(parts[1]))
        except ValueError:
            coord = None
    if coord:
        match = min(live, key=lambda c: km(coord, (c["lat"], c["lng"])), default=None)
        if match and km(coord, (match["lat"], match["lng"])) > SAME_CITY_KM:
            match = None
        return match, coord
    key = fold(arg)
    key = fold(ALIAS.get(key, key))
    match = next((c for c in live if fold(c["city"]) == key or fold(c["slug"]) == key), None)
    if match is None:
        # name did not match a live city directly; try locating it via the
        # registers and distance-checking against every live city, which is how
        # Napoli/Naples-class misses get caught even without an alias entry
        coord = centre_from_any_name(arg)
        if coord:
            near = min(live, key=lambda c: km(coord, (c["lat"], c["lng"])), default=None)
            if near and km(coord, (near["lat"], near["lng"])) <= SAME_CITY_KM:
                match = near
    return match, coord


INFLIGHT = os.path.join(ROOT, "data", "in-flight.json")


def _now():
    return datetime.datetime.now(datetime.timezone.utc)


def load_inflight():
    """The claim file, with expired claims already dropped.

    Returns (doc, live_claims). A claim older than expire_hours is ignored, so a
    session that dies mid-pass cannot block a city forever: the worst case is
    that the next run waits out the remainder of the window."""
    try:
        doc = json.load(open(INFLIGHT))
    except Exception:
        return {"expire_hours": 4, "claims": []}, []
    hours = doc.get("expire_hours", 4)
    live = []
    for c in doc.get("claims", []):
        try:
            at = datetime.datetime.fromisoformat(c["claimed_at"])
            if at.tzinfo is None:
                at = at.replace(tzinfo=datetime.timezone.utc)
        except Exception:
            continue
        age = (_now() - at).total_seconds() / 3600.0
        if age < hours:
            c = dict(c, age_hours=round(age, 1))
            live.append(c)
    return doc, live


def save_inflight(doc, claims):
    doc["claims"] = [{k: v for k, v in c.items() if k != "age_hours"}
                     for c in claims]
    with open(INFLIGHT, "w") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def claims_for(target, live):
    key = fold(target)
    out = []
    for c in live:
        ck = fold(c.get("target", ""))
        # match either spelling: a claim on Padova blocks a pass on Padua
        if ck == key or ALIAS.get(ck) == ALIAS.get(key, key) or \
                ALIAS.get(ck, ck) == key or ck == ALIAS.get(key, key):
            out.append(c)
    return out


def print_inflight(target, live):
    """Print what is being worked on, loudest for the place being asked about."""
    mine = claims_for(target, live) if target else []
    if mine:
        print("\n  !! ALREADY CLAIMED, DO NOT DISPATCH:")
        for c in mine:
            print(f"     {c['target']} ({c['kind']}) claimed by {c.get('by', '?')} "
                  f"{c['age_hours']}h ago")
        print("     Another run is on this right now. Pick a different target, or")
        print("     --release it first if you know that pass is dead.")
    others = [c for c in live if c not in mine]
    if others:
        print("\n  in flight elsewhere: " + ", ".join(
            f"{c['target']}({c['kind']}, {c['age_hours']}h)" for c in others))


def do_claim(target, kind, by):
    doc, live = load_inflight()
    existing = claims_for(target, live)
    if existing:
        c = existing[0]
        print(f"REFUSED: {c['target']} ({c['kind']}) is already claimed by "
              f"{c.get('by', '?')}, {c['age_hours']}h ago.")
        print("Pick another target, or --release it if that pass is dead.")
        return 1
    live.append({"target": target, "kind": kind, "by": by,
                 "claimed_at": _now().replace(microsecond=0).isoformat()})
    save_inflight(doc, live)
    print(f"CLAIMED {target} ({kind}) by {by}.")
    print("Commit and push data/in-flight.json now, or the night runs cannot see it.")
    print(f"Release it when the output is merged: "
          f"python3 scripts/passcheck.py --release {target}")
    return 0


def do_release(target):
    doc, live = load_inflight()
    keep = [c for c in live if c not in claims_for(target, live)]
    if len(keep) == len(live):
        print(f"no live claim on {target} (already released, or it expired)")
    else:
        print(f"released {target}")
    save_inflight(doc, keep)
    return 0


def print_blocklist():
    bl = os.path.join(ROOT, "data", "fetch-blocklist.json")
    if not os.path.exists(bl):
        return
    hosts = json.load(open(bl))["hosts"]
    print("\nHOSTS THAT COST A WINDOW (they are why every fetch gets a hard timeout):")
    # Two entry schemas exist (the original behaviour/cost/seen fields, and a
    # 2026-08-08 addition using host/noted/symptom); normalize rather than
    # pick one, since a third addition should not break this a second time.
    def desc(v):
        return v.get("behaviour") or v.get("symptom") or ""
    for h, v in sorted(hosts.items(), key=lambda kv: 0 if "hang" in desc(kv[1]) else 1):
        d = desc(v)
        mark = "!!" if "hang" in d else "  "
        print(f" {mark} {h}: {d}. {v['workaround']}")
    print("    Every fetch: curl -m 20 (or timeout= on urllib). A hang burns the "
          "window; a refusal costs a second.")


def print_archived_notes(slug, place):
    """What CURATION.md and LOG.md already said about this place, including
    what has since moved to archive/.

    Hidde, 2026-08-08: "we willen geen bruikbare kennis verwijderen, we moeten
    slim oordelen wat weg kan en niet." Archiving moves nothing out of
    existence, but a file nothing reads is lost in practice, and telling runs
    to remember to grep is exactly the kind of rule this project has watched
    fail twice. So the grep runs here, automatically, at the one moment the
    knowledge matters: the brief. Age decides what moves; relevance decides
    what surfaces.
    """
    import re
    needles = {place.lower(), slug.replace("-", " ").lower()}
    hits = []
    files = [os.path.join(ROOT, f) for f in ("CURATION.md", "LOG.md")]
    files += sorted(glob.glob(os.path.join(ROOT, "archive", "*.md")))
    for f in files:
        if not os.path.exists(f):
            continue
        rel = os.path.relpath(f, ROOT)
        heading = ""
        for line in open(f, encoding="utf-8", errors="ignore"):
            if line.startswith("## "):
                heading = line[3:].strip()
                continue
            low = line.lower()
            # Word boundaries, or "cork" matches "Amur cork tree" and the
            # brief fills with noise the reader learns to skip.
            if any(re.search(r"\b" + re.escape(n) + r"\b", low)
                   for n in needles if len(n) > 3):
                snippet = re.sub(r"\s+", " ", line).strip()
                hits.append((rel, heading, snippet[:150]))
    if not hits:
        return
    print(f"\nALREADY WRITTEN ABOUT {place.upper()} (newest first, "
          f"{len(hits)} mention(s); read before repeating a hunt):")
    seen = set()
    shown = 0
    for rel, heading, snippet in hits:
        if heading in seen:
            continue
        seen.add(heading)
        print(f"  [{rel}] {heading}")
        print(f"      {snippet}")
        shown += 1
        if shown >= 6:
            break
    if len(seen) > shown:
        print(f"  ...and more: grep -ri \"{place}\" CURATION.md LOG.md archive/")


def print_wikidata(slug):
    """The CC0 Wikidata candidates harvested by scripts/wikidata_harvest.py.
    Banked 2026-08-09 (1,185 candidates, 660 with images) and wired here the
    same day, because a feed nothing reads is not a feed. Sitelinked articles
    are where second sources live; an image link is a photo candidate."""
    try:
        d = json.load(open(os.path.join(ROOT, "data", "research",
                                        "wikidata-candidates.json")))
    except Exception:
        return
    block = d.get("cities", {}).get(slug)
    if not block:
        return
    fresh = [c for c in block.get("candidates", []) if not c.get("probably_ours")]
    if not fresh:
        return
    print(f"\nWIKIDATA CANDIDATES (CC0, harvested {block.get('harvested')}): "
          f"{len(fresh)} not already ours; discovery AND corroboration feed.")
    for c in fresh[:12]:
        img = "img" if c.get("image") else "no-img"
        des = f"  [{c['designation']}]" if c.get("designation") else ""
        print(f"  {c['qid']}  {c.get('label','?')[:52]:<54} "
              f"({c['latitude']:.5f},{c['longitude']:.5f}) {img}{des}")
    if len(fresh) > 12:
        print(f"  ...and {len(fresh)-12} more in data/research/wikidata-candidates.json")


def print_leads(slug):
    for kind in ("leads", "research"):
        for f in sorted(glob.glob(os.path.join(ROOT, "data", kind, f"*{slug}*"))):
            rel = os.path.relpath(f, ROOT)
            try:
                d = json.load(open(f))
            except Exception:
                print(f"\nEARLIER PASS NOTES: {rel} (not json; read it before searching)")
                continue
            print(f"\nEARLIER PASS ALREADY WORKED HERE: {rel}")
            if isinstance(d, dict):
                for lead in (d.get("leads") or []):
                    nm = lead.get("name", "?")
                    why = lead.get("why") or lead.get("status") or ""
                    print(f"  lead:    {nm}: {why[:110]}")
                for b in (d.get("blocked") or []):
                    nm = b.get("name", "?")
                    why = b.get("why") or b.get("reason") or ""
                    print(f"  BLOCKED: {nm}: {why[:110]} (never ship; do not re-research)")


def brief(arg, live):
    match, coord = resolve(arg, live)
    slug = match["slug"] if match else fold(arg)
    print(f"=== VERIFICATION BRIEF: {arg} ===")
    print("(generated by scripts/passcheck.py --brief; the facts below come from the")
    print(" project's own data and outrank any queue entry or memory of this place)\n")

    if match:
        centre = (match["lat"], match["lng"])
        nid = f"{match['ids'][-1][:4]}{int(match['ids'][-1][4:]) + 1:03d}"
        print(f"STATUS: ALREADY PUBLISHED as {match['city']} (/{match['slug']}): this is a DEEPEN pass.")
        print(f"  {match['n']} trees live, {match['photos']} with a photo, "
              f"{match['approx']} approximate pins, walk spans {match['spread']:.1f} km")
        print(f"  New entries start at id {nid}. Never edit the city file; deliver to")
        print(f"  data/research/{match['slug']}-verified.json (JSON array, one object per tree).")
    else:
        centre = coord or centre_from_any_name(arg)
        taken = sorted({i[:3] for c in live for i in c["ids"]})
        print("STATUS: NOT published, this would be a NEW city. Floor: 4 verified trees or no page.")
        print(f"  Pick a 3-letter id prefix NOT in: {' '.join(taken)}")
        print(f"  Deliver to data/research/{slug}-verified.json (JSON array, one object per tree).")

    print("\nTHE JOB, and only the job: VERIFY, do not write prose and do not hunt photos.")
    print("  Per candidate: (1) alive now, (2) species + age with two independent sources")
    print("  (one official register counts as one), (3) the exact spot, precision stated")
    print("  honestly. Rules, schema and register pitfalls: read BRIEF_RESEARCH.md at the")
    print("  repo root. Do NOT read CLAUDE.md; everything a verification pass needs is in")
    print("  that one file. APPEND each verified tree to the delivery file AS FOUND,")
    print("  never only at the end.")

    if centre:
        cands = candidates_near(*centre)
        pub_pts = match["points"] if match else []
        for e in cands:
            e["_pub"] = any(km((e["lat"], e["lng"]), p) <= NEAR_PUBLISHED_KM
                            for p in pub_pts)
            e["_judged"] = (None if e["_pub"]
                            else already_judged(e["lat"], e["lng"], e.get("species")))
        unmined = [e for e in cands if not e["_pub"] and not e["_judged"]]
        shown = unmined[:40] + [e for e in cands if e["_pub"] or e["_judged"]][:12]
        shown = sorted(shown, key=lambda e: e["dist"])
        print(f"\nCANDIDATES from official registers, licence already verified "
              f"({len(cands)} within {SAME_CITY_KM:.0f} km of {centre[0]:.4f},{centre[1]:.4f}):")
        print(f"  UNMINED, i.e. not published and not already judged by an earlier pass: "
              f"{len(unmined)} of {len(cands)}.")
        if cands and not unmined:
            print("  Every register tree within reach is already published or already")
            print("  recorded as a lead or blocked. There is no register work left here:")
            print("  new trees would have to come from web research, and a pass that")
            print("  hunts this register again will spend its window confirming that.")
        if not cands:
            print("  none: no imported register covers this area. Verification here is")
            print("  web research; scout the register first if one exists (OPEN_DATA_SURVEY.md).")
        for e in shown:
            already = e["_pub"]
            bits = [f"{e['dist']:4.1f} km", e["name"] or "(unnamed)"]
            if e["species"]:
                bits.append(e["species"])
            if e["girth_m"]:
                bits.append(f"girth {e['girth_m']:.1f} m")
            if e["age"]:
                bits.append(f"age {e['age']}")
            bits.append(f"({e['lat']:.5f},{e['lng']:.5f})")
            bits.append(e["file"])
            line = "  " + "  ".join(str(b) for b in bits)
            if already:
                line += "  << within 80 m of a live tree: probably already published, check first"
            elif e["_judged"]:
                j = e["_judged"]
                tag = "BLOCKED" if j["kind"] == "blocked" else "already a lead"
                line += (f"\n        << {tag} by an earlier pass ({j['file']}): "
                         f"{j['why'][:150]}")
            print(line)
        if len(cands) > len(shown):
            print(f"  ...and {len(cands) - len(shown)} more; run passcheck again with a "
                  f"tighter coordinate if the cluster needs them.")
        print("  A register says protected, not worth the walk: judge each. Prefer trees")
        print("  that join a walkable cluster over better trees that stand alone.")
    else:
        print("\nCANDIDATES: no coordinates known for this place (not in any imported")
        print("  register). Give passcheck a coordinate, or accept that this pass is web")
        print("  research from zero and budget accordingly.")

    print_leads(slug)
    print_wikidata(slug)
    print_archived_notes(slug, match["city"] if match else arg)
    print_blocklist()

    print("\nDISPATCH: paste this whole brief into the 'verify' subagent (.claude/agents/")
    print("verify.md). That agent definition pins the model to Sonnet, so the tiering is")
    print("mechanical: dispatching any other way is what needs a reason. Stories come")
    print("later from the 'write-stories' agent (Opus), 15 to 20 verified trees at once.")
    print("\nSTOP CONDITION: report what you have after roughly 40 minutes; do not run to")
    print("completeness. A pass never holds a whole city back on its own judgement: it")
    print("delivers what verifies and records the rest as leads with reasons.")
    print("\nWITH YOUR REPORT, return this line for data/agent-costs.json, filled in:")
    print(f'  {{"target": "{arg}", "kind": "verify", "tokens": <total>, "trees": 0, "note": "<one line>"}}')
    return 0


def main():
    args = sys.argv[1:]
    if "--pending" in args:
        print_pending()
        return 0
    want_brief = "--brief" in args
    args = [a for a in args if a != "--brief"]
    if "--claim" in args:
        args.remove("--claim")
        kind = "verify"
        if "--kind" in args:
            i = args.index("--kind")
            kind = args[i + 1]
            del args[i:i + 2]
        by = os.environ.get("GITHUB_RUN_ID") and "night-run" or "session"
        if "--by" in args:
            i = args.index("--by")
            by = args[i + 1]
            del args[i:i + 2]
        if not args:
            print("usage: passcheck.py --claim <place> [--kind verify|write|photo] [--by who]")
            return 1
        return do_claim(" ".join(args), kind, by)
    if "--release" in args:
        args.remove("--release")
        if not args:
            print("usage: passcheck.py --release <place>")
            return 1
        return do_release(" ".join(args))
    if not args:
        print(__doc__)
        return 1
    live = cities()
    arg = " ".join(args)
    _, inflight = load_inflight()
    if want_brief:
        # --as <who> lets the claim HOLDER print the brief for its own pass;
        # anyone else stays refused. Found five minutes after the lock shipped,
        # when it refused its own author the Rome brief he had just claimed.
        as_who = None
        if "--as" in args:
            i = args.index("--as")
            as_who = args[i + 1]
            del args[i:i + 2]
            arg = " ".join(args)
        mine = claims_for(arg, inflight)
        if mine and mine[0].get("by") != as_who:
            c = mine[0]
            print(f"\nREFUSED: no brief for {arg}. It is claimed by "
                  f"{c.get('by', '?')} ({c['kind']}, {c['age_hours']}h ago).")
            print("A brief for a claimed place is how two passes end up doing the")
            print("same work. If this claim is YOURS, rerun with --as "
                  f"{c.get('by', '<who>')}. Otherwise pick another target, or")
            print("--release it if you know that pass is dead.")
            return 1
        return brief(arg, live)

    match, coord = resolve(arg, live)
    print(f"\n=== passcheck: {arg} ===\n")
    if match:
        print(f"  ALREADY PUBLISHED as {match['city']} (/{match['slug']})")
        print(f"  {match['n']} trees, {match['photos']} with a photo, "
              f"{match['approx']} approximate pins, walk spans {match['spread']:.1f} km")
        print(f"  ids {match['ids'][0]} to {match['ids'][-1]}; "
              f"a deepening pass starts at {match['ids'][-1][:4]}{int(match['ids'][-1][4:]) + 1:03d}")
        print(f"  register trees within {SAME_CITY_KM:.0f} km: "
              f"{len(candidates_near(match['lat'], match['lng']))}")
        print("\n  => brief this as DEEPEN. Run with --brief for the paste-ready brief.")
    else:
        print("  NOT published. This would be a new city.")
        if coord:
            print(f"  register trees within {SAME_CITY_KM:.0f} km: {len(candidates_near(*coord))}")
        taken = sorted({i[:3] for c in live for i in c["ids"]})
        print(f"\n  id prefixes already in use ({len(taken)}): {' '.join(taken)}")
        print("  pick three letters that are NOT in that list.")
        print("\n  => run with --brief for the paste-ready brief.")

    print_inflight(arg, inflight)
    print_blocklist()
    slug = match["slug"] if match else fold(arg)
    for kind in ("leads", "research"):
        for f in sorted(glob.glob(os.path.join(ROOT, "data", kind, f"*{slug}*"))):
            try:
                d = json.load(open(f))
                counts = {k: len(v) for k, v in d.items() if isinstance(v, list)} if isinstance(d, dict) else {"items": len(d)}
            except Exception:
                counts = "not json"
            print(f"\n  {kind}: {os.path.relpath(f, ROOT)}  {counts}")
            print("     read it before researching: it says what was already rejected and why")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
