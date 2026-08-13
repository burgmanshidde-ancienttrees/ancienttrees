#!/usr/bin/env python3
"""Keep the staging shelf stocked, so no run ever starts from zero.

Hidde, 2026-08-13, on why night runs produce a fraction of a session: "moet je
niet een van de runs laten voorbereiden - of dat een lijst met voorbereiding
altijd wordt bijgewerkt die uitwerk runs dan weer kunnen pakken."

He is right, and the insight underneath is that PREPARATION IS RETRIEVAL, NOT
JUDGEMENT. Everything a session did by hand today before dispatching a verify
pass (find the register rows within 5 km of the city, drop the ones the register
itself marks unpublishable, flag anything standing near a tree we already
publish) is arithmetic. The measured week-one rule applies: retrieval is code
and costs nothing; judgement needs an agent. So the shelf is stocked by this
script rather than by anyone's window, and a run's whole hour goes to the only
parts that need a mind: is it alive, can you reach it, is it worth the walk,
and the writing.

    python3 scripts/prepare.py            # stock the shelf, print the pipeline
    python3 scripts/prepare.py --status   # print the pipeline only

What it does per invocation:
  1. Walks the queue in sprint order (below target, not claimed, no staging
     file yet) and writes data/research/<slug>-register-candidates.json for the
     next few cities that have register supply. Rows the register marks
     `publishable: false` are excluded; rows within 80 m of a published tree
     are KEPT and annotated with `near_published`, never dropped, because two
     remarkable trees can stand close together (the rule of 2026-08-13, learned
     after a distance filter silently discarded eleven different conifer
     species standing near Hobart's Douglas fir).
  2. Prints the pipeline: STAGED (candidates awaiting a verify pass), VERIFIED
     (trees awaiting a write pass, from passcheck's own view), and what the
     queue says comes next.

A run reads one command and knows the state of the line. A session dispatches
against the same files. Nobody prepares by hand any more.
"""
import argparse
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from geo import km              # noqa: E402
import city_queue as Q          # noqa: E402

STAGE_LIMIT = 5        # cities stocked per invocation: fresh beats plentiful
MIN_CANDIDATES = 3     # below this a staging file is not worth a pass


def register_rows():
    rows = []
    for path in glob.glob(os.path.join(ROOT, "data", "registers", "*.json")):
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        for r in (d if isinstance(d, list) else (d.get("trees") or d.get("entries") or [])):
            if not isinstance(r, dict) or r.get("publishable") is False:
                continue
            la = r.get("latitude", r.get("lat"))
            lo = r.get("longitude", r.get("lng"))
            try:
                if la is not None and lo is not None:
                    rows.append((float(la), float(lo), os.path.basename(path)[:-5], r))
            except (TypeError, ValueError):
                continue
    return rows


def live_trees(slug):
    path = os.path.join(ROOT, "data", "cities", f"{slug}.json")
    try:
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
    except OSError:
        return []
    return [(t["location"]["latitude"], t["location"]["longitude"], t["id"],
             t.get("name", ""), t.get("species", ""))
            for t in d.get("trees") or []
            if (t.get("location") or {}).get("latitude") is not None]


def live_count(slug):
    path = os.path.join(ROOT, "data", "cities", f"{slug}.json")
    try:
        with open(path, encoding="utf-8") as fh:
            return len(json.load(fh).get("trees") or [])
    except OSError:
        return 0


def already_worked(slug):
    """A leads file with judged entries means a pass already went through this
    city's register and what remains is leads, not fresh candidates. Staging it
    again sends the next run to re-verify rejects, which is the grinding the
    80/20 rule forbids. The first test run of this script did exactly that: it
    staged Palermo, Bordeaux, Strasbourg and Toulouse hours after passes had
    worked all four to their honest ceilings. leads.py surfaces what is left
    there; this script only stocks untouched ground."""
    path = os.path.join(ROOT, "data", "leads", f"{slug}.json")
    try:
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        return bool((d.get("leads") or []) or (d.get("blocked") or []))
    except OSError:
        return False


def claimed():
    try:
        with open(os.path.join(ROOT, "data", "in-flight.json"), encoding="utf-8") as fh:
            return {c["target"].lower() for c in json.load(fh)["claims"]}
    except (OSError, ValueError, KeyError):
        return set()


def stage(rows, city):
    slug = city["slug"]
    pos = Q.city_coords(city["city"], city.get("article"))
    if not pos:
        return None
    out = []
    live = live_trees(slug)
    for la, lo, reg, r in rows:
        d_km = km((la, lo), pos)
        if d_km > 5:
            continue
        e = {k: v for k, v in r.items() if k != "geometry"}
        e["register"] = reg
        e["km_from_centre"] = round(d_km, 2)
        for tla, tlo, tid, tname, tsp in live:
            d_m = km((la, lo), (tla, tlo)) * 1000
            if d_m < 80:
                e["near_published"] = {"metres": round(d_m, 1), "id": tid,
                                       "name": tname, "species": tsp}
                break
        out.append(e)
    if len(out) < MIN_CANDIDATES:
        return None
    out.sort(key=lambda e: e.get("km_from_centre", 9))
    path = os.path.join(ROOT, "data", "research", f"{slug}-register-candidates.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    return len(out)


def pipeline_status():
    staged = sorted(glob.glob(os.path.join(ROOT, "data", "research", "*-register-candidates.json")))
    verified = sorted(glob.glob(os.path.join(ROOT, "data", "research", "*-verified.json")))
    print("\nTHE LINE, stage by stage:")
    print("  staged for verify : %d file(s)  %s" % (
        len(staged), " ".join(os.path.basename(p).split("-register")[0] for p in staged) or "(empty)"))
    print("  awaiting a writer : %d file(s)  %s" % (
        len(verified), " ".join(os.path.basename(p).split("-verified")[0] for p in verified) or "(empty)"))
    print("  (passcheck.py --pending tells you which verified trees still lack stories)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()
    if a.status:
        pipeline_status()
        return 0

    with open(os.path.join(ROOT, "data", "city-queue.json"), encoding="utf-8") as fh:
        queue = json.load(fh)["cities"]
    busy = claimed()
    rows = register_rows()
    done = 0
    for c in queue:
        if done >= STAGE_LIMIT:
            break
        if not c.get("rank") or c["rank"] > 250:
            continue
        # Live count from data/cities, never the queue's copy: the queue is
        # regenerated periodically and its tree counts lag the same afternoon
        # that changes them. And the sprint only: cities at 10 or more wait,
        # because nothing deepens while the sprint runs (Hidde, 2026-08-13).
        if live_count(c["slug"]) >= 10:
            continue
        if already_worked(c["slug"]):
            continue
        if c["city"].lower() in busy or c["slug"] in busy:
            continue
        path = os.path.join(ROOT, "data", "research", f"{c['slug']}-register-candidates.json")
        if os.path.exists(path):
            continue
        if os.path.exists(os.path.join(ROOT, "data", "research", f"{c['slug']}-verified.json")):
            continue
        n = stage(rows, c)
        if n:
            print("  staged %-18s rank %3d  %3d candidates" % (c["slug"], c["rank"], n))
            done += 1
    if not done:
        print("  shelf already stocked, nothing new to stage")
    pipeline_status()
    return 0


if __name__ == "__main__":
    sys.exit(main())
