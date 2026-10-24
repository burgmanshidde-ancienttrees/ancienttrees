// Ported from map_head()/country_map_script()/single_pin_script(),
// build_site.py:1199-1230ish, 4045-4101. Raw <script>/<link> tags loading
// MapLibre from a CDN, matching the current site exactly rather than going
// through the bundled npm package (see site-config.ts's note on MAPLIBRE_JS).
import {MAPLIBRE_JS, MAPLIBRE_CSS, MAP_STYLE, MAP_CREDIT} from "./site-config";
import { NO_PHOTO_CARD } from "./images";

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
/** The five seconds (2026-09-12, Hidde: "does it need to be visible, is rather
 * not show it"). It does need to be reachable and it does not need to be read.
 * The OSMF attribution guideline of 2021-06-25 allows a credit to collapse
 * "automatically on map interaction such as panning, clicking, or zooming" or
 * "automatically after five seconds", on one condition: "If the attribution has
 * been collapsed, the user must still be able to find the licence information
 * if they look for it, for example from an '(i)' button in the corner of the
 * map." MapLibre already does the first half on a touch; a visitor who never
 * touches the map was left reading a band across the top forever.
 *
 * So: five seconds, then it is a 24 point (i) and nothing else. That is the
 * floor rather than a preference. OpenFreeMap's own terms say plainly
 * "Attribution is required", and the guideline's collapsed state still wants
 * the (i) there, so it cannot go altogether. */
const COLLAPSE_ATTRIBUTION = `
setTimeout(function () {
  var list = document.querySelectorAll('.maplibregl-ctrl-attrib');
  for (var i = 0; i < list.length; i++) {
    list[i].classList.remove('maplibregl-compact-show');
    if (list[i].tagName === 'DETAILS') { list[i].open = false; }
  }
}, 5000);`;


/** WHICH PINS SHOW: THE AIRBNB WAY, ON EVERY MAP (Hidde, 2026-10-24: "doe de
 *  Airbnb-manier overal: volledige pins voor wat past, kleine stippen voor de
 *  rest, nooit bubbels, een tik opent altijd de boom. Web en app.").
 *
 *  Looked at the same day (CONVENTIONS.md, "How close two pins have to be"):
 *  Airbnb never piles listings into a counted bubble at any zoom. It draws
 *  a ranked handful of full pins, small unlabelled dots for the rest, and
 *  zooming in draws more; a tap always opens a listing and nothing zooms for
 *  you. Google Maps draws every result pin, overlapping where it must, no
 *  counts. The counted bubbles this replaced (2026-10-04 to 10-24) were
 *  MapKit's and the web clustering libraries' default, and Hidde's verdict on
 *  them: "je wil ook niet nodeloos bubbels openklikken en je wil trouwens ook
 *  niet dat je altijd inzoomt bij bubbels klikken."
 *
 *  So every map draws every tree, and the only question is which get the
 *  full pin: a tree with a photograph before one without, then the one more
 *  readers saved (`pr` on the feature, pinPriority(); Airbnb ranks by what
 *  you are likely to book, we rank by what is worth the walk), then our own
 *  order, and a pin that would collide
 *  with one already placed is drawn as a dot instead. PIN_DISTANCE is the
 *  collision rule, centre to centre, the same 40 the app uses (TreeMap.swift,
 *  pinDistance) and supercluster's own default. The circle-pin maps (explore,
 *  country, state, My trees) hand the placing to MapLibre's symbol collision
 *  (PINS_JS); the city map does the same pass over its DOM pins
 *  (city-map-script.ts). The one bubble left is a same-spot stack, below.
 *  qa: check_every_map_shows_pins_the_same_way(). */
export const PIN_DISTANCE = 40;

/** WHICH TREE GETS THE FULL PIN where two collide, as a sort key, lower
 *  first: a photograph before none, and among equals the tree more readers
 *  saved to Want to go (Hidde, 2026-10-24: "i think photo and likes are the
 *  best way"; saves from data/tree-saves.json, lib/saves.ts). The app's
 *  TreeMap.swift pinPriority is the same arithmetic; qa holds the two equal.
 *  Kept small so a feature carries one short number. */
export function pinPriority(hasPhoto: boolean, saves: number): number {
  return (hasPhoto ? 0 : 100000) - Math.min(Math.max(0, Math.round(saves)), 99999);
}
/** The full pin on the circle-pin maps: a moss disc with a 2px cream ring. */
export const PIN_RADIUS = 7;
/** The dot a tree becomes where its pin did not fit. */
export const DOT_RADIUS = 4;
/** The same-spot stack's bubble (CONVENTIONS.md 2026-10-15), 26px plus ring,
 *  the app's stackPin at 32 points. */
