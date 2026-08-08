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

        command = (
            decision.command
            or ""
        ).lower().strip()

        # ---------------------------------
        # PLAY VIDEO
        # ---------------------------------

        if decision.intent == "PLAY_VIDEO":

            query = decision.query

            if query:

                tasks.append(
                    Task(
                        skill="browser",
                        action="play_first",
                        entity=(
                            decision.target
                            or "youtube"
                        ),
                        query=query
                    )
                )

        # ---------------------------------
        # MULTI-STEP BROWSER SEARCH
        # ---------------------------------

        elif (
            decision.intent == "SEARCH"
        ):

            compound_markers = [
                " and search for ",
                " and search ",
                " and find ",
                " and look for "
            ]

            compound_marker = None

            for marker in compound_markers:

                if marker in command:

                    compound_marker = marker

                    break

            if (
                compound_marker
                and decision.entity
                and decision.query
            ):

                opening_part = command.split(
                    compound_marker,
                    1
                )[0].strip()

                opening_part = (
                    opening_part
                    .replace(
                        "open ",
                        "",
                        1
                    )
                    .replace(
                        "launch ",
                        "",
                        1
                    )
                    .replace(
                        "start ",
                        "",
                        1
                    )
                    .replace(
                        "run ",
                        "",
                        1
                    )
                    .strip()
                )

                tasks.append(
                    Task(
                        skill="browser",
                        action="open",
                        entity=opening_part
                    )
                )

                tasks.append(
                    Task(
                        skill="browser",
                        action="search",
                        entity=(
                            decision.target
                            or decision.entity
                        ),
                        query=decision.query
                    )
                )

            else:

                target = (
                    decision.target
                    or decision.entity
                    or "google"
                )

                tasks.append(
                    Task(
                        skill="browser",
                        action="search",
                        entity=target,
                        query=decision.query
                    )
                )

        # ---------------------------------
        # OPEN APP
        # ---------------------------------

        elif decision.intent == "OPEN_APP":

            tasks.append(
                Task(
                    skill="browser",
                    action="open",
                    entity=decision.entity
                )
            )

        # ---------------------------------
        # CREATE FOLDER
        # ---------------------------------

        elif decision.intent == "CREATE_FOLDER":

            tasks.append(
                Task(
                    skill="filesystem",
                    action="create_folder",
                    entity=decision.entity
                )
            )

        # ---------------------------------
        # CREATE FILE
        # ---------------------------------

        elif decision.intent == "CREATE_FILE":

            tasks.append(
                Task(
                    skill="filesystem",
                    action="create_file",
                    entity=decision.entity
                )
            )

        # ---------------------------------
        # CREATE PYTHON PROJECT
        # ---------------------------------

        elif (
            decision.intent
            == "CREATE_PYTHON_PROJECT"
        ):

            project_name = (
                decision.target
                or decision.entity
            )

            tasks.extend([

                Task(
                    skill="developer",
                    action="create_project",
                    entity=project_name
                ),

                Task(
                    skill="developer",
                    action="create_venv",
                    entity=project_name
                ),

                Task(
                    skill="developer",
                    action="open_cursor",
                    entity=project_name
                )

            ])

        # ---------------------------------
        # DEBUG PLAN
        # ---------------------------------

        print(
            "\n========== PLAN =========="
        )

        if not tasks:

            print(
                "No tasks generated."
            )

        else:

            for i, task in enumerate(
                tasks,
                start=1
            ):

                print(
                    f"{i}. "
                    f"{task.skill} -> "
                    f"{task.action} "
                    f"({task.entity})"
                )

                if task.query:

                    print(
                        f"   Query: "
                        f"{task.query}"
                    )

        print(
            "==========================\n"
        )

        return tasks