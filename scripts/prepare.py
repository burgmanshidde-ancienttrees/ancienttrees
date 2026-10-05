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
import datetime
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from geo import km              # noqa: E402
import city_queue as Q          # noqa: E402

STAGED_FIRST = []      # set by pipeline_status, read by refill_batches
STAGE_LIMIT = 5       # cities stocked per invocation: fresh beats plentiful
MIN_CANDIDATES = 3     # below this a staging file is not worth a pass


def tree_level(la, lo):
    """Is this a coordinate for one trunk, or a grid square?

    Three decimals or fewer on both axes is ~110 m or coarser, which can never
    become a confirmed pin. Measured 2026-10-03 across all 57 registers: exactly
    one is like that, Hawaii's (all 338 rows), and two night passes of ~150k
    tokens each went into it on 10-02 for zero trees, because nothing upstream
    said its pins could not be confirmed.
    """
    def dp(v):
        s = repr(float(v))
        return len(s.split(".")[1].rstrip("0")) if "." in s else 0
    return dp(la) > 3 or dp(lo) > 3


def claimable():
    """(proven slugs, focus countries, supply-focus countries), from the same
    files passcheck --claim reads, so the shelf never stages work the claim
    will refuse. On 2026-10-03 it held 49 staged cities and 46 of them could
    not be claimed for a verify pass at all."""
    try:
        from passcheck import FOCUS_COUNTRIES, SUPPLY_FOCUS
    except Exception:
        FOCUS_COUNTRIES, SUPPLY_FOCUS = set(), []
    try:
        with open(os.path.join(ROOT, "data", "depth-roster-frozen.json"), encoding="utf-8") as fh:
            proven = set((json.load(fh).get("cities") or {}).keys())
    except (OSError, ValueError):
        proven = set()
    return proven, set(FOCUS_COUNTRIES), list(SUPPLY_FOCUS)


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
                if la is not None and lo is not None and tree_level(la, lo):
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
    try:
        from passcheck import already_judged
    except Exception:
        already_judged = None
    for la, lo, reg, r in rows:
        d_km = km((la, lo), pos)
        if d_km > 5:
            continue
        # A row an earlier pass already put in leads or blocked is not a
        # candidate. This used to be done by skipping any city with a leads
        # file at all, which also skipped every city worth deepening: Berlin,
        # the one register that shipped trees on 10-03, was never staged.
        sp = r.get("species") or r.get("species_latin") or r.get("species_name")
        if already_judged and already_judged(la, lo, sp):
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
    # Rung 1 before any of the stages below it, because a photograph somebody
    # walked to a tree to take outranks anything the machine found by itself.
    # Printed here rather than left to memory: the queue is written by a
    # workflow step the run never sees, so without this line the only way to
    # learn it is not empty is to think of asking.
    try:
        waiting_photos = json.load(open(os.path.join(ROOT, "data", "sighting-queue.json"),
                                        encoding="utf-8")).get("queue", [])
    except Exception:
        waiting_photos = []
    if waiting_photos:
        print("  *** %d reader photograph(s) waiting for your eyes (RUNG 1). LOOK at the "
              "files in out/sightings/, then apply with scripts/sightings_publish.py."
              % len(waiting_photos))
        for e in waiting_photos[:10]:
            print("      %s%s  %s  match=%s  the tree has: %s"
                  % ("[ours] " if e.get("mine") else "",
                     e.get("tree_id"), (e.get("tree_name") or "")[:38],
                     e.get("match"), e.get("current_photo")))

    # AND THE HALF THAT WAS INVISIBLE (2026-09-08). The queue above only ever
    # holds photographs of trees we ALREADY map. A photograph of a tree we do
    # not map went to data/leads/_sightings.json and was marked done in the
    # same breath, and nothing read that file, so `--status` said "0 waiting"
    # while five of Hidde's own photographs sat in it untouched. His words:
    # "Hoe kan het dat die niet zijn bekeken? Dat moet dicht."
    #
    # It is the more interesting half, not the less. A photograph of a tree we
    # have is at best a better picture; this is a tree the map does not know
    # about at all.
    try:
        sys.path.insert(0, os.path.join(ROOT, "scripts"))
        from sightings_inbox import open_leads
        unmapped = open_leads()
    except Exception:
        unmapped = []
    if unmapped:
        print("  *** %d reader photograph(s) of a tree we do NOT map, still without a "
              "verdict (RUNG 1). Check each against the bar, then write one sentence "
              "into its `why` in data/leads/_sightings.json." % len(unmapped))
        for l in unmapped[:10]:
            where = ("%.4f %.4f" % (l["latitude"], l["longitude"])
                     if l.get("latitude") is not None else "no coordinate")
            print("      %s  %-30s %s%s"
                  % (str(l.get("sighting_id"))[:8], (l.get("name") or "unnamed")[:30],
                     where,
                     ("  note: " + l["note"].strip()[:36]) if (l.get("note") or "").strip() else ""))
        print("      python3 scripts/corroborate.py <lat> <lng> --country <country>"
              "   asks the registers AND Wikipedia")
    # Split by whether a verify claim would be accepted. Older staging files
    # for cities outside the proven roster or the focus countries stay on disk
    # (nothing is thrown away) but are named apart, so a run does not pick one
    # and spend its window being refused.
    proven, focus, supply = claimable()
    try:
        with open(os.path.join(ROOT, "data", "city-queue.json"), encoding="utf-8") as fh:
            qc = {c["slug"]: c.get("country") for c in json.load(fh)["cities"]}
    except (OSError, ValueError, KeyError):
        qc = {}
    names = [os.path.basename(p).split("-register")[0] for p in staged]

    def has_tree_level(slug):
        p = os.path.join(ROOT, "data", "research", f"{slug}-register-candidates.json")
        try:
            rows = json.load(open(p, encoding="utf-8"))
        except (OSError, ValueError):
            return False
        for r in rows if isinstance(rows, list) else []:
            try:
                if tree_level(r.get("latitude", r.get("lat")), r.get("longitude", r.get("lng"))):
                    return True
            except (TypeError, ValueError):
                continue
        return False

    ok = [s for s in names if (not proven or s in proven) and (not focus or qc.get(s) in focus)
          and has_tree_level(s)]
    global STAGED_FIRST
    # A city a verify pass just came back empty from is a wall, not work
    # (passcheck.py WALLS, 2026-10-05): naming it again is how Munich got
    # claimed six times in three days.
    try:
        from passcheck import recent_walls
        walls = recent_walls()
    except Exception:
        walls = {}
    STAGED_FIRST = [s for s in ok if qc.get(s) in supply and s not in walls]
    if walls:
        print("  walls (verified empty in the last 48h, do not re-verify): %s" % " ".join(sorted(walls)))
    ok.sort(key=lambda s: (qc.get(s) not in supply, s))
    parked = [s for s in names if s not in ok]
    print("  staged for verify : %d claimable  %s" % (
        len(ok), " ".join("%s%s" % (s, "*" if qc.get(s) in supply else "") for s in ok) or "(empty)"))
    if ok:
        print("      (* = where the visitors are: the US, the UK, Germany. Take those first.)")
    if parked:
        print("  parked            : %d staged file(s) a verify claim would refuse, or "
              "whose coordinates cannot become a confirmed pin" % len(parked))
    # Count TREES that still need a story, not FILES that exist. A verified
    # file survives its own merge: nothing deletes it once the stories are
    # written, so the shelf kept reporting work that had already shipped. On
    # 2026-08-17 it announced "8 files awaiting a writer" when all eight were
    # fully published and the true number was zero, which is the first thing a
    # night run reads at the top of its window. Same disease as the leads file
    # offering held trees back as READY: a queue that cannot see completion.
    try:
        from leads import has_photo_or_pin as _photo_or_pin
    except Exception:
        _photo_or_pin = lambda t: True
    _proven = claimable()[0]
    waiting, stale, held = [], [], []
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
        # A file that is not a proven city cannot be claimed for writing, so
        # all of it waits, whatever its trees carry.
        blocked_here = (todo if (_proven and slug not in _proven)
                        else [t for t in todo if not _photo_or_pin(t)])
        if blocked_here:
            held.append((slug, len(blocked_here)))
    held_n = dict(held)
    print("  awaiting a writer : %d tree(s)  %s" % (
        sum(n - held_n.get(s, 0) for s, n in waiting),
        " ".join(f"{s}({n - held_n.get(s, 0)})" for s, n in waiting
                 if n - held_n.get(s, 0) > 0) or "(empty)"))
    if held:
        # Written or verified, and refused by preflight until a photograph or a
        # confirmed pin exists. On 10-02 runs merged and reverted these seven
        # times; they are depth work (photo_fetch / a pin check), not writing.
        print("  held               : %d tree(s)  %s  (no photo or confirmed pin, "
              "or not a proven city; a photo or pin pass frees the first kind. "
              "Do NOT merge them as they are)"
              % (sum(held_n.values()), " ".join(f"{s}({n})" for s, n in held)))
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

    data_age()
    fame_gap()

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
            # Count the leads that are ONE field away, not every mention of a
            # field. The raw count answers the wrong question, because a lead
            # missing name, position, species and source is a scrape rather
            # than a lead and closing any one of its gaps buys nothing. On
            # 2026-09-11 the raw count made "position" the dominant gap (527
            # of it) while only 96 leads were actually one coordinate away,
            # and 119 were one verify pass away.
            #
            # That mattered more than a wrong label. Neither branch below
            # fires on "position", so the whole directive fell through and a
            # run under the floor was told NOTHING: the shelf sat at 3 against
            # a floor of 60 with the alarm silently doing nothing. An alarm
            # with a hole in it is worse than no alarm, because the silence
            # reads as "fine". Hence the else below: every gap now says
            # something, whatever the dominant one turns out to be.
            single = {}
            for _, _, miss in b["needs"]:
                for m in miss:
                    miss_counts[m] = miss_counts.get(m, 0) + 1
                if len(miss) == 1:
                    single[miss[0]] = single.get(miss[0], 0) + 1
            top = max(single, key=single.get) if single else None
            if top:
                print("      one field away: "
                      + ", ".join("%d on %s" % (n, k.split(" (")[0])
                                  for k, n in sorted(single.items(),
                                                     key=lambda kv: -kv[1])))
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
                      f"{READY_FLOOR} and {single[top]} leads need only a source, a scrape "
                      f"never looked at by a pass ({miss_counts[top]} lack one in total, "
                      f"the rest are short of more than one field). No script fills that. "
                      f"Dispatch a verify agent on the batch below BEFORE taking anything "
                      f"else off the ladder. ***")
                for line in refill_batches(b):
                    print(line)
            else:
                # Anything else: still a directive, still pointing at work.
                # A verify pass is what turns a scraped lead into a writable
                # one whatever field it happens to be short of, so the batches
                # are worth printing here too.
                print(f"  *** REFILL THE SHELF FIRST: the writable pile is under "
                      f"{READY_FLOOR}. The nearest work is the {single[top]} lead(s) "
                      f"one '{top.split(' (')[0]}' away. No script closes that gap; "
                      f"dispatch a verify agent before taking anything else off the "
                      f"ladder. ***")
                for line in refill_batches(b):
                    print(line)
    except Exception as exc:
        print(f"  ready to write    : unknown ({exc.__class__.__name__})")




