"""
==================================================
SCOOBA

Planner

Author: Sachin
==================================================
"""

from planner.task import Task


class Planner:

    def create_plan(self, decision):

        tasks = []

        if decision.intent == "OPEN_APP":

            tasks.append(
                Task(
                    skill="desktop",
                    action="open",
                    entity=decision.entity
                )
            )

        elif decision.intent == "CREATE_FOLDER":

            tasks.append(
                Task(
                    skill="filesystem",
                    action="create_folder",
                    entity=decision.entity
                )
            )

        elif decision.intent == "CREATE_FILE":

            tasks.append(
                Task(
                    skill="filesystem",
                    action="create_file",
                    entity=decision.entity
                )
            )

        elif decision.intent == "CREATE_PYTHON_PROJECT":

            tasks.extend([

                Task(
                    "developer",
                    "create_project",
                    decision.entity
                ),

                Task(
                    "developer",
                    "create_venv",
                    decision.entity
                ),

                Task(
                    "developer",
                    "open_cursor",
                    decision.entity
                )

            ])

        return tasks