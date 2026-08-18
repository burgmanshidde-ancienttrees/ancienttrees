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
    # Every page, not the top 5 and no longer the top 200. The five best pages
    # tell you where the wins are; the depth rule (CLAUDE.md, 2026-08-12:
    # photos, pins and best_time only on pages with impressions) needs the
    # opposite question answered, which is whether a given page has ANY demand.
    # With a top-5 pull a run asking "does Vienna get impressions" could not
    # tell, and the honest default under a rule like that is to do nothing. The
    # night run holds no Search Console credentials (they live in this workflow
    # and weekly-analysis only), so this file is the only place it can read the
    # answer.
    #
    # Raised from 200 to 5,000 on 2026-08-16, because 200 was quietly answering
    # a different question than everything downstream believed. This API sorts
    # by CLICKS descending, and the whole site takes about 90 clicks in a
    # window, so roughly 40 pages have any clicks at all and the remaining 160
    # slots went to zero-click pages in an order Google does not promise. Every
    # page past that cut was written into data/city-queue.json as
    # `impressions_10d: 0`, which reads as "nobody searched for this" when it
    # actually meant "did not make the top 200 rows".
    #
    # It was self-evidently wrong in this file's own output: the 2026-08-16
    # digest printed /cambridge/newtons-apple-tree at 22 impressions in its
    # seen-not-clicked line (that line reads the `pairs` pull) and wrote
    # cambridge = 0 impressions into the queue in the same run. promote() then
    # scores a city on that number and rescore.py ranks on it, so a truncated
    # readback was steering which cities get worked on next.
    #
    # 5,000 covers all 1,626 URLs with headroom; the API's ceiling is 25,000.
    # Same class of fault as the sendBeacon bug fixed on 2026-08-15: the
    # instrument read zero and nothing about a zero looked broken.
    pages = q({"startDate": start, "endDate": end, "dimensions": ["page"], "rowLimit": 5000, "dataState": "all"})
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
    # 1,000 rather than 200 since 2026-08-18. This pull now feeds the depth
    # table's "where does it really rank" column as well as the seen-not-clicked
    # line, and at 200 rows sorted by clicks the low-click cities that column
    # exists to diagnose, Palermo and Bath among them, were exactly the ones
    # falling off the end.
    pairs = q({"startDate": start, "endDate": end, "dimensions": ["page", "query"],
               "rowLimit": 1000, "dataState": "all"})
    return days, queries, pages, gap_queries, pairs


# The industry CTR-by-position curve, rounded from the public studies that
# agree with each other (Advanced Web Ranking, Sistrix, Backlinko). It exists
# so a CTR can be read against what its RANK already predicts: 2% at position
# 11 is normal and 2% at position 3 is a broken snippet, and the same number
# means opposite things.
CTR_CURVE = {1: 28.0, 2: 15.0, 3: 11.0, 4: 8.0, 5: 7.0, 6: 5.0, 7: 4.0,
             8: 3.5, 9: 3.0, 10: 2.5, 12: 1.8, 15: 1.2, 20: 0.8, 30: 0.4}


def expected_ctr(pos):
    """What a result at this average position normally earns, in percent."""
    if pos <= 0:
        return 0.0
    keys = sorted(CTR_CURVE)
    if pos <= keys[0]:
        return CTR_CURVE[keys[0]]
    if pos >= keys[-1]:
        return CTR_CURVE[keys[-1]]
    for a, b in zip(keys, keys[1:]):
        if a <= pos <= b:
            t = (pos - a) / (b - a)
            return CTR_CURVE[a] + t * (CTR_CURVE[b] - CTR_CURVE[a])
    return 0.0


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


