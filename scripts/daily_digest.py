#!/usr/bin/env python3
"""Daily data digest: writes one dated entry per day into DATA.md.

Sources:
- Cloudflare zone analytics (GraphQL API), token from CLOUDFLARE_ANALYTICS_TOKEN.
- Search Console via OAuth refresh token (GSC_CLIENT_ID / GSC_CLIENT_SECRET /
  GSC_REFRESH_TOKEN), authorised by Hidde 2026-07-27. Data lags 2-3 days.

Stdlib only (hard rule 5). Safe to run twice a day: the second run is a no-op.
"""
import datetime
import hashlib
import glob
import json
import os
import subprocess
import sys
import unicodedata
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

Three event counts changed meaning on 2026-08-20, and the fall in them is the
fix rather than a regression. Until that date `app-cta`, `directions` and
`walks-app` were each counted by two click listeners at once, so one click
inserted two rows. Read any figure for those three from before 2026-08-20 as
roughly double the real number, and do not compare one across that date.
`app-cta` was worse than doubled: it also fired on the two `walks-app` links,
because those point at /app and the listener matched the href. Every other
event on the list is unaffected.
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
    # The window BEFORE this one, so the digest can say what is climbing rather
    # than only what is big. Hidde, 2026-08-20: "kun je ook winnaars en
    # verliezers toevoegen aan de daily digest maar vooral google search trend
    # positief". A level tells you where you stand; only a delta tells you
    # whether anything you did worked, and this file had no delta at all.
    # 11 days back to 1 day before this window starts. Search Console counts
    # startDate and endDate INCLUSIVELY, so the obvious arithmetic (today-20 to
    # today-10) puts the boundary day in BOTH windows and every delta carries
    # one day of double counting. Hidde caught it by asking what the +65 was
    # measured against, which is the useful thing about being asked to explain
    # a number out loud.
    pstart = (today - datetime.timedelta(days=21)).isoformat()
    pend = (today - datetime.timedelta(days=11)).isoformat()
    prev_pages = q({"startDate": pstart, "endDate": pend, "dimensions": ["page"],
                    "rowLimit": 5000, "dataState": "all"})
    prev_queries = q({"startDate": pstart, "endDate": pend, "dimensions": ["query"],
                      "rowLimit": 5000, "dataState": "all"})
    return days, queries, pages, gap_queries, pairs, prev_pages, prev_queries


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


def fold(s):
    """Lowercase and strip accents. Google's queries arrive unaccented far more
    often than not, and our own names are full of accents, so a raw string
    compare between the two is a coin toss."""
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


# Standing-page names that are ordinary English words. Matched only against a
# query that is that word and nothing else, the same treatment known_terms()
# already gives generic tree-name tails. Without this, "about" matched any
# query containing the word about, and the day's biggest real gap could sit
# behind it unreported.
GENERIC_EXACT = {"about", "app", "map", "species", "cities", "countries",
                 "explore", "collections", "privacy", "contribute", "trees",
                 "tree"}


def tokens(s):
    """Accent-folded word list. Word boundaries are the point: matching bare
    substrings meant the city Ede matched 'oudste boom van nederland', because
    "ede" sits inside "nederland". Every short place name that is also a
    fragment of a longer word had the same effect, and each one silently
    swallowed a real gap."""
    out, cur = [], []
    for ch in fold(s):
        if ch.isalnum():
            cur.append(ch)
        elif cur:
            out.append("".join(cur)); cur = []
    if cur:
        out.append("".join(cur))
    return out


def term_matches(term, query):
    """True when one of these is a contiguous run of words inside the other.
    Both directions, because a searcher types the distinctive half of a name
    ("alameda dos platanos") and not the whole page title ("alameda dos
    platanos of jardim da cordoaria")."""
    if len(term) == 1 and term[0] in GENERIC_EXACT:
        return query == term
    a, b = (term, query) if len(term) <= len(query) else (query, term)
    n = len(a)
    return any(b[i:i + n] == a for i in range(len(b) - n + 1))


def content_gaps(gap_queries):
    """Every query (10d) whose text matches no page we already have: content
    leads, the kind that found us before we had a page for them ("albero roma").
    A query that matches a page we already have is not a gap, it is a ranking
    problem, and those two need opposite responses: one is a page to write, the
    other is a page to strengthen.

    Two faults fixed 2026-08-26, either of which alone produced a false gap.
    The match ran in ONE direction, asking only whether our name sits inside
    their query, so a searcher typing less than our full page title always read
    as a miss. And nothing folded accents, so 'platanos' never met 'plátanos'.
    Together they reported 'alameda dos platanos' (i13, p8) as a page to write
    while we had TWO pages ranking for it, which is how the duplicate Cordoaria
    entries were found. Third occurrence of this class after 'ancient tree map'
    (08-06) and 'den brandt park' (08-07/08), so per the ratchet it is code.

    Returns the full list, biggest first, not one. Reporting a single gap made
    the day's lead depend on which false positive happened to score highest.

    What it still cannot do: partial name overlap. 'vegas trees' and 'oldest
    tree in dc' read as gaps while /las-vegas and /washington-dc exist, because
    neither query is a word run inside the city name. Those are real leads about
    real unserved demand, but the fix for them is a stronger page, not a new
    one, so the printed line says to check before building."""
    terms = [tokens(t) for t in known_terms()]
    terms = [t for t in terms if t]
    misses = []
    for r in gap_queries:
        q = tokens(r["keys"][0])
        if any(term_matches(t, q) for t in terms):
            continue
        misses.append(r)
    return sorted(misses, key=lambda r: -r["impressions"])


