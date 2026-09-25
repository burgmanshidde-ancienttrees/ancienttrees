#!/usr/bin/env python3
"""What a night run actually did, written by the workflow rather than by the run.

    python3 scripts/run_health.py --execution-file <path> --since-sha <sha>

Why this exists. On 2026-08-15 four night runs in a row ended after nine minutes
of a sixty minute window, with `is_error: false` and `subtype: success`, having
published nothing and having written not one line to LOG.md. From the repository
they were indistinguishable from runs that never fired. The prompt already tells
a run to log even when it shipped nothing, and a run that gives up is exactly the
run that skips that instruction, so the instruction cannot be the mechanism.

So the workflow measures the run instead of asking it to measure itself:

  data/run-health.json  one record per run, always, so the pattern is visible
                        across nights instead of having to be dug out of
                        `gh run view --log` one run at a time.
  LOG.md                a stub entry, ONLY when the run wrote none, so that a
                        silent run is loud in the one file Hidde reads cold.

The numbers come from the SDK's own result record, which is the only part of the
run this repository can see: the transcript is hidden on purpose (the repo is
public and reader submissions pass through these runs). Turns, minutes, and the
count of commands the allowlist refused. That last one is why this was worth
building: every run refuses between 4 and 25 commands and nobody knew.

Deliberately not recorded: the dollar figure the SDK reports. Usage here is
counted in tokens against a subscription, never in money.
"""

import argparse
import datetime
import json
import re
from pathlib import Path
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEALTH = os.path.join(ROOT, "data", "run-health.json")
LOG = os.path.join(ROOT, "LOG.md")
INFLIGHT = os.path.join(ROOT, "data", "in-flight.json")


def git(*args):
    """Run a git command in the repo, returning stdout or '' when it fails.

    Never raises: this whole script runs after the work is done and must not be
    able to fail a job that already produced something."""
    try:
        out = subprocess.run(["git", "-C", ROOT] + list(args),
                             capture_output=True, text=True, timeout=60)
        return out.stdout.strip() if out.returncode == 0 else ""
    except Exception:
        return ""


def read_result(path):
    """The SDK result record: {duration_ms, num_turns, permission_denials_count...}.

    The action writes a JSON array of stream messages; older versions wrote one
    JSON object per line. Accept both, and accept a bare result object, because a
    format change here must degrade to 'unknown' rather than to a crash."""
    if not path or not os.path.exists(path):
        return {}
    try:
        raw = open(path, errors="replace").read().strip()
    except Exception:
        return {}
    records = []
    try:
        doc = json.loads(raw)
        records = doc if isinstance(doc, list) else [doc]
    except Exception:
        for line in raw.split("\n"):
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                records.append(json.loads(line))
            except Exception:
                continue
    for rec in reversed(records):
        if isinstance(rec, dict) and rec.get("type") == "result":
            return rec
    return {}


# What a stopping attempt says is the one thing the stub could never tell: WHY.
# The console hides the transcript (public repo), but the execution file holds
# the agent's own closing message, which is written for a reader anyway. Found
# 2026-09-25: three windows in a row ended "without saying anything" after four
# attempts each, every one of them subtype success, and nothing on disk said
# why any of the twelve attempts decided it was done.
_SECRETISH = [
    re.compile(r"https?://[^\s/@]+@"),                  # credentials in a url
    re.compile(r"\beyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-.]+"),  # a JWT
    re.compile(r"\b(?:gh[pousr]_|sk-|xox[abp]-)[A-Za-z0-9_\-]+"),
    re.compile(r"[A-Za-z0-9+/_\-]{40,}={0,2}"),          # any long opaque token
]
CLOSING_CHARS = 700


def closing_words(path):
    """The attempt's last words to whoever reads the log, secrets scrubbed.

    Prefers the result record's own text; falls back to the last assistant
    message with text in it. Empty when there is nothing readable."""
    if not path or not os.path.exists(path):
        return ""
    try:
        doc = json.loads(open(path, errors="replace").read())
    except Exception:
        return ""
    records = doc if isinstance(doc, list) else [doc]
    text = ""
    for rec in reversed(records):
        if isinstance(rec, dict) and rec.get("type") == "result" and isinstance(rec.get("result"), str):
            text = rec["result"]
            break
    if not text.strip():
        for rec in reversed(records):
            if not isinstance(rec, dict) or rec.get("type") != "assistant":
                continue
            content = (rec.get("message") or {}).get("content") or []
            parts = [c.get("text", "") for c in content
                     if isinstance(c, dict) and c.get("type") == "text"]
            if any(p.strip() for p in parts):
                text = "\n".join(parts)
                break
    for pat in _SECRETISH:
        text = pat.sub("[redacted]", text)
    text = " ".join(text.split())
    if len(text) > CLOSING_CHARS:
        text = text[:CLOSING_CHARS].rsplit(" ", 1)[0] + " ..."
    return text


DENIAL_KEYS = ("permission_denials_count", "permission_denials",
               "num_permission_denials", "denied_tool_uses",
               "tool_permission_denials", "blocked_tool_uses")


