import re
import base64
from pkg.logger.logger import log_info

class SecretAnalyzer:
    def __init__(self):
        self.patterns = {
            "AWS Key": re.compile(r'AKIA[0-9A-Z]{16}'),
            "Google API Key": re.compile(r'AIza[0-9A-Za-z\-_]{35}'),
            "JWT Token": re.compile(r'eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+'),
            "Base64 Potential": re.compile(r'[a-zA-Z0-9+/]{20,}={0,2}')
        }

    def scan_content(self, content):
        found = []
        for name, pattern in self.patterns.items():
            matches = pattern.findall(content)
            for match in matches:
                if name == "Base64 Potential":
                    try:
                        decoded = base64.b64decode(match).decode('utf-8', errors='ignore')
                        if len(decoded) > 10:
                             found.append(f"Found Base64 Content ({match}) -> Decoded: {decoded[:50]}...")
                    except Exception:
                        pass
                else:
                    found.append(f"Found {name}: {match}")
        return found