export const STACK_RADIUS = 13;
/** From this zoom a same-spot stack is its bubble; below it the stack is one
 *  ordinary pin, because below it two pins a street apart would overlap
 *  anyway and the bubble would read as the clustering we no longer do. The
 *  same number as the app's stackZoom (TreeMap.swift). */
export const STACK_ZOOM = 14;

/** TREES ON ONE SPOT, on every map (Hidde, 2026-10-15: "map interaction need
 *  to stay consistent so do everywhere"). The city map and the app do it
 *  first (spreadStack() in city-map-script.ts, MapLayers.spread in
 *  TreeMap.swift); this is the same behaviour for maps that draw trees as
 *  circles in a GeoJSON source: /explore, the country maps, My trees.
 *
 *  Trees on one coordinate drew one dot over the other with only the top one
 *  reachable, and no zoom parts them.
 *  So before the data goes in, atMarkPiles() gives every feature a `pile`:
 *  0 alone, n on the one feature that stands for a pile of n, -1 on the rest.
 *  The tree layer draws pile 0 only; atPileLayers() adds a bubble (the
 *  cluster's own) for the rest. A tap flies to zoom 17 on the spot and the
 *  dots spring apart round it on thin legs, Leaflet's spiderfy; a dot opens
 *  its tree through `open`; a tap on the map or your own zoom folds them.
 *  Clusters still count every tree, hidden ones included.
 *  CONVENTIONS.md, "Two trees on exactly the same spot". */
export const PILES_JS = `
// The piles as the DATA has them. Never read back from the map: a feature
// from the map's tiles has its coordinate rounded to the tile grid, so it no
// longer matches its own spot (the app's first tap only zoomed because of
// this, 2026-10-15).
var atPiles = [];
function atPileKey(c) { return c[1].toFixed(5) + ',' + c[0].toFixed(5); }
function atMarkPiles(features) {
  var by = {};
  features.forEach(function(f) {
    var c = f.geometry && f.geometry.coordinates;
    if (!c || c[0] == null || c[1] == null) { return; }
    var k = atPileKey(c);
    (by[k] = by[k] || []).push(f);
  });
  atPiles = [];
  Object.keys(by).forEach(function(k) {
    var g = by[k];
    g.forEach(function(f, i) { f.properties.pile = g.length < 2 ? 0 : (i === 0 ? g.length : -1); f.properties.pk = k; });
    if (g.length > 1) { atPiles.push({c: g[0].geometry.coordinates.slice(), fs: g}); }
  });
  return features;
}
function atPileLayers(map, source, treeLayer, open, hollow) {
  var pileOnly = ['all', ['!', ['has', 'point_count']], ['>=', ['coalesce', ['get', 'pile'], 0], 2]];
  map.setFilter(treeLayer, ['all', ['!', ['has', 'point_count']], ['==', ['coalesce', ['get', 'pile'], 0], 0]]);
  // The bubble only from STACK_ZOOM; below it the stack is one ordinary pin
  // (atPinLayers draws the pile's first tree there).
  map.addLayer({id: treeLayer + '-pile', type: 'circle', source: source, filter: pileOnly, minzoom: ${STACK_ZOOM},
    paint: {'circle-color': '#4A6B2A', 'circle-opacity': 0.92, 'circle-radius': ${STACK_RADIUS},
            'circle-stroke-width': 2, 'circle-stroke-color': '#F6F2E9'}});
  map.addLayer({id: treeLayer + '-pile-n', type: 'symbol', source: source, filter: pileOnly, minzoom: ${STACK_ZOOM},
    layout: {'text-field': ['to-string', ['get', 'pile']], 'text-font': ['Noto Sans Regular'],
             'text-size': 12, 'text-allow-overlap': true},
    paint: {'text-color': '#F6F2E9'}});
  var spread = [], tapAt = 0;
  // The bubble is a map layer, so while its pile is spread it is filtered out.
  function showBubbles(except) {
    var f = except ? ['all', pileOnly, ['!=', ['get', 'pk'], except]] : pileOnly;
    map.setFilter(treeLayer + '-pile', f);
    map.setFilter(treeLayer + '-pile-n', f);
  }
  function fold() {
    if (!spread.length) { return; }
    spread.forEach(function(m) { m.remove(); });
    spread = [];
    showBubbles(null);
  }
  function fan(pile) {
    fold();
    var c = pile.c, g = pile.fs, n = g.length, R = n <= 2 ? 24 : 30;
    showBubbles(atPileKey(c));
    var legs = document.createElement('div');
    legs.className = 'stack-legs-host';
    var html = '<i class="stack-dot"></i>';
    g.forEach(function(f, i) {
      var a = n === 2 ? Math.PI * i : -Math.PI / 2 + i * 2 * Math.PI / n;
      html += '<i class="stack-leg" style="width:' + (R - 9) + 'px;transform:rotate(' + (a * 180 / Math.PI) + 'deg)"></i>';
      var d = document.createElement('button');
      d.type = 'button';
      d.className = 'pile-dot' + (hollow && hollow(f.properties) ? ' pile-dot--hollow' : '');
      if (f.properties.name) { d.setAttribute('aria-label', f.properties.name); d.title = f.properties.name; }
      d.addEventListener('click', function(e) { e.stopPropagation(); tapAt = Date.now(); open(f.properties, c); });
      spread.push(new maplibregl.Marker({element: d, offset: [Math.round(R * Math.cos(a)), Math.round(R * Math.sin(a))]})
        .setLngLat(c).addTo(map));
    });
    legs.innerHTML = html;
    spread.unshift(new maplibregl.Marker({element: legs}).setLngLat(c).addTo(map));
  }
  map.on('click', treeLayer + '-pile', function(e) {
    tapAt = Date.now();
    // The nearest pile on screen to the tap: the bubble was drawn there.
    var best = null, bestD = 30 * 30;
    atPiles.forEach(function(p) {
      var q = map.project(p.c), dx = q.x - e.point.x, dy = q.y - e.point.y;
      if (dx * dx + dy * dy < bestD) { bestD = dx * dx + dy * dy; best = p; }
    });
    if (!best) { return; }
    if (map.getZoom() >= 16.5) { fan(best); return; }
    map.easeTo({center: best.c, zoom: 17, duration: 900});
    setTimeout(function() { fan(best); }, 950);
  });
  map.on('click', function() { if (Date.now() - tapAt > 400) { fold(); } });
  map.on('zoomstart', function(e) { if (e.originalEvent) { fold(); } });
  map.on('mouseenter', treeLayer + '-pile', function() { map.getCanvas().style.cursor = 'pointer'; });
  map.on('mouseleave', treeLayer + '-pile', function() { map.getCanvas().style.cursor = ''; });
}`;

