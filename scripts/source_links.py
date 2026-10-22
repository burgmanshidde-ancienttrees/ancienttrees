#!/usr/bin/env python3
"""Dead source links on the trees Google indexes.

Written 2026-10-22 during the recovery push: a page whose sources lead to
404s costs trust with readers and with Google, and on that day 57 links on 53
indexed trees were dead (2 trees with every link dead) while the site also
linked 280 "url (note)" sources as one broken href (fixed in
site/src/lib/tree-sources.ts). This checks every http source of every tree
with an approved photograph (the trees Google is shown), HEAD then GET, 12 at
a time, 20 s timeout, skipping data/fetch-blocklist.json hosts, and prints
the 404/410s per tree. Rate limits (429) and refusals (403) are not deaths.

  python3 scripts/source_links.py          dead links, worst trees first
  python3 scripts/source_links.py --all    every tree, not only indexed ones

Fix a dead link by finding the page's new address (the host's search, the
Wayback Machine for the old text) or replacing it with another source that
says the same; never drop a tree's last source.
"""
import argparse
import concurrent.futures as cf
import glob
import json
import os
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) AncientTrees source check"}


def blocklist():
    try:
        bl = json.load(open(os.path.join(ROOT, "data", "fetch-blocklist.json")))
    except (OSError, ValueError):
        return set()
    return set(bl if isinstance(bl, list) else (bl.get("hosts") or bl.keys()))


def url_of(source):
    """The link in a source line: "url (note)" is common, and a closing
    bracket stays when the url opened one, as site/src/lib/tree-sources.ts does."""
    s = (source if isinstance(source, str) else (source or {}).get("url") or "").strip()
    if not s.startswith("http"):
        return None
    u = s.split()[0].rstrip(",.;")
    while u.endswith(")") and u.count("(") < u.count(")"):
        u = u[:-1]
    p = urllib.parse.urlsplit(u)
    return urllib.parse.urlunsplit((p.scheme, p.netloc.encode("idna").decode(),
                                    urllib.parse.quote(p.path, safe="/%:@()!$&'*+,;=-._~"),
                                    urllib.parse.quote(p.query, safe="=&%+/:,;"), p.fragment))


def check(job, block):
    city, tid, u = job
    host = urllib.parse.urlsplit(u).netloc
    if host in block or host.replace("www.", "") in block:
        return "blocked"
    for method in ("HEAD", "GET"):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, method=method, headers=UA), timeout=20) as r:
                return r.status
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (400, 403, 405, 429, 501):
                continue
            return e.code
        except Exception as e:
            if method == "GET":
                return e.__class__.__name__
    return "?"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    block = blocklist()
    jobs, per_tree = [], {}
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        city = os.path.basename(p)[:-5]
        for t in json.load(open(p)).get("trees") or []:
            if not a.all and (t.get("photo") or {}).get("status") != "approved":
                continue
            urls = [u for u in (url_of(s) for s in t.get("verified_sources") or []) if u]
            per_tree[t["id"]] = len(urls)
            jobs += [(city, t["id"], u) for u in dict.fromkeys(urls)]
    with cf.ThreadPoolExecutor(12) as ex:
        res = list(zip(jobs, ex.map(lambda j: check(j, block), jobs)))
    dead = {}
    for (city, tid, u), code in res:
        if code in (404, 410):
            dead.setdefault((city, tid), []).append(u)
    print(f"{len(res)} links on {len(per_tree)} trees; {sum(len(v) for v in dead.values())} dead on {len(dead)} trees")
    for (city, tid), urls in sorted(dead.items(), key=lambda kv: (len(kv[1]) < per_tree[kv[0][1]], kv[0])):
        tag = "EVERY LINK DEAD" if len(urls) >= per_tree[tid] else f"{len(urls)} of {per_tree[tid]}"
        print(f"  {city}/{tid}  {tag}")
        for u in urls:
            print(f"      {u}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
