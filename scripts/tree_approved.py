#!/usr/bin/env python3
"""Congratulate a reader the day a tree THEY added goes live on Ancient Trees.

Hidde, 2026-10-09: "I think once a tree is added to the database we should
email the user with the link and congratulate them, eventually we can add
gamification for this." The convention is Google Maps': a place you added that
it accepts arrives as a mail saying so, with the link (CONVENTIONS.md
2026-10-09, the word "Approved").

Narrow on purpose, because the 2026-10-02 rulings stand beside it: a PHOTOGRAPH
going live on a tree we already had still sends nothing (MAIL_WHEN_LIVE in
sightings_publish.py). This is only for a tree that did not exist here until a
reader sent it, which is the rarer and bigger thing. How it knows: the sighting
went into data/leads/_sightings.json as a NEW tree (that is where a sighting
matching nothing we map lands), and a published tree now carries a contributor
photograph with that same sighting_id.

Once per sighting, recorded in data/tree-approved-mailed.json (sighting ids and
dates only, never an address: this repository is public). Our own accounts
(scripts/ours.py) are never mailed. Signed "Ancient Trees", never as Hidde
(hard rule 4). Every mail goes through mailcheck and the do-not-contact list by
way of sightings_publish.send_mail.

    python3 scripts/tree_approved.py           # dry run: prints what it would send
    python3 scripts/tree_approved.py --send    # needs SUPABASE_SERVICE_KEY and OUTREACH_* secrets
"""
import datetime
import glob
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import people  # noqa: E402  account ids as codes in public files (2026-10-19)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import ours  # noqa: E402
from sightings_publish import (address_of, send_mail, SUPA,  # noqa: E402
                               BASE_URL, load, save)

LEADS = os.path.join(ROOT, "data", "leads", "_sightings.json")
MAILED = os.path.join(ROOT, "data", "tree-approved-mailed.json")


def lead_sightings():
    """Every sighting id that entered the leads file as a tree we did not have."""
    out = set()

    def walk(o):
        if isinstance(o, dict):
            sid = o.get("sighting_id")
            if sid:
                out.add(str(sid).lower())
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(load(LEADS, {}))
    return out


def approved_trees():
    """[(sighting_id, user_id, tree, city_name, city_slug)] for reader-added trees now live."""
    new_trees = lead_sightings()
    found = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        with open(path, encoding="utf-8") as fh:
            city = json.load(fh)
        slug = os.path.splitext(os.path.basename(path))[0]
        for t in city.get("trees") or []:
            for p in [t.get("photo") or {}] + [p for p in (t.get("photos") or []) if p]:
                sid = str(p.get("sighting_id") or "").lower()
                if p.get("source") == "contributor" and sid in new_trees:
                    found.append((sid, p.get("contributor_user_id"), t, city.get("city", slug), slug))
                    break
    return found