# A bare command name: letters, digits, dash, underscore, dot. Anything that
# does not match is reported as "?" rather than truncated, because a guess at
# where an argument starts is how a path leaks.
_BARE_NAME = re.compile(r"[A-Za-z0-9._-]{1,20}")
# The operators that chain one command to the next. Captured, not discarded:
# which operator joined two segments is half of what makes a shape readable.
_CHAIN = re.compile(r"(&&|\|\||;|\||\n)")
# How many segments a label carries before it gives up and says "more". Four is
# enough to see the shape and short enough to read in a table.
_MAX_SEGMENTS = 4


def _segment_head(segment):
    """The command name at the head of one segment, and whether it opened a
    subshell. Redaction-safe: only a bare command name is ever returned."""
    s = segment.strip()
    opened = False
    # A parenthesised subshell is the shape that silently stopped every night
    # run for a day in August, so it is worth naming rather than stripping.
    while s[:1] in ("(", "{", "!"):
        opened = opened or s[0] == "("
        s = s[1:].lstrip()
    words = s.split()
    # FOO=bar cmd: the assignment is not the command, and it can carry a value.
    while words and "=" in words[0] and not words[0].startswith("="):
        words.pop(0)
    if not words:
        return None, opened
    first = words[0]
    return (first if _BARE_NAME.fullmatch(first) else "?"), opened


def command_shape(cmd):
    """The SHAPE of a shell command: the head word of every segment, joined by
    the operators that chained them, and nothing else.

    Why the shape rather than the first word. Until 2026-09-19 this recorded the
    first word alone, on the reasoning that the allowlist is a list of binaries
    so the binary is the whole question. That reasoning was wrong in a way the
    record itself could not show: the allowlist matches the WHOLE command
    string, so `python3 x.py && git commit` is refused although `python3` and
    `git` are both on the list, and it was logged as `Bash(python3)`. For a
    month the record named the one word that was never the problem. Measured
    over the last 60 runs, `Bash(python3)` was the most-refused label on the
    board, appearing in 43 of them, while `Bash(python3:*)` sat on the
    allowlist the whole time.

    That is also why the 2026-08-20 widening bought nothing: binaries were added
    from first words that were already allowed. Guessing which to add has now
    been tried twice, so what changes again is the record, this time at the
    level the matcher actually works on.

    The privacy rule is unchanged and is what bounds this: only bare command
    names ever leave here, one per segment, never an argument. `python3 x.py |
    head -5` becomes `python3 | head`, and a path, a URL or a reader's
    submission cannot survive that.
    """
    if not cmd or not cmd.strip():
        return None
    parts = _CHAIN.split(cmd)
    out, subshell, truncated = [], False, False
    for i, part in enumerate(parts):
        if i % 2:                                   # an operator
            if len(out) >= _MAX_SEGMENTS * 2 - 1:
                truncated = True
                continue
            out.append("&&" if part == "&&" else
                       "||" if part == "||" else
                       "|" if part == "|" else ";")
            continue
        head, opened = _segment_head(part)
        subshell = subshell or opened
        if head is None:
            # An empty segment: a trailing operator, or a split inside quotes.
            if out and out[-1] in ("&&", "||", "|", ";"):
                out.pop()
            continue
        if len([x for x in out if x not in ("&&", "||", "|", ";")]) >= _MAX_SEGMENTS:
            truncated = True
            continue
        out.append(head)
    while out and out[-1] in ("&&", "||", "|", ";"):
        out.pop()
    while out and out[0] in ("&&", "||", "|", ";"):
        out.pop(0)
    if not out:
        return None
    shape = " ".join(out)
    if truncated:
        shape += " ..."
    if subshell:
        shape = "subshell " + shape
    return shape


def _denial_label(d):
    """What was refused, in the smallest form that is still useful.

    The first version recorded the TOOL name only, on the reasoning that a
    denied command can carry a URL or a path from a reader submission and this
    file is public. The reasoning is right and the result was useless: every
    night reported "Bash" and nothing else, so 123 refusals across six runs told
    us the wall was made of shell and never which wall. The second version took
    the first word, which named a wall that was not there; see command_shape.
    """
    tool = str(d.get("tool_name") or d.get("tool") or d.get("name") or "?")[:24]
    inp = d.get("tool_input") or d.get("input") or {}
    cmd = inp.get("command") if isinstance(inp, dict) else None
    if tool == "Bash" and isinstance(cmd, str):
        shape = command_shape(cmd)
        if shape:
            return "Bash(%s)" % shape
    return tool


def denials_from(result):
    """How many commands the allowlist refused, and never a silent zero.

    Returns (count, source_key). The count read 4 to 25 on every run until
    2026-08-15 and has been null on every run since, because the SDK key this
    read went away in a version bump. A null recorded as if it were a fact is
    the same class of fault as the truncated Search Console readback and the
    dead sendBeacon: an instrument that reads zero while nothing about the zero
    looks broken. So try every name the field has plausibly taken, and when
    none of them is present return the key list instead, which turns the next
    run's record into the answer rather than another shrug.
    """
    if not isinstance(result, dict):
        return None, "no result record"
    for key in DENIAL_KEYS:
        v = result.get(key)
        if isinstance(v, (int, float)):
            return int(v), key
        if isinstance(v, list):
            # The list carries WHAT was refused, which is the whole point: a
            # count told us runs hit a wall between 4 and 25 times a night and
            # never which wall. Confirmed 2026-08-17, the first night after the
            # key search shipped: the field is `permission_denials`, a list,
            # and the run that recorded 6 of them produced nothing in 7.8
            # minutes. Names only, truncated, never arguments: a denied command
            # can carry a URL or a path from a reader submission, and this file
            # is public.
            return len(v), "%s: %s" % (key, ", ".join(sorted(
                {_denial_label(d) for d in v if isinstance(d, dict)}))
                or "no names in the record")
    # Nested one level, which is where SDKs usually move a counter to.
    for holder in ("permissions", "stats", "metrics", "usage"):
        sub = result.get(holder)
        if isinstance(sub, dict):
            for key in DENIAL_KEYS + ("denials", "denied", "refused"):
                v = sub.get(key)
                if isinstance(v, (int, float)):
                    return int(v), f"{holder}.{key}"
    return None, "NOT FOUND; result keys were: " + ",".join(sorted(result)[:24])


