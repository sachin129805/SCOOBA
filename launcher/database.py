"""
==================================================
SCOOBA

Application Database

Author: Sachin
==================================================
"""

import json
from pathlib import Path


class ApplicationDatabase:

    def __init__(self):

        self.database = Path("launcher/apps.json")

        self.apps = {}

        self.load()

    def load(self):

        if self.database.exists():

            with open(
                self.database,
                "r",
                encoding="utf8"
            ) as f:

                self.apps = json.load(f)

        else:

            self.apps = {}

    def save(self):

        with open(
            self.database,
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                self.apps,
                f,
                indent=4
            )

    def add(self, name, path):

        self.apps[name.lower()] = path

    def exists(self, name):

        return name.lower() in self.apps

    def get(self, name):

        return self.apps.get(
            name.lower()
        )

    def all(self):

        return self.apps

    def count(self):

        return len(self.apps)