def fame_gap():
    """Famous-tree fame numbers that only a run with network can fetch.

    /collections/famous-trees ranks on how many language Wikipedias wrote a
    tree up, and the numbers come from data/famous-demand.json. Filling that
    cache needs Wikidata and the pageviews API, which a sandboxed session
    often cannot reach, so the work lands on whoever CAN: a night run, where
    those hosts answer. It is a script rather than an agent task, so it costs
    tokens for nothing but the two lines it takes to run.

    Printed rather than remembered because the page is already live and grows
    by itself: every lead resolved is another tree that appears on it, and
    General Sherman is in the unresolved pile.
    """
    path = os.path.join(ROOT, "data", "famous-demand.json")
    if not os.path.exists(path):
        return
    try:
        cache = json.load(open(path, encoding="utf-8"))
    except Exception as exc:                          # noqa: BLE001
        print(f"  fame data         : unreadable ({exc.__class__.__name__})")
        return
    unresolved = sum(1 for e in cache.values() if not e.get("wikis"))
    if not unresolved:
        print("  fame data         : every cached famous lead is resolved")
        return
    print("  fame data         : %d of %d famous leads carry no fame number. "
          "If this run has network:" % (unresolved, len(cache)))
    print("      python3 scripts/famous_demand.py --resolve && "
          "python3 scripts/famous_demand.py")
    print("      python3 scripts/fame.py --apply    "
          "# puts the newly resolved trees on /collections/famous-trees")


