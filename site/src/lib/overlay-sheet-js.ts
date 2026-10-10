// THE ONE SHEET'S BEHAVIOUR, for every <dialog class="at-sheet"> on a page
// (components/Sheet.astro, 2026-10-10). Delegated from the document, so a sheet
// rendered by any component works without wiring of its own: the cross closes
// it, a tap on the backdrop closes it, Escape closes it (the browser's own),
// and on a phone a downward drag from the top closes it. The drag is the
// sign-in sheet's (lib/signin-js.ts), the same thresholds, generalised.
export const OVERLAY_SHEET_JS = `
<script>
(function() {
  document.addEventListener('click', function(e) {
    var x = e.target.closest && e.target.closest('.at-sheet-x');
    if (x) { var d = x.closest('dialog'); if (d && d.open) d.close(); return; }
    var t = e.target;
    if (t && t.tagName === 'DIALOG' && t.classList.contains('at-sheet') && t.open) t.close();
  });
  var mq = window.matchMedia('(max-width: 600px)');
  var dlg = null, y0 = 0, dy = 0, t0 = 0;
  document.addEventListener('touchstart', function(e) {
    var d = e.target.closest && e.target.closest('dialog.at-sheet');
    if (!d || !d.open || !mq.matches || e.touches.length !== 1 || d.scrollTop > 0) return;
    if (e.target.closest('button, a, input, textarea, select')) return;
    dlg = d; y0 = e.touches[0].clientY; dy = 0; t0 = Date.now();
    d.classList.add('is-dragging');
  }, { passive: true });
  document.addEventListener('touchmove', function(e) {
    if (!dlg) return;
    dy = e.touches[0].clientY - y0;
    if (dy <= 0) { dy = 0; dlg.style.transform = ''; return; }
    e.preventDefault();
    dlg.style.transform = 'translateY(' + dy + 'px)';
  }, { passive: false });
  function release() {
    if (!dlg) return;
    var d = dlg; dlg = null;
    d.classList.remove('is-dragging');
    var far = dy > d.offsetHeight * 0.25;
    var flick = dy > 40 && (Date.now() - t0) < 300;
    if (far || flick) {
      d.style.transform = 'translateY(100%)';
      setTimeout(function() { d.close(); d.style.transform = ''; }, 220);
    } else {
      d.style.transform = '';
    }
  }
  document.addEventListener('touchend', release);
  document.addEventListener('touchcancel', release);
})();
</script>
`;
