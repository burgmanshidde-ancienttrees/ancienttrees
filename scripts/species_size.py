#!/usr/bin/env python3
"""How big is big, per species, measured against everything we know.

Hidde, 2026-09-23, on a ranking that compared a tree only against the 60 in
the mail it arrived in: "je moet inderdaad niet meten binnen deze lijst van 60
maar binnen wat er bekend is in de hele database over de soort."

He is right, and it is the difference between a measurement and an accident of
sampling. A snake spruce of 1,22 m looked like the biggest of its species
because it was the ONLY one in the sample. Against every girth this project
holds it is an ordinary tree.

WHY THIS EXISTS AT ALL. "Worth the visit" needs a test that a register row can
answer, and the honest one is size FOR ITS SPECIES, never absolute girth: a
Turkish hazel of 2,10 m is close to the biggest in Denmark, an oak of 4,62 m is
a park oak. Absolute girth picks the wrong one of those two every time.

WHAT IT READS. Every girth this project has written down, which is more than
anybody guessed: published trees (girth_cm), imported registers (girth_cm,
trunk_girth), and leads. All in centimetres, checked: the ICNF lesson about
metres in a column named cm is the reason this prints its own ranges.

THE REFERENCE. Per species, and per genus as a fallback for a lead that only
reaches the genus (the publish-and-ask rule of 2026-08-13 means we carry plenty
of "Quercus sp."):
  max   the biggest we know of
  p90   the 90th percentile, which is the number to score against once the
        species has ten records. One mistyped row can set a max; it cannot
        move a p90. Below ten records the reference is the max and the count
        says so, because a reference resting on three trees is a guess with
        arithmetic on top.

Usage:
  python3 scripts/species_size.py                      # rebuild data/species-size.json
  python3 scripts/species_size.py --rel "Zelkova serrata" 755
  python3 scripts/species_size.py --top 20             # best-known species
"""
import glob
import json
import os
import re
import sys

OUT = "data/species-size.json"
CUT = re.compile(r"\b(subsp|ssp|var|f|cv|x)\.?\b", re.I)


def binomial(name):
    """'Olea europaea subsp. oleaster (Hoffmanns)' -> ('Olea europaea', 'Olea')."""
    if not name:
        return None, None
    s = str(name)
    s = re.sub(r"[`'‘’\"].*?[`'‘’\"]", " ", s)   # cultivars
    s = re.sub(r"\(.*?\)", " ", s)                                    # authorities in brackets
    s = s.replace("×", " ").replace(" x ", " ")
    parts = [p for p in re.split(r"[\s,]+", s) if p]
    out = []
    for p in parts:
        if CUT.fullmatch(p.rstrip(".")):
            break
        if not re.fullmatch(r"[A-Za-z-]+", p):
            break
        if out and p[0].isupper():          # a second capital is an author, not an epithet
            break
        out.append(p)
        if len(out) == 2:
            break
    if not out or not out[0][0].isupper():
        return None, None
    genus = out[0]
    return (" ".join(out) if len(out) == 2 else None), genus


def latin_from_our_species(s):
    """'European Yew (Taxus baccata)' -> 'Taxus baccata'."""
    m = re.search(r"\(([^)]+)\)", s or "")
    return m.group(1) if m else s


def cm(v):
    try:
        f = float(re.sub(r"[^\d.,]", "", str(v)).replace(",", "."))
    except (TypeError, ValueError):
        return None
    return f if 20 <= f <= 5000 else None


def collect_ages():
    """Ages, which we have MORE of than girths: 77 percent of published trees
    carry one against 47 percent with a measurement.

    Age is a second axis rather than the same one twice. Across species the two
    are not interchangeable at all, because growth rate varies fourteenfold in
    our own data, from 60 cm of girth per century for an olive or a yew to 836
    for an ombu. Within a species they mostly agree, and where they disagree
    the girth is the one that lies: a holm oak of a thousand years at 200 cm,
    an 800 year yew at 292, a Scots pine of five centuries at 188. Every one of
    those is under-ranked by thickness alone.

    So the two are combined by taking the BETTER of the two, never by adding
    them. Adding would count one fact twice for the ordinary tree, where the
    age was calculated from the girth in the first place.
    """
    recs = []
    for f in glob.glob("data/cities/*.json"):
        for t in json.load(open(f)).get("trees", []):
            a = t.get("age_max") or t.get("age_min")
            try:
                a = float(a)
            except (TypeError, ValueError):
                continue
            if 10 <= a <= 6000:
                recs.append((a, latin_from_our_species(t.get("species")), "published"))
    return recs