def data_age():
    """How old is the demand data a run is about to make decisions on?

    Hidde, 2026-09-01: "is het probleem niet in onze autonome flow dat als de
    daily digest nachtrun niet werkt dat we dan een dag achterlopen". The
    digest itself turns out to be the reliable part (37 consecutive days in
    DATA.md with no gap), and health.py already flags the WORKFLOW going
    quiet. What nothing did was tell the run how old the FILE is, so a run
    reading a stale depth roster could not know it was stale and would spend
    its window deepening cities that stopped being the answer days ago.

    Two days is the threshold rather than one, because Search Console lags two
    to three days by itself: a single missed digest moves nothing and warning
    about it would train a run to ignore the line.
    """
    path = os.path.join(ROOT, "DATA.md")
    if not os.path.exists(path):
        return
    head = open(path, encoding="utf-8").read(40000)
    m = re.search(r"^## (\d{4}-\d{2}-\d{2})", head, re.M)
    if not m:
        print("  demand data      : DATA.md carries no dated entry")
        return
    age = (datetime.date.today() - datetime.date.fromisoformat(m.group(1))).days
    if age <= 2:
        print("  demand data      : DATA.md newest entry %s (%d day(s) old)"
              % (m.group(1), age))
    else:
        print("  *** DATA.md's newest entry is %s, %d days old. The depth roster and "
              "the queue's ranking are that old too, so rule two ('depth only where "
              "there is demand') is being applied to stale numbers. Check the Data "
              "digest workflow before spending the window on depth: "
              "python3 scripts/health.py ***" % (m.group(1), age))


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
    # A staged register city where the visitors are beats any leads batch:
    # its rows carry tree-level coordinates, so a verify pass can confirm the
    # pins, which is what Berlin and Dresden did on 10-03 for 25 trees.
    if STAGED_FIRST:
        return ["      verify a STAGED city first, where the visitors are: "
                + " ".join(STAGED_FIRST)
                + "\n      brief: python3 scripts/passcheck.py --brief <city>; verify "
                "agent, per BRIEF_RESEARCH.md (one official register is enough)."]
    per = collections.Counter()
    photos = collections.Counter()
    # Only batches a claim would accept and preflight could publish (2026-10-03).
    # The old order put `_tree-of-the-year` (73 leads, none with a photograph)
    # and `_famous-portugal` (refused at claim time: not a proven city) first,
    # and on 10-02 runs took exactly those and shipped nothing. An underscore
    # file is never a proven city, so it is a reader-submission matter now.
    proven, focus, supply = claimable()
    try:
        from leads import has_photo_or_pin
    except Exception:
        has_photo_or_pin = lambda e: True
    countries = {}
    try:
        with open(os.path.join(ROOT, "data", "city-queue.json"), encoding="utf-8") as fh:
            countries = {c["slug"]: c.get("country") for c in json.load(fh)["cities"]}
    except (OSError, ValueError, KeyError):
        pass
    for item in b["needs"]:
        city, lead, miss = item[0], item[1], item[2]
        if city.startswith("_") or (proven and city not in proven):
            continue
        if not any(m.startswith("source") for m in miss):
            continue
        # A lead with no tree-level coordinate and no photograph cannot become
        # either from a verify pass of its sources alone, so it refills nothing.
        coords = None
        if isinstance(lead, dict):
            loc = lead.get("location") if isinstance(lead.get("location"), dict) else lead
            la, lo = loc.get("latitude", loc.get("lat")), loc.get("longitude", loc.get("lng"))
            try:
                coords = tree_level(la, lo) if la is not None and lo is not None else None
            except (TypeError, ValueError):
                coords = None
            if not coords and not has_photo_or_pin(lead):
                continue
        per[city] += 1
        if isinstance(lead, dict) and has_photo_or_pin(lead):
            photos[city] += 1
    if not per:
        return ["      no lead batch can refill it: every remaining lead is outside "
                "the proven cities or has neither a photo nor a tree-level "
                "coordinate. Verify a STAGED city above, or scout "
                "(scout_next.py --target)."]
    ranked = sorted(per, key=lambda c: (countries.get(c) not in supply, -per[c]))
    out = ["      the batches that would refill it, biggest first:"]
    for city in ranked[:want]:
        out.append("        %-26s %3d unsourced, %3d with a photo or pin already  (%s)"
                   % (city, per[city], photos[city], countries.get(city) or "?"))
    out.append("      brief it from data/leads/<name>.json; verify agent, per "
               "BRIEF_RESEARCH.md.")
    return out


