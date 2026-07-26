from planner.planner import Planner
from planner.executor import Executor

planner = Planner()
executor = Executor()

tasks = planner.create_plan(
    "Create Python project called WeatherApp"
)

executor.execute(tasks)

print()

for task in tasks:
    print(task)