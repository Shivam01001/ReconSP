import aiohttp
import json
from pkg.logger.logger import log_info, log_error

async def get_crt_sh_subdomains(target):
    log_info(f"Querying crt.sh for passive intelligence: {target}")
    url = f"https://crt.sh/?q=%25.{target}&output=json"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=30) as response:
                if response.status != 200:
                    log_error(f"crt.sh returned status {response.status}")
                    return []
                
                data = await response.json()
                subdomains = set()
                for entry in data:
                    name = entry.get("name_value", "")
                    if name:
                        for sub in name.split('\n'):
                            if sub.endswith(target):
                                subdomains.add(sub.strip().replace("*.", ""))
                
                return list(subdomains)
    except Exception as e:
        log_error(f"crt.sh query error: {e}")
        return []
