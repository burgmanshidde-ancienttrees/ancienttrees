#!/usr/bin/env python3
"""Static site generator for ancienttrees.app.

Builds the four content layers from SEO_GEO_BLUEPRINT.md:
  Contract A  tree pages       /[city]/[tree-slug]
  Contract B  question pages   /[city]/oldest-tree
  Contract C  city pages       /[city]
  Contract D  collection pages /collections/[slug]
  Contract E  about page       /about

Pages are validated against the Layer 2 contracts (title length,
description length, schema presence, internal link minima) before
anything is written. A page that fails validation fails the build.

URLs are extensionless (london.html is served at /london by GitHub
Pages). Old /cities/[slug]/ URLs get redirect stubs.

Reads data/city-list.json, data/cities/*.json, data/collections/*.json.
Writes site/dist/. No dependencies beyond the Python 3.9 stdlib.

Usage: python3 scripts/build_site.py
"""

import json
import html
import math
import re
import shutil
import sys
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DIST = ROOT / "site" / "dist"
BASE_URL = "https://ancienttrees.app"
CUSTOM_DOMAIN = "ancienttrees.app"
CONTACT = "hello@ancienttrees.app"

# Paste the public submission form URL here (Tally, Google Forms, anything) and
# every contribution button on the site switches from a prefilled mailto to the
# form. Left empty, the site falls back to mailto so nothing is ever a dead end.
SUBMISSION_FORM_URL = ""

MAPLIBRE_JS = "https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"
MAPLIBRE_CSS = "https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css"
# OpenFreeMap: free vector tiles, no API key, commercial use permitted
MAP_STYLE = "https://tiles.openfreemap.org/styles/positron"

TITLE_MAX = 60
DESC_MAX = 155

CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --cream: #F7F4EE; --cream-dark: #EDE9DF; --ink: #1A1A14; --ink-mid: #4A4A3A;
  --ink-light: #8A8A7A; --moss: #3D5C1E; --moss-light: #EAF0E0;
  --serif: 'Playfair Display', Georgia, serif; --sans: 'Inter', system-ui, sans-serif;
  --header-h: 3.5rem;
}
html { scroll-behavior: smooth; }
body { background: var(--cream); color: var(--ink); font-family: var(--sans); font-size: 16px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
a { color: var(--moss); }

header.bar { position: fixed; top: 0; left: 0; right: 0; z-index: 50; height: var(--header-h); display: flex; align-items: center; justify-content: space-between; padding: 0 1.5rem; background: rgba(247,244,238,0.92); backdrop-filter: blur(8px); border-bottom: 1px solid var(--cream-dark); }
.bar-logo { font-family: var(--serif); font-size: 14px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink); text-decoration: none; }
.bar-links a { font-size: 13px; color: var(--ink-mid); text-decoration: none; margin-left: 1.25rem; }
.bar-links a:hover { color: var(--moss); }
.bar-links a.bar-cta { color: var(--moss); font-weight: 500; border: 1px solid var(--moss); border-radius: 3px; padding: 0.35rem 0.7rem; }
.bar-links a.bar-cta:hover { background: var(--moss); color: #fff; }
.city-card.soon:hover { opacity: 1; border-top-color: var(--moss); }
.city-card-cta { font-size: 12px; color: var(--moss); font-weight: 500; margin-top: 0.35rem; }
.path { border: 1px solid var(--cream-dark); border-radius: 6px; padding: 1.4rem 1.6rem; margin: 1.25rem 0; }
.path h2 { margin-top: 0; }
.path .go-btn { margin-top: 0.75rem; }

/* ---- City page: split layout, map is the stage ---- */
.split { display: flex; height: 100vh; padding-top: var(--header-h); }
.panel { width: 30rem; max-width: 45vw; height: 100%; overflow-y: auto; background: var(--cream); border-right: 1px solid var(--cream-dark); flex-shrink: 0; }
.panel-head { padding: 2rem 1.75rem 1.5rem; border-bottom: 1px solid var(--cream-dark); }
.eyebrow { font-size: 11px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; color: var(--ink-light); margin-bottom: 0.75rem; }
.panel-head h1 { font-family: var(--serif); font-size: 1.9rem; font-weight: 400; line-height: 1.2; margin-bottom: 0.75rem; }
.panel-head h1 em { font-style: italic; color: var(--moss); }
.lede { font-size: 14px; font-weight: 300; color: var(--ink-mid); line-height: 1.7; }
.notice { background: var(--moss-light); border-left: 3px solid var(--moss); padding: 0.7rem 1rem; font-size: 12px; color: var(--ink-mid); margin-top: 1rem; }
.stage { flex: 1; position: relative; }
.stage .map { position: absolute; inset: 0; width: 100%; height: 100%; }

.tree-card { padding: 1.75rem; border-bottom: 1px solid var(--cream-dark); cursor: pointer; border-left: 3px solid transparent; transition: border-color 0.2s, background 0.2s; }
.tree-card:hover { background: #fbf9f5; }
.tree-card.active { border-left-color: var(--moss); background: #fbf9f5; }
.tree-card-photo { margin: 0 0 1rem; border-radius: 8px; overflow: hidden; aspect-ratio: 3 / 2; background: var(--cream-dark); }
.tree-card-photo img { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform 0.4s ease; }
.tree-card:hover .tree-card-photo img { transform: scale(1.04); }
.tree-card-credit { font-size: 10px; color: var(--ink-light); margin: -0.6rem 0 0.85rem; }
.tree-card-top { display: flex; align-items: baseline; gap: 0.75rem; margin-bottom: 0.4rem; }
.tree-num { font-family: var(--serif); font-size: 1.1rem; color: var(--moss); flex-shrink: 0; width: 1.4rem; }
.tree-name { font-family: var(--serif); font-size: 1.35rem; font-weight: 400; line-height: 1.25; }
.tree-label { display: inline-block; font-size: 10px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink-mid); background: var(--cream-dark); border-radius: 2px; padding: 0.15rem 0.45rem; margin-left: 0.6rem; vertical-align: middle; white-space: nowrap; }
.tree-meta { font-size: 12px; color: var(--ink-light); margin: 0 0 0.6rem 2.15rem; }
/* Overview shows a teaser; the full story lives on the tree page. The whole
   text stays in the HTML so crawlers and AI engines still read it. */
.tree-story { font-size: 14px; font-weight: 300; color: var(--ink-mid); line-height: 1.7; margin: 0 0 0.7rem 2.15rem;
  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
.tree-more { font-size: 13px; font-weight: 500; margin: 0 0 0 2.15rem; }
.tree-more a { text-decoration: none; }
.tree-more a:hover { text-decoration: underline; }
.panel-foot { padding: 1.75rem; font-size: 13px; color: var(--ink-mid); }
.panel-foot h2 { font-family: var(--serif); font-size: 1.25rem; font-weight: 400; margin-bottom: 0.75rem; }
.panel-foot dt { font-weight: 500; margin-top: 1rem; }
.panel-foot dd { font-weight: 300; margin-top: 0.3rem; }
.panel-foot .suggest { border-top: 1px solid var(--cream-dark); margin-top: 1.5rem; padding-top: 1.25rem; color: var(--ink-light); }

/* ---- Content pages (tree, question, collection, about) ---- */
.content-page { max-width: 700px; margin: 0 auto; padding: calc(var(--header-h) + 2.25rem) 1.5rem 3.5rem; }
.crumbs { font-size: 12px; color: var(--ink-light); margin-bottom: 1.25rem; }
.crumbs a { color: var(--ink-light); text-decoration: none; }
.crumbs a:hover { color: var(--moss); }
.content-page h1 { font-family: var(--serif); font-size: 2.1rem; font-weight: 400; line-height: 1.2; margin-bottom: 1rem; }
.content-page h2 { font-family: var(--serif); font-size: 1.4rem; font-weight: 400; margin: 2.25rem 0 0.75rem; }
.content-page h3 { font-family: var(--serif); font-size: 1.15rem; font-weight: 400; margin: 1.5rem 0 0.35rem; }
.answer-first { font-size: 1.05rem; line-height: 1.75; margin-bottom: 1rem; }
.prose-block p { font-size: 15px; font-weight: 300; color: var(--ink-mid); line-height: 1.75; margin-bottom: 1rem; }
.facts { display: grid; grid-template-columns: max-content 1fr; gap: 0.4rem 1.5rem; background: var(--cream-dark); padding: 1.25rem 1.5rem; border-radius: 4px; margin: 1.5rem 0; }
.facts dt { font-size: 10px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink-light); padding-top: 3px; }
.facts dd { font-size: 13px; color: var(--ink); }
.tree-photo { margin: 1.5rem 0; }
.tree-photo img { width: 100%; display: block; border-radius: 4px; }
.tree-photo figcaption { font-size: 11px; color: var(--ink-light); margin-top: 0.45rem; }
.go-btn { display: inline-block; background: var(--moss); color: #fff; text-decoration: none; font-size: 14px; font-weight: 500; padding: 0.7rem 1.25rem; border-radius: 4px; margin: 0.25rem 0 0.5rem; }
.go-btn:hover { background: #2f4717; }
.go-note { font-size: 12px; color: var(--ink-light); margin-bottom: 1.5rem; }
.take-with-you { background: var(--cream-dark); border-radius: 4px; padding: 1.1rem 1.4rem; margin: 1.5rem 0; font-size: 13px; }
.take-with-you a { font-weight: 500; }
.map-embed { position: relative; height: 340px; border-radius: 4px; overflow: hidden; margin: 1.75rem 0; border: 1px solid var(--cream-dark); }
.map-embed .map { position: absolute; inset: 0; width: 100%; height: 100%; }
.faq dt { font-weight: 500; font-size: 15px; margin-top: 1.25rem; }
.faq dd { font-size: 14px; font-weight: 300; color: var(--ink-mid); margin-top: 0.35rem; line-height: 1.7; }
.cta { background: var(--moss-light); border-left: 3px solid var(--moss); padding: 1.1rem 1.4rem; border-radius: 0 4px 4px 0; margin: 2rem 0; font-size: 14px; }
.entry { margin-bottom: 1.6rem; }
.entry p { font-size: 14px; font-weight: 300; color: var(--ink-mid); line-height: 1.7; margin-top: 0.25rem; }
/* Image first, text second: a thumbnail leads the row where a photo exists. */
.entry.has-thumb { display: grid; grid-template-columns: 96px 1fr; gap: 1rem; align-items: start; }
.entry-thumb { border-radius: 6px; overflow: hidden; aspect-ratio: 1 / 1; background: var(--cream-dark); }
.entry-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
.entry-body h3 { margin-top: 0; }
@media (max-width: 800px) {
  .entry.has-thumb { grid-template-columns: 72px 1fr; gap: 0.8rem; }
}
.suggest { font-size: 13px; color: var(--ink-light); border-top: 1px solid var(--cream-dark); padding-top: 1.25rem; margin-top: 2.5rem; }
ul.link-list { list-style: none; }
ul.link-list li { margin-bottom: 0.5rem; font-size: 14px; }

/* ---- Homepage ---- */
.home-hero { position: relative; height: 72vh; min-height: 420px; margin-top: var(--header-h); }
.home-hero .map { position: absolute; inset: 0; width: 100%; height: 100%; }
.hero-overlay { position: absolute; top: 1.5rem; left: 1.5rem; z-index: 10; background: rgba(247,244,238,0.95); backdrop-filter: blur(8px); border: 1px solid var(--cream-dark); border-radius: 4px; padding: 1.75rem 2rem; max-width: 26rem; box-shadow: 0 4px 24px rgba(26,26,20,0.08); }
.hero-overlay h1 { font-family: var(--serif); font-size: 1.75rem; font-weight: 400; line-height: 1.25; margin-bottom: 0.6rem; }
.hero-overlay h1 em { font-style: italic; color: var(--moss); }
.hero-overlay p { font-size: 13px; font-weight: 300; color: var(--ink-mid); line-height: 1.65; }
.page { max-width: 1100px; margin: 0 auto; padding: 3rem 2.5rem; }
.section-heading { font-family: var(--serif); font-size: 1.75rem; font-weight: 400; margin-bottom: 1.5rem; }
.prose { font-size: 15px; font-weight: 300; color: var(--ink-mid); line-height: 1.75; max-width: 640px; margin-bottom: 2.5rem; }
.city-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 2px; background: var(--cream-dark); border: 1px solid var(--cream-dark); margin-bottom: 3rem; }
.city-card { background: var(--cream); padding: 1.5rem; text-decoration: none; border-top: 2px solid transparent; transition: border-top-color 0.2s; }
.city-card:hover { border-top-color: var(--moss); }
.city-card-name { font-family: var(--serif); font-size: 1.25rem; color: var(--ink); margin-bottom: 0.25rem; }
.city-card-meta { font-size: 12px; color: var(--ink-light); }
.city-card.soon { opacity: 0.55; }

footer { border-top: 1px solid var(--cream-dark); padding: 2rem 2.5rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }
.footer-logo { font-family: var(--serif); font-size: 14px; letter-spacing: 0.08em; text-transform: uppercase; }
.footer-links { font-size: 12px; }
.footer-links a { color: var(--ink-mid); text-decoration: none; margin-right: 1rem; }
.footer-note { font-size: 12px; color: var(--ink-light); }

/* ---- Markers ---- */
.pin { width: 30px; height: 30px; border-radius: 50%; background: var(--moss); border: 2px solid #fff; box-shadow: 0 2px 8px rgba(26,26,20,0.35); cursor: pointer; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 12px; font-weight: 600; font-family: var(--sans); transition: transform 0.15s, background 0.15s; }
.pin:hover { transform: scale(1.15); }
.pin.active { background: var(--ink); transform: scale(1.25); z-index: 5; }
.maplibregl-popup-content { font-family: var(--sans); font-size: 13px; padding: 0.75rem 1rem; border-radius: 4px; }
.maplibregl-popup-content strong { font-family: var(--serif); font-size: 15px; font-weight: 400; }

@media (max-width: 800px) {
  .split { flex-direction: column-reverse; height: auto; }
  .panel { width: 100%; max-width: none; height: auto; overflow: visible; border-right: none; }
  /* Smaller map on phones: the list is what people scan, the map is context. */
  .stage { position: sticky; top: var(--header-h); height: 32vh; min-height: 200px; z-index: 5; }
  .tree-card { padding: 1.25rem 1.1rem; }
  .tree-meta, .tree-story, .tree-more { margin-left: 0; }
  .tree-card-photo { aspect-ratio: 16 / 10; }
  .bar-links a { margin-left: 0.7rem; font-size: 12px; }
  .bar-links a.bar-cta { padding: 0.3rem 0.5rem; }
  /* Keep the bar on one line on phones: secondary links stay reachable from
     the homepage and from the pages themselves. */
  header.bar { flex-wrap: nowrap; padding: 0 1rem; }
  .bar-logo { font-size: 12px; white-space: nowrap; }
  .bar-links { display: flex; align-items: center; white-space: nowrap; }
  .bar-links a.bar-secondary { display: none; }
  /* Get to the trees faster: the intro is still fully in the HTML. */
  .panel-head .lede { display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden; }
  .panel-head { padding: 1.25rem 1.1rem 1rem; }
  .panel-head h1 { font-size: 1.6rem; }
  .home-hero { height: 60vh; }
  .hero-overlay { left: 1rem; right: 1rem; top: 1rem; max-width: none; padding: 1.25rem 1.5rem; }
  .page { padding: 2rem 1.5rem; }
  footer { flex-direction: column; text-align: center; }
}
"""

PAGE_SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="google-site-verification" content="uVA_hyHOJQWM3wH90g2QwP5qw2pk1WlPrtZ-lZKq2Hc">
<title>%%TITLE%%</title>
<meta name="description" content="%%DESCRIPTION%%">
<link rel="canonical" href="%%CANONICAL%%">
<meta property="og:title" content="%%TITLE%%">
<meta property="og:description" content="%%DESCRIPTION%%">
<meta property="og:type" content="%%OGTYPE%%">
<meta property="og:url" content="%%CANONICAL%%">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="%%ROOTPATH%%assets/style.css">
%%HEAD_EXTRA%%
</head>
<body>
<header class="bar">
  <a href="%%ROOTPATH%%" class="bar-logo">Ancient Trees</a>
  <nav class="bar-links">
    <a href="%%ROOTPATH%%#cities">Cities</a>
    <a href="%%ROOTPATH%%species" class="bar-secondary">Species</a>
    <a href="%%ROOTPATH%%collections" class="bar-secondary">Collections</a>
    <a href="%%ROOTPATH%%contribute" class="bar-cta">Map your city</a>
  </nav>
</header>
%%BODY%%
%%FOOTER%%
%%SCRIPTS%%
</body>
</html>
"""

FOOTER = """
<footer>
  <span class="footer-logo">Ancient Trees</span>
  <span class="footer-links"><a href="%%ROOTPATH%%collections">Collections</a></span>
  <span class="footer-note">&copy; %%YEAR%% Ancient Trees, ancienttrees.app. Map &copy; OpenFreeMap, OpenMapTiles, OpenStreetMap contributors.</span>
</footer>
"""

ERRORS = []


def esc(s):
    return html.escape(str(s), quote=True)


def slugify(name):
    s = name.lower().replace("'", "").replace("’", "")
    if s.startswith("the "):
        s = s[4:]
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def age_token(tree):
    m = re.match(r"([\d,]+\+?)", tree.get("age_estimate", ""))
    return m.group(1) if m else str(tree.get("age_min", ""))


def species_common(tree):
    return tree.get("species", "").split(" (")[0]


def meta_from_story(story):
    """Build a meta description from the story's opening sentences, max DESC_MAX."""
    sentences = re.split(r"(?<=[.!?]) ", story)
    out = ""
    for s in sentences:
        if out and len(out) + 1 + len(s) > DESC_MAX:
            break
        out = (out + " " + s).strip()
        if len(out) > DESC_MAX:
            out = out[:DESC_MAX].rsplit(" ", 1)[0].rstrip(",.;:")
            break
    return out


def fit_title(candidates, page):
    for c in candidates:
        if len(c) <= TITLE_MAX:
            return c
    ERRORS.append(f"{page}: no title candidate fits {TITLE_MAX} chars: {candidates[-1]!r}")
    return candidates[-1]


def haversine(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def site_graph():
    """Site-level WebSite + Person schema, on every page.

    About page (Contract E) is deferred by Hidde's decision 2026-07-19;
    when it ships, point the Person url at /about and add sameAs.
    """
    return [
        {"@type": "WebSite", "name": "Ancient Trees", "url": BASE_URL},
        {"@type": "Person", "name": "Hidde", "url": BASE_URL},
    ]


def breadcrumb_schema(items):
    elements = []
    for i, (name, url) in enumerate(items, 1):
        el = {"@type": "ListItem", "position": i, "name": name}
        if url:
            el["item"] = url
        elements.append(el)
    return {"@type": "BreadcrumbList", "itemListElement": elements}


def breadcrumb_html(items, rootpath):
    parts = []
    for name, url in items:
        if url:
            rel = url.replace(BASE_URL + "/", rootpath) if url != BASE_URL else rootpath
            rel = rel or rootpath or "."
            parts.append(f'<a href="{rel if rel else "."}">{esc(name)}</a>')
        else:
            parts.append(esc(name))
    return '<nav class="crumbs">' + " &rsaquo; ".join(parts) + "</nav>"


def ld_script(graph):
    payload = {"@context": "https://schema.org", "@graph": graph}
    return f'<script type="application/ld+json">{json.dumps(payload)}</script>'


def map_head():
    return f'<link rel="stylesheet" href="{MAPLIBRE_CSS}">'


def single_pin_script(lat, lng, label="1"):
    return f"""
<script src="{MAPLIBRE_JS}"></script>
<script>
var map = new maplibregl.Map({{
  container: 'map', style: '{MAP_STYLE}',
  center: [{lng}, {lat}], zoom: 14.5, scrollZoom: false
}});
map.addControl(new maplibregl.NavigationControl());
map.on('load', function() {{ map.resize(); }});
var el = document.createElement('div');
el.className = 'pin';
el.textContent = '{label}';
new maplibregl.Marker({{ element: el }}).setLngLat([{lng}, {lat}]).addTo(map);
</script>
"""


def city_map_script(markers, center):
    data = json.dumps(markers)
    return f"""
<script src="{MAPLIBRE_JS}"></script>
<script>
var markers = {data};
var map = new maplibregl.Map({{
  container: 'map',
  style: '{MAP_STYLE}',
  center: [{center[1]}, {center[0]}],
  zoom: 10.5,
  scrollZoom: true
}});
map.addControl(new maplibregl.NavigationControl());
map.addControl(new maplibregl.FullscreenControl());
map.on('load', function() {{ map.resize(); }});
new ResizeObserver(function() {{ map.resize(); }}).observe(document.getElementById('map'));

var pins = [];
var activeIdx = -1;

function setActive(idx, fly, scroll) {{
  if (activeIdx >= 0) {{
    pins[activeIdx].classList.remove('active');
    document.getElementById('tree-' + (activeIdx + 1)).classList.remove('active');
  }}
  activeIdx = idx;
  var m = markers[idx];
  pins[idx].classList.add('active');
  var card = document.getElementById('tree-' + (idx + 1));
  card.classList.add('active');
  if (scroll) {{ card.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }}); }}
  if (fly) {{ map.flyTo({{ center: [m.lng, m.lat], zoom: 14.5, duration: 1200 }}); }}
}}

var bounds = new maplibregl.LngLatBounds();
markers.forEach(function(m, idx) {{
  var el = document.createElement('div');
  el.className = 'pin';
  el.textContent = m.label;
  el.addEventListener('click', function(e) {{
    e.stopPropagation();
    setActive(idx, true, true);
  }});
  new maplibregl.Marker({{ element: el }}).setLngLat([m.lng, m.lat]).addTo(map);
  pins.push(el);
  bounds.extend([m.lng, m.lat]);
}});
if (markers.length > 1) {{ map.fitBounds(bounds, {{ padding: 70, maxZoom: 13 }}); }}

document.querySelectorAll('.tree-card').forEach(function(card, idx) {{
  card.addEventListener('click', function(e) {{
    if (e.target.closest('a')) {{ return; }}
    setActive(idx, true, false);
  }});
}});
</script>
"""


def home_map_script(markers):
    data = json.dumps(markers)
    return f"""
<script src="{MAPLIBRE_JS}"></script>
<script>
var markers = {data};
var map = new maplibregl.Map({{
  container: 'map',
  style: '{MAP_STYLE}',
  center: [10, 35],
  zoom: 1.7,
  scrollZoom: false
}});
map.addControl(new maplibregl.NavigationControl());
map.on('load', function() {{ map.resize(); }});
new ResizeObserver(function() {{ map.resize(); }}).observe(document.getElementById('map'));
markers.forEach(function(m) {{
  var el = document.createElement('div');
  el.className = 'pin';
  el.textContent = m.label;
  el.addEventListener('click', function() {{
    map.flyTo({{ center: [m.lng, m.lat], zoom: 9, duration: 1400 }});
    setTimeout(function() {{ window.location.href = m.url; }}, 1500);
  }});
  new maplibregl.Marker({{ element: el }}).setLngLat([m.lng, m.lat]).addTo(map);
}});
</script>
"""


def render_page(title, description, canonical, body, head_extra="", scripts="",
                rootpath="", footer=True, og_type="article"):
    if len(title) > TITLE_MAX:
        ERRORS.append(f"{canonical}: title exceeds {TITLE_MAX} chars ({len(title)}): {title!r}")
    if len(description) > DESC_MAX:
        ERRORS.append(f"{canonical}: description exceeds {DESC_MAX} chars ({len(description)})")
    footer_html = FOOTER.replace("%%ROOTPATH%%", rootpath) if footer else ""
    return (
        PAGE_SHELL
        .replace("%%TITLE%%", esc(title))
        .replace("%%DESCRIPTION%%", esc(description))
        .replace("%%CANONICAL%%", canonical)
        .replace("%%OGTYPE%%", og_type)
        .replace("%%ROOTPATH%%", rootpath)
        .replace("%%HEAD_EXTRA%%", head_extra)
        .replace("%%BODY%%", body)
        .replace("%%FOOTER%%", footer_html)
        .replace("%%SCRIPTS%%", scripts)
        .replace("%%YEAR%%", str(date.today().year))
    )


def check_links(page, count, minimum):
    if count < minimum:
        ERRORS.append(f"{page}: {count} internal links, contract minimum is {minimum}")


def tree_is_renderable(tree):
    loc = tree.get("location") or {}
    return bool(tree.get("story")) and loc.get("latitude") is not None and loc.get("longitude") is not None


SUBMIT_TEMPLATES = {
    "city": (
        "I want to map my city",
        "Which city?%0D%0A%0D%0A"
        "The trees you would put on its list (as many as you know, a name and rough location each is plenty):%0D%0A"
        "1.%0D%0A2.%0D%0A3.%0D%0A%0D%0A"
        "Anything that makes this city's trees particular? (a species that thrives here, a park, a local habit)%0D%0A%0D%0A"
        "How do you know the city? (you live there, you grew up there, you walk it often)%0D%0A%0D%0A"
        "Your name, for the credit:%0D%0A",
    ),
    "tree": (
        "A tree you are missing",
        "Tree name or description:%0D%0A%0D%0A"
        "City:%0D%0A%0D%0A"
        "Where exactly is it? (street, park, or a Google Maps link, the more precise the better)%0D%0A%0D%0A"
        "Why is it remarkable? (age, size, story, anything you know)%0D%0A%0D%0A"
        "How do you know about it? (link, book, local knowledge)%0D%0A%0D%0A"
        "Photo: attach it if you took it yourself%0D%0A%0D%0A"
        "Your name, for the credit:%0D%0A",
    ),
    "correction": (
        "A correction",
        "Which page or tree?%0D%0A%0D%0A"
        "What is wrong?%0D%0A%0D%0A"
        "How do you know? (a link or local knowledge both count)%0D%0A",
    ),
}


def submit_link(kind):
    """Where a contribution button points.

    One constant at the top of this file flips every button on the site from a
    prefilled mailto to the hosted form, so switching over is a one-line change.
    """
    if SUBMISSION_FORM_URL:
        return SUBMISSION_FORM_URL
    subject, body = SUBMIT_TEMPLATES[kind]
    return f"mailto:{CONTACT}?subject={subject}&amp;body={body}"


def usable_photo(tree):
    """Return the photo dict if it has a URL, license and attribution and is
    cleared for display; otherwise None. One gate for every page type."""
    photo = tree.get("photo") or {}
    if (photo.get("url") and photo.get("license") and photo.get("attribution")
            and photo.get("status") in ("approved", "found_needs_check")):
        return photo
    return None


def load_cities():
    city_list = json.loads((DATA / "city-list.json").read_text())["cities"]
    for entry in city_list:
        f = DATA / "cities" / f"{entry['slug']}.json"
        entry["data"] = json.loads(f.read_text()) if f.exists() else None
    return city_list


def load_collections():
    coll_dir = DATA / "collections"
    if not coll_dir.exists():
        return []
    return [json.loads(f.read_text()) for f in sorted(coll_dir.glob("*.json"))]


def load_species_intros():
    """Hand-written intros keyed by common_name. A species page can't publish
    without one (Contract F, P3)."""
    sp_dir = DATA / "species"
    if not sp_dir.exists():
        return {}
    out = {}
    for f in sorted(sp_dir.glob("*.json")):
        s = json.loads(f.read_text())
        out[s["common_name"]] = s
    return out


def group_trees_by_species(renderable):
    """common_name -> list of (city_entry, tree), preserving city order then age."""
    groups = {}
    for entry in renderable:
        trees = [t for t in entry["data"]["trees"] if tree_is_renderable(t)]
        for t in trees:
            groups.setdefault(species_common(t), []).append((entry, t))
    return groups


SPECIES_MIN_TREES = 3


def oldest_tree(trees):
    return max(trees, key=lambda t: t.get("age_max") or 0)


def curation_notice(status):
    if status in ("curated", "published"):
        return ""
    return (
        '<div class="notice">This page is awaiting curation. Facts have been researched '
        "and cross-referenced, but the final human review is still in progress.</div>"
    )


# ---------------------------------------------------------------- tree pages

def build_tree_page(city_entry, tree, all_trees, collections, pages, species_pages=None):
    species_pages = species_pages or {}
    city_data = city_entry["data"]
    city = city_data["city"]
    country = city_data["country"]
    cslug = city_entry["slug"]
    tslug = slugify(tree["name"])
    loc = tree["location"]
    age = age_token(tree)
    canonical = f"{BASE_URL}/{cslug}/{tslug}"
    rootpath = "../"

    title = fit_title([
        f"{tree['name']}: {age} Year Old {species_common(tree)} in {city}",
        f"{tree['name']}: {age} Year Old Tree in {city}",
        f"{tree['name']} in {city}",
        tree["name"],
    ], canonical)
    description = meta_from_story(tree["story"])

    others = [t for t in all_trees if t["id"] != tree["id"]]
    others.sort(key=lambda t: haversine(
        (loc["latitude"], loc["longitude"]),
        (t["location"]["latitude"], t["location"]["longitude"])))
    nearby = others[:3]

    crumb_items = [
        ("Home", BASE_URL),
        (country, None),
        (city, f"{BASE_URL}/{cslug}"),
        (tree["name"], None),
    ]

    photo = usable_photo(tree)
    photo_html = ""
    og_image = ""
    if photo:
        photo_html = f"""
  <figure class="tree-photo">
    <img src="{esc(photo['url'])}" alt="{esc(tree['name'])}" loading="lazy">
    <figcaption>Photo: {esc(photo['attribution'])} ({esc(photo['license'])})</figcaption>
  </figure>"""
        og_image = f'\n<meta property="og:image" content="{esc(photo["url"])}">'

    label = f'<span class="tree-label">{esc(tree["label"])}</span>' if tree.get("label") else ""
    facts = f"""
<dl class="facts">
  <dt>Species</dt><dd>{esc(tree.get('species', ''))}</dd>
  <dt>Age estimate</dt><dd>{esc(tree.get('age_estimate', 'unknown'))}</dd>
  <dt>Location</dt><dd>{esc(loc.get('address', ''))} ({esc(loc.get('neighbourhood', ''))})</dd>
  <dt>Access</dt><dd>{esc(tree.get('access', ''))}</dd>
  <dt>Getting there</dt><dd>{esc(tree.get('transport', ''))}</dd>
</dl>"""

    nearby_html = "".join(
        f'<li><a href="{slugify(t["name"])}">{esc(t["name"])}, '
        f'{esc(t.get("age_estimate", ""))} ({esc(t["location"].get("neighbourhood", ""))})</a></li>'
        for t in nearby
    )

    sp_common = species_common(tree)
    sp_slug = species_pages.get(sp_common)
    species_line = (
        f' It is a {esc(sp_common)}; see <a href="../species/{sp_slug}">every {esc(sp_common.lower())} on the site</a>.'
        if sp_slug else ""
    )

    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>{esc(tree['name'])}{label}</h1>
  {curation_notice(city_data.get('status'))}
  {photo_html}
  {facts}
  <div class="prose-block"><p>{esc(tree['story'])}</p></div>
  <div class="map-embed"><div id="map" class="map"></div></div>
  <a class="go-btn" href="https://www.google.com/maps/dir/?api=1&amp;destination={loc['latitude']},{loc['longitude']}" target="_blank" rel="noopener">Take me there</a>
  <p class="go-note">Opens directions in your maps app. {esc(tree.get('transport', ''))}</p>
  <h2>Trees nearby</h2>
  <ul class="link-list">{nearby_html}</ul>
  <div class="cta">Curious what else is standing in {esc(city)}? See <a href="../{cslug}">all 10 remarkable ancient trees in {esc(city)}</a> or find out <a href="oldest-tree">what the oldest tree in {esc(city)} is</a>.{species_line}</div>
  <p class="suggest">Something wrong on this page, or do you have an openly licensed photo of this tree? <a href="{submit_link('correction')}">Tell us</a>. Corrections are checked and credited.</p>
</main>
"""

    graph = site_graph() + [
        {
            "@type": "TouristAttraction",
            "name": tree["name"],
            "description": tree["story"][:300],
            "isAccessibleForFree": "free" in tree.get("access", "").lower(),
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": loc["latitude"],
                "longitude": loc["longitude"],
            },
        },
        breadcrumb_schema(crumb_items),
    ]
    head_extra = map_head() + og_image + "\n" + ld_script(graph)
    scripts = single_pin_script(loc["latitude"], loc["longitude"])

    check_links(canonical, 2 + len(nearby), 4)

    page = render_page(title, description, canonical, body, head_extra, scripts, rootpath)
    pages.append((f"{cslug}/{tslug}.html", page, canonical))
    return tslug


# ------------------------------------------------------------ question pages

def build_question_page(city_entry, collections, pages):
    city_data = city_entry["data"]
    city = city_data["city"]
    country = city_data["country"]
    cslug = city_entry["slug"]
    trees = [t for t in city_data["trees"] if tree_is_renderable(t)]
    old = oldest_tree(trees)
    oslug = slugify(old["name"])
    loc = old["location"]
    age = age_token(old)
    canonical = f"{BASE_URL}/{cslug}/oldest-tree"
    rootpath = "../"
    question = f"What is the oldest tree in {city}?"

    title = fit_title([
        f"What Is the Oldest Tree in {city}? ({old['name']}, {age} Years)",
        f"What Is the Oldest Tree in {city}? ({age} Years Old)",
        f"What Is the Oldest Tree in {city}?",
    ], canonical)
    description = city_data.get("question_meta") or city_data.get("question_answer", "")[:DESC_MAX]
    answer = city_data.get("question_answer", "")
    context = city_data.get("question_context", "")
    if not answer or not context:
        ERRORS.append(f"{canonical}: question_answer and question_context must be written per city (Contract B)")

    crumb_items = [
        ("Home", BASE_URL),
        (country, None),
        (city, f"{BASE_URL}/{cslug}"),
        ("Oldest tree", None),
    ]

    related = [f for f in city_data.get("faq", []) if "oldest" not in f["q"].lower()][:3]
    faq_entities = [{
        "@type": "Question", "name": question,
        "acceptedAnswer": {"@type": "Answer", "text": answer},
    }] + [{
        "@type": "Question", "name": f["q"],
        "acceptedAnswer": {"@type": "Answer", "text": f["a"]},
    } for f in related]

    coll = collections[0] if collections else None
    coll_link = (
        f'<p class="prose-block">The yew, the oaks and their peers across other cities are collected in '
        f'<a href="../collections/{coll["slug"]}">{esc(coll["title"])}</a>.</p>'
        if coll else ""
    )

    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>{esc(question)}</h1>
  <p class="answer-first">{esc(answer)}</p>
  {curation_notice(city_data.get('status'))}
  <div class="map-embed"><div id="map" class="map"></div></div>
  <div class="prose-block"><p>{esc(context)}</p></div>
  <div class="cta">Read <a href="{oslug}">the full story of {esc(old['name'])}</a>, or see <a href="../{cslug}">all 10 remarkable ancient trees in {esc(city)}</a>.</div>
  {coll_link}
</main>
"""

    graph = site_graph() + [
        {"@type": "FAQPage", "mainEntity": faq_entities},
        breadcrumb_schema(crumb_items),
    ]
    head_extra = map_head() + "\n" + ld_script(graph)
    scripts = single_pin_script(loc["latitude"], loc["longitude"])

    link_count = 2 + (1 if coll else 0)
    check_links(canonical, link_count, 3)

    page = render_page(title, description, canonical, body, head_extra, scripts, rootpath)
    pages.append((f"{cslug}/oldest-tree.html", page, canonical))


# ---------------------------------------------------------------- city pages

def build_city_page(entry, tree_slugs, collections, pages, other_cities=()):
    city_data = entry["data"]
    city = city_data["city"]
    country = city_data["country"]
    slug = entry["slug"]
    trees = [t for t in city_data.get("trees", []) if tree_is_renderable(t)]
    if not trees:
        return None
    canonical = f"{BASE_URL}/{slug}"
    rootpath = "./"

    title = fit_title([
        f"Ancient Trees in {city}: 10 Remarkable Trees Worth Visiting",
        f"Ancient Trees in {city}: 10 Trees Worth Visiting",
        f"Ancient Trees in {city}",
    ], canonical)
    description = city_data.get("meta_description") or (
        f"The oldest and most remarkable trees in {city}, {country}: "
        f"verified locations, real stories, and how to reach each one."
    )
    intro = city_data.get("intro")
    if not intro:
        ERRORS.append(f"{canonical}: city intro (60-100 words, unique) is required by Contract C")
        intro = ""

    crumb_items = [("Home", BASE_URL), (country, None), (city, None)]

    cards = []
    markers = []
    for i, t in enumerate(trees, 1):
        loc = t["location"]
        tslug = tree_slugs[t["id"]]
        label = f'<span class="tree-label">{esc(t["label"])}</span>' if t.get("label") else ""
        cphoto = usable_photo(t)
        photo_block = ""
        if cphoto:
            photo_block = f"""
      <div class="tree-card-photo"><img src="{esc(cphoto['url'])}" alt="{esc(t['name'])}" loading="lazy"></div>
      <p class="tree-card-credit">Photo: {esc(cphoto['attribution'])} ({esc(cphoto['license'])})</p>"""
        cards.append(f"""
    <article class="tree-card" id="tree-{i}">
      {photo_block}
      <div class="tree-card-top">
        <span class="tree-num">{i}</span>
        <h2 class="tree-name">{esc(t['name'])}{label}</h2>
      </div>
      <p class="tree-meta">{esc(t.get('species', ''))} &middot; {esc(t.get('age_estimate', 'age unknown'))} &middot; {esc(loc.get('neighbourhood', ''))}</p>""")
        cards[-1] += f"""
      <p class="tree-story">{esc(t['story'])}</p>
      <p class="tree-more"><a href="{slug}/{tslug}">Read more and get directions &rarr;</a></p>
    </article>"""
        markers.append({"lat": loc["latitude"], "lng": loc["longitude"], "label": str(i)})

    faq = city_data.get("faq", [])
    if not faq:
        ERRORS.append(f"{canonical}: FAQ block (3-4 real questions) is required by Contract C")
    faq_html = "".join(f"<dt>{esc(f['q'])}</dt><dd>{esc(f['a'])}</dd>" for f in faq)

    coll = collections[0] if collections else None
    coll_link_html = (
        f'<dt>More like this</dt><dd>Several of these trees also appear in '
        f'<a href="collections/{coll["slug"]}">{esc(coll["title"])}</a>.</dd>'
        if coll else ""
    )
    others_html = " &middot; ".join(
        f'<a href="./{c["slug"]}">Ancient trees in {esc(c["city"])}</a>'
        for c in other_cities
    )
    more_cities_html = (
        f'<dt>More cities</dt><dd>{others_html}</dd>' if others_html else ""
    )

    panel_foot = f"""
    <div class="panel-foot">
      <div class="take-with-you">
        <strong>Going there?</strong> <a href="{slug}.gpx" download>Download all {len(trees)} trees</a> as a map file and open it in Google Maps, Organic Maps or any hiking app. Works offline, no app needed.
      </div>
      <h2>Frequently asked</h2>
      <dl class="faq">
        {faq_html}
        <dt>More on the oldest tree</dt>
        <dd><a href="{slug}/oldest-tree">What is the oldest tree in {esc(city)}?</a> The full answer, with map and directions.</dd>
        {coll_link_html}
        {more_cities_html}
      </dl>
      <p class="suggest">Know a tree that belongs on this list? <a href="{submit_link('tree')}">Send it in</a>. Suggestions feed curation; the list itself stays editorial.</p>
    </div>"""

    graph = site_graph() + [
        {
            "@type": "ItemList",
            "name": title,
            "itemListElement": [
                {
                    "@type": "ListItem", "position": i,
                    "name": t["name"],
                    "url": f"{BASE_URL}/{slug}/{tree_slugs[t['id']]}",
                    "item": {
                        "@type": "TouristAttraction",
                        "name": t["name"],
                        "description": t["story"][:200],
                        "geo": {
                            "@type": "GeoCoordinates",
                            "latitude": t["location"]["latitude"],
                            "longitude": t["location"]["longitude"],
                        },
                    },
                }
                for i, t in enumerate(trees, 1)
            ],
        },
        {
            "@type": "FAQPage",
            "mainEntity": [{
                "@type": "Question", "name": f["q"],
                "acceptedAnswer": {"@type": "Answer", "text": f["a"]},
            } for f in faq],
        },
        breadcrumb_schema(crumb_items),
    ]
    head_extra = map_head() + "\n" + ld_script(graph)

    avg_lat = sum(m["lat"] for m in markers) / len(markers)
    avg_lng = sum(m["lng"] for m in markers) / len(markers)

    body = f"""
<div class="split">
  <aside class="panel">
    <div class="panel-head">
      {breadcrumb_html(crumb_items, rootpath)}
      <p class="eyebrow">{esc(country)}</p>
      <h1>Ancient Trees in <em>{esc(city)}</em></h1>
      <p class="lede">{esc(intro)}</p>
      {curation_notice(city_data.get('status'))}
    </div>
    {''.join(cards)}
    {panel_foot}
  </aside>
  <div class="stage">
    <div id="map" class="map"></div>
  </div>
</div>
"""
    scripts = city_map_script(markers, (avg_lat, avg_lng))

    link_count = len(trees) + 1 + (1 if coll else 0) + len(other_cities)
    check_links(canonical, link_count, 12)

    page = render_page(title, description, canonical, body, head_extra, scripts,
                       rootpath="./", footer=False)
    pages.append((f"{slug}.html", page, canonical))
    return {"slug": slug, "city": city, "country": country, "count": len(trees),
            "markers": markers, "canonical": canonical}


# ---------------------------------------------------------- collection pages

def build_collection_page(coll, cities_by_slug, tree_slugs, published, pages):
    slug = coll["slug"]
    canonical = f"{BASE_URL}/collections/{slug}"
    rootpath = "../"
    title = fit_title([coll["title"]], canonical)
    description = coll.get("meta_description", "")

    crumb_items = [("Home", BASE_URL), ("Collections", f"{BASE_URL}/collections"), (coll["title"], None)]

    grouped = {}
    for e in coll.get("entries", []):
        grouped.setdefault(e["city_slug"], []).append(e)

    sections = []
    entry_count = 0
    list_elements = []
    for cslug, entries in grouped.items():
        city_data = cities_by_slug[cslug]["data"]
        trees_by_id = {t["id"]: t for t in city_data["trees"]}
        rows = []
        for e in entries:
            t = trees_by_id[e["tree_id"]]
            tslug = tree_slugs[t["id"]]
            entry_count += 1
            list_elements.append({
                "@type": "ListItem", "position": entry_count,
                "name": t["name"], "url": f"{BASE_URL}/{cslug}/{tslug}",
            })
            ph = usable_photo(t)
            thumb = (f'<div class="entry-thumb"><img src="{esc(ph["url"])}" alt="{esc(t["name"])}" loading="lazy"></div>'
                     if ph else "")
            rows.append(f"""
      <div class="entry{' has-thumb' if ph else ''}">
        {thumb}
        <div class="entry-body">
          <h3><a href="../{cslug}/{tslug}">{esc(t['name'])}</a> <span class="tree-label">{esc(t.get('age_estimate', ''))}</span></h3>
          <p>{esc(e['note'])}</p>
        </div>
      </div>""")
        sections.append(f"<h2>{esc(city_data['city'])}</h2>{''.join(rows)}")

    city_links = " &middot; ".join(
        f'<a href="../{p["slug"]}">Ancient trees in {esc(p["city"])}</a>' for p in published
    )

    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>{esc(coll['title'])}</h1>
  {curation_notice(coll.get('status'))}
  <div class="prose-block"><p>{esc(coll['intro'])}</p></div>
  {''.join(sections)}
  <p class="suggest">Explore by city: {city_links}</p>
</main>
"""

    graph = site_graph() + [
        {"@type": "ItemList", "name": coll["title"], "itemListElement": list_elements},
        breadcrumb_schema(crumb_items),
    ]
    head_extra = ld_script(graph)

    check_links(canonical, entry_count + len(published), entry_count + min(3, len(published)))

    page = render_page(title, description, canonical, body, head_extra, "", rootpath)
    pages.append((f"collections/{slug}.html", page, canonical))
    return canonical


def build_city_gpx(entry, trees, pages):
    """One waypoint per tree, loadable in any maps or hiking app.

    This is what turns the page into something you can carry: the whole city's
    trees on your phone, working offline, no app install.
    """
    city = entry["data"]["city"]
    slug = entry["slug"]
    pts = []
    for t in trees:
        loc = t["location"]
        desc = f"{t.get('species', '')}. {t.get('age_estimate', '')}. {t.get('access', '')}"
        pts.append(
            f'  <wpt lat="{loc["latitude"]}" lon="{loc["longitude"]}">\n'
            f'    <name>{esc(t["name"])}</name>\n'
            f'    <desc>{esc(desc.strip())}</desc>\n'
            f'  </wpt>'
        )
    gpx = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<gpx version="1.1" creator="Ancient Trees" xmlns="http://www.topografix.com/GPX/1/1">\n'
        f'  <metadata><name>Ancient Trees in {esc(city)}</name>'
        f'<link href="{BASE_URL}/{slug}"><text>ancienttrees.app</text></link></metadata>\n'
        + "\n".join(pts) + "\n</gpx>\n"
    )
    pages.append((f"{slug}.gpx", gpx, None))


def build_species_page(intro_data, members, tree_slugs, published, pages):
    """members: list of (city_entry, tree) for this species, already gated to 3+."""
    slug = intro_data["slug"]
    common = intro_data["common_name"]
    canonical = f"{BASE_URL}/species/{slug}"
    rootpath = "../"
    title = fit_title([
        intro_data.get("title", ""),
        f"{common}: Ancient {common}s You Can Visit",
        f"Ancient {common} Trees",
        common,
    ], canonical)
    description = intro_data.get("meta_description", "")

    crumb_items = [("Home", BASE_URL), ("Species", f"{BASE_URL}/species"), (common, None)]

    # group members by city, in published-city order
    order = {p["slug"]: i for i, p in enumerate(published)}
    by_city = {}
    for entry, t in members:
        by_city.setdefault(entry["slug"], (entry, []))[1].append(t)
    sections = []
    list_elements = []
    n = 0
    for cslug in sorted(by_city, key=lambda s: order.get(s, 99)):
        entry, trees = by_city[cslug]
        trees = sorted(trees, key=lambda t: -(t.get("age_max") or 0))
        rows = []
        for t in trees:
            tslug = tree_slugs[t["id"]]
            loc = t["location"]
            n += 1
            list_elements.append({
                "@type": "ListItem", "position": n,
                "name": t["name"], "url": f"{BASE_URL}/{cslug}/{tslug}",
            })
            ph = usable_photo(t)
            thumb = (f'<div class="entry-thumb"><img src="{esc(ph["url"])}" alt="{esc(t["name"])}" loading="lazy"></div>'
                     if ph else "")
            rows.append(f"""
      <div class="entry{' has-thumb' if ph else ''}">
        {thumb}
        <div class="entry-body">
          <h3><a href="../{cslug}/{tslug}">{esc(t['name'])}</a> <span class="tree-label">{esc(t.get('age_estimate',''))}</span></h3>
          <p>{esc(loc.get('neighbourhood',''))}. {esc(t['story'].split('. ')[0])}.</p>
        </div>
      </div>""")
        sections.append(f'<h2>{esc(entry["data"]["city"])}</h2>{"".join(rows)}')

    city_links = " &middot; ".join(
        f'<a href="../{p["slug"]}">Ancient trees in {esc(p["city"])}</a>' for p in published
    )

    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>{esc(common)}</h1>
  <p class="answer-first">{esc(intro_data['intro'].split('. ')[0])}. This page maps every {esc(common.lower())} on the site, {n} so far across {len(by_city)} cit{'y' if len(by_city)==1 else 'ies'}.</p>
  <div class="prose-block"><p>{esc(intro_data['intro'])}</p></div>
  {''.join(sections)}
  <p class="suggest">Explore by city: {city_links} &middot; or browse <a href="../species">all species</a>.</p>
</main>
"""
    graph = site_graph() + [
        {"@type": "ItemList", "name": f"{common} trees", "itemListElement": list_elements},
        breadcrumb_schema(crumb_items),
    ]
    head_extra = ld_script(graph)
    check_links(canonical, n + len(published) + 1, n + min(2, len(published)) + 1)
    page = render_page(title, description, canonical, body, head_extra, "", rootpath)
    pages.append((f"species/{slug}.html", page, canonical))
    return {"slug": slug, "common": common, "scientific": intro_data.get("scientific_name", ""),
            "count": n, "cities": len(by_city)}


def build_species_index(species_cards, published, pages):
    canonical = f"{BASE_URL}/species"
    rootpath = "./"
    title = fit_title(["Ancient Trees by Species", "Browse Ancient Trees by Species"], canonical)
    description = ("Browse the mapped trees by species: the London plane that lines half of "
                  "Europe's streets, the wingnut Amsterdam went to court over, and more.")
    crumb_items = [("Home", BASE_URL), ("Species", None)]

    entries = "".join(
        f"""
      <div class="entry">
        <h3><a href="species/{c['slug']}">{esc(c['common'])}</a> <span class="tree-label">{c['count']} trees</span></h3>
        <p><em>{esc(c['scientific'])}</em>. Mapped across {c['cities']} cit{'y' if c['cities']==1 else 'ies'} so far.</p>
      </div>"""
        for c in species_cards
    )
    city_links = " &middot; ".join(
        f'<a href="{p["slug"]}">Ancient trees in {esc(p["city"])}</a>' for p in published
    )
    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>Ancient Trees by Species</h1>
  <div class="prose-block"><p>Cities group these trees by place; collections group them by theme. This page groups them by what they actually are. A species earns a page once the site has mapped at least three of them, so every list here has real depth rather than a lone specimen. More species appear as new cities join the map.</p></div>
  {entries}
  <p class="suggest">Or explore by city: {city_links}</p>
</main>
"""
    graph = site_graph() + [
        {"@type": "ItemList", "name": "Tree species",
         "itemListElement": [
             {"@type": "ListItem", "position": i, "name": c["common"],
              "url": f"{BASE_URL}/species/{c['slug']}"}
             for i, c in enumerate(species_cards, 1)]},
        breadcrumb_schema(crumb_items),
    ]
    head_extra = ld_script(graph)
    page = render_page(title, description, canonical, body, head_extra, "", rootpath)
    pages.append(("species.html", page, canonical))


def build_collections_index(collections, published, pages):
    """Overview of all collections at /collections."""
    canonical = f"{BASE_URL}/collections"
    rootpath = "./"
    title = fit_title(["Collections: Remarkable Trees by Theme"], canonical)
    description = ("Hand-curated lists that cut across cities: the oldest, the strangest, "
                   "the ones worth a detour. Every entry links to a verified tree.")

    crumb_items = [("Home", BASE_URL), ("Collections", None)]

    entries = []
    for c in collections:
        first_sentence = c["intro"].split(". ")[0] + "."
        entries.append(f"""
      <div class="entry">
        <h3><a href="collections/{c['slug']}">{esc(c['title'])}</a></h3>
        <p>{esc(first_sentence)} {len(c.get('entries', []))} trees, across {len({e['city_slug'] for e in c.get('entries', [])})} cities.</p>
      </div>""")

    city_links = " &middot; ".join(
        f'<a href="{p["slug"]}">Ancient trees in {esc(p["city"])}</a>' for p in published
    )

    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>Collections</h1>
  <div class="prose-block"><p>Cities organise these trees by place. Collections organise them by what makes them worth the trip: age, strangeness, the stories they carry. Each one is hand-curated, and every entry links to a verified tree with its own map and directions. More collections are added as the map grows.</p></div>
  {''.join(entries)}
  <p class="suggest">Explore by city instead: {city_links}</p>
</main>
"""
    graph = site_graph() + [
        {
            "@type": "ItemList",
            "name": "Collections",
            "itemListElement": [
                {"@type": "ListItem", "position": i, "name": c["title"],
                 "url": f"{BASE_URL}/collections/{c['slug']}"}
                for i, c in enumerate(collections, 1)
            ],
        },
        breadcrumb_schema(crumb_items),
    ]
    head_extra = ld_script(graph)
    page = render_page(title, description, canonical, body, head_extra, "", rootpath)
    pages.append(("collections.html", page, canonical))


def build_contribute_page(published, pages):
    """The flywheel's front door: readers send trees, the nightly run verifies
    and writes them up. Deliberately asks for the few things that make a
    submission verifiable, because unverifiable ones cannot be published."""
    canonical = f"{BASE_URL}/contribute"
    rootpath = "./"
    title = fit_title(["Become Your City's Tree Guide",
                       "Map Your City's Ancient Trees"], canonical)
    description = ("Know the remarkable old trees of your city? Put them on the map. "
                   "Every submission is verified against independent sources before it goes live.")
    crumb_items = [("Home", BASE_URL), ("Map your city", None)]

    city_links = " &middot; ".join(
        f'<a href="{p["slug"]}">{esc(p["city"])}</a>' for p in published
    )

    body = f"""
<main class="content-page">
  {breadcrumb_html(crumb_items, rootpath)}
  <h1>Become your city's tree guide</h1>
  <p class="answer-first">This map is missing far more cities than it has, and the trees that matter most are the ones locals already know about. If you know your city's remarkable old trees, you can put them on the map and be credited for it.</p>
  <div class="prose-block">
    <p>Research from a distance finds the famous trees. It misses the one on the corner that everyone in the neighbourhood walks past, the one with the story attached, the one that is only obvious if you live there. That gap is why this page exists.</p>
    <p>Everything sent in gets checked against independent sources, and the location gets verified, because a wrong pin is worse than a missing tree. Confirmed trees get their own page with your credit on the city. What cannot be confirmed waits instead of going live half-true. To be straight with you about what you get: your name on the city you mapped, not a login or a profile. Those may come later.</p>
  </div>

  <div class="path">
    <h2>Map your whole city</h2>
    <p class="prose-block">The big one. Tell us which city and which trees belong on its list. You do not need ten, and you do not need to write anything polished. Names and rough locations are enough; the research, the checking and the writing happen here.</p>
    <a class="go-btn" href="{submit_link('city')}">Map my city</a>
  </div>

  <div class="path">
    <h2>Or just one tree</h2>
    <p class="prose-block">Saw something remarkable and know roughly where it stands? That is enough. One tree in a city we have never touched is often the thing that starts it.</p>
    <a class="go-btn" href="{submit_link('tree')}">Send one tree</a>
  </div>

  <h2>What helps most</h2>
  <ul class="link-list">
    <li><strong>Where exactly it stands.</strong> A street corner, a park entrance, or a dropped pin from Google Maps. The single most useful thing you can give us.</li>
    <li><strong>Why it is remarkable.</strong> Old, enormous, strange, or tied to a local story.</li>
    <li><strong>How you know.</strong> A link, a book, a plaque, or just that you grew up next to it.</li>
    <li><strong>A photo you took yourself,</strong> if you have one. We can only publish photos that are yours to share or openly licensed.</li>
  </ul>

  <h2>Or fix something</h2>
  <div class="prose-block">
    <p>Spotted a wrong location, an age that looks off, or a tree that has fallen since we wrote about it? Those corrections are just as valuable. <a href="{submit_link('correction')}">Send a correction</a> and say what is wrong.</p>
  </div>
  <p class="suggest">Cities on the map so far: {city_links}</p>
</main>
"""
    graph = site_graph() + [breadcrumb_schema(crumb_items)]
    head_extra = ld_script(graph)
    page = render_page(title, description, canonical, body, head_extra, "", rootpath)
    pages.append(("contribute.html", page, canonical))


# ----------------------------------------------------------------- homepage

def build_homepage(published, upcoming, collections, pages):
    title = "Ancient Trees: the world's most remarkable trees, mapped"
    description = ("Ancient Trees maps the oldest and most beautiful trees in 100 cities worldwide. "
                   "Free to explore. Find them before everyone else does.")

    city_markers = []
    for p in published:
        lat = sum(m["lat"] for m in p["markers"]) / len(p["markers"])
        lng = sum(m["lng"] for m in p["markers"]) / len(p["markers"])
        city_markers.append({
            "lat": lat, "lng": lng, "label": str(p["count"]),
            "url": p["slug"],
        })

    live_cards = "".join(
        f"""<a class="city-card" href="{p['slug']}">
      <div class="city-card-name">{esc(p['city'])}</div>
      <div class="city-card-meta">{esc(p['country'])} &middot; {p['count']} trees</div>
    </a>"""
        for p in published
    )
    soon_cards = "".join(
        f"""<a class="city-card soon" href="contribute">
      <div class="city-card-name">{esc(c['city'])}</div>
      <div class="city-card-meta">{esc(c['country'])} &middot; not mapped yet</div>
      <div class="city-card-cta">Be the first to map it</div>
    </a>"""
        for c in upcoming
    )

    coll_html = "".join(
        f'<p class="prose">Start with a collection: <a href="collections/{c["slug"]}">{esc(c["title"])}</a>.</p>'
        for c in collections
    )

    body = f"""
<div class="home-hero">
  <div id="map" class="map"></div>
  <div class="hero-overlay">
    <h1>Every city has a tree that was <em>here before the city was</em>.</h1>
    <p>The oldest and most remarkable trees in 100 cities, each verified, each with its story, each on the map. Tap a pin to start.</p>
  </div>
</div>
<main class="page">
  <h2 class="section-heading" id="cities">Cities</h2>
  <div class="city-grid">{live_cards}{soon_cards}</div>
  {coll_html}
  <h2 class="section-heading">Why trees</h2>
  <p class="prose">A 400 year old tree has outlasted every empire, plague, and war its city has seen. It was here before the street was named. It will be here after you leave. Most travel guides send you to the same squares, the same views, the same lunch spots. Ancient Trees takes you somewhere quieter. These are the spots that do not make the top ten lists. They are better.</p>
</main>
"""
    head_extra = map_head() + "\n" + ld_script(site_graph())
    scripts = home_map_script(city_markers)
    page = render_page(title, description, BASE_URL + "/", body, head_extra, scripts,
                       rootpath="./", og_type="website")
    pages.append(("index.html", page, BASE_URL + "/"))


# ------------------------------------------------------------ redirect stubs

def redirect_stub(target_rel, canonical, title):
    return (
        '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
        f'<meta http-equiv="refresh" content="0; url={target_rel}">'
        f'<link rel="canonical" href="{canonical}">'
        f'<title>{esc(title)}</title>'
        f'<script>window.location.replace("{target_rel}");</script></head>'
        f'<body><p>This page moved to <a href="{target_rel}">{canonical}</a>.</p></body></html>'
    )


def build_redirects(published, pages):
    """Old /cities/[slug]/ URLs redirect to the contract URLs, and
    /[slug]/ with a trailing slash redirects to the canonical /[slug]."""
    for p in published:
        title = f"Moved: Ancient Trees in {p['city']}"
        pages.append((f"cities/{p['slug']}/index.html",
                      redirect_stub(f"../../{p['slug']}", p["canonical"], title), None))
        pages.append((f"{p['slug']}/index.html",
                      redirect_stub(f"../{p['slug']}", p["canonical"], title), None))
    pages.append(("collections/index.html",
                  redirect_stub("../collections", f"{BASE_URL}/collections",
                                "Moved: Collections"), None))
    pages.append(("species/index.html",
                  redirect_stub("../species", f"{BASE_URL}/species",
                                "Moved: Species"), None))


def validate_internal_links(pages):
    """Every internal href must resolve to a page this build produces.

    Catches wrong relative paths (P8: no dead ends) before deploy.
    """
    valid = {"/", "/assets/style.css"}
    for relpath, _, _ in pages:
        url = "/" + relpath
        valid.add(url)
        if url.endswith("/index.html"):
            valid.add(url[: -len("index.html")])
        elif url.endswith(".html"):
            valid.add(url[:-5])

    for relpath, content, _ in pages:
        page_url = "/" + relpath
        if page_url.endswith("/index.html"):
            page_url = page_url[: -len("index.html")]
        elif page_url.endswith(".html"):
            page_url = page_url[:-5]
        if page_url == "/index":
            page_url = "/"
        for href in re.findall(r'href="([^"]+)"', content):
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = urlparse(urljoin(page_url, href)).path
            if target not in valid:
                ERRORS.append(f"{page_url}: broken internal link {href!r} resolves to {target}")


def build_sitemap(pages):
    today = date.today().isoformat()
    urls = [canonical for _, _, canonical in pages if canonical]
    entries = "".join(
        f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls
    )
    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}</urlset>\n'
    (DIST / "sitemap.xml").write_text(sitemap)
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")


def main():
    cities = load_cities()
    collections = load_collections()
    species_intros = load_species_intros()
    cities_by_slug = {c["slug"]: c for c in cities}
    pages = []  # (relative path, html, canonical or None)

    published = []
    upcoming = []
    tree_slugs = {}

    renderable = []
    for entry in cities:
        if entry["data"] and any(tree_is_renderable(t) for t in entry["data"].get("trees", [])):
            renderable.append(entry)
        elif entry["tier"] == 1:
            upcoming.append(entry)

    # Which species qualify for a page: 3+ renderable trees AND a hand-written intro.
    species_groups = group_trees_by_species(renderable)
    qualifying = {
        common: members for common, members in species_groups.items()
        if len(members) >= SPECIES_MIN_TREES and common in species_intros
    }
    species_pages = {common: species_intros[common]["slug"] for common in qualifying}

    for entry in renderable:
        trees = [t for t in entry["data"]["trees"] if tree_is_renderable(t)]
        for tree in trees:
            tree_slugs[tree["id"]] = build_tree_page(entry, tree, trees, collections, pages, species_pages)
        build_question_page(entry, collections, pages)
        other_cities = [
            {"slug": e["slug"], "city": e["data"]["city"]}
            for e in renderable if e["slug"] != entry["slug"]
        ]
        build_city_gpx(entry, trees, pages)
        result = build_city_page(entry, tree_slugs, collections, pages, other_cities)
        if result:
            published.append(result)

    for coll in collections:
        build_collection_page(coll, cities_by_slug, tree_slugs, published, pages)
    if collections:
        build_collections_index(collections, published, pages)

    species_cards = []
    for common in sorted(qualifying, key=lambda c: -len(qualifying[c])):
        card = build_species_page(species_intros[common], qualifying[common],
                                  tree_slugs, published, pages)
        species_cards.append(card)
    if species_cards:
        build_species_index(species_cards, published, pages)

    build_contribute_page(published, pages)
    build_homepage(published, upcoming, collections, pages)
    build_redirects(published, pages)
    validate_internal_links(pages)

    if ERRORS:
        print(f"BUILD FAILED: {len(ERRORS)} contract violation(s), nothing deployed\n")
        for e in ERRORS:
            print(f"  - {e}")
        sys.exit(1)

    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "assets").mkdir(parents=True)
    (DIST / "assets" / "style.css").write_text(CSS)
    # Custom domain for GitHub Pages; must survive every rebuild.
    (DIST / "CNAME").write_text(CUSTOM_DOMAIN + "\n")
    for relpath, content, _ in pages:
        out = DIST / relpath
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content)
    build_sitemap(pages)

    n_trees = sum(p["count"] for p in published)
    print(f"Built {len(pages)} page(s) into {DIST}: "
          f"{len(published)} city, {n_trees} tree, {len(published)} question, "
          f"{len(collections)} collection, homepage. All contracts validated.")
    for p in published:
        print(f"  - {p['city']}: {p['count']} trees")


if __name__ == "__main__":
    main()
