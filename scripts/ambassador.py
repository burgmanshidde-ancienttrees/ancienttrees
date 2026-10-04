#!/usr/bin/env python3
"""Who looks after a place: grant, name and sync the ambassadors.

Hidde, 2026-10-02: "email each person that adds trees to become the cities
ambassador ... maybe we can even give them special tag if they want - share
some responsibility and amplify them." The convention behind the tag is
komoot's Pioneer (CONVENTIONS.md 2026-10-02): per place, a badge beside the
name, earned by what the person already did. The rule for who is asked lives in
CLAUDE.md ("Ambassadors"); this script only records the answer.

    python3 scripts/ambassador.py --list
    python3 scripts/ambassador.py --grant <user_id> <place_slug>
    python3 scripts/ambassador.py --public <user_id> <place_slug> yes|no
    python3 scripts/ambassador.py --revoke <user_id> <place_slug>
    python3 scripts/ambassador.py --sync
    python3 scripts/ambassador.py --grant-named "<Name>" <place_slug>
    python3 scripts/ambassador.py --invite-scan [--send]
    python3 scripts/ambassador.py --requests [--send]

--invite-scan is the standard first contact (Hidde, 2026-10-02: "lets make it
a standard thing whenever someone adds something to a city we dont have a
ambassador for we email this - and once they respond with more info we actually
give them the badge"). It finds every reader whose photograph is live on a tree
in a place with no ambassador, who has not been invited, and sends them the
invitation once, from the Ancient Trees address the other contributor mails use
(never as Hidde: hard rule 4). The badge is NOT granted here: it follows their
answer, by hand, with --grant. Without --send it prints the mails it would send.
The invitations live in data/ambassadors.json under "invited".

--requests answers the OPEN SEAT (Hidde, 2026-10-04: every city with nobody
named shows "Tokyo is looking for an ambassador" with a button). The button
writes a submissions row of kind 'ambassador'; this sends each new one the
editor mail once (how they see the list, what to take off or add, photographs),
the same second mail Giulia Torta got, and records it under "requested" so it
never repeats. The badge still follows their answer, by hand, with --grant.

--grant-named is for somebody who gave us trees by MAIL and has no app account
(Hidde, 2026-10-02, on Hans Erik Lund and Paulo Araujo: "dont email paulo or
hans ive had much contact with them just make them ambassador"). It writes a
json-only entry, named and public on his word, with no user_id; the badge
reaches them in the app the day they make an account and --grant links it. A
sync keeps these entries, because the table knows nothing about them.

--grant writes the row to Supabase (the person said yes to Hidde's mail) with
`public` false: consent to be NAMED on the website is a second, separate yes,
and --public records it. --sync rewrites data/ambassadors.json from the table,
with the display name only where public is true, and drops anybody whose
account is gone (the row cascades, so the table is already right; the file has
to follow). The knock runs --sync beside photo_takedown.py, for the same
promise. Everything needs SUPABASE_SERVICE_KEY; without it this prints what it
would do and changes nothing.
"""
import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import smtplib
from email.message import EmailMessage
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPA = "https://caimvxiyrtifilimlkqw.supabase.co"
KEY = os.environ.get("SUPABASE_SERVICE_KEY")
FILE = os.path.join(ROOT, "data", "ambassadors.json")


def _req(path, method="GET", body=None, prefer=None):
    headers = {"apikey": KEY, "Authorization": "Bearer " + KEY,
               "Content-Type": "application/json"}
    if prefer:
        headers["Prefer"] = prefer
    req = urllib.request.Request(SUPA + path, method=method, headers=headers,
                                 data=json.dumps(body).encode() if body is not None else None)
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    return json.loads(raw) if raw else None


def place_name(slug):
    """The place's name as its own city file spells it, English (CLAUDE.md,
    place names). A slug with no file is refused rather than guessed."""
    path = os.path.join(ROOT, "data", "cities", f"{slug}.json")
    if not os.path.exists(path):
        sys.exit(f"ambassador: no data/cities/{slug}.json; the place has to exist before it has an ambassador")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh).get("city") or slug


