#!/usr/bin/env python3
"""The quality line: one light per platform, under Hidde's numbers.

    python3 scripts/quality.py          the line as DATA.md carries it
    python3 scripts/quality.py --json   every cell, for a session to read

Hidde, 2026-11-04: "I'd rather have some sort of overview and a green, red,
or orange light somewhere in the daily digest than more text. I don't want to
have to look at it if everything's green." So when every light is green (or
grey for what does not exist yet) the digest carries ONE line; otherwise the
line plus a small table holding only the rows that are not green, each
non-green cell with its reason.

Three platforms, Web, iOS and Android (grey "not live yet" until an android/
folder exists), and three rows:

  Next version  the version about to go live: the newest CI verdict on main
                (web: "Build and deploy site", deploy.yml, and whether the
                last good deploy is older than 12 hours while newer commits
                wait; iOS: "iOS app", ios.yml), the weekly code review
                (REVIEW.md "## YYYY-MM-DD code", due every 7 days) and the
                daily fresh-eyes review (REVIEW.md "## YYYY-MM-DD", daily).
                Web also: page speed of the ten most-seen pages
                (scripts/page_speed.py, data/page-speed.json, weekly) and
                open Dependabot security alerts on the site's libraries.
  Live          what people use now: iOS from the MetricKit crash data
                (crashes.assess, the same burst logic health.py reads); Web
                from the page error table (scripts/web_errors.py) and the
                outside site-up check (uptime.yml, every 15 minutes). Reader
                submissions carry no "bug" kind, so they are not read here.
  Open bugs     open BUG rows per surface in data/code-audit.json (APP is the
                iOS app, WEB the website), and how many are older than 7 days.

Lights: green fine; orange late or being fixed (a check overdue up to twice
its maximum age, a deploy 12 to 24 hours behind, an open bug, a crash fix
waiting for the store); red needs a person (CI red on main, a deploy stuck
past 24 hours, a crash burst, a new web error spreading, a check overdue past
twice its age, a bug open past 14 days). Grey is unknown or not live: it
never turns the line red, and the one-line form says when something could
not be read, so "all fine" is never claimed on missing data.

GitHub's run states are read with gh (~/.local/bin locally; in data-digest.yml
with the workflow's GITHUB_TOKEN). Without gh, or without a token, those cells
are grey "unknown" and nothing fails.
"""
import datetime
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ORDER = {"grey": 0, "green": 1, "orange": 2, "red": 3}
PLATFORMS = ("web", "ios", "android")
NAMES = {"web": "Web", "ios": "iOS", "android": "Android"}
ROWS = (("next", "Next version"), ("live", "Live"), ("bugs", "Open bugs"))
SURFACE = {"web": "WEB", "ios": "APP"}

FRESH_EYES_DAYS = 1    # review.yml, twice a day
CODE_REVIEW_DAYS = 7   # BRIEF_CODE_AUDIT.md, due every seven days
DEPLOY_ORANGE_H = 12
DEPLOY_RED_H = 24
BUG_ORANGE_DAYS = 7
BUG_RED_DAYS = 14

HEX = {"green": "#2f8a3c", "orange": "#e0891a", "red": "#c6372c", "grey": "#a7a79d"}


def worst(cells):
    return max((c[0] for c in cells), key=lambda c: ORDER[c], default="grey")


UNKNOWN = r"unknown|unreadable|no database key|no finished|needs a|settings\)|not measured|not connected"
UNREAD = []  # grey parts hidden inside a green cell, named in the one-line form


def combine(cells):
    """One cell from several: the worst colour, the reasons of the cells
    that are not green (or of every cell when all are grey). A grey part
    that should have answered is kept in UNREAD so "all fine" is never
    claimed over it."""
    colour = worst(cells)
    reasons = [r for c, r in cells if c == colour and c != "green"]
    if colour == "green":
        reasons = []
    if colour != "grey":
        UNREAD.extend(r for c, r in cells if c == "grey" and re.search(UNKNOWN, r)
                      and r not in UNREAD)
    return colour, "; ".join(reasons)


# ---------------------------------------------------------------- GitHub

