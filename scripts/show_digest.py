#!/usr/bin/env python3
"""The newest DATA.md day entry as one local page, for the preview pane.

Hidde, 2026-10-14, on what the daily digest costs in a session: reading the
43,000-character entry and typing it back into chat was most of it. So a
session shows him the entry AS WRITTEN on a page (his own tables, his own
order, nothing reworded), and chat carries only what needs him: the two lines
this script prints.

    python3 scripts/show_digest.py        # build the page, print the top lines

Written to out/digest/index.html and mirrored next to the inspect page, so the
same preview server shows both: `preview_start {name: "inspect"}`, then open
http://127.0.0.1:8766/digest.html. See inspect_readers.py's docstring for the
server (four lines; /private/tmp can be cleared on a reboot).
"""
import datetime
import hashlib
import html
import os
import re
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out", "digest")
PREVIEW = "/private/tmp/claude-501/-Users-hidde-Documents-Ancienttrees/preview/inspect"
WITHHELD = re.compile(r"^(\d+) chars, read it in the database$")


def readers_words(md, day):
    """Put a reader's own words where DATA.md says "read it in the database".

    Hidde, 2026-10-19, on "The Yew of Campo Santana | correction sent in |
    49 chars, read it in the database": "please also show me these things
    always with digest". DATA.md is public, so daily_digest.py withholds what
    a reader typed; this page is local, so it fetches the words and shows
    them. A row is matched on its day, tree, kind, account marker and length,
    the same fields daily_digest.readers_said() printed.
    """
    if "read it in the database" not in md:
        return md, 0, 0
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import inbox
    key = inbox.load_key()
    if not key:
        return md, 0, -1
    since = (datetime.date.fromisoformat(day) - datetime.timedelta(days=10)).isoformat()
    try:
        rows = inbox.get("/rest/v1/submissions?select=created_at,kind,city,tree,why,user_id"
                         "&created_at=gte.%s&order=created_at.asc"
                         % urllib.parse.quote(since + "T00:00:00"), key)
    except Exception as e:
        print("reader words: database unreadable (%s)" % str(e)[:60])
        return md, 0, -1
    found = {}
    for r in rows or []:
        why = (r.get("why") or "").strip()
        uid = r.get("user_id")
        who = hashlib.sha1(str(uid).encode()).hexdigest()[:4] if uid else "no acct"
        k = (str(r.get("created_at"))[5:10], (r.get("tree") or r.get("city") or "-")[:34],
             "%s sent in" % (r.get("kind") or "?"), len(why), who)
        found[k] = why
    out, shown, missing = [], 0, 0
    for line in md.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else []
        m = WITHHELD.match(cells[3]) if len(cells) >= 5 else None
        if m:
            words = found.get((cells[0], cells[1], cells[2], int(m.group(1)), cells[4]))
            if words is None:
                missing += 1
            else:
                cells[3] = "“%s”" % re.sub(r"\s+", " ", words).replace("|", "/")
                line = "| " + " | ".join(cells) + " |"
                shown += 1
        out.append(line)
    text = "\n".join(out)
    if shown:
        text = text.replace("structure only; the words stay in the database",
                            "their words fetched from the database for this page")
    return text, shown, missing


