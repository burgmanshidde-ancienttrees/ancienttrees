#!/usr/bin/env python3
"""Readers' own words that have not reached their tree's page yet.

Hidde, 2026-10-22, after the Tangier fig: "we krijgen soms zoals bij tangier
hele stukken - zonde om die niet te gebruiken". A reader who writes about a
tree we publish gets their words on that page, quoted and unnamed, their
facts stated as theirs (CLAUDE.md, Reader input). Until today that was done
by hand when somebody remembered; on the day this was written 3 of the 35
trees with a reader's contribution quoted them.

This reads every note a stranger left with a sighting (the app) and every
`why` with a submission (web and app) that names a tree we publish, and
prints the ones whose words are not on the page: no run of six words from
the note appears in the story. A note in another language than the story
cannot match and is listed for a look ("other language?"). Our own accounts
are left out (scripts/ours.py). The notes stay in Supabase: they are readers'
text and this repository is public, so nothing here writes them to disk.

  python3 scripts/reader_words.py            the notes still to use
  python3 scripts/reader_words.py --all      every note, used or not
  python3 scripts/reader_words.py --tree tng_001
  python3 scripts/reader_words.py --done <row id> "why"   quoted in translation,
                                     or nothing in it belongs on the page

Shorter than MIN_WORDS is not a note worth a quote ("big tree!"). --done keeps
only the row id and a reason in data/reader-words-done.json, never the words.

WORDS THAT CAME BY MAIL (Hidde, 2026-10-25, on Luisa Carta's two Sardinian
oaks: "shouldnt we use her literal words so that google loves us more than
ai?"). Everything above came from the app and the form; a contribution that
arrived by mail had its facts retold in our story and its own sentences lost.
So the session that handles such a mail copies the sender's OWN sentences
about a tree into data/outreach-words.json, which is private (gitignored,
synced by private_store.py like the rest of outreach) because they are a
person's words and this repository is public:

  {"words": [{"id": "mail-2026-10-13-carta-1", "tree_id": "sar_006",
              "date": "2026-10-13", "lang": "it", "text": "..."}]}

Only their own words: a passage they quote from a book is someone else's
text and is named, never copied (Camarda in that same mail). They are listed
here beside the app notes and go on the page the same way, quoted, unnamed.
"""
import argparse
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inbox  # noqa: E402
import ours  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN_WORDS = 12
RUN = 6  # words in a row that count as a quote
DONE = os.path.join(ROOT, "data", "reader-words-done.json")
MAILED = os.path.join(ROOT, "data", "outreach-words.json")


def done():
    try:
        return json.load(open(DONE))
    except (OSError, ValueError):
        return {}


def words(s):
    return re.findall(r"[^\W_]+", (s or "").lower())


def quoted(note, story):
    n, s = words(note), " ".join(words(story))
    if len(n) < RUN:
        return False
    return any(" ".join(n[i:i + RUN]) in s for i in range(len(n) - RUN + 1))


def live_trees():
    out = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        slug = os.path.basename(p)[:-5]
        for t in json.load(open(p)).get("trees") or []:
            out[t["id"]] = (slug, t)
    return out


def notes(key):
    """(tree_id, source, row id, date, text) for every stranger's note on a tree."""
    rows = []
    for r in inbox.get("/rest/v1/sightings?select=id,user_id,tree_id,note,taken_at,status"
                       "&tree_id=not.is.null&note=neq.", key):
        if r.get("status") != "mine" and not ours.is_ours(r.get("user_id")):
            rows.append((r["tree_id"], "sighting", r["id"], (r.get("taken_at") or "")[:10], r.get("note") or ""))
    # submissions.tree is "lis_015 (Name)" from the app, the tree's name from a
    # web page (whose path names it), or the sighting's id for a tree a reader
    # added in the app (found_by_reader.sighting_id on the published tree).
    for r in inbox.get("/rest/v1/submissions?select=id,user_id,kind,tree,page,why,created_at&why=neq.", key):
        # A correction is an instruction to us ("the pin is wrong"), handled
        # on its own rung; it is not words for the page.
        if ours.is_ours(r.get("user_id")) or r.get("kind") == "correction" or "TEST ROW" in (r.get("why") or ""):
            continue
        tid = tree_of(r.get("tree") or "", r.get("page") or "")
        if tid:
            rows.append((tid, "submission " + (r.get("kind") or ""), r["id"],
                         (r.get("created_at") or "")[:10], r.get("why") or ""))
    return [r for r in rows + mailed() if len(words(r[4])) >= MIN_WORDS]


def mailed():
    """Rows for words that came by mail, from the private data/outreach-words.json."""
    try:
        doc = json.load(open(MAILED, encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return [(w["tree_id"], "mail", w["id"], w.get("date", ""), w.get("text") or "")
            for w in doc.get("words", []) if w.get("tree_id")]


_BY_PATH, _BY_SIGHTING = {}, {}


def tree_of(tree, page):
    m = re.match(r"([a-z]{2,4}_\d{3})\b", tree)
    if m:
        return m.group(1)
    if tree in _BY_SIGHTING:
        return _BY_SIGHTING[tree]
    return _BY_PATH.get(page.split("?")[0].rstrip("/"))


def index(trees):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from thin_pages import slugify
    for tid, (slug, t) in trees.items():
        _BY_PATH[f"/{slug}/{slugify(t['name'])}"] = tid
        sid = (t.get("found_by_reader") or {}).get("sighting_id")
        if sid:
            _BY_SIGHTING[str(sid).upper()] = tid
            _BY_SIGHTING[str(sid).lower()] = tid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--tree")
    ap.add_argument("--done", nargs=2, metavar=("ROW_ID", "WHY"))
    a = ap.parse_args()
    if a.done:
        d = done()
        d[str(a.done[0])] = a.done[1]
        json.dump(d, open(DONE, "w"), indent=1, ensure_ascii=False, sort_keys=True)
        print(f"{a.done[0]} marked done.")
        return 0
    handled = done()
    key = inbox.load_key()
    if not key:
        print("No SUPABASE_SERVICE_KEY (environment or ~/.ancienttrees-supabase.env).")
        return 1
    trees = live_trees()
    index(trees)
    todo = 0
    for tid, src, rid, day, text in sorted(notes(key), key=lambda r: (r[0], r[3])):
        if tid not in trees or (a.tree and tid != a.tree):
            continue
        slug, t = trees[tid]
        used = quoted(text, t.get("story")) or str(rid) in handled
        ascii_share = sum(c.isascii() for c in text) / max(len(text), 1)
        if used and not a.all:
            continue
        todo += not used
        flag = "on the page" if used else ("TO USE" + ("" if ascii_share > 0.97 else ", other language?"))
        print("=" * 72)
        print(f"{tid} ({slug}/{t['name']})  {src} {rid}  {day}  {len(words(text))} words  {flag}")
        for line in text.strip().splitlines():
            print("    " + line)
    print("=" * 72)
    print(f"{todo} note(s) whose words are not on their tree's page yet.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
