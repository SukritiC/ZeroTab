import subprocess
import json
import os
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Optional, Any

class BrowserAPI:
    def __init__(self, browser_name: str, stub_dir: str = "~/.zerotab/stubs"):
        self.browser_name = browser_name.lower()
        self.stub_dir = Path(os.path.expanduser(stub_dir))
        self.stub_dir.mkdir(parents=True, exist_ok=True)
        self.stub_file = self.stub_dir / "stub.html"
        self._create_stub_html()

    def _create_stub_html(self):
        """Creates a generic HTML stub that redirects when clicked or loaded."""
        if not self.stub_file.exists():
            html_content = """<!DOCTYPE html>
<html>
<head>
    <title>ZeroTab - Tab Suspended</title>
    <style>
        body { font-family: system-ui, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f4f4f5; color: #18181b; }
        .container { text-align: center; max-width: 500px; padding: 2rem; background: white; border-radius: 12px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
        h1 { margin-top: 0; }
        p { color: #52525b; }
        a { display: inline-block; margin-top: 1rem; padding: 0.5rem 1rem; background-color: #2563eb; color: white; text-decoration: none; border-radius: 6px; font-weight: 500; }
        a:hover { background-color: #1d4ed8; }
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const params = new URLSearchParams(window.location.search);
            const originalUrl = params.get('url');
            if (originalUrl) {
                const link = document.getElementById('restore-link');
                link.href = originalUrl;
            }
        });
    </script>
</head>
<body>
    <div class="container">
        <h1>Tab Suspended</h1>
        <p>This tab was compressed by ZeroTab to save memory.</p>
        <a id="restore-link" href="#">Click to Restore</a>
    </div>
</body>
</html>"""
            self.stub_file.write_text(html_content, encoding='utf-8')

    def get_tabs(self) -> List[Dict[str, str]]:
        raise NotImplementedError

    def evict_tab(self, url: str) -> bool:
        raise NotImplementedError

    def get_active_tab_url(self) -> str:
        raise NotImplementedError

