#!/usr/bin/env python3
"""Session briefing, injected automatically at session start.

Hidde checks in sporadically and should not have to ask where things stand.
This prints the state of the project so it lands in context before he types.
"""

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def sh(*args):
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                              timeout=15).stdout.strip()
    except Exception:
        return ""


STATE = ROOT / ".claude" / "last-brief-head"


def since_last_visit(out):
    """What happened since Hidde's previous session: the missed part."""
    sh("git", "fetch", "-q")  # pick up overnight run pushes; silent if offline
    tip = sh("git", "rev-parse", "origin/main") or sh("git", "rev-parse", "HEAD")
    last = STATE.read_text().strip() if STATE.exists() else ""
    if last and last != tip:
        rng = f"{last}..{tip}"
        commits = sh("git", "log", "--oneline", rng)
        n = len(commits.splitlines()) if commits else 0
        bots = sh("git", "log", "--format=%an", rng).splitlines().count("claude[bot]")
        out += [f"SINCE YOUR LAST VISIT: {n} commit(s), {bots} by the autonomous runs.", ""]
        titles = sh("git", "log", "--format=%s", rng, "--author=claude[bot]")
        if titles:
            out.append("What the runs did, newest first:")
            out += [f"  - {t}" for t in titles.splitlines()[:12]]
            out.append("")
        # newest visitors line the runs logged
        log = sh("git", "show", f"{tip}:LOG.md")
        for line in log.splitlines():
            if line.strip().startswith("- Visitors"):
                out += [f"Latest visitor reading: {line.strip()[2:]}", ""]
                break
    elif last:
        out += ["SINCE YOUR LAST VISIT: nothing new pushed. The machine may be mid-run.", ""]
    try:
        STATE.parent.mkdir(exist_ok=True)
        STATE.write_text(tip)
    except Exception:
        pass


# THE ALARM, WHERE SOMEBODY IS STANDING.
#
# Added 2026-08-27, and the reason is one of this project's worst weeks. iOS CI
# had built the app, run every test and measured every screen on every push
# since 08-20. It went RED on 08-24 and stayed red through five pushes and three
# days, with a real bug in it the whole time: a destructive confirmation whose
# only button was the destructive one. Nothing was wrong with the gate. Nothing
# read it.
#
# health.py has watched ios.yml since 08-25, and that is a rung a RUN checks,
# which means it is checked when a run happens to look. This is the other half:
# the brief is the first thing in front of every session and in front of Hidde,
# so a red gate now has to be walked past rather than found.
#
# ONE gh call for every workflow at once, because the hook has twenty seconds
# and a call per workflow would eat them. Silent on every failure: no network,
# no gh, no auth, and the brief still prints. A briefing that breaks is worse
# than a briefing that is missing a line.
def broken_gates(out):
    """Name a broken gate above everything else.

    ONE CALL PER WORKFLOW, run side by side, and it has to be. The first
    version asked `gh run list -L 100` once and grouped the answer, which is
    cheaper and was wrong: this repository runs about twenty-five workflows an
    hour, so a hundred runs reach back roughly FOUR HOURS. Every job that runs
    once a day, which is every job worth watching here, fell out of the window
    and read as fine. Seven small calls in parallel take about as long as the
    one big one did.
    """
    watched = ["deploy.yml", "smoke.yml", "ios.yml", "review.yml",
               "data-digest.yml", "weekly-analysis.yml", "routes.yml"]

    def latest(wf):
        raw = sh("gh", "run", "list", "--workflow", wf, "-L", "8",
                 "--json", "workflowName,conclusion,status,createdAt,event")
        try:
            rows = json.loads(raw) if raw else []
        except Exception:
            return wf, []
        return wf, [r for r in rows
                    if r.get("status") == "completed" and r.get("conclusion")]

    try:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=7) as pool:
            answers = dict(pool.map(latest, watched))
    except Exception:
        return

    failed, never, asleep = [], [], []
    for wf, runs in answers.items():
        if not runs:
            continue
        name = runs[0].get("workflowName") or wf

        # CANCELLED IS NOT AN ALARM ON ITS OWN, and getting this wrong would
        # make the whole thing useless. Every workflow here cancels its own
        # predecessor on a new push, so on a busy afternoon the newest finished
        # run is cancelled almost every time. An alarm that fires every day is
        # an alarm nobody believes, which is the exact problem this solves.
        if runs[0]["conclusion"] == "failure":
            failed.append((name, runs[0].get("createdAt", "")[:10]))
        elif not any(r["conclusion"] == "success" for r in runs):
            # Nothing has passed at all, which is what cancelled-only hides,
            # including a job cancelled by its own timeout.
            never.append((name, len(runs)))

        # A JOB WHOSE SCHEDULED RUNS KEEP DYING WHILE MANUAL ONES PASS looks
        # perfectly healthy to both questions above. Not hypothetical: the
        # fresh-eyes review died on its 06:10 cron on three consecutive days in
        # August, and running it by hand later each day left a green run behind
        # that answered both questions with "fine". Nobody noticed the nightly
        # review had simply stopped happening. So ask separately about the runs
        # the job starts BY ITSELF, which are the ones nobody is watching.
        timed = [r for r in runs if r.get("event") == "schedule"][:3]
        if timed and all(r["conclusion"] != "success" for r in timed):
            asleep.append((name, len(timed), timed[0].get("createdAt", "")[:10]))

    if not failed and not never and not asleep:
        return

    out.append("BROKEN, and this outranks new work (CLAUDE.md rung 2):")
    for name, when in sorted(failed):
        out.append(f"  {name} FAILED, newest finished run {when}")
    for name, n in sorted(never):
        out.append(f"  {name} has not passed once in its last {n} finished run(s)")
    for name, n, when in sorted(asleep):
        out.append(f"  {name} keeps failing ON ITS SCHEDULE ({n} in a row, newest {when}), "
                   f"even though running it by hand works")
    out += ["  Why: gh run list --workflow=<file> -L 5, "
            "then gh run view <id> --log-failed", ""]