def _gh():
    for p in (shutil.which("gh"), os.path.expanduser("~/.local/bin/gh")):
        if p and os.path.exists(p):
            return p
    return None


def runs(workflow, limit=60):
    """Runs of a workflow on main, newest first, or None when gh cannot say."""
    gh = _gh()
    if not gh:
        return None
    try:
        out = subprocess.run([gh, "run", "list", "--workflow", workflow, "-b", "main",
                              "-L", str(limit), "--json", "conclusion,status,createdAt"],
                             capture_output=True, text=True, timeout=60, cwd=ROOT)
        if out.returncode != 0:
            return None
        return json.loads(out.stdout or "[]")
    except Exception:
        return None


def _when(iso):
    try:
        return datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except Exception:
        return None


def newest_commit():
    """When main last moved: origin/main when it can be read, else HEAD."""
    for ref in ("origin/main", "HEAD"):
        try:
            out = subprocess.run(["git", "log", "-1", "--format=%cI", ref], capture_output=True,
                                 text=True, timeout=20, cwd=ROOT).stdout.strip()
            if out:
                return datetime.datetime.fromisoformat(out)
        except Exception:
            pass
    return None


def ci_cell(workflow, label, now, deploy=False):
    rows = runs(workflow)
    if rows is None:
        return "grey", "%s state unknown (no gh)" % label
    judged = [r for r in rows if r.get("status") == "completed"
              and r.get("conclusion") not in ("", None, "cancelled", "skipped")]
    if not judged:
        return "grey", "no finished %s run in the last %d" % (label, len(rows))
    if judged[0]["conclusion"] != "success":
        return "red", "%s %s on main" % (label, judged[0]["conclusion"])
    if deploy:
        ok = [_when(r["createdAt"]) for r in judged if r["conclusion"] == "success"]
        last_ok = max(w for w in ok if w)
        head = newest_commit()
        hours = (now - last_ok).total_seconds() / 3600
        if head and head > last_ok and hours > DEPLOY_ORANGE_H:
            colour = "red" if hours > DEPLOY_RED_H else "orange"
            return colour, "last deploy %.0fh ago, newer commits waiting" % hours
    return "green", ""


# ---------------------------------------------------------------- reviews

def _review_days(text):
    fresh, code = [], []
    for m in re.finditer(r"^## (\d{4}-\d{2}-\d{2})(.*)$", text, flags=re.M):
        try:
            d = datetime.date.fromisoformat(m.group(1))
        except ValueError:
            continue
        (code if m.group(2).strip().startswith("code") else fresh).append(d)
    return max(fresh, default=None), max(code, default=None)


def _age_cell(last, today, max_days, label):
    if last is None:
        return "red", "no %s on file" % label
    age = (today - last).days
    if age <= max_days:
        return "green", ""
    colour = "orange" if age <= 2 * max_days else "red"
    return colour, "%s %d days old (due every %d)" % (label, age, max_days)


def review_cells(today):
    try:
        text = open(os.path.join(ROOT, "REVIEW.md"), encoding="utf-8").read()
    except OSError:
        text = ""
    fresh, code = _review_days(text)
    label = "code review"
    if code is None:
        # Before the first weekly entry: the one-off review of 2026-11-04
        # filled the ledger, so its newest first_seen stands in for it.
        seen = [r.get("first_seen") for r in _ledger()]
        seen = [s for s in seen if s]
        if seen:
            code = datetime.date.fromisoformat(max(seen))
    return (_age_cell(fresh, today, FRESH_EYES_DAYS, "fresh-eyes review"),
            _age_cell(code, today, CODE_REVIEW_DAYS, label))


# ---------------------------------------------------------------- bugs

def _ledger():
    try:
        with open(os.path.join(ROOT, "data", "code-audit.json"), encoding="utf-8") as f:
            return json.load(f).get("findings") or []
    except (OSError, ValueError):
        return []


