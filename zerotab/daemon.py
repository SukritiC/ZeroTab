import asyncio
import logging
import sys
from .lru import TabLRU
from .storage import TabStorage
from .browser_api import MacOSAppleScriptAPI, CDPBrowserAPI

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ZeroTabDaemon:
    def __init__(self, browser: str = "chrome", timeout_seconds: int = 300, max_ram_mb: int = 4096, poll_interval: int = 5):
        self.browser = browser.lower()
        self.timeout_seconds = timeout_seconds
        self.max_ram_mb = max_ram_mb
        self.poll_interval = poll_interval
        
        self.lru = TabLRU(capacity=1000)
        self.storage = TabStorage()
        
        if sys.platform == "darwin":
            self.api = MacOSAppleScriptAPI(browser_name=self.browser)
        else:
            if self.browser == "safari":
                logger.error("Safari is only supported on macOS.")
                sys.exit(1)
            # Use CDP for Windows/Linux
            self.api = CDPBrowserAPI(browser_name=self.browser, port=9222)
            logger.info(f"Using CDP on port 9222 for Windows/Linux. Make sure {self.browser} was launched with --remote-debugging-port=9222")
            
        self.running = False

    async def _poll_tabs(self):
        """Poll open tabs and update the LRU cache."""
        try:
            # We use asyncio.to_thread because the API calls might be blocking
            tabs = await asyncio.to_thread(self.api.get_tabs)
            active_url = await asyncio.to_thread(self.api.get_active_tab_url)
            
            # Create a set of current tab urls to identify closed tabs
            current_tab_urls = set()
            
            for tab in tabs:
                url = tab.get("url")
                if url and not url.startswith("chrome://") and "stub.html" not in url:
                    current_tab_urls.add(url)
                    
                    if url == active_url:
                        self.lru.touch(url)
                    else:
                        if self.lru.get(url) is None:
                            self.lru.put(url, tab)
            
            # Clean up closed tabs from LRU to prevent memory leaks
            for url in list(self.lru.cache.keys()):
                if url not in current_tab_urls:
                    del self.lru.cache[url]
                    
        except Exception as e:
            logger.error(f"Error polling tabs: {e}")

    async def _evict_idle_tabs(self):
        """Check for idle tabs and evict them."""
        try:
            evicted_tabs = self.lru.evict_idle(self.timeout_seconds)
            for url, tab_info in evicted_tabs:
                logger.info(f"Evicting idle tab: {tab_info.get('title', url)}")
                
                # Compress and save state
                await asyncio.to_thread(self.storage.save_tab, url, tab_info)
                
                # Navigate tab to stub
                success = await asyncio.to_thread(self.api.evict_tab, url)
                if not success:
                    logger.warning(f"Failed to evict tab in browser: {url}")
        except Exception as e:
            logger.error(f"Error evicting tabs: {e}")

    async def start(self):
        """Start the daemon loop."""
        self.running = True
        logger.info(f"Starting ZeroTab Daemon for {self.browser.capitalize()} (Timeout: {self.timeout_seconds}s, Poll: {self.poll_interval}s)")
        
        while self.running:
            await self._poll_tabs()
            await self._evict_idle_tabs()
            await asyncio.sleep(self.poll_interval)
            
    def stop(self):
        """Stop the daemon loop."""
        self.running = False
        logger.info("Stopping ZeroTab Daemon.")
