"""Serves site/dist for the in-app preview. Lives in the repo so
.claude/launch.json survives session restarts (the per-session scratchpad
path 404'd on every new session until 2026-07-31)."""
import os
import http.server

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site", "dist")


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, *a):
        pass


http.server.HTTPServer(("127.0.0.1", 8971), H).serve_forever()
