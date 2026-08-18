// Ported from city_map_script(), build_site.py:1532-2058. The city page's
// map: tree pins, walk switching (redraw, not navigation), the zoom-out
// city chooser, the passport (localStorage, ancienttrees_seen — see
// ARCHITECTURE.md, this key never changes), and "where am I" GPS.
//
// Note: .seen-btn (the actual check-in button element) is referenced here
// and in the CSS, but build_city_page never renders one into the tree
// cards in the current production site — the passport/check-in wiring
// below is real and ported faithfully, but nothing currently triggers it.
// Confirmed by grep: no template anywhere emits `class="seen-btn"`.
//
// Below, cityMapScript() returns its whole body as a template literal that
// ships verbatim as an inline <script> (see mapScript() in ./map): no
// bundler or module graph reaches that text. That's why metresBetween(),
// defined inside the template, can't import haversineKm from ./walks the
// way this file's own build-time code does above: it is the one unavoidable
// duplicate of the haversine formula in the codebase. Keep it in step with
// walks.ts::haversineKm and geo.py::km by hand if either changes.
import { MAP_STYLE } from "./site-config";
import { mapScript } from "./map";
import { kmLabel } from "./walks";
import type { WalkMarker, Walk } from "./walks";

export interface OtherCity {
  slug: string;
  city: string;
  country: string;
  n: number;
  ph: string | null;
  rank: number;
  lat: number;
  lng: number;
}