def bug_cell(surface, today):
    open_ = [r for r in _ledger() if r.get("surface") == surface
             and r.get("kind") == "BUG" and r.get("status") == "open"]
    if not open_:
        return "green", "", 0, 0
    ages = []
    for r in open_:
        try:
            ages.append((today - datetime.date.fromisoformat(r.get("first_seen", ""))).days)
        except ValueError:
            ages.append(0)
    old = sum(1 for a in ages if a > BUG_ORANGE_DAYS)
    colour = "red" if max(ages) > BUG_RED_DAYS else "orange"
    reason = "%d open" % len(open_) + (", %d older than 7 days" % old if old else "")
    if colour == "red":
        reason += ", oldest %d days" % max(ages)
    return colour, reason, len(open_), old


# ---------------------------------------------------------------- live

def ios_live():
    try:
        import crashes
        sigs, stores = crashes.load(days=7, symbolicate=False)
    except Exception as e:
        return "grey", "crash data unreadable (%s)" % str(e)[:50]
    if sigs is None:
        return "grey", "crash data unreadable (%s)" % stores
    levels = [a["level"] for a in crashes.assess(sigs, stores)]
    if "urgent" in levels:
        return "red", "crash needs a new build now"
    if "act" in levels or "reapply" in levels:
        return "red", "crash burst on a store build"
    if "waiting" in levels:
        return "orange", "crash fix waiting for the store build"
    return "green", ""


def web_live():
    try:
        import web_errors
        return web_errors.light()
    except Exception as e:
        return "grey", "error table unreadable (%s)" % str(e)[:50]


def uptime_cell(now):
    """uptime.yml, every 15 minutes from outside: red when the last two
    checks failed, orange when any failed in the last 24 hours."""
    rows = runs("uptime.yml", limit=120)
    if rows is None:
        return "grey", "site-up check unknown"
    done = [r for r in rows if r.get("status") == "completed"
            and r.get("conclusion") in ("success", "failure", "timed_out")]
    if not done:
        return "grey", "site-up check has no finished run yet (unknown)"
    if len(done) >= 2 and all(r["conclusion"] != "success" for r in done[:2]):
        return "red", "site not answering (last two checks failed)"
    cut = now - datetime.timedelta(hours=24)
    failed = [r for r in done if r["conclusion"] != "success"
              and (_when(r.get("createdAt", "")) or now) >= cut]
    if failed:
        return "orange", "site check failed %d time(s) in 24h" % len(failed)
    return "green", ""


def speed_cell():
    try:
        import page_speed
        return page_speed.light()
    except Exception as e:
        return "grey", "page speed unreadable (%s)" % str(e)[:50]


def security_cell(now):
    """Open Dependabot security alerts on the repository (gh api). Orange
    for any open alert, red for a high or critical one older than 7 days.
    No permission, or alerts switched off, is grey: it never fails."""
    gh = _gh()
    if not gh:
        return "grey", "security alerts unknown (no gh)"
    try:
        out = subprocess.run([gh, "api", "repos/{owner}/{repo}/dependabot/alerts?state=open&per_page=100"],
                             capture_output=True, text=True, timeout=60, cwd=ROOT)
    except Exception:
        return "grey", "security alerts unknown"
    if out.returncode != 0:
        if "disabled" in (out.stdout + out.stderr):
            return "grey", "security alerts (off in GitHub settings)"
        return "grey", "security alerts unknown (no permission)"
    try:
        alerts = json.loads(out.stdout or "[]")
    except ValueError:
        return "grey", "security alerts unknown"
    if not alerts:
        return "green", ""
    old_bad = [a for a in alerts
               if (a.get("security_advisory") or {}).get("severity") in ("high", "critical")
               and (_when(a.get("created_at", "")) or now) < now - datetime.timedelta(days=7)]
    if old_bad:
        return "red", "%d high or critical library alert(s) open past 7 days" % len(old_bad)
    return "orange", "%d open library security alert(s)" % len(alerts)


# ---------------------------------------------------------------- the line

def android_exists():
    return os.path.isdir(os.path.join(ROOT, "android"))


