#!/usr/bin/env python3
import os, hashlib, xml.etree.ElementTree as ET, sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).parent
APP_DIR = BASE_DIR / "apps"
REPO_DIR = BASE_DIR / "repo"

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            apps = list(APP_DIR.glob("*.apk")) if APP_DIR.exists() else []
            html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>F-Droid Repo</title>
<style>
body {{ font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
h1 {{ color: #009688; }}
.app {{ background: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 8px; }}
a {{ color: #009688; text-decoration: none; }}
code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
</style>
</head><body>
<h1>F-Droid Simple Repo</h1>
<p>Repository URL: <code>http://localhost:8000</code></p>
<h2>Apps ({len(apps)}):</h2>"""
            
            for app in sorted(apps, key=lambda x: x.name):
                size = app.stat().st_size
                size_mb = size / (1024*1024)
                html += f'<div class="app"><h3>{app.stem}</h3><p>Size: {size_mb:.2f} MB</p>'
                html += f'<a href="/apps/{urllib.parse.quote(app.name)}">Download APK</a></div>'
            
            html += """<p style="color:#888;font-size:0.9em">Add to F-Droid: Settings > Repositories > Add</p>
</body></html>"""
            
            self.wfile.write(html.encode("utf-8"))
        
        elif self.path.startswith("/apps/"):
            filename = urllib.parse.unquote(self.path[6:])
            filepath = APP_DIR / filename
            if filepath.exists() and filename.endswith(".apk"):
                self.send_response(200)
                self.send_header("Content-Type", "application/vnd.android.package-archive")
                self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
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
        
        else:
            super().do_GET()

if __name__ == "__main__":
    APP_DIR.mkdir(exist_ok=True)
    REPO_DIR.mkdir(exist_ok=True)
    
    apps = list(APP_DIR.glob("*.apk"))
    root = ET.Element("repositories")
    root.set("xmlns", "http://f-droid.org/xml/delivery")
    repo = ET.SubElement(root, "repo")
    repo.set("name", "Simple F-Droid Repo")
    repo.set("url", "http://localhost:8000")
    
    for app in apps:
        with open(app, "rb") as f:
            content_hash = hashlib.sha256(f.read()).hexdigest()
        app_elem = ET.SubElement(repo, "app")
        app_elem.set("package", app.stem)
        app_elem.set("versionCode", "1")
        app_elem.set("versionName", "1.0.0")
        app_elem.set("contentHash", content_hash)
        app_elem.set("size", str(app.stat().st_size))
    
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(REPO_DIR / "repos.xml", encoding="utf-8", xml_declaration=True)
    
    print("Starting server on port 8000...")
    server = HTTPServer(("localhost", 8000), Handler)
    server.serve_forever()