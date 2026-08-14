// The "Worth the visit?" control's one delegated script (design: Hidde,
// 2026-08-14, DECISIONS.md same date). One listener serves every control on
// the page, because a city page carries up to 46 of them.
//
// Where a vote goes: the same Supabase submissions table the /contribute form
// posts to (live since 2026-07-31), kind 'feedback', tree id and city
// prefilled from the control's own data attributes. Step 0b reads that table,
// so dead and wrong-location reports land in the existing correction flow
// with its same-day rule. No new backend, no accounts, no personal data.
//
// localStorage soft-dedupe, one vote per tree per browser (the passport
// pattern). Votes are stored and shown to nobody until volume makes a count
// honest; nothing here renders numbers.
import { SUPABASE_URL, SUPABASE_KEY } from "./site-config";

export const WORTHIT_JS = `
<script>
(function() {
  function send(tree, city, name, verdict, reason) {
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
  function done(box) {
    box.querySelectorAll('.worthit-btn').forEach(function(b) { b.hidden = true; });
    var why = box.querySelector('.worthit-why');
    if (why) why.hidden = true;
    box.querySelector('.worthit-q').hidden = true;
    box.querySelector('.worthit-done').hidden = false;
  }
  document.addEventListener('click', function(e) {
    var btn = e.target.closest('.worthit-btn, .worthit-chip');
    if (!btn || btn.classList.contains('worthit-chip-link')) return;
    var box = btn.closest('.worthit');
    var tree = box.dataset.tree;
    var key = 'at_worthit_' + tree;
    if (localStorage.getItem(key)) { done(box); return; }
    if (btn.classList.contains('worthit-btn')) {
      if (btn.dataset.vote === 'up') {
        localStorage.setItem(key, 'up');
        send(tree, box.dataset.city, box.dataset.name, 'worth it', '');
        done(box);
      } else {
        box.querySelector('.worthit-why').hidden = false;
        btn.hidden = true;
      }
    } else {
      localStorage.setItem(key, 'down');
      send(tree, box.dataset.city, box.dataset.name, 'not worth it', btn.dataset.reason);
      done(box);
    }
  });
})();
</script>
`;
