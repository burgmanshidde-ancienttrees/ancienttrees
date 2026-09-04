#!/usr/bin/env python3
"""Take the PERSON out of a published photograph when their account goes.

The gap this closes, found 2026-09-03 while writing down what protects this
project. Deleting an account empties the database properly: delete_user()
takes the auth row and the foreign keys take saves, visited, profiles,
follows, blocks, reports and the sightings themselves.

A PUBLISHED photograph is the one thing that is not in the database. When a
reader's picture goes on a tree's page it becomes a copy in data/cities and a
file in site/public/photos, in a static site the database cannot reach. So an
account could be deleted in full and their name would stay on the internet,
under a photograph, belonging to somebody who had just asked us to forget them.

What this does about it changed on 2026-09-04, on Hidde's ruling: "als de boom
een verrijking van de database is dan moeten we de info houden maar loskoppelen
van een account". It used to delete the photograph. Now it UNLINKS it: the name
comes off, the account id comes off, `unlinked` is set, and the picture stays.

The two halves are different things and that is the whole point. A name under a
photograph is a person, and it goes. A photograph of a tree is not a person; it
is often the only picture of that tree, on a page that is worse without it. The
licence for keeping it is in /terms under "What you send us", where permission
to show a PUBLISHED photograph explicitly survives deletion and is the only
thing that does. Ownership never transfers. Somebody who wants the picture
itself gone sends a privacy request, and /terms and /privacy both say it goes.

The design is a sweep rather than a queue, deliberately. A queue needs a table,
a migration Hidde has to paste, and a delete_user() that knows about the
website; a sweep needs nothing but the id we already record, and it also
catches an account removed by any other route, including by hand in the
Supabase dashboard. The cost is latency: a published photograph comes off
within a day rather than within a second, which is why /terms says a day.

    python3 scripts/photo_takedown.py            # sweep and unlink
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
# What a photograph is credited to once the account behind it is gone. Not a
# name, because a name is the part that had to go; not blank, because a reader
# gave us this and the page should say a reader did.
ANON_CREDIT = "A reader of Ancient Trees"


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
            # Already unlinked: the account went, the picture stayed, and there
            # is nobody left to ask Supabase about. Asking again would spend a
            # request a night forever on a question already answered.
            if photo.get("unlinked"):
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
    """UNLINK one photograph from the account that sent it. The picture stays.

    Changed 2026-09-04 on Hidde's ruling: "als de boom een verrijking van de
    database is dan moeten we de info houden maar loskoppelen van een account".
    Until then this deleted the photograph outright, which kept the promise as
    /terms then worded it and threw away the thing the loop exists to collect:
    often the only picture of that tree, on a page that is worse without it.

    So the person comes off and the picture stays. The display name goes, the
    account id goes, and `unlinked` marks what happened so nothing ever asks
    Supabase about that account again. What is left is a photograph of a tree
    with nothing tying it to anybody.

    The licence for this is in /terms under "What you send us": permission to
    show a PUBLISHED photograph survives deletion, and it is the one thing that
    does. Ownership does not transfer and never did; somebody who wants the
    picture itself gone sends a privacy request and it goes, by hand, which is
    the same sentence in /terms and /privacy.
    """
    with open(item["path"], encoding="utf-8") as fh:
        city = json.load(fh)
    for tree in city.get("trees", []):
        if tree.get("id") != item["tree_id"]:
            continue
        photo = tree.get("photo") or {}
        photo.pop("contributor_user_id", None)
        photo["attribution"] = ANON_CREDIT
        photo["license"] = ("Provided by a reader through the Ancient Trees app, "
                            "all rights reserved")
        photo["unlinked"] = True
        photo["note"] = ((photo.get("note") or "").split(" The account was ")[0]
                         + " The account was deleted, so the photograph was unlinked "
                           "from it: the picture stays under the licence in /terms, "
                           "the person does not.")
        tree["photo"] = photo
    with open(item["path"], "w", encoding="utf-8") as fh:
        json.dump(city, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return []


def unlink_leads(gone_ids):
    """Take the account id off a lead a deleted account had sent us.

    Same ruling as the photographs and the same split (2026-09-04): the TREE
    is a fact about a tree and stays, the account behind it is a person and
    goes. A lead is not published, but data/leads sits in this repository, so
    an id left there outlives the account exactly the way a name under a
    photograph would. The tree, its coordinates and its note stay, because
    that is the enrichment the ruling is about.
    """
    path = os.path.join(ROOT, "data/leads/_sightings.json")
    if not os.path.exists(path) or not gone_ids:
        return 0
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    n = 0
    for lead in doc.get("leads", []):
        if lead.get("user_id") in gone_ids:
            lead.pop("user_id", None)
            lead["unlinked"] = True
            n += 1
    if n:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
    return n


def lead_accounts():
    """Every account id sitting in the sightings leads file."""
    path = os.path.join(ROOT, "data/leads/_sightings.json")
    if not os.path.exists(path):
        return set()
    try:
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
    except Exception:
        return set()
    return {l["user_id"] for l in doc.get("leads", []) if l.get("user_id")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="report only, exit 1 if a photograph should have come off")
    args = ap.parse_args()

    photos = contributor_photos()
    leads = lead_accounts()
    if not photos and not leads:
        print("photo_takedown: no reader photographs are published and no lead names "
              "an account, nothing to sweep")
        return 0
    if not KEY:
        print("photo_takedown: SUPABASE_SERVICE_KEY is not set, so whether these "
              "%d account(s) still exist cannot be asked. Skipping rather than "
              "guessing." % len({p["user_id"] for p in photos} | leads))
        return 0

    verdicts, gone, unknown = {}, [], []
    for uid in sorted(leads):
        verdicts[uid] = account_exists(uid)
    for item in photos:
        uid = item["user_id"]
        if uid not in verdicts:
            verdicts[uid] = account_exists(uid)
        if verdicts[uid] is False:
            gone.append(item)
        elif verdicts[uid] is None:
            unknown.append(item)

    print("photo_takedown: %d reader photograph(s) published, %d account(s), "
          "%d to unlink" % (len(photos), len(verdicts), len(gone)))
    for item in unknown:
        print("  UNKNOWN %s (%s): could not reach the account. Left alone."
              % (item["tree_id"], item["tree_name"]))
    for item in gone:
        print("  GONE %s (%s), %s" % (item["tree_id"], item["tree_name"], item["city"]))
    stale_leads = {u for u, v in verdicts.items() if v is False} & lead_accounts()
    if args.check:
        # --check answers "is anything still linked to an account that is gone",
        # which is both halves or it is not an answer.
        return 1 if (gone or stale_leads) else 0
    for item in gone:
        take_down(item)
        print("  unlinked the photograph on %s: the picture stays, the name is off"
              % item["tree_id"])
    n_leads = unlink_leads({u for u, v in verdicts.items() if v is False})
    if n_leads:
        print("  unlinked %d lead(s) sent by a deleted account: the tree stays, the "
              "id is off" % n_leads)
    if gone or n_leads:
        print("photo_takedown: commit this. %d photograph(s) and %d lead(s) unlinked "
              "from a deleted account." % (len(gone), n_leads))
    return 0


if __name__ == "__main__":
    sys.exit(main())
