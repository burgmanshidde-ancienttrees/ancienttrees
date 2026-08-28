#!/usr/bin/env python3
"""Is anything at rung 2? One command, because rung 2 runs every single time.

    python3 scripts/health.py

Rung 2 of Step 0 is "the site is broken, fix it before adding anything new", and
it is the step every run executes. Doing it by hand means four `gh run list`
calls, three different staleness thresholds held in your head (8 days for the
weekly analysis, 26 hours for the digest and the fresh-eyes review, latest-must-
be-green for the smoke test), and reading REVIEW.md for a BLOCKER. Written out
2026-08-17 while walking the ladder by hand: every one of those is a lookup a
script can do, and a check that takes four commands and mental arithmetic is a
check that gets skipped on a short window.

Exit code is the answer: 0 nothing at rung 2, 1 something is. Prints what and
what to do about it. Degrades to a printed line rather than an exception when
`gh` is missing or unauthenticated, because this must never be the thing that
stops a run from working.
"""

import datetime
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# workflow file -> (label, max age, what to do when it is stale)
WATCHED = {
    "smoke.yml": ("Smoke test", None, None),
    "deploy.yml": ("Build and deploy", None, None),
    # THE APP, watched from 2026-08-25. It had a full CI gate since 08-20 that
    # builds it, runs seventeen tests and measures every screen's layout, and
    # nothing on this list read the verdict, so it sat RED from 08-24 to 08-25
    # through five pushes while Hidde found the same bugs on his own telephone
    # and asked "kunnen we de app dezelfde kwaliteit qa of ci testen als de
    # website geven, er gaat veel fout volgens mij". The gate was not the
    # missing piece. Somebody looking at it was.
    "ios.yml": ("iOS app", None, None),
    "data-digest.yml": ("Data digest", datetime.timedelta(hours=26),
                        "gh workflow run data-digest.yml"),
    "review.yml": ("Fresh-eyes review", datetime.timedelta(hours=26),
                   "gh workflow run review.yml"),
    "weekly-analysis.yml": ("Weekly analysis", datetime.timedelta(days=8),
                            "gh workflow run weekly-analysis.yml"),
}


def gh_latest(workflow):
    """(conclusion, created_at) of the newest run, or None when gh cannot say."""
    try:
        # Five, not one, and then take the newest COMPLETED run. A run that is
        # still going reports conclusion "", which the caller compared against
        # None and therefore read as a failure: on 2026-08-17 this told a night
        # run "Smoke test is  (its newest run, 0h ago). The site may be broken"
        # while the site was fine and the deploy was simply mid-flight. The
        # question this function answers is "did the last finished check pass",
        # and an unfinished run has not answered it either way.
        out = subprocess.run(
            ["gh", "run", "list", "--workflow", workflow, "-L", "5",
             "--json", "conclusion,createdAt,status"],
            capture_output=True, text=True, timeout=60, cwd=ROOT)
        if out.returncode != 0:
            return None
        rows = json.loads(out.stdout or "[]")
        done = [r for r in rows if r.get("status") == "completed"
                and r.get("conclusion")]
        if not done:
            return None
        created = done[0].get("createdAt", "")
        when = datetime.datetime.fromisoformat(created.replace("Z", "+00:00"))
        return done[0].get("conclusion"), when
    except Exception:
        return None


# A workflow that RUNS CLAUDE fails in two completely different ways, and they
# want opposite responses. Broken means read the log. Out of allowance means do
# nothing at all and wait for the window; CLAUDE.md's capacity doctrine already
# says "attempts that hit the usage limit die in seconds and cost nothing".
# Told apart by how long the run lasted: a real failure takes minutes, an
# exhausted allowance dies on its first request in well under two.
#
# Written 2026-08-26 after this told a session the site might be broken for
# twenty-plus red runs, and the session spent its window diagnosing a stale
# credential before Hidde said his account was simply out of tokens.
CLAUDE_WORKFLOWS = {"nightly.yml", "review.yml", "weekly-analysis.yml"}
STARVED_SECONDS = 120


def looks_starved(workflow):
    """True when the newest failed runs died too fast to have done anything."""
    try:
        out = subprocess.run(
            ["gh", "run", "list", "--workflow", workflow, "-L", "5",
             "--json", "conclusion,status,startedAt,updatedAt"],
            capture_output=True, text=True, timeout=60, cwd=ROOT)
        if out.returncode != 0:
            return False
        fast = 0
        for r in json.loads(out.stdout or "[]"):
            if r.get("status") != "completed" or r.get("conclusion") != "failure":
                continue
            try:
                a = datetime.datetime.fromisoformat(
                    r["startedAt"].replace("Z", "+00:00"))
                b = datetime.datetime.fromisoformat(
                    r["updatedAt"].replace("Z", "+00:00"))
            except Exception:
                return False
            if (b - a).total_seconds() > STARVED_SECONDS:
                return False
            fast += 1
        return fast >= 2
    except Exception:
        return False


