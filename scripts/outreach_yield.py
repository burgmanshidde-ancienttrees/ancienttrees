#!/usr/bin/env python3
"""What each outreach group gives back: mailed, answered, linked, per send week.

Hidde, 2026-10-30, after a week of 164 mails: we know how much goes out, not
which group answers or links, so we cannot tell which to grow. The replies log
(data/outreach-replies.json) was kept by hand and stopped on 2026-10-07, so this
reads the answers from the mailbox itself: every message in All Mail from an
address we mailed (or another address at the same organisation's own domain),
dated after our first mail to it. Out-of-office replies are counted apart and
never as an answer. A link is a live page in data/backlinks.json on a domain we
mailed, or a contact marked linked=yes in the outreach database.

Writes data/mail-yield.json: counts per group and per send week, no address,
no name, no organisation, so it is committed and the weekly analyst reads it.
New answers are appended to data/outreach-replies.json (private) as kind
"inbox", so contacts_db.py marks them replied.

    python3 scripts/outreach_yield.py            # reads the mailbox when it can
    python3 scripts/outreach_yield.py --no-mail  # from the replies log only

Runs daily in data-digest.yml after private_store.py pull.
"""
import collections
import datetime
import email
import email.utils
import imaplib
import json
import os
import re
import sys
from email.header import decode_header, make_header

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contacts_db import FREEMAIL, SEGMENTS, norm  # noqa: E402
from sent_drafts import load_env, ours  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(DATA, "mail-yield.json")
REPLIES = os.path.join(DATA, "outreach-replies.json")
DAYS = 120
AUTO = re.compile(r"out of (the )?office|automatic reply|auto.?reply|automatische|abwesenheit|"
                  r"afwezig|r[ée]ponse automatique|absence|risposta automatica|fuori ufficio|"
                  r"resposta autom[aá]tica|respuesta autom[aá]tica|fuera de la oficina|"
                  r"autosvar|frånvaro|delivery status|undeliverable|mail delivery|returned mail", re.I)


def load(path, default):
    try:
        return json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        return default


def monday(day):
    d = datetime.date.fromisoformat(day[:10])
    return (d - datetime.timedelta(days=d.weekday())).isoformat()


def host(url):
    h = re.sub(r"^https?://", "", url or "").split("/")[0].lower()
    return h[4:] if h.startswith("www.") else h


def inbox(since):
    """(from, date, auto) for every message in All Mail since `since`. Headers only."""
    user, pw = os.environ.get("OUTREACH_SMTP_USER"), os.environ.get("OUTREACH_SMTP_PASS")
    if not (user and pw):
        return None
    me = ours()
    d = imaplib.IMAP4_SSL(os.environ.get("OUTREACH_IMAP_HOST", "imap.gmail.com"), timeout=30)
    d.login(user, pw)
    d.select('"[Gmail]/All Mail"', readonly=True)
    day = datetime.date.fromisoformat(since)
    ok, data = d.search(None, "(SINCE %s)" % day.strftime("%d-%b-%Y"))
    ids = data[0].split() if ok == "OK" else []
    out = []
    for i in range(0, len(ids), 200):
        ok, rows = d.fetch(b",".join(ids[i:i + 200]),
                           "(BODY.PEEK[HEADER.FIELDS (FROM DATE SUBJECT AUTO-SUBMITTED X-AUTOREPLY)])")
        for row in rows if ok == "OK" else []:
            if not isinstance(row, tuple):
                continue
            h = email.message_from_bytes(row[1])
            sender = email.utils.parseaddr(h.get("From") or "")[1].lower()
            if not sender or sender in me:
                continue
            try:
                subj = str(make_header(decode_header(h.get("Subject") or "")))
                when = email.utils.parsedate_to_datetime(h.get("Date")).date().isoformat()
            except Exception:
                continue
            auto = (h.get("Auto-Submitted") or "no").lower() != "no" or bool(h.get("X-Autoreply")) \
                or bool(AUTO.search(subj))
            out.append((sender, when, auto))
    d.logout()
    return out


