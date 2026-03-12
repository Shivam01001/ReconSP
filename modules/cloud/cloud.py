import asyncio
import aiodns
from pkg.logger.logger import log_info, log_error

async def detect_cloud_assets(target):
    log_info(f"Scanning for cloud assets related to: {target}")
    buckets = [
        f"{target}-backup",
        f"{target}-assets",
        f"{target}-prod",
        f"{target}-dev",
        f"staging-{target}",
        f"assets-{target}"
    ]
    
    platforms = [
        ".s3.amazonaws.com",
        ".storage.googleapis.com",
        ".blob.core.windows.net"
    ]
    
    found = []
    resolver = aiodns.DNSResolver()
    
    for bucket in buckets:
        for platform in platforms:
            url = f"{bucket}{platform}"
            try:
                await resolver.query(url, 'A')
                found.append(url)
            except Exception:
                continue
                
    return found

