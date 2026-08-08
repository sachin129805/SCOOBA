"""
==================================================
SCOOBA

NLP Processor

Author: Sachin
==================================================
"""

import spacy

from ai.intent.classifier import IntentClassifier


class NLPProcessor:

    def __init__(self):

        self.nlp = spacy.load(
            "en_core_web_sm"
        )

        self.classifier = IntentClassifier()

    def process(self, text: str):

        text = text.lower().strip()

        doc = self.nlp(text)

        result = {
            "intent": None,
            "entity": None,
            "query": None,
            "target": None,
            "lemmas": [],
            "tokens": []
        }

        # ---------------------------------
        # Extract Tokens & Lemmas
        # ---------------------------------

        for token in doc:

            result["tokens"].append(
                token.text
            )

            result["lemmas"].append(
                token.lemma_
            )

        # ---------------------------------
        # Intent Classification
        # ---------------------------------

        result["intent"] = self.classifier.classify(
            result["lemmas"]
        )

        # ---------------------------------
        # Browser Applications
        # ---------------------------------

        browser_sites = [
            "youtube",
            "github",
            "gmail",
            "chatgpt",
            "google"
        ]

        for site in browser_sites:

            if site in text:

                result["entity"] = site

                break

        # ---------------------------------
        # Browser Search Query
        # ---------------------------------

        search_markers = [
            "search for",
            "look for",
            "search",
            "find"
        ]

        for marker in search_markers:

            if marker in text:

                query = text.split(
                    marker,
                    1
                )[1].strip()

                # Remove trailing punctuation
                query = query.rstrip(
                    ".,!?;:"
                ).strip()

                if query:

                    result["query"] = query

                break

        # ---------------------------------
        # File / Folder / Project
        # ---------------------------------

        if result["intent"] in (
            "CREATE_PYTHON_PROJECT",
            "CREATE_FOLDER",
            "CREATE_FILE"
        ):

            keywords = [
                "called",
                "named",
                "project",
                "folder",
                "file"
            ]

            for keyword in keywords:

                if keyword in text:

                    entity = text.split(
                        keyword,
                        1
                    )[1].strip()

                    entity = entity.rstrip(
                        ".,!?;:"
                    ).strip()

                    if entity:

                        result["entity"] = entity

                        break

        # ---------------------------------
        # Debug
        # ---------------------------------

        print("\n========== NLP DEBUG ==========")

        for token in doc:

            print(
                f"{token.text:<15}"
                f"POS={token.pos_:<10}"
                f"Lemma={token.lemma_}"
            )

        print("--------------------------------")
        print("Intent :", result["intent"])
        print("Entity :", result["entity"])
        print("Query  :", result["query"])
        print("Target :", result["target"])
        print("===============================\n")

        return result