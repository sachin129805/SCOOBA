"""
==================================================
SCOOBA

Task Executor

Author: Sachin
==================================================
"""

from launcher.resolver import ApplicationResolver
from launcher.windows_launcher import WindowsLauncher
from skills.filesystem import FileSystemSkill
from skills.terminal import TerminalSkill


class Executor:

    def __init__(self):

        self.resolver = ApplicationResolver()
        self.launcher = WindowsLauncher()
        self.filesystem = FileSystemSkill()
        self.terminal = TerminalSkill()

    def execute(self, tasks):

        for task in tasks:

            print(f"\nExecuting : {task}")

            if task.action == "OPEN_APP":

                print("\n========== EXECUTOR ==========")
                print("Target :", task.target)

                path = self.resolver.resolve(task.target)

                print("Resolved Path :", path)

                if path:

                    result = self.launcher.open(path)

                    print("Launch Result :", result)

                    if result:
                        task.complete()
                    else:
                        task.fail()

                else:

                    print("Application not found.")
                    task.fail()

                print("==============================")

            elif task.action == "CREATE_FOLDER":

                success = self.filesystem.create_folder(task.target)

                if success:
                    print(f"✅ Folder created : {task.target}")
                    task.complete()
                else:
                    task.fail()

            elif task.action == "CREATE_FILE":

                success = self.filesystem.create_file(task.target)

                if success:
                    print(f"✅ File created : {task.target}")
                    task.complete()
                else:
                    task.fail()

            elif task.action == "RUN_COMMAND":

                success = self.terminal.run(
                    task.target,
                    cwd=task.params.get("cwd")
                )

                if success:
                    task.complete()
                else:
                    task.fail()

        return tasks