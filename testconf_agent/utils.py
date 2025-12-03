import yaml
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ConfigLoader:
    @staticmethod
    def load() -> Dict[str, Any]:
        """
        Loads the configuration from a YAML file.
        """
        try:
            with open("../config.yaml", 'r') as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            logger.warning("Config file not found.")
            return {
                "llm": {
                    "model_id": "llama3.2:3b",
                    "temperature": 0.7,
                    "device": "cpu",
                    "max_tokens": 3000
                },
                "generation": {
                    "n_valid_values": 9,
                    "n_invalid_values": 1
                }
            }