export function cityMapScript(
  markers: WalkMarker[],
  center: [number, number],
  route: Walk | null,
  otherCities: OtherCity[],
  walks: Walk[]
): string {
  const data = JSON.stringify(markers);
  const routeCoords = JSON.stringify(route && markers.length > 1 ? route.order.map((i) => [markers[i].lng, markers[i].lat]) : []);
  const walksJson = JSON.stringify(
    walks.map((w) => ({
      coords: w.shape ?? w.order.map((i) => [markers[i].lng, markers[i].lat]),
      members: w.order,
      url: w.url ?? "",
      label: w.label ?? "",
      name: w.name ?? "",
      meta: `about ${kmLabel(w.km)} km, ${w.duration ?? ""} on foot`,
      combined: Boolean(w.combined),
    }))
  );
  const otherCitiesJson = JSON.stringify({
    type: "FeatureCollection",
    features: otherCities.map((c) => ({
      type: "Feature",
      geometry: { type: "Point", coordinates: [c.lng, c.lat] },
      properties: { slug: c.slug, city: c.city, n: c.n },
    })),
  });
  const ranked = [...otherCities].sort((a, b) => (a.rank ?? 99) - (b.rank ?? 99) || b.n - a.n);
  const chooserCitiesJson = JSON.stringify(
    ranked.map((c) => ({ url: c.slug, city: c.city, country: c.country, n: c.n, ph: c.ph, lat: c.lat, lng: c.lng }))
  );

  return mapScript(`
var markers = ${data};
var map = new maplibregl.Map({
  container: 'map',
  style: '${MAP_STYLE}',
  center: [${center[1]}, ${center[0]}],
  zoom: 10.5,
  scrollZoom: true,
  attributionControl: { compact: true }
});
map.addControl(new maplibregl.NavigationControl());
map.addControl(new maplibregl.FullscreenControl());
map.on('load', function() { map.resize(); });
new ResizeObserver(function() { map.resize(); }).observe(document.getElementById('map'));
var OTHER_CITIES = ${otherCitiesJson};
if (OTHER_CITIES.features.length) {
  map.on('load', function() {
    if (map.getSource('othercities')) { return; }
    map.addSource('othercities', {type: 'geojson', data: OTHER_CITIES});
    map.addLayer({id: 'othercity', type: 'circle', source: 'othercities', maxzoom: 9,
      paint: {'circle-color': '#4A6B2A', 'circle-opacity': 0.92, 'circle-radius': 13,
              'circle-stroke-width': 2, 'circle-stroke-color': '#F6F2E9'}});
    map.addLayer({id: 'othercity-n', type: 'symbol', source: 'othercities', maxzoom: 9,
      layout: {'text-field': ['get', 'n'], 'text-font': ['Noto Sans Regular'], 'text-size': 11,
               'text-allow-overlap': true},
      paint: {'text-color': '#F6F2E9'}});
    map.on('click', 'othercity', function(e) {
      window.location.href = '/' + e.features[0].properties.slug;
    });
    map.on('mouseenter', 'othercity', function() { map.getCanvas().style.cursor = 'pointer'; });
    map.on('mouseleave', 'othercity', function() { map.getCanvas().style.cursor = ''; });
  });
}
var CHOOSER_CITIES = ${chooserCitiesJson};
var cityPanel = document.querySelector('.panel');
// The chooser goes INSIDE the sheet's scroller, never beside it. .panel's own
// children are the grab handle and the body, and the loop below hides every
// sibling of the chooser: appending here meant that zooming out until other
// cities appeared hid the grab handle itself, which is the only thing you can
// drag, so the sheet froze where it stood (Hidde, 2026-08-18: "dan loopt de
// bottombar vast, je kunt hem dan niet omhoog slepen").
var chooserHost = (cityPanel && cityPanel.querySelector('.sheet-body')) || cityPanel;
var chooserBox = null;
var chooserOn = false;
var homeZoom = null;
function ensureChooserBox() {
  if (chooserBox) { return chooserBox; }
  chooserBox = document.createElement('div');
  chooserBox.className = 'panel-chooser';
  chooserBox.style.display = 'none';
  chooserHost.appendChild(chooserBox);
  return chooserBox;
}
function chooserCard(c) {
  var ph = c.ph ? '<span class="exc-ph"><img src="' + c.ph + '" alt="" loading="lazy"></span>' : '<span class="exc-ph exc-noph"></span>';
  return '<a class="exc-card" href="/' + c.url + '">' + ph +
         '<span class="exc-body"><b>' + c.city + '</b>' +
         '<span>' + c.n + ' trees &middot; ' + c.country + '</span></span></a>';
}
function updatePanelMode() {
  if (!cityPanel || !CHOOSER_CITIES.length) { return; }
  var z = map.getZoom();
  var onAt = homeZoom === null ? 9.5 : Math.min(9.5, homeZoom - 1.2);
  if (!chooserOn && z <= onAt) { chooserOn = true; }
  else if (chooserOn && z >= onAt + 1) { chooserOn = false; }
  var box = ensureChooserBox();
  for (var i = 0; i < chooserHost.children.length; i++) {
    var el = chooserHost.children[i];
    if (el !== box) { el.style.display = chooserOn ? 'none' : ''; }
  }
  if (chooserOn) {
    var b = map.getBounds();
    var inview = CHOOSER_CITIES.filter(function(c) { return b.contains([c.lng, c.lat]); });
    box.innerHTML = '<div class="exc-cityhead"><h2>Cities in view</h2></div>' +
      (inview.length ? inview.slice(0, 10).map(chooserCard).join('')
                     : '<p class="exc-empty">No other mapped cities in view yet. Keep zooming out.</p>');
    box.style.display = '';
  } else {
    box.style.display = 'none';
  }
}
if (markers.length > 1) {
  var _b = new maplibregl.LngLatBounds();
  markers.forEach(function(m) { _b.extend([m.lng, m.lat]); });
  var _el = document.getElementById('map');
  var _pad = Math.max(30, Math.min(90, Math.floor(Math.min(_el.clientWidth, _el.clientHeight) * 0.16)));
  map.fitBounds(_b, { padding: _pad, maxZoom: 14.5, duration: 0 });
  homeZoom = map.getZoom();
}
map.on('moveend', updatePanelMode);

var pins = [];
var activeIdx = -1;

function setActive(idx, fly, scroll) {
  // Selecting a tree OUTSIDE the chosen walk releases the walk instead of
  // leaving the tree dimmed under it (Hidde, 2026-08-14: "the tree stays in
  // opacity mode instead of jumping out of the hike and towards the tree").
  // The person's intent moved from the route to the tree; the filter follows.
  if (typeof activeWalk !== 'undefined' && activeWalk >= 0 && WALKS[activeWalk] &&
      WALKS[activeWalk].members.indexOf(idx) === -1) {
    showWholeCity();
  }
  if (activeIdx >= 0) {
    pins[activeIdx].classList.remove('active');
    document.getElementById('tree-' + (activeIdx + 1)).classList.remove('active');
  }
  activeIdx = idx;
  var m = markers[idx];
  pins[idx].classList.add('active');
  var card = document.getElementById('tree-' + (idx + 1));
  card.classList.add('active');
  // On a phone the cards live inside the bottom sheet, and picking a tree
  // means opening THAT tree rather than scrolling a list behind a map. The
  // sheet publishes this hook; on desktop it is undefined and nothing changes.
  if (window.atSheetFocus) { window.atSheetFocus(card.dataset.treeId); }
  if (scroll) { card.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }
  // A tree centred in the map element is a tree hidden behind the sheet, since
  // the sheet covers the lower half of it. Maps recentres on the part of the
  // map you can still see, so this does too: the offset moves the target up by
  // half the difference between the element's centre and the visible centre.
  var flyOffset = [0, 0];
  if (fly && window.atSheetTop) {
    var sheetTop = window.atSheetTop();
    var mapEl = document.getElementById('map');
    if (sheetTop !== null && mapEl) {
      var mr = mapEl.getBoundingClientRect();
      var visibleMid = (mr.top + Math.min(mr.bottom, sheetTop)) / 2;
      flyOffset = [0, Math.round(visibleMid - (mr.top + mr.bottom) / 2)];
    }
  }
  if (fly) { map.flyTo({ center: [m.lng, m.lat], zoom: 14.5, duration: 1200, offset: flyOffset }); }
}

var bounds = new maplibregl.LngLatBounds();
markers.forEach(function(m, idx) {
  var el = document.createElement('div');
  el.className = 'pin-tree';
  el.title = m.name;
  el.innerHTML = '<svg viewBox="0 0 40 40" fill="currentColor" aria-hidden="true">' + m.icon + '</svg>'
               + '<span class="pin-rank">' + m.label + '</span>';
  el.addEventListener('click', function(e) {
    e.stopPropagation();
    setActive(idx, true, true);
  });
  new maplibregl.Marker({ element: el }).setLngLat([m.lng, m.lat]).addTo(map);
  pins.push(el);
  bounds.extend([m.lng, m.lat]);
});
if (markers.length > 1) { map.fitBounds(bounds, { padding: 70, maxZoom: 13 }); }

document.querySelectorAll('.tree-card').forEach(function(card, idx) {
  card.addEventListener('click', function(e) {
    if (e.target.closest('a')) { return; }
    setActive(idx, true, false);
  });
});

var routeCoords = ${routeCoords};
function addWalkLayer() {
  if (routeCoords.length < 2 || map.getSource('walk')) { return; }
  map.addSource('walk', {
    type: 'geojson',
    data: { type: 'Feature', geometry: { type: 'LineString', coordinates: routeCoords } }
  });
  map.addLayer({
    id: 'walk-casing', type: 'line', source: 'walk',
    layout: { 'line-cap': 'round', 'line-join': 'round' },
    paint: { 'line-color': '#fff', 'line-width': 8, 'line-opacity': 0.85 }
  });
  map.addLayer({
    id: 'walk', type: 'line', source: 'walk',
    layout: { 'line-cap': 'round', 'line-join': 'round' },
    paint: { 'line-color': '#3D5C1E', 'line-width': 4.5, 'line-opacity': 0.95,
              'line-dasharray': [1.4, 1.1] }
  });
}
if (map.isStyleLoaded()) { addWalkLayer(); } else { map.on('styledata', addWalkLayer); }

function addAllWalksLayer() {
  if (WALKS.length < 2 || map.getSource('walks-all')) { return; }
  map.addSource('walks-all', {
    type: 'geojson',
    // The combined option is the sum of lines already on the map: drawing it
    // grey as well would double every segment, so only the real walks show.
    data: { type: 'FeatureCollection', features: WALKS.map(function(w, i) {
      return { type: 'Feature', properties: { idx: i },
               geometry: { type: 'LineString', coordinates: w.coords } };
    }).filter(function(f) { return !WALKS[f.properties.idx].combined; }) }
  });
  map.addLayer({
    id: 'walks-all-hit', type: 'line', source: 'walks-all',
    layout: { 'line-cap': 'round', 'line-join': 'round' },
    paint: { 'line-color': '#000', 'line-width': 16, 'line-opacity': 0.001 }
  });
  map.addLayer({
    id: 'walks-all-casing', type: 'line', source: 'walks-all',
    layout: { 'line-cap': 'round', 'line-join': 'round' },
    paint: { 'line-color': '#fff', 'line-width': 7, 'line-opacity': 0.7 }
  });
  map.addLayer({
    id: 'walks-all', type: 'line', source: 'walks-all',
    layout: { 'line-cap': 'round', 'line-join': 'round' },
    paint: { 'line-color': '#4b5563', 'line-width': 3, 'line-opacity': 0.3,
              'line-dasharray': [1.4, 1.1] }
  });
  map.on('click', 'walks-all-hit', function(e) {
    if (e.features && e.features.length) { selectWalk(e.features[0].properties.idx); }
  });
  map.on('mouseenter', 'walks-all-hit', function() { map.getCanvas().style.cursor = 'pointer'; });
  map.on('mouseleave', 'walks-all-hit', function() { map.getCanvas().style.cursor = ''; });
}
function setAllWalksFilter(activeIdx) {
  // Hide the grey copy of whatever is selected, so the chosen walk shows once
  // in green rather than twice in two colours.
  if (!map.getLayer('walks-all')) { return; }
  // Selecting the combined option hides every grey copy: its green line
  // covers all of them, and grey under green reads as a third walk.
  var f = activeIdx < 0 ? null
        : (WALKS[activeIdx] && WALKS[activeIdx].combined) ? ['==', ['get', 'idx'], -1]
        : ['!=', ['get', 'idx'], activeIdx];
  map.setFilter('walks-all', f);
  map.setFilter('walks-all-hit', f);
  if (map.getLayer('walks-all-casing')) { map.setFilter('walks-all-casing', f); }
}
if (map.isStyleLoaded()) { addAllWalksLayer(); } else { map.on('styledata', addAllWalksLayer); }

var WALKS = ${walksJson};
var wantCoords = [];
function drawWalk(coords) {
  wantCoords = coords;
  var src = null;
  try { src = map.getSource('walk'); } catch (e) { src = null; }
  if (src) {
    src.setData({ type: 'Feature', geometry: { type: 'LineString', coordinates: coords } });
    return;
  }
  if (!map.isStyleLoaded()) {
    map.once('styledata', function() { drawWalk(wantCoords); });
    return;
  }
  addWalkLayer();
}
function selectWalk(idx) {
  var w = WALKS[idx];
  if (!w) { return; }
  activeWalk = idx;
  setAllWalksFilter(idx);
  routeCoords = w.coords;
  drawWalk(w.coords);
  var go = document.getElementById('route-go');
  if (go) { go.href = w.url; }
  var lab = document.getElementById('route-label');
  if (lab) { lab.textContent = w.label; }
  var meta = document.getElementById('route-meta');
  if (meta) { meta.textContent = w.meta; }
  var nm = document.querySelector('.route-name');
  if (nm) { nm.textContent = w.name; nm.hidden = !w.name; }
  var on = {};
  w.members.forEach(function(i) { on[i] = true; });
  pins.forEach(function(el, i) { el.classList.toggle('pin-off', !on[i]); });
  document.querySelectorAll('.tree-card').forEach(function(card, i) {
    card.classList.toggle('card-off', !on[i]);
  });
  document.querySelectorAll('.walk-pick').forEach(function(b, i) {
    b.classList.toggle('is-on', i === idx);
    b.setAttribute('aria-pressed', i === idx ? 'true' : 'false');
  });
  if (w.coords.length > 1) {
    var bb = new maplibregl.LngLatBounds();
    w.coords.forEach(function(c) { bb.extend(c); });
    map.fitBounds(bb, { padding: 70, maxZoom: 15 });
  }
}
var activeWalk = -1;
function showWholeCity() {
  activeWalk = -1;
  setAllWalksFilter(-1);
  drawWalk([]);
  pins.forEach(function(el) { el.classList.remove('pin-off'); });
  document.querySelectorAll('.tree-card').forEach(function(card) {
    card.classList.remove('card-off');
  });
  document.querySelectorAll('.walk-pick').forEach(function(b) {
    b.classList.remove('is-on');
    b.setAttribute('aria-pressed', 'false');
  });
  // The bar goes back to the lead walk too, or deselecting leaves it naming a
  // walk no chip shows as chosen ("Both walks" with nothing selected).
  var w0 = WALKS[0];
  if (w0) {
    routeCoords = w0.coords;
    var go = document.getElementById('route-go');
    if (go) { go.href = w0.url; }
    var lab = document.getElementById('route-label');
    if (lab) { lab.textContent = w0.label; }
    var meta = document.getElementById('route-meta');
    if (meta) { meta.textContent = w0.meta; }
    var nm = document.querySelector('.route-name');
    if (nm) { nm.textContent = w0.name; nm.hidden = !w0.name; }
  }
  if (markers.length > 1) { map.fitBounds(bounds, { padding: 70, maxZoom: 13 }); }
}
document.querySelectorAll('.walk-pick').forEach(function(btn) {
  btn.addEventListener('click', function() {
    var idx = parseInt(btn.getAttribute('data-walk'), 10);
    if (idx === activeWalk) { showWholeCity(); } else { selectWalk(idx); }
  });
});
if (WALKS.length === 1 && WALKS[0].coords.length > 1) {
  drawWalk(WALKS[0].coords);
} else if (WALKS.length > 1) {
  drawWalk([]);
}

var SEEN_KEY = 'ancienttrees_seen';

function readSeen() {
  try { return JSON.parse(localStorage.getItem(SEEN_KEY)) || []; }
  catch (e) { return []; }
}
function writeSeen(list) {
  try { localStorage.setItem(SEEN_KEY, JSON.stringify(list)); } catch (e) {}
}

function paintPassport() {
  var seen = readSeen();
  var here = 0;
  markers.forEach(function(m, idx) {
    var got = seen.indexOf(m.id) !== -1;
    if (got) { here++; }
    pins[idx].classList.toggle('seen', got);
  });
  document.querySelectorAll('.seen-btn').forEach(function(btn) {
    var got = seen.indexOf(btn.dataset.tree) !== -1;
    btn.setAttribute('aria-pressed', got ? 'true' : 'false');
    btn.querySelector('.seen-text').textContent = got ? 'Visited' : 'Check in at this tree';
  });
  var box = document.getElementById('passport');
  if (box) {
    document.getElementById('passport-count').textContent = here;
    box.hidden = here === 0;
    box.classList.toggle('complete', here === markers.length);
    var total = document.getElementById('passport-total');
    if (seen.length > here) {
      total.textContent = seen.length + ' trees in total, across every city.';
    } else if (here === markers.length) {
      total.textContent = 'Every tree here. Go find another city.';
    } else {
      total.textContent = '';
    }
  }
}

function metresBetween(lat1, lng1, lat2, lng2) {
  var R = 6371000, p = Math.PI / 180;
  var a = Math.sin((lat2 - lat1) * p / 2) * Math.sin((lat2 - lat1) * p / 2)
        + Math.cos(lat1 * p) * Math.cos(lat2 * p)
        * Math.sin((lng2 - lng1) * p / 2) * Math.sin((lng2 - lng1) * p / 2);
  return 2 * R * Math.asin(Math.sqrt(a));
}

function flash(btn, msg, ms) {
  var t = btn.querySelector('.seen-text'), was = t.textContent;
  t.textContent = msg;
  setTimeout(function() { if (t.textContent === msg) { t.textContent = was; } }, ms || 4000);
}

document.querySelectorAll('.seen-btn').forEach(function(btn) {
  btn.addEventListener('click', function(e) {
    e.stopPropagation();
    var id = btn.dataset.tree;
    var seen = readSeen();

    if (seen.indexOf(id) !== -1) {
      seen.splice(seen.indexOf(id), 1);
      writeSeen(seen);
      paintPassport();
      return;
    }

    if (!navigator.geolocation) {
      flash(btn, 'This browser cannot check where you are');
      return;
    }
    flash(btn, 'Checking where you are...', 20000);
    navigator.geolocation.getCurrentPosition(function(pos) {
      var away = metresBetween(pos.coords.latitude, pos.coords.longitude,
                               parseFloat(btn.dataset.lat), parseFloat(btn.dataset.lng));
      if (away <= parseFloat(btn.dataset.radius)) {
        var list = readSeen();
        if (list.indexOf(id) === -1) { list.push(id); }
        writeSeen(list);
        paintPassport();
      } else {
        var far = away > 2000 ? Math.round(away / 1000) + ' km' : Math.round(away) + ' m';
        flash(btn, 'Still ' + far + ' away. Check in at the tree.', 6000);
      }
    }, function(err) {
      flash(btn, err.code === 1 ? 'Location needed to check in' : 'Could not find you. Try again.', 6000);
    }, { enableHighAccuracy: true, maximumAge: 30000, timeout: 15000 });
  });
});

if (location.hash.indexOf('#trees=') === 0) {
  var incoming = decodeURIComponent(location.hash.slice(7)).split(',').filter(Boolean);
  if (incoming.length) {
    var merged = readSeen();
    incoming.forEach(function(id) { if (merged.indexOf(id) === -1) { merged.push(id); } });
    writeSeen(merged);
    history.replaceState(null, '', location.pathname + location.search);
  }
}

var saveBtn = document.getElementById('passport-save');
if (saveBtn) {
  saveBtn.addEventListener('click', function() {
    var link = location.origin + location.pathname + '#trees=' + encodeURIComponent(readSeen().join(','));
    function done(msg) {
      saveBtn.textContent = msg;
      setTimeout(function() { saveBtn.textContent = 'Save or move to another device'; }, 4000);
    }
    if (navigator.share) {
      navigator.share({ title: 'My trees', url: link }).then(function() { done('Saved'); },
                                                              function() {});
    } else if (navigator.clipboard) {
      navigator.clipboard.writeText(link).then(function() { done('Link copied. Bookmark it or mail it to yourself.'); },
                                               function() { window.prompt('Copy this link:', link); });
    } else {
      window.prompt('Copy this link:', link);
    }
  });
}

paintPassport();

var gpsBtn = document.getElementById('gps-btn');
var meMarker = null, watchId = null;
if (gpsBtn && navigator.geolocation) {
  gpsBtn.addEventListener('click', function() {
    if (watchId !== null) {
      navigator.geolocation.clearWatch(watchId);
      watchId = null;
      if (meMarker) { meMarker.remove(); meMarker = null; }
      gpsBtn.setAttribute('aria-pressed', 'false');
      gpsBtn.textContent = 'Where am I';
      return;
    }
    gpsBtn.textContent = 'Finding you...';
    watchId = navigator.geolocation.watchPosition(function(pos) {
      var here = [pos.coords.longitude, pos.coords.latitude];
      if (!meMarker) {
        var dot = document.createElement('div');
        dot.className = 'pin-me';
        meMarker = new maplibregl.Marker({ element: dot }).setLngLat(here).addTo(map);
        map.flyTo({ center: here, zoom: 15, duration: 1000 });
      } else {
        meMarker.setLngLat(here);
      }
      gpsBtn.setAttribute('aria-pressed', 'true');
      gpsBtn.textContent = 'Hide me';
    }, function(err) {
      gpsBtn.textContent = err.code === 1 ? 'Location blocked' : 'Location unavailable';
      watchId = null;
      setTimeout(function() { gpsBtn.textContent = 'Where am I'; }, 3000);
    }, { enableHighAccuracy: true, maximumAge: 10000, timeout: 10000 });
  });
} else if (gpsBtn) {
  gpsBtn.hidden = true;
}
`);
}