def tokens_from(result):
    """Total tokens, when the result carries a usage block. None when it does not."""
    usage = result.get("usage")
    if not isinstance(usage, dict):
        return None
    total = 0
    for key in ("input_tokens", "output_tokens",
                "cache_creation_input_tokens", "cache_read_input_tokens"):
        value = usage.get(key)
        if isinstance(value, (int, float)):
            total += int(value)
    return total or None


def trees_in(path, sha=None):
    """Tree count in one city file, at HEAD or at a given commit."""
    if sha:
        raw = git("show", f"{sha}:{path}")
        if not raw:
            return 0
    else:
        try:
            raw = open(os.path.join(ROOT, path), errors="replace").read()
        except Exception:
            return 0
    try:
        return len(json.loads(raw).get("trees", []))
    except Exception:
        return 0


def what_changed(since_sha):
    """Commits, city files touched and net trees published since the run started.

    Returns None when the range cannot be resolved (a force-push, a missing sha),
    because a wrong 'nothing shipped' is worse than an honest 'unknown'."""
    if not since_sha:
        return None
    check = subprocess.run(["git", "-C", ROOT, "merge-base", "--is-ancestor",
                            since_sha, "HEAD"], capture_output=True)
    if check.returncode != 0:
        return None
    rng = f"{since_sha}..HEAD"
    commits = [c for c in git("log", "--pretty=%s", rng).split("\n") if c]
    files = [f for f in git("diff", "--name-only", rng).split("\n") if f]
    cities = [f for f in files if f.startswith("data/cities/") and f.endswith(".json")]
    delta = 0
    # Hidde, 2026-08-24: "kun je ook altijd vertellen welke steden de nachtruns
    # hebben gedaan." The count alone ("3 city files") was answering how many
    # and never which, so the digest could not say a city had opened without
    # somebody reading the git log by hand. Names cost nothing here: the file
    # paths are already in front of us. Recorded per city with its own tree
    # delta, so a run that added four to Utrecht reads differently from one
    # that touched four cities for one tree each.
    by_city = []
    for path in cities:
        d = trees_in(path) - trees_in(path, since_sha)
        delta += d
        by_city.append({"city": path.split("/")[-1][:-5], "trees": d})
    by_city.sort(key=lambda c: (-c["trees"], c["city"]))
    return {
        "commits": len(commits),
        "cities_touched": len(cities),
        "cities": by_city,
        "trees": delta,
        "logged": "LOG.md" in files,
    }


def claims_held(by):
    """Claims this holder still has open, so claim-and-die shows up in the record."""
    try:
        doc = json.load(open(INFLIGHT))
    except Exception:
        return []
    return [c.get("target", "?") for c in doc.get("claims", [])
            if c.get("by") == by]


def release_claims(by):
    """Drop every claim this holder still has, because the run is over.

    Added 2026-08-16, from the night's own numbers. A claim exists so two
    passes do not work the same city; it has no job once the run holding it
    has ended. But nothing released them, so a run that claimed and quit left
    the lock standing for its full 90-minute life, and passcheck refuses to
    print a brief for a claimed place. With cron knocking about every 90
    minutes that is a rolling lockout: the 22:49 run claimed Bucaco and
    Cordoba at 22:54 and ended at 23:01 without writing either, and the runs
    behind it inherited a queue with its cheapest work fenced off. By 05:55
    one run was looking at five cities locked by dead predecessors.

    This step already runs `if: always()`, so it fires on success, error and
    the 60-minute timeout alike, which is exactly the set of cases where the
    holder is definitively gone. Sessions are untouched: only claims whose
    `by` matches this run's holder are released.
    """
    try:
        doc = json.load(open(INFLIGHT))
    except Exception:
        return []
    claims = doc.get("claims", [])
    mine = [c.get("target", "?") for c in claims if c.get("by") == by]
    if not mine:
        return []
    doc["claims"] = [c for c in claims if c.get("by") != by]
    with open(INFLIGHT, "w") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
    return mine


