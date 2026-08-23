#!/usr/bin/env python3
"""Find the next batch of outreach addresses without doing it by hand.

Hidde, 2026-08-23: "een idee om de volgende batch aan nuttige email adressen
te gaan zoeken? we hebben er een hoop steden bij." He is right that the gap
moved: it used to be whole countries, and now it is CITIES. The Netherlands is
37 published cities against 25 contacts, Italy 24 against 23. Every city we
open has a local tree group, a friends-of-the-park society or a parish that
nobody has looked for.

Three jobs, and the split follows CLAUDE.md's rule that retrieval is code and
judgement is not:

  --gaps      which published cities and countries have no contact at all,
              ranked by how many trees we publish there. Pure arithmetic over
              our own files.
  --harvest   which sites we CITE on our tree pages have never been mailed,
              with government and municipal domains filtered out. This is the
              lane that produced Paulo Araujo and Prazske stromy, and it is
              free: the research already happened when the trees were written.
  --find D..  fetch the usual contact pages of a domain and read the address
              off it. Mechanical, so it is a script rather than an agent: an
              earlier hand-scout cost a session for 24 addresses.

What it deliberately does NOT do is decide who is worth writing to. The
measured rule (scripts/outreach_stats.py) is that groups attached to ONE place
answer and big institutions' general inboxes do not: gardens and palaces are 0
of 12. A machine cannot see that difference, so this prints candidates and a
session picks.

  python3 scripts/outreach_scout.py --gaps
  python3 scripts/outreach_scout.py --harvest
  python3 scripts/outreach_scout.py --find bomenstichtingutrecht.nl villaserra.it
"""
import collections
import glob
import json
import os
import re
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIMEOUT = 15          # every fetch gets a hard timeout (CLAUDE.md, 2026-08-06)

# Paths that carry an address on a small organisation's site, in the languages
# we actually write in. The homepage is last because it is the least likely to
# carry one and the most likely to be heavy.
PATHS = ["/contact", "/kontakt", "/contatti", "/contacto", "/kapcsolat",
         "/impressum", "/impresszum", "/about", "/contact-us", "/contacts",
         "/contacte", "/kontakty", "/colofon", "/over-ons", "/about-us",
         "/chi-siamo", "/quienes-somos", "/o-nas", "/mentions-legales", "/"]

# The homepage stays LAST, and what it is really for is its LINKS: three of
# four test sites hid their address behind a page this list would not have
# guessed (/impresszum, a Wordpress slug, a Dutch "Contact ons"), and each of
# them linked to it from the front page. So every page we fetch also donates
# its contact-looking links to the queue.
CONTACTISH = re.compile(
    r"contact|kontakt|contatti|contacto|contacte|kapcsolat|impresszum|"
    r"impressum|colofon|over-ons|about|chi-siamo|quienes-somos", re.I)
HREF = re.compile(r"href=[\"']([^\"']+)[\"']", re.I)
MAILTO = re.compile(r"mailto:([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})", re.I)

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# Obfuscations we have actually met: "(arobase)" on a French blog, "(at)" and
# "[at]" everywhere else.
DEOBF = [(re.compile(r"\s*\((?:at|arobase|apenstaartje)\)\s*", re.I), "@"),
         (re.compile(r"\s*\[(?:at|arobase)\]\s*", re.I), "@"),
         (re.compile(r"\s*\((?:dot|punt)\)\s*", re.I), ".")]
JUNK = ("noreply", "no-reply", "donotreply", "example.com", "sentry.io",
        "wixpress", "godaddy", "wordpress", "@2x.png", ".png", ".jpg", ".gif",
        ".webp", ".svg", "@sentry", "yourdomain", "domain.com")
# Not people: filtered out of --harvest, since a ministry's general inbox has
# never once answered us.
GOVISH = (".gov", "gov.", "comune.", "ajuntament", "ayuntamiento", "regione.",
          "gemeente", "municip", "opendata", "data.", "geo", "kommun",
          ".gv.at", "wien.gv", "berlin.de", "paris.fr", "canada.ca")


def load_contacts():
    seen = {}
    for f in glob.glob(os.path.join(ROOT, "data", "outreach-contacts*.json")):
        for c in json.load(open(f)):
            e = (c.get("email") or "").lower().strip()
            if e:
                seen.setdefault(e, c)
    return seen


def sent_addresses():
    d = json.load(open(os.path.join(ROOT, "data", "outreach-sent.json")))
    return {s["to"].lower() for s in d["sent"]}


def cities():
    out = []
    for f in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
        d = json.load(open(f))
        out.append((d["city"], d["country"], len(d["trees"]),
                    os.path.basename(f)[:-5]))
    return out


