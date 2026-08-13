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

        command = getattr(
            decision,
            "command",
            None
        )

        # ==================================================
        # SWITCH PERSONALITY MODE
        # ==================================================

        if intent == "PERSONALITY_MODE":

            mode = getattr(
                decision,
                "personality_mode",
                None
            )

            if mode:

                changed = (
                    self.personality.set_mode(
                        mode
                    )
                )

                if changed:

                    return (
                        f"Personality mode switched "
                        f"to {mode}."
                    )

            return (
                "I couldn't change the personality mode."
            )

        # ==================================================
        # GET CURRENT PERSONALITY MODE
        # ==================================================

        if intent == "GET_PERSONALITY_MODE":

            mode = (
                self.personality.get_mode()
            )

            return (
                f"I'm currently in "
                f"{mode.replace('_', ' ').lower()} mode."
            )

        # ==================================================
        # NORMAL RESPONSE
        # ==================================================

        response = (
            self.personality.speak(

                intent=intent,

                entity=entity,

                query=query,

                position=position,

                success=success,

                command=command

            )
        )

        # ==================================================
        # MEMORY
        # ==================================================

        self.personality.remember(
            decision,
            success
        )

        return response