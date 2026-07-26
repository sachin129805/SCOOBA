from planner.task import Task


task = Task(

    action="OPEN_APP",

    target="chrome"

)

print(task)

task.complete()

print(task)