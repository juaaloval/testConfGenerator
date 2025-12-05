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
            with open("config.yaml", 'r') as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            logger.warning("Config file not found.")
            return {
                "llm": {
                    "model_path": "model/llama_32_3B_Q4_K_M.gguf", # Path to the local LLM
                    "temperature": 0.3,
                    "device": "cpu",
                    "max_tokens": 3000
                },
                "generation": {
                    "n_valid_values": 9,
                    "n_invalid_values": 1
                }
            }
