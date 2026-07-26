"""
==================================================
SCOOBA

Task Planner

Author: Sachin
==================================================
"""

import re

from planner.task import Task


class Planner:

    def create_plan(self, text: str):

        text = text.lower().strip()

        tasks = []

        # ----------------------------
        # OPEN APPLICATION
        # ----------------------------

        if text.startswith("open "):

            app = text.replace("open ", "", 1).strip()

            return [
                Task("OPEN_APP", app)
            ]

        # ----------------------------
        # SEARCH WEB
        # ----------------------------

        if text.startswith("search "):

            query = text.replace("search ", "", 1).strip()

            return [
                Task("SEARCH_WEB", query)
            ]

        # ----------------------------
        # CREATE PYTHON PROJECT
        # ----------------------------

        if "python project" in text:

            match = re.search(
                r"(?:called|named)\s+([a-zA-Z0-9_-]+)",
                text
            )

            project = "PythonProject"

            if match:

                project = match.group(1)

            return [

                Task("OPEN_APP", "visual studio code"),

                Task("CREATE_FOLDER", project),

                Task(
                    "RUN_COMMAND",
                    "python -m venv .venv",
                    {
                        "cwd": project
                    }
                ),

                Task(
                    "CREATE_FILE",
                    f"{project}/main.py"
                ),

                Task(
                    "CREATE_FILE",
                    f"{project}/requirements.txt"
                ),

                Task(
                    "RUN_COMMAND",
                    "code .",
                    {
                        "cwd": project
                    }
                )

            ]

        return tasks