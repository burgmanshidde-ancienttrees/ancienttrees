#!/usr/bin/env python3
"""Static site generator for ancienttrees.app.

Reads data/city-list.json and data/cities/*.json, writes a complete
static site to site/dist/. No dependencies beyond the Python 3.9
standard library, so it runs anywhere including GitHub Actions.

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

OSM_STYLE = {
    "version": 8,
    "sources": {
        "osm": {
            "type": "raster",
            "tiles": ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
            "tileSize": 256,
            "attribution": "&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors",
        }
    },
    "layers": [{"id": "osm", "type": "raster", "source": "osm"}],
}

CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --cream: #F7F4EE; --cream-dark: #EDE9DF; --ink: #1A1A14; --ink-mid: #4A4A3A;
  --ink-light: #8A8A7A; --moss: #3D5C1E; --moss-light: #EAF0E0;
  --serif: 'Playfair Display', Georgia, serif; --sans: 'Inter', system-ui, sans-serif;
}
html { scroll-behavior: smooth; }
body { background: var(--cream); color: var(--ink); font-family: var(--sans); font-size: 16px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
a { color: var(--moss); }
nav { display: flex; align-items: center; justify-content: space-between; padding: 1.25rem 2.5rem; background: var(--cream); border-bottom: 1px solid var(--cream-dark); }
.nav-logo { font-family: var(--serif); font-size: 15px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink); text-decoration: none; }
.nav-links { display: flex; gap: 1.5rem; }
.nav-links a { font-size: 13px; color: var(--ink-mid); text-decoration: none; }
.nav-links a:hover { color: var(--moss); }
.page { max-width: 1100px; margin: 0 auto; padding: 3rem 2.5rem; }
.eyebrow { font-size: 11px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; color: var(--ink-light); margin-bottom: 1rem; }
h1 { font-family: var(--serif); font-size: clamp(2.2rem, 4vw, 3.5rem); font-weight: 400; line-height: 1.15; margin-bottom: 1.25rem; }
h1 em { font-style: italic; color: var(--moss); }
.lede { font-size: 17px; font-weight: 300; color: var(--ink-mid); line-height: 1.75; max-width: 640px; margin-bottom: 2.5rem; }
.map { width: 100%; height: 480px; border: 1px solid var(--cream-dark); border-radius: 3px; margin-bottom: 3rem; }
.map:fullscreen { height: 100vh; }
.notice { background: var(--moss-light); border: 1px solid var(--moss); border-radius: 3px; padding: 0.85rem 1.25rem; font-size: 13px; color: var(--ink-mid); margin-bottom: 2.5rem; }
.tree-list { display: flex; flex-direction: column; gap: 2px; background: var(--cream-dark); border: 1px solid var(--cream-dark); }
.tree-item { background: var(--cream); padding: 2.25rem 2rem; display: grid; grid-template-columns: 3rem 1fr; gap: 1.5rem; }
.tree-num { font-family: var(--serif); font-size: 2rem; color: var(--ink-light); line-height: 1; }
.tree-name { font-family: var(--serif); font-size: 1.5rem; font-weight: 400; line-height: 1.25; margin-bottom: 0.35rem; }
.tree-meta { font-size: 13px; color: var(--ink-light); margin-bottom: 1rem; }
.tree-story { font-size: 15px; font-weight: 300; color: var(--ink-mid); line-height: 1.75; max-width: 640px; margin-bottom: 1rem; }
.tree-practical { font-size: 13px; color: var(--ink-light); }
.tree-practical span { margin-right: 1.5rem; }
.city-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 2px; background: var(--cream-dark); border: 1px solid var(--cream-dark); margin-bottom: 3rem; }
.city-card { background: var(--cream); padding: 1.5rem; text-decoration: none; border-top: 2px solid transparent; transition: border-color 0.2s; }
.city-card:hover { border-top-color: var(--moss); }
.city-card-name { font-family: var(--serif); font-size: 1.25rem; color: var(--ink); margin-bottom: 0.25rem; }
.city-card-meta { font-size: 12px; color: var(--ink-light); }
.city-card.soon { opacity: 0.55; }
h2.section-heading { font-family: var(--serif); font-size: 1.75rem; font-weight: 400; margin: 3rem 0 1.5rem; }
footer { border-top: 1px solid var(--cream-dark); padding: 2rem 2.5rem; display: flex; align-items: center; justify-content: space-between; margin-top: 4rem; }
.footer-logo { font-family: var(--serif); font-size: 14px; letter-spacing: 0.08em; text-transform: uppercase; }
.footer-note { font-size: 12px; color: var(--ink-light); }
.marker-pin { width: 26px; height: 26px; border-radius: 50% 50% 50% 0; background: var(--moss); transform: rotate(-45deg); border: 2px solid #fff; box-shadow: 0 1px 4px rgba(0,0,0,0.3); cursor: pointer; }
.marker-pin span { display: block; transform: rotate(45deg); color: #fff; font-size: 12px; font-weight: 600; text-align: center; line-height: 22px; font-family: var(--sans); }
.maplibregl-popup-content { font-family: var(--sans); font-size: 13px; padding: 0.75rem 1rem; }
.maplibregl-popup-content strong { font-family: var(--serif); font-size: 15px; font-weight: 400; }
@media (max-width: 700px) {
  nav { padding: 1rem 1.5rem; }
  .page { padding: 2rem 1.5rem; }
  .tree-item { grid-template-columns: 1fr; gap: 0.5rem; }
  .map { height: 360px; }
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
<nav>
  <a href="%%ROOTPATH%%" class="nav-logo">Ancient Trees</a>
  <div class="nav-links">
    <a href="%%ROOTPATH%%#cities">Cities</a>
  </div>
</nav>
%%BODY%%
<footer>
  <span class="footer-logo">Ancient Trees</span>
  <span class="footer-note">&copy; %%YEAR%% Ancient Trees, ancienttrees.app. Map data &copy; OpenStreetMap contributors.</span>
</footer>
%%SCRIPTS%%
</body>
</html>
"""


