#!/usr/bin/env python3
"""The cheap contract checks, run before pushing instead of one per red build.

Written 2026-08-09. Five city files grew that morning and the deploy went red
four times in a row, each build surfacing exactly one violation because a
build throws on the first error it meets: a stale count promise, then an
intro over the word range, then a description over 155. Each round trip cost
a push and two minutes. Everything below is already enforced at build time in
site/src, and it is enforced there too; this only moves the finding-out to
before the push. It is a mirror, never the authority: when the two disagree
the Astro build wins and this file is the thing that is wrong.

Usage: python3 scripts/preflight.py
"""
import glob
import json
import os
import re
import sys

DESC_MAX = 155          # site/src/lib/site-config.ts
INTRO_MIN, INTRO_MAX = 60, 100   # Contract C, site/src/pages/[city].astro

WORDS = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
         "fifteen sixteen seventeen eighteen nineteen twenty twenty-one twenty-two twenty-three "
         "twenty-four twenty-five twenty-six twenty-seven twenty-eight twenty-nine thirty").split()
NUM = {w: i for i, w in enumerate(WORDS)}
N = "|".join([r"\d+"] + sorted(WORDS, key=len, reverse=True))
NMW = r"(?<![\w-])"      # not the tail of a compound number
SUMMARY = {"meta_description", "question_meta"}
ALL_COPY = {"intro", "meta_description", "question_meta", "question_answer", "question_context", "faq"}

PROMISE = [
    (re.compile(NMW + r"(%s)\s+(?:most|remarkable)\b" % N, re.I), lambda n: {n}, ALL_COPY),
    (re.compile(NMW + r"(%s)\s+more\b" % N, re.I), lambda n: {n + 1, n + 2}, SUMMARY),
    (re.compile(r"\bof the\s+" + NMW + r"(%s)\s+trees?\b" % N, re.I), lambda n: {n}, ALL_COPY),
    (re.compile(r"\b(?:these|the)\s+" + NMW +
                r"(%s)\s+(?:are|is|need|needs|were|was|stand|stands|remain|listed|below)\b" % N, re.I),
     lambda n: {n}, ALL_COPY),
    (re.compile(r"\ball\s+" + NMW + r"(%s)\s+(?:trees?|are|stand|need|needs|remain)\b" % N, re.I),
     lambda n: {n}, ALL_COPY),
    # "Sixteen verified locations, real stories." The standard meta_description
    # closer, and the one this check never covered until Geneva and Utrecht
    # both grew in one session with this exact phrase still naming the old
    # count.
    (re.compile(NMW + r"(%s)\s+verified\s+locations?\b" % N, re.I), lambda n: {n}, SUMMARY),
    # "Yes, all fourteen." Anchored on "Yes," so Frankfurt's "the station for
    # all four" (four of six, mid sentence) is not a false positive.
    (re.compile(r"\bYes,\s+all\s+" + NMW + r"(%s)\." % N, re.I), lambda n: {n}, ALL_COPY),
    # "The full six." question_meta's own fixed closer; always the total.
    (re.compile(r"\bfull\s+" + NMW + r"(%s)\." % N, re.I), lambda n: {n}, ALL_COPY),
]


