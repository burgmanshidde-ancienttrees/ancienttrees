#!/usr/bin/env python3
"""Which drafted mails have gone out, so nobody has to tell us.

Hidde, 2026-10-26: "die ambassadeurs zijn al gemaild - kun je mn mail checken
of bijhouden zodat ik je niet steeds de status hoef te vertellen". The four
ambassador mails and the archive batch had gone on 10-25, both through
outreach_send.py, yet the digest's Waiting for you, the night run ("the archive
batch still waits for Hidde") and a session all still called them waiting: each
read a "For Hidde:" line in LOG.md, and none checked the send log or his mail.

So every draft gets a status from the evidence:

- The recipients and subjects a draft names: `To:` lines and addresses in a
  drafts/*.md file, `Subject:` lines, and the `to`/`subject` of every mail in a
  drafts/batches/*.json file (the batch files and previews sync through the
  private store, so the digest runner sees them too).
- data/outreach-sent.json, where every script-sent mail is logged.
- His Gmail "Sent Mail" folder, HEADERS ONLY (To, Subject, Date), read-only,
  for what he sent by hand. Only a message to an address or with a subject one
  of our drafts names counts; the rest of his sent mail is never kept. A
  hand-sent match is written into outreach-sent.json, so the one-week rest
  (mailer.py) and every later check know it too.

A draft is `sent` when every address it names got a mail on or after the day
it was drafted (or, for a draft with no address, every subject it names was
sent), `partly` when some did, `open` when none did, and `not_mail` when it
names neither (the Reddit previews). The result is data/outreach-drafts.json
(private, gitignored, synced by private_store.py).

Usage:
  python3 scripts/sent_drafts.py            # scan, check, write, print what is open
  python3 scripts/sent_drafts.py --all      # the same, and list every sent draft
  python3 scripts/sent_drafts.py --quiet    # same, print nothing (brief.py, CI)
  python3 scripts/sent_drafts.py --no-mail  # send log only, never the mailbox

Credentials: OUTREACH_SMTP_USER / OUTREACH_SMTP_PASS from the environment, or
~/.ancienttrees-mail.env on the Mac (the same app password as outreach_inbox.py).
"""
import datetime
import email
import email.utils
import glob
import imaplib
import json
import os
import re
import sys
from email.header import decode_header, make_header

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUS = os.path.join(ROOT, "data", "outreach-drafts.json")
SENT = os.path.join(ROOT, "data", "outreach-sent.json")
ENV_FILE = os.path.expanduser("~/.ancienttrees-mail.env")
HAND = "sent by hand from Gmail, recorded by sent_drafts.py"
DAYS = 30                     # drafts older than this are left as they stand
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# Reference documents, not drafts: they name dozens of addresses.
NOT_DRAFTS = {"OUTREACH.md", "HIS_VOICE.md", "PITCH_VOICE.md", "ambassador-prospects.md",
              "ambassador-mails.md", "OUTREACH_STRATEGY.md",
              "lisbon-ten.md",            # the research list behind lisbon-ten-mails.md
              "photo-live-mail.md",       # a template, sent by sightings_publish.py
              "reddit-lisbon.md"}         # a Reddit post, not a mail


def load_env():
    if os.environ.get("OUTREACH_SMTP_USER") or not os.path.exists(ENV_FILE):
        return
    for line in open(ENV_FILE, encoding="utf-8"):
        m = re.match(r"\s*(?:export\s+)?(OUTREACH_[A-Z_]+)=(.*)", line)
        if m:
            os.environ.setdefault(m.group(1), m.group(2).strip().strip('"'))


def ours():
    out = {"info@ancienttrees.app", "hello@ancienttrees.app"}
    for k in ("OUTREACH_SMTP_USER", "OUTREACH_FROM"):
        a = email.utils.parseaddr(os.environ.get(k) or "")[1].lower()
        if a:
            out.add(a)
    return out


def norm_subject(s):
    t = (s or "").strip().lower()
    while True:
        for p in ("re:", "fwd:", "fw:", "aw:", "antw:", "wg:", "r:"):
            if t.startswith(p):
                t = t[len(p):].strip()
                break
        else:
            return re.sub(r"\s+", " ", t)


def made_date(path):
    m = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(path))
    if m:
        return m.group(1)
    # Creation time, not mtime: a private_store pull rewrote every synced
    # draft on 2026-10-25, which made August batches look a day old.
    st = os.stat(path)
    return datetime.date.fromtimestamp(getattr(st, "st_birthtime", st.st_mtime)).isoformat()


