"""
==================================================
SCOOBA

Application Scanner

Author: Sachin
==================================================
"""

import os
import json


class ApplicationScanner:

    OUTPUT_FILE = "scanner/apps.json"

    SEARCH_PATHS = [

        os.path.join(
            os.environ.get("ProgramFiles", ""),
            ""
        ),

        os.path.join(
            os.environ.get("ProgramFiles(x86)", ""),
            ""
        ),

        os.path.join(
            os.environ.get("APPDATA", ""),
            ""
        ),

        os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            ""
        ),

        os.path.join(
            os.environ.get(
                "ProgramData",
                ""
            ),
            "Microsoft",
            "Windows",
            "Start Menu",
            "Programs"
        )

    ]

    def scan(self):

        apps = {}

        for root in self.SEARCH_PATHS:

            if not os.path.exists(root):
                continue

            for path, dirs, files in os.walk(root):

                for file in files:

                    if file.endswith(".exe"):

                        name = os.path.splitext(file)[0].lower()

                        if name not in apps:

                            apps[name] = os.path.join(
                                path,
                                file
                            )

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

        return len(apps)