def main():
    out = ["ANCIENT TREES — state at session start", ""]
    since_last_visit(out)
    broken_gates(out)

    # Cities and trees
    try:
        cities = json.loads((ROOT / "data" / "city-list.json").read_text())["cities"]
        done = [c for c in cities if c["status"] != "pending"]
        nxt = next((c["city"] for c in cities if c["status"] == "pending"), "none")
        trees = approx = photos = 0
        for f in sorted((ROOT / "data" / "cities").glob("*.json")):
            for t in json.loads(f.read_text()).get("trees", []):
                trees += 1
                note = (t.get("notes") or "").lower()
                if t.get("location_precision") == "approximate" or (
                        t.get("curation_status") == "flagged" and "exact position" in note):
                    approx += 1
                p = t.get("photo") or {}
                if p.get("url"):
                    photos += 1
        out += [f"{len(done)} cities live, {trees} trees. Next up: {nxt}.",
                f"{photos}/{trees} have a photo. {approx} pins are only approximate.", ""]
    except Exception as e:
        out += [f"(could not read city data: {e})", ""]

    # What the runs have been doing
    commits = sh("git", "log", "--oneline", "-8", "--no-merges")
    if commits:
        out += ["Recent commits:"] + [f"  {c}" for c in commits.splitlines()] + [""]

    # Anything waiting on Hidde
    log = ROOT / "LOG.md"
    if log.exists():
        text = log.read_text()
        if "# Open with Hidde" in text:
            block = text.split("# Open with Hidde", 1)[1].split("\n---", 1)[0]
            heads = [ln.strip("# ").strip() for ln in block.splitlines()
                     if ln.startswith("###")]
            if heads:
                out += ["Waiting on Hidde (full detail in LOG.md):"]
                out += [f"  - {h}" for h in heads] + [""]
        fors = [ln.strip("- ").strip() for ln in text.splitlines()
                if ln.strip().startswith("- FOR HIDDE")]
        if fors:
            out += ["Flagged by recent runs:"] + [f"  - {f}" for f in fors[:5]] + [""]

    # Is the working tree clean and is anything unpushed
    dirty = sh("git", "status", "--porcelain")
    if dirty:
        out.append(f"Working tree has {len(dirty.splitlines())} uncommitted change(s).")
    ahead = sh("git", "rev-list", "--count", "origin/main..HEAD")
    if ahead and ahead != "0":
        out.append(f"{ahead} commit(s) not pushed.")

    out += ["", "Open with a short spoken summary of this: what changed, what needs him.",
            "Do not re-read these files unless he asks for detail."]
    print("\n".join(out))


if __name__ == "__main__":
    main()


# Presence beacon (Hidde's capacity ruling, 2026-07-28): opening a session tells
# the research chain to leave the daytime usage window alone for 4 hours.
# Fire-and-forget; every failure is silent because the brief must never break.
try:
    import subprocess, os
    env = dict(os.environ)
    env["PATH"] = os.path.expanduser("~/.local/bin") + ":" + env.get("PATH", "")
    subprocess.Popen(
        ["gh", "workflow", "run", "presence.yml",
         "--repo", "burgmanshidde-ancienttrees/ancienttrees"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)
except Exception:
    pass
