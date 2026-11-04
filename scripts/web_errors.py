#!/usr/bin/env python3
"""What breaks on the website, grouped so a person can read it.

    python3 scripts/web_errors.py           every error type of the last 8 days
    python3 scripts/web_errors.py --light   only the quality line's verdict
    python3 scripts/web_errors.py --prune   delete rows past 90 days and test rows
                                            (daily, data-digest.yml)

Every page posts its script errors to the Supabase `web_errors` table
(site/src/lib/web-errors-js.ts, supabase/web-errors.sql; Hidde, 2026-11-04,
the digest's quality line). This is the reader, with the service key
(SUPABASE_SERVICE_KEY, or ~/.ancienttrees-supabase.env, as crashes.py).

A TYPE is the message plus the script it came from. The last 24 hours are
read against the seven days before them:
  red     a type not seen in those seven days, on 3+ pages or 5+ reports in
          the last 24 hours (a new fault spreading): rung-2 work
  orange  any other new type
  green   nothing new (known types still firing are listed, not lit)
  grey    the table is not there yet, or no key
A row holds no visitor id, so "visitors" is counted as reports; the page
caps itself at three a load, which keeps one visitor from looking like five.

PRIVACY: a row holds a message, a file and line, a path, a browser family and
a build. Nothing here prints anything else, and nothing about a person exists
to print.
"""
import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inbox import SUPA, load_key  # noqa: E402

RED_PAGES = 3
RED_REPORTS = 5
KEEP_DAYS = 90  # the privacy promise in supabase/web-errors.sql and CLAUDE.md


def fetch(key, days=8):
    """Rows of the last `days` days, or raises. 404 means no table yet."""
    since = (datetime.datetime.now(datetime.timezone.utc)
             - datetime.timedelta(days=days)).isoformat()
    q = ("/rest/v1/web_errors?select=message,source,line,path,browser,build,created_at"
         "&created_at=gte." + urllib.parse.quote(since) + "&order=created_at.desc&limit=5000")
    req = urllib.request.Request(SUPA + q, headers={"apikey": key, "Authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def _when(iso):
    return datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))


def group(rows, now=None):
    """One dict per type: last-24h reports and pages, the week before, newest."""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    cut = now - datetime.timedelta(hours=24)
    types = {}
    for r in rows:
        k = (r.get("message") or "", r.get("source") or "")
        t = types.setdefault(k, {"message": k[0], "source": k[1], "day": 0, "pages": set(),
                                 "before": 0, "browsers": set(), "last": ""})
        when = _when(r["created_at"])
        if when >= cut:
            t["day"] += 1
            t["pages"].add(r.get("path") or "")
        else:
            t["before"] += 1
        t["browsers"].add(r.get("browser") or "")
        t["last"] = max(t["last"], r["created_at"])
    out = list(types.values())
    for t in out:
        t["new"] = t["day"] > 0 and t["before"] == 0
        t["spreading"] = t["new"] and (len(t["pages"]) >= RED_PAGES or t["day"] >= RED_REPORTS)
    out.sort(key=lambda t: (-t["spreading"], -t["new"], -t["day"], -t["before"]))
    return out


def light():
    """(colour, reason) for the quality line's Web "Live" cell."""
    key = load_key()
    if not key:
        return "grey", "no database key here"
    try:
        rows = fetch(key)
    except urllib.error.HTTPError as e:
        if e.code in (404, 400):
            return "grey", "web errors not connected yet (paste supabase/web-errors.sql)"
        return "grey", "error table unreadable (HTTP %d)" % e.code
    except Exception as e:
        return "grey", "error table unreadable (%s)" % str(e)[:60]
    types = group(rows)
    spreading = [t for t in types if t["spreading"]]
    new = [t for t in types if t["new"]]
    if spreading:
        t = spreading[0]
        return "red", "new error spreading: \"%s\" in %s, %d reports on %d pages" % (
            t["message"][:60], t["source"] or "?", t["day"], len(t["pages"]))
    if new:
        t = new[0]
        return "orange", "%d new error type(s), first \"%s\" in %s" % (
            len(new), t["message"][:60], t["source"] or "?")
    firing = sum(1 for t in types if t["day"])
    return "green", ("no new errors" + (", %d known type(s) still firing" % firing if firing else ""))


def delete(key, where):
    """DELETE rows matching a PostgREST filter; returns how many went."""
    req = urllib.request.Request(SUPA + "/rest/v1/web_errors?" + where, method="DELETE",
                                 headers={"apikey": key, "Authorization": "Bearer " + key,
                                          "Prefer": "return=representation"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return len(json.load(r))


def prune(key):
    """Rows older than KEEP_DAYS go, and any row a test left (message starts TEST web_errors)."""
    cut = (datetime.datetime.now(datetime.timezone.utc)
           - datetime.timedelta(days=KEEP_DAYS)).isoformat()
    old = delete(key, "created_at=lt." + urllib.parse.quote(cut))
    tests = delete(key, "message=like." + urllib.parse.quote("TEST web_errors*"))
    return old, tests


def main():
    if "--prune" in sys.argv:
        key = load_key()
        if not key:
            print("web_errors: SUPABASE_SERVICE_KEY not set")
            return 1
        try:
            old, tests = prune(key)
        except urllib.error.HTTPError as e:
            print("web_errors: prune failed (HTTP %d)" % e.code)
            return 1
        print("web_errors: removed %d row(s) older than %d days, %d test row(s)" % (old, KEEP_DAYS, tests))
        return 0
    if "--light" in sys.argv:
        print("%s: %s" % light())
        return 0
    key = load_key()
    if not key:
        print("web_errors: SUPABASE_SERVICE_KEY not set")
        return 1
    try:
        rows = fetch(key)
    except urllib.error.HTTPError as e:
        print("web_errors: the table is not there yet (HTTP %d); paste supabase/web-errors.sql" % e.code)
        return 1
    types = group(rows)
    if not types:
        print("web_errors: no errors in the last 8 days")
        return 0
    print("%-6s %5s %5s %6s  %-28s %s" % ("", "24h", "pages", "before", "source", "message"))
    for t in types:
        tag = "RED" if t["spreading"] else ("new" if t["new"] else "")
        print("%-6s %5d %5d %6d  %-28s %s" % (tag, t["day"], len(t["pages"]), t["before"],
                                              t["source"][:28], t["message"][:90]))
    print("\n%s: %s" % light())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