def rows():
    return _req("/rest/v1/ambassadors?select=user_id,place_slug,place_name,public,since&order=since.asc") or []


def grant(user_id, slug):
    name = place_name(slug)
    row = {"user_id": user_id, "place_slug": slug, "place_name": name,
           "public": False, "since": datetime.date.today().isoformat()}
    if not KEY:
        print("ambassador (dry, no SUPABASE_SERVICE_KEY): would grant", row)
        return
    _req("/rest/v1/ambassadors?on_conflict=user_id,place_slug", "POST", [row],
         prefer="resolution=merge-duplicates,return=minimal")
    print(f"ambassador: {user_id[:8]} is the ambassador of {name} ({slug}), not yet named publicly")
    sync()


def set_public(user_id, slug, yes):
    if not KEY:
        print(f"ambassador (dry): would set public={yes} for {user_id[:8]} / {slug}")
        return
    q = urllib.parse.urlencode({"user_id": f"eq.{user_id}", "place_slug": f"eq.{slug}"})
    _req(f"/rest/v1/ambassadors?{q}", "PATCH", {"public": yes}, prefer="return=minimal")
    print(f"ambassador: {user_id[:8]} / {slug}: {'named on the page' if yes else 'badge only, not named'}")
    sync()


def revoke(user_id, slug):
    if not KEY:
        print(f"ambassador (dry): would revoke {user_id[:8]} / {slug}")
        return
    q = urllib.parse.urlencode({"user_id": f"eq.{user_id}", "place_slug": f"eq.{slug}"})
    _req(f"/rest/v1/ambassadors?{q}", "DELETE", prefer="return=minimal")
    print(f"ambassador: {user_id[:8]} / {slug} revoked")
    sync()


def grant_named(name, slug):
    """A named, public ambassador with no account: Hidde's own word stands in
    for the consent flag, because he has the correspondence."""
    pname = place_name(slug)
    with open(FILE, encoding="utf-8") as fh:
        doc = json.load(fh)
    entries = [e for e in doc["ambassadors"] if not (e.get("user_id") is None and e["place_slug"] == slug
                                                    and e.get("display_name") == name)]
    entries.append({"user_id": None, "place_slug": slug, "place_name": pname, "public": True,
                    "since": datetime.date.today().isoformat(), "display_name": name,
                    "source": "mail, granted by Hidde"})
    doc["ambassadors"] = entries
    with open(FILE, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"ambassador: {name} is named on /{slug} as the ambassador of {pname} (no account yet)")