def append_health(record):
    try:
        doc = json.load(open(HEALTH))
        runs = doc.get("runs", []) if isinstance(doc, dict) else list(doc)
    except Exception:
        doc, runs = {}, []
    runs.append(record)
    # Rebuild note and runs, KEEP everything else. This used to assign a fresh
    # two-key dict, which silently deleted any other key on the first night run
    # after it was written: a `schedule_changes` block recording the 2026-08-16
    # baseline (8 runs, 87.3 minutes, 28 trees) was destroyed within hours of
    # being added, and it existed precisely so the next morning could measure
    # whether the schedule change helped. A file that eats the context someone
    # deliberately stored in it is worse than one that never accepted it.
    if not isinstance(doc, dict):
        doc = {}
    doc["note"] = (
        "One record per night run, written by the workflow's own Run health "
        "step, never by the run. A run cannot leave this empty by giving up, "
        "which is the entire point: on 2026-08-15 four runs ended after nine "
        "minutes of a sixty minute window and left no trace at all. "
        "'denials' counts commands the allowlist refused; it read 4 to 25 "
        "until 2026-08-15 and has returned null since, because the SDK key "
        "it reads went away. Treat a null as a broken instrument, not a zero.")
    doc["runs"] = runs[-400:]
    with open(HEALTH, "w") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def window_minutes(default=90):
    """The run's cap, read from the workflow rather than remembered.

    This line said "of its 60 minute window" for every run logged after the cap
    became 90, which is a number Hidde reads in LOG.md to judge whether the
    schedule is working. A hardcoded constant describing a value that lives in
    another file goes stale silently, exactly like the workflow prompt that kept
    declaring a superseded phase.
    """
    try:
        wf = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "nightly.yml"
        m = re.search(r"^\s*timeout-minutes:\s*(\d+)", wf.read_text(encoding="utf-8"), re.M)
        return int(m.group(1)) if m else default
    except OSError:
        return default

def stub_entry(record):
    """The LOG.md line a silent run did not write."""
    started = record.get("started", "")[:16].replace("T", " ")
    bits = []
    if record.get("minutes") is not None:
        window = window_minutes()
        line = f"{record['minutes']} minutes of its {window} minute window"
        if str(record.get("minutes_basis", "")).startswith("wall clock"):
            line += " (wall clock: cancelled before it could report its own duration)"
        bits.append(line)
    if record.get("turns") is not None:
        bits.append(f"{record['turns']} turns")
    if record.get("denials"):
        bits.append(f"{record['denials']} commands refused by the allowlist")
    shape = ", ".join(bits) if bits else "no measurements available"

    produced = "Nothing reached data/cities."
    if record.get("trees"):
        produced = (f"{record['trees']} tree(s) reached data/cities across "
                    f"{record.get('cities_touched', 0)} city file(s), and the run "
                    "still wrote no log entry of its own.")
    elif record.get("commits"):
        produced = (f"{record['commits']} commit(s), none of them a published "
                    "tree.")

    left = ""
    if record.get("claims_held"):
        left = (" Claims left behind: " + ", ".join(record["claims_held"]) +
                ", which block the top of the queue until they expire.")

    ended = record.get("ended") or "unknown"
    said = [w for w in record.get("closing_words") or [] if w]
    if said:
        why = ("What each attempt said as it stopped, in its own words (secrets "
               "scrubbed):\n\n" + "\n".join(
                   f"- Attempt {i}: {w}" for i, w in
                   enumerate(record["closing_words"], 1) if w) + "\n")
    else:
        why = ("What it cannot tell you is WHY the run stopped: no attempt left "
               "closing words on disk. If this shape repeats, the two things "
               "worth suspecting are the usage window and the refused commands.\n")
    return (
        f"## {record['date']} - Night run {started} UTC ended without saying anything\n"
        "\n"
        f"Written by the workflow's Run health step, not by the run. {shape.capitalize()}, "
        f"ended clean ({ended}). {produced}{left}\n"
        "\n"
        "This entry exists because the run wrote none. The prompt asks every run to "
        "log even when it ships nothing, and a run that gives up is exactly the one "
        "that skips that instruction, so the count above is measured rather than "
        "reported.\n"
        "\n"
        + why
    )


def prepend_log(entry):
    """Put the stub above the newest entry, below the archive index."""
    try:
        lines = open(LOG, errors="replace").read().split("\n")
    except Exception:
        return False
    for i, line in enumerate(lines):
        if line.startswith("## "):
            body = "\n".join(lines[:i]) + "\n" + entry + "\n" + "\n".join(lines[i:])
            open(LOG, "w").write(body)
            return True
    return False


