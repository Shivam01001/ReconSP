import asyncio.subprocess
import os
from pkg.logger.logger import log_info, log_error, log_success

async def crawl_target(url, log_dir):
    log_info(f"Starting crawling engine for: {url}")
    output_file = os.path.join(log_dir, "endpoints.txt")
    
    try:
        # Using katana as per SRS recommendation
        process = await asyncio.create_subprocess_exec(
            "katana", "-u", url, "-silent", "-o", output_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()
        
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                links = [line.strip() for line in f if line.strip()]
                log_success(f"Crawling complete. Discovered {len(links)} endpoints.")
                return links
        return []
    except Exception:
        # Fallback if katana is not installed
        log_error("Katana not found. Skipping crawling engine.")
        return []

