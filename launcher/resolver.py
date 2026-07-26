"""
==================================================
SCOOBA

Application Resolver

Author: Sachin
==================================================
"""

from launcher.database import ApplicationDatabase
from memory.apps_memory import ApplicationMemory


class ApplicationResolver:

    def __init__(self):

        self.db = ApplicationDatabase()
        self.memory = ApplicationMemory()

    def resolve(self, app_name):

        app_name = app_name.lower()

        # 1. User Memory
        path = self.memory.recall(app_name)

        if path:
            return path

        # 2. Launcher Database
        path = self.db.get(app_name)

        if path:
            return path

        return None