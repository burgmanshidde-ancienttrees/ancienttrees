#!/usr/bin/env python3
"""Static site generator for ancienttrees.app.

Map-first layout inspired by travel apps: the map is the primary
interface, with a scrollable story panel beside it. All tree content
stays in plain HTML for SEO.

Reads data/city-list.json and data/cities/*.json, writes site/dist/.
No dependencies beyond the Python 3.9 standard library.

Usage: python3 scripts/build_site.py
"""

import json
import html
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DIST = ROOT / "site" / "dist"
BASE_URL = "https://ancienttrees.app"

MAPLIBRE_JS = "https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"
MAPLIBRE_CSS = "https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css"
# OpenFreeMap: free vector tiles, no API key, commercial use permitted
MAP_STYLE = "https://tiles.openfreemap.org/styles/positron"

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
.tree-card-top { display: flex; align-items: baseline; gap: 0.75rem; margin-bottom: 0.4rem; }
.tree-num { font-family: var(--serif); font-size: 1.1rem; color: var(--moss); flex-shrink: 0; width: 1.4rem; }
.tree-name { font-family: var(--serif); font-size: 1.35rem; font-weight: 400; line-height: 1.25; }
.tree-meta { font-size: 12px; color: var(--ink-light); margin: 0 0 0.85rem 2.15rem; }
.tree-story { font-size: 14px; font-weight: 300; color: var(--ink-mid); line-height: 1.7; margin: 0 0 0.85rem 2.15rem; }
.tree-practical { font-size: 12px; color: var(--ink-light); margin-left: 2.15rem; }
.tree-practical span { display: block; margin-bottom: 0.2rem; }

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

footer { border-top: 1px solid var(--cream-dark); padding: 2rem 2.5rem; display: flex; align-items: center; justify-content: space-between; }
.footer-logo { font-family: var(--serif); font-size: 14px; letter-spacing: 0.08em; text-transform: uppercase; }
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
  .stage { position: sticky; top: var(--header-h); height: 46vh; min-height: 300px; z-index: 5; }
  .home-hero { height: 60vh; }
  .hero-overlay { left: 1rem; right: 1rem; top: 1rem; max-width: none; padding: 1.25rem 1.5rem; }
  .page { padding: 2rem 1.5rem; }
  footer { flex-direction: column; gap: 0.5rem; text-align: center; }
}
"""

PAGE_SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%%TITLE%%</title>
<meta name="description" content="%%DESCRIPTION%%">
<link rel="canonical" href="%%CANONICAL%%">
<meta property="og:title" content="%%TITLE%%">
<meta property="og:description" content="%%DESCRIPTION%%">
<meta property="og:type" content="website">
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
  <span class="footer-note">&copy; %%YEAR%% Ancient Trees, ancienttrees.app. Map &copy; OpenFreeMap, OpenMapTiles, OpenStreetMap contributors.</span>
</footer>
"""


def esc(s):
    return html.escape(str(s), quote=True)


def render_page(title, description, canonical, body, head_extra="", scripts="", rootpath="/", footer=True):
    return (
        PAGE_SHELL
        .replace("%%TITLE%%", esc(title))
        .replace("%%DESCRIPTION%%", esc(description))
        .replace("%%CANONICAL%%", canonical)
        .replace("%%ROOTPATH%%", rootpath)
        .replace("%%HEAD_EXTRA%%", head_extra)
        .replace("%%BODY%%", body)
        .replace("%%FOOTER%%", FOOTER if footer else "")
        .replace("%%SCRIPTS%%", scripts)
        .replace("%%YEAR%%", str(date.today().year))
    )


def map_head():
    return f'<link rel="stylesheet" href="{MAPLIBRE_CSS}">'


def city_map_script(markers, center):
    """Interactive city map: numbered pins linked to story cards, fly-to on select."""
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
  card.addEventListener('click', function() {{ setActive(idx, true, false); }});
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


def tree_is_renderable(tree):
    loc = tree.get("location") or {}
    return bool(tree.get("story")) and loc.get("latitude") is not None and loc.get("longitude") is not None


def load_cities():
    city_list = json.loads((DATA / "city-list.json").read_text())["cities"]
    for entry in city_list:
        f = DATA / "cities" / f"{entry['slug']}.json"
        entry["data"] = json.loads(f.read_text()) if f.exists() else None
    return city_list


