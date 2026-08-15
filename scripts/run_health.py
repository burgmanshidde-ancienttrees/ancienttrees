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
    for path in cities:
        delta += trees_in(path) - trees_in(path, since_sha)
    return {
        "commits": len(commits),
        "cities_touched": len(cities),
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


def append_health(record):
    try:
        doc = json.load(open(HEALTH))
        runs = doc.get("runs", []) if isinstance(doc, dict) else list(doc)
    except Exception:
        doc, runs = {}, []
    runs.append(record)
    doc = {
        "note": ("One record per night run, written by the workflow's own Run "
                 "health step, never by the run. A run cannot leave this empty "
                 "by giving up, which is the entire point: on 2026-08-15 four "
                 "runs ended after nine minutes of a sixty minute window and "
                 "left no trace at all. 'denials' counts commands the allowlist "
                 "refused; it has never been below 4 and reached 25."),
        "runs": runs[-400:],
    }
    with open(HEALTH, "w") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def stub_entry(record):
    """The LOG.md line a silent run did not write."""
    started = record.get("started", "")[:16].replace("T", " ")
    bits = []
    if record.get("minutes") is not None:
        bits.append(f"{record['minutes']} minutes of its 60 minute window")
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--execution-file", default=os.environ.get("CLAUDE_EXECUTION_FILE"))
    ap.add_argument("--since-sha", default=os.environ.get("RUN_START_SHA"))
    ap.add_argument("--by", default="night-run")
    ap.add_argument("--run-id", default=os.environ.get("GITHUB_RUN_ID"))
    ap.add_argument("--started", default=os.environ.get("RUN_STARTED_AT"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    result = read_result(args.execution_file)
    changed = what_changed(args.since_sha)
    now = datetime.datetime.now(datetime.timezone.utc)

    ms = result.get("duration_ms")
    record = {
        "started": args.started or now.replace(microsecond=0).isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "run_id": args.run_id,
        "minutes": round(ms / 60000.0, 1) if isinstance(ms, (int, float)) else None,
        "turns": result.get("num_turns"),
        "denials": result.get("permission_denials_count"),
        "ended": result.get("subtype") or ("error" if result.get("is_error") else None),
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
    wrote_stub = prepend_log(stub_entry(record)) if silent else False
    print(f"run health: {record['minutes']}min, {record['turns']} turns, "
          f"{record['denials']} refused, trees {record.get('trees')}, "
          f"logged={record.get('logged')}")
    if wrote_stub:
        print("the run wrote no LOG.md entry; a stub was added in its place")
    return 0


if __name__ == "__main__":
    sys.exit(main())
