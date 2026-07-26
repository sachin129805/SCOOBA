"""
==================================================
SCOOBA

Context Engine

Author: Sachin
==================================================
"""


class ContextEngine:

    def __init__(self):

        self.context = {}

    def set(self, key, value):

        self.context[key] = value

    def get(self, key):

        return self.context.get(key)

    def clear(self):

        self.context.clear()

    def dump(self):

        return self.context