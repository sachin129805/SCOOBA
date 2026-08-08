"""
==================================================
SCOOBA V4

Windows Launcher

Author: Sachin
==================================================
"""

import os
import subprocess
import webbrowser


class WindowsLauncher:

    def open(self, app):

        if app is None:
            return False

        if isinstance(app, dict):
            path = app.get("path")
        else:
            path = app

        if not path:
            return False

        path = path.lower().strip()

        try:

            # ---------------------------------
            # Built-in Apps
            # ---------------------------------

            if path == "linkedin":
                webbrowser.open("https://www.linkedin.com/feed/")
                return True

            if path == "youtube":
                webbrowser.open("https://www.youtube.com/")
                return True

            if path == "gmail":
                webbrowser.open("https://mail.google.com/")
                return True

            if path == "chatgpt":
                webbrowser.open("https://chat.openai.com/")
                return True

            if path == "whatsapp":

                subprocess.Popen([
                    "explorer.exe",
                    "shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"
                ])

                return True

            # ---------------------------------
            # Windows executables
            # ---------------------------------

            if path in ("notepad.exe", "calc.exe", "mspaint.exe"):
                os.startfile(path)
                return True

            # ---------------------------------
            # Store App AUMID
            # ---------------------------------

            if "!" in path:

                subprocess.Popen([
                    "explorer.exe",
                    f"shell:AppsFolder\\{path}"
                ])

                return True

            # ---------------------------------
            # Shortcut
            # ---------------------------------

            if path.endswith(".lnk"):
                os.startfile(path)
                return True

            # ---------------------------------
            # Executable
            # ---------------------------------

            if path.endswith(".exe"):
                os.startfile(path)
                return True

            return False

        except Exception as e:

            print("Launch Error:", e)
            return False