def collect():
    recs = []                                    # (cm, latin, source)
    for f in glob.glob("data/cities/*.json"):
        for t in json.load(open(f)).get("trees", []):
            g = cm(t.get("girth_cm"))
            if g:
                recs.append((g, latin_from_our_species(t.get("species")), "published"))
    for f in glob.glob("data/registers/*.json"):
        try:
            d = json.load(open(f))
        except (ValueError, OSError):
            continue
        rows = d.get("trees") or d.get("rows") or (d if isinstance(d, list) else [])
        if not isinstance(rows, list):
            continue
        src = os.path.basename(f)
        for r in rows:
            if not isinstance(r, dict):
                continue
            g = cm(r.get("girth_cm") or r.get("trunk_girth"))
            if not g:
                continue
            lat = r.get("latin") or r.get("species_latin") or r.get("species") or r.get("specie")
            recs.append((g, lat, src))
    for f in glob.glob("data/leads/*.json"):
        try:
            d = json.load(open(f))
        except (ValueError, OSError):
            continue
        rows = d.get("leads") if isinstance(d, dict) else d
        if not isinstance(rows, list):
            continue
        for r in rows:
            if not isinstance(r, dict):
                continue
            g = cm(r.get("girth_cm") or r.get("girth"))
            if g:
                recs.append((g, latin_from_our_species(r.get("species")), "leads"))
    return recs


def pct(vals, p):
    vals = sorted(vals)
    if not vals:
        return None
    i = min(len(vals) - 1, int(round((p / 100) * (len(vals) - 1))))
    return vals[i]


def bucket(recs):
    species, genera = {}, {}
    for g, lat, src in recs:
        b, gen = binomial(lat)
        if b:
            species.setdefault(b, []).append(g)
        if gen:
            genera.setdefault(gen, []).append(g)
    return species, genera


def build():
    recs = collect()
    species, genera = bucket(recs)
    arecs = collect_ages()
    aspecies, agenera = bucket(arecs)

    def summarise(d):
        out = {}
        for k, v in d.items():
            out[k] = {
                "n": len(v),
                "max": max(v),
                "p90": pct(v, 90),
                "reference": pct(v, 90) if len(v) >= 10 else max(v),
                "thin": len(v) < 10,
            }
        return out

    doc = {
        "built_from": {"records": len(recs), "species": len(species), "genera": len(genera),
                       "age_records": len(arecs), "age_species": len(aspecies)},
        "species": summarise(species),
        "genera": summarise(genera),
        "age_species": summarise(aspecies),
        "age_genera": summarise(agenera),
    }
    json.dump(doc, open(OUT, "w"), ensure_ascii=False, indent=1, sort_keys=True)
    print(f"{len(recs)} girth records -> {len(species)} species, {len(genera)} genera")
    print(f"{len(arecs)} age records   -> {len(aspecies)} species, {len(agenera)} genera")
    print(f"written to {OUT}")
    return doc


def load():
    return json.load(open(OUT))


def _rel(doc, skey, gkey, name, value, unit):
    b, gen = binomial(name)
    row = doc[skey].get(b or "") or doc[gkey].get(gen or "")
    level = "species" if (b and b in doc[skey]) else ("genus" if gen in doc[gkey] else None)
    if not row or not value:
        return None, f"nothing known about {name}"
    r = float(value) / row["reference"]
    note = f"{r:.0%} of the {level} reference ({row['reference']:.0f} {unit}, n={row['n']}, max {row['max']:.0f})"
    if row["thin"]:
        note += "  THIN: fewer than ten records, treat as a hint"
    return r, note


def rel(name, girth_cm):
    return _rel(load(), "species", "genera", name, girth_cm, "cm")


def rel_age(name, years):
    return _rel(load(), "age_species", "age_genera", name, years, "yr")


def remarkable(name, girth_cm=None, years=None):
    """The better of the two, never the sum. Returns (score, which, note)."""
    doc = load()
    g, gn = _rel(doc, "species", "genera", name, girth_cm, "cm") if girth_cm else (None, None)
    a, an = _rel(doc, "age_species", "age_genera", name, years, "yr") if years else (None, None)
    if g is None and a is None:
        return None, None, f"nothing measurable about {name}"
    if a is None or (g is not None and g >= a):
        return g, "girth", gn
    return a, "age", an


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        build()
    elif a[0] == "--rel":
        r, note = rel(a[1], a[2])
        print(f"{a[1]} at {a[2]} cm: {note}")
    elif a[0] == "--age":
        r, note = rel_age(a[1], a[2])
        print(f"{a[1]} at {a[2]} yr: {note}")
    elif a[0] == "--top":
        doc = load()
        rows = sorted(doc["species"].items(), key=lambda kv: -kv[1]["n"])[: int(a[1]) if len(a) > 1 else 20]
        print(f"{'species':34s} {'n':>5} {'p90':>7} {'max':>7}")
        for k, v in rows:
            print(f"{k:34s} {v['n']:5d} {v['p90']:7.0f} {v['max']:7.0f}")
