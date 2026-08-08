"""
==================================================
SCOOBA V4

Application Database

Author: Sachin
==================================================
"""

import json
from pathlib import Path


class ApplicationDatabase:

    def __init__(self):

        self.path = Path("launcher/v4/apps.json")

        self.apps = {}

        self.load()

    def load(self):

        if self.path.exists():

            with open(
                self.path,
                "r",
                encoding="utf-8"
            ) as f:

                self.apps = json.load(f)

        else:

            self.apps = {}

    def save(self):

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.apps,
                f,
                indent=4,
                sort_keys=True
            )

    def add(self, name, path, source):

        name = name.lower().strip()

        self.apps[name] = {

            "path": path,
            "source": source

        }

    def get(self, name):

        return self.apps.get(
            name.lower()
        )

    def exists(self, name):

        return name.lower() in self.apps

    def all(self):

        return self.apps

    def count(self):

        return len(self.apps)

    def clear(self):

        self.apps = {}
        self.save()


if __name__ == "__main__":

    db = ApplicationDatabase()

    print("Applications :", db.count())