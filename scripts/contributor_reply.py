#!/usr/bin/env python3
"""Thank contributors and send them the run's answer. The transport half of
the contributor reply loop (spec: docs/superpowers/specs/
2026-08-21-contributor-reply-design.md; Hidde's ruling, 2026-08-21: input is
one of the core features and gets treated with care).

Two mail kinds, both from "Ancient Trees" via the outreach SMTP creds, with
standing approval given in session for exactly these two:

  THANK-YOU  templated, to any submission row we can answer and that has no
             thanked_at. Sent once per address however many rows a
             double-submit left, and it NAMES the tips it covers, with a link
             to the tree where the tree is one of ours.
  ANSWER     the run-composed reply_text, to answerable rows with no
             replied_at. mailcheck.py gates every one; a failing draft is
             held and printed, never sent.

Answerable means: the row carries a user_id (feedback is account-gated since
2026-08-21, the Google Maps convention, so the account is the reply channel;
the address is resolved from it at send time and never stored twice) or, for
older rows, a typed email.

DRY RUN by default; --send sends. Missing env prints and exits 0, so a CI
step can always call it. State lives in the submissions columns, so a lost
log line can never cause a double send. The do-not-contact list in
data/outreach-sent.json beats everything, and every send is appended there
so the outreach once-only guard knows these addresses too.

Never mailed: privacy-kind rows (a deletion request must not get marketing
warmth; they are printed for the session to handle) and vote-undone
bookkeeping rows.
"""
import datetime
import json
import os
import re
import smtplib
import subprocess
import sys
import tempfile
import urllib.request
from email.message import EmailMessage

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mailcheck import NO_APP_LINK, APP_STORE_URL  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPA = "https://caimvxiyrtifilimlkqw.supabase.co"
SENT_PATH = os.path.join(ROOT, "data", "outreach-sent.json")
DAILY_CAP = int(os.environ.get("OUTREACH_DAILY_CAP", "50"))


HEALTH_PATH = os.path.join(ROOT, "data", "mail-health.json")


def _note_transport(error, sent=True):
    """Record whether the mail actually went, so a dead transport is visible.

    Written 2026-09-01 after finding that the reply to submission #54 had been
    failing on every digest and every night run since 2026-08-30 with a Gmail
    535 BadCredentials, and nobody knew. The step is deliberately
    continue-on-error so a mail problem cannot kill the digest, which is right,
    and the cost of that is that the failure is silent. This file is what
    health.py reads, so the silence ends at the next rung-2 check.
    """
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        state = json.load(open(HEALTH_PATH))
    except Exception:
        state = {}
    if error:
        state["last_error"] = error
        state["last_error_at"] = now
        state["consecutive_failures"] = int(state.get("consecutive_failures", 0)) + 1
    else:
        if sent:
            state["last_sent_at"] = now
        state["last_ok_at"] = now
        state["consecutive_failures"] = 0
        state.pop("last_error", None)
    try:
        with open(HEALTH_PATH, "w") as fh:
            json.dump(state, fh, indent=2, sort_keys=True)
            fh.write("\n")
    except OSError:
        pass


SITE = "https://ancienttrees.app"
FEED = SITE + "/api/trees.json"
TREE_ID = re.compile(r"^([a-z]{2,6}_\d{2,4})\b", re.I)
COORDS = re.compile(r"(-?\d{1,3}\.\d+),\s*(-?\d{1,3}\.\d+)")
# A tree added through the app carries the sighting's own uuid in `tree`
# since 2026-09-03 (CollectSheet.swift's transmit()), so the mail can link to
# its unlisted page (SightingSync.url(for:)) rather than printing the raw
# coordinate below. Sightings are shared by default now, so the page is live
# by the time this mail sends.
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
_feed = {}


def tree_pages():
    """id -> url, read from the site's own feed rather than slugged here.

    The website already decides what a tree's URL is, and the slug rule behind
    it has a transliteration table, a leading-"the" strip and a frozen legacy
    twin. Porting that into Python would be the second implementation CLAUDE.md
    warns about (a decision travels as an ANSWER, never as a rule written
    twice), and the mail is the worst place to be the copy that drifts: a dead
    link in a thank-you is worse than no link at all.

    Fetched lazily, so a run with nothing to send never pays for it, and a feed
    we cannot read costs the link rather than the mail.
    """
    if "by_id" not in _feed:
        by_id, paths = {}, set()
        try:
            with urllib.request.urlopen(FEED, timeout=60) as r:
                for t in json.load(r).get("trees") or []:
                    if t.get("id") and t.get("url"):
                        by_id[t["id"]] = t["url"]
                        paths.add(t["url"])
        except Exception as e:
            print("contributor_reply: tree feed unreadable (%s); naming the "
                  "tip without a link" % str(e)[:60])
        _feed["by_id"], _feed["paths"] = by_id, paths
    return _feed["by_id"], _feed["paths"]


