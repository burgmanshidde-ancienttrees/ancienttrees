#!/usr/bin/env python3
"""Read the photographs readers sent through the app and queue them for a look.

The loop this closes (Hidde, 2026-09-04: "go"). Since 2026-09-03 the app says,
at the moment somebody sends a photograph, that it can appear on the tree's
page with their name under it (DECISIONS.md 2026-09-02), and the share link
lets them see and pass on their own tree. What did not exist was the middle:
nothing read those photographs, looked at them, and put the good ones on the
page. Zero reader photographs had reached a page. This is the retrieval half
of that middle; the judgement half stays a viewing pass (the photo-judge
agent), and scripts/sightings_publish.py applies its verdicts.

What it does, each knock:
  1. Fetches every sighting with a photograph and sharing on (the `shared`
     column, default true; somebody who turned it off is not asking).
  2. Matches it to a tree we map: the app's own tree_id when it ticked one
     off, otherwise the nearest published tree within MATCH_M metres. A
     sighting matching nothing is a tree we do not map: it goes to
     data/leads/_sightings.json as a lead for the normal pipeline, never
     straight to a page, because a page needs the bar every tree meets.
  3. Downloads the photograph from the private bucket to out/sightings/ and,
     on a Mac, scores its light with photo_light.py so the viewing pass can
     skip the obviously bad ones.
  4. Writes data/sighting-queue.json: what the viewing pass LOOKS at, one
     entry per photograph, with the tree it is claimed to be, whether the
     tree already has a photograph, and the reader's display name for the
     credit. Never the email address.

State: data/sightings-processed.json, sighting id -> outcome, so no
photograph is fetched or judged twice. A queue entry that has no verdict yet
is rebuilt from the same rows on the next knock, which is how a dead run
loses nothing.

Needs SUPABASE_SERVICE_KEY. Without it, it says so and exits 0.

    python3 scripts/sightings_inbox.py            # fetch, match, queue
    python3 scripts/sightings_inbox.py --status   # print the queue only
"""
import datetime
import glob
import json
import math
import os
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPA = "https://caimvxiyrtifilimlkqw.supabase.co"
KEY = os.environ.get("SUPABASE_SERVICE_KEY")
QUEUE = os.path.join(ROOT, "data", "sighting-queue.json")
PROCESSED = os.path.join(ROOT, "data", "sightings-processed.json")
LEADS = os.path.join(ROOT, "data", "leads", "_sightings.json")
OUT = os.path.join(ROOT, "out", "sightings")
MATCH_M = 30  # a phone's GPS in a park is rarely better than this


