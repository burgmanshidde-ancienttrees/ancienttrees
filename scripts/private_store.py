#!/usr/bin/env python3
"""The files that hold people's addresses, kept in Supabase instead of the
public repository.

Hidde, 2026-10-06: the GitHub repository is public, and data/outreach-*.json,
drafts/OUTREACH.md and drafts/batches/ carried 600+ email addresses of people
we wrote to, their replies and the waitlist. His answer: "What about
supabase", then "Yes". So those files stay exactly where every script already
reads them, git stops tracking them (.gitignore, MOVED below), and this script
moves them between disk and the private_files table (supabase/private-files.sql:
RLS on, no policy, service key only). No script had to learn a new path.

    python3 scripts/private_store.py pull    # Supabase -> disk
    python3 scripts/private_store.py push    # disk -> Supabase, merging
    python3 scripts/private_store.py sync    # both: push merged, then pull
    python3 scripts/private_store.py status  # what differs, both ways
    python3 scripts/private_store.py migrate # one-off: upload, untrack, gitignore

PULL FAILS LOUDLY, and it has to: the send scripts check data/outreach-sent.json before mailing anybody, so an empty pull would make every
address look new. A run that cannot pull must not send.

PUSH MERGES rather than overwrites when both sides changed a JSON file that
holds lists (outreach-sent.json above all): the night run and a session on the
Mac both append to it, and last-write-wins would lose a send and re-mail
somebody. Lists are unioned, keeping order, by their full JSON value.

The key comes from SUPABASE_SERVICE_KEY, or else ~/.ancienttrees-supabase.env.
"""
import glob
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPA = "https://caimvxiyrtifilimlkqw.supabase.co"
ENV_FILE = os.path.expanduser("~/.ancienttrees-supabase.env")

# What leaves the repository: every file that carries an address of a person
# we mailed. Paths are relative to ROOT and are the table's keys as they are.
MOVED = [
    "data/outreach-*.json",
    "data/ambassador-prospects.json",
    "data/research/outreach-contacts.json",
    "drafts/OUTREACH.md",
    "drafts/ambassador-prospects.md",
    "drafts/batches/*.json",
    "drafts/batch-*-preview.md",
    "drafts/batch-licence-asks.md",
    "drafts/backlinks-parks.md",
    "drafts/bomenstichting-permission.md",
    "drafts/catalonia-permission.md",
    "drafts/coimbra-jardim-botanico.md",
    "drafts/mail-paulo-link.md",
    "drafts/permission-us-registers.md",
    "drafts/reply-clara-visser-link.md",
    "drafts/woodland-trust-permission.md",
    "drafts/woodland-trust-reply.md",
    "drafts/app-review-2.1-reply.md",
    "drafts/app-review-notes-field.txt",
]


def key():
    k = os.environ.get("SUPABASE_SERVICE_KEY")
    if not k and os.path.exists(ENV_FILE):
        for line in open(ENV_FILE):
            if line.strip().startswith(("SUPABASE_SERVICE_KEY=", "export SUPABASE_SERVICE_KEY=")):
                k = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not k:
        sys.exit("private_store: no SUPABASE_SERVICE_KEY; nothing pulled, and nothing may be sent")
    return k


def req(path, method="GET", body=None, prefer=None):
    k = key()
    h = {"apikey": k, "Authorization": "Bearer " + k, "Content-Type": "application/json"}
    if prefer:
        h["Prefer"] = prefer
    r = urllib.request.Request(SUPA + path, method=method, headers=h,
                               data=json.dumps(body).encode() if body is not None else None)
    with urllib.request.urlopen(r, timeout=60) as resp:
        raw = resp.read()
    return json.loads(raw) if raw else None


def remote():
    out, start = {}, 0
    while True:
        rows = req(f"/rest/v1/private_files?select=path,content&order=path&offset={start}&limit=200") or []
        for r in rows:
            out[r["path"]] = r["content"]
        if len(rows) < 200:
            return out
        start += 200


