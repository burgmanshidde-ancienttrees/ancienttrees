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
import datetime
import glob
import json
import os
import sys
import urllib.error
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
            # updated_at travels with it, or the phone never takes the change:
            # SightingSync.merge adopts a remote row only when its updated_at
            # is newer than the phone's last push, and a PATCH that leaves the
            # stamp alone looks to the phone like nothing happened. Found
            # 2026-10-03 on Hidde's own Fukuoka camphor, still two cards a day
            # after this script had linked it.
            now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")
            _req(f"/rest/v1/sightings?{q}", "PATCH",
                 {"tree_id": tree, "status": "published", "updated_at": now})
        fixed += 1
    print(f"sightings_link: {len(rows)} sighting(s) behind published photographs, {fixed} linked")
    tick_collected(dry)
    mark_added(dry)
    drop_public_copies_of_gone_accounts(dry)
    return 0


def drop_public_copies_of_gone_accounts(dry):
    """A deleted account's trees stay; their PUBLIC copies go (Hidde,
    2026-11-12: "het hele idee is toch dat we de bomen houden als mensen hun
    account verwijderen"). The phones and the website now delete only the
    avatar when an account goes, so the photographs of trees stay in the
    private sightings bucket, where data/leads/_sightings.json (unlinked by
    photo_takedown.py) and the published pages still point. What would
    otherwise outlive the person in public is the copy in shared-sightings,
    readable by anyone holding its address; this deletes the copies under any
    folder whose account no longer exists. Never a private original, never a
    living account's file."""
    def call(path, method="GET", body=None):
        req = urllib.request.Request(SUPA + path, method=method,
                                     data=json.dumps(body).encode() if body is not None else None,
                                     headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
                                              "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read()
        return json.loads(raw) if raw else None

    alive, page = set(), 1
    while True:
        got = (call("/auth/v1/admin/users?page=%d&per_page=1000" % page) or {}).get("users") or []
        alive |= {u["id"] for u in got}
        if len(got) < 1000:
            break
        page += 1
    if not alive:
        print("sightings_link: no accounts read, public copies left alone")
        return
    gone = []
    for folder in call("/storage/v1/object/list/shared-sightings", "POST", {"prefix": "", "limit": 1000}) or []:
        if folder.get("id") or folder["name"] in alive:
            continue
        for f in call("/storage/v1/object/list/shared-sightings", "POST",
                      {"prefix": folder["name"] + "/", "limit": 1000}) or []:
            if f.get("id"):
                gone.append(folder["name"] + "/" + f["name"])
    if gone and not dry:
        call("/storage/v1/object/shared-sightings", "DELETE", {"prefixes": gone})
    print("sightings_link: %d public copie(s) of deleted accounts %s"
          % (len(gone), "would go (dry)" if dry else "taken down"))


def mark_added(dry):
    """The sighting a reader's own tree grew from carries `added = true`, which
    public_profile() reads to put "Approved" on that tree's tile (Hidde,
    2026-11-12, supabase/approved-on-profiles.sql). The city file knows:
    found_by_reader.sighting_id. Idempotent; before that file is pasted the
    column does not exist and this says so in one line."""
    ids = set()
    for path in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
        with open(path, encoding="utf-8") as fh:
            for t in json.load(fh).get("trees") or []:
                sid = (t.get("found_by_reader") or {}).get("sighting_id")
                if sid and not str(sid).startswith("tip-"):
                    ids.add(str(sid).lower())
    if not ids:
        return
    try:
        rows = _req("/rest/v1/sightings?select=id,added&id=in.(%s)" % ",".join(sorted(ids))) or []
    except urllib.error.HTTPError as e:
        print("sightings_link: added not marked (HTTP %s; supabase/approved-on-profiles.sql is FOR HIDDE)" % e.code)
        return
    todo = [r["id"] for r in rows if not r.get("added")]
    if todo and not dry:
        q = urllib.parse.urlencode({"id": "in.(%s)" % ",".join(todo)})
        _req("/rest/v1/sightings?%s" % q, "PATCH", {"added": True})
    print("sightings_link: %d reader-found tree(s), %d marked added%s"
          % (len(rows), len(todo), " (dry)" if dry else ""))


def tick_collected(dry):
    """A PHOTOGRAPH OF A TREE IS A VISIT (Hidde, 2026-11-12: "je kan niet een
    foto hebben zonder er te zijn geweest ... waar je hem ook vandaan komt").

    Every surface ticks the tree when the photograph is taken (CollectSheet's
    claim on the iPhone, Collector on Android, add-photo-js on the web; qa's
    check_a_photo_is_a_visit_on_every_surface). This is the backstop for what
    no surface can do: a reader's NEW tree has no tree id when they photograph
    it, and gets one only when we publish it (main() above), so seven readers'
    published trees were missing from their own Collected on 2026-11-12. Any
    account, any route: a sighting with a photograph and a tree id gets a
    `visited` row for that tree, dated the day it reached us, unless a viewing
    pass rejected it as the wrong tree (data/sightings-processed.json). Never
    overwrites an existing tick, never removes one.
    """
    rejected = set()
    try:
        with open(os.path.join(ROOT, "data", "sightings-processed.json"), encoding="utf-8") as fh:
            done = json.load(fh).get("done") or {}
        rejected = {k for k, v in done.items() if isinstance(v, dict) and v.get("outcome") == "rejected"}
    except (OSError, ValueError):
        pass
    # Dated the day it reached us, not the day the camera says (Hidde, same day:
    # "upload datum is relevanter"); a sighting row has no created_at, and
    # updated_at is that day for every row nobody edited since.
    sights = _req("/rest/v1/sightings?select=id,user_id,tree_id,updated_at"
                  "&photo=not.is.null&tree_id=not.is.null&limit=10000") or []
    have = {(v["user_id"], v["tree_id"]) for v in
            (_req("/rest/v1/visited?select=user_id,tree_id&limit=100000") or [])}
    rows = {}
    for r in sights:
        key = (r["user_id"], r["tree_id"])
        if r["id"] in rejected or key in have or key in rows:
            continue
        rows[key] = {"user_id": r["user_id"], "tree_id": r["tree_id"],
                     "visited_at": (r.get("updated_at") or "")[:10] or None}
    for (_, tree) in rows:
        print(f"  collected: {tree}" + (" (dry)" if dry else ""))
    if rows and not dry:
        req = urllib.request.Request(
            SUPA + "/rest/v1/visited?on_conflict=user_id,tree_id", method="POST",
            data=json.dumps(list(rows.values())).encode(),
            headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
                     "Content-Type": "application/json",
                     "Prefer": "resolution=ignore-duplicates,return=minimal"})
        urllib.request.urlopen(req, timeout=30).close()
    print(f"sightings_link: {len(sights)} photographed sighting(s) on a tree, {len(rows)} ticked as collected"
          + (" (dry)" if dry else ""))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
