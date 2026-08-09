#!/usr/bin/env python3
"""Daily data digest: writes one dated entry per day into DATA.md.

Sources:
- Cloudflare zone analytics (GraphQL API), token from CLOUDFLARE_ANALYTICS_TOKEN.
- Search Console via OAuth refresh token (GSC_CLIENT_ID / GSC_CLIENT_SECRET /
  GSC_REFRESH_TOKEN), authorised by Hidde 2026-07-27. Data lags 2-3 days.

Stdlib only (hard rule 5). Safe to run twice a day: the second run is a no-op.
"""
import datetime
import glob
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_MD = os.path.join(ROOT, "DATA.md")
ZONE_NAME = "ancienttrees.app"
ACCOUNT_TAG = "949aa102070e5f296c9cc0d5bc1e1891"  # Cloudflare account for Web Analytics (RUM)

PREAMBLE = """# DATA — the daily numbers, and what they mean

One entry per day, newest first, written automatically by the data-digest
workflow. Numbers are for the previous UTC day. While volume is tiny the
conclusion says so plainly; noise is never narrated as trend (Hidde's
standing rule, 2026-07-27).
"""


def api(url, payload=None, token=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode() if payload else None,
        headers={
            "Authorization": "Bearer %s" % token,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch_gsc(today):
    """Return (day_rows, top_queries, top_pages) from Search Console, or None
    if the three GSC_* secrets are absent. Data lags 2-3 days; we report the
    freshest rows Google provides and say which date they are."""
    cid = os.environ.get("GSC_CLIENT_ID")
    csec = os.environ.get("GSC_CLIENT_SECRET")
    rtok = os.environ.get("GSC_REFRESH_TOKEN")
    if not (cid and csec and rtok):
        return None
    body = urllib.parse.urlencode({
        "client_id": cid, "client_secret": csec,
        "refresh_token": rtok, "grant_type": "refresh_token",
    }).encode()
    with urllib.request.urlopen("https://oauth2.googleapis.com/token", body, timeout=30) as r:
        access = json.load(r)["access_token"]

    def q(payload):
        req = urllib.request.Request(
            "https://www.googleapis.com/webmasters/v3/sites/sc-domain%3Aancienttrees.app/searchAnalytics/query",
            data=json.dumps(payload).encode(),
            headers={"Authorization": "Bearer " + access, "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r).get("rows", [])

    start = (today - datetime.timedelta(days=10)).isoformat()
    end = today.isoformat()
    days = q({"startDate": start, "endDate": end, "dimensions": ["date"], "dataState": "all"})
    queries = q({"startDate": start, "endDate": end, "dimensions": ["query"], "rowLimit": 5, "dataState": "all"})
    pages = q({"startDate": start, "endDate": end, "dimensions": ["page"], "rowLimit": 5, "dataState": "all"})
    # Wider pull for the content-gap line below: the top 5 by clicks are
    # almost always queries we already rank for, so finding one with no page
    # needs a bigger pool to pick the highest-impression miss out of.
    gap_queries = q({"startDate": start, "endDate": end, "dimensions": ["query"],
                      "rowLimit": 25, "dataState": "all"})
    # Page and query crossed, which the separate pulls above cannot tell you.
    # /rome takes 165 impressions and 2 clicks while /lisbon takes 104 and 7,
    # and no amount of page data or query data alone says why. The pair does:
    # a page seen a lot and clicked rarely is either ranking for the wrong
    # question or showing the wrong snippet, and those need opposite fixes.
    pairs = q({"startDate": start, "endDate": end, "dimensions": ["page", "query"],
               "rowLimit": 200, "dataState": "all"})
    return days, queries, pages, gap_queries, pairs


def known_terms():
    """Every city, country and species name a rendered page already covers.
    Used to spot a Search Console query with no matching page (PRODUCT_TODO.md
    item 1, 2026-07-31): a deterministic string match, not a page build, so a
    miss here is a lead, not an action. Deliberately excludes collection
    titles: their words ("trees", "ancient", "with") are generic enough to
    false-match almost any query on this site and would swallow real gaps."""
    terms = set()
    for path in glob.glob(os.path.join(ROOT, "data/cities/*.json")):
        d = json.load(open(path))
        terms.add(d.get("city", "").lower())
        terms.add(d.get("country", "").lower())
        # Tree pages too. On 2026-08-07/08 'den brandt park' was reported as a
        # gap two days running while Antwerp's "The Park Trees of Den Brandt"
        # was live: the detector knew cities, countries, species and standing
        # pages, and had never heard of the trees themselves. Same failure
        # class as the 'ancient tree map' false positive below, so per the
        # ratchet it becomes code. Add each tree's full name and, for the
        # common "The X of Y" shape, the distinctive part after the last
        # " of ", which is what a searcher actually types.
        # A few "of Y" tails are generic English nouns ("...Cathedral of
        # Trees", "...Tree of Science") that would swallow almost any query;
        # everything that generic is skipped, everything distinctive kept.
        generic = {"trees", "tree", "science", "battles", "venus"}
        for t in d.get("trees", []):
            name = t.get("name", "").lower()
            if not name:
                continue
            terms.add(name.removeprefix("the ").strip())
            if " of " in name:
                tail = name.rsplit(" of ", 1)[1].strip()
                if tail not in generic:
                    terms.add(tail)
    for path in glob.glob(os.path.join(ROOT, "data/countries/*.json")):
        d = json.load(open(path))
        terms.add(d.get("country", "").lower())
    for path in glob.glob(os.path.join(ROOT, "data/species/*.json")):
        d = json.load(open(path))
        terms.add(d.get("common_name", "").lower())
    # The standing pages, which have no data file behind them and were therefore
    # invisible here. On 2026-08-06 this reported "ancient tree map" as a gap
    # while /explore carried exactly that title and H1, and a session nearly
    # built a page that already existed. A lead that names something we have is
    # worse than no lead: it sends work at a solved problem.
    terms.update({"ancient tree map", "ancient trees", "ancient tree", "tree map", "map", "explore", "collections",
                  "species", "cities", "countries", "in season", "contribute",
                  "suggest a tree", "about", "privacy", "app"})
    return {t for t in terms if t}


def find_content_gap(gap_queries):
    """The top-impression query (10d) whose text matches no known city, country,
    species or standing page: a content lead, the kind that found us before we
    had a page for it ("albero roma"). A query that matches a page we already
    have is not a gap, it is a ranking problem, and those two need opposite
    responses: one is a page to write, the other is a page to strengthen."""
    terms = known_terms()
    misses = [r for r in gap_queries
              if not any(t in r["keys"][0].lower() for t in terms if len(t) > 2)]
    if not misses:
        return None
    return max(misses, key=lambda r: r["impressions"])


def gsc_section(gsc):
    if gsc is None:
        return ("Search Console: GSC_* secrets not configured; section skipped.", None)
    days, queries, pages, gap_queries, pairs = gsc
    days = [d for d in days if d.get("impressions") or d.get("clicks")]
    if not days:
        return ("Search Console: connected, but Google returned no rows for the window.", None)
    latest = days[-1]
    prev = days[-2] if len(days) > 1 else None
    trend = "  ".join("%s:c%d/i%d" % (d["keys"][0][5:], d["clicks"], d["impressions"]) for d in days)
    gap = find_content_gap(gap_queries)
    gap_line = (
        "- Content lead: %r has no matching page (i%d, p%.0f)" % (
            clean_query(gap["keys"][0]), gap["impressions"], gap["position"])
        if gap else "- Content lead: none of the top 25 queries lack a matching page"
    )
    # The pages Google shows most and visitors click least, with what those
    # impressions are actually for. Ranked by wasted impressions rather than by
    # volume, because that is the number a fix would move.
    seen = {}
    for r in pairs:
        page, query = r["keys"][0], r["keys"][1]
        d = seen.setdefault(page, {"imp": 0, "clicks": 0, "q": []})
        d["imp"] += r["impressions"]
        d["clicks"] += r["clicks"]
        d["q"].append((r["impressions"], query, r.get("position", 0)))
    leaks = sorted((v["imp"] - v["clicks"] * 20, p, v) for p, v in seen.items()
                   if v["imp"] >= 20 and v["clicks"] * 100 < v["imp"] * 3)
    leak_lines = []
    for _, page, v in sorted(leaks, key=lambda t: -t[2]["imp"])[:3]:
        top = "; ".join("%s (i%d, p%.0f)" % (clean_query(qq), i, pos)
                        for i, qq, pos in sorted(v["q"], reverse=True)[:3])
        leak_lines.append("- Seen, not clicked: %s (c%d/i%d, %.1f%%) for %s" % (
            page.replace("https://ancienttrees.app", ""), v["clicks"], v["imp"],
            v["clicks"] * 100.0 / max(v["imp"], 1), top))

    lines = [
        "Search Console (freshest day Google provides, data lags 2-3 days):",
        "- %s: %d clicks, %d impressions, avg position %.1f%s" % (
            latest["keys"][0], latest["clicks"], latest["impressions"], latest["position"],
            (" (day before: c%d/i%d)" % (prev["clicks"], prev["impressions"])) if prev else ""),
        "- Days: %s" % trend,
        "- Top queries (10d): " + "; ".join(
            "%s (i%d, p%.0f)" % (clean_query(r["keys"][0]), r["impressions"], r["position"]) for r in queries) if queries else "- Top queries: none",
        "- Top pages (10d): " + "; ".join(
            "%s (c%d/i%d)" % (r["keys"][0].replace("https://ancienttrees.app", ""), r["clicks"], r["impressions"]) for r in pages) if pages else "- Top pages: none",
        gap_line,
        *leak_lines,
    ]
    return "\n".join(lines), {"clicks": latest["clicks"], "impressions": latest["impressions"],
                               "prev_clicks": prev["clicks"] if prev else 0,
                               "prev_impressions": prev["impressions"] if prev else 0}


def clean_query(q):
    """Search Console hands back whatever the visitor typed, operators and
    all. A query like `quercus aggressive -site:reddit.com -s` is a real
    search someone ran, not a parsing bug, but the operators say nothing
    about us; strip them so the digest reports the term (weekly analysis,
    2026-08-02, suggestion 3)."""
    import re as _re
    q = _re.sub(r"-?\bsite:\S+", "", q)
    q = _re.sub(r"(^|\s)-\S*", " ", q)
    return " ".join(q.split())[:40] or "(operators only)"


def fetch_cloudflare(token, today):
    """Return list of per-day dicts for the last 8 days, oldest first."""
    zones = api(
        "https://api.cloudflare.com/client/v4/zones?name=" + ZONE_NAME,
        token=token,
    )
    if not zones.get("success") or not zones.get("result"):
        raise RuntimeError("cannot list zone: %s" % json.dumps(zones.get("errors")))
    tag = zones["result"][0]["id"]

    query = {
        "query": """
query($tag: String!, $since: String!, $until: String!) {
  viewer { zones(filter: {zoneTag: $tag}) {
    httpRequests1dGroups(limit: 10, filter: {date_geq: $since, date_lt: $until},
                         orderBy: [date_ASC]) {
      dimensions { date }
      sum { requests pageViews countryMap { clientCountryName requests } }
      uniq { uniques }
    } } }
}""",
        "variables": {
            "tag": tag,
            "since": (today - datetime.timedelta(days=8)).isoformat(),
            "until": today.isoformat(),
        },
    }
    g = api("https://api.cloudflare.com/client/v4/graphql", query, token=token)
    if g.get("errors"):
        raise RuntimeError("graphql: %s" % json.dumps(g["errors"]))
    return g["data"]["viewer"]["zones"][0]["httpRequests1dGroups"]


def fetch_rum(token, today):
    """Cookieless Web Analytics (beacon) numbers: real browser visits, no bots.
    Returns text; never raises past itself."""
    q = {
        "query": """
query($tag: String!, $since: Date!, $until: Date!) {
  viewer { accounts(filter: {accountTag: $tag}) {
    days: rumPageloadEventsAdaptiveGroups(limit: 10,
        filter: {date_geq: $since, date_lt: $until}, orderBy: [date_ASC]) {
      count dimensions { date } sum { visits }
    }
    paths: rumPageloadEventsAdaptiveGroups(limit: 5,
        filter: {date_geq: $since, date_lt: $until}, orderBy: [count_DESC]) {
      count dimensions { requestPath }
    }
    refs: rumPageloadEventsAdaptiveGroups(limit: 5,
        filter: {date_geq: $since, date_lt: $until}, orderBy: [count_DESC]) {
      count dimensions { refererHost }
    }
    countries: rumPageloadEventsAdaptiveGroups(limit: 5,
        filter: {date_geq: $since, date_lt: $until}, orderBy: [count_DESC]) {
      count dimensions { countryName }
    }
    devices: rumPageloadEventsAdaptiveGroups(limit: 3,
        filter: {date_geq: $since, date_lt: $until}, orderBy: [count_DESC]) {
      count dimensions { deviceType }
    }
    perf: rumPerformanceEventsAdaptiveGroups(limit: 1,
        filter: {date_geq: $since, date_lt: $until}) {
      quantiles { pageLoadTimeP50 pageLoadTimeP90 }
    }
  } }
}""",
        "variables": {"tag": ACCOUNT_TAG,
                      "since": (today - datetime.timedelta(days=8)).isoformat(),
                      "until": today.isoformat()},
    }
    g = api("https://api.cloudflare.com/client/v4/graphql", q, token=token)
    if g.get("errors"):
        raise RuntimeError("rum graphql: %s" % json.dumps(g["errors"]))
    acct = g["data"]["viewer"]["accounts"]
    if not acct:
        return "Web Analytics (beacon): no account data visible to this token."
    days, paths = acct[0]["days"], acct[0]["paths"]
    refs = acct[0].get("refs") or []
    countries = acct[0].get("countries") or []
    devices = acct[0].get("devices") or []
    if not days:
        return "Web Analytics (beacon): live since 2026-07-27, no visits recorded yet."
    trend = "  ".join("%s:v%d/p%d" % (d["dimensions"]["date"][5:], d["sum"]["visits"], d["count"]) for d in days)
    top = "; ".join("%s (%d)" % (p["dimensions"]["requestPath"], p["count"]) for p in paths)
    def _dim(rows, key, skip=("", None)):
        out = []
        for r in rows:
            v = r["dimensions"].get(key)
            if v in skip:
                v = "(direct)" if key == "refererHost" else "(unknown)"
            out.append("%s (%d)" % (v, r["count"]))
        return "; ".join(out) if out else "none recorded"
    perf = acct[0].get("perf") or []
    speed = ""
    if perf and perf[0].get("quantiles"):
        qq = perf[0]["quantiles"]
        # Cloudflare's RUM returns page load time in MICROseconds. We printed
        # it as milliseconds for weeks, so the dashboard read "p50 519000ms",
        # which is eight and a half minutes and would mean the site never
        # loads. Nobody flinched, which is the point: CLAUDE.md already tells
        # us to sanity-check every numeric field against the physical world,
        # and that rule was written for other people's registers rather than
        # for our own dashboard.
        speed = "\n- Page load (8d): p50 %dms, p90 %dms" % (
            (qq.get("pageLoadTimeP50") or 0) / 1000,
            (qq.get("pageLoadTimeP90") or 0) / 1000)
    return ("Web Analytics (beacon, real browsers, cookieless):\n"
            "- Days (visits/pageviews): %s\n- Top paths: %s\n"
            "- Referrers: %s\n- Countries: %s\n- Devices: %s%s"
            % (trend, top, _dim(refs, "refererHost"),
               _dim(countries, "countryName"), _dim(devices, "deviceType"), speed)
            + "\n\n" + referrers_section(refs))


# Hosts that are us, or a search engine sending us traffic we already measure
# in Search Console. Neither is a link somebody chose to give us.
NOT_A_BACKLINK = (
    "ancienttrees.app", "google.", "bing.", "duckduckgo.", "ecosia.",
    "yandex.", "baidu.", "search.brave.", "startpage.", "qwant.",
)


def referrers_section(refs):
    """The external referrers, which is the closest thing to a backlink report
    we can automate.

    Google's Search Console API has no links endpoint at all: the Links report
    exists only in the web interface, confirmed 2026-08-07. So the number of
    sites linking to us cannot be pulled here, and the digest says so and links
    straight to the report rather than pretending otherwise.

    What this line does measure is better in one way and worse in another: a
    referrer is a link somebody actually followed, which is traffic rather than
    an index entry, but it only sees links that get clicked."""
    external = []
    for r in refs or []:
        host = (r["dimensions"].get("refererHost") or "").lower()
        if not host or any(b in host for b in NOT_A_BACKLINK):
            continue
        external.append("%s (%d)" % (host, r["count"]))
    line = "; ".join(external) if external else "none yet"
    return ("Links and referrers:\n"
            "- External referrers (a link somebody clicked): %s\n"
            "- Backlink count: not automatable, Search Console's API has no links "
            "endpoint. Read it by hand at "
            "https://search.google.com/search-console/links?resource_id=sc-domain%%3Aancienttrees.app"
            % line)


def fetch_events(today):
    """Anonymous action counts from the site's own events table (Supabase,
    insert-only from the site; read here with the service key). Absent key or
    table: one quiet line, never an error."""
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not key:
        return None
    since = (today - datetime.timedelta(days=1)).isoformat()
    url = ("https://caimvxiyrtifilimlkqw.supabase.co/rest/v1/events"
           "?select=name&created_at=gte.%sT00:00:00Z&created_at=lt.%sT00:00:00Z"
           % (since, today.isoformat()))
    req = urllib.request.Request(url, headers={
        "apikey": key, "Authorization": "Bearer " + key})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            rows = json.load(r)
    except Exception as e:
        return "Site actions: events table unreadable (%s)." % e
    if not rows:
        line = "Site actions (yesterday): none recorded."
    else:
        counts = {}
        for row in rows:
            counts[row["name"]] = counts.get(row["name"], 0) + 1
        line = "Site actions (yesterday): " + "; ".join(
            "%s %d" % (k, v) for k, v in sorted(counts.items(), key=lambda kv: -kv[1]))
    # Waitlist total: a fortnight-review criterion (2026-08-14, "whether a
    # single waitlist signup exists"), so the digest states it daily. Count
    # only, never the addresses.
    try:
        req = urllib.request.Request(
            "https://caimvxiyrtifilimlkqw.supabase.co/rest/v1/waitlist?select=id",
            headers={"apikey": key, "Authorization": "Bearer " + key,
                     "Prefer": "count=exact", "Range": "0-0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            total = (r.headers.get("Content-Range") or "/0").split("/")[-1]
        line += "\nWaitlist signups (total): %s." % total
    except Exception:
        pass
    return line


def fetch_machine(today):
    """Chain utilization from the GitHub Actions API: attempts vs runs that got
    real work time. Answers Hidde's standing question (2026-07-28) whether his
    subscription's windows actually get used."""
    tok = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY", "burgmanshidde-ancienttrees/ancienttrees")
    if not tok:
        return None
    yday = (today - datetime.timedelta(days=1)).isoformat()
    req = urllib.request.Request(
        "https://api.github.com/repos/%s/actions/workflows/nightly.yml/runs?per_page=100&created=%s..%s" % (repo, yday, yday),
        headers={"Authorization": "Bearer " + tok, "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        runs = json.load(r).get("workflow_runs", [])
    total, worked, minutes = len(runs), 0, 0
    for run in runs:
        try:
            a = datetime.datetime.fromisoformat(run["run_started_at"].replace("Z", "+00:00"))
            b = datetime.datetime.fromisoformat(run["updated_at"].replace("Z", "+00:00"))
            dur = (b - a).total_seconds()
        except Exception:
            dur = 0
        if dur > 150:
            worked += 1
            minutes += int(dur // 60)
    line = ("Machine: %d chain attempts yesterday, %d got real work time (~%d min "
            "total). Dead-in-seconds attempts cost nothing; few get-throughs means "
            "the usage window was full or closed." % (total, worked, minutes))

    # Cron watchdog (2026-07-30, after review.yml and data-digest.yml both
    # silently skipped their morning slots): GitHub drops schedules without a
    # trace, so every scheduled workflow is checked for a run in the last 26h.
    # A missed cron becomes a visible line instead of a discovery.
    quiet = []
    for wf, label in (("review.yml", "fresh-eyes review"),
                      ("data-digest.yml", "data digest"),
                      ("nightly.yml", "research chain")):
        try:
            req2 = urllib.request.Request(
                "https://api.github.com/repos/%s/actions/workflows/%s/runs?per_page=1" % (repo, wf),
                headers={"Authorization": "Bearer " + tok, "Accept": "application/vnd.github+json"})
            with urllib.request.urlopen(req2, timeout=30) as r:
                latest = json.load(r).get("workflow_runs", [])
            if not latest:
                quiet.append(label + " (never ran)")
                continue
            started = datetime.datetime.fromisoformat(
                latest[0]["created_at"].replace("Z", "+00:00"))
            age = datetime.datetime.now(datetime.timezone.utc) - started
            if age.total_seconds() > 26 * 3600:
                quiet.append("%s (last ran %dh ago)" % (label, int(age.total_seconds() // 3600)))
        except Exception:
            quiet.append(label + " (status unreadable)")
    if quiet:
        line += ("\nWATCHDOG: scheduled workflows silent past their slot: "
                 + "; ".join(quiet) + ". Kick with `gh workflow run <file>` and "
                 "treat a repeat as rung 2.")
    return line


def build_entry(days, today, gsc_text):
    yday = today - datetime.timedelta(days=1)
    by_date = {d["dimensions"]["date"]: d for d in days}
    y = by_date.get(yday.isoformat())
    b = by_date.get((yday - datetime.timedelta(days=1)).isoformat())

    def n(day, *path):
        cur = day
        for p in path:
            if cur is None:
                return 0
            cur = cur.get(p)
        return cur or 0

    y_views, y_uniq, y_req = n(y, "sum", "pageViews"), n(y, "uniq", "uniques"), n(y, "sum", "requests")
    b_views, b_uniq = n(b, "sum", "pageViews"), n(b, "uniq", "uniques")

    def delta(cur, prev):
        d = cur - prev
        return "%+d" % d if prev or cur else "0"

    trend = "  ".join(
        "%s:%d" % (d["dimensions"]["date"][5:], n(d, "sum", "pageViews")) for d in days
    ) or "no data"

    countries = {}
    for c in (n(y, "sum", "countryMap") or []) if y else []:
        countries[c["clientCountryName"]] = c["requests"]
    top = sorted(countries.items(), key=lambda kv: -kv[1])[:5]
    top_line = ", ".join("%s %d" % kv for kv in top) or "none recorded"

    week_uniques = sum(n(d, "uniq", "uniques") for d in days)
    if y_uniq < 100:
        conclusion = (
            "Volume is still noise-level (%d unique visitors yesterday, %d over the "
            "window): direction is not readable and no strategic conclusion should "
            "be drawn from these numbers yet." % (y_uniq, week_uniques)
        )
    else:
        half = len(days) // 2
        first = sum(n(d, "uniq", "uniques") for d in days[:half]) or 1
        second = sum(n(d, "uniq", "uniques") for d in days[half:])
        conclusion = (
            "Second half of the window vs first: %d vs %d unique visitors "
            "(%+.0f%%). A run reading this should replace this templated line "
            "with a sharper one when something real happens." % (second, first, 100.0 * (second - first) / first)
        )

    # The zone block is structurally zero and always will be: it counts
    # requests through Cloudflare's proxy, and this site's DNS lives at the
    # registrar so no request ever passes through it (the "Invalid
    # nameservers" notice in the dashboard is the same fact). Printed only
    # when a number actually appears, so the report stops carrying a
    # guaranteed zero every day (weekly analysis, 2026-08-02).
    zone_block = ""
    if y_req or y_views or y_uniq:
        zone_block = """Cloudflare zone (proxied traffic), %s:
- Page views: %d (day before: %d, %s)
- Unique visitors: %d (day before: %d, %s)
- Requests total: %d
- Page views, last days: %s
- Top countries by requests: %s

""" % (ZONE_NAME,
       y_views, b_views, delta(y_views, b_views),
       y_uniq, b_uniq, delta(y_uniq, b_uniq),
       y_req, trend, top_line)

    return """## %s (previous UTC day)

%s%s

**Conclusion:** %s
""" % (yday.isoformat(), zone_block, gsc_text, conclusion)


def main():
    token = os.environ.get("CLOUDFLARE_ANALYTICS_TOKEN")
    if not token:
        print("SKIP: CLOUDFLARE_ANALYTICS_TOKEN not set")
        return 0

    today = datetime.datetime.now(datetime.timezone.utc).date()
    yday = yesterday_header = "## %s" % (today - datetime.timedelta(days=1)).isoformat()

    existing = ""
    if os.path.exists(DATA_MD):
        with open(DATA_MD) as f:
            existing = f.read()
    if yesterday_header in existing:
        print("Entry for %s already present, nothing to do" % yday)
        return 0

    try:
        days = fetch_cloudflare(token, today)
    except (RuntimeError, urllib.error.URLError, KeyError) as e:
        print("SKIP: Cloudflare fetch failed: %s" % e)
        return 1

    gsc_latest = None
    try:
        gsc_text, gsc_latest = gsc_section(fetch_gsc(today))
    except Exception as e:  # GSC failure must never kill the Cloudflare half
        gsc_text = "Search Console: fetch failed today (%s); numbers resume tomorrow." % e

    try:
        gsc_text += "\n\n" + fetch_rum(token, today)
    except Exception as e:
        gsc_text += "\n\nWeb Analytics (beacon): fetch failed today (%s)." % e

    try:
        ev = fetch_events(today)
        if ev:
            gsc_text += "\n\n" + ev
        m = fetch_machine(today)
        if m:
            gsc_text += "\n\n" + m
    except Exception as e:
        gsc_text += "\n\nMachine utilization: fetch failed today (%s)." % e

    entry = build_entry(days, today, gsc_text)
    # While the CF zone is dormant (domain not proxied), its zeros must not drive
    # the conclusion. If search data exists, it replaces the conclusion line.
    if gsc_latest is not None:
        c, i = gsc_latest["clicks"], gsc_latest["impressions"]
        pc, pi = gsc_latest["prev_clicks"], gsc_latest["prev_impressions"]
        if i < 1000:
            concl = ("Search is the only channel with real data and it is still small: "
                     "%d clicks and %d impressions on Google's freshest day (day before: c%d/i%d). "
                     "Directional at best; no strategic conclusions from these volumes." % (c, i, pc, pi))
        else:
            concl = ("Google's freshest day: %d clicks, %d impressions (day before: c%d/i%d). "
                     "Volumes are past noise; a run should replace this line with an actual "
                     "reading of what moved." % (c, i, pc, pi))
        import re as _re
        entry = _re.sub(r"\*\*Conclusion:\*\* .*\n", "**Conclusion:** %s\n" % concl, entry)
    body = existing[len(PREAMBLE):] if existing.startswith(PREAMBLE) else (
        "\n" + existing if existing else ""
    )
    with open(DATA_MD, "w") as f:
        f.write(PREAMBLE + "\n" + entry + body)
    print("Wrote digest entry to DATA.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