def find_content_gap(gap_queries):
    """The biggest content gap, or None. Kept for callers that want just one."""
    gaps = content_gaps(gap_queries)
    return gaps[0] if gaps else None


# The language prefixes translated pages live under. A path like /it/rome is
# not a city called "it", which is exactly how this file read it until
# 2026-08-22: every Spanish page summed into one fake city row, and the depth
# rule could have sent photo work there. With seven languages that would be
# seven fake cities and no way to read the language test at all.
LANG_PREFIXES = ("es", "it", "nl", "de", "pt", "fr", "ja")


def split_path(path):
    """(lang, city) for a page path. lang is 'en' for the canonical pages."""
    parts = [p for p in path.strip("/").split("/") if p]
    if parts and parts[0] in LANG_PREFIXES:
        return parts[0], (parts[1] if len(parts) > 1 else "")
    return "en", (parts[0] if parts else "")


def language_lines(pages):
    """What each translated language earns, beside its English twin.

    Contract J v1.13 recorded the measure before anything was built: within
    four weeks of indexing a translated set should pass its English twin's
    impressions, and beat its position on the target-language query. Neither
    half is readable unless a page is attributed to a language AND a city."""
    if not pages:
        return []
    per = {}
    for r in pages:
        lang, city = split_path(r["keys"][0].replace("https://ancienttrees.app", ""))
        if not city:
            continue
        c, i, wp = per.get((lang, city), (0, 0, 0.0))
        per[(lang, city)] = (c + r["clicks"], i + r["impressions"],
                             wp + r.get("position", 0) * r["impressions"])
    pairs = [(lg, ct, v) for (lg, ct), v in per.items() if lg != "en"]
    if not pairs:
        return ["", "**The language test:** no translated page took an impression in this window yet."]
    out = ["", "**The language test** (Contract J v1.13: a translated set should pass its"
               " English twin's impressions within four weeks of indexing):", "",
           "| Lang | City | Clicks | Impressions | Position | English twin |",
           "|---|---|---:|---:|---:|---:|"]
    for lg, ct, v in sorted(pairs, key=lambda x: -x[2][1]):
        en = per.get(("en", ct), (0, 0, 0.0))
        pos = (v[2] / v[1]) if v[1] else 0
        out.append("| %s | %s | %d | %d | %.1f | %d |" % (lg, ct, v[0], v[1], pos, en[1]))
    return out


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
        lang, city = split_path(path)
        # A translated page belongs to the language test, not to its city's
        # English demand: counting it here would inflate the depth rule with
        # readers the English page never had.
        if lang != "en":
            continue
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


def pages_table(pages):
    """Every page that got a click, and the same totals split by page TYPE.

    NOT in the daily entry (Hidde, 2026-08-22: "niet voor elke digest gewoon
    voor nu"). It is a question you ask now and then, not a number that changes
    a day: call it from a session with the GSC secrets, or paste the call back
    into gsc_section for one run. Kept because working it out again from
    scratch would cost more than the twenty lines it is.

    Hidde, 2026-08-22: "mag ik de totale lijst van meest geklikte pagina's zien
    en moeten we meer tijd stoppen in bv de specifieke boom pagina's die veel
    worden bezocht." The digest printed five pages, which cannot answer either
    half. The type split is the half that decides work: if the clicks arrive on
    city pages, the work is more cities; if they arrive on individual tree
    pages, the work is deeper trees, and the two are nearly opposite.
    """
    if not pages:
        return ""
    def path(r):
        return r["keys"][0].replace("https://ancienttrees.app", "") or "/"
    def kind(p):
        parts = [x for x in p.strip("/").split("/") if x]
        if not parts:
            return "home"
        if parts[0] in ("collections", "species", "parks", "cities", "countries"):
            return parts[0]
        if parts[0] in ("explore", "app", "account", "contribute", "in-season", "press", "privacy", "saved"):
            return "product"
        if parts[0] == "es":
            parts = parts[1:]
            if not parts:
                return "es index"
        if len(parts) >= 2:
            return "tree page" if parts[1] != "oldest-tree" else "question page"
        return "city page"
    clicked = [r for r in pages if r["clicks"] > 0]
    clicked.sort(key=lambda r: (-r["clicks"], -r["impressions"]))
    rows = ["", "**Every page that got a click** (10 days)", "",
            "| Page | Clicks | Impressions | CTR | Position |",
            "|---|---:|---:|---:|---:|"]
    for r in clicked:
        rows.append("| %s | %d | %d | %.1f%% | %.1f |" % (
            path(r), r["clicks"], r["impressions"], 100 * r["ctr"], r["position"]))
    agg = {}
    for r in pages:
        k = kind(path(r))
        a = agg.setdefault(k, [0, 0, 0])
        a[0] += r["clicks"]; a[1] += r["impressions"]; a[2] += 1
    rows += ["", "**And the same clicks by page type**", "",
             "| Type | Pages seen | Clicks | Impressions | CTR |",
             "|---|---:|---:|---:|---:|"]
    for k, (c, i, n) in sorted(agg.items(), key=lambda x: -x[1][0]):
        rows.append("| %s | %d | %d | %d | %.1f%% |" % (k, n, c, i, 100.0 * c / i if i else 0))
    return "\n".join(rows)