# The starvation check above only sees workflows that FAIL. A night run that
# hits the usage limit ends with conclusion "success" after 0.0 minutes and one
# turn, so twenty of them in a row (2026-08-24 to 08-26) looked in LOG.md like
# "nothing new pushed" while the truth was "the engine has been off for two
# days". This reads the runs' own health ledger and says so.
RUN_HEALTH = os.path.join(ROOT, "data", "run-health.json")
IDLE_STREAK_FLOOR = 4  # four dead in a row is a third of a day, whatever the knock count


def night_shift_idle():
    """(streak, since) of newest consecutive runs that died in seconds."""
    try:
        doc = json.load(open(RUN_HEALTH))
    except (OSError, ValueError):
        return 0, None
    runs = doc if isinstance(doc, list) else doc.get("runs", [])
    streak, since = 0, None
    for r in reversed(runs):
        try:
            idle = (float(r.get("minutes") or 0) < 0.5
                    and int(r.get("turns") or 0) <= 2
                    and int(r.get("commits") or 0) == 0)
        except (TypeError, ValueError):
            break
        if not idle:
            break
        streak += 1
        since = r.get("started") or r.get("date") or ""
    return streak, since


# And the failure mode that is the exact opposite, invisible to everything
# above: a knock that never ARRIVES. run-health.json only records runs that
# happened, so nine scheduled knocks delivering two looks identical to a quiet
# night. Measured 2026-08-27 and 08-28: 2 of 9 both days, while the two that did
# fire used their full window and worked fine. The digest's own watchdog cannot
# see it either, because it waits for 26 hours of TOTAL silence and 2-of-9 never
# produces a gap that long.
KNOCKS_A_DAY = 12  # nightly.yml, every two hours round the clock since 2026-08-28
KNOCK_FLOOR = 7  # under this in 24h is a delivery problem, not a quiet night


def knocks_fired():
    """How many nightly.yml runs GitHub actually started in the last 24h."""
    try:
        out = subprocess.run(
            ["gh", "api", "repos/{owner}/{repo}/actions/workflows/nightly.yml/runs",
             "-q", ".workflow_runs[].created_at"],
            capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=24)
    n = 0
    for line in out.stdout.split():
        try:
            when = datetime.datetime.fromisoformat(line.strip().replace("Z", "+00:00"))
        except ValueError:
            continue
        if when > cutoff:
            n += 1
    return n


ANSWERED = os.path.join(ROOT, "data", "review-answered.json")


def answered():
    """BLOCKERs a run has already dealt with, so the ladder stops re-serving them.

    REVIEW.md is the reviewer's file and it is append-only: fixing a finding does
    not retract it, and the next review is 24 hours away. Without this ledger the
    rung-2 check reports the same BLOCKER to every knock in between, so with six
    knocks a day a run could re-litigate a finding five times after it was fixed.
    Recorded per review date with a note, by `health.py --answer <date> "<note>"`.
    """
    try:
        return json.load(open(ANSWERED))
    except OSError:
        return {"note": "BLOCKERs from REVIEW.md that a run has answered, keyed by "
                        "the review date. health.py stops reporting these.",
                "answered": {}}
    except ValueError:
        return {"answered": {}}


def record_answer(date, note):
    doc = answered()
    doc.setdefault("answered", {})[date] = {
        "note": note,
        "at": datetime.datetime.now(datetime.timezone.utc).replace(
            microsecond=0).isoformat(),
    }
    with open(ANSWERED, "w") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
    print(f"recorded: the {date} BLOCKER is answered. {note}")


def newest_review_block():
    """The most recent dated section of REVIEW.md, as text."""
    path = os.path.join(ROOT, "REVIEW.md")
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return "", ""
    parts = re.split(r"^## (\d{4}-\d{2}-\d{2})\s*$", text, flags=re.M)
    # parts = [preamble, date, body, date, body, ...]; newest first in the file
    if len(parts) < 3:
        return "", ""
    return parts[1], parts[2]


