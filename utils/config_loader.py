import yaml
from typing import Dict, Any

class ConfigLoader:
    @staticmethod
    def load(config_path: str) -> Dict[str, Any]:
        """
        Loads the configuration from a YAML file.
        """
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            print(f"Warning: Config file {config_path} not found. Using defaults.")
            return {}
