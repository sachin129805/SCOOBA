import json
from pathlib import Path


class ConfigManager:
    """
    Loads and provides access to the SCOOBA configuration.
    """

    def __init__(self):
        config_path = Path(__file__).parent / "config.json"

        with open(config_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)

    def get(self, key, default=None):
        """
        Example:
        config.get("assistant.name")
        """

        value = self.config

        for part in key.split("."):
            if isinstance(value, dict):
                value = value.get(part)
            else:
                return default

        return value if value is not None else default