def tip_link(row):
    """The page of the tree this row is about, or "" when there is not one.

    Three routes in, because the rows arrive from three surfaces. The
    worth-it control names the tree by id and sends page "app" or a bare
    path; the contribute form sends the referrer, which is a full URL when
    the reader came from a tree page and something useless when they did
    not; a tree added through the app sends the sighting's own uuid, which
    has an unlisted page of its own the moment it is written (sightings are
    shared by default, CollectSheet.swift). A path is only used when the
    feed confirms it is a tree page, so a referrer of /contribute or
    google.com never becomes a link.
    """
    by_id, paths = tree_pages()
    raw = (row.get("tree") or "").strip()
    if UUID_RE.match(raw):
        return SITE + "/t?id=" + raw.lower()
    m = TREE_ID.match(raw)
    if m and m.group(1).lower() in by_id:
        return SITE + by_id[m.group(1).lower()]
    path = (row.get("page") or "").strip()
    for pre in ("https://ancienttrees.app", "http://ancienttrees.app"):
        if path.startswith(pre):
            path = path[len(pre):]
    if not path.startswith("/"):
        return ""
    path = path.split("?")[0].split("#")[0].rstrip("/")
    stripped = re.sub(r"^/[a-z]{2}(/)", r"\1", path)
    if path in paths or stripped in paths:
        return SITE + path
    return ""


def tip_name(row):
    """What to call the tree, as the reader would recognise it."""
    t = (row.get("tree") or "").strip()
    if UUID_RE.match(t):
        # A sighting id names nothing a reader would recognise; fall through
        # to the same "no name" handling a blank tree field gets.
        t = ""
    m = re.match(r"^[a-z]{2,6}_\d{2,4}\s*\((.+)\)$", t, re.I)
    if m:
        t = m.group(1).strip()
    if not t and row.get("kind") in ("tree", "city"):
        t = (row.get("why") or "").strip().splitlines()[0][:60] if row.get("why") else ""
    return t


def tip_lines(row):
    """Name and link one tip, as the lines it gets in the mail.

    Once there is a link, real or the sighting's own unlisted page, it
    replaces the raw coordinate rather than sitting beside it: a pair of
    numbers tells a reader nothing a tap does not tell them better. Only a
    tree with neither a name nor any page at all, which is now just the
    rows written before 2026-09-03, falls back to the coordinate the phone
    sent, which is honestly all we hold for those.
    """
    name, url = tip_name(row), tip_link(row)
    city = (row.get("city") or "").strip()
    if name:
        head = "%s, %s" % (name, city) if city and city.lower() not in name.lower() else name
    elif url:
        head = "The tree you added near %s" % city if city else "The tree you added"
    else:
        here = COORDS.search(row.get("location_hint") or "")
        head = "The tree you added near %s" % city if city else "The tree you added"
        if here:
            head += ", at %s, %s" % (here.group(1), here.group(2))
    return [head] + ([url] if url else [])


