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


DENIAL_KEYS = ("permission_denials_count", "permission_denials",
               "num_permission_denials", "denied_tool_uses",
               "tool_permission_denials", "blocked_tool_uses")


def _denial_label(d):
    """What was refused, in the smallest form that is still useful.

    The first version recorded the TOOL name only, on the reasoning that a
    denied command can carry a URL or a path from a reader submission and this
    file is public. The reasoning is right and the result was useless: every
    night reported "Bash" and nothing else, so 123 refusals across six runs told
    us the wall was made of shell and never which wall.

    So take the first word of the command, the binary, and nothing after it.
    `rm`, `xargs`, `chmod`, `swiftc`, `bash` carry no URL, no path and no
    reader data, and the binary is the entire question: the allowlist is a list
    of binaries. Anything that does not look like a bare command name is
    dropped rather than truncated, because a guess at where an argument starts
    is how a path leaks.
    """
    tool = str(d.get("tool_name") or d.get("tool") or d.get("name") or "?")[:24]
    inp = d.get("tool_input") or d.get("input") or {}
    cmd = inp.get("command") if isinstance(inp, dict) else None
    if tool == "Bash" and isinstance(cmd, str):
        first = cmd.strip().split()[0] if cmd.strip() else ""
        # A bare binary name only: letters, digits, dash, underscore, dot.
        if first and re.fullmatch(r"[A-Za-z0-9._-]{1,20}", first):
            return "Bash(%s)" % first
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
    return (
        f"## {record['date']} - Night run {started} UTC ended without saying anything\n"
        "\n"
        f"Written by the workflow's Run health step, not by the run. {shape.capitalize()}, "
        f"ended clean ({ended}). {produced}{left}\n"
        "\n"
        "This entry exists because the run wrote none. The prompt asks every run to "
        "log even when it ships nothing, and a run that gives up is exactly the one "
        "that skips that instruction, so the count above is measured rather than "
        "reported. What it cannot tell you is WHY the run stopped: the transcript is "
        "hidden on purpose, the repo being public. If this shape repeats, the two "
        "things worth suspecting are the usage window and the refused commands.\n"
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
# One continuation, never a loop: there is a single extra step in the workflow,
# so the worst case is two attempts inside one already-paid-for window. It fires
# only for the case that is pure waste, an early voluntary stop with no trees.
# A run that died on the usage limit is left alone, because a second attempt
# would die in seconds for the same reason.
PROBE_MINUTES = 20      # under this, with nothing shipped, the window is worth another go
PROBE_MIN_TURNS = 5     # below this it never really started: usage limit, not a decision


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
    out["attempts"] = 2
    return out


def probe(result, changed, minutes):
    """(should_continue, one-line reason). Never raises: unknown means no."""
    if not isinstance(result, dict) or not result:
        return False, "no execution record, so nothing can be judged"
    if result.get("is_error"):
        return False, "the run reported an error; a retry would repeat it"
    turns = result.get("num_turns")
    if isinstance(turns, (int, float)) and turns < PROBE_MIN_TURNS:
        return False, f"only {turns} turn(s): the usage limit, not a decision"
    if minutes is None:
        return False, "duration unknown, so the window cannot be judged"
    if minutes >= PROBE_MINUTES:
        return False, f"used {minutes} min of its window"
    if changed is None:
        return False, "cannot resolve what changed, so assume it worked"
    if (changed.get("trees") or 0) > 0:
        return False, f"shipped {changed['trees']} tree(s) in {minutes} min"
    return True, (f"stopped after {minutes} min with {changed.get('commits', 0)} commit(s) "
                  f"and no trees; {int(PROBE_MINUTES)}+ min of window left unused")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--execution-file", default=os.environ.get("CLAUDE_EXECUTION_FILE"))
    ap.add_argument("--execution-file-2", default=os.environ.get("CLAUDE_EXECUTION_FILE_2"),
                    help="the continuation attempt's record, when the window got one")
    ap.add_argument("--since-sha", default=os.environ.get("RUN_START_SHA"))
    ap.add_argument("--by", default="night-run")
    ap.add_argument("--run-id", default=os.environ.get("GITHUB_RUN_ID"))
    ap.add_argument("--started", default=os.environ.get("RUN_STARTED_AT"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--probe", action="store_true",
                    help="judge only: should this window get one more attempt? "
                         "Writes continue=yes|no to GITHUB_OUTPUT, records nothing.")
    args = ap.parse_args()

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
        go, why = probe(result, changed, minutes if minutes_basis == "measured" else None)
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

    if args.dry_run:
        print(json.dumps(record, indent=1))
        if silent:
            print("\n--- would prepend to LOG.md ---\n")
            print(stub_entry(record))
        return 0

    append_health(record)
    freed = release_claims(args.by)
    wrote_stub = prepend_log(stub_entry(record)) if silent else False
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
