#!/usr/bin/env python3
"""One outreach database: every address we know, its group and where it stands.

Hidde, 2026-10-19: "maak een outreach strategie en start met het aanleggen van
een database van emailadressen, dit gaat te ad hoc". Until then contacts lived
in 27 files (outreach-contacts-*.json, press desks, source contacts, the sent
log, replies, ambassadors), and every batch was assembled by hand from them.
This script folds them into data/outreach-db.json, keyed by address, and the
strategy (OUTREACH_STRATEGY.md) draws every batch from it.

The database is rebuilt from those files on every --build, so it never drifts
from the sent log. Fields a person sets by hand (notes, linked, segment, hold)
survive a rebuild. It holds people's and organisations' addresses, so it is
gitignored (data/outreach-*.json) and synced by private_store.py. Never commit it.

    python3 scripts/contacts_db.py --build
    python3 scripts/contacts_db.py --status
    python3 scripts/contacts_db.py --ready source --limit 15
    python3 scripts/contacts_db.py --set someone@example.org linked=yes notes="link on /about"

Status, in order of precedence: do_not_contact, ambassador (never asked for
links, Hidde 2026-10-16), declined, replied, linked, mailed, org_mailed (another
address of the same organisation was mailed), ready (an address and never
mailed), no_address.
"""
import argparse
import glob
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DB = os.path.join(DATA, "outreach-db.json")
FREEMAIL = {"gmail.com", "hotmail.com", "yahoo.com", "outlook.com", "libero.it", "seznam.cz",
            "gmx.de", "web.de", "proton.me", "icloud.com", "tiscali.it", "freenet.de", "hetnet.nl"}
MANUAL = ("notes", "linked", "linked_url", "segment", "hold")

# The groups of the strategy, one ask each (OUTREACH_STRATEGY.md).
SEGMENTS = ("source", "press", "tourism", "garden", "society", "guide", "council", "reader", "other")
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", re.I)
JUNK = re.compile(r"example\.|beispiel|domein\.nl|przyklad|xxxxx|legalmail|^pec\.|@pec\.|"
                  r"abbonament|publicid|pubblicit|contabilid|rrhh|assinatur|suscrip|"
                  r"satis@|accionista|booking@|biglietteria|group\.bookings|podcast-compl", re.I)
NEWS = re.compile(r"zeitung|krant|dagblad|courant|news|nieuws|gazette|times|post|journal|"
                  r"herald|press|diario|giornale|corriere|quotidiano|tribune|advertiser|"
                  r"advocate|omroep|rtv|radio|tv|actualidad|report|magazine|nazione|"
                  r"ominho|primabergamo|staradvertiser|infobae|elespanol|telemadrid|beteve|rtbf|voria", re.I)
# Official tourism sites (Hidde, 2026-10-20: a new group; a visit-the-city site
# links to free local resources, which a register or a ministry never does).
TOURISM = re.compile(r"\bvisit[a-z-]*\.|tourism|turism|tourisme|toerisme|\bvvv\b|turisme|"
                     r"office-de-tourisme|tourist|fremdenverkehr|visitor", re.I)
GUIDE = re.compile(r"welcome|bonita|untapped|bonjour|guide|getlisbon", re.I)
# Registers, ministries and regional governments are council, not source
# (2026-10-20: zero of 29 source mails to them answered, and none would link;
# the source ask is for sites a person runs).
COUNCIL = re.compile(r"\.gov|\.gob\.|\.gouv\.|gemeente|comune|ayuntamiento|ajuntament|stadt-|stadt\.|"
                     r"municip|council|\.gv\.|overheid|ville-|city\.|regione|junta|jcyl\.es|navarra\.es|"
                     r"\.ge\.ch|\.vd\.ch|\.zh\.ch|\.bs\.ch|kanton|canton|landkreis|bezirk|regierung|"
                     r"ministerio|ministero|ministry|minist[eè]re|bund\.de|\.land\.|landesamt|"
                     r"generalitat|provincia|diputaci|medioambiente|naturschutz|lubw|forst", re.I)


def load(path, default):
    try:
        return json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        return default


def norm(a):
    a = (a or "").strip().lower().replace("mailto:", "")
    return a if EMAIL.match(a) and not JUNK.search(a) else ""


