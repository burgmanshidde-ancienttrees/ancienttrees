#!/usr/bin/env python3
"""Notes from visitors (supabase/tree-notes.sql): what the night run reads.

A note goes live for everyone the moment it is written (Hidde, 2026-10-24:
"zet gewoon live en we kunnen altijd wegmodereren later"), so somebody has to
read them afterwards. This is that reader.

  python3 scripts/tree_notes.py --new            every note not yet read, with the tree
  python3 scripts/tree_notes.py --seen           mark everything printed by --new as read
  python3 scripts/tree_notes.py --hide <code> <tree_id> "<why>"
                                                 take one down (hidden=true; the person
                                                 still sees and can edit their own)
  python3 scripts/tree_notes.py --show <code> <tree_id>
                                                 put it back
  python3 scripts/tree_notes.py --count          one line for the digest

Needs SUPABASE_SERVICE_KEY. What has been read is in data/notes-seen.json as
(code, tree_id, updated_at): codes, never ids (scripts/people.py), and never
the text, which stays in Supabase. A note is taken down for the closed list
only: a person's name or address, abuse, an instruction that harms the tree
(CLAUDE.md, Stories), spam. A wrong fact is answered on the page, never
deleted: readers correct us too.
"""
import datetime
import json
import os
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import people  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPA = "https://caimvxiyrtifilimlkqw.supabase.co"
KEY = os.environ.get("SUPABASE_SERVICE_KEY")
SEEN = os.path.join(ROOT, "data", "notes-seen.json")


def supa(path, method="GET", body=None):
    h = {"apikey": KEY, "Authorization": "Bearer " + KEY}
    data = None
    if body is not None:
        h["Content-Type"] = "application/json"
        h["Prefer"] = "return=minimal"
        data = json.dumps(body).encode()
    req = urllib.request.Request(SUPA + path, data=data, method=method, headers=h)
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
        return json.loads(raw) if raw else None


def load_seen():
    try:
        return json.load(open(SEEN, encoding="utf-8"))
    except Exception:
        return {"_note": "Visitor notes the night run has read: (code, tree_id) -> updated_at. "
                         "Codes, never ids; the words stay in Supabase.", "seen": {}}


def save_seen(doc):
    with open(SEEN, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def tree_names():
    out = {}
    import glob
    for fp in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
        try:
            c = json.load(open(fp, encoding="utf-8"))
        except Exception:
            continue
        for t in c.get("trees", []):
            out[t.get("id")] = (t.get("name"), c.get("city"))
    return out


def rows():
    return supa("/rest/v1/tree_notes?select=user_id,tree_id,body,hidden,created_at,updated_at"
                "&order=updated_at.desc&limit=500") or []


def new(mark=False):
    doc = load_seen()
    seen = doc.setdefault("seen", {})
    names = tree_names()
    fresh = []
    for r in rows():
        k = f"{people.ref(r['user_id'])}|{r['tree_id']}"
        if seen.get(k) == r["updated_at"]:
            continue
        fresh.append((k, r))
    if not fresh:
        print("tree notes: nothing new")
        return 0
    print(f"tree notes: {len(fresh)} new or changed")
    for k, r in fresh:
        name, city = names.get(r["tree_id"], (r["tree_id"], "?"))
        flag = " HIDDEN" if r.get("hidden") else ""
        print(f"\n  {k}  {r['updated_at'][:10]}  {name} ({city}){flag}")
        print("    " + (r["body"] or "").replace("\n", "\n    "))
        if mark:
            seen[k] = r["updated_at"]
    if mark:
        save_seen(doc)
    return 0


def set_hidden(code, tree_id, hidden, why=""):
    uid = people.uid(code)
    if not uid:
        print(f"tree notes: no account behind code {code}")
        return 1
    q = f"/rest/v1/tree_notes?user_id=eq.{uid}&tree_id=eq.{urllib.parse.quote(tree_id)}"
    supa(q, "PATCH", {"hidden": hidden})
    doc = load_seen()
    doc.setdefault("taken_down", []).append({"code": code, "tree_id": tree_id, "hidden": hidden,
                                             "why": why[:200], "on": datetime.date.today().isoformat()})
    save_seen(doc)
    print(f"tree notes: {code} on {tree_id} {'hidden' if hidden else 'shown again'}")
    return 0


def count():
    r = rows()
    live = [x for x in r if not x.get("hidden")]
    print(f"{len(live)} visitor note(s) live, {len(r) - len(live)} taken down")
    return 0


def main():
    if not KEY:
        print("tree notes: SUPABASE_SERVICE_KEY absent, nothing read")
        return 0
    a = sys.argv[1:]
    if "--new" in a:
        return new(mark="--seen" in a)
    if "--seen" in a:
        return new(mark=True)
    if "--hide" in a:
        i = a.index("--hide")
        return set_hidden(a[i + 1], a[i + 2], True, a[i + 3] if len(a) > i + 3 else "")
    if "--show" in a:
        i = a.index("--show")
        return set_hidden(a[i + 1], a[i + 2], False)
    if "--count" in a:
        return count()
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
