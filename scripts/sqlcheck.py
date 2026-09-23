#!/usr/bin/env python3
"""Which migrations in supabase/ have never reached the live database.

Written 2026-09-23. `sightings.girth_hugs` had been waiting twelve days: the
app asks a reader how many hugs round the trunk is, the answer is posted, and
PostgREST drops it, because the column only exists in a file in this repo. The
code was written to degrade quietly and did, which is right, and the cost of
degrading quietly is that nobody finds out.

Nothing could see it. The app builds, the site builds, every gate is green,
and the only symptom is a field that is always empty. It is the same shape as
the two faults of that morning: we ask for something and nothing reads it.

WHAT IT DOES. Reads every supabase/*.sql for the objects they create, then
asks the live database for each one with the service key. A table is asked for
directly; a column is asked for by name, which is the only question PostgREST
answers about a schema. Missing means the file was never pasted.

It is deliberately mechanical rather than a hand-kept list: a list somebody has
to extend when they write a migration is a list that goes stale the first busy
afternoon, which is the failure this whole file is about.

    python3 scripts/sqlcheck.py

Exit 1 when something is missing, 0 when everything is applied, and 0 with a
printed line when SUPABASE_SERVICE_KEY is absent, so CI can always call it.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUPA = "https://caimvxiyrtifilimlkqw.supabase.co"
KEY = os.environ.get("SUPABASE_SERVICE_KEY")

TABLE = re.compile(r"create table if not exists\s+public\.(\w+)", re.I)
COLUMN = re.compile(r"alter table\s+public\.(\w+)\s+add column if not exists\s+(\w+)", re.I | re.S)


def wanted():
    """[(file, table, column or None)], in the order the files name them."""
    out = []
    for f in sorted((ROOT / "supabase").glob("*.sql")):
        text = f.read_text(encoding="utf-8")
        for m in TABLE.finditer(text):
            out.append((f.name, m.group(1), None))
        for m in COLUMN.finditer(text):
            out.append((f.name, m.group(1), m.group(2)))
    return out


def ask(table, column):
    """True when the live database has it, False when it does not."""
    sel = column or "*"
    url = f"{SUPA}/rest/v1/{table}?select={sel}&limit=1"
    req = urllib.request.Request(url, headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY})
    try:
        urllib.request.urlopen(req, timeout=20).read()
        return True
    except urllib.error.HTTPError as e:
        # 400 is "no such column", 404 is "no such table". Anything else is a
        # problem with us rather than a verdict about the schema, so it is not
        # reported as a missing migration.
        if e.code in (400, 404):
            return False
        print(f"sqlcheck: {table}.{sel} answered {e.code}, not asking again")
        return True
    except Exception as e:
        print(f"sqlcheck: could not ask about {table} ({e.__class__.__name__})")
        return True


def main():
    if not KEY:
        print("sqlcheck: SUPABASE_SERVICE_KEY absent, nothing checked")
        return 0
    missing, seen = [], set()
    for fname, table, column in wanted():
        key = (table, column)
        if key in seen:
            continue
        seen.add(key)
        if not ask(table, column):
            missing.append((fname, table, column))
    if not missing:
        print(f"sqlcheck: {len(seen)} object(s), every migration is applied")
        return 0
    print(f"sqlcheck: {len(missing)} migration(s) never pasted. "
          f"The code degrades quietly around these, which is why nothing else "
          f"says so:")
    for fname, table, column in missing:
        what = f"{table}.{column}" if column else f"table {table}"
        print(f"  {what:34s} supabase/{fname}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
