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
    // Measured, because until 2026-09-18 this route emitted nothing and the
    // email route below was the funnel's only event. It had fired ZERO times
    // ever while twelve accounts existed, so every account on the site had
    // arrived by a path nothing recorded and nobody could say which.
    try { at.track('signin-oauth', provider); } catch (e) {}
    location.href = SB + '/auth/v1/authorize?provider=' + provider
      + '&redirect_to=' + encodeURIComponent(back);
  };
  document.addEventListener('click', function(e) {
    var g = e.target.closest('#signin-google, #acct-google');
    if (g) { e.preventDefault(); window.atOAuth('google'); }
    // Apple, 2026-09-12, through the identical redirect. The app signs in with
    // Apple natively and a browser has no native credential to present, so the
    // web takes the ordinary OAuth route and the only difference from Google is
    // the word. It sits on the SECOND screen (SignInPanel.astro says why), so
    // this listener fires only after More options. The buttons render only where
    // APPLE_SIGNIN is on, so it is dormant rather than wrong while that is off.
    var a = e.target.closest('#signin-apple, #acct-apple');
    if (a) { e.preventDefault(); window.atOAuth('apple'); }
  });

  // ONE WIRING, RUN PER SURFACE. The dialog and the account page render the
  // same panel (SignInPanel.astro) with different id prefixes, because both
  // are on /account at once and two elements cannot share an id. Everything
  // below therefore takes the prefix rather than naming the dialog's ids, so a
  // behaviour cannot exist on one surface and not the other.
  function wire(p) {
    var el = function(n) { return document.getElementById(p + '-' + n); };
    if (!el('more')) return;

    // CONTINUE IN THE APP takes the loud slot on an iPhone and nowhere else,
    // demoting Google, which holds it everywhere else.
    // The tree id rides along so the app lands on the tree the reader was
    // standing on; it comes off the save heart, the one element already
    // carrying it on every tree page.
    var ua = navigator.userAgent || '';
    var isIOS = /iPhone|iPad|iPod/.test(ua)
      || (ua.indexOf('Macintosh') > -1 && navigator.maxTouchPoints > 1);
    if (isIOS && el('openapp')) {
      var open = el('openapp');
      var loud = document.querySelector('#' + p + '-google.oauth-loud');
      if (loud) { loud.classList.remove('oauth-loud'); loud.classList.add('oauth-quiet'); }
      var t = document.querySelector('[data-tree]');
      var slug = location.pathname.split('/').filter(Boolean)[0] || '';
      var q = t && t.dataset.tree ? '?tree=' + encodeURIComponent(t.dataset.tree)
            : (slug && slug !== 'account' ? '?city=' + encodeURIComponent(slug) : '');
      open.setAttribute('href', '/open' + q);
      open.hidden = false;
      // The rule separates continuing from signing in, so it belongs directly
      // under the app button rather than where the sign-in layout left it.
      var rule = el('rule');
      if (rule) {
        rule.hidden = false;
        if (open.nextSibling !== rule) open.parentNode.insertBefore(rule, open.nextSibling);
      }
      // The headline becomes the offer the button makes, and the subtitle goes
      // with it: "Sign in to save X" under "works better in the app" answers a
      // question nobody asked.
      var title = el('title');
      if (title && title.getAttribute('data-app')) {
        title.setAttribute('data-generic', title.getAttribute('data-app'));
        title.textContent = title.getAttribute('data-app');
      }
      var sub = el('sub');
      if (sub) sub.hidden = true;
      var host = open.closest('.signin-dialog') || open.parentNode;
      if (host && host.classList) host.classList.add('signin-dialog--app');
      // "Get the app" at the foot is the same offer as the button at the top.
      var al = open.parentNode.querySelector('.signin-applink');
      if (al) al.hidden = true;
    }

    // THE SECOND SCREEN: every remaining route, and "More options" gone.
    el('more').addEventListener('click', function() {
      ['apple', 'emailbtn'].forEach(function(n) { if (el(n)) el(n).hidden = false; });
      el('more').hidden = true;
    });
    // The address is asked for only once somebody has chosen to type one.
    if (el('emailbtn')) el('emailbtn').addEventListener('click', function() {
      if (el('rest')) el('rest').hidden = false;
      el('emailbtn').hidden = true;
      if (el('email')) el('email').focus();
    });
  }
  wire('signin');
  wire('acct');

  var dlg = document.getElementById('signin-dialog');
  if (!dlg) return;
  window.atOpenSignIn = function(treeName, reason) {
    // Name the tree that was just saved. A 'feedback' reason (the gated
    // vote/report/contribute flows) swaps both lines: nothing was saved, so the
    // save wording would be a lie. On a phone the headline is already the app
    // offer and stays that way.
    var sub = document.getElementById('signin-sub');
    var title = document.getElementById('signin-title');
    var appMode = !!document.querySelector('#signin-openapp:not([hidden])');
    if (title && !appMode) {
      title.textContent = title.getAttribute(
        reason === 'feedback' ? 'data-feedback' : 'data-generic') || title.textContent;
    }
    if (sub && !appMode) {
      if (reason === 'feedback') {
        sub.textContent = sub.getAttribute('data-feedback') || sub.getAttribute('data-generic');
      } else {
        var tpl = treeName ? sub.getAttribute('data-named') : null;
        sub.textContent = tpl ? tpl.replace('%s', treeName) : sub.getAttribute('data-generic');
      }
    }
    // Back to the FIRST screen, because a dialog is reopened on the same page
    // and would otherwise remember a state the visitor did not choose.
    var rest = document.getElementById('signin-rest');
    var moreBtn = document.getElementById('signin-more');
    if (rest) rest.hidden = true;
    if (moreBtn) moreBtn.hidden = false;
    var eb = document.getElementById('signin-emailbtn');
    if (eb) eb.hidden = true;
    var ap = document.getElementById('signin-apple');
    if (ap) ap.hidden = true;
    if (dlg.showModal) { dlg.showModal(); } else { location.href = '/account'; }
    // The TOP of the funnel, and the number that decides what the low account
    // count means (2026-09-18). Without it, "few people sign in" cannot be
    // told apart from "few people are ever asked to", which are opposite
    // problems with opposite fixes. The detail says what asked: a save, a
    // gated vote or report, or the plain sign-in link in the bar.
    try { at.track('signin-open', reason || (treeName ? 'save' : 'direct')); } catch (e) {}
  };
  document.addEventListener('click', function(e) {
    var t = e.target.closest('[data-signin]');
    if (t) { e.preventDefault(); window.atOpenSignIn(); }
  });

  // SIGNING IN NEVER TAKES YOU OFF YOUR PAGE. Hidde, 2026-09-18: "hij moet
  // zich vertonen over de pagina waar je bent zodat je terug kan naar waar je
  // was." The nav's account entries pointed at /account, so signing in from a
  // tree page meant leaving it, and the only way back was the back button.
  // The heart has opened this sheet in place since the day it was built; the
  // nav simply never did, because for most of the site there was no sheet to
  // open (it is Base's now, which is the other half of this change).
  //
  // Signed IN they still go to /account, because then it is a real page with
  // your trees on it rather than a sign-in form. On /account itself there is
  // nothing to open a sheet over, so those links are left alone.
  document.addEventListener('click', function(e) {
    var a = e.target.closest ? e.target.closest('a[href^="/account"]') : null;
    if (!a) return;
    if (document.documentElement.dataset.signedIn === '1') return;
    if (location.pathname === '/account' || location.pathname === '/account/') return;
    e.preventDefault();
    var d = a.closest('details');
    if (d) d.open = false;
    window.atOpenSignIn();
  });
  document.getElementById('signin-close').addEventListener('click', function() { dlg.close(); });
  dlg.addEventListener('click', function(e) { if (e.target === dlg) dlg.close(); });

  // SWIPE IT AWAY. The handle has been drawing a promise since the sheet took
  // this shape and nothing honoured it (Hidde, 2026-09-18). Material 3 settles
  // a modal bottom sheet to a detent or to hidden, so a downward drag is a
  // dismissal; ours has one stop, so it is open or gone. Apple's sheets are
  // the same gesture, which is why no invention was needed here.
  //
  // Phone only. Above 600px this is a centred dialog and a drag would mean
  // nothing; the close button, the backdrop and Escape work at every width.
  (function() {
    var mq = window.matchMedia('(max-width: 600px)');
    var y0 = 0, dy = 0, t0 = 0, active = false;
    function rest() { dlg.classList.remove('is-dragging'); dlg.style.transform = ''; }
    dlg.addEventListener('touchstart', function(e) {
      if (!mq.matches || e.touches.length !== 1) return;
      // A finger landing on a scrolled sheet scrolls it. Only a sheet already
      // at its top can be dragged away, which is the map sheet's rule too and
      // is what stops the two gestures fighting.
      if (dlg.scrollTop > 0) return;
      active = true; y0 = e.touches[0].clientY; dy = 0; t0 = Date.now();
      dlg.classList.add('is-dragging');
    }, { passive: true });
    dlg.addEventListener('touchmove', function(e) {
      if (!active) return;
      dy = e.touches[0].clientY - y0;
      // Down only: there is nothing above this sheet to drag it into.
      if (dy <= 0) { dy = 0; dlg.style.transform = ''; return; }
      e.preventDefault();
      dlg.style.transform = 'translateY(' + dy + 'px)';
    }, { passive: false });
    function release() {
      if (!active) return;
      active = false;
      dlg.classList.remove('is-dragging');
      // Far enough, or a flick. The flick matters: a short fast swipe is how
      // people actually dismiss a sheet, and distance alone refuses it.
      var far = dy > dlg.offsetHeight * 0.25;
      var flick = dy > 40 && (Date.now() - t0) < 300;
      if (far || flick) {
        dlg.style.transform = 'translateY(100%)';
        setTimeout(function() { dlg.close(); }, 220);
      } else {
        dlg.style.transform = '';
      }
    }
    dlg.addEventListener('touchend', release);
    dlg.addEventListener('touchcancel', release);
    // A reopened sheet must not inherit where the last drag left it.
    dlg.addEventListener('close', rest);
  })();
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
