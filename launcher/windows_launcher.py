"""
==================================================
SCOOBA

Windows Launcher

Author: Sachin
==================================================
"""

import os
import subprocess


class WindowsLauncher:

    def open(self, path: str):

        if not path:
            return False

        try:

            # Microsoft Store App (AUMID)
            if "!" in path:

                subprocess.Popen([
                    "explorer.exe",
                    f"shell:AppsFolder\\{path}"
                ])

                return True

            # Normal EXE / Shortcut / Folder
            os.startfile(path)

            return True

        except Exception as e:

            print(f"Launch Error : {e}")

            return False