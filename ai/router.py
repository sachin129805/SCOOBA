"""
==================================================
SCOOBA

AI Router

Author: Sachin
==================================================
"""


class AIRouter:

    def route(self, decision):

        if decision.intent == "OPEN_APP":

            websites = [

                "youtube",
                "github",
                "gmail",
                "chatgpt"

            ]

            if decision.entity in websites:

                return "browser"

            return "desktop"

        if decision.intent == "GREETING":

            return "greeting"

        if decision.intent == "MEMORY":

            return "memory"

        return "brain"