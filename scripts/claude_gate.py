#!/usr/bin/env python3
"""Is there work for the Claude window of this knock, or would it only re-check?

Hidde, 2026-10-25, after a day of 26 night-run log entries of which 23 said
"nothing shipped" (own supply paused, so the ladder below rung 4 is empty):
"saving tokens is good tbh if we can", on the condition that nothing a reader
sent waits longer. So the knock keeps its two-hour rhythm and every cheap step
(mail, live-first photos, unlinking, outreach batches, page dates, deploy),
and only the Claude window asks first. It starts when:

  - a reader's work waits: an app photograph in the sighting queue, a
    submission sent since the last knock, or a note on a tree nobody has read
    (rungs 1 and 3, which CLAUDE.md wants handled within hours);
  - or this knock falls in a fixed slot, two hours from 00, 06, 12 or 18
    UTC (two slots until 2026-10-29), for outreach mail and everything else on the ladder (rung 2's
    breakage included: a red deploy waits at most until the next slot, and the
    digest names it the same morning).

    python3 scripts/claude_gate.py      # prints the reasons; exit 0 = start, 1 = skip

Any doubt starts the window: an unreadable queue or database is a reason to
look, never a reason to stay quiet. Revert: delete the gate step in
nightly.yml and every knock starts Claude again, as before 2026-10-25.
"""
import datetime
import json
import os
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Four slots since 2026-10-29 (Hidde, "ok", when own supply opened again
# without the photo rule and the two slots left the runs 280 minutes a week):
# 00, 06, 12 and 18 UTC, each two hours wide.
SLOT_HOURS = {0, 1, 6, 7, 12, 13, 18, 19}
SUPA = "https://caimvxiyrtifilimlkqw.supabase.co"


def sighting_queue():
    try:
        q = json.load(open(os.path.join(ROOT, "data", "sighting-queue.json"), encoding="utf-8"))
        return len(q.get("queue") or [])
    except Exception:
        return None


def fresh_submissions():
    """Submissions sent in the last 150 minutes: one knock interval plus room,
    so every new one meets at least one window. Not "without an outcome": a
    worth-it vote never gets one, and that count never reaches zero
    (submissions-processed.json is not kept either; 58 'unprocessed' on
    2026-10-25). Anything a window leaves open, the next slot picks up."""
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not key:
        return 0
    since = (datetime.datetime.now(datetime.timezone.utc)
             - datetime.timedelta(minutes=150)).strftime("%Y-%m-%dT%H:%M:%S")
    try:
        req = urllib.request.Request(SUPA + "/rest/v1/submissions?select=id,why&created_at=gte." + since,
                                     headers={"apikey": key, "Authorization": "Bearer " + key})
        with urllib.request.urlopen(req, timeout=30) as r:
            rows = json.load(r)
    except Exception:
        return None
    return sum(1 for r in rows if not (r.get("why") or "").startswith("vote undone"))


def unread_notes():
    if not os.environ.get("SUPABASE_SERVICE_KEY"):
        return 0
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "tree_notes.py"), "--waiting"],
                       capture_output=True, text=True)
    try:
        return int(r.stdout.split(":")[1].split()[0])
    except Exception:
        return None


def main():
    reasons = []
    hour = datetime.datetime.now(datetime.timezone.utc).hour
    if hour in SLOT_HOURS:
        reasons.append("fixed slot (%02d UTC)" % hour)
    for label, n in (("app photograph(s) in the queue", sighting_queue()),
                     ("submission(s) sent since the last knock", fresh_submissions()),
                     ("unread note(s) on trees", unread_notes())):
        if n is None:
            reasons.append("could not read %s, so looking" % label.split("(s)")[0].strip())
        elif n:
            reasons.append("%d %s" % (n, label))
    if reasons:
        print("claude gate: start (%s)" % "; ".join(reasons))
        return 0
    print("claude gate: skip, no reader work waiting and outside the 00, 06, 12 and 18 UTC slots")
    return 1


if __name__ == "__main__":
    sys.exit(main())
