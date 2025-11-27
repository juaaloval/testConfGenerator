import yaml
from typing import Dict, Any

class TestConfParser:
    @staticmethod
    def parse(file_path: str) -> Dict[str, Any]:
        """
        Parses the TestConf file and returns the raw dictionary.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def save(data: Dict[str, Any], file_path: str):
        """
        Saves the TestConf data to a file.
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, sort_keys=False)
