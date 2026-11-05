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


def fetch(key, path):
    """Every row of a table query, a thousand at a time."""
    out, start, page = [], 0, 1000
    while True:
        req = urllib.request.Request(
            SUPA + path,
            headers={"apikey": key, "Authorization": "Bearer " + key,
                     "Range": "%d-%d" % (start, start + page - 1)})
        with urllib.request.urlopen(req, timeout=30) as r:
            batch = json.load(r)
        out += batch
        if len(batch) < page:
            return out
        start += page


def worth_counts(key):
    """Readers whose STANDING vote on a tree is "worth it" (2026-11-05, the
    Highlights order, site/src/lib/highlights.ts). A vote is a submissions row
    whose why is "worth it", "not worth it" or "vote undone: ...", newest
    first; the first of those per reader and tree is the one that stands
    (worthit-js.ts reads it the same way). Our own accounts left out."""
    standing = {}
    for r in fetch(key, "/rest/v1/submissions?select=tree,why,user_id&kind=eq.feedback&order=created_at.desc"):
        uid, why = r.get("user_id"), str(r.get("why") or "")
        tid = str(r.get("tree") or "").split(" (")[0].strip()
        if not uid or not tid or ours.is_ours(uid):
            continue
        if why not in ("worth it", "not worth it") and not why.startswith("vote undone"):
            continue
        standing.setdefault((uid, tid), why)
    counts = {}
    for (_, tid), why in standing.items():
        if why == "worth it":
            counts[tid] = counts.get(tid, 0) + 1
    return counts


def note_counts(key):
    """Visible notes per tree, our own accounts left out."""
    counts = {}
    for r in fetch(key, "/rest/v1/tree_notes?select=tree_id,user_id,hidden"):
        tid = r.get("tree_id")
        if not tid or r.get("hidden") or ours.is_ours(r.get("user_id")):
            continue
        counts[tid] = counts.get(tid, 0) + 1
    return counts


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
    def ranked(c):
        return dict(sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))
    # Votes and notes are a bonus to the saves: a table this script cannot
    # read leaves its counts empty rather than failing the night.
    try:
        worth = worth_counts(key)
    except Exception as e:
        print("tree_saves: votes unreadable (%s)" % str(e)[:80])
        worth = {}
    try:
        notes = note_counts(key)
    except Exception as e:
        print("tree_saves: notes unreadable (%s)" % str(e)[:80])
        notes = {}
    doc = {"updated": datetime.date.today().isoformat(),
           "note": "What readers did with each tree, counts only, our own accounts left out: "
                   "Want to go saves, standing Worth the visit votes, visible notes. "
                   "Written by scripts/tree_saves.py; read by lib/saves.ts, lib/highlights.ts "
                   "and the app feed.",
           "saves": ranked(counts),
           "worth": ranked(worth),
           "notes": ranked(notes)}
    OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    top = list(doc["saves"].items())[:5]
    print("tree_saves: %d trees saved by readers, %d saves; top %s; %d worth-it votes on %d trees; %d notes"
          % (len(counts), sum(counts.values()), top, sum(worth.values()), len(worth), sum(notes.values())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
