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
    python3 scripts/leads.py --ready          only leads a pass has actually
                                               sourced and that need just a story

READY means a pass looked at this tree and left evidence (a register entry or
a why/reason note), not merely that a name and a coordinate exist. A lead with
neither is filed under NEARLY, missing "source", because it has never been
verified and writing from it would be inventing facts to fit a template.
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
DONE = re.compile(r"\bresolved\b|\bdelivered as\b|\bdelivered to\b|"
                  r"\balready published\b|\bpromoted\b|\bshipped as\b", re.I)


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

# A second shape of the same problem, found 2026-08-23: a verify or write pass
# often declines a lead in its OWN words without ever setting `status` or using
# the word HELD, and a mechanical reader (this file, or a future write pass
# reading `leads.py --ready`) has no way to tell that apart from a lead nobody
# has looked at yet. Vienna is the worked example: all 8 of its "READY" leads
# that afternoon turned out to be candidates an earlier verify pass had
# individually considered and declined (a live political dispute over the
# tree's address, two trees planted in 1977/2016 and too young to be
# remarkable, an unresolved access question, "off the Ring walk or a weaker
# specimen than the six shipped this pass"), none of it recorded anywhere
# `is_done()` or `HELD_MARKER` could see, because those phrases use neither
# "resolved" nor "HELD... on". Rome's leads file uses a third, cleaner
# convention for the same thing, a bracketed tag: "[SKIPPED 2026-08-14 by the
# write pass]". Both are read here.
#
# This must NOT catch the one thing that looks similar and is a different
# problem entirely: a lead held back only on COUNT ("held back on count
# rather than merit", "ready to ship, held back only to avoid overshooting
# the target") is a candidate CLAUDE.md explicitly says must ship regardless
# ("being ninth in line is not a reason to hold a tree back"), and excluding
# those from READY would be reintroducing the exact over-strictness the
# fail-open design of this file exists to undo. Checked against the corpus
# before being written: `not pursued`, `left unverified` and `left
# undelivered` produced zero count/target/quota hits across every leads file
# (the one near-miss, "one blog account", is the substring "count" inside
# "account", not a real one), so the phrases below are safe as written. If a
# future case combines one of these phrases with a count-based reason,
# not_ready_marker() below checks the whole entry for a count word, not just
# a short lookahead window, so a count-based justification anywhere in the
# text keeps the lead in READY rather than mis-filing it.
#
# Widened 2026-08-31: a leads.py --ready dispatch found 9 of 10 cities'
# "READY" trees were leads an earlier pass had explicitly declined in its own
# words, just not in one of the three phrasings above. Menorca's four were
# private land with no access evidence (a real hard-rule-10 case, "privada"
# never matched the English-only "private" pattern below); Vienna's ginkgo,
# Perugia's cedar, Paris's mulberry, Napoli's plane, Zaragoza's lime and
# Kagoshima's camphor were each held on access, identity, a register
# conflict, survival doubt or a delisted register number, each in different
# words. Every phrase below was checked against the FULL leads corpus before
# being added (not just the flagged cities) for both count: each is a small,
# specific hit list, and content: every hit is a genuine hold, never a lead
# that should still ship. "would need a" and "likely/almost certainly
# beyond" target the day-trip-boundary case specifically (an unverified or
# doubtful transit claim), which is a location-honesty question and not the
# same thing as CLAUDE.md's protected "nobody got round to researching it
# further" (bare distance or lack of a second source, which stays READY).
NOT_READY_MARKER = re.compile(
    r"\[SKIPPED\b[^\]]*\]|\b(?:not pursued|left unverified|left undelivered|"
    r"ship once|not delivered on|removed from protection|"
    r"survival is a genuine question|identity unresolved|unresolved conflict|"
    r"could be a genuine second|almost certainly beyond|likely beyond|"
    r"would need a)\b",
    re.I)