def readers_in_full(day):
    """Everything a stranger sent since the digest's day, word for word.

    Hidde, 2026-10-25, after a Porto ambassador request reached the digest as
    "1 feedback report": "ik wil vanaf nu altijd exacte feedback berichten in
    mn daily digest net als tree inzendingen of notities, niet samenvatten,
    gewoon geheel aan me geven". DATA.md is public, so the words never go
    there; this page is local and fetches them. Submissions (every kind,
    votes included), notes on trees, and the note under a shared app
    photograph. Never a name or an address."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import inbox
    from daily_digest import is_ours, TEST_SUBMISSION_IDS
    key = inbox.load_key()
    if not key:
        return "**Everything readers sent, in full**: no database key on this Mac, nothing read."
    since = urllib.parse.quote(day + "T00:00:00")
    rows = []
    try:
        for r in inbox.get("/rest/v1/submissions?select=id,created_at,kind,city,tree,page,why,"
                           "location_hint,girth_cm,photo,outcome,reply_text,user_id"
                           "&created_at=gte.%s&order=created_at.asc" % since, key) or []:
            if r.get("id") in TEST_SUBMISSION_IDS or is_ours(r.get("user_id")):
                continue
            extra = []
            if r.get("location_hint"):
                extra.append("where: %s" % r["location_hint"])
            if r.get("girth_cm"):
                extra.append("girth: %s cm" % r["girth_cm"])
            if r.get("photo"):
                extra.append("with a photograph")
            if r.get("reply_text"):
                extra.append("our reply: “%s”" % r["reply_text"])
            rows.append((r["created_at"], "%s (#%s, %s)" % (r.get("kind") or "?", r["id"], r.get("page") or "web"),
                         r.get("tree") or r.get("city") or "-", r.get("why") or "", extra,
                         r.get("outcome") or "open"))
    except Exception as e:
        rows.append(("", "submissions", "-", "database unreadable (%s)" % str(e)[:60], [], ""))
    try:
        for r in inbox.get("/rest/v1/tree_notes?select=user_id,tree_id,body,hidden,created_at"
                           "&created_at=gte.%s&order=created_at.asc" % since, key) or []:
            if is_ours(r.get("user_id")):
                continue
            rows.append((r["created_at"], "note on a tree", r.get("tree_id") or "-", r.get("body") or "",
                         ["hidden"] if r.get("hidden") else [], "live"))
    except Exception as e:
        rows.append(("", "tree notes", "-", "database unreadable (%s)" % str(e)[:60], [], ""))
    try:
        for r in inbox.get("/rest/v1/sightings?select=user_id,tree_id,name,note,shared,status,updated_at"
                           "&shared=eq.true&updated_at=gte.%s&order=updated_at.asc" % since, key) or []:
            if is_ours(r.get("user_id")):
                continue
            rows.append((r["updated_at"], "app photograph", r.get("tree_id") or r.get("name") or "-",
                         r.get("note") or "", [], r.get("status") or ""))
    except Exception as e:
        rows.append(("", "app photographs", "-", "database unreadable (%s)" % str(e)[:60], [], ""))
    head = "**Everything readers sent since %s, in full** (word for word; names and addresses left out)" % day
    if not rows:
        return head + "\n\nNothing."
    out = [head, "", "| When (UTC) | What | Tree or place | Their words, in full | Also | Status |",
           "|---|---|---|---|---|---|"]
    for when, what, where, words, extra, status in sorted(rows, key=lambda r: r[0]):
        cell = lambda s: re.sub(r"\s+", " ", str(s)).replace("|", "/")
        out.append("| %s | %s | %s | %s | %s | %s |" % (
            cell(when[:16].replace("T", " ")), cell(what), cell(where),
            "“%s”" % cell(words) if words.strip() else "(nothing typed)",
            cell("; ".join(extra)) or "-", cell(status)))
    return "\n".join(out)


def newest_entry():
    txt = open(os.path.join(ROOT, "DATA.md"), encoding="utf-8").read()
    m = re.search(r"^## \d{4}-\d{2}-\d{2} \(previous UTC day\)$", txt, flags=re.M)
    if not m:
        return None, ""
    nxt = txt.find("\n## ", m.end())
    return m.group(0)[3:], txt[m.end():nxt if nxt != -1 else len(txt)]


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*([^*]+)\*(?![*\w])", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2" target="_blank">\1</a>', s)
    return s


def render(md):
    out, lines, i = [], md.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            out.append("<pre>%s</pre>" % html.escape("\n".join(lines[i + 1:j])))
            i = j + 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            cells = lambda r: [c.strip() for c in r.strip().strip("|").split("|")]
            body = [r for r in rows[1:] if not re.match(r"^\|[\s:|-]+\|?$", r)]
            t = ["<table><thead><tr>%s</tr></thead><tbody>" % "".join(
                "<th>%s</th>" % inline(c) for c in cells(rows[0]))]
            for r in body:
                t.append("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in cells(r)))
            out.append("".join(t) + "</tbody></table>")
            continue
        if re.match(r"^\s*- ", line):
            items = []
            while i < len(lines) and re.match(r"^\s*- ", lines[i]):
                items.append("<li>%s</li>" % inline(re.sub(r"^\s*- ", "", lines[i])))
                i += 1
            out.append("<ul>%s</ul>" % "".join(items))
            continue
        if line.strip():
            out.append("<p>%s</p>" % inline(line))
        i += 1
    return "\n".join(out)


PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Daily digest %(day)s</title><style>
body{font:15px/1.5 -apple-system,system-ui,sans-serif;max-width:1100px;margin:0 auto;padding:16px;color:#1d2a1f;background:#fbfbf8}
h1{font-size:22px;margin:8px 0 16px}p{margin:10px 0}strong{color:#22301f}
table{border-collapse:collapse;margin:8px 0 16px;font-size:13.5px;display:block;overflow-x:auto;max-width:100%%}
th,td{border-bottom:1px solid #e3e3dc;padding:5px 9px;text-align:left;vertical-align:top}
th{background:#eef0e8;position:sticky;top:0}td:first-child,th{white-space:nowrap}code,pre{font:12.5px ui-monospace,Menlo,monospace;background:#f0f1ec;border-radius:4px}
code{padding:1px 4px}pre{padding:10px;overflow-x:auto}a{color:#3d6b35}ul{padding-left:20px}
</style></head><body><h1>Daily digest %(day)s</h1>
%(body)s</body></html>"""


