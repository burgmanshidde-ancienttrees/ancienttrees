#!/usr/bin/env python3
"""Mint the refresh token the daily digest uses to read Google Analytics.

Why this and not a service account: Hidde's Google Cloud organisation enforces
iam.disableServiceAccountKeyCreation (2026-10-12), so no key file can exist.
An OAuth client of the "Desktop app" kind is allowed, and it is how the digest
already reads Search Console (GSC_CLIENT_ID / GSC_CLIENT_SECRET /
GSC_REFRESH_TOKEN). This is the same pattern for a second, read-only scope.

Run on the Mac, once:
    python3 scripts/ga_auth.py ~/Downloads/client_secret_XXXX.json

It opens the browser, Hidde signs in with the account that owns the GA
property, and the client id, secret and refresh token are written to
~/.ancienttrees-ga.env (mode 600), never printed and never in the repository.
`gh secret set` then moves them into GitHub from that file.

The consent screen must be published ("In production") or the token dies
after seven days, which is Google's rule for apps in Testing.
"""
import http.server
import json
import os
import secrets
import sys
import threading
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

SCOPE = "https://www.googleapis.com/auth/analytics.readonly"
OUT = Path.home() / ".ancienttrees-ga.env"


def main():
    if len(sys.argv) != 2:
        print("usage: python3 scripts/ga_auth.py <client_secret.json>")
        return 2
    raw = json.loads(Path(sys.argv[1]).expanduser().read_text())
    c = raw.get("installed") or raw.get("web") or {}
    cid, csec = c.get("client_id"), c.get("client_secret")
    if not cid or not csec:
        print("that file holds no client_id/client_secret; download the JSON of a Desktop app client")
        return 2

    state = secrets.token_urlsafe(16)
    got = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if q.get("state", [""])[0] == state:
                got["code"] = q.get("code", [""])[0]
                got["error"] = q.get("error", [""])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Done. You can close this tab and go back to Claude.")

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    redirect = "http://127.0.0.1:%d/" % srv.server_port
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": cid, "redirect_uri": redirect, "response_type": "code",
        "scope": SCOPE, "access_type": "offline", "prompt": "consent", "state": state,
    })
    t = threading.Thread(target=srv.handle_request)
    t.start()
    print("Opening the browser. Sign in with the account that owns the Google Analytics property.")
    webbrowser.open(url)
    t.join(timeout=600)
    srv.server_close()
    if not got.get("code"):
        print("no code came back (%s)" % (got.get("error") or "timed out"))
        return 1

    body = urllib.parse.urlencode({
        "code": got["code"], "client_id": cid, "client_secret": csec,
        "redirect_uri": redirect, "grant_type": "authorization_code",
    }).encode()
    with urllib.request.urlopen("https://oauth2.googleapis.com/token", body, timeout=30) as r:
        tok = json.loads(r.read())
    refresh = tok.get("refresh_token")
    if not refresh:
        print("Google returned no refresh token; remove the app's access at myaccount.google.com/permissions and run again")
        return 1
    OUT.write_text("GA_CLIENT_ID=%s\nGA_CLIENT_SECRET=%s\nGA_REFRESH_TOKEN=%s\n" % (cid, csec, refresh))
    os.chmod(OUT, 0o600)
    print("written to %s (not printed). Next: tell Claude it worked." % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
