#!/usr/bin/env python3
"""Build the waitlist batch from Supabase, so the cutoff lives in code.

Hidde, 2026-09-10, on being shown one mail written for all seventeen rows:
"behalve de mensen die zich hebben aangemeld na de Android waitlist
hernoeming." The people who signed up after that rename were promised a mail
the day an ANDROID app exists, and the iPhone app being live is not that mail.

THE CUTOFF IS A TIMESTAMP, NOT THE `source` FIELD, and that is the whole
reason this is a script rather than a hand-filtered paste. Commit 71244a79 put
the device-aware form live at 2026-09-03T14:16:33Z. `source` looks like the
obvious discriminator and cannot be trusted here: 04af8338 and 49865e1b, both
from that same afternoon, record two submit listeners racing on /app and
writing different sources for one submit, swallowed silently by the table's
unique-email constraint. A row's creation time has no such history.

Four exclusions, all applied here rather than by eye. Our own test rows
(@ancienttrees.app: two of the seventeen are `chain-test` and `formuliertest`).
Anybody Hidde names as family or a colleague, in SKIP below with his words.
Anybody who ALREADY had the launch news in the 010-app-launch outreach batch,
which ran 3 to 8 September and reached 258 people; Quercus Setubal is on both
lists and being told twice in five days reads as a mailing list rather than a
letter. And anybody mailed about something ELSE keeps outreach_send.py's
never-twice guard satisfied on purpose, with a resend_reason, rather than
around it.

It writes a batch and sends nothing. The sending, its do-not-contact list, its
never-mail-twice guard and its daily cap all stay in outreach_send.py, which
also refuses to send a batch whose status is not `approved_by_hidde`:

    python3 scripts/waitlist_batch.py
    python3 scripts/outreach_send.py drafts/batches/waitlist-app-live.json
    python3 scripts/outreach_send.py drafts/batches/waitlist-app-live.json --send

The copy has one home, `drafts/waitlist-app-live.md`, read from below the
`---` separator exactly as mailcheck.py reads it. Editing the mail means
editing that file and rebuilding, never editing the JSON.

Needs SUPABASE_URL and SUPABASE_SERVICE_KEY. Neither this repository's
checkout nor a Claude web session has them (that session's egress policy
refuses supabase.co outright), so this runs where the night run runs.
"""
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRAFT = os.path.join(ROOT, "drafts", "waitlist-app-live.md")
OUT = os.path.join(ROOT, "drafts", "batches", "waitlist-app-live.json")

# The commit that put the Android-only form live. Anything at or after this
# moment saw a promise about Android and is not ours to mail here.
CUTOFF = "2026-09-03T14:16:33Z"

# The batch that already carried the launch to 258 correspondents, 3 to 8
# September. Anybody on it has heard.
LAUNCH_BATCH = "010-app-launch"

# Hidde, 2026-09-10: "ignore myrthe and eric - family and the last one is for
# android". The third is already outside the cutoff.
SKIP = {
    "myrthe@koos.agency": "his own agency, not a stranger who signed up",
    "ep.burgmans@casema.nl": "family",
}

SENT_PATH = os.path.join(ROOT, "data", "outreach-sent.json")


def draft():
    """Subject from the notes, body from below the --- separator."""
    text = open(DRAFT, encoding="utf-8").read()
    parts = re.split(r"^---\s*$", text, maxsplit=1, flags=re.M)
    if len(parts) != 2:
        sys.exit(f"{DRAFT} has no --- separator, so there is no body to send.")
    head, body = parts[0], parts[1].strip()
    m = re.search(r"^Subject:\s*(.+)$", head, flags=re.M)
    if not m:
        sys.exit(f"{DRAFT} names no Subject.")
    return m.group(1).strip(), body


def history():
    """Who has been mailed at all, and who already had the launch news."""
    try:
        log = json.load(open(SENT_PATH, encoding="utf-8"))
    except Exception:
        return set(), set(), set()
    mailed, launched = set(), set()
    for row in log.get("sent", []):
        addr = row.get("to", "").lower()
        mailed.add(addr)
        if str(row.get("batch", "")).startswith(LAUNCH_BATCH):
            launched.add(addr)
    dnc = {a.lower().strip() for a in log.get("do_not_contact", [])}
    return mailed, launched, dnc


def rows(url, key):
    req = urllib.request.Request(
        f"{url.rstrip('/')}/rest/v1/waitlist"
        f"?select=email,created_at,source&created_at=lt.{CUTOFF}"
        "&order=created_at.asc",
        headers={"apikey": key, "Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def source_rows(url, key):
    """Supabase, or a pasted export where supabase.co is unreachable."""
    if "--from-file" in sys.argv:
        path = sys.argv[sys.argv.index("--from-file") + 1]
        return json.load(open(path, encoding="utf-8"))
    return rows(url, key)


def main():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if "--from-file" not in sys.argv and not (url and key):
        sys.exit("REFUSED: needs SUPABASE_URL and SUPABASE_SERVICE_KEY, or "
                 "--from-file <export.json>.")
    subject, body = draft()
    mailed, launched, dnc = history()
    seen, mails, dropped = set(), [], []
    for row in source_rows(url, key):
        addr = (row.get("email") or "").strip()
        low = addr.lower()
        when = str(row.get("created_at") or "")[:19].replace(" ", "T")
        if not addr or low in seen:
            continue
        seen.add(low)
        if when >= CUTOFF.rstrip("Z"):
            dropped.append((addr, "after the Android rename"))
            continue
        if low.endswith("@ancienttrees.app"):
            dropped.append((addr, "one of ours, not a person"))
            continue
        if low in dnc:
            dropped.append((addr, "do not contact"))
            continue
        if low in SKIP:
            dropped.append((addr, SKIP[low]))
            continue
        if low in launched:
            dropped.append((addr, f"already had the launch in {LAUNCH_BATCH}"))
            continue
        mail = {"to": addr,
                "outlet": f"waitlist signup, {str(row.get('created_at'))[:10]}"
                          f", via {row.get('source') or 'unknown'}",
                "subject": subject,
                "body": body}
        if low in mailed:
            mail["resend_reason"] = ("They asked on the waitlist to be told when "
                                     "the app was ready; the earlier mail to this "
                                     "address was about something else.")
        mails.append(mail)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({
        "batch": "waitlist-app-live",
        "note": f"The app is out. Waitlist rows created before {CUTOFF}, the "
                f"moment the form started promising an Android app instead. "
                f"Built by scripts/waitlist_batch.py; copy lives in "
                f"drafts/waitlist-app-live.md.",
        "status": "draft",
        "mails": mails,
    }, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{len(mails)} address(es) -> {os.path.relpath(OUT, ROOT)}")
    for m in mails:
        tail = "  [resend]" if m.get("resend_reason") else ""
        print(f"  {m['to']}  ({m['outlet']}){tail}")
    if dropped:
        print(f"\n{len(dropped)} left out:")
        for addr, why in dropped:
            print(f"  {addr}  ({why})")
    print("\nStatus is 'draft'. Hidde reads the text, flips it to "
          "'approved_by_hidde', then outreach_send.py --send will go.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