def local():
    out = {}
    for pat in MOVED:
        for p in glob.glob(os.path.join(ROOT, pat)):
            if os.path.isfile(p):
                out[os.path.relpath(p, ROOT).replace(os.sep, "/")] = open(p, encoding="utf-8").read()
    return out


def _union(a, b):
    """b merged into a: lists unioned in order, dicts merged key by key."""
    if isinstance(a, list) and isinstance(b, list):
        seen = {json.dumps(x, sort_keys=True) for x in a}
        return a + [x for x in b if json.dumps(x, sort_keys=True) not in seen]
    if isinstance(a, dict) and isinstance(b, dict):
        out = dict(b)
        for k, v in a.items():
            out[k] = _union(v, b[k]) if k in b else v
        return out
    return a


def merged(path, mine, theirs):
    if mine == theirs or theirs is None:
        return mine
    if path.endswith(".json"):
        try:
            return json.dumps(_union(json.loads(mine), json.loads(theirs)), indent=1, ensure_ascii=False) + "\n"
        except ValueError:
            pass
    return mine


def pull():
    r = remote()
    if not r:
        sys.exit("private_store: the table is empty or unreachable; refusing to continue (no send may run)")
    for path, content in r.items():
        dest = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(content)
    print(f"private_store: pulled {len(r)} file(s)")


def push():
    mine, theirs = local(), remote()
    rows = []
    for path, content in mine.items():
        body = merged(path, content, theirs.get(path))
        if body != theirs.get(path):
            rows.append({"path": path, "content": body})
            if body != content:
                with open(os.path.join(ROOT, path), "w", encoding="utf-8") as fh:
                    fh.write(body)
    for i in range(0, len(rows), 50):
        req("/rest/v1/private_files?on_conflict=path", "POST",
            rows[i:i + 50],
            prefer="resolution=merge-duplicates,return=minimal")
    print(f"private_store: pushed {len(rows)} changed file(s)")


def migrated():
    """True once the files have left the repository (their patterns are in
    .gitignore); before that, nothing needs syncing."""
    gi = os.path.join(ROOT, ".gitignore")
    return os.path.exists(gi) and "data/outreach-*.json" in open(gi).read().split("\n")


def sync():
    """Both ways: what changed here goes up (merged with what changed there),
    then everything comes down. Safe on the Mac and in a run alike."""
    if local():
        push()
    pull()


def status():
    mine, theirs = local(), remote()
    for p in sorted(set(mine) | set(theirs)):
        if mine.get(p) != theirs.get(p):
            where = "only here" if p not in theirs else "only in Supabase" if p not in mine else "differs"
            print(f"  {where:16s} {p}")


def migrate():
    """One-off: upload every file in MOVED, stop tracking it, and gitignore
    the patterns. Nothing is deleted from disk. Refuses to untrack anything
    until the upload has landed, because an untracked file that never reached
    the table would exist only on this Mac."""
    push()
    have = remote()
    missing = [p for p in local() if p not in have]
    if missing:
        sys.exit(f"private_store: {len(missing)} file(s) did not reach the table; nothing untracked: {missing[:5]}")
    tracked = set(subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split())
    gone = [p for p in local() if p in tracked]
    for i in range(0, len(gone), 100):
        subprocess.run(["git", "rm", "-q", "--cached", *gone[i:i + 100]], cwd=ROOT, check=True)
    gi = os.path.join(ROOT, ".gitignore")
    text = open(gi).read() if os.path.exists(gi) else ""
    add = [p for p in MOVED if p not in text.split("\n")]
    if add:
        with open(gi, "a") as fh:
            fh.write("\n# People's addresses live in Supabase (scripts/private_store.py, 2026-10-06)\n" + "\n".join(add) + "\n")
    print(f"private_store: {len(gone)} file(s) untracked; they stay on disk and in Supabase")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    {"pull": pull, "push": push, "sync": sync, "status": status, "migrate": migrate}.get(cmd, status)()
