"""
==================================================
SCOOBA

Executable Scanner V4

Author: Sachin
==================================================
"""

import os

from launcher.database import ApplicationDatabase
from launcher.validator import ApplicationValidator
from launcher.filters import should_skip


SEARCH_DIRS = [

    r"C:\Program Files",
    r"C:\Program Files (x86)",
    os.path.expandvars(r"%LOCALAPPDATA%")

]


class ExecutableScanner:

    def __init__(self):

        self.db = ApplicationDatabase()
        self.validator = ApplicationValidator()

    def scan(self):

        upgraded = 0
        added = 0
        skipped = 0

        existing = self.db.all()

        for root in SEARCH_DIRS:

            if not os.path.exists(root):
                continue

            for path, dirs, files in os.walk(root):

                dirs[:] = [

                    d for d in dirs

                    if d.lower() not in (

                        "__pycache__",
                        "cache",
                        "temp",
                        "tmp",
                        "logs"

                    )

                ]

                for file in files:

                    if not file.lower().endswith(".exe"):
                        continue

                    exe = os.path.join(path, file)

                    if should_skip(exe):
                        skipped += 1
                        continue

                    exe = self.validator.clean_path(exe)

                    if not self.validator.is_valid(file, exe):
                        skipped += 1
                        continue

                    name = os.path.splitext(file)[0].lower()

                    if name in existing:

                        old = existing[name]

                        # Prefer a real executable over uninstall/icon paths
                        if (
                            "uninstall" in old.lower()
                            or ".ico" in old.lower()
                            or ".url" in old.lower()
                            or old.lower().endswith(".lnk")
                        ):

                            self.db.add(name, exe)
                            upgraded += 1

                    else:

                        self.db.add(name, exe)
                        added += 1

        self.db.save()

        print("\n========================================")
        print("Applications Upgraded :", upgraded)
        print("New Applications      :", added)
        print("Skipped               :", skipped)
        print("Database Size         :", self.db.count())
        print("========================================")


if __name__ == "__main__":

    ExecutableScanner().scan()