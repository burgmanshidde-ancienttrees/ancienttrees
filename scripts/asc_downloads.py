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
    # ASK FOR EVERYTHING, THEN KEEP THE NEWEST (2026-10-02). With limit=14 the
    # endpoint returned the FIRST fourteen instances it holds, oldest first, and
    # the client-side sort below then ordered those fourteen: the newest day
    # this ever printed was 09-20, eleven days stale, and the digest read it as
    # Apple lagging. Apple was not lagging; we were reading the wrong end of
    # the list. 200 is the API's page maximum, and a daily report has one
    # instance per day, so this covers more than half a year before paging
    # would be needed.
    data = _get("%s/analyticsReports/%s/instances" % (API, report_id), token,
                params={"filter[granularity]": "DAILY", "limit": 200})
    rows = data.get("data", [])
    next_url = data.get("links", {}).get("next")
    while next_url:
        data = _get(next_url, token)
        rows += data.get("data", [])
        next_url = data.get("links", {}).get("next")
    rows.sort(key=lambda r: r["attributes"].get("processingDate") or "", reverse=True)
    return rows[:limit]


def _segment_rows(token, instance_id):
    data = _get("%s/analyticsReportInstances/%s/segments" % (API, instance_id), token)
    rows = []
    for seg in data.get("data", []):
        raw = _get_no_auth(seg["attributes"]["url"])
        text = gzip.decompress(raw).decode("utf-8")
        rows += list(csv.DictReader(io.StringIO(text), delimiter="\t"))
    return rows


def download_rows(days=14):
    """Every row of the daily report for the newest `days` instances, as
    (date, row) pairs, first-time downloads only. One fetch that both the
    daily table and the source table are derived from, so the digest does
    not walk Apple's segment chain twice for one block (2026-10-06)."""
    token = bearer_token()
    state = _load_state()
    request_id = _ensure_request(token, state)
    report_id = _ensure_report(token, state, request_id)
    instances = _daily_instances(token, report_id, limit=days)
    if not instances:
        return [], "no report instances yet (first one can take up to 48h " \
                   "after the request was created)"
    # Apple's daily instances OVERLAP: the one processed on the 10th carries
    # the 8th again beside the 9th. Keyed on the processing date and summed,
    # every download counted up to twice (found 2026-10-10: 34 in the window
    # where Apple's own rows hold 22). So rows are keyed on the row's own Date
    # and each day is taken from the NEWEST instance that carries it, which
    # is also the one Apple restates late arrivals into.
    newest = {}
    for inst in instances:
        processed = inst["attributes"].get("processingDate") or ""
        per_day = {}
        for row in _segment_rows(token, inst["id"]):
            if _download_type(row) in NEW_PERSON:
                day = _col(row, "date", default=processed)
                per_day.setdefault(day, []).append(row)
        for day, day_rows in per_day.items():
            if day not in newest or processed > newest[day][0]:
                newest[day] = (processed, day_rows)
    out = [(day, row) for day in sorted(newest) for row in newest[day][1]]
    return out, None


def _dedupe_selftest():
    """The overlap, in miniature: two instances both carrying the 8th."""
    a = {"Date": "2026-10-08", "Counts": "1", "Download Type": "First-time download"}
    b = {"Date": "2026-10-09", "Counts": "1", "Download Type": "First-time download"}
    newest = {}
    for processed, rows in (("2026-10-09", [a]), ("2026-10-10", [a, b])):
        per_day = {}
        for row in rows:
            per_day.setdefault(_col(row, "date"), []).append(row)
        for day, day_rows in per_day.items():
            if day not in newest or processed > newest[day][0]:
                newest[day] = (processed, day_rows)
    assert sum(_count(r) for d in newest for r in newest[d][1]) == 2


def _count(row):
    for k in row:
        if k.strip().lower() in ("counts", "count", "units"):
            try:
                return int(row[k])
            except (ValueError, TypeError):
                return 0
    return 0


def _col(row, name, default="unknown"):
    for k in row:
        if k.strip().lower() == name:
            v = str(row[k]).strip()
            return v or default
    return default


def split_by_type(rows):
    """{date: {"first-time download": n}} from download_rows() output."""
    split = {}
    for date, row in rows:
        bucket = split.setdefault(date, {})
        kind = _download_type(row)
        bucket[kind] = bucket.get(kind, 0) + _count(row)
    return split


