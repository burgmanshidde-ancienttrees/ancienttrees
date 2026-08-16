#!/usr/bin/env python3
"""Japan's giant-tree database, crawled by prefecture.

`kyoju.biodic.go.jp`, the 巨樹・巨木林データベース: every tree in Japan over
300 cm girth. Licence PDL 1.0, proven 2026-08-04 in OPEN_DATA_SURVEY.md.

What it took to reach, recorded because none of it is guessable:

- There is no API and no bulk download. Search is a POST to `?_action=gtsearch`
  carrying `_token` and `csrf_token` scraped from the search page, plus a
  cookie. `sort` and `page` must both be present or the server answers
  "ソートが入力されていません" and silently re-renders the empty form.
- `place_filter=3` LOOKS like a map-radius search and is not one. Asked for a
  point in Hiroshima at zoom 10 it returned 76,368 records, which is the whole
  national total: the marker coordinates are ignored. Only `place_filter=1`
  with `prefecture_code` actually filters, and that is the route here.
- The species dropdown holds 503 options and is re-rendered on the results
  page, so anything that parses the page as text swallows it. Parse
  `ul.resultList` and nothing else.

**The licence caveat is solved by a field, not by judgement.** The corpus
warned that the database mixes ministry survey data (PDL 1.0) with citizen
submissions whose copyright stays with the poster, and that the interface does
not obviously separate them. It does: every row carries ユーザ, and the
ministry's own 1988/2000 survey records read `Admin`. Rows with any other user
are somebody's submission and are kept out of the register entirely.

**What this source does NOT have, correcting the 2026-08-04 entry: coordinates.**
That entry said "with measured girth, height, species, and location", and the
location is prefecture, municipality and an address line, never a lat/lon. The
detail page's map link renders a whole-Japan view with no marker for records
whose position is not published, and the schema carries 位置の公表について
("about publishing the position") with a reason-for-non-disclosure field beside
it, which is hard rule 10 written into the source. So this is a LEAD source: it
says which trees exist and how big they are, and pinning is a separate job.

Usage:
    python3 scripts/jp_kyoju.py --prefecture 34 --city 広島市
    python3 scripts/jp_kyoju.py --prefecture 34 --out data/leads/hiroshima.json
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import http.cookiejar

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://kyoju.biodic.go.jp/?_action=gtsearch"
UA = "Mozilla/5.0 (compatible; AncientTrees/1.0; +https://ancienttrees.app)"

# Prefecture codes are the standard JIS order, 1 Hokkaido to 47 Okinawa.
PREF = {1: "Hokkaido (Sapporo)", 23: "Aichi (Nagoya)", 27: "Osaka",
        28: "Hyogo (Kobe)", 34: "Hiroshima", 14: "Kanagawa (Kamakura)",
        26: "Kyoto", 29: "Nara", 40: "Fukuoka", 13: "Tokyo"}

FIELDS = ["ユーザ", "健全度", "都道府県", "市区町村", "報告件数",
          "独特の呼称", "樹種", "幹周", "樹高", "確認年月日"]


def session():
    cj = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    op.addheaders = [("User-Agent", UA), ("Referer", BASE)]
    page = op.open(BASE, timeout=30).read().decode("utf-8", "replace")
    tok = dict(re.findall(
        r'name="(_token|csrf_token)"\s+value="([^"]*)"', page))
    return op, tok


def fetch_page(op, tok, pref, page):
    # Two things here, and both fail silently rather than erroring.
    #
    # 1. The first request is _command=search; every later page is
    #    _command=changepage with a ZERO-BASED page number, which is what
    #    js/pager.js does (`form1.page.value = page - 1;
    #    execCmd('changepage')`).
    # 2. THE CSRF TOKEN ROTATES ON EVERY RESPONSE. Reusing the one from the
    #    search page returns HTTP 200 with a re-rendered empty form carrying
    #    "CSRFトークンが一致しませんでした" buried in it, so a crawler that
    #    misses this reads page one of a thousand-record prefecture and
    #    reports success. `tok` is therefore mutated in place from each
    #    response before the next request goes out.
    data = {"_action": "gtsearch",
            "_command": "search" if page == 0 else "changepage",
            "_token": tok["_token"], "csrf_token": tok["csrf_token"],
            "keyword": "", "species_name": "0", "diameter_from": "",
            "diameter_to": "", "height_from": "", "height_to": "",
            "proper_name": "", "is_branch": "0", "place_filter": "1",
            "prefecture_code": str(pref), "city_code": "0",
            "prefecture_code_label": "", "city_code_label": "",
            "sort": "0", "page": str(page)}
    req = urllib.request.Request(BASE, data=urllib.parse.urlencode(data).encode(),
                                 method="POST")
    body = op.open(req, timeout=45).read().decode("utf-8", "replace")
    fresh = dict(re.findall(
        r'name="(_token|csrf_token)"\s+value="([^"]*)"', body))
    tok.update({k: v for k, v in fresh.items() if v})
    return body


def parse(body):
    """Rows out of the result list. Split on the <li> items rather than
    matching the <ul>: each item contains its own nested lists, so a
    non-greedy `<ul>...</ul>` stops at the first inner close and returns
    nothing. One <dl> per tree. Fields are dt/dd pairs, read by flattening tags to separators
    and pairing each known label with the token after it. A label whose value
    is empty (many trees have no 独特の呼称) is followed directly by the next
    label, which is why the lookahead checks FIELDS before taking a value."""
    start = body.find('class="resultList"')
    if start < 0:
        return []
    chunk = body[start:]
    # Split on <dl>, not on <li>: only the FIRST item carries
    # class="section" and the other nine are bare <li>, so an li-class split
    # returns one row per page and silently loses 90 percent of the register.
    items = re.split(r"<dl[^>]*>", chunk)[1:]
    out = []
    for li in items:
        rid = re.search(r"report_id=(\d+)&(?:amp;)?branch_number=(\d+)", li)
        txt = re.sub(r"<[^>]+>", "\n", li)
        txt = txt.replace("&nbsp;", " ")
        lines = [x.strip() for x in txt.split("\n") if x.strip()]
        rec = {}
        for i, line in enumerate(lines):
            if line in FIELDS:
                nxt = lines[i + 1] if i + 1 < len(lines) else ""
                rec[line] = "" if nxt in FIELDS or nxt == "詳しく見る" else nxt
        if rid:
            rec["report_id"] = int(rid.group(1))
            rec["branch_number"] = int(rid.group(2))
        if rec.get("樹種"):
            out.append(rec)
    return out


def cm(v):
    m = re.match(r"(\d+(?:\.\d+)?)", (v or "").replace(",", ""))
    return float(m.group(1)) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefecture", type=int, required=True)
    ap.add_argument("--city", help="keep only rows whose 市区町村 contains this")
    ap.add_argument("--max-pages", type=int, default=200)
    ap.add_argument("--out")
    a = ap.parse_args()

    op, tok = session()
    rows, page = [], 0
    total = None
    while page < a.max_pages:
        body = fetch_page(op, tok, a.prefecture, page)
        if total is None:
            nums = [int(x.replace(",", "")) for x in
                    re.findall(r"([\d,]+)件", re.sub(r"<[^>]+>", "", body))]
            total = max(nums) if nums else 0
            print("prefecture %d: %d records" % (a.prefecture, total),
                  file=sys.stderr)
        got = parse(body)
        if not got:
            break
        rows.extend(got)
        page += 1
        if len(rows) >= total:
            break
        if page % 10 == 0:
            print("  %d/%d" % (len(rows), total), file=sys.stderr)
        time.sleep(0.4)      # somebody's ministry server, not an API

    if a.city:
        rows = [r for r in rows if a.city in (r.get("市区町村") or "")]

    # Ministry survey rows only. Anything else is a citizen submission whose
    # copyright belongs to the poster and falls outside PDL 1.0.
    admin = [r for r in rows if (r.get("ユーザ") or "").strip() == "Admin"]
    trees = [{
        "report_id": r.get("report_id"),
        "branch_number": r.get("branch_number"),
        "species_ja": r.get("樹種"),
        "name_ja": r.get("独特の呼称") or None,
        "girth_cm": cm(r.get("幹周")),
        "height_m": cm(r.get("樹高")),
        "health_ja": r.get("健全度"),
        # 良好 is good, 一部枯損 partly dead, 主幹折損 trunk broken. A vitality
        # field, which the corpus says registers never carry.
        "alive_hint": (r.get("健全度") or "").strip() != "枯死",
        "prefecture_ja": r.get("都道府県"),
        "municipality_ja": r.get("市区町村"),
        "surveyed": r.get("確認年月日"),
        "source": "https://kyoju.biodic.go.jp/?_action=gtsearchdetail&report_id=%s&branch_number=%s"
                  % (r.get("report_id"), r.get("branch_number")),
    } for r in admin]

    doc = {
        "source": "環境省生物多様性センター 巨樹・巨木林データベース "
                  "(Biodiversity Center of Japan, giant tree database)",
        "endpoint": "POST https://kyoju.biodic.go.jp/?_action=gtsearch with "
                    "place_filter=1 and prefecture_code; see scripts/jp_kyoju.py",
        "country": "Japan",
        "licence": "公共データ利用規約 1.0 (PDL 1.0), commercial reuse with "
                   "attribution",
        "licence_proof": "biodic.go.jp/copyright/terms_of_service.html, read "
                         "2026-08-04. The same page reserves user submissions "
                         "to their posters, which is why only ユーザ=Admin "
                         "rows (the ministry's own 1988/2000 survey) are kept "
                         "here.",
        "attribution": "環境省生物多様性センター 巨樹・巨木林データベース, "
                       "extract of 2026-08-16",
        "prefecture_code": a.prefecture,
        "prefecture": PREF.get(a.prefecture, str(a.prefecture)),
        "city_filter": a.city,
        "scope": "%d rows read, %d kept as ministry survey records"
                 % (len(rows), len(admin)),
        "caveat": "NO COORDINATES. The database gives prefecture, municipality "
                  "and an address line, never a lat/lon, and its schema carries "
                  "a position-disclosure field with a reason-for-withholding "
                  "beside it. So this is a lead list: it says which trees exist "
                  "and how big they are, and every pin is a separate job. Girth "
                  "is the survey figure at 確認年月日, often 2000, so add the "
                  "years since. Hard rule 10 still applies per tree.",
        "count": len(trees),
        "leads": trees,
    }
    out = a.out or os.path.join(ROOT, "data", "leads",
                                "jp-pref-%02d.json" % a.prefecture)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
    print("%d rows, %d ministry records -> %s"
          % (len(rows), len(trees), os.path.relpath(out, ROOT)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
