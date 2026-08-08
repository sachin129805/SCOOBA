"""
==================================================
SCOOBA

AI Engine

Author: Sachin
==================================================
"""

from ai.nlp.processor import NLPProcessor
from ai.decision import Decision

from launcher.v4.resolver import ApplicationResolver


class AIEngine:

    def __init__(self):

        self.processor = NLPProcessor()

        self.app_resolver = ApplicationResolver()

    def think(self, text: str) -> Decision:

        # ---------------------------------
        # Speech Normalization
        # ---------------------------------

        text = text.lower().strip()

        replacements = {

            # WhatsApp
            "what's up": "whatsapp",
            "whats up": "whatsapp",
            "what up": "whatsapp",
            "what's app": "whatsapp",
            "whats app": "whatsapp",
            "what app": "whatsapp",
            "what sap": "whatsapp",
            "whatsup": "whatsapp",

            # LinkedIn
            "linked in": "linkedin",

            # Microsoft Office
            "power point": "powerpoint",
            "microsoft word": "word",
            "micro soft word": "word",
            "microsoft excel": "excel",
            "micro soft excel": "excel",

            # Development
            "vs code": "visual studio code",
            "visual studio": "visual studio code",
            "git hub": "github"
        }

        for wrong, correct in replacements.items():

            text = text.replace(
                wrong,
                correct
            )

        # ---------------------------------
        # NLP
        # ---------------------------------

        result = self.processor.process(
            text
        )

        decision = Decision()

        decision.intent = result["intent"]

        decision.entity = result["entity"]

        decision.query = result.get(
            "query"
        )

        decision.target = result.get(
            "target"
        )

        # ---------------------------------
        # Resolve Application
        # ---------------------------------

        if decision.intent == "OPEN_APP":

            # IMPORTANT:
            #
            # If NLP already detected an
            # application, preserve it.
            #
            # Example:
            #
            # "youtube and search for good day"
            #
            # NLP gives:
            #
            # entity = youtube
            # query  = good day
            #
            # We must NOT overwrite entity
            # with the entire sentence.

            if not decision.entity:

                words = (
                    text
                    .replace("open", "")
                    .replace("launch", "")
                    .replace("start", "")
                    .replace("run", "")
                    .strip()
                )

                # ---------------------------------
                # Remove Search Portion
                # ---------------------------------

                search_markers = [
                    " and search for ",
                    " and search ",
                    " search for ",
                    " search ",
                    " and find ",
                    " and look for "
                ]

                for marker in search_markers:

                    if marker in words:

                        words = words.split(
                            marker,
                            1
                        )[0].strip()

                        break

                # ---------------------------------
                # Resolve Complete App Name
                # ---------------------------------

                app = self.app_resolver.resolve(
                    words
                )

                if app:

                    decision.entity = words

                else:

                    # ---------------------------------
                    # Resolve Individual Tokens
                    # ---------------------------------

                    for token in result["tokens"]:

                        app = self.app_resolver.resolve(
                            token
                        )

                        if app:

                            decision.entity = (
                                token.lower()
                            )

                            break

        # ---------------------------------
        # Confidence
        # ---------------------------------

        decision.confidence = (
            1.0
            if decision.intent
            else 0.0
        )

        # ---------------------------------
        # Debug
        # ---------------------------------

        print("\n========== AI DECISION ==========")

        print(
            f"Intent      : "
            f"{decision.intent}"
        )

        print(
            f"Entity      : "
            f"{decision.entity}"
        )

        print(
            f"Query       : "
            f"{decision.query}"
        )

        print(
            f"Target      : "
            f"{decision.target}"
        )

        print(
            f"Confidence  : "
            f"{decision.confidence}"
        )

        print(
            "=================================\n"
        )

        return decision