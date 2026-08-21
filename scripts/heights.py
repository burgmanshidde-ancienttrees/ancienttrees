#!/usr/bin/env python3
"""Fill height_m on published trees from the registers we have already imported.

Hidde asked for a tallest-trees ranking (2026-08-21). We had no height field at
all: 862 stories MENTION a height, but pulling a number out of prose is how you
end up publishing the species' maximum, or the neighbour's, or the height a tree
had before a cyclone took the top off it. The registers carry the measurement
per tree, with a coordinate, which is a different kind of number.

The match is deliberately narrow. A register row must be within 5 metres of our
pin, or within 30 metres AND agree on the genus, before its height is copied.
Most of our register-backed trees sit at exactly the imported coordinate, so the
strict rule costs almost nothing and refuses the ambiguous cases outright.

    python3 scripts/heights.py            # match and write
    python3 scripts/heights.py --report   # say what would happen, write nothing

Re-runnable: a tree that already carries a height is left alone, so a hand-read
measurement from a plaque always beats a register match.
"""
import glob
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def num(v):
    try:
        f = float(str(v).replace(",", "."))
        return f if f > 0 else None
    except Exception:
        return None


def rows_of(d):
    for k in ("trees", "entries", "rows", "data"):
        if isinstance(d.get(k), list):
            return d[k]
    return d if isinstance(d, list) else []


def genus(s):
    return (str(s or "").strip().split() or [""])[0].lower().strip("(),")


def load_registers():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "registers", "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for r in rows_of(d):
            if not isinstance(r, dict):
                continue
            lat = num(r.get("latitude") or r.get("lat"))
            lng = num(r.get("longitude") or r.get("lng") or r.get("lon"))
            h = num(r.get("height_m"))
            if h is None:
                ft = num(r.get("height_ft"))
                h = round(ft * 0.3048, 1) if ft else None
            # A tree under 3 m is a shrub or a typo; over 120 m is not on
            # this planet outside California, and no register of ours holds one.
            if lat and lng and h and 3 <= h <= 120:
                out.append((lat, lng, h, genus(r.get("species") or r.get("especie") or ""),
                            os.path.basename(f)))
    return out


def metres(a, b, c, d):
    return math.hypot((a - c) * 111000.0,
                      (b - d) * 111000.0 * math.cos(math.radians(a)))


def main():
    report = "--report" in sys.argv
    reg = load_registers()
    print("%d register rows carry a height and a coordinate" % len(reg))

    filled = skipped = already = 0
    per_source = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        doc = json.load(open(path, encoding="utf-8"))
        touched = False
        for t in doc["trees"]:
            if t.get("height_m"):
                already += 1
                continue
            loc = t.get("location") or {}
            la, ln = loc.get("latitude"), loc.get("longitude")
            if not la or not ln:
                continue
            g = genus(t.get("species"))
            best = None
            for rla, rln, h, rg, src in reg:
                if abs(rla - la) > 0.001 or abs(rln - ln) > 0.001:
                    continue
                d = metres(la, ln, rla, rln)
                if d > 30:
                    continue
                if d > 5 and rg and g and rg != g:
                    skipped += 1
                    continue
                if best is None or d < best[0]:
                    best = (d, h, src)
            if best:
                filled += 1
                per_source[best[2]] = per_source.get(best[2], 0) + 1
                if not report:
                    t["height_m"] = best[1]
                    note = ("Height %s m from the %s register, matched on our own pin "
                            "(%d m away)." % (best[1], best[2].replace(".json", ""), round(best[0])))
                    t["verify_notes"] = ((t.get("verify_notes") + " ") if t.get("verify_notes") else "") + note
                    touched = True
        if touched and not report:
            json.dump(doc, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
            open(path, "a", encoding="utf-8").write("\n")

    print("%d trees %s a height, %d already had one, %d refused on genus"
          % (filled, "would get" if report else "got", already, skipped))
    for s, n in sorted(per_source.items(), key=lambda x: -x[1])[:8]:
        print("   %4d  %s" % (n, s))
    return 0


if __name__ == "__main__":
    sys.exit(main())
