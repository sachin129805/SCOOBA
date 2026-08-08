"""
=========================================
SCOOBA

Workspace Manager
=========================================
"""

from pathlib import Path

from config.manager import ConfigManager


class Workspace:

    def __init__(self):

        config = ConfigManager()

        self.root = Path(
            config.get("workspace")
        )

        self.root.mkdir(
            parents=True,
            exist_ok=True
        )

    def project(self, name):

        return self.root / name