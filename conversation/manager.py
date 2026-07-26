"""
==================================================
SCOOBA

Conversation Manager

Author: Sachin
==================================================
"""


class ConversationManager:

    def __init__(self):

        self.history = []

    def add(self, role, message):

        self.history.append({

            "role": role,

            "message": message

        })

    def last(self):

        if not self.history:

            return None

        return self.history[-1]

    def clear(self):

        self.history.clear()

    def all(self):

        return self.history