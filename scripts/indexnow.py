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

Gear, not product: no reader ever meets it, and if IndexNow disappears the
only loss is freshness on Bing. Never raises past a printed line.
"""
import datetime
import json
import re
import sys
import urllib.request

HOST = "ancienttrees.app"
KEY = "81e2b7f644c7a01071949732c4937da8"
ENDPOINT = "https://api.indexnow.org/indexnow"
BATCH = 10000


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
        print("::warning::indexnow: %d batch(es) refused or failed; Bing has "
              "not accepted the key for this site yet" % refused)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
