#!/usr/bin/env python3
"""Thank contributors and send them the run's answer. The transport half of
the contributor reply loop (spec: docs/superpowers/specs/
2026-08-21-contributor-reply-design.md; Hidde's ruling, 2026-08-21: input is
one of the core features and gets treated with care).

Two mail kinds, both from "Ancient Trees" via the outreach SMTP creds, with
standing approval given in session for exactly these two:

  THANK-YOU  templated, to any submission row with an email and no
             thanked_at. Sent once per address per day however many rows the
             double-submit left.
  ANSWER     the run-composed reply_text, to rows with an email, a
             reply_text, and no replied_at. mailcheck.py gates every one;
             a failing draft is held and printed, never sent.

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
import urllib.parse
import urllib.request
from email.message import EmailMessage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPA = "https://caimvxiyrtifilimlkqw.supabase.co"
SENT_PATH = os.path.join(ROOT, "data", "outreach-sent.json")
DAILY_CAP = int(os.environ.get("OUTREACH_DAILY_CAP", "50"))

THANKS_SUBJECT = {
    "tree": "Thank you, we received your tree tip",
    "city": "Thank you, we received your tree tip",
    "correction": "Thank you, we received your correction",
    "feedback": "Thank you, we received your report",
}

THANKS_BODY = """Thank you. Your input is very valuable: a real person telling us about a real tree is the best thing this project receives. Together we're building the best database of remarkable trees there is, and the point of it all is getting people outside, standing in front of something old and epic.

We check everything against independent sources, so give us a little time. We'll come back to you with what your input changed. And please feel free to send more: a tree you love, a correction, a photo. They all make the map better.

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
                    "why,email,outcome,reply_text,thanked_at,replied_at"
                    "&email=not.is.null&order=created_at.asc", key)
    except Exception as e:
        # Before Hidde pastes the SQL the email column does not exist and this
        # select 400s; that is the expected state, not an error worth a red run.
        print("contributor_reply: submissions not readable yet (%s)" % str(e)[:80])
        return 0
    rows = [r for r in rows or [] if (r.get("email") or "").strip()]

    jobs = []  # (row, subject, body, column_to_stamp)
    thanked_addrs = set()
    for r in rows:
        addr = r["email"].strip().lower()
        why = (r.get("why") or "")
        if r.get("kind") == "privacy":
            print("PRIVACY row %s from %s: handle in session, never auto-mail"
                  % (r["id"], addr))
            continue
        if why.startswith("vote undone"):
            continue
        if not r.get("thanked_at") and addr not in thanked_addrs:
            subj = THANKS_SUBJECT.get(r.get("kind"), THANKS_SUBJECT["feedback"])
            jobs.append((r, subj, THANKS_BODY, "thanked_at"))
            thanked_addrs.add(addr)
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
        addr = r["email"].strip()
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
        if server is None:
            server = smtplib.SMTP(creds["SMTP_HOST"], int(creds["SMTP_PORT"]),
                                  timeout=30)
            server.starttls()
            server.login(creds["SMTP_USER"], creds["SMTP_PASS"])
        server.send_message(msg)
        sent_today += 1
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        # Stamp every row of this address needing this stamp, so the
        # double-submit's siblings are covered by the one mail.
        if stamp == "thanked_at":
            supa("/rest/v1/submissions?email=eq.%s&thanked_at=is.null"
                 % urllib.parse.quote(addr), key, "PATCH", {"thanked_at": now})
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
