// THE ONE WAY A MAP SHOWS A TAPPED TREE, on every map of the website: the city
// map, /explore in every language, the country and state maps, and your own
// map on the profile (Hidde, 2026-10-24, after the Airbnb card went onto the
// city map and nowhere else: "kun je altijd de city maps en de explore map
// gelijk houden ... kan dat gewoon een en hetzelfde ding worden?"). It is the
// fourth time the map interaction was asked to be the same everywhere, so the
// interaction lives here once and qa.py's check_one_tree_card_on_every_map()
// refuses a map that builds its own or that jumps straight to a page.
//
// Airbnb's map (CONVENTIONS.md, "Tapping a pin on a map that has a list in a
// sheet"): the pin is marked, a card with the photograph appears, the card
// opens the listing, its heart saves, a tap on the map or Escape lets it go.
// On a desktop the card stands beside the pin, never over it. On a phone it is
// the map's width less 16 a side, 16 above the bottom with the sheet stepped
// away (2026-10-25), and
// the map's own buttons lift above it (--map-pop-lift); the map only moves
// when the pin would sit behind the card.
//
// The card itself is the one tree card (TreeCard.astro). A page that has the
// tree's card in its list hands that element over (the city page); a map with
// thousands of trees and no list of them gets the same markup from
// /api/cards.json through atCollection.card (collection-js.ts), the card the
// saved list already draws.
//
// Ships as text inside mapScript()'s body, like PINS_JS: nothing in it can
// import, so the two build-time words it needs are interpolated here.
import { icon } from "./icons";
import { ui } from "./i18n";

