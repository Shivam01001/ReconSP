import aiohttp
from pkg.logger.logger import log_info

async def detect_graphql(url):
    common_endpoints = [
        "/graphql",
        "/api/graphql",
        "/v1/graphql",
        "/query",
        "/graphiql"
    ]
    
    found = []
    log_info(f"Checking for GraphQL endpoints on {url}...")
    
    async with aiohttp.ClientSession() as session:
        for endpoint in common_endpoints:
            target = f"{url.rstrip('/')}{endpoint}"
            try:
                # Introspection query pattern as per SRS
                introspection_query = {"query": "{__schema{queryType{name}}}"}
                async with session.post(target, json=introspection_query, timeout=5, ssl=False) as response:
                    if response.status == 200:
                        data = await response.json()
                        if "data" in data and "__schema" in data["data"]:
                            found.append(target)
            except Exception:
                continue
                
    return found
