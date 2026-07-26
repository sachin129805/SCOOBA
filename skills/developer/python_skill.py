"""
==================================================
SCOOBA

Python Project Skill

Author: Sachin
==================================================
"""

import re

from planner.task import Task


class PythonSkill:

    def can_handle(self, text):

        return "python project" in text.lower()

    def plan(self, text):

        text = text.lower()

        match = re.search(
            r"(?:called|named)\s+([a-zA-Z0-9_-]+)",
            text
        )

        project = "PythonProject"

        if match:
            project = match.group(1)

        return [

            Task("OPEN_APP", "visual studio code"),

            Task(
                "CREATE_PROJECT",
                project,
                {
                    "template": "python"
                }
            )

        ]