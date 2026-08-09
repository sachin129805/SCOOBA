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

        print(
            "\n========== EXECUTION =========="
        )

        if not tasks:

            print(
                "No tasks to execute."
            )

            print(
                "================================"
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
                f"Skill    : "
                f"{task.skill}"
            )

            print(
                f"Action   : "
                f"{task.action}"
            )

            print(
                f"Entity   : "
                f"{task.entity}"
            )

            if task.query:

                print(
                    f"Query    : "
                    f"{task.query}"
                )

            if task.position:

                print(
                    f"Position : "
                    f"{task.position}"
                )

            success = (
                self.skills.execute_task(
                    task
                )
            )

            if success:

                print(
                    f"✅ Task {i} completed."
                )

            else:

                print(
                    f"❌ Task {i} failed."
                )

                overall_success = False

                print(
                    "⚠ Plan execution stopped."
                )

                break

        print(
            "\n================================"
        )

        return overall_success