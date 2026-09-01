#!/usr/bin/env python3
"""Thank contributors and send them the run's answer. The transport half of
the contributor reply loop (spec: docs/superpowers/specs/
2026-08-21-contributor-reply-design.md; Hidde's ruling, 2026-08-21: input is
one of the core features and gets treated with care).

Two mail kinds, both from "Ancient Trees" via the outreach SMTP creds, with
standing approval given in session for exactly these two:

  THANK-YOU  templated, to any submission row we can answer and that has no
             thanked_at. Sent once per address however many rows a
             double-submit left.
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
import smtplib
import subprocess
import sys
import tempfile
import urllib.request
from email.message import EmailMessage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPA = "https://caimvxiyrtifilimlkqw.supabase.co"
SENT_PATH = os.path.join(ROOT, "data", "outreach-sent.json")
DAILY_CAP = int(os.environ.get("OUTREACH_DAILY_CAP", "50"))


HEALTH_PATH = os.path.join(ROOT, "data", "mail-health.json")


def _note_transport(error):
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
        state["last_sent_at"] = now
        state["consecutive_failures"] = 0
        state.pop("last_error", None)
    try:
        with open(HEALTH_PATH, "w") as fh:
            json.dump(state, fh, indent=2, sort_keys=True)
            fh.write("\n")
    except OSError:
        pass


THANKS_SUBJECT = {
    "tree": "Thank you, we received your tree tip",
    "city": "Thank you, we received your tree tip",
    "correction": "Thank you, we received your correction",
    "feedback": "Thank you, we received your report",
}

THANKS_BODY = """Thank you for your feedback. We are looking into it and we will come back to you with what it changed.

Please keep them coming: a tree you love, a mistake we have made, a photograph. Every one of them makes the map better, and a real person telling us about a real tree is the best thing this project receives.

We are also building an iPhone app. It is not live yet, and it will make this much easier: you photograph a tree standing in front of it and it reaches us with the location attached. You can put your name down here and we will tell you when it is out:

https://ancienttrees.app/app

Ancient Trees
https://ancienttrees.app
"""


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

    try:
        sent_log = json.load(open(SENT_PATH))
    except Exception:
        sent_log = {"sent": []}
    today = datetime.date.today().isoformat()
    sent_today = sum(1 for s in sent_log["sent"] if s.get("date") == today)
    dnc = {a.lower().strip() for a in sent_log.get("do_not_contact", [])}

    try:
        rows = supa("/rest/v1/submissions?select=id,created_at,kind,city,tree,"
                    "why,user_id,email,outcome,reply_text,thanked_at,replied_at"
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
            jobs.append((r, subj, THANKS_BODY, "thanked_at"))
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
            page = (r.get("page") or "").strip()
            if not page and r.get("city"):
                page = "https://ancienttrees.app/%s" % (
                    r["city"].strip().lower().replace(" ", "-"))
            thing = (r.get("tree") or "").strip()
            lines = ["Thank you again. What you sent us is on the site now."]
            if thing:
                lines.append("")
                lines.append("%s: %s" % (thing, page or "https://ancienttrees.app"))
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
