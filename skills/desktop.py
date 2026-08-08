"""
==================================================
SCOOBA

Desktop Skill

Author: Sachin
==================================================
"""

from launcher.v4.resolver import ApplicationResolver
from launcher.v4.launcher import WindowsLauncher


class DesktopSkill:

    def __init__(self):

        self.resolver = ApplicationResolver()
        self.launcher = WindowsLauncher()

    def open(self, app_name: str) -> bool:

        app_name = app_name.lower().strip()

        print("\n========== DESKTOP ==========")
        print("Requested :", app_name)

        app = self.resolver.resolve(app_name)

        print("Resolver Returned :", app)

        if app is None:

            print("Application not found.")
            print("=============================\n")
            return False

        success = self.launcher.open(app)

        print("Launch :", success)
        print("=============================\n")

        return success