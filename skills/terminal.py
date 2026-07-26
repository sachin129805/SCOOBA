"""
==================================================
SCOOBA

Terminal Skill

Author: Sachin
==================================================
"""

import subprocess


class TerminalSkill:

    def run(self, command, cwd=None):

        try:

            print(f"\n💻 Running : {command}")

            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True
            )

            if result.stdout.strip():
                print(result.stdout)

            if result.stderr.strip():
                print(result.stderr)

            return result.returncode == 0

        except Exception as e:

            print(e)

            return False