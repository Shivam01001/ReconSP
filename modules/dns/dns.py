import asyncio
import aiodns
from pkg.logger.logger import log_info, log_error

class DNSResolver:
    def __init__(self):
        self.resolver = aiodns.DNSResolver()

    async def resolve(self, domain):
        try:
            result = await self.resolver.query(domain, 'A')
            ips = [entry.host for entry in result]
            return ips
        except Exception:
            return []

    async def resolve_batch(self, domains, max_concurrency=50):
        semaphore = asyncio.Semaphore(max_concurrency)
        results = {}

        async def _resolve(domain):
            async with semaphore:
                ips = await self.resolve(domain)
                if ips:
                    results[domain] = ips

        tasks = [_resolve(domain) for domain in domains]
        await asyncio.gather(*tasks)
        return results
