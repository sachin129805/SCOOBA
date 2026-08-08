"""
=========================================================
SCOOBA

Memory Manager

Author : Sachin
=========================================================
"""

import json
from pathlib import Path


class MemoryManager:

    def __init__(self):

        self.path = Path(__file__).parent / "database.json"

        self.load()

    def load(self):

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as file:

            self.data = json.load(file)

    def save(self):

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.data,
                file,
                indent=4
            )

    def remember_project(

        self,

        name,

        path,

        language

    ):

        self.data["projects"].append(

            {

                "name": name,

                "path": str(path),

                "language": language

            }

        )

        self.save()

    def find_project(

        self,

        name

    ):

        for project in self.data["projects"]:

            if project["name"].lower() == name.lower():

                return project

        return None