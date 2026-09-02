#!/usr/bin/env python3
"""The Monday mail: is the machine alive, and what did it produce.

Hidde, 2026-09-02, leaving for Japan for the coming months: "ik heb niet het
idee als ik jou geen input ga geven dat je genoeg tokens gaat gebruiken om
steden te vullen en bomen te zoeken, hoe zorgen we dat je dit zonder mij wel
gaat doen." Part of the answer is that nothing reaches him. Every alarm this
project has fires into a file: health.py, brief.py and the fresh-eyes review
all wait for somebody to open a session. In August the review failed on its own
schedule three mornings running and the weekly analysis was dead for a week,
and both were found by accident. That is survivable while he is here most days.
It is not survivable for months.

So this is deliberately NOT another dashboard. It is one screen, once a week,
and its first job is the alarm: a red gate, a night shift that stopped, knocks
that stopped arriving, a week that produced nothing. Underneath it passes
through DATA.md's newest entry VERBATIM, because that file already writes the
tables he asked for in the format he asked for them (CLAUDE.md: "kun je je
digest vanaf nu altijd in tabellen geven dit is onleesbaar"), and re-narrating
those numbers into a paragraph is exactly what he told us to stop doing.

    python3 scripts/weekly_mail.py            # print it, send nothing
    python3 scripts/weekly_mail.py --send     # send it to $WEEKLY_TO

The address lives in the WEEKLY_TO environment variable, out of the repository,
because this repository is public and his email address is not.

A mail failure never fails the caller. There is nothing here that cannot wait a
week, and the workflow around it should not go red over an SMTP hiccup.
"""
import argparse
import datetime
import json
import os
import re
import smtplib
import subprocess
import sys
from email.message import EmailMessage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

RUN_HEALTH = os.path.join(ROOT, "data", "run-health.json")
DATA_MD = os.path.join(ROOT, "DATA.md")


def runs():
    try:
        doc = json.load(open(RUN_HEALTH))
    except (OSError, ValueError):
        return []
    return doc if isinstance(doc, list) else doc.get("runs", [])


def week_table(days=7):
    """One row per day: runs, minutes, trees, commits, and the cities touched.

    The cities column is Hidde's (2026-08-24, "kun je ook altijd vertellen welke
    steden de nachtruns hebben gedaan"), and it is the column that turns this
    from a utilisation meter into something worth reading on a phone: minutes
    say the machine ran, city names say what came of it.
    """
    by = {}
    for r in runs():
        d = r.get("date") or (r.get("started") or "")[:10]
        if not d:
            continue
        b = by.setdefault(d, {"runs": 0, "min": 0.0, "trees": 0, "commits": 0,
                              "cities": []})
        b["runs"] += 1
        b["min"] += float(r.get("minutes") or 0)
        t = r.get("trees")
        b["trees"] += t if isinstance(t, int) else 0
        c = r.get("commits")
        b["commits"] += len(c) if isinstance(c, list) else (c if isinstance(c, int) else 0)
        # `cities` is a COUNT on the older records and a list on the newer
        # ones, and `cities_touched` is the list that replaced it. Read whichever
        # is actually a list; a number here is not a name.
        touched = r.get("cities_touched")
        if not isinstance(touched, list):
            touched = r.get("cities") if isinstance(r.get("cities"), list) else []
        for city in touched:
            name = city if isinstance(city, str) else (city.get("city") or "")
            if name and name not in b["cities"]:
                b["cities"].append(name)
    rows, tot = [], {"runs": 0, "min": 0.0, "trees": 0, "commits": 0}
    for d in sorted(by)[-days:]:
        b = by[d]
        rows.append((d, b["runs"], round(b["min"]), b["trees"], b["commits"],
                     ", ".join(b["cities"][:6]) or "-"))
        for k in tot:
            tot[k] += b[k]
    return rows, tot


def gates():
    """Every watched workflow's newest FINISHED verdict, via health.py's own list."""
    try:
        import health
    except Exception:
        return []
    out = []
    for wf, (label, max_age, fix) in health.WATCHED.items():
        got = health.gh_latest(wf)
        if not got:
            out.append((label, "unknown", None))
            continue
        conclusion, created = got
        out.append((label, conclusion or "unknown", created))
    return out


