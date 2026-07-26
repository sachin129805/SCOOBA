"""
==================================================
SCOOBA

NLP Processor

Author: Sachin
==================================================
"""

import spacy

from ai.nlp.intents import INTENTS


class NLPProcessor:

    def __init__(self):

        self.nlp = spacy.load("en_core_web_sm")

    def process(self, text: str):

        doc = self.nlp(text.lower())

        result = {
            "intent": None,
            "lemmas": [],
            "tokens": []
        }

        # -----------------------------
        # Extract Tokens & Lemmas
        # -----------------------------

        for token in doc:

            result["tokens"].append(token.text)
            result["lemmas"].append(token.lemma_)

        # -----------------------------
        # Detect Intent
        # -----------------------------

        for intent, data in INTENTS.items():

            if any(
                lemma in data["verbs"]
                for lemma in result["lemmas"]
            ):

                result["intent"] = intent
                break

        # -----------------------------
        # Debug
        # -----------------------------

        print("\n========== NLP DEBUG ==========")

        for token in doc:

            print(
                f"{token.text:<15}"
                f"POS={token.pos_:<10}"
                f"Lemma={token.lemma_}"
            )

        print("===============================\n")

        return result