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
  // Keep the session alive. Supabase hands out an access token that lasts an
  // hour and a refresh token that lasts far longer, and until 2026-08-18
  // nothing ever used the second one. So an hour after signing in, session()
  // started returning null everywhere: saves stopped syncing to the account,
  // the union on /account stopped running, and nothing said so. Hidde hit it
  // exactly that way ("im logged in saving trees but nothing is showing up"),
  // and on a second device there was nothing to show.
  //
  // Refresh on load when the token is spent or within five minutes of it, then
  // tell the save code to run its sync, because that code has already decided
  // there was no session by the time this resolves.
  (function refreshIfStale() {
    var s = null;
    try { s = JSON.parse(localStorage.getItem('ancienttrees_session')); } catch (e) { return; }
    if (!s || !s.refresh_token) return;
    if (s.expires_at > Date.now() / 1000 + 300) return;
    fetch(SB + '/auth/v1/token?grant_type=refresh_token', {
      method: 'POST',
      headers: { 'apikey': SBK, 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: s.refresh_token })
    }).then(function(r) { return r.ok ? r.json() : null; })
      .then(function(j) {
        if (!j || !j.access_token) {
          // The refresh token is spent or revoked. Clear it rather than leave
          // a dead session that makes the site look signed in.
          try { localStorage.removeItem('ancienttrees_session'); } catch (e) {}
          return;
        }
        try {
          localStorage.setItem('ancienttrees_session', JSON.stringify({
            access_token: j.access_token,
            refresh_token: j.refresh_token || s.refresh_token,
            expires_at: Math.floor(Date.now() / 1000) + (j.expires_in || 3600)
          }));
        } catch (e) {}
        try { sessionStorage.removeItem('at_saves_synced'); } catch (e) {}
        if (window.atSyncSaves) window.atSyncSaves();
      })
      .catch(function() {});
  })();

  // Google, added 2026-08-20. One redirect: Supabase talks to Google, Google
  // sends the person back to Supabase, and Supabase returns them here with the
  // tokens in the fragment, which the code at the top of this file already
  // catches on whatever page they were on. Nothing else to wire.
  window.atOAuth = function(provider) {
    var back = location.origin + location.pathname;
    location.href = SB + '/auth/v1/authorize?provider=' + provider
      + '&redirect_to=' + encodeURIComponent(back);
  };
  document.addEventListener('click', function(e) {
    var g = e.target.closest('#signin-google, #acct-google');
    if (g) { e.preventDefault(); window.atOAuth('google'); }
  });

  var dlg = document.getElementById('signin-dialog');
  if (!dlg) return;
  window.atOpenSignIn = function(treeName, reason) {
    // Name the tree that was just saved. The generic line stays for every
    // other entry point, and a missing name is not an error, it is the
    // ordinary case on the account page and in the nav. A reason of
    // 'feedback' (the gated vote/report/contribute flows, 2026-08-21) swaps
    // both lines: nothing was saved, so the save wording would be a lie.
    var sub = document.getElementById('signin-sub');
    var title = document.getElementById('signin-title');
    if (title) {
      title.textContent = title.getAttribute(
        reason === 'feedback' ? 'data-feedback' : 'data-generic') || title.textContent;
    }
    if (sub) {
      if (reason === 'feedback') {
        sub.textContent = sub.getAttribute('data-feedback') || sub.getAttribute('data-generic');
      } else {
        var tpl = treeName ? sub.getAttribute('data-named') : null;
        sub.textContent = tpl ? tpl.replace('%s', treeName) : sub.getAttribute('data-generic');
      }
    }
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
