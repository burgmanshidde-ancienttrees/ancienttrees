#!/usr/bin/env python3
"""Who we cite, and how to write to them: the cheap address list for link asks.

Hidde, 2026-10-15: daily outreach for months, aimed at backlinks, ambassadors
and attention, with addresses that cost code rather than tokens. The warmest
cold contact we have is a site we already cite as a source: the mail is true
("our page on <tree> names you, with a link") and specific, and it is the shape
of the one link ask that worked (getLISBON, 2026-09-04).

Per source domain in data/cities/*.json `verified_sources`:
- the trees and cities that cite it (the mail names a real tree);
- registers, government portals and big platforms are skipped: they do not
  link back and nobody reads their inbox (SKIP below);
- domains we ever mailed, or that are on the do-not-contact list, are skipped
  (data/outreach-sent.json);
- the homepage and up to three contact / about / impressum pages are read
  with press_desks.scrape(), and the addresses found are scored.

The output names organisations' addresses, so it goes to
data/outreach-source-contacts.json, gitignored (data/outreach-*.json) and
synced by private_store.py. Never commit it. Nothing here sends.

    python3 scripts/source_contacts.py --top 60
    python3 scripts/source_contacts.py --list        (domains only, no fetching)
"""
import argparse
import glob
import json
import os
import re
import sys
import time
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import press_desks  # noqa: E402

OUT = os.path.join(ROOT, "data", "outreach-source-contacts.json")
SENT = os.path.join(ROOT, "data", "outreach-sent.json")

SKIP = re.compile(
    r"wikipedia|wikimedia|wikidata|wikivoyage|google|monumentaltrees|youtube|"
    r"facebook|instagram|twitter|tripadvisor|archive\.org|openstreetmap|"
    r"inaturalist|gbif|flickr|arcgis|opendata|^data\.|\.gov(\.|$)|gov\.|\.go\.jp|"
    r"gouv\.fr|\.gob\.|regione\.|masaf|gdos|bunka|biodic|bayern\.de$|"
    r"amazon|bing\.|apple\.com|jstor|doi\.org|researchgate|sciencedirect|"
    r"springer|wiley|academia\.edu|nytimes|theguardian|bbc\.|cnn\.|"
    r"atlasobscura|lonelyplanet|timeout\.com|britannica|kew\.org$|"
    # municipal, regional and register portals: they do not link back
    r"comune\.|ajuntament|^cm-|\.cm-|\.lg\.jp|\.gv\.|overheid|gencat|gva\.es|caib\.es|"
    r"metropole|stadtplan|geoportal|geoproxy|^sig|\.sig\.|^gdi\.|^maps\.|^service\.|"
    r"inventaris|heritage\.brussels|onf\.fr|icnf|saugoma|stvk\.|nature\.cz|lubw|pdok|"
    r"public\.lu|nycgovparks|outdooractive|^city\.|^www2?\.city\.|kunishitei")

CITY_PORTAL = None  # filled in main(): <cityname>.<tld> is the town hall


def is_city_portal(host, names):
    first = host.split(".")[0].replace("-", "")
    return first in names or first.removeprefix("my") in names or first.removesuffix("city") in names


def known_text():
    """Everything we ever wrote down about outreach, lowercased: a domain that
    appears in it was mailed or discussed under another address (the Tree
    Register as treeregister.org, Rainer Lippert at freenet, 2026-10-15)."""
    parts = []
    for p in (SENT, os.path.join(ROOT, "drafts", "OUTREACH.md")):
        try:
            parts.append(open(p, encoding="utf-8").read().lower())
        except OSError:
            pass
    return "\n".join(parts)


def sent_domains():
    try:
        doc = json.load(open(SENT))
    except (OSError, ValueError):
        return set(), set()
    mailed = {(m.get("to") or "").lower().split("@")[-1] for m in doc.get("sent", [])}
    dnc = {a.lower().lstrip("@").split("@")[-1] for a in doc.get("do_not_contact", [])}
    return mailed, dnc


def cited():
    """{domain: [{city, id, name, url}]} from every published tree's sources."""
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        slug = os.path.basename(f)[:-5]
        city = json.load(open(f, encoding="utf-8"))
        for t in city.get("trees", []):
            for s in t.get("verified_sources") or []:
                url = s if isinstance(s, str) else (s.get("url") or "")
                host = urllib.parse.urlparse(url).netloc.lower().removeprefix("www.")
                if not host or SKIP.search(host):
                    continue
                rows = out.setdefault(host, [])
                if not any(r["id"] == t["id"] for r in rows):
                    rows.append({"city": slug, "id": t["id"], "name": t["name"], "url": url})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=40)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    mailed, dnc = sent_domains()
    names = set()
    for f in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
        slug = os.path.basename(f)[:-5]
        names.add(slug.replace("-", ""))
        names.add(json.load(open(f, encoding="utf-8")).get("city", "").lower().replace(" ", "").replace("-", ""))
    names |= {"sevilla", "nuernberg", "muenchen", "wien", "praha", "roma", "firenze", "napoli", "torino",
              "lisboa", "bruxelles", "brussel", "koeln", "kobenhavn", "warszawa", "krakow", "bcnsostenible"}
    sources = {h: r for h, r in cited().items() if not is_city_portal(h, names)}
    ranked = sorted(sources.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    known = known_text()

    def seen(h):
        core = h.split(".")[-2] if h.count(".") >= 1 else h
        return h in mailed or h in dnc or h.split(".", 1)[-1] in dnc or (len(core) > 5 and core in known)
    fresh = [(h, rows) for h, rows in ranked if not seen(h)]
    print(f"{len(sources)} citable domains, {len(fresh)} never mailed")
    if args.list:
        for h, rows in fresh[:args.top]:
            print(f"{len(rows):4}  {h:40} {', '.join(sorted({r['city'] for r in rows}))[:60]}")
        return 0

    try:
        doc = json.load(open(OUT))
    except (OSError, ValueError):
        doc = {"_note": "Contact addresses of the sites our trees cite, from scripts/source_contacts.py. Private: never commit.",
               "domains": {}}
    blocked = press_desks.blocked_hosts()
    done = 0
    for host, rows in fresh:
        if done >= args.top:
            break
        if host in doc["domains"] and doc["domains"][host].get("checked"):
            continue
        city = rows[0]["city"].replace("-", " ")
        emails, note = press_desks.scrape("https://" + host + "/", city, blocked)
        own = [e for e in emails if e.split("@")[-1].endswith(host.split(".", 1)[-1]) or e.split("@")[-1] == host]
        doc["domains"][host] = {"trees": rows, "emails": own or emails, "fetch": note,
                                "checked": time.strftime("%Y-%m-%d")}
        done += 1
        print(f"{len(rows):3} trees  {host:38} {', '.join((own or emails)[:2]) or '-':45} {note}")
        json.dump(doc, open(OUT, "w"), ensure_ascii=False, indent=1)
        time.sleep(1)
    found = sum(1 for d in doc["domains"].values() if d["emails"])
    print(f"written to {os.path.relpath(OUT, ROOT)}: {found} of {len(doc['domains'])} domains have an address")
    return 0


if __name__ == "__main__":
    sys.exit(main())
