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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from layout_rules import MIN_TAP, DRIFT_MAX, SAME, PHONE_W  # noqa: E402

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


# The same three rules the app is judged by (scripts/layout_rules.py), applied
# to the site. DRIFT is the one this adds: two things that should share a left
# edge and sit a few points apart. Hidde found it by eye twice in two days, on
# the phone header and then on /explore, and asked the obvious question: "kunnen
# we zorgen dat jij de alignment altijd van de website in de gaten houdt?"
#
# How it decides what "should share a left edge" means, because a naive version
# flags every page:
#   * A COLUMN is any element whose visible children are stacked vertically.
#     Anything laid out as a row (flex-row, multi-column grid) is not a column
#     and neither are its children compared, because horizontal offsets inside a
#     row ARE the layout.
#   * A column child's GUTTER is the leftmost place it puts ink: walk down until
#     you reach text, an image, a control, or a row, and take that edge.
#   * An element that paints a box (background or border) and is INSET from its
#     parent contributes its box edge, because a pill's box is what the eye
#     lines up. A full-bleed card contributes its text instead, for the same
#     reason: nobody sees its edges.
#   * Centred and right-aligned text is skipped outright. Its left edge is a
#     function of its length, not of a gutter.
#   * Anything inside a horizontal scroller is skipped, exactly as in the fit
#     check above.
# Two gutters in one column that differ by more than SAME and at most DRIFT_MAX
# are a fault. Bigger differences are deliberate insets and are left alone.
ALIGN_HARNESS = """<!doctype html><meta charset="utf-8"><title>align</title>
<style>html,body{margin:0}iframe{border:0;height:900px}</style>
<iframe id="f"></iframe><pre id="r">pending</pre>
<script>
var p = new URLSearchParams(location.search);
var f = document.getElementById('f');
f.style.width = (p.get('w') || '375') + 'px';
f.src = p.get('u');
f.addEventListener('load', function() {
  setTimeout(function() {
    try {
      var d = f.contentDocument, w = f.contentWindow;
      var HTML = 'http://www.w3.org/1999/xhtml', SAME = %(same)s, DRIFT = %(drift)s, TAP = %(tap)s;
      function cs(el) { return w.getComputedStyle(el); }
      function vis(el) {
        var s = cs(el);
        if (s.display === 'none' || s.visibility === 'hidden' || s.opacity === '0') return false;
        if (s.position === 'absolute' || s.position === 'fixed') return false;
        var r = el.getBoundingClientRect();
        return r.width >= 1 && r.height >= 1;
      }
      function inScroller(el, stop) {
        for (var q = el.parentElement; q && q !== stop && q !== d.body; q = q.parentElement) {
          var ox = cs(q).overflowX;
          if (ox === 'auto' || ox === 'scroll') return true;
        }
        return false;
      }
      function rowish(el) {
        var s = cs(el);
        if (s.display === 'flex' || s.display === 'inline-flex') return s.flexDirection.indexOf('row') === 0;
        if (s.display === 'grid' || s.display === 'inline-grid') return (s.gridTemplateColumns || 'none').split(' ').length > 1;
        return false;
      }
      function centred(el) { var a = cs(el).textAlign; return a === 'center' || a === 'right' || a === 'end'; }
      function contentLeft(el) {
        var r = el.getBoundingClientRect(), s = cs(el);
        return r.left + parseFloat(s.borderLeftWidth || 0) + parseFloat(s.paddingLeft || 0);
      }
      function paints(el) {
        var s = cs(el), bg = s.backgroundColor || '';
        var clear = bg === 'transparent' || /,\s*0\)$/.test(bg);
        return !clear || parseFloat(s.borderLeftWidth || 0) > 0;
      }
      // A box the reader can see lines up by its edge; everything else lines up
      // by its text. That is why a tinted fact table inside a text column is not
      // a fault (its border sits on the gutter) while a padded row with no
      // background is (nothing marks the 7px it steals).
      function blockish(el) {
        var disp = cs(el).display;
        if (disp.indexOf('inline') !== 0) return true;
        return paints(el) || !!LEAF[el.tagName.toUpperCase()];
      }
      function ownText(el) {
        for (var i = 0; i < el.childNodes.length; i++) {
          var n = el.childNodes[i];
          if (n.nodeType === 3 && n.textContent.trim()) return true;
        }
        return false;
      }
      var LEAF = {IMG:1, SVG:1, CANVAS:1, INPUT:1, BUTTON:1, TEXTAREA:1, SELECT:1, VIDEO:1, HR:1};
      function sel(el) {
        var c = (el.className && typeof el.className === 'string')
              ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
        return el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + c;
      }
      function gutter(el, stop) {
        var best = null, who = null;
        (function walk(n) {
          if (n.namespaceURI !== HTML || !vis(n) || inScroller(n, stop) || centred(n)) return;
          // An inline run's left edge is set by the words in front of it, not by
          // a gutter, so <strong> halfway down a paragraph is not a measurement.
          if (!blockish(n)) return;
          var stop = LEAF[n.tagName.toUpperCase()] || paints(n) || ownText(n) || !n.children.length;
          if (!stop) {
            // Rows are descended into as well. Only the MINIMUM is kept, so a
            // row hands back its leftmost item's ink, which is where the reader
            // sees it start. Stopping at the row's own padding box instead read
            // a multi-column grid as 7px left of its own cards.
            for (var i = 0; i < n.children.length; i++) walk(n.children[i]);
            return;
          }
          var L = paints(n) ? n.getBoundingClientRect().left : contentLeft(n);
          if (best === null || L < best - 0.01) { best = L; who = sel(n); }
        })(el);
        return best === null ? null : {left: best, who: who};
      }
      function stacked(kids) {
        for (var i = 1; i < kids.length; i++) {
          var a = kids[i - 1].getBoundingClientRect(), b = kids[i].getBoundingClientRect();
          if (b.top < a.bottom - 2) return false;
        }
        return true;
      }
      var drift = [], seen = {}, all = d.querySelectorAll('body *');
      for (var i = 0; i < all.length; i++) {
        var col = all[i];
        if (col.namespaceURI !== HTML || !vis(col) || rowish(col)) continue;
        if (LEAF[col.tagName.toUpperCase()] || inScroller(col, null)) continue;
        var kids = [];
        for (var j = 0; j < col.children.length; j++) {
          var k = col.children[j];
          if (k.namespaceURI === HTML && vis(k) && !centred(k)) kids.push(k);
        }
        if (kids.length < 2 || !stacked(kids)) continue;
        var gs = [];
        for (var m = 0; m < kids.length; m++) {
          var g = gutter(kids[m], col);
          if (g) gs.push({sel: sel(kids[m]), left: g.left, who: g.who});
        }
        for (var a2 = 0; a2 < gs.length; a2++) for (var b2 = a2 + 1; b2 < gs.length; b2++) {
          var gap = Math.abs(gs[a2].left - gs[b2].left);
          if (gap <= SAME || gap > DRIFT) continue;
          var key = sel(col) + '|' + Math.round(gs[a2].left) + '|' + Math.round(gs[b2].left);
          if (seen[key]) continue;
          seen[key] = 1;
          drift.push('in ' + sel(col) + ': ' + gs[a2].sel + ' starts at ' + Math.round(gs[a2].left * 10) / 10
                     + ' but ' + gs[b2].who + ' at ' + Math.round(gs[b2].left * 10) / 10
                     + ' (' + Math.round(gap * 10) / 10 + ' off)');
        }
      }
      // SMALL: a control the thumb cannot reliably hit. What counts as the
      // control is the TAP AREA and not the pixels, so an absolutely positioned
      // ::before or ::after that reaches outside the box counts: that is the
      // ordinary way to keep a small-looking pill hittable, and a check that
      // could not see it would push us to make things bigger than they should
      // look. Measured, not declared, so nobody can opt out with a class.
      function tap(el) {
        var r = el.getBoundingClientRect(), W = r.width, H = r.height;
        ['::before', '::after'].forEach(function(pe) {
          var s = w.getComputedStyle(el, pe);
          if (!s || s.content === 'none' || s.position !== 'absolute') return;
          function out(v) { var n = parseFloat(v); return isNaN(n) ? 0 : Math.max(0, -n); }
          var ww = r.width + out(s.left) + out(s.right);
          var hh = r.height + out(s.top) + out(s.bottom);
          var pw = parseFloat(s.width), ph = parseFloat(s.height);
          if (s.width !== 'auto' && !isNaN(pw)) ww = Math.max(ww, pw);
          if (s.height !== 'auto' && !isNaN(ph)) hh = Math.max(hh, ph);
          W = Math.max(W, ww); H = Math.max(H, hh);
        });
        return {w: W, h: H};
      }
      var small = [];
      d.querySelectorAll('button, [role=button], a, summary').forEach(function(el) {
        if (!vis(el) || !paints(el)) return;
        // Inside a closed <details> a control still has a box and no visitor can
        // reach it; measuring it reports the wrong number for the wrong reason.
        if (el.closest('details:not([open])') && el.tagName !== 'SUMMARY') return;
        // MapLibre's own attribution and zoom chrome is not ours to restyle.
        if (el.closest('.maplibregl-ctrl, .maplibregl-control-container')) return;
        var b = tap(el);
        if (b.w < TAP - SAME || b.h < TAP - SAME)
          small.push(sel(el) + ' ' + Math.round(b.w) + 'x' + Math.round(b.h));
      });
      document.getElementById('r').textContent = 'RESULT ' + JSON.stringify({
        drift: drift.slice(0, 6), nsmall: small.length, small: small.slice(0, 3)
      });
    } catch (e) {
      document.getElementById('r').textContent = 'RESULT ' + JSON.stringify({error: String(e)});
    }
  }, 2500);
});
</script>""" % {"same": SAME, "drift": DRIFT_MAX, "tap": MIN_TAP}


