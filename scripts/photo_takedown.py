#!/usr/bin/env python3
"""Keep the deletion promise for a photograph somebody sent us.

The gap this closes, found 2026-09-03 while writing down what protects this
project. /terms and /privacy both say that deleting your account removes
everything attached to it, and the database keeps that promise properly:
delete_user() takes the auth row and the foreign keys take saves, visited,
profiles, follows, blocks, reports and the sightings themselves.

A PUBLISHED photograph is the one thing that is not in the database. When a
reader's picture goes on a tree's page it becomes a copy in data/cities and a
file in site/public/photos, in a static site the database cannot reach. So an
account could be deleted in full and the person's photograph would stay on the
internet, credited to a name belonging to somebody who had just asked us to
forget them. That is the worst kind of broken promise: silent, and about the
one thing they most wanted gone.

The design is a sweep rather than a queue, deliberately. A queue needs a table,
a migration Hidde has to paste, and a delete_user() that knows about the
website; a sweep needs nothing but the id we already record, and it also
catches an account removed by any other route, including by hand in the
Supabase dashboard. The cost is latency: a published photograph comes off
within a day rather than within a second, which is why /terms says a day.

    python3 scripts/photo_takedown.py            # sweep and remove
    python3 scripts/photo_takedown.py --check    # report only, exit 1 if any

Needs SUPABASE_SERVICE_KEY. Without it the sweep cannot ask whether an account
still exists, so it says so and exits 0 rather than guessing, the same way
every other reader-data script here behaves when the secret is absent.
"""

import argparse
import glob
import json
import os
import sys
import urllib.error
import urllib.request

BASE = "https://caimvxiyrtifilimlkqw.supabase.co"
KEY = os.environ.get("SUPABASE_SERVICE_KEY")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def contributor_photos():
    """Every published photograph that came from a reader, with its account.

    Recognised by photo.source == "contributor", which preflight requires to
    travel with a contributor_user_id: a reader's photograph without the id is
    a photograph we could never take down, so shipping one is refused there
    rather than discovered here.
    """
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data/cities/*.json"))):
        with open(path, encoding="utf-8") as fh:
            city = json.load(fh)
        for tree in city.get("trees", []):
            photo = tree.get("photo") or {}
            if photo.get("source") != "contributor":
                continue
            out.append({
                "path": path,
                "city": city.get("city"),
                "tree_id": tree.get("id"),
                "tree_name": tree.get("name"),
                "user_id": photo.get("contributor_user_id"),
                "url": photo.get("url"),
            })
    return out


def account_exists(user_id):
    """True, False, or None when we could not tell.

    None matters: a network failure must never be read as "this account is
    gone", because the action on the other side is deleting a photograph.
    """
    req = urllib.request.Request(f"{BASE}/auth/v1/admin/users/{user_id}")
    req.add_header("apikey", KEY)
    req.add_header("Authorization", f"Bearer {KEY}")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status == 200
    except urllib.error.HTTPError as e:
        if e.code in (403, 404):
            return False
        return None
    except Exception:
        return None


def unvendor(url):
    """Drop a photograph's local copies and its manifest entry.

    Nothing here is fatal. A file that is already gone is the state we want,
    and a manifest entry with no file is caught by qa.py's own check on the
    next build, which is a better place to hear about it than here.
    """
    removed = []
    man_path = os.path.join(ROOT, "data/photo-manifest.json")
    if not os.path.exists(man_path):
        return removed
    with open(man_path, encoding="utf-8") as fh:
        man = json.load(fh)
    rec = (man.get("photos") or {}).pop(url, None)
    if not rec:
        return removed
    for width in rec.get("widths", []):
        f = os.path.join(ROOT, "site/public/photos", f"{rec['base']}-{width}.jpg")
        if os.path.exists(f):
            os.remove(f)
            removed.append(os.path.relpath(f, ROOT))
    with open(man_path, "w", encoding="utf-8") as fh:
        json.dump(man, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return removed


def take_down(item):
    """Remove one photograph from its tree, leaving an honest gap behind.

    The tree keeps its page and its story. A tree with no photograph is a
    normal state here, said plainly on the page, which is exactly why this is
    safe to do without anybody looking: the worst case is a page that loses a
    picture it should have kept, and the best case is a promise kept.
    """
    with open(item["path"], encoding="utf-8") as fh:
        city = json.load(fh)
    for tree in city.get("trees", []):
        if tree.get("id") != item["tree_id"]:
            continue
        tree["photo"] = {
            "url": None,
            "license": None,
            "attribution": None,
            "status": "missing",
            "note": "A reader's photograph stood here and came off when they "
                    "deleted their account. Deleting an account takes what was "
                    "published with it.",
        }
    with open(item["path"], "w", encoding="utf-8") as fh:
        json.dump(city, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return unvendor(item["url"]) if item["url"] else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="report only, exit 1 if a photograph should have come off")
    args = ap.parse_args()

    photos = contributor_photos()
    if not photos:
        print("photo_takedown: no reader photographs are published, nothing to sweep")
        return 0
    if not KEY:
        print("photo_takedown: SUPABASE_SERVICE_KEY is not set, so whether these "
              "%d account(s) still exist cannot be asked. Skipping rather than "
              "guessing." % len({p["user_id"] for p in photos}))
        return 0

    verdicts, gone, unknown = {}, [], []
    for item in photos:
        uid = item["user_id"]
        if uid not in verdicts:
            verdicts[uid] = account_exists(uid)
        if verdicts[uid] is False:
            gone.append(item)
        elif verdicts[uid] is None:
            unknown.append(item)

    print("photo_takedown: %d reader photograph(s) published, %d account(s), "
          "%d to take down" % (len(photos), len(verdicts), len(gone)))
    for item in unknown:
        print("  UNKNOWN %s (%s): could not reach the account. Left alone."
              % (item["tree_id"], item["tree_name"]))
    for item in gone:
        print("  GONE %s (%s), %s" % (item["tree_id"], item["tree_name"], item["city"]))
    if args.check:
        return 1 if gone else 0
    for item in gone:
        files = take_down(item)
        print("  removed the photograph from %s%s"
              % (item["tree_id"], (" and %d local file(s)" % len(files)) if files else ""))
    if gone:
        print("photo_takedown: commit this. %d photograph(s) came off." % len(gone))
    return 0


if __name__ == "__main__":
    sys.exit(main())