/** THE PINS OF A CIRCLE-PIN MAP (explore, country, state, My trees, and the
 *  other cities on a city map), the Airbnb way: see PIN_DISTANCE. Two layers
 *  on one plain source. Under: every tree as a dot. Over: the full pin, a
 *  symbol whose placement MapLibre decides, lowest `pr` first, and a symbol
 *  that would collide with one already placed is simply not drawn, which
 *  leaves its dot showing. A tap on either opens the tree; a symbol that was
 *  not placed is not in queryRenderedFeatures, so the tap falls through to
 *  the dot. The same-spot stacks (PILES_JS) are added on top.
 *  `hollowExpr`, when given, is a MapLibre expression naming the features
 *  drawn hollow (My trees: a tree saved but not yet collected). */
export const PINS_JS = `
function atPinImage(map, name, hollow) {
  if (map.hasImage(name)) { return; }
  var r = ${PIN_RADIUS}, dpr = Math.min(window.devicePixelRatio || 1, 3), d = (r + 2) * 2;
  var c = document.createElement('canvas');
  c.width = d * dpr; c.height = d * dpr;
  var g = c.getContext('2d');
  g.scale(dpr, dpr);
  g.beginPath();
  g.arc(d / 2, d / 2, hollow ? r - 0.25 : r, 0, Math.PI * 2);
  if (!hollow) { g.fillStyle = '#4A6B2A'; g.fill(); }
  g.lineWidth = hollow ? 2.5 : 2;
  g.strokeStyle = hollow ? '#4A6B2A' : '#F6F2E9';
  g.stroke();
  map.addImage(name, g.getImageData(0, 0, c.width, c.height), {pixelRatio: dpr});
}
function atPinLayers(map, source, treeLayer, open, hollowExpr, hollow) {
  atPinImage(map, 'at-pin', false);
  atPinImage(map, 'at-pin-hollow', true);
  var loose = ['all', ['!', ['has', 'point_count']], ['==', ['coalesce', ['get', 'pile'], 0], 0]];
  // A same-spot pile's first tree stands for the pile below STACK_ZOOM, where
  // the bubble is not drawn (atPileLayers).
  var pileHead = ['all', ['!', ['has', 'point_count']], ['>=', ['coalesce', ['get', 'pile'], 0], 2]];
  var dotPaint = {'circle-color': hollowExpr ? ['case', hollowExpr, 'rgba(0,0,0,0)', '#4A6B2A'] : '#4A6B2A',
                  'circle-radius': ${DOT_RADIUS},
                  'circle-stroke-width': 1.5,
                  'circle-stroke-color': hollowExpr ? ['case', hollowExpr, '#4A6B2A', '#F6F2E9'] : '#F6F2E9'};
  var pinLayout = {'icon-image': hollowExpr ? ['case', hollowExpr, 'at-pin-hollow', 'at-pin'] : 'at-pin',
                   'icon-allow-overlap': false, 'icon-ignore-placement': false,
                   'icon-padding': ${(PIN_DISTANCE - (PIN_RADIUS + 2) * 2) / 2},
                   'symbol-sort-key': ['coalesce', ['get', 'pr'], 1]};
  map.addLayer({id: treeLayer + '-dot', type: 'circle', source: source, filter: loose, paint: dotPaint});
  map.addLayer({id: treeLayer + '-head-dot', type: 'circle', source: source, filter: pileHead, maxzoom: ${STACK_ZOOM}, paint: dotPaint});
  map.addLayer({id: treeLayer, type: 'symbol', source: source, filter: loose, layout: pinLayout});
  map.addLayer({id: treeLayer + '-head', type: 'symbol', source: source, filter: pileHead, maxzoom: ${STACK_ZOOM}, layout: pinLayout});
  [treeLayer, treeLayer + '-dot', treeLayer + '-head', treeLayer + '-head-dot'].forEach(function(l) {
    map.on('click', l, function(e) {
      var f = e.features[0];
      open(f.properties, f.geometry.coordinates);
    });
    map.on('mouseenter', l, function() { map.getCanvas().style.cursor = 'pointer'; });
    map.on('mouseleave', l, function() { map.getCanvas().style.cursor = ''; });
  });
  atPileLayers(map, source, treeLayer, open, hollow);
}`;
export function mapScript(body: string): string {
  return `\n<script defer src="${MAPLIBRE_JS}"></script>\n<script>\n` +
    `document.addEventListener("DOMContentLoaded", function () {\n${body}\n${COLLAPSE_ATTRIBUTION}\n});\n</script>\n`;
}

