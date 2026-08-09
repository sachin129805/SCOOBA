"""
==================================================
SCOOBA

Planner

Author: Sachin
==================================================
"""

from planner.task import Task


class Planner:

    # ==================================================
    # CREATE PLAN
    # ==================================================

    def create_plan(self, decision):

        # ==================================================
        # MULTI-STEP COMMAND
        # ==================================================

        if (
            getattr(
                decision,
                "steps",
                None
            )
            and
            len(decision.steps) > 1
        ):

            return self.create_multi_step_plan(
                decision
            )

        # ==================================================
        # SINGLE COMMAND
        # ==================================================

        return self.create_single_plan(
            decision
        )

    # ==================================================
    # MULTI-STEP PLAN
    # ==================================================

    def create_multi_step_plan(
        self,
        decision
    ):

        tasks = []

        # --------------------------------------------------
        # Context
        #
        # Used when a later command omits information.
        #
        # Example:
        #
        # search for avicii
        # and play the third video
        #
        # The second step inherits:
        #
        # query = avicii
        #
        # --------------------------------------------------

        current_target = None

        current_query = None

        for step in decision.steps:

            # ==================================================
            # OPEN APP
            # ==================================================

            if step.intent == "OPEN_APP":

                target = (
                    step.entity
                    or step.target
                )

                if target:

                    current_target = (
                        target
                    )

                tasks.append(
                    Task(
                        skill="browser",
                        action="open",
                        entity=target
                    )
                )

            # ==================================================
            # SEARCH
            # ==================================================

            elif step.intent == "SEARCH":

                target = (
                    step.target
                    or step.entity
                    or current_target
                    or "google"
                )

                query = (
                    step.query
                    or current_query
                )

                if query:

                    current_query = (
                        query
                    )

                if target:

                    current_target = (
                        target
                    )

                tasks.append(
                    Task(
                        skill="browser",
                        action="search",
                        entity=target,
                        query=query
                    )
                )

            # ==================================================
            # PLAY VIDEO
            # ==================================================

            elif step.intent == "PLAY_VIDEO":

                target = (
                    step.target
                    or step.entity
                    or current_target
                    or "youtube"
                )

                query = (
                    step.query
                    or current_query
                )

                position = (
                    step.position
                    or 1
                )

                # --------------------------------------------------
                # Play first
                # --------------------------------------------------

                if position == 1:

                    action = "play_first"

                else:

                    action = "play_video"

                tasks.append(
                    Task(
                        skill="browser",
                        action=action,
                        entity=target,
                        query=query,
                        position=position
                    )
                )

            # ==================================================
            # CREATE FOLDER
            # ==================================================

            elif step.intent == "CREATE_FOLDER":

                tasks.append(
                    Task(
                        skill="filesystem",
                        action="create_folder",
                        entity=(
                            step.entity
                            or step.target
                        )
                    )
                )

            # ==================================================
            # CREATE FILE
            # ==================================================

            elif step.intent == "CREATE_FILE":

                tasks.append(
                    Task(
                        skill="filesystem",
                        action="create_file",
                        entity=(
                            step.entity
                            or step.target
                        )
                    )
                )

            # ==================================================
            # CREATE PYTHON PROJECT
            # ==================================================

            elif (
                step.intent
                == "CREATE_PYTHON_PROJECT"
            ):

                project_name = (
                    step.target
                    or step.entity
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

        self.print_plan(
            tasks
        )

        return tasks

    # ==================================================
    # SINGLE PLAN
    # ==================================================

    def create_single_plan(
        self,
        decision
    ):

        tasks = []

        # ==================================================
        # PLAY VIDEO
        # ==================================================

        if decision.intent == "PLAY_VIDEO":

            query = decision.query

            position = (
                decision.position
                or 1
            )

            target = (
                decision.target
                or decision.entity
                or "youtube"
            )

            if query:

                if position == 1:

                    tasks.append(
                        Task(
                            skill="browser",
                            action="play_first",
                            entity=target,
                            query=query,
                            position=1
                        )
                    )

                else:

                    tasks.append(
                        Task(
                            skill="browser",
                            action="play_video",
                            entity=target,
                            query=query,
                            position=position
                        )
                    )

        # ==================================================
        # SEARCH
        # ==================================================

        elif decision.intent == "SEARCH":

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

        # ==================================================
        # OPEN APP
        # ==================================================

        elif decision.intent == "OPEN_APP":

            tasks.append(
                Task(
                    skill="browser",
                    action="open",
                    entity=decision.entity
                )
            )

        # ==================================================
        # CREATE FOLDER
        # ==================================================

        elif decision.intent == "CREATE_FOLDER":

            tasks.append(
                Task(
                    skill="filesystem",
                    action="create_folder",
                    entity=decision.entity
                )
            )

        # ==================================================
        # CREATE FILE
        # ==================================================

        elif decision.intent == "CREATE_FILE":

            tasks.append(
                Task(
                    skill="filesystem",
                    action="create_file",
                    entity=decision.entity
                )
            )

        # ==================================================
        # CREATE PYTHON PROJECT
        # ==================================================

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

        # ==================================================
        # DEBUG
        # ==================================================

        self.print_plan(
            tasks
        )

        return tasks

    # ==================================================
    # PRINT PLAN
    # ==================================================

    def print_plan(
        self,
        tasks
    ):

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

                if getattr(
                    task,
                    "position",
                    None
                ):

                    print(
                        f"   Position: "
                        f"{task.position}"
                    )

        print(
            "==========================\n"
        )