# The window is two hours (timeout-minutes in nightly.yml) and runs keep handing
# it back after five. Measured over the 20 runs from 2026-08-15: the ones that
# shipped nothing ended with is_error false and subtype success after 47 to 122
# turns, having committed a claim and stopped. Nothing killed them. They decided
# they were done.
#
# The prompt has told them otherwise since 2026-08-13 ("do not stop after one
# item ... keep going until the usage limit stops you or the clock runs out"),
# and the workflow already carries a note from 2026-08-15 about four runs in a
# row doing exactly this. Written twice, ignored twice, which is where this
# project stops writing and starts building. Measurement came first and is now
# in; this is the cure.
#
# Rewritten 2026-08-29, because the rule below was switching the continuation
# OFF for exactly the runs that were working. It said: continue only if the
# attempt shipped no trees. So a run that shipped eight trees in 28 minutes was
# told it was fine and the window ended with 92 of its 120 minutes unspent.
#
# Measured over the 66 working runs since 2026-08-15: 6,106 minutes of window
# handed back, 93 per run against a 120-minute cap. The runs that shipped trees
# averaged 41 minutes and 1.26 attempts; the runs that shipped nothing averaged
# 15 minutes and 1.52. Productivity was being punished with an early night.
#
# So the question is no longer "did it ship" but "is there time left". A window
# continues while enough of it remains to be worth a fresh orientation, and it
# stops for the three reasons that are real: the usage limit killed the attempt,
# an error was reported, or the clock is nearly out.
#
# The fourth stop is the WEEK, and it is the reason this is safe. The night of
# 2026-08-23 spent 329 minutes, closing a five-day stretch of 1,053, and then
# every knock for two and a half days died in seconds on the usage limit: three
# days of no machine at all. Handing every run its full window would roughly
# triple the weekly spend, so the budget guard below spends the headroom and
# stops before it buys another blackout. WEEK_BUDGET_MINUTES is the dial; it is
# Hidde's number, because it is his usage window.
PROBE_CAP_MINUTES = 120     # the job's timeout-minutes, the size of one window
PROBE_MIN_REMAINING = 25    # below this a fresh attempt cannot pay its orientation cost
PROBE_MIN_TURNS = 5         # below this it never really started: usage limit, not a decision
# Raised from 1000 to 1400 on 2026-08-29 (Hidde: "ik verbruik zelf minder tokens
# dus is er meer over voor runs"). He is right and the 1000 was my guess, not a
# measurement: it came from the ONE week the machine hit the wall, and how much
# room there is depends on how much of the subscription he is using himself,
# which changes week to week. So the fixed number stops being the brake and
# becomes a runaway backstop. What actually governs is the limit itself, felt
# rather than predicted: see recent_limit_deaths below.
# Raised again, 1400 to 1800, on 2026-08-29 (Hidde: "ik zit op 57% van de week
# qua tokens"). The minutes said 74 percent spent while he measured 57, so the
# proxy was braking a third early: three runs that evening ran 7, 15 and 12
# minutes and produced nothing between them. 1040 minutes being 57 percent puts
# the week at about 1800, which is where this now sits.
#
# THE CAVEAT, because the arithmetic hides it: his 57 percent is the whole
# subscription, his own sessions included, and the minutes here only ever count
# the runs. So this number can only ever be approximately right, which is the
# same reason the paragraph above says a fixed number cannot know. It is a
# backstop against a runaway, not a measurement, and the real governor is still
# the limit felt in recent_limit_deaths.
# Raised again, 1800 to 5000, on 2026-09-02, and this one is a different KIND of
# change from the two above. Hidde is in Japan for the coming months and asked
# the question this file has been circling since July: "hoe zorgen we dat je dit
# zonder mij wel gaat doen." Every number here was calibrated for a week he
# SHARES, and he is about to stop sharing it. Measured the day he asked: the
# week stood at 1462 of 1800 and every knock after 06:00 UTC died on this line,
# nine of them in the preceding week spending 118 minutes between them for zero
# trees. The budget, not the usage limit, was the thing stopping the machine.
#
# 5000 a week and 900 a day was deliberately close to the physical ceiling (12
# knocks x 120 minutes = 1440 a day), which is another way of saying it was
# a runaway backstop and nothing else. The governor is recent_limit_deaths
# below, exactly as the paragraph above intends: an attempt the limit kills dies
# in seconds and costs nothing, and two deaths in six hours stop the window
# extending. That brake needs no number from anybody and it feels his absence
# and his return on its own.
#
# Back to 1800 / 260 on 2026-09-24 (Hidde: "zet het budget maar terug"): the
# raised budget cost about twice the minutes per tree by its second week
# (5.4 -> 9.1) and the shared subscription ran dry for his own sessions.
WEEK_BUDGET_MINUTES = 1800  # backstop only; the death brake is the real governor
# And the week has to be spread, not raced. A weekly budget alone front-loads:
# the loop would spend all thousand minutes by Wednesday and leave the back half
# of the week with a machine that starts and dies in seconds, which is the same
# blackout arriving on a schedule instead of by surprise. A seventh a day keeps
# it running every day, and a seventh is still one full 120-minute window plus
# change, which is the shape the numbers want (a tree every 2.4 minutes in a
# 40-to-70 minute run against every 25 minutes in a run under 20).
# Day raised 50% to 390 on 2026-09-26 (Hidde: "vergroot de dagrem maar ...
# laten we m met 50% vergroten"), the week left at 1800: on 09-25 two knocks
# died in seconds on the day's share while the week stood at 1075 of 1800.
DAY_BUDGET_MINUTES = 390   # was 260, a seventh of the week
LIMIT_DEATH_WINDOW_HOURS = 6   # how far back to look for "the window is shut right now"
LIMIT_DEATHS_TO_BACK_OFF = 2   # one can be a blip; two in six hours is the wall
PROBE_MINUTES = 20          # kept for the older callers that read it


