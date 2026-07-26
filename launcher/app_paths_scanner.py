"""
==================================================
SCOOBA

Windows App Paths Scanner

Scans:
HKLM/HKCU
SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths

Author: Sachin
==================================================
"""

import winreg

from launcher.database import ApplicationDatabase
from launcher.validator import ApplicationValidator


class AppPathsScanner:

    KEYS = [

        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"
        ),

        (
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"
        )

    ]

    def __init__(self):

        self.db = ApplicationDatabase()
        self.validator = ApplicationValidator()

    def scan(self):

        added = 0

        for root, path in self.KEYS:

            try:

                key = winreg.OpenKey(root, path)

            except Exception:
                continue

            count = winreg.QueryInfoKey(key)[0]

            for i in range(count):

                try:

                    subkey = winreg.EnumKey(key, i)

                    appkey = winreg.OpenKey(key, subkey)

                    try:

                        exe = winreg.QueryValue(appkey, None)

                    except Exception:
                        continue

                    exe = self.validator.clean_path(exe)

                    name = subkey.lower()

                    if name.endswith(".exe"):
                        name = name[:-4]

                    if not self.validator.is_valid(name, exe):
                        continue

                    if not self.db.exists(name):

                        self.db.add(name, exe)
                        added += 1

                except Exception:
                    pass

        self.db.save()

        print("\n========================================")
        print("App Paths Added :", added)
        print("Database Size   :", self.db.count())
        print("========================================")


if __name__ == "__main__":

    AppPathsScanner().scan()