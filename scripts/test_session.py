#!/usr/bin/env python3
"""A real session for the app's UI tests, on the test account (2026-11-08).

Hidde, after Discover's ambassador seat ignored his tap and every app test
turned out to run signed out or on a fake session that cannot write: "waarom
testen we in Gods naam alleen uitgelogd", then "Ja" to a test account in our
own database. This is the only door to it.

In CI (needs SUPABASE_SERVICE_KEY):
  1. make sure the account apptest@ancienttrees.app exists (confirmed, no mail);
  2. give it a fresh random password, so no password is ever stored anywhere;
  3. sign in with that password and print the session the app reads from
     AT_TEST_SESSION: "access|refresh|userId|email";
  4. keep its profile private, so it never shows up as a person to follow.

    python3 scripts/test_session.py            # prints the session line
    python3 scripts/test_session.py --ours     # prints the line for data/our-accounts.json

The account is OURS (data/our-accounts.json): the digest, the inbox and every
count leave it out. It is never a reader, and nothing it does is a reader's.
"""
import hashlib
import json
import os
import secrets
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inbox import SUPA  # noqa: E402

EMAIL = "apptest@ancienttrees.app"


def call(method, path, key, body=None):
    req = urllib.request.Request(SUPA + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None)
    req.add_header("apikey", key)
    req.add_header("Authorization", "Bearer " + key)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, raw.decode(errors="replace")[:200]


def find_user(key):
    page = 1
    while page < 50:
        st, d = call("GET", "/auth/v1/admin/users?per_page=200&page=%d" % page, key)
        if st != 200:
            sys.exit("could not list accounts: %s" % st)
        users = d.get("users", []) if isinstance(d, dict) else d
        for u in users:
            if (u.get("email") or "").lower() == EMAIL:
                return u["id"]
        if len(users) < 200:
            return None
        page += 1
    return None


def main():
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not key:
        sys.exit("SUPABASE_SERVICE_KEY is not set: no test session")
    password = secrets.token_urlsafe(24)
    uid = find_user(key)
    if uid is None:
        st, d = call("POST", "/auth/v1/admin/users", key,
                     {"email": EMAIL, "password": password, "email_confirm": True})
        if st not in (200, 201):
            sys.exit("could not create the test account: %s %s" % (st, d))
        uid = d["id"]
    else:
        st, d = call("PUT", "/auth/v1/admin/users/" + uid, key, {"password": password})
        if st != 200:
            sys.exit("could not reset the test password: %s %s" % (st, d))

    if "--ours" in sys.argv:
        import people
        print(json.dumps({"sha1": hashlib.sha1(uid.encode()).hexdigest(),
                          "who": "apptest, the app's UI-test account (scripts/test_session.py)",
                          "ref": people.ref(uid, key)}))
        return

    # Private, so the test account is never suggested or listed as a person.
    call("PATCH", "/rest/v1/profiles?id=eq." + uid, key, {"public": False})

    st, d = call("POST", "/auth/v1/token?grant_type=password", key,
                 {"email": EMAIL, "password": password})
    if st != 200 or not isinstance(d, dict) or "access_token" not in d:
        sys.exit("could not sign the test account in: %s" % st)
    print("%s|%s|%s|%s" % (d["access_token"], d["refresh_token"], uid, EMAIL))


if __name__ == "__main__":
    main()
