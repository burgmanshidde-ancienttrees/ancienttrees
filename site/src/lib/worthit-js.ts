// The "Worth the visit?" control's one delegated script (design: Hidde,
// 2026-08-14; split into vote and report 2026-08-16, see WorthIt.astro for the
// reasoning and the convention it follows). One listener serves every control
// on the page, because a city page carries up to 46 of them.
//
// Two independent actions, which is the whole point of the rebuild:
//   the thumbs are an opinion, a toggle, complete on their own;
//   "Something's wrong" opens fact chips and reports a problem.
// They keep separate localStorage keys, so voting never blocks a correction and
// a correction never spends the vote. Someone may love a tree and still tell us
// the pin is wrong; the old nested version made that impossible.
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
// rule. No new backend, no accounts, no personal data.
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
  function paint(box) {
    var v = localStorage.getItem('at_worthit_' + box.dataset.tree);
    box.querySelectorAll('.worthit-btn').forEach(function(b) {
      var on = v === b.dataset.vote;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    show(box, '.worthit-done', !!v);
  }
  function openWhy(box, heading) {
    var why = box.querySelector('.worthit-why');
    if (!why || localStorage.getItem('at_wrong_' + box.dataset.tree)) return;
    var q = why.querySelector('.worthit-q');
    if (q) q.textContent = heading;
    why.hidden = false;
    var rep = box.querySelector('.worthit-report');
    if (rep) rep.setAttribute('aria-expanded', 'true');
  }
  function reportDone(box) {
    show(box, '.worthit-why', false);
    show(box, '.worthit-report', false);
    show(box, '.worthit-thanks', true);
    // One tap did the reporting; the form is only for whoever has more to say
    // (Hidde, 2026-08-14: "filling in the form is quite an effort while a thumb
    // is very inviting"). Offered, never required.
    show(box, '.worthit-more', true);
  }
  document.querySelectorAll('.worthit').forEach(paint);
  document.addEventListener('click', function(e) {
    var btn = e.target.closest('.worthit-btn, .worthit-chip, .worthit-report');
    if (!btn || btn.classList.contains('worthit-chip-link')) return;
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
      var vkey = 'at_worthit_' + tree;
      var cur = localStorage.getItem(vkey);
      var vote = btn.dataset.vote;
      if (cur === vote) {
        // Accidental or changed mind: undo writes a compensating row, so the
        // tally nets out without anonymous deletes.
        localStorage.removeItem(vkey);
        send(box, 'vote undone', cur === 'up' ? 'worth it' : 'not worth it');
        paint(box);
        return;
      }
      if (cur) send(box, 'vote undone', cur === 'up' ? 'worth it' : 'not worth it');
      localStorage.setItem(vkey, vote);
      send(box, vote === 'up' ? 'worth it' : 'not worth it', '');
      paint(box);
      // The app-store convention: the vote already counted; the why is an
      // optional follow-up, never an interrogation.
      if (vote === 'down') openWhy(box, 'Care to say why? (optional)');
      return;
    }

    var rkey = 'at_wrong_' + tree;
    if (localStorage.getItem(rkey)) { reportDone(box); return; }
    localStorage.setItem(rkey, btn.dataset.reason);
    send(box, 'report', btn.dataset.reason);
    reportDone(box);
  });
})();
</script>
`;
