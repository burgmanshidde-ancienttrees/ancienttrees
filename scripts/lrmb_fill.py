#!/usr/bin/env python3
"""Fill the register record, girth and height of Dutch trees from the LIVE LRMB layer.

data/registers/netherlands-lrmb.json lacks the survey fields; the Bomenstichting's own
ArcGIS layer carries `stamomtrek` (girth, cm) and `hoogte` (height, m) per tree. For each
Dutch tree that lacks an official register record or a measurement, ask the layer for
records within MATCH_M metres, keep those whose genus agrees, and take the nearest. A tree
is skipped when two different records of the genus sit within AMBIG_M of each other.
Writes out/enrich/lrmb-bulk.json in enrich.py's answer shape; then:

    python3 scripts/enrich.py --apply out/enrich/lrmb-bulk.json

(the file name carries no city slug, so nothing is dead-ended). Attribution is the layer's
own: Bomenstichting, attribution required. Costs no tokens.
"""
import glob
import json
import math
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAYER = "https://services-eu1.arcgis.com/qONmLUR87PipcM5W/arcgis/rest/services/LRMB_v2024_openbaar/FeatureServer/1/query"
MATCH_M = 40
KEEP_M = 25
AMBIG_M = 8
FIELDS = "nr,sci,soort,status,stamomtrek,hoogte,aantal_bomen,GTYPE,LAT,LON"
NAME = "Landelijk Register Monumentale Bomen (Bomenstichting)"


def dist_m(a, b, c, d):
    r = 6371000
    p1, p2 = math.radians(a), math.radians(c)
    dl = math.radians(d - b)
    x = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(x))


def genus(species):
    m = re.search(r"\(([A-Z][a-z]+)", species or "")
    return m.group(1).lower() if m else None


def query(lat, lng):
    q = {"geometry": f"{lng},{lat}", "geometryType": "esriGeometryPoint", "inSR": 4326,
         "spatialRel": "esriSpatialRelIntersects", "distance": MATCH_M, "units": "esriSRUnit_Meter",
         "outFields": FIELDS, "returnGeometry": "false", "f": "json"}
    url = LAYER + "?" + urllib.parse.urlencode(q)
    for _ in range(2):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ancienttrees-enrich"}), timeout=20) as r:
                return json.load(r).get("features") or []
        except Exception:
            time.sleep(2)
    return None


def main():
    answers = []
    seen = skipped = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        if d.get("country") != "Netherlands":
            continue
        for t in d["trees"]:
            need_reg = not t.get("official_register")
            need_g = not t.get("girth_cm")
            need_h = not t.get("height_m")
            if not (need_reg or need_g or need_h):
                continue
            g = genus(t.get("species"))
            loc = t.get("location") or {}
            if not g or loc.get("latitude") is None:
                skipped += 1
                continue
            feats = query(loc["latitude"], loc["longitude"])
            time.sleep(0.25)
            seen += 1
            if feats is None:
                continue
            cands = []
            for ft in feats:
                a = ft["attributes"]
                if a.get("status") in (4, 5, 6) or genus("(" + str(a.get("sci") or "") + ")") != g:
                    continue
                if a.get("LAT") is None or a.get("GTYPE") not in ("Point", None):
                    continue
                dd = dist_m(loc["latitude"], loc["longitude"], a["LAT"], a["LON"])
                if dd <= KEEP_M:
                    cands.append((dd, a))
            cands.sort(key=lambda c: c[0])
            if not cands:
                continue
            if len(cands) > 1 and cands[1][1]["nr"] != cands[0][1]["nr"] and cands[1][0] - cands[0][0] < AMBIG_M:
                skipped += 1
                continue
            dist, a = cands[0]
            url = LAYER + "?where=nr%3D" + str(a["nr"]) + "&outFields=*&f=json"
            ans = {"id": t["id"]}
            if need_reg:
                ans["register_name"] = NAME
                ans["register_id"] = str(a["nr"])
                ans["add_source"] = url
            single = a.get("aantal_bomen") in (1, None) and a.get("GTYPE") in ("Point", None)
            if single and (a.get("stamomtrek") or 0) > 0 and need_g:
                ans["girth_cm"] = int(a["stamomtrek"])
            if single and (a.get("hoogte") or 0) > 0 and need_h:
                ans["height_m"] = int(a["hoogte"])
            if "girth_cm" in ans or "height_m" in ans:
                ans["measure_source"] = f"LRMB register record nr {a['nr']} (Bomenstichting), {dist:.0f} m from our pin: {url}"
            if len(ans) > 1:
                answers.append(ans)
    out = os.path.join(ROOT, "out", "enrich", "lrmb-bulk.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(answers, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"queried {seen} Dutch trees, skipped {skipped}, {len(answers)} answers -> {out}")
    print("next: python3 scripts/enrich.py --apply out/enrich/lrmb-bulk.json")


if __name__ == "__main__":
    sys.exit(main())
