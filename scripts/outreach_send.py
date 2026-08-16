#!/usr/bin/env python3
"""Send an approved outreach batch, with the guardrails in code.

The model, approved by Hidde 2026-08-08 ("bovenstaande mail strategie klinkt
ook goed"): the machine writes, addresses, sends and logs; Hidde authorises
per batch after reading the texts. This script is the sending half, and its
guardrails are not etiquette but code:

- DRY RUN by default. --send actually sends, and only works when the batch
  file's status is "approved_by_hidde" (he flips it, or says so in session).
- An address on the do-not-contact list is refused, always, and that beats
  every other rule here including a deliberate second batch. Added 2026-08-16:
  batches 003 and 004 closed with "if you would rather not hear from me again,
  just say so", and nothing in the machine could honour it. The list lives in
  data/outreach-sent.json and takes whole domains as "@example.org".
- An address that was ever mailed before is refused (data/outreach-sent.json),
  so nobody is double-mailed by a re-run or a second session. THIS GUARD IS
  ONLY AS GOOD AS THAT FILE, and on 2026-08-16 it was not good enough: the two
  licence asks Hidde sent by hand on 2026-08-08 lived in drafts/OUTREACH.md's
  markdown table, which no script reads, so a batch built that morning put the
  Woodland Trust back on the list eight days after his first ask. He spotted it,
  the script did not. Anything sent by hand goes in outreach-sent.json too.
- A daily cap, raised 10 -> 40 on 2026-08-09 and 40 -> 50 on 2026-08-16, both
  by Hidde ("we mogen zoveel
  mensen mailen als we zelf bedenken dat goed is"). It stays a number rather
  than becoming unlimited for one reason that is not caution: this sends from
  his own mailbox, and a burst of cold mail that bounces or gets marked as
  spam damages the domain's sending reputation, after which his OWN mail
  (waitlist, replies, anything he writes later) starts landing in spam
  folders. That is slow to undo and invisible until it has happened. Forty a
  day from a young domain is already assertive; the cap's job is to stop a
  bug from blasting the same list fifty times, not to stop him.
- A mail with an empty "to" is skipped with a warning, never guessed.
- Every send is appended to data/outreach-sent.json AND printed for the
  OUTREACH.md log.

Credentials come from the environment, set up once by Hidde (his mailbox,
his app password; the machine never stores them):
  OUTREACH_SMTP_HOST  e.g. smtp.gmail.com
  OUTREACH_SMTP_PORT  e.g. 587
  OUTREACH_SMTP_USER  the account that authenticates
  OUTREACH_SMTP_PASS  an app password, never his real one
  OUTREACH_FROM       e.g. "Hidde, Ancient Trees <press@ancienttrees.app>"

Usage:
  python3 scripts/outreach_send.py drafts/batches/batch-001-nl-regio.json
  python3 scripts/outreach_send.py drafts/batches/batch-001-nl-regio.json --send
"""
import datetime
import json
import os
import smtplib
import sys
from email.message import EmailMessage
from email.utils import formataddr, parseaddr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SENT_PATH = os.path.join(ROOT, "data", "outreach-sent.json")
DAILY_CAP = int(os.environ.get("OUTREACH_DAILY_CAP", "50"))


def load_sent():
    try:
        return json.load(open(SENT_PATH))
    except Exception:
        return {"note": "Every outreach mail ever sent by the machine, so no "
                        "address is ever mailed twice without a human deciding "
                        "to. Appended by scripts/outreach_send.py.",
                "sent": []}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    batch_path = sys.argv[1]
    really = "--send" in sys.argv
    batch = json.load(open(batch_path))
    sent_log = load_sent()
    today = datetime.date.today().isoformat()
    sent_today = sum(1 for s in sent_log["sent"] if s["date"] == today)
    already = {s["to"].lower() for s in sent_log["sent"]}
    dnc = {a.lower().strip() for a in sent_log.get("do_not_contact", [])}


    if really and batch.get("status") != "approved_by_hidde":
        print(f"REFUSED: batch status is {batch.get('status')!r}, sending needs "
              f"'approved_by_hidde'. Hidde reads the texts, then the status flips.")
        return 1

    creds = {k: os.environ.get(f"OUTREACH_{k}") for k in
             ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS", "FROM")}
    if really and not all(creds.values()):
        missing = [k for k, v in creds.items() if not v]
        print(f"REFUSED: missing environment: {', '.join('OUTREACH_' + m for m in missing)}")
        return 1

    server = None
    results = []
    for m in batch["mails"]:
        to = (m.get("to") or "").strip()
        label = m.get("outlet", to or "?")
        if not to or "@" not in parseaddr(to)[1]:
            results.append(f"SKIP  {label}: no verified address, never guessed")
            continue
        if to.lower() in already:
            results.append(f"SKIP  {label}: {to} was already mailed on a previous run")
            continue
        # The promise we made in writing, now enforced. Batches 003 and 004
        # closed with "if you would rather not hear from me again, just say
        # so", and until 2026-08-16 nothing in the machine could honour that:
        # an address that asked to be left alone was protected only by the
        # once-only rule, which expires the moment somebody writes a second
        # batch on purpose. An entry here is permanent and beats every other
        # rule in this file, including a deliberate re-send. Domains are
        # allowed ("@example.org") for an organisation that asks as a whole.
        if to.lower() in dnc or ("@" + to.lower().split("@")[-1]) in dnc:
            results.append(f"SKIP  {label}: {to} is on the do-not-contact list, "
                           f"which is never overridden")
            continue
        if sent_today >= DAILY_CAP:
            results.append(f"HOLD  {label}: daily cap of {DAILY_CAP} reached, "
                           f"re-run tomorrow")
            continue
        if not really:
            results.append(f"DRY   {label}: would send {m['subject']!r} to {to}")
            continue
        msg = EmailMessage()
        msg["From"] = creds["FROM"]
        msg["To"] = to
        msg["Subject"] = m["subject"]
        msg.set_content(m["body"])
        if server is None:
            server = smtplib.SMTP(creds["SMTP_HOST"], int(creds["SMTP_PORT"]), timeout=30)
            server.starttls()
            server.login(creds["SMTP_USER"], creds["SMTP_PASS"])
        server.send_message(msg)
        sent_today += 1
        sent_log["sent"].append({"date": today, "to": to, "outlet": label,
                                 "subject": m["subject"], "batch": batch.get("batch")})
        json.dump(sent_log, open(SENT_PATH, "w"), ensure_ascii=False, indent=1)
        results.append(f"SENT  {label}: {to}")
    if server:
        server.quit()
    print(f"batch {batch.get('batch')} ({'SEND' if really else 'dry run'}):")
    for r in results:
        print(" ", r)
    if really and any(r.startswith("SENT") for r in results):
        print("\nAdd the sends to OUTREACH.md's log table, and commit "
              "data/outreach-sent.json in the same commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
