"""
==================================================
SCOOBA

Application Memory

Author: Sachin
==================================================
"""

import json
from pathlib import Path


class ApplicationMemory:

    def __init__(self):

        self.file = Path("memory/apps.json")

        if not self.file.exists():

            self.file.parent.mkdir(
                exist_ok=True
            )

            self.file.write_text(
                "{}",
                encoding="utf8"
            )

    def load(self):

        with open(
            self.file,
            "r",
            encoding="utf8"
        ) as f:

            return json.load(f)

    def save(self, data):

        with open(
            self.file,
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

    def remember(self, name, path):

        data = self.load()

        data[name.lower()] = path

        self.save(data)

    def recall(self, name):

        data = self.load()

        return data.get(
            name.lower()
        )

    def all(self):

        return self.load()