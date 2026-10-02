#!/usr/bin/env python3
"""Link every reader sighting to the published tree it became.

Hidde, 2026-10-02, with a screenshot of the app showing the same camphor
twice: "why am I seeing this tree twice". His own sighting ("A tree near
Fukuoka", status sent) had been published by a session as fuk_016, the Camphor
of Oimatsu Tenjin Shrine, with the sighting's photograph as the tree's lead,
and nothing told the sighting row. The app draws a sighting with no tree_id as
"your tree" beside the catalogue, so one tree wore two cards.

The city file knows the answer: a contributor photograph carries the
`sighting_id` it came from. This walks every such photograph, lead or extra,
and PATCHes the sighting row to `tree_id = <tree>` and `status = published`
where either differs. Idempotent; runs on every knock beside photo_takedown.py;
without SUPABASE_SERVICE_KEY it prints what it would do and changes nothing.

    python3 scripts/sightings_link.py [--dry]
"""
import glob
import json
import os
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPA = "https://caimvxiyrtifilimlkqw.supabase.co"
KEY = os.environ.get("SUPABASE_SERVICE_KEY")


def _req(path, method="GET", body=None):
    headers = {"apikey": KEY, "Authorization": "Bearer " + KEY,
               "Content-Type": "application/json", "Prefer": "return=representation"}
    req = urllib.request.Request(SUPA + path, method=method, headers=headers,
                                 data=json.dumps(body).encode() if body is not None else None)
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    return json.loads(raw) if raw else None


def wanted():
    """{sighting_id: tree_id} from every contributor photograph on a page."""
    out = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        with open(path, encoding="utf-8") as fh:
            city = json.load(fh)
        for t in city.get("trees") or []:
            shots = [t.get("photo") or {}] + [p for p in (t.get("photos") or []) if p]
            for p in shots:
                sid = p.get("sighting_id")
                if p.get("source") == "contributor" and sid:
                    out[sid] = t["id"]
    return out


def main(argv):
    dry = "--dry" in argv or not KEY
    want = wanted()
    if not want:
        print("sightings_link: no contributor photographs on any page")
        return 0
    if not KEY:
        print(f"sightings_link (dry, no SUPABASE_SERVICE_KEY): {len(want)} photograph(s) would be checked")
        return 0
    ids = ",".join(want)
    rows = _req(f"/rest/v1/sightings?select=id,tree_id,status&id=in.({ids})") or []
    fixed = 0
    for r in rows:
        tree = want.get(r["id"])
        if not tree:
            continue
        if r.get("tree_id") == tree and r.get("status") == "published":
            continue
        print(f"  {r['id'][:8]}: tree_id {r.get('tree_id')!r} -> {tree!r}, status {r.get('status')!r} -> 'published'"
              + (" (dry)" if dry else ""))
        if not dry:
            q = urllib.parse.urlencode({"id": f"eq.{r['id']}"})
            _req(f"/rest/v1/sightings?{q}", "PATCH", {"tree_id": tree, "status": "published"})
        fixed += 1
    print(f"sightings_link: {len(rows)} sighting(s) behind published photographs, {fixed} linked")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
