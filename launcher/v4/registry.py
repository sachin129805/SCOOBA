"""
==================================================
SCOOBA V4

Registry Scanner

Author: Sachin
==================================================
"""

import winreg

from launcher.v4.database import ApplicationDatabase


class RegistryScanner:

    ROOTS = [

        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        ),

        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ),

        (
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        )

    ]

    BAD_WORDS = [

        "uninstall",
        "installer",
        "setup",
        "update",
        "repair",
        "helper",
        "documentation",
        "readme",
        "website",
        "sample"

    ]

    def __init__(self):

        self.db = ApplicationDatabase()

    def valid(self, name, path):

        if not name or not path:
            return False

        name = name.lower()
        path = path.lower()

        for word in self.BAD_WORDS:

            if word in name:
                return False

            if word in path:
                return False

        if ".exe," in path:
            path = path.split(",")[0]

        if not path.endswith(".exe"):
            return False

        return True

    def scan(self):

        added = 0

        for root, location in self.ROOTS:

            try:

                key = winreg.OpenKey(root, location)

            except Exception:

                continue

            total = winreg.QueryInfoKey(key)[0]

            for i in range(total):

                try:

                    subkey = winreg.EnumKey(key, i)

                    appkey = winreg.OpenKey(key, subkey)

                    try:

                        name = winreg.QueryValueEx(
                            appkey,
                            "DisplayName"
                        )[0]

                    except Exception:

                        continue

                    path = None

                    try:

                        path = winreg.QueryValueEx(
                            appkey,
                            "DisplayIcon"
                        )[0]

                    except Exception:

                        pass

                    if not self.valid(name, path):
                        continue

                    if ".exe," in path:
                        path = path.split(",")[0]

                    self.db.add(
                        name,
                        path,
                        "registry"
                    )

                    added += 1

                except Exception:

                    pass

        self.db.save()

        print("\n========================================")
        print("Registry Applications :", added)
        print("Database Size         :", self.db.count())
        print("========================================")


if __name__ == "__main__":

    RegistryScanner().scan()