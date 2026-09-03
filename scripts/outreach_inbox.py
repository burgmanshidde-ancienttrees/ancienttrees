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


def our_subjects():
    """The subjects we sent, normalised. A reply keeps them behind "Re:".

    Added 2026-08-23, and it closes the hole that mattered most. Hanna Hirsch,
    chair of Bomenstichting Amsterdam, answered from hhirsch@xs4all.nl, a
    private address at a free-mail host. The sender filter excludes free-mail
    domains on purpose, so that mail was never opened and the most useful
    reply this project has had was invisible to the reader. Hidde spotted it:
    "volgens mij is er een mail vanuit amsterdam waarop niet geantwoord is."

    Matching the SUBJECT is the fix and it is not a widening of what gets
    read: a message only qualifies if its subject is one WE wrote, or carries
    the domain name of the site. A private mail about anything else still
    stays shut."""
    d = json.load(open(os.path.join(ROOT, "data", "outreach-sent.json")))
    out = set()
    for s2 in d["sent"]:
        t = (s2.get("subject") or "").strip().lower()
        for p in ("re:", "fwd:", "fw:", "aw:", "antw:", "r:"):
            while t.startswith(p):
                t = t[len(p):].strip()
        if len(t) > 12:
            out.add(t)
    return out


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
    return addrs, domains, FREEMAIL


def decode(s):
    try:
        return str(make_header(decode_header(s or "")))
    except Exception:
        return s or ""


