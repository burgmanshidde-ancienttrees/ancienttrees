#!/usr/bin/env python3
"""Import Castilla y Leon's Arboles Notables into data/registers/.

138 declared notable trees, served as WFS GeoJSON in WGS84 on request, so no
shapefile and no reprojection.

Finding the data took three wrong turns worth recording, because the obvious
route is the broken one. The open-data portal advertises a .shp URL that 404s;
the general IDECyL WFS has no tree layer; and datosabiertos.jcyl.es fails TLS
verification on plain fetches. The working endpoint is only named inside the
GeoNetwork metadata record SPAGOBCYLMNADTSPSANO, which also carries a plainer
licence than the portal's machine-readable field does.

Licence, verbatim from that record:
  "Sin validez juridica, caracter informativo. Uso libre y gratuito. Cita
   obligada a la propiedad de la fuente: 'Junta de Castilla y Leon'."
Free use, attribution obligatory. Note this is SIMPLER than the IGCYL-NC
licence the portal's dataset field points at, which has a commercial branch
obliging us to tell readers the data is free at jcyl.es. Both are satisfied by
attributing the Junta, so this import carries that attribution and the
free-availability sentence, and needs nothing from our pages beyond a credit.

Each tree carries its own designation order and a per-tree page on
medioambiente.jcyl.es, which is a second source a research pass gets for free.

    python3 scripts/import_castilla_leon.py
"""
import json
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "registers" / "castilla-leon-arboles-notables.json"
WFS = "https://idecyl.jcyl.es/geoserver/espaciosnaturales/ows"
LAYER = "espaciosnaturales:en_cyl_znie_arboles_notables_vw"
UA = "Mozilla/5.0 (compatible; AncientTrees/import; https://ancienttrees.app)"


def fetch():
    q = urllib.parse.urlencode({
        "service": "WFS", "version": "2.0.0", "request": "GetFeature",
        "typeNames": LAYER, "outputFormat": "application/json",
        "srsName": "EPSG:4326", "count": 1000,
    })
    req = urllib.request.Request(f"{WFS}?{q}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def clean(v):
    s = str(v).strip() if v is not None else ""
    return "" if s.lower() in ("", "none", "null") else s


def main():
    data = fetch()
    entries = []
    for f in data.get("features", []):
        p = f.get("properties", {})
        g = f.get("geometry") or {}
        if g.get("type") != "Point":
            continue
        lng, lat = g["coordinates"][0], g["coordinates"][1]
        # m_dn_cm is a diameter in centimetres, not a girth. Recorded as what it
        # is, because the ICNF import once read metres as centimetres and turned
        # a 2.84 m trunk into 3 cm.
        try:
            dia = float(p.get("m_dn_cm")) if p.get("m_dn_cm") else None
        except (TypeError, ValueError):
            dia = None
        try:
            hgt = float(p.get("m_altura_m")) if p.get("m_altura_m") else None
        except (TypeError, ValueError):
            hgt = None
        entries.append({
            "register_id": clean(p.get("c_arbolnot")),
            "name": clean(p.get("n_arbolnot")),
            "species": clean(p.get("n_especie")),
            "place": clean(p.get("n_mun")),
            "province": clean(p.get("n_prov")),
            "site": clean(p.get("n_paraje")),
            "latitude": round(lat, 6),
            "longitude": round(lng, 6),
            "diameter_cm": dia,
            "height_m": hgt,
            "designation": clean(p.get("n_figura")),
            "designation_order": clean(p.get("n_norm_reg"))[:180],
            "updated": clean(p.get("f_actualiz"))[:10],
            "url": clean(p.get("url_info")),
        })
    entries.sort(key=lambda e: (e["province"], e["place"], e["name"] or e["register_id"]))
    unnamed = sum(1 for e in entries if not e["name"])
    out = {
        "source": "Junta de Castilla y Leon, Arboles Notables (IDECyL, espaciosnaturales)",
        "endpoint": f"{WFS}?service=WFS&request=GetFeature&typeNames={LAYER}&outputFormat=application/json&srsName=EPSG:4326",
        "licence": "Free use with obligatory attribution (Junta de Castilla y Leon)",
        "licence_proof": (
            "The IDECyL GeoNetwork metadata record SPAGOBCYLMNADTSPSANO states "
            "verbatim: \"Sin validez juridica, caracter informativo. Uso libre y "
            "gratuito. Cita obligada a la propiedad de la fuente: 'Junta de "
            "Castilla y Leon'.\" The portal's separate machine-readable licence "
            "field points at https://www.jcyl.es/licencia-IGCYL-NC, whose name "
            "reads non-commercial and is not: its commercial branch authorises "
            "\"el uso comercial de la cartografia e informacion geografica\" with "
            "attribution as \"(c)Junta de Castilla y Leon\", no distorting "
            "transformation, and a duty to inform end users the material is "
            "available free at jcyl.es. Both are satisfied by attributing the "
            "Junta and stating the data is freely available, which the "
            "attribution field below does."),
        "designation": "Arbol Notable de Castilla y Leon",
        "country": "Spain",
        "attribution": ("Junta de Castilla y Leon, freely available at "
                        "https://idecyl.jcyl.es"),
        "fetched": date.today().isoformat(),
        "publish_dots": True,
        "scope": (
            f"All {len(entries)} declared Arboles Notables. Each carries the "
            f"designation order that created it and a per-tree page on "
            f"medioambiente.jcyl.es, which gives a research pass its second "
            f"source for free. {unnamed} have no proper name and are known only "
            f"by their register code."),
        "caveat": (
            "diameter_cm is a DIAMETER in centimetres, not a girth: multiply by "
            "pi before comparing it with the girth figures every other register "
            "here publishes. No vitality field, so whether a tree still stands "
            "is a per-tree check; the designation orders date from 2006 and the "
            "record was last revised in 2018. These are mostly rural trees in "
            "small municipalities rather than city-centre specimens, so treat "
            "this as a lead pool for day-trip range, not a source of city walks."),
        "entries": entries,
    }
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(entries)} entries -> {OUT.relative_to(ROOT)}")
    print(f"  {unnamed} unnamed (register code only)")
    print(f"  provinces: {len({e['province'] for e in entries})}")


if __name__ == "__main__":
    main()
