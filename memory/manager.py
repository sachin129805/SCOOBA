"""
==================================================
SCOOBA

Memory Manager

Author: Sachin
==================================================
"""

import json
import os


class MemoryManager:

    FILE = "memory/storage.json"

    def __init__(self):

        if not os.path.exists(self.FILE):

            with open(self.FILE, "w") as f:

                json.dump({}, f)

    def load(self):

        with open(self.FILE, "r") as f:

            return json.load(f)

    def save(self, data):

        with open(self.FILE, "w") as f:

            json.dump(data, f, indent=4)

    def remember(self, key, value):

        data = self.load()

        data[key] = value

        self.save(data)

    def recall(self, key):

        data = self.load()

        return data.get(key)