def guess_segment(c):
    t = (c.get("type") or "").lower()
    blob = " ".join(str(c.get(k) or "") for k in ("org", "email", "source_url", "outlet"))
    if "press" in t or "(press" in blob or t in ("newspaper", "media", "broadcaster"):
        return "press"
    if t in ("garden", "arboretum", "park", "cemetery", "estate", "university"):
        return "garden"
    if t in ("ngo", "society", "blog", "person", "association", "friends"):
        return "society"
    if t in ("municipality", "register", "government"):
        return "council"
    if NEWS.search(blob):
        return "press"
    if COUNCIL.search(blob):
        return "council"
    if TOURISM.search(blob):
        return "tourism"
    if GUIDE.search(blob):
        return "guide"
    if c.get("_from") == "source":
        return "source"
    return "other"


def lang_of(c):
    l = (c.get("language") or "").lower()[:2]
    if l:
        return {"en": "en", "ge": "de"}.get(l, l)
    tld = (c.get("email") or "").rsplit(".", 1)[-1]
    return {"nl": "nl", "be": "nl", "de": "de", "at": "de", "ch": "de", "it": "it", "es": "es",
            "pt": "pt", "fr": "fr", "jp": "ja"}.get(tld, "en")


def gather():
    """Every contact record from every file, tagged with where it came from."""
    out = []
    for f in sorted(glob.glob(os.path.join(DATA, "outreach-contacts*.json")) +
                    [os.path.join(DATA, "research", "outreach-contacts.json")]):
        d = load(f, [])
        rows = d.get("contacts", []) if isinstance(d, dict) else d
        for c in rows:
            if isinstance(c, dict):
                out.append(dict(c, _from=os.path.basename(f)))
    for slug, city in load(os.path.join(DATA, "outreach-press-desks.json"), {}).get("cities", {}).items():
        for p in city.get("papers", []):
            for e in p.get("emails", [])[:2]:
                out.append({"org": p["name"], "email": e, "type": "press", "city": slug,
                            "country": city.get("country"), "language": p.get("language", ""),
                            "source_url": p.get("site"), "_from": "press_desks"})
    for host, v in load(os.path.join(DATA, "outreach-source-contacts.json"), {}).get("domains", {}).items():
        for e in v.get("emails", [])[:2]:
            trees = v.get("trees", [])
            out.append({"org": host, "email": e, "source_url": "https://" + host + "/",
                        "city": trees[0]["city"] if trees else None,
                        "trees": [t["city"] + "/" + t["id"] for t in trees],
                        "why_them": f"{len(trees)} of our tree pages cite {host}", "_from": "source"})
    return out