def esc(s):
    return html.escape(str(s), quote=True)


def render_page(title, description, canonical, body, head_extra="", scripts="", rootpath="/"):
    return (
        PAGE_SHELL
        .replace("%%TITLE%%", esc(title))
        .replace("%%DESCRIPTION%%", esc(description))
        .replace("%%CANONICAL%%", canonical)
        .replace("%%ROOTPATH%%", rootpath)
        .replace("%%HEAD_EXTRA%%", head_extra)
        .replace("%%BODY%%", body)
        .replace("%%SCRIPTS%%", scripts)
        .replace("%%YEAR%%", str(date.today().year))
    )


def map_head():
    return f'<link rel="stylesheet" href="{MAPLIBRE_CSS}">'


def map_script(container_id, markers, center, zoom, fit_bounds):
    """markers: list of dicts {lat, lng, label, title, subtitle, url}"""
    data = json.dumps(markers)
    style = json.dumps(OSM_STYLE)
    fit = "true" if fit_bounds else "false"
    return f"""
<script src="{MAPLIBRE_JS}"></script>
<script>
var markers = {data};
var map = new maplibregl.Map({{
  container: '{container_id}',
  style: {style},
  center: [{center[1]}, {center[0]}],
  zoom: {zoom},
  scrollZoom: false
}});
map.addControl(new maplibregl.NavigationControl());
map.addControl(new maplibregl.FullscreenControl());
map.on('load', function() {{ map.resize(); }});
new ResizeObserver(function() {{ map.resize(); }}).observe(document.getElementById('{container_id}'));
var bounds = new maplibregl.LngLatBounds();
markers.forEach(function(m) {{
  var el = document.createElement('div');
  el.className = 'marker-pin';
  el.innerHTML = '<span>' + m.label + '</span>';
  var popupHtml = '<strong>' + m.title + '</strong><br>' + m.subtitle;
  if (m.url) {{ popupHtml += '<br><a href="' + m.url + '">View trees</a>'; }}
  new maplibregl.Marker({{ element: el, anchor: 'bottom' }})
    .setLngLat([m.lng, m.lat])
    .setPopup(new maplibregl.Popup({{ offset: 18 }}).setHTML(popupHtml))
    .addTo(map);
  bounds.extend([m.lng, m.lat]);
}});
if ({fit} && markers.length > 1) {{
  map.fitBounds(bounds, {{ padding: 60, maxZoom: 13 }});
}}
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
        '<div class="notice">This city is awaiting curation. '
        "Facts have been researched and cross-referenced, but the final human review is still in progress.</div>"
    )

    items = []
    markers = []
    for i, t in enumerate(trees, 1):
        loc = t["location"]
        practical = []
        if t.get("access"):
            practical.append(f"<span>Access: {esc(t['access'])}</span>")
        if t.get("transport"):
            practical.append(f"<span>Getting there: {esc(t['transport'])}</span>")
        items.append(f"""
    <div class="tree-item" id="tree-{i}">
      <div class="tree-num">{i}</div>
      <div>
        <h2 class="tree-name">{esc(t['name'])}</h2>
        <p class="tree-meta">{esc(t.get('species', ''))} &middot; {esc(t.get('age_estimate', 'age unknown'))} &middot; {esc(loc.get('neighbourhood', ''))}</p>
        <p class="tree-story">{esc(t['story'])}</p>
        <p class="tree-practical">{''.join(practical)}</p>
      </div>
    </div>""")
        markers.append({
            "lat": loc["latitude"], "lng": loc["longitude"], "label": str(i),
            "title": t["name"],
            "subtitle": f"{t.get('age_estimate', '')}, {loc.get('neighbourhood', '')}",
            "url": f"#tree-{i}",
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
<main class="page">
  <p class="eyebrow">{esc(country)}</p>
  <h1>10 Most Beautiful <em>Ancient Trees</em> in {esc(city)}</h1>
  <p class="lede">Every one of these trees has been verified against independent sources. Ages are estimates, locations are exact. Pick one and go look at it.</p>
  {notice}
  <div id="map" class="map"></div>
  <div class="tree-list">{''.join(items)}
  </div>
</main>
"""
    scripts = map_script("map", markers, (avg_lat, avg_lng), 11, True)
    page = render_page(title, description, canonical, body, head_extra, scripts, rootpath="../../")
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
            "title": p["city"], "subtitle": f"{p['count']} remarkable trees",
            "url": f"/cities/{p['slug']}/",
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
<main class="page">
  <p class="eyebrow">1,000 trees. 100 cities. The ones worth walking to.</p>
  <h1>Every city has a tree that was <em>here before the city was</em>.</h1>
  <p class="lede">Most travel guides send you to the same squares, the same views, the same lunch spots. Ancient Trees takes you somewhere quieter. The oldest and most remarkable trees in 100 cities, each verified, each with its story, each on the map.</p>
  <div id="map" class="map"></div>
  <h2 class="section-heading" id="cities">Cities</h2>
  <div class="city-grid">{live_cards}{soon_cards}</div>
</main>
"""
    head_extra = map_head()
    scripts = map_script("map", city_markers, (30, 10), 1.5, False)
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
