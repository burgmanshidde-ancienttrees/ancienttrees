#!/usr/bin/env python3
"""Which rows are ours rather than a reader's, in ONE place.

Written 2026-09-07, after Hidde spent a day in Nara testing the app and every
part of the pipeline treated him as a stranger. Three different things went
wrong at once and they all had the same cause: the digest knew his account and
nothing else did.

  - His own photograph of the Roben-sugi was queued as a reader's contribution
    and published as one.
  - The contributor mailer wrote to him about each of his own submissions
    ("i got a lot of emails with feedback").
  - Every sighting he made stood ready to enter the leads file as supply.

The digest has kept this list since 2026-09-02 and kept it privately, so the
two scripts that needed it most could not see it. The list now lives in
data/our-accounts.json and every script reads it here.

THE RULE THAT DOES NOT BEND: never add a stranger. Everything listed here is
subtracted from the only numbers on the page that are people rather than
traffic, so a wrong entry does not make a number slightly off, it deletes a
person from the record.
"""
import hashlib
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data", "our-accounts.json")


def hashes():
    """The sha1 set, or an empty set when the file is missing or unreadable.

    Empty fails OPEN into treating everybody as a reader, which is the safe
    direction: a run that cannot read this file over-counts us by a row or two
    and never silently deletes somebody's contribution.
    """
    try:
        with open(PATH) as fh:
            return {a["sha1"] for a in json.load(fh).get("accounts", []) if a.get("sha1")}
    except Exception:
        return set()


def is_ours(uid):
    """True when a row was made by us rather than by a reader."""
    if not uid:
        return False
    return hashlib.sha1(str(uid).encode()).hexdigest() in hashes()


# A Google query typed by us rather than a reader (2026-10-14). The /prague
# close-up (seo_diagnose.py, LOG.md "Prague's Google numbers are mostly ours")
# found its 294 impressions were `site:ancienttrees.app prague` from Hidde's
# phone and operator searches like `+"oldest" "pear" "on record" "park"` from
# research agents, and the digest had ranked it the one city Google still
# shows. A positive site:/inurl:/intitle: checks our own index; a query that
# starts with + or % (or carries +"...") is a research tool's syntax. A
# NEGATIVE operator (`quercus aggressive -site:reddit.com`) is a stranger
# narrowing their own search and stays theirs.
_OWN_QUERY = re.compile(
    r'(^|\s)(site|inurl|intitle|intext|allintitle|allinurl|allintext):'
    r'|^\s*[+%]'
    r'|(^|\s)\+["“]', re.I)


def own_search(query):
    """True when a Search Console query is our own looking, not demand."""
    return bool(query) and bool(_OWN_QUERY.search(query))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for u in sys.argv[1:]:
            print(f"{u}  sha1={hashlib.sha1(u.encode()).hexdigest()}  "
                  f"{'OURS' if is_ours(u) else 'a reader'}")
    else:
        print(f"{len(hashes())} account(s) recorded as ours in data/our-accounts.json")
