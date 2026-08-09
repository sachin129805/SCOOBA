"""
==================================================
SCOOBA

PLAY VIDEO TEST

Author: Sachin
==================================================
"""

from ai.engine import AIEngine
from planner.planner import Planner
from planner.executor import Executor
from skills.manager import SkillManager


# ==================================================
# INITIALIZE
# ==================================================

ai = AIEngine()

planner = Planner()

skills = SkillManager()

executor = Executor(
    skills
)


# ==================================================
# TEST COMMAND
# ==================================================

commands = [

    "Michael Jackson and play the seventh video",

]


# ==================================================
# RUN TESTS
# ==================================================

for command in commands:

    print(
        "\n"
        + "=" * 60
    )

    print(
        "COMMAND:",
        command
    )

    print(
        "=" * 60
    )

    # ----------------------------------------------
    # AI
    # ----------------------------------------------

    decision = ai.think(
        command
    )

    print(
        "\nDECISION:"
    )

    print(
        decision
    )

    # ----------------------------------------------
    # PLAN
    # ----------------------------------------------

    tasks = planner.create_plan(
        decision
    )

    print(
        f"TASK COUNT: "
        f"{len(tasks)}"
    )

    # ----------------------------------------------
    # EXECUTION
    # ----------------------------------------------

    success = executor.execute(
        tasks
    )

    # ----------------------------------------------
    # RESULT
    # ----------------------------------------------

    print(
        "\nFinal Result:",
        "SUCCESS"
        if success
        else
        "FAILED"
    )