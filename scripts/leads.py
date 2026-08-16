#!/usr/bin/env python3
"""What is sitting in data/leads/ that could go live, and what genuinely cannot.

Built 2026-08-10, after Hidde corrected three separate over-strictness calls in
one session (a missing age, a modest girth, being ninth in line) and asked:
"can you improve your system so that we aren't so strict and waste tokens?"

The waste is specific and measurable. A lead is a tree we ALREADY PAID to find,
at roughly 19,000 tokens each. Holding it for a reason that is not a reason
means paying that again the next time somebody researches the same city, and
the leads files were being presented to every brief as a graveyard ("EARLIER
PASS ALREADY WORKED HERE") rather than as stock.

So this reads data/block-reasons.json, which is the CLOSED list of reasons a
tree may not ship, and sorts every lead into three piles. The default is the
whole point: a reason matching nothing in that file is treated as publishable,
not as blocked. Fail open toward shipping.

    python3 scripts/leads.py                  the whole corpus, summarised
    python3 scripts/leads.py --city kyoto     one city, listed
    python3 scripts/leads.py --ready          only leads with enough data to write
"""
import argparse
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES = os.path.join(ROOT, "data", "block-reasons.json")


def rules():
    with open(RULES, encoding="utf-8") as fh:
        return json.load(fh)


def reason_text(entry):
    # Was a fixed list of keys (why_not_published, reason, why, status, note),
    # which missed real block reasons written under other names: Trento's
    # leads file records them under `why_a_lead`, `next_step` and
    # `hold_reason_2026_08_14`, and a 2026-08-14 write pass explicitly found
    # "the cautious reading of hard rule 10 is that this is somebody's home"
    # in one of those fields for the Villa O'Santissima sequoia, invisible to
    # this function because nothing reads that key. Scan the whole entry, the
    # same fix already applied to is_done() below for the same failure shape.
    return json.dumps(entry, ensure_ascii=False)


# A lead that has already shipped is not a lead. Found 2026-08-12 while sizing
# a write pass: Berlin showed 7 READY of which 4 read "[RESOLVED 2026-08-09,
# delivered as ber_018]" in their NAME, with `why` empty, so neither the
# blocking rules (which read `why`) nor the readiness check (which reads name,
# species and position, all present) could see it. A brief built on that number
# would have re-written four live stories, which is the 2026-08-08 error again.
# Seven leads across four cities were affected. The marker is searched across
# the whole entry, because the run that resolved one wrote it wherever it was
# standing: in the name, in a note, in `status`.
DONE = re.compile(r"\bresolved\b|\bdelivered as\b|\balready published\b|"
                  r"\bpromoted\b|\bshipped as\b", re.I)


def is_done(entry):
    return bool(DONE.search(json.dumps(entry, ensure_ascii=False)))


# See classify() below. Matched against every "why" field in data/leads/
# before being written, 2026-08-16: catches the 5 real cases in the corpus
# at the time (Braga's two Tibaes trees, Como's Museo Giovio plane, Guimaraes'
# Moreira de Conegos and Citania de Briteiros pines), zero false positives on
# the two known traps (Barcelona's "Held on count[...]", a forbidden reason
# under CLAUDE.md's never_blocking list; Toulouse's "held in spring,
# announced on...", unrelated prose about open-day scheduling).
HELD_MARKER = re.compile(
    r"\bHELD\b[\w\s-]{0,25}?\bon\b\s+(?:access|evidence|courtyard access|"
    r"the day-trip boundary|transport)\b", re.I)


# Found 2026-08-13 while writing a Munich batch: the DONE marker above only
# catches a lead that SOMEONE remembered to annotate after shipping it. Munich's
# own leads file held four entries for Schlosspark Nymphenburg trees that had
# already been published twice, under two different ids (muc_011-014, then
# muc_015-018 from a second pass that never checked), with no marker either
# time, plus four more that matched already-published trees under different
# names. A coordinate match doesn't need anyone to remember anything: if a
# lead's own position is within ~11m (4 decimal places) of a tree the city file
# already ships, the lead is done whether or not its text says so.
_CITY_COORD_CACHE = {}


