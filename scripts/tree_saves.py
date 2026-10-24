#!/usr/bin/env python3
"""How many readers saved each tree to Want to go, as counts only.

Hidde, 2026-10-24, on which tree gets the full pin where two collide on a map:
"i think photo and likes are the best way." The photograph the data already
has; the likes live in Supabase's `saves` table and never reached the build.
This writes data/tree-saves.json, {tree_id: count}, nightly from
data-digest.yml, and the site build and the app feed read it (lib/saves.ts,
lib/app-feed.ts `saves`, TreeMap.swift pinPriority).

Counts only, never who: a reader's account never lives in the repository
(CLAUDE.md, "Privacy and accounts"), and our own accounts are left out
(ours.is_ours), as the digest leaves them out of every number.

    python3 scripts/tree_saves.py          # needs SUPABASE_SERVICE_KEY
"""
import datetime
import json
import os
import pathlib
import sys
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ours  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "tree-saves.json"
SUPA = "https://caimvxiyrtifilimlkqw.supabase.co"


def rows(key):
    """Every save, a thousand at a time (PostgREST's default page)."""
    out, start, page = [], 0, 1000
    while True:
        req = urllib.request.Request(
            SUPA + "/rest/v1/saves?select=tree_id,user_id",
            headers={"apikey": key, "Authorization": "Bearer " + key,
                     "Range": "%d-%d" % (start, start + page - 1)})
        with urllib.request.urlopen(req, timeout=30) as r:
            batch = json.load(r)
        out += batch
        if len(batch) < page:
            return out
        start += page


def main():
    key = os.environ.get("SUPABASE_SERVICE_KEY", "").strip()
    if not key:
        env = pathlib.Path.home() / ".ancienttrees-supabase.env"
        if env.exists():
            for line in env.read_text().splitlines():
                if line.startswith("SUPABASE_SERVICE_KEY="):
                    key = line.split("=", 1)[1].strip()
    if not key:
        print("tree_saves: no SUPABASE_SERVICE_KEY, leaving data/tree-saves.json as it is")
        return 0
    counts = {}
    for r in rows(key):
        tid = r.get("tree_id")
        if not tid or ours.is_ours(r.get("user_id")):
            continue
        counts[tid] = counts.get(tid, 0) + 1
    doc = {"updated": datetime.date.today().isoformat(),
           "note": "Readers' Want to go saves per tree, counts only, our own accounts left out. "
                   "Written by scripts/tree_saves.py; read by lib/saves.ts and the app feed.",
           "saves": dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))}
    OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    top = list(doc["saves"].items())[:5]
    print("tree_saves: %d trees saved by readers, %d saves; top %s"
          % (len(counts), sum(counts.values()), top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
