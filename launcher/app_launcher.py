"""
==================================================
SCOOBA

Universal Launcher

Author: Sachin
==================================================
"""

import os
import json
import subprocess


class Launcher:

    DATABASE = "scanner/apps.json"

    def __init__(self):

        if os.path.exists(self.DATABASE):

            with open(
                self.DATABASE,
                "r",
                encoding="utf-8"
            ) as f:

                self.apps = json.load(f)

        else:

            self.apps = {}

    def launch(self, app_name):

        app_name = app_name.lower()

        if app_name not in self.apps:

            return False

        target = self.apps[app_name]

        try:

            os.startfile(target)

            return True

        except Exception as e:

            print(e)

            return False