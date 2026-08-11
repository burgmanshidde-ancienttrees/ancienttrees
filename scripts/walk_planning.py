#!/usr/bin/env python3
"""City data loading and walk planning, extracted from build_site.py when its
rendering code was deleted (2026-08-09, after a clean deploy cycle from the
Astro port: see ARCHITECTURE.md's rollout plan, step 6).

The page-rendering half of build_site.py had no reason to survive the
migration, but this half does: scripts/route_walks.py runs plan_walks() on
every city to work out which walks need a real routed distance cached in
data/walk-routes.json, and that has nothing to do with which generator
renders the pages that walk feeds. Moved verbatim, not rewritten, so its
behaviour (and therefore every existing entry in data/walk-routes.json's
cache keys) stays exactly what it was.

The site/src/lib/walks.ts port is the second, independent implementation of
this same algorithm (necessary, not duplicated for its own sake: Astro's
build needs it in JS, this script needs it in Python to talk to a Python
HTTP client). Changing the algorithm on one side without the other is how
this file and walks.ts drift apart; keep them in step.
"""
import json
import math
import math
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

ERRORS = []


def _fold_name(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def city_aliases():
    """Local spelling -> the English name this site publishes under.

    Shared with scripts/passcheck.py so there is one table rather than two that
    drift. See data/city-aliases.json for why the direction matters."""
    f = DATA / "city-aliases.json"
    if not f.exists():
        return {}
    return json.loads(f.read_text()).get("aliases", {})


def check_city_names(city_list):
    """Refuse to ship a city under its local name when English uses another.

    Every page here is written in English and its readers search in English, so
    the site says Florence and Naples. This shipped wrong twice: the brief
    generator once translated names in the wrong direction (2026-08-06), and the
    same day a city went live as Padova while every other Italian city on the
    site used its English name. Per CLAUDE.md's ratchet, a lesson that lands
    twice becomes a build check rather than a third note. Removing this check
    needs Hidde."""
    alias = city_aliases()
    for entry in city_list:
        d = entry.get("data")
        if not d:
            continue
        for value, field in ((d.get("city", ""), "city name"),
                             (entry.get("slug", ""), "slug")):
            english = alias.get(_fold_name(value))
            if english and _fold_name(english) != _fold_name(value):
                ERRORS.append(
                    f"{entry.get('slug')}: {field} is {value!r}, but this site "
                    f"publishes in English, where it is {english.title()!r}. "
                    f"Rename it and add the old slug to RENAMED_CITY_SLUGS so "
                    f"the live URL keeps resolving, or remove the pair from "
                    f"data/city-aliases.json if English really does use {value!r}.")


def load_cities():
    city_list = json.loads((DATA / "city-list.json").read_text())["cities"]
    for entry in city_list:
        f = DATA / "cities" / f"{entry['slug']}.json"
        entry["data"] = json.loads(f.read_text()) if f.exists() else None
    check_city_names(city_list)
    return city_list


def haversine_km(a, b):
    """Straight line distance between two (lat, lng) points, in kilometres."""
    lat1, lng1 = math.radians(a[0]), math.radians(a[1])
    lat2, lng2 = math.radians(b[0]), math.radians(b[1])
    h = (math.sin((lat2 - lat1) / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin((lng2 - lng1) / 2) ** 2)
    return 2 * 6371.0 * math.asin(math.sqrt(h))


# Streets do not run in straight lines, so the crow-flies total always
# understates a real walk. 1.35 is the usual rule of thumb for dense European
# city centres. The number shown to a visitor is deliberately rounded and
# labelled "about", because promising 3.8 km and delivering 4.6 is the kind of
# small lie that loses trust on a hot afternoon.
DETOUR_FACTOR = 1.35
WALKING_KMH = 4.5


# A real afternoon on foot. Beyond this it stops being a walk and starts being
# a day out, and the honest move is to offer fewer trees rather than a number
# nobody will act on.
WALK_BUDGET_KM = 6.0
WALK_MIN_TREES = 3


def plan_walking_route(points, budget_km=WALK_BUDGET_KM):
    """Find the best walk through a cluster of trees, not through all of them.

    Routing through every tree only works in a compact city. London's ten are
    scattered from Totteridge to Kew: a single path is 69 km, which is not a
    walk and would make the site look like it cannot read its own data. So this
    grows a nearest neighbour path from each possible start and stops when the
    next tree would blow the budget, then keeps whichever attempt gathered the
    most trees (shortest wins a tie).

    Returns None when no honest walk exists, and the page then simply has no
    route bar. Fewer trees is a fine answer; a fake one is not.
    """
    n = len(points)
    if n < WALK_MIN_TREES:
        return None

    best = None
    for start in range(n):
        unvisited = set(range(n))
        unvisited.remove(start)
        order, total, current = [start], 0.0, start
        while unvisited:
            nxt = min(unvisited, key=lambda i: haversine_km(points[current], points[i]))
            step = haversine_km(points[current], points[nxt])
            if (total + step) * DETOUR_FACTOR > budget_km:
                break
            total += step
            order.append(nxt)
            unvisited.remove(nxt)
            current = nxt
        if len(order) < WALK_MIN_TREES:
            continue
        # More trees beats a shorter walk; between equals, take the shorter.
        if best is None or (len(order), -total) > (len(best[0]), -best[1]):
            best = (order, total)

    if best is None:
        return None

    order, total = best
    km = total * DETOUR_FACTOR
    return {
        "order": order,
        "count": len(order),
        "of": n,
        "km": round(km, 1),
        "minutes": int(round(km / WALKING_KMH * 60)),
    }


WALK_CLUSTER_M = 900       # two trees belong to the same walk if this close
WALK_NAME_STOP = {"the", "of", "de", "di", "da", "del", "della", "van", "op",
                  "and", "en", "a", "an", "in", "at", "on"}


def _walk_clusters(points, radius_m=WALK_CLUSTER_M):
    """Single-link clustering: trees joined when one is within radius of another.

    Chosen over k-means or a fixed grid because a walk is a chain, not a blob.
    Porto's seventeen trees run as a 1.6 km ribbon along the hill: any method
    that wants round clusters splits it, and single-link keeps it whole."""
    n = len(points)
    seen, groups = set(), []
    for i in range(n):
        if i in seen:
            continue
        stack, comp = [i], []
        while stack:
            k = stack.pop()
            if k in seen:
                continue
            seen.add(k)
            comp.append(k)
            for j in range(n):
                if j not in seen and haversine_km(points[k], points[j]) * 1000 <= radius_m:
                    stack.append(j)
        groups.append(sorted(comp))
    return groups


WALK_NAME_MAX = 34


def _area_head(area):
    """The place name out of a neighbourhood field.

    Three shapes appear in the data and all three need flattening, or one place
    counts as several and no name ever wins a vote: a trailing clause
    ("Parco Treves de' Bonfili, on Padua's walls"), a parenthetical that varies
    per tree ("Orto Botanico (arboretum section)" beside plain "Orto Botanico"),
    and a compound parish written both long and short ("Lordelo do Ouro e
    Massarelos" beside "Massarelos")."""
    head = str(area or "").split(",")[0]
    head = re.sub(r"\([^)]*\)?", "", head)          # drop parentheticals, even unclosed
    head = re.sub(r"\s+", " ", head).strip(" -/")
    return head


def _walk_name(members, markers):
    """Name a walk after the place most of its trees share.

    Falls back to nothing rather than inventing a name: an unnamed walk still
    says how many trees and how far, which is the part a visitor acts on. The
    place name is used whole, never trimmed to a word count: cutting "Lordelo
    do Ouro e Massarelos" to four words produced "Lordelo do Ouro e"."""
    counts = {}
    for idx in members:
        head = _area_head(markers[idx].get("area"))
        if len(head) >= 3:
            counts[head] = counts.get(head, 0) + 1
    if not counts:
        return ""
    # A compound parish and its short form are one place: fold a name that is
    # contained in a longer one into the longer, then re-vote.
    merged = {}
    for name, n in counts.items():
        parent = next((o for o in counts
                       if o != name and name.lower() in o.lower()), None)
        merged[parent or name] = merged.get(parent or name, 0) + n
    best, hits = max(merged.items(), key=lambda kv: (kv[1], -len(kv[0])))
    # A plurality, with a floor, so one tree never names a walk of eight.
    if hits < 2 or hits * 3 < len(members):
        return ""
    return best if len(best) <= WALK_NAME_MAX else ""


WALK_SPLIT_KM = 3.0      # past this a walk stops being an afternoon and becomes a route
WALK_MAX_OVERLAP = 0.5   # two walks may never be more than half the same trees


def _leg_km(order, points):
    """Walking distance along an ordered route, detour factor included."""
    total = sum(haversine_km(points[order[i]], points[order[i + 1]])
                for i in range(len(order) - 1))
    return total * DETOUR_FACTOR


def _split_route(order, points, depth=0):
    """Cut a long route in half at its midpoint, into two DISJOINT halves.

    Hidde, 2026-08-08, having noticed walks are built as disjoint clusters:
    "you can use the same tree in several walks, does that open options?" It
    opens exactly one worth having. Eighteen cities had a single walk over
    2.5 km, Prague at 6.0 km and 79 minutes, which is a route rather than an
    afternoon. Splitting at the middle gives two real walks.

    The first version let the junction tree belong to both halves. Hidde saw
    the result on Amsterdam the same day and called it: two walks whose lines
    are welded together at the shared tree read as ONE walk on the overview
    map. So the halves are now disjoint, and the way to walk both is the
    explicit "Both walks" choice plan_walks adds when the whole route is
    still a doable afternoon.

    What it deliberately does NOT do is manufacture variety. Sharing trees
    freely would let any city be sliced into four walks that are the same trees
    wearing hats, which is the padding rule applied to walks instead of counts:
    Cadiz has five trees in 600 metres and should have one walk, not four.
    So a split happens only when a route is too long to walk in one go, and
    only while both halves still clear WALK_MIN_TREES."""
    km = _leg_km(order, points)
    if depth >= 2 or km <= WALK_SPLIT_KM or len(order) < WALK_MIN_TREES * 2:
        return [order]
    # cut where the accumulated distance passes halfway
    run, half, cut = 0.0, km / DETOUR_FACTOR / 2, len(order) // 2
    for i in range(len(order) - 1):
        run += haversine_km(points[order[i]], points[order[i + 1]])
        if run >= half:
            cut = i
            break
    cut = max(WALK_MIN_TREES - 1, min(cut, len(order) - WALK_MIN_TREES - 1))
    first, second = order[:cut + 1], order[cut + 1:]   # disjoint: no shared tree
    if len(first) < WALK_MIN_TREES or len(second) < WALK_MIN_TREES:
        return [order]
    return _split_route(first, points, depth + 1) + _split_route(second, points, depth + 1)



def _centroid(order, markers):
    """Mean position of a walk's trees, for telling two same-named walks apart."""
    lats = [markers[i]["lat"] for i in order]
    lngs = [markers[i]["lng"] for i in order]
    return (sum(lats) / len(lats), sum(lngs) / len(lngs))

def _too_similar(a, b):
    """True when two walks are more than half the same trees."""
    sa, sb = set(a), set(b)
    return len(sa & sb) / min(len(sa), len(sb)) > WALK_MAX_OVERLAP


def plan_walks(markers, budget_km=WALK_BUDGET_KM):
    """Every honest walk in a city, not just the best one.

    Hidde, 2026-08-06: a city like Rome should offer a few walks to choose
    from, inside the one page, never as pages of their own. So each cluster
    that holds enough trees gets its own route, and a city with one cluster
    behaves exactly as it always did.

    Returns walks sorted by tree count, longest first, each with its member
    indexes in walking order. Returns [] when no cluster clears the bar, and
    the page then has no route bar at all, which stays the honest answer."""
    points = [(m["lat"], m["lng"]) for m in markers]
    # The chaining radius, with a fallback measured on 2026-08-08. At 900 m,
    # 30 of 91 cities had no walk at all, and 11 of them (London, Venice,
    # Copenhagen, The Hague among them) get their first walk at 1500 m: their
    # trees stand 1.0-1.5 km apart, which is still an afternoon in a big
    # city. But 1500 m globally welds Paris, Vienna, Naples and Nice's named
    # walks into one blob each. So the wider radius applies ONLY to a city
    # that would otherwise have no walk: cities with walks keep them exactly
    # as they are, and a first walk beats no walk.
    groups = _walk_clusters(points)
    if not any(len(g) >= WALK_MIN_TREES for g in groups):
        groups = _walk_clusters(points, radius_m=1500)
    walks, combined = [], []
    for members in groups:
        if len(members) < WALK_MIN_TREES:
            continue
        sub = [points[i] for i in members]
        route = plan_walking_route(sub, budget_km)
        if not route:
            continue
        order = [members[i] for i in route["order"]]
        kept = 0
        for leg in _split_route(order, points):
            if any(_too_similar(leg, w["order"]) for w in walks):
                continue
            kept += 1
            km = round(_leg_km(leg, points), 1)
            walks.append({
                "order": leg,
                "count": len(leg),
                "km": km,
                "minutes": int(round(km / WALKING_KMH * 60)),
                "name": _walk_name(leg, markers),
            })
        # NO COMBINED "BOTH WALKS" OPTION. Removed 2026-08-11.
        #
        # It was added on 2026-08-08 so a visitor with the whole day did not
        # lose the full route when a cluster got split. In practice it was the
        # longest thing on every page and it contradicted the split that had
        # just been made: Porto offered all 18 of its trees over 4.0 km,
        # Barcelona 14 over 3.5, Lisbon 11 over 4.5. Hidde, shown those three:
        # "die te lange lijkt me niet realistisch toch?"
        #
        # And it could never have been realistic, by construction rather than
        # by accident: the chip only appears when a route was split, a route is
        # only split above WALK_SPLIT_KM, so the combined option is ALWAYS
        # longer than the distance we ourselves call too long for an afternoon.
        # Anyone re-adding it should fix that contradiction first.

    # Photographed trees first, then size. Sorting on size alone put Barcelona's
    # worst walk in front: the ten Pedralbes trees are its tightest cluster and
    # also its newest, imported from the municipal register two days before this
    # was written, so not one of them had a photograph while a Montjuic walk with
    # four sat hidden behind a chip. Rome had the same shape. A visitor decides
    # from the pictures whether an afternoon is worth it, so the walk that leads
    # is the one they can see, and every other walk is still one tap away.
    for w in walks:
        w["shots"] = sum(1 for i in w["order"] if markers[i].get("shot"))
    walks.sort(key=lambda w: (-w["shots"], -w["count"], w["km"]))
    # Two walks under one name tells a visitor nothing and quietly implies the
    # second is somewhere else. Vienna produced two "Innere Stadt" walks.
    #
    # Blanking both was the first fix and it was too blunt, because the commonest
    # cause is not coincidence but a split: a route over WALK_SPLIT_KM is cut in
    # half, both halves sit in the same place, so both get that place's name and
    # both then lost it. Barcelona shipped "Walk 2" and "Walk 3" for the two
    # halves of Montjuic, which is a number where a name should be, and you
    # cannot choose between things that have no names.
    #
    # So disambiguate by where they actually are before giving up. Two walks in
    # one place differ along some axis; say which, using the dominant one, and
    # fall back to blanking only when even that cannot separate them.
    by_name = {}
    for w in walks:
        if w["name"]:
            by_name.setdefault(w["name"], []).append(w)
    for name, group in by_name.items():
        if len(group) < 2:
            continue
        cents = [_centroid(w["order"], markers) for w in group]
        lats = [c[0] for c in cents]
        lngs = [c[1] for c in cents]
        spread_ns = max(lats) - min(lats)
        spread_ew = (max(lngs) - min(lngs)) * math.cos(math.radians(sum(lats) / len(lats)))
        mid_lat, mid_lng = sum(lats) / len(lats), sum(lngs) / len(lngs)
        for w, (la, lo) in zip(group, cents):
            if spread_ew >= spread_ns and spread_ew > 0:
                w["name"] = f"{name} {'east' if lo >= mid_lng else 'west'}"
            elif spread_ns > 0:
                w["name"] = f"{name} {'north' if la >= mid_lat else 'south'}"
            else:
                w["name"] = ""
        # If the axis put two walks under the same label anyway, nobody is
        # helped by a wrong distinction: drop back to no name.
        labels = [w["name"] for w in group]
        for w in group:
            if labels.count(w["name"]) > 1:
                w["name"] = ""
    # The combined option rides last, after its parts, never as the lead walk.
    return walks
