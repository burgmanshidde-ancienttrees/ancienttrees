#!/usr/bin/env python3
"""Fill girth_cm on published trees from the registers we have already imported.

The sibling of heights.py, and the more useful of the two. CLAUDE.md calls
girth "the cheap unlock": it is the one measurement from which an age can be
DERIVED rather than invented, because girth plus a published growth rate for
the species is how every register in the world dates a tree. 236 published
trees carry no age at all, and an estimate is unavailable for almost every one
of them because nobody wrote down a girth. It also feeds /collections/thickest-
trees, which re-ranks itself on every build.

    python3 scripts/girths.py            # match and write
    python3 scripts/girths.py --report   # say what would happen, write nothing

Re-runnable: a tree that already carries a girth is left alone, so a figure
read off a plaque or a source always beats a register match.

THE MATCH is heights.py's, deliberately: within 5 metres of our pin, or within
30 metres AND the genus agrees. Most register-backed trees sit at exactly the
imported coordinate, so the strict rule costs almost nothing and refuses the
ambiguous cases outright.

THE UNITS are the hard part, and this is where a register will quietly lie to
you. Ten different column names across 21 files carry this measurement, in
centimetres, metres, feet and inches, as girth and as diameter, and the column
name cannot be trusted: CLAUDE.md records ICNF publishing metres in a column
our own import had labelled girth_cm, so a 2.84 metre trunk read as under three
centimetres and nobody noticed for days. So every value is converted by its
column AND then checked against the physical world, and anything landing
outside 40 to 4600 cm is thrown away rather than published.

That single check is what catches Melbourne, whose `girth_m` column has a
median of 91 and a maximum of 235. Read as metres that is a trunk 29 metres
across. It is almost certainly a diameter in centimetres, and because it is
"almost certainly" rather than "certainly" the right answer is to publish none
of it.

Only measured girths and circumferences are read. Diameter columns are refused
outright: see the note beside COLUMNS for the banyan that made the case.
"""
import glob
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "data", "research", "girths-from-registers.json")

# (column, multiplier to centimetres), in order of preference: a column that
# says girth beats one that says circumference, because the second is more
# often a survey figure somebody rounded.
COLUMNS = [
    ("girth_cm", 1.0),
    ("circumference_cm", 1.0),
    ("trunk_girth", 1.0),
    ("girth_m", 100.0),
    ("girth", 100.0),
    ("circumference_ft", 30.48),
]
# The diameter columns are deliberately NOT here. Across the whole database
# they produced exactly one match that a direct girth column had not already
# covered, and that one was wrong: Hilo's Rainbow Falls banyan came out at 92 cm
# round, which is a sapling, because a banyan's "diameter" in that register is
# one stem of a tree that has dozens. A conversion whose entire yield is a
# single bad number is not worth keeping, and pi has a way of making a wrong
# figure look computed.
# A trunk under 40 cm round is a sapling and not what any of these registers
# protects; over 4600 cm is beyond the widest single trunk on earth, and the
# few real values near that ceiling are banyan complexes measured around their
# aerial roots. Anything outside the band is a unit error, not a tree.
MIN_CM, MAX_CM = 40.0, 4600.0


def num(v):
    """A number out of a register cell, which is as often '3,3 m' as 3.3."""
    if v is None:
        return None
    s = str(v).strip().lower().replace(",", ".")
    keep = []
    for ch in s:
        if ch.isdigit() or ch == ".":
            keep.append(ch)
        elif keep:
            break
    try:
        f = float("".join(keep))
    except ValueError:
        return None
    return f if f > 0 else None


def unit_in_text(v):
    """cm or m written into the cell itself always beats the column name."""
    s = str(v or "").lower()
    if "cm" in s:
        return 1.0
    if s.rstrip().endswith("m") or " m" in s:
        return 100.0
    return None


def rows_of(d):
    for k in ("entries", "trees", "rows", "data"):
        if isinstance(d.get(k), list):
            return d[k]
    return d if isinstance(d, list) else []


