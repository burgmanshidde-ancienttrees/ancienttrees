#!/usr/bin/env python3
"""Find the official visit-the-city tourism site of every roster city, and its inbox.

Hidde, 2026-10-20 ("start doing all this"): a new outreach group. A visit-the-city
site links to free local resources on its parks or green page, which a register
or a ministry never does. The ask is one line: would our map of the city's old
trees fit as a resource there. The strategy row lives in OUTREACH_STRATEGY.md
(group "tourism", two a day); this script is the feeder, so the addresses cost
code rather than tokens. It never sends anything.

How it works, per roster city (data/depth-roster-frozen.json, the cities Google
showed before the 09-28 demotion; focus countries first, then by impressions):
1. The city's Wikidata item, through its Wikipedia title in data/city-aliases.json.
   P2872 (tourist office) and that office's P856 (official website) win; the
   city's own P856 counts only when its host reads as a tourism site, since a
   municipality's official website is the town hall.
2. Otherwise the city's English Wikivoyage page: the tourism-looking domain it
   links most often is nearly always the official one (visitbath.co.uk 20 times).
3. Otherwise the common shapes are probed: visit<city>.<tld>, <city>.travel,
   tourism.<city>.<tld>, vvv<city>.nl, <city>-tourisme.fr and so on, with the
   local spelling as well as the English one. A host counts when it answers 200,
   is not a parked domain, and still carries the city's name after redirects.
   A pattern hit whose homepage never calls itself official is marked
   "pattern, unverified": look before mailing.
4. The homepage and its contact, press and about pages (at most four) are read,
   every address found is scored: press and editorial desks first, then the
   general inbox; booking, subscriptions, ads, privacy and jobs addresses are
   dropped. Every fetch has a hard 20 s timeout; hosts in
   data/fetch-blocklist.json are skipped.

The output holds organisations' addresses, so it goes to
data/outreach-tourism-sites.json, gitignored (data/outreach-*.json) and synced
by private_store.py like the other outreach files. Never commit it.
scripts/contacts_db.py reads it into the "tourism" segment.

    python3 scripts/tourism_sites.py --top 40
    python3 scripts/tourism_sites.py --city lisbon
    python3 scripts/tourism_sites.py --top 40 --no-fetch   (sites only, no inbox scraping)
    python3 scripts/tourism_sites.py --list                (what the file holds)
"""
import argparse
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

OUT = os.path.join(ROOT, "data", "outreach-tourism-sites.json")
ROSTER = os.path.join(ROOT, "data", "depth-roster-frozen.json")
ALIASES = os.path.join(ROOT, "data", "city-aliases.json")
BLOCKLIST = os.path.join(ROOT, "data", "fetch-blocklist.json")
UA = "Mozilla/5.0 (compatible; AncientTreesBot/1.0; +https://ancienttrees.app)"
TIMEOUT = 20  # the repo's rule: every fetch has a hard timeout (curl -m 20)

# passcheck.FOCUS_COUNTRIES, repeated here so a feeder never imports the gate.
FOCUS = ("United States", "United Kingdom", "Ireland", "Japan", "France", "Spain",
         "Portugal", "Italy", "Germany", "Netherlands", "Belgium", "Luxembourg",
         "Austria", "Switzerland", "Denmark", "Norway", "Sweden", "Australia", "Canada")
TLD = {"United States": "com", "United Kingdom": "co.uk", "Ireland": "ie", "Japan": "jp",
       "France": "fr", "Spain": "es", "Portugal": "pt", "Italy": "it", "Germany": "de",
       "Netherlands": "nl", "Belgium": "be", "Luxembourg": "lu", "Austria": "at",
       "Switzerland": "ch", "Denmark": "dk", "Norway": "no", "Sweden": "se",
       "Australia": "com.au", "Canada": "ca", "Czech Republic": "cz", "Czechia": "cz",
       "Poland": "pl", "Hungary": "hu", "Greece": "gr", "Singapore": "sg",
       "South Korea": "kr", "Iceland": "is", "Turkey": "com.tr", "Croatia": "hr"}
