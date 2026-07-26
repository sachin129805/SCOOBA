"""
==================================================
SCOOBA

Application Validator

Filters invalid launcher entries.

Author: Sachin
==================================================
"""

import os


class ApplicationValidator:

    BAD_WORDS = [

        "uninstall",
        "uninstaller",
        "setup",
        "installer",
        "update",
        "updater",
        "repair",
        "remove",
        "crashpad",
        "helper",
        "documentation",
        "readme",
        "release notes",
        "website",
        "manual",
        "sample",
        "example"

    ]

    VALID_EXTENSIONS = [

        ".exe",
        ".lnk"

    ]

    def clean_path(self, path: str):

        if not path:
            return None

        path = path.strip().strip('"')

        # Remove icon index (e.g. chrome.exe,0)
        if ".exe," in path.lower():
            path = path.split(",")[0]

        return path

    def is_valid(self, name: str, path: str):

        if not name or not path:
            return False

        name = name.lower()
        path = self.clean_path(path).lower()

        # Microsoft Store App (AUMID)
        if "!" in path:
            return True

        # Reject bad names
        for word in self.BAD_WORDS:
            if word in name:
                return False

        # Reject bad paths
        for word in self.BAD_WORDS:
            if word in path:
                return False

        # Reject icons and urls
        if path.endswith(".ico"):
            return False

        if path.endswith(".url"):
            return False

        # Allow shortcuts
        if path.endswith(".lnk"):
            return True

        # Allow executables
        if path.endswith(".exe"):
            return True

        return False