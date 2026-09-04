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
import collections
import glob
import json
import math
import os
import re
import sys
import unicodedata

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


# The register identifiers that actually appear in verified_sources across the
# corpus. A shared one is what separates a duplicate from two neighbours:
# Portugal's ICNF processo codes, Hawaii's register_id, Poland's CRFOP fop ids,
# German Naturdenkmal numbers, NYC Parks' great-trees ids.
REGISTER_ID_PATTERNS = [
    re.compile(r"processo\s+([A-Z]{3}\d+/\d+)", re.I),
    re.compile(r"register_id\s+(\d+)", re.I),
    re.compile(r"fop=([A-Za-z0-9.]+)"),
    re.compile(r"\bND[-\s](\d+)\b"),
    re.compile(r"great-trees\?id=(\d+)"),
]

SAME_CITY_DUPLICATE_RADIUS_M = 100


def register_ids(tree):
    out = set()
    for s in tree.get("verified_sources") or []:
        for pat in REGISTER_ID_PATTERNS:
            for m in pat.findall(s):
                out.add(m.upper())
    return out


def check_same_city_duplicates():
    """One physical tree published twice inside ONE city file.

    The third occurrence of this class, and the first one a script can see.
    muc_015-018 (2026-08-13) re-wrote four Nymphenburg register entries already
    live as muc_011-014. pot_005/pot_006 (2026-08-16) duplicated Berlin's
    ber_012/ber_011 and were caught by a REVIEW.md BLOCKER. por_026/por_028 and
    por_019/por_029 duplicated the Cordoaria plane avenue and its bunya pine,
    and were found only because a digest reported 'alameda dos platanos' as a
    content gap while we had TWO pages ranking for it at position 8. Per the
    ratchet, a class that appears on three different days becomes a check.

    Distance alone cannot do this job, which is why check_cross_city_duplicates
    skips same-city pairs outright: trees legitimately stand metres apart, and
    a register that rounds its coordinates puts them on one point. Hawaii's four
    Kalopa trees, Nuremberg's ND-9 and ND-10 five metres apart, Poznan's four
    protected planes on one square and Osaka's two named camphors at one shrine
    are all real, all close, all correct.

    What every genuine duplicate shares and no legitimate neighbour does is a
    REGISTER ID. Hawaii's are 1184 and 1185; Nuremberg's are ND-9 and ND-10;
    Porto's two pairs each cite one processo twice. So the signal is a shared
    identifier plus proximity, and on the corpus as it stood when this was
    written it fired on exactly the two Porto pairs out of 1,842 trees.

    This FAILS rather than notes. Two pages for one tree is not a smell: it
    splits the trees' own search demand between them, it puts two ages and two
    girths on the site for one trunk, and the fix is a merge plus a redirect
    (RENAMED_TREE_SLUGS in site/src/lib/redirect-map.ts), never a deletion."""
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
            ids = register_ids(t)
            if ids:
                trees.append((lat, lon, city, t.get("id"), t.get("name"), ids))
    out = []
    for i in range(len(trees)):
        lat1, lon1, city1, id1, name1, ids1 = trees[i]
        for lat2, lon2, city2, id2, name2, ids2 in trees[i + 1:]:
            if city1 != city2:
                continue          # cross-city is check_cross_city_duplicates
            shared = ids1 & ids2
            if not shared:
                continue
            dlat = (lat1 - lat2) * 111320
            dlon = (lon1 - lon2) * 111320 * math.cos(math.radians((lat1 + lat2) / 2))
            dist = math.hypot(dlat, dlon)
            if dist <= SAME_CITY_DUPLICATE_RADIUS_M:
                out.append(
                    "%s (%r) and %s (%r) in %s are %.0fm apart and cite the same "
                    "register entry (%s): one tree with two pages. Merge into the "
                    "earlier id, fold in what the later one measured, and redirect "
                    "the retired slug."
                    % (id1, name1, id2, name2, city1, dist,
                       ", ".join(sorted(shared))))
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


_NUMBER_WORDS = {w: n for n, w in enumerate((
    "zero one two three four five six seven eight nine ten eleven twelve "
    "thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty "
    "twenty-one twenty-two twenty-three twenty-four twenty-five twenty-six "
    "twenty-seven twenty-eight twenty-nine thirty thirty-one thirty-two "
    "thirty-three thirty-four thirty-five thirty-six thirty-seven"
).split())}
_NUM_RX = "|".join(sorted((["\\d+"] + list(_NUMBER_WORDS)), key=len, reverse=True))


def _num(word):
    return int(word) if word.isdigit() else _NUMBER_WORDS.get(word.lower())