def demand_lines(pages, pairs=None):
    """Every page with real demand, as a table, so the depth rule has a list.

    CLAUDE.md sends photo, pin and best_time work only to pages Search Console
    shows impressions for. That rule needs a roster rather than a top five, and
    a run cannot query Search Console itself. Threshold at 10 impressions over
    the ten-day window: below that a page is one person scrolling past, and
    treating it as demand would make the rule mean nothing. Cities only, since
    depth work is per city; a tree page's impressions count toward its city."""
    if not pages:
        return []
    by_city = {}
    for r in pages:
        path = r["keys"][0].replace("https://ancienttrees.app", "").strip("/")
        if not path:
            continue
        city = path.split("/")[0]
        if city in ("app", "explore", "cities", "contribute", "privacy", "account",
                    "species", "collections", "countries", "parks"):
            continue
        c, i, wp = by_city.get(city, (0, 0, 0.0))
        by_city[city] = (c + r["clicks"], i + r["impressions"],
                         wp + r.get("position", 0) * r["impressions"])
    rows = sorted(((c, v[0], v[1], (v[2] / v[1]) if v[1] else 0)
                   for c, v in by_city.items()), key=lambda x: -x[2])
    rows = [r for r in rows if r[2] >= 10]
    if not rows:
        return ["", "**Depth is allowed on:** no city cleared 10 impressions this window."]
    # Position, impression-weighted across the city's pages, and the CTR a
    # result at that position normally earns. Added 2026-08-14 after a session
    # read Palermo's 2% CTR as a titles-and-thumbnails problem and Hidde asked
    # what that meant: the digest could not answer, because it reported clicks
    # and impressions per city but position only for zero-click pages. Without
    # position, every weak CTR looks like a copy problem, and almost all of
    # them are a ranking problem instead. "vs" is the industry CTR curve, so a
    # city at or above its expected rate has a RANK problem (only a better
    # position helps), and one well below it has a SNIPPET problem (title,
    # description and thumbnail are worth rewriting).
    # The city's BIGGEST SINGLE QUERY and where that one query actually ranks,
    # added 2026-08-18 because the column beside it was being over-read, by me
    # among others. `Position` is impression-weighted ACROSS a city's pages, so
    # it is an average, and comparing an average against the CTR curve is only
    # honest when the underlying positions are tight. A city averaging 9.8 out
    # of one query at 3 and another at 30 behaves nothing like a city sitting
    # at 9.8, and the curve comparison will call the first a snippet problem
    # when it is nothing of the kind. So print the one query that carries the
    # most impressions and its own position: when that number is close to the
    # average, the snippet reading holds; when it is far off, the average was
    # never the thing to reason from.
    top_q = {}
    for r in (pairs or []):
        page = r["keys"][0].replace("https://ancienttrees.app", "").strip("/")
        city = page.split("/")[0] if page else ""
        if not city:
            continue
        cur = top_q.get(city)
        if cur is None or r["impressions"] > cur[1]:
            top_q[city] = (r["keys"][1], r["impressions"], r.get("position", 0))

    out = ["", "**Depth is allowed on these cities** (10+ impressions in the window;"
               " photos, pins and best_time go here and nowhere else):", "",
           "| City | Clicks | Impressions | CTR | Position | Normal there | Biggest query, and where it really sits |",
           "|---|---:|---:|---:|---:|---:|---|"]
    for c, cl, im, pos in rows:
        ctr = 100.0 * cl / im if im else 0
        q = top_q.get(c)
        qcell = ("%s (i%d, p%.0f)" % (clean_query(q[0]), q[1], q[2])) if q else "-"
        out.append("| %s | %d | %d | %.1f%% | %.1f | %.1f%% | %s |"
                   % (c, cl, im, ctr, pos, expected_ctr(pos), qcell))
    return out