def live_urls():
    """{tree_id: page url} from the live feed, so the link is the site's own
    answer (slug rules live in site/src/lib/slug.ts and are not copied here)
    and a tree is only congratulated once its page is actually deployed."""
    try:
        req = urllib.request.Request(f"{BASE_URL}/api/trees.json",
                                     headers={"User-Agent": "AncientTreesBot/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            feed = json.loads(r.read())
        return {t["id"]: BASE_URL + t["url"] for t in feed.get("trees", []) if t.get("url")}
    except Exception as e:
        print(f"tree_approved: live feed unreadable ({e.__class__.__name__}), nothing sent")
        return {}


def display_name(user_id):
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not key or not user_id:
        return None
    req = urllib.request.Request(
        f"{SUPA}/rest/v1/profiles?select=display_name&user_id=eq.{user_id}",
        headers={"apikey": key, "Authorization": "Bearer " + key})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            rows = json.loads(r.read()) or []
        return (rows[0].get("display_name") or "").strip() or None if rows else None
    except Exception:
        return None


def full_note(sid):
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not key:
        return None
    req = urllib.request.Request(
        f"{SUPA}/rest/v1/sightings?select=note&id=eq.{sid}",
        headers={"apikey": key, "Authorization": "Bearer " + key})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            rows = json.loads(r.read()) or []
        return rows[0].get("note") if rows else None
    except Exception:
        return None


def what_they_gave(sid):
    """What the reader filled in when adding the tree: age, trunk size, a note."""
    # A note can carry what the fields do not: the Tangier fig's reader gave
    # the trunk as "2.2 to 2.8 m" in prose and left girth empty, and the mail
    # would have asked them for it (2026-10-21).
    sid = str(sid).lower()
    for l in (load(LEADS, {}).get("leads") or []):
        if str(l.get("sighting_id") or "").lower() == sid:
            # data/leads/_sightings.json keeps 500 characters; the measure was
            # in the third paragraph, so read the whole note when we can.
            note = (full_note(sid) or l.get("note") or "").strip()
            size = re.search(r"\d+(?:[.,]\d+)?\s*(?:cm|m|metres?|meters?|ft|feet)\b", note, re.I) \
                and re.search(r"girth|circumference|diameter|trunk|around", note, re.I)
            years = re.search(r"\d{2,4}\s*(?:years|yrs|jaar|ans|años|anni|jahre)", note, re.I)
            return {
                "age": bool(l.get("age") or years),
                "trunk": bool(l.get("girth_cm") or l.get("girth_hugs") or size),
                "story": len(note) >= 40,
            }
    return {"age": False, "trunk": False, "story": False}


AMBASSADORS = os.path.join(ROOT, "data", "ambassadors.json")


def seat_open(uid, slug):
    """True when this place has no ambassador and this reader was never asked
    for it, nor asked never to be mailed (ambassador.py's own skip rules)."""
    doc = load(AMBASSADORS, {})
    if any(e.get("place_slug") == slug for e in doc.get("ambassadors", [])):
        return False
    ref = people.ref(uid)
    for i in doc.get("invited", []):
        if people.ref(i.get("user_id")) == ref and i.get("place_slug") in (slug, "*"):
            return False
    return True


def note_invited(uid, slug, place, tree_name):
    """Record the P.S. as the invitation, so ambassador.py --invite-scan does
    not send a second mail for the same place."""
    doc = load(AMBASSADORS, {})
    doc.setdefault("invited", []).append({
        "user_id": people.ref(uid), "place_slug": slug, "place_name": place,
        "date": datetime.date.today().isoformat(), "trees": [tree_name],
        "note": "asked in a P.S. under the congratulation mail (tree_approved.py)"})
    save(AMBASSADORS, doc, indent=2)


def mail_for(name, tree, city_name, page, gave=None, seat=False):
    """THE ASK FOLLOWS WHAT THEY GAVE (Hidde, 2026-10-20, on the Freiburg beech,
    which arrived as a photograph and a pin and nothing else: "ask if they have
    more info on the tree (age, girth, story etc) ... make that standard unless
    they gave a full info thing"). A page built from a photograph alone is a
    page that asks its readers for everything; the person who stood there is
    the one most likely to know. So the one ask in this mail is for what is
    missing, by name, and only when nothing is missing does it ask for the next
    tree. One ask, never two (drafts/HIS_VOICE.md), and a reply to the mail,
    never a form. Nothing here reads as a task: it asks what they know."""
    gave = gave or {"age": False, "trunk": False, "story": False}
    missing = [w for k, w in (("age", "how old it might be"), ("trunk", "how big around the trunk is"),
                              ("story", "a story about it")) if not gave.get(k)]
    if missing:
        wants = ", ".join(missing[:-1]) + (" or " if len(missing) > 1 else "") + missing[-1]
        ask = (f"Do you know more about it, {wants}? Just reply to this mail and it goes on the page.")
    else:
        ask = ("Is there another tree near you that belongs on the map? You can add it in the app "
               "the same way.")
    subject = "Your tree is on Ancient Trees"
    body = (
        f"Hi {name or 'there'},\n\n"
        f"Congratulations: {tree['name']} in {city_name}, the tree you added, has been "
        f"approved and is now on Ancient Trees for everybody to find:\n"
        f"{page}\n\n"
        f"You stood in front of it and sent it to us, and now other people can go and see it too.\n\n"
        f"{ask}\n\n"
        f"Ancient Trees\n{BASE_URL}\n"
    )
    # THE AMBASSADOR ASK RIDES ALONG, SMALL (Hidde, 2026-10-21: "is het niet
    # subtieler om je mail te schrijven en eronder minder groot also: city is
    # still looking for an ambassador - let us know if your interested"). The
    # Freiburg reader got the congratulation and a separate invitation on the
    # same day; one mail with a P.S. replaces the second.
    if seat:
        body += (f"\nP.S. {city_name} is still looking for an ambassador, somebody who adds "
                 f"photos and keeps an eye on the list. Let us know if you're interested.\n")
    return subject, body


def main(argv):
    really = "--send" in argv
    mailed = load(MAILED, {"mailed": {}})
    done = mailed.setdefault("mailed", {})
    sent = 0
    urls = None
    for sid, uid, tree, city_name, city_slug in approved_trees():
        if sid in done:
            continue
        if not uid or ours.is_ours(uid):
            continue
        if urls is None:
            urls = live_urls()
        page = urls.get(tree["id"])
        if not page:
            print(f"  {tree['id']}: not in the live feed yet, waits for the deploy")
            continue
        addr = address_of(people.uid(uid))
        if not addr:
            print(f"  {tree['id']}: no address for the account (no service key, or the account is gone)")
            continue
        seat = seat_open(uid, city_slug)
        subject, body = mail_for(display_name(people.uid(uid)), tree, city_name, page,
                                 what_they_gave(sid), seat=seat)
        if send_mail(addr, subject, body, really, sid):
            done[sid] = {"tree_id": tree["id"], "date": datetime.date.today().isoformat()}
            if seat:
                note_invited(uid, city_slug, city_name, tree["name"])
            sent += 1
    if really:
        save(MAILED, mailed)
    print(f"tree_approved: {sent} congratulation(s) sent")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
