import re
import aiohttp
from pkg.logger.logger import log_info, log_error

class JSAnalyzer:
    def __init__(self):
        self.js_re = re.compile(r'<script.*?src=["\'](.*?.js.*?)["\']', re.IGNORECASE)
        self.api_re = re.compile(r'/(?:api|v[0-9])/[\w\-./]+')

    async def analyze(self, base_url):
        log_info(f"Analyzing JavaScript on: {base_url}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, timeout=10, ssl=False) as response:
                    if response.status != 200:
                        return []
                    body = await response.text()
                    
                    js_urls = self.js_re.findall(body)
                    endpoints = []
                    
                    for js_url in js_urls:
                        if not js_url.startswith("http"):
                            js_url = base_url.rstrip("/") + "/" + js_url.lstrip("/")
                            
                        js_content = await self.fetch_js(session, js_url)
                        if js_content:
                            api_matches = self.api_re.findall(js_content)
                            endpoints.extend(api_matches)
                    
                    return list(set(endpoints))
        except Exception as e:
            log_error(f"JS Analysis error for {base_url}: {e}")
            return []

    async def fetch_js(self, session, url):
        try:
            async with session.get(url, timeout=5, ssl=False) as response:
                if response.status == 200:
                    return await response.text()
        except Exception:
            pass
        return ""