def from_md(path, skip):
    text = open(path, encoding="utf-8", errors="replace").read()
    to = {a.lower().rstrip(".") for a in EMAIL.findall(text)} - skip
    subjects = set()
    for m in re.finditer(r"^[\s>*-]*\**subject\**\s*:\s*(.+)$", text, flags=re.I | re.M):
        s = re.sub(r"\s*\([^)]*\)\s*$", "", m.group(1)).strip().strip("*` ")
        if s:
            subjects.add(norm_subject(s))
    return to, subjects


def from_json(path, skip):
    try:
        doc = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        return set(), set()
    mails = doc.get("mails") if isinstance(doc, dict) else doc
    to, subjects = set(), set()
    for m in mails or []:
        if isinstance(m, dict):
            a = (m.get("to") or "").lower().strip()
            if a and a not in skip:
                to.add(a)
            if m.get("subject"):
                subjects.add(norm_subject(m["subject"]))
    return to, subjects


def scan(drafts, skip):
    """Add or refresh every recent draft present on this machine; drafts that
    are not here (the digest runner has no session drafts) keep their row."""
    cutoff = (datetime.date.today() - datetime.timedelta(days=DAYS)).isoformat()
    paths = glob.glob(os.path.join(ROOT, "drafts", "*.md")) + \
        glob.glob(os.path.join(ROOT, "drafts", "batches", "*.json"))
    for p in paths:
        if os.path.basename(p) in NOT_DRAFTS:
            continue
        made = made_date(p)
        if made < cutoff:
            continue
        rel = os.path.relpath(p, ROOT)
        to, subjects = (from_json if p.endswith(".json") else from_md)(p, skip)
        twin = os.path.join(ROOT, "drafts", "batches",
                            os.path.basename(p)[:-3] + ".json")
        if not (to or subjects) and p.endswith(".md") and os.path.exists(twin):
            # reply-katherine-2026-10-22.md names no address; the batch file
            # it was sent from, under the same name, does.
            to, subjects = from_json(twin, skip)
        row = drafts.setdefault(rel, {})
        made = min(made, row.get("made") or made)   # a Linux runner has no birthtime
        row.update({"made": made, "to": sorted(to), "subjects": sorted(subjects)})
        row.setdefault("sent", {})


