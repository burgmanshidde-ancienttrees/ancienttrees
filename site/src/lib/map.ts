// Ported from map_head()/country_map_script()/single_pin_script(),
// build_site.py:1199-1230ish, 4045-4101. Raw <script>/<link> tags loading
// MapLibre from a CDN, matching the current site exactly rather than going
// through the bundled npm package (see site-config.ts's note on MAPLIBRE_JS).
import { MAPLIBRE_JS, MAPLIBRE_CSS, MAP_STYLE } from "./site-config";

/** MapLibre, loaded without blocking the page.
 *
 * Until 2026-08-09 every page with a map carried a plain
 * `<script src="unpkg.com/maplibre-gl...">`, which stops the parser dead
 * while a few hundred kilobytes come down from a host that is not ours, on a
 * fresh DNS lookup and TLS handshake. Our own server answers in 33 to 158
 * milliseconds, so that download was most of what a visitor waited for, and
 * 72 percent of our search clicks arrive on a phone.
 *
 * `defer` fixes it without changing behaviour: the browser fetches in
 * parallel, executes after parsing, and deferred external scripts run in
 * document order strictly before DOMContentLoaded. So the init below, moved
 * into a DOMContentLoaded listener, is guaranteed to find `maplibregl`
 * defined. That guarantee is the whole reason this is a wrapper rather than
 * an IntersectionObserver: lazy-until-visible would be faster still and
 * would also stop the map ever building in a headless render, which is what
 * the smoke test checks. */
export function mapScript(body: string): string {
  return `\n<script defer src="${MAPLIBRE_JS}"></script>\n<script>\n` +
    `document.addEventListener("DOMContentLoaded", function () {\n${body}\n});\n</script>\n`;
}

export function mapHead(): string {
  return `<link rel="preconnect" href="https://unpkg.com" crossorigin>\n<link rel="stylesheet" href="${MAPLIBRE_CSS}">`;
}

/** A single-pin map: the tree page's own map, ported from
 * single_pin_script(), build_site.py:1203-1219. */
export function singlePinScript(lat: number, lng: number, label = "1"): string {
  return mapScript(`
var map = new maplibregl.Map({
  container: 'map', style: '${MAP_STYLE}',
  center: [${lng}, ${lat}], zoom: 14.5, scrollZoom: false,
  attributionControl: { compact: true }
});
map.addControl(new maplibregl.NavigationControl());
map.on('load', function() { map.resize(); });
var el = document.createElement('div');
el.className = 'pin';
el.textContent = '${label}';
new maplibregl.Marker({ element: el }).setLngLat([${lng}, ${lat}]).addTo(map);
`);
}

export interface CountryMapCity {
  slug: string;
  city: string;
  count: number;
  markers: { lat: number; lng: number }[];
}

/** One green dot per mapped city, click goes to its page. Deliberately the
 * simplest map on the site: at country zoom the job is orientation, not
 * detail. */
export function countryMapScript(cities: CountryMapCity[]): string {
  const centre = (c: CountryMapCity): [number, number] => [
    c.markers.reduce((s, m) => s + m.lng, 0) / c.markers.length,
    c.markers.reduce((s, m) => s + m.lat, 0) / c.markers.length,
  ];
  const data = {
    type: "FeatureCollection",
    features: cities.map((c) => ({
      type: "Feature",
      geometry: { type: "Point", coordinates: centre(c) },
      properties: { slug: c.slug, city: c.city, n: String(c.count) },
    })),
  };
  return mapScript(`
var CITIES = ${JSON.stringify(data)};
var map = new maplibregl.Map({
  container: 'map', style: '${MAP_STYLE}',
  center: [0, 0], zoom: 3, renderWorldCopies: false,
  attributionControl: { compact: true }
});
map.addControl(new maplibregl.NavigationControl());
var b = new maplibregl.LngLatBounds();
CITIES.features.forEach(function(f) { b.extend(f.geometry.coordinates); });
var touched = false;
function fit() { if (!touched) { map.fitBounds(b, { padding: 48, maxZoom: 9, duration: 0 }); } }
map.on('dragstart', function() { touched = true; });
map.on('zoomstart', function(e) { if (e.originalEvent) { touched = true; } });
new ResizeObserver(function() { map.resize(); fit(); }).observe(document.getElementById('map'));
map.on('load', function() {
  fit();
  map.addSource('cities', {type: 'geojson', data: CITIES});
  map.addLayer({id: 'city-dot', type: 'circle', source: 'cities',
    paint: {'circle-color': '#4A6B2A', 'circle-opacity': 0.92, 'circle-radius': 15,
            'circle-stroke-width': 2, 'circle-stroke-color': '#F6F2E9'}});
  map.addLayer({id: 'city-n', type: 'symbol', source: 'cities',
    layout: {'text-field': ['get', 'n'], 'text-font': ['Noto Sans Regular'],
             'text-size': 12, 'text-allow-overlap': true},
    paint: {'text-color': '#F6F2E9'}});
  map.addLayer({id: 'city-name', type: 'symbol', source: 'cities',
    layout: {'text-field': ['get', 'city'], 'text-font': ['Noto Sans Regular'],
             'text-size': 12, 'text-offset': [0, 1.6], 'text-anchor': 'top'},
    paint: {'text-color': '#26301E', 'text-halo-color': '#F6F2E9', 'text-halo-width': 1.4}});
  map.on('click', 'city-dot', function(e) {
    window.location.href = '/' + e.features[0].properties.slug;
  });
  map.on('mouseenter', 'city-dot', function() { map.getCanvas().style.cursor = 'pointer'; });
  map.on('mouseleave', 'city-dot', function() { map.getCanvas().style.cursor = ''; });
});
`);
}

