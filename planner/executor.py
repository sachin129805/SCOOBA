"""
==================================================
SCOOBA

Plan Executor

Author: Sachin
==================================================
"""

from skills.manager import SkillManager


class Executor:

    def __init__(self, skills=None):

        self.skills = (
            skills
            if skills is not None
            else SkillManager()
        )

    def execute(self, tasks):

        print("\n========== EXECUTION ==========")

        if not tasks:

            print(
                "No tasks to execute."
            )

            print(
                "================================\n"
            )

            return False

        overall_success = True

        for i, task in enumerate(
            tasks,
            start=1
        ):

            print(
                f"\n▶ Task {i}"
            )

            print(
                f"  Skill    : {task.skill}"
            )

            print(
                f"  Action   : {task.action}"
            )

            print(
                f"  Entity   : {task.entity}"
            )

            if task.query:

                print(
                    f"  Query    : {task.query}"
                )

            # ---------------------------------
            # Execute Task
            # ---------------------------------

            success = (
                self.skills.execute_task(
                    task
                )
            )

            if success:

                print(
                    f"  ✅ Task {i} completed."
                )

            else:

                print(
                    f"  ❌ Task {i} failed."
                )

                overall_success = False

                # Stop execution when a
                # previous task fails.

                print(
                    "\n⚠ Plan execution stopped."
                )

                break

        print(
            "\n================================\n"
        )

        return overall_success