def alarms():
    """The lines that justify the mail existing. Empty is the good week."""
    said = []
    # CANCELLED IS NOT BROKEN, and saying it is would kill this mail inside a
    # month. Every workflow here cancels its predecessor, so a busy afternoon
    # leaves a trail of cancelled runs and an alarm that fires every week is an
    # alarm nobody opens. brief.py made the same decision for the same reason.
    for label, conclusion, _ in gates():
        if conclusion in ("failure", "timed_out", "startup_failure"):
            said.append("%s: the newest finished run %s. Something is broken."
                        % (label, conclusion.replace("_", " ")))
    try:
        import health
        streak, since = health.night_shift_idle()
        if streak >= 3:
            said.append("The night shift has died in seconds %d times running, "
                        "since %s. That is the usage limit or a broken workflow, "
                        "not a quiet week." % (streak, (since or "")[:16]))
        fired = health.knocks_fired()
        if fired is not None and fired < health.KNOCK_FLOOR:
            said.append("Only %d of %d knocks arrived in the last 24 hours. "
                        "GitHub is dropping the schedule."
                        % (fired, health.KNOCKS_A_DAY))
    except Exception:
        pass
    _, tot = week_table()
    if tot["trees"] == 0:
        said.append("Not one tree went live in seven days.")
    if tot["min"] < 200:
        said.append("The machine worked %d minutes in seven days. It has stopped."
                    % round(tot["min"]))
    try:
        import run_health
        spent = run_health.week_minutes()
        if spent and spent >= run_health.WEEK_BUDGET_MINUTES * 0.9:
            said.append("The week spent %d of its %d budgeted minutes, so knocks "
                        "are being refused. Raise WEEK_BUDGET_MINUTES or leave it."
                        % (spent, run_health.WEEK_BUDGET_MINUTES))
    except Exception:
        pass
    return said


def newest_data_entry():
    """DATA.md's newest day, verbatim, headings and tables and all."""
    try:
        text = open(DATA_MD).read()
    except OSError:
        return ""
    parts = re.split(r"^## ", text, flags=re.M)
    return ("## " + parts[1]).rstrip() if len(parts) > 1 else ""


def md_to_html(md):
    """The smallest markdown renderer that covers what DATA.md writes.

    Tables, headings, bold and plain lines. Stdlib only and deliberately dumb:
    this reads a file we write ourselves, so the input is known, and a real
    markdown library would be a dependency bought for one mail a week.
    """
    # A cap, and it SAYS what it dropped. CLAUDE.md's rule: "if a workflow bounds
    # coverage, log what was dropped, because silent truncation reads as
    # covered-everything when it did not." The reader-feedback table runs to
    # forty rows of vote bookkeeping and this is a mail read on a phone.
    MAX_ROWS = 14
    out, in_table, rows_done, dropped = [], False, 0, 0
    for line in md.split("\n"):
        cells = None
        if line.strip().startswith("|") and line.strip().endswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
            continue  # the alignment row
        if cells and in_table and rows_done >= MAX_ROWS and "**" not in line:
            dropped += 1
            continue
        if cells:
            rows_done = rows_done + 1 if in_table else 0
            if not in_table:
                out.append('<table cellspacing="0" cellpadding="6" '
                           'style="border-collapse:collapse;margin:12px 0;'
                           'font-size:14px">')
                in_table = True
                tag = "th"
            else:
                tag = "td"
            row = "".join(
                '<%s style="border:1px solid #ddd;text-align:%s">%s</%s>'
                % (tag, "right" if re.fullmatch(r"[\d.,%*\s-]+", c) else "left",
                   inline(c), tag)
                for c in cells)
            out.append("<tr>%s</tr>" % row)
            continue
        if in_table:
            if dropped:
                out.append("<tr><td colspan='9' style='border:1px solid #ddd;"
                           "font-size:13px;color:#777'>%d more row(s) not shown; "
                           "the whole table is in DATA.md</td></tr>" % dropped)
            out.append("</table>")
            in_table, rows_done, dropped = False, 0, 0
        s = line.strip()
        if not s:
            continue
        if s.startswith("## "):
            out.append("<h2 style='font-size:18px;margin:22px 0 6px'>%s</h2>"
                       % inline(s[3:]))
        elif s.startswith("**") and s.endswith("**"):
            out.append("<p style='margin:14px 0 4px'><strong>%s</strong></p>"
                       % inline(s.strip("*")))
        else:
            out.append("<p style='margin:6px 0;font-size:14px'>%s</p>" % inline(s))
    if in_table:
        if dropped:
            out.append("<tr><td colspan='9' style='border:1px solid #ddd;"
                       "font-size:13px;color:#777'>%d more row(s) not shown; "
                       "the whole table is in DATA.md</td></tr>" % dropped)
        out.append("</table>")
    return "\n".join(out)


def inline(s):
    s = (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)


