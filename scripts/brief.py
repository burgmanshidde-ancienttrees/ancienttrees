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


def main():
    out = ["ANCIENT TREES — state at session start", ""]
    since_last_visit(out)

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
