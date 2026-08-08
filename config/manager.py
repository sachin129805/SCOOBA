"""
=========================================
SCOOBA

Configuration Manager
=========================================
"""

import json
from pathlib import Path


class ConfigManager:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if hasattr(self, "_loaded"):
            return

        self.path = Path(__file__).parent / "config.json"

        with open(self.path, "r", encoding="utf-8") as file:
            self.data = json.load(file)

        self._loaded = True

    def get(self, *keys):

        value = self.data

        for key in keys:
            value = value[key]

        return value

    def set(self, *keys, value):

        data = self.data

        for key in keys[:-1]:
            data = data[key]

        data[keys[-1]] = value

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)