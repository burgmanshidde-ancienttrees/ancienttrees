#!/usr/bin/env python3
"""Serve site/dist locally for previewing. Usage: python3 scripts/serve.py [port]"""
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

os.chdir(Path(__file__).resolve().parent.parent / "site" / "dist")
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8321
print(f"Serving site/dist at http://localhost:{port}")
HTTPServer(("127.0.0.1", port), SimpleHTTPRequestHandler).serve_forever()
