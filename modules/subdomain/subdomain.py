import asyncio
import asyncio.subprocess
from pkg.logger.logger import log_info, log_error

class Enumerator:
    def __init__(self, target, depth):
        self.target = target
        self.depth = depth

    async def enumerate(self):
        log_info(f"Starting Subdomain Enumeration for: {self.target} (Depth: {self.depth})")
        
        try:
            process = await asyncio.create_subprocess_exec(
                "subfinder", "-d", self.target, "-silent",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                log_error(f"subfinder failed: {stderr.decode().strip()}")
                return []

            subs = stdout.decode().strip().split('\n')
            cleaned_subs = [s.strip() for s in subs if s.strip()]
            return cleaned_subs
            
        except Exception as e:
            log_error(f"Subdomain enumeration error: {e}")
            return []
