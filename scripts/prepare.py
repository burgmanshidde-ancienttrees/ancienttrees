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
    # Count TREES that still need a story, not FILES that exist. A verified
    # file survives its own merge: nothing deletes it once the stories are
    # written, so the shelf kept reporting work that had already shipped. On
    # 2026-08-17 it announced "8 files awaiting a writer" when all eight were
    # fully published and the true number was zero, which is the first thing a
    # night run reads at the top of its window. Same disease as the leads file
    # offering held trees back as READY: a queue that cannot see completion.
    waiting, stale = [], []
    for p in verified:
        slug = os.path.basename(p).split("-verified")[0]
        try:
            doc = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        rows = doc if isinstance(doc, list) else (doc.get("trees") or [])
        live = set()
        city = os.path.join(ROOT, "data", "cities", f"{slug}.json")
        if os.path.exists(city):
            try:
                live = {t.get("id") for t in json.load(open(city, encoding="utf-8")).get("trees", [])}
            except Exception:
                pass
        todo = [t for t in rows if t.get("id") not in live]
        (waiting if todo else stale).append((slug, len(todo)))
    print("  awaiting a writer : %d tree(s)  %s" % (
        sum(n for _, n in waiting),
        " ".join(f"{s}({n})" for s, n in waiting) or "(empty)"))
    if stale:
        print("  fully published, safe to delete : %s"
              % " ".join(s for s, _ in stale))
    print("  (passcheck.py --pending tells you which verified trees still lack stories)")

    # The stage BEFORE a writer, and the one that ran dry without anyone
    # noticing. leads.py --ready is the cheapest supply in the project (rule
    # 1(a): the verify work is already paid for, only the prose is left) and it
    # fell from ~300 leads on 2026-08-12 to 54 on 08-28, while 1,321 leads sat
    # blocked on nothing but a missing species. refill.py recovers the genus
    # from the tree's own name, costs no tokens and no network, and is
    # idempotent, so there is no decision to make about whether to run it: it
    # runs here, every run, before any work is chosen.
    try:
        import refill
        filled, _, _, files = refill.refill(write=True)
        if filled:
            print(f"  refilled          : {filled} lead(s) given a genus from their own "
                  f"name, across {files} file(s); commit these")
    except Exception as exc:  # never let preparation cost a window
        print(f"  refilled          : skipped ({exc.__class__.__name__})")

    try:
        import leads as _leads
        b = _leads.buckets()
        ready = len(b["ready"])
        print(f"  ready to write    : {ready} lead(s)  (leads.py --ready lists them)")
        if ready < READY_FLOOR:
            # Which gap actually dominates decides which fix is cheap. Before
            # 2026-08-30 readiness() never checked sourcing, so this pile was
            # always "missing species" and genus-names.json was always the
            # right advice. Now that a lead needs real evidence to count as
            # READY (see leads.has_source_evidence), the dominant gap is
            # usually "no source", which genus-names.json cannot fix at all:
            # that needs an actual verify pass, not a word list.
            miss_counts = {}
            for _, _, miss in b["needs"]:
                for m in miss:
                    miss_counts[m] = miss_counts.get(m, 0) + 1
            top = max(miss_counts, key=miss_counts.get) if miss_counts else None
            if top and top.startswith("species"):
                print(f"  *** the writable pile is under {READY_FLOOR}. Widening "
                      f"data/genus-names.json is the cheap way to refill it: every word "
                      f"added there turns leads into writable trees for nothing. ***")
            elif top and top.startswith("source"):
                # A directive, not advice. Until 2026-09-01 this printed the
                # diagnosis and stopped, and a run was free to read it and go
                # do something else, which is what happened: the pile went
                # from 366 on 08-28 to 16 on 09-01 while every run walked
                # past this line. Hidde named the gap in one sentence ("de
                # schrijfplank moet ook autonoom gevuld worden als die leeg
                # raakt"), and an empty shelf is the one state that makes the
                # cheapest rung on the ladder unavailable, so it outranks
                # whatever else the run had in mind.
                print(f"  *** REFILL THE SHELF FIRST: the writable pile is under "
                      f"{READY_FLOOR} and {miss_counts[top]} leads are unsourced, a scrape "
                      f"never looked at by a pass. No script fills that. Dispatch a verify "
                      f"agent on the batch below BEFORE taking anything else off the "
                      f"ladder. ***")
                for line in refill_batches(b):
                    print(line)
    except Exception as exc:
        print(f"  ready to write    : unknown ({exc.__class__.__name__})")



def refill_batches(b, want=3):
    """Name the verify batches that would refill the writable shelf.

    Exists so the directive above points at work rather than at a problem. A
    run should not have to derive which file to verify: that derivation is
    the same every time and a run on a short window skips it.

    The order is size first, because CLAUDE.md's assembly line refuses a pass
    under six expected candidates and the fixed cost per pass is what makes a
    thin batch expensive. The `_famous-*` files are deliberately eligible and
    usually win: they are country batches, which is the shape CLAUDE.md asks
    for, and famous_trees.py records that nearly all of their entries arrive
    with a photograph already attached, so a verified one lands on a page
    complete rather than with a gap.
    """
    import collections
    per = collections.Counter()
    photos = collections.Counter()
    for item in b["needs"]:
        city, lead, miss = item[0], item[1], item[2]
        if not any(m.startswith("source") for m in miss):
            continue
        per[city] += 1
        if isinstance(lead, dict) and lead.get("photos"):
            photos[city] += 1
    if not per:
        return []
    out = ["      the batches that would refill it, biggest first:"]
    for city, n in per.most_common(want):
        kind = "country batch" if city.startswith("_famous-") else "city"
        out.append("        %-26s %3d unsourced, %3d with a photo already  (%s)"
                   % (city, n, photos[city], kind))
    out.append("      brief it from data/leads/<name>.json; verify agent, per "
               "BRIEF_RESEARCH.md.")
    return out


# Under this many writable leads and refilling the pile outranks writing from
# it, because three passes from now there is nothing to write at all.
READY_FLOOR = 60


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