/** MapLibre's stylesheet. The `preconnect` to unpkg.com that used to sit here
 * went with the vendoring on 2026-08-16 (see site-config.ts): warming a
 * connection to a host we no longer call is a wasted DNS lookup, and our own
 * origin is already connected. */
export function mapHead(): string {
  return `<link rel="stylesheet" href="${MAPLIBRE_CSS}">`;
}

/** A single-pin map: the tree page's own map, ported from
 * single_pin_script(), build_site.py:1203-1219. */
export function singlePinScript(lat: number, lng: number): string {
  return mapScript(`
var map = new maplibregl.Map({
  container: 'map', style: '${MAP_STYLE}',
  center: [${lng}, ${lat}], zoom: 14.5, scrollZoom: false,
  attributionControl: false
});
map.addControl(new maplibregl.AttributionControl({compact: true, customAttribution: ${JSON.stringify(MAP_CREDIT)}}), 'top-left');
map.addControl(new maplibregl.NavigationControl());
map.on('load', function() { map.resize(); });
var el = document.createElement('div');
// A dot, not a numbered pill. There is exactly one pin on this map, so a "1"
// on it was never telling anybody anything.
el.className = 'pin pin-dot';
new maplibregl.Marker({ element: el }).setLngLat([${lng}, ${lat}]).addTo(map);
`);
}

export interface CountryMapCity {
  slug: string;
  city: string;
  count: number;
  /** pinPriority(): which tree gets the full pin first. */
  markers: { lat: number; lng: number; url?: string; pr?: number }[];
}

/** Every tree in the country, drawn the way /explore and the app draw them
 *  (PINS_JS): a pin or a dot per tree, and either opens its tree. */