def _city_coords(city_slug):
    if city_slug in _CITY_COORD_CACHE:
        return _CITY_COORD_CACHE[city_slug]
    path = os.path.join(ROOT, "data", "cities", f"{city_slug}.json")
    coords = {}
    try:
        d = json.load(open(path, encoding="utf-8"))
        for t in d.get("trees", []):
            loc = t.get("location", {})
            lat, lng = loc.get("latitude"), loc.get("longitude")
            if lat is not None and lng is not None:
                coords[(round(lat, 4), round(lng, 4))] = t["id"]
    except Exception:
        pass
    _CITY_COORD_CACHE[city_slug] = coords
    return coords


_CITY_SPECIES_CACHE = {}


def _city_species(city_slug):
    if city_slug in _CITY_SPECIES_CACHE:
        return _CITY_SPECIES_CACHE[city_slug]
    path = os.path.join(ROOT, "data", "cities", f"{city_slug}.json")
    out = {}
    try:
        d = json.load(open(path, encoding="utf-8"))
        for t in d.get("trees", []):
            out[t["id"]] = t.get("species") or ""
    except Exception:
        pass
    _CITY_SPECIES_CACHE[city_slug] = out
    return out


def _genus(species):
    """The Latin genus out of either shape we store: "Common Name (Genus sp)"
    or a bare "Genus sp"."""
    if not species:
        return ""
    m = re.search(r"\(([A-Z][a-z]+)\s", species) or re.match(r"\s*([A-Z][a-z]+)\s", species)
    return m.group(1).lower() if m else ""


def published_match(city_slug, entry):
    """The id of an already-published tree at this lead's own coordinates, or None.

    **A shared coordinate is not proof of a shared tree, and the genus decides.**
    Added 2026-08-13 after Hidde pointed out the obvious thing a distance test
    cannot see: "interessante bomen kunnen natuurlijk wel dichtbij elkaar
    staan." Two remarkable trees stand metres apart all over this site, and a
    register frequently gives a group of them one coordinate. Measured across
    the whole leads corpus, 76 leads matched a published tree by position and
    three of them were a different genus entirely: an Araucaria of 1920 filed as
    done because a horse chestnut shares its point in Barcelona, and an incense
    cedar and a plane in Lucca, both dedicated on the same morning as the Atlas
    cedar they sit beside. Those are three real trees this check would have
    quietly retired.

    So the guard is the one passcheck.py already applies for the same reason:
    when both sides name a species and the genus differs, it is not the same
    tree whatever the distance says. Where either side is silent the coordinate
    still wins, because an unnamed lead on a published tree's exact point is
    almost always that tree."""
    loc = entry.get("location") if isinstance(entry.get("location"), dict) else entry
    lat = loc.get("latitude", loc.get("lat"))
    lng = loc.get("longitude", loc.get("lng"))
    if lat is None or lng is None:
        return None
    hit = _city_coords(city_slug).get((round(lat, 4), round(lng, 4)))
    if not hit:
        return None
    g_lead = _genus(entry.get("species"))
    g_live = _genus(_city_species(city_slug).get(hit, ""))
    if g_lead and g_live and g_lead != g_live:
        return None
    return hit


