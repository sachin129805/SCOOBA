"""
==================================================
SCOOBA

Application Learning

Learns new applications by asking the user
to select the executable once.

Author: Sachin
==================================================
"""

from tkinter import Tk, filedialog

from launcher.database import ApplicationDatabase


class ApplicationLearning:

    def __init__(self):

        self.db = ApplicationDatabase()

    def learn(self, app_name):

        root = Tk()

        root.withdraw()

        root.attributes("-topmost", True)

        path = filedialog.askopenfilename(

            title=f"Locate '{app_name}'",

            filetypes=[

                ("Executable", "*.exe"),

                ("All Files", "*.*")

            ]

        )

        root.destroy()

        if not path:

            return None

        self.db.add(app_name.lower(), path)

        self.db.save()

        print("\n========================================")
        print("New Application Learned")
        print("Name :", app_name)
        print("Path :", path)
        print("========================================\n")

        return path