// The three behaviours the app's tree page has and the web page did not, ported
// 2026-09-24 (Hidde, on the page redesign: "do all functionalities also work
// like the app?"). Each one names the Swift it copies.
//
//   1. THE MAP IN THE CORNER (TreeDetail.swift `hero`, MapInset.swift). A small
//      live map sits on the photograph; tapping it swaps the two, so the map
//      fills the hero and the photograph shrinks into the corner; tapping that
//      swaps back. A second button opens the full map, which on the web is the
//      city map opened on this tree (#tree=<id>). On a desktop the same map
//      lives in the side card instead, because there is room for it and a
//      72px map on a 1200px page is a stamp.
//   2. TAKE ME THERE (Kit/Directions.swift). On an iPhone the first tap asks
//      Apple Maps or Google Maps and remembers the answer, which is what the
//      app does. Everywhere else the link simply opens Google Maps, walking.
//   3. SHOW US WHERE IT IS (PlacePin.swift). On an approximate pin, a full
//      screen map with the pin fixed in the middle: drag the map until the
//      pin sits on the tree, and send. Same row, same words, as the app sends:
//      kind correction, the coordinate in location_hint.
//
// One map element serves both hosts (inset and side card) and is MOVED between
// them, so the page never runs two WebGL maps, and the smoke test's
// maplibregl-canvas is there at every width.

import { MAP_STYLE, MAP_CREDIT, SUPABASE_URL, SUPABASE_KEY } from "./site-config";
import { mapScript } from "./map";

