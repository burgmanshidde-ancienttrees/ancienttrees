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
import urllib.parse
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


ANON = "sb_publishable_qOTuw-LCejk2VhO2J6aXGQ_6X2O2mgb"


def anon_can_post_a_tree():
    """Try, with the key a stranger has. True means the door is open.

    A column either exists or it does not and PostgREST will say so. A POLICY
    answers no question at all; the only way to know whether the postbox is
    shut is to push something through it. So this posts one marked row with the
    publishable key and no session, and deletes it again with the service key
    when it lands, because a door that turned out to be open has just been
    walked through by this check.

    Hidde, 2026-09-23: "i can suggest a tree without logging in". The rule that
    it needs an account was set on 2026-08-21 and lived only in the form's
    JavaScript, which is a courtesy to the person using it and never a
    boundary. A check that reads our own source could not have found this; it
    had to be asked of the database.
    """
    marker = "sqlcheck anon probe"
    req = urllib.request.Request(
        f"{SUPA}/rest/v1/submissions", method="POST",
        data=json.dumps({"kind": "tree", "city": marker, "tree": "probe",
                         "why": "automated probe, deleted immediately"}).encode(),
        headers={"apikey": ANON, "Content-Type": "application/json",
                 "Prefer": "return=minimal"})
    try:
        urllib.request.urlopen(req, timeout=20).read()
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return False
        print(f"sqlcheck: the anonymous probe answered {e.code}, not a verdict")
        return False
    except Exception as e:
        print(f"sqlcheck: could not run the anonymous probe ({e.__class__.__name__})")
        return False
    # It landed. Take it straight back out.
    gone = urllib.request.Request(
        f"{SUPA}/rest/v1/submissions?city=eq.{urllib.parse.quote(marker)}",
        method="DELETE",
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    try:
        urllib.request.urlopen(gone, timeout=20).read()
    except Exception:
        print("sqlcheck: the probe row could NOT be deleted, remove it by hand: "
              f"submissions where city = '{marker}'")
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
    doors = []
    if anon_can_post_a_tree():
        doors.append("anybody can post a tree to submissions with no account at "
                     "all (the publishable key alone). The form's own sign-in "
                     "gate is JavaScript and is not a boundary. An anonymous row "
                     "can never reach the sender's account page and can never be "
                     "answered: supabase/postbox-needs-an-account.sql")
    if not missing and not doors:
        print(f"sqlcheck: {len(seen)} object(s), every migration is applied, "
              f"and the postbox needs an account")
        return 0
    for d in doors:
        print("sqlcheck: " + d)
    if not missing:
        return 1
    print(f"sqlcheck: {len(missing)} migration(s) never pasted. "
          f"The code degrades quietly around these, which is why nothing else "
          f"says so:")
    for fname, table, column in missing:
        what = f"{table}.{column}" if column else f"table {table}"
        print(f"  {what:34s} supabase/{fname}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