def sent_log():
    try:
        doc = json.load(open(SENT, encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return doc


def mailbox(since, wanted_to, wanted_subj):
    """(to, subject, date) of every message in his Sent folder since `since`
    that goes to a wanted address or carries a wanted subject. Headers only."""
    user, pw = os.environ.get("OUTREACH_SMTP_USER"), os.environ.get("OUTREACH_SMTP_PASS")
    if not (user and pw):
        return None
    d = imaplib.IMAP4_SSL(os.environ.get("OUTREACH_IMAP_HOST", "imap.gmail.com"), timeout=30)
    d.login(user, pw)
    d.select('"[Gmail]/Sent Mail"', readonly=True)
    day = datetime.date.fromisoformat(since)
    ok, data = d.search(None, "(SINCE %s)" % day.strftime("%d-%b-%Y"))
    hits = []
    for i in (data[0].split() if ok == "OK" else []):
        ok, hdr = d.fetch(i, "(BODY.PEEK[HEADER.FIELDS (TO CC BCC DATE SUBJECT)])")
        if ok != "OK" or not hdr or not hdr[0]:
            continue
        h = email.message_from_bytes(hdr[0][1])
        try:
            subj = str(make_header(decode_header(h.get("Subject") or "")))
            when = email.utils.parsedate_to_datetime(h.get("Date")).date().isoformat()
        except Exception:
            continue
        s = norm_subject(subj)
        tos = [a.lower() for _, a in email.utils.getaddresses(
            h.get_all("To", []) + h.get_all("Cc", []) + h.get_all("Bcc", []))]
        for a in tos:
            if a in wanted_to or s in wanted_subj:
                hits.append((a, subj, when))
    d.logout()
    return hits


def main():
    quiet = "--quiet" in sys.argv
    load_env()
    skip = ours()
    try:
        doc = json.load(open(STATUS, encoding="utf-8"))
    except (OSError, ValueError):
        doc = {"drafts": {}}
    drafts = doc.setdefault("drafts", {})
    scan(drafts, skip)
    log = sent_log()
    if log is None:
        print("REFUSED: data/outreach-sent.json unreadable (private_store.py pull first).")
        return 1
    rows = log.setdefault("sent", [])
    open_ = {k: v for k, v in drafts.items() if v.get("to") or v.get("subjects")}
    since = min([v["made"] for v in open_.values()] or [datetime.date.today().isoformat()])

    seen = [((r.get("to") or "").lower(), norm_subject(r.get("subject")), (r.get("date") or "")[:10])
            for r in rows if isinstance(r, dict)]
    added, box = 0, None
    if "--no-mail" not in sys.argv:
        want_to = {a for v in open_.values() for a in v.get("to", [])}
        want_subj = {s for v in open_.values() for s in v.get("subjects", [])}
        try:
            box = mailbox(since, want_to, want_subj)
        except Exception as e:
            if not quiet:
                print("(Sent folder not read: %s)" % e)
        # Every script send through Gmail leaves a copy in Sent too, dated in
        # UTC where the log has the local day: a copy within a day of a logged
        # row to the same address is that row, not a second mail.
        logged = {(a, d) for a, _, d in seen}

        def near(a, when):
            day = datetime.date.fromisoformat(when)
            return any((a, (day + datetime.timedelta(days=k)).isoformat()) in logged
                       for k in (-1, 0, 1))
        for a, subj, when in box or []:
            if not near(a, when):
                rows.append({"date": when, "to": a, "outlet": "sent by hand", "subject": subj,
                             "batch": HAND})
                logged.add((a, when))
                seen.append((a, norm_subject(subj), when))
                added += 1
        if added:
            with open(SENT, "w", encoding="utf-8") as fh:
                json.dump(log, fh, ensure_ascii=False, indent=1)

    for rel in [k for k in drafts if os.path.basename(k) in NOT_DRAFTS]:
        del drafts[rel]
    for rel, v in drafts.items():
        to, subjects, made = v.get("to", []), v.get("subjects", []), v.get("made", "")
        sent = v.setdefault("sent", {})
        for a, s, d in seen:
            if d < made:
                continue
            if a in to and a not in sent:
                sent[a] = d
            if s in subjects and ("subject:" + s) not in sent:
                sent["subject:" + s] = d
        if to:
            n = sum(1 for a in to if a in sent)
            total = len(to)
        elif subjects:
            n = sum(1 for s in subjects if ("subject:" + s) in sent)
            total = len(subjects)
        else:
            # A mail draft that names no address and no subject (reply-peter-
            # wifi-crash.md: "To: Peter Kálnai") cannot be checked: say so.
            mailish = re.match(r"(reply|mail|ambassador)-", os.path.basename(rel))
            v["status"] = "unknown" if mailish else "not_mail"
            continue
        v["status"] = "sent" if n == total else ("partly" if n else "open")
        v["count"] = "%d of %d" % (n, total)
        if n == total:
            v["sent_on"] = max(sent.values())

    doc["updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="minutes")
    doc["mailbox_read"] = box is not None
    with open(STATUS, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1, sort_keys=True)
    if quiet:
        return 0
    print("Sent folder %s; %d hand-sent mail(s) added to the send log." % (
        "read" if box is not None else "NOT read", added))
    for status in ("open", "partly", "unknown", "sent"):
        names = sorted(k for k, v in drafts.items() if v.get("status") == status)
        if status == "sent" and "--all" not in sys.argv:
            print("\nSENT: %d (--all lists them)" % len(names))
            continue
        if names:
            print("\n%s (%d):" % (status.upper(), len(names)))
            for k in names:
                v = drafts[k]
                print("  %s  %s%s" % (k, v.get("count", ""),
                                      ("  sent %s" % v["sent_on"]) if v.get("sent_on") else ""))
    return 0


def status_of(rel_path):
    """The status of one draft path ('drafts/x.md'), or None. For the digest."""
    try:
        doc = json.load(open(STATUS, encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return (doc.get("drafts", {}).get(rel_path) or {}).get("status")


def open_drafts(days=14):
    """Drafts of the last `days` still waiting to go out, for brief.py."""
    try:
        doc = json.load(open(STATUS, encoding="utf-8"))
    except (OSError, ValueError):
        return []
    cutoff = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    return sorted((k, v.get("count") or "no address to check")
                  for k, v in doc.get("drafts", {}).items()
                  if v.get("status") in ("open", "partly", "unknown")
                  and v.get("made", "") >= cutoff)


if __name__ == "__main__":
    sys.exit(main())
