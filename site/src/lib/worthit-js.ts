// The "Worth the visit?" control's one delegated script (design: Hidde,
// 2026-08-14; split into vote and report 2026-08-16, see WorthIt.astro for the
// reasoning and the convention it follows). One listener serves every control
// on the page, because a city page carries up to 46 of them.
//
// Two independent actions, which is the whole point of the rebuild:
//   the thumbs are an opinion, one tap, no follow-up question;
//   "Something's wrong" opens fact chips and reports a problem.
// They keep separate localStorage keys, so voting never blocks a correction and
// a correction never spends the vote. Someone may love a tree and still tell us
// the pin is wrong; the old nested version made that impossible.
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
  function send(box, verdict, reason) {
    var tree = box.dataset.tree, city = box.dataset.city, name = box.dataset.name;
    try {
      fetch('${SUPABASE_URL}/rest/v1/submissions', {
        method: 'POST',
        headers: {'apikey': '${SUPABASE_KEY}', 'Content-Type': 'application/json', 'Prefer': 'return=minimal'},
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
  function voteDone(box) {
    box.querySelectorAll('.worthit-btn').forEach(function(b) { b.hidden = true; });
    show(box, '.worthit-q', false);
    show(box, '.worthit-done', true);
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
  document.addEventListener('click', function(e) {
    var btn = e.target.closest('.worthit-btn, .worthit-chip, .worthit-report');
    if (!btn || btn.classList.contains('worthit-chip-link')) return;
    var box = btn.closest('.worthit');
    if (!box) return;
    var tree = box.dataset.tree;

    if (btn.classList.contains('worthit-report')) {
      var why = box.querySelector('.worthit-why');
      var open = why && why.hidden;
      if (why) why.hidden = !open;
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      return;
    }

    if (btn.classList.contains('worthit-btn')) {
      var vkey = 'at_worthit_' + tree;
      if (localStorage.getItem(vkey)) { voteDone(box); return; }
      var vote = btn.dataset.vote;
      localStorage.setItem(vkey, vote);
      send(box, vote === 'up' ? 'worth it' : 'not worth it', '');
      voteDone(box);
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
