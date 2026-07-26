from planner.planner import Planner
from planner.executor import Executor

planner = Planner()

executor = Executor()

tasks = planner.create_plan("Open Chrome")

executor.execute(tasks)

print()

print("Final Status")

print("----------------")

for task in tasks:

    print(task)