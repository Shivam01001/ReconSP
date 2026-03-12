import asyncio.subprocess
from pkg.logger.logger import log_info, log_error, log_success

async def check_takeover(domains):
    log_info(f"Checking {len(domains)} domains for subdomain takeover...")
    # Using subjack if available, or a simple python-based check
    # For now, we'll implement a wrapper for subzy/subjack pattern
    try:
        # Create a temp file for domains
        with open("temp_takeover.txt", "w") as f:
            f.write("\n".join(domains))
        
        process = await asyncio.create_subprocess_exec(
            "subzy", "run", "--targets", "temp_takeover.txt",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await process.communicate()
        
        results = stdout.decode().strip()
        if "VULNERABLE" in results:
            log_success("Potential subdomain takeover discovered!")
            
        return results
    except Exception as e:
        log_error(f"Takeover check failed: {e}")
        return ""
