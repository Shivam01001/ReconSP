import asyncio
import os
import json
from datetime import datetime
from typing import List, Dict
from pkg.logger.logger import log_info, log_success, log_error, setup_logger
from pkg.config.config import app_config
from modules.subdomain.subdomain import Enumerator
from modules.passive.passive import get_crt_sh_subdomains
from modules.dns.dns import DNSResolver
from modules.http.http_probe import probe_batch
from modules.http.brute import brute_force_paths
from modules.vulnerability.vulnerability import NucleiScanner
from modules.js.js_analyzer import JSAnalyzer
from modules.takeover.takeover import check_takeover
from modules.cloud.cloud import detect_cloud_assets
from modules.technology.technology import detect_technologies
from modules.crawler.crawler import crawl_target
from modules.graphql.graphql import detect_graphql
from internal.secrets.secrets_analyzer import SecretAnalyzer
from internal.reporting.reporting import generate_report

class Orchestrator:
    def __init__(self, target: str, depth: int):
        self.target = target
        self.depth = depth
        self.log_dir = os.path.join("logs", target)
        self.start_time = datetime.now()
        
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(os.path.join(self.log_dir, "screenshots"), exist_ok=True)
        setup_logger(self.log_dir)

    async def run(self):
        log_info(f"Pipeline initialized for: {self.target} (Max Workers: {app_config.max_workers})")
        
        # 1. Passive Intelligence
        passive_subs: List[str] = await get_crt_sh_subdomains(self.target)
        
        # 2. Subdomain Enumeration (Recursive implementation)
        enumerator = Enumerator(self.target, self.depth)
        enum_subs: List[str] = await enumerator.enumerate()
        
        all_subs_list: List[str] = list(set(passive_subs + enum_subs))
        log_info(f"Total unique subdomains discovered: {len(all_subs_list)}")
        
        # 3. DNS Resolution
        resolver = DNSResolver()
        resolved_map: Dict[str, List[str]] = await resolver.resolve_batch(all_subs_list, max_concurrency=app_config.max_workers)
        
        # 4. Takeover Detection
        takeover_results = await check_takeover(list(resolved_map.keys()))
        
        # 5. Cloud Asset Discovery
        cloud_assets = await detect_cloud_assets(self.target)
        if cloud_assets:
            log_success(f"Found {len(cloud_assets)} potential cloud assets")

        # 6. Live Host Detection & Intelligence Gathering
        urls = []
        for domain in resolved_map.keys():
            urls.append(f"http://{domain}")
            urls.append(f"https://{domain}")
        
        live_probe_results = await probe_batch(urls, max_concurrency=app_config.max_workers)
        
        secret_analyzer = SecretAnalyzer()
        found_secrets = []
        all_js_endpoints = set()
        js_analyzer = JSAnalyzer()
        brute_results = []
        graphql_endpoints = []
        crawled_endpoints = []
        tech_map = {}

        for res in live_probe_results:
             # Scan for secrets in body
             secrets = secret_analyzer.scan_content(res['body'])
             found_secrets.extend(secrets)
             
             # GraphQL Detection
             gql = await detect_graphql(res['url'])
             graphql_endpoints.extend(gql)
             
             # Tech Detection
             techs = await detect_technologies(res['url'], self.log_dir)
             if techs:
                 tech_map[res['url']] = techs
             
             # Deep analysis for main target or high priority hosts
             if self.target in res['url']:
                 # Crawling
                 links = await crawl_target(res['url'], self.log_dir)
                 crawled_endpoints.extend(links)
                 
                 # JS Analysis
                 endpoints = await js_analyzer.analyze(res['url'])
                 all_js_endpoints.update(endpoints)
                 
                 # Wordlist-driven discovery (Discovery, Backup, Dev)
                 wordlists_to_check = [
                     "wordlists/discovery/top-10k-web-directories.txt",
                     "wordlists/discovery/api.txt",
                     "wordlists/discovery/admin.txt",
                     "wordlists/discovery/config.txt",
                     "wordlists/discovery/env.txt"
                 ]
                 for wl in wordlists_to_check:
                     if os.path.exists(wl):
                          brute = await brute_force_paths(res['url'], wl)
                          brute_results.extend(brute)
        
        # 7. Vulnerability Scanning
        scanner = NucleiScanner(self.target, self.log_dir)
        await scanner.run_scan()
        
        # 8. Report Generation
        subdomains_data = []
        for domain in all_subs_list:
            ips = resolved_map.get(domain, ["N/A"])
            probe = next((p for p in live_probe_results if domain in p['url']), None)
            
            techs = []
            if probe:
                 techs = tech_map.get(probe['url'], [])
            
            subdomains_data.append({
                "host": domain,
                "ip": ", ".join(ips),
                "status": str(probe['status']) if probe else "Down",
                "server": probe['server'] if probe else "N/A",
                "tech_stack": ", ".join(techs) if techs else "N/A"
            })

        vulns_data = []
        vuln_file = os.path.join(self.log_dir, "vulnerabilities.json")
        if os.path.exists(vuln_file):
            with open(vuln_file, 'r') as f:
                for line in f:
                    try:
                        v = json.loads(line)
                        vulns_data.append({
                            "name": v.get("info", {}).get("name", "Unknown"),
                            "severity": v.get("info", {}).get("severity", "info"),
                            "description": v.get("info", {}).get("description", "No description provided"),
                            "target": v.get("matched-at", self.target)
                        })
                    except Exception:
                        continue

        report_data = {
            "target": self.target,
            "subdomain_count": len(all_subs_list),
            "vulnerability_count": len(vulns_data),
            "risk_score": self._calculate_risk(vulns_data, cloud_assets, takeover_results),
            "subdomains": subdomains_data,
            "vulnerabilities": vulns_data,
            "js_endpoints": list(all_js_endpoints),
            "secrets": found_secrets,
            "cloud_assets": cloud_assets,
            "takeovers": takeover_results,
            "discovered_paths": brute_results,
            "graphql_endpoints": graphql_endpoints,
            "crawled_links": crawled_endpoints
        }

        generate_report(self.target, report_data, self.log_dir)
        
        end_time = datetime.now()
        duration = end_time - self.start_time
        log_success(f"ReconSP Pipeline finished in {duration}")

    def _calculate_risk(self, vulns, cloud, takeover):
        score = 100
        if takeover and "VULNERABLE" in takeover: score -= 40
        if cloud: score -= len(cloud) * 10
        for v in vulns:
            sev = v['severity'].lower()
            if sev == 'critical': score -= 30
            elif sev == 'high': score -= 15
            elif sev == 'medium': score -= 5
        score = max(0, score)
        if score > 85: return "Grade: A"
        if score > 70: return "Grade: B"
        if score > 50: return "Grade: C"
        return "Grade: F"