def check_city(path):
    d = json.load(open(path))
    slug = os.path.basename(path)[:-5]
    n = len(d.get("trees", []))
    out = []

    intro = (d.get("intro") or "").strip()
    if not intro:
        out.append("%s: no intro, Contract C requires 60-100 words" % slug)
    else:
        wc = len(intro.split())
        if not INTRO_MIN <= wc <= INTRO_MAX:
            out.append("%s: intro is %d words, Contract C requires %d-%d" % (slug, wc, INTRO_MIN, INTRO_MAX))

    for key in ("meta_description", "question_meta"):
        v = d.get(key) or ""
        if len(v) > DESC_MAX:
            out.append("%s: %s is %d chars, the limit is %d" % (slug, key, len(v), DESC_MAX))

    fields = [(k, d.get(k) or "") for k in
              ("intro", "meta_description", "question_meta", "question_answer", "question_context")]
    for f in d.get("faq") or []:
        fields += [("faq", f.get("q") or ""), ("faq", f.get("a") or "")]
    for key, text in fields:
        if not text:
            continue
        for rx, allowed, scope in PROMISE:
            if key not in scope:
                continue
            for m in rx.finditer(text):
                w = m.group(1).lower()
                claims = allowed(int(w) if w.isdigit() else NUM[w])
                if min(claims) < 4 or n in claims:
                    continue
                out.append("%s: %s promises %s trees but the city has %d (%r)" % (
                    slug, key, "/".join(str(c) for c in sorted(claims)), n, m.group(0)))
    return out


# Contract B, mirrored from site/src/pages/[city]/oldest-tree.astro. Added
# 2026-08-13 after four new cities went out with a 46-word question_context and
# the deploy went red on the first one: preflight checked the intro's word range
# and the description's length and had never looked at this field, so the whole
# point of running it before pushing was lost. Same mirror rule as the rest of
# this file: the Astro build is the authority and this only moves the finding-out
# earlier.
CONTEXT_MIN, CONTEXT_MAX = 150, 200


def check_contract_b(slug, d):
    out = []
    if not (d.get("trees") or []):
        return out
    answer = (d.get("question_answer") or "").strip()
    context = (d.get("question_context") or "").strip()
    if not answer or not context:
        out.append("%s: question_answer and question_context must both be written (Contract B)" % slug)
        return out
    wc = len(context.split())
    if wc < CONTEXT_MIN or wc > CONTEXT_MAX:
        out.append("%s: question_context is %d words, Contract B requires %d-%d"
                   % (slug, wc, CONTEXT_MIN, CONTEXT_MAX))
    return out


RECOGNISE_MAX = 240
# Hidde, 2026-08-12, seeing the field on all eleven Den Bosch trees: "kun je deze
# which one is it functie weghalen, hij is alleen in den bosch, dit zou logisch
# om dieper te doen bij specifiek bomen die moeilijk te vinden zijn. niet bij
# elke in den bosch." Two failures at once. It was on every tree in the city
# including ones standing alone with nothing to confuse them for, and the longest
# ran to 499 characters of method: a register id, a re-confirmation date, GPS
# coordinates and an aerial-imagery cross-check. That is our working shown to a
# reader who asked which trunk to walk to, which is the builder-speak rule
# arriving in a new field.
#
# So the field is for trees a visitor genuinely cannot pick out: near-identical
# neighbours of the same species, close enough that the pin cannot settle it.
# One plain sentence about what you SEE. Never the evidence behind it.
RECOGNISE_METHOD = [
    r"register id", r"registered GPS", r"aerial imagery", r"cross-check",
    r"re-confirmed", r"\bper both\b", r"\b20\d\d-\d\d-\d\d\b",
    r"municipal register", r"coordinates",
]


def check_recognise(slug, d):
    out = []
    for tree in d.get("trees") or []:
        v = (tree.get("how_to_recognise") or "").strip()
        if not v:
            continue
        if len(v) > RECOGNISE_MAX:
            out.append("%s: %s how_to_recognise is %d chars, the limit is %d. "
                       "One plain sentence about what you see."
                       % (slug, tree.get("id"), len(v), RECOGNISE_MAX))
        for pat in RECOGNISE_METHOD:
            if re.search(pat, v, re.I):
                out.append("%s: %s how_to_recognise shows our method (%s). "
                           "The reader wants the tree, not the evidence."
                           % (slug, tree.get("id"), pat))
    return out