def build():
    old = load(DB, {}).get("contacts", {})
    sent = load(os.path.join(DATA, "outreach-sent.json"), {})
    replies = load(os.path.join(DATA, "outreach-replies.json"), {}).get("replies", [])
    dnc = {a.lower().strip() for a in sent.get("do_not_contact", [])}
    amb_names = {(a.get("named") or a.get("display_name") or "").lower()
                 for a in load(os.path.join(DATA, "ambassadors.json"), {}).get("ambassadors", [])} - {""}

    db = {}
    for c in gather():
        e = norm(c.get("email"))
        if not e:
            continue
        r = db.setdefault(e, {"email": e, "found_in": []})
        for k in ("org", "name", "role", "type", "country", "city", "language", "source_url",
                  "why_them", "our_page", "ask", "trees"):
            if c.get(k) and not r.get(k):
                r[k] = c[k]
        if c["_from"] not in r["found_in"]:
            r["found_in"].append(c["_from"])
        r.setdefault("_seg", guess_segment(c))

    for m in sent.get("sent", []):
        e = norm(m.get("to"))
        if not e:
            continue
        r = db.setdefault(e, {"email": e, "found_in": ["outreach-sent"], "org": m.get("outlet")})
        r.setdefault("_seg", guess_segment({"org": m.get("outlet"), "email": e}))
        r.setdefault("mails", []).append({"date": m.get("date"), "batch": m.get("batch"),
                                          "subject": m.get("subject")})
    for x in replies:
        e = norm(x.get("to_address"))
        if e in db:
            db[e].setdefault("replies", []).append({"date": x.get("date"), "kind": x.get("kind"),
                                                    "gave": x.get("gave")})

    for e, r in db.items():
        prev = old.get(e, {})
        for k in MANUAL:
            # A segment survives a rebuild only when a person set it (--set
            # marks segment_manual); otherwise the regexes decide afresh, so a
            # rule change (2026-10-20: registers are council, tourism is a
            # group) reaches every address instead of only new ones.
            if k == "segment" and not prev.get("segment_manual"):
                continue
            if k in prev:
                r[k] = prev[k]
        if prev.get("segment_manual"):
            r["segment_manual"] = True
        r["segment"] = r.get("segment") or r.pop("_seg", "other")
        r.pop("_seg", None)
        r["language"] = lang_of(r)
        mails = sorted(r.get("mails", []), key=lambda m: m.get("date") or "")
        r["times_mailed"] = len(mails)
        r["last_mailed"] = mails[-1]["date"] if mails else None
        kinds = [x.get("kind") for x in r.get("replies", [])]
        domain = e.split("@")[-1]
        named = " ".join(str(r.get(k) or "") for k in ("name", "org")).lower()
        if e in dnc or "@" + domain in dnc or domain in dnc:
            st = "do_not_contact"
        elif any(n and n in named for n in amb_names):
            st = "ambassador"
        elif "no" in kinds:
            st = "declined"
        elif any(k and k != "auto" for k in kinds):
            st = "replied"
        elif r.get("linked") == "yes":
            st = "linked"
        elif mails:
            st = "mailed"
        else:
            st = "ready"
        r["status"] = st

    # An organisation is one contact, whatever address we found for it: a second
    # address of a domain or site we already wrote to is not a fresh one
    # (botanic@uv.es after 24cicbotanic@uv.es, jirka@ after honza@turistika.cz, 2026-10-20).
    touched = [r for r in db.values() if r["status"] not in ("ready", "no_address")]
    domains = {r["email"].split("@")[-1] for r in touched} - FREEMAIL
    sites = {(r.get("org") or "").lower() for r in touched} | {(r.get("source_url") or "").lower() for r in touched}
    sites -= {""}
    for r in db.values():
        if r["status"] != "ready":
            continue
        dom = r["email"].split("@")[-1]
        if dom in domains or (r.get("org") or "").lower() in sites or (r.get("source_url") or "").lower() in sites:
            r["status"] = "org_mailed"

    doc = {"_note": "One row per address. Built by scripts/contacts_db.py from every outreach file; "
                    "manual fields (notes, linked, linked_url, segment, hold) survive rebuilds. Private: never commit.",
           "built": time.strftime("%Y-%m-%d %H:%M"), "contacts": dict(sorted(db.items()))}
    json.dump(doc, open(DB, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return doc


def status(doc):
    rows = doc["contacts"].values()
    states = ("ready", "mailed", "org_mailed", "replied", "linked", "declined", "ambassador", "do_not_contact")
    print(f"{len(doc['contacts'])} addresses, built {doc['built']}\n")
    print(f"{'segment':10}" + "".join(f"{s[:10]:>12}" for s in states))
    for seg in SEGMENTS:
        cnt = [sum(1 for r in rows if r["segment"] == seg and r["status"] == s) for s in states]
        if sum(cnt):
            print(f"{seg:10}" + "".join(f"{n:>12}" for n in cnt))
    tot = [sum(1 for r in rows if r["status"] == s) for s in states]
    print(f"{'total':10}" + "".join(f"{n:>12}" for n in tot))


def ready(doc, seg, limit):
    rows = [r for r in doc["contacts"].values()
            if r["status"] == "ready" and not r.get("hold") and (seg == "all" or r["segment"] == seg)]
    rows.sort(key=lambda r: (-len(r.get("trees") or []), r.get("country") or "", r["email"]))
    for r in rows[:limit]:
        print(f"{r['segment']:8} {r['language']:3} {len(r.get('trees') or []):3} trees  "
              f"{r['email']:42} {(r.get('org') or '')[:40]:40} {r.get('city') or ''}")
    print(f"\n{len(rows)} ready in {seg}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--ready", metavar="SEGMENT")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--set", nargs="+", metavar="EMAIL field=value")
    a = ap.parse_args()
    if a.set:
        doc = load(DB, None) or build()
        e = norm(a.set[0])
        if e not in doc["contacts"]:
            print("unknown address"); return 1
        for kv in a.set[1:]:
            k, _, v = kv.partition("=")
            if k not in MANUAL:
                print(f"{k}: only {', '.join(MANUAL)} are set by hand"); return 1
            doc["contacts"][e][k] = v
            if k == "segment":
                doc["contacts"][e]["segment_manual"] = True
        json.dump(doc, open(DB, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        return 0
    doc = build() if (a.build or not os.path.exists(DB)) else load(DB, {})
    if a.status or a.build:
        status(doc)
    if a.ready:
        ready(doc, a.ready, a.limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
