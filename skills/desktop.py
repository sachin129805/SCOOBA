"""
==================================================
SCOOBA

Desktop Skill

Author: Sachin
==================================================
"""

from launcher.resolver import ApplicationResolver
from launcher.windows_launcher import WindowsLauncher
from launcher.learning import ApplicationLearning


class DesktopSkill:

    def __init__(self):

        self.resolver = ApplicationResolver()
        self.launcher = WindowsLauncher()
        self.learning = ApplicationLearning()

    def open(self, app_name: str) -> bool:

        app_name = app_name.lower().strip()

        print("\n========== DESKTOP ==========")
        print("Requested :", app_name)

        # -----------------------------
        # Try Existing Database
        # -----------------------------

        path = self.resolver.resolve(app_name)

        # -----------------------------
        # Learn if Missing
        # -----------------------------

        if path is None:

            print("Application not found.")
            print("Opening file picker...")

            path = self.learning.learn(app_name)

            if path is None:

                print("Learning cancelled.")
                print("=============================\n")

                return False

        print("Resolved :", path)

        # -----------------------------
        # Launch
        # -----------------------------

        success = self.launcher.open(path)

        print("Launch :", success)
        print("=============================\n")

        return success