export function treePageScript(lat: number, lng: number): string {
  return mapScript(`
var LAT = ${lat}, LNG = ${lng};
var mapEl = document.getElementById('map');
var hero = document.querySelector('.td-hero');
var insetHost = document.querySelector('.td-inset');
var sideHost = document.querySelector('.td-side-map');
var wide = window.matchMedia('(min-width: 900px)');
var map = null;

function interactive(on) {
  if (!map) return;
  ['dragPan', 'touchZoomRotate', 'doubleClickZoom', 'keyboard'].forEach(function (h) {
    if (map[h]) { on ? map[h].enable() : map[h].disable(); }
  });
}
function place() {
  var host = wide.matches ? sideHost : insetHost;
  if (host && mapEl && mapEl.parentNode !== host) host.appendChild(mapEl);
  if (wide.matches && hero) hero.classList.remove('td-show-map');
  if (map) {
    map.resize();
    interactive(wide.matches || (hero && hero.classList.contains('td-show-map')));
    map.jumpTo({ center: [LNG, LAT] });
  }
}
if (mapEl) {
  place();
  map = new maplibregl.Map({
    container: mapEl, style: '${MAP_STYLE}', center: [LNG, LAT], zoom: 15,
    scrollZoom: false, attributionControl: false
  });
  map.addControl(new maplibregl.AttributionControl({ compact: true, customAttribution: ${JSON.stringify(MAP_CREDIT)} }), 'top-left');
  var dot = document.createElement('div');
  dot.className = 'pin pin-dot';
  new maplibregl.Marker({ element: dot }).setLngLat([LNG, LAT]).addTo(map);
  map.on('load', function () { map.resize(); });
  interactive(wide.matches);
  if (wide.addEventListener) wide.addEventListener('change', place);
}

// The swap. The inset is a button over the photograph; while the map is big
// the photograph's own corner button swaps back.
function swap(toMap) {
  if (!hero) return;
  hero.classList.toggle('td-show-map', toMap);
  interactive(toMap);
  // Redraw once the 0.22s grow has finished, and once more when the browser
  // says it has: a map redrawn mid-transition keeps the 72px frame's centre,
  // which parks the pin in the top-left corner of the big map.
  setTimeout(recentre, 260);
}
function recentre() { if (map) { map.resize(); map.jumpTo({ center: [LNG, LAT] }); } }
if (insetHost) insetHost.addEventListener('transitionend', function (e) {
  if (e.propertyName === 'width') recentre();
});
var insetBtn = document.querySelector('.td-inset-hit');
if (insetBtn) insetBtn.addEventListener('click', function () { swap(true); });
var backBtn = document.querySelector('.td-photo-back');
if (backBtn) backBtn.addEventListener('click', function () { swap(false); });

// Back, the arrow on the photograph. The link is the city page, which is the
// honest destination for somebody who arrived from a search engine; when they
// came from a page of ours, back means the page they came from, as it does in
// the app and on AllTrails.
var backA = document.querySelector('.td-back');
if (backA) backA.addEventListener('click', function (e) {
  var ref = document.referrer;
  if (ref && ref.indexOf(location.origin) === 0 && history.length > 1) {
    e.preventDefault();
    history.back();
  }
});

// Take me there. iOS detection is the one signin-js.ts already uses, iPadOS
// included (it reports itself as a Mac with touch).
var ua = navigator.userAgent || '';
var isIOS = /iPhone|iPad|iPod/.test(ua) || (ua.indexOf('Macintosh') > -1 && navigator.maxTouchPoints > 1);
var pick = document.querySelector('.dir-pick');
var URLS = {
  apple: 'https://maps.apple.com/?daddr=' + LAT + ',' + LNG + '&dirflg=w',
  google: 'https://www.google.com/maps/dir/?api=1&destination=' + LAT + ',' + LNG + '&travelmode=walking'
};
function remembered() { try { return localStorage.getItem('at_maps_app'); } catch (e) { return null; } }
document.addEventListener('click', function (e) {
  var a = e.target.closest && e.target.closest('a.dir-link');
  if (!a || !isIOS) return;
  var app = remembered();
  e.preventDefault();
  if (app && URLS[app]) { location.href = URLS[app]; return; }
  if (pick && pick.showModal) pick.showModal(); else location.href = URLS.google;
});
if (pick) {
  pick.addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (e.target === pick || (b && b.value === 'cancel')) { pick.close(); return; }
    if (!b || !URLS[b.value]) return;
    try { localStorage.setItem('at_maps_app', b.value); } catch (err) {}
    pick.close();
    location.href = URLS[b.value];
  });
}

// Show us where it is.
var pinDlg = document.querySelector('.pin-dlg');
var pinMap = null;
function session() {
  try {
    var s = JSON.parse(localStorage.getItem('ancienttrees_session'));
    return (s && s.expires_at > Date.now() / 1000) ? s : null;
  } catch (e) { return null; }
}
function metresFrom(a, b) {
  var R = 6371000, r = Math.PI / 180;
  var dLat = (b[1] - a[1]) * r, dLng = (b[0] - a[0]) * r;
  var h = Math.sin(dLat / 2) * Math.sin(dLat / 2)
    + Math.cos(a[1] * r) * Math.cos(b[1] * r) * Math.sin(dLng / 2) * Math.sin(dLng / 2);
  return Math.round(2 * R * Math.asin(Math.sqrt(h)));
}
if (pinDlg) {
  var sendBtn = pinDlg.querySelector('.pin-send');
  var moved = pinDlg.querySelector('.pin-moved');
  var note = pinDlg.querySelector('.pin-note');
  var acct = pinDlg.querySelector('.pin-acct');
  var metres = 0;
  function paintMoved() {
    if (!pinMap) return;
    var c = pinMap.getCenter();
    metres = metresFrom([LNG, LAT], [c.lng, c.lat]);
    moved.textContent = metres < 5 ? pinDlg.dataset.zoom : pinDlg.dataset.moved.replace('{m}', metres);
    sendBtn.disabled = metres < 5;
  }
  document.addEventListener('click', function (e) {
    if (!e.target.closest || !e.target.closest('.td-pin-open')) return;
    e.preventDefault();
    pinDlg.showModal();
    if (acct) acct.hidden = !!session();
    if (!pinMap) {
      pinMap = new maplibregl.Map({
        container: pinDlg.querySelector('.pin-map'), style: '${MAP_STYLE}',
        center: [LNG, LAT], zoom: 17, attributionControl: false
      });
      pinMap.on('move', paintMoved);
      pinMap.on('load', function () { pinMap.resize(); });
    } else {
      setTimeout(function () { pinMap.resize(); }, 30);
    }
    paintMoved();
  });
  pinDlg.querySelector('.pin-cancel').addEventListener('click', function () { pinDlg.close(); });
  sendBtn.addEventListener('click', function () {
    var s = session();
    if (!s) {
      pinDlg.close();
      if (window.atOpenSignIn) window.atOpenSignIn(pinDlg.dataset.name, 'feedback');
      return;
    }
    var c = pinMap.getCenter();
    sendBtn.disabled = true;
    sendBtn.textContent = pinDlg.dataset.sending;
    fetch('${SUPABASE_URL}/rest/v1/submissions', {
      method: 'POST',
      headers: { 'apikey': '${SUPABASE_KEY}', 'Authorization': 'Bearer ' + s.access_token,
                 'Content-Type': 'application/json', 'Prefer': 'return=minimal' },
      body: JSON.stringify({
        kind: 'correction',
        city: pinDlg.dataset.city,
        tree: pinDlg.dataset.tree + ' (' + pinDlg.dataset.name + ')',
        location_hint: c.lat.toFixed(6) + ', ' + c.lng.toFixed(6),
        why: 'Moved the pin on the map, ' + metres + ' m from the published position. Our pin was marked approximate.',
        page: location.pathname
      })
    }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      pinDlg.classList.add('is-sent');
      note.textContent = pinDlg.dataset.done;
      try { at.track('pin-moved'); } catch (e) {}
    }).catch(function () {
      sendBtn.disabled = false;
      sendBtn.textContent = pinDlg.dataset.send;
      note.textContent = pinDlg.dataset.failed;
    });
  });
}
`);
}