LANG = {"United States": "en", "United Kingdom": "en", "Ireland": "en", "Australia": "en",
        "Canada": "en", "Singapore": "en", "Japan": "ja", "France": "fr", "Spain": "es",
        "Portugal": "pt", "Italy": "it", "Germany": "de", "Austria": "de", "Switzerland": "de",
        "Netherlands": "nl", "Belgium": "nl", "Luxembourg": "fr", "Denmark": "en",
        "Norway": "en", "Sweden": "en", "Czech Republic": "en", "Czechia": "en",
        "Poland": "en", "Hungary": "en", "Greece": "en", "Iceland": "en"}
# Where the country's language is not the city's.
LANG_CITY = {"brussels": "fr", "geneva": "fr", "lausanne": "fr", "montreal": "fr",
             "quebec-city": "fr", "luxembourg-city": "fr", "bilbao": "es", "barcelona": "es"}

# A host that reads as a tourism site (shares its shape with contacts_db.TOURISM).
TOURISM_HOST = re.compile(r"visit|tourism|turism|tourisme|toerisme|turisme|vvv|\.travel$|"
                          r"fremdenverkehr|visitor|welcome|iamsterdam|"
                          r"jetaime|convention|cvb|experience|discover|explore|^go[a-z]+\.org$|"
                          r"turismo|tourist|incoming|cityguide|guide", re.I)
CONTACT_WORDS = ("contact", "contacto", "contatti", "kontakt", "impressum", "press", "presse",
                 "prensa", "stampa", "pers/", "/pers", "media", "about", "over-ons", "chi-siamo",
                 "quienes-somos", "a-propos", "inquiry", "newsroom", "redaktion", "redactie",
                 "sala-de-prensa", "sala-stampa", "pressroom", "team")
GOOD = {"press": 3, "presse": 3, "communiques": 3, "communique": 3, "prensa": 3, "stampa": 3, "pers": 3, "media": 3,
        "redaktion": 3, "redactie": 3, "redaccion": 3, "redazione": 3, "editorial": 3,
        "content": 3, "communication": 2, "kommunikation": 2, "comunicacion": 2,
        "comunicazione": 2, "comunicacao": 2, "info": 2, "contact": 2, "contacto": 2,
        "contatti": 2, "kontakt": 2, "hello": 2, "hallo": 2, "hola": 2, "office": 1,
        "tourism": 1, "turismo": 1, "tourisme": 1, "toerisme": 1, "visit": 1, "welcome": 1,
        "mail": 1, "post": 1, "enquiries": 2, "inquiry": 2, "marketing": 1}
BAD = ("booking", "reserv", "buchung", "prenot", "hotel", "ticket", "shop", "store",
       "newsletter", "subscri", "abo@", "abonn", "privacy", "datenschutz", "dpo", "gdpr",
       "job", "career", "karriere", "vacature", "stage@", "intern", "recruit", "advert",
       "anzeig", "werbung", "ads@", "sales", "noreply", "no-reply", "webmaster",
       "invoice", "factur", "billing", "accounting", "example", "beispiel", "domain",
       "sentry", "wixpress", "officestation", "support@", "helpdesk", "abuse", "security", "legal",
       "membership", "member", "partner", "b2b", "trade@", "convention@", "meetings",
       "group", "ticketing", "complaint", "klacht", "lost", "found", "wifi", "accessibil",
       "username", "user@", "name@", "email@", "mail@mail", "yourname", "nome@", "voornaam")
EMAIL = re.compile(r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@(?:[A-Za-z0-9-]+\.)+"
                   r"[a-z]{2,24}(?![A-Za-z0-9-])")  # .brussels, .travel, .info and the rest
FOOTPRINT = re.compile(r"\.(?:png|jpe?g|gif|webp|svg|css|js|woff2?)$", re.I)


def load(path, default):
    try:
        return json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        return default


def get(url, accept="text/html"):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept,
                                               "Accept-Language": "en,*;q=0.5"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read(2_500_000).decode("utf-8", "replace"), r.geturl(), r.status  # visit.brussels pages run past 900 kB


