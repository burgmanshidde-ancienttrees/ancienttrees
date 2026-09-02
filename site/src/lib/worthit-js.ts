// The "Worth the visit?" control's one delegated script (design: Hidde,
// 2026-08-14; split into vote and report 2026-08-16, see WorthIt.astro for the
// reasoning and the convention it follows). One listener serves every control
// on the page, because a city page carries up to 46 of them.
//
// Two independent actions, which is the whole point of the rebuild:
//   the thumbs are an opinion, a toggle, complete on their own;
//   "Something's wrong" opens fact chips and reports a problem.
// They are independent, so voting never blocks a correction and a correction
// never spends the vote. Someone may love a tree and still tell us the pin is
// wrong; the old nested version made that impossible.
//
// WHAT YOU ALREADY SAID IS READ BACK FROM YOUR ACCOUNT, not remembered by the
// browser (2026-09-02, Hidde: "alles wat wordt opgeslagen, moet op je account
// zijn"). It used to sit in three localStorage keys per tree, which meant the
// same person could vote again from a second browser and a vote made on the
// phone was invisible here. The rows were always on the server; what was
// missing was permission to read them back, and supabase/own-data.sql granted
// exactly that on 2026-08-27 for the app's sake. This is the website catching
// up with a policy that already exists.
//
// Revised 2026-08-21 on Hidde's ask, knowingly amending his 2026-08-16 split:
// thumbs are now toggle buttons (press selects, press again undoes, the other
// thumb switches; undo writes a compensating "vote undone" row rather than
// deleting anything), and a down-vote unfolds the why-chips as an OPTIONAL
// follow-up, the app-store convention. The split's core survives: the vote is
// complete without a reason, and the standalone report button stays for the
// up-voter who spotted a wrong pin.
//
// And gated behind sign-in, same day, after the convention check he asked
// for: Google Maps, AllTrails, Waze and Apple Maps all require an account to
// contribute, because the account IS the reply channel and the authenticity
// check; only civic tools like FixMyStreet take anonymous reports, and they
// make an email mandatory instead. His ruling: "people can see the options
// but have to login to actually give feedback." So the controls render for
// everyone, and the first tap while signed out opens the one sign-in dialog
// (atOpenSignIn) instead of counting. Unlike a save, nothing happens locally
// first: a vote that only existed in one browser would be a lie in the tally.
// Signed-in posts carry the user's token, so the row arrives with auth.uid()
// and the reply loop needs no typed email.
//
// Where a report goes: the same Supabase submissions table the /contribute form
// posts to (live since 2026-07-31), kind 'feedback', tree id and city prefilled
// from the control's own data attributes. Step 0b reads that table, so dead and
// wrong-location reports land in the existing correction flow with its same-day
// rule. No new backend; the account that gates it is the reply channel.
//
// Votes are stored and shown to nobody until volume makes a count honest;
// nothing here renders numbers.
import { SUPABASE_URL, SUPABASE_KEY } from "./site-config";

