"""
==================================================
SCOOBA

Entity Resolver

Uses Launcher Database

Author: Sachin
==================================================
"""

from rapidfuzz import process

from launcher.database import ApplicationDatabase


class EntityResolver:

    def __init__(self):

        self.db = ApplicationDatabase()

        self.entities = list(self.db.all().keys())

    def resolve(self, entity):

        if not entity:
            return None

        entity = entity.lower().strip()

        # Exact Match
        if entity in self.entities:
            return entity

        # Fuzzy Match
        match = process.extractOne(
            entity,
            self.entities,
            score_cutoff=75
        )

        if match:
            return match[0]

        return None