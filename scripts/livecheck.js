// THE LIVE SITE, signed out, tapped (2026-10-07). Hidde: "on the website i can
// still click on the ambassador thing without logging in". Every check so far
// ran against the BUILD; this runs against ancienttrees.app itself from a
// runner with network, so a stale edge cache or a deploy that never landed is
// measured rather than argued. For each page and control: clear storage, click,
// and report what opened, whether it is actually visible, what was stored and
// what was sent to Supabase.
const { chromium } = require('playwright-core');
const pages = (process.env.LIVE_PAGES || '/aachen,/aachen/forster-linde,/explore,/es/aachen').split(',');
const controls = ['.ambassador-apply', '.save-btn', '.worthit-btn', '.mf[data-f="fav"]', '.mf[data-f="mine"]'];
(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROME || '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const out = [];
  for (const p of pages) {
    const ctx = await browser.newContext({ viewport: { width: 420, height: 900 } });
    const page = await ctx.newPage();
    const writes = [];
    // Our own cookieless page-event beacon (rest/v1/events) is anonymous by
    // design and is not an account write.
    page.on('request', r => { if (r.url().includes('supabase') && r.method() !== 'GET' && !r.url().includes('/rest/v1/events')) writes.push(r.method() + ' ' + r.url().split('?')[0].slice(-40)); });
    const url = 'https://ancienttrees.app' + p;
    const resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    const h = resp ? resp.headers() : {};
    const served = { cache: h['cf-cache-status'] || h['x-cache'] || '', age: h['age'] || '', modified: h['last-modified'] || '', etag: h['etag'] || '' };
    const html = await page.content();
    const build = { served, gate: html.includes("C.gate(function() { open(); }"), intent: html.includes("kind: 'ambassador'"), writeTo: html.includes('amb-who'), chipsBeforeMap: html.indexOf("querySelectorAll('.mf[data-f]')") > 0 && html.indexOf("querySelectorAll('.mf[data-f]')") < html.indexOf('new maplibregl.Map') };
    console.log('PAGE ' + p + ' ' + JSON.stringify(build));
    // No session, and NOT A VISITOR: at_notrack is the flag the page beacon
    // honours, so a runner's taps never land in the product funnel. The first
    // four runs on 2026-10-07 had put eight sign-in opens on /aachen into the
    // events table, which the seat-tap probe then had to explain away.
    await page.evaluate(() => { try { localStorage.clear(); sessionStorage.clear(); localStorage.setItem('at_notrack', '1'); } catch (e) {} });
    await page.reload({ waitUntil: 'networkidle' });
    await page.waitForTimeout(2500);
    for (const sel of controls) {
      // The first VISIBLE match: a tree page carries a hidden heart in the bar
      // before the one on the page.
      let b = null;
      for (const cand of await page.$$(sel)) { const bb = await cand.boundingBox(); if (bb && bb.width > 0 && bb.height > 0) { b = cand; break; } }
      if (!b) continue;
      // Bring it into view the way the page scrolls (a city page scrolls in a
      // container, not the window), then measure where it is.
      await b.evaluate(el => el.scrollIntoView({ block: 'center', inline: 'nearest' }));
      await page.waitForTimeout(400);
      const w0 = writes.length;
      await page.evaluate(() => { const d = document.getElementById('signin-dialog'); if (d && d.open) d.close(); });
      await page.waitForTimeout(200);
      // What a finger meets: where the control is, and what is on top of it.
      const where = await page.evaluate((sel) => {
        const el = document.querySelector(sel); const r = el.getBoundingClientRect();
        const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
        return { box: [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)], inView: r.top >= 0 && r.bottom <= innerHeight,
                 onTop: top ? (top.tagName.toLowerCase() + (top.id ? '#' + top.id : '') + (top.className && typeof top.className === 'string' ? '.' + top.className.trim().split(/\s+/).slice(0, 2).join('.') : '')) : null,
                 covered: !!(top && el !== top && !el.contains(top)) };
      }, sel);
      try { await b.click({ timeout: 8000 }); }
      catch (e) {
        // Say what stood in the way, then press through it the way a finger
        // that has scrolled would, so the gate itself is still measured.
        out.push({ page: p, control: sel, error: String(e).split('\n').filter(l => /intercepts|outside|not visible|hidden|receives/.test(l)).slice(0, 2).join(' | ').slice(0, 160) || String(e).slice(0, 120), where, build });
        try { await b.evaluate(el => el.click()); } catch (e2) { continue; }
      }
      await page.waitForTimeout(1500);
      const r = await page.evaluate((sel) => {
        const d = document.getElementById('signin-dialog');
        const a = document.getElementById('amb-dialog');
        const vis = (el) => { if (!el || !el.open) return false; const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; };
        return { signinOpen: !!(d && d.open), signinVisible: vis(d), ambassadorConfirmOpen: !!(a && a.open), stored: Object.keys(localStorage), pending: localStorage.getItem('ancienttrees_pending'),
                 pressed: document.querySelectorAll('[aria-pressed="true"]').length, hasSignIn: typeof window.atOpenSignIn, hasGate: !!(window.atCollection && window.atCollection.gate) };
      }, sel);
      r.page = p; r.control = sel; r.writes = writes.slice(w0); r.build = build; r.where = where;
      out.push(r);
    }
    await ctx.close();
  }
  await browser.close();
  console.log('LIVE RESULT ' + JSON.stringify(out, null, 1));
  // A refused click that was then pressed through is reported for the
  // record, not counted: the row that follows it is the verdict.
  const pressed = new Set(out.filter(r => !r.error).map(r => r.page + ' ' + r.control));
  const bad = out.filter(r => (r.error && !pressed.has(r.page + ' ' + r.control)) || (!r.error && !r.signinOpen) || (r.signinOpen && !r.signinVisible) || r.ambassadorConfirmOpen || (r.writes && r.writes.length) || (r.stored && r.stored.some(k => k !== 'ancienttrees_pending' && k !== 'at_notrack')));
  console.log(bad.length ? 'LIVE: ' + bad.length + ' control(s) did not ask, or asked invisibly, or acted' : 'LIVE: every control asked for sign-in, visibly, and nothing was stored or sent');
  process.exit(bad.length ? 1 : 0);
})();