def zero_click_queries(pages, pairs):
    """What the cities that earn impressions and no clicks are shown FOR.

    The depth table names them, and until 2026-08-28 nothing said why. The
    seen-not-clicked list is per PAGE, and a city's impressions are spread
    across its tree pages, so a city can carry 214 impressions at zero clicks
    while no single page of it reaches the list at all. Milan, Vienna and
    Madrid were named in the weekly analysis and none of the three could be
    diagnosed from this file.

    Aggregating the same pairs by CITY answers it, and the answer decides what
    kind of problem it is: local-language queries an English page will never
    win are a translation job, wrong-intent queries are a targeting job, and
    right-intent queries at a good position are the only case where rewriting
    a title is the fix."""
    if not pairs or not pages:
        return []
    by_city = {}
    for r in pairs:
        lang, city = split_path(r["keys"][0].replace("https://ancienttrees.app", ""))
        if lang != "en" or not city or city in ("app", "explore", "cities", "contribute",
                                                "privacy", "account", "species",
                                                "collections", "countries", "parks"):
            continue
        d = by_city.setdefault(city, {"imp": 0, "clicks": 0, "q": []})
        d["imp"] += r["impressions"]
        d["clicks"] += r["clicks"]
        d["q"].append((r["impressions"], r["keys"][1], r.get("position", 0)))
    worst = [(c, v) for c, v in by_city.items() if v["clicks"] == 0 and v["imp"] >= 60]
    if not worst:
        return []
    out = ["", "**Cities seen but never clicked** (60+ impressions, zero clicks, with"
               " what they are actually shown for):", ""]
    for city, v in sorted(worst, key=lambda t: -t[1]["imp"])[:8]:
        top = "; ".join("%s (i%d, p%.0f)" % (clean_query(q), i, pos)
                        for i, q, pos in sorted(v["q"], reverse=True)[:4])
        out.append("- %s (i%d): %s" % (city, v["imp"], top))
    return out


def gsc_section(gsc):
    if gsc is None:
        return ("Search Console: GSC_* secrets not configured; section skipped.", None)
    days, queries, pages, gap_queries, pairs = gsc[:5]
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
    for i, d in enumerate(days):
        imp = d["impressions"] or 0
        # THE NEWEST ROW IS NOT FINISHED. Google backfills for days, and it
        # backfills impressions harder than clicks, so a fresh row reads as a
        # brilliant day. Measured from our own files on 2026-08-24: 08-22 was
        # first reported as 12 clicks on 769 impressions and settled at 17 on
        # 1,030; 08-23 went from 13/776 to 15/957. A session read the newest
        # row's 3.6% CTR as a jump that morning and was wrong.
        #
        # The lag note above this table says the newest row is never yesterday,
        # which is about WHICH day it is, not about the row being incomplete.
        # Two different facts, and only one of them was written down.
        partial = " *partial*" if i == len(days) - 1 else ""
        rows.append("| %s%s | %d | %d | %.1f%% | %.1f |" % (
            d["keys"][0][5:], partial, d["clicks"], imp,
            (100.0 * d["clicks"] / imp) if imp else 0.0, d.get("position", 0)))
    tc = sum(d["clicks"] for d in days)
    ti = sum(d["impressions"] or 0 for d in days)
    rows.append("| **window** | **%d** | **%d** | **%.1f%%** | |" % (
        tc, ti, (100.0 * tc / ti) if ti else 0.0))
    trend = "\n" + "\n".join(rows)
    gaps = content_gaps(gap_queries)
    if gaps:
        gap_line = "\n".join(
            ["- Content leads, biggest first. A lead is a query no page TITLE covers, "
             "so some are ranking problems on a page we have rather than a page to "
             "write ('vegas trees' against /las-vegas). Check before building:"]
            + ["    - %r (i%d, p%.0f)" % (clean_query(g["keys"][0]),
                                          g["impressions"], g["position"])
               for g in gaps[:8]]
            + (["    - and %d more" % (len(gaps) - 8)] if len(gaps) > 8 else []))
    else:
        gap_line = "- Content leads: every query Google showed us matches a page we have"
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
    # Eight, not three. Three was enough while the site had a handful of pages
    # earning impressions; it is not now. The 2026-08-28 weekly analysis named
    # Milan, Vienna and Madrid as sitting at 0% CTR on 145 to 211 impressions
    # each, and not one of them could be diagnosed from this file, because the
    # top three were taken by Rome, Tenerife and Las Vegas. A report that names
    # a problem and withholds the evidence for it makes the next session guess.
    for _, page, v in sorted(leaks, key=lambda t: -t[2]["imp"])[:8]:
        top = "; ".join("%s (i%d, p%.0f)" % (clean_query(qq), i, pos)
                        for i, qq, pos in sorted(v["q"], reverse=True)[:3])
        leak_lines.append("- Seen, not clicked: %s (c%d/i%d, %.1f%%) for %s" % (
            page.replace("https://ancienttrees.app", ""), v["clicks"], v["imp"],
            v["clicks"] * 100.0 / max(v["imp"], 1), top))

    lines = [
        "Search Console, the last 10 days Google will give us (its data lags 2-3 days,"
        " so the newest row is never yesterday). The newest row is also still"
        " FILLING: Google backfills for days and backfills impressions harder"
        " than clicks, so it reads as an unusually good day and is not one"
        " (08-22 arrived as 12/769 and settled at 17/1030). Position is an"
        " average across every query, so it dips whenever we start ranking for"
        " something new:",
        "%s" % trend,
        "- Top queries (10d): " + "; ".join(
            "%s (i%d, p%.0f)" % (clean_query(r["keys"][0]), r["impressions"], r["position"]) for r in queries) if queries else "- Top queries: none",
        "- Top pages (10d): " + "; ".join(
            "%s (c%d/i%d)" % (r["keys"][0].replace("https://ancienttrees.app", ""), r["clicks"], r["impressions"]) for r in pages[:5]) if pages else "- Top pages: none",
        gap_line,
        *demand_lines(pages, pairs),
        *language_lines(pages),
        *zero_click_queries(pages, pairs),
        *leak_lines,
    ]
    return "\n".join(lines), {"clicks": latest["clicks"], "impressions": latest["impressions"],
                               "prev_clicks": prev["clicks"] if prev else 0,
                               "prev_impressions": prev["impressions"] if prev else 0}


