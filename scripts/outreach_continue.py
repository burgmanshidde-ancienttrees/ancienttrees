#!/usr/bin/env python3
"""Continue any outreach batch Hidde has already approved, one day at a time.

Why this exists (2026-09-04): batch-010-app-launch holds 212 addresses and
the daily cap is 50, so finishing it takes five days. The first two mornings
were run by hand in session, and the second re-sent the first morning's 46
because the batch had no memory of itself (fixed in outreach_send.py the
same day). Hidde then said "1 you can do", meaning finish the batch, and the
honest mechanism is not a person remembering to run a command for four
mornings but the night run, which already carries the mail credentials for
contributor replies.

What it does, and the whole of what it does:
- finds every batch file whose status is "approved_by_hidde": nothing that
  awaits his word is ever touched, so a newly drafted batch stays a draft;
- runs scripts/outreach_send.py --send on each, which keeps every guard it
  has (daily cap, do-not-contact, never twice within a batch, never from a
  personal address);
- when a batch reports nothing SENT and nothing HELD, every address has been
  reached, and the status flips to "sent_complete" so the next knock does
  not open it again.

Absent credentials it is a printed dry run and exits 0, like the contributor
step. It never edits mail text and never adds an address.

It only CONTINUES (2026-10-14): a batch nobody has sent from yet is opened
here only when it carries `approved_word`, Hidde's own words and the date.
That morning a session flipped the press batch to approved_by_hidde to get
past a dry run before he had read the texts, rewrote the texts after his
correction, and this script sent the old version at the next knock. The
status alone is something a session can set; his quoted word is the record
that he read it.
"""
import glob
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEND = os.path.join(ROOT, "scripts", "outreach_send.py")


def started(name):
    """True when outreach_send.py already sent at least one mail of this batch."""
    try:
        sent = json.load(open(os.path.join(ROOT, "data", "outreach-sent.json")))["sent"]
    except (OSError, ValueError, KeyError):
        return False
    return any(s.get("batch") == name for s in sent)


def main():
    really = "--send" in sys.argv
    touched = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "drafts", "batches", "*.json"))):
        try:
            batch = json.load(open(path))
        except Exception as e:
            print(f"skip {os.path.basename(path)}: unreadable ({e})")
            continue
        if batch.get("status") != "approved_by_hidde":
            continue
        if not batch.get("approved_word") and not started(batch.get("batch", "")):
            print(f"skip {os.path.basename(path)}: approved but never started and no "
                  f"approved_word; the first send happens in session, after he read it")
            continue
        touched += 1
        args = [sys.executable, SEND, path] + (["--send"] if really else [])
        print(f"== {os.path.basename(path)} ({len(batch.get('mails', []))} mails)")
        out = subprocess.run(args, capture_output=True, text=True)
        sys.stdout.write(out.stdout)
        if out.returncode != 0:
            print(f"   outreach_send.py exited {out.returncode}; batch left as is")
            sys.stderr.write(out.stderr)
            continue
        lines = out.stdout.splitlines()
        sent = sum(1 for l in lines if l.startswith("SENT"))
        held = sum(1 for l in lines if l.lstrip().startswith("HOLD"))
        print(f"   sent {sent}, held for tomorrow {held}")
        if really and sent == 0 and held == 0:
            batch["status"] = "sent_complete"
            json.dump(batch, open(path, "w"), indent=1, ensure_ascii=False)
            print(f"   every address reached; status -> sent_complete")
    if touched == 0:
        print("no approved batch waiting")
    return 0


if __name__ == "__main__":
    sys.exit(main())
