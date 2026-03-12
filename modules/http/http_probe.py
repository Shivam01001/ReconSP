import asyncio
import aiohttp
from pkg.logger.logger import log_info, log_error

async def probe_url(url, timeout=10):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout, allow_redirects=True, ssl=False) as response:
                return {
                    "url": str(response.url),
                    "status": response.status,
                    "server": response.headers.get("Server", "Unknown"),
                    "length": response.content_length,
                    "body": await response.text()
                }
    except Exception:
        return None

async def probe_batch(urls, max_concurrency=100):
    semaphore = asyncio.Semaphore(max_concurrency)
    live_hosts = []

    async def _probe(url):
        async with semaphore:
            result = await probe_url(url)
            if result:
                live_hosts.append(result)

    tasks = [_probe(url) for url in urls]
    await asyncio.gather(*tasks)
    return live_hosts
