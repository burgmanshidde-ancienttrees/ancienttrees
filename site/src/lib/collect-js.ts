// Ported verbatim from COLLECT_JS, build_site.py:2795-2813. The tree page's
// "Collect this tree" button: opens an explainer dialog on tap (Hidde,
// 2026-08-01), funnels to /app. Not the passport/check-in system (that is
// city-page only, .seen-btn, and reads/writes the ancienttrees_seen key
// directly; see the city page build).
export const COLLECT_JS = `
<script>
(function() {
  var btn = document.getElementById('collect-btn');
  var dlg = document.getElementById('collect-dialog');
  if (!btn) return;
  if (dlg && dlg.showModal) {
    btn.addEventListener('click', function() {
      at.track('collect-open');
      dlg.showModal();
    });
    document.getElementById('collect-close').addEventListener('click', function() { dlg.close(); });
    dlg.addEventListener('click', function(e) { if (e.target === dlg) { dlg.close(); } });
  } else {
    btn.addEventListener('click', function() { window.location.href = '../app'; });
  }
})();
</script>
`;