def _short_page(url):
    path = str(url).replace("https://ancienttrees.app", "").rstrip("/")
    return path or "/"


def trend_section(gsc):
    """What is climbing, and what is slipping, against the previous ten days.

    Hidde, 2026-08-20, and the emphasis is his: "vooral google search trend
    positief". The digest reported levels only, so a page that doubled and a
    page that halved looked identical as long as they ended on the same number.
    Nothing in the file could tell him whether a rewrite worked.

    Climbing comes first and gets the longer table on purpose. Losses matter,
    but a daily report that leads with them trains you to stop reading it, and
    the useful action is almost always "do more of what moved" rather than
    "mourn what fell".

    Two guards against reading noise as a trend. A page needs 15 impressions in
    the current window to appear at all, because a jump from 1 to 4 is a
    rounding error with a big percentage on it. And NEW means genuinely absent
    before, which on a site opening four cities a night is the most common kind
    of good news and deserves saying separately.
    """
    if gsc is None or len(gsc) < 7:
        return None
    _, _, pages, _, _, prev_pages, prev_queries = gsc
    if not pages:
        return None

    def index(rows):
        out = {}
        for r in rows:
            key = (r.get("keys") or [""])[0]
            out[key] = r
        return out

    now, before = index(pages), index(prev_pages)
    MIN = 15

    climbed, arrived, slipped = [], [], []
    for key, r in now.items():
        imp = r.get("impressions") or 0
        if imp < MIN:
            continue
        old = before.get(key)
        if old is None:
            arrived.append((imp, _short_page(key), r.get("clicks") or 0,
                            r.get("position") or 0))
            continue
        d_imp = imp - (old.get("impressions") or 0)
        # Position: lower is better, so an improvement is a positive number.
        d_pos = (old.get("position") or 0) - (r.get("position") or 0)
        row = (_short_page(key), imp, d_imp, r.get("position") or 0, d_pos,
               (r.get("clicks") or 0) - (old.get("clicks") or 0))
        if d_imp > 0 or d_pos > 0.5:
            climbed.append(row)
        elif d_imp < 0 and d_pos < -0.5:
            slipped.append(row)

    climbed.sort(key=lambda x: -x[2])
    arrived.sort(reverse=True)
    slipped.sort(key=lambda x: x[2])

    out = ["", "**Climbing** (this ten days against the ten before it)", ""]
    if climbed:
        out += ["| Page | Impressions | Change | Position | Moved | Clicks |",
                "|---|---:|---:|---:|---:|---:|"]
        for name, imp, d_imp, pos, d_pos, d_clk in climbed[:8]:
            out.append("| %s | %d | %+d | %.1f | %s | %+d |" % (
                name, imp, d_imp, pos,
                ("%+.1f" % d_pos) if abs(d_pos) >= 0.1 else "-", d_clk))
    else:
        out.append("Nothing gained ground this window.")

    if arrived:
        out += ["", "**Newly ranking** (no impressions at all ten days ago)", "",
                "| Page | Impressions | Clicks | Position |", "|---|---:|---:|---:|"]
        for imp, name, clk, pos in arrived[:6]:
            out.append("| %s | %d | %d | %.1f |" % (name, imp, clk, pos))

    if slipped:
        out += ["", "**Slipping**", "",
                "| Page | Impressions | Change | Position | Moved |",
                "|---|---:|---:|---:|---:|"]
        for name, imp, d_imp, pos, d_pos, _ in slipped[:4]:
            out.append("| %s | %d | %+d | %.1f | %+.1f |" % (name, imp, d_imp, pos, d_pos))

    # Queries that are new, which is where a content gap turns into a page.
    qnow = {(r.get("keys") or [""])[0]: r for r in (gsc[1] or [])}
    qbefore = {(r.get("keys") or [""])[0] for r in (prev_queries or [])}
    fresh = [(r.get("impressions") or 0, k) for k, r in qnow.items()
             if k not in qbefore and (r.get("impressions") or 0) >= 3]
    if fresh:
        fresh.sort(reverse=True)
        out += ["", "- New queries this window: "
                + ", ".join("%s (i%d)" % (k, i) for i, k in fresh[:5]) + "."]
    return "\n".join(out)