# Two cities must never share an id prefix. Added 2026-08-13, after a Portland
# write pass came back with ten trees numbered por_001 to por_010, which is
# Porto's prefix and covers ten live, indexed Porto trees. Merging would have
# overwritten them, which is hard rule 3. The writing pass caught it and refused;
# the brief that told it to use por_ was mine, written without running
# passcheck.py --brief, which prints the free prefix precisely so this cannot
# happen. A mechanism nobody runs is not a mechanism, so this one runs itself.
def check_id_prefixes():
    import collections
    owner = collections.defaultdict(set)
    for path in sorted(glob.glob("data/cities/*.json")):
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        for tree in d.get("trees") or []:
            tid = tree.get("id") or ""
            if "_" in tid:
                owner[tid.split("_")[0]].add(d.get("city") or path)
    out = []
    for prefix, cities in sorted(owner.items()):
        if len(cities) > 1:
            out.append("id prefix %r is used by %s: two cities sharing a prefix "
                       "will overwrite each other's trees" % (prefix, ", ".join(sorted(cities))))
    return out


# A pin a pin pass could not confirm must not become "confirmed" later without
# NEW evidence. Added 2026-08-13, after Baarn's brn_005. The pin pass wrote in
# data/research/baarn-pins.json that the tree's marker "could not be located in
# the aerial imagery" and left it approximate. A later pass set it to confirmed
# citing that same aerial survey, and the pin turned out to sit 60 metres off,
# on a different tree. Nothing was fabricated at any step: an earlier finding of
# our own simply sat in a file nobody re-read. So the file reads itself now.
# New evidence is a real thing (a site visit, a register coordinate, Wikidata,
# OSM, a fresh aerial check), named in the tree's own sources.
PIN_NEW_EVIDENCE = re.compile(
    r"on-site|site visit|photograph|register|geoproxy|arcgis|wikidata|inaturalist"
    r"|overpass|openstreetmap|\bosm\b|pdok|luchtfoto|aerial|geoportal|gis\b", re.I)


def check_pin_upgrades():
    pins = {}
    for path in sorted(glob.glob("data/research/*-pins.json")):
        try:
            with open(path, encoding="utf-8") as fh:
                d = json.load(fh)
        except (ValueError, OSError):
            continue
        rows = d if isinstance(d, list) else (d.get("pins") or d.get("trees") or [])
        for r in rows:
            if isinstance(r, dict) and r.get("id"):
                pins[r["id"]] = (os.path.basename(path), r.get("new_precision"))
    out = []
    for path in sorted(glob.glob("data/cities/*.json")):
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        for tree in d.get("trees") or []:
            prev = pins.get(tree.get("id"))
            if not prev or prev[1] != "approximate":
                continue
            if tree.get("location_precision") != "confirmed":
                continue
            if not PIN_NEW_EVIDENCE.search(" ".join(tree.get("verified_sources") or [])):
                out.append(
                    "%s: %s is marked confirmed, but %s recorded this pin as approximate "
                    "and no source names new evidence (a site visit, a register or Wikidata "
                    "coordinate, OSM, a fresh aerial check). Say where the certainty came "
                    "from, or leave it approximate."
                    % (os.path.basename(path)[:-5], tree.get("id"), prev[0]))
    return out


# Two cities must never publish the same physical tree under two ids. Added
# 2026-08-16, after REVIEW.md's 2026-08-16 BLOCKER: Potsdam's pot_005/pot_006
# republished Berlin's already-live ber_012/ber_011 (same register ids,
# coordinates 10-15m apart), one tree collectible twice under two names and
# two cities. superlatives.py already catches two pages claiming the same
# crown; nothing caught two pages claiming the same trunk. Same shape as
# check_id_prefixes: build one index across every city file, flag collisions.
DUPLICATE_TREE_RADIUS_M = 60