class MacOSAppleScriptAPI(BrowserAPI):
    def __init__(self, browser_name: str, **kwargs):
        super().__init__(browser_name, **kwargs)
        # Map simple browser names to their macOS Application Names
        self.app_map = {
            "chrome": "Google Chrome",
            "edge": "Microsoft Edge",
            "opera": "Opera",
            "brave": "Brave Browser",
            "safari": "Safari"
        }
        self.app_name = self.app_map.get(self.browser_name, "Google Chrome")
        self.is_webkit = self.browser_name == "safari"

    def get_tabs(self) -> List[Dict[str, str]]:
        if self.is_webkit:
            jxa_script = f"""
            var Browser = Application('{self.app_name}');
            var tabsData = [];
            if (Browser.running()) {{
                Browser.windows().forEach(function(win) {{
                    try {{
                        win.tabs().forEach(function(t) {{
                            tabsData.push({{ url: t.url(), title: t.name() }});
                        }});
                    }} catch(e) {{}}
                }});
            }}
            JSON.stringify(tabsData);
            """
        else:
            jxa_script = f"""
            var Browser = Application('{self.app_name}');
            var tabsData = [];
            if (Browser.running()) {{
                Browser.windows().forEach(function(win) {{
                    try {{
                        win.tabs().forEach(function(t) {{
                            tabsData.push({{ url: t.url(), title: t.name() }});
                        }});
                    }} catch(e) {{}}
                }});
            }}
            JSON.stringify(tabsData);
            """
        try:
            result = subprocess.run(['osascript', '-l', 'JavaScript', '-e', jxa_script], 
                                    capture_output=True, text=True, check=True)
            output = result.stdout.strip()
            if output:
                return json.loads(output)
        except subprocess.CalledProcessError:
            pass
        return []

    def evict_tab(self, url: str) -> bool:
        if url.startswith("file://") and "stub.html" in url:
            return False
        if not url or url.startswith("chrome://"):
            return False

        stub_url = f"file://{self.stub_file.absolute()}?url={urllib.parse.quote(url)}"
        
        jxa_script = f"""
        var Browser = Application('{self.app_name}');
        var targetUrl = "{url}";
        var stubUrl = "{stub_url}";
        var evicted = false;
        
        if (Browser.running()) {{
            Browser.windows().forEach(function(win) {{
                try {{
                    win.tabs().forEach(function(t) {{
                        if (t.url() === targetUrl) {{
                            t.url = stubUrl;
                            evicted = true;
                        }}
                    }});
                }} catch(e) {{}}
            }});
        }}
        evicted;
        """
        try:
            result = subprocess.run(['osascript', '-l', 'JavaScript', '-e', jxa_script], 
                                    capture_output=True, text=True, check=True)
            return result.stdout.strip() == 'true'
        except subprocess.CalledProcessError:
            return False
            
    def get_active_tab_url(self) -> str:
        jxa_script = f"""
        var Browser = Application('{self.app_name}');
        var activeUrl = "";
        if (Browser.running() && Browser.frontmost()) {{
            try {{
                var win = Browser.windows[0];
                if (win) {{
                    var tab = win.{"currentTab" if self.is_webkit else "activeTab"}();
                    activeUrl = tab.url();
                }}
            }} catch(e) {{}}
        }}
        activeUrl;
        """
        try:
            result = subprocess.run(['osascript', '-l', 'JavaScript', '-e', jxa_script], 
                                    capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return ""

class CDPBrowserAPI(BrowserAPI):
    """
    Interfaces with Chromium-based browsers via the Chrome Remote Debugging Protocol.
    Requires the browser to be started with --remote-debugging-port=9222.
    """
    def __init__(self, browser_name: str, port: int = 9222, **kwargs):
        super().__init__(browser_name, **kwargs)
        self.port = port
        self.base_url = f"http://127.0.0.1:{self.port}"
        
    def _fetch_json(self, path: str) -> Optional[Any]:
        try:
            req = urllib.request.Request(f"{self.base_url}{path}")
            with urllib.request.urlopen(req, timeout=2) as response:
                return json.loads(response.read().decode('utf-8'))
        except (urllib.error.URLError, json.JSONDecodeError):
            return None

    def get_tabs(self) -> List[Dict[str, str]]:
        tabs_data = self._fetch_json("/json/list")
        if not tabs_data:
            return []
            
        tabs = []
        for t in tabs_data:
            if t.get('type') == 'page' and not t.get('url', '').startswith('chrome://'):
                tabs.append({
                    "url": t.get('url'),
                    "title": t.get('title'),
                    "id": t.get('id')
                })
        return tabs

    def evict_tab(self, url: str) -> bool:
        if url.startswith("file://") and "stub.html" in url:
            return False
            
        tabs_data = self._fetch_json("/json/list")
        if not tabs_data:
            return False
            
        target_tab_id = None
        for t in tabs_data:
            if t.get('url') == url:
                target_tab_id = t.get('id')
                break
                
        if not target_tab_id:
            return False
            
        # CDP doesn't have a simple HTTP endpoint to navigate an existing tab.
        # But we can close it, and open a new one with the stub.
        # Zero-dependency websocket is hard, so we just close the tab.
        # To restore, they have to click the stub. If we just close it, there's no stub in the browser!
        # Actually, without websockets, we can't cleanly navigate the tab via HTTP.
        # So we'll close the tab, and the stub is just gone. Or we can open a new tab with the stub.
        stub_url = f"file://{self.stub_file.absolute()}?url={urllib.parse.quote(url)}"
        
        # Close the target tab
        self._fetch_json(f"/json/close/{target_tab_id}")
        
        # Open a new tab with the stub
        # We need to URL encode the stub URL itself for the CDP endpoint
        # The endpoint is /json/new?{url}
        new_url_endpoint = f"/json/new?{urllib.parse.quote(stub_url)}"
        self._fetch_json(new_url_endpoint)
        
        return True

    def get_active_tab_url(self) -> str:
        # CDP HTTP endpoints don't reliably tell us which tab is actively focused in the window.
        # This is a limitation without full websockets or OS APIs.
        # For Phase 1 Windows/Linux CDP, we'll return an empty string to treat all tabs as background, 
        # or we could attempt to parse it if available. It's usually not exposed in /json/list.
        return ""
