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
import argparse
import json
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


HARNESS = """<!doctype html><meta charset="utf-8"><title>fit</title>
<style>html,body{margin:0}iframe{width:375px;height:812px;border:0}</style>
<iframe id="f"></iframe><pre id="r">pending</pre>
<script>
var p = new URLSearchParams(location.search);
var f = document.getElementById('f');
f.src = p.get('u');
f.addEventListener('load', function() {
  setTimeout(function() {
    try {
      var d = f.contentDocument, w = f.contentWindow;
      var vw = d.documentElement.clientWidth, out = [];
      // Running past the edge is only a fault when the visitor cannot get
      // there. A shelf with overflow-x:auto is SUPPOSED to hold cards beyond
      // the fold, which is how the homepage's card row tripped the first
      // version of this check on the day it was written.
      //
      // 'hidden' and 'clip' count too, and leaving them out cost a deploy on
      // 2026-08-20. MapLibre sizes its drawing canvas larger than the box it
      // draws into: on /explore at 375px the canvas measured 400 wide inside a
      // .map container of 375 with overflow:hidden. Nothing was off the screen,
      // the page's scrollWidth was exactly 375 and there was no horizontal
      // scroll, but the check called it a failure and turned the smoke run red.
      //
      // This does not weaken the check, which is the thing to be sure of before
      // touching it. An ancestor with overflow:hidden genuinely clips: its child
      // CANNOT appear past the viewport edge. And if that ancestor is itself too
      // wide, the loop still catches the ancestor on its own turn. So the nav bar
      // that ran 37 pixels off Hidde's screen, which is why this check exists,
      // would still be caught: it had no clipping ancestor.
      function inScroller(el) {
        for (var p = el.parentElement; p && p !== d.body; p = p.parentElement) {
          var ox = w.getComputedStyle(p).overflowX;
          if (ox === 'auto' || ox === 'scroll' || ox === 'hidden' || ox === 'clip') return true;
        }
        return false;
      }
      d.querySelectorAll('body *').forEach(function(el) {
        var r = el.getBoundingClientRect();
        if (!r.width && !r.height) return;
        var cs = w.getComputedStyle(el);
        if (cs.visibility === 'hidden' || cs.display === 'none') return;
        if (r.right > vw + 1 && !inScroller(el)) {
          out.push(el.tagName + '.' + String(el.className).slice(0, 40)
                   + ' right=' + Math.round(r.right));
        }
      });
      document.getElementById('r').textContent = 'RESULT ' + JSON.stringify({
        vw: vw, scroll: d.documentElement.scrollWidth, over: out.slice(0, 5)
      });
    } catch (e) {
      document.getElementById('r').textContent = 'RESULT ' + JSON.stringify({error: String(e)});
    }
  }, 1200);
});
</script>"""


