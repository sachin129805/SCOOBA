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

        # ==================================================
        # CONTEXT
        # ==================================================
        #
        # These values remember information from
        # previous steps.
        #
        # Example:
        #
        # open youtube
        # and search pokemon
        #
        # Step 1:
        # target = youtube
        #
        # Step 2:
        # target = youtube
        # query  = pokemon
        #
        # ==================================================

        current_target = None

        current_query = None

        # ==================================================
        # PROCESS EACH STEP
        # ==================================================

        for step in decision.steps:

            print(
                "\n🧠 Processing planner step:"
            )

            print(
                f"   Intent   : {step.intent}"
            )

            print(
                f"   Entity   : {step.entity}"
            )

            print(
                f"   Target   : {step.target}"
            )

            print(
                f"   Query    : {step.query}"
            )

            print(
                f"   Position : {step.position}"
            )

            # ==================================================
            # OPEN APP
            # ==================================================

            if step.intent == "OPEN_APP":

                # ------------------------------------------
                # Determine application
                # ------------------------------------------

                target = (
                    step.target
                    or step.entity
                )

                if target:

                    target = (
                        target
                        .lower()
                        .strip()
                    )

                    current_target = target

                # ------------------------------------------
                # Create task
                # ------------------------------------------

                if target:

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

                # ------------------------------------------
                # SAVE PREVIOUS TARGET
                # ------------------------------------------

                previous_target = (
                    current_target
                )

                # ------------------------------------------
                # Determine explicit target
                # ------------------------------------------
                #
                # Priority:
                #
                # 1. step.target
                # 2. step.entity
                # 3. previously opened target
                # 4. Google fallback
                #
                # ------------------------------------------

                explicit_target = (
                    step.target
                    or step.entity
                )

                if explicit_target:

                    target = explicit_target

                else:

                    target = (
                        current_target
                        or "google"
                    )

                # ------------------------------------------
                # Normalize target
                # ------------------------------------------

                target = (
                    target
                    .lower()
                    .strip()
                )

                # ------------------------------------------
                # Determine query
                # ------------------------------------------

                query = (
                    step.query
                    or current_query
                )

                if query:

                    query = (
                        query
                        .strip()
                    )

                    current_query = query

                # ------------------------------------------
                # Update active target
                # ------------------------------------------

                current_target = target

                # ------------------------------------------
                # DEBUG
                # ------------------------------------------

                print(
                    "\n🔍 SEARCH CONTEXT"
                )

                print(
                    f"   Previous target : "
                    f"{previous_target}"
                )

                print(
                    f"   Step target     : "
                    f"{step.target}"
                )

                print(
                    f"   Step entity     : "
                    f"{step.entity}"
                )

                print(
                    f"   Final target    : "
                    f"{target}"
                )

                print(
                    f"   Query           : "
                    f"{query}"
                )

                # ------------------------------------------
                # CREATE SEARCH TASK
                # ------------------------------------------

                if query:

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

                # ------------------------------------------
                # Determine target
                # ------------------------------------------

                target = (
                    step.target
                    or step.entity
                    or current_target
                    or "youtube"
                )

                target = (
                    target
                    .lower()
                    .strip()
                )

                # ------------------------------------------
                # Determine query
                # ------------------------------------------

                query = (
                    step.query
                    or current_query
                )

                if query:

                    query = (
                        query
                        .strip()
                    )

                    current_query = query

                # ------------------------------------------
                # Update target
                # ------------------------------------------

                current_target = target

                # ------------------------------------------
                # Position
                # ------------------------------------------

                position = (
                    step.position
                    or 1
                )

                # ------------------------------------------
                # DEBUG
                # ------------------------------------------

                print(
                    "\n🎬 VIDEO CONTEXT"
                )

                print(
                    f"   Target   : {target}"
                )

                print(
                    f"   Query    : {query}"
                )

                print(
                    f"   Position : {position}"
                )

                # ------------------------------------------
                # Play first
                # ------------------------------------------

                if position == 1:

                    action = (
                        "play_first"
                    )

                # ------------------------------------------
                # Play specific result
                # ------------------------------------------

                else:

                    action = (
                        "play_video"
                    )

                # ------------------------------------------
                # Create task
                # ------------------------------------------

                if query:

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

                entity = (
                    step.entity
                    or step.target
                )

                tasks.append(
                    Task(
                        skill="filesystem",
                        action="create_folder",
                        entity=entity
                    )
                )

            # ==================================================
            # CREATE FILE
            # ==================================================

            elif step.intent == "CREATE_FILE":

                entity = (
                    step.entity
                    or step.target
                )

                tasks.append(
                    Task(
                        skill="filesystem",
                        action="create_file",
                        entity=entity
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

        # ==================================================
        # PRINT PLAN
        # ==================================================

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

            query = (
                decision.query
            )

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

                # ------------------------------------------
                # First result
                # ------------------------------------------

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

                # ------------------------------------------
                # Specific result
                # ------------------------------------------

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

            query = (
                decision.query
            )

            if query:

                tasks.append(
                    Task(
                        skill="browser",
                        action="search",
                        entity=target,
                        query=query
                    )
                )

        # ==================================================
        # OPEN APP
        # ==================================================

        elif decision.intent == "OPEN_APP":

            entity = (
                decision.entity
                or decision.target
            )

            if entity:

                tasks.append(
                    Task(
                        skill="browser",
                        action="open",
                        entity=entity
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
        # PRINT PLAN
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