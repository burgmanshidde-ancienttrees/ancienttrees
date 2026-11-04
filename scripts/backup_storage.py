"""Copy every file in the Supabase storage buckets to a local folder, for the
weekly database backup (.github/workflows/db-backup.yml).

Hidde, 2026-11-04: the free Supabase plan keeps no backup we can restore, and
accounts, saves, readers' photos and notes live only there ("ok lets do option
1"). The database itself is dumped with pg_dump; this is the other half, the
files: avatars and readers' photographs.

    python3 scripts/backup_storage.py <out-dir>

Needs SUPABASE_SERVICE_KEY. Prints counts only, never a path or a name.
"""
import json
import os
import sys
import urllib.parse
import urllib.request

URL = "https://caimvxiyrtifilimlkqw.supabase.co"
BUCKETS = ["avatars", "sightings"]
KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")


def req(path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(URL + path, data=data, method="POST" if data else "GET",
                               headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
                                        "Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=60) as resp:
        return resp.read()


def walk(bucket, prefix=""):
    """Every object path under prefix. A folder comes back with id null."""
    offset = 0
    while True:
        rows = json.loads(req(f"/storage/v1/object/list/{bucket}",
                              {"prefix": prefix, "limit": 1000, "offset": offset,
                               "sortBy": {"column": "name", "order": "asc"}}))
        for r in rows:
            path = (prefix + "/" + r["name"]).lstrip("/")
            if r.get("id") is None:
                yield from walk(bucket, path)
            else:
                yield path
        if len(rows) < 1000:
            return
        offset += 1000


def main(out):
    if not KEY:
        sys.exit("backup_storage: no SUPABASE_SERVICE_KEY")
    total = 0
    for b in BUCKETS:
        n = 0
        for path in walk(b):
            dst = os.path.join(out, b, path)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            quoted = urllib.parse.quote(path)
            with open(dst, "wb") as fh:
                fh.write(req(f"/storage/v1/object/authenticated/{b}/{quoted}"))
            n += 1
        print(f"backup_storage: {b}: {n} file(s)")
        total += n
    print(f"backup_storage: {total} file(s) in all")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "backup-storage")
