"""
=========================================
SCOOBA

Python Project Builder
=========================================
"""

import shutil
import subprocess

from developer.workspace import Workspace
from developer.vscode import VSCode
from config.manager import ConfigManager


class PythonBuilder:

    def __init__(self):

        self.workspace = Workspace()

        self.vscode = VSCode()

        self.config = ConfigManager()

    def create(self, name):

        project = self.workspace.project(name)

        project.mkdir(
            parents=True,
            exist_ok=True
        )

        (project / "main.py").write_text(
            'print("Hello from SCOOBA!")\n',
            encoding="utf-8"
        )

        (project / "README.md").write_text(
            f"# {name}\n",
            encoding="utf-8"
        )

        (project / "requirements.txt").write_text(
            "",
            encoding="utf-8"
        )

        (project / ".gitignore").write_text(
            ".venv/\n__pycache__/\n*.pyc\n",
            encoding="utf-8"
        )

        if self.config.get("developer", "create_venv"):

            subprocess.run(
                [
                    "python",
                    "-m",
                    "venv",
                    ".venv"
                ],
                cwd=project
            )

        if self.config.get("developer", "create_git"):

            if shutil.which("git"):

                subprocess.run(
                    [
                        "git",
                        "init"
                    ],
                    cwd=project
                )

        if self.config.get("developer", "open_after_create"):

            self.vscode.open_project(project)

        return project