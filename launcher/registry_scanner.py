"""
==================================================
SCOOBA

Registry Scanner V3

Author: Sachin
==================================================
"""

import winreg

from launcher.database import ApplicationDatabase
from launcher.validator import ApplicationValidator


class RegistryScanner:

    UNINSTALL_KEYS = [

        (winreg.HKEY_LOCAL_MACHINE,
         r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),

        (winreg.HKEY_LOCAL_MACHINE,
         r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),

        (winreg.HKEY_CURRENT_USER,
         r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")

    ]

    def __init__(self):

        self.db = ApplicationDatabase()
        self.validator = ApplicationValidator()

    def scan(self):

        added = 0

        for root, path in self.UNINSTALL_KEYS:

            try:

                key = winreg.OpenKey(root, path)

            except Exception:
                continue

            count = winreg.QueryInfoKey(key)[0]

            for i in range(count):

                try:

                    sub = winreg.EnumKey(key, i)

                    app = winreg.OpenKey(key, sub)

                    try:
                        name = winreg.QueryValueEx(app, "DisplayName")[0]
                    except Exception:
                        continue

                    exe = None

                    for field in [

                        "DisplayIcon",
                        "InstallLocation",
                        "DisplayIcon"

                    ]:

                        try:

                            value = winreg.QueryValueEx(app, field)[0]

                            if value:

                                exe = value
                                break

                        except Exception:
                            pass

                    if not exe:
                        continue

                    exe = self.validator.clean_path(exe)

                    if not self.validator.is_valid(name, exe):
                        continue

                    if not self.db.exists(name):

                        self.db.add(name, exe)
                        added += 1

                except Exception:
                    pass

        self.db.save()

        print("\n========================================")
        print("Registry Apps Added :", added)
        print("Database Size       :", self.db.count())
        print("========================================")


if __name__ == "__main__":

    RegistryScanner().scan()