def blocked_hosts():
    d = load(BLOCKLIST, {})
    items = d.get("hosts", d) if isinstance(d, dict) else d
    if isinstance(items, dict):
        return {h.lower() for h in items}
    return {(h if isinstance(h, str) else h.get("host", "")).lower() for h in items}


def host_of(url):
    return urllib.parse.urlparse(url).netloc.lower().removeprefix("www.")


def is_blocked(url, blocked):
    h = host_of(url)
    return h in blocked or "www." + h in blocked


def roster_cities():
    """[(slug, impressions)] for every roster city with a city file, focus countries first."""
    roster = load(ROSTER, {}).get("cities", {})
    rows = []
    for slug, v in roster.items():
        city = load(os.path.join(ROOT, "data", "cities", slug + ".json"), None)
        if not city or not city.get("trees"):
            continue  # a country or region page, or a city not yet published
        rows.append((slug, city.get("country", ""), int(v.get("impressions", 0))))
    rows.sort(key=lambda r: (r[1] not in FOCUS, -r[2]))
    return rows


def city_names(slug, city):
    """English name, local spellings and the Wikipedia title for one city."""
    al = load(ALIASES, {})
    english = city.get("city", slug)
    local = [k for k, v in (al.get("aliases") or {}).items() if v == slug]
    title = (al.get("wikipedia_titles") or {}).get(slug) or english
    return english, local, title


def wikidata_item(title):
    url = ("https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&redirects=1"
           "&ppprop=wikibase_item&format=json&titles=" + urllib.parse.quote(title))
    body, _, _ = get(url, "application/json")
    for page in json.loads(body).get("query", {}).get("pages", {}).values():
        q = page.get("pageprops", {}).get("wikibase_item")
        if q:
            return q
    return None


def wikidata_claims(qid):
    url = ("https://www.wikidata.org/w/api.php?action=wbgetentities&props=claims|labels"
           "&languages=en&format=json&ids=" + qid)
    body, _, _ = get(url, "application/json")
    ent = json.loads(body).get("entities", {}).get(qid, {})
    return ent.get("claims", {}), ent.get("labels", {}).get("en", {}).get("value", "")


def claim_values(claims, prop):
    out = []
    for c in claims.get(prop, []):
        v = c.get("mainsnak", {}).get("datavalue", {}).get("value")
        if isinstance(v, dict) and "id" in v:
            out.append(v["id"])
        elif isinstance(v, str):
            out.append(v)
    return out


def wikidata_tourism(title):
    """(site, org, how) from Wikidata, or (None, None, note)."""
    qid = wikidata_item(title)
    if not qid:
        return None, None, "no wikidata item"
    claims, _ = wikidata_claims(qid)
    time.sleep(1)
    for office in claim_values(claims, "P2872"):  # tourist office
        oc, name = wikidata_claims(office)
        sites = claim_values(oc, "P856")
        if sites:
            return sites[0], name, "wikidata P2872 " + office
        time.sleep(1)
    for site in claim_values(claims, "P856"):
        if TOURISM_HOST.search(host_of(site)):
            return site, "", "wikidata P856 of " + qid
    return None, None, "wikidata " + qid + " holds no tourist office"


PARKED = re.compile(r"godaddy|sedo\.com|hugedomains|afternic|dan\.com|domain (?:is )?for sale|"
                    r"buy this domain|parked (?:free|domain)|this domain (?:may be|is) for sale|"
                    r"domainmarket|undeveloped\.com|namecheap", re.I)


def wikivoyage_tourism(title, names):
    """The tourism-looking domain the city's English Wikivoyage page links most."""
    url = ("https://en.wikivoyage.org/w/api.php?action=parse&prop=wikitext&redirects=1"
           "&format=json&page=" + urllib.parse.quote(title))
    body, _, _ = get(url, "application/json")
    text = json.loads(body).get("parse", {}).get("wikitext", {}).get("*", "")
    counts = {}
    for u in re.findall(r"https?://[^\s|\]}<>\"']+", text):
        h = host_of(u)
        if not h or "wiki" in h:
            continue
        if TOURISM_HOST.search(h) and any(n in compact(h) for n in names):
            counts[h] = counts.get(h, 0) + 1
    if not counts:
        return None
    return "https://" + max(counts, key=counts.get) + "/"


