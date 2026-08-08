from ai.engine import AIEngine
from planner.planner import Planner
from planner.executor import Executor
from skills.manager import SkillManager


ai = AIEngine()

planner = Planner()

skills = SkillManager()

executor = Executor(
    skills
)


command = "open youtube and search avicii"


print("\n" + "=" * 60)
print("COMMAND:", command)
print("=" * 60)


# ---------------------------------
# AI
# ---------------------------------

decision = ai.think(
    command
)


# ---------------------------------
# PLAN
# ---------------------------------

tasks = planner.create_plan(
    decision
)


# ---------------------------------
# EXECUTE
# ---------------------------------

success = executor.execute(
    tasks
)


# ---------------------------------
# RESULT
# ---------------------------------

print(
    "\nFinal Result:",
    "SUCCESS"
    if success
    else
    "FAILED"
)