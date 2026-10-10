#!/usr/bin/env python3
"""Fill girth_cm and height_m on Dutch trees from the Bomenstichting's own
ArcGIS layer (LRMB_v2024_openbaar), which carries `stamomtrek` (cm) and
`hoogte` (m) where the imported data/registers/netherlands-lrmb.json has
neither. Costs no tokens.

Written 2026-10-10 after the Arnhem enrichment pass found the layer: the
register file we imported has no measurement fields at all, and a pass taking
them tree by tree cost ~150k tokens for eleven trees.

Only fills a field that is empty, only for trees that cite an LRMB number
("entry nr N", "register nr N" or the official_register "no. N"), never for a
row the register carries as status 5 (Dood/geveld), and only with values that
survive a sanity range. The layer URL goes into verified_sources.

    python3 scripts/lrmb_measure.py            # dry run, prints what it would set
    python3 scripts/lrmb_measure.py --apply
"""
import glob
import json
import re
import sys
import urllib.parse
import urllib.request

LAYER = ("https://services-eu1.arcgis.com/qONmLUR87PipcM5W/arcgis/rest/services/"
         "LRMB_v2024_openbaar/FeatureServer/1")
CITE = re.compile(r"(?:entry nr|register nr|\bno\.)\s*(\d{7})")


def cited_nr(t):
    txt = " ".join([str(s) for s in t.get("verified_sources") or []]
                   + [str((t.get("official_register") or {}).get("name") or "")])
    m = CITE.search(txt)
    return int(m.group(1)) if m else None


def fetch(nrs):
    out = {}
    nrs = sorted(nrs)
    for i in range(0, len(nrs), 150):
        chunk = nrs[i:i + 150]
        q = urllib.parse.urlencode({
            "where": "nr in (%s)" % ",".join(map(str, chunk)),
            "outFields": "nr,status,stamomtrek,hoogte",
            "returnGeometry": "false", "f": "json"})
        with urllib.request.urlopen(LAYER + "/query?" + q, timeout=40) as r:
            data = json.load(r)
        for ft in data.get("features", []):
            a = ft["attributes"]
            out[a["nr"]] = a
    return out


def main():
    apply = "--apply" in sys.argv
    files = {}
    wanted = set()
    for p in sorted(glob.glob("data/cities/*.json")):
        d = json.load(open(p, encoding="utf-8"))
        files[p] = d
        for t in d.get("trees", []):
            n = cited_nr(t)
            if n and not (t.get("girth_cm") and t.get("height_m")):
                wanted.add(n)
    rows = fetch(wanted)
    changed = 0
    for p, d in files.items():
        hit = False
        for t in d.get("trees", []):
            n = cited_nr(t)
            r = rows.get(n) if n else None
            if not r or r.get("status") == 5:
                continue
            g, h = r.get("stamomtrek"), r.get("hoogte")
            new = {}
            if g and not t.get("girth_cm") and 30 <= g <= 2000:
                new["girth_cm"] = g
            if h and not t.get("height_m") and 2 <= h <= 60:
                new["height_m"] = h
            if not new:
                continue
            print(p.split("/")[-1][:-5], t["id"], t.get("name"), new)
            changed += 1
            if apply:
                t.update(new)
                src = t.setdefault("verified_sources", [])
                if LAYER not in src:
                    src.append(LAYER)
                hit = True
        if apply and hit:
            with open(p, "w", encoding="utf-8") as fh:
                json.dump(d, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
    print("%d tree(s) %s" % (changed, "updated" if apply else "would be updated"))


if __name__ == "__main__":
    main()
