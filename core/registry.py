"""
==================================================
SCOOBA

Skill Registry
==================================================
"""

class SkillRegistry:

    def __init__(self):

        self._handlers = {}

    def register(self, intent, handler):

        self._handlers[intent] = handler

    def execute(self, decision):

        handler = self._handlers.get(decision.intent)

        if handler is None:

            raise ValueError(
                f"No handler registered for '{decision.intent}'"
            )

        return handler(decision.entity)