def merge_results(first, second):
    """One window, two attempts: report the window, not the last attempt.

    The continuation writes its own execution record, and both attempts default
    to the same path on the runner, so reading only one of them would understate
    the window by exactly the amount the continuation was added to recover. The
    meter exists to be trusted, so it adds the halves and says there were two.
    Anything not additive (is_error, subtype) is taken from the LAST attempt,
    because that is the one that decided how the window ended."""
    if not second:
        return first
    if not first:
        return second
    out = dict(second)
    for key in ("duration_ms", "num_turns", "total_cost_usd"):
        a, b = first.get(key), second.get(key)
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            out[key] = a + b
        elif isinstance(a, (int, float)):
            out[key] = a
    for key in DENIAL_KEYS:
        a, b = first.get(key), second.get(key)
        if isinstance(a, list) and isinstance(b, list):
            out[key] = a + b
        elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
            out[key] = a + b
        elif key in first and key not in out:
            out[key] = a
    out["attempts"] = (first.get("attempts") or 1) + (second.get("attempts") or 1)
    return out


def spent_minutes(days, path=HEALTH, now=None):
    """Machine minutes recorded in the last `days` days. Unknown returns None."""
    try:
        with open(path, encoding="utf-8") as fh:
            runs = json.load(fh).get("runs") or []
    except (OSError, ValueError):
        return None
    now = now or datetime.datetime.now(datetime.timezone.utc)
    cutoff = now - datetime.timedelta(days=days)
    total = 0.0
    for r in runs:
        started = r.get("started")
        mins = r.get("minutes")
        if not started or not isinstance(mins, (int, float)):
            continue
        try:
            when = datetime.datetime.fromisoformat(str(started).replace("Z", "+00:00"))
        except ValueError:
            continue
        if when.tzinfo is None:
            when = when.replace(tzinfo=datetime.timezone.utc)
        if when >= cutoff:
            total += mins
    return round(total)


def recent_limit_deaths(hours=LIMIT_DEATH_WINDOW_HOURS, path=HEALTH, now=None):
    """Attempts the usage limit killed on arrival, in the last `hours`.

    The fingerprint is exact and worth writing down, because two different
    things both look like a dead run. A USAGE-LIMIT death has a result record
    saying turns 1, minutes 0.0, subtype success: the agent started, asked, was
    refused and stopped. A run killed for any other reason (the bot-actor
    refusal of 2026-08-28, a cancelled job) has NO result record at all, so its
    turns are null. Only the first kind means the window is shut, and only the
    first kind should make anything back off."""
    try:
        with open(path, encoding="utf-8") as fh:
            runs = json.load(fh).get("runs") or []
    except (OSError, ValueError):
        return None
    now = now or datetime.datetime.now(datetime.timezone.utc)
    cutoff = now - datetime.timedelta(hours=hours)
    deaths = 0
    for r in runs:
        turns = r.get("turns")
        if not isinstance(turns, (int, float)) or turns >= PROBE_MIN_TURNS:
            continue
        try:
            when = datetime.datetime.fromisoformat(str(r.get("started")).replace("Z", "+00:00"))
        except (TypeError, ValueError):
            continue
        if when.tzinfo is None:
            when = when.replace(tzinfo=datetime.timezone.utc)
        if cutoff <= when <= now:
            deaths += 1
    return deaths


def week_minutes(path=HEALTH, now=None):
    return spent_minutes(7, path, now)


def day_minutes(path=HEALTH, now=None):
    return spent_minutes(1, path, now)


