"""
==================================================
SCOOBA

Shortcut Scanner

Scans Windows Start Menu shortcuts (.lnk)

Author: Sachin
==================================================
"""

import os
import json


class ShortcutScanner:

    OUTPUT_FILE = "scanner/apps.json"

    START_MENU_PATHS = [

        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",

        os.path.join(
            os.environ.get("APPDATA", ""),
            "Microsoft",
            "Windows",
            "Start Menu",
            "Programs"
        )

    ]

    def scan(self):

        if os.path.exists(self.OUTPUT_FILE):

            with open(
                self.OUTPUT_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                apps = json.load(f)

        else:

            apps = {}

        count = 0

        for root in self.START_MENU_PATHS:

            if not os.path.exists(root):
                continue

            for path, dirs, files in os.walk(root):

                for file in files:

                    if file.lower().endswith(".lnk"):

                        name = os.path.splitext(file)[0].lower()

                        full_path = os.path.join(path, file)

                        if name not in apps:

                            apps[name] = full_path

                            count += 1

        with open(
            self.OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                apps,
                f,
                indent=4
            )

        return count