export function countryMapScript(cities: CountryMapCity[],
                                 frame?: [[number, number], [number, number]],
                                 focus?: [[number, number], [number, number]]): string {
  // THE APP'S COUNTRY MAP (Hidde, 2026-10-04, on Italy: "deze stad preview is
  // niet echt mooi trek dit ook gelijk met app"). It was one dot per CITY with
  // its count and its name printed beside it, and in a country with forty
  // cities the names and numbers piled over each other. The app's country
  // page draws its TreeMap instead: every tree, no labels of our own over
  // the base map's. So this is the explore map's pin style and its one rule:
  // a pin or a dot opens its tree.
  const data = {
    type: "FeatureCollection",
    features: cities.flatMap((c) => c.markers.map((m) => ({
      type: "Feature",
      geometry: { type: "Point", coordinates: [m.lng, m.lat] },
      properties: { cs: "/" + c.slug, url: m.url ?? "/" + c.slug, pr: m.pr ?? 1 },
    }))),
  };
  return mapScript(`${PILES_JS}${PINS_JS}
var TREES = atMarkPiles(${JSON.stringify(data)}.features);
TREES = { type: 'FeatureCollection', features: TREES };
var map = new maplibregl.Map({
  container: 'map', style: '${MAP_STYLE}',
  center: [0, 0], zoom: 3, renderWorldCopies: false,
  scrollZoom: false, attributionControl: false
});
map.addControl(new maplibregl.AttributionControl({compact: true, customAttribution: ${JSON.stringify(MAP_CREDIT)}}), 'top-left');
map.addControl(new maplibregl.NavigationControl({showCompass: false}));
var b = new maplibregl.LngLatBounds();
TREES.features.forEach(function(f) { b.extend(f.geometry.coordinates); });
// A country whose cities all hug one border names extra ground to show
// (map_frame in data/countries), so Canada's map is not centred on the US.
var FRAME = ${JSON.stringify(frame ?? null)};
if (FRAME) { b.extend(FRAME[0]); b.extend(FRAME[1]); }
// A country with trees overseas opens on its mainland instead (map_focus):
// Martinique, Tenerife and Hawaii stay on the map, one zoom out away.
var FOCUS = ${JSON.stringify(focus ?? null)};
if (FOCUS) { b = new maplibregl.LngLatBounds(FOCUS[0], FOCUS[1]); }
var touched = false;
function fit() {
  if (touched) return;
  map.fitBounds(b, { padding: 36, maxZoom: 9, duration: 0 });
  // On a phone held upright the width decides the zoom, so the frame sits in
  // the middle with a band of neighbour above and below it: for Canada that
  // lower band was the US and Mexico (Hidde, 2026-09-24). Slide the view north
  // until the frame's southern edge meets the bottom, so the spare height
  // shows more of the country instead of its neighbour.
  if (FRAME) {
    var h = map.getContainer().clientHeight;
    var y = map.project([FRAME[0][0], Math.min(FRAME[0][1], FRAME[1][1])]).y;
    var dy = y - (h - 48);
    if (dy < 0) { map.panBy([0, dy], { duration: 0 }); }
  }
}
map.on('dragstart', function() { touched = true; });
map.on('zoomstart', function(e) { if (e.originalEvent) { touched = true; } });
new ResizeObserver(function() { map.resize(); fit(); }).observe(document.getElementById('map'));
map.on('load', function() {
  fit();
  map.addSource('trees', {type: 'geojson', data: TREES});
  atPinLayers(map, 'trees', 'tree', function(p) { window.location.href = p.url; }, null, null);
});
`);
}