def gsc_section(gsc):
    if gsc is None:
        return ("Search Console: GSC_* secrets not configured; section skipped.", None)
    days, queries, pages, gap_queries, pairs = gsc
    days = [d for d in days if d.get("impressions") or d.get("clicks")]
    if not days:
        return ("Search Console: connected, but Google returned no rows for the window.", None)
    latest = days[-1]
    prev = days[-2] if len(days) > 1 else None
    # A markdown table, not a run-on line. Hidde, 2026-08-10: "ik wil duidelijke
    # website en search console getallen in een tabel". The old shape packed ten
    # days into "07-31:c2/i230  08-01:c7/i253 ..." which is technically complete
    # and unreadable, so nobody read it. CTR is computed here because it is the
    # column that actually says whether a day was good: impressions move with
    # Google's mood, the ratio moves with our titles and snippets.
    rows = ["| Day | Clicks | Impressions | CTR | Position |",
            "|---|---:|---:|---:|---:|"]
    for d in days:
        imp = d["impressions"] or 0
        rows.append("| %s | %d | %d | %.1f%% | %.1f |" % (
            d["keys"][0][5:], d["clicks"], imp,
            (100.0 * d["clicks"] / imp) if imp else 0.0, d.get("position", 0)))
    tc = sum(d["clicks"] for d in days)
    ti = sum(d["impressions"] or 0 for d in days)
    rows.append("| **window** | **%d** | **%d** | **%.1f%%** | |" % (
        tc, ti, (100.0 * tc / ti) if ti else 0.0))
    trend = "\n" + "\n".join(rows)
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
        "Search Console, the last 10 days Google will give us (its data lags 2-3 days,"
        " so the newest row is never yesterday). Position is an average across every"
        " query, so it dips whenever we start ranking for something new:",
        "%s" % trend,
        "- Top queries (10d): " + "; ".join(
            "%s (i%d, p%.0f)" % (clean_query(r["keys"][0]), r["impressions"], r["position"]) for r in queries) if queries else "- Top queries: none",
        "- Top pages (10d): " + "; ".join(
            "%s (c%d/i%d)" % (r["keys"][0].replace("https://ancienttrees.app", ""), r["clicks"], r["impressions"]) for r in pages[:5]) if pages else "- Top pages: none",
        gap_line,
        *demand_lines(pages, pairs),
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
    refs: rumPageloadEventsAdaptiveGroups(limit: 25,
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
    # Same table treatment as the search rows, plus the warning that belongs
    # beside every one of these numbers: Cloudflare's beacon buckets counts to
    # the nearest ten, so "10 visits" is anywhere from 5 to 14 and "0" is not
    # zero. At our volume that makes the per-day column decorative and the
    # window total the only figure worth reading. Search Console does not
    # round, which is why it, and not this, is the series to steer by.
    rows = ["| Day | Visits | Pageviews |", "|---|---:|---:|"]
    for d in days:
        rows.append("| %s | %d | %d |" % (
            d["dimensions"]["date"][5:], d["sum"]["visits"], d["count"]))
    rows.append("| **window** | **%d** | **%d** |" % (
        sum(d["sum"]["visits"] for d in days), sum(d["count"] for d in days)))
    trend = "\n" + "\n".join(rows)
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
            "Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.\n%s\n- Top paths: %s\n"
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

# The assistants, kept separate from both lists above because an arrival from
# one is neither a search click nor a backlink: it means a model answered
# somebody's question and cited us, which is the only evidence of AI
# visibility this project can currently gather at all.
#
# Everything else about AI findability is unmeasurable from here and it is
# worth writing down why, so nobody spends a window rediscovering it. The site
# is served straight from GitHub Pages with no proxy in front, so there are no
# access logs and a crawl by GPTBot, ClaudeBot or PerplexityBot leaves no
# trace we can see. Cloudflare Web Analytics is a JavaScript beacon and bots
# do not run JavaScript, so it cannot see them either. That leaves the human
# who clicks a citation, which is what this list catches.
#
# It is deliberately a named line rather than a host in the referrer list: the
# referrer pull was limit 5 until 2026-08-16, and with direct, self, google
# and one corporate proxy filling those slots, the first arrival from an
# assistant would have been cut off before anybody saw it. The limit is 25
# now, and this line names the answer instead of leaving it to be spotted.
AI_SOURCES = (
    "chatgpt.com", "chat.openai.com", "openai.com", "perplexity.ai",
    "claude.ai", "copilot.microsoft.com", "gemini.google.com",
    "bard.google.com", "you.com", "phind.com", "poe.com",
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
    external, ai = [], []
    for r in refs or []:
        host = (r["dimensions"].get("refererHost") or "").lower()
        if not host:
            continue
        if any(a in host for a in AI_SOURCES):
            ai.append("%s (%d)" % (host, r["count"]))
            continue
        if any(b in host for b in NOT_A_BACKLINK):
            continue
        external.append("%s (%d)" % (host, r["count"]))
    line = "; ".join(external) if external else "none yet"
    ai_line = ("\nAI: arrivals from an assistant that cited us: %s"
               % ("; ".join(ai) if ai else "none yet"))
    # The standing "read your backlinks by hand" instruction that used to sit
    # here was printed identically every morning for a fortnight, which is the
    # definition of a line nobody reads. Ahrefs Webmaster Tools answers it now,
    # and the honest state as of 2026-08-09 is that our 298 referring domains
    # are a spam network, every one nofollow, so the count is not the metric.
    return ("Links: external referrers (a link somebody actually clicked): %s%s"
            % (line, ai_line))


SUPA = "https://caimvxiyrtifilimlkqw.supabase.co"

# Row 1 of the submissions table is our own pipeline test from 2026-07-31, made
# when the form was wired up. The digest counted it as a reader submission for
# ten days, so "Submissions: 1" read as somebody having sent us a tree when the
# true figure is zero. Same class of error as the beacon counting our own CI
# until 2026-08-08: a number that includes us flatters us, and the fortnight
# review's own criterion is literally "whether a single reader submission
# exists". Excluded by id rather than by guessing at content.
# Ids 2 and 3 are the same class: the 2026-08-14 session's live test of the
# new vote-and-report chain, both on Baarn's brn_005, one of them explicitly
# marked "[TEST ROW...]". They made the 08-14 digest announce two reader
# submissions, and the session reading it believed them for a paragraph. A
# number that includes us flatters us, so ours are excluded by id.
TEST_SUBMISSION_IDS = {1, 2, 3}

# Anything a block thinks should reach Hidde today. The verdict line at the top
# of the entry is built from this, and an empty list is the good case and says
# so in words. Without it the report has no front door: fifteen true blocks and
# no statement of which one, if any, is today's.
ATTENTION = []


def _supa(path, key, timeout=30):
    req = urllib.request.Request(SUPA + path, headers={
        "apikey": key, "Authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r), dict(r.headers)


def _days_since(iso, today):
    """Whole days between an ISO timestamp and today, or None."""
    if not iso:
        return None
    try:
        d = datetime.date.fromisoformat(str(iso)[:10])
    except ValueError:
        return None
    return (today - d).days


def _ago(n):
    if n is None:
        return "never"
    if n == 0:
        return "today"
    if n == 1:
        return "yesterday"
    return "%d days ago" % n


def product_section(today):
    """Block 1, and the only block that answers goal 1.

    Restructured 2026-08-09 with Hidde on the hierarchy question. Every other
    number here is upstream of this one: search brings people, pages hold
    them, and none of it counts until somebody actually sets out for a tree.

    The design choice that matters is "days since", not the count. At these
    volumes a daily count of zero prints the same thing every morning and
    stops being read by the second week, while "31 days since anyone opened
    directions" is a number that grows and gets harder to look away from."""
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not key:
        return "Did the product happen: Supabase key absent, cannot say."
    out = ["**Did the product happen**"]

    # Every action we record, with yesterday's count and how long since the
    # last one of each kind. 800 rows covers months at current volume.
    try:
        rows, _ = _supa("/rest/v1/events?select=name,created_at"
                        "&order=created_at.desc&limit=800", key)
    except Exception as e:
        rows = None
        out.append("- Actions: events table unreadable (%s)" % str(e)[:70])
    if rows is not None:
        yday = (today - datetime.timedelta(days=1)).isoformat()
        counts, last = {}, {}
        for r in rows:
            n = r.get("name") or "?"
            if str(r.get("created_at"))[:10] == yday:
                counts[n] = counts.get(n, 0) + 1
            if n not in last:
                last[n] = r.get("created_at")
        # Named explicitly so an action that has NEVER fired still gets a line.
        # A missing row is the loudest signal here and an empty dict hides it.
        # The three funnels of FUNNELS.md, in step order. collect and share
        # died with the collect button (2026-08-14); walk-open/save/signin
        # arrived the same day.
        # "worthit-not worth it" added 2026-08-16, and its absence had already
        # cost us a reading. On 2026-08-15 a reader gave Prague's prg_007 a
        # thumbs DOWN with the "wrong location" chip, which is the first time
        # anyone used that control. The vote reached Supabase, a night run
        # re-verified the pin and found no error, and the digest still reported
        # "0 actions on 370 visits" the next morning, because the up-vote was
        # named here and the down-vote was not. The comment above says the
        # point of this list is that a never-fired action still gets a line;
        # half a control was missing from it.
        for name in ("directions", "walk-open", "walk-start", "save",
                     "worthit-worth it", "worthit-not worth it",
                     "signin-link-sent", "app-cta", "waitlist-submit"):
            last.setdefault(name, None)
        for name in sorted(last, key=lambda k: (-counts.get(k, 0), k)):
            out.append("- %-12s %d yesterday, last %s" % (
                name + ":", counts.get(name, 0), _ago(_days_since(last[name], today))))

    # Sign-ups over time, not just a running total. Hidde, 2026-08-10: he wants
    # the registrations in the numbers he reads. A total answers "how many" and
    # hides the only thing worth knowing at this size, which is whether anything
    # arrived this week. Fourteen days, and a column that is entirely zeros is
    # itself the finding rather than a formatting problem.
    try:
        since = today - datetime.timedelta(days=14)
        series = {}
        for label, path in (("waitlist", "/rest/v1/waitlist?select=created_at"),
                            ("submissions", "/rest/v1/submissions?select=id,created_at")):
            rows_, _ = _supa(path, key)
            for r in rows_:
                if label == "submissions" and r.get("id") in TEST_SUBMISSION_IDS:
                    continue
                d = str(r.get("created_at"))[:10]
                series.setdefault(d, {})[label] = series.setdefault(d, {}).get(label, 0) + 1
        users, _ = _supa("/auth/v1/admin/users?page=1&per_page=1000", key)
        for u in ((users or {}).get("users") or []):
            d = str(u.get("created_at"))[:10]
            series.setdefault(d, {})["accounts"] = series.setdefault(d, {}).get("accounts", 0) + 1
        days_ = [(since + datetime.timedelta(days=i)).isoformat() for i in range(15)]
        if any(series.get(d) for d in days_):
            out.append("")
            out.append("| Day | Accounts | Waitlist | Submissions |")
            out.append("|---|---:|---:|---:|")
            for d in days_:
                v = series.get(d, {})
                out.append("| %s | %d | %d | %d |" % (
                    d[5:], v.get("accounts", 0), v.get("waitlist", 0), v.get("submissions", 0)))
            tot = {k: sum(v.get(k, 0) for d, v in series.items() if d in days_)
                   for k in ("accounts", "waitlist", "submissions")}
            out.append("| **14 days** | **%d** | **%d** | **%d** |" % (
                tot["accounts"], tot["waitlist"], tot["submissions"]))
        else:
            out.append("- Nothing signed up, joined the waitlist or was submitted in 14 days.")
    except Exception as e:
        out.append("- Sign-up series unreadable (%s)" % str(e)[:60])

    for label, path in (("Waitlist", "/rest/v1/waitlist"),
                        ("Submissions", "/rest/v1/submissions")):
        try:
            head, hd = _supa(path + "?select=id&limit=1", key)
            _, hd2 = _supa(path + "?select=id", key)
            newest, _ = _supa(path + "?select=created_at&order=created_at.desc&limit=1", key)
            total = len(hd2) if isinstance(hd2, list) else 0
        except Exception as e:
            out.append("- %s: unreadable (%s)" % (label, str(e)[:60]))
            continue
        try:
            allrows, _ = _supa(path + "?select=id,created_at", key)
            if label == "Submissions":
                allrows = [r for r in allrows if r.get("id") not in TEST_SUBMISSION_IDS]
            total = len(allrows)
            newest_at = max((r.get("created_at") or "" for r in allrows), default=None)
        except Exception:
            newest_at = None
        since = _days_since(newest_at, today)
        if since is not None and since <= 1:
            ATTENTION.append("a %s arrived %s (%d total)"
                             % (label.rstrip("s").lower(), _ago(since), total))
        out.append("- %-12s %d total, newest %s" % (
            label + ":", total, _ago(since)))

    try:
        acc, newest_at, page = 0, None, 1
        while page <= 10:
            users, _ = _supa("/auth/v1/admin/users?page=%d&per_page=1000" % page, key)
            users = (users or {}).get("users") or []
            acc += len(users)
            for u in users:
                c = u.get("created_at")
                if c and (newest_at is None or c > newest_at):
                    newest_at = c
            if len(users) < 1000:
                break
            page += 1
        since = _days_since(newest_at, today)
        if since is not None and since <= 1:
            ATTENTION.append("an account was opened %s (%d total)" % (_ago(since), acc))
        out.append("- %-12s %d total, newest %s" % ("Accounts:", acc, _ago(since)))
    except Exception as e:
        out.append("- Accounts: unreadable (%s)" % str(e)[:60])
    return "\n".join(out)


def funnel_section(today, cf_token):
    """Block 2: the same journey as rates rather than levels.

    Levels tell you how big yesterday was; rates tell you which step is
    leaking, and those need opposite work. 78 clicks and 0 actions is a
    fact you cannot act on. "2.1% of people who see us click, 1.6 pages per
    visit, 0% of visits do anything" points at one step.

    Two weeks against the two before, because a day of this is noise."""
    import audience as A
    rows = []

    def rate(a, b):
        return (100.0 * a / b) if b else 0.0

    q = A.gsc_client(today)
    if q is not None:
        def window(d0, d1):
            r = q([], 1, {"startDate": (today - datetime.timedelta(days=d0)).isoformat(),
                          "endDate": (today - datetime.timedelta(days=d1)).isoformat()})
            return (r[0]["clicks"], r[0]["impressions"]) if r else (0, 0)
        c1, i1 = window(14, 0)
        c0, i0 = window(28, 14)
        rows.append("- Seen to clicked: %.1f%% (%d of %d) vs %.1f%% the fortnight before"
                    % (rate(c1, i1), c1, i1, rate(c0, i0)))
    if cf_token:
        try:
            a, since = A.rum(cf_token, today)
        except Exception:
            a = None
        if a:
            days = a.get("days") or []
            pv = sum(d["count"] for d in days)
            vis = sum(d["sum"]["visits"] for d in days)
            rows.append("- Pages per visit: %.1f (%d visits, %d pageviews since %s)"
                        % ((pv / vis) if vis else 0, vis, pv, since))
            key = os.environ.get("SUPABASE_SERVICE_KEY")
            if key and vis:
                try:
                    ev, _ = _supa("/rest/v1/events?select=id&created_at=gte.%sT00:00:00Z"
                                  % since, key)
                    rows.append("- Visits that did something: %.1f%% (%d actions on %d visits)"
                                % (rate(len(ev), vis), len(ev), vis))
                    # The watchdog that was missing, added 2026-08-16 the day
                    # the beacon bug was found. Every funnel event had been
                    # silently dropped since launch (sendBeacon cannot
                    # preflight a Blob of type application/json, so the request
                    # died and sendBeacon still returned true), and the zeros
                    # were read for five weeks as a fact about users. A number
                    # that is exactly zero on hundreds of visits is the
                    # signature of a broken instrument, not of an audience, so
                    # the digest says so itself rather than waiting for
                    # somebody to wonder.
                    if not ev and vis >= 100:
                        rows.append("- **WARNING: %d visits and not one event of "
                                    "any kind. At this volume that reads as a "
                                    "broken recorder rather than as user "
                                    "behaviour. Check at.track() reaches the "
                                    "events table before drawing any conclusion "
                                    "from a zero above.**" % vis)
                except Exception:
                    pass
    return "**The funnel, as rates**\n" + ("\n".join(rows) if rows else "- no data")


def audience_section(today, cf_token, short=False):
    """Who they are, over 28 days: country, device, search language, landing
    page, and how they arrived. Volume answers 'how many', this answers 'who',
    and the two need different windows: a day is enough for a click count and
    far too little for an audience, so this one deliberately looks back 28 days
    while everything above it reports yesterday.

    Every line carries its denominator. At the volumes this site currently
    sees, a ranked list without one reads as knowledge and is arithmetic on
    single digits."""
    import audience as A

    out = ["**Who they are**" + ("" if short else " (full cut, Mondays)")]
    q = A.gsc_client(today)
    if q is None:
        out.append("Audience: Search Console secrets absent.")
    else:
        countries = q(["country"], 8)
        devices = q(["device"], 5)
        pages = q(["page"], 8)
        queries = q(["query"], 100)
        # Totals come from an undimensioned query, never from summing a top-N
        # list: the first version of this line added up the top 8 countries and
        # printed the result as the site total, which understated it by a third.
        totals = q([], 1)
        tc = totals[0]["clicks"] if totals else 0
        ti = totals[0]["impressions"] if totals else 0
        out.append("Audience, 28 days of search (%d clicks, %d impressions):" % (tc, ti))

        def line(label, rows, n=5):
            bits = []
            for r in rows[:n]:
                k = (r["keys"][0] or "?").replace("https://ancienttrees.app", "") or "/"
                bits.append("%s c%d/i%d" % (k, r["clicks"], r["impressions"]))
            return "- %s: %s" % (label, "; ".join(bits) if bits else "none")

        out.append(line("Countries", countries))
        out.append(line("Devices", devices))
        out.append(line("Landing pages", pages))
        if short:
            return "\n".join(out)

        langs = {}
        for r in queries:
            a = langs.setdefault(A.classify(r["keys"][0]), {"c": 0, "i": 0, "n": 0})
            a["c"] += r["clicks"]; a["i"] += r["impressions"]; a["n"] += 1
        ranked = sorted(langs.items(), key=lambda kv: -kv[1]["i"])
        # Directional only, and the reason is Google's, not ours: query-level
        # data omits rare queries for privacy, so most of the clicks above
        # never appear in any query row. Read the shape, never the totals.
        out.append("- Search language (top %d named queries, crude match, most clicks "
                   "are in queries Google withholds): %s" % (
            len(queries), "; ".join("%s %dq c%d/i%d" % (k, v["n"], v["c"], v["i"])
                                    for k, v in ranked)))

    if cf_token:
        try:
            a, since = A.rum(cf_token, today)
        except Exception as e:
            a = None
            out.append("- On-site beacon: unreadable (%s)" % str(e)[:80])
        if a:
            days = a.get("days") or []
            pv = sum(d["count"] for d in days)
            vis = sum(d["sum"]["visits"] for d in days)

            def dim(rows, key, n=5):
                bits = []
                for r in (rows or [])[:n]:
                    v = r["dimensions"].get(key) or "(direct)"
                    bits.append("%s %d" % (str(v)[:26], r["count"]))
                return "; ".join(bits) if bits else "none"

            out.append("On the site since %s (%d visits, %d pageviews, %.1f pages per visit):"
                       % (since, vis, pv, (pv / vis) if vis else 0))
            out.append("- Countries: " + dim(a.get("countries"), "countryName"))
            out.append("- Devices: " + dim(a.get("devices"), "deviceType", 4))
            out.append("- Browsers: " + dim(a.get("browsers"), "userAgentBrowser", 4))
            out.append("- Arrived via: " + dim(a.get("refs"), "refererHost"))
            out.append("- Opened: " + dim(a.get("paths"), "requestPath", 8))
    return "\n".join(out)


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
        ATTENTION.append("scheduled workflows silent past their slot: " + "; ".join(quiet))
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

    # The front door. Most mornings the honest answer is that nothing here
    # needs him, and saying so plainly is what keeps the report readable on
    # the mornings when something does.
    verdict = ("**Today: nothing here needs you.** The blocks below are the "
               "standing picture."
               if not ATTENTION else
               "**Today: " + "; ".join(ATTENTION) + ".**")

    return """## %s (previous UTC day)

%s

%s%s

**Conclusion:** %s
""" % (yday.isoformat(), verdict, zone_block, gsc_text, conclusion)


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
    # --force rewrites today's entry instead of refusing. Added 2026-08-09,
    # when a new number (registered accounts) shipped after the morning's
    # entry had already been written and there was no way to see it before
    # the next day. The old entry is replaced, never appended twice.
    force = "--force" in sys.argv
    if yesterday_header in existing:
        if not force:
            print("Entry for %s already present, nothing to do" % yday)
            return 0
        start = existing.index(yesterday_header)
        nxt = existing.find("\n## ", start + 1)
        existing = existing[:start] + (existing[nxt + 1:] if nxt != -1 else "")
        with open(DATA_MD, "w") as f:
            f.write(existing)
        print("Entry for %s replaced (--force)" % yday)

    try:
        days = fetch_cloudflare(token, today)
    except (RuntimeError, urllib.error.URLError, KeyError) as e:
        print("SKIP: Cloudflare fetch failed: %s" % e)
        return 1

    # The hierarchy, agreed with Hidde 2026-08-09. The old entry was a
    # collection: fifteen true things in the order they happened to be
    # written. The order below is the order in which a bad number changes
    # what we do tomorrow, and anything that has not changed a decision in a
    # fortnight should be demoted out of it rather than kept for tidiness.
    #
    #   1. did the product happen        goal 1, the only block that is the point
    #   2. the funnel, as rates          which step leaks, which levels cannot say
    #   3. demand we are wasting         a work queue, not a report
    #   4. who they are                  slow-moving, three lines daily, full on Mondays
    #   5. supply and machine            it matters, it rarely changes the day
    blocks = []

    def block(fn, *a):
        try:
            t = fn(*a)
            if t:
                blocks.append(t)
        except Exception as e:
            blocks.append("%s: failed today (%s)." % (fn.__name__, str(e)[:90]))

    block(product_section, today)
    block(funnel_section, today, token)

    gsc_latest = None
    gsc_data = None
    try:
        gsc_data = fetch_gsc(today)
        gsc_text, gsc_latest = gsc_section(gsc_data)
        blocks.append("**Where demand is going to waste**\n\n" + gsc_text)
    except Exception as e:
        blocks.append("Search Console: fetch failed today (%s); numbers resume tomorrow." % e)

    # Monday gets the full audience cut, every other day gets the three lines
    # that can actually move. A 28-day window barely differs from yesterday's
    # 28-day window, and printing it in full daily buries the blocks above it.
    block(audience_section, today, token, today.weekday() != 0)

    block(fetch_rum, token, today)
    block(fetch_machine, today)
    gsc_text = "\n\n".join(blocks)

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
    # gsc_data, not a name that only existed inside gsc_section's argument:
    # the first version referenced `gsc`, which is undefined in this scope, and
    # the NameError hid in the force-rewrite path until a --force test hit it.
    promote(gsc_data[2] if gsc_data else None)
    return 0


def promote(pages):
    """Feed measured demand back into the queue, so a city that starts ranking
    climbs the list on its own.

    Hidde, 2026-08-13: "hebben we een mechanisme hoe de steden zoals palermo die
    het goed doen dan verhogen op de to do lijst?" We did not. CITY_QUEUE.md's
    score was a snapshot taken on 2026-08-11 and nothing fed Search Console back
    into it, so Palermo sat at rank 74 while taking 167 impressions and 3 clicks,
    which is better than most of the top twenty.

    The formula is not invented here, it is recovered from the file's own
    numbers. CITY_QUEUE.md says score is demand times realised yield, and yield
    is clicks per 100,000 Wikipedia pageviews; multiply those and the demand
    cancels, so **a measured city's score is simply the clicks it took in the
    window.** Checked against all ten measured rows: Lisbon 7.99 for 8 clicks,
    Porto 5.00 for 5, Prague 4.00 for 4, Athens 1.01 for 1.

    A city ranking without converting is not promoted: 10+ impressions and zero
    clicks scores 0.25, the same as a page that never ranked at all, because
    that is what the evidence says. Unpublished and unmeasured cities keep the
    score they have."""
    if not pages:
        print("promote: no Search Console rows, queue untouched")
        return
    src = os.path.join(ROOT, "data", "city-queue.json")
    if not os.path.exists(src):
        return
    with open(src, encoding="utf-8") as fh:
        doc = json.load(fh)
    per = {}
    for r in pages:
        path = r["keys"][0].replace("https://ancienttrees.app", "").strip("/")
        if not path:
            continue
        slug = path.split("/")[0]
        if slug in ("app", "explore", "cities", "contribute", "privacy", "account",
                    "species", "collections", "countries", "parks"):
            continue
        c, i = per.get(slug, (0, 0))
        per[slug] = (c + r["clicks"], i + r["impressions"])
    moved = []
    for city in doc["cities"]:
        clicks, imps = per.get(city.get("slug") or "", (0, 0))
        city["impressions_10d"], city["clicks_10d"] = imps, clicks
        if imps < 10:
            continue
        # SCORING MOVED OUT, 2026-08-16. This used to set score and basis
        # here, and from 2026-08-15 that made two scorers fight over one file:
        # scripts/rescore.py had taken over score/basis on travel demand and
        # measured yield, and this ran daily afterwards and overwrote the
        # measured half with its own clicks formula. The result was a queue
        # that was half one system and half the other, and it read as nonsense:
        # London on 95 impressions and 27k travel views sat at score 0.25 and
        # rank 259 while Toronto, with no page and no impressions, was rank 1.
        #
        # So promote() now writes only what it MEASURES (impressions and clicks
        # from Search Console) and rescore.py owns what those numbers MEAN.
        # The workflow runs rescore.py straight after this. Same rule this file
        # already applies to the city order: one authority per number.
        if imps or clicks:
            moved.append((city["city"], city.get("score"), None))
    # Ranks are NOT assigned here: scripts/city_queue.py owns ranking (score
    # times the ease factor) and the digest workflow runs it immediately after
    # this. Assigning ranks here too would be the two-copies disease again.
    with open(src, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
    print("promote: %d cities updated from measured demand "
          "(scoring is rescore.py's job)" % len(moved))
    for name, was, _ in moved[:8]:
        print("  %-16s measured (previous score %s)" % (name, was))


if __name__ == "__main__":
    sys.exit(main())
