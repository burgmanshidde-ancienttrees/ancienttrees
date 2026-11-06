#!/usr/bin/env python3
"""Do the pages RUN? A real Chrome opens a fixed set of pages and waits.

Hidde, 2026-11-06 ("ons platform wordt steeds groter, dit soort fouten worden
steeds duurder", then "dit lijkt me een goed systeem doe het"): that afternoon
/explore crashed every visitor's tab a few seconds after loading (Chrome
"Error code 5"). The trees list painted its hearts with a function that
refiltered the map, the refilter redrew the list, forever. Every check in the
deploy passed, because qa.py and preflight read the HTML and the data and
never run a line of the JavaScript; the smoke test runs Chrome, but after the
site is live, and its hang was read as a fault of the test.

So this opens each page in Chrome at desktop and phone width, waits long
enough for the late work to happen (the card catalogue arrives after a few
seconds, which is exactly when that loop started), and fails when:
  - the tab crashed (the renderer died: Chrome's "Aw, Snap" / error code 5),
  - the page stopped answering (the main thread is stuck in a loop),
  - an uncaught JavaScript error came from our own scripts.
A failing page is opened once more before it counts, so one slow start is not
a blocked deploy; a broken page fails both times.

Two uses, one page set:
  python3 scripts/pagecheck.py                 the built site in site/dist,
                                               served locally (deploy.yml,
                                               BEFORE the upload: a failure
                                               keeps the old site live)
  python3 scripts/pagecheck.py --live          https://ancienttrees.app
                                               (livecheck.yml, every hour)
  python3 scripts/pagecheck.py --base URL      any other origin

Needs Python Playwright (pip install playwright==1.60.0). It drives the Chrome
the machine already has (channel "chrome", as GitHub's ubuntu runners carry
google-chrome), else Playwright's own Chromium if one is installed.

Exit 0 when every page ran, 1 when one did not, 2 when no browser could start.
"""
import argparse
import functools
import os
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "site" / "dist"
LIVE = "https://ancienttrees.app"

# The pages people land on, and every kind of map: the explore map over the
# United Kingdom is the 2026-11-06 crash, kept as its own line. The tree is the
# one uptime.yml fetches (lon_001); if it is ever retired, change both.
PAGES = [
    ("/", "home"),
    ("/explore", "explore map"),
    ("/explore#map=5.5/54.5/-3", "explore map over the United Kingdom"),
    ("/london", "city page"),
    ("/london/totteridge-yew", "tree page"),
    ("/united-kingdom", "country page"),
    ("/cities", "cities index"),
    ("/contribute", "contribute"),
    ("/nl/amsterdam", "translated city page"),
]
WIDTHS = [(1280, 800, "desktop"), (390, 844, "phone")]

# How long a page gets to do its late work before it is judged, and how long a
# stuck main thread is given to answer before it counts as hung.
SETTLE_S = 8
ANSWER_MS = 5000
LOAD_MS = 30000


class Pages(SimpleHTTPRequestHandler):
    """site/dist the way GitHub Pages serves it: /london is london.html or
    london/index.html, a missing file is 404.html."""

    def log_message(self, *a):
        pass

    def translate_path(self, path):
        clean = path.split("?", 1)[0].split("#", 1)[0]
        p = Path(super().translate_path(clean))
        if p.is_dir():
            if (p / "index.html").exists():
                return str(p / "index.html")
            if p.with_suffix(".html").exists():
                return str(p.with_suffix(".html"))
        if not p.exists() and not p.suffix and p.with_suffix(".html").exists():
            return str(p.with_suffix(".html"))
        return str(p)


def serve(dist):
    handler = functools.partial(Pages, directory=str(dist))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, "http://127.0.0.1:%d" % server.server_address[1]


def launch(pw):
    args = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--no-sandbox"]
    for kw in ({"channel": "chrome"}, {}):
        try:
            return pw.chromium.launch(args=args, **kw)
        except Exception as e:
            last = e
    raise last


def check(browser, base, path, size):
    """One page at one width: None when it ran, else what went wrong."""
    w, h, _ = size
    ctx = browser.new_context(viewport={"width": w, "height": h})
    page = ctx.new_page()
    origin = base.split("://", 1)[-1]
    crashed, errors = [], []
    page.on("crash", lambda *a: crashed.append(True))

    def on_error(e):
        stack = (getattr(e, "stack", "") or "") + " " + str(e)
        # Ours only: a page's own inline script, or a file served from it.
        # A failure inside the map library's WebGL start on a headless machine
        # is the machine, not the page (web_errors.py sees those as well).
        if origin in stack and "Failed to initialize WebGL" not in stack:
            errors.append(str(e).splitlines()[0][:200])
    page.on("pageerror", on_error)
    try:
        try:
            page.goto(base + path, wait_until="domcontentloaded", timeout=LOAD_MS)
        except Exception as e:
            if crashed:
                return "the tab crashed while loading"
            return "did not load (%s)" % str(e).splitlines()[0][:120]
        deadline = time.time() + SETTLE_S
        while time.time() < deadline:
            if crashed:
                return "the tab crashed (Chrome error code 5)"
            try:
                page.wait_for_function("true", timeout=ANSWER_MS)
            except Exception:
                if crashed:
                    return "the tab crashed (Chrome error code 5)"
                return "the page stopped answering (a script is stuck in a loop)"
            time.sleep(1)
        if crashed:
            return "the tab crashed (Chrome error code 5)"
        if errors:
            return "JavaScript error: " + errors[0]
        return None
    finally:
        try:
            ctx.close()
        except Exception:
            pass


def run(base):
    from playwright.sync_api import sync_playwright
    failures = []
    with sync_playwright() as pw:
        try:
            browser = launch(pw)
        except Exception as e:
            print("pagecheck: no browser could start (%s)" % str(e).splitlines()[0][:160])
            return 2
        for path, label in PAGES:
            for size in WIDTHS:
                what = check(browser, base, path, size)
                if what:
                    # A crashed renderer can take the browser down with it.
                    if not browser.is_connected():
                        browser = launch(pw)
                    again = check(browser, base, path, size)
                    if again:
                        failures.append((path, label, size[2], again))
                        print("  FAIL  %-34s %-7s %s" % (path, size[2], again))
                        if not browser.is_connected():
                            browser = launch(pw)
                        continue
                print("  ok    %-34s %s" % (path, size[2]))
        browser.close()
    if failures:
        print("\npagecheck: %d page(s) do not run in Chrome on %s:" % (len(failures), base))
        for path, label, width, what in failures:
            print("  %s (%s, %s): %s" % (path, label, width, what))
        return 1
    print("\npagecheck: all %d pages ran at both widths on %s" % (len(PAGES), base))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--live", action="store_true", help="check %s" % LIVE)
    ap.add_argument("--base", help="check this origin instead of site/dist")
    ap.add_argument("--dist", default=str(DIST), help="the built site to serve")
    a = ap.parse_args()
    if a.live or a.base:
        return run((a.base or LIVE).rstrip("/"))
    dist = Path(a.dist)
    if not (dist / "index.html").exists():
        print("pagecheck: no built site at %s (run astro build first)" % dist)
        return 1
    server, base = serve(dist)
    try:
        return run(base)
    finally:
        server.shutdown()


if __name__ == "__main__":
    sys.exit(main())
