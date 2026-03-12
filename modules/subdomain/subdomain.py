import asyncio
import asyncio.subprocess
from pkg.logger.logger import log_info, log_error, log_success

class Enumerator:
    def __init__(self, target, depth):
        self.target = target
        self.depth = depth

    async def enumerate(self):
        all_discovered = set()
        to_scan = {self.target}
        
        for current_depth in range(1, self.depth + 1):
            if not to_scan:
                break
                
            log_info(f"Subdomain Discovery Layer {current_depth}/{self.depth} for {len(to_scan)} targets...")
            
            tasks = [self._run_subfinder(target) for target in to_scan]
            results = await asyncio.gather(*tasks)
            
            new_discovered = set()
            for subs in results:
                new_discovered.update(subs)
            
            # Filter only new ones to avoid loops and redundant scans
            actual_new = new_discovered - all_discovered
            all_discovered.update(actual_new)
            
            # Next layer will scan the newly found subdomains
            to_scan = actual_new
            
            log_success(f"Layer {current_depth} completed. Total unique subdomains so far: {len(all_discovered)}")

        return list(all_discovered)

    async def _run_subfinder(self, target):
        try:
            process = await asyncio.create_subprocess_exec(
                "subfinder", "-d", target, "-silent",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                # Silently ignore errors for deep layers to keep logs clean
                return []

            subs = stdout.decode().strip().split('\n')
            return [s.strip() for s in subs if s.strip()]
            
        except Exception:
            return []
