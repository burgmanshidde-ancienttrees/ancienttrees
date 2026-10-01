#!/usr/bin/env python3
"""Who looks after a place: grant, name and sync the ambassadors.

Hidde, 2026-10-02: "email each person that adds trees to become the cities
ambassador ... maybe we can even give them special tag if they want - share
some responsibility and amplify them." The convention behind the tag is
komoot's Pioneer (CONVENTIONS.md 2026-10-02): per place, a badge beside the
name, earned by what the person already did. The rule for who is asked lives in
CLAUDE.md ("Ambassadors"); this script only records the answer.

    python3 scripts/ambassador.py --list
    python3 scripts/ambassador.py --grant <user_id> <place_slug>
    python3 scripts/ambassador.py --public <user_id> <place_slug> yes|no
    python3 scripts/ambassador.py --revoke <user_id> <place_slug>
    python3 scripts/ambassador.py --sync
    python3 scripts/ambassador.py --grant-named "<Name>" <place_slug>

--grant-named is for somebody who gave us trees by MAIL and has no app account
(Hidde, 2026-10-02, on Hans Erik Lund and Paulo Araujo: "dont email paulo or
hans ive had much contact with them just make them ambassador"). It writes a
json-only entry, named and public on his word, with no user_id; the badge
reaches them in the app the day they make an account and --grant links it. A
sync keeps these entries, because the table knows nothing about them.

--grant writes the row to Supabase (the person said yes to Hidde's mail) with
`public` false: consent to be NAMED on the website is a second, separate yes,
and --public records it. --sync rewrites data/ambassadors.json from the table,
with the display name only where public is true, and drops anybody whose
account is gone (the row cascades, so the table is already right; the file has
to follow). The knock runs --sync beside photo_takedown.py, for the same
promise. Everything needs SUPABASE_SERVICE_KEY; without it this prints what it
would do and changes nothing.
"""
import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPA = "https://caimvxiyrtifilimlkqw.supabase.co"
KEY = os.environ.get("SUPABASE_SERVICE_KEY")
FILE = os.path.join(ROOT, "data", "ambassadors.json")


def _req(path, method="GET", body=None, prefer=None):
    headers = {"apikey": KEY, "Authorization": "Bearer " + KEY,
               "Content-Type": "application/json"}
    if prefer:
        headers["Prefer"] = prefer
    req = urllib.request.Request(SUPA + path, method=method, headers=headers,
                                 data=json.dumps(body).encode() if body is not None else None)
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    return json.loads(raw) if raw else None


def place_name(slug):
    """The place's name as its own city file spells it, English (CLAUDE.md,
    place names). A slug with no file is refused rather than guessed."""
    path = os.path.join(ROOT, "data", "cities", f"{slug}.json")
    if not os.path.exists(path):
        sys.exit(f"ambassador: no data/cities/{slug}.json; the place has to exist before it has an ambassador")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh).get("city") or slug


def rows():
    return _req("/rest/v1/ambassadors?select=user_id,place_slug,place_name,public,since&order=since.asc") or []


def grant(user_id, slug):
    name = place_name(slug)
    row = {"user_id": user_id, "place_slug": slug, "place_name": name,
           "public": False, "since": datetime.date.today().isoformat()}
    if not KEY:
        print("ambassador (dry, no SUPABASE_SERVICE_KEY): would grant", row)
        return
    _req("/rest/v1/ambassadors?on_conflict=user_id,place_slug", "POST", [row],
         prefer="resolution=merge-duplicates,return=minimal")
    print(f"ambassador: {user_id[:8]} is the ambassador of {name} ({slug}), not yet named publicly")
    sync()


def set_public(user_id, slug, yes):
    if not KEY:
        print(f"ambassador (dry): would set public={yes} for {user_id[:8]} / {slug}")
        return
    q = urllib.parse.urlencode({"user_id": f"eq.{user_id}", "place_slug": f"eq.{slug}"})
    _req(f"/rest/v1/ambassadors?{q}", "PATCH", {"public": yes}, prefer="return=minimal")
    print(f"ambassador: {user_id[:8]} / {slug}: {'named on the page' if yes else 'badge only, not named'}")
    sync()


