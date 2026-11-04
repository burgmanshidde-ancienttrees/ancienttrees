// What breaks on the website, told to us by the page it broke on (Hidde,
// 2026-11-04, the quality line: the app had MetricKit and the website had
// nothing, so a script that threw for one kind of visitor was invisible until
// somebody mailed).
//
// Every page carries this in the head, before any other page script, so an
// error in any of them is heard. It listens for window `error` and
// `unhandledrejection` and posts one small row to public.web_errors
// (supabase/web-errors.sql), read back by scripts/web_errors.py for the
// digest's quality line.
//
// WHAT A ROW HOLDS, AND NOTHING ELSE: the message (300 characters at most),
// the script file and line it came from, the page path without its query
// string, a browser family and major version ("Safari 18"), the build it ran
// and the day. No account, no session, no cookie, no full user agent, no
// query string, and the table keeps no IP address. A row cannot be traced to
// a person, which is why it needs no consent and no account.
//
// HOW MUCH: at most three reports per page load and each distinct error once,
// held in memory only. Nothing is written to the browser (hard rule 11 and
// check_nothing_is_stored_locally: a dedupe key on the device would be a
// store, and three a page load is a cap good enough at our volumes).
//
// WHAT IS LEFT OUT: errors from browser extensions and from scripts on other
// origins (the browser hands those over as a bare "Script error." with no
// file, and they are not ours to fix), and every page not served from
// ancienttrees.app (the smoke test and preview servers would report their own
// runs).
//
// NOT sendBeacon: a beacon carrying JSON is not a CORS-simple request and is
// dropped silently (the events table learned that on 2026-08-16, Base.astro).
// fetch with keepalive survives the unload the same way and sets the headers.
import { SUPABASE_URL, SUPABASE_KEY } from "./site-config";

// The commit the deploy built, so an error can be read against the version
// that threw it. GitHub Actions sets GITHUB_SHA on every run; a local build
// has none and reports "".
const BUILD_ID = (process.env.GITHUB_SHA || "").slice(0, 7);

export const WEB_ERRORS_JS = `
<script>
(function() {
  if (location.hostname !== 'ancienttrees.app') return;
  var sent = 0, seen = {};
  var origin = location.origin;
  function browser() {
    var ua = navigator.userAgent || '', m;
    var tests = [['Edge', /Edg(?:A|iOS)?\\/(\\d+)/], ['Opera', /OPR\\/(\\d+)/],
                 ['Samsung', /SamsungBrowser\\/(\\d+)/], ['Firefox', /(?:Firefox|FxiOS)\\/(\\d+)/],
                 ['Chrome', /(?:Chrome|CriOS)\\/(\\d+)/], ['Safari', /Version\\/(\\d+).*Safari/]];
    for (var i = 0; i < tests.length; i++) {
      m = ua.match(tests[i][1]);
      if (m) return tests[i][0] + ' ' + m[1];
    }
    return 'other';
  }
  function local(url) {
    // The file's path on our own origin, or null for anything else.
    if (!url) return null;
    if (url.indexOf(origin + '/') !== 0 && url !== origin) return null;
    var p = url.slice(origin.length).split('?')[0].split('#')[0] || '/';
    return p === location.pathname ? 'inline' : p;
  }
  function foreign(text) {
    return /(chrome|moz|safari|safari-web|ms-browser)-extension:\\/\\//.test(text || '');
  }
  function report(message, source, line) {
    try {
      if (sent >= 3) return;
      message = String(message || '').slice(0, 300);
      var key = message + '|' + source + '|' + line;
      if (seen[key]) return;
      seen[key] = 1;
      sent++;
      fetch('${SUPABASE_URL}/rest/v1/web_errors', {
        method: 'POST', keepalive: true,
        headers: { apikey: '${SUPABASE_KEY}', 'Content-Type': 'application/json', Prefer: 'return=minimal' },
        body: JSON.stringify({
          day: new Date().toISOString().slice(0, 10),
          message: message,
          source: String(source).slice(0, 200),
          line: line > 0 && line < 10000000 ? line : null,
          path: location.pathname.slice(0, 200),
          browser: browser(),
          build: '${BUILD_ID}'
        })
      }).catch(function() {});
    } catch (e) {}
  }
  window.addEventListener('error', function(e) {
    try {
      // A failed image or stylesheet fires error on the element, not a script fault.
      if (!e || !e.message || e.target !== window && e.target && e.target.tagName) return;
      if (e.message === 'Script error.' || foreign(e.filename)) return;
      var src = local(e.filename);
      if (!src) return;
      report(e.message, src, e.lineno || 0);
    } catch (err) {}
  });
  window.addEventListener('unhandledrejection', function(e) {
    try {
      var r = e && e.reason;
      var msg = r && r.message ? (r.name ? r.name + ': ' : '') + r.message : String(r);
      var stack = r && r.stack ? String(r.stack) : '';
      if (foreign(stack)) return;
      var src = 'promise', line = 0;
      if (stack) {
        var urls = stack.match(/https?:\\/\\/[^\\s)]+/g) || [];
        var mine = null;
        for (var i = 0; i < urls.length; i++) {
          var at = urls[i].match(/^(.*?):(\\d+)(?::\\d+)?$/);
          var p = local(at ? at[1] : urls[i]);
          if (p) { mine = p; line = at ? parseInt(at[2], 10) : 0; break; }
        }
        // A stack that names files, none of them ours, is somebody else's script.
        if (urls.length && !mine) return;
        if (mine) src = mine;
      }
      report(msg, src, line);
    } catch (err) {}
  });
})();
</script>
`;