def check_country_counts():
    """A country page's own "N cities, M trees" closer must match reality.

    Found 2026-08-29 while opening Bamberg and Assisi: eleven of twenty-one
    country pages' meta_description carried a stale city and/or tree count,
    some (Poland: 23 against 63 real, the Netherlands: 14 mapped cities
    against 37 real) off by a wide margin. The city-level equivalent of this
    check (count-promises.ts) is a hard build failure; this one is a NOTE
    rather than a FAIL on its first day; per this file's own docstring it is
    "a mirror, never the authority", and no country-page authority exists
    yet to mirror. Widen to FAIL once an Astro-side check exists and this has
    run clean for a while, same as the ratchet everywhere else in this
    project: ship the check, promote it once trusted.

    Deliberately narrow, anchored patterns only (a country intro is full of
    OTHER numbers, ages, years, girths, that this must never trip on):
    a trailing "N cities/places [mapped], M trees" sentence at the very end
    of meta_description, or a "across N mapped cities" mid-sentence claim.
    Both are the exact phrasings already in use; a country whose copy uses
    neither pattern is silently skipped rather than guessed at.
    """
    real = {}
    for f in sorted(glob.glob("data/cities/*.json")):
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        country = d.get("country")
        if not country:
            continue
        n_cities, n_trees = real.get(country, (0, 0))
        real[country] = (n_cities + 1, n_trees + len(d.get("trees") or []))

    patterns = [
        re.compile(r"(?P<cities>%s)\s+(?:cities|places)(?:\s+mapped)?,\s*(?P<trees>%s)\s+trees\.?\s*$" % (_NUM_RX, _NUM_RX), re.I),
        re.compile(r"(?P<trees>%s)\s+trees\s+mapped\.?\s*$" % _NUM_RX, re.I),
        re.compile(r"across\s+(?P<cities>%s)\s+mapped\s+cities\b" % _NUM_RX, re.I),
    ]

    out = []
    for f in sorted(glob.glob("data/countries/*.json")):
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        country = d.get("country")
        meta = d.get("meta_description") or ""
        if country not in real:
            continue
        real_cities, real_trees = real[country]
        for pat in patterns:
            m = pat.search(meta)
            if not m:
                continue
            gd = m.groupdict()
            claimed_trees = _num(gd["trees"]) if gd.get("trees") else None
            claimed_cities = _num(gd["cities"]) if gd.get("cities") else None
            if claimed_trees is not None and claimed_trees != real_trees:
                out.append("%s: meta_description says %d trees, data has %d (%s)"
                           % (country, claimed_trees, real_trees, os.path.basename(f)))
            if claimed_cities is not None and claimed_cities != real_cities:
                out.append("%s: meta_description says %d cities, data has %d (%s)"
                           % (country, claimed_cities, real_cities, os.path.basename(f)))
            break
    return out


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
    deciding to.

    Reads the `paid_entry` boolean where a tree has one, falling back to the
    "paid entry" substring in `access` only for trees that don't (older data).
    REVIEW.md flagged this gap on 2026-08-29: this function used to read only
    the access STRING, which is why 8 trees across 5 cities had paid_entry
    correctly set but rendered no ticket banner (the boolean and the string
    are two different things a writer can get out of sync), and separately
    would have missed Cesky Krumlov's own three ("paid admission", "paid tour
    route") the same day for saying it three different honest ways rather
    than the one exact phrase this used to grep for."""
    out = []
    mismatches = []
    for path in sorted(glob.glob("data/cities/*.json")):
        with open(path, encoding='utf-8') as fh:
            d = json.load(fh)
        trees = d.get("trees") or []
        for t in trees:
            access_text = t.get("access") or ""
            has_flag = t.get("paid_entry") is True
            has_text = "aid entry" in access_text
            # "Free ... (the museum/building itself has paid entry)" is this
            # site's own idiom for a tree that is free while something next to
            # it is not (Aarhus's Moesgard trees, NYC's Van Cortlandt oak).
            # Only a leading "Free" counts as the guard: a stray later "free"
            # (as in "free to view from the path") is not the same claim.
            about_this_tree = not re.match(r"^\s*free\b", access_text, re.I)
            if has_text and not has_flag and about_this_tree:
                mismatches.append("%s/%s: access text says paid entry but paid_entry is not true"
                                  % (d.get("city", os.path.basename(path)[:-5]), t.get("id")))
        if len(trees) < 6:
            continue
        paid = [t for t in trees if t.get("paid_entry") is True
                or (t.get("paid_entry") is None and "aid entry" in (t.get("access") or ""))]
        if len(paid) * 3 > len(trees):
            out.append("%s: %d of %d trees are behind paid entry (%d%%). Add free "
                       "trees rather than removing good ones; check the register "
                       "first." % (d.get("city", os.path.basename(path)[:-5]),
                                   len(paid), len(trees),
                                   round(100 * len(paid) / len(trees))))
    return out + mismatches


# The words hard rule 10's first access test names. Deliberately NARROW, and
# the first draft was not: it also matched "closed to the public", "guided tour
# only" and "no public access", and produced eight hits of which one was real.
# A park shut for a year of restoration works, a garden with closing times, a
# ranger station closed beside an open lawn, and a daily ticketed tour you walk
# up and join are none of them a permission. What the rule actually names is a
# person you have to ask: an appointment, an arrangement, a booking, a doorbell,
# a reception desk. So that is all this matches, and it still catches every one
# of the five trees that failed on 2026-08-29.
NEEDS_PERMISSION = re.compile(
    r"\bby (?:prior )?appointment\b|\bprior arrangement\b|\bby arrangement\b"
    r"|\bop afspraak\b|\bprevia cita\b|\bsur rendez-vous\b|nach Vereinbarung"
    r"|must be booked|booked in advance|by prior request|on prior request"
    r"|not open to casual|ring the (?:door)?bell|ask at the reception",
    re.I)
# A tree you can SEE from ground the public may stand on is publishable and
# says so, which is the exception Hidde opened on 2026-08-13. Split's mulberry
# inside a rugby club's ground is the worked example.
VIEW_ONLY = re.compile(r"view-only|visible from|in (?:clear |full )?view from|from the "
                       r"(?:public )?(?:pavement|street|road|quay)", re.I)
# The field says outright that nobody has to be asked. Crete's olive at Vouves
# is the case: it takes appointments only through the winter off-season, is
# open daily the rest of the year, and ends "Signposted, and no permission is
# needed."
NO_PERMISSION = re.compile(r"no permission is needed|no permission needed|"
                           r"without an appointment|no appointment (?:is )?needed", re.I)
# The sentence is about a DIFFERENT place. Seville's lagunaria is the reason:
# its access field distinguishes the free city garden the tree stands in from
# the palace gardens next door, and it is the neighbours that need the
# appointment. A check that reads an access field as one undifferentiated blob
# calls that a failure.
ANOTHER_PLACE = re.compile(r"not the same ground|whose own|the adjoining|next door"
                           r"|rather than the|separate from", re.I)


def check_collection_targets():
    """A collection may not point at a tree that is not published.

    Written 2026-08-29, ten minutes after it happened. Five trees were pulled
    from live pages on hard rule 10, preflight passed, and the deploy died on
    /collections/the-oldest-tree-in-every-country-we-map with "Cannot read
    properties of undefined (reading 'name')", because that collection had
    named Kyoto's Katanami cedar as Japan's oldest and the id no longer existed.

    Removing a tree is normal work here and it will keep happening: a tree
    dies, an access line turns out to fail a rule, a duplicate is found. The
    expensive part is that a hand-curated collection is the one place a tree id
    is written down away from the city file, so nothing local to the removal
    ever looks at it. One comparison of two sets costs nothing and turns a red
    deploy into a line of output."""
    ids = set()
    for path in glob.glob("data/cities/*.json"):
        with open(path, encoding='utf-8') as fh:
            for t in json.load(fh).get("trees") or []:
                if t.get("id"):
                    ids.add(t["id"])
    out = []
    for path in sorted(glob.glob("data/collections/*.json")):
        try:
            with open(path, encoding='utf-8') as fh:
                doc = json.load(fh)
        except (ValueError, OSError):
            continue
        for entry in (doc.get("entries") or []):
            tid = isinstance(entry, dict) and entry.get("tree_id")
            if tid and tid not in ids:
                out.append("%s: names %s, which is not published in any city "
                           "file. Point it at a live tree or drop the entry; "
                           "the build cannot render a collection whose subject "
                           "does not exist."
                           % (os.path.basename(path)[:-5], tid))
    return out


def check_access_permission():
    """No published tree may need somebody's permission to reach.

    Hard rule 10's first test is one question, and it is not about how
    inconvenient a visit is: "Can they get in without asking anyone's
    permission? A reception desk to talk past, a doorbell, a code, an
    appointment, a guard who checks: no."

    Written 2026-08-29, after five live trees failed it. They were found by
    accident, while writing recognition lines for Malaga, whose avocado sat on
    a page with an access field reading "working school grounds, visits by
    prior appointment only". Grepping the rest of the database turned up four
    more: a Kyoto cedar needing a city permit and a guide, a Granada pair
    inside a university residence, The Hague's 1638 pear on a booked tour, and
    the ficus inside Valencia's regional parliament. Every one of them stated
    its own disqualification in its own access field, in plain English, and
    had done for months.

    That is the argument for a check rather than a rule. This one is a FAIL
    and not a NOTE, because unlike the paid-entry ratio there is nothing to
    weigh: the rule does not bend, and a page that sends somebody to a gate
    they cannot pass is a broken promise whatever the tree is like.

    The escape hatch is the real one Hidde opened on 2026-08-13: a tree you can
    SEE from ground the public may stand on ships, with the pin on the viewing
    place and the access line saying plainly what you can and cannot do. So an
    access field that says where to stand and look passes, and one that only
    says how to book does not."""
    out = []
    for path in sorted(glob.glob("data/cities/*.json")):
        with open(path, encoding='utf-8') as fh:
            d = json.load(fh)
        for t in d.get("trees") or []:
            access = t.get("access") or ""
            if VIEW_ONLY.search(access) or NO_PERMISSION.search(access):
                continue
            # Sentence by sentence, because an access field routinely describes
            # more than one place and the gate is often on the other one.
            hit = None
            for sentence in re.split(r"(?<=[.;]) +", access):
                if NEEDS_PERMISSION.search(sentence) and not ANOTHER_PLACE.search(sentence):
                    hit = sentence
                    break
            if hit is None:
                continue
            out.append("%s: %s needs somebody's permission to reach (%r). Hard "
                       "rule 10's first test: an appointment, a booked tour, a "
                       "doorbell or a reception desk is a no. Either it is "
                       "genuinely visible from public ground, in which case say "
                       "where to stand, or it comes off the page and goes to "
                       "data/leads/ with the reason."
                       % (os.path.basename(path)[:-5], t.get("id"), hit[:110]))
    return out


def check_register_licences():
    """No register file without a recorded licence.

    CLAUDE.md lists this among the seven lessons that stopped being notes and
    became build checks. It never was one. Searched 2026-08-27 after a
    copyright question from Hidde: neither qa.py nor this file carried it, and
    the corpus had been asserting the guarantee for weeks.

    The data was fine, which is the uncomfortable part. Fifty registers, fifty
    licences, so nothing was ever caught because nothing was ever wrong yet.
    A check that exists only in a document protects nothing on the day
    somebody imports in a hurry, and register imports are the cheapest trees
    this project gets, which is exactly when a hurry happens.

    Shapes accepted, because the existing files legitimately differ and
    normalising fifty files to satisfy a checker would be the tail wagging
    the dog: a top-level `licence`/`license`, a `licence_name` with its terms
    url beside it, or a `license` inside the `source` block. What is NOT
    accepted is a file that records where the data came from and never says
    what we are allowed to do with it.
    """
    out = []
    for f in sorted(glob.glob("data/registers/*.json")):
        name = os.path.basename(f)
        try:
            with open(f, encoding="utf-8") as fh:
                d = json.load(fh)
        except Exception as e:
            out.append("%s: unreadable (%s)" % (name, e))
            continue
        if not isinstance(d, dict):
            out.append("%s: no licence block; a register with no recorded "
                       "licence may not be imported (hard rule, register layer)" % name)
            continue
        lic = (d.get("licence") or d.get("license")
               or d.get("licence_name") or d.get("license_name"))
        src = d.get("source")
        if not lic and isinstance(src, dict):
            lic = src.get("license") or src.get("licence")
        if not lic:
            out.append("%s: no licence block; a register with no recorded "
                       "licence may not be imported (hard rule, register layer)" % name)
    return out



def check_no_sender_names():
    """A submitter's name must never be written down anywhere we publish.

    Hidde, 2026-08-11, on finding a submitter's name rendered on a tree page:
    "privacy technisch echt een no go... ookal is het via formulier niet meer
    doen nooit." That was day one. Day two was 2026-08-30, when a run closing
    reader submission #54 wrote the sender's real name into a tree's
    verify_notes and into a drafts/ file. It never rendered on the site, and it
    did not need to: this repository is public, so a name in data/ or drafts/ is
    published on GitHub the moment it is pushed.

    A lesson that appears on two different days becomes a build check, so here
    it is. The shape it looks for is the one that actually happened, a name in
    brackets straight after a submission reference, plus the older
    submitted_by field carrying anything new. Removing this check needs Hidde.
    """
    out = []
    pat = re.compile(r"submission\s*#?\s*\d+\s*\(([^)]{2,60})\)", re.I)
    allowed = ("gps", "app", "no name", "kind", "city", "tree", "feedback",
               "correction", "privacy", "photo", "test", "vote")
    targets = sorted(glob.glob("data/cities/*.json")) + sorted(glob.glob("drafts/*.md")) \
        + sorted(glob.glob("data/leads/*.json"))
    for path in targets:
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError:
            continue
        for m in pat.finditer(text):
            inside = m.group(1).strip()
            if any(a in inside.lower() for a in allowed):
                continue
            if re.match(r"^[A-Z][a-z]+(\s+[A-Z][a-z'\-]+)+$", inside):
                out.append("%s: a submitter's name is written next to a submission "
                           "reference (%r). No sender is ever named in anything we "
                           "publish, and this repo is public." % (path, inside))
    return out




def check_contributor_photos_are_traceable():
    """A reader's photograph must carry the account that sent it.

    Written 2026-09-03, before the first one was published, which is the only
    moment this could be written cheaply. /terms and /privacy both promise that
    deleting an account removes what was published with it, and the database
    keeps that promise properly. A published photograph is the one thing that
    lives outside the database: a copy in data/cities and a file in
    site/public/photos, in a static site no cascade can reach.

    scripts/photo_takedown.py keeps the promise by asking Supabase whether the
    contributing account still exists. It can only ask about an id it can see,
    so a reader's photograph without one is a photograph that can never be
    taken down, and the promise would be broken silently by the one page nobody
    would think to check.

    Hence both directions. A photograph marked as a reader's must name the
    account, and an id must not sit on a photograph not marked as one, because
    the sweep would not look at it. Removing this check needs Hidde: it is the
    mechanism behind a promise in the terms people accept at sign-in.
    """
    out = []
    for path in sorted(glob.glob("data/cities/*.json")):
        with open(path, encoding="utf-8") as fh:
            city = json.load(fh)
        for tree in city.get("trees", []):
            photo = tree.get("photo") or {}
            uid = photo.get("contributor_user_id")
            is_contrib = photo.get("source") == "contributor"
            if is_contrib and not uid:
                out.append("%s: %s carries a reader's photograph with no "
                           "contributor_user_id. It could never be taken down when "
                           "they delete their account, which /terms promises."
                           % (path, tree.get("id")))
            if uid and not is_contrib:
                out.append("%s: %s names a contributor_user_id without "
                           'photo.source == "contributor", so the takedown sweep '
                           "will not look at it." % (path, tree.get("id")))
    return out


def check_translated_components_are_neutral():
    """A component that renders every language must not have one typed into it.

    Found 2026-09-02 by LOOKING at a German tree page, which no check caught and
    no grep would have: every translated tree page in all seven languages was
    serving SPANISH labels. A Japanese reader got "Especie", "Edad estimada",
    "Ubicacion", "Acceso" and "Como llegar" above Japanese prose. It had been
    live since the seven-language rollout on 2026-08-22, because
    TranslatedTreePage.astro was written during the one-city Spanish test and
    its labels were never lifted into the string table when six more languages
    landed.

    The test is narrow and therefore trustworthy: these three components render
    for every language, so any Spanish-specific character in a literal inside
    them is by definition wrong. Comments are exempt, since the corpus explains
    itself in prose and several of those explanations quote Spanish.
    """
    out = []
    files = ["TranslatedTreePage.astro", "TranslatedQuestionPage.astro",
             "TranslatedCityPage.astro"]
    spanish = re.compile(r"[\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1\u00bf\u00a1]")
    for name in files:
        path = os.path.join("site", "src", "components", name)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as fh:
            lines = fh.readlines()
        for n, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith(("//", "*", "/*", "{/*")):
                continue
            if spanish.search(line):
                out.append("%s:%d has Spanish typed into a component that renders "
                           "every language, so it shows on the Japanese and German "
                           "pages too. Put it in UIStrings in site/src/lib/i18n.ts "
                           "and read it through ui(lang): %s"
                           % (name, n, stripped[:70]))
    return out



def check_tree_labels_are_translated():
    """A tree's editorial label must exist in every language it renders in.

    Found 2026-09-02 by reading a Portuguese page rather than by any scan: the
    card label on /pt/porto said "Ensemble" and /it/naples said "Young
    replacement". The 756-page sweep run an hour earlier missed both, because a
    scan can only find the words somebody thought to look for and nobody had
    thought of these.

    The lookup falls back to English rather than dropping the label, so a new
    one never breaks a page. This is the NOTE that makes the fallback visible,
    because a graceful failure nobody sees is how these last a fortnight.
    """
    out = []
    labels = set()
    for path in sorted(glob.glob(os.path.join("data", "cities", "*.json"))):
        try:
            with open(path, encoding="utf-8") as fh:
                city = json.load(fh)
        except Exception:
            continue
        for t in city.get("trees", []):
            if t.get("label"):
                labels.add(t["label"])
    if not labels:
        return out
    i18n = os.path.join("site", "src", "lib", "i18n.ts")
    if not os.path.exists(i18n):
        return out
    with open(i18n, encoding="utf-8") as fh:
        src = fh.read()
    for label in sorted(labels):
        # every language block should carry the key; count the occurrences of
        # the quoted English label, one per language plus none for en itself.
        n = src.count('"%s":' % label)
        if n < 7:
            out.append("the tree label %r is translated in %d of 7 languages, "
                       "so it renders in English on the rest. Add it to treeLabels "
                       "in site/src/lib/i18n.ts." % (label, n))
    return out

def check_no_two_language_switch():
    """No component may choose between Spanish and English and call that i18n.

    This is the shape of four separate faults found on 2026-09-01 and 09-02, and
    four is not a coincidence. `const T = es ? {...} : {...}` was correct in
    August when Malaga was the only translated city. Six languages landed on
    2026-08-22, a `lang` prop was bolted onto the ternary, and the copy was
    never widened, so six languages took the English branch for a fortnight:
    the sign-in dialog including the sentence about what personal data we hold,
    and the app overlay on every page of the site.

    A `Record<Lang, ...>` cannot fail this way, because a missing language stops
    the build. So the rule is not "translate these strings", it is "never write
    the two-language switch again", and this is where that gets enforced.

    The test looks for the switch itself rather than for untranslated text,
    because untranslated text is the symptom and the ternary is the cause.
    """
    out = []
    for path in sorted(glob.glob(os.path.join("site", "src", "**", "*.astro"),
                                 recursive=True)
                       + glob.glob(os.path.join("site", "src", "**", "*.ts"),
                                   recursive=True)):
        with open(path, encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                stripped = line.strip()
                if stripped.startswith(("//", "*", "/*", "{/*")):
                    continue
                # Any ternary on a variable called `es`, not only one picking
                # between object literals: the AppModal fix first read
                # `es ? COPY.es : COPY.en`, which is the same fault wearing a
                # table. Caught by testing the check against that exact line.
                if re.search(r"\bes\s*\?", line) or \
                   re.search(r'lang\s*===\s*"es"', line) or \
                   re.search(r'\bes:\s*esProp', line):
                    out.append("%s:%d picks between Spanish and English, which is "
                               "not a language choice, it is the 2026-08 Malaga test "
                               "left in place. Use a Record<Lang, ...> table like "
                               "site/src/lib/ui-strings.ts so a missing language "
                               "stops the build: %s"
                               % (os.path.relpath(path), n, stripped[:70]))
    return out

TYPED_TEXT_IS_CODE = re.compile(
    r"^(const|let|var|return|if|for|while|switch|case|else|await|import)\b"
    r"|;\s*$|=>\s*\(?\s*$")


def language_aware_components():
    """The components a reader meets in seven languages, found rather than listed.

    A hardcoded list of four was the first version and it had the flaw the
    whole check exists to close: the NEXT shared component nobody adds to the
    list ships unchecked, which is how the Spanish labels lived for eleven days.
    So the rule is derived from the file: it is language-aware if it is named
    Translated*, calls ui(), or declares a lang prop.

    What this deliberately skips are the components that take their labels as
    PROPS (SaveHeart, WorthIt, ShareButton, Breadcrumbs, LanguagePicker). Those
    carry no text of their own; their caller passes it, and the caller is
    checked here or is a page.
    """
    out = []
    for path in sorted(glob.glob(os.path.join("site", "src", "components", "*.astro"))):
        with open(path, encoding="utf-8") as fh:
            src = fh.read()
        name = os.path.basename(path)
        if (name.startswith("Translated") or "ui(" in src
                or re.search(r"lang\s*[?]?:\s*string", src)):
            out.append((name, src))
    return out


TYPED_TEXT_IS_CODE = re.compile(
    r"^(const|let|var|return|if|for|while|switch|case|else|await|import)\b"
    r"|;\s*$|=>\s*\(?\s*$")


def visible_text(body):
    """What a reader would see: tags, scripts, styles and expressions removed.

    Tags go first and across line breaks, since an attribute list is often
    several lines. Then every {expression}, including one that opens on this
    line and closes on another. Anything still standing was typed.
    """
    body = re.sub(r"<script[\s\S]*?</script>", " ", body, flags=re.I)
    body = re.sub(r"<style[\s\S]*?</style>", " ", body, flags=re.I)
    body = re.sub(r"\{/\*[\s\S]*?\*/\}", " ", body)
    body = re.sub(r"<[^>]*>", " ", body, flags=re.S)
    out = []
    for line in body.split("\n"):
        text, prev = line, None
        while prev != text:
            prev = text
            text = re.sub(r"\{[^{}]*\}", " ", text)
        text = re.sub(r"\{.*$", " ", text)
        text = re.sub(r"^[^{}]*\}", " ", text)
        text = text.strip()
        if not re.search(r"[A-Za-z]{3}", text):
            continue
        if TYPED_TEXT_IS_CODE.search(text):
            continue
        out.append(text)
    return out


def check_translated_components_have_no_typed_text():
    """A word typed into a component that renders in seven languages.

    The general form of the check below, and it exists because that one only
    catches SPANISH. On 2026-09-02 the photo credit under every tree read
    "Foto:" on the Japanese, French and German pages, and "Photo:" on every
    card in all seven, because both labels were typed into the markup. Neither
    carries an accent, so nothing fired.

    Hidde the same day, making it a standing rule rather than a bug report:
    "vanaf nu verwacht ik dat je al je aanpassingen ook verbetert voor alle
    talen, alle paginas en talen moeten consistent blijven." A rule that has to
    be remembered on every edit fails on the edit nobody remembers, so this is
    the check instead.

    A translated component should carry no bare text at all, which is what
    makes this quiet by construction: it finds nothing in any of the six today,
    and names either label the moment one is typed back in.
    """
    out = []
    for name, src in language_aware_components():
        parts = src.split("---", 2)
        body = parts[2] if len(parts) > 2 else src
        for text in visible_text(body):
            if text in ("Ancient Trees",):      # the brand is never translated
                continue
            out.append("%s: %r is typed into a component that renders in seven "
                       "languages, so every reader gets it in English. Add a key "
                       "to UIStrings in site/src/lib/i18n.ts, fill it for every "
                       "language, and read it through ui(lang)." % (name, text[:60]))
    return out


UI_LANGS = ("es", "it", "nl", "de", "pt", "fr", "ja")


def check_ui_strings_cover_every_language():
    """A string added in English only, which seven languages then serve in English.

    ui() is `{...EN, ...TABLE[lang]}` and TABLE is typed Partial<UIStrings>, so
    a key filled for English and forgotten everywhere else compiles, ships, and
    silently reads English on every translated page. Nothing anywhere said so:
    the fallback is deliberate and good for a language we have not added yet,
    and useless as a signal about a language we have.

    All seven cover all sixty keys today, which is what makes this the right
    shape of check: it is silent now and speaks on the first key somebody adds
    to EN alone. Written 2026-09-02 with the check above, when Hidde asked how
    this would be held rather than remembered.
    """
    path = os.path.join("site", "src", "lib", "i18n.ts")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    try:
        iface = src[src.index("interface UIStrings"):src.index("const EN: UIStrings")]
        table = src[src.index("const TABLE"):src.index("export function ui")]
    except ValueError:
        return ["site/src/lib/i18n.ts no longer has the shape this check reads "
                "(interface UIStrings, const EN, const TABLE); update the check "
                "rather than deleting it."]
    keys = set(re.findall(r"^\s{2}([A-Za-z][A-Za-z0-9]*)\s*[?]?:", iface, re.M))
    out = []
    for lang in UI_LANGS:
        marker = "\n  %s: {" % lang
        if marker not in table:
            out.append("site/src/lib/i18n.ts has no block for %r at all, so that "
                       "language reads English throughout." % lang)
            continue
        i = table.index(marker)
        j = table.find("\n  },", i)
        have = set(re.findall(r"^\s{4}([A-Za-z][A-Za-z0-9]*):", table[i:j], re.M))
        missing = sorted(keys - have)
        if missing:
            out.append("site/src/lib/i18n.ts: %s is missing %d of %d strings, so "
                       "readers of that language get English for %s. Fill them in "
                       "its block in TABLE."
                       % (lang, len(missing), len(keys),
                          ", ".join(missing[:5]) + (", ..." if len(missing) > 5 else "")))
    return out


def check_chrome_is_translated():
    """The navigation and footer must read from the string table, not be typed.

    Added 2026-09-02. Until that day we served 663 hand-translated trees inside
    an English frame: /es/seville gave Spanish stories under a nav reading Map,
    Cities, Countries, Species and buttons saying "Suggest a tree" and "Get the
    app". komoot ships its interface in 14 languages and AllTrails in 12, and
    the fix here was one string table (site/src/lib/ui-strings.ts) plus wiring.

    The table's own TypeScript Record guarantees every string exists in all
    eight languages, so the gap this guards is the other one: somebody adding a
    NEW nav or footer link and typing its label straight into Base.astro. That
    compiles, ships, and silently un-translates the chrome for seven languages
    at once, which is exactly how the first version of this problem arrived.

    The test is deliberately narrow, only the anchor and heading text inside
    the nav and footer of Base.astro, because a broader "no English in this
    file" rule would fire on comments, class names and the brand, and a check
    that cries wolf is one everybody learns to skip.
    """
    out = []
    path = os.path.join("site", "src", "layouts", "Base.astro")
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    # <a ...>Some Words</a> and <h4>Some Words</h4>, but not {t.something}
    pat = re.compile(r"<(a|h4|p class=\"nav-group[^\"]*\")\b[^>]*>"
                     r"((?:(?!</?(?:a|h4|p)\b)[\s\S])*?)</(?:a|h4|p)>")
    for m in pat.finditer(src):
        inner = m.group(2)
        text = re.sub(r"<[^>]+>", "", inner).strip()
        if not text or "{t." in inner or "set:html" in inner:
            continue
        if text in ("Ancient Trees",):      # the brand is never translated
            continue
        if not re.search(r"[A-Za-z]{3}", text):
            continue
        out.append("Base.astro: %r is typed into the chrome rather than read "
                   "from site/src/lib/ui-strings.ts, so it stays English on all "
                   "seven translated languages. Add a key to UiStrings, fill it "
                   "for every language, and use {t.yourKey}." % text[:60])
    return out

def check_overlay_coverage():
    """Every translated city must cover every tree its English page holds.

    Added 2026-09-01, after the same failure took the whole site down TWICE in
    one day. A translation overlay lists trees by id, the build refuses to
    render a page whose overlay is short, and because this is a static site
    that refusal kills the entire deploy rather than one page. Munich went
    from 30 trees to 45 in a write pass and its German overlay did not follow;
    Madeira went from 6 to 10 a few hours later and its Portuguese overlay did
    not follow either. Between them they blocked every change from every
    session and night run for most of a day.

    `scripts/i18ncheck.py` already catches this and catches far more, but it
    is a separate command that a write pass has no reason to run, and both
    failures were committed by passes that ran preflight and saw it pass. So
    the cheap half of that check lives here too, where the work actually
    happens: does the overlay have an entry for every tree. Anything subtler
    about a translation, the word counts, the count promises in prose, the
    banned words, stays in i18ncheck.

    Deliberately a FAIL rather than a NOTE: this one does not degrade a page,
    it stops the site shipping.
    """
    out = []
    for path in sorted(glob.glob("data/i18n/*/*.json")):
        lang, name = path.split(os.sep)[-2:]
        slug = name[:-5]
        city_path = os.path.join("data", "cities", name)
        if not os.path.exists(city_path):
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                overlay = json.load(fh)
            with open(city_path, encoding="utf-8") as fh:
                city = json.load(fh)
        except Exception:
            continue
        translated = overlay.get("trees") or {}
        missing = [t["id"] for t in city.get("trees", []) if t["id"] not in translated]
        if missing:
            out.append("%s/%s: the overlay is missing %d of %d trees (%s). A short "
                       "overlay does not degrade one page, it refuses the whole build "
                       "and nothing ships. Translate them or the deploy stays red; "
                       "python3 scripts/i18ncheck.py %s/%s says what else it needs."
                       % (lang, slug, len(missing), len(city.get("trees", [])),
                          ", ".join(missing[:6]) + (", ..." if len(missing) > 6 else ""),
                          lang, slug))
    return out


LEAD_SAME_TREE_RADIUS_M = 60
# The lead says, in its own words, that this is a tree we do not have.
LEAD_CLAIMS_NEW = re.compile(
    r"we do not publish|we don't publish|a tree we do not|never heard|new to us|"
    r"do not have|not (?:yet )?on (?:the|our) (?:site|map|list)|not published", re.I)
# Somebody sent it to us, which is the other way a wrong verdict reaches a person.
LEAD_IS_A_GIFT = re.compile(
    r"photograph sent|photo sent|sent by transfer|submitted by|sent to us|reader submission", re.I)
_LEAD_STOP = {"the", "of", "a", "an", "and", "do", "da", "de", "di", "du", "des", "del",
              "der", "die", "das", "el", "la", "le", "les", "los", "en", "in", "at", "on",
              "no", "na", "dos", "tree", "trees", "walk", "old", "great", "big"}


def _fold(s):
    """Lowercase, strip accents, keep letters and digits. Botanico == Botanico."""
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def _genus(species):
    """The genus out of either 'Bishop Wood (Bischofia javanica)' or 'Bischofia javanica'."""
    s = species or ""
    m = re.search(r"\(([^)]*)\)", s)
    if m:
        s = m.group(1)
    m = re.match(r"([A-Z][a-z]+)", s.strip())
    return m.group(1).lower() if m else ""


def _place_bigrams(text):
    w = [x for x in _fold(text).split() if x not in _LEAD_STOP]
    return {" ".join(w[i:i + 2]) for i in range(len(w) - 1)}


def check_leads_already_published():
    """A lead that is a tree we already publish.

    The fourth appearance of one class, and the first time it cost a
    contributor rather than a run. passcheck.py was written when three briefs
    went out to "open" cities that were already live, and backlog.py exists
    because those were matched by name. Same error, one layer down: on
    2026-09-02 Paulo Araujo's eight photographs of Porto were matched only
    against trees WITHOUT a photograph, so the two of trees that already had
    one were filed as trees we do not publish, and the mail asked him whether
    his Bischofia deserved a place on a page it has been on since July. He
    wrote back with a link to our own list.

    A NOTE, not a FAIL: a leads file is never rendered, so nothing on the site
    is broken by one. What it breaks is the next thing we say to somebody.

    Two ways to match, and never on the name alone. Distance where the lead
    carries a coordinate, because no language can fool it. Where it does not,
    the genus plus a place phrase both texts share, accent-folded, which is
    what "Bischofia / Jardim Botanico" and "Camellia / Casa Tait" both were.

    And it reads only the leads that would COST something, which is the
    difference between a check and a wall of text: matching every lead against
    every published tree prints 374 notes, most of them a lead that was
    promoted to a tree and left in the file, and an alarm that fires 374 times
    is an alarm nobody reads. So: a lead whose own prose says we do not have
    this tree, or one somebody sent us with a photograph. Those are the two
    that end up in a sentence addressed to a person.
    """
    import math
    published = {}
    for path in sorted(glob.glob("data/cities/*.json")):
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        slug = os.path.basename(path)[:-5]
        rows = []
        for t in d.get("trees") or []:
            loc = t.get("location") or {}
            rows.append({
                "id": t.get("id"),
                "name": t.get("name") or "",
                "genus": _genus(t.get("species")),
                "lat": loc.get("latitude"),
                "lon": loc.get("longitude"),
                "words": _place_bigrams((t.get("name") or "") + " " + (loc.get("address") or "")),
            })
        published[slug] = rows

    out = []
    for path in sorted(glob.glob("data/leads/*.json")):
        slug = os.path.basename(path)[:-5]
        rows = published.get(slug)
        if not rows:                      # a city we do not publish, or a country file
            continue
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        for lead in (d.get("leads") or []):
            if not isinstance(lead, dict):
                continue
            text = " ".join(str(v) for v in lead.values() if isinstance(v, str))
            claims_new = LEAD_CLAIMS_NEW.search(text)
            gift = "photo_available" in lead or LEAD_IS_A_GIFT.search(text)
            if not (claims_new or gift):
                continue
            name = lead.get("name") or lead.get("name_pt") or ""
            genus = _genus(lead.get("species"))
            loc = lead.get("location") or {}
            # A leads file is hand-written and `location` is a dict in some and
            # a plain address string in others; both are readable, so read both.
            if not isinstance(loc, dict):
                loc = {"address": str(loc)}
            lat = lead.get("lat", loc.get("latitude"))
            lon = lead.get("lng", loc.get("longitude"))
            hit = None
            if lat is not None and lon is not None:
                for t in rows:
                    if t["lat"] is None or t["lon"] is None:
                        continue
                    dlat = (lat - t["lat"]) * 111320
                    dlon = (lon - t["lon"]) * 111320 * math.cos(math.radians((lat + t["lat"]) / 2))
                    dist = math.hypot(dlat, dlon)
                    if dist <= LEAD_SAME_TREE_RADIUS_M and (not genus or genus == t["genus"]):
                        hit = "%s (%r) stands %.0fm away" % (t["id"], t["name"], dist)
                        break
            if hit is None and genus:
                words = _place_bigrams(name + " " + (loc.get("address") or lead.get("place") or ""))
                for t in rows:
                    if genus != t["genus"]:
                        continue
                    shared = words & t["words"]
                    if shared:
                        hit = "%s (%r) is the same genus at %r" % (
                            t["id"], t["name"], sorted(shared)[0])
                        break
            if hit:
                out.append("%s: lead %r may already be published, %s. "
                           "Check before treating it as a tree we do not have."
                           % (slug, name or lead.get("species") or "?", hit))
    return out


def check_pin_is_in_its_own_country():
    """A pin thousands of kilometres from every other tree in its country.

    Written 2026-09-03, the day a verify pass delivered two New Zealand kauri
    with the minus sign missing from the latitude, which put them in the
    Pacific east of Japan and marked them `confirmed`. It was caught by eye
    before publication, and eyes are not a mechanism.

    The test needs no table of country boxes, which is the point: the trees we
    already publish ARE the box. A dropped sign moves a tree between seven and
    fifteen thousand kilometres, a swapped latitude and longitude moves it
    about as far, and both land far outside any cluster. Ordinary spread does
    not: the widest legitimate gap on the site is well under the threshold,
    and 2,379 trees across 46 countries produced zero hits the day this was
    written.

    Widened to 2000km on 2026-09-04, one day after it shipped: Derby's Boab
    Prison Tree sits 1804km from Pemberton, the nearest other published
    Australian tree, and that is real geography rather than a bug. Its
    coordinates (-17.347862, 123.670163) were checked against Wikipedia's
    infobox (-17.3507, 123.6699, ~300m away) and the WA heritage register's
    own description before raising the threshold; a dropped sign or a
    lat/long swap still moves a tree far past 2000km, so the check keeps its
    whole purpose. Expect this to recur: single-famous-tree destinations
    (rung 0c) are often chosen for standing alone, and Australia, Canada,
    Russia and the US are large enough that a genuine outlier over 800km is
    no longer surprising.

    What it cannot see is a country where we publish one tree, and that is
    exactly the single-famous-tree case rung (0c) creates. It is the cheap
    ninety percent rather than the whole answer, and it fails LOUD, because a
    wrong pin is the one error a reader cannot forgive: they are standing in
    the wrong place before any correction can reach them.
    """
    FAR_KM = 2000
    # Cleared by hand against the tree's own sources: a genuine outlier rather
    # than a bad pin. An id here keeps the threshold tight for everybody else,
    # which is what widening it a second time would have cost.
    CHECKED_BY_HAND = {
        # Pirangi do Norte lies 12km south of Natal on the Rio Grande do Norte
        # coast, 2054km from the nearest other Brazilian tree we publish (Rio
        # de Janeiro). Coordinate checked against the pt/en Wikipedia position
        # for the Cajueiro de Pirangi, 2026-09-04.
        "pir_001",
    }
    by_country = collections.defaultdict(list)
    for path in sorted(glob.glob("data/cities/*.json")):
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
        for t in doc.get("trees", []):
            loc = t.get("location") or {}
            if loc.get("latitude") is None or loc.get("longitude") is None:
                continue
            by_country[doc.get("country")].append(
                (loc["latitude"], loc["longitude"], doc["city"], t.get("name"),
                 t.get("id")))
    out = []
    for country, rows in by_country.items():
        if len(rows) < 2:
            continue
        for i, r in enumerate(rows):
            nearest = min(_haversine(r[0], r[1], s[0], s[1])
                          for j, s in enumerate(rows) if j != i)
            if nearest > FAR_KM and r[4] not in CHECKED_BY_HAND:
                out.append("%s (%s, %s) sits %.0f km from the nearest other "
                           "tree in %s, at %.5f,%.5f. A dropped minus sign or "
                           "a swapped latitude and longitude looks exactly "
                           "like this."
                           % (r[3], r[4], r[2], nearest, country, r[0], r[1]))
    return out


def _haversine(lat1, lon1, lat2, lon2):
    R, p = 6371.0, math.pi / 180
    return 2 * R * math.asin(math.sqrt(
        math.sin((lat2 - lat1) * p / 2) ** 2
        + math.cos(lat1 * p) * math.cos(lat2 * p)
        * math.sin((lon2 - lon1) * p / 2) ** 2))


def check_city_indent():
    """A city file is written with indent=2, the way 337 of 353 were on
    2026-09-04; the other 24 had been rewritten by a script using indent=1.

    A NOTE rather than a FAIL. Two writers with two indents means every touch
    by the other one rewrites the whole file: on 2026-09-03 one commit
    re-indented 21 files without changing a fact and restamped 2,035 sitemap
    URLs as changed that day. Per-page lastmod (scripts/lastmod.py) is immune
    to this now, so the remaining cost is an unreadable diff; the note exists
    so the next one-space writer is caught on its first file.
    """
    out = []
    for p in sorted(glob.glob("data/cities/*.json")):
        with open(p, encoding="utf-8") as fh:
            fh.readline()
            second = fh.readline()
        if second.startswith(" ") and not second.startswith("  "):
            out.append(f"{os.path.basename(p)} is indented with one space; city files use "
                       "indent=2 (a script writing indent=1 rewrites the whole file)")
    return out


def main():
    problems = (check_id_prefixes() + check_pin_upgrades()
                + check_cross_city_duplicates() + check_same_city_duplicates()
                + check_phenology() + check_register_licences()
                + check_access_permission() + check_no_sender_names()
                + check_collection_targets() + check_overlay_coverage()
                + check_chrome_is_translated()
                + check_translated_components_have_no_typed_text()
                + check_ui_strings_cover_every_language()
                + check_translated_components_are_neutral()
                + check_no_two_language_switch()
                + check_pin_is_in_its_own_country()
                + check_contributor_photos_are_traceable())
    files = sorted(glob.glob("data/cities/*.json"))
    for p in files:
        problems += check_city(p)
        with open(p, encoding='utf-8') as fh:
            problems += check_recognise(os.path.basename(p)[:-5], json.load(fh))
        with open(p, encoding='utf-8') as fh2:
            problems += check_contract_b(os.path.basename(p)[:-5], json.load(fh2))
    for line in problems:
        print("FAIL " + line)
    for line in (check_stacked_pins() + check_search_names() + check_paid_share()
                 + check_country_counts() + check_leads_already_published()
                 + check_tree_labels_are_translated() + check_city_indent()):
        print("NOTE " + line)
    print("preflight: %d cities checked, %d problems" % (len(files), len(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