def gaps():
    contacts = load_contacts()
    by_city = collections.Counter()
    by_country = collections.Counter()
    for c in contacts.values():
        if c.get("city"):
            by_city[c["city"].lower()] += 1
        by_country[(c.get("country") or "").lower()] += 1
    rows = [(t, city, country, slug) for city, country, t, slug in cities()
            if by_city.get(city.lower(), 0) == 0]
    rows.sort(reverse=True)
    print(f"PUBLISHED CITIES WITH NO CONTACT OF THEIR OWN ({len(rows)}), "
          f"biggest first:\n")
    print(f"  {'trees':>5}  {'city':22} country")
    for t, city, country, slug in rows[:40]:
        mark = "  <- country has none either" if by_country.get(country.lower(), 0) == 0 else ""
        print(f"  {t:5}  {city[:22]:22} {country}{mark}")
    if len(rows) > 40:
        print(f"  ... and {len(rows)-40} more")
    return 0


def harvest():
    sent = sent_addresses()
    sent_domains = {a.split("@")[-1] for a in sent}
    dom = collections.Counter()
    where = collections.defaultdict(set)
    SKIP = ("wikipedia", "wikimedia", "monumentaltrees", "google", "facebook",
            "instagram", "youtube", "tripadvisor", "openstreetmap", "wikidata",
            "inaturalist", "flickr", "commons", "web.archive", "researchgate")
    for f in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
        d = json.load(open(f))
        for t in d["trees"]:
            for u in t.get("verified_sources") or []:
                h = urlparse(u).netloc.lower().replace("www.", "")
                if not h or any(s in h for s in SKIP):
                    continue
                dom[h] += 1
                where[h].add(d["city"])
    print("SITES WE CITE, NEVER MAILED, NOT GOVERNMENT (the lane that gave us "
          "Paulo Araujo and Prazske stromy):\n")
    print(f"  {'cited':>5} {'cities':>6}  domain")
    n = 0
    for h, c in dom.most_common():
        if c < 3 or h in sent_domains or any(g in h for g in GOVISH):
            continue
        n += 1
        print(f"  {c:5} {len(where[h]):6}  {h:38} [{', '.join(sorted(where[h])[:3])}]")
        if n >= 45:
            break
    print(f"\nRun --find on the ones worth writing to.")
    return 0


def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; ancienttrees.app contact lookup)"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        raw = r.read(400_000)
    try:
        return raw.decode("utf-8", "replace")
    except Exception:
        return ""


def find(domains):
    blocked = set()
    bl = os.path.join(ROOT, "data", "fetch-blocklist.json")
    if os.path.exists(bl):
        try:
            b = json.load(open(bl))
            blocked = set(b if isinstance(b, list) else b.get("hosts", b.keys()))
        except Exception:
            pass
    out = []
    for d in domains:
        d = d.strip().replace("https://", "").replace("http://", "").strip("/")
        if any(d in str(x) for x in blocked):
            print(f"{d}: on the fetch blocklist, skipped")
            continue
        found, source = None, None
        todo = [f"https://{d}{p}" for p in PATHS]
        tried = set()
        while todo:
            url = todo.pop(0)
            if url in tried or len(tried) > 20:
                continue
            tried.add(url)
            try:
                html = fetch(url)
            except Exception:
                continue
            for pat, rep in DEOBF:
                html = pat.sub(rep, html)
            # mailto: first. A site can obfuscate the visible text and still
            # carry a plain address in the link, and that is the address the
            # organisation itself chose to publish.
            hits = [m.group(1) for m in MAILTO.finditer(html)]
            hits += [m.group(0) for m in EMAIL.finditer(html)]
            hits = [h for h in hits if not any(j in h.lower() for j in JUNK)]
            own = [h for h in hits if h.lower().endswith(d.lower())]
            pick = own or hits
            # An organisation usually publishes several: info@ reaches a
            # person, biglietteria@ reaches the ticket desk. Measured on
            # villaserra.it, which handed back its box office until this
            # existed.
            GENERAL = ("info", "contact", "kontakt", "contatti", "contacto",
                       "mail", "post", "hello", "bureau", "secretariat",
                       "secretaria", "segreteria", "geral", "office",
                       "algemeen", "kancelaria", "sekretariat")
            pick.sort(key=lambda h: 0 if h.split("@")[0].lower().startswith(GENERAL) else 1)
            if pick:
                found, source = pick[0], url
                break
            for m in HREF.finditer(html):
                h = m.group(1)
                if not CONTACTISH.search(h) or h.startswith(("mailto:", "tel:", "#")):
                    continue
                if h.startswith("http") and d not in h:
                    continue
                full = h if h.startswith("http") else "https://" + d + "/" + h.lstrip("/")
                if full not in tried and full not in todo:
                    todo.append(full)
        if found:
            print(f"{d:34} {found:38} <- {source}")
            out.append({"domain": d, "email": found, "source_url": source})
        else:
            print(f"{d:34} {'(no address found, form only?)':38}")
            out.append({"domain": d, "email": None, "source_url": None,
                        "note": "no address on the usual contact pages"})
    p = os.path.join(ROOT, "data", "outreach-candidates.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print(f"\nwritten to {p}")
    return 0


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    if a[0] == "--gaps":
        return gaps()
    if a[0] == "--harvest":
        return harvest()
    if a[0] == "--find":
        return find(a[1:])
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