def main():
    head, md = newest_entry()
    if head is None:
        print("DATA.md carries no day entry")
        return 1
    day = head.split(" ")[0]
    # An entry written before 2026-10-19 has no block for photographs on
    # existing trees; compute it now so the page always answers that.
    if "Photographs added to trees already live" not in md:
        try:
            import daily_digest
            extra = daily_digest.photos_on_existing_section()
        except Exception:
            extra = None
        if extra:
            md = extra + " (computed now)\n\n" + md if extra.endswith("none.") else \
                extra.replace("\n\n", " (computed now)\n\n", 1) + "\n\n" + md
    md, shown, missing = readers_words(md, day)
    # Every reader photograph he has not seen, new tree or existing (Hidde,
    # 2026-10-25: "het is echt kwalijk als ik niet weet van ambassadeurs of
    # fotos of trees"). reader_photos.py builds photos.html beside this page.
    try:
        import subprocess
        out = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "reader_photos.py")],
                             capture_output=True, text=True, timeout=900).stdout
        n = int(out.split("reader photos:")[1].split()[0])
        md = ("**Readers' photographs you have not seen: %d.** [Open them all](http://127.0.0.1:8766/photos.html), "
              "new trees and trees we already had." % n) + "\n\n" + md
    except Exception as e:
        md = "**Readers' photographs**: the photo page failed (%s)\n\n" % str(e)[:90] + md
    try:
        md = readers_in_full(day) + "\n\n" + md
    except Exception as e:
        md = "**Everything readers sent, in full**: failed (%s)\n\n" % str(e)[:90] + md
    if missing < 0:
        print("READER WORDS NOT SHOWN: no database key (~/.ancienttrees-supabase.env); the page still says 'read it in the database'.")
    elif missing:
        print("reader words: %d shown, %d not matched in the database" % (shown, missing))
    page = PAGE % {"day": html.escape(day), "body": render(md)}
    for folder, name in ((OUT, "index.html"), (PREVIEW, "digest.html")):
        try:
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, name), "w", encoding="utf-8") as f:
                f.write(page)
        except OSError as e:
            print("could not write %s (%s)" % (folder, e))
    print("digest %s: out/digest/index.html; preview: http://127.0.0.1:8766/digest.html" % day)
    # Hidde, 2026-10-15, after being shown the 13th on the 15th: when he asks
    # in the morning, yesterday's digest is made first, not shown stale.
    yesterday = (datetime.datetime.now(datetime.timezone.utc).date()
                 - datetime.timedelta(days=1)).isoformat()
    if day < yesterday:
        print("STALE: the newest entry is %s, not %s. Run `gh workflow run data-digest.yml --ref main`,"
              " watch it, git pull, then run this again before showing him the link." % (day, yesterday))
    # The lines for chat: the headline and the trees waiting for him.
    for line in md.splitlines():
        if line.startswith("**Today:") or line.startswith("**Trees readers sent"):
            print(re.sub(r"\*\*", "", line))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