export interface ExploreTreeFeature {
  type: "Feature";
  // Nullable to match Python: a tree with no recorded location still
  // serializes ([None, None] -> [null, null]) rather than crashing the
  // build, exactly like the unfiltered-trees quirk in search-index.json.
  geometry: { type: "Point"; coordinates: [number | null, number | null] };
  properties: { id: string; name: string; url: string; cs: string; city: string; age: string; now: 0 | 1 };
}
export interface ExploreCityRow {
  city: string;
  url: string;
  country: string;
  n: number;
  lat: number;
  lng: number;
  ph: string | null;
  rank: number;
}

/** The /explore world map: one GeoJSON circle layer per tree with native
 * clustering, plus the register layer fetched separately. Ported from the
 * inline `script` string in build_explore_page(), build_site.py:4641-4805. */
export function exploreMapScript(features: ExploreTreeFeature[], cities: ExploreCityRow[]): string {
  const geojson = JSON.stringify({ type: "FeatureCollection", features });
  const citiesJson = JSON.stringify(cities);
  return (
    mapScript(
    `
var DATA = ${geojson};
var CITIES = ${citiesJson};
// One world only (Hidde, 2026-07-29: "ik hoef niet 2 werelden te zien").
var map = new maplibregl.Map({
  container: 'map', style: '${MAP_STYLE}',
  center: [8, 48], zoom: 3.4, minZoom: 1.3,
  renderWorldCopies: false,
  attributionControl: {compact: true}
});
map.addControl(new maplibregl.NavigationControl());
new ResizeObserver(function() { map.resize(); }).observe(document.getElementById('map'));
// Location is asked HERE, in map context, never on the homepage.
map.addControl(new maplibregl.GeolocateControl({
  positionOptions: { enableHighAccuracy: true },
  showUserLocation: true, fitBoundsOptions: { maxZoom: 13.5 }
}));
// Open where the visitor is, without asking for anything (Hidde,
// 2026-07-30). The browser's own timezone gives a region for free: no
// permission prompt, no IP lookup, no third-party service, nothing stored.
// The Geolocate button above is still there for an exact fix.
var REGIONS = {
  'Europe/Amsterdam': [4.9, 52.37], 'Europe/Brussels': [4.35, 50.85],
  'Europe/London': [-0.13, 51.51], 'Europe/Dublin': [-6.26, 53.35],
  'Europe/Lisbon': [-9.14, 38.72], 'Europe/Madrid': [-3.7, 40.42],
  'Europe/Paris': [2.35, 48.86], 'Europe/Berlin': [13.4, 52.52],
  'Europe/Rome': [12.5, 41.9], 'Europe/Vienna': [16.37, 48.21],
  'Europe/Prague': [14.42, 50.09], 'Europe/Athens': [23.73, 37.98],
  'Europe/Warsaw': [21.01, 52.23], 'Europe/Istanbul': [28.98, 41.01],
  'Asia/Tokyo': [139.69, 35.69], 'Asia/Singapore': [103.82, 1.35],
  'Asia/Bangkok': [100.5, 13.75], 'America/New_York': [-74.0, 40.71],
  'Atlantic/Reykjavik': [-21.9, 64.15]
};
try {
  var tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
  if (REGIONS[tz]) { map.jumpTo({center: REGIONS[tz], zoom: 9}); }
  else if (tz && tz.indexOf('Europe/') === 0) { map.jumpTo({center: [10, 50], zoom: 4}); }
} catch (e) {}
function initTreeLayers() {
  if (map.getSource('trees')) { return; }
  map.addSource('trees', {type: 'geojson', data: DATA, cluster: true,
                          clusterMaxZoom: 11, clusterRadius: 42});
  // The season heartbeat: a soft pulse behind trees at their peak, the
  // recorded pulsing-pin idea (BACKLOG) in its cheapest honest form.
  map.addLayer({id: 'tree-pulse', type: 'circle', source: 'trees',
    filter: ['all', ['!', ['has', 'point_count']], ['==', ['get', 'now'], 1]],
    paint: {'circle-color': '#D9A13F', 'circle-opacity': 0.35, 'circle-radius': 9}});
  map.addLayer({id: 'clusters', type: 'circle', source: 'trees',
    filter: ['has', 'point_count'],
    paint: {'circle-color': '#4A6B2A', 'circle-opacity': 0.92,
            'circle-radius': ['step', ['get', 'point_count'], 14, 10, 18, 30, 24],
            'circle-stroke-width': 2, 'circle-stroke-color': '#F6F2E9'}});
  map.addLayer({id: 'cluster-count', type: 'symbol', source: 'trees',
    filter: ['has', 'point_count'],
    layout: {'text-field': ['get', 'point_count_abbreviated'],
             'text-font': ['Noto Sans Regular'], 'text-size': 12},
    paint: {'text-color': '#F6F2E9'}});
  map.addLayer({id: 'tree', type: 'circle', source: 'trees',
    filter: ['!', ['has', 'point_count']],
    paint: {'circle-color': ['case', ['==', ['get', 'now'], 1], '#D9A13F', '#4A6B2A'],
            'circle-radius': ['case', ['==', ['get', 'now'], 1], 9, 7],
            'circle-stroke-width': 2, 'circle-stroke-color': '#F6F2E9'}});
  // The register layer: officially designated trees from a government
  // register, not our own research. Visually quieter than the curated
  // trees on purpose (small, hollow, grey) so the two layers read as
  // different kinds of thing, not competing dots. No clustering (small
  // pilot count); no click-through URL, since these carry no own page.
  // Fetched rather than inlined: there are thousands of these and they would
  // otherwise be the heaviest thing on the page, loaded before the map the
  // visitor actually came for. They also only appear from zoom 8, because a
  // grey haze over Europe at world zoom tells nobody anything.
  if (!map.getSource('registers')) {
    fetch('assets/registers.json').then(function(r) { return r.json(); }).then(function(data) {
      if (!data.features.length || map.getSource('registers')) { return; }
      map.addSource('registers', {type: 'geojson', data: data});
      map.addLayer({id: 'register', type: 'circle', source: 'registers', minzoom: 8,
        paint: {'circle-color': 'rgba(0,0,0,0)', 'circle-radius': 5,
                'circle-stroke-width': 1.5, 'circle-stroke-color': '#8A8578'}});
      map.on('click', 'register', function(e) {
        var p = e.features[0].properties;
        new maplibregl.Popup({offset: 10})
          .setLngLat(e.features[0].geometry.coordinates)
          .setHTML('<strong>' + p.name + '</strong><br>' + p.designation +
                   (p.area ? ' &middot; ' + p.area : '') +
                   '<br><em>From the official register, not yet verified by us.</em>')
          .addTo(map);
      });
      map.on('mouseenter', 'register', function() { map.getCanvas().style.cursor = 'pointer'; });
      map.on('mouseleave', 'register', function() { map.getCanvas().style.cursor = ''; });
    }).catch(function() { /* the map works without this layer */ });
  }
  // One map experience, not two (Hidde, 2026-07-30): the world map is the
  // launcher, the city page (map plus tree list) is the destination. A
  // cluster that is entirely one city's trees opens that city's page; only
  // a multi-city cluster zooms. getClusterLeaves/ExpansionZoom are Promises
  // in MapLibre v4 (the old callback form failed silently once).
  map.on('click', 'clusters', function(e) {
    var f = map.queryRenderedFeatures(e.point, {layers: ['clusters']})[0];
    var src = map.getSource('trees');
    src.getClusterLeaves(f.properties.cluster_id, 1000, 0).then(function(leaves) {
      var cities = {};
      leaves.forEach(function(l) { cities[l.properties.cs] = true; });
      var keys = Object.keys(cities);
      if (keys.length === 1) { window.location.href = keys[0]; return; }
      src.getClusterExpansionZoom(f.properties.cluster_id).then(function(zoom) {
        map.easeTo({center: f.geometry.coordinates, zoom: zoom + 0.5, duration: 700});
      });
    });
  });
  map.on('click', 'tree', function(e) {
    var p = e.features[0].properties;
    var badge = p.now == 1 ? ' <span class="pop-now">at its best now</span>' : '';
    // The heart rides in the popup (the 2026-08-14 consistency pass: the map
    // is where AllTrails' hearts live most densely, and ours had none).
    // TREE_ACTIONS_JS handles the click by delegation; atPaintSaves() sets
    // the saved state on this late-added node.
    var heart = '<button class="save-btn heart-btn heart-compact" type="button" data-tree="' + p.id +
                '" data-name="' + p.name.replace(/"/g, '&quot;') + '" aria-pressed="false">' +
                '<svg class="heart" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21C6.5 16.3 3.5 13 3.5 9.6 3.5 7 5.5 5 8 5c1.6 0 3.1.8 4 2.1C12.9 5.8 14.4 5 16 5c2.5 0 4.5 2 4.5 4.6 0 3.4-3 6.7-8.5 11.4z"/></svg>' +
                '<span>Save</span></button>';
    new maplibregl.Popup({offset: 12})
      .setLngLat(e.features[0].geometry.coordinates)
      .setHTML('<strong>' + p.name + '</strong>' + badge + '<br>' + p.age + ' &middot; ' + p.city +
               '<br><a href="' + p.url + '">See this tree &rarr;</a> &middot; ' +
               '<a href="' + p.cs + '">All ' + p.city + ' trees &rarr;</a><br>' + heart)
      .addTo(map);
    if (window.atPaintSaves) window.atPaintSaves();
  });
  ['clusters', 'tree'].forEach(function(l) {
    map.on('mouseenter', l, function() { map.getCanvas().style.cursor = 'pointer'; });
    map.on('mouseleave', l, function() { map.getCanvas().style.cursor = ''; });
  });
}
map.on('style.load', initTreeLayers);
if (map.isStyleLoaded()) { initTreeLayers(); }
// ---- The city chooser (Hidde, 2026-07-31, final form: "waarom kom ik
// dan niet direct op de City Page?"). The map is where you choose; the
// city page is the city experience, full stop. The panel lists up to ten
// cities in view, most likely first, and every click goes straight there.
var panel = document.getElementById('ex-panel');
function fmtCard(c) {
  var ph = c.ph ? '<span class="exc-ph"><img src="' + c.ph + '" alt="" loading="lazy"></span>' : '<span class="exc-ph exc-noph"></span>';
  return '<a class="exc-card" href="' + c.url + '">' + ph +
         '<span class="exc-body"><b>' + c.city + '</b>' +
         '<span>' + c.n + ' trees &middot; ' + c.country + '</span></span></a>';
}
function renderPanel() {
  if (!panel) return;
  var b = map.getBounds();
  var cities = CITIES.filter(function(c) { return b.contains([c.lng, c.lat]); });
  if (!cities.length) {
    panel.innerHTML = '<p class="exc-empty">No mapped cities in view. Zoom out, or <a href="contribute">be the first to map one here</a>.</p>';
    return;
  }
  var head = cities.length === 1 ? cities[0].city : 'Cities in view';
  panel.innerHTML = '<div class="exc-cityhead"><h2>' + head + '</h2></div>' +
    cities.slice(0, 10).map(fmtCard).join('');
}
map.on('moveend', renderPanel);
map.on('load', renderPanel);
renderPanel();

// The pulse: radius and opacity breathe on a 2s cycle. Paint-property
// animation only, no per-frame data churn; stops costing anything when the
// tab is hidden because rAF pauses.
(function pulse(ts) {
  if (map.getLayer && map.getLayer('tree-pulse')) {
    var t = (ts % 2000) / 2000;
    map.setPaintProperty('tree-pulse', 'circle-radius', 9 + t * 9);
    map.setPaintProperty('tree-pulse', 'circle-opacity', 0.4 * (1 - t));
  }
  requestAnimationFrame(pulse);
})(0);
`)
  );
}

/** "the Netherlands" in a sentence, "The Netherlands" at its start. */
export function countryName(intro: { country: string; article?: string }, capital = false): string {
  const art = intro.article;
  if (!art) return intro.country;
  const displayArt = capital ? art.charAt(0).toUpperCase() + art.slice(1) : art;
  return `${displayArt} ${intro.country}`;
}