# Under this many writable leads and refilling the pile outranks writing from
# it, because three passes from now there is nothing to write at all.
READY_FLOOR = 60


def arm_the_hooks():
    """Point git at scripts/hooks, because a hook nobody enables is no hook.

    Written 2026-09-17, after a push went to main with a red gate on it. The
    pre-push hook has carried eight checks since 27 August and it had never run
    once in this clone: it needs `git config core.hooksPath scripts/hooks`, and
    that is per clone, while every remote session starts from a clone made an
    hour ago. So handoffcheck, paritycheck, crosscheck and pitchcheck were all
    installed, all documented, and all dead on arrival in exactly the sessions
    that most needed them.

    prepare.py runs at the top of every run, which makes it the one place that
    can fix a fresh clone before anything is pushed from it. It never overrides
    a path somebody set deliberately.
    """
    import subprocess
    try:
        cur = subprocess.run(["git", "config", "core.hooksPath"], cwd=ROOT,
                             capture_output=True, text=True, timeout=10).stdout.strip()
        if cur:
            return
        subprocess.run(["git", "config", "core.hooksPath", "scripts/hooks"],
                       cwd=ROOT, capture_output=True, timeout=10)
        print("  armed the pre-push hooks (core.hooksPath was unset in this clone)")
    except Exception:
        pass  # never let a git quirk stop a run from starting


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()
    arm_the_hooks()
    if a.status:
        pipeline_status()
        return 0

    with open(os.path.join(ROOT, "data", "city-queue.json"), encoding="utf-8") as fh:
        queue = json.load(fh)["cities"]
    busy = claimed()
    rows = register_rows()
    proven, focus, supply = claimable()
    # Where the visitors are first (SUPPLY_FOCUS), then the other focus
    # countries, each in queue order. A city outside the proven roster or the
    # focus countries is refused at claim time, so it is not staged at all.
    order = sorted(
        [c for c in queue if c.get("rank")
         and (not proven or c["slug"] in proven)
         and (not focus or c.get("country") in focus)],
        key=lambda c: (c.get("country") not in supply, c["rank"]))
    done = 0
    for c in order:
        if done >= STAGE_LIMIT:
            break
        # Live count from data/cities, never the queue's copy: the queue is
        # regenerated periodically and its tree counts lag the same afternoon
        # that changes them. Below TARGET, not below ten: the sprint-to-ten of
        # 2026-08-13 ended with recovery mode (2026-10-01), which puts new
        # trees into proven cities ahead of new places.
        if live_count(c["slug"]) >= (c.get("target") or 10):
            continue
        if c["city"].lower() in busy or c["slug"] in busy:
            continue
        path = os.path.join(ROOT, "data", "research", f"{c['slug']}-register-candidates.json")
        # A staging file is restocked once it is a day old, because the leads
        # it was built against move every run. A verified file no longer stops
        # staging: Berlin had one (a single held tree) and so was never staged.
        if os.path.exists(path) and (datetime.datetime.now().timestamp()
                                     - os.path.getmtime(path)) < 86400:
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
