#!/usr/bin/env python3
"""Read the replies to our own outreach out of Hidde's mailbox, and nothing else.

Hidde, 2026-08-22: "ik krijg echt veel reacties het liefst hoef ik ze niet
allemaal door te geven en lees je ze zelf en hou je bij wat werkt en niet."
So this exists to take the forwarding out of his day. It is his personal
mailbox, so the point of this script is not what it can fetch but what it
refuses to look at.

THE FILTER, and it is the whole design:

- Read-only. The mailbox is selected with readonly=True, so nothing is marked
  read, moved or deleted. This script cannot write to his mail account, and it
  never sends: sending stays scripts/outreach_send.py, which needs his word.
- Only senders we wrote to first. A message is opened only when its From
  address, or its From domain, appears in data/outreach-sent.json. Everything
  else is counted and skipped without its subject or body ever being read.
  A stranger's mail, a bank, a friend: never opened.
- Only since the first batch (2026-08-08). Nothing older is fetched at all.
- --list prints senders and subjects only, no bodies, so the filter can be
  checked before anything personal is read. Run that first.

Usage:
  source ~/.ancienttrees-mail.env
  python3 scripts/outreach_inbox.py --list        # who replied, subjects only
  python3 scripts/outreach_inbox.py --read        # bodies of matched threads
  python3 scripts/outreach_inbox.py --read --since 2026-08-20

Credentials: the same ones the sender already uses (OUTREACH_SMTP_USER and
OUTREACH_SMTP_PASS). A Gmail app password works for IMAP unchanged, so this
adds no new secret. IMAP host defaults to imap.gmail.com and can be overridden
with OUTREACH_IMAP_HOST.
"""
import email
import email.utils
import imaplib
import json
import os
import sys
from email.header import decode_header, make_header

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIRST_BATCH = "2026-08-08"


def allowed_senders():
    """Addresses we mailed, and their domains. Nothing else is ever opened."""
    d = json.load(open(os.path.join(ROOT, "data", "outreach-sent.json")))
    addrs = {s["to"].lower().strip() for s in d["sent"]}
    domains = {a.split("@")[-1] for a in addrs}
    # Personal replies often come from a colleague at the same organisation, so
    # the organisation's domain is allowed as well as the exact address. FREE
    # MAIL IS NOT, and this is the correction that matters: we have written to
    # a handful of gmail addresses, so the first version of this rule made
    # gmail.com an allowed domain and put every private message in his inbox
    # inside the filter. A free-mail sender must match the exact address we
    # wrote to, never the domain.
    FREEMAIL = {"gmail.com", "googlemail.com", "hotmail.com", "hotmail.nl",
                "outlook.com", "live.nl", "live.com", "yahoo.com", "yahoo.fr",
                "icloud.com", "me.com", "gmx.de", "gmx.net", "web.de",
                "protonmail.com", "proton.me", "seznam.cz", "xs4all.nl",
                "ziggo.nl", "kpnmail.nl", "planet.nl", "telenet.be", "sapo.pt",
                "libero.it", "alice.it", "wanadoo.fr", "orange.fr", "free.fr"}
    domains -= FREEMAIL
    return addrs, domains


def decode(s):
    try:
        return str(make_header(decode_header(s or "")))
    except Exception:
        return s or ""


def body_of(msg, limit=4000):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    return part.get_payload(decode=True).decode(
                        part.get_content_charset() or "utf-8", "replace")[:limit]
                except Exception:
                    continue
        return "(no plain-text part)"
    try:
        return msg.get_payload(decode=True).decode(
            msg.get_content_charset() or "utf-8", "replace")[:limit]
    except Exception:
        return "(unreadable)"


def main():
    read_bodies = "--read" in sys.argv
    since = FIRST_BATCH
    if "--since" in sys.argv:
        since = sys.argv[sys.argv.index("--since") + 1]
    user = os.environ.get("OUTREACH_SMTP_USER")
    pw = os.environ.get("OUTREACH_SMTP_PASS")
    host = os.environ.get("OUTREACH_IMAP_HOST", "imap.gmail.com")
    if not (user and pw):
        print("REFUSED: source ~/.ancienttrees-mail.env first "
              "(OUTREACH_SMTP_USER / OUTREACH_SMTP_PASS).")
        return 1

    addrs, domains = allowed_senders()
    d = imaplib.IMAP4_SSL(host)
    d.login(user, pw)
    d.select("INBOX", readonly=True)          # readonly: cannot change his mail
    y, m, dd = since.split("-")
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][int(m) - 1]
    ok, data = d.search(None, f'(SINCE {int(dd)}-{month}-{y})')
    ids = data[0].split()
    matched, skipped = [], 0
    for i in ids:
        ok, hdr = d.fetch(i, "(BODY.PEEK[HEADER.FIELDS (FROM DATE SUBJECT)])")
        if ok != "OK" or not hdr or not hdr[0]:
            continue
        h = email.message_from_bytes(hdr[0][1])
        frm = email.utils.parseaddr(h.get("From", ""))[1].lower()
        if not frm or (frm not in addrs and frm.split("@")[-1] not in domains):
            skipped += 1                       # never opened, never printed
            continue
        matched.append((i, frm, decode(h.get("Subject")), h.get("Date", "")))

    print(f"inbox since {since}: {len(ids)} messages, {len(matched)} from "
          f"addresses we wrote to, {skipped} never opened.\n")
    for i, frm, subj, date in matched:
        print(f"--- {date}\n    from: {frm}\n    subj: {subj}")
        if read_bodies:
            ok, raw = d.fetch(i, "(BODY.PEEK[])")
            if ok == "OK" and raw and raw[0]:
                print("    ---")
                for line in body_of(email.message_from_bytes(raw[0][1])).splitlines():
                    print("    " + line)
        print()
    d.logout()
    if not read_bodies:
        print("Bodies not read. Re-run with --read once this list looks right.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
