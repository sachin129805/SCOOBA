"""
==================================================
SCOOBA

Plan Executor

Author: Sachin
==================================================
"""


class Executor:

    def execute(self, tasks):

        print("\n========== PLAN ==========")

        for i, task in enumerate(tasks, start=1):

            print(
                f"{i}. "
                f"{task.skill} -> "
                f"{task.action} "
                f"({task.entity})"
            )

        print("==========================\n")