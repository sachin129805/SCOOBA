"""
==================================================
SCOOBA V4

Start Menu Scanner

Author: Sachin
==================================================
"""

from pathlib import Path

from launcher.v4.database import ApplicationDatabase


class StartMenuScanner:

    FOLDERS = [

        Path(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"),

        Path.home() /
        r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs"

    ]

    BAD_WORDS = [

        "uninstall",
        "documentation",
        "readme",
        "release notes",
        "website",
        "help",
        "sample",
        "examples",
        "manual"

    ]

    def __init__(self):

        self.db = ApplicationDatabase()

    def valid(self, name):

        name = name.lower()

        for word in self.BAD_WORDS:

            if word in name:
                return False

        return True

    def scan(self):

        added = 0

        for folder in self.FOLDERS:

            if not folder.exists():
                continue

            for shortcut in folder.rglob("*.lnk"):

                name = shortcut.stem.strip()

                if not self.valid(name):
                    continue

                if not self.db.exists(name):

                    self.db.add(
                        name,
                        str(shortcut),
                        "startmenu"
                    )

                    added += 1

        self.db.save()

        print("\n========================================")
        print("Start Menu Applications :", added)
        print("Database Size           :", self.db.count())
        print("========================================")


if __name__ == "__main__":

    StartMenuScanner().scan()