def denial_report(days=7, path=HEALTH, now=None):
    """Which walls the runs hit, and how much of the window they cost.

    Measured 2026-09-19 across the 25 most recent working runs: 892 refusals in
    9,612 turns, 9.3 percent, one turn in eleven, and each one usually costs a
    retry as well. It was zero in mid-August and has grown every week since.
    That is the largest single piece of a night window this project can buy back
    without changing anything about how the work is done.

    Counts are RUNS a shape appeared in, not times it was refused: the record
    carries a set per run, deliberately, because the full list would be long and
    would repeat. So a shape in 40 of 60 runs is a standing wall, and one in 2 is
    a run improvising.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            records = json.load(fh).get("runs") or []
    except (OSError, ValueError):
        return None
    now = now or datetime.datetime.now(datetime.timezone.utc)
    cutoff = (now - datetime.timedelta(days=days)).date().isoformat()
    shapes, runs, turns, denials = {}, 0, 0, 0
    for r in records:
        if not isinstance(r, dict) or str(r.get("date") or "") < cutoff:
            continue
        if (r.get("minutes") or 0) <= 1:        # a knock the limit killed
            continue
        runs += 1
        turns += r.get("turns") or 0
        denials += r.get("denials") or 0
        source = r.get("denials_source") or ""
        if ":" not in source:
            continue
        for name in source.split(":", 1)[1].split(","):
            name = name.strip()
            if name and name != "no names in the record":
                shapes[name] = shapes.get(name, 0) + 1
    return {"days": days, "runs": runs, "turns": turns, "denials": denials,
            "rate": (denials / turns) if turns else 0.0,
            "shapes": sorted(shapes.items(), key=lambda kv: -kv[1])}


def probe(result, changed, minutes, elapsed=None, spent_week=None, spent_day=None,
          deaths=None):
    """(should_continue, one-line reason). Never raises: unknown means no.

    `elapsed` is minutes since the JOB started, which is not the same as the
    attempt's own duration once a window has had more than one attempt. The
    window is what has a clock; the attempt only has a decision."""
    if not isinstance(result, dict) or not result:
        return False, "no execution record, so nothing can be judged"
    if result.get("is_error"):
        return False, "the run reported an error; a retry would repeat it"
    turns = result.get("num_turns")
    if isinstance(turns, (int, float)) and turns < PROBE_MIN_TURNS:
        return False, f"only {turns} turn(s): the usage limit, not a decision"
    if minutes is None and elapsed is None:
        return False, "duration unknown, so the window cannot be judged"

    used = elapsed if elapsed is not None else minutes
    left = PROBE_CAP_MINUTES - used
    if left < PROBE_MIN_REMAINING:
        return False, (f"{round(left)} min left of the {PROBE_CAP_MINUTES} min window, "
                       f"too little to pay a fresh orientation")

    # The governor, and the reason the two budgets below are backstops rather
    # than predictions. How much room the machine has depends on how much of the
    # subscription Hidde is using himself that week, which no number here can
    # know. The limit can be FELT instead: attempts it kills leave a record, so
    # two of them in six hours means the window is shut and extending a run into
    # it buys nothing. When he is quiet there are none and the machine runs long.
    if deaths is not None and deaths >= LIMIT_DEATHS_TO_BACK_OFF:
        return False, (f"{deaths} attempts died on the usage limit in the last "
                       f"{LIMIT_DEATH_WINDOW_HOURS}h; the window is shut, not idle")
    if spent_week is not None and spent_week >= WEEK_BUDGET_MINUTES:
        return False, (f"the week has spent {spent_week} of {WEEK_BUDGET_MINUTES} "
                       f"budgeted minutes; the cron keeps knocking, this stops extending")
    if spent_day is not None and spent_day >= DAY_BUDGET_MINUTES:
        return False, (f"the last 24h spent {spent_day} of {DAY_BUDGET_MINUTES} budgeted "
                       f"minutes; the rest of the week gets its share")

    shipped = (changed or {}).get("trees") or 0
    week = f"; week at {spent_week}/{WEEK_BUDGET_MINUTES} min" if spent_week is not None else ""
    return True, (f"stopped after {round(used)} min having shipped {shipped} tree(s); "
                  f"{round(left)} min of the window still unspent{week}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--execution-file", default=os.environ.get("CLAUDE_EXECUTION_FILE"))
    ap.add_argument("--execution-file-2", default=os.environ.get("CLAUDE_EXECUTION_FILE_2"),
                    help="the continuation attempt's record, when the window got one")
    ap.add_argument("--execution-files", nargs="*", default=None,
                    help="every attempt's record, in order. One window can now have "
                         "four attempts, and reading only the last would understate it "
                         "by exactly the amount the loop was added to recover.")
    ap.add_argument("--since-sha", default=os.environ.get("RUN_START_SHA"))
    ap.add_argument("--by", default="night-run")
    ap.add_argument("--run-id", default=os.environ.get("GITHUB_RUN_ID"))
    ap.add_argument("--started", default=os.environ.get("RUN_STARTED_AT"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--week", action="store_true",
                    help="print the last 7 days of machine minutes against the budget. "
                         "Exit 1 when the budget is spent, so a caller can stop knocking.")
    ap.add_argument("--probe", action="store_true",
                    help="judge only: should this window get one more attempt? "
                         "Writes continue=yes|no to GITHUB_OUTPUT, records nothing.")
    ap.add_argument("--denials", action="store_true",
                    help="print which commands the allowlist refused, worst "
                         "first, and what share of every turn they cost.")
    ap.add_argument("--days", type=int, default=7,
                    help="the window --denials reads (default 7).")
    args = ap.parse_args()

    if args.denials:
        rep = denial_report(args.days)
        if not rep or not rep["runs"]:
            print("no run history readable")
            return 0
        print("%d working runs in %d days: %d of %d turns refused (%.1f%%)"
              % (rep["runs"], rep["days"], rep["denials"], rep["turns"],
                 rep["rate"] * 100))
        if not rep["shapes"]:
            print("no shapes recorded yet; the record carries counts only")
            return 0
        print("\n%-44s %s" % ("refused command shape", "runs it appeared in"))
        for name, n in rep["shapes"][:25]:
            print("%-44s %3d of %d" % (name[:44], n, rep["runs"]))
        print("\nA shape naming one binary is a binary to consider allowing. A "
              "shape naming\nseveral is a COMPOUND command, and no allowlist "
              "entry can ever match one:\nthe fix for those is to type them as "
              "separate calls.")
        return 0

    if args.week:
        spent, today = week_minutes(), day_minutes()
        if spent is None or today is None:
            print("no run history readable; assuming there is room")
            return 0
        deaths = recent_limit_deaths()
        print("week %d/%d min, last 24h %d/%d min, %s limit deaths in %dh"
              % (spent, WEEK_BUDGET_MINUTES, today, DAY_BUDGET_MINUTES,
                 "?" if deaths is None else deaths, LIMIT_DEATH_WINDOW_HOURS))
        if deaths is not None and deaths >= LIMIT_DEATHS_TO_BACK_OFF:
            print("the usage window is shut right now")
            return 1
        if spent >= WEEK_BUDGET_MINUTES:
            print("the week is spent")
            return 1
        if today >= DAY_BUDGET_MINUTES:
            print("the day's share is spent; the rest of the week gets its own")
            return 1
        return 0

    attempt_paths = []
    if args.execution_files and not args.probe:
        result = {}
        for path in args.execution_files:
            result = merge_results(result, read_result(path))
        attempt_paths = list(args.execution_files)
    else:
        attempt_paths = [p for p in (args.execution_file, args.execution_file_2) if p]
        result = read_result(args.execution_file)
        if not args.probe and args.execution_file_2 and args.execution_file_2 != args.execution_file:
            result = merge_results(result, read_result(args.execution_file_2))
    changed = what_changed(args.since_sha)
    now = datetime.datetime.now(datetime.timezone.utc)

    ms = result.get("duration_ms")
    denials, denials_source = denials_from(result)
    started_iso = args.started or now.replace(microsecond=0).isoformat()

    # A cancelled run is not an idle run, and until 2026-08-17 the meter counted
    # it as one. `duration_ms` comes from the agent's own execution-result file,
    # which a timeout cancellation never gets to write, so minutes came out null
    # and contributed ZERO to the utilisation number. On the night of 08-16 the
    # run that hit the 90 minute cap did 10 of the night's 12 real commits, and
    # the meter reported 9% utilisation against an honest 34%. Understating by a
    # factor of four, on the exact number a schedule decision is made from.
    #
    # So fall back to the wall clock, and say which of the two it is, because an
    # estimate presented as a measurement is the thing this project does not do.
    minutes = round(ms / 60000.0, 1) if isinstance(ms, (int, float)) else None
    minutes_basis = "measured"
    if minutes is None:
        try:
            began = datetime.datetime.fromisoformat(started_iso.replace("Z", "+00:00"))
            minutes = round((now - began).total_seconds() / 60.0, 1)
            minutes_basis = ("wall clock: the agent wrote no duration, which usually "
                             "means the job was cancelled at its timeout")
        except (TypeError, ValueError):
            minutes_basis = "unknown: no duration and no parseable start time"

    if args.probe:
        # Judge only. This runs BEFORE the record is written, changes nothing on
        # disk, and releases no claim: the window is not over yet.
        #
        # Elapsed is measured from the JOB's start, not the attempt's, because
        # by the third attempt the attempt's own duration says nothing about how
        # much window is left. Without a parseable start time it falls back to
        # the attempt duration, which is right for a first attempt and merely
        # conservative afterwards.
        elapsed = None
        try:
            began = datetime.datetime.fromisoformat(str(args.started).replace("Z", "+00:00"))
            if began.tzinfo is None:
                began = began.replace(tzinfo=datetime.timezone.utc)
            elapsed = round((now - began).total_seconds() / 60.0, 1)
        except (TypeError, ValueError):
            elapsed = None
        spent = week_minutes()
        today = day_minutes()
        if elapsed is not None:
            if spent is not None:
                spent += round(elapsed)
            if today is not None:
                today += round(elapsed)
        go, why = probe(result, changed,
                        minutes if minutes_basis == "measured" else None,
                        elapsed=elapsed, spent_week=spent, spent_day=today,
                        deaths=recent_limit_deaths())
        print(("continue: %s" % ("yes" if go else "no")) + " (%s)" % why)
        out = os.environ.get("GITHUB_OUTPUT")
        if out:
            with open(out, "a") as fh:
                fh.write("continue=%s\n" % ("yes" if go else "no"))
                fh.write("reason=%s\n" % why.replace("\n", " ")[:200])
        return 0

    record = {
        "started": started_iso,
        "date": now.strftime("%Y-%m-%d"),
        "run_id": args.run_id,
        "minutes": minutes,
        "minutes_basis": minutes_basis,
        "attempts": result.get("attempts", 1),
        "turns": result.get("num_turns"),
        "denials": denials,
        "denials_source": denials_source,
        # A run with no result record did not "end" in any sense the SDK saw;
        # it was killed. Saying so beats a null, because a null in this column
        # was being read as "quiet night" for two nights running.
        "ended": (result.get("subtype")
                  or ("error" if result.get("is_error") else None)
                  or ("cut off at the cap, no result record" if not result else None)),
        "tokens": tokens_from(result),
        "claims_held": claims_held(args.by),
    }
    if changed:
        record.update(changed)
    else:
        record["logged"] = None

    silent = changed is not None and not changed["logged"]
    # Only for the stub, and kept out of run-health.json: a run that logged
    # itself already said why, and the meter file is numbers.
    said = ([closing_words(p) for p in dict.fromkeys(attempt_paths)]
            if silent else [])

    if args.dry_run:
        print(json.dumps(record, indent=1))
        if silent:
            print("\n--- would prepend to LOG.md ---\n")
            print(stub_entry(dict(record, closing_words=said)))
        return 0

    append_health(record)
    freed = release_claims(args.by)
    wrote_stub = prepend_log(stub_entry(dict(record, closing_words=said))) if silent else False
    print(f"run health: {record['minutes']}min, {record['turns']} turns, "
          f"{record['denials']} refused, trees {record.get('trees')}, "
          f"logged={record.get('logged')}")
    if freed:
        print("released %d claim(s) the ended run still held: %s"
              % (len(freed), ", ".join(freed)))
    if wrote_stub:
        print("the run wrote no LOG.md entry; a stub was added in its place")
    return 0


if __name__ == "__main__":
    sys.exit(main())
