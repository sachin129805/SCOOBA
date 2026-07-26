"""
==================================================
SCOOBA

AI Dispatcher

Author: Sachin
==================================================
"""

from personality.engine import PersonalityEngine


class AIDispatcher:

    def __init__(self):

        self.personality = PersonalityEngine()

    def response(self, decision):

        if decision.intent == "GREETING":

            return self.personality.speak("GREETING")

        elif decision.intent == "OPEN_APP":

            return self.personality.speak(
                "OPEN_APP",
                decision.entity
            )

        return self.personality.speak("UNKNOWN")