"""
==================================================
SCOOBA

AI Engine

Author: Sachin
==================================================
"""

from ai.nlp.processor import NLPProcessor
from ai.normalizer.resolver import EntityResolver
from ai.decision import Decision


class AIEngine:

    def __init__(self):

        self.processor = NLPProcessor()
        self.resolver = EntityResolver()

    def think(self, text: str) -> Decision:

        result = self.processor.process(text)

        decision = Decision()

        decision.intent = result["intent"]

        entity = None

        # Try each token
        for token in result["tokens"]:

            candidate = self.resolver.resolve(token)

            if candidate:

                entity = candidate
                break

        # Try the whole sentence if no token matched
        if entity is None:

            entity = self.resolver.resolve(text)

        decision.entity = entity

        decision.confidence = 1.0 if decision.intent else 0.0

        return decision