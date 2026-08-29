#!/usr/bin/env python3
"""Stop calling a pin approximate when it sits on a named register point.

Measured 2026-08-29 across the whole database: of 713 pins marked
`approximate`, 230 sit within five metres of a row in a register we have
already imported, and 154 of those rows NAME the tree individually. Those pins
are not vague. We took the coordinate out of the register and then labelled it
approximate out of caution, and the cost of that caution is real: the tree page
prints a warning beside the directions button saying we know the park and not
the trunk, when we know the trunk.

CLAUDE.md is blunt about which way this rule cuts. "Precision is optional;
honesty about precision is not. Never mark a pin confirmed to make a city look
finished." This script is the other half of the same sentence: never leave a
pin marked approximate when a source we have already verified places the trunk,
because that is also a false statement about how much we know, and the reader
pays for it by not trusting the pins that really are exact.

    python3 scripts/pin_upgrade.py             # report, writes nothing
    python3 scripts/pin_upgrade.py --write     # apply
    python3 scripts/pin_upgrade.py --source netherlands-lrmb --write

WHAT IT REFUSES, and every guard here exists because a register has already
been caught doing the thing it guards against:

1. The register row must carry its own NAME. A register that names each tree
   is recording an individual; one that does not is usually recording a place.
   This single test is what separates the Dutch national register, which names
   all 124 of its matches, from Italy's national MASAF file, which names none
   of its 46 and whose coordinates this project has already recorded as coarse.
2. The row must not say it holds more than one tree (`n_trees`, `point_count`,
   `units`). A Naturdenkmal is often a group, and a group's point is a place to
   stand rather than a trunk.
3. No second register row within 25 metres. Two candidate trunks that close
   means we cannot say which one the pin is on, which is the Copenhagen
   pacifier-tree error wearing a different hat.
4. Five metres, not thirty. At five metres our pin IS the register's point and
   nothing is being moved; this script never moves a pin, it only stops
   understating what we know about one. Rows between 5 and 120 metres are
   printed under `--far` as work for a person, because moving a pin is a
   decision and this is not the tool for it.

On write it does two things, and the second is not optional: the register's own
catalogue url goes into `verified_sources`, so `check_pin_upgrades()` in
preflight.py can see where the certainty came from. A pin upgraded without
saying why is exactly what that check exists to refuse.

Every change is appended to data/research/pin-upgrades.json with the register
row's id and the measured distance, so any of this can be read back or undone.
"""
import argparse
import glob
import re
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "data", "research", "pin-upgrades.json")

# How to cite a register when its coordinate is what settles the pin. Falls
# back to the file's own `catalogue` or `endpoint` when a source is not listed.
CITATION = {
    "netherlands-lrmb": "https://www.monumentalebomen.nl/",
    "barcelona-ail": "https://opendata-ajuntament.barcelona.cat/data/dataset/7052709e-1087-4ef3-862a-1a6c3e9a7200",
    "bayern-naturdenkmale": "https://www.lfu.bayern.de/natur/schutzgebiete/",
    "brussels-arbres-remarquables": "https://opendata.brussels.be/explore/dataset/bruxelles_arbres_remarquables/",
    "paris-arbres-remarquables": "https://opendata.paris.fr/explore/dataset/arbresremarquablesparis/",
}

NAME_KEYS = ("name", "name_nl", "nom", "nombre", "denominazione")
SPECIES_KEYS = ("species", "especie", "espece", "specie", "soort", "taxon")
ID_KEYS = ("nr", "register_id", "id", "ref", "code")
COUNT_KEYS = ("n_trees", "point_count", "units", "n_ex", "count")

EXACT_M = 5.0
AMBIGUOUS_M = 25.0
FAR_M = 120.0


def num(v):
    try:
        return float(str(v).replace(",", "."))
    except Exception:
        return None


def rows_of(d):
    for k in ("entries", "trees", "rows", "data"):
        if isinstance(d.get(k), list):
            return d[k]
    return d if isinstance(d, list) else []


def first(r, keys):
    for k in keys:
        v = r.get(k)
        if v not in (None, "", [], {}):
            return v
    return None


