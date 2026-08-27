#!/usr/bin/env python3
"""account_delete_test.py - prove that deleting an account really deletes it.

This is the one item on RELEASE_CHECKLIST.md that cannot be waved through. It is
the condition Hidde set in July before accounts could be opened at all, it is
the promise the delete button makes in the app's own words, and Apple's review
tests it by tapping. Until today it had been designed and never proven.

    SUPABASE_SERVICE_KEY=... python3 scripts/account_delete_test.py

What it does, end to end, against the real database:

  1. makes a throwaway account with the admin API
  2. gives it everything an account can own: a save, a visit, a profile with a
     display name, an avatar image in the bucket, a follow, a block, a report
  3. signs in AS that account, so the token is a real user token
  4. calls delete_user() the way the app's own button does
  5. asks the service key what is left, table by table, and the bucket too

It cleans up after itself even when it fails, so a red run does not leave a test
account and a picture behind.

WHY A PASSWORD ACCOUNT. The app signs in by magic link, Apple or Google, none of
which a script can complete. The admin API can create a confirmed account with a
password, and a password sign-in returns the same kind of token the app holds,
so step 4 exercises the same path with the same permissions.
"""

import json
import os
import sys
import urllib.error
import urllib.request

BASE = "https://caimvxiyrtifilimlkqw.supabase.co"
KEY = os.environ.get("SUPABASE_SERVICE_KEY")
TEST_EMAIL = "delete-test@ancienttrees.app"
TEST_PASSWORD = "not-a-real-password-9f3a2b"


def call(path, method="GET", body=None, token=None, raw=None, content_type=None):
    url = f"{BASE}/{path}"
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("apikey", KEY)
    r.add_header("Authorization", f"Bearer {token or KEY}")
    if data is not None:
        r.add_header("Content-Type", content_type or "application/json")
    try:
        with urllib.request.urlopen(r, timeout=20) as resp:
            text = resp.read().decode()
            return resp.status, (json.loads(text) if text.strip().startswith(("{", "[")) else text)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def find_user():
    """The throwaway account, if a previous run left it behind."""
    code, rows = call(f"auth/v1/admin/users?per_page=200")
    if code != 200 or not isinstance(rows, dict):
        return None
    for u in rows.get("users", []):
        if u.get("email") == TEST_EMAIL:
            return u["id"]
    return None


def make_user():
    old = find_user()
    if old:
        call(f"auth/v1/admin/users/{old}", "DELETE")
    code, u = call("auth/v1/admin/users", "POST", {
        "email": TEST_EMAIL, "password": TEST_PASSWORD, "email_confirm": True})
    if code not in (200, 201):
        sys.exit(f"could not create the test account: {code} {u}")
    return u["id"]


def sign_in():
    code, s = call("auth/v1/token?grant_type=password", "POST",
                   {"email": TEST_EMAIL, "password": TEST_PASSWORD})
    if code != 200:
        sys.exit(f"could not sign in as the test account: {code} {s}")
    return s["access_token"]


def main():
    if not KEY:
        sys.exit("SUPABASE_SERVICE_KEY is not set. This test writes to the real "
                 "database, so it needs the service key in the environment.")

    print("making a throwaway account")
    uid = make_user()
    # A second account, so there is a follow and a block with somebody on the
    # other end of them. Reusing one account cannot test either.
    other = None
    code, u = call("auth/v1/admin/users", "POST", {
        "email": "delete-test-other@ancienttrees.app",
        "password": TEST_PASSWORD, "email_confirm": True})
    if code in (200, 201):
        other = u["id"]

    token = sign_in()
    print(f"  signed in as {uid}")

    print("giving it everything an account can own")
    made = {}
    made["saves"] = call("rest/v1/saves", "POST", [
        {"user_id": uid, "tree_id": "ams_001", "name": "Test", "url": "/x"}], token=token)[0]
    made["visited"] = call("rest/v1/visited", "POST", [
        {"user_id": uid, "tree_id": "ams_001"}], token=token)[0]
    made["profiles"] = call("rest/v1/profiles", "POST", [
        {"user_id": uid, "display_name": "Delete Test",
         "avatar_url": f"{BASE}/storage/v1/object/public/avatars/{uid}/avatar.jpg"}],
        token=token)[0]
    made["avatar file"] = call(f"storage/v1/object/avatars/{uid}/avatar.jpg", "POST",
                               raw=b"\xff\xd8\xff\xdb" + b"0" * 64, token=token,
                               content_type="image/jpeg")[0]
    if other:
        made["follows"] = call("rest/v1/follows", "POST", [
            {"follower": uid, "followee": other}], token=token)[0]
        made["blocks"] = call("rest/v1/blocks", "POST", [
            {"blocker": uid, "blocked": other}], token=token)[0]
        made["reports"] = call("rest/v1/reports", "POST", [
            {"reporter": uid, "subject": other, "reason": "test"}], token=token)[0]
    for k, v in made.items():
        print(f"  {k:12} {'made' if 200 <= v < 300 else 'FAILED ' + str(v)}")

    # EXACTLY WHAT THE APP DOES, in the same order: the picture through the
    # Storage API first, because SQL may not touch storage.objects, then the
    # account. A test that skipped the first step would pass while the app in
    # somebody's hand left their face in a public bucket.
    print("deleting the avatar through the Storage API, as the app does")
    code, out = call(f"storage/v1/object/avatars/{uid}/avatar.jpg", "DELETE", token=token)
    print(f"  {code} {'ok' if 200 <= code < 300 else out}")

    print("calling delete_user() with the account's own token, as the app does")
    code, out = call("rest/v1/rpc/delete_user", "POST", {}, token=token)
    print(f"  {code} {out if code >= 300 else 'ok'}")

    print("\nwhat is left")
    left = {}
    for table, col in [("saves", "user_id"), ("visited", "user_id"),
                       ("profiles", "user_id"), ("reports", "reporter")]:
        c, rows = call(f"rest/v1/{table}?select={col}&{col}=eq.{uid}")
        left[table] = len(rows) if isinstance(rows, list) else f"? {c}"
    if other:
        c, rows = call(f"rest/v1/follows?select=follower&follower=eq.{uid}")
        left["follows"] = len(rows) if isinstance(rows, list) else f"? {c}"
        c, rows = call(f"rest/v1/blocks?select=blocker&blocker=eq.{uid}")
        left["blocks"] = len(rows) if isinstance(rows, list) else f"? {c}"
    c, listing = call(f"storage/v1/object/list/avatars", "POST",
                      {"prefix": f"{uid}/", "limit": 10})
    left["avatar file"] = len(listing) if isinstance(listing, list) else f"? {c}"
    left["the account"] = 1 if find_user() else 0

    bad = False
    for k, v in left.items():
        ok = v == 0
        bad = bad or not ok
        print(f"  {k:14} {v}   {'gone' if ok else 'STILL THERE'}")

    # Clean up whatever survived, and the second account, so a red run leaves
    # nothing behind for the next one to trip over.
    for u in (find_user(), other):
        if u:
            call(f"auth/v1/admin/users/{u}", "DELETE")

    print()
    if bad:
        print("DELETION IS NOT COMPLETE. Everything marked STILL THERE outlives "
              "the account, and the delete button in the app promises it does not.")
        sys.exit(1)
    print("Deleting the account took everything with it, the avatar file included.")


if __name__ == "__main__":
    main()