export function mapCardJs(lang = "en"): string {
  return `
function atMapCard(map, opts) {
  opts = opts || {};
  var phone = window.matchMedia('(max-width: 800px)');
  // How far beside the pin the card stands on a desktop: a DOM pin with its
  // drawing is wider than a circle pin.
  var gap = opts.gap || 24;
  var el = null, at = null, openedAt = 0;
  function close() {
    if (!el) return;
    el.remove(); el = null; at = null;
    document.documentElement.style.removeProperty('--map-pop-lift');
    if (window.atSheetAway) window.atSheetAway(false);
    if (opts.onClose) opts.onClose();
  }
  function place() {
    if (!el || !at) return;
    var p = map.project(at);
    var W = map.getContainer().clientWidth, H = map.getContainer().clientHeight;
    var w = el.offsetWidth, h = el.offsetHeight;
    if (phone.matches) {
      var mr = map.getContainer().getBoundingClientRect();
      var st = window.atSheetTop ? window.atSheetTop() : null;
      var bottom = (st !== null ? Math.min(mr.bottom, st) : mr.bottom) - mr.top;
      el.style.left = '16px';
      el.style.top = Math.max(16, bottom - h - 16) + 'px';
      document.documentElement.style.setProperty('--map-pop-lift', (h + 12) + 'px');
      return;
    }
    // Right of the pin when there is room, else left; 16 from every edge.
    var x = p.x + gap + w > W - 16 ? p.x - gap - w : p.x + gap;
    var y = Math.min(Math.max(16, p.y - h / 2), H - h - 16);
    el.style.left = Math.max(16, x) + 'px';
    el.style.top = y + 'px';
  }
  // card: a .tree-card element (copied) or its markup; lngLat: [lng, lat].
  function open(card, lngLat, href) {
    // The sheet steps away while the card is up (Airbnb), so the card stands
    // alone 16 above the bottom; a page without the hook keeps the peek.
    if (phone.matches) {
      if (window.atSheetAway) { window.atSheetAway(true); }
      else if (window.atSheetPeek) { window.atSheetPeek(); }
    }
    if (el) { el.remove(); }
    el = document.createElement('div');
    el.className = 'map-pop' + (phone.matches ? ' map-pop--phone' : '');
    var copy;
    if (typeof card === 'string') {
      var box = document.createElement('div'); box.innerHTML = card; copy = box.firstElementChild;
    } else {
      copy = card.cloneNode(true);
      copy.removeAttribute('id');
      copy.classList.remove('active');
    }
    if (!copy) { el = null; return; }
    el.appendChild(copy);
    var x = document.createElement('button');
    x.type = 'button';
    x.className = 'map-pop-close';
    x.setAttribute('aria-label', ${JSON.stringify(ui(lang).photoClose)});
    x.innerHTML = ${JSON.stringify(icon("x"))};
    x.addEventListener('click', function(e) { e.stopPropagation(); close(); });
    // With a photograph the pair floats on it; without one, the save already
    // sits on the name's row, so the cross joins it there (2026-10-20).
    // (The catalogue's card does not carry TreeCard's no-photo class.)
    if (!copy.querySelector('.tree-card-photo')) { copy.classList.add('tree-card-nophoto'); }
    var row = copy.classList.contains('tree-card-nophoto') && copy.querySelector('.tree-card-top');
    if (row) { row.appendChild(x); } else { el.appendChild(x); }
    // The card opens the tree page; its heart still saves, as on every card.
    el.addEventListener('click', function(e) {
      if (e.target.closest('.heart-card, .map-pop-close, a')) return;
      if (href) window.location.href = href;
    });
    map.getContainer().appendChild(el);
    at = lngLat; openedAt = Date.now();
    if (window.atPaintSaves) window.atPaintSaves();
    if (window.atPaintSeen) window.atPaintSeen();
    place();
    if (phone.matches) {
      var mr = map.getContainer().getBoundingClientRect();
      var cardTop = el.getBoundingClientRect().top - mr.top;
      var p = map.project(at);
      if (p.y > cardTop - 48 || p.y < 48) {
        map.easeTo({ center: at, duration: 600, offset: [0, Math.round(cardTop / 2 - mr.height / 2)] });
      }
    }
  }
  map.on('move', place);
  map.on('resize', place);
  // A tap on the map lets the tree go. A tap on a circle pin is ALSO a tap on
  // the map, so the click that opened the card does not close it.
  map.on('click', function() { if (el && Date.now() - openedAt > 350) close(); });
  document.addEventListener('keydown', function(e) { if (e.key === 'Escape' && el) close(); });
  return { open: open, close: close, place: place, isOpen: function() { return Boolean(el); }, phone: phone };
}

// A circle-pin map (explore, country, state, My trees): the tapped tree is
// marked the way the city map marks its pin, a larger ring on top, and gets
// the one card from /api/cards.json. A tree the catalogue does not know (your
// own added tree before it has a page) gets the same card from what the pin
// carries: its name and place.
function atCirclePinCard(map, source, treeLayer) {
  var sel = treeLayer + '-sel';
  map.addLayer({id: sel, type: 'circle', source: source, filter: ['==', ['get', 'id'], ''],
    paint: {'circle-color': '#4A6B2A', 'circle-radius': 11,
            'circle-stroke-width': 3, 'circle-stroke-color': '#F6F2E9'}});
  var ctl = atMapCard(map, { gap: 20, onClose: function() { map.setFilter(sel, ['==', ['get', 'id'], '']); } });
  var C = window.atCollection;
  // Warm, so the first tap does not wait for the catalogue.
  map.once('idle', function() { if (C && C.catalogue) C.catalogue(); });
  var asked = 0;
  return function(p, c) {
    var mine = ++asked;
    var id = p.id || '';
    map.setFilter(sel, ['==', ['get', 'id'], id]);
    var known = C && C.catalogue ? C.catalogue() : Promise.resolve({});
    known.then(function(cards) {
      if (mine !== asked) return;
      var k = (id && cards[id]) || { n: p.name || '', c: p.city || '' };
      var rec = {};
      for (var key in k) { rec[key] = k[key]; }
      if (p.url) { rec.u = p.url; }
      var saved = Boolean(window.atHasSaved && window.atHasSaved(id));
      var seen = Boolean(window.atHasVisited && window.atHasVisited(id));
      var html = C && C.card ? C.card(id, rec, saved, seen) : '';
      if (html) { ctl.open(html, c, rec.u || null); }
    });
  };
}
`;
}
