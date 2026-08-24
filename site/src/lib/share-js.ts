// The share button, on every page worth sending to somebody.
//
// Hidde, 2026-08-24: "ik denk dat je gelijk een deel knop wil voor mooie bomen
// en mooie steden - mss zelfs nog andere paginas en dit consistent doorvoeren -
// wederom kijk naar de concurent." He then sent three frames, and AllTrails and
// komoot turn out to do the same thing: the hero photo carries back on the left
// and share on the right, and the share itself opens the system sheet.
//
// On the web that system sheet is navigator.share, which every phone browser
// has and no desktop browser reliably does, so the desktop path copies the link
// and says so. Nothing here is invented; this is the whole convention.
//
// What we do NOT copy, and it is worth writing down: AllTrails' sheet is not
// the system one, it is a carousel of GENERATED images with the route's name
// and figures drawn on them, because a bare link posted to a story shows
// nothing. On the web we already have that in a different form, and it is the
// og:image the page carries: paste our link into WhatsApp or Slack and the
// tree's photograph is what unfolds. Generating a share IMAGE is an app job and
// a separate piece of work.
export const SHARE_JS = `
<script>
(function() {
  document.querySelectorAll('[data-share]').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var url = btn.getAttribute('data-share-url') || location.href;
      var title = btn.getAttribute('data-share-title') || document.title;
      if (navigator.share) {
        navigator.share({ title: title, url: url }).catch(function() {});
        return;
      }
      // No system sheet here, so the useful thing is the link itself. The
      // button says what happened rather than doing it silently.
      var done = function() {
        var was = btn.getAttribute('aria-label');
        btn.classList.add('is-copied');
        btn.setAttribute('aria-label', 'Link copied');
        setTimeout(function() {
          btn.classList.remove('is-copied');
          btn.setAttribute('aria-label', was);
        }, 1800);
      };
      // The clipboard API needs a secure context AND a real user gesture, and
      // it rejects silently when it does not have one. A share button that
      // does nothing and says nothing is the silent no-op this codebase keeps
      // a check for, so a rejection falls through to the old way rather than
      // into an empty handler.
      var legacy = function() {
        var f = document.createElement('textarea');
        f.value = url;
        f.setAttribute('readonly', '');
        f.style.position = 'fixed';
        f.style.opacity = '0';
        document.body.appendChild(f);
        f.select();
        var ok = false;
        try { ok = document.execCommand('copy'); } catch (e) {}
        document.body.removeChild(f);
        return ok;
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(done, function() {
          if (legacy()) done();
        });
      } else if (legacy()) {
        done();
      }
    });
  });
})();
</script>`;
