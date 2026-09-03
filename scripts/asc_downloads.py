"""asc_downloads.py - App Store download counts from the Analytics Reports API.

Read-only reporting gear, not a product dependency: see hard rule 5's "gear
for us" carve-out in CLAUDE.md. Auth is scripts/asc_auth.py, credentials are
~/.ancienttrees-appstoreconnect.env (never in this repo). Stdlib urllib only,
matching every other fetch in daily_digest.py; the one new dependency in this
pair of files is `cryptography`, in asc_auth.py, because ES256 JWT signing
has no stdlib path.

The Analytics Reports API is asynchronous and per-app rather than one call:
an ONGOING "report request" is created once, Apple attaches dozens of named
reports to it, each report has DAILY/WEEKLY instances that show up with a lag
(first instance can take up to ~48h after the request is created, per
Apple's own docs), and each instance's actual numbers live in one or more
gzipped TSV "segments" fetched from a signed URL. This module walks that
chain and caches the two ids that never change (the request, and the "App
Downloads Standard" report under it) in data/asc-report-ids.json so a normal
run does one GET instead of re-discovering the whole tree.

Created 2026-09-03: request id 61d9c707-7087-41ec-8171-423c761bf876, report
r3 "App Downloads Standard" (category COMMERCE). No instances existed yet at
creation time, which is expected for a brand-new request.
"""
import csv
import gzip
import io
import json
import os
import urllib.error
import urllib.parse
import urllib.request

from asc_auth import bearer_token

APP_ID = "6806177833"
API = "https://api.appstoreconnect.apple.com/v1"
STATE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "asc-report-ids.json")
REPORT_NAME = "App Downloads Standard"


def _get(url, token, params=None):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": "Bearer %s" % token})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def _post(url, token, body):
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": "Bearer %s" % token,
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def _get_no_auth(url):
    # Segment URLs are pre-signed; sending our own bearer token can make
    # the storage backend reject the request outright.
    with urllib.request.urlopen(url, timeout=30) as r:
        return r.read()


def _load_state():
    if os.path.isfile(STATE_PATH):
        with open(STATE_PATH) as f:
            return json.load(f)
    return {}


def _save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)
        f.write("\n")


def _ensure_request(token, state):
    if state.get("request_id"):
        return state["request_id"]
    data = _get("%s/apps/%s/analyticsReportRequests" % (API, APP_ID), token)
    for row in data.get("data", []):
        if row["attributes"].get("accessType") == "ONGOING":
            state["request_id"] = row["id"]
            _save_state(state)
            return row["id"]
    resp = _post("%s/analyticsReportRequests" % API, token,
                 {"data": {"type": "analyticsReportRequests",
                           "attributes": {"accessType": "ONGOING"},
                           "relationships": {"app": {"data": {"type": "apps", "id": APP_ID}}}}})
    req_id = resp["data"]["id"]
    state["request_id"] = req_id
    _save_state(state)
    return req_id


def _ensure_report(token, state, request_id):
    if state.get("report_id"):
        return state["report_id"]
    data = _get("%s/analyticsReportRequests/%s/reports" % (API, request_id),
                token, params={"limit": 50})
    reports = list(data.get("data", []))
    next_url = data.get("links", {}).get("next")
    while next_url:
        data = _get(next_url, token)
        reports += data.get("data", [])
        next_url = data.get("links", {}).get("next")
    for row in reports:
        if row["attributes"].get("name") == REPORT_NAME:
            state["report_id"] = row["id"]
            _save_state(state)
            return row["id"]
    raise SystemExit("No %r report found under request %s (Apple may not "
                      "have attached it yet)" % (REPORT_NAME, request_id))


def _daily_instances(token, report_id, limit=14):
    # No sort param: the endpoint 400s on "-processingDate" (not a
    # documented sortable field here), and the list is small enough that
    # sorting client-side after the fact is simpler than guessing at one
    # that works.
    data = _get("%s/analyticsReports/%s/instances" % (API, report_id), token,
                params={"filter[granularity]": "DAILY", "limit": limit})
    rows = data.get("data", [])
    rows.sort(key=lambda r: r["attributes"].get("processingDate") or "", reverse=True)
    return rows


def _segment_rows(token, instance_id):
    data = _get("%s/analyticsReportInstances/%s/segments" % (API, instance_id), token)
    rows = []
    for seg in data.get("data", []):
        raw = _get_no_auth(seg["attributes"]["url"])
        text = gzip.decompress(raw).decode("utf-8")
        rows += list(csv.DictReader(io.StringIO(text), delimiter="\t"))
    return rows


def daily_download_totals(days=14):
    """{date: total_downloads} for the most recent DAILY instances, newest
    Apple has processed first. Sums every numeric 'Counts'-style column
    across whatever breakdown columns the report carries (territory, device
    etc.), because the totals table wants one number per day, not a
    dimension the report happens to include this week."""
    token = bearer_token()
    state = _load_state()
    request_id = _ensure_request(token, state)
    report_id = _ensure_report(token, state, request_id)
    instances = _daily_instances(token, report_id, limit=days)
    if not instances:
        return {}, "no report instances yet (first one can take up to 48h " \
                    "after the request was created)"
    totals = {}
    for inst in instances:
        date = inst["attributes"].get("processingDate")
        rows = _segment_rows(token, inst["id"])
        count_col = None
        for row in rows:
            if count_col is None:
                for k in row:
                    if k.strip().lower() in ("counts", "count", "units"):
                        count_col = k
                        break
            if count_col:
                try:
                    totals[date] = totals.get(date, 0) + int(row[count_col])
                except (ValueError, TypeError):
                    pass
    return totals, None


if __name__ == "__main__":
    totals, note = daily_download_totals()
    if note:
        print(note)
    for date in sorted(totals):
        print(date, totals[date])
