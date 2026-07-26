from planner.planner import Planner

planner = Planner()

tasks = planner.create_plan(

    "Create Python Project"

)

print()

for task in tasks:

    print(task)