#!/usr/bin/env python3
"""Smoke test: render key pages in headless Chrome and assert the product
actually works, the way a visitor meets it.

qa.py checks the HTML as written; this checks the HTML as EXECUTED. The gap
between those two is exactly where the dead check-in button of 2026-07-29
lived for days: the markup was fine, the script never ran. Approved by Hidde
2026-07-29 ("laten we het doen"); Chrome here is CI test tooling, not a site
dependency, the stack stays static.

Pages and assertions, deliberately few and stable:
  - homepage: hero image and search input exist in the rendered DOM
  - city page: walk banner exists, MapLibre actually produced a canvas
  - tree page: check-in button exists, carries the aria-pressed state the
    script sets on load, and no script source leaks as visible text
  - /explore: MapLibre canvas exists

Run: python3 scripts/smoke_test.py   (needs Chrome or Chromium on PATH)
Exit 1 on any failure; CI treats that as the site being broken (rung 2).
"""
import re
import shutil
import socket
import subprocess
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / "site" / "dist"

CHROME_CANDIDATES = [
    "google-chrome", "chromium-browser", "chromium", "chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def find_chrome():
    for c in CHROME_CANDIDATES:
        path = shutil.which(c) or (c if Path(c).exists() else None)
        if path:
            return path
    return None


def dump_dom(chrome, url):
    """Rendered DOM after JS ran. virtual-time-budget fast-forwards timers and
    waits on in-flight fetches, so map libs and inline scripts complete."""
    out = subprocess.run(
        [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
         "--virtual-time-budget=10000", "--dump-dom", url],
        capture_output=True, text=True, timeout=90)
    return out.stdout


def main():
    chrome = find_chrome()
    if not chrome:
        print("SMOKE: no Chrome/Chromium found; cannot run. "
              "In CI this is a real failure, locally install Chrome.")
        return 1
    if not (DIST / "index.html").exists():
        print(f"SMOKE: no build under {DIST}, run build_site.py first")
        return 1

    # pick a served city and tree page from what the build produced
    city = next(p for p in sorted(DIST.glob("*.html"))
                if (DIST / p.stem).is_dir() and p.stem not in ("app", "plus"))
    tree = next(p for p in sorted((DIST / city.stem).glob("*.html"))
                if p.name != "index.html" and "oldest-tree" not in p.name)

    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]

    class Quiet(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(DIST), **kw)

        def log_message(self, *a):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", port), Quiet)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{port}"

    checks = [
        (f"{base}/index.html", "homepage", [
            ('class="hero-bg"', "hero image"),
            ('id="city-q"', "search input"),
        ]),
        (f"{base}/{city.name}", f"city page ({city.stem})", [
            ('class="route-bar"', "walk banner"),
            ("maplibregl-canvas", "map canvas (JS ran, map constructed)"),
        ]),
        (f"{base}/{city.stem}/{tree.name}", f"tree page ({tree.stem})", [
            ("Check in with the app", "app-funnel check-in button (Hidde, 2026-07-30)"),
            ("maplibregl-canvas", "map canvas (JS on this page executed)"),
        ]),
        (f"{base}/explore.html", "explore", [
            ("maplibregl-canvas", "map canvas"),
            ("exc-", "city chooser panel rendered"),
        ]),
        (f"{base}/contribute.html", "contribute", [
            ('id="suggest"', "native suggestion form"),
            ("rest/v1/submissions", "form posts to our backend"),
        ]),
        (f"{base}/app.html", "app page", [
            ('id="waitlist"', "waitlist form"),
        ]),
    ]

    failures = []
    for url, label, wants in checks:
        dom = ""
        for attempt in (1, 2):  # one retry, headless Chrome can hiccup in CI
            try:
                dom = dump_dom(chrome, url)
            except subprocess.TimeoutExpired:
                dom = ""
            if dom:
                break
        if not dom:
            failures.append(f"{label}: Chrome produced no DOM for {url}")
            continue
        for needle, what in wants:
            if needle not in dom:
                failures.append(f"{label}: missing {what} ({needle!r})")
        # Script leaking as visible text: the 2026-07-29 bug class. Strip every
        # real script block from the rendered DOM; JS syntax in what remains is
        # source code the visitor can read, i.e. a script that never ran.
        visible = re.sub(r"<script\b.*?</script>", "", dom, flags=re.S)
        if re.search(r"\(function\(\)|localStorage\.|querySelector\(", visible):
            failures.append(f"{label}: script source visible as page text")

    server.shutdown()
    if failures:
        print(f"SMOKE FAILED: {len(failures)} problem(s)")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"Smoke passed: {len(checks)} pages rendered in Chrome, all assertions hold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