COUNT_DOCTRINE_WORDS = re.compile(r"\b(?:count|quota|target|overshoot)\b", re.I)


def not_ready_marker(why):
    """True when an earlier pass declined this lead in its own words.

    Skips the whole thing if a count-doctrine word (count, quota, target,
    overshoot) appears ANYWHERE in the text: CLAUDE.md is explicit that being
    ninth in line, or any other count-based reason, must never hold a tree
    back, so a lead whose only recorded objection is about count stays in
    READY rather than being mis-filed as declined.
    """
    return bool(NOT_READY_MARKER.search(why)) and not COUNT_DOCTRINE_WORDS.search(why)


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
    # A tree carrying `pulled_from_city` was not merely unattended, it was
    # DEMOTED from a published page by name, on Hidde's own paid-entry-ratio
    # ruling (CLAUDE.md, "at most about a third of a city may sit behind a
    # ticket"). Found 2026-08-27: leads.py --ready offered Amsterdam's Artis/
    # Hortus quintet straight back as READY, and shipping them would have
    # exactly reproduced the 39-tree, 10-paid state Hidde rejected ("ik heb
    # liever 34 goede bereikbare dan 39"). Every fact in these entries is
    # verified, which is exactly why nothing else here would have caught
    # them: this is a placement decision, not a truth problem, and it needs
    # a fresh paid-ratio check (not a blind readd) before any of them ship.
    if entry.get("pulled_from_city"):
        return {"label": "pulled from a published city on a ratio/reach ruling, not merely unattended"}
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
    if not_ready_marker(why):
        return {"label": "an earlier pass looked at this and declined it in its own words (not a status field, not HELD... on)"}
    for rule in blocking:
        for pat in rule["patterns"]:
            if re.search(pat, why, re.I):
                return rule
    return None


def has_source_evidence(entry):
    """Was this lead ever looked at by a pass, or is it a bare scrape?

    A register entry (register_id/register_notes) or a why/reason field left
    by a pass that actually considered the tree both count, per Step 2's
    "one official register counts as one source" and the ship-rough doctrine
    that a single source is fine to publish flagged. What does not count is
    silence: a name, a coordinate and maybe photos, with nothing else.

    That silence is exactly the shape of famous_trees.py's output. CLAUDE.md
    is explicit about that file: "Treat that file as a research list, never
    an import: its name matching is deliberately loose and has produced
    nonsense." Its entries carry no register, no verify_notes and no why,
    because no pass has ever confirmed them; the genus in `species` is a
    guess read off the tree's own name, not a finding.
    """
    return bool(entry.get("register_id") or entry.get("register_notes")
                or entry.get("why") or entry.get("why_not_published")
                or entry.get("reason"))


