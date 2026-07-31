#!/usr/bin/env python3
"""Post-build QA over site/dist. Runs on every deploy, after build_site.py.

build_site.py validates what it is ABOUT to write (contracts, lengths,
script hygiene); this script validates what actually landed on disk, the
way a browser will meet it. The split matters: build checks catch what the
generator knows about, this catches what it forgot it was generating.

Checks, all deterministic, no network:
  1. Internal links resolve to a real file (GitHub Pages resolution rules:
     exact file, +.html, or /index.html).
  2. Internal image/script/css sources resolve the same way.
  3. No em dash anywhere in rendered text (hard rule 3).
  4. No banned filler words in rendered text (CLAUDE.md Step 3).
  5. img src urls are http(s) or site-relative, never a Wikimedia File: page.

Exit 1 on any failure, so CI fails the deploy. Run: python3 scripts/qa.py
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / "site" / "dist"

BANNED_WORDS = ["hidden gem", "must-see", "breathtaking", "nestled"]


class PageScan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []      # href/src values
        self.img_srcs = []
        self.text_parts = []
        self._skip_depth = 0  # inside script/style

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self._skip_depth += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("img", "script") and a.get("src"):
            (self.img_srcs if tag == "img" else self.links).append(a["src"])
        if tag == "link" and a.get("href"):
            self.links.append(a["href"])

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data):
        if not self._skip_depth:
            self.text_parts.append(data)


def resolves(target: Path) -> bool:
    """GitHub Pages resolution: exact file, file + .html, or dir/index.html."""
    if target.is_file():
        return True
    if target.with_suffix(target.suffix + ".html").is_file():
        return True
    if (target / "index.html").is_file():
        return True
    return False


def main():
    failures = []
    pages = sorted(DIST.rglob("*.html"))
    if not pages:
        print(f"QA: no pages found under {DIST}, run build_site.py first")
        return 1

    for page in pages:
        rel = page.relative_to(DIST)
        scan = PageScan()
        scan.feed(page.read_text(encoding="utf-8"))
        text = " ".join(scan.text_parts)

        if rel.name == "index.html" and rel.parent.name == "":
            import re as _re
            m = _re.search(r"<title>([^<]*)</title>", page.read_text(encoding="utf-8"))
            if m and not m.group(1).startswith("Ancient Trees"):
                failures.append(f"{rel}: homepage <title> is {m.group(1)!r}; a shelf caption once shadowed it")

        if "—" in text:
            failures.append(f"{rel}: em dash in rendered text (hard rule 3)")
        lower = text.lower()
        for word in BANNED_WORDS:
            if word in lower:
                failures.append(f"{rel}: banned word {word!r} in rendered text")

        for src in scan.img_srcs:
            if "/wiki/File:" in src:
                failures.append(f"{rel}: img src is a wiki File: page: {src}")
            if not (src.startswith("http") or src.startswith("data:")
                    or not re.match(r"^[a-z]+:", src)):
                failures.append(f"{rel}: img src with unexpected scheme: {src}")

        for url in scan.links + scan.img_srcs:
            if re.match(r"^(https?:|mailto:|data:|tel:)", url):
                continue
            path = url.split("#", 1)[0].split("?", 1)[0]
            if not path:
                continue  # pure #anchor
            base = DIST if path.startswith("/") else page.parent
            target = (base / path.lstrip("/")).resolve()
            if not resolves(target):
                failures.append(f"{rel}: dead internal link {url!r}")

    if failures:
        print(f"QA FAILED: {len(failures)} problem(s) in {len(pages)} pages")
        for f in failures[:60]:
            print(f"  - {f}")
        if len(failures) > 60:
            print(f"  ... and {len(failures) - 60} more")
        return 1
    print(f"QA passed: {len(pages)} pages, links resolve, text clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