def genus(s):
    """The Latin genus, from either 'Horse Chestnut (Aesculus hippocastanum)' or
    a bare 'Aesculus hippocastanum'. Returns '' when there is nothing to read."""
    s = str(s or "")
    m = re.search(r"\(([A-Z][a-z]+)[\s)]", s)
    if m:
        return m.group(1).lower()
    m = re.match(r"\s*([A-Z][a-z]{2,})\b", s)
    return m.group(1).lower() if m else ""


def metres(a, b, c, d):
    return math.hypot((a - c) * 111000.0,
                      (b - d) * 111000.0 * math.cos(math.radians(a)))


def load_registers():
    """Every positioned register row, plus how to cite the file it came from."""
    rows, cite = [], {}
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "registers", "*.json"))):
        try:
            doc = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        src = os.path.basename(path)[:-5]
        if isinstance(doc, dict):
            cite[src] = (CITATION.get(src) or doc.get("catalogue")
                         or (doc.get("endpoint") or "").split(" ")[0] or "")
        else:
            cite[src] = CITATION.get(src, "")
        for r in rows_of(doc if isinstance(doc, dict) else {"entries": doc}):
            if not isinstance(r, dict):
                continue
            lat = num(r.get("latitude") or r.get("lat"))
            lng = num(r.get("longitude") or r.get("lng") or r.get("lon"))
            if lat is None or lng is None:
                continue
            rows.append((lat, lng, r, src))
    return rows, cite


def index(rows):
    grid = {}
    for lat, lng, r, src in rows:
        grid.setdefault((round(lat * 20), round(lng * 20)), []).append((lat, lng, r, src))
    return grid


def near(grid, lat, lng, radius):
    out = []
    k, j = round(lat * 20), round(lng * 20)
    for a in (k - 1, k, k + 1):
        for b in (j - 1, j, j + 1):
            for rl, rg, r, src in grid.get((a, b), ()):
                d = metres(lat, lng, rl, rg)
                if d <= radius:
                    out.append((d, r, src))
    out.sort(key=lambda x: x[0])
    return out


def holds_one_tree(r):
    """False when the register itself says this row covers more than one tree."""
    n = first(r, COUNT_KEYS)
    if n is None:
        return True
    v = num(n)
    return v is None or v <= 1