def drifts_at(chrome, base, page, width):
    """Does everything in a column start on the same line? See ALIGN_HARNESS."""
    url = "%s/__align.html?w=%d&u=%s" % (base, width, page)
    out = subprocess.run(
        [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
         "--window-size=%d,900" % (width + 60), "--virtual-time-budget=20000",
         "--dump-dom", url],
        capture_output=True, text=True, timeout=120).stdout
    m = re.search(r"RESULT (\{.*?\})</pre>", out, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&"))
    except Exception:
        return None


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


def check_basemap(dist):
    """The map is the product, and nothing was checking that it draws.

    Every layer we have asserts a CANVAS EXISTS ("map constructed"). None of
    them asks whether anything was painted into it, so if the style stopped
    resolving or the tile provider went dark, every visitor would get an empty
    grey rectangle with our pins floating on it and the whole pipeline would
    stay green. Found 2026-08-23 while restyling the map.

    Split deliberately, because a check that turns the deploy red for somebody
    else's outage is a check people learn to ignore:

      FAIL   our own style asset is missing or unparseable, or points at
             nothing. That is our bug and it must not ship.
      WARN   the tile host does not answer. That is not our bug, we cannot
             fix it in a deploy, and blocking the deploy would not help.
    """
    import json as _json
    import urllib.request as _u
    fails, warns = [], []
    style_path = dist / "assets" / "map-style.json"
    if not style_path.exists():
        return ["basemap: assets/map-style.json is not in the build"], warns
    try:
        style = _json.loads(style_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return ["basemap: assets/map-style.json does not parse (%s)" % exc], warns
    layers = style.get("layers") or []
    if len(layers) < 20:
        fails.append("basemap: the style has only %d layers, which is not a map" % len(layers))
    src = (style.get("sources") or {}).get("openmaptiles") or {}
    tilejson = src.get("url")
    if not tilejson:
        fails.append("basemap: the style names no vector tile source")
    if not src.get("attribution"):
        fails.append("basemap: the style carries no attribution, which OpenStreetMap's "
                     "licence requires")
    if not style.get("glyphs"):
        fails.append("basemap: the style names no glyph source, so every label would vanish")
    if tilejson:
        try:
            req = _u.Request(tilejson, headers={
                "User-Agent": "AncientTrees/1.0 (+https://ancienttrees.app) smoke"})
            with _u.urlopen(req, timeout=20) as fh:
                tj = _json.loads(fh.read().decode("utf-8"))
            if not tj.get("tiles"):
                warns.append("basemap: %s answered but names no tile urls" % tilejson)
        except Exception as exc:
            warns.append("basemap: the tile host did not answer (%s). Not our bug and not "
                         "a reason to block a deploy, but the map is blank while it lasts."
                         % exc)
    return fails, warns


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
    align_page = DIST / "__align.html"
    align_page.write_text(ALIGN_HARNESS, encoding="utf-8")

    failures = []
    base_fails, base_warns = check_basemap(DIST)
    failures += base_fails
    for w in base_warns:
        print("SMOKE WARN: %s" % w)

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

    # Does everything line up? Same three rules as the app (layout_rules.py),
    # at the two widths the site is actually read at.
    pages = [(f"/{city.name}", "city page"),
             ("/index.html", "homepage"),
             ("/explore.html", "explore"),
             (f"/{city.stem}/{tree.name}", "tree page"),
             ("/cities.html", "cities index"),
             ("/account.html", "account"),
             ("/netherlands.html", "country page")]
    small_seen = []
    for page, label in pages:
        for width in (PHONE_W, 1280):
            r = drifts_at(chrome, base, page, width)
            if r is None:
                failures.append(f"{label}: could not measure alignment at {width}px")
                continue
            if r.get("error"):
                failures.append(f"{label} at {width}px: alignment probe failed: {r['error']}")
                continue
            for d in r.get("drift", []):
                failures.append(f"DRIFT {label} at {width}px: {d}")
            if width == PHONE_W and r.get("nsmall"):
                small_seen.append((label, r["nsmall"], r.get("small", [])))

    # SMALL gates here as it does on the app (Hidde, 2026-08-20: "fix beide").
    # It was reported-only for a day, which was long enough to learn that the
    # list is four controls rather than the dozens the first count suggested:
    # the save heart at 26 points tall, the locate button at 40, the primary
    # pill at 41, and two false readings the check now avoids (a control inside
    # a closed menu, and MapLibre's own chrome, which is not ours to restyle).
    for label, n, examples in small_seen:
        failures.append("SMALL %s at %dpx: %d control(s) under %.0fx%.0f: %s"
                        % (label, PHONE_W, n, MIN_TAP, MIN_TAP, "; ".join(examples)))

    for page in (fit_page, align_page):
        try:
            page.unlink()
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