def compact(name):
    name = name.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        name = name.replace(a, b)
    name = re.sub(r"[àáâã]", "a", name)
    name = re.sub(r"[èéêë]", "e", name)
    name = re.sub(r"[ìíî]", "i", name)
    name = re.sub(r"[òóôõ]", "o", name)
    name = re.sub(r"[ùúû]", "u", name)
    return re.sub(r"[^a-z0-9]", "", name)


def pattern_hosts(slug, english, local, country):
    """The host shapes official tourism sites take, most common first."""
    names = []
    # Local spelling first: visitlisboa.com is Turismo de Lisboa, visitlisbon.org is not.
    for n in local + [english, slug.replace("-", "")]:
        c = compact(n)
        if c and c not in names:
            names.append(c)
    tld = TLD.get(country, "com")
    hosts = []
    for c in names:
        shapes = [f"visit{c}.com", f"visit{c}.{tld}", f"visit{c}.org", f"{c}.travel",
                  f"visit{c}.travel", f"tourism.{c}.{tld}", f"visit-{c}.{tld}",
                  f"{c}tourism.com", f"{c}tourism.{tld}", f"go{c}.org"]
        if country == "Netherlands":
            shapes = [f"vvv{c}.nl", f"visit{c}.nl", f"visit{c}.com"] + shapes
        if country == "Belgium":
            shapes = [f"visit{c}.be", f"visit.{c}.be"] + shapes
        if country == "France":
            shapes = [f"{c}-tourisme.com", f"{c}-tourisme.fr", f"tourisme-{c}.fr",
                      f"{c}tourisme.com", f"{c}-tourisme.org"] + shapes
        if country == "Spain":
            shapes = [f"visita{c}.es", f"visit{c}.com", f"turismo{c}.com", f"turismo.{c}.es",
                      f"{c}turismo.com", f"visita.{c}.eu", f"es{c}.com"] + shapes
        if country == "Italy":
            shapes = [f"turismo{c}.it", f"{c}turismo.it", f"turismo.{c}.it", f"visit{c}.it",
                      f"visit{c}.com", f"{c}welcome.com"] + shapes
        if country == "Portugal":
            shapes = [f"visit{c}.pt", f"visit{c}.com", f"visit{c}.travel"] + shapes
        if country in ("Germany", "Austria", "Switzerland"):
            shapes = [f"visit{c}.de", f"{c}.travel", f"{c}-tourismus.de", f"{c}tourismus.de",
                      f"{c}.info", f"{c}-tourismus.at", f"{c}-tourism.ch", f"{c}tourismus.ch"] + shapes
        if country == "United Kingdom":
            shapes = [f"visit{c}.co.uk", f"visit{c}.com", f"visit{c}.org", f"{c}.org"] + shapes
        if country == "Japan":
            shapes = [f"go{c}.org", f"{c}.travel", f"visit{c}.jp", f"visit-{c}.jp",
                      f"{c}-tourism.jp", f"{c}-tourism.org"] + shapes
        for h in shapes:
            if h not in hosts:
                hosts.append(h)
    return hosts


def answers(host, blocked):
    """The site's final URL when the host answers 200, else None. DNS failures are quick."""
    if host in blocked or "www." + host in blocked:
        return None
    try:
        socket.gethostbyname(host)
    except OSError:
        return None
    for url in ("https://" + host + "/", "https://www." + host + "/", "http://" + host + "/"):
        try:
            body, final, status = get(url)
        except urllib.error.HTTPError as e:
            if e.code == 403:
                return "403:" + url  # a real site behind a bot wall; the caller records it
            continue
        except (urllib.error.URLError, OSError, ValueError):
            continue
        if status == 200 and len(body) > 500 and not PARKED.search(body[:30000]):
            return final
    return None