def build_city_page(entry):
    city_data = entry["data"]
    city = city_data["city"]
    country = city_data["country"]
    slug = entry["slug"]
    trees = [t for t in city_data.get("trees", []) if tree_is_renderable(t)]
    if not trees:
        return None

    title = f"10 Most Beautiful Ancient Trees in {city}"
    description = (
        f"The oldest and most remarkable trees in {city}, {country}: "
        f"verified locations, real stories, and how to reach each one."
    )
    canonical = f"{BASE_URL}/cities/{slug}/"

    curated = city_data.get("status") in ("curated", "published")
    notice = "" if curated else (
        '<div class="notice">This city is awaiting curation. Facts have been researched '
        "and cross-referenced, but the final human review is still in progress.</div>"
    )

    cards = []
    markers = []
    for i, t in enumerate(trees, 1):
        loc = t["location"]
        practical = []
        if t.get("access"):
            practical.append(f"<span>Access: {esc(t['access'])}</span>")
        if t.get("transport"):
            practical.append(f"<span>Getting there: {esc(t['transport'])}</span>")
        cards.append(f"""
    <article class="tree-card" id="tree-{i}">
      <div class="tree-card-top">
        <span class="tree-num">{i}</span>
        <h2 class="tree-name">{esc(t['name'])}</h2>
      </div>
      <p class="tree-meta">{esc(t.get('species', ''))} &middot; {esc(t.get('age_estimate', 'age unknown'))} &middot; {esc(loc.get('neighbourhood', ''))}</p>
      <p class="tree-story">{esc(t['story'])}</p>
      <p class="tree-practical">{''.join(practical)}</p>
    </article>""")
        markers.append({
            "lat": loc["latitude"], "lng": loc["longitude"], "label": str(i),
        })

    ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": title,
        "itemListElement": [
            {
                "@type": "ListItem", "position": i,
                "name": t["name"],
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
    }
    head_extra = map_head() + f'\n<script type="application/ld+json">{json.dumps(ld)}</script>'

    avg_lat = sum(m["lat"] for m in markers) / len(markers)
    avg_lng = sum(m["lng"] for m in markers) / len(markers)

    body = f"""
<div class="split">
  <aside class="panel">
    <div class="panel-head">
      <p class="eyebrow">{esc(country)}</p>
      <h1>10 Most Beautiful <em>Ancient Trees</em> in {esc(city)}</h1>
      <p class="lede">Every one of these trees has been verified against independent sources. Ages are estimates, locations are exact. Tap a tree to see where it stands.</p>
      {notice}
    </div>
    {''.join(cards)}
  </aside>
  <div class="stage">
    <div id="map" class="map"></div>
  </div>
</div>
"""
    scripts = city_map_script(markers, (avg_lat, avg_lng))
    page = render_page(title, description, canonical, body, head_extra, scripts,
                       rootpath="../../", footer=False)
    out = DIST / "cities" / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    return {"slug": slug, "city": city, "country": country, "count": len(trees),
            "markers": markers, "canonical": canonical}


def build_homepage(published, upcoming):
    title = "Ancient Trees: the world's most remarkable trees, mapped"
    description = ("Ancient Trees maps the oldest and most beautiful trees in 100 cities worldwide. "
                   "Free to explore. Find them before everyone else does.")

    city_markers = []
    for p in published:
        lat = sum(m["lat"] for m in p["markers"]) / len(p["markers"])
        lng = sum(m["lng"] for m in p["markers"]) / len(p["markers"])
        city_markers.append({
            "lat": lat, "lng": lng, "label": str(p["count"]),
            "url": f"cities/{p['slug']}/",
        })

    live_cards = "".join(
        f"""<a class="city-card" href="cities/{p['slug']}/">
      <div class="city-card-name">{esc(p['city'])}</div>
      <div class="city-card-meta">{esc(p['country'])} &middot; {p['count']} trees</div>
    </a>"""
        for p in published
    )
    soon_cards = "".join(
        f"""<div class="city-card soon">
      <div class="city-card-name">{esc(c['city'])}</div>
      <div class="city-card-meta">{esc(c['country'])} &middot; coming soon</div>
    </div>"""
        for c in upcoming
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
  <h2 class="section-heading">Why trees</h2>
  <p class="prose">A 400 year old tree has outlasted every empire, plague, and war its city has seen. It was here before the street was named. It will be here after you leave. Most travel guides send you to the same squares, the same views, the same lunch spots. Ancient Trees takes you somewhere quieter. These are the spots that do not make the top ten lists. They are better.</p>
</main>
"""
    head_extra = map_head()
    scripts = home_map_script(city_markers)
    page = render_page(title, description, BASE_URL + "/", body, head_extra, scripts, rootpath="")
    (DIST / "index.html").write_text(page)


def build_sitemap(published):
    today = date.today().isoformat()
    urls = [f"{BASE_URL}/"] + [p["canonical"] for p in published]
    entries = "".join(
        f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls
    )
    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}</urlset>\n'
    (DIST / "sitemap.xml").write_text(sitemap)
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "assets").mkdir(parents=True)
    (DIST / "assets" / "style.css").write_text(CSS)

    cities = load_cities()
    published = []
    upcoming = []
    for entry in cities:
        if entry["data"]:
            result = build_city_page(entry)
            if result:
                published.append(result)
                continue
        if entry["tier"] == 1:
            upcoming.append(entry)

    build_homepage(published, upcoming)
    build_sitemap(published)
    print(f"Built {len(published)} city page(s) + homepage into {DIST}")
    for p in published:
        print(f"  - {p['city']}: {p['count']} trees")


if __name__ == "__main__":
    main()
