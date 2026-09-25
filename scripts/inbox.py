#!/usr/bin/env python3
"""Read what readers sent in, in their own words, from a session on Hidde's Mac.

Hidde, 2026-09-25: "ik wil dat je dit kan lezen". The daily digest prints only
the SHAPE of each submission (length, kind, outcome), because DATA.md sits in
a public repository. The words live in Supabase, and until today only the
night run could read them, since the service key existed only as a GitHub
secret. This reads them to the terminal and nowhere else: nothing here writes
a reader's words to a file in the repository.

The key comes from SUPABASE_SERVICE_KEY, or else from ~/.ancienttrees-supabase.env
(outside the repo, chmod 600, the same pattern as ~/.ancienttrees-mail.env).
A session that cannot see that file is not on his Mac and must not be given
the key.

  python3 scripts/inbox.py            open rows (no outcome yet), readers only
  python3 scripts/inbox.py --all      the last 14 days, answered or not
  python3 scripts/inbox.py --ours     include rows from our own accounts
"""
import argparse
import datetime
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ours  # noqa: E402

SUPA = "https://caimvxiyrtifilimlkqw.supabase.co"
ENV_FILE = os.path.expanduser("~/.ancienttrees-supabase.env")


def load_key():
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if key:
        return key
    if not os.path.exists(ENV_FILE):
        return None
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line.startswith("export "):
                line = line[7:]
            if line.startswith("SUPABASE_SERVICE_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                return val if val and "PLAK" not in val else None
    return None


def get(path, key):
    req = urllib.request.Request(SUPA + path, headers={"apikey": key, "Authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--ours", action="store_true")
    ap.add_argument("--days", type=int, default=14)
    a = ap.parse_args()

    key = load_key()
    if not key:
        print("No Supabase key. Put the service_role key in %s as" % ENV_FILE)
        print("  SUPABASE_SERVICE_KEY=...")
        print("(Supabase dashboard > Project Settings > API keys > service_role.)")
        return 1

    since = (datetime.date.today() - datetime.timedelta(days=a.days)).isoformat()
    q = ("/rest/v1/submissions?select=*&created_at=gte.%sT00:00:00&order=created_at.asc" % since)
    if not a.all:
        q += "&outcome=is.null"
    rows = get(q, key)
    shown = 0
    for r in rows:
        if not a.ours and ours.is_ours(r.get("user_id")):
            continue
        shown += 1
        print("=" * 72)
        print("id %s   %s   kind %s   outcome %s" % (
            r.get("id"), (r.get("created_at") or "")[:16], r.get("kind"), r.get("outcome")))
        for f in ("city", "tree", "tree_id", "species", "latitude", "longitude", "photo_url"):
            if r.get(f) not in (None, ""):
                print("  %-9s %s" % (f, r[f]))
        why = (r.get("why") or "").strip()
        if why:
            print("  why:")
            for line in why.splitlines():
                print("    " + line)
    print("=" * 72)
    print("%d row(s)%s." % (shown, "" if a.all else " without an outcome"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