def sync():
    """data/ambassadors.json from the table. The file carries a display name
    ONLY for a row whose person consented (public), and that name is read
    from profiles at sync time rather than stored twice."""
    if not KEY:
        print("ambassador --sync: no SUPABASE_SERVICE_KEY, file left as it is")
        return 0
    try:
        table = rows()
    except urllib.error.HTTPError as e:
        if e.code in (404, 400):
            print("ambassador --sync: the table does not exist yet (paste supabase/PENDING.sql); file left as it is")
            return 0
        raise
    names = {}
    public_ids = sorted({r["user_id"] for r in table if r.get("public")})
    if public_ids:
        q = ",".join(public_ids)
        for p in _req(f"/rest/v1/profiles?select=user_id,display_name&user_id=in.({q})") or []:
            names[p["user_id"]] = p.get("display_name")
    out = []
    for r in table:
        entry = {"user_id": r["user_id"], "place_slug": r["place_slug"],
                 "place_name": r["place_name"], "public": bool(r.get("public")),
                 "since": r.get("since")}
        if entry["public"] and names.get(r["user_id"]):
            entry["display_name"] = names[r["user_id"]]
        elif entry["public"]:
            # Consented, but never set a name: nothing to print, and the page
            # says nothing rather than inventing one.
            entry["public"] = False
            entry["note"] = "consented but has no display name yet"
        out.append(entry)
    with open(FILE, encoding="utf-8") as fh:
        doc = json.load(fh)
    # Named people without an account live only in this file; keep them.
    kept = [e for e in doc.get("ambassadors", []) if e.get("user_id") is None]
    if out + kept == doc.get("ambassadors", []):
        # Nothing moved, so nothing is written: the knock commits any change
        # to this file as "a reader deleted their account", and on 2026-10-02
        # six such commits were this timestamp alone, which read in the
        # digest as six people leaving.
        print(f"ambassador --sync: {len(out)} row(s), unchanged")
        return 0
    doc["ambassadors"] = out + kept
    doc["synced"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    with open(FILE, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"ambassador --sync: {len(out)} row(s), {sum(1 for e in out if e['public'])} named publicly")
    return 0


INVITE_SUBJECT = "Your {place} trees"
INVITE_BODY = (
    "Hi,\n\n"
    "Thanks so much for adding {what} in {place}. {itis} live, for everybody to see:\n"
    "{links}\n\n"
    "We would love to make you our ambassador for {place}: somebody who adds photos, checks the "
    "facts and helps sharpen the list. What do you think of our {place} list, is it missing any, "
    "are some wrong? Let us know if you are up for it.\n{listlink}\n\n"
    "Thanks,\nAncient Trees\n"
)
BASE_URL = "https://ancienttrees.app"


def _contributions():
    """{(user_id, place_slug): [tree names]} for every reader photograph live
    on a tree page, lead or extra. Today a photograph is how a reader adds
    something to a city; a tree they sent that went live carries no account id
    in the city file, so it is not seen here yet."""
    out = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "cities", "*.json"))):
        slug = os.path.basename(path)[:-5]
        with open(path, encoding="utf-8") as fh:
            city = json.load(fh)
        for t in city.get("trees") or []:
            shots = [t.get("photo") or {}] + [p for p in (t.get("photos") or []) if p]
            for p in shots:
                if p.get("source") == "contributor" and p.get("contributor_user_id") \
                        and p.get("status") == "approved":
                    out.setdefault((p["contributor_user_id"], slug), [])
                    if (t["name"], t["id"]) not in out[(p["contributor_user_id"], slug)]:
                        out[(p["contributor_user_id"], slug)].append((t["name"], t["id"]))
    return out


_FEED_URLS = None


def _tree_urls():
    """id -> page path, from the site's own feed rather than slugged here: the
    site drops a leading "The" and the two Paris links guessed from the name
    came back 404 on 2026-10-02."""
    global _FEED_URLS
    if _FEED_URLS is None:
        _FEED_URLS = {}
        try:
            with urllib.request.urlopen(BASE_URL + "/api/trees.json", timeout=30) as r:
                d = json.load(r)
            for t in (d.get("trees") if isinstance(d, dict) else d) or []:
                if t.get("id") and t.get("url"):
                    _FEED_URLS[t["id"]] = t["url"]
        except Exception:
            pass
    return _FEED_URLS


def _address(user_id):
    try:
        u = _req(f"/auth/v1/admin/users/{user_id}")
    except Exception:
        return None
    return (u or {}).get("email")


def _what(names):
    low = [n[0].lower() + n[1:] if n[:4] == "The " else n for n in names]
    low = [n[4:] if n.startswith("the ") else n for n in low]
    low = ["the " + n for n in low]
    if len(low) == 1:
        return low[0], "It is"
    if len(low) == 2:
        return f"{low[0]} and {low[1]}", "They are"
    return f"{', '.join(low[:-1])} and {low[-1]}", "They are"