def score(addr, site, names):
    a = addr.lower()
    local = a.split("@")[0]
    if any(w in a for w in BAD):
        return None
    if FOOTPRINT.search(a) or len(local) > 40:
        return None
    s = 0
    for w, pts in GOOD.items():
        if w in local:
            s = max(s, pts)
    if s == 0 and "." in local:
        s -= 1  # firstname.lastname: a person, kept below every desk address
    if any(n and n in a for n in names):
        s += 1
    site_host = host_of(site)
    mail_host = a.split("@")[-1]
    if mail_host.split(".")[-2:] != site_host.split(".")[-2:]:
        s -= 2  # another organisation's domain (the city hall, a newsletter tool)
    return s


OFFICIAL = re.compile(r"\b(?:official|oficial|officiel|offiziell|officieel|ufficiale|officiële|"
                      r"公式|offici[ae]l)\b", re.I)


def claims_official(home):
    """Does the homepage call itself the official site? Only the title, meta
    description and the first visible text count, so a footer link to the
    city hall does not."""
    head = re.search(r"<head.*?</head>", home, re.S | re.I)
    head = head.group(0) if head else home[:20000]
    return bool(OFFICIAL.search(re.sub(r"<[^>]+>", " ", head)))


def contact_links(home, site):
    host = host_of(site)
    links = []
    for href in re.findall(r'href=["\']([^"\'#]+)', home):
        low = href.lower()
        if any(w in low for w in CONTACT_WORDS) and not low.startswith("mailto:"):
            full = urllib.parse.urljoin(site, href)
            if host_of(full) == host and full not in links:
                links.append(full)
    # press and contact pages before "about" pages
    links.sort(key=lambda u: 0 if re.search(r"press|presse|prensa|stampa|/pers|media|contact|kontakt", u, re.I) else 1)
    return links


def unhide(html):
    """Addresses hidden from harvesters: hello&#64;visit.brussels, info [at] site.de."""
    html = html.replace("&#64;", "@").replace("&#x40;", "@").replace("&#064;", "@")
    html = re.sub(r"\s*(?:\[at\]|\(at\)|\{at\})\s*", "@", html, flags=re.I)
    return re.sub(r"\s*(?:\[dot\]|\(dot\))\s*", ".", html, flags=re.I)


def scrape(site, names, blocked):
    """([(score, address, page)], note) for one site. The note says when the
    homepage never calls itself official: a pattern hit (visit<city>.org) can
    be a private guide, so those rows get a look before a mail goes out."""
    if is_blocked(site, blocked):
        return [], "blocklisted"
    try:
        home, site, _ = get(site)
    except Exception as e:  # a dead or slow site is a note, not a stop
        return [], "home failed: %s" % type(e).__name__
    home = unhide(home)
    official = claims_official(home)
    found = {}
    for a in EMAIL.findall(home):
        found.setdefault(a.lower(), site)
    for a in re.findall(r"mailto:([^\"'?]+)", home):
        found.setdefault(urllib.parse.unquote(a).strip().lower(), site)
    links = contact_links(home, site)
    for link in links[:6]:
        try:
            page, _, _ = get(link)
        except Exception:
            continue
        page = unhide(page)
        for a in EMAIL.findall(page):
            found.setdefault(a.lower(), link)
        for a in re.findall(r"mailto:([^\"'?]+)", page):
            found.setdefault(urllib.parse.unquote(a).strip().lower(), link)
        time.sleep(1)
    out = []
    for a, page in found.items():
        a = a.strip(".")
        if a.startswith("u003e"):
            a = a[5:]
        if not EMAIL.fullmatch(a):
            continue
        s = score(a, site, names)
        if s is not None:
            out.append((s, a, page))
    out.sort(key=lambda x: (-x[0], x[1]))
    return out[:5], "ok, %d contact page(s) read%s" % (min(6, len(links)), "" if official else "; homepage never says official")


def photo_trees(city):
    return [t["id"] for t in city.get("trees", [])
            if (t.get("photo") or {}).get("status") == "approved" and (t.get("photo") or {}).get("url")]


