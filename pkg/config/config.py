import yaml
import os

class Config:
    def __init__(self):
        self.rate_limit = 100
        self.max_workers = 50
        self.depth_limit = 3
        self.enable_cloud_scan = True
        self.enable_takeover_scan = True
        self.proxy = None

    def load(self, config_path="configs/config.yaml"):
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                data = yaml.safe_load(f)
                if data:
                    self.rate_limit = data.get('rate_limit', self.rate_limit)
                    self.max_workers = data.get('max_workers', self.max_workers)
                    self.depth_limit = data.get('depth_limit', self.depth_limit)
                    self.enable_cloud_scan = data.get('enable_cloud_scan', self.enable_cloud_scan)
                    self.enable_takeover_scan = data.get('enable_takeover_scan', self.enable_takeover_scan)
                    self.proxy = data.get('proxy', self.proxy)

app_config = Config()
