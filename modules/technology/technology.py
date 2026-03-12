import asyncio.subprocess
import json
import os
from pkg.logger.logger import log_info, log_error

async def detect_technologies(url, log_dir):
    log_info(f"Detecting technologies for: {url}")
    output_file = os.path.join(log_dir, "technologies.json")
    
    try:
        # Using httpx for technology detection as per SRS
        process = await asyncio.create_subprocess_exec(
            "httpx", "-u", url, "-td", "-json", "-o", output_file, "-silent",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()
        
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                res = json.load(f)
                return res.get("technologies", [])
        return []
    except Exception as e:
        log_error(f"Tech detection failed: {e}")
        return []
