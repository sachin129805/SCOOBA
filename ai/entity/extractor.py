"""
==================================================
SCOOBA

Application Entity Extractor

Author: Sachin
==================================================
"""

from rapidfuzz import process


class EntityExtractor:

    def extract(self, text, candidates):

        text = text.lower()

        if not candidates:
            return None

        names = list(candidates.keys())

        # Best fuzzy match
        match = process.extractOne(
            text,
            names,
            score_cutoff=70
        )

        if match:
            return match[0]

        return None