def main():
    load_env()
    sent = load(os.path.join(DATA, "outreach-sent.json"), None)
    if not sent:
        print("outreach_yield: data/outreach-sent.json unreadable (private_store.py pull first)")
        return 0
    db = load(os.path.join(DATA, "outreach-db.json"), {}).get("contacts", {})
    replies_doc = load(REPLIES, {"replies": []})

    # Every address we mailed, with its first mail and its group.
    first = {}
    for m in sent.get("sent", []):
        a, day = norm(m.get("to")), str(m.get("date") or "")[:10]
        if a and day and (a not in first or day < first[a]):
            first[a] = day
    seg = {a: (db.get(a) or {}).get("segment", "other") for a in first}
    by_domain = collections.defaultdict(list)
    for a in first:
        dom = a.split("@")[-1]
        if dom not in FREEMAIL:
            by_domain[dom].append(a)

    def who(sender):
        """The mailed address a sender answers for, or None."""
        if sender in first:
            return sender
        hits = by_domain.get(sender.split("@")[-1]) or []
        return min(hits, key=lambda a: first[a]) if hits else None

    answered, autos = {}, set()
    for r in replies_doc.get("replies", []):
        a = norm(r.get("to_address"))
        if a in first:
            if r.get("kind") == "auto":
                autos.add(a)
            else:
                answered.setdefault(a, str(r.get("date") or first[a])[:10])
    since = (datetime.date.today() - datetime.timedelta(days=DAYS)).isoformat()
    mail = None if "--no-mail" in sys.argv else inbox(since)
    new = []
    for sender, when, auto in mail or []:
        a = who(sender)
        if not a or when < first[a]:
            continue
        if auto:
            autos.add(a)
        elif a not in answered:
            answered[a] = when
            new.append({"date": when, "to_address": a, "from": sender, "type": seg[a], "kind": "inbox",
                        "gave": "an answer in the mailbox (outreach_yield.py, not yet read)"})
    if new:
        replies_doc.setdefault("replies", []).extend(new)
        json.dump(replies_doc, open(REPLIES, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    linked = {a for a, r in db.items() if r.get("linked") == "yes" and a in first}
    for page, s in load(os.path.join(DATA, "backlinks.json"), {}).get("seen", {}).items():
        if s.get("state") == "live":
            linked.update(by_domain.get(host(page), []))

    weeks = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.Counter()))
    total = collections.defaultdict(collections.Counter)
    for a, day in first.items():
        for bucket in (weeks[monday(day)][seg[a]], total[seg[a]]):
            bucket["mailed"] += 1
            bucket["answered"] += a in answered
            bucket["only_auto"] += a in autos and a not in answered
            bucket["linked"] += a in linked
    order = {s: i for i, s in enumerate(SEGMENTS)}
    doc = {
        "_note": "Per outreach group: addresses mailed, how many answered (a human reply, out-of-office "
                 "left out), how many link to us. 'weeks' is keyed by the Monday of the week of our FIRST "
                 "mail, so a week's answers keep arriving for weeks after. Counts only, no addresses. "
                 "Built by scripts/outreach_yield.py.",
        "built": datetime.date.today().isoformat(),
        "mailbox_read": mail is not None,
        "total": {s: dict(total[s]) for s in sorted(total, key=lambda s: order.get(s, 99))},
        "weeks": {w: {s: dict(c) for s, c in sorted(g.items(), key=lambda kv: order.get(kv[0], 99))}
                  for w, g in sorted(weeks.items(), reverse=True) if w >= since},
    }
    json.dump(doc, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"{'group':10}{'mailed':>8}{'answered':>10}{'rate':>7}{'linked':>8}   (mailbox read: {mail is not None}, "
          f"{len(new)} new answers logged)")
    for s, c in doc["total"].items():
        rate = f"{100 * c.get('answered', 0) / c['mailed']:.0f}%" if c["mailed"] else "-"
        print(f"{s:10}{c['mailed']:>8}{c.get('answered', 0):>10}{rate:>7}{c.get('linked', 0):>8}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
