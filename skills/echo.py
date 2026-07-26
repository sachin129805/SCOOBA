"""
==================================================
SCOOBA

Echo Skill

Author: Sachin
==================================================
"""

from sdk.skill import Skill


class EchoSkill(Skill):

    @property
    def name(self):

        return "echo"

    def can_handle(self, decision):

        return decision.intent == "ECHO"

    def execute(self, decision):

        print("Echo Skill Executed")

        return True