def thanks_body(rows_for_addr, addr=None):
    """The thank-you, saying which tree it is about.

    Hidde, 2026-09-02, on receiving his second "thank you, we received your
    tree tip" and being unable to tell which of his tips it answered: "can we
    add a link to the tree the person tipped in the mail". Somebody who sends
    us three trees in a week gets three identical letters otherwise, and the
    one thing they want to know, that we understood WHICH tree, is the one
    thing the template never said.

    It lists every unanswered tip from that address, because one mail already
    stamps all of them.
    """
    out = ["Thank you for your feedback. We are looking into it and we will "
           "come back to you with what it changed.", ""]
    tips = []
    for r in rows_for_addr:
        tips += tip_lines(r) + [""]
    if tips:
        out += ["What you sent us:", ""] + tips
    # A LINK TO OPEN IN THE APP, when one of the tips above is the sighting's
    # own unlisted page rather than a published tree (Hidde, 2026-09-03: the
    # mail should link to the tree instead of printing coordinates, and say
    # plainly that it can be adjusted). Opening it there, signed in, lands on
    # the same page the app already gives you for a tree of your own, fields
    # and all; opened anywhere else it is the read-only page, which still
    # proves we understood what was sent.
    if any(tip_link(r).startswith(SITE + "/t?id=") for r in rows_for_addr):
        out += ["Open a link above in the app and you land on the tree's own "
                "page: you can change the name, the species, the pin, or turn "
                "the link off, any time, from its menu.", ""]
    # WHERE THEIR OWN TREES ARE (Hidde, 2026-09-02: "deze link ook toevoegen in
    # de bedank voor het toevoegen van een boom mail zodat mensen hun eigen
    # boom kunnen zien en delen"). Only to somebody with an account, because
    # /account shows what that account holds and shows an empty page to
    # anybody else, and only where a tree was actually added: a correction is
    # not a tree of theirs.
    if (any(r.get("user_id") for r in rows_for_addr)
            and any(r.get("kind") in ("tree", "city") for r in rows_for_addr)):
        out += ["You can see the trees you added, with your own photographs, "
                "on your account:", "", SITE + "/account", ""]
    out += ["Please keep them coming: a tree you love, a mistake we have made, "
            "a photograph. Every one of them makes the map better, and a real "
            "person telling us about a real tree is the best thing this "
            "project receives.", ""]
    # THE APP IS LIVE, SO SAY SO (Hidde, 2026-09-03: "onze app staat live dus
    # vertel dat en we zijn beniewud wat ie er van vindt", then "stuur dat nu
    # altijd maar mee met de komende mailtjes"). Standing instruction on every
    # outbound mail, mailcheck.py's check_app_link enforces it, and the exact
    # two lines are HIS_VOICE.md's own. Somebody already using the app gets
    # the shorter form: telling them it exists would be telling them what they
    # are holding.
    if addr and addr.lower() in NO_APP_LINK:
        pass
    elif all((r.get("page") or "").startswith("app") for r in rows_for_addr):
        out += ["We would like to know what you think of the app:", "",
                APP_STORE_URL, ""]
    else:
        out += ["Our app is also live now. We would like to know what you "
                "think of it:", "", APP_STORE_URL, ""]
    out += ["Ancient Trees", SITE]
    return "\n".join(out) + "\n"


THANKS_SUBJECT = {
    "tree": "Thank you, we received your tree tip",
    "city": "Thank you, we received your tree tip",
    "correction": "Thank you, we received your correction",
    "feedback": "Thank you, we received your report",
}



def supa(path, key, method="GET", body=None):
    req = urllib.request.Request(SUPA + path, method=method, headers={
        "apikey": key, "Authorization": "Bearer " + key,
        "Content-Type": "application/json", "Prefer": "return=minimal"})
    data = json.dumps(body).encode() if body is not None else None
    with urllib.request.urlopen(req, data=data, timeout=30) as r:
        raw = r.read()
        return json.loads(raw) if raw else None


def mailcheck_ok(text):
    """Run mailcheck.py on the draft; nonzero exit means hold it."""
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write("draft\n---\n" + text)
        path = f.name
    try:
        out = subprocess.run([sys.executable,
                              os.path.join(ROOT, "scripts", "mailcheck.py"),
                              path], capture_output=True, text=True, timeout=60)
        return out.returncode == 0, out.stdout.strip()
    finally:
        os.unlink(path)