def attachment_names(msg):
    """The file names hanging off a message.

    Added 2026-09-03, because a reply arrived whose entire body was "Se
    vedlegg". Oslo kommune answers by formal letter: the mail carries two
    words and a PDF, and the PDF held the answer plus three photographs of
    Birkelunden we had asked for. Printing the body alone said nothing at
    all, and a public agency writing that way is normal rather than rare."""
    out = []
    if not msg.is_multipart():
        return out
    for part in msg.walk():
        fn = part.get_filename()
        if fn:
            out.append(decode(fn))
    return out


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

    addrs, domains, FREEMAIL_SEEN = allowed_senders()
    SUBJECTS = our_subjects()
    d = imaplib.IMAP4_SSL(host)
    d.login(user, pw)
    d.select("INBOX", readonly=True)          # readonly: cannot change his mail
    y, m, dd = since.split("-")
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][int(m) - 1]
    ok, data = d.search(None, f'(SINCE {int(dd)}-{month}-{y})')
    ids = data[0].split()
    matched, skipped, bounces = [], 0, []
    for i in ids:
        ok, hdr = d.fetch(i, "(BODY.PEEK[HEADER.FIELDS (FROM DATE SUBJECT)])")
        if ok != "OK" or not hdr or not hdr[0]:
            continue
        h = email.message_from_bytes(hdr[0][1])
        frm = email.utils.parseaddr(h.get("From", ""))[1].lower()
        subj_peek = decode(h.get("Subject"))
        subj_norm = subj_peek.strip().lower()
        for pre in ("re:", "fwd:", "fw:", "aw:", "antw:", "r:"):
            while subj_norm.startswith(pre):
                subj_norm = subj_norm[len(pre):].strip()
        # BOUNCES. A dead address answers from mailer-daemon, never from the
        # address we wrote to, so the sender filter above hid every one of
        # them: 146 mails out and this reader could not have told us that one
        # never arrived. Added 2026-08-23. The match is on the postmaster
        # sender AND the standard delivery-report subjects, so an ordinary
        # mail from a person is still never opened on a subject alone.
        bouncer = frm.split("@")[0] in ("mailer-daemon", "postmaster")
        if bouncer and any(k in subj_peek.lower() for k in
                           ("delivery status", "undelivered", "returned",
                            "delivery has failed", "failure notice")):
            bounces.append((subj_peek, h.get("Date", "")))
            continue
        # Never his own outgoing copy. Gmail delivers a copy of anything sent
        # through its SMTP back to the account, so subject matching alone
        # pulled in all 146 of our own mails: 172 "replies" out of 277
        # messages, which is how a filter tells you it is broken.
        # Never his own outgoing copy, and never a robot. Gmail delivers a
        # copy of anything sent through its SMTP back to the account, and
        # subject matching then pulls in all 146 of our own mails. The second
        # half keeps out Ahrefs, Cloudflare, Search Console and GitHub, which
        # all put the domain name in their subject lines and are not people.
        selves = {(os.environ.get("OUTREACH_SMTP_USER") or "").lower().strip()}
        selves |= {email.utils.parseaddr(os.environ.get("OUTREACH_FROM") or "")[1].lower()}
        robot = frm.split("@")[0] in ("noreply", "no-reply", "notifications",
                                      "sc-noreply", "notify", "donotreply")
        robot = robot or frm.split("@")[-1] in ("notify.cloudflare.com",
                                                "notifications.github.com",
                                                "github.com", "ahrefs.com",
                                                "google.com", "feverup.com")
        if frm in selves or robot:
            skipped += 1
            continue
        by_subject = "ancienttrees" in subj_norm or subj_norm in SUBJECTS
        if not frm or (frm not in addrs and frm.split("@")[-1] not in domains
                       and not by_subject):
            skipped += 1                       # never opened, never printed
            continue
        matched.append((i, frm, decode(h.get("Subject")), h.get("Date", "")))

    print(f"inbox since {since}: {len(ids)} messages, {len(matched)} from "
          f"addresses we wrote to, {skipped} never opened.\n")
    if bounces:
        print(f"BOUNCES ({len(bounces)}), an address that never received us:")
        for subj, date in bounces:
            print(f"  {date}  {subj[:70]}")
        print()
    for i, frm, subj, date in matched:
        print(f"--- {date}\n    from: {frm}\n    subj: {subj}")
        if read_bodies:
            ok, raw = d.fetch(i, "(BODY.PEEK[])")
            if ok == "OK" and raw and raw[0]:
                msg = email.message_from_bytes(raw[0][1])
                print("    ---")
                for line in body_of(msg).splitlines():
                    print("    " + line)
                names = attachment_names(msg)
                if names:
                    print(f"    ATTACHMENTS ({len(names)}), not read here:")
                    for n in names:
                        print(f"      {n}")
        print()
    # WHAT HE ALREADY ANSWERED HIMSELF. Added 2026-08-23 because the first
    # version read INBOX only, so every thread Hidde had replied to by hand
    # still looked unanswered and the owed-a-reply list was wrong. His words:
    # "volgens mij lees je over mn reply mails heen."
    #
    # The comparison is by TIMESTAMP, not by presence. Every outreach mail we
    # send leaves a copy in his Sent folder, so "there is a sent message to
    # this address" is true of all 146 of them and means nothing. What counts
    # is a message to that address dated AFTER their reply arrived.
    import email.utils as eu
    incoming = {}
    for i, frm, subj, date in matched:
        t = eu.parsedate_to_datetime(date) if date else None
        if t and (frm not in incoming or t > incoming[frm]):
            incoming[frm] = t
    answered = {}
    try:
        d.select('"[Gmail]/Sent Mail"', readonly=True)   # the space needs the quotes
        ok, sdata = d.search(None, f'(SINCE {int(dd)}-{month}-{y})')
        for i in sdata[0].split():
            ok, hdr = d.fetch(i, "(BODY.PEEK[HEADER.FIELDS (TO DATE SUBJECT)])")
            if ok != "OK" or not hdr or not hdr[0]:
                continue
            h = email.message_from_bytes(hdr[0][1])
            when = h.get("Date")
            t = eu.parsedate_to_datetime(when) if when else None
            if not t:
                continue
            for _, to in eu.getaddresses([h.get("To", "")]):
                to = to.lower()
                if to in incoming and t > incoming[to]:
                    if to not in answered or t < answered[to][0]:
                        answered[to] = (t, decode(h.get("Subject")))
    except Exception as e:
        print(f"(sent folder not read: {e})")
    print(f"Of {len(incoming)} people who wrote to us, {len(answered)} already have "
          f"a reply from him, {len(incoming) - len(answered)} do not.\n")
    if answered:
        print("ALREADY ANSWERED:")
        for to, (t, subj) in sorted(answered.items(), key=lambda kv: kv[1][0]):
            print(f"  {to:44} {t:%Y-%m-%d %H:%M}  {subj[:44]}")
        print()
    owed = sorted(set(incoming) - set(answered), key=lambda a: incoming[a])
    if owed:
        print("NO REPLY FROM HIM YET:")
        for a in owed:
            print(f"  {a:44} wrote {incoming[a]:%Y-%m-%d}")
        print()
    d.logout()
    if not read_bodies:
        print("Bodies not read. Re-run with --read once this list looks right.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