def compose():
    said = alarms()
    rows, tot = week_table()
    today = datetime.date.today().isoformat()

    head = []
    if said:
        head.append("<div style='background:#fff4f4;border-left:4px solid #c33;"
                    "padding:10px 14px;margin:0 0 18px'>")
        head.append("<p style='margin:0 0 6px'><strong>Needs you</strong></p>")
        for s in said:
            head.append("<p style='margin:4px 0;font-size:14px'>%s</p>" % inline(s))
        head.append("</div>")
    else:
        head.append("<p style='margin:0 0 18px;font-size:14px;color:#2a6'>"
                    "Everything is running. Nothing needs you.</p>")

    machine = ["<h2 style='font-size:18px;margin:22px 0 6px'>What the machine did"
               "</h2>",
               '<table cellspacing="0" cellpadding="6" style="border-collapse:'
               'collapse;margin:12px 0;font-size:14px">',
               "<tr>" + "".join(
                   "<th style='border:1px solid #ddd;text-align:left'>%s</th>" % h
                   for h in ("Day", "Runs", "Minutes", "Trees", "Commits", "Cities"))
               + "</tr>"]
    for d, n, m, t, c, cities in rows:
        machine.append("<tr>"
                       + "".join("<td style='border:1px solid #ddd;text-align:%s'>%s</td>"
                                 % (a, inline(str(v)))
                                 for v, a in ((d, "left"), (n, "right"), (m, "right"),
                                              (t, "right"), (c, "right"),
                                              (cities, "left")))
                       + "</tr>")
    machine.append("<tr><td style='border:1px solid #ddd'><strong>7 days</strong></td>"
                   "<td style='border:1px solid #ddd;text-align:right'><strong>%d</strong></td>"
                   "<td style='border:1px solid #ddd;text-align:right'><strong>%d</strong></td>"
                   "<td style='border:1px solid #ddd;text-align:right'><strong>%d</strong></td>"
                   "<td style='border:1px solid #ddd;text-align:right'><strong>%d</strong></td>"
                   "<td style='border:1px solid #ddd'></td></tr>"
                   % (tot["runs"], round(tot["min"]), tot["trees"], tot["commits"]))
    machine.append("</table>")

    gate_lines = ["<p style='margin:14px 0 4px;font-size:14px'>%s: %s</p>"
                  % (label, conclusion) for label, conclusion, _ in gates()]

    html = ("<div style=\"font-family:-apple-system,Segoe UI,Helvetica,Arial,"
            "sans-serif;max-width:720px;margin:0 auto;color:#222\">"
            + "<p style='color:#777;font-size:13px;margin:0 0 14px'>Ancient Trees, "
            "week to %s</p>" % today
            + "\n".join(head) + "\n".join(machine) + "\n".join(gate_lines)
            + md_to_html(newest_data_entry())
            + "<p style='color:#777;font-size:12px;margin:26px 0 0'>Written by "
              "scripts/weekly_mail.py. The tables under the line are DATA.md's "
              "newest entry, passed through unchanged.</p></div>")

    subject = "Ancient Trees: %d trees this week%s" % (
        tot["trees"], ", %d thing(s) need you" % len(said) if said else "")
    plain = re.sub(r"<[^>]+>", " ", html)
    plain = re.sub(r"\s+", " ", plain).strip()
    return subject, html, plain


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", action="store_true")
    a = ap.parse_args()

    subject, html, plain = compose()
    to = os.environ.get("WEEKLY_TO", "").strip()

    if not a.send:
        print("SUBJECT:", subject)
        print("TO:", to or "(WEEKLY_TO not set)")
        print()
        print(plain[:4000])
        return 0

    if not to:
        print("WEEKLY_TO is not set, so there is nobody to send to. "
              "Set it as a repository secret; it stays out of this public repo.")
        return 0

    creds = {k: os.environ.get("OUTREACH_" + k) for k in
             ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS", "FROM")}
    if not all(creds.values()):
        print("No SMTP credentials in the environment; printed nothing, sent nothing.")
        return 0

    msg = EmailMessage()
    msg["From"] = creds["FROM"]
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(plain)
    msg.add_alternative(html, subtype="html")
    try:
        server = smtplib.SMTP(creds["SMTP_HOST"], int(creds["SMTP_PORT"]), timeout=30)
        server.starttls()
        server.login(creds["SMTP_USER"], creds["SMTP_PASS"])
        server.send_message(msg)
        server.quit()
        print("sent:", subject)
    except Exception as e:
        # Never fail the caller. See the module docstring.
        print("MAIL FAILED: %s" % str(e)[:200])
    return 0


if __name__ == "__main__":
    sys.exit(main())
