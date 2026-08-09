#!/usr/bin/env python3
"""Move old LOG.md and CURATION.md entries into monthly archives.

Hidde, 2026-08-08: "onze files steeds groter aan het worden en daarmee token
verbruik, moeten we een ritme afspreken dat we dit opruimen." He is right and
the numbers were stark: CURATION.md had grown to 1,085 KB across 369 entries
and LOG.md to 562 KB across 313, both of which a session or a run may read.

What this does NOT do is delete anything. Every entry moves, verbatim, into
archive/LOG-YYYY-MM.md or archive/CURATION-YYYY-MM.md, and the living file
keeps a link to each archive. That matters because CURATION.md is the file
that records dead ends, and re-running an exhausted hunt is this project's
most repeated waste: a lost record costs research windows later.

Run it: python3 scripts/archive_logs.py [--days 30] [--dry-run]
"""
import argparse
import datetime
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE_DIR = os.path.join(ROOT, "archive")
FILES = ("LOG.md", "CURATION.md")
ENTRY_RE = re.compile(r"^## (\d{4})-(\d{2})-(\d{2})", re.M)

ARCHIVE_HEADER = """# {name} archive, {month}

Entries moved out of {name}.md by scripts/archive_logs.py to keep the living
file small enough to read cheaply. Nothing here is edited or summarised: it is
the original text, newest first. {name}.md links back to this file.
"""

POINTER_MARK = "<!-- archive-index -->"


def split_entries(text):
    """(header, [(date, entry_text)]) with entries in file order."""
    starts = [m.start() for m in ENTRY_RE.finditer(text)]
    if not starts:
        return text, []
    header = text[: starts[0]]
    entries = []
    for i, s in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(text)
        chunk = text[s:end]
        m = ENTRY_RE.match(chunk)
        entries.append((datetime.date(*(int(g) for g in m.groups())), chunk))
    return header, entries


def pointer_block(name, months):
    """The link list the living file carries, rebuilt from scratch each run."""
    if not months:
        return ""
    links = "\n".join(
        f"- [{m}](archive/{name}-{m}.md)" for m in sorted(months, reverse=True))
    return (f"{POINTER_MARK}\n\n**Older entries live in the archive**, moved by "
            f"`scripts/archive_logs.py`, nothing deleted:\n\n{links}\n\n"
            f"So absence from this file is not evidence something was never "
            f"tried: `grep -ri \"<place>\" archive/` before concluding a hunt "
            f"is new. Re-running an exhausted hunt is this project's most "
            f"repeated waste.\n{POINTER_MARK}\n")


def strip_pointer(header):
    return re.sub(re.escape(POINTER_MARK) + r".*?" + re.escape(POINTER_MARK) + r"\n?",
                  "", header, flags=re.S).rstrip() + "\n\n"


def archive_file(fname, cutoff, dry_run=False):
    path = os.path.join(ROOT, fname)
    if not os.path.exists(path):
        return None
    name = fname[:-3]
    text = open(path, encoding="utf-8").read()
    header, entries = split_entries(text)
    if not entries:
        return None

    keep = [(d, t) for d, t in entries if d >= cutoff]
    move = [(d, t) for d, t in entries if d < cutoff]

    # Months already archived stay in the pointer list even when this run moves
    # nothing new, or the links would vanish the week after they appeared.
    existing = set()
    if os.path.isdir(ARCHIVE_DIR):
        for f in os.listdir(ARCHIVE_DIR):
            m = re.match(rf"{re.escape(name)}-(\d{{4}}-\d{{2}})\.md$", f)
            if m:
                existing.add(m.group(1))

    by_month = {}
    for d, t in move:
        by_month.setdefault(f"{d.year:04d}-{d.month:02d}", []).append((d, t))

    if not move and existing:
        # Nothing to move, but make sure the pointer is present and correct.
        new_header = strip_pointer(header) + pointer_block(name, existing)
        new_text = new_header + "".join(t for _, t in keep)
        if new_text != text and not dry_run:
            open(path, "w", encoding="utf-8").write(new_text)
        return {"file": fname, "moved": 0, "kept": len(keep), "months": []}
    if not move:
        return {"file": fname, "moved": 0, "kept": len(keep), "months": []}

    if not dry_run:
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
    for month, items in by_month.items():
        apath = os.path.join(ARCHIVE_DIR, f"{name}-{month}.md")
        items.sort(key=lambda x: x[0], reverse=True)
        body = "".join(t for _, t in items)
        if os.path.exists(apath):
            old = open(apath, encoding="utf-8").read()
            _, old_entries = split_entries(old)
            merged = old_entries + items
            merged.sort(key=lambda x: x[0], reverse=True)
            body = "".join(t for _, t in merged)
        out = ARCHIVE_HEADER.format(name=name, month=month) + "\n" + body
        if not dry_run:
            open(apath, "w", encoding="utf-8").write(out)

    months = existing | set(by_month)
    new_text = strip_pointer(header) + pointer_block(name, months) + \
        "".join(t for _, t in keep)
    if not dry_run:
        open(path, "w", encoding="utf-8").write(new_text)
    return {"file": fname, "moved": len(move), "kept": len(keep),
            "months": sorted(by_month), "kb_before": len(text) // 1024,
            "kb_after": len(new_text) // 1024}


def main():
    ap = argparse.ArgumentParser()
    # 7, and the number is measured rather than chosen: at 14 days the two
    # files still totalled 1.4 MB, at 7 they total 172 KB, because a single
    # heavy day sits just outside the week. Seven also matches what CLAUDE.md
    # already says about LOG.md, "assume he has not looked in a week".
    ap.add_argument("--days", type=int, default=7,
                    help="entries older than this move to the archive")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    cutoff = datetime.date.today() - datetime.timedelta(days=args.days)
    print(f"cutoff: entries before {cutoff} move to archive/")
    for fname in FILES:
        r = archive_file(fname, cutoff, args.dry_run)
        if not r:
            print(f"  {fname}: no dated entries")
            continue
        if r["moved"]:
            print(f"  {r['file']}: moved {r['moved']}, kept {r['kept']}, "
                  f"{r.get('kb_before')}KB -> {r.get('kb_after')}KB, "
                  f"months {', '.join(r['months'])}")
        else:
            print(f"  {r['file']}: nothing older than the cutoff, kept {r['kept']}")


if __name__ == "__main__":
    main()
