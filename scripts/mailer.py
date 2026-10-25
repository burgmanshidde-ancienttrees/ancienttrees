"""One door for every mail we send, so it goes out signed for ancienttrees.app.

Why (2026-10-12): every mail went out through Hidde's Gmail wearing
info@ancienttrees.app, and Gmail signs such mail for gmail.com, never for our
domain. Yahoo refused it outright ("sender is unauthenticated ... DKIM"), and
other providers are free to file it as spam without saying so. Resend signs
with a DKIM key published under resend._domainkey.ancienttrees.app (set up at
TransIP the same day, with a DMARC record beside it).

So: when RESEND_SMTP_* is set, mail leaves through Resend; otherwise through
OUTREACH_SMTP_* exactly as before, so a machine without the new key keeps
working. Gmail is still the inbox (replies arrive through ImprovMX), and a
mail sent through Resend never lands in Gmail's Sent folder by itself, which
outreach_inbox.py reads to know what was answered. keep_copy() puts it there.

    server = mailer.connect(creds)       # logged in, ready
    server.send_message(msg)             # sends, then files a copy in Sent
    server.quit()

ONE REST PERIOD ACROSS EVERY ROUTE (Hidde, 2026-10-25: "we hebben die porto
dude nu in totaal 3 keer gemaild kun je in het vervolg altijd checken voor je
mailt of we niet iemand al eerder hebben gemaild"). Five scripts send mail
(outreach batches, ambassador invitation, editor mail and heads-up, reader
replies, photo-live and congratulation mails) and each guarded only its own
history, so one person could hear from three of them in a week. Every one of
them sends through this door, so the check lives here: an address that got any
mail logged in data/outreach-sent.json in the last RECENT_DAYS is refused with
RecentlyMailed. The automatic routes catch it and try again on a later knock.
Let through without the check: a reply in a thread (In-Reply-To set), and a
caller that passes recent_ok, a sentence saying why (an answer to a message
the person just sent us).
"""
import datetime
import imaplib
import json
import os
import smtplib
import time
from email.utils import formatdate, make_msgid, parseaddr

SENT_LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "outreach-sent.json")
RECENT_DAYS = 7


class RecentlyMailed(Exception):
    pass


def last_sent(addr, days=RECENT_DAYS):
    """The latest logged mail to this address within `days`, or None. A missing
    log answers None: the routes that send pull it first (nightly.yml)."""
    addr = (addr or "").strip().lower()
    try:
        sent = json.load(open(SENT_LOG, encoding="utf-8")).get("sent", [])
    except (OSError, ValueError):
        return None
    since = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    hits = [s for s in sent if (s.get("to") or "").strip().lower() == addr and (s.get("date") or "") >= since]
    return max(hits, key=lambda s: s.get("date") or "") if hits else None


def _route(creds):
    host = os.environ.get("RESEND_SMTP_HOST")
    if host and os.environ.get("RESEND_SMTP_PASS"):
        return (host, int(os.environ.get("RESEND_SMTP_PORT") or 587),
                os.environ.get("RESEND_SMTP_USER") or "resend",
                os.environ["RESEND_SMTP_PASS"], True)
    return (creds["SMTP_HOST"], int(creds["SMTP_PORT"]),
            creds["SMTP_USER"], creds["SMTP_PASS"], False)


def keep_copy(msg):
    """File a sent mail in Gmail's Sent folder, read with the same app password
    the inbox reader uses. Never raises: a missing copy costs a thread view,
    not the send."""
    user = os.environ.get("OUTREACH_SMTP_USER") or ""
    pw = os.environ.get("OUTREACH_SMTP_PASS")
    if not (user.endswith("@gmail.com") and pw):
        return
    try:
        box = imaplib.IMAP4_SSL(os.environ.get("OUTREACH_IMAP_HOST", "imap.gmail.com"), timeout=30)
        box.login(user, pw)
        box.append('"[Gmail]/Sent Mail"', "\\Seen",
                   imaplib.Time2Internaldate(time.time()), msg.as_bytes())
        box.logout()
    except Exception as e:  # noqa: BLE001
        print(f"mailer: sent, but no copy in Gmail's Sent folder ({type(e).__name__})")


class _Server:
    def __init__(self, smtp, copy):
        self._smtp, self._copy = smtp, copy

    def send_message(self, msg, recent_ok=None):
        if not recent_ok and not msg["In-Reply-To"]:
            prior = last_sent(parseaddr(msg["To"] or "")[1])
            if prior:
                raise RecentlyMailed(
                    f"{parseaddr(msg['To'])[1]} already had a mail on {prior.get('date')} "
                    f"({prior.get('batch') or prior.get('outlet') or '?'}: {(prior.get('subject') or '')[:60]}); "
                    f"{RECENT_DAYS}-day rest across every route")
        if not msg["Date"]:
            msg["Date"] = formatdate(localtime=True)
        if not msg["Message-ID"]:
            msg["Message-ID"] = make_msgid(domain="ancienttrees.app")
        self._smtp.send_message(msg)
        if self._copy:
            keep_copy(msg)

    def quit(self):
        try:
            self._smtp.quit()
        except Exception:  # noqa: BLE001
            pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.quit()


def connect(creds, timeout=30):
    host, port, user, pw, via_resend = _route(creds)
    smtp = smtplib.SMTP(host, port, timeout=timeout)
    smtp.starttls()
    smtp.login(user, pw)
    return _Server(smtp, via_resend)