def main():
    really = "--send" in sys.argv
    only = None
    for i, a in enumerate(sys.argv):
        if a == "--only" and i + 1 < len(sys.argv):
            only = sys.argv[i + 1]
    if only not in (None, "thanks", "answers"):
        print("contributor_reply: --only takes 'thanks' or 'answers'")
        return 2
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not key:
        print("contributor_reply: SUPABASE_SERVICE_KEY absent, nothing to do")
        return 0
    creds = {k: os.environ.get("OUTREACH_" + k) for k in
             ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS", "FROM")}
    if really and not all(creds.values()):
        print("contributor_reply: SMTP env missing (%s); dry run only"
              % ", ".join(k for k, v in creds.items() if not v))
        really = False

    # THE BRAND ADDRESS, NEVER HIS OWN (Hidde, 2026-09-03: "ik wil nooit meer
    # burgmans.hidde ergens zien"). A reader who sends a tree gets an answer
    # from Ancient Trees, not from a private Gmail, which is PRINCIPLES.md #10
    # and was simply impossible until info@ancienttrees.app started receiving
    # today. It degrades to a dry run rather than raising, for the reason the
    # comment further down gives: this runs inside the digest workflow, and a
    # mail problem must never take the day's numbers with it.
    _from_addrs = re.findall(r"[\w.+-]+@[\w.-]+", creds["FROM"] or "")
    if really and not (_from_addrs and all(
            a.lower().endswith("@ancienttrees.app") for a in _from_addrs)):
        print("contributor_reply: OUTREACH_FROM is not an @ancienttrees.app "
              "address; dry run only. Replies go out as Ancient Trees.")
        really = False

    try:
        sent_log = json.load(open(SENT_PATH))
    except Exception:
        sent_log = {"sent": []}
    today = datetime.date.today().isoformat()
    sent_today = sum(1 for s in sent_log["sent"] if s.get("date") == today)
    dnc = {a.lower().strip() for a in sent_log.get("do_not_contact", [])}

    try:
        rows = supa("/rest/v1/submissions?select=id,created_at,kind,city,tree,"
                    "why,page,location_hint,user_id,email,outcome,reply_text,"
                    "thanked_at,replied_at"
                    "&or=(user_id.not.is.null,email.not.is.null)"
                    "&order=created_at.asc", key)
    except Exception as e:
        # Before Hidde pastes the SQL these columns do not exist and this
        # select 400s; that is the expected state, not an error worth a red run.
        print("contributor_reply: submissions not readable yet (%s)" % str(e)[:80])
        return 0
    rows = rows or []

    # The account IS the reply channel (2026-08-21 ruling): resolve user_id
    # to the account's email at send time, storing no second copy. The email
    # column is the legacy/fallback path only.
    users = {}
    page = 1
    while page <= 10:
        got = supa("/auth/v1/admin/users?page=%d&per_page=1000" % page, key)
        batch = (got or {}).get("users") or []
        for u in batch:
            if u.get("id") and u.get("email"):
                users[u["id"]] = u["email"]
        if len(batch) < 1000:
            break
        page += 1

    def address(r):
        return ((r.get("email") or "").strip()
                or users.get(r.get("user_id") or "", "")).strip()

    def mailable(r):
        """A privacy request is handled by hand and a vote-undo is bookkeeping."""
        return (r.get("kind") != "privacy"
                and not (r.get("why") or "").startswith("vote undone"))

    # One mail per address covers every unthanked row that address left, since
    # the stamping below already does. So the tips are gathered per address
    # first, and the mail names all of them rather than the one row that
    # happened to trigger it.
    unthanked = {}
    for r in rows:
        addr = address(r).lower()
        if addr and mailable(r) and not r.get("thanked_at"):
            unthanked.setdefault(addr, []).append(r)

    jobs = []  # (row, subject, body, column_to_stamp)
    thanked_addrs = set()
    for r in rows:
        addr = address(r).lower()
        if not addr:
            continue
        why = (r.get("why") or "")
        if r.get("kind") == "privacy":
            print("PRIVACY row %s from %s: handle in session, never auto-mail"
                  % (r["id"], addr))
            continue
        if why.startswith("vote undone"):
            continue
        if only != "answers" and not r.get("thanked_at") and addr not in thanked_addrs:
            subj = THANKS_SUBJECT.get(r.get("kind"), THANKS_SUBJECT["feedback"])
            jobs.append((r, subj, thanks_body(unthanked.get(addr, [r]), addr),
                         "thanked_at"))
            thanked_addrs.add(addr)
        if only == "thanks":
            continue
        # STAGE TWO, AUTOMATIC (Hidde, 2026-09-01): "if we put it on the
        # website give a confirmation with the page". A run that acted on a
        # submission sets outcome 'changed'; it should not also have to write
        # the mail. When it did write one, that wins, because a specific
        # answer always beats a template.
        if (r.get("outcome") == "changed" and not r.get("reply_text")
                and not r.get("replied_at")):
            # The tree's own page when we can name it, the city page
            # otherwise. It used to read the row's `page` column, which the
            # select did not even carry, and which holds the referrer rather
            # than the tree: a reader who arrived from Google would have been
            # sent a link to Google.
            page = tip_link(r)
            if not page and r.get("city"):
                page = "%s/%s" % (SITE, r["city"].strip().lower().replace(" ", "-"))
            thing = (r.get("tree") or "").strip()
            lines = ["Thank you again. What you sent us is on the site now."]
            if thing:
                lines.append("")
                lines.append("%s: %s" % (thing, page or SITE))
            elif page:
                lines.append("")
                lines.append(page)
            lines += ["",
                      "Have a look and tell us if anything is still wrong. And "
                      "if you know another tree worth adding, we would like to "
                      "hear about it.",
                      "", "Ancient Trees", "https://ancienttrees.app"]
            r["reply_text"] = "\n".join(lines) + "\n"
            supa("/rest/v1/submissions?id=eq.%s" % r["id"], key, "PATCH",
                 {"reply_text": r["reply_text"]})
            print("AUTO composed a change confirmation for row %s" % r["id"])
        if r.get("reply_text") and not r.get("replied_at"):
            ok, report = mailcheck_ok(r["reply_text"])
            if not ok:
                print("HOLD reply for row %s: mailcheck says:\n%s"
                      % (r["id"], report))
                continue
            jobs.append((r, "About what you sent us: %s" % (r.get("tree") or
                         r.get("city") or "your tip"), r["reply_text"],
                         "replied_at"))

    server = None
    for r, subject, body, stamp in jobs:
        addr = address(r)
        low = addr.lower()
        if low in dnc or ("@" + low.split("@")[-1]) in dnc:
            print("SKIP %s: on the do-not-contact list, never overridden" % low)
            continue
        if sent_today >= DAILY_CAP:
            print("HOLD %s: daily cap of %d reached" % (low, DAILY_CAP))
            break
        if not really:
            print("DRY  would send %r to %s (then set %s on row %s)"
                  % (subject, low, stamp, r["id"]))
            continue
        msg = EmailMessage()
        msg["From"] = creds["FROM"]
        msg["To"] = addr
        msg["Subject"] = subject
        msg.set_content(body)
        # A MAIL PROBLEM MUST NEVER TAKE THE NUMBERS WITH IT. On 2026-08-22
        # this script raised SMTPAuthenticationError inside the data-digest
        # workflow, the job aborted on the spot, and the day's DATA.md entry
        # was written and then thrown away because the commit step never ran.
        # The thank-you can always wait for the next knock; the digest cannot
        # be rewritten after the fact, since it reads yesterday.
        try:
            if server is None:
                server = smtplib.SMTP(creds["SMTP_HOST"], int(creds["SMTP_PORT"]),
                                      timeout=30)
                server.starttls()
                server.login(creds["SMTP_USER"], creds["SMTP_PASS"])
            server.send_message(msg)
        except Exception as e:
            print("MAIL FAILED for %s: %s" % (low, str(e)[:160]))
            _note_transport(str(e)[:200])
            print("Nothing was stamped, so the next run tries again. "
                  "If this is a 535 BadCredentials, the app password in the "
                  "environment is wrong or has spaces in it.")
            return 0
        sent_today += 1
        _note_transport(None)
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        # Stamp every row of this address needing this stamp, so the
        # double-submit's siblings are covered by the one mail. The address
        # may come from either column, so match rows by resolving each.
        if stamp == "thanked_at":
            sibling_ids = [str(r2["id"]) for r2 in rows
                           if address(r2).lower() == low and not r2.get("thanked_at")]
            supa("/rest/v1/submissions?id=in.(%s)" % ",".join(sibling_ids),
                 key, "PATCH", {"thanked_at": now})
        else:
            supa("/rest/v1/submissions?id=eq.%s" % r["id"], key, "PATCH",
                 {"replied_at": now})
        sent_log["sent"].append({"date": today, "to": addr,
                                 "outlet": "contributor",
                                 "subject": subject,
                                 "batch": "contributor-reply"})
        json.dump(sent_log, open(SENT_PATH, "w"), ensure_ascii=False, indent=1)
        print("SENT %r to %s" % (subject, low))
    if server:
        server.quit()
    if not jobs:
        print("contributor_reply: nothing waiting")
        # PROVE THE TRANSPORT EVEN WITH AN EMPTY QUEUE. Added 2026-09-01: the
        # Gmail credentials were dead for two days and the only thing that
        # could have noticed was a mail actually trying to go. Most runs have
        # nothing to send, so on those runs the fault stayed invisible. One
        # login per run costs nothing and means health.py always knows whether
        # we could answer a reader if one wrote to us right now.
        if really and all(creds.values()):
            try:
                probe = smtplib.SMTP(creds["SMTP_HOST"], int(creds["SMTP_PORT"]),
                                     timeout=30)
                probe.starttls()
                probe.login(creds["SMTP_USER"], creds["SMTP_PASS"])
                probe.quit()
                _note_transport(None, sent=False)
                print("contributor_reply: transport ok")
            except Exception as e:
                _note_transport(str(e)[:200])
                print("TRANSPORT DEAD: %s" % str(e)[:160])
                print("Nobody is owed a mail right now, but the next reader "
                      "who writes to us could not be answered.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