export const WORTHIT_JS = `
<script>
(function() {
  function session() {
    try {
      var s = JSON.parse(localStorage.getItem('ancienttrees_session'));
      return (s && s.expires_at > Date.now() / 1000) ? s : null;
    } catch (e) { return null; }
  }
  function send(box, verdict, reason) {
    var s = session();
    if (!s) return;
    var tree = box.dataset.tree, city = box.dataset.city, name = box.dataset.name;
    try {
      fetch('${SUPABASE_URL}/rest/v1/submissions', {
        method: 'POST',
        headers: {'apikey': '${SUPABASE_KEY}', 'Authorization': 'Bearer ' + s.access_token,
                  'Content-Type': 'application/json', 'Prefer': 'return=minimal'},
        body: JSON.stringify({
          kind: 'feedback',
          city: city,
          tree: tree + ' (' + name + ')',
          why: verdict + (reason ? ': ' + reason : ''),
          page: location.pathname
        })
      });
    } catch (e) {}
    try { at.track('worthit-' + verdict); } catch (e) {}
  }
  function show(box, sel, on) {
    var el = box.querySelector(sel);
    if (el) el.hidden = !on;
  }
  // Thumbs are toggle buttons (Hidde, 2026-08-21: "buttons to press and than
  // it selects and than unpress"): press selects and counts, press again
  // undoes, the other thumb switches. They stay visible after a vote; the
  // selected state IS the confirmation.
  // What this account has already said about this tree, rebuilt from its own
  // submission rows. Held in memory for this page and never written down.
  //   why = "worth it" | "not worth it" | "vote undone: ..." | "report: ..."
  //         | "report detail: ..."
  var mine = {};   // tree id -> { vote, reported, detailed }
  function state(tree) {
    if (!mine[tree]) mine[tree] = { vote: null, reported: false, detailed: false };
    return mine[tree];
  }
  function load(box) {
    var s = session();
    if (!s) return Promise.resolve();
    var tree = box.dataset.tree;
    return fetch('${SUPABASE_URL}/rest/v1/submissions?select=why&order=created_at.desc'
                 + '&tree=like.' + encodeURIComponent(tree + '%'),
      { headers: { 'apikey': '${SUPABASE_KEY}', 'Authorization': 'Bearer ' + s.access_token } })
      .then(function(r) { return r.ok ? r.json() : []; })
      .then(function(rows) {
        var st = state(tree);
        (rows || []).forEach(function(row) {
          var why = String(row.why || '');
          // Newest first, so the FIRST vote-shaped row is the standing one.
          // "vote undone" first means the vote was taken back.
          if (st.vote === null) {
            if (why === 'worth it' || why === 'not worth it') {
              st.vote = why === 'worth it' ? 'up' : 'down';
            } else if (why.indexOf('vote undone') === 0) {
              st.vote = false;   // decided: no standing vote
            }
          }
          if (why.indexOf('report detail') === 0) st.detailed = true;
          else if (why.indexOf('report') === 0) st.reported = true;
        });
        if (st.vote === false) st.vote = null;
      })
      .catch(function() {});
  }
  function paint(box) {
    var v = state(box.dataset.tree).vote;
    box.querySelectorAll('.worthit-btn').forEach(function(b) {
      var on = v === b.dataset.vote;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    show(box, '.worthit-done', !!v);
  }
  function openWhy(box, heading) {
    var why = box.querySelector('.worthit-why');
    if (!why || state(box.dataset.tree).reported) return;
    var q = why.querySelector('.worthit-q');
    if (q) q.textContent = heading;
    why.hidden = false;
    var rep = box.querySelector('.worthit-report');
    if (rep) rep.setAttribute('aria-expanded', 'true');
  }
  // One tap did the reporting (Hidde, 2026-08-14: "filling in the form is
  // quite an effort while a thumb is very inviting"). What unfolds after it
  // is the one question whose answer lets a run close the case, asked right
  // here (Hidde, 2026-08-21: "i want them to tell us which of the two elms
  // it is"), never a redirect to the form: the Google Maps convention is
  // "Add details (optional)" inside the same sheet, and sending people away
  // for an optional sentence lost the context when they came back.
  function reportDone(box) {
    var tree = box.dataset.tree;
    show(box, '.worthit-why', false);
    show(box, '.worthit-report', false);
    show(box, '.worthit-thanks', true);
    var form = box.querySelector('.worthit-detail');
    if (!form) return;
    if (state(tree).detailed) {
      form.hidden = true;
      box.querySelector('.worthit-thanks').textContent = 'Thanks, that helps.';
      return;
    }
    var reason = state(tree).reason;
    var chip = reason ? box.querySelector('.worthit-chip[data-reason="' + reason + '"]') : null;
    var q = form.querySelector('.worthit-q'), ta = form.querySelector('textarea');
    if (chip && q) q.textContent = chip.dataset.q || q.textContent;
    if (chip && ta) ta.placeholder = chip.dataset.ph || '';
    form.hidden = false;
  }
  // Paint what is known now (nothing), then again once the account answers.
  // A control that is briefly blank is honest; one that says "you voted" from
  // a stale browser key is not.
  document.querySelectorAll('.worthit').forEach(function(box) {
    paint(box);
    load(box).then(function() {
      paint(box);
      if (state(box.dataset.tree).reported) reportDone(box);
    });
  });
  document.addEventListener('submit', function(e) {
    var form = e.target.closest('.worthit-detail');
    if (!form) return;
    e.preventDefault();
    var box = form.closest('.worthit');
    if (!session()) {
      if (window.atOpenSignIn) window.atOpenSignIn(box.dataset.name, 'feedback');
      return;
    }
    var text = (form.querySelector('textarea').value || '').trim();
    if (!text) return;
    send(box, 'report detail', text.slice(0, 1000));
    state(box.dataset.tree).detailed = true;
    reportDone(box);
  });
  document.addEventListener('click', function(e) {
    var btn = e.target.closest('.worthit-btn, .worthit-chip, .worthit-report');
    if (!btn || btn.type === 'submit') return;
    var box = btn.closest('.worthit');
    if (!box) return;
    var tree = box.dataset.tree;

    // The gate: options visible to everyone, acting needs the account.
    // Opening the why-list stays free (it is looking, not acting).
    if (!session() && !btn.classList.contains('worthit-report')) {
      if (window.atOpenSignIn) window.atOpenSignIn(box.dataset.name, 'feedback');
      return;
    }

    if (btn.classList.contains('worthit-report')) {
      var why = box.querySelector('.worthit-why');
      var open = why && why.hidden;
      if (why) {
        var q = why.querySelector('.worthit-q');
        if (q) q.textContent = "What's wrong?";
        why.hidden = !open;
      }
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      return;
    }

    if (btn.classList.contains('worthit-btn')) {
      var st = state(tree);
      var cur = st.vote;
      var vote = btn.dataset.vote;
      if (cur === vote) {
        // Accidental or changed mind: undo writes a compensating row, so the
        // tally nets out without anonymous deletes.
        st.vote = null;
        send(box, 'vote undone', cur === 'up' ? 'worth it' : 'not worth it');
        paint(box);
        return;
      }
      if (cur) send(box, 'vote undone', cur === 'up' ? 'worth it' : 'not worth it');
      st.vote = vote;
      send(box, vote === 'up' ? 'worth it' : 'not worth it', '');
      paint(box);
      // The app-store convention: the vote already counted; the why is an
      // optional follow-up, never an interrogation.
      if (vote === 'down') openWhy(box, 'Care to say why? (optional)');
      return;
    }

    if (state(tree).reported) { reportDone(box); return; }
    state(tree).reported = true;
    state(tree).reason = btn.dataset.reason;
    send(box, 'report', btn.dataset.reason);
    reportDone(box);
  });
})();
</script>
`;