def supa(path):
    req = urllib.request.Request(SUPA + path, headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
        return json.loads(raw) if raw else None


def metres(a_lat, a_lng, b_lat, b_lng):
    r = 6371000.0
    p1, p2 = math.radians(a_lat), math.radians(b_lat)
    dp = math.radians(b_lat - a_lat)
    dl = math.radians(b_lng - a_lng)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def tree_index():
    """Every published tree: id -> {slug, name, lat, lng, photo_status, path}."""
    out = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        slug = os.path.basename(p)[:-5]
        try:
            city = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        for t in city.get("trees", []):
            loc = t.get("location") or {}
            if not t.get("id") or not t.get("story") or loc.get("latitude") is None:
                continue
            ph = t.get("photo") or {}
            out[t["id"]] = {
                "slug": slug, "city": city.get("city"), "name": t.get("name"),
                "lat": loc["latitude"], "lng": loc["longitude"],
                "photo_status": ph.get("status") if ph.get("url") else "none",
                "photo_source": ph.get("source"),
                "path": p,
            }
    return out


def match(row, index):
    """(tree_id, how, distance_m). how is app, distance or none.

    The app's own tree_id wins when it names a tree we still map. Otherwise the
    nearest published tree within MATCH_M. A tree_id the app sent that we no
    longer map falls through to distance rather than being trusted.
    """
    tid = row.get("tree_id")
    lat, lng = row.get("lat"), row.get("lng")
    if tid and tid in index:
        t = index[tid]
        d = metres(lat, lng, t["lat"], t["lng"]) if lat is not None else None
        return tid, "app", None if d is None else round(d)
    if lat is None or lng is None:
        return None, "none", None
    best, best_d = None, None
    for i, t in index.items():
        if abs(t["lat"] - lat) > 0.01 or abs(t["lng"] - lng) > 0.02:
            continue
        d = metres(lat, lng, t["lat"], t["lng"])
        if best_d is None or d < best_d:
            best, best_d = i, d
    if best is not None and best_d <= MATCH_M:
        return best, "distance", round(best_d)
    return None, "none", None if best_d is None else round(best_d)


def load(path, default):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return default


def save(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def fetch_photo(path, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return True
    req = urllib.request.Request(f"{SUPA}/storage/v1/object/sightings/{path}", headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        print(f"  photo {path}: HTTP {e.code}")
        return False
    except Exception as e:
        print(f"  photo {path}: {e.__class__.__name__}")
        return False
    parent = os.path.dirname(dest)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(dest, "wb") as fh:
        fh.write(data)
    return True


def light(dest):
    """photo_light's numbers on a Mac; None where sips is missing (CI)."""
    try:
        sys.path.insert(0, os.path.join(ROOT, "scripts"))
        import photo_light  # noqa: E402
        s = photo_light.score(dest)
        return {"verdict": photo_light.verdict(s), **{k: round(v, 2) if isinstance(v, float) else v
                                                     for k, v in s.items()}}
    except Exception:
        return None


def status():
    q = load(QUEUE, {"queue": []}).get("queue", [])
    print(f"sightings inbox: {len(q)} photograph(s) waiting for a look")
    for e in q:
        print(f"  {e['sighting_id'][:8]}  {e.get('tree_id') or 'NO MATCH'}  "
              f"{(e.get('tree_name') or e.get('name') or '')[:40]}  "
              f"match={e['match']}  has_photo={e['current_photo']}  light={(e.get('light') or {}).get('verdict', 'unmeasured')}")
    return 0


def main():
    if "--status" in sys.argv:
        return status()
    if not KEY:
        print("sightings inbox: SUPABASE_SERVICE_KEY absent, nothing read")
        return 0
    try:
        rows = supa("/rest/v1/sightings?select=user_id,id,tree_id,name,note,species,age,"
                    "lat,lng,taken_at,status,photo,shared,updated_at"
                    "&photo=not.is.null&shared=eq.true&order=updated_at.asc") or []
    except Exception as e:
        print(f"sightings inbox: could not read sightings ({e.__class__.__name__}: {str(e)[:80]})")
        return 0
    try:
        profiles = {p["user_id"]: p.get("display_name") or ""
                    for p in (supa("/rest/v1/profiles?select=user_id,display_name") or [])}
    except Exception:
        profiles = {}

    processed = load(PROCESSED, {"_note": "sighting id -> what happened to the "
                                          "photograph a reader sent, so none is judged "
                                          "twice. Written by sightings_inbox.py and "
                                          "sightings_publish.py.", "done": {}})
    done = processed.setdefault("done", {})
    index = tree_index()
    leads_doc = load(LEADS, {"_note": "Trees readers added through the app that match "
                                      "nothing we map. Leads for the normal pipeline, never "
                                      "an import: a page needs the bar every tree meets. "
                                      "The photograph sits in the private sightings bucket "
                                      "under the path recorded here; the display name is "
                                      "not recorded, because a lead is not a credit.",
                             "leads": []})
    lead_ids = {l.get("sighting_id") for l in leads_doc["leads"]}

    queue, new_leads, skipped = [], 0, 0
    today = datetime.date.today().isoformat()
    for row in rows:
        sid = row["id"]
        if sid in done:
            skipped += 1
            continue
        tid, how, dist = match(row, index)
        if tid is None:
            if sid not in lead_ids:
                leads_doc["leads"].append({
                    "sighting_id": sid, "user_id": row["user_id"],
                    "name": row.get("name") or "", "species": row.get("species"),
                    "age": row.get("age"), "note": (row.get("note") or "")[:500],
                    "latitude": row.get("lat"), "longitude": row.get("lng"),
                    "taken_at": row.get("taken_at"), "photo": row.get("photo"),
                    "nearest_published_m": dist,
                    "status": "lead",
                    "why": "added by a reader through the app; matches no tree we map. "
                           "Verify to the normal bar before it gets a page.",
                    "seen": today,
                })
                new_leads += 1
            done[sid] = {"outcome": "lead", "date": today}
            continue
        t = index[tid]
        dest = os.path.join(OUT, f"{sid}.jpg")
        if not fetch_photo(row["photo"], dest):
            continue
        queue.append({
            "sighting_id": sid, "user_id": row["user_id"],
            "display_name": profiles.get(row["user_id"]) or "",
            "tree_id": tid, "city_slug": t["slug"], "city": t["city"], "tree_name": t["name"],
            "match": how, "distance_m": dist,
            "current_photo": t["photo_status"], "current_source": t["photo_source"],
            "name": row.get("name") or "", "species": row.get("species"),
            "note": (row.get("note") or "")[:300],
            "taken_at": row.get("taken_at"), "photo_path": row["photo"],
            "file": os.path.relpath(dest, ROOT),
            "light": light(dest),
        })

    save(QUEUE, {"_note": "Photographs readers sent through the app, matched to a tree "
                          "we map, waiting for a viewing pass. Judge with the photo-judge "
                          "agent and apply with scripts/sightings_publish.py. Rebuilt on "
                          "every knock from the rows without a verdict.",
                 "written": today, "queue": queue})
    save(PROCESSED, processed)
    if new_leads:
        save(LEADS, leads_doc)
    print(f"sightings inbox: {len(rows)} row(s) with a photograph, {skipped} already handled, "
          f"{len(queue)} queued for a look, {new_leads} new lead(s) for trees we do not map")
    for e in queue:
        print(f"  {e['sighting_id'][:8]}  {e['tree_id']}  {e['tree_name'][:40]}  "
              f"match={e['match']}{'' if e['distance_m'] is None else ' ' + str(e['distance_m']) + 'm'}  "
              f"has_photo={e['current_photo']}  light={(e.get('light') or {}).get('verdict', 'unmeasured')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
