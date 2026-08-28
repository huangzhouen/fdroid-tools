#!/usr/bin/env python3
import os, hashlib, xml.etree.ElementTree as ET, sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).parent
APP_DIR = BASE_DIR / "apps"
REPO_DIR = BASE_DIR / "repo"
ICON_FILE = BASE_DIR / "icon.png"

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            apps = list(APP_DIR.glob("*.apk")) if APP_DIR.exists() else []
            port = sys.argv[1] if len(sys.argv) > 1 else "8000"
            icon_url = "/icon.png" if ICON_FILE.exists() else ""
            
            html = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>F-Droid Repo</title>
<style>
body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
h1 { color: #009688; }
.app { background: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 8px; }
a { color: #009688; text-decoration: none; }
code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
.icon-preview { max-width: 128px; margin: 10px 0; }
</style>
</head><body>
<h1>F-Droid Repository</h1>
"""
            if icon_url:
                html += '<img src="/icon.png" class="icon-preview" alt="Repo Icon">' + "\n"
            html += '<p>URL: <code>http://localhost:' + port + '</code></p>'
            html += '<h2>Apps (' + str(len(apps)) + '):</h2>'
            
            for app in sorted(apps, key=lambda x: x.name):
                size = app.stat().st_size
                size_mb = size / (1024*1024)
                html += '<div class="app"><h3>' + app.stem + '</h3><p>Size: ' + str(round(size_mb, 2)) + ' MB</p>'
                html += '<a href="/apps/' + urllib.parse.quote(app.name) + '">Download APK</a></div>'
            
            html += '<p style="color:#888;font-size:0.9em">Add to F-Droid: Settings > Repositories > Add</p>'
            html += '</body></html>'
            
            self.wfile.write(html.encode("utf-8"))
        
        elif self.path.startswith("/apps/"):
            filename = urllib.parse.unquote(self.path[6:])
            filepath = APP_DIR / filename
            if filepath.exists() and filename.endswith(".apk"):
                self.send_response(200)
                self.send_header("Content-Type", "application/vnd.android.package-archive")
                self.send_header("Content-Disposition", 'attachment; filename="' + filename + '"')
                self.end_headers()
                with open(filepath, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404)
        
        elif self.path == "/repo/repos.xml":
            if (REPO_DIR / "repos.xml").exists():
                self.send_response(200)
                self.send_header("Content-Type", "application/xml; charset=utf-8")
                self.end_headers()
                with open(REPO_DIR / "repos.xml", "r", encoding="utf-8") as f:
                    self.wfile.write(f.read().encode("utf-8"))
            else:
                self.send_error(404)
        
        elif self.path == "/icon.png":
            if ICON_FILE.exists():
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.end_headers()
                with open(ICON_FILE, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404)
        
        else:
            super().do_GET()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    APP_DIR.mkdir(exist_ok=True)
    REPO_DIR.mkdir(exist_ok=True)
    print("Starting F-Droid server on port " + str(port) + "...")
    server = HTTPServer(("localhost", port), Handler)
    server.serve_forever()