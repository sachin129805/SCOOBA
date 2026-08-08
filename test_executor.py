from ai.engine import AIEngine
from planner.planner import Planner
from planner.executor import Executor
from skills.manager import SkillManager


# ---------------------------------
# Initialize
# ---------------------------------

ai = AIEngine()

planner = Planner()

skills = SkillManager()

executor = Executor(
    skills
)


# ---------------------------------
# Command
# ---------------------------------

command = "search youtube for Avicii"


# ---------------------------------
# AI
# ---------------------------------

print("\n========== COMMAND ==========")
print(command)
print("=============================\n")

decision = ai.think(
    command
)


# ---------------------------------
# Planning
# ---------------------------------

tasks = planner.create_plan(
    decision
)


# ---------------------------------
# Execution
# ---------------------------------

success = executor.execute(
    tasks
)


print(
    f"\nFinal Result: "
    f"{'SUCCESS' if success else 'FAILED'}"
)