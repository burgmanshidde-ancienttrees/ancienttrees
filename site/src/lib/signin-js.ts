// The one sign-in surface's script. Three jobs, shared by every page that
// includes SignInModal.astro:
//
// 1. Parse a magic-link token out of the URL hash ON ANY PAGE, store the
//    session, and clean the URL. The link's redirect_to is the page the
//    visitor was on, so signing in never loses their place; until now only
//    /account could catch the token.
// 2. Open the dialog from anything carrying data-signin, or from script via
//    atOpenSignIn() (the save heart's first-save funnel uses this).
// 3. The inline email flow, same OTP endpoint the account page uses.
import { SUPABASE_URL, SUPABASE_KEY } from "./site-config";

export const SIGNIN_JS = `
<script>
(function() {
  var SB = '${SUPABASE_URL}';
  var SBK = '${SUPABASE_KEY}';
  // 1. catch a returning magic link on any page
  var h = {};
  location.hash.slice(1).split('&').forEach(function(kv) {
    var p = kv.split('=');
    if (p[0]) h[decodeURIComponent(p[0])] = decodeURIComponent(p[1] || '');
  });
  if (h.access_token) {
    try {
      localStorage.setItem('ancienttrees_session', JSON.stringify({
        access_token: h.access_token,
        refresh_token: h.refresh_token || '',
        expires_at: Math.floor(Date.now() / 1000) + parseInt(h.expires_in || '3600', 10)
      }));
    } catch (e) {}
    history.replaceState(null, '', location.pathname);
  }
  var dlg = document.getElementById('signin-dialog');
  if (!dlg) return;
  window.atOpenSignIn = function() {
    if (dlg.showModal) { dlg.showModal(); } else { location.href = '/account'; }
  };
  document.addEventListener('click', function(e) {
    var t = e.target.closest('[data-signin]');
    if (t) { e.preventDefault(); window.atOpenSignIn(); }
  });
  document.getElementById('signin-close').addEventListener('click', function() { dlg.close(); });
  dlg.addEventListener('click', function(e) { if (e.target === dlg) dlg.close(); });
  document.getElementById('signin-form').addEventListener('submit', function(ev) {
    ev.preventDefault();
    var email = document.getElementById('signin-email').value.trim();
    if (!email) return;
    fetch(SB + '/auth/v1/otp?redirect_to=' + encodeURIComponent(location.origin + location.pathname), {
      method: 'POST',
      headers: { 'apikey': SBK, 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, create_user: true })
    }).then(function(r) {
      if (!r.ok) throw new Error('otp');
      document.getElementById('signin-sent-to').textContent = email;
      document.getElementById('signin-ask').hidden = true;
      document.getElementById('signin-sent').hidden = false;
      try { at.track('signin-link-sent'); } catch (e) {}
    }).catch(function() {
      var f = document.getElementById('signin-email');
      f.setCustomValidity('That did not work; try again in a minute.');
      document.getElementById('signin-form').reportValidity();
      setTimeout(function() { f.setCustomValidity(''); }, 3000);
    });
  });
})();
</script>
`;