export interface ExploreTreeFeature {
  type: "Feature";
  // Nullable to match Python: a tree with no recorded location still
  // serializes ([None, None] -> [null, null]) rather than crashing the
  // build, exactly like the unfiltered-trees quirk in search-index.json.
  geometry: { type: "Point"; coordinates: [number | null, number | null] };
  properties: {
    id: string; name: string; url: string; cs: string; city: string; age: string; now: 0 | 1;
    /** Behind a ticket. The filter hides these; 241 of 3,055 trees. */
    paid?: 0 | 1;
    /** pinPriority(): which tree gets the full pin where two collide. */
    pr?: number;
    /** Index into the species list the page ships beside the features. An
     *  index rather than the name, because 3,055 copies of "Pedunculate Oak"
     *  is 45KB of the same twelve words. */
    sp?: number;
  };
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

/** The /explore world map: every tree as a pin or a dot (PINS_JS), plus the
 * register layer fetched separately. Ported from the
 * inline `script` string in build_explore_page(), build_site.py:4641-4805. */
export function exploreMapScript(features: ExploreTreeFeature[], cities: ExploreCityRow[],
                                 species: string[] = []): string {
  const geojson = JSON.stringify({ type: "FeatureCollection", features });
  const citiesJson = JSON.stringify(cities);
  const speciesJson = JSON.stringify(species);
  return (
    mapScript(
    `${PILES_JS}${PINS_JS}
var DATA = ${geojson};
var CITIES = ${citiesJson};
var SPECIES = ${speciesJson};
// THE FILTER MODEL AND THE ACCOUNT CHIPS COME BEFORE THE MAP (2026-10-07):
// MapLibre throws where WebGL is unavailable, and everything below the
// constructor then never runs. A chip that cannot ask for sign-in because
// the map failed is the dead control Hidde keeps finding; it asks first.
// ---- THE FILTER ROW (2026-09-12).
//
// Convention, looked up rather than invented (CONVENTIONS.md): Google Maps
// puts a scrolling row of capsule chips over the top of the map and nothing
// else; AllTrails and Airbnb put a Filters BUTTON that opens a sheet, which is
// the right shape for eight filters and the wrong one for four. Our own app
// draws the chip row, so the website draws the same row: same capsules, same
// words, same order.
//
// WHICH CHIPS, and this is the half that needed checking rather than copying.
// MapFilters.swift still DEFINES five (peaking, photo, walkable, species,
// mine) and the app's row carried four of them for a while. It does not now:
// what ships on the phone today is the walk chip, Favourites, My trees and
// Species, because Hidde cut the rest, and his reasons are in MapTab.swift.
// "At their best" is a pulse on the pins rather than a filter, "with a photo"
// was doing the editorial order's job, and "within 2 km" was doing the
// distance-ordered list's job. So the website takes the row the app actually
// has, minus the walk chip, which is Plus.
//
// Plus one the app has not got: FREE TO VISIT (Hidde, 2026-09-12: "ik zou nog
// wel een filter willen bouwen voor betaalde bomen waar je een ticket voor
// moet kopen - dat je die weg kunt halen"). It is the oldest complaint about
// this site wearing a control: a city page that turns out to be a garden page
// (2026-08-23, "ik heb liever 34 goede bereikbare dan 39"). 241 of our trees
// stand behind a ticket, and somebody who wants an afternoon out for nothing
// should be able to say so. It belongs in the app's row too; that half needs
// a Mac and is written down.
//
// FILTERING RE-SOURCES, it does not hide a layer: the same-spot piles are
// marked on the data (atMarkPiles), so what is hidden must leave the data.
var FILTERS = { free: false, fav: false, mine: false, sp: -1 };
function filtersOn() {
  return FILTERS.free || FILTERS.fav || FILTERS.mine || FILTERS.sp >= 0;
}
function keepsTree(f) {
  var p = f.properties;
  if (FILTERS.free && p.paid === 1) return false;
  if (FILTERS.sp >= 0 && p.sp !== FILTERS.sp) return false;
  if (FILTERS.fav && !(window.atHasSaved && window.atHasSaved(p.id))) return false;
  if (FILTERS.mine && !(window.atHasVisited && window.atHasVisited(p.id))) return false;
  return true;
}
function applyFilters() {
  var src = (typeof map !== 'undefined' && map && map.getSource) ? map.getSource('trees') : null;
  if (!src) return;
  var kept = filtersOn() ? DATA.features.filter(keepsTree) : DATA.features;
  src.setData({ type: 'FeatureCollection', features: atMarkPiles(kept) });
  var note = document.getElementById('mf-count');
  if (note) {
    // A number only while a filter is on. The map's own copy carries no counts
    // on purpose (2026-07-29), and this is not copy: it is the answer to what
    // you just pressed, and zero has to be sayable.
    note.hidden = !filtersOn();
    note.textContent = kept.length === 0 ? 'No trees match'
      : (kept.length === 1 ? '1 tree' : kept.length + ' trees');
  }
}
// Both lists live in the account, so both chips need one. Signed out they ask
// rather than emptying the map, which is the rule Hidde set for the app's own
// two: "als je uitgelogd op favourites of my trees filter klikt moet er ook
// een inlog scherm opkomen."
// AND THE SERVER DECIDES whether there is an account, through the one door
// every gated tap uses (atCollection.gate, 2026-10-05). This chip used to ask
// the browser (a stored session believed on its own say-so), so a token the
// server had already refused let the filter switch on and empty the map, with
// no sign-in in sight (Hidde, 2026-10-07: "if I press favourites or mytrees
// as a filter it should force people to login").
function toggleFilter(b, f) {
  FILTERS[f] = !FILTERS[f];
  b.classList.toggle('is-on', FILTERS[f]);
  b.setAttribute('aria-pressed', FILTERS[f] ? 'true' : 'false');
  applyFilters();
}
document.querySelectorAll('.mf[data-f]').forEach(function(b) {
  b.addEventListener('click', function() {
    var f = b.dataset.f;
    if ((f === 'fav' || f === 'mine') && !FILTERS[f]) {
      var C = window.atCollection;
      var ask = function() {
        // Signed out: sign in and come back with THIS chip on, rather than
        // landing on an unfiltered map having been asked for nothing.
        if (window.atOpenSignIn) window.atOpenSignIn(b.dataset.label || b.textContent.trim(), null, { kind: 'filter', filter: f });
      };
      if (C && C.gate) C.gate(function() { toggleFilter(b, f); }, ask);
      else ask();
      return;
    }
    toggleFilter(b, f);
  });
});
// Back from signing in with a chip to switch on (signin-js hands it over).
if (window.atPendingFilter) {
  var pf = window.atPendingFilter; window.atPendingFilter = null;
  var pb = document.querySelector('.mf[data-f="' + pf + '"]');
  var PC = window.atCollection;
  if (pb && !FILTERS[pf] && PC && PC.gate) {
    // After the saved and seen lists have arrived, or the filter keeps nothing.
    var jobs = [];
    if (window.atSyncSaves) jobs.push(Promise.resolve(window.atSyncSaves()));
    if (window.atSyncVisited) jobs.push(Promise.resolve(window.atSyncVisited()));
    PC.gate(function() { Promise.all(jobs).then(function() { toggleFilter(pb, pf); }).catch(function() {}); }, function() {});
  }
}

// One world only (Hidde, 2026-07-29: "ik hoef niet 2 werelden te zien").
var map = new maplibregl.Map({
  container: 'map', style: '${MAP_STYLE}',
  center: [8, 48], zoom: 3.4, minZoom: 1.3,
  renderWorldCopies: false,
  attributionControl: false
});
map.addControl(new maplibregl.AttributionControl({compact: true, customAttribution: ${JSON.stringify(MAP_CREDIT)}}), 'top-left');
map.addControl(new maplibregl.NavigationControl());
new ResizeObserver(function() { map.resize(); }).observe(document.getElementById('map'));
// Location is asked HERE, in map context, never on the homepage.
var _geo = new maplibregl.GeolocateControl({
  positionOptions: { enableHighAccuracy: true },
  showUserLocation: true, fitBoundsOptions: { maxZoom: 13.5 }
});
map.addControl(_geo);
// Arriving from the search field's "Trees near me" row (#near) triggers the
// locate control once the map is ready, so that row does what it says
// instead of merely opening the map. The permission prompt still belongs to
// the browser and only appears because the visitor asked for it.
// On /explore itself the row only changes the hash and the page does not
// reload, so a hashchange has to trigger it too (Hidde, 2026-10-12: "er
// gebeurt niks").
function _nearFromHash() {
  if (location.hash !== '#near') { return; }
  if (map.loaded()) { _geo.trigger(); }
  else { map.once('load', function() { setTimeout(function() { _geo.trigger(); }, 300); }); }
  try { history.replaceState(null, '', location.pathname + location.search); } catch (e) {}
}
_nearFromHash();
window.addEventListener('hashchange', _nearFromHash);
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
  atMarkPiles(DATA.features);
  map.addSource('trees', {type: 'geojson', data: DATA});
  // The season heartbeat (a pulse and a gold dot behind trees at their peak)
  // is switched off: Hidde, 2026-10-03, "its not good enough lets look at it
  // later". The 'now' property still travels in DATA, so bringing it back is
  // a halo layer, its requestAnimationFrame loop and the two gold cases on
  // the tree layer (git history has all three).
  // A pin or a dot opens its tree, as in the app (TreeMap.swift onSelectTree,
  // and the city page since 2026-10-04). The popup this replaced was a third
  // way of showing a tree, with its own links and its own Save pill.
  atPinLayers(map, 'trees', 'tree', function(p) { if (p.url) { window.location.href = p.url; } }, null, null);
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
}
map.on('style.load', initTreeLayers);
if (map.isStyleLoaded()) { initTreeLayers(); }

// The species chip wears the chosen species, the way the app's does
// (FilterChipLabel(label: filters.species ?? "Species")). The select is the
// invisible tap layer over it, so the filled state and the word both belong to
// the pill around it rather than to the field.
var spPick = document.getElementById('mf-species');
var spWrap = document.getElementById('mf-species-wrap');
var spLabel = document.getElementById('mf-species-label');
if (spPick) {
  var spAny = spLabel ? spLabel.textContent : '';
  spPick.addEventListener('change', function() {
    FILTERS.sp = spPick.value === '' ? -1 : parseInt(spPick.value, 10);
    if (spWrap) spWrap.classList.toggle('is-on', FILTERS.sp >= 0);
    if (spLabel) {
      spLabel.textContent = FILTERS.sp < 0 ? spAny
        : spPick.options[spPick.selectedIndex].textContent;
    }
    applyFilters();
  });
}
// The account's two lists arrive after this runs, so a chip pressed while they
// are still in flight repaints when they land.
window.atRefilterMap = applyFilters;
// ---- The city chooser (Hidde, 2026-07-31, final form: "waarom kom ik
// dan niet direct op de City Page?"). The map is where you choose; the
// city page is the city experience, full stop. The panel lists up to ten
// cities in view, most likely first, and every click goes straight there.
var panel = document.getElementById('ex-panel');
function fmtCard(c) {
// The no-photo drawing is interpolated at BUILD time, so the script text that
// ships still carries no import: one drawing for every card on the site, rather
// than the empty beige rectangle this line used to emit (2026-09-17).
  var ph = c.ph ? '<span class="exc-ph"><img src="' + c.ph + '"' + (c.ph2 ? ' srcset="' + c.ph2 + '"' : '') + ' alt="" loading="lazy"></span>' : '${NO_PHOTO_CARD}';
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

`)
  );
}

/** "the Netherlands" in a sentence, "The Netherlands" at its start. */
/** YOUR OWN MAP, on your own profile.
 *
 * Hidde, 2026-09-02, having put the Polarsteps profile beside ours: "kun je
 * het helemaal gelijk trekken met polarsteps - dat je dus ook een persoonlijke
 * kaart naast je account krijgt met jouw bomen - zoals op de app account
 * pagina." Polarsteps gives half the profile to a world map of where you have
 * been; our own app puts the map above the profile sheet with your trees
 * pinned on it. Both make the same point, which is that a collection is a
 * shape rather than a list.
 *
 * It is the SAME map as everywhere else: the same style, the same wrapper, the
 * same .split skeleton the city and explore pages share, because the one thing
 * this project has learned twice about maps is that a second implementation
 * drifts (CLAUDE.md, one layout for map pages).
 *
 * What differs is where the pins come from. Every other map bakes its features
 * at build time; this one cannot, because whose trees they are is only known
 * once somebody signs in. So it starts empty and profile-js hands it the
 * features through atSetMyTrees() once the account has answered. An empty map
 * is the honest first frame: it is what a collection with nothing in it looks
 * like.
 */
export function myTreesMapScript(): string {
  return mapScript(`${PILES_JS}${PINS_JS}
var map = new maplibregl.Map({
  container: 'map', style: '${MAP_STYLE}',
  center: [8, 48], zoom: 2.6, minZoom: 1.3,
  renderWorldCopies: false,
  attributionControl: false
});
map.addControl(new maplibregl.AttributionControl({compact: true, customAttribution: ${JSON.stringify(MAP_CREDIT)}}), 'top-left');
map.addControl(new maplibregl.NavigationControl());
new ResizeObserver(function() { map.resize(); }).observe(document.getElementById('map'));

var EMPTY = { type: 'FeatureCollection', features: [] };
var pending = null;

function initMine() {
  if (map.getSource('mine')) { return; }
  map.addSource('mine', { type: 'geojson', data: EMPTY });
  // TWO KINDS OF PIN, because the profile holds two independent lists and
  // they mean opposite things: a tree you have stood in front of is done, a
  // tree you saved is still ahead of you. Filled moss for collected, hollow
  // for a favourite, which is the same filled-versus-hollow language the
  // heart itself uses. A pin or a dot opens the tree.
  // A tree only you have may have no page at all: sharing is what gives it
  // one, and somebody who turned that off has no url to point at. Straight
  // to the tree when it has a page, as every other pin does since
  // 2026-10-04; the name alone when sharing is off and there is no page.
  atPinLayers(map, 'mine', 'mine-tree', function(p, c) {
    if (p.url) { window.location.href = p.url; return; }
    new maplibregl.Popup({offset: 12}).setLngLat(c)
      .setHTML('<strong>' + p.name + '</strong><br>' + p.city).addTo(map);
  }, ['!=', ['get', 'got'], 1], function(p) { return p.got !== 1; });
  if (pending) { paint(pending); pending = null; }
}

function paint(features) {
  map.getSource('mine').setData({ type: 'FeatureCollection', features: atMarkPiles(features) });
  if (!features.length) { return; }
  // Frame the whole collection. One tree gets a city-level zoom rather than
  // a bounding box of nothing.
  var b = new maplibregl.LngLatBounds();
  features.forEach(function(f) { b.extend(f.geometry.coordinates); });
  if (features.length === 1) { map.easeTo({ center: features[0].geometry.coordinates, zoom: 12 }); }
  else { map.fitBounds(b, { padding: 70, maxZoom: 12, duration: 700 }); }
}

// Called by profile-js once the account has said which trees are yours. It
// may arrive before or after the style loads, so both orders work.
window.atSetMyTrees = function(features) {
  if (map.getSource('mine')) { paint(features); } else { pending = features; }
};

map.on('style.load', initMine);
if (map.isStyleLoaded()) { initMine(); }
`);
}

export function countryName(intro: { country: string; article?: string }, capital = false): string {
  const art = intro.article;
  if (!art) return intro.country;
  const displayArt = capital ? art.charAt(0).toUpperCase() + art.slice(1) : art;
  return `${displayArt} ${intro.country}`;
}
