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

LIGHT ON EGRESS (2026-11-13, Supabase mailed that the free plan's 5 GB a month
was passed; Hidde: "fix maar"). The table is 6.4 MB of JSON, and the night run
read it whole four times a knock (two pulls, two pushes that each read the
remote first), about 160 MB a day, half of all our egress. Now every request
asks for gzip (1.2 MB on the wire instead of 5.8), a pull leaves a snapshot of
what it fetched (out/private-store-pulled.json, hashes only), and a push reads
back only the files that changed on disk since that snapshot, so a push after
a run that mailed nobody reads nothing. Without a snapshot it reads all, as before.
"""
import glob
import gzip
import hashlib
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
    # 2026-11-03: dated mail drafts that carried an address, caught by qa when
    # Hidde said "push alle uncommited stuff"
    "drafts/lisbon-ten-mails.md",
    "drafts/lisbon-ten.md",
    "drafts/mail-pamplona-belasko-2026-10-29.md",
    "drafts/northern-woodlands-2026-10-28.md",
    "drafts/reply-fred-van-holland-2026-10-27.md",
    "drafts/reply-james-kearney-2026-10-2*.md",
    "drafts/reply-jerry-bull-2026-1*.md",
    "drafts/reply-john-beetham-2026-10-24.md",
    "drafts/reply-john-beetham-2026-10-25.md",
    "drafts/reply-laura-parrack-2026-10-27.md",
    "drafts/reply-luisa-carta-2026-10-25.md",
    "drafts/reply-michael-roe-cammo-2026-11-0*.md",
    "drafts/reply-miguel-portugal-icnf-2026-10-27.md",
    "drafts/reply-mikel-belasko-2026-10-29.md",
    "drafts/reply-paulo-calvos-2026-10-2*.md",
    "drafts/reply-pere-vives-amicsjbb-2026-11-01.md",
    "drafts/reply-pere-vives-photos-2026-11-02.md",
    "drafts/reply-sjaan-openbomenkaart-2026-10-31.md",
    "drafts/reply-tatiana-verona-ferrara-2026-11-03.md",
    "drafts/reply-veronika-willhalm-*2026-11-0*.md",
]


def key():
    # The Mac's own key file wins over the environment: ~/.ancienttrees-mail.env
    # also exports a SUPABASE_SERVICE_KEY, an older one that Supabase refuses
    # (401, found 2026-10-07), and sourcing it before a send shadowed this one.
    k = None
    if os.path.exists(ENV_FILE):
        for line in open(ENV_FILE):
            if line.strip().startswith(("SUPABASE_SERVICE_KEY=", "export SUPABASE_SERVICE_KEY=")):
                k = line.split("=", 1)[1].strip().strip('"').strip("'")
    k = k or os.environ.get("SUPABASE_SERVICE_KEY")
    if not k:
        sys.exit("private_store: no SUPABASE_SERVICE_KEY; nothing pulled, and nothing may be sent")
    return k


def req(path, method="GET", body=None, prefer=None):
    k = key()
    h = {"apikey": k, "Authorization": "Bearer " + k, "Content-Type": "application/json",
         "Accept-Encoding": "gzip"}
    if prefer:
        h["Prefer"] = prefer
    r = urllib.request.Request(SUPA + path, method=method, headers=h,
                               data=json.dumps(body).encode() if body is not None else None)
    with urllib.request.urlopen(r, timeout=60) as resp:
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
    return json.loads(raw) if raw else None


def remote(paths=None):
    """Every file in the table, or only `paths` (those that exist there)."""
    out = {}
    if paths is not None:
        paths = sorted(paths)
        for i in range(0, len(paths), 40):
            chunk = ",".join('"%s"' % p.replace('"', '\\"') for p in paths[i:i + 40])
            q = urllib.parse.quote("in.(" + chunk + ")", safe="")
            for r in req(f"/rest/v1/private_files?select=path,content&path={q}") or []:
                out[r["path"]] = r["content"]
        return out
    start = 0
    while True:
        rows = req(f"/rest/v1/private_files?select=path,content&order=path&offset={start}&limit=200") or []
        for r in rows:
            out[r["path"]] = r["content"]
        if len(rows) < 200:
            return out
        start += 200


SNAPSHOT = os.path.join(ROOT, "out", "private-store-pulled.json")


def _hash(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def _snapshot():
    try:
        return json.load(open(SNAPSHOT))
    except (OSError, ValueError):
        return None


def _save_snapshot(snap):
    os.makedirs(os.path.dirname(SNAPSHOT), exist_ok=True)
    with open(SNAPSHOT, "w") as fh:
        json.dump(snap, fh)


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


def _merge_batch(mine, theirs):
    """A draft batch is EDITED, not appended to, so the local copy wins
    outright. 2026-10-09, twice in one afternoon: first the list union
    re-added an edited reply's old wording beside the new one, then a
    merge-by-address re-added a mail that had been MOVED to another batch,
    and that mail went out a second time. Removing a mail from a batch has
    to stick, and only replacing the whole file does that."""
    return mine


def merged(path, mine, theirs):
    if mine == theirs or theirs is None:
        return mine
    if path.endswith(".json"):
        try:
            a, b = json.loads(mine), json.loads(theirs)
            if path.startswith("drafts/batches/") and isinstance(a, dict) and isinstance(b, dict):
                return json.dumps(_merge_batch(a, b), indent=1, ensure_ascii=False) + "\n"
            return json.dumps(_union(a, b), indent=1, ensure_ascii=False) + "\n"
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
    _save_snapshot({p: _hash(c) for p, c in r.items()})
    print(f"private_store: pulled {len(r)} file(s)")


def push():
    mine, snap = local(), _snapshot()
    if snap is None:
        theirs = remote()
    else:
        # Only what changed on disk since the last pull can need writing.
        mine = {p: c for p, c in mine.items() if snap.get(p) != _hash(c)}
        theirs = remote(mine.keys()) if mine else {}
    rows, on_disk = [], {}
    for path, content in mine.items():
        body = merged(path, content, theirs.get(path))
        on_disk[path] = content
        if body != theirs.get(path):
            rows.append({"path": path, "content": body})
            if body != content:
                with open(os.path.join(ROOT, path), "w", encoding="utf-8") as fh:
                    fh.write(body)
                on_disk[path] = body
    for i in range(0, len(rows), 50):
        req("/rest/v1/private_files?on_conflict=path", "POST",
            rows[i:i + 50],
            prefer="resolution=merge-duplicates,return=minimal")
    if snap is not None and on_disk:
        snap.update({p: _hash(c) for p, c in on_disk.items()})
        _save_snapshot(snap)
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
