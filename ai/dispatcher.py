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

    # ==================================================
    # RESPONSE
    # ==================================================

    def response(
        self,
        decision,
        success=None
    ):

        intent = getattr(
            decision,
            "intent",
            None
        )

        entity = getattr(
            decision,
            "entity",
            None
        )

        query = getattr(
            decision,
            "query",
            None
        )

        position = getattr(
            decision,
            "position",
            None
        )

        response = self.personality.speak(
            intent=intent,
            entity=entity,
            query=query,
            position=position,
            success=success
        )

        self.personality.remember(
            decision,
            success
        )

        return response