def judge(tree, grid, only_source):
    """(verdict, distance, row, source). verdict is 'upgrade' or a refusal."""
    loc = tree.get("location") or {}
    lat, lng = loc.get("latitude"), loc.get("longitude")
    if lat is None or lng is None:
        return "no position", None, None, None
    hits = near(grid, lat, lng, FAR_M)
    if not hits:
        return "no register row within %d m" % FAR_M, None, None, None
    d, row, src = hits[0]
    if d > EXACT_M:
        return "nearest row is %.0f m away, a person decides" % d, d, row, src
    if only_source and src != only_source:
        return "other source (%s)" % src, d, row, src
    if not first(row, NAME_KEYS):
        return "the register does not name this row (%s)" % src, d, row, src
    if not holds_one_tree(row):
        return "the row covers more than one tree (%s)" % src, d, row, src
    ours, theirs = genus(tree.get("species")), genus(first(row, SPECIES_KEYS))
    if ours and theirs and ours != theirs:
        # Not a matching failure. At this range one of the two records is wrong
        # about which tree it is, and the register is far likelier to be right
        # about its own entry than we are about a pin we copied from it. This is
        # how bcn_043 was found: we call it a horse chestnut on the placa Carles
        # Buigas and sit on the register's araucaria, 250 m from the tipuana
        # that actually stands on that square.
        return "SPECIES CONFLICT: we say %s, the register says %s" % (
            ours, theirs), d, row, src
    close = [h for h in hits if h[0] <= AMBIGUOUS_M]
    if len(close) > 1:
        return "%d register rows within %d m, cannot say which trunk" % (
            len(close), AMBIGUOUS_M), d, row, src
    return "upgrade", d, row, src


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--source", help="only this register file's rows")
    ap.add_argument("--far", action="store_true",
                    help="also list the 5 to 120 m cases, which are a person's job")
    args = ap.parse_args()

    rows, cite = load_registers()
    grid = index(rows)
    print("%d positioned register rows loaded\n" % len(rows))

    upgrades, refusals, far, conflicts = [], {}, [], []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        doc = json.load(open(path, encoding="utf-8"))
        touched = False
        for tree in doc.get("trees") or []:
            if tree.get("location_precision") != "approximate":
                continue
            verdict, d, row, src = judge(tree, grid, args.source)
            if verdict.startswith("SPECIES CONFLICT"):
                conflicts.append((doc["city"], tree["id"], tree.get("name", ""),
                                  tree.get("species", ""), round(d),
                                  str(first(row, NAME_KEYS) or "")[:44],
                                  str(first(row, SPECIES_KEYS) or "")[:28], src))
            if verdict != "upgrade":
                refusals[verdict.split(" (")[0].split(":")[0]] = refusals.get(
                    verdict.split(" (")[0].split(":")[0], 0) + 1
                if args.far and d is not None and EXACT_M < d <= FAR_M:
                    far.append((doc["city"], tree["id"], tree.get("name", ""), round(d),
                                str(first(row, NAME_KEYS) or "")[:40], src))
                continue
            rid = first(row, ID_KEYS)
            entry = {"city": doc["city"], "id": tree["id"], "tree": tree.get("name"),
                     "register": src, "register_id": rid,
                     "register_name": first(row, NAME_KEYS), "metres": round(d, 1)}
            upgrades.append(entry)
            if args.write:
                tree["location_precision"] = "confirmed"
                url = cite.get(src) or ""
                srcs = tree.setdefault("verified_sources", [])
                if url and url not in srcs:
                    srcs.append(url)
                touched = True
        if touched and args.write:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(doc, fh, ensure_ascii=False, indent=2)
                fh.write("\n")

    by_src = {}
    for u in upgrades:
        by_src[u["register"]] = by_src.get(u["register"], 0) + 1
    print("%d pin(s) would be upgraded from approximate to confirmed"
          % len(upgrades) if not args.write else
          "%d pin(s) upgraded from approximate to confirmed" % len(upgrades))
    for s, n in sorted(by_src.items(), key=lambda x: -x[1]):
        print("  %5d  %s" % (n, s))
    print("\nrefused:")
    for k, n in sorted(refusals.items(), key=lambda x: -x[1]):
        print("  %5d  %s" % (n, k))
    if conflicts:
        print("\nSPECIES CONFLICTS. Our pin sits on a register row for a different "
              "genus. One of the two records is wrong about which tree this is, and "
              "it is usually ours, because the coordinate came from that register. "
              "Each of these needs a person; none was upgraded.")
        for c, i, n, sp, d, rn, rs, s_ in conflicts:
            print("  %-14s %-9s %-30s %-26s %3d m  %-44s %s" % (c[:14], i, n[:30], sp[:26], d, rn, rs))
    if far:
        print("\n5 to 120 m: the register names a trunk somewhere else. A person "
              "decides whether to move the pin; this script never does.")
        for c, i, n, d, rn, s in sorted(far, key=lambda r: r[3])[:40]:
            print("  %-16s %-9s %-34s %4d m  %-40s %s" % (c[:16], i, n[:34], d, rn, s))

    if args.write and upgrades:
        old = []
        if os.path.exists(LEDGER):
            try:
                old = json.load(open(LEDGER, encoding="utf-8")).get("upgrades") or []
            except Exception:
                old = []
        with open(LEDGER, "w", encoding="utf-8") as fh:
            json.dump({"note": "Pins moved from approximate to confirmed because a "
                               "named register row sits within 5 m. Written by "
                               "scripts/pin_upgrade.py. Kept so any of this can be "
                               "read back or undone.",
                       "upgrades": old + upgrades}, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        print("\nledger: %s (%d total)" % (LEDGER, len(old) + len(upgrades)))
    elif not args.write:
        print("\n(report only; pass --write to apply)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
