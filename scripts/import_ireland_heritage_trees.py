"""Import the public-site subset of Heritage Trees of Ireland into
data/registers/ireland-heritage-trees.json.

Source: maps.biodiversityireland.ie/Dataset/27 (Aubrey Fennell / Tree
Council of Ireland, via the National Biodiversity Data Centre), CC BY 4.0.
724 records total, most NOT extracted here: per hard rule 10, only sites
already known to be genuinely public are included (see PUBLIC_SITES).
Adding a new site to that dict needs an actual access check first, not just
a plausible-looking name; the dataset's own 'Access' field is identical
boilerplate on every row and is not a usable per-tree signal.

Coordinates arrive in Irish Grid (East/North) and are converted with
scripts/irish_grid.py; see that module's docstring for the accuracy caveat.
Re-run this whenever a new PUBLIC_SITES entry is added.
"""
import csv
import io
import json
import os
import sys
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from scripts.irish_grid import irish_grid_to_latlon  # noqa: E402

DATASET_URL = "https://maps.biodiversityireland.ie/Dataset/Download?datasetId=27"

PUBLIC_SITES = {
    "Trinity College, Dublin": "Trinity College campus, publicly accessible",
    "National Botanic Gardens, Dublin": "National Botanic Gardens, Glasnevin, free entry, open daily",
    "St Anne's Park, Dublin": "St Anne's Park, Raheny/Clontarf, public park",
    "Marley Park, Dublin": "Marley Park, Rathfarnham, public park run by South Dublin County Council",
}


def fetch_rows():
    req = urllib.request.Request(DATASET_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        blob = resp.read()
    z = zipfile.ZipFile(io.BytesIO(blob))
    with z.open("HeritageTreesOfIreland.txt") as f:
        text = f.read().decode("utf-8", errors="replace")
    return list(csv.DictReader(io.StringIO(text), delimiter="\t"))


def build():
    rows = fetch_rows()
    entries = []
    for r in rows:
        site = r.get("SiteName", "").strip()
        if site not in PUBLIC_SITES:
            continue
        try:
            e, n = float(r["East"]), float(r["North"])
        except (ValueError, KeyError):
            continue
        lat, lon = irish_grid_to_latlon(e, n)
        entries.append({
            "record_key": r.get("RecordKey"),
            "species": r.get("TaxonName"),
            "latitude": lat,
            "longitude": lon,
            "place": site,
            "age_band": r.get("Age Range") or None,
            "heritage_type": r.get("Heritage Type") or None,
            "category": r.get("Category of Tree") or None,
            "tree_form": r.get("Tree form") or None,
            "condition": r.get("Condition of tree") or None,
            "recorded_date": r.get("Date") or None,
            "recorder": r.get("Recorder") or None,
        })

    out = {
        "source": "Heritage Trees of Ireland (Aubrey Fennell / Tree Council of Ireland), via National Biodiversity Data Centre Biodiversity Maps",
        "endpoint": DATASET_URL + " (Dataset 27, Darwin Core Archive)",
        "licence": "CC BY 4.0",
        "licence_proof": "Stated directly on the dataset's Biodiversity Maps page (maps.biodiversityireland.ie/Dataset/27) as CC BY 4.0.",
        "country": "Ireland",
        "fetched": "2026-08-08",
        "publish_dots": False,
        "scope": (
            "SUBSET ONLY: 724 total records in the source file, most sites "
            "unfiltered. This file holds only the sites already confirmed "
            "genuinely public (Trinity College, National Botanic Gardens "
            "Glasnevin, St Anne's Park, Marley Park), per hard rule 10. The "
            "remaining ~700 records (private houses, hotels, Garda HQ, RTE "
            "studios, streets, other counties) are NOT extracted here and "
            "need a real per-site access read before any future pass "
            "touches them; do not bulk-import the rest without doing that."
        ),
        "caveat": (
            "Coordinates converted from Irish Grid (East/North, OSI/TM75) "
            "via scripts/irish_grid.py, an inverse transverse Mercator "
            "implementation with no Helmert datum shift applied (no "
            "reprojection library available in this environment). Verified "
            "against three register entries that independently matched "
            "already-published, confirmed-pin trees to within 40m (Kings "
            "Inns plane = dub_001 Hungry Tree; two Trinity New Square planes "
            "= dub_006). Treat every coordinate here as approximate on that "
            "basis, on top of the register's own stated 100m precision. Age "
            "Range is the source field name (e.g. '100 - 150 years'), a "
            "band as of the 2009 survey date, not current age. Every "
            "register row carries the same boilerplate access disclaimer "
            "regardless of the site actually being open or not, so 'Access' "
            "was not a usable per-tree signal; PUBLIC_SITES above was "
            "decided by knowledge of the site itself, not by anything in "
            "the data."
        ),
        "entries": entries,
    }

    dest = os.path.join(ROOT, "data", "registers", "ireland-heritage-trees.json")
    with open(dest, "w") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"wrote {len(entries)} entries to {dest}")


if __name__ == "__main__":
    build()