def fits_at_375(chrome, base, page):
    """Does this page fit a phone, or does something run off the right edge?

    The twelfth ratchet check, and it exists because of a question Hidde asked
    on 2026-08-18 that had no good answer: "we hebben toch een qa proces? hoe
    kunnen we dit voorkomen in de toekomst?" We did, and none of its four
    layers could see this. The build checks structure, qa.py checks that
    elements EXIST, the fresh-eyes reviewer reads diffs, and the composition
    walk with real eyes runs every two weeks. Nothing measured whether a page
    FITS. So an account menu added to an already-tight bar pushed "Get the app"
    37 pixels off the screen, and every gate stayed green.

    Chrome's --dump-dom returns markup rather than a value, so the measuring
    happens inside a harness page that loads the target in a 375px iframe and
    writes its findings into its own DOM, which the dump then carries out.
    """
    url = "%s/__fit.html?u=%s" % (base, page)
    out = subprocess.run(
        [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
         "--window-size=420,900", "--virtual-time-budget=15000", "--dump-dom", url],
        capture_output=True, text=True, timeout=90).stdout
    m = re.search(r"RESULT (\{.*?\})</pre>", out, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&"))
    except Exception:
        return None


def main():
    global DIST
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", type=Path, default=None,
                        help="Override the dist directory (default: site/dist). "
                             "Used during the Astro migration to check site/dist-astro "
                             "without touching behavior against the real dist.")
    args = parser.parse_args()
    if args.dist:
        # Resolve to absolute: qa.py's --dist shipped this same flag with a
        # relative-path bug (a comparison elsewhere assumed DIST was
        # absolute and silently broke), so this file resolves() up front
        # rather than repeat that mistake.
        DIST = args.dist.resolve()

    chrome = find_chrome()
    if not chrome:
        print("SMOKE: no Chrome/Chromium found; cannot run. "
              "In CI this is a real failure, locally install Chrome.")
        return 1
    if not (DIST / "index.html").exists():
        print(f"SMOKE: no build under {DIST}, run (cd site && npx astro build) first")
        return 1

    # pick a served city and tree page from what the build produced
    city = next(p for p in sorted(DIST.glob("*.html"))
                if (DIST / p.stem).is_dir() and p.stem not in ("app", "plus"))
    tree = next(p for p in sorted((DIST / city.stem).glob("*.html"))
                if p.name != "index.html" and "oldest-tree" not in p.name)

    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]

    # Served only by this test, never shipped: after load it measures whether
    # the map paints over the prose section and writes the numbers into the
    # DOM, where dump_dom can read them. Exists because the 2026-08-06 explore
    # bug (prose added inside the fixed-height flex column, map overlapping the
    # text) was invisible to every string check while being obvious to eyes.
    GEOMETRY_PROBE = b"""<script>
setTimeout(function(){
  var m = document.getElementById('map');
  var p = document.querySelector('.explore-prose');
  var out = 'mapH=-1 proseOverlap=-1';
  if (m && p) {
    var a = m.getBoundingClientRect(), b = p.getBoundingClientRect();
    var oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
    var ox = Math.min(a.right, b.right) - Math.max(a.left, b.left);
    var overlap = (oy > 0 && ox > 0) ? Math.round(Math.min(oy, ox)) : 0;
    out = 'mapH=' + Math.round(a.height) + ' proseOverlap=' + overlap;
  }
  var d = document.createElement('div');
  d.id = 'smoke-geometry';
  d.textContent = out;
  document.body.appendChild(d);
}, 500);
</script>"""

    class Quiet(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(DIST), **kw)

        def log_message(self, *a):
            pass

        def do_GET(self):
            if self.path.split("?")[0].endswith("explore.html"):
                data = (DIST / "explore.html").read_bytes()
                if b"</body>" in data:
                    data = data.replace(b"</body>", GEOMETRY_PROBE + b"</body>", 1)
                else:
                    data += GEOMETRY_PROBE
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            super().do_GET()

    server = ThreadingHTTPServer(("127.0.0.1", port), Quiet)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{port}"

    checks = [
        (f"{base}/index.html", "homepage", [
            ('class="hero-bg"', "hero image"),
            ('id="city-q"', "search input"),
            ('class="ats-drop"', "shared search dropdown (one interaction, home and explore)"),
        ]),
        (f"{base}/{city.name}", f"city page ({city.stem})", [
            # The walk banner became a capsule on 2026-08-14, and the walking
            # routes left the web entirely on 2026-08-18 (Hidde: "die ik niet
            # beschikbaar wil maken op web"). What must exist on the map now is
            # the pill that says where the routes are, and the sheet the whole
            # phone layout hangs on: on 2026-08-17 that sheet shipped as CSS
            # with no markup and no script, which served a city page with no
            # map and no way to scroll, and every check including this one
            # stayed green.
            ('class="map-cta"', "the pill pointing at the app's walking routes"),
            ('id="sheet"', "the bottom sheet the phone layout is built on"),
            ('class="sheet-body"', "the sheet's inner scroller, without which the list cannot scroll"),
            ("atSheetFocus", "the sheet script"),
            ("maplibregl-canvas", "map canvas (JS ran, map constructed)"),
        ]),
        (f"{base}/{city.stem}/{tree.name}", f"tree page ({tree.stem})", [
            # Collect left the mobile web on Hidde's ruling of 2026-08-14
            # ("op mobiel totaal onlogisch... lekkermakertje voor de app");
            # the bar and the save heart are what must exist now.
            ('class="tree-bar"', "the hanging action bar (AllTrails funnel, 2026-08-14)"),
            ("save-btn", "the save heart (local, no account)"),
            ("Take me there", "directions, the primary action"),
            ("maplibregl-canvas", "map canvas (JS on this page executed)"),
        ]),
        (f"{base}/explore.html", "explore", [
            ("maplibregl-canvas", "map canvas"),
            ("exc-", "city chooser panel rendered"),
            ('class="ats-drop"', "shared search dropdown (one interaction, home and explore)"),
            ("proseOverlap=0", "map does not paint over the prose section (2026-08-06 bug class)"),
        ]),
        (f"{base}/netherlands.html", "country page (Contract G)", [
            ("maplibregl-canvas", "country map canvas (JS ran)"),
            ("ctry-row", "ranked city list rendered"),
            ("The oldest tree mapped in", "oldest-tree block"),
        ]),
        (f"{base}/contribute.html", "contribute", [
            ('id="suggest"', "native suggestion form"),
            ("rest/v1/submissions", "form posts to our backend"),
        ]),
        (f"{base}/app.html", "app page", [
            ('id="waitlist"', "waitlist form"),
        ]),
    ]

    # The harness lives in dist only while the test runs; it is written here
    # rather than shipped so it can never reach a visitor.
    fit_page = DIST / "__fit.html"
    fit_page.write_text(HARNESS, encoding="utf-8")

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

    # Does it fit a phone? One representative page per template that a visitor
    # actually lands on.
    for page, label in [(f"/{city.name}", "city page"),
                        ("/index.html", "homepage"),
                        ("/explore.html", "explore"),
                        (f"/{city.stem}/{tree.name}", "tree page"),
                        ("/cities.html", "cities index"),
                        ("/account.html", "account")]:
        r = fits_at_375(chrome, base, page)
        if r is None:
            failures.append(f"{label}: could not measure whether it fits 375px")
            continue
        if r.get("over"):
            failures.append("%s: %d element(s) run off the right edge at 375px: %s"
                            % (label, len(r["over"]), "; ".join(r["over"][:3])))
        elif r.get("scroll", 0) > r.get("vw", 375) + 1:
            failures.append("%s: page scrolls sideways at 375px (%dpx wide)"
                            % (label, r["scroll"]))

    try:
        fit_page.unlink()
    except OSError:
        pass
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
