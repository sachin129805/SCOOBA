from planner.planner import Planner
from planner.executor import Executor

planner = Planner()
executor = Executor()

tasks = planner.create_plan(
    "Create Python Project"
)

executor.execute(tasks)

print("\nFinal Status")
print("-" * 30)

for task in tasks:
    print(task)