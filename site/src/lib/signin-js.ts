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

// THE TOKEN IS CAUGHT IN THE HEAD, BEFORE ANY PAGE SCRIPT ASKS WHO YOU ARE.
//
// Hidde, 2026-09-18, on the whole flow: it is clunky which pages you land on.
// One cause was invisible and underneath most of it. A magic link and a Google
// return both come back as an ORDINARY PAGE LOAD with the tokens in the
// fragment, and this token was parsed at the FOOT of the body. Every script
// that asks C.session() runs earlier than that: the hearts (tree-actions-js),
// the ticks (visited-sync-js), the worth-it vote, the settings page. All of
// them asked before the answer existed, got null, and painted the page as
// signed out. So you came back from Google onto the tree you were reading and
// your own saves were invisible, the tick was blank and /account/settings said
// you were not signed in, until you reloaded by hand.
//
// It was hidden by the two pages that happened to be fine. /account parses the
// fragment itself, and the nav's "Account" swap is a type="module" script,
// which the browser defers until after everything else, so those two were
// right while the rest of the site was wrong.
//
// Parsing it here fixes the class rather than the cases: whatever a page asks,
// it now gets the right answer on the first ask. It is deliberately the
// smallest thing that can run this early, with no dependency on anything.
export const SIGNIN_CATCH_JS = `
<script>
(function() {
  var h = {};
  location.hash.slice(1).split('&').forEach(function(kv) {
    var p = kv.split('=');
    if (p[0]) h[decodeURIComponent(p[0])] = decodeURIComponent(p[1] || '');
  });
  if (!h.access_token) return;
  try {
    localStorage.setItem('ancienttrees_session', JSON.stringify({
      access_token: h.access_token,
      refresh_token: h.refresh_token || '',
      expires_at: Math.floor(Date.now() / 1000) + parseInt(h.expires_in || '3600', 10)
    }));
  } catch (e) {}
  history.replaceState(null, '', location.pathname + location.search);
  document.documentElement.dataset.signedIn = '1';
  // What they were doing when they were asked to sign in, read here and handed
  // to the foot of the page, which is where the code that can finish it lives.
  var want = null;
  try {
    want = JSON.parse(localStorage.getItem('ancienttrees_pending') || 'null');
    localStorage.removeItem('ancienttrees_pending');
  } catch (e) {}
  // Half an hour, because a magic link is read in another app and sometimes on
  // another device, and replaying a press from yesterday is a surprise.
  if (!want || !want.at || Date.now() - want.at > 1800000) want = {};
  window.atJustSignedIn = want;
})();
</script>
`;

export const SIGNIN_JS = `
<script>
(function() {
  var SB = '${SUPABASE_URL}';
  var SBK = '${SUPABASE_KEY}';
  // 1. the returning magic link is caught in the HEAD now, by SIGNIN_CATCH_JS
  //    at the top of this file, for the reason written there. What is left
  //    here is the half that needs the rest of the page: finishing the act
  //    that asked for the sign-in.
  if (window.atJustSignedIn) landed();

  // WHAT HAPPENS ON THE PAGE YOU LAND ON (2026-09-18). Hidde: signing in and
  // out is clunky about which pages you land on. Two halves were missing. The
  // first is fixed in the head (SIGNIN_CATCH_JS): the page now knows you are
  // signed in before any of its own scripts ask. This is the second.
  //
  // THE ACT THAT ASKED FOR THE SIGN-IN WAS DROPPED. You press Save, the sheet
  // says "Sign in to save the Totteridge Yew", you sign in, and the tree is not
  // saved: you are returned to the page you were on and have to press it again.
  // The convention is not ours to invent and we already record it
  // (CONVENTIONS.md, landing after you have added something): you land on the
  // thing, and its state is written ON it and stays there while it is true. So
  // the save is finished and the heart says Saved, which IS the
  // acknowledgement. Our own app has always worked this way, dismissing its
  // sheet back onto the tree; only the website lost the thread.
  //
  // A vote is deliberately NOT replayed. A save and a tick are one press and
  // the account was the only thing in the way; an opinion is not something to
  // post on somebody's behalf because they signed in afterwards.
  function landed() {
    var want = window.atJustSignedIn;
    // The END of the funnel, which had no event: signin-open and
    // signin-link-sent said who was asked and who typed an address, and nothing
    // said who arrived back signed in.
    try { at.track('signin-done', want.kind || 'direct'); } catch (e) {}
    if (!want.tree) return;
    if (!document.querySelector('[data-tree="' + want.tree + '"]')) return;
    // The account's answer FIRST. Both lists were fetched by their own scripts
    // a moment ago and neither hands back a handle to wait on, so this asks
    // again: two requests, only on the sign-in landing, only when there is an
    // act to finish. Replaying ahead of them would be painted straight back off
    // by the answer landing after it, and atPushVisited does nothing at all
    // until the visited list has arrived.
    var jobs = [];
    if (window.atSyncSaves) jobs.push(Promise.resolve(window.atSyncSaves()));
    if (window.atSyncVisited) jobs.push(Promise.resolve(window.atSyncVisited()));
    Promise.all(jobs).then(function() {
      if (want.kind === 'save' && window.atSaveTree) {
        window.atSaveTree(want.tree, true);
      } else if (want.kind === 'visit' && window.atPushVisited) {
        if (!(window.atHasVisited && window.atHasVisited(want.tree))) {
          window.atPushVisited(want.tree, true);
          try { at.track('visit'); } catch (e) {}
        }
        if (window.atPaintSeen) window.atPaintSeen();
        if (window.atPaintPassport) window.atPaintPassport();
      }
    }).catch(function() {});
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
  window.atOpenSignIn = function(treeName, reason, want) {
    // What the person was trying to DO, kept for the page they come back to.
    // Written here rather than at each gate so a new gate cannot forget it, and
    // cleared below the moment they dismiss the sheet instead of signing in.
    try {
      if (want && want.tree) {
        localStorage.setItem('ancienttrees_pending',
          JSON.stringify({ kind: want.kind, tree: want.tree, at: Date.now() }));
      } else {
        localStorage.removeItem('ancienttrees_pending');
      }
    } catch (e) {}
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
  // CLOSING IT IS A NO. Every dismissal ends here (the corner, the backdrop,
  // Escape, and the swipe below all call close()), so the act it was going to
  // finish is dropped in one place rather than in four.
  dlg.addEventListener('close', function() {
    // Unless a link is already in their inbox. That sheet is CLOSED on purpose
    // by somebody going off to read their mail, often on the other device, and
    // the save they asked for should still be waiting when the link brings them
    // back.
    var sent = document.getElementById('signin-sent');
    if (sent && !sent.hidden) return;
    try { localStorage.removeItem('ancienttrees_pending'); } catch (e) {}
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
