#!/usr/bin/env python3
"""Give a tree its seasonal peak, where its species already tells us one.

Hidde's paywall copy sells Season Radar as the first premium feature: "get
notified when trees around you hit their peak golden week, blossom, or autumn
foliage". On 2026-08-18 it could fire for 383 of 1,377 trees, so three quarters
of the map would have been sold a notification that never comes. 510 of the
silent ones belong to a species whose phenology file we already wrote. This
fills those in, and only those.

WHAT IT WILL NOT DO, because the value of the badge is entirely in its
scarcity (CLAUDE.md): it never invents a peak. A species moment rated `nice` or
`unseen` earns nothing. `nice` is deliberately the dull default, so a species
nobody has judged yet stays silent rather than gaining a false peak, and if
every deciduous tree claimed one the "at its best right now" badge would be lit
all year and stop being a reason to go anywhere.

Two things it gets right that a naive fill would not:

  * The LATITUDE SHIFT. A stored best_time is read literally by the site
    (bestTimeShort does not shift), while the year calendars are shifted at
    render by phenologyFor(). So the months written here carry the same shift
    that function applies: half a year for the southern hemisphere, one month
    early below 42 degrees, one month late above 56, and nothing at all inside
    25 degrees of the equator, where the temperate pattern is simply wrong and
    a wrong calendar is worse than none.
  * The LABEL says what happens, not just a month, using the species file's own
    words where it has them: "late November, when the whole crown turns butter
    gold" rather than "November".

    python3 scripts/season_backfill.py --dry-run   # report only
    python3 scripts/season_backfill.py             # write
"""
import argparse
import glob
import json
import statistics
import sys

MONTHS = ["", "January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

# Which species moments can earn a badge, strongest first. Anything rated
# `nice` or `unseen` is deliberately absent.
EARNS = ("worth the trip", "striking")

# A moment maps to the kind the site renders as an icon chip. These are the
# only values CLAUDE.md allows.
KIND = {
    "colour": "autumn colour",
    "flowers": "flowers",
    "fruit": "fruit",
    "leaf": "fresh leaves",
    "bare": "bare silhouette",
}

# The order a tie is broken in: a crown of autumn colour beats blossom beats
# fruit, because that is the order of how far people travel for them.
PREFERENCE = ["colour", "flowers", "fruit", "leaf", "bare"]


def shift(months, delta):
    """Same arithmetic as shift() in site/src/lib/phenology.ts."""
    return sorted({((m - 1 + delta) % 12 + 12) % 12 + 1 for m in months})


def centroid_lat(city):
    lats = [t["location"]["latitude"] for t in city.get("trees", [])
            if (t.get("location") or {}).get("latitude") is not None]
    return statistics.median(lats) if lats else None


def species_common(tree):
    return (tree.get("species") or "").split("(")[0].strip()


def peak_for(entry, lat):
    """(months, kind, label_fragment) for the species' strongest moment, or None."""
    intensity = entry.get("intensity") or {}
    best = None
    for key in PREFERENCE:
        rating = intensity.get(key)
        if rating not in EARNS:
            continue
        months = entry.get(key) or []
        if not months or len(months) >= 12:
            continue
        rank = EARNS.index(rating)
        if best is None or rank < best[0]:
            best = (rank, key, months)
    if best is None:
        return None
    _, key, months = best
    away = abs(lat)
    if away < 25:
        return None  # the temperate pattern does not hold here
    delta = (6 if lat < 0 else 0) + (-1 if away < 42 else (1 if away > 56 else 0))
    return shift(months, delta), KIND[key], entry.get(key + "_label")


# What happens, when the species file has no words of its own. Matches
# CLAUDE.md's own example ("May, when it flowers" beats "May").
PLAIN = {
    "autumn colour": "when the leaves turn",
    "flowers": "when it flowers",
    "fruit": "when the fruit ripens",
    "fresh leaves": "when the new leaves come",
    "bare silhouette": "when the bare frame shows",
}


def label_for(months, kind, fragment):
    """A month alone is a weak reason to go, so the label says what happens.

    A colon rather than "when", because the species files write their labels in
    two shapes and only one survives that word: "acorns drop, and a good mast
    year buries the ground in them" is a clause, while "winged seeds that spin
    down in pairs" is a noun phrase, and "September to October, when winged
    seeds that spin down in pairs" is not a sentence. A colon introduces both.
    """
    when = MONTHS[months[0]] if len(months) == 1 else "%s to %s" % (MONTHS[months[0]], MONTHS[months[-1]])
    if fragment:
        frag = fragment[0].lower() + fragment[1:]
        return "%s: %s" % (when, frag)
    return "%s, %s" % (when, PLAIN.get(kind, "when it is at its best"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    pheno = {}
    for f in glob.glob("data/phenology/*.json"):
        with open(f, encoding="utf-8") as fh:
            e = json.load(fh)
        pheno[e["common_name"]] = e

    filled, skipped_nice, skipped_tropics, touched_files = 0, 0, 0, 0
    examples = []

    for path in sorted(glob.glob("data/cities/*.json")):
        with open(path, encoding="utf-8") as fh:
            city = json.load(fh)
        lat = centroid_lat(city)
        if lat is None:
            continue
        changed = False
        for t in city.get("trees", []):
            if t.get("best_time"):
                continue
            entry = pheno.get(species_common(t))
            if not entry:
                continue
            here = (t.get("location") or {}).get("latitude")
            peak = peak_for(entry, here if here is not None else lat)
            if peak is None:
                if abs(here if here is not None else lat) < 25:
                    skipped_tropics += 1
                else:
                    skipped_nice += 1
                continue
            months, kind, fragment = peak
            t["best_time"] = {"months": months, "label": label_for(months, kind, fragment), "kind": kind}
            filled += 1
            changed = True
            if len(examples) < 6:
                examples.append("%s (%s): %s" % (t["name"], city["city"], t["best_time"]["label"]))
        if changed and not args.dry_run:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(city, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
        if changed:
            touched_files += 1

    print("%d tree(s) given a peak across %d cities." % (filled, touched_files))
    print("%d left silent: their species' moments are only 'nice' or 'unseen'." % skipped_nice)
    print("%d left silent: inside 25 degrees of the equator." % skipped_tropics)
    if examples:
        print("\nexamples:")
        for e in examples:
            print("  " + e)
    if args.dry_run:
        print("\n(dry run, nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