def assess(now=None):
    """{platform: {row: (colour, reason)}}, plus the open-bug counts."""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    today = now.date()
    del UNREAD[:]
    fresh, code = review_cells(today)
    q = {}
    web_bugs = bug_cell("WEB", today)
    q["web"] = {
        "next": combine([ci_cell("deploy.yml", "deploy", now, deploy=True), code, fresh,
                         speed_cell(), security_cell(now)]),
        "live": combine([web_live(), uptime_cell(now)]),
        "bugs": web_bugs[:2],
    }
    ios_bugs = bug_cell("APP", today)
    q["ios"] = {
        "next": combine([ci_cell("ios.yml", "iOS build", now), code, fresh]),
        "live": ios_live(),
        "bugs": ios_bugs[:2],
    }
    why = "no checks wired yet" if android_exists() else "not live yet"
    q["android"] = {k: ("grey", why) for k, _ in ROWS}
    q["_unread"] = list(UNREAD)
    return q


def overall(q, p):
    return worst(q[p].values())


def _unknown(q):
    """What should have answered and could not ("not connected yet" and "not
    live yet" are known states, not missing data): grey cells, and grey parts
    of cells that are green."""
    out = [r for p in ("web", "ios") for c, r in q[p].values()
           if c == "grey" and re.search(UNKNOWN, r)]
    return out + [r for r in q.get("_unread", []) if r not in out]


def _tail(q):
    n = _unknown(q)
    if not n:
        return "all fine"
    return "nothing wrong seen; not read: " + "; ".join(n)


def markdown(q):
    """The block DATA.md carries. Plain words for the colours: DATA.md is text."""
    heads = ", ".join("%s %s" % (NAMES[p], "not live yet" if q[p]["next"][1] == "not live yet"
                                 else overall(q, p)) for p in PLATFORMS)
    bad = [(k, label) for k, label in ROWS
           if any(q[p][k][0] in ("orange", "red") for p in PLATFORMS)]
    if not bad:
        tail = _tail(q)
        return "**Quality**: %s. %s." % (heads, tail[0].upper() + tail[1:])
    out = ["**Quality**: %s." % heads, "",
           "| | %s |" % " | ".join(NAMES[p] for p in PLATFORMS),
           "|---|%s|" % "|".join("---" for _ in PLATFORMS)]
    for k, label in bad:
        cells = []
        for p in PLATFORMS:
            c, r = q[p][k]
            cells.append(c if c in ("green", "grey") and not (c == "grey" and r)
                         else ("%s: %s" % (c, r) if r else c))
        out.append("| %s | %s |" % (label, " | ".join(cells)))
    return "\n".join(out)


def _dot(colour, size=11):
    return ('<span style="display:inline-block;width:%dpx;height:%dpx;border-radius:50%%;'
            'background:%s;vertical-align:-1px;margin-right:5px"></span>' % (size, size, HEX[colour]))


def html(q):
    """The same block for the digest page, with real lights."""
    import html as _h
    heads = "&nbsp;&nbsp;".join("%s%s" % (_dot(overall(q, p)), NAMES[p]) for p in PLATFORMS)
    bad = [(k, label) for k, label in ROWS
           if any(q[p][k][0] in ("orange", "red") for p in PLATFORMS)]
    style = 'style="margin:10px 0 6px;font-size:15px"'
    if not bad:
        return '<p %s><strong>Quality</strong>&nbsp;&nbsp;%s&nbsp;&nbsp;%s</p>' % (
            style, heads, _h.escape(_tail(q)))
    out = ['<p %s><strong>Quality</strong>&nbsp;&nbsp;%s</p>' % (style, heads),
           "<table><thead><tr><th></th>%s</tr></thead><tbody>" % "".join(
               "<th>%s</th>" % NAMES[p] for p in PLATFORMS)]
    for k, label in bad:
        tds = []
        for p in PLATFORMS:
            c, r = q[p][k]
            show = r if c in ("orange", "red") or (c == "grey" and r) else ""
            tds.append("<td>%s%s</td>" % (_dot(c, 9), _h.escape(show)))
        out.append("<tr><td>%s</td>%s</tr>" % (label, "".join(tds)))
    out.append("</tbody></table>")
    return "".join(out)


def section(_today=None):
    """For daily_digest.py: the markdown block."""
    return markdown(assess())


def main():
    q = assess()
    if "--json" in sys.argv:
        print(json.dumps(q, indent=1))
    else:
        print(markdown(q))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
