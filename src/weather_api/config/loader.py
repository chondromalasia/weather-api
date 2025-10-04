import os
import yaml
from pathlib import Path
from typing import Dict, Any

class Config:
    def __init__(self):
        self.config_dir = Path(__file__).parent
        self.database_config = self.load_yaml(self.config_dir / 'database.yaml')['database']

    def load_yaml(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r') as f:
            content = f.read()
            return yaml.safe_load(content)
