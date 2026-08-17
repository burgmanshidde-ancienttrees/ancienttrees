// The city page's bottom sheet: Google Maps' structure, copied rather than
// invented (Hidde, 2026-08-17: "het is makkelijker als je google maps gewoon
// helemaal afkijkt").
//
// The four movements he described, which are Maps' own:
//   1. the page opens as a map, with the sheet at a peek
//   2. dragging the sheet up shrinks the map and grows the list
//   3. tapping a tree slides THAT tree in, with its actions (save, thumbs,
//      something's wrong) and a way back to the list
//   4. touching the map again drops the sheet back to the peek
//
// Three detents, the same three Maps uses: peek (a header's worth), half, and
// full (a strip of map still showing, so it never reads as a new page).
//
// What this must never do, and it is Hidde's own ruling of 2026-08-06: the
// city page is the indexed asset, so every tree stays in the served HTML.
// Collapsing is CSS and transforms only. The detail view HIDES the other cards
// with a class; it never removes them, never fetches, and never rebuilds the
// list. A crawler sees exactly what it saw before this file existed.
//
// Desktop is untouched: there the split layout is already Maps-shaped (list
// left, map right), so every listener here is behind the same media query the
// stylesheet uses, checked once via matchMedia.
export const SHEET_JS = `
<script>
(function() {
  var mq = window.matchMedia('(max-width: 800px)');
  var sheet = document.getElementById('sheet');
  var stage = document.querySelector('.stage');
  if (!sheet || !stage) return;

  var grab = sheet.querySelector('.sheet-grab');
  var body = sheet.querySelector('.sheet-body');
  var back = sheet.querySelector('.sheet-back');
  var DETENTS = ['peek', 'half', 'full'];
  var at = 'peek';

  function setDetent(name, animate) {
    at = name;
    sheet.classList.toggle('is-animating', animate !== false);
    sheet.dataset.detent = name;
    // The offset is computed rather than declared in CSS, because the peek has
    // to be exactly one header tall and the header's height depends on the
    // city name wrapping. A hardcoded number is wrong on every long name.
    sheet.style.transform = 'translateY(' + offsetFor(name) + 'px)';
    // Only the full sheet scrolls its own body; at peek and half a drag
    // anywhere moves the sheet instead, which is what Maps does and what stops
    // the two gestures fighting each other.
    body.style.overflowY = name === 'full' ? 'auto' : 'hidden';
    if (name !== 'full') body.scrollTop = 0;
  }

  function offsetFor(name) {
    var h = sheet.offsetHeight;
    if (name === 'full') return 0;
    if (name === 'half') return Math.round(h * 0.45);
    return h - peekHeight();
  }

  function peekHeight() {
    var head = sheet.querySelector('.panel-head');
    return (head ? head.offsetHeight : 84) + 8;
  }

  // --- dragging ------------------------------------------------------------
  var dragging = false, startY = 0, startOff = 0, lastY = 0, lastT = 0, vel = 0;

  function onDown(e) {
    if (!mq.matches) return;
    // A drag that starts on the scrolled body should scroll it, not move the
    // sheet, unless the body is already at its top and the pull is downward.
    if (at === 'full' && e.target.closest('.sheet-body') && body.scrollTop > 0) return;
    dragging = true;
    startY = lastY = e.touches ? e.touches[0].clientY : e.clientY;
    startOff = offsetFor(at);
    lastT = Date.now();
    vel = 0;
    sheet.classList.remove('is-animating');
  }

  function onMove(e) {
    if (!dragging) return;
    var y = e.touches ? e.touches[0].clientY : e.clientY;
    var dy = y - startY;
    var off = Math.max(0, Math.min(offsetFor('peek'), startOff + dy));
    // An upward pull from a body scrolled to the top should expand the sheet
    // rather than rubber-band, so the list feels like one continuous surface.
    if (at === 'full' && dy < 0) { dragging = false; return; }
    sheet.style.transform = 'translateY(' + off + 'px)';
    var now = Date.now();
    if (now > lastT) { vel = (y - lastY) / (now - lastT); lastT = now; lastY = y; }
    if (e.cancelable) e.preventDefault();
  }

  function onUp() {
    if (!dragging) return;
    dragging = false;
    var cur = parseFloat((sheet.style.transform.match(/-?[\\d.]+/) || [offsetFor(at)])[0]);
    // A flick beats proximity, the way every sheet on a phone behaves.
    if (Math.abs(vel) > 0.6) {
      var i = DETENTS.indexOf(at);
      setDetent(DETENTS[Math.max(0, Math.min(2, i + (vel > 0 ? -1 : 1)))]);
      return;
    }
    var best = 'peek', bestD = Infinity;
    DETENTS.forEach(function(d) {
      var dd = Math.abs(offsetFor(d) - cur);
      if (dd < bestD) { bestD = dd; best = d; }
    });
    setDetent(best);
  }

  grab.addEventListener('mousedown', onDown);
  grab.addEventListener('touchstart', onDown, { passive: true });
  body.addEventListener('touchstart', onDown, { passive: true });
  document.addEventListener('mousemove', onMove);
  document.addEventListener('touchmove', onMove, { passive: false });
  document.addEventListener('mouseup', onUp);
  document.addEventListener('touchend', onUp);

  // Tapping the peek header opens it, because a bar that only responds to a
  // drag hides its own affordance from anyone who has not tried.
  grab.addEventListener('click', function() {
    if (!mq.matches) return;
    if (at === 'peek') setDetent('half');
  });

  // --- movement 4: touching the map gives the map back --------------------
  stage.addEventListener('pointerdown', function() {
    if (!mq.matches) return;
    if (at !== 'peek') setDetent('peek');
  });

  // --- movement 3: one tree, with its actions ------------------------------
  function openTree(id) {
    var found = false;
    document.querySelectorAll('.tree-card').forEach(function(c) {
      var mine = c.dataset.treeId === id;
      c.classList.toggle('is-open', mine);
      if (mine) found = true;
    });
    if (!found) return;
    sheet.classList.add('is-detail');
    sheet.dataset.tree = id;
    if (at === 'peek') setDetent('half');
    body.scrollTop = 0;
  }
  function closeTree() {
    sheet.classList.remove('is-detail');
    sheet.dataset.tree = '';
    document.querySelectorAll('.tree-card.is-open').forEach(function(c) {
      c.classList.remove('is-open');
    });
  }

  document.addEventListener('click', function(e) {
    if (!mq.matches) return;
    var open = e.target.closest('[data-open-tree]');
    if (open) {
      var card = open.closest('.tree-card');
      if (card && card.dataset.treeId) { openTree(card.dataset.treeId); }
      return;
    }
    if (e.target.closest('.sheet-back')) { closeTree(); }
  });

  // The map script already scrolls a card into view when its pin is tapped
  // (city-map-script.ts). On a phone that card is inside this sheet, so the
  // same tap should also promote it, which is Maps' behaviour exactly.
  window.atSheetFocus = function(id) {
    if (!mq.matches) return;
    openTree(id);
  };

  // Reset cleanly when the layout crosses into the desktop split, where the
  // sheet does not exist as a concept.
  mq.addEventListener('change', function() {
    if (!mq.matches) { sheet.style.transform = ''; closeTree(); }
    else setDetent('peek', false);
  });

  if (mq.matches) setDetent('peek', false);
})();
</script>
`;