def split_by_source(rows):
    """WHERE THE DOWNLOADS CAME FROM (2026-10-06), the question the week of
    the Google demotion could not answer: the site's own "get the app" button
    took 22 clicks in 14 days against 38 first-time downloads, so most people
    found the app some other way, and nothing here said which.

    Apple's App Downloads Standard report carries it per row: "Source Type"
    (App Store search, App Store browse, App referrer, Web referrer,
    Institutional purchase, Unavailable), "Source Info" (the referring
    domain or app, where there is one) and "Territory". Returns
    ({(source_type, source_info): n}, {territory: n}) over the whole window,
    first-time downloads only, same unit as the daily table. A row shape
    without the columns lands in "unknown" rather than being dropped."""
    sources, territories = {}, {}
    for _date, row in rows:
        n = _count(row)
        if not n:
            continue
        key = (_col(row, "source type"), _col(row, "source info", default="-"))
        sources[key] = sources.get(key, 0) + n
        t = _col(row, "territory")
        territories[t] = territories.get(t, 0) + n
    return sources, territories


def daily_downloads_by_type(days=14):
    """{date: {"first-time download": n}} per day.

    Split rather than summed since 2026-09-10, because the total could never
    be reconciled with the screen Hidde actually looks at. App Store Connect's
    Trends screen shows UNITS, which is first-time downloads only; we count a
    redownload as well, deliberately (see NEW_PERSON below: a returning person
    is a person). Both numbers are right and they will never match, so his own
    reading of the app was that ours was broken: 42 over six days here against
    22 over seven days there.

    A number nobody can reconcile with the source they can see gets distrusted,
    and the fix is the one this project uses everywhere, which is to say what
    the number is rather than to pick a side. The digest prints both, and the
    first-time column is the one that should equal Trends to the unit.
    """
    rows, note = download_rows(days)
    if note:
        return {}, note
    return split_by_type(rows), None


def daily_download_totals(days=14):
    """{date: downloads}, first-time only since 2026-10-02 (NEW_PERSON). Kept
    because it is the shape every caller before 2026-09-10 expects."""
    split, note = daily_downloads_by_type(days)
    if note:
        return {}, note
    return {d: sum(v.values()) for d, v in split.items()}, None


# AUTO-UPDATES ARE NOT DOWNLOADS, and summing every row said they were
# (2026-09-08). Hidde asked why Apple and PostHog disagreed so badly on how many
# people had the app, and this was most of the answer: the report carries a
# "Download Type" column and we were adding up all of it, so 09-06 read as 12
# when four people had actually arrived and seven existing phones had quietly
# updated themselves to 1.0.1 overnight. Across the first four days that turned
# 28 real arrivals into 38.
#
# The distinction is the whole point of the number. An update is a phone doing
# housekeeping and tells us nothing; a first-time download is a person who read
# the page and pressed the button, which is the only figure we have that counts
# somebody DECIDING rather than arriving. A redownload is a person too, and a
# returning one, so it counts.
# FIRST-TIME ONLY since 2026-10-02 (Hidde: "can you only count first time
# downloads please your number is way higher than what apple shows me"). A
# redownload used to count as a returning person; it also made every figure we
# printed disagree with the one screen he reads, and a number he cannot check
# against Apple is a number he cannot trust. First-time is Apple's Trends unit.
NEW_PERSON = ("first-time download",)


def _download_type(row):
    """Which kind of download this row is, lowercased.

    Absent column means an older or narrower report shape, and there the honest
    default is to count the row as a first-time download rather than silently
    drop the whole day.
    """
    for key in row:
        if key.strip().lower() == "download type":
            return str(row[key]).strip().lower()
    return "first-time download"


def source_lines(sources, territories, limit=8):
    """Digest-ready markdown for the source split; shared by the CLI and
    daily_digest.py so the two never print different tables."""
    out = []
    if not sources:
        return out
    total = sum(sources.values())
    out.append("")
    out.append("| Came from | Via | Downloads |")
    out.append("|---|---|---:|")
    ranked = sorted(sources.items(), key=lambda kv: (-kv[1], kv[0]))
    shown = 0
    for (kind, info), n in ranked[:limit]:
        out.append("| %s | %s | %d |" % (kind, info, n))
        shown += n
    if total > shown:
        out.append("| other | - | %d |" % (total - shown))
    out.append("| **window** | | **%d** |" % total)
    if territories:
        top = sorted(territories.items(), key=lambda kv: (-kv[1], kv[0]))[:6]
        out.append("- Countries: " + "; ".join("%s (%d)" % (t, n) for t, n in top))
    out.append("- Apple's own source split, first-time downloads only. \"Web referrer\" "
               "with our own domain is the site's app page; \"App Store search\" is "
               "somebody who typed into the store. \"Unavailable\" is Apple's word for "
               "a source it could not attribute.")
    return out


if __name__ == "__main__":
    rows, note = download_rows()
    if note:
        print(note)
    split = split_by_type(rows)
    print("%-12s %10s" % ("date", "downloads"))
    for date in sorted(split):
        print("%-12s %10d" % (date, split[date].get("first-time download", 0)))
    print("first-time downloads only, the unit App Store Connect's Trends screen counts.")
    sources, territories = split_by_source(rows)
    for line in source_lines(sources, territories):
        print(line)
