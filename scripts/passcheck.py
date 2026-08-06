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
from cluster_register import km  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAME_CITY_KM = 20.0
NEAR_PUBLISHED_KM = 0.08  # a register entry this close to a live tree is probably that tree

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
    for h, v in sorted(hosts.items(), key=lambda kv: 0 if "hang" in kv[1]["behaviour"] else 1):
        mark = "!!" if "hang" in v["behaviour"] else "  "
        print(f" {mark} {h}: {v['behaviour']}. {v['workaround']}")
    print("    Every fetch: curl -m 20 (or timeout= on urllib). A hang burns the "
          "window; a refusal costs a second.")


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
        shown = cands[:40]
        print(f"\nCANDIDATES from official registers, licence already verified "
              f"({len(cands)} within {SAME_CITY_KM:.0f} km of {centre[0]:.4f},{centre[1]:.4f}):")
        if not cands:
            print("  none: no imported register covers this area. Verification here is")
            print("  web research; scout the register first if one exists (OPEN_DATA_SURVEY.md).")
        for e in shown:
            already = any(km((e["lat"], e["lng"]), p) <= NEAR_PUBLISHED_KM for p in pub_pts)
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
        mine = claims_for(arg, inflight)
        if mine:
            c = mine[0]
            print(f"\nREFUSED: no brief for {arg}. It is claimed by "
                  f"{c.get('by', '?')} ({c['kind']}, {c['age_hours']}h ago).")
            print("A brief for a claimed place is how two passes end up doing the")
            print("same work. Pick another target, or --release it if that pass is dead.")
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
