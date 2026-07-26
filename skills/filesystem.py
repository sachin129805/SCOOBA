"""
==================================================
SCOOBA

Filesystem Skill

Author: Sachin
==================================================
"""

from pathlib import Path


class FileSystemSkill:

    def create_folder(self, name):

        path = Path(name)

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path.exists()

    def create_file(self, filename):

        path = Path(filename)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        path.touch(
            exist_ok=True
        )

        return path.exists()