def _selftest_trend():
    """Prove trend_section on known input. `python3 scripts/daily_digest.py --selftest`.

    Exists because this section cannot be checked against the live API without
    the GSC secrets, and because the digest refuses to rewrite a day it has
    already written: a mistake here would sit unseen until tomorrow's entry.
    """
    def pg(page, imp, clicks, pos):
        return {"keys": ["https://ancienttrees.app" + page], "impressions": imp,
                "clicks": clicks, "position": pos}
    def qy(q, imp):
        return {"keys": [q], "impressions": imp, "clicks": 0, "position": 10}
    now = [pg("/palermo", 184, 3, 10.1), pg("/prague", 136, 8, 7.6),
           pg("/ottawa", 40, 1, 14.0), pg("/rome", 214, 1, 15.0),
           pg("/london", 131, 0, 22.1), pg("/tiny", 4, 0, 40.0)]
    before = [pg("/palermo", 120, 2, 13.0), pg("/prague", 140, 7, 7.4),
              pg("/rome", 260, 4, 12.0), pg("/london", 150, 1, 19.0)]
    out = trend_section(([], [qy("new query", 4)], now, [], [], before, []))
    fails = []
    def want(cond, msg):
        if not cond:
            fails.append(msg)
    want("/palermo | 184 | +64" in out, "a page that gained should be listed with its gain")
    want("+2.9" in out, "an improved position should read as a positive move")
    want("/ottawa" in out and "Newly ranking" in out, "a page absent before is newly ranking")
    want("/tiny" not in out, "under 15 impressions is noise and must not appear")
    want("/prague" not in out, "a flat page belongs in neither list")
    want("/rome" in out.split("**Slipping**")[-1], "a page that fell belongs under Slipping")
    want(out.index("Climbing") < out.index("Slipping"), "climbing comes first, on purpose")
    for f in fails:
        print("  FAIL " + f)
    print("trend self-test: " + ("all passed" if not fails else "%d FAILED" % len(fails)))
    return 1 if fails else 0


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
    """Per-day zone numbers for the last 8 days, oldest first, or [] if the
    zone is gone.

    This has always been structurally zero (see the note beside zone_block
    below: nothing is proxied, DNS lives at the registrar and points straight
    at GitHub Pages), and on 2026-08-18 Cloudflare removed the domain from the
    account entirely because its nameservers were never pointed there. From
    then on this raised, and the raise killed the whole digest before it could
    write a line: on 2026-08-19 the daily numbers simply stopped, and Search
    Console, the signups and the beacon went unreported with them.

    So a missing zone is now an empty list rather than an exception. The one
    number anybody quotes comes from fetch_rum(), which is ACCOUNT-scoped Web
    Analytics and is unaffected by any of this; it kept working throughout.
    """
    zones = api(
        "https://api.cloudflare.com/client/v4/zones?name=" + ZONE_NAME,
        token=token,
    )
    if not zones.get("success") or not zones.get("result"):
        print("NOTE: no Cloudflare zone for %s, so no proxied-traffic block. "
              "Expected since 2026-08-18; the beacon numbers are unaffected." % ZONE_NAME)
        return []
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
    paths: rumPageloadEventsAdaptiveGroups(limit: 12,
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
    # How much of the site people actually walk through, which is the closest
    # thing to navigation this beacon can give (Hidde, 2026-08-22: "hoe ze
    # navigeren"). A pageview whose referrer is our own host is somebody
    # moving from one of our pages to another; one from a search engine or
    # nothing at all is an arrival. Cloudflare's cookieless beacon carries no
    # session, so page-to-page paths do not exist to be reported: this ratio
    # and pages-per-visit are the honest substitutes.
    internal = sum(r["count"] for r in refs
                   if "ancienttrees.app" in (r["dimensions"].get("refererHost") or ""))
    total_pv = sum(r["count"] for r in refs) or 1
    nav = ("\n- Moved between our own pages: %d of %d pageviews (%.0f%%); the rest arrived "
           "from search or straight in. Cookieless means no session, so which page led to "
           "which cannot be measured." % (internal, total_pv, 100.0 * internal / total_pv))
    return ("Web Analytics (beacon, real browsers, cookieless):\n"
            "Counts are bucketed to the nearest ten by Cloudflare; read the window, not the day.\n%s\n- Top paths: %s\n"
            "- Referrers: %s%s\n- Countries: %s\n- Devices: %s%s"
            % (trend, top, _dim(refs, "refererHost"), nav,
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
    # Two changes on Hidde's ask, 2026-08-21. Saves joined the table ("please
    # add saves to the table"): a save is a person keeping a tree, the closest
    # thing to collecting the site has, and it was living as one line in the
    # events list where nobody weighs it. And submissions split in two, because
    # one column was hiding the difference that matters most at this size: a
    # reader SENDING US A TREE (kind tree or city, the contribute form's real
    # work) is a contributor, while a worth-it thumb or a correction (kind
    # feedback, correction, privacy) is a reaction. Both are people, only one
    # is supply, and "Submissions: 3" made them indistinguishable.
    try:
        since = today - datetime.timedelta(days=14)
        series = {}

        def bump(day_, label_):
            series.setdefault(day_, {})[label_] = series.setdefault(day_, {}).get(label_, 0) + 1

        rows_, _ = _supa("/rest/v1/waitlist?select=created_at", key)
        for r in rows_:
            bump(str(r.get("created_at"))[:10], "waitlist")
        # Dedupe form double-submits before counting: on 2026-08-20 one reader's
        # Toulouse correction arrived as three identical rows (CURATION.md, same
        # day) and the digest announced three submissions. Same day, same kind,
        # same tree, city and text is one submission however many times the
        # button was pressed. Worth-it votes (kind feedback) are exempt: two
        # readers giving the same thumb on the same tree the same day are two
        # people, and the vote control carries no text to tell them apart.
        rows_, _ = _supa("/rest/v1/submissions?select=id,created_at,kind,city,tree,why", key)
        seen_sub = set()
        for r in rows_:
            if r.get("id") in TEST_SUBMISSION_IDS:
                continue
            if (r.get("why") or "").startswith("vote undone"):
                continue  # a cancelled vote is bookkeeping, not feedback
            if r.get("kind") != "feedback":
                fp = (str(r.get("created_at"))[:10], r.get("kind"),
                      r.get("city"), r.get("tree"), r.get("why"))
                if fp in seen_sub:
                    continue
                seen_sub.add(fp)
            bump(str(r.get("created_at"))[:10],
                 "trees" if r.get("kind") in ("tree", "city") else "feedback")
        rows_, _ = _supa("/rest/v1/events?select=created_at&name=eq.save"
                         "&created_at=gte.%sT00:00:00" % since.isoformat(), key)
        for r in rows_:
            bump(str(r.get("created_at"))[:10], "saves")
        users, _ = _supa("/auth/v1/admin/users?page=1&per_page=1000", key)
        for u in ((users or {}).get("users") or []):
            bump(str(u.get("created_at"))[:10], "accounts")
        days_ = [(since + datetime.timedelta(days=i)).isoformat() for i in range(15)]
        if any(series.get(d) for d in days_):
            out.append("")
            out.append("| Day | Accounts | Waitlist | Saves | Trees sent | Feedback |")
            out.append("|---|---:|---:|---:|---:|---:|")
            for d in days_:
                v = series.get(d, {})
                out.append("| %s | %d | %d | %d | %d | %d |" % (
                    d[5:], v.get("accounts", 0), v.get("waitlist", 0),
                    v.get("saves", 0), v.get("trees", 0), v.get("feedback", 0)))
            tot = {k: sum(v.get(k, 0) for d, v in series.items() if d in days_)
                   for k in ("accounts", "waitlist", "saves", "trees", "feedback")}
            out.append("| **14 days** | **%d** | **%d** | **%d** | **%d** | **%d** |" % (
                tot["accounts"], tot["waitlist"], tot["saves"],
                tot["trees"], tot["feedback"]))
        else:
            out.append("- Nothing signed up, saved a tree or was submitted in 14 days.")
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
            sel = ("?select=id,created_at,kind,city,tree,why"
                   if label == "Submissions" else "?select=id,created_at")
            allrows, _ = _supa(path + sel, key)
            if label == "Submissions":
                allrows = [r for r in allrows if r.get("id") not in TEST_SUBMISSION_IDS]
                allrows = [r for r in allrows
                           if not (r.get("why") or "").startswith("vote undone")]
                # Same double-submit dedupe as the table above, votes exempt.
                dedup, seen_fp = [], set()
                for r in allrows:
                    if r.get("kind") != "feedback":
                        fp = (str(r.get("created_at"))[:10], r.get("kind"),
                              r.get("city"), r.get("tree"), r.get("why"))
                        if fp in seen_fp:
                            continue
                        seen_fp.add(fp)
                    dedup.append(r)
                allrows = dedup
            total = len(allrows)
            newest_at = max((r.get("created_at") or "" for r in allrows), default=None)
        except Exception:
            newest_at = None
        since = _days_since(newest_at, today)
        if label == "Submissions":
            # A tree sent in and a thumbs-up report are different animals
            # (Hidde, 2026-08-21), so the headline and the total both say
            # which kind arrived instead of the flattering generic word.
            trees_n = sum(1 for r in (allrows or [])
                          if r.get("kind") in ("tree", "city"))
            if since is not None and since <= 1:
                yday_ = (today - datetime.timedelta(days=1)).isoformat()
                fresh = [r for r in allrows if str(r.get("created_at"))[:10] >= yday_]
                fresh_trees = sum(1 for r in fresh if r.get("kind") in ("tree", "city"))
                fresh_fb = len(fresh) - fresh_trees
                parts = []
                if fresh_trees:
                    parts.append("%d tree submission%s" % (fresh_trees, "" if fresh_trees == 1 else "s"))
                if fresh_fb:
                    parts.append("%d feedback report%s" % (fresh_fb, "" if fresh_fb == 1 else "s"))
                ATTENTION.append("%s arrived %s (%d total)"
                                 % (" and ".join(parts) or "a submission", _ago(since), total))
            out.append("- %-12s %d total (%d trees sent, %d feedback), newest %s" % (
                label + ":", total, trees_n, total - trees_n, _ago(since)))
            continue
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


# The report chips and the two verdicts, which are OUR words rather than the
# reader's: a fixed list the control offers, so printing one publishes nothing
# about the person who tapped it.
CHIPS = {"wrong location", "dead or gone", "could not reach it",
         "could not tell which tree", "something else",
         "worth it", "not worth it"}


def feedback_section(today):
    """What readers actually told us, one line each, so the count can be judged.

    Hidde, 2026-08-22, after a day showed 16 feedback rows: "ik wil wel dat je
    kunt uitlezen of de feedback nuttig is." A count cannot answer that. Sixteen
    thumbs from one account on one afternoon is us testing the control; three
    wrong-location reports on three trees from three accounts is a work queue.
    The difference is visible only per row.

    What this prints and what it deliberately does not. Structure only: the
    day, the tree, the verdict or the chip, and a four-character marker for the
    account so repeat senders and our own test traffic are recognisable without
    naming anybody. The reader's own words are NOT printed here, because
    DATA.md sits in a public repository and a sentence somebody typed about a
    tree can carry anything. A note is flagged as present; reading it is a
    session job against the database, where it belongs.
    """
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not key:
        return None
    since = (today - datetime.timedelta(days=14)).isoformat()
    try:
        rows, _ = _supa("/rest/v1/submissions?select=id,created_at,kind,city,tree,why,"
                        "user_id,outcome&created_at=gte.%sT00:00:00&order=created_at.asc" % since, key)
    except Exception as e:
        return "**What readers told us**: unreadable today (%s)" % str(e)[:60]
    rows = [r for r in (rows or []) if r.get("id") not in TEST_SUBMISSION_IDS]
    if not rows:
        return None

    def who(r):
        uid = r.get("user_id")
        if not uid:
            return "no acct"
        return hashlib.sha1(str(uid).encode()).hexdigest()[:4]

    out = ["**What readers told us** (14 days, structure only; the words stay in the database)",
           "", "| Day | Tree | What | Note | From | Outcome |", "|---|---|---|---|---|---|"]
    per_acct = {}
    for r in rows:
        why = (r.get("why") or "").strip()
        head, _, tail = why.partition(":")
        # A form submission's `why` is the reader's own prose, and this file is
        # public: print what KIND it was, never the opening of the sentence.
        # The vote control's `why` is our own vocabulary and prints in full.
        if r.get("kind") in ("tree", "city", "correction", "privacy"):
            what = "%s sent in" % (r.get("kind") or "?")
            tail = ""
            detail_len = len(why)
        else:
            what = head.strip()[:34] or (r.get("kind") or "?")
            detail_len = 0
        detail = tail.strip()
        tree = (r.get("tree") or r.get("city") or "-")
        # A vote and a chip carry the chip word in the tail; a form submission
        # carries prose, which is the thing we do not print.
        # A chip comes from a closed list, so it is printed in full: it is our
        # own vocabulary, not the reader's words, and "14 chars" made the one
        # thing worth knowing unreadable (Hidde, 2026-08-22: "wat is de notitie
        # van 14 tekens"). Free prose from the form stays withheld.
        note = "-"
        if detail_len:
            note = "%d chars, read it in the database" % detail_len
        elif detail:
            note = detail if detail in CHIPS else "%d chars" % len(detail)
        w = who(r)
        per_acct[w] = per_acct.get(w, 0) + 1
        out.append("| %s | %s | %s | %s | %s | %s |" % (
            str(r.get("created_at"))[5:10], tree[:34], what, note, w, r.get("outcome") or "-"))
    lead = max(per_acct.items(), key=lambda x: x[1])
    if len(rows) >= 5 and lead[1] > len(rows) / 2:
        out += ["", "- %d of these %d came from one account (%s). At this volume that is "
                    "almost certainly our own testing rather than readers, and it should be "
                    "read that way until somebody checks the rows." % (lead[1], len(rows), lead[0])]
    else:
        out += ["", "- %d rows from %d accounts." % (len(rows), len(per_acct))]
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



def night_shift(today):
    """What the night runs actually achieved, as a table, every day.

    Hidde, 2026-08-18: "Wat hebben de nachtjes bereikt en kun je dat standaard
    in de daily digest vertellen." Until now the digest reported utilisation, an
    attempts-versus-worked count, which answers whether the windows were USED
    and not whether anything came out of them. He had to ask what the runs
    achieved, which is the question, so it goes in the file rather than in a
    person's memory.

    It reads data/run-health.json, which the workflow writes after every run
    whether the run says anything or not. That is the point of that file: a run
    that gives up is exactly the run that skips its own LOG.md entry.

    The denials column is the one to watch. It went dark for two days when the
    SDK renamed its field and was repaired on 2026-08-17; the first full night
    after showed 10 to 27 refused commands per run, which is a wall nobody could
    see before and is the best current lead on why short runs stop early.
    """
    path = os.path.join(ROOT, "data", "run-health.json")
    try:
        doc = json.load(open(path, encoding="utf-8"))
        runs = doc.get("runs", []) if isinstance(doc, dict) else list(doc)
    except Exception:
        return None
    yday = (today - datetime.timedelta(days=1)).isoformat()
    # A night belongs to the day it ENDS on, so take everything from 18:00 the
    # previous day onward: a run starting 23:16 and one starting 05:20 are the
    # same night's work and reading them into different days hides that.
    since = yday + "T18"
    rows = [r for r in runs if str(r.get("started", "")) >= since]
    if not rows:
        return None
    mins = sum(r.get("minutes") or 0 for r in rows)
    trees = sum(r.get("trees") or 0 for r in rows)
    commits = sum(r.get("commits") or 0 for r in rows)
    idle = sum(1 for r in rows if not (r.get("trees") or 0))
    out = ["", "**What the night shift did**", "",
           "| Started | Minutes | Trees | Commits | Refused | Cities |",
           "|---|---:|---:|---:|---:|---|"]
    for r in rows:
        out.append("| %s | %s | %s | %s | %s | %s |" % (
            str(r.get("started"))[5:16], r.get("minutes") if r.get("minutes") is not None else "-",
            r.get("trees") or 0, r.get("commits") or 0,
            r.get("denials") if r.get("denials") is not None else "-",
            city_names(r)))
    out.append("| **%d runs** | **%.0f** | **%d** | **%d** | | |"
               % (len(rows), mins, trees, commits))
    note = []
    if idle:
        note.append("%d of %d produced no trees" % (idle, len(rows)))
    d = [r.get("denials") for r in rows if r.get("denials")]
    if d:
        note.append("%d to %d commands refused per run" % (min(d), max(d)))
    unlogged = sum(1 for r in rows if r.get("logged") is False)
    if unlogged:
        note.append("%d wrote nothing to LOG.md" % unlogged)
    if note:
        out.append("")
        out.append("- " + "; ".join(note) + ".")

    made = night_work(since)
    if made:
        out.append("")
        out.append("**What they made**")
        out.append("")
        for line in made:
            out.append("- " + line)
    return "\n".join(out)


def city_names(run):
    """Which cities a run touched, for the night-shift table.

    Hidde, 2026-08-24: "kun je ook altijd vertellen welke steden de nachtruns
    hebben gedaan." The table had a Turns column, which is a number nobody has
    ever acted on, and no column for the one thing he asks about every time. So
    turns come out and cities go in.

    Reads the `cities` list run_health.py has written since the same day, with
    each city's own tree delta, and falls back to the older `cities_touched`
    count for the nights recorded before that. A run whose city list is empty
    but which committed something says "-" rather than nothing, because blank
    reads as missing data and a bookkeeping-only run is a fact.
    """
    cities = run.get("cities")
    if isinstance(cities, list) and cities:
        bits = []
        for c in cities[:4]:
            name = str(c.get("city", "")).replace("-", " ").title()
            d = c.get("trees") or 0
            bits.append("%s +%d" % (name, d) if d > 0 else name)
        if len(cities) > 4:
            bits.append("+%d more" % (len(cities) - 4))
        return ", ".join(bits)
    n = run.get("cities_touched")
    if n:
        return "%d city file(s), names not recorded" % n
    return "-"


def night_work(since):
    """The night's actual work, as the machine's own commit subjects.

    Hidde, 2026-08-20: "en wat hebben de nachtruns gedaan en kun je dat
    toevoegen aan de daily digest". The table above already answered how MUCH
    (minutes, turns, trees, commits) and he still had to ask what they DID,
    which means the table was answering the wrong question. Counts tell you the
    windows were used; they do not tell you a city opened.

    Read from git rather than from LOG.md on purpose: three of last night's five
    runs wrote nothing to LOG.md at all, and a run that gives up is exactly the
    run that skips its own entry. Its commits are still there.

    Filtered to the machine's own commits and to real work: claims, releases,
    run-health stubs, log entries and index regenerations are bookkeeping, and
    listing them would bury the four cities that actually opened.
    """
    bot = "claude[bot]"
    noise = ("Run health", "Claim ", "Release ", "Reclaim ", "LOG:", "Log ",
             "Regenerate", "Update first-seen", "Daily data digest",
             "Archive log", "Merge branch", "Push the ")
    try:
        out = subprocess.run(
            ["git", "-C", ROOT, "log", f"--since={since.replace('T', ' ')}:00",
             "--pretty=%ae\t%s"],
            capture_output=True, text=True, timeout=60)
        if out.returncode != 0:
            return []
    except Exception:
        return []
    lines = []
    for row in out.stdout.strip().splitlines():
        if "\t" not in row:
            continue
        email, subject = row.split("\t", 1)
        if bot not in email or subject.startswith(noise):
            continue
        lines.append(subject.strip())
    # Newest first is how git gives them and how LOG.md reads, so keep it.
    return lines[:14]


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


def _maybe_selftest():
    if "--selftest" in sys.argv:
        raise SystemExit(_selftest_trend())


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
        # Never fatal. This block is a bonus; the numbers that matter come from
        # Search Console, Supabase and the beacon, and losing all of those
        # because a proxy we do not use went away is how 2026-08-19 lost its
        # digest entirely.
        print("NOTE: Cloudflare zone fetch failed (%s); carrying on without it." % e)
        days = []

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
    block(feedback_section, today)
    block(funnel_section, today, token)

    gsc_latest = None
    gsc_data = None
    try:
        gsc_data = fetch_gsc(today)
        gsc_text, gsc_latest = gsc_section(gsc_data)
        blocks.append("**Where demand is going to waste**\n\n" + gsc_text)
        trend = trend_section(gsc_data)
        if trend:
            blocks.append(trend.strip())
    except Exception as e:
        blocks.append("Search Console: fetch failed today (%s); numbers resume tomorrow." % e)

    # Monday gets the full audience cut, every other day gets the three lines
    # that can actually move. A 28-day window barely differs from yesterday's
    # 28-day window, and printing it in full daily buries the blocks above it.
    block(audience_section, today, token, today.weekday() != 0)

    block(fetch_rum, token, today)
    block(night_shift, today)
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
        lang, slug = split_path(path)
        if lang != "en":
            continue
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
    _maybe_selftest()
    sys.exit(main())
