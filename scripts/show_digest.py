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
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out", "digest")
PREVIEW = "/private/tmp/claude-501/-Users-hidde-Documents-Ancienttrees/preview/inspect"


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
th{background:#eef0e8;position:sticky;top:0}code,pre{font:12.5px ui-monospace,Menlo,monospace;background:#f0f1ec;border-radius:4px}
code{padding:1px 4px}pre{padding:10px;overflow-x:auto}a{color:#3d6b35}ul{padding-left:20px}
</style></head><body><h1>Daily digest %(day)s</h1>
%(body)s</body></html>"""


def main():
    head, md = newest_entry()
    if head is None:
        print("DATA.md carries no day entry")
        return 1
    day = head.split(" ")[0]
    page = PAGE % {"day": html.escape(day), "body": render(md)}
    for folder, name in ((OUT, "index.html"), (PREVIEW, "digest.html")):
        try:
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, name), "w", encoding="utf-8") as f:
                f.write(page)
        except OSError as e:
            print("could not write %s (%s)" % (folder, e))
    print("digest %s: out/digest/index.html; preview: http://127.0.0.1:8766/digest.html" % day)
    # The lines for chat: the headline and the trees waiting for him.
    for line in md.splitlines():
        if line.startswith("**Today:") or line.startswith("**Trees readers sent"):
            print(re.sub(r"\*\*", "", line))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