def main():
    if "--answer" in sys.argv:
        i = sys.argv.index("--answer")
        rest = sys.argv[i + 1:]
        if len(rest) < 2:
            print('usage: health.py --answer <YYYY-MM-DD> "<what was done>"')
            return 2
        record_answer(rest[0], " ".join(rest[1:]))
        return 0
    now = datetime.datetime.now(datetime.timezone.utc)
    problems = []
    unknown = []
    notes = []

    for wf, (label, max_age, remedy) in WATCHED.items():
        got = gh_latest(wf)
        if got is None:
            unknown.append(label)
            continue
        conclusion, when = got
        age = now - when
        hours = age.total_seconds() / 3600
        if conclusion not in ("success", None) and conclusion != "cancelled":
            # The app is not the site, and a run told to read a failing log
            # should be told which thing is broken. `gh run view --log-failed`
            # on the newest ios.yml run prints the failed assertions; the
            # xcresult artifact carries the screenshot XCTest took at each one.
            starved = wf in CLAUDE_WORKFLOWS and looks_starved(wf)
            if starved:
                # Not a problem to fix, so it does not join `problems` and does
                # not fail the exit code. There is nothing to do but wait.
                notes.append(f"{label} is failing, but its runs die in under "
                             f"{STARVED_SECONDS}s having done nothing: that is the "
                             f"usage allowance, not breakage. Do NOT regenerate "
                             f"CLAUDE_CODE_OAUTH_TOKEN. It resumes when the window "
                             f"resets, and if it is still failing a full window "
                             f"later, then it is not the allowance and the log is "
                             f"worth reading after all.")
            else:
                what = ("The APP is broken, not the site; the failed assertions are "
                        "in the log and the screenshots are in its xcresult artifact"
                        if wf == "ios.yml"
                        else "The site may be broken; read the failing log before "
                             "anything else")
                problems.append(f"{label} is {conclusion} (its newest run, "
                                f"{hours:.0f}h ago). {what}.")
        if max_age and age > max_age:
            problems.append(f"{label} has not run in {hours:.0f}h "
                            f"(threshold {max_age.total_seconds()/3600:.0f}h). "
                            f"GitHub drops schedules silently: {remedy}")
        state = conclusion or "in progress"
        print(f"  {label:20s} {state:10s} {hours:5.1f}h ago")

    streak, since = night_shift_idle()
    if streak >= IDLE_STREAK_FLOOR:
        when = (since or "")[:16].replace("T", " ")
        notes.append(f"The night shift has been idle: the newest {streak} runs "
                     f"(since {when} UTC) each died in seconds with nothing "
                     f"done. That is almost certainly the usage window, not "
                     f"breakage; runs end 'success' so nothing else reports it. "
                     f"Nothing to fix. If a run still does 0.0 minutes after "
                     f"the window has reset, then it is not the allowance and "
                     f"its log is worth reading.")

    fired = knocks_fired()
    if fired is None:
        unknown.append("nightly knocks")
    else:
        print(f"  {'Nightly knocks':20s} {fired} of {KNOCKS_A_DAY} in 24h")
        if fired < KNOCK_FLOOR:
            problems.append(
                f"Only {fired} of {KNOCKS_A_DAY} nightly knocks were delivered in the "
                f"last 24h. That is GitHub dropping the cron, not the usage window: "
                f"a starved run still appears in this count. Dispatch one by hand: "
                f"gh workflow run nightly.yml")

    date, body = newest_review_block()
    if date:
        # Match the reviewer's own heading form, "**BLOCKER — ...", not any line
        # mentioning the word. The first version of this check counted the file's
        # own legend and a sentence about YESTERDAY's blocker being fixed, and
        # reported three where there was one. A check that cries wolf is a check
        # that gets ignored, which is worse than not having it.
        def headings(word):
            return [ln for ln in body.splitlines()
                    if re.match(r"\s*\*\*" + word + r"\b", ln)]
        blockers, warns = headings("BLOCKER"), headings("WARN")
        print(f"  {'REVIEW.md':20s} {date:10s} "
              f"{len(blockers)} BLOCKER, {len(warns)} WARN")
        already = answered().get("answered", {}).get(date)
        if blockers and already:
            print(f"  {'':20s} {'':10s} its BLOCKER is recorded as answered: "
                  f"{already.get('note','')[:70]}")
        if blockers and not already:
            problems.append(f"REVIEW.md {date} carries a BLOCKER. Runs treat it as rung 2, "
                            "so it outranks new coverage. First line: "
                            + blockers[0].strip()[:160])
    else:
        unknown.append("REVIEW.md")

    if unknown:
        print(f"\n  could not check: {', '.join(unknown)} "
              "(gh missing, unauthenticated, or the file is absent)")

    if notes:
        print("\n  nothing to do about these:\n")
        for n in notes:
            print(f"  - {n}")

    if problems:
        print(f"\nRUNG 2: {len(problems)} thing(s) to deal with before new coverage\n")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("\nRUNG 2 clear: nothing broken, nothing stale, no BLOCKER. "
          "Move down the ladder.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
