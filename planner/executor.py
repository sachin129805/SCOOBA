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

        print("\n========== PLAN ==========")

        if not tasks:

            print("No tasks to execute.")
            print("==========================\n")

            return False

        overall_success = True

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

            # ---------------------------------
            # Execute Task
            # ---------------------------------

            success = self.skills.execute_task(
                task
            )

            if success:

                print(
                    f"   ✅ Task {i} completed."
                )

            else:

                print(
                    f"   ❌ Task {i} failed."
                )

                overall_success = False

                # Stop plan execution if a
                # previous task fails.

                break

        print("==========================\n")

        return overall_success