def genus(s):
    s = str(s or "")
    if "(" in s:
        s = s.split("(", 1)[1]
    return (s.strip().split() or [""])[0].lower().strip("(),")


def girth_of(row):
    """(centimetres, which column) or (None, None)."""
    for col, mult in COLUMNS:
        raw = row.get(col)
        if raw in (None, "", [], {}):
            continue
        v = num(raw)
        if v is None:
            continue
        m = unit_in_text(raw) or mult
        cm = v * m
        if MIN_CM <= cm <= MAX_CM:
            return round(cm), col
    return None, None


def metres(a, b, c, d):
    return math.hypot((a - c) * 111000.0,
                      (b - d) * 111000.0 * math.cos(math.radians(a)))


def load_registers():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "registers", "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for r in rows_of(d if isinstance(d, dict) else {"entries": d}):
            if not isinstance(r, dict):
                continue
            lat, lng = num(r.get("latitude") or r.get("lat")), num(r.get("longitude") or r.get("lng"))
            if lat is None or lng is None:
                continue
            # longitude west of Greenwich survives num()'s sign-stripping only
            # because we re-read it here rather than trusting the parse.
            try:
                lat = float(str(r.get("latitude") or r.get("lat")).replace(",", "."))
                lng = float(str(r.get("longitude") or r.get("lng")).replace(",", "."))
            except Exception:
                continue
            cm, col = girth_of(r)
            if cm is None:
                continue
            out.append((lat, lng, cm, col, genus(r.get("species") or r.get("especie") or ""),
                        os.path.basename(f)))
    return out


def main():
    report = "--report" in sys.argv
    reg = load_registers()
    print("%d register rows carry a usable girth and a coordinate" % len(reg))

    filled = skipped = already = 0
    per_source, per_col, ledger = {}, {}, []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        doc = json.load(open(path, encoding="utf-8"))
        touched = False
        for t in doc.get("trees") or []:
            if t.get("girth_cm"):
                already += 1
                continue
            loc = t.get("location") or {}
            la, ln = loc.get("latitude"), loc.get("longitude")
            if not la or not ln:
                continue
            g = genus(t.get("species"))
            best = None
            for rla, rln, cm, col, rg, src in reg:
                if abs(rla - la) > 0.001 or abs(rln - ln) > 0.001:
                    continue
                d = metres(la, ln, rla, rln)
                if d > 30:
                    continue
                if d > 5 and rg and g and rg != g:
                    skipped += 1
                    continue
                if best is None or d < best[0]:
                    best = (d, cm, col, src)
            if best:
                filled += 1
                per_source[best[3]] = per_source.get(best[3], 0) + 1
                per_col[best[2]] = per_col.get(best[2], 0) + 1
                ledger.append({"city": doc["city"], "id": t["id"], "tree": t.get("name"),
                               "girth_cm": best[1], "column": best[2],
                               "register": best[3], "metres": round(best[0], 1)})
                if not report:
                    t["girth_cm"] = best[1]
                    touched = True
        if touched and not report:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(doc, fh, ensure_ascii=False, indent=2)
                fh.write("\n")

    print("%d tree(s) %s a girth, %d already had one, %d refused on genus"
          % (filled, "would get" if report else "got", already, skipped))
    for s, n in sorted(per_source.items(), key=lambda x: -x[1]):
        print("  %5d  %s" % (n, s))
    print("read from columns: " + ", ".join("%s x%d" % (c, n)
          for c, n in sorted(per_col.items(), key=lambda x: -x[1])))
    if ledger and not report:
        with open(LEDGER, "w", encoding="utf-8") as fh:
            json.dump({"note": "girth_cm copied onto published trees from an imported "
                               "register, by scripts/girths.py. Kept so the provenance "
                               "of a measurement is not lost the moment it is written.",
                       "filled": ledger}, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        print("ledger: %s" % LEDGER)
    if report:
        print("(report only; run without --report to write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