def lookup(slug, blocked, fetch=True):
    city = load(os.path.join(ROOT, "data", "cities", slug + ".json"), {})
    english, local, title = city_names(slug, city)
    country = city.get("country", "")
    row = {"city": english, "country": country, "language": LANG_CITY.get(slug) or LANG.get(country, "en"),
           "type": "tourism", "checked": time.strftime("%Y-%m-%d"),
           "trees": photo_trees(city), "tree_count": len(city.get("trees", []))}
    site = org = None
    try:
        site, org, how = wikidata_tourism(title)
    except Exception as e:
        how = "wikidata failed: %s" % type(e).__name__
    if site and is_blocked(site, blocked):
        site, how = None, how + " (blocklisted)"
    walled = None
    if site:
        final = answers(host_of(site), blocked)
        if not final:
            how += " (does not answer)"
            site = None
        elif final.startswith("403:"):
            walled, site = final[4:], None
        else:
            site = final
    names = [compact(n) for n in [english] + local]
    if not site:
        try:
            wv = wikivoyage_tourism(title, names)
        except Exception as e:
            wv, how = None, how + "; wikivoyage failed: %s" % type(e).__name__
        if wv and not is_blocked(wv, blocked):
            final = answers(host_of(wv), blocked)
            if final and final.startswith("403:"):
                walled = walled or final[4:]
            elif final and any(n in compact(host_of(final)) for n in names):
                site, how = final, "wikivoyage " + host_of(wv)
    if not site:
        for h in pattern_hosts(slug, english, local, country):
            final = answers(h, blocked)
            if final and final.startswith("403:"):
                walled = walled or final[4:]
                continue
            # the redirect target must still carry the city's name: visitpalermo.it
            # lands on a private agency's wonderfulitaly.eu
            if (final and any(n in compact(host_of(final)) for n in names)
                    and TOURISM_HOST.search(host_of(final))):
                site, how = final, "pattern " + h
                break
    row["site_source"] = how
    if not site:
        row["site"] = None
        row["walled"] = walled
        row["note"] = ("%s answers curl with 403 (bot wall): read its contact page in a browser" % walled
                       if walled else "no official tourism site found; look it up by hand")
        return row
    row["site"] = site
    row["org"] = org or host_of(site)
    row["why_them"] = ("official tourism site of %s; our map has %d trees there, %d with a photograph"
                       % (english, row["tree_count"], len(row["trees"])))
    if fetch:
        hits, note = scrape(site, names, blocked)
        row["emails"] = [a for _, a, _ in hits]
        row["email"] = hits[0][1] if hits and hits[0][0] >= 0 else None
        row["source_url"] = hits[0][2] if hits else site
        row["scores"] = {a: s for s, a, _ in hits}
        row["fetch"] = note
        official = "never says official" not in note
        row["confidence"] = ("wikidata" if how.startswith("wikidata") else
                             "wikivoyage" if how.startswith("wikivoyage") else
                             "pattern, says official" if official else "pattern, unverified: look first")
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=40)
    ap.add_argument("--city")
    ap.add_argument("--no-fetch", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    doc = load(OUT, None) or {"_note": "Official tourism sites and their inboxes per roster city, "
                                       "from scripts/tourism_sites.py. Private: never commit.",
                              "cities": {}}
    if args.list:
        for slug, r in doc["cities"].items():
            print("%-18s %-3s %-40s %s" % (slug, r.get("language", ""), (r.get("site") or "-")[:40], r.get("email") or "-"))
        return 0

    rows = roster_cities()
    if args.city:
        rows = [r for r in rows if r[0] == args.city] or [(args.city, "", 0)]
    else:
        rows = rows[:args.top]
    blocked = blocked_hosts()
    for slug, country, impressions in rows:
        row = lookup(slug, blocked, fetch=not args.no_fetch)
        row["impressions"] = impressions
        doc["cities"][slug] = row
        json.dump(doc, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("%-18s %4d impr  %-42s %s" % (slug, impressions, (row.get("site") or "no site")[:42],
                                            row.get("email") or ("" if row.get("site") else row["site_source"])))
        time.sleep(1)
    with_mail = sum(1 for r in doc["cities"].values() if r.get("email"))
    print("%d cities in %s, %d with an address" % (len(doc["cities"]), os.path.relpath(OUT, ROOT), with_mail))
    return 0


if __name__ == "__main__":
    sys.exit(main())
