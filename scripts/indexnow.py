#!/usr/bin/env python3
"""Tell Bing (and every IndexNow engine) which pages changed. Written 2026-10-01.

Google demoted the whole site on 09-28. Bing does not follow Google's
judgement, and ChatGPT's web search reads Bing's index, so being fresh there is
the quickest channel that does not wait on Google. IndexNow is one POST: the
engine is told a URL changed and fetches it, instead of finding out on its own
schedule weeks later.

What it sends: every URL in the live sitemap whose lastmod falls in the last
--days days (default 2), because lastmod is dated by CONTENT since 2026-09-04
(scripts/lastmod.py) and so is credible. `--all` sends every URL once, for the
first submission. The key file is site/public/<KEY>.txt, which proves the site
is ours; engines fetch it to check.

Two channels, 2026-10-09. Bing's IndexNow endpoint has answered every ping
since 10-01 with 403 UserForbiddedToAccessSite, while the site is verified in
Bing Webmaster Tools and the key file is served (200, 32 bytes, checked from
here and with bingbot's user agent). So the refusal is Bing's, and Hidde gave
the Webmaster Tools API key instead ("fix the bing thing with this api key").
When IndexNow refuses and BING_API_KEY is set, the same URLs go through the
Bing Webmaster URL Submission API, which has a QUOTA (100 a day, 2,300 a
month for this site on the day it was wired) where IndexNow has none. So that
channel sends the newest pages first, up to what the quota endpoint says is
left today, and the rest wait for the next deploy. IndexNow is still tried
first on every run, because the day Bing accepts the key it costs nothing.

Gear, not product: no reader ever meets it, and if IndexNow disappears the
only loss is freshness on Bing. Never raises past a printed line.
"""
import datetime
import json
import os
import re
import sys
import urllib.parse
import urllib.request

HOST = "ancienttrees.app"
KEY = "81e2b7f644c7a01071949732c4937da8"
ENDPOINT = "https://api.indexnow.org/indexnow"
BATCH = 10000
# Bing Webmaster URL Submission API (the fallback). The key is Hidde's and
# lives in the BING_API_KEY secret, never in this file: it grants write access
# to the site's Bing account, unlike the IndexNow key above, which is public
# by design (the key file is served to anyone).
BWT = "https://ssl.bing.com/webmaster/api.svc/json/"
BWT_SITE = "https://%s/" % HOST
BWT_BATCH = 500  # the API's own per-request ceiling


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ancienttrees-indexnow"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def sitemap_entries(url, seen=None):
    """(loc, lastmod) for every page, following a sitemap index if there is one."""
    seen = seen or set()
    if url in seen:
        return []
    seen.add(url)
    body = get(url)
    out = []
    for block in re.findall(r"<sitemap>(.*?)</sitemap>", body, re.S):
        loc = re.search(r"<loc>(.*?)</loc>", block)
        if loc:
            out += sitemap_entries(loc.group(1).strip(), seen)
    for block in re.findall(r"<url>(.*?)</url>", body, re.S):
        loc = re.search(r"<loc>(.*?)</loc>", block)
        mod = re.search(r"<lastmod>(.*?)</lastmod>", block)
        if loc:
            out.append((loc.group(1).strip(), (mod.group(1).strip()[:10] if mod else "")))
    return out


def bwt_call(name, api_key, payload=None, query=""):
    url = BWT + name + "?apikey=" + api_key + query
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "ancienttrees-indexnow"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8", "replace")).get("d")


