import asyncio
import aiohttp
import os
from pkg.logger.logger import log_info, log_error

async def brute_force_paths(url, wordlist_path):
    if not os.path.exists(wordlist_path):
        log_error(f"Wordlist not found: {wordlist_path}")
        return []

    log_info(f"Brute forcing paths on {url} using {os.path.basename(wordlist_path)}")
    found = []
    
    try:
        with open(wordlist_path, 'r') as f:
            paths = [line.strip() for line in f if line.strip()]

        async with aiohttp.ClientSession() as session:
            tasks = []
            semaphore = asyncio.Semaphore(20) # Limit concurrency

            async def check_path(path):
                async with semaphore:
                    target = f"{url.rstrip('/')}/{path.lstrip('/')}"
                    try:
                        async with session.get(target, timeout=5, ssl=False, allow_redirects=False) as response:
                            if response.status in [200, 204, 301, 302, 403]:
                                found.append({"url": target, "status": response.status})
                    except Exception:
                        pass

            tasks = [check_path(p) for p in paths]
            await asyncio.gather(*tasks)
            
        return found
    except Exception as e:
        log_error(f"Brute force failed for {url}: {e}")
        return []
