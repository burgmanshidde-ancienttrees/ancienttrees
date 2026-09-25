#!/usr/bin/env python3
"""The walks table does what supabase/walks.sql promises, tested against the live database.

Written 2026-09-26, the day the table went live, when this test found a stop
with no position getting through the check. It makes a throwaway account,
tries what a stranger and a broken client might try, and deletes the account.

    set -a; source ~/.ancienttrees-supabase.env; set +a
    python3 scripts/walks_rules_test.py
"""
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import account_delete_test as t
ANON = "sb_publishable_qOTuw-LCejk2VhO2J6aXGQ_6X2O2mgb"
def anon(path):
    r = urllib.request.Request(f"{t.BASE}/{path}")
    r.add_header("apikey", ANON)
    try:
        with urllib.request.urlopen(r, timeout=20) as x: return x.status, json.loads(x.read() or b"null")
    except urllib.error.HTTPError as e: return e.code, e.read().decode()[:160]

code, u = t.call("auth/v1/admin/users", "POST", {"email": t.TEST_EMAIL, "password": t.TEST_PASSWORD, "email_confirm": True})
uid = u["id"]; tok = t.sign_in()
ok = True
def check(label, cond):
    global ok; ok = ok and cond; print(("PASS " if cond else "FAIL ") + label)
try:
    ours = {"treeId": "ams_001", "lat": 52.37, "lng": 4.89, "name": "Ours"}
    mine = {"sightingId": "11111111-1111-1111-1111-111111111111", "lat": 52.1, "lng": 4.2, "name": "Mine"}
    c,_ = t.call("rest/v1/walks", "POST", [{"name": "Private", "stops": [ours]}], token=tok)
    check("own walk saves", 200 <= c < 300)
    c,_ = t.call("rest/v1/walks", "POST", [{"name": "Bad", "stops": [{**ours, "sightingId": mine["sightingId"]}]}], token=tok)
    check("stop with both ids refused (%s)" % c, c >= 400)
    c,_ = t.call("rest/v1/walks", "POST", [{"name": "Bad", "stops": [{"treeId": "x", "name": "no position"}]}], token=tok)
    check("stop without position refused (%s)" % c, c >= 400)
    c,_ = t.call("rest/v1/walks", "POST", [{"name": "  ", "stops": []}], token=tok)
    check("blank name refused (%s)" % c, c >= 400)
    c,_ = t.call("rest/v1/walks", "POST", [{"name": "Shared", "shared": True, "stops": [ours, mine], "shape": [[4.89, 52.37], [4.2, 52.1]]}], token=tok)
    check("shared walk saves", 200 <= c < 300)
    c, rows = anon("rest/v1/walks?select=*")
    check("stranger reads no walks from the table (%s, %s)" % (c, rows if not isinstance(rows, list) else len(rows)), c >= 400 or rows == [])
    c, rows = anon("rest/v1/shared_walks?select=*")
    names = [r["name"] for r in rows] if isinstance(rows, list) else rows
    check("stranger sees only the shared walk: %s" % names, isinstance(rows, list) and "Private" not in names and "Shared" in names)
    s = [r for r in rows if r["name"] == "Shared"][0]
    check("no user_id in the view", "user_id" not in s)
    check("our tree keeps its position", "lat" in s["stops"][0])
    check("your own tree loses its position", "lat" not in s["stops"][1] and "lng" not in s["stops"][1])
    check("route line hidden when it passes your own tree", s["shape"] is None)
finally:
    t.call(f"auth/v1/admin/users/{uid}", "DELETE")
    print("test account deleted, left behind:", len(t.call(f"rest/v1/walks?select=id&user_id=eq.{uid}")[1]))
sys.exit(0 if ok else 1)
