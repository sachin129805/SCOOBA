from ai.engine import AIEngine
from planner.planner import Planner


ai = AIEngine()

planner = Planner()


command = "open youtube and search for avicii and play the third video"


print(
    "\n" + "=" * 60
)

print(
    "COMMAND:",
    command
)

print(
    "=" * 60
)


decision = ai.think(
    command
)


print(
    "\nMAIN DECISION:"
)

print(
    decision
)


tasks = planner.create_plan(
    decision
)


print(
    f"\nTASK COUNT: {len(tasks)}"
)

for i, task in enumerate(
    tasks,
    start=1
):

    print(
        f"\nTask {i}"
    )

    print(
        f"Skill    : {task.skill}"
    )

    print(
        f"Action   : {task.action}"
    )

    print(
        f"Entity   : {task.entity}"
    )

    print(
        f"Query    : {task.query}"
    )

    print(
        f"Position : {task.position}"
    )