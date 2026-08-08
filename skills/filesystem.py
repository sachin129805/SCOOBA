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

        try:

            path = Path(name)

            path.mkdir(
                parents=True,
                exist_ok=True
            )

            return True

        except Exception as e:

            print(f"❌ {e}")

            return False

    def create_file(self, filename):

        try:

            path = Path(filename)

            path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            path.touch(
                exist_ok=True
            )

            return True

        except Exception as e:

            print(f"❌ {e}")

            return False