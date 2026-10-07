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
    page.on('request', r => { if (r.url().includes('supabase') && r.method() !== 'GET') writes.push(r.method() + ' ' + r.url().split('?')[0].slice(-40)); });
    const url = 'https://ancienttrees.app' + p;
    await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    const html = await page.content();
    const build = { gate: html.includes("C.gate(function() { open(); }"), intent: html.includes("kind: 'ambassador'"), chipsBeforeMap: html.indexOf("querySelectorAll('.mf[data-f]')") > 0 && html.indexOf("querySelectorAll('.mf[data-f]')") < html.indexOf('new maplibregl.Map') };
    await page.evaluate(() => { try { localStorage.clear(); sessionStorage.clear(); } catch (e) {} });
    await page.reload({ waitUntil: 'networkidle' });
    await page.waitForTimeout(2500);
    for (const sel of controls) {
      const b = await page.$(sel);
      if (!b) continue;
      const w0 = writes.length;
      await page.evaluate(() => { const d = document.getElementById('signin-dialog'); if (d && d.open) d.close(); });
      await page.waitForTimeout(200);
      try { await b.click({ timeout: 5000 }); } catch (e) { out.push({ page: p, control: sel, error: String(e).slice(0, 80) }); continue; }
      await page.waitForTimeout(1500);
      const r = await page.evaluate((sel) => {
        const d = document.getElementById('signin-dialog');
        const a = document.getElementById('amb-dialog');
        const vis = (el) => { if (!el || !el.open) return false; const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; };
        return { signinOpen: !!(d && d.open), signinVisible: vis(d), ambassadorConfirmOpen: !!(a && a.open), stored: Object.keys(localStorage), pending: localStorage.getItem('ancienttrees_pending'),
                 pressed: document.querySelectorAll('[aria-pressed="true"]').length, hasSignIn: typeof window.atOpenSignIn, hasGate: !!(window.atCollection && window.atCollection.gate) };
      }, sel);
      r.page = p; r.control = sel; r.writes = writes.slice(w0); r.build = build;
      out.push(r);
    }
    await ctx.close();
  }
  await browser.close();
  console.log('LIVE RESULT ' + JSON.stringify(out, null, 1));
  const bad = out.filter(r => r.error || (r.control && !r.signinOpen) || (r.signinOpen && !r.signinVisible) || r.ambassadorConfirmOpen || (r.writes && r.writes.length) || (r.stored && r.stored.some(k => k !== 'ancienttrees_pending')));
  console.log(bad.length ? 'LIVE: ' + bad.length + ' control(s) did not ask, or asked invisibly, or acted' : 'LIVE: every control asked for sign-in, visibly, and nothing was stored or sent');
  process.exit(bad.length ? 1 : 0);
})();