def revoke(user_id, slug):
    if not KEY:
        print(f"ambassador (dry): would revoke {user_id[:8]} / {slug}")
        return
    q = urllib.parse.urlencode({"user_id": f"eq.{user_id}", "place_slug": f"eq.{slug}"})
    _req(f"/rest/v1/ambassadors?{q}", "DELETE", prefer="return=minimal")
    print(f"ambassador: {user_id[:8]} / {slug} revoked")
    sync()


def grant_named(name, slug):
    """A named, public ambassador with no account: Hidde's own word stands in
    for the consent flag, because he has the correspondence."""
    pname = place_name(slug)
    with open(FILE, encoding="utf-8") as fh:
        doc = json.load(fh)
    entries = [e for e in doc["ambassadors"] if not (e.get("user_id") is None and e["place_slug"] == slug
                                                    and e.get("display_name") == name)]
    entries.append({"user_id": None, "place_slug": slug, "place_name": pname, "public": True,
                    "since": datetime.date.today().isoformat(), "display_name": name,
                    "source": "mail, granted by Hidde"})
    doc["ambassadors"] = entries
    with open(FILE, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"ambassador: {name} is named on /{slug} as the ambassador of {pname} (no account yet)")


def sync():
    """data/ambassadors.json from the table. The file carries a display name
    ONLY for a row whose person consented (public), and that name is read
    from profiles at sync time rather than stored twice."""
    if not KEY:
        print("ambassador --sync: no SUPABASE_SERVICE_KEY, file left as it is")
        return 0
    try:
        table = rows()
    except urllib.error.HTTPError as e:
        if e.code in (404, 400):
            print("ambassador --sync: the table does not exist yet (paste supabase/PENDING.sql); file left as it is")
            return 0
        raise
    names = {}
    public_ids = sorted({r["user_id"] for r in table if r.get("public")})
    if public_ids:
        q = ",".join(public_ids)
        for p in _req(f"/rest/v1/profiles?select=user_id,display_name&user_id=in.({q})") or []:
            names[p["user_id"]] = p.get("display_name")
    out = []
    for r in table:
        entry = {"user_id": r["user_id"], "place_slug": r["place_slug"],
                 "place_name": r["place_name"], "public": bool(r.get("public")),
                 "since": r.get("since")}
        if entry["public"] and names.get(r["user_id"]):
            entry["display_name"] = names[r["user_id"]]
        elif entry["public"]:
            # Consented, but never set a name: nothing to print, and the page
            # says nothing rather than inventing one.
            entry["public"] = False
            entry["note"] = "consented but has no display name yet"
        out.append(entry)
    with open(FILE, encoding="utf-8") as fh:
        doc = json.load(fh)
    # Named people without an account live only in this file; keep them.
    kept = [e for e in doc.get("ambassadors", []) if e.get("user_id") is None]
    doc["ambassadors"] = out + kept
    doc["synced"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    with open(FILE, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"ambassador --sync: {len(out)} row(s), {sum(1 for e in out if e['public'])} named publicly")
    return 0


def listing():
    with open(FILE, encoding="utf-8") as fh:
        doc = json.load(fh)
    if not doc["ambassadors"]:
        print("no ambassadors yet (file synced", doc.get("synced"), ")")
    for e in doc["ambassadors"]:
        who = (e.get("user_id") or "no account")[:10]
        print(f"{who:<10}  {e['place_name']:<24} since {e['since']}  "
              f"{'named: ' + e['display_name'] if e.get('display_name') else 'badge only'}")


def main(argv):
    if "--list" in argv or len(argv) == 1:
        return listing()
    if "--sync" in argv:
        return sync()
    if "--grant-named" in argv:
        i = argv.index("--grant-named")
        return grant_named(argv[i + 1], argv[i + 2])
    if "--grant" in argv:
        i = argv.index("--grant")
        return grant(argv[i + 1], argv[i + 2])
    if "--public" in argv:
        i = argv.index("--public")
        return set_public(argv[i + 1], argv[i + 2], argv[i + 3].lower() in ("yes", "true", "1"))
    if "--revoke" in argv:
        i = argv.index("--revoke")
        return revoke(argv[i + 1], argv[i + 2])
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv) or 0)