def invite_scan(send):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import ours
    try:
        from contributor_reply import mailcheck_ok
    except Exception:
        mailcheck_ok = None
    with open(FILE, encoding="utf-8") as fh:
        doc = json.load(fh)
    covered = {e["place_slug"] for e in doc.get("ambassadors", [])}
    badged = {e.get("user_id") for e in doc.get("ambassadors", []) if e.get("user_id")}
    invited = doc.setdefault("invited", [])
    already = {(i["user_id"][:8], i["place_slug"]) for i in invited}
    # A person Hidde has said never to mail: an entry with place "*", matched
    # on the first eight characters of the id (Leon, 2026-10-02).
    never = {i["user_id"][:8] for i in invited if i.get("place_slug") == "*"}
    sent_log_path = os.path.join(ROOT, "data", "outreach-sent.json")
    n = 0
    for (uid, slug), pairs in sorted(_contributions().items()):
        names = [n for n, _ in pairs]
        if ours.is_ours(uid) or slug in covered or uid in badged or (uid[:8], slug) in already or uid[:8] in never:
            continue
        place = place_name(slug)
        what, itis = _what(names)
        urls = _tree_urls()
        if not all(tid in urls for _, tid in pairs):
            print(f"invite {uid[:8]} / {slug}: the feed has no page for one of the trees yet, next knock")
            continue
        links = "\n".join(BASE_URL + urls[tid] for _, tid in pairs)
        body = INVITE_BODY.format(what=what, place=place, itis=itis, links=links,
                                  listlink=f"{BASE_URL}/{slug}")
        subject = INVITE_SUBJECT.format(place=place)
        if mailcheck_ok:
            ok, why = mailcheck_ok(body, app_user=True)
            if not ok:
                print(f"invite {uid[:8]} / {slug}: held by mailcheck\n{why}")
                continue
        addr = _address(uid) if KEY else None
        creds = {k: os.environ.get(f"OUTREACH_{k}") for k in ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS", "FROM")}
        if not send or not addr or not all(creds.values()):
            why = "dry run" if not send else ("no address" if not addr else "no mail credentials")
            print(f"invite {uid[:8]} / {slug} ({why}):\n  {subject}\n" + "\n".join("  " + l for l in body.splitlines()))
            continue
        if "burgmans.hidde" in creds["FROM"].lower():
            print("REFUSED: an invitation would go out under a personal address")
            continue
        msg = EmailMessage()
        msg["From"], msg["To"], msg["Subject"] = creds["FROM"], addr, subject
        msg.set_content(body)
        try:
            with smtplib.SMTP(creds["SMTP_HOST"], int(creds["SMTP_PORT"]), timeout=60) as server:
                server.starttls()
                server.login(creds["SMTP_USER"], creds["SMTP_PASS"])
                server.send_message(msg)
        except Exception as e:
            print(f"invite {uid[:8]} / {slug}: transport failed ({e.__class__.__name__})")
            continue
        today = datetime.date.today().isoformat()
        invited.append({"user_id": uid, "place_slug": slug, "place_name": place,
                        "date": today, "trees": names})
        try:
            with open(sent_log_path, encoding="utf-8") as fh:
                log = json.load(fh)
            log.setdefault("sent", []).append({"date": today, "to": addr, "outlet": "ambassador invitation",
                                               "subject": subject, "batch": "ambassador-invite"})
            with open(sent_log_path, "w", encoding="utf-8") as fh:
                json.dump(log, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
        except Exception:
            pass
        n += 1
        print(f"invite {uid[:8]} / {slug}: sent ({', '.join(names)[:60]})")
    with open(FILE, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"invite-scan: {n} invitation(s) sent")
    return 0


REQUEST_SUBJECT = "Looking after {place}"
REQUEST_BODY = (
    "Hi,\n\n"
    "Thanks for offering to look after our {place} list. Here it is as it stands:\n{listlink}\n\n"
    "Three questions, answer whichever you like: how do you see the list, which trees would you "
    "take off or add, and do you have photographs of any of them? Those would go on the pages.\n\n"
    "Thanks,\nAncient Trees\n"
)


def _slug_for(city):
    """The page slug for the English city name the request row carries."""
    want = (city or "").strip().lower()
    for path in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
        with open(path, encoding="utf-8") as fh:
            if (json.load(fh).get("city") or "").strip().lower() == want:
                return os.path.basename(path)[:-5]
    return None


def requests_scan(send):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import ours
    try:
        from contributor_reply import mailcheck_ok
    except Exception:
        mailcheck_ok = None
    if not KEY:
        print("ambassador --requests: no SUPABASE_SERVICE_KEY, nothing read")
        return 0
    with open(FILE, encoding="utf-8") as fh:
        doc = json.load(fh)
    requested = doc.setdefault("requested", [])
    seen_rows = {r.get("row") for r in requested}
    asked = {(r["user_id"], r["place_slug"]) for r in requested if r.get("user_id")}
    badged = {(e.get("user_id"), e["place_slug"]) for e in doc.get("ambassadors", [])}
    rows_ = _req("/rest/v1/submissions?select=id,user_id,city,created_at"
                 "&kind=eq.ambassador&order=created_at.asc") or []
    n = 0
    for row in rows_:
        uid, rid = row.get("user_id"), row.get("id")
        if rid in seen_rows or not uid or ours.is_ours(uid):
            continue
        slug = _slug_for(row.get("city"))
        if not slug:
            print(f"request {rid}: no published place called {row.get('city')!r}")
            continue
        if (uid, slug) in asked or (uid, slug) in badged:
            requested.append({"row": rid, "user_id": uid, "place_slug": slug, "date": None, "note": "repeat"})
            continue
        place = place_name(slug)
        subject = REQUEST_SUBJECT.format(place=place)
        body = REQUEST_BODY.format(place=place, listlink=f"{BASE_URL}/{slug}")
        if mailcheck_ok:
            ok, why = mailcheck_ok(body, app_user=True)
            if not ok:
                print(f"request {rid} / {slug}: held by mailcheck\n{why}")
                continue
        addr = _address(uid)
        creds = {k: os.environ.get(f"OUTREACH_{k}") for k in ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS", "FROM")}
        if not send or not addr or not all(creds.values()):
            why = "dry run" if not send else ("no address" if not addr else "no mail credentials")
            print(f"request {rid} {uid[:8]} / {slug} ({why}):\n  {subject}\n" + "\n".join("  " + l for l in body.splitlines()))
            continue
        if "burgmans.hidde" in creds["FROM"].lower():
            print("REFUSED: a reply would go out under a personal address")
            continue
        msg = EmailMessage()
        msg["From"], msg["To"], msg["Subject"] = creds["FROM"], addr, subject
        msg.set_content(body)
        try:
            with smtplib.SMTP(creds["SMTP_HOST"], int(creds["SMTP_PORT"]), timeout=60) as server:
                server.starttls()
                server.login(creds["SMTP_USER"], creds["SMTP_PASS"])
                server.send_message(msg)
        except Exception as e:
            print(f"request {rid} / {slug}: transport failed ({e.__class__.__name__})")
            continue
        requested.append({"row": rid, "user_id": uid, "place_slug": slug, "place_name": place,
                          "date": datetime.date.today().isoformat()})
        asked.add((uid, slug))
        n += 1
        print(f"request {rid} / {slug}: editor mail sent")
    with open(FILE, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"ambassador --requests: {n} mail(s) sent")
    return 0


def listing():
    with open(FILE, encoding="utf-8") as fh:
        doc = json.load(fh)
    if not doc["ambassadors"]:
        print("no ambassadors yet (file synced", doc.get("synced"), ")")
    for e in doc["ambassadors"]:
        who = (e.get("user_id") or "no account")[:10]
        print(f"{who:<10}  {e['place_name']:<24} since {e['since']}  "
              f"{'named: ' + e['display_name'] if e.get('display_name') else 'badge only'}")


def main(argv):
    if "--list" in argv or len(argv) == 1:
        return listing()
    if "--sync" in argv:
        return sync()
    if "--requests" in argv:
        return requests_scan("--send" in argv)
    if "--invite-scan" in argv:
        return invite_scan("--send" in argv)
    if "--grant-named" in argv:
        i = argv.index("--grant-named")
        return grant_named(argv[i + 1], argv[i + 2])
    if "--grant" in argv:
        i = argv.index("--grant")
        return grant(argv[i + 1], argv[i + 2])
    if "--public" in argv:
        i = argv.index("--public")
        return set_public(argv[i + 1], argv[i + 2], argv[i + 3].lower() in ("yes", "true", "1"))
    if "--revoke" in argv:
        i = argv.index("--revoke")
        return revoke(argv[i + 1], argv[i + 2])
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv) or 0)