def check_cross_city_duplicates():
    import math
    trees = []
    for path in sorted(glob.glob("data/cities/*.json")):
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        city = d.get("city") or path
        for t in d.get("trees") or []:
            loc = t.get("location") or {}
            lat, lon = loc.get("latitude"), loc.get("longitude")
            if lat is None or lon is None:
                continue
            trees.append((lat, lon, city, t.get("id"), t.get("name")))
    out = []
    for i in range(len(trees)):
        lat1, lon1, city1, id1, name1 = trees[i]
        for lat2, lon2, city2, id2, name2 in trees[i + 1:]:
            if city1 == city2:
                continue
            dlat = (lat1 - lat2) * 111320
            dlon = (lon1 - lon2) * 111320 * math.cos(math.radians((lat1 + lat2) / 2))
            dist = math.hypot(dlat, dlon)
            if dist <= DUPLICATE_TREE_RADIUS_M:
                out.append(
                    "%s (%r, %s) and %s (%r, %s) are %.0fm apart across two cities: "
                    "likely one physical tree published twice"
                    % (id1, name1, city1, id2, name2, city2, dist))
    return out


# A stack of pins is a SMELL, not a defect, and this prints rather than fails
# for a reason worth stating. Six trees on one coordinate along a 0.7 mile
# signposted loop is fine: you park, you walk, you see all six. The same six
# inside a 1.4 square kilometre cemetery sends somebody to one point and leaves
# them searching, which is the one failure this project cannot afford. The
# difference is the size of the site, and no script can measure that from a
# city file. So it names the stack and a person decides.
STACK_LIMIT = 4


def check_stacked_pins():
    """Trees in one city sharing an identical coordinate.

    Found 2026-08-20 by Hidde, who looked at the Hawaii page, saw one map pin
    labelled 6 and said it seemed unlikely. He was right to doubt it: the state
    register rounds coordinates to two decimals, about a kilometre, and all six
    Kalopa trees came through on the same grid point. The page had said so in
    three places and the map still read as broken.

    Nineteen cities carried a stack that day. Most are pairs and threes inside
    one small garden, which is what `approximate` is for. The three fixes, in
    order of preference: pin the place a visitor should actually go to (Hawaii
    moved from the register's rounded grid point to the park itself), say in
    `access` where within the site to look, or fold the trees into one entry
    when they really are one destination. Never spread pins apart to fill the
    gap, which would invent precision and is the error this whole field exists
    to prevent."""
    out = []
    for path in sorted(glob.glob("data/cities/*.json")):
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        seen = {}
        for t in d.get("trees") or []:
            loc = t.get("location") or {}
            key = (loc.get("latitude"), loc.get("longitude"))
            if key[0] is None:
                continue
            seen.setdefault(key, []).append(t.get("id"))
        for key, ids in seen.items():
            if len(ids) >= STACK_LIMIT:
                out.append("%s: %d trees share one coordinate %.5f,%.5f (%s). "
                           "Pin the place a visitor should go to and say in "
                           "access where to look; never spread pins apart to "
                           "fake precision."
                           % (d.get("city") or path, len(ids), key[0], key[1],
                              ", ".join(ids)))
    return out


# The season files are hand-edited and their key names are not guessable. The
# label for a flowering is `flower_label`, singular, while the month array beside
# it is `flowers`, plural. On 2026-08-20 I wrote nine flowering descriptions
# under `flowers_label` because I derived the key from the moment name instead
# of reading the file, and site/src/lib/phenology.ts never saw one of them. A
# key nobody reads is worse than a missing one: the work looks done.
PHENOLOGY_KEYS = {
    "common_name", "habit", "leaf", "flowers", "fruit", "colour", "bare",
    "intensity", "flower_label", "fruit_label", "colour_label", "sources",
    "peak", "flower_colour", "flower_peak", "flower_days",
}
# Blossom is not curated the way the other moments are. Hidde, 2026-08-21:
# "alle bomen die bloeien mogen de animatie van bloei in de kleur van hun bloei,
# op hun moment." So any species whose flowering is visible at all blooms on the
# map in its own colour, and the only thing that disqualifies one is that nobody
# can see it: a plane flowers every April and no one has ever noticed. That is
# what `intensity.flowers == "unseen"` records, and it is the whole gate.
# `peak` answers the six questions Hidde asked of this database on 2026-08-20:
# which phenotype, what the calendar looks like, when the peak falls, whether it
# is worth sharing, what the map should do, and where else it is surfaced. The
# first two were already answered by habit and the month arrays; the other four
# were not stored anywhere.
#
# It deliberately does NOT repeat the grade. A peak block may only exist where
# intensity already rates that moment "worth the trip", and the check below
# enforces it, so the judgement lives in one place and cannot drift from its
# copy. That is the same rule the layout thresholds got today: a bar written
# down twice stops being one bar.
PEAK_KEYS = {"moment", "months", "share", "map", "surfaces"}
MAP_EFFECTS = {"falling-leaves", "blossom", "fruit-drop", "catkins", "bare-frame"}
SURFACES = {"map", "push", "tree", "city", "home", "collection"}
PHENOLOGY_MOMENTS = {"leaf", "flowers", "fruit", "colour", "bare"}
INTENSITIES = {"unseen", "nice", "striking", "worth the trip"}