def submit_via_bing_api(entries, urls):
    """Send what the daily quota allows through the Bing Webmaster API.

    Newest lastmod first, and within a day the pages of sitemap.xml before
    those of sitemap-bing.xml (a finished page before a photo-less one). Returns
    how many were sent, or None when the channel is not available.
    """
    api_key = os.environ.get("BING_API_KEY", "").strip()
    if not api_key:
        print("indexnow: BING_API_KEY not set; the Bing Webmaster API channel is off")
        return None
    try:
        quota = bwt_call("GetUrlSubmissionQuota", api_key,
                         query="&siteUrl=" + urllib.parse.quote(BWT_SITE, safe=""))
        left = int(quota.get("DailyQuota", 0))
    except Exception as e:
        print("indexnow: Bing Webmaster API quota check failed (%s); nothing sent that way" % e)
        return None
    if left <= 0:
        print("indexnow: Bing Webmaster API daily quota is spent; the rest waits for tomorrow")
        return 0
    rank = {}
    for i, (u, m) in enumerate(entries):
        # entries keep sitemap order, sitemap.xml first; the first sighting wins
        rank.setdefault(u, (m, -i))
    ordered = sorted(urls, key=lambda u: rank.get(u, ("", 0)), reverse=True)
    todo = ordered[:left]
    sent = 0
    for i in range(0, len(todo), BWT_BATCH):
        batch = todo[i:i + BWT_BATCH]
        try:
            bwt_call("SubmitUrlBatch", api_key, {"siteUrl": BWT_SITE, "urlList": batch})
            sent += len(batch)
        except urllib.error.HTTPError as e:
            print("indexnow: Bing Webmaster API HTTP %d %s" % (e.code, e.read()[:200]))
            break
        except Exception as e:
            print("indexnow: Bing Webmaster API failed: %s" % e)
            break
    print("indexnow: %d of %d URLs sent through the Bing Webmaster API (quota left today was %d)%s"
          % (sent, len(urls), left,
             "; the other %d wait for the next deploy" % (len(urls) - sent) if len(urls) > sent else ""))
    return sent


def main(argv):
    send_all = "--all" in argv
    days = 2
    if "--days" in argv:
        days = int(argv[argv.index("--days") + 1])
    try:
        entries = sitemap_entries("https://%s/sitemap.xml" % HOST)
    except Exception as e:
        print("indexnow: could not read the sitemap (%s); nothing sent" % e)
        return 0
    # The pages Google alone is asked not to list (2026-10-08, the engine
    # split) are in sitemap-bing.xml and nowhere Google reads; Bing is the
    # engine behind IndexNow, so it hears about them like any other page.
    try:
        entries += sitemap_entries("https://%s/sitemap-bing.xml" % HOST)
    except Exception as e:
        print("indexnow: no sitemap-bing.xml (%s); Google-only pages not sent" % e)
    if send_all:
        # The noindexed pages too (2026-10-01): Bing only drops them once it
        # has refetched them and seen the tag.
        try:
            entries += sitemap_entries("https://%s/sitemap-recrawl.xml" % HOST)
        except Exception:
            pass
    since = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    urls = sorted({u for u, m in entries if send_all or (m and m >= since)})
    print("indexnow: %d URLs in the sitemap, %d to send (%s)"
          % (len(entries), len(urls), "all" if send_all else "lastmod since " + since))
    refused = 0
    for i in range(0, len(urls), BATCH):
        payload = {"host": HOST, "key": KEY,
                   "keyLocation": "https://%s/%s.txt" % (HOST, KEY),
                   "urlList": urls[i:i + BATCH]}
        req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json; charset=utf-8"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                print("indexnow: batch %d sent, HTTP %d" % (i // BATCH + 1, r.status))
        except urllib.error.HTTPError as e:
            # 202 is accepted-pending-key-check; 403 means the key file was not
            # found yet, which is normal on the very first deploy that adds it.
            print("indexnow: batch %d HTTP %d %s" % (i // BATCH + 1, e.code, e.read()[:200]))
            refused += 1
        except Exception as e:
            print("indexnow: batch %d failed: %s" % (i // BATCH + 1, e))
            refused += 1
    # A refusal used to end in exit 0 silently, so the workflow went green
    # while Bing had accepted nothing (2026-10-01). It then went red, and red
    # on a workflow that fires after every deploy mailed Hidde a failure
    # roughly fifteen times a day for a refusal only he can fix, in Bing
    # Webmaster Tools (2026-10-03: "Why are all night runs failing?"). So a
    # refusal is a visible warning annotation on the run, not a failure.
    if refused:
        sent = submit_via_bing_api(entries, urls)
        if not sent:
            print("::warning::indexnow: %d batch(es) refused or failed; Bing has "
                  "not accepted the key for this site yet" % refused)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