def classify(entry, blocking):
    """Return the blocking rule this lead trips, or None.

    None means publishable. That includes leads whose reason we cannot parse,
    which is deliberate: an unreadable reason is not evidence of a problem, and
    treating it as one is exactly the habit this file exists to end.
    """
    # A pass that has already looked at this tree and HELD it is evidence, and
    # stronger than any keyword. Added 2026-08-14: Braga's two Tibaes trees
    # were held that morning (the monastery's cerca is closed for works, the
    # notice names the lake they stand beside) and leads.py offered all three
    # back as READY the same afternoon, folded twin included. A status field
    # someone deliberately set is not a lead waiting for prose.
    status = str(entry.get("status") or "").strip().lower()
    if status in ("folded", "blocked", "held", "duplicate", "resolved"):
        return {"label": "held by an earlier pass (status: %s)" % status}
    # The fix above only works when a pass remembers to also set status to
    # "held", and in practice it often does not: Braga's own two entries still
    # read status "lead" today, prose only. Found 2026-08-16 when a Guimaraes
    # verify pass spent 109k tokens re-confirming what its own leads file
    # already said in words ("Held back only on access... Needs Hidde's
    # call"), and Braga's identical "HELD ON ACCESS" pair would have cost the
    # next pass the same. This is not a new blocking judgement (that list
    # needs Hidde, see data/block-reasons.json): it is reading a determination
    # an earlier pass already recorded in its own words. Deliberately narrow,
    # matched against real corpus text before being written: requires "on"
    # plus one of the reasons this project actually uses this marker for.
    # "Held on count[...]" (a quota, forbidden by CLAUDE.md as a reason to
    # hold anything back) and incidental prose ("open days, held in spring,
    # announced on...") are excluded on purpose; a bare "held" elsewhere in
    # the text is not treated as this marker.
    why_field = str(entry.get("why") or entry.get("why_not_published") or entry.get("reason") or "")
    if HELD_MARKER.search(why_field):
        return {"label": "held by an earlier pass's own note (its status field was never updated)"}
    why = reason_text(entry)
    for rule in blocking:
        for pat in rule["patterns"]:
            if re.search(pat, why, re.I):
                return rule
    return None


def readiness(entry):
    """Can a story be written from what we already hold, with no new research?

    Needs a name to call it, a species to describe it, and a position to send
    someone to. Anything else (age, girth, photo, second source) is optional by
    ruling, so it is not checked here.
    """
    loc = entry.get("location") if isinstance(entry.get("location"), dict) else entry
    missing = []
    if not entry.get("name") or entry.get("name") == "?":
        missing.append("name")
    if not entry.get("species"):
        missing.append("species")
    if (loc.get("latitude", loc.get("lat")) is None
            or loc.get("longitude", loc.get("lng")) is None):
        missing.append("position")
    return missing


def load(city=None):
    pat = f"{city}.json" if city else "*.json"
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "leads", pat))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        for e in (d.get("leads") or []):
            if isinstance(e, dict):
                yield os.path.basename(f)[:-5], e


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city")
    ap.add_argument("--ready", action="store_true")
    a = ap.parse_args()

    r = rules()
    blocking = r["blocking"]
    ready, needs, blocked, done = [], [], [], []
    matched = 0
    for city, e in load(a.city):
        if is_done(e):
            done.append((city, e))
            continue
        match = published_match(city, e)
        if match:
            done.append((city, e))
            matched += 1
            continue
        rule = classify(e, blocking)
        if rule:
            blocked.append((city, e, rule))
            continue
        miss = readiness(e)
        (ready if not miss else needs).append((city, e, miss))

    total = len(ready) + len(needs) + len(blocked) + len(done)
    print(f"\n{total} leads. Fail-open: anything not matching data/block-reasons.json ships.\n")
    print(f"  {len(ready):4d}  READY: publishable now, needs only a story written")
    if done:
        extra = f" ({matched} caught only by coordinate match, no marker)" if matched else ""
        print(f"  {len(done):4d}  DONE: already published, kept as a record{extra}")
    print(f"  {len(needs):4d}  NEARLY: unblocked, but missing a field a story needs")
    print(f"  {len(blocked):4d}  BLOCKED: genuinely cannot ship")

    if blocked:
        by = {}
        for _, _, rule in blocked:
            by[rule["label"]] = by.get(rule["label"], 0) + 1
        print("\n  blocked breaks down as:")
        for k, v in sorted(by.items(), key=lambda x: -x[1]):
            print(f"    {v:4d}  {k}")

    if needs:
        by = {}
        for _, _, miss in needs:
            for m in miss:
                by[m] = by.get(m, 0) + 1
        print("\n  the NEARLY pile is missing:")
        for k, v in sorted(by.items(), key=lambda x: -x[1]):
            print(f"    {v:4d}  no {k}")

    show = ready if (a.ready or a.city) else []
    if show:
        print(f"\n  READY, by city:")
        by = {}
        for city, e, _ in show:
            by.setdefault(city, []).append(e)
        for city in sorted(by, key=lambda c: -len(by[c])):
            print(f"\n  {city} ({len(by[city])})")
            for e in by[city]:
                print(f"    {e.get('name','?')[:56]}  {str(e.get('species',''))[:34]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