def readiness(entry):
    """Can a story be written from what we already hold, with no new research?

    Needs a name to call it, a species to describe it, a position to send
    someone to, and SOME evidence a pass actually looked at it. Age, girth,
    photo and a second source are optional by ruling and not checked here;
    a total absence of sourcing is not the same gap and is checked below.

    Added 2026-08-30, the third time this file's own READY count was found to
    include unresearched leads: LOG.md records it twice on 2026-08-29 (a
    session that sampled a dozen READY leads across nine cities and found
    only 11 carried real sources, and a second entry naming the same gap by
    name) and the fix was left for "a session tightening what leads.py
    --ready actually promises". Measured the day this was written: 401 of
    446 READY leads were _famous-* entries with no register, no why, nothing
    beyond a name and a guessed genus, mostly Japanese and Baltic giant-tree
    lists with photos already attached. Writing a story from those would be
    inventing facts to fill a template, which hard rule 2 forbids regardless
    of how the gap arrived.
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
    if not has_source_evidence(entry):
        missing.append("source (never looked at by a pass, only scraped)")
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


STACK_M = 15.0  # closer than this and a visitor is standing in one spot


def fold_stacked(ready):
    """Split READY into (still ready, folded), where folded means several
    entries share one standing place.

    Found 2026-08-16 on Toronto: six of its thirteen READY leads carried the
    same heritage designation, HT-2016-121, and the SAME COORDINATE to four
    decimals, spread 0 metres. Shipping them would have produced six near
    identical pages for one place to stand, which fails CLAUDE.md's rule that
    an entry must be a collectible point, six times over. It is also the
    Setubal-twins problem, which the corpus already records as a thing
    registers do: a register counts what it designates, not what a visitor
    sees, and one designation over a group becomes N rows on import.

    This is the second time in one session that READY turned out not to mean
    verified, so by the standing ratchet it stops being a caution and becomes
    a check. Deliberately narrow: it does not block anything and it does not
    judge quality. It moves stacked entries out of the "needs only a story"
    bucket, because the honest next step for them is one folded entry written
    by someone who has looked, not N stories.

    Distance, not id: a shared registration number is the usual cause, but
    coordinates are what a reader actually experiences, and no naming scheme
    is common to every register we import.
    """
    from geo import km as _km
    groups, loose = {}, []
    for row in ready:
        e = row[1]
        la, lo = e.get("lat"), e.get("lng")
        if la is None or lo is None:
            loose.append(row)
            continue
        for key in groups:
            if _km(key, (la, lo)) * 1000 <= STACK_M:
                groups[key].append(row)
                break
        else:
            groups[(la, lo)] = [row]
    still, folded = list(loose), []
    for rows in groups.values():
        if len(rows) > 1:
            folded.append(rows)
        else:
            still.extend(rows)
    return still, folded


def buckets(city=None):
    """The one classification of the leads corpus, for anyone who needs a count.

    Extracted 2026-08-28 because prepare.py grew its own version of this to
    print the writable count at the top of every run, and got 563 where this
    file said 366: it applied classify() and readiness() but not
    published_match() or fold_stacked(). A second implementation of a
    classification is a second answer to the same question, and the wrong one
    was the one a night run would have read first.
    """
    blocking = rules()["blocking"]
    ready, needs, blocked, done = [], [], [], []
    matched = 0
    for city_slug, e in load(city):
        if is_done(e):
            done.append((city_slug, e))
            continue
        if published_match(city_slug, e):
            done.append((city_slug, e))
            matched += 1
            continue
        rule = classify(e, blocking)
        if rule:
            blocked.append((city_slug, e, rule))
            continue
        miss = readiness(e)
        (ready if not miss else needs).append((city_slug, e, miss))
    ready, folded = fold_stacked(ready)
    return {"ready": ready, "needs": needs, "blocked": blocked,
            "done": done, "folded": folded, "matched": matched}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city")
    ap.add_argument("--ready", action="store_true")
    a = ap.parse_args()

    b = buckets(a.city)
    ready, needs, blocked = b["ready"], b["needs"], b["blocked"]
    done, folded, matched = b["done"], b["folded"], b["matched"]
    total = len(ready) + len(needs) + len(blocked) + len(done) + len(folded)
    print(f"\n{total} leads. Fail-open: anything not matching data/block-reasons.json ships.\n")
    print(f"  {len(ready):4d}  READY: publishable now, needs only a story written")
    if done:
        extra = f" ({matched} caught only by coordinate match, no marker)" if matched else ""
        print(f"  {len(done):4d}  DONE: already published, kept as a record{extra}")
    print(f"  {len(needs):4d}  NEARLY: unblocked, but missing a field a story needs")
    if folded:
        n = sum(len(g) for g in folded)
        print(f"  {n:4d}  STACKED: {len(folded)} group(s) sharing one standing place, "
              f"one folded entry each, not one story per row")
        for g in folded:
            city = g[0][0]
            names = ", ".join((row[1].get("name") or "?")[:30] for row in g[:3])
            more = f" +{len(g) - 3} more" if len(g) > 3 else ""
            print(f"        {city}: {len(g)} at one point  {names}{more}")
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