def check_phenology():
    """Season files: no key the build cannot read, no judgement it cannot parse."""
    out = []
    for path in sorted(glob.glob("data/phenology/*.json")):
        name = os.path.basename(path)
        try:
            with open(path, encoding="utf-8") as fh:
                d = json.load(fh)
        except Exception as exc:
            out.append("%s: will not parse (%s)" % (name, str(exc)[:60]))
            continue
        for k in d:
            if k not in PHENOLOGY_KEYS:
                out.append("%s: unknown key %r. The build reads only %s, so "
                           "anything else is written and never shown."
                           % (name, k, ", ".join(sorted(PHENOLOGY_KEYS))))
        fc = d.get("flower_colour")
        if fc is not None:
            if not (isinstance(fc, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", fc)):
                out.append("%s: flower_colour %r is not a #RRGGBB hex" % (name, fc))
            if not (d.get("flowers") or []):
                out.append("%s: flower_colour but no flowering months" % name)
            if (d.get("intensity") or {}).get("flowers") == "unseen":
                out.append("%s: flower_colour on a flowering rated 'unseen'. "
                           "If nobody can see it, it must not bloom on the map."
                           % name)

        fp = d.get("flower_peak")
        if fp is not None:
            if fp not in (d.get("flowers") or []):
                out.append("%s: flower_peak %r is not one of its flowering months %s"
                           % (name, fp, d.get("flowers")))
            if not d.get("flower_colour"):
                out.append("%s: flower_peak without a flower_colour" % name)

        peak = d.get("peak")
        if isinstance(peak, dict):
            for k in peak:
                if k not in PEAK_KEYS:
                    out.append("%s: peak has unknown key %r" % (name, k))
            mom = peak.get("moment")
            if mom == "flowers":
                out.append("%s: peak.moment is 'flowers'. Blossom is derived from "
                           "flower_colour and flower_peak, never curated, so a "
                           "curated one is a second answer that will drift from "
                           "the first. Drop it and set flower_peak." % name)
            if (d.get("intensity") or {}).get(mom) != "worth the trip":
                out.append("%s: peak names %r but intensity does not rate it "
                           "'worth the trip'. A peak is not a second opinion; "
                           "raise the intensity or drop the peak." % (name, mom))
            for m in peak.get("months") or []:
                if m not in (d.get(mom) or []):
                    out.append("%s: peak month %s is not in the %s calendar"
                               % (name, m, mom))
            eff = ((peak.get("map") or {}).get("effect"))
            if eff and eff not in MAP_EFFECTS:
                out.append("%s: map effect %r is not one of %s"
                           % (name, eff, ", ".join(sorted(MAP_EFFECTS))))
            for sfc in peak.get("surfaces") or []:
                if sfc not in SURFACES:
                    out.append("%s: surface %r is not one of %s"
                               % (name, sfc, ", ".join(sorted(SURFACES))))
        elif peak is not None:
            out.append("%s: peak must be an object" % name)
        for moment, level in (d.get("intensity") or {}).items():
            if moment not in PHENOLOGY_MOMENTS:
                out.append("%s: intensity names %r, which is not a moment" % (name, moment))
            if level not in INTENSITIES:
                out.append("%s: intensity %r for %s is not one of %s"
                           % (name, level, moment, ", ".join(sorted(INTENSITIES))))
    return out


def check_search_names():
    """Not a gate, a nag. Every published city should carry its name in other
    languages so the site search finds Den Haag as well as The Hague (Hidde,
    2026-08-18), but a city missing them is a missing nicety, not a broken
    page, and failing a deploy over it would block a night run from shipping a
    city behind a network call. So this prints and never fails. The night run
    regenerates them, which is what makes it standard practice rather than
    something anyone has to remember."""
    f = os.path.join("data", "city-aliases.json")
    if not os.path.exists(f):
        return []
    with open(f, encoding="utf-8") as fh:
        doc = json.load(fh)
    accounted = set(doc.get("search_names", {})) | set(doc.get("no_other_names", {})) \
        | set(doc.get("unresolved_names", {}))
    missing = sorted(os.path.basename(p)[:-5] for p in glob.glob("data/cities/*.json")
                     if os.path.basename(p)[:-5] not in accounted)
    if not missing:
        return []
    return ["%d city/cities have never been looked up in other languages (%s). "
            "Run: python3 scripts/city_names.py"
            % (len(missing), ", ".join(missing[:8]))]


def check_paid_share():
    """A city page should be walkable without buying tickets all day.

    The rule, set by Hidde on 2026-08-23 after Bomenstichting Amsterdam made
    the point twice: at most about a third of a city's trees may sit behind
    paid entry. Her words were that it stays "bezwaarlijk dat 10 bomen (een
    derde) niet gratis toegankelijk zijn", and his were "ik heb liever 34 goede
    bereikbare dan 39".

    A NOTE and not a FAIL, deliberately, because the honest fix is almost never
    a deletion. Paid entry is allowed and always has been, as long as `access`
    says so, and some cities really do keep their best trees in one old
    botanical garden. Leiden is the worked example: five were pulled there the
    day this check was written and three went straight back, because the first
    zelkovas ever to leave Japan and the thickest horse chestnut in the country
    are not padding. What the ratio means is "this city needs FREE trees
    added", which is research, not a red build.

    The one thing it does catch, and the reason it exists: a run that opens a
    city by taking the eight easiest trees out of one ticketed garden, which is
    how both Amsterdam and Leiden ended up over a third without anybody
    deciding to."""
    out = []
    for path in sorted(glob.glob("data/cities/*.json")):
        with open(path, encoding='utf-8') as fh:
            d = json.load(fh)
        trees = d.get("trees") or []
        if len(trees) < 6:
            continue
        paid = [t for t in trees if "aid entry" in (t.get("access") or "")]
        if len(paid) * 3 > len(trees):
            out.append("%s: %d of %d trees are behind paid entry (%d%%). Add free "
                       "trees rather than removing good ones; check the register "
                       "first." % (d.get("city", os.path.basename(path)[:-5]),
                                   len(paid), len(trees),
                                   round(100 * len(paid) / len(trees))))
    return out


def main():
    problems = (check_id_prefixes() + check_pin_upgrades()
                + check_cross_city_duplicates() + check_phenology())
    files = sorted(glob.glob("data/cities/*.json"))
    for p in files:
        problems += check_city(p)
        with open(p, encoding='utf-8') as fh:
            problems += check_recognise(os.path.basename(p)[:-5], json.load(fh))
        with open(p, encoding='utf-8') as fh2:
            problems += check_contract_b(os.path.basename(p)[:-5], json.load(fh2))
    for line in problems:
        print("FAIL " + line)
    for line in check_stacked_pins() + check_search_names() + check_paid_share():
        print("NOTE " + line)
    print("preflight: %d cities checked, %d problems" % (len(files), len(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
